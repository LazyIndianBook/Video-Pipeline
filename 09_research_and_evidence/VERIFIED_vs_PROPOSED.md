# Verified vs proposed - what was actually run, and what is still a plan

> **Section 09 - research and evidence.** The single place that answers "was this actually tested?" for the whole project. It consolidates the explicit status tables in ChatGPT's messages 06, 08, 10 and 12, the "not implemented" paragraphs of the four pack READMEs, the machine-written status files (`delivery_status.json`, `live_speech_probe.json`, `browser_smoke.json`, `release_blockers.json`, `sample_structural_check.json`, `DELIVERY_MANIFEST.json`) and the known environment limitations.
>
> **Headline (all packs agree):** no ExamLeaf lesson has been narrated, rendered at ten minutes, academically approved, teacher-reviewed or tested with students. The code that exists is a bounded, locally-tested technical proof; every public Skill, compositor, voice model and generative-video service was researched, not run. Nothing here is a production release.
>
> **15 Oct 2026:** sections 11, 12, 13 and 14 (added 14–15 Oct 2026) are covered in **Part H** at the end of this file.

## Status vocabulary used below

| Label | Meaning |
|---|---|
| **TESTED** | Code or tool was executed and an automated check passed (test counts quoted). Scope is bounded. |
| **LIVE-NARROW** | A real external service was called once or twice through a connected account; output not retrievable/locally verified. |
| **DRAFTED** | Written text/spec/config exists; never executed, evaluated or reviewed. |
| **RESEARCHED** | Documentation or repository files were read on 13 Oct 2026; nothing installed or run. |
| **PROPOSED** | A design, budget, plan or recommendation only. |
| **NOT DONE** | Explicitly stated as not performed/blocked. |

Quotation marks mean the source's own words. Cross-references: `EVIDENCE_REGISTER.md` (learning-science evidence), `TECHNOLOGY_DECISION_MATRIX.md` (per-tool detail), `PUBLIC_SKILLS_AND_INTEGRATIONS.md` (49 public rows, all "not installed or executed" except where noted).

---

## Part A - Cross-pack summary

| Capability | Status | One-line truth | Where it is detailed |
|---|---|---|---|
| Four scientific model checks (RC charging, H2/O2/H2O atom counts, d/dx of (3x+1)^2, Aa x Aa cross) | **TESTED** | Bounded to the specified models; "Checks cover the specified model only; they do not establish curriculum fit or expert approval." | Part C |
| Native SVG -> CairoSVG -> FFmpeg rendering, 16:9 and 9:16 | **TESTED** | Eight real 30-second **silent** MP4s (720 frames, 24 fps) | Part C |
| Local batch, cache, atomic output, cents-based budget ledger, release-policy demonstration | **TESTED** (local) | Not distributed; approvals are JSON objects, not an authenticated service | Part C |
| 56 unit/contract/science/media tests (Video Engine) | **TESTED** | `56 passed in 3.51s` | Part C |
| 57 local tests (Narration pack) | **TESTED** | `57 passed in 3.17s`; signal fixtures only. *15 Oct 2026: after the Indic tokenizer fix, 60 cases: 58 passed + 2 FFmpeg-environment failures on this Mac; 60 with FFmpeg (`05_narration_system/narration_system_v1/CHANGES.md`)* | Part D |
| 12 structural linter tests (Super Teacher pack) | **TESTED** | Structure only: `academic_approval: false`, `audio_timing_measured: false` | Part B |
| Live speech connection (Runway) | **LIVE-NARROW** | One 32.18-s asset (9 credits) + two Eleven v3 auditions (18 credits); none downloaded, listened to, aligned or ranked | Parts C, D, F |
| Narration imported and synchronized into any video | **NOT DONE** | "Local audio download was blocked" | Part C |
| Four complete narrated 10-minute lessons | **NOT DONE** | Four 600-second beat plans only | Part C |
| HyperFrames / Remotion / Manim / Blender execution | **RESEARCHED** | "not installed or benchmarked here" | Part C; matrix s1 |
| 32 + 15 + 10 + 40 custom Skills | **DRAFTED** | 0 agent evaluations performed | Parts B-E |
| TTS provider adapters (ElevenLabs, Cartesia, Gemini, OpenAI) | **DRAFTED** (compiled non-executing recipes) | Zero network requests; production transport, billing ledger and authentication not implemented | Part D |
| Real forced alignment / independent ASR | **NOT DONE** | Only a timestamp validator and synthetic fixtures | Part D |
| Neural TTS run locally | **NOT DONE** | `neural_tts_local: false` | Part D |
| Teacher/academic approval; native-language review; student learning study | **NOT DONE** | `academic_approval: "pending"`, `student_learning_study: "not_performed"` | Parts B-D |
| Public Skills / MCP / CLI / API (49 rows) | **RESEARCHED** | "Documentation inspected; not installed or executed" (Runway: read-only auth + speech job) | PUBLIC_SKILLS file |
| Business model workbook (9 scenarios) | **PROPOSED** (model reconciled internally) | "planning scenarios, not sales forecasts or supplier quotations" | Part E |
| Cost models (1 / 100 / 1,000 videos) | **PROPOSED** | Published tariffs as inputs; workloads, labour, render time are assumptions | Part E |

---

## Part B - Super Teacher starter pack (message 08 + pack README + `evals/`)

Message 08 intro, verbatim: *"The pack contains **ten custom Skill drafts, reusable prompts, an evidence ledger, a structured lesson file, and a script checker**. The checker passed **12 local structural tests**. The Skills have not been evaluated through Claude/Codex runs, and the sample has not been voiced, rendered, or tested with students."*

