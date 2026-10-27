#!/usr/bin/env python3
"""text_fixture_diff.py - rendered on-screen text vs fixture / approved display text, plus Indic cluster-split check.

Usage:
  python3 text_fixture_diff.py --expected jobs/<scene>/qa/expected_text.json --rendered jobs/<scene>/qa/dom_text.json [--out diff.json]
  python3 text_fixture_diff.py --selftest

expected_text.json: [{"element_id","text","source": "fixture:<id>#<field>" | "approved_script:<segment_id>", "science": bool}]
  (built from the scene's read-only props, never typed by hand).
dom_text.json: {"mode": "dom"|"ocr", "items": [{"element_id"?, "text", "missing_glyphs"?: [...]}],
                "spans": [{"element_id", "parts": ["...", "..."]}]}   # spans = per-animated-unit text pieces
DOM mode (preferred evidence) matches by element_id after NFC + whitespace + minus-sign normalisation; case-sensitive
(Co is not CO). OCR mode folds compatibility forms (NFKC: H2O vs H₂O) and can only raise MAJOR "verify" findings.
Severity: science mismatch/missing = critical; display-text drift = major; untraceable science-looking text = CRITICAL
(accuracy invariant, report 9; raised from major on 15 Oct 2026, audit science-safety-6: never waivable); broken
grapheme cluster or missing glyph = major/critical (#55).
Exit codes: 0 no critical/major, 1 otherwise, 2 usage/IO error. Edge cases: #12, #54, #55.
"""
import argparse, json, re, sys, unicodedata

MINUS = dict.fromkeys(map(ord, "−‒–—﹣－"), "-")
SCIENCEY = re.compile(r"\d|[=±×÷√∝∞°Ω→⇌]|\b[A-Z][a-z]?\d|\b(?:m/s|km|kg|mol|Hz|nm|N|J|W|V|A|K)\b")
VIRAMAS = {"्", "্"}  # Devanagari, Bengali-Assamese
JOINERS = {"\u200c", "\u200d"}


def norm(s, ocr=False):
    s = unicodedata.normalize("NFKC" if ocr else "NFC", s).translate(MINUS)
    return " ".join(s.split())


def cluster_breaks(parts):
    """Return problems where an animation unit boundary splits a grapheme cluster (heuristic, #55)."""
    probs = []
    for i in range(1, len(parts)):
        prev, cur = parts[i - 1], parts[i]
        if not prev or not cur:
            continue
        if unicodedata.category(cur[0]).startswith("M") or cur[0] in JOINERS:
            probs.append(f"part {i} starts with combining mark/joiner U+{ord(cur[0]):04X}")
        if prev[-1] in VIRAMAS:
            probs.append(f"part {i - 1} ends with a virama U+{ord(prev[-1]):04X} (conjunct split)")
    return probs


def diff(expected, rendered):
    findings = []

    def add(sev, eid, msg, edge):
        findings.append({"severity": sev, "element": eid, "edge_case": edge, "message": msg})
    ocr = rendered.get("mode") == "ocr"
    items = rendered.get("items", [])
    used = set()
    if not ocr:
        by_id = {}
        for it in items:
            by_id.setdefault(it.get("element_id"), []).append(it)
        for ex in expected:
            eid, sci = ex["element_id"], bool(ex.get("science"))
            got = by_id.get(eid)
            if not got:
                add("critical" if sci else "major", eid, f"expected text {ex['text']!r} not rendered", "#12")
                continue
            used.add(eid)
            for g in got:
                if norm(g["text"]) != norm(ex["text"]):
                    add("critical" if sci else "major", eid,
                        f"rendered {g['text']!r} != {ex['source']} {ex['text']!r}", "#12" if sci else "#11")
        for it in items:
            if it.get("element_id") not in used and SCIENCEY.search(it.get("text", "")):
                add("critical", it.get("element_id"), f"science-looking text {it['text']!r} not traceable to a fixture field", "#12")
    else:
        lines = [norm(it["text"], ocr=True) for it in items]
        for ex in expected:
            want = norm(ex["text"], ocr=True)
            if not any(want in ln for ln in lines):
                add("major", ex["element_id"], f"OCR did not find {ex['text']!r}: verify the frame by eye (OCR is weak evidence)", "#12")
    for it in items:
        if it.get("missing_glyphs"):
            add("critical", it.get("element_id"), f"missing glyphs (tofu): {it['missing_glyphs']}", "#55")
    for sp in rendered.get("spans", []):
        for p in cluster_breaks(sp["parts"]):
            add("major", sp["element_id"], p + "; animate per word or grapheme cluster", "#55")
        whole = next((ex["text"] for ex in expected if ex["element_id"] == sp["element_id"]), None)
        if whole is not None and "".join(norm("".join(sp["parts"])).split()) != "".join(norm(whole).split()):
            add("major", sp["element_id"], "animated parts do not reassemble the approved text", "#55")
    sev = "critical" if any(f["severity"] == "critical" for f in findings) else \
        "major" if findings else "pass"
    return {"mode": "ocr" if ocr else "dom", "findings": findings, "severity": sev}


