# Architect plan 4 — lens: pedagogy-by-stage-and-safety-first

**Lens statement:** pedagogy-by-stage-and-safety-first

**Thesis:** One pipeline can serve Class 1 through Masters if no stage rule is ever hard-coded. Who the learner is lives in versioned, hash-bound registry entries: Level Profile, Audience Safety Class, Persona, Accessibility Profile, Subject Family Profile and Locale Profile. These are compiled together with a Format Spec into one Effective Production Profile (EPP) per artefact. Every author, the Production Kit, the cascade and every validator reads only the EPP. Stage-specific gates (child-development, safety, family accuracy) attach to the profile, never to the lesson. Today's Assam Class 10–12 STEM rules become the first two Level Profiles, ported with zero behaviour change. Every number for younger or older learners starts as a labelled hypothesis, because the evidence register is mostly adult MOOC data.

**Biggest risk:** Level Profile values for Class 1–8 (segment length, pacing, density, interaction cadence) have no direct evidence in the register, because the quantitative evidence is adult MOOC data. If wrong defaults are hash-bound into thousands of child-directed artefacts before pilots and the child-development reviewer confirm them, the result is mass rework or quietly bad pedagogy for the youngest learners. There is a second risk in the same area: children's-data law scope may be misjudged, because India's DPDP Act treats anyone under 18 as a child, while store made-for-kids regimes use under-13. If only Class 1–5 is treated as children, Class 6–12 content is under-protected.

---

# ExamLeaf Content Engine v2: pedagogy by stage, safety first

## 1. Thesis

The engine should not know whether a lesson is for a 6-year-old or a postgraduate. It should know only which **Effective Production Profile (EPP)** to obey. An EPP is compiled from these registry entries:

- **Format Spec**: what is being made.
- **Level Profile**: who is learning, and how they attend, read, pace and interact.
- **Audience Safety Class**: what legal and child-safety envelope applies.
- **Persona Profile**: who is speaking.
- **Accessibility Profile**: who must not be excluded.
- **Subject Family Profile**: how truth is established.
- **Locale Profile**: in what language and script.

The engine compiles one EPP per artefact, hashes it and binds every approval to that hash (CE-L10). Authors, the Production Kit, the Haiku→Sonnet→Opus cascade and all validators read only the EPP. That is how one pipeline makes a Class 2 song-led concept and a Masters paper explainer without branching code.

Three principles follow from this lens:

1. **Pedagogy is data, not code.** The rules in section 02 (pacing, density, interaction) and section 03 (persona, explanation ladder, interaction loop) were written for teenagers. They become the *Class 9–10 and 11–12 Level Profiles*, and other stages get their own profiles.
2. **Safety is not commerce.** CE-L1 bans free/paid logic. It does not ban knowing the audience's age band. Audience Safety Class is neutral metadata, like subject or language. The platform layer turns it into store flags (for example made-for-kids), data rules and ad rules. The pipeline guarantees that the *content itself* is safe for that class.
3. **Unproven numbers are labelled, not frozen.** Most of the quantitative engagement evidence is from adult MOOC learners ([N1], [N2], [N26]–[N31]). Every Level Profile value for younger learners starts as **[Hypothesis]** with an owner and a pilot that confirms it. No number in this plan is invented. Where the evidence register has no number, the value is "calibrate in pilot".

---

## 2. Architecture from this lens

### 2.1 Components

