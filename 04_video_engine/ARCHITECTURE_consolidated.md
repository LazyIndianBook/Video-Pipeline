# ExamLeaf Video Engine — consolidated architecture (v1 plan + v2 implementation)

**Merged from:** v1 message 02 §1, §2, §6, §7 (`FULL_v1_architecture_and_plan.md`); `planning_pack_v1/QA_and_Implementation_Contract.md`; v2 message 10 §1.3, §3.1, §5, §7.3, §10, §12 (`FULL_v2_implementation_and_research.md`); `implementation_v2/docs/Architecture.md`, `docs/Production_Runbook.md`, `docs/Higgsfield_Findings.md`; and the implemented contracts in `implementation_v2/src/examleaf/`.
Quoted material is verbatim; tables are reproduced unchanged. Where v1 and v2 differ, both are shown and labelled. Organizer comments are marked *(organizer)*.

**Core principle (both versions).**
- v1: "**AI drafts the explanation and assembles approved components. Verified scientific data determines what those components display.**"
- v2: "**Python scientific validation → structured lesson and scene specifications → HyperFrames as the production compositor candidate → selective Manim/Three.js/Blender inserts → independently generated narration → measured synchronization → FFmpeg export → academic and production approval.**"
- v2: "**Every simultaneous representation of the same system must consume the same verified state.**"

---

## 1. End-to-end pipeline diagrams (verbatim)

### 1.1 v1 (message 02 §7)
```text
Permitted textbook/PDF + board/year syllabus
                    ↓
Source extraction + provenance + rights ledger
                    ↓
Topic map + prerequisites + lesson objective
                    ↓
Claim ledger + draft explanation + worked examples
                    ↓
Deterministic checks + independent scientific review
                    ↓
HUMAN ACADEMIC APPROVAL
                    ↓
Storyboard + typed SceneSpec
                    ↓
Approved components + verified scientific data
                    ↓
Narration generation + pronunciation review
                    ↓
Final-audio alignment + semantic event timing
                    ↓
Per-scene rendering + automated QA
                    ↓
FFmpeg assembly + captions + export checks
                    ↓
FULL FINAL-VIDEO REVIEW
                    ↓
Approved release + immutable manifest
```

### 1.2 v2 (message 10 §5)
```text
Permitted books/PDFs + official syllabus/version
                         ↓
Native extraction + page references + rights record
                         ↓
Source-linked claims + prerequisites + checked answers
                         ↓
Lesson plan + Super Teacher script
                         ↓
Independent scientific validation
                         ↓
ACADEMIC APPROVAL
                         ↓
Storyboard + scene classification
                         ↓
Verified scientific data + approved components
                         ↓
Narration generation + pronunciation review
                         ↓
Actual-audio alignment + semantic event timing
                         ↓
Scene rendering + captions + automated QA
                         ↓
FULL FINAL-VIDEO REVIEW
                         ↓
Approved long-form export
                         ↓
Standalone ShortSpec → vertical recomposition → review
                         ↓
Approved publishing and acquisition metadata
```

### 1.3 v2 data flow (`docs/Architecture.md`, verbatim)
"Permitted source PDF + current official syllabus → native extraction and visual flags → SourceRef/claim ledger → curriculum/prerequisite map → LessonPlan → original Super Teacher script → independent science review → storyboard and routing → validated state data + approved components → narration → actual-audio alignment → 16:9 lesson → automated QA → academic + full-video approval → release. ShortSpec selects complete teaching units and reflows them into 9:16, followed by a separate release review."

### 1.4 The stage the user asked for (v2 prompt) vs. where it lives *(organizer)*
Books/PDFs → Syllabus Extraction → Chapter Planning → Academic Research → Human-Like Script → Scientific Verification → Storyboard → Scene Classification → Best Library Selection → Animation Generation → AI Narration → Timeline Synchronization → Video Composition → Automated QA → Human Approval → Export → Instagram/YouTube Repurposing — maps 1:1 onto §1.2, with "Scene Classification + Best Library Selection" = the scene router (§8) and "Instagram/YouTube Repurposing" = ShortSpec (§10).

---

## 2. Technology layers

### 2.1 v1 layer-by-layer stack (message 02 §2, verbatim)

