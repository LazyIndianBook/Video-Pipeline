# Level Profiles v1

Ten Level Profiles plus exam overlays. Each profile is a registry entry validated by `schemas/level_profile.schema.json`. Numeric fields are **tagged values**: Recommendation, Evidence, Inherited (from 02/03) or Hypothesis. A Hypothesis requires an owner and a pilot reference, and a null value ("calibrate in pilot") must be tagged Hypothesis (schema-enforced). No number in this document is invented: where the evidence register has none, the value is "calibrate".

## 1. Why these bands

Indian boards write outcomes by NCF-SE stages, so the bands follow them where the evidence gives spans: Preparatory = Grades 3–5 [N8]; Middle = Grades 6–8 [N32]. Classes 1–2 belong to the Foundational stage, which is not yet in the evidence register (O-10). CE-L9 groups Classes 1–5 for safety; pedagogically they split into l1_2 and l3_5. Band boundaries for other boards come from that board's framework in the Curriculum Graph, never from this table.

The engagement evidence ([N1], [N2], [N26]–[N31]) is adult MOOC data measured by proxies. It sets an adult ceiling (segments under 6 minutes [N3][N28]); it is not a child target. The speaking-rate evidence ([N6], [N29]) is contested and must never be used to speed up l1_2 to l6_8.

## 2. Audience safety classes

