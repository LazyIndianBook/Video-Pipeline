# Format Registry v1

26 registered formats: 18 with full specifications (F1–F18) and 8 compact entries (F19–F26). Every format is a Format Spec validated by `schemas/format_spec.schema.json` and linted by the spec linter. Two **Series configurations** (Paper Walkthrough and Chapter One-Shot) are instances of `format/series`, not separate formats. **Audio-only** is a render target (R10), not a format. **Print** is a render target too (level-3+, CE-119, 15 Oct 2026); its four print configurations (F-W Worksheet, F-TN Teacher Notes, F-GN Guardian Note and Revision Sheet print) are configurations of existing format specs, not new formats, so the count of 26 and the Level Profiles §6 matrix are unchanged (see "Print format configurations" at the end).

## Rules common to every format

- **Gates (schema-enforced).** GA-Δ, H-SB, A-suite, DISCLOSURE and RELEASE-CHECK, plus GF (long formats) or GS (Shorts and reels). Primary formats also require GA-Graph. Derived formats may not introduce node types. Compositions may only contain approved artefacts.
- **Interaction.** Check answers are always hidden until reveal, and think windows are protected (RD-11). Both are schema constants.
- **Segments.** No segment is longer than 360 s [N3][N28]. Longer formats are chaptered, with `check.interpolated` between chapters when the spec requires it [N30] (contested evidence).
- **Durations** are [Hypothesis] starting bounds unless marked. Pilots tune them through registry versions. They are intersected with the level ceiling (R5).
- **Voice.** Each spec states its default path. R1 overrides to Path A for first-in-series, flagship, real demos, AC0 and locales without a GL-voice-passed TTS.
- **Visual rules.** Style comes from `styles_allowed` filtered by the safety class. Text is externalised to string tables. Colour is never the only differentiator. The reduced-motion variant is always rendered. Talking-head intercuts [N4] and continuous drawn flow [N5] are style features available to any format.
- **QA.** Every format runs Q-SCHEMA, Q-COMM, Q-CLOSURE, family checks, Q-FLASH, Q-SAFE, Q-A11Y, Q-DET, Q-DISC, Q-META and A1–A17. Extra checks are listed per format.
- **Overlays.** R4 intersects `overlays_allowed` with the level's `exam_overlays_allowed`; an overlay never changes safety class or accuracy gate (LP §5). (15 Oct 2026)
- **Families.** R4 also requires the resolved family in `families_allowed`. "All ten" means the nine families of SUBJECT_VALIDATION_PROFILES plus `evs_foundational`. (15 Oct 2026)
- **Truth.** Formats assemble approved nodes. Simplification happens only through SIM nodes and analogy only through ANL nodes permitted at the level (CE-11).

## Registry index

| # | format_id | Kind | Default voice | Aspect | Levels allowed | Families allowed | Overlays allowed |
|---|---|---|---|---|---|---|---|
| F1 | detailed | primary | A | 9:16 | all except educator | all ten | any except jnvst |
| F2 | simplified | derived | B | 9:16 | l3_5, l6_8, l9_10, l11_12, ug, adult_prof, voc | all ten | any except jnvst |
| F3 | recap | derived | B | 9:16 | all except educator | all ten | any except jnvst |
| F4 | question_analysis | primary | B | 9:16 | l3_5 to pg, adult_prof, voc | all ten | any (jnvst resolves only at l3_5) |
| F5 | short | derived | B | 9:16 | all | all ten | any except jnvst |
| F6 | worked_example | primary | B | 9:16 | l3_5 (simple), l6_8 to pg, adult_prof, voc | all ten | any except jnvst |
| F7 | misconception_fix | derived | B | 9:16 | all except educator (gentle form l1_2, l3_5; full form l6_8+) | all ten | any except jnvst |
| F8 | concept_intro | derived | B | 9:16 | all except educator | all ten | any except jnvst |
| F9 | exam_strategy | primary | B | 9:16 | l6_8 (junior overlays), l9_10, l11_12, ug, adult_prof; overlay required | all except arts_skills, vocational, evs_foundational | any except jnvst (overlay required) |
| F10 | revision_sheet | derived | B | 9:16 | l6_8 to pg, adult_prof, voc | all ten | any except jnvst |
| F11 | flashcard_reel | derived | B | 9:16 | all except educator | all ten | any except jnvst |
| F12 | lab_demo | primary | B (A when real) | 9:16 | all except educator | stem_fixture, humanities_citation (geography practicals), arts_skills, vocational, health_medicine, evs_foundational | any except jnvst |
| F13 | comparison | derived | B | 9:16 | l6_8 to pg, adult_prof, voc | all ten | any except jnvst |
| F14 | story_history | primary | B (A for AC0) | 9:16 | all except educator | all ten | any except jnvst |
| F15 | qa_doubt | primary | B | 9:16 | l6_8 to pg, adult_prof, voc | all ten | any except jnvst |
| F16 | series | composition | inherits | members' | all | all ten | the overlay its members carry, never jnvst |
| F17 | practice_set | derived | B | 9:16 | l3_5 to pg, adult_prof, voc | all ten | any (jnvst resolves only at l3_5) |
| F18 | prerequisite_repair | derived | B | 9:16 | l3_5 to pg, adult_prof, voc | all ten | any except jnvst |
| F19 | derivation_proof | primary | A | 9:16 | l11_12, ug, pg | stem_fixture, quant_social | any except jnvst |
| F20 | lecture_segment | primary | A | 16:9 | ug, pg, adult_prof | all ten | any except jnvst |
| F21 | source_analysis | primary | B | 9:16 | l6_8 to pg, adult_prof | humanities_citation, languages_literature, quant_social, law | any except jnvst |
| F22 | perspectives | derived | B | 9:16 | l9_10, l11_12, ug, pg, adult_prof | humanities_citation, languages_literature, quant_social, law, health_medicine, stem_fixture (history-of-science claims only) | any except jnvst |
| F23 | read_along | primary | A | 9:16 | l1_2, l3_5, l6_8 | languages_literature | none |
| F24 | concept_map | derived | B | 9:16 | l6_8 to pg, adult_prof, voc | all ten | any except jnvst |
| F25 | viva_prep | derived | B | 9:16 | l11_12, ug, pg | all ten | any except jnvst |
| F26 | teacher_explainer | derived | B | 9:16 | educator | all ten | none |

