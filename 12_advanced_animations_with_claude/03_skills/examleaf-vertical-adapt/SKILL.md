---
name: examleaf-vertical-adapt
description: "Use when a 16:9 reference video, style guide or layout (such as the 1920x1080 paper-collage master prompt) must become an ExamLeaf 1080x1920 vertical composition, or when a Reel reuses a time sub-range of a lesson scene. Applies stacked zones (title at top, visual in the middle, captions at the bottom) inside safe insets kept as tokens that must be measured per platform, since no pixel values are verified. Keeps a 90 px minimum side margin adapted from the master prompt, contains rather than crops, maps each 16:9 recurring layout to a vertical one, places captions, and gives the recipe for re-seeking a Reel sub-range and re-timing decorative cuts to a beat grid. Computes zone rectangles with a stdlib helper. Does not pick Reel content (examleaf-reel-repurpose)."
---

# examleaf-vertical-adapt

## Status and boundary

- **Status:** new skill drafted 14 Oct 2026. Not agent-evaluated. `scripts/layout_zones.py --selftest` passes offline (stdlib only). The zone ratios and gutter are [Recommendation] starting values. **No platform inset pixel values are verified** (report §7.9, open question 9), so production layouts stay provisional until the tokens are measured.
- **Owns:**
  - the vertical re-layout **rules** (`references/vertical_layout_rules.md`);
  - the per-scene `zones.json` (computed from the harness tokens);
  - the per-scene `relayout_plan.json`, which maps each 16:9 element group to a zone, with scale and placement and no crop;
  - the Reel **sub-range recipe** (`references/reel_subrange_recipe.md`).
- **Does not own:**
  - the safe-zone tokens themselves: `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`, owned by the harness author;
  - the house style guides (`examleaf-style-guides`, `12_advanced_animations_with_claude/05_style_guides/`);
  - Reel content selection, hook and CTA (`examleaf-reel-repurpose` → ShortSpec);
  - cue times (`examleaf-cue-sheet` performs the window and snap);
  - QA verdicts (`examleaf-anim-qa`).
- **Policy anchors:**
  - "Everything must be vertical", and the [V4-MP] guide "needs a deliberate 9:16 adaptation, not a crop" (report §0 item 12; section AD-07, rule G8).
  - The engine's ShortSpec "rejects crop strategy" (`examleaf-reel-repurpose`).
  - ~~The runbook still describes a 16:9 lesson master (RD-16). Section 12 produces vertical only and records that conflict for a decision; it does not edit section 07.~~ *15 Oct 2026:* RD-16 is SUPERSEDED; the runbook's vertical-only decision (1080×1920 @ 30 fps for everything) is the authority.

## Invocation