| Layer | Recommended implementation | Integration decision |
|---|---|---|
| Source ingestion | `pdfplumber`; Docling when layout reconstruction is useful | Preserve page references and source coordinates. Extract native text before considering OCR. |
| Curriculum/content records | Versioned JSON, source files, Git, PostgreSQL metadata | Store board, academic year, class, subject, chapter, prerequisites, and source permissions explicitly. |
| Scientific validation | Python: SymPy, NumPy/SciPy, Pint, RDKit, Biopython and approved domain-specific checks | Produce verified data before animation generation. |
| Scene composition | HyperFrames, HTML/SVG, KaTeX, seekable animation timelines | Compile typed scene specifications into approved components. |
| Specialist animation | Manim Community; selective Three.js | Render inserts or consume the same verified data as the main compositor. |
| Narration | Provider-neutral TTS adapter, pronunciation dictionary, segment cache | Keep voice generation independent of the video renderer. |
| Timing | Final audio waveform plus alignment/event metadata | Audio duration determines scene timing—not an estimated reading speed. |
| Orchestration | Prefect, Docker workers, bounded queues and retries | Keep long-running production jobs outside chat sessions. |
| Review | Small browser-based review application | Show video, script, source claims, unresolved issues, and approval controls together. |
| Export/storage | FFmpeg; filesystem initially, then object storage such as R2/S3 | Retain immutable manifests and regenerate only changed scenes. |

"**Do not use an automation canvas as a frame scheduler.** A tool such as n8n may be useful for notifications or business integrations, but the render graph should live in tested code and a durable job system."

### 2.2 v2 primary rendering decision (message 10 §3.1, verbatim)

| Technology | Recommended role | Strength for ExamLeaf | Main limitation |
|---|---|---|---|
| **HyperFrames** | Primary production compositor candidate | HTML/SVG, seekable animation, local rendering, agent-oriented workflow | Must pass the same scientific fixtures and narration tests before adoption |
| **Remotion** | Strong alternative, particularly for React teams | Programmatic React composition and reusable components | Conditional commercial licensing; avoid maintaining two compositors unnecessarily |
| **Manim Community** | Specialist mathematics/physics inserts | Equations, geometry, vectors, graphs, transformations | Additional runtime and authoring conventions |
| **Motion Canvas** | Alternative vector-animation environment | TypeScript animation designed for explanatory work | Another full animation stack if added alongside the others |
| **Three.js** | Selective browser-based 3D | Spatial relationships, geometry, molecules | Camera and geometry accuracy remain your responsibility |
| **Blender** | Reusable specialist 3D assets | Detailed spatial models and offline rendering | Higher authoring/review cost; asset and script security |
| **FFmpeg** | Required media infrastructure | Encoding, assembly, muxing, probing, audio processing | Does not verify educational or scientific correctness |
| **Native SVG/CairoSVG proof** | Reference adapter and regression fixture | Small, locally testable, model-driven | Only four bounded templates are implemented |

`docs/Architecture.md` decision: "Use HyperFrames as the primary compositor candidate, with SVG/KaTeX components driven by verified Python data. Add Manim Community for specialist mathematical inserts and Blender/Three.js only when spatial reasoning benefits. FFmpeg performs final assembly, audio processing and encoding. Remotion is the alternative when the same golden-scene benchmark shows React workflow/maturity saves more engineering cost than its licence. Do not maintain both by default. This is a recommendation based on documentation and use-case fit. The local proof tested native SVG/CairoSVG/FFmpeg, not HyperFrames or Remotion."

The v1 ranked comparison (HyperFrames 1, Remotion 2, Manim 3, Motion Canvas 4, Three.js 5, Blender 6, FFmpeg required, HeyGen avatar services "do not use as the core engine") is in `FULL_v1_architecture_and_plan.md` §1. v1: "Start with **one compositor, one scientific animation specialist, one scientific validation layer, and one audio pipeline**."

### 2.3 Do not confuse integration layers
`docs/Architecture.md` (verbatim): "Skill = instructions/resources an agent loads. MCP = protocol exposing tools/resources to an agent. API = callable service contract. SDK = client library. CLI = executable interface. Platform = hosted workflow/UI/billing. None supplies scientific verification merely by existing. A plugin can bundle multiple layers and installation hooks."

Message 10 §1.3 (verbatim):