Pack README: *"This pack contains original instructional materials and ten custom Skill drafts, not an installed plugin or completed production platform. No audio or video was synthesized. Claude/Codex model evaluations and student-learning experiments have not been run. The local linter tests are structural tests only."*

| Item | Status | What exists / what does not | Evidence in this section |
|---|---|---|---|
| Personality + production guide (`Super_Teacher_Guide.md`) | **DRAFTED** | Original standard for tone, pacing, interaction; evidence boundaries in `EVIDENCE_REGISTER.md` | pack README |
| Ten Skill drafts: `examleaf-lesson-architect`, `-conversational-script`, `-analogy-auditor`, `-concept-humour`, `-interaction-designer`, `-confidence-editor`, `-voice-director`, `-language-editor`, `-science-reviewer`, `-script-evaluator` | **DRAFTED** | Portable `SKILL.md` folders with local contract references and evaluation prompts; "No Claude/Codex evaluations are run" (`test_linter.py` docstring) | msg 08 s11.1; README |
| Prompts: master authoring, conversational repair, independent review | **DRAFTED** | Never run through a model in the pack | README |
| Evidence/capability ledger `Research_Ledger.md` | **Compiled** | 29 entries; "targeted research synthesis, not a preregistered systematic review" | `EVIDENCE_REGISTER.md` Part F |
| Analogy card example (`CHEM-COEFF-SANDWICH-01`) | **DRAFTED** | `"status": "DRAFT_HUMAN_REVIEW_REQUIRED"` | `references/analogy_card.example.json` |
| Complete sample script - "Balancing Chemical Equations: Change the Count, Not the Substance" | **DRAFTED** | Original narration; "has not been voiced, rendered, or tested with students"; scientific basis is standard atom conservation (OpenStax Chemistry 2e 4.1) | msg 08 s12 |
| `examples/sample_lesson.json` | **TESTED (structure only)** | 16 planned beats over 600 seconds; "The sample's 600-second timeline is planned, not measured audio" | README |
| `tools/lint_script.py` (standard-library-only structural checker) | **TESTED** | **12 tests, OK**: active_task_needs_answer_key, boolean_time_rejected, checker_does_not_modify_lesson, duplicate_is_caught, fake_sensing_is_flagged, gap_is_caught, hold_cannot_fill_entire_beat, nonfinite_time, runtime_mismatch, sample_is_structurally_valid, stage_direction_is_not_spoken, wrong_root | `evals/local_test_report.txt` ("Ran 12 tests in 0.007s - OK") |
| Result of running the checker on the sample | **TESTED** | `{"check": "STRUCTURE_ONLY", "errors": 0, "warnings": 0, "issues": [], "academic_approval": false, "audio_timing_measured": false}` | `evals/sample_structural_check.json` |
| Academic approval | **NOT DONE** | `academic_approval: false` | JSON above |
| Audio timing | **NOT DONE** | `audio_timing_measured: false` | JSON above |
| Claude / Codex evaluations of the Skills | **NOT DONE** | "have not been run" | README |
| Student-learning experiments; pilot comparisons (msg 08 s13: formal vs conversational, humour, support reduction, delivery, language) | **NOT DONE** | Planned only: `EVIDENCE_REGISTER.md` Part H E-H10 to E-H14 | msg 08 s13 |
| Assamese / Hindi lines | **DRAFTED** | Hindi mnemonic is original/optional; Assamese prompt "drafted for native-speaker review" | msg 08 s5.5 |
| Third-party Skills, textbooks, model weights, fonts, media | **Not redistributed** | "The pack does not redistribute third-party Skills, textbooks, model weights, fonts or media assets." | README |

Authoring-contract release rule (still binding): *"Unverified sources, scientific implications, pronunciation, translations and any answer marked correct require review. Automated structure checks cannot approve science or humour. Human subject review plus full rendered-video review remain mandatory."* And: *"A passing linter does not establish correctness, accessibility or learning efficacy."*

---

## Part C - Video Engine: planning pack (msg 02) and implementation (msg 10)

### C1. Planning pack (message 02)

Message 02: *"These are planning artifacts, not an already implemented video engine."* Planning-pack README: *"This pack is a researched design and planning model. It does not contain a deployed engine, validated Skill implementations, benchmarked render timings, or auditioned narration samples. The $8,000 initial implementation budget and all staffing, token and workload volumes are illustrative assumptions, not vendor quotes."* `QA_and_Implementation_Contract.md` is headed *"production contract - proposed, not implemented"*. Cost_and_Skills ReadMe: *"No candidate renderer, voice, locale or model was benchmarked or auditioned as part of this report"*; *"40 proposed custom Skills are marked as not implemented"*; *"Token budgets, render duration, staffing rates and setup effort are assumptions requiring pilot measurements."*

| Planning-pack item | Status |
|---|---|
| Ranked technology comparison (HyperFrames first; Remotion alternative) | **PROPOSED** - "recommendations for your use case - not results of a renderer benchmark or voice audition" |
| 40-Skill custom inventory (`ExamLeaf_Skills_Inventory.csv`) | **PROPOSED** - "not claims that they already exist" |
| Cost model ($2.37 machine + $18 human = $20.37/video; 45-minute render time) | **PROPOSED** - "The 45-minute render duration is not a measured benchmark"; Fargate US East example, not Mumbai |
| Design tokens / palette / typography | **PROPOSED** - "production choices, not universal research-derived optima" |
| Release gates, negative tests, artifact contracts, repository layout | **PROPOSED** |
| Eight-pilot / 30-50-lesson roadmap | **PROPOSED** |

### C2. What was actually tested (message 10, table reproduced in full)

| Deliverable | Actual status (verbatim) |
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

