# 00 · Overview and principles: the whole pipeline on one page set

**Purpose of this document.** Show the complete system before any step is executed: the end-to-end flow, the layers, who does what (AI, deterministic code, humans), the data contracts, and the seams where the three subsystems meet. Detailed procedures are in documents 01–09; field lists are in [`12_GLOSSARY_and_DATA_CONTRACTS.md`](12_GLOSSARY_and_DATA_CONTRACTS.md).

**Sources merged here:** [`04_video_engine/ARCHITECTURE_consolidated.md`](../04_video_engine/ARCHITECTURE_consolidated.md) (v1 + v2 diagrams, layers, contracts), [`04_video_engine/FULL_v2_implementation_and_research.md`](../04_video_engine/FULL_v2_implementation_and_research.md) §5, §10, [`04_video_engine/implementation_v2/docs/Architecture.md`](../04_video_engine/implementation_v2/docs/Architecture.md), [`05_narration_system/INSTRUCTIONS_narration_pipeline.md`](../05_narration_system/INSTRUCTIONS_narration_pipeline.md) §6, [`05_narration_system/narration_system_v1/docs/Architecture.md`](../05_narration_system/narration_system_v1/docs/Architecture.md), [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](../01_business_model/INSTRUCTIONS_business_launch_runbook.md) §6, §9, §10.

---

## 1. The integrated pipeline (runbook view)

This diagram merges the engine (left column), the narration sidecar (inserted at stage S10–S11) and the business platform (bottom). Gate names (GA, GF, GS) are used in every other document. Stage numbers (S0–S16) are the stages of [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md). The merge itself is a Runbook layout of the source diagrams, not a new design.

