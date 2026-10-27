# 03_super_teacher_framework: the ExamLeaf "Super Teacher" personality, narration and scriptwriting framework

## 1. What this section is and where it came from

**What it is.** The complete material on the "Super Teacher": the persona that narrates ExamLeaf's ten-minute STEM revision videos (Class 10–12, Assam Board). It contains the research-based framework, the personality and delivery rules, the interaction and humour rules, ten draft Claude/Codex Skills, reusable prompts, a structural checker, and one complete timed sample lesson (balancing chemical equations).

**Where it came from.** One exchange in the ChatGPT research project (share `6acf03ec-b480-83ee-a000-3701059934d9`):

| Source | What it is | Where the original sits (never modified) |
|---|---|---|
| Message 07 (user) | The research and creative-analysis brief: ten areas to research (human-like teaching, teaching psychology, Dora-style interaction, humour/memes, emotional connection, voice acting, stories, attention, language/personality, scriptwriting framework) and eight required deliverables | `00_source/chatgpt_transcript/messages/07_USER_prompt_super_teacher.md` |
| Message 07a (assistant) | A one-sentence progress note | `00_source/chatgpt_transcript/messages/07a_ASSISTANT_progress_note.md` |
| Message 08 (assistant) | The answer: a 13-section framework (about 48K characters) ending with the complete timed sample script | `00_source/chatgpt_transcript/messages/08_ASSISTANT_super_teacher_framework.md` |
| Starter pack | The zip that message 08 links as "the complete Super Teacher starter pack": guide, ten Skills, prompts, ledger, sample JSON and script, linter, tests | `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/` (45 files) |
| Separate downloads | Loose copies of the guide and the sample script | `00_source/downloads/ExamLeaf_Super_Teacher/` (2 files) |
| Engine contract | How the later Video Engine implementation encodes the same persona | `00_source/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/docs/Super_Teacher_Contract.md` |

**The idea in one line (from message 08):** the teacher should be "warm toward the student, exacting about the science, and playful about the problem", and sound human "because it teaches responsively, not because it imitates human imperfections".

## 2. Start here

1. Want the whole argument and every example? Read `FULL_super_teacher_framework.md`.
2. Want to write a lesson? Follow `INSTRUCTIONS_super_teacher_authoring.md` (17 steps plus a one-page checklist).
3. Want to see the finished product? Read `SAMPLE_SCRIPT_balancing_chemical_equations.md`.
4. Want to wire up the Skills? Read `SKILLS_INDEX_super_teacher_10.md`, then the folders under `starter_pack/ExamLeaf_Super_Teacher/skills/`.

## 3. Directory layout

```text
03_super_teacher_framework/
  README.md                                          (this file)
  FULL_super_teacher_framework.md                    cleaned full text of message 08 (incl. complete timed sample script)
  INSTRUCTIONS_super_teacher_authoring.md            step-by-step authoring procedure
  SKILLS_INDEX_super_teacher_10.md                   table and per-skill summary of the ten Skills
  SAMPLE_SCRIPT_balancing_chemical_equations.md      sample script extracted standalone, plus pack comparison and beat table
  prompt/                                            the user prompt (07) and progress note (07a)
  related/                                           Super_Teacher_Contract.md from the engine implementation
  starter_pack/ExamLeaf_Super_Teacher/               verbatim copy of the 45-file pack (README, guide, skills/, prompts/, references/, examples/, tools/, evals/)
```

## 4. Every file placed, with a one-line description

### 4.1 Written for this section (5 files, plus this README)

| File | One-line description |
|---|---|
| `README.md` | This index: provenance, file list, usage, verified-versus-proposed status, gaps, cross-references. |
| `FULL_super_teacher_framework.md` | Message 08 in full: research support, personality standards, explanation ladder, repair route, analogy contract, Aha pattern, interaction loop and schedule, humour, feedback, subject examples, before/after narration, voice and cue tags, ten-minute structure, ten Skills, master prompt, ledger and negative tests, full timed sample script, pilot comparisons. Only LaTeX and citation markers were reformatted. |
| `INSTRUCTIONS_super_teacher_authoring.md` | 17-step procedure for authoring a lesson in this persona, quoting the source verbatim for every rule, table and prompt, with the linter and test commands and a pre-flight checklist. |
| `SKILLS_INDEX_super_teacher_10.md` | The ten Skills: name, responsibility, required output, path, folder contents, and per-skill inputs, steps, outputs and negative eval. |
| `SAMPLE_SCRIPT_balancing_chemical_equations.md` | Section 12 of message 08 as a standalone file (16 timed beats, 00:00–10:00), with a comparison to the pack version and a beat table read from `sample_lesson.json`. |

