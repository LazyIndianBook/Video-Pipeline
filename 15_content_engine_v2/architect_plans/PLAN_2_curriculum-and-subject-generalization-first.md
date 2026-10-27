# Architect plan 2 — lens: curriculum-and-subject-generalization-first

**Lens statement:** curriculum-and-subject-generalization-first: a CASE-shaped curriculum/standards graph (any board, Class 1 to Masters, any subject family) plus per-subject-family Validation Profiles (STEM fixtures kept; claim ledgers, citation rules, qualified-reviewer rubrics and contested-claim handling for every other family)

**Thesis:** The pipeline generalizes by making the learning objective, not the lesson, the unit of truth. Every artefact (any format, level, locale) is compiled from Knowledge Units bound to globally identified curriculum objectives and to claims that have already passed their subject family's Validation Profile. Derived formats (Simplified, Recap, Shorts, Question Analysis and others) may only reuse approved claims ("derivation-closed"), so accuracy is checked once per objective and family. It is not re-litigated per video. Scale then comes from adding registry entries (board framework, family profile, level profile, format spec, locale profile), never from adding new pipelines.

**Biggest risk:** Qualified-reviewer capacity, not technology. Each new subject family and level band needs an in-house reviewer who is genuinely qualified for it: a historian, a native-language literature editor, a child-development specialist, a commerce teacher. Validation profiles with no reviewer behind them would either stall production or quietly turn into rubber stamps. The design reduces the load by reviewing each objective once and requiring derived formats to reuse only approved claims, but those savings are unproven. A family must never be activated until a named, qualified reviewer is assigned to it.

---

# ExamLeaf Content Engine v2: the curriculum-and-subject-generalization-first architecture

## 1. Thesis

Today the pipeline is lesson-centric and STEM-centric. A LessonPlan carries its own facts, and a validated scientific model (one of four fixtures) proves them. That design will not stretch to Class 1 rhymes, Class 8 history, B.Com accountancy, M.A. literature or a competitive-exam strategy Reel. It cannot do it without either dropping the accuracy bar or building a new pipeline for each case.

**[Recommendation]** Make the **curriculum objective** the unit of truth and the **subject family** the unit of validation:

1. A **Curriculum Graph** with a globally unique ID for every competency or learning outcome, a parent/child hierarchy and typed associations (prerequisite, crosswalk to another board, exam-blueprint mapping). This is the shape CASE already standardizes [N46][N47][N48][N50].
2. **Validation Profiles (VP)**, one per subject family. STEM keeps executable fixtures. Every other family gets a source-grounded **Claim Ledger**, citation rules, a qualified-reviewer rubric and a contested-claim policy, modelled on mature verifiability practice [N13][N14][N15][N17] and professional editorial process [N59][N60][N61].
3. **Knowledge Units (KUs)**: typed, self-contained, reusable content modules in the DITA style [N21][N22][N24]. Each KU is bound to objective IDs and approved claim IDs.
4. **Formats compile from KUs and may only cite already-approved claims.** One validated source can then be published as many products, in the same way DITA single-sources HTML, PDF and EPUB [N25]. The only video-level accuracy work left for a derived format is a cheap "claim-subset + no new assertion" check plus the existing final-watch gates.

This is the cheapest way to make "Class 1 to Masters, all subjects, any language" possible without weakening CE-L8. Accuracy cost scales with the number of *objectives × families*, not with *videos × formats × locales*.

## 2. Architecture

### 2.1 Components

Following the ponytail rule (smallest thing that works), every registry starts as **versioned JSON files with JSON Schema in the repository**, hashed by the existing hashing code. No graph database and no new service are added until file-based queries measurably fall short. **[Recommendation]**

