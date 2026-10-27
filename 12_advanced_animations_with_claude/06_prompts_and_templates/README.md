# 06 · Prompts and templates for the advanced-animation layer

**What this folder is.** The reusable text that turns an approved script, a cue sheet, validated fixtures and a chosen style into (1) a brief for the animation agent, (2) a storyboard request and a human review checkpoint, (3) a vertical rewrite of the [V4-MP] master prompt, (4) one filled example per style, and (5) a set of adversarial tests that the agent must pass.

**Evidence labels.** [V#]/[N#] are cited from `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement. [Hypothesis] = untested. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Nothing here has been installed or run.

## 1. Index

| File | What it is | Consumed by | Used when |
|---|---|---|---|
| `brief_template.md` | The canonical L2/L3 structured brief: goal, audience, duration from narration, style, reference numbers, brand tokens, fonts, harness contract, determinism, safe zones, holds, sync, cue sheet, fixtures, forbidden list, iteration cap, deliverables, review checkpoint | `examleaf-anim-brief` (as its `--template`) | Every animation job |
| `master_prompt_paper_collage_VERTICAL.md` | The [V4-MP] master prompt rewritten for ExamLeaf, with `ORIGINAL →` / `EXAMLEAF →` pairs for every step | Humans, `examleaf-anim-brief` (wording), `examleaf-anim-storyboard-gate` | Paper-collage scenes |
| `storyboard_request.md` | The exact request text for the 3×3 grid (code thumbnails and Higgsfield), `beats.json` and `estimate.json` shapes, the credit-estimate line, the hard-stop wording | `examleaf-anim-storyboard-gate` | Before any paid asset or scene code |
| `review_checkpoint.md` | The checkpoint message, what the human checks, outcomes, the approval record | `examleaf-anim-storyboard-gate`, reviewers | At the storyboard gate |
| `prompt_doodle_reel.md` | Filled example: doodle hook, Reel CSV 30 | Assembler tests, reviewers | Style `doodle-handdrawn` |
| `prompt_collage_recap.md` | Filled example: collage recap, Reel CSV 10 | same | Style `paper-collage-vertical` |
| `prompt_editorial_comparison.md` | Filled example: editorial comparison, Reel CSV 11 | same | Style `editorial-vox` |
| `prompt_kinetic_hook.md` | Filled example: kinetic hook, Reel CSV 2 | same | Style `kinetic-type` |
| `prompt_voxel_insert.md` | Filled example: voxel lattice insert, Reel CSV 12 | same | Style `voxel-isometric` |
| `negative_tests.md` | 31 adversarial prompts with the correct response | `examleaf-effort-governor`, `examleaf-anim-qa` evaluation | After any change to a template, a guide or the model |

Style guides these refer to are in `12_advanced_animations_with_claude/05_style_guides/` (see its `README.md`).

## 2. How the templates feed the skills

### 2.1 `examleaf-anim-brief`

- The skill's helper (`03_skills/examleaf-anim-brief/scripts/build_brief.py`) takes `--template` pointing at `brief_template.md` and a job request (`brief_request.json`; example in `03_skills/examleaf-anim-brief/templates/brief_request.example.json`, and one per style in the `prompt_*.md` files, section A).
- It fills the double-brace placeholders in section 3 below. **Any placeholder left unfilled blocks the brief.** The template therefore uses only those names.
- The template carries `<!-- BRIEF-START -->` and `<!-- BRIEF-END -->` markers: the assembler should use only the text between them (the first comment is authoring notes). If it ignores the markers the notes are harmless, they contain no double-brace names.
- Values that come from the cue sheet at run time (the duration, word times, cue times) are written in angle brackets, such as `<cue_sheet.duration>`. The agent resolves them from the staged file; the assembler never does.
- The skill's `constraints_block.md` is inserted as `{{constraints_block}}` at the end. Sections 9-16 of the template restate the same rules in more detail; where wording differs, the stricter rule wins and the assembler should flag the difference.
- The skill's own `brief_template.reference.md` is a fallback skeleton for offline use. This folder owns the canonical template; change it here first.
- The agent's effort is set explicitly (`{{effort_model}}` pinned, `{{effort_level}}` high by default) and ultracode is never used (#1, #3, #4).

### 2.2 `examleaf-anim-storyboard-gate`

- Uses `storyboard_request.md` verbatim for the request (variant A code thumbnails by default; variant B Higgsfield only if approved), produces `grid.png`, `beats.json`, `estimate.json` and `storyboard_note.md`, then prints the hard-stop message and waits.
- Uses `review_checkpoint.md` for the checkpoint message and the reviewer checklist. The approval record is written by the approval service (or, until it exists, a human reviewer), never by the agent (RD-17, RD-32), and is bound to the script hash, the grid, beats and estimate hashes and the credit cap.
- The brief's section 18 refuses to start scene code until that record exists and its `script_sha256` matches.

### 2.3 Master prompt, filled examples, negative tests

- `master_prompt_paper_collage_VERTICAL.md` is the reference wording for the paper-collage workflow; its steps map to pipeline stages (script by the Super Teacher system; storyboard by the gate; voice and cue sheet by the narration pipeline; audio by `examleaf-audio-compose`; QA by `examleaf-anim-qa`).
- `prompt_*.md` are **golden examples**: for the request in section A, the assembler's output should equal the brief in section F, apart from hashes. They also serve as reviewer reference and as fixtures for the QA skill. They use *illustrative* approved text and fixture excerpts marked `EXAMPLE_NOT_A_VALIDATED_FIXTURE`; the animation agent never authors those inputs.
- `negative_tests.md` is run against the agent with a section F brief loaded (its own instructions say how).

## 3. Placeholders filled by the assembler

| Placeholder | Source field in `brief_request.json` |
|---|---|
| `{{scene_id}}`, `{{lesson_id}}`, `{{language}}` | top-level |
| `{{route_tag}}` | `route.tag` (from `examleaf-storyboard-route`) |
| `{{style_id}}`, `{{style_version}}`, `{{style_guide_path}}` | `style.*` (15 Oct 2026: `style_guide_path` is the **staged** copy inside the workspace, `<workspace>/style/<style>.md`; the runner stages and hashes it, see `brief_template.md` §2) |
| `{{script_path}}`, `{{script_sha256}}` | `script.*` (read-only, approved) |
| `{{cue_sheet_path}}` | `cue_sheet.path` |
| `{{brand_tokens_path}}` | `brand_tokens.path` |
| `{{reference_analysis_path}}` | `reference_analysis.path` or `none` |
| `{{fixtures_block}}` | rendered list of `fixtures[]` (the placeholder sits alone on its line; the block is a bulleted list) |
| `{{fonts_allow}}`, `{{fonts_ban}}` | `fonts.*` (computed from `style_tokens.json`; see `05_style_guides/README.md` §4) |
| `{{headline_min_s}}`, `{{equation_tail_s}}`, `{{indic_multiplier}}` | `holds.*` |
| `{{iteration_cap}}` | `iteration_cap` (3) |
| `{{effort_model}}`, `{{effort_level}}` | `effort.*` (from `examleaf-effort-governor`) |
| `{{workspace}}` | `workspace` (ends with `/`) |
| `{{creative_direction}}` | `creative_direction` (from the approved storyboard) |
| `{{constraints_block}}` | `templates/constraints_block.md`, filled with the same values |

These are exactly the names in `03_skills/examleaf-anim-brief/templates/brief_template.reference.md`. Do not add a new double-brace name to `brief_template.md` without adding it to the helper first.

## 4. Runtime references (resolved by the agent, not the assembler)

`<cue_sheet.duration>`, `<cue_sheet.words>`, `<cues[].at>`, `<sfx[].at>`: read from `cue_sheet.json`. The authoritative schema is `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json` (checked by `validate_cue_sheet.py`); the contract is `contract.md`. The harness's safe-zone tokens are `04_harness_contract/vertical_safe_zones.tokens.json` (zone shares and PLACEHOLDER insets); no insets are stored in this folder or in the style guides.

## 5. How a job flows through these files

```text
approved script (GA) + validated fixtures + cue-sheet plan
        │                                   examleaf-storyboard-route tags the scene
        ▼
style chosen (05_style_guides/README.md §2)
        │
        ├─► storyboard_request.md  ──► grid.png, beats.json, estimate.json
        │                              ⛔ review_checkpoint.md (human; approval record bound to hashes)
        ▼
voice (TTS adapter) ─► alignment ─► cue_sheet.json
        │
        ▼
examleaf-anim-brief fills brief_template.md ──► brief (like section F of a prompt_*.md)
        │
        ▼
animation agent (Opus 5.5, high; no MCP; ≤ 3 fix rounds) ──► scene files + notes + lint report
        │
        ▼
examleaf-audio-compose ─► mix ─► examleaf-anim-qa ─► human gates (GF/GS)
```

## 6. Conventions

- **Scene IDs** for Reel scenes: `short-csv<ID>-s<NN>`, where `<ID>` is the Reel backlog CSV ID (the stable ID; `01_business_model/REEL_BACKLOG_36.md`) and `<NN>` the scene number. These IDs are examples, not catalogue entries.
- **Hashes** in examples are written `<64 hex>`; real jobs carry real SHA-256 values.
- **Timings** are PLANNED until the voice is measured; the cue sheet then replaces them.
- **Hooks** are quoted as in the backlog. Where the response and the CSV word a hook differently, the file says so.
- **Versions.** Every file carries a version and date. A change to `brief_template.md` or the constraints block means regenerating the `prompt_*.md` examples and re-running `negative_tests.md`.
- **Language.** Examples are `en-IN`. Hindi, Hinglish and Assamese are drafts until the locale gate (RD-26) and native review.
- **Placeholders.** Double-brace names are assembler placeholders (section 3). Angle-bracket names are runtime references or fields to fill in prose templates (`storyboard_request.md`, `review_checkpoint.md`, the master prompt).

## 7. Edge cases covered

| # | Edge case | Where handled |
|---|---|---|
| 1-4 | Effort default; ultracode | Brief header; master prompt run settings; NT-01, NT-30 |
| 7 | One-line prompt | Entire brief template; every example is L2 |
| 8 | Generic look | Fonts allow/ban and palette in the brief; NT-15 |
| 9 | Context contamination | Brief section 2 and 15; NT-05 |
| 10 | Missing audio | Brief section 13; master prompt Step 6 |
| 11 | Agent-written script | Brief section 1 and 15; master prompt Step 2; NT-09, NT-22 |
| 12 | Hallucinated facts on screen | Brief section 14; NT-03, NT-18, NT-31 |
| 15-19 | Determinism | Brief sections 9-10; NT-07, NT-08, NT-20 |
| 39 | Unnormalised audio | Master prompt Step 6 |
| 40 | Keys in the repo | Brief section 15; NT-19 |
| 41-45 | Credits, caps, late results | `storyboard_request.md` §3.2 and §6; NT-13 |
| 47 | Skipped review gate | `review_checkpoint.md`; brief section 18; NT-12 |
| 48 | Character drift | `storyboard_request.md` preconditions; collage example |
| 49 | 16:9 in a 9:16 pipeline | Brief section 9; NT-06 |
| 50 | Short headline hold | Brief section 12 |
| 51 | Platform UI overlap | Brief section 11; NT-14 |
| 53 | Parser expects a fenced block | Brief section 17: files only, final message is one JSON object |
| 54 | Image model draws text | Brief section 15; storyboard panels; NT-04 |
| 55 | Indic glyph gaps | Brief section 8; kinetic example; NT-17 |
| 56 | Photosensitive flashes | Brief section 15; NT-16 |
| 60 | "Don't stop until perfect" | Brief section 16; NT-02, NT-29 |
| 63 | TTS regenerated | Brief sections 4 and 13; NT-26 |
| 64 | Camera effects over labels | Brief section 14; NT-27 |
| 65 | Headless WebGL variance | Voxel example; NT-18 |

## 8. Known gaps and integration notes

1. **Digest placeholder.** The brief helper has no field for a style digest, so the brief references the style guide by path and tells the agent to read the guide's Digest first. If a `style_digest` placeholder is added to the helper, add it to `brief_template.md` section 5 in the same change.
2. **`indic_multiplier`.** The skill's example request leaves it `null`; the template needs a number. Examples here use 1.5 (a [Hypothesis] to tune in phone tests) even for English-only scenes, where it is unused.
3. **Safe-zone insets are placeholders.** The token file's platform insets are PLACEHOLDERS (`measured` false). Briefs block if the file is missing; otherwise the file's provisional insets apply and the manifest says so. Measuring them later can change the safe box and re-open layout approvals.
4. **Constraints block drift.** The filled examples embed the constraints block as of 15 Oct 2026; regenerate them when it changes.
5. **Model ID.** Examples show `<pinned full model ID, Opus 5.5>`; pin the real ID at launch (#6).
6. **Higgsfield facts.** The model ID `gpt_image_2_5` and its options come from [V4-MP] and must be verified in the tool; per-generation credit costs are not stored anywhere in this folder, and plan prices from competitor sources are not used (report §6.1).
7. **Approval service.** Until it exists, a human reviewer records the approval line in the job folder (RD-17).

## 9. Verify list

Fixture field names (examples are illustrative); the helper's handling of the BRIEF-START/END markers; whether `display_text` is staged and marked `data-fx` as proposed (the contract's `data-fx` rule names fixture fields only); Higgsfield model ID, aspect-ratio options and costs; font licences and glyph coverage (see the style-guide README); phone legibility of every size; the 6 s default `think` window with real students.

## 10. Files

`README.md`, `brief_template.md`, `master_prompt_paper_collage_VERTICAL.md`, `storyboard_request.md`, `review_checkpoint.md`, `prompt_doodle_reel.md`, `prompt_collage_recap.md`, `prompt_editorial_comparison.md`, `prompt_kinetic_hook.md`, `prompt_voxel_insert.md`, `negative_tests.md`.