### 4.2 `prompt/` (2 files, byte-identical copies of the transcript files)

| File | One-line description |
|---|---|
| `prompt/07_USER_prompt_super_teacher.md` | The user's research brief: ten research areas, eight required deliverables, tone constraints, and the "Ultimate Goal" student reaction. |
| `prompt/07a_ASSISTANT_progress_note.md` | ChatGPT's interim note: "chemistry sample and 14 draft Skills are complete" (see discrepancy in section 8). |

### 4.3 `related/` (1 file, byte-identical copy)

| File | One-line description |
|---|---|
| `related/Super_Teacher_Contract.md` | The engine implementation's compact contract: identity, sequence, pilot targets (roughly 1,100–1,250 words, 130–155 wpm), analogy contract, voice tags, conditional feedback, evidence and evaluation notes. |

### 4.4 `starter_pack/ExamLeaf_Super_Teacher/` (45 files, copied with `cp -R`; `diff -r` against the source showed no differences)

**Root and examples**

| File | One-line description |
|---|---|
| `README.md` | Pack readme (v1.0, research checked 13 October 2026): contents, how to copy Skills, the lint and test commands, production safeguards, third-party material note. |
| `Super_Teacher_Guide.md` | The 15-section personality and scriptwriting guide (personality, evidence, voice of a teacher, prerequisite repair, analogies, interaction, humour, confidence, language, voice direction, animation sync, process, repetition, validation, release gate). |
| `examples/Complete_Sample_Script.md` | The balancing-equations lesson as 16 timed beats with Direction, narration, Visual and Synchronization fields and a timing audit (1,225 words, 63 seconds of holds). |
| `examples/sample_lesson.json` | The same lesson as machine-readable JSON (beats B01 to B16, 600 s target, status UNRENDERED_DRAFT) that the linter reads. |

**Prompts**

| File | One-line description |
|---|---|
| `prompts/Master_Authoring_Prompt.md` | One-shot prompt to author a complete lesson and return narration, a timed beat table, a claim/analogy/humour audit and an answer key. |
| `prompts/Conversational_Repair_Prompt.md` | Pass that finds written-sounding lines and returns a minimal change set with science-meaning checks. |
| `prompts/Independent_Review_Prompt.md` | Independent subject-teacher review: solve tasks blind, then check script and visuals; blockers first. |

**References**

| File | One-line description |
|---|---|
| `references/Research_Ledger.md` | Evidence and capability ledger: P01–P18 (studies), S01–S04 (subject sources), T01–T07 (tool and accessibility docs), with limits of each. |
| `references/authoring_contract.md` | The shared contract every Skill must read first (priorities, narrator, concept sequence, analogies and jokes, voice and timing, release). |
| `references/analogy_card.example.json` | Filled analogy card `CHEM-COEFF-SANDWICH-01` (status DRAFT_HUMAN_REVIEW_REQUIRED). |

**Tools**

| File | One-line description |
|---|---|
| `tools/lint_script.py` | Standard-library structural checker for lesson JSON (timing contiguity, IDs, stage tags in speech, fake sensing, answer keys). Not run by the organiser. |
| `tools/build_sample.py` | Generator that builds `sample_lesson.json` and `Complete_Sample_Script.md` from the in-file beat table. Not run by the organiser. |

**Evals**

| File | One-line description |
|---|---|
| `evals/test_linter.py` | Twelve `unittest` regression tests for the linter. Not run by the organiser. |
| `evals/local_test_report.txt` | The pack's recorded run: 12 tests, OK. |
| `evals/sample_structural_check.json` | The recorded lint result for the sample: 0 errors, 0 warnings, `academic_approval: false`, `audio_timing_measured: false`. |

**Skills (10 folders x 3 files = 30 files).** Each folder holds `SKILL.md` (the instructions), `evals/evals.json` (one negative test) and `references/authoring_contract.md` (identical copy of the shared contract). Details of each are in `SKILLS_INDEX_super_teacher_10.md`.