```text
                        ┌──────────────────────── VIDEO ENGINE (04_video_engine) ───────────────────────┐
 Permitted PDF ──► S1  Native extraction + page refs + source SHA-256 + rights record      [examleaf-source-ingest]
 + official    ──► S2  Curriculum / board-year-edition map ............ HUMAN: approve syllabus fit & rights
   syllabus          S3  Source-linked claim ledger + independently solved answer keys     [examleaf-claim-research]
                     S4  LessonPlan + 11-beat 600 s plan + assessment first                [examleaf-lesson-plan]
                     S5  Super Teacher script (spoken text separate from display/directions)
                     S6  Analogy / humour / interaction / confidence review
                     S7  Independent scientific validation (typed checks + independent re-solve)
                     ════ GA  ACADEMIC APPROVAL (script, answers, model assumptions; bound to hash) ════
                     S8  Storyboard + scene classification + routing (deterministic first; generated video = 0 s)
                     ════ H-SB  STORYBOARD GATE: grid + token/credit estimate; founder + academic lead (two identities) ════
                          (added 15 Oct 2026, PA-03 / RD-43 / RD-46: nothing paid — TTS, stills, clips, credits — and no scene code before it)
                     S9  Verified scientific state data → approved components (same-state rule)
                          │
                          │   ┌──────────── NARRATION SIDECAR (05_narration_system) ────────────┐
                     S10 ─┼──►│ narration plan → lexicon → provider compile → segment synthesis │
                          │   │ → independent ASR + critical-term review → accept/repair        │
                     S11 ◄┼───│ → forced alignment → sample-index timeline + protected pauses   │
                          │   │ → captions → mastering (−16 LUFS, ≤ −1 dBTP) → audio approvals  │
                          │   └─ hands over: timeline.events, narration_plan_uri,               │
                          │      narration_manifest_sha256, mastered WAV, VTT ──────────────────┘
                     S12 Scene rendering 9:16 1080×1920 @ 30 fps + captions (atomic, probed, hashed) [examleaf-render-batch]
                          (15 Oct 2026: vertical-only, RD-16 SUPERSEDED; the proof CLI renders only 1280×720 / 720×1280,
                           so a 1080×1920 output mode is a P1 build item)
                     S13 Automated QA: visual, science-frame, audio/caption, contrast, text size, reveal timing
                          (+ A1–A17 animated-scene checks and H-RV rubric, 06 §3.1; added 15 Oct 2026, PA-07)
                     ════ GF  FULL FINAL-VIDEO REVIEW: academic + production approvals on the exact video hash ════
                     S14 Approved long-form export + immutable manifest + export metadata
                     S15 Cache keys / S16 repair loop (only affected units; ≤ 2 repair attempts; cost cap)
                          │
                     SH  ShortSpec: 1–3 complete units → RECOMPOSED from the approved vertical scenes (never crop) → H-SB → QA
                     ════ GS  SHORT APPROVAL: same two approvals, per Short hash ════
                        └────────────────────────────────────────────────────────────────────────────────┘
                                         │ export record (IDs, access tier, destination,
                                         │ approved title/thumbnail, attribution, video hash,
                                         │ ai_voice_disclosure + performer_credit [RD-45, 15 Oct 2026])
                                         │ DISCLOSURE GATE before publish (06 §6.4)
                                         ▼  (NO activation secrets)
      ┌────────────────────────── BUSINESS PLATFORM (01_business_model) ──────────────────────────┐
      │ Website / YouTube free lessons ─ Reels/Shorts ─ checkout (Razorpay) ─ guardian account     │
      │ book: public QR = navigation only; scratch-panel secret = entitlement                      │
      │ atomic one-time redemption → subject+edition entitlement → short-lived signed video token  │
      │ analytics: qualified visits, checkpoint attempts, activations, retained sales (privacy-safe)│
      └─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The source diagrams (verbatim)

### 2.1 v2 production architecture (message 10 §5): the governing engine flow

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

The v1 diagram (message 02 §7) has the same order with "HUMAN ACADEMIC APPROVAL", "FFmpeg assembly + captions + export checks" and ends at "Approved release + immutable manifest"; it is reproduced in [`04_video_engine/ARCHITECTURE_consolidated.md`](../04_video_engine/ARCHITECTURE_consolidated.md) §1.1. The user's requested stage list (Books/PDFs → Syllabus Extraction → … → Instagram/YouTube Repurposing) maps 1:1 onto the v2 diagram ("Scene Classification + Best Library Selection" = scene router; "Repurposing" = ShortSpec), see §1.4 of the same file.

v2 data flow in one sentence (`docs/Architecture.md`): "Permitted source PDF + current official syllabus → native extraction and visual flags → SourceRef/claim ledger → curriculum/prerequisite map → LessonPlan → original Super Teacher script → independent science review → storyboard and routing → validated state data + approved components → narration → actual-audio alignment → 16:9 lesson → automated QA → academic + full-video approval → release. ShortSpec selects complete teaching units and reflows them into 9:16, followed by a separate release review."

**[15 Oct 2026]** The quoted source flow above is kept verbatim for provenance. Its "16:9 lesson" step is superseded: the lesson master is vertical 1080×1920 @ 30 fps (RD-16 SUPERSEDED in 10), and a storyboard gate H-SB now sits between storyboard/routing and narration/paid assets (RD-46).

### 2.2 Super Teacher production sequence (message 08 §11.2)

```text
Approved sources + independently checked answer key
                         ↓
Lesson architecture
                         ↓
Conversational draft
                         ↓
Analogy / humour / interaction review
                         ↓
Scientific review and repair
                         ↓
Language and voice preparation
                         ↓
Audio generation and measured synchronization
                         ↓
Rendered academic + accessibility review
                         ↓
