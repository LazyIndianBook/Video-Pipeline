#!/usr/bin/env python3
"""build_brief.py - validate an animation brief request and render brief.md (stdlib only).

Usage:
  python3 build_brief.py --request brief_request.json --out-dir jobs/<scene_id>/brief [--template T] [--no-file-checks]
  python3 build_brief.py --selftest

Exit codes: 0 ok, 1 validation failed (blocker JSON on stdout), 2 usage/IO error.
Edge cases enforced: #7 structured brief, #8 font ban, #9 isolated workspace, #11 script read-only,
#12 facts only from fixtures, #50 hold times, #60 iteration cap. Report: RESEARCH_REPORT section 8.
"""
import argparse, hashlib, json, os, re, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
STYLES = {"paper-collage-vertical", "doodle-handdrawn", "editorial-vox", "kinetic-type", "voxel-isometric"}
ROUTES_OK = {"illustrative", "typographic", "data-bound"}
ROUTE_ELSEWHERE = {"spatial-hero": "examleaf-blender-scenes"}
MANDATORY_BANS = {"arial", "inter"}                      # [N51]
CONVERGENCE_FONTS = {"space grotesk"}                    # [N55] ban or rotate
INDIC_LANGS = {"hi-IN", "as-IN", "bn-IN"}
MAX_ITER = 3                                             # report 3.4 "for example 3 fix loops per scene"
FORBIDDEN = [                                            # (#60, #11, #12)
    (r"don'?t stop|do not stop|until (it is |it's )?perfect|until it matches", "#60 unbounded iteration instruction"),
    (r"\bresearch\b|look up|search the web|find facts", "#12 agent research of on-screen facts is forbidden"),
    (r"(re)?write the script|edit the script|improve the narration|change the wording", "#11 approved script is read-only"),
]
INDIC_RE = re.compile(r"[ऀ-ॿঀ-৿]")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _need(d, key, errs, where):
    if not isinstance(d, dict) or key not in d or d[key] in (None, "", []):
        errs.append(f"missing {where}.{key}")
        return None
    return d[key]


def _check_file(ref, label, errs, file_checks):
    if not file_checks or not isinstance(ref, dict):
        return
    p, want = ref.get("path"), ref.get("sha256")
    if not p or not os.path.isfile(p):
        errs.append(f"{label}: file not found: {p}")
    elif want and sha256_file(p) != want:
        errs.append(f"{label}: sha256 mismatch (artifact changed since approval)")


