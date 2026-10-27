# 02 · Phased build roadmap: one gated plan for engine, narration and business

**Purpose.** Merge the four roadmaps the sources produced into one plan with explicit ordering and gates:

| Source roadmap | Where it is | Units |
|---|---|---|
| Engine v2 phases 0–4 | [`04_video_engine/implementation_v2/docs/Implementation_Roadmap.md`](../04_video_engine/implementation_v2/docs/Implementation_Roadmap.md); message 10 §13 | phases with day/week estimates |
| Engine v1 phases A–G | [`04_video_engine/FULL_v1_architecture_and_plan.md`](../04_video_engine/FULL_v1_architecture_and_plan.md) §14 | phases with gates |
| Narration 6-week sequence | [`05_narration_system/narration_system_v1/docs/Implementation_Roadmap.md`](../05_narration_system/narration_system_v1/docs/Implementation_Roadmap.md); message 12 §15 | weeks 1–6 |
| Business 90-day / 13-week launch | [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](../01_business_model/INSTRUCTIONS_business_launch_runbook.md) §2, §11 | weeks 1–13, gates G1–G8, budget |

**Status.** All four are [PROPOSED]. Engine: "Planning schedule assumes dedicated engineering and available subject reviewers. It is not a committed calendar or evidence that the full system can be delivered without further work." Narration: "Assumes dedicated engineering time and available subject/language reviewers, not an unattended guarantee." Business: "a proposed operating specification, not legal advice, actual customer research, a printer quote, or a guarantee of business results." The merged calendar in §4 is a **Runbook decision [RD-37]**: the earliest feasible sequencing of the sources' estimates, not a promise.

**Overriding rule:** "Four full pilots require a separate, explicit reviewer schedule and **no publishing deadline should bypass it**" ([`10_pilots_and_examples/pilots/Four_Pilots.md`](../10_pilots_and_examples/pilots/Four_Pilots.md)). If an engine gate slips, the business calendar slips with it.

---

## 1. How the four roadmaps correspond

| Unified phase | Engine v2 | Engine v1 | Narration | Business weeks |
|---|---|---|---|---|
| PS · Setup | (not a phase) | (not a phase) | (not a phase) | before / during W1 |
| P0 · Contracts and academic scope | 0 (3–5 working days) | A · Scientific and design contracts | prerequisite for week 1 ("Approve the academic/spoken source pipeline") | W1–W3 (interviews, syllabus map, lock titles + medium) |
| P1 · Compositor selection + core components | 1 (1–2 weeks) | B · Renderer benchmark; start of C · Core reusable library | weeks 1–2 (casting; one live transport) | W2–W4 (prototypes; reusable visuals) |
| P2 · Audio lifecycle + four full pilots | 2 (2–3 weeks) | D · Eight pilot lessons (re-scoped, [RD-05]) | weeks 3–4 (independent ASR + real alignment; renderer integration + four pilots) | W4–W6 (free lessons, checkout build) |
| P2b · Class 10 launch wave (six free lessons) | (inside 2–3) | remainder of D ("one lesson per subject strand and class level") | week 4 onward | W6 (six free chapters) |
| P3 · Controlled batch | 3 (2–3 weeks) | E · Controlled batch (~30–50) | weeks 5–6 (20–30-lesson batch, queue, dashboard) | W7–W8 (paid catalogue promised at launch) |
| P4 · Scalable production | 4 (incremental) | F · Bulk production (+ rest of C) | "Expand catalogue when the cost and quality distribution — not just the best demo — are acceptable" | after W13 decision |
| PG · Continuous evaluation | (gate of 4: "evidence of independent learning") | G · Continuous evaluation | study C (learning evaluation) | W10–W13 learning feedback; day-90 review |

Correspondence notes: v1 C (core reusable library) is folded into v2 phases 1 and 4; v1 D (eight lessons) became v2 phase 2 (four lessons) — this runbook keeps both by splitting D into the four engine pilots plus the Class 10 launch wave [RD-05]; v1 E (30–50 lessons) became v2 phase 3 (20–30) — this runbook runs 20–30 first [RD-14]; v1 G is carried by `examleaf-learning-evaluation` and the pilot acceptance gates. Source: [`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md`](../04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md) §15.