| Surface | Actual role | Integration implication |
|---|---|---|
| **Skill** | Instructions telling an agent how to perform a workflow | Does not itself supply rendering or scientific verification |
| **CLI** | Executable interface for account, model, and generation operations | Needs installation, authentication, version pinning, and command-level controls |
| **MCP server** | Exposes provider tools to an agent | Needs approved account access, permissions, and spending controls |
| **Developer API** | Programmatic service interface | Requires confirmed endpoint access, credentials, and separate billing assumptions |
| **Web platform** | Hosted interface, workflows, plans, and credits | A web subscription does not establish unlimited API/MCP capacity |

---

## 3. AI work vs deterministic work vs human gates

### 3.1 Message 10 §5.1 (verbatim)

| Responsibility | AI-assisted task | Deterministic task | Human gate |
|---|---|---|---|
| Curriculum | Propose topic mapping and identify gaps | Preserve source/year/edition records | Approve syllabus fit and rights |
| Teaching | Draft explanation, analogy, questions | Check references and coverage | Approve explanation and answer keys |
| Science | Suggest model and tests | Symbolic, numerical, dimensional, count checks | Approve assumptions and limitations |
| Visuals | Select components and propose layout | Render exact state at frame time | Inspect scientific implications |
| Audio | Normalize terminology and delivery | Synthesize, cache, measure, align | Listen for pronunciation and clarity |
| Release | Summarize defects and draft metadata | Verify hashes, required checks, approvals | Approve the complete final lesson |

"An LLM may help discover an error. It should not be the sole authority declaring its own work correct."

### 3.2 `docs/Architecture.md` — Stage ownership (verbatim)

| Stage | AI work | Deterministic work | Required human action |
|---|---|---|---|
| Source/curriculum | Propose mapping, identify gaps | Hash, page extract, schema validation | Approve rights, edition and syllabus fit |
| Lesson/script | Scope, explain, analogy, interaction drafts | Coverage checks and referenced claim IDs | Approve scientific explanations and answer keys |
| Model/data | Suggest appropriate model | Symbolic/numerical/count/units tests | Approve assumptions and limits |
| Visuals | Select component and propose layout | Render verified state at explicit time | Inspect scientific implications and readability |
| Audio | Normalize pronunciation/delivery | Synthesis request cache and waveform alignment | Listen for terminology and natural delivery |
| QA | Summarize defects, suggest bounded fixes | Media/schema/hash/bounds/caption tests | Final complete-video review |
| Publishing | Draft titles/CTAs | Verify approved hashes/access metadata | Authorize release and disclosures |

### 3.3 The two mandatory human approvals (v1 §12, verbatim)
"**Academic approval:** claims, scope, explanations, notation, worked examples, and scientific visuals. **Final production approval:** the entire rendered lesson, including narration, synchronization, captions, and mobile readability. Sampling frames can support automated QA. It does not replace watching the whole final video." Implemented as a policy check in `pipeline.release_check()` (both roles, bound to the artifact SHA-256, production requires `full_video_watched`, different reviewer IDs) — see `INSTRUCTIONS_video_engine_setup_and_run.md` §3.6.

---

## 4. Data contracts

### 4.1 v1 renderer-independent records (message 02 §7, verbatim)
"**`LessonSpec`:** objective, prerequisites, source claims, worked problems, narration, retrieval questions, expected answers, and exam terminology.
**`SceneSpec`:** scene ID, approved component, scientific-data hash, displayed text, separate spoken text, semantic events, layout, timings, and declared simplifications.
This makes it possible to change renderers without rewriting the lesson's scientific content."

v1 scene-spec contract (`QA_and_Implementation_Contract.md`, verbatim): "Each scene records: stable ID; learning objective; claim IDs; approved component; scientific data hash; display text; separate spoken text; semantic event IDs; actual audio offsets; camera/layout tokens; declared simplifications; output hash. Math, reactions and process states come from approved data, not renderer improvisation."

### 4.2 v2 contracts (message 10 §5.2, verbatim)
- **`LessonPlan`** — board, class, language, objectives, prerequisites, sources, claims, review state.
- **`SceneSpec`** — scientific parameters, assumptions, cues, duration, subject, renderer kind.
- **`AssetManifest`** — content hash, origin, licence, attribution, and generated-asset provenance.
- **`ProviderJob`** — input hash, idempotency key, provider job identifier, estimated/actual cost, state.
- **`ShortSpec`** — source claims, retained conditions, complete payoff, duration, access destination, vertical reflow.
- **`Approval`** — reviewer role and exact artifact hash.

"The local approval model is **not an authenticated approval service**. Production must establish who can approve, bind approval to the exact artifact, and invalidate it after material changes."

