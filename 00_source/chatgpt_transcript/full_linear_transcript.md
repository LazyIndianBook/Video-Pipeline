# FULL LINEAR CONVERSATION — AI Video System Research — conversation_id 6acf03ec-b480-83ee-a000-3701059934d9
# nodes on path: 610


=====================================================================
MESSAGE id=bc697a74-40b2-43d3-b537-bae210beef1d role=user content_type=text create_time=1791871578.791 chars=4775
=====================================================================

Conduct comprehensive, end-to-end research to design the **best AI-powered, highly automated STEM video production system for ExamLeaf**, focusing on Class 10 and 12 Physics, Chemistry, Mathematics, and Biology. Our goal is to produce premium, scientifically accurate, engaging 10-minute fast-track revision videos inspired primarily by **Professor Dave Explains** and secondarily by **Khan Academy**, without avatars, generic stock footage, or unnecessary visual effects.

Research and recommend:

1. **Complete Technology Stack:** Identify the best video-generation, animation, rendering, scientific visualization, audio, and automation tools—including Manim, Remotion, Motion Canvas, Hyperframes, Blender, Three.js, FFmpeg, HeyGen, and relevant subject-specific libraries and sub-libraries. Compare alternatives, limitations, integration, licensing, costs, and performance.
2. **Claude Skills & AI Automation:** Find existing Claude Skills and identify every custom Skill we should develop for our libraries, scientific animations, scriptwriting, storyboarding, narration, rendering, validation, and bulk production. Design an integrated Claude Code/Codex workflow with reusable components, subagents, MCP integrations, and minimal manual intervention.
3. **Student Psychology & Confidence:** Research scientifically supported techniques to improve attention, curiosity, understanding, memory retention, motivation, exam confidence, and independent problem-solving. Explain how to simplify difficult concepts, reduce anxiety, create achievable learning milestones, and keep students engaged without cognitive overload or manipulative engagement techniques.
4. **Visual Design & Colour Psychology:** Determine the ideal colour schemes (with HEX codes), backgrounds, typography, contrast, layouts, scientific diagram styles, highlighting, transitions, and animation pacing for comfortable, engaging educational viewing. Include accessibility, mobile readability, and visual consistency.
5. **Voice & Narration:** Research ideal voice characteristics, tone, pacing, pauses, enthusiasm, confidence-building expressions, pronunciation, emotional variation, sound effects, and background music. Compare AI voice engines for naturalness, STEM accuracy, multilingual support, cost, and automation.
6. **Subject-Specific Visualizations:** Recommend the best libraries and techniques for Physics simulations, Chemistry reactions and molecular structures, Mathematics derivations and graphs, and Biology diagrams and processes. Explain how to animate formulas, calculations, diagrams, and abstract concepts while ensuring scientific correctness.
7. **Educational Video Structure:** Develop optimal 10-minute lesson formats, including compelling openings, intuitive explanations, progressive animations, worked examples, student challenges, exam-focused tips, micro-recaps, and confidence-building conclusions.
8. **End-to-End Production Pipeline:** Architect an automated workflow from textbooks/PDFs → syllabus analysis → scripts → scientific verification → storyboards → animation generation → AI voice → synchronization → rendering → quality assurance → final export.
9. **Risks & Best Practices:** Identify everything we should avoid, including AI hallucinations, incorrect animations, robotic voices, excessive effects, poor readability, boring explanations, psychological overload, copyright issues, expensive dependencies, and unreliable automation.
10. **Cost Optimization & Scalability:** Compare open-source, commercial, self-hosted, and hybrid approaches. Calculate estimated costs for producing 1, 100, and 1,000 videos, including AI tokens, rendering, voice generation, infrastructure, and human review.

**Final Deliverables:** Provide a ranked technology comparison, subject-wise recommended libraries, complete Claude Skills inventory (existing vs. custom), student engagement and confidence-building guidelines, visual/audio design standards, automated production architecture, cost analysis, and a practical implementation roadmap.

**Research Requirements:** Verify current tools, documentation, pricing, licensing, and capabilities. Challenge assumptions, distinguish proven learning science from speculation, and prioritize scientific accuracy, genuine student learning, professional production quality, reusability, and low operating costs.

**Ultimate Goal:** Build a scalable **ExamLeaf Video Engine** capable of producing hundreds of consistently excellent educational videos through Claude Code/Codex automation, with minimal repetitive work and strong educational outcomes. Don't provide generic recommendations—identify exactly **what to use, why, how everything integrates, what Skills to build, what to avoid, and how to implement the complete system.**


=====================================================================
MESSAGE id=7397cbcf-4573-43e5-8564-c292fd110fd5 role=assistant content_type=text create_time=1791871593.891713 chars=202
=====================================================================

I’ll verify tools, pricing, and licensing, then design ExamLeaf’s costed architecture, Skills, QA, and rollout while separating evidence-backed teaching practices from choices requiring student testing.


=====================================================================
MESSAGE id=1c565a59-7b70-4ec9-b517-dc20d1f1d20b role=assistant content_type=text create_time=1791871789.080466 chars=221
=====================================================================

HyperFrames merits direct comparison with Remotion because its Apache-2.0 local renderer is separate from HeyGen. Learning design will pair concise explanations with retrieval practice and feedback-driven problem solving.


=====================================================================
MESSAGE id=cc6bf278-77c7-4a33-a322-0a76a2424378 role=assistant content_type=text create_time=1791872915.140412 chars=209
=====================================================================

Scientific review appears to dominate recurring costs, so I’m separating reusable-template production from new-animation work and structuring the implementation around distinct pilot and bulk-production gates.


=====================================================================
MESSAGE id=1b0f1ac0-7679-407c-8ab4-f06647a77c51 role=assistant content_type=text create_time=1791873358.957302 chars=48051
=====================================================================

# ExamLeaf Video Engine: recommended architecture and implementation plan

**Build ExamLeaf around a deterministic, code-driven video engine—not a general-purpose text-to-video generator.**

My recommended starting stack is:

> **HyperFrames + reusable SVG/KaTeX components + Python scientific validation + selective Manim animations + FFmpeg**, with **Claude Code/Codex for development and controlled production tasks**, and a separately managed narration pipeline.

**Remotion is the strongest alternative compositor**, particularly when your developers already work comfortably with React. I would test both against the same small benchmark before committing, but would not maintain two production engines unnecessarily.

The essential design principle is:

> **AI drafts the explanation and assembles approved components. Verified scientific data determines what those components display.**

This avoids repeatedly asking an AI to invent equations, molecular structures, biological processes, and animation code from scratch.

The analysis below uses documentation and prices checked on **13 October 2026**. Tool rankings are recommendations for your use case—not results of a renderer benchmark or voice audition performed here. Rendering time, staffing, and development costs are explicitly identified as planning assumptions.

### Downloadable planning files

[**Editable cost model and Skills inventory — Excel**](sandbox:/mnt/data/ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx)

[**Complete implementation planning pack — ZIP**](sandbox:/mnt/data/ExamLeaf_Video_Engine_Planning_Pack.zip)

The pack also contains the 40-Skill backlog as CSV, proposed design tokens, and a production QA contract. These are planning artifacts, not an already implemented video engine.

---

## 1. The technology decision

### Ranked comparison for ExamLeaf

These tools serve different purposes. A compositor, a scientific animation library, and an encoder should not be treated as interchangeable products.

| Priority | Technology | Recommended role | Strengths for ExamLeaf | Limitations and licensing |
|---|---|---|---|---|
| **1 — primary compositor candidate** | **HyperFrames** | Assemble narrated, frame-controlled lessons from HTML, SVG, equations, diagrams, and rendered inserts | Local rendering; web-based components; agent-oriented workflow; suitable foundation for reusable templates | Apache-2.0 engine, but dependencies/assets need separate review. Newer ecosystem: validate rendering reliability before bulk adoption. |
| **2 — strongest compositor alternative** | **Remotion** | React-based lesson composition and rendering | Excellent fit for React teams; programmatic sequencing; reusable components and preview workflow | Not unrestricted open-source software. Free eligibility and paid automation terms depend on organization/use. |
| **3 — specialist renderer** | **Manim Community** | Mathematical derivations, coordinate geometry, graphs, vectors, and selected physics explanations | Precise equation/object transformations; excellent control over mathematical presentation | MIT. More engineering effort for general layouts, characterful biology diagrams, and large editorial workflows. |
| **4 — alternative animation environment** | **Motion Canvas** | Carefully choreographed narrated 2D vector animations | TypeScript workflow designed around explanatory animation | MIT. Attractive alternative, but adding it alongside HyperFrames and Manim creates another runtime to maintain. |
| **5 — selective 3D layer** | **Three.js** | Spatial geometry, fields, molecules, and selected 3D process explanations | Browser-based, programmable 3D; integrates with web scenes | MIT. Correctness, camera direction, and deterministic timing remain your responsibility. |
| **6 — occasional specialist asset production** | **Blender** | High-value 3D anatomy, spatial mechanisms, and reusable rendered inserts | Strong modelling, lighting, animation, and offline rendering | GPL application. More production and rendering effort; audit redistribution obligations separately. |
| **Required infrastructure** | **FFmpeg** | Audio processing, concatenation, encoding, muxing, and export validation | Essential final-stage media processing | LGPL/GPL obligations depend on the build and enabled components; codec/patent questions are separate. |
| **Do not use as the core engine** | **HeyGen’s avatar-oriented services** | At most, a separately justified service later | Not needed to satisfy your faceless STEM requirement | Adds the wrong primary abstraction. **HyperFrames can be used without adopting a HeyGen avatar workflow.** |

HyperFrames’ repository documents its local engine and rendering architecture; Remotion publishes separate automation licensing; Manim, Motion Canvas, Three.js, Blender, and FFmpeg publish their respective code/licensing information. citeturn155086view0turn912487view3turn352003search6turn155086view2turn400430view2turn400430view0turn849402view7

### Why HyperFrames first—but conditionally

For a greenfield ExamLeaf engine, I would begin with HyperFrames because your requirements favour **reusable web diagrams, explicit timing, local rendering, and low incremental licensing costs**. Its architecture includes browser-based rendering and FFmpeg-backed production components. citeturn155086view0

However, **a small licensing saving is not worth expensive engineering instability**. Switch the primary compositor to Remotion when its React workflow demonstrably reduces implementation, debugging, or maintenance effort.

The pilot should compare identical scenes for:

**Correctness → reproducibility → memory consumption → render time → ease of repair → total operating cost.**

Do not choose from promotional demos alone.

### Important licensing distinctions

**Remotion:** its current pricing distinguishes free eligibility from paid company use. The Automators offering is **$0.01 per billable render, with a $100 monthly minimum** when applicable. Render infrastructure is additional. A 10-minute lesson assembled from multiple separately rendered scenes may involve more than one billable render; confirm the billing interpretation before estimating costs. citeturn912487view3

**GSAP:** it is free under its current standard licence, but **it is not MIT-licensed**. Ordinary commercial video production and a future customer-facing visual editor are different licensing situations. Review the restrictions before turning ExamLeaf’s internal renderer into an external no-code product. citeturn166988view8

**Open-source code does not automatically clear asset rights.** Fonts, pretrained model weights, voices, textbook illustrations, icons, and molecular/anatomical assets require their own records.

### What I would not add initially

Do not combine HyperFrames, Remotion, Motion Canvas, Blender, and Manim merely because each is capable.

Start with **one compositor, one scientific animation specialist, one scientific validation layer, and one audio pipeline**. Add another renderer only for a demonstrated requirement.

Also distinguish **Hygen**, the template scaffolding utility, from **HeyGen**. Hygen can generate standardized project files; it is not a video or narration engine. citeturn385024view4

---

## 2. The recommended stack, layer by layer

| Layer | Recommended implementation | Integration decision |
|---|---|---|
| Source ingestion | `pdfplumber`; Docling when layout reconstruction is useful | Preserve page references and source coordinates. Extract native text before considering OCR. |
| Curriculum/content records | Versioned JSON, source files, Git, PostgreSQL metadata | Store board, academic year, class, subject, chapter, prerequisites, and source permissions explicitly. |
| Scientific validation | Python: SymPy, NumPy/SciPy, Pint, RDKit, Biopython and approved domain-specific checks | Produce verified data before animation generation. |
| Scene composition | HyperFrames, HTML/SVG, KaTeX, seekable animation timelines | Compile typed scene specifications into approved components. |
| Specialist animation | Manim Community; selective Three.js | Render inserts or consume the same verified data as the main compositor. |
| Narration | Provider-neutral TTS adapter, pronunciation dictionary, segment cache | Keep voice generation independent of the video renderer. |
| Timing | Final audio waveform plus alignment/event metadata | Audio duration determines scene timing—not an estimated reading speed. |
| Orchestration | Prefect, Docker workers, bounded queues and retries | Keep long-running production jobs outside chat sessions. |
| Review | Small browser-based review application | Show video, script, source claims, unresolved issues, and approval controls together. |
| Export/storage | FFmpeg; filesystem initially, then object storage such as R2/S3 | Retain immutable manifests and regenerate only changed scenes. |

`pdfplumber` exposes text/layout information; Docling supports document conversion but has separately licensed model dependencies. Prefect supplies workflow state, retries, caching, and approval-oriented orchestration capabilities. citeturn633295view5turn934155view7turn633295view4

**Do not use an automation canvas as a frame scheduler.** A tool such as n8n may be useful for notifications or business integrations, but the render graph should live in tested code and a durable job system.

---

## 3. Subject-specific libraries and scientific safeguards

### Mathematics

**Recommended:** SymPy + KaTeX + SVG/D3 + Manim.

| Requirement | Library/component | Implementation |
|---|---|---|
| Algebra, calculus, matrices, symbolic verification | SymPy | Store expressions with assumptions and verify each transformation. |
| Typeset equations | KaTeX | Render structured mathematics rather than asking an image model to draw text. |
| Graphs and geometric relationships | SVG/D3; Manim for more involved sequences | Use computed coordinates, explicit domains, labelled axes, and consistent scales. |
| Derivation animations | Manim `MathTex` and matching-transform facilities, or semantic equation components in the main renderer | Give symbols stable identities so the animation reflects the actual operation. |

SymPy provides symbolic mathematics and related modules; Manim exposes matching transformation classes; KaTeX documents supported mathematical notation. citeturn712377view0turn847752view3turn849402view4

**Critical safeguard:** a visually smooth transformation is not mathematical justification.

For example, the validator must reject:

\[
\sqrt{x^2}=x
\]

unless the required assumption is present. For real \(x\), the generally valid result is \(|x|\).

Likewise, cancelling a factor must not silently discard a valid case where that factor is zero.

### Physics

**Recommended:** SymPy physics modules + SciPy + Pint + Schemdraw + Manim; Magpylib selectively.

| Requirement | Recommended tool | Boundary |
|---|---|---|
| Mechanics, vectors, symbolic relationships | SymPy `physics.mechanics`, `physics.vector`, appropriate optics modules | Declare reference frames, sign conventions, and idealizations. |
| Time-dependent motion | SciPy `solve_ivp` | Integrate first; sample the computed solution at animation times. |
| Units | Pint | Check dimensional consistency independently of displayed formatting. |
| Circuit diagrams | Schemdraw | It draws circuits; it does not establish that the circuit analysis is correct. |
| Magnetostatic field visualizations | Magpylib | Do not represent it as a general time-dependent Maxwell solver. |
| Spatial explanations | Three.js or Manim | Geometry and camera movements must not change the underlying scientific model. |

These packages document their respective symbolic, numerical, unit-handling, diagramming, and magnetostatic capabilities. citeturn712377view0turn712377view1turn712377view2turn712377view3turn712377view4

**Recommended rule:** particle motion, its velocity vector, the corresponding graph, and displayed numerical values must all consume **the same trajectory data**.

Do not animate a projectile with decorative easing and then place a physically calculated graph next to it.

### Chemistry

**Recommended:** RDKit + SVG + KaTeX’s chemistry support; 3Dmol.js selectively.

Use RDKit for molecular parsing, sanitization, atom identities, 2D coordinates, and structure drawing. Relevant submodules include `Chem`, `rdDepictor`, `rdMolDraw2D`, `rdChemReactions`, and selected `AllChem` functionality. Use 3Dmol.js where a spatial molecular view genuinely helps. citeturn712377view5turn712377view6turn712377view7

The scene model should explicitly record:

**Atoms → bonds → charges → reaction conditions → atom mapping → approved reaction states.**

The renderer then animates those records.

**Critical distinction:** RDKit accepting a structure, or an equation balancing correctly, does **not** prove that a reaction occurs under the stated conditions.

For school chemistry, the strongest visual sequence is often:

> **Observable phenomenon → particle-level explanation → symbolic equation.**

Use separate approved representations for resonance contributors, intermediates, and transition states. Do not let a visually attractive bond morph imply that these are interchangeable.

### Biology

**Recommended:** approved layered SVG diagrams + a process-state model; Biopython and Mol* only where relevant.

| Requirement | Recommended implementation |
|---|---|
| Cells, organs, transport, pathways | Teacher-approved, layered SVG assets |
| Mitosis, meiosis, replication, transcription | Explicit process states with counts, compartments, and directional checks |
| DNA/protein sequences and structures | Biopython modules such as `Bio.Seq`, `SeqIO`, and `Bio.PDB` |
| Selected molecular structures | Mol*, with declarative scene descriptions where appropriate |
| Reusable illustration sources | Individually licensed Bioicons assets and Servier Medical Art |

Biopython supports biological data workflows; Mol* specializes in molecular visualization. Bioicons includes mixed asset licences, while Servier Medical Art uses CC BY 4.0 and requires attribution. citeturn849402view1turn849402view0turn849402view2turn849402view3

**Biology needs more than a diagram renderer.** It needs checks for chromosome counts, ploidy, cellular compartments, membrane orientation, and 5′/3′ direction.

A polished animation with an incorrect chromosome count is still a failed lesson.

---

## 4. Existing Claude/Codex Skills: what to adopt

### Verified starting points

| Source | Existing resources worth considering | ExamLeaf use |
|---|---|---|
| **HyperFrames official repository** | `hyperframes`, `hyperframes-core`, `hyperframes-animation`, `hyperframes-keyframes`, `hyperframes-cli`, `hyperframes-audio`, `hyperframes-registry`, `hyperframes-studio` | Core engine usage and rendering workflow |
| **Remotion official Skills** | `remotion-best-practices`, `remotion-create`, `remotion-render`, `remotion-captions`, `remotion-multimedia`, `remotion-docs` | Alternative React-based engine |
| **Anthropic official Skills** | `skill-creator`, `webapp-testing` | Skill evaluation and preview testing |
| **OpenAI official Skills** | `playwright`, `speech` | Browser automation and adaptable audio workflow patterns |
| **K-Dense scientific-agent-skills** | Selected SymPy, RDKit, Biopython, and scientific-visualization guidance | Package-specific assistance—not scientific approval |
| **Manim Community documentation/plugins** | Official API documentation and `manim-voiceover` | Reference material for a custom ExamLeaf adapter |

The checked HyperFrames manifest contains 21 entries; the checked Remotion Skills README lists 12. Anthropic and OpenAI maintain official Skill repositories, and K-Dense maintains a larger community scientific collection. citeturn885266view2turn885266view1turn885266view4turn885266view5turn633295view2turn633295view3turn953217view3turn992652view2

### Do not install everything indiscriminately

A Skill is an instruction package. It is **not automatically a reliable implementation, a security boundary, or evidence of scientific correctness**.

Use a reviewed subset, pin commits, inspect scripts, and run negative tests before granting execution privileges.

Two findings illustrate the need for this:

**Licensing:** Anthropic’s repository does not apply one blanket open-source licence to everything. Its document Skills are source-available under separate terms. K-Dense also advises checking individual Skill licence fields. citeturn885266view0turn934155view6

**Lifecycle drift:** the checked OpenAI `speech` Skill defaults to a TTS model whose current model card is marked deprecated. Copying a previously valid Skill without checking its dependencies can create a new production problem. citeturn633295view2turn934155view0

I did not verify a first-party general-purpose Manim Claude Skill. Build an ExamLeaf-specific adapter against pinned Manim documentation rather than assuming a community prompt package provides that assurance.

---

## 5. The custom Skills ExamLeaf should build

The proposed v1 inventory contains **40 Skills**. The spreadsheet gives each one inputs, outputs, priority, and a release test.

These are **proposed Skills**, not claims that they already exist.

| Workstream | Custom Skills |
|---|---|
| **Sources and curriculum — 4** | `rights-ingest`, `syllabus-map`, `source-claim-ledger`, `prerequisite-graph` |
| **Teaching and script design — 7** | `lesson-scope`, `revision-script`, `worked-examples`, `retrieval-challenges`, `misconception-audit`, `confidence-load-audit`, `exam-rubric` |
| **Scientific verification — 5** | `math-verification`, `physics-verification`, `chemistry-verification`, `biology-verification`, `independent-review` |
| **Storyboarding and visual components — 8** | `storyboard`, `design-system`, `scene-compiler`, `equation-animation`, `graph-geometry`, `physics-animation`, `chemistry-animation`, `biology-animation` |
| **Specialist adapters — 2** | `manim-adapter`, `threejs-adapter` |
| **Narration and localization — 5** | `narration-normalizer`, `pronunciation-lexicon`, `tts-batch-cache`, `forced-alignment`, `multilingual-localization` |
| **Production — 3** | `render-orchestrator`, `audio-mastering`, `captions-export` |
| **QA, operations, and outcomes — 6** | `visual-accessibility-qa`, `science-frame-qa`, `regression-qa`, `rights-security-release`, `bulk-cost-ops`, `learning-evaluation` |

Use an `examleaf-` prefix in the implementation.

Add a Blender adapter only when a real lesson requires it. Add a Remotion adapter when Remotion is selected—not simply to maintain theoretical compatibility.

### What every Skill must contain

Use the following contract:

```text
SKILL.md
  Purpose and trigger
  Typed inputs and outputs
  Approved dependencies and commands
  Required source evidence
  Forbidden transformations
  Acceptance tests
  Escalation conditions

scripts/
  Deterministic implementation

references/
  Reviewed documentation and conventions

evals/
  Correct examples
  Deliberately incorrect examples
  Regression fixtures
```

Anthropic’s Skill-creation guidance explicitly includes evaluation and comparison of Skill behaviour; apply that principle to ExamLeaf rather than treating a polished `SKILL.md` as completion. citeturn885266view4

**Do not build one Skill per sub-library function.** Keep orchestration Skills small and task-oriented; place package-specific details in references and tested helper modules.

---

## 6. Claude Code/Codex, subagents, and MCP architecture

### Separate engine development from routine video production

**Development workflow:** Claude Code/Codex help implement components, tests, schema migrations, adapters, and bounded repairs.

**Production workflow:** a job runner submits structured tasks to model APIs and executes approved components.

This prevents every lesson from becoming an expensive, unpredictable coding project.

### Suggested agent responsibilities

| Agent | Responsibility | Must not do |
|---|---|---|
| Curriculum/script agent | Scope the lesson and draft from approved sources | Invent syllabus coverage or exam marking rules |
| Independent science reviewer | Re-solve, inspect assumptions, challenge claims | Approve solely because the author sounds convincing |
| Storyboard agent | Select approved visual components and semantic events | Invent scientific geometry or process states |
| Animation engineer | Compile scenes and repair bounded implementation failures | Rewrite approved science to make a render easier |
| Audio/localization agent | Normalize pronunciation, generate/cache narration, align timing | Silently change scientific meaning |
| QA agent | Inspect test results, frames, audio, captions, and manifests | Possess unrestricted publishing authority |

For development, use isolated worktrees and clear file ownership. Start with two to four concurrent agents rather than a large group editing the same files.

### MCP integrations worth implementing

**Read-only source retrieval:** return approved textbook spans, syllabus entries, and provenance—not arbitrary search snippets.

**GitHub:** issues, pull requests, test results, and review records.

**Browser inspection:** the local preview/review application.

**Workflow diagnostics:** job states, failures, and cost records. Prefect documents an MCP integration for read-oriented diagnostics. citeturn633295view4

**Custom scientific services:** narrow operations such as “verify derivation,” “check reaction atom balance,” and “render approved scene.”

MCP is useful when an agent needs a controlled service interface. It is unnecessary merely to import SymPy or invoke an internal FFmpeg function.

### Security boundary

Source PDFs, retrieved text, and downloaded Skills are untrusted input. They must not be able to instruct agents to reveal credentials, install packages, or bypass review.

Enforce permissions in the runner, containers, and release service—not only in prompts.

---

## 7. The end-to-end production pipeline

```text
Permitted textbook/PDF + board/year syllabus
                    ↓
Source extraction + provenance + rights ledger
                    ↓
Topic map + prerequisites + lesson objective
                    ↓
Claim ledger + draft explanation + worked examples
                    ↓
Deterministic checks + independent scientific review
                    ↓
HUMAN ACADEMIC APPROVAL
                    ↓
Storyboard + typed SceneSpec
                    ↓
Approved components + verified scientific data
                    ↓
Narration generation + pronunciation review
                    ↓
Final-audio alignment + semantic event timing
                    ↓
Per-scene rendering + automated QA
                    ↓
FFmpeg assembly + captions + export checks
                    ↓
FULL FINAL-VIDEO REVIEW
                    ↓
Approved release + immutable manifest
```

### Source handling

Every claim should retain a source identity, page/region reference, academic-year context, and source hash.

For digitally generated PDFs, extract native text first. Use OCR only where needed, and manually check recovered equations, signs, units, and diagram labels. Document extraction is not scientific interpretation. citeturn633295view5turn934155view7

For ExamLeaf’s initial market, make the board and year explicit in every lesson record. Do not assume that a familiar textbook chapter automatically matches the intended syllabus or marking scheme.

### The key intermediate formats

Use two renderer-independent records:

**`LessonSpec`:** objective, prerequisites, source claims, worked problems, narration, retrieval questions, expected answers, and exam terminology.

**`SceneSpec`:** scene ID, approved component, scientific-data hash, displayed text, separate spoken text, semantic events, layout, timings, and declared simplifications.

This makes it possible to change renderers without rewriting the lesson’s scientific content.

### Narration and synchronization

Plan scenes before generating voice, but finalize their durations **after** the actual audio exists.

Generate short segments—typically one to three sentences—not a single fragile 10-minute request.

For a formula, maintain separate representations:

```text
Display: I = neAv_d

Spoken:
“Current magnitude equals the number density of electrons,
multiplied by the elementary charge, cross-sectional area,
and drift-speed magnitude.”
```

Use word/event timestamps to reveal the corresponding quantities. Do not align by dividing the total audio duration equally among words.

### Deterministic rendering

Every frame should be evaluated from an explicit time or frame index.

Avoid wall-clock animation, uncontrolled randomness, network-loaded fonts, and simulations that advance differently depending on render speed.

Pin dependencies, browser versions, fonts, and container images. Treat cross-platform bitwise identity as a separate engineering challenge; a fixed seed alone does not guarantee identical GPU output.

### Caching and repair

Cache scenes by a hash of:

**Source claims + scientific model + component version + narration + design tokens + renderer environment.**

A pronunciation correction should regenerate the affected audio and dependent scenes—not the entire subject catalogue.

---

## 8. Learning science: engagement that produces understanding

### What has stronger support

| Principle | ExamLeaf application | Evidence qualification |
|---|---|---|
| **Retrieval practice** | Ask students to recall or solve before revealing the answer | Practice testing is strongly supported; in-video testing has also reduced mind-wandering and improved retention in studied lecture settings. |
| **Distributed practice** | Provide short follow-up questions after the lesson and on later days | Supported broadly; the exact spacing should depend on the retention goal and material. |
| **Segmentation and pre-training** | Introduce essential symbols first; divide the lesson into coherent sections | Helps manage essential processing, especially when students can control pacing. |
| **Worked examples with fading** | Show a complete solution, then remove selected steps, then require independent solving | Appropriate scaffolding; its effectiveness depends on prior knowledge and task design. |
| **Signalling and spatial/temporal alignment** | Highlight the part being explained and place labels beside it | Useful for guiding attention without adding unrelated information. |

The supporting literature includes Dunlosky and colleagues’ review, research on interpolated testing during video lectures, multimedia-learning research on segmentation/pre-training, and worked-example research. citeturn532263search2turn532263search9turn107054view1turn698207search11turn953217view1

**Important limitation:** findings from university lectures or laboratory tasks do not automatically establish the best pacing for Assam Class 10 and 12 students. Use them as design foundations, then test with your actual audience.

### Confidence should be earned through observable success

The desired progression is:

> **“I understand the representation” → “I can complete a step” → “I can solve a related problem without help.”**

Use specific feedback:

> “You identified the relevant law correctly. Now keep the positive direction consistent.”

> “The answer changed because the area changed—not because the material suddenly gained more charge carriers.”

Avoid “This is easy,” “Only geniuses get this,” or “Watch this and full marks are guaranteed.”

A slogan is not a substitute for successful practice. Growth-mindset intervention findings are heterogeneous; they do not justify promising that motivational wording alone improves attainment. citeturn698207search10

### Reduce overload without removing necessary thinking

Keep the reference diagram or equation visible while the student uses it. Remove redundant prose, irrelevant decorative movement, and simultaneous competing highlights.

The goal is not to eliminate effort. It is to direct effort toward the concept rather than toward deciphering the presentation. Multimedia-learning research supports coherence and signalling, not constant stimulation. citeturn953217view1

### Ten minutes is a format target, not a scientific law

Do not stretch a six-minute idea to ten minutes or compress a difficult chapter into ten minutes by speaking faster.

A chapter that needs two coherent revision lessons should receive two. Students lacking prerequisites need a preparatory explanation, not merely a faster recap.

Published observations about shorter-video engagement should not be interpreted as a universal attention-span limit or proof that longer explanations cannot work. citeturn953217view1

### Evaluate learning, not “addictiveness”

Track immediate recall, delayed recall, unprompted problem-solving, transfer to changed problems, and confidence calibration.

Watch time is useful diagnostically, but a student watching continuously while learning little is not a successful outcome.

---

## 9. Visual design and colour standards

### Recommended light palette

There is no scientifically established “best HEX code for learning.” Colour effects depend on context, and the literature does not justify claims such as “this blue increases retention.” Use colour primarily for hierarchy, consistency, and accessibility. citeturn107054view0

The following is a proposed ExamLeaf design system:

| Role | HEX | Contrast against `#F7F9FC` |
|---|---|---:|
| Main background | **`#F7F9FC`** | — |
| Primary text/equations | **`#14213D`** | **15.15:1** |
| Secondary text | **`#526074`** | **6.06:1** |
| Primary explanatory blue | **`#185ABD`** | **6.15:1** |
| Teal emphasis | **`#087986`** | **4.87:1** |
| Amber caution | **`#9A5B00`** | **5.14:1** |
| Error/correction red | **`#B42318`** | **6.23:1** |
| Secondary relationship purple | **`#6E44AA`** | **6.49:1** |

These contrast ratios were calculated for this proposal.

A dark variant can use **`#101826`** with **`#EAF0F6`** text. Revalidate its accent colours independently; do not reuse the light palette blindly.

WCAG’s commonly relevant thresholds include 4.5:1 for normal text and 3:1 for meaningful non-text graphics. Palette compliance alone does not establish that the complete video player or learning product is accessible. citeturn487573search8turn487573search12

### Typography and phone readability

Use **Inter** for English interface/explanatory text, appropriate Noto Sans script families for localization, and proper mathematical typesetting. Inter is distributed under the SIL Open Font License. citeturn107054view4

Proposed starting sizes for a **1920 × 1080** master:

| Element | Starting range |
|---|---:|
| Essential labels | **64–72 px** |
| Main equations | **84–112 px**, adjusted for indices |
| Headings | **72–88 px** |
| Outer safe margin | **96 px** |
| Caption-reserved lower area | Approximately **190 px** |

These are production choices, not universal research-derived optima.

Test the actual lesson on a small phone. At 360-pixel display width, a 64-pixel source label becomes only about 12 pixels high. **Remove or split content before shrinking essential text.**

### Diagram and animation rules

Maintain one dominant explanatory focus. Put labels beside their objects, keep axes and units visible, and use shapes or labels in addition to colour.

Colour conventions should be context-aware: oxygen being red in a molecular diagram must not imply that it is “wrong.”

Suggested starting timings are **150–300 ms** for simple transitions, **300–600 ms** for highlights, and **0.8–1.5 seconds** for equation transformations followed by a readable hold. Adjust these through observation; physical motion must follow the scientific model, not those aesthetic timing ranges.

Use cuts, reveals, and restrained dissolves. Avoid cinematic transitions, constant zooming, decorative particles, and syllable-by-syllable karaoke text.

---

## 10. Voice and narration

### Recommended provider shortlist

These are candidates for audition, not an assertion that one has objectively superior naturalness for your students.

| Engine | Recommended position | Current price/capability consideration | Main caution |
|---|---|---|---|
| **ElevenLabs Multilingual v2** | Initial English production candidate | Listed standard API rate: **$0.08/1,000 characters** | Test STEM pronunciation and specific voice rights. |
| **ElevenLabs newer models** | Challenger in the audition | Evaluate newer expressive models against the stable baseline | Do not assume newer means clearer for equations. The checked page still showed a promotion ending 12 October; it is excluded from the cost model. |
| **Cartesia Sonic 3.6** | Strong cost/quality challenger | Pro: **$5/100,000 credits**; Startup: **$49/1.25 million**; one TTS character per credit | Effective cost depends on using the plan allowance; minimum subscriptions matter. |
| **Sarvam Bulbul v3** | Indian-language candidate for documented locales | **₹30/10,000 characters** | Confirm exact model/language support, not just marketing claims. |
| **Google Chirp 3 HD** | Alternative multilingual enterprise provider | **$30/million characters** beyond applicable free allowances | Audition terminology, pacing, and language-specific voice quality. |
| **Kokoro 82M** | Self-hosted preview voice and possible production challenger | Apache-2.0 model weights; no per-character provider fee | Compute, integration, voice suitability, and language limitations remain. |
| **OpenAI speech workflow** | Re-evaluate before adoption | The checked older TTS model card is marked deprecated | Do not deploy the old Skill’s default without selecting a supported replacement. |

These prices and status observations come from provider pricing pages, model documentation, and the Kokoro model card. citeturn912487view2turn992652view0turn992652view1turn833953view5turn802690view0turn934155view0

### Assamese requires a separate acceptance gate

Sarvam’s marketing mentions Assamese, but the checked model-specific API language list omits it. That discrepancy is sufficient to block an Assamese production commitment until an actual API request succeeds and native reviewers approve the results. citeturn352003search7turn802690view4

Do not substitute Bengali pronunciation or infer support from script similarity.

### The voice specification

My proposed starting brief is:

**Clear adult voice, conversational but authoritative, moderate warmth, restrained enthusiasm, and deliberate emphasis on causal relationships.**

Start around **130–150 spoken words per minute during ordinary explanation**, slower around symbolic expressions. Aim for approximately **1,150–1,300 narration words** in a 10-minute lesson with inspection and thinking time. Treat these as pilot targets.

Prefer:

> “Notice what stays constant.”

> “Before substituting, decide which direction is positive.”

Avoid constant excitement, promotional delivery, breathy whispering, and exaggerated praise after every step.

### Pronunciation and evaluation

Build a versioned audition set containing difficult subject terms, units, fractions, powers, signs, abbreviations, and connected explanations.

