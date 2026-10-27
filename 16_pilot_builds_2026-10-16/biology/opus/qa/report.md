# QA report: bio-photosyn-ci-01 (opus tier, format concept_short_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "5 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 2013, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.7, "true_peak_dbtp": -1.4} |
| A7 transcript matches script (Scribe v2) | **pass** | {"match_ratio": 1.0, "diffs": []} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present | **pass** | {"wpm": 150, "total_s": 67.1, "spoken_s": 56.4, "think_windows": [["b02", 5.0]]} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 1} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 67.1, "timeline_s": 67.1, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **fail** | duration 67.10 s outside 60.0 ± 1.0 s |
| A12 brand: no forbidden string anywhere; end card | **fail** | forbidden 'ExamLeaf' (F01) in spoken script.json#b07; forbidden 'disclosure line (Path B)' (PD-20) in spoken script.json#b07; forbidden 'ExamLeaf' (F01) in spoken narration/timeline.json#b07; forbidden 'disclosure line (Path B)' (PD-20) in spoken narration/timeline.json#b07; missing end-card item opening_ident_text; missing end-card item end_card.brand_line (+5 more) |
| A13 pause policy by purpose (PD-01) | **fail** | script has no pauses[] with purpose labels (legacy pause_after_s/think_window_s); unscripted silence 0.00–0.70 s (0.70 s) > 0.6 s; unscripted silence 6.09–6.90 s (0.81 s) > 0.6 s; unscripted silence 13.62–18.87 s (5.25 s) > 0.6 s; unscripted silence 27.32–28.09 s (0.76 s) > 0.6 s; unscripted silence 38.83–39.91 s (1.08 s) > 0.6 s (+3 more) |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **fail** | no insight_beat declared; first explain beat b03 starts at 18.9 s |
| A15 change events: none > 3 s static during speech | **pass** | {"reasons": [], "longest_static_s": 2.5, "longest_static_from_s": 49.5, "changes": 61, "changes_per_10s": 10.8, "change_threshold": 0.0015} |
| A16 diagram never empty while speaking; hero fill | **fail** | diagram lane empty for 2.5 s from 7.0 s while speaking; diagram lane empty for 2.5 s from 19.0 s while speaking; diagram lane empty for 7.0 s from 40.5 s while speaking; no visible hero (Diki.hero / [data-role=hero]) at 16.8 s; no visible hero (Diki.hero / [data-role=hero]) at 33.5 s; no visible hero (Diki.hero / [data-role=hero]) at 50.3 s |
| A17 persistence: no teardown before the end card | **fail** | 5 scene files (PD-03: one persistent scene); diagram similarity 0.12 at 7.0 s < 0.60 (teardown); diagram similarity 0.01 at 18.5 s < 0.60 (teardown); diagram similarity 0.00 at 40.0 s < 0.60 (teardown); diagram similarity 0.07 at 52.5 s < 0.60 (teardown) |
| A18 teaching order: predict with givens, transfer | **fail** | missing slot reveal.answer; missing slot check.transfer; missing slot feedback.transfer; missing slot close.next_step; missing slot outro.brand; check.predict b02 declares no givens |
| A19 pace per beat 125–165 wpm | **fail** | b07 77 wpm beyond ±30 % of 125–165; (warn) b01 204 wpm outside 125–165; (warn) b02 166 wpm outside 125–165 |
| A20 silence ≤ 15 % of runtime | **fail** | silence 16.8% of runtime > 15% |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **fail** | no energy marks in script (beats[].energy absent) |