"All" means l1_2, l3_5, l6_8, l9_10, l11_12, ug, pg, adult_prof, voc and educator. The two right-hand columns were added on 15 Oct 2026 and are copied into each spec; adult_prof was added to F2 and F18 the same day. "l6_8 to pg" means l6_8, l9_10, l11_12, ug and pg.

---

## F1 Detailed (`format/detailed`, primary)

- **Purpose.** The flagship full lesson for an objective set: the 03 Super Teacher lesson, chaptered.
- **Learner outcome.** Can explain the concept, apply it to a worked problem, avoid the named misconceptions and retrieve the key ideas.
- **Length.** 420–720 s overall [Hypothesis, around the existing ~600 s target], in chapters ≤360 s. Median engagement is at most about 6 minutes regardless of length [N2]; engagement is about 50% at 9–12 minutes [N27]. The product stays ~10 minutes as chapters, not a single block [N3].
- **Beats.** Ch1: `hook.realworld` → `misconception.elicit` (top MIS) → `explain.ladder_step` (rungs 1–2) → `check.interpolated`. Ch2: `explain.ladder_step` (remaining rungs) → `explain.analogy` (≤1) → `worked.step` (all steps) → `check.interpolated`. Ch3: `worked.faded_twin` → `check.retrieval` (independent attempt, l6_8 and above: a fresh ASM with interaction type `solve_independently`, `pause-video`, no worked method on screen) → `misconception.confront` (remaining MIS) → `recap.retrieval` → `close.next_step`; the AC0 episode variant is unchanged (independent attempt added 15 Oct 2026).
- **Graph inputs.** All core and extension objectives in scope; every MIS; CON rungs; ANL permitted at the level; ≥1 WRK per objective (levels l6_8 and above) or ≥1 ACT or STY per objective (l1_2, l3_5); ASM for checks; ≥1 fresh ASM per objective for the independent attempt (l6_8 and above; 15 Oct 2026).
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Requirements are level-conditional (`node_requirements_by_level`), so an AC0 Detailed compiles from activities and stories without worked items. Extension objectives are included at l11_12 and above, and at lower levels only if flagged by the academic lead.
- **Narration.** Path A (CE-L2). Persona from the level.
- **Visual.** Continuous drawn flow [N5]; head-in moments at chapter transitions [N4] where the style allows.
- **Interaction.** Interpolated checks required between chapters; predict prompts with hidden answers; an independent attempt after the faded twin (l6_8 and above; 15 Oct 2026).
- **QA extra.** Chapter boundary check (each chapter stands alone, ends in a check); fixture coverage of every on-screen number.
- **Level variants.** l1_2/l3_5 "episode": activity-led, `activity.*` and `story.beat` slots replace the worked slots; shortest durations set by the child-development reviewer [Hypothesis]. l6_8: inquiry framing. l9_10/l11_12: the current lesson. ug/pg: notation-dense register (the 16:9 form is F20).
- **Example.** Class 10 Ohm's law: three chapters, ~10 minutes, misconception "current is used up" confronted in Ch1 and re-tested in Ch3.

## F2 Simplified (`format/simplified`, derived)

- **Purpose.** The same level, a lower entry point, the same truth (03 §3.1 "simplify the entry point, not the truth").
- **Learner outcome.** Grasps the core idea and can do one worked item; is ready for Detailed.
- **Length.** 180–360 s [Hypothesis]; single segment.
- **Beats.** `hook.realworld` → `explain.ladder_step` (rungs 1–2, simplified) → `explain.analogy` (1) → `worked.step` (one WRK) → `check.retrieval` → `close.next_step` (points to Detailed).
- **Graph inputs.** Core objectives only; SIM nodes with `permitted_levels ∋ level` replace their claims; one ANL; one WRK.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** A claim without a permitted SIM is either stated in full or omitted; the slot filler may never improvise a simplification (CE-11). Every SIM used is listed at GA-Δ with its `what_is_lost`.
- **Narration.** Path B.
- **Visual.** One dominant focus per frame (02 §B2).
- **Interaction.** One retrieval check, answer hidden.
- **QA extra.** SIM coverage report; closure check confirms no unsimplified claim was paraphrased.
- **Level variants.** Not offered at l1_2 (Detailed episodes are already the simplest form). At l3_5 (ac0), `close.next_step` is delayed_practice, never a pointer to Detailed (CE-19; 15 Oct 2026). At ug and adult_prof (from 15 Oct 2026) it serves as a "fundamentals" entry.
- **Example.** Class 9 Newton's second law with "more push, more speed-up" (an approved SIM noting that mass and direction are lost).