Have subject teachers judge **meaning and pronunciation**, and students judge **clarity and listening effort**. Blind comparisons are more useful than choosing from an impressive marketing sample.

Store separate dictionaries by **language, subject, provider, model, and voice**.

### Music and mastering

Use **no background music during the main explanation** as the default. Add sound only when it carries instructional meaning or provides a brief, unobtrusive section cue.

Suggested internal mastering target: **−16 LUFS integrated, true peak no higher than −1 dBTP**. This is an ExamLeaf production target, not a claimed universal platform requirement.

Keep a high-quality audio master, process loudness after assembly, and provide accurate selectable captions.

### A self-hosting licence trap

F5-TTS distinguishes MIT-licensed code from pretrained weights released under **CC BY-NC**. Those weights are not a straightforward commercial deployment choice merely because the repository’s code is open. citeturn802690view1

---

## 11. The proposed 10-minute lesson structure

This is a starting template, not a compulsory timing formula.

| Time | Segment | Student action |
|---|---|---|
| **0:00–0:25** | Concrete problem or diagnostic question | Predict or notice a gap |
| **0:25–0:55** | Prerequisites and essential terms | Recall the minimum required knowledge |
| **0:55–2:55** | Intuitive visual explanation | Build the mental model |
| **2:55–4:25** | Equation, formal relationship, or process model | Connect the intuition to formal language |
| **4:25–6:25** | Worked example | Follow why each step is chosen |
| **6:25–7:35** | Partially completed example | Supply a missing step |
| **7:35–8:45** | Independent challenge and explanation | Solve or predict without immediate help |
| **8:45–9:30** | Common error, exam terminology, micro-recap | Diagnose and correct |
| **9:30–10:00** | Confidence checkpoint and next practice | State what can now be done independently |

Include optional pause prompts rather than stressful countdowns.

For Biology, replace a long derivation with process states and causal explanation. For Chemistry, move between observable, particle, and symbolic representations. For Physics, connect diagram, equation, and graph. For Mathematics, connect symbolic operations to geometric or numerical meaning.

**The closing statement should describe a demonstrated capability**, not offer vague encouragement:

> “You can now identify the relevant relationship, substitute with consistent units, and explain how changing the area affects the result.”

---

## 12. QA, risks, and release standards

| Risk | Required control |
|---|---|
| Hallucinated scientific claims | Claim-to-source ledger, deterministic checks, independent review, academic approval |
| Correct equation but misleading animation | Compare rendered semantic events with the approved scientific model |
| Wrong textbook/board/year | Explicit curriculum version in every lesson |
| Incorrect worked answer | Independent re-solution with assumptions and boundary cases |
| Robotic or ambiguous narration | Pronunciation corpus, separate spoken notation, full listening review |
| Poor mobile readability | Real small-screen playback tests—not desktop screenshots alone |
| Dependency or model update breaks output | Pinned versions, golden scenes, lifecycle checks, controlled upgrade tests |
| Prompt injection from documents/Skills | Sandboxing, allowlisted tools, no source-triggered execution |
| Copyright or asset-rights problems | Permission records and per-asset attribution/licence ledger |
| Runaway retries or token consumption | Per-stage budgets, retry caps, escalation, and stop controls |
| Over-automation hides errors | Agents cannot self-approve critical failures or publish without approval |

### Every released lesson needs two human approvals

**Academic approval:** claims, scope, explanations, notation, worked examples, and scientific visuals.

**Final production approval:** the entire rendered lesson, including narration, synchronization, captions, and mobile readability.

Sampling frames can support automated QA. It does not replace watching the whole final video.

Where reuse is high, these reviews become faster because reviewers examine changes against established components. That is the correct way to reduce manual work.

---

## 13. Cost analysis: 1, 100, and 1,000 videos

### What the model represents

The baseline assumes a working reusable-component library, ordinary 2D STEM lessons, cloud model APIs, ElevenLabs narration, and CPU rendering.

It **does not** assume that the first bespoke biology animation costs the same as the hundredth lesson using approved components.

All amounts below are **USD before taxes**, except the separately quoted Sarvam price. No currency conversion, introductory promotion, free tier, or batch discount is assumed.

### AI token budget per video

| Task | Planning allowance: input/output tokens | Verified rates per million input/output tokens | Estimated cost |
|---|---:|---:|---:|
| Haiku 5.5 extraction/routing | 30,000 / 5,000 | $0.10 / $0.50, within its short-prompt tier | $0.0055 |
| Sonnet 5.5 writing/component adaptation | 120,000 / 25,000 | $2 / $10 | $0.4900 |
| Independent `gpt-6.1-sol` review | 60,000 / 10,000 | $2 / $10, short-context rates | $0.2200 |
| Opus 5.5 escalation reserve | 10,000 / 2,000, amortized | $4 / $20 | $0.0800 |
| **Subtotal** | | | **$0.7955** |
| **Including 30% rewrite/retry allowance** | | | **$1.0342** |

The token workloads are assumptions; the listed prices are from current official pricing documentation. citeturn912487view0turn912487view1

### Other variable costs

| Component | Assumption | Cost/video |
|---|---|---:|
| Narration | 8,000 characters × 1.20 regeneration × $0.08/1,000 | **$0.7680** |
| Rendering | 8 vCPU, 16 GB; 45 worker-minutes; 20% retry reserve | **$0.3555** |
| ASR validation | 10 minutes × $0.003/minute | **$0.0300** |
| Working-asset storage | 2 GB for one month × $0.015/GB-month | **$0.0300** |
| Miscellaneous API/request reserve | Planning allowance | **$0.1500** |
| **Variable machine cost, including LLMs** | | **$2.3676** |

The compute calculation uses AWS Fargate’s published US East CPU/memory rate example; storage uses R2 standard pricing. **The 45-minute render duration is not a measured benchmark**, and these are not Mumbai-region prices. citeturn953217view0turn284193view4turn912487view1turn912487view2

### Human review and fixed overhead

The baseline allows **45 minutes of academic review at $20/hour** and **15 minutes of production QA at $12/hour**: **$18/video**.

Fixed monthly allowances are **$100 for infrastructure/tools** and **$100 for maintenance**. Four maintenance hours per month is a mature-system planning assumption, not a realistic allowance during active engine development.

Therefore:

\[
\text{Production cost}
=
N(2.3676+18)+200
\]

### Volume comparison

All three cases use the same one-month accounting period.

| Cost | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|
| Variable machine costs | $2.37 | $236.76 | $2,367.62 |
| Human review | $18.00 | $1,800.00 | $18,000.00 |
| Fixed overhead | $200.00 | $200.00 | $200.00 |
| **Total production cost** | **$220.37** | **$2,236.76** | **$20,567.62** |
| **Average production cost/video** | **$220.37** | **$22.37** | **$20.57** |
| Reviewer hours | 1 | 100 | 1,000 |

**The important conclusion is not “premium videos cost $2.”** Approximately $2.37 is the assumed machine portion. Academic and final-video review dominate the baseline cost.

At 1,000 videos per month, the model requires **1,000 reviewer-hours**, equivalent to **6.25 full-time equivalents at 160 hours/month**. Automation does not eliminate that capacity requirement.

### Initial implementation budget

An illustrative initial budget is:

**240 engineering hours × $25 + 60 academic-template hours × $25 + 20 design/voice hours × $25 = $8,000.**

That produces first-batch totals of approximately **$8,220**, **$10,237**, and **$28,568** respectively.

This is an initial engine/template budget—not a quote or promise for a fully mature platform. Bespoke diagrams, extensive localization, rights clearance, and complex 3D can increase it substantially.

### Open-source, commercial, and self-hosted alternatives

| Approach | Economic interpretation | Recommendation |
|---|---|---|
| **HyperFrames + commercial AI/TTS** | Low renderer licensing burden; usage-based model/audio costs | **Best initial balance** |
| **Remotion + commercial AI/TTS** | Similar variable media costs, plus applicable renderer licensing | Choose when saved engineering effort exceeds licensing cost |
| **HyperFrames + self-hosted Kokoro** | Removes the $0.768 narration API line, but adds inference, integration, and maintenance | Test for previews first; production only after audition |
| **More extensively self-hosted AI** | Replaces API bills with hardware utilization, serving, maintenance, and model-quality risk | Consider after real volume and performance measurements exist |

For Remotion, the workbook includes an optional assumption of **20 billable renders/video**. At the published automation rate, this would add **$100, $100, and $200** to the three volume cases when the paid licence applies. The billable-render interpretation must be confirmed. citeturn912487view3

At 1,000 videos, the baseline LLM-plus-narration API spend is only about **$1,802/month**. That is the relevant ceiling against which additional self-hosted serving and maintenance should be compared—not a hypothetical unlimited API bill.

**Sensitivity:** increasing human review from $18 to $40 adds $22/video. One extra hour of skilled review can matter more than a large percentage reduction in render cost.

---

## 14. Practical implementation roadmap

| Phase | Build | Gate before proceeding |
|---|---|---|
| **A. Scientific and design contracts** | Source/rights ledger, syllabus records, LessonSpec, SceneSpec, design tokens, negative tests | Reviewers agree on what constitutes a correct lesson |
| **B. Renderer benchmark** | Identical HyperFrames and Remotion scenes, including equations, SVG biology, graphs, captions, and audio | Compare real correctness, memory, timing, repair effort, and cost |
| **C. Core reusable library** | Equation steps, coordinate graphs, vectors, circuits, molecular diagrams, biological process states, worked-example layouts | Components pass scientific and visual regression tests |
| **D. Eight pilot lessons** | One lesson per subject strand and class level | Teacher approval, voice audition, small-phone readability, student feedback |
| **E. Controlled batch** | Approximately 30–50 lessons with orchestration, caching, cost limits, and review queues | No unresolved critical errors; repair/review time and cost are predictable |
| **F. Bulk production** | Larger queues, more reviewers, localization, selective 3D | Stable quality gates and evidence of independent learning |
| **G. Continuous evaluation** | Delayed quizzes, transfer items, confidence calibration, controlled template improvements | Changes improve learning or accessibility—not merely watch time |

### What I would build first

The first engineering milestone should be a **single complete, scientifically reviewed lesson**, not an elaborate dashboard.

A good Physics pilot is drift velocity and current: it tests equations, units, diagrams, opposite electron/current directions, narration of symbols, parameter changes, and a worked example.

A Biology pilot should then test a process with explicit state and count changes. That exposes problems a mathematics-only demo will miss.

---

## Final recommendation

**Approve HyperFrames as the initial compositor candidate, Manim as the specialist mathematical renderer, Python as the scientific verification layer, and FFmpeg as the media backbone.** Keep Remotion as the measured alternative, not a parallel default.

Build the **source/claim system, verified component library, narration lexicon, and release tests before scaling generation**. Retain academic approval and full final-video review, while automating extraction, assembly, synchronization, rendering, captioning, caching, and routine checks.

The most valuable ExamLeaf asset will not be a large collection of prompts. It will be a **versioned library of scientifically correct teaching components, tested lesson patterns, and traceable source material** that AI can reliably assemble into excellent revision lessons.


=====================================================================
MESSAGE id=0fe4d7a0-e1d1-42c0-9199-473780936955 role=user content_type=text create_time=1791876825.614 chars=3521
=====================================================================

Conduct an **extremely in-depth, evidence-based psychological and neuroscience analysis** to determine how ExamLeaf can create highly engaging, confidence-building, and genuinely effective 10-minute educational videos for Class 10–12 students.

Research every major factor influencing **human attention, memory, curiosity, motivation, cognitive load, emotional engagement, learning retention, and perceived learning effectiveness**.

Focus particularly on:

1. **Brain & Attention Psychology:** How students process information, how attention changes over time, what causes distraction or boredom, and how to maintain engagement. Investigate actual attention-span research rather than assuming fixed limits.
2. **Colours & Visual Psychology:** Identify ideal colour combinations, backgrounds, contrast, typography, highlighting, visual hierarchy, and animation styles that support focus, readability, comprehension, and reduced visual fatigue.
3. **Animation & Explanation Strategy:** Determine how much animation to use, how frequently visuals should change, and when to use diagrams, working simulations, equation transformations, real-world examples, and step-by-step calculations without overstimulation.
4. **Active Student Interaction:** Design strategic moments encouraging students to **pause, write definitions, copy essential formulas, draw diagrams, predict outcomes, solve questions, recall concepts, and verify their answers**. Determine the ideal timing, frequency, and psychological effectiveness of these interactions.
5. **Video Speed & Engagement:** Research optimal narration speeds, explanation pacing, scene durations, pauses, visual transitions, and changes in intensity. Determine when faster delivery improves engagement and when slowing down is necessary for understanding.
6. **Confidence & Positive Reinforcement:** Explore how narration, encouragement, achievable challenges, visible progress, small successes, and mastery checkpoints can make students genuinely believe in their ability to learn and trust ExamLeaf's effectiveness. Develop powerful, positive messaging without exaggerated claims, false promises, or manipulative psychology.
7. **Learning Retention & Behaviour:** Investigate curiosity loops, retrieval practice, spaced repetition, reward mechanisms, storytelling, progressive difficulty, misconception correction, and techniques that motivate students to complete lessons and continue studying.
8. **Practical Implementation:** Translate every finding into specific video-production rules, including recommended animation density, interaction intervals, narration patterns, colour HEX codes, visual examples, confidence-building scripts, and a **second-by-second blueprint for an ideal 10-minute lesson**.

**Research Requirements:** Consult credible neuroscience, cognitive psychology, educational research, and successful teaching methodologies. Distinguish proven findings from assumptions, identify individual differences, and propose A/B experiments to validate recommendations.

**Ultimate Goal:** Make ExamLeaf videos so clear, visually compelling, interactive, encouraging, and academically valuable that students **enjoy watching, actively participate, understand difficult concepts, retain knowledge, develop genuine confidence, and improve their exam performance**.

Prioritize **real learning outcomes over views, watch time, superficial excitement, or psychological manipulation**. Provide actionable, scientifically justified recommendations—not generic advice.


=====================================================================
MESSAGE id=6be84c31-0ec1-490b-a044-145182dab712 role=assistant content_type=text create_time=1791877825.694609 chars=208
=====================================================================

Confidence will come from successful attempts plus specific feedback, not generic praise. The blueprint separates viewing from self-paced practice, delaying answers until students genuinely attempt each task.


=====================================================================
MESSAGE id=2efad524-72b6-41fd-9c62-3f5e7844d00b role=assistant content_type=text create_time=1791878548.834969 chars=58353
=====================================================================

# ExamLeaf’s learning psychology blueprint

**ExamLeaf should optimize for a sequence of successful mental actions—not uninterrupted watching.**

The target experience is:

> **“I know what I am trying to understand. I can follow the explanation. I can attempt the next step. I can identify and correct my mistake. I can now solve something without the video.”**

That is a more defensible foundation for engagement and confidence than constant animation, rapid editing, motivational slogans, or attempts to “trigger dopamine.”

For your fast-track revision format, I recommend a **visually stable, conversational lesson with purposeful animation, several brief predictions, two or three substantial practice pauses, specific corrective feedback, and follow-up retrieval outside the video**.

A crucial distinction runs through this report:

**Make information easy to perceive and understand. Do not make every learning activity effortless.** Reading a legible diagram should be easy; reconstructing its explanation from memory may require productive effort.

This is a research synthesis and a proposed production standard—not evidence that ExamLeaf’s exact format has already been validated. The research includes classroom studies, laboratory experiments, meta-analyses, neuroscience, and accessibility standards. Many video-specific experiments involve university students rather than Indian secondary-school students, so the precise production settings need testing with your audience.

---

## 1. What the evidence supports—and what it cannot specify

Use three evidence categories internally:

**Strong foundation:** converging research supports the general practice.

**Context-dependent:** useful findings exist, but outcomes depend substantially on learners, material, implementation, or measurement.

**Production hypothesis:** a sensible starting specification that ExamLeaf should test, not a scientifically established optimum.

| Design decision | Evidence assessment | What ExamLeaf should conclude |
|---|---|---|
| Include retrieval practice rather than relying exclusively on rewatching | **Strong foundation** | Require students to retrieve or apply information before showing the answer. |
| Revisit material across separate study occasions | **Strong foundation** | Build practice after the video, not just repetition within it. |
| Segment complex explanations into meaningful units | **Strong foundation, implementation-dependent** | Separate conceptual steps and allow processing time. No universal segment duration is established. |
| Use worked examples, then reduce support | **Strong foundation for appropriate tasks** | Move from demonstrated reasoning toward independent problem-solving. |
| Highlight the relevant part of a diagram or equation | **Strong foundation, when selective** | Direct attention; do not highlight everything. |
| Replace all static diagrams with animation | **Not supported** | Animate when change, movement, or transformation is part of what must be understood. |
| Insert a quiz at a particular fixed interval | **Production hypothesis** | Useful checkpoints need testing; there is no established “reset attention every 90 seconds” law. |
| Choose a particular blue, green, or background to improve memory | **Insufficient for that specific claim** | Choose colours for legibility, meaning, consistency, and tested comfort. |
| Increase confidence through repeated praise | **Insufficient as a stand-alone strategy** | Build confidence through evidence of competence and useful feedback. |
| Treat high completion rates as proof of learning | **Not justified** | Measure delayed recall, transfer, and independent performance. |

The retrieval, segmentation, signalling, and worked-example recommendations are grounded in the corresponding research syntheses and experiments—not in the popularity of particular educational channels. citeturn649723view0turn649723view1turn880959search1turn806608search8

### How large are the reported effects?

A classroom testing meta-analysis integrated **222 studies involving 48,478 students** and reported an average effect of approximately **g = 0.50**. That supports retrieval practice as a serious instructional tool, but its effects varied with feedback, question format, comparison activity, repetition, and other factors. **It does not mean “50% higher marks.”** citeturn649723view0

Conversely, a meta-analysis published in **March 2026**, drawing on 50 studies, found a **small average negative effect** of interesting but irrelevant details on learning, **g = −0.16**. That argues against unnecessary decoration—not against attractive educational design. citeturn999403view0

Do not add effect sizes from separate studies together or turn them into a predicted ExamLeaf exam-score improvement.

---

# 2. Brain, attention, and information processing

## 2.1 There is no universal attention countdown

The familiar claims that people can concentrate for only eight seconds, or that all students lose attention after ten minutes, are not sound production rules. A review specifically examining lecture attention found that the often-repeated 10–15-minute limit rests on a weak evidential foundation. This does not mean fatigue and mind-wandering are imaginary; it means they are not governed by one universal cutoff. citeturn700183search8

**ExamLeaf implication:** do not insert an effect because a timer says attention has expired. Insert a meaningful change when the student needs to perform a different mental operation.

For example:

> “We have established what changes. Now predict what happens when we double it.”

That is a purposeful transition from understanding to prediction. A zoom, sound effect, or unrelated image is not an equivalent substitute.

## 2.2 Attention is several interacting functions

Neuroscience distinguishes functions associated with **alerting, orienting, and executive control**, supported by interacting networks rather than a single “attention centre.” Being awake, looking at a highlighted object, and deliberately following a difficult argument are related but different processes. citeturn842694search15

For production, this distinction matters:

| Function | What can go wrong | Proposed response |
|---|---|---|
| Readiness to engage | The student is tired, distracted, or uncertain what the lesson offers | State a concrete objective and provide a low-friction starting task. |
| Selecting relevant information | Several arrows, labels, animations, and captions compete | Establish one dominant explanatory focus. |
| Maintaining the task goal | The student loses track of why a calculation is being performed | Keep the question or target quantity visible. |
| Monitoring understanding | The student follows the narrator but cannot reproduce the reasoning | Introduce an answer-hidden checkpoint. |

These are design applications of the distinction, not claims that a particular graphic directly activates a particular brain network.

## 2.3 Working memory is limited—but “four objects per screen” is not a law

Working-memory research supports limitations on how much unfamiliar information can be actively maintained. However, performance depends on attention, task demands, prior knowledge, and how information is grouped. The influential “four chunks” literature does **not** establish that a video must contain no more than four visible objects. citeturn253767search1

A familiar equation may function as a meaningful unit for one student and as several disconnected symbols for another.

**Proposed rule:** count **unexplained relationships**, not just objects.

A diagram can contain ten familiar labels and remain manageable. A diagram with three unfamiliar quantities and an unexplained interaction may be overwhelming.

Before a dense explanation, briefly establish:

- What each essential symbol represents.
- Which quantities are changing.
- What remains constant.
- What the student is trying to determine.

This is especially important when a revision viewer has forgotten a prerequisite.

## 2.4 Attention is not the same as memory

A useful instructional distinction is:

**Noticing → interpreting → connecting → retrieving → retaining and transferring.**

An animation can help a student notice a relationship without ensuring that they can later reconstruct it.

Memory also involves processes extending beyond the viewing session. Research on sleep and memory consolidation is one reason a compelling ten-minute presentation should not be treated as a complete long-term learning intervention. citeturn253767search14

**ExamLeaf implication:** the video should initiate a learning cycle, not claim to finish it.

Its closing task should be something like:

> “Tomorrow, try a new question before reopening your notes.”

It should not imply that a feeling of clarity means the information is permanently secure.

## 2.5 What causes boredom?

Boredom is not simply “too little stimulation.” Research models distinguish difficulties engaging attention from a lack of perceived meaning. Both insufficient challenge and excessive difficulty can contribute to disengagement. citeturn842694search2

Use different interventions for different problems:

| Apparent problem | Better response than adding visual excitement |
|---|---|
| “I already know this.” | Offer a challenge or a clearly marked route to the next section. |
| “I cannot follow this.” | Restore a prerequisite, simplify the representation, or supply one worked step. |
| “Why does this matter?” | Show the question or phenomenon the concept helps explain. |
| “There is too much happening.” | Remove competing elements and hold the useful diagram. |
| “I have been listening but not thinking.” | Ask for a prediction or explanation before continuing. |

A calmer scene can therefore be **more engaging intellectually** than a busier one.

## 2.6 What neuroscience says about curiosity

In a well-known fMRI study, participants remembered answers to high-curiosity trivia questions better, with benefits also observed for incidental information. Curiosity-related memory benefits were associated with activity and connectivity involving reward-related regions and the hippocampus. citeturn903930view1

That is interesting mechanistic evidence. It does **not** establish that:

- A cliffhanger releases a measurable “dose” of dopamine.
- A particular colour activates a learning state.
- Surprise every few seconds improves school examination performance.

**Practical interpretation:** use a genuine question whose answer helps explain the subject. Do not turn the neuroscience into a marketing promise.

---

# 3. Cognitive load: simplify the presentation without simplifying away the science

## 3.1 Reduce unnecessary work; preserve necessary reasoning

Cognitive load theory distinguishes the demands of the learning material from demands imposed by how it is presented. Existing knowledge changes those demands substantially. citeturn461055search2

For ExamLeaf, unnecessary work includes searching for a label, remembering an equation that just disappeared, decoding inconsistent notation, or listening to a new explanation while copying the previous one.

Necessary work includes choosing a law, explaining a causal link, comparing two cases, or reconstructing a process.

**Do not confuse “lower cognitive load” with “no thinking.”**

### Example: a calculation scene

A weak sequence is:

> Show the question → replace it with a formula → replace that with substitutions → replace those with the answer.

The student must remember several disappearing states.

A better proposed sequence keeps the **question and relevant diagram stable**, while building:

\[
\text{Known quantities}
\quad\rightarrow\quad
\text{Relevant relationship}
\quad\rightarrow\quad
\text{Substitution}
\quad\rightarrow\quad
\text{Result and check}
\]

The previous step remains inspectable until the current step makes sense.

## 3.2 Segment by meaning, not by arbitrary duration

A segmentation meta-analysis covering **56 investigations and 88 comparisons** found benefits for retention and transfer, along with reduced cognitive load. It also found that segmentation increased learning time. That trade-off matters for a “fast-track” product: more efficient presentation does not necessarily mean fewer seconds spent learning. citeturn649723view1

For a derivation, useful segment boundaries are usually changes in reasoning:

> Define the system → select the law → substitute the model → simplify → interpret the result.

A new shot is not necessarily a new conceptual segment. Conversely, one stable canvas can contain several well-signalled segments.

## 3.3 Use worked examples, then remove support

Worked-example research supports gradually removing solution steps, particularly when students are also prompted to explain the principle behind each step. Fading alone does not guarantee broad transfer to unfamiliar problems. citeturn806608search8

A proposed ExamLeaf progression is:

**Full example:** the narrator explains why each step is chosen.

**Completion example:** the student supplies one missing step.

**Independent example:** the student selects the relationship without the formula being displayed.

**Transfer example:** change the representation, conditions, or wording—not merely the numbers.

Do not call the third stage “independent” while leaving the completed method beside the question.

## 3.4 Ask for explanations that have a clear target

A meta-analysis of self-explanation prompts reported a positive average effect, but a useful self-explanation requires more than asking students to repeat a sentence. citeturn649723view2

Prefer:

> “Why must the temperature remain unchanged in this comparison?”

> “Which quantity stayed constant, and how does that determine the next step?”

Avoid:

> “Do you understand?”

The latter produces little evidence about what the learner actually understands.

---

# 4. Colours, typography, visual hierarchy, and comfort

## 4.1 There is no scientifically established “best learning colour”

Colour research is sensitive to context, luminance, saturation, task, and methodology. It does not justify universal claims such as “blue improves retention” or “green removes anxiety.” citeturn129227search0

Research on emotionally appealing multimedia design is more nuanced than either “colour improves learning” or “decoration is always harmful.” A systematic review found varied outcomes and substantial differences in implementation and learner populations; much of the evidence involved higher education. citeturn289891search3

**Recommendation:** give ExamLeaf a calm, attractive identity through spacing, alignment, legibility, and restrained colour. Treat hue preferences as a lower-priority experiment than explanation quality or retrieval practice.

## 4.2 Proposed ExamLeaf palette

These are **design specifications**, not neuroscientific optima.

### Primary light theme

| Role | HEX | Calculated contrast against `#F7F9FC` |
|---|---|---:|
| Background | **`#F7F9FC`** | — |
| Main text and equations | **`#14213D`** | **15.15:1** |
| Supporting text | **`#526074`** | **6.06:1** |
| Primary explanatory blue | **`#185ABD`** | **6.15:1** |
| Teal relationship/highlight | **`#087986`** | **4.87:1** |
| Amber condition or caution | **`#9A5B00`** | **5.14:1** |
| Purple secondary relationship | **`#6E44AA`** | **6.48:1** |
| Red error marker | **`#B42318`** | **6.23:1** |

The ratios were calculated for this report using relative luminance. They concern each colour against the specified background—not every possible pair of accent colours.

WCAG specifies at least **4.5:1 for normal text**, with relevant exceptions, and **3:1 for essential non-text graphical information** against adjacent colours. These thresholds are useful starting requirements, not a substitute for testing actual video frames. citeturn880959view0turn880959view1

### Optional dark theme

Use **`#101826`** as background and **`#EAF0F6`** as main text: calculated contrast is approximately **15.49:1**.

Do not claim that dark mode universally reduces fatigue. Research showing advantages for dark text on light backgrounds often concerns tasks such as proofreading, not long-term learning or every viewing environment. Offer and test a dark variant where appropriate. citeturn880959search0

## 4.3 Use colour to identify meaning, not decorate every object

Proposed rules:

**Keep identity stable.** A quantity should not change colour simply because the scene changed.

**Limit emphasis.** Use one dominant highlight at a time.

**Do not rely on colour alone.** Distinguish graph lines with labels, line patterns, or shapes.

**Respect scientific conventions.** A red oxygen atom is not an error indicator. A colour’s meaning must be clear in its context.

**Check adjacent colours.** Two colours that each contrast well with the background may be difficult to distinguish from each other.

Use a pale highlight area with dark text rather than a large block of saturated colour behind a long explanation.

## 4.4 Design text for the phone, not the editing monitor

For a 1920-pixel-wide video displayed at 360 pixels wide:

\[
\text{Displayed size}
=
\text{Source size}\times\frac{360}{1920}
\]

Therefore, **64-pixel source text becomes approximately 12 pixels high**, while **88-pixel text becomes approximately 16.5 pixels**.

That is why a technically sharp 1080p video can still be difficult to read.

### Proposed starting typography

| Element | Starting specification for a 1920 × 1080 master |
|---|---|
| Essential English labels | Approximately **88–96 px** |
| Main equations | Approximately **112–144 px**, with separately checked indices |
| Headings | Approximately **104–128 px** |
| Typeface | A clear family such as Inter or an appropriate Noto Sans script family |
| Weight | Medium or semibold for essential labels; avoid very thin strokes |
| Layout | Split, enlarge, or zoom before shrinking essential information |

These are pilot targets, not accessibility rules mandating a particular font size.

Test symbols that are easily confused: \(I/l/1\), \(O/0\), minus signs, decimal points, subscripts, superscripts, and Greek letters.

A derivation that does not fit at readable size should occupy multiple stages. Do not compress an entire textbook page into one frame.

## 4.5 Captions are an accessibility feature, not visual clutter to eliminate

Captioning supports access for deaf and hard-of-hearing learners, and research also identifies benefits for other audiences, including some second-language viewers. That does not mean every learner benefits equally from every caption configuration. citeturn589380view3turn833234search11

Provide accurate selectable captions, an accessible transcript, and a protected caption area.

Avoid simultaneously displaying:

> Full narration as a paragraph + animated diagram + equation + moving karaoke captions.

A concise definition or critical phrase can remain on screen. The problem is not all text duplication; it is competing demands and poor layout.

---

# 5. Animation and explanation strategy

## 5.1 Animate relationships, not merely objects

Research comparing animation with static visuals supports a conditional position: animation can help, but its value depends on what is being taught and how the visual information is presented. “More animation” is not a reliable learning prescription. citeturn129227search1

Use animation when it helps answer:

> **What changes? In what order? In which direction? Because of what?**

Use a static diagram when the student needs to inspect structure, compare labels, calculate, or reproduce an exam diagram.

| Learning goal | Proposed visual treatment |
|---|---|
| Understand a structure | Stable, labelled diagram |
| Understand a sequence | Stepwise state changes with persistent landmarks |
| Understand motion | Scientifically valid animation plus inspectable trajectory or graph |
| Understand an equation transformation | Show the operation and preserve correspondence between symbols |
| Compare two conditions | Matched before/after views with common scales |
| Solve a numerical problem | Stable givens and stepwise calculation |
| Reproduce an exam diagram | Final simplified view followed by drawing from memory |

## 5.2 Proposed animation density

For the first ordinary 2D revision pilots, budget approximately:

**25–35% of runtime for substantial, purposeful motion; the remainder for stable explanation, inspection, questions, and feedback.**

This is an **untested starting budget**, not a learning-science ratio. A process-heavy Biology lesson may legitimately need more motion; a mathematical proof may need less.

Do not require animation merely to satisfy the percentage.

Count substantial changes in the explanatory model—not tiny caption updates or a continuously moving cursor.

## 5.3 How frequently should the visual change?

Do **not** impose “a new visual every five seconds.”

Instead, distinguish:

**Layout changes:** a new representation or task.

**Semantic changes:** an arrow appears, a variable changes, a solution step is added.

**Decorative changes:** movement that conveys no new meaning.

For initial production, a layout may remain stable for **20–60 seconds or longer**, while meaningful steps appear within it. The relevant question is whether the student has enough information and time to perform the current task.

Proposed timing defaults:

| Event | Starting range |
|---|---:|
| Simple transition | **150–300 ms** |
| Highlight appearing | **300–600 ms** |
| Simple equation transformation | **0.8–1.5 seconds** |
| Hold after an important transformation | **2–4 seconds**, longer when necessary |
| Inspection of a completed diagram | Determined by its labels and required task, not a fixed limit |

All are production hypotheses. Never change a physical simulation’s behaviour merely to satisfy an animation timing rule.

## 5.4 Subject-specific applications

**Physics:** connect the physical model, graph, and numerical values. Keep axes and scale stable when comparing cases. Label slow motion, magnification, or other deliberate distortions.

**Chemistry:** maintain atom identity across representations. Distinguish a symbolic reaction, a particle model, and an observed phenomenon. Do not use a smooth visual morph to conceal a scientific discontinuity or unsupported mechanism.

**Mathematics:** show “divide both sides by \(R\)” rather than merely flying \(R\) across the equals sign. Make assumptions and excluded cases visible where relevant.

**Biology:** retain spatial landmarks and compartments. Show the completed state before advancing. For multi-stage processes, provide an inspectable state summary rather than requiring students to remember a disappearing animation.

These are proposed scientific communication requirements. They should be checked by the subject reviewer, not inferred from whether the animation looks convincing.

## 5.5 Attractive does not have to mean distracting

The research on seductive details concerns **interesting but instructionally irrelevant information**. Its implication is to remove material that competes with the explanation—not to produce ugly, emotionless videos. citeturn903930view3

ExamLeaf can be visually appealing through precise diagrams, elegant spacing, smooth but restrained motion, clear audio, and the satisfaction of seeing a difficult relationship become understandable.

---

# 6. Active student interaction: what to ask, when, and why

## 6.1 A pause is only useful when it has a task

“Pause and think” is too vague.

Every substantial interaction should specify:

**What to produce → what help is available → when to resume → how to check → what to repair.**

For example:

> “Pause and calculate the current. Write the relationship before substituting. Resume when you have an answer with a unit.”

This is operationally different from asking a rhetorical question and revealing the answer immediately.

## 6.2 Recommended interaction pattern

For an initial ten-minute revision pilot, use:

**Two or three substantial pause-to-write or pause-to-solve activities**, plus **three or four brief predictions or recall prompts**.

That usually creates an invitation to think approximately every **75–120 seconds**, but boundaries should follow the material. This interval is a design hypothesis.

Avoid forcing every lesson to include definitions, copying, drawing, prediction, solving, and multiple quizzes. Choose actions that match the objective.

### Interaction menu

| Activity | What it should accomplish | Proposed execution |
|---|---|---|
| Predict an outcome | Commit to an expectation before seeing the result | Ask one clear question; allow roughly **5–8 seconds** for a simple prediction. |
| Retrieve a definition | Reconstruct the essential meaning | Hide the definition; ask for its key components, then show an answer checklist. |
| Record a formula | Create a useful reference, not a transcript | Include symbol meanings, units, and applicability conditions. |
| Reconstruct a formula | Test retrieval rather than copying | Remove it, ask students to write it, then compare. |
| Draw a diagram | Reconstruct relationships or process order | Ask for a simple labelled sketch, not polished artwork. |
| Complete a missing step | Bridge demonstration and independence | Supply enough context to make the next operation achievable. |
| Solve independently | Test method selection and execution | Hide the method; allow a genuine learner-controlled pause. |
| Explain an error | Diagnose a misconception | Show the claim clearly as incorrect and require a reason or counterexample. |
| Verify an answer | Build monitoring habits | Check units, direction, order of magnitude, conditions, or process consistency. |

The time ranges are proposed defaults, not experimentally established optima.

## 6.3 Do embedded quizzes actually “reset attention”?

Early experiments found that interpolated tests could reduce mind-wandering and improve learning from video lectures. However, later work has not reproduced every benefit under every condition. citeturn871107search0

A 2022 study of 195 undergraduates found limited evidence for reduced task-unrelated thoughts and no statistically supported learning benefit in its particular design. A larger 2025 study involving 703 university and community-college students found learning benefits from interpolated retrieval, with effects moderated by the distraction conditions. citeturn897669view0turn589380view0

The correct conclusion is:

> **Retrieval practice has a strong general foundation. The claim that a quiz reliably resets everyone’s attention at a specific interval is much weaker.**

Design the questions for learning first.

## 6.4 Writing: understanding and reconstruction, not compulsory transcription

Do not tell students to copy the entire narration.

A proposed formula routine is:

> **Understand → record a compact reference → hide it → reconstruct → compare.**

For a definition, identify the components that make it scientifically correct. For an exam answer, distinguish essential terminology from unnecessary verbatim memorization.

Research comparing handwritten and typed notes does not justify a blanket claim that handwriting is always superior. A replication and extension found inconsistent differences and concluded that the superiority claim was premature. citeturn589380view1

Use handwriting where it supports equation work and exam practice, while permitting typing, oral explanation, or accessible alternatives.

## 6.5 Drawing: make it a reasoning task

Drawing can support learning, but its effectiveness depends on task design, the kind of representation, and learner skill. A 2025 review emphasizes mixed findings and important boundary conditions. citeturn589380view2

Good prompt:

> “Draw the two compartments, add the direction of movement, and label the condition that causes it.”

Poor prompt:

> “Copy this detailed illustration exactly.”

Supply a partial outline when drawing demands would otherwise obscure the science.

During demanding writing or drawing, **stop introducing new explanation**. Let students work, then resume with feedback.

## 6.6 Ten minutes of video is not necessarily ten minutes of study

A student who pauses three times for a minute has already turned a ten-minute video into at least thirteen minutes of study.

Be transparent:

> **“10-minute revision video, with optional practice pauses.”**

Do not make students feel slow for using the pauses that the lesson itself requires.

For an ordinary video platform, use a spoken pause instruction and a stable prompt. In an ExamLeaf player, provide a learner-controlled **“Continue to explanation”** action rather than an automatic answer reveal after a stressful countdown.

---

# 7. Narration speed, pauses, and changes in intensity

## 7.1 Faster can be efficient—but not universally better

A study of accelerated lecture playback found relatively small costs at 1.5× and 2× under its conditions, with poorer performance above 2×. Its materials included lectures on real estate and Roman history, with original speech rates around 157 and 166 words per minute. Those results do not establish that unfamiliar equations, second-language narration, or dense Biology processes should be delivered at 2×. citeturn649723view3

Likewise, observational MOOC findings about faster speech and engagement do not establish a causal improvement in learning. Watching longer or attempting an assessment is not equivalent to retaining more. citeturn615777search10

## 7.2 Proposed voice pacing standard

| Narration type | Initial target |
|---|---|
| Ordinary explanation | **130–155 spoken words per minute** |
| Familiar recap or straightforward transition | Approximately **145–165 wpm** |
| New symbolic relationship or dense terminology | Slower delivery, often equivalent to **90–120 wpm**, with meaningful pauses |
| Independent practice | Silence or minimal instructions |
| Final recap | Clear and compact, not rushed |

These are starting points for English-language pilots. Validate other languages separately rather than transferring word-rate targets directly.

For a ten-minute lesson with substantial silent processing time, approximately **1,050–1,250 narration words** is a reasonable initial writing budget. The actual requirement depends on the scene and pause design.

## 7.3 Pause at the point where thinking must happen

Proposed starting ranges:

**0.3–0.6 seconds:** between ordinary phrases where natural.

**0.8–1.5 seconds:** after a key causal statement or before an important contrast.

**2–4 seconds:** to inspect a completed transformation or diagram.

**5–8 seconds:** for a genuinely simple mental prediction.

**Learner-controlled pause:** for writing, drawing, multi-step calculation, or explanation.

Do not use a two-second silence as evidence that students had a fair opportunity to solve a problem.

## 7.4 Make intensity follow the reasoning

A useful pattern is:

> **Curious opening → steady explanation → deliberate emphasis → quiet attempt → precise feedback → calm conclusion.**

Emphasize logical relationships:

> “The current changes **because**…”

> “This conclusion holds **provided that**…”

> “Notice the difference between…”

Avoid constant excitement. No particular gender, accent, pitch, or breathiness should be treated as inherently optimal without audience testing.

Keep the core explanation free of background music as the initial default. That is a conservative production choice, not a claim that music always harms learning. Test any musical version against silence on comprehension and listening effort—not merely preference.

---

# 8. Confidence, encouragement, emotion, and trust

## 8.1 Genuine confidence is calibrated confidence

In a controlled college Physics study, students in active-learning conditions learned more while reporting a lower feeling of learning than students in passive conditions. The effort involved in learning can therefore distort subjective judgments. This does not mean any difficult experience is productive. citeturn871107view2

ExamLeaf should teach students to distinguish:

**“That explanation felt clear.”**

from:

**“I can now perform the relevant task without help.”**

The ideal outcome is not maximum confidence. It is confidence that appropriately reflects capability.

| Student state | Appropriate response |
|---|---|
| Correct and confident | Offer a less familiar application. |
| Correct but unsure | Identify the valid reasoning and provide a second independent check. |
| Incorrect and unsure | Supply a targeted hint and another attempt. |
| Incorrect but confident | Address the misconception explicitly with evidence or a counterexample. |

## 8.2 Build competence, control, and relevance

Motivation research distinguishes more autonomous reasons for learning from externally controlled motivation, with different relationships to educational outcomes. Much of the broad evidence is associative, so a few interface choices should not be advertised as a proven motivational intervention. citeturn827434search3

Control-value theory also emphasizes students’ perceptions of control and the value of the activity in understanding emotions such as enjoyment, anxiety, and boredom. citeturn861279search0

Proposed applications:

**Competence:** provide a task the student can complete using the explanation just given.

**Control:** allow pauses, replay, hints, and a route to prerequisite help.

**Value:** explain what the concept enables, including its examination use.

**Respect:** acknowledge uncertainty without ridicule or infantilizing language.

Do not remove exam goals in pursuit of “pure intrinsic motivation.” Students can reasonably value marks, understanding, future opportunities, and personal interest simultaneously.

## 8.3 Feedback should contain information

A large feedback meta-analysis found a positive average effect with substantial variation between implementations. The implication is not that any praise is powerful, but that feedback quality and content matter. citeturn827434search1

Use feedback that answers:

> **What was correct? What needs changing? What should the learner do next?**

### Proposed narration scripts

| Situation | Useful wording |
|---|---|
| Opening | “We will connect the diagram, the equation, and one exam-style application.” |
| Before a challenge | “Try the next step before looking at the solution. An unfinished attempt is useful here.” |
| Correct method | “You selected the right relationship. Now check the unit.” |
| Correct prediction | “Your prediction matches the model because you kept the other quantity constant.” |
| Calculation error | “The relationship is correct. Recheck the substitution rather than restarting the whole problem.” |
| Conceptual error | “The important distinction is the direction of the relationship. Let us compare the two cases.” |
| After a difficult step | “That was the key reasoning step. The remaining calculation uses it.” |
| Closing | “Check which parts you completed without help. Those are your starting points for the next practice question.” |

In a non-interactive video, use conditional wording:

> “**If** you obtained \(1.5\ \mathrm{A}\) using this relationship, your method matches the model.”

The narrator should not pretend to know that an unseen student succeeded.

## 8.4 Avoid identity-based praise and empty effort messages

Research on intelligence praise found adverse motivational responses under some conditions, particularly following difficulty. This is not a reason to become cold or never compliment students; it supports caution about making success a judgment of fixed intelligence. citeturn837224search1

Avoid:

> “You are a genius.”

> “This is so easy.”

> “You just need to try harder.”

Prefer:

> “Your diagram shows the correct relationship.”

> “This step is unfamiliar; use the previous result as a starting point.”

> “A different strategy will help here.”

Growth-mindset intervention reviews differ in their conclusions about size and conditions of benefit. Neither supports guaranteeing improved attainment through motivational slogans alone. citeturn232424search6turn232424search7

## 8.5 Reduce avoidable anxiety—not all challenge

A meta-analysis found a reliable association between anxiety and poorer working-memory performance, while also documenting important variation and methodological limitations. citeturn861279search1

Proposed ExamLeaf safeguards are predictable lesson structure, low-stakes practice, private attempts, available hints, and feedback that identifies a repairable issue.

Avoid public comparisons, humiliating error messages, threatening countdowns, and promises that imply failure is the student’s fault.

Videos should not be presented as treatment for persistent anxiety. The production goal is to avoid adding unnecessary threat.

## 8.6 Progress should reflect capability, not just consumption

Keep two indicators separate:

**Lesson completed:** the media has been viewed.

**Skill demonstrated:** the learner has successfully completed an appropriate task.

An initial correct answer is still not proof of durable mastery.

A proposed progress display might say:

> “Today: calculated with support. Next: solve a fresh question without the formula.”

That is more honest than awarding “Mastered” after watching the final frame.

---

# 9. Curiosity, storytelling, retention, and continued study

## 9.1 Use a genuine knowledge gap

A strong opening asks a question the student can understand but cannot yet confidently resolve.

Examples of proposed openings:

**Physics:** “Does doubling the voltage always double the current?”

**Mathematics:** “These two expressions look similar. Why does one require an extra condition?”

**Chemistry:** “What must remain unchanged when we balance this reaction?”

**Biology:** “The final structures look similar. Which process step distinguishes how they formed?”

Prequestioning research supports potential learning benefits, but effects depend on the questions and what is subsequently taught. Questions can direct attention toward selected information rather than improving everything equally. citeturn827434view1

Close the initial knowledge gap when the explanation reaches it. Do not withhold an essential answer merely to extend watch time.

## 9.2 Prefer causal stories over unrelated entertainment

A useful explanatory story has:

**A system → a change → a consequence → an explanation.**

It does not require an invented character, dramatic music, or a long historical anecdote.

Relevance can also come from students making their own connections. In a randomized high-school science study, a relevance-writing intervention improved interest and performance particularly for students with low expectations of success. It was a semester-level intervention, not proof that a ten-second “real-life connection” guarantees the same benefit. citeturn698760search0

A suitable ExamLeaf application is an occasional prompt:

> “Where else could this relationship help explain what you observe?”

Keep the connection scientifically accurate and proportionate to the lesson.

## 9.3 Correct misconceptions with an explanation, not a red cross

Research on refutation texts supports explicitly identifying and correcting misconceptions rather than assuming that presenting the correct statement will always displace the incorrect one. citeturn846030search9

Use a proposed sequence:

**Correct principle → clearly identified misconception → reason it fails → better model → new application.**

For example:

> “On an \(I\)-versus-\(V\) graph, a steeper line does not mean greater resistance. At the same voltage, the steeper line represents more current, so \(R=V/I\) is smaller.”

Keep the graph axes visible. Do not flash the wrong statement and then leave it unresolved.

## 9.4 Extend retrieval beyond the video

Spacing research shows that the useful interval between study occasions depends on the desired retention interval. There is no universally optimal “1–3–7” sequence. citeturn232424search0

Nevertheless, ExamLeaf needs a practical starting schedule. A proposed one is:

| Occasion | Practice |
|---|---|
| End of lesson | One unprompted explanation or application |
| Next day | Brief recall before reopening notes |
| About three days later | A changed numerical or diagram question |
| About one week later | Mixed practice requiring method selection |
| Later, according to exam timing | Another delayed check and targeted repair |

The dates are adjustable hypotheses.

Change the cues: use a paper-style question, a different diagram orientation where appropriate, or different wording. Students should not depend on ExamLeaf’s colour scheme or the narrator’s next sentence to retrieve the concept.

## 9.5 Encourage stopping at a useful point

The desired behaviour is not endless viewing.

A good ending is:

> “Complete one fresh question now, then return for the next topic.”

Avoid autoplay pressure, streak-loss guilt, variable rewards, and artificial scarcity. Use reminders only with student choice and a clear learning purpose.

---

# 10. Individual differences that should change the design

There is no single ideal pace for every Class 10–12 student.

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

Do not assign students to fixed “visual,” “auditory,” or “kinaesthetic” learning styles. Preferences and accessibility needs are real; evidence does not support the general claim that matching instruction to a declared learning style improves learning. citeturn253767search3

Most importantly, a revision video should not conceal a first-teaching problem. A student missing the underlying concept may need a longer preparatory explanation—not simply the same compressed lesson at a slower playback speed.

---

# 11. A complete 600-second lesson blueprint

## Example: Ohm’s law and interpreting current–voltage graphs

This is suitable as a **Class 10 revision example and a Class 12 prerequisite check**, not a complete Class 12 electricity lesson.

**Learning targets:** state the relevant condition, calculate current, and interpret resistance from a graph with \(I\) on the vertical axis and \(V\) on the horizontal axis.

The scientific model is an ohmic resistor under constant relevant physical conditions. The relationship and its applicability should be presented consistently with the textbook treatment. citeturn903930view2

**Production format:** approximately seven persistent layouts containing the following 41 instructional beats. These are not 41 scene cuts.

**Interaction design:** four brief predictions and three substantial learner-controlled practice pauses.

**Important:** the timecodes cover exactly ten minutes of media. Student-controlled pauses add study time. The quoted lines below are script excerpts, not the complete narration.

### 00:00–03:30: establish the model and reconstruct the relationship

| Time | Visual and narration direction | Student action |
|---|---|---|
| **00:00–00:10** | Show a resistor and a change from 2 V to 4 V. Ask: “Does twice the voltage always mean twice the current?” No long logo introduction. | Identify the question. |
| **00:10–00:18** | Hold the two conditions. Do not display the answer. | Make a private prediction. |
| **00:18–00:30** | Show three compact outcomes: relationship, calculation, graph. Say: “We will also identify the condition that makes the rule valid.” | Establish the goal. |
| **00:30–00:45** | Briefly recall current, potential difference, and their units. Keep labels adjacent to the circuit. | Reactivate prerequisites. |
| **00:45–01:00** | Establish the model: the same 10 Ω resistor, constant temperature and other relevant conditions. Keep that condition visible. | Notice what is controlled. |
| **01:00–01:15** | Show the first reading: 2 V and 0.2 A. Use clean instruments or numerical labels, not decorative particle motion. | Inspect the relationship. |
| **01:15–01:25** | Change voltage to 4 V while leaving the current reading blank. Ask for the prediction under these conditions. | Prepare an answer. |
| **01:25–01:33** | Eight seconds of stable visual and silence. | Predict the current. |
| **01:33–01:50** | Reveal 0.4 A. Compare the two cases with identical scales. Explain the proportional change. | Compare prediction with evidence. |
| **01:50–02:10** | State the relationship in words and connect it to the controlled condition. Close the opening question without implying the rule applies universally. | Build the causal qualification. |
| **02:10–02:30** | Introduce \(V=IR\). Identify each symbol in place. | Connect words to notation. |
| **02:30–02:45** | Show division by \(R\) on both sides to obtain \(I=V/R\). Retain the previous line during the transformation. | Follow the operation. |
| **02:45–03:00** | Show the unit relationship and a compact condition note. Avoid introducing another unrelated formula. | Organize the essential reference. |
| **03:00–03:12** | Hide the completed formula. Say: “Pause and write the current relationship and the condition under which we are using it.” | **Major pause 1:** reconstruct from memory. |
| **03:12–03:30** | Reveal a model response. Highlight the relationship, unit information, and condition—not a full paragraph of narration. | Compare and repair the note. |

### 03:30–07:20: worked example, reduced support, and graphical meaning

| Time | Visual and narration direction | Student action |
|---|---|---|
| **03:30–03:45** | Present 12 V across 6 Ω. Keep “Find current” visible. Mark known quantities and the target. | Recognize the task structure. |
| **03:45–04:05** | Choose \(I=V/R\), then substitute to obtain \(12/6=2\). Explain why this relationship is selected. | Follow the method, not just arithmetic. |
| **04:05–04:20** | Add A and check the result against the model. Keep the entire short solution visible. | Observe verification. |
| **04:20–04:32** | Keep 12 V but change resistance to 4 Ω. Show a partially completed expression and ask for the result and direction of change. | Complete a missing step. |
| **04:32–04:40** | Eight seconds of silence with no answer reveal. | Calculate and predict. |
| **04:40–05:00** | Reveal 3 A. Explain why lower resistance at the same voltage gives more current in this model. | Check the reasoning. |
| **05:00–05:15** | Introduce a graph explicitly labelled **current vertically, voltage horizontally**. | Establish the representation. |
| **05:15–05:35** | Plot the earlier points, using fixed axes and units. Build the line without changing scale. | Connect the measurements to the graph. |
| **05:35–05:55** | Show that the slope is \(\Delta I/\Delta V=1/R\). Use one highlighted rise/run pair. | Interpret slope. |
| **05:55–06:08** | Add a second, steeper line on the same axes. Ask which represents the smaller resistance. | Prepare a comparative prediction. |
| **06:08–06:16** | Eight seconds of silence. Keep both lines labelled and the answer hidden. | Choose and justify. |
| **06:16–06:35** | Compare currents at the same voltage. Explain why the steeper \(I\)-versus-\(V\) line represents smaller resistance. | Verify using the physical relationship. |
| **06:35–06:50** | Address the tempting wrong rule: “Steeper always means more resistance.” Emphasize checking which quantity is on each axis. | Correct the misconception. |
| **06:50–07:05** | Show a clearly labelled contrasting non-ohmic characteristic. Do not apply the constant-resistance interpretation to the whole curve. | Recognize a boundary of the model. |
| **07:05–07:20** | Return to the condition statement. Explain why the lesson did not claim every device behaves identically. | Consolidate applicability. |

### 07:20–10:00: independent performance, retrieval, and calibrated confidence

| Time | Visual and narration direction | Student action |
|---|---|---|
| **07:20–07:35** | Present a fresh problem: 9 V across 6 Ω. Ask for current, then ask what happens if resistance doubles while voltage stays fixed. Hide the formula. | Select a method independently. |
| **07:35–07:45** | Say: “Pause, write your relationship, calculate, and include the unit. Resume when ready.” Hold the prompt. | **Major pause 2:** solve independently. |
| **07:45–08:05** | Reveal \(I=9/6=1.5\ \mathrm{A}\), showing relationship before substitution. | Check method and result. |
| **08:05–08:20** | Reveal \(I=9/12=0.75\ \mathrm{A}\). Connect doubling resistance with halving current under the stated conditions. | Verify the changed case. |
| **08:20–08:35** | Give targeted repair options: wrong relationship, arithmetic, unit, or condition. Use conditional feedback rather than claiming every viewer succeeded. | Identify any specific error. |
| **08:35–08:50** | Remove solutions. Ask students to state the law with its condition and sketch the labelled \(I\)-versus-\(V\) graph. | Prepare a compact retrieval task. |
| **08:50–09:00** | Hold a clean prompt and invite pausing. Do not display a ghosted answer. | **Major pause 3:** recall and draw. |
| **09:00–09:20** | Reveal a model statement and graph. Provide a brief checklist: proportional relationship, condition, axes, shape. | Compare and repair. |
| **09:20–09:35** | Ask: “Which could you do without help: state, calculate, interpret?” Offer “secure on this check” and specific review routes. | Calibrate confidence. |
| **09:35–09:48** | Say: “A fresh question will show whether the method transfers. Use the next practice item without reopening the formula first.” | Plan an independent application. |
| **09:48–10:00** | Give a next-day retrieval instruction and a calm ending. No forced autoplay or “full marks guaranteed” message. | Leave with a concrete next action. |

### Why this blueprint is preferable to constant stimulation

The proposed lesson changes the **student’s task** repeatedly while keeping the visual environment stable.

It includes evidence of understanding, explicit conditions, a reduced-support example, an independent example, misconception correction, and a memory-based reconstruction.

The exact second boundaries remain hypotheses. A Biology process, Chemistry mechanism, or difficult Class 12 derivation should use the same principles without being forced into the identical timing pattern.

---

# 12. A/B experiments that can establish what works for ExamLeaf

## 12.1 Choose learning outcomes before choosing variants

The recommended primary outcome is:

> **Performance on a delayed, unprompted assessment containing unfamiliar but curriculum-aligned applications.**

A practical initial delay is seven days; that interval is a study-design choice, not the only valid measure of retention.

Secondary outcomes should include immediate understanding, task completion without hints, confidence calibration, total study time, listening effort, and voluntary return to useful practice.

Watch time should remain a diagnostic measure.

## 12.2 Prioritized experiments

| Priority | Comparison | Main question |
|---|---|---|
| **1** | Explanation-only versus explanation plus retrieval and feedback | Does the active version improve delayed performance enough to justify additional study time? |
| **2** | Full worked examples throughout versus gradually faded support | Does fading improve independent method selection? |
| **3** | Fewer substantial checkpoints versus more frequent brief checkpoints | Which pattern benefits learning without excessive interruption? |
| **4** | Clear static sequence versus semantically equivalent animation | Does motion improve understanding of this particular relationship? |
| **5** | Approximately 130 versus 150 wpm with the same substantive explanation | Who benefits from each pace, and what happens to study time and comprehension? |
| **6** | Specific task feedback versus generic but respectful feedback | Does specificity improve error correction and calibration? |
| **7** | Learner-controlled pause versus automatic answer reveal | Do students actually attempt the task, and does delayed learning improve? |
| **8** | Copying a compact reference versus reconstruction followed by checking | Which produces better later retrieval for the time invested? |
| **9** | Two accessible, aesthetically coherent palettes | Are there meaningful differences in reading accuracy and comfort? |

Do not test an unreadable palette against a readable one and label the result “colour psychology.”

## 12.3 Design the comparisons carefully

Randomly assign learners or classes as appropriate. Record prior knowledge, class level, language proficiency, and device conditions before interpreting group differences.

Keep scientific content and assessment difficulty equivalent. Decide whether the experiment is **content-matched** or **time-matched**: adding practice usually adds study time, while increasing speech rate changes runtime unless another element is adjusted.

Use parallel test items rather than showing the identical question repeatedly. Have written responses scored with a predefined rubric, preferably without the marker knowing which version the student watched.

Predefine the main outcome and analysis. Report attrition, confidence intervals, and all planned comparisons rather than selecting whichever metric looks favourable.

For experiments involving minors, use age-appropriate informed participation, necessary permissions, minimal data collection, and no intrusive emotion or attention surveillance.

## 12.4 Sample size: distinguish usability from efficacy

A small group can reveal that a graph label is unreadable. It cannot reliably establish a modest learning advantage.

As an illustrative calculation, a conventional two-group comparison targeting a standardized difference of **0.30**, with 80% power and a two-sided 5% significance level, requires approximately **175 independent learners per group** before allowing for attrition. A difference of **0.20** requires roughly **400 per group**.

These are approximate planning calculations, not a power analysis for a finished study. Classroom clustering, repeated observations, baseline adjustment, measurement reliability, and missing data change the requirement.

Begin with a small, diverse usability study; then run a properly powered learning study on the most consequential design decision.

## 12.5 Measure confidence calibration—not merely confidence increases

At selected checkpoints, ask students to estimate whether their answer is correct before seeing feedback.

Then distinguish:

**Accurate confidence**, **high-confidence errors**, and **correct answers accompanied by excessive uncertainty**.

A variant that makes students feel highly confident while increasing errors should lose—even when they prefer it.

Conversely, a useful variant should not unnecessarily leave successful students believing they are incapable.

---

# 13. Convert the psychology into production requirements

The ExamLeaf Video Engine should store pedagogical intent alongside its visual and audio instructions.

| Scene field | What it records |
|---|---|
| Learning objective | The capability this scene supports |
| Prerequisite | What the student must already know |
| Scientific relationship | The verified claim or model being explained |
| Attention target | The object or relationship that should dominate |
| Representation | Diagram, equation, graph, process state, or example |
| Learner action | Observe, predict, explain, write, draw, solve, or retrieve |
| Available support | Full example, partial hint, or independent task |
| Answer visibility | Whether the answer must remain hidden |
| Pause mode | Brief built-in silence or learner-controlled pause |
| Feedback | What a correct or incorrect attempt should lead to |
| Misconception | The specific incorrect interpretation being addressed |
| Delayed assessment | How this capability will later be tested |

### Release review should answer four questions

**Scientific:** Is every claim, diagram, transformation, condition, and answer correct?

**Instructional:** Does the learner get an opportunity to perform the target task without the explanation doing it for them?

**Perceptual:** Can the essential content be read and followed on the intended devices, with captions and audio working together?

**Emotional:** Are the challenges fair, feedback specific, and confidence statements honest?

Automated checks can flag contrast, text size, clipping, answer-reveal timing, missing units, absent captions, or suspiciously dense scenes. They cannot determine scientific validity or genuine student learning from visual polish alone.

## The recommended ExamLeaf standard

Build each lesson around:

> **One clear purpose, a small number of connected ideas, a stable visual model, explicit reasoning, meaningful student attempts, useful feedback, and a later opportunity to retrieve the learning.**

The strongest brand promise is not that ExamLeaf makes every topic feel effortless.

It is that **students can see what they understand, discover what still needs work, and become progressively more capable of answering without ExamLeaf beside them.**


=====================================================================
MESSAGE id=ba028713-2683-4c6c-b701-3d63d60f5713 role=user content_type=text create_time=1791884054.236 chars=5476
ATTACHMENTS: [{"id":"file_00000000ec8c820ba11e5201d4b98d83","is_big_paste":true,"library_file_id":"libfile_c00fe37693048191a53c4a47628ea00d","mime_type":"text/plain","name":"Pasted text(1).txt","size":14505}]
=====================================================================

Conduct an **in-depth, end-to-end business, marketing, student psychology, and financial analysis** to develop a profitable and scalable business model for **ExamLeaf**, initially targeting Assam Board Class 10 and 12 students, with future expansion across India.

### Our Proposed Business Model

We plan to combine **viral Instagram Reels, free educational tutorials, physical Sample Paper + Quick Revision Books, and premium chapter-wise videos** into one integrated learning ecosystem.

Our proposed funnel:

**Instagram Reels → Free Chapter Videos → Student Trust → Physical Book Purchase → Unlock Remaining Chapters → Practice & Revision → Referrals.**

Initially, we want to provide the **first 3 chapters of each subject free**. Students who purchase our physical ExamLeaf Sample Paper + Quick Revision Book can unlock all remaining chapter videos using a unique QR code or activation code.

We want ExamLeaf positioned as a **premium, results-oriented brand for serious students**, with compelling, curiosity-driven marketing that attracts attention while delivering real educational value.

### Research and Analyze

1. **Business Model Validation:** Critically evaluate our free-3-chapter strategy. Compare alternative freemium models, digital-only purchases, bundles, subscriptions, and book-linked video access. Recommend the most profitable and student-friendly structure.
2. **Viral Instagram Strategy:** Research student attention, Instagram algorithms, trending educational formats, Reel durations, hooks, thumbnails, captions, posting frequency, and shareability. Develop **30+ specific viral Reel ideas** covering quick revisions, exam tricks, misconceptions, challenging questions, formulas, and animated scientific explanations.
3. **Student Psychology & Branding:** Analyze how students develop trust, motivation, curiosity, confidence, and purchasing intent. Determine how to establish ExamLeaf as a premium, academically credible brand that serious students prefer, without discouraging beginners or using misleading claims.
4. **High-Converting Content:** Develop compelling but truthful titles, thumbnails, curiosity gaps, opening hooks, calls to action, and content structures that increase clicks, watch completion, shares, free-video registrations, and book purchases.
5. **Complete Conversion Funnel:** Design the student journey from Instagram to free lessons, registration, book purchase, QR activation, progress tracking, referrals, and repeat purchases. Identify friction points, conversion improvements, and suitable platforms (YouTube, website, app, WhatsApp).
6. **Physical Book Strategy:** Research how our Sample Paper + Quick Revision Books can compete with Oswaal, Arihant, and other publishers through quality, pricing, practice questions, detailed solutions, QR-linked tutorials, formula sheets, and board-specific revision resources.
7. **Pricing & Financial Analysis:** Calculate realistic printing, video production, marketing, shipping, commissions, infrastructure, and support costs. Model revenue, profit margins, customer acquisition costs, break-even, and cash flow for **500, 5,000, and 50,000 book sales**, using conservative, realistic, and optimistic assumptions.
8. **Marketing & Distribution:** Develop strategies for Instagram, YouTube Shorts, student referrals, teacher commissions, school/coaching partnerships, bookstores, Amazon/Flipkart, WhatsApp communities, and exam-season campaigns.
9. **Automation & Operations:** Recommend economical workflows for producing Reels from long-form tutorials, publishing content, student onboarding, book redemption, payments, fulfillment, analytics, customer support, and protecting digital content from unauthorized sharing.
10. **Risks & Growth:** Identify potential failures such as viral views without purchases, free-content-only students, piracy, high inventory costs, weak conversions, and competition from free YouTube videos. Recommend practical solutions and opportunities for expanding into guides, question banks, and AI-based answer evaluation.

### Required Deliverables

Provide a **complete, execution-ready business plan**, including:

- An honest verdict on our proposed strategy and recommended improvements.
- Competitor analysis and ExamLeaf's unique value proposition.
- 30+ Instagram Reel ideas with hooks and conversion CTAs.
- Student psychology, premium positioning, and marketing guidelines.
- Optimized free-to-paid funnel and book activation architecture.
- Product pricing, unit economics, profitability, and break-even calculations.
- A practical 90-day launch roadmap with budget and priorities.
- Growth metrics, conversion targets, automation strategy, and scalability plan.

**Research Requirements:** Use current Indian EdTech and publishing-market data, real competitor examples, verified platform guidance, and evidence-based psychology. Clearly separate verified facts from estimates. Challenge my assumptions and suggest better alternatives wherever necessary.

**Ultimate Goal:** Build ExamLeaf into a **highly trusted, recognizable, profitable educational brand** where viral content attracts students, free tutorials demonstrate quality, physical books generate revenue, and premium revision resources deliver genuine academic improvement.

**Be practical, critical, financially realistic, and specific. Explain exactly what to implement, how to execute it, what it will cost, what to avoid, and how to maximize sustainable growth.**


=====================================================================
MESSAGE id=ffa34e70-820f-4621-8d77-0aa37557d55d role=assistant content_type=text create_time=1791884996.757644 chars=201
=====================================================================

The economics look tighter than the funnel suggests: 500 sales mainly validate demand, while even 5,000 may not break even. CAC, fulfillment, discounts, sell-through, and tax treatment become decisive.


=====================================================================
MESSAGE id=d2ec027b-d30c-4d9c-8b46-673defcfef0b role=assistant content_type=text create_time=1791886471.690609 chars=50814
=====================================================================

# ExamLeaf: business model, launch strategy, and financial plan

## Executive verdict

**ExamLeaf can become a viable publishing-led education business—but “viral videos + a QR code inside a book” is not a sufficient competitive advantage.**

The stronger business is:

> **Board-specific revision and practice, with reliable solutions and short videos that help students correct the exact mistakes they make.**

Use free videos to demonstrate that system. Sell the convenience, structure, academic reliability, and practice experience—not merely access to information already available elsewhere.

I recommend **two initial Class 10 titles, three carefully selected free chapters per subject, an optional digital-only purchase, and a two-book bundle**. Do not begin by funding six books, a native app, a large custom video platform, and a nationwide marketing operation simultaneously.

The financial conclusions are important:

| Scale | Interpretation under the model developed here |
|---|---|
| **500 retained book sales** | A product-validation exercise, not enough to recover the initial content and launch investment. |
| **5,000 retained book sales** | Meaningful demand, but the base case still loses money after properly allocating content, staffing, and launch costs. |
| **50,000 retained book sales** | Potentially profitable—but only with controlled acquisition costs, good inventory sell-through, sufficient working capital, and disciplined distribution. |

In the **base operating scenario**, 50,000 retained sales produce approximately **₹1.82 crore of publisher revenue excluding modeled GST and ₹34.07 lakh of operating profit**, before financing and income tax. However, that scenario needs approximately **₹52.09 lakh of funding capacity**, including modeled working-capital headroom. The conservative scenario loses money even at 50,000 sales.

These are **planning scenarios, not sales forecasts or supplier quotations**.

### Download the execution tools

[**Editable financial model and launch workbook — Excel**](sandbox:/mnt/data/ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx)

[**Complete launch toolkit — ZIP**](sandbox:/mnt/data/ExamLeaf_Business_Launch_Toolkit.zip)

The workbook contains nine financial scenarios, channel-level economics, monthly cash flows, price/CAC sensitivity, digital-only economics, a launch budget, a 13-week roadmap, 36 Reel concepts, and a source ledger. The ZIP also contains the Reel backlog as CSV and an activation/operations runbook.

**Research date: 13 October 2026.** Verified public facts are cited below. Proposed prices, printing costs, conversion rates, staffing allocations, and campaign targets are explicitly treated as assumptions.

---

# 1. Validate the business before optimizing the marketing

## 1.1 What is sound about your proposed model?

Your brief proposes three free chapters, a physical book that unlocks the remaining videos, and an integrated practice-and-revision experience. It also explicitly invites alternatives to compulsory physical purchase. fileciteturn2file0L21-L32

The attractive feature is the **connection between a physical task and a targeted explanation**:

> Attempt a question → identify the error → scan the relevant lesson → understand the correction → solve another question independently.

That is a stronger product than a large video library attached to a book.

Retrieval practice has substantial research support, including classroom evidence. Nevertheless, this supports the learning mechanism—not a claim that an ExamLeaf purchase will produce a particular increase in marks. citeturn658056search7

## 1.2 What needs changing?

### Do not make “first three chapters” a permanent rule

Sequential free chapters can work when they contain essential foundations. But they can also demonstrate only the easiest part of the subject, fail to address the student’s immediate difficulty, or attract learners who never encounter your strongest teaching.

**Recommended free selection per live subject:**

| Free component | Purpose |
|---|---|
| One foundational chapter | Demonstrate clarity and make later learning accessible. |
| One commonly difficult chapter | Show that ExamLeaf can resolve real confusion. |
| One representative later chapter | Demonstrate that quality extends beyond introductory material. |
| One complete sample paper with useful solutions | Prove the quality of the paid practice product. |
| Short previews of other chapters | Show coverage without interrupting an explanation halfway through its answer. |

Three is a **testable starting point**, not a proven optimum. Three chapters out of ten is a very different offer from three out of twenty.

Do not restrict all Reels to the free chapters. A useful misconception correction from a paid chapter can stand alone and lead to a relevant preview, worksheet, or product demonstration.

### Do not force every customer to buy a physical book

Some learners will want the book. Others will already own a question bank, need immediate access, or face inconvenient delivery.

**Digital-only can be profitable despite its lower selling price**, because printing and shipping disappear. In the illustrative model, a ₹299 digital-only subject purchase contributes about **₹112 before fixed content costs**, after the specified usage, support, payment, and acquisition allowances.

Compulsory physical purchase therefore does not automatically maximize profit.

### Do not make paid videos the entire reason to buy

Students already have alternatives. PW has a dedicated ASSEB Class 10 offering, including free content and paid programs. Assam-specific digital education is not an uncontested market. citeturn480908view6

The purchase proposition should be:

> **“A complete, checked revision-and-practice system for your board, with explanations connected to the questions you need to solve.”**

Not:

> “Pay us because the remaining videos are locked.”

---

# 2. Recommended product and pricing structure

## 2.1 Launch offers

These are **proposed price tests**, not existing ExamLeaf prices.

