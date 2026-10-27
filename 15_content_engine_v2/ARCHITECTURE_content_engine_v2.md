# ExamLeaf Content Engine v2 — architecture

Status: final specification (synthesis). Date: 15 Oct 2026. Owner: founder-engineer (information architect) with the academic lead.
Supersedes: the per-lesson procedure (07/03) and the Shorts procedure (07/05) as *procedures*. Their rules are kept and recompiled as data.
Binding inputs: lead decisions CE-L1 to CE-L10. RD-49, RD-50 and RD-51 in 07/10. Evidence [N1]–[N76].
Companion documents: Format Registry, Level Profiles, Subject Validation Profiles, Maturity Roadmap, Decisions (CE-01 onward), Templates, Schemas (`schemas/`), Sources.

Tag convention: **[Recommendation]** is a design choice made here. **[Hypothesis]** is a value or claim that a pilot must confirm before anything depends on it. **[Evidence]** cites [N#]. Untagged statements restate binding decisions or existing sections.

---

## 0. Executive summary

ExamLeaf does one thing well today. Sections 04, 05, 07, 12 and 13 produce a roughly 10-minute Assam Board Class 10–12 STEM lesson with derived Reels, in 9:16, in en-IN, Hinglish or hi-IN. The founder now wants the same engine to make many formats (Detailed, Simplified, Recap, Question Analysis, Shorts and more), for every stage from Class 1 to Masters, in every subject family and any language, without losing anything that already works. The non-negotiables stay: scientific and factual accuracy, human approvals bound to hashes, deterministic rendering, cheap-model production through the Production Kit and cascade, cost ledgers and the storyboard gate. The engine must also stay commercially agnostic.

The v2 design rests on three separations.

1. **Truth is separated from packaging.** One canonical, source-grounded **Lesson Graph** holds claims, objectives, concept steps, analogies, misconceptions, worked items, assessment items, simplifications, activities, stories, vocabulary, text passages, media and locale renderings. Each objective is bound to a curriculum competency GUID in a CASE-shaped **Curriculum Graph** [N46]–[N50]. Academics approve the graph once (GA-Graph). Every format reads from it and none may add truth to it.
2. **Formats are data; slot types are code.** A **Format Spec** is a versioned declaration: which graph nodes to select, which beat grammar to lay out from a **closed, tested slot vocabulary**, what length, aspect, voice path, interaction and gates apply. A deterministic **Derivation Compiler** turns graph × spec into the contracts that exist today (LessonPlan, SceneSpec, NarrationPlan, cue sheet). Adding a format is a data change that passes a linter and one golden render. Adding a slot type is code with tests and an A-check.
3. **Who is learning is separated from what is made.** Level, audience safety class, persona, accessibility, subject family and locale are registry entries. A **Resolver** compiles one **Effective Production Profile (EPP)** per artefact by fixed precedence rules: safety beats level, level beats format, format beats style. Validation is the union of all applicable validators, gates are additive and never removed, and duration is an intersection (an empty one is a compile error). Every author, Kit task, validator and reviewer reads the EPP, and every approval binds to its hash.

Accuracy scales by subject family, never by commercial value (CE-L8). STEM keeps executable fixtures (the four validated models in 04 become the first entries of a fixture library). Every other family uses a source-grounded claim ledger with verifiability rules [N13]–[N19], a citation-need flagger that only adds flags [N43], a span-hash check against a stored copy of each source, a four-state contested-claim policy and a qualified-reviewer rubric. A family cannot be activated without a named, qualified reviewer; the schema enforces it.

Everything is versioned and hash-bound (CE-L10). Hashes use RFC 8785 canonical JSON after Unicode NFC normalisation, so Devanagari, Bengali-Assamese and Hinglish text hash identically across tools. Every registry change is classified (semantic, safety, pedagogical, locale, presentational, narration, production, render toolchain, metadata, revocation). Every change queues re-QA of exactly the affected artefacts. Human gates reopen only when bytes change or the change class requires human judgement, and revocations block release.

The build is **files first**. Registries, graphs, sources and approvals are versioned JSON in git with JSON Schema draft-07 validation. There is no database, graph store or workflow engine until a measured KPI needs one. The first milestone is one vertical lesson end to end: the Class 10 Ohm's-law blueprint from section 02, re-expressed as a Lesson Graph, compiled to a Detailed lesson and one Short, rendered at 1080×1920 in the pinned Linux container, passed through every gate, cost-reconciled and reproduced byte-identically.

Biggest risks: review and Path A studio capacity (now the binding constraints), slot-vocabulary sprawl, unproven young-learner numbers, and legal scope for child-directed content. Each has a named mitigation and a revisit trigger.

Addendum, 15 Oct 2026 (CE-111 to CE-122, completeness review): the specification now also covers the Curriculum Framework schema and GUID-minting rule (§2.6), the blob store and the untrusted-data rule (§2.2), the `framework/`, `rights/` and `a11y/` registry kinds (§3.1), signed approvals and agent identities (§3.2, §3.7), the framework-diff change rows and the exam-window freeze (§3.6), the `print` render target (§3.3), the corpus representation audit (§7), the transcreation rule (§8), the new §9.5 Storage, backup and recovery, §9.6 Incidents, withdrawal and on-call and §9.7 Learning signals (aggregate only), and open items O-23 and O-24 (§12).

---

## 1. Scope and principles

### 1.1 Scope

In scope: every artefact ExamLeaf produces from curriculum-aligned knowledge, for any format in the registry, any level from Class 1 to Masters plus competitive, vocational, adult-professional and educator audiences, any subject family with an activated validation profile, and any locale with an admitted Locale Profile.

Out of scope (owned elsewhere): entitlement, pricing, bundles, free-chapter policy, storefront and ads (section 01 and the platform layer); learner accounts and learner data (platform); live classes.

### 1.2 Principles

**P1 Commercially agnostic (CE-L1, RD-49).** No schema, registry entry, job, check or export field carries price, free/paid, tier, entitlement, subscription or SKU meaning. Artefacts carry neutral metadata only: subject, family, level, format, locale, competency GUIDs, versions, hashes, audience safety class, accessibility tracks, disclosure and provenance. A CI **commercial-term lint** rejects, case-insensitively, any match of `(price|pricing|paid|is_free|free_|premium|entitle|subscri|sku|paywall|unlock|monetis|monetiz|revenue|discount|coupon|tier|destination_resource|cta_destination|funnel|purchase_|checkout_|product_id|offer_|trial_|utm_|campaign_|affiliate_|activation_code|storefront)` in every pipeline schema, registry file and export sidecar, applied to every object key at every depth (including REN `fields` keys), every `required` entry, pattern key and enum or const value (regex and scope widened 15 Oct 2026; the earlier regex omitted `tier` and the funnel terms and covered property names only). Three editorial fields are explicitly exempt and documented as non-commercial: `series_position`, `flagship` and `demo_kind` (§3.4). The word "tier" is not used in any pipeline field name; source quality is `reliability_class` and objective depth is `depth_band`. RD-44 lives only in section 01. The audience safety class is not commerce: it describes who the content is safe for, and the platform maps it to store flags (CE-17).

**P2 Accuracy first, scaled by subject family (CE-L8).** No format ships without its family's validation. A format or level can add validators but can never remove one.

**P3 Human gates bound to hashes (CE-L10).** Every human approval binds to the artefact SHA-256, the EPP hash, the graph subtree hash and the closure hash of all registry pins. Gates are never sampled (CE-14). ~~The same identity cannot approve twice on one artefact or approve content it authored.~~ Within one gate, every required role is held by a distinct identity (for example GF: academic owner and production QA are two people). No identity approves a gate that covers a node, script, performance or render it authored. One identity may approve different gates on the same artefact. (Corrected 15 Oct 2026: the struck reading would refuse the academic owner's GF signature after GA-Δ, which QA_PROFILES §4.1 requires; 07/06 §5 asks for distinct identities within one approval pair.)

**P4 Deterministic rendering (CE-L4, CE-L7).** Every format renders through the seek-deterministic harness contract (section 12) in the pinned Linux reference container (RD-50). Model and TTS outputs are stored by hash and replayed, so a re-render from a closure reproduces identical bytes (§9.3).

**P5 Model-agnostic, Kit-first production (CE-L6).** Contracts never name a vendor. A ModelProfile pins the full model ID and explicit effort. The Production Kit plus the Haiku→Sonnet→Opus cascade fills slots per scene. Strong models (Fable 5.1 / Opus 5.5) work offline as compilers and judges. Ultracode is refused in code; the single attended, founder-approved, provider-capped $50 probe in the strong-model campaign is the only exception and runs outside production (CE-L3, RD-48).

**P6 Vertical first, aspect defined by format (CE-L7).** The default is 1080×1920 (9:16). A Format Spec may declare 16:9 (1920×1080) only for lecture-style formats at `level/ug`, `level/pg` or `level/adult_prof`; the schema enforces this. Aspect is decided per format, never per lesson.

**P7 Any language through Locale Profiles (CE-L5).** Claims are locale-invariant; renderings are locale-specific child nodes. Launch locales are en-IN, Hinglish and hi-IN. Assamese and other Indic languages ship with a human voice (Path A) until a TTS passes the native-speaker gate.

**P8 Safety is data, enforced by deterministic validators.** Audience safety classes, accessibility and persona rules are registry entries checked by linters before any human gate (CE-17 to CE-23).

**P9 Smallest thing that works.** Files before services; one runner before an orchestrator; report-only validators before blocking ones (except the safety-critical set in CE-35). Each maturity level ships only what its KPIs need.

**P10 Labelled uncertainty.** The quantitative engagement evidence comes from adult MOOC learners measured by proxies (watch time and problem attempts) [N1], for 1× plays only [N7]. Any value that extrapolates it to children, Indic locales or vertical mobile video is tagged [Hypothesis] with an owner and a pilot, and the schema rejects an untagged null.

---

## 2. The Lesson Graph (single source of truth)

### 2.1 Role

The Lesson Graph is the canonical store of *what is true and taught*. It generalises 04's `SourceRef`, `Claim` and `LessonPlan` content. It follows the DITA pattern of typed, self-contained topics [N21][N22], reused by reference [N24] and single-sourced into many outputs [N25], extended by specialisation [N23]. ExamLeaf uses the pattern, not the DITA toolchain [N20]. One correction to a shared node propagates to every format that cites it and, through the dependency index, to every approval that consumed it.

### 2.2 Storage

- `content/graphs/LG-<id>.json`: one graph document per lesson scope (objective set), validated by `schemas/lesson_graph.schema.json`.
- `content/sources/SRC-<id>.json`: the **Source Registry**, the single writer for sources, validated by `lesson_graph#/definitions/source`. Graph documents reference sources by ID and never embed them (CE-48).
- `content/curriculum/<framework_id>.json`: Curriculum Graph frameworks (§2.6).
- `content/approvals/`, `content/ledger/`: append-only JSONL.
- `content/blobs/sha256/<aa>/<hash>`: the write-once, content-addressed blob store for every hashed binary (narration audio, Path A raw takes, consulted SRC copies, MED files, lossless intermediates, renders); `<aa>` is the first two hex characters of the SHA-256. The manifest is in git; versioned object storage holds the bytes. Backup, retention classes and the restore drill are in §9.5 (level-1, 15 Oct 2026, CE-114) [Recommendation].

Graphs reference nodes owned by other graphs (conref-style [N24]); the loader resolves cross-graph IDs and includes them in closures.

**Untrusted data in model prompts (level-1, 15 Oct 2026, CE-113).** SRC copies, TXT passages, syllabus PDFs, learner doubts and learning-signal text (§9.7) are untrusted data. When they enter a model prompt they are passed as delimited data, never as instructions, and no Kit task, judge or skill acts on an instruction found inside them [Recommendation]. The closure check remains the backstop: every assertive sentence must map to an approved node, so injected text cannot reach a script as truth.

### 2.3 Node types (14 graph types plus the source record)

All nodes carry the base fields `id` (type-prefixed), `node_type`, `version` (semver), `status` (draft → machine_checked → expert_approved → superseded | revoked), `locale_invariant`, `sha256` and `provenance`. **Each type schema lists the base fields itself and sets `additionalProperties: false`** (no `allOf` base), so a misspelled field (`fixture_id` for `fixture_ids`, `sources` for `source_refs`) or a commercial field fails validation. A negative test in CI proves it.

| Prefix | Node | Key fields (beyond base) | Main rules |
|---|---|---|---|
| OBJ | Objective | `statement`, `competency_guid`, `framework_id`, `depth_band` (core/extension), `dok_from_framework?`, `assessed`, `requires[]` (OBJ prerequisite edges) | Depth of knowledge is taken from a framework rubric only when one is published [N49], never invented. `assessed: false` marks non-evaluative units [N36] (contested evidence). |
| CLM | Claim | `statement`, `claim_type`, `objective_ids[≥1]`, `source_refs[≥1]` (source_id, locator, span_sha256), `risk`, `contested_status`, `attribution?`, `board_position_decision?`, `fixture_ids[]`, `assumptions[]`, `requires[]`, `key`, `contrast_dimension?`, `time_bound`, `as_of_date?`, `review_by?`, `jurisdiction?` | ≥1 source always [N14][N15]. Exceptional or sensitive risk needs ≥2 sources [N17]. Attributed and contested claims need an attribution. `board_vs_scholarship` needs a recorded decision. `time_bound: true` requires `as_of_date` and `review_by`. Claim types exam_pattern, legal_rule, rate_or_threshold, current_affairs and clinical force `time_bound: true`. legal_rule requires `jurisdiction`. |
| CON | Concept step | `rung`, `text`, `supports[CLM ≥1]`, `objective_ids` | A rung of 03's explanation ladder. |
| ANL | Analogy | `mapping`, `non_mapping`, `likely_misconception?`, `formal_return`, `permitted_levels[≥1]`, `supports[CLM ≥1]` | Mirrors SIM: an analogy is usable only at the levels the reviewer approved. |
| MIS | Misconception | `statement`, `why_plausible`, `confronted_by[CLM ≥1]`, `diagnostic_item?` (ASM), `priority` (1–5), `objective_ids` | Misconceptions are authored before scripting [N73]; ignoring them risks an illusion of understanding [N74][N76]. Priority drives Recap and Short selection. |
| WRK | Worked item | `problem`, `steps[]` (n, text, claim_ids, fixture_ref, common_error_mis_ids), `answer`, `objective_ids`, `twin_of?`, `fixture_ids[]` | `twin_of` links a faded twin to its parent. Every STEM intermediate value has a fixture_ref. |
| ASM | Assessment item | `stem`, `item_kind`, `expected_answer`, `acceptable_variations`, `hint`, `feedback`, `objective_ids`, `misconception_ids`, `evaluative`, `original`, `exam_tags?`, `answer_key_check` | `original: true` forbids marks and marks_source and needs no source paper. `original: false` requires `exam_tags.source_id`, `board_or_exam` and `year`. Marks require `marks_source ∈ {source_paper, official_key}`. |
| SIM | Simplification | `of` (CLM), `simplified_statement`, `what_is_lost`, `permitted_levels[≥1]` | The only way any format may say less than a claim (CE-11). |
| ACT | Activity | `title`, `objective_ids`, `materials`, `household_safe`, `steps`, `safety_claim_ids`, `observation_claim_ids`, `grown_up_cue`, `demo_kind` (real/virtual) | Not household-safe ⇒ ≥1 safety claim. |
| STY | Story | `title`, `objective_ids`, `beats[]` (each `carries` CLM or SIM IDs), `song_chant?` (text, music_source, license_ref), `real_child_likeness: false` | Every story beat that teaches carries an approved claim or simplification; licensed music needs a licence reference. |
| VOC | Vocabulary | `term`, `definition_claim_id`, `lexicon_key?`, `objective_ids` | Feeds 05 pronunciation lexicon and level vocabulary lists. |
| TXT | Text passage | `text`, `edition_source_id`, `span_locator`, `rights_status`, `license_ref?`, `char_count` | Literature and language passages; licensed text needs a licence reference. |
| MED | Media asset | `asset_kind`, `file_sha256`, `rights_status`, `license_ref?`, `generator?`, `depicts_real_child`, `guardian_release_ref?`, `map_boundary_review?` | A map requires a boundary review against a registered policy source; a real child requires a guardian release; generated assets record their ProviderJob. |
| REN | Rendering | `rendering_of`, `locale`, `fields{}`, `source_node_sha256` | A locale rendering of any node. If the source node hash changes, the rendering goes stale automatically. |
| SRC | Source (registry record) | `citation`, `reliability_class`, `rights_status`, `copy_sha256`, `access_date`, `edition?`, `url?`, `self_published`, `about_living_person`, `open_wiki: false` | Self-published sources about living people fail [N18]. Open wikis are not citable [N19]. A source is never rejected for cost of access [N16]; a hash of the consulted copy lets a reviewer re-check spans. |

### 2.4 Edges

Edges are **typed ID-reference fields on the owning node**: `supports`, `requires`, `confronted_by`, `of` (simplifies), `objective_ids` (assesses/teaches), `twin_of`, `rendering_of`, `source_refs`, `carries`, `diagnostic_item`, `common_error_mis_ids`. There is no separate edge store [Recommendation, CE-06]. Every edge is therefore inside its owner's hash and inside every subtree hash, and the schema validates edge target prefixes. Crosswalk associations between curricula live in the Curriculum Graph (§2.6), not in content.

### 2.5 Versioning, hashing and provenance

- **Hash canon (CE-32).** Every string is normalised to Unicode NFC, then the document is serialised with RFC 8785 JSON Canonicalization Scheme (JCS), then SHA-256 is taken. The `sha256` field itself is excluded when hashing a node. Measured quantities are decimal strings with units ("2.50 V") so significant figures survive. JSON numbers are integers or multiples of 0.5 (marks) only. CI runs a **cross-language golden-hash test**: Python and Node implementations must produce identical hashes for a fixture set that includes Devanagari, Bengali-Assamese (with conjuncts), Hinglish, NFD-decomposed input and Urdu (RTL) strings.
- **Node closure hash.** `node_closure_sha256(node)` (renamed 15 Oct 2026 from `closure_sha256(node)` to keep it apart from the approval `closure_hash` of §3.7) hashes the sorted list of (id, sha256) for the node, every node it references transitively and every referenced SRC record.
- **Subtree hash.** `subtree_sha256` for a lesson scope hashes the closure of its objective set.
- **Versions.** A semantic change bumps the minor or major version; a typo in a non-asserting field bumps the patch. Any byte change produces a new hash whatever the version, so approvals never rely on semver.
- **Provenance.** Every node records `author_kind` (human, model, import), `author_id` and `created_at`. A model-authored node must record `model_id` (full ID), `effort` and `kit_version` (schema-enforced; CE-L6). An imported node records `import_ref`.

### 2.6 Curriculum Graph

A Curriculum Framework file holds a board × edition × stage × subject hierarchy of items (competency, learning outcome, topic). Each has a GUID, parent/child links and associations (`prerequisite_of`, `crosswalk_equivalent`, `assessed_by_blueprint`, `non_evaluative`), in the CASE 1.1 information-model shape [N46][N47][N48][N50][N66][N67][N72]. Optional depth rubrics are imported when published [N49]. CASE is a Final specification [N69] with conformance [N70] and an implementation guide [N71], so it is a stable target. **[Hypothesis]** Indian boards, including Assam's, probably publish no CASE feeds. ExamLeaf therefore acts as its own CASE Provider [N51] with stable internal GUIDs. A REST/JSON binding [N52][N68] is built only when a partner needs it, and no conformance claim is made until tested [N70] (CE-04). The curricular shift "from content to competencies" [N56] is why objectives bind to competency GUIDs rather than free text (CE-05). Crosswalks let one graph node serve Assam Board, NCERT/CBSE and a competitive syllabus without duplication [N50].

Gate **H-CG**: the academic owner approves the framework version and the selected item GUIDs for a lesson scope. It replaces the syllabus-map half of H-S2; rights stay in H-S2.

**Curriculum Framework record (level-1, 15 Oct 2026, CE-111).** A framework validates against `schemas/curriculum_framework.schema.json` (draft-07, `additionalProperties: false`). It carries `framework_id` (edition-independent and matching the schema pattern `framework/<id>`, for example `framework/seba_hslc_science` as in TEMPLATES §6; corrected by the critic-pass verifier 15 Oct 2026, the earlier example `FW-assam-class10-science` failed that pattern and would have minted different GUIDs), `board`, `edition`, `stage`, `subject`, `medium_locale`, `valid_academic_years[]` (CE-116, §3.6), `exam_windows[]` {name, start, end} (CE-122, §3.6), `source_refs[≥1]` (SRC records with `reliability_class: official_curriculum`, each with `locator` and `span_sha256`) and `items[]`. Each item carries `guid`, `human_code`, `kind` (competency, learning_outcome or topic), `statement`, `parent_guid?`, `associations[]` {type ∈ prerequisite_of, crosswalk_equivalent, assessed_by_blueprint, non_evaluative; target_guid} and `source_span` {source_id, locator, span_sha256}, so every item links back to the syllabus text it came from. H-CG still binds `framework_version`.

**GUID minting rule (level-1, 15 Oct 2026, CE-111).** `guid = UUIDv5(namespace = UUIDv5(NS_URL, framework_id), name = human_code)`, where `human_code` is the edition-independent code of the item. Re-ingesting the same syllabus therefore returns the same GUIDs, and an item carried into a new edition keeps its GUID, so the framework diff of §3.6 is computed per GUID and a re-ingest never sets off an invalidation storm [Recommendation].

**Ingestion (level-1, 15 Oct 2026, CE-111).** The skill `examleaf-curriculum-ingest` turns a syllabus PDF into candidate items with source spans; nothing enters `content/curriculum/` until H-CG approves it. Hand-authored frameworks (the `cg-import` path) validate against the same schema. The schema, its fixtures and negative tests enter CI before M1 step 1 (P1-14 "curriculum_framework schema, fixtures and negative tests in CI before M1 step 1"), because the M1 exit gate requires schema CI for every record type M1 writes.

---

## 3. Registries and request resolution

### 3.1 Registries

All registries are versioned JSON/YAML files in git with a JSON Schema each. Entries are immutable once released; a change is a new version made by pull request through gate **GR** (registry change review with impact preview). GR's registry check validates the entry against its schema and confirms that every id an entry references exists in the registry snapshot (added 15 Oct 2026; per-artefact schemas take registry ids as patterns, so this check and Q-SCHEMA's EPP check replace the old enums). IDs follow `^<kind>/<lowercase-id>(@semver)?$`, for example `safety/ac0`, `level/l9_10@1.0.0`, `locale/hi-in`.

**Registry entry hash (15 Oct 2026).** A registry entry is parsed as YAML 1.2 core schema (JSON is valid input). Anchors, aliases, merge keys, explicit tags and duplicate keys are rejected, and every date or date-time is a quoted string. The pin is `sha256(JCS-RFC8785(NFC(parsed value)))`, so comments and layout are not hashed. The Q-HASH golden fixture set includes one YAML registry entry with an unquoted `no`, a quoted date and a Devanagari string; Python and Node must agree on its hash.

**Id character sets (15 Oct 2026; one pattern per kind in every schema).** `format`, `level`, `family` and `overlay`: `[a-z0-9_]+`. `style`, `persona`, `locale`, `music`, `voice`, `packaging`, `framework`, `rights` and `a11y`: `[a-z0-9][a-z0-9_-]*` (the last three added 15 Oct 2026 with CE-111, CE-112 and CE-120; lead ruling CE-124). `lex` and `gs`: `[a-z0-9][a-z0-9_.-]*`. A persona variant: `#[a-z][a-z0-9_-]*`. Each is optionally followed by `@x.y.z`.

| Registry | Holds | Seeded from |
|---|---|---|
| `format/` | Format Specs (26 in v1; Format Registry document) | 03 10-minute structure, 07/05 SH1–SH8 |
| `slot/` | Closed slot-type vocabulary; each entry names its code module, tests and A-check | 02 production rules, 03 interaction loop |
| `level/` | Level Profiles: l1_2, l3_5, l6_8, l9_10, l11_12, ug, pg, adult_prof, voc, educator | 02 §G/§B values for L9–12, NCF stages [N8][N32] |
| `overlay/` | Exam overlays (jee, neet, cuet, olympiad_junior, olympiad_senior, nmms, jnvst, upsc, state_psc, ca_cs) | new |
| `safety/` | Audience safety classes ac0, ac1, ac2 | new (CE-17) |
| `a11y/` | Accessibility profiles (`a11y/base` in v1) | 02 §D7/§J |
| `persona/` | Persona variants inheriting the 03 core | 03 |
| `family/` | Subject-family validation profiles (`subject_profile` schema) | 04 science validators |
| `locale/` | Locale Profiles | 05 lexicon, 07/04 §18 locale gate |
| `style/` | Style guides (tokens, motion vocabulary, sonic logo, aspects supported, safety classes allowed) | 02 tokens, 12 five style guides, 11 sonic logo |
| `voice/` | VoiceIdentity (licence, path, locales, disclosure text, GL-voice status, revocation) | 05 VoiceIdentity/ProviderProfile, 11 |
| `model/` | ModelProfile (full model ID, effort, role, qualifying experiment run) | 13 |
| `kit/` | Production Kit versions per Kit cell | 13 |
| `harness/` | Harness version, container digest, font bundle hash, Chrome build, FFmpeg build, HarfBuzz version | 12, RD-50 |
| `reviewer/` | Reviewer registry (qualifications, roles, families, levels, locales, conflicts, delegates) | 07/09 roles |
| `budget/` | Budget and ledger policy: per (format × level × voice path) reservation lines, invoice-reconciliation tolerance, delegate caps. Change class Metadata (§3.6). Added 15 Oct 2026 | 08 cost workbooks |

**Addendum, 15 Oct 2026 (CE-63): registry kinds added by the subsystem specifications.** The subsystem documents in `subsystems/` need five kinds the table above does not list. They follow the same rules (versioned files, JSON Schema each, immutable once released, change by pull request through GR) and the same id pattern.

| Registry | Holds | Owner document and schema | Change class (§3.6) |
|---|---|---|---|
| `qa/` | The check catalogue (`qa/catalogue@x.y.z`): check ids, severities, owners, applicability per format, level, safety class and family | `subsystems/QA_PROFILES_REGISTRY.md`; `qa_profile.schema.json` | ~~**Validation** (same row as a subject-family profile): re-run the affected checks on every artefact in scope; GV-claims or GA-Δ only for artefacts that fail a tightened rule~~ Corrected 15 Oct 2026: classed by the effect of the diff; GR rejects a release whose declared class does not match it. Tightening (a new check, raised severity, narrowed threshold or wider applicability) is **Validation**: re-run the changed checks on every artefact in scope, and send any failing artefact to the owner gate of that check. Loosening any Q-SAFE, Q-FLASH, Q-A11Y, Q-DISC or Q-RIGHTS check (lowered severity, widened threshold, narrower applicability or removal) is **Safety**: before merge it needs child-development sign-off where `safety/ac0` is in scope, and a G-COUNSEL re-record where a class's rules loosen (§3.6, safety-class row). Loosening any other check is **Validation**, with the academic lead signing off at GR. GR refuses removing a CE-35 day-one check or making it report-only (QA §3 rule 4); that needs a new CE decision. Adding a gate or a co-sign role is **Structural**: unreleased artefacts acquire it before RELEASE-CHECK, and released artefacts go stale and acquire it at re-QA |
| `music/` | Sonic logos, stings, beds, SFX, ambiences and song backings; owned or commissioned audio only; a style entry points to its logo with `sonic_logo_ref: music/<id>@x.y.z` (the sonic logo no longer lives inside `style/`) | `subsystems/MUSIC_and_SOUND_REGISTRY.md`; `music_entry.schema.json` | Presentational for a new logo, bed or SFX version; Safety for AC0 audio parameters; Revocation for a withdrawn licence |
| `lex/` | Pronunciation lexicons per family and locale: `lex/<family>.<locale>@x.y.z`, plus `lex/core.<locale>` for numerals, units, dates and currency. A lesson lexicon is `core ∪ family`; the Locale Profile `lexicon_ref` points here. The Level Profile `lexicon_ref` (a controlled-vocabulary list, `lex/<level>-<locale>` in `TEMPLATES.md`) reuses the prefix and the field name for a different meaning, recorded as P1-09 in the Roadmap | `subsystems/VOICE_and_PERSONA_REGISTRY.md` §3.6 | Locale/narration (already a row in §3.6: "Locale lexicon or glossary") |
| `gs/` | Golden sets for the GL-voice native-speaker gate: `gs/<locale>-<family>` (the 05 casting corpus generalised) | `subsystems/VOICE_and_PERSONA_REGISTRY.md` §3.7 | Narration: a change re-runs GL-voice for every admitted voice in the locale; released artefacts are unaffected unless a defect is found; not an EPP pin; it reaches artefacts only through the voice entry's golden_set record (15 Oct 2026) |
| `packaging/` | Packaging profiles per channel: encode, renditions, captions, disclosure placements, copy rules, the neutral sidecar | `subsystems/PACKAGING_and_DISTRIBUTION_REGISTRY.md`; `packaging_profile.schema.json` | **Two halves.** Distribution fields (copy rules, sidecar, chapters mode, series display) are Metadata: re-export only. Bytes fields (encode, burned captions) are Render toolchain or Presentational. The EPP pins only `packaging/<id>@x.y.z#render` (SHA-256 of {render_variant, loudness, captions.max_lines, safe_zone}); the whole-profile hash is `binding.packaging_profile_sha256` (15 Oct 2026; the end-card line belongs to the master, never to packaging) |

Two id extensions in the same addendum. A persona reference may carry a variant after the optional version: `persona/<id>#<variant>` or the pin `persona/<id>@x.y.z#<variant>` (see the §6 note). Lexicon and golden-set ids may contain a dot to separate family from locale. ~~The resolver's pin map (EPP `pins`) takes entries of all five new kinds, and RELEASE-CHECK recomputes them like any other pin. (15 Oct 2026: in practice `music/` is pinned through the cue sheet and `gs/` through the voice entry, §3.5 Required pins.)~~ Corrected 15 Oct 2026 (resolver-02, resolver-08): the resolver's pin map (EPP `pins`) takes entries of the new kinds `qa/`, `music/`, `lex/` and `packaging/` (packaging as its `#render` bytes half), and RELEASE-CHECK recomputes them like any other pin. `music/` candidates are pinned at S5 (MUSIC §2.1 item 4); their placement is written to the cue sheet at S10. `gs/` appears only on the voice entry's `golden_set` record and is never an EPP pin.

**Addendum, 15 Oct 2026 (CE-111, CE-112, CE-120): `framework/`, `rights/` and `a11y/` kinds.** Same rules and id pattern as above; id character set `[a-z0-9][a-z0-9_-]*`, optionally followed by `@x.y.z`. `a11y/` is already in the main table; this row adds its new profiles and states its change class.

| Registry | Holds | Owner document and schema | Change class (§3.6) |
|---|---|---|---|
| `framework/` (level-1, CE-111) | Curriculum Framework versions (§2.6), stored as `content/curriculum/<framework_id>.json` and released through GR and H-CG; the registry id is the `framework_id` itself (already lowercase `framework/<id>`) | §2.6; `schemas/curriculum_framework.schema.json` | Classed by the framework diff (§3.6, CE-116): an item removed or a depth or outcome change is Semantic (truth class); an item text or metadata edit is Metadata; a moved item is Metadata plus H-CG; an added item opens a coverage-gap row only |
| `rights/` (level-1, CE-112) | Written rights positions per publisher class, `rights/<publisher>@x.y.z` (O-23): verbatim display, adapted display, marks citation and figure redraw, the statutory basis counsel relies on, the `quotation_within_policy` limits (characters per source per artefact) and an expiry. SRC `rights_basis` {policy_ref, decided_by, decided_on} cites an entry and is required when `rights_status` ≠ `consulted_only`; Q-RIGHTS fails when `rights_basis` is missing or its policy has expired (P1-17 "rights_basis field and Q-RIGHTS expiry check") | Counsel; `lesson_graph.schema.json` SRC definition; `subsystems/QA_PROFILES_REGISTRY.md` Q-RIGHTS | [Recommendation] Tightening is Validation (re-run Q-RIGHTS on every artefact citing the publisher); loosening is Safety (G-COUNSEL re-record before merge); withdrawal or expiry is Revocation for every artefact relying on it |
| `a11y/` (level-3+, CE-120) | `a11y/base` (exists); `a11y/low_vision` (larger caption scale, higher-contrast tokens, no meaning carried by thin lines); `a11y/cognitive` (pacing slower than the level band, one idea per beat, plain-language SIMs only); `a11y/dyslexia` (font, spacing and line-length tokens) [Hypothesis until piloted]; `a11y/isl` (an Indian Sign Language interpreter inset in a safe-zone token; Path A only; gated on a qualified ISL reviewer in `reviewer/`). Q-A11Y adds keyboard and screen-reader labels for every ASM option in the interaction sidecar, and reading-order and tag checks for `print` (CE-119). Sources to register: O-24 | `LEVEL_PROFILES.md` a11y section; `subsystems/QA_PROFILES_REGISTRY.md` Q-A11Y | Safety (the existing "Accessibility profile" row); a new profile touches no released artefact until a request names it |

### 3.2 Reviewer registry (closes the "named qualified reviewer" gap)

Each entry: `reviewer_id`, `roles[]`, `qualifications[]` (kind, detail, verified_by, verified_on, expires_on), `families[]`, `levels[]`, `locales[]`, `conflicts[]`, `delegate_for[]`, `status` (active, suspended, revoked) and version. Rules [Recommendation, CE-36]:

- A family profile's `activation.named_reviewer_ids` must reference active registry entries with a matching role and qualification. The Resolver refuses a request for a family whose named reviewers are all unavailable.
- **Delegation.** Each gate role in an activated cell names a primary and should name a backup. The founder's H-SB cost approval may be delegated to a named delegate with a per-artefact budget cap recorded in the registry. The child-development reviewer for AC0 has no out-of-registry substitute: if no qualified child-development reviewer is available, AC0 work waits. There is no bypass.
- **Conflict of interest.** An author of a node cannot approve the gate that reviews that node. A Path A performer cannot be the GF approver of their own performance. ~~The same identity cannot approve twice on one artefact (existing RD-17 rule).~~ Within one gate, every required role is held by a distinct identity (for example GF: academic owner and production QA are two people). No identity approves a gate that covers a node, script, performance or render it authored. One identity may approve different gates on the same artefact. (Corrected 15 Oct 2026, as P3.)
- **Change class.** A qualification that lapses or is revoked is a revocation for approvals made under it after the lapse date. Approvals made while it was valid stay valid.
- **Signing keys and agent identities (level-1, 15 Oct 2026, CE-113).** Each entry carries `signing_keys[]` {ssh_ed25519_pub, valid_from, valid_to}; approvals are signed with them (§3.7). Agent and service identities (content agents, Kit tasks, the runner, CI bots) hold no reviewer role and no signing key, and GR refuses an entry that gives one a role. A CI rule rejects any commit by an agent identity that adds rows to `content/approvals/` (P1-16 "signed approvals and the agent-identity CI rule"). Adding or rotating a key is a routine update (Metadata row of §3.6); revoking a compromised key follows the scoped Revocation row for approvals signed with it after the compromise date.

### 3.3 Content Request

A request (`schemas/content_request.schema.json`) names: `competency_guids[]` (and optionally objective IDs), `format`, `level`, `subject`, `locale`, optional `exam_overlay` and `style`, optional `packaging_profiles[]` (R14), optional `variant` and `root_node_ids[]` (R4), `taught_level` (required for `level/educator` and refused otherwise; §5.1 step 2) (these four added 15 Oct 2026), `series` (`series_position`: first, subsequent or standalone, plus `series_id`), `flagship` (`value`, and when true, `set_by` and `reason`, set by the academic lead), `demo_kind` (real, virtual or none), `render_target` (video or audio_only), `requested_by` and `created_at`. It has `additionalProperties: false`. **It does not carry a subject family**; the Resolver derives the family (R3).

**Note, 15 Oct 2026 (level-3+, CE-119): `render_target: print`.** The `render_target` enum adds `print`: a tagged, accessible PDF/UA plus HTML rendered from the same Format Plan through the pinned Chrome print path, so `artefact_sha256` is stable. It is valid only for formats that list it: F-W Worksheet (ASM by objective, answer key as a separate file), F-TN Teacher Notes, F-GN Guardian Note (AC0) and the print render of Revision Sheet (`FORMAT_REGISTRY.md`). Gates are unchanged (GA-Δ on the text, GF on the rendered PDF); the packaging profile is `packaging/print-pdf`.

`series_position`, `flagship` and `demo_kind` are **editorial** fields that exist to resolve CE-L2 deterministically. They carry no commercial meaning and are exempt from the commercial-term lint (CE-25).

### 3.4 Resolver rules

The Resolver is a pure function `resolve(request, registry_snapshot, graph) → EPP | error`. Unversioned references resolve to the latest released version, and the pinned version is recorded. ~~Rules apply in order:~~ Rules are evaluated in this order: R2, R3, R1, R4, R5, R6, R7, R8, R9, R9a, R10, R11, R12, then R13 (if adopted) and R14. R1 keeps its number for CE-24 traceability but reads the safety class from R2 (corrected 15 Oct 2026: evaluated literally in number order, R1 would run before any safety class exists).

- **R1 Voice path (CE-L2, CE-24).** Path A if *any* of these holds: `format.voice_path_default = A` (Detailed, and the formats listed as A in the Format Registry); `series.series_position = first`; `flagship.value = true`; `demo_kind = real`; `safety_class = safety/ac0`; `level.voice_path_floor = A`; the resolved a11y profile is `a11y/isl` (CE-120; reason code `a11y_isl`, lead ruling 15 Oct 2026, CE-123); the locale has no voice that passed GL-voice for Path B. Otherwise Path B. The EPP records which conditions fired.
- **R2 Safety class.** Taken from the Level Profile only. Overlays, formats and styles can tighten safety rules but never change the class.
- **R3 Subject family.** Exactly one `family/*` entry must list the subject in `subjects[]`. None or more than one is a compile error. The family must be activated. The request level must be in the family's `levels_allowed`; otherwise compile error ("subject <s> resolves to family/<f>, not valid at level/<l>") (added 15 Oct 2026).
- **R4 Compatibility.** The format lists the level and the family; the level lists the format; the overlay (if any) is allowed by both the level and the format; the style supports the format's aspect and the safety class; the locale's locale gate has passed, and GL-glossary has passed for this family × locale or the request is flagged as the first artefact of the pair (GL-glossary then runs before GA-Δ).
  - *Variants and roots (15 Oct 2026).* If the format declares `format_variants`, `request.variant` is required and must name one; otherwise `request.variant` is a compile error. The effective `select.root` is the variant's, else the format's. If it is assessment_item, misconception, worked_item, claim, activity, story or text_passage, `request.root_node_ids` must name exactly one `expert_approved` node of that type inside the requested objectives; for claim_pair, exactly two CLM sharing `contrast_dimension`; for objective_set or member_artefacts, `root_node_ids` is a compile error. The EPP records `resolved.variant` and `resolved.root_node_ids`.
  - *Compositions (15 Oct 2026).* For `kind = composition`, aspect, resolution and duration come from the approved members. All members must share one aspect (mixed aspects are a compile error); duration is the sum of member durations.
  - *Single-language levels (15 Oct 2026).* If the level's `language.single_language_per_lesson` is true, the Locale Profile's `code_mix_policy` for that level must have pattern `none` or carry `approved_by` from a child-development reviewer; otherwise compile error "locale/<id> code-mixes at level/<id>". Until such an approval exists, `locale/hinglish` is refused at l1_2 and l3_5, and `locale/hi-in` at those levels uses Hindi-medium terms only (no Latin-script spans).
- **R5 Duration.** Intersection of the format duration (or its level variant) and the level ceiling; segment length is the minimum of format `max_segment_s` and level `attention.max_segment_s`. An empty intersection is a compile error, never a silent clamp. A locale whose narration runs longer than the budget produces a compile error routed to the spec owner; content is never silently cut.
  - *Level ceiling (15 Oct 2026).* The level ceiling is `level.attention.max_artefact_s`. If it is absent or its value is null (Cal), R5 uses the format duration unchanged and records provenance `level_ceiling: unset`. For l9_10 and l11_12 the seed value is unset (Inherited: no ceiling in 02/03 beyond chaptering).
  - *Compositions (15 Oct 2026).* For `kind = composition` the duration is the sum of the approved members' durations and the aspect is the members' shared aspect (R4).
  - *Uncalibrated values (15 Oct 2026).* A null `attention.max_segment_s` in the Level Profile is a compile error ("level/<id> max_segment_s not calibrated"). To run a pilot, the value owner publishes a pilot version of the Level Profile through GR with a provisional value tagged Hypothesis (owner, pilot_ref); Q-LEVEL stays report-only for it. A null pacing band is valid only as `teacher_set` when R1 resolves Path A (SCRIPTING §2, CE-71); a Path B artefact at a level whose `pacing.wpm_ordinary` is null is a compile error. Null `max_sentence_words`, `max_new_terms_per_scene` and `max_new_ideas_per_segment` never block compilation (Q-LEVEL report-only, SCRIPTING §5). The spec linter checks that provisional values satisfy l1_2 ≤ l3_5 ≤ l6_8 for `max_segment_s` (LEVEL_PROFILES §3.1 "shortest of all levels", §3.2 "≤ l6_8 value").
- **R6 Validators.** The union of family validators, format `qa_checks`, level, safety class, accessibility and locale checks.
- **R7 Gates.** The union of format gates, family gates (GV-claims; two reviewers for contested claims), level co-signers (child-development for AC0), safety requirements (a current G-COUNSEL record for the class must exist) and locale gates (GL-glossary, GL-voice). Nothing removes a gate.
- ~~**R8 Scalar precedence.** safety class > level > overlay > format > style > persona.~~ **R8 Scalar resolution** (corrected 15 Oct 2026; pure first-match precedence let a level's looser limit override a format's tighter one, against R5). (a) A limit is any field its schema marks `"x-kind": "limit"` (maxima such as max_segment_s, flash, motion, bed level and duration ceilings; minima such as hold times, contrast and think windows). A limit takes the most restrictive value across safety class, a11y profile, level, overlay, format, locale and style. A lower entry may tighten a limit but never loosen it. (b) Every other scalar takes the value of the highest entry in the order safety class > a11y profile > level > overlay > format > locale > style > persona. (c) Locale sets only surface fields (R9); persona sets no number (CE-16). Provenance records which entry set or tightened each value, so a reviewer can see why a Class 4 Recap is 90 s and human-voiced.
- **R9 Locale changes surface only.** Lexicon, script, register and voice. It never changes node selection or claims.
- **R9a Target locale for language subjects (15 Oct 2026).** For `family/languages_literature` the Resolver sets `target_locale` from the family's `subject_locales` and records it in the EPP and in the Script Spec language pair. When `target_locale` ≠ `locale`: R1 fires Path A unless both locales have a GL-voice-passed voice (target spans use the target-locale voice); R4 requires the locale gate of both locales; the lesson lexicon is core ∪ family for the medium plus `lex/languages_literature.<target>`; target spans carry `lang` with the target BCP-47 tag. A language subject with no registered locale is refused (SUBJECT_VALIDATION_PROFILES §5).
- **R10 Audio-only.** `render_target = audio_only` is allowed only if the format lists it and the accessibility check confirms that every `visual_essential` scene is fully narrated.
- **R11 Persona.** The level's persona; an overlay may supply a register variant (for example Exam Strategist). Safety and retired-expression rules are inherited, never relaxed.
- **R12 Kit cell.** Selected by (format family × subject family × level band). A Kit for a Class 4 story cannot be used for a UG derivation.
- **R13 Voice entry (15 Oct 2026).** After R1 the Resolver runs VOICE §1 selection steps 1–3; no candidate is a compile error. The EPP pins the identity voice: the `B_tts` voice, the `A_conversion_target` brand voice, or the `A_direct_release` performer voice. For Path A with STS, the performer source voice (`A_performance_source`) is pinned in the narration record at S9, which enters `closure_hash`.
- **R14 Packaging (15 Oct 2026).** Use the request's `packaging_profiles`, or else the format's default profiles from PACKAGING §2.2. Each profile must list the format in `formats_allowed`, the EPP safety class in `safety_classes_allowed`, the format aspect in `aspects_accepted`, and the render target. A requested profile that fails is a compile error; a default that fails is dropped, with provenance; an empty result is a compile error. The EPP pins the bytes half of each profile (`packaging/<id>@x.y.z#render`) and lists the bytes variants it requires (burned captions); the distribution half stays in the PKG record. The master is rendered to the bytes half of `packaging/in-app-player`; each other selected profile whose bytes half differs yields a variant. An unmeasured profile may be pinned, but A4 and RELEASE-CHECK block its release (walkthrough-12, merged 15 Oct 2026; end card removed from the bytes half by packaging-08). Each delivered variant gets the review set by the CE-14 lead ruling (PACKAGING §15 item 5), and until then its own GF/GS per PACKAGING §1. The distribution half is pinned later in the Distribution Package record. (R13 is reserved for the voice-selection rule.)

### 3.5 Effective Production Profile (EPP)

~~`EPP = {request, pins{every registry entry@version: sha256}, resolved{voice_path, safety_class, persona, family, duration, segment, validators[], gates[], reviewers[], kit_cell, aspect, resolution, render_target, …}, provenance{field: entry}}`. `epp_hash = sha256(JCS(NFC(EPP)))`.~~ Corrected 15 Oct 2026: the field list is closed (no "…"), named reviewers leave the EPP, and the pipeline code versions enter it. Validated by `schemas/epp.schema.json`:

`EPP = {epp_version, hash_canon: "JCS-RFC8785+NFC", resolver_version, toolchain{format_compiler_version, closure_checker_version, qa_resolve_version, validator_versions{validator_id: semver}}, request, pins{every registry entry@version[#variant]: sha256}, resolved{voice_path, voice_path_reasons[], safety_class, level, taught_level?, format, variant?, root_node_ids[]?, family, locale, target_locale?, style[], overlay?, persona (persona/<id>@x.y.z#<variant>), register_overlay?, a11y, duration_s{min, max}, segment_max_s, validators[], gates[], reviewer_requirements[]{gate, role, qualification, family, level, locale, count}, kit_cell, aspect, resolution, render_target, packaging_profiles[]}, provenance{field: entry}}`.

`epp_hash = sha256(JCS(NFC(EPP)))`, computed over the EPP with `request.request_id`, `request.requested_by` and `request.created_at` removed; those fields live in the job manifest, so two identical requests produce one epp_hash and share cached stages. The EPP is complete at S5: nothing is added to it afterwards (music placement goes to the cue sheet and `bed_meta.json`, narration to the narration record), so epp_hash and the approvals that bind it stay valid (15 Oct 2026). Authors, Kit tasks, judges, validators and reviewers read only the EPP.

**Required pins (15 Oct 2026).** format, level, safety, family, locale, a11y, persona (with `#variant`), voice (R13), `lex/core.<locale>` plus `lex/<family>.<locale>` where one is registered, `qa/catalogue`, model (one per cascade rung of the Kit cell), kit, harness and every slot used; at least one style when `render_target = video`; at least one packaging profile (R14); overlay when the request names one; ~~`music/` is not pinned here (it is pinned in the cue sheet)~~ every candidate `music/` entry (logo variants, format-admissible beds, level-filtered SFX palette) when the artefact has audio (selected at S5; MUSIC §2.1 item 4; corrected 15 Oct 2026). `gs/` is not pinned (recorded on the voice entry), nor `reviewer/`.

**Reviewers (15 Oct 2026).** The EPP states reviewer *requirements*, never named reviewers. Who approved is bound on the approval record (`reviewer_id`, `reviewer_pin`, §3.7), so a routine reviewer-entry update changes no epp_hash (§3.6, Metadata row).

**Toolchain (15 Oct 2026).** The resolver, format compiler, closure checker, `qa_resolve` and validator versions shape the output as much as the inputs do, so they are inside epp_hash. A change to any of them is the pipeline-code row of §3.6.

**Set order (15 Oct 2026).** JCS keeps array order, so writers of hash-bound records emit set-valued arrays in canonical order. EPP `resolved.validators[]`, `gates[]`, `reviewer_requirements[]` and `voice_path_reasons[]` are sorted by Unicode code point. QA Profile `checks[]` are sorted by `check_id` and `gates[]` by `gate`. `binding.approvals[]` are sorted by `approval_id`. All other arrays keep their meaningful order (beats, sentences, grammar, slot instances, interactions, chapters, composition members, description_order, mode_order_slow_to_fast, prompt_sentence_ids). Registry entries are hashed as authored (§3.1).

The **Format Plan** (§5.1 steps 4–6) validates against `schemas/format_plan.schema.json` (15 Oct 2026).

### 3.6 Change classes and invalidation (CE-L10 made operational)

Registry entries are immutable; a change is a new version. On release of any new version, the **dependency index** (a reverse map from every pin and node hash to the artefacts and approvals whose closure contains it) computes the affected set. Every affected approval moves from `valid` to `stale` and **every affected artefact is queued for re-QA**. That is CE-L10 taken literally. What re-QA means depends on the change class. **Auto re-affirmation** is allowed only when re-derivation produces identical artefact bytes and all automated checks pass. "Bytes" means `script_content_sha256` and `interaction_spec_content_sha256` for scripts, and `artefact_sha256` for rendered files, never the hash of a whole record (15 Oct 2026). It is recorded on the approval as a re-QA record (`state: reaffirmed`, with the new closure hash and the check results). A human gate reopens whenever bytes change or the class requires human judgement. A **revocation** (defect, licence withdrawal, retracted source, lapsed qualification, safety breach) blocks release and withdraws published artefacts until re-approved.

**Re-resolution (15 Oct 2026).** The dependency index keys on entry id (`kind/id`). When X@n+1 is released, every artefact that pins an earlier version of X is re-resolved with X replaced by X@n+1, whether or not its request named a version. A version in a request is only for reproducing a past build; RELEASE-CHECK refuses an EPP that pins a superseded version unless the GR record of the newer version lists the older one as still releasable.

Published artefacts stay published while `stale` and in the queue, unless the class is revocation or safety-tightening with a failing check.

| Changed entry | Class | Automated re-QA | Human gates reopened | Published artefacts |
|---|---|---|---|---|
| Graph node (CLM, CON, ANL, MIS, WRK, ASM, SIM, ACT, STY, VOC, TXT) | Semantic | Recompile; closure, fixtures, ledger, all A-checks | GV-claims (for a changed CLM), GA-Graph (that subtree), then GA-Δ, H-SB if storyboard changes, VOICE if narration regenerates, GF/GS, DISCLOSURE (GV-claims and VOICE added 15 Oct 2026) | Stale; revoked if the old node was wrong (errata, RD-31) |
| REN rendering | Locale | Locale checks, lexicon, captions | GA-Δ for that locale, GF/GS for that locale | Stale (that locale only) |
| SRC new edition | Semantic | Span-hash re-check of every citing claim | GV-claims where a span changed or vanished, then as graph node | Stale |
| SRC retraction | Revocation | — | GV-claims for citing claims | Blocked and withdrawn |
| ~~Curriculum framework~~ (replaced 15 Oct 2026 by the five framework-diff rows below, CE-116) | ~~Metadata~~ | ~~Re-export metadata, coverage check~~ | ~~H-CG; content gates only if the objective set changes~~ | ~~Stale (metadata re-export)~~ |
| Curriculum framework: item text or metadata edited (level-2, 15 Oct 2026, CE-116) | Metadata | Re-export metadata, coverage check | H-CG (framework version) | Stale (metadata re-export) |
| Curriculum framework: item moved to another class or unit (level-2, CE-116) | Metadata | Sidecar re-export, coverage check | H-CG | Stale (sidecar re-export) |
| Curriculum framework: item removed (level-2, CE-116) | Semantic | Coverage check; list every artefact whose sidecar lists only removed GUIDs | H-CG; content gates for any artefact re-scoped | Relabelled "Not in <board> <year> syllabus" or unlisted for that framework edition; never silently kept |
| Curriculum framework: item added (level-2, CE-116) | Metadata | Coverage-gap row; no invalidation | H-CG (framework version) | Unaffected |
| Curriculum framework: depth or outcome changed (level-2, CE-116) | Semantic | Recompile the affected subtree | H-CG, then GA-Graph for the subtree and the graph-node gates above | Stale |
| Format Spec | Structural | Recompile; if the Format Plan hash is unchanged, auto re-affirm | GA-Δ, H-SB, GF/GS if bytes change | Stale |
| Slot type (code) | Structural | Slot tests and golden renders, recompile users | As Format Spec | Stale |
| Pipeline code (resolver, format compiler, closure checker, qa_resolve, validators) (added 15 Oct 2026) | Structural | Recompile and re-validate every artefact compiled with the old version; auto re-affirm when format_plan_sha256, script_content_sha256 and artefact_sha256 are unchanged and all checks pass | As Format Spec | Stale |
| Level Profile, safety fields (safety class, motion/flash, voice floor, reviewers) | Safety | Full automated suite under the new limits | Child-development or academic re-sign where the reviewer set changed; GF/GS if bytes change | Failing artefacts revoked; passing ones re-affirmed |
| Level Profile, non-safety fields (pacing, register, density, interaction) | Pedagogical | Recompile, level linters | GA-Δ and GF/GS if bytes change | Stale |
| Safety class | Safety | As above for every level using it | G-COUNSEL re-record if rules loosen (tightening needs none); re-sign as above | Failing artefacts revoked |
| Accessibility profile | Safety | a11y suite | GF/GS if bytes change | Failing artefacts revoked |
| Persona register | Pedagogical | Persona linter; regenerate scripts only on request | GA-Δ and GF/GS if scripts regenerate | Stale |
| Exam overlay | Semantic | Pattern recompute, expiry check | GA-Δ for exam slots, GF/GS | Stale; revoked if a pattern claim is wrong |
| Subject-family profile | Validation | Re-run validators on affected claims | GV-claims for claims that fail the new rule | Stale; failing artefacts revoked |
| Locale lexicon or glossary | Locale/narration | Lexicon check, critical-term listening (ASR) | VOICE gate if audio regenerates; GF/GS | Stale |
| Locale other fields (fonts, direction, shaping) | Presentational | Re-render, render-text checks | GF/GS if bytes change | Stale |
| Style | Presentational; Safety when the diff touches `safety_classes_allowed`, `motion.by_safety_class`, `flash` or `asset_sources_allowed` (VISUAL §11; loosening needs G-COUNSEL as this section states; 15 Oct 2026) | Re-render, A-suite, flash, a11y | H-SB only if the layout grid changes; GF/GS | Stale |
| Voice new version (for example new disclosure text) | Narration/disclosure | Disclosure check, re-mux | DISCLOSURE; VOICE + GF/GS if audio regenerates | Stale |
| Voice licence revoked | Revocation | — | Re-voice, VOICE, GF/GS, DISCLOSURE | Blocked and withdrawn |
| ModelProfile, Kit, cascade policy | Production | Kit regression on the frozen eval set for every affected Kit cell, plus automated QA on affected artefacts; result recorded on each approval | None unless re-derivation is requested and bytes change; in-flight unapproved work restarts at the affected stage | Stale, then re-affirmed when checks pass |
| Harness, container, fonts, Chrome, FFmpeg, HarfBuzz | Render toolchain | Re-render from the stored closure; compare bytes | None if bytes are identical; GF/GS if they differ | Stale, then re-affirmed or re-reviewed |
| Reviewer qualification lapse or revocation | Revocation (scoped) | — | The gates signed after the lapse, by another qualified reviewer | Blocked if signed after the lapse |
| Reviewer entry routine update (renewed qualification, new locale, changed delegate) (added 15 Oct 2026) | Metadata | None; the EPP holds reviewer requirements only and each approval keeps its own `reviewer_pin` | None | Unaffected |
| Ledger or budget policy (`budget/`) | Metadata | None | None | Unaffected |

**Impact preview.** GR shows "this change re-opens N approvals across M artefacts, with K human gate-minutes estimated" before merge, so invalidation storms are visible and scheduled, not accidental [Recommendation].

**Framework editions (level-2, 15 Oct 2026, CE-116).** The framework diff is computed per GUID (§2.6 minting rule). A framework version carries `valid_academic_years[]`, and an artefact stays releasable for every edition still inside its window, so repeaters and supplementary-exam learners on an older edition keep their content. For a framework change, the GR impact preview also lists the removed and changed GUIDs with the artefact count for each.

**Exam-window freeze (level-3+, 15 Oct 2026, CE-122).** Overlay entries and frameworks carry `exam_windows[]` {name, start, end} as data (no new registry kind). Inside any window that touches a change's affected set, GR releases only Revocation, Safety-tightening and S1 incident fixes (§9.6). Every other change queues, and the impact preview shows the deferral date. Surge playbook [Recommendation]: at T-10 weeks, plan and gate Recap, Revision Sheet, Practice Set and Paper Walkthrough for the in-window competencies so the window needs no new GA-Graph work; confirm the reviewer rota with backups for the window; forecast gate-minutes against the rota in the ledger capacity lines; staff on-call (§9.6) for the whole window.

### 3.7 Approval record

`{approval_id, gate, artefact_sha256 (GF/GS), epp_hash, graph_subtree_sha256, closure_hash, bound{…}, reviewer_id, ~~reviewer_registry_version~~ reviewer_pin (reviewer/<id>@x.y.z), role, decision, full_video_watched (boolean; required true for role production_qa on GF/GS, 07/06 §6.1), notes, waivers[] {check_id, finding_sha256, reason, reviewer_id, role, artefact_sha256, catalogue_pin} (QA_PROFILES_REGISTRY §1.1), timestamp, state (valid | stale | reaffirmed | revoked), reqa_records[], signature}` (full_video_watched and waivers[] added 15 Oct 2026; signature added 15 Oct 2026, CE-113), validated by `schemas/approval_record.schema.json` (record and reviewer pin corrected 15 Oct 2026). The approval service is the only writer.

**Approval signature (level-1, 15 Oct 2026, CE-113).** `signature` is an SSH signature (namespace `examleaf-approval`) over JCS(record minus signature), with the NFC normalisation of §2.5 and with `state` and `reqa_records` taken as at signing (`valid` and `[]`) so later re-QA writes do not break it (as `approval_record.schema.json` states; aligned by the critic-pass verifier 15 Oct 2026), made with a key from the reviewer's `signing_keys[]` (§3.2). Lead ruling 15 Oct 2026 (CE-123): the signature is required on every human gate (H_CG, GV_CLAIMS, GA_GRAPH, GA_DELTA, H_SB, VOICE, GF, GS, COPY, DISCLOSURE, G_COUNSEL, GL_GLOSSARY, GL_VOICE); only the machine gates A_SUITE and RELEASE_CHECK are unsigned. RELEASE-CHECK verifies every approval with `ssh-keygen -Y verify` against the key of the entry named by `reviewer_pin` whose `valid_from`–`valid_to` window contains the record's `timestamp`. An unsigned or mis-signed row counts as absent. Schema change in `approval_record.schema.json` (P1-16).

**Closure manifest (corrected 15 Oct 2026).** ~~`closure_hash = sha256(JCS(sorted input hashes + registry pins + harness pins))`~~ (the inputs were never enumerated and the parts had no JSON structure). `closure_hash = sha256(JCS(NFC(M)))`. The closure manifest M has these keys: `epp_hash`; `graph_subtree_sha256`; `format_plan_sha256`; `script_content_sha256` {locale: …}; `interaction_spec_content_sha256`; `storyboard_sha256`; `fill_output_sha256` [sorted; every stored Kit or model fill, S6 and S10]; `fixture_output_sha256` [sorted]; `narration_audio_sha256` [sorted]; `cue_sheet_sha256` (which carries the music stem and file hashes); `artefact_sha256` {role: …} for the master and every delivered variant. Registry pins, including `harness/`, enter only through `epp_hash`. An approval records the closure of the keys that exist at its gate's stage. Note, 15 Oct 2026: for GA-Δ the bound input hashes are the Script Spec `script_content_sha256` and the Interaction Spec `interaction_spec_content_sha256` (not their record `sha256` values; resolver-07 supersedes the interaction-02 wording). Each gate's bound object is listed in QA_PROFILES_REGISTRY §4.1 and in the per-gate table below; the record's `bound` holds that object's hash (`artefact_sha256` itself is set for GF/GS and DISCLOSURE, where the bound object is the delivered file), and its `closure_hash` is the closure of the inputs that exist at the gate's stage (15 Oct 2026). RELEASE-CHECK recomputes every key from the current records. It refuses release if a key recorded on an approval has changed with no reaffirmed re-QA record, or if any pin is revoked. Q-DET re-renders from M.

**Per-gate binding (15 Oct 2026).** Each approval also binds, in `bound`, the hashes its gate actually reviewed (QA_PROFILES §4.1 `bound_to`):

| Gate | Binds |
|---|---|
| H-CG | `framework_version` |
| GV-claims | `claim_sha256` of every claim reviewed (its span hashes are inside the claim) |
| GA-Graph | `graph_subtree_sha256` |
| GA-Δ | ~~`script_bundle_sha256` (the Script Spec content for every locale in scope)~~ `script_content_sha256` per locale in scope and `interaction_spec_content_sha256` (content hashes, never a whole-record hash; corrected 15 Oct 2026) |
| H-SB | `storyboard_sha256` (grid, beats, cue intent, estimate, fixture, style and hero hashes; RD-46, 07/03) |
| VOICE | `voice_version` and `narration_audio_sha256` |
| GF / GS | `artefact_sha256` of the master and every delivered variant |
| DISCLOSURE | ~~`export_record_sha256` (the Distribution Package `PKG-<id>`, S14)~~ the delivered file `artefact_sha256`, the voice pin (`voice_version`) and `disclosure_text_sha256` (S12; corrected 15 Oct 2026, PACKAGING §1) |
| COPY | `copy_sha256` per locale (S12; added 15 Oct 2026) |
| RELEASE-CHECK | `closure_hash` |

An approval goes stale only when a key in its own `bound` set, or a closure key that existed at its stage, changes; a later-stage key (audio, cue sheet, artefact) never makes an earlier approval stale. A script edit therefore makes GA-Δ stale through `script_content_sha256`, and H-SB binds the storyboard hash rather than `format_plan_sha256` alone.

**Release check.** ~~The release check (07/06 §6) recomputes the closure from the current artefact record and refuses release if any pin is revoked, any approval is stale or revoked, or the closure differs.~~ The release check (07/06 §6) recomputes the closure manifest from the current records and refuses release if any pin is revoked, any approval is stale or revoked, or a key recorded on an approval has changed with no reaffirmed re-QA record (corrected 15 Oct 2026: an S7 approval cannot bind keys that only exist after S9). RELEASE-CHECK also refuses release unless every human gate_requirement in the artefact's QA Profile (`qa_profile_sha256`, pinned in the EPP) is met in the approval store: at least `count` approvals per listed role, in state valid or reaffirmed, bound to every hash named in `bound_to`, from distinct reviewer identities, none of whom authored the covered node, script or render (QA §3 rule 9). GF/GS needs academic_subject and production_qa from two identities. At `safety/ac0`, GA_DELTA, H_SB and GF/GS each carry a child_development co-sign. Every record named in the profile's preconditions (`g_counsel_record_ref`, `gl_voice_record_ref`, `gl_glossary_record_ref`) must be current. ~~DISCLOSURE binds to the export record, so the publish step checks it by the same rule before upload (07/06 §6.4; §4, S14).~~ DISCLOSURE and COPY are approved at S12 and checked here at S13; no approval is added after S13. Platform flags are recorded per channel in the publish receipt that Q-DISC.placement reads before the item is public (§4 Publish row; corrected 15 Oct 2026).

---

## 4. Pipeline stages v2

The stages keep 07's order and skills. Each stage is an idempotent job keyed by its input hash; a cache hit is free. Jobs are file manifests run by a small runner (CE-58); there is no workflow engine at levels 0–3.

| # | Stage | Input → output | Gate after stage | Owner (skills/sections) |
|---|---|---|---|---|
| S1 | **Ingest** | Source documents → SRC records (copy hash, locators, rights) + native text | — | `examleaf-source-ingest` (04); rights from H-S2 |
| S2 | **Curriculum map** | Framework files + scope → selected item GUIDs, prerequisite edges | **H-CG** | `examleaf-curriculum-map` (04), extended with `cg-import` |
| S3 | **Claim ledger** | SRC + scope → CLM nodes with source spans; flagger marks needs-citation sentences [N43]; span-hash verify; family validators (fixtures, solvers, date/name consistency) | **GV-claims** (family-qualified; two reviewers for contested claims) | `examleaf-claim-research` (04); new `claim-ledger`, `citation-flag`, `span-verify`; `examleaf-science-*` (STEM) |
| S4 | **Lesson Graph** | Approved claims → OBJ, CON, ANL, MIS, WRK, ASM, SIM, ACT, STY, VOC, TXT, MED nodes. Strong model offline as compiler (CE-L6); humans edit. Misconceptions authored first [N73] | **GA-Graph** (binds `graph_subtree_sha256`) | `examleaf-lesson-plan` (04) becomes `graph-author`; `examleaf-lesson-architect` as review lens; `examleaf-analogy-auditor` for ANL |
| S5 | **Format derivation** | Request + registry + graph → EPP → **Format Plan** (chapters, slots bound to node IDs, duration budget, provenance) | Compile errors only | new `profile-resolver`, `format-compiler`; absorbs `examleaf-reel-repurpose` logic |
| S6 | **Script per format** | Format Plan → scripts per slot via Kit + cascade (Haiku→Sonnet→Opus per scene); every sentence tagged with node IDs; NarrationPlan draft | — | `examleaf-super-teacher` → `examleaf-super-teacher-scriptwriter` → `examleaf-dialogue-naturalizer` (05); `examleaf-interaction-design`; Kit (13) |
| S7 | **Validation per family + level** | Script → closure check (no claim outside the approved set; no new numbers, dates or names), fixture recompute, ledger coverage, level/density/persona/safety linters, lexicon check | **GA-Δ** (full script read, derived surface highlighted; child-development co-sign for AC0; native editor for each locale) | `examleaf-science-*`, `examleaf-science-reviewer`, `examleaf-confidence-editor`; new `closure-check`, `level-lint`, `persona-lint`, `safety-lint` |
| S8 | **Storyboard gate** | Grid, beats, cue intent, token/credit/minute estimate; budget reserved | **H-SB** (founder or delegate for cost, academic lead for fit; two identities; RD-46) | `examleaf-storyboard-route`, `examleaf-anim-storyboard-gate`, `examleaf-effort-governor` |
| S9 | **Narration** | Path A (teacher performance → STS into licensed brand voice) or Path B (directed TTS through the Kit with per-beat direction); sample-accurate timeline; −16 LUFS; protected pauses | **VOICE** (voice gate + critical-term listening) | 05 skills: `examleaf-voice-direction`, `examleaf-voice-acting-director`, `examleaf-pacing-controller`, `examleaf-stem-pronunciation`, `examleaf-multilingual-director`, `examleaf-tts-provider-adapter`, `examleaf-audio-production-engineer`; 11 playbook |
| S10 | **Animation and composition** | Cue sheet from measured narration; scene authoring (SVG, procedural 2D, kinetic type, Three.js) through the seek-deterministic harness; FFmpeg assembly at the EPP resolution | — | `examleaf-cue-sheet`, `examleaf-motion-harness`, `examleaf-svg-scenes`, `examleaf-procedural-2d`, `examleaf-kinetic-typography`, `examleaf-vertical-adapt`, `examleaf-render-batch`; 04 assembler |
| S11 | **QA (automated, 100%)** | A1–A17 + Q-checks (§9.1) on script, cue sheet, frames and audio | Blocking per CE-35 | `examleaf-visual-qa`, `examleaf-anim-qa`, `examleaf-audio-caption-qa`, `examleaf-narration-quality-reviewer`; new `flash-analyser`, `a11y-check` |
| S12 | **Approvals** | Full watch; title, cover, description and hashtags (copy string table) | **GF** (long formats) / **GS** (Shorts), level co-signs; Q-DISC content checks (disclosure record matches voice path and locale); **COPY** (the GF/GS pair on `copy_sha256`); **DISCLOSURE** (RD-45; S12, publisher identity) binds each delivered file's SHA-256 with the voice pin and the disclosure text hash; RELEASE-CHECK requires it. ~~moved to S14 (15 Oct 2026)~~ *(15 Oct 2026, stitch: the walkthrough-06 move of DISCLOSURE to S14 is reversed in favour of the packaging and resolver findings, because a DISCLOSURE bound to the PKG hash would sit inside the PKG it binds.)* | `examleaf-release-review`; `examleaf-thumbnail-package` (moved from S14); approval service |
| S13 | **Release check** | Recompute closure; confirm no stale or revoked pins; every QA-Profile gate requirement met (§3.7) | **RELEASE-CHECK (content)** | approval service |
| S14 | **Export** | Media + sidecar with neutral metadata, provenance block (contributors, sources, last revision date [N60]), captions, transcript, audio-description track when required, disclosure, `export/interactions.json` | ~~**DISCLOSURE** (RD-45; publisher confirms each platform placement on the Distribution Package `PKG-<id>`, bound to `export_record_sha256`), then **RELEASE-CHECK (publish)**: recompute the closure plus the PKG hash; nothing is uploaded until both pass (15 Oct 2026; was "—")~~ Export checks (PACKAGING §11); no approval is added after S13 (corrected 15 Oct 2026) | `examleaf-packaging-export` (neutral exporter) |
| Publish | **Publish** (unnumbered; 15 Oct 2026) | Publisher sets platform flags in the upload flow before the item is public and writes `content/packages/PKG-<id>.publish.<channel>.json`; Q-DISC.placement reads it | Upload refused without a passing record | Publisher identity |

Cross-cutting: `examleaf-observability-cost` and `examleaf-cost-regeneration-optimizer` (ledger, S1–S14); `examleaf-learning-evaluation` (pre/post items); `examleaf-skills-security` (skill admission, 07/07); new `impact-analyser` (GR) and `v1-import` (migration).

**Never skipped:** GA-Δ, H-SB, A-suite, GF or GS, DISCLOSURE and RELEASE-CHECK apply to every format, primary or derived. The Format Spec schema refuses a spec that omits them (CE-08, CE-13, CE-14).

**Why GA-Graph plus GA-Δ.** Review minutes are the throughput constraint (RD-41: 85 min per lesson as a capacity metric). Approving the graph once and reviewing each derived script with its *derived surface* highlighted (wording, every SIM and ANL used, interaction prompts and the sentence-to-node map) makes review grow with new surface rather than with format count. **[Hypothesis]** GA-Δ for a Recap or Short takes a fraction of a full GA. M3 times it. To prevent under-review, GA-Δ reviewers read the *whole* script, not only the diff, and a second reviewer audits a sample of GA-Δ decisions during pilots. GF/GS full watch is never reduced, because render, voice and sync defects are per artefact.

---

## 5. Format derivation engine

### 5.1 Algorithm

1. **Resolve** the EPP (§3.4). Errors stop here, for example "Question Analysis is not defined for level/l1_2".
2. **Select** the sub-graph with `format.select` (root kind plus include selectors over node types and fields such as `CLM[key=true]`, `MIS[priority<=2]`, `SIM[permitted_levels∋level]`, `ANL[permitted_levels∋level]`). Only `expert_approved` nodes are eligible. SIM and ANL nodes are filtered by `permitted_levels`, so a simplification approved for Class 6–8 is invisible to a Class 4 request. For `format/teacher_explainer` the SIM/ANL filter uses the request `taught_level` (15 Oct 2026).
3. **Check requirements** from `node_requirements_by_level`. Example: Detailed requires ≥1 WRK per objective for `level/l6_8` and above, and ≥1 ACT or STY per objective for `level/l1_2` and `level/l3_5`. A missing requirement is a compile error naming the gap ("OBJ-ohm1 has no worked item"), which goes back to graph authoring.
4. **Lay out the grammar** (the level variant if one matches, else the default) using only registered slot types. Expand `repeat` (per objective, per step, per item).
5. **Budget.** Apply the R5 duration intersection; split into chapters of at most `max_segment_s` (≤360 s by schema [N3][N28]); place `check.interpolated` between chapters when the spec requires it [N30] (contested evidence) and protected think windows (RD-11).
6. **Bind and hash.** Each slot instance gets node IDs and parameters. The result is a **Format Plan** with `format_plan_sha256`. The same inputs always give the same Format Plan hash.
7. **Fill** slots through Kit templates (one Kit skill per slot type), cascading per scene. Every output sentence carries `node_ids[]` and is stored by hash.
8. **Closure check (CE-12).** Every assertive sentence (flagged by the claim flagger) must map to ≥1 approved CLM, SIM, WRK step or ASM in the Format Plan. Numbers, dates, names and units in a sentence must appear in a referenced node or a fixture output. Derived formats may not introduce node types (schema: `may_introduce_node_types` is empty when `kind = derived`). Primary formats may introduce nodes only through S4 and GA-Graph, never at S6.
9. **Emit** the compiled v1 contracts: LessonPlan (now a compiled view whose `class_level` is replaced by `level_ref`), SceneSpec (with `kind` decoupled from subject; RD-35 retired), NarrationPlan, cue-sheet inputs and ShortSpec where applicable.

### 5.2 Slot vocabulary (v1, closed)

`hook.realworld`, `hook.question_reveal`, `hook.surprise`, `explain.ladder_step`, `explain.definition`, `explain.analogy`, `explain.derivation_step`, `worked.step`, `worked.faded_twin`, `check.interpolated`, `check.predict`, `check.retrieval`, `misconception.elicit`, `misconception.confront`, `misconception.retest`, `recap.retrieval`, `recap.statement`, `marking.scheme`, `exam.pattern`, `exam.time_plan`, `compare.dimension`, `activity.setup`, `activity.do`, `activity.observe`, `activity.safety_cue`, `story.beat`, `story.song_chant`, `card.front`, `card.back`, `qa.doubt_statement`, `qa.answer`, `source.show`, `source.read`, `source.interpret`, `perspective.position`, `map.node`, `map.link`, `viva.prompt`, `viva.model_answer`, `teach.move`, `bridge.return_link`, `chapter.title`, `close.next_step`. That is 43 slot types.

Every slot type has a code module, unit tests, a Kit template, an A-check and an owner. Adding one requires a decision record (ADR). The KPI is the share of new formats shipped with zero new slot types; a quarterly review merges near-duplicates (CE-07). Each slot type has exactly one slot owner (SKILLS_and_KIT_MAP_v2 §4). manim-scenes, procedural-2d, asset-library, molecule-, biology- and threejs-scenes may be alternate renderers for a slot instance but never own its module, tests, Kit template or A-check (added 15 Oct 2026).

### 5.3 Spec linter (CE-08)

The linter runs in CI over every Format Spec:

- **Schema.** Every spec validates against `schemas/format_spec.schema.json`. The schema already enforces mandatory gates, `check_answer_hidden: true`, `think_window_protected: true`, segment ≤360 s, 16:9 only for ug/pg/adult_prof, and no new node types for derived formats.
- **Vocabulary.** Every slot exists in `slot/`.
- **Satisfiability.** The selector and requirements can be met on the golden graph set (10 pilots plus the 54 frozen scene packages from 13 §3.2 as seed fixtures) for every allowed level.
- **Non-weakening.** A spec cannot drop below any family validation floor or level safety floor, omit disclosure, or list a level whose `formats_allowed` excludes it.
- **Determinism.** Compiling twice gives the same Format Plan hash.

### 5.4 How one graph yields each format

Full specifications are in the Format Registry. Beat grammar: FORMAT_REGISTRY.md (owner). (15 Oct 2026: the "Grammar core" column that used to sit in this table was a drifting second copy and is removed.) In summary:

| Format | Kind | Selects | Voice | Aspect |
|---|---|---|---|---|
| Detailed | primary | Whole objective set; every MIS; ≥1 WRK per objective (L6+) or ≥1 ACT/STY (L1–5) | A | 9:16 |
| Simplified | derived | Core objectives; SIM nodes permitted at the level replace their claims; one ANL; one WRK | B | 9:16 |
| Recap | derived | `CLM[key=true]` per objective + top MIS by priority | B | 9:16 |
| Question Analysis | primary | One ASM (exam tags when sourced) + linked WRK + MIS | B | 9:16 |
| Shorts | derived | One complete unit: one key claim, one MIS + confronting claim, or one WRK step | B | 9:16 |
| Worked Example | primary | One WRK + its `twin_of` faded twin | B | 9:16 |
| Misconception Fix | derived | One MIS with `diagnostic_item` + confronting claims | B | 9:16 |
| Concept Intro | derived | CON rung 1–2 + real-life hook + one ANL | B | 9:16 |
| Exam Strategy | primary | exam_pattern claims (time-bound) + ASM with exam tags; overlay required | B | 9:16 |
| Revision Sheet | derived | `CLM[key=true]` across a chapter + VOC | B | 9:16 |
| Flashcard Reel | derived | One key CLM, VOC or formula claim | B | 9:16 |
| Lab/Demo | primary | ACT + safety and observation claims | A if `demo_kind = real`, else B | 9:16 |
| Comparison | derived | Claim pair sharing `contrast_dimension` | B | 9:16 |
| Story/History | primary | STY (Class 1–5 story or song) or a narrative chain of historical/biographical claims | A for AC0, else B | 9:16 |
| Q&A/Doubt | primary | A recurring doubt recorded as MIS or ASM + answering claims | B | 9:16 |
| Series/Course | composition | Approved member artefacts | inherits members | members' |

Plus Practice Set, Prerequisite Repair, Derivation/Proof, Lecture Segment (16:9), Source Analysis, Perspectives, Read-Along, Concept Map, Viva Prep and Teacher Explainer: 26 registered formats in total. Two Series configurations, **Paper Walkthrough** (Question Analysis members in paper order) and **Chapter One-Shot** (Detailed chapters + Recap + Practice Set rendered as one file with chapter markers), cover the PYQ-paper and marathon products without new formats. Audio-only output is a render target, not a format (R10).

**Shorts are not a separate procedure.** The 07/05 SH1–SH8 rules become `format/short` with variants (concept, misconception, trap). "Recompose, never crop" becomes a compiler invariant: a Short is laid out at 1080×1920 from nodes, never cut from a Detailed render.

**Speaking rate.** Format Specs carry no WPM numbers. Pacing comes from the Level Profile. The evidence that faster speech raises engagement is contested and comes from MOOC proxies ([N6][N29][N1]), so 03's audition targets remain the defaults and faster bands are tested only in the 11 A/B programme (CE-16).

---

## 6. Level adaptation

Details are in the Level Profiles document. Architecture-level rules:

- **Ten Level Profiles**: l1_2 (Classes 1–2), l3_5 (3–5, Preparatory [N8]), l6_8 (Middle [N32]), l9_10, l11_12, ug, pg, adult_prof, voc (NSQF-aligned vocational, ITI and polytechnic), educator. **Exam overlays** sit on a base level and never change its safety class.
- **Audience safety classes (CE-17).** AC0 = Classes 1–5 (child-directed, CE-L9). AC1 = Classes 6–12, UG (every year) and vocational, because India's data-protection law treats under-18s as children and UG and vocational cohorts include minors (CE-18). AC2 = PG, adult professional and educator. **level/ug always applies AC1 content rules**, so resolution is deterministic and max-restrictive.
- **Personas** inherit the 03 core (scaffolding over charisma, calibrated confidence, never fabricating the student's response, a humour ceiling rather than a quota). The variants are Super Teacher Junior (l1_2, l3_5), Super Teacher Coach (l6_8), Super Teacher (l9_10, current), Super Teacher Mentor (l11_12), Lecturer (ug), Seminar Lead (pg), Exam Strategist (overlay register), Skills Instructor (voc) and Colleague (educator). A persona linter checks retired expressions and register rules to stop cheap-model drift.
- **Pacing and density.** Values for l9_10 and l11_12 are inherited from 02 §G2 and §B3 and 03 audition targets. Every value for l1_2 to l6_8 starts as **[Hypothesis]** with an owner and pilot, because the evidence is adult MOOC data ([N1], [N2], [N26]–[N31]). The 6-minute evidence is a ceiling for adults, not a target for children.
- **Interaction.** The interaction loop "redesigned for teenagers" (03) stays at l9_10 and l11_12. Lower levels get say-aloud, point, move, draw and sing modes [N10]; Middle Stage gets predict-explain-check and reasoning prompts [N37][N55]; UG/PG gets interpolated questions and critique.
- **Safety and accessibility** are enforced by validators (CE-19 to CE-22): AC0 content rules, the zero-flash definition, WCAG floors, reduced-motion variants, the visual-essential flag, colour-vision checks and captions derived from the approved script.

**Note, 15 Oct 2026 (CE-64): persona ids.** The nine names above are display names. In the registry they are five ids with variants, as specified in `subsystems/VOICE_and_PERSONA_REGISTRY.md` §2.2: `persona/super-teacher` (variants `core`, `mentor`), `persona/super-teacher-junior` (`junior`, `coach`), `persona/lecturer` (`lecturer`, `seminar-lead`, `colleague`), `persona/skills-instructor` (`instructor`) and the register overlay `persona/exam-coach` (`strategist`, never at `safety/ac0`). Super Teacher Junior is l1_2 and l3_5; Super Teacher Coach is l6_8; Super Teacher is l9_10; Super Teacher Mentor is l11_12; Lecturer is ug (and adult_prof); Seminar Lead is pg; Colleague is educator; Skills Instructor is voc; Exam Strategist is the overlay register. A Level Profile `persona:` field reads `persona/<id>#<variant>`, for example `persona/super-teacher-junior#coach` (table in `LEVEL_PROFILES.md` §3.11). R11 and CE-23 are unchanged.

---

## 7. Subject-family validation

Details are in the Subject Validation Profiles document. Architecture-level rules:

- **Nine family profiles in v1:** `stem_fixture` (maths, physics, chemistry, biology, earth science, CS with sandboxed executable fixtures, engineering), `quant_social` (economics, accountancy, commerce, business studies, statistics, management), `humanities_citation` (history, geography, civics/political science, sociology, philosophy, IKS and value education), `languages_literature`, `arts_skills` (art, music, PE and well-being), `vocational`, `exam_strategy`, `health_medicine` (high-risk), `law` (high-risk). Each subject appears in exactly one family (R3).
- **Validation modes.** Fixture (STEM numerics and worked steps are computed, never generated), claim ledger, executable (code runs in a sandbox and the screen must equal captured output), or hybrid.
- **Claim-ledger rules** [Recommendation, CE-28], adopted from verifiability practice: the author carries the burden of proof [N13]; unsourced claims are removed by default [N14]; truth is not enough without publication in a reliable source [N15]; sources are not rejected for cost [N16]; exceptional claims need multiple high-quality sources [N17]; self-published sources are never used about living people [N18]; open wikis are not citable [N19]; claims are corroborated against reliable secondary sources [N39]. Model knowledge is never a source.
- **Triage, not judgement.** The citation-need flagger [N41]–[N43] only adds flags. Citations are often missing even under policy [N40], robustness varies by content quality [N44], and human-only checking is uneven [N45] (contested). The design is therefore flagger + span-hash check + qualified reviewer, never any one alone, mirroring editorial practice of verifying each fact [N59] with specialist review [N61] and regular revision [N62].
- **Contested claims (CE-29).** Four states (settled, attributed, contested, board_vs_scholarship). Contested claims need two qualified reviewers. A Short may not state one side as fact. The Perspectives format is required where a family profile says so.
- **Time-bound claims (CE-30).** Expiry at `review_by` marks the claim stale. If it is not re-reviewed within the family's grace period, the claim is revoked (blocking).
- **No activation without a named qualified reviewer** (schema-enforced; CE-27).

**Note, 15 Oct 2026 (CE-65): a tenth family, `family/evs_foundational`.** Classes 1–5 Environmental Studies (integrated science, social and health content) belonged to none of the nine families, so R3 would have refused every such request. `SUBJECT_VALIDATION_PROFILES.md` §13 adds `family/evs_foundational` as a [Recommendation]: fixture where quantitative, citation where factual, and a child-development reviewer co-sign. It is valid at l1_2 and l3_5 only and is not activated until its named reviewers exist (CE-27). The "nine families" figure above is therefore nine active-or-planned families plus this recommended one.

**Note, 15 Oct 2026 (level-3+, CE-121): corpus representation audit.** Per-artefact sensitivity review cannot see skew across many artefacts. WRK contexts, STY characters, ASM stems and MED people (generated or drawn only; never real children) may carry the optional tag object `depicted_attributes` {given_name_origin_region, gender_presented, setting, disability_presented, language}. The corpus check `Q-REPR` (`subsystems/QA_PROFILES_REGISTRY.md`) runs quarterly over released artefacts per level × family × locale and reports distributions against reference ranges set by the academic lead and the sensitivity reviewer. It is report-only, feeds the next quarter's authoring brief and never blocks an artefact.

---

## 8. Localisation

- **Claims are locale-invariant; surface is locale-specific.** Translations are REN nodes bound to the source node hash and approved by the native-language subject editor. Translating a lesson approves renderings; it does not re-approve science. A changed source node makes its renderings stale automatically. Q-CLOSURE.literals resolves a sentence that cites a REN through `rendering_of` and matches its literals against the source node at `source_node_sha256`, never against the REN text alone; Q-CLOSURE.ren_equivalence checks every REN's literals against its source (added 15 Oct 2026).
- **String tables (CE-39).** On-screen text is externalised into string tables keyed by node ID and cue ID, never baked into SVG paths. The visual timeline is reused; only text layers, narration and timing regenerate. H-SB re-runs only if layout changes beyond the cue sheet's tolerance.
- **Locale Profile fields (CE-40; schema `schemas/locale_profile.schema.json`, 15 Oct 2026):** BCP-47 tag, script, **text direction** (ltr or rtl; Urdu and Kashmiri in Perso-Arabic script are rtl), font stack (vendored Noto families in the container), **shaping engine pin** (the HarfBuzz version in the container, recorded in `harness/`, with conjunct render tests for Devanagari and Bengali-Assamese), numerals, **spoken-math and notation policy** (how symbols are spoken; display/spoken split per RD-29), **transliteration table** for Hinglish (a versioned house table, with ISO 15919 as the reference for term romanisation once registered in 09), code-mix policy (which terms stay in English), caption line rules, readability method (controlled vocabulary lists per level × locale, not ported English formulas [Hypothesis]), pronunciation lexicon (05), per-family glossaries, voice inventory with **GL-voice** status, native-reviewer pool and locale-gate status (07/04 §18), and `pacing_by_level` (per level_id: a tagged wpm range for ordinary, dense and recap; owner the native subject editor; absent = the Script Spec uses `teacher_set` for every beat) (CE-40; 15 Oct 2026).
- **GL-glossary.** The first artefact in each family × locale pair needs native subject-editor approval of the family glossary (a Hindi chemistry glossary differs from a Hindi history glossary).
- **GL-voice.** A blind native-speaker review of a TTS voice against the human reference, recorded in the ledger. **Launch statement (CE-41):** en-IN, Hinglish and hi-IN artefacts use Path B only with voices that have a recorded GL-voice pass. This specification does not record a pass for any voice. If none exists on launch day, R1 forces Path A for every artefact in that locale, which is a capacity risk tracked as open item O-12.
- **Language as subject vs language as medium.** Hindi literature is validated by `languages_literature`; a Hindi-medium physics lesson is `stem_fixture` plus `locale/hi-in`. They are never conflated. Language-learning formats take a locale pair (medium, target) in the Format Plan; the target comes from the family's `subject_locales` (R9a, 15 Oct 2026). Middle Stage requires three languages, at least two native to India [N33], so the locale registry grows by data, never code.
- **Transcreation versus rendering (level-3+, 15 Oct 2026, CE-118).** A REN changes wording only. It may not change ANL `mapping` or `non_mapping`, STY `beats[].carries`, WRK numbers or context entities, or ASM keys. A culturally adapted analogy, story or word-problem context is a new ANL, STY or WRK node with `adapted_from` (the source node id) and `locale_scope[]`, reviewed at GA-Graph like any node. Check `Q-LOC.meaning` (`subsystems/QA_PROFILES_REGISTRY.md`) back-translates each REN with a model and diffs it against the source node; flagged sentences go to a bilingual subject reviewer at GA-Δ. It is report-only until the level-4 pilot measures its precision. The GL-glossary record lists which terms were transcreated and which were kept in English, following the code-mix policy.
- **AC0 language.** ~~l1_2 defaults~~ l1_2 and l3_5 default (corrected 15 Oct 2026; enforced at compile time by R4) to one language per lesson until the child-development reviewer approves a code-mix pattern [Recommendation].

---

## 9. Quality, observability and cost

### 9.1 Automated checks (100% of artefacts, every time)

The check catalogue, severities and blocking status are owned by subsystems/QA_PROFILES_REGISTRY.md §2; CE-35 report-only rules apply. (15 Oct 2026: the table that stood here duplicated the catalogue and had drifted from it, for example by omitting Q-INT and Q-NARR; it is removed.)

**Captions.** Captions are generated from the approved script text, not from ASR. ASR is used only to detect narration drifting from the script (critical-term listening). Spoken mathematics is captioned in display notation; the transcript carries both display and spoken forms.

**Audio description (deliverable).** When a scene is `visual_essential` and its meaning is not fully spoken, export includes `ad.vtt` (WebVTT description cues) and an audio-described mix `audio_described.m4a`. Otherwise the narration itself must carry the meaning, and the validator blocks unflagged silent visuals.

### 9.2 Observability and ledger

One append-only ledger (JSONL in git or object storage, CE-49) with row types: `cost` (ProviderJob, render minutes, storage), `capacity` (human minutes by gate and role, **Path A studio minutes** by teacher and locale, STS minutes by locale), `provenance` (job → input/output hashes), `licence` (voice, music, text, map) and `reservation` (H-SB budget hold per artefact: storyboard_sha256, estimate, approver, released_on_gf; added 15 Oct 2026). Every row references an artefact hash and its EPP pins. Row types added 15 Oct 2026: `backup` (§9.5, CE-114), `incident` (§9.6, CE-115) and `signal_proposal` (§9.7, CE-117); these three reference a snapshot, an incident or a proposal rather than an artefact where none applies. Derived metrics:

- cost per approved finished minute, by format × level × family × locale × voice path;
- reviewer minutes per gate and role (GA-Graph, GA-Δ, GF/GS, child-development co-sign), measured against RD-41's 85 min per lesson;
- Path A studio minutes per approved minute, which is likely the binding constraint under CE-L2;
- cascade escalation rate per slot type; cache-hit rate; rework rate by stage; gate fail reasons;
- time waiting on gates; re-QA backlog after a change; defect-escape rate (errata per released minute).

H-SB reserves budget against the `budget/policy@x.y.z` lines per (format × level × voice path), seeded from the 08 cost workbooks; reconciliation runs monthly against provider invoices. Section 13's "review-free cost model" becomes a ledger query. No revenue or price lines exist in pipeline ledgers (CE-L1).

### 9.3 Determinism rules (CE-38)

- The container pins Node 22+, Chrome (exact build, `--disable-gpu`, `--force-color-profile=srgb`, `--font-render-hinting=none`, fixed device scale factor), FFmpeg (exact build), HarfBuzz and the vendored font bundle. Their digests live in `harness/`.
- Frames are captured by seek, never by wall clock (12 harness contract). The intermediate is lossless (PNG sequence or FFV1) with `framemd5` recorded. The final encode uses the pinned encoder with `-threads 1`, bitexact flags (`-fflags +bitexact -flags:v +bitexact -flags:a +bitexact`) and stripped metadata (`-map_metadata -1`), so the MP4 is bit-identical across runs.
- **TTS and STS outputs are not deterministic.** Narration audio is stored by `narration_audio_sha256` and is an immutable input to every re-render. Re-synthesis is a new narration version, never a silent replacement.
- **LLM slot fills are not deterministic.** Every fill is stored by hash. "Reproducible" means replaying stored outputs from the closure, not re-calling models.
- The macOS machine is for development only. The founder installs FFmpeg with `brew install ffmpeg` and Node 24 with `nvm install 24 && nvm use 24` (documented, not run by the agent; RD-50).

### 9.4 Kit and model qualification

The Kit is versioned per Kit cell. A new ModelProfile must re-run the 13 experiment protocol on the frozen evaluation set for each Kit cell before it is pinned. That is a production-class change (§3.6). Judges receive the level, persona, safety and family rubrics from the EPP.

### 9.5 Storage, backup and recovery

Level-1 (15 Oct 2026, CE-114). TTS, STS and model fills are not deterministic (§9.3), so losing one stored narration file breaks byte-identical reproduction for good.

- **Blob store.** `content/blobs/sha256/<aa>/<hash>` is write-once and content-addressed (§2.2). Every binary named in a closure manifest (§3.7) resolves to a blob: narration audio, Path A raw takes, consulted SRC copies, MED files, lossless intermediates and renders. A blob is never overwritten; it is removed only by crypto-shredding (below).
- **Backup [Recommendation].** Git and blobs are backed up daily to a second provider in another region. Each backup writes a `backup` ledger row {snapshot id, object count, verification hash}.
- **Retention classes.** Each blob carries `retention_class` ∈ {artefact_permanent, consent_bound, guardian_release, raw_take, reviewer_pii} with an expiry (none for artefact_permanent). Every class other than artefact_permanent is encrypted, and deletion on expiry or withdrawn consent is crypto-shredding of the key, so backups honour it too. Keys are held per class and per data subject, so one performer's or guardian's withdrawal shreds only their data (lead ruling 15 Oct 2026, CE-123; previously a [Recommendation]). Shredding a blob that a released artefact's closure names is a Revocation for that artefact (§3.6).
- **Restore drill.** Part of the M1 exit gate: rebuild a clean machine from backups only, re-render CR-1 from the stored closure, and obtain an equal MP4 SHA-256. Repeat quarterly and record each drill in the ledger (P1-15 "content-addressed blob store, daily cross-region backup, restore drill").

### 9.6 Incidents, withdrawal and on-call

Level-2 (15 Oct 2026, CE-115). Revocation (§3.6) says "blocked and withdrawn"; this section says how fast, by whom and how a withdrawal reaches every copy.

- **Severity.** S1: safety or child harm, a wrong fact or key in a released artefact, or a rights breach. S2: a stale exam-pattern claim or wrong metadata. S3: cosmetic.
- **Targets [Recommendation].** S1 withdrawn from every channel within 24 h. S2 corrected or labelled within 7 days. S3 joins the normal queue.
- **On-call.** The role `reviewer/on-call` sits in `reviewer/` with a primary and a backup on a weekly rota. On-call may withdraw an S1 artefact at once; the fix and any re-release pass the normal gates.
- **Withdrawal propagation.** Withdrawals are appended to `export/withdrawals.jsonl` {artefact_sha256, reason_class, replacement_sha256?, erratum_text}. The platform polls it; offline clients (`packaging/offline-download`) check it on reconnect and hide matching files.
- **Record and review.** Each incident writes an `incident` ledger row (detect, withdraw and fix times) and a post-incident review entry. Time-to-withdraw joins defect-escape rate (§9.2) in the monthly review.

### 9.7 Learning signals (aggregate only)

Level-2 for the interface, level-3+ for operation (15 Oct 2026, CE-117). The pipeline still holds no learner data (§1.1); it receives aggregates only.

- **Record.** The platform sends `learning_signal` records validated by `schemas/learning_signal.schema.json`, keyed by ids the sidecar already exports: artefact_sha256, asm_id, option_id or misconception_id, attempts, selection_share, cue_id with rewatch_share, doubt_cluster_text (paraphrased by the platform), window and cohort_level.
- **Privacy rules.** No learner identifiers. Each cell has a minimum cohort size set by counsel under O-3, with a stricter minimum for ac0 and ac1; a cell below its minimum is not sent. `doubt_cluster_text` is untrusted data (§2.2).
- **No direct edits.** A signal never edits the graph. It opens a proposal (raise a MIS priority, add a SIM, author a new MIS, or queue an F15 doubt) that goes through S4 and GA-Graph. Each proposal writes a `signal_proposal` ledger row; accepted and rejected counts are a KPI from level 3.

---

## 10. Migration of sections 01–14

| Section | Disposition | Detail |
|---|---|---|
| 01 Business model | **Reuse, outside the boundary** | Sole home of entitlement, pricing and free-chapter policy (RD-44 removed from pipeline scope by RD-49). The pipeline exports neutral metadata; the platform joins entitlement. |
| 02 Learning psychology + tokens | **Extend** | Production rules become level fields, slot constraints and A/Q-checks. `palette_and_typography_tokens.json` becomes `style/base@1.0.0`. The §K checklist becomes validator rules. Values become the l9_10 and l11_12 profile baseline. |
| 03 Super Teacher | **Extend** | The 10-minute structure becomes the Detailed grammar (compiled into chapters ≤360 s). The explanation ladder becomes `explain.ladder_step`. ~~The 10 skills drive slot filling.~~ The ten ST skills do not author in the engine (06 OVERLAP default rule). lesson-architect and analogy-auditor are S4 review lenses, confidence-editor is an S7 lens, science-reviewer is the independent re-solver and script-evaluator owns the repetition ledger and the script pre-review. conversational-script, concept-humour, interaction-designer, voice-director and language-editor are retired in the engine, their rules are folded into the NA owners, and they stay usable as the standalone ST kit (subsystems/SKILLS_and_KIT_MAP_v2.md §2.1). Slot narration is written by the NA script fillers (super-teacher-scriptwriter; interactive-teaching-director for check, card and viva slots) through the Kit (corrected 15 Oct 2026). The five delivery modes become a cue `voice` enum. The core becomes the persona root. |
| 04 Video engine v2 | **Extend** | `SourceRef`/`Claim` become SRC/CLM. `LessonPlan` becomes a compiled view with `level_ref`. `SceneSpec.subject` moves to the family registry and `kind` decouples (RD-35 retired). The four validated models seed the STEM fixture library. The SVG→FFmpeg 720×1280 renderer stays as preview profile and determinism oracle; production is 1080×1920. The 56 tests stay as regression. |
| 05 Narration | **Reuse** | NarrationPlan, lexicon (now per locale), provider compiler, timeline, −16 LUFS mastering and 60 tests (2 need FFmpeg; all 60 must pass in the pinned container) are format-agnostic. Pacing comes from the EPP. |
| 06 Skills library | **Extend** | New skills: `cg-import`, `graph-author`, `claim-ledger`, `citation-flag`, `span-verify`, `profile-resolver`, `format-compiler`, `closure-check`, `level-lint`, `persona-lint`, `safety-lint`, `flash-analyser`, `a11y-check`, `impact-analyser`, `v1-import`, `packaging-export`, `kit-verify` (the last two added 15 Oct 2026). The ownership map gains registry owners and slot-type owners. Skills for no active cell stay dormant. |
| 07 Runbook | **Extend** | Stages kept. GA splits into GA-Graph + GA-Δ. H-CG, GV-claims, GL-glossary, GL-voice, G-COUNSEL and GR are added. 07/03 and 07/05 are retired *as procedures* and absorbed into Format Specs. The vertical-only absolute rule is replaced by the format aspect field (CE-L7). One pointer row, RD-52, adopts the CE register. |
| 08 Cost workbooks | **Extend, then replace by ledger queries** | Lines per (format × level × voice path); reviewer minutes per role; Path A studio minutes; STS per-minute cost per locale; child-development minutes for AC0. |
| 09 Evidence | **Extend** | Seeds the Source Registry. Add N1–N76 and the legal, accessibility and standards sources listed in the Sources document (open items O-1 to O-11). |
| 10 Pilots | **Reuse** | Golden graphs, regression corpus and the M1 lesson. |
| 11 Human feel | **Reuse** | Path A/B definitions, sonic logo (style entry), disclosure wording; a child-appropriate sonic logo variant for AC0. Path selection moves to R1. |
| 12 Animation | **Reuse + extend** | Harness contract, cue-sheet schema, A1–A17 and edge cases apply to every format. The five style guides become style entries with `aspects_supported` and `safety_classes_allowed` (doodle-handdrawn and paper-collage are candidates for l1_2 to l6_8). A 16:9 safe-zone token set is added before the first 16:9 format is approved. HyperFrames default; Remotion benchmark. |
| 13 Strong-to-cheap | **Reuse + extend** | Kit cells; archetypes map to slot types; experiment protocol qualifies models; Ultracode banned; the $50 attended probe kept (CE-L3). |
| 14 Audit | **Reuse** | Level-0 exit checklist; re-run at every maturity gate. |
| Retired | — | Hard-coded `class_level ∈ {10,11,12}`, one-kind-per-subject (RD-35), single-persona assumption, vertical-only absolute rule, single-block 10-minute renders without chapters, `syllabus-map.json` as free text, any free/paid fields. |

**Note, 15 Oct 2026 (CE-68): the 04 `ShortSpec` commercial fields are retired from the pipeline contract.** The 04 row above refers to contracts that still carry `ShortSpec.access_tier` (free / preview / book_entitlement) and `destination_resource_id`. The pipeline is commercially agnostic (CE-L1, RD-49), so both fields are removed from the v2 pipeline contract: `v1-import` drops them, the v2 exporter never writes them, and the platform attaches entitlement and destination outside the pipeline, joined by artefact id. The 04 repository code is not edited by this specification; removing the fields there is a P1 build item at maturity level 1 (`MATURITY_MODEL_and_ROADMAP.md`). The same applies to the 07/06 §7 "free / preview / book-entitlement" and "destination resource" rows. See `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`, note dated 15 Oct 2026.

### 10.1 v1 → v2 import (CE-47)

Existing v1 artefacts (pilot lessons, published Reels, the 54 frozen scene packages, voice assets) have no EPP, closure hash or registry pins. Without migration, every one would fail the v2 release check. The converter `v1-import`:

1. Maps `LessonPlan.class_level` 10 → `level/l9_10`, 11 and 12 → `level/l11_12`; subject → `family/stem_fixture`; locale tags → `locale/*`; ShortSpec → `format/short`; LessonPlan → `format/detailed`.
2. ~~Converts `SourceRef`/`Claim` into SRC/CLM nodes~~ Converts `SourceRef`/`Claim` into SRC/CLM import drafts with `provenance.author_kind = import` and `import_ref` set to the v1 file hash; source-ingest and graph-author write them (15 Oct 2026). Spans without a stored copy hash are flagged `machine_checked`, not `expert_approved`.
3. Creates synthetic pins `legacy/v1@1.0.0` for registries that did not exist (safety, a11y, persona, overlay).
4. ~~Wraps each v1 approval as a **legacy approval**~~ Emits a wrap manifest for each v1 approval; the approval service writes it as a **legacy approval** with `legacy_closure_hash = sha256(JCS(v1 approval record + artefact sha256 + script bundle hash))` (15 Oct 2026).

**Policy.** Published v1 artefacts are **grandfathered**: they stay published, the release check accepts `legacy/v1` pins only for artefacts in state `published_v1`, and never for a new release, a re-release or a derived format. Any new format derived from v1 content must pass full v2 gates. The 54 frozen scene packages become Kit evaluation fixtures (not releasable). Voice assets enter `voice/` only with licence evidence; otherwise they are not admitted.

**Converter test.** Import the pilot set → compile with v2 → emit v1 contracts. The LessonPlan/SceneSpec/NarrationPlan hashes must equal the originals, and the 56 + 60 tests must pass on the compiled output. A second test re-imports the output and requires a stable graph hash (idempotence).

---

## 11. Risks

1. **Review and Path A capacity (highest).** CE-L2 makes every Detailed, first-in-series, flagship, real-demo and Class 1–5 artefact Path A. CE-L8 needs qualified reviewers per family, and AC0 needs a child-development reviewer at GA-Δ, H-SB and GF. *Mitigation:* the ledger tracks studio and reviewer minutes from M1; claims are approved once per objective; a cell is not activated without named reviewers and backups. *Revisit trigger:* Path A studio minutes or reviewer queue time exceed the H-SB plan for two consecutive months; the CE-L2 A/B data then goes to the lead. *Exam-season surge (level-3+, 15 Oct 2026, CE-122; pointer added by the critic-pass verifier):* reviewer load peaks before board and entrance exams; the reviewer rota with backups, `reviewer/on-call` (§9.6) and the exam-window freeze and T-10-week surge playbook (§3.6) mitigate it.
2. **Slot-vocabulary sprawl.** If every request adds a slot type, formats become code in disguise. *Mitigation:* ADR per slot, quarterly merge review, KPI of formats shipped with zero new slots.
3. **GA-Δ under-review.** Reviewers may skim derived formats because the graph was approved. *Mitigation:* full script read, every SIM/ANL shown, second-reviewer audit sample during pilots, GF/GS never reduced, no sampling of human gates. The saving is [Hypothesis] until M3 measures it.
4. **Front-loaded graph authoring.** A rich graph costs more than one script and pays back only with several formats per lesson. *Mitigation:* measure the break-even format count at M3; allow lean graphs for single-format scopes (the requirements table decides what is needed).
5. **Invalidation storms.** A popular entry (for example `level/l9_10`) touches thousands of approvals. *Mitigation:* change classes, auto re-affirmation when bytes are identical, impact preview at GR, batch re-QA. *Exam-season surge (level-3+, 15 Oct 2026, CE-122):* a storm in the weeks before board and entrance exams would take reviewer capacity from revision content; the exam-window freeze and the T-10-week surge playbook (§3.6) and on-call staffing (§9.6) mitigate it.
6. **Unproven young-learner and Indic values.** Engagement evidence is adult MOOC data [N1][N7]. *Mitigation:* Hypothesis tags with owners and pilots; report-only validators until confirmed; versioning makes correction cheap.
7. **Legal scope for minors.** India's under-18 child definition vs store under-13 regimes; synthetic-content labelling; personality rights for STS performers. *Mitigation:* AC1 no-solicitation, G-COUNSEL gate, sources registered before freeze.
8. **CASE data unavailable.** *Mitigation:* ExamLeaf as its own CASE provider [N51]; CASE as a shape, not a dependency.
9. **Model and voice drift.** A pinned model may be retired or a voice licence withdrawn. *Mitigation:* ModelProfile requalification (production class) and voice revocation (blocking) are routine drills.
10. **Over-building.** *Mitigation:* files first, maturity gates, YAGNI on the CASE REST service, sign-language tracks and a workflow engine until a KPI needs them.

---

## 12. Open items

| ID | Item | Blocks | Owner |
|---|---|---|---|
| O-1 | Register WCAG 2.2 (2.3.1 flashes, 1.4.1 use of colour, 1.4.3 contrast) as primary sources in 09 | AC0 release; Q-FLASH thresholds go from report to final | Founder |
| O-2 | Child-development reviewer signs the AC0 flash-analyser parameters (tile grid, luminance-change rule) and the l1_2/l3_5 hypothesis values | AC0 release | Academic lead |
| O-3 | Register India's Digital Personal Data Protection Act 2023 and its Rules (child = under 18; verifiable parental consent) | G-COUNSEL; AC0/AC1 freeze | Counsel |
| O-4 | Register store made-for-kids regimes (YouTube made-for-kids, US COPPA) | G-COUNSEL | Counsel |
| O-5 | Register the IT Rules provisions on labelling synthetically generated content and platform AI-disclosure rules; confirm whether Path A STS and Path B both need a visible label | DISCLOSURE gate update | Counsel |
| O-6 | Voice and personality-rights consent template for STS performers and brand voices | Path A at scale | Counsel |
| O-7 | Music and song licensing policy for `story.song_chant` (in-house composition default) | AC0 Story/Song | Founder |
| O-8 | Survey of India policy on depicting India's boundaries; map review procedure | Any map asset | Academic lead |
| O-9 | Medical-advice and legal-advice disclaimer rules | `health_medicine`, `law` activation | Counsel |
| O-10 | NCF Foundational Stage source for Classes 1–2 (not in the evidence set) | l1_2 profile freeze | Academic lead |
| O-11 | NSQF level descriptors for `level/voc` | voc activation | Academic lead |
| O-12 | GL-voice status of the en-IN, Hinglish and hi-IN TTS voices | Path B at launch | Founder |
| O-13 | Whether Assam Board (SEBA/AHSEC) publishes machine-readable outcomes | CG import vs hand authoring | Founder |
| O-14 | GA-Δ timing data (M3) | Capacity plan | Academic lead |
| O-15 | Path A studio capacity plan per locale | Throughput | Founder |
| O-16 | Exact Chrome, FFmpeg, HarfBuzz and font builds pinned in the container | Q-DET at M1 | Founder |
| O-17 | Controlled vocabulary lists per level × locale | Q-LEVEL blocking | Academic lead |
| O-18 | Sign-language profile trigger: ~~a partner or regulatory request~~ the first `a11y/isl` request or a pilot with a special-education partner (reworded 15 Oct 2026, CE-120) | — | Founder |
| O-19 | 16:9 caption and safe-zone token set | First 16:9 format | Founder |
| O-20 | CVD simulation thresholds and caption-timing tolerance confirmed for all levels | Q-A11Y CVD blocking | Founder |
| O-21 | Lead confirmation that §3.6 (every change queues re-QA; auto re-affirm only on identical bytes; revocation blocks) is the intended reading of CE-L10 | None (adopted pending confirmation) | Lead |
| O-22 | Child-development reviewer signs the AC0 audio startle parameters (maximum SFX peak relative to dialogue, minimum onset ramp, low-frequency limit; MUSIC §7) (added 15 Oct 2026) | AC0 release; Q-SAFE.startle (audio) blocking | Academic lead |
| O-23 | Written rights position per publisher class (NCERT, state boards, CBSE, NTA and other exam bodies, universities) covering verbatim display, adapted display, marks citation and figure redraw, with the statutory basis counsel relies on; recorded as `rights/<publisher>@x.y.z` entries (§3.1) that SRC `rights_basis` cites and that define the `quotation_within_policy` limits. Until it closes, M1's past-paper ASM uses `stem_form: adapted` and shows no marks (level-1, 15 Oct 2026, CE-112) | Any verbatim past-paper stem, official-key marking, textbook figure or TXT passage at release | Counsel |
| O-24 | Register the Rights of Persons with Disabilities Act 2016 and the Ministry of Education guidelines on e-content for children with disabilities (2021) as primary sources in 09; status: to verify, no quote until registered (level-3+, 15 Oct 2026, CE-120) | Freeze of `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia` and `a11y/isl` | Academic lead |
