# Evidence register

> **Section 09 - research and evidence.** One consolidated register of every research claim, effect size, design principle and evidence caveat that ChatGPT's six responses and the delivered packs rely on. Research date of all sources: **13 October 2026** (the Super Teacher ledger header: *"This is a targeted research synthesis, not a preregistered systematic review. ... Exact pacing/humour prescriptions are production hypotheses."*).
>
> Nothing here was re-researched or re-verified. Every row is a transcription of what the source says, including what the source says the evidence does **not** establish. No URL was fetched.

## How to read the register

All parts use the same six columns:

| Column | Meaning |
|---|---|
| **ID** | Stable row key (`E-A01` = Part A row 1, etc.) so other sections can cite a row. |
| **Claim / principle** | The design decision, finding or number as the source words it. |
| **Evidence label (as the source states it)** | The source's own wording. Message 04 section 1 uses three internal categories plus three negative verdicts; other sources use sentences instead of labels - those are quoted, not re-labelled. |
| **Does NOT establish** | The limit the source itself attaches to the claim ("It does not mean ...", "no universal ... is established"). Never filled in by inference; `(none stated)` where the source gave no limit. |
| **Source and link(s)** | Message number + section, then the URL(s). **Link caveat below.** |
| **Used in** | Project section(s) where the claim is applied: `S01` business model, `S02` learning psychology, `S03` Super Teacher framework, `S04` video engine, `S05` narration system, `S06` skills library, `S07` end-to-end pipeline instructions, `S08` cost models, `S09` this section, `S10` pilots and examples. This is the *primary* home by topic, not a check of the sibling sections' contents. |

### The three internal labels from message 04 section 1

* **Strong foundation** - converging research supports the general practice.
* **Context-dependent** - useful findings exist, but outcomes depend substantially on learners, material, implementation or measurement.
* **Production hypothesis** - a sensible starting specification that ExamLeaf should test, not a scientifically established optimum.

The same table also issues these verdicts: **Not supported**, **Insufficient for that specific claim**, **Insufficient as a stand-alone strategy**, **Not justified**. Message 02 section 8 phrases the same idea as "What has stronger support" with an "Evidence qualification" column.

### Link caveat (read this once)

`cited_source_links.md` lists 18 learning-science URLs, 4 OpenStax pages, 2 WCAG pages, Skill/tool repositories, pricing pages and TTS provider pages. The raw transcript marks each citation with an opaque token (e.g. `turn649723view0`) and **the token-to-URL mapping was not preserved** (the raw JSON records only `search_result_groups: 97` for message 04). Therefore:

* Where the Super Teacher `Research_Ledger.md` gives an author, year **and** URL for a study (P01-P18), the link is exact.
* Where a claim matches a listed URL only by the label in `cited_source_links.md` (e.g. "multimedia learning / segmentation"), the link is marked **(inferred)**.
* Where no listed URL fits (e.g. the March 2026 seductive-details meta-analysis, the 2022/2025 interpolated-testing studies, working-memory, handwriting, growth-mindset, anxiety, learning-styles papers), the cell says **URL not preserved** - the claim is real in the transcript but its link was not captured. These are listed again in Part K as gaps.

## Part A - Message 04 section 1: evidence assessment table (all 10 rows)

| ID | Claim / principle | Evidence label (as the source states it) | Does NOT establish | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-A01 | Include retrieval practice rather than relying exclusively on rewatching. ExamLeaf conclusion: "Require students to retrieve or apply information before showing the answer." | **Strong foundation** | "It does not mean '50% higher marks'" (re g = 0.50); effects "varied with feedback, question format, comparison activity, repetition, and other factors". Msg 04 s6.3: "Retrieval practice has a strong general foundation. The claim that a quiz reliably resets everyone's attention at a specific interval is much weaker." Msg 06 s1.1: supports the learning mechanism "not a claim that an ExamLeaf purchase will produce a particular increase in marks". `sources.csv`: "retrieval evidence, not fixed interaction timing". | Msg 04 s1 and s1 "How large are the reported effects?"; Yang et al. 2021 (ledger P06) https://pubmed.ncbi.nlm.nih.gov/33683913/ | S02, S03, S04, S05, S07, S10, S01 |
| E-A02 | Revisit material across separate study occasions. Conclusion: "Build practice after the video, not just repetition within it." | **Strong foundation** | "There is no universally optimal '1-3-7' sequence" (msg 04 s9.4); exact interval "depends on the desired retention interval" / "retention goal and material" (msg 02 s8, msg 08 s13). The proposed schedule (end of lesson, next day, ~3 days, ~1 week, later) is "adjustable hypotheses". | Msg 04 s1, s9.4; Cepeda et al. 2006 (ledger P14: "Distributed verbal practice synthesis; exact spacing depends on retention goal and material") https://pubmed.ncbi.nlm.nih.gov/16719566/ | S02, S03, S10 |
| E-A03 | Segment complex explanations into meaningful units. Conclusion: "Separate conceptual steps and allow processing time." | **Strong foundation, implementation-dependent** | "No universal segment duration is established." Segmentation "increased learning time", so "more efficient presentation does not necessarily mean fewer seconds spent learning" (msg 04 s3.2). Segment by meaning, not arbitrary duration. | Msg 04 s1, s3.2; https://link.springer.com/article/10.1007/s10648-023-09842-1 **(inferred - the link list labels this URL "multimedia learning / segmentation"; ledger P16 is Mayer 2024)** | S02, S04, S10 |
| E-A04 | Use worked examples, then reduce support. Conclusion: "Move from demonstrated reasoning toward independent problem-solving." | **Strong foundation for appropriate tasks** | "Fading alone does not guarantee broad transfer to unfamiliar problems" (msg 04 s3.3); ledger P04: "Near-transfer support; far transfer is not automatic. Include explicit explanation of principles." Msg 02 s8: effectiveness "depends on prior knowledge and task design". "Do not call the third stage 'independent' while leaving the completed method beside the question." | Msg 04 s1, s3.3; Atkinson, Renkl & Merrill 2003 (ledger P04) https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/ | S02, S03, S04, S06, S10 |
| E-A05 | Highlight the relevant part of a diagram or equation. Conclusion: "Direct attention; do not highlight everything." | **Strong foundation, when selective** | Not a licence for constant highlighting; msg 02 s8: "Useful for guiding attention without adding unrelated information"; "one dominant highlight at a time" (msg 04 s4.3). Ledger P16: multimedia theory is "not a mandate for constant animation". | Msg 04 s1; msg 02 s8 (signalling). **URL not preserved**; nearest listed: Mayer 2024 https://link.springer.com/article/10.1007/s10648-023-09842-1 (inferred) | S02, S04 |
| E-A06 | Replace all static diagrams with animation. Conclusion: "Animate when change, movement, or transformation is part of what must be understood." | **Not supported** | Msg 04 s5.1: animation research "supports a conditional position: animation can help, but its value depends on what is being taught and how the visual information is presented. 'More animation' is not a reliable learning prescription." | Msg 04 s1, s5.1. **URL not preserved** | S02, S04, S10 |
| E-A07 | Insert a quiz at a particular fixed interval (e.g. "reset attention every 90 seconds"). | **Production hypothesis** | "There is no established 'reset attention every 90 seconds' law." Msg 04 s6.3: early experiments found interpolated tests could reduce mind-wandering and improve learning from video lectures, "later work has not reproduced every benefit under every condition"; a 2022 study of 195 undergraduates found limited evidence for reduced task-unrelated thoughts and no statistically supported learning benefit; a larger 2025 study of 703 university and community-college students found benefits from interpolated retrieval, "moderated by the distraction conditions". | Msg 04 s1, s6.3. **URLs not preserved** | S02, S03, S05, S10 |
| E-A08 | Choose a particular blue, green or background to improve memory. Conclusion: "Choose colours for legibility, meaning, consistency, and tested comfort." | **Insufficient for that specific claim** | Msg 04 s4.1: colour research "is sensitive to context, luminance, saturation, task, and methodology" and "does not justify universal claims such as 'blue improves retention' or 'green removes anxiety'". Emotional-design systematic review: "varied outcomes", mostly higher education. Msg 02 s9: "There is no scientifically established 'best HEX code for learning.'" The palette is "design specifications, not neuroscientific optima" (msg 04 s4.2). Dark mode: "Do not claim that dark mode universally reduces fatigue." WCAG 4.5:1 / 3:1 are "useful starting requirements, not a substitute for testing actual video frames". | Msg 04 s1, s4.1-4.2; msg 02 s9; WCAG contrast https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html ; colour-research papers **URL not preserved** | S02, S04, S10 |
| E-A09 | Increase confidence through repeated praise. Conclusion: "Build confidence through evidence of competence and useful feedback." | **Insufficient as a stand-alone strategy** | Msg 04 s8.4: intelligence praise showed "adverse motivational responses under some conditions, particularly following difficulty"; growth-mindset reviews "differ in their conclusions about size and conditions of benefit. Neither supports guaranteeing improved attainment through motivational slogans alone." Msg 02 s8: heterogeneous findings "do not justify promising that motivational wording alone improves attainment". | Msg 04 s1, s8.3-8.4; feedback meta-analysis (ledger P08) https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full ; praise / mindset papers **URL not preserved** | S02, S03, S05 |
| E-A10 | Treat high completion rates as proof of learning. Conclusion: "Measure delayed recall, transfer, and independent performance." | **Not justified** | Msg 04 s7.1: observational MOOC findings about faster speech and engagement "do not establish a causal improvement in learning. Watching longer or attempting an assessment is not equivalent to retaining more." Msg 02 s8: "Watch time is useful diagnostically" only. | Msg 04 s1, s7.1, s8.6, s12.1; msg 02 s8. **URL not preserved** | S02, S08, S10 |

## Part B - Effect sizes and quantitative evidence anchors

