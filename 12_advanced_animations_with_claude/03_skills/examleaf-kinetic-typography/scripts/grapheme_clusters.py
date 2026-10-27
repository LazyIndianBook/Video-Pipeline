#!/usr/bin/env python3
"""grapheme_clusters.py - split Devanagari / Bengali-Assamese text into animation units (stdlib only).

Usage:
  python3 grapheme_clusters.py --text "क्षत्रिय नमस्कार"            # clusters per word (JSON)
  python3 grapheme_clusters.py --plan CUE_SHEET.json [--mode cluster|word] [--lead 0.05] [--stagger 0.045]
                               [--entrance 0.35] [--exit-at SECONDS] [--hold-min 1.2] [--indic-multiplier 1.5]
  python3 grapheme_clusters.py --selftest

Rule (#55): animate Indic text per word or per grapheme cluster, never per code point.

LIMITS vs full UAX #29 (Unicode Standard Annex #29, "Unicode Text Segmentation") - verify against the current annex:
  * Implemented: base + Extend (Mn/Me) + SpacingMark (Mc) + ZWJ/ZWNJ attach to the previous cluster (GB9, GB9a);
    Indic conjuncts consonant + virama [+ ZWJ] + consonant stay together, approximating GB9c (Unicode 15.1+)
    for Devanagari and Bengali only, using hard-coded consonant ranges (approximate InCB=Consonant) and
    "combining class 9" as the linker. ZWNJ after a virama ends the conjunct (InCB=Extend excludes ZWNJ).
  * Not implemented: CR/LF and control rules, Hangul syllables, regional-indicator pairs, emoji ZWJ sequences
    (Extended_Pictographic), Prepend, other Indic scripts' InCB data, and Unicode-version differences in Python's
    unicodedata tables (reported as unicode_version).
  * In the browser, prefer Intl.Segmenter(lang, {granularity: 'grapheme'}); whether its ICU build implements GB9c
    conjunct clusters depends on the Chrome version - compare its output with this helper on the glyph test sheet.
Exit: 0 ok, 1 failed check or refused mode, 2 usage/IO error.
"""
import argparse, json, sys, unicodedata

ZWJ, ZWNJ = "‍", "‌"
CONSONANT_RANGES = [  # approximate InCB=Consonant (UAX #29, Unicode 15.1+); verify against DerivedCoreProperties.txt
    (0x0915, 0x0939), (0x0958, 0x095F), (0x0978, 0x097F),                     # Devanagari
    (0x0995, 0x09A8), (0x09AA, 0x09B0), (0x09B2, 0x09B2), (0x09B6, 0x09B9),     # Bengali-Assamese
    (0x09DC, 0x09DD), (0x09DF, 0x09DF), (0x09F0, 0x09F1),                       # incl. Assamese RA/WA
]
INDIC_BLOCKS = [(0x0900, 0x097F), (0x0980, 0x09FF)]


def is_consonant(ch):
    o = ord(ch)
    return any(a <= o <= b for a, b in CONSONANT_RANGES)


def is_indic(text):
    return any(a <= ord(c) <= b for c in text for a, b in INDIC_BLOCKS)


def is_linker(ch):
    return unicodedata.combining(ch) == 9 and is_indic(ch)       # virama / hasanta


def clusters(text):
    out = []
    for ch in text:
        if not out:
            out.append(ch)
            continue
        cur = out[-1]
        cat = unicodedata.category(ch)
        attach = cat in ("Mn", "Mc", "Me") or ch in (ZWJ, ZWNJ)
        if not attach and is_consonant(ch):
            tail = cur[:-1] if cur.endswith(ZWJ) else cur
            attach = len(tail) > 0 and is_linker(tail[-1]) and not cur.endswith(ZWNJ)
        if attach and not ch.isspace():
            out[-1] = cur + ch
        else:
            out.append(ch)
    return out


def words_with_clusters(text):
    return [{"word": w, "clusters": clusters(w), "codepoints": len(w),
             "per_codepoint_would_split": len(w) != len(clusters(w))} for w in text.split()]


def plan(sheet, mode="cluster", lead=0.05, stagger=0.045, entrance=0.35, exit_at=None,
         hold_min=1.2, indic_multiplier=None):
    if mode not in ("cluster", "word"):
        raise ValueError("mode must be 'cluster' or 'word' (never per code point, #55)")
    lang = sheet.get("language", "")
    units, warnings = [], []
    for wi, w in enumerate(sheet.get("words", [])):
        text, t0, t1 = w["w"], float(w["t0"]), float(w["t1"])
        start = max(0.0, t0 - lead)                     # reveal on, or ~0.05 s before, its word [V4-MP]
        parts = [text] if mode == "word" else clusters(text)
        step = stagger if len(parts) < 2 else min(stagger, max(0.0, (t1 - start)) / (len(parts) - 1))
        for ui, p in enumerate(parts):
            units.append({"word_index": wi, "unit_index": ui, "text": p, "at": round(start + ui * step, 4),
                          "lang": w.get("lang", lang)})
    indic = any(is_indic(u["text"]) for u in units)     # script of the shown text, not the sheet language
    need = hold_min
    if indic:
        if not isinstance(indic_multiplier, (int, float)) or indic_multiplier <= 1.0:
            warnings.append("Indic text: indic_multiplier not set (>1.0 required); hold check uses hold_min only")
        else:
            need = hold_min * indic_multiplier
    visible = (max(u["at"] for u in units) + entrance) if units else 0.0
    hold = None if exit_at is None else round(exit_at - visible, 4)
    if hold is not None and hold < need - 1e-9:
        warnings.append(f"hold {hold:.2f} s < required {need:.2f} s (#50) - delay the exit or shorten the line")
    return {"mode": mode, "language": lang, "units": units, "fully_visible_at": round(visible, 4),
            "exit_at": exit_at, "hold_s": hold, "required_hold_s": round(need, 4), "warnings": warnings,
            "unicode_version": unicodedata.unidata_version}


