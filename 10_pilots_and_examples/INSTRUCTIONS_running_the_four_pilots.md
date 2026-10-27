# INSTRUCTIONS - running the four pilots

**What this is.** A step-by-step working guide for the next validation gate of the ExamLeaf Video Engine: producing, reviewing, measuring and (only if every gate passes) releasing the **four full pilot lessons** (Physics, Chemistry, Mathematics, Biology). Quoted blocks (`>`) are copied verbatim from the cited ChatGPT message or from the engine's `Four_Pilots.md`; unquoted text is the organiser's wording and is marked **[SOURCE]** (restates a source) or **[PROPOSED]** (organiser's synthesis of the sources' gates, or a source's own unvalidated proposal). Provenance of every quote is in its heading.

**Verified vs proposed, stated exactly as the sources state it:**
- **Verified (ChatGPT sandbox, 13 Oct 2026):** four bounded science models, eight 30 s silent MP4s (re-checked in `PREVIEW_BENCHMARKS.md`), 56 passing tests.
- **Not done:** the four 600-second lessons. The `*_600s_plan.json` files are `blueprint_only` beat plans. No full script, no teacher-approved answers, no narration, no event alignment, no teacher approval, no student study exist. Browser playback of `preview.html`, HyperFrames/Remotion execution and agent evaluation of the Skills were not performed.
- Everything in sections 4-6 and 8-10 below is therefore a **procedure to execute**, not a record of something that has been run.

> **15 Oct 2026 addendum: vertical-only output (RD-16 superseded; audit M1).** ExamLeaf now publishes vertical only. In every pilot the **scored output is 1080×1920 (9:16) @ 30 fps**. A 16:9 render may still be made only as an **unscored smoke test** (does the scene build at all); it does not count toward any gate, measurement or compositor choice. **Renderer limit:** the proof renderer in `04_video_engine/implementation_v2` hard-codes 720×1280 for 9:16 (`pipeline.py:35`, `visuals.py:74`) and defaults its CLI to 16:9, so it cannot produce the scored 1080×1920 output until a 1080×1920 output mode is added (P1 build item). Use its 720×1280 output for layout checks only. For the compositor benchmark, follow `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md`, which is vertical-only. Verbatim source quotes below that mention 16:9 are kept as the sources wrote them.

---

## 1. Inputs you already hold (all inside this section)

| Need | File |
|---|---|
| Pilot plans and the four 30 s technical scenes | `pilots/` (`PILOT_PLANS_SUMMARY.md` lists every beat; `Four_Pilots.md` is the engine's own pilot document) |
| Full-length script format to imitate | `sample_scripts/SAMPLE_balancing_chemical_equations_full_script.md` (16 sections, 00:00-10:00); `sample_scripts/super_teacher_examples/` (`Complete_Sample_Script.md`, `sample_lesson.json`: 16 beats / 600 s) |
| Beat-by-beat interaction design to imitate | `sample_scripts/BLUEPRINT_ohms_law_600_seconds.md` (41 beats, three tables) |
| Narration direction and structured-narration examples | `sample_scripts/EXAMPLE_textbook_vs_teacher_narration.md`; `sample_scripts/narration_examples/` (`Before_After.md`, `claims.json`, `teacher.json`, `textbook.json`) |
| Rendered proof of the engine | `rendered_previews/` (8 MP4, captions, manifests, contact sheets); numbers in `PREVIEW_BENCHMARKS.md` |
| Offline narration-pipeline fixtures (NOT SPEECH) | `narration_outputs/` |

---

## 2. The four pilots

### 2.1 Pilot table [SOURCE] - message 10, section 9 (verbatim)

> # 9. Four complete pilot lessons: the next validation gate
>
> Do not stretch the technical clips to ten minutes. Build actual teaching sequences.
>
> | Pilot | Full-lesson objective | Critical validation |
> |---|---|---|
> | Physics | Interpret a changing circuit model and its graph | Conditions, units, numerical/display agreement; approve actual syllabus relevance before publishing |
> | Chemistry | Balance a fresh equation and explain coefficient versus subscript | No changed chemical identity; no implication that balance proves reaction feasibility |
> | Mathematics | Apply the chain rule to a new nested expression | Domains, visible reasoning, independent method selection |
> | Biology | Explain a monohybrid cross and distinguish probability from guaranteed counts | Genotype/phenotype distinction, explicit assumptions, no small-family guarantee |
>
> For each, record:
>
> **Academic defects, reviewer minutes, editing minutes, pronunciation repairs, render time, peak memory, accepted-asset generation attempts, total cost, and student performance on a fresh question.**
>
> Compare HyperFrames and Remotion using identical approved content, voice, fonts, frame counts, hardware, and concurrency. Record cold and cached performance separately.
>
> **A single critical scientific error should block release regardless of the overall visual score.**
>
> The planning document allows more academic and editorial effort for the first pilots than the mature per-video cost model. New components and first-use explanations should not be priced as if the library already existed.

### 2.2 Pilot table [SOURCE] - `pilots/Four_Pilots.md`, "Full narrated pilot objectives" (verbatim)

> | Subject | Proposed full pilot | Tests and traps | Independent outcome |
> |---|---|---|---|
> | Physics | RC charging as a technical benchmark; confirm Assam syllabus relevance before publishing | Initial condition, dimensions, one tau, KVL, numerical/analytic agreement; graph/counter match; no instant charge | Interpret a changed R/C case and identify the model conditions |
> | Chemistry | Balancing equations as Class 10 foundation / Class 12 repair | Fixed formulas, atom ledger, simplest ratios, no claim balance proves feasibility or mechanism | Balance a fresh simple equation and explain coefficient versus subscript |
> | Mathematics | Chain rule with nested functions | Assumptions/domains, symbolic and finite-difference check, visible inner derivative | Differentiate a new expression and justify the factors |
> | Biology | Monohybrid inheritance under explicit assumptions | Genotype vs phenotype, complete dominance, probability vs guaranteed counts | Explain a new cross and distinguish expected ratio from a small family outcome |
>
> Each *_600s_plan.json is only a beat plan. Complete scripts, teacher-approved answers, narration and event alignment still need producing. Do not stretch a 30-second fixture to ten minutes and call it a pilot.

### 2.3 What each plan JSON itself says [SOURCE] (read from `pilots/*_600s_plan.json`)

| Pilot id | Objective (JSON) | Prerequisites / assumptions (JSON) |
|---|---|---|
| `physics_rc_full_pilot` | Connect ideal RC charging to its graph and one-time-constant value. | Ideal linear resistor and capacitor; constant 10 V source. Capacitor initially uncharged. Model time is explicitly shown as t/(RC); not a footage timestamp. |
| `chemistry_balance_full_pilot` | Distinguish coefficients from molecular formulas and verify element counts. | Correct starting and product formulas are supplied. Counts are conserved for each element. Discrete schematic states are not a reaction mechanism or lab demonstration. |
| `mathematics_chain_full_pilot` | Differentiate a squared linear expression using the chain rule. | Real x; polynomial function. The tangent and displayed derivative share the same symbolic model. |
| `biology_genetics_full_pilot` | Distinguish genotype probabilities from guaranteed small-sample counts. | One Mendelian locus with two alleles and equal gamete probabilities. Random gamete union; complete dominance for phenotype mapping. Probabilities are not guaranteed counts in four offspring. |

All four share the same 11-beat, 600 s structure (curiosity 25 s, prerequisite 35 s, intuitive_model 60 s, formal_model 60 s, worked_example 90 s, micro_recap 45 s, guided_example 75 s, independent_practice 65 s, feedback 55 s, exam_conversion 50 s, confidence_and_spacing 40 s), `board_mapping_status = pending current syllabus and ExamLeaf source review`, `audio_status = not_generated`, `mandatory_reviews = academic, full_render, native_language_when_localized`, and `success_measures = zero critical science errors; full timed voice listen; mobile visual review; independent item; delayed retrieval; measured human_minutes; measured generation_and_render_cost`.

---

## 3. Before you start

1. **[SOURCE]** Treat every `*_600s_plan.json` as a plan only. The engine's `batch` command accepts only the four scene JSONs and ignores `*_600s_plan.json` (implementation README); the test `test_plans_total_600` only checks that each plan's beat durations sum to 600 and that `status == blueprint_only`.
2. **[SOURCE]** Use the right scope: the Chemistry pilot is "Class 10 chemistry / Class 12 prerequisite repair; not a Class 12 chapter pilot"; the Physics RC lesson is a "Class 12 circuit-model technical benchmark; board coverage is not yet approved" (scene JSON `class_context`).
3. **[SOURCE]** Plan the human time. `Four_Pilots.md`, "Work/time planning, not measured":

> Budget 8-16 academic/editorial hours per initial full lesson plus shared component engineering, then measure reductions with reuse. The mature cost model assumes 85 hybrid human minutes per video; that is not a promise for first-time bespoke lessons. Four full pilots require a separate, explicit reviewer schedule and no publishing deadline should bypass it.

---

## 4. Step-by-step procedure, repeated for each pilot

The order is a **[PROPOSED]** synthesis of the gates in `Four_Pilots.md`, message 10 (sections 9 and 13), message 02 (sections 12 and 14) and `docs/Production_Runbook.md`. The content of each step is from the cited source.

| Step | Do this | Gate to pass before moving on | Source |
|---:|---|---|---|
| 1 | **Fix curriculum scope and sources.** Replace `board_mapping_status: pending...` with a recorded current Assam-board syllabus version, class and chapter; copy the OpenStax `sources`/`claims` from the scene JSON into the source/claim ledger, mark rights, and have an ExamLeaf source review. Physics: confirm syllabus relevance before publishing. | Reviewers agree on what a correct lesson is (roadmap phase A / phase 0). | `Four_Pilots.md`; message 02 section 14 phase A; message 10 section 13 phase 0 |
| 2 | **Author the complete script** from the 11 beats (each beat's `task` field is the brief; 25-90 s per beat). Use the Super Teacher structure: approachable problem, reveal relationship, demonstrate reasoning, hand over part of the work, check an independent attempt. Keep spoken text free of directions; put holds, tone and visuals in separate fields (see the full sample and `sample_lesson.json`). | Every beat moves from `requires_authoring_and_review` to authored. | `sample_scripts/` examples; message 08 sections 10-12; message 12 section 9 |
| 3 | **Produce at least one original fully solved example and one independent transfer item per lesson**, with an independent re-solution including boundary cases. | Answers independently verified. | `Four_Pilots.md` acceptance gates; message 02 section 12 |
| 4 | **Academic approval (first of two).** Reviewer checks claims, scope, explanations, notation, worked examples and scientific visuals. | Zero unresolved critical scientific errors. | message 02 section 12 |
| 5 | **Narration.** Build/extend the versioned STEM pronunciation test corpus; generate speech; run native review per language; align the script to the measured waveform; place visual events on the alignment; insert true silence for thinking pauses and make the practice pauses learner-controlled. | Correct pronunciation of the corpus; full timed voice listen done. | `Four_Pilots.md` acceptance gates; `docs/Production_Runbook.md` step 7; `05_narration_system` |
| 6 | *(15 Oct 2026: **render 1080×1920 (9:16) @ 30 fps as the scored output**; 16:9 only as an unscored smoke test; the proof renderer stops at 720×1280, see the addendum above.)* ~~Render both 16:9 and 9:16~~ (vertical is recomposed, not cropped) from typed scientific state so that diagram, equation, graph and counters consume the same data; a parameter change must invalidate the dependent assets. | Same data drives all representations. | `Four_Pilots.md`; message 10 section 10.1; `test_vertical_not_crop` |
| 7 | **Compositor comparison**: run the HyperFrames vs Remotion protocol in section 6 on the approved content. | Real numbers recorded; no extrapolation from the SVG proof. | `Four_Pilots.md`; message 10 section 9 |
| 8 | **Final production approval (second of two).** Watch the entire rendered lesson, including narration, synchronisation, captions and mobile readability on representative small phones. Sampling frames supports QA but does not replace watching the whole video. | Diagram, equations, captions and text readable on small phones; genuine learner-controlled practice pauses. | message 02 section 12; `Four_Pilots.md` |
| 9 | **Record the per-pilot measurements** (section 5) for every pilot, including the failed attempts. | Sheet complete for the pilot. | message 10 section 9 |
| 10 | **Apply the release rule** (section 8). | No critical scientific error remains. | message 10 section 9 |
| 11 | **Evaluate learning** (section 10): fresh question, delayed retrieval, confidence calibration. Start with a small usability study, then a properly powered learning study on the most consequential design decision. | Delayed learning and calibration measured separately from retention/watch time. | message 04 section 12; message 08 section 13; `Four_Pilots.md` |
| 12 | **Decide.** Choose the compositor only after cost including human repair is compared. Promote the engine to production status only after four complete pilots demonstrate correct science, clear teaching, reliable synchronisation, manageable human effort and defensible costs. | Then move to a controlled batch of 20-30 (message 10) or ~30-50 (message 02) lessons. | `Four_Pilots.md`; message 10 final decision |

---

## 5. What to record for each pilot

[SOURCE] Message 10, section 9: "For each, record: **Academic defects, reviewer minutes, editing minutes, pronunciation repairs, render time, peak memory, accepted-asset generation attempts, total cost, and student performance on a fresh question.**"

| # | Metric | What to log | Suggested unit [PROPOSED] | Notes from the sources |
|---:|---|---|---|---|
| 1 | Academic defects | Every defect found by academic review, with severity (Critical / Major / Minor) | count per severity | A single critical scientific error blocks release. Severity classes come from `docs/Production_Runbook.md` and are summarised in section 8 of this file. |
| 2 | Reviewer minutes | Time spent by academic and full-video reviewers | minutes | The plan JSON's `success_measures` calls this `measured human_minutes`. |
| 3 | Editing minutes | Time spent editing script, scenes, captions after review | minutes | Same `human_minutes` measure. Mature model assumes 85 hybrid human minutes per video; first-time pilots are budgeted at 8-16 academic/editorial hours. |
| 4 | Pronunciation repairs | Number of spoken-term fixes against the versioned STEM test corpus | count (and per language) | Native review per language. |
| 5 | Render time | Wall time per render, first build vs cached build | seconds | The only timings that exist are the eight 30 s proofs (27.3-29.4 s, two workers). Do not extrapolate. |
| 6 | Peak memory | Peak resident set size (RSS) of the render | MB | Not measured anywhere so far. |
| 7 | Accepted-asset generation attempts | Attempts per accepted generated asset (audio/illustration) | attempts per accepted asset | Runbook cost section: "attempts per accepted asset", "accepted generated seconds". |
| 8 | Total cost | Provider spend + machine + human time | currency | `measured generation_and_render_cost`. "Machine cost is not total cost." The local proofs had `invoice_cost_usd = 0.0`; 9 Runway workspace credits were debited for the one speech probe, not converted to USD. |
| 9 | Student performance on a fresh question | Result on an unseen item immediately and later | % correct, with confidence rating | See section 10. |

### 5.1 Blank recording sheet (copy per release candidate)

| Metric | Physics `physics_rc_full_pilot` | Chemistry `chemistry_balance_full_pilot` | Mathematics `mathematics_chain_full_pilot` | Biology `biology_genetics_full_pilot` |
|---|---|---|---|---|
| Academic defects (Critical / Major / Minor) | | | | |
| Reviewer minutes | | | | |
| Editing minutes | | | | |
| Pronunciation repairs | | | | |
| Render time - first build (s) | | | | |
| Render time - cached (s) | | | | |
| Peak memory (MB) | | | | |
| Accepted-asset generation attempts | | | | |
| Total cost | | | | |
| Fresh-question performance (immediate) | | | | |
| Fresh-question performance (delayed) | | | | |
| Confidence calibration (2x2 counts) | | | | |
| Full timed voice listen done (Y/N) | | | | |
| Mobile visual review done (Y/N) | | | | |
| Academic approval (name/date/artifact hash) | | | | |
| Final production approval (name/date/artifact hash) | | | | |

---

## 6. HyperFrames vs Remotion comparison protocol

[SOURCE] `pilots/Four_Pilots.md`, "Compare the shortlisted browser compositor" (verbatim):

> Render identical approved scenes in HyperFrames and Remotion: 16:9 + 9:16, same fonts/content/audio/frame count, same hardware and concurrency. Use a warm-up then at least five measured repeats per configuration. Record first-build and cached build separately; measure peak RSS, CPU/GPU usage, wall time, file size, repairs and visual differences. Do not extrapolate the simple native SVG timings as browser-engine benchmarks.

[SOURCE] Message 10 section 9 (verbatim): "Compare HyperFrames and Remotion using identical approved content, voice, fonts, frame counts, hardware, and concurrency. Record cold and cached performance separately." Message 02 phase B: "Identical HyperFrames and Remotion scenes, including equations, SVG biology, graphs, captions, and audio" with the gate "Compare real correctness, memory, timing, repair effort, and cost". Message 10 phase 1: port the four golden fixtures to audited HyperFrames and Remotion environments and "Choose using correctness, reliability, repair time, and cost". `Four_Pilots.md`: "Choose the compositor only after cost including human repair is compared."

**Procedure [PROPOSED layout of the source's rules]**

1. Freeze one approved scene set per pilot (same fixture JSON, text, equations, fonts, audio file and frame count) and record its hash.
2. Use one machine and one concurrency setting for both compositors; write them down.
3. For each of the 2 compositors at **1080×1920 (9:16) @ 30 fps** (the scored configuration; *15 Oct 2026, was "x 2 aspect ratios (16:9, 9:16)"*): do one warm-up run, then at least 5 measured repeats. A single 16:9 run per compositor is allowed as an unscored smoke test and is not entered in the grid.
4. Log cold (first build) and cached builds separately.
5. For each run capture: wall time, peak RSS, CPU/GPU usage, output file size, number of repairs needed, and visual differences (compare against the approved scene).
6. Compare correctness first (any scientific or visual error is a failure), then reliability, then repair effort and cost including human repair time.
7. Do not use the 27-29 s native-SVG proof timings as a baseline for a browser engine.

**Recording grid**

| Pilot | Compositor | Aspect | Cold wall (s) | Cached wall (s) | Repeats (>= 5) | Peak RSS (MB) | CPU/GPU | File size | Repairs | Visual differences |
|---|---|---|---|---|---|---|---|---|---|---|
| (each of 4) | HyperFrames | 9:16, 1080×1920 @ 30 fps | | | | | | | | |
| (each of 4) | Remotion | 9:16, 1080×1920 @ 30 fps | | | | | | | | |

*(15 Oct 2026: the 16:9 rows were removed from the scored grid; record any 16:9 smoke test as a note only.)*

---

## 7. Do not stretch technical clips to ten minutes

[SOURCE] Message 10 section 9: "Do not stretch the technical clips to ten minutes. Build actual teaching sequences." `Four_Pilots.md`: "Do not stretch a 30-second fixture to ten minutes and call it a pilot." Also, from the same document, "Four actual narrated lessons near the pedagogically appropriate duration; exact ten minutes is not mandatory." and message 02 section 8: "Ten minutes is a format target, not a scientific law" (do not stretch a six-minute idea, and do not compress a hard chapter by speaking faster).

---

## 8. Release rule and acceptance gates

[SOURCE] Message 10 section 9: "**A single critical scientific error should block release regardless of the overall visual score.**" Message 02 section 12: every released lesson needs two human approvals (academic approval; final production approval of the entire rendered lesson).

**Acceptance gates** - `pilots/Four_Pilots.md` (verbatim):

> - Zero unresolved critical scientific errors; separate academic and full-video production approval.
> - Four actual narrated lessons near the pedagogically appropriate duration; exact ten minutes is not mandatory.
> - Correct pronunciation of a versioned STEM test corpus and native review per language.
> - Diagram, equations, captions and text readable on representative small phones, with genuine learner-controlled practice pauses.
> - Same data drives simultaneous representations; parameter changes invalidate dependent assets.
> - Retry/cancel/resume, rate limits, cost caps, expiring assets and duplicate-job prevention tested against real staging APIs.
> - At least one original fully solved and one independent transfer item per lesson. Measure delayed learning and confidence calibration separately from retention/watch time.
> - Choose the compositor only after cost including human repair is compared. No overall quality score may hide a critical scientific error.

**What "critical" means** [SOURCE, `docs/Production_Runbook.md`, QA severity]: Critical = wrong science/answer/condition, misleading visual, unlicensed asset, missing critical text/audio, unauthorized data/spend (blocks release). Major = poor pronunciation, unreadable essential label, distracting pacing, caption error changing meaning, answer revealed too early (repair and re-review). Minor = cosmetic timing/alignment issue without learning impact (track it).

**Current machine-enforced block [SOURCE].** The release check must currently block, and that is correct behaviour because the previews lack narration and genuine academic/full-video approval:

```sh
PYTHONPATH=src python -m examleaf.cli release-check outputs/physics_rc_16x9.mp4 outputs/physics_rc_16x9.manifest.json
```

(Linux reference environment; not run here. Do not bypass it by fabricating reviewer identities; the implementation README says production needs an authenticated approval service.) Every manifest currently carries `release_status: blocked_pending_audio_and_expert_review`.

---

## 9. What ChatGPT proposed building first (message 02, section 14) - [SOURCE, unvalidated proposal]

> ## 14. Practical implementation roadmap
>
> | Phase | Build | Gate before proceeding |
> |---|---|---|
> | **A. Scientific and design contracts** | Source/rights ledger, syllabus records, LessonSpec, SceneSpec, design tokens, negative tests | Reviewers agree on what constitutes a correct lesson |
> | **B. Renderer benchmark** | Identical HyperFrames and Remotion scenes, including equations, SVG biology, graphs, captions, and audio | Compare real correctness, memory, timing, repair effort, and cost |
> | **C. Core reusable library** | Equation steps, coordinate graphs, vectors, circuits, molecular diagrams, biological process states, worked-example layouts | Components pass scientific and visual regression tests |
> | **D. Eight pilot lessons** | One lesson per subject strand and class level | Teacher approval, voice audition, small-phone readability, student feedback |
> | **E. Controlled batch** | Approximately 30–50 lessons with orchestration, caching, cost limits, and review queues | No unresolved critical errors; repair/review time and cost are predictable |
> | **F. Bulk production** | Larger queues, more reviewers, localization, selective 3D | Stable quality gates and evidence of independent learning |
> | **G. Continuous evaluation** | Delayed quizzes, transfer items, confidence calibration, controlled template improvements | Changes improve learning or accessibility—not merely watch time |
>
> ### What I would build first
>
> The first engineering milestone should be a **single complete, scientifically reviewed lesson**, not an elaborate dashboard.
>
> A good Physics pilot is drift velocity and current: it tests equations, units, diagrams, opposite electron/current directions, narration of symbols, parameter changes, and a worked example.
>
> A Biology pilot should then test a process with explicit state and count changes. That exposes problems a mathematics-only demo will miss.

Note the difference between the two proposals: message 02 (v1) suggested a **drift-velocity physics** pilot and then a **biology process** pilot, and **eight pilot lessons** (phase D). Message 10 (v2) then built technical proofs for **RC charging, atom balancing, chain rule and a monohybrid cross** and set the **four** pilots in section 2 as the next gate. Neither suggestion has been executed; the four-pilot gate in message 10 is the more recent one. Message 10's own roadmap (section 13, verbatim table):

> | Phase | Build | Gate |
> |---|---|---|
> | **0 — contracts and academic scope** | Review source rights, syllabus mapping, claim structure, design tokens, voice corpus | Academic owners agree on the definition of correctness |
> | **1 — compositor selection** | Port the four golden fixtures to audited HyperFrames and Remotion environments | Choose using correctness, reliability, repair time, and cost |
> | **2 — audio and four full pilots** | Implement TTS lifecycle, actual forced alignment, pronunciation review, full scripts and exercises | Four complete, reviewed lessons—not expanded silent previews |
> | **3 — controlled batch** | Durable orchestration, provider failure recovery, object storage, reviewer workflow | Twenty to thirty lessons with measured costs and defects |
> | **4 — scalable production** | Expand validated components, subjects, languages, and worker capacity | Stable quality gates and evidence of independent learning |
>
> A reasonable planning sequence is several weeks of dedicated engineering and available subject review—not a promise that installing Skills completes the system.

---

## 10. Learning-outcome measures and the evaluation studies

### 10.1 The four measures [SOURCE]

Measure **(1) immediate understanding, (2) a fresh application, (3) delayed retrieval** (message 08 section 13), and **(4) confidence calibration**. Message 04 section 12.1 (verbatim):

> ## 12.1 Choose learning outcomes before choosing variants
>
> The recommended primary outcome is:
>
> > **Performance on a delayed, unprompted assessment containing unfamiliar but curriculum-aligned applications.**
>
> A practical initial delay is seven days; that interval is a study-design choice, not the only valid measure of retention.
>
> Secondary outcomes should include immediate understanding, task completion without hints, confidence calibration, total study time, listening effort, and voluntary return to useful practice.
>
> Watch time should remain a diagnostic measure.

**Confidence calibration, 2 x 2** - message 08 section 13 lists the four cells and message 04 section 12.5 explains what to do with them. The arrangement into a grid is the organiser's [PROPOSED] layout of the four listed outcomes:

| | Student said "confident" | Student said "uncertain" |
|---|---|---|
| **Answer correct** | Correct and confident (accurate confidence) | Correct but uncertain (excessive uncertainty) |
| **Answer incorrect** | Incorrect but confident (**high-confidence error**) | Incorrect and uncertain (listed in message 08 section 13 without a name) |

Message 04 section 12.5 (verbatim):

> ## 12.5 Measure confidence calibration—not merely confidence increases
>
> At selected checkpoints, ask students to estimate whether their answer is correct before seeing feedback.
>
> Then distinguish:
>
> **Accurate confidence**, **high-confidence errors**, and **correct answers accompanied by excessive uncertainty**.
>
> A variant that makes students feel highly confident while increasing errors should lose—even when they prefer it.
>
> Conversely, a useful variant should not unnecessarily leave successful students believing they are incapable.

### 10.2 Super Teacher pilot comparisons - message 08, section 13 (verbatim)

> # 13. How to establish whether this style works for ExamLeaf
>
> Do not evaluate the sample only by asking:
>
> > “Was the teacher fun?”
>
> That is useful feedback, but not the primary outcome.
>
> ## Recommended pilot comparisons
>
> | Experiment | Compare | Main outcome |
> |---|---|---|
> | Conversational wording | Formal versus conversational versions with equivalent science | Independent application |
> | Relevant humour | No humour versus a few concept-linked lines | Delayed learning, comfort, distraction |
> | Support reduction | Full examples throughout versus faded support | Method selection without hints |
> | Delivery | Steady warmth versus more variable enthusiasm | Comprehension and listening effort |
> | Language | Audience-appropriate language versions | Understanding, terminology recall, comfort |
>
> Keep content, difficulty, and study-time differences visible. Predefine the outcome before choosing a winner.
>
> Measure immediate understanding, a fresh application, and delayed retrieval. Spaced practice has a substantial evidence base, but the precise follow-up interval should reflect the intended retention goal rather than a universal schedule. citeturn290870search2
>
> Also inspect **confidence calibration**:
>
> - Correct but uncertain.
> - Correct and confident.
> - Incorrect and uncertain.
> - Incorrect but confident.
>
> A version that makes students feel brilliant while producing more confident errors should lose.
>
> Small student sessions are excellent for finding confusing wording, cringe humour, unreadable diagrams, or inadequate pauses. They are not sufficient to establish a modest statistical improvement in learning.

### 10.3 Narration benchmark studies A, B, C - message 12, section 14 (verbatim)

> # 14. Benchmark the voice before making it the brand
>
> Run three separate studies.
>
> ## A. Voice/provider audition
>
> Use identical passages, normalized playback levels, blinded provider names, and rotated order.
>
> Include connected explanations—not only isolated impressive sentences.
>
> The corpus should cover numbers, units, negation, scientific conditions, formula reading, Indian names, code-switching, a question, a correction, and a restrained joke.
>
> Use native teachers and language editors to identify **meaning-changing defects**, and students to rate clarity, listening effort, warmth, dignity, and preference.
>
> ## B. Script-style comparison
>
> Hold the science and study opportunity comparable. Compare a straightforward explanation with the Super Teacher version.
>
> The two Runway demonstrations produced here are useful for discussion, but **not** sufficient for a causal conclusion because several variables changed together.
>
> ## C. Learning evaluation
>
> Measure an independent question immediately and a fresh question later.
>
> Do not use preference, voice similarity, completion rate, or apparent confidence as the primary learning outcome.
>
> Use short listening panels first to find obvious problems, then a properly designed study for claims about learning effectiveness. A small panel is not enough to establish a modest examination-performance advantage.

### 10.4 Experiment design cautions [SOURCE, message 04 section 12]

Message 04 section 12.2 prioritises nine A/B comparisons (explanation-only vs explanation plus retrieval and feedback first; fading; checkpoint frequency; static vs animated; ~130 vs ~150 wpm; specific vs generic feedback; learner-controlled pause vs automatic reveal; copying vs reconstruction; two accessible palettes). Section 12.3: randomise, record prior knowledge, class level, language proficiency and device conditions; decide content-matched vs time-matched; use parallel test items; score with a predefined rubric, ideally blind; predefine the main outcome and analysis; minimal data and age-appropriate permission for minors. Section 12.4: a small group finds usability problems (e.g. an unreadable graph label) but cannot establish a modest learning advantage; as an *illustrative* calculation about 175 learners per group (standardised difference 0.30, 80% power, 5% two-sided) or about 400 per group (0.20) before attrition. The two Runway auditions in the narration pack differ in wording, length and expressive instructions, so they are **not** a controlled A/B experiment.

---

## 11. Opening `preview.html` locally

`rendered_previews/preview.html` is the engine's review page: eight `<video>` players (4 subjects x 16:9 / 9:16), each with a poster frame, an English WebVTT caption track and links to its verification manifest and MP4. It contains no scripts and no external URLs. **ChatGPT could not validate it** (browser smoke test blocked by administrator policy; see `PREVIEW_BENCHMARKS.md` section 7); the supplied page was not browser-tested in the source.

**Path caveat.** In the original repository the page sits one level above an `outputs/` folder and refers to files as `outputs/<name>`. In this section the page and the files sit side by side, so the original page would show broken players. Two options:

**Option A - use the path-fixed copy (recommended).** `rendered_previews/preview_local.html` was created by the organiser: it is `preview.html` with only the `outputs/` prefix removed from the 32 file references (verified that every one resolves to an existing file; no other change). Run from a terminal:

```sh
cd "<ROOT>/10_pilots_and_examples/rendered_previews"
python3 -m http.server 8000 --bind 127.0.0.1
# then open  http://127.0.0.1:8000/preview_local.html   in a browser
```

(`python -m http.server 8000 --bind 127.0.0.1` is the exact command given in the source; on macOS `python3` is usually the right executable. Stop the server with Ctrl+C. Not executed by the organiser.)

**Option B - recreate the original layout and use the untouched `preview.html`.**

```sh
mkdir -p ~/examleaf_preview && cd ~/examleaf_preview
cp -R "<ROOT>/10_pilots_and_examples/rendered_previews" outputs
cp outputs/preview.html .
python3 -m http.server 8000 --bind 127.0.0.1
# then open  http://127.0.0.1:8000/preview.html
```

**Option C - no server.** Double-click any `.mp4` (H.264 High profile, yuv420p, 30 s, 24 fps, silent; see `PREVIEW_BENCHMARKS.md` section 3) in QuickTime, VLC or a browser; open the two contact-sheet JPGs and the `*_opening/question/answer/recap.png` frames directly. Captions are the `.vtt` files (VLC can load them as subtitles). Expect **no audio** - the previews are silent by design.

---

## 12. Re-running the engine (optional, from the source README)

[SOURCE] The reference environment is Linux with Python 3.13.5; the implementation README says a macOS/Windows port must configure the equivalent DejaVu font path in `visuals.py` and re-run the tests, and that FFmpeg/ffprobe, Cairo and DejaVu Sans must come from trusted OS package channels. The organiser did not run or install anything. The commands (implementation repository root, not this folder):

```sh
python -m venv .venv
python -m pip install -e '.[chemistry,test]'
PYTHONPATH=src python -m examleaf.cli validate examples/physics_rc.json
PYTHONPATH=src python -m examleaf.cli batch --workers 2
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m examleaf.cli render examples/chemistry_balance.json --aspect 9:16 --out outputs
```

*15 Oct 2026: always pass `--aspect 9:16` (the CLI defaults to 16:9). The proof renderer outputs at most 720×1280 for 9:16, not the scored 1080×1920; treat its output as a layout check only until the 1080×1920 mode exists.*

The engine itself lives in `04_video_engine/`; see that section for architecture, schemas and the 32 Skill drafts.

---

## 13. Cross-references

| Topic | Section |
|---|---|
| Why the lesson is shaped this way (attention, cognitive load, retrieval, calibration); the Ohm's-law 600 s blueprint's source | `02_learning_psychology/` |
| Teacher personality, interaction loop, complete balancing script, pilot comparisons | `03_super_teacher_framework/` |
| Engine architecture, schemas, Skills, compositor decision, implementation README and runbook | `04_video_engine/` |
| Voice identity, provider requests, pronunciation lexicon, alignment, mastering, benchmark studies | `05_narration_system/` |
| Overall end-to-end production procedure these pilots plug into | `07_end_to_end_pipeline_instructions/` |

---

## 14. Gaps to close before the pilots can start

- No complete script exists for any of the four 600 s lessons (the balancing-equations script in `sample_scripts/` is a full chemistry script produced in message 08 and is the only one; it is also an *unrendered draft*: `status UNRENDERED_DRAFT`, `academic_review PENDING_HUMAN_REVIEW`, `timing_status PLANNED_NOT_AUDIO_MEASURED`).
- Assam-board syllabus mapping is `pending` in all four plans; the Physics RC lesson in particular needs a relevance decision.
- No audio has been imported into any MP4; the one Runway speech result (32.18 s, 9 credits) was never downloaded.
- HyperFrames/Remotion have not been installed or benchmarked; no peak-memory or cold/cached numbers exist.
- No teacher approval, no student testing, no native-language (Assamese/Hindi) review.
- The two "first pilot" ideas in message 02 (drift velocity; a biology process) differ from the four in message 10; decide whether they join the four or become the later eight-lesson phase.
