#!/usr/bin/env python3
"""check_pd_script.py <script.json> [...]: Professor Diki script checks that 16/tooling/check_script.py (v2) does not run.

Run check_script.py first (schema, slot order, PD-01 pause ranges, energy 1-5, verbs, insight <= 10 s, words, duration,
silence, outro, disclosure). This adds framework §8: banned phrases (SQ-30), sentence length (SQ-38), terms before use
(SQ-26), structural answerability and hidden answer (SQ-25, SQ-04), confront evidence (SQ-23), payoff placement and
conditional feedback (SQ-27, SQ-05), payoff sentence (SQ-33), energy shape (SQ-28), re-hooks every <= 12 s (SQ-35),\nclose and follow line (SQ-37, SQ-43), scroll test and five hooks (SQ-39, SQ-40), hook timing (SQ-41), quotable line (SQ-42).
Timing comes from pilotlib.plan (one estimator for the whole pipeline). Stdlib only. Exit 1 on problems.
"""
import json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
TOOLING = pathlib.Path(os.environ.get("PILOT_TOOLING", HERE.parents[3] / "16_pilot_builds_2026-10-16" / "tooling"))
sys.path.insert(0, str(TOOLING))
import pilotlib as L  # noqa: E402

TASK_PAUSE = {"recall": "think_recall", "binary": "think_recall", "count": "think_recall",
              "choose": "think_choice", "calc": "think_calc", "multi": "pause_video"}


REHOOK_SLOTS = {"hook.question_reveal", "check.predict", "reveal.answer", "misconception.confront", "check.transfer", "explain.mechanism", "explain.condition", "worked.step",
                "feedback.transfer", "close.next_step"}


def sentences(t): return [x for x in re.split(r"(?<=[.?!])\s+", t.strip()) if x]


