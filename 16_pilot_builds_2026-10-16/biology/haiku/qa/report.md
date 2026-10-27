# QA report: bio-photosyn-ci-01 (haiku tier)

| Check | Status | Detail |
|---|---|---|
| A1 seek-contract lint level 1 | **pass** | "5 scenes ok" |
| A2 cue sheets valid (production) | **pass** | "all valid" |
| A3 on-screen science text equals fixture | **pass** | "every [data-fx] element matches" |
| A4 safe zones (text inside zones, side margin) | **pass** | "no critical or major finding" |
| A5 flash test (luminance deltas, 3 Hz rule) | **pass** | {"frames": 2045, "verdict": "pass", "summary": {}} |
| A6 loudness −16 LUFS ±1, true peak ≤ −1 dBTP | **pass** | {"integrated_lufs": -16.8, "true_peak_dbtp": -1.5} |
| A7 transcript matches script (Scribe v2) | **pass** | {"match_ratio": 0.989, "diffs": [["replace", ["eighteen"], ["18"]], ["delete", ["percent"], []]]} |
| A8 pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present | **pass** | {"wpm": 141, "total_s": 68.16666666666667, "spoken_s": 57.4, "think_windows": [["b02", 5.0]]} |
| A9 render: no scene errors, injected sources, re-render determinism | **pass** | {"errors": 0, "sources_injected": true, "deterministic": true, "warnings": 3} |
| A10 video length equals narration timeline (±1 frame) | **pass** | {"video_s": 68.167, "timeline_s": 68.16666666666667, "first_scene_start": 0.0} |
