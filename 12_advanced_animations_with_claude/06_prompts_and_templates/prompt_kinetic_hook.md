# Filled brief: kinetic hook for Reel CSV 2 ("Which line has the larger resistance? Check the axes.")

**Reel:** CSV ID 2 (Class 10 Physics, I-V graph interpretation, P0, target 30 s). Hook: "Which line has the larger resistance? Check the axes." Truthful cover text: CHECK THE AXES. Caption first line: "The axes decide what this slope means." CTA: "Try the three-question graph check." Scientific check: keep I vertical and V horizontal throughout.
**This scene:** s01 of the Reel, the typographic hook and the prediction window (11.2 s). The two labelled I-versus-V lines and the comparison at the same voltage are data-bound scenes built from a validated fixture. This scene draws no graph, no lines and no axes.
**Why kinetic type:** the job is to put 1-3 key words on screen on their spoken words; the sentence itself is carried by the caption track.

**Style:** `kinetic-type@1.0.0` | **Version of this example:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** EXAMPLE. Every input below is illustrative so that the brief can be read end to end. In a real job the pipeline supplies approved inputs; the animation agent never authors them, and nothing here has been run.

**Evidence labels:** [V#]/[N#] are cited from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement; [Hypothesis] = untested. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Hook text and CSV IDs come from `01_business_model/REEL_BACKLOG_36.md` (the CSV ID is the stable ID).

## How this example is built

The generator filled `brief_template.md` from the job request in section A. Section D adds a **locale variant** (Hindi and Hinglish drafts) that is inactive until the locale gate passes (RD-26) and shows how the kinetic rules change for Indic text.

## A. Job request (`brief_request.json`, the input to `examleaf-anim-brief`)

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv02-s01",
  "lesson_id": "phy-10-electricity",
  "language": "en-IN",
  "route": {
    "tag": "typographic",
    "source": "examleaf-storyboard-route",
    "scene_spec_id": "short-csv02-s01"
  },
  "script": {
    "path": "jobs/short-csv02-s01/inputs/approved_script.md",
    "sha256": "<64 hex>",
    "approval_status": "approved",
    "segment_text": "Which line has the larger resistance? Check the axes. [THINK:6]"
  },
  "style": {
    "id": "kinetic-type",
    "version": "1.0.0",
    "guide_path": "12_advanced_animations_with_claude/05_style_guides/kinetic-type.md",
    "tokens_path": "12_advanced_animations_with_claude/05_style_guides/style_tokens.json"
  },
  "cue_sheet": {"path": "jobs/short-csv02-s01/inputs/cue_sheet.json", "sha256": "<64 hex>"},
  "brand_tokens": {"path": "jobs/short-csv02-s01/inputs/brand_tokens.json", "sha256": "<64 hex>"},
  "fixtures": [
    {
      "id": "display-text-short-csv02-s01",
      "path": "jobs/short-csv02-s01/inputs/display_text.json",
      "sha256": "<64 hex>",
      "fields_on_screen": ["t_which_line", "t_check_axes"]
    }
  ],
  "fonts": {
    "allow": [
      "Bebas Neue (Latin display and ransom glyphs)",
      "Noto Sans Bold (the small word THE and support text)",
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
  "workspace": "jobs/short-csv02-s01/",
  "approval_record": {"path": "jobs/short-csv02-s01/storyboard/approval_record.json", "sha256": "<64 hex>"},
  "creative_direction": "Kinetic hook for Reel CSV 2, scene s01, 11.2 s. Background plain `#F7F9FC` with static grain; no artwork. Mode 1 (ransom, Latin per-letter): `t_which_line` = \"WHICH\" / \"LINE?\" in two rows in the title zone; ink tiles with paper-white letters (15.15:1), tile edge 128 px, glyph em 96 px, Bebas Neue; rotation within ±6° and vertical jitter within ±8 px from the seeded PRNG keyed by (scene_id, tile_index); the first letter of WHICH lands at 0.25 s (0.05 s before the word), letters 0.045 s apart; LINE? lands from 0.51 s; a physics-blue (`#185ABD`) underline draws under LINE? at 1.09 s over 0.35 s. Mode 2 (display, mask-reveal-up): `t_check_axes` = \"CHECK\" / \"THE\" / \"AXES\" stacked in the visual zone, Bebas Neue 150 px for CHECK and AXES, Noto Sans Bold 84 px for THE, ink on paper; each word enters on its own word (3.05, 3.41, 3.53 s), 0.35 s, `power3.out`. At 3.58 s a 28% amber tint highlighter (`#DDCDB5`) swipes behind AXES in 0.35 s (amber because it is a caution: check before reading); no other highlight is active at the same time. From 4.60 s to 10.60 s (the 6 s `think` window) nothing moves; both phrases stay fully visible so the question remains on screen; no countdown, no answer, no drift. Do not draw any graph, line, axis or value. The caption track carries the full sentences in the caption zone and stays static (no karaoke) while tiles animate."
}
```

## B. Example approved script segment (illustrative; the real text comes from the approved script bundle)

| ID | Mode | Spoken text | Notes |
|---|---|---|---|
| k1 | curious | Which line has the larger resistance? | The hook. Display text `t_which_line`: "WHICH LINE?" |
| k2 | deliberate | Check the axes. | Display text `t_check_axes`: "CHECK THE AXES". |
| - | - | `[THINK:6]` | Six seconds of timeline silence; the answer is hidden (RD-11). |

Sentences are 6 and 3 words. The hook is a genuine knowledge gap that the Reel closes in the data-bound scenes that follow (ROOT/02 I1).

## C. Example cue sheet (`inputs/cue_sheet.json`; timings are PLANNED until the voice is measured)

Conforms to `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`. Checked with `python3 validate_cue_sheet.py`: valid, 0 errors, one warning (the null narration hash, expected while timings are PLANNED). `--production` would reject it (`alignment_source` is `example`, the hashes are placeholders). Free-form extras live under `meta`. Reveal cues carry `element_id` and `word_index`, and each `at` is in `[t0 - 0.05, t0]` of its word.

```json
{
  "schema_version": "1.0",
  "scene_id": "short-csv02-s01",
  "fps": 30,
  "duration": 11.2,
  "language": "en-IN",
  "alignment_source": "example",
  "narration_audio_sha256": null,
  "script_sha256": "acc26d1966a97028cfa7c8c9606538b5d8c1e1a57d0a187cc19136912be6d633",
  "words": [
    {"w": "Which", "t0": 0.3, "t1": 0.56},
    {"w": "line", "t0": 0.56, "t1": 0.86},
    {"w": "has", "t0": 0.86, "t1": 1.02},
    {"w": "the", "t0": 1.02, "t1": 1.14},
    {"w": "larger", "t0": 1.14, "t1": 1.58},
    {"w": "resistance", "t0": 1.58, "t1": 2.42},
    {"w": "Check", "t0": 3.1, "t1": 3.46},
    {"w": "the", "t0": 3.46, "t1": 3.58},
    {"w": "axes", "t0": 3.58, "t1": 4.1}
  ],
  "beats": [],
  "cues": [
    {"id": "c_which", "at": 0.25, "kind": "reveal", "element_id": "which", "word_index": 0},
    {"id": "c_line", "at": 0.51, "kind": "reveal", "element_id": "line", "word_index": 1},
    {
      "id": "c_line_underline",
      "at": 1.09,
      "kind": "reveal",
      "element_id": "line_underline",
      "word_index": 4
    },
    {"id": "c_check", "at": 3.05, "kind": "reveal", "element_id": "check", "word_index": 6},
    {"id": "c_the", "at": 3.41, "kind": "reveal", "element_id": "the", "word_index": 7},
    {"id": "c_axes", "at": 3.53, "kind": "reveal", "element_id": "axes", "word_index": 8},
    {
      "id": "c_axes_highlight",
      "at": 3.58,
      "kind": "reveal",
      "element_id": "axes_highlight",
      "word_index": 8
    },
    {"id": "think_1", "at": 4.6, "kind": "hold", "element_id": "scene", "until": 10.6}
  ],
  "sfx": [
    {"file": "sfx/tick.wav", "at": 0.25, "gain_db": -18},
    {"file": "sfx/tick.wav", "at": 0.51, "gain_db": -18},
    {"file": "sfx/tick.wav", "at": 3.05, "gain_db": -18},
    {"file": "sfx/tick.wav", "at": 3.53, "gain_db": -18}
  ],
  "meta": {
    "note": "EXAMPLE ONLY. Timings are PLANNED, not aligned to real audio, and the wording is not an approved ExamLeaf script.",
    "status": "PLANNED",
    "script_text": "Which line has the larger resistance? Check the axes. [THINK:6]",
    "script_sha256_of": "UTF-8 bytes of meta.script_text",
    "narration_audio_sha256_of": "null while no narration exists (production requires a hash)",
    "sentences": [
      {"id": "k1", "t0": 0.3, "t1": 2.42, "mode": "curious"},
      {"id": "k2", "t0": 3.1, "t1": 4.1, "mode": "deliberate"}
    ],
    "think_windows": [{"id": "think_1", "kind": "think", "t0": 4.6, "t1": 10.6, "answer_hidden": true}],
    "beats_note": "empty: no music bed in this scene, so no beat grid"
  }
}
```

## D. Example inputs the scene may read

**Fixtures:** no science fixture. The words on screen are approved display text (`t_which_line`, `t_check_axes`), staged as `display_text.json` and marked `data-fx="display_text.<id>"`; no graph, line or axis is drawn.

**Locale variant (inactive until the locale gate passes; RD-26).** DRAFTS for native-speaker and subject review, never released unreviewed (ROOT/03 §5.5):
- Hindi draft: `कौन-सी रेखा का प्रतिरोध ज़्यादा है? अक्षों को देखिए।`
- Hinglish draft (Latin script): `Kaun si line ka resistance zyada hai? Axes check karo.`

What changes for these locales: ransom mode becomes one paper strip per word (rotation ±3°, never per letter); the display words use a Devanagari-capable face after the glyph smoke test (`क्ष ज्ञ श्र द्ध विद्युत प्रतिरोध`) and the end-state equality test; no letter-spacing; line height at least 1.4; headline holds multiply by 1.5 (so at least 1.8 s); cue-sheet word timings come from the aligned Hindi audio, not from the English file; the 6 s `think` window is unchanged. Captions come from the original script.

## E. Example storyboard beats (excerpt of the approved `storyboard/beats.json`)

```json
{
  "schema_version": "1.0.0",
  "scene_id": "short-csv02-s01",
  "timing_status": "PLANNED",
  "beats": [
    {
      "beat_id": "b01",
      "panel": 1,
      "sentence_ids": ["k1"],
      "merged_from": [],
      "planned_start_s": 0.3,
      "planned_end_s": 2.42,
      "voice_mode": "curious",
      "route": "illustrative",
      "visual_brief": "Two rows of ink paper tiles spell WHICH and LINE? at the top; a blue underline draws under LINE?.",
      "fixture_refs": [],
      "on_screen_text_refs": ["t_which_line"],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b02",
      "panel": 2,
      "sentence_ids": ["k2"],
      "merged_from": [],
      "planned_start_s": 3.1,
      "planned_end_s": 4.1,
      "voice_mode": "deliberate",
      "route": "illustrative",
      "visual_brief": "Large display words CHECK / THE / AXES stacked in the middle; a soft amber highlighter swipes behind AXES.",
      "fixture_refs": [],
      "on_screen_text_refs": ["t_check_axes"],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    },
    {
      "beat_id": "b03",
      "panel": 3,
      "sentence_ids": [],
      "merged_from": [],
      "planned_start_s": 4.6,
      "planned_end_s": 10.6,
      "voice_mode": "steady",
      "route": "illustrative",
      "visual_brief": "Everything held still while the viewer predicts; no graph, lines or axes are drawn.",
      "fixture_refs": [],
      "on_screen_text_refs": [],
      "placeholder": false,
      "think_hold_s": 6,
      "unused": false
    }
  ]
}
```

## F. The assembled brief

This is `brief_template.md` with every placeholder filled, followed by the constraints block as it stands in `03_skills/examleaf-anim-brief/templates/constraints_block.md` on 15 Oct 2026. Regenerate this example if either file changes.

````markdown
# Animation brief: short-csv02-s01

**Lesson:** phy-10-electricity | **Language:** en-IN | **Route:** typographic | **Style:** kinetic-type@1.0.0
**Author run:** model `<pinned full model ID, Opus 5.5>`, effort `high` (set explicitly; ultracode is never used), at most 3 fix rounds.
**Workspace:** `jobs/short-csv02-s01/` (work only here)
**Brief level:** L2 structured brief with references ([V2]). Any L3 orchestration (voice, music, paid image generation) is done by ExamLeaf's pipeline adapters before or after this job, never by you. You have no MCP tools.

## 1. Goal

Build one seek-pure 1080×1920 scene for `short-csv02-s01` that animates the approved narration in the `kinetic-type` style, and nothing else. You write scene code only. You do not write, edit, shorten, paraphrase or "improve" any narration or on-screen wording, and you do not research any fact.

Creative direction from the approved storyboard:
Kinetic hook for Reel CSV 2, scene s01, 11.2 s. Background plain `#F7F9FC` with static grain; no artwork. Mode 1 (ransom, Latin per-letter): `t_which_line` = "WHICH" / "LINE?" in two rows in the title zone; ink tiles with paper-white letters (15.15:1), tile edge 128 px, glyph em 96 px, Bebas Neue; rotation within ±6° and vertical jitter within ±8 px from the seeded PRNG keyed by (scene_id, tile_index); the first letter of WHICH lands at 0.25 s (0.05 s before the word), letters 0.045 s apart; LINE? lands from 0.51 s; a physics-blue (`#185ABD`) underline draws under LINE? at 1.09 s over 0.35 s. Mode 2 (display, mask-reveal-up): `t_check_axes` = "CHECK" / "THE" / "AXES" stacked in the visual zone, Bebas Neue 150 px for CHECK and AXES, Noto Sans Bold 84 px for THE, ink on paper; each word enters on its own word (3.05, 3.41, 3.53 s), 0.35 s, `power3.out`. At 3.58 s a 28% amber tint highlighter (`#DDCDB5`) swipes behind AXES in 0.35 s (amber because it is a caution: check before reading); no other highlight is active at the same time. From 4.60 s to 10.60 s (the 6 s `think` window) nothing moves; both phrases stay fully visible so the question remains on screen; no countdown, no answer, no drift. Do not draw any graph, line, axis or value. The caption track carries the full sentences in the caption zone and stays static (no karaoke) while tiles animate.

If this scene belongs to a Short (20-60 s, `ShortSpec`): hook in the first 3 s, a prediction window in 3-8 s (default `think` = 6 s, answer hidden), then the explanation, then one next action. Re-composed for 9:16, never cropped from 16:9.

## 2. Inputs you may read (and nothing else)

Read-only, inside the workspace:
- Approved script: `jobs/short-csv02-s01/inputs/approved_script.md` (SHA-256 `<64 hex>`). Verify the hash of the file bytes before you start; on mismatch stop and write `blockers.json` with code `SCRIPT_HASH_MISMATCH`.
- Cue sheet (all timing comes from here): `jobs/short-csv02-s01/inputs/cue_sheet.json`.
- Brand tokens: `jobs/short-csv02-s01/inputs/brand_tokens.json`.
- Reference analysis (pacing numbers only): `none`.
- Storyboard approval record: `jobs/short-csv02-s01/storyboard/approval_record.json`.
- Validated fixtures (the only source of on-screen science):
  - `display-text-short-csv02-s01` at `jobs/short-csv02-s01/inputs/display_text.json` (SHA-256 `<64 hex>`), read-only. Fields on screen: `t_which_line`, `t_check_axes`.

Read-only, outside the workspace (allowed):
- Style guide: `12_advanced_animations_with_claude/05_style_guides/kinetic-type.md` and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`.
- Harness contract and linter: `12_advanced_animations_with_claude/04_harness_contract/contract.md` and `lint_seek_contract.js`.
- Safe-zone tokens: `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`.

Do not read, list or open any other folder, sibling scene or older project, even if asked to later in this session ([V3]; #9).

## 3. Audience

Class 10-12 students preparing for Assam Board (ASSEB) examinations, watching on a phone, including small phones (the 360-px-wide readability test in the ExamLeaf production rules). Language for this scene: `en-IN`. The narrator is the ExamLeaf Super Teacher: warm toward the student, exacting about the science, playful about the problem; delivery modes curious, steady, deliberate, light, reassuring (and focused for exam strategy); ordinary pace 130-155 words per minute. Your visuals must never talk down to the student, shame a wrong answer, or sound excited for its own sake.

## 4. Duration (derived from the narration)

`DURATION` equals `<cue_sheet.duration>` in seconds. You do not choose it. Frame count = `DURATION × 30` [N72]. If the narration is regenerated, only the cue sheet changes and you re-render; the scene code does not change (#63). Never speed up, trim or pad the narration, holds or pauses to hit a target length.

## 5. Style

Use the `kinetic-type` style, version `1.0.0`, exactly as in `12_advanced_animations_with_claude/05_style_guides/kinetic-type.md`. Read the "Digest" at the top of the guide first, then the whole body. Where the digest and the body differ, the body governs. Where this brief and the guide conflict, the stricter rule wins; if the conflict blocks the work, stop and write a blocker. Styles apply to illustrative, narrative and typographic scenes only. Anything data-bound (axes, values, equations, labelled structures) comes from fixtures and is never wobbled, boiled, drifted, tilted or push-in'd.

## 6. Reference analysis numbers

Reference analysis file: `none`. If this says `none`, there is no reference: use the style tokens' defaults and skip the rest of this section. Otherwise read these fields:
- `fps`, `duration_s`, `shot_lengths_s` (median, lower and upper quartile), `cut_rhythm`, `text_hold_estimates_s`, `palette_swatches`.
Use them only to set pacing: the median shot length is a guide for average beat length; the text-hold estimates are compared with section 12, and the longer one wins. A reference video is for analysis only. Never reuse its artwork, characters, layouts, music or text (copyright; edge case on references).

## 7. Brand tokens and palette

Colours, sizes and timings come from `jobs/short-csv02-s01/inputs/brand_tokens.json` and the style tokens, never from memory or taste. ExamLeaf light theme only (background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00` for conditions only, purple `#6E44AA`, red `#B42318` for error markers only). One dominant highlight at a time. A quantity keeps its colour across scenes. Do not rely on colour alone to distinguish things. Text at least 4.5:1 and essential graphics at least 3:1 on the actual rendered background.

Sizes on the 1080-wide master: essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; use the style tokens for display sizes.

## 8. Fonts: allow and ban

- Allowed: Bebas Neue (Latin display and ransom glyphs), Noto Sans Bold (the small word THE and support text), Inter (captions and labels only), KaTeX fonts (not used in this scene)
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

Write files only; do not paste scene code into chat. Layout inside `jobs/short-csv02-s01/`:

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

- Do not write scene code until `jobs/short-csv02-s01/storyboard/approval_record.json` exists, is approved, and its `script_sha256` equals `<64 hex>`. If not, stop with `STORYBOARD_NOT_APPROVED`.
- When the rubric passes, stop. The pipeline then runs `examleaf-anim-qa`, audio and caption QA, and human review. Changing the style, the script or the layout after approval re-opens the gate.

## 19. Tools and environment

You may read and write files inside the workspace and run the harness lint and render commands named in the workspace's README. No network, no installs, no MCP tools, no provider calls. Credits and tokens are capped by the pipeline, not by this prompt; if you receive a budget-exceeded signal, stop and write a blocker.

## 20. Non-negotiable constraints (assembler-generated, identical across briefs)

1. **Harness contract.** Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`: set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]; the renderer seeks and never calls `play()` [N68]. Frame count = DURATION x fps [N72].
2. **Determinism.** Every visual state is a pure function of `t` [N61]. No `Date.now()`, `performance.now()`, `setInterval`, `requestAnimationFrame` loops, or `Math.random`; use the seeded PRNG only. Every idle loop has a finite repeat count ([V4-MP]). Two renders must produce identical frame hashes.
3. **Canvas and safe zones.** 1080x1920. Keep text and critical diagram parts inside the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`; do not invent insets.
4. **Fonts.** Use only: Bebas Neue (Latin display and ransom glyphs), Noto Sans Bold (the small word THE and support text), Inter (captions and labels only), KaTeX fonts (not used in this scene). Never use: Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter (as a display face), Times New Roman, Comic Sans, Papyrus [N51][N55]. Preload fonts before the first frame resolves. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point.
5. **Hold times.** Headlines stay fully readable for at least 1.2 s [N60]; Indic text multiplies that by 1.5. Equations stay until the narration finishes reading them plus 0.5 s.
6. **Sync rule.** Read every time from the cue sheet (`cues[].at`, `words[]`); never hard-code times. Each reveal lands on, or about 0.05 s before, its word; one sentence = one visual beat ([V4-MP]).
7. **Science accuracy.** Every number, unit, formula, label, arrow direction and graph shape on screen comes from a fixture field listed above. Decoration must not change an angle, ratio or direction the lesson teaches.
8. **Forbidden.** Do not alter, paraphrase, shorten or add narration or on-screen wording beyond the approved script. Do not research, look up or infer facts. Do not ask an image model to draw text, labels, numbers or formulas. Do not add full-frame flashes.
9. **Isolation.** Do not read or inspect any folder outside `jobs/short-csv02-s01/` and the paths listed in section 2; do not open older projects or sibling scenes [V3].
10. **Iteration cap.** At most 3 fix rounds. If the scene still fails lint, the determinism test or review, stop and return a structured blocker; do not keep going "until perfect".
````

## G. Style-specific acceptance checks (added to the rubric in section 16 of the brief)

- [ ] Every reveal cue `at` is in [t0 - 0.05 s, t0] of its word (the validator rejects later); entrances settle within about 0.30 s; the stagger inside WHICH and LINE? is 0.04-0.05 s per letter (minimum 0.02 s).
- [ ] Only tokens from the approved display text appear: WHICH, LINE?, CHECK, THE, AXES. No graph, line, axis, number or symbol other than "?" is drawn.
- [ ] One staggered entrance per beat; the amber highlighter is the only active highlight when it runs; at most two accents (blue underline, amber highlight).
- [ ] Tile letter contrast at least 4.5:1; display sizes 96-150 px; THE may be smaller; no banned font; no `letter-spacing`.
- [ ] Captions stay in the caption zone and stay static while tiles animate; no overlap with the caption plate.
- [ ] Nothing moves from 4.60 s to 10.60 s; no SFX in that window; the question stays visible.
- [ ] Hold at least 1.2 s after AXES has landed and before the scene ends.
- [ ] Double-render hashes identical; reduced-motion variant fades words in (150-300 ms).

## H. Expected output and final message

```text
jobs/short-csv02-s01/
  inputs/                 (read-only, staged by the pipeline)
  storyboard/             (read-only; approval_record.json written by the approval service)
  scene/scene.html        window.DURATION = 11.2; async window.seek(t)
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
      "code": "CUE_SHEET_MISSING",
      "message": "cue_sheet.json is missing; I will not estimate word times.",
      "evidence": ["inputs/"],
      "needs_human": true
    }
  ]
}
```

## I. Style digest (for reviewers; the agent reads it at the top of the guide)

1. Text is timed from the cue sheet's `words[]` (`t0`, `t1`). Nothing is hard-coded. Each reveal lands on, or about 0.05 s before, its word.
2. Three modes: ransom (tiles), handwriting (reveal), label (pop). Latin may animate per letter; Devanagari and Bengali-Assamese animate per word or grapheme cluster, never per code point (#55).
3. One staggered entrance per beat [N53]. Dominant colour plus at most two accents [N52]. One highlighted keyword at a time.
4. Fonts: a named allow-list; ban Arial, Helvetica, Roboto, system-ui, Space Grotesk, and Inter as a display face [N51][N55]; rotate display faces between Reels.
5. Hold a headline at least 1.2 s [N60]; Indic text longer (multiplier 1.5 [Hypothesis]); equations until narration finishes reading them plus 0.5 s and at least 2 s after an important transformation (RD-02).
6. Only words from the approved script or approved on-screen text appear. Equations and science statements are never kinetic text; formulae arrive from fixtures as a unit.
7. Captions stay in the caption zone and stay static while kinetic text moves (#51). Kinetic text carries 1-3 key words, not the sentence.
8. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px.
9. Determinism: seek-driven, stateless seeded PRNG, finite repeats, no wall-clock CSS animation. Reduced-motion variant required.
10. Cost: zero credits.

## J. What this example is designed to catch

- **#11** script: the brief forbids rewording the hook; displayed tokens must exist in the approved text.
- **#50** hold: stated for Latin and multiplied for Indic.
- **#51** caption clash: static captions while tiles animate; nothing over the caption plate.
- **#55** Indic: the variant shows the rule change without activating it.
- **#8** generic fonts: Bebas Neue and Noto Sans named; Inter banned as display.
- **#12** science on screen: no graph is drawn here at all.
- **Anxiety:** no timer or countdown in the think window.
- **#63** timing: a regenerated voice only changes the cue sheet.
