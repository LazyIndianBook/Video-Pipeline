#!/usr/bin/env python3
"""build_scene.py: authoring scene (references tokens/runtime/components) -> one self-contained scene file.

  python3 tools/build_scene.py SRC.html OUT.html [--fixture fixture.json] [--cues sheet.json]
                               [--script script.json --scene s01]    # synthetic sheet via the pilot tooling

1. Inlines every <link rel="stylesheet" href="..."> and <script src="..."> (relative paths only; a remote URL
   is an error). The output needs no sibling files, and the seek lint now sees the runtime and components too.
2. Replaces the inline fallbacks (#cue-sheet-inline, #fixture-inline) when --cues/--script or --fixture is given.
3. Gates (exit 1), v2.0.0:
   * brand: tokens brand.forbidden_on_screen ("ExamLeaf", "AI-generated"), case-insensitive, ANYWHERE in the output
     (code, fixture, cue sheet; PD-20: the disclosure is upload metadata, never in a scene)
   * structural bans only (tokens gates.banned_patterns, regexes): CSS transition / animation / keyframes,
     requestAnimationFrame, Date.now / new Date, Math.random, remote URLs, elastic / back / bounce / spring
     easings, Unicode subscript code points. The A2 decoration ban (washi, polaroid, ransom, grain...) is reversed
     by PD-19: that vocabulary is the house style.
   * node lint_seek_contract.js --level 1 on the output.
"""
import argparse, json, pathlib, re, subprocess, sys

DS = pathlib.Path(__file__).resolve().parent.parent
ROOT = DS.parent.parent
LINT = ROOT / "12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js"
PILOT_TOOLING = ROOT / "16_pilot_builds_2026-10-16/tooling"
TOK = json.loads((DS / "tokens.json").read_text(encoding="utf-8"))


def inline(html, base):
    def css(m):
        href = m.group(1)
        if re.match(r"^[a-z]+:|^//", href):
            sys.exit(f"remote stylesheet not allowed: {href}")
        return "<style>/* inlined " + pathlib.Path(href).name + " */\n" + (base / href).read_text(encoding="utf-8") + "</style>"
    def js(m):
        src = m.group(1)
        if re.match(r"^[a-z]+:|^//", src):
            sys.exit(f"remote script not allowed: {src}")
        body = (base / src).read_text(encoding="utf-8").replace("</script", "<\\/script")
        return "<script>/* inlined " + pathlib.Path(src).name + " */\n" + body + "</script>"
    html = re.sub(r'<link rel="stylesheet" href="([^"]+)">', css, html)
    return re.sub(r'<script src="([^"]+)"></script>', js, html)


def put_json(html, block_id, data):
    pat = re.compile(r'(<script type="application/json" id="' + block_id + r'">)(.*?)(</script>)', re.S)
    if not pat.search(html):
        sys.exit(f"no #{block_id} block in source")
    return pat.sub(lambda m: m.group(1) + "\n" + json.dumps(data, ensure_ascii=False) + "\n" + m.group(3), html, count=1)


def gates(html):
    bad = []
    for w in TOK["brand"]["forbidden_on_screen"]:
        if w.lower() in html.lower():
            bad.append(f"forbidden brand string '{w}' present")
    code = re.sub(r'<script type="application/json".*?</script>', "", html, flags=re.S)
    for g in TOK["gates"]["banned_patterns"]:
        m = re.search(g["re"], code if g["scope"] == "code" else html)
        if m:
            bad.append(f"banned pattern {g['id']} ({g['why']}): {m.group(0)!r}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--fixture"); ap.add_argument("--cues"); ap.add_argument("--script"); ap.add_argument("--scene")
    a = ap.parse_args()
    src = pathlib.Path(a.src).resolve(); out = pathlib.Path(a.out).resolve()
    html = inline(src.read_text(encoding="utf-8"), src.parent)
    if a.fixture:
        html = put_json(html, "fixture-inline", json.loads(pathlib.Path(a.fixture).read_text(encoding="utf-8")))
    if a.cues:
        html = put_json(html, "cue-sheet-inline", json.loads(pathlib.Path(a.cues).read_text(encoding="utf-8")))
    elif a.script:
        sys.path.insert(0, str(PILOT_TOOLING)); import pilotlib as L
        sheet, _, _ = L.build_scene_sheet(L.load_script(a.script), a.scene or "s01")
        html = put_json(html, "cue-sheet-inline", sheet)
    bad = gates(html)
    out.write_text(html, encoding="utf-8")
    r = subprocess.run(["node", str(LINT), "--level", "1", str(out)], capture_output=True, text=True)
    lint = json.loads(r.stdout)["summary"] if r.stdout.strip().startswith("{") else {"ok": False, "raw": r.stdout + r.stderr}
    print(json.dumps({"out": str(out), "bytes": out.stat().st_size, "lint_level1": lint, "gate_failures": bad}, indent=1))
    if r.returncode or bad:
        print(r.stderr, file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