| # | Component | Role | Builds on |
|---|---|---|---|
| C1 | **Profile Registry** (git-versioned YAML plus a JSON Schema per entry type) | Stores Format, Level, Safety Class, Persona, Accessibility, Subject Family, Locale and Style entries. Every entry has an id, a semver and a content hash. | 04 typed contracts; 12 `style_tokens.json`; 02 design tokens |
| C2 | **Profile Resolver** | Compiles (format × level × family × locale × persona) into an EPP. It rejects invalid combinations through an explicit compatibility matrix and records the hash of every input entry. | new, small, pure function |
| C3 | **Competency Graph** | Curriculum nodes (board → class → subject → chapter → learning outcome), each with a stable GUID, a parent/child hierarchy and cross-board associations. It follows the CASE information-model shape [N46]–[N50], [N67]. | new. Import/export through the CASE REST binding [N52], [N68] is deferred until a partner needs it |
| C4 | **Concept Atom store** | Self-contained, typed teaching units (concept, worked example, misconception, check question, activity) that formats assemble, in the DITA topic model [N21], [N22], with conref-style reuse [N24]. A fix to one atom propagates to every format that uses it, and CE-L10 re-QA follows automatically. | 04 LessonPlan/SceneSpec |
| C5 | **Stage Validators** (deterministic, no LLM) | Level linter, density linter, interaction-cadence checker, motion/flash analyser, safety linter, accessibility checker, persona-rule linter. | 02 checklist §K; 12 edge cases; 14 audit |
| C6 | **Family Accuracy Gate** | STEM fixtures (04 scientific models) or source-grounded claim ledgers per CE-L8. | 04, 09 |
| C7 | **Human Gate Router** | Picks the required approvers from the EPP: storyboard gate H-SB (existing), plus a level/child-development reviewer, a safety sign-off and a family-qualified reviewer. All are bound to hashes. | 07 two gates + H-SB + disclosure gate |
| C8 | **Impact Analyser** | When a registry entry changes, it walks EPP hash → artefacts and lists exactly which approvals are void. This scopes re-QA instead of re-reviewing everything. | CE-L10 |
| C9 | **Neutral Export** | Emits media plus a sidecar with subject, level, format, language, version, hashes, `audience_class`, accessibility tracks and disclosure. No price or entitlement fields (CE-L1). | 07 export |

### 2.2 Data model (essential fields only)

```yaml
LevelProfile:            # e.g. level/L4-class9-10@1.0.0
  id, version, hash
  stage_ref: NCF stage    # Foundational / Preparatory [N8] / Middle [N32] / Secondary
  audience_class: AC0|AC1|AC2
  attention:
    max_segment_s         # chapter length; per-level value, labelled
    max_continuous_new_ideas_per_segment
  pacing:
    wpm_bands: {ordinary, recap, dense}   # 02 §G2 values for L4/L5; calibrate others
    pause_bands                           # 02 §G3
  language:
    lexicon_ref           # controlled vocabulary for level × locale
    max_sentence_tokens, max_new_terms_per_scene, abstraction_ceiling
  interaction:
    cadence_rule, allowed_types[], response_mode  # think/say-aloud/draw/write/move
  on_screen:
    max_text_elements, max_unexplained_relationships (02 §B3), min_type_px, caption_policy
  motion: {flash_policy_ref, reduced_motion_required: true, max_visual_change_rate}
  persona_ref, voice_path: A|B|either     # CE-L2/CE-L9 constraint
  required_reviewers[]                    # e.g. child_dev for L1/L2
  evidence: [{field, tag: Recommendation|Hypothesis, source: N#|section-ref}]

FormatSpec:              # format/recap@1.2.0
  id, purpose, allowed_levels[], aspect: 9:16|16:9 (CE-L7), duration_rule (per level),
  structure_template (ordered atom types), interaction_min, voice_path_default,
  required_gates[], derivable_from[] (e.g. Recap derives from Detailed atoms)

AudienceSafetyClass:     # safety/AC0@1.0.0
  content_rules[], prohibited_elements[], flash_policy, data_solicitation: forbidden,
  external_links: forbidden|allowed, disclosure_variant, required_signoffs[]

PersonaProfile:          # persona/super-teacher-junior@1.0.0
  base: 03 Super Teacher, register, warmth, humour_ceiling (03 §5.2), retired_expressions,
  call_and_response_rules, voice_refs[] (05/11 licensed voices), locales[]

SubjectFamilyProfile:    # family/social-science@1.0.0
  validation_mode: fixture|claim_ledger|executable|hybrid, source_policy,
  reviewer_qualification, sensitivity_checks[], as_of_date_required

LocaleProfile:           # locale/hi-IN@1.0.0
  script, font_stack, numerals, lexicon_ref (05), code_mix_policy,
  tts_eligible (native-speaker gate, CE-L5), caption_line_rules, readability_method

EPP: { input_refs{entry_id: hash}, resolved_constraints{...}, epp_hash }
Artefact.metadata += { level_id, format_id, family_id, locale_id, persona_id,
                       audience_class, epp_hash, competency_guids[] }
Approval += { epp_hash, reviewer_role }   # an approval is void if epp_hash changes
```