| ID | Claim / principle | Evidence label (as the source states it) | Does NOT establish | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-B01 | **g = 0.50** - classroom testing meta-analysis integrating **222 studies involving 48,478 students**; "average effect of approximately g = 0.50". "Supports retrieval practice as a serious instructional tool." | Strong foundation (retrieval practice); effect reported as an average with variation | "It does not mean '50% higher marks.'" Effects varied with feedback, question format, comparison activity and repetition. **"Do not add effect sizes from separate studies together or turn them into a predicted ExamLeaf exam-score improvement."** | Msg 04 s1 "How large are the reported effects?"; `sources.csv` ("222 studies; retrieval evidence, not fixed interaction timing"); Yang et al. 2021 https://pubmed.ncbi.nlm.nih.gov/33683913/ | S02, S03, S01, S10 |
| E-B02 | **g = -0.16** - meta-analysis "published in March 2026, drawing on 50 studies": "small average negative effect" of interesting but irrelevant details on learning. | Supports removing unnecessary decoration | "That argues against unnecessary decoration - not against attractive educational design." Not additive with other effect sizes (same warning as E-B01). | Msg 04 s1. **URL not preserved** (the 2026 meta-analysis is not individually identifiable in `cited_source_links.md`); nearest listed: Kienitz et al. 2023, ledger P17 https://pmc.ncbi.nlm.nih.gov/articles/PMC10176302/ ("relevant visual beauty is not the same as irrelevant decoration") | S02, S04, S03 |
| E-B03 | **Segmentation: 56 investigations / 88 comparisons** - benefits for retention and transfer, reduced cognitive load; also increased learning time. | Strong foundation, implementation-dependent | No universal segment duration; "fast-track" does not mean fewer seconds spent learning. | Msg 04 s3.2; https://link.springer.com/article/10.1007/s10648-023-09842-1 (inferred) | S02, S04 |
| E-B04 | **Teacher humour 2026: 206 expert raters and 325 students**, two randomized video-lesson studies (Learning and Instruction 102, 102311). Course-related humour improved rapport, interestingness, motivation, enjoyment; aggressive humour produced less favourable emotional responses. | Experimental (randomized video lessons) - socio-emotional outcomes only | "These results do **not** demonstrate better delayed retention or examination performance" (msg 08 s1.2); ledger P03: "do not infer delayed achievement gains"; `sources.csv`: "not proof of exam gain". | Msg 08 s1.2; ledger P03 https://www.sciencedirect.com/science/article/pii/S095947522500235X | S03, S10 |
| E-B05 | **Synthetic-voice enthusiasm: 244 university participants.** Varying enthusiasm affected some emotional / cognitive-load measures. | Single study | "Did not improve immediate retention or transfer." | Msg 08 s9.1; ledger P12 (Liew et al., 2023; online 2022) https://pubmed.ncbi.nlm.nih.gov/35967831/ | S03, S05 |
| E-B06 | **Modern TTS vs human voice** - no statistically significant difference under the study's conditions. | Single study | "Does not establish universal equivalence" but cautions against rejecting modern synthesis on older machine-voice findings (msg 08 s9.1); ledger P11: "not proof of equivalence for every task". | Msg 08 s9.1; ledger P11 (Dincer, 2022) https://www.ijopr.com/article/the-voice-effect-in-multimedia-instruction-revisited-does-it-still-exist-12116 | S05, S03 |
| E-B07 | **Prerecorded response prompts: 58 four-year-olds** (Gaudreau et al., 2020). | Single study (preschool) | "Preschool story-reading cannot establish optimal teen lesson design"; cannot establish best interaction frequency for adolescents (msg 08 s4.1). | Ledger P10; msg 08 s4.1 https://pubmed.ncbi.nlm.nih.gov/33013552/ | S03, S05 |
| E-B08 | **Interpolated tests: 195 undergraduates (2022)** vs **703 university and community-college students (2025)**. | Mixed replication record | 195-student study: no statistically supported learning benefit in its design; 703-student study: benefits, moderated by distraction. Neither fixes an interval. | Msg 04 s6.3. **URLs not preserved** | S02, S03 |
| E-B09 | **Accelerated lecture playback**: relatively small costs at 1.5x and 2x under the study's conditions; poorer above 2x; lectures on real estate and Roman history at original speech rates of about 157 and 166 words per minute. | Single study (non-STEM lectures) | "Do not establish that unfamiliar equations, second-language narration, or dense Biology processes should be delivered at 2x." | Msg 04 s7.1. **URL not preserved** | S02, S05 |
| E-B10 | **Sample-size planning**: standardized difference 0.30, 80% power, two-sided 5% -> about **175 learners per group**; difference 0.20 -> about **400 per group**, before attrition. | Illustrative calculation | "Approximate planning calculations, not a power analysis for a finished study." Classroom clustering, repeated observations, baseline adjustment, reliability and missing data change the requirement. "A small group can reveal that a graph label is unreadable. It cannot reliably establish a modest learning advantage." | Msg 04 s12.4 | S10, S02 |
| E-B11 | **Contrast ratios computed for the proposal** against `#F7F9FC`: text `#14213D` 15.15:1; support `#526074` 6.06:1; blue `#185ABD` 6.15:1; teal `#087986` 4.87:1; amber `#9A5B00` 5.14:1; purple `#6E44AA` 6.48:1 (msg 04) / 6.49:1 (msg 02); red `#B42318` 6.23:1; dark theme `#101826` with `#EAF0F6` about 15.49:1. | Calculated "for this report" (relative luminance) | They concern each colour against the specified background "not every possible pair of accent colours"; "Palette compliance alone does not establish that the complete video player or learning product is accessible." WCAG: 4.5:1 normal text, 3:1 essential non-text. | Msg 04 s4.2; msg 02 s9; WCAG contrast https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | S04, S02 |
| E-B12 | **Conversational wording: three narrated-animation experiments** (Mayer et al., 2004): improved transfer, not retention. | Experiments | "Not proof that slang, fake intimacy or constant informality helps." | Msg 08 s1.1; ledger P01 https://eric.ed.gov/?id=EJ684999 | S03 |
| E-B13 | **University Physics active-learning experiment**: active-learning students learned more while reporting lower feeling of learning. | Controlled experiment (university) | "The study does not mean difficulty is always productive." Not a direct ExamLeaf conversion study (`Research_Source_Ledger.csv`). | Msg 04 s8.1; msg 08 s1.5; ledger P07 (Deslauriers et al., 2019) https://pubmed.ncbi.nlm.nih.gov/31484770/ ; also https://www.pnas.org/doi/10.1073/pnas.1821936116 (business ledger) | S02, S03, S01 |
| E-B14 | **Relevance-writing intervention**, randomized high-school science study: improved interest and performance, especially for students with low expectations of success. | Randomized study (semester-level) | "Not proof that a ten-second 'real-life connection' guarantees the same benefit." | Msg 04 s9.2. **URL not preserved** | S02, S03 |
| E-B15 | **Indian multilingual teaching: eight secondary English teachers** (Anderson, 2024; online 2022). | Case study | "Not causal evidence for a fixed Hinglish proportion in STEM"; "not a randomized test of Hinglish science instruction". | Msg 08 s5.5; ledger P18 https://www.tandfonline.com/doi/full/10.1080/01434632.2022.2045300 | S03, S05 |
| E-B16 | **Attention-span myths**: 8-second and 10-15-minute rules. | Review (Bradbury, 2016) | The review "challenges fixed 8-second and 10-15-minute rules; does not deny attention fluctuation" (ledger P13); "This does not mean fatigue and mind-wandering are imaginary" (msg 04 s2.1). | Msg 04 s2.1; msg 08 s1.6; ledger P13 https://pubmed.ncbi.nlm.nih.gov/28145268/ | S02, S03 |

## Part C - Message 08 section 1.1-1.6 ("What the research actually supports") and the evidence statements that qualify the Super Teacher framework

| ID | Claim / principle | Evidence label (as the source states it) | Does NOT establish | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-C01 | **s1.1** Conversational teaching can help - but informality alone is not the mechanism. Three multimedia experiments: conversational wording improved ability to **apply** what was learned, but not **retention** of the presented material. Recommendation: "make narration conversational through useful guidance, not decorative informality." | Experiments (3); supports a conversational approach | "It does not establish that adding slang, 'bro,' filler words, or constant jokes improves learning." Ledger P01: "Not proof that slang, fake intimacy or constant informality helps." | Msg 08 s1.1; ledger P01 (Mayer et al., 2004) https://eric.ed.gov/?id=EJ684999 | S03, S05, S06 |
| E-C02 | **s1.2** Humour can improve the experience without improving achievement. 2026 study: 206 expert raters, 325 students; course-related humour improved rapport, interestingness, motivation, enjoyment; aggressive humour less favourable. Broader review: mixed achievement literature. Recommendation: "use humour as a supporting instructional tool. Its presence is not evidence that the lesson works." | Experimental (randomized video lessons) + review ("complex, mixed achievement literature") | "These results do not demonstrate better delayed retention or examination performance." "Students enjoying a teacher, remembering a joke, and learning the scientific principle are different outcomes." Ledger P02: "perceived enjoyment and achievement must be separated." | Msg 08 s1.2; ledger P03 https://www.sciencedirect.com/science/article/pii/S095947522500235X ; ledger P02 (Zhou & Lee, 2025) https://pmc.ncbi.nlm.nih.gov/articles/PMC11814177/ | S03, S05, S06, S10 |
| E-C03 | **s1.3** Scaffolding is more important than charisma. Research supports moving from worked examples toward independent problems by gradually removing support; asking students to explain the principle strengthens the transition. Teacher roles progress "Watch how I choose the step" -> "You choose the next step" -> "Now choose the method without my help." | Research support (worked-example fading + self-explanation) | "Success on substantially different problems is not automatic." "A highly entertaining explanation that never reaches the third stage is incomplete as a problem-solving lesson." | Msg 08 s1.3; ledger P04 https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/ | S03, S06, S10 |
| E-C04 | **s1.4** Questions should cause thinking, not create the appearance of interaction. Self-explanation research supports prompts asking learners to explain relationships; retrieval-practice research supports recall/application over repeated exposure. Prefer "Why did that coefficient change both atom counts?" over "Understood? Great!" | Research support (self-explanation meta-analysis; retrieval-practice meta-analysis) | "Neither establishes an ideal fixed number of questions per video." Ledger P05: specific relational explanations, "not simply repeating sentences"; ledger P06: "effects depend on task, feedback and other implementation details". | Msg 08 s1.4; ledger P05 (Bisra et al., 2018) https://link.springer.com/article/10.1007/s10648-018-9434-x ; ledger P06 https://pubmed.ncbi.nlm.nih.gov/33683913/ | S03, S06 |
| E-C05 | **s1.5** Feeling that a lesson was easy is not the same as learning. University Physics experiment (active vs passive instruction). Desired reaction refined to "That finally makes sense - and I can show that it makes sense by solving the next question." | Controlled experiment (university) | "It shows why fluency and confidence alone are unreliable success measures"; "does not mean difficulty is always productive." Ledger P07: "passive fluency can produce misleadingly positive feelings of learning." | Msg 08 s1.5; ledger P07 https://pubmed.ncbi.nlm.nih.gov/31484770/ | S03, S02 |
| E-C06 | **s1.6** Neuroscience does not supply a "charisma formula". Curiosity research links high-curiosity states with memory benefits and reward-region / hippocampal activity. Fixed claims about everyone losing attention after a number of seconds/minutes "are not sound production rules". | Mechanistic evidence (fMRI) | The experiments "do not prescribe a dopamine-triggering joke, colour, sound, or cliffhanger schedule." Ledger P09: "Trivia/fMRI findings are not a recipe for dopamine-triggering edits or guaranteed exam gains." "Use the research to design meaningful thinking - not to decorate production decisions with brain terminology." | Msg 08 s1.6; ledger P09 (Gruber et al., 2014) https://pubmed.ncbi.nlm.nih.gov/25284006/ ; ledger P13 https://pubmed.ncbi.nlm.nih.gov/28145268/ | S03, S02 |
| E-C07 | **s3.1** The explanation ladder (familiar observation -> visual relationship -> plain language -> formal language -> worked reasoning -> reduced support -> independent application -> verification) "implements the broader multimedia goal of helping learners select relevant information, organize it, and connect it with existing knowledge". | Proposed structure grounded in multimedia theory | It is a "proposed structure", not a tested sequence. Ledger P16: multimedia theory is "not a mandate for constant animation". | Msg 08 s3.1; ledger P16 (Mayer, 2024) https://link.springer.com/article/10.1007/s10648-023-09842-1 | S03, S06 |
| E-C08 | **s3.3** Analogies need a written contract: what corresponds -> what does not -> where the explanation returns to science. "Reject an analogy when it needs more explanation than the concept itself." | "Consistent with established teaching-with-analogies approaches" | Ledger P15: "Teacher/research resource: explicit mappings and limitations are important safeguards" - not an effect-size result. The sandwich analogy "does not explain reaction conditions or how bonds rearrange" (msg 08 s3.3). | Msg 08 s3.3; ledger P15 (Glynn et al., 1994) https://eric.ed.gov/?id=ED378554 ; `references/analogy_card.example.json` (status `DRAFT_HUMAN_REVIEW_REQUIRED`) | S03, S06 |
| E-C09 | **s4.1** Dora-inspired interaction: borrow "inviting a response and leaving space for it", not the preschool register. | Preschool study (58 four-year-olds) | "Research involving preschoolers and prerecorded questions cannot establish the best interaction frequency for adolescents." | Msg 08 s4.1; ledger P10 https://pubmed.ncbi.nlm.nih.gov/33013552/ | S03, S05 |
| E-C10 | **s4.2** Starting interaction schedule: three or four brief predictions + two or three substantial pauses; "often places an invitation to think approximately every 75-120 seconds". | **Production hypotheses** | "Not a scientific attention-reset interval." Place interactions at conceptual boundaries, not where a stopwatch demands. | Msg 08 s4.2; msg 04 s6.2 ("This interval is a design hypothesis") | S03, S05, S10 |
| E-C11 | **s5.1** Humour forms (tempting shortcut exposed, harmless observation, relatable exam friction, light diagram reassurance, brief personification). | Creative examples | "These are creative examples, not experimentally validated lines." | Msg 08 s5.1 | S03, S06 |
| E-C12 | **s5.2** Humour ceiling: "up to three to five short light moments", generally "less than about 25 seconds in total"; zero is acceptable. Interesting-but-irrelevant additions can hinder learning. | **Editorial starting points** | "Research does not identify an optimal number of jokes in a ten-minute STEM lesson." Removing distracting comedy is not a reason to remove attractive design or all personality. | Msg 08 s5.2; see E-B02 and ledger P17 https://pmc.ncbi.nlm.nih.gov/articles/PMC10176302/ | S03, S06, S10 |
| E-C13 | **s5.5** Hindi / Assamese optional and audience-led; one multilingual-teaching study (eight secondary English teachers). | Case study | "Does not establish an ideal percentage of code-switching for STEM videos"; do not assume Hindi is universally comfortable for an Assam audience. | Msg 08 s5.5; ledger P18 https://www.tandfonline.com/doi/full/10.1080/01434632.2022.2045300 | S03, S05 |
| E-C14 | **s6.1** Feedback structure: what was correct -> what needs attention -> what to do next. | Meta-analysis with "substantial variation between implementations" | "'Feedback works' should not be interpreted as 'any praise improves learning.'" Ledger P08: "Specific information matters; no guarantee from praise alone." | Msg 08 s6.1; ledger P08 (Wisniewski, Zierer & Hattie, 2020) https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full | S03, S05 |
| E-C15 | **s9.1** Choose a teacher voice, not a promotional voice; modern TTS vs human no significant difference in one comparison; synthetic enthusiasm study (244 participants). | Single studies | See E-B05, E-B06. "Do not assume one gender, accent, or pitch is best for learning." | Msg 08 s9.1; ledger P11, P12 | S05, S03 |
| E-C16 | **s9.3** Starting pacing: ordinary English ~130-155 active wpm; dense notation ~105-125; important distinction ~1-2 s; simple prediction ~4-8 s; ~1,100-1,250 words for ten minutes. | **Production targets to audition** | "Not established universal optima." "Do not accelerate the science simply to meet a word budget." | Msg 08 s9.3 (compare E-G05 for cross-message variants) | S03, S05, S10 |
| E-C17 | **s9.4** Editorial cues (`[CURIOUS]`, `[BEAT:0.35]`, `[THINK:6]`...) are ExamLeaf metadata, not TTS syntax. Current ElevenLabs documentation: "Eleven v4 and v3 do not support SSML break tags"; exact thinking time belongs in the video timeline. | Provider-documentation fact (checked 2026-10-13) | Ledger T05/T06: Google SSML break/prosody controls are "model-dependent; confirm selected voice support". | Msg 08 s9.4; ledger T05 https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices , T06 https://cloud.google.com/text-to-speech/docs/ssml | S05, S06 |
| E-C18 | **s9.4 / s12** Captions are an accessibility requirement; "A passing linter does not establish correctness, accessibility or learning efficacy" (pack README). | Standards guidance (WCAG 2.2) | Captions must not reveal an answer before the attempt; "do not remove access in the name of conversational delivery" (ledger T07). | Msg 08 s9.4; ledger T07 https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html | S04, S05, S07 |
| E-C19 | **s11.4** Review roughly the previous twenty scripts as an "initial editorial window" for repetition. | **Initial editorial window** (hypothesis) | "Do not replace stable scientific terminology with random synonyms." | Msg 08 s11.4 | S06, S07 |
| E-C20 | **Starter-pack status** (msg 08 intro, pack README): ten custom Skill drafts, a lesson JSON and a script checker; checker passed **12 local structural tests**. | Executed: structural tests only | Skills "have not been evaluated through Claude/Codex runs"; the sample "has not been voiced, rendered, or tested with students"; `sample_structural_check.json`: `"academic_approval": false`, `"audio_timing_measured": false`. | Msg 08 intro; `ledgers/super_teacher_pack/evals/*`; `pack_readme/README.md` | S03, S06, S10 |