---

## 2. Phase cards

Each card: build items, owner role (roles defined in [`09_ROLES_humans_and_agents.md`](09_ROLES_humans_and_agents.md)), inputs, outputs, exit gate, effort and cost pointers.

### PS · Setup

| Field | Content |
|---|---|
| Build | Everything in [`01_SETUP_new_machine_and_repository.md`](01_SETUP_new_machine_and_repository.md) |
| Owner | Engineer |
| Inputs | Empty machine; ROOT sections |
| Outputs | Canonical repository tagged `setup-baseline`; setup log; lock files; worker identities |
| Exit gate | **S-GATE** (01 §10): 56 + 57 + 12 tests pass on your machine; both release checks block; no credentials held by authoring identities |
| Effort / cost | Not estimated by the sources. No provider spend |

### P0 · Contracts and academic scope (v2 phase 0 ≈ v1 A)

| Field | Content |
|---|---|
| Build | (1) **Assign an academic owner per subject** (Physics, Chemistry, Mathematics, Biology). (2) Obtain syllabus and rights evidence: current ASSEB division (Division I formerly SEBA; Division II formerly AHSEC), academic year, class, medium, edition; source/rights ledger for every permitted PDF. (3) Review the scaffold and **reject unsupported assumptions** (v2 roadmap). (4) Freeze contracts: extend `LessonPlan`/`SceneSpec` with the v1 `LessonSpec` fields (worked problems, retrieval questions, expected answers, exam terminology), the 12 scene-pedagogy fields, display-vs-spoken separation [RD-29], `focused` voice mode [RD-12]; define the approval record schema the approval service will issue. (5) Pin dependencies and **design tokens**: resolve typography [RD-01], holds [RD-02], master format [RD-16], vertical readability [RD-18], fonts [RD-23], light theme only [RD-27]. (6) Write the v1 minimum negative tests as fixtures (√x² = \|x\|; division by a possibly-zero quantity; equation change must match narration and graph axes/units; electron motion vs conventional current; atom/charge balance ≠ feasibility; bond interpolation must not present a transition state as stable; chromosome count, ploidy, 5′/3′ per state; symbols readable at smallest viewing size; untrusted source text cannot instruct agents; upgraded versions cannot pass because an earlier version passed). (7) Select one voice audition corpus (feeds narration week 1). (8) Decide the launch locale with the business medium decision [RD-26] *(15 Oct 2026: decided by RD-42: en-IN, Hinglish and hi-IN, each behind the locale gate; as-IN deferred, human voice only)* |
| Owner | Academic lead + per-subject academic owners; engineer; founder |
| Inputs | Permitted PDFs; official syllabus; business W1–W3 interview results |
| Outputs | `sources/` ledger with hashes and rights; `ledgers/` started; versioned contracts and schemas; production `design_tokens.json`; negative-test fixtures in `tests/golden/`; written "definition of a correct lesson" signed by the academic owners |
| Exit gate | v2: "**Academic owners agree on the definition of correctness**" (everyone agrees on source/claim/scene/approval meaning). v1 A: "Reviewers agree on what constitutes a correct lesson" |
| Effort / cost | 3–5 working days (v2 estimate). Business discovery spend capped at ₹60,000 until G1 passes |

### P1 · Compositor selection and core components (v2 phase 1 ≈ v1 B + start of C)

