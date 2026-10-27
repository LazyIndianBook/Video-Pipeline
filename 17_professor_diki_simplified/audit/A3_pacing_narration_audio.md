# A3 — Pacing, narration, audio, momentum (Opus physics, chemistry, biology)

Auditor A3, 16 Oct 2026. **Sources:** `measurements.json`, the beat WAVs and align files, `timeline.json`, `script.json`, the cue sheets, the tooling (`narrate.py`, `qa.py`, `check_script.py`, `pilotlib.py`), `PILOT_CONTRACT.md`, the 05 voice guide, the 11 playbook and the persona registry.

**What I measured** (scripts and output in `_scratch_A3/`):
- per-beat active wpm, from first word to last word;
- provider head and tail silence;
- word-level RMS;
- an autocorrelation F0 track (70 Hz floor, crude);
- ebur128 and astats on the MP4s;
- change-event density from the cue sheets.

**I cannot listen.** Accent, warmth, creak and whether emphasis lands are inferred from numbers and need a human check.

**Findings:** 21 in `A3_findings.json`: 1 critical, 9 high, 7 medium, 4 low.

## 1. Where the seconds go

| | Physics | Chemistry | Biology |
|---|---|---|---|
| Duration | 71.93 s | 73.20 s | 67.10 s |
| Content speech / active rate | 55.6 s / 147 wpm | 57.2 s / 147 wpm | 51.4 s / 159 wpm |
| Silence ≥ 0.3 s | 18.7 s (26 %) | 20.9 s (29 %) | 17.2 s (26 %) |
| Effective rate (content words ÷ duration) | 113 wpm | 115 wpm | 122 wpm |
| Lead-in / think / tail | 0.71 / 5.51 / 2.19 | 0.70 / 5.56 / 2.25 | 0.70 / 5.25 / 2.18 |
| Recap end → video end | 6.61 s | 6.70 s | 6.52 s |

The speaking rate is already in the 130–155 band. The videos feel slow because a quarter of the runtime is silence and the last ~6.6 s is a slow legal line. For "faster but comprehensible", cut the dead time first. Speed up only ordinary beats, and only second. The fixes below take physics from 71.9 s to about 59–60 s without changing a word of teaching.

## 2. Pacing, voice and audio findings

Full evidence, root causes and controls for each row are in the JSON.

