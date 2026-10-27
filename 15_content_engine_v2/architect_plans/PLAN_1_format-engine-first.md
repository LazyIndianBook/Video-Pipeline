# Architect plan 1 — lens: format-engine-first

**Lens statement:** format-engine-first: one canonical Lesson Graph, every format derived by a declarative, versioned Format Spec (formats are data, not code paths)

**Thesis:** Approve the knowledge once and derive the videos many times. Each lesson becomes a canonical, hash-addressed Lesson Graph holding claims, objectives, prerequisites, worked items, misconceptions, assessments, assets and cue timing. Every format (Detailed, Simplified, Recap, Question Analysis, Shorts and others) is a versioned Format Spec. The spec selects and orders graph nodes using a closed vocabulary of slot types, and the existing contracts (LessonPlan, SceneSpec, NarrationPlan, cue sheet, ShortSpec) are what it compiles into. Each new format, level, subject family or locale is then a registry entry plus its tests, not a new pipeline. Accuracy, approvals and determinism are enforced once, at the graph and at the slot types, rather than separately for each format.

**Biggest risk:** The closed slot-type vocabulary is what makes "formats are data" true, and it is also the weakest point. If every new format request adds an untested slot type, or Format Specs become an expressive DSL, the engine turns back into one code path per format, with weaker gates than today. The second risk is that reviewers under-review derived formats in GA-Δ because the graph was already approved. Both need governance: an ADR for each slot type, a non-weakening spec linter, an unreduced GF/GS full watch, and GA-Δ minutes timed in the pilots.

---

# ExamLeaf Content Engine v2: the format-engine-first architecture

## 1. Thesis

Today, sections 04, 05, 07 and 12 produce **one thing well**: a roughly 10-minute Class 10–12 STEM lesson with derived Reels. ShortSpec is a separate procedure (07/05, SH1–SH8). SceneSpec ties `subject` to `kind` one-to-one (RD-35). `LessonPlan.class_level` only accepts 10–12. If we added Simplified, Recap, Question Analysis, Class 1–5 stories and 16:9 PG lectures the same way, we would get a separate code path for each format × level × family × locale. Each path would need its own QA and its own approvals, and they would drift apart.

**[Recommendation] Separate *what is true and taught* from *how it is packaged*.**

- **Lesson Graph.** The canonical, source-grounded store of claims, objectives, prerequisites, worked items, misconceptions, assessments, media assets and cue timing. The academic team approves it once.
- **Format Spec.** Declarative data saying which graph nodes to pull, in what beat grammar, at what length, aspect, register, voice path and interaction density, and which gates apply.
- **Derivation Compiler.** Deterministic code that turns *Graph × Format Spec × Level Profile × Subject-Family Profile × Locale Profile × Style × Voice* into the contracts that already exist. Cheap models then fill text slots through the Production Kit cascade (13).

This is the same idea as DITA's typed, self-contained topics with content reuse and single-source publishing ([N21], [N22], [N24], [N25]), applied to video. DITA's extensibility through specialization [N23] is the model for adding formats without forking.

**Formats are data. Slot types are code.** The Format Spec can only compose a **closed, tested vocabulary of slot types** (for example `hook.realworld`, `explain.ladder_step`, `worked.step`, `check.interpolated`, `misconception.confront`, `recap.retrieval`). Adding a format means adding data. Adding a slot type means adding code, tests and an A-check. Without this boundary, "formats as data" decays into an untested DSL. 13 §2.3 already warned against a full DSL compiler, so this design keeps to templates over a closed vocabulary.

---

## 2. Architecture

### 2.1 Components

