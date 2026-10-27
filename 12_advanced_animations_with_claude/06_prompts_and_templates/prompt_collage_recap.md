# Filled brief: paper-collage recap for Reel CSV 10 ("Balance this without changing the substance.")

**Reel:** CSV ID 10 (Class 10 Chemistry, balancing equations, P0, target 30 s). Hook in the response wording: "Balance this without changing the substance." (the CSV wording is "Balance the equation WITHOUT changing the substance."). Caption first line: "Change the count of particles, not the identity of the formula." CTA: "Try the next balancing question." Scientific check: use an approved reaction and preserve atom counts.
**This scene:** s05 of the Reel, the recap and CTA (11.4 s). The atom-count tiles and the balancing itself are data-bound scenes (earlier in the Reel) built from validated fixtures. This scene only calls back the approved sandwich analogy and shows the fixture-driven equation as a tag.
**Analogy contract:** the canteen sandwich analogy comes from the analogy card `CHEM-COEFF-SANDWICH-01` (mapping: number of sandwiches to coefficient; ingredients per sandwich to atoms per molecular copy; non-mapping: molecules are not sandwiches, a recipe order is not a reaction mechanism, no reaction conditions). The card in the Super Teacher pack is marked DRAFT_HUMAN_REVIEW_REQUIRED, so **this brief must not be issued until the card is approved**.
**Why collage here:** a recap that needs warmth and a gag-free callback; zero-credit tier A (code-made paper shapes) is the default, so no Higgsfield call is needed.

**Style:** `paper-collage-vertical@1.0.0` | **Version of this example:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** EXAMPLE. Every input below is illustrative so that the brief can be read end to end. In a real job the pipeline supplies approved inputs; the animation agent never authors them, and nothing here has been run.

