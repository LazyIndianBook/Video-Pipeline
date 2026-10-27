# INSTRUCTIONS - production rules extracted from the learning-psychology blueprint

**Source:** every rule below is converted from `FULL_learning_psychology_blueprint.md` (ChatGPT message 04). Section numbers in brackets, e.g. `[s2.3]`, point to the blueprint section. Wording of numbers, thresholds and quoted scripts is kept exactly as the source gives it. Nothing here is new research; where the organiser added anything it is marked **(organiser)**.

**How to use this file:** treat each `- [ ]` line as a testable requirement when writing a lesson plan, scene spec, narration script, or release review. Do the pre-release checklist in section K last. The source's own caveat applies to the whole file: *this is a research synthesis and a proposed production standard, not evidence that ExamLeaf's exact format has already been validated; many video experiments involve university students rather than Indian secondary-school students, so precise production settings need testing with your audience.*

## Legend - evidence tags (source's own labels, kept literally)

| Tag | Meaning in the source |
|---|---|
| **[Strong foundation]** | "converging research supports the general practice." |
| **[Context-dependent]** | "useful findings exist, but outcomes depend substantially on learners, material, implementation, or measurement." |
| **[Production hypothesis]** | "a sensible starting specification that ExamLeaf should test, not a scientifically established optimum." |
| **[Proposed]** | The source's word for its own design rules/specs (e.g. "Proposed rule", "Proposed palette", "proposed defaults"). Treat as Production hypothesis. |
| **[Recommendation]** | Stated by the source as a recommendation or accessibility practice without a separate evidence label. |
| **[Not supported / Insufficient / Not justified]** | Source's negative verdicts: things the pipeline must NOT claim or do. |

Source rule of thumb behind all tags: *"Make information easy to perceive and understand. Do not make every learning activity effortless."* (reading a legible diagram should be easy; reconstructing its explanation from memory may require productive effort.) [s0]

Target student experience the whole standard serves [s0]: *"I know what I am trying to understand. I can follow the explanation. I can attempt the next step. I can identify and correct my mistake. I can now solve something without the video."*

Recommended lesson shape for the fast-track revision format [s0]: a **visually stable, conversational lesson with purposeful animation, several brief predictions, two or three substantial practice pauses, specific corrective feedback, and follow-up retrieval outside the video.**

---

## A. Evidence discipline

### A1. Evidence-category table (how each design decision may be justified) [s1]
Use it as a claims filter: before writing any claim into a script, description, landing page or reel, find its row.

| Design decision | Evidence assessment | What ExamLeaf should conclude |
|---|---|---|
| Include retrieval practice rather than relying exclusively on rewatching | **Strong foundation** | Require students to retrieve or apply information before showing the answer. |
| Revisit material across separate study occasions | **Strong foundation** | Build practice after the video, not just repetition within it. |
| Segment complex explanations into meaningful units | **Strong foundation, implementation-dependent** | Separate conceptual steps and allow processing time. No universal segment duration is established. |
| Use worked examples, then reduce support | **Strong foundation for appropriate tasks** | Move from demonstrated reasoning toward independent problem-solving. |
| Highlight the relevant part of a diagram or equation | **Strong foundation, when selective** | Direct attention; do not highlight everything. |
| Replace all static diagrams with animation | **Not supported** | Animate when change, movement, or transformation is part of what must be understood. |
| Insert a quiz at a particular fixed interval | **Production hypothesis** | Useful checkpoints need testing; there is no established "reset attention every 90 seconds" law. |
| Choose a particular blue, green, or background to improve memory | **Insufficient for that specific claim** | Choose colours for legibility, meaning, consistency, and tested comfort. |
| Increase confidence through repeated praise | **Insufficient as a stand-alone strategy** | Build confidence through evidence of competence and useful feedback. |
| Treat high completion rates as proof of learning | **Not justified** | Measure delayed recall, transfer, and independent performance. |

Checklist:
- [ ] Every pedagogical claim in a script or marketing line maps to a row above or to a row in `09_research_and_evidence`; none relies on "popularity of particular educational channels" (the source grounds retrieval, segmentation, signalling and worked-example advice in research syntheses and experiments, not channel popularity). [Strong foundation]
- [ ] Never say or imply that a colour, background, cliffhanger or fixed-interval quiz *causes* memory/attention gains. [Insufficient / Production hypothesis]
- [ ] Never treat completion rate, watch time or views as proof of learning; they are diagnostic only. Measure delayed recall, transfer and independent performance. [Not justified]

### A2. Effect-size rules [s1]
- [ ] Retrieval practice (classroom testing meta-analysis: 222 studies, 48,478 students, average g ~ 0.50) is a serious instructional tool, but effects "varied with feedback, question format, comparison activity, repetition, and other factors." **It does not mean "50% higher marks."** [Context-dependent]
- [ ] Interesting-but-irrelevant details: a meta-analysis published March 2026, 50 studies, small average negative effect, g = -0.16. Use it to argue against unnecessary decoration, not against attractive design.
- [ ] **Do not add effect sizes from separate studies together or convert them into a predicted ExamLeaf exam-score improvement.** (No "improves marks by X%" claims anywhere.)