| # | Component | What it is | Builds on |
|---|---|---|---|
| C1 | **Curriculum Graph (CG)** | Frameworks (board × edition × stage × subject) → Items (competency / learning outcome / topic) with GUIDs, parent/child edges and associations: `prerequisite_of`, `crosswalk_equivalent`, `assessed_by_blueprint`, `non_evaluative` (some units are explicitly non-evaluative [N36]). An optional `depth` rubric per item [N49]. | Replaces `syllabus-map.json` (H-S2) and the unowned prerequisite graph (RD-30) |
| C2 | **Source Registry** | Each consulted source: bibliographic record, tier, rights status (from H-S2), SHA-256 of the copy consulted, page/span locators, access date | New; feeds C3 |
| C3 | **Claim Ledger** | Every assertable statement in a script, with type, sources, evidence span, risk class, review status and contested status | Generalizes the "claims" already in the GA script bundle |
| C4 | **Validation Profile Registry** | One profile per subject family: allowed claim types, validator kinds, citation rules, reviewer qualifications, contested-claim policy, required automated checks | STEM profile = the existing four fixtures + science checks |
| C5 | **KU Store** | Typed KUs: concept, procedure, worked-example, reference/fact-set, misconception, question+marking-scheme, source-analysis, activity, story. Each bound to objective GUIDs + claim IDs + fixture IDs. Reuse is by reference, never by copy [N24] | LessonPlan beats become KU references |
| C6 | **Format Spec Registry** | Per format: duration bounds, aspect ratio (CE-L7), maximum segment length, structure template, required interaction beats, narration path (CE-L2), allowed KU types, validation delta | Generalizes ShortSpec and the 10-minute structure (03) |
| C7 | **Level Profile Registry** | Per stage band: language complexity limits, segment ceilings, interaction density, motion/flash class, reviewer roles, voice path, made-for-kids flag (CE-L9) | New |
| C8 | **Locale Profile Registry** | Existing locale gate (doc 04 §18) + lexicon + per-family terminology glossaries + numeral/script rules | Extends 05 lexicon and RD-42 |
| C9 | **Gate & invalidation engine** | Existing approval service (RD-17/RD-32), now with a dependency graph from every artefact hash to the registry entries it used (CE-L10) | Extends 07/06 gates |

The existing engine (04), narration (05), animation harness (12) and Production Kit/cascade (13) stay as the **render back-end**. They receive a compiled LessonPlan/SceneSpec exactly as now. This lens changes what comes *before* the LessonPlan and how the LessonPlan is validated.

### 2.2 Data model (core records)

- `Framework {framework_guid, board, edition, stage, subject, source_doc_hash, provider: "CASE-import" | "hand-authored", version}`
- `CurriculumItem {item_guid, framework_guid, parent_guid, statement, item_type (competency|outcome|topic), depth_rubric?, associations[] {type, target_guid}, version}`
- `Source {source_id, citation, tier, rights_status, copy_hash, locators[], self_published: bool, about_living_person: bool}`
- `Claim {claim_id, text_pivot, translations{locale: text}, type, objective_guids[], sources[] {source_id, span_locator, span_hash}, risk (routine|exceptional|sensitive), contested_status (settled|attributed|contested|board-vs-scholarship), validator_results[], reviewer_approvals[], version}`
- `ValidationProfile {family_id, claim_types_allowed[], validators[], citation_rules{}, reviewer_roles[] {role, qualification, count}, contested_policy{}, required_checks[], version}`
- `KnowledgeUnit {ku_id, ku_type, objective_guids[], claim_ids[], fixture_ids[], level_band_range, body (script fragment + visual intent), version}`
- `FormatSpec {format_id, aspect, duration{min,max}, max_segment_s, structure_template, interaction_rules, narration_path, ku_types_allowed[], validation_delta, version}`
- `LevelProfile {band_id, reading_level_rule, max_segment_s, interaction_density, motion_class, made_for_kids: bool, reviewer_roles[], voice_path_override, version}`
- `LocaleProfile {locale, gate_status, lexicon_hash, glossaries{family: hash}, voice_identity, version}`
- `Artefact metadata (export)`: neutral only (CE-L1), with `{objective_guids[], framework_guid, family, level_band, format_id, locale, version, content_hash, approvals[], registry_versions{}, sources_and_revision_record}`. A public sources-and-revision record follows the practice of identifying contributors, sources and last revision date [N60]. There are no price, tier, free/paid or entitlement fields.

