# Architect plan 3 — lens: platform-maturity-and-scale-first

**Lens statement:** platform-maturity-and-scale-first

**Thesis:** ExamLeaf will scale to many formats, Class 1 to Masters, every subject family and any locale because of a small, strict operating core, not because it adds more services. That core has four parts. (1) Versioned, immutable registries describe what can be made: Format, Level, Subject-Family, Locale, Style, Voice, Model and Curriculum. (2) Every artefact is content-addressed and records exactly which registry versions and inputs produced it. (3) Approvals are bound to hashes and to those recorded inputs, and they become invalid automatically when an input is revoked. (4) One durable, idempotent orchestrator runs a stage graph declared by each Format Spec. It writes every model call, render and human minute to a single cost and provenance ledger. Adding a new format, level, subject family or language should mean adding a registry entry and passing a gate, not writing new pipeline code. The existing sections 01–14 already contain most of the parts (contracts, the Approval model, the release-check, the cascade, the harness, the gates). v2 turns them into a platform with maturity levels 0–5, each with its own KPIs.

**Biggest risk:** The biggest risk is that the CE-L10 invalidation rule, read literally as "any registry change invalidates affected approvals", combined with a small in-house review team, turns platform growth into an endless re-review backlog. Each style tweak, model swap or locale glossary edit would re-open hundreds of hash-bound approvals, so the team could not ship new formats or levels. The plan's mitigation separates two kinds of change. A new immutable version leaves approved bytes valid and re-derives by change class. A revocation (a defect, a withdrawn licence, a retracted source) blocks release. Approved Knowledge Units are reused across derived formats, and human sampling for derivatives only is allowed once evidence supports it. All of this depends on the lead confirming that reading of CE-L10 and on approving a new RD before any sampling replaces 100% human review.

---

# ExamLeaf Content Engine v2: platform-maturity-and-scale-first

## 1. Thesis

The pipeline must eventually produce Detailed, Simplified, Recap, Question Analysis, Shorts and more, for Class 1 to Masters, across all subject families, in any language. A founder-engineer and a small academic team will build and review it. With a team that size, scale cannot come from people or from per-format code. It has to come from **declaration plus enforcement**:

- **Declare** what a format, level, subject family, locale, style, voice and model *are*, as versioned registry entries.
- **Enforce** that every artefact records which registry versions and inputs produced it. Every human approval is bound to the artefact's hash and to that set of inputs. Every cost is written to the ledger against the artefact.
- **Orchestrate** one durable stage graph per format. Each step is keyed by its input hash, so re-runs are idempotent and cache hits are free.

On this view, "mature" does not mean more microservices. It means that adding a locale or a format is a data change that passes a gate, and that any change to an upstream input is traced, through recorded dependencies, to exactly the artefacts it affects.

[Recommendation] Treat the existing sections 01–14 as the reference implementation of one cell of the matrix: Assam Board, Class 10–12, STEM, Detailed + Shorts, en-IN/Hinglish/hi-IN, vertical. v2 generalises the *axes* around that cell and does not rewrite the cell itself.

## 2. Platform principles (from the lead decisions)

1. **Commercially agnostic (CE-L1, RD-49).** No schema in v2 has a field for price, tier, entitlement or free/paid. Artefacts carry only neutral metadata: subject, level, format, locale, version, hashes. A CI lint rejects any such field name in pipeline schemas. RD-44 lives only in section 01.
2. **Accuracy scales by subject family, not by commercial value (CE-L8).** The validation profile comes from the Subject-Family entry. No format or level can opt out.
3. **Everything is versioned and hash-bound (CE-L10).** See §3.4 for the invalidation semantics.
4. **Model-agnostic production (CE-L6).** Contracts never name a vendor. A ModelProfile entry pins the full model ID and the effort setting. The Production Kit plus the Haiku→Sonnet→Opus cascade is the default, and strong models act offline as compilers and judges.
5. **Deterministic rendering (CE-L4, CE-L7).** Every format renders through the seek-deterministic harness contract (section 12) on the pinned Linux reference container. A render is identified by (scene hash, harness version, container digest, font bundle hash).
6. **Ultracode is refused in code (CE-L3).** The only exception is the attended $50 probe, which is a ledgered, founder-approved campaign event outside the production orchestrator.