| Field | Content |
|---|---|
| Build | (1) Admit HyperFrames (Node 22+, FFmpeg, pinned `hyperframes` package; disable its on-demand workflow auto-install) and optionally Remotion (confirm licence eligibility first) in **isolated** environments via the admission process ([`07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md`](07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md) §4). (2) Port the **same four golden fixtures** (RC charging, atom balance, chain rule, monohybrid cross) **without rewriting the science models**; both engines consume the same verified state. (3) Benchmark per the protocol: identical approved scenes, 16:9 + 9:16 *(15 Oct 2026: 9:16 scored, 16:9 an unscored smoke test; see (7))*, same fonts/content/audio/frame count, same hardware and concurrency; warm-up then **≥ 5 measured repeats**; cold and cached builds separately; peak RSS, CPU/GPU, wall time, file size, repairs, visual differences, plus academic defects, reviewer/editing minutes and total cost. (4) **Select one** compositor; "Do not maintain both by default" [RD-07]. (5) Add reusable components: equation steps, coordinate graphs, vectors, circuits, molecular diagrams, biological process states, worked-example layouts. (6) Fix the native reference adapter's known limits: still-frame export at fixed 2/13/22/28 s (scenes < 28 s + 1 frame fail) [RD-34]; one renderer kind per subject [RD-35]. (7) *(added 15 Oct 2026; vertical-only, RD-16 SUPERSEDED)* Add a **1080×1920 @ 30 fps output mode** to the proof renderer: today `--aspect` accepts only 16:9 (default) or 9:16 and the sizes are hard-coded to 1280×720 / 720×1280 (`pipeline.py`, `visuals.py`), with fixtures at 24 fps. Score the benchmark on 9:16 only; any 16:9 run is an unscored smoke test. (8) *(added 16 Oct 2026, pilot gap L-09)* **Vendor the fonts**: ship every style guide's licensed display and text faces as local `@font-face` files next to the harness (licence and SHA-256 recorded, RD-23), and the Noto Indic families; until then the system stack is the pilot fallback and frames are not comparable across machines (`12_advanced_animations_with_claude/05_style_guides/README.md` §12) |
| Owner | Engineer (component author); independent science reviewer agent; test/QA engineer; academic owners inspect components |
| Inputs | P0 contracts and tokens; four golden fixtures `engine/examples/*.json` |
| Outputs | Benchmark report (`10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md` §6 recording grid); `components/` v1 with negative tests; `ledgers/skill_activations.md` entries for admitted public Skills |
| Exit gate | v2: "**Same correct scientific states across layouts and repeated builds**"; choose "using correctness, reliability, repair time, and cost". Metric order (v1): **correctness → reproducibility → memory → render time → ease of repair → total operating cost**. "Choose the compositor only after cost including human repair is compared. No overall quality score may hide a critical scientific error." If neither engine passes the golden fixtures: **stop and escalate**; do not start P2 on an unvalidated compositor [RD-07] |
| Effort / cost | 1–2 weeks (estimate). Part of the illustrative set-up budget ($10,000 hybrid, message 10; v1 $8,000 = 240 eng + 60 academic-template + 20 design/voice hours × $25). Remotion, if selected: $0.01/billable render, $100/month minimum when the paid licence applies; billable-render definition unconfirmed |