### 2.3 Main flow (objective → artefacts)

```
CG items selected (H-CG)          -- academic owner approves objective set + framework version
  → research: Sources registered (rights from H-S2)
  → Claim Ledger drafted (cheap model via Kit; claim-flagger marks every needs-citation sentence [N43])
  → Family validators run (fixtures | citation/span checks | answer-key solver | grammar/pronunciation)
  → Claim review by qualified reviewer(s) per VP  (GV-claims)
  → KUs authored from approved claims only
  → GA-{family}: script bundle = KUs + claims + fixtures + answer keys, hash-bound
  → Format compile: FormatSpec × LevelProfile × LocaleProfile → LessonPlan/SceneSpec/NarrationPlan
  → derivation-closure check (no claim outside the approved set; no new numbers/dates/names)
  → H-SB (unchanged: founder cost + academic fit, two identities)
  → narration Path A/B (CE-L2) → render (pinned Linux box, seek-deterministic) → A1–A17
  → GF (full watch) / GS (per Short) → Disclosure gate (RD-45) → export with neutral metadata
```

### 2.4 Gates (existing kept, three added, one parametrized)

| Gate | Status | Bound to |
|---|---|---|
| **H-CG** curriculum fit | *new*; replaces H-S2's syllabus-map half (rights stay in H-S2) | Framework version + selected item GUIDs |
| **GV-claims** | *new* | Claim IDs + versions + source span hashes + validator results |
| **GA-{family}** | *parametrized* GA; the reviewer qualification comes from the VP | Script bundle hash (now including KU and claim hashes) |
| H-SB, voice gate, critical-term listening, GF, GS, Disclosure, Publish | unchanged | unchanged |
| **GL-family** (per locale × family, first time only) | *new*; extends the locale gate | Glossary hash for that family in that locale + native subject-editor approval |

**Invalidation (CE-L10).** Each approval stores the registry versions it consumed. Changing any registry entry gives a set of affected artefacts (a reverse lookup over stored dependencies), and those artefacts drop back to the earliest gate that entry feeds. Examples: claim → GV-claims; VP → GV-claims for that family; FormatSpec → H-SB; LevelProfile → GA; Locale glossary → GL; voice → voice gate; model ID → the Kit regression. A corrected claim propagates to every KU and format that references it [N24], which also drives errata (RD-31).

## 3. Formats: how they are produced

**Core rule [Recommendation]:** a format is a FormatSpec, not code. A **primary** format (Detailed, and the family-specific primaries below) is where claims are first assembled and passes the full GA-{family}. A **derived** format (Simplified, Recap, Shorts and most others) passes the derivation-closure check and reuses the parent's GA. A derived format gets its own GA only when it introduces a KU the parent did not contain.

On length, the evidence does not support single 10-minute blocks. Median engagement is at most about 6 minutes regardless of video length [N2]. It is near 100% under 6 minutes and about 50% at 9–12 minutes [N26][N27], and the recommendation is to segment into chunks shorter than 6 minutes [N3][N28]. Evidence on interpolated questions is contested but positive [N30], and mind-wandering rises over a long lecture [N31]. The data comes from MOOC sessions measured by proxies [N1]. **[Recommendation]** Every FormatSpec therefore carries `max_segment_s`. Detailed stays ~10 minutes as a product but is built as chapters of at most 6 minutes, separated by the existing interaction loop and protected think windows (RD-11). **[Hypothesis]** This chaptering keeps total watch time closer to the under-6-minute curve. The A/B in section 10 will test it.

