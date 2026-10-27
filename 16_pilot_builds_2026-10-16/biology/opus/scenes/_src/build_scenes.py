#!/usr/bin/env python3
"""build_scenes.py: assembles the self-contained scenes/sNN.html files from engine.js + per-scene markup below.
Static art only (build-time seeded jitter for torn edges is fixed markup, not runtime randomness). Headlines and the
disclosure come from ../../script.json; inline fallbacks are the synthetic cue sheet and fixtures/fixture.json.
Run: python3 scenes/_src/build_scenes.py   (from the tier folder or anywhere)."""
import json, math, pathlib, random, sys

SRC = pathlib.Path(__file__).resolve().parent
TIER = SRC.parent.parent
sys.path.insert(0, str(TIER.parent.parent / "tooling"))
import pilotlib as L  # noqa: E402

SCRIPT = L.load_script(TIER / "script.json")
FIXTURE = json.loads((TIER / "fixtures" / "fixture.json").read_text(encoding="utf-8"))
ENGINE = (SRC / "engine.js").read_text(encoding="utf-8")
PAUSE_TEXT = "Pause. Predict."

CSS = r"""
:root{--bg:#F7F9FC;--ink:#14213D;--sec:#526074;--blue:#185ABD;--red:#B42318;
  --cream:#f3ecdf;--paper:#fbf7ee;--kraft:#b98f5e;--sink:#2b2622;--pencil:#3a332c;--tomato:#d9483b;--mustard:#e0a73a;
  --pteal:#2f7f7a;--ultra:#2f4fa8;--olive:#7c8a3c;--sage:#9dbb8e;--blush:#f1a9a0;--navy:#1b2a4a;
  --font:"Noto Sans","Noto Sans Devanagari","Noto Sans Bengali","Kohinoor Devanagari","Kohinoor Bangla",system-ui,sans-serif;
  --head:70px;--label:54px;--eq:72px;
  --shadow:0 9px 7px rgba(74,48,22,.30),0 2px 1.5px rgba(0,0,0,.20)}
html,body{margin:0;background:var(--cream)}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--cream);font-family:var(--font);color:var(--ink)}
#bg{position:absolute;left:0;top:0}
.box{position:absolute;box-sizing:border-box}
#title .hl{position:absolute;left:0;top:0;right:0;bottom:0;display:flex;flex-wrap:wrap;align-content:center;justify-content:center;gap:30px 18px}
.tile{display:inline-block;font-size:var(--head);font-weight:800;line-height:1.12;padding:2px 18px 8px;border:6px solid #fffdf7;border-radius:3px;opacity:0;box-shadow:var(--shadow)}
.tile.grid{background-image:linear-gradient(rgba(47,79,168,.22) 2px,transparent 2px),linear-gradient(90deg,rgba(47,79,168,.22) 2px,transparent 2px);background-size:20px 20px}
#vis{position:absolute;width:864px;height:659px;transform-origin:50% 60%}
.prop{position:absolute;transform-origin:50% 100%}
.prop>svg{display:block;overflow:visible;position:absolute;left:0;top:0}
.tag{position:absolute;box-sizing:border-box;background:var(--bg);color:var(--ink);font-weight:600;font-size:var(--label);line-height:1.2;border:8px solid #fff;border-radius:6px;padding:2px 18px 6px;box-shadow:var(--shadow);white-space:nowrap;transform-origin:50% 50%}
.tag.big{font-size:var(--eq)}
.tape{position:absolute;width:110px;height:32px;top:-30px;left:50%;margin-left:-55px;background:rgba(241,169,160,.72);transform:rotate(-4deg)}
.tape.m{background:rgba(224,167,58,.62)} .tape.t{background:rgba(47,127,122,.45)}
.sheet{position:absolute;box-sizing:border-box;background:var(--bg);color:var(--ink);border:8px solid #fff;border-radius:6px;box-shadow:var(--shadow);display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px}
.eq .row{display:flex;align-items:baseline;justify-content:center;gap:0 22px;font-size:var(--eq);font-weight:600;line-height:1.12;white-space:nowrap}
.piece{display:inline-block;transform-origin:50% 60%}
.piece b{font-weight:700;margin-right:4px}
.atom{display:inline-flex;align-items:center;justify-content:center;width:84px;height:84px;border-radius:50%;background:var(--ink);color:var(--bg);font-weight:700;margin-right:12px}
#cap{display:flex;align-items:center;justify-content:center}
#cap .tag{position:relative}
.wrap{white-space:normal;text-align:center;max-width:860px}
.zone{display:none;position:absolute;border:2px dashed #B42318;box-sizing:border-box;font:600 28px system-ui;color:#B42318;padding:6px 12px;z-index:9}
.safe .zone{display:block}
#scrub{position:fixed;right:8px;top:8px;width:360px}
"""