| Skill folder | `SKILL.md` | `evals/evals.json` | `references/authoring_contract.md` |
|---|---|---|---|
| `skills/examleaf-lesson-architect/` | `skills/examleaf-lesson-architect/SKILL.md`: Plans one lesson: capability, prerequisites, claim ledger, assessment first | `skills/examleaf-lesson-architect/evals/evals.json`: all-of-electromagnetism-in-ten-minutes test | `skills/examleaf-lesson-architect/references/authoring_contract.md` |
| `skills/examleaf-conversational-script/` | `skills/examleaf-conversational-script/SKILL.md`: Drafts source-grounded narration in the teacher voice | `skills/examleaf-conversational-script/evals/evals.json`: fake stutters / "I heard you" test | `skills/examleaf-conversational-script/references/authoring_contract.md` |
| `skills/examleaf-analogy-auditor/` | `skills/examleaf-analogy-auditor/SKILL.md`: Builds and audits analogy cards; rejects false-science analogies | `skills/examleaf-analogy-auditor/evals/evals.json`: traffic-and-electrons test | `skills/examleaf-analogy-auditor/references/authoring_contract.md` |
| `skills/examleaf-concept-humour/` | `skills/examleaf-concept-humour/SKILL.md`: Proposes or reviews concept-linked, respectful humour (or none) | `skills/examleaf-concept-humour/evals/evals.json`: ten-memes-and-insult test | `skills/examleaf-concept-humour/references/authoring_contract.md` |
| `skills/examleaf-interaction-designer/` | `skills/examleaf-interaction-designer/SKILL.md`: Designs prediction, retrieval and practice moments with hidden answers | `skills/examleaf-interaction-designer/evals/evals.json`: answer-leakage test | `skills/examleaf-interaction-designer/references/authoring_contract.md` |
| `skills/examleaf-confidence-editor/` | `skills/examleaf-confidence-editor/SKILL.md`: Replaces empty praise with evidence-specific feedback | `skills/examleaf-confidence-editor/evals/evals.json`: "you are a genius" test | `skills/examleaf-confidence-editor/references/authoring_contract.md` |
| `skills/examleaf-voice-director/` | `skills/examleaf-voice-director/SKILL.md`: Prepares clean narration and provider-neutral cues | `skills/examleaf-voice-director/evals/evals.json`: unsupported-timing-tag test | `skills/examleaf-voice-director/references/authoring_contract.md` |
| `skills/examleaf-language-editor/` | `skills/examleaf-language-editor/SKILL.md`: Adapts to a chosen English, Hinglish or Assamese-supported edition | `skills/examleaf-language-editor/evals/evals.json`: 50-percent-Hindi test | `skills/examleaf-language-editor/references/authoring_contract.md` |
| `skills/examleaf-science-reviewer/` | `skills/examleaf-science-reviewer/SKILL.md`: Independently re-solves and verifies claims and implications | `skills/examleaf-science-reviewer/evals/evals.json`: H2O-to-H2O2 test | `skills/examleaf-science-reviewer/references/authoring_contract.md` |
| `skills/examleaf-script-evaluator/` | `skills/examleaf-script-evaluator/SKILL.md`: Combined release review, repetition and learner-action checks | `skills/examleaf-script-evaluator/evals/evals.json`: entertaining-but-no-independent-task test | `skills/examleaf-script-evaluator/references/authoring_contract.md` |

## 5. How to use this section (step by step)