def validate(req, file_checks=True):
    """Return (errors, warnings). Errors block the brief."""
    errs, warns = [], []
    for k in ("scene_id", "language", "route", "script", "style", "cue_sheet", "brand_tokens",
              "fonts", "holds", "iteration_cap", "effort", "workspace"):
        _need(req, k, errs, "request")
    if errs:
        return errs, warns
    # route (storyboard-route owns the tag; we only accept it)
    tag = req["route"].get("tag")
    if tag in ROUTE_ELSEWHERE:
        errs.append(f"route '{tag}' belongs to {ROUTE_ELSEWHERE[tag]}, not the animation brief")
    elif tag not in ROUTES_OK:
        errs.append(f"unknown route tag '{tag}'")
    fixtures = req.get("fixtures") or []
    if tag == "data-bound" and not fixtures:
        errs.append("#12 data-bound scene needs validated fixtures; none supplied")
    for i, fx in enumerate(fixtures):
        for k in ("id", "path", "sha256", "fields_on_screen"):
            _need(fx, k, errs, f"fixtures[{i}]")
        _check_file(fx, f"fixture {fx.get('id')}", errs, file_checks)
    # script: read-only, approved, hash-bound (#11)
    sc = req["script"]
    if sc.get("approval_status") != "approved":
        errs.append("#11 script is not approved; brief cannot be built")
    _need(sc, "sha256", errs, "script")
    _check_file(sc, "script", errs, file_checks)
    # style
    st = req["style"]
    if st.get("id") not in STYLES:
        errs.append(f"style id '{st.get('id')}' is not one of {sorted(STYLES)}")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(st.get("version", ""))):
        errs.append("style.version must be pinned semver (e.g. 1.0.0)")
    # cue sheet (#63 handled downstream; here: integrity and frame math [N72])
    _check_file(req["cue_sheet"], "cue_sheet", errs, file_checks)
    cs_path = req["cue_sheet"].get("path")
    if file_checks and cs_path and os.path.isfile(cs_path):
        try:
            cs = json.load(open(cs_path, encoding="utf-8"))
            fps, dur = cs.get("fps"), cs.get("duration")
            if not isinstance(fps, (int, float)) or fps <= 0 or not isinstance(dur, (int, float)) or dur <= 0:
                errs.append("cue_sheet needs positive fps and duration")
            elif abs(dur * fps - round(dur * fps)) > 1e-6:
                warns.append("cue_sheet duration x fps is not whole; frame count = round(duration x fps) [N72]")
            if not cs.get("cues"):
                errs.append("cue_sheet has no cues; animation would hard-code times (#63)")
            if cs.get("scene_id") != req["scene_id"]:
                errs.append("cue_sheet scene_id does not match request scene_id")
            if cs.get("alignment_source") in ("synthetic_even_spacing", "example"):
                errs.append("cue_sheet alignment_source '%s' is not valid for production (guessed timing)"
                            % cs.get("alignment_source"))
            if cs.get("script_sha256") and cs["script_sha256"] != sc.get("sha256"):
                errs.append("#11/#63 cue_sheet was aligned to a different script hash than the approved script")
        except (ValueError, OSError) as e:
            errs.append(f"cue_sheet unreadable: {e}")
    _check_file(req["brand_tokens"], "brand_tokens", errs, file_checks)
    ra = req.get("reference_analysis")
    if ra:
        _check_file(ra, "reference_analysis", errs, file_checks)
        if ra.get("rights") != "analysis_only":
            errs.append("reference_analysis.rights must be 'analysis_only' (no asset reuse)")
    # fonts (#8)
    allow = {f.lower() for f in req["fonts"].get("allow", [])}
    ban = {f.lower() for f in req["fonts"].get("ban", [])}
    if not allow:
        errs.append("#8 fonts.allow is empty; name fonts explicitly [N50][N51]")
    missing = MANDATORY_BANS - ban
    if missing:
        errs.append(f"#8 fonts.ban must include {sorted(missing)} [N51]")
    if allow & ban:
        errs.append(f"#8 fonts both allowed and banned as display: {sorted(allow & ban)}")
    text = {f.lower() for f in req["fonts"].get("text", [])}   # labels/captions/science text roles
    if text & (ban - {"inter"}):                               # house policy: Inter allowed for these roles only
        errs.append(f"#8 banned families in text roles: {sorted(text & (ban - {'inter'}))}")
    if allow & CONVERGENCE_FONTS:
        warns.append("#8 Space Grotesk is a convergence font [N55]; ban or rotate it deliberately")
    # holds (#50)
    h = req["holds"]
    if not isinstance(h.get("headline_min_s"), (int, float)) or h["headline_min_s"] < 1.2:
        errs.append("#50 holds.headline_min_s must be >= 1.2 [N60]")
    if not isinstance(h.get("equation_tail_s"), (int, float)) or h["equation_tail_s"] < 0.5:
        errs.append("holds.equation_tail_s must be >= 0.5 (report section 7.5 [Recommendation])")
    indic = req["language"] in INDIC_LANGS or bool(INDIC_RE.search(sc.get("segment_text", "")))
    if indic:
        m = h.get("indic_multiplier")
        if not isinstance(m, (int, float)) or m <= 1.0:
            errs.append("#50 Indic text needs holds.indic_multiplier > 1.0: copy it from "
                        "04_harness_contract/vertical_safe_zones.tokens.json hold_times_s (a [Hypothesis] until the "
                        "pilot reading test calibrates it); never leave it unset")
        elif h.get("indic_multiplier_status") != "calibrated":
            warns.append("#50 indic_multiplier is an uncalibrated [Hypothesis]; pilot reading test pending")
    # iteration cap (#60) and effort ([N22][N24])
    cap = req["iteration_cap"]
    if not isinstance(cap, int) or not 1 <= cap <= MAX_ITER:
        errs.append(f"#60 iteration_cap must be an integer 1..{MAX_ITER}")
    lvl = str(req["effort"].get("level", "")).lower()
    if lvl == "ultracode":
        errs.append("ultracode is banned in production runs ([V1], [N24])")
    elif lvl not in {"low", "medium", "high", "xhigh", "max"}:
        errs.append("effort.level must be explicit (Opus 5.5 silently defaults to medium [N22])")
    if lvl == "max" and not req["effort"].get("justification"):
        errs.append("effort max requires a written justification (report section 3.4)")
    if not req["effort"].get("model"):
        errs.append("effort.model must be a pinned full model ID ([N28])")
    # workspace isolation (#9)
    ws = str(req["workspace"]).rstrip("/")
    if req["scene_id"] not in ws:
        errs.append("#9 workspace must be a per-job folder containing the scene_id")
    # free-text fields scanned for forbidden instructions (#60/#11/#12)
    text = " ".join(str(req.get(k, "")) for k in ("creative_direction", "extra_notes"))
    for pat, why in FORBIDDEN:
        if re.search(pat, text, re.I):
            errs.append(f"forbidden instruction in free text: {why}")
    return errs, warns


