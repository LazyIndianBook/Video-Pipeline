#!/usr/bin/env python3
"""validate_style_tokens.py - validate the ExamLeaf 9:16 style-token library (stdlib only).

Validates the canonical file 12_advanced_animations_with_claude/05_style_guides/style_tokens.json
(shape: schema_version, _meta, common, fonts_registry[], styles{}; see templates/style_tokens.schema.json).

Usage:
  python3 validate_style_tokens.py [TOKENS.json] [--production] [--json]
          (default TOKENS.json: ../../../05_style_guides/style_tokens.json relative to this script)
  python3 validate_style_tokens.py --bump-check OLD.json NEW.json     # changed style => version bumped
  python3 validate_style_tokens.py --selftest                          # offline, synthetic document

Edge cases: #49 canvas 1080x1920 / no 16:9 crop, #54 no image-model text, #55 Indic fonts and units,
#56 flash ban, #8 display-font bans [N51][N55], #17/#18 seeded + finite, #64 camera lock, [N52] accents.
--production also fails on unverified licences, unvendored fonts and unverified Indic coverage.
Exit: 0 valid (warnings allowed), 1 invalid, 2 usage/IO error.
"""
import argparse, json, os, re, sys

HOUSE = ["paper-collage-vertical", "doodle-handdrawn", "editorial-vox", "kinetic-type", "voxel-isometric"]
MANDATORY_DISPLAY_BANS = {"arial", "inter", "space grotesk"}          # [N51] [N55]
REQUIRED_FORBIDDEN = {                                                # common.forbidden flags that must be true
    "image_model_text_numbers_formulae": "#54", "full_frame_flash": "#56", "infinite_repeats": "#18",
    "math_random": "#17", "per_codepoint_indic_animation": "#55",
    "camera_fx_during_label_or_measurement_reveal": "#64", "crop_16x9_into_9x16": "#49",
    "agent_writes_or_edits_script": "#11", "agent_researches_facts": "#12", "read_other_folders": "#9",
    "ultracode": "#3", "dont_stop_until_perfect": "#60"}
REQUIRED_DETERMINISM = ["seeded_prng_required", "wall_clock_forbidden", "raf_loops_forbidden",
                        "finite_repeats_only", "fonts_preloaded_before_first_frame", "double_render_frame_hash_test"]
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
FONT_LIST_KEYS = ("primary", "secondary", "handwriting", "science_text", "number_callout")


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o


def font_refs(fonts):
    refs = []
    for k in FONT_LIST_KEYS:
        v = fonts.get(k)
        if isinstance(v, list):
            refs += [(k, x) for x in v if isinstance(x, str)]
    ind = fonts.get("indic_fallback")
    if isinstance(ind, dict):
        for k, v in ind.items():
            if isinstance(v, list):
                refs += [("indic_fallback." + k, x) for x in v if isinstance(x, str)]
    return refs


