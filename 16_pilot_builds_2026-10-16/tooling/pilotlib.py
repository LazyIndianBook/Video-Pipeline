"""Shared helpers for the 16 Oct 2026 pilot builds: script loading, word tokenising, synthetic and measured
cue sheets, Chrome injection. Plain Python 3.11+; Playwright only where a function says so.

Script v2 (16 Oct 2026, Professor Diki Simplified, `format/concept_short_60`; field reference
17_professor_diki_simplified/format/script_v2_fields.md). A script with `"schema_version": "script/v2"` (or
`"script_version": 2`) uses per-beat `pauses: [{purpose, after_s?}]` (alias `s`; PD-01 seconds when omitted),
`energy` 1-5 (low|mid|high|peak accepted as 2|3|4|5), `visual_op`, `insight_beat`, a `check.transfer` beat, an `outro.brand` beat spoken exactly
"Professor Diki Simplified." and an on-screen disclosure (outro `on_screen.disclosure`, top-level
`outro.end_card.disclosure_line`, or fixture `display.ui.disclosure` bound by the scene).
v1 scripts (no script_version) behave exactly as before: `pause_after_s` + `think_window_s`, 144 wpm synthetic pacing.
Cue sheets of both versions carry `meta.pauses[]` (beat, purpose, seconds, start, end), `meta.energy[]` and the old
`meta.think_windows[]` (every think_* pause), so v1 scenes keep working."""
import hashlib, json, os, pathlib, re, unicodedata

FPS = 30
WORDS_PER_S = 2.4            # synthetic pacing ≈ 144 wpm (l9_10 band)
WORD_GAP_S = 0.06
LEAD_DEFAULT = 0.05
TAG_RE = re.compile(r"\[[a-z ]+\]")
ALLOWED_TAGS = {"[curious]", "[calm]", "[warm]", "[thoughtful]"}
SLOTS = ["hook.question_reveal", "check.predict", "explain.ladder_step", "worked.step", "misconception.confront",
         "check.retrieval", "recap.statement", "outro.disclosure"]
DISCLOSURE = "AI-generated narration; script by ExamLeaf."   # v1 only (retired by PD-02 for shorts)

# --- script v2 -------------------------------------------------------------------------------------------------
LEAD_IN_S = 0.3              # first word of the video (PD-16, 16 Oct 2026: was 0.6; the board is complete at frame 0)
TAIL_S_V1 = 1.6              # v1 hold after the last beat
TAIL_S_V2 = 0.9   # 0.1 s after the last word + the 0.70 s end motif + frame rounding (16 Oct 2026: 0.8 clipped the motif by 60 ms)              # v2 tail after the last word: the 0.6-0.75 s end motif (A3-07); override with `tail_s`
END_CARD_MIN_S = 1.5         # v2 end card on screen from the outro beat's first word to the end (brand line + tail)
PROVIDER_PAD_S = 0.25        # v1 only: provider head/tail silence per beat clip (A3-01); v2 trims clips to word edges
SILENCE_MIN_S = 0.3          # a gap shorter than this is a join, not silence (A3 measurement, scorecard A13)
PAUSE_S = {"join": 0.25, "land": 0.6, "inspect": 1.0, "think_recall": 1.5, "think_choice": 2.0, "think_calc": 3.0,
           "pause_video": 1.0}                                   # PD-01 defaults when after_s is omitted
PAUSE_RANGE = {"join": (0.2, 0.35), "land": (0.5, 0.7), "inspect": (0.8, 1.2), "think_recall": (1.35, 1.65),
               "think_choice": (1.8, 2.2), "think_calc": (2.7, 3.3), "pause_video": (0.9, 1.1)}   # PD-01, ±10 %
PAUSE_ALIAS = {"think_choose": "think_choice"}               # professor-diki-script skill spelling
# slot names shared with skills/professor-diki-script (check_pd_script.py); speaking rate per slot (wpm, active rate
# first word to last word of a one-sentence beat): narration 150-160, formula and exception 125-140
RATE_WPM = {"hook.question_reveal": 160, "explain.intuition": 155, "explain.givens": 160, "explain.prerequisite": 150,
            "check.predict": 150, "reveal.answer": 160, "explain.mechanism": 160, "worked.step": 145, "worked.faded": 145,
            "explain.formal": 130, "exam.language": 135, "misconception.confront": 135, "check.transfer": 150,
            "explain.definition": 150, "explain.condition": 140, "recap.statement": 140,   # explainer_60 (PD-24)
            "feedback.transfer": 160, "close.next_step": 150, "outro.brand": 140}