| Offer | Proposed price | What it contains | Recommendation |
|---|---:|---|---|
| Free learning | ₹0 | Three complete chapter lessons, diagnostic questions, one sample paper and solutions | No registration required to begin watching |
| Digital-only subject edition | **₹299** | Remaining chapter lessons, selected practice resources, progress/checkpoint features where lawfully implemented | Offer alongside the book |
| One subject book + digital access | **₹499** | Printed revision/practice book, complete printed solutions, corresponding digital package | Main product |
| Two-book Class 10 bundle | **₹949** | General Science + General Mathematics, both digital packages | Preferred DTC basket |
| Institutional/bulk purchase | Negotiated | Same legitimate product, bulk delivery and defined support | Discount according to order economics |
| Monthly subscription | Not initially | Would require an ongoing service proposition | Postpone |

A proposed MRP of **₹549** can be tested, but do not present it as a previously charged price unless that is true. Avoid permanent fake “today only” promotions.

The financial base case uses **₹479 average DTC realization per book**, allowing for the actual mix of bundles and coupons. It does not assume every copy sells for ₹499.

## 2.2 Access terms

My recommended starting policy is:

**Twelve months of access from activation, for the subject and edition purchased, with a clearly printed latest-redemption date.**

Also disclose that:

- Future editions, new boards, and future AI services are not automatically included.
- There is no automatic renewal.
- Shared-family-phone use and legitimate device replacement are supported.
- The printed book remains useful without activating the digital package.

For digital customers upgrading to the corresponding book, credit the **actual earlier digital payment** against the package within a disclosed period. Keep one entitlement and record only the incremental purchase value.

## 2.3 Compare the alternative models honestly

| Model | Advantage | Main weakness | Verdict |
|---|---|---|---|
| Book-only unlock | Simple positioning; supports physical distribution | Delivery friction; loses digital-only buyers | Too restrictive as the sole route |
| Book + optional digital-only | Accommodates different needs; reveals willingness to pay | Requires careful upgrade and channel policies | **Best initial structure** |
| Everything free, books optional | Broad reach and trust | Harder to recover content costs without strong distribution | Possible later, not the safest starting model |
| Low-priced monthly subscription | Low initial payment | Seasonal use, churn, cancellation friction, weak recurring value | Avoid initially |
| Annual all-subject subscription | Higher advance collection | Large catalogue and support obligations | Consider only after several strong subjects |
| AI evaluation subscription | Potential recurring utility | Accuracy, child-data, support, and inference costs | Separate later product |

---

# 3. Assam market reality and competitive positioning

## 3.1 Use the correct examination structure

ASSEB now has **Division I**, formerly SEBA, and **Division II**, formerly AHSEC. Product metadata, syllabus references, and edition labels should reflect the current board structure while retaining familiar search terms where useful. citeturn973282search1

For Class 10, build examination-aligned **General Science and General Mathematics** products—not separate Physics, Chemistry, and Biology books simply because your video engine organizes content by scientific discipline. Verify the current syllabus and subject structure before production. citeturn358323search4turn973282search7

For Class 12, Physics, Chemistry, Mathematics, and Biology can become separate titles.

**Recommended launch sequence:** Class 10 Science and Mathematics first, unless paid reservations and teacher partnerships demonstrate a materially stronger Class 12 opportunity.

## 3.2 Shared-device access matters

ASER 2024’s Assam rural survey found that **91.4% of surveyed 14–16-year-olds had a smartphone at home**. However, **among those able to use a smartphone, only 14.6% owned one themselves**. These are different denominators, and the survey is rural—not an all-Assam personal-device census. citeturn676578view2

The practical implication is substantial:

**Do not design the service around the assumption that every student owns a private phone.**

Make free viewing easy, permit account recovery, accommodate parent purchasing, avoid unnecessary app installation, and ensure the physical book remains valuable offline.

## 3.3 Do not underwrite the business using an inflated national market size

The relevant market is:

\[
\text{Board cohort}
\times
\text{subject eligibility}
\times
\text{print medium}
\times
\text{reachable geography}
\times
\text{ability and willingness to pay}
\]

The total number of Class 12 students is **not** the market for four science-subject books.

I did not reconcile the exact 2026 Assam participation figures to an official class-and-stream census. Before a large print commitment, obtain current **district, stream, and medium-level counts** and build the serviceable market from actual school and retail coverage.

A practical initial market estimate is more useful than a national EdTech valuation: count the students your signed or actively engaged schools, coaching partners, bookstores, and DTC channels can realistically reach.

## 3.4 Competitor comparison

| Competitor | Verified example or strength | What ExamLeaf should learn |
|---|---|---|
| **Oswaal** | Its current catalogue lists Class 10 Science sample papers around ₹449 and Class 12 Physics at ₹499; current products advertise digital/AI-related features | Digital additions and premium presentation are already competitive expectations |
| **Arihant** | Its iSucceed range combines sample papers and revision aids; one checked 2027 ISC five-book bundle was listed at ₹962 | Strong discounting and feature-rich bundles create price pressure; compare exact board/SKU, not only brand |
| **PW ASSEB** | Assam-specific Class 10 free and paid learning offerings | “Assam-specific videos” alone are not a defensible differentiation |
| **Local publishers, coaching notes, bookstores** | Exact local shelf pricing and adoption were not independently audited here | Obtain and review physical copies; local trust and distribution may matter more than online aesthetics |

The Oswaal and Arihant examples concern different products and, in some cases, different boards. They are **pricing and feature references**, not like-for-like proof that ExamLeaf should charge the same amount. citeturn140858view0turn509123view0turn660650view6turn480908view6

### ExamLeaf’s strongest proposed differentiation

> **Assam-board practice with clear solutions, short misconception-specific explanations, and a visible route from a wrong answer to an independently correct one.**

The defensible assets would be the checked question-and-solution library, board-specific editorial process, teacher relationships, distribution, corrections system, and evidence of useful learning—not the QR technology.

---

# 4. Physical book strategy: compete through usefulness

## 4.1 A workable first specification

Start by quoting a **256-page, approximately 7 × 10-inch book**, with a predominantly black-and-white interior, readable diagrams, suitable writing space, durable binding, and a restrained colour cover.

This is a prototype specification, not a final requirement for every subject.

| Section | Illustrative page allocation |
|---|---:|
| How to use the system, syllabus map, diagnostic | 16 |
| Quick revision notes, formulas, conditions, diagrams | 56 |
| Topic practice and common errors | 24 |
| Eight full sample papers | 64 |
| Detailed solutions | 80 |
| Trackers, answer checklists, revision plan | 16 |
| **Total** | **256** |

Actual pagination must determine whether that allocation is educationally adequate.

**Do not promise 30 fully solved papers, extensive revision notes, and spacious solutions inside this extent without testing the manuscript.** More papers are not automatically more useful than fewer, better-explained papers.

For longer Mathematics or derivation-heavy Class 12 titles, increase the extent and reprice rather than compressing the text.

## 4.2 Product quality standards

The paid book should include **all essential solutions in print**. Digital explanations should add diagnosis, visualization, alternative approaches, and extra practice.

Use:

**Foundation → Board-standard → Stretch**

rather than implying that only “toppers” deserve the difficult material.

Clearly distinguish an **official marking scheme** from an **ExamLeaf-authored answer rubric**. Publish an errata page, edition number, syllabus version, and a method for reporting errors.

The useful QR destinations are specific:

> “Why this sign is negative.”

> “How to choose the law.”

> “How to interpret this diagram.”

Not simply a generic chapter homepage containing a long playlist.

## 4.3 Printing decisions that protect margin

Obtain three written quotations for the **same specification**, including cover, binding, scratch-code insertion, tax, freight, spoilage tolerance, replacement terms, and payment schedule.

Public short-run printing rates can be considerably higher than an attractive bulk offset assumption; one checked printer separately prices printing and binding. That is why the model’s ₹105 or ₹78 costs must not be treated as obtained quotations. citeturn673898search10

Quote **per title, language, and batch**. Fifty thousand aggregate sales split across numerous SKUs do not give every SKU the economics of a 50,000-copy run.

---

# 5. Student psychology and premium branding

## 5.1 “Premium” should describe the service, not the student’s status

Recommended positioning:

> **Clear concepts. Deliberate practice. Exam-ready answers.**

Supporting message:

> “Built for students who want to practise seriously—even when a topic currently feels difficult.”

Avoid “only for intelligent students,” “weak students cannot understand this,” and “buy this to become a topper.”

## 5.2 Trust must be demonstrated before it is requested

A strong trust-building experience is:

> Student attempts a question → ExamLeaf identifies the relevant mistake → the explanation resolves it → the student completes a related question without help.

A pleasant feeling of clarity is not sufficient evidence. Research has shown that perceived learning and measured learning can diverge, although the cited experiment was in university Physics rather than ExamLeaf’s market. citeturn658056search2

**Proposed trust signals:** visible academic reviewers, a complete specimen paper, real page photographs, clear content coverage, an accessible corrections log, transparent access terms, and responsive support.

## 5.3 Address three different decision-makers

| Decision-maker | Main question | Best evidence to show |
|---|---|---|
| Student | “Will this help me solve questions I currently get wrong?” | One strong explanation followed by a successful independent attempt |
| Parent | “What exactly are we paying for, and is it reliable?” | Full inclusions, sample pages, access period, delivery and support terms |
| Teacher/coaching partner | “Are the questions, solutions, and board alignment trustworthy?” | Specimen book, syllabus mapping, reviewer process, error-reporting channel |

## 5.4 Use confidence-building feedback, not promises

Prefer:

> “Your method is correct; recheck the substitution.”

> “You identified the right relationship. Now include its condition.”

> “Try a fresh question before deciding that the chapter is secure.”

Avoid invented statistics such as “90% of students get this wrong” and unsupported claims such as “guaranteed 95%.”

CCPA’s education/coaching advertising guidance addresses misleading score guarantees, success claims, hidden information, false urgency, and the use of student success stories. Have the precise applicability to ExamLeaf reviewed before launch. citeturn250458view3

---

# 6. Instagram and YouTube acquisition strategy

## 6.1 Optimize for qualified interest, not maximum reach

Meta describes ranking as involving multiple predictions and signals. Its creator Best Practices hub also provides account-specific guidance. Neither establishes a universal Reel length, posting frequency, or guaranteed viral formula. citeturn886284view1turn140858view3

Use the following as **launch experiments**:

| Element | Proposed starting rule |
|---|---|
| Frequency | Four or five reviewed Reels per week |
| Most clips | 20–45 seconds, one concept or one mistake |
| More complex explanations | 45–75 seconds when needed |
| Hook | A clear question, contradiction, or unfinished task—not unrelated spectacle |
| Cover text | Short, readable, topic-specific |
| Captions | Audience + useful promise + necessary condition + one CTA |
| Music | Optional; never necessary to make the explanation work |
| Distribution | Re-layout and publish suitable material to YouTube Shorts as well |
| Review | Compare qualified visits, attempts, and purchases by topic/format cohort |

Use licensed audio and original visual assets. Do not distort a scientific diagram to follow a trend.

## 6.2 A high-converting Reel structure

**0–3 seconds:** identify the problem.

**3–8 seconds:** invite a prediction or point out the tempting error.

**8–30 seconds:** deliver a complete explanation.

**Final seconds:** offer one relevant next action.

Example:

> **Hook:** “Which line represents the larger resistance? Check the axes.”

> **Payoff:** Show the comparison at the same voltage.

> **CTA:** “Try the three-question graph check.”

Do not ask viewers to like, follow, comment, save, tag three people, and buy—all in the same clip.

## 6.3 Truthful titles and thumbnails

| Content | Proposed title | Cover/thumbnail |
|---|---|---|
| Electricity | “HSLC Electricity: Read the Graph Before Using the Formula” | **CHECK THE AXES** |
| Algebra | “This Cancellation Can Remove a Valid Answer” | **WHERE DID IT GO?** |
| Chemistry | “Balance the Equation Without Changing the Substance” | **COEFFICIENT OR SUBSCRIPT?** |
| Biology | “Chromosome Count and DNA Amount: Keep Them Separate” | **TWO DIFFERENT COUNTS** |
| Product demonstration | “How One ExamLeaf Question Links to Its Explanation” | **QUESTION → REPAIR → RETRY** |

The title should accurately describe what the viewer receives. A 60-second checklist is not “the complete chapter mastered in one minute.”

---

# 7. Thirty-six specific Reel concepts

These are **original creative drafts, not field-tested viral formats**. Match them to the current syllabus and have every explanation reviewed before publishing.

The workbook contains fuller visual directions, caption opening lines, duration targets, scientific checks, priorities, and statuses.

## Class 10 acquisition: launch first

| # | Topic and hook | Visual approach | Single CTA |
|---|---|---|---|
| 1 | **Ohm’s law:** “Does twice the voltage ALWAYS mean twice the current?” | Matched resistor cases; reveal the condition | Watch the free Electricity lesson |
| 2 | **Graphs:** “Which line has the larger resistance? Check the axes.” | Two labelled \(I\)-versus-\(V\) lines | Try the graph check |
| 3 | **Circuits:** “Same resistors, same supply—which circuit uses more power?” | Matched series/parallel diagrams | Open the worked comparison |
| 4 | **Mirrors:** “Move the object—where will its image move?” | Stepwise ray diagram | Try the next ray question |
| 5 | **Lens signs:** “The arithmetic is right. Why is the answer wrong?” | Find one wrong sign | Get the sign checklist |
| 6 | **Balancing:** “Balance this without changing the substance.” | Atom-count tiles; fixed subscripts | Solve the next equation |
| 7 | **pH:** “One pH unit: one small change?” | Compare labelled cases | Watch the acids-and-bases lesson |
| 8 | **Ionic compounds:** “Same salt—why compare the solid with the melt?” | Fixed lattice versus mobile ions | Open the conductivity explanation |
| 9 | **Redox:** “Who is oxidised—and what changed?” | Highlight the relevant change | Try the identification card |
| 10 | **Algebra:** “This cancellation quietly deletes an answer.” | Check the excluded case | Watch the algebra repair |
| 11 | **Trigonometry:** “Identity—or true only for this angle?” | Contrast two statements | Try the identity pair |
| 12 | **AP:** “The nth term and the sum answer different questions.” | Sequence versus accumulated sum | Get the AP decision card |
| 13 | **Similarity:** “Double a length—what happens to the area?” | Scaled figures and unit squares | Try the scaling challenge |
| 14 | **Plant transport:** “Which tissue belongs on this route?” | Simplified transport pathways | Watch Life Processes revision |
| 15 | **Reflexes:** “Fast response—does that mean the brain learns nothing?” | Separate response and information paths | Label the reflex-arc sketch |
| 16 | **Inheritance:** “A 3:1 ratio is not a promise about exactly four offspring.” | Probability versus small samples | Open the inheritance explanation |
| 17 | **Stomata:** “Open the pore: what useful exchange and cost change together?” | Relevant arrows only | Draw and check the diagram |

## Class 12 backlog: release when the corresponding product is ready

| # | Topic and hook | Visual approach | Single CTA |
|---|---|---|---|
| 18 | **Gauss’s law:** “Zero flux—does that mean zero field?” | Closed surface with balanced contributions | Watch field versus flux |
| 19 | **Current:** “Must electrons travel from the switch to the bulb first?” | Separate drift from circuit response | Open Current Electricity revision |
| 20 | **Capacitors:** “Battery connected or disconnected? The answer changes.” | Two cases with different fixed quantities | Try both cases |
| 21 | **Lenz’s law:** “Choose the direction before the animation reveals it.” | Motion, flux change, then answer | Watch the induction explanation |
| 22 | **Nernst equation:** “Before the logarithm, build this correctly.” | Construct reaction quotient | Open the full example |
| 23 | **Kinetics:** “Can the unit of \(k\) help check the reaction order?” | Dimensional comparison | Solve the second question |
| 24 | **Organic chemistry:** “Same starting molecule. Different conditions. Same product?” | Reagent/condition cards | Get the conditions map |
| 25 | **Coordination:** “Find the oxidation state before naming the complex.” | Charge ledger | Try one naming question |
| 26 | **Inverse functions:** “Why can an inverse need a restricted domain?” | Select an appropriate branch | Open inverse-functions revision |
| 27 | **Differentiation:** “One missing factor changes the derivative.” | Nested-function boxes | Try the next derivative |
| 28 | **Integration:** “Does \(+C\) really matter?” | Family of curves and one condition | Watch the worked example |
| 29 | **Probability:** “\(P(A\mid B)\) or \(P(B\mid A)\)?” | Change the reference group | Try the conditional pair |
| 30 | **Cell division:** “Chromosome count and DNA amount are different counters.” | Stage-labelled model | Count the next stage |
| 31 | **Replication:** “Why do the two new strands look different?” | Persistent strand directions | Watch the walkthrough |
| 32 | **Microbiology:** “Bacterium or virus—why does the distinction matter here?” | Relevant structures and mechanisms | Open the syllabus explanation |
| 33 | **Ecology:** “Which pyramid are you drawing: energy or biomass?” | Clearly named diagrams and units | Try the ecosystem question |

## Trust and conversion content

| # | Hook | Visual approach | Single CTA |
|---|---|---|---|
| 34 | “Which line makes this answer scientifically complete?” | Improve an original model answer | Inspect a solved specimen paper |
| 35 | “It feels clear. Can you do the next one without the video?” | Hide the method; show a fresh question | Take the free checkpoint |
| 36 | “One wrong step. One page. One explanation.” | Real book page → QR → targeted repair → retry | Preview the book and access terms |

Launch with the Class 10 and trust formats. Publishing Class 12 purchase CTAs before the corresponding product exists would waste attention and undermine trust.

---

# 8. The complete conversion funnel

## 8.1 Recommended platform roles

**Instagram:** discovery and short proof of teaching quality.

**YouTube:** searchable free chapter lessons and Shorts-to-long-video handoff. YouTube provides a related-video feature for Shorts, subject to the relevant account access requirements. citeturn673898search1

**ExamLeaf website:** curriculum navigation, sample pages, checkout, activation, and paid lessons.

**WhatsApp:** permissioned order/support messages and optional revision reminders—not compulsory student groups. WhatsApp’s policy requires appropriate permission, expectations, and opt-out handling. citeturn874416view4

**Native app:** postpone until the website’s usage and support data reveal a need that justifies it.

## 8.2 Journey and friction removal

| Stage | Likely objection | Proposed implementation | Measure |
|---|---|---|---|
| Reel discovery | “Is this relevant to my exam?” | Class, board, topic and medium are clear | Qualified visits, not only plays |
| Free lesson | “Will this explain it properly?” | Begin immediately; no compulsory phone capture | Meaningful participation |
| Practice | “Did I actually understand?” | One independent question and feedback | Attempts and answer quality |
| Registration | “Why do you need my details?” | Offer saved progress or purchase utility after value | Lawfully completed registrations |
| Product page | “Why buy when videos are free?” | Show the full practice system, specimen and inclusions | Product-to-checkout rate |
| Checkout | “What is the final cost?” | Upfront delivery, access and refund information | Paid, retained orders |
| Delivery | “Where is the book?” | Tracking and realistic dispatch commitments | Delivery failures and contacts |
| Activation | “Will this code work on our phone?” | Simple redemption and recovery | Valid first-attempt success |
| Practice cycle | “What should I do next?” | Question → targeted explanation → retry | Independent practice |
| Referral | “Is it worth recommending?” | Ask after a useful experience | Retained referred purchases |

## 8.3 Why viral reach can still produce few sales

An **illustration**, not a benchmark:

\[
1{,}000{,}000 \text{ reached accounts}
\times 20\% \text{ relevant}
\times 2\% \text{ visit}
\times 50\% \text{ qualify}
\times 5\% \text{ purchase}
=100 \text{ buyers}
\]

At 1.5 books per order, that is **150 books**.

Repeated Reel plays are not unique accounts, visits are not students, and students are not necessarily purchasers.

The lesson is not that Reels are ineffective. It is that **national viral reach cannot substitute for relevant demand, a credible product, and distribution**.

## 8.4 The 5,000-book base-channel plan

| Channel | Retained books | Illustrative requirement |
|---|---:|---|
| DTC | 2,250 | 1,500 customers at 1.5 books/order |
| Institutional/bulk | 1,000 | 20 partners selling/distributing 50 copies each |
| Trade/bookstores | 1,250 | 25 outlets selling 50 copies each |
| Marketplace | 500 | Actual fulfilled, retained sales |
| **Total** | **5,000** | Not a commitment already secured |

At a 5% qualified-free-learner-to-order rate, the DTC portion requires **30,000 qualified learners**. At 3%, it requires 50,000; at 8%, 18,750.

This is why teacher, search, school, and retail distribution should complement social media from the beginning.

---

# 9. Activation, security, and student-friendly access

## 9.1 Separate navigation from entitlement

A public QR code should open the relevant chapter page.

A **separate protected activation secret** should grant paid access.

Recommended implementation:

```text
Purchase / issued physical code
            ↓
Learner or guardian account
            ↓
Consent and eligibility checks
            ↓
Atomic one-time redemption
            ↓
Subject + edition entitlement
            ↓
Short-lived authorized video token
```

Generate strong random codes, store hashes rather than exposed secrets, rate-limit attempts, and record SKU, edition, batch, issuing status and redemption history.

Test duplicate claims, delayed payment webhooks, gifts, refunds, scratched codes, wrong-account redemption, and device replacement.

## 9.2 Use proportionate protection

Cloudflare Stream supports private playback through signed tokens and origin restrictions. These help control access; they do not prevent screen recording. citeturn874416view7

A reasonable starting policy is **two registered devices and one concurrent stream**, with accessible support.

Avoid intrusive fingerprinting, visible student phone-number watermarks, and punitive lockouts on shared family devices.

## 9.3 Minors’ data is a launch requirement

The DPDP Rules have phased commencement, including important rules commencing eighteen months after publication. They include provisions on verifiable parental consent and limited educational exceptions. Do not assume that every provision is already operative—or that ExamLeaf automatically qualifies for an exception. citeturn658056view4turn658056view5

Have counsel review the actual registration, progress-tracking, analytics, and advertising design.

**Do not build the funnel around behavioural retargeting of children.** Meta already restricts teen advertising targeting; design paid acquisition around appropriate adult purchaser/contextual routes rather than student profiling. citeturn660650view3

A phone OTP alone does not establish that someone is an adult or necessarily satisfy parental-verification requirements.

---

# 10. Pricing and unit economics

## 10.1 What is verified versus estimated?

| Input | Status |
|---|---|
| Razorpay standard 2% platform fee plus GST | Published provider pricing; promotional periods excluded |
| Amazon Books referral fee of 2% for prices above ₹250 through ₹500 | Published category rate; not the total selling cost |
| Cloudflare delivery at $1 per 1,000 delivered minutes | Published provider tariff |
| Printing, courier cost, CAC, sell-through, staffing and conversion rates | Planning assumptions requiring validation |
| ₹90/USD | Budget conversion assumption, not a live exchange-rate quote |
| 18% output GST on the bundle | Cautious model assumption, not a classification conclusion |

Amazon also charges other fees, and book bundles may have different category treatment. Do not interpret a low or zero referral rate as free distribution. citeturn480908view0turn874416view6turn480908view3

### Tax warning

**Do not assume the entire book-plus-premium-video offer is exempt merely because it contains a printed book.**

The actual treatment depends on the supplies, contract and applicable classification. GST guidance distinguishes composite supplies from mixed supplies. The workbook therefore includes a cautious 18% case and a separate zero-output-tax sensitivity—not a recommendation to claim exemption. citeturn250458view2

Obtain written advice before finalizing prices and invoices.

## 10.2 Scenario assumptions

All scenarios use the same cautious output-tax assumption.

| Assumption | Conservative | Base | Optimistic |
|---|---:|---:|---:|
| Average DTC realization/book | ₹429 | ₹479 | ₹499 |
| DTC books/order | 1.2 | 1.5 | 1.8 |
| Incremental DTC CAC/customer | ₹220 | ₹120 | ₹70 |
| DTC courier/order | ₹85 | ₹65 | ₹55 |
| Combined trade discount from MRP | 45% | 40% | 35% |
| Inventory sell-through | 75% | 90% | 97% |
| Landed print cost: 500-sale project | ₹190 | ₹160 | ₹135 |
| Landed print cost: 5,000-sale project | ₹125 | ₹105 | ₹88 |
| Landed print cost: 50,000-sale project | ₹95 | ₹78 | ₹65 |

The print costs must be achieved at the actual **per-SKU phased batch sizes**. They are not confirmed quotes.

Base channel mix is **45% DTC, 20% institutional, 25% trade, 10% marketplace**.

## 10.3 Base economics at 5,000 retained book sales

“Retained” means paid sales remaining after refunds/returns. It does not mean copies merely dispatched to a distributor.

| Per retained book | Base model |
|---|---:|
| Weighted publisher realization including modeled GST | ₹430.15 |
| Publisher revenue excluding modeled GST | **₹364.53** |
| Printed-copy cost | ₹105.00 |
| Unsold-edition write-off allocation | ₹11.68 |
| Full-entitlement streaming reserve | ₹29.74 |
| Support/servicing reserve | ₹8.00 |
| Weighted shipping, packaging, payment/channel fees and claims | ₹53.49 |
| Incremental acquisition/marketplace advertising | ₹38.50 |
| **Contribution after variable costs** | **₹118.13** |
| **Contribution margin on net publisher revenue** | **32.4%** |

At 90% sell-through, 5,000 retained sales require approximately **5,556 printed copies**. The model fully expenses unsold edition stock rather than assuming it will eventually sell.

The streaming reserve covers the modeled usage over the access obligation—not just the first month. Fixed video storage and tooling are separately budgeted.

## 10.4 Channel contribution matters more than headline discounts

At the same base 5,000-copy cost tier:

| Channel | Contribution per retained book |
|---|---:|
| DTC, after modeled CAC | **₹98.88** |
| Institutional/bulk | **₹175.53** |
| Trade/bookstores | **₹104.74** |
| Marketplace, after modeled advertising | **₹123.47** |

These are model outputs, not channel guarantees. Institutional economics are attractive partly because consolidated delivery and lower acquisition friction can offset the discount.

**Do not stack a full retailer/distributor discount, a teacher commission, a referral payout, and paid-ad acquisition on the same order without recalculating contribution.**

---

# 11. Revenue, profit, break-even, and cash flow

## 11.1 Nine scenarios

All money columns below are in **₹ lakh**. Revenue excludes modeled output GST. Profit is before financing and income tax, after the specified variable and fixed costs.

| Retained books | Scenario | Net publisher revenue | Contribution/book | Fixed costs | Operating profit/loss |
|---:|---|---:|---:|---:|---:|
| 500 | Conservative | 1.60 | −₹98.50 | 7.50 | **−7.99** |
| 500 | Base | 1.82 | ₹56.89 | 6.50 | **−6.22** |
| 500 | Optimistic | 1.98 | ₹150.55 | 6.00 | **−5.25** |
| 5,000 | Conservative | 16.04 | −₹11.71 | 15.00 | **−15.59** |
| 5,000 | Base | 18.23 | ₹118.13 | 12.00 | **−6.09** |
| 5,000 | Optimistic | 19.78 | ₹199.15 | 10.00 | **−0.04** |
| 50,000 | Conservative | 160.42 | ₹28.30 | 50.00 | **−35.85** |
| 50,000 | Base | 182.27 | ₹148.14 | 40.00 | **34.07** |
| 50,000 | Optimistic | 197.76 | ₹222.86 | 35.00 | **76.43** |

### Interpretation

**500 sales:** pay for a controlled test and reusable intellectual property, not an expectation of immediate payback.

**5,000 sales:** enough to demonstrate demand, but not automatically enough to fund a broad catalogue and team.

**50,000 sales:** can support attractive economics, but the conservative case shows why scaling a weak offer can destroy capital.

The cases fund different scopes: a two-title pilot, an expanded season, and a larger catalogue. They are not simple multiples of one unchanged operation.

## 11.2 Break-even

\[
\text{Static break-even copies}
=
\frac{\text{Fixed costs}}{\text{Contribution per retained copy}}
\]

The base 5,000-copy cost structure gives approximately **10,158 copies** to cover ₹12 lakh of fixed costs.

The larger base structure, with ₹40 lakh of fixed costs and ₹148.14 contribution, gives approximately **27,001 copies**.

These are **static cost-tier calculations**. Requote printing, staffing and distribution when crossing a scale threshold; do not present either as a guaranteed real-world break-even point.

## 11.3 CAC limits

At the base DTC economics, maintaining **₹100 contribution per book** permits approximately **₹118 CAC per customer/order** at a 1.5-book basket.

That is why I would initially require paid/referral CAC to settle around **₹100–₹120 or lower**, subject to actual costs.

The workbook also allocates fixed social/creative production to DTC. On that basis, the base 5,000-copy **fully loaded marketing CAC is approximately ₹187/customer**, not ₹120.

The fixed creative cost is already in operating profit; do not deduct that fuller KPI a second time.

## 11.4 Working capital

The cash model uses phased print orders, 50% printer advances, delayed trade collections, tax reserves, and full digital-service usage reserves.

| Base project | Modeled funding requirement, including 15% headroom |
|---|---:|
| 500 retained sales | **₹7.15 lakh** |
| 5,000 retained sales | **₹12.71 lakh** |
| 50,000 retained sales | **₹52.09 lakh** |

Profitability does not eliminate cash needs. Printing and content are paid before many sales; trade payments can arrive after stock has moved.

Use preorder/bulk advances where appropriate, short initial trade-credit limits, SKU-level reprints, and strict receivable follow-up. Do not print 50,000 copies upfront to obtain a lower unit price.

## 11.5 Costs that must not disappear into “AI automation”

The pilot budget assumes a lean, reusable 2D production workflow—not a complete bespoke platform with every custom Skill discussed earlier.

A separate **₹10 lakh engineering project**, for example, would reduce the base 50,000-sale profit from approximately ₹34.07 lakh to ₹24.07 lakh before other effects. Budget such work explicitly.

The model also assumes commissioned content with agreed paid-up rights. Royalties, third-party licences, additional staff, borrowing costs, and any obligations not included in those contracts must be added.

---

# 12. Distribution, referrals, and partnerships

## DTC

Lead with the two-book bundle and a strong specimen. Keep standard shipping terms simple and disclose remote-area exceptions before payment.

Begin with prepaid orders. Add COD only after measuring confirmation, return-to-origin, and support costs by location and channel.

India Post’s Gyan Post may offer economical eligible-book delivery, but eligibility and the actual packed weight must be confirmed for this product. It is not a blanket justification for assuming a ₹25 delivery cost everywhere. citeturn874416view2turn686545search8

## Schools and coaching centres

Provide a specimen, syllabus map, sample lesson, and an actual question-solving demonstration.

Offer two clean arrangements: **institutional bulk pricing** or a **disclosed referral arrangement**. Do not combine them automatically.

For independent commercial partners, test a modest commission against actual contribution. Avoid covert sales payments to teachers steering students they assess; obtain necessary institutional approval and respect applicable employment restrictions.

## Bookstores

Start with a small number of relevant outlets and capped opening stock. Agree on discounts, payment dates, returns, damaged-code handling, display copies, and edition expiry in writing.

Measure **sell-through**, not distributor dispatches.

## Amazon and Flipkart

Use marketplaces for convenience and demand capture—not as the only acquisition engine.

Amazon’s fee schedule needs to be calculated using the actual price, category, fulfillment route, packed weight and returns. Flipkart should be similarly costed using the actual seller-account quotation. citeturn886284view2

Do not assume the same all-in fee for single books and multi-book bundles.

## Student referrals

A proposed pilot is a small buyer discount and a capped referrer credit after the refund window.

Accounting must remain clean:

**Buyer discount → lower realized selling price.**

**Referrer reward → marketing cost/liability.**

Do not count either twice. Avoid rewards tied to fabricated reviews or pressure to expose classmates’ contact details.

---

# 13. Lean automation and operating system

## Recommended initial stack

| Function | Initial implementation |
|---|---|
| Store, product pages, orders | WooCommerce on managed hosting |
| Payments | Razorpay |
| Accounts and entitlements | One account system plus a small, tested activation extension |
| Free lessons | YouTube, embedded where appropriate |
| Paid videos | Private hosted delivery with signed playback |
| Fulfillment | Courier/aggregator workflow, initially supervised; automate after validation |
| Social publishing | Native scheduling and approved publishing tools |
| Accounting | Suitable accounting software with accountant-reviewed tax treatment |
| Analytics | Aggregated funnel data and legally approved first-party records |
| Support | Help pages, ticket inbox, permissioned WhatsApp support |

WooCommerce provides an open-source commerce foundation, but hosting, extensions, development and maintenance are not costless. citeturn973282view0

### Automate repetitive work—not academic approval

A suitable content workflow is:

```text
Approved chapter and question IDs
        ↓
Long-form explanation
        ↓
Select one useful misconception/question
        ↓
Re-layout into vertical composition
        ↓
Generate caption and one matching CTA
        ↓
Scientific + editorial approval
        ↓
Schedule publication
        ↓
Aggregate performance by topic and destination
```

Keep humans responsible for scientific accuracy, syllabus fit, disputed answers, misleading claims, sensitive support cases, refund exceptions, and large stock commitments.

Do not crop a horizontal animation into a Reel if it removes axes, conditions, units, or necessary context.

---

# 14. Ninety-day launch roadmap and budget

Starting on the research date, a 90-day window reaches approximately **11 January 2027**. That makes a broad rushed catalogue particularly risky. The roadmap below does not assume an unverified 2027 exam timetable.

## Budget for the two-title pilot

| Fixed project allocation | Budget |
|---|---:|
| Manuscripts and independent academic review | ₹1,60,000 |
| Editing, pagination, design and proofs | ₹60,000 |
| Reviewed chapter videos | ₹1,20,000 |
| Reels, free-content packaging and community work | ₹50,000 |
| Commerce and activation development | ₹60,000 |
| Fixed hosting, tools and storage | ₹15,000 |
| Allocated founder/operational workload | ₹1,15,000 |
| Legal, tax, accounts and rights administration | ₹25,000 |
| Partner specimens, visits and travel | ₹30,000 |
| QA/project contingency | ₹15,000 |
| **Fixed pilot budget** | **₹6,50,000** |

Printing and other variable costs are additional, with sales receipts incorporated in the cash model. The labor allocation is for a defined project workload—not an unlimited full-time team.

**Suggested available capital ceiling: ₹8 lakh**, released in stages. Begin with only **₹60,000 for discovery and prototypes**.

## Week-by-week execution

| Week | Priority | Gate |
|---|---|---|
| 1 | Interview students, parents, teachers and shops; collect competing books | Confirm real pain points and medium |
| 2 | Test two lessons, sample pages and price cards; obtain three print quotes | Do not confuse survey enthusiasm with demand |
| 3 | Lock two titles, syllabus map and content extent | Academic team can complete the promised product |
| 4 | Establish reusable visuals; begin four or five Reels/week | Measure qualified visits and attempts |
| 5 | Build checkout, accounts, redemption and refund flow | Payment and entitlement tests pass |
| 6 | Complete six free chapters; test low-cost phones and partner specimens | Usability and academic review pass |
| 7 | Review print proofs and full solutions; finalize access/tax terms | Credible delivery commitments |
| 8 | Complete the paid catalogue promised at launch | No undisclosed major missing chapters |
| 9 | Authorize first short print batch; test urban/rural dispatch | Actual weight, price and delivery evidence |
| 10 | Fulfill pilot purchases and repair activation friction | No unresolved critical content/access issue |
| 11 | Test referrals and digital-only versus bundle paths | Positive contribution by acquisition cohort |
| 12 | Reconcile sales, returns, stock and receivables | Reprint justified by actual demand |
| 13 | Decide to continue, change the offer, or stop | Expansion follows evidence—not sunk costs |

