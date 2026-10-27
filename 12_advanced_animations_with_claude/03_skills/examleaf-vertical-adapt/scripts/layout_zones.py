#!/usr/bin/env python3
"""layout_zones.py - stacked 9:16 zone rectangles (title / visual / caption) from safe-zone tokens. Stdlib only.

Usage:
  python3 layout_zones.py --tokens 12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json \
        [--platform all|<name>] [--ratios T,V,C] [--gutter 24] [--out zones.json]
  python3 layout_zones.py --tokens T --provisional-insets 200,380,60,60 --out zones.json   # unmeasured tokens only
  python3 layout_zones.py --fit 1920x1080 --zones zones.json        # contain a 16:9 visual group in the visual zone
  python3 layout_zones.py --selftest

Rules: canvas 1080x1920; safe rect = canvas minus platform insets (union over platforms for 'all'); side margin never
below zones.side_margin_min_px; zones stacked top->bottom inside the safe rect. 15 Oct 2026 (audit "Safe-zone geometry
disagrees"): 04_harness_contract/vertical_safe_zones.tokens.json is the ONLY owner of the zone shares
(zones.top_title/middle_visual/bottom_caption.share) and of side_margin_min_px (96); this script reads them and falls
back to its defaults (same values) only when a token file lacks them; --ratios overrides for experiments only.
Gutter is a [Recommendation] starting value - tune in the pilot. Insets have NO verified pixel
values (report 7.9): when tokens are unmeasured the script refuses unless --provisional-insets is given, and then
marks the output provisional (anim-qa treats that as uncertified). --fit always contains, never crops (#49).
Exit codes: 0 ok, 1 refused (JSON on stdout), 2 usage/IO error. Edge cases: #49, #51.
"""
import argparse, hashlib, json, sys

SIDE_MIN_PX = 96                      # fallback only; the token zones.side_margin_min_px wins
DEFAULT_RATIOS = (0.22, 0.54, 0.24)   # fallback only; the token zones.*.share wins (title, visual, caption)
SHARE_KEYS = ("top_title", "middle_visual", "bottom_caption")
DEFAULT_GUTTER = 24                   # [Recommendation]
ZONE_NAMES = ("title", "visual", "caption")


def load_insets(tokens, platform="all"):
    """Same tolerant loader as anim-qa/safe_zone_check.py (kept in sync by hand; skills install independently)."""
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


def token_geometry(tokens):
    """(ratios, side_min_px, source) from the harness token file; defaults only for keys it lacks."""
    z = tokens.get("zones") or {}
    shares = [((z.get(k) or {}).get("share")) for k in SHARE_KEYS]
    ratios = tuple(shares) if all(isinstance(s, (int, float)) for s in shares) else DEFAULT_RATIOS
    side = z.get("side_margin_min_px")
    side = side if isinstance(side, (int, float)) else SIDE_MIN_PX
    src = "tokens" if ratios is not DEFAULT_RATIOS and "side_margin_min_px" in z else "defaults (token keys absent)"
    return ratios, side, src


def zones_for(insets, canvas, ratios=DEFAULT_RATIOS, gutter=DEFAULT_GUTTER, side_min=SIDE_MIN_PX):
    if abs(sum(ratios) - 1.0) > 1e-6 or any(r <= 0 for r in ratios):
        raise ValueError("ratios must be positive and sum to 1")
    left, right = max(insets["left"], side_min), max(insets["right"], side_min)
    safe = {"x": left, "y": insets["top"], "w": canvas["width"] - left - right,
            "h": canvas["height"] - insets["top"] - insets["bottom"]}
    usable = safe["h"] - gutter * (len(ratios) - 1)
    if safe["w"] <= 0 or usable <= 0:
        raise ValueError("insets leave no usable area")
    zones, y = {}, safe["y"]
    for i, (name, r) in enumerate(zip(ZONE_NAMES, ratios)):
        h = usable - sum(z["h"] for z in zones.values()) if i == len(ratios) - 1 else round(usable * r)
        zones[name] = {"x": safe["x"], "y": y, "w": safe["w"], "h": h}
        y += h + gutter
    return safe, zones


def fit(src_w, src_h, dst):
    """Uniform 'contain' scale and centred offset; never crops."""
    s = min(dst["w"] / src_w, dst["h"] / src_h)
    w, h = src_w * s, src_h * s
    return {"scale": round(s, 6), "x": round(dst["x"] + (dst["w"] - w) / 2, 2), "y": round(dst["y"] + (dst["h"] - h) / 2, 2),
            "w": round(w, 2), "h": round(h, 2), "crop": False}


def build(tokens, platform="all", ratios=None, gutter=DEFAULT_GUTTER, provisional=None):
    tok_ratios, side_min, geo_src = token_geometry(tokens)
    if ratios is None:
        ratios = tok_ratios
    else:
        geo_src = "--ratios override (experiment; tokens own production values)"
    insets, canvas, unmeasured = load_insets(tokens, platform)
    is_prov = False
    if insets is None:
        if not provisional:
            raise PermissionError(f"tokens unmeasured for {unmeasured}: measure per platform (no verified pixel values) "
                                  "or pass --provisional-insets top,bottom,left,right for a provisional layout")
        insets, is_prov = dict(zip(("top", "bottom", "left", "right"), provisional)), True
    safe, zones = zones_for(insets, canvas, ratios, gutter, side_min)
    raw = json.dumps(tokens, sort_keys=True).encode()
    return {"canvas": canvas, "platform": platform, "provisional": is_prov, "insets_used": insets,
            "side_min_px": side_min, "safe_rect": safe, "zones": zones, "gutter": gutter, "ratios": list(ratios),
            "geometry_source": geo_src,
            "bleed_rect": {"x": 0, "y": 0, "w": canvas["width"], "h": canvas["height"]},
            "tokens_sha256": hashlib.sha256(raw).hexdigest(),
            "rules": ["text and science-critical parts stay inside their zone; only decor may use bleed_rect",
                      "re-layout, never crop, a 16:9 composition (#49)"]}