V2_SLOTS = list(RATE_WPM)
V2_ANCHORS = ["hook.question_reveal", "check.predict", "reveal.answer", "check.transfer", "feedback.transfer",
              "close.next_step", "outro.brand"]                   # first occurrences must come in this order
EXPLAINER_ANCHORS = ["hook.question_reveal", "explain.definition", "explain.mechanism", "explain.formal", "explain.condition",
                     "worked.step", "recap.statement", "close.next_step", "outro.brand"]   # explainer_60 (PD-24): no questions
PEAK_SLOTS = {"concept_short_60": ("reveal.answer", "check.transfer", "feedback.transfer"), "explainer_60": ("explain.mechanism", "worked.step", "recap.statement")}
SILENCE_MAX_BY_FORMAT = {"concept_short_60": 0.15, "explainer_60": 0.10}
SHORT_FORMATS = tuple(SILENCE_MAX_BY_FORMAT)


EXPLAINER_REQUIRED = ("explain.definition", "explain.mechanism", "explain.condition", "worked.step")
EXPLAINER_TAIL = ("recap.statement", "close.next_step", "outro.brand")


def spine_problems(script):
    """explainer_60 spine (PD-26, method §2): hook first; the required functions present in whatever order the example
    needs; recap -> close -> outro last and in order. Returns a list of problem strings (empty = fine)."""
    slots = [b["slot"] for b in script.get("beats", [])]; out = []
    if not slots or slots[0] != "hook.question_reveal": out.append("first beat must be hook.question_reveal (the purpose)")
    for r in EXPLAINER_REQUIRED:
        if r not in slots: out.append(f"missing function {r}")
    tail = [s for s in slots if s in EXPLAINER_TAIL]
    firsts = [slots.index(t) for t in EXPLAINER_TAIL if t in slots]
    if firsts != sorted(firsts) or any(t not in slots for t in EXPLAINER_TAIL): out.append("the short must end recap.statement -> close.next_step -> outro.brand (pay-off before the invitation, brand last)")
    elif firsts and any(i > firsts[0] for i, s in enumerate(slots) if s not in EXPLAINER_TAIL): out.append("no explain/worked beat may follow the recap (the promise is paid before the invitation)")
    return out


def anchors_for(script):
    """Slot spine by format: explainer_60 (PD-24) has no prediction or transfer; everything else uses the question format."""
    return EXPLAINER_ANCHORS if (script or {}).get("format") == "explainer_60" else V2_ANCHORS
ENERGY_ALIAS = {"low": 2, "mid": 3, "high": 4, "peak": 5}


def energy_level(b):
    """Energy mark of a beat as an int 1-5, or None when missing or invalid."""
    e = ENERGY_ALIAS.get(b.get("energy"), b.get("energy"))
    return e if isinstance(e, int) and not isinstance(e, bool) and 1 <= e <= 5 else None
VISUAL_OPS = {"PreserveObject", "Reveal", "Headline", "Badge", "StrikeThrough", "MapSymbol", "PauseForPrediction",
              "Emphasize", "ChangeValue", "CompareStates", "EquationTransform", "RevealMismatch", "SwapPart",
              "TracePath", "EndMotif"}          # 17/design_system/tokens.json motion.verbs + PreserveObject
CANDIDATE_TAGS = {"[excited]", "[confident]", "[surprised]"}   # usable in v2 with a warning until an audition admits them
OUTRO_TEXT = "Professor Diki Simplified."
CTA_RE = re.compile(r"Try the free lesson on [^.?!]+\.")      # PD-14 default shape; the request's `cta_line` wins
DISCLOSURE_RE = {"B": r"AI-generated narration", "A": r"Performed by [^;·{}]+ ?[;·] voice converted with AI",   # PD-12 "·"
                 "A_direct": r"Narrated by [^;{}]+"}            # 17/brand/strings.json end_card.disclosure_line_pattern