def _fallback_template():
    raw = (TEMPLATES / "brief_template.reference.md").read_text(encoding="utf-8")
    m = re.search(r"<!-- FALLBACK-SKELETON-START -->(.*)<!-- FALLBACK-SKELETON-END -->", raw, re.S)
    if not m:
        raise SystemExit("fallback skeleton markers missing in templates/brief_template.reference.md")
    return m.group(1).strip() + "\n"


def render(req, template_text):
    fx = req.get("fixtures") or []
    fixture_lines = "\n".join(f"- `{f['id']}` ({f['path']}, sha256 {f['sha256'][:12]}...): on-screen fields "
                              f"{', '.join(f['fields_on_screen'])}" for f in fx) or "- none (no on-screen science values allowed)"
    ra = req.get("reference_analysis") or {}
    h = req["holds"]
    values = {
        "scene_id": req["scene_id"], "lesson_id": req.get("lesson_id", ""),
        "language": req["language"], "route_tag": req["route"]["tag"],
        "style_id": req["style"]["id"], "style_version": req["style"]["version"],
        "style_guide_path": req["style"].get("guide_path", ""),
        "script_path": req["script"].get("path", ""), "script_sha256": req["script"]["sha256"],
        "cue_sheet_path": req["cue_sheet"].get("path", ""),
        "brand_tokens_path": req["brand_tokens"].get("path", ""),
        "reference_analysis_path": ra.get("path", "none"),
        "fixtures_block": fixture_lines,
        "fonts_allow": ", ".join(req["fonts"]["allow"]) + (
            "; text roles (labels, captions, science text): " + ", ".join(req["fonts"]["text"])
            if req["fonts"].get("text") else ""),
        "fonts_ban": ", ".join(req["fonts"]["ban"]) + " (as display faces)",
        "headline_min_s": str(h["headline_min_s"]), "equation_tail_s": str(h["equation_tail_s"]),
        "indic_multiplier": str(h.get("indic_multiplier") or "n/a (Latin-script narration)"),
        "iteration_cap": str(req["iteration_cap"]),
        "effort_model": req["effort"]["model"], "effort_level": req["effort"]["level"],
        "workspace": str(req["workspace"]).rstrip("/") + "/",
        "creative_direction": req.get("creative_direction", "Follow the approved storyboard beats."),
    }
    constraints = (TEMPLATES / "constraints_block.md").read_text(encoding="utf-8")
    values["constraints_block"] = _fill(constraints, values)
    out = _fill(template_text, values)
    left = sorted(set(re.findall(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", out)))
    return out, left


def _fill(text, values):
    return re.sub(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}", lambda m: values.get(m.group(1), m.group(0)), text)


def build(req, out_dir, template_path=None, file_checks=True):
    errs, warns = validate(req, file_checks)
    if errs:
        return {"status": "blocked", "skill": "examleaf-anim-brief", "scene_id": req.get("scene_id"),
                "errors": errs, "warnings": warns}
    tpl = Path(template_path).read_text(encoding="utf-8") if template_path else _fallback_template()
    m = re.search(r"<!--\s*BRIEF-START\s*-->(.*)<!--\s*BRIEF-END\s*-->", tpl, re.S)
    if m:                                   # canonical template: only the text between the markers is the brief
        tpl = m.group(1).strip() + "\n"
    text, unresolved = render(req, tpl)
    if unresolved:
        return {"status": "blocked", "skill": "examleaf-anim-brief", "scene_id": req["scene_id"],
                "errors": [f"template placeholders not filled: {unresolved}"], "warnings": warns}
    os.makedirs(out_dir, exist_ok=True)
    brief = Path(out_dir) / "brief.md"
    brief.write_text(text, encoding="utf-8")
    inputs = {k: req[k].get("sha256") for k in ("script", "cue_sheet", "brand_tokens") if isinstance(req.get(k), dict)}
    inputs.update({f"fixture:{f['id']}": f["sha256"] for f in req.get("fixtures") or []})
    if req.get("reference_analysis"):
        inputs["reference_analysis"] = req["reference_analysis"].get("sha256")
    manifest = {"schema_version": "1.0", "skill": "examleaf-anim-brief", "scene_id": req["scene_id"],
                "style": f"{req['style']['id']}@{req['style']['version']}", "input_sha256": inputs,
                "brief_sha256": sha256_file(brief), "warnings": warns, "status": "ready_for_authoring"}
    (Path(out_dir) / "brief_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def selftest():
    with tempfile.TemporaryDirectory() as td:
        def w(name, data):
            p = os.path.join(td, name)
            with open(p, "w", encoding="utf-8") as f:
                f.write(data if isinstance(data, str) else json.dumps(data))
            return p, sha256_file(p)
        sp, sh = w("script.md", "Light bends when it changes medium.")
        cp, ch = w("cue.json", {"scene_id": "phy-10-03-s04", "fps": 30, "duration": 7.4,
                                "alignment_source": "forced_alignment", "script_sha256": sh,
                                "words": [{"w": "refraction", "t0": 1.12, "t1": 1.71}],
                                "cues": [{"id": "label_n1", "at": 1.07, "kind": "reveal"}]})
        bp, bh = w("brand.json", {"background": "#F7F9FC"})
        fp, fh = w("fx.json", {"n1": 1.0, "n2": 1.5})
        req = {"scene_id": "phy-10-03-s04", "lesson_id": "phy-10-03", "language": "en-IN",
               "route": {"tag": "data-bound", "source": "examleaf-storyboard-route"},
               "script": {"path": sp, "sha256": sh, "approval_status": "approved",
                          "segment_text": "Light bends when it changes medium."},
               "style": {"id": "doodle-handdrawn", "version": "1.0.0", "guide_path": "g.md"},
               "cue_sheet": {"path": cp, "sha256": ch}, "brand_tokens": {"path": bp, "sha256": bh},
               "fixtures": [{"id": "fx-refraction", "path": fp, "sha256": fh, "fields_on_screen": ["n1", "n2"]}],
               "fonts": {"allow": ["Caveat Brush", "Patrick Hand"], "text": ["Inter", "Noto Sans"],
                         "ban": ["Arial", "Inter", "Space Grotesk"]},
               "holds": {"headline_min_s": 1.2, "equation_tail_s": 0.5, "indic_multiplier": None},
               "iteration_cap": 3, "effort": {"model": "claude-opus-5-5", "level": "high"},
               "workspace": os.path.join(td, "jobs", "phy-10-03-s04"),
               "creative_direction": "Pencil doodle of a straw bending in a glass."}
        out = build(req, os.path.join(td, "out"))
        assert out.get("status") == "ready_for_authoring", out
        txt = open(os.path.join(td, "out", "brief.md"), encoding="utf-8").read()
        assert "{{" not in txt and "Do not read" in txt and "fx-refraction" in txt
        tp, _ = w("canon.md", "<!-- notes {{not_a_field}} -->\n<!-- BRIEF-START -->\n# {{scene_id}} in {{workspace}}x\n"
                              "<!-- BRIEF-END -->\ntrailer {{also_not}}")
        out2 = build(req, os.path.join(td, "out-canon"), tp)
        txt2 = open(os.path.join(td, "out-canon", "brief.md"), encoding="utf-8").read()
        assert out2["status"] == "ready_for_authoring" and txt2.startswith("# phy-10-03-s04 in ") \
            and "phy-10-03-s04/x" in txt2 and "trailer" not in txt2, txt2
        bad_cases = {
            "ultracode": lambda r: r["effort"].update(level="ultracode"),
            "silent-effort": lambda r: r["effort"].pop("level"),
            "no-fixture": lambda r: r.update(fixtures=[]),
            "loop": lambda r: r.update(creative_direction="Don't stop until it is perfect"),
            "research": lambda r: r.update(creative_direction="Research the refractive index online"),
            "font": lambda r: r["fonts"].update(ban=["Space Grotesk"]),
            "text-font": lambda r: r["fonts"].update(text=["Arial"]),
            "display-inter": lambda r: r["fonts"].update(allow=["Inter"]),
            "hold": lambda r: r["holds"].update(headline_min_s=0.8),
            "indic": lambda r: r.update(language="hi-IN"),
            "cap": lambda r: r.update(iteration_cap=10),
            "unapproved": lambda r: r["script"].update(approval_status="draft"),
            "tampered": lambda r: r["script"].update(sha256="0" * 64),
            "workspace": lambda r: r.update(workspace=td),
            "spatial": lambda r: r["route"].update(tag="spatial-hero"),
        }
        # cue sheet aligned to an older script hash must block (#11/#63)
        cp2, ch2 = w("cue_old.json", {"scene_id": "phy-10-03-s04", "fps": 30, "duration": 7.4,
                                      "alignment_source": "forced_alignment", "script_sha256": "f" * 64,
                                      "cues": [{"id": "a", "at": 1.0, "kind": "reveal"}]})
        bad_cases["stale-cue"] = lambda r: r.update(cue_sheet={"path": cp2, "sha256": ch2})
        cp3, ch3 = w("cue_syn.json", {"scene_id": "phy-10-03-s04", "fps": 30, "duration": 7.4,
                                      "alignment_source": "synthetic_even_spacing",
                                      "cues": [{"id": "a", "at": 1.0, "kind": "reveal"}]})
        bad_cases["synthetic-timing"] = lambda r: r.update(cue_sheet={"path": cp3, "sha256": ch3})
        ok_hi = json.loads(json.dumps(req)); ok_hi["language"] = "hi-IN"; ok_hi["holds"]["indic_multiplier"] = 1.5
        res_hi = build(ok_hi, os.path.join(td, "out-hi"))
        assert res_hi["status"] == "ready_for_authoring" and any("Hypothesis" in x for x in res_hi["warnings"]), res_hi
        for name, mutate in bad_cases.items():
            r = json.loads(json.dumps(req))
            mutate(r)
            res = build(r, os.path.join(td, "bad-" + name))
            assert res["status"] == "blocked", (name, res)
    print(json.dumps({"selftest": "pass", "script": "build_brief.py", "negative_cases": len(bad_cases)}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--request")
    ap.add_argument("--out-dir")
    ap.add_argument("--template", help="canonical 12_advanced_animations_with_claude/06_prompts_and_templates/brief_template.md")
    ap.add_argument("--no-file-checks", action="store_true", help="skip path/hash checks (dry-run only)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.request or not a.out_dir:
        ap.error("--request and --out-dir are required")
    try:
        req = json.load(open(a.request, encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(json.dumps({"status": "error", "error": str(e)}))
        return 2
    res = build(req, a.out_dir, a.template, not a.no_file_checks)
    print(json.dumps(res, indent=2))
    return 0 if res.get("status") == "ready_for_authoring" else 1


if __name__ == "__main__":
    sys.exit(main())
