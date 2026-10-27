#!/usr/bin/env python3
"""build_tokens.py: tokens.json -> tokens.css + tokens.js (generated; never edit them by hand).
Checks (exit 1 on any failure) and writes every measured ratio to tokens.json > contrast:
  * every TEXT role on every surface it can sit on (sheets/paper, cream, grid chips, sticker outline) >= 4.5:1
  * every chip style fg on its bg >= 4.5:1; atom letters on their sticker fill >= 4.5:1
  * graphics >= 3:1: ink strokes on every board band of every world (the bands under the diagram lane) and the
    cream sky; colour strokes on paper, cream and the sticker outline (on a band they always ride a cream outline:
    stickers, two-tone connectors, strike lines); biology arrows on paper and cream
  * bands: ink and paper on every band fill are RECORDED (text never sits on a band; chips and sheets carry it)
  * type floors, true-subscript size, lanes inside 250..1470 and ordered, ident above every title lane and gone by
    2.5 s, diagram share floors, side margin, verb durations inside their class, chip stagger <= 40 ms, no banned easing
Usage: python3 tools/build_tokens.py"""
import json, pathlib, re, sys

DS = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((DS / "tokens.json").read_text(encoding="utf-8"))
BUILD_ONLY = ("gates", "forbidden_on_screen", "banned_easings", "contrast")


def strip(o):
    """Drop $comment keys and build-only sections so the scene never carries the gate patterns or the brand blacklist."""
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if not k.startswith("$") and k not in BUILD_ONLY}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def lum(hexc):
    c = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


TEXT_ROLES = ("ink", "muted", "voltage", "current", "resistance", "condition", "mismatch")


def lane_y(ref, layout):
    """'diagram.y0+8' -> px in that layout (None if the lane is absent); a number passes through."""
    if isinstance(ref, (int, float)):
        return ref
    m = re.fullmatch(r"([a-z]+)\.(y0|y1)([+-]\d+)?", ref)
    z = T["lanes"][layout].get(m.group(1))
    return None if z is None else z[m.group(2)] + int(m.group(3) or 0)