BANNED_RE = re.compile(r"exam[\s_.\-]*leaf", re.I)


def is_v2(script):
    return script.get("schema_version") == "script/v2" or int(script.get("script_version", 1)) >= 2


def tail_s(script):
    if not is_v2(script):
        return float(script.get("tail_s", TAIL_S_V1))
    return float(script.get("tail_s", (script.get("outro") or {}).get("tail_s", TAIL_S_V2)))


def disclosure_of(script, b):
    """On-screen disclosure text carried by the script for beat b (outro), or None (scene binds display.ui.disclosure)."""
    d = (b.get("on_screen") or {}).get("disclosure")
    if not d and b["slot"] == "outro.brand":
        d = ((script.get("outro") or {}).get("end_card") or {}).get("disclosure_line")
    return d


def beat_wpm(b, v2=True):
    """Planned words per minute for a beat. v2: the slot rate (or target_wpm) times the script's voice.rate_scale, the
    calibration knob for the real voice: George / eleven_v4 dialogue with the direction tags measured 122 wpm overall on
    16 Oct 2026 against a table mean near 150, i.e. rate_scale 0.82 (set it per voice in script.json voice{})."""
    if not v2:
        return WORDS_PER_S * 60
    return float(b.get("target_wpm") or RATE_WPM.get(b["slot"], 150)) * float(b.get("_rate_scale", 1.0))


def beat_pause(b):
    """(purpose, seconds) of the gap after a beat's last word. v2: `pauses` [{purpose, after_s?}] (one entry; a bare
    object is accepted); v1 or v2 without `pauses`: pause_after_s + think_window_s, purpose think_calc if a window."""
    p = end_pause(b)
    if p:
        purpose = PAUSE_ALIAS.get(p["purpose"], p["purpose"])
        return purpose, float(p.get("after_s", p.get("s", PAUSE_S.get(purpose, 0.0))))
    pa, tw = float(b.get("pause_after_s", 0)), float(b.get("think_window_s", 0))
    return ("think_calc" if tw > 0 else "unlabelled"), pa + tw


def end_pause(b):
    """The v2 pause entry at the end of beat b (`at` omitted or "end"), or None."""
    p = b.get("pauses")
    p = [p] if isinstance(p, dict) else (p or [])
    return next((x for x in p if x.get("at", "end") == "end"), None)


def plan(script):
    """Estimated video timeline as narrate.py places it: ([{id, slot, words, wpm, start, end, purpose, pause_s}], total).
    v2: per-beat rate, word-edge placement, no gap after the last beat, TAIL_S_V2 tail.
    v1: 144 wpm + PROVIDER_PAD_S per clip, pause_after_s + think_window_s, TAIL_S_V1."""
    v2 = is_v2(script); beats = script["beats"]; t = LEAD_IN_S; out = []
    for i, b in enumerate(beats):
        n = len(words_of(b["text"])); wpm = beat_wpm(b, v2)
        end = t + n * 60.0 / wpm + (0.0 if v2 else PROVIDER_PAD_S)
        purpose, sec = beat_pause(b)
        if v2 and i == len(beats) - 1:
            sec = 0.0
        out.append({"id": b["id"], "slot": b["slot"], "words": n, "wpm": wpm, "start": round(t, 2), "end": round(end, 2),
                    "purpose": purpose, "pause_s": sec})
        t = end + sec
    return out, round(t + tail_s(script), 2)


def silence_share(script):
    """Planned silence (lead-in + every gap ≥ SILENCE_MIN_S) over planned duration; the tail is excluded (it carries the
    end motif under the end card). Intra-beat sentence breaks the voice adds are not in the plan: measure them."""
    rows, total = plan(script)
    return (LEAD_IN_S + sum(r["pause_s"] for r in rows if r["pause_s"] >= SILENCE_MIN_S)) / total


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p) -> str:
    return sha256_bytes(pathlib.Path(p).read_bytes())


def norm_word(w: str) -> str:
    """Same spirit as the narration comparator: NFC, casefold, keep letters/marks/digits and inner apostrophes."""
    w = unicodedata.normalize("NFC", w).casefold()
    return "".join(ch for ch in w if unicodedata.category(ch)[0] in "LMN" or ch in "'’")


