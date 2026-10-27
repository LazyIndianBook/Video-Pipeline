#!/usr/bin/env python3
"""safe_zone_check.py - element boxes vs safe-zone tokens; holds, reveal sync, caption overlap, camera fx (stdlib).

Usage:
  python3 safe_zone_check.py --tokens 12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json \
      --boxes jobs/<scene>/qa/elements.json [--zones zones.json] [--platform all|<name>] [--require-measured] \
      [--indic-hold-factor 1.5] [--cues cue_sheet.json] [--out safe_zone_report.json]
  python3 safe_zone_check.py --selftest

elements.json: {"canvas": {"width":1080,"height":1920}, "elements": [{"id","role","x","y","w","h",
  "visible": [[t0,t1],...], "zone": "title|visual|caption" (optional), "lang": "hi-IN" (optional),
  "reading_end_s": <s> (equations: when narration finishes reading it), "cue_id": <id> (optional),
  "answer": true (optional; also inferred from the cue sheet's meta.answer_protection)}],
  "camera": [{"t", "scale", "tx", "ty"}] (optional)} - a DOM dump taken by seeking the scene
  at every cue boundary (roles: headline, text, caption, label, equation, critical, decor).
Tokens: {"canvas":{...}, "insets":{"top","bottom","left","right"}} or {"platforms": {name: {"insets": {...}}}};
  null/missing inset = unmeasured ("measure per platform, no verified pixel values", report 7.9).
Checks: canvas bounds; text-like roles inside the safe rect (#51); side margin >= zones.side_margin_min_px (96, tokens);
  headline hold >= 1.2 s [N60] (x factor for Indic, [Recommendation]); equation visible until reading_end + 0.5 s
  (report 7.5) (#50); optional zone membership; captions never covering a label/equation while both show (#51);
  with --cues, each element carrying cue_id first appears within one frame of its cue (#63), and an answer element
  visible before its cue is CRITICAL (early answer reveal, 15 Oct 2026); optional "camera"
  samples [{t, scale, tx, ty}] flag push-ins/shakes while labels or equations are visible (#64).
Severity: critical blocks release; major blocks unless a named reviewer waives it; minor is logged. Exit codes: 0 no critical/major, 1 otherwise, 2 usage/IO error.
"""
import argparse, json, sys

TEXT_ROLES = {"headline", "text", "caption", "label", "equation", "critical"}
SCIENCE_ROLES = {"label", "equation", "critical"}
SIDE_MIN_PX = 96          # fallback; the harness token zones.side_margin_min_px wins (one owner, 15 Oct 2026)
HEADLINE_HOLD_S = 1.2     # [N60] example figure
EQUATION_TAIL_S = 0.5     # report 7.5 [Recommendation]
INDIC = ("hi", "as", "bn")


def load_insets(tokens, platform="all"):
    """Return (insets dict or None if unmeasured, canvas, notes). Union (max) of platforms for 'all'."""
    canvas = dict(tokens.get("canvas") or {"width": 1080, "height": 1920})
    if "width" not in canvas and "width_px" in canvas:
        canvas["width"] = canvas["width_px"]
    if "height" not in canvas and "height_px" in canvas:
        canvas["height"] = canvas["height_px"]
    forced_unmeasured = False
    if "insets" in tokens:
        sets = {"default": tokens["insets"]}
    elif "platforms" in tokens:
        sets = {k: (v.get("insets", v) if isinstance(v, dict) else {}) for k, v in tokens["platforms"].items()}
    elif "platform_insets_px" in tokens:
        # Harness shape (04_harness_contract/vertical_safe_zones.tokens.json): per-platform inset dicts plus a
        # top-level "measured" flag. Placeholder values count as UNMEASURED until measured is true (#51).
        pip = tokens["platform_insets_px"]
        sets = {k: v for k, v in pip.items()
                if isinstance(v, dict) and all(e in v for e in ("top", "bottom", "left", "right"))}
        if not sets:
            raise ValueError("platform_insets_px has no per-platform inset dicts")
        forced_unmeasured = not bool(pip.get("measured", False))
    else:
        raise ValueError("unrecognised token shape: expected 'insets', 'platforms' or 'platform_insets_px'")
    if platform != "all":
        if platform not in sets:
            raise ValueError(f"platform {platform!r} not in tokens ({sorted(sets)})")
        sets = {platform: sets[platform]}
    out, unmeasured = {}, []
    for side in ("top", "bottom", "left", "right"):
        vals = [s.get(side) for s in sets.values()]
        if any(v is None for v in vals):
            unmeasured.append(side)
        else:
            out[side] = max(vals)
    if forced_unmeasured and not unmeasured:
        unmeasured = ["placeholder:" + s for s in ("top", "bottom", "left", "right")]
    return (None if unmeasured else out), canvas, unmeasured