def selftest():
    cases = {
        "क्षत्रिय": ["क्ष", "त्रि", "य"],
        "हिन्दी": ["हि", "न्दी"],
        "प्रकाश": ["प्र", "का", "श"],
        "ज्ञान": ["ज्ञा", "न"],
        "धर्म": ["ध", "र्म"],
        "हैं": ["हैं"],
        "मुड़ता": ["मु", "ड़", "ता"],
        "অসমীয়া": ["অ", "স", "মী", "য়া"],                      # decomposed YA + NUKTA
        "অসমীয়া": ["অ", "স", "মী", "য়া"],   # precomposed YYA
        "নমস্কাৰ": ["ন", "ম", "স্কা", "ৰ"],
        "ক্ষ": ["ক্ষ"],
        "ৱাৰ্তা": ["ৱা", "ৰ্তা"],
        "क्‌ष": ["क्‌", "ष"],                          # ZWNJ breaks the conjunct
        "क्‍ष": ["क्‍ष"],                              # ZWJ keeps it
        "éte": ["é", "t", "e"],
    }
    fails = []
    for text, want in cases.items():
        got = clusters(text)
        if got != want:
            fails.append({"text": text, "want": want, "got": got})
    sheet = {"language": "hi-IN", "words": [{"w": "इसे", "t0": 5.4, "t1": 5.65},
                                            {"w": "refraction", "t0": 5.7, "t1": 6.3, "lang": "en-IN"},
                                            {"w": "कहते", "t0": 6.35, "t1": 6.62}]}
    p = plan(sheet, "cluster", exit_at=7.4, indic_multiplier=1.5)
    first = p["units"][0]
    if first["at"] != 5.35 or first["text"] != "इ":
        fails.append({"plan_first": first})
    if not any(u["text"] == "refraction"[0] for u in p["units"]):   # Latin splits per letter-cluster
        fails.append({"plan_latin": "missing"})
    if not any("hold" in x for x in p["warnings"]):                 # 7.4 - (6.30+0.35) < 1.8 required
        fails.append({"plan_hold_warning": p["warnings"]})
    pw = plan(sheet, "word", exit_at=9.0, indic_multiplier=1.5)
    if [u["text"] for u in pw["units"]] != ["इसे", "refraction", "कहते"] or pw["warnings"]:
        fails.append({"plan_word": pw})
    latin = plan({"language": "hi-IN", "words": [{"w": "refraction", "t0": 5.7, "t1": 6.3}]}, "word",
                 exit_at=7.4, indic_multiplier=1.5)
    if latin["required_hold_s"] != 1.2 or latin["warnings"]:           # Latin label in a Hindi lesson
        fails.append({"plan_latin_label": latin})
    try:
        plan(sheet, "codepoint")
        fails.append({"codepoint_mode": "not refused"})
    except ValueError:
        pass
    wc = words_with_clusters("क्षत्रिय नमस्कार")
    if not (wc[0]["codepoints"] == 8 and len(wc[0]["clusters"]) == 3 and wc[0]["per_codepoint_would_split"]):
        fails.append({"words_with_clusters": wc})
    print(json.dumps({"selftest": "pass" if not fails else "fail", "script": "grapheme_clusters.py",
                      "cases": len(cases), "unicode_version": unicodedata.unidata_version,
                      "failures": fails}, ensure_ascii=False))
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Grapheme clusters / animation plan for Indic text")
    ap.add_argument("--text"); ap.add_argument("--plan")
    ap.add_argument("--mode", default="cluster"); ap.add_argument("--lead", type=float, default=0.05)
    ap.add_argument("--stagger", type=float, default=0.045); ap.add_argument("--entrance", type=float, default=0.35)
    ap.add_argument("--exit-at", type=float); ap.add_argument("--hold-min", type=float, default=1.2)
    ap.add_argument("--indic-multiplier", type=float)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.text is not None:
        print(json.dumps({"words": words_with_clusters(a.text), "unicode_version": unicodedata.unidata_version},
                         ensure_ascii=False, indent=2))
        return 0
    if a.plan:
        try:
            sheet = json.load(open(a.plan, encoding="utf-8"))
            res = plan(sheet, a.mode, a.lead, a.stagger, a.entrance, a.exit_at, a.hold_min, a.indic_multiplier)
        except ValueError as e:
            print(json.dumps({"status": "refused", "error": str(e)}))
            return 1
        except OSError as e:
            print(json.dumps({"status": "error", "error": str(e)}))
            return 2
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    ap.error("one of --text, --plan, --selftest is required")


if __name__ == "__main__":
    sys.exit(main())
