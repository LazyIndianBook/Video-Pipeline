# Brief template: reference and fallback skeleton

**Canonical template:** `12_advanced_animations_with_claude/06_prompts_and_templates/brief_template.md` (owned by the prompts-and-templates folder, not by this skill). Pass it to the helper with `--template`. This file exists so the helper still works offline and so reviewers can see which placeholders the helper fills.

## Placeholders the helper fills (`{{name}}` syntax)

| Placeholder | Source field in `brief_request.json` |
|---|---|
| `{{scene_id}}`, `{{lesson_id}}`, `{{language}}` | top-level |
| `{{route_tag}}` | `route.tag` (from `examleaf-storyboard-route`) |
| `{{style_id}}`, `{{style_version}}`, `{{style_guide_path}}` | `style.*` |
| `{{script_path}}`, `{{script_sha256}}` | `script.*` (read-only, approved) |
| `{{cue_sheet_path}}` | `cue_sheet.path` |
| `{{brand_tokens_path}}` | `brand_tokens.path` |
| `{{reference_analysis_path}}` | `reference_analysis.path` or `none` |
| `{{fixtures_block}}` | rendered list of `fixtures[]` |
| `{{fonts_allow}}`, `{{fonts_ban}}` | `fonts.allow` (+ `fonts.text` rendered as "text roles (labels, captions, science text)"), `fonts.ban` rendered "(as display faces)" |
| `{{headline_min_s}}`, `{{equation_tail_s}}`, `{{indic_multiplier}}` | `holds.*` |
| `{{iteration_cap}}` | `iteration_cap` |
| `{{effort_model}}`, `{{effort_level}}` | `effort.*` (from `examleaf-effort-governor`) |
| `{{workspace}}` | `workspace` |
| `{{creative_direction}}` | `creative_direction` |
| `{{constraints_block}}` | `templates/constraints_block.md`, filled with the same values |

Any placeholder left unfilled blocks the brief. When the template contains `<!-- BRIEF-START -->` and `<!-- BRIEF-END -->`, only the text between them is rendered (template notes outside the markers are ignored). The canonical template uses this same `{{name}}` syntax (checked 2026-10-15).

<!-- FALLBACK-SKELETON-START -->
# Animation brief: {{scene_id}}

**Lesson:** {{lesson_id}} | **Language:** {{language}} | **Route:** {{route_tag}} | **Style:** {{style_id}}@{{style_version}}
**Author run:** model `{{effort_model}}`, effort `{{effort_level}}`, at most {{iteration_cap}} fix rounds.
**Workspace:** `{{workspace}}` (work only here)

## 1. What to build
One seek-pure 1080x1920 scene for `{{scene_id}}` that animates the approved narration in the {{style_id}} style. Creative direction from the approved storyboard: {{creative_direction}}

## 2. Inputs you may read (and nothing else)
- Approved script (read-only): `{{script_path}}` (sha256 `{{script_sha256}}`)
- Cue sheet (all timing comes from here): `{{cue_sheet_path}}`
- Style guide: `{{style_guide_path}}`
- Brand tokens: `{{brand_tokens_path}}`
- Reference analysis (pacing numbers only): `{{reference_analysis_path}}`
- Validated fixtures (the only source of on-screen science):
{{fixtures_block}}

## 3. Typography
- Allowed fonts: {{fonts_allow}}
- Banned fonts: {{fonts_ban}}

## 4. Constraints (non-negotiable)
{{constraints_block}}

## 5. Deliverables
1. `scene.html` (or the harness's scene file) implementing the contract.
2. `scene_notes.md`: which cue drives each reveal, which fixture field drives each on-screen value.
3. A lint report from `12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js` with zero errors.
<!-- FALLBACK-SKELETON-END -->
