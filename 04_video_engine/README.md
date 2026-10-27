# 04_video_engine — ExamLeaf Video Engine (v1 plan + v2 tested implementation)

## 1. What this section is and where it came from

This section holds everything ChatGPT produced about the **ExamLeaf Video Engine**: the AI-assisted pipeline that turns permitted textbooks into scientifically verified ~10-minute STEM revision videos (16:9) and Reels/Shorts (9:16) for Assam Board Class 10–12 Physics, Chemistry, Mathematics and Biology.

There are two generations of answer:

| | v1 — architecture + planning pack | v2 — tested implementation + research |
|---|---|---|
| User prompt | `prompts/01_USER_prompt_video_engine_research_v1.md` | `prompts/09_USER_prompt_video_engine_skills_and_implementation_v2.md` |
| ChatGPT progress notes | `prompts/01a…`, `01b…`, `01c…` | `prompts/09a…`, `09b…` |
| ChatGPT answer (cleaned full text) | `FULL_v1_architecture_and_plan.md` (message 02) | `FULL_v2_implementation_and_research.md` (message 10) |
| Downloaded deliverable | `planning_pack_v1/` (5 files, from `ExamLeaf_Video_Engine_Planning_Pack.zip`) | `implementation_v2/` (284 files, from `ExamLeaf_Video_Engine_Implementation.zip`) |
| Research/price check date stated | 13 October 2026 | 13 October 2026 |

**Provenance (untouched originals):** `00_source/chatgpt_transcript/messages/01*, 02*, 09*, 10*`; `00_source/extracted/ExamLeaf_Video_Engine_Planning_Pack/ExamLeaf_Video_Engine/`; `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/`. Everything here was copied with `cp`/`cp -R` and verified (§6). Nothing was installed or executed; the repository's code was read, not run.

## 2. Contents — every top-level item

| Item | Type | What it is |
|---|---|---|
| `README.md` | doc (organizer) | This file |
| `FULL_v1_architecture_and_plan.md` | cleaned full text | Message 02 in full: decision, ranked tech comparison, layer stack, subject libraries & safeguards, existing Skills, 40 custom Skills + Skill contract, Claude Code/Codex/subagent/MCP architecture + security boundary, pipeline diagram, LessonSpec/SceneSpec, narration/sync, deterministic rendering, caching, learning science, palette/typography/animation rules, voice shortlist, 10-minute structure, QA/risk table, cost analysis (1/100/1,000), roadmap A–G |
| `FULL_v2_implementation_and_research.md` | cleaned full text | Message 10 in full: "what was actually tested" table, Higgsfield analysis (reuse/replace, integration surfaces), public Skills directory, technology decision matrix, subject libraries, generative-media routing, architecture diagram, AI/deterministic/human table, data contracts, orchestration, caching/recovery, 32 Skills, Super Teacher in data, audio implementation, prototype contents + render benchmarks + run commands, four pilots, Shorts/funnel, three-architecture costs, security, roadmap 0–4 |
| `INSTRUCTIONS_video_engine_setup_and_run.md` | doc (organizer) | Step-by-step: prerequisites (incl. macOS font-path port), install, **every CLI command** with exit behaviour, what `batch` accepts, every `src` module, schemas, configs, caching/manifests/budget ledger, runbook, adding a template (PendingAdapter rule), HyperFrames-vs-Remotion procedure, public-Skill admission, subject-library boundaries, generative routing, security non-negotiables, roadmaps 0–4 and A–G, troubleshooting |
| `ARCHITECTURE_consolidated.md` | doc (organizer) | v1 + v2 architecture merged: both pipeline diagrams verbatim, layer tables, integration-surface table, AI-vs-deterministic-vs-human tables, all data contracts (v1 LessonSpec/SceneSpec + v2 six contracts + gap table), agent roles, MCP, orchestration progression, narration/sync, caching key, failure recovery, Higgsfield reuse/replace, ShortSpec, publishing vs access control |
| `V1_vs_V2_evolution.md` | doc (organizer) | What changed: 40 → 32 Skill mapping, compositor decision, cost-model comparison with totals, what v2 proved vs what is still open, internal inconsistencies |
| `SKILLS_INDEX_video_engine_32.md` | doc (organizer, generated from the CSV and cross-checked against every SKILL.md) | All 32 Skills: group, priority, purpose, inputs → outputs, dependencies, steps, acceptance, failure rule, cost, status, folder |
| `prompts/` | 7 copies | 01_USER, 01a, 01b, 01c, 09_USER, 09a, 09b (verbatim message files) |
| `planning_pack_v1/` | 5 files (cp -R) | v1 planning pack (below) |
| `implementation_v2/` | 284 files (cp -R) | v2 repository incl. `outputs/` (below) |