def selftest():
    exp = [{"element_id": "n_glass", "text": "n = 1.50", "source": "fixture:refr-01#n_glass", "science": True},
           {"element_id": "unit", "text": "v = 2.0 × 10⁸ m/s", "source": "fixture:refr-01#v", "science": True},
           {"element_id": "title", "text": "Why does light bend?", "source": "approved_script:seg-01", "science": False},
           {"element_id": "hi_title", "text": "प्रकाश क्यों मुड़ता है?", "source": "approved_script:seg-01-hi", "science": False}]
    ok = {"mode": "dom", "items": [{"element_id": "n_glass", "text": "n  =  1.50"},
                                   {"element_id": "unit", "text": "v = 2.0 × 10⁸ m/s"},
                                   {"element_id": "title", "text": "Why does light bend?"},
                                   {"element_id": "hi_title", "text": "प्रकाश क्यों मुड़ता है?"}],
          "spans": [{"element_id": "hi_title", "parts": ["प्रकाश", "क्यों", "मुड़ता", "है?"]}]}
    assert diff(exp, ok)["severity"] == "pass", diff(exp, ok)
    bad = json.loads(json.dumps(ok))
    bad["items"][0]["text"] = "n = 1.05"
    bad["items"].pop(1)
    bad["items"].append({"element_id": "decor7", "text": "c = 3 × 10⁸ m/s"})
    r = diff(exp, bad)
    sev = {(f["element"], f["severity"]) for f in r["findings"]}
    assert ("n_glass", "critical") in sev and ("unit", "critical") in sev and ("decor7", "critical") in sev, sev
    minus = [{"element_id": "q", "text": "q = -1.6", "source": "fixture:e#q", "science": True}]
    assert diff(minus, {"mode": "dom", "items": [{"element_id": "q", "text": "q = −1.6"}]})["severity"] == "pass"
    case = [{"element_id": "f", "text": "CO", "source": "fixture:c#f", "science": True}]
    assert diff(case, {"mode": "dom", "items": [{"element_id": "f", "text": "Co"}]})["severity"] == "critical"
    o = diff([{"element_id": "w", "text": "H₂O", "source": "fixture:w#f", "science": True}],
             {"mode": "ocr", "items": [{"text": "Water H2O boils"}]})
    assert o["severity"] == "pass", o
    split = {"mode": "dom", "items": ok["items"], "spans": [{"element_id": "hi_title", "parts": ["प्रक", "ाश", "क्", "यों मुड़ता है?"]}]}
    msgs = [f["message"] for f in diff(exp, split)["findings"]]
    assert any("combining mark" in m for m in msgs) and any("virama" in m for m in msgs), msgs
    assert not any("reassemble" in m for m in msgs), msgs
    lost = {"mode": "dom", "items": ok["items"], "spans": [{"element_id": "hi_title", "parts": ["प्रकाश", "क्यों"]}]}
    assert any("reassemble" in f["message"] for f in diff(exp, lost)["findings"])
    tofu = {"mode": "dom", "items": [dict(ok["items"][3], missing_glyphs=["U+0981"])] + ok["items"][:3]}
    assert diff(exp, tofu)["severity"] == "critical"
    print("text_fixture_diff selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--expected")
    ap.add_argument("--rendered")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.expected or not a.rendered:
        ap.print_usage(sys.stderr)
        return 2
    try:
        rep = diff(json.load(open(a.expected, encoding="utf-8")), json.load(open(a.rendered, encoding="utf-8")))
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(rep, f, indent=2, ensure_ascii=False)
    print(json.dumps(rep, indent=2, ensure_ascii=False))
    return 0 if rep["severity"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