Message 10: *"The previews are therefore **technical proofs, not finished ExamLeaf lessons or evidence of production readiness**."* Closing: *"It does **not** yet establish a production-grade, fully narrated, academically approved video factory. **Promote it to that status only after the four complete pilots demonstrate correct science, clear teaching, reliable synchronization, manageable human effort, and defensible costs.**"*

### C3. Video Engine README - "What is actually implemented" and "What is not implemented or approved" (nothing omitted)

**Implemented (TESTED):**
* Strict typed source/claim/scene/cue/asset/job/short/review contracts.
* Native PDF text extraction with file hashes and page references (tested on a synthetic PDF; not the full ExamLeaf books).
* Four bounded scientific model checks: RC charging, H2/O2/H2O atom balance, the derivative of (3x+1)^2, and a single-locus Aa x Aa cross.
* Frame-driven native SVG -> CairoSVG -> FFmpeg rendering, independently reflowed for 16:9 and 9:16.
* Eight real 30-second silent MP4s, captions, sampled SVG/PNG frames and hash-based manifests.
* Two-worker local batch execution, cache integrity checks, atomic output files, a cents-based budget ledger, fail-closed provider interfaces and a local release-policy demonstration.
* 56 passing unit/contract/media integration tests (`outputs/tests.txt`: `56 passed in 3.51s`).
* 32 original Skill instruction drafts with input/output contracts, steps, references, handoff templates and authored evaluation cases. "These Skills have NOT been run or evaluated in Claude/Codex."

**Not implemented or approved (verbatim):** *"The four 600-second plans are outlines, NOT complete narrated ten-minute videos. HyperFrames, Remotion, Manim and Blender were researched but not installed or run. Distributed scheduling, cloud deployment, native TTS provider adapters, forced alignment, authenticated human-review service and platform publishing remain proposed. No teacher approval or student study was performed. Canvas-bounds checks do not prove every overlap/accessibility property."*

**Live speech probe (verbatim):** *"A separate connected Runway speech call returned an audio asset (32.182857 seconds, 9 workspace credits). Its local download was blocked by the environment and it is not synchronized into the previews. This confirms one connector speech operation, not the packaged provider adapter, final voice quality, Assamese support or video generation."* (`live_speech_probe.json`: model `eleven_multilingual_v2`, voice Arjun, language en, speed 0.95, task `2cf16161-f661-430f-a80d-a70908c1b972`; `integrated_into_video: false`; `listened_and_academically_approved: false`; `packaged_provider_adapter: "not implemented"`; `signed_asset_url` omitted to avoid redistributing a temporary bearer URL.)

**Engineering boundaries (verbatim README):** *"The native renderer is a reference adapter, not a new general-purpose animation framework. The mathematics fixture deliberately rejects parameters other than its reviewed worked example. Science checks prove only specified model invariants, not universal correctness, source rights or board fit. No arbitrary expression evaluation from uploaded content is implemented. Cache keys currently hash all source files (safe but broad invalidation); production should move to tested adapter-scoped dependency hashes. Reproducibility is observed within this environment, not guaranteed byte identity across GPUs/OSes."*

**Release gate behaves as designed:** `release-check outputs/physics_rc_16x9.mp4 ...manifest.json` "MUST currently exit with a blocking result: previews lack narration and genuine academic/full-video approval. Do not bypass it by fabricating JSON reviewer identities." (`benchmark.json`: `release_status: blocked_pending_audio_and_expert_review`, `audio_status: intentionally_silent_technical_preview`.) `configs/providers.example.json`: `network_generation_enabled: false`; Higgsfield, ElevenLabs and Blender MCP all `enabled: false`; `default_renderer: native_svg_proof`; `production_compositor_candidate: hyperframes`; `publish_enabled: false`; `authenticated_review_service: not_implemented`.

**A defect the proof actually found and fixed (msg 10 s3.2):** the RC explanation referred to one time constant while the animated display had already moved past that state; synchronization was corrected and a regression test added - "A mathematically correct model alone had not prevented the misleading presentation."

### C4. The eight renders (identical across msg 10 s8.1, `Four_Pilots.md`, `Measured_Proof` sheet, `benchmark.json`)

| Fixture | Aspect | Media s | Frames | Render wall s | Resolution | Status |
|---|---|---:|---:|---:|---|---|
| biology_genetics | 16:9 | 30 | 720 | 27.425 | 1280x720 | Render passed; audio and expert release pending |
| biology_genetics | 9:16 | 30 | 720 | 27.951 | 720x1280 | same |
| chemistry_balance | 16:9 | 30 | 720 | 28.670 | 1280x720 | same |
| chemistry_balance | 9:16 | 30 | 720 | 29.375 | 720x1280 | same |
| mathematics_chain | 16:9 | 30 | 720 | 27.372 | 1280x720 | same |
| mathematics_chain | 9:16 | 30 | 720 | 27.576 | 720x1280 | same |
| physics_rc | 16:9 | 30 | 720 | 27.338 | 1280x720 | same |
| physics_rc | 9:16 | 30 | 720 | 28.102 | 720x1280 | same |

Caveats: two jobs ran concurrently ("Local wall time per job is not isolated single-worker performance"); "Source fixtures are original examples based on the cited OpenStax sections, not a completed conversion of ExamLeaf PDFs"; frames were inspected by sampling, "not teacher-approved or student-tested"; "These timings are **not** a forecast for a fully narrated ten-minute lesson, complex 3D, or a browser compositor"; the local proof had no cloud-render invoice - "**not** evidence that production rendering is free."

The four pilots (`Four_Pilots.md`): each `*_600s_plan.json` is "only a beat plan. Complete scripts, teacher-approved answers, narration and event alignment still need producing. Do not stretch a 30-second fixture to ten minutes and call it a pilot." Work time (8-16 academic/editorial hours per initial full lesson; 85 human minutes in the mature hybrid model) is "planning, not measured."