## F3 Recap (`format/recap`, derived)

- **Purpose.** Retrieval-first summary after a lesson.
- **Learner outcome.** Recalls the key claim per objective and avoids the top misconception.
- **Length.** 60–180 s [Hypothesis].
- **Beats.** `recap.retrieval` (question first, answer hidden) → `recap.statement` per objective → `misconception.confront` (top MIS by priority, max 1) → `close.next_step`.
- **Graph inputs.** `CLM[key=true]` per objective; `MIS[priority=min]`; VOC for terms.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Only key claims; no new examples; no ANL unless permitted at the level.
- **Narration.** Path B; faster familiar-recap pacing uses the level's `wpm_recap` band (03 §9.3), never a format number.
- **Visual.** Card-style, low motion.
- **Interaction.** Retrieval before reveal.
- **QA extra.** Every objective in scope covered by one key claim; render-target audio_only allowed.
- **Level variants.** l1_2/l3_5: a song or sequence recap (`story.song_chant` with the approved claims; music owned only, commissioned or in-house, never licensed stock; 15 Oct 2026, CE-66). l11_12+: formula or claim sheet with a spaced-retrieval prompt (02 §I4).
- **Example.** 90 s Ohm's-law recap: "What happens to current if resistance doubles?" then the key claim and "current is not used up".

## F4 Question Analysis (`format/question_analysis`, primary)

- **Purpose.** Dissect one exam or practice item: what is asked, the trap, the method and the marking.
- **Learner outcome.** Can solve this item type and avoid its trap.
- **Length.** 60–240 s [Hypothesis].
- **Beats.** `hook.question_reveal` → `check.predict` (answer hidden) → `explain.definition` (what is asked) → `misconception.confront` (≤2) → `worked.step` (all) → `marking.scheme` (only if marks exist with `marks_source`) → `recap.retrieval` (transferable rule).
- **Graph inputs.** Root ASM; its objectives' key claims; MIS linked by `misconception_ids`; the WRK solving it.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any (jnvst resolves only at l3_5).
- **Derivation rules.** A past-paper item (`original: false`) cites board/exam, year and source paper on screen. An original item is labelled "Original practice question" and can never show marks. Marking renders only from the source paper or official key (schema-enforced).
- **Narration.** Path B.
- **Visual.** The question text stays visible during the think window.
- **Interaction.** Predict before solving; protected think window.
- **QA extra.** Answer key verified by the family (fixture or solver for STEM; official scheme for others); exam-tag display check; question-text licence (Q-RIGHTS).
- **Level variants.** l3_5: "let's try together", no marks, no exam framing. l9_10/l11_12 with a board or competitive overlay: marking-scheme aware. Not defined for l1_2.
- **Example.** AHSEC 2024 2-mark item on series resistors, marks from the official key.

## F5 Shorts / Reels (`format/short`, derived)

- **Purpose.** One complete learning unit in 20–60 s (07/05).
- **Learner outcome.** Takes away one idea and answers one check.
- **Length.** 20–60 s [Recommendation, existing 07/05 rule].
- **Beats.** Variant `short.concept`: `hook.surprise` → `recap.statement` (one key claim) → `check.retrieval`. Variant `short.misconception`: `misconception.elicit` → `misconception.confront` → `check.retrieval`. Variant `short.trap`: `hook.question_reveal` → `worked.step` (the trap step) → `check.retrieval`.
- **Graph inputs.** One complete unit: a key CLM, a MIS plus its confronting claims, or one WRK step with its `common_error_mis_ids`. Variant roots (15 Oct 2026, declared in `format_variants`): short.concept → root claim; short.misconception → root misconception; short.trap → root worked_item. The request names `variant` and `root_node_ids` (Architecture §3.4 R4).
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** The selector demands a complete unit; recompose, never crop (compiler invariant). A contested claim may appear only with its attribution, and a Short may not state one side as fact (CE-29).
- **Narration.** Path B.
- **Visual.** 1080×1920 native layout; caption safe zone from the style.
- **Interaction.** One check, answer hidden.
- **QA extra.** GS full watch; disclosure line; AC0 rules (no calls to action, no trend audio, no links).
- **Level variants.** AC0: no like/subscribe/comment prompts, owned audio only (CE-66). AC1/AC2: existing 07/05 rules.
- **Example.** 35 s: "Does a bulb use up current?" → confront → "Same current in and out: true or false?"

## F6 Worked Example (`format/worked_example`, primary)