1. **Orient.** Read section 1 of `FULL_super_teacher_framework.md` ("What the research actually supports"), then `starter_pack/ExamLeaf_Super_Teacher/README.md` and the "Research and capability ledger" so you know which numbers are hypotheses.
2. **Set the persona.** Read sections 2 to 6 of the FULL file (personality, explanation ladder, interaction, humour, feedback). The authoring file turns these into Steps 1 to 9.
3. **Study the model lesson.** Read `SAMPLE_SCRIPT_balancing_chemical_equations.md` beside its pack twin `starter_pack/.../examples/Complete_Sample_Script.md` (adds Visual and Synchronization notes) and `sample_lesson.json` (the data shape the engine and linter expect).
4. **Author a new lesson.** Gather an approved source packet and an independently solved answer key. Follow `INSTRUCTIONS_super_teacher_authoring.md` Steps 1 to 14. Use the master prompt in Step 13 (two versions, both quoted verbatim there) in a model session, then the repair and independent-review prompts in separate sessions.
5. **Use the Skills.** Read `SKILLS_INDEX_super_teacher_10.md` for the order and inputs. The pack README says to copy the chosen Skill folders into `.claude/skills/` (Claude Code) or `.agents/skills/` (Codex), alternatives not both. The organiser installed nothing; installation is your decision, and `06_skills_library/` is where the consolidated library is described.
6. **Check structure.** From inside a *copy* of the pack folder run the two pack commands (Step 15 of the authoring file). They check shape only.
7. **Prepare voice and render.** Hand the clean script, display text, voice direction and renderer events to the narration and engine sections (`05_narration_system/`, `04_video_engine/`). Measure real audio before calling any timing final.
8. **Review and release.** Human academic review, rendered-video review, captions and (for Assamese or Hinglish) native-language review; then the release gate (Step 16), then the pilot comparisons (Step 17).

## 6. Verified versus proposed or untested, exactly as the sources state it

| Item | Status stated in the source | Where stated |
|---|---|---|
| Existing foundations: Claude Code Skills, Agent Skills standard, Codex Skills support, Anthropic skill-creator evaluation workflow | Described as "verified existing foundations" (documentation consulted, ledger T01–T04); they supply packaging conventions, "not a proven ExamLeaf teaching personality" | Message 08 section 11.1; Research_Ledger |
| ElevenLabs Eleven v4 and v3 do not support SSML break tags; Google SSML support is model-specific | Checked against official documentation on 2026-10-13 (ledger T05, T06) | Message 08 section 9.4; Research_Ledger |
| The linter | "Passed 12 local structural tests"; "structural tests only"; cannot judge science, answer leakage in every graphic, naturalness or learning | Message 08 intro; pack README; `evals/local_test_report.txt` |
| Research findings (Mayer 2004, Atkinson/Renkl/Merrill 2003, Bisra 2018, Yang 2021, Deslauriers 2019, Wisniewski 2020, 2026 humour study, etc.) | Real studies with stated limits; ledger calls itself "a targeted research synthesis, not a preregistered systematic review" | Message 08 section 1; Research_Ledger |
| The ten Skills | "Drafts"; "have not been evaluated through Claude/Codex runs"; one negative eval each, none run | Message 08 intro; each SKILL.md; pack README |
| The sample lesson | "Not been voiced, rendered, or tested with students"; no audio generated; `status` UNRENDERED_DRAFT, `academic_review` PENDING_HUMAN_REVIEW, `timing_status` PLANNED_NOT_AUDIO_MEASURED; 600 s is "planned, not measured audio" | Message 08 section 12; `sample_lesson.json`; pack README |
| Chemistry content of the sample | Based on standard atom conservation (OpenStax Chemistry 2e 4.1, ledger S01); narration original; still needs human academic review | Message 08 section 12; Complete_Sample_Script |
| Interaction schedule (3–4 predictions, 2–3 pauses, a prompt about every 75–120 s), humour ceiling (3–5 moments, under about 25 s), pacing (130–155 / 105–125 wpm), 1,100–1,250 words, twenty-script ledger window | "Production hypotheses", "editorial starting points", "not a scientific attention-reset interval" | Message 08 sections 4.2, 5.2, 9.3, 11.4; pack guide |
| Example jokes and the Hindi mnemonic "Naam wahi, ginti nayi; har atom ka hisaab sahi." | "Creative examples, not experimentally validated lines"; original, "not a mandatory catchphrase or a sourced quotation" | Message 08 section 5.1, 5.5; pack guide section 9 |
| Assamese prompt "এতিয়া নিজে চেষ্টা কৰি চোৱা।" ("Now try it yourself.") | "Drafted for native-speaker review"; do not release unreviewed | Message 08 section 5.5; pack guide section 9 |
| Analogy card `CHEM-COEFF-SANDWICH-01` | `DRAFT_HUMAN_REVIEW_REQUIRED` | `references/analogy_card.example.json` |
| Voice and TTS quality | Not auditioned; modern TTS "must be auditioned"; one study found no significant human-versus-synthetic difference "under its particular conditions" | Message 08 section 9.1; pack guide section 2 |
| Whether the style improves learning | Untested; pilot comparisons proposed (section 13); small student sessions find confusing wording but "are not sufficient to establish a modest statistical improvement" | Message 08 section 13; pack guide section 14 |
| Overall guide | "Original proposed production standard"; "not a validated intervention, a performed voice audition, or proof of improved examination scores" | Pack guide status line |
| Release | Nothing may release with an unresolved critical scientific claim, misleading analogy, humiliating line, incorrect answer, inaccessible essential symbol, deceptive personal response, missing rights or untested critical pronunciation | Pack guide section 15 |