Parallel narration work during P1: **Week 1** casting and reference contracts (12 connected passages + 40 written term entries; audition 3 suitable voices per needed language on identical content at normalized playback level; establish actual voice rights and model IDs; teachers/native reviewers reject meaning-changing pronunciations regardless of acting preference) → gate "Approved primary voice per required locale". **Week 2** one live provider transport (Eleven v4 or Gemini 3.8 after account access is confirmed; synthesis kept out of the agent's direct shell; persist request/response format, provider ID and billed usage; per-run spending limits, concurrency limits, timeout reconciliation, HTTP error classes, no blind paid retries; never the deprecated OpenAI fixture) → gate "Successful controlled synthesis and failure tests". Procedure: [`04_NARRATION_SUBPIPELINE.md`](04_NARRATION_SUBPIPELINE.md).

### P2 · Audio lifecycle and four complete pilots (v2 phase 2 ≈ v1 D, re-scoped)

| Field | Content |
|---|---|
| Build | (1) Native TTS lifecycle in the provider worker: **estimate / submit / cache / poll / fetch**, idempotency keys, ledger reservation. (2) **Actual forced alignment** and **independent ASR** (narration week 3): verbatim ASR settings where supported; reject unavailable language resources rather than inventing word timing; verify alignment against a manually annotated sample; separate transcript-normalization tests for English, Hindi, Assamese; manually listen to critical terms and numbers; test omitted words, repeated phrases, code-switching, planned pauses. (3) Sentence-level (segment) regeneration. (4) Pronunciation dictionaries + native-language review. (5) Connect `timeline.events` to the selected compositor's scene adapters; add `narration_plan_uri` and `narration_manifest_sha256` to the lesson manifest; let natural narration determine scene duration (narration week 4). (6) **Minimum authenticated approval service** (reviewer identity, role, artefact SHA-256, full-watch evidence, append-only audit log, invalidation on change), pulled forward from phase 3 so that no lesson is ever released on local JSON [RD-17]. (7) Write and approve **full scripts and exercises** and produce the **four complete pilots** with timed reviewer records, through every stage of [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md) |
| The four pilots (message 10 §9) | **Physics**: interpret a changing circuit model (RC charging) and its graph; conditions, units, numerical/display agreement; approve actual Assam syllabus relevance before publishing. **Chemistry**: balance a fresh equation and explain coefficient vs subscript; no changed chemical identity; no implication that balance proves feasibility. **Mathematics**: apply the chain rule to a new nested expression; domains, visible reasoning, independent method selection. **Biology**: explain a monohybrid cross and distinguish probability from guaranteed counts; genotype/phenotype; explicit assumptions; no small-family guarantee. Plans: `10_pilots_and_examples/pilots/*_600s_plan.json` (`blueprint_only`; every beat `requires_authoring_and_review`). "Do not stretch the technical clips to ten minutes." |
| Owner | Academic owner per subject (author oversight + GA + GF academic); production QA reviewer (GF production); narration lead; audio editor; native-language editor if localized; engineer |
| Inputs | P1 compositor + components; narration weeks 1–2 outputs; approved voice; lexicon |
| Outputs | Four pilot lesson folders with all artefacts; the per-pilot record sheet ([`10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md`](../10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md) §5.1): academic defects by severity, reviewer minutes, editing minutes, pronunciation repairs, render time cold/cached, peak memory, accepted-asset generation attempts, total cost, fresh-question performance (immediate and delayed), calibration counts, approvals with hashes |
| Exit gate (Four_Pilots acceptance gates, verbatim) | Zero unresolved critical scientific errors; separate academic and full-video production approval. Four actual narrated lessons near the pedagogically appropriate duration; exact ten minutes is not mandatory. Correct pronunciation of a versioned STEM test corpus and native review per language. Diagram, equations, captions and text readable on representative small phones, with genuine learner-controlled practice pauses. Same data drives simultaneous representations; parameter changes invalidate dependent assets. Retry/cancel/resume, rate limits, cost caps, expiring assets and duplicate-job prevention tested against real staging APIs. At least one original fully solved and one independent transfer item per lesson. Measure delayed learning and confidence calibration separately from retention/watch time. Choose the compositor only after cost including human repair is compared. No overall quality score may hide a critical scientific error. Narration week 4 gate: "Full academic/native-language/listening approval" |
| Effort / cost | 2–3 weeks (estimate). "Budget **8–16 academic/editorial hours per initial full lesson** plus shared component engineering … The mature cost model assumes 85 hybrid human minutes per video; that is not a promise for first-time bespoke lessons." Narration set-up reserve $4,000 (separate). Premium narration ≈ $12.50 variable/lesson (narration-only view) |

**Promotion rule (message 10 final decision):** "Promote it to [production] status only after the four complete pilots demonstrate correct science, clear teaching, reliable synchronization, manageable human effort, and defensible costs."

### P2b · Class 10 launch wave (remainder of v1 D) [RD-05]

| Field | Content |
|---|---|
| Build | The **six free lessons** the business plan needs (three carefully selected free chapters × two Class 10 titles: General Science and General Mathematics), produced with pilot-grade rigour (timed records, both approvals). Together with the four engine pilots this satisfies v1's "one lesson per subject strand and class level". The Chemistry pilot may count as a General Science free lesson only if the academic lead maps it to the current Class 10 syllabus |
| Owner | Academic lead (selection "by diagnostic value", business W3), per-subject owners, production QA |
| Inputs | Business W3 decisions (two titles, one medium, first three free chapters per title by diagnostic value: one foundational, one commonly difficult, one representative later chapter [RD-20]; *15 Oct 2026: **DECISION NEEDED (RD-44)** — "first three chapters" vs "three selected chapters"; RD-20 stands until the founder decides*); candidate topics from the Class 10 P0 concepts in [`01_business_model/REEL_BACKLOG_36.md`](../01_business_model/REEL_BACKLOG_36.md) and the Ohm's-law blueprint [`02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md`](../02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md) | *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
| Outputs | Six released free lessons (hash-bound approvals); 1–3 Shorts each (stage SH) |
| Exit gate | Each lesson passes GF; business W6 gate "Usability and academic review pass" (low-cost-phone test, partner specimens) |
| Effort / cost | Same per-lesson budget as P2 pilots (8–16 h each) until measured reductions appear |

### P3 · Controlled batch (v2 phase 3 ≈ v1 E; narration weeks 5–6)

| Field | Content |
|---|---|
| Build | Durable orchestration (local jobs + SQLite → **Prefect, PostgreSQL, staged object storage, isolated workers**) [RD-22]; secret isolation; retry / cancel / resume; real provider failure injection in staging; reviewer workflow on the approval service; CPU rendering and paid provider jobs in **separate queues**; dashboard and queue only "around validated contracts"; independent vertical Shorts and reviewed title/CTA metadata; trial **20–30 lessons** first [RD-14] (the business pilot funds 40 reviewed chapter videos; complete the remainder only after the batch gate) |
| Owner | Engineer; academic owners; production QA; narration lead; founder (budget) |
| Inputs | P2 gate passed; launch catalogue list (business W3, W8) |
| Outputs | 20–30 released lessons; measured accepted-audio cost, retake fraction, human minutes, synchronization defects, failure/repair/cost per lesson |
| Exit gate | v2: "**Twenty to thirty lessons with measured costs and defects**"; "failure/repair/cost targets demonstrated, not assumed". v1 E: "No unresolved critical errors; repair/review time and cost are predictable". Narration weeks 5–6: "Predictable accepted-output cost and defect rate" |
| Effort / cost | 2–3 weeks (estimate). v2 hybrid $34.34 variable/lesson ($30.34 with zero generated video, the default [RD-39]); fixed $300/month; reviewer time 85 min/lesson planning figure. Business budget line "Reviewed chapter videos" ₹3,000 × 40 = ₹1.2 lakh (placeholder; re-derive per [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) §6) |

### P4 · Scalable production (v2 phase 4 ≈ v1 F)

| Field | Content |
|---|---|
| Build | "Increase workers only with queue/CPU/storage observations. Expand component and source libraries, not arbitrary per-lesson code generation. Introduce additional languages after real supported-voice/native-review tests. Review student outcomes and board updates. Publish solely approved hashes; keep acquisition/entitlements separate from media production." v1 F adds larger queues, more reviewers, localization, selective 3D. Class 12 subjects only after title-level approval and business day-90 evidence |
| Owner | Founder + review board; engineer; academic owners (more reviewers) |
| Exit gate | "**Stable quality gates and evidence of independent learning**" |
| Not prerequisites | "Native app, Kubernetes, full self-hosted LLM serving, large MCP fleets and a broad Blender asset pipeline are not launch prerequisites." |
| Effort / cost | Human capacity is the constraint: 1,000 hybrid lessons ≈ 1,417 reviewer hours ≈ 8.85 FTE-months (v2); v1 baseline 1,000 reviewer-hours ≈ 6.25 FTE |

### PG · Continuous evaluation (v1 G)

| Field | Content |
|---|---|
| Build | Delayed quizzes, transfer items, confidence calibration, controlled template improvements; the nine prioritized A/B experiments (message 04 §12.2; start with priority 1: explanation-only vs explanation + retrieval + feedback); Super Teacher style comparisons (message 08 §13); narration studies A/B/C |
| Gate | "Changes improve learning or accessibility — not merely watch time." Primary outcome: delayed (initially 7 days), unprompted assessment with unfamiliar but curriculum-aligned items; ≈ 175 learners/group for d = 0.30, ≈ 400 for d = 0.20 (planning calculations, before attrition and clustering) |
| Safeguards | Minors: age-appropriate informed participation, necessary permissions, minimal data, no intrusive emotion/attention surveillance |
| Pointers | [`02_learning_psychology/AB_EXPERIMENTS_and_EVALUATION.md`](../02_learning_psychology/AB_EXPERIMENTS_and_EVALUATION.md); [`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) §9 |

---

## 3. The business track: 13 weeks, gates and engine dependencies

Business gates (all must pass before the next spend tranche): **G1** real (paid) demand · **G2** academic quality and teacher approval · **G3** legal/tax/privacy clearance (written GST advice on the book + premium video bundle, DPDP/minors applicability, CCPA advertising applicability) · **G4** print proof and three like-for-like written print quotes · **G5** rural and urban delivery test · **G6** payment + activation + refund tests (webhook, duplicate redemption, refund, two-device recovery; free viewing without forced registration) · **G7** reprint rule (by SKU, positive contribution, cash, defect/return rates, time before exams) · **G8** day-90 decision. Full table: [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](../01_business_model/INSTRUCTIONS_business_launch_runbook.md) §2.

| Week (days) | Owner (workbook) | Business work and stop rule | Depends on the pipeline for |
|---|---|---|---|
| W1 (1–7) | Founder + academic lead | Interview 15 students, 5 parents, 5 teachers, 4 shops; collect competing books; confirm medium and board/year; source/rights register. Stop rule: "No claim that an Instagram poll proves demand." | P0 source/rights ledger format |
| W2 (8–14) | Academic lead + founder | Test two free-chapter prototypes, price cards, real book pages; three like-for-like print quotes; start tax/privacy review. Cap: **₹60,000 discovery/prototype spend until gate passed** | Two **private** prototypes: academically checked scripts with preview renders; labelled previews, never published [RD-38] |
| W3 (15–21) | Academic editors | Lock two Class 10 titles and **one medium**; 8-paper pagination; all printed solutions; design first 3 free chapters by diagnostic value. Stop a title that cannot be accurately completed before promised delivery | Locale decision [RD-26] → RD-42 (15 Oct 2026); free-chapter policy **DECISION NEEDED (RD-44)**; launch-wave selection [RD-05] | *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
| W4 (22–28) | Video + design team | Reusable diagrams and vertical Reel templates; publish 4–5 Class 10 Reels/week and free lesson 1 per title; track qualified visits and question attempts. "No paid reach boost merely because a Reel gets views." | **Publication only of GF-approved lessons and GS-approved Shorts** [RD-38]; until P2 ends, publication slips rather than bypassing review |
| W5 (29–35) | Editors + developers | Checkout, entitlement database, refund/coupon rules, guardian flow; payment webhook test; free viewing without forced registration. "No third-party behavioural pixels on student learning pages." | Export record contract (S14) and destination resource IDs |
| W6 (36–42) | QA + partnerships | Finish **six free lessons**; low-cost phone tests; teacher specimen; recruit permissioned partners. "No covert teacher commission or compulsory pupil purchase." | P2b launch wave released |
| W7 (43–49) | Publisher + finance | Blind-review representative papers and all prototype solutions; compare printer proofs; approve tax/invoicing/access terms. "Accept transparent preorders only against a credible dispatch date." | — |
| W8 (50–56) | Editorial + video lead | Complete the **paid catalogue promised for launch** and the first two print masters; test scratch-code sequence and two-device recovery; duplicate-redemption and refund tests. "Do not sell all-chapter access while undisclosed major chapters are missing." | P3 controlled batch outputs (paid lessons, each GF-approved) |
| W9 (57–63) | Founder + fulfilment | Authorize only the first short batch against paid demand/partner commitments; test urban and rural dispatch. "Check actual per-SKU print price and latest viable dispatch date." | **Milestone M3** prerequisites (§5) |
| W10 (64–70) | Support + academic lead | Fulfil pilot buyers; repair activation friction; collect voluntary learning feedback; seed 10–20 outlets with capped stock. "No further ad scale while refund or academic issues remain." | Corrections process ([`06_QA_GATES_and_RELEASE.md`](06_QA_GATES_and_RELEASE.md) §8) |
| W11 (71–77) | Growth + partnerships | Promote best-converting Reel families; disclosed referral pilot; digital-only vs bundle (*15 Oct 2026: **DECISION NEEDED (RD-44)** whether a digital-only SKU is in the launch at all*). "One reward/commission path per sale; no incentive stacking." | More Shorts (SH) from released lessons | *(Resolved 15 Oct 2026: out of pipeline scope per RD-49; the pipeline is commercially agnostic and this item lives in the business layer only.)*
| W12 (78–84) | Finance + operations | Reconcile channels and printer stock; reprint by demand and lead time. "Do not print ahead merely to obtain a cheaper unit quote." | Cost ledger reconciliation (08) |
| W13 (85–90) | Founder + review board | Continue, revise price/offer, or stop; Class 12 only after title-level approval; next-season plan; corrections log; source and customer-data audits. "Expansion requires positive contribution, dependable delivery and evidence of learning." | P3 gate result; learning evaluation plan (PG) |

Calendar caveats from the sources: starting 13 Oct 2026 the window ends ≈ 11 Jan 2027; **no 2027 Assam exam date is assumed**; **print lead time is not stated anywhere** (nail it down in the W2 quotes and the W9 gate).

---

## 4. Merged calendar (earliest feasible sequence) [RD-37]

Engine durations are the v2 estimates; narration weeks are message 12 §15; business weeks are the 90-day roadmap. "W" = business week; engine/narration start in W1 after S-GATE.

| W | Engine | Narration | Business | Gates that may be passed this week | Money released |
|---|---|---|---|---|---|
| 0 | PS setup | (setup inside PS) | — | S-GATE | none |
| 1 | **P0** (3–5 days) | prepare corpus inputs | W1 interviews | P0 gate (end W1 or early W2) | ≤ ₹60,000 discovery cap |
| 2 | **P1** begins | **Week 1** casting, corpus, rights | W2 prototypes, quotes | narration W1 gate (approved primary voice per locale) | still ≤ ₹60,000 until G1 |
| 3 | P1 continues | **Week 2** one live transport | W3 lock titles + medium | P1 gate (end W2–W3); narration W2 gate | tranche 1 after G1 (demand) |
| 4 | **P2** begins | **Week 3** independent ASR + real alignment | W4 visuals; publication waits for GF | narration W3 gate (manually verified timing/pronunciation samples) | — |
| 5 | P2 | **Week 4** integration + four pilots | W5 checkout build | — | — |
| 6 | P2 ends (four pilots), **P2b** launch wave | Week 4 completes | W6 six free lessons | **P2 gate** (engine promotion); M1 first public free lesson | tranche 2 after G2 (academic quality) |
| 7 | **P3** controlled batch begins | **Weeks 5–6** batch, queue, dashboard | W7 proofs, tax/access terms | G3 (legal/tax/privacy) approved | — |
| 8 | P3 | Weeks 5–6 | W8 paid catalogue; activation tests | G6; **M2 first paid lesson** | — |
| 9 | P3 ends (latest estimate) | — | W9 first short print batch | **M3 before first print**; G4, G5 | print against paid demand only |
| 10 | P3 gate review | — | W10 fulfilment | **M4 public launch / sales** | — |
| 11–12 | PG starts (learning evaluation design) | — | W11–W12 | G7 reprint rule | — |
| 13 | P4 go / no-go | — | W13 decision | **G8 / M5 day-90 decision** | next season only on evidence |

If P1 or P2 runs to its upper estimate, M1–M4 move right by the same amount. The business plan says the same: "Expansion follows evidence — not sunk costs."

---

## 5. Milestones: what must exist before each

| Milestone | Must exist (all) | Detail |
|---|---|---|
| **M0 · First pilot render with real speech** | S-GATE; P0 gate; P1 compositor selected; narration W1–W3 gates; approved licensed or consented voice with rights record; lexicon covering the lesson's `{{tokens}}` | 03, 04 |
| **M1 · First public free lesson (YouTube/website) or first public Short** | P2 gate passed (four pilots) **or** this lesson itself produced with pilot-grade records; GA and GF approvals issued by the **authenticated approval service** bound to the exact hash [RD-17]; captions; export record without secrets; platform resource ID for the destination; for Shorts: GS approval of the Short's own hash | 03, 05, 06 |
| **M2 · First paid lesson available behind entitlement** | M1 conditions for that lesson; business G6 (payment webhook signature-verified, idempotent, reconciled; duplicate redemption; refund; two-device recovery); entitlement enforced by the platform with signed short-lived playback; access terms published (12 months from activation, latest-redemption date, edition covered); "all paid chapters must be ready, or an honest, specific delivery schedule and appropriate remedy must be visible before payment" | 06 §7, business runbook §3, §6 |
| **M3 · Before first book print** | Every QR destination is a **stable, specific** platform resource ("Why this sign is negative", not a generic playlist); activation secrets generated by the platform (≥ 128-bit random, readable base32), only hashes stored, serial/SKU/edition/batch recorded, never printed sequentially; edition number, syllabus version and errata URL printed; G3 written tax and privacy advice; G4 print proof and three like-for-like quotes; essential solutions printed (not paywalled); access terms and latest-redemption date printed | business runbook §5–§6 |
| **M4 · Public launch / sales** | M2 + M3; G5 delivery test; support channel (permissioned WhatsApp, help pages); corrections process live; no behavioural retargeting of children; guardian-mediated registration where required | 06 §8, 07 §8 |
| **M5 · Day-90 decision** | Measured: CAC, sell-through, contribution by cohort, activation success, academic defects, time to correct an error, learning feedback; P3 gate result | business runbook §12–§13 |
| **M6 · Scale (P4) / Class 12 / new language** | P3 gate; M5 "continue"; for a new language: real supported-voice request + native review + new lexicon + new timing verification | 04 §12 |

---

## 6. Budget envelope and release rules

| Item | Amount (planning estimate) | Rule | Source |
|---|---|---|---|
| Business discovery / prototypes | **₹60,000** cap | Nothing more until G1 passes | business W2 stop rule |
| Business two-title pilot fixed budget | **₹6.5 lakh** (₹6,50,000) | Released in tranches as gates pass | `90-Day_Budget` |
| Suggested available capital ceiling | **₹8 lakh** | "not a mandate to spend it all" | message 06 §14 |
| Of which: reviewed chapter videos | ₹1,20,000 = 40 × ₹3,000 "including allocated human review and machine costs; reusable 2D templates" | Placeholder; re-derive from engine + narration workbooks after pilots | `90-Day_Budget` row 6 |
| Engine set-up (not in the business budget) | v2 hybrid **$10,000** ≈ ₹9.0 lakh; v1 $8,000 ≈ ₹7.2 lakh | Separate line; the ₹8 lakh ceiling cannot absorb it [RD-21] | message 10 §11; 08_cost_models Part E |
| Narration set-up reserve (not in the business budget) | **$4,000** ≈ ₹3.6 lakh | Separate line if its scope is not already inside the engine set-up | message 12 §13 |
| Effect of a separate engineering project | A ₹10 lakh project lowers Base 50,000-sale profit from ≈ ₹34.07 lakh to ≈ ₹24.07 lakh | Budget it explicitly | message 06 §11.5 |

How to combine the models without double counting: [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) §6.

---

## 7. Stop rules and failure responses (any phase)

| Signal | Response | Source |
|---|---|---|
| A critical scientific error in any lesson | Block release regardless of visual score; repair; re-approve on the new hash | message 10 §9 |
| Compositor fails golden fixtures | Stop P1; do not proceed on an unvalidated engine | [RD-07] |
| Voice/provider unavailable or failing | Approved fallback voice/model or the job waits; never silently switch | message 12 §12 |
| Budget exhausted or invoice state unresolved | Pause batch; freeze generation; reconcile | Production_Runbook; `examleaf-observability-cost` |
| Rising human repair minutes, repeated provider failure, spend anomalies | Alert; investigate before scaling | Production_Runbook "Cost and observability" |
| Viral views, few relevant visits | Narrow board/class/topic cues; change distribution, not editing speed | business runbook §13 |
| Paid acquisition exceeds contribution | Stop scaling; improve basket, mix, offer or costs | same |
| Missing chapters or repeated errors | Pause promotion and repair the product | same |
| Refund or academic issues open | No further ad scale | business W10 |
| Learning evidence absent at day 90 | No expansion | business G8 |