The complete workbook assigns owners and deliverables to each week.

---

# 15. Growth metrics, experiments, and expansion gates

## 15.1 Proposed operating targets

These are **management targets to test**, not industry benchmarks.

| Metric | Initial target or rule |
|---|---|
| Qualified free learner → paid order | Test a **3–8%** range |
| Incremental DTC CAC | Approximately **₹100–₹120 or below** at confirmed base economics |
| Valid first-attempt activation | **At least 97%** |
| DTC activation by day seven | Test **60–75% of delivered eligible books** |
| Inventory sell-through | Plan around **90%**, stress at 75% |
| Academic release defects | **Zero unresolved critical errors** |
| Stock decisions | By SKU and lead time, not aggregate follower count |
| Learning success | Independent and delayed performance—not video completion alone |

For bookstore sales, activation divided by copies shipped to the retailer is not a valid student-activation rate. First establish retailer sell-through.

## 15.2 Highest-priority experiments

Test **selected versus sequential free-chapter curation**, **one-book versus two-book presentation**, **digital-only availability**, and **product-proof versus generic motivational marketing**.

For Reels, compare a prediction-first opening with a worked-example opening using comparable topics and destinations.

Define the primary outcome before running each test. Measure retained sales and contribution, not only clicks. Do not announce a winner after two purchases or one unusually viral post.

## 15.3 Failure modes and response

| Failure | Response |
|---|---|
| Viral views, few relevant visits | Narrow board/class/topic cues; change distribution, not merely editing speed |
| Free lessons used but no purchase | Review product value, price and practice needs; do not punish free learners |
| Paid acquisition exceeds contribution | Stop scaling; improve basket, channel mix, offer or costs |
| High print inventory | Shorter reprints, fewer SKUs, paid demand and capped trade stock |
| Weak teacher adoption | Audit scientific quality and local fit before offering a larger commission |
| Code sharing | Secure issuance and redemption, reasonable device controls, easy legitimate recovery |
| Students prefer free YouTube | Make the paid practice/solution system meaningfully better organized and dependable |
| Missing chapters or repeated errors | Pause promotion and repair the product |
| Seasonality | Maintain cash reserves; develop reusable guides/question banks only after core validation |
| Attractive accounting profit, cash shortage | Shorten collections, phase printing, reserve tax and future service obligations |

## 15.4 Expansion sequence

**First:** one cohort, one print medium, two excellent titles.

**Then:** dependable Assam distribution and Class 12 subjects introduced individually.

**Next:** guides and question banks that reuse the verified source and solution library.

**Later:** AI answer evaluation as a separately validated service with rubric-specific testing, protected child data, uncertainty handling, capped usage, and human escalation.

A new board requires new syllabus and assessment alignment. Translating the cover and reusing the same paper set is not a credible expansion strategy.

---

## Final recommendation

**Proceed with ExamLeaf—but launch it as a disciplined publishing and practice business, not as a bet on virality.**

The immediate investment should create **two trustworthy products, a frictionless free demonstration, reliable fulfillment and activation, and a measured route to repeatable contribution**.

The biggest unresolved commercial inputs are actual per-SKU printer quotes, courier/account charges, language demand, partner sell-through, and observed customer acquisition costs. Those should be resolved before large inventory commitments—not hidden behind optimistic assumptions.

**The best evidence that ExamLeaf deserves to grow will be students solving better, partners reordering, customers recommending it voluntarily, and each additional order contributing enough to sustain the next edition.**

A monthly syllabus, competitor-price, and service-tariff alert would help keep the operating model current.


=====================================================================
MESSAGE id=849b2e48-c4f8-4085-b5d6-c7be7844e63e role=user content_type=text create_time=1791897175.113 chars=6016
=====================================================================

# ExamLeaf — Human-Like Teaching, Storytelling, Humour & Student Psychology

Conduct an **in-depth research and creative analysis** to develop the ultimate teaching, narration, and scriptwriting framework for ExamLeaf's 10-minute educational videos, targeting Class 10–12 students.

Our goal is to create videos that feel like **an extraordinarily talented, energetic, funny, friendly, and inspiring teacher is personally teaching the student**—not an AI reading a textbook or a robotic educational lecture.

The teaching should be so simple, relatable, interactive, and enjoyable that even students with very weak fundamentals can understand difficult concepts, experience genuine progress, and gradually become confident problem-solvers.

### Research and Develop

1. **Natural Human-Like Teaching:** Design conversational scripts with spontaneous-sounding expressions, personality, curiosity, excitement, humour, natural pauses, rhetorical questions, and emotional variation. Avoid textbook language, artificial enthusiasm, predictable AI phrases, and monotonous explanations.
2. **Teaching Psychology:** Research the most effective methods for explaining complicated concepts in extremely simple language, using analogies, scaffolding, storytelling, everyday experiences, active recall, worked examples, and gradual difficulty progression. Make students feel capable without being patronizing.
3. **Dora-Style Interactive Teaching:** Take inspiration from Dora the Explorer's question-and-response approach, adapted appropriately for teenagers. Frequently involve students through easy questions, predictions, pauses, mini-challenges, writing formulas, drawing diagrams, and celebrating genuine understanding. Determine how often to interact without disrupting lesson flow.
4. **Humour, Memes & Relatability:** Explore natural comedy, witty observations, relatable school situations, Indian student experiences, exam-related jokes, culturally relevant memes, light sarcasm, funny comparisons, short stories, and occasional Hindi/Assamese shayari or expressions where appropriate. Humour should reinforce concepts rather than distract from them. Avoid forced jokes, cringe dialogue, outdated memes, or insulting students.
5. **Emotional Connection & Confidence:** Research how exceptional teachers build trust, reduce academic anxiety, encourage struggling learners, create satisfying "Aha!" moments, and make students feel proud of their progress. Use warmth, encouragement, achievable wins, and positive reinforcement without fake promises or exaggerated praise.
6. **Voice Acting & Delivery:** Define the ideal narration personality, speaking speed, pitch variation, excitement, comedic timing, suspense, pauses, emphasis, storytelling tone, and confidence-building expressions. Provide directions suitable for AI voice synthesis so the final narration feels authentically human.
7. **Stories & Real-Life Examples:** Develop memorable storytelling techniques, analogies, humorous situations, and visual explanations that turn abstract Physics, Chemistry, Mathematics, and Biology concepts into relatable experiences. Balance entertainment with scientific accuracy and examination relevance.
8. **Attention & Engagement:** Investigate how to keep students emotionally and intellectually engaged throughout a 10-minute lesson using curiosity, anticipation, changing vocal energy, interactive questions, surprising explanations, visual reveals, and well-timed humour—without excessive stimulation or cognitive overload.
9. **Language & Personality:** Recommend the best language style for Indian students, including simple English, natural conversational expressions, and selective Hinglish or Assamese cultural references where appropriate. Develop a distinctive, consistent **ExamLeaf Super Teacher Personality** that feels intelligent, approachable, funny, energetic, trustworthy, and genuinely invested in student success.
10. **Complete Scriptwriting Framework:** Build reusable instructions and Claude Skills for generating human-sounding scripts, dialogues, jokes, analogies, interactive moments, emotional cues, narration directions, animations, and subject-specific explanations automatically, while preventing repetitive or generic AI-generated writing.

### Required Deliverables

- A complete **ExamLeaf Super Teacher Personality & Scriptwriting Guide**.
- Evidence-based psychological principles for humour, confidence, engagement, and effective teaching.
- Subject-specific storytelling, analogies, interactions, and humour examples.
- A practical structure for an engaging 10-minute educational video.
- Sample dialogues comparing boring textbook narration with exceptional human-like teaching.
- Voice direction tags, pauses, emotional cues, and animation synchronization instructions.
- Reusable prompts and Claude Skills for generating consistently outstanding educational scripts.
- A complete sample script demonstrating the proposed teaching style.

**Important:** The videos must never feel like forced comedy, motivational speeches, artificial AI conversations, or childish cartoons. They should feel like a **brilliant, charismatic teacher who knows exactly how to make difficult topics easy, interesting, memorable, and enjoyable.**

Take inspiration from the interactivity of Dora, the conceptual clarity of Professor Dave Explains, the simplicity of Khan Academy, and the natural humour and storytelling of exceptional Indian teachers—while developing an original ExamLeaf identity.

**Ultimate Goal:** Students should finish each video thinking:

*"Wait… that was actually so easy! Why did this seem difficult before? I understood it, I can solve the questions, and I actually want to learn the next topic!"*

Don't just recommend techniques. **Research the psychology, explain why they work, demonstrate exactly how to use them in scripts, and develop a repeatable teaching system that creates genuine understanding, emotional connection, student confidence, and long-term learning.**


=====================================================================
MESSAGE id=39025c35-4a43-4dc4-85f4-593245adb65e role=assistant content_type=text create_time=1791898177.263539 chars=203
=====================================================================

The chemistry sample and 14 draft Skills are complete, with structural checks passing for pauses, answer reveals, timing, and narration cues. Academic review, voice rendering, and student testing remain.


=====================================================================
MESSAGE id=a4673c7a-882a-4ee9-a8a5-d8fda56e2d2f role=assistant content_type=text create_time=1791898895.56802 chars=48077
=====================================================================

# ExamLeaf Super Teacher  
## A research-based personality, narration, and scriptwriting framework

**ExamLeaf’s ideal teacher should be warm toward the student, exacting about the science, and playful about the problem.**

The teacher’s defining quality should not be “says funny things.” It should be:

> **“This teacher notices exactly where I might get confused, explains the missing step, and gives me a fair chance to work it out.”**

That is the identity I recommend building.

Borrow the **invitation to participate** from Dora, the **conceptual focus** you value in Professor Dave, and the **transparent working** you value in Khan Academy. Develop original language, examples, visual conventions, and delivery—not an imitation of anyone’s voice or recurring dialogue.

The central teaching pattern should be:

> **Make the problem approachable → reveal the relationship → demonstrate the reasoning → hand over part of the work → check an independent attempt.**

Humour, stories, and voice acting should strengthen that progression, not compete with it.

### Ready-to-use materials

[**Download the complete Super Teacher starter pack**](sandbox:/mnt/data/ExamLeaf_Super_Teacher_Starter_Pack.zip)

[**Read the personality and production guide**](sandbox:/mnt/data/ExamLeaf_Super_Teacher/Super_Teacher_Guide.md)

[**Read the complete sample lesson script**](sandbox:/mnt/data/ExamLeaf_Super_Teacher/examples/Complete_Sample_Script.md)

The pack contains **ten custom Skill drafts, reusable prompts, an evidence ledger, a structured lesson file, and a script checker**. The checker passed **12 local structural tests**. The Skills have not been evaluated through Claude/Codex runs, and the sample has not been voiced, rendered, or tested with students.

---

# 1. What the research actually supports

## 1.1 Conversational teaching can help—but informality alone is not the mechanism

In three multimedia-learning experiments, conversational wording improved students’ ability to **apply what they learned**, but did not improve retention of the presented material. That supports a conversational approach; it does not establish that adding slang, “bro,” filler words, or constant jokes improves learning. citeturn783960search11

The practical distinction is:

**Textbook narration:**

> “The coefficient is a numerical factor multiplying the entire chemical formula.”

**Teacher narration:**

> “That two belongs to the whole formula. It gives us two complete water molecules—not a different kind of molecule.”

The second version explains what the learner should notice and how to interpret it.

**Recommendation:** make narration conversational through **useful guidance**, not decorative informality.

## 1.2 Humour can improve the experience without improving achievement

A 2026 study used experimentally varied video lessons with **206 expert raters and 325 students**. Course-related humour improved several perceptions and experiences, including rapport, interestingness, motivation, and enjoyment. Aggressive humour produced less favourable emotional responses. These results do **not** demonstrate better delayed retention or examination performance. citeturn783960search16

A broader review likewise describes a mixed achievement literature. Students enjoying a teacher, remembering a joke, and learning the scientific principle are different outcomes. citeturn783960search20

**Recommendation:** use humour as a supporting instructional tool. Its presence is not evidence that the lesson works.

## 1.3 Scaffolding is more important than charisma

Research supports transitioning from worked examples toward independent problems by gradually removing support. However, success on substantially different problems is not automatic. Asking students to explain the underlying principle can strengthen that transition. citeturn439792search8

This means the teacher should progressively change roles:

> **“Watch how I choose the step.”**  
> **“You choose the next step.”**  
> **“Now choose the method without my help.”**

A highly entertaining explanation that never reaches the third stage is incomplete as a problem-solving lesson.

## 1.4 Questions should cause thinking, not merely create the appearance of interaction

Self-explanation research supports prompts that ask learners to explain relationships and reasoning. Retrieval-practice research supports asking students to recall or apply information rather than relying exclusively on repeated exposure. Neither establishes an ideal fixed number of questions per video. citeturn955193view4turn955193view5

Prefer:

> “Why did that coefficient change both atom counts?”

over:

> “Understood? Great!”

The first produces a meaningful mental task. The second tells you almost nothing.

## 1.5 Feeling that a lesson was easy is not the same as learning

In a university Physics experiment, students in active-learning conditions learned more while reporting a lower feeling of learning than students experiencing passive instruction. The study does not mean difficulty is always productive; it shows why fluency and confidence alone are unreliable success measures. citeturn661037view0

Therefore, slightly refine your desired student reaction:

> **“That finally makes sense—and I can show that it makes sense by solving the next question.”**

The second half matters.

## 1.6 Neuroscience does not supply a “charisma formula”

Curiosity research has linked high-curiosity states with memory benefits and activity involving reward-related regions and the hippocampus. But the relevant experiments do not prescribe a dopamine-triggering joke, colour, sound, or cliffhanger schedule. citeturn144471search6

Similarly, fixed claims about everyone losing attention after a specific number of seconds or minutes are not sound production rules. citeturn870523search4

**Use the research to design meaningful thinking—not to decorate production decisions with brain terminology.**

---

# 2. The ExamLeaf Super Teacher personality

## The personality in one paragraph

> **A brilliant, friendly teacher who speaks plainly, enjoys the subject, anticipates mistakes, occasionally finds something amusing in the problem, and respects the student enough to ask them to think. The teacher is patient without being slow, confident without pretending certainty, and encouraging without manufacturing success.**

“Super Teacher” is a useful internal design label. The narrator does not need to announce it.

### Personality standards

| Quality | What students should experience | What to avoid |
|---|---|---|
| **Intelligent** | “Now I see why that step was chosen.” | Unexplained cleverness or jargon |
| **Warm** | “Getting this wrong gives me a way forward.” | Fake intimacy or exaggerated reassurance |
| **Energetic** | Important moments feel alive | Every sentence delivered like a trailer |
| **Funny** | A quick observation makes the idea memorable | A joke quota or compulsory meme |
| **Trustworthy** | Conditions and limitations are explained | Concealing exceptions to keep the story simple |
| **Interactive** | Students get genuine opportunities to answer | Pretending prerecorded narration heard them |
| **Exam-aware** | Understanding returns to correct notation and answers | Replacing reasoning with unqualified “tricks” |

### The most important behavioural rule

**The teacher should reveal their instructional decisions.**

Not private thought or a rambling monologue—just the decisions a learner needs:

> “We know the voltage and resistance. Current is the unknown, so use this form.”

> “Let’s keep the diagram still while we check the direction.”

> “That answer could be right, but the units will tell us whether our substitution makes sense.”

This is more convincingly human than adding “umm,” laughter, or deliberately imperfect grammar.

### Expressions that earn their place

Useful expressions include:

> “Keep that part fixed.”

> “Here is the step to watch.”

> “That would solve a different question.”

> “The diagram gives us a starting point.”

> “Before calculating, predict whether the answer should increase or decrease.”

> “Your first step is useful. The repair starts here.”

Do not repeat them mechanically. Their **function** should recur; their exact wording need not.

### Expressions to retire

Avoid using these as default script furniture:

> “Let’s dive into the fascinating world of…”

> “Prepare to have your mind blown!”

> “This is super easy!”

> “Boom! You have mastered the chapter!”

> “Even a child can understand this.”

The problem is not that a phrase can never appear. It is that it often substitutes for an actual teaching move.

---

# 3. How to make difficult concepts genuinely simpler

## 3.1 Simplify the entry point, not the truth

The recommended explanation ladder is:

| Stage | Teacher’s task | Example |
|---|---|---|
| Familiar observation | Give the learner something interpretable | “We have two copies of this molecule.” |
| Visual relationship | Show what changes and what remains fixed | Duplicate the complete molecule |
| Plain-language explanation | Explain the relationship without unnecessary terminology | “Every atom count doubles.” |
| Formal language | Introduce the required term | “That number is the coefficient.” |
| Worked reasoning | Explain why a step is chosen | “Oxygen does not match, so start there.” |
| Reduced support | Let the learner complete a step | “Now recount hydrogen.” |
| Independent application | Remove the worked method | “Balance this new equation.” |
| Verification | Teach how to check | “Count every element on both sides.” |

This proposed structure implements the broader multimedia goal of helping learners select relevant information, organize it, and connect it with existing knowledge. citeturn144471search15

## 3.2 Weak fundamentals require a repair route

A ten-minute video cannot responsibly promise to replace every missing prerequisite of a whole chapter.

For each lesson, identify the **one or two prerequisites most likely to block understanding**.

For example, before balancing equations:

> “Does \(2H_2O\) mean two water molecules, or one molecule with a changed formula?”

A short repair can follow. More substantial gaps should lead to a separate foundation lesson.

Do not call that route “for weak students.” Use:

> **“Need the symbol-reading version? Start here.”**

Students with strong fundamentals should also have a clear route past material they already know.

## 3.3 Use the smallest helpful analogy

An analogy should have a written contract:

**What corresponds → what does not correspond → where the explanation returns to science.**

This is consistent with established teaching-with-analogies approaches that explicitly consider mapping and limitations. citeturn755614search3

For chemical coefficients:

> “Ordering three sandwiches multiplies every ingredient in the recipe. It does not change what one sandwich contains.”

Useful mapping:

- Number of recipe copies ↔ coefficient.
- Contents of each molecular copy ↔ subscripts.

Boundary:

> “This helps us read the numbers. It does not explain reaction conditions or how bonds rearrange.”

**Reject an analogy when it needs more explanation than the concept itself.**

## 3.4 Make the “Aha!” testable

A proposed three-step pattern is:

> **Tempting interpretation → revealing contrast → fresh prediction.**

Example:

> “These equations both conserve atoms. Why is only one the requested smallest whole-number form?”

The reveal creates clarity. The fresh prediction establishes whether the learner can use it.

Do not stop at:

> “See? Amazing, right?”

---

# 4. Dora-inspired interaction, redesigned for teenagers

## 4.1 Borrow the structure, not the performance

The useful idea is **inviting a response and leaving space for it**.

Do not borrow a preschool vocal register, repetitive celebration, or pretend listening. Research involving preschoolers and prerecorded questions cannot establish the best interaction frequency for adolescents. citeturn755614search11

### The ExamLeaf interaction loop

> **Ask something specific → allow an attempt → explain the answer → identify a repair → ask a related question.**

Example:

> **Teacher:** “Each water molecule has two hydrogen atoms. How many hydrogen atoms are in two water molecules?”  
> **[Six seconds of silence; answer hidden.]**  
> **Teacher:** “Four. If you wrote two, you counted the molecules. Now multiply by the hydrogen atoms inside each one.”

That is respectful, purposeful, and achievable.

## 4.2 Starting interaction schedule

For initial ten-minute pilots, try:

- **Three or four brief predictions or mental checks.**
- **Two or three substantial pauses for writing, drawing, or solving.**

This often places an invitation to think approximately every **75–120 seconds**, but these are **production hypotheses**, not a scientific attention-reset interval.

Put interactions at conceptual boundaries, not wherever the stopwatch demands one.

### Match the pause to the work

| Task | Proposed treatment |
|---|---|
| Choose between two simple outcomes | Approximately 4–8 seconds |
| Explain one recently demonstrated relationship | Brief thinking time, with optional pause |
| Write a definition from memory | Learner-controlled pause |
| Draw and label a diagram | Learner-controlled pause |
| Multi-step calculation | Learner-controlled pause |
| Copy a compact reference | Stop new narration while students record it |

A ten-second hold is not enough for every learner to solve a multi-step problem. Say:

> “Pause here and give yourself the time you need. Resume when you have an answer to check.”

## 4.3 Never fabricate the student’s response

Avoid:

> “Yes! I heard you say four!”

> “You got it right again!”

Use:

> “Four is the count we need.”

> “If your answer matches, check whether your reasoning matches too.”

> “If you chose the other direction, look at this arrow.”

Actual adaptive responses should be used only when the platform has received the relevant input.

## 4.4 Let questions vary in intellectual purpose

Not every interaction should be “calculate this.”

Alternate between:

**Predict → identify → explain → reconstruct → draw → solve → verify.**

For example:

> “Which quantity must stay fixed?”

> “What would make this statement false?”

> “Write the formula without looking.”

> “Sketch the direction before we animate it.”

> “Find the first incorrect step—not just the final wrong answer.”

---

# 5. Humour, memes, stories, and cultural relevance

## 5.1 Use humour inside the explanation

The safest recurring forms are:

| Humour type | Original example | Teaching purpose |
|---|---|---|
| **A tempting shortcut exposed** | “Very efficient way to solve a different question.” | Shows why changing a chemical formula is not balancing |
| **A harmless observation** | “Bigger numbers do not earn bonus marks for looking busy.” | Distinguishes balanced from simplest coefficients |
| **Relatable exam friction** | “The formula is correct. The minus sign has other plans.” | Leads immediately to checking the sign convention |
| **Light diagram reassurance** | “Circles and labels are enough; this is not an art competition.” | Keeps attention on relationships rather than drawing perfection |
| **Brief personification** | “The inside function is not on leave.” | Reminds students to include the inner derivative |

These are creative examples, not experimentally validated lines.

The joke should end where the explanation resumes.

## 5.2 Set a ceiling, not a quota

For the first pilots, use **up to three to five short light moments**, generally consuming **less than about 25 seconds in total**.

Zero jokes is acceptable when the topic or delivery does not need them.

These limits are editorial starting points. Research does not identify an optimal number of jokes in a ten-minute STEM lesson.

Interesting but irrelevant additions can hinder learning. That is a reason to remove distracting comedy—not to remove attractive design or all personality. citeturn870523search3

## 5.3 Apply the “concept survives” test

For every joke, ask:

> **Will the student remember the scientific relationship, or only the punchline?**

Then ask:

> **Does the joke imply something scientifically false?**

For example, “electrons are lazy” may be memorable but can introduce an unhelpful intention-based explanation. Prefer an accurate statement about the relevant model.

The same applies to enzymes “wanting” substrates, molecules “deciding,” or evolution “planning ahead.” Personification should never become the causal explanation.

## 5.4 Use memes sparingly—and usually make your own visual gag

A durable split-screen comparison is often better than a recognisable celebrity reaction clip.

Example:

**Left:** “Changing the coefficient.”  
**Right:** “Accidentally changing the substance.”

Use your own molecule graphics. The humour follows from the contrast.

Do not force current slang or copyrighted reaction clips into an otherwise clear lesson. Cultural freshness is not worth confusing the concept or creating unnecessary licensing work.

## 5.5 Hindi and Assamese should be optional, audience-led choices

Do not assume Hindi is universally comfortable for an Assam audience.

Choose among:

**Simple English**, **Assamese-supported explanation**, or **a Hinglish edition**, according to the learners and their examination medium.

Research on multilingual teaching in India provides useful contextual examples, but does not establish an ideal percentage of code-switching for STEM videos. One relevant study examined eight secondary English teachers—not a randomized test of Hinglish science instruction. citeturn290870search0

### Original optional language examples

A brief Hindi mnemonic:

> **“Naam wahi, ginti nayi; har atom ka hisaab sahi.”**

Intended meaning:

> “Keep the specified substances; change their counts; account for every atom.”

Follow it with the formal coefficient rule. Do not make the rhyme the only explanation.

An Assamese prompt, **drafted for native-speaker review**:

> **“এতিয়া নিজে চেষ্টা কৰি চোৱা।”**  
> “Now try it yourself.”

Use a native language editor for nuance, pronunciation, and age appropriateness. Do not scatter regional expressions through a script merely to signal local identity.

---

# 6. Building warmth, trust, and genuine confidence

## 6.1 Give feedback that contains useful information

A large feedback meta-analysis found substantial variation between implementations. “Feedback works” should not be interpreted as “any praise improves learning.” citeturn661037view2

Recommended feedback structure:

> **What was correct → what needs attention → what to do next.**

Examples:

| Situation | Proposed narration |
|---|---|
| Correct relationship, wrong arithmetic | “Your relationship is correct. Recheck the substitution rather than restarting.” |
| Correct answer, uncertain learner | “Your atom counts match on both sides. That is the check that supports your answer.” |
| Incorrect concept | “The important distinction is molecules versus atoms. Let’s separate those counts.” |
| Incomplete attempt | “You have a useful starting point. Match nitrogen first, then recount hydrogen.” |
| Correct independent solution | “You selected the coefficients without the worked example. Now test the method on a different equation.” |

## 6.2 Do not insult students through reassurance

“This is easy” can make an unsuccessful learner wonder why they are still struggling.

Prefer:

> “There are two counts to keep separate.”

> “The notation makes this look more complicated than the counting actually is.”

> “Let’s make the first step visible.”

Similarly, avoid praising an unseen learner’s intelligence. Praise a demonstrated action conditionally.

## 6.3 Confidence should follow evidence

Use three checkpoints:

**I followed it.**  
**I completed a step with support.**  
**I solved a related problem without support.**

These should not be collapsed into one “mastered” badge.

After the lesson, ask students to identify the part they can do independently. A remaining difficulty should produce a specific next action—not a motivational speech.

## 6.4 The narrator can be personable without pretending to be a human teacher

Do not invent personal memories such as:

> “When I taught this in my classroom last year…”

unless a real teacher supplied and authorized that account.

Likewise, do not fabricate degrees, teaching experience, or emotional knowledge of the student.

A transparent description such as **“AI-narrated, academically reviewed”** is compatible with excellent teaching. The quality should come from the instruction, not from concealing the production process.

---

# 7. Subject-specific storytelling and explanation examples

The following are original examples. Their scientific foundations should remain fixed when adapting the wording.

## Physics: current is a rate, not a speed

**Opening:**

> “Imagine counting people passing through a doorway. Twenty people in a minute tells you a flow rate. It does not tell you how fast each person walked.”

**Return to physics:**

> “Current tells us how much charge crosses a section per unit time. Drift velocity describes the average motion of the charge carriers. Those quantities are related, but they are not the same thing.”

**Interaction:**

> “Could more charge cross each second without every carrier moving faster? What else could change?”

**Boundary:** the doorway analogy is about counting flow. It does not explain electrical signal propagation or all details of electron motion. citeturn809499view3

**Visual:** a stationary cross-section, a charge-count counter, and a separately labelled carrier velocity. Do not use one animation speed to stand for both current and signal speed.

## Chemistry: coefficients change quantity, not identity

**Opening:**

> “Changing water into hydrogen peroxide would make the atom count look convenient. Unfortunately, we were asked to balance the water equation—not replace the product.”

**Analogy:** multiple copies of a recipe.

**Interaction:**

> “How many hydrogen atoms are in three water molecules?”

**Return to science:** hold the supplied formulas fixed, adjust coefficients, and verify the atom count of every element. citeturn809499view0

## Mathematics: chain rule as two connected changes

Use:

\[
y=(3x+1)^2
\]

**Narration:**

> “There are two operations here. First, multiply by three and add one. Then square the result. When \(x\) changes, both layers matter.”

> “Differentiate the outside, then account for how the inside changes. The inside function is not on leave.”

\[
\frac{dy}{dx}=2(3x+1)\times3=6(3x+1)
\]

**Interaction:**

> “Change the inside to \(5x+1\). Which factor in the derivative must change?”

**Boundary:** the boxes represent function composition. They are not an alternative proof of the chain rule. citeturn809499view2

## Biology: enzymes change the barrier, not the destination

**Opening:**

> “Two routes connect the same starting point and destination. One requires a bigger climb.”

**Scientific explanation:**

> “An enzyme provides a pathway with a lower activation-energy barrier. It does not change the overall free-energy difference between the starting and ending states.”

**Light line:**

> “A shortcut—not teleportation.”

**Interaction:**

> “On the energy diagram, which should change: the barrier, the endpoints, or all three?”

**Boundary:** the hill is an energy representation, not a literal route travelled through a cell. For binding, avoid treating a rigid lock-and-key picture as the complete model; induced fit matters. citeturn809499view1

---

# 8. Before-and-after narration examples

| Weak narration | Proposed ExamLeaf version |
|---|---|
| “The learner must observe that the coefficient multiplies the molecular formula.” | “That two gives us two complete molecules. Count everything inside each copy.” |
| “Now apply the chain rule.” | “The outside is a square. The inside is \(3x+1\). Differentiate both layers, then multiply their factors.” |
| “Enzymes catalyse reactions by reducing activation energy.” | “Keep the starting and ending energy levels fixed. Now lower the barrier between them. That is the change we want to explain.” |
| “This is a very easy numerical.” | “We have the two quantities needed. Let’s identify the unknown before substituting.” |
| “Excellent! You all answered correctly!” | “If your result matches, check the unit and the reasoning. A matching number alone is not the whole check.” |
| “Let us embark upon the fascinating journey of chemical balancing.” | “This equation has an oxygen problem. Can we fix it without changing what the substances are?” |

The formal terminology still appears. It is introduced at the point where students have something meaningful to connect it to.

---

# 9. Voice acting and AI narration directions

## 9.1 Choose a teacher voice, not a promotional voice

The initial voice brief should be:

> **Clear adult voice; conversational authority; moderate warmth; restrained amusement; audible interest; patient correction; no theatrical shouting or constant upward inflection.**

Do not assume one gender, accent, or pitch is best for learning.

A modern TTS comparison found no statistically significant human-versus-synthetic difference under its particular conditions. That does not establish universal equivalence, but it does caution against rejecting modern synthesis based solely on older machine-voice findings. citeturn762447view5

Enthusiasm also needs restraint. In a study of 244 university participants, varying synthetic voice enthusiasm affected some emotional or cognitive-load measures but did not improve immediate retention or transfer. citeturn955193view0

## 9.2 Five delivery modes are sufficient

| Editorial mode | Delivery | Best use |
|---|---|---|
| **CURIOUS** | A real question, modest anticipation | Opening, prediction |
| **STEADY** | Clear, ordinary explanation | Most teaching |
| **DELIBERATE** | Slower, stronger contrast | Conditions, units, misconceptions |
| **LIGHT** | Slightly amused; no laugh required | A brief relevant observation |
| **REASSURING** | Matter-of-fact, constructive | Feedback and repair |

The voice should move between these modes because the **teaching task changes**, not because every scene needs a new emotion.

## 9.3 Starting pacing targets

These are **production targets to audition**, not established universal optima.

| Passage | Initial target |
|---|---|
| Ordinary English explanation | Approximately **130–155 active words/minute** |
| Dense notation or an unfamiliar relationship | Approximately **105–125**, with inspection time |
| Familiar recap | Can be somewhat faster |
| Important distinction | Approximately **1–2 seconds** of processing space |
| Simple prediction | Approximately **4–8 seconds**, answer hidden |
| Writing or solving | Learner-controlled pause |

A natural ten-minute lesson may contain roughly **1,100–1,250 narration words**, depending on its pauses and visual demands. Do not accelerate the science simply to meet a word budget.

## 9.4 Separate editorial cues from TTS syntax

Use internal cues such as:

```text
[CURIOUS]
[DELIBERATE]
[LIGHT]
[BEAT:0.35]
[THINK:6]
[PAUSE_VIDEO]
[REVEAL:oxygen_count]
```

These are **ExamLeaf metadata**, not a universal voice-engine language.

Current ElevenLabs documentation states that **Eleven v4 and v3 do not support SSML break tags**. Their audio tags and punctuation can influence delivery, but exact thinking time should be controlled in the video timeline. Google’s SSML controls must likewise be checked against the selected model and voice. citeturn771459view2turn762447view3

### Example production record

```yaml
scene_id: coefficient_check
voice_mode: curious

spoken_before:
  "Together, how many hydrogen atoms?
   And how many oxygen atoms?"

student_task:
  type: prediction
  answer_hidden: true
  timeline_hold_seconds: 6

spoken_after:
  "Four hydrogen; two oxygen.
   The coefficient multiplies the whole formula."

visual_events:
  - Show two intact water molecules.
  - Keep element labels visible.
  - Do not reveal totals during the attempt.
  - Reveal hydrogen count with "Four hydrogen".
  - Reveal oxygen count with "two oxygen".
```

Generate the voice, measure the waveform, align meaningful events, then conform the scene.

Keep equations in a **display-text field** and their pronunciation in a **spoken-text field**. Provide accurate captions without allowing them to reveal an answer before the attempt. Captioning is an accessibility requirement, not an optional casualty of a cleaner layout. citeturn290870view1

---

# 10. The reusable ten-minute structure

This is a flexible pattern, not a compulsory timetable.

| Approximate section | Purpose |
|---|---|
| **0:00–0:30** | A concrete question or tempting misconception |
| **0:30–1:30** | Essential prerequisites and readable representation |
| **1:30–3:00** | Core relationship, with a brief analogy only when useful |
| **3:00–4:45** | Worked example with reasoning made visible |
| **4:45–6:15** | Guided completion and targeted feedback |
| **6:15–7:45** | Independent attempt and explanation |
| **7:45–9:15** | Misconception check, retrieval, exam-language conversion |
| **9:15–10:00** | Capability check and one delayed-practice action |

Keep the question, important givens, and relevant diagram visible while students use them.

Use movement for a changing relationship. Use stillness for inspection, writing, or calculation. The charisma should not disappear when the animation stops.

---

# 11. A repeatable Claude/Codex authoring system

## 11.1 Existing resources versus custom work

The verified existing foundations are **Claude Code Skills**, the **Agent Skills standard**, Codex’s Skill support, and Anthropic’s **skill-creator** evaluation workflow. These provide packaging and development conventions; they do not provide a proven ExamLeaf teaching personality. citeturn771459view3turn290870view0turn762447view1turn809499view4

The starter pack contains these **ten original custom Skill drafts**:

| Skill | Responsibility | Required output |
|---|---|---|
| `examleaf-lesson-architect` | Scope, prerequisites, objectives, teaching progression | Lesson plan and independent target task |
| `examleaf-conversational-script` | Natural narration without losing scientific meaning | Clean spoken draft |
| `examleaf-analogy-auditor` | Mapping, limits, misconception risks | Analogy cards and rejected options |
| `examleaf-concept-humour` | Relevant, respectful light moments | Optional lines and deletion rationale |
| `examleaf-interaction-designer` | Questions, wait time, hidden answers, retries | Interaction sequence and answer keys |
| `examleaf-confidence-editor` | Informative feedback and honest progress language | Revised feedback |
| `examleaf-voice-director` | Pronunciation, delivery, pauses, synchronization | Voice-ready records |
| `examleaf-language-editor` | English/localized versions and terminology consistency | Language review draft |
| `examleaf-science-reviewer` | Independent verification of claims and solutions | Errors, assumptions, approval blockers |
| `examleaf-script-evaluator` | Combined review, repetition checks, release issues | Structured evaluation report |