## 3. Architecture

### 3.1 Components (deliberately few)

| Component | What it is | Built from |
|---|---|---|
| **Registry** | Versioned, immutable entries (Format, Level, SubjectFamily, Locale, Style, Voice, Model, Curriculum, Kit). Stored in git as JSON/YAML, validated by JSON Schema, indexed into Postgres at release. A change is made by PR and needs registry gate **GR**. | Extends section 04 schemas, section 05 `ProviderProfile`/`VoiceIdentity`, section 12 style guides, section 13 Kit |
| **Knowledge store** | Typed Knowledge Units (KUs), claims, sources, fixtures, answer keys, curriculum links | Extends `SourceRef`, `Claim`, `ScienceReport` |
| **Artefact store** | Content-addressed object store (SHA-256 keys) plus an `ArtefactRecord` row per object | Generalises the render manifest and `AssetManifest` |
| **Orchestrator** | Durable workflow runner that executes the stage graph declared by a FormatSpec. Steps are idempotent and keyed by input hash, and every step can be resumed | Replaces the per-lesson procedure (07/03) and the Shorts procedure (07/05) |
| **Workers** | Kit/cascade runner, narration compiler (05), harness renderer (12), FFmpeg assembler (04), QA checkers | Reused |
| **Approval service** | The only writer of `Approval`. Binds each approval to (artefact hash, input closure, reviewer identity, role, gate). Enforces the rule that the same identity cannot approve twice | Generalises RD-17 and 07/06 §5 |
| **Ledger** | Append-only tables for cost, provenance, licences and gate events | Extends `budget.py` and the four section 08 workbooks |
| **Observability** | Structured step events, plus dashboards per format × level × family × locale | New and thin. Reads the ledger |
| **Export** | Writes neutral-metadata packages to the platform, with a public provenance block | Extends S14 |

[Recommendation] Durable orchestration starts as **Postgres-backed step state plus a worker queue**. Each step is a row with `(workflow_id, step, input_hash, status, attempts, output_hash)`. That covers resume, retry, idempotency and audit with one database. A dedicated workflow engine is adopted only if the KPIs at maturity level 3 show contention or a need for long human waits that the table cannot express. [Hypothesis] Human gates are the long waits, and a `waiting_on_gate` status covers them.

### 3.2 Data model (the key records)