## 7. Integrity checks the organiser performed

- `cp -R` of the pack: 45 files; `diff -r` source versus copy: identical.
- `prompt/` and `related/` files: `diff` against the source: identical.
- Pack `Super_Teacher_Guide.md` versus `00_source/downloads/ExamLeaf_Super_Teacher/Super_Teacher_Guide.md`: **identical**.
- Pack `examples/Complete_Sample_Script.md` versus `00_source/downloads/ExamLeaf_Super_Teacher/examples/Complete_Sample_Script.md`: **identical**.
- The ten `references/authoring_contract.md` files and the pack-level one: same MD5 (94af7c71e0b8a25beab739265d716e77).
- Sample script: the spoken narration of all 16 beats in message 08 equals the pack version (after ignoring curly versus straight quotes). Word total 1,225 and hold total 63 s recomputed from `sample_lesson.json`: both match the stated figures.
- `FULL_super_teacher_framework.md`: a line-level `diff` against the transcript file showed changes only on lines containing LaTeX or citation markers (plus the added header).
- Nothing under `00_source/` was modified. No Python from the pack was executed; no packages installed; no network calls.

## 8. Gaps, discrepancies and things to know

1. **Skill count.** The progress note (07a) says "14 draft Skills"; message 08 and the pack contain **ten**. No fourteen-skill set is in the sources.
2. **Citation markers.** The transcript export stripped the citation widgets but left opaque handles such as `turn783960search11`. They are preserved as `[cite: ...]` in the FULL file. They cannot be resolved to URLs from the sources alone; the inferred mapping to ledger entries is in section 9.
3. **Dead links.** Message 08's three "Ready-to-use materials" links point to `sandbox:/mnt/data/...`. Local equivalents are in `starter_pack/`.
4. **Tone vocabulary.** The pack's sample JSON uses tone `inviting`, which is not one of the five delivery modes (CURIOUS, STEADY, DELIBERATE, LIGHT, REASSURING) defined in the framework. Beat tones also differ slightly between the chat sample and the pack sample (listed in `SAMPLE_SCRIPT_balancing_chemical_equations.md`).
5. **Linter blind spot.** `tools/lint_script.py` flags `[BEAT`, `[THINK`, `[PAUSE_VIDEO`, `[VOICE`, `[TONE`, `[EMPHASIS`, `[REVEAL`, `[SMILE`, `[LAUGH`, `[SIGH` in spoken text but not `[CURIOUS]`, `[STEADY]`, `[DELIBERATE]`, `[LIGHT]`, `[REASSURING]`. Organiser's reading of the code, not a claim in the source.
6. **Not delivered by the source:** no audio, no rendered video, no student data, no native-speaker review of the Assamese or Hindi lines, no evaluated Skill runs, no second subject lesson (physics, maths and biology appear only as short example snippets in section 7 of the framework).
7. **Where the machinery lives.** The Skills here are the *authoring* layer. Rendering, voice synthesis and the engine's schema are in `04_video_engine/`, `05_narration_system/` and `07_end_to_end_pipeline_instructions/`.

## 9. Inferred map of the `[cite: ...]` markers to the Research Ledger

Inferred by matching the sentence each marker follows to the ledger entries (`starter_pack/.../references/Research_Ledger.md`). The sources do not state this mapping; treat it as a navigation aid, not a citation.