def checks():
    bad, info = [], {}
    C = T["color"]

    def need(key, a, b, floor):
        r = contrast(a, b); info[key] = round(r, 2)
        if r < floor:
            bad.append(f"{key}: {a} on {b} = {r:.2f}:1 < {floor}")

    for surf, bg in C["surfaces"].items():                       # text roles on every surface
        if surf.startswith("$"): continue
        for role in TEXT_ROLES:
            need(f"text.{role}.on.{surf}", C[role], bg, 4.5)
        need(f"text.coefficient.on.{surf}", C["chem"]["coefficient"], bg, 4.5)
    for st in T["chips"]["styles"]:                               # chips: fg on bg (any size)
        need(f"chip.{st['name']}", st["fg"], st["bg"], 4.5)
    for el, v in C["chem"].items():                               # atom letters on their sticker fill
        if isinstance(v, dict):
            need(f"atom.{el}.letter", v["text"], v["fill"], 4.5)
    for world, W in T["world"]["subjects"].items():
        if world.startswith("$"): continue
        board = ["cream"] + [b for b in W["bands"]]               # what a board line can cross in that world
        for b in W["bands"]:                                      # recorded only: text never sits on a band
            info[f"band.{world}.{b['name']}.ink"] = round(contrast(C["ink"], b["fill"]), 2)
            info[f"band.{world}.{b['name']}.paper"] = round(contrast(C["hue"]["paper"], b["fill"]), 2)
            info[f"band.{world}.{b['name']}.luminance"] = round(lum(b["fill"]), 3)
            if lum(b["fill"]) < T["world"]["band_min_luminance"]:   # PD-17: no dark colour blocks
                bad.append(f"band {world}.{b['name']} {b['fill']} is dark (luminance {lum(b['fill']):.3f} < {T['world']['band_min_luminance']})")
            sp = C["ink"] if contrast(C["ink"], b["fill"]) >= contrast(C["hue"]["paper"], b["fill"]) else C["hue"]["paper"]
            info[f"sparkle.{world}.{b['name']}"] = round(contrast(sp, b["fill"]), 2)   # decorative, recorded
        layout = "carded"
        dg = T["lanes"][layout]["diagram"]
        under = [b for b in W["bands"] if (lane_y(b["top"], layout) or 9e9) < dg["y1"] - 20]   # bands under the board
        need(f"line.ink.{world}.cream", C["line"]["ink"], C["hue"]["cream"], 3.0)
        for b in under:                                           # only INK strokes touch a band directly
            need(f"line.ink.{world}.{b['name']}", C["line"]["ink"], b["fill"], 3.0)
    for role in ("voltage", "current", "resistance", "mismatch"):  # colour strokes ride paper or a cream outline
        for sn in ("paper", "cream", "outline"):
            need(f"line.{role}.on.{sn}", C["line"][role], C["surfaces"][sn], 3.0)
    for k in ("material", "energy", "boundary"):
        need(f"bio.{k}.on.paper", C["bio"][k], C["surfaces"]["paper"], 3.0)
        need(f"bio.{k}.on.cream", C["bio"][k], C["hue"]["cream"], 3.0)
    for tint in C["bio"]["compartment_tints"]:                     # biology compartments: ink text, material arrow
        need(f"text.ink.on.bio_tint.{tint}", C["ink"], tint, 4.5)
        need(f"bio.material.on.tint.{tint}", C["bio"]["material"], tint, 3.0)
    need("bio.energy.on.outline", C["bio"]["energy"], T["sticker"]["outline_color"], 3.0)
    need("link.dash.on.outline", C["line"]["resistance"], T["sticker"]["outline_color"], 3.0)
    need("strike.on.outline", C["line"]["mismatch"], T["sticker"]["outline_color"], 3.0)
    BS = T["brand"]["sticker"]
    need("brand.sticker.line1", BS["fg1"], BS["bg"], 4.5)
    need("brand.sticker.line2", BS["fg2"], BS["bg"], 4.5)

    ty = T["type"]
    for k, v in ty.items():
        if isinstance(v, dict) and "floor" in v and "size" in v and v["size"] < v["floor"]:
            bad.append(f"type {k} {v['size']} < floor {v['floor']}")
    if ty["chip"]["size"] != ty["headline"]["size"]:
        bad.append("chips must use the headline size")
    sub = ty["equation"]["size"] * ty["subscript"]["scale"]
    if sub < ty["subscript"]["floor"]:
        bad.append(f"subscript at equation size {sub:.1f} < {ty['subscript']['floor']}")
    L = T["lanes"]
    for name in ("default", "captioned", "carded"):
        lanes = L[name]; prev = 0
        if "lockup" in lanes:
            bad.append(f"lane {name}.lockup exists: retired by PD-21")
        for lane, z in lanes.items():
            if z["y0"] < 250 or z["y1"] > 1470 or z["y0"] < prev:
                bad.append(f"lane {name}.{lane} outside band 250..1470 or overlapping")
            prev = z["y1"]
        if L["ident"]["y1"] > lanes["title"]["y0"]:
            bad.append(f"ident overlaps the {name} title lane")
        share = (lanes["diagram"]["y1"] - lanes["diagram"]["y0"]) / T["canvas"]["height"]
        floor = T["fill"]["diagram_min_share" + {"default": "", "captioned": "_captioned", "carded": "_carded"}[name]]
        info["diagram_share_" + name] = round(share, 3)
        if share + 1e-9 < floor:
            bad.append(f"diagram share {name} {share:.3f} < {floor}")
    if L["x0"] < 96 or L["x1"] > 1080 - 96:
        bad.append("side margin < 96")
    idt = T["brand"]["ident"]
    if idt["hold_until_s"] + idt["out_dur_s"] > idt["out_end_s"] + 1e-9 or idt["out_end_s"] > 2.5:
        bad.append("opening ident must be gone by 2.5 s (PD-21)")
    M = T["motion"]
    for verb, v in M["verbs"].items():
        lo, hi = M["range"][v["class"]]
        if not lo - 1e-9 <= v["dur"] <= hi + 1e-9:
            bad.append(f"verb {verb} {v['dur']} s outside {v['class']} {lo}-{hi}")
        if v["ease"] in M["banned_easings"]:
            bad.append(f"verb {verb} uses banned easing")
    if M["chip_stagger_s"] > M["chip_stagger_max_s"] or M["chip_stagger_max_s"] > 0.04:
        bad.append("chip stagger > 40 ms: headlines appear as a whole phrase")
    if not 0.9 <= M["pop_scale0"] < 1:
        bad.append("Pop scale0 must be in [0.9, 1): no big pops")
    return bad, info