- **FormatSpec** (id, version): purpose; the KU types it consumes; the stage graph (an ordered list of stages, with optional and parallel branches); duration band; aspect ratio (default 1080×1920, 16:9 allowed per format only, CE-L7); chaptering rule; voice path (A/B, CE-L2); required gates; interaction pattern (from the Super Teacher interaction loop); the QA checks that apply; whether it may be *derived* from approved KUs or must be authored fresh.
- **LevelProfile**: stage band; language-complexity limits; the reviewer roles it requires; flash/motion limits; maximum chunk length; whether Path A is forced; data-collection rules (CE-L9); assessment orientation (recall vs reasoning); the curriculum frameworks it binds to.
- **SubjectFamilyProfile**: the validation mode (fixtures, claim ledger, or both); source-reliability rules; reviewer qualification; required evidence per claim class; revision cadence.
- **LocaleProfile**: language/script, numerals, code-mix rules, pronunciation lexicon, caption fonts, voice inventory with TTS-gate status, native-reviewer pool, subject glossaries.
- **StyleGuide**: design tokens (from 02), motion vocabulary and cue-sheet schema version (12), the vertical style guides, sonic logo (11).
- **VoiceIdentity**: licence reference, path (A/STS or B/TTS), locale coverage, disclosure text, revocation status.
- **ModelProfile**: full model ID, effort, the role it may play (author, critic, judge), price source and date, the experiment-protocol run that qualified it (13).
- **Curriculum framework**: a CASE-shaped hierarchy of competencies with GUIDs, parent/child relations and associations [N46][N47][N48], optional depth-of-knowledge rubrics [N49], and associations between frameworks for crosswalks between boards [N50]. [Recommendation] Store internally in the CASE 1.1 information-model shape [N66][N67][N72], and consume CASE REST/JSON feeds where a provider publishes them [N51][N52][N68]. Do not claim conformance until it is tested against the published conformance document [N70]. CASE 1.1 is a Final specification [N69] with an implementation guide [N71], so it is a stable target. ExamLeaf does not invent a curriculum schema.
- **Knowledge Unit (KU)**: one self-contained topic [N21], typed as concept / procedure (worked example) / reference (definition, formula, fact) / misconception / assessment item [N22]. New types are added by specialisation [N23]. Formats reference KU fragments instead of copying them, so a corrected fragment propagates to every artefact that uses it [N24]. One approved KU set yields many formats [N25]. This is the DITA single-sourcing pattern applied to video. DITA itself is an open, vendor-neutral OASIS standard [N20]. [Recommendation] Use the *pattern*. Do not adopt the DITA toolchain.
- **ArtefactRecord**: `{hash, kind, inputs:[hash], registry_pins:{format@v, level@v, family@v, locale@v, style@v, voice@v, model@v, kit@v, harness@v, container@digest}, producer, ledger_refs, status}`.
- **Approval**: `{gate, artefact_hash, closure_hash, reviewer_id, role, decision, notes, timestamp}`. Here `closure_hash` is the hash of the sorted input hashes plus the registry pins. This extends the existing `Approval` contract, which already binds to the script-bundle hash and the final.mp4 SHA-256.

### 3.3 Flow (generic, driven by the FormatSpec)

1. **Source and plan.** Native extraction (S1), mapping to curriculum GUIDs, then KU authoring and claim extraction (S2–S3). Misconception KUs are authored *before* scripting [N73].
2. **Validate by family.** Fixtures (STEM) and/or the claim ledger (other families) produce a `ScienceReport` or `ClaimReport`.
3. **Compose.** The FormatSpec selects KUs and produces a LessonPlan or ShortSpec, then the script and NarrationPlan draft. Gate **GA** binds the script bundle and records the reviewer roles that the level and subject family require.
4. **Storyboard.** Grid, beats and the token/credit estimate. Gate **H-SB** (two identities) runs before any paid generation (RD-46). Every format that has generated visuals must pass H-SB, including derived formats.
5. **Produce.** Kit/cascade scene authoring, then narration (Path A or B), the cue sheet and the harness render. Each step is an idempotent job written to the ledger.
6. **Automated QA.** All checks run on 100% of artefacts: engine checks, narration checks (−16 LUFS mastering, protected pauses), animated-scene checks A1–A17, flash/motion limits from the LevelProfile, caption/locale checks, the disclosure check (RD-45), and the neutral-metadata lint.
7. **Human final.** **GF** for long formats and **GS** for Shorts, plus level-specific roles (§5).
8. **Export** with the provenance block: contributors, sources and last revision date, the same transparency standard Britannica publishes [N60].

### 3.4 Hash-bound approvals and invalidation (CE-L10 made operational)

Registry entries are **immutable once released**. A change creates a new version. Two events are therefore distinct:

- **New version (supersede).** Approvals pinned to the old version stay *valid for the bytes they cover*, because those bytes have not changed. The artefact is marked `superseded-upstream`. Whether to re-derive it is decided by the change class:
  - *Semantic*: a fixture, claim, KU, curriculum mapping or LevelProfile safety limit changed. The artefact is re-derived and must pass full GA→GF.
  - *Presentational*: a style token, font, harness or container changed. The artefact is re-rendered, all automated QA re-runs, and GF re-runs.
  - *Production-only*: a ModelProfile or Kit changed. This affects only work in flight. Approved bytes are untouched.
