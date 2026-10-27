# Index of the ten Super Teacher Skills

**Where these come from.** ChatGPT message 08, section 11.1 ("Existing resources versus custom work"), lists ten custom Skill drafts and says the starter pack contains them. They are the folders under `starter_pack/ExamLeaf_Super_Teacher/skills/` (copied unchanged from `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/skills/`). Each folder has the same three files: `SKILL.md`, `evals/evals.json`, `references/authoring_contract.md`.

**Status, exactly as the source states it.**
- They are *drafts*: "original custom Skill drafts", "not an installed plugin or completed production platform" (pack `README.md`).
- "The Skills have not been evaluated through Claude/Codex runs" (message 08). Each `SKILL.md` repeats: "Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required." Each skill has exactly one eval (a negative test); none has been run.
- The existing foundations (Claude Code Skills, the Agent Skills standard, Codex Skills, Anthropic's skill-creator workflow) are "verified"; the *ExamLeaf teaching personality* in these Skills is not: "they do not provide a proven ExamLeaf teaching personality."
- Discrepancy to be aware of: the progress note (`prompt/07a_ASSISTANT_progress_note.md`) says "14 draft Skills". The final message and the pack contain **ten**. The ten are the deliverable; no fourteen-skill set exists in the sources.

**Where the same ideas live elsewhere.** `06_skills_library/` is the section for the consolidated Skills library; `05_narration_system/` holds the narration/voice material that `examleaf-voice-director` and `examleaf-conversational-script` feed. The engine's compact version of this persona is `related/Super_Teacher_Contract.md`.

## 1. Summary table

Responsibility and "required output" are quoted from the table in section 11.1 of message 08. File lists are the actual contents of each folder.

| # | Skill (folder name) | Responsibility | Required output (message 08) | SKILL.md path | Files in folder |
|---|---|---|---|---|---|
| 1 | `examleaf-lesson-architect` | Scope, prerequisites, objectives, teaching progression | Lesson plan and independent target task | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-lesson-architect/SKILL.md` | `SKILL.md`, `evals/evals.json`, `references/authoring_contract.md` |
| 2 | `examleaf-conversational-script` | Natural narration without losing scientific meaning | Clean spoken draft | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-conversational-script/SKILL.md` | same three files |
| 3 | `examleaf-analogy-auditor` | Mapping, limits, misconception risks | Analogy cards and rejected options | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-analogy-auditor/SKILL.md` | same three files |
| 4 | `examleaf-concept-humour` | Relevant, respectful light moments | Optional lines and deletion rationale | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-concept-humour/SKILL.md` | same three files |
| 5 | `examleaf-interaction-designer` | Questions, wait time, hidden answers, retries | Interaction sequence and answer keys | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-interaction-designer/SKILL.md` | same three files |
| 6 | `examleaf-confidence-editor` | Informative feedback and honest progress language | Revised feedback | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-confidence-editor/SKILL.md` | same three files |
| 7 | `examleaf-voice-director` | Pronunciation, delivery, pauses, synchronization | Voice-ready records | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-voice-director/SKILL.md` | same three files |
| 8 | `examleaf-language-editor` | English/localized versions and terminology consistency | Language review draft | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-language-editor/SKILL.md` | same three files |
| 9 | `examleaf-science-reviewer` | Independent verification of claims and solutions | Errors, assumptions, approval blockers | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-science-reviewer/SKILL.md` | same three files |
| 10 | `examleaf-script-evaluator` | Combined review, repetition checks, release issues | Structured evaluation report | `starter_pack/ExamLeaf_Super_Teacher/skills/examleaf-script-evaluator/SKILL.md` | same three files |

The ten `references/authoring_contract.md` copies are byte-identical to each other and to the pack-level `starter_pack/ExamLeaf_Super_Teacher/references/authoring_contract.md` (same MD5 for all eleven files). Its content is summarised in section 4 below.

**Shared frontmatter shape.** Every `SKILL.md` begins with YAML `name:` and `description:` (the portable Agent Skills convention), then a heading, the line "Read `references/authoring_contract.md` before working.", and the sections Inputs, Workflow, Outputs, Acceptance and escalation, Evaluation.

**Suggested order of use** (organiser's mapping of the skills onto the production sequence in message 08 section 11.2 and pack guide section 12; the source does not assign each skill to a stage in so many words):

```text
Approved sources + independently checked answer key
  -> 1 lesson-architect          (Lesson architecture)
  -> 2 conversational-script     (Conversational draft)
  -> 3 analogy-auditor, 4 concept-humour, 5 interaction-designer   (Analogy / humour / interaction review)
  -> 6 confidence-editor         (feedback and confidence wording)
  -> 9 science-reviewer          (Scientific review and repair)
  -> 8 language-editor, 7 voice-director   (Language and voice preparation)
  -> audio generation and measured synchronization (outside these skills)
  -> 10 script-evaluator         (combined release review, repetition checks)
  -> human academic + rendered-video + accessibility review, student testing, controlled release
```

## 2. Per-skill detail (purpose, inputs, steps, outputs, negative test)

The "Steps" are the Workflow paragraph of each `SKILL.md`, split into numbered steps without changing their content. Read the `SKILL.md` itself for the exact wording.

### 1. `examleaf-lesson-architect`
- **Purpose (frontmatter description):** Plan one manageable ExamLeaf STEM lesson from an approved source packet and a specified learner baseline.
- **Inputs:** Source packet with stable source IDs; class, topic, language, learner baseline, duration and exam scope.
- **Steps:**
  1. Produce `lesson_brief.md` with one primary independent capability, prerequisites and a source-linked claim ledger.
  2. Identify what is deliberately out of scope.
  3. Write the assessment before drafting a hook.
  4. Choose a phenomenon, misconception or problem that leads to that assessment.
  5. Budget fully worked, completion and independent tasks; include a targeted repair route.
  6. Use planned timing, not claimed audio timing.
  7. Do not quietly turn a revision brief into first teaching of an entire difficult chapter. If the sources are incomplete, mark the gap and scope down rather than inventing content.
- **Outputs:** `lesson_brief.md`; `claims.json`; `assessment_key.md`
- **Negative eval (`evals/evals.json`, id 1):** prompt "Input requests all of electromagnetism for a learner unfamiliar with algebra in ten minutes." Expected: "Narrows the scope, identifies prerequisites, refuses a universal mastery promise and records missing sources."

### 2. `examleaf-conversational-script`
- **Purpose:** Draft or rewrite source-grounded educational narration into the original ExamLeaf teacher voice.
- **Inputs:** Approved lesson brief, claim ledger, answer keys, analogy cards and recent script ledger.
- **Steps:**
  1. Write for a single teenage viewer, not for a textbook or an auditorium.
  2. Keep the scientific relationships fixed while rewriting their explanation; state why each step is chosen.
  3. Prefer concrete verbs, short clauses, natural contractions and purposeful question-answer turns.
  4. Include exact exam terminology after the plain-language explanation.
  5. Write every spoken word; do not replace difficult teaching with placeholders. Separate narration from stage directions.
  6. Do not fabricate memories, an audible student, spontaneous errors or named-teacher impersonation.
  7. Return meaningful alternative openings, choose one, and explain the choice briefly.
  8. Keep humour optional and secondary.
- **Outputs:** `script.md`; `beat_plan.json`; `change_log.md`
- **Negative eval:** prompt "Rewrite a correct but formal derivation. The request asks for fake stutters and 'I heard you say three.'" Expected: "Preserves the derivation while using natural clauses; excludes fake hearing and unnecessary disfluencies."

### 3. `examleaf-analogy-auditor`
- **Purpose:** Create or audit a scientific analogy without letting the analogy imply false science.
- **Inputs:** Target concept, learner familiarity, candidate analogy, formal model and sources.
- **Steps:**
  1. Create an analogy card with: `target_relation`, `familiar_relation`, `mapping`, `non_mapping`, `likely_misconception`, `formal_return`, `learner_check` (see `starter_pack/ExamLeaf_Super_Teacher/references/analogy_card.example.json` for a filled example).
  2. Compare at least two possible analogies, including no analogy.
  3. Choose the least complex one that explains the relationship.
  4. State the limit aloud where the wrong inference is likely.
  5. Reject analogies that need more background than the target concept, equate unlike quantities, or imply organisms and particles act with intentions.
  6. Require the learner to explain the scientific relation without the story at the end.
- **Outputs:** `analogy_cards.json`; `rejected_analogies.md`
- **Negative eval:** prompt "Use traffic to explain current and claim electrons travel from a switch to a lamp almost instantly." Expected: "Separates charge flow from signal propagation and rejects the false transport implication."

### 4. `examleaf-concept-humour`
- **Purpose:** Generate or review original, teenager-appropriate humour tied to a particular learning point.
- **Inputs:** Approved explanation, exact misconception, audience/language profile and used-joke ledger.
- **Steps:**
  1. Offer up to three short candidates and a no-joke alternative.
  2. For each record `concept_anchor`, `comedic_mechanism`, `literal_science_risk`, `translation_risk`, `narration_seconds` and the follow-up scientific sentence.
  3. Prefer dry observation, a gentle contrast, or a short callback. Do not require a quota.
  4. Reject identity-targeted ridicule, teacher imitation, political or relationship bait, sarcasm whose literal reading teaches the wrong answer, unlicensed meme clips and generic motivational rhymes.
  5. Put the joke after clarity, or use it to expose the exact wrong turn; never over the first dense derivation.
  6. Recheck that the next remembered sentence is the scientific one.
- **Outputs:** `humour_candidates.json`; `chosen_edits.md`
- **Negative eval:** prompt "Add ten memes and a joke calling students stupid for changing a chemical subscript." Expected: "Rejects the insult and quota; offers at most a brief concept-specific line or no joke."

### 5. `examleaf-interaction-designer`
- **Purpose:** Create genuine prediction, retrieval and practice moments for prerecorded or interactive lessons.
- **Inputs:** Lesson objectives, script, answer keys, player type and timing budget.
- **Steps:**
  1. Distinguish rhetorical questions from learner-response prompts.
  2. Give each learner prompt: `expected_answer`, `acceptable_variations`, `available_hint`, `reveal_trigger`, `estimated_task_time`, `feedback` and `retry`.
  3. Use a few meaningful checkpoints, not questions on every sentence.
  4. Reserve learner-controlled pauses for writing, drawing and multi-step work; during such tasks stop new narration.
  5. Keep answers hidden across diagram, captions and overlays.
  6. Prerecorded feedback is conditional; actual answer-dependent branches require recorded input and a verified rule.
  7. Do not count copying as retrieval.
  8. Select tasks appropriate to the subject, rather than forcing all activity types into every lesson.
- **Outputs:** `interactions.json`; `timing_changes.md`
- **Negative eval:** prompt "The solution appears in the background during a five-second question pause." Expected: "Flags answer leakage and moves all answer-bearing states after the reveal trigger."

### 6. `examleaf-confidence-editor`
- **Purpose:** Replace empty praise and anxiety-inducing wording with evidence-specific, respectful teaching feedback.
- **Inputs:** Script, anticipated student errors, answer rubric and evidence level.
- **Steps:**
  1. Inspect every claim about the learner, every success message and every correction.
  2. Rewrite feedback as observed/conditional success, specific issue and actionable next step.
  3. Use "your choice of relationship is correct" only when actual input supports it, or phrase it conditionally in video.
  4. Separate arithmetic, representation, strategy, terminology and prerequisite errors.
  5. Remove "easy", "obvious", score promises and intelligence judgments where they shame or overclaim.
  6. Preserve warmth without fabricated intimacy.
  7. End with a self-check and a fresh task, not a declaration that viewing equals mastery.
  8. Keep persistent anxiety outside the scope of a teaching-video cure.
- **Outputs:** `feedback_edits.md`; `confidence_checks.json`
- **Negative eval:** prompt: the script says "You are a genius. You have mastered this chapter just by watching." Expected: "Replaces identity praise and unearned mastery with a task-specific self-check and next attempt."

### 7. `examleaf-voice-director`
- **Purpose:** Prepare clean narration and provider-neutral performance cues for ExamLeaf voice production.
- **Inputs:** Approved script, pronunciation lexicon, chosen provider/model capabilities and shot/scene IDs.
- **Steps:**
  1. Separate `spoken_text`, `display_text`, tone, emphasis, pause and `visual_event` fields.
  2. Use one stable narrator voice with local energy changes at conceptual turns.
  3. Spell out ambiguous formulas, units and chemical coefficients; preserve academic notation on screen.
  4. Avoid laughter over instructions, fake gasps and every-line emotion tags.
  5. Write a short performance brief and a native-language pronunciation audition.
  6. Map only documented controls to the selected voice engine. Unknown controls must fail validation, not be spoken accidentally.
  7. Exact waits and reveals belong to the renderer.
  8. Measure generated audio; edit scope or wording instead of blindly speeding it up.
- **Outputs:** `narration.txt`; `performance.json`; `pronunciation_review.md`
- **Negative eval:** prompt "Feed [THINK:8] and SSML break tags unchanged to an engine that does not support them." Expected: "Keeps internal timing tags out of speech; schedules silence separately and checks model-specific support."

### 8. `examleaf-language-editor`
- **Purpose:** Adapt ExamLeaf narration to an explicitly chosen English, Hinglish or Assamese-supported audience.
- **Inputs:** Approved semantic script, language/medium, terminology glossary and native reviewer availability.
- **Steps:**
  1. Preserve the scientific meaning, numbers, assumptions and task demand across versions.
  2. Use one dominant teaching language.
  3. Introduce official terms beside their explanation and retain required examination terminology.
  4. Put any code-switch at a meaningful boundary, not inside a difficult formula.
  5. Do not assume Hindi suits every Assam learner or that Indian students share one slang register.
  6. Translate the learning function of humour rather than a pun word-for-word.
  7. Mark Assamese drafts for native subject-editor review.
  8. Original rhyme is optional, brief, and followed by the scientific rule; no pseudo-traditional attribution.
- **Outputs:** `localized_script.md`; `terminology.csv`; `native_review_queue.md`
- **Negative eval:** prompt "Make an English-medium Assam lesson automatically 50 percent Hindi and translate all jokes literally." Expected: "Rejects the demographic assumption; offers audience-tested editions and preserves technical meaning."

### 9. `examleaf-science-reviewer`
- **Purpose:** Independently verify the scientific claims, examples and implications in a finished ExamLeaf script.
- **Inputs:** Script, claim ledger, source packet, equations, visual specification and answer keys.
- **Steps:**
  1. Re-solve the examples without relying on the author answer.
  2. Check conditions, signs, units, domains, atom and charge counts, diagram directions, biological compartments and declared simplifications as applicable.
  3. Review what humour and analogy imply literally.
  4. Check intermediate states, not only the final answer.
  5. Distinguish balanced equations from plausible reactions, schematic motion from mechanism and authored exam wording from official rubrics.
  6. Return critical/major/minor findings with scene IDs, source support and a minimal repair.
  7. Do not use an aggregate score to pass a critical error. Human approval remains separate from this agent review.
- **Outputs:** `science_review.json`; `independently_solved_answers.md`
- **Negative eval:** prompt "A chemical equation is atom-balanced after replacing H2O by H2O2 and is marked the correct answer." Expected: "Fails the altered-species answer even though its atom counts balance."

### 10. `examleaf-script-evaluator`
- **Purpose:** Evaluate an ExamLeaf script for regressions, naturalness, accessibility and actual learning opportunities.
- **Inputs:** Current script, approved prior scripts, test corpus, source reviews and any learner-study results.
- **Steps:**
  1. Run structural checks (the pack's `tools/lint_script.py`; see `INSTRUCTIONS_super_teacher_authoring.md`), then perform a qualitative read-aloud review.
  2. Track repeated opening forms, analogy families, jokes and closures across the recent catalogue; do not replace accurate technical terms merely for novelty.
  3. Check that timing includes pauses and that prompt answers are hidden.
  4. Report separately: science blockers, learner-action failures, naturalness observations and research hypotheses.
  5. Compare the voice-only, visual-only and combined experience.
  6. Design content-matched or time-matched learner tests explicitly, with immediate and delayed unprompted outcomes and confidence calibration.
  7. Small usability tests do not establish causal effectiveness. Never claim model evaluation proves teenagers will enjoy a joke.
- **Outputs:** `release_review.md`; `regression_report.json`; `experiment_plan.md`
- **Negative eval:** prompt "A script is entertaining but has no unprompted problem and reuses the previous ten openings." Expected: "Flags missing independent performance, repeated structure and unvalidated enjoyment; requests targeted repair."

## 3. Text shared by all ten `SKILL.md` files (verbatim)

**Acceptance and escalation** (identical in every skill):
> Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

**Evaluation** (identical in every skill):
> See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.

## 4. What the shared `authoring_contract.md` says (summary of the file every skill must read first)

Full file: `starter_pack/ExamLeaf_Super_Teacher/references/authoring_contract.md` (2,954 bytes, identical in all ten skill folders).
- **Priority:** scientific accuracy, then genuine independent learning, then accessibility, then warmth and clarity, then humour and novelty. **Audience:** Class 10–12; faceless, diagram-led STEM revision; do not copy a named teacher's voice, character, catchphrase or personal anecdotes; simple English by default for the sample; Assamese/Hinglish need audience fit and native editorial review.
- **Evidence versus production choices:** retrieval, worked examples, selective signalling and feedback have a research foundation, but exact joke counts, interaction intervals, word rates and creative devices are "unvalidated production settings until tested with ExamLeaf learners". No promise of ten-minute chapter mastery.
- **Narrator:** capable, warm, notices the next likely difficulty, explains the reason for each step; contractions, direct questions, varied sentence length; no stagey fillers, fake mistakes, constant exclamation marks, generic motivational paragraphs or invented school memories; never pretend to hear, see or know the viewer; conditional feedback allowed; no score guarantees, identity praise or shaming.
- **Each concept:** meaning, representation, precise terminology, worked decision, reduced-support attempt, independent attempt, feedback and delayed retrieval. Copying while looking at the answer is not independent performance; hide the answer in visuals and captions until the response interval ends.
- **Analogies and jokes:** record target relationship, familiar relationship, mapping, limitations, return to formal science; no teleology disguised as mechanism; humour targets the situation or a misconception, never ability, identity, family, accent, poverty, marks or body; a joke must survive deletion; no unlicensed clips or invented popularity statistics.
- **Voice and timing:** keep spoken text, formula display, voice direction and animation cues separate; internal tags are not universal TTS syntax; insert exact response pauses in the media timeline; the ten-minute target is a production plan until audio is measured.
- **Release:** unverified sources, scientific implications, pronunciation, translations and any answer marked correct need review; automated checks cannot approve science or humour; human subject review plus full rendered-video review are mandatory.

## 5. Companion prompts and reference files in the same pack

| File | Role | Closest skill (organiser's mapping) |
|---|---|---|
| `starter_pack/ExamLeaf_Super_Teacher/prompts/Master_Authoring_Prompt.md` | One-shot prompt that produces a complete lesson (narration, timed beat table, claim/analogy/humour audit, answer key) | `examleaf-lesson-architect` + `examleaf-conversational-script` |
| `starter_pack/ExamLeaf_Super_Teacher/prompts/Conversational_Repair_Prompt.md` | Minimal-change rewrite pass for sentences that sound written, with science-meaning check | `examleaf-conversational-script` |
| `starter_pack/ExamLeaf_Super_Teacher/prompts/Independent_Review_Prompt.md` | Independent reviewer that solves tasks first, then checks the script; blockers first | `examleaf-science-reviewer` |
| `starter_pack/ExamLeaf_Super_Teacher/references/analogy_card.example.json` | Filled analogy card `CHEM-COEFF-SANDWICH-01`, status `DRAFT_HUMAN_REVIEW_REQUIRED` | `examleaf-analogy-auditor` |
| `starter_pack/ExamLeaf_Super_Teacher/references/Research_Ledger.md` | Evidence IDs P01–P18, S01–S04, T01–T07 | all (cited as [P01] etc. in the guide) |

## 6. If and when you choose to install them (not done here)

This section restates the pack's own README; the organiser installed nothing. The pack says: copy the desired Skill directories into `.claude/skills/` in a Claude Code repository, or `.agents/skills/` for Codex. These are *alternatives*; keep one canonical source and avoid duplicate drifting copies. In Claude Code an installed skill is invoked by its slash command, for example `/examleaf-lesson-architect`; in Codex select or name the skill via the supported interface. Do not assume Claude-specific frontmatter or invocation controls transfer unchanged; confirm discovery against your current client documentation. The pack warns that a SKILL.md file is not reliable behaviour on its own and recommends Anthropic's skill-creator evaluation workflow for evaluated development.