def css():
    C, ty, L, CH, ST = T["color"], T["type"], T["lanes"], T["chips"], T["sticker"]
    out = ["/* GENERATED by tools/build_tokens.py from tokens.json v" + T["version"] + ". Do not edit. */", ":root{"]
    for k, v in C.items():
        if isinstance(v, str) and not k.startswith("$"):
            out.append(f"  --c-{k}:{v};")
    for grp in ("hue", "fill", "surfaces"):
        out.append("  " + "".join(f"--{grp}-{k}:{v};" for k, v in C[grp].items() if not k.startswith("$")))
    out.append("  " + "".join(f"--line-{k}:{v};" for k, v in C["line"].items() if not k.startswith("$")))
    for el, v in C["chem"].items():
        if isinstance(v, dict):
            out.append(f"  --chem-{el}-fill:{v['fill']};--chem-{el}-text:{v['text']};")
    out.append("  " + "".join(f"--bio-{k}:{v};" for k, v in C["bio"].items() if not k.startswith("$")))
    for k in ("sans", "serif", "mono", "math"):
        out.append(f"  --font-{k}:{T['font'][k]};")
    for k, v in ty.items():
        if isinstance(v, dict) and "size" in v:
            out.append(f"  --t-{k}:{v['size']}px;")
    out.append("  " + "".join(f"--s-{k}:{v}px;" for k, v in T["space"].items() if not k.startswith("$")))
    out.append("  " + "".join(f"--w-{k}:{v}px;" for k, v in T["stroke"].items() if isinstance(v, (int, float))))
    out.append(f"  --lane-x0:{L['x0']}px;--lane-w:{L['x1'] - L['x0']}px;")
    out.append(f"  --outline:{ST['outline_color']};--outline-w:{ST['outline']}px;--shadow:{ST['shadow']};")
    out.append(f"  --chip-line:{CH['line']};")
    out.append(f"  --chip-border:{CH['border']}px;--chip-radius:{CH['radius']}px;--chip-pad:{' '.join(str(p) + 'px' for p in CH['pad'])};")
    out.append(f"  --sheet-fill:{T['sheet']['fill']};--sheet-border:{T['sheet']['border']}px;--sheet-radius:{T['sheet']['radius']}px;")
    out.append(f"  --tape-w:{T['tape']['w']}px;--tape-h:{T['tape']['h']}px;")
    out.append("}")
    for subj, W in T["world"]["subjects"].items():             # subject family on #stage (D.color('page'|'paper'|'surface'|'rule'))
        if subj.startswith("$"): continue
        sel = ":root," if subj == "physics" else ""
        out.append(f"{sel}.subject-{subj}{{--c-page:{C['hue']['cream']};--c-paper:{C['hue']['paper']};--c-surface:{C['hue']['paper']};--c-rule:{W['rule']};}}")
    fam = {"sans": "var(--font-sans)", "serif": "var(--font-serif)", "mono": "var(--font-mono)"}
    rule = CH["grid_rule"]; gp = CH["grid_px"]
    grid_bg = f"background-image:linear-gradient({rule} 2px,transparent 2px),linear-gradient(90deg,{rule} 2px,transparent 2px);background-size:{gp}px {gp}px;"
    for st in CH["styles"]:
        out.append(f".chip-{st['name']}{{background-color:{st['bg']};color:{st['fg']};font-family:{fam[st['font']]};{grid_bg if st.get('rules') else ''}}}")
    for name, col in T["tape"]["colors"].items():
        if not name.startswith("$"):
            out.append(f".tape-{name}{{background:{col};}}")
    out.append(f".grid-paper{{{grid_bg}}}")
    BS = T["brand"]["sticker"]
    out.append(f".brand-sticker{{background:{BS['bg']};border-radius:{BS['radius']}px}}.brand-sticker .bs1{{color:{BS['fg1']};font-family:{fam[BS['font1']]}}}.brand-sticker .bs2{{color:{BS['fg2']};font-family:{fam[BS['font2']]}}}")
    return "\n".join(out) + "\n"


def main():
    bad, info = checks()
    src = DS / "tokens.json"; raw = json.loads(src.read_text(encoding="utf-8"))
    lows = sorted(((v, k) for k, v in info.items() if k.startswith(("text.", "chip.", "atom."))))[:3]
    glows = sorted(((v, k) for k, v in info.items() if k.startswith(("line.", "bio.", "link.", "strike."))))[:3]
    raw["contrast"] = {"$comment": "GENERATED by tools/build_tokens.py: WCAG ratios, text >= 4.5 on every surface it can sit on, graphics >= 3. band.* is recorded only (text never sits on a band).",
                       "$lowest_text": [f"{k} {v}" for v, k in lows], "$lowest_graphic": [f"{k} {v}" for v, k in glows], **info}
    src.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DS / "tokens.css").write_text(css(), encoding="utf-8")
    js = ("/* GENERATED by tools/build_tokens.py from tokens.json v" + T["version"] + ". Do not edit. */\n"
          "window.DIKI_TOKENS = " + json.dumps(strip(T), ensure_ascii=False, indent=1) + ";\n")
    (DS / "tokens.js").write_text(js, encoding="utf-8")
    print(json.dumps({"ok": not bad, "lowest_text": raw["contrast"]["$lowest_text"], "lowest_graphic": raw["contrast"]["$lowest_graphic"],
                      "checked": len(info), "failures": bad}, ensure_ascii=False, indent=1))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
