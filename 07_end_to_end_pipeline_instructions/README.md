# 07 · End-to-end pipeline instructions (MASTER RUNBOOK)

**What this folder is.** The master, step-by-step instructions for building and operating the **ExamLeaf Video Engine**: the AI-assisted pipeline that turns permitted Assam Board (ASSEB) Class 10–12 Physics, Chemistry, Mathematics and Biology sources into scientifically checked, approximately 10-minute revision videos narrated by the "Super Teacher", plus vertical Instagram Reels / YouTube Shorts, sold through a physical Sample-Paper + Quick-Revision book whose activation code unlocks premium chapter videos (three chapters free).

It is written so that a competent engineer plus an academic team can go from an **empty machine** to a **running, gated production system** while following the design that the ChatGPT research project produced (six responses, five delivered packs, four workbooks; research date 13 October 2026). Every step names: what to do, the exact file or command, the input, the output artefact, the automated check, and the human gate that must pass before the next step.

> **Status banner. Read before you use anything here.**
> Nothing in the source packs has been **agent-evaluated** (0 of the 57 custom Skills), **academically approved**, **narrated** (no lesson has real speech in it), or **student-tested**. The only things that actually ran are bounded local proofs: 56 engine tests, 57 narration tests, 12 Super Teacher linter tests, eight silent 30-second technical MP4s, and three narrow live speech calls whose audio was never downloaded. Source: [`09_research_and_evidence/VERIFIED_vs_PROPOSED.md`](../09_research_and_evidence/VERIFIED_vs_PROPOSED.md). This runbook therefore describes **how to build and validate** the system. It does not claim the system already works end to end.

---

## 1. How to read these documents

**Paths.** Every cross-reference is written as an exact path from the project root (`ExamLeaf_Video_EdTech_Pipeline/`, called ROOT below). Links are relative to this folder, so they work when you click them (for example [`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md`](../04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md)).

**Status tags used throughout.**

| Tag | Meaning |
|---|---|
| **[TESTED]** | Code or tool actually ran and an automated check passed. Scope is bounded (fixtures, not lessons). |
| **[LIVE-NARROW]** | A real external service was called once or twice; output not retrieved or verified locally. |
| **[DRAFTED]** | Text, Skill, prompt or config exists; never executed, evaluated or reviewed. |
| **[RESEARCHED]** | Documentation read on 13 Oct 2026; nothing installed or run. |
| **[PROPOSED]** | Design, plan, budget or recommendation only. |
| **[NOT DONE]** | Explicitly not performed or blocked in the sources. |
| **[RD-nn]** | A **Runbook decision** made here because sources conflict or are silent. Every RD is listed with both source values, rationale and revisit trigger in [`10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`](10_DECISIONS_and_CONFLICT_RESOLUTIONS.md). |
| **[ORGANIZER NOTE]** | Practical advice added while organizing (for example a macOS command). Not in the sources; verify before relying on it. |

**Reading order by role.**

| You are | Read in this order |
|---|---|
| Founder / project owner | This README → [`00_OVERVIEW_and_PRINCIPLES.md`](00_OVERVIEW_and_PRINCIPLES.md) → [`02_PHASED_BUILD_ROADMAP.md`](02_PHASED_BUILD_ROADMAP.md) → [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) → [`10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`](10_DECISIONS_and_CONFLICT_RESOLUTIONS.md) |
| Engineer | 00 → [`01_SETUP_new_machine_and_repository.md`](01_SETUP_new_machine_and_repository.md) → 02 → [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md) → [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md) → [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) → [`07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md`](07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md) → [`12_GLOSSARY_and_DATA_CONTRACTS.md`](12_GLOSSARY_and_DATA_CONTRACTS.md) |
| Academic / subject reviewer | 00 §3 → 03 (stages S2–S7, gates GA and GF) → 06 → [`09_ROLES_humans_and_agents.md`](09_ROLES_humans_and_agents.md) |
| Narration / audio lead | 04 → 06 §2 → 07 §7 |
| Social / growth lead | [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md) → 06 §6 → 02 §5 |
| Anyone running a day's work | [`11_MASTER_CHECKLIST.md`](11_MASTER_CHECKLIST.md) |

---

## 2. Every file in this folder