[Recommendation] Extend the existing 04 contracts (LessonPlan, SceneSpec, ShortSpec, Approval) with these fields instead of creating parallel types. ShortSpec becomes one instance of FormatSpec.

### 2.3 Flow

1. **Request**: competency GUID(s) + format + level + locale.
2. **Resolve**: C2 builds the EPP, or rejects the request with a reason (for example "Question Analysis is not defined for L1"). The EPP hash is fixed here.
3. **Plan**: the strong-model compiler (CE-L6) writes the LessonPlan from atoms under EPP constraints. The plan must name, in advance, the misconceptions it addresses. Misconception-first design is a core step [N73], [N74], [N76] and is already rule 02 §I3.
4. **Accuracy pre-gate**: the family gate (C6) runs on the atom claims *before* any media spend.
5. **Storyboard gate H-SB**: the reviewer set comes from the EPP (§2.4).
6. **Produce**: the Kit plus the cascade write per-scene scripts and cue sheets. Narration follows Path A or B as the EPP dictates.
7. **Validate**: all C5 validators run on the script, the cue sheet and the rendered frames.
8. **Render** in the pinned Linux container with the seek-deterministic harness (CE-L4, CE-L7).
9. **Final gates**: the existing two human gates, the disclosure gate, and the EPP-specific sign-offs.
10. **Neutral export** (C9).

### 2.4 Gates by audience

| Gate | AC2 (UG/PG/adult) | AC1 (Class 6–12, under-18 teen) | AC0 (Class 1–5, child-directed) |
|---|---|---|---|
| Family accuracy (CE-L8) | required | required | required |
| H-SB storyboard | required | required | required + child-development reviewer co-signs |
| Level fit (reading, pacing, density) | automated + academic reviewer | automated + academic reviewer | automated + child-development reviewer |
| Safety linter | report | blocking | blocking, zero-tolerance list |
| Motion/flash analyser | blocking | blocking | blocking at stricter AC0 thresholds |
| Disclosure gate | adult variant | teen variant | child variant (age-appropriate wording) |
| Voice path | A or B per format | A or B per format | **Path A only** (CE-L2, CE-L9) |

---

## 3. Level Profiles: Class 1 to Masters

Level boundaries follow NCF-SE stages so they match how Indian boards write outcomes: Preparatory = Grades 3–5 [N8] and Middle = Grades 6–8 [N32]. CE-L9 groups Class 1–5 together for safety; pedagogically they split into **L1 (Class 1–2)** and **L2 (Class 3–5)**. Grades 1–2 belong to the Foundational stage of the NEP 5+3+3+4 structure, which is not yet in the evidence register (add it to section 09).

**Profile defaults by level, part 1: Class 1 to 10**

| | **L1 Class 1–2** | **L2 Class 3–5** | **L3 Class 6–8** | **L4 Class 9–10** |
|---|---|---|---|---|
| **Audience class** | AC0 | AC0 | AC1 | AC1 |
| **Segment / attention** | Shortest of all levels. [Hypothesis] Calibrate with the child-development reviewer. The ≤6-min evidence [N2], [N26] is an adult ceiling, not a child target. | [Hypothesis] ≤ L3. Play-way and activity-based [N9]. | Chapters under 6 min [N3], [N28]. | Existing 10-min lesson split into chapters under 6 min [N3], [N27]. |
| **Pacing** | Calibrate. Path A teacher sets the natural pace. | Calibrate. Path A. | Start from 02 §G2 bands. [Hypothesis] Validate. | 02 §G2: 130–155 wpm ordinary, slower for dense terms (production hypothesis). |
| **Reading / vocabulary** | Pre-reader. Narration carries all meaning; on-screen text is single words or icons. | Early reader. Grade-appropriate language in real-life context [N11]. | Shift to abstraction [N53]. Inquiry methods over facts [N54]. | Board terminology plus a glossary. |
| **Interaction** | Say-aloud, point, move, sing [N10]. | Draw, act, predict, sing [N10]. | Predict-explain-check [N37]. Reasoning prompts [N55]. | 03 interaction loop. Self-explanation (02 §C4). |
| **On-screen density** | One idea per frame. | One dominant focus (02 §B2). | 02 §B3 relationship count. | 02 §B3, §E2. |
| **Persona** | Super Teacher Junior | Super Teacher Junior | Super Teacher Coach | Super Teacher (current) |
| **Voice path** | A only | A only | A or B per format | A or B per format |
| **Reviewers** | child-development + family | child-development + family | academic + family | academic + family |

