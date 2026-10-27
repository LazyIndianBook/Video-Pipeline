# Filled brief: editorial comparison for Reel CSV 11 ("One pH unit: one small change?")

**Reel:** CSV ID 11 (Class 10 Chemistry, pH scale, P0, target 35 s). Hook: "One pH unit: one small change?" Caption first line: "Check what the scale represents before comparing acidity." CTA: "Open the Acids, Bases and Salts lesson." Scientific check: use the school-level pH model and the correct direction; avoid health claims.
**This scene:** s02 of the Reel, the comparison (12.2 s) that answers the hook visually: two labelled solutions one pH unit apart and a tenfold step in hydrogen ion concentration. The hook itself is a separate kinetic scene (s01).
**Why editorial:** "see the ratio" is exactly the scale-story job of this style, with every number from a fixture.

**Style:** `editorial-vox@1.0.0` | **Version of this example:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** EXAMPLE. Every input below is illustrative so that the brief can be read end to end. In a real job the pipeline supplies approved inputs; the animation agent never authors them, and nothing here has been run.

**Evidence labels:** [V#]/[N#] are cited from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement; [Hypothesis] = untested. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Hook text and CSV IDs come from `01_business_model/REEL_BACKLOG_36.md` (the CSV ID is the stable ID).

## How this example is built

The generator filled `brief_template.md` from the job request in section A. The reference analysis in section D uses **illustrative** numbers (not measured from a real video) to show where pacing numbers enter the brief.

## A. Job request (`brief_request.json`, the input to `examleaf-anim-brief`)

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv11-s02",
  "lesson_id": "chem-10-acids-bases-salts",
  "language": "en-IN",
  "route": {
    "tag": "illustrative",
    "source": "examleaf-storyboard-route",
    "scene_spec_id": "short-csv11-s02"
  },
  "script": {
    "path": "jobs/short-csv11-s02/inputs/approved_script.md",
    "sha256": "<64 hex>",
    "approval_status": "approved",
    "segment_text": "Take two solutions, one pH unit apart. The lower pH has ten times the hydrogen ion concentration. That is a tenfold step, not a small one."
  },
  "style": {
    "id": "editorial-vox",
    "version": "1.0.0",
    "guide_path": "12_advanced_animations_with_claude/05_style_guides/editorial-vox.md",
    "tokens_path": "12_advanced_animations_with_claude/05_style_guides/style_tokens.json"
  },
  "cue_sheet": {"path": "jobs/short-csv11-s02/inputs/cue_sheet.json", "sha256": "<64 hex>"},
  "brand_tokens": {"path": "jobs/short-csv11-s02/inputs/brand_tokens.json", "sha256": "<64 hex>"},
  "reference_analysis": {
    "path": "jobs/short-csv11-s02/inputs/reference_analysis.json",
    "sha256": "<64 hex>",
    "rights": "analysis_only"
  },
  "fixtures": [
    {
      "id": "display-text-short-csv11-s02",
      "path": "jobs/short-csv11-s02/inputs/display_text.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["t_headline_claim", "t_headline_support"]
    },
    {
      "id": "chem10-ph-compare-3-4",
      "path": "jobs/short-csv11-s02/inputs/chem10-ph-compare-3-4.json",
      "sha256": "<64 hex>",
      "fields_on_screen": [
        "solutions[].label_display",
        "solutions[].ph_display",
        "solutions[].h_ion_relative_count",
        "gap_display",
        "direction_note_display",
        "encoding_note_display",
        "factor_per_ph_unit_display"
      ]
    }
  ],
  "fonts": {
    "allow": [
      "Noto Serif (Bold or Black",
      "headline claim words)",
      "Noto Sans semibold (connecting words",
      "labels)",
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
  "workspace": "jobs/short-csv11-s02/",
  "approval_record": {"path": "jobs/short-csv11-s02/storyboard/approval_record.json", "sha256": "<64 hex>"},
  "creative_direction": "Editorial comparison for Reel CSV 11, scene s02, 12.2 s. Background `#F7F9FC` with static grain (3-5%); a halftone band (dots at least 6 px, ink at 6-8%) behind the title zone only. Layout: matched views, A above B, two equal cards (40-46% of the visual zone height each) with a bracket between them; A is a teal 18% tint card (`#CCE2E7`) and B is a secondary 18% tint card (`#D9DDE4`); each carries a big letter A or B so colour is never the only cue. At 0.35 s both cards enter as ONE staggered group (60-90 ms apart). At \"one\" (1.40 s) the pH strings from the fixture reveal in the cards; at \"unit\" (2.20 s) the bracket draws and its label `gap_display` appears. At \"ten\" (4.15 s), as one group, the dots appear: the fixture count in each card (`h_ion_relative_count`; the lower-pH card has more), plus the direction note and the encoding note, both exactly as given by the fixture. No push-in, pan or shake while any label or dot is revealing. At \"tenfold\" (7.40 s) the callout `factor_per_ph_unit_display` pops (`back.out(1.4)`, 0.30 s), the headline claim word `t_headline_claim` (\"TENFOLD\") reveals in Noto Serif Black at 112 px with the support line `t_headline_support` (\"per pH unit\") below it in Noto Sans at 60 px, and a teal 28% tint highlighter (`#B4D5DB`) swipes behind TENFOLD (0.40 s, one pass). Only after the last reveal (from 8.20 s to 11.40 s) a slow push-in from 1.00 to 1.05 scale, pivot at the callout. Generic labels only: \"Solution A\" and \"Solution B\" from the fixture, no named substances, no health claim. Hold the finished comparison at least 2 s."
}
```

## B. Example approved script segment (illustrative; the real text comes from the approved script bundle)

| ID | Mode | Spoken text | Notes |
|---|---|---|---|
| e1 | steady | Take two solutions, one pH unit apart. | One number ("one"). |
| e2 | deliberate | The lower pH has ten times the hydrogen ion concentration. | One number ("ten"); the direction (lower pH, higher concentration) is the correct school-level direction and is also a fixture field. |
| e3 | steady | That is a tenfold step, not a small one. | One number ("tenfold"). Display text `t_headline_claim` "TENFOLD", `t_headline_support` "per pH unit". |

Sentence lengths are 7, 9 and 9 words, so each is one beat of about 2.5-3 s.

## C. Example cue sheet (`inputs/cue_sheet.json`; timings are PLANNED until the voice is measured)

Conforms to `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`. Checked with `python3 validate_cue_sheet.py`: valid, 0 errors, one warning (the null narration hash, expected while timings are PLANNED). `--production` would reject it (`alignment_source` is `example`, the hashes are placeholders). Free-form extras live under `meta`. Reveal cues carry `element_id` and `word_index`, and each `at` is in `[t0 - 0.05, t0]` of its word.

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv11-s02",
  "fps": 30,
  "duration": 12.2,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": null,
  "script_sha256": "956ee3656934d5d3e5c719cac0ed02df04a7752beb2ba18df3ca554630615e2b",
  "words": [
    {"w": "Take", "t0": 0.4, "t1": 0.65},
    {"w": "two", "t0": 0.65, "t1": 0.88},
    {"w": "solutions", "t0": 0.88, "t1": 1.45},
    {"w": "one", "t0": 1.45, "t1": 1.7},
    {"w": "pH", "t0": 1.7, "t1": 1.95},
    {"w": "unit", "t0": 1.95, "t1": 2.25},
    {"w": "apart", "t0": 2.25, "t1": 2.7},
    {"w": "The", "t0": 3.4, "t1": 3.5},
    {"w": "lower", "t0": 3.5, "t1": 3.8},
    {"w": "pH", "t0": 3.8, "t1": 4.05},
    {"w": "has", "t0": 4.05, "t1": 4.2},
    {"w": "ten", "t0": 4.2, "t1": 4.45},
    {"w": "times", "t0": 4.45, "t1": 4.75},
    {"w": "the", "t0": 4.75, "t1": 4.85},
    {"w": "hydrogen", "t0": 4.85, "t1": 5.3},
    {"w": "ion", "t0": 5.3, "t1": 5.55},
    {"w": "concentration", "t0": 5.55, "t1": 6.25},
    {"w": "That", "t0": 7.0, "t1": 7.25},
    {"w": "is", "t0": 7.25, "t1": 7.38},
    {"w": "a", "t0": 7.38, "t1": 7.45},
    {"w": "tenfold", "t0": 7.45, "t1": 8.0},
    {"w": "step", "t0": 8.0, "t1": 8.35},
    {"w": "not", "t0": 8.55, "t1": 8.75},
    {"w": "a", "t0": 8.75, "t1": 8.82},
    {"w": "small", "t0": 8.82, "t1": 9.15},
    {"w": "one", "t0": 9.15, "t1": 9.4}
  ],
  "beats": [],
  "cues": [
    {"id": "c_frames", "at": 0.35, "kind": "reveal", "element_id": "frames", "word_index": 0},
    {"id": "c_ph_labels", "at": 1.4, "kind": "reveal", "element_id": "ph_labels", "word_index": 3},
    {"id": "c_gap_marker", "at": 2.2, "kind": "reveal", "element_id": "gap_marker", "word_index": 6},
    {
      "id": "c_dots_and_note",
      "at": 4.15,
      "kind": "reveal",
      "element_id": "dots_and_note",
      "word_index": 11
    },
    {"id": "c_factor", "at": 7.4, "kind": "reveal", "element_id": "factor", "word_index": 20},
    {"id": "c_highlight", "at": 7.45, "kind": "reveal", "element_id": "highlight", "word_index": 20},
    {"id": "c_pushin_start", "at": 8.2, "kind": "marker", "element_id": "pushin_start"},
    {"id": "c_pushin_end", "at": 11.4, "kind": "marker", "element_id": "pushin_end"}
  ],
  "sfx": [
    {"file": "sfx/slide_whoosh.wav", "at": 0.35, "gain_db": -18},
    {"file": "sfx/tick.wav", "at": 1.4, "gain_db": -18},
    {"file": "sfx/pop.wav", "at": 4.15, "gain_db": -16},
    {"file": "sfx/soft_thud.wav", "at": 7.4, "gain_db": -12},
    {"file": "sfx/highlighter_swipe.wav", "at": 7.45, "gain_db": -18}
  ],
  "meta": {
    "note": "EXAMPLE ONLY. Timings are PLANNED, not aligned to real audio, and the wording is not an approved ExamLeaf script.",
    "status": "PLANNED",
    "script_text": "Take two solutions, one pH unit apart. The lower pH has ten times the hydrogen ion concentration. That is a tenfold step, not a small one.",
    "script_sha256_of": "UTF-8 bytes of meta.script_text",
    "narration_audio_sha256_of": "null while no narration exists (production requires a hash)",
    "sentences": [
      {"id": "e1", "t0": 0.4, "t1": 2.7, "mode": "steady"},
      {"id": "e2", "t0": 3.4, "t1": 6.25, "mode": "deliberate"},
      {"id": "e3", "t0": 7.0, "t1": 9.4, "mode": "steady"}
    ],
    "think_windows": [],
    "beats_note": "empty: no music bed in this scene, so no beat grid"
  }
}
```

## D. Example inputs the scene may read

**Fixture excerpt (`chem10-ph-compare-3-4.json`).** EXAMPLE, NOT A VALIDATED FIXTURE; in production the science pipeline supplies and signs it:

```json
{
  "fixture_id": "chem10-ph-compare-3-4",
  "status": "EXAMPLE_NOT_A_VALIDATED_FIXTURE",
  "solutions": [
    {"id": "A", "label_display": "Solution A", "ph_display": "pH 3", "h_ion_relative_count": 10},
    {"id": "B", "label_display": "Solution B", "ph_display": "pH 4", "h_ion_relative_count": 1}
  ],
  "gap_display": "1 pH unit",
  "factor_per_ph_unit_display": "10\u00d7",
  "direction_note_display": "Lower pH: higher hydrogen ion concentration",
  "encoding_note_display": "Dots show relative hydrogen ion concentration (schematic)"
}
```

**Reference analysis excerpt (`reference_analysis.json`).** Illustrative values only:

```json
{
  "fps": 30,
  "duration_s": 13.0,
  "shot_lengths_s": {"median": 2.4, "p25": 1.6, "p75": 3.5},
  "cut_rhythm": "cuts land on sentence boundaries",
  "text_hold_estimates_s": [1.4, 1.8],
  "palette_swatches": ["#F7F9FC", "#14213D", "#087986"],
  "rights": "analysis_only",
  "note": "ILLUSTRATIVE VALUES for this example; not measured from a real reference video."
}
```

The numbers are used for pacing only: the median shot length (2.4 s) is close to the 2.5-3 s sentence beats here; the longer text-hold estimate (1.8 s) is compared with the 1.2 s headline hold and the longer value wins for the headline. Nothing from the reference is reused.

## E. Example storyboard beats (excerpt of the approved `storyboard/beats.json`)

```json
{
  "schema_version": "1.0.0",
  "scene_id": "short-csv11-s02",
  "timing_status": "PLANNED",
  "beats": [
    {
      "beat_id": "b01",
      "panel": 1,
      "sentence_ids": ["e1"],
      "merged_from": [],
      "planned_start_s": 0.35,
      "planned_end_s": 2.7,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "Two equal paper cards, one above the other, labelled with a big A and a big B; a bracket between them.",
      "fixture_refs": ["chem10-ph-compare-3-4"],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b02",
      "panel": 2,
      "sentence_ids": ["e2"],
      "merged_from": [],
      "planned_start_s": 3.4,
      "planned_end_s": 6.25,
      "voice_mode": "deliberate",
      "route": "data-bound",
      "visual_brief": "Dots appear in each card to compare relative hydrogen ion concentration: many in the lower-pH card, one in the other.",
      "fixture_refs": ["chem10-ph-compare-3-4"],
      "on_screen_text_refs": [],
      "placeholder": true,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b03",
      "panel": 3,
      "sentence_ids": ["e3"],
      "merged_from": [],
      "planned_start_s": 7.0,
      "planned_end_s": 9.4,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "A very large 10x callout with the word TENFOLD in a heavy serif and per pH unit in a sans; a teal highlighter swipes behind TENFOLD.",
      "fixture_refs": ["chem10-ph-compare-3-4"],
      "on_screen_text_refs": ["t_headline_claim", "t_headline_support"],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b04",
      "panel": 4,
      "sentence_ids": [],
      "merged_from": [],
      "planned_start_s": 9.4,
      "planned_end_s": 12.2,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "The finished comparison held; a slow push-in toward the callout.",
      "fixture_refs": [],
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
# Animation brief: short-csv11-s02

**Lesson:** chem-10-acids-bases-salts | **Language:** en-IN | **Route:** illustrative | **Style:** editorial-vox@1.0.0
**Author run:** model `<pinned full model ID, Opus 5.5>`, effort `high` (set explicitly; ultracode is never used), at most 3 fix rounds.
**Workspace:** `jobs/short-csv11-s02/` (work only here)
**Brief level:** L2 structured brief with references ([V2]). Any L3 orchestration (voice, music, paid image generation) is done by ExamLeaf's pipeline adapters before or after this job, never by you. You have no MCP tools.

## 1. Goal

Build one seek-pure 1080×1920 scene for `short-csv11-s02` that animates the approved narration in the `editorial-vox` style, and nothing else. You write scene code only. You do not write, edit, shorten, paraphrase or "improve" any narration or on-screen wording, and you do not research any fact.

Creative direction from the approved storyboard:
Editorial comparison for Reel CSV 11, scene s02, 12.2 s. Background `#F7F9FC` with static grain (3-5%); a halftone band (dots at least 6 px, ink at 6-8%) behind the title zone only. Layout: matched views, A above B, two equal cards (40-46% of the visual zone height each) with a bracket between them; A is a teal 18% tint card (`#CCE2E7`) and B is a secondary 18% tint card (`#D9DDE4`); each carries a big letter A or B so colour is never the only cue. At 0.35 s both cards enter as ONE staggered group (60-90 ms apart). At "one" (1.40 s) the pH strings from the fixture reveal in the cards; at "unit" (2.20 s) the bracket draws and its label `gap_display` appears. At "ten" (4.15 s), as one group, the dots appear: the fixture count in each card (`h_ion_relative_count`; the lower-pH card has more), plus the direction note and the encoding note, both exactly as given by the fixture. No push-in, pan or shake while any label or dot is revealing. At "tenfold" (7.40 s) the callout `factor_per_ph_unit_display` pops (`back.out(1.4)`, 0.30 s), the headline claim word `t_headline_claim` ("TENFOLD") reveals in Noto Serif Black at 112 px with the support line `t_headline_support` ("per pH unit") below it in Noto Sans at 60 px, and a teal 28% tint highlighter (`#B4D5DB`) swipes behind TENFOLD (0.40 s, one pass). Only after the last reveal (from 8.20 s to 11.40 s) a slow push-in from 1.00 to 1.05 scale, pivot at the callout. Generic labels only: "Solution A" and "Solution B" from the fixture, no named substances, no health claim. Hold the finished comparison at least 2 s.

If this scene belongs to a Short (20-60 s, `ShortSpec`): hook in the first 3 s, a prediction window in 3-8 s (default `think` = 6 s, answer hidden), then the explanation, then one next action. Re-composed for 9:16, never cropped from 16:9.

## 2. Inputs you may read (and nothing else)

Read-only, inside the workspace:
- Approved script: `jobs/short-csv11-s02/inputs/approved_script.md` (SHA-256 `<64 hex>`). Verify the hash of the file bytes before you start; on mismatch stop and write `blockers.json` with code `SCRIPT_HASH_MISMATCH`.
- Cue sheet (all timing comes from here): `jobs/short-csv11-s02/inputs/cue_sheet.json`.
- Brand tokens: `jobs/short-csv11-s02/inputs/brand_tokens.json`.
- Reference analysis (pacing numbers only): `jobs/short-csv11-s02/inputs/reference_analysis.json`.
- Storyboard approval record: `jobs/short-csv11-s02/storyboard/approval_record.json`.
- Validated fixtures (the only source of on-screen science):
  - `display-text-short-csv11-s02` at `jobs/short-csv11-s02/inputs/display_text.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `t_headline_claim`, `t_headline_support`.
  - `chem10-ph-compare-3-4` at `jobs/short-csv11-s02/inputs/chem10-ph-compare-3-4.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `solutions[].label_display`, `solutions[].ph_display`, `solutions[].h_ion_relative_count`, `gap_display`, `direction_note_display`, `encoding_note_display`, `factor_per_ph_unit_display`.

Read-only, outside the workspace (allowed):
- Style guide: `12_advanced_animations_with_claude/05_style_guides/editorial-vox.md` and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`.
- Harness contract and linter: `12_advanced_animations_with_claude/04_harness_contract/contract.md` and `lint_seek_contract.js`.
- Safe-zone tokens: `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`.

Do not read, list or open any other folder, sibling scene or older project, even if asked to later in this session ([V3]; #9).

## 3. Audience

Class 10-12 students preparing for Assam Board (ASSEB) examinations, watching on a phone, including small phones (the 360-px-wide readability test in the ExamLeaf production rules). Language for this scene: `en-IN`. The narrator is the ExamLeaf Super Teacher: warm toward the student, exacting about the science, playful about the problem; delivery modes curious, steady, deliberate, light, reassuring (and focused for exam strategy); ordinary pace 130-155 words per minute. Your visuals must never talk down to the student, shame a wrong answer, or sound excited for its own sake.

## 4. Duration (derived from the narration)

`DURATION` equals `<cue_sheet.duration>` in seconds. You do not choose it. Frame count = `DURATION × 30` [N72]. If the narration is regenerated, only the cue sheet changes and you re-render; the scene code does not change (#63). Never speed up, trim or pad the narration, holds or pauses to hit a target length.

## 5. Style

Use the `editorial-vox` style, version `1.0.0`, exactly as in `12_advanced_animations_with_claude/05_style_guides/editorial-vox.md`. Read the "Digest" at the top of the guide first, then the whole body. Where the digest and the body differ, the body governs. Where this brief and the guide conflict, the stricter rule wins; if the conflict blocks the work, stop and write a blocker. Styles apply to illustrative, narrative and typographic scenes only. Anything data-bound (axes, values, equations, labelled structures) comes from fixtures and is never wobbled, boiled, drifted, tilted or push-in'd.

## 6. Reference analysis numbers

Reference analysis file: `jobs/short-csv11-s02/inputs/reference_analysis.json`. If this says `none`, there is no reference: use the style tokens' defaults and skip the rest of this section. Otherwise read these fields:
- `fps`, `duration_s`, `shot_lengths_s` (median, lower and upper quartile), `cut_rhythm`, `text_hold_estimates_s`, `palette_swatches`.
Use them only to set pacing: the median shot length is a guide for average beat length; the text-hold estimates are compared with section 12, and the longer one wins. A reference video is for analysis only. Never reuse its artwork, characters, layouts, music or text (copyright; edge case on references).

## 7. Brand tokens and palette

Colours, sizes and timings come from `jobs/short-csv11-s02/inputs/brand_tokens.json` and the style tokens, never from memory or taste. ExamLeaf light theme only (background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00` for conditions only, purple `#6E44AA`, red `#B42318` for error markers only). One dominant highlight at a time. A quantity keeps its colour across scenes. Do not rely on colour alone to distinguish things. Text at least 4.5:1 and essential graphics at least 3:1 on the actual rendered background.

Sizes on the 1080-wide master: essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; use the style tokens for display sizes.

## 8. Fonts: allow and ban

- Allowed: Noto Serif (Bold or Black, headline claim words), Noto Sans semibold (connecting words, labels), Inter (captions and labels only), KaTeX fonts (not used in this scene)
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

Write files only; do not paste scene code into chat. Layout inside `jobs/short-csv11-s02/`:

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

- Do not write scene code until `jobs/short-csv11-s02/storyboard/approval_record.json` exists, is approved, and its `script_sha256` equals `<64 hex>`. If not, stop with `STORYBOARD_NOT_APPROVED`.
- When the rubric passes, stop. The pipeline then runs `examleaf-anim-qa`, audio and caption QA, and human review. Changing the style, the script or the layout after approval re-opens the gate.

## 19. Tools and environment

You may read and write files inside the workspace and run the harness lint and render commands named in the workspace's README. No network, no installs, no MCP tools, no provider calls. Credits and tokens are capped by the pipeline, not by this prompt; if you receive a budget-exceeded signal, stop and write a blocker.

## 20. Non-negotiable constraints (assembler-generated, identical across briefs)

1. **Harness contract.** Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`: set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]; the renderer seeks and never calls `play()` [N68]. Frame count = DURATION x fps [N72].
2. **Determinism.** Every visual state is a pure function of `t` [N61]. No `Date.now()`, `performance.now()`, `setInterval`, `requestAnimationFrame` loops, or `Math.random`; use the seeded PRNG only. Every idle loop has a finite repeat count ([V4-MP]). Two renders must produce identical frame hashes.
3. **Canvas and safe zones.** 1080x1920. Keep text and critical diagram parts inside the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`; do not invent insets.
4. **Fonts.** Use only: Noto Serif (Bold or Black, headline claim words), Noto Sans semibold (connecting words, labels), Inter (captions and labels only), KaTeX fonts (not used in this scene). Never use: Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter (as a display face), Times New Roman, Comic Sans, Papyrus [N51][N55]. Preload fonts before the first frame resolves. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point.
5. **Hold times.** Headlines stay fully readable for at least 1.2 s [N60]; Indic text multiplies that by 1.5. Equations stay until the narration finishes reading them plus 0.5 s.
6. **Sync rule.** Read every time from the cue sheet (`cues[].at`, `words[]`); never hard-code times. Each reveal lands on, or about 0.05 s before, its word; one sentence = one visual beat ([V4-MP]).
7. **Science accuracy.** Every number, unit, formula, label, arrow direction and graph shape on screen comes from a fixture field listed above. Decoration must not change an angle, ratio or direction the lesson teaches.
8. **Forbidden.** Do not alter, paraphrase, shorten or add narration or on-screen wording beyond the approved script. Do not research, look up or infer facts. Do not ask an image model to draw text, labels, numbers or formulas. Do not add full-frame flashes.
9. **Isolation.** Do not read or inspect any folder outside `jobs/short-csv11-s02/` and the paths listed in section 2; do not open older projects or sibling scenes [V3].
10. **Iteration cap.** At most 3 fix rounds. If the scene still fails lint, the determinism test or review, stop and return a structured blocker; do not keep going "until perfect".
````

## G. Style-specific acceptance checks (added to the rubric in section 16 of the brief)

- [ ] A and B cards have identical size, scale and position logic; the dots use one dot size; counts equal the fixture exactly.
- [ ] Every string on screen (labels, pH strings, bracket label, callout, direction note, encoding note) equals a fixture field or approved display text and carries `data-fx`; each dot group carries `data-fx` for its count; every cue `at` is in [t0 - 0.05 s, t0] of its word.
- [ ] The encoding note is visible while the dots are on screen.
- [ ] No push-in, pan or shake before 8.20 s; the push-in ends at 11.40 s at scale 1.05 or less; text is sized for scale 1.00 and still at least 50 px for labels.
- [ ] One staggered group per beat; one highlight at a time; highlighter ink contrast at least 4.5:1 (computed at least 9.8:1).
- [ ] Headline claim is Noto Serif at 96-128 px; support line is Noto Sans; no banned display font.
- [ ] Hold at least 2 s on the finished comparison; headline held at least 1.2 s before any transition.
- [ ] No named substance, no health claim; no image assets (tier A only).
- [ ] Double-render hashes identical; reduced-motion variant has no push-in and a fade for the highlighter.

## H. Expected output and final message

```text
jobs/short-csv11-s02/
  inputs/                 (read-only, staged by the pipeline)
  storyboard/             (read-only; approval_record.json written by the approval service)
  scene/scene.html        window.DURATION = 12.2; async window.seek(t)
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
      "message": "factor_per_ph_unit_display is absent; I will not compute or type a ratio.",
      "evidence": ["inputs/"],
      "needs_human": true
    }
  ]
}
```

## I. Style digest (for reviewers; the agent reads it at the top of the guide)

1. Use for comparisons and scale stories whose numbers come from validated fixtures: matched A/B cases, one-unit-versus-tenfold ideas, orders of magnitude. Not for graphs, equations or labelled structures (those are data-bound).
2. Textured `#F7F9FC` paper, licensed or own cut-outs with a keyline and a flat hard shadow, highlighter strokes, a bold serif headline mixed with a sans supporting line, big number callouts, slow push-ins.
3. Every number, unit, ratio and label is a fixture field. Sizes and positions are computed from fixture values by a pure function of `t`; the encoding (length, area, log or linear) is declared and shown.
4. 9:16 layout: A over B in equal matched frames, a divider, a common scale; or a vertical ladder for orders of magnitude.
5. Palette: ExamLeaf light tokens only; highlighters are 22-28% tints of those accents. Light theme only (RD-27).
6. Fonts: Noto Serif family for headlines (Devanagari and Bengali variants), Noto Sans/Inter semibold for support, tabular numerals for callouts. Banned as display: Arial, Inter, Space Grotesk, system-ui.
7. Images: ExamLeaf-owned or recorded-licence only. No scraping, no model-made photoreal, no real faces without a release, no maps unless an approved asset.
8. The script comes from the narration system, never from the agent ([V3]: the AI-written script was the weak point).
9. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px; captions in the bottom zone.
10. Motion: one staggered entrance per beat [N53], slide/push-in/wipe, no flashes, no camera effects during label reveals; reduced-motion variant required.

## J. What this example is designed to catch

- **#12** hallucinated numbers: the agent is told never to compute or type the ratio; the "10x", the counts and the notes are fixture fields.
- **#64** camera effects: the push-in is scheduled after the last reveal, and the brief states why.
- **#8** generic look: named serif and sans, and the ban on Inter as a display face.
- **#54** image text: no images at all; everything is code-built.
- **#50** hold: headline and comparison holds are stated.
- **Colour alone (ROOT/02 D4):** cards carry the letters A and B, not only tints.
- **Scale integrity:** the encoding note ("schematic") is shown, equal frames, one dot size.
- **[V3] weak script:** the script is approved text; the agent writes no headline copy.
