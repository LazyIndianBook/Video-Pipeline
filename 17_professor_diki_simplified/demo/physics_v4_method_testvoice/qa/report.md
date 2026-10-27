# QA report: phy-ohm-pd-04 (physics_v4_method_testvoice tier, format explainer_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "1 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 1806, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.4, "true_peak_dbtp": -1.3} |
| A7 transcript matches script (local Whisper) | **pass** | {"match_ratio": 0.988, "diffs": [["replace", ["volts"], ["volt"]], ["replace", ["resistance"], ["resistant"]]]} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present (v2: think window judged by A13) | **warn** | {"wpm": 165, "total_s": 60.2, "spoken_s": 60.5, "think_windows": []} |
| A9 render: no scene errors, injected sources, re-render determinism | **warn** | {"errors": 0, "sources_injected": true, "deterministic": false, "warnings": 0} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 60.2, "timeline_s": 60.2, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **pass** | {"reasons": [], "duration_s": 60.2, "target_s": 60.0, "tolerance_s": 1.0, "format": "explainer_60"} |
| A12 brand: no forbidden string anywhere; end card | **pass** | {"reasons": [], "brand_check": {"status": "pass", "violations": 0, "scanned": {"spoken": 26, "on_screen": 1, "fixture": 56, "metadata": 4}}, "extra_sources_scanned": 34} |
| A13 pause policy by purpose (PD-01) | **pass** | {"reasons": [], "silences_ge_0_3": 9, "matched": [["b07", 0.46, "land"], ["b11", 0.44, "land"]], "failures_total": 0} |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **pass** | {"reasons": [], "insight_beat": "b02", "insight_start_s": 9.625, "board_edge_at_1_5s": 0.12944, "empty_floor": 0.1017} |
| A15 change events: none > 3 s static during speech | **pass** | {"reasons": [], "longest_static_s": 2.0, "longest_static_from_s": 0.5, "changes": 108, "changes_per_10s": 19.29, "change_threshold": 0.0015} |
| A16 diagram never empty while speaking; hero fill | **pass** | {"reasons": [], "empty_floor": 0.1017, "empty_speech_s": 0, "empty_runs": [], "hero_height_px": [[15.1, 480, 584], [30.1, 480, 584], [45.2, 480, 584]], "hero_min_px": 409, "diagram_lane_px": 584} |
| A17 persistence: no teardown before the end card | **pass** | {"reasons": [], "min_similarity": 0.798, "min_similarity_t": 18.0, "end_card_from_s": 57.88, "threshold": 0.6} |
| A18 teaching order: predict with givens, transfer | **pass** | {"reasons": [], "slots": ["hook.question_reveal", "explain.definition", "explain.definition", "explain.definition", "explain.formal", "explain.mechanism", "explain.mechanism", "worked.step", "explain.condition", "explain.condition", "recap.statement", "close.next_step", "outro.brand"], "givens": nul |
| A19 pace per beat 125–165 wpm | **warn** | (warn) b12 240 wpm outside 150–215 |
| A20 silence ≤ 15 % of runtime | **pass** | {"reasons": [], "silence_s": 0.46, "duration_s": 60.2, "share": 0.008} |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **pass** | {"reasons": [], "curve": [["b01", 4], ["b02", 3], ["b03", 3], ["b04", 3], ["b05", 2], ["b06", 4], ["b07", 5], ["b08", 4], ["b09", 3], ["b10", 4], ["b11", 4], ["b12", 3], ["b13", 3]], "peak": 5} |