**Profile defaults by level, part 2: Class 11 to Masters**

| | **L5 Class 11–12** | **L6 UG** | **L7 PG / Masters** |
|---|---|---|---|
| **Audience class** | AC1 | AC2 (mixed-age: AC1 rules for the under-18 first year) | AC2 |
| **Segment / attention** | Same as L4, plus derivation deep-dives as separate formats. | Chapters under 6 min, even inside long lectures [N31]. | Same. Long lectures exist only as chaptered playlists. |
| **Pacing** | 02 §G2 | [Hypothesis] Faster bands allowed; [N6] and [N29] are contested. | Same. |
| **Reading / vocabulary** | Discipline register. | Disciplinary register plus notation conventions. | Research register plus citations on screen. |
| **Interaction** | Retrieval + worked → faded examples (02 §C3). | Interpolated questions between segments ([N30], contested). | Pause-and-critique of claims or methods. |
| **On-screen density** | 02 §E2 | Higher density allowed in 16:9 lecture formats. | Same. |
| **Persona** | Super Teacher Mentor | Lecturer | Seminar Lead |
| **Voice path** | A or B per format | A or B per format | A or B per format |
| **Reviewers** | academic + family | subject-qualified (UG) | subject-qualified (PG or above) |

**Competitive-exam levels (JEE/NEET-style, UPSC-style, and so on) are an overlay, not a Level.** An **Exam Overlay** profile sits on top of a base level (typically L5 or L6). It adds:

- the official pattern reference and syllabus GUIDs;
- an as-of date for patterns and marking schemes;
- a strategy register in the persona (Exam Strategist variant);
- question-provenance rules: past-paper questions cite paper and year, and original questions are marked as original.

It never changes the accuracy gate. [Recommendation] Treating exams as an overlay avoids combining every exam with every level.

**Rules that apply across all levels:**

- [Recommendation] **Chaptering is mandatory.** The ~10-minute lesson stays as the delivery unit for L4/L5. Internally it is built from segments that each stand alone, each ending in a check, because engagement falls sharply past 6–9 minutes [N27], [N28] and interpolated questions help ([N30], contested). This also turns segments into reusable atoms for Recap and Shorts.
- [Recommendation] **Middle Stage tone shift.** L3 balances direct instruction with exploration [N34], [N54]. Each chapter opens from a real-life situation and follows each activity with a check-understanding question [N37], and assessment targets reasoning, not recall [N55]. The Coach persona is less performative than Junior and more Socratic than the current Super Teacher.
- [Hypothesis] **Pace and age.** The speaking-rate evidence ([N6], [N29]) is contested and comes from adult MOOC data. It must not be used to speed up L1–L3. Every L1–L3 pacing value ships with an A/B plan reusing the method in 02 `AB_EXPERIMENTS_and_EVALUATION.md`.

### 3.1 Narration persona variants

All personas inherit the section 03 core: scaffolding over charisma, calibrated confidence, never fabricating the student's response (03 §4.3), and a humour ceiling rather than a quota (03 §5.2). Variants override only register, call-and-response and expression lists.

- **Super Teacher Junior (L1–L2).**
  - Warm and slow, with real call-and-response pauses and songs and rhymes where the atom allows [N10].
  - Praise names the action ("you counted all five"), never the child's identity (02 §H4).
  - Never asks for anything that could be personal data ("tell me your name", "what school").
  - Human teacher only (Path A).
- **Super Teacher Coach (L3).** Inquiry questions, "what would happen if…", experiment framing.
- **Super Teacher (L4).** The current section 03 persona, unchanged.
- **Super Teacher Mentor (L5).** Exam-aware, deeper derivations, fewer hooks.
- **Lecturer (L6).** Fewer interjections, explicit notation and definitions, talking-head inserts at transitions [N4], drawn derivations [N5].
- **Seminar Lead (L7).** Cites sources on screen, models critique, states uncertainty explicitly.
- **Exam Strategist (overlay).** Time management and elimination tactics, never "tricks" that bypass understanding.