def words_of(text: str):
    """Spoken words of a beat text (tags stripped), as they will be shown and matched. Keeps the surface form."""
    text = TAG_RE.sub(" ", text)
    out = []
    for tok in text.split():
        core = tok.strip(".,;:!?\"“”()[]")
        if core and norm_word(core):
            out.append(core)
    return out


NUM = {"zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "twelve": "12", "twenty": "20", "forty": "40", "fifty": "50", "hundred": "100"}


def canon(seq):
    """Spoken-vs-heard canonical form: number words → digits; a lone letter followed by digits joins (H two → h2)."""
    SYM = {"+": "plus", "=": "equals", "→": "gives", "->": "gives"}
    toks = [NUM.get(w, SYM.get(w, w)) for w in seq]; out = []
    formula = lambda t: any(ch.isdigit() for ch in t) and any(ch.isalpha() for ch in t) and len(t) <= 8
    for w in toks:
        if out and len(out[-1]) == 1 and out[-1].isalpha() and w.isdigit():
            out[-1] = out[-1] + w                       # H 2 → h2
        elif out and formula(out[-1]) and (w.isdigit() or (len(w) == 1 and w.isalpha())):
            out[-1] = out[-1] + w                       # h2 o → h2o ; h2o 2 → h2o2
        else:
            out.append(w)
    return out


# --- local voice and speech-to-text (PD-29, 27 Oct 2026: ElevenLabs retired) -------------------------------------
STUDIO = pathlib.Path(os.environ.get("DIKI_STUDIO", "~/Movies/DikiStudio")).expanduser()   # .venv, models/, voice/reference.wav
STT_MODEL = "models/whisper-small.en-asr-fp16"
STT_PROMPT = "Professor Diki Simplified."   # spelling hint: without it Whisper writes "Dickey" and "iR", flagging every outro (27 Oct 2026)


def stt_words(wav_path, model=None):
    """[(word, t0, t1)] from local Whisper small.en word timestamps (MLX Audio, offline). Pass a loaded model to reuse it."""
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    if model is None:
        from mlx_audio.stt.utils import load
        model = load(str(STUDIO / STT_MODEL))
    r = model.generate(str(wav_path), word_timestamps=True, language="en", initial_prompt=STT_PROMPT)
    return [(w["word"].strip(), float(w["start"]), float(w["end"])) for seg in r.segments for w in seg.get("words", [])]


def heard_tokens(words):
    """norm_word tokens of a transcript in the script's spoken style: a transcript's "0.2" reads "point 2" and "1.5"
    reads "1 point 5" (PD-27 speaks numbers naturally), so canon() of both sides compares like for like. Whisper may
    split "0.2" into the words "0" and ".2"; the pair reads the same way."""
    out = []
    for w in words:
        m = re.fullmatch(r"(\d*)\.(\d+)", w.strip(",;:!?\"“”()").rstrip("."))
        if m:
            if not m[1] and out and out[-1] == "0": out.pop()
            out += ([m[1]] if m[1] not in ("", "0") else []) + ["point"] + list(m[2])
        elif norm_word(w):
            out.append(norm_word(w))
    return out


def load_script(path):
    p = pathlib.Path(path)
    s = json.loads(p.read_text(encoding="utf-8"))
    s["_path"] = str(p); s["_dir"] = str(p.parent); s["_sha256"] = sha256_file(p)
    rs = float(((s.get("voice") or {}).get("rate_scale")) or 1.0)          # voice calibration (see beat_wpm)
    for b in s.get("beats", []):
        b["_rate_scale"] = rs
    return s


def beats_by_scene(script):
    by = {sc["id"]: [] for sc in script["scenes"]}
    for b in script["beats"]:
        by[b["scene"]].append(b)
    return by


def resolve_cues(scene_words, beat_word_ranges, beats):
    """scene_words: list of {w,t0,t1,beat}; beat_word_ranges: beat_id -> (start_index, end_index). Returns cue list."""
    cues = []
    for b in beats:
        s, e = beat_word_ranges[b["id"]]
        for c in b.get("cues", []):
            target = norm_word(c["anchor_word"]); occ = int(c.get("occurrence", 1)); n = 0; idx = None
            for i in range(s, e):
                if norm_word(scene_words[i]["w"]) == target:
                    n += 1
                    if n == occ:
                        idx = i; break
            if idx is None:
                raise ValueError(f"cue {c['id']}: anchor '{c['anchor_word']}' (occurrence {occ}) not in beat {b['id']}")
            at = max(0.0, round(scene_words[idx]["t0"] - float(c.get("lead_s", LEAD_DEFAULT)), 3))
            cue = {"id": c["id"], "at": at, "kind": c["kind"], "element_id": c["element_id"], "word_index": idx}
            if c["kind"] == "hold":
                cue["until"] = float(c["until"]) if "until" in c else None
            cues.append(cue)
    return cues


def build_scene_sheet(script, scene_id, timing=None, audio_sha=None, alignment_source="synthetic_even_spacing", duration_override=None):
    """timing: optional {beat_id: {"start": s, "words": [{"w","t0","t1"}], "end": s}} in VIDEO time; without it, synthetic.
    Returns (sheet, scene_start_video_s, scene_end_video_s)."""
    by = beats_by_scene(script)
    beats = by[scene_id]; v2 = is_v2(script); last_id = script["beats"][-1]["id"]
    gap = lambda b: 0.0 if (v2 and b["id"] == last_id) else beat_pause(b)[1]
    words = []; ranges = {}; t = 0.0; beat_marks = []
    scene_start = None
    for b in beats:
        if timing:
            tb = timing[b["id"]]
            if scene_start is None:
                scene_start = tb.get("scene_start", tb["start"])
            start = tb["start"] - scene_start
            ws = [{"w": w["w"], "t0": round(w["t0"] - scene_start, 3), "t1": round(w["t1"] - scene_start, 3), "beat": b["id"]} for w in tb["words"]]
            t = tb["end"] - scene_start
        else:
            if scene_start is None:
                scene_start = 0.0
            start = t; ws = []; wps = beat_wpm(b, v2) / 60
            for w in words_of(b["text"]):
                ws.append({"w": w, "t0": round(t, 3), "t1": round(t + 1 / wps - WORD_GAP_S, 3), "beat": b["id"]}); t += 1 / wps
            t += gap(b)
        beat_marks.append(round(start, 3))
        ranges[b["id"]] = (len(words), len(words) + len(ws)); words.extend(ws)
    duration = round(duration_override, 3) if duration_override else round(t + 0.4, 3)   # tail hold so the last word never ends on the cut
    cues = sorted(resolve_cues(words, ranges, beats), key=lambda c: (c["at"], c["id"]))   # validator: sorted by at
    for c in cues:
        if c["kind"] == "hold" and c.get("until") is None:
            c["until"] = duration
    # occurrence index for repeated surface forms: exact `w` string, 1..n in order (validate_cue_sheet.py semantics)
    groups = {}
    for w in words:
        groups.setdefault(w["w"], []).append(w)
    for form, ws in groups.items():
        if len(ws) > 1:
            for n, w in enumerate(ws, 1):
                w["occurrence"] = n
    sheet = {"schema_version": "1.0", "scene_id": f"{script['video_id']}-{scene_id}", "fps": FPS, "duration": duration,
             "language": script["locale"], "alignment_source": alignment_source,
             "narration_audio_sha256": audio_sha, "script_sha256": script["_sha256"],
             "words": [{k: v for k, v in w.items() if k != "beat"} for w in words], "beats": beat_marks, "cues": cues, "sfx": [],
             "meta": {"video_id": script["video_id"], "scene": scene_id, "beat_ids": [b["id"] for b in beats]}}
    # scene-local beat records: verbatim approved text (punctuation intact), headline, slot, spoken span, think window,
    # labelled pause (v2: from the last word; v1: pause_after_s "unlabelled" then the think window), energy, visual op
    beat_meta = []; think = []; pauses = []; energy = []
    for b in beats:
        s_i, e_i = ranges[b["id"]]
        start = words[s_i]["t0"] if e_i > s_i else beat_marks[[x["id"] for x in beats].index(b["id"])]
        end = words[e_i - 1]["t1"] if e_i > s_i else start
        on = b.get("on_screen") or {}
        rec = {"id": b["id"], "slot": b["slot"], "text": b["text"], "headline": on.get("headline", ""),
               "start": round(start, 3), "end": round(end, 3), "word_range": [s_i, e_i]}
        for k in ("energy", "visual_op", "insight_beat", "emphasis_words"):
            if k in b:
                rec[k] = b[k]
        if on.get("claim_line"):
            rec["claim_line"] = on["claim_line"]
        if v2 and disclosure_of(script, b):
            rec["disclosure"] = disclosure_of(script, b)
        if v2:
            purpose, sec = beat_pause(b)
            if sec > 0 and b["id"] != last_id:
                pz = {"beat": b["id"], "purpose": purpose, "seconds": sec, "start": round(end, 3), "end": round(end + sec, 3)}
                if (end_pause(b) or {}).get("prompt"):
                    pz["prompt"] = end_pause(b)["prompt"]
                pauses.append(pz); rec["pause"] = pz
                if purpose.startswith("think_"):
                    tw = dict(pz); think.append(tw); rec["think_window"] = tw
        else:
            pa = float(b.get("pause_after_s", 0))
            if pa > 0:
                pauses.append({"beat": b["id"], "purpose": "unlabelled", "seconds": pa, "start": round(end, 3), "end": round(end + pa, 3)})
            if float(b.get("think_window_s", 0)) > 0:
                tw = {"beat": b["id"], "seconds": float(b["think_window_s"]), "start": round(end + pa, 3)}
                tw["end"] = round(tw["start"] + tw["seconds"], 3); think.append(tw); rec["think_window"] = tw
                pauses.append({"beat": b["id"], "purpose": "think_calc", **{k: tw[k] for k in ("seconds", "start", "end")}})
        if "energy" in b:
            energy.append({"beat": b["id"], "energy": energy_level(b), "start": round(start, 3), "end": round(end, 3)})
        beat_meta.append(rec)
    sheet["meta"]["beats_text"] = beat_meta; sheet["meta"]["think_windows"] = think
    sheet["meta"]["pauses"] = pauses; sheet["meta"]["energy"] = energy
    if v2 and (script.get("outro") or {}).get("end_card"):
        sheet["meta"]["end_card"] = script["outro"]["end_card"]
    return sheet, scene_start, (scene_start + duration)


def init_script_for(sheet, fixture):
    return ("window.__CUE_SHEET__=" + json.dumps(sheet, ensure_ascii=False) + ";window.__FIXTURE__=" + json.dumps(fixture, ensure_ascii=False) + ";")


def open_scene(p, scene_path, sheet, fixture, fps=FPS, seed=20261016):
    """Playwright: returns (browser, page) with the scene loaded, ready awaited. Caller closes the browser."""
    import os
    # Software rasterisation by default (16 Oct 2026): with the GPU on, a long scene showed 2–4 mismatched frames of 831
    # across identical runs; with --disable-gpu the same scene reproduced 831/831 at near-identical speed (49.9 s vs 44.3 s).
    extra = [x for x in os.environ.get("PILOT_CHROME_ARGS", "--disable-gpu").split() if x]
    b = p.chromium.launch(channel="chrome", headless=True, args=["--force-device-scale-factor=1", "--hide-scrollbars"] + extra)
    ctx = b.new_context(viewport={"width": 1080, "height": 1920}, device_scale_factor=1, offline=True)
    page = ctx.new_page()
    page.add_init_script(init_script_for(sheet, fixture))
    page.goto(pathlib.Path(scene_path).resolve().as_uri() + f"?fps={fps}&seed={seed}&strict=1", wait_until="load")
    page.evaluate("async () => { if (window.ready) await window.ready; }")
    return b, page


# The design system's verb list is the source of truth for visual_op (tokens.motion.verbs), so the checker cannot
# drift behind it (16 Oct 2026: v2 added Pop, Slide, Chips, Tape and Card for PD-18/PD-19).
try:
    import json as _json, pathlib as _pathlib
    _T = _json.loads((_pathlib.Path(__file__).resolve().parents[2] / "17_professor_diki_simplified/design_system/tokens.json").read_text(encoding="utf-8"))
    VISUAL_OPS = set(VISUAL_OPS) | {k for k in _T["motion"]["verbs"] if not str(k).startswith("$")} | {"PreserveObject"}
except Exception:
    pass