| Format | Kind | Source KUs | Shape (FormatSpec) | Voice (CE-L2) | Validation delta |
|---|---|---|---|---|---|
| **Detailed** | Primary | All KUs for the objective set, incl. misconception KUs | ~10 min as chapters ≤6 min; Super Teacher 10-min structure; head-in moments [N4], continuous drawn visual flow [N5] | Path A | Full: GV + GA-{family} + H-SB + GF |
| **Simplified** | Derived | Concept + one worked example + misconception KU, lower level band | Shorter; simpler language rule from the LevelProfile | Path B | Closure check; GA only if a KU is rewritten beyond lexical simplification (a simplification can change meaning, so the academic owner spot-checks it in GF) |
| **Recap** | Derived | Fact-set/reference KUs + objective statements | Single segment; recall prompts | Path B | Closure check + GF |
| **Question Analysis** | Primary for its question KU | Question+marking-scheme KUs; worked-solution KUs | Problem → think window → solution → common errors → marking note | Path B | Answer key verified by the family validator (solver/fixture for STEM; scheme-grounded rubric for others); the official marking scheme is stored separately from any ExamLeaf rubric (RD-30) |
| **Shorts/Reels** | Derived | One KU (often a misconception or hook) | 20–60 s vertical; one claim cluster | Path B | Closure check + GS |
| **Misconception Buster** | Derived | Misconception KU + the correcting claim | Elicit the wrong belief → test it → resolve. Misconceptions are a core pre-scripting design step [N73]; ignoring them gives an "illusion of understanding" [N74][N76] | Path B | Closure + GS/GF |
| **Prerequisite Bridge** | Derived | KUs of `prerequisite_of` items from the CG | Short refresher placed before a Detailed lesson | Path B | Closure + GF |
| **Worked Example / Derivation Walk** | Primary (STEM, commerce) | Worked-example KUs | Step-by-step with fixture-verified intermediate values | Path B | Fixture/solver |
| **Activity / Virtual Lab** | Primary | Activity KU; safety notes as claims | Real-life opener, activity, check-understanding questions (the textbook pattern [N37]) | A for Class 1–5, else B | Fixture + safety-claim review |
| **Story / Song (Class 1–5)** | Primary | Story KU bound to outcome GUIDs | Multi-modal: speaking, drawing, singing, playing [N10] | Path A (CE-L9) | GA + child-development reviewer |
| **Source Analysis (humanities)** | Primary | Source-analysis KU + primary-source record | Show the source, ask what it says, then what historians infer (attributed) | Path A for flagship, else B | Humanities VP (attribution required) |
| **Perspectives (contested topics)** | Primary | Claims marked `contested` with attributed positions | Each position stated with its attribution; no verdict unless the board prescribes one, and then labelled as such | Path B | Two qualified reviewers (section 5.3) |
| **Language Drill** | Primary | Grammar/pronunciation KUs | Model → repeat window → contrast pairs | Path A for Indic languages until TTS passes the native gate (CE-L5) | Language VP + native editor |
| **Case Study (commerce/UG)** | Primary | Case KU + numerical claims | Situation → analysis → decision; 16:9 allowed if the format declares it | Path B | Commerce VP |
| **Exam Strategy / Paper Walkthrough** | Primary | Blueprint associations from the CG + question KUs | Pattern analysis of an exam paper | Path B | Exam-strategy VP (claims about patterns must cite the published paper/scheme) |
| **Revision Sprint (chapter/unit)** | Derived | Recap KUs across a CG subtree | Chained Recaps with interpolated questions | Path B | Closure + GF |
| **Lecture Segment (UG/PG, 16:9)** | Primary | Concept/derivation KUs at UG/PG depth | Declared 16:9 at the format level only (CE-L7); still ≤6 min chapters | Path A for flagship, else B | Full |
| **Formula / Fact Card video** | Derived | Reference KUs | Static-heavy, very short | Path B | Closure + GS |

Adding a format means one FormatSpec file, its structure template, its A-check thresholds and one golden render. There is no pipeline change. **[Recommendation]**

## 4. Levels: Class 1 to Masters and competitive exams

Level Profiles bind to CG stages. The board's own framework document is the authority. The bands below use NCF-SE stage spans where the evidence gives them: Preparatory = Grade 3–5 [N8], Middle = Grades 6–8 [N32]. Band boundaries for other boards come from that board's framework in C1, never from this table.

