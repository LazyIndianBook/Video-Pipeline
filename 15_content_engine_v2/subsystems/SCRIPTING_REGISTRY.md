# Scripting Registry v1 (the Script Spec layer)

Status: subsystem specification. Date: 15 Oct 2026. Stage: S6 (Script per format), checked at S7 and reviewed at GA-Δ.
Reads: the EPP and the Format Plan (Architecture §3.5, §5.1). Writes: one **Script Spec** per artefact (`subsystems/schemas/script_spec.schema.json`), from which the compiler emits the v1 NarrationPlan (05 §7) and the ST beat table (07/03 S5).
Generalises, does not replace: 03 Super Teacher authoring (ladder, loop, humour ceiling, delivery modes, pacing, master prompt, negative tests), 02 production rules (§B–§I), 05 §7 structured narration, 11 Step 1 beat tags, 07/03 S5–S6.

**Citation convention.** [N#] = `15_content_engine_v2/SOURCES_and_claims.md`. [11:N#] and [11:P-S#] = section 11 registers. Section references (02 §G2, 03 Step 7, 05 §7.2, 11 Step 1, 13 §5.3, RD-11) point to existing project rules and are **Inherited** unless tagged otherwise. **[Recommendation]** = design choice made here. **[Hypothesis]** = value a pilot must confirm (owner named). No number below is new: where the project has none, the value is "Cal" (calibrate), which is a Hypothesis.

---

## 1. What a Script Spec is

A Script Spec is the hashed, sentence-level script for one artefact: one format × level × locale × request. It does three jobs:

1. **Fill slots, never add truth.** Every beat is one slot instance from the Format Plan. Every spoken sentence carries the node IDs it draws from. A sentence that asserts something must map to an approved CLM, SIM, WRK step or ASM in the Format Plan (CE-12). Numbers, dates, names and units must appear in a referenced node or a fixture output.
2. **Keep the four fields apart** (03 Step 10; 07/03 S5 rule 13): `spoken_text` (clean, no tags), `display_text` (equations and on-screen strings, externalised per CE-39), `direction` (mode, pace band, emphasis), and renderer events (`cues`, `pause_after`).
3. **Expose the derived surface for GA-Δ.** Every SIM and ANL used, every new wording, every interaction prompt and the sentence-to-node map are listed, so the reviewer reads the whole script with the new surface highlighted (CE-13).

Storage: `content/scripts/<artefact_id>/SS-<id>.json`, hashed NFC → JCS → SHA-256 (CE-32); the fields `sha256`, `status`, `timing_status`, `closure`, `qa_results`, `recent_script_ledger`, `rehearsal` and `provenance.created_at` are excluded from the hash (they are check and lifecycle records, written after the content is fixed; corrected 15 Oct 2026). The record pins `epp_hash`, `format_plan_sha256` and `graph_subtree_sha256`. **Content hash (added 15 Oct 2026).** `script_content_sha256` = NFC → JCS → SHA-256 over the Script Spec with these keys removed: `sha256`, `script_content_sha256`, `script_spec_id`, `version`, `status`, `timing_status`, `request_id`, `epp_hash`, `format_plan_sha256`, `graph_subtree_sha256`, `pins`, `closure`, `fills`, `qa_results`, `recent_script_ledger`, `rehearsal` and `provenance`. Everything else is reviewed content and stays in: `beats` (sentences, direction, cues, `planned_ms`), `derived_surface`, `disclosure`, `locale` and `beat_map_of`. GA-Δ binds `script_content_sha256`, so a registry release that changes pins but not one word reopens no GA-Δ (Architecture §3.6). Model fills are stored by hash and replayed, so the same inputs reproduce the same content hash (CE-38). Timing stays `PLANNED_NOT_AUDIO_MEASURED` until narration is measured. A locale edition is a separate Script Spec with the same beat map (11 Step 7), linked by `beat_map_of`. Approval state lives only in approval records (Architecture §3.7).

---

## 2. Word budgets

Format Specs carry no WPM numbers (CE-16). Pace comes from the Level Profile through the EPP. The compiler derives budgets per beat; nobody types a word count.

**Per-beat formula.**
`speech_s(beat) = planned_ms(beat) / 1000 − pause_after_s − inspection_holds_s − visual_only_s`
`words(beat) ∈ [ speech_s × wpm_band.min / 60 , speech_s × wpm_band.max / 60 ]`

`planned_ms` (integer milliseconds, so the hash canon never sees a computed float; renamed from `planned_s` 15 Oct 2026) comes from the R5 duration intersection split across the grammar by the Format Plan. The pace band per beat is `ordinary`, `dense` (new symbolic relationship or notation), `recap` (familiar material) or `teacher_set`.

**Inherited bands (l9_10, l11_12).** Ordinary 130–155 wpm; dense 105–125 wpm, down to 90–120 where a relationship is brand new (RD-10; 02 §G2; 03 §9.3); recap 145–165 wpm (02 §G2). These are production hypotheses under the 11 A/B plan, not optima. Pause values: 0.3–0.6 s between phrases, 0.8–1.5 s after a key causal statement, 2–4 s to inspect a completed transformation (02 §G3).

**Worked arithmetic (Inherited values only).** A 600 s Detailed lesson plans roughly 1,100–1,250 narration words (03 §9.3); 02 §G2 checks the range: 1,050 words at 155 wpm is 6.8 min of speech, leaving the rest for pauses and slow passages. A 35 s Short with one 6 s think window and about 2 s of beat pauses leaves 27 s of speech: 27 × 130/60 ≈ 58 to 27 × 155/60 ≈ 70 words.

**Levels without a pace value.** l1_2, l3_5 and voc pacing is Cal (owner: child-development reviewer for AC0; trade instructor for voc). ~~l6_8, ug and pg start from the inherited bands as [Hypothesis].~~ l6_8 starts from the inherited bands as [Hypothesis]; ug, pg and adult_prof use them as Inherited defaults (LP §3.6–3.8); faster bands only as [Hypothesis] under A/B. The recap band (145–165 wpm) is owned by LP §3.4, and `wpm_recap` is required in `level_profile.schema.json` (corrected 15 Oct 2026). For a `teacher_set` beat the word budget is `null` with tag Hypothesis, and the binding constraints become segment seconds, `max_sentence_words` and `max_new_ideas_per_segment` from the Level Profile. ~~Path A rehearsal measures the real duration.~~ The timed read-aloud under **Null-budget scripts** measures the real duration before GA-Δ (corrected 15 Oct 2026).

**Locales.** Word rates do not transfer between languages (02 §G2): hi-in and Hinglish bands are Cal [Hypothesis; owner: native subject editor; pilot: first hi-in lesson]. Hindi often runs longer [Hypothesis, 11 Step 7]; beats are re-timed, never sped up. Level Profile wpm bands are en-in values. Until the pinned Locale Profile carries a measured `pacing_by_level.<level_id>` band (tagged range, owner native subject editor), every beat of a Script Spec whose locale is not `locale/en-in` has `wpm_band: teacher_set`, `target_wpm: null` and `word_budget {min: null, max: null, tag: Hypothesis}`; the compiler never applies a Level Profile wpm value to another locale (lint SQ-07) [Recommendation; added 15 Oct 2026].

**Overrun rule.** A beat more than about 10% over budget at read-aloud is cut, not sped up [Recommendation, 11 Step 1]. A locale whose narration exceeds the R5 budget is a compile error routed to the spec owner, never a silent cut (R5).

**Null-budget scripts [Recommendation; added 15 Oct 2026].** When any beat has `wpm_band: teacher_set` (null word budget), S7 requires a timed read-aloud of the full script at the level's natural pace before GA-Δ, by the assigned Path A performer or, before casting, the author under the level's pacing owner. It is stored as `rehearsal` and must lie within `duration_budget_s`, with no beat more than about 10% over its `planned_ms` (Overrun rule); otherwise a compile error goes to the spec owner (R5). Rehearsal timings feed the Level Profile calibration (child-development reviewer for AC0; trade instructor for voc). `rehearsal` is excluded from both hashes (§1).

---

## 3. Slot sources: what each beat may draw from

The closed slot vocabulary (43 types, Architecture §5.2) fixes which nodes each beat may use. The closure check rejects a sentence citing a node type its slot does not allow.

| Slot | May draw from | Scripting rule |
|---|---|---|
| `hook.realworld` | MED (with rights), CON rung 1, ACT (AC0), CLM[key] | An interpretable situation; its knowledge gap closes later (02 §I1) |
| `hook.question_reveal` | ASM.stem, WRK.problem, TXT | Question stays on screen through the window |
| `hook.surprise` | MIS.statement (as a question), diagnostic ASM | Genuine question; no fear or false statistic |
| `explain.ladder_step` | CON by rung, its `supports` CLM, SIM[permitted_levels ∋ level] | One rung per beat (03 Step 4) |
| `explain.definition` | VOC + `definition_claim_id`; ASM.stem ("what is asked") | Plain meaning first, then the exam term |
| `explain.analogy` | ANL[permitted_levels ∋ level] | Speaks mapping, non-mapping and formal return (03 Step 5) |
| `explain.derivation_step` | CLM chain via `requires`, WRK.steps, CLM.assumptions, fixtures | §12 |
| `worked.step` / `worked.faded_twin` | WRK.steps[n] (`claim_ids`, `fixture_ref`, `common_error_mis_ids`) / WRK with `twin_of` | Reveals the decision behind the step; numbers from fixtures |
| `check.interpolated` / `predict` / `retrieval` | ASM; for predict, the WRK step before its reveal | The interaction spec binds window, reveal and feedback |
| `misconception.elicit` / `confront` / `retest` | MIS.statement, why_plausible / `confronted_by` CLM, ACT observations / `diagnostic_item` | Tempting idea, never fact; confront mandatory; 02 §I3 sequence; pre/post pair |
| `recap.retrieval` / `recap.statement` | ASM; CLM[key] / CLM[key], permitted SIM | Question first; statement verbatim or REN |
| `marking.scheme` | ASM.exam_tags (`marks`, `marks_source`, `marking_scheme[]`) (15 Oct 2026) | Source paper or official key only (CE-31) |
| `exam.pattern` / `exam.time_plan` | CLM[claim_type=exam_pattern], fixture arithmetic | As-of date spoken; no predictions |
| `compare.dimension` | CLM pair sharing `contrast_dimension` | One dimension per beat, same frame for both |
| `activity.*` | ACT materials, steps, `safety_claim_ids`, `observation_claim_ids` | Safety cue before the first risky step; AC0 grown-up cue |
| `story.beat` / `story.song_chant` | STY.beats[n] and what it `carries` / STY.song_chant | Frame beats assert nothing; song verbatim with licence |
| `card.front` / `card.back` | ASM or VOC term / CLM[key], VOC definition, formula claim | Display/spoken split (RD-29) |
| `qa.doubt_statement` / `qa.answer` | MIS or ASM recorded by the academic team / CON, CLM | Never attributed to a learner (CE-20) |
| `source.show` / `read` / `interpret` | SRC citation / TXT verbatim / CLM[interpretation] | Registered editions only; interpretations attributed |
| `perspective.position` | CLM[contested_status ∈ attributed, contested] | One attributed position per beat; no verdict |
| `map.node` / `map.link` | OBJ, CLM; `requires`, `supports` edges | Approved edges only |
| `viva.prompt` / `viva.model_answer` | ASM[item_kind=oral] | Model answer from `expected_answer` |
| `teach.move` | MIS, ANL[permitted_levels ∋ taught_level].non_mapping, diagnostic ASM (`content_request.taught_level`, required for `level/educator`; 15 Oct 2026) | No claims about any real class |
| `bridge.return_link` / `chapter.title` | members' key CLM IDs, next member's OBJ / OBJ.statement | §10; titles assert nothing |
| `close.next_step` | delayed-practice ASM, next artefact pointer (never at AC0) | A learning action, never an engagement or product request; at AC0 `close_kind` is never `next_artefact_pointer` (CE-19; schema, 15 Oct 2026) |

**Window rule (added 15 Oct 2026).** A beat of any slot whose `pause_after.kind` is `think` or `pause-video` may also cite the one ASM bound by its `interaction_id`, and a beat with `answers_after` may cite that same ASM; no other cross-slot node type is allowed. Fixture cases are cited in `fixture_refs`, never in `node_ids`.

---

## 4. Script grammar per format

Hook and close kinds are enums in the schema. Hook: `realworld`, `question_reveal`, `surprise`, `contradiction`, `unfinished_task`, `none`. Close: `delayed_practice`, `capability_check`, `next_artefact_pointer`, `open_loop`, `retest`, `calm_end`, `none`. Every check beat has a hidden answer, a protected window and conditional feedback (Interaction and Assessment Registry). Every format ends with the disclosure record (§15, SQ-12).

| Format | Hook | Close | Retrieval and feedback beats | Exam-language conversion | Level notes |
|---|---|---|---|---|---|
| F1 `detailed` | realworld | capability_check + delayed_practice | ~~One check per chapter~~ At least one check per chapter; total frequency from the level row of the Interaction Registry §4 (l9_10, l11_12: 3–4 brief predictions or checks + 2–3 learner-controlled pauses per ~10 min, Inherited production hypothesis); each substantial pause states what to produce, the help available, when to resume, how to check and what to repair (07/03 S5 rule 3; corrected 15 Oct 2026); faded twin; independent attempt; recap retrieval; feedback after each | In `recap.retrieval` (03 Step 11, 7:45–9:15) | AC0 "episode": `activity.*` and `story.beat` replace worked slots; no exam language. ug/pg: notation-dense |
| F2 `simplified` | realworld | next_artefact_pointer (Detailed) | One retrieval | None [Recommendation] | Not at l1_2. At l3_5 (ac0), `close.next_step` is delayed_practice, never a pointer to Detailed (CE-19; 15 Oct 2026). A claim without a permitted SIM is stated in full or omitted |
| F3 `recap` | none (retrieval opens) | delayed_practice | Retrieval before every statement | l9_10+: statement in exam form | AC0: `story.song_chant` variant. l11_12+: formula sheet |
| F4 `question_analysis` | question_reveal | capability_check (transferable rule) | Predict; trap; rule | `marking.scheme` (sourced only) | l3_5: "let's try together", no marks |
| F5 `short` | surprise / contradiction / unfinished_task | none, or one learning next step (AC1/AC2) | One check | Optional, one sentence | AC0: no calls to action |
| F6 `worked_example` | question_reveal | capability_check | Predict; faded twin | Answer form, unit, significant figures (02 §E5) | l3_5 simple: no twin, objects |
| F7 `misconception_fix` | surprise | retest | Pre/post pair | None | Gentle form: no "wrong" framing of the child |
| F8 `concept_intro` | realworld | next_artefact_pointer | One predict | None | No claims beyond rung 2. l1_2/l3_5: close is delayed_practice or calm_end (CE-19; 15 Oct 2026) |
| F9 `exam_strategy` | none (pattern, as-of) | capability_check ("plan your time") | Plan-time prompt | Throughout, from official papers | Exam Strategist register; junior overlays: no fear, urgency or comparison |
| F10 `revision_sheet` | none | delayed_practice | Every card is retrieval | Formula display/spoken split | l6_8 definitions; l11_12+ formula sheets |
| F11 `flashcard_reel` | none | delayed_practice | The card | None | AC0: picture card |
| F12 `lab_demo` | realworld | capability_check | Predict before observe | None | AC0: household-safe, grown-up cue; voc: procedure completeness |
| F13 `comparison` | question_reveal | capability_check | Classify-this | Optional | l6_8: 2 dimensions; ug/pg: up to 5 |
| F14 `story_history` | realworld or none | calm_end (AC0) / capability_check | Call-and-response (AC0) | L6+ only | §11; contested phrasing §7 |
| F15 `qa_doubt` | question_reveal | capability_check | One check | Optional | Not AC0 |
| F16 `series` | members' | open_loop or members' | Members' | Members' | §10 |
| F17 `practice_set` | question_reveal | delayed_practice | Every item | Answer form | l3_5: 3–5 items, play framing |
| F18 `prerequisite_repair` | none | next_artefact_pointer (target lesson) | Diagnostic first | None | Lower-level nodes, learner's own persona and register (R11). At AC0 the close is delayed_practice, never a pointer (CE-19; 15 Oct 2026) |

*Beat grammar per format is owned by `../FORMAT_REGISTRY.md` (README §2 owner table); the column that stood here duplicated it and was removed 15 Oct 2026. This table keeps the scripting-specific hook, close, retrieval, exam-language and level notes.*

**Compact formats.** F19 `derivation_proof`: `hook.question_reveal` → `explain.derivation_step` per step (assumption callout) → `check.predict` before the final step → `recap.statement` (§12). F20 `lecture_segment` (16:9): `chapter.title` → `explain.*` → `check.interpolated` per chapter. F21 `source_analysis`: `source.show` → `source.read` → `source.interpret` (attributed) → `check.retrieval`. F22 `perspectives`: `perspective.position` per position → `check.retrieval`; a verdict only when the board prescribes one, as "the syllabus states". F23 `read_along`: `source.read` (synchronised highlight) → `explain.definition` (VOC) → `check.retrieval` (say-aloud). F24 `concept_map`: `map.node` / `map.link` → `check.retrieval`. F25 `viva_prep`: `viva.prompt` → think → `viva.model_answer` → `misconception.confront`. F26 `teacher_explainer`: `teach.move` per MIS, ANL non-mapping and diagnostic, addressed to a colleague.

---

## 5. Level register rules

Numeric limits are Level Profile fields (`max_sentence_words`, `max_new_terms_per_scene`, `max_new_ideas_per_segment`). The project holds no sentence-length number for any level, so all are Cal until O-17 and the pilots; Q-LEVEL is report-only until then (CE-35).

| Band (level id) | Sentence and vocabulary | Analogy policy | Humour ceiling | Personification | Rigour markers |
|---|---|---|---|---|---|
| Class 1–2 (`level/l1_2`) | Pre-reader; narration carries all meaning; icons and single words on screen; one language | Concrete only, ≤1 per objective [Recommendation] | Gentle delight; no irony, sarcasm or teasing; Cal (child-development) | Story frame only (§11) | None |
| Class 3–5 (`level/l3_5`) | Early reader; short phrases; real-life context [N11] (contested); one language (15 Oct 2026) | As l1_2; limit named in one child-level sentence | As l1_2 | As l1_2 | None |
| Class 6–8 (`level/l6_8`) | Sentences; standard notation introduced; abstraction [N53] | ≤1 per objective; non-mapping spoken | 03 ceiling pro-rata [Hypothesis] | Never causal | Discipline's form of understanding named |
| Class 9–10 (`level/l9_10`) | Board terminology plus glossary | 03 contract | 3–5 light moments, under ~25 s per ~10 min; zero acceptable (03 §5.2, Inh) | Never causal (03 §5.3) | Conditions stated with the law |
| Class 11–12 (`level/l11_12`) | Discipline register | Fewer expected | As l9_10 | As l9_10 | Assumptions, domains, derivation checks |
| UG (`level/ug`) | Disciplinary register; notation defined at first use | Only where it beats the formal statement | None inside derivations | None | `CLM.assumptions`, domains, notation, units |
| PG/Masters (`level/pg`) | Research register; citations on screen | Rare; attributed if borrowed | Zero by default [Recommendation] | None | Citations, stated uncertainty, method critique |
| Adult professional (`level/adult_prof`); exam overlays on any base level are a register, not a level | Base register plus Exam Strategist | Base level | Never about marks, ranks or failure | None | As-of pattern claims; past items cite paper and year |
| Vocational (`level/voc`) | One action per sentence [Recommendation]; trade glossary | Trade-relevant only | Never in a safety cue | None | Tool, check and safety step in order |
| Educator (`level/educator`) | Colleague register | Taught with their non-mapping | 03 ceiling | None | Diagnostic evidence [N73] |

**Humour pro-rata [Recommendation].** Below the 600 s reference the 25 s ceiling scales with duration, rounded down; formats under 120 s carry at most one light line, and only when the line is the concept itself (03 §5.1). Every line passes the "concept survives" test (03 §5.3) and never consumes a window.

---

## 6. Persona voice rules

All personas inherit the 03 core: warm toward the student, exacting about the science, playful about the problem; priority order correctness → independent capability → accessibility → warmth → humour; reveal instructional decisions; no fake sensing; no invented biography; conditional, action-based praise (03 Steps 1, 2, 9). A Level Profile may override register and expression lists, never these rules (R11).

Persona IDs and variants are owned by `VOICE_and_PERSONA_REGISTRY.md` §2.2 (five IDs; the nine architecture names are variants). The Script Spec records both `persona` and `persona_variant`; the EPP pins `persona@version#variant`. This table lists only what scripting adds.

| Persona id # variant | Levels | Register and moves | Added script-level retired expressions [Recommendation] |
|---|---|---|---|
| `persona/super-teacher-junior#junior` | l1_2, l3_5 | Warm, slow, call-and-response with real pauses, songs where the STY allows [N10]; "let's try together"; praise names a possible action conditionally ("If you counted five, you counted every one") | "good boy/good girl", "clever", "hurry", "fastest", "wrong!", "tell me your name", any request to comment, send or share |
| `persona/super-teacher-junior#coach` | l6_8 | Inquiry: "what would happen if…", predict-explain-check [N37] (contested), experiment framing; less performative than Junior, more Socratic than Super Teacher | "obviously", "as you all know" before new content |
| `persona/super-teacher#core` | l9_10 | The current 03 persona, unchanged | 03 list |
| `persona/super-teacher#mentor` | l11_12 | Exam-aware, deeper derivations, fewer hooks | "this will definitely come", any "trick" without its reason |
| `persona/lecturer#lecturer` | ug, adult_prof | Fewer interjections, explicit notation and definitions, head-in at transitions [N4], drawn derivations [N5] | Unexplained jargon; "trivially", "clearly" before a non-trivial step |
| `persona/lecturer#seminar-lead` | pg | Cites sources on screen, models critique, states uncertainty | Uncited "studies show"; a verdict on a contested claim |
| `persona/lecturer#colleague` | educator | Peer to a teacher | Claims about "your students" or any real class |
| `persona/skills-instructor#instructor` | voc | Procedural, safety-first, demonstration-led | "you can skip this", any phrasing that softens a safety step |
| Register overlay `persona/exam-coach#strategist` | overlay levels; never AC0 | Time management and elimination tactics, never tricks that bypass understanding | "toppers", "don't be left behind", "only N days left", "guaranteed" |

The 03 retired list (03 Step 2; 02 §H4) applies to every persona. **Delivery modes** are the 05 enum: the five 03 modes (`curious`, `steady`, `deliberate`, `light`, `reassuring`) plus `focused`; which persona may use which mode is set in the persona registry. The mode changes because the teaching task changes (03 Step 10). Q-PERSONA checks retired expressions and register: report-only first, then blocking (CE-35).

---

## 7. Locale and family constraints

### 7.1 Locale register

Locales change surface only: lexicon, script, register and voice, never node selection or claims (R9). Node text in another locale comes from REN nodes; new script wording in a locale is reviewed by the native subject editor at GA-Δ.

| Locale | Script and register | Code-switch boundary | Technical terms |
|---|---|---|---|
| `locale/en-in` | Latin; simple Indian English (03 Step 8) | n/a | Exam term after plain-language meaning |
| `locale/hinglish` | Latin (romanised Hindi, house transliteration table, CE-40). Hindi connective and orienting language; English technical terms | Switch only at a clause or phrase boundary. Never inside a term, a formula, a unit or a definition sentence; never mid-equation (03 Step 8). At a level whose pinned Level Profile has `single_language_per_lesson: true` (l1_2 by default), `locale/hinglish` is a Resolver R4 error unless the EPP pins a code-mix pattern approved by the child-development reviewer (15 Oct 2026; the schema blocks l1_2 + hinglish until such a pattern is approved through GR) | The family × locale glossary decides (GL-glossary). stem_fixture default: English terms and SI symbols |
| `locale/hi-in` | Devanagari (`hi-IN`). Register follows the Hindi-medium textbook | English terms in Latin script inside Devanagari text only where the glossary says so. At l1_2 and l3_5: Hindi-medium terms only unless a code-mix pattern is approved (Resolver R4; 15 Oct 2026) | Glossary decides between the Hindi-medium term (for example प्रतिरोध for resistance) and the English term; first use gives both [Recommendation; draft for native review] |
| `locale/as-in` | Bengali-Assamese script; Path A only until a TTS passes GL-voice (CE-L5) | One language per lesson at AC0 | Native editor review always |

Rules: rewrite, never translate line by line, and keep the same beat map (11 Step 7). Numbers, units and symbols are written in spoken form because TTS normalisation is on by default [11:N7]; `display_text` keeps the notation (RD-29). Code-mixed input is supported by at least one engine [11:P-S15]; Devanagari-with-Latin-terms versus romanised input is settled per engine by listening test [Hypothesis, 11 Step 7]. Each code-switched span records its `lang` for the cue sheet. `spans` is required when the locale is `locale/hinglish` or a `language_pair` is present; the concatenation of `spans[].text` must equal `spoken_text` (closure-check lint; added 15 Oct 2026).

Illustration (Hinglish, draft for native review): "Dekho, resistor same hai aur temperature bhi same. Voltage double kiya, toh current bhi double hua." Switches fall between clauses; the terms stay whole.

### 7.2 Family constraints

| Family | Statement rule | Required phrasing |
|---|---|---|
| `family/stem_fixture` | **Fixture-bound.** Every number, intermediate value and unit in speech or display equals a fixture output named by `fixture_ref`; significant figures preserved as decimal strings | Condition with the law ("for this resistor, at constant temperature"); assumption sentences map to `CLM.assumptions`; CS code on screen equals sandbox output |
| `family/quant_social` | Recomputed figures from fixtures; rates time-bound | "As of <as_of_date>, …"; normative statements as positions ("one view is…") |
| `family/humanities_citation` | **Citation-bound.** Every date, name, place, quantity, quotation and causal claim maps to a CLM with a source; `source.show` puts the citation on screen | Interpretations attributed; maps only with boundary review (CE-53); IKS and value education normative claims as "the curriculum states" |
| `family/languages_literature` | Quotations verbatim from TXT with edition; interpretations attributed | Language-learning scripts take a (medium, target) locale pair; target-language spans are tagged `lang`, never transliterated in `display_text`; pronunciation from the 05 lexicon |
| `family/arts_skills` | Technique steps from ACT/procedure claims; health-adjacent claims routed to health rules | Safety cue before physical steps |
| `family/vocational` | Procedure complete and in order (procedure_completeness) | Safety step spoken before the action it protects |
| `family/exam_strategy` | Pattern claims from official papers only | "Based on the <years> papers, …" for any trend; no "will come" |
| `family/health_medicine`, `family/law` | Not activated (O-9) | Disclaimer line; jurisdiction and as-of date spoken for legal rules |
| `family/evs_foundational` (added 15 Oct 2026, [Recommendation]) | Quantities from fixtures; factual statements cited from the board textbook; simplifications stated as simplifications (SIM) | Child-level phrasing from `level/l1_2` or `level/l3_5`; safety cue before any household activity; local examples carry a region tag |

**Quotations across locales (added 15 Oct 2026) [Recommendation].** In an edition whose language differs from a quotation's source, the quotation is spoken and displayed either (a) verbatim in its source language as a `lang`-tagged span (§7.1), with the edition on screen and the REN rendering shown as a labelled gloss ("meaning: …"), or (b) verbatim from a registered translated edition (its own SRC and TXT with `edition_source_id`), introduced as "in <translator or edition>'s translation". An ExamLeaf REN rendering is never spoken or shown as a quotation: without (a) or (b), the beat uses reported speech ("<author> wrote, in substance, that …") with role `assertive`, citing the quotation's CLM and its REN. Name and date tokens match the REN node field after the Locale Profile transliteration table and numeral policy (CE-40).

**Contested-claim phrasing (CE-29).** `settled`: plain statement. `attributed`: "According to <attribution>, …". `contested`: "Scholars differ. <A> argues …; <B> argues …." with no verdict and both sources on screen. `board_vs_scholarship`: "The syllabus states …", followed by the attributed scholarly position only if `board_position_decision.include_scholarly_position` is true. A Short may show a contested claim only with its attribution and may never state one side as fact. Time-bound claims always carry their as-of date in speech or on screen (Q-EXPIRY).

---

## 8. Question-analysis scripting

| Beat | Rule |
|---|---|
| `hook.question_reveal` | Shows the stem. A past item (`original: false`) shows board or exam, year and source paper on screen. An original item is labelled "Original practice question" and never shows marks (CE-31). |
| `check.predict` | The learner commits before any method appears. A simple choice uses a think window; solving uses pause-video. The question stays visible (F4). A predict prompt may not introduce a number that no node holds ("more or less than one ampere?" fails closure unless an ASM carries it). |
| `explain.definition` | "What is asked": givens, unknown, required form of the answer. |
| `misconception.confront` (≤2) | **Common-error beats** come from `WRK.steps[].common_error_mis_ids` and `ASM.misconception_ids`, never from the author's guess. The wrong move is named; a wrong numerical result is spoken only if a fixture computes it. |
| `worked.step` | Every step; every value from the fixture. |
| `marking.scheme` | Rendered only when `exam_tags.marks` and `marks_source ∈ {source_paper, official_key}` exist. ~~Sentences paraphrase spans of the registered key, with locator ("The official key gives <marks> marks for <element>").~~ Sentences are the K template "The official key gives <marks> marks for <span>", where <span> quotes the registered key span verbatim, with locator (corrected 15 Oct 2026: a no-model fill cannot paraphrase). Step marks come only from `exam_tags.marking_scheme[]` key spans; an invented split is never written (15 Oct 2026). No "examiners expect", "examiners hate" or generic advice without a source span. Otherwise the slot is skipped and the compiler logs why. |
| `recap.retrieval` | The transferable rule as a fresh question, answer hidden. |

**Timing.** Exam time advice ("about N minutes for this item") is allowed only as fixture arithmetic over an exam_pattern claim (marks and time limit from the official pattern). It is never invented and never shown as a countdown.

---

## 9. Shorts hook scripting

A Short is one complete learning unit, recomposed from nodes and never cropped (F5; 07/05 principles 1–3).

- **Hook in 0–3 s** (07/05 SH2, SH5): a question (`short.misconception`), a contradiction (`short.concept`, `hook.surprise`) or an unfinished task (`short.trap`, `hook.question_reveal`). The hook maps to an MIS, ASM or CLM like any sentence.
- **Forbidden hooks:** invented statistics ("90% of students get this wrong"), fear, urgency, guaranteed marks, "you won't believe", a promise the payoff does not keep, trend audio at AC0.
- **A Short that asks gets the window or does not ask** (11 Step 1, RD-11); default 6 s.
- **The payoff is complete**; nothing is withheld (07/05 principle 3).
- **Close:** at most one learning next step at AC1/AC2 ("Try it on the next circuit diagram in your textbook"); none at AC0. The script never names a product or destination; the platform attaches any link (CE-L1). For `concept_short_60` the spoken close is two sentences (PD-14): the request's `cta_line` (default `Try the free lesson on <topic>.`; none at AC0), then exactly `Professor Diki Simplified.`; a disclosure is never spoken or shown (PD-02, PD-20).
- **New wording is new script** and goes through GA-Δ (13 §5.7; 07/05 SH4).

---

## 10. Series and course continuity

- **Recaps of prior episodes (`bridge.return_link`)** use only the key CLM IDs of an approved, released member and pin its artefact hash; if the member goes stale or is revoked, so does the bridge (Architecture §3.6).
- **Open loops** are genuine questions that the next member answers (an ASM or OBJ of that member). An episode never withholds its own essential answer (02 §I1). AC0 loops are gentle, with no cliffhanger or "don't miss" language.
- **Paper Walkthrough** bridges name paper, board or exam and year from the source record; **Chapter One-Shot** uses `chapter.title` and chapters ≤360 s.
- Bridges are Path B (A for AC0); the first member of a series is Path A by R1.

---

## 11. Kids' story, song and read-along scripts (Class 1–5, `safety/ac0`)

1. Teaching beats carry an approved CLM or a SIM permitted at the level; frame beats ("This is Tiku the torch") assert nothing about the world.
2. **Personification** is a frame only: a character may talk, but causes are stated physically from the SIM or CLM; no character "wants" a scientific outcome (03 §5.3).
3. **Call-and-response** uses real windows; prompts invite saying, pointing, moving, drawing or singing [N10], with "or just think it" as an alternative. No character answers before the window ends.
4. No data solicitation, names, schools, photos, brands, links, QR codes, calls to action, urgency, fear, comparison or streak language (CE-19). No "wrong"; feedback is conditional and names an action.
5. Songs are verbatim from `STY.song_chant` with licence (CE-54, O-7); music is muted under teaching except the song itself.
6. A physical action needs an ACT node with `household_safe: true` and the grown-up cue.
7. **Read-along (F23):** TXT verbatim with synchronised highlight; VOC meanings from definition claims; 05 lexicon; native editor at GA-Δ; Path A for Indic languages.
8. Child-variant disclosure, pending counsel (O-5, CE-55). Close is `calm_end` or a song repeat.

---

## 12. Lecture, derivation and proof scripts (Class 11–12, UG, PG)

- **Derivation step grammar:** state the current line → name the operation ("divide both sides by R", 02 §E5) → justify with a CLM or fixture → call out the assumption (`CLM.assumptions`) → keep the previous line visible.
- `check.predict` before the final step; the result is hidden until the window ends.
- **Notation** is defined at first use (VOC); a symbol never changes meaning within an artefact.
- **Rigour markers:** domains and excluded cases ("for real x, √x² is |x|", 07/03 S7 maths rule), units, approximations named as such.
- **Seminar Lead (pg):** citations on screen (`source.show`), uncertainty stated, a critique prompt per chapter ("Which assumption would fail first in a real conductor?"), mapped to an ASM.
- **Lecture Segment (16:9):** `chapter.title` and `check.interpolated` each chapter, ≤360 s [N3][N31]; requires the 16:9 safe-zone tokens (O-19).
- Humour: none during a derivation (07/03 S5 rule 8).

---

## 13. Beat direction tag grammar

Tags are ExamLeaf metadata, never TTS syntax (03 Step 10). They live in structured fields; the header is their readable form for recording sheets and reviews, unifying the 11 Step 1 header, the 03 tags and the 05 segment fields.

```ebnf
header    = "[BEAT " beat_id { " | " field } "]" ;
field     = "ch: " int | "slot: " slot_id | "mode: " mode | "wpm: " band
          | "pause-after: " pause | "emphasis: " quoted { ", " quoted }
          | "cues: " cue { ", " cue } | "answers-after: " beat_id
          | "nodes: " node_id { ", " node_id } | "fixtures: " fixture_ref { ", " fixture_ref }
          | "itx: " interaction_id
          | "lang: " bcp47 | "sting: " ( "yes" | "no" ) ;
mode      = "curious" | "steady" | "deliberate" | "light" | "reassuring" | "focused" ;
band      = "ordinary" | "dense" | "recap" | "teacher_set" ;
pause     = "none" | "beat " seconds | "think " seconds | "pause-video" ;
cue       = cue_id "@" ( "show" | "highlight" | "transform" | "hide" | "reveal-answer" ) ;
```

| Tag | Maps to (05 §7.2 segment) | Rule |
|---|---|---|
| `mode` | `direction.mode` | The 03 modes plus `focused` |
| `wpm` band | `direction.wpm_band` (the EPP resolves `target_wpm`) | Specs and scripts name bands, never numbers (CE-16) |
| `pause-after: beat s` | `pause_after {kind: beat}` | 0.3–1.5 s phrase or contrast pauses; 2–4 s inspection holds (02 §G3). The old 11 "1.5 s THINK" emphasis hold migrates here |
| `pause-after: think s` | `pause_after {kind: think, prompt}` | Protected window: 5–8 s, default 6, 4 s only for a binary choice (RD-11). Below 4 s fails lint |
| `pause-after: pause-video` | `pause_after {kind: pause-video, prompt}` | Learner-controlled; narration stops (03 Step 7) |
| `emphasis` | `direction.emphasis` | Each phrase must occur verbatim in `spoken_text` |
| `cues` | `cues[]` (`cue_id`, `phrase`, `occurrence`, `edge`, `action`, `element_id`) | `reveal-answer` cannot fire before the window of the beat named by `answers-after` ends |
| `answers-after` | `answers_after` | Must reference an earlier beat that ends in think or pause-video with seconds > 0 (05 §7.2) |
| `fixtures` | `sentences[].fixture_refs` | Fixture cases (`FIX-…#case`) never go in `nodes` (added 15 Oct 2026) |
| `sting` | cue-sheet `sfx` | Sonic logo and transition stings only; muted under teaching (11 correction 7) |

03 migration: `[CURIOUS]` → `mode: curious`; `[BEAT:0.35]` → `beat 0.35`; `[THINK:6]` → `think 6`; `[PAUSE_VIDEO]` → `pause-video`; `[REVEAL:x]` → `x@reveal-answer`. Break tags cap at 3 s where supported [11:N1] and Eleven v3/v4 support none [11:N2], so protected windows are room tone inserted in the edit (11 Step 8).

---

## 14. Sentence-to-node traceability and the closure check

Every sentence record carries `sentence_id`, `role`, `spoken_text`, optional `display_text`, `node_ids[]`, `tokens[]` and the `assertive` mark (true unless a deterministic Kit template marks the sentence non-assertive with `non_assertive_template_id`; corrected 15 Oct 2026).

| Role | Node requirement |
|---|---|
| `assertive`, `exam_language`, `citation` | ≥1 CLM, SIM, WRK step or ASM allowed for the slot |
| `analogy` | The ANL node; a `non_mapping` sentence must exist in the same beat |
| `misconception_statement` | The MIS node; a later `misconception.confront` for the same MIS must exist |
| `question_prompt` | An ASM (or the WRK step for a predict); the answer may not appear before the window |
| `feedback` | ASM.feedback, ASM.hint or the MIS it repairs |
| `humour` | The node it illuminates |
| `story_frame` | ~~None, and only inside a `story.beat` whose `carries` is empty~~ The STY beat it renders (`STY-…#n`), only inside a `story.beat` whose `carries` is empty; a model-authored frame sentence counts as assertive (Q-CLOSURE) and passes closure against that STY beat; zero nodes only for Kit template output (corrected 15 Oct 2026) |
| `instruction`, `transition`, `rhetorical`, `call_response` | ~~None, but only if the flagger marks them non-assertive and they contain no number, date, name or unit~~ None only when the sentence is emitted verbatim by a registered deterministic Kit template (rung K) that marks it non-assertive (`non_assertive_template_id`) and it contains no number, date, name or unit. A model-authored sentence counts as assertive whatever its role (QA_PROFILES Q-CLOSURE): it cites ≥1 node allowed for its slot (§3), and every token matches. The flagger may only add assertive marks (corrected 15 Oct 2026) |
| `disclosure` | The voice registry entry |

**Schema enforcement (added 15 Oct 2026).** `script_spec.schema.json` checks the node type per role: `assertive`, `exam_language` and `citation` cite ≥1 CLM, SIM, ASM or WRK step (`WRK-…#n`); `analogy` an ANL; `misconception_statement` an MIS; `question_prompt` an ASM or WRK step; `feedback` an ASM or MIS; an assertive `story_frame` an STY beat; `assertive: false` requires `non_assertive_template_id`; a `submitted` Script Spec has `closure.status: pass`. Slot permission (§3) stays with `closure-check`.

**Tokens.** Every number, date, name, unit and symbol is extracted as a token and must match a field of a referenced node or a fixture output, after NFC and the locale's spoken-math normalisation ("zero point four amperes" ↔ fixture "0.4 A").

**Closure algorithm.** ~~The claim flagger [N43] marks assertive sentences and only adds flags (CE-28)~~ Every sentence counts as assertive unless a deterministic Kit template marks it non-assertive; the claim flagger [N43] may only add flags, never remove one (CE-28; Q-CLOSURE; corrected 15 Oct 2026); each assertive sentence maps to an allowed node in the Format Plan; each token matches; derived formats introduce no node types; every elicited MIS is confronted; every cited claim's conditions are present and no revision drops one (SQ-20). The report lists totals, unmapped sentence IDs and unmatched tokens; any failure fails Q-CLOSURE, blocking from day one.

---

## 15. Script QA checks

Feeds names the parent Q-check and sub-check in `QA_PROFILES_REGISTRY.md`; the QA profile is authoritative for severity.

| ID | Check | Feeds | Blocking? |
|---|---|---|---|
| SQ-01 | Closure: assertive sentences mapped, tokens matched | Q-CLOSURE, Q-CLOSURE.literals | Yes |
| SQ-02 | Spoken and on-screen numbers equal fixture outputs | Q-FIX | Yes |
| SQ-03 | Schema; no `[ ] < >` in `spoken_text` | Q-SCHEMA | Yes |
| SQ-04 | Answer hidden in narration, display, captions, overlays, thumbnail and preview until the window ends; `answers_after` valid | Q-INT.answer_hidden, Q-INT.reveal_order | Yes |
| SQ-05 | No fake sensing ("I heard you", "you got it", "you have mastered"; unconditional praise) | Q-PERSONA.fake_sensing | Yes for the 03/07 phrase list (03 Step 16 blocks deceptive personal responses); report-only for new patterns |
| SQ-06 | No fake enthusiasm: retired expressions, unconditional celebration, `light` on feedback, one non-steady mode on every beat | Q-PERSONA.fake_enthusiasm, Q-PERSONA.forbidden | Report-only, then blocking |
| SQ-07 | Register: sentence length, new terms per scene, density | Q-LEVEL.reading, Q-PERSONA.register | Report-only until the pilot (CE-35) |
| SQ-08 | Reading level against controlled vocabulary per level × locale | Q-LEVEL.reading | Report-only until O-17 |
| SQ-09 | Forbidden phrases: pressure, fear, comparison, guaranteed marks, data solicitation, AC0 calls to action, predictive exam claims | Q-SAFE | Yes |
| SQ-10 | Analogy non-mapping and formal return spoken; ANL permitted | Q-CLOSURE.sim_anl | Yes |
| SQ-11 | Every SIM listed with `what_is_lost`; no improvised simplification | Q-CLOSURE.sim_anl | Yes |
| SQ-12 | Disclosure matches the EPP voice path (A converted, A direct, B, or mixed for a single-file F16 with `voice_path_by_chapter`) and locale; child variant at AC0 (RD-45; corrected 15 Oct 2026) | Q-DISC | Yes |
| SQ-13 | Contested and time-bound phrasing (§7.2) | Q-LEDGER, Q-EXPIRY | Yes |
| SQ-14 | Marks only from source paper or official key | Q-CLOSURE | Yes |
| SQ-15 | Humour ceiling; none inside a window or derivation | Q-PERSONA | Report-only |
| SQ-16 | Word budget against measured audio | pacing-controller | Report-only |
| SQ-17 | Emphasis and critical phrases occur verbatim | narration validator | Yes |
| SQ-18 | Recent-script ledger (about 20 scripts, 03 Step 14) | script-evaluator | Report-only |
| SQ-19 | Path A ASR diff against the approved script; any change returns to GA-Δ (11 Step 3) | `qa.transcript_check` | Yes |
| SQ-20 | Condition preservation (added 15 Oct 2026): (a) every `CLM.assumptions` entry of each CLM cited by an `assertive` or `exam_language` sentence is spoken or displayed in the same beat or an earlier beat of the same chapter, recorded as a `term` token with `node_id` = that CLM and `field` = `assumptions[i]`; (b) a review or repair fill may not remove, relative to the fill it revises, a negation, a direction word (increase/decrease, more/less), a sign, an exponent or any token matched to `CLM.assumptions` (07/03 S5 naturalizer invariant) | Q-CLOSURE.conditions | Yes |
| SQ-21 | Every fill's `model_profile_ref` is in the EPP pins; no ultracode; effort max only with a ledger justification (`max_justification_ref`) (added 15 Oct 2026) | A17a | Yes |
| SQ-22 | [Recommendation] Condition and relationship glyph present (added 16 Oct 2026): every `CLM.assumptions` entry and every relationship or equation an `assertive` sentence states has a fixture display string (`display.conditions.*` or the equation's fixture field) bound in the scene, revealed on its anchor word (cue `at` in `[t0 − 0.05, t0]`), and shown again in the `recap.statement` visual. Extends SQ-20 from "spoken" to "shown". Evidence: pilot physics/haiku spoke "constant temperature" and "voltage equals current multiplied by resistance" and never showed either; pedagogy 14 vs 19 (`16_pilot_builds_2026-10-16/judging/physics/verdict_pedagogy.json`); Kit R-002, detector PK-D02 (proposed) | Q-CLOSURE.conditions (proposed sub-check `.shown`) | Report-only until PK-D02 is calibrated on the pilot frames, then Yes |
| SQ-23 | [Recommendation] Confront answers the predict and shows evidence (added 16 Oct 2026): in `concept_intro`, the `misconception.confront` beat's first sentence answers the open half of the `check.predict` prompt, and its scene shows the counter-example in the same setup as the worked/compare scene with at least one fixture-bound change glyph revealed on the causal word and the struck shortcut. Evidence: pilot physics/haiku asserted "Ohm's law is always true" over a bare bulb with no circuit (blocking in both lenses); physics/opus "But always is not safe" with the lamp in the same loop, "R ↑" and a struck ×2 (`16_pilot_builds_2026-10-16/judging/physics/verdict_*.json`); Kit R-003, detector PK-D05 (proposed) | Q-INT.reveal_order; Q-CLOSURE (MIS confronted) | Report-only until PK-D05 exists, then Yes |
| SQ-24 | [Recommendation] Worked step recounts after each change (added 16 Oct 2026): every `worked.step` changes one coefficient or quantity per sentence, names the element that moves, and is followed in the same beat by a spoken and on-screen recount bound to a named fixture intermediate state (`results.<state>`, e.g. `step1`); no sentence announces the final answer without the recount. Evidence: pilot chemistry/haiku "Put a two in front of hydrogen and a two in front of water" with no recount and a stale tally (blocking in both lenses); chemistry/opus recounted from `step1` to "Four and four. Balanced."; pedagogy 13 vs 19 (`16_pilot_builds_2026-10-16/judging/chemistry/verdict_pedagogy.json`); Kit R-004, detector PK-D06 (proposed) | Q-FIX (proposed sub-check `.states`) | Report-only until PK-D06 exists, then Yes |

---

## 16. The scripting cascade

Kit first, model second (CE-L6). Each slot type has one Kit template; fills cascade per beat: **Kit slot-fill → Haiku → Sonnet review → Opus escalation → human ticket** (13 §5.3). Every fill records `model_profile_ref` (a pinned ModelProfile, never a bare alias; corrected 15 Oct 2026), `effort`, `kit_version`, `cascade_rung` and output hash.

**Current constraint.** Until the T0–T3 text arms pass for a Kit cell, model-authored script text stays on today's mix: Sonnet authors, Opus reviews, Haiku routes (13 §5.6, D-8). The entry rungs below apply per Kit cell only after its arm passes. No cheap-model cascade runs until the `kit_cascade` task family (D-16) exists in the effort governor (13 §5.8; added 15 Oct 2026).

| Entry rung | Slots | Review |
|---|---|---|
| **K: Kit deterministic fill** (no model) | `chapter.title`, ~~`recap.statement` (verbatim CLM/SIM/REN)~~ `recap.statement` (template: when the beat has `answers_after`, the bound ASM's `expected_answer` in spoken form; then each key CLM or permitted SIM statement verbatim or its REN, after the locale's exam-form lead-in string at l9_10+; corrected 15 Oct 2026), `card.back`, `marking.scheme` (key spans, §8 template), `exam.pattern` (pattern table), `source.show`, `source.read`, `story.song_chant`, `map.node`, `map.link`, `qa.doubt_statement`, the disclosure line | Validators only |
| **H: Haiku author** | `hook.question_reveal`, `check.*`, `card.front`, `recap.retrieval`, `close.next_step`, `bridge.return_link`, `worked.step`, `activity.setup`, `activity.do`, `activity.observe`, `compare.dimension`, `exam.time_plan`, `viva.prompt` | Sonnet reviews every Haiku line |
| **S: Sonnet author** | `hook.realworld`, `hook.surprise`, `explain.ladder_step`, `explain.definition`, `explain.analogy`, `misconception.*`, `worked.faded_twin`, `qa.answer`, `activity.safety_cue`, `story.beat`, `source.interpret`, `viva.model_answer`, `teach.move` | Opus reviews |
| **O: Opus author** | `explain.derivation_step` (l11_12, ug, pg), `perspective.position`, any beat on a contested or sensitive claim | Human reviewer at GA-Δ |

**Escalation triggers** (any one, 13 §5.4): closure or fixture failure persisting after one repair; a refusal; `UNKNOWN` routing; caps exhausted; persona or safety lint failing twice [Recommendation]; a per-beat spend ceiling reached ($0.02 Haiku, $0.25 Sonnet, $0.60 Opus; 13 §5.4 [Recommendation]; added 15 Oct 2026). **Circuit breaker:** more than 20% of beats escalating past their entry rung stops the artefact; the rest run on Opus-low via the Kit and a Kit defect opens (13 §5.8, applied to beats). Repairs are append-only. Fable 5.1 and Opus 5.5 author Kit templates and exemplars offline, not per beat.

---

## 17. Negative tests

The correct response in every case is to keep the constraint, not to comply creatively (03 Step 14).

| # | Request or input | Required outcome |
|---|---|---|
| NT-01 | "Make it funnier by mocking students who get it wrong." | Line refused; humour stays concept-linked |
| NT-02 | "Say the electrons want to move to the positive terminal." | Rejected as causal personification |
| NT-03 | "Congratulate the viewer as though we heard their answer." | SQ-05 blocks; conditional feedback substituted |
| NT-04 | "Fit the Detailed explanation into a 60 s Short without dropping anything." | Compile error (R5 or incomplete unit); never sped up |
| NT-05 | A fill adds "about 70% of students make this mistake." | SQ-01: unmatched number |
| NT-06 | A Simplified fill paraphrases a claim with no permitted SIM. | SQ-11 fails |
| NT-07 | A Recap caption shows the answer during the think window. | SQ-04 blocks |
| NT-08 | Question Analysis on an original item shows "2 marks". | SQ-14 and schema fail (CE-31) |
| NT-09 | A Short states one side of a contested claim as fact. | SQ-13 blocks (CE-29) |
| NT-10 | An AC0 story ends "Comment your favourite colour below!" | SQ-09 blocks (CE-19) |
| NT-11 | An AC0 script says "open the torch and take out the cells." | Fails: action without an ACT node and grown-up cue |
| NT-12 | A Hinglish line switches language inside "I equals V over R". | Q-LOCALE flags; rewritten at a clause boundary |
| NT-13 | A Path B Short carries the Path A disclosure wording. | SQ-12 blocks (RD-45) |
| NT-14 | `[THINK:6]` inside `spoken_text`; or `think 2` on a prediction. | SQ-03 blocks; lint fails below the RD-11 floor |
| NT-15 | A Q&A Doubt opens "Riya from Jorhat asked us…". | SQ-09 blocks (CE-20) |
| NT-16 | "This question will definitely come this year." | SQ-09 blocks: predictive claim |
| NT-17 | A Path A teacher ad-libs a new example while recording. | SQ-19 fails; re-record or re-approve |
| NT-18 | A bridge recaps a revoked member; a PG line says "studies show" with no source node. | Release check refuses; SQ-01 fails |
| NT-19 | A review fill shortens "for an ohmic conductor at constant temperature, V equals I R" to "V equals I R". | SQ-20 blocks |

---

## 18. Worked example: one Ohm's-law objective, six scripts

Illustrative graph `LG-phy10-ohm` (IDs are examples; fixture `FIX-ohm@1.0.0` must exist before compile, with the cases from the 02 blueprint, organiser table C). `OBJ-phy10-ohm-1`: calculate current for an ohmic conductor and state the condition. Key claims: `CLM-ohm-prop` (current ∝ potential difference for an ohmic conductor at constant temperature and other conditions) and `CLM-ohm-vir` (V = IR). Also `CLM-series-current` (same current through every series component) and `CLM-energy-transfer` (a bulb transfers electrical energy to light and heat). `MIS-used-up` (priority 1, diagnostic `ASM-diag-used-up`); `MIS-ivr-invert` ("current equals voltage times resistance"). `WRK-ohm-12v6` (→ 2 A) with twin `WRK-ohm-12v4` (→ 3 A); `ASM-ohm-9v6` (original; 1.5 A, then 0.75 A with R doubled) with worked solution `WRK-ohm-9v6` (fixture case `FIX-ohm#9v_6ohm`). `ANL-pipe-flow` (permitted l6_8, l9_10). `SIM-ohm-push` (permitted l6_8; lost: exact proportionality, the condition, V = IR). `SIM-ohm-junior` (permitted l3_5; lost: proportionality, resistance, units, and that a bulb is not a constant resistor, so the story avoids bulbs), carried by `STY-cells-push`.

**Detailed (`level/l9_10`, `persona/super-teacher#core`, en-in, Path A), Ch1**

```
[BEAT b02 | ch: 1 | slot: misconception.elicit | mode: steady | pause-after: beat 1.0 | nodes: MIS-used-up]
  "A tempting idea: the resistor uses up some current, so less comes out than goes in. Keep that idea; we will test it."
[BEAT b03 | ch: 1 | slot: explain.ladder_step | mode: deliberate | wpm: dense | pause-after: think 6 | emphasis: "the same resistor" | itx: II-d-01 | nodes: CON-ohm-r1, CLM-ohm-prop, ASM-ohm-predict-4v | fixtures: FIX-ohm#2v_10ohm]
  "Keep the same resistor at the same temperature. Two volts gives zero point two amperes. Now make it four volts. Predict the current."
[BEAT b04 | ch: 1 | slot: explain.ladder_step | answers-after: b03 | cues: i_reading@reveal-answer | nodes: CLM-ohm-prop | fixtures: FIX-ohm#4v_10ohm]
  "Zero point four amperes. Twice the voltage, twice the current: for this resistor, under these conditions."
```

**Recap (`level/l9_10`, Path B)**

```
[BEAT b01 | slot: recap.retrieval | mode: curious | wpm: recap | pause-after: think 6 | itx: II-r-01 | nodes: ASM-recap-double-r]
  "Same voltage, resistance doubled. What happens to the current?"
[BEAT b02 | slot: recap.statement | answers-after: b01 | nodes: ASM-recap-double-r, CLM-ohm-prop, CLM-ohm-vir]      K template output (corrected 15 Oct 2026)
  "It halves."                     (feedback: the expected_answer of ASM-recap-double-r, spoken form)
  "In the board answer:"           (transition: en-in exam-form lead-in string, non_assertive_template_id)
  "Current through an ohmic conductor is proportional to the potential difference across it, at constant temperature and other conditions. V equals I R."      (exam_language: the CLM-ohm-prop and CLM-ohm-vir statements verbatim, spoken form)
[BEAT b03 | slot: misconception.confront | mode: deliberate | nodes: MIS-used-up, CLM-series-current]
  "And current is not used up: the same current leaves the resistor as enters it."
```

**Question Analysis (`level/l9_10`, Path B)**

```
[BEAT b01 | slot: hook.question_reveal | nodes: ASM-ohm-9v6]          on screen: "Original practice question"
  "A six-ohm resistor is connected across nine volts. Find the current."
[BEAT b02 | slot: check.predict | pause-after: pause-video | itx: II-q-01 | nodes: ASM-ohm-9v6]
  "Pause and solve it. Write the relationship before you substitute, and include the unit."
[BEAT b03 | slot: misconception.confront | mode: deliberate | nodes: MIS-ivr-invert, CLM-ohm-vir]
  "The trap is multiplying voltage by resistance. V equals I R, so to find current we divide."
[BEAT b04 | slot: worked.step | answers-after: b02 | nodes: WRK-ohm-9v6#1 | fixtures: FIX-ohm#9v_6ohm]
  "I equals V over R: nine over six, one point five amperes."
-- marking.scheme skipped: ASM-ohm-9v6.original = true (CE-31) --
```

**Short (`level/l9_10`, `short.misconception`, about 35 s, Path B)**

```
[BEAT b01 | slot: misconception.elicit | mode: curious | pause-after: beat 0.8 | nodes: MIS-used-up]        hook ≤3 s
  "Does a bulb use up current?"
[BEAT b02 | slot: misconception.confront | mode: deliberate | nodes: CLM-series-current, CLM-energy-transfer]
  "No. In a series circuit the same current flows through every part. What the bulb transfers is energy, to light and heat."
[BEAT b03 | slot: check.retrieval | pause-after: think 6 | itx: II-s-01 | nodes: ASM-diag-used-up]
  "True or false: the current leaving the bulb equals the current entering it?"   → b04 (answers-after b03): "True."
```

**Simplified (`level/l6_8`, `persona/super-teacher-junior#coach`, Path B)**

```
[BEAT b01 | slot: hook.realworld | mode: curious | pause-after: think 6 | itx: II-p-01 | nodes: MED-circuit-1, ASM-predict-add-cell]
  "What would happen to the current if we added a second cell to this circuit?"
[BEAT b02 | slot: explain.ladder_step | answers-after: b01 | nodes: SIM-ohm-push]        derived surface: SIM-ohm-push
  "A bigger push from the cells makes more current flow through the same resistor."
[BEAT b03 | slot: explain.analogy | nodes: ANL-pipe-flow]
  "Think of a pump pushing water through a pipe: a stronger pump, more flow. Where the picture breaks: water can leak from a pipe, but charge is not used up in a circuit."
```

**Story (`level/l3_5`, `persona/super-teacher-junior#junior`, Path A, `safety/ac0`, one language)**

```
[BEAT b01 | slot: story.beat | wpm: teacher_set | nodes: STY-cells-push#1]          story_frame (carries none)
  "This is Tiku the torch. Tiku has one cell inside."
[BEAT b02 | slot: story.beat | nodes: STY-cells-push#2, SIM-ohm-junior]
  "One cell gives a small push. A little electricity flows through Tiku's wire."
[BEAT b03 | slot: check.retrieval | mode: curious | pause-after: think <Cal, floor 6> | itx: II-k-01 | nodes: ASM-k-more-cells]
  "What do you think happens with two cells? Say it out loud, or just think it."
[BEAT b04 | slot: story.beat | answers-after: b03 | nodes: STY-cells-push#3, SIM-ohm-junior, ASM-k-more-cells]
  "Two cells give a bigger push, and more electricity flows. If you said a bigger push, you are thinking like a scientist."
```

**What the example exposes.** (1) The Story and the Simplified compile only if the request's competency GUID resolves to an objective at that level (a precursor OBJ linked by `requires`, or a Curriculum Graph crosswalk) and SIM nodes permitted at that level exist; otherwise the Resolver refuses, correctly, because Simplified is "the same level, a lower entry point" (F2). (2) The Short's energy sentence needs `CLM-energy-transfer`; without it SQ-01 fails. (3) The Question Analysis predict beat cannot ask "more or less than one ampere?", because no node holds "one ampere".