**Evidence labels:** [V#]/[N#] are cited from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement; [Hypothesis] = untested. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Hook text and CSV IDs come from `01_business_model/REEL_BACKLOG_36.md` (the CSV ID is the stable ID).

## How this example is built

The generator filled `brief_template.md` from the job request in section A. The collage recap uses tier A assets (code-drawn paper shapes, tape, tags, simple sandwich cutouts as SVG), so the storyboard estimate is 0 credits. Sections B-E are staged inputs; F is the brief.

## A. Job request (`brief_request.json`, the input to `examleaf-anim-brief`)

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv10-s05",
  "lesson_id": "chem-10-balancing",
  "language": "en-IN",
  "route": {
    "tag": "illustrative",
    "source": "examleaf-storyboard-route",
    "scene_spec_id": "short-csv10-s05"
  },
  "script": {
    "path": "jobs/short-csv10-s05/inputs/approved_script.md",
    "sha256": "<64 hex>",
    "approval_status": "approved",
    "segment_text": "Coefficients count the copies. Order more sandwiches, and every ingredient multiplies. The subscripts stay put. Try the next balancing question."
  },
  "style": {
    "id": "paper-collage-vertical",
    "version": "1.0.0",
    "guide_path": "12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md",
    "tokens_path": "12_advanced_animations_with_claude/05_style_guides/style_tokens.json"
  },
  "cue_sheet": {"path": "jobs/short-csv10-s05/inputs/cue_sheet.json", "sha256": "<64 hex>"},
  "brand_tokens": {"path": "jobs/short-csv10-s05/inputs/brand_tokens.json", "sha256": "<64 hex>"},
  "fixtures": [
    {
      "id": "display-text-short-csv10-s05",
      "path": "jobs/short-csv10-s05/inputs/display_text.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["t_coefficient", "t_subscript", "t_cta_words"]
    },
    {
      "id": "chem10-balance-h2-o2",
      "path": "jobs/short-csv10-s05/inputs/chem10-balance-h2-o2.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["equation.display_latex"]
    },
    {
      "id": "analogy-CHEM-COEFF-SANDWICH-01",
      "path": "jobs/short-csv10-s05/inputs/analogy-CHEM-COEFF-SANDWICH-01.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["visual_counts.sandwiches"]
    }
  ],
  "fonts": {
    "allow": [
      "Alfa Slab One",
      "Bowlby One",
      "Bungee",
      "Lilita One and Bebas Neue (Latin ransom tiles",
      "3-5 per title)",
      "Caveat Brush (punchlines)",
      "Patrick Hand (plain-word labels only)",
      "Inter and Noto Sans (science tags and captions)",
      "KaTeX fonts (the equation tag)"
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
  "workspace": "jobs/short-csv10-s05/",
  "approval_record": {"path": "jobs/short-csv10-s05/storyboard/approval_record.json", "sha256": "<64 hex>"},
  "creative_direction": "Collage recap for Reel CSV 10, scene s05, 11.4 s. Paper sheet slides in from the bottom at 0.00-0.60 s (`power3.out`, settles from a slight rotation, torn leading edge, drop shadow). Background: pale-blue watercolour sky with layered torn-paper hills; the lower hills are painted as simple green strips with row marks (a tea-garden hillside, background only, no people). The top 10% of the visual zone stays empty sky so the expanded title zone never overlaps content. Layout (central prop with small tags): a canteen counter with a plate in the middle of the visual zone; hero (student-age, plain school-style outfit, from the hero sheet) at the lower left. Beats: at \"copies\" (1.90 s) the tag `t_coefficient` pops on a cream tag with washi tape; at \"Order\" (3.05 s) one sandwich cutout pops; at \"sandwiches\" (3.60 s) the sandwich multiplies 1, 2, 3 using the count in the analogy card (`visual_counts.sandwiches` = 3), with ingredient doodles multiplying alongside at \"multiplies\" (5.25 s); at \"subscripts\" (6.65 s) the fixture-driven equation tag pops in as a unit (fixture string via KaTeX on an `#F7F9FC` tag, no wobble, boil or tilt) and stays to the end, then `t_subscript` pops at \"stay\" (7.30 s); at \"Try\" (8.65 s) the hero switches to the tick pose; the ransom words of `t_cta_words` (NEXT / BALANCING / QUESTION) land one per row in the title zone (which may grow to 30% for three rows) at 9.00, 9.30 and 9.90 s with letters 0.045 s apart and hold at least 1.2 s. No joke, no tear, no flip in this scene. No music under the narration; SFX only from the cue sheet."
}
```

## B. Example approved script segment (illustrative; the real text comes from the approved script bundle)

| ID | Mode | Spoken text | Notes |
|---|---|---|---|
| r1 | steady | Coefficients count the copies. | Display text `t_coefficient`: "Coefficient = copies". |
| r2 | steady | Order more sandwiches, and every ingredient multiplies. | From the approved analogy card; no number is spoken, the visual count (3) comes from the card. |
| r3 | deliberate | The subscripts stay put. | Display text `t_subscript`: "Subscript = inside one". The equation tag is a fixture field. |
| r4 | curious | Try the next balancing question. | The single CTA; `t_cta_words`: "NEXT BALANCING QUESTION". |

18 words in total, about 7.7 s of speech at 140 wpm plus pauses. A zero-joke recap is deliberate: zero light moments is acceptable (ROOT/03), and a 30-second Reel has little room.

## C. Example cue sheet (`inputs/cue_sheet.json`; timings are PLANNED until the voice is measured)

Conforms to `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`. Checked with `python3 validate_cue_sheet.py`: valid, 0 errors, one warning (the null narration hash, expected while timings are PLANNED). `--production` would reject it (`alignment_source` is `example`, the hashes are placeholders). Free-form extras live under `meta`. Reveal cues carry `element_id` and `word_index`, and each `at` is in `[t0 - 0.05, t0]` of its word.

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv10-s05",
  "fps": 30,
  "duration": 11.4,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": null,
  "script_sha256": "eb293adcaee4de16c0f672d7b6c49f7aa4bade776ef48f584a61eb0d659d016d",
  "words": [
    {"w": "Coefficients", "t0": 0.9, "t1": 1.5},
    {"w": "count", "t0": 1.5, "t1": 1.85},
    {"w": "the", "t0": 1.85, "t1": 1.95},
    {"w": "copies", "t0": 1.95, "t1": 2.45},
    {"w": "Order", "t0": 3.1, "t1": 3.4},
    {"w": "more", "t0": 3.4, "t1": 3.65},
    {"w": "sandwiches", "t0": 3.65, "t1": 4.3},
    {"w": "and", "t0": 4.3, "t1": 4.42},
    {"w": "every", "t0": 4.42, "t1": 4.7},
    {"w": "ingredient", "t0": 4.7, "t1": 5.3},
    {"w": "multiplies", "t0": 5.3, "t1": 5.95},
    {"w": "The", "t0": 6.6, "t1": 6.7},
    {"w": "subscripts", "t0": 6.7, "t1": 7.35},
    {"w": "stay", "t0": 7.35, "t1": 7.65},
    {"w": "put", "t0": 7.65, "t1": 7.95},
    {"w": "Try", "t0": 8.7, "t1": 8.95},
    {"w": "the", "t0": 8.95, "t1": 9.05},
    {"w": "next", "t0": 9.05, "t1": 9.35},
    {"w": "balancing", "t0": 9.35, "t1": 9.95},
    {"w": "question", "t0": 9.95, "t1": 10.45}
  ],
  "beats": [],
  "cues": [
    {"id": "c_sheet", "at": 0.0, "kind": "transition", "element_id": "sheet"},
    {"id": "c_hero_in", "at": 0.55, "kind": "reveal", "element_id": "hero_in"},
    {"id": "c_tag_coeff", "at": 1.9, "kind": "reveal", "element_id": "tag_coeff", "word_index": 3},
    {
      "id": "c_sandwich_1",
      "at": 3.05,
      "kind": "reveal",
      "element_id": "sandwich_1",
      "word_index": 4
    },
    {
      "id": "c_sandwich_x3",
      "at": 3.6,
      "kind": "reveal",
      "element_id": "sandwich_x3",
      "word_index": 6
    },
    {
      "id": "c_ingredients",
      "at": 5.25,
      "kind": "reveal",
      "element_id": "ingredients",
      "word_index": 10
    },
    {"id": "c_equation", "at": 6.65, "kind": "reveal", "element_id": "equation", "word_index": 12},
    {"id": "c_tag_sub", "at": 7.3, "kind": "reveal", "element_id": "tag_sub", "word_index": 13},
    {"id": "c_hero_tick", "at": 8.65, "kind": "reveal", "element_id": "hero_tick", "word_index": 15},
    {"id": "c_cta_next", "at": 9.0, "kind": "reveal", "element_id": "cta_next", "word_index": 17},
    {
      "id": "c_cta_balancing",
      "at": 9.3,
      "kind": "reveal",
      "element_id": "cta_balancing",
      "word_index": 18
    },
    {
      "id": "c_cta_question",
      "at": 9.9,
      "kind": "reveal",
      "element_id": "cta_question",
      "word_index": 19
    }
  ],
  "sfx": [
    {"file": "sfx/paper_swish.wav", "at": 0.0, "gain_db": -14},
    {"file": "sfx/boing.wav", "at": 0.55, "gain_db": -16},
    {"file": "sfx/pop.wav", "at": 1.9, "gain_db": -14},
    {"file": "sfx/pop.wav", "at": 3.05, "gain_db": -14},
    {"file": "sfx/boing.wav", "at": 3.6, "gain_db": -16},
    {"file": "sfx/pop.wav", "at": 6.65, "gain_db": -14},
    {"file": "sfx/pop.wav", "at": 7.3, "gain_db": -14},
    {"file": "sfx/tap.wav", "at": 9.0, "gain_db": -16},
    {"file": "sfx/tap.wav", "at": 9.3, "gain_db": -16},
    {"file": "sfx/tap.wav", "at": 9.9, "gain_db": -16}
  ],
  "meta": {
    "note": "EXAMPLE ONLY. Timings are PLANNED, not aligned to real audio, and the wording is not an approved ExamLeaf script.",
    "status": "PLANNED",
    "script_text": "Coefficients count the copies. Order more sandwiches, and every ingredient multiplies. The subscripts stay put. Try the next balancing question.",
    "script_sha256_of": "UTF-8 bytes of meta.script_text",
    "narration_audio_sha256_of": "null while no narration exists (production requires a hash)",
    "sentences": [
      {"id": "r1", "t0": 0.9, "t1": 2.45, "mode": "steady"},
      {"id": "r2", "t0": 3.1, "t1": 5.95, "mode": "steady"},
      {"id": "r3", "t0": 6.6, "t1": 7.95, "mode": "deliberate"},
      {"id": "r4", "t0": 8.7, "t1": 10.45, "mode": "curious"}
    ],
    "think_windows": [],
    "beats_note": "empty: no music bed in this scene, so no beat grid"
  }
}
```

## D. Example inputs the scene may read

**Fixture excerpt (`chem10-balance-h2-o2.json`).** EXAMPLE, NOT A VALIDATED FIXTURE; in production the science pipeline supplies and signs it:

```json
{
  "fixture_id": "chem10-balance-h2-o2",
  "status": "EXAMPLE_NOT_A_VALIDATED_FIXTURE",
  "equation": {
    "display_latex": "2\\mathrm{H}_2 + \\mathrm{O}_2 \\rightarrow 2\\mathrm{H}_2\\mathrm{O}",
    "spoken_text": "two H two plus O two gives two H two O"
  }
}
```

**Analogy card excerpt (`analogy-CHEM-COEFF-SANDWICH-01.json`).** EXAMPLE of an approved card (status must read APPROVED before issue):

```json
{
  "id": "CHEM-COEFF-SANDWICH-01",
  "status": "APPROVED_EXAMPLE",
  "mapping": {"number_of_sandwiches": "coefficient", "ingredients_per_sandwich": "atoms per molecular copy"},
  "non_mapping": ["Molecules are not sandwiches.", "A recipe order is not a reaction mechanism.", "The analogy does not establish reaction conditions or feasibility."],
  "visual_counts": {"sandwiches": 3},
  "formal_return": "Coefficient changes copies; subscript changes molecular composition."
}
```

**Approved display text:** `t_coefficient` "Coefficient = copies"; `t_subscript` "Subscript = inside one"; `t_cta_words` "NEXT BALANCING QUESTION".

**Hero sheet:** `inputs/assets/hero_sheet.png` with its SHA-256 and pose atlas (pointing, thinking, puzzled, checking, writing, waving, quiet-win); every hero frame references it (#48).

## E. Example storyboard beats (excerpt of the approved `storyboard/beats.json`)

```json
{
  "schema_version": "1.0.0",
  "scene_id": "short-csv10-s05",
  "timing_status": "PLANNED",
  "beats": [
    {
      "beat_id": "b01",
      "panel": 1,
      "sentence_ids": ["r1"],
      "merged_from": [],
      "planned_start_s": 0.0,
      "planned_end_s": 2.45,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "A pale-blue watercolour sky with torn-paper hills rises into frame on a paper sheet from the bottom; the hero hops up from behind the foreground strip and points at a tag that reads coefficient equals copies.",
      "fixture_refs": [],
      "on_screen_text_refs": ["t_coefficient"],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b02",
      "panel": 2,
      "sentence_ids": ["r2"],
      "merged_from": [],
      "planned_start_s": 3.1,
      "planned_end_s": 5.95,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "A plate on a canteen counter: one sandwich cutout, then three, with small ingredient doodles multiplying with them.",
      "fixture_refs": ["analogy-CHEM-COEFF-SANDWICH-01"],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b03",
      "panel": 3,
      "sentence_ids": ["r3"],
      "merged_from": [],
      "planned_start_s": 6.6,
      "planned_end_s": 7.95,
      "voice_mode": "deliberate",
      "route": "data-bound",
      "visual_brief": "A fixture-driven equation tag on a plain paper card; a second tag says subscript equals inside one. The equation is a placeholder here and is drawn from the fixture in the build.",
      "fixture_refs": ["chem10-balance-h2-o2"],
      "on_screen_text_refs": ["t_subscript"],
      "placeholder": true,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b04",
      "panel": 4,
      "sentence_ids": ["r4"],
      "merged_from": [],
      "planned_start_s": 8.7,
      "planned_end_s": 10.45,
      "voice_mode": "curious",
      "route": "illustrative",
      "visual_brief": "The hero makes a tick; three ransom-tile rows land in the title zone: NEXT, BALANCING, QUESTION.",
      "fixture_refs": [],
      "on_screen_text_refs": ["t_cta_words"],
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
# Animation brief: short-csv10-s05

**Lesson:** chem-10-balancing | **Language:** en-IN | **Route:** illustrative | **Style:** paper-collage-vertical@1.0.0
**Author run:** model `<pinned full model ID, Opus 5.5>`, effort `high` (set explicitly; ultracode is never used), at most 3 fix rounds.
**Workspace:** `jobs/short-csv10-s05/` (work only here)
**Brief level:** L2 structured brief with references ([V2]). Any L3 orchestration (voice, music, paid image generation) is done by ExamLeaf's pipeline adapters before or after this job, never by you. You have no MCP tools.

## 1. Goal

Build one seek-pure 1080×1920 scene for `short-csv10-s05` that animates the approved narration in the `paper-collage-vertical` style, and nothing else. You write scene code only. You do not write, edit, shorten, paraphrase or "improve" any narration or on-screen wording, and you do not research any fact.

Creative direction from the approved storyboard:
Collage recap for Reel CSV 10, scene s05, 11.4 s. Paper sheet slides in from the bottom at 0.00-0.60 s (`power3.out`, settles from a slight rotation, torn leading edge, drop shadow). Background: pale-blue watercolour sky with layered torn-paper hills; the lower hills are painted as simple green strips with row marks (a tea-garden hillside, background only, no people). The top 10% of the visual zone stays empty sky so the expanded title zone never overlaps content. Layout (central prop with small tags): a canteen counter with a plate in the middle of the visual zone; hero (student-age, plain school-style outfit, from the hero sheet) at the lower left. Beats: at "copies" (1.90 s) the tag `t_coefficient` pops on a cream tag with washi tape; at "Order" (3.05 s) one sandwich cutout pops; at "sandwiches" (3.60 s) the sandwich multiplies 1, 2, 3 using the count in the analogy card (`visual_counts.sandwiches` = 3), with ingredient doodles multiplying alongside at "multiplies" (5.25 s); at "subscripts" (6.65 s) the fixture-driven equation tag pops in as a unit (fixture string via KaTeX on an `#F7F9FC` tag, no wobble, boil or tilt) and stays to the end, then `t_subscript` pops at "stay" (7.30 s); at "Try" (8.65 s) the hero switches to the tick pose; the ransom words of `t_cta_words` (NEXT / BALANCING / QUESTION) land one per row in the title zone (which may grow to 30% for three rows) at 9.00, 9.30 and 9.90 s with letters 0.045 s apart and hold at least 1.2 s. No joke, no tear, no flip in this scene. No music under the narration; SFX only from the cue sheet.

If this scene belongs to a Short (20-60 s, `ShortSpec`): hook in the first 3 s, a prediction window in 3-8 s (default `think` = 6 s, answer hidden), then the explanation, then one next action. Re-composed for 9:16, never cropped from 16:9.

## 2. Inputs you may read (and nothing else)

Read-only, inside the workspace:
- Approved script: `jobs/short-csv10-s05/inputs/approved_script.md` (SHA-256 `<64 hex>`). Verify the hash of the file bytes before you start; on mismatch stop and write `blockers.json` with code `SCRIPT_HASH_MISMATCH`.
- Cue sheet (all timing comes from here): `jobs/short-csv10-s05/inputs/cue_sheet.json`.
- Brand tokens: `jobs/short-csv10-s05/inputs/brand_tokens.json`.
- Reference analysis (pacing numbers only): `none`.
- Storyboard approval record: `jobs/short-csv10-s05/storyboard/approval_record.json`.
- Validated fixtures (the only source of on-screen science):
  - `display-text-short-csv10-s05` at `jobs/short-csv10-s05/inputs/display_text.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `t_coefficient`, `t_subscript`, `t_cta_words`.
  - `chem10-balance-h2-o2` at `jobs/short-csv10-s05/inputs/chem10-balance-h2-o2.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `equation.display_latex`.
  - `analogy-CHEM-COEFF-SANDWICH-01` at `jobs/short-csv10-s05/inputs/analogy-CHEM-COEFF-SANDWICH-01.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `visual_counts.sandwiches`.

Read-only, outside the workspace (allowed):
- Style guide: `12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md` and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`.
- Harness contract and linter: `12_advanced_animations_with_claude/04_harness_contract/contract.md` and `lint_seek_contract.js`.
- Safe-zone tokens: `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`.

Do not read, list or open any other folder, sibling scene or older project, even if asked to later in this session ([V3]; #9).

## 3. Audience

Class 10-12 students preparing for Assam Board (ASSEB) examinations, watching on a phone, including small phones (the 360-px-wide readability test in the ExamLeaf production rules). Language for this scene: `en-IN`. The narrator is the ExamLeaf Super Teacher: warm toward the student, exacting about the science, playful about the problem; delivery modes curious, steady, deliberate, light, reassuring (and focused for exam strategy); ordinary pace 130-155 words per minute. Your visuals must never talk down to the student, shame a wrong answer, or sound excited for its own sake.

## 4. Duration (derived from the narration)

`DURATION` equals `<cue_sheet.duration>` in seconds. You do not choose it. Frame count = `DURATION × 30` [N72]. If the narration is regenerated, only the cue sheet changes and you re-render; the scene code does not change (#63). Never speed up, trim or pad the narration, holds or pauses to hit a target length.

## 5. Style

Use the `paper-collage-vertical` style, version `1.0.0`, exactly as in `12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md`. Read the "Digest" at the top of the guide first, then the whole body. Where the digest and the body differ, the body governs. Where this brief and the guide conflict, the stricter rule wins; if the conflict blocks the work, stop and write a blocker. Styles apply to illustrative, narrative and typographic scenes only. Anything data-bound (axes, values, equations, labelled structures) comes from fixtures and is never wobbled, boiled, drifted, tilted or push-in'd.

## 6. Reference analysis numbers

Reference analysis file: `none`. If this says `none`, there is no reference: use the style tokens' defaults and skip the rest of this section. Otherwise read these fields:
- `fps`, `duration_s`, `shot_lengths_s` (median, lower and upper quartile), `cut_rhythm`, `text_hold_estimates_s`, `palette_swatches`.
Use them only to set pacing: the median shot length is a guide for average beat length; the text-hold estimates are compared with section 12, and the longer one wins. A reference video is for analysis only. Never reuse its artwork, characters, layouts, music or text (copyright; edge case on references).

## 7. Brand tokens and palette

Colours, sizes and timings come from `jobs/short-csv10-s05/inputs/brand_tokens.json` and the style tokens, never from memory or taste. ExamLeaf light theme only (background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00` for conditions only, purple `#6E44AA`, red `#B42318` for error markers only). One dominant highlight at a time. A quantity keeps its colour across scenes. Do not rely on colour alone to distinguish things. Text at least 4.5:1 and essential graphics at least 3:1 on the actual rendered background.

Sizes on the 1080-wide master: essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; use the style tokens for display sizes.

## 8. Fonts: allow and ban

- Allowed: Alfa Slab One, Bowlby One, Bungee, Lilita One and Bebas Neue (Latin ransom tiles, 3-5 per title), Caveat Brush (punchlines), Patrick Hand (plain-word labels only), Inter and Noto Sans (science tags and captions), KaTeX fonts (the equation tag)
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

Write files only; do not paste scene code into chat. Layout inside `jobs/short-csv10-s05/`:

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

- Do not write scene code until `jobs/short-csv10-s05/storyboard/approval_record.json` exists, is approved, and its `script_sha256` equals `<64 hex>`. If not, stop with `STORYBOARD_NOT_APPROVED`.
- When the rubric passes, stop. The pipeline then runs `examleaf-anim-qa`, audio and caption QA, and human review. Changing the style, the script or the layout after approval re-opens the gate.

## 19. Tools and environment

You may read and write files inside the workspace and run the harness lint and render commands named in the workspace's README. No network, no installs, no MCP tools, no provider calls. Credits and tokens are capped by the pipeline, not by this prompt; if you receive a budget-exceeded signal, stop and write a blocker.

## 20. Non-negotiable constraints (assembler-generated, identical across briefs)

1. **Harness contract.** Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`: set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]; the renderer seeks and never calls `play()` [N68]. Frame count = DURATION x fps [N72].
2. **Determinism.** Every visual state is a pure function of `t` [N61]. No `Date.now()`, `performance.now()`, `setInterval`, `requestAnimationFrame` loops, or `Math.random`; use the seeded PRNG only. Every idle loop has a finite repeat count ([V4-MP]). Two renders must produce identical frame hashes.
3. **Canvas and safe zones.** 1080x1920. Keep text and critical diagram parts inside the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`; do not invent insets.
4. **Fonts.** Use only: Alfa Slab One, Bowlby One, Bungee, Lilita One and Bebas Neue (Latin ransom tiles, 3-5 per title), Caveat Brush (punchlines), Patrick Hand (plain-word labels only), Inter and Noto Sans (science tags and captions), KaTeX fonts (the equation tag). Never use: Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter (as a display face), Times New Roman, Comic Sans, Papyrus [N51][N55]. Preload fonts before the first frame resolves. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point.
5. **Hold times.** Headlines stay fully readable for at least 1.2 s [N60]; Indic text multiplies that by 1.5. Equations stay until the narration finishes reading them plus 0.5 s.
6. **Sync rule.** Read every time from the cue sheet (`cues[].at`, `words[]`); never hard-code times. Each reveal lands on, or about 0.05 s before, its word; one sentence = one visual beat ([V4-MP]).
7. **Science accuracy.** Every number, unit, formula, label, arrow direction and graph shape on screen comes from a fixture field listed above. Decoration must not change an angle, ratio or direction the lesson teaches.
8. **Forbidden.** Do not alter, paraphrase, shorten or add narration or on-screen wording beyond the approved script. Do not research, look up or infer facts. Do not ask an image model to draw text, labels, numbers or formulas. Do not add full-frame flashes.
9. **Isolation.** Do not read or inspect any folder outside `jobs/short-csv10-s05/` and the paths listed in section 2; do not open older projects or sibling scenes [V3].
10. **Iteration cap.** At most 3 fix rounds. If the scene still fails lint, the determinism test or review, stop and return a structured blocker; do not keep going "until perfect".
````

## G. Style-specific acceptance checks (added to the rubric in section 16 of the brief)

- [ ] Sheet arrives 0.00-0.60 s with `power3.out`; no flash; the incoming sheet is the only transition; no exit animations.
- [ ] Die-cut borders measure 6-12 px at rest; shadows equal `0 9px 7px rgba(74,48,22,0.30)` plus `0 2px 1.5px rgba(0,0,0,0.20)`; wrapper holds the filter and the child holds the sway.
- [ ] Every text element carries `data-fx` (`display_text.<id>` or a fixture path); every cue `at` is in [t0 - 0.05 s, t0] of its word.
- [ ] The equation tag text equals the fixture string; the tag is `#F7F9FC` with ink `#14213D`; nothing wobbles, tilts or sways it; no camera effect runs while it appears.
- [ ] The sandwich count reaches exactly the card value (3); no other quantity is implied.
- [ ] Ransom tiles: letters 0.04-0.05 s apart, rotation within ±6°, jitter within ±8 px, seeded; contrast pairs used are at or above 3:1 for display glyphs of at least 72 px, or at least 4.5:1 otherwise.
- [ ] The title zone grows to at most 30% for the three CTA rows and never over the caption zone; the top 10% of the visual zone is empty.
- [ ] Hold at least 1.2 s after the last tile lands and before the scene ends; no transition inside the hold.
- [ ] Faces appear only on the hero; no atoms, ions or molecules have faces; no stereotype flags from the native reviewer.
- [ ] No music under narration; SFX only at cue-sheet times; loudness -16 LUFS +/-1, true peak at most -1 dBTP after mux.

## H. Expected output and final message

```text
jobs/short-csv10-s05/
  inputs/                 (read-only, staged by the pipeline)
  storyboard/             (read-only; approval_record.json written by the approval service)
  scene/scene.html        window.DURATION = 11.4; async window.seek(t)
  scene/scene.js, scene.css
  scene/assets/           code-made assets only
  scene_notes.md          cue -> reveal map; fixture field -> on-screen value map; seed constants
  lint_report.json        zero errors
  manifest.json           hashes as read, files written, loops used
  preview/                stills at cue times (optional)
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
      "code": "FIXTURE_MISSING",
      "message": "visual_counts.sandwiches is absent from the analogy card; I will not choose a count.",
      "evidence": ["inputs/"],
      "needs_human": true
    }
  ]
}
```

## I. Style digest (for reviewers; the agent reads it at the top of the guide)

1. 1080×1920, 30 fps, flat head-on paper diorama. No 3D, gloss, photoreal, heavy blur or glow.
2. Stacked zones inside the platform-safe box: title (top), visual (middle), accessible caption (bottom). Insets come from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them. Side margin at least 96 px.
3. Cutouts: watercolour + coloured-pencil look, white die-cut border 6-12 px, two-layer shadow `0 9px 7px rgba(74,48,22,0.30)` + `0 2px 1.5px rgba(0,0,0,0.20)`.
4. 13-colour storybook palette for artwork. Science-bearing text uses ExamLeaf tokens on an `#F7F9FC` tag, never storybook colours on cream.
5. Three kinds of text only: ransom-note titles (Latin letters per tile; Indic per word), Caveat Brush punchlines (Indic: wipe per word), small labels on washi-taped tags. Short text only.
6. Motion: back.out(2-3) pops pivoting at the feet, power3.out sheets, expo.out whips, boil at 10 fps, finite repeats, seeded PRNG, seek-driven timeline. Reveals land on, or 0.05 s before, the spoken word, times read from the cue sheet.
7. Narration is the Super Teacher's (130-155 wpm, five modes), not a storybook narrator. Storybook warmth only in hooks and recaps.
8. House loudness -16 LUFS integrated, true peak at most -1 dBTP. No music under reasoning.
9. Image models never draw text, numbers, formulas or labels (#54). Number tags on storyboard grids are added in code.
10. Forbidden: infinite repeats, Math.random/Date.now, full-frame flashes, camera effects during label reveals, per-code-point Indic animation, unlicensed or scraped images, stereotypes.

## J. What this example is designed to catch

- **#54** image-model text: tier A assets only; ransom tiles, tags and the equation are built in code.
- **#12** facts: the equation and the sandwich count come from fixtures; the agent is told not to retype them.
- **#49, #51** vertical layout: stacked zones, a title zone that is allowed to grow for three rows but not into the caption zone.
- **#55** Indic: the locale gate is closed (RD-26), but the rules are in the guide for later.
- **#56** flashes: sheet transitions only.
- **#50** hold: the CTA rows hold at least 1.2 s.
- **#64** camera effects: none near the equation tag.
- **Personification (ROOT/03 §5.3):** faces only on the hero; nothing in the chemistry has a face.
- **Draft analogy:** the brief states that it must not be issued while the card is a draft.
