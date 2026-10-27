# Narration direction sheet: Professor Diki Simplified 60 s short (Eleven v4)

**27 Oct 2026 (PD-29):** the voice is now VoxCPM2 in the founder's cloned voice. `narrate_voxcpm.py` strips these tags before speaking and takes the delivery from one fixed instruction, so the tags only record intent. They will steer delivery again only if a VoxCPM2 audition shows that a per-tag instruction measurably changes F0, level or rate.

Status (16 Oct 2026): binding for `format/concept_short_60`. Sources: A3 measurements and §4, PD-01, PD-02, PD-05. Tags marked † are candidates: they stay out of production scripts until an audition on the chosen voice shows a measured change in F0, level or rate. check_script warns when one is used.

## 1. Tags per beat type (one tag per beat, in the `tag` field, never inside `text`)

| Beat | Tag | Delivery |
|---|---|---|
| hook (question) | `[curious]` (`[excited]`† later) | bright, +2 st above the median, rising end |
| givens, insight | none | brisk and plain; the numbers are the content |
| predict, transfer (questions) | `[curious]` | one question, a real rise, then stop: the window is the answer |
| reveal, feedback (payoff) | none now; `[confident]`† after audition; `[warm]` on the confirmation line | the answer is short and lands; "If you said …, you're right" is warm, not loud |
| mechanism | none | steady, contrastive |
| formula, exam line | `[calm]` | 125–135 wpm, each symbol distinct |
| exception (turn) | none now; `[surprised]`† after audition | the second peak: "But a bulb?" ≥ +1 st above the median |
| close, outro | `[warm]` | falling cadence; "Try the free lesson on <topic>." (PD-14 `cta_line`) said as an invitation, not a pitch; brand line unhurried, never sung |

**Do not tag** a beat under 1.5 s (except the outro), two same-intention beats in a row, a reveal's number sentence (tags blur digits), or any line a tag would make sound like an advert. No `[excited]` in the close, no laughter tags, no jokes by tag.

## 2. Energy curve (marks 1–5)

**4 · 3 · 4 · 5 · 3 · 2 · 4→3 · 4 · 5 · 3 · 3** (hook, givens, predict, reveal, mechanism, formal, exception, transfer, feedback, close, outro). Peaks are the payoffs, the trough is the formula, nothing after the transfer drops below 3. Beats run 2–6 s; no run over 20 s stays within ±0.5 dB and ±1 semitone (A3-M1).

## 3. Emphasis rules

- **Contrast the changed quantity.** Emphasise the one value that changed ("**four** volts", "**six** volts"), a negation ("**never** the small two") or the condition ("**constant** temperature"). List them in `emphasis_words`.
- **Land the unit.** Say the number and its unit as one breath group ("zero point four amps"), not number … unit. When the unit is dropped (as in "zero point six"), the screen shows it.
- **One emphasis per sentence.** Never put it on the last word of a falling sentence: declination drops it (A3-10, "air" −7.1 dB). Put the changed value in a short sentence of its own or before the final word.
- **No stock phrases** ("Let us embark", "It's that simple", "Mind blown"), no hype, no countdown.

## 4. Pause rendering

The pause policy (PD-01; seconds ±10 %; every pause carries its `purpose`):

| Purpose | Use | Seconds |
|---|---|---|
| join | clause to clause | 0.2–0.35 |
| land | a result or changed value | 0.5–0.7 |
| inspect | formula or condition | 0.8–1.2 |
| think_recall | recall, binary, count ≤ 3 | 1.5 |
| think_choice | choose 1 of 3–4 | 2.0 |
| think_calc | one-step calculation, numbers on screen | 3.0 |
| pause_video | multi-step (out of format) | 1.0 hold |

**Room tone, not digital silence.** `narrate.py` renders every gap as room tone:
- A seeded pink-noise bed (−60 dBFS RMS, seed 20261016) runs under the whole mix; clips get 10 ms edge fades.
- The master is two-pass linear loudnorm (−16 LUFS, −1.5 dBTP), so the bed is not pumped up in the gaps.
- v2 clips are trimmed to their aligned words (+0.03 s head, +0.08 s tail). The next word starts exactly the pause seconds after the last word: provider head and tail silence never adds to a pause.

A human mixer keeps the bed continuous (never gated) and adds nothing in think windows; the motif plays only in the tail.

## 5. What to measure after synthesis

Measure from `narration/timeline.json` and the beat align files before any render:

| Measure | Target |
|---|---|
| Per-beat active wpm | inside the slot band; never sped past ×1.1 (shorten the text instead) |
| Silence share | ≤ 15 % (silences of 0.3 s or more, lead-in included, motif tail excluded); every silence matches its scripted purpose ±25 % |
| Unlabelled silence ≥ 0.3 s | 0 |
| Intra-beat sentence breaks | ≤ 0.35 s (split the beat if longer) |
| Onset of the first insight | `insight_beat` first word ≤ 10.0 s |
| Hook question | complete ≤ 3.0 s (3.5 s accepted) |
| Payoff | reveal first word ≤ 3 s after its window |
| Turn and reveal pitch | reveal and turn ≥ +1 st (or +1 dB) above the video median |
| Emphasis words | at or above the beat median RMS |
| Total | 60.0 ± 1.0 s; tail ≤ 1.0 s |
| Loudness | −16 ± 1 LUFS; true peak ≤ −1.5 dBTP |
| Brand | no "ExamLeaf" in any word of the timeline |

Regenerate or shorten only the failing beat; the cache keeps passing beats free.

## 6. Voice brief for the Indian-English audition (after the plan upgrade; PD-05)

Professor Diki is an adult Indian-English science teacher: warm, bright, alert and on the learner's side; crisp STEM consonants ("ohms", "coefficient", "subscript"); clear numbers ("zero point four"); natural en-IN rhythm, no put-on accent, no British storyteller register.

**Candidates.** Audition three on one 60 s golden passage, the physics sample script: two Voice Library en-IN voices and one Voice Design voice.

**Rubric** (native-editor and teacher ratings): number clarity, warmth, energy range (hook and turn lift measurably), question rise, terminal creak (A3-11: none), pace control at 125–160 wpm, and tag response (do `[curious]`, `[confident]`, `[surprised]` move F0, level or rate?).

**Admission.** Pin the winner's voice_id and settings in the voice registry. Admit only the tags whose measured effect passed. Until then, demos keep the stock voice and are labelled as such.

## Measured (16 Oct 2026, first narration of the physics demo)

George (`JBFqnCBsd6RMkjVDRZzb`) on `eleven_v4` text-to-dialogue with the tags above: 122 words per minute overall across 14 beats (99–164 by beat; the calm formal and exam beats are the slowest at 99–118), pauses landed within 0.1 s of the plan. The rate table in `pilotlib.RATE_WPM` assumed 130–160, so a 125-word script ran 70.0 s. Calibration: `voice.rate_scale` 0.82 (PD-22); a 60-second short for this voice is 98–111 words. Re-measure when the voice, model or tags change.

**Alignment edges (16 Oct 2026, second pass).** The v4 character alignment stamps the first word at 0.00 s and the last word at the clip end even when the clip carries lead or trailing silence, which stretched every gap by 0.1–0.3 s (2.6 s over 14 beats). `narrate.py` now trims each clip to its audible voice (10 ms windows above −45 dBFS) before placing it, so measured gaps equal the planned pauses to the hundredth. Plan pauses at the middle of their PD-01 bands; do not reach for tempo to hit 60 s.
