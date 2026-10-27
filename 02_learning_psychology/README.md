# 02_learning_psychology - evidence-based learning psychology for ExamLeaf videos

## 1. What this section is and where it came from

This section holds ExamLeaf's **learning-psychology and neuroscience blueprint**: how to make 10-minute STEM revision videos (Class 10-12, Assam Board) attention-friendly, confidence-building and actually effective, plus a complete **600-second Ohm's-law lesson blueprint**, a **prioritised A/B experiment plan**, and the **scene-level pedagogy fields** the Video Engine should store.

**Exact provenance (all unmodified in `00_source/`):**

| Item | Source file | ChatGPT message id (share `6acf03ec-b480-83ee-a000-3701059934d9`) |
|---|---|---|
| The request (8 focus areas, "extremely in-depth, evidence-based" brief) | `00_source/chatgpt_transcript/messages/03_USER_prompt_learning_psychology.md` | `0fe4d7a0-e1d1-42c0-9199-473780936955` (user) |
| Mid-research progress note | `00_source/chatgpt_transcript/messages/03a_ASSISTANT_progress_note.md` | `6be84c31-0ec1-490b-a044-145182dab712` (assistant) |
| **The answer: "ExamLeaf's learning psychology blueprint"** (13 sections, ~58K chars) | `00_source/chatgpt_transcript/messages/04_ASSISTANT_learning_psychology_blueprint.md` | `2efad524-72b6-41fd-9c62-3f5e7844d00b` (assistant) |
| Cross-checks only (not copied) | `00_source/extracted/ExamLeaf_Video_Engine_Planning_Pack/ExamLeaf_Video_Engine/design_tokens.json` (canonical design tokens); `00_source/extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/references/Research_Ledger.md`; `00_source/chatgpt_transcript/cited_source_links.md` | - |

