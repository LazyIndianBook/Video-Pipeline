# 09 · Video quality scorecard (Professor Diki Simplified, v1.0, 16 Oct 2026)

Status: defined; computed by `tooling/scorecard.py` from the QA report (machine checks A1–A21) and the blind judges' verdicts (D1–D8). The weights are house policy, not a validated instrument; they are revised when student validation data exists (10_ROADMAP.md).

## 1. Hard gates (any failure = not releasable, score not reported)

| Gate | Evidence | Check |
|---|---|---|
| Scientific accuracy | every spoken number traces to a fixture; every claim to a graph node with a source; no unresolved material error; subject reviewer sign-off | A3 (fixture = screen), A7 (transcript = script), judge D1 ≥ 4, human GA |
| Brand and disclosure | "Professor Diki Simplified" present; no "ExamLeaf" or forbidden strings on screen, spoken or in metadata; AI narration disclosed on the end card and in platform labels | A12, brand_check.py, human release check |
| Answerable prediction and transfer | the prediction's givens are shown before the window; a transfer question exists and is solvable with the rule taught | A18, judge D2 |
| Persistence | the diagram never tears down inside the lesson | A17 |
| Silence and length | silence ≤ 15 % of runtime; 60 ± 1 s for `concept_short_60` | A20, A11 |
| Technical | lint, cue sheets, loudness, flash, safe zones, byte-identical re-render, sync | A1, A2, A4, A5, A6, A9, A10 |

## 2. Weighted score (0–100; release threshold 85 with no failed gate)

| Dimension | Weight | Evidence (machine → judge) | 5 looks like |
|---|---|---|---|
| D1 Scientific accuracy | 20 | A3, A7 pass; judge D1 | no error; conditions and units stated; boundary of the model named |
| D2 Concept simplicity and pedagogy | 20 | A18; judge D2 | intuition before the term; prediction answerable; misconception confronted with evidence; transfer solved; a Class 8 reader could follow |
| D3 Script craft and voice | 10 | A19 wpm per beat, banned phrases; judge D3 | short sentences, contrastive emphasis, no stock phrases, Professor Diki register |
| D4 Visual explanation | 15 | A14, A15, A16, A17; judge D4 | board fills ≥ 45 %, every change has a causal role, identities persist, semantic colour, legible |
| D5 Sync and timing | 8 | A10, A13; judge D5 | reveals on their words; pauses by purpose; no dead time |
| D6 Technical conformance | 5 | A1–A9 | all pass |
| D7 Learner outcome (holistic) | 10 | judge D7 | "I understand and I can solve the next one" |
| D8 Momentum and motivation | 12 | A14 first insight ≤ 10 s, A15 change density, A20 silence share, A21 energy curve; judge D8 | pulled forward from the first second; payoff lands; close builds capability |

Computation: each dimension score = 0.5 × (machine sub-score, from its checks: pass 5, warn 3, fail 0, averaged) + 0.5 × (mean judge score over the panel), scaled to 0–5; weighted sum × 4 gives 0–100. Where no machine check exists for a dimension (D7), the judge score counts alone.

## 3. Measurable acceptance criteria (the numbers behind the gates)

| Criterion | Target | Source |
|---|---|---|
| Duration | 60.0 ± 1.0 s | A11 |
| Spoken words | 120–135 | check_script |
| Speaking rate per beat | 125–165 wpm (narration 150–160; formula and exception 125–140) | A19 |
| Silence share | ≤ 15 % | A20 |
| Pause compliance | every silence ≥ 0.3 s matches a scripted purpose within ±25 % | A13 |
| First usable idea | ≤ 10 s | A14 |
| Board visible | by 1.5 s | A14 |
| Change events during speech | ≥ 1 per 3 s; none > 3 s without change | A15 |
| Diagram fill | ≥ 45 % of frame height by the hero bounding box | A16 |
| Persistence | minimum consecutive-second similarity in the diagram area ≥ threshold except end card | A17 |
| Energy curve | ≥ 3 distinct marks; peak at reveal or transfer | A21 |
| Loudness | −16 ± 1 LUFS; true peak ≤ −1.5 dBTP | A6 |
| Transcript match | ≥ 0.97 after canonicalisation; no numeric mismatch | A7 |
| Brand | 0 forbidden strings; lockup and end card present | A12, brand_check |
| Determinism | byte-identical re-render | A9 |

## 4. Learner validation (not a score input until measured)

Formative sessions with 12–20 students across prerequisite levels: a novel numeric question immediately and a related one a week later; record where they pause, misread or form a wrong inference; publish no learning claim until measured (playbook §5.2, external audit §25).


**Measurement note (PD-23, 16 Oct 2026).** A20 counts pauses ≥ 0.45 s; A19's band scales with `voice.rate_scale` and warns before it fails; A16's hero floor is 70 % of the lane the scene uses; A3 honours `data-fx-dec`. The audit's historical silence numbers (0.3 s rule) are reported alongside the new rule in the before-vs-after comparison.
