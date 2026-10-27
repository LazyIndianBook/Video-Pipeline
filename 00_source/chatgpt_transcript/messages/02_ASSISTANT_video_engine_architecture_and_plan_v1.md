<!-- source: ChatGPT share 6acf03ec-b480-83ee-a000-3701059934d9 | message 1b0f1ac0-7679-407c-8ab4-f06647a77c51 | 1b0f1ac0-7679-407c-8ab4-f06647a77c51 role=assistant content_type=text create_time=1791873358.957302 chars=48051 -->

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