### 2.1 `planning_pack_v1/` (5 files) — "a researched design and planning model… does not contain a deployed engine"

| File | Content |
|---|---|
| `README.md` | Pack contents, recommendation (HyperFrames + SVG/KaTeX + Python validation + selective Manim + FFmpeg; Remotion alternative), scope/limitations, 13 price/capability source URLs |
| `QA_and_Implementation_Contract.md` | 7 release gates, 10 minimum negative tests, 17 required artefacts per lesson, scene-spec contract, proposed repo layout, operational boundaries — "proposed, not implemented" |
| `design_tokens.json` | Proposed canvas (1920×1080, 30 fps, 96 px margin, 190 px caption reserve), light + dark palette, type scale, timing ranges, audio target (−16 LUFS, −1 dBTP), contrast ratios |
| `ExamLeaf_Skills_Inventory.csv` | 40 proposed custom Skills (ID, name, workstream, priority, status "Proposed; not implemented", inputs, outputs, release test) |
| `ExamLeaf_Cost_and_Skills.xlsx` | Editable v1 cost model (ReadMe, Inputs, UnitCosts, Volumes, CustomSkills, ExistingSkills); CSV exports in `00_source/spreadsheets_as_csv/ExamLeaf_Cost_and_Skills__*`. See `08_cost_models` |

### 2.2 `implementation_v2/` — per-directory description (284 files)