- **Purpose.** One problem with every step narrated, then a faded twin (02 §C3).
- **Learner outcome.** Can execute the procedure and complete the faded twin unaided.
- **Length.** 90–300 s [Hypothesis].
- **Beats.** `hook.question_reveal` → `worked.step` (per step, pause per step) → `check.predict` before the final step → `worked.faded_twin` → `recap.retrieval` (the transferable rule).
- **Graph inputs.** One WRK and its `twin_of` twin; claims cited by steps; MIS from `common_error_mis_ids`.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Primary because a twin is often authored for this format, entering through S4 and GA-Graph. Every STEM intermediate value has a `fixture_ref`.
- **Narration.** Path B.
- **Visual.** Khan-style continuous writing [N5]; each step stays on screen.
- **Interaction.** Learner-controlled pause per step; faded twin answer hidden.
- **QA extra.** Q-FIX on every intermediate; units and significant figures (02 §E5).
- **Level variants.** l3_5 "simple": one- or two-step arithmetic with objects, no twin, Path A (AC0). l6_8+: full form. Not defined for l1_2.
- **Example.** Class 12 Kirchhoff loop problem with a faded twin changing one resistor.

## F7 Misconception Fix (`format/misconception_fix`, derived)

- **Purpose.** Replace an intuitive wrong belief with the correct model [N73][N76].
- **Learner outcome.** Predicts correctly on the diagnostic item after the video, where many would not before [N74].
- **Length.** 60–180 s [Hypothesis].
- **Beats (full form, l6_8+).** `misconception.elicit` → `check.predict` (diagnostic item, answer hidden) → `misconception.confront` (evidence) → `explain.ladder_step` (the correct model) → `misconception.retest` (the diagnostic again). **Gentle form (l1_2, l3_5):** `hook.surprise` ("what do you think will happen?") → `activity.observe` or `story.beat` → `explain.ladder_step` (SIM permitted at the level) → `check.retrieval`; no "wrong" framing of the child.
- **Graph inputs.** One MIS with `diagnostic_item` and `confronted_by` claims.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Never leaves the wrong statement standing at the end (02 §I3). The compile fails if the MIS has no diagnostic item.
- **Narration.** Path B (R1 forces A for AC0 and flagship).
- **Visual.** The wrong model is shown visually distinct (shape and label, not colour alone) and is visibly retired.
- **Interaction.** Pre and post item pair recorded for learning evaluation.
- **QA extra.** Closure; "ends on correct model" check; child-development co-sign for the gentle form.
- **Level variants.** As above (CE-42).
- **Example.** "Heavier objects fall faster": predict → drop demo evidence → air resistance model → re-test.

## F8 Concept Intro (`format/concept_intro`, derived)

- **Purpose.** Pre-lesson primer that opens a concept from a real-life situation [N37] (contested evidence).
- **Learner outcome.** Knows what the concept is for and has a first mental model.
- **Length.** 45–120 s [Hypothesis]; single segment.
- **Beats.** `hook.realworld` → `explain.ladder_step` (rungs 1–2) → `explain.analogy` (≤1) → `check.predict` → `close.next_step`.
- **Graph inputs.** CON rungs 1–2, a permitted ANL, one key claim.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** No worked items; no claims beyond rung 2.
- **Narration.** Path B.
- **Visual.** Real-life footage or illustration (MED with rights).
- **Interaction.** One predict prompt.
- **QA extra.** Analogy non-mapping is stated (ANL `non_mapping` surfaced at GA-Δ).
- **Level variants.** l1_2/l3_5: picture-led with say-aloud prompts; close is delayed_practice or calm_end (15 Oct 2026). ug/pg: motivation from a research or industry problem.
- **Example.** "Why does your phone charger get warm?" introducing resistance.

## F9 Exam Strategy (`format/exam_strategy`, primary)

- **Purpose.** Pattern, time plan and tactics for a specific exam, always grounded in official papers.
- **Learner outcome.** Plans time and question order using the published pattern.
- **Length.** 120–360 s [Hypothesis].
- **Beats.** `exam.pattern` (cited, with as-of date) → `exam.time_plan` → `worked.step` on one or two past items → `misconception.confront` (common strategic errors) → `recap.retrieval`.
- **Graph inputs.** `exam_pattern` claims (time-bound, citing the official notification or paper); ASM with exam tags; overlay registry entry.
- **Families and overlays (15 Oct 2026).** families_allowed: all except arts_skills, vocational, evs_foundational; overlays_allowed: any except jnvst (overlay required).
- **Derivation rules.** Overlay required. No predictive claims ("this will come") without stated evidence. Compile fails if any exam_pattern claim's `review_by` has passed (Q-EXPIRY).
- **Narration.** Path B; Exam Strategist register (overlay).
- **Visual.** Pattern tables with as-of date on screen.
- **Interaction.** "Plan your time" prompt.
- **QA extra.** Pattern recompute from the stored paper set (`pattern_recompute`); expiry.
- **Level variants.** Junior overlays (olympiad_junior, nmms) at l6_8 under AC1 rules, with no fear, urgency or peer-comparison language. **Not available at AC0**: a jnvst overlay on l3_5 uses Question Analysis and Practice Set only.
- **Example.** NEET physics section: time per question from the official pattern, two past items.

## F10 Revision Sheet (`format/revision_sheet`, derived)