- **Revocation.** Examples: a voice licence withdrawn, a fixture found to be wrong, a style that breaks a flash limit, a source retracted. A revocation **invalidates every approval whose closure contains that version**. The affected artefacts are blocked at release-check and enter the re-QA queue.

[Recommendation] The lead should confirm this reading of CE-L10. A "change" means a new version (tracked, re-derivation by class). A defect or revocation means invalidation (blocking). Without this distinction, every token tweak would re-open thousands of approvals. That cost would be self-inflicted.

The release-check (07/06 §6) is extended to recompute `closure_hash` and confirm that no pin in the closure is revoked.

### 3.5 QA sampling at volume

- Automated checks run on 100% of artefacts, always.
- Human gates GA, H-SB and GF/GS run on 100% of **original** artefacts (new KUs, new scripts).
- [Hypothesis] **Derivative** artefacts could move to risk-based human sampling once evidence supports it. Derivatives are artefacts whose inputs are all already approved: a Recap compiled only from approved KUs, a Short cut from an approved lesson, a presentational re-render. The evidence needed: across maturity level 3, the defect-escape rate of derivatives under 100% review is measured and found to be consistently low. This changes existing rules (two human gates on every release), so it needs a new RD and founder approval. Until then, derivatives also get 100% review. Sampling never applies to Class 1–5 content, a new subject family, or a new locale.
- An escaped defect found after release raises the sampling rate for that format × family cell and triggers the errata process (07/06 §8).

### 3.6 Cost ledger and observability

- Every `ProviderJob`, render minute, storage write and human review minute is written as a ledger row against an artefact hash and its registry pins.
- Derived metrics: cost per approved finished minute; rework rate by stage; gate fail reasons; cascade escalation rate (Haiku→Sonnet→Opus) per scene type; cache-hit rate; time waiting on gates; defect-escape rate.
- Dashboards slice these by format × level × family × locale × model. No commercial field exists, so revenue attribution happens downstream in section 01. Section 13's "review-free cost model" becomes a ledger query, not a separate spreadsheet.

## 4. Formats

Each format is a FormatSpec and a set of KU selection rules. **Evidence on length:** median engagement is highest for short videos and falls off past about 6 minutes [N2][N26][N27]. The study authors recommend chunks under 6 minutes [N3] and call longer videos likely wasted effort [N28]. These are MOOC-based proxy measurements [N1], so they are a ceiling to respect, not a target to copy. Mind-wandering rises over long video [N31]. Interpolated questions between segments improved later test scores in one line of research [N30, contested].

[Recommendation] Every format longer than one chunk declares **chapters under 6 minutes**, each with an interpolated retrieval question. The existing ~10-minute Detailed lesson becomes chaptered and is not shortened by fiat. Duration bands for new formats are set from pilot data and the ledger, not invented here.