| # | Component | Responsibility | Built from |
|---|---|---|---|
| C1 | **Source & Claim Ledger** | Ingests sources and extracts claims, each with ≥1 `SourceRef`. Unsourced claims are removable by default ([N14]); the claim owner carries the burden of proof ([N13]). | 04 `SourceRef`/`Claim`, S1–S3, 09 evidence register |
| C2 | **Lesson Graph Store** | Versioned, content-addressed nodes and edges, with a sub-graph hash per lesson and per node closure. | New; generalises `LessonPlan` |
| C3 | **Registries** | Format, Level, Subject Family, Locale, Style, Voice, Model and Slot Type. Every entry is versioned and hashed (CE-L10). | New; absorbs 02 tokens, 12 style guides, 05 `VoiceIdentity`/`ProviderProfile`, 13 model pins |
| C4 | **Competency Map** | Each objective links to a curriculum competency with a stable GUID, a parent/child hierarchy and crosswalk associations, following CASE ([N46]–[N50], [N66]–[N72]). | New; replaces free-text `objective`/`prerequisites` |
| C5 | **Derivation Compiler** | Deterministic. Resolves the Format Spec query against the graph, applies precedence merging (§2.4), lays out the beat grammar and emits a **Format Plan**. | New; absorbs 07/05 SH1–SH2 logic and 03's 10-minute structure |
| C6 | **Slot Filler** | Fills Format Plan slots through Production Kit templates, cascading Haiku→Sonnet→Opus per scene, with judges and verifiers (13). | 13 as-is |
| C7 | **Validators** | Validation scales by subject family (CE-L8): STEM fixtures (04's four validated models), claim-ledger coverage, level-register checks, locale lexicon checks. The A-suite runs on every artefact. | 04, 05, 12 A1–A17 extended |
| C8 | **Gate & Approval Service** | Every human approval is bound to a hash tuple. A dependency index invalidates approvals when any input changes (CE-L10). | RD-17 approval service, RD-46 H-SB |
| C9 | **Renderer** | Seek-deterministic harness (HyperFrames by default, Remotion benchmarked), pinned Linux container (CE-L4, RD-50), aspect taken from the Format Spec (CE-L7). | 12 harness contract, 04 SVG→FFmpeg proof renderer |
| C10 | **Narration** | Path A (performance → STS) or Path B (directed TTS), chosen by precedence merge. Sample-accurate timeline, −16 LUFS. | 05, 11 |
| C11 | **Cost Ledger** | Per-stage caps (RD-40), budget reserved at H-SB, reconciliation. | 08, `budget.py` |
| C12 | **Neutral Exporter** | Emits the artefact with neutral metadata only: subject, level, format, language, versions and hashes, plus disclosure and performer credit (RD-45). It has no entitlement fields (CE-L1/RD-49). | 07 S14 export record minus "access designation" |

### 2.2 Lesson Graph data model

Node types (all carry `id`, `version`, `sha256`, `status ∈ draft · machine_checked · expert_approved`, `locale_invariant: bool`):

- **Claim**: `statement`, `source_ids[≥1]`, `assumptions[]`, `exceptional: bool`, `contested: bool`, `jurisdiction?`, `as_of_date?`. Exceptional claims need ≥2 high-quality sources ([N17]). Truth alone is not enough; the claim must be published in a reliable source ([N15]). Wikipedia is not citable ([N19]). Sources are not rejected for cost or difficulty of access ([N16]).
- **Objective**: `competency_guid` (CASE item), `bloom_or_dok?` (taken from the framework's rubric if it publishes one [N49]; never invented), `tier ∈ core · extension`.
- **Prerequisite**: an edge `Objective → Objective` (possibly cross-lesson, cross-level), with `repair_slot_ref`.
- **Concept/Explanation step**: a rung on 03's explanation ladder, linked to claims through `supports`.
- **Analogy card**: 07/12 §5 proposed record (`mapping`, `non_mapping`, `likely_misconception`, `formal_return`).
- **Misconception**: `statement`, `why_plausible`, `confronting_evidence → Claim`, `diagnostic_item → Assessment`. The misconception-first design step is evidence-backed: [N73]. Without it, viewers risk an illusion of understanding [N74], and intuitive observation often misleads [N76] (contested).
- **Worked item**: ordered `steps[]`, each step linking to claims, with a `fixture_ref` for STEM numerics and `common_error_at_step[] → Misconception`.
- **Assessment item**: `stem`, `expected_answer`, `acceptable_variations`, `hint`, `feedback`, `exam_tags[]` (board, year, marks, as given by source paper), `evaluative: bool`. Some units are non-evaluative by design [N36] (contested).
- **Simplification**: `of → Claim`, `simplified_statement`, `what_is_lost`, `permitted_levels[]`. **[Recommendation]** Simplified, Class 1–5 and Shorts content may only say less through an *approved* Simplification node. The slot filler may never improvise a simplification.
- **Media asset**: the `AssetManifest` entry (rights, hash, generator, `ProviderJob`).
- **Cue/timing**: *not* stored on the canonical graph. Timing is a property of a derived artefact, so the graph holds only `min_inspection_s` hints per node. Measured timing lives in each artefact's cue sheet (12 schema: `words`, `beats`, `cues`, `narration_audio_sha256`, `script_sha256`).

Edges: `supports`, `requires`, `confronts`, `simplifies`, `assesses`, `illustrates`, `crosswalk` (CASE association [N50]). Each lesson is a sub-graph rooted at one or more Objectives, and it can reference nodes owned by other lessons (DITA conref [N24]). **One correction to a shared claim propagates to every format that cites it**, and through C8 it also invalidates their approvals.

### 2.3 The Format Spec

An illustrative shape. Field names are the proposal; values are examples, not adopted numbers.

```yaml
format_id: question_analysis
version: 1.2.0
intent: "Dissect one exam item: what is asked, the trap, the method, the marking."
select:                       # graph query, evaluated deterministically
  root: Assessment[exam_tags.present]
  include: [assesses->Objective, Objective<-supports-Claim, Misconception(confronted_by root), WorkedItem(assesses root)]
grammar:                      # closed slot vocabulary only
  - hook.question_reveal
  - check.interpolated {mode: predict, answer_hidden: true}
  - explain.what_is_asked
  - misconception.confront {max: 2}
  - worked.step {repeat: all}
  - marking.scheme {requires: exam_tags.marks}
  - recap.retrieval {max: 1}
duration_s: {min: 60, max: 240}      # [Hypothesis] to be tuned by pilots
aspect: 9x16                         # CE-L7: per format, never per lesson
voice_path: B                        # CE-L2; Level Profile may force A
interaction: {interpolated_checks: required}
levels_allowed: [L9_10, L11_12, COMPETITIVE, UG]
families_allowed: [stem, commerce, humanities]
gates: [GA_delta, H_SB, A_suite, GF]
styles_allowed: [editorial-vox, kinetic-type]
```

**Spec linter [Recommendation].** Every spec must be *satisfiable*: each slot type exists and the query can be filled. It must also be *non-weakening*. A spec cannot drop below its family's validation floor or its level's safety floor, cannot set `answer_hidden: false` on a `check.*` slot, and cannot omit disclosure. The linter runs in CI over all specs against a frozen golden graph set (reusing the 54 frozen scene packages from 13 §3.2 as seed fixtures).

### 2.4 Precedence merge

Several registries constrain one artefact. The compiler merges them by fixed rules:

1. **Safety and level floors win.** Level Profile beats Format Spec beats Style. Examples: Class 1–5 forces Path A (CE-L2, CE-L9) even if the format says B, and it imposes the stricter flash/motion limits.
2. **Validation is max-restrictive.** The union of family, format and level validators applies.
3. **Gates are additive.** The union applies, and no gate is ever removed.
4. **Duration is the intersection** of the format and level bounds. An empty intersection is a compile error, not a silent clamp.
5. **Locale changes surface only.** Locale Profiles change lexicon, script, register and voice. They never change claims.

The merged result is written into the Format Plan with a `provenance` field per value. A reviewer can then see *why* a Class 4 Recap is 90 s and human-voiced.

### 2.5 Flow and gates

```
S1–S3 Sources → Claim Ledger ──► G-SRC (source/claim review, family-qualified reviewer)
        │
Lesson Graph authored (strong model offline as compiler, CE-L6; humans edit)
        │
      GA-Graph  ◄── academic approval of the graph sub-tree (claims, items, misconceptions,
        │            simplifications, assessments); binds graph_subtree_sha256
        ▼
for each requested (format, level, locale):
   Derivation Compiler → Format Plan (deterministic, hashed)
   Slot Filler (Kit, cascade) → script/beat table
   GA-Δ  ◄── academic review of ONLY the derived surface: wording, declared
             simplifications used, analogies, interaction prompts (diff vs graph)
   H-SB  ◄── storyboard + cost estimate, founder (cost) + academic lead (fit) (RD-46)
   paid generation: narration (Path A/B), assets → Cost Ledger
   Render (pinned container) → A-suite (A1–A17 + format/level checks) → determinism hash
   GF (full watch, long formats) | GS (shorts)  + disclosure gate (RD-45)
   Neutral Export (CE-L1)
```

**Approval binding [Recommendation].** Every approval stores the tuple `{graph_subtree_sha256, format_spec@ver+sha, level_profile@ver+sha, family_profile@ver+sha, locale_profile@ver+sha, style@ver+sha, voice@ver+sha, model_pins_sha, kit_version, artefact_sha256}`. The C8 dependency index maps every registry entry and graph node to the approvals that consumed it. A change re-opens exactly the affected gates (CE-L10). For example, editing a claim invalidates GA-Graph for that sub-tree and every downstream GA-Δ, GF and GS. Editing a Style invalidates only H-SB, A-suite and GF/GS for artefacts using that style.

**Why GA-Graph plus GA-Δ, not GA per format.** RD-41 makes review minutes the throughput constraint (85 min per lesson as a capacity metric). If the graph is approved once and only the diff is reviewed per format, review time grows with *new surface* rather than with format count. **[Hypothesis]** GA-Δ for a Recap or Short takes a fraction of a full GA. The pilot must time it before any capacity plan relies on it. GF/GS full-watch is never reduced, because rendering, voice and sync defects are per artefact.

---

## 3. How the formats are produced

Each row is one Format Spec. All share the graph, validators and gates. Durations are **[Hypothesis]** starting bounds for pilots, informed by the evidence noted.

| Format | Graph selection | Grammar highlights | Aspect / voice | Evidence and notes |
|---|---|---|---|---|
| **Detailed** | All core + extension objectives of the sub-graph, every misconception, ≥1 worked item per objective | 03 ten-minute structure, compiled as **chapters under ~6 min**, with `check.interpolated` between chapters | 9:16 (16:9 allowed for the UG/PG variant); **Path A** | Median engagement is at most ~6 min regardless of length [N2]. Segment below 6 min [N3], [N28]. Engagement falls to ~50% at 9–12 min [N27]. Interpolated questions help [N30] (contested). Keeps the 10-min product as a playlist of chapters. |
| **Simplified** | Core objectives only; each claim replaced by its approved Simplification where `permitted_levels` matches | Shorter ladder, one analogy, one worked item, retrieval close | 9:16; Path B | Simplifications are only those declared in the graph |
| **Recap** | Objectives + the key claim per objective + top misconception | `recap.retrieval` first (retrieval before reveal), then a compressed statement | 9:16; Path B | Faster familiar-recap pacing per 03 §9.3 targets |
| **Question Analysis** | One Assessment with exam tags + linked worked item + misconceptions | §2.3 example | 9:16; Path B | Marking slot only renders if the source paper's marks exist; never invented |
| **Shorts/Reels** | One *complete learning unit*: one claim, or one misconception + confrontation, or one worked step | 07/05 SH5 timing compiled from spec; recomposed, never cropped | 9:16; Path B | Absorbs SH1–SH8 as a spec family (`short.concept`, `short.misconception`, `short.trap`) |
| **Prerequisite Repair** | Prerequisite edges whose target objective is in a lower level | Diagnostic check → minimal explanation → return link | 9:16; B (A for Class 1–5) | Generated automatically from graph gaps |
| **Misconception Buster** | One Misconception + confronting claim + diagnostic item | Predict → reveal conflict → explain → re-test | 9:16; B | [N73], [N74], [N76] |
| **Worked Example Walkthrough** | One WorkedItem, all steps | `worked.step` with learner-controlled pause per step | 9:16 or 16:9 per spec; B | Khan-style continuous drawing flow is more engaging than slides [N5] |
| **Derivation / Proof** | Claim chain with `requires` edges, fixture-checked | Step-by-step with an assumption callout per step | 16:9 variant for UG/PG; A | STEM fixtures validate each step |
| **Formula / Definition Card** | One claim plus its symbols, units and conditions | 15–30 s, display/spoken split (RD-29) | 9:16; B | Pure reuse of graph nodes |
| **Rapid Revision (chapter)** | All Recaps of a chapter's lessons | Concatenation spec: references other formats' approved artefacts | 9:16; B | Pure composition; no new claims, so GA-Δ is minimal |
| **Practice Set** | Assessment items by objective, difficulty-ordered | Question → think window (RD-11, answer hidden) → solution | 9:16; B | Interaction-heavy |
| **Activity / Lab Demo** | Activity node + safety claims + observation claims | Real-life opener → do → observe → check-understanding | 9:16; A for Class 1–5 | Mirrors the textbook pattern of real-life opener and check questions [N37] (contested) |
| **Story / Read-along (Class 1–5)** | Simplified claims + vocabulary nodes | Narrative, song/chant slot, drawing slot | 9:16; **A only** | Play-way, multimodal pedagogy [N9], [N10] |
| **Lecture (UG/PG)** | Full sub-graph incl. extension objectives | Slides + instructor-head intercuts, chaptered | **16:9** declared by spec (CE-L7); A | Talking head intercut with slides beats slides alone [N4] |
| **Case Study (humanities/commerce/law)** | Source documents + claims with `as_of_date`/`jurisdiction` + interpretive claims | Context → evidence → competing readings → question | 9:16 or 16:9; A/B by level | Interpretations rendered as interpretations (§5) |

**Shorts are no longer a separate procedure.** They are specs whose selector demands a *complete unit*, so 07/05's "recompose, never crop" principle becomes a compiler invariant.

**Speaking rate.** Format Specs carry WPM bands as `[Hypothesis]` values only. The evidence that faster speech raises engagement is contested ([N6], [N29]) and is measured on MOOC proxies ([N1]: watch time and problem attempts). Results cover 1× plays only [N7]. **[Recommendation]** Keep 03's audition targets (130–155 active wpm ordinary, 105–125 dense) as defaults, and test faster bands only in the 11 A/B programme.

---

## 4. Levels: Level Profiles

A **Level Profile** is a registry entry, not a code branch. Fields: `register` (sentence length, vocabulary list, notation allowed), `duration_ceiling`, `interaction_density`, `motion_flash_limits` (references to A-check thresholds), `voice_path_floor`, `reviewer_roles_required`, `child_safety: bool`, `curriculum_frameworks[]` (CASE GUIDs), `assessment_style`.

| Profile | Key settings | Basis |
|---|---|---|
| **L1_2 (Classes 1–2)** | `child_safety: true`; Path A forced; shortest formats; Story/Activity/Read-along formats enabled; no exam formats; child-development reviewer added to GA-Δ and GF | CE-L9. Classes 1–2 precede the Preparatory Stage; [N8] places Preparatory as bridging from Foundational |
| **L3_5 (Classes 3–5)** | As L1_2, plus textbooks introduced gently: "without overwhelming" | Preparatory = Grades 3–5 [N8]; play-way and activity methods continue [N9]; multimodal [N10]; textbook is one tool among many [N12] |
| **L6_8** | More abstract ideas; explicit learning goals per lesson; reasoning-focused assessment; direct instruction balanced with inquiry | Middle Stage Grades 6–8 [N32]; abstraction shift [N53]; inquiry over facts [N54]; reasoning over recall [N55]; balance of instruction and exploration [N34] |
| **L9_10, L11_12** | Today's scope; board exam tags enabled; Question Analysis and Rapid Revision enabled | Existing 03/04/07 rules |
| **COMPETITIVE** | Exam-pattern tags (exam, year, paper section, as published); trap-focused Shorts; Practice Set density high; marking only from official keys | **[Recommendation]** a separate profile because traps and marking schemes differ from board exams |
| **UG, PG/Masters** | 16:9 Lecture/Derivation formats permitted; notation-dense register; extension objectives default-on; reviewers must hold subject qualification at or above level | CE-L7, CE-L8 |

**Child-safety rules (CE-L9) live in the Level Profile and the exporter, not in formats.** `child_safety: true` sets the export metadata to made-for-kids, strips any comment or data-collection hooks the platform layer might attach, applies the tightest motion/flash A-checks, forces Path A, and adds the child-development reviewer. No numeric flash thresholds are invented here. The A-suite's existing limits are tightened by a value the child-development reviewer sets and records as a registry change. The NCERT Preparatory text contains no explicit child-safety rules [N12], so this must come from platform made-for-kids policy and qualified review rather than from the curriculum documents.

**Crosswalks.** Because objectives carry CASE GUIDs with associations [N50], one graph node can serve Assam Board, NCERT and a competitive syllabus at once. Board-specific framing lives in Level/Locale metadata rather than duplicate content. **[Hypothesis]** Machine-readable CASE frameworks for Indian boards may not exist. In that case ExamLeaf acts as its own CASE *Provider* [N51], publishing internal GUIDs, and switches to official GUIDs if they appear.

---

## 5. Subject families beyond STEM: Subject-Family Profiles

The **Subject-Family Profile** declares the validators, source tiers, reviewer roles, slot types permitted and family-specific node fields. Gates scale by family, never by commercial value (CE-L8).

| Family | Validation floor | Specific rules |
|---|---|---|
| **STEM (physics, chemistry, maths, biology, earth science)** | Fixture validation: 04's four validated models generalise into a fixture library. Every numeric claim and worked step is computed, not generated. | `kind` decouples from `subject` (retire RD-35's 1:1). New fixture = code + tests |
| **Social science / history / geography / civics** | Source-grounded claim ledger; ≥1 reliable published source per claim [N15]; exceptional claims ≥2 high-quality sources [N17]; `contested` claims must render as contested with attribution; dates/boundaries carry `as_of_date` | Qualified historian/geographer reviewer; map assets need rights + boundary review |
| **Languages & literature** | Text rights in AssetManifest; quotations from licensed/public-domain editions only; interpretive claims marked `interpretation` with attribution | Native-speaker reviewer per language; pronunciation lexicon mandatory |
| **Commerce, economics, law, accountancy** | Claims carry `jurisdiction` + `as_of_date`; a statute or rate claim expires on a review date | Qualified reviewer; re-QA triggered by expiry (CE-L10 extended to time) |
| **Health, PE & wellbeing, biology-health topics** | Safety claims are treated as exceptional (≥2 high-quality sources) | Qualified health reviewer; activity safety slot required |
| **Arts, music, vocational** | Technique claims sourced; demonstration assets reviewed by a practitioner | Path A preferred for demonstration formats |
| **Indian Knowledge Systems and value education** (cross-cutting themes [N35]) | Historical claims sourced as social science; normative statements marked as curriculum position, not empirical fact | Reviewer qualified in the specific tradition |

**Automated claim flagging.** C1 runs a classifier stage that flags statements needing a citation and the likely reason, following the citation-need work ([N43]), which was tested across article-quality classes and a fact-checking dataset ([N44]). Human-only verification does not scale evenly ([N45], contested), and citations are often missing even under policy ([N40]). **[Recommendation]** The classifier only *adds* flags. It never clears a claim. Clearance is GA-Graph by a family-qualified reviewer, mirroring the editorial practice of verifying each fact against reputable sources [N59] with subject-expert review [N61] and regular revision [N62]. The exporter publishes contributors, sources and last-revision date per artefact, as Britannica does [N60]. Its five-role editorial cycle [N63] (contested) is a reference for the in-house team's role split, not a requirement.

---

## 6. Languages and locales: Locale Profiles

A **Locale Profile** holds the BCP-47 tag, script, numeral and notation conventions, pronunciation lexicon (05), register per Level, code-mix policy (for Hinglish: which terms stay in English), caption font stack, TTS provider admissions with native-speaker gate status, and the human-voice requirement.

- **Claims are locale-invariant. Surface is locale-specific.** Graph nodes hold canonical meaning, and locale-specific *renderings* are child nodes (`rendering_of → node`, `locale`) with their own review status. Translating a lesson therefore means approving renderings, not re-approving science. [Recommendation]
- **Launch locales:** en-IN, Hinglish and hi-IN, each behind the 07/04 §18 locale gate (CE-L5, RD-42). Assamese and other Indic locales get a Profile with `tts_admitted: false`, which forces Path A human voice until a TTS passes the native-speaker gate.
- **Precedence:** Locale may tighten duration (scripts can run longer in some languages), but if that exceeds the Format/Level intersection it is a compile error routed to the spec owner. Content is never silently cut.
- **Curriculum language breadth:** the Middle Stage requires three languages, at least two native to India [N33]. Language-learning formats therefore need a Locale Profile *pair* (`medium`, `target`). That is a Format Spec field, not a new pipeline.

---

## 7. Sections 01–14: reuse, extend, retire

| Section | Disposition |
|---|---|
| 01 business model | **Reuse, but moved outside the boundary.** It holds entitlement, pricing and free-chapter policy (RD-44 removed from pipeline, RD-49). The pipeline exports neutral metadata; the platform joins entitlement. |
| 02 learning psychology + tokens | **Extend.** Production rules become A-checks and slot-type constraints; `palette_and_typography_tokens.json` becomes the base Style registry entry. Scene pedagogy record (12 fields) maps onto Format Plan slots. |
| 03 Super Teacher | **Reuse as-is for content; extend structurally.** The 10 skills drive slot filling; the explanation ladder becomes `explain.ladder_step`; the five delivery modes become the `voice` enum on cues; the 10-min structure becomes the Detailed Format Spec grammar (compiled into <6-min chapters [N3]). |
| 04 video engine v2 | **Extend.** `SourceRef`/`Claim` become graph nodes. `LessonPlan` becomes a *compiled view* of graph + Format Plan, with `class_level` replaced by a Level Profile ref. `SceneSpec.subject` enum moves to the Family registry and `kind` decouples. The four validated models seed the fixture library. The SVG→FFmpeg proof renderer is kept as a fallback and determinism oracle. The 56 tests remain regression. |
| 05 narration | **Reuse as-is.** NarrationPlan, lexicon, provider compiler, timeline and mastering are format-agnostic. Lexicons move under Locale Profiles. |
| 06 skills library | **Extend.** Ownership map gains Registry-owner and Slot-Type-owner roles; one skill per slot type (consistent with 13 §4.1 one-skill-per-archetype). |
| 07 runbook | **Extend.** Stages stay; GA splits into GA-Graph + GA-Δ; 07/05 Shorts procedure is **retired as a procedure** and absorbed as Short Format Specs. RD-35 is retired. RD-44 is already removed. New RDs record each registry's governance. |
| 08 cost workbooks | **Extend.** Cost lines become per (format × level × voice path); H-SB reserves against these. |
| 09 evidence | **Reuse.** The evidence register becomes the Source Ledger's seed; this plan's [N#] are added. |
| 10 pilots | **Reuse** as golden graphs for the spec linter. |
| 11 human-feel | **Reuse.** Path A/B wording and the disclosure gate are untouched; Path selection moves into precedence merge. |
| 12 animation layer | **Reuse as-is.** The seek-deterministic contract, cue-sheet schema and A-checks apply to every format. The five style guides become Style registry entries with `aspects_supported`, and a 16:9 safe-zone token set is added only when a 16:9 format is first approved. |
| 13 strong-to-cheap | **Reuse as-is.** Kit and cascade fill slots, and the archetypes map onto slot types. The $50 attended probe is kept (CE-L3). |
| 14 audit | **Reuse** as the baseline; re-run the audit at each maturity gate below. |

---

## 8. Build order with gates

Each milestone exits only when its gate passes. **[Recommendation]** Do not start the next milestone on partial gates.

**M0: Contracts and registries (no new content).**
Define the Lesson Graph schema, Format Spec schema, Level/Family/Locale Profile schemas, Slot-Type registry and approval tuple. Re-express the *current* Ohm's-law/600 s blueprint (02) and one pilot as a graph.
*Gate:* the compiler re-derives today's Detailed LessonPlan/SceneSpec/NarrationPlan and a ShortSpec, and the existing 56 + 58 tests pass on the compiled output. Same input gives the same Format Plan hash.

**M1: Derivation of the five core formats for L9_10/L11_12 STEM, en-IN.**
Ship specs for Detailed (chaptered), Simplified, Recap, Question Analysis and Short; the spec linter; precedence merge; and GA-Graph + GA-Δ in the approval service with the dependency index.
*Gate:* for 4 pilot lessons, all five formats render deterministically in the pinned container (identical hashes across two runs). A-suite passes. GF/GS full watch by in-house reviewers. Approvals are verified to invalidate when one claim is edited (an invalidation test). GA-Δ minutes are timed and compared against the 85-min baseline (RD-41).

**M2: Locales.**
Hinglish and hi-IN Locale Profiles with renderings.
*Gate:* the locale gate (07/04 §18) passes per locale, a native reviewer signs the renderings, and no claim node changes during localisation (graph diff empty).

**M3: Second subject family and claim-ledger validator.**
Pick one non-STEM family (for example social science for L9_10). Build the citation-need flagger, contested/as-of rendering slots and a family-qualified reviewer role.
*Gate:* every rendered claim resolves to an approved claim with a reliable source. An adversarial test (inject an unsourced claim) is caught. Case Study and Recap formats ship for that family.

**M4: Level breadth downwards (L6_8, then L3_5/L1_2).**
Level Profiles, Story/Activity/Read-along specs, child-safety exporter settings, Path A capacity, child-development reviewer.
*Gate:* made-for-kids metadata is verified on export, Path A is enforced (a compile error if B is requested), the tightened motion/flash A-checks are recorded by the reviewer, and a pilot with the reviewer's sign-off passes.

**M5: Level breadth upwards (UG/PG, COMPETITIVE) and 16:9.**
Lecture and Derivation specs at 16:9, a 16:9 safe-zone token set and competitive exam-tag ingestion.
*Gate:* 16:9 renders pass the same determinism and A-suite. A qualified UG/PG reviewer approves. Competitive marking slots render only from official keys.

**M6: Scale operations.**
Registry change management (impact preview: "this Style edit invalidates N approvals"), re-QA batch runner and cost dashboards per format × level.
*Gate:* a full registry change (for example a Voice version bump) is executed end to end, with re-QA and re-approval completed and cost reconciled against H-SB reservations.

New formats after M1 follow one rule: **spec + linter pass + one golden-graph render + GF**. A format that needs a new slot type waits for that slot type's code, tests and A-check.

---

## 9. Risks

1. **Slot vocabulary sprawl (highest).** If every format request adds a slot type, "formats as data" becomes "formats as code in disguise". *Mitigation:* slot types need an ADR, an owner, tests and an A-check. A quarterly review merges near-duplicates. The KPI is the fraction of formats shipped with zero new slot types.
2. **GA-Δ under-review.** Reviewers may skim derived formats because "the graph was approved". A simplification that is technically declared can still mislead in context. *Mitigation:* GA-Δ shows the diff and *every* Simplification and Analogy used. GF/GS full watch is never reduced. Pilots time GA-Δ and sample-audit it by a second reviewer. **[Hypothesis]** that GA-Δ is materially cheaper than GA; unproven until M1.
3. **Graph authoring cost moves up front.** A rich graph (misconceptions, diagnostic items, simplifications) is more work than one script. It pays back only if several formats are derived per lesson. **[Hypothesis]**: break-even format count is unknown; measure at M1.
4. **Invalidation storms.** CE-L10 plus shared nodes means one claim fix can re-open dozens of approvals. *Mitigation:* impact preview before commit, batch re-QA, and node-closure hashes. This is cost, not a defect: it is the price of a single source of truth [N24].
5. **Competency frameworks unavailable.** CASE is a published standard ([N69] Final, with conformance [N70] and an implementation guide [N71]), but Indian boards may not publish CASE data. *Mitigation:* ExamLeaf becomes its own Provider [N51] with stable internal GUIDs.
6. **Evidence transfer.** Engagement evidence comes from MOOC adults and uses watch-time proxies [N1]. It may not hold for Class 1–5 or vertical mobile video. Six-minute chaptering [N2], [N3] and speaking-rate claims ([N6], [N29], contested) must be pilot-tested per Level Profile, not assumed.
7. **Non-STEM reviewer supply.** CE-L8 requires qualified reviewers per family. A small in-house team bounds how many families can open (M3 opens one). Opening a family without its reviewer is forbidden by the linter's family-floor rule.
8. **Child-safety drift.** Made-for-kids obligations come from platform and legal policy, not from curriculum texts [N12]. *Mitigation:* legal review of the exporter's child-safety fields before M4's gate.

**Biggest single risk:** the closed slot vocabulary. It is what makes "formats as data" honest, and it is also where the architecture degrades if governance is skipped.
