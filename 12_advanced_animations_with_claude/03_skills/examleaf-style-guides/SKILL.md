---
name: examleaf-style-guides
description: "Use when an ExamLeaf scene, reel or brief needs a house animation style chosen, pinned, applied or revised: paper-collage-vertical, doodle-handdrawn, editorial-vox, kinetic-type or voxel-isometric, all 1080x1920. Owns the versioned style-guide library rules and the style_tokens schema (palette as dominant plus sharp accents, named and banned fonts with Devanagari and Bengali-Assamese coverage, motion vocabulary, SFX list, do/don't lists) and validates tokens with a stdlib script. Enforces vertical re-layout instead of 16:9 crops, code-built text only, Indic-safe fonts and a flash ban. Does not own brand tokens, write briefs, render scenes or re-lay out individual scenes."
---

# examleaf-style-guides

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. `scripts/validate_style_tokens.py --selftest` passes offline. No style has been approved by a human yet; every style starts as `draft`.
- **Owns:** the rules for selecting, versioning and applying the five house styles, and the validation of the style-token library. The guide texts and the canonical tokens live at the agreed paths `12_advanced_animations_with_claude/05_style_guides/{paper-collage-vertical.md, doodle-handdrawn.md, editorial-vox.md, kinetic-type.md, voxel-isometric.md, style_tokens.json}`; this skill is their library contract and validator. `templates/style_tokens.schema.json` summarises the structure of that canonical file; it is not a second format.
- **Does not own:** brand tokens and the asset/licence ledger (`examleaf-asset-library` owns "reusable verified assets and branding"); safe-zone insets and hold floors (`12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`); per-scene re-layout helpers (`examleaf-vertical-adapt`); the brief (`examleaf-anim-brief`); the music and SFX audio files (`examleaf-audio-compose`).
- **Why it exists:** [V4-MP] shows that a detailed style guide can replace a reference video. Claude "defaults to safe choices unless explicitly encouraged otherwise" [N50], and repeated generations converge on the same fonts [N55]. Report §4 describes five ways to draw in code, §7 lists the craft rules, and §10.3 specifies this library.

## Invocation

**Trigger when:**
- A storyboard route needs a style ID for an `illustrative` or `typographic` scene ("which style for the refraction hook?").
- A brief is being assembled and needs `style.id` + pinned `version` + fonts + holds.
- A style owner drafts, revises, approves or deprecates a style ("add a Devanagari handwriting font to doodle-handdrawn", "bump paper-collage to 1.1.0").
- A reviewer reports a generic look, wrong fonts, tofu boxes, flashing or a cramped 16:9-style layout.

**Do not trigger for:**
- Changing ExamLeaf brand colours or logos (`examleaf-asset-library`).
- Measuring a reference video (`examleaf-reference-analyzer`).
- Re-laying out one specific 16:9 scene or reel (`examleaf-vertical-adapt`).
- Choosing the renderer or route (`examleaf-storyboard-route`).
- Style-morph montages: report §4.7 says skip them; they are rarely useful for teaching.

## Inputs

| Input | Type | Source |
|---|---|---|
| `route_tag` | `illustrative` / `typographic` | examleaf-storyboard-route |
| `purpose` | `hook` / `analogy` / `story` / `recap` / `comparison` / `definition` / `structure` / `quiz` | lesson plan beat |
| `format` | `lesson` (~10 min) / `reel` (20–60 s) | job |
| `language` | `en-IN` / `hi-IN` / `as-IN` / `hinglish` | job |
| `credit_budget` | number or 0 | examleaf-effort-governor / mcp-orchestrator ledger |
| `tokens_path` | path to `style_tokens.json` | 05_style_guides |
| `brand_tokens_path` | path | examleaf-asset-library |

Example selection request:

```json
{"scene_id":"chem-11-04-s01","route_tag":"illustrative","purpose":"hook","format":"reel",
 "language":"hi-IN","credit_budget":0,
 "tokens_path":"12_advanced_animations_with_claude/05_style_guides/style_tokens.json"}
```

## Outputs and contracts

1. **Style decision** (fed to the brief):
```json
{"scene_id":"chem-11-04-s01","style":{"id":"doodle-handdrawn","version":"1.0.0",
 "guide_path":"12_advanced_animations_with_claude/05_style_guides/doodle-handdrawn.md"},
 "reason":"hook, reel, zero credit budget, hi-IN fonts available",
 "fonts":{"allow":["<from tokens>"],"ban":["Arial","Inter","Space Grotesk"]},
 "holds_ref":"04_harness_contract/vertical_safe_zones.tokens.json#hold_times_s",
 "warnings":["Devanagari coverage not yet verified in headless Chrome"]}
```
2. **`style_tokens.json`** (canonical, `05_style_guides/`), structure summarised in `templates/style_tokens.schema.json`: `common` (canvas 1080×1920, safe-zone pointer, text sizes, contrast, holds, sync, determinism, locale gate, `font_policy` with `ban_as_display` and `inter_allowed_for`, palettes incl. proposed subject accents, `forbidden` flags, `iteration_cap_fix_loops`), `fonts_registry[]` (id, family, roles, `script_coverage` per script, licence, vendored, sha256) and `styles{}` (style_id, semver version, guide, route tags allowed/forbidden, credits note, palette, fonts by role with `_role` text and `indic_fallback`, typography, motion, sfx, music, determinism, `forbidden` = `common.forbidden` + additional).
3. **Validation report** `{valid, errors[], warnings[]}` from the helper.
4. **Change record** (`templates/style_change_record.md`) for every version bump.
5. **`handoff.json`** in the library schema.