| Band | Pedagogical constraints (sourced) | Profile settings [Recommendation] |
|---|---|---|
| **Class 1–2** | Boundaries and pedagogy taken from the board's foundational-stage document when it is imported into C1 (not in the current evidence set) | Made-for-kids (CE-L9): no data collection, no ads targeting; strictest motion/flash class; Path A only; shortest formats; Story/Song/Activity primaries; child-development reviewer mandatory in GA and GF |
| **Class 3–5 (Preparatory)** | Play-way, discovery, activity-based pedagogy while textbooks are introduced "without overwhelming children" [N9]; multi-modal [N10]; real-life and cultural context [N11] | As above (CE-L9 covers all of Class 1–5); Activity and Story primaries; Detailed is shorter than the Class 9+ version and decided by the child-development reviewer **[Hypothesis]**; the textbook is one resource among many [N12] |
| **Class 6–8 (Middle)** | Shift to abstract ideas and unfamiliar contexts [N53]; methods of inquiry per discipline over fact accumulation [N54]; reasoning-focused assessment [N55]; content-to-competency shift [N56]; nine subjects incl. three languages [N33]; balance of direct instruction and inquiry [N34]; cross-cutting themes [N35] | Each KU must name its discipline's "form of understanding"; Question Analysis targets reasoning, not recall; Misconception Buster and Activity are first-class; Dive-Deeper-style optional extension KUs, following the recurring-box taxonomy [N38] (contested evidence) |
| **Class 9–10, 11–12** | Current Assam Board scope; board exam blueprints | Current defaults (vertical 1080×1920, Super Teacher structure); CG `assessed_by_blueprint` associations drive Question Analysis and Exam Strategy |
| **UG** | Discipline depth; source/derivation rigour | 16:9 Lecture Segment allowed per format; claim ledger requires scholarly/textbook-tier sources; reviewer = subject specialist holding at least a postgraduate degree in the discipline **[Recommendation]** |
| **Masters** | Research-frontier claims, contested scholarship | Exceptional-claim rule (multiple high-quality sources) [N17] applied more often; Perspectives format common; two specialist reviewers for contested claims |
| **Competitive exams** (cross-band) | Modelled as **exam frameworks** in the CG (syllabus items + blueprint associations), crosswalked to board items [N50] | Exam-strategy VP; claims about exam patterns cite the official notification/paper; no predictive claims ("will come") without stated evidence |

Speaking rate is set per Level Profile and locale, not taken from the edX finding. That evidence is contested [N6][N29], and its adult MOOC population [N1] does not transfer to Class 1–5. **[Hypothesis]**

## 5. Validating subject families beyond STEM

### 5.1 Family registry and profiles

| Family | Evidence type | Automated validators | Citation rules | Reviewer (in-house) |
|---|---|---|---|---|
| **STEM-quantitative** (maths, physics, chemistry) | Executable fixtures (existing four validated models), solvers | Fixture execution, unit/dimension checks, renderer-independent science data (existing) | Textbook/board source for definitions and conventions | Subject teacher (existing GA) |
| **STEM-life & earth** | Fixtures where modelable; otherwise ledger | Fixture + claim ledger | As above + peer-reviewed or textbook tier for facts beyond the syllabus | Subject teacher |
| **Humanities & social science** (history, geography, civics/political science, sociology) | Claim ledger | Claim flagger [N43]; span-hash match (the quoted span exists in the cited source); date/name consistency across KUs | Every date, name, quantity, quotation and causal claim cites a source; interpretations are attributed; Wikipedia not citable [N19] | Discipline-qualified reviewer; second reviewer for `sensitive` |
| **Languages & literature** | Text record + ledger | Grammar/orthography checker per locale; quote-length and rights check; lexicon | Primary text edition hash for every quotation; critical interpretations attributed | Native-language subject editor (exists in GA for localized scripts) |
| **Commerce & management** (accountancy, business studies, economics) | Ledger + numeric fixtures | Ledger-balance/numeric recomputation as fixtures; statute/standard references checked against the registered copy | Rules and standards cite the registered edition with date (they change) | Qualified commerce teacher |
| **Arts, music & physical education** | Ledger + demonstration record | Safety-claim flagging (PE); technique claims attributed | Technique and history claims sourced; performance demos credited | Practitioner-teacher |
| **Vocational & applied** | Ledger + procedure fixtures | Procedure-step completeness; safety claims mandatory | Official vocational curriculum and safety standards cited by edition | Trade-qualified instructor |
| **Exam strategy & aptitude** | Ledger tied to official papers | Pattern claims recomputed from the stored paper set | Official notifications/papers only for pattern claims | Academic lead |
| **Foundational integrated (Class 1–5)** | Ledger + activity safety | As the parent family + CE-L9 checks | Board textbook as primary authority | Child-development reviewer + subject teacher |