### C5. Status of the 32 custom Skill drafts (`research/custom_skills.csv`, column `status`, verbatim)

| # | Skill (`examleaf-` prefix in the repository) | Priority | Status (verbatim) |
|---|---|---|---|
| 1 | `examleaf-source-ingest` | P0 | Native-text CLI tested on synthetic PDF; textbook/syllabus ingestion not end-to-end validated |
| 2 | `examleaf-curriculum-map` | P0 | Proposed agent workflow; not model-evaluated |
| 3 | `examleaf-claim-research` | P0 | Proposed agent workflow; not model-evaluated |
| 4 | `examleaf-lesson-plan` | P0 | Proposed agent workflow; not model-evaluated |
| 5 | `examleaf-super-teacher` | P0 | Proposed agent workflow; not model-evaluated |
| 6 | `examleaf-analogy-humour` | P0 | Proposed agent workflow; not model-evaluated |
| 7 | `examleaf-interaction-design` | P0 | Proposed agent workflow; not model-evaluated |
| 8 | `examleaf-science-math` | P0 | Bounded chain-rule validator tested; not a general theorem prover |
| 9 | `examleaf-science-physics` | P0 | RC analytic/SciPy cross-check tested; broader models proposed |
| 10 | `examleaf-science-chemistry` | P0 | Bounded H2/O2/H2O count checks tested; mechanisms not implemented |
| 11 | `examleaf-science-biology` | P0 | Single-locus probability model tested; anatomy/process validators proposed |
| 12 | `examleaf-storyboard-route` | P0 | Proposed agent workflow; not model-evaluated |
| 13 | `examleaf-svg-scenes` | P0 | Implemented and tested for four bounded fixtures |
| 14 | `examleaf-manim-scenes` | P1 | Proposed agent workflow; not model-evaluated |
| 15 | `examleaf-web-composition` | P1 | Proposed agent workflow; not model-evaluated |
| 16 | `examleaf-blender-scenes` | P2 | Proposed agent workflow; not model-evaluated |
| 17 | `examleaf-molecule-scenes` | P1 | Proposed agent workflow; not model-evaluated |
| 18 | `examleaf-biology-scenes` | P1 | Proposed agent workflow; not model-evaluated |
| 19 | `examleaf-voice-direction` | P0 | Proposed agent workflow; not model-evaluated |
| 20 | `examleaf-voice-synthesis` | P0 | Packaged remote adapter unimplemented; standalone live speech probe separate |
| 21 | `examleaf-alignment-localize` | P0 | Proposed agent workflow; not model-evaluated |
| 22 | `examleaf-render-batch` | P0 | Local batch/cache/atomic output tested; distributed queue proposed |
| 23 | `examleaf-visual-qa` | P0 | Proposed agent workflow; not model-evaluated |
| 24 | `examleaf-audio-caption-qa` | P0 | Proposed agent workflow; not model-evaluated |
| 25 | `examleaf-release-review` | P0 | Local policy tests pass; identity-authenticated approval service not implemented |
| 26 | `examleaf-reel-repurpose` | P0 | Proposed agent workflow; not model-evaluated |
| 27 | `examleaf-thumbnail-package` | P1 | Proposed agent workflow; not model-evaluated |
| 28 | `examleaf-observability-cost` | P0 | Local cents ledger tested; provider reconciliation proposed |
| 29 | `examleaf-skills-security` | P0 | Proposed agent workflow; not model-evaluated |
| 30 | `examleaf-learning-evaluation` | P1 | Proposed agent workflow; not model-evaluated |
| 31 | `examleaf-asset-library` | P0 | Proposed agent workflow; not model-evaluated |
| 32 | `examleaf-selective-generation` | P1 | Proposed agent workflow; not model-evaluated |

Summary: **22 of 32** carry the status *"Proposed agent workflow; not model-evaluated"*. The other **10** name a bounded tested local component or a separately recorded probe: source-ingest (native-text CLI on a synthetic PDF), the four science validators (chain rule, RC, H2/O2/H2O counts, Aa x Aa), svg-scenes (four fixtures), render-batch (local batch/cache/atomic output), observability-cost (local cents ledger), release-review (local policy tests) and voice-synthesis (adapter unimplemented; one standalone live Runway probe). Note: the `acceptance` column of alignment-localize says a timestamp range/ordering validator was tested, although its `status` stays *Proposed*. None of the 32 was run or evaluated in Claude Code/Codex. Purpose, inputs, outputs, steps, acceptance tests and fallbacks for each: `ledgers/video_engine_implementation/research/custom_skills.csv` and section `06_skills_library`.

---

## Part D - Narration system (message 12 + README + status files)

Narration README: *"**Status: offline-tested sidecar, not a finished production speech service.**"* `DELIVERY_MANIFEST.json`: `"status": "offline-tested narration sidecar; live connector auditions separate"`, `"local_tests": "57 passed"`, `"neural_tts_local": false`, `"human_voice_approval": false`.

### D1. Message 12 "What was actually implemented and tested" (table reproduced in full)

| Item | Status (verbatim) |
|---|---|
| Structured narration contracts and provider-request compiler | Implemented locally |
| Fifteen dedicated ExamLeaf narration Skills | Written, with evaluation cases; **not agent-evaluated** |
| Forty explicit English STEM pronunciation mappings | Included; **not acoustically approved** |
| Sample-accurate timeline, protected thinking pauses, and animation markers | Implemented and tested |
| Cache invalidation, transcript comparison, signal analysis, and two-pass mastering | Implemented within the starter |
| Local tests | **57 passed** |
| Actual voice demonstrations | **Two speech auditions generated through your connected Runway account**, using 18 workspace credits |
| Local processing of those generated voices | Not completed; the audio assets were not transferred into this runtime |
| Local speech-quality or pronunciation benchmark | **Not performed** |
| Local audio fixtures | Real WAV test files, explicitly labelled **NOT SPEECH** |
| Complete production service | Not yet: authenticated synthesis transport, actual ASR/alignment execution, and authenticated approval remain to be integrated |