DEFS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
 <filter id="cut" x="-20%" y="-20%" width="140%" height="145%" color-interpolation-filters="sRGB">
  <feMorphology in="SourceGraphic" operator="dilate" radius="8" result="d"/>
  <feFlood flood-color="#fffdf7"/><feComposite in2="d" operator="in" result="border"/>
  <feGaussianBlur in="d" stdDeviation="3.5"/><feOffset dy="9" result="o1"/>
  <feFlood flood-color="#4a3016" flood-opacity="0.30"/><feComposite in2="o1" operator="in" result="s1"/>
  <feGaussianBlur in="d" stdDeviation="0.75"/><feOffset dy="2" result="o2"/>
  <feFlood flood-color="#000" flood-opacity="0.20"/><feComposite in2="o2" operator="in" result="s2"/>
  <feMerge><feMergeNode in="s1"/><feMergeNode in="s2"/><feMergeNode in="border"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
 <filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3" seed="3"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0.42  0 0 0 0 0.33  0 0 0 0 0.22  0.5 0 0 0 -0.18"/>
 </filter>
 <filter id="wash" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="3" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="38"/><feGaussianBlur stdDeviation="6"/></filter>
 <radialGradient id="vig" cx="50%" cy="48%" r="75%"><stop offset="62%" stop-color="#4a3016" stop-opacity="0"/><stop offset="100%" stop-color="#4a3016" stop-opacity="0.12"/></radialGradient>
