# Filled brief: voxel lattice insert for Reel CSV 12 ("Same salt: why compare the solid with the melt?")

**Reel:** CSV ID 12 (Class 10 Chemistry, ionic conductivity, P0, target 40 s). Hook: "Same salt: why compare the solid with the melt?" Caption first line: "Identify which charged particles can move." CTA: "Watch the bonding-to-conductivity explanation." Scientific check: differentiate ionic motion from electron conduction.
**This scene:** s02 of the Reel, the short voxel insert (10.8 s) showing the fixed arrangement of ions in the solid. The melt comparison is a separate data-bound panel built from fixture frames; this insert ends on the fixed lattice and never animates ion motion.
**Why voxel:** a cubic lattice on an integer grid is the one case where voxels are faithful (report §4.5). The grid and species come from the fixture; seeded randomness only decorates the ground.

**Style:** `voxel-isometric@1.0.0` | **Version of this example:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** EXAMPLE. Every input below is illustrative so that the brief can be read end to end. In a real job the pipeline supplies approved inputs; the animation agent never authors them, and nothing here has been run.

**Evidence labels:** [V#]/[N#] are cited from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement; [Hypothesis] = untested. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Hook text and CSV IDs come from `01_business_model/REEL_BACKLOG_36.md` (the CSV ID is the stable ID).

## How this example is built

The generator filled `brief_template.md` from the job request in section A. Unlike the other examples, this scene is data-bound in its geometry, so the route tag is `illustrative` only for the insert's framing: every voxel that carries science is a fixture cell. The voxel render needs the pinned WebGL render box and exports a PNG sequence.

## A. Job request (`brief_request.json`, the input to `examleaf-anim-brief`)

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv12-s02",
  "lesson_id": "chem-10-ionic-compounds",
  "language": "en-IN",
  "route": {
    "tag": "illustrative",
    "source": "examleaf-storyboard-route",
    "scene_spec_id": "short-csv12-s02"
  },
  "script": {
    "path": "jobs/short-csv12-s02/inputs/approved_script.md",
    "sha256": "<64 hex>",
    "approval_status": "approved",
    "segment_text": "In the solid, the ions sit in fixed positions. Positive and negative ions alternate in every direction. Locked in place, the ions cannot carry current."
  },
  "style": {
    "id": "voxel-isometric",
    "version": "1.0.0",
    "guide_path": "12_advanced_animations_with_claude/05_style_guides/voxel-isometric.md",
    "tokens_path": "12_advanced_animations_with_claude/05_style_guides/style_tokens.json"
  },
  "cue_sheet": {"path": "jobs/short-csv12-s02/inputs/cue_sheet.json", "sha256": "<64 hex>"},
  "brand_tokens": {"path": "jobs/short-csv12-s02/inputs/brand_tokens.json", "sha256": "<64 hex>"},
  "fixtures": [
    {
      "id": "chem10-ionic-lattice-cubic-4",
      "path": "jobs/short-csv12-s02/inputs/chem10-ionic-lattice-cubic-4.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["grid", "cells[]", "species[].label_display", "species[].color_token", "note_display"]
    }
  ],
  "fonts": {
    "allow": [
      "Noto Sans semibold (DOM labels and legend",
      "never inside WebGL)",
      "Inter (captions and labels only)",
      "KaTeX fonts (not used in this scene)"
    ],
    "ban": [
      "Arial",
      "Helvetica",
      "Roboto",
      "system-ui",
      "generic sans-serif",
      "Space Grotesk",
      "Inter (as a display face)",
      "Times New Roman",
      "Comic Sans",
      "Papyrus"
    ]
  },
  "holds": {"headline_min_s": 1.2, "equation_tail_s": 0.5, "indic_multiplier": 1.5},
  "iteration_cap": 3,
  "effort": {"model": "<pinned full model ID, Opus 5.5>", "level": "high"},
  "workspace": "jobs/short-csv12-s02/",
  "approval_record": {"path": "jobs/short-csv12-s02/storyboard/approval_record.json", "sha256": "<64 hex>"},
  "creative_direction": "Voxel lattice insert for Reel CSV 12, scene s02, 10.8 s. three.js `InstancedMesh` of unit cubes, orthographic camera at the true isometric angle (azimuth 45 degrees, elevation atan(1/sqrt(2)) which is about 35.264 degrees), baked face shading (top 1.00, left 0.80, right 0.62), unlit material, no real lights or shadows. Scientific voxels: the 4x4x4 grid, each cell and its species exactly as in the fixture (`cells[]`); never add, remove, move or recolour one. Colours from the fixture's `color_token`: positive = blue `#185ABD`, negative = teal `#087986` (no red or amber species). Ground: a one-high plate of ground voxels in two close tints, plus five decorative tufts placed by `rnd(\"short-csv12-s02:layout:i\")`. Timeline: layers build from the bottom, scale 0 to 1 with `back.out(1.4)`, 0.3 s each, 50 ms apart, from 0.35 s; the fixture's `note_display` (schematic note) appears with the build as part of the same group; camera still from 0 to 2.20 s; slow orbit 0 to 20 degrees from 2.20 to 3.60 s (no label reveals in that window); camera still from 3.60 s to the end. At \"Positive\" (3.95 s) the legend tag for the positive species appears (DOM label from `species[].label_display`, leader line to a voxel, anchor from the projected voxel centre) and the positive voxels brighten 1.00 to 1.25 for 0.40 s; at \"negative\" (4.63 s) the same for the negative species. A legend always shows both species with colour and a letter mark (colour is never the only cue). From 7.55 s the lattice is held unchanged. Render on the pinned render box at 2x and downscale; export a PNG sequence; run the software-GL fallback check; fail with `WEBGL_CONTEXT_LOST` if the context is lost. The melt comparison is not in this scene."
}
```

## B. Example approved script segment (illustrative; the real text comes from the approved script bundle)

| ID | Mode | Spoken text | Notes |
|---|---|---|---|
| v1 | steady | In the solid, the ions sit in fixed positions. | Build-up sentence. |
| v2 | deliberate | Positive and negative ions alternate in every direction. | Legend and brightening. |
| v3 | steady | Locked in place, the ions cannot carry current. | Hold. Differentiates ionic motion from electron conduction in the next scene. |

Sentences are 9, 8 and 8 words, so about 3 s each; the camera schedule leaves the orbit in the pause between v1 and v2.

## C. Example cue sheet (`inputs/cue_sheet.json`; timings are PLANNED until the voice is measured)

Conforms to `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`. Checked with `python3 validate_cue_sheet.py`: valid, 0 errors, one warning (the null narration hash, expected while timings are PLANNED). `--production` would reject it (`alignment_source` is `example`, the hashes are placeholders). Free-form extras live under `meta`. Reveal cues carry `element_id` and `word_index`, and each `at` is in `[t0 - 0.05, t0]` of its word.

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv12-s02",
  "fps": 30,
  "duration": 10.8,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": null,
  "script_sha256": "246a2587a077a4a4469ae1959b080a8f6c8812b0a597ea09f68d03f835c74c84",
  "words": [
    {"w": "In", "t0": 0.4, "t1": 0.55},
    {"w": "the", "t0": 0.55, "t1": 0.65},
    {"w": "solid", "t0": 0.65, "t1": 1.05},
    {"w": "the", "t0": 1.5, "t1": 1.6},
    {"w": "ions", "t0": 1.6, "t1": 1.95},
    {"w": "sit", "t0": 1.95, "t1": 2.2},
    {"w": "in", "t0": 2.2, "t1": 2.3},
    {"w": "fixed", "t0": 2.3, "t1": 2.65},
    {"w": "positions", "t0": 2.65, "t1": 3.25},
    {"w": "Positive", "t0": 4.0, "t1": 4.55},
    {"w": "and", "t0": 4.55, "t1": 4.68},
    {"w": "negative", "t0": 4.68, "t1": 5.15},
    {"w": "ions", "t0": 5.15, "t1": 5.45},
    {"w": "alternate", "t0": 5.45, "t1": 6.05},
    {"w": "in", "t0": 6.05, "t1": 6.15},
    {"w": "every", "t0": 6.15, "t1": 6.45},
    {"w": "direction", "t0": 6.45, "t1": 7.05},
    {"w": "Locked", "t0": 7.55, "t1": 7.95},
    {"w": "in", "t0": 7.95, "t1": 8.05},
    {"w": "place", "t0": 8.05, "t1": 8.4},
    {"w": "the", "t0": 8.55, "t1": 8.65},
    {"w": "ions", "t0": 8.65, "t1": 8.95},
    {"w": "cannot", "t0": 8.95, "t1": 9.3},
    {"w": "carry", "t0": 9.3, "t1": 9.6},
    {"w": "current", "t0": 9.6, "t1": 10.1}
  ],
  "beats": [],
  "cues": [
    {"id": "c_build", "at": 0.35, "kind": "reveal", "element_id": "build", "word_index": 0},
    {"id": "c_note", "at": 0.35, "kind": "reveal", "element_id": "note", "word_index": 0},
    {"id": "c_orbit_start", "at": 2.2, "kind": "marker", "element_id": "orbit_start"},
    {"id": "c_orbit_end", "at": 3.6, "kind": "marker", "element_id": "orbit_end"},
    {
      "id": "c_legend_pos",
      "at": 3.95,
      "kind": "reveal",
      "element_id": "legend_pos",
      "word_index": 9
    },
    {"id": "c_pulse_pos", "at": 4.0, "kind": "emphasis", "element_id": "pulse_pos", "word_index": 9},
    {
      "id": "c_legend_neg",
      "at": 4.63,
      "kind": "reveal",
      "element_id": "legend_neg",
      "word_index": 11
    },
    {
      "id": "c_pulse_neg",
      "at": 4.68,
      "kind": "emphasis",
      "element_id": "pulse_neg",
      "word_index": 11
    }
  ],
  "sfx": [
    {"file": "sfx/block_tick.wav", "at": 0.35, "gain_db": -20},
    {"file": "sfx/block_tick.wav", "at": 0.45, "gain_db": -20},
    {"file": "sfx/block_tick.wav", "at": 0.55, "gain_db": -20},
    {"file": "sfx/block_tick.wav", "at": 0.65, "gain_db": -20},
    {"file": "sfx/pop.wav", "at": 3.95, "gain_db": -16},
    {"file": "sfx/pop.wav", "at": 4.63, "gain_db": -16}
  ],
  "meta": {
    "note": "EXAMPLE ONLY. Timings are PLANNED, not aligned to real audio, and the wording is not an approved ExamLeaf script.",
    "status": "PLANNED",
    "script_text": "In the solid, the ions sit in fixed positions. Positive and negative ions alternate in every direction. Locked in place, the ions cannot carry current.",
    "script_sha256_of": "UTF-8 bytes of meta.script_text",
    "narration_audio_sha256_of": "null while no narration exists (production requires a hash)",
    "sentences": [
      {"id": "v1", "t0": 0.4, "t1": 3.25, "mode": "steady"},
      {"id": "v2", "t0": 4.0, "t1": 7.05, "mode": "deliberate"},
      {"id": "v3", "t0": 7.55, "t1": 10.1, "mode": "steady"}
    ],
    "think_windows": [],
    "beats_note": "empty: no music bed in this scene, so no beat grid"
  }
}
```