Msg 12: *"They differ in wording, length, and expressive instructions, so they are demonstrations - not a controlled A/B experiment."* Hence `Audition_and_Evaluation.md`: no waveform measurement, ASR/alignment, human listening or acoustic ranking is claimed; the two task IDs, the 116 -> 98 credit drop and the voice settings (Arjun, `eleven_v3`, speed 0.95, en) are recorded; signed URLs deliberately not persisted; "This package's audio WAVs are explicitly labelled signal fixtures, not generated voices. **Never play or market them as speech demonstrations.**"

### D2. README deliverables and boundaries (nothing omitted)

* TESTED/implemented locally: 15 original narration Skill drafts; 40 explicit English STEM speech mappings; Pydantic contracts and JSON schema; **four current/snapshot provider-profile recipes plus one legacy migration fixture covering four providers** (Eleven v3, Eleven v4, Cartesia 3.5 snapshot, Gemini 3.8 + legacy OpenAI fixture); deterministic sample-index timeline; protected response windows; prototype captions; waveform and two-pass loudness tooling; cache/invalidation checks; 57 passing local tests; public directory and voice/evaluation guides.
* *"Two live Eleven v3 auditions were generated through the connected Runway service. They were not transferred into this runtime, listened to or mastered here. Local signal fixtures demonstrate engineering timing only. No new voice clone was created."*
* *"The compile command sends **zero network requests**. Placeholder IDs and ENV markers are configuration templates, not credentials. Production HTTP transport, billing ledger and authentication are not implemented. Do not blindly execute request JSON."*
* The release check intentionally exits with code 2: *"It requires true speech and an authenticated approval service; local self-asserted booleans cannot approve a production lesson."* `outputs/release_blockers.json` (`release_allowed: false`): "Synthetic fixture is not speech and cannot be released"; "Missing academic_listening"; "Missing voice_rights"; "Missing native_language_review"; "Missing caption_review"; "Missing sync_review"; "Approval/audio hash mismatch"; "Audio mastering not passed"; "Authenticated approval service not implemented; local booleans are not trusted approvals".
* `LICENSING_AND_SECURITY.md`: no third-party repositories, model weights, font binaries, performer recordings, credentials or signed temporary URLs are bundled; "Never convert a local audition-only flag into fictional consent"; a Runway preset name is not a vendor voice ID; legacy OpenAI recipes are migration-inspection only.
* Environment: Python 3.13.5, Linux-6.18.44; numpy 2.3.5, scipy 1.17.0, soundfile 0.13.1, pydantic 2.13.5; *"Offline signal tests; no speech model downloaded or executed locally."* Dependency ranges "are not a fully hashed reproducible lock."
* "Next engineering steps" (not done): cast native-appropriate licensed voices and approve the corpus; implement one provider transport; import independent ASR and actual forced alignment; connect `timeline.events` to the existing renderer; complete four narrated subject pilots; only then expand the batch queue and catalogue.
* Sample-accurate timeline: 6 s = 288,000 samples at 48 kHz, inserted explicitly - not requested of the TTS engine.
* Cost summary (`cost_summary.json`, five methods): reproduced in `TECHNOLOGY_DECISION_MATRIX.md` s12b - planning assumptions, "not performer quotations or a controlled quality benchmark."

### D3. Status of the 15 narration Skills (`research/custom_skills.csv`, column `status_cost`, verbatim)

| # | Skill | Status / cost note (verbatim) |
|---|---|---|
| 1 | `super-teacher-scriptwriter` | Original authored conversation pass; no provider calls. |
| 2 | `dialogue-naturalizer` | Bounded edit pass; do not rewrite approved paragraphs unnecessarily. |
| 3 | `educational-storytelling` | No generation API; zero analogies is valid. |
| 4 | `humour-meme-director` | Small editing pass; do not rerun entire script. |
| 5 | `student-psychology-director` | One review of checkpoints, not generic motivational prose. |
| 6 | `interactive-teaching-director` | Local timing; no paid audio generated for silence. |
| 7 | `voice-acting-director` | Reuse approved voice profile; no blind synthesis of all candidates. |
| 8 | `pacing-controller` | Prefer re-timing visuals to paid resynthesis. |
| 9 | `stem-pronunciation` | Cache dictionaries by used entries; expand before synthesis. |
| 10 | `multilingual-director` | Translate text and reflow audio/visuals separately; not unconditional dubbing. |
| 11 | `tts-provider-adapter` | compiler.py implemented offline; live transport pending. |
| 12 | `speech-animation-synchronizer` | timeline.py implemented; actual aligner provider integration pending. |
| 13 | `audio-production-engineer` | Local FFmpeg mastering tested on signals, not speech audition. |
| 14 | `narration-quality-reviewer` | Local surface comparator and measurements implemented; human review mandatory. |
| 15 | `cost-regeneration-optimizer` | Local hashing/cache checks implemented; distributed paid-job ledger remains production work. |

Summary: all 15 are *authored* with positive/negative evaluation cases but **none was run through Claude/Codex**; implemented local pieces are `compiler.py` (offline), `timeline.py`, local FFmpeg mastering on signals, the local surface comparator and measurements, and local hashing/cache checks. Live transport, real aligner integration, a distributed paid-job ledger and human review remain production work.