def validate(doc, base_dir=None, production=False):
    E, W = [], []
    if not doc.get("schema_version"):
        E.append("schema_version missing")
    c = doc.get("common") or {}
    cv = c.get("canvas") or {}
    if (cv.get("width"), cv.get("height")) != (1080, 1920):
        E.append("#49 common.canvas must be 1080x1920")
    fb = c.get("forbidden") or {}
    for k, edge in REQUIRED_FORBIDDEN.items():
        if fb.get(k) is not True:
            E.append(f"{edge} common.forbidden.{k} must be true")
    det = c.get("determinism") or {}
    for k in REQUIRED_DETERMINISM:
        if det.get(k) is not True:
            E.append(f"common.determinism.{k} must be true")
    fp = c.get("font_policy") or {}
    common_ban = {x.lower() for x in fp.get("ban_as_display", [])}
    inter_ok = list(fp.get("inter_allowed_for", []))
    if MANDATORY_DISPLAY_BANS - common_ban:
        E.append(f"#8 common.font_policy.ban_as_display must include {sorted(MANDATORY_DISPLAY_BANS - common_ban)} [N51][N55]")
    unit = str(fp.get("indic_animation_unit", ""))
    if "code_point" in unit and "never" not in unit:
        E.append("#55 indic_animation_unit must be word or grapheme cluster, never code point")
    if not unit:
        E.append("#55 common.font_policy.indic_animation_unit missing")
    if not isinstance(fp.get("indic_line_height_min"), (int, float)) or fp["indic_line_height_min"] < 1.4:
        E.append("#55 common.font_policy.indic_line_height_min must be >= 1.4")
    h = c.get("holds") or {}
    if not isinstance(h.get("headline_min_s"), (int, float)) or h["headline_min_s"] < 1.2:
        E.append("#50 common.holds.headline_min_s must be >= 1.2 [N60]")
    if not isinstance(h.get("equation_tail_s"), (int, float)) or h["equation_tail_s"] < 0.5:
        E.append("common.holds.equation_tail_s must be >= 0.5 (report 7.5)")
    m = h.get("indic_multiplier")
    if not isinstance(m, (int, float)) or m <= 1.0:
        E.append("#50 common.holds.indic_multiplier must be > 1.0")
    elif "hypothesis" in str(h.get("indic_multiplier_status", "")).lower():
        W.append("#50 indic_multiplier is a Hypothesis; calibrate with a reading test")
    cap = c.get("iteration_cap_fix_loops")
    if not isinstance(cap, int) or not 1 <= cap <= 3:
        E.append("#60 common.iteration_cap_fix_loops must be 1..3")
    indic_active = bool((c.get("locale") or {}).get("indic_rules_active"))
    # fonts registry
    reg = {}
    cov_enum = set(((doc.get("_meta") or {}).get("coverage_enum") or {}).keys()) or \
        {"yes", "claimed_verify", "assumed_none", "n_a"}
    for i, f in enumerate(doc.get("fonts_registry") or []):
        fid = f.get("id")
        if not fid or fid in reg:
            E.append(f"fonts_registry[{i}]: missing or duplicate id {fid!r}")
            continue
        reg[fid] = f
        for script, v in (f.get("script_coverage") or {}).items():
            if v not in cov_enum:
                E.append(f"fonts_registry.{fid}: coverage '{v}' for {script} not in coverage_enum")
        if production and (f.get("licence") in (None, "verify") or not f.get("vendored") or not f.get("sha256")):
            E.append(f"fonts_registry.{fid}: production needs a recorded licence, vendored file and sha256")
    if not reg:
        E.append("fonts_registry is empty")
    if any(f.get("licence") == "verify" for f in reg.values()):
        W.append("some fonts have licence 'verify' and are not vendored yet (not production-ready)")
    # styles
    styles = doc.get("styles") or {}
    for sid in HOUSE:
        if sid not in styles:
            W.append(f"house style '{sid}' missing")
    for sid, st in styles.items():
        p = f"styles.{sid}"
        if st.get("style_id") != sid:
            E.append(f"{p}.style_id must equal its key")
        if not SEMVER.match(str(st.get("version", ""))):
            E.append(f"{p}.version must be semver")
        g = st.get("guide")
        if not g:
            E.append(f"{p}.guide missing")
        elif base_dir and not os.path.isfile(os.path.join(base_dir, g)):
            W.append(f"{p}.guide not found next to the tokens file: {g}")
        ra, rf = set(st.get("route_tags_allowed") or []), set(st.get("route_tags_forbidden") or [])
        if ra & rf:
            E.append(f"{p}: route tags both allowed and forbidden: {sorted(ra & rf)}")
        fonts = st.get("fonts") or {}
        ban = common_ban | {x.lower() for x in fonts.get("ban_as_display", [])}
        for role, ref in font_refs(fonts):
            f = reg.get(ref)
            if not f:
                E.append(f"{p}.fonts.{role}: '{ref}' not in fonts_registry")
                continue
            fam = str(f.get("family", "")).lower()
            role_text = str(fonts.get(role + "_role", "")).lower()
            positive = re.sub(r"\b(not|never|no)\b[^,;)]*", "", role_text)   # ignore "Inter not as display"
            display = any(w in positive for w in ("display", "headline", "title", "hook"))
            if fam in ban:
                if display:
                    E.append(f"#8 {p}: '{f.get('family')}' is banned as a display face but used in '{role}' ({role_text})")
                elif fam == "inter" and not (role == "science_text" or any(
                        a.rstrip("s").replace("_", " ") in role_text for a in inter_ok)):
                    E.append(f"#8 {p}: Inter allowed only for {sorted(inter_ok)}; '{role}' role is '{role_text}'")
                elif fam != "inter":
                    W.append(f"#8 {p}: banned family '{f.get('family')}' used in non-display role '{role}'")
            if role.startswith("indic_fallback"):
                script = "bengali_assamese" if "bengali" in role else "devanagari"
                cv_ = (f.get("script_coverage") or {}).get(script)
                if cv_ == "assumed_none":
                    E.append(f"#55 {p}.fonts.{role}: '{ref}' has no {script} coverage")
                elif cv_ != "yes":
                    msg = f"#55 {p}.fonts.{role}: '{ref}' {script} coverage '{cv_}'; run the glyph test"
                    (E if production else W).append(msg)
        ind = fonts.get("indic_fallback") or {}
        has_dev = any("devanagari" in k for k in ind) or any(
            (reg.get(r) or {}).get("script_coverage", {}).get("devanagari") in ("yes", "claimed_verify")
            for _, r in font_refs(fonts))
        has_bn = any("bengali" in k for k in ind) or any(
            (reg.get(r) or {}).get("script_coverage", {}).get("bengali_assamese") in ("yes", "claimed_verify")
            for _, r in font_refs(fonts))
        for ok, name in ((has_dev, "Devanagari"), (has_bn, "Bengali-Assamese")):
            if not ok:
                (E if indic_active else W).append(f"#55 {p}: no {name} font route (locale gate {'active' if indic_active else 'inactive'})")
        for path, v in walk(st.get("palette") or {}):
            if isinstance(v, str) and v.startswith("#") and not HEX.match(v):
                E.append(f"{p}.palette.{path}: '{v}' is not #rrggbb")
        pal = st.get("palette") or {}
        acc = (pal.get("usage") or {}).get("max_foreground_accent_hues", pal.get("max_accent_colours"))
        if acc is None and "ref" not in pal:
            W.append(f"[N52] {p}: no accent limit stated (dominant colour with sharp accents)")
        elif isinstance(acc, int) and acc > 3:
            E.append(f"[N52] {p}: {acc} accent hues; keep a dominant colour with 1-3 sharp accents")
        for path, v in walk(st):
            leaf = path.split(".")[-1].split("[")[0]
            if "boil" in path and leaf in ("fps_allowed", "fps", "boil_fps") and isinstance(v, (int, float)) \
                    and not 8 <= v <= 10:
                E.append(f"{p}.{path}: boil fps {v} outside 8-10 ([V4-MP])")
            if "repeat" in leaf and (v in (-1, "infinite", "Infinity") or v == float("inf")):
                E.append(f"#18 {p}.{path}: infinite repeat")
        sf = st.get("forbidden") or {}
        if sf.get("ref") != "common.forbidden":
            E.append(f"{p}.forbidden must reference common.forbidden")
        for k, v in (sf.get("additional") or {}).items():
            if v is not True:
                E.append(f"{p}.forbidden.additional.{k} must be true (forbidden_true_means forbidden)")
        for k in REQUIRED_FORBIDDEN:
            if k in (sf.get("overrides") or {}) and (sf["overrides"][k] is not True):
                E.append(f"{p}: may not relax common.forbidden.{k}")
        cr = st.get("credits")
        if isinstance(cr, (int, float)) and cr > 0:
            W.append(f"{p}.credits={cr}: prices are not stored in tokens; estimate at the storyboard gate")
    E.extend(safe_zone_drift(c.get("safe_zones") or {}, base_dir))
    return E, W


