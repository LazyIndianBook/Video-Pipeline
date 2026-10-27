# FULL TEXT — Video Engine v2: Architecture, Verified Research and Working Prototype (ChatGPT message 10)

> **Provenance.** Cleaned full-text copy of the ChatGPT message `10_ASSISTANT_video_engine_implementation_v2.md` (raw, untouched original: `../00_source/chatgpt_transcript/messages/10_ASSISTANT_video_engine_implementation_v2.md`).
> Original header: `source: ChatGPT share 6acf03ec-b480-83ee-a000-3701059934d9 | message 91516339-0f60-4e45-b1ef-5a24d6a68871 | 91516339-0f60-4e45-b1ef-5a24d6a68871 role=assistant content_type=text create_time=1791906572.643237 chars=43768`
>
> **What was cleaned (formatting artefacts only):** 30 opaque inline citation markers (`cite…turn…` / `filecite…` tokens, which point to ChatGPT's internal browsing session and cannot be resolved) were removed; LaTeX delimiters `\[ \]` / `\( \)` were converted to `$$ $$` / `$ $` so they render in Markdown; `sandbox:/mnt/data/...` download links (dead outside ChatGPT) were re-pointed to the local copies in this folder — the original sandbox path for each is listed at the end of this file. Every heading, paragraph, table, number, formula and code block is otherwise unchanged and in original order.

---

# ExamLeaf Video Engine: recommended architecture, verified research, and working prototype

**Build ExamLeaf around verified scientific models and reusable teaching components—not around a general-purpose “generate a complete video” prompt.**

My recommendation is:

> **Python scientific validation → structured lesson and scene specifications → HyperFrames as the production compositor candidate → selective Manim/Three.js/Blender inserts → independently generated narration → measured synchronization → FFmpeg export → academic and production approval.**

Use **Higgsfield and other generative-media services selectively** for illustrations, visual exploration, and packaging. Do not make them responsible for equations, reaction mechanisms, chromosome counts, circuit behaviour, or other scientific assertions.

I have also created an initial implementation rather than stopping at the architecture.

## Deliverables

[**Download the implementation repository, research directory, 32 custom Skill drafts, and eight rendered previews**](implementation_v2/)

[**Download the editable production-cost model**](implementation_v2/ExamLeaf_Video_Engine_Cost_Model.xlsx)

[**Read the implementation README**](implementation_v2/README.md)

[**Read the Public Skills and Integrations Directory**](implementation_v2/research/Public_Skills_Directory.md)

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

The linked Higgsfield article combines topic selection, scripting, narration, video generation, dubbing, thumbnails, Shorts, and a publishing plan. That is useful as an example of **workflow packaging**. Its revenue and growth claims are marketing claims—not evidence that the same process will produce scientifically accurate lessons or ExamLeaf sales. I did not independently audition its embedded example videos.

The important question is not whether one prompt can start many jobs. It is whether the resulting jobs produce correct, reusable, reviewable educational content.

## 1.2 The inspected explainer Skill is more specific than the blog

The live `higgsfield-video-explainer` Skill I inspected was **v0.13.0**. Its documented process uses a shared style reference, short narration blocks, separately generated audio, approximately ten-second generated video clips, and provider-side assembly. Its duration convention implies **60 ten-second blocks for a ten-minute video**. This differs from treating the entire lesson as one monolithic generation request.

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

The public generation guidance exposes a “Virality Predictor” capability. I did not find evidence establishing its calibration for student understanding, examination performance, or ExamLeaf conversion. Its name should not be interpreted as a neurological measurement.

## 1.3 Its integration surfaces are not interchangeable

| Surface | Actual role | Integration implication |
|---|---|---|
| **Skill** | Instructions telling an agent how to perform a workflow | Does not itself supply rendering or scientific verification |
| **CLI** | Executable interface for account, model, and generation operations | Needs installation, authentication, version pinning, and command-level controls |
| **MCP server** | Exposes provider tools to an agent | Needs approved account access, permissions, and spending controls |
| **Developer API** | Programmatic service interface | Requires confirmed endpoint access, credentials, and separate billing assumptions |
| **Web platform** | Hosted interface, workflows, plans, and credits | A web subscription does not establish unlimited API/MCP capacity |

Higgsfield documents its CLI, MCP connection, and separate API offering. Its web “Unlimited” arrangements should not be assumed to apply to MCP/CLI workflows. **I did not obtain a verified, authenticated all-in price for a ten-minute Higgsfield explainer.** That remains a required account-level estimate, not a number to invent from a subscription headline.

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

The live Remotion README listed twelve Skills; the ElevenLabs README listed ten. The ElevenLabs documentation also identifies its current Python package, JavaScript package, CLI, and API-key environment variable. These are separate from whether a particular voice is appropriate for ExamLeaf.

### Important licensing distinction

Anthropic’s repository does **not** apply one unrestricted open-source licence to everything. Its document Skills are source-available under separate terms. Likewise, an open-source Skill or bridge does not grant commercial rights to every voice, model weight, imported asset, or hosted service it invokes.

## 2.2 Additional resources worth selecting

**HyperFrames:** reuse the core composition, animation, keyframe, audio, and CLI guidance. Its live manifest and cached README did not agree on the number of available Skills, illustrating why production should pin inspected files rather than depend on a remembered marketplace count.

**Community Manim Skills:** the `adithya-s-k/manim_skill` repository is a useful candidate for Manim Community guidance. Do not mix its Manim Community and ManimGL instructions. Some runtime guidance can lag current official requirements; I did not execute its claimed tests.

**K-Dense scientific-agent-skills:** selectively consult SymPy, RDKit, Biopython, and scientific-visualization instructions. Do not install the entire scientific stack or treat package guidance as an academic reviewer.

**Skills.sh, MCP registries, and Claude plugin marketplaces:** use them for discovery, then return to the publisher’s repository and actual package. A listing, install count, or badge is not a complete security audit.

## 2.3 Blender MCP deserves special caution

The renamed project is a **community bridge, not an official Blender Foundation integration**. It can execute Python inside Blender. Its documented local bridge and arbitrary-code capabilities require meaningful isolation, not merely a reassuring Skill prompt.

The current README distinguishes **opt-in content telemetry** from **minimal anonymous usage telemetry enabled by default**. `DISABLE_TELEMETRY=true` disables telemetry. This is more precise than saying either “all telemetry is on” or “nothing is collected.”

**Production decision:** use MCP, when necessary, on an isolated authoring workstation. Render approved assets through pinned, headless Blender scripts—not an unrestricted live agent session.

## 2.4 Safe installation process

Do not run public `curl | bash` installers or install every discovered Skill.

Use this admission process:

> Confirm publisher → inspect repository and scripts → review licences and permissions → pin a real commit/package digest → test in isolation → copy only approved components → re-audit upgrades.

An inspected **file blob SHA is not a commit SHA**. The directory preserves this distinction.

For ExamLeaf’s original Skills, copy only the relevant folders into the client’s supported Skill directory. Claude Code and Codex support Skill-based workflows, but their discovery, invocation, and permission behaviour should be checked against current documentation.

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

HyperFrames documents HTML-based, seekable rendering through a browser and FFmpeg under Apache-2.0. Manim Community and Motion Canvas provide different specialist animation approaches. These documentation findings establish their intended capabilities—not a benchmark victory for ExamLeaf.

Remotion’s current automation pricing includes **$0.01 per billable render with a $100 monthly minimum when the paid licence applies**. Confirm organizational eligibility and what counts as a render; a finished lesson can involve multiple rendering operations.

**Decision:** begin the production comparison with HyperFrames. Switch to Remotion when measured developer productivity, reliability, or repair time makes it the better total-cost choice.

Do not decide from licence price alone.

## 3.2 Subject-specific libraries and boundaries

| Subject | Recommended libraries/modules | What they should control | What they do not prove |
|---|---|---|---|
| **Physics** | SymPy physics/vector/mechanics; SciPy `solve_ivp`; Pint; Schemdraw; selective Magpylib | Equations, trajectories, units, circuit drawings, selected magnetic fields | That the chosen model matches every real system |
| **Chemistry** | RDKit `Chem`, `AddHs`, `rdDepictor`, `rdMolDraw2D`, `rdChemReactions`; selective 3Dmol.js | Molecular identity, atom counts, coordinates, approved reaction-state depictions | Reaction feasibility, correct mechanism, or required conditions |
| **Mathematics** | SymPy; KaTeX; SVG; Manim Community | Expressions, domains, graphs, symbolic checks, visible transformations | That an attractive transformation is a justified mathematical step |
| **Biology** | Approved layered SVG; explicit process-state tables; Biopython; Mol* where useful | Counts, sequence data, structure displays, process-state transitions | General anatomical or biological correctness |

The official documentation supports these package roles. In particular, Schemdraw is a drawing tool, Magpylib is not a general time-dependent Maxwell solver, and molecular viewers are not chemistry validators.

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

Runway publishes per-model credit rates; Pika publishes a separate developer pricing structure. These cannot be flattened into one universal “AI video cost per minute.”

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

[**Download/read the complete custom Skill inventory**](implementation_v2/research/custom_skills.csv)

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

Claude’s Skill and subagent mechanisms support this organization, but Skill instructions are not operating-system security controls or evidence that the autonomous workflow has passed evaluation.

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

Retrieval practice has strong classroom evidence, but that does not establish a universal interaction interval. Relevant humour can improve some social-emotional and motivational responses; the cited 2026 study does not establish examination-score gains.

## 7.2 Initial production targets—not universal scientific optima

For pilots, start with approximately **1,100–1,250 narration words**, ordinary English delivery around **130–155 active words per minute**, three or four brief predictions, and two or three learner-controlled practice pauses.

Use less animation when students need to inspect, write, or calculate.

Keep essential diagrams and quantities visible. Use colour consistently, but do not claim that particular HEX codes improve memory.

The proposed palette remains `#F7F9FC` background, `#14213D` text, `#185ABD` blue, and `#087986` teal. Check real adjacent colours, fine symbols, phone display sizes, and captions. WCAG’s normal-text contrast baseline is 4.5:1; meeting that alone does not establish complete accessibility.

## 7.3 Audio implementation

Keep separate fields for:

- Display equation.
- Spoken wording.
- Pronunciation guidance.
- Editorial delivery mode.
- Pedagogical silence.
- Visual reveal event.

Editorial modes such as **STEADY, CURIOUS, DELIBERATE, LIGHT, REASSURING** are not universal TTS syntax.

Generate short segments, measure the actual waveform, then align meaningful events. ElevenLabs offers a forced-alignment endpoint, but that integration is **not implemented in the supplied project**.

For future Assamese production, require a successful model-specific request and native review. A vendor’s broad language count is insufficient.

For self-hosted voice experiments, Kokoro’s model card is worth evaluating. F5-TTS illustrates why code and weight licences must be checked separately; its open code does not automatically make all pretrained weights suitable for commercial use.

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
| Physics | [RC charging](implementation_v2/outputs/physics_rc_16x9.mp4): initial condition, one time constant, KVL, numerical/analytical agreement | **27.338 s** | **28.102 s** |
| Chemistry | [Atom balancing](implementation_v2/outputs/chemistry_balance_16x9.mp4): specified molecular identities and atom counts | **28.670 s** | **29.375 s** |
| Mathematics | [Chain rule](implementation_v2/outputs/mathematics_chain_16x9.mp4): symbolic and finite-difference check for $(3x+1)^2$ | **27.372 s** | **27.576 s** |
| Biology | [Monohybrid cross](implementation_v2/outputs/biology_genetics_16x9.mp4): probabilities and complete-dominance assumption | **27.425 s** | **27.951 s** |

Each file is **30 seconds, 720 frames, 24 fps**, rendered at 1280×720 or 720×1280. Two jobs ran concurrently.

These timings are **not** a forecast for a fully narrated ten-minute lesson, complex 3D, or a browser compositor.

[**View the landscape contact sheet**](implementation_v2/outputs/technical_previews_contact_sheet.jpg)

[**View the vertical-layout contact sheet**](implementation_v2/outputs/vertical_review.jpg)

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

At the checked published rates, this gives approximately **$1.72 of LLM usage per lesson**. The token workloads are assumptions, not observations from the local proof.

Narration assumes 8,000 characters, 20% regeneration, and **$0.10 per 1,000 characters**, giving approximately **$0.96**. That tariff is from the checked ElevenLabs API page; the separate Runway audition used workspace credits and is not billed by this calculation.

The generated-video comparison uses an illustrative **$0.10/second provider route**, not a Higgsfield whole-lesson price. Exact requests may have additional model/input/resolution charges.

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

**Licences are tracked by component.** Blender’s software licence does not automatically impose that licence on rendered artwork, but imported models and assets retain their own obligations. GSAP likewise has its own standard licence rather than being assumed MIT because it is free to use in many contexts.

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

---

## Appendix: original sandbox link targets

| Original ChatGPT sandbox path | Local copy (relative to `04_video_engine/`) |
|---|---|
| `sandbox:/mnt/data/ExamLeaf_Video_Engine_Implementation.zip` | `implementation_v2/` |
| `sandbox:/mnt/data/ExamLeaf_Video_Engine_Cost_Model.xlsx` | `implementation_v2/ExamLeaf_Video_Engine_Cost_Model.xlsx` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/README.md` | `implementation_v2/README.md` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/research/Public_Skills_Directory.md` | `implementation_v2/research/Public_Skills_Directory.md` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/research/custom_skills.csv` | `implementation_v2/research/custom_skills.csv` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/physics_rc_16x9.mp4` | `implementation_v2/outputs/physics_rc_16x9.mp4` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/chemistry_balance_16x9.mp4` | `implementation_v2/outputs/chemistry_balance_16x9.mp4` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/mathematics_chain_16x9.mp4` | `implementation_v2/outputs/mathematics_chain_16x9.mp4` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/biology_genetics_16x9.mp4` | `implementation_v2/outputs/biology_genetics_16x9.mp4` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/technical_previews_contact_sheet.jpg` | `implementation_v2/outputs/technical_previews_contact_sheet.jpg` |
| `sandbox:/mnt/data/ExamLeaf_Engine_Implementation/outputs/vertical_review.jpg` | `implementation_v2/outputs/vertical_review.jpg` |