def side_min(tokens):
    v = (tokens.get("zones") or {}).get("side_margin_min_px")
    return v if isinstance(v, (int, float)) else SIDE_MIN_PX


def safe_rect(insets, canvas, side=SIDE_MIN_PX):
    left = max(insets["left"], side)
    right = max(insets["right"], side)
    return {"x": left, "y": insets["top"], "w": canvas["width"] - left - right,
            "h": canvas["height"] - insets["top"] - insets["bottom"]}


def inside(e, r, tol=0.5):
    return (e["x"] >= r["x"] - tol and e["y"] >= r["y"] - tol and
            e["x"] + e["w"] <= r["x"] + r["w"] + tol and e["y"] + e["h"] <= r["y"] + r["h"] + tol)


def _overlap(a, b):
    return a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]


def _co_visible(a, b):
    return any(s0 < t1 and t0 < s1 for s0, s1 in a.get("visible", []) for t0, t1 in b.get("visible", []))


def check(tokens, boxes, zones=None, platform="all", require_measured=False, indic_factor=1.5, cues=None):
    defects = []

    def add(sev, eid, msg, edge):
        defects.append({"severity": sev, "element": eid, "edge_case": edge, "message": msg})
    insets, canvas, unmeasured = load_insets(tokens, platform)
    canvas_r = {"x": 0, "y": 0, "w": canvas["width"], "h": canvas["height"]}
    if insets is None:
        add("critical" if require_measured else "major", None,
            f"safe-zone insets unmeasured for {unmeasured}: cannot certify (#51); phone review by a named reviewer required", "#51")
        rect = None
    else:
        rect = safe_rect(insets, canvas, side_min(tokens))
    for e in boxes["elements"]:
        role, eid = e.get("role", "decor"), e.get("id")
        if role != "decor" and not inside(e, canvas_r):
            add("critical", eid, "outside the canvas", "#51")
            continue
        if rect and role in TEXT_ROLES and not inside(e, rect):
            add("critical" if role in SCIENCE_ROLES else "major", eid,
                f"{role} outside the safe rect {rect} (platform UI may hide it)", "#51")
        if zones and e.get("zone"):
            z = zones["zones"].get(e["zone"])
            if z is None or not inside(e, z):
                add("minor", eid, f"not inside its declared zone {e['zone']!r}", "#49")
        spans = e.get("visible", [])
        if role == "headline":
            need = HEADLINE_HOLD_S * (indic_factor if str(e.get("lang", "")).split("-")[0] in INDIC else 1.0)
            for t0, t1 in spans:
                if t1 - t0 < need - 1e-6:
                    add("major", eid, f"headline readable {t1 - t0:.2f} s < {need:.2f} s hold", "#50")
        if role == "equation" and e.get("reading_end_s") is not None and spans:
            if max(t1 for _, t1 in spans) < e["reading_end_s"] + EQUATION_TAIL_S - 1e-6:
                add("major", eid, f"equation leaves before narration end + {EQUATION_TAIL_S} s", "#50")
    els = boxes["elements"]
    sci = [e for e in els if e.get("role") in SCIENCE_ROLES]
    for c in (e for e in els if e.get("role") == "caption"):  # captions must not cover science while both show
        for e in sci:
            if _overlap(c, e) and _co_visible(c, e):
                add("major", c.get("id"), f"caption overlaps {e.get('id')} while both are visible", "#51")
    if cues:  # reveal lands on its cue: first visible frame within one frame of cue.at (report 5.5, [V4-MP] 8)
        at = {c["id"]: c["at"] for c in cues.get("cues", [])}
        frame = 1.0 / cues.get("fps", 30)
        answer_cues = {a.get("cue_id") for a in (cues.get("meta") or {}).get("answer_protection", [])}
        for e in els:
            cid = e.get("cue_id")
            if cid and e.get("visible"):
                first = min(t0 for t0, _ in e["visible"])
                if cid not in at:
                    add("major", e.get("id"), f"cue {cid!r} not in the cue sheet", "#63")
                elif (e.get("answer") or cid in answer_cues) and first < at[cid] - 1e-6:
                    # 15 Oct 2026 (audit science-safety-12): an early answer reveal is CRITICAL, never waivable
                    add("critical", e.get("id"), f"answer visible at {first:.3f}s before its cue {at[cid]:.3f}s "
                        "(early answer reveal: the protected think window is broken)", "#63")
                elif abs(first - at[cid]) > frame + 1e-6:
                    add("major", e.get("id"), f"first visible at {min(t0 for t0, _ in e['visible']):.3f}s, cue at {at[cid]:.3f}s (> 1 frame)", "#63")
    for cam in boxes.get("camera", []):  # #64: no push-in/shake while a label or equation is on screen
        moved = abs(cam.get("scale", 1.0) - 1.0) > 1e-3 or abs(cam.get("tx", 0)) > 0.5 or abs(cam.get("ty", 0)) > 0.5
        if moved:
            hit = [e.get("id") for e in sci if any(t0 <= cam["t"] <= t1 for t0, t1 in e.get("visible", []))]
            if hit:
                add("major", None, f"camera transform at t={cam['t']}s while {hit} visible (geometry may be misread)", "#64")
    worst = "critical" if any(d["severity"] == "critical" for d in defects) else \
        "major" if any(d["severity"] == "major" for d in defects) else "minor" if defects else "pass"
    return {"safe_rect": rect, "canvas": canvas, "platform": platform, "unmeasured": unmeasured,
            "defects": defects, "severity": worst}