---

## Part E - Business model and cost models: verified vs estimated

### E1. Message 06 section 10.1 "What is verified versus estimated?" (table reproduced in full)

| Input | Status (verbatim) |
|---|---|
| Razorpay standard 2% platform fee plus GST | Published provider pricing; promotional periods excluded |
| Amazon Books referral fee of 2% for prices above INR 250 through INR 500 | Published category rate; not the total selling cost |
| Cloudflare delivery at $1 per 1,000 delivered minutes | Published provider tariff |
| Printing, courier cost, CAC, sell-through, staffing and conversion rates | Planning assumptions requiring validation |
| INR 90/USD | Budget conversion assumption, not a live exchange-rate quote |
| 18% output GST on the bundle | Cautious model assumption, not a classification conclusion |

Msg 06 follow-up: "Amazon also charges other fees, and book bundles may have different category treatment. Do not interpret a low or zero referral rate as free distribution." Tax warning: *"Do not assume the entire book-plus-premium-video offer is exempt merely because it contains a printed book."* ... "Obtain written advice before finalizing prices and invoices."

### E2. Other status statements in the business pack

| Statement | Source |
|---|---|
| "These are **planning scenarios, not sales forecasts or supplier quotations**." | Msg 06 executive verdict |
| "Verified public facts are cited below. Proposed prices, printing costs, conversion rates, staffing allocations, and campaign targets are explicitly treated as assumptions." | Msg 06 intro |
| Proposed prices (INR 299 / 499 / 949; MRP INR 549) are "**proposed price tests**, not existing ExamLeaf prices"; do not present MRP as a previously charged price | Msg 06 s2.1 |
| 36 Reel concepts are "**original creative drafts, not field-tested viral formats**" | Msg 06 s7 |
| Competitor local-shelf pricing "not independently audited" | Msg 06 s3.4 |
| Exact 2026 Assam participation figures: "I did not reconcile the exact 2026 Assam participation figures to an official class-and-stream census." Ledger: "Exact 2026 participation figures were not reconciled to an official result census." | Msg 06 s3.3; ledger row Market size |
| ASER 2024: 91.4% had a home smartphone; 14.6% owned one among smartphone-capable - "different denominators ... rural - not an all-Assam personal-device census" | Msg 06 s3.2; ledger row Assam rural digital access |
| Operating targets (3-8% conversion, CAC INR 100-120, activation >= 97%, 60-75% day-seven activation, 90% sell-through) are "management targets to test, not industry benchmarks" | Msg 06 s15.1 |
| Biggest unresolved commercial inputs: "actual per-SKU printer quotes, courier/account charges, language demand, partner sell-through, and observed customer acquisition costs" | Msg 06 final recommendation |
| Workbook `Read_Me`: "Verified provider tariffs are distinguished from unquoted planning assumptions. Replace printer/courier/account inputs." / "Model QA: Nine case P&Ls independently reconciled to monthly cash-flow totals; no negative stock; formula-error scan clear." / "No legal classification opinion; no corporate/income tax or borrowing interest included. CA/counsel review required." / "Do not interpret a positive unit contribution as total profitability or use static break-even outside the modeled cost tier." | `ExamLeaf_Business_Model__Read_Me__values.csv` |
| Runbook: "a proposed operating specification, not legal advice, actual customer research, a printer quote, or a guarantee of business results"; "The book/printing/CAC/conversion/staffing forecasts are planning estimates, not quotations or audited ExamLeaf performance." | `ExamLeaf_Execution_Runbook.md` |
| DPDP: phased commencement; "Legal review of ExamLeaf status; do not assume an institutional exemption"; a phone OTP alone does not establish adulthood or satisfy parental verification | Ledger rows DPDP rules / DPDP Act; msg 06 s9.3 |
| GST bundle: "No automatic nil-rate assumption"; review notification 10/2025 and later amendments with a CA | Ledger rows GST current notification / GST bundle classification |
| Cloudflare signed tokens: "Access control reduces casual sharing; does not prevent screen recording." | Ledger row Video access control |
| Cost models (all packs): "USD before taxes"; "published tariffs are inputs; workloads, rates of regeneration, labour and setup budgets are assumptions"; "No Higgsfield whole-lesson quote is claimed"; "No benchmark claim" | Cost_and_Skills ReadMe; Video_Engine_Cost_Model Inputs; msg 10 s11 |
| A 40-Skill engineering project is **not** in the lean launch budget; a separate INR 10 lakh engineering project would cut base 50,000-sale profit from ~INR 34.07 lakh to ~INR 24.07 lakh | Msg 06 s11.5; Runbook s6 |

Business ledger rows (30) with their limits: `EVIDENCE_REGISTER.md` Part I.

---

## Part F - Known environment limitations

These explain *why* several items above are NOT DONE. They are limits of the sandbox ChatGPT ran in, not design choices.