def selftest():
    tok = {"canvas": {"width": 1080, "height": 1920},
           "platforms": {"a": {"insets": {"top": 200, "bottom": 380, "left": 40, "right": 40}},
                         "b": {"insets": {"top": 240, "bottom": 300, "left": 100, "right": 60}}}}
    out = build(tok)                       # no zone keys in this token shape -> defaults (same values as the tokens)
    s, z = out["safe_rect"], out["zones"]
    assert s == {"x": 100, "y": 240, "w": 884, "h": 1300}, s
    assert out["geometry_source"].startswith("defaults") and out["ratios"] == list(DEFAULT_RATIOS)
    assert z["title"]["y"] == 240 and z["caption"]["y"] + z["caption"]["h"] == 240 + 1300, z
    assert sum(v["h"] for v in z.values()) + 2 * 24 == 1300 and not out["provisional"]
    assert all(v["x"] >= SIDE_MIN_PX for v in z.values())
    hf = {"canvas": {"width_px": 1080, "height_px": 1920},
          "platform_insets_px": {"measured": False, "status": "PLACEHOLDER",
                                 "generic_conservative": {"top": 250, "bottom": 450, "left": 60, "right": 120, "status": "P"}}}
    ins_h, can_h, um_h = load_insets(hf)
    assert ins_h is None and um_h and can_h["width"] == 1080 and can_h["height"] == 1920, "harness placeholder shape must load as unmeasured"
    hf["platform_insets_px"]["measured"] = True
    ins_h, _, um_h = load_insets(hf)
    assert ins_h == {"top": 250, "bottom": 450, "left": 60, "right": 120} and not um_h, "harness measured shape must load"
    un = {"insets": {"top": None, "bottom": None, "left": None, "right": None}}
    try:
        build(un)
        raise AssertionError("unmeasured tokens must refuse")
    except PermissionError:
        pass
    p = build(un, provisional=(200, 380, 60, 60))
    assert p["provisional"] and p["safe_rect"]["x"] == 96
    # 15 Oct 2026: the real harness token file is the single owner of shares and side margin
    import os
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "04_harness_contract",
                        "vertical_safe_zones.tokens.json")
    if os.path.isfile(real):
        rt = json.load(open(real, encoding="utf-8"))
        r, side, src = token_geometry(rt)
        assert src == "tokens" and side == rt["zones"]["side_margin_min_px"], (src, side)
        assert r == tuple(rt["zones"][k]["share"] for k in SHARE_KEYS) and r == DEFAULT_RATIOS and side == SIDE_MIN_PX, \
            "fallback defaults drifted from the token file"
        rp = build(rt, provisional=(250, 450, 60, 120))
        assert rp["safe_rect"]["x"] == side and rp["geometry_source"] == "tokens"
    custom = dict(hf, zones={"top_title": {"share": 0.3}, "middle_visual": {"share": 0.5}, "bottom_caption": {"share": 0.2},
                             "side_margin_min_px": 120})
    rc = build(custom)
    assert rc["ratios"] == [0.3, 0.5, 0.2] and rc["safe_rect"]["x"] == 120 and rc["side_min_px"] == 120
    f = fit(1920, 1080, z["visual"])
    assert f["w"] <= z["visual"]["w"] + 1e-6 and f["h"] <= z["visual"]["h"] + 1e-6 and not f["crop"]
    assert abs(f["w"] / f["h"] - 16 / 9) < 1e-3
    try:
        zones_for({"top": 0, "bottom": 0, "left": 0, "right": 0}, {"width": 1080, "height": 1920}, (0.5, 0.6, 0.1))
        raise AssertionError("bad ratios")
    except ValueError:
        pass
    print("layout_zones selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--tokens")
    ap.add_argument("--platform", default="all")
    ap.add_argument("--ratios", help="experiment override T,V,C; default = the token file's zones.*.share")
    ap.add_argument("--gutter", type=int, default=DEFAULT_GUTTER)
    ap.add_argument("--provisional-insets")
    ap.add_argument("--fit", help="WxH of a source group to contain in the visual zone, e.g. 1920x1080")
    ap.add_argument("--zones", help="zones.json produced earlier (used with --fit)")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.fit:
            if not a.zones:
                ap.print_usage(sys.stderr)
                return 2
            w, h = (float(v) for v in a.fit.lower().split("x"))
            res = fit(w, h, json.load(open(a.zones, encoding="utf-8"))["zones"]["visual"])
        elif a.tokens:
            prov = tuple(int(v) for v in a.provisional_insets.split(",")) if a.provisional_insets else None
            res = build(json.load(open(a.tokens, encoding="utf-8")), a.platform,
                        tuple(float(v) for v in a.ratios.split(",")) if a.ratios else None, a.gutter, prov)
        else:
            ap.print_usage(sys.stderr)
            return 2
    except PermissionError as e:
        print(json.dumps({"status": "refused", "skill": "examleaf-vertical-adapt", "error": str(e)}, indent=2))
        return 1
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
