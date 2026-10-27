#!/usr/bin/env python3
"""brand_check.py - Professor Diki Simplified brand gate v1.0.0 (stdlib only).

Usage:
  python3 brand_check.py BUILD_DIR      # pilot layout: script.json, scenes/*.html, fixtures/fixture.json,
                                        # narration/timeline.json, render/*.mp4 (optional)
  python3 brand_check.py --selftest

Fails if a forbidden string (strings.json "forbidden") appears in spoken text, on-screen text (scene text nodes outside
<script>/<style>/<title>, plus fixture values bound by data-fx), fixture strings, script title/topic/video_id, or an MP4
filename or MP4 title tag. Passes only if the outro scene (last scene in script.json) shows the header lockup text and the
end-card lines for the build's voice path, has no unfilled {{slot}}, and the last spoken line is the outro line.
Prints a JSON report. Exit codes: 0 pass, 1 fail, 2 usage/IO error.
"""
import html.parser, json, re, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STRINGS = json.loads((HERE / "strings.json").read_text(encoding="utf-8"))
FORBIDDEN = [(f, re.compile(f["pattern"], re.I)) for f in STRINGS["forbidden"]]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


class TextNodes(html.parser.HTMLParser):
    """Visible text nodes and data-fx paths; skips <script>, <style>, <title>."""
    SKIP = {"script", "style", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.chunks, self.fx = 0, [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.depth += 1
        fx = dict(attrs).get("data-fx")
        if fx:
            self.fx.append(fx)

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth and data.strip():
            self.chunks.append(data.strip())


def fx_value(fixture, path):
    v = fixture
    for k in path.split("."):
        if not isinstance(v, dict) or k not in v:
            return None
        v = v[k]
    return None if isinstance(v, (dict, list)) else str(v)


def string_leaves(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k != "compute":                       # a file path, not display text
                yield from string_leaves(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from string_leaves(v, f"{prefix}[{i}]")
    elif isinstance(obj, str):
        yield prefix, obj


def mp4_title(path):
    """Value of the iTunes-style title atom (the tag FFmpeg writes for -metadata title=...), or None."""
    b = Path(path).read_bytes()
    i = b.find(b"\xa9nam")
    if i < 0 or b[i + 8:i + 12] != b"data":
        return None
    n = int.from_bytes(b[i + 4:i + 8], "big")
    return b[i + 20:i + 4 + n].decode("utf-8", "replace")


def scene_text(path, fixture):
    p = TextNodes()
    p.feed(Path(path).read_text(encoding="utf-8"))
    bound = [(fx, fx_value(fixture, fx)) for fx in p.fx]
    return p.chunks, bound


def check(build):
    build = Path(build)
    script = json.loads((build / "script.json").read_text(encoding="utf-8"))
    fx_path = build / "fixtures/fixture.json"
    fixture = json.loads(fx_path.read_text(encoding="utf-8")) if fx_path.exists() else {}
    tl_path = build / "narration/timeline.json"
    timeline = json.loads(tl_path.read_text(encoding="utf-8")) if tl_path.exists() else {"beats": []}

    sources = []                                      # (kind, where, text)
    for b in script.get("beats", []):
        sources.append(("spoken", f"script.json#{b.get('id')}", b.get("text", "")))
    for b in timeline.get("beats", []):
        sources.append(("spoken", f"narration/timeline.json#{b.get('id')}", " ".join(w["w"] for w in b.get("words", []))))
    outro_text = ""; first_text = ""
    scene_files = [s["file"] for s in script.get("scenes", [])]
    for rel in scene_files:
        chunks, bound = scene_text(build / rel, fixture)
        joined = norm(" ".join(chunks + [v for _, v in bound if v]))
        sources.append(("on_screen", rel, joined))
        outro_text = joined                           # last scene wins
        first_text = first_text or joined             # first scene carries the opening ident (PD-21)
    for where, s in string_leaves(fixture):
        sources.append(("fixture", f"fixtures/fixture.json:{where}", s))
    for k in ("title", "topic", "video_id"):
        if k in script:
            sources.append(("metadata", f"script.json:{k}", str(script[k])))
    for mp4 in sorted((build / "render").glob("*.mp4")) if (build / "render").is_dir() else []:
        sources.append(("metadata", f"render/{mp4.name}:filename", mp4.name))
        t = mp4_title(mp4)
        if t:
            sources.append(("metadata", f"render/{mp4.name}:title_tag", t))

    violations = []
    for kind, where, text in sources:
        for f, rx in FORBIDDEN:
            m = rx.search(text)
            if m:
                violations.append({"check": "forbidden_string", "scope": kind, "where": where, "id": f["id"],
                                   "label": f["label"], "match": m.group(0), "reason": f["reason"]})
        if kind in ("spoken", "on_screen"):               # PD-20: the AI declaration lives in the upload metadata, never in the lesson
            for k, pat in STRINGS["end_card"]["disclosure_line_pattern"].items():
                m = re.search(pat, text, re.I)
                if m:
                    violations.append({"check": "disclosure_in_lesson", "scope": kind, "where": where, "id": "PD-20",
                                       "label": f"disclosure line (Path {k})", "match": m.group(0), "reason": "PD-20: no AI-generated line on screen or spoken; declare at upload"})

    ec, path = STRINGS["end_card"], (script.get("voice") or {}).get("path")
    required = []

    def req(item, ok, detail=""):
        required.append({"item": item, "ok": bool(ok), **({"detail": detail} if detail else {})})

    req("outro_scene_exists", scene_files, scene_files[-1] if scene_files else "script.json has no scenes")
    req("opening_ident_text", STRINGS["header_lockup"]["text"].lower() in first_text.lower(), "PD-21: the brand sticker must be in the first scene")
    req("end_card.brand_line", ec["brand_line"].lower() in outro_text.lower())
    req("voice_path_known", path in ec["disclosure_line_pattern"], f"script.json voice.path = {path!r}; expected one of {sorted(ec['disclosure_line_pattern'])}")
    req("end_card.free_lesson_line", re.search(ec["free_lesson_line_pattern"], outro_text))
    req("no_unfilled_slots_in_outro", "{{" not in outro_text and "}}" not in outro_text)
    beats = script.get("beats", [])
    req("spoken_outro_line_last", beats and norm(beats[-1].get("text", "")) == STRINGS["spoken"]["outro_line"],
        f"expected last beat text {STRINGS['spoken']['outro_line']!r}")

    ok = not violations and all(r["ok"] for r in required)
    return {"status": "pass" if ok else "fail", "checker": "brand_check.py", "strings_version": STRINGS["asset_version"],
            "build": str(build), "voice_path": path, "outro_scene": scene_files[-1] if scene_files else None,
            "violations": violations, "required": required,
            "scanned": {k: sum(1 for s in sources if s[0] == k) for k in ("spoken", "on_screen", "fixture", "metadata")}}


# ---------------------------------------------------------------- selftest
def _write_build(d, *, good):
    d = Path(d)
    for sub in ("scenes", "fixtures", "narration", "render"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    last = "Professor Diki Simplified." if good else "AI-generated narration; script by ExamLeaf."
    script = {"video_id": "phy-ohm-60-01", "topic": "Ohm's law: does current always double?",
              "voice": {"path": "B", "persona": "persona/super-teacher#core"},     # persona ids are not scanned
              "scenes": [{"id": "s01", "file": "scenes/s01.html"}, {"id": "s02", "file": "scenes/s02.html"}],
              "beats": [{"id": "b01", "text": "Double the voltage. Does the current double too?"},
                        {"id": "b02", "text": "The full free lesson is linked below."},
                        {"id": "b03", "text": last}]}
    (d / "script.json").write_text(json.dumps(script), encoding="utf-8")
    fixture = {"compute": "fixtures/compute.py", "parameters": {"v1": 2},
               "display": {"v_unit": "V", "efficiency": "100%" if not good else "all of it", "brand": "Professor Diki Simplified"}}
    (d / "fixtures/fixture.json").write_text(json.dumps(fixture), encoding="utf-8")
    words = [{"w": w} for w in last.split()]
    (d / "narration/timeline.json").write_text(json.dumps({"beats": [{"id": "b03", "words": words}]}), encoding="utf-8")
    s01 = ("<html><head><title>ExamLeaf scene template</title><script>var x='ExamLeaf';</script></head><body>"
           "<svg><text>Professor Diki Simplified</text><text>Double the voltage</text><text data-fx='parameters.v1'></text><text data-fx='display.v_unit'></text>"
           + ("" if good else "<text>Mind blown!</text>") + "</svg></body></html>")
    (d / "scenes/s01.html").write_text(s01, encoding="utf-8")
    if good:
        s02 = ("<svg><text>PROFESSOR DIKI</text><text>SIMPLIFIED</text>"
               "<text>Free lesson: Ohm's law</text></svg>")
    else:
        s02 = "<svg><text data-fx='display.brand'></text><text>AI-generated narration</text><text>Free lesson: {{TOPIC}}</text></svg>"
    (d / "scenes/s02.html").write_text(s02, encoding="utf-8")
    name = "phy-ohm-60-01.mp4" if good else "examleaf_phy-ohm-60-01.mp4"
    title = b"Does current always double?" if good else b"ExamLeaf: Ohm's law guaranteed"
    atom = b"\xa9nam" + (16 + len(title)).to_bytes(4, "big") + b"data" + b"\x00\x00\x00\x01\x00\x00\x00\x00" + title
    (d / "render" / name).write_bytes(b"\x00\x00\x00\x18ftypisom" + b"\x00" * 16 + atom)


def selftest():
    with tempfile.TemporaryDirectory() as t:
        _write_build(Path(t) / "good", good=True)
        _write_build(Path(t) / "bad", good=False)
        g, b = check(Path(t) / "good"), check(Path(t) / "bad")
        assert g["status"] == "pass", json.dumps(g, indent=1)
        assert b["status"] == "fail"
        hits = {(v["scope"], v["id"]) for v in b["violations"]}
        for want in [("spoken", "F01"), ("fixture", "F04"), ("on_screen", "F06"), ("metadata", "F01"), ("metadata", "F02"), ("on_screen", "PD-20"), ("spoken", "PD-20")]:
            assert want in hits, (want, hits)
        failed = {r["item"] for r in b["required"] if not r["ok"]}
        for want in ("no_unfilled_slots_in_outro", "spoken_outro_line_last"):
            assert want in failed, (want, failed)
        assert "opening_ident_text" not in failed, "brand text bound through data-fx must count"
    own = [s for k in ("header_lockup", "end_card", "spoken") for _, s in string_leaves(STRINGS[k])]
    assert not [(s, f["id"]) for s in own for f, rx in FORBIDDEN if rx.search(s)], "strings.json lines must be clean"
    print(json.dumps({"selftest": "OK", "positive": g["status"], "negative": b["status"],
                      "negative_violations": len(b["violations"]),
                      "negative_failed_required": sorted(failed)}, indent=2))
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) != 1 or argv[0].startswith("-"):
        print(__doc__, file=sys.stderr)
        return 2
    try:
        report = check(argv[0])
    except (OSError, ValueError, KeyError) as e:
        print(json.dumps({"status": "error", "error": f"{type(e).__name__}: {e}"}))
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