| # | Limitation | Detail (source wording) | Consequence | Source |
|---|---|---|---|---|
| F1 | **Runway audio download blocked** | `local_audio_download: "blocked by container DNS/network; no audio file included"`. Narration: "Local transfer could not be completed" / "the audio assets were not transferred into this runtime". | The 32.18-s asset and the two 18-credit Eleven v3 auditions were never measured, aligned, listened to or ranked; narration was **not** imported or synchronized into any video; signed URLs deliberately not persisted | `live_speech_probe.json`; `Audition_and_Evaluation.md`; msg 10 "What was actually tested"; msg 12 "What was actually implemented and tested" |
| F2 | **Browser navigation blocked** | `Playwright Page.goto: net::ERR_BLOCKED_BY_ADMINISTRATOR for local HTTP preview`; `status: blocked_by_environment`; `network_policy_bypassed: false`; `passed_browser_tests: 0` | `preview.html` browser playback not validated; fallback: MP4/ffprobe integration tests passed; generated PNG contact sheets manually inspected. "The supplied browser page was not validated here because administrator policy blocked navigation." | `browser_smoke.json`; msg 10 s8.2; README |
| F3 | **Linux font path** | "The reference font path is Debian/Linux-specific. Use Linux/WSL for the supplied proof; a native macOS/Windows port must configure the equivalent DejaVu path in `visuals.py` and rerun the tests." Install FFmpeg/ffprobe, Cairo and DejaVu Sans through trusted OS channels; "Font binaries are not included." Font SHA-256 recorded: `57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e` | The Video Engine proof was only run on Linux (Python 3.13.5, Linux-6.18.44-x86_64-with-glibc2.41, FFmpeg 7.1.5-0+deb13u1); a macOS run (as on this machine) has not been tested by the source | `environment_observed.json`; README; msg 10 s8.2 |
| F4 | Dependencies not installed in the sandbox | "Dependency installation was not executed in this network-restricted environment; preinstalled versions were used and are recorded in manifests. Use a reviewed fully hashed lock/container digest before production." The `PYTHONPATH=src ...` examples are POSIX shell syntax. | Version ranges in `pyproject.toml` are not a hashed lock | README (both packs); `requirements-observed.txt` |
| F5 | Reproducibility is local | "Reproducibility is observed within this environment, not guaranteed byte identity across GPUs/OSes."; "a fixed seed alone does not guarantee identical GPU output" | No cross-platform determinism claim | README; msg 02 s7 |
| F6 | Concurrency distorts timing | Two render workers ran at once; "not isolated single-worker performance" | The 27-29 s timings are not a benchmark | `Four_Pilots.md` |
| F7 | No GPU / no neural TTS | `neural_tts_local: false`; "does not include pretrained weights"; no local inference benchmark for any open model | Self-hosted TTS costs rest on illustrative $0.80 or $1 per GPU/worker-hour | Narration manifest; msg 12 s3 |
| F8 | No generative-video capability in the connected workspace | "Current workspace has no available video models" (Runway) | Generated-video quality/cost untested; the AI-heavy cost scenario is purely arithmetic | VE directory row 16 |
| F9 | Cached documentation older than indexed pages | "Some directly opened pages were cached months earlier while current indexed official pages described newer models." (Eleven v4, Sonic 3.6, Gemini 3.8, OpenAI deprecation) | Every capability/price must be re-checked before use; keep a dated capability manifest | `Public_Narration_Directory.md` |
| F10 | Landing pages not retrievable | Luma landing page "could not be fully retrieved"; old `ahujasid/blender-mcp` path failed then the renamed repo was inspected; no authenticated Higgsfield whole-lesson quote obtained | Luma price unresolved; no Higgsfield whole-lesson quote | VE directory rows 1-4, 9, 18 |
| F11 | No user-supplied source books | Source fixtures are original examples "based on the cited OpenStax sections, not a completed conversion of ExamLeaf PDFs"; native PDF extraction tested only on a synthetic PDF | Textbook/syllabus ingestion not validated end-to-end | `Four_Pilots.md`; README |
| F12 | Local approval service is a demonstration | Approval objects are "an executable policy demonstration, not authenticated role access." | Forged JSON reviewer identities must not be used to bypass release checks | `Security_and_Installation.md`; both READMEs |

---

## Part G - Promotion gates stated by the sources (how PROPOSED becomes VERIFIED)

| Gate | Evidence required (source words) | Source |
|---|---|---|
| Four narrated pilots (physics, chemistry, mathematics, biology) | "Zero unresolved critical scientific errors; separate academic and full-video production approval"; "Four actual narrated lessons near the pedagogically appropriate duration; exact ten minutes is not mandatory"; correct pronunciation of a versioned STEM test corpus and native review per language; phone-readable diagrams/captions with learner-controlled pauses; same data drives all simultaneous representations; retry/cancel/resume, rate limits, cost caps, duplicate-job prevention tested against real staging APIs; at least one fully solved and one independent transfer item per lesson; delayed learning and confidence calibration measured separately; compositor chosen only after human-repair cost is compared | `Four_Pilots.md` |
| Compositor selection | Port the four golden fixtures to audited HyperFrames and Remotion; compare correctness, reliability, repair time, cost; at least five measured repeats; cold vs cached | Msg 10 s13 phase 1; msg 02 s14 B |
| Audio lifecycle | Native TTS estimate/submit/cache/poll/fetch, actual forced alignment, sentence-level regeneration, pronunciation dictionaries, native-language review | `Implementation_Roadmap.md` (video) phase 2 |
| Narration six-week plan | Week 1 casting and rights -> approved primary voice per locale; Week 2 one live provider transport; Week 3 independent ASR + real alignment; Week 4 renderer integration + four pilots; Weeks 5-6 controlled 20-30-lesson batch | Msg 12 s15; `Implementation_Roadmap.md` (narration) |
| Controlled batch | 20-30 lessons with measured costs and defects; durable orchestration, Postgres, object storage, secret isolation | Msg 10 s13 phase 3 |
| Voice/model admission | "A successful request plus content and listening checks can promote a recipe into a production integration" - record provider, API version, exact model ID, lifecycle dates, voice rights, voice ID, locale, permitted controls, audio format, limits, estimate/actual usage, sample hashes and reviewer approvals | `Provider_Lifecycle.md` "Admission checklist" |
| Public Skill admission | Confirm publisher -> inspect repository and scripts -> review licences and permissions -> pin a real commit/package digest -> test in isolation -> copy only approved components -> re-audit upgrades | msg 10 s2.4; `Security_and_Installation.md` |
| Business expansion | Obtain printer quotes, courier quotes, paid demand, teacher approval, print proof, legal/tax clearance; start with INR 60,000 discovery; pilot fixed budget INR 6.5 lakh; "Expansion follows evidence - not sunk costs" | Msg 06 s14; Runbook s7 |
| Learning claims | Predefined delayed unprompted assessment; ~175 learners/group for d = 0.30 (see `EVIDENCE_REGISTER.md` E-B10) | Msg 04 s12 |

