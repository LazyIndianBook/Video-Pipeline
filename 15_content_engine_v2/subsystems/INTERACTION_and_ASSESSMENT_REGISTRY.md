# Interaction and Assessment Registry v1

Status: subsystem specification. Date: 15 Oct 2026. Stages: S5 (bound in the Format Plan), S6 (scripted), S7 (validated), GA-Δ (reviewed), S14 (exported as a sidecar).
Object: one **Interaction Spec** per artefact (`subsystems/schemas/interaction_spec.schema.json`), bound to its Script Spec by hash. Companion: `SCRIPTING_REGISTRY.md`.
Generalises: 03 Step 7 (interaction loop, pause matching, no fake listening, question variety) and Step 9 (feedback, confidence); 02 §C3–§C4, §F1–§F7, §G3, §H1–§H6, §I3–§I5, §J; 05 §7.2 (`pause_after`, `answers_after`); RD-11.

**Citation convention.** [N#] = `15_content_engine_v2/SOURCES_and_claims.md`; [11:N#] = section 11 register. Section references are **Inherited** project rules. **[Recommendation]** = design choice made here; **[Hypothesis]** = value a pilot must confirm (owner named); "Cal" = calibrate, a Hypothesis. No new numbers are introduced.

---

## 1. Purpose and boundary

An interaction is a genuine task: ask something specific → allow an attempt → explain the answer → identify a repair → ask a related question (03 Step 7). A rhetorical question answered at once is not an interaction and never uses a check slot (02 §F1).

Prerecorded video cannot hear, see or score a learner. So the video **prompts, waits, reveals and gives conditional feedback**. The platform, which is outside the pipeline, may capture responses, adapt and schedule (§13). The Interaction Spec carries everything the video does and exports a neutral sidecar the platform can attach behaviour to. It carries no commercial field (CE-L1).

---

## 2. Interaction types

A closed vocabulary used by Level Profiles (`interaction.allowed_types`) and Interaction Specs. Types not named in 02 or 03 are marked.

| `itype` | What it accomplishes | Response modes | Window | Host slots | Answer source | Levels |
|---|---|---|---|---|---|---|
| `predict` | Commit to an expectation before the result (02 §F3) | think | think | `check.predict`, hooks, `explain.ladder_step`, before `activity.observe` | ASM or WRK step | All; AC0 as picture choice |
| `retrieve_definition` | Reconstruct essential meaning, then compare with an answer checklist | think, say_aloud, write | think (oral components) or pause-video (written) | `check.retrieval`, `recap.retrieval`, `card.front` | ASM (components) | l3_5 (say-aloud) up |
| `record_formula` | A compact reference with symbol meanings, units and conditions, not a transcript (02 §F3, §F5) | write | pause-video, narration stopped | after `recap.statement` or `explain.definition` | ASM (reference checklist) | l6_8 up |
| `reconstruct` | Hide it, write it from memory, compare (02 §F5) | write | pause-video | `check.interpolated`, `recap.retrieval` | ASM | l6_8 up |
| `draw` | A labelled sketch as reasoning, with a partial outline where drawing would obscure the science (02 §F6) | draw | pause-video | `check.*`, `recap.retrieval` | ASM (model sketch and checklist) | l3_5 up |
| `complete_missing_step` | Supply one step between demonstration and independence (02 §C3) | solve, write | think for one simple operation; otherwise pause-video | `worked.faded_twin`, `explain.derivation_step` | WRK twin step or ASM | l3_5 (objects) up |
| `solve_independently` | Select and execute the method with the method hidden (02 §C3) | solve, write | pause-video | `check.*`, practice items | ASM | l3_5 ("let's try together") up |
| `explain_error` | Give a reason a clearly labelled wrong claim fails (02 §F3) | think, write, say_aloud | think or pause-video | `misconception.confront`, `check.*` | ASM linked to MIS | l6_8 up; never AC0 |
| `verify` | Check units, direction, magnitude, conditions (02 §F3) | think | think | end of `worked.step`, `check.*` | ASM or WRK step | l3_5 (count again) up |
| `classify` | Place a case in the right category (F13) [Recommendation] | think, point | think | `check.retrieval` in Comparison | ASM | l6_8 up |
| `plan_time` | Plan time and order from the official pattern (F9) [Recommendation] | think, write | pause-video | `exam.time_plan` | ASM + exam_pattern claim | Overlay levels; never AC0 |
| `read_along` | Read a passage aloud with highlighting (F23) | say_aloud | learner follows the text | `source.read` | TXT | l1_2, l3_5, l6_8 |
| `call_response` | Say a word or phrase back [N10] | say_aloud, think | call_response | `story.beat`, `check.retrieval` | ASM or STY beat | l1_2, l3_5 |
| `point_and_say` | Point to a picture and name it [N10] | point, say_aloud | call_response | `check.retrieval`, `card.front` | ASM | l1_2, l3_5 |
| `sing_along` | Sing the approved song [N10] | sing | song tempo; no answer | `story.song_chant` | STY.song_chant | l1_2, l3_5 |
| `move_along` | Act out a movement, with a seated alternative [N10] | move | call_response | `story.beat`, `activity.do` | ACT or STY | l1_2, l3_5 |
| `do_along` | Perform a procedure step with the demonstrator [Recommendation] | move, solve | pause-video | `activity.do` | ACT | voc; Lab/Demo l6_8 up |
| `discussion_prompt` | Open question for reflection or peer discussion | think, critique, write | pause-video; no single answer | `check.interpolated` (ug), `teach.move` (educator) | ASM optional (model points) | ug, pg, educator |
| `viva_prompt` | Answer an oral examination question (F25) | say_aloud | think, then pause-video | `viva.prompt` | ASM[item_kind=oral] | l11_12, ug, pg |
| `critique` | Pause and critique a claim or method (Level Profiles §3.7) | critique | pause-video | `check.interpolated`, `source.interpret` | ASM with criteria, optional | pg; ug optional |

Variety is required, not a quota: alternate predict → identify → explain → reconstruct → draw → solve → verify (03 Step 7). Copying an answer is never retrieval (07/03 S6).

---

## 3. Pause kinds and windows

| Window | Use | Length | Tag and source |
|---|---|---|---|
| `beat` (not an interaction) | Phrase, contrast, inspection | 0.3–0.6 s; 0.8–1.5 s after a key causal statement; 2–4 s to inspect a completed transformation | Inherited, 02 §G3 |
| `think`: brief protected silence | Simple prediction, binary choice, one recently shown relationship, a verify check | 5–8 s, **default 6 s**; 4 s only for a binary choice (`binary_choice: true`) | Inherited, RD-11 |
| `pause-video`: learner-controlled | Writing a definition, drawing, multi-step calculation, copying a compact reference | Learner's own time. The media holds the prompt for a short span (the 02 blueprint uses 10–12 s) | Inherited, 03 Step 7; 02 blueprint |
| `call_response` (AC0) | Say-aloud, point, move | Cal; never shorter than the 6 s think default | [Hypothesis; floor is a Recommendation; owner: child-development reviewer; pilot: first AC0 episode] |

**Hindi and Hinglish.** Word rates and timings are validated per language (02 §G2), and Hindi narration often runs longer [Hypothesis, 11 Step 7]. Windows in `locale/hi-in` and `locale/hinglish` are never shorter than the en-IN value; any extension is Cal [Hypothesis; owner: native subject editor with the academic lead; pilot: first hi-in lesson]. The Interaction Spec records the value with `tag: Hypothesis`, `owner` and `pilot_ref`; the schema rejects an untagged null.

**Window rules.**
- The window is room tone inserted in the edit, never digital silence and never a TTS break tag. Break tags cap at 3 s where supported [11:N1], and Eleven v3/v4 support none [11:N2] (11 Step 8).
- Narration stops during the window; the question, givens and relevant diagram stay visible (02 §B2, §C1).
- "Do not use a two-second silence as evidence that students had a fair opportunity to solve a problem" (02 §G3). A think window below 4 s fails schema validation. Added 15 Oct 2026: a think window below 5 s without `binary_choice: true`, and a `call_response` window below 6 s, also fail schema validation; the upper bound is checked by IQ-03 against the level's `think_window_s.max`.
- A multi-step task always uses pause-video with the 03 wording: "Pause here and give yourself the time you need. Resume when you have an answer to check."
- Every substantial pause states what to produce → what help is available → when to resume → how to check → what to repair (02 §F1).
- A Short that asks a question gets the window or does not ask (11 Step 1).
- No visible countdown (02 §F7, §H5). `timer_display` is `none` by default and always `none` at AC0; a neutral progress indicator at AC1/AC2 is a style option to test [Hypothesis; owner: founder; pilot: 11 A/B].

---

## 4. Per-level rules

| Level | Allowed types | Frequency | Windows | Feedback form | Confidence checkpoint |
|---|---|---|---|---|---|
| `level/l1_2` | call_response, point_and_say, sing_along, move_along, predict (picture), read_along | Cal (child-development reviewer) | call_response, think | Conditional, names an action; no "wrong" | None in video [Recommendation] |
| `level/l3_5` | Above + draw, retrieve_definition (say-aloud), complete_missing_step and solve_independently (objects, "let's try together"), verify | Cal | think, call_response; pause-video only with a grown-up cue [Recommendation] | As l1_2 | Optional gentle "Which part could you do by yourself?" if the child-development reviewer approves |
| `level/l6_8` | predict, retrieve_definition, record_formula, reconstruct, draw, complete_missing_step, solve_independently, explain_error, verify, classify, read_along (F23), plan_time (junior overlays), do_along | Start from the l9_10 pattern [Hypothesis; owner: academic lead; pilot: first l6_8 lesson] | think, pause-video | correct → change → next | Three checkpoints |
| `level/l9_10` | All school types except read_along | 3–4 brief predictions or checks + 2–3 substantial pauses per ~10 min, roughly one invitation every 75–120 s, placed at conceptual boundaries (Inherited production hypothesis, 02 §F2, 03 §4.2) | think (5–8 s, default 6), pause-video | correct → change → next | Three checkpoints and the 2×2 |
| `level/l11_12` | As l9_10 + viva_prompt (practical viva), derivation step completion | As l9_10 | As l9_10 | As l9_10 | As l9_10 |
| `level/ug` | As l11_12 + discussion_prompt, critique (optional) | ≥1 `check.interpolated` per chapter [N30] (contested) | think, pause-video | Criteria-based model answer | Three checkpoints |
| `level/pg` | As ug + critique | One critique prompt per chapter [Recommendation] | Mainly pause-video | Criteria plus stated uncertainty | Three checkpoints |
| `level/adult_prof` (adult professional; exam overlays add the patterns, "competitive" is an overlay and not a level) | School and ug types + plan_time | Per base register; overlay patterns | think, pause-video | As ug | Three checkpoints |
| `level/voc` | do_along, predict, verify, complete_missing_step, solve_independently, record_formula (procedure reference), explain_error ("spot the unsafe step"), retrieve_definition, classify, reconstruct (added 15 Oct 2026 so F1, F3, F10, F11, F13, F14 and F24 have a legal type) | Cal [Hypothesis; owner: trade instructor] | pause-video for do-along | Safety error branch first | Three checkpoints |
| `level/educator` | discussion_prompt, predict ("which misconception will your class show?") | Per `teach.move` | pause-video | No single answer; model points | None |

Interactions sit where the reasoning changes, never where a stopwatch says (02 §B1, §F4). Retrieval is justified by learning, never by an "attention reset" claim (RD-06; 02 §F4).

---

## 5. Answer-reveal rules

1. **Hidden until the window ends** in narration, display, captions, overlays, audio description, thumbnail and the following preview (03 Step 7; 07/03 S6). `check_answer_hidden: true` is a Format Spec constant; `answer_hidden_until_reveal: true` and the channel list are Interaction Spec constants.
2. The reveal beat declares `answers_after`; its reveal cue cannot precede the window, checked at validation and again at assembly ("Premature answer", 05 §7.2).
3. Captions show the prompt only during the window. The transcript places the answer after a "pause point" marker (`transcript_order`).
4. Reveal order: relationship before substitution (02 blueprint 07:45–08:05); for definitions, a model answer plus a short checklist (02 §F3).
5. In an ExamLeaf player, the reveal follows a learner "Continue to explanation" action, never an automatic reveal after a stressful countdown (02 §F7). On ordinary platforms: spoken pause instruction plus a stable prompt.
6. A Short delivers its answer inside the Short (07/05 principle 3); a cover never shows it.
7. **No fabricated responses.** No narrator, story character or on-screen "student" answers for the learner before the window ends, and no script contains an invented learner answer ("A student says: four").
8. `discussion_prompt` and `critique` use `no_single_answer`: a model response is labelled as one possible answer with its criteria.

---

## 6. Feedback script rules

**Structure (03 Step 9; 02 §H3).** What was correct → what needs to change → what to do next. Every feedback sentence maps to `ASM.feedback`, `ASM.hint` or the confronting claims of the MIS it repairs (closure).

**Conditional wording.** Prerecorded feedback is always conditional: "If you obtained 1.5 A using this relationship, your method matches the model" (02 §H3). Never "I heard you", "Yes! You got it!", "Everyone got this" (03 Step 7).

| Branch (`error_kind`) | Pattern (adapted from 03 Step 9 and 02 §H3) |
|---|---|
| correct, method shown | "If you chose I = V/R, you picked the right relationship. Now check the unit." |
| `arithmetic` | "If the relationship is right but the number differs, recheck the substitution rather than restarting." |
| `representation` | "If you read the graph the other way, check which quantity is on each axis." |
| `strategy` | "If you started with a different formula, look again at what is given and what is unknown." |
| `terminology` | "If you wrote the number without a unit, add it: the answer is a current." |
| `prerequisite` | "Need the symbol-reading version? Start here." (03 Step 3; never "for weak students") |
| `misconception` | Confront with evidence or a counterexample from the MIS's `confronted_by` claims (02 §I3); never a red cross alone |

**By level.** AC0: "If you said a bigger push, you are thinking like a scientist"; the repair is "Let's look again together"; no "wrong". l6_8 to l11_12: the 03 patterns. ug and pg: criteria-based ("A complete answer names the assumption and the domain"). voc: the safety branch comes first.

**Forbidden** (02 §H4; 03 Step 9): identity praise ("You are a genius"), "This is so easy", "You just need to try harder", promised marks, claims to know the learner's feelings.

---

## 7. Confidence-calibration checkpoints

Three checkpoints, never collapsed into one "mastered" badge (03 Step 9): **I followed it. I completed a step with support. I solved a related problem without support.**

The video speaks the 2×2 response conditionally (02 §H1):

| State | Spoken response |
|---|---|
| Correct and confident | "If you solved it without help, try a less familiar version next." |
| Correct but unsure | "If your answer matched but you were unsure, check the reasoning step once more on a new question." |
| Incorrect and unsure | "If you were unsure and got a different answer, use the hint and try once more." |
| Incorrect but confident | "If you were sure and got a different answer, compare your step with this one: that difference is the idea to fix." |

Placement: Detailed close (02 blueprint 09:20–09:35), Worked Example after the faded twin, Practice Set end, Misconception Fix after the re-test. Not in Shorts or Flashcard Reels. AC0 has no self-rating in video [Recommendation, pending the child-development reviewer]. Self-reports are captured only by the platform (`self_report_captured_by: platform`). The video never awards "Mastered"; lesson completed and skill demonstrated stay separate (02 §H6).

---

## 8. Assessment item kinds

Every item is an ASM node approved at GA-Graph. Its answer key is solved independently of the creative draft, and a second, independent re-solve checks it; "two models agreeing is not scientific validation" (03 Step 1; 07/03 S7).

| Kind | Stored as (`ASM.item_kind`) | Required content | Display and validation rules |
|---|---|---|---|
| MCQ | `mcq` | `options[]` with exactly one `is_key`; in original items each distractor carries `distractor_source` (MIS, WRK step or wrong-method fixture); past-paper distractors stay as printed | Each distractor maps to an MIS or a WRK common error [Recommendation]; `expected_answer` equals the key's `option_id` (Q-CLOSURE); options visible during the window |
| Numerical | `numeric` | `expected_answer` as `<decimal> <unit>` (schema pattern; unit `1` if dimensionless); `acceptable_variations` in the same form, enumerated from the fixture's rounding rule (e.g. `0.40 A`, `400 mA`); no tolerance field | Fixture recompute (Q-FIX); unit required in the model answer (02 §E5) |
| Short answer | `short` | `rubric[]` (one criterion per expected component, each citing CLMs); `acceptable_variations` | Component checklist on reveal (02 §F5) |
| Long answer, drawing | `long` | Model answer (`expected_answer`) and `rubric[]` (criteria or sketch checklist, each citing CLMs) | Reviewer key |
| Diagram label | `diagram_label` + MED diagram (enum value added to `lesson_graph.schema.json` 15 Oct 2026; was `match` before) | `pair_keys[]` (label → MED region id) | Labels and shapes, never colour alone (WCAG 1.4.1, CE-22); not allowed for audio_only |
| Ordering | `ordering` (enum value added 15 Oct 2026; was `match` with positions before) | `sequence[]` in the correct order | Procedure fixture or reviewer key; audio_only only if fully spoken |
| Fill in the blank, match | `fill_blank`, `match` | `blank_keys[]` (`fill_blank`) or `pair_keys[]` (`match`) | As above |
| Oral or viva | `oral` | Model answer and `rubric[]` | Reviewer key; audio_only allowed (F25) |
| Practical | `practical` | Procedure steps and checks; `rubric[]` | procedure_completeness |
| Past-paper item | Any kind, `original: false` | `exam_tags.source_id`, `board_or_exam`, `year`; `marks` only with `marks_source ∈ {source_paper, official_key}`; `stem_form` (`verbatim` \| `adapted`); a step-wise split only as `exam_tags.marking_scheme[]` (`step`, `marks`, optional `wrk_step_ref`, `key_span` into the official key) | Board, year and paper on screen; ~~text licence (Q-RIGHTS)~~ a `verbatim` stem needs the `exam_tags.source_id` SRC to have a `rights_status` other than `consulted_only` (Q-RIGHTS, extended to past-paper ASM stems 15 Oct 2026). *(Level-1, CE-112, 15 Oct 2026.)* That SRC also needs `rights_basis` citing a current `rights/<publisher>@x.y.z` entry, for a verbatim stem and for official-key marks alike; until O-23 (Counsel) closes no such entry exists, so M1's past-paper item uses `stem_form: adapted` and shows no marks. With no registered key, marks are not shown; step marks sum to `marks` (Q-CLOSURE) |
| Original practice item | Any kind, `original: true` | No marks, no marks source | Labelled "Original practice question" (CE-31) |
| Diagnostic item | The ASM in `MIS.diagnostic_item`, usually `evaluative: false` | Pre/post pair | Same item before and after in Misconception Fix (`pre_post`) |
| Delayed-practice item | A twin or variant ASM | Changed cues against the in-video item (02 §I4) | Delivered by the platform (§11) |

Note, 15 Oct 2026: before this date `node_ASM` in `schemas/lesson_graph.schema.json` held only the single `expected_answer` string, so options, rubrics, per-blank and per-pair keys, sequences, the numeric form, `stem_form` and a step-wise marking scheme could not be stored or validated. The fields `options[]`, `rubric[]`, `blank_keys[]`, `pair_keys[]`, `sequence[]`, `stem_form` and `exam_tags.marking_scheme[]`, and the per-`item_kind` required rules (mcq → `options`; numeric → the `<decimal> <unit>` pattern; short, long, oral, practical → `rubric`; fill_blank → `blank_keys`; match, diagram_label → `pair_keys`; ordering → `sequence`; past-paper → `stem_form`), are added there [Recommendation] (stitched into the schema 15 Oct 2026; meta-validated with draft-07).

Representation tags (level-3+, CE-121, 15 Oct 2026). An ASM stem may carry the optional `depicted_attributes` tags {given_name_origin_region, gender_presented, setting, disability_presented, language} for the people it names or shows (never real children). They feed only the quarterly corpus report Q-REPR (QA_PROFILES §2.13), which never blocks an item. A REN of an ASM changes wording only and never its keys (CE-118); a culturally adapted word-problem context is a new WRK node with `adapted_from` and `locale_scope[]`.

ASM authorship (added 15 Oct 2026). ASM item drafts (item_kind, stem, options, hints, feedback, MIS links) come from examleaf-interaction-design with examleaf-interactive-teaching-director at S4 and are written by graph-author. The first independent answer-key solve is made by examleaf-claim-research (method: fixture, solver or official scheme) and recorded in ASM.answer_key_check. At S6 these skills bind only ASM nodes present in the Format Plan; a new question is a compile error routed to graph-author.

---

## 9. Items and interactions per format

| Format | Interactions | Items |
|---|---|---|
| F1 detailed | predict, reconstruct, complete_missing_step, solve_independently, draw, verify; 3–4 brief + 2–3 substantial at l9_10 (l1_2: predict (picture), point_and_say or call_response only) | Original or past items; diagnostic optional; checkpoint at close |
| F2 simplified | predict, one retrieve_definition | One item |
| F3 recap | retrieve_definition per objective (l1_2: point_and_say or call_response per objective) | Key-claim recall items |
| F4 question_analysis | predict or solve on the root item; the `marking.scheme` beat draws only from `exam_tags.marking_scheme[]`, each step's marks from a `key_span` in an official key, never an invented split | Root ASM (past or original); marks only from the key; with no registered scheme the `marking.scheme` slot is skipped |
| F5 short | One predict or true/false check | One diagnostic or recall item |
| F6 worked_example | Pause per step, predict before the final step, complete_missing_step on the twin | WRK + twin |
| F7 misconception_fix | Diagnostic pre and post (l1_2: predict (picture) as the pre and post diagnostic) | `diagnostic_item` pair |
| F8 concept_intro | One predict | One item |
| F9 exam_strategy | plan_time, solve on 1–2 past items | Past items only, with exam tags |
| F10 revision_sheet | retrieve_definition per card; check every 3–5 cards | Recall items |
| F11 flashcard_reel | One retrieve_definition (l1_2, l3_5: point_and_say on the picture card) | One item |
| F12 lab_demo | predict before observe; do_along (voc) | Observation item |
| F13 comparison | classify | Classification items |
| F14 story_history | call_response (AC0); retrieve_definition (L6+) | Recall items |
| F15 qa_doubt | One check | One item |
| F16 series | Members' interactions | Members' |
| F17 practice_set | solve_independently per item | 3–5 items at l3_5; ordered by difficulty |
| F18 prerequisite_repair | Diagnostic predict first | Lower-level diagnostic |
| F19 derivation_proof | predict before the final step; complete_missing_step | Derivation items |
| F20 lecture_segment | One interpolated check per chapter | Chapter items |
| F21 source_analysis | retrieve_definition, explain (attributed interpretation) | Source-based items |
| F22 perspectives | retrieve_definition on positions, never "which side is right" | Attribution items |
| F23 read_along | read_along; call_response at l1_2 and l3_5 only; retrieve_definition at l6_8 | VOC recall |
| F24 concept_map | retrieve_definition on a link | Edge recall |
| F25 viva_prep | viva_prompt | Oral items |
| F26 teacher_explainer | discussion_prompt | Diagnostic items shown to teachers |

---

## 10. Item validation per family

| Family | Answer key method (`answer_key_check.method`) | Rule |
|---|---|---|
| `family/stem_fixture` | `fixture` or `solver` | Expected answers are fixture outputs as decimal strings with units; acceptable variations come from the fixture's rounding rule; numeric distractors come from a fixture of the wrong method (`options[].distractor_source.fixture_ref`), never from guesses [Recommendation]; CS answers equal sandbox output |
| `family/quant_social` | `fixture` (ledger recompute) | Rates and thresholds carry as-of dates; an expired rate blocks release |
| `family/humanities_citation` | `official_scheme` or `reviewer_key` | The expected answer is entailed by a cited CLM; dates and names consistent across nodes; contested topics assess knowledge of the positions, never which side is right (CE-29); every `rubric[]` criterion cites approved CLMs within the item's objectives (`rubric_entailment`, added 15 Oct 2026) |
| `family/languages_literature` | `reviewer_key` or `official_scheme` | Grammar items cite a grammar reference or the board textbook; quotation items come from TXT with edition; interpretation items accept attributed readings; every `rubric[]` criterion cites linguistic_rule CLMs or a TXT with edition (`rubric_entailment`, added 15 Oct 2026) |
| `family/arts_skills`, `family/vocational` | `reviewer_key` with procedure fixtures | Practical and ordering items checked by procedure_completeness; safety claims required |
| `family/exam_strategy` | `solver` (aptitude), `official_scheme` | Pattern items recomputed from the stored paper set |
| `family/health_medicine`, `family/law` | — | Not activated (O-9) |
| `family/evs_foundational` (added 15 Oct 2026, [Recommendation]) | `fixture` (counts, measures) or `reviewer_key` | Play and talk orientation: no F9; F4 and F17 only in their l3_5 gentle variants (no marks, no exam framing) (corrected 15 Oct 2026); expected answers cited from the board textbook; the child-development reviewer co-signs |

---

## 11. Spacing schedule per level

The video initiates the cycle; it does not finish it (02 §B4). The video speaks only the end-of-lesson task and names one next action. Any later delivery is the platform's, with the learner's choice (02 §I5).

| Level | Schedule | Tag |
|---|---|---|
| l9_10, l11_12 | End of lesson: one unprompted explanation or application. Next day: brief recall before notes. About three days: a changed numerical or diagram question. About one week: mixed practice requiring method selection. Later, by exam timing: another delayed check (02 §I4) | Inherited production hypothesis; "no universally optimal 1-3-7 sequence" |
| l6_8, ug, pg, adult_prof | The 02 §I4 pattern as a starting point | [Hypothesis; owner: academic lead; pilot: first lesson at the level] |
| voc | End-of-lesson practical recap; later occasions Cal | [Hypothesis; owner: trade instructor] |
| l1_2, l3_5 | An optional gentle cue in the video ("Tomorrow, sing the push song again"); `platform_reminders: false` in the pipeline record | Cal; platform behaviour subject to G-COUNSEL (O-3, O-4) |
| educator | Not applicable | — |

Cues change between occasions: new wording, a different representation or orientation, a paper-style question (02 §I4). The schema forbids `none_same_session` after the end of the lesson and requires those occasions to be delivered by the platform.

---

## 12. Accessibility alternatives

Every interaction lists at least one alternative (02 §J; CE-22). Learners are never assigned to "visual" or "auditory" learning styles (02 §J).

| Response mode | Alternatives |
|---|---|
| write | `typing`, `oral`, `partial_template` |
| draw | `partial_template`, `describe_aloud`, `choose_from_options` |
| say_aloud, sing | `think_only`, `point` (or `choose_from_options`), captioned prompt |
| point | `describe_aloud`, `audio_described` |
| solve | `typing`, `oral`, `larger_view` |
| move | `seated` (required at AC0) or `think_only` |

**Keyboard and screen-reader labels (level-3+, CE-120, 15 Oct 2026).** Every interaction whose `item_presentation` is `mcq`, `match`, `ordering` or `diagram_label` carries `option_labels[]`: one entry per ASM option (the mcq `option_id`, the match or diagram-label left item, or the ordering element) with a `screen_reader_label` and a unique single-character `keyboard_key` (`1`–`9` or `A`–`Z`). The schema requires the array; Q-A11Y.asm_labels checks one entry per option and that no label differs in form for the keyed option, so a screen reader never reveals the answer. The exporter copies the array verbatim into `export/interactions.json`, where the sidecar schema requires it whenever the key has options. The profiles `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia` and `a11y/isl` (Architecture §3.1 addendum) change windows only through their tokens and the level band (a slower pacing band under `a11y/cognitive` lengthens think windows, never shortens them).

Rules: every prompt is captioned (`captioned_prompt`) and narrated if visual-essential; `audio_only` renders allow no diagram-label or ordering item and no pointing response (schema); the reduced-motion variant keeps the same windows; small symbols get a larger view rather than more text (02 §J). Handwriting is used where it supports equation work, but typing, oral explanation and other alternatives are always allowed (02 §F5).

---

## 13. Child-safety rules

**AC0 (`safety/ac0`, CE-19).** No competitive pressure, comparison, ranks or "fastest". No streaks, points, badges or variable rewards (02 §I5). No timers or countdown visuals or sounds. No request to say a name, school or anything personal aloud to the screen, and no comment, send, share or record prompts. No links or QR codes. No "wrong" framing. Any movement is space-safe with a seated alternative; any physical activity needs a household-safe ACT and the grown-up cue. No `plan_time`, `explain_error`, `record_formula`, `discussion_prompt`, `viva_prompt` or `critique` (schema). No marks.

**AC1 and AC2.** No fear, urgency or peer comparison in exam content; no threatening countdowns (02 §H5); time plans are information from the official pattern, never a clock on screen during a window. No data solicitation in AC1 (CE-20). The `safety_constraints` block is constant `true` for every level.

---

## 14. What the platform does and what the video does

| Concern | Video (pipeline) | Platform (outside the pipeline) |
|---|---|---|
| Prompt | Spoken and displayed; captioned | May mirror it as an input field |
| Window | Protected room-tone window or pause-video | "Continue to explanation" control |
| Response | Never captured (`response_capture_in_video: false`) | May capture, under counsel-approved data rules |
| Feedback | Conditional, the same for every viewer | May adapt, only on input it actually received (03 Step 7) |
| Confidence | Spoken checkpoint and routes | May record the self-report |
| Spacing | End-of-lesson task and one next action | Schedules later occasions with the learner's choice; none for AC0 unless counsel approves |
| Progress | Never says "mastered" | Keeps "lesson completed" and "skill demonstrated" separate (02 §H6) |
| Export | `export/interactions.json` (file role `interactions_json`), validated by `packaging_profile.schema.json#/definitions/interaction_sidecar` (15 Oct 2026; the earlier cell listed contents with no schema or file role); checked by Q-META.interactions_sidecar. Each option carries its keyboard key and screen-reader label (`option_labels[]`, CE-120, 15 Oct 2026) | Joins any learner data on its own side; may send back only aggregate `learning_signal` records keyed by these ids (Architecture §9.7, CE-117) |

---

## 15. Interaction Spec and QA checks

The Interaction Spec (schema) holds: identity and hashes (`sha256`, `interaction_spec_content_sha256`, `script_content_sha256`, `epp_hash`, `format_plan_sha256`), format, level, safety class, family, locale, render target, `interactions[]`, `confidence_checkpoints[]`, `spacing`, and the constant `platform_boundary` and `safety_constraints` blocks. ~~It is hashed by NFC → JCS → SHA-256 and reviewed at GA-Δ with the script; any change to it is a script change.~~ Corrected 15 Oct 2026: it is hashed by NFC → JCS → SHA-256 with the `sha256` field excluded, and `sha256` is required. ~~The GA-Δ approval's closure inputs are the Script Spec `sha256` and this `sha256` (Architecture §3.7).~~ Corrected again 15 Oct 2026 (resolver-07; GA-Δ binds content hashes, never whole-record hashes): the Interaction Spec references the Script Spec by `script_content_sha256` (was `script_spec_sha256`) and carries a required `interaction_spec_content_sha256` (NFC → JCS → SHA-256 with `sha256`, `interaction_spec_content_sha256`, `interaction_spec_id`, `version`, `epp_hash`, `format_plan_sha256`, `script_content_sha256`, `qa_results` and `provenance` removed). GA-Δ binds `script_content_sha256` and `interaction_spec_content_sha256` (Architecture §3.7). The artefact record lists both, so RELEASE-CHECK's recomputed closure covers it. Any change to the Interaction Spec's content stales GA-Δ; a pin-only registry release does not.

| ID | Check | Blocking? |
|---|---|---|
| IQ-01 | Schema valid; level ↔ safety class consistent (checked by Q-SCHEMA against the EPP; the schema no longer copies the mapping, 15 Oct 2026) | Yes |
| IQ-02 | Every answer-bearing interaction has an ASM or WRK step answer source | Yes |
| IQ-03 | Windows meet RD-11 (think ≥ 4 s; default 6; below 5 s only with `binary_choice: true`; at most the level's `think_window_s.max`; call_response ≥ 6 s); feeds Q-INT.window_length | Yes |
| IQ-04 | Answer hidden on every channel; `reveal_beat_id` matches the Script Spec `answers_after`; feeds Q-INT.answer_hidden, Q-INT.reveal_order | Yes |
| IQ-05 | Feedback conditional; branch sentences map to ASM or MIS nodes | Yes |
| IQ-06 | Marks only from source paper or official key; original items labelled | Yes |
| IQ-07 | AC0 rules (types, timers, marks, reminders, seated alternative for movement, grown-up cue for pause-video) | Yes |
| IQ-08 | Accessibility alternatives present; audio_only restrictions | Yes |
| IQ-09 | Level allows the type; frequency against the level pattern | Report-only until pilots (CE-35) |
| IQ-10 | Spacing cues change across occasions | Yes |
| IQ-11 | Hypothesis values carry owner and pilot | Yes |
| IQ-12 | Interaction variety (not all one type in a long format) | Report-only |
| IQ-14 | For `locale/hi-in` and `locale/hinglish`: when the Script Spec has `beat_map_of` and that master's Interaction Spec (found via its `interaction_spec_id`) is `locale/en-in`, every `window.seconds.value` must be ≥ the master value for the same `interaction_id`. A longer value carries `tag: Hypothesis`, `owner` and `pilot_ref` (§3). Added 15 Oct 2026 | Yes |
| IQ-15 | Every option of an `mcq`, `match`, `ordering` or `diagram_label` interaction has an `option_labels[]` entry with a screen-reader label and a unique keyboard key; no label marks the key (feeds Q-A11Y.asm_labels; level-3+, CE-120, 15 Oct 2026) | Yes |

---

## 16. Negative tests

| # | Input | Required outcome |
|---|---|---|
| NI-01 | A prediction with a 2 s think window | IQ-03 fails; schema rejects below 4 s |
| NI-02 | "Yes! I heard you say four!" after a window | Script SQ-05 blocks; IQ-05 requires conditional feedback |
| NI-03 | Caption shows "0.4 A" during the window | IQ-04 blocks |
| NI-04 | An original practice item displays "2 marks" | IQ-06 and schema fail (CE-31) |
| NI-05 | An AC0 episode adds a 10-second countdown clock | IQ-07 blocks |
| NI-06 | An AC0 check says "Tell me your name and your school!" | Q-SAFE and IQ-07 block (CE-19) |
| NI-07 | A multi-step calculation gets a 6 s think window | Schema rejects (15 Oct 2026): solve_independently, record_formula, reconstruct, draw, plan_time, discussion_prompt, critique and do_along, and any `write` or `draw` response mode, require pause-video (03 Step 7) |
| NI-08 | The next-day item repeats the in-video item verbatim | IQ-10 fails (02 §I4) |
| NI-09 | Video feedback branches on what the learner "said" | Schema: `adaptive_feedback_in_video` is constant false |
| NI-10 | A diagram-label item in an audio_only render | Schema rejects |
| NI-11 | A Perspectives check asks "Which historian is right?" | IQ-05/GA-Δ reject (CE-29) |
| NI-12 | A story character answers the call-and-response before the window ends | IQ-04 blocks; fabricated response |
| NI-13 | A Hindi edition shortens the think window "to fit" | IQ-14 rejects; overrun is a compile error (R5) |
| NI-14 | An AC0 spec lists a next_day platform occasion | Schema and IQ-07 reject (O-3) |
| NI-15 | An MCQ interaction with no `option_labels`, or whose keyed option's label reads "Option B, correct answer" (15 Oct 2026) | Schema rejects the missing array; IQ-15 / Q-A11Y.asm_labels block the revealing label |
| NI-16 | A hi-IN REN of an ASM changes its key or a WRK number to suit a local context (15 Oct 2026) | Q-CLOSURE.ren_equivalence critical; the adapted context must be a new WRK node with `adapted_from` (CE-118) |

---

## 17. Worked example: Interaction Spec for the Ohm's-law Detailed lesson (`level/l9_10`, en-in)

Graph IDs as in the Scripting Registry §18. With the `<sha256>` and model-ID placeholders filled, this instance validates against `interaction_spec.schema.json` (checked with `jsonschema`, Draft-07, on 15 Oct 2026). Two interactions are shown; the full spec adds the Ch1 reconstruct pause, the faded-twin completion and the final draw-and-state retrieval from the 02 blueprint.

```json
{
  "interaction_spec_id": "IS-phy10-ohm-detailed-en",
  "version": "1.0.0",
  "hash_canon": "JCS-RFC8785+NFC",
  "sha256": "<sha256>",
  "script_spec_id": "SS-phy10-ohm-detailed-en",
  "interaction_spec_content_sha256": "<sha256>", "script_content_sha256": "<sha256>", "epp_hash": "<sha256>", "format_plan_sha256": "<sha256>",
  "format": "format/detailed", "level": "level/l9_10", "safety_class": "safety/ac1",
  "family": "family/stem_fixture", "locale": "locale/en-in", "render_target": "video",
  "interactions": [
    {
      "interaction_id": "II-d-01", "beat_id": "b03", "slot": "explain.ladder_step",
      "itype": "predict", "prompt_sentence_ids": ["b03-s3"], "response_modes": ["think"],
      "asm_id": "ASM-ohm-predict-4v", "asm_item_kind": "numeric", "evaluative": false,
      "item_presentation": "numeric",
      "window": {"kind": "think", "seconds": {"value": 6, "tag": "Inherited", "source": "RD-11 default think window"},
                 "protected": true, "prompt_stays_visible": true, "narration_stops": true},
      "reveal": {"trigger": "window_end", "reveal_beat_id": "b04", "answer_hidden_until_reveal": true,
                 "hidden_channels": ["narration", "display", "captions", "overlays", "audio_description", "thumbnail", "preview"]},
      "feedback": {"structure": "correct_change_next", "conditional": true, "sentence_ids": ["b04-s2"],
                   "branches": [{"error_kind": "representation", "sentence_id": "b04-s3"}]},
      "accessibility_alternatives": ["think_only", "captioned_prompt"],
      "timer_display": "none", "item_label": "none"
    },
    {
      "interaction_id": "II-d-04", "beat_id": "b16", "slot": "check.interpolated",
      "itype": "solve_independently", "prompt_sentence_ids": ["b16-s1", "b16-s2"], "response_modes": ["solve", "write"],
      "asm_id": "ASM-ohm-9v6", "asm_item_kind": "numeric", "mis_ids": ["MIS-ivr-invert"], "evaluative": true,
      "item_presentation": "numeric",
      "window": {"kind": "pause-video", "seconds": {"value": 10, "tag": "Inherited", "source": "02 blueprint 07:35-07:45 media hold"},
                 "protected": true, "prompt_stays_visible": true, "narration_stops": true},
      "reveal": {"trigger": "learner_continue", "reveal_beat_id": "b17", "answer_hidden_until_reveal": true,
                 "hidden_channels": ["narration", "display", "captions", "overlays", "audio_description", "thumbnail", "preview", "transcript_order"]},
      "feedback": {"structure": "correct_change_next", "conditional": true, "sentence_ids": ["b17-s1", "b17-s2", "b18-s1"],
                   "branches": [{"error_kind": "misconception", "mis_id": "MIS-ivr-invert", "sentence_id": "b18-s2"},
                                {"error_kind": "arithmetic", "sentence_id": "b18-s3"},
                                {"error_kind": "terminology", "sentence_id": "b18-s4"}]},
      "accessibility_alternatives": ["typing", "oral", "larger_view"],
      "timer_display": "none", "item_label": "examleaf_practice_question", "marks_display": {"shown": false}
    }
  ],
  "confidence_checkpoints": [
    {"checkpoint_id": "CC-d-01", "beat_id": "b21", "kinds": ["followed", "completed_with_support", "solved_without_support"],
     "prompt_sentence_ids": ["b21-s1"], "route_sentence_ids": ["b21-s2", "b21-s3"], "self_report_captured_by": "platform"}
  ],
  "spacing": {
    "schedule_ref": "02 §I4", "tag": "Inherited", "platform_reminders": true,
    "occasions": [
      {"occasion": "end_of_lesson", "asm_ids": ["ASM-ohm-9v6"], "cue_change": "none_same_session", "delivered_by": "video"},
      {"occasion": "next_day", "asm_ids": ["ASM-delayed-ohm-recall"], "cue_change": "new_wording", "delivered_by": "platform"},
      {"occasion": "about_3_days", "asm_ids": ["ASM-ohm-iv-graph-2"], "cue_change": "new_representation", "delivered_by": "platform"},
      {"occasion": "about_1_week", "asm_ids": ["ASM-elec-mixed-1"], "cue_change": "mixed_method_selection", "delivered_by": "platform"}
    ]
  },
  "platform_boundary": {"adaptive_feedback_in_video": false, "response_capture_in_video": false, "interaction_sidecar_exported": true},
  "safety_constraints": {"no_competition_or_comparison": true, "no_streaks_or_variable_rewards": true,
                         "no_threatening_countdowns": true, "no_data_solicitation": true, "no_links_in_prompts": true},
  "provenance": {"author_kind": "model", "author_id": "kit/interaction-fill", "created_at": "2026-10-15T09:00:00Z",
                 "model_id": "<full model id>", "effort": "medium", "kit_version": "1.0.0"}
}
```

Script lines behind it: b03-s3 "Now make it four volts. Predict the current." b04-s2 "If you predicted zero point four amperes, you kept the resistor and temperature fixed, which is what the rule needs." b16 "A six-ohm resistor is across nine volts. Pause, write your relationship, calculate, and include the unit." b18-s2 "If you multiplied nine by six, you used V equals I R the wrong way round: current is voltage divided by resistance."

What it shows: the predict uses a think window because it is a simple prediction; the independent solve uses pause-video because it is multi-step (03 Step 7); the original item shows no marks; every feedback branch is conditional and names a node; later spacing occasions change cues and belong to the platform.