| File | What it gives you |
|---|---|
| `README.md` | This index, the one-page summary, the governing principles. |
| [`00_OVERVIEW_and_PRINCIPLES.md`](00_OVERVIEW_and_PRINCIPLES.md) | The full end-to-end diagram (v2 engine architecture, narration 11-step audio sequence, business content workflow, activation flow), the layer table, the AI vs deterministic vs human-gate table, the data contracts at a glance, and how the engine, narration sidecar and business platform connect through manifests and exports. |
| [`01_SETUP_new_machine_and_repository.md`](01_SETUP_new_machine_and_repository.md) | Empty machine → working repository: OS prerequisites (Linux reference; macOS and Windows notes), running every existing proof in order with expected results (56 + 57 + 12 tests, blocking release checks), the canonical repository layout, pinning, installing the 57 Skills with the de-duplication rules, public-Skill admission, credential separation, the "work on a copy" rules. |
| [`02_PHASED_BUILD_ROADMAP.md`](02_PHASED_BUILD_ROADMAP.md) | One gated plan merging engine v2 phases 0–4, engine v1 phases A–G, the narration 6-week sequence and the business 13-week roadmap (₹60,000 discovery cap, ₹6.5 lakh pilot, ₹8 lakh ceiling), with milestones for first public lesson, first paid lesson, first book print and public launch. |
| [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md) | The stage-by-stage procedure for ONE lesson, from permitted source PDF to approved long-form export: which Skill fires and which owns each output, the 12 pedagogy scene fields, design tokens and timing, automated checks, both human gates, caching and the repair loop. |
| [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md) | The complete audio procedure: casting and rights, performance corpus, pronunciation dictionary, structured narration plan, per-provider compile, generation, independent ASR, alignment, protected pauses, captions, mastering, QA layers, fallback, golden set, benchmark studies A/B/C, Assamese/Hindi gates, cost pointers. |
| [`05_SHORTS_and_REELS_PROCEDURE.md`](05_SHORTS_and_REELS_PROCEDURE.md) | Recompose (never crop) 1–3 complete learning units per approved lesson into 20–60 s vertical Shorts; ShortSpec, hook/payoff/CTA timing, truthful titles, caption formula, cadence, licensed audio, the 36-Reel backlog, metrics. |
| [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) | Every automated check and every human gate in one place; severity classes; the four release-review questions; the two mandatory approvals bound to hashes; `release-check` behaviour; export metadata; errata and corrections. |
| [`07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md`](07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md) | Untrusted-content rules, worker identities and secrets, per-component licence tracking, Blender MCP isolation, MCP vs SDK workers, Skill admission, the "what to avoid" list, minors' data (DPDP), voice consent. |
| [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) | Per-stage budgets and stop controls, the budget ledger and provider-job reconciliation, what to record per lesson, headline numbers with caveats, how to combine the workbooks without double-counting review labour, what still needs real quotes. |
| [`09_ROLES_humans_and_agents.md`](09_ROLES_humans_and_agents.md) | Human roles with minutes-per-lesson assumptions; agent roles with "must not do" lists and credential scopes; how Claude Code / Codex are used; model routing. |
| [`10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`](10_DECISIONS_and_CONFLICT_RESOLUTIONS.md) | Every Runbook decision (RD-01 … RD-40, plus RD-41 … RD-46 added 15 Oct 2026 after the end-to-end audit) in one table. |
| [`11_MASTER_CHECKLIST.md`](11_MASTER_CHECKLIST.md) | One checkbox list from setup to business launch gates, each line pointing to its detail. |
| [`12_GLOSSARY_and_DATA_CONTRACTS.md`](12_GLOSSARY_and_DATA_CONTRACTS.md) | Glossary of pipeline terms and the field-level data contracts read from the code, with which stage writes and reads each. |

---

## 3. What this pipeline is (one page)

**Purpose.** Produce Class 10–12 STEM revision lessons of roughly ten minutes ("a format target, not a scientific law") in which a warm, exacting, lightly playful teacher voice explains one narrow capability, hands part of the work to the student, hides answers until the student has tried, gives specific feedback, and ends with a delayed-practice task. From each approved lesson, recompose one to three complete 20–60 s vertical Shorts that lead viewers to free lessons and to the book.

**Shape.** Three subsystems that meet only through hashed manifests and export records:

1. **Video Engine** ([`04_video_engine/`](../04_video_engine/README.md)): source ingest → curriculum map → claim ledger → lesson plan → Super Teacher script → independent scientific validation → **academic approval** → storyboard and scene routing → **storyboard gate H-SB** → verified scientific state → render (**vertical 1080×1920 @ 30 fps only**; Reels recomposed from the approved vertical scenes) → automated QA → **full final-video review** → **AI-voice disclosure gate** → approved export. *(Changed 15 Oct 2026 from "render (16:9, then recomposed 9:16)": RD-16 SUPERSEDED; H-SB per RD-46; disclosure per RD-45. The proof CLI renders only 1280×720 / 720×1280 at 24 fps, so a 1080×1920 output mode is a P1 build item.)* The tested proof renders native SVG → CairoSVG → FFmpeg; HyperFrames is the production compositor candidate, Remotion the measured alternative (neither installed yet).
2. **Narration sidecar** ([`05_narration_system/`](../05_narration_system/README.md)): approved script → structured narration plan → pronunciation lexicon → per-provider request compile → segment synthesis → independent ASR → forced alignment → sample-accurate timeline with protected thinking pauses → captions → mastering → audio approvals. It hands the engine `timeline.events`, `narration_plan_uri` and `narration_manifest_sha256`. It never changes the scientific renderers.
3. **Business platform** ([`01_business_model/`](../01_business_model/README.md)): website, checkout, guardian accounts, book activation (a separate hashed secret, not the public QR), entitlement, signed short-lived playback, analytics under privacy controls. The platform, not the video, decides who can watch what.