### 5.2 Claim-ledger rules (all non-STEM families; STEM for non-fixture claims)

**[Recommendation]** These rules are adopted from verifiability practice:

1. **The claim author carries the burden of proof** [N13]. In the pipeline the drafting agent must attach a source and span or the claim does not enter the ledger.
2. **Unsourced claims are removed by default** [N14]. The closure check fails any sentence that the flagger marks as needing a citation [N43] and that has no claim ID.
3. **Truth is not enough; the claim must be published in a reliable source** [N15]. Model "knowledge" is never a source.
4. **Paywalled or costly sources are not rejected for that reason** [N16]. The Source Registry stores a hash of the consulted copy so a reviewer can re-check the span.
5. **Exceptional claims need multiple high-quality sources** [N17]. `risk: exceptional` requires two or more independent sources.
6. **No self-published source about living people** [N18]. This is enforced as a schema rule on `Source`.
7. **No encyclopaedia-wiki citations** [N19]. It may be used for discovery, never as a source.
8. **Corroborate against reliable secondary sources** [N39].

The automated flagger is a triage stage, not a validator. Citations are often missing even in policy-governed corpora [N40], and the model's robustness across quality classes was tested rather than guaranteed [N44]. Human-only checking is uneven [N45], so the design is **flagger + span-hash check + qualified reviewer**, never any one of them alone. The flagger and span matcher are Kit tasks run on the cheap cascade (CE-L6). Strong models act only as offline judges.

### 5.3 Contested-claim handling

**[Recommendation]** Each claim gets one `contested_status`:

- **settled**: normal rules.
- **attributed**: an interpretation stated with its holder ("According to …").
- **contested**: positions in scholarship differ. Use the Perspectives pattern: each position is attributed and sourced and no verdict is given. Two qualified reviewers must approve. Any Short derived from it must carry at least the attribution, and a Short may not state one side as fact.
- **board-vs-scholarship**: the prescribed textbook differs from current scholarship. The video states the board's version as "the syllabus states …" (it is exam-relevant) and adds the attributed scholarly position. The academic lead decides whether to include the second, and the decision is recorded on the claim.

Any reviewer can escalate a claim to `contested`. Escalation freezes the dependent artefacts at their current gate. Revisions follow the editorial principle of regular integration of new research [N62]. Re-review is triggered when a cited source changes (new edition hash), which reuses CE-L10 invalidation.

### 5.4 Reviewer rubrics

Each VP ships a rubric with the same structure:

- accuracy (claim-level)
- attribution
- level-appropriateness
- misconception coverage [N73]
- bias/sensitivity (humanities)
- safety (PE/vocational/activities)
- exam alignment

Britannica's five editorial roles (fact checker, subject editor, supervisory, copy, information architect) [N63] are contested as evidence. **[Hypothesis]** They still map usefully onto in-house roles:

- the flagger plus reviewer act as fact checker;
- the qualified reviewer is the subject editor;
- the academic lead is the supervisory editor;
- the native editor is the copy editor;
- the founder-engineer owns the CG and registries (information architect).

Reviewer time is a capacity metric (85 min/lesson baseline, RD-41). Claim-level review is paid once per objective and reused across formats. **[Hypothesis]** This makes derived formats cost mainly GF/GS watch time. Pilot timings will confirm or refute it.