- **Purpose.** Chapter-level revision of all key claims, formulas and terms.
- **Learner outcome.** Can recall every key claim in a chapter.
- **Length.** 90–300 s [Hypothesis]; chapters ≤360 s.
- **Beats.** For each objective: `card.front` (prompt) → think window → `card.back` (key claim or formula) → every 3–5 cards a `check.retrieval`.
- **Graph inputs.** `CLM[key=true]` across the chapter scope; VOC; formula claims with symbols and units.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** No new examples; display/spoken split for formulas (RD-29).
- **Narration.** Path B.
- **Visual.** Static-heavy cards; consistent layout.
- **Interaction.** Retrieval cadence from the level.
- **QA extra.** Coverage (every objective in the chapter has ≥1 key claim); audio_only allowed only if every formula is fully spoken.
- **Level variants.** l6_8: definitions and relationships; l11_12+: formula sheets.
- **Example.** Class 10 Electricity: 14 cards in two chapters.

## F11 Flashcard Reel (`format/flashcard_reel`, derived)

- **Purpose.** One fact, formula or term as a 10–30 s card for spaced revision.
- **Learner outcome.** Recalls one item.
- **Length.** 10–30 s [Hypothesis].
- **Beats.** `card.front` → think window → `card.back` → `close.next_step`.
- **Graph inputs.** One key CLM, one VOC (with its definition claim) or one formula claim. Unsourced facts are impossible (every CLM has a source [N14]).
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Exactly one node; no analogy.
- **Narration.** Path B.
- **Visual.** Single card, minimal motion.
- **Interaction.** The think window is protected.
- **QA extra.** GS.
- **Level variants.** l1_2/l3_5: picture vocabulary cards (icons and single words), Path A by R1.
- **Example.** "Unit of resistance?" → think → "ohm (Ω)".

## F12 Lab / Demo (`format/lab_demo`, primary)

- **Purpose.** Show an activity or experiment, real or virtual, with safety.
- **Learner outcome.** Knows the procedure, the safety cue and what is observed and why.
- **Length.** 90–360 s [Hypothesis].
- **Beats.** `hook.realworld` → `activity.setup` → `activity.safety_cue` → `activity.do` → `check.predict` → `activity.observe` → `explain.ladder_step` → `check.retrieval`.
- **Graph inputs.** ACT; safety and observation claims; MED footage (real) or the fixture model (virtual).
- **Families and overlays (15 Oct 2026).** families_allowed: stem_fixture, humanities_citation (geography practicals), arts_skills, vocational, health_medicine, evs_foundational; overlays_allowed: any except jnvst.
- **Derivation rules.** `demo_kind = real` in the request (matching the ACT) forces Path A (R1). An ACT that is not household-safe requires safety claims (schema) and is never shown to AC0 as something to try at home.
- **Narration.** Path A for real demos; Path B for virtual labs.
- **Visual.** Real footage or fixture-driven simulation (04 models) for virtual labs.
- **Interaction.** Predict before observe [N37] (contested evidence).
- **QA extra.** Safety-claim review (`safety_claim`); AC0 household-safe check and "with a grown-up" cue.
- **Level variants.** l1_2/l3_5: household-safe materials only; play-way [N9]. l9_10+: virtual lab with fixture model. voc: procedure-completeness validator.
- **Example.** Class 6 "magnets attract iron": paper clips, safety cue, prediction, observation.

## F13 Comparison (`format/comparison`, derived)

- **Purpose.** Contrast two related concepts along named dimensions.
- **Learner outcome.** Distinguishes the pair and does not confuse them.
- **Length.** 60–240 s [Hypothesis].
- **Beats.** `hook.question_reveal` ("what is the difference?") → `compare.dimension` (per shared `contrast_dimension`) → `misconception.confront` (confusion MIS, if any) → `check.retrieval`.
- **Graph inputs.** Claim pairs sharing a `contrast_dimension` value; MIS about the confusion.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** The compile fails if fewer than two dimensions are shared.
- **Narration.** Path B.
- **Visual.** Side-by-side layout. **A consistent colour per concept is allowed, but every concept also carries a shape, label or pattern** (WCAG 1.4.1); the CVD simulation must pass.
- **Interaction.** Classify-this check.
- **QA extra.** Q-A11Y colour rule.
- **Level variants.** l6_8: two dimensions; ug/pg: up to five.
- **Example.** Series vs parallel circuits: current, voltage, total resistance.

## F14 Story / History (`format/story_history`, primary)

- **Purpose.** A narrative carrying approved knowledge: a story or song for young learners; a historical or scientist narrative for older learners.
- **Learner outcome.** Remembers the concept through narrative (L1–5) or understands an event or discovery in sequence with sourced facts (L6+).
- **Length.** 60–300 s [Hypothesis]; chapters ≤360 s.
- **Beats.** L1–5: `story.beat` (per beat) → `story.song_chant` (optional) → `check.retrieval` (say-aloud). L6+: `hook.realworld` → `story.beat` (chronological, each carrying claims) → `source.show` (≥1 primary or secondary source on screen) → `check.retrieval`.
- **Graph inputs.** STY (with beats carrying CLM or SIM); historical_event, date_fact and biographical claims; MED with rights.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Every teaching beat carries an approved claim or simplification. Biographical claims about living people never rest on self-published sources [N18]. No generated faces of real-looking children (`real_child_likeness: false`).
- **Narration.** Path A for AC0 (R1); Path B otherwise.
- **Visual.** ~~Doodle or paper-collage styles for AC0; editorial style for history.~~ storybook-junior (the ac0 child of paper-collage) by default, or doodle-handdrawn, for AC0; paper-collage for stories (default) and editorial-vox for history at l6_8 and above (VISUAL §4.2; corrected 15 Oct 2026: paper-collage is ac1/ac2 only).
- **Interaction.** Call-and-response for AC0 [N10].
- **QA extra.** Music licence (Q-RIGHTS); dates and names consistent across nodes (`date_name_consistency`).
- **Level variants.** l1_2/l3_5 story/song; l6_8+ history and Know-a-Scientist profile [N38] (contested evidence).
- **Example.** Class 2 "Water's journey" song; Class 8 "How the 1857 uprising began" with attributed interpretations.