The skill files use portable `SKILL.md` conventions. Current project discovery paths are `.claude/skills/` for Claude Code and `.agents/skills/` for Codex; client-specific invocation and permission controls should not be assumed interchangeable. citeturn771459view3turn762447view1

## 11.2 Production sequence

```text
Approved sources + independently checked answer key
                         ↓
Lesson architecture
                         ↓
Conversational draft
                         ↓
Analogy / humour / interaction review
                         ↓
Scientific review and repair
                         ↓
Language and voice preparation
                         ↓
Audio generation and measured synchronization
                         ↓
Rendered academic + accessibility review
                         ↓
Student testing and controlled release
```

Use separate authoring and review roles. Two models agreeing is not, by itself, scientific validation.

## 11.3 Master authoring prompt

```text
Create an original ExamLeaf lesson for the supplied audience,
topic, language and approved source packet.

Audience:
[Class, prerequisite knowledge, examination medium]

Target capability:
[What the learner must do independently after the lesson]

Sources and answer key:
[Approved claims, assumptions, examples and independently
checked answers]

Write as a precise, warm teacher who notices likely confusion
and explains the decision behind each step.

First identify the minimum prerequisites. Do not compress
missing foundations into an unexplained revision.

Use:
familiar observation → accurate representation → plain-language
relationship → formal terminology → worked example → reduced
support → independent attempt → specific feedback.

Use humour only when it clarifies the concept or gently
reduces tension. Zero jokes is acceptable. Do not insult the
student, invent personal teaching experiences, imitate a real
teacher, or pretend the video heard an answer.

For every analogy, provide its mapping, limit, likely
misconception and return to the scientific model.

Distinguish rhetorical questions from genuine tasks.
Keep answers hidden during attempts. Use conditional feedback.
Allow learner-controlled pauses for writing and solving.

Return:
1. Scope and prerequisite check.
2. Beat-by-beat lesson plan.
3. Clean spoken narration.
4. Separate visual, voice and timing directions.
5. Interaction prompts and answer keys.
6. Scientific assumptions and source mapping.
7. Humour/analogy risks.
8. A fresh independent question and delayed-practice task.
9. Unresolved issues requiring human review.

The ten-minute timeline is a planning target, not measured audio.
Do not accelerate dense science or remove necessary conditions
to fit it.
```

## 11.4 Prevent repetitive AI writing

Maintain a recent-script ledger containing the opening type, analogy, joke premise, interaction type, feedback wording, and conclusion.

Review approximately the previous twenty scripts as an initial editorial window. Flag repeated full sentences and nearly identical rhythms—but **do not replace stable scientific terminology with random synonyms**.

Useful variation changes the teaching approach:

> Prediction opening in one lesson; worked-error opening in another.

Unhelpful variation merely replaces “fascinating” with “incredible.”

### Negative tests worth running

Ask the system to handle requests such as:

> “Make the lesson funnier by mocking students who get the answer wrong.”

> “Say the enzyme wants the reaction to happen.”

> “Congratulate the viewer as though we heard their answer.”

> “Fit the same explanation into half the time without dropping anything.”

> “Change the chemical formula so the equation balances.”

The correct response is to preserve the instructional and scientific constraints—not comply creatively.

---

# 12. Complete sample script

## Balancing Chemical Equations: Change the Count, Not the Substance

**Audience:** Class 10 foundations/revision; suitable as Class 12 prerequisite repair, not a complete Class 12 chapter.

**Scope:** simple molecular equations with supplied correct formulas. Ionic equations, reaction mechanisms, and practical reaction procedures are outside this lesson.

The scientific basis is standard atom conservation and balancing through coefficients rather than changing the specified formulas. The narration below is original. citeturn809499view0

**Production status:** planned ten-minute cut, approximately **1,225 spoken words**, with **63 seconds of explicit inspection/thinking allowance** in the downloadable version. No audio has been generated. Final timing must follow the actual voice performance; student-controlled pauses add study time.

*Directions in italics are not spoken.*

---

### 00:00–00:30 — The tempting shortcut

*Curious. Show \(H_2+O_2\rightarrow H_2O\). Display the proposed alternative separately and label it “proposed wrong fix.”*

“Look at this equation. Hydrogen plus oxygen gives water. The oxygen count does not match. So, can we fix it by changing water from H two O to H two O two?

“Hold that answer.”

*[Five seconds.]*

“That would balance the count here. It would also change the product. Very efficient way to solve a different question. Let’s fix the original one.”

---

### 00:30–01:05 — Read the symbols before balancing

*Steady. Show labelled molecules with large, readable subscripts.*

“First, let’s make the symbols readable. H stands for hydrogen. O stands for oxygen. In these molecules, the small number tells us how many atoms of that element are present.

“H two means two hydrogen atoms in one molecule. O two means two oxygen atoms. Water, H two O, contains two hydrogen atoms and one oxygen atom. No small number beside the O means one.

“Those small numbers are called subscripts.”

---

### 01:05–01:40 — What balancing preserves

*Build a simple hydrogen/oxygen counting table. Keep the equation visible.*

“The arrow separates the starting substances, called reactants, from the products formed.

“In an ordinary chemical reaction, atoms are rearranged. We don’t make extra hydrogen atoms appear, or quietly turn oxygen atoms into hydrogen.

“So the equation needs the same number of atoms of each element on both sides. Not the same number of molecules. The same number of each kind of atom.

“That’s the job. We need careful counting, not a new set of substances.”

---

### 01:40–02:25 — Coefficient versus subscript

*Show \(2H_2O\) as two intact molecular copies.*

“There is a number we can change: the number in front of a formula. That’s its coefficient.

“Watch two H two O. It means two water molecules, not one strange new molecule. Each copy still has two hydrogen atoms and one oxygen atom.

“Together, how many hydrogen atoms? And how many oxygen atoms?”

*[Six seconds; totals hidden.]*

“Four hydrogen; two oxygen. The coefficient multiplies the whole formula.

“Now compare H two O two. That’s one molecule of hydrogen peroxide. Changing a subscript changes the composition. We are balancing water’s equation, so water must stay water.”

---

### 02:25–03:00 — A short canteen analogy

*Light. Show one recipe card, then three copies. No crowd animation or sound effects.*

“Think of a canteen recipe card: one sandwich uses two bread slices and one portion of filling. Ordering three sandwiches multiplies every item. It doesn’t rewrite what one sandwich contains.

“That is the useful comparison: the coefficient changes how many copies; the subscripts describe each molecule.

“The comparison stops there. Molecules aren’t sandwiches, and real reactions need suitable conditions. This little story helps us read the numbers; it isn’t a model of how a reaction happens.”

---

### 03:00–03:40 — Worked example: match oxygen

*Return to the equation. Show each count as it is named.*

“Back to hydrogen plus oxygen giving water. Keep the formulas fixed and count.

“On the left: two hydrogen atoms and two oxygen atoms. On the right: two hydrogen atoms, but only one oxygen atom.

“Let’s match oxygen first by putting a two in front of water. We now have two water molecules, so two oxygen atoms on the right.

“But don’t stop at the first matching row. That coefficient changed the hydrogen count as well. Recount it.”

*Display \(H_2+O_2\rightarrow2H_2O\), clearly marked “not yet balanced.”*

---

### 03:40–04:20 — Repair the changed hydrogen count

*Curious. Keep the incomplete equation and atom ledger visible.*

“Two water molecules contain four hydrogen atoms. Our left side has only two.

“Each hydrogen molecule supplies a pair. How many hydrogen molecules give four hydrogen atoms?”

*[Six seconds.]*

“Two. Put a two in front of H two.

“Now count both elements: four hydrogen atoms on each side, and two oxygen atoms on each side.

“That’s why the coefficients are two, one, two. The middle one is normally not written. Nothing was invented, and none of the formulas needed changing.”

*Final display:*

\[
2H_2+O_2\rightarrow2H_2O
\]

---

### 04:20–04:55 — Preserve the important distinction

*Show molecule count separately from atom counts.*

“Notice something slightly surprising. We started with three molecules in this written ratio: two hydrogen molecules and one oxygen molecule. We finish with two water molecules.

“Three molecules became two, but the atom counts still match. Balancing preserves the number of each type of atom, not the number of molecules.

“For your notes, keep one short rule: change coefficients, keep the specified formulas fixed, and check every element. We will use it again without the pictures.”

---

### 04:55–05:35 — Guided completion

*Show \(\_\_CO+\_\_O_2\rightarrow2CO_2\). Do not reveal coefficients.*

“Try a shorter repair. Carbon monoxide plus oxygen gives carbon dioxide. The formulas are C O, O two, and C O two.

“I’ve put a two before carbon dioxide. That gives two carbon atoms on the right. What coefficient must go before carbon monoxide?

“Work that out, then check oxygen as well. Pause the video if you’d like to write both counting rows.

“Don’t change the small two inside carbon dioxide. We’re choosing how many molecules take part.”

*[Seven-second hold; permit a longer student-controlled pause.]*

---

### 05:35–06:15 — Check rather than congratulate blindly

*Reveal the coefficients, then the counting table.*

“Two carbon monoxide molecules give two carbon atoms and two oxygen atoms. One oxygen molecule supplies another two oxygen atoms.

“So the left has two carbon atoms and four oxygen atoms. The right has the same counts. Two C O plus O two gives two C O two.

“If that matches your work, your counting method is working on a new equation.

“If you changed a subscript, restore the original formula first. Then use coefficients to adjust the totals.”

\[
2CO+O_2\rightarrow2CO_2
\]

---

### 06:15–07:05 — Independent attempt

*Remove the counting table. Show only \(N_2+H_2\rightarrow NH_3\) and the task.*

“Now take away the counting table. Nitrogen and hydrogen form ammonia. The given formulas are N two, H two, and N H three.

“Balance the equation using the smallest whole-number coefficients. Start by counting nitrogen, then hydrogen. Write a final count for both elements.

“Pause here and give yourself the time you need. This isn’t a speed test. Resume when you have a candidate answer, even if you still want to check one part.

“Get a candidate answer on the page before you look at the solution.”

*[Ten-second hold; student-controlled pause for the actual working time.]*

---

### 07:05–07:45 — Explain the independent solution

*Reveal the nitrogen match first, then the hydrogen match.*

“One nitrogen molecule contains two nitrogen atoms, so we need two ammonia molecules on the right. Those two ammonia molecules contain six hydrogen atoms.

“Hydrogen arrives in pairs in H two. Three pairs give six.

“That gives one, three, two: N two plus three H two gives two N H three.

“Check nitrogen: two on each side. Check hydrogen: six on each side.

“If you wrote six before H two, you counted hydrogen atoms correctly but forgot that each molecule contains two.”

\[
N_2+3H_2\rightarrow2NH_3
\]

---

### 07:45–08:20 — Balanced versus simplest

*Light. Show \(2N_2+6H_2\rightarrow4NH_3\).*

“One final trap. Two N two plus six H two gives four N H three. Is that balanced?”

*[Five seconds.]*

“Yes. But the coefficients all share a factor of two. Divide all three coefficients by two to get the simplest whole-number ratio: one, three, two.

“The bigger version isn’t chemically unbalanced. It just isn’t the requested simplest answer. Bigger numbers do not earn bonus marks for looking busy.

“Check the ratio as well as the atom totals.”

*Label the original “balanced, not simplest”—not “wrong.”*

---

### 08:20–08:55 — Retrieve and draw

*Hide the worked examples.*

“Close the worked examples. Write one sentence explaining why we change coefficients rather than the given subscripts. Then sketch what two H two O represents. Circles and letters are enough; the diagram does not need to win an art competition.

“Pause while you write.”

*[Seven-second hold; student-controlled pause as needed.]*

“When you return, check two things: did you draw two separate water molecules, and does your sentence explain that changing a subscript changes the composition of the substance?”

---

### 08:55–09:30 — Turn the idea into an exam answer

*Deliberate. Show the definition clearly.*

“Now put the idea into an exam-ready sentence: a balanced chemical equation has equal numbers of atoms of each element on its reactant and product sides.

“Underneath, write your balanced equation and check its smallest whole-number coefficients. Include state symbols and conditions when the question requires them; this lesson has left those out to focus on balancing.

“Remember: a balanced equation checks the atom bookkeeping. By itself, it does not establish the conditions, speed, or steps of a real reaction.”

---

### 09:30–10:00 — Confidence tied to capability

*Warm, matter-of-fact. Return briefly to the opening misconception.*

“Look back at the first shortcut. You can now explain why changing water’s formula answered the wrong question.

“Check your own work: can you count the atoms, choose coefficients, and verify the result without the animation? Any unfinished part tells you exactly what to practise next.

“Tomorrow, balance a fresh equation before reopening your notes. You don’t need to remember my sandwich. You need the counting method.”

---

# 13. How to establish whether this style works for ExamLeaf

Do not evaluate the sample only by asking:

> “Was the teacher fun?”

That is useful feedback, but not the primary outcome.

## Recommended pilot comparisons

| Experiment | Compare | Main outcome |
|---|---|---|
| Conversational wording | Formal versus conversational versions with equivalent science | Independent application |
| Relevant humour | No humour versus a few concept-linked lines | Delayed learning, comfort, distraction |
| Support reduction | Full examples throughout versus faded support | Method selection without hints |
| Delivery | Steady warmth versus more variable enthusiasm | Comprehension and listening effort |
| Language | Audience-appropriate language versions | Understanding, terminology recall, comfort |

Keep content, difficulty, and study-time differences visible. Predefine the outcome before choosing a winner.

Measure immediate understanding, a fresh application, and delayed retrieval. Spaced practice has a substantial evidence base, but the precise follow-up interval should reflect the intended retention goal rather than a universal schedule. citeturn290870search2

Also inspect **confidence calibration**:

- Correct but uncertain.
- Correct and confident.
- Incorrect and uncertain.
- Incorrect but confident.

A version that makes students feel brilliant while producing more confident errors should lose.

Small student sessions are excellent for finding confusing wording, cringe humour, unreadable diagrams, or inadequate pauses. They are not sufficient to establish a modest statistical improvement in learning.

---

## The governing principle

**ExamLeaf should sound human because it teaches responsively—not because it imitates human imperfections.**

The strongest personality will emerge from precise explanations, appropriate pauses, respectful correction, and the occasional line that makes a difficult idea feel less intimidating.

**Make students glad to start with the teacher—and increasingly able to solve the next problem without the teacher.**


=====================================================================
MESSAGE id=fcf95e1b-58a1-4f9a-a3dc-a7250d5ec221 role=user content_type=text create_time=1791903351.955 chars=10798
=====================================================================

# ExamLeaf Video Engine — Complete AI Skills Research, Architecture & Automated Production

Act as a **senior AI systems architect, educational video director, STEM animation engineer, learning psychologist, and Claude Code automation specialist**.

Conduct exhaustive, up-to-date research to design and implement **ExamLeaf Video Engine**, a production-grade AI-assisted system capable of generating hundreds of premium, scientifically accurate, highly engaging educational videos with minimal manual intervention and sustainable costs.

Our focus is Class 10–12 Physics, Chemistry, Mathematics, and Biology, initially for Assam Board. We require approximately 10-minute chapter-wise fast-track revision videos, alongside viral Instagram Reels and YouTube Shorts.

**Quality references:** Professor Dave Explains (primary) and Khan Academy (secondary). No avatars, generic stock footage, robotic narration, irrelevant animations, or inaccurate scientific visuals.

## 1. Discover ALL Relevant Public AI Skills & Integrations

Start by deeply investigating this Higgsfield workflow:

https://higgsfield.ai/blog/faceless-channel-one-prompt

Research its complete pipeline, public Skills, MCP servers, CLI, APIs, automation capabilities, video quality, limitations, and costs.

**Mandatory public repositories to investigate:**

- https://github.com/higgsfield-ai/skills
- https://github.com/remotion-dev/skills
- https://github.com/elevenlabs/skills
- https://github.com/anthropics/skills
- https://github.com/ahujasid/blender-mcp

Also search GitHub, Skills.sh, Claude plugin marketplaces, MCP registries, and other trustworthy sources for relevant public Skills, plugins, agents, and automation frameworks.

Investigate Higgsfield Video Explainer, image/video generation, thumbnail creation, branding, and virality analysis. Explore comparable workflows from Runway, HeyGen, Kling, Veo, Seedance, Pika, Luma, and other relevant services.

Evaluate Manim, Remotion, Motion Canvas, Hyperframes, Blender, Three.js, FFmpeg, scientific simulation packages, specialized subject libraries, AI audio tools, and emerging alternatives.

**Do not confuse agent Skills, MCP servers, APIs, SDKs, and full production platforms.** Identify their actual functions and integration requirements separately.

For each relevant solution, verify:

- Official/community origin, repository, installation, maintenance, documentation, and compatibility.
- Actual capabilities, example outputs, API access, authentication, commercial licensing, and security risks.
- Scientific accuracy, visual consistency, controllability, rendering speed, scalability, and cost.
- Whether it can be reused directly, extended, or replaced by a better custom implementation.

Do not blindly install untrusted Skills or execute unknown scripts. Audit permissions, dependencies, code execution, and credential access first.

## 2. Design the Best Hybrid Video Production Architecture

Determine the ideal combination of **AI-generated visuals and deterministic code-based animations**.

Use whichever technology gives the best result for each scene, not necessarily one video generator for everything.

Research dedicated tools for:

- **Physics:** simulations, forces, optics, electromagnetism, circuits, waves, and working diagrams.
- **Chemistry:** molecular structures, chemical reactions, orbitals, mechanisms, and equations.
- **Mathematics:** animated derivations, graphs, geometry, calculations, and transformations.
- **Biology:** cells, genetics, anatomy, biological processes, and 2D/3D scientific illustrations.

Evaluate subject-specific libraries such as SymPy, SciPy, RDKit, 3Dmol.js, plotting tools, SVG frameworks, and appropriate scientific rendering systems.

Decide where Higgsfield and generative-video tools provide genuine value and where Manim, Remotion, Blender, or other deterministic technologies are more accurate and economical.

Prioritize reusable assets, animations, templates, and consistent ExamLeaf branding.

## 3. Human-Like Teaching & Educational Psychology

Build our previously defined **ExamLeaf Super Teacher** approach into the complete pipeline.

Scripts must feel like an excellent human teacher explaining concepts naturally—not somebody reading a textbook.

Include simple conversational language, storytelling, humour, relatable Indian student experiences, occasional memes/shayari, natural enthusiasm, and memorable analogies.

Use age-appropriate Dora-inspired question-and-answer interactions, intentional pauses, easy confidence-building questions, note-taking prompts, worked examples, and independent practice.

Research effective pacing, attention management, cognitive load, curiosity, student confidence, and memory retention.

Create voice-direction instructions for emotion, emphasis, comedic timing, questions, reassurance, and satisfying learning breakthroughs.

**Every animation, joke, interaction, or motivational statement must improve understanding, engagement, or genuine confidence—not merely increase watch time.**

## 4. Build the Complete End-to-End Automation Pipeline

Architect and specify the actual system:

**Books/PDFs → Syllabus Extraction → Chapter Planning → Academic Research → Human-Like Script → Scientific Verification → Storyboard → Scene Classification → Best Library Selection → Animation Generation → AI Narration → Timeline Synchronization → Video Composition → Automated QA → Human Approval → Export → Instagram/YouTube Repurposing.**

Include:

- Source attribution and syllabus mapping.
- Structured scene specifications and animation manifests.
- Agent orchestration using Claude Code/Codex.
- Subject-specific rendering adapters.
- Reusable assets and centrally managed design tokens.
- Voice pronunciation dictionaries and forced alignment.
- Automated mathematical/scientific validation.
- Frame inspection, subtitle checks, and audio QA.
- Batch rendering, caching, parallel jobs, retry logic, and failure recovery.
- Versioning, observability, reproducible builds, and cost tracking.
- 16:9 long-form and 9:16 short-form output.
- Multilingual support for future expansion.

Clearly distinguish **AI reasoning tasks, deterministic programmatic tasks, and mandatory expert-review checkpoints**.

## 5. Design Our Complete Claude Skills Ecosystem

Identify all existing public Skills we should reuse, those requiring modification, and custom Skills we must develop.

Include Skills for curriculum analysis, academic research, teacher-style scriptwriting, educational psychology, storytelling, humour, storyboarding, library selection, scientific animations, Manim, Remotion, Blender, chemistry/biology visualization, voice direction, synchronization, video assembly, QA, thumbnails, Reel generation, and production orchestration.

For each Skill specify:

- Purpose and invocation conditions.
- Required technologies and dependencies.
- Inputs, outputs, and data formats.
- Installation and integration method.
- `SKILL.md` structure, references, scripts, and templates.
- Exact execution steps.
- Testing, error handling, and fallback behaviour.
- Cost and performance impact.

Prevent duplicate functionality, unnecessary API calls, excessive token usage, and repeated generation of already verified assets.

Design the Skills to work together as **one coordinated, maintainable production system**, rather than disconnected AI tools.

## 6. Instagram & Short-Form Content Automation

Automatically repurpose our chapter tutorials into exceptional educational Reels.

Generate strong hooks, 20–60-second conceptual explanations, animated questions, exam tips, misconception corrections, captions, thumbnails, and appropriate CTAs.

Optimize content for genuine educational value, organic discovery, shares, saves, and bringing students into the ExamLeaf ecosystem.

Support our **3 free chapters → premium content unlocked through physical book purchase** acquisition strategy.

Avoid deceptive clickbait, fake statistics, exaggerated educational claims, and superficial virality scoring.

## 7. Costs, Risks & Production Validation

Compare three production architectures:

1. Commercial AI-heavy.
2. Hybrid open-source + selective AI services.
3. Primarily open-source/self-hosted.

Estimate complete production costs for **1, 100, and 1,000 ten-minute videos**, including AI tokens, generated clips, narration, rendering, infrastructure, human verification, editing, and regeneration.

Identify what to avoid: scientific hallucinations, expensive unnecessary video generation, visual inconsistency, robotic voices, unreadable equations, animation overload, fragile plugins, vendor lock-in, copyright issues, insecure Skills, unreliable automation, and unverified educational claims.

Test the shortlisted architecture through **four pilot videos—one per STEM subject**. Benchmark video quality, academic accuracy, human effort, rendering time, cost, and potential for automation.

## 8. Required Final Output & Implementation

Provide:

1. **Public Skills Master Directory:** Verified repositories, recommended Skills, integrations, and install/use instructions.
2. **Technology Decision Matrix:** Best tools, subject-specific uses, costs, limitations, and alternatives.
3. **Complete System Architecture:** Data flow, agents, rendering engines, integration points, and infrastructure.
4. **Claude Skills Development Plan:** Existing vs custom Skills, dependencies, structures, and implementation priorities.
5. **End-to-End Pipeline:** Exact workflows, automated checks, fallbacks, and human review.
6. **Quality & Cost Comparison:** Recommended architecture with realistic financial calculations.
7. **Implementation Roadmap:** What to build first, in what order, and why.
8. **Pilot Blueprint:** Repository structure, configuration, reusable components, sample scenes, and production instructions.

**Go beyond research. Produce an implementable technical blueprint and, where the development environment permits, create the initial project scaffolding, reusable Skills, interfaces, and a working proof of concept.**

Do not claim an integration works without testing it. Clearly distinguish verified implementations from proposed designs.

**Final objective:** Build an economical, scalable, highly automated **ExamLeaf Video Engine** that combines the best public AI Skills and video technologies with our custom educational framework—producing outstanding long-form tutorials and short-form content with human-like teaching, precise scientific animation, consistent branding, genuine student learning, and minimal repetitive manual work.

**Be comprehensive in your research but decisive in your recommendations. Tell us exactly what to use, what to build, how to integrate it, how to validate it, what it costs, and what to avoid.**


=====================================================================
MESSAGE id=a5cd4964-0c55-403d-8e04-361b5028dd7a role=assistant content_type=text create_time=1791903808.614029 chars=232
=====================================================================

I’ll audit the requested repositories without executing untrusted code, then build subject-specific local rendering tests. I’ll separately flag provider-dependent integrations, academic approvals, and Higgsfield’s actual STEM value.


=====================================================================
MESSAGE id=b50e3e42-e69b-4057-9b66-2862845b24cf role=assistant content_type=text create_time=1791905993.335687 chars=222
=====================================================================

The prototype now renders all four subjects in 16:9 and 9:16, with 55 tests passing; these are silent 24-second engineering tests. Higgsfield’s 10-second-block orchestration remains separate from deterministic STEM scenes.


=====================================================================
MESSAGE id=91516339-0f60-4e45-b1ef-5a24d6a68871 role=assistant content_type=text create_time=1791906572.643237 chars=43768
=====================================================================

# ExamLeaf Video Engine: recommended architecture, verified research, and working prototype

**Build ExamLeaf around verified scientific models and reusable teaching components—not around a general-purpose “generate a complete video” prompt.**

My recommendation is:

> **Python scientific validation → structured lesson and scene specifications → HyperFrames as the production compositor candidate → selective Manim/Three.js/Blender inserts → independently generated narration → measured synchronization → FFmpeg export → academic and production approval.**

Use **Higgsfield and other generative-media services selectively** for illustrations, visual exploration, and packaging. Do not make them responsible for equations, reaction mechanisms, chromosome counts, circuit behaviour, or other scientific assertions.

I have also created an initial implementation rather than stopping at the architecture.

## Deliverables

[**Download the implementation repository, research directory, 32 custom Skill drafts, and eight rendered previews**](sandbox:/mnt/data/ExamLeaf_Video_Engine_Implementation.zip)

[**Download the editable production-cost model**](sandbox:/mnt/data/ExamLeaf_Video_Engine_Cost_Model.xlsx)

[**Read the implementation README**](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/README.md)

[**Read the Public Skills and Integrations Directory**](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/research/Public_Skills_Directory.md)

### What was actually tested

| Deliverable | Actual status |
|---|---|
| Four scientific models and associated visual templates | Implemented and tested |
| Landscape and vertical rendering | **Eight real 30-second MP4s**, two per subject |
| Unit, contract, scientific, and media tests | **56 tests passed** |
| Local caching, media hashes, atomic rendering, and budget ledger | Implemented and tested within the proof |
| Live speech connection | One Runway speech operation returned a **32.18-second audio asset**, consuming **9 workspace credits** |
| Narration imported and synchronized into the videos | **Not completed**; local audio download was blocked |
| Four complete narrated 10-minute lessons | **Not completed**; four full-length planning blueprints are provided |
| HyperFrames, Remotion, Manim, or Blender execution | Researched, **not installed or benchmarked here** |
| Custom Skills evaluated through Claude Code/Codex | Drafted, **not agent-evaluated** |
| Teacher approval or student learning evaluation | Not performed |
| Browser-preview automation | Attempted, but local navigation was blocked by the environment; the restriction was not bypassed |

The previews are therefore **technical proofs, not finished ExamLeaf lessons or evidence of production readiness**.

Research and pricing were checked on **13 October 2026**. Published capabilities, local test results, architectural recommendations, and financial assumptions are distinguished below.

---

# 1. What Higgsfield’s workflow really provides

## 1.1 The useful idea: packaging a complete production workflow

The linked Higgsfield article combines topic selection, scripting, narration, video generation, dubbing, thumbnails, Shorts, and a publishing plan. That is useful as an example of **workflow packaging**. Its revenue and growth claims are marketing claims—not evidence that the same process will produce scientifically accurate lessons or ExamLeaf sales. I did not independently audition its embedded example videos. citeturn488852view0

The important question is not whether one prompt can start many jobs. It is whether the resulting jobs produce correct, reusable, reviewable educational content.

## 1.2 The inspected explainer Skill is more specific than the blog

The live `higgsfield-video-explainer` Skill I inspected was **v0.13.0**. Its documented process uses a shared style reference, short narration blocks, separately generated audio, approximately ten-second generated video clips, and provider-side assembly. Its duration convention implies **60 ten-second blocks for a ten-minute video**. This differs from treating the entire lesson as one monolithic generation request. fileciteturn8file0L2-L2 fileciteturn9file0L2-L2

That architecture has several strengths: asynchronous jobs, consistent style references, modular regeneration, and a clear assembly process.

However, its fixed-slot structure is not ideal for every STEM task. A reaction-state comparison may need a long inspection hold. A calculation may require a student-controlled pause. A derivation may need one persistent diagram rather than successive generated shots.

### What to reuse—and what to replace

| Higgsfield capability | ExamLeaf decision |
|---|---|
| Shared style reference and brand kit | Reuse the concept for approved visual identity |
| Model discovery and generation-cost estimation | Reuse through a bounded provider adapter |
| Persistent asynchronous generation jobs | Reuse the operational pattern |
| Thumbnail exploration | Optional; place exact titles, formulas, and labels deterministically |
| General contextual illustrations | Optional, after scientific and rights review |
| Fully generated scientific diagrams | Do not use as the default |
| Fixed ten-second lesson pacing | Replace with concept- and audio-driven timing |
| Automatic narration fitting | Do not allow it to rush difficult explanations |
| Automatic production of twenty Shorts | Replace with selection of genuinely complete learning units |
| “Virality” or `brain_activity` scoring | Do not treat as a learning, neuroscience, or sales metric |

The public generation guidance exposes a “Virality Predictor” capability. I did not find evidence establishing its calibration for student understanding, examination performance, or ExamLeaf conversion. Its name should not be interpreted as a neurological measurement. citeturn691217view1

## 1.3 Its integration surfaces are not interchangeable

| Surface | Actual role | Integration implication |
|---|---|---|
| **Skill** | Instructions telling an agent how to perform a workflow | Does not itself supply rendering or scientific verification |
| **CLI** | Executable interface for account, model, and generation operations | Needs installation, authentication, version pinning, and command-level controls |
| **MCP server** | Exposes provider tools to an agent | Needs approved account access, permissions, and spending controls |
| **Developer API** | Programmatic service interface | Requires confirmed endpoint access, credentials, and separate billing assumptions |
| **Web platform** | Hosted interface, workflows, plans, and credits | A web subscription does not establish unlimited API/MCP capacity |

Higgsfield documents its CLI, MCP connection, and separate API offering. Its web “Unlimited” arrangements should not be assumed to apply to MCP/CLI workflows. **I did not obtain a verified, authenticated all-in price for a ten-minute Higgsfield explainer.** That remains a required account-level estimate, not a number to invent from a subscription headline. citeturn823021view1turn472407search2turn472829search0

**Verdict:** Higgsfield is a useful optional media supplier and workflow reference. It should not be ExamLeaf’s scientific authority or primary lesson-planning system.

---

# 2. Public Skills master directory

The downloadable directory records **21 repositories or integration surfaces**, with origin, purpose, installation approach, authentication, licensing cautions, verification level, and important inspected-file identifiers.

This is a verified shortlist—not a claim that every relevant Skill in a changing public ecosystem has been exhaustively enumerated.

## 2.1 Mandatory repositories and recommended selections