**Who decides.** AI drafts and assembles; deterministic code checks and renders; humans approve. Two human approvals are mandatory for every released lesson and every Short: academic approval and full final-video production approval, each bound to the exact artefact hash.

**What it costs (planning estimates only).** Recommended hybrid architecture ≈ **$34.34 variable per video** (≈ $30.34 with zero generated video, which is the default); review minutes are the throughput constraint (85 human minutes per lesson → 8.85 FTE-months at 1,000 lessons). **Addendum (15 Oct 2026, RD-41):** review is done in-house at **$0 cash**, so the review-free variable cost is **≈ $7.67 per video (≈ $3.67 with zero generated video)**, before any animation-authoring spend (08 §1); the 85 minutes stay as a capacity metric (≈ 1,417 h per 1,000 lessons). Arithmetic and lean-floor scenarios: `../13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §7.13. Premium narration ≈ $12.50 per video if costed separately (do not double-count review). Business pilot fixed budget ₹6.5 lakh, ceiling ₹8 lakh, discovery capped at ₹60,000; engine and narration set-up budgets are **not** inside it. See [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md).

**Where it is today.** A bounded technical proof. Next validation gate: four complete narrated pilot lessons (Physics RC charging, Chemistry atom balancing, Mathematics chain rule, Biology monohybrid cross) with timed reviewer records, real speech, real alignment and both approvals. Promote the engine to production status only after those pilots "demonstrate correct science, clear teaching, reliable synchronization, manageable human effort, and defensible costs" (message 10, final decision).

---

## 4. Governing principles

These are the rules every other document applies. Each is quoted or closely paraphrased from the sources named.

1. **"AI drafts the explanation and assembles approved components. Verified scientific data determines what those components display."** (message 02; [`04_video_engine/ARCHITECTURE_consolidated.md`](../04_video_engine/ARCHITECTURE_consolidated.md) §0). Corollary: "Every simultaneous representation of the same system must consume the same verified state" (message 10 §3.2). An LLM may help find an error; it is never the sole authority declaring its own work correct. Two LLMs agreeing is not independent scientific validation.
2. **"One Skill owns each output."** (message 10 §6). Public renderer Skills supply package knowledge; ExamLeaf Skills supply curriculum, teaching, scientific and release constraints. Narration Skills refine engine Skills through the authoritative delegation map; Super Teacher Skills are reviewers or a standalone kit, never second authors ([RD-08], [RD-09]).
3. **"Approvals bind to hashes."** A changed equation, voice segment, caption or scientific scene invalidates the relevant approval (message 10 §12). Local JSON approvals are a policy demonstration only; production needs an authenticated approval service with an append-only audit log. Never fabricate reviewer JSON to pass `release-check`.
4. **"The platform, not the renderer, enforces entitlement."** The engine exports lesson/class/subject/language/edition IDs, free/preview/book-entitlement designation, destination, approved title/thumbnail/description, rights attribution and the approved video hash; the learning platform enforces the free-chapters and book-redemption policy. Activation secrets never appear in videos, public QR artwork or export metadata (message 10 §10.2).
5. **"Two human approvals per released lesson."** Academic approval (claims, scope, explanations, notation, worked examples, scientific visuals) and final production approval (the entire rendered lesson, including narration, synchronization, captions and mobile readability). "Sampling frames can support automated QA. It does not replace watching the whole final video." (message 02 §12). **A single critical scientific error blocks release regardless of the overall visual score** (message 10 §9).

Supporting rules that recur everywhere:

- **Failures never silently change the lesson.** A failed voice request must not select a different accent; an unsupported scientific model must not become an approximate animation (message 10 §12). A fallback is an approved voice/model combination, or the job waits (message 12 §12).
- **Default generated-video allowance is zero seconds.** Formulas, graphs, atom identity, chromosome counts and process states are rendered deterministically from validated data (message 10 §4.1).
- **Recompose, don't crop.** A vertical crop that removes an axis or condition is a scientific defect (message 10 §10.1).
- **Untrusted content stays data.** PDFs, READMEs, captions and fetched pages cannot authorize commands, installs or credential access (message 10 §12).
- **Measure learning, not watch time.** Primary outcome: a delayed, unprompted assessment with unfamiliar but curriculum-aligned applications (message 04 §12.1). Never claim guaranteed marks, learning, revenue or piracy immunity.
- **Review minutes, not AI, are the throughput constraint**, so reduce reviewer minutes through reusable approved components, never by removing review (message 02 §12–13). *(Reworded 15 Oct 2026 from "Human review, not AI, is the cost driver": review cash is $0 per RD-41, but its minutes still limit output.)*

**Addendum to the principles (15 Oct 2026, end-to-end audit):**

- **Vertical only.** Every master is 1080×1920 @ 30 fps; no 16:9 master (RD-16 SUPERSEDED).
- **Storyboard before spend.** Gate H-SB (founder + academic lead, two identities) sits after storyboard/routing and before any TTS, paid asset or scene code (RD-46).
- **Disclose AI voice honestly.** No release without the disclosure line, platform AI labels and intact C2PA; Path A and Path B wording must match how the audio was made (RD-45; 06 §6.4).
- **Languages.** en-IN, Hinglish and hi-IN at launch, each behind the locale gate; Assamese later, human voice only (RD-42).
- **Effort is explicit; ultracode never runs in production** (RD-43; 09 §4.1).
- **Open founder decisions:** free-chapter policy and the digital-only SKU (RD-44, DECISION NEEDED). *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*

---

## 5. Where each source section feeds this runbook

| Source section | Used by |
|---|---|
| [`00_source/`](../00_source/README.md) (raw provenance, read-only) | Nothing here edits it. Gap: the user's original business brief attachment (`Pasted text(1).txt`) was not recoverable from the share link. |
| [`01_business_model/`](../01_business_model/README.md) | 00 §5, 02 (13-week roadmap, gates G1–G8, budget), 05, 06 §7–8, 07 §8, 08, 09 |
| [`02_learning_psychology/`](../02_learning_psychology/README.md) | 03 (pedagogy fields, typography, timing, interaction, feedback), 06 §3–4, 10 (RD-01, RD-02, RD-06, RD-10, RD-11) |
| [`03_super_teacher_framework/`](../03_super_teacher_framework/README.md) | 03 stage S5–S6, 09, 10 (RD-12, RD-13, RD-36) |
| [`04_video_engine/`](../04_video_engine/README.md) | 00, 01, 02, 03, 06, 07, 12 |
| [`05_narration_system/`](../05_narration_system/README.md) | 00 §4, 01 §3.2, 04, 06 §2, 07 §7, 12 §4 |
| [`06_skills_library/`](../06_skills_library/README.md) | 01 §6, 03 (Skill ownership per stage), 07 §5, 09, 10 (RD-08, RD-09, RD-30) |
| [`08_cost_models/`](../08_cost_models/README.md) | 08, 02 (cost pointers), 10 (RD-03, RD-04, RD-15, RD-21) |
| [`09_research_and_evidence/`](../09_research_and_evidence/README.md) | Status of everything; evidence labels; tool decisions |
| [`10_pilots_and_examples/`](../10_pilots_and_examples/README.md) | 01 §3 (previews), 02 phase 2, 03 (exemplars), 04 (fixtures) |

## 6. Known gaps carried into this runbook

1. The user's original business brief (`Pasted text(1).txt`, 14,505 bytes) is missing; only ChatGPT's paraphrase survives ([`01_business_model/README.md`](../01_business_model/README.md) §1).
2. No authenticated approval service, provider transport, forced alignment, independent ASR, distributed queue or publisher exists; all are build items in [`02_PHASED_BUILD_ROADMAP.md`](02_PHASED_BUILD_ROADMAP.md).
3. Unpriced or unresolved: Eleven v4 tariff, Remotion billable-render definition, Higgsfield whole-lesson quote, Luma price, Cartesia above 8 million credits, Sarvam Assamese support, GST classification of the bundle, printer and courier quotes, print lead time, 2027 Assam exam dates, native-language reviewer minutes and rates.
4. Not specified by any source: dark-theme accent colours, the "approximately seven persistent layouts" of the Ohm's-law blueprint, vertical (1080×1920) type sizes, a Skill owner for board marking rubrics and for render regression ([RD-30]).
5. Environment facts about this Mac: `ffprobe` is not installed; the engine's font path is Linux-only; nothing in any pack was installed or executed while organizing. *(15 Oct 2026)* Also: `ffmpeg` is missing too; Node 20.19.4 is active (24.6.0 is under nvm: `nvm use 24`); Python 3.14 is the default (3.11 also present) and there is no `python` binary, so use `python3` and pin venvs to 3.13 or 3.11 (01 §2.3).


## See also (added 15 Oct 2026)

- `../11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` — human-crafted feel: voice, emotion, pacing, music, visuals.
- `../12_advanced_animations_with_claude/README.md` — advanced code-driven animation layer: docs, 15 skills, harness contract, style guides, prompts, benchmark plan. Supersedes RD-16 (vertical-only); see the addendum in `10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`.