## F15 Q&A / Doubt (`format/qa_doubt`, primary)

- **Purpose.** Answer one real recurring doubt.
- **Learner outcome.** The doubt is resolved and the learner can apply the answer.
- **Length.** 45–180 s [Hypothesis].
- **Beats.** `qa.doubt_statement` → `qa.answer` (ladder steps) → `misconception.confront` (if the doubt reflects a MIS) → `check.retrieval`.
- **Graph inputs.** The doubt recorded as MIS or ASM (added through S4 and GA-Graph); answering claims.
- **Doubt intake (level-2 interface, level-3+ operation, CE-117, 15 Oct 2026).** Besides the academic team's own list, a recurring doubt can arrive as a `signal_proposal` ledger row raised from an aggregate `learning_signal` record (`schemas/learning_signal.schema.json`; ARCHITECTURE §9.7). The row carries the platform-paraphrased `doubt_cluster_text` for a cell above the minimum cohort size set under O-3 (stricter for ac0 and ac1) and no learner identifiers. A proposal never edits the graph: accepting it opens the S4 + GA-Graph change that records the doubt as MIS or ASM, and only then can an F15 request cite it. Rejected proposals stay in the ledger with a reason.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Doubts are paraphrased by the academic team and never display learner names, handles or submissions (AC1 no-solicitation rule; CE-20).
- **Narration.** Path B.
- **Visual.** Doubt card, then explanation.
- **Interaction.** One check.
- **QA extra.** Safety lint: no personal data, no invitation to submit data (platform handles any submission flow).
- **Level variants.** l6_8 to pg, adult_prof, voc. Not offered to AC0.
- **Example.** "If current is the same everywhere in series, why do bulbs differ in brightness?"

## F16 Series / Course (`format/series`, composition)

- **Purpose.** Assemble approved artefacts into an ordered playlist or a single file with chapters.
- **Learner outcome.** Covers a chapter, unit, paper or course in order.
- **Length.** Sum of members; each member keeps chapters ≤360 s.
- **Beats.** Members in `ordering` (curriculum, difficulty, paper_order or explicit), with `bridge.return_link` and `chapter.title` between members.
- **Graph inputs.** None directly; members' approvals and closures.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: the overlay its members carry, never jnvst.
- **Derivation rules.** `members_must_be_approved: true`; no new claims; series metadata assigns `series_position` to members (first-in-series lessons were Path A under R1).
- **Narration.** Inherits members. Bridges are Path B (A for AC0).
- **Visual.** Members' styles; bridges from the series style.
- **Interaction.** Members' checks.
- **QA extra.** Member closures valid; GF of bridges and the assembled single file.
- **Aspect and length (15 Oct 2026).** The Series spec declares no `duration_s`, `aspect` or `resolution` (schema); they come from the approved members. All members share one aspect (mixed aspects are a compile error) and the duration is the sum of member durations (Architecture §3.4 R4, R5).
- **Configurations.** **Paper Walkthrough**: Question Analysis members in `paper_order` for one past paper, with the paper's licence. **Chapter One-Shot**: `single_file: true`; Detailed chapters + Recap + Practice Set, rendered as one file with chapter markers. This covers the Indian "one-shot" marathon while keeping chapters under 6 minutes [N2][N3].
- **Member rules (15 Oct 2026).** Every member's EPP has the series' level and locale. Chapter One-Shot is offered where F1 and F3 are allowed; it includes F17 only where F17 is allowed (so at l1_2 it is Detailed + Recap) and is not offered at educator. Paper Walkthrough is offered only where F4 is Y (not G), so never at safety/ac0. A compile error names the missing member format.
- **Example.** "Class 10 Electricity complete": 6 Detailed lessons, 6 Recaps, 1 Practice Set.

## F17 Practice Set (`format/practice_set`, derived)

- **Purpose.** Several items with no new teaching: question, response window, solution.
- **Learner outcome.** Fluency through retrieval and application.
- **Length.** 120–360 s per chapter [Hypothesis]; chapters ≤360 s.
- **Beats.** For each item: `hook.question_reveal` → response window (`solve_independently`: pause-video, never a bare think window; INTERACTION §2–3, NI-07) → `worked.step` (brief) → `check.retrieval` (next). (Corrected 15 Oct 2026; was ~~think window~~.)
- **Graph inputs.** ASM by objective, ordered by difficulty; WRK solutions.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any (jnvst resolves only at l3_5).
- **Derivation rules.** Original items are labelled; past items cite source (schema).
- **Narration.** Path B.
- **Visual.** The question stays visible during the response window (the media holds the prompt; the learner pauses).
- **Interaction.** Answer hidden (RD-11), interaction-heavy.
- **QA extra.** Answer keys verified per family.
- **Level variants.** l3_5: 3–5 items, play framing, Path A (AC0); junior overlay jnvst allowed here. Competitive overlays: exam-pattern ordering.
- **Example.** Five Ohm's-law numericals, increasing difficulty.