| # | Format | Built from | Voice path | Aspect | Notes / gates |
|---|---|---|---|---|---|
| 1 | **Detailed** | Fresh authoring; full Super Teacher 10-min structure and explanation ladder | A (CE-L2) | 9:16 (16:9 allowed for a UG/PG lecture variant) | GA, H-SB, GF; chaptered |
| 2 | **Simplified** | Same KUs as Detailed, a lower ladder rung, fewer claims per minute | B | 9:16 | Derived; GA on the new script bundle |
| 3 | **Recap** | Approved KUs only (reference + concept summaries) | B | 9:16 | Derivative; candidate for sampling (§3.5) |
| 4 | **Question Analysis** | Assessment-item KUs + answer keys + misconception KUs | B | 9:16 | Answer key validated by family; reasoning focus, not recall, for Middle and above [N55] |
| 5 | **Shorts** | ShortSpec cut from approved lessons or a single KU | B | 9:16 | GS; disclosure gate |
| 6 | **Misconception Buster** | Misconception KU: state the intuition, test it, resolve it [N73][N76, contested] | B (A for flagship) | 9:16 | Pre/post item pair recorded so the "illusion of understanding" risk [N74] can be measured |
| 7 | **Worked Example / Step-through** | Procedure KU with numbered steps | B | 9:16 | STEM fixture must cover every intermediate value |
| 8 | **Concept Primer** (pre-lesson) | Concept KU + a real-life opener [N37, contested] | B | 9:16 | Single chunk |
| 9 | **Activity / Lab Demo** | Procedure KU + safety notes | A (real demo footage) | 9:16 | Safety reviewer role required |
| 10 | **Derivation Walkthrough** | Chain of concept + procedure KUs | A or B | 16:9 allowed (UG/PG) | Every step a fixture or cited claim |
| 11 | **Chaptered Lecture** (UG/Masters) | Many KUs, chapter map | A | 16:9 declared per format | Chapters under 6 minutes [N3] |
| 12 | **Previous-Year Paper Walkthrough** (competitive / board) | Assessment KUs mapped to exam framework GUIDs | B | 9:16 | Questions need a source and licence entry |
| 13 | **Revision Sprint** | Many Recap fragments in sequence | B | 9:16 | Derivative; interpolated questions |
| 14 | **Read-along / Language Practice** | Text KU + pronunciation lexicon | A | 9:16 | Native speaker in GA; text licence |
| 15 | **Story / Song / Activity** (Class 1–5) | Play-way, multi-modal KUs [N9][N10] | A (mandatory) | 9:16 | Child-development reviewer; young-learner rules |
| 16 | **Case Study / Source Analysis** (humanities, commerce) | Claim-ledger KUs with primary/secondary sources | A or B | 9:16 | Claim-ledger validation (§6) |
| 17 | **Know-a-Scientist / Profile** | Biographical claims [N38, contested] | B | 9:16 | Self-published sources never accepted about living people [N18] |

Talking-head interleaving [N4] and continuous hand-drawn-style motion [N5] are style-guide features, not formats, so any format can use them. A personal, informal feel can outperform studio polish [N7], which supports the human-feel playbook (section 11) over production spend. Speaking rate: higher rates correlated with engagement in MOOC data [N6][N29], but both findings are contested. [Hypothesis] LevelProfiles set speaking-rate bands from pilots. They must never raise the rate for Class 1–5 on the strength of adult MOOC evidence.

## 5. Levels

Each band is a LevelProfile. A level never changes *whether* accuracy validation applies. It only changes reviewer roles, language, motion and length limits.

- **Class 1–2.** The Foundational-stage profile must be sourced from NCF-SE before it is used. No evidence row covers it yet. Until then it inherits the Class 3–5 constraints in their strictest form. Young-learner rules (CE-L9) apply: no data collection and no ads targeting in exported metadata, Path A only, stricter flash/motion limits, simpler language, shorter formats, and a child-development reviewer in GA and GF. The specific flash/motion thresholds must cite a photosensitivity standard added to the evidence register (section 09) before Class 1–5 launches. No numbers are set here.
- **Class 3–5 (Preparatory, Grades 3–5 [N8]).** Pedagogy stays play-way, discovery and activity-based [N9]. Learning is multi-modal: drawing, singing, playing [N10]. Textbooks use language suited to the grade and the child's context [N11, contested]. Video is one resource among many, aligned to curricular goals [N12]. Formats allowed: Story/Song/Activity, Concept Primer, Activity Demo, Shorts, all Path A.
- **Class 6–8 (Middle, Grades 6–8 [N32]).** Nine subjects including three languages [N33]. The shift is toward abstraction [N53] and methods of inquiry rather than accumulating facts [N54]. Assessment targets reasoning [N55]. The curricular shifts include moving "from content to competencies" [N56]. This is why curriculum mapping is competency-GUID based. Science integrates cross-cutting themes [N35]. Direct instruction is balanced with inquiry [N34]. Some units are non-evaluative [N36, contested], so a KU carries an `assessed: bool` flag per framework.
- **Class 9–10 and 11–12 (Secondary).** The existing Assam Board reference cell. All 14 sections apply as they stand. Competitive-exam overlays are separate frameworks associated with the board frameworks [N50].
- **UG and Masters.** Formats may declare 16:9 (Chaptered Lecture, Derivation Walkthrough). Reviewers must be qualified at or above the content level. Exceptional or frontier claims need multiple high-quality sources [N17].
- **Competitive exams.** Modelled as their own curriculum frameworks plus assessment-item KUs. Question Analysis and Previous-Year Paper formats dominate. Licensing of question text is recorded in the licence ledger.

