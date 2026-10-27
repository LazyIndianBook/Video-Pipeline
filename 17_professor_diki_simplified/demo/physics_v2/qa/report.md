# QA report: phy-ohm-pd-02 ( tier, format concept_short_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "1 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 1776, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.8, "true_peak_dbtp": -1.3} |
| A7 transcript matches script (Scribe v2) | **pass** | {"match_ratio": 0.99, "diffs": [["replace", ["diki"], ["dickie"]]]} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present (v2: think window judged by A13) | **warn** | {"wpm": 113, "total_s": 59.2, "spoken_s": 54.3, "think_windows": []} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 0} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 59.2, "timeline_s": 59.2, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **pass** | {"reasons": [], "duration_s": 59.2, "target_s": 60.0, "tolerance_s": 1.0, "format": "concept_short_60"} |
| A12 brand: no forbidden string anywhere; end card | **pass** | {"reasons": [], "brand_check": {"status": "pass", "violations": 0, "scanned": {"spoken": 26, "on_screen": 1, "fixture": 36, "metadata": 4}}, "extra_sources_scanned": 33} |
| A13 pause policy by purpose (PD-01) | **pass** | {"reasons": [], "silences_ge_0_3": 22, "matched": [["b03", 0.46, "land"], ["b04", 1.8, "think_choice"], ["b05", 0.5, "land"], ["b07", 0.8, "inspect"], ["b09", 0.44, "land"], ["b10", 2.66, "think_calc"], ["b11", 0.45, "land"]], "failures_total": 0} |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **pass** | {"reasons": [], "insight_beat": "b03", "insight_start_s": 8.065, "board_edge_at_1_5s": 0.14555, "empty_floor": 0.0829} |
| A15 change events: none > 3 s static during speech | **fail** | no visual change for 3.5 s from 22.5 s during speech (> 3 s) |
| A16 diagram never empty while speaking; hero fill | **pass** | {"reasons": [], "empty_floor": 0.0829, "empty_speech_s": 0, "empty_runs": [], "hero_height_px": [[14.8, 480, 584], [29.6, 480, 584], [44.4, 480, 584]], "hero_min_px": 409, "diagram_lane_px": 584} |
| A17 persistence: no teardown before the end card | **pass** | {"reasons": [], "min_similarity": 0.89, "min_similarity_t": 36.0, "end_card_from_s": 56.7, "threshold": 0.6} |
| A18 teaching order: predict with givens, transfer | **pass** | {"reasons": [], "slots": ["hook.question_reveal", "explain.givens", "explain.givens", "check.predict", "reveal.answer", "explain.mechanism", "explain.formal", "exam.language", "misconception.confront", "check.transfer", "feedback.transfer", "close.next_step", "outro.brand"], "givens": ["parameters.v |
| A19 pace per beat 125–165 wpm | **warn** | (warn) b01 99 wpm outside 102–135; (warn) b02 97 wpm outside 102–135; (warn) b10 141 wpm outside 102–135; (warn) b11 166 wpm outside 102–135; (warn) b13 174 wpm outside 102–135 |
| A20 silence ≤ 15 % of runtime | **pass** | {"reasons": [], "silence_s": 8.31, "duration_s": 59.2, "share": 0.14} |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **pass** | {"reasons": [], "curve": [["b01", 4], ["b02", 3], ["b03", 3], ["b04", 4], ["b05", 5], ["b06", 3], ["b07", 2], ["b08", 3], ["b09", 4], ["b10", 4], ["b11", 5], ["b13", 3], ["b14", 3]], "peak": 5} |