[Recommendation] The persona-rule linter checks scripts against each persona's retired-expression list and register rules. This is the guard against cheap-model persona drift in the cascade.

---

## 4. Child safety, legal and accessibility rules

### 4.1 Audience Safety Classes

- **AC0, child-directed (L1–L2).** Platform exports set made-for-kids flags from `audience_class`; the pipeline never sets them. Content rules (blocking):
  - no data solicitation of any kind (no names, schools, photos, comments);
  - no external links or QR codes;
  - no brand names, logos or product placement;
  - no calls to like, subscribe, comment or share;
  - no urgency, fear, peer-comparison or streak pressure (02 §H5);
  - no generated faces of real-looking children;
  - activities only with household-safe materials, and an "with a grown-up" cue on any physical activity;
  - age-appropriate disclosure of AI assistance;
  - stricter flash and motion policy, with a reduced-motion variant always rendered.
- **AC1, minor teen (L3–L5 and the first UG year).** Same rule set, but external links are allowed only to official board or government sources, and sensitive-topic (health, mental health, safety) review is required.
- **AC2, adult (UG/PG).** Standard rules plus sensitivity review per family.

[Recommendation] Escalate to counsel before Phase 4. Two legal facts change scope and are **not** in the evidence register:

1. India's Digital Personal Data Protection Act treats anyone under 18 as a child for data purposes, so AC1 is also "children's data" in India. This is a platform-layer concern, but it means the pipeline's no-solicitation rule should cover AC1 too.
2. Store made-for-kids regimes (YouTube, COPPA) use different age cut-offs.

Record both in section 09 with primary sources before freezing AC rules. The pipeline's job stays neutral: correct `audience_class` metadata plus safe content. Data collection, ads and targeting are enforced only downstream (CE-L1, CE-L9).

### 4.2 Talent and voice consent

- Path A teacher recordings and licensed brand voices already need releases (section 11).
- **New:** if any child appears or is heard (for example a peer voice in an L1 song), get a guardian release stored with the artefact hash. [Recommendation] Default to no child talent at all; the teacher voices both roles.

### 4.3 Motion and flash

- Run the existing harness edge case #56 (no full-frame flashes) and the 12 style-guide rules as a **frame analyser** over rendered output: luminance and red-flash transitions per second, measured on the deterministic render.
- [Recommendation] Adopt WCAG 2.3.1 (Three Flashes or Below Threshold) as the AC1/AC2 floor. For AC0 the policy is "no flashing elements at all". This is stricter than the standard, so it needs no new number.

### 4.4 Accessibility Profile (all levels)

These items are already in 02 §D7/§J; the new parts are noted.

- Accurate captions in a protected zone and a transcript.
- WCAG contrast of 4.5:1 for text and 3:1 for essential graphics, checked against 02 tokens.
- Reduced-motion variant.
- **New:** a "visual-essential" flag on SceneSpec. Any meaning carried only by visuals must be spoken in narration or placed in an audio-description track, and the validator blocks unflagged silent visuals.
- **New:** caption policy per level. L1 captions exist for hearing access but are never needed to follow the lesson; L2–L3 caption line length is shorter (calibrate).
- [Hypothesis] Dyslexia-friendly type choices for L1–L2; test before adopting.
- Sign-language overlay is a future Accessibility Profile, not a v2 build item (YAGNI until requested).

---

## 5. Formats and how each adapts by level

Each format is a FormatSpec: an ordered atom template plus duration, interaction and gate rules, and per-level overrides. Formats assemble atoms; they never author truth themselves. Truth lives in atoms that have passed the family gate.

