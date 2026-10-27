# QA report: phy-ohm-ci-01 (haiku tier, format concept_short_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "5 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 2216, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.9, "true_peak_dbtp": -1.4} |
| A7 transcript matches script (Scribe v2) | **pass** | {"match_ratio": 0.993, "diffs": [["replace", ["'always'"], ["always"]]]} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present | **pass** | {"wpm": 139, "total_s": 73.86666666666666, "spoken_s": 62.6, "think_windows": [["b02", 5.0]]} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 0} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 73.867, "timeline_s": 73.86666666666666, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **fail** | duration 73.87 s outside 60.0 ± 1.0 s |
| A12 brand: no forbidden string anywhere; end card | **fail** | forbidden 'ExamLeaf' (F01) in spoken script.json#b07; forbidden 'ExamLeaf' (F01) in spoken narration/timeline.json#b07; missing end-card item header_lockup_text; missing end-card item end_card.brand_line; missing end-card item end_card.disclosure_line[B]; missing end-card item end_card.free_lesson_line (+4 more) |
| A13 pause policy by purpose (PD-01) | **fail** | script has no pauses[] with purpose labels (legacy pause_after_s/think_window_s); unscripted silence 0.00–0.71 s (0.71 s) > 0.6 s; unscripted silence 9.17–10.01 s (0.84 s) > 0.6 s; unscripted silence 14.78–20.58 s (5.80 s) > 0.6 s; unscripted silence 31.44–32.55 s (1.12 s) > 0.6 s; unscripted silence 43.29–44.38 s (1.09 s) > 0.6 s (+3 more) |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **fail** | no insight_beat declared; first explain beat b03 starts at 20.6 s |
| A15 change events: none > 3 s static during speech | **fail** | no visual change for 8.0 s from 27.5 s during speech (> 3 s) |
| A16 diagram never empty while speaking; hero fill | **fail** | diagram lane empty for 5.5 s from 44.5 s while speaking; diagram lane empty for 6.5 s from 56.0 s while speaking; no visible hero (Diki.hero / [data-role=hero]) at 18.5 s; no visible hero (Diki.hero / [data-role=hero]) at 36.9 s; no visible hero (Diki.hero / [data-role=hero]) at 55.4 s |
| A17 persistence: no teardown before the end card | **fail** | 5 scene files (PD-03: one persistent scene); diagram similarity 0.59 at 10.0 s < 0.60 (teardown); diagram similarity 0.00 at 20.5 s < 0.60 (teardown); diagram similarity 0.01 at 44.5 s < 0.60 (teardown); diagram similarity 0.00 at 56.0 s < 0.60 (teardown) |
| A18 teaching order: predict with givens, transfer | **fail** | missing slot reveal.answer; missing slot check.transfer; missing slot feedback.transfer; missing slot close.next_step; missing slot outro.brand; check.predict b02: given parameters.resistance_ohm = 10 is not spoken by then |
| A19 pace per beat 125–165 wpm | **fail** | b01 167 wpm outside 125–165; b06 122 wpm outside 125–165; b07 74 wpm outside 125–165 |
| A20 silence ≤ 15 % of runtime | **fail** | silence 23.0% of runtime > 15% |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **fail** | no energy marks in script (beats[].energy absent) |