## 6. Languages and locales

- **Claims are language-independent records.** `text_pivot` holds the approved claim. Translations are bound to the claim ID, and each translation is approved by the native-language subject editor (already a GA role). A translation change invalidates only that locale's artefacts.
- **The Locale Profile** carries the existing locale gate (API request + native review + lexicon), plus per-family glossaries (for example, a Hindi chemistry glossary differs from a Hindi history glossary), numeral and script rules, and voice identity.
- **GL-family**: the first artefact in any (locale × family) pair needs glossary approval.
- **Launch locales** are en-IN, Hinglish and hi-IN (CE-L5/RD-42). Assamese and other Indic languages ship with a human voice (Path A) until a TTS passes the native-speaker gate.
- **Language-as-subject** (literature, grammar) uses the Languages VP. Language-as-medium uses the Locale Profile. The two are never conflated: a Hindi-medium physics lesson is STEM-validated plus a hi-IN locale, while Hindi literature is Languages-validated.
- **Multi-language curricula.** Middle Stage requires three languages, at least two native to India [N33]. The CG therefore models a language subject per framework, and the Locale Registry must grow by adding profiles, never by changing code.

## 7. Reuse, extend, retire (sections 01–14)

| Section | Verdict | Detail |
|---|---|---|
| 01 business model | **Reuse, boundary hardened** | Sole home of entitlement/pricing/free-chapter policy (CE-L1, RD-49); RD-44 out of pipeline scope |
| 02 learning-psychology rules + tokens | **Extend** | Rules become Level Profile and Format Spec fields; tokens unchanged; add the `max_segment_s` ≤6-min rule [N3][N28] |
| 03 Super Teacher framework | **Extend** | The 10-min structure becomes the Detailed `structure_template`; the explanation ladder maps to KU ordering; the interaction loop fills chapter breaks [N30]; delivery modes map to format/level choices |
| 04 video engine v2 | **Reuse + extend** | Contracts kept. LessonPlan/SceneSpec gain `objective_guids`, `claim_ids`, `format_id`, `level_band`, `family`. The four validated models become the first entries in the STEM VP fixture library. RD-35 (allowed set of kinds per subject) becomes per-family. 56 tests must stay green |
| 05 narration system | **Reuse + extend** | Lexicon extended with per-family glossaries; provider compiler unchanged; 58 tests must stay green |
| 06 skills library (72) | **Extend** | Add skills: `cg-import`, `claim-ledger-draft`, `citation-flag`, `span-verify`, `derivation-closure-check`, `vp-{family}-review-pack`. The ownership map gains the CG/registry owner |
| 07 master runbook | **Extend** | Gate map gains H-CG, GV-claims, GA-{family}, GL-family; RD-51 implemented here; H-SB unchanged |
| 08 cost workbooks | **Extend** | Cost per (objective × family) for validation plus cost per derived artefact; reviewer minutes as a capacity line |
| 09 evidence register | **Reuse + extend** | Becomes a seed of the Source Registry schema; N1–N76 added |
| 10 pilots | **Reuse** | Existing STEM pilots become regression goldens |
| 11 human-feel playbook | **Reuse** | Path A/B as decided (CE-L2); disclosure unchanged |
| 12 animation layer | **Reuse** | Seek-deterministic harness, cue sheets, A-checks; style guides gain a level/motion-class dimension (Class 1–5 strictest) |
| 13 strong-to-cheap | **Reuse** | Production Kit gains claim-ledger and closure-check tasks; cascade unchanged; Ultracode banned except the one attended $50 probe (CE-L3) |
| 14 audit | **Reuse** | Its fixes stand; the audit checklist gains family/level/locale coverage |
| **Retire** | — | `syllabus-map.json` as a free-form file (folded into the CG); the one-kind-per-subject assumption (RD-35); every free/paid or "first-three-free" field in engine metadata (CE-L1); single-block 10-minute renders without chapter boundaries |

## 8. Build order with gates