### 4.3 Core records — production intent (`docs/Architecture.md`, verbatim)
"SourceRef retains URI, locator, rights status, date and claim scope. Production extends it with stored source hash, academic-year version and exact extracted coordinates.
Claim includes source IDs, assumptions and review state. A statement is not approved because an LLM marked it approved.
LessonPlan includes board, division, class, language, objectives, prerequisites and review gates.
SceneSpec separates scientific parameters, explanatory cues, visible state, voice direction and duration. Content never contains executable Python/JS.
AssetManifest records SHA-256, origin, licence, attribution and provider/model/job when generated.
ProviderJob retains input hash, idempotency key, provider job ID, state and estimated/actual cost. Unknown status triggers rejoin, not a duplicate submission.
ShortSpec keeps source claim IDs, assumptions, complete payoff, access destination and reflow strategy.
Approval binds an authenticated reviewer role to an exact artifact hash and full-watch evidence. Local JSON is only a policy prototype."

### 4.4 v1 LessonSpec/SceneSpec → v2 implemented fields *(organizer comparison)*

| v1 field (proposed) | v2 implemented where | Gap |
|---|---|---|
| LessonSpec objective, prerequisites, source claims | `LessonPlan.objective`, `.prerequisites`, `.sources`, `.claims` | — |
| LessonSpec worked problems, retrieval questions, expected answers, exam terminology, narration | not fields; only beat purposes in `*_600s_plan.json` | not implemented |
| SceneSpec scene ID, declared simplifications | `SceneSpec.id`, `.assumptions` | — |
| approved component | `SceneSpec.kind` (4 fixed kinds) | no component registry/versioning |
| scientific-data hash | covered indirectly by `cache_key` (hashes full scene + code) | no explicit per-scene data hash field |
| displayed text vs separate spoken text | `Cue.text` only (single caption text) | spoken/display separation not implemented |
| semantic events, actual audio offsets | `Cue.start_s/end_s`, `role`, `answer_visible` | no audio offsets; forced alignment not integrated |
| voice direction | `Cue.voice` (steady/curious/deliberate/light/reassuring) | — |
| layout/camera tokens | `configs/design_tokens.json` + per-aspect geometry in `visuals.py` | — |
| output hash | render manifest `sha256` | — |

Field-level schema rules for all v2 contracts: `INSTRUCTIONS_video_engine_setup_and_run.md` §5.