SHARE_MAP = {"title": "top_title", "visual": "middle_visual", "caption": "bottom_caption"}


def safe_zone_drift(sz, base_dir):
    """15 Oct 2026 (AD-42): the harness token file owns zone shares and the side margin; this file only mirrors them."""
    src = sz.get("source_of_truth")
    if not src or not base_dir:
        return []
    p = os.path.normpath(os.path.join(base_dir, src))
    if not os.path.isfile(p):
        return [f"common.safe_zones.source_of_truth {src!r} not found"]
    z = (json.load(open(p, encoding="utf-8")).get("zones") or {})
    errs = []
    if "min_side_margin_px" in sz and sz["min_side_margin_px"] != z.get("side_margin_min_px"):
        errs.append(f"common.safe_zones.min_side_margin_px {sz['min_side_margin_px']} != owner zones.side_margin_min_px "
                    f"{z.get('side_margin_min_px')} (AD-42)")
    for k, hk in SHARE_MAP.items():
        mine = (sz.get("zone_shares_of_usable_band") or {}).get(k)
        if mine is not None and mine != (z.get(hk) or {}).get("share"):
            errs.append(f"common.safe_zones share {k}={mine} != owner zones.{hk}.share (AD-42)")
    return errs


def bump_check(old, new):
    errs = []
    for sid, st in (new.get("styles") or {}).items():
        o = (old.get("styles") or {}).get(sid)
        if o is None:
            continue
        strip = lambda d: json.dumps({k: v for k, v in d.items() if k != "version"}, sort_keys=True)
        if strip(o) != strip(st) and o.get("version") == st.get("version"):
            errs.append(f"styles.{sid} changed but version stayed {st.get('version')}; bump it")
    return errs