| Repository | Recommended use | Audit conclusion |
|---|---|---|
| **[higgsfield-ai/skills](https://github.com/higgsfield-ai/skills)** | Selected explainer, generation, brand-kit, and thumbnail patterns | Adapt; do not inherit its scientific generation or fixed pacing wholesale |
| **[remotion-dev/skills](https://github.com/remotion-dev/skills)** | Best practices, rendering, captions, multimedia, documentation | Reuse only when Remotion is the selected compositor |
| **[elevenlabs/skills](https://github.com/elevenlabs/skills)** | `text-to-speech`, `speech-to-text`; selective isolation/dubbing | Reuse behind ExamLeaf pronunciation, caching, timing, and budget controls |
| **[anthropics/skills](https://github.com/anthropics/skills)** | Skill evaluation, web testing, MCP-development patterns | Useful foundations, not production guarantees |
| **[ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender)** | Supervised Blender asset authoring | The requested older repository redirects to this renamed project; isolate it from production |

The live Remotion README listed twelve Skills; the ElevenLabs README listed ten. The ElevenLabs documentation also identifies its current Python package, JavaScript package, CLI, and API-key environment variable. These are separate from whether a particular voice is appropriate for ExamLeaf. fileciteturn7file0L2-L2 fileciteturn6file0L2-L2

### Important licensing distinction

Anthropic’s repository does **not** apply one unrestricted open-source licence to everything. Its document Skills are source-available under separate terms. Likewise, an open-source Skill or bridge does not grant commercial rights to every voice, model weight, imported asset, or hosted service it invokes. fileciteturn16file0L2-L2

## 2.2 Additional resources worth selecting

**HyperFrames:** reuse the core composition, animation, keyframe, audio, and CLI guidance. Its live manifest and cached README did not agree on the number of available Skills, illustrating why production should pin inspected files rather than depend on a remembered marketplace count. fileciteturn10file0L2-L2 citeturn162484view0

**Community Manim Skills:** the `adithya-s-k/manim_skill` repository is a useful candidate for Manim Community guidance. Do not mix its Manim Community and ManimGL instructions. Some runtime guidance can lag current official requirements; I did not execute its claimed tests. citeturn903828view0

**K-Dense scientific-agent-skills:** selectively consult SymPy, RDKit, Biopython, and scientific-visualization instructions. Do not install the entire scientific stack or treat package guidance as an academic reviewer. citeturn472829search1

**Skills.sh, MCP registries, and Claude plugin marketplaces:** use them for discovery, then return to the publisher’s repository and actual package. A listing, install count, or badge is not a complete security audit. citeturn472829view0turn472829view1turn672487search6

## 2.3 Blender MCP deserves special caution

The renamed project is a **community bridge, not an official Blender Foundation integration**. It can execute Python inside Blender. Its documented local bridge and arbitrary-code capabilities require meaningful isolation, not merely a reassuring Skill prompt. fileciteturn11file0L2-L2 citeturn337943search1

The current README distinguishes **opt-in content telemetry** from **minimal anonymous usage telemetry enabled by default**. `DISABLE_TELEMETRY=true` disables telemetry. This is more precise than saying either “all telemetry is on” or “nothing is collected.” fileciteturn15file0L2-L2

**Production decision:** use MCP, when necessary, on an isolated authoring workstation. Render approved assets through pinned, headless Blender scripts—not an unrestricted live agent session.

## 2.4 Safe installation process

Do not run public `curl | bash` installers or install every discovered Skill.

Use this admission process:

> Confirm publisher → inspect repository and scripts → review licences and permissions → pin a real commit/package digest → test in isolation → copy only approved components → re-audit upgrades.

An inspected **file blob SHA is not a commit SHA**. The directory preserves this distinction.

For ExamLeaf’s original Skills, copy only the relevant folders into the client’s supported Skill directory. Claude Code and Codex support Skill-based workflows, but their discovery, invocation, and permission behaviour should be checked against current documentation. citeturn132751view0turn132751view2

---

# 3. Technology decision matrix

## 3.1 Primary rendering decision

| Technology | Recommended role | Strength for ExamLeaf | Main limitation |
|---|---|---|---|
| **HyperFrames** | Primary production compositor candidate | HTML/SVG, seekable animation, local rendering, agent-oriented workflow | Must pass the same scientific fixtures and narration tests before adoption |
| **Remotion** | Strong alternative, particularly for React teams | Programmatic React composition and reusable components | Conditional commercial licensing; avoid maintaining two compositors unnecessarily |
| **Manim Community** | Specialist mathematics/physics inserts | Equations, geometry, vectors, graphs, transformations | Additional runtime and authoring conventions |
| **Motion Canvas** | Alternative vector-animation environment | TypeScript animation designed for explanatory work | Another full animation stack if added alongside the others |
| **Three.js** | Selective browser-based 3D | Spatial relationships, geometry, molecules | Camera and geometry accuracy remain your responsibility |
| **Blender** | Reusable specialist 3D assets | Detailed spatial models and offline rendering | Higher authoring/review cost; asset and script security |
| **FFmpeg** | Required media infrastructure | Encoding, assembly, muxing, probing, audio processing | Does not verify educational or scientific correctness |
| **Native SVG/CairoSVG proof** | Reference adapter and regression fixture | Small, locally testable, model-driven | Only four bounded templates are implemented |

HyperFrames documents HTML-based, seekable rendering through a browser and FFmpeg under Apache-2.0. Manim Community and Motion Canvas provide different specialist animation approaches. These documentation findings establish their intended capabilities—not a benchmark victory for ExamLeaf. citeturn162484view0turn162484view2turn162484view3

Remotion’s current automation pricing includes **$0.01 per billable render with a $100 monthly minimum when the paid licence applies**. Confirm organizational eligibility and what counts as a render; a finished lesson can involve multiple rendering operations. citeturn162484view1

**Decision:** begin the production comparison with HyperFrames. Switch to Remotion when measured developer productivity, reliability, or repair time makes it the better total-cost choice.

Do not decide from licence price alone.

## 3.2 Subject-specific libraries and boundaries

| Subject | Recommended libraries/modules | What they should control | What they do not prove |
|---|---|---|---|
| **Physics** | SymPy physics/vector/mechanics; SciPy `solve_ivp`; Pint; Schemdraw; selective Magpylib | Equations, trajectories, units, circuit drawings, selected magnetic fields | That the chosen model matches every real system |
| **Chemistry** | RDKit `Chem`, `AddHs`, `rdDepictor`, `rdMolDraw2D`, `rdChemReactions`; selective 3Dmol.js | Molecular identity, atom counts, coordinates, approved reaction-state depictions | Reaction feasibility, correct mechanism, or required conditions |
| **Mathematics** | SymPy; KaTeX; SVG; Manim Community | Expressions, domains, graphs, symbolic checks, visible transformations | That an attractive transformation is a justified mathematical step |
| **Biology** | Approved layered SVG; explicit process-state tables; Biopython; Mol* where useful | Counts, sequence data, structure displays, process-state transitions | General anatomical or biological correctness |

The official documentation supports these package roles. In particular, Schemdraw is a drawing tool, Magpylib is not a general time-dependent Maxwell solver, and molecular viewers are not chemistry validators. citeturn903828view1turn254930view0turn416018view0turn416018view1turn254930view3turn903828view2turn903828view3turn254930view1turn254930view2

### The essential integration rule

**Every simultaneous representation of the same system must consume the same verified state.**

For example, the capacitor voltage, graph marker, displayed number, and explanatory caption must agree.

The prototype exposed precisely this issue: the explanation referred to one time constant while the animated display had already moved past that state. I corrected the synchronization and added a regression test. A mathematically correct model alone had not prevented the misleading presentation.

---

# 4. Where generative media belongs

## 4.1 Route by scientific responsibility

| Scene type | Default production method |
|---|---|
| Formula, derivation, graph, calculation | Deterministic |
| Atom identity, charge, reaction state | Domain-validated deterministic representation |
| Chromosome count, genetic probability, process direction | Explicit reviewed state model |
| Anatomical/spatial structure | Reviewed SVG or licensed/approved 3D model |
| Contextual real-world illustration | Owned/licensed media or selectively generated illustration |
| Thumbnail background, visual metaphor, brand exploration | Optional generation; exact text added afterward |

**The default generated-video allowance should be zero seconds.** Add generated material only when it serves a clear instructional purpose.

This does not mean generative tools never produce useful scientific-looking material. It means ExamLeaf must not infer correctness from appearance.

## 4.2 Comparable commercial services

| Service/model route | Sensible ExamLeaf use | Verified limitation |
|---|---|---|
| **Runway** | Optional contextual clips and supported audio operations | Model access depends on the account; no generative-video operation was tested here |
| **Higgsfield** | Creative exploration, brand references, optional illustrations and packaging | No authenticated all-in lesson quote obtained |
| **Veo** | Selected context footage through an approved provider | Exact model, audio mode, resolution, input charges, and route affect cost |
| **Seedance** | Optional generated clips through a verified provider | Provider catalogue access is not evidence of direct model-owner API access |
| **Kling** | Optional contextual generation | Direct-owner access/pricing was not fully verified in this audit |
| **Pika** | Secondary API candidate | Its current developer pricing includes membership plus usage; not simply web-plan credits |
| **Luma** | Secondary image/video candidate | API existence was checked, but a reliable current all-in price was not resolved |
| **HeyGen avatar services** | Not needed for this brief | HyperFrames can be selected without adopting an avatar workflow |

Runway publishes per-model credit rates; Pika publishes a separate developer pricing structure. These cannot be flattened into one universal “AI video cost per minute.” citeturn488852view2turn397395view1turn982399search4

**Do not rank generated-video quality as tested here.** No side-by-side scientific-video audition was performed.

---

# 5. Complete production architecture

```text
Permitted books/PDFs + official syllabus/version
                         ↓
Native extraction + page references + rights record
                         ↓
Source-linked claims + prerequisites + checked answers
                         ↓
Lesson plan + Super Teacher script
                         ↓
Independent scientific validation
                         ↓
ACADEMIC APPROVAL
                         ↓
Storyboard + scene classification
                         ↓
Verified scientific data + approved components
                         ↓
Narration generation + pronunciation review
                         ↓
Actual-audio alignment + semantic event timing
                         ↓
Scene rendering + captions + automated QA
                         ↓
FULL FINAL-VIDEO REVIEW
                         ↓
Approved long-form export
                         ↓
Standalone ShortSpec → vertical recomposition → review
                         ↓
Approved publishing and acquisition metadata
```

## 5.1 Separate AI work from programmatic work

| Responsibility | AI-assisted task | Deterministic task | Human gate |
|---|---|---|---|
| Curriculum | Propose topic mapping and identify gaps | Preserve source/year/edition records | Approve syllabus fit and rights |
| Teaching | Draft explanation, analogy, questions | Check references and coverage | Approve explanation and answer keys |
| Science | Suggest model and tests | Symbolic, numerical, dimensional, count checks | Approve assumptions and limitations |
| Visuals | Select components and propose layout | Render exact state at frame time | Inspect scientific implications |
| Audio | Normalize terminology and delivery | Synthesize, cache, measure, align | Listen for pronunciation and clarity |
| Release | Summarize defects and draft metadata | Verify hashes, required checks, approvals | Approve the complete final lesson |

An LLM may help discover an error. It should not be the sole authority declaring its own work correct.

## 5.2 Core data contracts

The scaffold includes typed contracts for:

**`LessonPlan`** — board, class, language, objectives, prerequisites, sources, claims, review state.

**`SceneSpec`** — scientific parameters, assumptions, cues, duration, subject, renderer kind.

**`AssetManifest`** — content hash, origin, licence, attribution, and generated-asset provenance.

**`ProviderJob`** — input hash, idempotency key, provider job identifier, estimated/actual cost, state.

**`ShortSpec`** — source claims, retained conditions, complete payoff, duration, access destination, vertical reflow.

**`Approval`** — reviewer role and exact artifact hash.

The local approval model is **not an authenticated approval service**. Production must establish who can approve, bind approval to the exact artifact, and invalidate it after material changes.

## 5.3 Orchestration

Use Claude Code/Codex for **engine development, component authoring, bounded repairs, and structured production tasks**.

Use a durable workflow system—not an indefinitely running chat—to own production state.

My proposed progression is:

> Local jobs and SQLite → validated pilot batch → Prefect, PostgreSQL, object storage, and isolated workers.

Do not introduce Kubernetes, multiple orchestration frameworks, or a large MCP fleet before the workload justifies them.

Separate workers for research, rendering, paid provider operations, and publishing. The scriptwriter should not possess publishing credentials or unrestricted billing access.

## 5.4 Caching and failure recovery

A scene cache should depend on:

> Source claims + scientific assumptions/data + component version + design tokens + narration + language + voice/model settings + renderer environment.

Regenerate only affected units.

For paid jobs, persist the provider job ID immediately. A timeout or unknown status means **reconcile the existing job**, not “submit again and hope.”

The local implementation already tests a cents-based reservation ledger and idempotency behaviour. Actual provider reconciliation and distributed scheduling remain implementation work.

---

# 6. The coordinated custom Skills ecosystem

I consolidated the workflow into **32 purpose-specific custom Skills** rather than installing several overlapping “make a video” agents.

Every draft includes purpose, inputs, outputs, dependencies, execution steps, acceptance criteria, fallback behaviour, cost implications, references, and authored evaluation cases.

[**Download/read the complete custom Skill inventory**](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/research/custom_skills.csv)

| Group | Skills |
|---|---|
| **Sources and curriculum** | `source-ingest`, `curriculum-map`, `claim-research`, `lesson-plan` |
| **Teaching** | `super-teacher`, `analogy-humour`, `interaction-design` |
| **Scientific validation** | `science-math`, `science-physics`, `science-chemistry`, `science-biology` |
| **Storyboarding and rendering** | `storyboard-route`, `svg-scenes`, `manim-scenes`, `web-composition`, `blender-scenes`, `molecule-scenes`, `biology-scenes` |
| **Audio and language** | `voice-direction`, `voice-synthesis`, `alignment-localize` |
| **Production and release** | `render-batch`, `visual-qa`, `audio-caption-qa`, `release-review` |
| **Short-form and packaging** | `reel-repurpose`, `thumbnail-package` |
| **Operations and assurance** | `observability-cost`, `skills-security`, `learning-evaluation`, `asset-library`, `selective-generation` |

All names carry the `examleaf-` prefix in the repository.

### Example of a useful Skill contract

**`examleaf-science-chemistry`**

**Invoked when:** a scene introduces structures, atom counts, reaction states, or balancing.

**Inputs:** approved structures, formulas, conditions, claim IDs, and answer key.

**Execution:** parse permitted structures; verify identity/counts; hold formulas fixed; inspect charge and mapping where relevant; flag mechanism/condition claims for expert review.

**Output:** machine-readable scientific report and approved scene data.

**Failure:** stop unsupported content. Do not reinterpret “balanced” as “chemically feasible.”

**Cost:** predominantly local computation, with expert review retained.

The corresponding local proof checks the bounded hydrogen/oxygen/water example. It does not claim a general reaction-mechanism validator.

## Avoid duplication

One Skill owns each output. Public renderer Skills supply package-specific knowledge; ExamLeaf Skills supply curriculum, teaching, scientific and release constraints.

Do not have three agents independently rewrite the narration, or both HyperFrames and Remotion Skills competing over the same composition.

Claude’s Skill and subagent mechanisms support this organization, but Skill instructions are not operating-system security controls or evidence that the autonomous workflow has passed evaluation. citeturn132751view0turn132751view1

---

# 7. Super Teacher behaviour belongs in the data, not just the prompt

The engine should explicitly represent:

**Question → hidden answer → thinking time → explanation → targeted repair → independent attempt.**

That is much more reliable than placing “make it engaging and human” in a system prompt.

## 7.1 Proposed script requirements

Every lesson should have a concrete capability, prerequisite repair, worked example, reduced-support task, independent attempt, and useful feedback.

Humour and analogies are optional. Each analogy should record what maps, what does not, and where the explanation returns to science.

Example:

> “Changing water into hydrogen peroxide would make the count convenient. Unfortunately, we were asked to balance the water equation—not replace the product.”

Then immediately restore the scientific rule and ask the student to count.

Do not fabricate student responses:

> “If your answer matches, check whether your reasoning matches too.”

Not:

> “Yes! I heard you say four.”

Retrieval practice has strong classroom evidence, but that does not establish a universal interaction interval. Relevant humour can improve some social-emotional and motivational responses; the cited 2026 study does not establish examination-score gains. citeturn416018search0turn416018search2

## 7.2 Initial production targets—not universal scientific optima

For pilots, start with approximately **1,100–1,250 narration words**, ordinary English delivery around **130–155 active words per minute**, three or four brief predictions, and two or three learner-controlled practice pauses.

Use less animation when students need to inspect, write, or calculate.

Keep essential diagrams and quantities visible. Use colour consistently, but do not claim that particular HEX codes improve memory.

The proposed palette remains `#F7F9FC` background, `#14213D` text, `#185ABD` blue, and `#087986` teal. Check real adjacent colours, fine symbols, phone display sizes, and captions. WCAG’s normal-text contrast baseline is 4.5:1; meeting that alone does not establish complete accessibility. citeturn161541view2

## 7.3 Audio implementation

Keep separate fields for:

- Display equation.
- Spoken wording.
- Pronunciation guidance.
- Editorial delivery mode.
- Pedagogical silence.
- Visual reveal event.

Editorial modes such as **STEADY, CURIOUS, DELIBERATE, LIGHT, REASSURING** are not universal TTS syntax.

Generate short segments, measure the actual waveform, then align meaningful events. ElevenLabs offers a forced-alignment endpoint, but that integration is **not implemented in the supplied project**. citeturn161541view5

For future Assamese production, require a successful model-specific request and native review. A vendor’s broad language count is insufficient.

For self-hosted voice experiments, Kokoro’s model card is worth evaluating. F5-TTS illustrates why code and weight licences must be checked separately; its open code does not automatically make all pretrained weights suitable for commercial use. citeturn416018view4turn416018view5

---

# 8. What the prototype contains

The repository is deliberately small and inspectable:

```text
ExamLeaf_Video_Engine/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── pyproject.toml
├── configs/
├── schemas/
├── src/examleaf/
│   ├── contracts.py
│   ├── interfaces.py
│   ├── science.py
│   ├── visuals.py
│   ├── pipeline.py
│   ├── audio.py
│   ├── budget.py
│   └── cli.py
├── examples/
├── skills/                  # 32 original Skill drafts
├── tests/
├── scripts/
├── research/
├── docs/
├── outputs/
├── preview.html
└── DELIVERY_MANIFEST.json
```

The scientific templates are bounded by design. Unsupported parameters or models should fail rather than produce a plausible-looking animation.

## 8.1 Four actual rendering proofs

| Subject | Preview and checked model | Landscape render time | Vertical render time |
|---|---|---:|---:|
| Physics | [RC charging](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/physics_rc_16x9.mp4): initial condition, one time constant, KVL, numerical/analytical agreement | **27.338 s** | **28.102 s** |
| Chemistry | [Atom balancing](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/chemistry_balance_16x9.mp4): specified molecular identities and atom counts | **28.670 s** | **29.375 s** |
| Mathematics | [Chain rule](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/mathematics_chain_16x9.mp4): symbolic and finite-difference check for \((3x+1)^2\) | **27.372 s** | **27.576 s** |
| Biology | [Monohybrid cross](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/biology_genetics_16x9.mp4): probabilities and complete-dominance assumption | **27.425 s** | **27.951 s** |

Each file is **30 seconds, 720 frames, 24 fps**, rendered at 1280×720 or 720×1280. Two jobs ran concurrently.

These timings are **not** a forecast for a fully narrated ten-minute lesson, complex 3D, or a browser compositor.

[**View the landscape contact sheet**](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/technical_previews_contact_sheet.jpg)

[**View the vertical-layout contact sheet**](sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/vertical_review.jpg)

## 8.2 Run the proof

The reference environment is Linux; the README explains the system-font dependency and portability limitations.

```bash
python -m venv .venv
# Activate the environment using your shell's normal command.

python -m pip install -e '.[chemistry,test]'

PYTHONPATH=src python -m examleaf.cli validate examples/physics_rc.json
PYTHONPATH=src python -m examleaf.cli batch --workers 2
PYTHONPATH=src pytest -q
```

Media preview:

```bash
python -m http.server 8000 --bind 127.0.0.1
# Open http://127.0.0.1:8000/preview.html locally.
```

The supplied browser page was not validated here because administrator policy blocked navigation. The actual MP4 dimensions, frames, duration, codec, and stream properties were checked separately.

The release command should currently **block**:

```bash
PYTHONPATH=src python -m examleaf.cli release-check \
  outputs/physics_rc_16x9.mp4 \
  outputs/physics_rc_16x9.manifest.json
```

That is correct behaviour: the preview lacks final narration and genuine academic/full-video approval.

---

# 9. Four complete pilot lessons: the next validation gate

Do not stretch the technical clips to ten minutes. Build actual teaching sequences.

| Pilot | Full-lesson objective | Critical validation |
|---|---|---|
| Physics | Interpret a changing circuit model and its graph | Conditions, units, numerical/display agreement; approve actual syllabus relevance before publishing |
| Chemistry | Balance a fresh equation and explain coefficient versus subscript | No changed chemical identity; no implication that balance proves reaction feasibility |
| Mathematics | Apply the chain rule to a new nested expression | Domains, visible reasoning, independent method selection |
| Biology | Explain a monohybrid cross and distinguish probability from guaranteed counts | Genotype/phenotype distinction, explicit assumptions, no small-family guarantee |

For each, record:

**Academic defects, reviewer minutes, editing minutes, pronunciation repairs, render time, peak memory, accepted-asset generation attempts, total cost, and student performance on a fresh question.**

Compare HyperFrames and Remotion using identical approved content, voice, fonts, frame counts, hardware, and concurrency. Record cold and cached performance separately.

**A single critical scientific error should block release regardless of the overall visual score.**

The planning document allows more academic and editorial effort for the first pilots than the mature per-video cost model. New components and first-use explanations should not be priced as if the library already existed.

---

# 10. Short-form production and the book-linked funnel

## 10.1 Recompose, do not merely crop

For each approved lesson, initially select **one to three genuinely complete Shorts**:

**One misconception → one prediction → one explanatory payoff → one relevant CTA.**

Do not require twenty outputs because a platform workflow advertises twenty.

The `ShortSpec` retains source claims and assumptions, constrains duration to 20–60 seconds, and requires vertical reflow. A crop that removes a graph axis or condition is a scientific defect, not a cosmetic issue.

### Example

**Hook:** “Which line represents greater resistance? Check the axes.”

**Payoff:** Compare current at the same voltage.

**CTA:** “Try the free graph checkpoint.”

The answer should be delivered in the Short. The CTA offers useful next practice rather than withholding essential information.

## 10.2 Separate publishing from access control

The engine should export:

- Lesson, class, subject, language, and edition identifiers.
- Free/preview/book-entitlement designation.
- Correct destination resource.
- Approved thumbnail/title/description.
- Source and rights attribution.
- Approved video hash.

Your learning platform—not the renderer—should enforce the **first-three-free and book-redemption policy**.

That prevents changing a commercial offer from requiring the scientific video to be rebuilt.

Do not include activation secrets in videos, public QR artwork, or export metadata.

## 10.3 Measure useful behaviour

Track qualified visits, checkpoint attempts, completion of useful practice, book activation, and retained purchases using appropriate privacy controls.

Do not optimize the production agent against an opaque virality score. A title that increases clicks but attracts the wrong students or misrepresents the lesson is not a successful result.

---

# 11. Production costs: three architectures

The workbook contains editable formulas for **1, 100, and 1,000 videos**, plus human-capacity and optional-Shorts calculations.

**All figures below are USD before tax.** They are planning estimates using published tariff inputs—not vendor quotes or measured ten-minute production costs.

## 11.1 Tariff and workload basis

The illustrative API workload uses:

- Sonnet 4.6: 120,000 input and 25,000 output tokens.
- Opus 4.6 review: 60,000 input and 10,000 output tokens.
- Haiku 4.5 routing: 20,000 input and 3,000 output tokens.
- A 30% LLM regeneration allowance.

At the checked published rates, this gives approximately **$1.72 of LLM usage per lesson**. The token workloads are assumptions, not observations from the local proof. citeturn488852view3

Narration assumes 8,000 characters, 20% regeneration, and **$0.10 per 1,000 characters**, giving approximately **$0.96**. That tariff is from the checked ElevenLabs API page; the separate Runway audition used workspace credits and is not billed by this calculation. citeturn488852view1

The generated-video comparison uses an illustrative **$0.10/second provider route**, not a Higgsfield whole-lesson price. Exact requests may have additional model/input/resolution charges. citeturn488852view2

## 11.2 Per-video operating assumptions

| Component | Commercial AI-heavy | Recommended hybrid | Mostly self-hosted |
|---|---:|---:|---:|
| Generated video | 600 seconds × 1.8 attempts | Optional 20 seconds × 2 attempts | None |
| Machine cost, including modeled regeneration | **$111.48** | **$7.68** | **$2.32** |
| Academic, production QA, and repair labour | **$47.50** | **$26.67** | **$35.00** |
| **Variable cost/video** | **$158.98** | **$34.34** | **$37.32** |
| Fixed monthly allowance | $250 | $300 | $900 |
| Illustrative one-time setup | $5,000 | $10,000 | $16,000 |

The self-hosted case assumes more maintenance/repair effort and unbenchmarked GPU workloads. It does **not** establish that every self-hosted implementation will cost more than hybrid.

The AI-heavy case does **not** assume equal scientific quality. More spending cannot make an unvalidated generated diagram acceptable.

## 11.3 Total operating cost by volume

All cases use the same one-month accounting period.

| Architecture | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|
| **Commercial AI-heavy** | **$408.98** | **$16,147.60** | **$159,226.00** |
| **Hybrid** | **$334.34** | **$3,734.27** | **$34,642.67** |
| **Mostly self-hosted** | **$937.32** | **$4,631.50** | **$38,215.00** |

These totals exclude the separately displayed setup investment.

For the hybrid case at 1,000 videos:

- Operating production: approximately **$34,643**.
- Including the illustrative initial setup: approximately **$44,643**.
- Removing the optional generated-video allowance reduces variable cost to approximately **$30.34/video**.

The proposed three-Short package adds approximately **$4.32 per source lesson** under its stated token, voice, rendering, and editorial allowances.

### Human capacity is the major scaling constraint

The hybrid model includes **85 human minutes per lesson** across academic review, production QA, and repairs.

At 1,000 lessons, that is approximately **1,417 hours**, or **8.85 full-time-equivalent months at 160 hours each**.

“Minimal repetitive work” is realistic. “No subject reviewers needed” is not the operating model being recommended.

### Exclusions to keep visible

Taxes, audience streaming, long-term asset retention, legal clearance, purchased hardware, royalties, and a larger engineering team are not silently included. New bespoke anatomy, complex mechanisms, or extensive localization can materially increase costs.

The separate local proof had no cloud-render invoice. That is **not evidence that production rendering is free**.

---

# 12. Security, licensing, and reliability requirements

## Non-negotiable controls

**Untrusted content stays data.** PDFs, README files, source comments, captions, and fetched pages cannot authorize shell commands, package installation, or credential access.

**Production renders use staged local assets.** No uncontrolled network fonts or remote media dependencies during final rendering.

**Provider workers have narrow secrets and budgets.** The scriptwriter does not need billing credentials.

**Failures do not silently change the lesson.** A failed voice request must not select a different accent; an unsupported scientific model must not become an approximate animation without review.

**Approvals bind to hashes.** A changed equation, voice segment, caption, or scientific scene invalidates the relevant approval.

**Licences are tracked by component.** Blender’s software licence does not automatically impose that licence on rendered artwork, but imported models and assets retain their own obligations. GSAP likewise has its own standard licence rather than being assumed MIT because it is free to use in many contexts. citeturn444810search14turn162484view5

### What to avoid

Do not build an unrestricted agent that can install Skills, browse private files, generate billable media, modify scientific claims, and publish—all under one identity.

Do not equate two LLMs agreeing with independent scientific validation.

Do not use “physics-aware video generation” as a replacement for equations and boundary conditions.

Do not approve a lesson from thumbnail frames alone.

Do not claim that a fully automated production process guarantees learning, revenue, monetization, or immunity from piracy.

---

# 13. Implementation roadmap

| Phase | Build | Gate |
|---|---|---|
| **0 — contracts and academic scope** | Review source rights, syllabus mapping, claim structure, design tokens, voice corpus | Academic owners agree on the definition of correctness |
| **1 — compositor selection** | Port the four golden fixtures to audited HyperFrames and Remotion environments | Choose using correctness, reliability, repair time, and cost |
| **2 — audio and four full pilots** | Implement TTS lifecycle, actual forced alignment, pronunciation review, full scripts and exercises | Four complete, reviewed lessons—not expanded silent previews |
| **3 — controlled batch** | Durable orchestration, provider failure recovery, object storage, reviewer workflow | Twenty to thirty lessons with measured costs and defects |
| **4 — scalable production** | Expand validated components, subjects, languages, and worker capacity | Stable quality gates and evidence of independent learning |

A reasonable planning sequence is several weeks of dedicated engineering and available subject review—not a promise that installing Skills completes the system.

The highest-value next work is **not another discovery sweep or a more elaborate dashboard**. It is implementing the selected browser adapter, finishing the audio lifecycle, and producing the four genuinely complete pilot lessons.

---

## Final decision

**Use HyperFrames as the initial production candidate, preserve Remotion as the measured alternative, and make verified scientific data the permanent centre of the system.**

Reuse public Skills for package knowledge and workflow mechanics. Keep ExamLeaf’s curriculum mapping, teacher personality, scientific checks, interactions, pronunciation, and release rules in a coordinated custom layer.

The delivered repository establishes a working technical foundation: four checked models, eight actual outputs, 56 passing tests, explicit interfaces, and a documented path to full production. It does **not** yet establish a production-grade, fully narrated, academically approved video factory.

**Promote it to that status only after the four complete pilots demonstrate correct science, clear teaching, reliable synchronization, manageable human effort, and defensible costs.**


=====================================================================
MESSAGE id=bbcd91bd-45e5-4150-848f-d955054c8ef5 role=user content_type=text create_time=1791907371.529 chars=8893
=====================================================================

# ExamLeaf — Advanced AI Narration, Human Voice Acting & Teaching Skills

Research and develop a **complete AI-powered narration and voice-production system** for ExamLeaf, integrated with Claude Code/Codex and our educational video-generation pipeline.

Our narration must feel like an **exceptionally talented, energetic, funny, warm, and experienced human teacher**—never like an AI reading a textbook.

Students should feel that a brilliant teacher is personally explaining the concept, asking them questions, making them laugh naturally, encouraging them, and helping them confidently solve problems.

### 1. Research Public Narration Skills & Voice Technologies

Discover and evaluate all relevant public Claude Skills, agent plugins, MCP servers, APIs, and open-source tools, especially:

- ElevenLabs Skills (TTS, STT, voice changer, dubbing, audio cleanup).
- Cartesia Skills and Sonic TTS.
- Remotion voiceover and audio synchronization Skills.
- Gemini TTS and its expressive speech controls.
- OpenAI speech-generation technologies.
- Chatterbox, Fish Speech, F5-TTS, CosyVoice, Kokoro, and other relevant open-source alternatives.
- Forced-alignment, audio analysis, pronunciation, mastering, and automated QA tools.

Verify current documentation, actual capabilities, licensing, pricing, Indian English/Hindi/Assamese support, emotional expressiveness, voice consistency, and suitability for bulk production.

### 2. Build Dedicated Custom Claude Narration Skills

Design reusable Skills for:

1. **Super Teacher Scriptwriter** — Convert academic material into simple, conversational, engaging explanations.
2. **Human Dialogue Naturalizer** — Remove robotic phrasing, unnatural transitions, textbook language, and repetitive AI expressions.
3. **Educational Storytelling** — Introduce relatable stories, analogies, real-life situations, and memorable explanations.
4. **Humour & Meme Director** — Add natural jokes, witty observations, appropriate shayari, and culturally relevant humour without interrupting learning.
5. **Student Psychology Director** — Use curiosity, achievable challenges, encouragement, and genuine confidence-building techniques.
6. **Interactive Teaching Director** — Insert questions, student-response pauses, predictions, note-taking instructions, and guided practice.
7. **Voice Acting Director** — Specify emotional delivery, vocal energy, excitement, warmth, emphasis, suspense, comedic timing, and natural pauses.
8. **Narration Pacing Controller** — Adjust speaking speed according to concept complexity, calculations, emotional moments, and student interaction.
9. **STEM Pronunciation Specialist** — Ensure correct spoken formulas, equations, symbols, Greek letters, units, chemicals, scientific terms, and Indian names.
10. **Multilingual Language Director** — Manage natural English, selective Hinglish, Hindi, and Assamese while preserving scientific correctness.
11. **TTS Provider Adapter** — Translate our standardized narration instructions into provider-specific settings, supported expressive tags, and API requests.
12. **Speech-to-Animation Synchronizer** — Align narration with diagrams, equations, scene changes, captions, highlights, and interactive pauses.
13. **Audio Production Engineer** — Handle audio mastering, loudness consistency, clean dialogue, silence, music, and sound effects.
14. **Narration Quality Reviewer** — Detect mispronunciation, missing words, artificial delivery, unsuitable emotion, inconsistent voices, awkward pauses, and script/audio mismatches.
15. **Cost & Regeneration Optimizer** — Cache approved audio, regenerate only affected segments, and minimize paid synthesis costs.

Determine which existing Skills can be reused and which require custom development.

### 3. Create a Consistent ExamLeaf Voice Personality

Develop the **ExamLeaf Super Teacher Voice Identity**:

- Highly intelligent but never intimidating.
- Energetic without shouting.
- Funny without forced comedy.
- Confident without arrogance.
- Friendly without sounding childish.
- Emotionally expressive without artificial enthusiasm.
- Simple enough for students with weak fundamentals.
- Serious and precise when explaining examinations, formulas, and calculations.

Research optimal speaking rates, vocal variation, pauses, pronunciation, conversational rhythm, and listening comfort.

### 4. Emotionally Intelligent Narration

Define voice-delivery rules for different teaching situations:

- **Introducing a mystery:** Curious, playful, slightly suspenseful.
- **Explaining a difficult concept:** Calm, clear, reassuring.
- **Revealing an answer:** Excited, satisfying, confident.
- **Teaching formulas:** Precise, measured, with intentional emphasis.
- **Making jokes:** Naturally playful, with appropriate comedic timing.
- **Asking students questions:** Inviting and genuinely interactive.
- **Correcting mistakes:** Supportive, never humiliating.
- **Celebrating understanding:** Warm and enthusiastic without exaggerated praise.
- **Explaining exam strategies:** Focused, credible, and motivating.

Do not use one emotional tone throughout the entire lesson.

### 5. Advanced Interactive Narration

Research how to incorporate age-appropriate Dora-inspired interactive teaching into Class 10–12 lessons.

Examples:

- "Okay, your turn. What do you think happens next?"
- "Before I reveal the answer, try this yourself."
- "Got it? Beautiful. Now watch what happens when we change this value."
- "Pause here and write down this formula. We'll use it in the next question."
- "See? You just solved the first part. Now let's make it a little more interesting!"

Design intentional pauses, response windows, writing prompts, retrieval questions, and increasingly challenging examples.

Avoid predictable questions every few seconds. Interaction must serve learning rather than becoming repetitive.

### 6. Narration-to-Animation Integration

Create a structured narration format containing:

- Spoken dialogue.
- Emotional direction.
- Voice identity.
- Pacing and emphasis.
- Pronunciation overrides.
- Pauses and interaction cues.
- Expected visual elements.
- Animation synchronization markers.
- Scene transitions.
- Educational objectives.

Keep directing metadata separate from spoken text and convert it into whichever format the selected TTS provider supports.

Use forced alignment and accurate audio timing to synchronize narration, formula highlights, visual reveals, and animations.

Where possible, adjust animation timing to natural narration rather than forcing speech into rigid scene lengths.

### 7. Complete Automated Narration Pipeline

**Academic Content → Human-Like Script → Teaching Psychology Review → Humour & Storytelling → Emotional Voice Direction → Pronunciation Validation → TTS Generation → Speech Alignment → Audio QA → Animation Synchronization → Final Mastering.**

Implement automatic checks for missing words, inaccurate scientific pronunciation, awkward phrasing, inconsistent delivery, clipped audio, excessive silence, unnatural intonation, and incorrect synchronization.

Require human listening tests before approving the main ExamLeaf voice.

### 8. Compare Narration Production Methods

Benchmark:

- Premium commercial TTS.
- Open-source self-hosted TTS.
- Human-recorded narration.
- Human-performed narration enhanced by speech-to-speech AI.
- Hybrid approaches using a human performance reference and consistent licensed synthetic voice.

For each method, evaluate realism, expressiveness, consistency, costs, scalability, language support, and quality-control requirements.

Use only appropriately licensed or consented voices and voice samples.

### Required Deliverables

Provide:

1. Complete public narration Skills directory.
2. Recommended voice-generation technology stack.
3. Custom Claude narration Skills architecture and implementation specifications.
4. ExamLeaf Super Teacher Voice & Personality Guide.
5. Scriptwriting, voice-direction, and emotional-delivery templates.
6. Structured narration data format and TTS integration strategy.
7. Full pronunciation, timing, and audio QA pipeline.
8. Cost comparisons for 1, 100, and 1,000 ten-minute videos.
9. Working example showing the same academic explanation as boring textbook narration versus outstanding human-like teaching, including voice directions and animation cues.
10. An implementation roadmap for integrating the complete narration system into ExamLeaf Video Engine.

**Ultimate Goal:** Produce narration so natural, captivating, understandable, funny, and encouraging that students feel they are learning directly from an exceptional human teacher—not listening to generated speech.

Prioritize **authentic teaching, scientific accuracy, real understanding, memorable explanations, emotional connection, and genuine student confidence** over artificial excitement or unnecessary theatrical delivery.


=====================================================================
MESSAGE id=ef490fbf-33df-4096-bbce-8080977095a4 role=assistant content_type=text create_time=1791910794.693964 chars=45047
=====================================================================

# ExamLeaf Narration System  
## Research, voice direction, production architecture, and implementation starter

**Build narration as a dedicated production system—not as the last step of video generation.**

The recommended approach is:

> **Approved academic explanation → conversational teaching script → performance direction → context-aware pronunciation → segmented speech generation → independent transcription and listening checks → alignment → animation timing → mastering → final approval.**

For ExamLeaf, I recommend **one consistent lead voice per language**, premium commercial speech generation initially, and **selective human-performed reference passages** for difficult humour, emotional transitions, or particularly important explanations.

Do not make every lesson a two-character conversation. The student’s thinking should provide the interaction; a second synthetic character is usually unnecessary.

### Deliverables created

[**Download the narration implementation, 15 custom Skills, templates, pronunciation library, and tests**](sandbox:/mnt/data/ExamLeaf_Narration_System.zip)

[**Download the editable narration cost model**](sandbox:/mnt/data/ExamLeaf_Narration_Cost_Model.xlsx)

[**Read the Super Teacher Voice Identity Guide**](sandbox:/mnt/data/ExamLeaf_Narration_System/docs/Voice_Identity_Guide.md)

[**Read the Public Narration Skills and Tools Directory**](sandbox:/mnt/data/ExamLeaf_Narration_System/research/Public_Narration_Directory.md)

### What was actually implemented and tested

| Item | Status |
|---|---|
| Structured narration contracts and provider-request compiler | Implemented locally |
| Fifteen dedicated ExamLeaf narration Skills | Written, with evaluation cases; **not agent-evaluated** |
| Forty explicit English STEM pronunciation mappings | Included; **not acoustically approved** |
| Sample-accurate timeline, protected thinking pauses, and animation markers | Implemented and tested |
| Cache invalidation, transcript comparison, signal analysis, and two-pass mastering | Implemented within the starter |
| Local tests | **57 passed** |
| Actual voice demonstrations | **Two speech auditions generated through your connected Runway account**, using 18 workspace credits |
| Local processing of those generated voices | Not completed; the audio assets were not transferred into this runtime |
| Local speech-quality or pronunciation benchmark | **Not performed** |
| Local audio fixtures | Real WAV test files, explicitly labelled **NOT SPEECH** |
| Complete production service | Not yet: authenticated synthesis transport, actual ASR/alignment execution, and authenticated approval remain to be integrated |

The two generated auditions compare textbook-style wording with a more interactive teaching rendition using the same requested voice, model, and speed. **They differ in wording, length, and expressive instructions, so they are demonstrations—not a controlled A/B experiment.**

Research was checked on **13 October 2026**. Pricing, model lifecycle, documented capabilities, original design recommendations, and local test results are distinguished below.

---

# 1. The decisive technology recommendation

## Recommended launch stack

| Layer | Recommended choice | Why |
|---|---|---|
| Script and teaching direction | Custom ExamLeaf Skills through Claude Code/Codex | Your personality, scientific constraints, and teaching progression should remain provider-independent |
| Primary expressive TTS candidate | **Eleven v4** | Strong candidate for directed, expressive narration and a consistent voice identity |
| Main alternative to audition | **Gemini 3.8 Flash TTS** | Explicit separation of spoken text and performance metadata; broad language coverage and attractive published pricing |
| Additional challenger | **Cartesia Sonic 3.6** | Particularly worth testing for conversational Indian English/Hindi and production efficiency |
| Human-performance path | Consented human recording, optionally converted to a licensed target voice | Preserves a deliberately performed rhythm where text prompting is insufficient |
| Independent transcription | A separately evaluated ASR model/provider | Helps detect omissions, additions, wrong numbers, and substituted terms |
| Alignment | ElevenLabs alignment initially; WhisperX/MFA where language resources are suitable | Align accepted speech with the approved transcript |
| Audio processing | FFmpeg + SoundFile + NumPy/SciPy | Reproducible audio assembly, measurement, mastering, and export |
| Playback timing | Sample-index narration timeline passed to existing scene adapters | Animations follow actual speech instead of forcing speech into rigid scenes |
| Release | Academic/native-language listening plus full-video review | Automated checks cannot certify teacher quality or every pronunciation |

**This is a ranked implementation recommendation, not a claim that I have listened to and benchmarked all three commercial models.**

The choice of final voice should follow a controlled audition. A marginally cheaper API is not a saving when it produces substantially more pronunciation repairs or reviewer work.

---

# 2. Current commercial voice technologies

## 2.1 ElevenLabs: first production candidate, with model-specific controls

Eleven v4 is the current expressive candidate. Current documentation also lists Assamese and Hindi coverage in the relevant newer model families. That resolves an important uncertainty from earlier generic language-support discussions, but **documented support is not proof of native-quality pronunciation for your curriculum**. citeturn569163search0turn391053search7turn391053search12

For ExamLeaf:

**Use TTS** for most approved script segments.

**Use speech-to-speech** when a performer can deliver a passage more effectively than a text instruction can.

**Use voice isolation** only when a recording genuinely needs cleanup.

**Use dubbing cautiously** for exploratory localization. Final Hindi or Assamese lessons should retain explicit control over scientific wording, conditions, notation, and timing.

### Important control changes

Do not copy old ElevenLabs settings into a new model blindly. The inspected v4 guidance differs from older models: **SSML and legacy speed/style controls are not interchangeable across the family**. Dictionary phoneme support likewise does not imply universal SSML support. citeturn569163search0turn145960search0

The starter therefore uses an explicit model-specific request recipe rather than a generic payload containing every setting.

**Keep the original teaching direction even when a provider cannot represent it exactly.** The adapter should report that limitation, not silently discard it.

## 2.2 Cartesia Sonic: strong challenger, not automatically the cheapest accepted audio

Cartesia has an official Skills repository covering its raw APIs, SDKs, and optional MCP tooling. Its `cartesia-api` Skill is relevant here; `line-voice-agent` is primarily aimed at interactive voice-agent applications rather than prerecorded lessons. citeturn676449view1

Sonic 3.6 is the current marketed generation, including multilingual/code-switching use cases. However, the request contract I could directly inspect in detail used a documented Sonic 3.5 snapshot. **The bundled recipe is labelled accordingly; I did not rename it “3.6” and imply that it was tested.** citeturn901218search3turn637231view2

Recommended role:

> Audition Sonic against the other shortlisted engines using identical Indian-English and Hindi passages, then compare **accepted output cost**, not advertised latency alone.

Assamese is **not admitted by the Cartesia contract in this starter**. Do not substitute Bengali or assume that a broad multilingual claim covers the intended language.

## 2.3 Gemini TTS: particularly promising for directed multilingual narration

The current Gemini 3.8 TTS interface separates **verbatim spoken text** from turn-level delivery instructions in `speech_metadata.style`. It also supports point-in-time vocal events. This maps well to an ExamLeaf narration format with separate dialogue and directing metadata. citeturn280214search0

Both Gemini 3.8 Flash TTS and Flash-Lite list **Assamese and Hindi**. Native review is still mandatory, particularly for scientific names, numbers, borrowed terminology, and code-switch boundaries. citeturn280214search7

### Two implementation details that matter

**Audio format:** current unary output is a complete WAV file; streaming output commonly uses raw PCM. Do not prepend a second WAV header or concatenate complete WAV containers as though they were raw samples.

**Voice lifecycle:** custom voice identifiers have documented storage and expiry limits. A brand voice needs a renewal/version policy, not just a voice ID stored indefinitely. citeturn280214search0

**Recommended role:** main commercial alternative, especially for multilingual expansion and cost-sensitive bulk production.

## 2.4 OpenAI speech: a migration issue must be handled now

The current official deprecation notice schedules `tts-1`, `tts-1-hd`, and the listed `gpt-4o-mini-tts` snapshots for removal on **6 January 2027**. It names **`gpt-realtime-2.1-mini`** as the recommended replacement. Older guides and public Skills still contain legacy examples. citeturn280214search1

Therefore:

**Do not start a new ExamLeaf catalogue on an old TTS snapshot merely because a Skill still uses it.**

The replacement is a realtime model with a different integration context. Its documentation lists text and audio pricing, but it should not be treated as a proven drop-in prerecorded-narration replacement without an exact-script audition and endpoint test. citeturn391053search0

The supplied OpenAI recipe is consequently an **offline migration fixture**. The code blocks it for new production.

## 2.5 Language support versus voice suitability

| Candidate | English/Indian-English assessment | Hindi/Hinglish | Assamese |
|---|---|---|---|
| Eleven v4 | Audition the actual voice, not just the model | Documented language support; test code-switching | Documented; native audition required |
| Gemini 3.8 TTS | Explicit style/accent direction available; test outcome | Documented | Documented |
| Cartesia Sonic | Worth auditioning for conversational delivery | Worth testing; model-specific controls matter | Not verified/admitted here |
| OpenAI replacement route | Requires new exact-script benchmark | Requires locale-specific testing | Not admitted by this starter |
| Human narration | Depends on the actual performer | Native/competent performer available | Native performer offers the clearest control route |

The documentation supports the language coverage, **not the comparative naturalness ranking**. citeturn391053search12turn280214search7turn901218search3

---

# 3. Open-source and self-hosted options

“Open-source TTS” is not one category. Code, pretrained weights, voice references, and commercial permissions must be checked separately.

| Project | Recommended ExamLeaf role | Important boundary |
|---|---|---|
| **Chatterbox** | First self-hosted expressive English/Hindi challenger | MIT project; select the correct multilingual model rather than assuming every variant has identical language support |
| **Indic Parler TTS** | Important self-hosted Assamese/Hindi audition candidate | Model card explicitly covers Indian languages, including Assamese; native quality still needs testing |
| **Kokoro 82M** | Lightweight preview or cost experiment | Apache-2.0 model; do not assume the exact release covers every requested Indian language |
| **CosyVoice** | Secondary research candidate | Inspected language coverage does not make it an automatic Hindi/Assamese solution |
| **Qwen3-TTS** | Additional expressive/voice-control candidate | Verify the exact release’s language coverage and weight licence |
| **Fish Speech** | Research or separately licensed commercial candidate | Current repository uses a **FISH AUDIO RESEARCH LICENSE**; do not treat the “open source” label as unrestricted commercial permission |
| **F5-TTS** | Useful research and architecture reference | MIT code and **non-commercial pretrained-weight terms** are separate |

Chatterbox, Indic Parler, and Kokoro are the most relevant first self-hosted investigations for this project. Fish and F5 require particular licensing care. citeturn676449view2turn676449view3turn565458view7turn676449view4turn676449view5

CosyVoice and Qwen3-TTS remain useful alternatives, but should not expand the deployment stack without a demonstrated language or quality advantage. citeturn858572view5turn145960view2

### My self-hosting verdict

**Do not self-host first solely to save the TTS API fee.**

Start self-hosting when one of these is demonstrated:

- A tested model provides a better required language or voice.
- Privacy/offline requirements justify it.
- Real usage exceeds the complete hosting, maintenance, and QA cost.
- Vendor independence is valuable enough to fund the engineering.

The supplied package does **not** include pretrained weights or claim that a neural TTS model was run locally.

---

# 4. Public narration Skills and integrations

The downloadable directory covers **28 repositories, APIs, model families, and audio tools**, classified by their actual function.

## Recommended reuse

| Resource | What to reuse | What not to assume |
|---|---|---|
| **ElevenLabs Skills** | `text-to-speech`, `speech-to-text`, `voice-changer`, `voice-isolator`, selective dubbing | A Skill installation does not approve a voice or establish scientific pronunciation |
| **ElevenLabs MCP** | Supervised auditions and asset operations | MCP is not a permission sandbox or durable production queue |
| **Cartesia Skills** | `cartesia-api` | A conversational-agent platform is not necessary for prerecorded lessons |
| **Cartesia MCP** | Optional development/audition interface | Production should still have controlled SDK/API workers |
| **Remotion Skills** | Audio timing, captions, rendering, multimedia guidance | Remotion composes audio; it is not itself a speech model |
| **Manim Voiceover** | Voiceover/bookmark synchronization patterns | Its service adapters do not validate the scientific narration |
| **Anthropic Skill Creator** | Trigger tests, functional evaluations, regression cases | A polished `SKILL.md` is not evidence of effectiveness |
| **OpenAI speech Skill** | Selected CLI and workflow patterns | Its model defaults require lifecycle review |

The official ElevenLabs repository currently provides ten relevant product Skills and documents both Python and JavaScript SDK usage. Its JavaScript guidance distinguishes the current scoped package from an outdated package name. citeturn676449view0

Cartesia explicitly distinguishes its Skills, documentation, SDKs, and optional MCP interface. That separation should remain intact in ExamLeaf’s architecture. citeturn676449view1

### Installation policy

Before enabling a public Skill:

> Confirm origin → inspect scripts and permissions → review licences → pin the selected revision → test in isolation → enable only the needed components.

Do not run unreviewed shell installers, install entire collections indiscriminately, or give a script-writing agent unrestricted synthesis and publishing credentials.

For bulk narration, use **SDK/API workers with explicit budgets and persistent job records**. Use MCP primarily for supervised development and auditions.

---

# 5. The fifteen custom narration Skills

These are authored in the starter pack. Each contains a `SKILL.md`, handoff template, references, and positive/negative evaluation cases.

They are **fifteen capabilities—not fifteen mandatory LLM calls for every segment**.

| Skill | Input → output | Essential safeguard |
|---|---|---|
| **1. Super Teacher Scriptwriter** | Approved claims and answer key → conversational lesson | Preserve conditions and prerequisites |
| **2. Human Dialogue Naturalizer** | Draft → minimal spoken-language revision | Do not remove qualifiers, negations, or exact quantities |
| **3. Educational Storytelling** | Concept → story/analogy card | Specify the mapping and where it breaks |
| **4. Humour & Meme Director** | Teaching beat → optional relevant humour | Zero jokes is acceptable; never ridicule students |
| **5. Student Psychology Director** | Lesson sequence → confidence/scaffolding audit | Confidence must follow evidence of competence |
| **6. Interactive Teaching Director** | Objectives → predictions, attempts, pauses, feedback | Hide answers and allow adequate response time |
| **7. Voice Acting Director** | Approved text → delivery metadata | One dominant intention per segment |
| **8. Narration Pacing Controller** | Complexity and audio timing → pace/hold plan | Never rush a formula to fit an arbitrary slot |
| **9. STEM Pronunciation Specialist** | Terms and expressions → contextual speech forms | No blanket symbol replacement |
| **10. Multilingual Language Director** | Approved meaning → locale-specific narration | Preserve science and examination terminology |
| **11. TTS Provider Adapter** | Canonical narration → model-specific request | Reject unsupported controls and deprecated models |
| **12. Speech-to-Animation Synchronizer** | Accepted audio/alignment → sample/frame events | Timing comes from the actual accepted take |
| **13. Audio Production Engineer** | Raw audio → measured master | Preserve intentional silence and intelligible consonants |
| **14. Narration Quality Reviewer** | Script, audio evidence, visuals → defect report | ASR or alignment alone cannot approve pronunciation |
| **15. Cost & Regeneration Optimizer** | Changes, jobs, cache → smallest repair plan | Do not regenerate unrelated approved segments |

### How they integrate with the existing engine

The package includes a mapping to the earlier ExamLeaf Skills so you do not create competing owners for the same task.

For example:

**Existing Super Teacher workflow** delegates naturalization and delivery preparation to these Skills.

**Existing scientific reviewer** remains the authority for the explanation and answer key.

**Existing renderer** receives measured narration events.

**Existing release workflow** requires audio-specific approval evidence rather than trusting the narration agent’s own conclusion.

---

# 6. ExamLeaf’s voice identity

## The defining brief

> **A highly competent teacher who is warm toward the learner, precise about the science, and occasionally amused by the problem.**

The voice should sound interested—not constantly excited.

### Recommended personality rules

**Intelligence appears through explanation.**

> “The equation is useful here because we know these two quantities.”

**Warmth appears through repair.**

> “Your relationship is correct. Recheck the substitution rather than restarting.”

**Humour appears through a relevant observation.**

> “Changing the substance would be a very efficient way to answer a different question.”

**Confidence appears through a check.**

> “The counts match on both sides. That is the evidence supporting your answer.”

Do not manufacture intelligence by using difficult vocabulary, warmth through fake intimacy, or humanity through random “ums,” breaths, and laughter.

## Emotional delivery by teaching situation

The following are proposed performance directions, not universal psychological prescriptions.

| Situation | Delivery | Example |
|---|---|---|
| Introducing a mystery | Curious, modest anticipation | “These graphs look similar. Which difference changes the answer?” |
| Difficult explanation | Steady, unhurried, reassuring | “There are two counts here. Let’s keep them separate.” |
| Revealing the answer | Brief satisfaction, then explanation | “Four. Here is why.” |
| Formula or condition | Deliberate emphasis | “This conclusion holds **when the temperature stays constant**.” |
| Joke | Slightly amused, no forced laugh | “A shortcut to the wrong question.” |
| Student question | Inviting, then genuinely quiet | “Choose a direction before we reveal it.” |
| Correcting an error | Specific and matter-of-fact | “You counted atoms correctly; now account for the pair in each molecule.” |
| Recognizing progress | Conditional, evidence-based | “If you selected that relationship without the example, you completed the key step.” |
| Examination strategy | Focused, credible | “Write the relationship before substituting, then include the unit.” |

Research does not establish that maximum enthusiasm is optimal. A 2024 multimedia study found context-dependent effects of vocal enthusiasm and visual cues rather than a simple additive benefit from intensifying both. citeturn719963search0

---

# 7. Pacing and teenage-appropriate interaction

## 7.1 Starting voice targets

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

These are **ExamLeaf starting specifications to test**. They should not be represented as neuroscientifically optimal rates.

Also distinguish **active speaking rate** from total lesson rate. A ten-minute lesson containing silence and practice instructions should not be scripted as ten uninterrupted minutes of speech.

## 7.2 Dora-inspired structure without childish delivery

Use:

> **Specific question → opportunity to attempt → explanation → targeted repair → fresh attempt.**

Avoid predictable questions after every sentence.

A suitable initial pattern is **three or four brief checks and two or three substantial attempts** in a ten-minute lesson. Place them at meaningful reasoning boundaries, not at a fixed attention-reset timer.

Retrieval practice has strong classroom support, but that evidence does not establish a universal question interval. citeturn719963search1

### Improve the user’s sample phrases

| Original approach | Stronger ExamLeaf version |
|---|---|
| “Got it? Beautiful.” | “Check it with the next example.” |
| “You just solved the first part!” | “If your result matches, check that you used this relationship.” |
| “What happens next?” | “At the same voltage, what happens to current when resistance doubles?” |
| “Pause and write the formula.” | “Pause, write the formula and the condition under which we are using it.” |
| “Now let’s make it interesting.” | “Now the diagram changes, but the underlying relationship is the same.” |

A prerecorded voice cannot know what an unseen student answered. **Never pretend it heard them.**

---

# 8. Script example: textbook reading versus teaching

The scientific target is the distinction between a coefficient and a subscript in a chemical equation. Changing coefficients adjusts quantities; changing the specified formula changes the chemical representation. citeturn676449view5

*The citation above concerns the tool project rather than chemistry and should not be used to establish the chemistry claim; the complete example’s scientific source is recorded in the downloadable script.*

## Textbook version

> “A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms.”

This is clear factual narration. It is not necessarily badly voiced. Its weakness is that it provides little help in constructing or testing the learner’s understanding.

## ExamLeaf version

**CURIOUS**

> “Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.”

*Show two intact water molecules. Keep totals hidden. Insert six seconds of actual silence after the question audio ends.*

**DELIBERATE**

> “Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules—not what a molecule is.”

*Reveal the hydrogen count when it is spoken. Highlight the coefficient when it is named.*

**LIGHT**

> “Changing water into hydrogen peroxide would be a very efficient way to answer a different question.”

*Show the rejected change separately and clearly label it.*

**FOCUSED**

> “Keep the given formulas fixed. Use coefficients to change the counts.”

**REASSURING**

> “Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.”

*Allow a learner-controlled pause. Do not treat the short media hold as a deadline.*

**FOCUSED**

> “Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.”

[**Read the full before-and-after example and directions**](sandbox:/mnt/data/ExamLeaf_Narration_System/examples/Before_After.md)

### Why this version is more useful

The proposed script separates counts, creates a genuine attempt, explains the error, and checks a new case. The humour reinforces the identity-versus-quantity distinction.

Its value should be measured through the next independent question—not simply whether students preferred the voice.

---

# 9. Structured narration format

Keep directing instructions out of canonical spoken text. The provider adapter decides what can safely become a model-specific control.

The included plan contains a voice identity, version, locale, rights record, source-claim manifest, lexicon version, and an ordered set of segments.

### One segment from the implemented schema

```yaml
segment_id: question
objective_id: count_atoms
claim_ids:
  - water-composition

text_template: >
  Two water molecules. How many hydrogen atoms altogether?
  Count each complete molecule before you answer.

direction:
  mode: curious
  target_wpm: 140
  emphasis:
    - each complete molecule

pause_after:
  kind: think
  seconds: 6
  prompt: Count hydrogen atoms in two separate water molecules.

expected_visuals:
  - Two water molecules; label elements, not totals.

critical_phrases:
  - Two water molecules
  - hydrogen

cues:
  - cue_id: show_molecules
    phrase: Two water molecules
    action: show
    element_id: molecule-pair
```

The answer segment declares `answers_after: question`. Its answer-reveal events cannot precede the protected response window.

## Provider translation strategy

**ElevenLabs:** map supported delivery cues into the selected model’s actual controls. Preserve unsupported detailed direction for the reviewer.

**Cartesia:** use its actual versioned request fields. A speed multiplier is a heuristic, not an exact words-per-minute guarantee.

**Gemini:** pass exact dialogue separately from `speech_metadata.style`.

**OpenAI:** keep the deprecated request only for migration inspection; implement and test the replacement separately.

**Human performance:** export the same segment text and direction as a recording sheet.

This separation allows a voice provider to change without rewriting the lesson’s educational structure.

---

# 10. STEM pronunciation system

## 10.1 Do not send raw formulas and hope

Maintain at least four representations:

**Scientific meaning → displayed notation → intended spoken form → accepted audio realization.**

Example:

| Display | Context-dependent spoken form |
|---|---|
| \(I=neAv_d\) | “Current magnitude equals number density times elementary charge times cross-sectional area times drift-speed magnitude.” |
| \(mA\) | “milliamperes” |
| \(MA\) | “megaamperes” |
| \(10^{-3}\) | “ten to the power minus three” |
| \(x^{-2}\) | “x to the power minus two” |
| \(\sin^{-1}x\) | “inverse sine of x,” where that notation is intended |
| \(1/\sin x\) | “one divided by sine x” |
| \(Na^+\) | “sodium ion with a positive charge,” or the shorter approved form |
| \(5'\rightarrow3'\) | “five-prime to three-prime” |
| \(\Delta G\) | “delta G,” with the meaning introduced separately |

These are **contextual authoring examples**, not one universal pronunciation dictionary.

The included library uses explicit identifiers such as `{{water_formula}}` rather than replacing every occurrence of a short symbol in arbitrary text.

## 10.2 What the dictionary must record

Each entry should contain:

**Subject, meaning, display form, locale, spoken form, allowed variants, model-specific phoneme/alias override, reviewer status, and accepted audio reference.**

Critical distinctions include:

- Molarity versus molality.
- Milli versus mega.
- Minus signs, charges, exponents, and reciprocals.
- “Increase” versus “decrease.”
- “Not,” “only,” “provided that,” and other conditions.
- Biological directions and counts.
- Similar-sounding scientific names.

Do not automatically use English phonetic spelling as the final Assamese or Hindi representation.

## 10.3 Pronunciation overrides are model-specific

An IPA string, phoneme dictionary, alias dictionary, and SSML tag are not interchangeable mechanisms. ElevenLabs documents different pronunciation options across models; the adapter must verify what the selected endpoint actually accepts. citeturn145960search0turn145960search10

For ExamLeaf, **an explicit spoken alias is the portable baseline**. Use provider phoneme features only after a successful acoustic test.

---

# 11. Exact synchronization and audio QA

## 11.1 The correct sequence

```text
Accepted narration text
        ↓
Generate coherent sentence groups
        ↓
Save raw audio and provider usage
        ↓
Independent ASR and critical-term review
        ↓
Accept or repair the take
        ↓
Forced alignment to accepted speech
        ↓
Resolve semantic animation markers
        ↓
Insert protected thinking/writing pauses
        ↓
Compose captions and visual events
        ↓
Master, encode, re-measure and review
```

Do not begin by estimating that every sentence needs eight seconds.

## 11.2 ASR and forced alignment answer different questions

**ASR asks:** “What does another system think was spoken?”

**Forced alignment asks:** “Where does the supplied text fit in this audio?”

A forced aligner can attempt to place expected words even when the performance is imperfect. ASR can also normalize a mispronunciation into the intended term.

Therefore:

> **Zero word error rate and a successful alignment do not prove correct STEM pronunciation.**

WhisperX documents language-resource requirements and limitations involving some numbers and symbols. Montreal Forced Aligner likewise relies on appropriate dictionaries and acoustic models. citeturn565458view2turn145960view4

For independent Assamese transcription, Gemini’s current transcription documentation lists Assamese and word-level timestamps. That is a relevant candidate, not an integration tested in this package. citeturn280214search3

## 11.3 Timing should be sample-based

At 48 kHz:

\[
6\text{ seconds}=288{,}000\text{ samples}
\]

The starter inserts those samples explicitly. It does not ask the TTS engine to “pause for exactly six seconds.”

Store animation events against the accepted audio’s sample positions, then convert once to output-frame time. Avoid repeated floating-point rounding or independent sentence-duration estimates.

Repeated phrases need an explicit occurrence index. “Highlight when the word ‘current’ is spoken” is ambiguous when it appears four times.

## 11.4 QA layers

| Layer | Automated checks | Human responsibility |
|---|---|---|
| Text | Missing conditions, unresolved terms, forbidden metadata in dialogue | Scientific meaning and natural teaching |
| Transcript | Added/omitted words, critical numbers and phrases | Ambiguous pronunciation and ASR mistakes |
| Signal | Clipping, DC offset, duration, unexpected silence | Audible distortion, joins, fatigue |
| Voice consistency | Flag unusual rate, level, or speaker changes | Judge acceptable performance variation |
| Alignment | Word order, monotonic timestamps, audio/transcript hashes | Inspect difficult anchors |
| Interaction | Answer hidden until response window ends | Confirm the task is fair and meaningful |
| Captions | Timing and text checks | Readability and accurate meaning |
| Final video | Automated defect report | Listen/watch the whole result |

Pitch tracks or model-generated “naturalness scores” may help triage. They should not automatically reject a voice because of accent or approve a lesson because it scores highly.

## 11.5 Mastering standards

Proposed ExamLeaf starting target:

**48 kHz mono, 24-bit archival WAV; approximately −16 LUFS integrated; true peak no higher than −1 dBTP.**

This is an **internal production target**, not a universal platform requirement. FFmpeg supports two-pass loudness processing, but the final encoded delivery should be measured again. citeturn552538search0

Avoid processing clean synthetic speech as though it were a noisy location recording. Excessive denoising can damage consonants; removing all breaths can sound unnatural.

Keep background music **off during the main explanation initially**. Add music or sound effects only when their contribution survives a comprehension and listening-effort comparison.

---

# 12. Human performance, speech-to-speech, and voice consistency

## 12.1 Best use of a human reference

Commission a performer to record a small **performance reference corpus**:

**A calm explanation, prediction, difficult formula, understated joke, supportive correction, and confident recap.**

This gives directors and reviewers a concrete standard. It does not necessarily need to become a cloned voice.

There are two different uses:

**Performance reference:** demonstrates rhythm and intention.

**Identity reference:** creates or conditions a voice resembling that speaker.

The latter requires specific permission and the provider’s applicable verification process. Consent to record a lesson should not be silently treated as consent to create an indefinitely reusable synthetic identity. ElevenLabs’ professional-cloning workflow, for example, has explicit verification requirements. citeturn391053search12

## 12.2 When speech-to-speech is worthwhile

Use it for passages where the actor’s performance makes a material difference: a dry joke, difficult multilingual transition, careful contrast, or unusually subtle reassurance.

It is less compelling for every ordinary explanatory sentence.

Speech-to-speech can transfer performance into a target voice, but it does not automatically fix wrong science, missing words, or an incorrect pronunciation in the input. The official ElevenLabs Skill describes it as voice transformation—not an academic correction system. citeturn676449view0

## 12.3 Protect consistency without making delivery flat

Version the voice profile, pronunciation dictionary, reference passages, model, settings, and accepted samples.

Keep a “golden set” of difficult passages. Re-run it before model upgrades.

Do not silently replace a voice when a provider fails. A fallback must be an approved voice/model combination, or the job should wait.

A voice identity can be consistent while moving between curiosity, precision, amusement, and reassurance. Consistency is not identical pitch and rhythm on every sentence.

---

# 13. Costs for 1, 100, and 1,000 ten-minute videos

## 13.1 Scope and assumptions

These estimates cover the **narration subsystem**, including script-direction allowance, synthesis, audio QA, editing, and the modeled human work.

They do **not** include full academic research, animation production, platform marketing, or audience streaming. Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget.

All values are **USD before tax**, using one monthly accounting period.

### Baseline inputs

| Input | Assumption |
|---|---:|
| Finished media length | 10 minutes |
| Active speech | 8.5 minutes |
| Transcript length | 7,800 characters |
| Generation/retry allowance | 20% |
| LLM narration editing/direction | $0.60/video |
| ASR/alignment/automatic QA allowance | $0.08/video |
| Storage/export allowance | $0.05/video |
| Academic audio reviewer | $20/hour |
| Audio editor | $15/hour |
| Performer | $30/recording hour |
| Illustrative GPU cost | $0.80/hour |
| Self-hosted real-time factor | 2 compute seconds per generated audio second |

Personnel rates, processing times, retry rate, and GPU figures are **editable planning assumptions, not quotations or measured TTS benchmarks**.

## 13.2 Provider generation costs

The reference commercial calculation uses **$0.10 per 1,000 characters**, a published v2/v3 rate—not an invented Eleven v4 price. With 20% regeneration:

\[
7{,}800\times1.2/1{,}000\times\$0.10=\$0.936
\]

The published speech-to-speech reference is **$0.12 per generated minute**, before separate performer and review costs. citeturn500117search4

Gemini 3.8 Flash TTS currently lists **$0.50/million input tokens and $9/million audio output tokens**, with scheduled increases to **$1 and $18 from 1 January 2027**. Its pricing specifies 25 audio tokens per second. Under the workbook’s workload, synthesis is approximately **$0.139 now** or **$0.278 at the scheduled rate**, before QA and labour. citeturn500117search0

Cartesia’s plans list **$5/100,000 credits, $49/1.25 million, and $299/8 million**. At 9,360 generated characters per lesson, 100 lessons fit within 1.25 million credits, but 1,000 lessons require 9.36 million—beyond the 8-million allowance. Obtain the actual overage or higher-tier quote rather than extrapolating a false fixed price. citeturn500117search2

## 13.3 Five production methods

| Method | Variable cost/video | Monthly fixed allowance | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|---:|---:|
| **Premium commercial TTS** | **$12.50** | $100 | **$112.50** | **$1,349.93** | **$12,599.33** |
| Primarily self-hosted | $14.75 | $300 | $314.75 | $1,775.20 | $15,052.00 |
| Human recorded | $42.40 | $100 | $142.40 | $4,339.67 | $42,496.67 |
| Human performance + speech-to-speech | $34.87 | $125 | $159.87 | $3,612.07 | $34,995.67 |
| Hybrid: 80% TTS, 20% performed/converted | $17.06 | $150 | $167.06 | $1,855.69 | $17,206.93 |

The table assumes different review/editing workloads for each method. **It does not prove that self-hosting inherently costs more.** At equal labour requirements, it can be cheaper; actual retakes and maintenance decide the result.

### The dominant cost

The premium case allows **25 minutes of academic audio review and ten minutes of editing per video**. At 1,000 videos, that is approximately **583 human hours**.

Reducing generation from roughly one dollar to a few cents matters less than eliminating avoidable pronunciation and synchronization repairs.

An illustrative **$4,000 initial narration-subsystem implementation reserve** is separate. Voice buyouts, broader licences, substantial new localization, and hardware purchases require additional budgeting.

---

# 14. Benchmark the voice before making it the brand

Run three separate studies.

## A. Voice/provider audition

Use identical passages, normalized playback levels, blinded provider names, and rotated order.

Include connected explanations—not only isolated impressive sentences.

The corpus should cover numbers, units, negation, scientific conditions, formula reading, Indian names, code-switching, a question, a correction, and a restrained joke.

Use native teachers and language editors to identify **meaning-changing defects**, and students to rate clarity, listening effort, warmth, dignity, and preference.

## B. Script-style comparison

Hold the science and study opportunity comparable. Compare a straightforward explanation with the Super Teacher version.

The two Runway demonstrations produced here are useful for discussion, but **not** sufficient for a causal conclusion because several variables changed together.

## C. Learning evaluation

Measure an independent question immediately and a fresh question later.

Do not use preference, voice similarity, completion rate, or apparent confidence as the primary learning outcome.

Use short listening panels first to find obvious problems, then a properly designed study for claims about learning effectiveness. A small panel is not enough to establish a modest examination-performance advantage.

---

# 15. Integration roadmap and operating instructions

## Repository structure

```text
ExamLeaf_Narration_System/
├── src/examleaf_narration/
│   ├── contracts.py
│   ├── pronunciation.py
│   ├── compiler.py
│   ├── cache.py
│   ├── timeline.py
│   ├── qa.py
│   └── cli.py
├── skills/                  # 15 custom Skill drafts
├── configs/                 # Voice/provider/lexicon contracts
├── examples/                # Textbook and teacher versions
├── tests/
├── outputs/                 # Reports and NOT-SPEECH fixtures
├── research/
├── docs/
└── ExamLeaf_Narration_Cost_Model.xlsx
```

## Run the local starter

```bash
python -m venv .venv
# Activate the environment for your operating system.

python -m pip install -e '.[test]'

PYTHONPATH=src python scripts/build_examples.py
PYTHONPATH=src pytest -q

PYTHONPATH=src python -m examleaf_narration.cli validate \
  examples/teacher.json

PYTHONPATH=src python -m examleaf_narration.cli compile \
  examples/teacher.json \
  --lexicon configs/pronunciation.json \
  --profile configs/gemini_38.json \
  --out outputs/request_preview.json
```

The compile command creates request JSON and sends **zero network requests**. Provider IDs and environment markers are templates, not credentials.

The release check intentionally blocks the supplied fixtures:

```bash
PYTHONPATH=src python -m examleaf_narration.cli release-check \
  outputs/timeline.json
```

Do not bypass that result with fabricated reviewer identities.

## Practical six-week sequence

| Phase | Build | Completion gate |
|---|---|---|
| **Week 1** | Voice casting, language-specific corpus, rights records | Approved primary voice per required locale |
| **Week 2** | One live provider transport, usage records, limits, recovery | Successful controlled synthesis and failure tests |
| **Week 3** | Independent ASR, actual alignment, critical-term checks | Manually verified timing and pronunciation samples |
| **Week 4** | Integrate with existing renderer; complete four subject pilots | Full academic/native-language/listening approval |
| **Weeks 5–6** | Controlled 20–30-lesson batch, dashboard and queue | Predictable accepted-output cost and defect rate |

The current starter completes portions of the contracts, timing, caching, request compilation, and signal QA. It does not substitute synthetic test timestamps for real alignment or claim that the fifteen Skills have already operated as autonomous agents.

---

## Final recommendation

**Launch with commercially generated narration, a carefully cast and licensed voice, explicit pronunciation control, and selective human performance where it genuinely improves the teaching.**

Keep self-hosted models as measured alternatives, not mandatory infrastructure. Keep the voice provider replaceable, but the approved teaching language, terminology, timing, and academic standards under ExamLeaf’s control.

**The strongest ExamLeaf voice will not be the one that sounds most excited. It will be the one that makes a difficult step understandable, gives the student time to attempt it, and responds with a useful explanation rather than a manufactured celebration.**

---

Here's a quick summary of the conversation:

The conversation focuses on designing a scalable, AI-powered video production system named ExamLeaf for Class 10 and 12 STEM subjects. It discusses selecting a well-integrated technology stack—including HyperFrames, Manim, and FFmpeg—while emphasizing scientific rigor, reusable components, and clear licensing distinctions. The conversation also details a comprehensive approach to narration incorporating effective voice selection, emotional direction, synchronization with animations, and human oversight to enhance student engagement and understanding.

Key recommendations include starting with HyperFrames for composition, using Claude Code/Codex for automation of scripts and production, and prioritizing scientific validation and psychological research to optimize learning and confidence. Additionally, narration technologies such as ElevenLabs and Cartesia Sonic are evaluated, with a structured pipeline ensuring quality, naturalness, and alignment with educational goals.




Tab Context:
- Executed on tabId: seed
- Available tabs:
  • tabId seed: "AI Video System Research" ("https://chatgpt.com/share/6acf03ec-b480-83ee-a000-3701059934d9")