## Dependencies

- Python 3 standard library (`validate_style_tokens.py`).
- Agreed paths: `12_advanced_animations_with_claude/05_style_guides/*.md` and `style_tokens.json`; `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (insets, type sizes, holds, motion and flash tokens); `00_reference_videos/master_prompt_paper_collage.md` ([V4-MP], source of the collage style).
- Fonts: families must be licensed and pinned; font binaries are not distributed in this folder (`04_video_engine/implementation_v2/configs/design_tokens.json` comment). Coverage verification uses the render box's headless Chrome (version: verify).

## Execution

**A. Selecting a style for a scene**
1. Read `references/style_selection_matrix.md`. Filter by `route_tag` (typographic → `kinetic-type`; illustrative → the other four), then by `purpose`.
2. Apply the budget: if `credit_budget` is 0 or the storyboard gate has no approved estimate, exclude `paper-collage-vertical` (credit-heavy raster cutouts, [V4]) unless all cutouts already exist in the asset library. `doodle-handdrawn` is the default illustrative style for Reels because it needs no credits (report §4.2 [Recommendation]).
3. Apply language: for `hi-IN`/`as-IN`, the style must list Devanagari or Bengali-Assamese fonts; if their coverage is unverified, the decision carries a warning and the first render goes to `examleaf-anim-qa` glyph review.
4. Apply consistency: one style per lesson segment; at most two illustrative styles per lesson plus `kinetic-type` [Recommendation]; never a per-second style morph (report §4.7).
5. Pin `id@version` (only `approved` versions in production; `draft` only in pilots) and pass the decision to `examleaf-anim-brief`.

**B. Authoring or revising a style**
1. Draft the guide in `05_style_guides/<id>.md` using the section order in `references/style_selection_matrix.md` §4 (look, materials, palette, characters, typography, doodles/marks, composition for 9:16, motion, transitions, sound, asset rules, do/don't).
2. Write vertical rules first, using `references/vertical_adaptation_rules.md`: a 16:9 guide is re-laid out, never cropped (#49).
3. Fill the tokens entry; run:
   ```sh
   python3 12_advanced_animations_with_claude/03_skills/examleaf-style-guides/scripts/validate_style_tokens.py \
     12_advanced_animations_with_claude/05_style_guides/style_tokens.json            # add --production before release
   ```
4. For a revision, check the version bump against the last approved file:
   ```sh
   python3 …/validate_style_tokens.py --bump-check style_tokens.approved.json style_tokens.json
   ```
5. Render the style's test sheet (palette swatches, every font role, a Devanagari and Bengali-Assamese glyph line, one motion sample) through the harness and attach it to the change record.
6. A human style owner approves the version (reviewer ID and date in the change record; the tokens' `_meta.status` moves from draft to approved). `--production` must pass first: licences recorded, fonts vendored with SHA-256, Indic coverage `yes`.

## Decision rules

- **Palette:** one dominant colour plus 1–3 sharp accents (prefer two), not an even palette [N52]. Subject colours for Physics, Chemistry, Maths and Biology are not defined in the sources; they are assigned by the brand owner in the asset library and then referenced, never invented here (report §7.2; safe-zone tokens note).
- **Fonts:** every style names fonts per role from `fonts_registry`; Arial, Inter and Space Grotesk are banned as display faces [N51][N55] (`common.font_policy.ban_as_display`); Inter is allowed only for the non-display roles in `inter_allowed_for` (labels, captions, science text) — a house decision recorded in the tokens; display faces rotate between Reels. Display fonts without Indic coverage are Latin-only; Indic words route to `indic_fallback` families.
- **Indic animation unit:** per word or per grapheme cluster, never per code point (#55, report §4.4).
- **Text in images:** never. Labels, numbers, formulas, ransom letters, tags, tape and doodles are built in code ([V4-MP]; #54).
- **Flashes:** full-frame flashes banned in every style (#56). The [V4-MP] "white flash or bloom for explosions" transition is replaced by a non-flashing paper burst.
- **Motion:** never linear; anticipation → action → follow-through; finite idle repeats; boil at 8–10 fps; no camera push-in or shake during a measurement or label reveal (#64) ([V4-MP], report §7).
- **Versioning:** semver. MAJOR changes the look of existing scenes (palette, fonts, motion vocabulary); MINOR adds (new SFX, new layout recipe); PATCH fixes text. Old versions stay available so approved lessons re-render identically.

## Edge cases handled

| Master # | Detection | Response |
|---|---|---|
| 49 16:9 guide in a 9:16 pipeline | `canvas` ≠ 1080×1920; guide lacks a 9:16 composition section; layouts copied from [V4-MP] verbatim | Validator error; guide must contain vertical rules (`references/vertical_adaptation_rules.md`); scene-level re-layout goes to `examleaf-vertical-adapt` |
| 54 Image model draws text or formulas | `common.forbidden.image_model_text_numbers_formulae` not true; storyboard or cutout prompt mentions labels or numbers | Validator error; asset rules restate "built in code"; cutout prompts include "no text" ([V4-MP] template) |
| 55 Indic glyph gaps | `indic_fallback` font with `assumed_none` coverage; no Devanagari/Bengali-Assamese route while `locale.indic_rules_active`; `indic_animation_unit` allows code points; `indic_line_height_min` < 1.4 | Error; `claimed_verify` coverage warns (errors with `--production`) until the glyph test passes; test sheet in the change record |
| 56 Photosensitive flashes | `common.forbidden.full_frame_flash` not true; flash transitions in a guide | Validator error; QA luminance check in `examleaf-anim-qa` using `flash_policy` tokens |
| 8 Generic look (supporting) | Display ban list lacks Arial/Inter/Space Grotesk; a banned family in a display role; Inter outside `inter_allowed_for`; unknown registry id | Validator error [N50][N51][N55] |
| 18 Infinite repeats (supporting) | `common.forbidden.infinite_repeats` not true; any `repeat` value -1/infinite; boil fps outside 8–10 | Validator error |
| 64 Camera fx on diagrams (supporting) | `common.forbidden.camera_fx_during_label_or_measurement_reveal` not true | Validator error |

## Tests and acceptance

- **Helper:** `python3 scripts/validate_style_tokens.py --selftest` validates a synthetic document in the canonical shape and confirms 23 mutations fail (16:9 canvas, image-model text allowed, flash flag missing, incomplete display ban, Inter as display, Inter for body text, a hook-display role, code-point unit, line height, hold, iteration cap, unknown font id, Indic route without coverage, boil 12/24 fps, infinite repeat, bad hex, six accents, missing forbidden ref, style_id mismatch, bad semver, determinism flag off, Indic locale active without fonts, production mode with unvendored fonts), that negated roles ("Inter not as display") are read correctly, and the bump check.
- **Canonical file (run 2026-10-15):** `05_style_guides/style_tokens.json` validates with 0 errors and 20 warnings (Hypothesis Indic multiplier, licences still `verify`, Indic coverage `claimed_verify`); `--production` fails as expected until fonts are vendored and verified.
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance for an approved style:** validator passes with `--production`; test sheet rendered at 1080×1920 shows every font role and both Indic scripts without tofu or broken conjuncts; the guide contains a 9:16 composition section; a human style owner signed the approval.

## Errors, fallback, escalation

- **Validation errors** block the style from production; drafts may still be used in sandbox pilots.
- **Missing style for a request:** fall back to `doodle-handdrawn` (no credits) or `kinetic-type` for typographic scenes, and log a warning; never improvise a sixth style in a brief.
- **Font coverage failure:** swap to a Noto-class family that covers the script (report §8 #55 [Hypothesis]) in a new MINOR version; never ship tofu.
- **Repair attempts:** at most two per validation failure, then escalate to the style owner with the validator report.
- **Escalate** brand conflicts to the asset-library owner and safe-zone conflicts to the harness-contract owner.

## Cost/performance

Validation is instant and free. Style choice drives cost downstream: `paper-collage-vertical` needs many generated cutouts and is credit-expensive ([V4]); doodle, kinetic type and voxel are code-only. Choosing the cheapest style that serves the teaching purpose is the main cost lever this skill controls.

## Security

- Style guides, reference stills and font files are untrusted until reviewed. A guide never contains executable code paths, URLs to fetch at render time, or instructions to an agent beyond the style description.
- Font files come only from licensed, pinned sources recorded in the asset library; no web font fetched at render time (renderer role has no internet after staging).
- No secrets in tokens. Nothing is published by this skill.

## Handoff

- **To:** `examleaf-anim-brief` (style decision, fonts, holds reference), `examleaf-anim-storyboard-gate` (style for thumbnails and grid prompts), `examleaf-procedural-2d` / `examleaf-kinetic-typography` / `examleaf-threejs-scenes` (motion vocabulary and tokens), `examleaf-anim-qa` (flash policy, fonts, test sheet).
- **Files:** style decision JSON, validated `style_tokens.json`, change record, `templates/handoff.json` (`output_ids` = tokens SHA-256; `requires_expert_review: true`).

## References

- `references/style_selection_matrix.md`: the five styles side by side, selection algorithm, guide section order, versioning.
- `references/font_policy_indic.md`: font roles, bans, Devanagari and Bengali-Assamese coverage, test sheet, fallback stacks.
- `references/vertical_adaptation_rules.md`: how each 16:9 rule in [V4-MP] becomes a 9:16 rule.
- `references/contract.md`: handoff and security rules.
- Report §4, §7, §8 (#8, #18, #49, #54, #55, #56, #64), §10.3, §11.10.