Each phase ends with a gate. No phase starts with a red regression suite (56 engine + 58 narration tests + goldens).

| Phase | Scope | Exit gate |
|---|---|---|
| **CE0 Schemas** | JSON Schemas for all nine record types; hash/dependency capture in the approval service; neutral-metadata export; strip any commercial fields | All existing tests green; an invalidation demo (change a FormatSpec, see the affected artefacts listed) |
| **CE1 Curriculum Graph** | Hand-author the Assam Board Class 10–12 STEM frameworks into the CG with GUIDs and prerequisite edges; CASE-shaped so a future CASE provider import is a mapping, not a rewrite [N66][N68][N72] | H-CG approved by the academic owner for one chapter |
| **CE2 STEM VP + KUs** | Wrap the four fixtures as the STEM VP; refactor one existing pilot lesson into KUs; compile Detailed + Short from them | Byte-identical (or A-check-equivalent) render vs the existing pilot; GA/GF pass |
| **CE3 Derived formats** | Closure check; Simplified, Recap, Question Analysis, Misconception Buster from the CE2 KUs | Each passes GF/GS; the closure check catches an injected unsourced claim (negative test) |
| **CE4 First non-STEM family** | Source Registry + Claim Ledger + Humanities VP on one Class 10 social-science chapter, including one contested/attributed claim | GV-claims + GA-humanities pass; flagger recall measured against reviewer findings |
| **CE5 Young learners** | Class 3–5 Level Profile, made-for-kids export flags, Path A, child-development reviewer, one Story/Activity artefact | GA + GF with the child-development reviewer; motion-class checks pass |
| **CE6 Locale scale-out** | hi-IN + Hinglish per-family glossaries (STEM, humanities) | GL-family passes for both |
| **CE7 Higher ed** | UG Lecture Segment (16:9 FormatSpec) in one STEM and one commerce topic | Full gates; aspect handled by the format only |
| **CE8+** | One registry entry at a time: each new family, board, exam framework or locale | Its own GV/GA/GL gate; no code change unless a new validator kind is needed |

## 9. Risks

1. **Over-modelling the graph before content exists.** Mitigation: files first, one board, one chapter; add a database only on measured need (ponytail rule).
2. **Reviewer capacity across many families.** In-house review is $0 cash but finite (RD-41). Every new family needs a *qualified* reviewer, which a small team may not have. A VP must not be activated without a named qualified reviewer; this is a hard rule. Derivation-closure is the main throughput lever, and it is unproven **[Hypothesis]**.
3. **Over-trusting automated claim flagging.** Robustness varies by content quality [N44]. Mitigation: flagger + span-hash + human; measure recall in CE4.
4. **Board-vs-scholarship conflicts and politically sensitive history.** Handled by explicit `contested_status` and the attribution policy. Residual reputational risk remains; the academic lead's decision is recorded on each claim.
5. **Rights.** Literature texts, primary sources and textbook spans need rights records. H-S2 stays mandatory and quotation length is checked.
6. **CASE availability for Indian boards is unknown.** **[Hypothesis]** Most frameworks will be hand-authored. CASE is used as a shape, not a dependency.
7. **Evidence transfer.** The engagement evidence comes from MOOC adults using proxy measures [N1][N7]. The young-learner and Masters settings need ExamLeaf's own measurements (pre/post tests to detect illusion of understanding [N74]).
8. **Contested numbers in the evidence.** The speaking-rate [N6][N29], interpolated-question [N30] and time-allocation [N58] findings are contested. None of them becomes a hard gate threshold without pilot data.

## 10. Experiments that decide the open hypotheses

- **Chaptered vs single-block Detailed**: watch-through and post-video problem attempts (the edX proxies [N1]), plus a pre/post concept test.
- **Derived-format review minutes**: minutes for GF/GS on derived formats vs primaries (validates the derivation-closure economics).
- **Flagger recall/precision** vs qualified-reviewer findings per family.
- **Path A vs Path B** A/B per CE-L2 (existing 11 §8 plan), stratified by level band.