| ID | Sev | Evidence | Root cause | Permanent fix (control) |
|---|---|---|---|---|
| A3-01 | high | 67–73 s against 60 s; the estimate says ~68 s where physics measures 71.9 s, and nothing gates | contract §3 "60–70 s"; target_duration_s 65; check_script estimate omits pads; A8 accepts 55–80 s | hard limit 60.0 s; estimator includes lead-in, tail and 0.25 s/beat and gates; A8 fails above 60.0 s or below 135 effective wpm |
| A3-02 | **crit** | spoken "…script by ExamLeaf." runs 3.9–4.0 s at 74–77 wpm, plus gap and tail = 6.5–6.7 s | contract §3, pilotlib.DISCLOSURE, check_script exact match, RD-45 | disclosure on screen ≥ 1.5 s + platform AI label; wording for brand auditor/lead; lint: no "ExamLeaf" in speech |
| A3-03 | high | think windows 5.51 / 5.56 / 5.25 s for a binary count (chem), a 3-way choice (bio), a one-step calculation plus an unanswerable judgement (phy); digital silence | think_window_s 5; check_script 4–6; RD-11 5–8 | pause{purpose, difficulty, s} per §4; prompt answerable from the screen; add a short-form row to RD-11 (lead) |
| A3-04 | low | gaps are exact zeros; beat floor is −87 dBFS | narrate.py writes zeros | room tone at −60 dBFS, 10 ms fades |
| A3-05 | med | 4–5 gaps ≥ 0.6 s per video (4.1–6.1 s). Dead: phy 10.47, 56.43, 65.08; chem 11.11, 59.18, 66.17; bio 6.10, 51.49, 60.44. Protected: phy 32.10, 45.40; chem 36.21, 48.52; bio 27.33, 38.83 | provider head/tail + free pause_after_s; scene cuts | trim beats to energy edges; labelled pauses; QA silence-with-purpose |
| A3-06 | med | first word at 0.70 s | LEAD_IN_S 0.6 + provider head | LEAD_IN_S 0.15; first word ≤ 0.30 s |
| A3-07 | med | tail 2.18–2.25 s | last pause_after + TAIL_S 1.6, counted twice | TAIL_S 0.8 with motif; tail ≤ 1.0 s |
| A3-08 | med | bio b01 204 wpm, b02 166, b05 164, phy b01 163; phy b04 129 and bio b04 127 | A8 averages only; v4 has no speed control | target_wpm per beat type; shorten the text, never speed past ×1.1 |
| A3-09 | high | only 4 low-arousal tags; F0 falls 151/159/176 Hz → 126–133 Hz; RMS within 1.7 dB; LRA 3.2–3.9 LU; mode/tag drift | contract tag list; one tag per long beat | §4 tag vocabulary after audition; short beats; ≥ 3 tags |
| A3-10 | med | reveal "air" −7.1 dB (47.34), "not" −0.4 dB (47.64), "four" no longer than "two" (9.72) | no emphasis field; sentence-final placement | emphasis_words; changed value in its own sentence; gate emphasis word ≥ beat median |
| A3-11 | low | questions rise +4.5 / +7.0 st; phrase ends at the 70–79 Hz floor (creak?) | deep stock voice | creak in the audition rubric |
| A3-12 | high | "George" (British premade) on an en-IN persona; no admitted voice; voice_id hard-coded | voice registry gap | Professor Diki voice: adult Indian-English teacher, warm, bright, crisp STEM consonants; audition 2 library + 1 designed voice on a golden passage; gate on an admitted en-IN entry (quota 2,285 chars: auditions **or** regeneration) |
| A3-13 | med | narration only: no SFX, no motif | no audio cue kind; render muxes the voice only | no bed under science; one 0.4–0.8 s end motif; ≤ 3 event SFX, 18–22 dB under the voice, never within ±250 ms of a spoken number |
| A3-14 | low | −16.9 / −16.8 / −16.7 LUFS; TP −1.5 / −1.4 / −1.4; single-pass dynamic | narrate.py loudnorm, not the house two-pass master | two-pass linear to −16.0 ± 0.3; short-form variant at −14 / −1 dBTP (hypothesis; measure each platform) |
| A3-15 | low | word ends 0.08 s past the file on 18/21 beats | provider alignment trusted | snap to energy edges; ≤ 2 frames |

## 3. Momentum and motivation (founder addendum, digest §6)

**Energy curve** (wpm / tag; silence before → after):

| Beat | Physics | Chemistry | Biology |
|---|---|---|---|
| hook | 163 curious (0.71→0.91) | 152 curious | 204 curious |
| predict | 144 curious (→5.51) | 156 thoughtful | 166 curious |
| explain | 153 calm (5.51→0.89) | 143 calm | 160 calm |
| explain/worked | 129 thoughtful (→1.02) | 146 calm | 127 thoughtful |
| misconception | 146 thoughtful (→1.03) | 140 thoughtful | 164 thoughtful |
| recap | 144 warm (→0.94) | 143 warm | 147 warm |
| disclosure | 75 calm (→2.19) | 74 none | 77 calm |

**A3-M1 No arc (high).** Energy peaks in the hook and never again. After the think window there is a 33–38 s flat zone in each video: physics beat RMS within ±0.5 dB and F0 131–141 Hz. Every teaching beat is boxed between silences of 0.6 s or more. *Fix:* an energy-curve target per slot (§4). Gate: the reveal and turn beats sit ≥ +1 semitone or +1 dB above the video median; no run longer than 20 s within ±0.5 dB and ±1 semitone.

**A3-M2 Late first insight (high).** Time to the first usable idea:

| Video | First usable idea | Time |
|---|---|---|
| Physics | "twice the voltage, twice the current" (0.4 A is shown at 27.9 s) | 31.2 s |
| Chemistry | "same count on both sides" (first method at 36.8 s) | 34.6 s |
| Biology | "enters from the air" | 21.4–23.2 s |

The physics prediction comes before any tool: I = V/R and 0.2 A are never given, so a weak learner can only guess. *Fix:* a beat rule that hands over one concrete tool within 10 s, then asks a prediction the tool solves. Gate: first-insight t0 ≤ 10 s, and the answer can be derived from the fields on screen.