| Path | Files | Description |
|---|---:|---|
| *(root files)* | 9 | `README.md` (what is/isn't implemented, run commands), `AGENTS.md` (agent operating rules, PendingAdapter rule), `CLAUDE.md` (Claude Code entry: copy reviewed Skills into `.claude/skills/`), `DELIVERY_MANIFEST.json` (size + SHA-256 of the other 283 files), `ExamLeaf_Video_Engine_Cost_Model.xlsx` (v2 cost model: Decision, Inputs, Per_Video, Volume_Model, Measured_Proof, Public_Directory, Skill_Backlog — see `08_cost_models`), `pyproject.toml`, `requirements-observed.txt` (observed versions, not a lock), `preview.html` (8-video review page), `.gitignore` |
| `configs/` | 2 | `design_tokens.json` (palette + DejaVu Sans used by the renderer), `providers.example.json` (Higgsfield / ElevenLabs / Blender MCP / release — all disabled) |
| `schemas/` | 5 | JSON Schemas: `scene.schema.json` (SceneSpec), `LessonPlan`, `AssetManifest`, `ProviderJob`, `ShortSpec` |
| `src/examleaf/` | 9 | `__init__`, `contracts` (SourceRef/Claim/Cue/SceneSpec/ScienceReport/Approval), `interfaces` (LessonPlan/AssetManifest/ProviderJob/ShortSpec/GeneratorAdapter/PendingAdapter), `science` (4 bounded validators), `visuals` (frame-pure SVG templates), `pipeline` (render, cache, media/layout QA, captions, release gate), `audio` (WAV inspect, alignment validator, mux, fail-closed TTS), `budget` (SQLite cents ledger), `cli` |
| `examples/` | 8 | 4 × 30-second scene specs (`physics_rc`, `chemistry_balance`, `mathematics_chain`, `biology_genetics`) + 4 × `*_600s_plan.json` 11-beat ten-minute blueprints (not scripts) |
| `skills/` | 129 | `README.md` + 32 `examleaf-*` folders × 4 files (`SKILL.md`, `references/contract.md`, `templates/handoff.json`, `evals/cases.json`) — see `SKILLS_INDEX_video_engine_32.md` |
| `tests/` | 3 | `test_engine.py` (40 tests), `test_interfaces.py` (4), `test_media_integration.py` (12) = 56 |
| `scripts/` | 2 | `build_examples.py` (regenerates examples), `preview_smoke.py` (Playwright smoke test; was blocked) |
| `research/` | 7 | `Public_Skills_Directory.md` + `public_directory.csv` (21 audited public Skills/MCP/API/platform entries), `custom_skills.csv` (32-Skill backlog), `subject_libraries.csv` (17 library/boundary rows), `sources.csv` (14 cited sources), `cost_scenarios.json` (3-architecture totals), `environment_observed.json` |
| `docs/` | 7 | `Architecture.md`, `Four_Pilots.md`, `Higgsfield_Findings.md`, `Implementation_Roadmap.md`, `Production_Runbook.md`, `Security_and_Installation.md`, `Super_Teacher_Contract.md` |
| `outputs/` | 103 | 8 silent MP4s (4 subjects × 16:9/9:16) and for each: `.manifest.json`, `.vtt`, `.ffmpeg.log` (empty), 4 stills × (`.svg` + `.png`) at opening/question/answer/recap = 96 files; plus `benchmark.json`, `tests.txt` (56 passed), `live_speech_probe.json`, `browser_smoke.json`, `delivery_status.json`, `technical_previews_contact_sheet.jpg`, `vertical_review.jpg` |

## 3. How to use this section (step by step)

1. **Understand the decision:** read `FULL_v2_implementation_and_research.md` (latest), then `V1_vs_V2_evolution.md` to see what v1 proposed and what changed.
2. **Understand the system:** `ARCHITECTURE_consolidated.md` (pipeline, contracts, gates, agents, orchestration, Shorts, access control).
3. **Look at the proof:** open `implementation_v2/outputs/technical_previews_contact_sheet.jpg` and `vertical_review.jpg`, play the MP4s, open a `*.manifest.json` to see recorded science/media/layout checks.
4. **Run it yourself (optional):** follow `INSTRUCTIONS_video_engine_setup_and_run.md` §0–§3 on a *copy* of `implementation_v2/` (Linux/WSL reference; macOS needs the font-path edit). Order: install → `validate` → `batch --workers 2` → `pytest -q` → preview server → `release-check` (must block).
5. **Plan the next work:** roadmap phases 0–4 (INSTRUCTIONS §15), compositor benchmark (§10), the four full pilots (`implementation_v2/docs/Four_Pilots.md`, `10_pilots_and_examples`).
6. **Work with the Skills:** pick from `SKILLS_INDEX_video_engine_32.md`; copy only reviewed folders into `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex); admit any public Skill only via INSTRUCTIONS §11.
7. **Costs:** v1/v2 comparison in `V1_vs_V2_evolution.md` §4; editable workbooks in `planning_pack_v1/` and `implementation_v2/` (and `08_cost_models`).

## 4. Verified vs proposed — exactly as the sources state it

### 4.1 Message 10 — "What was actually tested" (verbatim)

| Deliverable | Actual status |
|---|---|
| Four scientific models and associated visual templates | Implemented and tested |
| Landscape and vertical rendering | **Eight real 30-second MP4s**, two per subject |
| Unit, contract, scientific, and media tests | **56 tests passed** |
| Local caching, media hashes, atomic rendering, and budget ledger | Implemented and tested within the proof |
| Live speech connection | One Runway speech operation returned a **32.18-second audio asset**, consuming **9 workspace credits** |
| Narration imported and synchronized into the videos | **Not completed**; local audio download was blocked |
| Four complete narrated 10-minute lessons | **Not completed**; four full-length planning blueprints are provided |
| HyperFrames, Remotion, Manim, or Blender execution | Researched, **not installed or benchmarked here** |
| Custom Skills evaluated through Claude Code/Codex | Drafted, **not agent-evaluated** |
| Teacher approval or student learning evaluation | Not performed |
| Browser-preview automation | Attempted, but local navigation was blocked by the environment; the restriction was not bypassed |

"The previews are therefore **technical proofs, not finished ExamLeaf lessons or evidence of production readiness**."

### 4.2 `implementation_v2/README.md` (verbatim)

**What is actually implemented**
- Strict typed source/claim/scene/cue/asset/job/short/review contracts.
- Native PDF text extraction with file hashes and page references (tested on a synthetic PDF; not the full ExamLeaf books).
- Four bounded scientific model checks: RC charging, H2/O2/H2O atom balance, the derivative of (3x+1)^2, and a single-locus Aa×Aa cross.
- Frame-driven native SVG → CairoSVG → FFmpeg rendering, independently reflowed for 16:9 and 9:16.
- Eight real 30-second silent MP4s, captions, sampled SVG/PNG frames and hash-based manifests.
- Two-worker local batch execution, cache integrity checks, atomic output files, a cents-based budget ledger, fail-closed provider interfaces and a local release-policy demonstration.
- 56 passing unit/contract/media integration tests. See outputs/tests.txt.
- 32 original Skill instruction drafts with input/output contracts, steps, references, handoff templates and authored evaluation cases. These Skills have NOT been run or evaluated in Claude/Codex.

**What is not implemented or approved**
"The four 600-second plans are outlines, NOT complete narrated ten-minute videos. HyperFrames, Remotion, Manim and Blender were researched but not installed or run. Distributed scheduling, cloud deployment, native TTS provider adapters, forced alignment, authenticated human-review service and platform publishing remain proposed. No teacher approval or student study was performed. Canvas-bounds checks do not prove every overlap/accessibility property."
"A separate connected Runway speech call returned an audio asset (32.182857 seconds, 9 workspace credits). Its local download was blocked by the environment and it is not synchronized into the previews. This confirms one connector speech operation, not the packaged provider adapter, final voice quality, Assamese support or video generation."
"Browser preview automation was attempted but local HTTP navigation was blocked by administrator policy. That limitation was not bypassed."

### 4.3 `implementation_v2/outputs/delivery_status.json` (values)
unit_contract_media_tests_passed **56**; browser_smoke **blocked_by_administrator_policy**; rendered_outputs **8**; subject_fixtures **4**; seconds_per_output **30**; full_600s_narrated_lessons_completed **0**; custom_skill_drafts **32**; agent_skill_evaluations_performed **0**; public_directory_entries **21**; external_video_generation_jobs **0**; external_speech_jobs_completed **1**; runway_credits_debited **9**; voice_output_provider_duration_seconds **32.182857**; voice_import_and_alignment **not_validated**; academic_approval **pending**; student_learning_study **not_performed**.

### 4.4 v1 status statements (verbatim)
- Message 02: "Tool rankings are recommendations for your use case—not results of a renderer benchmark or voice audition performed here. Rendering time, staffing, and development costs are explicitly identified as planning assumptions." "These are planning artifacts, not an already implemented video engine." The 40 Skills "are **proposed Skills**, not claims that they already exist." Voice engines "are candidates for audition". "**The 45-minute render duration is not a measured benchmark**."
- `planning_pack_v1/README.md`: "This pack is a researched design and planning model. It does not contain a deployed engine, validated Skill implementations, benchmarked render timings, or auditioned narration samples. The $8,000 initial implementation budget and all staffing, token and workload volumes are illustrative assumptions, not vendor quotes. Academic and final-video review remain mandatory."

## 5. Separately downloaded copies — comparison with the zip contents

`00_source/downloads/ExamLeaf_Engine_Implementation/` (downloaded individually from message 10's links) was compared byte-for-byte with `cmp` against the zip-extracted repository:

| Downloaded file | Bytes | Zip copy | Result |
|---|---:|---|---|
| `README.md` | 5,907 | `implementation_v2/README.md` | **identical** |
| `research/Public_Skills_Directory.md` | 15,701 | `implementation_v2/research/Public_Skills_Directory.md` | **identical** |
| `research/custom_skills.csv` | 18,147 | `implementation_v2/research/custom_skills.csv` | **identical** |
| `outputs/physics_rc_16x9.mp4` | 347,653 | same path | **identical** |
| `outputs/chemistry_balance_16x9.mp4` | 212,515 | same path | **identical** |
| `outputs/mathematics_chain_16x9.mp4` | 225,773 | same path | **identical** |
| `outputs/biology_genetics_16x9.mp4` | 203,333 | same path | **identical** |
| `outputs/technical_previews_contact_sheet.jpg` | 105,919 | same path | **identical** |
| `outputs/vertical_review.jpg` | 63,830 | same path | **identical** |

Also identical: `00_source/downloads/ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx` = `planning_pack_v1/ExamLeaf_Cost_and_Skills.xlsx`; `00_source/downloads/ExamLeaf_Video_Engine_Cost_Model.xlsx` = `implementation_v2/ExamLeaf_Video_Engine_Cost_Model.xlsx`. Because all are identical, the downloaded duplicates were not copied again.

## 6. Verification performed while organizing
- File counts: `prompts/` 7, `planning_pack_v1/` 5, `implementation_v2/` 284 (9 root + configs 2 + schemas 5 + src 9 + examples 8 + skills 129 + tests 3 + scripts 2 + research 7 + docs 7 + outputs 103).
- `diff -r` between each copy and its `00_source/extracted/` original: no differences.
- Every file in `implementation_v2/` re-hashed against `DELIVERY_MANIFEST.json`: 283/283 SHA-256 match.
- Cleaned full-text files diffed against the raw messages: the only changes are removal of 29 (v1) / 30 (v2) opaque citation markers, LaTeX delimiter conversion, and sandbox-link re-pointing (each file's header and appendix list these).
- All 32 SKILL.md files checked field-by-field against `research/custom_skills.csv`.

## 7. Cross-references to other sections
- `01_business_model` — the book-linked "3 free chapters → premium via physical book" funnel that `ShortSpec.access_tier` and the export metadata support (v2 §10).
- `02_learning_psychology` — evidence base behind v1 §8 (retrieval, spacing, segmentation, worked examples, signalling) and the Super Teacher contract.
- `03_super_teacher_framework` — the persona encoded in `implementation_v2/docs/Super_Teacher_Contract.md` and Skill `examleaf-super-teacher`.
- `05_narration_system` — narration/voice pipeline (message 12) that completes the "audio lifecycle" left unfinished here (TTS adapter, pronunciation, forced alignment).
- `06_skills_library` — project-wide Skills catalogue; this section's 32 Skills and 40-Skill v1 backlog.
- `07_end_to_end_pipeline_instructions` — whole-project pipeline instructions.
- `08_cost_models` — the two cost workbooks (`ExamLeaf_Cost_and_Skills.xlsx`, `ExamLeaf_Video_Engine_Cost_Model.xlsx`) and their CSV exports.
- `09_research_and_evidence` — public Skills directory, sources lists.
- `10_pilots_and_examples` — the four pilots (RC charging, equation balancing, chain rule, monohybrid cross), 600 s plans and rendered previews.

## 8. Known gaps and discrepancies (see `V1_vs_V2_evolution.md` §8)
- Progress note 09b mentions "24-second" tests and "55 tests"; the delivered result is 30-second MP4s and 56 tests.
- v1 and v2 quote different LLM model generations and tariffs, and different ElevenLabs rates, for the same check date.
- v1 proposed eight pilots; v2 four.
- The v2 implementation's cache and still-frame logic, rdkit requirement and Linux font path have practical consequences documented in `INSTRUCTIONS_video_engine_setup_and_run.md` §0, §1, §9, §16.
