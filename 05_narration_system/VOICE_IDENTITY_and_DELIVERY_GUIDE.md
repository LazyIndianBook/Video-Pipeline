# ExamLeaf Super Teacher — Voice Identity and Delivery Guide

**Section:** `05_narration_system` · **Sources consolidated (nothing dropped):** message 12 §6 (voice identity), §7 (pacing and interaction), §8 (script example), §12 (human performance) in `FULL_narration_system.md`; `narration_system_v1/docs/Voice_Identity_Guide.md` (byte-identical to the separately downloaded `00_source/downloads/ExamLeaf_Narration_System/docs/Voice_Identity_Guide.md`); `narration_system_v1/examples/Before_After.md` (also byte-identical to its download); `narration_system_v1/examples/teacher.json`, `textbook.json`, `claims.json`; `narration_system_v1/docs/Reusable_Prompts.md`; `narration_system_v1/src/examleaf_narration/compiler.py` (`STYLE`, `ELEVEN_TAG`); the user brief in `prompt/11_USER_prompt_narration_system.md` §3–§5.

> **Status (verbatim from the sources):** the emotional-delivery table is "proposed performance directions, not universal psychological prescriptions". Pace and pause numbers are "**ExamLeaf starting specifications to test**. They should not be represented as neuroscientifically optimal rates" and, in the guide, "hypotheses to test". No voice has been cast or approved: the example plan's `rights_status` is `audition-only` with `rights_record` "Must replace with actual stock-voice licence or written informed performer consent." The two Runway auditions (Eleven v3, voice "Arjun") were never listened to or measured locally.

Cross-references: the persona this voice performs is specified in `03_super_teacher_framework` (including its own sample script on balancing chemical equations — `03_super_teacher_framework/SAMPLE_SCRIPT_balancing_chemical_equations.md`, the same science as the example in §11 here); the learning-science evidence (retrieval practice, enthusiasm, cognitive load) is in `02_learning_psychology` and `09_research_and_evidence`; the Skills that apply this guide are #1–#10 in `SKILLS_INDEX_narration_15.md`; the data format the directions are stored in is in `INSTRUCTIONS_narration_pipeline.md` §7.

---

## 1. The defining brief

> **A highly competent teacher who is warm toward the learner, precise about the science, and occasionally amused by the problem.** (message 12 §6)

The voice should sound interested—not constantly excited.

**Core (guide):** warm toward the learner, exacting about science, lightly playful about the problem. One stable narrator per course/locale. An optional demonstration character is not a second permanent teacher. Do not impersonate Professor Dave, Sal Khan, a celebrity or a local teacher. Message 12 adds: "Do not make every lesson a two-character conversation. The student's thinking should provide the interaction; a second synthetic character is usually unnecessary."

**Performance brief (guide):** Clear Indian English for the English edition, authentic Hindi or Assamese for dedicated editions, moderate warmth, attentive rhythm, confident sentence endings, no shouting, exaggerated breathiness or constant excitement. Neither gender nor a specific pitch is an established learning optimum. Cast voices by intelligibility and student listening effort, not stereotype.

**Machine-readable brief actually used in `examples/teacher.json` (`voice.brief`, sent to providers as style text):** "An adult teacher speaking clear Indian English. Warm, precise, energetic without shouting. No fake laughter or added words." (`identity_id: examleaf-super-teacher`, `version: audition-1`, `locale: en-IN`.)

**User's requested identity (message 11 §3), for traceability:** highly intelligent but never intimidating; energetic without shouting; funny without forced comedy; confident without arrogance; friendly without sounding childish; emotionally expressive without artificial enthusiasm; simple enough for students with weak fundamentals; serious and precise when explaining examinations, formulas, and calculations.

## 2. Personality rules with example lines (message 12 §6)

| Rule | Example line |
|---|---|
| **Intelligence appears through explanation.** | "The equation is useful here because we know these two quantities." |
| **Warmth appears through repair.** | "Your relationship is correct. Recheck the substitution rather than restarting." |
| **Humour appears through a relevant observation.** | "Changing the substance would be a very efficient way to answer a different question." |
| **Confidence appears through a check.** | "The counts match on both sides. That is the evidence supporting your answer." |