### 4.5 Required artefacts per lesson (v1 `QA_and_Implementation_Contract.md`, verbatim)
source-ledger.json; syllabus-map.json; claims.json; verified-model.json; lesson-spec.json; scene-spec.json; approved-script.txt; pronunciation.json; audio/*.wav; alignment.json; render-manifest.json; test-results.json; final.mp4; captions.vtt; captions.srt; transcript.txt; reviewer-approvals.json.

---

## 5. Agents, subagents and MCP

### 5.1 Separate engine development from routine production (v1 §6, verbatim)
"**Development workflow:** Claude Code/Codex help implement components, tests, schema migrations, adapters, and bounded repairs. **Production workflow:** a job runner submits structured tasks to model APIs and executes approved components. This prevents every lesson from becoming an expensive, unpredictable coding project."

### 5.2 Agent responsibilities (v1 §6, verbatim)

| Agent | Responsibility | Must not do |
|---|---|---|
| Curriculum/script agent | Scope the lesson and draft from approved sources | Invent syllabus coverage or exam marking rules |
| Independent science reviewer | Re-solve, inspect assumptions, challenge claims | Approve solely because the author sounds convincing |
| Storyboard agent | Select approved visual components and semantic events | Invent scientific geometry or process states |
| Animation engineer | Compile scenes and repair bounded implementation failures | Rewrite approved science to make a render easier |
| Audio/localization agent | Normalize pronunciation, generate/cache narration, align timing | Silently change scientific meaning |
| QA agent | Inspect test results, frames, audio, captions, and manifests | Possess unrestricted publishing authority |

"For development, use isolated worktrees and clear file ownership. Start with two to four concurrent agents rather than a large group editing the same files."

v2 (`docs/Architecture.md`, verbatim): "During development, Claude Code/Codex use isolated worktrees: architecture/component author, independent science reviewer, test/QA engineer. Do not let multiple agents concurrently modify the same renderer contract." In v2 the production roles are realised as 32 Skills (`SKILLS_INDEX_video_engine_32.md`) with "one Skill owns each output".

### 5.3 MCP integrations
v1 §6 (verbatim): "**Read-only source retrieval:** return approved textbook spans, syllabus entries, and provenance—not arbitrary search snippets. **GitHub:** issues, pull requests, test results, and review records. **Browser inspection:** the local preview/review application. **Workflow diagnostics:** job states, failures, and cost records. Prefect documents an MCP integration for read-oriented diagnostics. **Custom scientific services:** narrow operations such as 'verify derivation,' 'check reaction atom balance,' and 'render approved scene.' MCP is useful when an agent needs a controlled service interface. It is unnecessary merely to import SymPy or invoke an internal FFmpeg function."

v2 (`docs/Architecture.md`, verbatim): "MCP is useful for repository issues, approved source retrieval, constrained provider tools and local preview inspection. It is not required to import SymPy or run internal FFmpeg. Do not route every function call through an LLM." Provider MCPs considered in v2: Higgsfield MCP ("Optional supervised authoring; not queue owner"), Runway connected MCP (one speech job), Playwright MCP ("Optional authoring inspection; CI uses direct Playwright tests"), Blender MCP (isolated authoring workstation only).

### 5.4 Security boundary
v1: "Source PDFs, retrieved text, and downloaded Skills are untrusted input. They must not be able to instruct agents to reveal credentials, install packages, or bypass review. Enforce permissions in the runner, containers, and release service—not only in prompts."
v2 separation of identities: "Separate workers for research, rendering, paid provider operations, and publishing. The scriptwriter should not possess publishing credentials or unrestricted billing access." Runtime separation and the full non-negotiables list: `INSTRUCTIONS_video_engine_setup_and_run.md` §11 and §14.

---

## 6. Orchestration progression

| Stage | What owns production state | Source |
|---|---|---|
| v1 plan | Prefect, Docker workers, bounded queues and retries from the start; PostgreSQL metadata; filesystem then R2/S3 | message 02 §2 |
| v2 now (implemented) | Local `ProcessPoolExecutor` (1–4 workers) + per-render manifests; SQLite cents ledger (tests only) | `cli.py`, `budget.py` |
| v2 next | "Local jobs and SQLite → validated pilot batch → Prefect, PostgreSQL, object storage, and isolated workers." Promote "once the four narrated pilots pass." "Keep CPU rendering and paid provider jobs in separate queues. No Kubernetes requirement at launch." | message 10 §5.3; `docs/Architecture.md` |

Message 10 §5.3 (verbatim): "Use Claude Code/Codex for **engine development, component authoring, bounded repairs, and structured production tasks**. Use a durable workflow system—not an indefinitely running chat—to own production state… Do not introduce Kubernetes, multiple orchestration frameworks, or a large MCP fleet before the workload justifies them."

v1 proposed repository layout (`QA_and_Implementation_Contract.md`): apps/review/; packages/scene-schema/; packages/design-system/; packages/hyperframes-adapter/; packages/science-python/; packages/audio/; components/; lessons/; sources/; skills/; tests/golden/; workers/; infra/.
v2 actual layout (message 10 §8): README.md, AGENTS.md, CLAUDE.md, pyproject.toml, configs/, schemas/, src/examleaf/{contracts, interfaces, science, visuals, pipeline, audio, budget, cli}.py, examples/, skills/ (32), tests/, scripts/, research/, docs/, outputs/, preview.html, DELIVERY_MANIFEST.json.

---

## 7. Narration, synchronization, deterministic rendering, caching and recovery

### 7.1 Narration and synchronization
v1 §7 (verbatim): "Plan scenes before generating voice, but finalize their durations **after** the actual audio exists. Generate short segments—typically one to three sentences—not a single fragile 10-minute request."
```text
Display: I = neAv_d

Spoken:
"Current magnitude equals the number density of electrons,
multiplied by the elementary charge, cross-sectional area,
and drift-speed magnitude."
```
"Use word/event timestamps to reveal the corresponding quantities. Do not align by dividing the total audio duration equally among words."

v2 §7.3 (verbatim): "Keep separate fields for: Display equation. Spoken wording. Pronunciation guidance. Editorial delivery mode. Pedagogical silence. Visual reveal event. Editorial modes such as **STEADY, CURIOUS, DELIBERATE, LIGHT, REASSURING** are not universal TTS syntax. Generate short segments, measure the actual waveform, then align meaningful events. ElevenLabs offers a forced-alignment endpoint, but that integration is **not implemented in the supplied project**."
Implemented pieces: `audio.verify_alignment` (timestamp validator), `audio.mux_supplied_audio` (refuses >0.05 s mismatch — "Conform the timeline; do not silently stretch speech."), `UnconfiguredRemoteVoice` (fails closed). Full narration design: `05_narration_system`.

### 7.2 Deterministic rendering (v1 §7, verbatim)
"Every frame should be evaluated from an explicit time or frame index. Avoid wall-clock animation, uncontrolled randomness, network-loaded fonts, and simulations that advance differently depending on render speed. Pin dependencies, browser versions, fonts, and container images. Treat cross-platform bitwise identity as a separate engineering challenge; a fixed seed alone does not guarantee identical GPU output."
v2 implementation: `render_svg(scene, frame, aspect)` is a pure function of frame time ("Animation is a pure function of frame time"); `test_renderer_reproducible` asserts identical SVG for the same frame.

### 7.3 Caching key
- v1: "**Source claims + scientific model + component version + narration + design tokens + renderer environment.** A pronunciation correction should regenerate the affected audio and dependent scenes—not the entire subject catalogue."
- v2: "Source claims + scientific assumptions/data + component version + design tokens + narration + language + voice/model settings + renderer environment. Regenerate only affected units."
- Implemented: scene JSON + aspect + environment (Python, platform, 7 package versions, FFmpeg version, font hash) + hashes of all `src/examleaf/*.py` and `design_tokens.json` — "safe but broad invalidation; production should move to tested adapter-scoped dependency hashes" (README).

### 7.4 Failure recovery
v2 §5.4 (verbatim): "For paid jobs, persist the provider job ID immediately. A timeout or unknown status means **reconcile the existing job**, not 'submit again and hope.' The local implementation already tests a cents-based reservation ledger and idempotency behaviour. Actual provider reconciliation and distributed scheduling remain implementation work." Full retry policy and QA severity: `INSTRUCTIONS_video_engine_setup_and_run.md` §7.5–7.6. Enforced in code by `ProviderJob` (unknown state requires job ID) and `BudgetLedger` (idempotent reservations, overrun recorded then pause).

---

## 8. Scene routing and generative media
Scene router (6 rules), routing table, provider table and the "zero generated seconds by default" rule: `INSTRUCTIONS_video_engine_setup_and_run.md` §13. Integration rule: "Do not make them [generative services] responsible for equations, reaction mechanisms, chromosome counts, circuit behaviour, or other scientific assertions." (message 10)

---

## 9. Higgsfield: what to reuse and what to replace (message 10 §1.2, verbatim)

| Higgsfield capability | ExamLeaf decision |
|---|---|
| Shared style reference and brand kit | Reuse the concept for approved visual identity |
| Model discovery and generation-cost estimation | Reuse through a bounded provider adapter |
| Persistent asynchronous generation jobs | Reuse the operational pattern |
| Thumbnail exploration | Optional; place exact titles, formulas, and labels deterministically |
| General contextual illustrations | Optional, after scientific and rights review |
| Fully generated scientific diagrams | Do not use as the default |
| Fixed ten-second lesson pacing | Replace with concept- and audio-driven timing |
| Automatic narration fitting | Do not allow it to rush difficult explanations |
| Automatic production of twenty Shorts | Replace with selection of genuinely complete learning units |
| "Virality" or `brain_activity` scoring | Do not treat as a learning, neuroscience, or sales metric |

Inspected `higgsfield-video-explainer` v0.13.0 pipeline (`docs/Higgsfield_Findings.md`): research/style planning; one shared style image; roughly 20–24-word narration blocks; generate Seed audio; generate Gemini Omni Flash ten-second 720p clips; assemble through explainer_video; a ten-minute run = sixty ten-second blocks (minutes × 6); provider-side assembly, not local FFmpeg. "Verdict: Higgsfield is a useful optional media supplier and workflow reference. It should not be ExamLeaf's scientific authority or primary lesson-planning system." "No Higgsfield integration was executed."

---

## 10. Short-form (ShortSpec) and the book-linked funnel

Message 10 §10.1 (verbatim): "For each approved lesson, initially select **one to three genuinely complete Shorts**: **One misconception → one prediction → one explanatory payoff → one relevant CTA.** Do not require twenty outputs because a platform workflow advertises twenty. The `ShortSpec` retains source claims and assumptions, constrains duration to 20–60 seconds, and requires vertical reflow. A crop that removes a graph axis or condition is a scientific defect, not a cosmetic issue."
Example: **Hook:** "Which line represents greater resistance? Check the axes." **Payoff:** Compare current at the same voltage. **CTA:** "Try the free graph checkpoint." "The answer should be delivered in the Short. The CTA offers useful next practice rather than withholding essential information."

`docs/Architecture.md`: "Vertical content is re-authored/reflowed, never blindly cropped or generatively outpainted to invent scientific details." Enforced: `ShortSpec.layout_strategy` must be `reflow`; `target_seconds` 20–60; `test_vertical_not_crop`. Cost of an optional three-Short package: ~$4.32 per source lesson (v2 cost model).

---

## 11. Publishing vs access control — what the platform (not the renderer) enforces

Message 10 §10.2 (verbatim): "The engine should export: Lesson, class, subject, language, and edition identifiers. Free/preview/book-entitlement designation. Correct destination resource. Approved thumbnail/title/description. Source and rights attribution. Approved video hash. Your learning platform—not the renderer—should enforce the **first-three-free and book-redemption policy**. That prevents changing a commercial offer from requiring the scientific video to be rebuilt. Do not include activation secrets in videos, public QR artwork, or export metadata."

Message 10 §10.3: "Track qualified visits, checkpoint attempts, completion of useful practice, book activation, and retained purchases using appropriate privacy controls. Do not optimize the production agent against an opaque virality score."

Runbook step 12: "Publish only released hashes. Use first-three-free entitlement metadata outside the video; actual playback access belongs to the web/book platform. Publishing and student-data handling are not implemented in this proof." Roadmap Phase 4: "keep acquisition/entitlements separate from media production."

**Split of responsibilities *(organizer summary of the above)*:** renderer/engine = produce approved, hashed media + metadata (`ShortSpec.access_tier` free / book_entitlement / preview, `destination_resource_id`); platform = playback access, book redemption, entitlement enforcement, analytics under privacy controls; release service = authenticated approvals bound to hashes, publishing credential held outside authoring agents. Business model detail: `01_business_model`.

---

## 12. Branding, readability and multilingual design (`docs/Architecture.md`, verbatim)

"Central tokens: background #F7F9FC; text #14213D; blue #185ABD; teal #087986; amber #9A5B00; purple #6E44AA; error #B42318. These are design choices, not neuroscience-based memory colours. Use labels/shapes in addition to colour. Target 4.5:1 normal text contrast, check adjacent graph colours and actual phone rendering.
A 1920px master scaled to 360px reduces an 88px label to 16.5px. Essential text must survive that display or be split/enlarged. The technical preview's finer labels are not claimed to pass the eventual phone-readability acceptance gate.
Final production target: 1920×1080 and 1080×1920, 24 or 30fps chosen consistently, H.264/yuv420p delivery, high-quality audio master, accurate VTT/SRT. The local benchmark is only 1280×720/720×1280 at 24fps."

"Keep display notation, spoken text, translations and phoneme/pronunciation guidance separate. Original English and native-reviewed Assamese-supported variants may have different durations and line breaks. Translate meaning and exam terminology; do not merely dub the English timeline. Model language support is a hard gate verified through a real request and native review, not a generic marketing language count."

v1 visual standards (palette contrast ratios, type sizes 64–72 / 84–112 / 72–88 px, 96 px margin, 190 px caption area, timing ranges, −16 LUFS / −1 dBTP): `FULL_v1_architecture_and_plan.md` §9–§10 and `planning_pack_v1/design_tokens.json`.

---

## 13. Source handling (v1 §7, verbatim)
"Every claim should retain a source identity, page/region reference, academic-year context, and source hash. For digitally generated PDFs, extract native text first. Use OCR only where needed, and manually check recovered equations, signs, units, and diagram labels. Document extraction is not scientific interpretation. For ExamLeaf's initial market, make the board and year explicit in every lesson record. Do not assume that a familiar textbook chapter automatically matches the intended syllabus or marking scheme."
Implemented: `extract-pdf` (native text, file SHA-256, per-page `requires_visual_review`, `syllabus_mapping_status: not_performed`); `SourceRef.rights_status` ∈ owned/permission/open_reference/unconfirmed.