---

## B. Attention, working memory and boredom

### B1. No attention countdown [s2.1]
- [ ] Do not insert an effect, cut, zoom or sound because "a timer says attention has expired." The 8-second and "10-15 minute" rules rest on weak evidence (the lecture-attention review); fatigue and mind-wandering are real but not governed by one universal cutoff.
- [ ] Insert a meaningful change only when the student needs to perform a **different mental operation**. Model transition: "We have established what changes. Now predict what happens when we double it." A zoom, sound effect or unrelated image is not an equivalent substitute.

### B2. Attention is several functions - design response table [s2.2]
Alerting, orienting and executive control are related but different processes; these are design applications, not claims that a graphic activates a particular network.

| Function | What can go wrong | Proposed response |
|---|---|---|
| Readiness to engage | The student is tired, distracted, or uncertain what the lesson offers | State a concrete objective and provide a low-friction starting task. |
| Selecting relevant information | Several arrows, labels, animations, and captions compete | Establish one dominant explanatory focus. |
| Maintaining the task goal | The student loses track of why a calculation is being performed | Keep the question or target quantity visible. |
| Monitoring understanding | The student follows the narrator but cannot reproduce the reasoning | Introduce an answer-hidden checkpoint. |

- [ ] Each scene has a stated objective in the first seconds and a low-friction starting task (e.g. the Ohm's-law opening prediction). [Proposed]
- [ ] Exactly one dominant explanatory focus per moment (scene field *Attention target*). [Proposed]
- [ ] The question or target quantity stays visible during a calculation. [Proposed]
- [ ] At least one answer-hidden checkpoint per lesson (see section F). [Proposed]

### B3. Working memory: count unexplained relationships, not objects [s2.3]
- [ ] **Do not enforce "four objects per screen."** The "four chunks" literature does not establish that a video must contain no more than four visible objects; a familiar equation may be one unit for one student and several disconnected symbols for another.
- [ ] **Proposed rule: count *unexplained relationships*, not just objects.** Ten familiar labels can be manageable; three unfamiliar quantities with an unexplained interaction can overwhelm. [Proposed]
- [ ] Before any dense explanation, briefly establish all four of: (1) what each essential symbol represents; (2) which quantities are changing; (3) what remains constant; (4) what the student is trying to determine. Especially when a revision viewer may have forgotten a prerequisite.

### B4. Attention is not memory [s2.4]
- [ ] Model the chain **Noticing -> interpreting -> connecting -> retrieving -> retaining and transferring.** An animation can make a relationship noticeable without ensuring it can be reconstructed later.
- [ ] The video **initiates a learning cycle, it does not claim to finish it.** Closing task example: "Tomorrow, try a new question before reopening your notes." Never imply that a feeling of clarity means information is permanently secure.

### B5. Diagnose boredom before adding excitement [s2.5]
Boredom is not simply "too little stimulation"; both too little challenge and too much difficulty can disengage.

| Apparent problem | Better response than adding visual excitement |
|---|---|
| "I already know this." | Offer a challenge or a clearly marked route to the next section. |
| "I cannot follow this." | Restore a prerequisite, simplify the representation, or supply one worked step. |
| "Why does this matter?" | Show the question or phenomenon the concept helps explain. |
| "There is too much happening." | Remove competing elements and hold the useful diagram. |
| "I have been listening but not thinking." | Ask for a prediction or explanation before continuing. |

- [ ] When a scene feels flat, pick the matching row; do not add effects. A calmer scene can be more intellectually engaging than a busier one.

### B6. Curiosity - claims boundary [s2.6]
- [ ] Do **not** claim: that a cliffhanger releases a measurable "dose" of dopamine; that a colour activates a learning state; that surprise every few seconds improves school-exam performance. (The fMRI study showed high-curiosity trivia answers were remembered better, with reward-region and hippocampus involvement.)
- [ ] Use a genuine question whose answer helps explain the subject; do not turn the neuroscience into a marketing promise.

---

## C. Cognitive load and instructional sequencing

### C1. Reduce unnecessary work, preserve necessary reasoning [s3.1]
- Unnecessary work = searching for a label; remembering an equation that just disappeared; decoding inconsistent notation; listening to a new explanation while copying the previous one.
- Necessary work = choosing a law; explaining a causal link; comparing two cases; reconstructing a process.
- [ ] **"Do not confuse 'lower cognitive load' with 'no thinking.'"**
- [ ] **Calculation scene (Proposed):** keep the *question and relevant diagram stable* while building **Known quantities -> Relevant relationship -> Substitution -> Result and check**; the previous step stays inspectable until the current step makes sense. Do NOT use the weak sequence "Show the question -> replace with formula -> replace with substitutions -> replace with answer" (student must remember several disappearing states).

### C2. Segment by meaning, not by arbitrary duration [s3.2]
Segmentation meta-analysis: 56 investigations, 88 comparisons - benefits for retention and transfer and reduced cognitive load, **but increased learning time** (more efficient presentation does not mean fewer seconds spent learning). [Strong foundation, implementation-dependent]
- [ ] Place segment boundaries at changes in reasoning, e.g. **Define the system -> select the law -> substitute the model -> simplify -> interpret the result.**
- [ ] A new shot is not necessarily a new conceptual segment; one stable canvas may hold several well-signalled segments.
- [ ] No universal segment duration is assumed (none is established).
- [ ] Budget for the extra learning time; do not promise "faster" learning from segmentation.

### C3. Worked example -> reduced support progression [s3.3]
Research supports gradually removing solution steps, especially when students are prompted to explain the principle behind each step; fading alone does not guarantee broad transfer. [Strong foundation for appropriate tasks]

| Stage | What it is (Proposed) |
|---|---|
| 1. **Full example** | The narrator explains why each step is chosen. |
| 2. **Completion example** | The student supplies one missing step. |
| 3. **Independent example** | The student selects the relationship without the formula being displayed. |
| 4. **Transfer example** | Change the representation, conditions or wording - not merely the numbers. |

- [ ] **Do not call stage 3 "independent" while leaving the completed method beside the question.**
- [ ] Where a lesson teaches a method, follow this progression. Reference implementation (organiser mapping onto the Ohm's-law blueprint): full 03:30-04:20; completion 04:20-05:00; independent 07:20-08:20; transfer is deferred to "a fresh question" after the lesson (09:35-09:48).

### C4. Self-explanation prompt rules [s3.4]
Self-explanation prompts have a positive average effect (meta-analysis), but a useful prompt needs more than asking students to repeat a sentence. [Context-dependent]
- [ ] Prompts must have a clear target and be relational. Prefer: "Why must the temperature remain unchanged in this comparison?" / "Which quantity stayed constant, and how does that determine the next step?"
- [ ] Never use "Do you understand?" as a check - "produces little evidence about what the learner actually understands."

---

## D. Colour, typography, visual hierarchy, captions

### D1. No "best learning colour" [s4.1]
- [ ] Do not claim "blue improves retention" or "green removes anxiety." Colour research is sensitive to context, luminance, saturation, task and methodology. [Insufficient]
- [ ] Give ExamLeaf a calm, attractive identity through spacing, alignment, legibility and restrained colour; treat hue preference as a lower-priority experiment than explanation quality or retrieval practice. [Recommendation]
- [ ] Emotional-design evidence is mixed (systematic review; much on higher education), so neither "colour improves learning" nor "decoration is always harmful" may be asserted.

### D2. Proposed ExamLeaf palette - primary light theme [s4.2]
**Design specifications, not neuroscientific optima.** Machine-readable copy: `palette_and_typography_tokens.json`. The ratios were calculated by the source against `#F7F9FC` using relative luminance (organiser re-computation reproduces them).

| Role | HEX | Contrast against `#F7F9FC` |
|---|---|---:|
| Background | `#F7F9FC` | - |
| Main text and equations | `#14213D` | 15.15:1 |
| Supporting text | `#526074` | 6.06:1 |
| Primary explanatory blue | `#185ABD` | 6.15:1 |
| Teal relationship/highlight | `#087986` | 4.87:1 |
| Amber condition or caution | `#9A5B00` | 5.14:1 |
| Purple secondary relationship | `#6E44AA` | 6.48:1 |
| Red error marker | `#B42318` | 6.23:1 |

- [ ] Thresholds to meet (WCAG): **at least 4.5:1 for normal text** (with relevant exceptions) and **3:1 for essential non-text graphical information** against adjacent colours. These are starting requirements, "not a substitute for testing actual video frames."
- [ ] The listed ratios are each colour against the background only - **not every pair of accent colours**; check adjacent-colour pairs in the actual frame. (Teal at 4.87:1 is the lowest margin over 4.5:1 - **organiser** observation.)

### D3. Optional dark theme [s4.2]
- [ ] Background `#101826`, main text `#EAF0F6`: contrast approximately **15.49:1** (organiser re-check: 15.494).
- [ ] Do not claim dark mode universally reduces fatigue (the dark-text-on-light advantages in the literature often concern tasks such as proofreading, not long-term learning or every viewing environment). Offer and test a dark variant where appropriate.
- [ ] **(organiser)** The source gives no dark values for the accent colours; the canonical `design_tokens.json` states "Other accents require separate contrast validation before dark-mode use." Re-computing the light accents against `#101826` gives only ~2.6-3.5:1, so they cannot be reused unchanged as text on the dark background.

### D4. Colour-use rules [s4.3] [Proposed]
- [ ] **Keep identity stable:** a quantity does not change colour just because the scene changed.
- [ ] **Limit emphasis:** one dominant highlight at a time.
- [ ] **Do not rely on colour alone:** distinguish graph lines with labels, line patterns or shapes.
- [ ] **Respect scientific conventions:** e.g. a red oxygen atom is not an error indicator; a colour's meaning must be clear in context.
- [ ] **Check adjacent colours:** two colours that each contrast well with the background may be hard to tell from each other.
- [ ] Use a pale highlight area with dark text rather than a large block of saturated colour behind a long explanation.

### D5. Phone-readability formula [s4.4]
For a 1920 px-wide video displayed 360 px wide:

`Displayed size = Source size x (360 / 1920)`

- 64 px source text -> approximately **12 px** high on screen; 88 px -> approximately **16.5 px**. "That is why a technically sharp 1080p video can still be difficult to read."
- [ ] Check every essential element at the phone size, not on the editing monitor.

### D6. Starting typography (1920 x 1080 master) [s4.4] [Proposed pilot targets, "not accessibility rules mandating a particular font size"]

| Element | Starting specification |
|---|---|
| Essential English labels | Approximately **88-96 px** |
| Main equations | Approximately **112-144 px**, with separately checked indices |
| Headings | Approximately **104-128 px** |
| Typeface | A clear family such as Inter or an appropriate Noto Sans script family |
| Weight | Medium or semibold for essential labels; avoid very thin strokes |
| Layout | Split, enlarge, or zoom before shrinking essential information |

- [ ] **(organiser)** The canonical `design_tokens.json` in the planning pack lists smaller px ranges (essential label 64-72, equation 84-112, heading 72-88). The source formula puts 64 px at ~12 px on a 360 px-wide phone. The conflict is recorded in `palette_and_typography_tokens.json` (`differences_noted`) and must be resolved by the `04_video_engine` owner before production; do not silently pick one.
- [ ] Test easily-confused glyphs: `I/l/1`, `O/0`, minus signs, decimal points, subscripts, superscripts and Greek letters.
- [ ] A derivation that does not fit at readable size occupies multiple stages. "Do not compress an entire textbook page into one frame."

### D7. Captions [s4.5]
Captions are an accessibility feature, not clutter to eliminate; benefits extend to some second-language viewers, but not every learner benefits equally from every configuration. [Recommendation]
- [ ] Provide accurate selectable captions, an accessible transcript, and a protected caption area.
- [ ] Avoid simultaneously displaying: full narration as a paragraph + animated diagram + equation + moving karaoke captions. A concise definition or critical phrase may remain on screen; the problem is competing demands and poor layout, not all text duplication.

---

## E. Animation and explanation strategy

### E1. Animation decision [s5.1]
Animation research is conditional ("More animation" is not a reliable prescription). Use animation when it helps answer: **What changes? In what order? In which direction? Because of what?** Use a static diagram when the student must inspect structure, compare labels, calculate, or reproduce an exam diagram.

| Learning goal | Proposed visual treatment |
|---|---|
| Understand a structure | Stable, labelled diagram |
| Understand a sequence | Stepwise state changes with persistent landmarks |
| Understand motion | Scientifically valid animation plus inspectable trajectory or graph |
| Understand an equation transformation | Show the operation and preserve correspondence between symbols |
| Compare two conditions | Matched before/after views with common scales |
| Solve a numerical problem | Stable givens and stepwise calculation |
| Reproduce an exam diagram | Final simplified view followed by drawing from memory |

- [ ] "Replace all static diagrams with animation" is **Not supported**; animate only when change, movement or transformation is part of what must be understood.

### E2. Animation density budget [s5.2] [Production hypothesis - "untested starting budget, not a learning-science ratio"]
- [ ] First ordinary 2D revision pilots: **25-35% of runtime for substantial, purposeful motion**; the remainder for stable explanation, inspection, questions and feedback.
- [ ] A process-heavy Biology lesson may need more motion; a mathematical proof less. **Do not require animation merely to satisfy the percentage.**
- [ ] Count substantial changes in the *explanatory model* - not tiny caption updates or a continuously moving cursor.

### E3. Rate of visual change [s5.3]
- [ ] **Do not impose "a new visual every five seconds."** Classify each change as: **Layout change** (new representation or task), **Semantic change** (an arrow appears, a variable changes, a solution step is added), or **Decorative change** (movement conveying no new meaning - remove it).
- [ ] A layout may remain stable for **20-60 seconds or longer**, with meaningful steps appearing within it. Key question: does the student have enough information and time to perform the current task?

### E4. Timing defaults [s5.3] [Production hypothesis - "All are production hypotheses."]

| Event | Starting range |
|---|---:|
| Simple transition | 150-300 ms |
| Highlight appearing | 300-600 ms |
| Simple equation transformation | 0.8-1.5 seconds |
| Hold after an important transformation | 2-4 seconds, longer when necessary |
| Inspection of a completed diagram | Determined by its labels and required task, not a fixed limit |

- [ ] **Never change a physical simulation's behaviour merely to satisfy an animation timing rule.**
- [ ] **(organiser)** Canonical `design_tokens.json` uses `equation_hold_ms: [1000, 3000]` versus the source's 2-4 s; see `differences_noted` in the tokens JSON.

### E5. Subject-specific visual rules [s5.4] [Proposed scientific-communication requirements - "should be checked by the subject reviewer, not inferred from whether the animation looks convincing"]

| Subject | Rule |
|---|---|
| **Physics** | Connect the physical model, graph and numerical values. Keep axes and scale stable when comparing cases. Label slow motion, magnification or other deliberate distortions. |
| **Chemistry** | Maintain atom identity across representations. Distinguish a symbolic reaction, a particle model and an observed phenomenon. Do not use a smooth visual morph to conceal a scientific discontinuity or unsupported mechanism. |
| **Mathematics** | Show "divide both sides by `R`" rather than merely flying `R` across the equals sign. Make assumptions and excluded cases visible where relevant. |
| **Biology** | Retain spatial landmarks and compartments. Show the completed state before advancing. For multi-stage processes provide an inspectable state summary rather than requiring students to remember a disappearing animation. |

### E6. Attractive but not distracting [s5.5]
- [ ] Remove *interesting but instructionally irrelevant* information (seductive details). Do **not** produce ugly, emotionless videos.
- [ ] Achieve appeal through precise diagrams, elegant spacing, smooth but restrained motion, clear audio, and the satisfaction of seeing a difficult relationship become understandable.

---

## F. Active student interaction

### F1. Every substantial pause needs a specification [s6.1]
"Pause and think" is too vague. Each substantial interaction specifies: **What to produce -> what help is available -> when to resume -> how to check -> what to repair.**
Template wording: "Pause and calculate the current. Write the relationship before substituting. Resume when you have an answer with a unit."
- [ ] No rhetorical question with an immediate answer reveal counts as an interaction.

### F2. Recommended interaction pattern [s6.2] [Production hypothesis - "This interval is a design hypothesis."]
- [ ] For a ten-minute revision pilot: **two or three substantial pause-to-write or pause-to-solve activities, plus three or four brief predictions or recall prompts.**
- [ ] This usually yields an invitation to think roughly every **75-120 seconds**, but boundaries follow the material.
- [ ] Do not force every lesson to include definitions, copying, drawing, prediction, solving and multiple quizzes; choose actions that match the objective.
- [ ] The Ohm's-law blueprint (4 brief predictions + 3 substantial pauses; spacing 75-96 s) is the reference implementation: `BLUEPRINT_600_second_ohms_law_lesson.md`.

### F3. Interaction menu [s6.2] [Production hypothesis - time ranges "are proposed defaults, not experimentally established optima"]

| Activity | What it should accomplish | Proposed execution |
|---|---|---|
| Predict an outcome | Commit to an expectation before seeing the result | Ask one clear question; allow roughly **5-8 seconds** for a simple prediction. |
| Retrieve a definition | Reconstruct the essential meaning | Hide the definition; ask for its key components, then show an answer checklist. |
| Record a formula | Create a useful reference, not a transcript | Include symbol meanings, units, and applicability conditions. |
| Reconstruct a formula | Test retrieval rather than copying | Remove it, ask students to write it, then compare. |
| Draw a diagram | Reconstruct relationships or process order | Ask for a simple labelled sketch, not polished artwork. |
| Complete a missing step | Bridge demonstration and independence | Supply enough context to make the next operation achievable. |
| Solve independently | Test method selection and execution | Hide the method; allow a genuine learner-controlled pause. |
| Explain an error | Diagnose a misconception | Show the claim clearly as incorrect and require a reason or counterexample. |
| Verify an answer | Build monitoring habits | Check units, direction, order of magnitude, conditions, or process consistency. |

### F4. Quizzes do not reliably "reset attention" [s6.3]
- [ ] Conclusion to embed: **retrieval practice has a strong general foundation; the claim that a quiz reliably resets everyone's attention at a specific interval is much weaker.** Early experiments found interpolated tests could reduce mind-wandering and improve video-lecture learning, but later work has not reproduced every benefit (a 2022 study, 195 undergraduates, limited evidence; a 2025 study, 703 students, learning benefits moderated by distraction conditions).
- [ ] Design questions for learning first; never justify a quiz by an attention-reset claim.

### F5. Writing [s6.4]
- [ ] Do not tell students to copy the entire narration.
- [ ] Formula routine (Proposed): **Understand -> record a compact reference -> hide it -> reconstruct -> compare.**
- [ ] For a definition, identify the components that make it scientifically correct. For an exam answer, distinguish essential terminology from unnecessary verbatim memorisation.
- [ ] Do not claim handwriting is always superior to typing (replication found inconsistent differences). Use handwriting where it supports equation work and exam practice; permit typing, oral explanation or accessible alternatives. [Context-dependent]

### F6. Drawing [s6.5]
Drawing can support learning but depends on task design, representation type and learner skill (2025 review: mixed findings, boundary conditions). [Context-dependent]
- [ ] Make drawing a *reasoning task*. Good prompt: "Draw the two compartments, add the direction of movement, and label the condition that causes it." Poor prompt: "Copy this detailed illustration exactly."
- [ ] Supply a partial outline when drawing demands would otherwise obscure the science.
- [ ] **During demanding writing or drawing, stop introducing new explanation.** Let students work, then resume with feedback.

### F7. Be transparent about total study time; player behaviour [s6.6]
- [ ] A student who pauses three times for a minute turns a 10-minute video into at least 13 minutes of study. Label honestly: **"10-minute revision video, with optional practice pauses."**
- [ ] Do not make students feel slow for using the pauses the lesson requires.
- [ ] On an ordinary video platform: spoken pause instruction + a stable prompt. In an ExamLeaf player: a learner-controlled **"Continue to explanation"** action, **not** an automatic answer reveal after a stressful countdown.

---

## G. Narration speed, pauses and intensity

### G1. Playback speed claims [s7.1]
- [ ] Accelerated-playback evidence (small costs at 1.5x and 2x, poorer above 2x; materials were real-estate and Roman-history lectures at ~157 and ~166 wpm) does **not** establish that unfamiliar equations, second-language narration or dense Biology processes should be delivered at 2x. [Context-dependent]
- [ ] Observational MOOC findings linking faster speech and engagement do not establish causal learning gains; watching longer or attempting an assessment is not retaining more. Do not cite them as proof that faster narration is better.

### G2. Voice pacing standard [s7.2] [Production hypothesis - "starting points for English-language pilots"]

| Narration type | Initial target |
|---|---|
| Ordinary explanation | **130-155 spoken words per minute** |
| Familiar recap or straightforward transition | Approximately **145-165 wpm** |
| New symbolic relationship or dense terminology | Slower delivery, often equivalent to **90-120 wpm**, with meaningful pauses |
| Independent practice | Silence or minimal instructions |
| Final recap | Clear and compact, not rushed |

- [ ] **Validate other languages separately; do not transfer word-rate targets directly.** (Organiser: this applies to Assamese, Hindi and any Hinglish narration used for Assam Board audiences; the source names no specific language.)
- [ ] Writing budget for a ten-minute lesson with substantial silent processing time: approximately **1,050-1,250 narration words**; the actual requirement depends on scene and pause design.
- [ ] **(organiser)** Sanity check: 1,050 words at 155 wpm = 6.8 min; 1,250 at 130 wpm = 9.6 min; the remainder of the 10 minutes is pauses, slow dense passages and silent practice, consistent with the Ohm's-law blueprint.

### G3. Pause lengths [s7.3] [Production hypothesis - "Proposed starting ranges"]

| Where | Pause |
|---|---|
| Between ordinary phrases where natural | **0.3-0.6 s** |
| After a key causal statement or before an important contrast | **0.8-1.5 s** |
| To inspect a completed transformation or diagram | **2-4 s** |
| A genuinely simple mental prediction | **5-8 s** |
| Writing, drawing, multi-step calculation, or explanation | **Learner-controlled pause** |

- [ ] Pause at the point where thinking must happen. **"Do not use a two-second silence as evidence that students had a fair opportunity to solve a problem."**

### G4. Intensity follows reasoning [s7.4]
- [ ] Intensity pattern (Proposed): **Curious opening -> steady explanation -> deliberate emphasis -> quiet attempt -> precise feedback -> calm conclusion.**
- [ ] Emphasise logical relationships, e.g. "The current changes **because**..." / "This conclusion holds **provided that**..." / "Notice the difference between..."
- [ ] Avoid constant excitement.

### G5. Voice identity and music [s7.4]
- [ ] No particular gender, accent, pitch or breathiness is treated as inherently optimal without audience testing.
- [ ] Core explanation has **no background music** by default - "a conservative production choice, not a claim that music always harms learning." Test any musical version against silence on comprehension and listening effort, not just preference.
- [ ] **(organiser)** Canonical `design_tokens.json` records `core_background_music: false`, which is consistent.

---

## H. Confidence, encouragement, emotion and trust

### H1. Genuine confidence = calibrated confidence [s8.1]
Controlled college Physics study: students in active-learning conditions learned more while reporting a *lower* feeling of learning than passive-condition students; effort can distort judgements (this does not make every difficult experience productive). [Context-dependent]
- [ ] Teach students to distinguish "That explanation felt clear." from "I can now perform the relevant task without help." Goal: confidence that appropriately reflects capability, not maximum confidence.

Confidence-calibration 2x2:

| Student state | Appropriate response |
|---|---|
| Correct and confident | Offer a less familiar application. |
| Correct but unsure | Identify the valid reasoning and provide a second independent check. |
| Incorrect and unsure | Supply a targeted hint and another attempt. |
| Incorrect but confident | Address the misconception explicitly with evidence or a counterexample. |

### H2. Competence, control, value, respect [s8.2] [Proposed applications; evidence is largely associative]
- [ ] **Competence:** provide a task the student can complete using the explanation just given.
- [ ] **Control:** allow pauses, replay, hints and a route to prerequisite help.
- [ ] **Value:** explain what the concept enables, including its examination use.
- [ ] **Respect:** acknowledge uncertainty without ridicule or infantilising language.
- [ ] Do not advertise a few interface choices as a proven motivational intervention. Do not remove exam goals in pursuit of "pure intrinsic motivation" - students can value marks, understanding, opportunities and interest simultaneously.

### H3. Feedback must contain information [s8.3]
Feedback meta-analysis: positive average effect with substantial variation; quality and content matter, not praise per se. [Context-dependent]
- [ ] Every feedback line answers: **What was correct? What needs changing? What should the learner do next?**

Proposed narration scripts:

| Situation | Useful wording |
|---|---|
| Opening | "We will connect the diagram, the equation, and one exam-style application." |
| Before a challenge | "Try the next step before looking at the solution. An unfinished attempt is useful here." |
| Correct method | "You selected the right relationship. Now check the unit." |
| Correct prediction | "Your prediction matches the model because you kept the other quantity constant." |
| Calculation error | "The relationship is correct. Recheck the substitution rather than restarting the whole problem." |
| Conceptual error | "The important distinction is the direction of the relationship. Let us compare the two cases." |
| After a difficult step | "That was the key reasoning step. The remaining calculation uses it." |
| Closing | "Check which parts you completed without help. Those are your starting points for the next practice question." |

- [ ] **Non-interactive video = conditional wording:** "**If** you obtained `1.5 A` using this relationship, your method matches the model." The narrator must not pretend to know that an unseen student succeeded.

### H4. What to avoid saying (identity-based praise and empty effort messages) [s8.4]
Intelligence-praise research found adverse motivational responses under some conditions, especially after difficulty; this is not a reason to be cold or never compliment, it is caution against making success a judgement of fixed intelligence. [Context-dependent]

| Avoid | Prefer |
|---|---|
| "You are a genius." | "Your diagram shows the correct relationship." |
| "This is so easy." | "This step is unfamiliar; use the previous result as a starting point." |
| "You just need to try harder." | "A different strategy will help here." |

- [ ] Growth-mindset reviews differ on size and conditions of benefit; **never promise improved attainment through motivational slogans alone.**
- [ ] **(organiser consolidation)** Also never use exaggerated claims, false promises ("full marks guaranteed" is explicitly excluded at blueprint beat 09:48-10:00) or manipulative psychology - the brief in `prompt/03_USER_prompt_learning_psychology.md` requires "positive messaging without exaggerated claims, false promises, or manipulative psychology."

### H5. Anxiety safeguards [s8.5]
Anxiety is reliably associated with poorer working-memory performance, with variation and methodological limits. [Context-dependent]
- [ ] Safeguards (Proposed): predictable lesson structure; low-stakes practice; private attempts; available hints; feedback that identifies a repairable issue.
- [ ] Avoid: public comparisons; humiliating error messages; threatening countdowns; promises that imply failure is the student's fault.
- [ ] Do not present the videos as treatment for persistent anxiety; the goal is to avoid adding unnecessary threat. Reduce avoidable anxiety, **not all challenge.**

### H6. Progress indicators reflect capability, not consumption [s8.6]
- [ ] Keep two indicators separate: **Lesson completed** (media viewed) and **Skill demonstrated** (learner completed an appropriate task).
- [ ] An initial correct answer is still not proof of durable mastery.
- [ ] Example display (Proposed): "Today: calculated with support. Next: solve a fresh question without the formula." Never award "Mastered" after the final frame.

---

## I. Curiosity, storytelling, retention and continued study

### I1. Open with a genuine knowledge gap [s9.1]
A strong opening asks a question the student can understand but cannot yet confidently resolve. Prequestioning has potential benefits, but effects depend on the questions and the later teaching and may direct attention to selected information rather than improving everything. [Context-dependent]

Proposed opening questions:

| Subject | Opening question |
|---|---|
| Physics | "Does doubling the voltage always double the current?" |
| Mathematics | "These two expressions look similar. Why does one require an extra condition?" |
| Chemistry | "What must remain unchanged when we balance this reaction?" |
| Biology | "The final structures look similar. Which process step distinguishes how they formed?" |

- [ ] Close the initial knowledge gap when the explanation reaches it. **Do not withhold an essential answer merely to extend watch time.**

### I2. Causal stories and relevance [s9.2]
- [ ] Prefer a causal story: **A system -> a change -> a consequence -> an explanation.** No invented character, dramatic music or long historical anecdote is required.
- [ ] Relevance can come from students making their own connections (randomised high-school study with a semester-level relevance-writing intervention improved interest and performance, especially for students with low expectations of success) - this does **not** prove a ten-second "real-life connection" gives the same benefit. [Context-dependent]
- [ ] Use an occasional prompt: "Where else could this relationship help explain what you observe?" Keep the connection scientifically accurate and proportionate.

### I3. Misconception-correction sequence [s9.3]
Refutation-text research supports explicitly identifying and correcting misconceptions.
- [ ] Sequence (Proposed): **Correct principle -> clearly identified misconception -> reason it fails -> better model -> new application.**
- [ ] Worked example: "On an `I`-versus-`V` graph, a steeper line does not mean greater resistance. At the same voltage, the steeper line represents more current, so `R = V/I` is smaller."
- [ ] Keep graph axes visible. **Do not flash the wrong statement and then leave it unresolved.** Correct with an explanation, not a red cross.

### I4. Retrieval beyond the video - spacing schedule [s9.4]
Spacing research: the useful interval depends on the desired retention interval; there is **no universally optimal "1-3-7" sequence.** The dates below are "adjustable hypotheses." [Strong foundation for spacing; schedule = Production hypothesis]

| Occasion | Practice |
|---|---|
| End of lesson | One unprompted explanation or application |
| Next day | Brief recall before reopening notes |
| About three days later | A changed numerical or diagram question |
| About one week later | Mixed practice requiring method selection |
| Later, according to exam timing | Another delayed check and targeted repair |

- [ ] **Change the cues** between occasions: a paper-style question, a different diagram orientation where appropriate, different wording. Students must not depend on ExamLeaf's colour scheme or the narrator's next sentence to retrieve the concept.

### I5. Ending rule [s9.5]
- [ ] Encourage stopping at a useful point; the desired behaviour is not endless viewing. Good ending: "Complete one fresh question now, then return for the next topic."
- [ ] **Avoid:** autoplay pressure, streak-loss guilt, variable rewards, artificial scarcity. Use reminders only with student choice and a clear learning purpose.
- [ ] Calm ending, no "full marks guaranteed" message (blueprint beat 09:48-10:00).

---

## J. Individual differences - accommodation table [s10]
"There is no single ideal pace for every Class 10-12 student."

| Difference | Proposed accommodation |
|---|---|
| Weak prerequisite knowledge | A short prerequisite explanation or an explicit link back |
| Strong prior knowledge | A visible challenge route and optional skipping of basic steps |
| Second-language viewing | Clear terminology, accurate captions, glossary support, and unhurried transitions |
| Difficulty reading small symbols | Larger views, fewer simultaneous expressions, accessible alternatives |
| Hearing access needs | Captions, transcripts, and meaningful visual representation of essential sound |
| Motion sensitivity or visual discomfort | Reduced-motion version and stable alternatives |
| Difficulty sustaining a task | Shorter meaningful sections, clear prompts, optional breaks |
| Difficulty drawing or writing | Partial templates, typing, oral explanation, or alternative response methods |
| Small device or unreliable connectivity | Mobile-tested visuals and lightweight downloadable practice material |

- [ ] **Do not assign students to fixed "visual," "auditory" or "kinaesthetic" learning styles.** Preferences and accessibility needs are real; evidence does not support the claim that matching instruction to a declared learning style improves learning. [Not supported]
- [ ] **A revision video must not conceal a first-teaching problem.** A student missing the underlying concept may need a longer preparatory explanation - not the same compressed lesson at a slower playback speed.

---

## K. Pre-release checklist (consolidation)

**The four release-review questions [s13]:**
- [ ] **Scientific:** Is every claim, diagram, transformation, condition and answer correct?
- [ ] **Instructional:** Does the learner get an opportunity to perform the target task without the explanation doing it for them?
- [ ] **Perceptual:** Can the essential content be read and followed on the intended devices, with captions and audio working together?
- [ ] **Emotional:** Are the challenges fair, feedback specific, and confidence statements honest?

**Spot checks distilled from sections A-J:**
- [ ] Scene records carry all 12 pedagogical fields (`SCENE_PEDAGOGY_SCHEMA.md`).
- [ ] 2-3 substantial pauses + 3-4 brief predictions; each substantial pause has produce / help / resume / check / repair specified (F1-F2).
- [ ] Answers hidden until after the attempt; learner-controlled "Continue to explanation" in the ExamLeaf player (F7).
- [ ] Question/target quantity visible; previous step inspectable; one dominant highlight; no colour-only encoding (B2, C1, D4).
- [ ] Palette and contrast verified on actual frames at phone size; typography conflict resolved (D2-D6).
- [ ] Captions accurate and selectable; transcript available; protected caption area (D7).
- [ ] Motion limited to meaningful change; no decorative motion; physical simulations unaltered (E2-E4).
- [ ] Narration within 130-155 wpm (slower for dense terms); 1,050-1,250 words; no background music in the core explanation (G).
- [ ] Feedback scripts informative and conditional; no identity praise; no countdown threats; no "Mastered" for viewing (H).
- [ ] Opening is a genuine knowledge gap that the lesson closes; misconception, if any, corrected with explanation (I1, I3).
- [ ] Closing gives a next-day retrieval action; no autoplay/streak/scarcity pressure (I4-I5).
- [ ] Any claim about outcomes is limited to what section A1/A2 allows.

**What automated checks can and cannot do [s13]:** they can flag contrast, text size, clipping, answer-reveal timing, missing units, absent captions, or suspiciously dense scenes; they cannot determine scientific validity or genuine student learning from visual polish alone.

**The recommended ExamLeaf standard [s13]:** "One clear purpose, a small number of connected ideas, a stable visual model, explicit reasoning, meaningful student attempts, useful feedback, and a later opportunity to retrieve the learning." The brand promise is not effortlessness but that **students can see what they understand, discover what still needs work, and become progressively more capable of answering without ExamLeaf beside them.**
