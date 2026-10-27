# 11 · Integration with the ExamLeaf pipeline

**Purpose.** How the advanced-animation layer plugs into the existing per-lesson procedure without weakening any gate: the routing tags, the 11-step flow with owners and hand-offs, the accuracy invariant, how Reels re-use time-pure scenes, and the **proposed runbook amendments** to `07_end_to_end_pipeline_instructions/`. Expands report §9 and §10.

**Status.** [PROPOSED]. This document does **not** edit ROOT/07. Every change to the runbook is listed in §7 as a proposed amendment for the project owner, to be recorded first in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` ("Change it here first").

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V#], [V4-MP], [N#], ROOT-relative project paths, [Recommendation]/[Hypothesis], master edge cases #1–#65, NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

---

## 0. Summary

1. **Nothing upstream changes.** Sources, claims, script, science validation and GA run exactly as in `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S0–S7. "The animation agent never writes or edits approved text" (report §9 step 2).
2. **Routing gains four tags** that sit on top of the existing router rules 1–6: `data-bound`, `spatial-hero`, `illustrative-narrative`, `typographic`.
3. **Two human checkpoints are added** inside the production stages: the storyboard-and-estimate gate (H-SB) and the director's rubric review (H-RV). GA, GF and GS are unchanged and still mandatory.
4. **New skills extend, not duplicate**, existing owners ("One Skill owns each output", `06_skills_library/OVERLAP_and_DEDUPLICATION.md`).
5. **The accuracy invariant** is enforced at four points: fixtures as read-only props, contract lint, DOM/OCR text diff, science-frame QA.
6. **Reels re-seek time-pure lesson scenes**, re-laid out for 9:16 and re-timed only by holds and decorative motion — never by speeding narration.

---

## 1. Routing tags

`examleaf-storyboard-route` keeps sole ownership of routing (`06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md` row 9). The tags are added to each scene's route record [Recommendation].