| Format | Purpose and structure | Level adaptation |
|---|---|---|
| **Detailed** | Full lesson: gap hook (02 §I1) → misconception surfacing → explanation ladder → worked → faded examples → checks → retrieval ending (02 §I5). Path A (CE-L2). | L1–L2: become activity-led episodes, not lectures. L4–L5: the current 10-min chaptered lesson. L6–L7: may declare 16:9 Lecture variant per format (CE-L7). |
| **Simplified** | The same atoms, a lower entry point, the same truth (03 §3.1 "simplify the entry point, not the truth"). Path B. | Never a different level's content. It is the same level with more scaffolding, and it must pass the same fixtures. |
| **Recap** | Retrieval-first summary from Detailed atoms (derivable). Path B. | L1–L2: a song or sequence recap. L5+: formula or claim sheet with a spaced-retrieval prompt (02 §I4). |
| **Question Analysis** | Question → what is it asking → common wrong paths (misconception atoms) → solution → transferable rule. Past-paper questions cite paper and year. | Not defined for L1. L2: "let's try together". L5 + Exam Overlay: marking-scheme aware. |
| **Shorts / Reels** | 20–60 s, one idea, one check (existing 07 §05 procedure). Path B. | AC0: no calls to action, no trend audio, no links. AC1/AC2: existing rules. |
| **Fundamentals Fix (prerequisite repair)** | Repairs a weak prerequisite (03 §3.2 repair route), linked through Competency Graph prerequisite edges. | Any level, drawing atoms from a lower level but with the persona and register of the learner's own level. |
| **Misconception Buster** | Elicit the prediction → show the evidence → resolve. Never leaves the wrong statement standing (02 §I3) [N73]–[N76]. | L3+: full form. L1–L2: gentle "surprise" form, reviewed by the child-development reviewer. |
| **Worked-Example Walkthrough** | One problem, every step narrated, then a faded twin (02 §C3). | L4–L7 |
| **Activity / Lab Demo** | Play-way, hands-on, with a safety cue [N9], [N37]. | L1–L3 core. L4+: virtual lab with the fixture model (04). |
| **Story / Song Concept** | Narrative or song carrying one concept, multimodal [N10]. Path A only. | L1–L2 only |
| **Read-Along / Vocabulary** | Language subjects: text, phonics and meaning, with the pronunciation lexicon (05). | L1–L5 language families, any locale |
| **Derivation / Proof Deep-Dive** | Step-justified derivation, drawn style [N5]. | L5–L7 |
| **Lecture Segment (16:9)** | Talking-head plus board, chaptered [N4], [N31]. | L6–L7 only; aspect is declared in the FormatSpec |
| **Paper / Research Explainer** | Claim → method → evidence → limits, with on-screen citations. | L7 |
| **Case Study** | Commerce, law, humanities: scenario → analysis → principle, with an as-of date. | L5–L7 |
| **Exam Strategy / PYQ Sprint** | Exam Overlay only: pattern, time plan, worked past-paper questions. | L5–L6 + overlay |
| **Formula / Fact Card** | A 10–20 s still or animated card for revision. Unsourced facts are not allowed [N14]. | L3–L7 |
| **Retrieval Drill** | A spaced question set with no new teaching. | L2–L7 |

[Recommendation] Formats are added only when a FormatSpec, its compatibility row and one pilot exist. The resolver refuses unknown combinations, so a "Shorts for Class 1" request either matches an AC0 Shorts spec or fails loudly.

---

## 6. Validating subject families beyond STEM (CE-L8)

Recurring content-box taxonomies (Fascinating Facts, Dive Deeper and similar [N38]) map naturally to atom types.

| Family | Validation mode | Reviewer | Extra checks |
|---|---|---|---|
| Physics / Chemistry / Maths / Biology | 04 validated fixtures (four models today, extended per topic) | subject-qualified | units, sig-figs (02 §E5) |
| Computer Science | **Executable fixtures**: code runs in the render container, and the output on screen must equal the captured output | CS-qualified | language version pinned |
| Social Science / History / Civics / Geography | Claim ledger | qualified historian / social scientist | political and religious sensitivity; official map boundaries (legal check, not yet in register) |
| Languages and Literature | Claim ledger for facts; text licensing record; native-speaker review | native-speaker teacher | copyright of extracts; pronunciation lexicon (05) |
| Commerce / Economics / Accountancy | Numeric fixtures + claim ledger with **as-of date** | CA/economist | law and tax rules are date-stamped, and expiry triggers re-QA |
| Arts / Music / PE / Well-being | Claim ledger + activity-safety review | qualified PE/art teacher | physical-safety cues, especially AC0 |
| Health / sensitive biology | Claim ledger + sensitivity review | medical/health educator | age-appropriateness per Level |
| Law / Medicine (UG/PG) | Claim ledger, jurisdiction + as-of date | licensed professional | "not advice" disclosure |