## D. Example inputs the scene may read

**Fixture excerpt (`chem10-ionic-lattice-cubic-4.json`).** EXAMPLE, NOT A VALIDATED FIXTURE; in production the science pipeline supplies and signs it:

```json
{
  "fixture_id": "chem10-ionic-lattice-cubic-4",
  "status": "EXAMPLE_NOT_A_VALIDATED_FIXTURE",
  "grid": {"nx": 4, "ny": 4, "nz": 4},
  "species": [
    {"id": "pos", "label_display": "Positive ion", "color_token": "blue", "mark": "+"},
    {"id": "neg", "label_display": "Negative ion", "color_token": "teal", "mark": "-"}
  ],
  "cells": [
    {"x": 0, "y": 0, "z": 0, "s": "pos"},
    {"x": 1, "y": 0, "z": 0, "s": "neg"},
    "... 62 more cells; each species is the opposite of its six face-neighbours ..."
  ],
  "note_display": "Schematic: ions drawn as equal-sized cubes"
}
```

The agent reads the cells from the file; it does not derive them from a rule it invents.

**Render box:** the pinned render box ID is supplied by `examleaf-render-batch`. Frame hashes are compared only between renders on that box (#65).

## E. Example storyboard beats (excerpt of the approved `storyboard/beats.json`)

```json
{
  "schema_version": "1.0.0",
  "scene_id": "short-csv12-s02",
  "timing_status": "PLANNED",
  "beats": [
    {
      "beat_id": "b01",
      "panel": 1,
      "sentence_ids": ["v1"],
      "merged_from": [],
      "planned_start_s": 0.4,
      "planned_end_s": 3.25,
      "voice_mode": "steady",
      "route": "data-bound",
      "visual_brief": "A 4x4x4 voxel lattice builds layer by layer on a small ground plate in an isometric view; a schematic note appears beside it.",
      "fixture_refs": ["chem10-ionic-lattice-cubic-4"],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b02",
      "panel": 2,
      "sentence_ids": ["v2"],
      "merged_from": [],
      "planned_start_s": 4.0,
      "planned_end_s": 7.05,
      "voice_mode": "deliberate",
      "route": "data-bound",
      "visual_brief": "The two ion types are named in a legend; first one type, then the other, brightens briefly; the camera is still.",
      "fixture_refs": ["chem10-ionic-lattice-cubic-4"],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b03",
      "panel": 3,
      "sentence_ids": ["v3"],
      "merged_from": [],
      "planned_start_s": 7.55,
      "planned_end_s": 10.1,
      "voice_mode": "steady",
      "route": "data-bound",
      "visual_brief": "The lattice held still, unchanged, while the sentence is read.",
      "fixture_refs": ["chem10-ionic-lattice-cubic-4"],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    }
  ]
}
```

## F. The assembled brief

This is `brief_template.md` with every placeholder filled, followed by the constraints block as it stands in `03_skills/examleaf-anim-brief/templates/constraints_block.md` on 15 Oct 2026. Regenerate this example if either file changes.

````markdown
# Animation brief: short-csv12-s02

**Lesson:** chem-10-ionic-compounds | **Language:** en-IN | **Route:** illustrative | **Style:** voxel-isometric@1.0.0
**Author run:** model `<pinned full model ID, Opus 5.5>`, effort `high` (set explicitly; ultracode is never used), at most 3 fix rounds.
**Workspace:** `jobs/short-csv12-s02/` (work only here)
**Brief level:** L2 structured brief with references ([V2]). Any L3 orchestration (voice, music, paid image generation) is done by ExamLeaf's pipeline adapters before or after this job, never by you. You have no MCP tools.

## 1. Goal

Build one seek-pure 1080×1920 scene for `short-csv12-s02` that animates the approved narration in the `voxel-isometric` style, and nothing else. You write scene code only. You do not write, edit, shorten, paraphrase or "improve" any narration or on-screen wording, and you do not research any fact.

Creative direction from the approved storyboard:
Voxel lattice insert for Reel CSV 12, scene s02, 10.8 s. three.js `InstancedMesh` of unit cubes, orthographic camera at the true isometric angle (azimuth 45 degrees, elevation atan(1/sqrt(2)) which is about 35.264 degrees), baked face shading (top 1.00, left 0.80, right 0.62), unlit material, no real lights or shadows. Scientific voxels: the 4x4x4 grid, each cell and its species exactly as in the fixture (`cells[]`); never add, remove, move or recolour one. Colours from the fixture's `color_token`: positive = blue `#185ABD`, negative = teal `#087986` (no red or amber species). Ground: a one-high plate of ground voxels in two close tints, plus five decorative tufts placed by `rnd("short-csv12-s02:layout:i")`. Timeline: layers build from the bottom, scale 0 to 1 with `back.out(1.4)`, 0.3 s each, 50 ms apart, from 0.35 s; the fixture's `note_display` (schematic note) appears with the build as part of the same group; camera still from 0 to 2.20 s; slow orbit 0 to 20 degrees from 2.20 to 3.60 s (no label reveals in that window); camera still from 3.60 s to the end. At "Positive" (3.95 s) the legend tag for the positive species appears (DOM label from `species[].label_display`, leader line to a voxel, anchor from the projected voxel centre) and the positive voxels brighten 1.00 to 1.25 for 0.40 s; at "negative" (4.63 s) the same for the negative species. A legend always shows both species with colour and a letter mark (colour is never the only cue). From 7.55 s the lattice is held unchanged. Render on the pinned render box at 2x and downscale; export a PNG sequence; run the software-GL fallback check; fail with `WEBGL_CONTEXT_LOST` if the context is lost. The melt comparison is not in this scene.

If this scene belongs to a Short (20-60 s, `ShortSpec`): hook in the first 3 s, a prediction window in 3-8 s (default `think` = 6 s, answer hidden), then the explanation, then one next action. Re-composed for 9:16, never cropped from 16:9.

## 2. Inputs you may read (and nothing else)

Read-only, inside the workspace:
- Approved script: `jobs/short-csv12-s02/inputs/approved_script.md` (SHA-256 `<64 hex>`). Verify the hash of the file bytes before you start; on mismatch stop and write `blockers.json` with code `SCRIPT_HASH_MISMATCH`.
- Cue sheet (all timing comes from here): `jobs/short-csv12-s02/inputs/cue_sheet.json`.
- Brand tokens: `jobs/short-csv12-s02/inputs/brand_tokens.json`.
- Reference analysis (pacing numbers only): `none`.
- Storyboard approval record: `jobs/short-csv12-s02/storyboard/approval_record.json`.
- Validated fixtures (the only source of on-screen science):
  - `chem10-ionic-lattice-cubic-4` at `jobs/short-csv12-s02/inputs/chem10-ionic-lattice-cubic-4.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `grid`, `cells[]`, `species[].label_display`, `species[].color_token`, `note_display`.

Read-only, outside the workspace (allowed):
- Style guide: `12_advanced_animations_with_claude/05_style_guides/voxel-isometric.md` and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`.
- Harness contract and linter: `12_advanced_animations_with_claude/04_harness_contract/contract.md` and `lint_seek_contract.js`.
- Safe-zone tokens: `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`.

Do not read, list or open any other folder, sibling scene or older project, even if asked to later in this session ([V3]; #9).

## 3. Audience

Class 10-12 students preparing for Assam Board (ASSEB) examinations, watching on a phone, including small phones (the 360-px-wide readability test in the ExamLeaf production rules). Language for this scene: `en-IN`. The narrator is the ExamLeaf Super Teacher: warm toward the student, exacting about the science, playful about the problem; delivery modes curious, steady, deliberate, light, reassuring (and focused for exam strategy); ordinary pace 130-155 words per minute. Your visuals must never talk down to the student, shame a wrong answer, or sound excited for its own sake.

## 4. Duration (derived from the narration)

`DURATION` equals `<cue_sheet.duration>` in seconds. You do not choose it. Frame count = `DURATION × 30` [N72]. If the narration is regenerated, only the cue sheet changes and you re-render; the scene code does not change (#63). Never speed up, trim or pad the narration, holds or pauses to hit a target length.

## 5. Style

Use the `voxel-isometric` style, version `1.0.0`, exactly as in `12_advanced_animations_with_claude/05_style_guides/voxel-isometric.md`. Read the "Digest" at the top of the guide first, then the whole body. Where the digest and the body differ, the body governs. Where this brief and the guide conflict, the stricter rule wins; if the conflict blocks the work, stop and write a blocker. Styles apply to illustrative, narrative and typographic scenes only. Anything data-bound (axes, values, equations, labelled structures) comes from fixtures and is never wobbled, boiled, drifted, tilted or push-in'd.

## 6. Reference analysis numbers

Reference analysis file: `none`. If this says `none`, there is no reference: use the style tokens' defaults and skip the rest of this section. Otherwise read these fields:
- `fps`, `duration_s`, `shot_lengths_s` (median, lower and upper quartile), `cut_rhythm`, `text_hold_estimates_s`, `palette_swatches`.
Use them only to set pacing: the median shot length is a guide for average beat length; the text-hold estimates are compared with section 12, and the longer one wins. A reference video is for analysis only. Never reuse its artwork, characters, layouts, music or text (copyright; edge case on references).

## 7. Brand tokens and palette

Colours, sizes and timings come from `jobs/short-csv12-s02/inputs/brand_tokens.json` and the style tokens, never from memory or taste. ExamLeaf light theme only (background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00` for conditions only, purple `#6E44AA`, red `#B42318` for error markers only). One dominant highlight at a time. A quantity keeps its colour across scenes. Do not rely on colour alone to distinguish things. Text at least 4.5:1 and essential graphics at least 3:1 on the actual rendered background.

Sizes on the 1080-wide master: essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; use the style tokens for display sizes.

## 8. Fonts: allow and ban

- Allowed: Noto Sans semibold (DOM labels and legend, never inside WebGL), Inter (captions and labels only), KaTeX fonts (not used in this scene)
- Banned as display or title faces: Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter (as a display face), Times New Roman, Comic Sans, Papyrus

Fonts are vendored files in the workspace, loaded before the first frame resolves. Explicitly load each family and weight you use with sample text that exercises its glyphs (for example a Devanagari conjunct): `document.fonts.ready` alone does not trigger loads for faces nothing has requested yet (contract §6). Set `lang` on text containers (`en`, `hi`, `as`). No remote fonts, no CDN, no system-font fallback at render time. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point (#55). Test confusable glyphs (I/l/1, O/0, minus signs, decimal points, subscripts, superscripts, Greek letters).

## 9. Harness contract block

Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`; this block is a summary.
- Start from `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`.
- Canvas 1080×1920 (9:16), 30 fps (fps is a parameter; times are in seconds). Lay out in fixed pixels; never use `vw`, `vh`, `innerWidth` or `innerHeight`. Never author at 16:9 and crop (#49).
- Set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]. The renderer seeks and never calls `play()` [N68]. Every frame is produced by `seek(t)` alone.
- The scene is a pure function of `t` [N61]. All repeats are finite. All randomness is seeded and stateless.
- Polling uses `setTimeout` loops with a deadline, never `requestAnimationFrame` (it does not fire in BeginFrame mode, #19) [N69].
- Video-heavy scenes use one worker (#20) [N70]; prefer still images and sprites.
- Declare `window.SCENE_META.contract = "1.0.0"`, expose `window.ready`, and report problems through `window.__errors`. The scene emits no audio (no WebAudio).
- Production target is conformance level L2. `node lint_seek_contract.js --level 2` (add `--hf` for a HyperFrames scene) must exit 0, and your lint report must show zero errors.

## 10. Determinism block

- Allowed randomness: a seeded, stateless keyed PRNG only (key = scene ID + element ID + step). Same key, same value, in any seek order.
- Forbidden: `Math.random`, `Date.now`, `performance.now`, `setInterval`, `requestAnimationFrame` loops, wall-clock CSS animations or transitions, autoplaying media, infinite repeats (`repeat: -1`, `infinite`).
- Idle and wobble loops use a finite repeat computed as `ceil(DURATION / period)` and end at the rest pose.
- Stop-motion boil steps are `floor(t × boil_fps)` with `boil_fps` from the style tokens.
- Two renders of the same scene must give identical frame hashes. If they do not, the scene fails (#17).

## 11. Safe zones and layout

- Insets come only from `vertical_safe_zones.tokens.json`. Do not invent insets. If the file is missing, stop and write a blocker (`SAFE_ZONES_MISSING`). If `platform_insets_px.measured` is false, use the insets named by `applies_until_measured` and record "provisional insets" in `manifest.json`.
- Side margin at least 96 px, and never inside the file's left/right insets.
- Stacked zones between the top and bottom insets, with shares read from `zones` in the same file (0.22 title, 0.54 visual, 0.24 caption in token version 1.0.0; the file wins). A three-row title may grow the title zone to at most 30%, taking space from the visual zone and never from the caption zone [Recommendation].
- Centre content in the horizontal band from `max(96, insets.left)` to `1080 - max(96, insets.right)`, not in the full frame.
- Backgrounds and decoration may bleed to the full frame; everything a learner must read or notice stays inside the safe box (#51).
- The caption zone holds the caption track only. Never place artwork text, kinetic text or tags over it.

## 12. Hold times

- Headlines: fully readable for at least 1.2 s before the next major transition [N60], or 0.3 s × word count if that is longer. Indic text: multiply by 1.5.
- Equations (rendered from fixtures): stay on screen until the narration has finished reading them plus 0.5 s, and at least 2 s after an important transformation (longer when necessary).
- During any `think` or `pause-video` window in the cue sheet, nothing moves except what the cue sheet says; the answer stays hidden.
- No major transition inside a hold.

## 13. Sync rule

Read every time from the cue sheet (`cues[].at`, `words[].t0/t1`, `sfx[].at`); never hard-code a time. Each reveal lands on, or up to 0.05 s before, the word it illustrates ([V4-MP]): a reveal cue's `at` must satisfy `word.t0 - 0.05 <= at <= word.t0`, and the cue-sheet validator rejects a later one. The entrance may then run on for up to about 0.30 s. One sentence is one visual beat. Never put everything on screen at once; reveal it across the scene. For each `sfx[]` entry there must be a matching visual event within one frame; list any mismatch in `scene_notes.md`. Your scene emits no audio; music and SFX stems are made by `examleaf-audio-compose` from the same cue sheet.

## 14. Fixtures (read-only) and the accuracy invariant

Every number, unit, formula, label, arrow direction, angle, ratio and graph shape on screen is a field of a fixture listed in section 2. Copy strings from fixture fields; do not retype, round, translate or reformat them. Mark every science glyph's element with `data-fx="path.to.field"` so QA can diff the rendered text against the fixture (contract §9). Approved on-screen text from the script bundle is staged as `display_text` and treated the same way: mark it `data-fx="display_text.<id>"` [Recommendation]. Decorative layers must not encode data: no position, size, count or colour that a student could read as a value. If you need a value that no fixture provides, stop and write `blockers.json` (`FIXTURE_MISSING`); never invent or look it up (#12). Decoration must not change an angle, a ratio or a direction that the lesson teaches (a stylised wobble must not bend a ray). No camera effect (push-in, pan, shake) during a measurement, axis or label reveal (#64).

## 15. FORBIDDEN

1. Altering, adding, removing or paraphrasing narration or on-screen wording that is not in the approved script bundle (#11).
2. Researching, looking up, estimating or recalling facts; any on-screen science glyph that is not traceable to a fixture field (#12).
3. Asking any image model to draw text, numbers, symbols, formulae or labelled diagrams (#54). All text is code-built.
4. Infinite loops or repeats (#18), wall-clock timing (#15), `Math.random` or any unseeded randomness (#17), `requestAnimationFrame` polling (#19).
5. Reading any folder other than those in section 2 (#9).
6. "Don't stop until it is perfect" or any open-ended iteration: you may run at most 3 fix rounds (#60).
7. Full-frame flashes, rapid luminance changes, strobing (#56); the safe-zone tokens' `flash_policy` bans full-frame flashes and caps flashes at 3 per second.
8. Text outside the safe box or over the caption zone (#51).
9. Downloading assets, calling the network, installing packages, or calling any MCP, provider or paid generation tool.
10. Unlicensed, scraped or reference-creator artwork; unlicensed or trending audio; voice cloning or imitating a real teacher.
11. Stereotypes in setting or characters; identity-based praise; shaming a wrong answer; fake enthusiasm.
12. Putting secrets, keys or tokens in code, prompts or logs.

## 16. Iteration cap and stop rules

One fix round = run the lint, the determinism test and the rubric below, read the failures, edit, run again. Do at most 3 rounds. After the last round, or earlier if a failure needs a human decision, stop and write `blockers.json`:

`{ "code": "<UPPER_SNAKE>", "message": "<what failed, in one sentence>", "evidence": ["<file or frame time>"], "needs_human": true }`

Rubric: (1) lint zero errors at level 2; (2) double-render frame hashes identical; (3) every rendered string equals a fixture field or approved script token; (4) safe-box and contrast checks pass on stills at cue times; (5) holds met, and every reveal cue `at` within `[t0 - 0.05, t0]` of its word; (6) no flash; (7) the reduced-motion variant renders. Do not self-approve; approval belongs to the humans and to `examleaf-anim-qa`.

## 17. Deliverables and file layout

Write files only; do not paste scene code into chat. Layout inside `jobs/short-csv12-s02/`:

```text
scene/scene.html            the scene (or the harness's scene file)
scene/scene.js, scene.css   optional splits; code only, no downloads
scene/assets/               code-made assets (SVG, procedural textures); vendored fonts are staged by the pipeline
scene_notes.md              which cue drives each reveal; which fixture field drives each on-screen value; the seed constants used
lint_report.json            output of lint_seek_contract.js (zero errors)
manifest.json               hashes of script, cue sheet, fixtures, tokens, style guide as read; list of files written; loops used (0-3)
preview/                    optional stills at cue times for the reviewer
blockers.json               only if you stopped
```

Provide a reduced-motion variant as a scene configuration flag that changes only motion (no boil, idle, drift, shake or push-in; transitions become 150-300 ms fades) and never changes content or hold times.

Your final chat message is one short JSON object: `{ "status": "done" | "blocked", "files": [...], "lint_errors": 0, "loops_used": N, "blockers": [...] }`.

## 18. Review checkpoint

- Do not write scene code until `jobs/short-csv12-s02/storyboard/approval_record.json` exists, is approved, and its `script_sha256` equals `<64 hex>`. If not, stop with `STORYBOARD_NOT_APPROVED`.
- When the rubric passes, stop. The pipeline then runs `examleaf-anim-qa`, audio and caption QA, and human review. Changing the style, the script or the layout after approval re-opens the gate.

## 19. Tools and environment

You may read and write files inside the workspace and run the harness lint and render commands named in the workspace's README. No network, no installs, no MCP tools, no provider calls. Credits and tokens are capped by the pipeline, not by this prompt; if you receive a budget-exceeded signal, stop and write a blocker.

## 20. Non-negotiable constraints (assembler-generated, identical across briefs)

1. **Harness contract.** Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`: set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]; the renderer seeks and never calls `play()` [N68]. Frame count = DURATION x fps [N72].
2. **Determinism.** Every visual state is a pure function of `t` [N61]. No `Date.now()`, `performance.now()`, `setInterval`, `requestAnimationFrame` loops, or `Math.random`; use the seeded PRNG only. Every idle loop has a finite repeat count ([V4-MP]). Two renders must produce identical frame hashes.
3. **Canvas and safe zones.** 1080x1920. Keep text and critical diagram parts inside the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`; do not invent insets.
4. **Fonts.** Use only: Noto Sans semibold (DOM labels and legend, never inside WebGL), Inter (captions and labels only), KaTeX fonts (not used in this scene). Never use: Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter (as a display face), Times New Roman, Comic Sans, Papyrus [N51][N55]. Preload fonts before the first frame resolves. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point.
5. **Hold times.** Headlines stay fully readable for at least 1.2 s [N60]; Indic text multiplies that by 1.5. Equations stay until the narration finishes reading them plus 0.5 s.
6. **Sync rule.** Read every time from the cue sheet (`cues[].at`, `words[]`); never hard-code times. Each reveal lands on, or about 0.05 s before, its word; one sentence = one visual beat ([V4-MP]).
7. **Science accuracy.** Every number, unit, formula, label, arrow direction and graph shape on screen comes from a fixture field listed above. Decoration must not change an angle, ratio or direction the lesson teaches.
8. **Forbidden.** Do not alter, paraphrase, shorten or add narration or on-screen wording beyond the approved script. Do not research, look up or infer facts. Do not ask an image model to draw text, labels, numbers or formulas. Do not add full-frame flashes.
9. **Isolation.** Do not read or inspect any folder outside `jobs/short-csv12-s02/` and the paths listed in section 2; do not open older projects or sibling scenes [V3].
10. **Iteration cap.** At most 3 fix rounds. If the scene still fails lint, the determinism test or review, stop and return a structured blocker; do not keep going "until perfect".
````

## G. Style-specific acceptance checks (added to the rubric in section 16 of the brief)

- [ ] All 64 scientific voxels match the fixture cell for cell; decorative voxels come from the keyed PRNG and are identical on every render.
- [ ] Camera: orthographic, azimuth 45 degrees, elevation about 35.264 degrees; no camera movement during any label reveal; dwell on the labelled view at least 2 s.
- [ ] Labels are DOM overlays equal to fixture strings, each marked `data-fx`; anchors within 4 px of voxel centres at every labelled frame; no text in WebGL; every cue `at` is in [t0 - 0.05 s, t0] of its word.
- [ ] Legend shows both species with colour and a mark; no red or amber species; schematic note visible.
- [ ] Highlight is localised, at most 1.25 brightness, one at a time; no full-frame luminance change.
- [ ] No `setAnimationLoop` or `requestAnimationFrame`; on `seek(t)` the scene renders once.
- [ ] Double render on the pinned box gives identical frame hashes; the software-GL run is visually equivalent; the PNG sequence imports as a clip without an extra video decoder.
- [ ] Reduced-motion variant: no orbit, no stagger; the lattice fades in over 150-300 ms.
- [ ] Safe box respected; captions in the caption zone only.

## H. Expected output and final message

```text
jobs/short-csv12-s02/
  inputs/                 (read-only, staged by the pipeline)
  storyboard/             (read-only; approval_record.json written by the approval service)
  scene/scene.html        window.DURATION = 10.8; async window.seek(t)
  scene/scene.js, scene.css
  scene/assets/           code-made assets only
  scene_notes.md          cue -> reveal map; fixture field -> on-screen value map; seed constants
  lint_report.json        zero errors
  manifest.json           hashes as read, files written, loops used
  preview/                stills at cue times (optional)
  scene/render/             PNG sequence exported on the pinned render box
```

Final chat message when it passes:

```json
{
  "status": "done",
  "files": [
    "scene/scene.html",
    "scene/scene.js",
    "scene/scene.css",
    "scene_notes.md",
    "lint_report.json",
    "manifest.json"
  ],
  "lint_errors": 0,
  "loops_used": 1,
  "blockers": []
}
```

Final chat message if blocked (example):

```json
{
  "status": "blocked",
  "files": ["blockers.json"],
  "lint_errors": 0,
  "loops_used": 0,
  "blockers": [
    {
      "code": "WEBGL_CONTEXT_LOST",
      "message": "The WebGL context was lost during frame 112; stopping instead of continuing silently.",
      "evidence": ["inputs/"],
      "needs_human": true
    }
  ]
}
```

## I. Style digest (for reviewers; the agent reads it at the top of the guide)

1. three.js with an `InstancedMesh` of unit cubes, an orthographic camera at the true isometric angle, flat baked lighting. No real lights, no shadow maps, no perspective.
2. Voxel positions and species for anything scientific (lattices, organelle blocks) come from a fixture's integer grid. Seeded randomness is for decoration only.
3. Rendering is seek-pure: on `seek(t)` set instance transforms from `t` and render once. Never `setAnimationLoop` or `requestAnimationFrame` (#15, #19).
4. Headless WebGL varies by machine (#65). Render on the pinned render box only; test a software-GL fallback; export a PNG sequence and import it as a clip (#20).
5. Labels are DOM overlays from fixture strings, positioned by projecting voxel centres at time `t`. No text in WebGL.
6. Uses: cubic lattices, stylised cell and organelle schematics, "island of concepts" recaps. Not for bond angles, molecular geometry, hexagonal lattices, field lines, physics simulations, or anything where angle or proportion carries the science.
7. Palette: ExamLeaf tokens; avoid red and amber for species (they carry error and condition meaning); never colour alone for species (add legend tags).
8. Camera: fixed or a slow orbit as a function of `t`, with no movement during label reveals (#64).
9. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px; captions in the bottom zone.
10. Cost: zero credits; render-box time is the cost (log it).

## J. What this example is designed to catch

- **#65** headless WebGL variance: pinned box, software-GL check, PNG-sequence export.
- **#12 / accuracy:** every scientific voxel is a fixture cell; the agent cannot invent a lattice.
- **#15, #19** time: render once per `seek(t)`; no animation loop.
- **#17** randomness: ground tufts are keyed, not `Math.random`.
- **#20** decoders: a PNG sequence instead of a video element.
- **#64** camera effects: the orbit sits in a window with no label reveals.
- **Colour alone (ROOT/02 D4):** legend with marks; blue and teal are near in luminance.
- **Colour meaning:** red and amber are kept for error and condition roles, not species.
- **Scope creep:** the melt comparison is explicitly out of scope; no invented ion motion.