def _sample():
    return {
        "schema_version": "1.0",
        "_meta": {"coverage_enum": {"yes": "", "claimed_verify": "", "assumed_none": "", "n_a": ""}},
        "common": {
            "canvas": {"width": 1080, "height": 1920, "fps": 30},
            "forbidden": {k: True for k in REQUIRED_FORBIDDEN},
            "determinism": {k: True for k in REQUIRED_DETERMINISM},
            "font_policy": {"ban_as_display": ["Arial", "Inter", "Space Grotesk"],
                            "indic_animation_unit": "word_or_grapheme_cluster_never_code_point",
                            "indic_line_height_min": 1.4, "inter_allowed_for": ["labels", "captions", "science_text"]},
            "holds": {"headline_min_s": 1.2, "equation_tail_s": 0.5, "indic_multiplier": 1.5,
                      "indic_multiplier_status": "Hypothesis"},
            "iteration_cap_fix_loops": 3, "locale": {"indic_rules_active": False}},
        "fonts_registry": [
            {"id": "inter", "family": "Inter", "script_coverage": {"latin": "yes", "devanagari": "assumed_none"}, "licence": "verify", "vendored": False, "sha256": None},
            {"id": "alfa_slab_one", "family": "Alfa Slab One", "script_coverage": {"latin": "yes", "devanagari": "assumed_none"}, "licence": "verify", "vendored": False, "sha256": None},
            {"id": "noto_sans_devanagari", "family": "Noto Sans Devanagari", "script_coverage": {"latin": "yes", "devanagari": "claimed_verify"}, "licence": "verify", "vendored": False, "sha256": None},
            {"id": "noto_sans_bengali", "family": "Noto Sans Bengali", "script_coverage": {"latin": "yes", "bengali_assamese": "claimed_verify"}, "licence": "verify", "vendored": False, "sha256": None}],
        "styles": {"paper-collage-vertical": {
            "style_id": "paper-collage-vertical", "version": "1.0.0", "guide": "paper-collage-vertical.md",
            "route_tags_allowed": ["illustrative"], "route_tags_forbidden": ["data-bound"], "credits": 0,
            "palette": {"storybook": {"cream": "#f3ecdf", "tomato": "#d9483b"},
                        "usage": {"dominant_background_families_per_scene": 1, "max_foreground_accent_hues": 2}},
            "fonts": {"primary": ["alfa_slab_one"], "primary_role": "ransom display tiles",
                      "secondary": ["inter"], "secondary_role": "small labels",
                      "indic_fallback": {"devanagari": ["noto_sans_devanagari"], "bengali_assamese": ["noto_sans_bengali"]}},
            "motion": {"boil": {"fps_allowed": [8, 10]}, "idle": {"repeat": "finite"}},
            "forbidden": {"ref": "common.forbidden", "additional": {"three_d_render": True}}}}}