---

## Part H - Sections 11, 12, 13 and 14 (added 15 Oct 2026)

Source: each section's README status block and `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` §2, §3 and §7. Same status vocabulary as above. **Headline for these four sections:** scripts are self-tested offline; nothing has been agent-evaluated; nothing has been rendered for real on this Mac; nothing has been auditioned or tested with students. The audit verdict was **PARTIALLY ALIGNED**, and the 15 Oct 2026 fix pass applies its findings in place (dated edits and addenda).

| Section / capability | Status | One-line truth | Where it is detailed |
|---|---|---|---|
| **11** Human-feel voice/audio research (report pass 1, playbook pass 2) | **RESEARCHED** | Two deep-research passes on 14 Oct 2026: 39 + 76 = 115 verified claims (20 sampled citations re-matched by the audit). Nothing auditioned, dubbed, mixed or tested with students; "contested" claims need re-checking | `11_human_feel_voice_audio_research/README.md`, `SOURCES_and_claims*.md` |
| 11 Playbook SOP, tricks catalogue, audio spec, sonic-branding plan, A/B plan | **PROPOSED** | Recommendations, labelled [Recommendation]/[Hypothesis]; corrected on 15 Oct 2026 for the audit's M9 (pause cap), Path A ASR diff, disclosure templates, Reels count, renderer default and music policy | `PLAYBOOK_human_crafted_vertical_video.md` (15 Oct 2026 addendum) |
| **12** Advanced-animation scripts (26 executable: 20 Python, 3 JS, `preflight.sh`, `reference_analysis.sh`) | **TESTED** (offline `--selftest` only) | All pass on this Mac; the template scene rendered byte-identical frames across Chrome processes. Known defect: the cue-sheet builder's output fails the harness schema (audit M7); `preflight.sh` performs fewer checks than its documentation credits (audit M11) | `12_advanced_animations_with_claude/README.md`; audit §2, M7, M11 |
| 12 Fifteen advanced-animation Skills (canonical in section 12; 57 + 15 = 72 in total) | **DRAFTED** | Complete structure, ≥7 eval cases each; **0 agent evaluations performed** | `12_.../03_skills/`; `06_skills_library/` |
| 12 Real lesson or Reel render at 1080×1920; HyperFrames vs Remotion benchmark | **NOT DONE** | This Mac fails preflight (Node 20 active, no FFmpeg/ffprobe; HyperFrames not installed). Determinism, loudness and visual quality are verified only by design and selftests | `12_.../07_benchmark_and_pilot_plan/`; audit §7 |
| 12 Docs, style guides, prompts, 18 proposed runbook amendments (PA-01…PA-18), decisions AD-01…AD-40 | **PROPOSED** | Design documents; PAs were not yet applied to 07 at audit time (audit M5) | `12_.../02_documentation/` |
| **13** Strong-to-cheap strategy, experiment protocol, templates, four architect plans, judges | **PROPOSED** | Research-plus-judge-panel output (96 of 100 verified claims survived). Cost arithmetic recomputes correctly, but nothing has been metered on ExamLeaf scenes; every token count, attempt rate and ratio is a hypothesis until week 1 of the protocol. Headline savings framing overstated (audit minors); gate order and Reels approvals contradicted 07/12 (audit M3, M4, M12) | `13_strong_to_cheap_model_strategy/README.md`; audit §3 |
| 13 Production Kit, verifiers V0–V8, cascade, fill-skills | **NOT DONE** (designed only) | No template, verifier or fill-skill has been built or run | `STRATEGY_strong_to_cheap_models.md` |
| 13 §7.13 review-at-$0 cost table (founder decision, RD-41) | **PROPOSED** (arithmetic checked by the audit) | Review cash $0; 85 min/lesson kept as capacity. Mirrored in `08_cost_models/README.md` §3.1 and `CONSOLIDATED_COST_SCENARIOS.md` E.8. Lean-floor TTS price doubles on 1 Jan 2027 | 13 §7.13; 08 addenda |
| **14** End-to-end audit | **TESTED** (static and offline checks) | Seven lenses plus adversarial refutation: ≈120 cost figures recomputed, SHA-1 match of 462 extracted files and 23 downloads, 26 selftests run, 283 links walked, secret scan, live toolchain check. Verdict **PARTIALLY ALIGNED**: 12 major and many minor findings, none critical. Release gates were read, not executed; nothing was rendered | `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` |
| 14 Fixes from the audit | **DRAFTED** (15 Oct 2026, in progress) | Applied as dated edits/addenda by section owner. Founder decisions the audit flags (free-chapter policy; digital-only SKU) remain **DECISION NEEDED** and are not made by the fix pass | each section's 15 Oct 2026 addendum |

**Promotion gates for these sections** are the same as Part G, plus: section 12 needs FFmpeg/ffprobe, Node 22+ (`nvm use 24`) and a Python 3.13 or 3.11 venv before its first real render, then one 1080×1920 lesson and one Reel through both human gates (audit §6 step 10); section 13's ratios become VERIFIED only after the week 1–4 meters replace its assumptions; section 11's recommendations become VERIFIED only after auditions, native-speaker review and the A/B plan run.