## 6. Subject families beyond STEM

The validation mode comes from the SubjectFamilyProfile (CE-L8).

- **STEM:** validated fixtures (the four models in section 04 are the template). Every number shown on screen traces to a fixture output.
- **Claim-ledger families** (social science, history, geography, commerce, civics, literature commentary, arts theory). The rules are adapted from Wikipedia's verifiability policy:
  - The author who adds a claim carries the burden of proof [N13].
  - A claim without a citation is removed by default [N14].
  - Being true is not enough; the claim must have been published in a reliable source [N15].
  - Reliable sources are not rejected for being costly to access [N16].
  - Exceptional claims need multiple high-quality sources [N17].
  - Self-published sources are never accepted about living people [N18].
  - Wikipedia is not itself a citable source [N19].

  Claims are corroborated against reliable secondary sources [N39]. Each family has its own source-reliability list, which is part of the registry and versioned.
- **Automated triage, not judgement.** Even under a governing policy, citations are often missing [N40]. Models can flag sentences that need a citation and predict why [N41][N42][N43], and have been tested for robustness across quality classes [N44]. [Recommendation] A cheap-model "citation-needed" pass flags uncited sentences before GA. A human qualified reviewer still decides, because evidence suggests human-only curation is uneven at scale [N45, contested], and so is automation.
- **Reviewer roles.** A family profile names its roles: fact-checker, subject editor, supervisory editor, copy editor, information architect. These follow Britannica's published model [N63, contested], where every fact is checked against reputable sources [N59] by scholars and specialists [N61], and content is revised as research changes [N62]. In a small team one person may hold several roles. The approval service still blocks the same identity from approving twice on the same artefact.
- **Languages, Arts, PE, Vocational** (the breadth shown in [N57], contested). These need a native-speaker or practitioner reviewer. Activity content needs a safety review. Text and music licences go in the licence ledger.
- **Time-sensitive families** (economics, current affairs). Claims carry an `as_of` date and a revision cadence [N62]. When an entry expires, a *revocation* is raised for that claim (§3.4).

## 7. Locales at scale

- **LocaleProfile drives everything.** It sets the script, numerals, code-mix rules (Hinglish), lexicon (section 05 pronunciation lexicon, now per locale), glossary per subject, caption fonts in the vendored font bundle, and voice inventory.
- **Launch locales:** en-IN, Hinglish, hi-IN (CE-L5, RD-42). Assamese and other Indic languages ship with **human voice** until a TTS voice passes the native-speaker gate. That gate is **GL**: a blind native-speaker review against the human reference, recorded in the ledger.
- **Localisation is derivation.** On-screen text is externalised into string tables keyed by KU and cue ID, and is never baked into SVG paths. The visual timeline is therefore reused, and only text layers, narration and timing are regenerated. Each locale variant has its own script-bundle hash, so it needs its own GA by a native-language subject editor (already required in 07/06). H-SB re-runs only if layout changes beyond the cue sheet's tolerance.
- **Curriculum stays language-neutral.** Locale never changes curriculum GUIDs.
- Disclosure text is per locale and per VoiceIdentity (RD-45).

## 8. Kit, cascade and models