def selftest():
    good = _sample()
    e, w = validate(good)
    assert not e, e
    assert any("glyph test" in x for x in w) and any("missing" in x for x in w)
    assert validate(good, production=True)[0], "production must reject unvendored fonts"
    S = lambda d: d["styles"]["paper-collage-vertical"]
    mut = {
        "canvas-16:9": lambda d: d["common"]["canvas"].update(width=1920, height=1080),
        "image-text": lambda d: d["common"]["forbidden"].update(image_model_text_numbers_formulae=False),
        "flash": lambda d: d["common"]["forbidden"].pop("full_frame_flash"),
        "inter-display-ban": lambda d: d["common"]["font_policy"].update(ban_as_display=["Arial"]),
        "inter-as-display": lambda d: S(d)["fonts"].update(primary=["inter"]),
        "inter-as-body": lambda d: S(d)["fonts"].update(secondary_role="body paragraphs"),
        "inter-negation-ok-but-display": lambda d: S(d)["fonts"].update(secondary_role="hook display (not labels)"),
        "codepoint": lambda d: d["common"]["font_policy"].update(indic_animation_unit="code_point"),
        "line-height": lambda d: d["common"]["font_policy"].update(indic_line_height_min=1.0),
        "hold": lambda d: d["common"]["holds"].update(headline_min_s=0.8),
        "cap": lambda d: d["common"].update(iteration_cap_fix_loops=10),
        "unknown-font": lambda d: S(d)["fonts"].update(primary=["comic_neue"]),
        "no-coverage": lambda d: S(d)["fonts"]["indic_fallback"].update(devanagari=["alfa_slab_one"]),
        "boil": lambda d: S(d)["motion"]["boil"].update(fps_allowed=[12, 24]),
        "infinite": lambda d: S(d)["motion"]["idle"].update(repeat="infinite"),
        "bad-hex": lambda d: S(d)["palette"]["storybook"].update(cream="#f3ecd"),
        "accents": lambda d: S(d)["palette"]["usage"].update(max_foreground_accent_hues=6),
        "forbidden-ref": lambda d: S(d).update(forbidden={"additional": {}}),
        "style-id": lambda d: S(d).update(style_id="collage"),
        "semver": lambda d: S(d).update(version="v1"),
        "determinism": lambda d: d["common"]["determinism"].update(seeded_prng_required=False),
    }
    for name, fn in mut.items():
        d = json.loads(json.dumps(good)); fn(d)
        assert validate(d)[0], name
    act = json.loads(json.dumps(good)); act["common"]["locale"]["indic_rules_active"] = True
    S(act)["fonts"].pop("indic_fallback")
    assert any("Devanagari" in x for x in validate(act)[0]), "active locale needs Indic fonts"
    neg = json.loads(json.dumps(good)); S(neg)["fonts"]["secondary_role"] = "support, labels (Inter not as display)"
    assert not validate(neg)[0], "negated display mention must not count as display"
    import tempfile
    with tempfile.TemporaryDirectory() as td:                       # AD-42 drift check against the owner file
        json.dump({"zones": {"side_margin_min_px": 96, "top_title": {"share": 0.22}, "middle_visual": {"share": 0.54},
                             "bottom_caption": {"share": 0.24}}}, open(os.path.join(td, "owner.json"), "w"))
        sz = {"source_of_truth": "owner.json", "min_side_margin_px": 96,
              "zone_shares_of_usable_band": {"title": 0.22, "visual": 0.54, "caption": 0.24}}
        assert not safe_zone_drift(sz, td)
        assert safe_zone_drift(dict(sz, min_side_margin_px=90), td)
        assert safe_zone_drift(dict(sz, zone_shares_of_usable_band={"title": 0.20, "visual": 0.58, "caption": 0.22}), td)
    new = json.loads(json.dumps(good)); S(new)["credits"] = 1
    assert bump_check(good, new)
    S(new)["version"] = "1.0.1"
    assert not bump_check(good, new)
    print(json.dumps({"selftest": "pass", "script": "validate_style_tokens.py", "mutations": len(mut) + 2}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate ExamLeaf style tokens")
    ap.add_argument("tokens", nargs="?")
    ap.add_argument("--production", action="store_true"); ap.add_argument("--json", action="store_true")
    ap.add_argument("--bump-check", nargs=2, metavar=("OLD", "NEW")); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.bump_check:
            errs = bump_check(*(json.load(open(x, encoding="utf-8")) for x in a.bump_check))
            print(json.dumps({"bump_check": "fail" if errs else "pass", "errors": errs}, indent=2))
            return 1 if errs else 0
        path = a.tokens or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                         "..", "..", "..", "05_style_guides", "style_tokens.json"))
        doc = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        print(json.dumps({"status": "error", "error": str(ex)}))
        return 2
    e, w = validate(doc, os.path.dirname(os.path.abspath(path)), a.production)
    print(json.dumps({"file": path, "valid": not e, "errors": e, "warnings": w}, indent=2, ensure_ascii=False))
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main())
