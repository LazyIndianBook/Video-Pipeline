# 08 · Before vs after: the physics short (Ohm's law), original Opus build vs Professor Diki Simplified rebuild

**Status (16 Oct 2026).** Before = `16_pilot_builds_2026-10-16/physics/opus` (the weakest Opus pilot by the audit: 71.9 s, five scene files, an unanswerable prediction, no transfer, "ExamLeaf" on screen). After = `17_professor_diki_simplified/demo/physics_v2` (102-word script from the Professor Diki framework, one persistent scene on design system v2 collage, narrated once with ElevenLabs v4, rendered deterministically). Machine numbers below come from the same QA suite run on both builds under the PD-23 definitions; the judge section is filled from the blind verdicts in `16_pilot_builds_2026-10-16/judging/physics_pd/`.

## 1. Machine measurements (same checks, same definitions)

| Measure | Before (Opus physics) | After (Professor Diki rebuild) |
|---|---|---|
| Runtime | 71.9 s (target 60 ± 1: fail) | 59.2 s (pass) |
| Spoken words / beats / scene files | 141 / 7 / 5 | 102 / 13 / 1 |
| Dead time, pauses ≥ 0.45 s (PD-23) ≤ 15 % | 17.5 % (fail) | 14.0 % (pass) |
| Longest still stretch during speech (≤ 3 s) | 4.0 s (fail) | 3.5 s (fail by 0.5 s at the formal statement; the two added halos are below the detector's threshold) |
| Visual changes per 10 s of speech | 6.12 | 7.5 |
| Board persistence, min similarity 1 s apart (≥ 0.60) | 0.433 (fail: tear-downs) | 0.89 (pass) |
| Pause policy failures (A13) | 11 | 0 (a 0.63 s sentence break is the voice's own, allowed up to 0.8 s) |
| Prediction answerable from spoken givens, transfer present (A18) | fail | pass |
| Brand and disclosure rules (A12) | fail (ExamLeaf on screen and spoken) | pass |
| First usable idea ≤ 10 s, board by 1.5 s (A14) | fail | pass |
| Energy curve with the peak on the reveal or transfer (A21) | fail | pass |
| Checks pass / warn / fail (A1–A21) | 10 / 0 / 11 | 18 / 2 / 1 |

Under the audit's original 0.3 s silence rule the figures are 22.5 % before and 22.6 % after: that rule counts every comma pause and cannot tell designed phrasing from dead air, which is why PD-23 moved the definition to pauses of at least 0.45 s.

## 2. What changed, and where the fix lives

| Defect in the original (audit id) | Root cause in our files | Permanent fix | Proof |
|---|---|---|---|
| 71.9 s runtime, 4–6 s think holds (A3 lens) | PILOT_CONTRACT think window 4–6 s; no time budget | PD-01 pause bands, PD-07 60 ± 1 s, PD-22 voice calibration | A11, A13, A20 pass |
| Prediction not answerable, no transfer (A1-01, A1-02) | slot grammar without givens-before-question or a transfer | PD-06 grammar, check_script v2, A18 | A18 pass |
| Five scene files, resets, empty time (A2-01, A2-10) | one HTML per scene, template hides parts until words | PD-03 one persistent scene, design system v2, A14–A17 | A14, A16, A17 pass |
| Flat, textbook pace (founder) | no energy marks, no re-hooks | energy curve, re-hook ≤ 12 s, claim line, D8 | A21 pass; D8 judged |
| "ExamLeaf" on screen and spoken; AI line on screen (A5) | constants in templates, PD-02 wording | PD-04/PD-20/PD-21 brand rules, brand_check, A12 | A12 pass |
| Voice ran 15 % slower than planned (first narration) | uncalibrated rate table | PD-22 `voice.rate_scale`, word band scaled | planned 59.75 s vs measured 59.1 s |
| Gaps 0.1–0.3 s longer than planned (second narration) | provider alignment edges | `narrate.py` trims clips to the audible voice | measured gaps = planned to 0.01 s |

## 3. Blind judging (three lenses, D1–D8)

Packets: `16_pilot_builds_2026-10-16/judging/physics_pd/` (labels assigned by hash; the judges never saw the mapping, the tier folders or the design-system files, and could not play audio). All three judges picked the rebuild.

| Lens | Build | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | Total /40 | First insight | Turns | Empty s | Shareable line | Gates failed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| craft | before | 3 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 15 | 22.6 s | 3 | 13.8 | none | 7 |
| craft | after | 4 | 4 | 4 | 4 | 4 | 3 | 4 | 4 | 31 | 8.1 s | 6 | 0.6 | Twice the push, twice the flow. | 0 |
| pull | before | 4 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 16 | 31.8 s | 3 | 13.6 | none | 7 |
| pull | after | 5 | 4 | 4 | 5 | 4 | 3 | 4 | 4 | 33 | 7.3 s | 6 | 0.6 | Twice the push, twice the flow. | 0 |
| teaching | before | 4 | 2 | 2 | 2 | 2 | 1 | 2 | 1 | 16 | 22.6 s | 3 | 8.4 | Twice the voltage, twice the current. | 7 |
| teaching | after | 5 | 4 | 4 | 5 | 4 | 3 | 5 | 4 | 34 | 8.1 s | 5 | 0.0 | Twice the push, twice the flow. | 0 |

**Gates the original failed (every judge):** 'ExamLeaf' spoken (b07, 69.16 s) and on screen (s05 at 69.4 s) (qa A12); 'ExamLeaf' spoken (b07, 69.16 s) and on screen (s05 from about 69.4 s; frames/s05_t014.png, s05_00435.png); AI-disclosure line spoken ('AI-generated narration', b07, 66.0 s) and on screen in s05 (PD-20); AI-disclosure line spoken and on screen (PD-20): b07 'AI-generated narration' from 66.0 s; the caption stays to the last frame (s05_t014); AI-disclosure line spoken and on screen: 'AI-generated narration; script by ExamLeaf' (b07, PD-20); board torn down inside the lesson at 22.4 s, 46.3 s and 57.4 s (five scene files; qa A17); board torn down inside the lesson at 22.4 s, 46.3 s and 57.4 s; 5 scene files (qa A17); board torn down inside the lesson: 5 scene files, diagram similarity 0.49 at 22.5 s, 0.43 at 46.5 s and 0.57 at 57.5 s (qa A17; frames s03_t000, s04_t000, s05_t002); duration 71.93 s outside 60 ± 1 s (qa A11).

**Judges' decisive differences, in their words:** teaching: one board from frame 0, a prediction answerable from the 0.20 A already shown, a solved 6 V → 0.60 A transfer; craft: colour-coded circuit from a complete first frame, reveals on their words and purposeful pauses, against three board wipes and a 5.5 s frozen hold; pull: usable idea by 7–8 s and a turn at least every 12 s, a named payoff, a transfer the learner solves and the shareable line "Twice the push, twice the flow", against nothing usable until 31.8 s and a close on the old disclosure line.

## 4. Scorecard

`tooling/scorecard.py` (0.5 machine checks + 0.5 judge means, weights D1 20, D2 20, D3 10, D4 15, D5 8, D6 5, D7 10, D8 12; releasable needs ≥ 85 with no gate failed and at least one judge verdict).

| | Before (Opus physics) | After, judged render | After, final cut |
|---|---|---|---|
| Gates (science, brand, prediction/transfer, persistence, silence+length, technical) | brand, prediction/transfer, persistence, silence+length **fail** | all pass | all pass |
| Total / 100 | **38.1** | 79.0 | **86.0** |
| Releasable (≥ 85, no gate failed) | no | no | **yes** (86.0; the one remaining machine flag is a 3.5 s still stretch at the formal statement, 0.5 s over the rule) |

The final cut (sha256 43c86e16…) differs from the judged render (66d6a0b4…) only by two emphasis halos at "ten ohms" and a calmer read of the free-lesson line; the judges' scores were not re-run for it.

**What the founder saw and decided after this comparison (17 Oct 2026):** the format itself should change: shorts become complete explainers without questions (PD-24) and the script must be told as a story (PD-25). The explainer rebuild is `demo/physics_v3_explainer/`; this document records the first, question-format round.

## 5. Honest limits

- One subject and one voice; chemistry and biology are smoke-tested on design system v2 but not yet narrated.
- The judges could not hear the audio; they judged narration from the script and word timings (the QA suite checked loudness and transcript).
- The Scribe transcript check hit the free tier's rate limit on the final run and was re-run separately.
- Pauses sit at the low end of their bands and the tempo is 0.98; a faster voice on the paid plan would restore the band middles.

## 6. The explainer (PD-24, PD-25): `demo/physics_v3_explainer/`

Built after the founder's second steer: a complete explainer told as a story, no pause questions. 13 beats, 120 words, one narration pass (the month's quota is now exhausted), rendered deterministically (1,771 frames; first cut sha256 261a47d4…, refined cut 6434bf1b… with the bulb handing back to the cool resistor on "cool"), 59.0 s at tempo 0.97.

| Measure | Explainer |
|---|---|
| Runtime | 59.0 s (pass) |
| Title question spoken by | 2.0 s |
| Dead time (PD-23a rule) | about 9 % (plan 8.7 %) |
| Visual changes per 10 s of speech | 5.2 |
| Checks pass / warn / fail (A1–A21, `--format explainer_60`) | first cut 17 / 2 / 2; refined cut 18 / 1 / 1 (transcript check skipped: the free account's STT returned 401) |
| Remaining flags | refined cut: A15 moves to the opening (4.5 s from 0.5 s: the hook's halos on the cell and the ammeter are below the detector's threshold while "tired cells dim your torch" is spoken; the method version opens differently, with the meter unknown and the first definition card, so the fix lives there); A19: three beats outside the per-beat band (warn). Closed since the first cut: the 6.5 s stretch at the bulb, the mid-tween A3 artefact. |

The script is the skill's story exemplar (`references/exemplar_ohms_law_explainer_script.json`). Blind judging of the explainer against the question version is the next comparison to run; the founder's preference for the explainer format is already the decision (PD-24).

## 7. The method version (PD-26, PD-27, PD-28): `demo/physics_v4_method/`

Rewritten three times on 17 Oct 2026 as the founder's direction sharpened: first to the "100 Seconds" method (12 beats, 125 words, 59.6 s planned), then to plain continuous speech after the founder judged the clipped lines "AI-generated" (PD-27), then to the fast, packed profile with the NCERT definition (PD-28). Final: 13 beats, 166 words (`pace: fast`, band 150–185), about 179 words per minute while speaking, planned 60.7 s at `rate_scale` 1.2 (to be measured on the first fast narration), planned silence 2.1 %; the NCERT §12.3 statement verbatim on a two-page sheet with the formula and its rearrangements beneath; three numeric cases on one board (2 V → 0.20 A, 4 V → 0.40 A, 20 Ω at 2 V → 0.10 A); the V–I straight line through the origin with its slope; the hot-filament exception; the claim line; "Try more cases in the free lesson." Checks: check_script OK (two expected warnings), check_pd_script OK with 0 register and 0 method warnings, compute OK, build lint ok with no gates, preview 0 errors, qa_scene PASS with purity 9/9, brand pass; no gap over 2.3 s between visible changes. Not narrated: the ElevenLabs free quota is exhausted until 15 Nov 2026; narration, render, QA and judging follow on the reset or the paid plan. For review: the NCERT figure number of the V–I graph is marked "to be confirmed" in its graph node.

**Preview voice (17 Oct 2026, PD-28a).** With the ElevenLabs quota exhausted, the method script was voiced locally with macOS `say` (Rishi, Indian English, `-r 170`, measured 175 wpm, tempo 1.03) through `narrate_preview.py` and rendered without the determinism pass: `demo/physics_v4_method_macvoice/render/phy-ohm-pd-04.mp4`, 59.5 s, 1,785 frames, errors 0. QA 15 pass / 3 warn / 2 fail / 1 skipped: A9 warns only because the determinism pass was skipped; A3 flagged a chip label whose words lost their space in the DOM text (check made whitespace-tolerant); A15 reported the opening still for 6.5 s; motion cues for "passes", "pushes" and "voltage" were added and the check learned to count coherent motion (PD-23b), after which the improved preview (sha256 7a8150cb…) reads 17 pass / 3 warn / 0 fail / 1 skipped; A19 warns on two beats above 215 wpm. The preview is labelled as such and is never released; the release voice re-runs the same chain.