**A3-M3 Stalls in the hard sentences (medium).** Change events per 10 s across the explanation: physics 5.2 (mean gap 1.94 s), chemistry 4.5 (2.24 s), biology 5.4 (1.86 s). Gaps longer than 3 s:
- physics: 3 (31.2, 34.8, 42.9);
- chemistry: 2, one of them **8.96 s** with no cue while the conservation law is spoken (25.57–34.53);
- biology: 2 (35.5, 44.2).

These counts come from cue sheets only. *Fix:* every spoken clause anchors a meaningful change on the persistent diagram. Gate: no gap over 3.0 s between the end of the think window and the recap, and ≥ 4 changes per 10 s.

**A3-M4 Diffuse payoff (high).**
- Physics: the number pays off 5.4 s after the window, which is good. The "always" half pays off 24–31 s later.
- Biology: the answer is implied 4.4 s after the window, then stated at 18.5 s and again at 28.5 s, around a detour.
- Chemistry: answered after 4.0 s, but the hook had already half-answered it.
- No video confirms the learner's prediction.

*Fix:* one question per prediction. The answer comes ≤ 3 s after the window as a standalone line with an explicit confirmation ("If you said air: right."), then the why. Gate: answer t0 − window end ≤ 3.0 s.

**A3-M5 The close just stops (high).** Every video ends recap → spoken disclosure → 2.2 s silence. `check.retrieval` is unused in all three. There is no transfer question, no conditional confidence and no next step (brief C01's "Try the free lesson" is missing). *Fix:* a mandatory close: transfer question (2–3 s window) → answer + "If you got 0.6 A, you can use this rule." → one-line next step → motif. Gate: a transfer slot exists, and the last spoken line is a confidence line or a next step.

**A3-M6 Dead time (high).** Lead-in + dead gaps + think time above the table + spoken disclosure + tail:

| Video | Dead time | Share |
|---|---|---|
| Physics | 12.3 s | 17–19 % |
| Chemistry | 13.6 s | 17–19 % |
| Biology | 12.6 s | 17–19 % |

This is before visual dead time (the empty physics board at 0–3.5 s, the 2.2 s of empty sky in biology s04). *Fix:* the A3-02/03/05/06/07 fixes together. Gate: dead time ≤ 2.0 s.

## 4. Professor Diki narration direction sheet (60 s short)

**Arc.** Bright hook (+2 semitones, 155–170 wpm) → hand over one tool → curious prediction that **can succeed** → the answer lands ≤ 3 s after the window, confirmed → steady mechanism (150–160) → **alert** turn on "But…", the second peak → deliberate formula (125–135) → curious transfer question → earned confidence → warm close with a falling cadence and the next step → motif.

**Tags** († = candidate; admit only after an audition shows a measured effect):

| Beat | Tag |
|---|---|
| hook | `[curious]` or `[excited]`† |
| predict / transfer | `[curious]` |
| mechanism | none |
| reveal | `[confident]`† |
| turn | `[surprised]`† |
| formula | `[calm]` |
| confidence / close | `[warm]` |

One intention per beat; beats run 2–6 s.

**Pause policy:**

| Purpose / difficulty | Example | Seconds |
|---|---|---|
| join | inputs → change | 0.2–0.35 |
| land (result or changed value) | "Four volts." | 0.5–0.7 |
| inspect (formula or condition) | V = IR | 0.8–1.2 |
| think: recall, binary, count ≤ 3 | "Which side is short?" | 1.5 |
| think: choose 1 of 3–4, one inference | soil / water / air | 2.0 |
| think: one-step calculation, numbers on screen | 6 V → ? A | 3.0 |
| multi-step or writing | — | not in a short; "pause the video", 1.0 s hold |

Vary each by ±10 %, fill with room tone, and keep the answer hidden until the window ends.

**Emphasis.** Emphasise only the changed quantity, a negation or a condition. One emphasised word per sentence, never the last word of a falling sentence.

**Measure:**
- total ≤ 60.0 s; first word ≤ 0.3 s; tail ≤ 1.0 s; dead time ≤ 2.0 s;
- unlabelled silence ≥ 0.6 s = 0;
- per-beat wpm inside its band;
- first insight ≤ 10 s; payoff ≤ 3 s after the window; no change-event gap over 3 s;
- reveal and turn ≥ +1 semitone;
- transfer slot present, close is a confidence line or next step;
- ≤ 3 SFX, none near a number;
- final MP4 at −16 or −14 LUFS ± 0.5;
- no "ExamLeaf" in spoken text.
