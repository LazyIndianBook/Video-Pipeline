# 13 · End-to-end walkthrough: one doodle Reel and one data-bound lesson scene

**Purpose.** Two fully worked examples showing the exact artefacts at each step: (A) a 30-second doodle-style Reel built on backlog item CSV ID 2, "Which line has the larger resistance? Check the axes." (`01_business_model/REEL_BACKLOG_36.md`); (B) one data-bound lesson scene, the Ohm's-law I–V graph at 05:00–05:55 of `02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md`.

**Status.** [PROPOSED] and **illustrative**. All timings, hashes, IDs and resource names below are placeholders unless marked otherwise; real values come from the accepted narration, the approval service and the platform. The narration lines are **drafts**: every spoken word must be written under S5 rules and approved by the academic owner (GA) before synthesis. Commands that do not exist yet are shown as `<placeholder — verify>`. Two stdlib-only checks used here were run locally on 14 Oct 2026 and are marked [RUN LOCALLY].

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V#], [V4-MP], [N#], ROOT-relative project paths, [Recommendation]/[Hypothesis], master edge cases #1–#65, NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`. Checks A1–A17 and gates H-SB, H-RV, GA, GF, GS are defined in `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`.

**Shared science** (from the blueprint's organiser cross-checks, `02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md` §C–§D): the opening model is the same 10 Ω resistor at constant temperature, 2 V → 0.2 A and 4 V → 0.4 A; a steeper I-versus-V line means smaller resistance; the blueprint leaves the second line's resistance unspecified ("any R below 10 Ω"). Both examples use **5 Ω** for the steeper line — a value the academic owner must confirm in the fixture (ambiguity D.1 in the blueprint).

---

## Part A · A 30-second doodle-style Reel (CSV ID 2)

### A.0 Preconditions

| Precondition | Where it comes from | Why |
|---|---|---|
| The source lesson (Ohm's law and I–V graphs) is GF-approved | `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` scope | Shorts come from approved lessons only |
| Backlog row CSV ID 2: Class 10, Physics, "I-V graph interpretation"; visual "Two labelled I-versus-V lines; compare current at the same voltage."; caption first line "The axes decide what this slope means."; CTA "Try the three-question graph check."; objective Practice; 30 s; check "Keep I vertical and V horizontal throughout."; P0 | `01_business_model/REEL_BACKLOG_36.md` §2 | Hook, payoff, check |
| Style: `doodle-handdrawn` (cheapest house style, no credits) | Report §4.2 [Recommendation]; `12_advanced_animations_with_claude/05_style_guides/` | Default illustrative style for Reels |
| Launch locale en-IN | RD-26 | No Indic text in this Reel |

### A.1 Step 1 — ShortSpec (`shorts/reel-002-iv-axes/ShortSpec.json`)

Fields per `07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §3.11.

```json
{
  "id": "reel-002-iv-axes",
  "source_lesson_id": "<approved lesson id, e.g. phy10_electricity_ohms_law>",
  "source_claim_ids": ["<clm_ohm_relationship>", "<clm_iv_slope_is_1_over_R>", "<clm_ohmic_condition>"],
  "target_seconds": 30,
  "hook": "Which line has the larger resistance? Check the axes.",
  "complete_payoff": "At the same voltage, 4 V, line B carries less current (0.4 A) than line A (0.8 A), so R = V/I is larger for B. On an I-versus-V graph the less steep line has the larger resistance.",
  "retained_conditions": [
    "I on the vertical axis, V on the horizontal axis, throughout",
    "Ohmic resistors at constant temperature",
    "Compare currents at the same voltage"
  ],
  "destination_resource_id": "<platform resource id of the three-question graph check>",
  "access_tier": "free",
  "layout_strategy": "reflow",
  "approval_status": "pending"
}
```

*`access_tier` and `destination_resource_id` above: (15 Oct 2026) Retired from the pipeline contract under RD-49 and CE-68: the platform attaches entitlement outside the pipeline; removal from the 04 code is P1-01.*

Automated check: `ShortSpec` validation (20–60 s, `reflow`, ≥ 1 claim) [TESTED as a schema].

### A.2 Step 2 — Draft script (new wording → GA required)

Structure from SH5 (0–3 s hook; 3–8 s tempting error and prediction; 8–30 s complete explanation; final CTA). Pacing targets: hook ≈ 150–155 wpm, body ≈ 145 wpm (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §5).

| Segment | Draft line (spoken) | Words | Planned window | Pause after |
|---|---|---:|---|---|
| `s1_hook` | "Which line has the larger resistance? Check the axes." | 9 | 0.0–3.4 s | beat (≈ 0.3 s) |
| `s2_tempt` | "Most people pick the steeper line. Lock in your answer." | 10 | 3.4–6.4 s | `think` 1.0 s (Reel THINK 0.8–1.2 s, playbook §5) |
| `s3_payoff` | "Current is up the side, voltage along the bottom. Pick one voltage: four volts. Line A gives zero point eight amps. Line B gives zero point four. Same voltage, less current, so R equals V over I is larger. B, the less steep line, has the larger resistance." | 48 | 7.4–22.6 s speech; answer state held to 26.9 s | — |
| `s4_cta` | "Try the three-question graph check." | 6 | 27.0–28.9 s | end-card hold to 30.0 s |

Notes:
- `s3_payoff` is 48 words in about 15 s of speech plus internal pauses. **`examleaf-pacing-controller` measures the real rate**; if the measured body rate exceeds the house range, cut words — never speed the audio (03 S16 forbidden repair; NEW-29).
- The tempting error ("steeper always means more resistance") is the blueprint's misconception at 06:35–06:50.
- The script names the condition implicitly through the axes; the ohmic condition stays visible on screen (retained condition).
- Spoken numbers use the lexicon (`examleaf-stem-pronunciation`): "zero point eight amps", "four volts", "R equals V over I".

⛔ **GA** for the changed wording (SH4: "the changed wording needs academic approval").

### A.3 Step 3 — Fixture (`shorts/reel-002-iv-axes/anim/fixtures/fx_iv_two_lines_v1.json`)

```json
{
  "fixture_id": "fx_iv_two_lines_v1",
  "claim_ids": ["<clm_iv_slope_is_1_over_R>", "<clm_ohmic_condition>"],
  "axes": {
    "x": {"quantity": "V", "label": "Voltage, V", "unit": "V", "min": 0, "max": 6, "ticks": [0, 2, 4, 6]},
    "y": {"quantity": "I", "label": "Current, I", "unit": "A", "min": 0, "max": 1.2, "ticks": [0, 0.4, 0.8, 1.2]}
  },
  "lines": [
    {"id": "line_A", "label": "A", "resistance_ohm": 5,  "stroke": "solid"},
    {"id": "line_B", "label": "B", "resistance_ohm": 10, "stroke": "dashed"}
  ],
  "probe": {"V": 4, "I_line_A": 0.8, "I_line_B": 0.4},
  "relation_text": "R = V / I",
  "condition_text": "Ohmic resistors, constant temperature",
  "answer": {"larger_resistance_line": "line_B"},
  "seed": 2024
}
```

- Lines differ by **stroke pattern and label**, not colour alone (`02_learning_psychology/INSTRUCTIONS_production_rules.md` D4).
- Same axes ranges as the lesson scene in Part B, so a viewer who follows the CTA sees the same graph.
- Validated by a bounded validator (pattern in §B.3) before rendering (A12a).

### A.4 Step 4 — Brief (`shorts/reel-002-iv-axes/anim/brief.md`, excerpt)

Assembled by `12_advanced_animations_with_claude/03_skills/examleaf-anim-brief/` from templates in `12_advanced_animations_with_claude/06_prompts_and_templates/`.

```text
SCENE: reel-002-iv-axes / single scene, 30.0 s, 900 frames, 1080x1920, 30 fps
ROUTE: layer 1 data-bound (axes, lines, probe, readouts, R = V/I, condition tag)
       layer 2 illustrative-narrative (doodle paper, pencil character, arrows, "?", sparkles)
       layer 3 typographic (hook question in handwriting mode; CTA card)
STYLE: doodle-handdrawn v1 (12_advanced_animations_with_claude/05_style_guides/doodle-handdrawn.md; tokens: style_tokens.json)
TIMING: read every time from cue_sheet.json; never hard-code times.
DATA: fixtures/fx_iv_two_lines_v1.json is read-only. Do not type any scientific value, label or unit.
DOODLE RULE: wobble/boil only on layer 2. Layer-1 strokes are exact (wobble amplitude 0) and may use the
             pencil texture only as fill/stroke texture. No camera moves while any data-fx element is revealed or held.
TEXT: hook in handwriting mode (mask wipe), CTA card; science text in house fonts; essential text >= 50 px.
SAFE ZONES: tools/ copy of 12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json; nothing in the caption reserve.
HOLDS: hook title >= 1.2 s; R = V/I visible until narration end + 0.5 s; answer state >= 2 s.
CONTRACT: 12_advanced_animations_with_claude/04_harness_contract/contract.md (window.DURATION, async window.seek(t), seeded PRNG, cue loader).
LIMITS: Opus 5.5, effort high, max 3 creative rounds, max 2 failed repairs; stop and report rubric.
ISOLATION: do not read any folder outside this workspace.
AUDIO: no music under s3_payoff; SFX list in cue_sheet.sfx.
```

### A.5 Step 5 — Storyboard grid and estimate (⛔ H-SB)

Code-rendered thumbnails (free) in beat order, 3×3, at `shorts/reel-002-iv-axes/anim/storyboard/grid.png`:

| Panel | Time | Content |
|---|---|---|
| 1 | 0.1 s | Cream notebook paper; handwritten "Which line has the larger resistance?" |
| 2 | 0.3 s | Graph draws on: axes with labels "Current, I (A)" and "Voltage, V (V)"; lines A (solid) and B (dashed) |
| 3 | 2.6 s | Axis labels pulse ("Check the axes") |
| 4 | 4.3 s | Pencil character points at steeper line A with a doodle "?" |
| 5 | 6.4 s | Stable frame, prompt "Lock in your answer" (think hold) |
| 6 | 11.1 s | Vertical probe line at V = 4 V |
| 7 | 13.2–15.0 s | Readouts: A 0.8 A, B 0.4 A |
| 8 | 17.7–20.2 s | "R = V / I"; line B highlighted; tag "larger R" |
| 9 | 27.0 s | CTA card "Try the three-question graph check" |

`estimate.json` (from `examleaf-effort-governor`, doc 09 §11):

```json
{"scene_count": 1, "task": "scene_code", "model": "claude-opus-5-5", "effort": "high",
 "rounds_cap": 3, "repair_cap": 2,
 "token_cap": 78000, "token_cap_basis": "provisional per-scene ceiling (doc 09 §10) [Hypothesis]",
 "credits": 0, "generated_video_seconds": 0, "render_box": "linux-render-01"}
```

⛔ Storyboard gate (`12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md`): for pilots the founder approves the cost and the academic lead approves fit with the approved script, including the data-bound panels; the record is bound to the grid, `beats.json` and `estimate.json` hashes in the approval service.

### A.6 Step 6 — Narration and timeline

1. Compile and synthesise through `examleaf-voice-synthesis` → `examleaf-tts-provider-adapter` with the approved `VoiceIdentity` and lexicon version (04 N6–N8).
2. ASR and critical-term review (N9): "zero point eight", "zero point four", "R equals V over I".
3. Forced alignment (N10) → `audio/alignment.json`.
4. Timeline (N11) → `shorts/reel-002-iv-axes/audio/timeline.json` (sample-exact at 48 kHz, events converted once to frames).

Excerpt of the timeline (illustrative values):

```json
{"lesson_id": "reel-002-iv-axes", "sample_rate": 48000, "fps_num": 30, "fps_den": 1,
 "total_samples": 1440000, "duration_seconds": 30.0, "audio_sha256": "<64 hex>",
 "events": [
   {"cue_id": "c_axes",    "sample": 128640,  "frame": 80,  "action": "highlight", "element_id": "axis_labels", "segment_id": "s1_hook"},
   {"cue_id": "c_answerB", "sample": 969600,  "frame": 606, "action": "reveal-answer", "element_id": "line_B", "segment_id": "s3_payoff"}
 ],
 "pauses": [{"segment_id": "s2_tempt", "start_sample": 307200, "end_sample": 355200, "kind": "think", "prompt": "Lock in your answer."}],
 "contains_fixture": false}
```

The `reveal-answer` at frame 606 (≈ 20.2 s) is after the think pause ends at sample 355,200 (7.4 s), so "Premature answer" does not fire.

### A.7 Step 7 — Cue sheet (`shorts/reel-002-iv-axes/anim/reel-002-iv-axes/cue_sheet.json`)

Built by `examleaf-cue-sheet` (doc 06 §5.3) to the schema in `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`. Reveals sit at `t0 − 0.05 s`, the template default (contract §8). `words[]` is abbreviated to the cue-bearing words; the real file lists every aligned word. `script_sha256` is the SHA-256 of the draft script in §A.2; `narration_audio_sha256` hashes a stand-in string because no audio exists, as the section's own example does. `alignment_source: "example"` marks it as non-production.

[RUN LOCALLY] `python3 12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py cue_sheet.json` → `VALID (0 errors, 0 warnings)`; with `--production` it is correctly rejected (`'example' is not valid for production`).

```json
{
  "schema_version": "1.0",
  "scene_id": "reel-002-iv-axes",
  "fps": 30,
  "duration": 30.0,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": "158aa65ea5fc401fdf6075d93d5076f4d999d69261ed628e5f8364efed8a29d9",
  "script_sha256": "209a622e6fb5aa74730dedcbba892d218c046b9779c925665e67ea130d4fdd3f",
  "words": [
    {"w": "Which", "t0": 0.12, "t1": 0.34},
    {"w": "line", "t0": 0.34, "t1": 0.58},
    {"w": "axes", "t0": 2.68, "t1": 3.2},
    {"w": "steeper", "t0": 4.38, "t1": 4.8},
    {"w": "Current", "t0": 7.6, "t1": 8.05},
    {"w": "voltage", "t0": 8.75, "t1": 9.25},
    {"w": "four", "t0": 11.1, "t1": 11.35, "occurrence": 1},
    {"w": "eight", "t0": 13.25, "t1": 13.55},
    {"w": "four", "t0": 15.05, "t1": 15.45, "occurrence": 2},
    {"w": "R", "t0": 17.75, "t1": 17.9},
    {"w": "I", "t0": 18.75, "t1": 18.9},
    {"w": "B", "t0": 20.2, "t1": 20.4},
    {"w": "resistance", "t0": 21.85, "t1": 22.6},
    {"w": "Try", "t0": 27.0, "t1": 27.2},
    {"w": "check", "t0": 28.4, "t1": 28.85}
  ],
  "beats": [0.0, 0.6, 1.2, 1.8, 2.4, 3.0, 3.6, 4.2, 27.6, 28.2, 28.8, 29.4],
  "cues": [
    {"id": "hook_title", "at": 0.07, "kind": "reveal", "element_id": "hook_title", "word_index": 0},
    {"id": "graph_draw", "at": 0.29, "kind": "reveal", "element_id": "graph", "word_index": 1},
    {"id": "axis_labels", "at": 2.63, "kind": "emphasis", "element_id": "axis_labels", "word_index": 2},
    {"id": "doodle_point", "at": 4.33, "kind": "reveal", "element_id": "doodle_point", "word_index": 3},
    {"id": "think_prompt", "at": 6.4, "kind": "hold", "element_id": "think_prompt", "until": 7.4},
    {"id": "axis_y", "at": 7.55, "kind": "emphasis", "element_id": "axis_y", "word_index": 4},
    {"id": "axis_x", "at": 8.7, "kind": "emphasis", "element_id": "axis_x", "word_index": 5},
    {"id": "probe_v4", "at": 11.05, "kind": "reveal", "element_id": "probe_v4", "word_index": 6},
    {"id": "readout_A", "at": 13.2, "kind": "reveal", "element_id": "readout_A", "word_index": 7},
    {"id": "readout_B", "at": 15.0, "kind": "reveal", "element_id": "readout_B", "word_index": 8},
    {"id": "relation_R", "at": 17.7, "kind": "reveal", "element_id": "relation_R", "word_index": 9},
    {"id": "relation_R_hold", "at": 17.7, "kind": "hold", "element_id": "relation_R", "until": 30.0},
    {"id": "answer_B", "at": 20.2, "kind": "emphasis", "element_id": "line_B", "word_index": 11},
    {"id": "answer_hold", "at": 20.2, "kind": "hold", "element_id": "line_B", "until": 26.95},
    {"id": "cta_card", "at": 26.95, "kind": "reveal", "element_id": "cta_card", "word_index": 13}
  ],
  "sfx": [
    {"file": "audio/sfx/pencil_scratch.wav", "at": 0.29, "gain_db": -18},
    {"file": "audio/sfx/tap.wav", "at": 2.63, "gain_db": -20},
    {"file": "audio/sfx/pop.wav", "at": 4.33, "gain_db": -18},
    {"file": "audio/sfx/tick.wav", "at": 11.05, "gain_db": -22},
    {"file": "audio/sfx/chime.wav", "at": 20.2, "gain_db": -16},
    {"file": "audio/sfx/pop.wav", "at": 26.95, "gain_db": -18}
  ],
  "meta": {"note": "ILLUSTRATIVE. words[] abbreviated to the cue-bearing words; timings not aligned to real audio; wording is a draft pending GA.", "script_sha256_of": "UTF-8 bytes of the draft script in doc 13 section A.2 (segments joined by single spaces)", "narration_audio_sha256_of": "UTF-8 bytes of the string 'EXAMPLE-NO-AUDIO-FILE reel-002-iv-axes'", "answer_protection": {"timeline_reveal_answer_element": "line_B", "think_pause_end_s": 7.4, "offset_rule": "reveal-answer cues use offset 0 (examleaf-cue-sheet rule)"}, "mood_segments": [{"from_s": 0.0, "to_s": 4.8, "mood": "curious"}, {"from_s": 4.8, "to_s": 27.6, "mood": "core_explanation"}, {"from_s": 27.6, "to_s": 30.0, "mood": "warm_end"}]}
}
```

Notes:
- Cue kinds come from the schema enum (`reveal`, `emphasis`, `transition`, `hold`, `marker`). The schema has no "answer" kind, so answer protection is checked against the narration timeline's `reveal-answer` event on `line_B` (§A.6), recorded in `meta.answer_protection` (doc 06 §5.3 step 6). The answer emphasis on `line_B` uses offset 0 (`at` = `t0` = 20.20 s), as `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/` requires for answer reveals, and is long after the think pause ends at 7.40 s.
- `hold` cues carry `until`: `relation_R` stays from 17.70 s to the end (narration of it ends ≈ 18.9 s, so the equation rule needs ≥ 19.4 s); the answer state is held 20.20–26.95 s.
- Beats exist only where the bed plays (hook and CTA); music is off in the body (`meta.mood_segments`). One correct-answer sting (the chime) — within the Reel's 0–1 budget (playbook §5).
- 30.0 s × 30 fps = 900 frames.

### A.8 Step 8 — Scene code outline (against the harness contract)

Outline only; the binding template is `12_advanced_animations_with_claude/04_harness_contract/scene_template.html` and the rules are in `12_advanced_animations_with_claude/04_harness_contract/contract.md`. Helper names are placeholders for whatever the contract provides.

```html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="fonts/fonts.css"><!-- vendored fonts only (NEW-16) -->
</head><body>
<svg id="stage" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
<script type="module">
// Helpers as provided by 12_advanced_animations_with_claude/04_harness_contract/scene_template.html (cue/fixture loaders, Timeline, rngAt).
import { loadCueSheet, loadFixture, cueState, rngAt } from "./harness.js";   // names: verify against the template

const cues = await loadCueSheet("cue_sheet.json");
const fx   = Object.freeze(await loadFixture("fixtures/fx_iv_two_lines_v1.json")); // deep-freeze per contract §9
await document.fonts.load('600 54px "HouseSans"', "Current I (A) 0.8 0.4 R = V / I"); // explicit load (contract §6)
const stage = document.getElementById("stage");

const layout = verticalLayout(fx);          // safe zones from vertical_safe_zones.tokens.json
buildDataLayer(stage, fx, layout);          // axes, ticks, lines A/B, labels: exact; every glyph has data-fx="…"
buildDoodleLayer(stage, layout, fx.seed);   // paper, pencil character, arrows (illustrative only; precomputed once)
buildTextLayer(stage, layout);              // hook (handwriting mask), CTA card

window.DURATION = cues.duration;            // 30.0 → 900 frames [N72]; set before window.ready resolves

window.seek = async (t) => {                // pure function of t; no rAF, no timers (#15, #19)
  const s = (id) => cueState(cues, id, t);  // {visible, progress 0..1} from cues[].at only
  setMaskWipe("hook_title", s("hook_title").progress);
  setDrawOn("graph", s("graph_draw").progress);          // stroke-dash draw-on, geometry unchanged
  setPulse("axis_labels", s("axis_labels").progress);
  setVisible("doodle_point", s("doodle_point").visible);
  setHighlight("axis_y", s("axis_y").visible && !s("axis_x").visible);  // one dominant highlight
  setHighlight("axis_x", s("axis_x").visible);
  setDrawOn("probe_v4", s("probe_v4").progress);
  setVisible("readout_A", s("readout_A").visible);        // text from fx.probe, never typed
  setVisible("readout_B", s("readout_B").visible);
  setVisible("relation_R", s("relation_R").visible);      // fx.relation_text
  setHighlight("line_B", s("line_B").visible);
  setVisible("cta_card", s("cta_card").visible);
  boilDoodles((i) => rngAt(fx.seed, Math.floor(t * 8) * 1000 + i)); // stateless 8 fps boil, layer 2 only ([V4-MP] §8)
};
</script></body></html>
```

What the contract linter (A1) must accept: `DURATION` and `seek` defined; no `Date.now`, `setInterval`, `requestAnimationFrame`, `Math.random`, infinite repeats or network fetches (rules F01–F12); no stateful PRNG draws inside `seek` (use `rngAt(seed, i)`, contract §4). The full contract also asks for `window.ready`, `window.__errors` and `window.__hf` (contract §2.3, §3); the template provides them.

### A.9 Step 9 — Audio bed and SFX

`examleaf-audio-compose` renders a bed only for the hook (bars 1–2, 0–4.8 s, ducked under speech) and the CTA (one bar, 27.6–30.0 s). Music is off in the body (playbook usage map: "Reel body — muted or very low (test)").

```json
{"bed_id": "reel-002-hook-cta-v1", "generator": "examleaf-audio-compose", "generator_version": "<pin>",
 "bpm": 100, "meter": "4/4", "bars": 3, "beat_offset_s": 0.0,
 "sample_rate": 48000, "bit_depth": 24, "channels": 1, "seed": 7,
 "placements": [{"bar": 1, "at_s": 0.0}, {"bar": 2, "at_s": 2.4}, {"bar": 3, "at_s": 27.6}],
 "mood_segments": [{"from_s": 0.0, "to_s": 4.8, "mood": "curious"},
                   {"from_s": 4.8, "to_s": 27.6, "mood": "core_explanation"},
                   {"from_s": 27.6, "to_s": 30.0, "mood": "warm_end"}],
 "stems": [{"name": "pluck", "path": "audio/beds/reel-002/pluck.wav", "sha256": "<64 hex>"}],
 "licence": "examleaf-generated (legal review pending)", "contains_samples": false}
```

At 100 BPM a bar is 2.4 s = 72 frames = 115,200 samples, so all placements are frame- and sample-exact [RUN LOCALLY: exact-fraction check]. Ducking is gain automation from the timeline clips (doc 06 §7.3). The programme mix is normalised to −16 LUFS ± 1, true peak ≤ −1 dBTP, and re-measured after mux.

### A.10 Step 10 — Render

Invocations follow each script's usage text in `12_advanced_animations_with_claude/04_harness_contract/`.

1. Preflight (A2): `bash 12_advanced_animations_with_claude/04_harness_contract/preflight.sh --dir <frames dir>` (Node 22+ and FFmpeg [N8], Chrome or `CHROME` [N17], Indic fonts, disk; exit 1 on any FAIL).
2. Lint (A1): `node 12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js --level 1 <scene>.html`.
3. Validate the cue sheet: `python3 12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py cue_sheet.json --production` (after real alignment exists).
4. Render: `<harness render command for HyperFrames — verify against contract.md §11 and the pinned HyperFrames docs>` → 900 PNG frames at 1080×1920, 30 fps, served over local HTTP or with the sheet injected (contract §8: production requires `__cueSource` "injected" or "path").
5. Determinism (A3): render twice in separate processes, then `python3 12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py DIR_A DIR_B` (exit 0 = byte-identical PNG frames); add a reverse-order render (AD-21 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`).
6. Encode once (RGB→YUV at the final encode only, `12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` §6.1), then mux narration + mix; `mux_supplied_audio(..., tolerance_s=0.05)` refuses mismatches.

### A.11 Step 11 — QA (expected results)

| Check | Expected |
|---|---|
| A1 lint | 0 violations |
| A3 determinism | Identical PNG frame hashes across two renders and a reverse-order render |
| A4 safe zones | Hook, graph, readouts, CTA inside the safe area; nothing in the caption reserve |
| A5 holds | Hook title fully readable ≥ 1.2 s; `R = V / I` visible from 17.70 s to the end (narration of it ends ≈ 18.9 s → needs ≥ 19.4 s); answer state held 20.20–26.95 s |
| A6 flashes | No full-frame flashes; sparkle doodles small-area |
| A7 text | Axis labels, tick values, readouts "0.8 A", "0.4 A", "R = V / I", condition tag equal fixture strings; no text in any raster |
| A12 science | From the first frame at or after 13.20 s the A readout equals `fx.probe.I_line_A`; probe line at V = 4; line slopes equal 1/R; axes unchanged on every sampled frame; layer-1 wobble amplitude 0 (NEW-28) |
| A13 contrast/phone | Text ≥ 4.5:1 on paper texture; essential labels ≥ ≈ 50 px source (RD-18) |
| A14 camera | No push-in or shake (none used) |
| A9 audio | −16 ± 1 LUFS; TP ≤ −1 dBTP; music stem silent 4.8–27.6 s |
| A10 sync | Captions match narration; each reveal at `t0 − 0.05 s`, inside `[t0 − 0.05, t0]` |
| A11 probe | 1080×1920, 30 fps, 900 frames, h264, yuv420p, audio present |
| Rubric (H-RV) | R1 Pass (critical criterion); R2: answer only after the think pause; R10: no crop |

### A.12 Step 12 — Approval and export

1. ⛔ **GS**: academic owner and a different production reviewer approve the Short's hash after a full watch on a small phone (SH7).
2. Package (SH6, `examleaf-thumbnail-package`): title "HSLC Electricity: Read the Graph Before Using the Formula"; cover **CHECK THE AXES**; caption first line "The axes decide what this slope means."; one CTA "Try the three-question graph check." (`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` SH6; `01_business_model/REEL_BACKLOG_36.md`).
3. Export record: class, subject, language, edition IDs; access `free`; destination resource; approved hash; attribution — never secrets (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §7).
4. Tracker row (SH8): chapter ID, claim source, science approval, script, 9:16 scene, caption, target class/medium, CTA destination, experiment ID, release status.

### A.13 Ledger record (example shape)

```json
{"run_id": "<uuid>", "short_id": "reel-002-iv-axes", "scene_id": "reel-002-iv-axes",
 "task_type": "scene_code", "claude_code_version": "<as reported>",
 "model_id": "claude-opus-5-5", "alias_used": false,
 "effort_requested": "high", "effort_effective": "<as reported>", "effort_fallback": false,
 "ultracode": false, "subagent_count": 0, "subagent_tokens_missing": false,
 "tokens_input": "<measured>", "tokens_output": "<measured>",
 "tokens_cache_read": "<measured>", "tokens_cache_write": "<measured>",
 "est_cost_api_usd": "<computed at price_table_date>", "price_table_date": "<date>",
 "wall_time_s": "<measured>", "round": 1, "repair_attempt": 0, "outcome": "rubric_pass",
 "credits_estimated": 0, "credits_actual": 0, "render_seconds": "<measured>"}
```

---

## Part B · One data-bound lesson scene: the I–V graph, 05:00–05:55

### B.0 The beat (from the blueprint)

| Time | Direction (blueprint) | Student action |
|---|---|---|
| 05:00–05:15 | "Introduce a graph explicitly labelled **current vertically, voltage horizontally**." | Establish the representation |
| 05:15–05:35 | "Plot the earlier points, using fixed axes and units. Build the line without changing scale." | Connect the measurements to the graph |
| 05:35–05:55 | "Show that the slope is `ΔI/ΔV = 1/R`. Use one highlighted rise/run pair." | Interpret slope |

The next beat (05:55–06:08) adds "a second, steeper line on the same axes", so the axes chosen now must already fit it. Duration 55 s = 1,650 frames at 30 fps; lesson global start frame 05:00 × 30 = **9,000**.

### B.1 Step 1 — Route

- Tag: `data-bound` (router rule 1: "Equation, calculation, graph or model state: deterministic only").
- Renderer: **`examleaf-svg-scenes`** (default and only tested path, RD-07). Optional Manim CE insert for the slope expression (§B.7) only if the academic owner wants an equation transformation shown; not required by the beat.
- Motion: semantic only — points appear, the line builds, one rise/run pair highlights. Layout stays stable for the whole 55 s and into the next beat (E3: layouts stable 20–60 s or longer).
- No music (core explanation), no camera moves (#64), one dominant highlight at a time.

### B.2 Step 2 — Fixture (`lessons/<…>/anim/phy10-ohm-iv-graph-s12/fixtures/fx_ohm_iv_graph_v1.json`)

```json
{
  "fixture_id": "fx_ohm_iv_graph_v1",
  "claim_ids": ["<clm_ohm_relationship>", "<clm_iv_slope_is_1_over_R>", "<clm_ohmic_condition>"],
  "model": {"resistor_ohm": 10, "condition": "Same resistor, constant temperature and other relevant conditions"},
  "axes": {
    "x": {"quantity": "V", "label": "Voltage, V", "unit": "V", "min": 0, "max": 6, "ticks": [0, 1, 2, 3, 4, 5, 6]},
    "y": {"quantity": "I", "label": "Current, I", "unit": "A", "min": 0, "max": 1.2, "ticks": [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]}
  },
  "points": [
    {"id": "pt_origin", "V": 0, "I": 0},
    {"id": "pt_2V", "V": 2, "I": 0.2, "source_beat": "01:00-01:15"},
    {"id": "pt_4V", "V": 4, "I": 0.4, "source_beat": "01:33-01:50"}
  ],
  "rise_run": [{"V": 2, "I": 0.2}, {"V": 4, "I": 0.4}],
  "display": {
    "run_text": "ΔV = 2 V", "rise_text": "ΔI = 0.2 A",
    "slope_text": "ΔI / ΔV = 1 / R", "slope_value_text": "0.2 A / 2 V = 0.1 A/V = 1 / (10 Ω)",
    "slope_A_per_V": 0.1
  },
  "reserved_for_next_beat": {"steeper_line_resistance_ohm": "<academic owner to confirm, e.g. 5>"},
  "seed": 0
}
```

Why these points: "Plot the earlier points" most naturally means the opening 10 Ω readings (2 V, 0.2 A) and (4 V, 0.4 A) (blueprint ambiguity D.1). The origin is included because the ohmic line passes through it; the academic owner confirms. Axes to 6 V and 1.2 A leave room for a 5 Ω line in the next beat (6 V → 1.2 A).

### B.3 Step 3 — Science validation (bounded template)

There is no `iv_graph` template today: the engine supports four kinds, one per subject (RD-35). Adding it follows `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §9: science approved first; declare the kind; allow several kinds per subject; write a bounded validator that raises outside scope; at least one independent cross-check; renderer computes displayed state from the same function; layouts for both aspects; tests (positive, wrong parameter, out of scope, frame-content agreement, media integration).

Validator sketch [RUN LOCALLY: 6 checks pass on the fixture; a wrong point fails; swapped axes raise]:

```python
from fractions import Fraction as F

def validate_iv(fx):
    checks, ax = [], fx["axes"]
    if not (ax["y"]["quantity"] == "I" and ax["x"]["quantity"] == "V"):
        raise ValueError("I must be vertical and V horizontal")       # retained condition
    R = F(str(fx["resistor_ohm"]))
    if R <= 0:
        raise ValueError("resistance must be positive (ohmic model only)")
    for p in fx["points"]:
        V, I = F(str(p["V"])), F(str(p["I"]))
        checks.append(("point_on_line", I == V / R))                   # I = V/R
        checks.append(("point_in_axes", ax["x"]["min"] <= V <= ax["x"]["max"]
                       and ax["y"]["min"] <= I <= ax["y"]["max"]))
    (v1, i1), (v2, i2) = [(F(str(p["V"])), F(str(p["I"]))) for p in fx["rise_run"]]
    slope = (i2 - i1) / (v2 - v1)
    checks.append(("slope_equals_1_over_R", slope == 1 / R))           # exact-fraction cross-check
    checks.append(("display_slope_matches", F(str(fx["display"]["slope_A_per_V"])) == slope))
    return checks
```

(The local test used a flattened fixture with `resistor_ohm` at the top level; the production validator reads `model.resistor_ohm`.) Exact fractions avoid float equality traps: (0.4 − 0.2)/(4 − 2) = 1/10 = 1/R for R = 10 Ω. Units: A/V = 1/Ω. Output: `science/science_report.json` with named checks; claim status `machine_checked`, never `expert_approved` by a machine.

### B.4 Step 4 — SceneSpec (`scenes/scene-spec.json`, entry)

Fields per `07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §3.4; `kind: iv_graph` is **proposed** (needs RD-35).

```json
{
  "schema_version": "1.0",
  "id": "phy10-ohm-iv-graph-s12",
  "subject": "physics",
  "kind": "iv_graph",
  "title": "Current-voltage graph and slope",
  "objective": "Interpret the slope of an I-versus-V graph as 1/R for an ohmic resistor",
  "class_context": "Class 10 revision; Class 12 prerequisite check",
  "duration_s": 55,
  "fps": 30,
  "parameters": {"fixture_id": "fx_ohm_iv_graph_v1"},
  "assumptions": ["Ohmic resistor at constant temperature and other relevant conditions"],
  "sources": ["<SourceRef ids>"],
  "claims": ["<clm_ohm_relationship>", "<clm_iv_slope_is_1_over_R>", "<clm_ohmic_condition>"],
  "cues": [
    {"start_s": 0,  "end_s": 15, "text": "<display text, beat 05:00-05:15>", "role": "explain", "voice": "steady",     "answer_visible": false},
    {"start_s": 15, "end_s": 35, "text": "<display text, beat 05:15-05:35>", "role": "explain", "voice": "steady",     "answer_visible": false},
    {"start_s": 35, "end_s": 55, "text": "<display text, beat 05:35-05:55>", "role": "explain", "voice": "deliberate", "answer_visible": false}
  ],
  "status": "review_pending"
}
```

Validator rules: cues contiguous from 0 and ending exactly at `duration_s`; 55 × 30 = 1,650 (whole frames). Sibling record (until RD-29 lands): display vs spoken text references, the 12 pedagogy fields, route (rule 1) and tag `data-bound`, vertical reflow plan, cost cap (no paid assets).

### B.5 Step 5 — Narration cues and the scene cue sheet

Draft narration (illustrative; the approved script governs, and the blueprint gives directions, not lines): "Let's put those readings on a graph. Current goes up the vertical axis. Voltage goes along the horizontal axis. At two volts we measured zero point two amps. At four volts, zero point four amps. The points line up through zero. Now the slope: rise over run. From two volts to four volts, current rises by zero point two amps. Delta I over delta V is one over R — here, one over ten ohms."

Narration `Cue` entries (contract in `07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §4.3):

```json
[
  {"cue_id": "c_axis_i",  "phrase": "current",  "occurrence": 1, "edge": "start", "action": "highlight", "element_id": "axis_y"},
  {"cue_id": "c_axis_v",  "phrase": "voltage",  "occurrence": 1, "edge": "start", "action": "highlight", "element_id": "axis_x"},
  {"cue_id": "c_pt2",     "phrase": "two volts", "occurrence": 1, "edge": "start", "action": "show",     "element_id": "pt_2V"},
  {"cue_id": "c_pt4",     "phrase": "four volts", "occurrence": 1, "edge": "start", "action": "show",    "element_id": "pt_4V"},
  {"cue_id": "c_line",    "phrase": "line up",  "occurrence": 1, "edge": "start", "action": "show",      "element_id": "line_10ohm"},
  {"cue_id": "c_run",     "phrase": "two volts to four volts", "occurrence": 1, "edge": "start", "action": "highlight", "element_id": "run_bracket"},
  {"cue_id": "c_rise",    "phrase": "rises",    "occurrence": 1, "edge": "start", "action": "highlight", "element_id": "rise_bracket"},
  {"cue_id": "c_slope",   "phrase": "Delta I over delta V", "occurrence": 1, "edge": "start", "action": "show", "element_id": "slope_text"},
  {"cue_id": "c_value",   "phrase": "one over ten ohms", "occurrence": 1, "edge": "start", "action": "show", "element_id": "slope_value_text"}
]
```

Each event is placed at a sample (`clip_start + round(word_time × 48,000)`) and converted once to a lesson frame (04 N11). Example (illustrative): "current" spoken 2.40 s into the scene → lesson sample 14,400,000 + 115,200 = 14,515,200 → lesson frame 9,072 → scene-local 2.40 s. The cue sheet reveals at `t0 − 0.05` = 2.35 s; the first captured frame at or after it is frame 71 (2.367 s) [RUN LOCALLY: arithmetic].

Scene cue sheet (`anim/phy10-ohm-iv-graph-s12/cue_sheet.json`; illustrative times, `words[]` abbreviated; hashes computed as in §A.7). [RUN LOCALLY] `validate_cue_sheet.py` → `VALID (0 errors, 0 warnings)`.

```json
{
  "schema_version": "1.0",
  "scene_id": "phy10-ohm-iv-graph-s12",
  "fps": 30,
  "duration": 55.0,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": "ef1d769a82d06963cfd4c3cda3b85e440220180a5705351204c98e7243df81b8",
  "script_sha256": "fc53ba34baf4037e997a42650294636373c6afb1376059cf6df55d4b81eda479",
  "words": [
    {"w": "Current", "t0": 2.4, "t1": 2.85},
    {"w": "Voltage", "t0": 5.1, "t1": 5.6},
    {"w": "two", "t0": 17.48, "t1": 17.7, "occurrence": 1},
    {"w": "four", "t0": 21.28, "t1": 21.5},
    {"w": "line", "t0": 26.08, "t1": 26.3},
    {"w": "two", "t0": 39.12, "t1": 39.32, "occurrence": 2},
    {"w": "rises", "t0": 42.45, "t1": 42.85},
    {"w": "Delta", "t0": 46.28, "t1": 46.6},
    {"w": "one", "t0": 49.62, "t1": 49.8},
    {"w": "ten", "t0": 50.7, "t1": 50.95},
    {"w": "ohms", "t0": 50.95, "t1": 51.4}
  ],
  "beats": [],
  "cues": [
    {"id": "graph_frame", "at": 0.0, "kind": "reveal", "element_id": "graph_frame"},
    {"id": "axis_y", "at": 2.35, "kind": "emphasis", "element_id": "axis_y", "word_index": 0},
    {"id": "axis_x", "at": 5.05, "kind": "emphasis", "element_id": "axis_x", "word_index": 1},
    {"id": "pt_2V", "at": 17.43, "kind": "reveal", "element_id": "pt_2V", "word_index": 2},
    {"id": "pt_4V", "at": 21.23, "kind": "reveal", "element_id": "pt_4V", "word_index": 3},
    {"id": "line_10ohm", "at": 26.03, "kind": "reveal", "element_id": "line_10ohm", "word_index": 4},
    {"id": "run_bracket", "at": 39.07, "kind": "emphasis", "element_id": "run_bracket", "word_index": 5},
    {"id": "rise_bracket", "at": 42.4, "kind": "emphasis", "element_id": "rise_bracket", "word_index": 6},
    {"id": "slope_text", "at": 46.23, "kind": "reveal", "element_id": "slope_text", "word_index": 7},
    {"id": "slope_hold", "at": 46.23, "kind": "hold", "element_id": "slope_text", "until": 55.0},
    {"id": "slope_value_text", "at": 49.57, "kind": "reveal", "element_id": "slope_value_text", "word_index": 8}
  ],
  "sfx": [],
  "meta": {"note": "ILLUSTRATIVE. words[] abbreviated; timings not aligned; narration is a draft pending GA.", "beats_note": "Empty: core explanation, no music bed.", "lesson_start_frame": 9000}
}
```

No SFX and no beats: this is core explanation, so music is off and stings are not used (doc 06 §1). The slope expression has a `hold` cue to the scene end and continues into the next beat.

### B.6 Step 6 — Render the SVG scene

Native proof adapter (reference/regression renderer; [TESTED] only for the four existing kinds):

```sh
# Works only after the iv_graph kind, validator, renderer branch and tests exist (§B.3).
PYTHONPATH=src python3 -m examleaf.cli validate examples/phy10_ohm_iv_graph.json
PYTHONPATH=src python3 -m examleaf.cli render examples/phy10_ohm_iv_graph.json --aspect 9:16 --out outputs
```

*15 Oct 2026 (audit M1, executability-13):* the `--aspect 16:9` render line was removed; output is vertical only (RD-16 SUPERSEDED). **What the proof renderer can do today:** `--aspect 9:16` renders **720×1280** at the scene's fps, which is **24 fps** in every existing fixture (`04_video_engine/implementation_v2/src/examleaf/visuals.py` `render_svg`: `w,h=(720,1280)`; `examples/*.json` `"fps": 24`). It has **no 1080×1920 @ 30 fps mode**; adding one is a **P1 build item** (doc 14 C13; RD-16 row in 07/10), and until it exists proof renders are review-only and are never imported as production clips. Use `python3` (this Mac has no `python` binary).

Note: the proof adapter writes 1280×720 / 720×1280 at the scene fps and exports stills at 2, 13, 22 and 28 s (scene ≥ 30 s required, RD-34; 55 s is fine). This section's layer renders **1080×1920 at 30 fps only** (AD-07 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`); ~~a 16:9 version exists only while the runbook keeps a 16:9 lesson master (RD-16; conflict C1), produced by recomposition from the same fixture~~ (withdrawn 15 Oct 2026: RD-16 superseded, no 16:9 output). Production render: `<compositor render command — verify after the P1 benchmark>`; export as a PNG sequence with a `clip.json` manifest (`12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` §2).

Rendering rules (03 S9): every frame evaluated from explicit `t = frame / fps`; displayed state computed by the same science function the validator used; no wall clock, no randomness, no network fonts; vertical layout only, never a crop of a 16:9 frame (15 Oct 2026: "both aspects" withdrawn).

### B.7 Optional Manim CE insert for the slope expression

Only if the academic owner wants the expression built as an equation insert. API names follow Manim CE conventions and must be verified against the pinned version [N46]; CE only (#28).

```python
# Manim CE outline — verify class/method names in the pinned CE version.
from manim import *            # CE, not ManimGL
import json

FX = json.load(open("fx_ohm_iv_graph_v1.json"))
CUES = json.load(open("cue_sheet.json"))

class SlopeInsert(Scene):
    def construct(self):
        # Symbol IDs bound to fixture fields (stable correspondence, doc 07 §3.3)
        slope = MathTex(r"\frac{\Delta I}{\Delta V}", "=", r"\frac{1}{R}")
        value = MathTex(r"\frac{0.2\,\mathrm{A}}{2\,\mathrm{V}}", "=", r"\frac{1}{10\,\Omega}")
        t_slope = cue_at(CUES, "slope_text") - cue_at(CUES, "run_bracket")
        self.wait(t_slope)                                   # waits from the cue sheet, not guesses
        self.play(Write(slope), run_time=1.0)                # within 0.8–1.5 s transform range
        self.wait(cue_at(CUES, "slope_value_text") - cue_at(CUES, "slope_text") - 1.0)
        self.play(FadeIn(value), run_time=0.5)
        self.wait(remaining(CUES))                           # hold to the scene end
```

The insert's total frames must equal its cue-sheet window × 30 (NEW-13); the strings must match `fx.display` (A7 via symbol manifest + OCR/human); its math font must match the composition's math font (NEW-19); LaTeX must be present on the render box (NEW-20).

### B.8 Step 7 — Import into the lesson timeline

1. Clip manifest `clip.json` (`12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` §2) with `fixture_sha256` and frames 1,650, plus the optional fields in doc 07 §5.2.
2. Place in the lesson composition at **start frame 9,000** (05:00) for 1,650 frames using the portable `clipFrame()` mapping (import notes §4.1); the clip start comes from the master cue sheet, never hard-coded; the next scene starts at frame 10,650 (05:55).
3. The next beat (05:55–06:35) reuses the **same axes object and scale** (fixture `axes` unchanged) and adds the steeper line; the composition must not re-animate the axes (Physics rule: "Keep axes and scale stable when comparing cases", E5).
4. Captions come from the narration timeline (speech-animation-synchronizer); the composition only places them in the protected area.
5. Probe and hash (A11; A3 on PNG frames before encode).

### B.9 Step 8 — Holds and pacing for this beat

| Element | Rule | Result in this scene |
|---|---|---|
| Axes and labels | Always visible (Physics E5; "axes and units always visible") | Visible from frame 0 to the end and beyond |
| Points and line | Appear on their words; remain | Remain into the next beat |
| `ΔI / ΔV = 1 / R` | Narration end + 0.5 s, and ≥ 2–4 s after the transformation (RD-02) | Revealed at 46.2 s; remains to 55 s and through the next beat |
| Value line | Same | Revealed at 49.6 s; remains |
| Dominant highlight | One at a time (D4) | Run bracket, then rise bracket, then slope text |
| Narration pace | Dense new relationship ≈ 105–125 wpm (RD-10) | Measured by `examleaf-pacing-controller`; if too fast, edit words or lengthen the beat, never speed audio |

### B.10 Step 9 — QA for the lesson scene (expected results)

| Check | Expected |
|---|---|
| A12a validators | All `validate_iv` checks pass; fixture hash equals the GA bundle's |
| A12b science-frame | At each cue frame, plotted pixel positions map back to the fixture values within one pixel; slope text equals fixture; tick positions identical on every sampled frame (scale unchanged) |
| A7 text | Axis titles, units, tick labels, "ΔV = 2 V", "ΔI = 0.2 A", "ΔI / ΔV = 1 / R", "0.2 A / 2 V = 0.1 A/V = 1 / (10 Ω)" equal fixture strings |
| A3 determinism | Identical PNG frame hashes |
| A4 / A13 | Both aspects: labels beside objects, inside safe area, contrast ≥ 4.5:1, essential text readable at 360 px (`Displayed = Source × 360 / master width`) |
| A5 holds | As §B.9 |
| A14 camera | No camera transform at any frame |
| A9 audio | Narration only; music stem absent; −16 LUFS ± 1 on the lesson master |
| A10 sync | Each reveal at `t0 − 0.05 s`; captions match narration |
| Engine negative test | "Equation changes must match narrated meaning and graph axes/units" (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §10 item 3) |

### B.11 Step 10 — Approvals

- GA already approved the planned scientific visual for this beat (03 GA: "the planned scientific visuals").
- The scene is part of the lesson's `final.mp4`; ⛔ **GF** binds both approvals to that file's hash after a full watch.
- Any later change to the fixture (for example the confirmed steeper-line resistance) invalidates GA and GF for the affected scenes (03 S15).

---

## Part C · What the two examples show

1. **The same fixture discipline serves both.** The Reel's doodle layer is free to wobble; its graph is not (NEW-28).
2. **Narration sets every time.** Both cue sheets are projections of a sample-exact timeline; regenerating TTS rebuilds them without touching scene code (#63).
3. **The cheap path is the default.** No credits, no generated video, code-rendered storyboard thumbnails, Python SFX, house fonts for science.
4. **The new template is the real cost.** The `iv_graph` kind needs validator, renderer branch and tests once; afterwards every Ohm's-law lesson and Reel re-renders it with new fixtures at near-zero agent cost (doc 09 §11.2).
5. **Open items to verify before production:** the steeper-line resistance (academic owner), the HyperFrames render command and adapter, the linter and hash-check invocations, the safe-zone token values, the final-mix command, and the Manim CE API names if the insert is used.