**Nature of the material (the source's own caveat):** "This is a research synthesis and a proposed production standard - not evidence that ExamLeaf's exact format has already been validated." Many video-specific experiments involve university students rather than Indian secondary-school students, so precise settings need testing with the intended audience.

**Core standard in one line (source):** build each lesson around "One clear purpose, a small number of connected ideas, a stable visual model, explicit reasoning, meaningful student attempts, useful feedback, and a later opportunity to retrieve the learning." Optimise for a **sequence of successful mental actions - not uninterrupted watching.**

## 2. Every file in this directory

| File | What it is |
|---|---|
| `README.md` | This guide: provenance, file list, how-to-use steps, evidence labels, cross-references, gaps. |
| `FULL_learning_psychology_blueprint.md` | **Cleaned full text of message 04**, all 13 sections, every table, formula, number and quote kept (only 39 citation tokens removed and LaTeX turned into readable inline text; verified word-for-word). |
| `INSTRUCTIONS_production_rules.md` | Every actionable rule from the blueprint converted into checklists/specs (sections A-K): evidence categories, attention, cognitive load, palette and typography, captions, animation decisions and timing, interaction menu, pacing and pauses, confidence/feedback scripts, curiosity and spacing, individual differences, and a pre-release checklist. |
| `BLUEPRINT_600_second_ohms_law_lesson.md` | **Verbatim section 11**: the 41-beat, 600-second Ohm's-law / I-V graph lesson in three timed tables (00:00-03:30, 03:30-07:20, 07:20-10:00), learning targets, interaction design and the "why preferable" rationale; plus marked organiser cross-checks (interaction gaps, numbers, ambiguities). |
| `AB_EXPERIMENTS_and_EVALUATION.md` | **Verbatim section 12**: outcomes, the 9 prioritised experiments, design rules, sample-size figures (175 / 400 per group), confidence-calibration measurement; plus organiser notes. |
| `SCENE_PEDAGOGY_SCHEMA.md` | **Verbatim section 13**: the 12 scene fields, the 4 release-review questions, the recommended ExamLeaf standard; plus an organiser example scene record and field-to-rule trace. |
| `palette_and_typography_tokens.json` | Machine-readable palette (HEX, contrast ratios, dark variant), typography px, phone-readability formula, animation timing, interaction frequency, pacing wpm, pause lengths, spacing schedule, evaluation parameters; with `canonical_design_tokens_path` and a 13-item `differences_noted` array vs the canonical planning-pack tokens. |
| `SOURCE_CITATION_TRACE.md` | Record of the 39 citation markers stripped from the cleaned text (position, claim context, token IDs), distinct-ID counts, probable matches to the evidence ledger, and the list of claims with no listed source. |
| `prompt/03_USER_prompt_learning_psychology.md` | Verbatim copy of the user's research brief. |
| `prompt/03a_ASSISTANT_progress_note.md` | Verbatim copy of ChatGPT's progress note ("confidence will come from successful attempts plus specific feedback..."). |
| `prompt/README.md` | Explains the two prompt files and maps each of the 8 asked focus areas to the blueprint sections that answer it. |

## 3. How to use the material (step by step)

1. **Start with the standard.** Read `FULL_learning_psychology_blueprint.md` sections 0 (opening) and 13 (recommended standard), then skim `INSTRUCTIONS_production_rules.md` section A (evidence discipline) so you know which claims may and may not be made.
2. **Plan the lesson around one purpose.** Write the learning objective and prerequisites; identify which quantities change, which stay constant, and what the student must determine (`INSTRUCTIONS` B3).
3. **Fill the 12 scene fields for every beat** (`SCENE_PEDAGOGY_SCHEMA.md`): learning objective, prerequisite, scientific relationship, attention target, representation, learner action, available support, answer visibility, pause mode, feedback, misconception, delayed assessment.
4. **Choose learner actions.** Plan 2-3 substantial pause-to-write/solve activities and 3-4 brief predictions, about one invitation to think every 75-120 s, boundaries following the material (`INSTRUCTIONS` F1-F3). Give every substantial pause: what to produce, help available, when to resume, how to check, what to repair.
5. **Use the Ohm's-law blueprint as a template, not a straitjacket.** Copy its structure (hook with prediction -> model and condition -> formula -> reconstruct -> worked example -> completion step -> graph -> misconception -> boundary -> independent problem -> recall and draw -> calibrate -> next-day task) from `BLUEPRINT_600_second_ohms_law_lesson.md`. Per the source, a Biology process, Chemistry mechanism or difficult Class 12 derivation "should use the same principles without being forced into the identical timing pattern."
6. **Set visual design from the tokens.** Take colours and sizes from `palette_and_typography_tokens.json` (and `INSTRUCTIONS` D). **Before production resolve the typography-size conflict with the planning-pack `design_tokens.json`** (see section 6 below). Check every essential element at phone size with `Displayed size = Source size x (360 / 1920)`.
7. **Decide animation per concept** with the table in `INSTRUCTIONS` E1 (animate only what changes, in what order, in which direction, because of what). Aim for about 25-35% of runtime as substantial motion in first pilots; keep layouts stable 20-60 s or longer; use the timing defaults in E4; never alter a physical simulation to satisfy a timing rule; get the subject reviewer to check E5.
8. **Write narration** to 130-155 wpm (145-165 for recaps, 90-120 for dense new material), about 1,050-1,250 words per 10 minutes, with the pause lengths in G3; use the feedback table and *conditional* wording (H3); avoid the "avoid" list (H4); no background music under the core explanation.
9. **Run the release review.** Answer the four questions - Scientific, Instructional, Perceptual, Emotional - and tick `INSTRUCTIONS` section K. Automated checks may flag contrast, text size, clipping, reveal timing, missing units, absent captions and dense scenes; humans must judge scientific validity and learning.
10. **Close the loop after release.** Give students the spacing tasks (end of lesson, next day, about 3 days, about 1 week, later by exam timing) and run the experiments in `AB_EXPERIMENTS_and_EVALUATION.md`, starting with a small usability study and then one properly powered learning study (priority 1: explanation-only vs explanation plus retrieval and feedback; primary outcome = delayed unprompted assessment, initial delay 7 days).
11. **Before any marketing or product claim**, check it against the evidence-category table (`INSTRUCTIONS` A1): never claim colour, cliffhanger or fixed-interval-quiz effects on memory, never convert effect sizes into predicted mark gains, never treat completion as learning.

## 4. Evidence labels - exactly as the source states them

**The three internal categories (source section 1):**
- **Strong foundation:** "converging research supports the general practice."
- **Context-dependent:** "useful findings exist, but outcomes depend substantially on learners, material, implementation, or measurement."
- **Production hypothesis:** "a sensible starting specification that ExamLeaf should test, not a scientifically established optimum."

**Design decisions and their source verdicts:**

| Decision | Source label |
|---|---|
| Retrieval practice rather than only rewatching | **Strong foundation** |
| Revisit material across separate study occasions | **Strong foundation** |
| Segment complex explanations into meaningful units | **Strong foundation, implementation-dependent** |
| Worked examples, then reduce support | **Strong foundation for appropriate tasks** |
| Highlight the relevant part of a diagram or equation | **Strong foundation, when selective** |
| Replace all static diagrams with animation | **Not supported** |
| Insert a quiz at a particular fixed interval | **Production hypothesis** |
| A particular blue, green or background to improve memory | **Insufficient for that specific claim** |
| Increase confidence through repeated praise | **Insufficient as a stand-alone strategy** |
| Treat high completion rates as proof of learning | **Not justified** |

**How the source labels each numeric specification (do not upgrade these):**

| Specification | Source's own words |
|---|---|
| Palette (HEX values and contrast ratios) | "design specifications, not neuroscientific optima" |
| Typography px sizes | "pilot targets, not accessibility rules mandating a particular font size" |
| 25-35% substantial-motion budget | "untested starting budget, not a learning-science ratio" |
| Timing defaults (150-300 ms etc.) | "All are production hypotheses." |
| Interaction frequency (2-3 substantial + 3-4 brief; 75-120 s) | "This interval is a design hypothesis." |
| Interaction time ranges (e.g. 5-8 s prediction) | "proposed defaults, not experimentally established optima" |
| Narration wpm and pause lengths | "starting points for English-language pilots" / "Proposed starting ranges" |
| 1,050-1,250 word budget | "a reasonable initial writing budget" |
| Spacing schedule | "adjustable hypotheses" (no universal "1-3-7" sequence) |
| Ohm's-law second boundaries | "The exact second boundaries remain hypotheses." |
| Scientific-communication rules per subject | "proposed ... should be checked by the subject reviewer" |
| 7-day delayed test; sample sizes (175 / 400 per group) | "a study-design choice, not the only valid measure of retention"; "approximate planning calculations, not a power analysis for a finished study" |
| Do-not-sum effect sizes | "Do not add effect sizes from separate studies together or turn them into a predicted ExamLeaf exam-score improvement." |

## 5. Cross-references to other sections

| Section directory | How this section connects |
|---|---|
| `01_business_model` | Brand promise and any public claims must follow `INSTRUCTIONS` A1/A2/H4 (no "full marks guaranteed", no effect-size promises); honest label "10-minute revision video, with optional practice pauses"; the post-video practice and spacing tasks (I4) are the natural hook for book/practice links; the strongest brand promise in the source is "students can see what they understand, discover what still needs work, and become progressively more capable of answering without ExamLeaf beside them." |
| `03_super_teacher_framework` | The Super Teacher persona must obey the feedback rules (H3-H4), conditional wording, confidence calibration (H1), anxiety safeguards (H5), no identity praise, no constant excitement (G4). |
| `04_video_engine` | Scene fields (`SCENE_PEDAGOGY_SCHEMA.md`); design tokens and the conflict recorded in `palette_and_typography_tokens.json`; animation density/timing (E); learner-controlled "Continue to explanation" in the player (F7); captions and protected caption area (D7). |
| `05_narration_system` | wpm targets, pause lengths, intensity pattern, no core background music, feedback scripts, conditional wording, language validation (G, H3). |
| `06_skills_library` | Skills should embed the evidence tags, the four release-review questions and the checklist in `INSTRUCTIONS` K; automated checks per section 13. |
| `07_end_to_end_pipeline_instructions` | Apply sections: planning (B-C, I1), scene spec (12 fields), asset/animation (D-E), narration (G-H), release review (K), post-release (I4, A/B plan). |
| `08_cost_models` | Retrieval pauses and segmentation increase learning time (not media time); experiments require roughly 175 (d=0.30) or 400 (d=0.20) learners per group before attrition; narration word budget drives TTS volume. |
| `09_research_and_evidence` | Evidence ledger and cited URLs; `SOURCE_CITATION_TRACE.md` shows which blueprint claims map to which ledger entries and which have no listed source. |
| `10_pilots_and_examples` | The Ohm's-law blueprint is the reference pilot; the nine experiments are designed to run on pilot lessons. |

## 6. Gaps, ambiguities and conflicts (flagged, not resolved)

1. **Typography conflict.** Message 04: essential labels 88-96 px, equations 112-144 px, headings 104-128 px. Canonical planning-pack `design_tokens.json`: essential labels 64-72, equations 84-112, headings 72-88. The source's own formula gives 64 px -> ~12 px on a 360 px-wide phone. Also `equation_hold_ms` is 1000-3000 in the tokens vs 2-4 s ("longer when necessary") in message 04. Recorded in `palette_and_typography_tokens.json` -> `differences_noted`; the `04_video_engine` owner must decide. Palette HEX values and light-theme contrast ratios agree everywhere.
2. **Dark-theme accents undefined.** Only background `#101826` and text `#EAF0F6` (about 15.49:1) are given. The planning-pack tokens say other accents need separate validation; organiser re-computation shows the light accents would be only about 2.6-3.5:1 on the dark background.
3. **"Approximately seven persistent layouts"** are mentioned in section 11 but never enumerated, so beats cannot be mapped to layouts from the source alone.
4. **Graph values unspecified** in the Ohm's-law blueprint (second, steeper line has no stated resistance). Also the 8-second window for the calculate-and-predict step at 04:32-04:40 sits at the top of the source's own 5-8 s "simple prediction" range.
5. **Not literally second-by-second.** The brief asked for a second-by-second blueprint; the source gives 41 timed beats (8-20 s typical) and states second boundaries are hypotheses. Narration is excerpts only, not a full script.
6. **Reels are not covered.** The blueprint addresses the 10-minute video only; no pedagogy rules are given for Instagram Reels.
7. **Citations cannot be resolved one-to-one.** The transcript's cite tokens are not mapped to URLs; about 20 research claims have no listed URL (see `SOURCE_CITATION_TRACE.md`). The research numbers (222 studies, 48,478 students, g = 0.50; 56 investigations and 88 comparisons; March 2026 50-study g = -0.16; 195 and 703 student quiz studies) are carried as the source states them and were not independently verified. Only the palette contrast ratios, the dark-theme ratio, the phone-size arithmetic and the sample-size numbers (175 and about 393, source: roughly 400) were re-computed and agree.
8. **Evidence base is mostly university students**, and nothing is specific to Assam Board students or Assamese/Hindi narration; the source says other languages must be validated separately.