def banned():
    for line in (HERE.parent / "references" / "banned_phrases.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            lvl, bid, rx, fix = line.split("\t")
            yield lvl, bid, re.compile(rx, re.I), fix


def check(path):
    s = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    s_fmt = s.get("format")
    beats = s["beats"]; ids = [b["id"] for b in beats]; slots = [b["slot"] for b in beats]
    rows, total = L.plan(s); start = {r["id"]: r["start"] for r in rows}
    P, W, seen = [], [], set()
    rules = list(banned())
    for i, b in enumerate(beats):
        bid, text = b["id"], b["text"]
        fx = set((b.get("on_screen") or {}).get("fx_refs", []))
        sens = sentences(text)
        for sen in sens:
            n = len(L.words_of(sen))
            if n > 18: P.append(f"{bid}: {n}-word sentence > 18 (SQ-38): '{sen}'")
            for lvl, rid, rx, fix in rules:
                if rx.search(sen): (P if lvl == "block" else W).append(f"{bid}: {rid} in '{sen}' -> {fix}")
        if b["slot"] in ("check.predict", "check.transfer"):
            ck = b.get("check") or {}
            if text.count("?") != 1: P.append(f"{bid}: one question per check (A1-02)")
            want = TASK_PAUSE.get(ck.get("task_kind"))
            if L.beat_pause(b)[0] != want: P.append(f"{bid}: task_kind {ck.get('task_kind')} needs pause {want} (PD-01)")
            miss = [f for f in ck.get("answerable_from", []) if f not in seen | fx]
            if not ck.get("answerable_from") or miss: P.append(f"{bid}: givens not shown before the question {miss} (SQ-25)")
            if ck.get("asks") in seen | fx: P.append(f"{bid}: answer {ck.get('asks')} already on screen (SQ-04)")
            nxt = beats[i + 1] if i + 1 < len(beats) else {}
            if ck.get("asks") not in (nxt.get("on_screen") or {}).get("fx_refs", []):
                P.append(f"{bid}: the next beat must show {ck.get('asks')} (payoff right after the window, A3-M4)")
        if b["slot"] == "misconception.confront" and not b.get("evidence"):
            P.append(f"{bid}: confront needs evidence: a fixture value or a sourced observation (SQ-23)")
        if b["slot"] == "reveal.answer" and len(L.words_of(sens[0])) > 8:
            P.append(f"{bid}: payoff sentence > 8 words (SQ-33)")
        seen |= fx
    if "reveal.answer" in slots and slots[slots.index("reveal.answer") - 1] != "check.predict":
        P.append("reveal.answer must directly follow check.predict (SQ-33)")
    pb = [b for b in beats if b.get("payoff_beat")]
    payoff_slots = ("explain.mechanism", "worked.step") if s_fmt == "explainer_60" else ("reveal.answer",)
    if len(pb) != 1 or pb[0]["slot"] not in payoff_slots:
        P.append(f"exactly one payoff_beat: true, on one of {', '.join(payoff_slots)} (insight_beat marks the first usable idea)")
    ib = [b for b in beats if b.get("insight_beat")]
    if ib and ib[0].get("payoff_beat"): P.append("insight_beat and payoff_beat are different beats")
    if "feedback.transfer" in slots:
        rt = beats[slots.index("feedback.transfer")]; pos = start[rt["id"]] / total
        if not 0.70 <= pos <= 0.90: P.append(f"transfer answer at {pos:.0%} of runtime; needs 70-90 % (SQ-27)")
        if "if you" not in rt["text"].casefold(): P.append("feedback.transfer needs a conditional 'If you ...' line (SQ-05)")
    en = [L.energy_level(b) or 0 for b in beats]
    if en and en[0] < 4: P.append("hook energy must be >= 4 (SQ-28)")
    if "reveal.answer" in slots and en[slots.index("reveal.answer")] != max(en):
        P.append("the predict payoff carries the peak energy (SQ-28)")
    if "check.transfer" in slots and min(en[slots.index("check.transfer"):]) < 3:
        P.append("nothing after the transfer below energy 3; never end at the lowest point (SQ-28)")
    # register (PD-27): talk, don't caption. Fragments, colon fragments, jargon-first terms and hard words warn.
    if s_fmt == "explainer_60":
        import re as _re2
        VERBS = _re2.compile(r"\b(is|are|was|were|be|has|have|do|does|did|can|will|say|says|call|called|pass|passes|push|pushes|flow|flows|count|counts|measure|measures|hold|holds|give|gives|get|gets|go|goes|stay|stays|read|reads|double|doubles|halve|halves|bend|bends|work|works|need|needs|keep|keeps|plot|see|try|let|make|makes|change|changes|means|equals|divided|times|try|remember|watch)\b", _re2.I)
        brand = (beats[-1]["text"].strip() if beats else ""); claim = str(s.get("claim_line") or "").strip()
        for b in beats:
            for sen in sentences(b["text"]):
                w = L.words_of(sen)
                if sen.strip() in (brand, claim) or sen.strip().endswith("?"): continue
                if len(w) < 4: W.append(f"{b['id']}: fragment {sen.strip()!r} (PD-27: full sentences, not captions)")
                elif not VERBS.search(sen): W.append(f"{b['id']}: no verb in {sen.strip()!r} (PD-27)")
                if ":" in sen and len(L.words_of(sen.split(":", 1)[1])) <= 3: W.append(f"{b['id']}: colon fragment {sen.strip()!r} (PD-27)")
        text_all = " ".join(b["text"] for b in beats); words_all = L.words_of(text_all)
        if words_all:
            avg = sum(len(x) for x in words_all) / len(words_all); longw = sum(1 for x in words_all if sum(1 for ch in x.lower() if ch in "aeiouy") >= 3 and len(x) >= 8) / len(words_all)
            if avg > 4.9 or longw > 0.12: W.append(f"PD-27: hard words (average {avg:.1f} letters, {longw:.0%} long words); write for a small child")
        for term in ("voltage", "current", "resistance"):
            first = next((sen for b in beats for sen in sentences(b["text"]) if _re2.search(r"\b" + term + r"\b", sen, _re2.I)), None)
            if first and not _re2.search(r"\b(called|call|is|means|that is)\b", first, _re2.I): W.append(f"PD-27: {term!r} is first spoken in {first.strip()!r} without being introduced in a full sentence")
    # the 60-second method (PD-26, 11_SIXTY_SECOND_EXPLAINER_METHOD.md): M01 outcome, M02 promise first, M05 explicit links
    if s_fmt == "explainer_60":
        import re as _re
        if not str(s.get("outcome", "")).strip(): W.append("M01: no `outcome` (one observable outcome the viewer can do afterwards)")
        hook_txt = beats[0]["text"] if beats else ""; first_sentence = _re.split(r"(?<=[.?!])\s+", hook_txt.strip())[0] if hook_txt else ""
        pl = str(s.get("promise_line", "")).strip()
        if not pl: W.append("M02: no `promise_line` (the first sentence: topic plus the viewer's task)")
        elif pl.rstrip(".?!").lower() != first_sentence.rstrip(".?!").lower(): W.append(f"M02: promise_line differs from the hook's first sentence ({first_sentence!r})")
        if not _re.search(r"\b(read|calculate|predict|find|see|explain|measure|work out|count|watch|tell|know)\b", hook_txt, _re.I): W.append("M02: the hook gives no task verb (read / calculate / predict / explain / see …)")
        links = sum(1 for b in beats[1:] if _re.search(r"\b(because|so|now|apply|double|keep|change|watch|for this|across|then|same)\b", b["text"], _re.I))
        if links < 3: W.append(f"M05: only {links} beats carry a link word (because / so / keep / change / watch …); the viewer must not invent the connections")
    # creator flow (founder steer 16 Oct 2026): scroll test, five hooks, hook timing, re-hooks, quotable line, close
    a = s.get("artefacts") or {}
    if len(str(a.get("scroll_test", "")).split()) < 6: P.append("artefacts.scroll_test sentence missing (SQ-39)")
    hooks = a.get("hooks", [])
    if len({h.get("kind") for h in hooks}) < 5 or [h.get("chosen") for h in hooks].count(True) != 1 \
            or not all(h.get("honest") for h in hooks if h.get("chosen")):
        P.append("five structurally different hooks, exactly one chosen, and it passes the honesty test (SQ-40)")
    if not s.get("board_at_start"): P.append("the hook's complete picture must be on the board at frame 0 (SQ-41)")
    h = rows[0]; hw = L.words_of(beats[0]["text"].split("?")[0] + "?") if "?" in beats[0]["text"] else []
    q_end = h["start"] + len(hw) * 60.0 / h["wpm"] if hw else 99
    if q_end > 3.0: P.append(f"hook question ends at {q_end:.1f} s; needs <= 3.0 s (SQ-41)")
    # re-hook events: a `rehook` tag, an anchor slot, or a spoken question (same rule as check_script REHOOK_SLOTS)
    end_rt = start[beats[slots.index("feedback.transfer")]["id"]] if "feedback.transfer" in slots else total
    rh = sorted(start[b["id"]] for b in beats if (b.get("rehook") or b["slot"] in REHOOK_SLOTS or "?" in b["text"])
                and start[b["id"]] <= end_rt)
    gaps = [y - x for x, y in zip(rh, rh[1:])]
    if len(rh) < 2 or max(gaps) > 12: P.append(f"re-hook gap {max(gaps) if gaps else total:.1f} s > 12 s (SQ-35)")
    cl = [(b, b["on_screen"]["claim_line"]) for b in beats if (b.get("on_screen") or {}).get("claim_line")]
    if len(cl) != 1 or cl[0][1] not in cl[0][0]["text"] or len(L.words_of(cl[0][1])) > 9:
        P.append("one on_screen.claim_line: the quotable line, <= 9 words, spoken verbatim in its beat (SQ-42)")
    for b in beats:
        if b["slot"] != "close.next_step" and re.search(r"\bfollow\b", b["text"], re.I):
            P.append(f"{b['id']}: the follow invitation belongs only in close.next_step (SQ-43)")
    # PD-14: spoken close is exactly "Try the free lesson on <topic>." then "Professor Diki Simplified.";
    # an optional "next one" tease (<= 12 words, may carry the light follow line) comes before them
    closes = [b for b in beats if b["slot"] == "close.next_step"]
    last_close = closes[-1]["text"].strip() if closes else ""
    m = re.fullmatch(r"Try the free lesson on ([^.?!]+)\.", last_close)
    cta = str(s.get("cta_line") or "").strip()
    custom_ok = bool(cta) and last_close == cta and re.search(r"\bfree lesson\b", cta, re.I) is not None   # PD-14 + M11: the script's own free-lesson invitation
    if not (m or custom_ok) or slots[-2:] != ["close.next_step", "outro.brand"]:
        P.append("PD-14: the close is the script's cta_line (a free-lesson invitation) or 'Try the free lesson on <topic>.', then 'Professor Diki Simplified.'")
    else:
        card = (beats[-1].get("on_screen") or {}).get("free_lesson", "")
        topic = m.group(1) if m else None
        if topic is not None and card.casefold() != f"free lesson: {topic}".casefold():
            P.append(f"end card '{card}' must read 'Free lesson: {topic}' (PD-14)")
        elif topic is None and not card.casefold().startswith("free lesson: "):
            P.append(f"end card '{card}' must read 'Free lesson: <topic>' (PD-14)")
    for b in closes[:-1]:
        if len(L.words_of(b["text"])) > 12 or not re.search(r"\bnext\b", b["text"], re.I):
            P.append(f"{b['id']}: the tease is a light 'next one' line of <= 12 words (SQ-37, SQ-43)")
    short = [len(L.words_of(x)) <= 14 for b in beats for x in sentences(b["text"])]
    if short and sum(short) / len(short) < 0.8: P.append("fewer than 80 % of sentences <= 14 words (SQ-38)")
    for t in s.get("terms", []):
        first = next((j for j, b in enumerate(beats) if re.search(rf"\b{re.escape(t['term'])}", b["text"], re.I)), None)
        if first is None: P.append(f"term '{t['term']}' never spoken"); continue
        shown = {c.get("element_id") for b in beats[:first + 1] for c in b.get("cues", [])} | set(s.get("board_at_start", []))
        if t.get("shown_by") not in shown: P.append(f"term '{t['term']}' not shown by its first use (SQ-26)")
        if t.get("meaning_beat") not in ids or ids.index(t["meaning_beat"]) > first + 1:
            P.append(f"term '{t['term']}': plain meaning later than the next beat (SQ-26)")
    words = sum(len(L.words_of(b["text"])) for b in beats)
    print(f"{path}\n  words {words} | plan {total:.1f} s | silence {L.silence_share(s):.1%} | "
          f"max re-hook gap {max(gaps) if gaps else 0:.1f} s | hook question ends {q_end:.1f} s")
    for r, b in zip(rows, beats):
        rk = (b.get("rehook") or {}).get("kind", "")
        print(f"    {r['id']:>4} {r['start']:5.1f}s {b.get('energy')!s:<4} {r['purpose']:<12} {rk:<10} {b['slot']:<22} {b['text']}")
    for label, xs in (("PROBLEMS", P), ("WARNINGS", W)):
        if xs: print(f"  {label}:"); [print("   -", x) for x in xs]
    print("  OK" if not P else "  FAIL")
    return not P


if __name__ == "__main__":
    sys.exit(0 if all([check(p) for p in sys.argv[1:]]) else 1)