| Marker(s) in FULL file | Sentence topic | Likely ledger entry |
|---|---|---|
| `turn783960search11` | Conversational wording experiments (section 1.1) | P01 Mayer et al., 2004 |
| `turn783960search16` | 2026 video-humour study, 206 experts and 325 students (1.2) | P03 |
| `turn783960search20` | Humour review, mixed achievement (1.2) | P02 Zhou and Lee, 2025 |
| `turn439792search8` | Worked examples to independent problems (1.3) | P04 Atkinson, Renkl and Merrill, 2003 |
| `turn955193view4`, `turn955193view5` | Self-explanation and retrieval practice (1.4) | P05 and P06 (order not determinable) |
| `turn661037view0` | University Physics active-learning experiment (1.5) | P07 Deslauriers et al., 2019 |
| `turn144471search6` | Curiosity and memory (1.6) | P09 Gruber et al., 2014 |
| `turn870523search4` | Fixed attention-span claims (1.6) | P13 Bradbury, 2016 |
| `turn144471search15` | Select, organise, integrate (3.1) | P16 Mayer, 2024 |
| `turn755614search3` | Teaching with analogies (3.3) | P15 Glynn et al., 1994 |
| `turn755614search11` | Preschool prerecorded questions (4.1) | P10 Gaudreau et al., 2020 |
| `turn870523search3` | Irrelevant additions hinder learning (5.2) | P17 Kienitz et al., 2023 |
| `turn290870search0` | Eight Indian secondary English teachers (5.5) | P18 Anderson, 2024 |
| `turn661037view2` | Feedback meta-analysis (6.1) | P08 Wisniewski, Zierer and Hattie, 2020 |
| `turn809499view3`, `view0`, `view2`, `view1` | Physics doorway; chemistry coefficients (also section 12); maths chain rule; biology enzymes | S02, S01, S03, S04 (OpenStax) |
| `turn762447view5` | Modern TTS versus human voice (9.1) | P11 Dincer, 2022 |
| `turn955193view0` | 244 participants, synthetic voice enthusiasm (9.1) | P12 Liew et al., 2023 |
| `turn771459view2`, `turn762447view3` | ElevenLabs and Google SSML (9.4) | T05 and T06 |
| `turn290870view1` | Captioning as accessibility (9.4) | T07 W3C WCAG 2.2 |
| `turn771459view3`, `turn290870view0`, `turn762447view1`, `turn809499view4` | Claude Code Skills, Agent Skills standard, Codex Skills, skill-creator (11.1); first and third again for discovery paths (11.1 end) | T01 to T04 (one-to-one pairing not determinable) |
| `turn290870search2` | Spaced practice (13) | P14 Cepeda et al., 2006 |

## 10. Cross-references to the other sections

| Section | Relationship to this one |
|---|---|
| `01_business_model/` | Why the persona matters commercially: the book-linked model and positioning that this teacher voice serves. The pack's rule against sales-pitch endings (Master Authoring Prompt: "End with a useful, independent next task rather than a mastery claim or sales pitch") constrains how funnel calls-to-action may appear in scripts. |
| `02_learning_psychology/` | The wider learning-science blueprint (psychology of engagement, memory, confidence). This section applies it to the narrator; section 1 of the FULL file and `references/Research_Ledger.md` hold the evidence used here. |
| `04_video_engine/` | Consumes the lesson JSON and the Super Teacher contract (`related/Super_Teacher_Contract.md` is the engine-side encoding of this persona). |
| `05_narration_system/` | **Closest sibling.** Voice brief, five delivery modes, pacing targets, cue tags, pronunciation and TTS adapters. Pairs with `examleaf-voice-director` and FULL section 9. |
| `06_skills_library/` | **Closest sibling.** The consolidated Skills library; the ten Skills indexed in `SKILLS_INDEX_super_teacher_10.md` are the authoring-layer subset and should be reconciled there to avoid drifting duplicate copies. |
| `07_end_to_end_pipeline_instructions/` | The pipeline in which the production sequence (FULL section 11.2) runs from source packet to controlled release. |
| `08_cost_models/` | Per-video cost, including narration generation and review time; the Super Teacher's separate author and reviewer passes add model calls. |
| `09_research_and_evidence/` | Research ledger context and source verification; this section's ledger is P01–P18, S01–S04, T01–T07. |
| `10_pilots_and_examples/` | Pilot videos and the pilot comparison table (FULL section 13); the balancing-equations sample is the first worked example. |
