# QA report: phy-ohm-pd-03 ( tier, format explainer_60)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "1 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 1771, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.4, "true_peak_dbtp": -1.3} |
| A7 transcript matches script (Scribe v2) | **skipped** | "no key or --no-stt" |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present (v2: think window judged by A13) | **pass** | {"wpm": 130, "total_s": 59.03333333333333, "spoken_s": 55.5, "think_windows": []} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 0} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 59.033, "timeline_s": 59.03333333333333, "first_scene_start": 0.0} |
| A11 duration 60 ± 1 s (concept_short_60) | **pass** | {"reasons": [], "duration_s": 59.03, "target_s": 60.0, "tolerance_s": 1.0, "format": "explainer_60"} |
| A12 brand: no forbidden string anywhere; end card | **pass** | {"reasons": [], "brand_check": {"status": "pass", "violations": 0, "scanned": {"spoken": 26, "on_screen": 1, "fixture": 30, "metadata": 4}}, "extra_sources_scanned": 32} |
| A13 pause policy by purpose (PD-01) | **pass** | {"reasons": [], "silences_ge_0_3": 22, "matched": [["b03", 1.02, "inspect"], ["b04", 0.56, "land"], ["b05", 0.53, "land"], ["b06", 0.99, "inspect"], ["b08", 0.55, "land"], ["b09", 0.59, "land"], ["b10", 0.55, "land"]], "failures_total": 0} |
| A14 first usable idea ≤ 10 s; board by 1.5 s | **pass** | {"reasons": [], "insight_beat": "b02", "insight_start_s": 5.035, "board_edge_at_1_5s": 0.1425, "empty_floor": 0.0984} |
| A15 change events: none > 3 s static during speech | **fail** | no visual change for 4.5 s from 0.5 s during speech (> 3 s) |
| A16 diagram never empty while speaking; hero fill | **pass** | {"reasons": [], "empty_floor": 0.0984, "empty_speech_s": 0, "empty_runs": [], "hero_height_px": [[14.8, 480, 584], [29.5, 480, 584], [44.3, 480, 584]], "hero_min_px": 409, "diagram_lane_px": 584} |
| A17 persistence: no teardown before the end card | **pass** | {"reasons": [], "min_similarity": 0.893, "min_similarity_t": 51.0, "end_card_from_s": 56.53, "threshold": 0.6} |
| A18 teaching order: predict with givens, transfer | **pass** | {"reasons": [], "slots": ["hook.question_reveal", "explain.definition", "explain.definition", "explain.mechanism", "explain.mechanism", "explain.formal", "explain.condition", "explain.condition", "explain.condition", "worked.step", "recap.statement", "close.next_step", "outro.brand"], "givens": null |
| A19 pace per beat 125–165 wpm | **warn** | (warn) b02 95 wpm outside 119–157; (warn) b03 158 wpm outside 119–157; (warn) b08b 170 wpm outside 119–157; (warn) b09 162 wpm outside 119–157; (warn) b10 161 wpm outside 119–157; (warn) b11 165 wpm outside 119–157 |
| A20 silence ≤ 15 % of runtime | **pass** | {"reasons": [], "silence_s": 4.79, "duration_s": 59.03, "share": 0.081} |
| A21 energy curve: ≥ 3 marks, peak at reveal/transfer | **pass** | {"reasons": [], "curve": [["b01", 4], ["b02", 3], ["b03", 3], ["b04", 3], ["b05", 5], ["b06", 2], ["b07", 4], ["b08", 3], ["b08b", 3], ["b09", 4], ["b10", 4], ["b11", 3], ["b12", 3]], "peak": 5} |