def selftest():
    tokens = {"canvas": {"width": 1080, "height": 1920},
              "platforms": {"p1": {"insets": {"top": 200, "bottom": 380, "left": 40, "right": 120}},
                            "p2": {"insets": {"top": 250, "bottom": 300, "left": 60, "right": 60}}}}
    ins, can, um = load_insets(tokens)
    assert ins == {"top": 250, "bottom": 380, "left": 60, "right": 120} and not um
    r = safe_rect(ins, can)
    assert r == {"x": 96, "y": 250, "w": 864, "h": 1290}, r
    assert side_min({"zones": {"side_margin_min_px": 110}}) == 110 and side_min({}) == SIDE_MIN_PX
    boxes = {"elements": [
        {"id": "title", "role": "headline", "x": 100, "y": 300, "w": 800, "h": 200, "visible": [[0.0, 1.5]]},
        {"id": "label_n1", "role": "label", "x": 100, "y": 1600, "w": 300, "h": 80, "visible": [[1.0, 4.0]]},
        {"id": "bg", "role": "decor", "x": -50, "y": -50, "w": 1180, "h": 2020},
        {"id": "hook", "role": "headline", "lang": "hi-IN", "x": 100, "y": 300, "w": 800, "h": 200, "visible": [[2.0, 3.5]]},
        {"id": "eq1", "role": "equation", "x": 100, "y": 800, "w": 800, "h": 150, "visible": [[1.0, 3.0]], "reading_end_s": 2.8},
        {"id": "cap", "role": "caption", "zone": "caption", "x": 100, "y": 1400, "w": 800, "h": 100, "visible": [[0, 4]]}]}
    zones = {"zones": {"caption": {"x": 90, "y": 1300, "w": 870, "h": 240}}}
    rep = check(tokens, boxes, zones)
    got = {(d["element"], d["severity"]) for d in rep["defects"]}
    assert ("label_n1", "critical") in got and ("hook", "major") in got and ("eq1", "major") in got, got
    assert not any(e == "title" or e == "bg" or e == "cap" for e, _ in got), got
    assert rep["severity"] == "critical"
    extra = {"camera": [{"t": 2.0, "scale": 1.03}, {"t": 0.5, "scale": 1.0}], "elements": [
        {"id": "lbl", "role": "label", "x": 200, "y": 900, "w": 300, "h": 80, "visible": [[1.04, 4.0]], "cue_id": "c1"},
        {"id": "lbl2", "role": "label", "x": 200, "y": 1100, "w": 300, "h": 80, "visible": [[2.5, 4.0]], "cue_id": "c2"},
        {"id": "cap2", "role": "caption", "x": 150, "y": 1090, "w": 800, "h": 100, "visible": [[3.0, 3.5]]}]}
    r2 = check(tokens, extra, cues={"fps": 30, "cues": [{"id": "c1", "at": 1.05}, {"id": "c2", "at": 2.0}]})
    msgs = [(d["element"], d["edge_case"]) for d in r2["defects"]]
    assert ("lbl2", "#63") in msgs and ("lbl", "#63") not in msgs, msgs
    assert ("cap2", "#51") in msgs and (None, "#64") in msgs, msgs
    ans = {"elements": [{"id": "ansB", "role": "text", "x": 200, "y": 900, "w": 300, "h": 80, "visible": [[1.99, 4.0]], "cue_id": "c_ans"}]}
    sheet = {"fps": 30, "cues": [{"id": "c_ans", "at": 2.0}], "meta": {"answer_protection": [{"cue_id": "c_ans"}]}}
    ra = check(tokens, ans, cues=sheet)                                  # 10 ms early: inside one frame, still critical
    assert ra["severity"] == "critical" and any("early answer" in d["message"] for d in ra["defects"]), ra
    ans["elements"][0]["visible"] = [[2.0, 4.0]]
    assert check(tokens, ans, cues=sheet)["severity"] == "pass"
    hf = {"canvas": {"width_px": 1080, "height_px": 1920},
          "platform_insets_px": {"measured": False, "status": "PLACEHOLDER",
                                 "generic_conservative": {"top": 250, "bottom": 450, "left": 60, "right": 120, "status": "P"}}}
    ins_h, can_h, um_h = load_insets(hf)
    assert ins_h is None and um_h and can_h["width"] == 1080 and can_h["height"] == 1920, "harness placeholder shape must load as unmeasured"
    hf["platform_insets_px"]["measured"] = True
    ins_h, _, um_h = load_insets(hf)
    assert ins_h == {"top": 250, "bottom": 450, "left": 60, "right": 120} and not um_h, "harness measured shape must load"
    un = {"insets": {"top": None, "bottom": 300, "left": 40, "right": 40}}
    assert check(un, {"elements": []})["severity"] == "major"
    assert check(un, {"elements": []}, require_measured=True)["severity"] == "critical"
    try:
        load_insets({"safe": 1})
        raise AssertionError("bad token shape must fail")
    except ValueError:
        pass
    print("safe_zone_check selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--tokens")
    ap.add_argument("--boxes")
    ap.add_argument("--zones")
    ap.add_argument("--platform", default="all")
    ap.add_argument("--require-measured", action="store_true")
    ap.add_argument("--indic-hold-factor", type=float, default=1.5)
    ap.add_argument("--cues", help="cue_sheet.json: check each element with cue_id appears within one frame of its cue")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.tokens or not a.boxes:
        ap.print_usage(sys.stderr)
        return 2
    try:
        rd = lambda p: json.load(open(p, encoding="utf-8"))  # noqa: E731
        rep = check(rd(a.tokens), rd(a.boxes), rd(a.zones) if a.zones else None, a.platform,
                    a.require_measured, a.indic_hold_factor, rd(a.cues) if a.cues else None)
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2)
    print(json.dumps(rep, indent=2))
    return 0 if rep["severity"] in ("pass", "minor") else 1


if __name__ == "__main__":
    sys.exit(main())