| Tag | What it covers | Router rules (03 S8) | Renderer / skill | Text and data rules |
|---|---|---|---|---|
| `data-bound` | Axes, values, graphs, equations, structures, counts, reaction states | 1, 2 | `examleaf-svg-scenes` (default), `examleaf-manim-scenes`, `examleaf-molecule-scenes`, `examleaf-biology-scenes`, `12_advanced_animations_with_claude/03_skills/examleaf-threejs-scenes/` (fixture-fed) | Every glyph from a fixture; deterministic only; no decorative distortion |
| `spatial-hero` | 3D structure where depth is the point | 3 | `examleaf-blender-scenes` (P2, opt-in) or `examleaf-threejs-scenes` | Labels in overlay from fixtures; "3D only if needed" |
| `illustrative-narrative` | Hooks, analogies, stories, recaps, history-of-science, end cards | 4, 5 | `12_advanced_animations_with_claude/03_skills/examleaf-procedural-2d/`, style guides; optional rasters via `examleaf-selective-generation` through `12_advanced_animations_with_claude/03_skills/examleaf-mcp-orchestrator/` | Non-authoritative; no labels or formulas in rasters (#54); must not contradict the science (report §7.13) |
| `typographic` | Kinetic titles, punchlines, CTAs, emphasis words | 5 | `12_advanced_animations_with_claude/03_skills/examleaf-kinetic-typography/` | Expressive layer only; scientific values stay in science text (doc 08 §2) |

**Layered scenes.** One scene can carry several layers (e.g. a doodle character pointing at a data-bound graph). Tag **per layer**; the strictest layer rules apply wherever layers overlap. Decorative wobble or boil never applies to a data-bound layer (NEW-28) [Recommendation].

**Animation decision first.** Before any tag, the existing test applies: animate only when the learner must understand what changes, in what order, in which direction, because of what (`02_learning_psychology/INSTRUCTIONS_production_rules.md` E1). Motion budget 25–35 % of runtime in first pilots, counted as substantial explanatory change (E2).

---

## 2. The 11-step flow, expanded

Arrows are hand-offs; ⛔ marks a mandatory gate. Paths are inside the lesson folder (`lessons/<board>/<class>/<subject>/<lesson_id>/`, `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` §1); `anim/` is the proposed new subtree (PA-01).

| Step | What happens | Existing owner(s) | New skill that fires | Input | Output artefact | Gate |
|---|---|---|---|---|---|---|
| 1 | Lesson plan, claims, **validated fixtures** | `examleaf-curriculum-map`, `examleaf-lesson-plan`, `examleaf-claim-research`, `examleaf-science-<subject>` | — | Source, syllabus map | `claims.json`, `science/verified-model.json`, fixture JSON per scene | H-S2 |
| 2 | Script | `examleaf-super-teacher-scriptwriter` (+ `examleaf-dialogue-naturalizer`), `examleaf-science-reviewer`, `examleaf-confidence-editor` lens | — | Lesson spec | `script/approved-script.txt`, `narration_plan.json` | ⛔ **GA** |
| 3 | Storyboard routing with tags | `examleaf-storyboard-route` | `examleaf-reference-analyzer` (if a reference is used), `examleaf-style-guides` | Approved script, verified model | `scenes/scene-spec.json` + route record with tags and cost cap; `anim/reference/<ref>.analysis.json` | — |
| 4 | Storyboard grid + estimate | `examleaf-storyboard-route` (parent) | `examleaf-anim-storyboard-gate`, `examleaf-effort-governor` (estimate) | Route record, style guide | `anim/storyboard/<segment>_grid.png`, `beats.json`, `estimate.json`; approval in `approvals/` | ⛔ **H-SB** storyboard gate (doc 05: visuals, scope, cost) |
| 5 | Narration and timing | `examleaf-voice-synthesis` → `examleaf-tts-provider-adapter`; `examleaf-stem-pronunciation`; `examleaf-multilingual-director`; `examleaf-alignment-localize` → `examleaf-speech-animation-synchronizer` | `examleaf-cue-sheet` | GA-approved script | `audio/*`, `audio/timeline.json`; `anim/<scene_id>/cue_sheet.json` | Native review; critical-term listening |
| 6 | Scene authoring (Claude Code, Opus 5.5 high) | Routed scene skill | `examleaf-anim-brief`, `examleaf-motion-harness`, `examleaf-procedural-2d` / `examleaf-kinetic-typography` / `examleaf-threejs-scenes`, `examleaf-vertical-adapt`, `examleaf-effort-governor` | Brief, cue sheet, tokens, style guide, fixtures (read-only, staged into the job folder) | Authoring in `anim_jobs/<lesson_id>/<job_id>/scenes/` (doc 01 §8); approved code copied back to `scenes/<scene_id>/`, clips and manifests to `render/clips/` | A1 lint; caps |
| 7 | Composition (1080×1920, AD-07) | `examleaf-web-composition` (HyperFrames default; Remotion benchmark) | `examleaf-motion-harness` | Scenes, clips, timeline | Composed video (silent) + render manifest | A3, A11, A15 |
| 8 | Audio | `examleaf-audio-production-engineer` | `examleaf-audio-compose`, `examleaf-audio-analysis` | Voice master, cue sheets | `audio/beds/`, `audio/sfx/`, `audio/mix/programme.wav` | A9 |
| 9 | QA | `examleaf-visual-qa`, `examleaf-audio-caption-qa`, `examleaf-release-review` | `examleaf-anim-qa` | Render, mix, captions, fixtures | `qa/anim_*.json`, `qa/visual_qa.json`, `qa/audio_caption_qa.json` | H-RV; ⛔ **GF** |
| 10 | Reels | `examleaf-reel-repurpose`, `examleaf-thumbnail-package` | `examleaf-vertical-adapt`, `examleaf-audio-analysis`, `examleaf-cue-sheet` | Approved lesson, ShortSpec | `shorts/<short_id>/…` | ⛔ **GS** |
| 11 | Ops | `examleaf-observability-cost`, `examleaf-render-batch`, `examleaf-skills-security` | `examleaf-effort-governor`, `examleaf-mcp-orchestrator` | All runs and jobs | `costs.json`, `anim/ledger/`, provider job records | Budget stop rules |

### 2.1 Step notes

**Step 1 — fixtures.** A fixture is approved typed data for one scene: values with units, geometry, labels, symbol IDs, axis ranges, the seed, and source/claim IDs. It derives from `science/verified-model.json` and is hashed into the GA bundle when it carries scientific content [Recommendation]. Scene code receives it read-only (report §9 accuracy invariant).

**Step 3 — reference analysis.** `examleaf-reference-analyzer` turns a reference video into numbers (fps, duration, shot lengths, cut rhythm, palette, text holds) using FFmpeg/ffprobe (report §7.10; commands in `12_advanced_animations_with_claude/04_harness_contract/reference_analysis.sh`, verify on your build). References are analysis inputs only, never assets (NEW-25); variable-frame-rate and letterboxed inputs are normalised first (NEW-24).

**Step 4 — storyboard gate.** Prefer **code-rendered thumbnails** (free) over Higgsfield grids (credits). The gate records: the 3×3 grid in beat order, the route tag per panel, the planned style, the token estimate per scene (doc 09 §11), the credit estimate if any paid asset is planned, and the reviewer's approval in the approval service. [V4]'s checkpoint exists "precisely to avoid wasting credits" (report §6.4) (#47).

**Step 5 — narration first, animation second.** Durations are finalised after the actual audio exists (03 S11). The cue sheet is a per-scene projection of `timeline.json` (doc 06 §5.4).

**Step 6 — authoring.** The brief (`examleaf-anim-brief`) contains: approved script excerpt (read-only), route tag, style guide ID, cue sheet, tokens, fixture schema, the harness contract, font allow/ban lists, hold rules, safe zones, iteration cap, and "do not read other folders" ([V3]; #9). Settings per doc 09 §3. Agent role: "Animation engineer — compile scenes and repair bounded implementation failures; must not rewrite approved science to make a render easier" (`07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §2.1).

**Step 7 — composition.** HyperFrames is the master timeline (report §2.6; RD-07 keeps the native SVG adapter as reference and regression renderer). Clips from Manim, three.js and Blender are placed at frame-exact offsets (doc 07 §5). Video-heavy compositions render with one worker [N70].

**Step 9 — QA.** Checks A1–A17 and the rubric are in `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`.

---

## 3. Hand-off artefacts

Authoring happens in an isolated job folder, `anim_jobs/<lesson_id>/<job_id>/`, with read-only staged fixtures, cue sheets, style files and tools (`12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` §8). The table lists the **canonical** location in the lesson folder; the job runner, not the agent, copies approved results back with hashes.

| Artefact | Path (proposed) | Producer | Consumers | Hashed into |
|---|---|---|---|---|
| Fixture JSON | `anim/<scene_id>/fixtures/*.json` (copies) or references to `science/` | `examleaf-science-<subject>` | Scene code, A7, A12 | GA bundle (scientific fixtures); render cache key |
| Reference analysis | `anim/reference/<ref_id>.analysis.json` | `examleaf-reference-analyzer` | Brief | — |
| Brief | `anim/<scene_id>/brief.md` | `examleaf-anim-brief` | Authoring session | Ledger record |
| Storyboard grid, beats, estimate | `anim/storyboard/` | `examleaf-anim-storyboard-gate` | H-SB reviewer | H-SB approval |
| Approval records | `approvals/` (approval service only) | Authenticated approval service | `examleaf-release-review` | Bound to artefact hashes |
| Cue sheet | `anim/<scene_id>/cue_sheet.json` | `examleaf-cue-sheet` | Scene code, A5, A10 | Render cache key |
| Scene code | Written in `anim_jobs/<lesson_id>/<job_id>/scenes/`; approved copy in `scenes/<scene_id>/` (job runner copies with hashes, doc 01 §8.2 rule 6) | Authoring session | Harness | Render cache key |
| Clips + `clip.json` | `render/clips/<clip_id>/` | Routed scene skill | `examleaf-web-composition` | Asset ledger |
| Beds, SFX, analysis, mix | `audio/beds/`, `audio/sfx/`, `audio/analysis/`, `audio/mix/` | Audio skills | Mixer, QA | Asset ledger; audio hashes |
| QA reports | `qa/anim_*.json` | `examleaf-anim-qa` | GF/GS evidence | Release evidence |
| Run ledger | Job `logs/run.json` (doc 01 §7.5) → copied to `anim/ledger/<run_id>.json` → rolled into `costs.json` | `examleaf-effort-governor` | `examleaf-observability-cost` | — |

---

## 4. The accuracy invariant

> "Any glyph that encodes science must be traceable to a fixture field. This covers numbers, units, chemical formulae, labels, arrows' directions and graph shapes. Scene code receives fixtures as read-only props, and QA diffs rendered text against fixtures." (report §9)

| Enforcement point | Mechanism | Check |
|---|---|---|
| Authoring | Brief passes fixtures as read-only data; the agent is told it may not type scientific values | Contract lint flags numeric literals in data-bound layers (A1) |
| Rendering | Displayed state computed from the same science function at frame time (03 S9) | Same-state tests for new templates (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §9) |
| Text | Every text node in a data-bound layer carries a fixture field ID | A7 DOM diff; OCR/human for rasters |
| Geometry | Positions projected from fixture coordinates | A12 geometry check; zero wobble on data strokes (NEW-28) |
| Generated media | No text in rasters; "Numerical/diagram assertions may not be delegated to a diffusion/video model" (03 S8) | OCR on generated assets (A7) |
| Approval | Fixture hash in the GA bundle; any change invalidates GA and GF (03 S15) | `release-check` hash binding |

Corollary: [V3]'s model "did its own proper research on the benchmarks" — in ExamLeaf that is forbidden for any on-screen fact (report §1.2) (#12).

---

## 5. Who owns what: existing versus new skills

| New skill | Relationship | Owns | Must not |
|---|---|---|---|
| `examleaf-anim-brief` | New; depends on storyboard-route, pacing-controller | `brief.md` | Edit script or fixtures |
| `examleaf-reference-analyzer` | New | Reference analysis JSON | Reuse reference frames as assets |
| `examleaf-style-guides` | New library | Versioned 9:16 style guides and tokens | Override house palette for science text |
| `examleaf-anim-storyboard-gate` | **Extends** `examleaf-storyboard-route` | Grid, beats, estimate | Approve itself |
| `examleaf-motion-harness` | **Extends** `examleaf-web-composition` | Contract, linter, determinism test | Maintain a second compositor by default ("Do not maintain both by default", RD-07) |
| `examleaf-procedural-2d` | New scene skill | Doodle/collage primitives | Distort data-bound geometry |
| `examleaf-kinetic-typography` | New scene skill | Expressive text timing and modes | Write captions (cluster 9) |
| `examleaf-threejs-scenes` | New scene skill | Seek-pure 3D clips | Invent geometry outside fixtures |
| `examleaf-audio-compose` | New | Beds, SFX | Master the mix; play music in core explanation |
| `examleaf-audio-analysis` | New | Beat grid, energy | Re-align narration |
| `examleaf-cue-sheet` | **Extends** `examleaf-speech-animation-synchronizer` and `examleaf-alignment-localize` | Per-scene cue sheets | Re-author timeline or captions |
| `examleaf-mcp-orchestrator` | New wrapper around `examleaf-selective-generation` | Per-job permissions, credit ledger calls | Hold keys in the repo; retry unknown jobs |
| `examleaf-effort-governor` | **Extends** `examleaf-observability-cost` | Model/effort/iteration policy, run ledger | Allow ultracode |
| `examleaf-anim-qa` | **Extends** `examleaf-visual-qa` and `examleaf-audio-caption-qa` | A-checks reports | Approve releases |
| `examleaf-vertical-adapt` | New helper | 9:16 re-layout rules, sub-range Reels | Crop ("`crop` is rejected", `ShortSpec`) |

All new skills are admitted and activated like the existing ones (`06_skills_library/INSTRUCTIONS_install_and_use_skills.md`); third-party skills (remotion-dev/skills [N1], heygen-com/hyperframes [N58]/plugin [N10], klsoen/opus-js-animations [N15], adithya-s-k/manim_skill CE only [N45]) go through `examleaf-skills-security` first (report §10).

---

## 6. Reels: re-seek sub-ranges and re-time to a beat grid

### 6.1 Why it works

Because every scene is a pure function of time [N61] (contested) with seeded randomness, any time window `[a, b]` of a lesson scene can be rendered on its own by calling `seek(a + τ)` for `τ ∈ [0, b − a]`. No earlier frames are needed. NEW-23 is the failure when this is violated: state accumulated from earlier frames.

### 6.2 Procedure

1. **Select the unit** (SH1): one misconception → one prediction → one payoff → one CTA (`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` §1). Write the `ShortSpec` (SH2): 20–60 s, `layout_strategy: reflow`, `retained_conditions` listed.
2. **Choose source windows** at sentence boundaries from `timeline.json` (never mid-word). Record each as `(scene_id, a, b)`.
3. **Re-layout for 9:16** with `examleaf-vertical-adapt`: the same verified state, re-authored panels, axes/units/conditions visible; "A crop that removes a graph axis or condition is a scientific defect" (§1). If the lesson scene has a 16:9-only layout, the vertical layout must be authored and tested (`test_vertical_not_crop` pattern).
4. **New wording** (hook line, shortened payoff, CTA) is new script: S5 rules, narration sub-pipeline, and academic approval of the changed wording (SH4).
5. **Build the Reel cue sheet** from the Reel's own timeline (the reused segments keep their accepted audio hashes).
6. **Optional beat grid.** If a bed is used (hook and CTA only, playbook usage map), take its analytic grid (doc 06 §4.2) or analyse a licensed bed with librosa (#31–#38).
7. **Re-time decoratively, never narratively** [Recommendation]:
   - Allowed: shift transitions, idle loops, doodle boils and SFX to the nearest beat within ±0.1 s; lengthen or shorten **holds between sentences** (not protected thinking pauses) by up to one beat to land a semantic reveal on a beat.
   - Forbidden: changing narration speed or pitch ("speeding audio to fit a slot" is a forbidden repair, 03 S16; NEW-29); moving a semantic reveal off its word; shortening a hold below its minimum (doc 08 §6).
   - If a reveal cannot land on a beat within the rules, leave it on its word.
8. **Hook card** (0–3 s): question text from the approved script in the expressive layer; the axis or diagram it refers to appears from fixtures.
9. **Render and QA** the Short as a new artefact: full A-suite, then ⛔ **GS** (SH7).
10. **Package** with `examleaf-thumbnail-package`: truthful title and cover (SH6).

---

### 6.3 What changes in the Reel timing structure

The house structure (SH5) stays: 0–3 s hook, 3–8 s prediction or tempting error, 8–30 s complete explanation, final seconds one CTA. The advanced layer only changes **how** each part looks (doodle, collage, kinetic type), not the structure.

---

## 7. Proposed runbook amendments (do not edit ROOT/07; for the project owner)

Each item names the target, the change, and the reason. Record accepted items as new RD rows first.

| ID | Target | Proposed change | Reason / evidence |
|---|---|---|---|
| PA-01 | `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` §1 lesson folder | Add `anim/` (brief, reference analysis, storyboard, per-scene cue sheets and fixtures, run ledger), `render/clips/`, and `audio/beds/`, `audio/sfx/`, `audio/analysis/`, `audio/mix/`; record the job-workspace pattern `anim_jobs/<lesson_id>/<job_id>/` of doc 01 §8 | §3 hand-offs |
| PA-02 | Same, S8 | Add the four routing tags as a field of the route record; per-layer tagging; illustrative layers non-authoritative | §1 |
| PA-03 | Same, S8 → S9 | Insert gate **H-SB** (storyboard grid + token/credit estimate) before asset generation and scene authoring for `illustrative-narrative`, `typographic` and `spatial-hero` scenes | [V4] checkpoint; #47 |
| PA-04 | Same, S9 | Add `examleaf-threejs-scenes`, `examleaf-procedural-2d`, `examleaf-kinetic-typography` as routed scene skills; require harness-contract compliance and A1 lint | Doc 07, doc 08 |
| PA-05 | Same, S11 | Add per-scene cue-sheet generation as a projection of `timeline.json`; re-build on any audio time change | Doc 06 §5 |
| PA-06 | Same, S12 | Hash PNG frames before encode for determinism (contract §11); one worker for video-heavy compositions; clip manifests | [N70]; NEW-12 |
| PA-07 | Same, S13 and `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2–§3 | Add checks A1–A17 and the H-RV rubric | Doc 10 |
| PA-08 | Same, S15 cache key | Add harness-contract version, style-token hash, cue-sheet hash, seed, Chrome/three.js/Manim/Blender versions, font and bed hashes | Determinism (#17, #65) |
| PA-09 | `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13 | Permit Python-composed SFX and short beds in non-core segments per the playbook usage map; music stays off in core explanation; final-mix loudness re-measured | Doc 06 §1, §7 |
| PA-10 | `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` SH3–SH5 | Add sub-range re-seek and the decorative-only beat re-timing rules (§6.2 step 7) | §6; NEW-29 |
| PA-11 | `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §1, §3 | New stage line "Animation authoring (Claude Code)" with a provisional per-scene cap until pilot data; add the run-ledger fields of doc 09 §9.2 to `costs.json` | Doc 09 §11.2 (even [V1]'s low figure per scene exceeds the $1.72 LLM line) |
| PA-12 | Same, §8 and `07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §4 | Effort governance: explicit effort, pinned full model IDs, no ultracode, iteration caps | Doc 09; [N22]–[N28] |
| PA-13 | `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` | Admission list for the third-party animation skills; MCP permissions per job, not global ([V3] grants "full permission" — not in production) | Report §6.4, §10 |
| PA-14 | `07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §1 | Add a human **animation director** (production side) who prepares the storyboard gate (approvers per doc 05 §1) and runs H-RV; may be the production QA reviewer only if GF still has two different identities | Doc 10 §3 |
| PA-15 | `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` | Record the conflicts in §8 as new RD rows | §8 |
| PA-16 | `07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` | Add contracts: cue sheet (schema in `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`), clip manifest, `bed.json`, run-ledger record, `anim_qa.json` | Docs 06, 07, 09, 10 |
| PA-17 | `07_end_to_end_pipeline_instructions/11_MASTER_CHECKLIST.md` §D, §F, §G, §I | Add the H-SB, cue-sheet, A-check and ledger items | — |
| PA-18 | `07_end_to_end_pipeline_instructions/02_PHASED_BUILD_ROADMAP.md` P1–P2 | Run the harness benchmark and the animation pilot (`12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/`) inside P1/P2 on the same golden fixtures | RD-07 metric order |

---

## 8. Conflicts with existing project documents

The section's register of conflicts and decisions is `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md` (decisions AD-01…, conflicts C1…). The table below uses those IDs; rows marked **new** were found while writing docs 06–13 and should be added to doc 14.

| Doc 14 ID | Topic | This layer | Existing document | Resolution |
|---|---|---|---|---|
| C1 / AD-07 | Master aspect | Vertical only, 1080×1920 at 30 fps | 03 scope "ONE long-form lesson (16:9)"; RD-16 masters both aspects | Runbook owner records a master-format decision; until then the engine keeps both aspects and this layer outputs vertical. **Recorded 15 Oct 2026:** RD-16 SUPERSEDED, vertical-only (07/10); the proof renderer still needs a 1080×1920 @ 30 fps mode (P1 build item; doc 13 B.6) |
| C2 / AD-04 | Loudness | [V4-MP] −14 LUFS, < −1.5 dBFS | −16 LUFS ± 1, ≤ −1 dBTP | Lessons −16/−1 dBTP; Reels A/B −14 vs −16 before any change (doc 06 §7) |
| C3 / AD-15 | Music under explanation | [V4-MP] continuous bed | `background_music_in_core_explanation: false` | Beds only in intros, transitions, outros, Reel hook/CTA |
| C4 / AD-16 | Idle/decorative motion | [V4-MP] "never frozen" | "No decorative motion" (06 §3) | Idle motion only on illustrative characters/props |
| C5 / AD-14 | Fonts | Avoid Arial/Inter [N51] | RD-23 Inter + Noto Sans + KaTeX | Two tiers: Inter for science text; distinctive fonts for expressive text (doc 08 §4.3) |
| C6 / AD-17 | Dark sheets | [V4-MP] navy/charcoal sheets | RD-27 light theme only | Narrow exception pending founder; default light |
| C7 / AD-11 | Iteration caps | 3 fix loops per scene | ≤ 2 failed repair attempts | 3 authoring loops + ≤ 2 repairs after QA (doc 09 §7) |
| C8 / AD-23 | Bespoke code per lesson | Claude writes scene code | 09 §3: avoid "an expensive, unpredictable coding project" | Bespoke only for illustrative scenes; promote to templates |
| C9 / AD-24 | Strong model use | Opus 5.5 high for scene code | RD-04: strong model for review/escalation | Pilot A/B against Sonnet 5.5 |
| **new** | Letter-by-letter text | [V4-MP] ransom/handwriting per letter | 03 S8: avoid syllable-by-syllable karaoke text | Per-unit staging only for ≤ 6-word expressive titles; never narration, captions, labels (doc 08 §1) |
| **new** | Bed level under voice | [V4-MP] 15–20 dB; tokens file `music_under_voice_db: [15, 20]` | Playbook: 20–24 (lesson) / 18–22 (Reel) dB [Hypothesis] | Playbook values as test starting points; update the tokens file **Resolved 15 Oct 2026** (AD-15 addendum, AD-37 corrected; tokens `audio.music_policy` / `audio.loudness`; `import_clip_notes.md` §6.3). |
| **new** | Music authorship | Python-composed ([V2], [V3]) | Playbook §7.1 item 7: music and sonic logo composed by a contracted person | Python for SFX, Reel hooks, prototypes; brand bed commissioned (doc 06 §2) |
| **new** | MCP orchestration | L3 MCP use ([V2], [V3], [V4]) | RD-22: "no Kubernetes or MCP fleet early" | MCP per job only for storyboard grids and optional rasters, behind the ledger; no MCP voice |
| **new** | Per-lesson LLM cost line | Scene authoring at high effort | 08 §1 LLM cap $1.72 per lesson | New "Animation authoring" line (PA-11; doc 09 §11.2) |
| **new** | Loudness in harness files | — | `vertical_safe_zones.tokens.json` and `import_clip_notes.md` §6.3 call loudness "unresolved" | Align them with AD-04 **Resolved 15 Oct 2026** (AD-15 addendum, AD-37 corrected; tokens `audio.music_policy` / `audio.loudness`; `import_clip_notes.md` §6.3). |

---

## 9. Rollout sequence [Recommendation]

1. **P1:** build the harness contract, linter, determinism test and one style guide; port the four golden fixtures plus one illustrative scene; benchmark HyperFrames (and Remotion only after licence confirmation) by correctness → reproducibility → memory → render time → ease of repair → total cost (RD-07).
2. **P2 pilots:** one physics (the Ohm's-law I–V scene, `12_advanced_animations_with_claude/02_documentation/13_END_TO_END_WALKTHROUGH.md` §B), one chemistry, one biology lesson with animated layers; record ledger, rubric and reviewer minutes.
3. **P2b Reels:** the Class 10 P0 backlog items whose source lessons are GF-approved (`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` §3), starting with CSV ID 2 (§A of doc 13).
4. **P3:** replace provisional caps with measured values; decide on Indic kinetic text after the test card.

Plan details: `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/`.