| Class | Applies to | Content rules (blocking via Q-SAFE) |
|---|---|---|
| **safety/ac0** child-directed | l1_2, l3_5 | No data solicitation of any kind (names, schools, photos, comments, voice). No external links or QR codes. ~~No brand names, logos or product placement.~~ No third-party brand names, logos or product placement. House identity at AC0 is audio only: the house sonic logo `music/logo-junior`, at most once at the open and once at the close, never under narration and never paired with a call to action. No house name or visual logo on screen, in copy or on covers (corrected 15 Oct 2026: the struck rule forbade the house sonic logo that MUSIC §3 and §4 place in every AC0 artefact). No calls to like, subscribe, comment or share. No urgency, fear, peer comparison or streak pressure (02 §H5). No generated faces of real-looking children. Physical activities only with household-safe materials and a "with a grown-up" cue. Age-appropriate disclosure wording. Zero-flash policy (§4). Path A only. Child-development reviewer co-signs GA-Δ, H-SB and GF. Child talent: default none; any child voice or image requires a guardian release on the MED node. Sensitive-topic review (health, body, mental health, safety, caste, religion, family structure, food), co-signed by the child-development reviewer (15 Oct 2026). Print (level-3+, CE-119, 15 Oct 2026): the Guardian Note (F-GN) is the AC0 print configuration for the grown-up at home: what the child learned, one `household_safe` ACT with its grown-up cue, no data requests, no links or QR codes, no house name or visual logo; a Worksheet (F-W) at l3_5 takes the gentle F17 form (FORMAT_REGISTRY, Print format configurations). |
| **safety/ac1** minor-inclusive | l6_8, l9_10, l11_12, ug (all years), voc | No data solicitation (under-18 learners are children under India's data law; O-3). External links only to official board or government sources. Sensitive-topic review (health, mental health, safety, caste, religion). WCAG 2.3.1 flash floor. No fear or pressure language in exam content. |
| **safety/ac2** adult | pg, adult_prof, educator | Standard rules, WCAG 2.3.1 floor, family sensitivity review, professional disclaimers where the family requires them. |

The pipeline sets `audience_class` as neutral metadata. The platform maps it to store flags such as made-for-kids, and to data and ad rules (CE-L1, CE-L9). **level/ug always applies AC1 rules**: first-year cohorts include under-18s, and a deterministic resolver cannot know a viewer's age (CE-18).

## 3. Profiles

Notation: **Inh** = inherited from 02/03 values in the repository (the profile file copies the exact number and cites the section); **Cal** = calibrate in pilot, [Hypothesis], owner named.

**Cal values at compile time (15 Oct 2026, Architecture §3.4 R5).** A null `attention.max_segment_s` is a compile error until the value owner publishes a pilot version of the profile through GR with a provisional value tagged Hypothesis (owner, pilot_ref); provisional values must satisfy l1_2 ≤ l3_5 ≤ l6_8. A null pacing band compiles only as `teacher_set` on Path A. Null sentence-length, new-term and new-idea values never block compilation (Q-LEVEL report-only). `attention.max_artefact_s` is optional; when it is omitted the level sets no artefact ceiling and R5 uses the format duration.

### 3.1 level/l1_2 (Classes 1–2, Foundational)

- **Safety:** ac0. **Persona:** Super Teacher Junior. **Voice floor:** A.
- **Pacing:** Cal (owner: child-development reviewer). The Path A teacher sets a natural pace; no WPM target is imported from adult data.
- **Segment:** Cal; shortest of all levels. **New ideas per segment:** Cal (expected 1).
- **Reading level and vocabulary:** pre-reader. Narration carries all meaning; on-screen text is icons and single words (`icons_and_single_words`). Controlled vocabulary list per locale (O-17). One language per lesson by default; code-mixing only after the child-development reviewer approves a pattern.
- **Interaction:** say-aloud, point, move, sing [N10]; call-and-response with real pauses. Never asks for personal information.
- **On-screen density:** one idea per frame. Minimum type size: Cal (≥ the 02 token minimum).
- **Assessment orientation:** play and talk; no exam formats.
- **Accessibility:** captions exist for hearing access but are never needed to follow the lesson; reduced-motion variant; audio-described track where visuals carry meaning.
- **Reviewers:** child-development + academic subject.
- **Gate note:** profile freeze needs O-10 (Foundational stage source).

### 3.2 level/l3_5 (Classes 3–5, Preparatory [N8])

- **Safety:** ac0. **Persona:** Super Teacher Junior. **Voice floor:** A.
- **Pedagogy:** play-way, discovery and activity methods continue while textbooks are introduced without overwhelming children [N9]; multimodal: reading, writing, speaking, drawing, singing, playing [N10]; grade-appropriate language in real-life and cultural context [N11] (contested); the textbook is one resource among many [N12].
- **Pacing:** Cal. **Segment:** Cal (≤ l6_8 value). **New ideas per segment:** Cal.
- **Reading level:** early reader; short phrases on screen; controlled vocabulary per locale.
- **Language:** one language per lesson (`single_language_per_lesson: true`) until the child-development reviewer approves a code-mix pattern, as l1_2 (added 15 Oct 2026; enforced by R4).
- **Interaction:** draw, act, predict, sing; "let's try together".
- **Density:** one dominant focus (02 §B2).
- **Assessment orientation:** play and talk, gentle recall.
- **Formats:** as §6 column l3_5 (the single source); notes: gentle Misconception Fix; simple Worked Example; Question Analysis without marks; jnvst only through F4 and F17 (corrected 15 Oct 2026; the list here was partial).
- **Reviewers:** child-development + academic subject.

### 3.3 level/l6_8 (Classes 6–8, Middle [N32])

- **Safety:** ac1. **Persona:** Super Teacher Coach (inquiry questions, "what would happen if…", experiment framing; less performative than Junior, more Socratic than the current Super Teacher).
- **Pedagogy:** shift to abstract ideas and unfamiliar contexts with clear goals [N53]; methods of inquiry per discipline, not accumulation of facts [N54]; direct instruction balanced with exploration [N34]; reasoning-focused assessment with formative and summative balance [N55]; content-to-competencies shift [N56]; nine subjects including three languages [N33]; cross-cutting themes [N35]; chapters open from real-life situations with check questions [N37] (contested); optional "Dive Deeper" style extension objectives [N38] (contested).
- **Pacing:** start from the 02 §G2 bands (Inh) as [Hypothesis] for this age; validate by A/B.
- **Segment:** ≤360 s [Recommendation from adult evidence, Hypothesis for this age].
- **Reading level:** sentences; standard notation introduced; glossary per locale.
- **Interaction:** predict-explain-check; reasoning prompts.
- **Density:** 02 §B3 relationship count (Inh) as Hypothesis.
- **Each objective names its discipline's form of understanding** in the graph (an OBJ field in the framework file).
- **Reviewers:** academic subject + family-qualified.

### 3.4 level/l9_10 (Classes 9–10, Secondary)

- **Safety:** ac1. **Persona:** Super Teacher (current 03, unchanged).
- **Pacing:** 130–155 wpm ordinary; 105–125 wpm dense, down to 90–120 for a brand-new relationship; 145–165 wpm recap (Inh: RD-10, 02 §G2, 03 §9.3, 05-VIG §5.1; production hypotheses under the 11 A/B plan). Think window 5–8 s, default 6 s, 4 s only for a binary choice (Inh, RD-11). (Recap band and think window added 15 Oct 2026; the Level Profile owns these numbers, CE-16.)
- **Artefact ceiling:** none; `attention.max_artefact_s` is omitted (Inh: 02/03 set no ceiling beyond chaptering), so R5 uses the format duration and records `level_ceiling: unset` (15 Oct 2026).
- **Segment:** ≤360 s [N3][N28]; the ~10-minute lesson is chaptered [N27].
- **Reading level:** board terminology plus glossary.
- **Interaction:** the 03 interaction loop; self-explanation (02 §C4); protected think windows (RD-11, Inh).
- **Density:** 02 §B3, §E2 (Inh).
- **Assessment orientation:** recall and reasoning; board exam tags enabled.
- **Overlays:** olympiad_senior (board-competitive). (Corrected 15 Oct 2026: nmms is a Class 8 exam and sits on l6_8 only, §5.)
- **Reviewers:** academic subject + family-qualified.

### 3.5 level/l11_12 (Classes 11–12, Higher Secondary)

- **Safety:** ac1. **Persona:** Super Teacher Mentor (exam-aware, deeper derivations, fewer hooks).
- **Pacing:** as l9_10 (Inh), including the recap band and think window. **Segment:** ≤360 s. **Artefact ceiling:** none, as l9_10.
- **Reading level:** discipline register.
- **Interaction:** retrieval, worked → faded examples (02 §C3), derivation checks.
- **Assessment orientation:** exam reasoning.
- **Overlays:** jee, neet, cuet, olympiad_senior.
- **Formats:** as §6 column l11_12 (the single source); notes: Derivation/Proof and Viva Prep (practical viva) start at this level.
- **Reviewers:** academic subject + family-qualified.

### 3.6 level/ug (Undergraduate)

- **Safety:** ac1 (always; CE-18). **Persona:** Lecturer (fewer interjections, explicit notation and definitions, talking-head inserts at transitions [N4], drawn derivations [N5]).
- **Pacing:** 02 bands (Inh) as defaults; faster bands only as [Hypothesis] under A/B ([N6][N29] contested).
- **Segment:** ≤360 s, even inside long lectures [N31].
- **Reading level:** disciplinary register plus notation conventions.
- **Interaction:** interpolated questions between segments [N30] (contested).
- **Formats:** as §6 column ug (the single source). **Formats added:** Lecture Segment (16:9). (Corrected 15 Oct 2026: ~~Viva Prep, Perspectives~~ are already available below ug.)
- **Overlays:** upsc, state_psc, ca_cs (AC1 rules). Seed `exam_overlays_allowed: [overlay/upsc, overlay/state_psc, overlay/ca_cs]` (15 Oct 2026).
- **Reviewers:** family-qualified reviewer holding at least a postgraduate degree in the discipline [Recommendation].

### 3.7 level/pg (Postgraduate / Masters)

- **Safety:** ac2. **Persona:** Seminar Lead (cites sources on screen, models critique, states uncertainty explicitly).
- **Pacing:** as ug. **Segment:** ≤360 s; long lectures only as chaptered playlists.
- **Reading level:** research register; citations on screen.
- **Interaction:** pause-and-critique of claims or methods.
- **Accuracy:** exceptional and frontier claims need multiple high-quality sources [N17]; Perspectives common; two specialist reviewers for contested claims.
- **Reviewers:** family-qualified at PG level or above.

### 3.8 level/adult_prof (adult professional and competitive aspirants)

- **Safety:** ac2. **Persona:** Lecturer with Exam Strategist register under overlays.
- **Purpose:** ~~UPSC, state PSC, CA/CS and similar adult exams.~~ UPSC, state PSC and similar adult exams (CA/CS sits on level/ug, §5; corrected 15 Oct 2026). The base register is UG-equivalent; overlays add patterns.
- **Pacing:** as ug (Inh).
- **Overlays:** ~~upsc, state_psc, ca_cs.~~ upsc, state_psc. Seed `exam_overlays_allowed: [overlay/upsc, overlay/state_psc]`.
- **Accuracy:** law and rates are time-bound (`as_of_date`, `review_by`, jurisdiction).
- **Reviewers:** family-qualified + academic lead for exam patterns.

### 3.9 level/voc (vocational: NSQF levels, ITI, polytechnic)

- **Safety:** ac1 (cohorts include minors; max-restrictive). **Persona:** Skills Instructor (procedural, safety-first, demonstration-led).
- **Band:** maps to NSQF levels through a `nsqf_level` field in the framework file (O-11).
- **Pacing:** Cal [Hypothesis]. **Segment:** ≤360 s.
- **Interaction:** do-along, procedure checks; retrieve_definition, classify and reconstruct so F1, F3, F10, F11, F13, F14 and F24 have a legal type (INTERACTION_and_ASSESSMENT_REGISTRY §4, 15 Oct 2026).
- **Formats:** as §6 column voc (the single source); notes: Lab/Demo real demos are Path A by R1 (corrected 15 Oct 2026; the list here was partial).
- **Reviewers:** trade-qualified instructor (practitioner) + safety reviewer for activities.

### 3.10 level/educator (teachers)

- **Safety:** ac2. **Persona:** Colleague.
- **Purpose:** Teacher Explainer only, plus Shorts and Series of them.
- **Print (level-3+, CE-119, 15 Oct 2026):** Teacher Notes (F-TN, the print configuration of Teacher Explainer: objectives, misconceptions to anticipate, analogies with their non-mappings, timings). Worksheets (F-W) and Revision Sheet print that teachers hand out are rendered at the learner's level, not at educator (FORMAT_REGISTRY, Print format configurations).
- **Reviewers:** academic lead.

### 3.11 Persona ids (note, 15 Oct 2026, CE-64)

The names above are the Architecture §6 persona names. The registry id scheme owned by `subsystems/VOICE_and_PERSONA_REGISTRY.md` §2.2 is five persona ids with variants, `persona/<id>#<variant>` (a pin adds the version: `persona/<id>@x.y.z#<variant>`). A Level Profile `persona:` field takes this form; every name above still resolves.

| Level | Name used above | `persona:` field |
|---|---|---|
| l1_2, l3_5 | Super Teacher Junior | `persona/super-teacher-junior#junior` |
| l6_8 | Super Teacher Coach | `persona/super-teacher-junior#coach` |
| l9_10 | Super Teacher | `persona/super-teacher#core` |
| l11_12 | Super Teacher Mentor | `persona/super-teacher#mentor` |
| ug | Lecturer | `persona/lecturer#lecturer` |
| pg | Seminar Lead | `persona/lecturer#seminar-lead` |
| adult_prof | Lecturer (Exam Strategist under overlays) | `persona/lecturer#lecturer` |
| voc | Skills Instructor | `persona/skills-instructor#instructor` |
| educator | Colleague | `persona/lecturer#colleague` |
| any base level under an overlay except `overlay/jnvst` | Exam Strategist | register overlay `persona/exam-coach#strategist`, never at `safety/ac0` |

### 3.12 Competitive is an overlay, not a level (note, 15 Oct 2026)

There is no `level/competitive`. "Competitive" in the README and in Architecture §1.1 means the exam overlays in §5 (jee, neet, cuet, olympiad_junior, olympiad_senior, nmms, jnvst, upsc, state_psc, ca_cs) sitting on a base level, plus `level/adult_prof` for adult aspirants. An overlay never changes a level's safety class or accuracy gate (§5).

## 4. Motion, flash and accessibility by class

- **AC1/AC2 floor:** WCAG 2.3.1, Three Flashes or Below Threshold (to be registered, O-1), measured by Q-FLASH on the deterministic render.
- **AC0 zero-flash (CE-21), operational definition.** (a) Zero general flashes and zero red flashes under the WCAG definitions, **with the area threshold removed**: any qualifying pair of opposing luminance changes counts, whatever its size. (b) The analyser evaluates every tile of a grid over the 1080×1920 frame. The tile grid and an additional per-tile luminance-change rate limit are parameters the child-development reviewer signs (O-2); until signed, the analyser runs a 10×10 grid in report-only mode [Hypothesis]. (c) AC0 release is gated on **both** O-1 (WCAG source registered) and O-2 (signed parameters). The rule is stricter than the standard, so it needs no new evidence beyond the standard's definitions.
- **Reduced-motion variant:** rendered for every level (schema constant).
- **Accessibility profile `a11y/base`:** captions from the approved script in a protected zone and a transcript; contrast 4.5:1 text and 3:1 essential graphics against the 02 tokens; colour never the only differentiator, with CVD simulation; `visual_essential` flag on SceneSpec (meaning carried only visually must be narrated or described in `ad.vtt` plus an audio-described mix); caption line length per level (`short_lines` for l3_5 and l6_8, Cal). Dyslexia-friendly type for l1_2/l3_5 is a [Hypothesis] to test, not adopted. A sign-language profile is deferred until triggered (O-18). (15 Oct 2026: both are now drafted as profiles below; the O-18 trigger is reworded.)
- **Further accessibility profiles (level-3+, CE-120, 15 Oct 2026).** Registry kind `a11y/` gains four entries as data. A request or the platform selects one in place of `a11y/base`; each one includes every `a11y/base` rule and adds the changes below. **Limits only tighten (R8 (a)):** a profile may make a limit stricter (slower pacing ceiling, longer think-window minimum, larger minimum type or caption scale, higher contrast) and never loosens a level, safety-class or format limit; other scalars follow R8 (b), where the a11y profile ranks just below the safety class. Values are Cal unless stated, owner Academic lead, and the sources are registered under O-24 (RPwD Act 2016; Ministry of Education guidelines on e-content for children with disabilities, 2021; both to verify, SOURCES S-14, S-15).
  - `a11y/low_vision`: larger caption scale; higher-contrast colour tokens; no meaning carried by thin lines or fine detail; in print, a larger minimum type size.
  - `a11y/cognitive`: pacing slower than the level band (tightens the band's maximum); one idea per beat; plain-language SIM nodes only, never a new simplification.
  - `a11y/dyslexia` [Hypothesis, owner Academic lead, pilot ref required]: font, letter-spacing, line-spacing and line-length tokens; not adopted until a pilot confirms it.
  - `a11y/isl`: an Indian Sign Language interpreter inset in a safe-zone token; Path A only; gated on a qualified ISL reviewer in `reviewer/`. O-18's trigger now reads: the first `a11y/isl` request or a pilot with a special-education partner.
  - For every profile, the interaction sidecar carries keyboard and screen-reader labels for every ASM option, and Q-A11Y checks them.

## 5. Exam overlays

An overlay sits on a base level and adds: the official pattern reference and syllabus GUIDs (a competitive framework in the Curriculum Graph, crosswalked to board items [N50]); as-of dates for patterns and marking schemes (time-bound claims); the Exam Strategist register; and question provenance rules (past questions cite paper and year; original questions are labelled). **An overlay never changes the accuracy gate or the safety class.**

| Overlay | Allowed base levels | Notes |
|---|---|---|
| jnvst (Navodaya entry) | l3_5 | AC0: Question Analysis and Practice Set only; no strategy, time pressure or marks framing |
| olympiad_junior | l6_8 | AC1; no fear or comparison language |
| nmms | l6_8 | AC1 |
| olympiad_senior | l9_10, l11_12 | |
| jee, neet, cuet | l11_12 | |
| upsc, state_psc | adult_prof, ug | ug keeps AC1 rules |
| ca_cs | ug | AC1 always: CA Foundation and CSEET candidates sit straight after Class 12, so the cohort includes under-18s (CE-18 reasoning). Moved off adult_prof (AC2) on 15 Oct 2026 |

**Exam windows, change freeze and surge (level-3+, CE-122, 15 Oct 2026).** Overlay entries and board frameworks in the Curriculum Graph carry `exam_windows[]` {name, start, end}: data on existing entries, not a new registry kind. Dates come from the exam body's published notice and are time-bound like any exam_pattern claim. **Freeze rule (GR):** inside any window that touches an entry's affected set, only Revocation, Safety-tightening and S1 incident fixes may release; every other change queues, and the GR impact preview shows its deferral date. **Surge playbook** [Recommendation]: at T-10 weeks, plan and gate Recap, Revision Sheet (video and print), Practice Set and Paper Walkthrough for the in-window competencies, so the window needs no new GA-Graph work; confirm the reviewer rota with backups and the `reviewer/on-call` primary and backup for the whole window; forecast gate-minutes against the rota in the ledger capacity lines.

## 6. Format availability matrix

Y = available; G = gentle or simple variant; — = not defined (the Resolver refuses it).

| Format | l1_2 | l3_5 | l6_8 | l9_10 | l11_12 | ug | pg | adult_prof | voc | educator |
|---|---|---|---|---|---|---|---|---|---|---|
| F1 detailed | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F2 simplified | — | Y | Y | Y | Y | Y | — | Y | Y | — |
| F3 recap | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F4 question_analysis | — | G | Y | Y | Y | Y | Y | Y | Y | — |
| F5 short | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| F6 worked_example | — | G | Y | Y | Y | Y | Y | Y | Y | — |
| F7 misconception_fix | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F8 concept_intro | Y | Y | Y | Y | Y | Y | Y | Y | Y | — |
| F9 exam_strategy | — | — | Y* | Y | Y | Y | — | Y | — | — |
| F10 revision_sheet | — | — | Y | Y | Y | Y | Y | Y | Y | — |
| F11 flashcard_reel | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F12 lab_demo | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F13 comparison | — | — | Y | Y | Y | Y | Y | Y | Y | — |
| F14 story_history | G | G | Y | Y | Y | Y | Y | Y | Y | — |
| F15 qa_doubt | — | — | Y | Y | Y | Y | Y | Y | Y | — |
| F16 series | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y |
| F17 practice_set | — | G | Y | Y | Y | Y | Y | Y | Y | — |
| F18 prerequisite_repair | — | Y | Y | Y | Y | Y | Y | Y | Y | — |
| F19 derivation_proof | — | — | — | — | Y | Y | Y | — | — | — |
| F20 lecture_segment | — | — | — | — | — | Y | Y | Y | — | — |
| F21 source_analysis | — | — | Y | Y | Y | Y | Y | Y | — | — |
| F22 perspectives | — | — | — | Y | Y | Y | Y | Y | — | — |
| F23 read_along | Y | Y | Y | — | — | — | — | — | — | — |
| F24 concept_map | — | — | Y | Y | Y | Y | Y | Y | Y | — |
| F25 viva_prep | — | — | — | — | Y | Y | Y | — | — | — |
| F26 teacher_explainer | — | — | — | — | — | — | — | — | — | Y |

*F9 at l6_8 only with olympiad_junior or nmms overlays.

15 Oct 2026: F2 and F18 opened at adult_prof (UG-equivalent base register; aspirants rebuild school foundations, and F18's R11 rule exists for that case).

The matrix is the union of each format's `levels_allowed` and each level's `formats_allowed`; the spec linter fails if the two disagree.

## 7. Evidence discipline

Every profile carries an `evidence[]` list mapping each field to a tag and source. Level validators (Q-LEVEL) run **report-only** until each level's Hypothesis values are confirmed by its pilot (CE-35). The exceptions block from day one: safety class rules, flash, contrast, captions, the visual-essential rule and the commercial lint. A pilot changes a value by publishing a new profile version through GR, which triggers pedagogical-class re-QA (Architecture §3.6).
