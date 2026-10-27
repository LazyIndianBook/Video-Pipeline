# Storyboard request: the 3×3 grid (code thumbnails and Higgsfield variants)

**Used by:** `examleaf-anim-storyboard-gate` (extends `examleaf-storyboard-route`), step 3 of `master_prompt_paper_collage_VERTICAL.md` and the equivalent step of every style. **Version:** 1.0.0 | **Date:** 15 Oct 2026.
**Why it exists:** [V4] makes a 3×3 storyboard grid and then waits for a human before spending credits or building ([V4-MP]); ExamLeaf adopts that gate (#47) and adds an estimate, hashes and science-free panels.

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; [Recommendation] = design judgement; "verify" = not confirmed. Edge cases #1-#65 (report §8). Project decisions RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## 1. Preconditions

1. The script is approved (academic gate GA) and its SHA-256 is recorded. The storyboard agent never writes or edits narration.
2. `examleaf-storyboard-route` has tagged the scene `illustrative`, `narrative` or `typographic`. Data-bound beats appear in the grid only as placeholder cards.
3. A style ID and version are chosen (`05_style_guides/README.md` §2).
4. Planned timings exist. They are PLANNED until the voice is generated and measured; the cue sheet does not exist yet.
5. The fixtures that the scene will use are listed by ID (not opened for values the grid does not need).
6. For a collage storyboard: the hero reference sheet and its hash, if a hero appears (#48).

## 2. Outputs

| File | Content |
|---|---|
| `storyboard/grid.png` | One image, 3×3 panels, each panel exactly 540×960 (9:16), 12 px cream gutters and a 12 px outer margin (so the sheet is 1668×2928) [Recommendation]; number tags 1-9 added in code at each panel's top-left |
| `storyboard/beats.json` | The nine beats in order (schema in §5) |
| `storyboard/estimate.json` | Credit, token and render estimate (schema in §6) |
| `storyboard/storyboard_note.md` | One paragraph: style match, and the confirmation that every panel is science-free |

The approval record `storyboard/approval_record.json` is NOT an output: it is written by the approval service (until it exists, by a human reviewer recording it in the job folder), never by the agent (RD-17, RD-32).

## 3. The request text

### 3.1 Variant A: code-rendered thumbnails (default, zero credits)

```text
STORYBOARD REQUEST (code thumbnails)
Scene: <scene_id>   Lesson: <lesson_id>   Style: <style_id>@<style_version>
Approved script: <script_path>   SHA-256: <script_sha256>

Build ONE storyboard sheet: 3 columns by 3 rows = 9 panels, each panel a 9:16 frame of
540x960 px, 12 px cream gutters, 12 px outer margin. Render each panel in code, with the
chosen style's own primitives (paper shapes, tape, doodles, placeholder cards). Do not call
any image-generation tool or MCP.

Panel i shows beat i of beats.json. The nine beats cover the main beats of the approved
script in order. If the scene has more than nine beats, merge adjacent beats of the same
mode and record the merge in beats.json (merged_from). If it has fewer, leave the unused
panels blank cream with a thin border and mark them "unused" in beats.json.

Rules for every panel:
 - Use the visual_brief of that beat. Do not add content that the brief does not contain.
 - Draw NO text, numbers, symbols, formulae, graphs, labelled diagrams, or arrows with
   scientific direction. A data-bound beat is a blank cream placeholder card with a thin
   border (the words "science fixture goes here" may be added in code as a review aid).
 - Keep the top 22% and bottom 24% of each panel visually quiet (title and caption zones, per the safe-zone tokens).
 - Panel number tags (1-9) are added in code after rendering, 40-48 px, ink on a cream tag.
 - Respect the style's palette and layout rules; no 3D, no photoreal, no flashes implied.

Write: storyboard/grid.png, storyboard/beats.json, storyboard/estimate.json,
storyboard/storyboard_note.md. Then STOP (see section 7).
```

### 3.2 Variant B: Higgsfield GPT Image grid (credits; only if approved)

Use only when a human has approved raster look-development in writing AND `estimate.json` holds a credit estimate and a cap. The agent does not call Higgsfield; `examleaf-mcp-orchestrator` does, with a per-job permission, an estimate-before-call, a hard credit ledger and idempotent job IDs (#41, #42, #43). The image model named below is the one used in [V4-MP] (`gpt_image_2_5`); verify the current ID and options (aspect ratio, output size) in the tool before use.

```text
STORYBOARD REQUEST (Higgsfield image grid)
Scene: <scene_id>   Style: <style_id>@<style_version>   Cap: <credit_cap> credits
Model: <image_model_id from the approved estimate>

Create ONE storyboard grid image: 3 columns x 3 rows = 9 panels, each panel a 9:16
portrait frame, separated by thin cream gutters. No numbers, letters, captions, labels or
symbols anywhere in the image (number tags will be added later in code).

Style: hand-made paper-cutout storybook collage - watercolour and coloured-pencil cutouts
with thin white die-cut borders and soft warm drop shadows on cream and kraft textured
paper and torn-paper strips. Warm, muted palette: tomato red, mustard, teal, ultramarine,
olive, sage, blush pink, cream, kraft. Flat, straight-on view. No 3D, no photorealism, no
gloss, no heavy blur or glow. Round friendly characters with small black dot eyes and
rosy cheeks, never scary. Keep the top fifth and bottom quarter of each panel visually quiet.
Match the attached hero reference sheet for the recurring character.

Panels in reading order (left to right, top to bottom):
 1. <visual_brief of beat 1>
 2. <visual_brief of beat 2>
 ... (through 9)
A panel marked PLACEHOLDER is a plain blank cream card with a thin border and nothing on it.
Do not draw any text, numerals, symbols, formulae, graphs, diagrams, or arrows that imply a
scientific direction.
```

After generation, in code: run a text-detection check on the grid (any detected glyph fails the panel, #54); add number tags 1-9; record the generator job ID, the prompt text, the output hash and the credits used in the ledger. If a panel fails, regenerate only within the cap; never retry silently after a late result, wait for the job (results can arrive after about 60 s [N35]) and reconcile by job ID.

## 4. Mapping beats to panels

- One panel per beat, in script order. The sentence IDs in `beats.json` come from the approved script's own segmentation; the agent does not re-split sentences.
- A `think` hold or learner-controlled pause belongs to the beat it follows; its panel shows a calm placeholder, never the answer.
- A panel never shows an answer that the script hides during an attempt.

## 5. `beats.json` expectations

```json
{
  "schema_version": "1.0.0",
  "scene_id": "<scene_id>",
  "lesson_id": "<lesson_id>",
  "style_id": "<style_id>",
  "style_version": "<style_version>",
  "script_sha256": "<64 hex>",
  "timing_status": "PLANNED",
  "beats": [
    {
      "beat_id": "b01",
      "panel": 1,
      "sentence_ids": ["s1"],
      "merged_from": [],
      "planned_start_s": 0.0,
      "planned_end_s": 3.2,
      "voice_mode": "curious",
      "route": "illustrative",
      "visual_brief": "<one or two sentences describing the picture, with no text or numbers in it>",
      "fixture_refs": [],
      "on_screen_text_refs": ["<id of an approved display_text item>"],
      "placeholder": false,
      "think_hold_s": null,
      "unused": false
    }
  ]
}
```

Requirements:
1. Exactly nine entries (some may be `unused`).
2. `script_sha256` equals the approved script's hash. `visual_brief` never contains text, numbers or formulae; science is referenced through `fixture_refs` only.
3. `on_screen_text_refs` point at approved display text; the agent invents none.
4. Times are PLANNED. They are replaced by measured times in the cue sheet after the voice is made.
5. `route` is `illustrative` or `data-bound`. A data-bound beat has `placeholder: true`.
6. The file validates against the pipeline's beats schema (the harness owner defines it; the shape above is the expectation).

## 6. `estimate.json` and the credit-estimate line

```json
{
  "schema_version": "1.0.0",
  "mode": "code_thumbnails | higgsfield",
  "credits": {
    "estimate": 0,
    "unit_cost": null,
    "pricing_source": "<document or tool page used>",
    "pricing_status": "VERIFIED | UNVERIFIED",
    "cap": 0,
    "ledger_path": "<path to the job ledger>"
  },
  "tokens": {
    "model": "<pinned full model ID>",
    "effort": "high",
    "estimate_input": null,
    "estimate_output": null,
    "basis": "<how the estimate was made, for example per-scene history>"
  },
  "render_minutes_estimate": null,
  "notes": ""
}
```

**The credit-estimate line** (printed in the checkpoint message):

- Code thumbnails: `CREDIT ESTIMATE: 0 credits (code-rendered thumbnails). Token estimate: <n or "unmeasured">.`
- Higgsfield: `CREDIT ESTIMATE: <n> generation(s) x <credits_per_generation> credits (<pricing_source>, <VERIFIED|UNVERIFIED>) = <total> credits; job cap <cap>; ledger <ledger_path>.`

Rules: never invent a price or a per-generation credit cost. If the unit cost is not from a verified source, print `UNVERIFIED` and leave the total for a human to supply before approval. Competitor-authored plan prices are not a verified source (report §6.1, [N75]). Premium video models are not used (RD-39: generated video default 0 s). Credits are deducted for every agent generation on any plan and there is no native cap, so the cap is enforced by the pipeline [N33][N34].

## 7. The hard stop

The agent prints this and ends its turn. It does nothing else until an approval record exists.

```text
⛔ STOP. Storyboard <storyboard_id> for scene <scene_id> is ready for review.
Script SHA-256 (unchanged): <script_sha256>
Grid: storyboard/grid.png   Beats: storyboard/beats.json   Estimate: storyboard/estimate.json
<the CREDIT ESTIMATE line>
I will not generate voice, assets or scene code until an approval record exists that is
bound to script_sha256=<script_sha256> and credits_max=<cap>. I cannot approve my own work.
Reply with the approval line or with requested changes.
```

**Approval line** (typed by an authorised reviewer and recorded by the approval service):

```text
APPROVED storyboard=<storyboard_id> script_sha256=<script_sha256> credits_max=<cap> reviewer=<role or name>
```

Anything else (silence, "looks good", an approval for a different hash or a higher cap than shown) is not approval. A change to the script, style, layout or cap invalidates the approval and re-opens the gate (RD note on approvals bound to hashes).

## 8. Revisions

- At most **2 revision rounds** per storyboard before the human decides to approve, narrow the scope or stop [Recommendation]. A revision that uses Higgsfield again re-estimates and re-checks the cap.
- A revision changes only what the reviewer named. It cannot change the script.
- Every round is logged: round number, what changed, credits used.

## 9. Edge cases

#41, #42, #43, #45 (estimate, cap, late results), #47 (gate), #48 (hero reference), #49 (9:16 panels), #51 (quiet top and bottom), #54 (no text in panels; tags added in code), #11 and #12 (script and facts untouched).