Student testing and controlled release
```

"Use separate authoring and review roles. Two models agreeing is not, by itself, scientific validation."

### 2.3 Narration: the overall approach and the 11-step audio sequence (message 12)

Overall approach: **Approved academic explanation → conversational teaching script → performance direction → context-aware pronunciation → segmented speech generation → independent transcription and listening checks → alignment → animation timing → mastering → final approval.**

The audio sequence (message 12 §11.1, ten boxes) plus the final approval gate = 11 steps:

```text
 1  Accepted narration text
          ↓
 2  Generate coherent sentence groups
          ↓
 3  Save raw audio and provider usage
          ↓
 4  Independent ASR and critical-term review
          ↓
 5  Accept or repair the take
          ↓
 6  Forced alignment to accepted speech
          ↓
 7  Resolve semantic animation markers
          ↓
 8  Insert protected thinking/writing pauses
          ↓
 9  Compose captions and visual events
          ↓
10  Master, encode, re-measure and review
          ↓
11  Final approval: native-language, academic and full-viewing, bound to hashes
```

"Do not begin by estimating that every sentence needs eight seconds." The full production graph (`narration_system_v1/docs/Architecture.md`): approved source-linked claims → teacher draft → naturalizer/story/interaction review → academic script approval → direction and context-aware pronunciation mappings → provider request compilation → rights/model/budget admission → one synthesis job per coherent segment → persist job ID and raw audio → independent ASR → script diff and critical-word review → forced alignment against exact accepted speech → semantic visual anchors → sample-index composition with protected pauses → captions → whole-track mastering → final encode/re-measure → native/academic/full-viewing approval bound to hashes. Detailed procedure: [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md).

### 2.4 Business content workflow (message 06 §13): automate repetitive work, not academic approval

```text
Approved chapter and question IDs
        ↓
Long-form explanation
        ↓
Select one useful misconception/question
        ↓
Re-layout into vertical composition
        ↓
Generate caption and one matching CTA
        ↓
Scientific + editorial approval
        ↓
Schedule publication
        ↓
Aggregate performance by topic and destination
```

"Keep humans responsible for scientific accuracy, syllabus fit, disputed answers, misleading claims, sensitive support cases, refund exceptions, and large stock commitments." This workflow starts **after** the engine's GF gate; the "Long-form explanation" box is an approved engine export. Procedure: [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md).

### 2.5 Activation and access flow (message 06 §9.1; Execution Runbook §3)

```text
Purchase / issued physical code
            ↓
Learner or guardian account
            ↓
Consent and eligibility checks
            ↓
Atomic one-time redemption
            ↓
Subject + edition entitlement
            ↓
