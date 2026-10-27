#!/usr/bin/env python3
"""check_script.py <script.json>: pilot-contract checks (§3). Prints OK or a list of problems; exit 1 on problems.
Warnings never fail. v1 scripts (no script_version) are checked as before; "ExamLeaf" and think_window_s only warn there.
v2 scripts (`"script_version": 2`, format concept_short_60; fields in 17_professor_diki_simplified/format/
script_v2_fields.md) are checked for: slot order (V2_SLOTS, repeats allowed), labelled pauses inside the PD-01 ranges,
energy 1-5 with >= 3 distinct marks and the peak on a reveal or the transfer, visual_op from the motion verbs, exactly one
insight_beat starting <= 10 s, 120-135 spoken words, the planned duration inside target_duration_s +- duration_tolerance_s,
planned silence share <= 15 %, an answerable prediction (every number in the predict question was spoken or shown, via
on_screen.fx_refs, in an earlier beat), check.transfer with a think window and a reveal.transfer after it, the close
(PD-14) "<cta_line>" then "Professor Diki Simplified." (one or two beats); no disclosure on screen or spoken (PD-20), no "ExamLeaf", one claim plus its condition (warn), a re-hook every <= 12 s and one claim_line (warn)."""
import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L

BUDGET = 1000
WORDS_60 = (120, 135)          # PD-07 spoken words for concept_short_60
INSIGHT_BY_S = 10.0
SILENCE_MAX = 0.15
NUM_WORDS = {w: i for i, w in enumerate("zero _ two three four five six seven eight nine ten eleven twelve thirteen fourteen "
             "fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUM_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100})
NUM_WORDS.pop("_")   # ponytail: "one" is skipped (pronoun in "which one"); digits and word forms only, no "half"/"double"


def number_tokens(text):
    """Number tokens of a text as normalised strings: digit runs and number words ("zero point two" -> zero, two)."""
    out = set()
    for w in L.words_of(text):
        n = L.norm_word(w)
        if n in NUM_WORDS:
            out.add(n)
        out.update(re.findall(r"\d+", w))
    return out


def shown_tokens(fixture, ref):
    """Number tokens a fixture path shows on screen: the digits of every numeric or string leaf plus small-int words."""
    v = fixture
    for k in ref.split("."):
        v = v.get(k) if isinstance(v, dict) else None
    leaves, out = [v], set()
    while leaves:
        x = leaves.pop()
        if isinstance(x, dict):
            leaves.extend(x.values())
        elif isinstance(x, list):
            leaves.extend(x)
        elif isinstance(x, (int, float, str)) and not isinstance(x, bool):
            for dg in re.findall(r"\d+", str(x)):
                out.add(dg)
                out.update(w for w, i in NUM_WORDS.items() if i == int(dg))
    return out


def question_of(text):
    qs = re.findall(r"[^.?!:;]*\?", text)
    return " ".join(qs) if qs else text


TASK_PAUSE = {"recall": "think_recall", "binary": "think_recall", "count": "think_recall", "choose": "think_choice",
              "calc": "think_calc", "multi": "pause_video"}       # check.task_kind -> pause purpose (PD-01)


REHOOK_SLOTS = {"hook.question_reveal", "check.predict", "reveal.answer", "misconception.confront", "check.transfer", "explain.mechanism", "explain.condition", "worked.step",
                "feedback.transfer", "close.next_step"}
REHOOK_MAX_S = 12.0


def check_v2(s, d, problems, warns):
    beats = s.get("beats", []); slots = [b["slot"] for b in beats]; fx = load_fixture(d)
    if s.get("format") == "concept_short_60" and float(s.get("target_duration_s", 0)) != 60:
        problems.append("concept_short_60 needs target_duration_s 60")
    if "duration_tolerance_s" not in s:
        warns.append("no duration_tolerance_s; using 1.0 s")
    if len(s.get("scenes", [])) != 1:
        problems.append(f"one persistent scene per short (PD-03); found {len(s.get('scenes', []))}")
    for i, b in enumerate(beats):
        last = i == len(beats) - 1
        if b["slot"] not in L.V2_SLOTS:
            problems.append(f"{b['id']}: unknown v2 slot {b['slot']}")
        if b.get("tag") in L.CANDIDATE_TAGS:
            warns.append(f"{b['id']}: tag {b['tag']} is a candidate, not admitted until the voice audition measures it")
        elif b.get("tag") and b["tag"] not in L.ALLOWED_TAGS:
            problems.append(f"{b['id']}: tag {b['tag']} not allowed")
        if L.energy_level(b) is None:
            problems.append(f"{b['id']}: energy must be an integer 1-5 (or low/mid/high/peak)")
        ops = b.get("visual_op"); ops = [ops] if isinstance(ops, str) else (ops or [])
        if not ops or any(o not in L.VISUAL_OPS for o in ops):
            problems.append(f"{b['id']}: visual_op {b.get('visual_op')} not a motion verb {sorted(L.VISUAL_OPS)}")
        if L.BANNED_RE.search(b["text"] + " " + json.dumps(b.get("on_screen") or {}, ensure_ascii=False)):
            problems.append(f"{b['id']}: banned brand string (ExamLeaf) in spoken or on-screen text")
        if re.search(r"ai[- ]generated|voice converted", b["text"], re.I):
            problems.append(f"{b['id']}: disclosure is spoken; it belongs on screen only (PD-02)")
        p = b.get("pauses"); p = [p] if isinstance(p, dict) else (p or [])
        if any(x.get("at", "end") != "end" for x in p):
            problems.append(f"{b['id']}: only end-of-beat pauses are placed (at: end); split the beat at the pause")
        if len(p) > 1:
            problems.append(f"{b['id']}: one pause per beat (the gap after its last word)")
        if p:
            purpose = L.PAUSE_ALIAS.get(p[0].get("purpose"), p[0].get("purpose"))
            if purpose not in L.PAUSE_S:
                problems.append(f"{b['id']}: pause purpose {p[0].get('purpose')} not in {sorted(L.PAUSE_S)}")
            else:
                lo, hi = L.PAUSE_RANGE[purpose]; sec = L.beat_pause(b)[1]
                if not lo - 1e-9 <= sec <= hi + 1e-9:
                    problems.append(f"{b['id']}: {purpose} pause {sec} s outside PD-01 {lo}-{hi} s")
        elif float(b.get("think_window_s", 0)) > 0:
            warns.append(f"{b['id']}: think_window_s is v1; read as think_calc {L.beat_pause(b)[1]} s; write pauses [{{purpose, after_s}}]")
        elif not last:
            problems.append(f"{b['id']}: no pauses entry; every gap carries a purpose (PD-01)")
        if last and L.beat_pause(b)[1] > 0:
            warns.append(f"{b['id']}: pause after the last beat is ignored (the end card and motif follow)")
        if b["slot"] in ("check.predict", "check.transfer"):
            purpose = L.beat_pause(b)[0]
            if not purpose.startswith("think_") and purpose != "pause_video":
                problems.append(f"{b['id']}: {b['slot']} needs a think_* pause (its own window)")
            want = TASK_PAUSE.get((b.get("check") or {}).get("task_kind"))
            if want and want != purpose:
                problems.append(f"{b['id']}: task_kind {b['check']['task_kind']} needs pause {want}, not {purpose} (PD-01)")
    if L.BANNED_RE.search(" ".join(str(s.get(k, "")) for k in ("video_id", "topic", "title")) + json.dumps(s.get("outro") or {})):
        problems.append("banned brand string (ExamLeaf) in video_id/topic/title/outro")
    anch = L.anchors_for(s)
    if s.get("format") == "explainer_60":
        problems += L.spine_problems(s)                       # PD-26: functions, not a fixed order
        anch = []
    firsts = [slots.index(x) for x in anch if x in slots]
    if firsts != sorted(firsts):
        problems.append("slots out of format order: " + " → ".join(anch))
    if s.get("format") == "explainer_60":
        for b in beats:
            for pz in (b.get("pauses") or []):
                if str(pz.get("purpose", "")).startswith("think") or pz.get("purpose") == "pause_video":
                    problems.append(f"{b['id']}: explainer_60 has no think or pause_video pauses (PD-24)")
    for req in anch:
        if req not in slots:
            problems.append(f"missing slot {req}")
    ev = {b.get("evidence") for b in beats}
    clm = {n for b in beats for n in b.get("node_ids", []) if n.startswith("CLM-")} - ev
    if s.get("format") in L.SHORT_FORMATS and len(clm) > 2:
        warns.append(f"PD-14 scope is one claim plus its condition; {len(clm)} CLM nodes outside confront evidence: {sorted(clm)}")
    if "misconception.confront" not in slots:
        warns.append("no misconception.confront beat: the bounded exception segment is expected (format §2)")
    if slots and slots[0] != "hook.question_reveal":
        problems.append("first beat must be hook.question_reveal")
    # close (PD-14): "<cta_line>" then "Professor Diki Simplified." as the last two spoken sentences (one beat or two);
    # the CTA text is the request's top-level `cta_line` (empty/null = no CTA, e.g. AC0); disclosure only on screen
    if beats and beats[-1]["slot"] == "outro.brand":
        o = beats[-1]; on = o.get("on_screen") or {}
        txt = o["text"].strip(); cta = s.get("cta_line", "missing")
        if not txt.endswith(L.OUTRO_TEXT):
            problems.append(f"{o['id']}: the last spoken sentence must be exactly '{L.OUTRO_TEXT}'")
        head = txt[: -len(L.OUTRO_TEXT)].strip() if txt.endswith(L.OUTRO_TEXT) else txt
        spoken_cta = head or (beats[-2]["text"].strip() if len(beats) > 1 and beats[-2]["slot"] == "close.next_step" else "")
        if cta == "missing":
            warns.append("no top-level cta_line (PD-14: supplied per request); checking the default 'Try the free lesson on <topic>.' shape")
            if not L.CTA_RE.fullmatch(spoken_cta):
                problems.append(f"the sentence before '{L.OUTRO_TEXT}' must be the CTA 'Try the free lesson on <topic>.' (PD-14); got '{spoken_cta}'")
        elif cta:
            if spoken_cta != cta.strip():
                problems.append(f"the sentence before '{L.OUTRO_TEXT}' must be cta_line '{cta}'; got '{spoken_cta}'")
        elif head:
            problems.append(f"{o['id']}: cta_line is empty (no CTA) but the outro speaks '{head}'")
        disc = L.disclosure_of(s, o) or (resolve(fx, "display.ui.disclosure") if "display.ui.disclosure" in on.get("fx_refs", []) else None)
        path = (s.get("voice") or {}).get("path", "B")
        if disc:
            problems.append(f"{o['id']}: on-screen disclosure '{disc}' is retired (PD-20): declare AI narration at upload (platform label + description), never in the lesson")
        for key in ("header", "endcard_line3"):
            if key in (fx.get("display", {}).get("ui", {}) if isinstance(fx, dict) else {}):
                v = str(fx["display"]["ui"][key])
                if any(re.search(pat, v, re.I) for pat in L.DISCLOSURE_RE.values()) or (key == "header" and v.strip()):
                    warns.append(f"fixture display.ui.{key} = '{v}': retired by PD-20/PD-21 (no disclosure line, no persistent header); drop it")
    elif beats:
        problems.append("last beat must be outro.brand")
    # answerable prediction: numbers in the predict question were spoken or shown earlier (heuristic), and every
    # check.answerable_from field was shown earlier or in this beat
    for i, b in enumerate(beats):
        if b["slot"] != "check.predict":
            continue
        known, shown = set(), set()
        for e in beats[:i]:
            known |= number_tokens(e["text"])
            for ref in (e.get("on_screen") or {}).get("fx_refs", []):
                known |= shown_tokens(fx, ref); shown.add(ref)
        missing = number_tokens(question_of(b["text"])) - known
        if missing:
            problems.append(f"{b['id']}: prediction not answerable: {sorted(missing)} not spoken or shown before the question")
        here = set((b.get("on_screen") or {}).get("fx_refs", []))
        gone = [f for f in (b.get("check") or {}).get("answerable_from", []) if f not in shown | here]
        if gone:
            problems.append(f"{b['id']}: check.answerable_from not on screen by the question: {gone}")
    # energy curve (scorecard A21): >= 3 distinct marks, peak on a reveal or the transfer
    marks = [L.energy_level(b) for b in beats if L.energy_level(b)]
    if marks:
        if len(set(marks)) < 3:
            problems.append("energy curve needs >= 3 distinct marks")
        top = max(marks)
        peak_slots = L.PEAK_SLOTS.get(s.get("format"), L.PEAK_SLOTS["concept_short_60"])
        if not any(L.energy_level(b) == top and (b["slot"] in peak_slots or b.get("payoff_beat") is True) for b in beats):
            problems.append(f"energy peak ({top}) must sit on one of {', '.join(peak_slots)}")
    # insight, duration, words, silence, end card
    rows, total = L.plan(s); start = {r["id"]: r["start"] for r in rows}
    ins = [b["id"] for b in beats if b.get("insight_beat")]
    if len(ins) != 1:
        problems.append(f"exactly one insight_beat needed; found {len(ins)}")
    elif start[ins[0]] > INSIGHT_BY_S:
        problems.append(f"{ins[0]}: first usable idea (insight_beat) planned at {start[ins[0]]} s > {INSIGHT_BY_S} s")
    tgt, tol = float(s.get("target_duration_s", 60)), float(s.get("duration_tolerance_s", 1))
    if abs(total - tgt) > tol:
        problems.append(f"planned duration {total} s outside {tgt} ± {tol} s")
    words = sum(len(L.words_of(b["text"])) for b in beats)
    rs = float(((s.get("voice") or {}).get("rate_scale")) or 1.0); lo, hi = round(WORDS_60[0] * rs), round(WORDS_60[1] * rs)   # PD-07 band scaled by the voice calibration
    if s.get("pace") == "fast": lo, hi = 150, 205                                                                         # PD-28: the fast, packed profile (upper bound raised 17 Oct: reference 195-235 wpm over four videos)
    if s.get("format") in L.SHORT_FORMATS and not lo <= words <= hi:
        problems.append(f"spoken words {words} outside {lo}-{hi} (PD-07 120-135 at rate_scale {rs:.2f})")
    sil = L.silence_share(s); sil_max = L.SILENCE_MAX_BY_FORMAT.get(s.get("format"), SILENCE_MAX)
    if s.get("pace") == "fast": sil_max = min(sil_max, 0.08)                                                                 # PD-28
    if sil > sil_max:
        problems.append(f"planned silence share {sil:.1%} > {sil_max:.0%}")
    if beats and beats[-1]["slot"] == "outro.brand":
        card = rows[-1]["end"] - rows[-1]["start"] + L.tail_s(s)
        if card < L.END_CARD_MIN_S:
            problems.append(f"end card on screen {card:.2f} s < {L.END_CARD_MIN_S} s (outro beat + tail)")
    # change density (planned): a beat longer than 3 s needs a change every 3 s
    for r, b in zip(rows, beats):
        dur = r["end"] - r["start"]
        if dur > 3.0 and len(b.get("cues", [])) < int(dur // 3.0):
            warns.append(f"{b['id']}: {dur:.1f} s of speech with {len(b.get('cues', []))} cues; need >= {int(dur // 3.0)} (1 change / 3 s)")
        if b["slot"] != "outro.brand" and not b.get("cues"):
            warns.append(f"{b['id']}: no cue; every spoken line anchors a change on the board")
    # retention (founder steer 16 Oct 2026): a re-hook (question, reveal, turn, transfer) every <= 12 s, one claim line
    hooks = [r["start"] for r, b in zip(rows, beats) if "?" in b["text"] or b.get("rehook") or b["slot"] in REHOOK_SLOTS]
    for x, y in zip(hooks, hooks[1:]):
        if y - x > REHOOK_MAX_S:
            warns.append(f"no re-hook between {x:.1f} s and {y:.1f} s (> {REHOOK_MAX_S:.0f} s): add a question, reversal or turn")
    claims = [b for b in beats if (b.get("on_screen") or {}).get("claim_line")]
    if len(claims) != 1:
        warns.append(f"one on_screen.claim_line (the quotable aha, on screen >= 1.5 s) expected; found {len(claims)}")
    for b in claims:
        spoken = {L.norm_word(w) for w in L.words_of(b["text"])}
        off = [w for w in L.words_of(b["on_screen"]["claim_line"]) if L.norm_word(w) not in spoken]
        if off:
            warns.append(f"{b['id']}: claim_line words not spoken in the beat: {off}")
    if rows and rows[0]["end"] > 3.5:
        warns.append(f"hook question ends at {rows[0]['end']} s; target <= 3.0 s")
    return rows, total, sil


def load_fixture(d):
    p = d / "fixtures" / "fixture.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def resolve(fx, ref):
    v = fx
    for k in ref.split("."):
        v = v.get(k) if isinstance(v, dict) else None
    return v if isinstance(v, str) else None


def main(path):
    s = L.load_script(path); d = pathlib.Path(s["_dir"]); problems = []; warns = []; v2 = L.is_v2(s)
    for k in ("video_id", "subject", "level", "locale", "language", "format", "target_duration_s", "style", "voice", "scenes", "beats"):
        if k not in s:
            problems.append(f"missing top-level field {k}")
    graph_path = d / "lesson_graph.json"
    node_ids = set()
    if graph_path.exists():
        try:
            node_ids = {n["id"] for n in json.loads(graph_path.read_text(encoding="utf-8"))["nodes"]}
        except Exception as e:
            problems.append(f"lesson_graph.json unreadable: {e}")
    else:
        problems.append("lesson_graph.json missing")
    scene_ids = [sc["id"] for sc in s.get("scenes", [])]
    for sc in s.get("scenes", []):
        if not (d / sc["file"]).exists():   # v2: the script is checked before the scene is built (script-first)
            (warns if v2 else problems).append(f"scene file missing: {sc['file']}")
    total = 0; slots = []
    beat_ids = set()
    for b in s.get("beats", []):
        beat_ids.add(b["id"]); total += len(b["text"]); slots.append(b["slot"])
        if b["scene"] not in scene_ids:
            problems.append(f"{b['id']}: scene {b['scene']} not declared")
        if not v2 and b["slot"] not in L.SLOTS:
            problems.append(f"{b['id']}: unknown slot {b['slot']}")
        if L.TAG_RE.search(b["text"]):
            problems.append(f"{b['id']}: tag inside text; use the 'tag' field")
        if not v2 and b.get("tag") and b["tag"] not in L.ALLOWED_TAGS:
            problems.append(f"{b['id']}: tag {b['tag']} not allowed")
        if not v2 and L.BANNED_RE.search(b["text"]):
            warns.append(f"{b['id']}: speaks 'ExamLeaf' (retired brand; v2 fails this)")
        if not v2 and float(b.get("think_window_s", 0)) > 0:
            warns.append(f"{b['id']}: think_window_s {b['think_window_s']} read as think_calc; v2 uses pauses [{{purpose, after_s}}] (PD-01)")
        if b["slot"] not in ("outro.disclosure", "outro.brand"):
            if not b.get("node_ids"):
                problems.append(f"{b['id']}: no node_ids")
            for n in b.get("node_ids", []):
                if node_ids and n not in node_ids:
                    problems.append(f"{b['id']}: node {n} not in lesson_graph.json")
        elif not v2:
            if b["text"].strip() != L.DISCLOSURE:
                problems.append(f"{b['id']}: outro text must be exactly '{L.DISCLOSURE}'")
        if not v2 and b["slot"] == "check.predict" and not (4 <= float(b.get("think_window_s", 0)) <= 6):
            problems.append(f"{b['id']}: check.predict needs think_window_s between 4 and 6")
        spoken = {L.norm_word(w) for w in L.words_of(b["text"])}
        head = (b.get("on_screen") or {}).get("headline", "")
        for w in L.words_of(head):
            if L.norm_word(w) not in spoken:
                problems.append(f"{b['id']}: headline word '{w}' is not spoken in this beat")
        for c in b.get("cues", []):
            for k in ("id", "kind", "element_id", "anchor_word"):
                if k not in c:
                    problems.append(f"{b['id']}: cue missing {k}")
            if c.get("kind") not in ("reveal", "emphasis", "hold"):
                problems.append(f"{b['id']}: cue {c.get('id')} kind {c.get('kind')}")
            if "anchor_word" in c and L.norm_word(c["anchor_word"]) not in spoken:
                problems.append(f"{b['id']}: cue {c.get('id')} anchor '{c['anchor_word']}' not spoken in this beat")
    for sc in s.get("scenes", []):
        for bid in sc["beats"]:
            if bid not in beat_ids:
                problems.append(f"scene {sc['id']} lists unknown beat {bid}")
    if total > BUDGET:
        problems.append(f"character budget exceeded: {total} > {BUDGET}")
    words = sum(len(L.words_of(b["text"])) for b in s.get("beats", []))
    if v2:
        rows, est, sil = check_v2(s, d, problems, warns)
        print(f"chars {total}/{BUDGET} | words {words} | planned {est:.2f} s (target {s.get('target_duration_s')} ± {s.get('duration_tolerance_s')}) "
              f"| planned silence {sil:.1%} (lead-in + gaps ≥ {L.SILENCE_MIN_S} s; motif tail excluded)")
        for r in rows:
            print(f"  {r['start']:6.2f}-{r['end']:6.2f}  {r['id']:<4} {r['slot']:<24} {r['words']:>2} w @{r['wpm']:.0f}  + {r['pause_s']:.2f} {r['purpose']}")
        return report(problems, warns)
    if slots and slots[0] != "hook.question_reveal":
        problems.append("first beat must be hook.question_reveal")
    if slots and slots[-1] != "outro.disclosure":
        problems.append("last beat must be outro.disclosure")
    for req in ("check.predict", "recap.statement"):
        if req not in slots:
            problems.append(f"missing slot {req}")
    order = [L.SLOTS.index(x) for x in slots if x in L.SLOTS]
    if order != sorted(order):
        problems.append("slots are out of the contract order (hook → check.predict → explain → worked/misconception → check.retrieval → recap → outro)")
    if "worked.step" not in slots and "misconception.confront" not in slots:
        problems.append("need at least one of worked.step or misconception.confront")
    est = words / 2.4 + sum(float(b.get("pause_after_s", 0)) + float(b.get("think_window_s", 0)) for b in s.get("beats", []))
    print(f"chars {total}/{BUDGET} | words {words} | estimated {est:.0f} s at 144 wpm (target {s.get('target_duration_s')}) "
          f"| as placed (lead-in, provider pads, tail) {L.plan(s)[1]:.1f} s | planned silence {L.silence_share(s):.1%}")
    return report(problems, warns)


def report(problems, warns):
    for w in warns:
        print("WARN:", w)
    if problems:
        print("PROBLEMS:"); [print(" -", p) for p in problems]; sys.exit(1)
    print("OK" + (f" ({len(warns)} warnings)" if warns else ""))


if __name__ == "__main__":
    main(sys.argv[1])