- **Kit cells.** The Production Kit (section 13) is versioned per (format family × subject family × level band), so a Class 4 story Kit cannot leak into a UG derivation.
- **Cascade.** Haiku→Sonnet→Opus runs per scene. The escalation reason is written to the ledger. Strong models (Fable 5.1 / Opus 5.5) act offline as Kit compilers and judges.
- **Qualifying a model.** A new ModelProfile must re-run the section 13 experiment protocol on a frozen evaluation set for each Kit cell before it can be pinned. Because this is production-only (§3.4), it never touches approved bytes.
- **Contracts stay model-agnostic.** Swapping vendors is a ModelProfile and Kit change, not a code change.

## 9. Maturity levels 0–5

KPIs are *defined* here. Their thresholds are set from the baseline measured at the previous level and recorded as registry policy; none are invented in this plan.

| Level | Name | What exists | KPIs measured | Gate to advance |
|---|---|---|---|---|
| **0** | Reference cell | Sections 01–14 as they are: Detailed + Shorts, STEM 10–12, 56 + 58 tests | Tests pass; one pilot rendered | Audit fixes from section 14 closed |
| **1** | Registered | Registries and schemas; ArtefactRecord and Approval closure wrapping the existing contracts; neutral-metadata lint | % artefacts with complete pins; release-check recomputes closure | 100% of new artefacts pinned; release-check blocks a revoked pin in a negative test |
| **2** | Orchestrated | FormatSpec-driven durable orchestrator runs Detailed and Shorts; idempotent steps; ledger rows on every job | Cache-hit rate; resume success after a forced kill; cost per approved minute | A Detailed lesson reproduces byte-identically on the reference container from its closure |
| **3** | Multi-format | Simplified, Recap, Question Analysis + at least 3 more formats via KU derivation; observability dashboards | Rework rate by stage; gate fail reasons; cascade escalation rate; defect-escape rate | Each new format passes a pilot through every gate; ledger reconciles against provider invoices |
| **4** | Multi-axis | Second subject family (claim ledger), Class 6–8, second Kit cell; optional sampling RD for derivatives | Claim-citation coverage; reviewer throughput; re-QA backlog after revocation | A revocation drill clears its re-QA queue with no escaped release |
| **5** | General | Class 1–5 (young-learner profile), UG/PG 16:9 lecture formats, an Indic locale with human voice or GL-passed TTS | All of the above, per cell; learning evidence (pre/post items) | A new format or locale is added with **zero pipeline code changes** |

## 10. Sections 01–14: reuse, extend, retire

| Section | Disposition |
|---|---|
| 01 Business model | **Moved out of the pipeline.** Holds RD-44, pricing and entitlement. Pipeline export never reads it |
| 02 Learning-psychology rules + tokens | **Reuse.** Tokens become StyleGuide v1. Production rules become checks in the FormatSpec and LevelProfile. `SCENE_PEDAGOGY_SCHEMA` is extended with KU types |
| 03 Super Teacher | **Reuse** as the Detailed FormatSpec. **Extend:** the explanation ladder's rungs are what Simplified and Recap select. The 5 delivery modes become a FormatSpec field |
| 04 Video engine v2 | **Reuse** contracts, the 4 scientific models (STEM fixtures), the 56 tests. **Extend:** ArtefactRecord, closure hashes. **Retire** the 720×1280 proof size as a production target; it stays as a preview profile, with 1080×1920 the default |
| 05 Narration | **Reuse** NarrationPlan, the provider compiler, timeline, −16 LUFS mastering, 58 tests. **Extend:** lexicon per locale; VoiceIdentity gains licence and revocation status |
| 06 Skills library | **Reuse.** Each skill declares the registry axes it serves. Skills for no current cell stay dormant, not deleted |
| 07 Runbook | **Extend.** Gates GA, H-SB, GF, GS and the disclosure gate are kept; GR, GL and the young-learner review roles are added; procedures 03/05 are replaced by FormatSpec stage graphs. RD-16 and RD-26 stay superseded |
| 08 Cost workbooks | **Replaced over time by ledger queries.** The workbooks stay as the planning model and are reconciled monthly against the ledger |
| 09 Evidence register | **Reuse and extend** with this plan's N-evidence, and with the photosensitivity and child-data standards still to be sourced |
| 10 Pilots | **Reuse** as the level-0 golden set and regression corpus |
| 11 Human-feel playbook | **Reuse** as the Path A/B definitions and sonic logo inside StyleGuide/VoiceIdentity |
| 12 Animation layer | **Reuse** the harness contract, cue-sheet schema and A1–A17 checks. The 5 style guides become StyleGuide entries. HyperFrames stays default and Remotion is kept as a benchmark |
| 13 Strong-to-cheap | **Reuse** the Kit, cascade and experiment protocol. **Extend** to Kit cells; the $50 probe stays attended and outside production |
| 14 Audit | **Reuse** as the level-0 exit checklist. Future audits run against maturity KPIs |