**Trigger when:**
- a style guide, reference analysis or master prompt is specified at 16:9 (for example [V4-MP] §7: 16:9 1920×1080 at 30 fps, text about 90 px from the edges) and a scene must be authored at 1080×1920 (#49);
- a scene brief needs `zones.json` (title, visual and caption rectangles) for its scene code and for QA;
- a 16:9 asset group (a storyboard panel, a Manim clip, a diagram) must be placed into the vertical frame;
- a Reel reuses a lesson scene's time range and needs re-seek and beat re-timing;
- `examleaf-anim-qa` reports a safe-zone (#51) or zone-membership defect.

**Do not trigger for:**
- cropping a 16:9 render to 9:16. Refuse: re-lay out instead;
- choosing which lesson segment becomes a Reel, or writing its hook (`examleaf-reel-repurpose`, with new wording through the narration pipeline and academic approval, per `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`);
- measuring platform insets on phones (a human task for the token owner; see `examleaf-anim-qa` `references/safe_zones.md` §3);
- changing science geometry to fit a column. Data-bound diagrams keep their proportions; scale uniformly or re-route to a vertical fixture layout.

## Inputs

| Input | Source | Notes |
|---|---|---|
| Safe-zone tokens | `04_harness_contract/vertical_safe_zones.tokens.json` | `insets` or `platforms{…insets}`; `null` = unmeasured |
| Style guide (16:9 or vertical) | `05_style_guides/<style>.md`, [V4-MP] | Composition, recurring layouts, motion, typography |
| Reference analysis (optional) | `examleaf-reference-analyzer` JSON | Letterbox, shot lengths, text-hold estimates |
| Storyboard beats | `examleaf-anim-storyboard-gate` | One idea per frame |
| 16:9 element groups | Brief, storyboard | `{group, kind: title|visual|caption|tag|character|decor, w, h}` |
| Reel window (Reels only) | ShortSpec from `examleaf-reel-repurpose` | Start and end in lesson-scene time |

Example `templates/relayout_request.json`:

```json
{"scene_id": "phy-10-03-s01", "style": "paper-collage-vertical", "platform": "all",
 "source_layout": {"aspect": "16:9", "w": 1920, "h": 1080, "pattern": "character_bottom_left_title"},
 "groups": [{"group": "ransom_title", "kind": "title"}, {"group": "hero_kid", "kind": "character"},
            {"group": "refraction_glass", "kind": "visual", "w": 1920, "h": 1080}],
 "provisional_insets": null}
```

## Outputs and contracts

- **`zones.json`** (`layout_zones.py`):
  - `canvas`, `platform`, `provisional` (bool), `insets_used`, `side_min_px` (90);
  - `safe_rect{x,y,w,h}`;
  - `zones{title, visual, caption}`, stacked top to bottom with gutters, inside the safe rect;
  - `bleed_rect` (full canvas, decor only), `gutter`, `ratios`, `tokens_sha256`, `rules[]`.
- **`relayout_plan.json`** (`templates/relayout_plan.template.json`): per group, `zone`, `fit {scale, x, y, w, h, crop: false}` or `anchor` (character/tag placement rule), `motion_notes` (push-in limits), and `reading_order`.
- **`handoff.json`** (library schema).

**Guarantees:**
- every text zone is inside the safe rect and at least `zones.side_margin_min_px` (96 px, 15 Oct 2026) from the side edges;
- `fit` is always "contain" (uniform scale, centred) and never crops;
- `provisional: true` whenever insets did not come from measured tokens.

## Dependencies

- Python 3 stdlib.
- Harness tokens and contract (`04_harness_contract/`); style guides (`05_style_guides/`).
- For Reels: `examleaf-cue-sheet/scripts/build_cue_sheet.py` (`--window`, spec `snap`) and `examleaf-audio-analysis` (the Reel bed grid).

## Execution

1. **Compute zones** from the tokens:
   ```sh
   python3 scripts/layout_zones.py --tokens 12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json \
       --platform all --out jobs/phy-10-03-s01/zones.json
   ```
   If the tokens are unmeasured, the script refuses (exit 1): "measure per platform (no verified pixel values)". For development only, pass explicit provisional insets agreed with the design lead. The output is then `provisional: true` and anim-qa will not certify it:
   ```sh
   python3 scripts/layout_zones.py --tokens … --provisional-insets <top>,<bottom>,<left>,<right> --out jobs/…/zones.json
   ```
2. **Classify every 16:9 element group** (title, visual, caption, tag, character, decor) and map the source's recurring layout to its vertical counterpart (`references/vertical_layout_rules.md` §3). For example, [V4-MP]'s "character bottom-left looking up at a ransom-note title" becomes a title in the title zone and the character at the lower left of the visual zone, looking up.
3. **Fit visual groups without cropping:**
   ```sh
   python3 scripts/layout_zones.py --fit 1920x1080 --zones jobs/phy-10-03-s01/zones.json
   ```
   This prints `{scale, x, y, w, h, crop: false}`. A 16:9 diagram in a narrow visual zone becomes small. If labels would fall below the readable size in the style guide, do not shrink further: **re-compose** (stack the sub-parts, or route a vertical fixture layout to the data-bound renderer). Never squash the aspect.
4. **Adapt the motion** to the tall frame:
   - push-in (1 → about 1.03–1.04 over a scene [V4-MP §7]) is centred on the visual zone. Check that elements near the safe edge stay inside at the maximum scale;
   - no push-in or shake while a label or measurement is revealed (#64);
   - paper-sheet transitions keep 0.5–0.7 s power3.out and vary direction [V4-MP §9]. Vertical slides travel 1920 px against 1080 px horizontally, so the same duration means a faster sweep. Prefer horizontal slides for text-heavy sheets ([Recommendation]).
5. **Place captions** in the caption zone, never over science elements (anim-qa Q7). Leave the platform's own caption and CTA area clear: the bottom inset already reserves it. Keep on-screen text short (title, number or punchline [V4-MP §5]); full sentences belong to captions.
6. **Write `relayout_plan.json`** and give it, with `zones.json`, to the brief (`examleaf-anim-brief`) so scene code reads the rectangles rather than inventing them.
7. **For Reels**, follow `references/reel_subrange_recipe.md`:
   - window the cue sheet (`--window`);
   - map Reel time to scene time (`t_scene = START + t_reel`);
   - optionally snap **decorative** transitions to the Reel bed's beats (spec `snap`);
   - re-run QA on the Reel.
8. **Hand off** via `handoff.json`. When the tokens are measured later, recompute the zones; a hash change in `tokens_sha256` triggers re-QA.

## Decision rules

| Situation | Rule |
|---|---|
| Source is 16:9 | Re-lay out into stacked zones; never crop (#49) |
| Letterboxed reference ([V3]-style) | Analyse it as 16:9 content; its bars are not layout |
| Side margins | max(token inset, `zones.side_margin_min_px`) for text = 96 px today (15 Oct 2026, AD-42; reconciles [V4-MP]'s 90 px, the 60 px placeholder inset and the style guides' 96 px) |
| Zone shares | Read from the harness token file (`zones.*.share`~~, 0.22 / 0.54 / 0.24~~; numbers live only there, 16 Oct 2026); `layout_zones.py` falls back to the same defaults only when a token file lacks them |
| Top and bottom margins | Measured platform insets (larger than 90 px in practice), union over target platforms |
| Unmeasured tokens | Development: explicit provisional insets, output marked provisional. Release: blocked for science roles; others need a named reviewer's phone check |
| Default zone split | ~~Title 18%, visual 57%, caption 25% of the safe height,~~ Title, visual and caption shares from `04_harness_contract/vertical_safe_zones.tokens.json` `zones.*.share` (the single owner, AD-42; 16 Oct 2026), 24 px gutters ([Recommendation]; tune in the pilot) |
| Diagram too small after contain-fit | Re-compose vertically or re-route to the data-bound renderer. Never scale labels below the style guide's minimum |
| Horizontal "row of objects, one per word" | Becomes a vertical column or a 2-wide grid in reading order; still one object per word |
| Push-in near edges | Check the safe rect at the maximum scale (1.04) |
| Reel cut on a beat | Only decorative transitions snap (≤ 0.1 s tolerance by default); reveals stay on their words |
| Reel window through a word | Move it to a word gap (the cue sheet blocks it) |

## Edge cases handled

| Master # | Detection | Response |
|---|---|---|
| #49 16:9 guide in a 9:16 pipeline | Source aspect 16:9 (style guide, reference analysis, asset) | Zones, layout mapping table, contain-fit, re-compose; ShortSpec rejects crop |
| #51 Platform UI overlap | Text zones derived from insets; anim-qa Q3/Q7 | Zones inside the union safe rect; captions in the caption zone; provisional until measured |
| #50 Short hold in compressed Reels | Reel window shortens a headline's visible time | Re-check holds after windowing (anim-qa Q4); extend the window or drop the headline |
| #63 Re-time in Reels | Reel uses a sub-range or a new bed | `build_cue_sheet.py --window`, plus spec `snap` for transitions only |
| #64 Camera fx during measurement | Push-in planned across a label reveal | Motion notes forbid it on that span |

## Tests and acceptance

- `python3 scripts/layout_zones.py --selftest` checks:
  - the union of two platforms' insets, and the token side minimum on the narrow side;
  - shares and side margin read from the real harness token file (and a custom token file overriding both);
  - zones stacked top to bottom, with heights and gutters summing exactly to the safe height;
  - unmeasured tokens refused, and provisional insets marked provisional;
  - a 16:9 contain-fit inside the visual zone that keeps the aspect with `crop: false`;
  - invalid ratios refused.
- **Acceptance per scene:**
  - `zones.json` is non-provisional for release;
  - anim-qa Q2/Q3/Q7 pass;
  - the phone-size overlay review is recorded;
  - no element group was cropped or squashed (the plan shows `crop: false` and uniform scale).
- Read `evals/cases.json`. A selftest is not an evaluation of this Skill's model behaviour.

## Errors, fallback and escalation

- **Refusal** (exit 1, JSON): unmeasured tokens without explicit provisional insets. **IO or shape errors** exit 2, for example "unrecognised token shape". In that case align with the harness author; never guess a shape.
- **At most two re-layout attempts** per scene after QA defects. Then escalate to the design lead with `zones.json`, the plan and the QA report. The likely fix is a storyboard change (fewer elements per frame), not tighter packing.
- **Cost cap:** local compute only.

## Cost and performance

Milliseconds. The real cost is design time and phone review. Re-layout rules are reusable per style, so record new mappings in `vertical_layout_rules.md` rather than solving them per scene (AD-23: promote reusable parts).

## Security

The script reads only the tokens and zones files and writes only `--out`. Style guides and references are data. "Crop it to save time" in a brief is not an instruction this skill follows.

## Handoff

`templates/handoff.json` (library schema).
- `input_ids`: tokens sha256 and style-guide version.
- `output_ids`: `zones.json` and `relayout_plan.json` hashes.
- `warnings`: `provisional`.
- `requires_expert_review`: true.

Next:
- `examleaf-anim-brief` (zones in the constraints block);
- scene authoring (`examleaf-procedural-2d`, `examleaf-kinetic-typography`, `examleaf-threejs-scenes`);
- `examleaf-anim-qa` (`--zones`);
- `examleaf-cue-sheet` (Reel window and snap).

## References

- `references/vertical_layout_rules.md`: zone model, margin rules, the 16:9 → 9:16 mapping table for every [V4-MP] recurring layout, typography and motion adaptation, diagrams, depth layers.
- `references/reel_subrange_recipe.md`: re-seek mapping, cue-sheet window, beat re-time with snapping, audio and narration rules, QA repeats.
- Research: report §0 item 12, §4.1, §7 rule 9, §8 (#49, #51), §9 item 10, §11 item 9; [V4-MP] §5, §7–§9.
- Project: `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`; `06_skills_library/custom_skills/video_engine/examleaf-reel-repurpose/SKILL.md`; `12_advanced_animations_with_claude/02_documentation/00_OVERVIEW_and_PRINCIPLES.md` §6 (G8) and §10 (RD-16 conflict).