## Part D - Message 02 section 8 ("Learning science: engagement that produces understanding")

Message 02 is the earliest of the six responses; message 04 later tightens several of these statements (see Part K, item 2).

| ID | Claim / principle | Evidence label (as the source states it) | Does NOT establish | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-D01 | **Retrieval practice**: ask students to recall or solve before revealing the answer. | "Practice testing is strongly supported; in-video testing has also reduced mind-wandering and improved retention in studied lecture settings." | Msg 02 s8 "Important limitation": findings from university lectures or laboratory tasks "do not automatically establish the best pacing for Assam Class 10 and 12 students. Use them as design foundations, then test with your actual audience." (Msg 04 s6.3 later qualifies the in-video-testing statement.) | Msg 02 s8; Dunlosky et al. review and interpolated-testing research **URLs not preserved**; Yang 2021 https://pubmed.ncbi.nlm.nih.gov/33683913/ | S02, S03 |
| E-D02 | **Distributed practice**: short follow-up questions after the lesson and on later days. | "Supported broadly; the exact spacing should depend on the retention goal and material." | A universal schedule. | Msg 02 s8; Cepeda 2006 https://pubmed.ncbi.nlm.nih.gov/16719566/ | S02 |
| E-D03 | **Segmentation and pre-training**: introduce essential symbols first; divide the lesson into coherent sections. | "Helps manage essential processing, especially when students can control pacing." | A fixed section length. | Msg 02 s8; multimedia-learning research **URL not preserved** (nearest https://link.springer.com/article/10.1007/s10648-023-09842-1, inferred) | S02, S04 |
| E-D04 | **Worked examples with fading**: complete solution -> remove selected steps -> require independent solving. | "Appropriate scaffolding; its effectiveness depends on prior knowledge and task design." | Transfer to unfamiliar problems (see E-A04). | Msg 02 s8; https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/ | S02, S03 |
| E-D05 | **Signalling and spatial/temporal alignment**: highlight the part being explained; place labels beside it. | "Useful for guiding attention without adding unrelated information." | Constant stimulation: "Multimedia-learning research supports coherence and signalling, not constant stimulation." | Msg 02 s8 (multimedia-learning research; **URL not preserved**) | S02, S04 |
| E-D06 | **Confidence should be earned through observable success** ("I understand the representation" -> "I can complete a step" -> "I can solve a related problem without help"); avoid "This is easy", "Only geniuses get this", "full marks are guaranteed". | Growth-mindset findings described as **heterogeneous** | They "do not justify promising that motivational wording alone improves attainment." | Msg 02 s8. **URL not preserved** | S02, S03 |
| E-D07 | **Reduce overload without removing necessary thinking**: keep reference diagram/equation visible; remove redundant prose and competing highlights. | Multimedia-learning research (coherence, signalling) | "The goal is not to eliminate effort." | Msg 02 s8. **URL not preserved** | S02, S04 |
| E-D08 | **Ten minutes is a format target, not a scientific law.** Do not stretch a six-minute idea or compress a difficult chapter by speaking faster; a chapter needing two lessons gets two. | Format decision | "Published observations about shorter-video engagement should not be interpreted as a universal attention-span limit or proof that longer explanations cannot work." Also in authoring contract: "No script can promise every learner will master any chapter in ten minutes." | Msg 02 s8; msg 04 s6.6; `authoring_contract.md` | S02, S03, S04, S10 |
| E-D09 | **Evaluate learning, not "addictiveness"**: track immediate recall, delayed recall, unprompted problem-solving, transfer, confidence calibration. | Evaluation design principle | "A student watching continuously while learning little is not a successful outcome." | Msg 02 s8, s14 phase G | S02, S08, S10 |
| E-D10 | **Supporting literature named in s8**: Dunlosky and colleagues' review; research on interpolated testing during video lectures; multimedia-learning research on segmentation/pre-training; worked-example research. | Named, not linked | Which specific paper backs which row was not preserved (tokens only). | Msg 02 s8 **URLs not preserved** | S09 |

## Part E - Other evidence claims inside message 04 (sections 2-10) and message 12

Message 04 sections 2-10 carry many further evidence statements beyond the section 1 table. They are registered here so that none is lost; every limit is the source's own.

| ID | Claim / principle | Evidence label (as the source states it) | Does NOT establish | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-E01 | **s2.1** There is no universal attention countdown. Insert a meaningful change when the learner needs a different mental operation, not because "a timer says attention has expired". | Review: the 10-15-minute lecture limit "rests on a weak evidential foundation" | "This does not mean fatigue and mind-wandering are imaginary; it means they are not governed by one universal cutoff." | Msg 04 s2.1; ledger P13 https://pubmed.ncbi.nlm.nih.gov/28145268/ | S02, S04 |
| E-E02 | **s2.2** Attention is several interacting functions (alerting, orienting, executive control). Used to design readiness, selection, goal maintenance and monitoring responses. | Neuroscience distinction | "These are design applications of the distinction, not claims that a particular graphic directly activates a particular brain network." | Msg 04 s2.2. **URL not preserved** | S02 |
| E-E03 | **s2.3** Working memory is limited but "four objects per screen" is not a law. Proposed rule: count **unexplained relationships**, not objects. | Working-memory research supports limits; performance depends on attention, task demands, prior knowledge, grouping | The "four chunks" literature "does not establish that a video must contain no more than four visible objects." | Msg 04 s2.3. **URL not preserved** | S02, S04 |
| E-E04 | **s2.4** Attention is not memory (noticing -> interpreting -> connecting -> retrieving -> retaining and transferring); sleep/consolidation research is why a ten-minute video is not a complete long-term intervention. | Research on sleep and memory consolidation (cited, not linked) | "The video should initiate a learning cycle, not claim to finish it." A feeling of clarity does not mean the information is permanently secure. | Msg 04 s2.4. **URL not preserved** | S02, S03 |
| E-E05 | **s2.5** Boredom is not simply "too little stimulation"; it can reflect difficulty engaging attention or lack of perceived meaning; both too little and too much challenge contribute. | Research models | Adding visual excitement is not the default fix; "A calmer scene can therefore be more engaging intellectually than a busier one." | Msg 04 s2.5. **URL not preserved** | S02, S04 |
| E-E06 | **s2.6** Curiosity: high-curiosity trivia answers better remembered, with incidental-information benefits; reward-region and hippocampal involvement. | fMRI study (mechanistic) | It does **not** establish that a cliffhanger releases a measurable dopamine "dose", that a colour activates a learning state, or that surprise every few seconds improves school examination performance. | Msg 04 s2.6; ledger P09 https://pubmed.ncbi.nlm.nih.gov/25284006/ | S02, S03 |
| E-E07 | **s3.1** Cognitive load theory: separate demands of the material from demands of presentation; prior knowledge changes them. | Theory-based | "Do not confuse 'lower cognitive load' with 'no thinking.'" | Msg 04 s3.1. **URL not preserved** | S02, S04 |
| E-E08 | **s3.4** Self-explanation prompts have a positive average effect (meta-analysis). Prefer "Why must the temperature remain unchanged in this comparison?" over "Do you understand?" | Meta-analysis | "A useful self-explanation requires more than asking students to repeat a sentence." | Msg 04 s3.4; ledger P05 https://link.springer.com/article/10.1007/s10648-018-9434-x | S02, S03 |
| E-E09 | **s4.5** Captions support deaf/hard-of-hearing learners and some second-language viewers; provide selectable captions, a transcript and a protected caption area. | Accessibility standard + research on benefits | "That does not mean every learner benefits equally from every caption configuration." Avoid stacking full-narration paragraph + animated diagram + equation + karaoke captions. | Msg 04 s4.5; https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html ; research **URLs not preserved** | S04, S05, S07 |
| E-E10 | **s4.2 (dark theme)** Optional dark theme `#101826` / `#EAF0F6`. | Offered "and test[ed]" | "Research showing advantages for dark text on light backgrounds often concerns tasks such as proofreading, not long-term learning or every viewing environment." | Msg 04 s4.2. **URL not preserved** | S04, S02 |
| E-E11 | **s4.4** Phone readability arithmetic: 64 px source text at 360 px display width is about 12 px; 88 px is about 16.5 px. | Arithmetic (displayed size = source size x 360/1920) | Typography numbers are "pilot targets, not accessibility rules mandating a particular font size." | Msg 04 s4.4; msg 02 s9 | S04 |
| E-E12 | **s5.5** Seductive details concern "interesting but instructionally irrelevant information"; implication: remove what competes with the explanation, not produce ugly videos. | Experimental evidence (ledger P17) + 2026 meta-analysis (E-B02) | Does not support removing attractive design. | Msg 04 s5.5; ledger P17 https://pmc.ncbi.nlm.nih.gov/articles/PMC10176302/ | S02, S04 |
| E-E13 | **s6.4** Handwriting vs typing: do not tell students to copy the entire narration; permit typing / oral explanation / accessible alternatives. | A replication and extension "found inconsistent differences" | "Concluded that the superiority claim was premature" - no blanket claim that handwriting is superior. | Msg 04 s6.4. **URL not preserved** | S02, S04 |
| E-E14 | **s6.5** Drawing can support learning when it is a reasoning task; supply a partial outline when drawing demands obscure the science. | 2025 review: "mixed findings and important boundary conditions" | Effectiveness "depends on task design, the kind of representation, and learner skill". | Msg 04 s6.5. **URL not preserved** | S02, S03 |
| E-E15 | **s7.4** No background music in the core explanation as the initial default. | **Conservative production choice** | "Not a claim that music always harms learning." Test any musical version against silence on comprehension and listening effort. No gender, accent, pitch or breathiness is inherently optimal without audience testing. | Msg 04 s7.4; msg 02 s10 | S05, S04 |
| E-E16 | **s8.1** Calibrated confidence: effort distorts subjective judgements (college Physics study); response matrix for correct/incorrect x confident/unsure. | Controlled study (see E-B13) | "This does not mean any difficult experience is productive." | Msg 04 s8.1 | S02, S03, S10 |
| E-E17 | **s8.2** Competence / control / value (self-determination and control-value theories). | Theory; broad evidence "associative" | "A few interface choices should not be advertised as a proven motivational intervention." Do not remove exam goals in pursuit of "pure intrinsic motivation". | Msg 04 s8.2. **URLs not preserved** | S02, S03 |
| E-E18 | **s8.5** Anxiety and working memory: "reliable association between anxiety and poorer working-memory performance". | Meta-analysis, "important variation and methodological limitations" | "Videos should not be presented as treatment for persistent anxiety." Goal: avoid adding threat (no countdowns, public comparisons, humiliating errors). | Msg 04 s8.5. **URL not preserved** | S02, S03 |
| E-E19 | **s9.1** Prequestioning / genuine knowledge gap as an opening. | Research "supports potential learning benefits" | "Effects depend on the questions and what is subsequently taught"; questions "can direct attention toward selected information rather than improving everything equally". Do not withhold an essential answer to extend watch time. | Msg 04 s9.1. **URL not preserved** | S02, S03 |
| E-E20 | **s9.3** Refutation: explicitly identify and correct misconceptions (principle -> misconception -> why it fails -> better model -> new application). | Refutation-text research | Supports explicit correction "rather than assuming that presenting the correct statement will always displace the incorrect one". | Msg 04 s9.3. **URL not preserved** | S02, S03, S06 |
| E-E21 | **s10** Learning styles: do not assign students to fixed "visual," "auditory," or "kinaesthetic" learning styles. | **Not supported** | "Preferences and accessibility needs are real; evidence does not support the general claim that matching instruction to a declared learning style improves learning." | Msg 04 s10. **URL not preserved** | S02, S04 |
| E-E22 | **s11** Ohm's-law 600-second blueprint: about seven persistent layouts, 41 instructional beats, four brief predictions, three learner-controlled pauses. | **Worked example / hypothesis** | "The exact second boundaries remain hypotheses." A Biology process, Chemistry mechanism or hard Class 12 derivation "should use the same principles without being forced into the identical timing pattern." The scientific model is an ohmic resistor under constant relevant conditions; textbook treatment governs (cited, not linked). | Msg 04 s11 | S02, S10 |
| E-E23 | **msg 12 s6** Vocal enthusiasm x visual cues (2024 multimedia study). | Context-dependent effects | "Research does not establish that maximum enthusiasm is optimal"; benefits of vocal enthusiasm and visual cues are not additive when intensified together (Voice_Identity_Guide: "separate benefits ... not additive benefits when combined"). | Msg 12 s6; `Voice_Identity_Guide.md` "Evidence boundaries"; https://onlinelibrary.wiley.com/doi/10.1111/jcal.13049 | S05, S03 |
| E-E24 | **msg 12 s11.2** ASR vs forced alignment answer different questions; "Zero word error rate and a successful alignment do not prove correct STEM pronunciation." | Engineering reasoning from tool documentation | Pitch tracks / neural "naturalness scores" "should not automatically reject a voice because of accent or approve a lesson because it scores highly." | Msg 12 s11.2, s11.4; WhisperX https://github.com/m-bain/whisperX ; MFA docs https://montreal-forced-aligner.readthedocs.io/en/latest/ | S05, S07 |
| E-E25 | **msg 12 s8 (script example)** Textbook-vs-ExamLeaf version of the coefficient/subscript lesson. | Example script | Msg 12 s8 itself notes: *"The citation above concerns the tool project rather than chemistry and should not be used to establish the chemistry claim; the complete example's scientific source is recorded in the downloadable script."* The two Runway auditions "differ in wording, length, and expressive instructions ... not a controlled A/B experiment". | Msg 12 s8, s14 B; `Audition_and_Evaluation.md` | S05, S10 |

## Part F - Super Teacher `Research_Ledger.md` (all 29 entries: 18 research, 4 subject, 7 tool/standard)

Source: `ledgers/super_teacher_pack/references/Research_Ledger.md` (pack `ExamLeaf_Super_Teacher`, checked 13 October 2026). Ledger header, verbatim: *"Checked 13 October 2026. This is a targeted research synthesis, not a preregistered systematic review. Dates are publication dates where distinguished from online-first. Exact pacing/humour prescriptions are production hypotheses."*

For P-entries the "Evidence label" is the study design/finding clause and "Does NOT establish" is the ledger's own limiting clause - both are substrings of the ledger text (checked mechanically). For S and T entries the label is the ledger's citation line and the right-hand cell is the ledger's complete note.

| ID | Claim / principle (ledger title) | Evidence label (design as stated in ledger) | Does NOT establish / limit (ledger) | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-F-P01 | **P01** Conversational personalization (Mayer et al., 2004) | Three narrated-animation experiments: conversational wording improved transfer, not retention. | Not proof that slang, fake intimacy or constant informality helps. | Ledger P01; https://eric.ed.gov/?id=EJ684999 | S03, S05, S06 |
| E-F-P02 | **P02** Instructional humour review (Zhou & Lee, 2025) | Review finds a complex, mixed achievement literature | Perceived enjoyment and achievement must be separated. | Ledger P02; https://pmc.ncbi.nlm.nih.gov/articles/PMC11814177/ | S03, S06 |
| E-F-P03 | **P03** Related versus aggressive teacher humour (Learning and Instruction 102, 2026, 102311) | Two randomized video-lesson studies, 206 experts and 325 students. Socio-emotional/motivational ratings improved with course-related humour | Do not infer delayed achievement gains. | Ledger P03; https://www.sciencedirect.com/science/article/pii/S095947522500235X | S03, S10 |
| E-F-P04 | **P04** Worked examples and fading (Atkinson, Renkl & Merrill, 2003) | Near-transfer support | Far transfer is not automatic. Include explicit explanation of principles. | Ledger P04; https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/ | S02, S03, S06 |
| E-F-P05 | **P05** Self-explanation (Bisra et al., 2018) | Meta-analysis of prompts | Specific relational explanations, not simply repeating sentences. | Ledger P05; https://link.springer.com/article/10.1007/s10648-018-9434-x | S02, S03 |
| E-F-P06 | **P06** Retrieval practice (Yang et al., 2021) | Classroom meta-analysis | Effects depend on task, feedback and other implementation details. | Ledger P06; https://pubmed.ncbi.nlm.nih.gov/33683913/ | S01, S02, S03 |
| E-F-P07 | **P07** Perceived versus actual learning (Deslauriers et al., 2019) | University Physics experiment | Passive fluency can produce misleadingly positive feelings of learning. | Ledger P07; https://pubmed.ncbi.nlm.nih.gov/31484770/ | S01, S02, S03 |
| E-F-P08 | **P08** Feedback (Wisniewski, Zierer & Hattie, 2020) | Meta-analysis with substantial variation. | Specific information matters; no guarantee from praise alone. | Ledger P08; https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full | S02, S03, S05 |
| E-F-P09 | **P09** Curiosity and memory (Gruber et al., 2014) | Trivia/fMRI findings | Are not a recipe for dopamine-triggering edits or guaranteed exam gains. | Ledger P09; https://pubmed.ncbi.nlm.nih.gov/25284006/ | S02, S03 |
| E-F-P10 | **P10** Prerecorded response prompts (Gaudreau et al., 2020) | 58 four-year-olds | Preschool story-reading cannot establish optimal teen lesson design. | Ledger P10; https://pubmed.ncbi.nlm.nih.gov/33013552/ | S03, S05 |
| E-F-P11 | **P11** Synthetic voice comparison (Dincer, 2022) | Modern TTS and human voice did not differ significantly in this study | Not proof of equivalence for every task. | Ledger P11; https://www.ijopr.com/article/the-voice-effect-in-multimedia-instruction-revisited-does-it-still-exist-12116 | S05 |
| E-F-P12 | **P12** Synthetic voice enthusiasm (Liew et al., 2023; online 2022) | 244 university participants; some emotion/load effects | No improved immediate retention or transfer. | Ledger P12; https://pubmed.ncbi.nlm.nih.gov/35967831/ | S05, S03 |
| E-F-P13 | **P13** Attention-span claims (Bradbury, 2016) | Review challenges fixed 8-second and 10–15-minute rules | Does not deny attention fluctuation. | Ledger P13; https://pubmed.ncbi.nlm.nih.gov/28145268/ | S02, S03 |
| E-F-P14 | **P14** Spacing (Cepeda et al., 2006) | Distributed verbal practice synthesis | Exact spacing depends on retention goal and material. | Ledger P14; https://pubmed.ncbi.nlm.nih.gov/16719566/ | S02, S10 |
| E-F-P15 | **P15** Analogies (Glynn et al., 1994) | Teacher/research resource | Explicit mappings and limitations are important safeguards. | Ledger P15; https://eric.ed.gov/?id=ED378554 | S03, S06 |
| E-F-P16 | **P16** Multimedia theory (Mayer, 2024) | Selecting, organizing and integrating relevant information | Not a mandate for constant animation. | Ledger P16; https://link.springer.com/article/10.1007/s10648-023-09842-1 | S02, S03 |
| E-F-P17 | **P17** Irrelevant details (Kienitz et al., 2023) | Experimental seductive-details evidence | Relevant visual beauty is not the same as irrelevant decoration. | Ledger P17; https://pmc.ncbi.nlm.nih.gov/articles/PMC10176302/ | S02, S03, S04 |
| E-F-P18 | **P18** Indian multilingual teaching (Anderson, 2024; online 2022) | Case study of eight secondary English teachers | Not causal evidence for a fixed Hinglish proportion in STEM. | Ledger P18; https://www.tandfonline.com/doi/full/10.1080/01434632.2022.2045300 | S03, S05 |
| E-F-S01 | **S01** Chemical balancing | OpenStax Chemistry 2e, 4.1 | Scientific check for coefficients, fixed species, atom conservation and simplest ratios; sample script is original. | Ledger S01; https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations | S03, S10 |
| E-F-S02 | **S02** Current and drift | OpenStax University Physics 2, 9.2 | Doorway analogy is only about flow rate and counting, not signal propagation. | Ledger S02; https://openstax.org/books/university-physics-volume-2/pages/9-2-model-of-conduction-in-metals | S03, S06 |
| E-F-S03 | **S03** Chain rule | OpenStax Calculus 1, 3.6 | Compose rate factors; examples should be independently verified. | Ledger S03; https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | S03, S10 |
| E-F-S04 | **S04** Enzymes | OpenStax Biology 2e, 6.5 | Activation-energy reduction and induced-fit limits to rigid lock/key stories. | Ledger S04; https://openstax.org/books/biology-2e/pages/6-5-enzymes | S03 |
| E-F-T01 | **T01** Claude Code Skills | Official documentation | Project discovery .claude/skills; SKILL.md; local permission and execution rules remain separate. | Ledger T01; https://code.claude.com/docs/en/skills | S06 |
| E-F-T02 | **T02** Codex Skills | Official documentation | Local repository discovery .agents/skills; shared standard content is not identical invocation configuration. | Ledger T02; https://developers.openai.com/codex/skills | S06 |
| E-F-T03 | **T03** Agent Skills standard | Official specification | Portable name/description frontmatter; supporting references and evals. | Ledger T03; https://agentskills.io/specification | S06 |
| E-F-T04 | **T04** Skill creation/evaluation | Anthropic official repository | Use evaluated prompts and negative examples. No third-party Skill files are copied into this pack. | Ledger T04; https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | S06 |
| E-F-T05 | **T05** ElevenLabs directing | Official best practices | Checked 2026-10-13: v3/v4 do not support SSML break tags; exact pauses should be renderer controlled. | Ledger T05; https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices | S05, S06 |
| E-F-T06 | **T06** Google SSML | Official documentation | Break/prosody controls are model-dependent; confirm selected voice support. | Ledger T06; https://cloud.google.com/text-to-speech/docs/ssml | S05 |
| E-F-T07 | **T07** Captions | W3C WCAG 2.2 guidance | Provide accurate accessible captions; do not remove access in the name of conversational delivery. | Ledger T07; https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html | S04, S05, S07 |

Also in the Super Teacher pack - `references/authoring_contract.md` ("Evidence versus production choices"): *"Retrieval, worked examples, selective signalling and feedback have a research foundation. Effects depend on implementation. Exact joke counts, interaction intervals, word rates and creative devices are unvalidated production settings until tested with ExamLeaf learners. No script can promise every learner will master any chapter in ten minutes. Missing prerequisites require repair or smaller scope."* And: *"Unverified sources, scientific implications, pronunciation, translations and any answer marked correct require review. Automated structure checks cannot approve science or humour. Human subject review plus full rendered-video review remain mandatory."* (Used in S03, S06, S07.)

## Part G - Production hypotheses (explicitly *not* evidence)

Every number below is a starting specification the source itself calls a hypothesis, target, default or assumption. They are listed so nobody mistakes them for findings. "Variants" shows where two messages give different numbers (see also Part K).

| ID | Parameter | Value(s) as stated | Label as stated | Variants across messages | Source | Used in |
|---|---|---|---|---|---|---|
| E-G01 | Substantial motion share | 25-35% of runtime | "untested starting budget, not a learning-science ratio" | none | Msg 04 s5.2 | S04, S10 |
| E-G02 | Layout persistence | stable 20-60 s or longer | production choice | none | Msg 04 s5.3 | S04 |
| E-G03 | Animation timings | transition 150-300 ms; highlight 300-600 ms; equation transform 0.8-1.5 s; hold 2-4 s | "All are production hypotheses." Never change a physical simulation to satisfy a timing rule. | same ranges in msg 02 s9 (hold wording differs) | Msg 04 s5.3; msg 02 s9 | S04 |
| E-G04 | Interaction cadence | 2-3 substantial pauses + 3-4 brief predictions; an invitation to think about every 75-120 s | "design hypothesis" / "production hypotheses, not a scientific attention-reset interval" | consistent in msgs 04, 08, 12 | Msg 04 s6.2; msg 08 s4.2; msg 12 s7.2 | S03, S05, S10 |
| E-G05 | Narration pace | ordinary English 130-155 wpm; recap 145-165; dense symbolic slower | "starting points for English-language pilots"; "Validate other languages separately" | Ordinary: 130-150 (msg 02 s10) vs 130-155 (msgs 04, 08, 10, 12). Dense: 90-120 (msg 04 s7.2) vs 105-125 (msgs 08 s9.3, 12 s7.1, Voice_Identity_Guide). | Msg 04 s7.2; msg 08 s9.3; msg 12 s7.1; msg 02 s10 | S05, S03 |
| E-G06 | Narration word budget for ten minutes | ~1,050-1,250 (msg 04); ~1,100-1,250 (msgs 08, 10, 12, Voice_Identity_Guide); ~1,150-1,300 (msg 02) | "reasonable initial writing budget"; "actual audio determines duration" | three different ranges | Msg 04 s7.2; msg 08 s9.3; msg 10 s7.2; msg 02 s10 | S03, S05 |
| E-G07 | Pause lengths | phrase 0.3-0.6 s (msg 04) / 0.2-0.6 s (msg 12); contrast 0.8-1.5 s; completed transform/diagram 2-4 s; simple prediction 5-8 s (msg 04) / 4-8 s (msgs 08, 12); writing/drawing/multistep = learner-controlled | "proposed defaults, not experimentally established optima"; "Do not use a two-second silence as evidence that students had a fair opportunity to solve a problem." | small variants as shown | Msg 04 s6.2, s7.3; msg 08 s9.3; msg 12 s7.1 | S05, S03, S10 |
| E-G08 | Humour budget | 0-5 short moments, < ~25 s total | "editorial starting points" | none | Msg 08 s5.2 | S03 |
| E-G09 | Typography, 1920x1080 master | msg 04: labels 88-96 px, equations 112-144, headings 104-128. Msg 02: labels 64-72, equations 84-112, headings 72-88, safe margin 96 px, caption area ~190 px. | "pilot targets"; "production choices, not universal research-derived optima" | msg 04 (the later message) gives larger sizes than msg 02; neither set is tested | Msg 04 s4.4; msg 02 s9 | S04 |
| E-G10 | Palette | `#F7F9FC` bg, `#14213D` text, `#526074`, `#185ABD`, `#087986`, `#9A5B00`, `#6E44AA`, `#B42318`; dark `#101826`/`#EAF0F6` | "design specifications, not neuroscientific optima" | purple 6.48:1 vs 6.49:1; msg 10 repeats four of the colours | Msg 04 s4.2; msg 02 s9; msg 10 s7.2 | S04 |
| E-G11 | Loudness / audio masters | -16 LUFS integrated, true peak <= -1 dBTP; 48 kHz mono 24-bit archival WAV | "ExamLeaf production target, not a claimed universal platform requirement" | none | Msg 02 s10; msg 12 s11.5 | S05, S07 |
| E-G12 | Delayed-assessment interval | seven days | "a study-design choice, not the only valid measure of retention" | none | Msg 04 s12.1 | S10 |
| E-G13 | Practice schedule after the video | end of lesson; next day; ~3 days; ~1 week; later by exam timing | "adjustable hypotheses" | none | Msg 04 s9.4 | S02, S10 |
| E-G14 | Ten-minute duration | 600 s | "a format target, not a scientific law"; "planning target, not measured audio" | none | Msg 02 s8; msg 04 s6.6; `authoring_contract.md` | S02, S03, S04 |
| E-G15 | Student-pause study time | 3 pauses of a minute turn ten minutes into at least thirteen | arithmetic; label the product "10-minute revision video, with optional practice pauses" | none | Msg 04 s6.6 | S02, S10 |
| E-G16 | Business tests: free chapters, Reels frequency and length, conversion, CAC, activation, sell-through | three free chapters, Reels 4-5/week at 20-45 s, qualified-learner-to-order 3-8%, CAC INR 100-120, activation >= 97%, sell-through 90% | "testable starting point, not a proven optimum" (free chapters); "launch experiments"; "management targets to test, not industry benchmarks" | none | Msg 06 s1.2, s6.1, s15.1 | S01, S08 |
| E-G17 | Script-repetition window | previous ~20 scripts | "initial editorial window" | none | Msg 08 s11.4 | S06, S07 |

## Part H - Planned validation experiments (how hypotheses become evidence)

None of these has been run (see `VERIFIED_vs_PROPOSED.md`). Rule from msg 04 s12.1-12.5: pick learning outcomes first; primary outcome = "Performance on a delayed, unprompted assessment containing unfamiliar but curriculum-aligned applications"; keep content-matched vs time-matched explicit; parallel items; rubric scoring blind to version; predefine analysis; report attrition and intervals; minors - minimal data, no emotion/attention surveillance; confidence calibration measured (accurate confidence, high-confidence errors, correct-but-unsure).

| ID | Comparison | Main question / outcome | Source | Status | Used in |
|---|---|---|---|---|---|
| E-H01 | Explanation-only vs explanation + retrieval and feedback (priority 1) | Does the active version improve delayed performance enough to justify extra study time? | Msg 04 s12.2 | not run | S10, S02 |
| E-H02 | Full worked examples throughout vs gradually faded support (2) | Does fading improve independent method selection? | Msg 04 s12.2 | not run | S10 |
| E-H03 | Fewer substantial checkpoints vs more frequent brief checkpoints (3) | Which pattern benefits learning without excessive interruption? | Msg 04 s12.2 | not run | S10 |
| E-H04 | Clear static sequence vs semantically equivalent animation (4) | Does motion improve understanding of this relationship? | Msg 04 s12.2 | not run | S10 |
| E-H05 | ~130 vs ~150 wpm, same explanation (5) | Who benefits from each pace; effect on study time and comprehension | Msg 04 s12.2 | not run | S10, S05 |
| E-H06 | Specific task feedback vs generic respectful feedback (6) | Does specificity improve error correction and calibration? | Msg 04 s12.2 | not run | S10 |
| E-H07 | Learner-controlled pause vs automatic answer reveal (7) | Do students attempt the task; does delayed learning improve? | Msg 04 s12.2 | not run | S10 |
| E-H08 | Copying a compact reference vs reconstruction then checking (8) | Which gives better later retrieval for time invested? | Msg 04 s12.2 | not run | S10 |
| E-H09 | Two accessible, coherent palettes (9) | Differences in reading accuracy and comfort; "Do not test an unreadable palette against a readable one and label the result 'colour psychology.'" | Msg 04 s12.2 | not run | S10, S04 |
| E-H10 | Formal vs conversational versions, equivalent science | Independent application | Msg 08 s13 | not run | S10, S03 |
| E-H11 | No humour vs a few concept-linked lines | Delayed learning, comfort, distraction | Msg 08 s13 | not run | S10, S03 |
| E-H12 | Full examples throughout vs faded support | Method selection without hints | Msg 08 s13 | not run | S10, S03 |
| E-H13 | Steady warmth vs more variable enthusiasm | Comprehension and listening effort | Msg 08 s13 | not run | S10, S03, S05 |
| E-H14 | Audience-appropriate language versions | Understanding, terminology recall, comfort | Msg 08 s13 | not run | S10, S03, S05 |
| E-H15 | Narration study A - voice/provider audition (identical passages, normalized level, blinded, rotated; 40 term mappings + 12 connected passages; 3 viable voices per locale, 2 repeat generations) | Meaning-changing defects (release blocker); listening effort, warmth, dignity, preference | Msg 12 s14 A; `Audition_and_Evaluation.md` | not run (only two uncontrolled Runway demonstrations exist) | S05, S10 |
| E-H16 | Narration study B - script-style comparison (straightforward vs Super Teacher) holding science and study opportunity comparable | Teaching effect of style | Msg 12 s14 B | not run | S05, S10 |
| E-H17 | Narration study C - learning evaluation (immediate independent question + fresh later question) | Not preference, voice similarity, completion rate or apparent confidence | Msg 12 s14 C | not run | S05, S10 |
| E-H18 | Compositor benchmark: identical approved scenes in HyperFrames and Remotion, 16:9 and 9:16, warm-up + at least five repeats, cold vs cached, peak RSS | Correctness, reproducibility, memory, render time, repair effort, total operating cost | Msg 02 s1, s14 B; msg 10 s9; `Four_Pilots.md` | not run (HyperFrames and Remotion not installed) | S04, S10 |
| E-H19 | Business A/B tests: selected vs sequential free chapters; one-book vs two-book; digital-only availability; product-proof vs generic motivation; prediction-first vs worked-example Reel opening | Retained sales and contribution, not clicks | Msg 06 s15.2 | not run | S01 |
| E-H20 | Four complete narrated pilots (physics, chemistry, mathematics, biology) with record: academic defects, reviewer minutes, editing minutes, pronunciation repairs, render time, peak memory, generation attempts, cost, student performance on a fresh question | Promotion gate for the whole system | Msg 10 s9; `Four_Pilots.md` | not run (only 600-second beat plans exist) | S10, S08 |

## Part I - Market, regulatory and platform-policy evidence: business `Research_Source_Ledger.csv` (all 30 rows)

Source: `ledgers/business_toolkit/Research_Source_Ledger.csv` = the `Sources` sheet of the business model (`ledgers/spreadsheet_sheets_csv/ExamLeaf_Business_Model__Sources__values.csv`, banner: *"PUBLIC SOURCES CHECKED 13 OCTOBER 2026 + OPEN VALIDATION GAPS"*). Evidence label = the ledger's *Type* column; claim = *Topic* + *Support*; "Does NOT establish" = the ledger's *Limit* column.

| ID | Claim / principle (Topic: what it supports) | Evidence label (source type) | Does NOT establish / limit | Source and link(s) | Used in |
|---|---|---|---|---|---|
| E-I01 | **ASSEB structure**: Current Division I/II naming; former SEBA/AHSEC. | Official board | Verified public source; no board endorsement implied. | https://asseb.in/ | S01 |
| E-I02 | **Assam curriculum**: Current syllabus/notifications; confirm class, medium, year before publication. | Official Division I | Download authoritative curriculum and record version before writing. | https://site.sebaonline.org/ | S01, S07 |
| E-I03 | **Assam rural digital access**: Rural ages 14–16; 91.4% home smartphone; 14.6% own among smartphone-capable. | ASER 2024 state report | Survey denominator differs by question; not an all-Assam personal-phone rate. | https://asercentre.org/wp-content/uploads/2022/12/Assam-1.pdf | S01 |
| E-I04 | **Oswaal current catalogue**: Current sample-paper products and publisher-advertised digital/AI features. | Publisher | Snapshot 13 Oct 2026; CBSE products are not exact Assam equivalents. | https://oswaalbooks.com/ | S01 |
| E-I05 | **Oswaal Physics**: Class 12 Physics 15 SQP 2026–27; listed INR 499 when checked. | Publisher product | Recheck price, availability and inclusions at launch. | https://oswaalbooks.com/products/cbse-15-sample-question-papers-class-12-board-exam-physics-2026-27-based-on-latest-cbse-sqp-dated-21-sep-2026-new-questions-typologies-with-oswaal-ai | S01 |
| E-I06 | **Arihant**: Sample-paper/All in One formats, solutions and revision aids. | Publisher | Exact SKU, board and discount must be compared, not brand-wide price assumptions. | https://arihantbooks.com/ | S01 |
| E-I07 | **PW Assam**: Dedicated ASSEB Class 10 page, free content and paid offerings. | Provider | Evidence that Assam digital education is not an uncontested market. | https://www.pw.live/asseb/class-10 | S01 |
| E-I08 | **Instagram creator guidance**: Professional-dashboard Best Practices provides personalized guidance. | Meta | Does not establish a universal posting frequency or viral formula. | https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/ | S01 |
| E-I09 | **Instagram ranking**: Multiple ranking predictions/signals and personalization. | Meta | Do not claim exact signal weights or guaranteed distribution. | https://about.fb.com/news/2023/06/how-ai-ranks-content-on-facebook-and-instagram/ | S01 |
| E-I10 | **Teen advertising**: Teen advertising restrictions. | Meta | Design no behavioural retargeting to minors; recheck account policies. | https://about.fb.com/news/2023/01/age-appropriate-ads-for-teens/ | S01 |
| E-I11 | **YouTube Shorts handoff**: Related video link from Short to channel content. | YouTube Help | Feature requires appropriate account access. | https://support.google.com/youtube/answer/14075157?hl=en | S01 |
| E-I12 | **WhatsApp permission**: Permission, expectation and opt-out policy. | WhatsApp | Message templates/categories and pricing must be checked for actual account. | https://business.whatsapp.com/policy | S01 |
| E-I13 | **Gateway**: Standard 2% + GST pricing; promo excluded. | Razorpay | Actual payment-method/negotiated rates may differ. | https://razorpay.com/pricing/ | S01, S08 |
| E-I14 | **Marketplace**: Books referral at >INR250–500 is 2%; additional fees apply. | Amazon India | All-in model fee is an assumption, not the referral percentage. | https://sell.amazon.in/fees-and-pricing | S01, S08 |
| E-I15 | **Book post eligibility**: Gyan Post eligibility and conditions. | India Post | Obtain written eligibility for the exact marketed book/insert/pack. | https://www.indiapost.gov.in/mailproducts/domesticservices/gyanpost | S01, S08 |
| E-I16 | **Postal tariffs**: Published Gyan Post slabs when eligible. | India Post | Weigh actual packed SKU; no all-India exam-date delivery guarantee. | https://www.indiapost.gov.in/mailproducts/domesticservices/domestictariff | S01, S08 |
| E-I17 | **Print-price reality check**: Public short-run print and binding prices; different from ExamLeaf offset specification. | Printer | Not an ExamLeaf quote; none of the modeled unit costs are represented as quoted. | https://www.bulkprintouts.com/book-printing.html | S01, S08 |
| E-I18 | **Video delivery**: USD1/1,000 delivered minutes; USD5/1,000 stored-minute capacity. | Cloudflare | Model adds planning FX/tax and full-edition usage reserve. | https://developers.cloudflare.com/stream/pricing/ | S01, S08 |
| E-I19 | **Video access control**: Signed tokens and origin restrictions. | Cloudflare docs | Access control reduces casual sharing; does not prevent screen recording. | https://developers.cloudflare.com/stream/viewing-videos/securing-your-stream/ | S01, S07 |
| E-I20 | **Commerce**: Open-source commerce and integration capabilities. | WooCommerce | Hosting, plugins and developer upkeep are not free. | https://woocommerce.com/woocommerce/ | S01, S08 |
| E-I21 | **Fulfillment API**: Official API documentation endpoint. | Shiprocket | Obtain serviceable-pincode, weight, fee and COD/RTO account quotes. | https://apidocs.shiprocket.in/ | S01, S08 |
| E-I22 | **GST current notification**: 2025 rate/exemption notifications supersede older goods-rate notifications. | Ministry of Finance / PIB | Review current 10/2025 notification and later amendments with a CA. | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2168426 | S01 |
| E-I23 | **GST bundle classification**: Principal-supply versus mixed-supply logic. | GST Council / NACIN | No automatic nil-rate assumption for a valuable book/video package. | https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf | S01 |
| E-I24 | **DPDP rules**: Phased commencement; verifiable parental consent and limited exceptions. | MeitY / Gazette | Legal review of ExamLeaf status; do not assume an institutional exemption. | https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf | S01 |
| E-I25 | **DPDP Act**: Children and targeted-advertising/behavioural-monitoring provisions. | MeitY | Track commencement notifications; build privacy-preserving defaults now. | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf | S01 |
| E-I26 | **Education advertising**: No misleading educational guarantees, false urgency or deceptive success stories. | CCPA / PIB | Scope and detailed compliance to be reviewed for books plus instruction. | https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2073013&lang=2&reg=48 | S01 |
| E-I27 | **Retrieval learning**: Testing/quizzing supports classroom learning on average. | Meta-analysis | Not a promise of a given ExamLeaf score improvement. | https://pubmed.ncbi.nlm.nih.gov/33683913/ | S01, S02 |
| E-I28 | **Confidence vs learning**: Feeling of learning can diverge from measured learning. | Primary experiment | University context; not a direct ExamLeaf business conversion study. | https://www.pnas.org/doi/10.1073/pnas.1821936116 | S01, S02 |
| E-I29 | **Market size**: Use official class/stream/medium/district counts before a large production order. | Planning limitation | Exact 2026 participation figures were not reconciled to an official result census. | https://asseb.in/ | S01 |
| E-I30 | **Model costs and conversions**: Printing, shipping, CAC, sell-through, salaries, conversions and production workloads are estimates. | ExamLeaf planning assumptions | Replace with quotes and observed cohort data. No virality or demand forecast claimed. | Not an external source | S01, S08 |

Message 06 s3.4 (competitor comparison) and s10.1 (verified vs estimated inputs) elaborate rows E-I04 to E-I07 (competitors) and E-I13, E-I14, E-I17, E-I18 (Razorpay, Amazon, printing, Cloudflare delivery); the competitor table is reproduced in `TECHNOLOGY_DECISION_MATRIX.md` section 10 and the verified-vs-estimated table in `VERIFIED_vs_PROPOSED.md` Part E (table E1).

## Part J - Capability and pricing source ledgers (video engine `sources.csv`, narration `Sources` sheet)

These two ledgers are lists of the documentation/pricing pages the cost models and tool evaluations rest on. Each states a *scope* that doubles as its limit (e.g. *"Workflow claims; not verified income/outcome evidence"*). Columns follow the ledgers, not the six-column claim format.

### J1 - Video Engine `research/sources.csv` (14 rows)

| ID | Source | URL | Scope / use as stated (incl. limit) | Checked | Used in |
|---|---|---|---|---|---|
| E-J1-01 | Higgsfield blog | https://higgsfield.ai/blog/faceless-channel-one-prompt | Workflow claims; not verified income/outcome evidence | 2026-10-13 | S04, S08 |
| E-J1-02 | Anthropic pricing | https://platform.claude.com/docs/en/about-claude/pricing | Sonnet4.6/Opus4.6/Haiku4.5 quoted model rate inputs | 2026-10-13 | S08 |
| E-J1-03 | ElevenLabs pricing | https://elevenlabs.io/pricing/api | Published $0.10/1K character baseline; conditions may change | 2026-10-13 | S05, S08 |
| E-J1-04 | Runway pricing | https://docs.dev.runwayml.com/guides/pricing/ | Published credit rates; account/route differences explicit | 2026-10-13 | S04, S08 |
| E-J1-05 | Remotion licence | https://www.remotion.dev/docs/license/pricing | Conditional paid automation terms | 2026-10-13 | S04, S08 |
| E-J1-06 | Claude Skills | https://code.claude.com/docs/en/skills | Agent instruction packaging | 2026-10-13 | S06 |
| E-J1-07 | Claude subagents | https://code.claude.com/docs/en/sub-agents | Development agent responsibilities | 2026-10-13 | S06 |
| E-J1-08 | Codex Skills | https://developers.openai.com/codex/skills | Client Skill support; verify current discovery paths | 2026-10-13 | S06 |
| E-J1-09 | Forced alignment | https://elevenlabs.io/docs/api-reference/forced-alignment/create | Proposed external alignment API, not locally integrated | 2026-10-13 | S05 |
| E-J1-10 | Retrieval meta-analysis | https://pubmed.ncbi.nlm.nih.gov/33683913/ | 222 studies; retrieval evidence, not fixed interaction timing | 2026-10-13 | S02, S03 |
| E-J1-11 | Teacher humour study | https://www.sciencedirect.com/science/article/pii/S095947522500235X | 2026 socio-emotional results; not proof of exam gain | 2026-10-13 | S03 |
| E-J1-12 | Contrast | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | Text contrast baseline, not complete accessibility certification | 2026-10-13 | S04 |
| E-J1-13 | Kokoro weights | https://huggingface.co/hexgrad/Kokoro-82M | Apache-2.0 model card; language/voice audition still required | 2026-10-13 | S05 |
| E-J1-14 | F5-TTS | https://github.com/SWivid/F5-TTS | Code and pretrained weight licences differ | 2026-10-13 | S05 |

### J2 - Narration cost model `Sources` sheet (14 rows)

Sheet banner: *"URLs support capability or tariff facts only. Research-read does not mean successfully executed or scientifically benchmarked."*

| ID | Topic | URL / file | As of | Use as stated | Used in |
|---|---|---|---|---|---|
| E-J2-01 | Eleven pricing | https://elevenlabs.io/pricing/api | 2026-10-13 | Reference character and speech-to-speech usage rates | S05, S08 |
| E-J2-02 | Eleven v4 | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 | 2026-10-13 | Capabilities, differences, expression; no copied v2 settings | S05 |
| E-J2-03 | Eleven languages | https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support | 2026-10-13 | Model-specific Assamese/Hindi coverage; not native QA | S05 |
| E-J2-04 | Cartesia pricing | https://cartesia.ai/pricing | 2026-10-13 | Plans, allowances; large usage still needs quote | S05, S08 |
| E-J2-05 | Gemini pricing | https://ai.google.dev/gemini-api/docs/pricing | 2026-10-13 | Current and scheduled tariff; token conversion | S05, S08 |
| E-J2-06 | Gemini TTS | https://ai.google.dev/gemini-api/docs/speech-generation | 2026-10-13 | Current3.8 schema and output formats | S05 |
| E-J2-07 | OpenAI lifecycle | https://developers.openai.com/api/docs/deprecations | 2026-10-13 | New-production block for deprecated old TTS | S05, S08 |
| E-J2-08 | OpenAI replacement | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini | 2026-10-13 | Replacement pricing; no drop-in guarantee | S05, S08 |
| E-J2-09 | WhisperX | https://github.com/m-bain/whisperX | 2026-10-13 | Word alignment boundary and language resource needs | S05 |
| E-J2-10 | MFA | https://montreal-forced-aligner.readthedocs.io/en/latest/ | 2026-10-13 | Dictionary/acoustic-model alignment pipeline | S05 |
| E-J2-11 | FFmpeg | https://ffmpeg.org/ffmpeg-filters.html#loudnorm | 2026-10-13 | Two-pass loudness and true-peak processing | S05, S07 |
| E-J2-12 | Local tests | outputs/tests.txt | 2026-10-13 | 57 tests; signal fixtures, not a speech-quality benchmark | S05, S10 |
| E-J2-13 | Live auditions | docs/Audition_and_Evaluation.md | 2026-10-13 | Two Runway outputs;18 workspace credits; no local listening score | S05, S10 |
| E-J2-14 | Budget assumptions | Inputs + Methods | 2026-10-13 | Workload, GPU speed/rate, personnel rates, time, fixed/setup spend are editable estimates | S08 |

## Part K - Gaps, inconsistencies and open caveats found while building the register

These are not corrections; they are places where the sources disagree with each other or leave something unresolved. Nothing was changed in the copied sources.

1. **Citation-token mapping lost.** The six assistant messages carry opaque citation tokens; `cited_source_links.md` lists the URLs "as rendered" but not which token is which. Claims marked **URL not preserved** in Parts A-E (E-A05 partially, E-A06, E-A07, E-A08 colour papers, E-A09 praise/mindset, E-A10, E-B02, E-B08, E-B09, E-B14, E-E02-E05, E-E07, E-E09 research, E-E10, E-E13-E14, E-E16-E21, E-D01 Dunlosky, E-D03-E-D07, E-D10) cannot be traced to a link without re-running the original ChatGPT research.
2. **Message 02 s8 vs message 04 s6.3 on embedded quizzes.** Msg 02: "in-video testing has also reduced mind-wandering and improved retention in studied lecture settings." Msg 04 (later): later work "has not reproduced every benefit under every condition"; a 195-student study found no learning benefit, a 703-student study did. Treat msg 04 as the more cautious statement; both agree no fixed interval is established.
3. **The g = -0.16 meta-analysis** (March 2026, 50 studies) is not in the 18 listed learning-science links; ledger P17 (Kienitz et al., 2023, PMC10176302) is experimental seductive-details evidence, a different paper. Do not cite P17 as the source of g = -0.16.
4. **The 56-investigation / 88-comparison segmentation meta-analysis** is not individually listed; the nearest link (Springer s10648-023-09842-1) is labelled "multimedia learning / segmentation" and is Mayer 2024 in ledger P16. The mapping is inferred.
5. **Numeric variants** for pace, word budget, pause lengths and typography between messages 02, 04, 08, 10, 12 (Part G rows E-G05-E-G09) and a 6.48 vs 6.49 contrast ratio for the purple accent (E-B11). All are hypotheses; no message reconciles them.
6. **Self-flagged mis-citation in message 12 s8:** the cited link "concerns the tool project rather than chemistry and should not be used to establish the chemistry claim" (E-E25).
7. **Pricing statements differ between packs** (Sonnet/Opus/Haiku rates, ElevenLabs $0.08 vs $0.10 per 1,000 characters) - listed in `TECHNOLOGY_DECISION_MATRIX.md` section 11; neither pack explains the difference beyond the model generation named in each.
8. **Ledger URLs absent from `cited_source_links.md`, and vice versa** - see Part L. The link list is the "as rendered" page list, not a complete bibliography of the packs' own ledgers.
9. **No ledger gives a publication-quality citation for several studies** (e.g. Dunlosky review, interpolated-testing papers, working-memory, handwriting, growth-mindset, anxiety, learning-style papers). The register therefore records them by description only.
10. **Everything in the ledgers is "checked 13 October 2026".** Pricing, model lifecycle and repository state change quickly (msg 12 "Documentation drift"); re-check before reuse.

## Part L - URL cross-check: `cited_source_links.md` vs the packs' own ledgers

Mechanical comparison (trailing `/` and punctuation ignored). Ledger files scanned: 16 (listed in the generating note below). **64** URLs in `cited_source_links.md`; **141** distinct URLs in the scanned ledgers; **58** appear in both.

*Scanned:* `super_teacher_pack/references/Research_Ledger.md`; `video_engine_implementation/research/Public_Skills_Directory.md`; `video_engine_implementation/research/public_directory.csv`; `video_engine_implementation/research/sources.csv`; `video_engine_implementation/research/subject_libraries.csv`; `video_engine_implementation/docs/Higgsfield_Findings.md`; `narration_system/research/Public_Narration_Directory.md`; `narration_system/research/public_directory.csv`; `narration_system/docs/Provider_Lifecycle.md`; `narration_system/docs/Costs_and_Methods.md`; `narration_system/docs/Voice_Identity_Guide.md`; `business_toolkit/Research_Source_Ledger.csv`; `spreadsheet_sheets_csv/ExamLeaf_Narration_Cost_Model__Sources__values.csv`; `spreadsheet_sheets_csv/ExamLeaf_Narration_Cost_Model__Provider_Tariffs__values.csv`; `spreadsheet_sheets_csv/ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv`; `planning_pack/README.md`.

### L1 - Cited on the share page but not in any scanned ledger (6)

These are provider-documentation or repository pages cited in messages 02/10/12 that no pack ledger lists as a row, or URL variants of ledger entries (the FunAudioLLM CosyVoice URL redirects to the QwenAudio/CosyVoice URL the narration directory uses).

* https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe
* https://www.cartesia.ai/fr/blog/sonic-3.6
* https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech
* https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning
* https://github.com/FunAudioLLM/CosyVoice
* https://raw.githubusercontent.com/higgsfield-ai/skills/main/higgsfield-generate/SKILL.md

### L2 - In the packs' ledgers but not in `cited_source_links.md` (83)

These are real sources of the packs (documentation/pricing/policy pages) that the share-page link list omitted. They are the authoritative URLs for tool, price and market rows elsewhere in this section.

* https://3dmol.csb.pitt.edu/  - in: subject_libraries.csv
* https://about.fb.com/news/2023/01/age-appropriate-ads-for-teens/  - in: Research_Source_Ledger.csv
* https://about.fb.com/news/2023/06/how-ai-ranks-content-on-facebook-and-instagram/  - in: Research_Source_Ledger.csv
* https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/  - in: Research_Source_Ledger.csv
* https://agentskills.io/specification  - in: Research_Ledger.md
* https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-lite-tts  - in: Provider_Lifecycle.md
* https://apidocs.shiprocket.in/  - in: Research_Source_Ledger.csv
* https://arihantbooks.com/  - in: Research_Source_Ledger.csv
* https://asercentre.org/wp-content/uploads/2022/12/Assam-1.pdf  - in: Research_Source_Ledger.csv
* https://asseb.in/  - in: Research_Source_Ledger.csv
* https://aws.amazon.com/fargate/pricing/  - in: README.md
* https://biopython.org/wiki/Documentation  - in: subject_libraries.csv
* https://www.bulkprintouts.com/book-printing.html  - in: Research_Source_Ledger.csv
* https://business.whatsapp.com/policy  - in: Research_Source_Ledger.csv
* https://cloud.google.com/text-to-speech/docs/ssml  - in: Research_Ledger.md
* https://code.claude.com/docs/en/sub-agents  - in: sources.csv
* https://dev.pika.art/pricing  - in: Public_Skills_Directory.md, public_directory.csv
* https://developers.cloudflare.com/r2/pricing/  - in: README.md
* https://developers.cloudflare.com/stream/pricing/  - in: Research_Source_Ledger.csv
* https://developers.cloudflare.com/stream/viewing-videos/securing-your-stream/  - in: Research_Source_Ledger.csv
* https://developers.openai.com/api/docs/guides/text-to-speech  - in: Public_Narration_Directory.md, public_directory.csv
* https://developers.openai.com/api/docs/pricing  - in: README.md
* https://developers.openai.com/codex/skills  - in: Research_Ledger.md, sources.csv
* https://docs.cartesia.ai/build-with-cartesia/tts-models/latest  - in: Provider_Lifecycle.md, Public_Narration_Directory.md, public_directory.csv
* https://docs.dev.runwayml.com/  - in: Public_Skills_Directory.md, public_directory.csv
* https://docs.manim.community/en/stable/  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html  - in: subject_libraries.csv
* https://elevenlabs.io/docs/changelog/2026/9/28  - in: Public_Narration_Directory.md, public_directory.csv
* https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support  - in: ExamLeaf_Narration_Cost_Model__Sources__values.csv, Provider_Lifecycle.md
* https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4  - in: ExamLeaf_Narration_Cost_Model__Sources__values.csv, Provider_Lifecycle.md
* https://ffmpeg.org/ffmpeg-filters.html#loudnorm  - in: ExamLeaf_Narration_Cost_Model__Sources__values.csv
* https://ffmpeg.org/legal.html  - in: subject_libraries.csv
* https://github.com/anthropics/claude-plugins-official  - in: Public_Skills_Directory.md, public_directory.csv
* https://github.com/cartesia-ai/cartesia-mcp  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/elevenlabs/elevenlabs-mcp  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/fishaudio/fish-speech  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/ManimCommunity/manim  - in: subject_libraries.csv
* https://github.com/ManimCommunity/manim-voiceover  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv, Public_Narration_Directory.md, public_directory.csv
* https://github.com/microsoft/playwright-mcp  - in: Public_Skills_Directory.md, public_directory.csv
* https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/motion-canvas/motion-canvas  - in: Public_Skills_Directory.md, public_directory.csv
* https://github.com/openai/skills  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv, README.md
* https://github.com/openai/skills/tree/main/skills/.curated/speech  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/QwenAudio/CosyVoice  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/QwenLM/Qwen3-TTS  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/snakers4/silero-vad  - in: Public_Narration_Directory.md, public_directory.csv
* https://github.com/SYSTRAN/faster-whisper  - in: Public_Narration_Directory.md, public_directory.csv
* https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf  - in: Research_Source_Ledger.csv
* https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp  - in: Higgsfield_Findings.md, Public_Skills_Directory.md, public_directory.csv
* https://higgsfield.ai/higgsfield-api  - in: Higgsfield_Findings.md, Public_Skills_Directory.md, public_directory.csv
* https://huggingface.co/ai4bharat/indic-parler-tts  - in: Public_Narration_Directory.md, public_directory.csv
* https://www.indiapost.gov.in/mailproducts/domesticservices/domestictariff  - in: Research_Source_Ledger.csv
* https://www.indiapost.gov.in/mailproducts/domesticservices/gyanpost  - in: Research_Source_Ledger.csv
* https://katex.org/docs/supported.html  - in: subject_libraries.csv
* https://librosa.org/doc/latest/index.html  - in: Public_Narration_Directory.md, public_directory.csv
* https://lumalabs.ai/api  - in: Public_Skills_Directory.md, public_directory.csv
* https://magpylib.readthedocs.io/en/latest/  - in: subject_libraries.csv
* https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf  - in: Research_Source_Ledger.csv
* https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf  - in: Research_Source_Ledger.csv
* https://molstar.org/  - in: subject_libraries.csv
* https://montreal-forced-aligner.readthedocs.io/en/latest/  - in: ExamLeaf_Narration_Cost_Model__Sources__values.csv
* https://oswaalbooks.com/  - in: Research_Source_Ledger.csv
* https://oswaalbooks.com/products/cbse-15-sample-question-papers-class-12-board-exam-physics-2026-27-based-on-latest-cbse-sqp-dated-21-sep-2026-new-questions-typologies-with-oswaal-ai  - in: Research_Source_Ledger.csv
* https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2073013&lang=2&reg=48  - in: Research_Source_Ledger.csv
* https://www.pib.gov.in/PressReleasePage.aspx?PRID=2168426  - in: Research_Source_Ledger.csv
* https://pint.readthedocs.io/en/stable/  - in: subject_libraries.csv
* https://www.pnas.org/doi/10.1073/pnas.1821936116  - in: Research_Source_Ledger.csv, Voice_Identity_Guide.md
* https://www.pw.live/asseb/class-10  - in: Research_Source_Ledger.csv
* https://python-soundfile.readthedocs.io/  - in: Public_Narration_Directory.md, public_directory.csv
* https://raw.githubusercontent.com/anthropics/skills/main/README.md  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv
* https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md  - in: Research_Ledger.md
* https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills-manifest.json  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv, README.md
* https://raw.githubusercontent.com/K-Dense-AI/scientific-agent-skills/main/skills/sympy/SKILL.md  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv
* https://raw.githubusercontent.com/openai/skills/main/skills/.curated/speech/SKILL.md  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv
* https://raw.githubusercontent.com/remotion-dev/skills/main/README.md  - in: ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv
* https://razorpay.com/pricing/  - in: Research_Source_Ledger.csv
* https://www.rdkit.org/docs/GettingStartedInPython.html  - in: subject_libraries.csv
* https://schemdraw.readthedocs.io/en/latest/  - in: subject_libraries.csv
* https://sell.amazon.in/fees-and-pricing  - in: Research_Source_Ledger.csv
* https://site.sebaonline.org/  - in: Research_Source_Ledger.csv
* https://support.google.com/youtube/answer/14075157?hl=en  - in: Research_Source_Ledger.csv
* https://threejs.org/  - in: subject_libraries.csv
* https://woocommerce.com/woocommerce/  - in: Research_Source_Ledger.csv

### L3 - Cited-URL index: where each of the 64 URLs in `cited_source_links.md` is used

Every cited URL is referenced at least once in the synthesis documents (register row IDs; matrix section `sN`; merged public-directory row; `VERIFIED_vs_PROPOSED.md` part). 58 of them also appear in a pack ledger.

| # | Cited URL | Register rows | Matrix | Public directory | Status doc |
|---|---|---|---|---|---|
| 1 | https://eric.ed.gov/?id=EJ684999 | E-B12, E-C01, E-F-P01 | - | - | - |
| 2 | https://www.sciencedirect.com/science/article/pii/S095947522500235X | E-B04, E-C02, E-F-P03, E-J1-11 | - | - | - |
| 3 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11814177/ | E-C02, E-F-P02 | - | - | - |
| 4 | https://asu.elsevierpure.com/en/publications/transitioning-from-studying-examples-to-solving-problems-effects-/ | E-A04, E-C03, E-D04, E-F-P04 | - | - | - |
| 5 | https://link.springer.com/article/10.1007/s10648-018-9434-x | E-C04, E-E08, E-F-P05 | - | - | - |
| 6 | https://pubmed.ncbi.nlm.nih.gov/31484770/ | E-B13, E-C05, E-F-P07 | - | - | - |
| 7 | https://pubmed.ncbi.nlm.nih.gov/25284006/ | E-C06, E-E06, E-F-P09 | - | - | - |
| 8 | https://pubmed.ncbi.nlm.nih.gov/28145268/ | E-B16, E-C06, E-E01, E-F-P13 | - | - | - |
| 9 | https://link.springer.com/article/10.1007/s10648-023-09842-1 | E-A03, E-A05, E-B03, E-C07, E-D03, E-F-P16 | - | - | - |
| 10 | https://eric.ed.gov/?id=ED378554 | E-C08, E-F-P15 | - | - | - |
| 11 | https://pubmed.ncbi.nlm.nih.gov/33013552/ | E-B07, E-C09, E-F-P10 | - | - | - |
| 12 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10176302/ | E-B02, E-C12, E-E12, E-F-P17 | - | - | - |
| 13 | https://www.tandfonline.com/doi/full/10.1080/01434632.2022.2045300 | E-B15, E-C13, E-F-P18 | - | - | - |
| 14 | https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2019.03087/full | E-A09, E-C14, E-F-P08 | - | - | - |
| 15 | https://pubmed.ncbi.nlm.nih.gov/35967831/ | E-B05, E-F-P12 | - | - | - |
| 16 | https://pubmed.ncbi.nlm.nih.gov/16719566/ | E-A02, E-D02, E-F-P14 | - | - | - |
| 17 | https://pubmed.ncbi.nlm.nih.gov/33683913/ | E-A01, E-B01, E-C04, E-D01, E-F-P06, E-I27, E-J1-10 | - | - | - |
| 18 | https://onlinelibrary.wiley.com/doi/10.1111/jcal.13049 | E-E23 | - | - | - |
| 19 | https://www.ijopr.com/article/the-voice-effect-in-multimedia-instruction-revisited-does-it-still-exist-12116 | E-B06, E-F-P11 | - | - | - |
| 20 | https://openstax.org/books/university-physics-volume-2/pages/9-2-model-of-conduction-in-metals | E-F-S02 | - | - | - |
| 21 | https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations | E-F-S01 | - | - | - |
| 22 | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | E-F-S03 | - | - | - |
| 23 | https://openstax.org/books/biology-2e/pages/6-5-enzymes | E-F-S04 | - | - | - |
| 24 | https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html | E-C18, E-E09, E-F-T07 | - | - | - |
| 25 | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html | E-A08, E-B11, E-J1-12 | - | - | - |
| 26 | https://code.claude.com/docs/en/skills | E-F-T01, E-J1-06 | - | - | - |
| 27 | https://github.com/higgsfield-ai/skills | - | - | row 1 | - |
| 28 | https://raw.githubusercontent.com/higgsfield-ai/skills/main/higgsfield-generate/SKILL.md | - | s5 | - | - |
| 29 | https://github.com/higgsfield-ai/cli | - | - | row 2 | - |
| 30 | https://higgsfield.ai/blog/faceless-channel-one-prompt | E-J1-01 | - | - | - |
| 31 | https://github.com/remotion-dev/skills | - | - | row 5, row 33 | - |
| 32 | https://github.com/elevenlabs/skills | - | - | row 7, row 22 | - |
| 33 | https://github.com/anthropics/skills | - | - | row 8, row 34 | - |
| 34 | https://github.com/ahujasid/mcp-for-blender | - | - | row 9 | - |
| 35 | https://github.com/heygen-com/hyperframes | - | - | row 6 | - |
| 36 | https://github.com/adithya-s-k/manim_skill | - | - | row 10 | - |
| 37 | https://github.com/k-dense-ai/scientific-agent-skills | - | - | row 11 | - |
| 38 | https://github.com/cartesia-ai/skills | - | - | row 27 | - |
| 39 | https://skills.sh/ | - | - | row 13 | - |
| 40 | https://registry.modelcontextprotocol.io/ | - | - | row 14 | - |
| 41 | https://www.remotion.dev/docs/license/pricing | E-J1-05 | - | - | - |
| 42 | https://docs.sympy.org/latest/index.html | - | s2 | - | - |
| 43 | https://www.blender.org/about/license/ | - | s2 | row 21 | - |
| 44 | https://ffmpeg.org/ffmpeg-filters.html | E-J2-11 | - | row 47 | - |
| 45 | https://docs.dev.runwayml.com/guides/pricing/ | E-J1-04 | - | row 19 | - |
| 46 | https://platform.claude.com/docs/en/about-claude/pricing | E-J1-02 | s4 | - | - |
| 47 | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices | E-C17, E-F-T05 | - | - | - |
| 48 | https://elevenlabs.io/docs/api-reference/forced-alignment/create | E-J1-09 | s6 | row 26 | - |
| 49 | https://elevenlabs.io/pricing/api | E-J1-03, E-J2-01 | s6 | - | - |
| 50 | https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech | - | s6 | - | - |
| 51 | https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning | - | s6 | - | - |
| 52 | https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries | - | s6 | row 25 | - |
| 53 | https://www.cartesia.ai/fr/blog/sonic-3.6 | - | s6 | - | - |
| 54 | https://www.cartesia.ai/pricing | E-J2-04 | s6 | - | - |
| 55 | https://ai.google.dev/gemini-api/docs/speech-generation | E-J2-06 | s6 | row 30 | - |
| 56 | https://ai.google.dev/gemini-api/docs/models/gemini-3.5-transcribe | - | s8 | - | - |
| 57 | https://ai.google.dev/gemini-api/docs/pricing | E-J2-05 | s6 | - | - |
| 58 | https://developers.openai.com/api/docs/deprecations | E-J2-07 | s6 | - | - |
| 59 | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini | E-J2-08 | s6 | - | - |
| 60 | https://huggingface.co/hexgrad/Kokoro-82M | E-J1-13 | - | row 37 | - |
| 61 | https://github.com/resemble-ai/chatterbox | - | - | row 36 | - |
| 62 | https://github.com/FunAudioLLM/CosyVoice | - | s7 | - | - |
| 63 | https://github.com/SWivid/F5-TTS | E-J1-14 | - | row 39 | - |
| 64 | https://github.com/m-bain/whisperX | E-E24, E-J2-09 | - | row 43 | - |