## 11. Build order with gates

1. **Freeze the reference cell (level 0).** Close the section 14 fixes and tag a golden set from section 10. *Gate:* all existing tests pass on the Linux reference container. The macOS setup is development only (founder runs Homebrew FFmpeg and Node 24 via nvm himself).
2. **Registries v1 + ArtefactRecord + Approval closure (level 1).** Wrap the existing schemas, write no new workers, add the neutral-metadata lint. *Gate:* negative tests — a revoked voice blocks release; a pricing field fails CI; a self-approval is refused.
3. **Orchestrator + ledger (level 2).** Postgres step table and worker queue; port Detailed and Shorts. *Gate:* kill-and-resume drill; byte-identical re-render from the closure; ledger matches provider invoices.
4. **KU store + derivation (level 3).** Simplified, Recap, Question Analysis, then Misconception Buster, Worked Example and Concept Primer. *Gate:* one pilot per format through GA → H-SB → GF/GS; dashboards live.
5. **Second subject family + Class 6–8 (level 4).** Claim ledger, source lists, citation-needed triage, and the CASE-shaped curriculum import for one framework. *Gate:* revocation drill; reviewer-role separation enforced.
6. **Locale expansion.** String-table externalisation proven on hi-IN; then Assamese with a human voice. *Gate:* GL record for any TTS voice; native-language GA.
7. **Class 1–5 (level 5a).** Sourced Foundational/Preparatory profile, photosensitivity standard cited, child-development reviewer onboarded, Path A only. *Gate:* legal/data review of the export metadata; pilot passed by the child-development reviewer.
8. **UG/PG + competitive exams (level 5b).** 16:9 Chaptered Lecture and Derivation formats; exam frameworks associated to boards. *Gate:* a new format is added with registry entries only.

## 12. Risks

1. **Over-building the platform before content.** [Recommendation] Each level ships only what its KPIs need, and the reference cell keeps producing lessons throughout.
2. **An invalidation storm** if CE-L10 is read as "any change invalidates everything". Mitigated by the supersede/revoke distinction (§3.4), which needs the lead's confirmation.
3. **Reviewer throughput** becomes the binding constraint once formats and families multiply. Mitigated by derivation (approved KUs are reused), citation triage, and evidence-gated sampling for derivatives only.
4. **Unsourced level profiles.** Class 1–2, photosensitivity thresholds and child-data rules are not yet in the evidence register and must be sourced before use.
5. **Contested evidence** (speaking rate [N6][N29], interpolated questions [N30]) could be over-applied. Treat it as hypotheses for A/B tests, not rules.
6. **Curriculum data availability.** Boards may not publish CASE feeds. The CASE shape is internal; imports may be manual.
7. **Localisation breaks visuals** if on-screen text is baked in. The string-table rule must be enforced by a check from level 3.
8. **Model drift.** A pinned model ID may be retired. A ModelProfile replacement re-runs the protocol; approved bytes are unaffected.