**Claim ledger rules**, adapted from verifiability practice:

- The claim owner carries the burden of proof [N13].
- Truth alone is insufficient; a reliable published source is required [N15].
- Unsourced claims are removed by default [N14].
- Exceptional claims need multiple high-quality sources [N17].
- Wikipedia is never a citable source [N19].
- Sources are not rejected for being costly to access [N16].
- Board or NCERT textbooks are primary sources for school levels.
- Each ledger entry carries: claim, source, locator, reviewer, as-of date and the hash of the atom. This mirrors Britannica's fact-verification and visible-revision practice [N59], [N60], [N62].

[Recommendation] Run an automated "needs-citation" flagger as a pre-filter [N43] before the reviewer, never instead of one: manual and automated checking both leave gaps ([N40], [N45], contested).

---

## 7. Languages and locales

- **Locale Profiles** carry: script, font stack (vendored Noto in the render container), numerals, caption line rules, the pronunciation lexicon (05), the code-mix policy, the `tts_eligible` flag and the readability method.
- [Hypothesis] **Readability.** English formula-based readability does not transfer to Hindi, Assamese or other Indic languages. Use **controlled vocabulary lists per level × locale** plus native-speaker review as the level-fit method, and do not port English formulas.
- **Code-mixing.** Hinglish is audience-led (03 §5.5). L1–L2 default to a single language per lesson. [Recommendation] Avoid mixing at the pre-reader stage until the child-development reviewer approves a pattern.
- **Voice.** CE-L5 applies: en-IN, Hinglish and hi-IN at launch. Assamese and others use a human voice until a TTS passes the native-speaker gate. AC0 is Path A in every locale anyway.
- **Translation.** Claims are translated at the atom level and *re-validated*: a translated atom gets a new hash and needs native-speaker review of terminology. Board-medium technical terms are kept per the Locale Profile glossary.
- **Curriculum.** The Competency Graph holds multiple board frameworks with crosswalk associations [N50]. One atom can serve Assam Board and CBSE outcomes without duplication.

---

## 8. Reuse of sections 01–14: as-is, extended or retired

| Sec | Decision | Detail |
|---|---|---|
| 01 Business | **Outside the pipeline** | Entitlement, pricing and free-chapter policy live here only (CE-L1). RD-44 is retired from pipeline scope (RD-49). |
| 02 Learning psychology + tokens | **Extended** | Becomes the L4/L5 Level Profile baseline verbatim. Tokens become per-level token sets; the §K checklist becomes validator rules. |
| 03 Super Teacher | **Extended** | Becomes the persona family root. The 10-min structure becomes FormatSpec Detailed@L4/L5. The interaction loop "redesigned for teenagers" stays L4/L5 only; L1–L3 loops are re-derived with reviewers. |
| 04 Video engine v2 | **Extended** | Contracts gain EPP fields; ShortSpec is folded into FormatSpec. Fixtures, renderer and the 56 tests stay. |
| 05 Narration | **As-is + inputs** | Pacing and pause bands come from the EPP. Lexicon per Locale. The 58 tests stay. |
| 06 Skills library | **Extended** | New skills: level-linter, safety-linter, flash-analyser, claim-ledger, profile-resolver, persona-linter, impact-analyser. Ownership map updated. |
| 07 Runbook | **Extended** | New gate roles (child-development, safety, family reviewer); RD-49–51 recorded; the vertical-only rule is replaced by the aspect field per FormatSpec (CE-L7). |
| 08 Cost workbooks | **Extended** | Reviewer cost lines per level and family; Path A share per level. No price or revenue lines inside pipeline ledgers. |
| 09 Evidence | **Extended** | Add N1–N76 plus the legal sources listed in §4.1; tag each Level Profile field to evidence. |
| 10 Pilots | **As-is** | Becomes the regression golden set; new pilots for L2, L3, L6. |
| 11 Human feel | **As-is** | Path A becomes the AC0 default. A child-appropriate sonic logo variant is a style entry. |
| 12 Animation | **Extended** | Style guides mapped to levels: doodle-handdrawn and paper-collage to L1–L3 candidates; editorial-vox and kinetic-type to L4+. New 16:9 lecture style. AC0 motion policy layered on top. |
| 13 Strong-to-cheap | **Extended** | The Kit takes the EPP as input. Judges receive level, persona and safety rubrics. The cascade is unchanged. |
| 14 Audit | **As-is** | Its findings become the regression checklist for the Phase 0 port. |
| **Retired** | | Hard-coded "Class 10–12 STEM", single-persona assumption, vertical-only absolute rule, RD-44, any free/paid hooks. |

