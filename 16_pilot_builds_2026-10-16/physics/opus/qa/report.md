# QA report: phy-ohm-ci-01 (opus tier, format concept_short_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "5 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 2158, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.9, "true_peak_dbtp": -1.5} |
| A7 transcript matches script (Scribe v2) | **pass** | {"match_ratio": 1.0, "diffs": []} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present | **pass** | {"wpm": 139, "total_s": 71.93333333333334, "spoken_s": 60.7, "think_windows": [["b02", 5.0]]} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 0} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 71.933, "timeline_s": 71.93333333333334, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **fail** | duration 71.93 s outside 60.0 ± 1.0 s |
| A12 brand: no forbidden string anywhere; end card | **fail** | forbidden 'ExamLeaf' (F01) in spoken script.json#b07; forbidden 'disclosure line (Path B)' (PD-20) in spoken script.json#b07; forbidden 'ExamLeaf' (F01) in spoken narration/timeline.json#b07; forbidden 'disclosure line (Path B)' (PD-20) in spoken narration/timeline.json#b07; missing end-card item opening_ident_text; missing end-card item end_card.brand_line (+5 more) |
| A13 pause policy by purpose (PD-01) | **fail** | script has no pauses[] with purpose labels (legacy pause_after_s/think_window_s); unscripted silence 0.00–0.71 s (0.71 s) > 0.6 s; unscripted silence 4.00–4.65 s (0.66 s) > 0.6 s; unscripted silence 8.15–8.76 s (0.61 s) > 0.6 s; unscripted silence 10.47–11.38 s (0.91 s) > 0.6 s; unscripted silence 17.00–22.50 s (5.51 s) > 0.6 s (+5 more) |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **fail** | no insight_beat declared; first explain beat b03 starts at 22.6 s; diagram lane empty at 1.5 s (edge density 0.049 < 0.055) |
| A15 change events: none > 3 s static during speech | **fail** | no visual change for 4.0 s from 13.5 s during speech (> 3 s) |
| A16 diagram never empty while speaking; hero fill | **fail** | diagram lane empty for 3.0 s from 1.0 s while speaking; diagram lane empty for 1.5 s from 58.0 s while speaking; no visible hero (Diki.hero / [data-role=hero]) at 18.0 s; no visible hero (Diki.hero / [data-role=hero]) at 36.0 s; no visible hero (Diki.hero / [data-role=hero]) at 53.9 s |
| A17 persistence: no teardown before the end card | **fail** | 5 scene files (PD-03: one persistent scene); diagram similarity 0.49 at 22.5 s < 0.60 (teardown); diagram similarity 0.43 at 46.5 s < 0.60 (teardown); diagram similarity 0.57 at 57.5 s < 0.60 (teardown) |
| A18 teaching order: predict with givens, transfer | **fail** | missing slot reveal.answer; missing slot check.transfer; missing slot feedback.transfer; missing slot close.next_step; missing slot outro.brand |
| A19 pace per beat 125–165 wpm | **fail** | b07 75 wpm beyond ±30 % of 125–165 |
| A20 silence ≤ 15 % of runtime | **fail** | silence 17.5% of runtime > 15% |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **fail** | no energy marks in script (beats[].energy absent) |