</defs></svg>"""


def torn(y, fill, seed, y2=1960, amp=9, step=24, edge=True):
    """A torn-paper strip whose ragged top edge sits at y (static markup; seeded at build time)."""
    r = random.Random(seed)
    pts = [(x, y + (r.random() - 0.5) * 2 * amp) for x in range(-40, 1121, step)]
    top = " ".join(f"L{x} {v:.1f}" for x, v in pts)
    body = f'<path d="M-40 {y2} {top} L1120 {y2} Z" fill="{fill}"/>'
    if not edge:
        return body
    fib = " ".join(f"L{x} {v - 7 - r.random() * 3:.1f}" for x, v in pts)
    return f'<path d="M-40 {y2} {fib} L1120 {y2} Z" fill="#fffdf7"/>' + f'<path d="M-40 {y2} {top} L1120 {y2} Z" fill="#000" opacity="0.10" transform="translate(0 -3)"/>' + body


def sparkle(x, y, s=22):
    return (f'<path d="M{x-s} {y} L{x+s} {y} M{x} {y-s} L{x} {y+s} M{x-s*.55} {y-s*.55} L{x+s*.55} {y+s*.55} M{x-s*.55} {y+s*.55} L{x+s*.55} {y-s*.55}" '
            'stroke="#3a332c" stroke-width="4" stroke-linecap="round" opacity="0.55"/>')


def bg(kind):
    parts = ['<rect width="1080" height="1920" fill="#f3ecdf"/>']
    if kind in ("sky", "sky2"):
        parts.append('<g filter="url(#wash)" opacity="0.9"><ellipse cx="300" cy="380" rx="520" ry="260" fill="#a9c0e2" opacity="0.38"/>'
                     '<ellipse cx="820" cy="620" rx="420" ry="300" fill="#a9c0e2" opacity="0.32"/>'
                     '<ellipse cx="260" cy="840" rx="300" ry="120" fill="#fbf7ee" opacity="0.8"/><ellipse cx="860" cy="300" rx="220" ry="90" fill="#fbf7ee" opacity="0.8"/></g>')
    if kind == "kraft":
        parts.append(torn(470, "#b98f5e", 21, y2=1300))
        r = random.Random(4)
        parts.append("".join(f'<circle cx="{r.uniform(0,1080):.0f}" cy="{r.uniform(480,1230):.0f}" r="{r.uniform(1.5,4):.1f}" fill="#3a332c" opacity="0.18"/>' for _ in range(120)))
        parts.append(torn(1236, "#f3ecdf", 22))
    if kind == "sky":
        parts.append(torn(1118, "#9dbb8e", 31) + torn(1250, "#7c8a3c", 32) + torn(1420, "#b98f5e", 33))
    else:
        parts.append(torn(1530, "#9dbb8e", 41) + torn(1660, "#7c8a3c", 42))
    parts.append('<rect width="1080" height="1920" filter="url(#grain)" opacity="0.5"/>')
    parts.append('<rect width="1080" height="1920" fill="url(#vig)"/>')
    parts.append(sparkle(54, 160) + sparkle(1020, 205, 18) + sparkle(46, 1840, 18) + sparkle(1030, 1800))
    return '<svg id="bg" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">' + "".join(parts) + "</svg>"


def svg(w, h, inner, vb=None):
    return f'<svg width="{w}" height="{h}" viewBox="{vb or f"0 0 {w} {h}"}" aria-hidden="true">{inner}</svg>'


PEN = 'stroke="#3a332c" stroke-width="2.5" stroke-opacity="0.55" fill="none"'

TREE = ('<g filter="url(#cut)"><g data-boil="tree-canopy">'
        '<path d="M245 620 C252 520 248 440 232 360 L330 360 C314 440 310 520 322 620 Z" fill="#b98f5e"/>'
        '<path d="M245 620 C232 600 206 606 190 618 Z M322 620 C336 600 360 606 378 618 Z" fill="#b98f5e"/>'
        '<path d="M262 382 C205 335 140 322 86 306 M300 382 C362 334 432 322 486 304" stroke="#b98f5e" stroke-width="26" stroke-linecap="round" fill="none"/>'
        '<path d="M112 316 L114 600 M150 326 L148 560 M418 322 L420 590 M458 312 L456 548" stroke="#b98f5e" stroke-width="8" stroke-linecap="round"/>'
        '<path d="M262 380 C262 470 270 540 266 612 M298 380 C300 470 292 540 300 612" ' + PEN + '/>'
        '<ellipse cx="280" cy="200" rx="262" ry="150" fill="#7c8a3c"/>'
        '<ellipse cx="150" cy="180" rx="125" ry="92" fill="#9dbb8e"/><ellipse cx="410" cy="170" rx="132" ry="96" fill="#9dbb8e"/>'
        '<ellipse cx="282" cy="110" rx="160" ry="92" fill="#9dbb8e"/><ellipse cx="200" cy="262" rx="112" ry="62" fill="#7c8a3c"/><ellipse cx="380" cy="262" rx="118" ry="62" fill="#7c8a3c"/>'
        '<ellipse cx="282" cy="96" rx="96" ry="46" fill="#b8cfa5" opacity="0.8"/><ellipse cx="420" cy="150" rx="70" ry="38" fill="#b8cfa5" opacity="0.7"/>'
        '<path d="M60 190 C80 120 160 90 210 100 M330 60 C400 50 470 100 500 150 M120 260 C170 300 240 300 280 280" ' + PEN + '/>'
        '</g></g>')

ELEPHANT = ('<g filter="url(#cut)"><g data-boil="elephant"><g transform="translate(220 0) scale(-1 1)">'
            '<path d="M70 128 h22 v38 h-22 Z M98 130 h22 v36 h-22 Z M140 130 h22 v36 h-22 Z M166 126 h22 v40 h-22 Z" fill="#a8845a"/>'
            '<ellipse cx="128" cy="96" rx="78" ry="52" fill="#b98f5e"/>'
            '<circle cx="54" cy="80" r="40" fill="#b98f5e"/>'
            '<path d="M24 92 C10 110 14 140 24 156" stroke="#b98f5e" stroke-width="17" stroke-linecap="round" fill="none"/>'
            '<ellipse cx="78" cy="74" rx="24" ry="32" fill="#f1a9a0"/>'
            '<circle cx="42" cy="70" r="4" fill="#2b2622"/><path d="M30 104 C36 112 46 112 50 106" stroke="#fbf7ee" stroke-width="6" stroke-linecap="round" fill="none"/>'
            '<path d="M204 92 C214 100 214 112 208 118" stroke="#3a332c" stroke-width="3" fill="none"/>'
            '<path d="M70 70 C100 40 170 40 196 80" ' + PEN + '/></g></g></g>')

QMARK = ('<path class="ink" d="M38 76 C36 26 122 18 124 70 C126 108 82 110 82 152" stroke="#2b2622" stroke-width="10" stroke-linecap="round" fill="none"/>'
         '<path class="ink" d="M82 186 a7 7 0 1 0 0.1 0" stroke="#2b2622" stroke-width="12" stroke-linecap="round" fill="none"/>')


def card(inner, rot, tape, cid):
    return svg(250, 330, f'<defs><clipPath id="clip{cid}"><rect x="18" y="18" width="214" height="232" rx="2"/></clipPath></defs>'
               f'<g transform="rotate({rot} 125 165)"><g filter="url(#cut)"><rect x="0" y="0" width="250" height="330" rx="4" fill="#fbf7ee"/>'
               f'<g clip-path="url(#clip{cid})"><g data-boil="card{cid}" data-amp="0.7">{inner}</g></g>'
               '<rect x="18" y="18" width="214" height="232" fill="none" stroke="#3a332c" stroke-opacity="0.35" stroke-width="2"/></g>'
               f'<rect x="80" y="-14" width="90" height="30" fill="{tape}" transform="rotate(-5 125 0)"/></g>')


SOIL_PIC = ('<rect x="0" y="0" width="250" height="330" fill="#b98f5e"/><rect x="0" y="18" width="250" height="40" fill="#9dbb8e"/>'
            '<path d="M0 58 C60 50 120 66 250 56 L250 120 L0 120 Z" fill="#3a332c" opacity="0.30"/>'
            '<ellipse cx="70" cy="150" rx="18" ry="11" fill="#f3ecdf"/><ellipse cx="160" cy="190" rx="22" ry="13" fill="#9dbb8e"/><ellipse cx="110" cy="224" rx="14" ry="9" fill="#f3ecdf"/>'
            '<ellipse cx="196" cy="128" rx="12" ry="8" fill="#f3ecdf"/><path d="M40 90 C70 110 60 150 90 170" ' + PEN + '/>')
WATER_PIC = ('<rect x="0" y="0" width="250" height="330" fill="#dfe6ef"/>'
             '<path d="M125 52 C150 100 182 136 182 172 C182 206 156 230 125 230 C94 230 68 206 68 172 C68 136 100 100 125 52 Z" fill="#2f4fa8"/>'
             '<path d="M100 170 C100 150 110 136 118 126" stroke="#fbf7ee" stroke-width="9" stroke-linecap="round" fill="none"/>'
             '<path d="M30 236 C60 226 90 240 120 230 M140 236 C170 226 200 240 230 230" stroke="#2f4fa8" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.6"/>')
AIR_PIC = ('<rect x="0" y="0" width="250" height="330" fill="#e7edf2"/>'
           '<ellipse cx="150" cy="80" rx="62" ry="28" fill="#fbf7ee"/><ellipse cx="110" cy="86" rx="44" ry="24" fill="#fbf7ee"/>'
           '<path d="M36 150 C80 120 130 170 180 140 C210 122 214 100 196 96 M50 196 C100 170 150 214 206 186 M70 112 C90 100 110 108 118 118" '
           'stroke="#3a332c" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.65"/>')

LOG = ('<g filter="url(#cut)"><g data-boil="log"><ellipse cx="110" cy="100" rx="102" ry="90" fill="#b98f5e"/><ellipse cx="110" cy="100" rx="84" ry="74" fill="#f3ecdf"/>'
       '<ellipse cx="110" cy="100" rx="64" ry="56" fill="none" stroke="#e0a73a" stroke-width="7"/><ellipse cx="110" cy="100" rx="42" ry="36" fill="none" stroke="#e0a73a" stroke-width="7"/>'
       '<ellipse cx="110" cy="100" rx="20" ry="17" fill="none" stroke="#e0a73a" stroke-width="7"/><path d="M110 100 L150 40 M110 100 L58 150" ' + PEN + '/></g></g>')

PLANT = ('<g filter="url(#cut)"><g data-boil="plant">'
         '<path d="M222 250 C214 210 226 170 220 120" stroke="#7c8a3c" stroke-width="16" stroke-linecap="round" fill="none"/>'
         '<path d="M220 168 C150 64 60 72 22 128 C76 212 170 214 220 168 Z" fill="#7c8a3c"/>'
         '<path d="M220 168 C160 130 100 120 40 128" ' + PEN + '/>'
         '<path d="M220 124 C282 20 384 18 426 70 C372 152 282 164 220 124 Z" fill="#9dbb8e"/>'
         '<path d="M220 124 C290 90 360 72 420 72" ' + PEN + '/>'
         '<path d="M0 236 C80 226 160 242 230 234 C300 228 380 242 440 234 L440 300 L0 300 Z" fill="#b98f5e"/>'
         '</g></g>')
STOMATA = ('<circle cx="66" cy="66" r="56" fill="#fbf7ee" fill-opacity="0.85"/>'
           '<path d="M52 34 C30 44 30 88 52 98 C62 84 62 48 52 34 Z" fill="#7c8a3c"/><path d="M80 34 C102 44 102 88 80 98 C70 84 70 48 80 34 Z" fill="#7c8a3c"/>'
           '<path class="ink" d="M66 10 a56 56 0 1 0 0.1 0" stroke="#2b2622" stroke-width="7" fill="none" stroke-linecap="round"/>'
           '<path class="ink" d="M106 108 L136 138" stroke="#2b2622" stroke-width="10" stroke-linecap="round"/>')
ROOTS = ('<path class="ink" d="M162 0 C160 22 140 36 118 58 M162 0 C168 26 190 40 214 62 M162 0 C162 26 164 44 160 68 M136 34 C120 38 104 36 92 44 M196 40 C214 40 228 34 240 40" '
         'stroke="#3a332c" stroke-width="5" stroke-linecap="round" fill="none"/>'
         '<g filter="url(#cut)"><path d="M70 30 C76 40 80 46 80 52 C80 58 75 62 70 62 C65 62 60 58 60 52 C60 46 64 40 70 30 Z" fill="#2f4fa8"/>'
         '<path d="M290 22 C296 32 300 38 300 44 C300 50 295 54 290 54 C285 54 280 50 280 44 C280 38 284 32 290 22 Z" fill="#2f4fa8"/></g>')
SUN = ('<g filter="url(#cut)"><g data-boil="sun">' +
       "".join(f'<path d="M200 100 L{200+125*math.cos(a*0.5236+0.13):.1f} {100+125*math.sin(a*0.5236+0.13):.1f} L{200+125*math.cos(a*0.5236+0.35):.1f} {100+125*math.sin(a*0.5236+0.35):.1f} Z" fill="{"#d9483b" if a % 2 else "#e0a73a"}"/>' for a in range(12)) +
       '<circle cx="200" cy="100" r="74" fill="#e0a73a"/><circle cx="200" cy="100" r="54" fill="#f0bf5c" opacity="0.7"/></g></g>')
AIR = ('<g data-boil="air" data-amp="1.4"><path d="M10 40 C40 10 80 50 60 70 C44 84 30 64 44 56 M4 100 C40 80 70 110 96 92" stroke="#3a332c" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.55"/></g>')
CLOUD = ('<g filter="url(#cut)"><g data-boil="cloud"><path d="M40 170 C0 170 0 110 46 106 C40 56 110 40 136 78 C160 20 250 24 262 82 C320 66 370 110 340 160 C330 176 300 180 280 178 Z" fill="#fbf7ee"/>'
         '<path d="M40 170 C0 170 0 110 46 106 C40 56 110 40 136 78 C160 20 250 24 262 82 C320 66 370 110 340 160 C330 176 300 180 280 178 Z" fill="#2f4fa8" opacity="0.12"/></g></g>')
POT = ('<g filter="url(#cut)"><g data-boil="pot">'
       '<path d="M190 160 C176 110 190 70 150 30 M190 150 C210 100 240 80 270 70" stroke="#7c8a3c" stroke-width="10" stroke-linecap="round" fill="none"/>'
       '<path d="M150 30 C110 30 96 70 120 92 C150 86 160 56 150 30 Z" fill="#9dbb8e"/><path d="M270 70 C300 50 330 80 310 104 C284 112 266 96 270 70 Z" fill="#7c8a3c"/>'
       '<ellipse cx="190" cy="168" rx="160" ry="30" fill="#3a332c" opacity="0.85"/>'
       '<path d="M28 160 L352 160 L352 196 L28 196 Z" fill="#d9483b"/>'
       '<path d="M48 196 L332 196 L300 420 L80 420 Z" fill="#d9483b"/><path d="M48 196 L332 196 L326 236 L54 236 Z" fill="#000" opacity="0.10"/>'
       '<path d="M90 260 C150 250 240 270 300 254" ' + PEN + '/></g></g>')
DROP = ('<g filter="url(#cut)"><path d="M30 6 C40 22 50 34 50 46 C50 58 41 66 30 66 C19 66 10 58 10 46 C10 34 20 22 30 6 Z" fill="#2f4fa8"/></g>')


def fxs(path, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-fx="{path}"></{tag}>'


def eq_rows(ids=True, rv=True):
    """6CO2 + 6H2O -> C6H12O6 + 6O2, every glyph bound to the fixture. ids=True gives each piece a cue target."""
    def piece(pid, inner):
        attrs = f' id="{pid}" data-reveal data-anim="fade"' if ids else ""
        return f'<span class="piece"{attrs}>{inner}</span>'
    r1 = piece("eq_co2", fxs("parameters.coef_co2", "b") + fxs("display.co2")) + piece("eq_h2o", fxs("display.plus") + " " + fxs("parameters.coef_h2o", "b") + fxs("display.h2o"))
    r2 = piece("eq_arrow", fxs("display.arrow")) + piece("eq_glucose", fxs("display.glucose")) + piece("eq_o2", fxs("display.plus") + " " + fxs("parameters.coef_o2", "b") + fxs("display.o2"))
    return f'<div class="row">{r1}</div><div class="row">{r2}</div>'


def prop(pid, x, y, w, h, inner, reveal=True, anim="pop", rot=None, extra=""):
    a = f' id="{pid}"' if pid else ""
    if reveal:
        a += f' data-reveal data-anim="{anim}"'
    if rot is not None:
        a += f' data-rot="{rot}"'
    return f'<div class="prop"{a} style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{inner}{extra}</div>'


SCENES = {
    "s01": dict(bg="sky", push=0.03, vis=
        prop("tree", 270, 0, 560, 620, svg(560, 620, TREE)) +
        prop("elephant", 34, 452, 220, 170, svg(220, 170, ELEPHANT)) +
        prop("qmark", 70, 120, 160, 210, svg(160, 210, QMARK), anim="draw", rot=0), cap=""),
    "s02": dict(bg="kraft", freeze="pause_chip", vis=
        prop("log", 322, 0, 220, 200, svg(220, 200, LOG)) +
        prop("card_soil", 22, 262, 250, 330, card(SOIL_PIC, -3, "rgba(241,169,160,.8)", 1), rot=0) +
        prop("card_water", 307, 250, 250, 330, card(WATER_PIC, 2, "rgba(224,167,58,.7)", 2), rot=0) +
        prop("card_air", 592, 262, 250, 330, card(AIR_PIC, -2, "rgba(47,127,122,.5)", 3), rot=0),
        cap='<div id="pause_chip" class="tag big" data-reveal data-anim="fade"></div>'),
    "s03": dict(bg="sky2", vis=
        prop(None, 40, 0, 440, 300, svg(440, 300, PLANT), reveal=False).replace('class="prop"', 'class="prop" id="plant" data-reveal data-anim="pop" data-rot="0"', 1) +
        prop("roots", 100, 240, 330, 62, svg(330, 62, ROOTS, vb="0 0 360 70"), anim="draw", rot=0) +
        prop("stomata", 342, 22, 140, 140, svg(140, 140, STOMATA), anim="draw", rot=0) +
        prop("chl_tag", 0, 118, 360, 90, '<div class="tag lbl" style="left:0;top:0"><div class="tape m"></div>' + fxs("display.chlorophyll") + '</div>', anim="fade") +
        prop(None, 478, 168, 100, 120, svg(100, 120, AIR), reveal=False) +
        prop("sun", 536, 0, 328, 300, svg(328, 300, SUN) + '<div class="tag lbl" style="left:24px;top:192px"><div class="tape"></div>' + fxs("display.sunlight") + '</div>', anim="fade") +
        '<div class="sheet eq" id="eqsheet" data-reveal data-anim="fade" data-follow="eq_co2" style="left:0;top:318px;width:864px;height:338px"><div class="tape t" style="left:12%"></div><div class="tape" style="left:88%"></div>' + eq_rows() +
        '<div class="row"><span class="piece" id="c_count" data-reveal data-anim="fade" style="display:inline-flex;align-items:center;font-size:64px">' +
        fxs("display.carbon_symbol", "span", "atom") + fxs("results.carbon_left", "b") + '<span style="margin:0 26px">' + fxs("display.equals") + '</span>' +
        fxs("display.carbon_symbol", "span", "atom") + fxs("results.carbon_right", "b") + '</span></div></div>', cap=""),
    "s04": dict(bg="sky2", vis=
        prop("co2_tag", 0, 0, 394, 200, svg(394, 200, CLOUD) + '<div class="tag big" style="left:118px;top:58px">' + fxs("display.co2") + '</div>', anim="fade") +
        prop("soil_pot", 10, 222, 380, 430, svg(380, 430, POT)) +
        prop("h2o_tag", 86, 448, 250, 120, svg(60, 70, DROP) + '<div class="tag big" style="left:64px;top:0">' + fxs("display.h2o") + '</div>', anim="fade") +
        prop("pie", 420, 40, 444, 560,
             '<div style="position:absolute;left:0;right:0;top:0;display:flex;justify-content:center"><div class="tag big" style="position:relative;font-size:64px">' + fxs("display.glucose") + '</div></div>' +
             svg(444, 560, '<g filter="url(#cut)"><circle cx="222" cy="272" r="140" fill="#9dbb8e"/>'
                 '<path data-geom="pie" data-fx-geom="results.carbon_mass_fraction" data-cx="222" data-cy="272" data-r="140" data-anchor="pie_pct" data-anchor-k="0.62" fill="#e0a73a"/></g>'
                 '<circle cx="222" cy="272" r="140" ' + PEN + '/>') +
             '<div class="tag big" id="pie_pct" style="font-size:64px">' + fxs("results.carbon_percent") + fxs("display.percent") + '</div>' +
             '<div style="position:absolute;left:0;right:0;top:440px;display:flex;justify-content:center"><div class="tag lbl" style="position:relative">' + fxs("results.glucose_carbon_mass") + " " + fxs("display.slash") + " " + fxs("results.glucose_molar_mass") + '</div></div>', anim="fade"),
        cap=""),
    "s05": dict(bg="sky", vis=
        prop("tree2", 282, 0, 300, 332, svg(300, 332, TREE, vb="0 0 560 620")) +
        prop(None, 190, 300, 484, 44, svg(484, 44, '<g filter="url(#cut)"><path d="M0 44 C40 10 120 2 242 2 C364 2 444 10 484 44 Z" fill="#9dbb8e"/><path d="M60 30 C120 20 200 22 250 18" ' + PEN + '/></g>'), reveal=False) +
        '<div class="sheet eq" id="eq_full" data-reveal data-anim="fade" style="left:0;top:344px;width:864px;height:312px;transform-origin:50% 50%"><div class="tape m" style="left:50%"></div>' + eq_rows(ids=False) +
        '<div class="row" style="gap:0 28px"><span class="tag lbl" style="position:relative">' + fxs("display.sunlight") + '</span><span class="tag lbl" style="position:relative">' + fxs("display.chlorophyll") + '</span></div></div>',
        cap='<div id="disclosure" class="tag wrap" data-reveal data-anim="fade" data-text-role="caption" style="font-size:50px"></div>'),
}


def config(sid):
    beats = L.beats_by_scene(SCRIPT)[sid]
    heads = [{"beat": b["id"], "words": L.words_of(b["on_screen"]["headline"]), "q": b["slot"] in ("hook.question_reveal", "check.predict")}
             for b in beats if b.get("on_screen", {}).get("headline")]
    cfg = {"id": sid, "headlines": heads}
    sc = SCENES[sid]
    if sc.get("push"):
        cfg["pushIn"] = sc["push"]
    if sc.get("freeze"):
        cfg["freezeOn"] = sc["freeze"]
        pb = next(b for b in beats if b["slot"] == "check.predict")
        cfg["approvedText"] = [{"element_id": "pause_chip", "text": PAUSE_TEXT, "words": [w for w in ("Pause", "predict") if L.norm_word(w) in {L.norm_word(x) for x in L.words_of(pb["text"])}]}]
    for b in beats:
        if b["slot"] == "outro.disclosure":
            cfg["approvedText"] = [{"element_id": "disclosure", "text": b["text"], "words": L.words_of(b["text"]), "breakAfter": ";"}]
    return cfg


def build(sid):
    sc = SCENES[sid]
    sheet, _, _ = L.build_scene_sheet(SCRIPT, sid)
    title = next(s["title"] for s in SCRIPT["scenes"] if s["id"] == sid)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>{SCRIPT['video_id']} {sid}: {title}</title>
<style>{CSS}</style>
</head>
<body>
<div id="stage">
{DEFS}
{bg(sc['bg'])}
<div id="title" class="box" data-zone="0"></div>
<div id="visbox" class="box" data-zone="1"><div id="vis">{sc['vis']}</div></div>
<div id="cap" class="box" data-zone="2">{sc['cap']}</div>
</div>
<script type="application/json" id="scene-config">{json.dumps(config(sid), ensure_ascii=False)}</script>
<!-- INLINE FALLBACKS (preview only): synthetic evenly spaced cue sheet and the fixture. Production injects both. -->
<script type="application/json" id="cue-sheet-inline">{json.dumps(sheet, ensure_ascii=False)}</script>
<script type="application/json" id="fixture-inline">{json.dumps(FIXTURE, ensure_ascii=False)}</script>
<script>
{ENGINE}
</script>
</body>
</html>
"""
    out = TIER / "scenes" / f"{sid}.html"
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(TIER), len(html), "bytes")


if __name__ == "__main__":
    for sid in (sys.argv[1:] or SCENES):
        build(sid)