---

## 9. Build order with gates

**Phase 0: registry and zero-change port.**
- Build the registry schemas, resolver, EPP hashing and approval binding.
- Encode current behaviour as `level/L4`, `level/L5`, `format/detailed`, `format/short`, `persona/super-teacher`, `family/stem`, plus locales en-IN, Hinglish and hi-IN.
- **Gate G0:** existing 04 and 05 test suites pass, and the section 10 pilots re-render with identical output hashes in the pinned container.

**Phase 1: validators in report-only mode.**
- Run the level, density, cadence, flash, safety, accessibility and persona linters on existing pilots.
- **Gate G1:** the academic team reviews every finding. Rules with false positives get fixed before they become blocking.

**Phase 2: format breadth at the known level.**
- Simplified, Recap, Question Analysis, Worked-Example and Misconception Buster for L4/L5 STEM, all built from shared atoms.
- **Gate G2:** each format passes the same fixtures, plus one learner check reusing the 02 A/B method.

**Phase 3: Middle Stage plus the first non-STEM family.**
- L3 STEM and L3 Social Science through the claim ledger, with the Coach persona.
- **Gate G3:** a qualified reviewer signs off; the ledger has zero unsourced claims; a small learner pilot checks the pacing hypotheses.

**Phase 4: Class 1–5 (AC0).**
- Contract a child-development reviewer first.
- Legal review of AC rules and consent (§4.1, §4.2).
- Super Teacher Junior and Path A recordings; Story/Song, Activity and Read-Along formats.
- **Gate G4:** counsel sign-off; zero flash violations; child-development reviewer co-signs H-SB on every artefact; a small guardian-consented user test with **no data collected beyond what consent covers**.

**Phase 5: UG/PG and exams.**
- Lecturer and Seminar personas, the 16:9 Lecture Segment, Paper Explainer and the Exam Overlay.
- **Gate G5:** subject-qualified reviewer per family; as-of dates enforced.

**Phase 6: locale expansion.**
- Assamese with a human voice, controlled vocabulary lists, and the native-speaker TTS gate per CE-L5.
- **Gate G6:** native-speaker sign-off per Locale Profile version.

Each phase runs the Impact Analyser on every registry change, so CE-L10 re-QA is scoped rather than global.

---

## 10. Risks

1. **Child-stage numbers have no evidence base.** The quantitative evidence is adult MOOC data ([N1], [N7]: 1x-speed sessions only), so L1–L3 values could be wrong and then hash-bound into many artefacts. *Mitigation:* every field carries a Hypothesis tag plus an owner; pilots run before freeze; registry versioning makes correction cheap.
2. **Legal scope mismatch.** India's under-18 "child" definition versus store under-13 regimes. *Mitigation:* no data solicitation for AC0 and AC1; counsel gate at G4; the pipeline stays metadata-neutral.
3. **Reviewer bottleneck.** Child-development and family-qualified reviewers are scarce for a small in-house team. *Mitigation:* atoms are reviewed once and reused across formats [N24]; Path A recordings are batched.
4. **Re-QA storms.** A popular registry entry (for example the L4 profile) changes and voids thousands of approvals. *Mitigation:* the Impact Analyser plus semver policy (patch = no approval impact only if the EPP hash is unchanged).
5. **Persona drift and unsafe phrasing from cheap models.** *Mitigation:* deterministic persona and safety linters before the human gates; judges get level rubrics.
6. **Indic readability is not measurable by formula.** *Mitigation:* controlled vocabulary lists plus native review; no ported English metrics.
7. **Over-building.** *Mitigation:* the CASE REST service, sign-language tracks and new formats are built only when demanded; the resolver plus registry is the only new core.