## F18 Prerequisite Repair (`format/prerequisite_repair`, derived)

- **Purpose.** Repair a weak prerequisite just before a lesson (03 §3.2 repair route).
- **Learner outcome.** Has the missing prerequisite needed for the target lesson.
- **Length.** 60–180 s [Hypothesis].
- **Beats.** `check.predict` (diagnostic) → `explain.ladder_step` (minimal) → `worked.step` (one, optional) → `bridge.return_link`.
- **Graph inputs.** Objectives reached by `requires` edges whose framework level is lower than the request; their key claims and SIMs.
- **Families and overlays (15 Oct 2026).** families_allowed: all ten; overlays_allowed: any except jnvst.
- **Derivation rules.** Nodes come from the lower level, but persona and register come from the learner's own level (R11). Compile fails if the prerequisite objective has no approved nodes.
- **Narration.** Path B.
- **Visual.** Matches the target lesson's style.
- **Interaction.** Diagnostic first.
- **QA extra.** Register check against the learner's level.
- **Level variants.** l3_5 to pg, adult_prof (15 Oct 2026), voc. At l3_5 (AC0) the close is delayed_practice, never a pointer (the script_spec ac0 rule rejects `next_artefact_pointer`; 15 Oct 2026).
- **Example.** Before Class 11 vectors: Class 9 "speed vs velocity" repair.

---

## Compact entries

**F19 Derivation / Proof (`format/derivation_proof`, primary, Path A, 9:16; l11_12, ug, pg).** A step-justified derivation of a claim chain via `requires` edges. Beats: `hook.question_reveal` → `explain.derivation_step` per step with an assumption callout → `check.predict` before the final step → `recap.statement`. Every step is a fixture or cited claim. Length 180–360 s per chapter [Hypothesis]. QA: Q-FIX on each step; notation conventions per locale. Example: deriving the lens formula. Families: stem_fixture, quant_social; overlays: any except jnvst (15 Oct 2026).

**F20 Lecture Segment (`format/lecture_segment`, primary, Path A, 16:9 at 1920×1080; ug, pg, adult_prof).** Slides or board interleaved with an instructor head [N4], chaptered ≤360 s even inside long lectures [N31]. Beats: `chapter.title` → `explain.*` → `check.interpolated` per chapter. Requires the 16:9 safe-zone token set (O-19) before first approval. Example: UG thermodynamics, second law, three chapters. Families: all ten; overlays: any except jnvst (15 Oct 2026).

**F21 Source Analysis (`format/source_analysis`, primary, Path B; l6_8 to pg, adult_prof).** For humanities, commerce and law cases: `source.show` → `source.read` → `source.interpret` (interpretation claims attributed) → `check.retrieval`. TXT/MED with rights; quotations from licensed or public-domain editions only. Case-study variant: situation → analysis → principle, with as-of date and jurisdiction for law. Example: reading a clause of the Constitution with its official text. Families: humanities_citation, languages_literature, quant_social, law; overlays: any except jnvst (15 Oct 2026).

**F22 Perspectives (`format/perspectives`, derived, Path B; l9_10, l11_12, ug, pg, adult_prof).** For contested claims: each position stated with attribution and source (`perspective.position`), no verdict unless the board prescribes one, and then labelled "the syllabus states". Requires two qualified reviewers (family contested policy). Required by `humanities_citation` for any contested topic taught at these levels. Example: historians' readings of a historical event's causes. Families: humanities_citation, languages_literature, quant_social, law, health_medicine, stem_fixture (history-of-science claims only); overlays: any except jnvst (15 Oct 2026).

**F23 Read-Along (`format/read_along`, primary, Path A; l1_2, l3_5, l6_8).** Language subjects: TXT on screen with synchronised highlighting, VOC meanings and phonics, pronunciation lexicon (05). Beats: `source.read` → `explain.definition` (VOC) → `check.retrieval` (say-aloud). Native-speaker editor in GA-Δ; text licence; Path A for Indic languages until TTS passes GL-voice. Example: a Class 3 Assamese poem with word meanings. Families: languages_literature; overlays: none (15 Oct 2026).

**F24 Concept Map (`format/concept_map`, derived, Path B; l6_8 to pg, adult_prof, voc).** Builds a map of objectives and claims (`map.node`, `map.link` from `requires` and `supports` edges) then a retrieval check. Every link is an approved edge; nothing is inferred. Labels and shapes, not colour alone. Example: Class 10 Electricity map. Families: all ten; overlays: any except jnvst (15 Oct 2026).

