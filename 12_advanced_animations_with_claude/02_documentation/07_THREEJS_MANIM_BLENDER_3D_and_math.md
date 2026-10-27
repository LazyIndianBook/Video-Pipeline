# 07 · three.js, Manim and Blender: 3D scenes and mathematical inserts

**Purpose.** When ExamLeaf uses three.js, Manim Community Edition (CE) or Blender; how each is made deterministic and fixture-bound; and how their clips enter the master timeline. Extends report §2.4–§2.6, §4.5–§4.6 and §6.2.

**Status.** [PROPOSED]. None of these renderers is installed or benchmarked in the project. `examleaf-manim-scenes` (P1) and `examleaf-blender-scenes` (P2) are "Proposed agent workflow; not model-evaluated" (`04_video_engine/SKILLS_INDEX_video_engine_32.md` §14, §16). The only tested renderer is the native SVG → CairoSVG → FFmpeg proof adapter (RD-07 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). three.js API names below come from general knowledge, not the verified evidence set: verify each against the pinned three.js version.

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [V#] videos, [N#] web evidence, project docs by ROOT-relative path, [Recommendation]/[Hypothesis] for judgement, #1–#65 master edge cases, NEW-# from `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

**Owning skills.** New: `12_advanced_animations_with_claude/03_skills/examleaf-threejs-scenes/`. Existing: `06_skills_library/custom_skills/video_engine/examleaf-manim-scenes/`, `06_skills_library/custom_skills/video_engine/examleaf-blender-scenes/`, `06_skills_library/custom_skills/video_engine/examleaf-svg-scenes/` (default), `06_skills_library/custom_skills/video_engine/examleaf-web-composition/` (master timeline). Contract: `12_advanced_animations_with_claude/04_harness_contract/contract.md`.

---

## 0. Summary

1. **SVG is the default** for every data-bound diagram. It is the only tested path (RD-07) and the regression reference.
2. **Manim CE** is the specialist for equation transformations and mathematical graphs where symbol correspondence matters. CE only; never ManimGL (#28).
3. **three.js** is for light 3D where depth carries meaning: orbitals, lattices, field lines, wave surfaces, and the voxel/isometric recap style. Every scene is a pure function of time, seeded and fixture-fed.
4. **Blender** is rare, opt-in (P2), scripted, seeded and rendered headless on an isolated workstation. A Blender MCP is an authoring aid only.
5. **All of them render to clips or PNG sequences** that `examleaf-web-composition` places in the HyperFrames master timeline (report §2.6 [Recommendation]).
6. **Accuracy invariant**: geometry, values and labels come from validated fixtures; the renderer only draws them. Text labels go in an SVG/DOM overlay, not baked into 3D textures, so QA can read them (NEW-17).

---

## 1. Decision rules: which renderer, and when

### 1.1 Router rules that already bind

`examleaf-storyboard-route` applies the scene router in `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S8 (verbatim rules 1–6). The ones that decide this document:
- Rule 1: "Equation, calculation, graph or model state: **deterministic only**."
- Rule 3: "Anatomy/spatial structure: licensed or reviewed model/SVG; **3D only if needed**."
- Rule 6: a failed scientific generative asset is replaced by a deterministic representation, "never regenerate until it merely looks plausible".
- Fallback: "Approved static SVG component before free-form generated animation."
- Library boundaries (S7): "3D is not automatically useful"; "Magpylib is not a Maxwell solver".

### 1.2 Decision procedure (ask in order; stop at the first "yes")

1. **Is the content a stable structure the learner must inspect, label or reproduce?** → static or stepwise **SVG** (`02_learning_psychology/INSTRUCTIONS_production_rules.md` E1: "Use a static diagram when the student must inspect structure, compare labels, calculate, or reproduce an exam diagram").
2. **Is it an equation transformation or a graph whose symbols must stay in correspondence?** → **Manim CE** insert, or SVG if an approved SVG template exists ("SVG fallback if it accurately represents the concept", `examleaf-manim-scenes` Errors).
3. **Does depth, rotation or 3D spatial relation carry the teaching point** (orbital lobes along axes, lattice coordination, field lines around a 3D magnet, a wave surface)? → **three.js** with an orthographic or fixed perspective camera.
4. **Is it a hero spatial asset that needs realistic lighting, complex topology or a licensed model** (and step 3 is not enough)? → **Blender**, opt-in, with written justification of spatial value.
5. **Is it decorative, narrative or a recap "island of concepts"?** → procedural 2D (`12_advanced_animations_with_claude/03_skills/examleaf-procedural-2d/`) or three.js voxel mode, under the `illustrative-narrative` route tag.

### 1.3 Comparison table

| Criterion | SVG (native / in harness) | Manim CE | three.js | Blender |
|---|---|---|---|---|
| Tested in project | **Yes** (4 bounded fixtures) | No (P1) | No (new) | No (P2) |
| Best for | Labelled diagrams, graphs, stepwise states | Equation transforms, plots, geometry | Orbitals, lattices, fields, waves, voxels | Rare hero spatial assets |
| Determinism | Frame from explicit `t` [TESTED] | Scripted [Hypothesis] | Seek-pure if contract followed [N72]; GPU variance (#65) | Scripted + seeded [Hypothesis]; GPU/CPU noise variance |
| Text/labels | Native, DOM/SVG-readable | Rendered glyphs (OCR to check) | Overlay in SVG/DOM [Recommendation] | Overlay in compositor |
| 9:16 (this layer: 1080×1920 only, AD-07) | Re-laid-out panels (`test_vertical_not_crop`) | Frame size in config (verify fields) | Canvas size | Render resolution |
| Install traps | Fonts, FFmpeg | CE vs GL (#28), ARM (#29), LaTeX (NEW-20) | Headless WebGL (#65), context loss (NEW-21) | Pinned Blender, MCP isolation |
| Cost | CPU, cheap | "Specialist render cost" | Browser + GPU | "High setup/render cost; opt-in only" |

---

## 2. three.js seek-pure scenes (`examleaf-threejs-scenes`)

### 2.1 The contract

Every verified harness seeks; none plays (report §2.1):
- "headless Chrome renders frame i as seek(i / fps)" [N18];
- HyperFrames "never calls play()" and exposes `window.__hf` [N68] (contested);
- the tutorial contract: set `window.DURATION` and expose `async window.seek(t)`; frame count = `DURATION × fps` [N72];
- rAF-based polling hangs because "rAF doesn't fire in beginFrame mode" [N69].

The binding version for ExamLeaf is `12_advanced_animations_with_claude/04_harness_contract/contract.md` with `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`. A three.js scene therefore:
1. builds its scene graph once at load (from fixtures and seed) and resolves `window.ready` only when geometry, textures and fonts are ready (contract §2.3);
2. on `seek(t)`, sets every transform, material parameter and camera pose from `t`;
3. calls `renderer.render(scene, camera)` once, synchronously, then resolves;
4. never runs an animation loop, never reads `Date.now()`/`performance.now()` for animation, never uses `Math.random()` (#15, #17, #19).

### 2.2 Outline (illustrative; the harness contract governs)

```js
// three.js scene outline — API names to verify against the pinned three.js version.
import * as THREE from "./vendor/three.module.js";        // vendored, never a CDN at render time
import { loadCueSheet, loadFixture, rngAt } from "./harness.js";   // template helpers; names: verify

const cues = await loadCueSheet("cue_sheet.json");
const fx   = Object.freeze(await loadFixture("fixtures/lattice_nacl.json")); // validated, deep-frozen (contract §9)
// Randomness: stateless rngAt(fx.seed, i) only; never a stateful stream inside seek (contract §4, #17)

window.DURATION = cues.duration;                               // [N72]
const W = 1080, H = 1920;                                      // vertical master
const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H);
const camera = new THREE.OrthographicCamera(-5.4, 5.4, 9.6, -9.6, 0.1, 100);
const scene  = buildLattice(fx, (i) => rngAt(fx.seed, i));      // geometry from fixture; jitter (if any) seeded

window.seek = async (t) => {                                   // pure function of t
  const u = cueProgress(cues, "rotate_lattice", t);            // 0..1 from cue sheet, clamped
  scene.rotation.y = fx.view.start_deg * Math.PI/180 + u * fx.view.sweep_rad;
  setCamera(camera, t, cues);                                  // camera = f(t)
  revealAtoms(scene, cues, t);                                 // visibility from cues, not timers
  renderer.render(scene, camera);
};
```

`antialias: false` and `setPixelRatio(1)` reduce cross-machine variance [Hypothesis]. `preserveDrawingBuffer: true` addresses blank captures of a WebGL canvas in some capture paths [Hypothesis, NEW-22]; test both settings on the render box.

### 2.3 Camera as a function of time

1. Read camera keyframes from the cue sheet (`cues[].kind = "camera"`) or from the brief.
2. Interpolate with a pure easing function of normalised progress `u ∈ [0,1]` (smoothstep or a cubic). Never "follow" an object with physics or damping that depends on previous frames.
3. **Freeze the camera during measurement and label reveals** (#64): no push-in, shake or orbit while a scale, angle or label must be read. The [V4-MP] slow push-in (scale 1 → about 1.03–1.04) is for illustrative scenes only.
4. Prefer orthographic cameras for lattices and voxels so sizes and angles are not distorted by perspective [Recommendation].

### 2.4 Fixed-step physics replay

Real-time physics breaks seek rendering (report §2.1: "no real-time physics stepping without a fixed-step replay").
1. **Simulate offline** at a fixed step `dt` (e.g. 1/240 s) from the seeded initial state — preferably in Python using the same validated science function the science Skill approved, so model and picture share one state (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S9: "Every simultaneous representation of the same system must consume the same verified state").
2. **Store** the trajectory as JSON or a binary array with its hash.
3. **At `seek(t)`**, index the sample at `t` (or interpolate between the two nearest samples). Never integrate forward from the previous frame.
4. **Model time is physical time.** "Never change a physical simulation's behaviour merely to satisfy an animation timing rule" (`02_learning_psychology/palette_and_typography_tokens.json` `physical_simulation_rule`). Label slow motion explicitly (`02_learning_psychology/INSTRUCTIONS_production_rules.md` E5 Physics).

### 2.5 Seeded layouts and instanced voxels

- **PRNG.** The template supplies `mulberry32` (a stateful stream, only for building precomputed data once, in a fixed order) and the stateless `rngAt(seed, i)` for anything evaluated inside `seek(t)` (`12_advanced_animations_with_claude/04_harness_contract/contract.md` §4 F04–F05). Key `i` by object ID so adding an object does not reshuffle the others [Recommendation].
- **Voxel/isometric mode** (report §4.5): instanced boxes (`InstancedMesh`), an orthographic camera, baked or simple lighting, seeded procedural layout. Use for the "island of concepts" recap and stylised lattices. Keep instance counts bounded; record peak GPU memory in the ledger (NEW-6).
- **Boil and idle motion** use stepped jitter `rngAt(seed, floor(t × boil_fps) · K + objectIndex)` with `boil_fps` 8–10 ([V4-MP] §8), so jitter is identical on every render and in any seek order.

### 2.6 Determinism and headless WebGL variance

| Risk | Control |
|---|---|
| Unseeded randomness (#17) | Lint for `Math.random`; seeded PRNG only |
| Wall-clock or rAF animation (#15, #19) | Lint; seek-only contract |
| GPU/driver differences (#65) | **One fixed render box** for 3D (RD-24: Linux render workers); record GPU, driver, Chrome version in the manifest |
| Software-GL fallback | Run a software-rendering test once per release of the render image [Hypothesis]; which software GL Chrome uses on the box must be verified |
| Antialiasing and float differences | Hash exactness for 2D; for 3D use exact hash on the same box plus a per-pixel tolerance comparison across boxes [Recommendation] |
| Context loss (NEW-21) | Listen for `webglcontextlost` and push an error-severity entry to `window.__errors`, which fails the render (contract §11 item 7) instead of emitting black frames; QA detects all-black or empty frames |
| Blank capture (NEW-22) | Test `preserveDrawingBuffer`; QA non-empty-frame check |

The double-render determinism check is `12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py` (procedure in `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` A3).

### 2.7 Export as a clip

Follow `12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` (rules in §1, three.js in §3.3):
1. Render each frame via `seek(i / fps)` to PNG (the harness captures; contract §11).
2. **Export a PNG sequence, not a video**: no decoder, frame-exact, and the master scene stays a pure function of `t`. PNG keeps alpha for overlays; H.264 yuv420p has none (NEW-15).
3. Write the clip manifest `clip.json` (import notes §2; extensions in §5.2 below) and a per-frame hash file via `determinism_hash_check.py --write-manifest`.
4. If an MP4 clip is unavoidable, the master scene declares `SCENE_META.workersMax = 1` because parallel seeking exhausts decoders [N70] (#20); re-encode intra-only for frame-accurate seeking (flags: verify; import notes §4.2).

### 2.8 Scientific uses, always from fixtures

| Topic (examples) | Fixture holds | Validator owner | Visual rules |
|---|---|---|---|
| Atomic orbitals (s, p, d shapes; Class 11) | Orbital type, axis orientation, nodal planes, lobe sign convention, isosurface level | `examleaf-science-chemistry` (new bounded template) | Lobes along the correct axes; signs/phases as the textbook draws them; label axes; state that shapes are probability boundaries, not orbits |
| Crystal lattices (e.g. NaCl unit cell) | Unit cell type, ion positions (fractional coords), coordination number, ion identities and colours | `examleaf-science-chemistry` | Same atom colour across scenes (`02_learning_psychology/INSTRUCTIONS_production_rules.md` D4); coordination count visible; orthographic |
| Magnetic/electric field lines | Source geometry (magnet poles, charges), line seeds, integration step | `examleaf-science-physics` | Direction arrows correct; density meaningful only if stated; "Magpylib is not a Maxwell solver" (S7) |
| Wave surfaces / standing waves | Amplitude, wavelength, frequency, phase, boundary conditions | `examleaf-science-physics` | Model time drives motion; label slow motion; axes and units visible |
| Molecular geometry | Approved structure inventory (atoms, bonds, angles) | `examleaf-science-chemistry`, `examleaf-molecule-scenes` | Atom identity maintained; no morph hiding a discontinuity (E5 Chemistry) |
| Cell organelles (stylised) | Approved diagram landmarks | `examleaf-science-biology`, `examleaf-biology-scenes` | Retain landmarks; label pending items; prefer 2D unless 3D adds value |

Each new topic is a **new bounded template** and must follow `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §9: science approved first; bounded validator with domain checks that raise; no `eval`/`sympify` of content strings; an independent cross-check; renderer computes displayed state from the same science function; both aspects re-laid out; tests before use. The SceneSpec subject↔kind mapping must first allow several kinds per subject (RD-35).

**Labels are not 3D geometry.** Render labels, values and units in an SVG or DOM overlay positioned from projected 3D coordinates. This keeps text crisp at phone size, readable by the DOM text-dump QA (#12), and in the house fonts (RD-23) [Recommendation].

---

## 3. Manim Community Edition (`examleaf-manim-scenes`)

### 3.1 Install and verify

1. Admit the package through `examleaf-skills-security` and `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §11 (pin a real version; isolated environment).
2. Install CE: `pip install manim`; verify with `manim --version` [N46]. Record the version in the manifest and the cache key.
3. **CE only.** "These are separate, incompatible frameworks" [N48] (#28). Code from ManimGL tutorials does not port. The existing skill's first step is "Choose CE-only component".
4. **ARM macOS:** ManimGL needs `arch -arm64 brew install pkg-config cairo` first [N47] (#29). CE's own native prerequisites on ARM are not in the evidence set; verify on the authoring Mac. Production renders run on Linux workers (RD-24).
5. **LaTeX.** `examleaf-manim-scenes` lists "LaTeX as needed". Equation objects that typeset through LaTeX fail if the TeX toolchain or a package is missing (NEW-20). Preflight must check it (verify which distribution and packages CE requires).
6. **Agent skill (optional):** `npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices` installs only the CE skill [N45]; the bare `npx skills add adithya-s-k/manim_skill` installs both CE and GL skills [N44] — do not use it. Security review first (report §10 "Third-party skills to evaluate").
7. **Test workers:** many parallel workers cause out-of-memory errors; use 4–6 [N49] (#30).

### 3.2 Vertical configuration

Manim CE's frame size and frame rate are configurable, but the exact option and config names were **not verified** (import notes §3.1 lists candidates such as `-r/--resolution` and `--fps` to verify). Render 1080×1920 at 30 fps: this layer is vertical only (AD-07 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`); a 16:9 insert is needed only while the runbook keeps a 16:9 lesson master (RD-16; conflict C1), and is then recomposed, not cropped. Keep Manim's logical frame proportions equal to the pixel aspect so circles stay circular, and verify the transparent/PNG output flags and whether alpha is straight or premultiplied.

### 3.3 Stable symbol IDs

The existing skill requires "Bind stable symbol IDs" and "Verify each transformation and units". Procedure [Recommendation]:
1. The fixture lists each symbol with an ID: `{"id":"sym_I","tex":"I","meaning":"current","unit":"A"}`.
2. The Manim scene builds equation objects from these IDs, never from free text.
3. Transformations map symbol IDs to symbol IDs (`I` in `V = IR` becomes `I` in `I = V/R`). The operation is shown ("divide both sides by R"), not R flying across the equals sign (`02_learning_psychology/INSTRUCTIONS_production_rules.md` E5 Mathematics).
4. The previous line is retained during the transformation (`02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md` beat 02:30–02:45).
5. QA compares rendered equations with the fixture by symbol ID (via a manifest the scene writes), then OCR or human check of the frame.

### 3.4 Timing from the cue sheet

- Every animation's start and run time come from `cue_sheet.json` (`12_advanced_animations_with_claude/02_documentation/06_AUDIO_compose_analyze_sync.md` §5). Waits fill gaps exactly.
- Total rendered frames must equal `duration × fps` of the cue sheet. A mismatch fails the clip manifest check (NEW-13).
- **Equation hold**: on screen until the narration finishes reading it plus 0.5 s (report §7.5) and at least 2–4 s after an important transformation (RD-02); take the longer.

### 3.5 Relation to manim-voiceover

A community plugin that couples Manim scenes to TTS voiceover is widely known as "manim-voiceover", but it is **not in the verified evidence set**. ExamLeaf must not use any plugin to *generate* narration, because the only voice path is `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter` (`12_advanced_animations_with_claude/02_documentation/06_AUDIO_compose_analyze_sync.md` §6). If evaluated at all, it may be considered only for reading timing from **already approved** audio — and the cue sheet already does that. Default: not used [Recommendation].

### 3.6 Output

Transparent or opaque insert plus manifest (existing skill outputs). For a transparent insert, keep an alpha-capable format (NEW-15). Hash the clip, record CE version, LaTeX distribution, fonts and fixture hash. Typography must match the rest of the lesson: if the composition uses KaTeX fonts (RD-23) and Manim uses a LaTeX font, equations look different between layers (NEW-19). Pick one math typeface per lesson and verify visually [Recommendation].

---

## 4. Blender (`examleaf-blender-scenes`)

### 4.1 What already binds

- P2, opt-in; "Pinned Blender; optional isolated MCP authoring"; steps: build from validated geometry/data → record units/camera → review topology/orientation → "Headless render approved script only"; tests: "No exposed MCP port; no production secrets; annotated turntable inspection"; fallback: "Use 2D diagram when spatial value is not demonstrated" (`04_video_engine/SKILLS_INDEX_video_engine_32.md` §16).
- Blender MCP: the renamed `mcp-for-blender` is third-party; "Arbitrary Python execution and a local TCP bridge require isolation. Do not expose the port, assume safe-mode is a full sandbox, or run with general cloud credentials"; "Set DISABLE_TELEMETRY=true to disable all telemetry"; "Production should render reviewed scripts headlessly, not run an unconstrained MCP conversation" (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §11).
- Report: [V3] shows Blender-MCP 3D motion graphics, but "no verified install or command evidence for a Blender MCP was collected" (§4.6, §6.2).

### 4.2 Procedure

1. **Justify spatial value** in the storyboard route record. If a 2D diagram or three.js covers it, stop.
2. **Author** a versioned Python script that builds the scene from the validated fixture (units in metres or stated units; camera position, focal length and target recorded). An MCP session may *draft* this script on an isolated workstation; the script, not the session, is the artefact.
3. **Seed everything:** procedural placement, noise textures and the renderer's sampling seed.
4. **Review** topology, orientation and scale with an annotated turntable (existing test).
5. **Render headless** on the pinned Blender build from the reviewed script only. The exact command line is not in the evidence set: use the form `<pinned-blender> --background <scene.blend> --python <render_scene.py>` and **verify flags** against the pinned version's documentation.
6. **Export** a PNG sequence or alpha-capable intermediate; hash; manifest.
7. **Determinism** [Hypothesis]: path-traced renders can differ between CPU and GPU devices and driver versions even with a fixed seed. Render on one fixed device type; compare with a tolerance; record device and version in the manifest.

### 4.3 Licences

Blender's software licence does not impose itself on rendered artwork, but imported models and assets keep their own obligations (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14). Every imported mesh, HDRI or texture gets an `AssetManifest` with licence and attribution; unconfirmed rights stay quarantined (NEW-7).

---

## 5. Integrating clips into the master timeline

### 5.1 Steps

1. **Render** the clip at the master fps (30) or an integer divisor, at 1080×1920 (or a declared inset size); its frame count equals `round(duration × fps)` of its window (import notes §1, §6.2). Never frame-rate-convert a rendered clip; re-render from the model.
2. **Write `clip.json`** (§5.2) and register the asset with `examleaf-asset-library` (`origin: deterministic`).
3. **Place** the clip with the portable mapping `clipFrame(t, clipStart, clipFps, nFrames)` (import notes §4.1): before start hide, after the end hold the last frame. `clipStart` comes from the master cue sheet (`cues[].at`), never hard-coded. A HyperFrames-native clip declaration is not in the evidence set (import notes §4.3: verify).
4. **Overlay** labels and values from fixtures in SVG/DOM (with `data-fx` attributes, contract §9) on top of the clip.
5. **Workers:** any scene importing MP4 clips declares `SCENE_META.workersMax = 1` [N70] (#20); PNG-sequence scenes may render in parallel.
6. **Colour:** clips and stills are sRGB 8-bit; convert RGB→YUV **once**, at the final H.264 yuv420p encode, tagged BT.709 with the correct range (FFmpeg options: verify) (import notes §6.1; NEW-5).
7. **Probe** the composed result: dimensions, frame count, codec, pixel format, audio stream (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.2).
8. **Hash PNG frames** before encoding for determinism, not the MP4 (contract §11; NEW-12).

### 5.2 Clip manifest

The manifest is `clip.json` as defined in `12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` §2 (`clip_id`, `kind`, `path`, `frames`, `fps`, `width`, `height`, `alpha`, `colour`, `producer{tool, version, command, seed}`, `fixture_sha256`, `frames_sha256_manifest`, `created`). For 3D and maths clips this document recommends three optional additions [Recommendation; add through the contract owner]:

```json
{
  "cue_sheet_sha256": "<sha256 of the cue sheet that timed the clip>",
  "render_box": {"os": "linux", "gpu": "<model>", "driver": "<version>", "browser": "<version>"},
  "science_review_status": "pending"
}
```

`render_box` matters for WebGL determinism (#65); `cue_sheet_sha256` detects a clip timed to stale narration (#63).

### 5.3 Who owns what

| Output | Owner |
|---|---|
| Fixture and validator | `examleaf-science-<subject>` |
| three.js clip | `examleaf-threejs-scenes` |
| Manim insert | `examleaf-manim-scenes` |
| Blender insert | `examleaf-blender-scenes` |
| SVG scene | `examleaf-svg-scenes` |
| Composition and placement | `examleaf-web-composition` (contract: `examleaf-motion-harness`) |
| Asset record | `examleaf-asset-library` |
| QA | `examleaf-anim-qa` → `examleaf-visual-qa` |

---

## 6. QA hooks specific to 3D and maths

Full gate list: `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`. Specific to this document:
1. **Contract lint** on three.js scenes (`12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js`).
2. **Double render + hash** on the same box; tolerance compare across boxes (#17, #65).
3. **Non-empty frame check** (NEW-21, NEW-22): no all-black or uniform frames unless the cue sheet marks them.
4. **Fixture-vs-render check:** overlay text by DOM dump; Manim equations by symbol manifest plus OCR or human check (#12).
5. **Geometry check** [Recommendation]: project fixture coordinates with the same camera and compare with rendered marker positions at sampled frames (e.g. ion centres, axis ends) within a pixel tolerance.
6. **Camera-freeze check** during measurement and label cues (#64).
7. **Frame count and fps** equal to the cue sheet (NEW-13).

---

## 7. Edge cases owned here

| # | Edge case | Section |
|---|---|---|
| #15 | Wall-clock animation | §2.1 |
| #17 | Unseeded randomness | §2.5, §2.6 |
| #19 | rAF polling hangs | §2.1 |
| #20 | Multiple video elements exhaust decoders | §2.7, §5.1 |
| #28 | Manim CE vs GL | §3.1 |
| #29 | ManimGL on ARM Mac | §3.1 |
| #30 | Manim parallel tests OOM | §3.1 |
| #52 | Photoreal request | §1.2 (route elsewhere or redesign; Opus "does not natively behave like a cinematic text-to-video model" [N62]) |
| #64 | Camera fx distort measurement | §2.3 |
| #65 | Headless WebGL variance | §2.6 |
| NEW-5, NEW-6, NEW-7, NEW-12, NEW-13, NEW-15, NEW-17, NEW-19, NEW-20, NEW-21, NEW-22 | See doc 12 | §2.5–§5.1 |

---

## 8. Open questions (verify)

1. three.js version, its WebGL capture behaviour in the chosen harness, and which software GL path headless Chrome uses on the Linux render box.
2. Manim CE version; exact vertical config fields; LaTeX packages required; ARM prerequisites for CE.
3. Clip intermediate codec with alpha that HyperFrames can seek reliably.
4. Blender version, headless command flags, device determinism.
5. Whether a Blender MCP is ever admitted (`examleaf-skills-security` record required).
6. Colour space and range convention across clips and delivery.
