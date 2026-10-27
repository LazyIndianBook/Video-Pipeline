#!/usr/bin/env python3
"""qa_scene.py: the design-system QA a built Diki scene must pass (Playwright + installed Chrome).

  $PY tools/qa_scene.py SCENE.html [--samples 9] [--query "?captions=1"]

Loads the self-contained scene (inline cue sheet + fixture), then reports:
  * window.__errors (any error fails; the design-system warnings below fail too)
  * window.__diki_qa: layout, subject world, diagram share, hero fill, verb list, motion inside think windows,
    ident, end card
  * v2 chrome at t = 0: W_WORLD_MISSING if the world layer (#world with >= 2 torn-paper bands) is absent;
    W_IDENT_MISSING if the opening ident is absent, is not the brand, or is not fully visible at t = 0;
    W_IDENT_LATE if it is still visible at 2.5 s (PD-21)
  * seek purity: the stage DOM after seek(t) on a fresh page equals the DOM after a scrambled seek history
Fails (exit 1) on: any error; W_FILL_LOW, W_DIAGRAM_SHARE, W_PERSIST_BROKEN, W_MOTION_IN_THINK, W_VERB_DURATION,
W_HEADLINE_OVERFLOW, W_EQ_OVERFLOW, W_FORMULA_OVERFLOW, W_END_CARD_SHORT, W_NO_HERO, W_CARD_*, W_LAYOUT,
W_WORLD_MISSING, W_IDENT_MISSING, W_IDENT_LATE; any purity mismatch.
"""
import argparse, hashlib, json, pathlib, sys
from playwright.sync_api import sync_playwright

BLOCKING = {"W_FILL_LOW", "W_DIAGRAM_SHARE", "W_PERSIST_BROKEN", "W_MOTION_IN_THINK", "W_VERB_DURATION",
            "W_HEADLINE_OVERFLOW", "W_EQ_OVERFLOW", "W_FORMULA_OVERFLOW", "W_END_CARD_SHORT", "W_NO_HERO",
            "W_CARD_OVERFLOW", "W_CARD_ROWS", "W_LAYOUT", "W_WORLD_MISSING", "W_IDENT_MISSING", "W_IDENT_LATE"}
BRAND = "Professor Diki Simplified"
CHROME_JS = """async (t) => { await window.seek(t); const w = document.getElementById('world');
  const id = document.getElementById('ident'), row = id && id.firstElementChild;
  return { bands: w ? w.querySelectorAll('[data-band]').length : 0,
           ident: id ? id.textContent.trim() : null,
           opacity: row && window.Diki ? window.Diki.effOpacity(row) : 0 }; }"""


def chrome_checks(pg):
    """v2 chrome: the world and the opening ident (frame 0), the ident gone by 2.5 s."""
    c0, c25 = pg.evaluate(CHROME_JS, 0), pg.evaluate(CHROME_JS, 2.5)
    out = []
    if c0["bands"] < 2:
        out.append({"code": "W_WORLD_MISSING", "severity": "warning", "message": f"world layer has {c0['bands']} torn-paper bands at t=0", "t": 0})
    if c0["ident"] != BRAND or c0["opacity"] < 0.99:
        out.append({"code": "W_IDENT_MISSING", "severity": "warning", "message": f"opening ident at t=0: text {c0['ident']!r}, opacity {c0['opacity']:.2f}", "t": 0})
    if c25["opacity"] > 0.001:
        out.append({"code": "W_IDENT_LATE", "severity": "warning", "message": f"opening ident still visible at 2.5 s (opacity {c25['opacity']:.2f})", "t": 2.5})
    return {"t0": c0, "t2.5": c25}, out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("scene"); ap.add_argument("--samples", type=int, default=9); ap.add_argument("--query", default="")
    a = ap.parse_args()
    url = pathlib.Path(a.scene).resolve().as_uri() + a.query
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", headless=True, args=["--force-device-scale-factor=1", "--hide-scrollbars", "--disable-gpu"])
        def page():
            pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
            pg.goto(url); pg.evaluate("async () => { await window.ready }"); return pg
        def dom(pg, order):
            for t in order:
                pg.evaluate(f"window.seek({t})")
            return hashlib.sha256(pg.evaluate("document.getElementById('stage').outerHTML").encode()).hexdigest()
        pg = page(); dur = pg.evaluate("window.DURATION")
        chrome, chrome_warn = chrome_checks(pg)
        times = [round(dur * k / (a.samples - 1), 3) for k in range(a.samples)]
        scramble = [times[-1], times[len(times) // 2], 0.0]
        purity = []
        for t in times:
            fresh = page(); h1 = dom(fresh, [t]); fresh.close()
            h2 = dom(pg, scramble + [t])
            purity.append({"t": t, "same": h1 == h2})
        errs = pg.evaluate("window.__errors") + chrome_warn; qa = pg.evaluate("window.__diki_qa || null")
        b.close()
    bad = [e for e in errs if e["severity"] == "error" or e["code"] in BLOCKING] + [x for x in purity if not x["same"]]
    print(json.dumps({"scene": a.scene, "duration": dur, "qa": qa, "chrome": chrome, "errors": errs, "purity": purity, "ok": not bad}, indent=1, ensure_ascii=False))
    print(f"qa_scene: {'PASS' if not bad else 'FAIL'} | purity {sum(x['same'] for x in purity)}/{len(purity)} | errors {sum(e['severity'] == 'error' for e in errs)} | blocking {len(bad)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