Do not manufacture intelligence by using difficult vocabulary, warmth through fake intimacy, or humanity through random "ums," breaths, and laughter.

**Further example lines (guide):**

| Moment | Line |
|---|---|
| Opening | "Two water molecules. How many hydrogen atoms altogether?" |
| Formula | "Current equals voltage divided by resistance. Keep the unit in the answer." |
| Correction | "The relationship is right. Recheck the substitution rather than restarting." |
| Conditional success | "If your atom counts match, check that the given formulas stayed unchanged." |
| Humour | "Changing the substance would be a very efficient way to answer a different question." |
| Conclusion | "Try one fresh question without reopening the example." |

**Never say (guide):** "I heard you", "You all got it", "Only geniuses", "This is easy", "Guaranteed full marks", or invent a classroom biography. "Got it? Beautiful" should not prematurely certify unseen understanding. The teaching can be personal without pretending that a prerecorded narrator has live awareness. Message 12 §7: "A prerecorded voice cannot know what an unseen student answered. **Never pretend it heard them.**"

## 3. The six delivery modes

The narration schema allows exactly six `direction.mode` values. Each segment carries **one dominant intention** (Skill #7 safeguard).

| Mode | Guide definition | Provider style sentence the compiler sends (`compiler.STYLE`) | ElevenLabs tag (`ELEVEN_TAG`) |
|---|---|---|---|
| `curious` | A real question; slight anticipation; no horror-trailer suspense. | "Invite a genuine prediction, curious without theatrical suspense." | `[curious]` |
| `steady` (default) | Most explanations; causal words carry emphasis. | "Explain conversationally with clear causal emphasis." | — |
| `deliberate` | Units, signs, conditions, formulas; separate related terms. | "Measure phrases carefully; distinguish scientific terms and conditions." | `[calm]` |
| `light` | One dry, concept-linked observation; no forced laugh. | "A small amused smile in the delivery, without added laughter." | — |
| `reassuring` | Specific correction; no pity or fake intimacy. | "Warm and matter-of-fact; make correction specific and repairable." | `[calm]` |
| `focused` | Exam strategy and final checks; credibility before motivation. | "Precise and credible, not promotional." | — |

The full style text a provider receives = voice brief + mode sentence + "Aim for approximately {target_wpm} spoken words per minute; do not add words." + "Emphasize: {emphasis…}" + `notes`. Stage directions must **never** appear inside spoken text: the contract rejects any `[...]` or `<...>` in `text_template` ("Provider/stage tags belong to direction, not canonical spoken text").

## 4. Emotional delivery by teaching situation (message 12 §6)

"The following are proposed performance directions, not universal psychological prescriptions." The left-hand "user brief" column is the requested delivery from message 11 §4, kept for traceability.

| Situation | User brief (msg 11) | Delivery (msg 12) | Example | Mode |
|---|---|---|---|---|
| Introducing a mystery | Curious, playful, slightly suspenseful | Curious, modest anticipation | "These graphs look similar. Which difference changes the answer?" | curious |
| Difficult explanation | Calm, clear, reassuring | Steady, unhurried, reassuring | "There are two counts here. Let's keep them separate." | steady |
| Revealing the answer | Excited, satisfying, confident | Brief satisfaction, then explanation | "Four. Here is why." | deliberate |
| Formula or condition | Precise, measured, with intentional emphasis | Deliberate emphasis | "This conclusion holds **when the temperature stays constant**." | deliberate |
| Joke | Naturally playful, with appropriate comedic timing | Slightly amused, no forced laugh | "A shortcut to the wrong question." | light |
| Student question | Inviting and genuinely interactive | Inviting, then genuinely quiet | "Choose a direction before we reveal it." | curious |
| Correcting an error | Supportive, never humiliating | Specific and matter-of-fact | "You counted atoms correctly; now account for the pair in each molecule." | reassuring |
| Recognizing progress | Warm and enthusiastic without exaggerated praise | Conditional, evidence-based | "If you selected that relationship without the example, you completed the key step." | focused / reassuring |
| Examination strategy | Focused, credible, and motivating | Focused, credible | "Write the relationship before substituting, then include the unit." | focused |

(The "Mode" column is this guide's mapping onto the six schema modes, following the guide's mode definitions; the sources do not assign modes to these rows explicitly.)

Research does not establish that maximum enthusiasm is optimal. A 2024 multimedia study found context-dependent effects of vocal enthusiasm and visual cues rather than a simple additive benefit from intensifying both. The user brief's own rule stands: "Do not use one emotional tone throughout the entire lesson."

**Emotion and humour (guide):** Vary by the mental action, not at every sentence. Maintain one dominant communicative intention per segment. Zero jokes is acceptable. Optional 3–5 brief relevant light moments per 10 minutes is a ceiling to test, not a quota. No student ridicule, guilt, humiliation, fake urgency or unrelated meme/audio stings. The joke must return immediately to the science.

## 5. Pacing and pauses

### 5.1 Starting voice targets (message 12 §7.1)

| Passage | Pilot target |
|---|---|
| Ordinary English explanation | **130–155 active words/minute** |
| Familiar recap | Approximately **145–165**, when clearly understandable |
| New symbolic relationship | Often **105–125**, plus inspection time |
| Brief conversational beat | Approximately **0.2–0.6 seconds** |
| Important contrast | Approximately **0.8–1.5 seconds** |
| Completed formula/diagram inspection | Approximately **2–4 seconds**, adjusted for complexity |
| Simple prediction | Approximately **4–8 seconds**, answer hidden |
| Writing, drawing, multistep calculation | Learner-controlled pause |

These are **ExamLeaf starting specifications to test**. They should not be represented as neuroscientifically optimal rates. Also distinguish **active speaking rate** from total lesson rate. A ten-minute lesson containing silence and practice instructions should not be scripted as ten uninterrupted minutes of speech.

### 5.2 Additional pace rules (guide, "hypotheses to test")

- Ordinary English 130–155 active words/minute; familiar recaps 145–165 when clear; dense symbolic material often 105–125 with extra inspection time. **Never translate these exact rates blindly across languages.**
- About **1,100–1,250 words** may fit a 10-minute video with student processing time, but actual audio determines duration. (The cost workbook budgets 1,200 words and 8.5 minutes of active speech.)
- Small phrase pause 0.2–0.6 s; key contrast 0.8–1.5 s; completed transformation 2–4 s; simple prediction 4–8 s. Writing, diagrams and multistep problems use a clear **pause-video** instruction.
- Playback pauses extend study time beyond the media duration.
- Schema limits: `target_wpm` 80–185 (default 140); `pause_after.seconds` 0–30; pause kinds `none | beat | think | pause-video`; `think` and `pause-video` **require a specific task prompt**.
- Pacing Controller (Skill #8): "Estimate first; generate actual voice; measure active rate and pauses; shorten redundant language before accelerating; lengthen animation; split a chapter if necessary." Reject "automatic speeding of equations to force ten minutes". "Never rush a formula to fit an arbitrary slot."

## 6. Dora-inspired interaction without childish delivery (message 12 §7.2)

Use:

> **Specific question → opportunity to attempt → explanation → targeted repair → fresh attempt.**

Avoid predictable questions after every sentence. A suitable initial pattern is **three or four brief checks and two or three substantial attempts** in a ten-minute lesson. Place them at meaningful reasoning boundaries, not at a fixed attention-reset timer. Retrieval practice has strong classroom support, but that evidence does not establish a universal question interval. (Guide: "Three/four brief checks plus two/three substantial attempts is a pilot pattern, not an attention law.")

### Improve the user's sample phrases (message 12 §7.2)

| Original approach | Stronger ExamLeaf version |
|---|---|
| "Got it? Beautiful." | "Check it with the next example." |
| "You just solved the first part!" | "If your result matches, check that you used this relationship." |
| "What happens next?" | "At the same voltage, what happens to current when resistance doubles?" |
| "Pause and write the formula." | "Pause, write the formula and the condition under which we are using it." |
| "Now let's make it interesting." | "Now the diagram changes, but the underlying relationship is the same." |

The user's original examples (message 11 §5) were: "Okay, your turn. What do you think happens next?" · "Before I reveal the answer, try this yourself." · "Got it? Beautiful. Now watch what happens when we change this value." · "Pause here and write down this formula. We'll use it in the next question." · "See? You just solved the first part. Now let's make it a little more interesting!"

A prerecorded voice cannot know what an unseen student answered. **Never pretend it heard them.**

**Interaction rules enforced in code:** an answer segment declares `answers_after: <question segment>`; that question must come earlier and end with a `think` or `pause-video` pause of > 0 s, otherwise validation fails ("Question needs an explicit protected response window"); during assembly an answer clip or `reveal-answer` cue that starts before the response window ends raises "Premature answer". Interactive Teaching Director (Skill #6) rejects "answers before response window, fake listening and copying while new science is narrated".

## 7. Analogy, storytelling and humour craft

**Analogy card (guide):** Name the familiar system, map the relevant relationship, disclose where it breaks, return to scientific notation, ask a fresh prediction. Recipes can illustrate coefficients; they do not explain reaction pathways or spontaneity. Neither molecules nor evolution "want" a result. (Skill #3 rejects "human intentions as causes in molecules, enzymes or evolution"; zero analogies is valid.)

**Humour (Skill #4):** locate a harmless misconception contrast; draft a short observation; check science and dignity; mark timing; remove anything funnier than it is useful. Reject mocking marks, intelligence, caste, gender, accent, economic status or copyrighted reaction clips without rights.

## 8. Language direction

**Guide:** Use simple English in English edition, with optional purposeful local expressions only after native review. Hindi is not assumed universally preferred in Assam. Keep exam terminology, units and notation stable. Do not write Assamese in Bengali just because a provider lists Bengali. Ask native reviewers to grade vowel/consonant distinctions, rhythm, scientific words, code-switch transitions and number reading. An advertised supported locale is not a passed audition.

Optional Hindi original: "Naam wahi, ginti nayi; har atom ka hisaab sahi." Explain the precise coefficient rule immediately; the rhyme is not the definition. Any Assamese expressions should be drafted/reviewed by native editors; this package does not fabricate approved Assamese pronunciations.

**Multilingual Director (Skill #10):** Use one main language; keep required scientific terms; code-switch purposefully; verify values and signs; use native-script text and native reviewer; do not substitute Bengali for Assamese. "Translate text and reflow audio/visuals separately; not unconditional dubbing." `docs/Architecture.md`: "Each locale has independent voice/lexicon/audio/timing objects. Do not time-stretch the translation into English durations."

## 9. Human performance reference and consistency (message 12 §12 + guide)

Commission a performer to record a small **performance reference corpus**: **a calm explanation, prediction, difficult formula, understated joke, supportive correction, and confident recap.** This gives directors and reviewers a concrete standard. It does not necessarily need to become a cloned voice.

- **Performance reference:** demonstrates rhythm and intention.
- **Identity reference:** creates or conditions a voice resembling that speaker. Requires specific permission and the provider's applicable verification process. Consent to record a lesson should not be silently treated as consent to create an indefinitely reusable synthetic identity.

**Guide method:** Commission an adult performer who knowingly permits the specific synthetic voice/use. Record calm explanation, prediction, warm correction, formula delivery, understated joke and recap. Use clean dry recording and precise text. Keep consent, allowed uses, territory, duration, payment, model permissions, revocation/future-use policy and deletion terms documented. Reference performance guides rhythm; copying identity needs explicit permission. Speech-to-speech can preserve acting but cannot repair wrong science, omitted words or bad pronunciation automatically.

**Consistency without flatness (message 12 §12.3):** Version the voice profile, pronunciation dictionary, reference passages, model, settings, and accepted samples. Keep a "golden set" of difficult passages; re-run it before model upgrades. Do not silently replace a voice when a provider fails — a fallback must be an approved voice/model combination, or the job should wait. A voice identity can be consistent while moving between curiosity, precision, amusement, and reassurance. Consistency is not identical pitch and rhythm on every sentence.

## 10. Evidence boundaries (guide)

Retrieval practice: strong broad classroom evidence, but no exact mandatory interval. Enthusiasm effects are context-dependent; a 2024 experiment found separate benefits of vocal enthusiasm and visual cues, not additive benefits when combined. Learning and feeling-of-learning can diverge. Fluency, a high engagement score or an impressive voice demo does not establish examination benefit. Sources: https://pubmed.ncbi.nlm.nih.gov/33683913/ ; https://onlinelibrary.wiley.com/doi/10.1111/jcal.13049 ; https://www.pnas.org/doi/10.1073/pnas.1821936116 . Production numbers above are assumptions, not published psychological optima.

---

## 11. Worked example — the same science as textbook narration vs ExamLeaf teaching

The scientific target is the distinction between a coefficient and a subscript in a chemical equation. Changing coefficients adjusts quantities; changing the specified formula changes the chemical representation. Message 12 notes that its inline citation for this sentence "concerns the tool project rather than chemistry and should not be used to establish the chemistry claim; the complete example's scientific source is recorded in the downloadable script" — that source is **OpenStax Chemistry 2e §4.1**, https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations (`examples/claims.json`, status `example-source-ledger-not-external-approval`).

`examples/Before_After.md`: "These are original scripts about coefficients and molecular composition. They are not a complete lesson. Exact seconds below are director targets until final audio is measured. The generated Runway auditions demonstrate the contrast but differ in length and wording; they are not a controlled provider or learning benchmark."

### 11.1 Textbook version

> "A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms." (message 12)

`Before_After.md` and `examples/textbook.json` add a fourth sentence: "Verification requires counting each element on both sides." Direction: neutral, clear (`mode: steady`, 140 wpm). Visual: equation and counts. No deliberately degraded pronunciation or robotic effect. Critical phrases: "equal", "not", "four hydrogen", "two oxygen".

This is clear factual narration. It is not necessarily badly voiced. Its weakness is that it provides little help in constructing or testing the learner's understanding.

### 11.2 ExamLeaf version — message 12 rendering (modes + visual directions)

**CURIOUS**
> "Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer."

*Show two intact water molecules. Keep totals hidden. Insert six seconds of actual silence after the question audio ends.*

**DELIBERATE**
> "Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules—not what a molecule is."

*Reveal the hydrogen count when it is spoken. Highlight the coefficient when it is named.*

**LIGHT**
> "Changing water into hydrogen peroxide would be a very efficient way to answer a different question."

*Show the rejected change separately and clearly label it.*

**FOCUSED**
> "Keep the given formulas fixed. Use coefficients to change the counts."

**REASSURING**
> "Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts."

*Allow a learner-controlled pause. Do not treat the short media hold as a deadline.*

**FOCUSED**
> "Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula."

### 11.3 ExamLeaf version — `examples/Before_After.md` rendering (director's script)

CURIOUS — Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.

[Keep two intact water molecules visible. Hide totals. After the question audio ends, insert six seconds of genuine silence.]

DELIBERATE — Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules, not what a molecule is.

[Reveal four hydrogen atoms when the phrase begins. Highlight the coefficient only when it is named.]

LIGHT — Changing water into hydrogen peroxide would be a very efficient way to answer a different question. Keep the given formulas fixed. Use coefficients to change the counts.

[Show a rejected proposed formula separately and clearly label it. Restore water. No laughing sound effect.]

REASSURING — Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.

[Five-second default media hold, plus explicit student-controlled pause. This is not a five-second deadline.]

FOCUSED — Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.

"The machine-readable version is teacher.json. Actual live audition B was one provider take with expressive tags, not the sample-exact classroom hold implementation."

**Differences between the two renderings (recorded, not resolved):** (a) message 12 splits "Keep the given formulas fixed. Use coefficients to change the counts." into its own FOCUSED beat, while `Before_After.md` and `teacher.json` keep it inside the LIGHT `repair` segment; (b) message 12 uses an em dash ("molecules—not") where the files use a comma; (c) the spoken text in `teacher.json` is `Changing {{water_formula}} into {{hydrogen_peroxide}} …`, which the shipped lexicon expands to "Changing **H two O** into hydrogen peroxide …" (see `outputs/*_requests.json`), whereas both prose renderings say "Changing **water** into …" — the lexicon's own note for `water_formula` is "prefer water in explanatory prose".

### 11.4 The machine-readable plan (`examples/teacher.json`, lesson `water_coefficient_demo`)

| # | segment_id | objective | claims | mode / wpm | emphasis / notes | pause_after | answers_after | cues (phrase → action → element) | expected visuals | critical phrases |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | `question` | count_atoms | water-composition | curious / 140 | "each complete molecule" | think 6 s — "Count hydrogen atoms in two separate water molecules." | — | "Two water molecules" → show → `molecule-pair` | two water molecules; label elements, not totals | "Two water molecules", "hydrogen" |
| 2 | `answer` | count_atoms | water-composition, coefficient-quantity | deliberate / 130 | "Four", "not" | beat 0.4 s | `question` | "Four hydrogen atoms" → reveal-answer → `hydrogen-count`; "coefficient" → highlight → `coefficient` | highlight four hydrogen atoms, coefficient stays separate from subscript | "Four hydrogen atoms", "not" |
| 3 | `repair` | preserve_identity | subscript-identity | light / 142 | notes: "Dry observation, not a laugh. Return to focused explanation after different question." | beat 0.3 s | — | — | wrong proposed formula clearly labelled, then restore water | "fixed", "coefficients" |
| 4 | `retry` | count_atoms | water-composition | reassuring / 140 | — | pause-video 5 s — "Write hydrogen and oxygen atom totals for three water molecules." | — | — | three water molecules with totals hidden | "three water molecules" |
| 5 | `check` | count_atoms | water-composition | focused / 140 | — | none | `retry` | "Six hydrogen atoms" → reveal-answer → `retry-totals` | six hydrogen atoms; three oxygen atoms | "Six hydrogen", "three oxygen" |

Claims (`examples/claims.json`): `water-composition` — "A water molecule has two H atoms and one O atom."; `coefficient-quantity` — "In the molecular counting representation, a coefficient multiplies all atoms in each specified molecule."; `subscript-identity` — "Do not alter supplied correct chemical formulas merely to balance the equation."

**Timing the starter computed for this plan with NOT-SPEECH tone fixtures** (`outputs/timeline.json`, 48 kHz, 30 fps; engineering proof only, not speech): total 34.94 s (1,677,120 samples). Question think-pause 148,800 → 436,800 samples (exactly 288,000 samples = 6 s); answer starts at 436,800; `reveal_hydrogen` at sample 444,000 (frame 278) — after the window; retry pause 1,201,920 → 1,441,920 (5 s); `reveal_retry` at 1,449,120 (frame 906). Signal QA found exactly two silences, both `planned: true` (3.10–9.10 s and 25.04–30.04 s).

### 11.5 Why this version is more useful (message 12 §8)

The proposed script separates counts, creates a genuine attempt, explains the error, and checks a new case. The humour reinforces the identity-versus-quantity distinction. Its value should be measured through the next independent question—not simply whether students preferred the voice.

The two Runway demonstrations ("A" task `f48aa57f-08e4-42b7-aa3a-4058c5fe2519`, textbook; "B" task `9c51652f-fe83-4d1f-be9e-05234654557c`, teacher-style; both Arjun / eleven_v3 / speed 0.95 / en; 18 credits) "differ in wording, length, and expressive instructions, so they are demonstrations—not a controlled A/B experiment."

---

## 12. Templates

### 12.1 Reusable authoring prompts (`docs/Reusable_Prompts.md`, verbatim)

**Master teacher prompt.** Use the provided source claims, prerequisite map and independent answer key. Create original ExamLeaf narration for [class, medium, topic]. Begin with a concrete question. Explain the decision behind each step. Scaffold from observation to relationship to formal term to worked example to missing step to independent task. Preserve every scientific condition, unit, direction and sign. Use one helpful analogy only when its boundary is explicit. Optional humour must clarify or gently reduce tension. Do not invent student responses or performer biography. Return canonical spoken text separately from delivery and visual metadata. Ask/write/draw/solve cues require a precise task, hidden answer and adequate user-controlled pause. End with a capability check and a fresh practice item. Flag missing prerequisites rather than promising a whole foundation in ten minutes.

**Naturalizer prompt.** Edit only awkward spoken phrasing. For each change, show the original and revised scientific assertion. Preserve qualifications and negations. Remove stock openings, redundant motivational language and fake dialogue. Do not add ums, laughs or random slang as a proxy for being human. Return a minimal diff and unresolved teaching problems.

**Voice direction prompt.** Use VoiceIdentity[version]. For each accepted segment choose one dominant mode: curious, steady, deliberate, light, reassuring or focused. Add emphasis only to words carrying logical/quantitative meaning. State an approximate pace target, not a duration guarantee. Put exact thinking time outside synthesized audio. Identify difficult terms for acoustic audition. Do not output provider syntax until the adapter selects a capability-tested model.

**QA prompt.** Compare approved claims, canonical spoken text, observed ASR, actual audio timings and visuals. Separate confirmed defects from uncertain automatic flags. Check every number, unit, negation, direction and scientific condition; verify that no caption or reveal leaks an answer during a response window. A forced-alignment match and zero WER do not prove pronunciation. Return severity, source span, audio timestamp, implicated component, smallest repair and required reviewer.

### 12.2 Segment direction template (compiled for this guide from `configs/narration.schema.json` and §3–§6; not a source file)

```yaml
segment_id: <lowercase_id>            # ^[a-z][a-z0-9_-]*$
objective_id: <learning objective>
claim_ids: [<approved claim id>]      # at least one
text_template: >                      # spoken words only; no [tags] or <tags>; STEM terms as {{lexicon_key}}
  <exact words to be spoken>
direction:
  mode: curious | steady | deliberate | light | reassuring | focused
  target_wpm: 140                     # 80–185; a target, not a guarantee
  emphasis: [<words carrying logical/quantitative meaning>]
  notes: <optional performance note, e.g. "Dry observation, not a laugh.">
pause_after:
  kind: none | beat | think | pause-video
  seconds: 0                          # 0–30; inserted locally as exact silence
  prompt: <required for think / pause-video: the precise task>
answers_after: <segment_id of the earlier question, if this segment reveals its answer>
expected_visuals: [<what must be on screen; answers hidden during the window>]
critical_phrases: [<numbers, negations, conditions to verify in ASR>]
cues:
  - cue_id: <id>
    phrase: <exact spoken phrase to anchor on>
    occurrence: 1                     # which repeat of the phrase
    edge: start | end
    action: show | highlight | transform | hide | reveal-answer
    element_id: <scene element>
```

### 12.3 Emotional-delivery checklist (compiled for this guide from §2–§6; not a source file)

| Check | Pass condition |
|---|---|
| One dominant intention | exactly one `mode` |
| Emphasis is meaningful | only logical/quantitative words emphasised |
| No fake awareness | no "I heard you", no unconditional "you got it" |
| Humour returns to science | the next sentence is the scientific point; zero jokes is fine |
| Correction is repairable | names what was right, then the specific fix |
| Praise is conditional | "If your result matches…" form |
| Pause is a real task | `think`/`pause-video` has a precise `prompt`, answer hidden |
| Not rushed | dense symbolic text at ~105–125 wpm with inspection time |