**F25 Viva Prep (`format/viva_prep`, derived, Path B; l11_12, ug, pg).** Oral-exam practice from ASM items with `item_kind: oral`: `viva.prompt` → response window (`viva_prompt`: think, then pause-video; INTERACTION §2; corrected 15 Oct 2026) → `viva.model_answer` → `misconception.confront`. Board practical viva at l11_12; UG/PG oral exams. audio_only allowed. Example: ten physics practical viva questions. Families: all ten; overlays: any except jnvst (15 Oct 2026).

**F26 Teacher Explainer (`format/teacher_explainer`, derived, Path B; educator).** For teachers: how to teach an objective using the approved graph (`teach.move` for misconceptions to anticipate [N73], analogies with their non-mappings, diagnostic items). AC2. Colleague persona. No new claims. Graph inputs (15 Oct 2026): objectives at the request's `taught_level`; SIM and ANL filtered by `permitted_levels ∋ taught_level`. Persona, register and safety class come from level/educator (R2, R11). Example: "Teaching current without the 'used up' misconception". Families: all ten; overlays: none (15 Oct 2026).

---

## Render targets and outputs

- **video** (default): MP4 at the EPP resolution, captions (WebVTT from the approved script), transcript, reduced-motion variant, audio-description track when required, sidecar metadata.
- **audio_only** (formats F3, F9, F10, F15, F23, F25 and F14 for AC0 stories): M4A at −16 LUFS plus transcript; allowed only when every visual-essential scene is narrated (R10).
- **print** (level-3+, CE-119, 15 Oct 2026; `content_request` `render_target` enum adds `print`): a tagged, accessible PDF (PDF/UA) plus an HTML file, both rendered from the same Format Plan through the pinned Chrome print path (the `harness/` Chrome build, O-16; fonts from the vendored bundle; document metadata fixed, no wall-clock timestamps), so `artefact_sha256` is stable and Q-DET applies as it does to video. Allowed only for the print configurations below, and only when every `visual_essential` element has a text alternative in the tag tree (the print counterpart of R10). Packaging profile `packaging/print-pdf` (R14 matches it on render target); its file-size limit for low-bandwidth use is a value to verify, not yet set. No narration, so no voice path is resolved and no audio checks run.

## Print format configurations (level-3+, CE-119, 15 Oct 2026)

Each configuration is a print instance of an existing format spec, in the way Paper Walkthrough and Chapter One-Shot are instances of `format/series`. It inherits that spec's `levels_allowed`, `families_allowed` and `overlays_allowed`, its derivation rules (no new claims, no new node types) and its closure. Common to all four [Recommendation]:

- **Gates.** The common gates apply. GA-Δ reviews the text; GF reviews the rendered PDF (and its HTML twin) page by page; DISCLOSURE and RELEASE-CHECK as for every artefact.
- **QA.** The common checks wherever they have input, plus Q-A11Y print checks: tag tree present and complete, reading order matches the Format Plan order, headings nested, every figure tagged with alt text or marked artefact, table headers tagged, document language set per locale, contrast and "colour never the only differentiator" on the rendered pages.
- **Packaging.** `packaging/print-pdf`.
- **Interaction.** Answers never sit on the same page as their questions; a key is a separate file or a separate final section, as stated per configuration (the print form of "hidden until reveal").

**F-W Worksheet (print configuration of `format/practice_set`).** Purpose: practice on paper for a classroom or a low-bandwidth learner. Graph inputs: OBJ in scope; ASM grouped by objective (same selection rules as F17, including `stem_form` and rights rules); MIS-tagged distractors where the item has them. Output: the worksheet PDF/HTML and the answer key as a separate file (ASM keys, worked marks only where Q-RIGHTS permits). Levels: as F17 (gentle form at l3_5). Example: Class 10 Electricity, 12 items across 4 objectives.

**F-TN Teacher Notes (print configuration of `format/teacher_explainer`).** Purpose: a lesson plan a teacher can hold in class. Graph inputs: OBJ at the request's `taught_level`; MIS to anticipate [N73] with their confront moves; ANL with `mapping` and `non_mapping`, and SIM, filtered by `permitted_levels ∋ taught_level` (as F26); diagnostic ASM with keys; suggested timings per phase [Hypothesis]. Level: educator (AC2, Colleague register). Example: "Teaching current without the 'used up' misconception", two pages.

**F-GN Guardian Note (AC0; print configuration of `format/recap`).** Purpose: tell the grown-up at home what the child learned and offer one safe thing to do together. Graph inputs: OBJ in scope stated as child-level outcomes; `CLM[key=true]` for "what we learned"; exactly one ACT with `household_safe: true` and its `grown_up_cue`. Rules (blocking via Q-SAFE): no data requests of any kind, no links or QR codes, no calls to action, no house name or visual logo (LP §2 AC0 row), no urgency or comparison, the AC0 disclosure wording. Levels: l1_2, l3_5. The child-development reviewer co-signs GA-Δ and GF as for every AC0 artefact. Example: Class 2 "Plants need water", one page with a watering activity.

**Revision Sheet print (print configuration of `format/revision_sheet`).** Graph inputs: as F10 (`CLM[key=true]`, VOC, formula claims with symbols and units, display form per RD-29). Layout: prompts in one column with the key claims in a separate section or on the reverse, so the page still works as retrieval practice. Levels: as F10. Example: Class 10 Electricity, two pages.