Short-lived authorized video token
```

Public QR = navigation only. A separate random secret (for example 128 bits in readable base32) under a scratch panel grants access; store its hash, serial, SKU, edition, print batch, status, redemption deadline and audit history; code states `generated → printed → issued → redeemed` (+ `suspended`, `revoked`, `expired`); two registered devices and one concurrent stream. Build specification: [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](../01_business_model/INSTRUCTIONS_business_launch_runbook.md) §6. [PROPOSED; nothing built.]

---

## 3. AI work vs deterministic work vs human gates

### 3.1 Responsibility table (message 10 §5.1, verbatim)

| Responsibility | AI-assisted task | Deterministic task | Human gate |
|---|---|---|---|
| Curriculum | Propose topic mapping and identify gaps | Preserve source/year/edition records | Approve syllabus fit and rights |
| Teaching | Draft explanation, analogy, questions | Check references and coverage | Approve explanation and answer keys |
| Science | Suggest model and tests | Symbolic, numerical, dimensional, count checks | Approve assumptions and limitations |
| Visuals | Select components and propose layout | Render exact state at frame time | Inspect scientific implications |
| Audio | Normalize terminology and delivery | Synthesize, cache, measure, align | Listen for pronunciation and clarity |
| Release | Summarize defects and draft metadata | Verify hashes, required checks, approvals | Approve the complete final lesson |

"An LLM may help discover an error. It should not be the sole authority declaring its own work correct."

### 3.2 Stage ownership, including narration and publishing (merged from `implementation_v2/docs/Architecture.md` and `narration_system_v1/docs/Architecture.md`)

| Stage | AI work | Deterministic work | Required human action |
|---|---|---|---|
| Source/curriculum | Propose mapping, identify gaps | Hash, page extract, schema validation | Approve rights, edition and syllabus fit |
| Lesson/script | Scope, explain, analogy, interaction drafts | Coverage checks and referenced claim IDs | Approve scientific explanations and answer keys |
| Model/data | Suggest appropriate model | Symbolic/numerical/count/units tests | Approve assumptions and limits |
| Visuals | Select component and propose layout | Render verified state at explicit time | Inspect scientific implications and readability |
| Narration text | Naturalize wording; direct delivery; draft pronunciations | Contract validation; `{{token}}` expansion; stage-tag rejection | Native-language review; academic script approval |
| Audio | Normalize pronunciation/delivery | Request compile, synthesis cache, independent ASR diff, waveform alignment, sample-index timeline, loudness measurement | Listen for terminology, critical terms and natural delivery |
| QA | Summarize defects, suggest bounded fixes | Media/schema/hash/bounds/caption tests | Final complete-video review |
| Publishing | Draft titles/CTAs | Verify approved hashes/access metadata | Authorize release and disclosures |
| Platform / commerce | None in the access path | Atomic redemption, signed tokens, webhook reconciliation | Refund exceptions, sensitive support, large stock commitments |

### 3.3 The two mandatory human approvals (message 02 §12, verbatim)

"**Academic approval:** claims, scope, explanations, notation, worked examples, and scientific visuals. **Final production approval:** the entire rendered lesson, including narration, synchronization, captions, and mobile readability. Sampling frames can support automated QA. It does not replace watching the whole final video."

How this runbook places them: the academic reviewer signs **twice**: at GA on the script/claims/answer-key hash (runbook step 4: "Unreviewed material remains preview-only") and again at GF on the final video hash (runbook step 10). The production reviewer signs at GF with `full_video_watched: true`. The two GF approvals must come from **different reviewer identities** (enforced by `release_check()`). Detail: [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) §4.

---

## 4. Layer table

| Layer | Recommended implementation | Integration decision | Status today |
|---|---|---|---|
| Source ingestion | `pdfplumber` (native text first); Docling only when layout reconstruction is useful | Preserve page references and source coordinates; OCR is an explicit reviewed exception | [TESTED] on a synthetic PDF only (`extract-pdf`) |
| Curriculum/content records | Versioned JSON, source files, Git; PostgreSQL metadata later | Board, division, academic year, class, subject, chapter, prerequisites, permissions explicit | [PROPOSED]; `LessonPlan` contract [TESTED] |
| Scientific validation | Python: SymPy, NumPy/SciPy, Pint, RDKit, Biopython, approved domain checks | Produce verified data **before** animation | 4 bounded validators [TESTED]; general validators [PROPOSED] |
| Scene composition | HyperFrames (candidate) + HTML/SVG + KaTeX; Remotion alternative | Compile typed SceneSpecs into approved components; one compositor, not two | [RESEARCHED]; native SVG → CairoSVG → FFmpeg reference adapter [TESTED] |
| Specialist animation | Manim Community; selective Three.js; Blender only when spatial value is demonstrated | Inserts consume the same verified data | [RESEARCHED] |
| Narration | Provider-neutral adapter, pronunciation lexicon, segment cache (sidecar) | Voice generation independent of the renderer | Offline compiler [TESTED]; live transport [NOT DONE] |
| Timing | Final audio waveform + alignment/event metadata (sample-index) | Audio duration determines scene timing, not an estimated reading speed | Timeline composer [TESTED] on NOT-SPEECH fixtures; real alignment [NOT DONE] |
| Orchestration | Local jobs + SQLite → validated pilot batch → Prefect, PostgreSQL, object storage, isolated workers | Keep long-running production state outside chat sessions | `ProcessPoolExecutor` batch + SQLite cents ledger [TESTED] locally |
| Review | Small browser-based review application with authenticated reviewers | Show video, script, claims, unresolved issues and approval controls together | [NOT DONE]; local `Approval` JSON is a policy demo only |
| Export/storage | FFmpeg; filesystem first, then object storage (R2/S3) | Immutable manifests; regenerate only changed scenes | Atomic outputs + manifests [TESTED] locally |
| Platform | WooCommerce, Razorpay, YouTube (free), private signed playback (e.g. Cloudflare Stream), courier workflow, permissioned WhatsApp | Entitlement outside the video | [PROPOSED] |

"Do not use an automation canvas as a frame scheduler" (n8n-type tools only for notifications/business integrations). Tool-by-tool strengths, licences and verification levels: [`09_research_and_evidence/TECHNOLOGY_DECISION_MATRIX.md`](../09_research_and_evidence/TECHNOLOGY_DECISION_MATRIX.md).

Do not confuse integration surfaces (`docs/Architecture.md`): "Skill = instructions/resources an agent loads. MCP = protocol exposing tools/resources to an agent. API = callable service contract. SDK = client library. CLI = executable interface. Platform = hosted workflow/UI/billing. None supplies scientific verification merely by existing. A plugin can bundle multiple layers and installation hooks."

---

## 5. Data contracts at a glance

Full field lists, validation rules and writer/reader stages are in [`12_GLOSSARY_and_DATA_CONTRACTS.md`](12_GLOSSARY_and_DATA_CONTRACTS.md). Status: engine contracts are pydantic models in `04_video_engine/implementation_v2/src/examleaf/contracts.py` and `interfaces.py` [TESTED as schemas]; narration contracts in `05_narration_system/narration_system_v1/src/examleaf_narration/contracts.py` [TESTED as schemas]; v1 `LessonSpec` and the 12 pedagogy fields are [PROPOSED] (not yet fields in code).

| Contract | One-line purpose | Written by stage | Read by stage |
|---|---|---|---|
| `SourceRef` | Source identity, locator, rights status, claim scope, retrieval date | S1 | S3, S4, S14 |
| `Claim` | Source-linked statement + assumptions + status (`draft` / `machine_checked` / `expert_approved`) | S3 (S7 updates status; GA sets `expert_approved`) | S4–S9, S14 |
| `LessonPlan` (v2) / `LessonSpec` (v1 proposal) | Board, year, subject, class, language, objective, prerequisites, sources, claims, target seconds, review states (+ v1: worked problems, retrieval questions, expected answers, exam terminology, narration) | S4 | S5–S14 |
| 600 s beat plan | 11 beats with purpose, task, script status | S4 | S5, S8 |
| Scene pedagogy record (12 fields) | Objective, prerequisite, relationship, attention target, representation, learner action, support, answer visibility, pause mode, feedback, misconception, delayed assessment | S4 (draft), S8 (complete) | S5–S13, GF |
| `SceneSpec` | Scientific parameters, assumptions, sources, claims, cues, duration, subject, renderer kind | S8–S9 | S12, S13 |
| `Cue` (engine) | Timed caption/role/voice/answer visibility; a question cannot show its answer | S8 (planned), S11 (measured) | S12, S13 |
| `ScienceReport` | Named checks; passes only if all pass; boundary statement | S7, S9 | GA, S12, GF |
| `NarrationPlan` (+ `VoiceIdentity`, `Segment`, `Direction`, `Pause`, `Cue`) | Canonical spoken text, delivery, pauses, cue anchors, `answers_after` | S5 (draft), S10 | S10–S11 |
| Lexicon entry | Display / spoken / caption forms per locale + review flags | S10 (N3) | Compiler, captions |
| `ProviderProfile` + compiled request | Model/voice/API version; non-executing request JSON with `audio_cache_key` | S10 (N5) | Provider worker |
| `ProviderJob` | Idempotency key, provider job ID, state, estimated/actual cents | S10, S9 (generated assets) | Ledger, reconciliation |
| `Alignment` / `AlignedWord` | Word timings bound to audio and transcript hashes; method | S11 | Timeline composer |
| Timeline (`timeline.json`) | Samples, clips, pauses, events (cue → sample → frame), captions, `contains_fixture` | S11 | S12, S13 |
| `AssetManifest` | Content hash, origin (`deterministic`/`licensed`/`generated`), licence, attribution, provider/model/job | S9, S10, S12 | S13, S14, legal |
| Render manifest | Scene, aspect, cache key, SHA-256, checks, environment, status | S12 | S13, GF, S15 |
| `Approval` | Role, reviewer ID, artifact SHA-256, approved, time, full_video_watched | GA, GF, GS (by the approval service) | `release-check`, S14 |
| `ShortSpec` | Source claims, retained conditions, payoff, 20–60 s, destination, access tier, `reflow` | SH | Platform export |
| Export record | IDs, access designation, destination, approved title/thumbnail/description, attribution, video hash | S14 | Platform |
| Activation code record | Hash of secret, serial, SKU, edition, batch, state, deadline, audit | Platform (print prep) | Platform |

---

## 6. How the three subsystems connect

The seams are deliberately narrow: each crossing is a file or record with a hash, so a change on one side invalidates exactly what depends on it.

| From | Artefact crossing the seam | To | Binding / invalidation rule | Source |
|---|---|---|---|---|
| Engine S5 (approved script) | `NarrationPlan` with claim IDs and `academic_edition` | Narration | Plan must reference approved claim IDs; academic script approval precedes synthesis | narration `docs/Architecture.md` |
| Narration | `narration_plan_uri`, `narration_manifest_sha256` added to the lesson manifest | Engine | Any audio change → new hash → dependent scenes re-timed, approvals invalidated | narration `docs/Architecture.md` "Connect to the existing engine" |
| Narration | `timeline.events` (cue, element, action, global sample, output frame), measured clip/hold intervals, captions | Engine scene adapters | "Replace estimated scene lengths with measured clip/hold intervals"; re-align after any trim | same |
| Engine | Visual-only edits | Narration | `audio_cache_key` excludes visuals and holds: no paid resynthesis for an editorial timing change | `compiler.py`, `test_cache_ignores_visual_edit` |
| Engine | Final video + render manifest (SHA-256) | Approval service | Approvals bind to that hash; any material change invalidates | message 10 §12 |
| Engine S14 | Export record (no secrets) | Business platform | Platform enforces free/preview/book-entitlement; offer changes never require re-rendering | message 10 §10.2 |
| Engine SH | `ShortSpec` (`access_tier`, `destination_resource_id`; *(15 Oct 2026) Retired from the pipeline contract under RD-49 and CE-68: the platform attaches entitlement outside the pipeline; removal from the 04 code is P1-01.*) + approved vertical video hash | Social scheduling | Only approved hashes are scheduled | message 10 §10.1; runbook step 12 |
| Business | Approved chapter and question IDs; free-chapter designations; Reel backlog IDs (CSV ID) | Engine (lesson intake) | Lesson IDs and edition IDs must match platform resource IDs and QR destinations | message 06 §13; [`01_business_model/REEL_BACKLOG_36.md`](../01_business_model/REEL_BACKLOG_36.md) |
| Business | Book QR destination URLs (public, specific: "Why this sign is negative") | Platform resource IDs | URLs must be stable before print ([RD-37] milestone M3) | message 06 §4.2 |
| All stages | `ProviderJob` + ledger reservations, reviewer minutes, render seconds | Cost ledger | Freeze generation when invoice/cost state is unresolved | `examleaf-observability-cost` failure rule |

What never crosses a seam: activation secrets (never in videos, QR artwork or export metadata), provider API keys (only inside provider workers), student identifiers (not in logs; separate services), signed temporary provider URLs (copy assets to controlled storage and hash them; never publish bearer URLs).

---

## 7. What is real today versus what you must build

| Capability | Today | Built in |
|---|---|---|
| Four bounded science models + SVG templates (RC charge, H₂/O₂/H₂O atom balance, d/dx (3x+1)², Aa×Aa) | [TESTED] | — |
| 16:9 and 9:16 rendering (native SVG proof), captions, manifests, cache, atomic outputs, budget ledger | [TESTED] locally (8 silent 30 s MP4s, 56 tests) at **1280×720 / 720×1280, 24 fps** fixtures | 1080×1920 @ 30 fps output mode: **P1 build item** (15 Oct 2026; not implemented) |
| Narration contracts, lexicon expansion, offline request compiler, timeline, signal QA, mastering | [TESTED] on NOT-SPEECH fixtures (15 Oct 2026: 60 cases; 58 passed + 2 FFmpeg-environment failures on a machine without FFmpeg; 60 with FFmpeg) | — |
| Structural script linter | [TESTED] (12 tests) | — |
| 72 custom Skills (57 original + 15 advanced-animation, canonical in section 12; count updated 15 Oct 2026) | [DRAFTED]; 0 agent evaluations | 01 §6 (evaluate before relying) |
| Production compositor (HyperFrames / Remotion) | [RESEARCHED] | Phase 1 |
| Live TTS transport, independent ASR, forced alignment | [NOT DONE] | Phase 2 / narration weeks 2–3 |
| Four complete narrated pilots | [NOT DONE] | Phase 2 / narration week 4 |
| Authenticated approval service + audit log | [NOT DONE] | Phase 2 (pulled forward, [RD-17]) |
| Durable orchestration, Postgres, object storage, secret isolation | [PROPOSED] | Phase 3 |
| Platform: checkout, activation, entitlement, signed playback | [PROPOSED] | Business weeks 5–8 |
| Learning evaluation | [NOT DONE] | After pilots (02 §6, 06 §9) |
| Storyboard gate H-SB, A1–A17 animated-scene checks, AI-voice disclosure gate | [PROPOSED] in 07 since 15 Oct 2026 (RD-43, RD-45, RD-46); A-check scripts exist in `12_advanced_animations_with_claude/` but are not agent-evaluated | Phase 1–2 |

---

## 8. Addendum (15 Oct 2026, end-to-end audit `../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`)

Decisions carried into the operating documents on this date (rows in [`10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`](10_DECISIONS_and_CONFLICT_RESOLUTIONS.md)):

- **Vertical-only (M1):** every master is 1080×1920 (9:16) @ 30 fps, H.264/yuv420p; no 16:9 master (RD-16 SUPERSEDED). The proof renderer's CLI supports only 1280×720 / 720×1280 and its fixtures run at 24 fps, so a 1080×1920 output mode is a P1 build item (02 P1).
- **Storyboard gate H-SB (M5, PA-03):** after S8, before S9/S10 and any paid generation (RD-46).
- **Animation checks (PA-07), animation-authoring cost line (PA-11), effort/ultracode rule (PA-12), checklist additions (PA-17):** RD-43; see 06 §3.1, 08 §1/§8, 09 §4.1, 11 §A/§D.
- **AI-voice disclosure (M2):** release blocker with Path A / Path B wording (RD-45; 06 §6.4).
- **Review cash $0 (M6):** review minutes are tracked as capacity, not cash (RD-41; 08 §1 addendum).
- **Launch locales (M8):** en-IN, Hinglish, hi-IN behind the locale gate; as-IN deferred, human voice only (RD-42; 04 §18).
- **DECISION NEEDED:** free-chapter policy and the digital-only SKU (RD-44). Nothing in 07 assumes an answer. *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
