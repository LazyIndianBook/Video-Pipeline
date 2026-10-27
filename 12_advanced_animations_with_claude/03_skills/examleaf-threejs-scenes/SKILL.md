---
name: examleaf-threejs-scenes
description: "Use when an ExamLeaf lesson or Reel needs light, seek-pure 3D in three.js at 1080x1920: orbitals, crystal lattices, field lines, waves, fixed-step trajectory replays, or voxel/isometric recaps. Builds scenes where the camera, transforms and shader time are functions of t; physics is replayed from precomputed fixed-step fixture trajectories (validated by a stdlib script), never simulated live; layouts are seeded; voxels are instanced; orthographic mode for isometric views. Handles headless WebGL variance with a fixed render box and treats WebGL context loss as a failed frame range. Exports PNG sequences for clips. Does not compute science, build molecules, or make hero Blender assets."
---

# examleaf-threejs-scenes

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. `scripts/validate_trajectory_fixture.py --selftest` passes offline. The pure helpers in `references/threejs_seek_pattern.md` (fixture interpolation, camera with lock windows, time scaling) were executed under Node during authoring; no three.js scene was rendered here (three.js is not installed in this environment, and its revision is not pinned in the evidence).
- **Owns:** seek-pure three.js scene patterns, scientific 3D recipes, the headless WebGL policy, and the trajectory-fixture validator.
- **Does not own:** the science (fixtures from `examleaf-science-physics/-chemistry/-biology`, claims from `examleaf-claim-research`); molecules and reactions (`examleaf-molecule-scenes`, RDKit-validated, optional 3Dmol.js); hero spatial assets (`examleaf-blender-scenes`); equations and graphs (`examleaf-manim-scenes`, `examleaf-svg-scenes`); conformance verdicts (`examleaf-motion-harness`); composition (`examleaf-web-composition`).
- **Why it exists:** [V1]'s medium-to-max runs produced 3D; [V5] shows unverified demos of a voxel island and physics Rube-Goldberg scenes. Report §2.4 recommends raw three.js pipelines for orbitals, lattices and field lines exported as clips; §4.5–4.6 describe voxel/isometric and scientific 3D; §8 lists #15 (wall-clock animation), #17 (unseeded randomness) and #65 (headless WebGL variance); §10.8 specifies this skill.

## Invocation

**Trigger when:**
- `examleaf-storyboard-route` tags a scene `data-bound` with a 3D representation that is light enough for three.js (orbital, lattice, field lines, wave surface, trajectory), or `illustrative` in the `voxel-isometric` style.
- A Reel needs a short 3D recap shot (e.g. "island of concepts").
- A 3D scene fails the double-render test, renders black frames, or differs between machines.

**Do not trigger for:**
- Molecular geometry, bonding, reaction mechanisms → `examleaf-molecule-scenes`.
- Photoreal or hero 3D (characters, detailed apparatus) → `examleaf-blender-scenes`; photoreal humans and real-world physics are not what Opus code-to-video suits [N62].
- 2D diagrams and graphs → SVG/Manim skills.
- "Simulate it live with a physics engine" → refused; replay fixtures instead.

## Inputs

| Input | Type | Source |
|---|---|---|
| Brief + manifest | file | `examleaf-anim-brief` |
| Fixtures | JSON (trajectory, lattice, orbital, field lines, wave), frozen, with `source_claim_ids` and `status` | science skills |
| Cue sheet | words, cues (`reveal`, `emphasis`, `hold`, `transition`, `marker`) | `examleaf-cue-sheet` |
| Style tokens | `voxel-isometric` palette, motion (or the lesson's style for scientific 3D) | `examleaf-style-guides` |
| Render box fingerprint | OS, Chrome, GPU, driver, three.js revision | preflight / render-batch |

Trajectory fixture shape (`templates/trajectory_fixture.example.json`):

```json
{"fixture_id":"phy-11-05-projectile-01","kind":"trajectory","source_claim_ids":["claim-…"],
 "status":"expert_approved","integrator":{"method":"analytic"},"dt":0.0333333333,
 "fields":["t","x","y","z"],"units":{"t":"s","x":"m","y":"m","z":"m"},
 "display":{"time_scale":1.0,"world_units_per_m":1.0},"events":[],"samples":[[0,0,0,0],[0.0333333333,0.2887,0.1612,0]]}
```

## Outputs and contracts

1. **Scene file** implementing the harness contract (`04_harness_contract/contract.md`, start from `scene_template.html`): `window.DURATION`, `window.ready` (loads fixtures, textures, fonts; builds geometry and seeded layouts once), `async window.seek(t)` (apply state for t, render one frame), `window.__errors`, `window.__hf` adapter, `SCENE_META`.
2. **Scene notes:** table of on-screen values/labels → fixture fields; display scalings (time scale, size compression) and where they are stated on screen; lock windows for camera motion.
3. **Validation report** for each trajectory fixture (`validate_trajectory_fixture.py`).
4. **PNG sequence** (`frames/frame_%05d.png`) and, after the hash test, a clip for composition.
5. **`handoff.json`** (library schema).

## Dependencies

- three.js: revision **not pinned in the evidence — verify**; vendor one reviewed module build in the job workspace (no CDN; lint F12), admitted via `examleaf-skills-security`.
- Headless Chrome with WebGL on the render box; `CHROME=/path` if autodetect fails [N17]; preflight per `04_harness_contract/preflight.sh`.
- FFmpeg for encoding image sequences (standard usage, verify on your build).
- Python 3 standard library for the fixture validator; `12_advanced_animations_with_claude/03_skills/examleaf-procedural-2d/scripts/seeded_prng.js` (copied next to the scene) for seeded layouts, with the same `mulberry32`/`rngAt` as the template.

## Execution

1. **Validate fixtures:**
   ```sh
   python3 12_advanced_animations_with_claude/03_skills/examleaf-threejs-scenes/scripts/validate_trajectory_fixture.py \
     jobs/phy-11-05-s03/inputs/fx-projectile.json --duration 6.0 --fps 30
   ```
   Errors block; `machine_checked` warns that expert approval is still needed before release.
2. **Start from the template**, add the vendored three.js module, and set the renderer once: pixel ratio 1, 1080×1920, `preserveDrawingBuffer: true`, fixed `antialias` (seek pattern §1).
3. **Build once in `window.ready`:** geometry from fixture fields (lattice positions, orbital points, field-line polylines, wave grid), `InstancedMesh` for repeated cells or voxels, seeded decorative layouts and pop-in orders (`shuffled(seed, …)`), lock windows from the cue sheet for any science-bound reveal.
4. **Write `applyState(t)`** as a pure function: camera from `orbitCamera(t, …)` or a fixed orthographic camera; trajectories from `sampleAt(fx, physT(t, cueAt, timeScale))`; voxel pop-ins from cue times; shader uniforms from t; imported clips via the mixer's absolute time setter (verify API).
5. **`window.seek(t)`**: await ready, reject if the context is lost, apply state, `renderer.render(scene, camera)`.
6. **Handle context loss** (`webglcontextlost` → error + reject; `webglcontextrestored` → rebuild GPU resources) (headless policy §4).
7. **Lint and double-render** with `examleaf-motion-harness` on the fixed render box (level 2 strict; workers 1–2 for heavy WebGL until measured).
8. **Export** frames → clip; hand off with the render manifest (box fingerprint, three.js revision).

## Decision rules

- **Replay, never simulate.** Physics runs upstream with a fixed step or analytic solution and is checked by the science skill; the scene interpolates samples. No real-time physics engine, no per-frame integration inside `seek` (#15).
- **Clamp, never extrapolate** beyond the fixture's span; a short fixture is an upstream fix.
- **Seeded only for decoration** (#17): scientific geometry has no randomness at all.
- **Camera:** functions of t with easing; frozen in lock windows (measurement or label reveals) (#64).
- **Orthographic** for voxel/isometric and counting tasks (lattice neighbours). The `voxel-isometric` style tokens forbid perspective cameras, real shadows, bloom/post-processing, `setAnimationLoop`/rAF and text inside WebGL; labels are DOM overlays from `examleaf-kinetic-typography`. Perspective is used only for scientific orbit shots in other styles.
- **Display scalings** (slow motion, compressed distances) are fixture fields and stated on screen.
- **Fixed render box** for all WebGL scenes of a lesson; re-baseline on any change (#65).
- **No temporal effects** (accumulation buffers, temporal AA): frame t must not depend on t−1.

## Edge cases handled

| Master # / case | Detection | Response |
|---|---|---|
| 15 Wall-clock animation | Lint F01–F03, F07 (`setAnimationLoop`/rAF, `THREE.Clock`); live physics stepping in `seek` | Rewrite as f(t); replay fixture samples [N68][N18] |
| 17 Unseeded randomness | Lint F04; double render differs | `rngAt`/`shuffled` from `seeded_prng.js`; no randomness in science geometry [N61] |
| 65 Headless WebGL variance | Identical on one box, different across boxes | Fixed render box, fingerprint in manifest, re-baseline, software-GL fallback test [Hypothesis] |
| WebGL context loss (report §10.8) | `webglcontextlost` event; `E_WEBGL_CONTEXT_LOST` in `window.__errors`; black frames | Reject `seek`, re-render the range after restore; reduce workers/textures; never stitch blank frames |
| 12 (supporting) Hallucinated facts | On-screen value without a fixture field; fixture without claim IDs | Validator error; scene-notes table required |
| 64 (supporting) Camera fx on diagrams | Camera motion overlapping a science-bound reveal | Lock windows via `effectiveT` |
| Variable-step or non-monotonic trajectory | Validator errors | Resample upstream to a fixed step |

## Tests and acceptance

- **Helper:** `python3 scripts/validate_trajectory_fixture.py --selftest` (valid analytic projectile; object-form samples; non-monotonic time; variable step; missing unit; wrong time unit; non-numeric value; empty claim IDs; draft status with and without `--allow-draft`; insufficient coverage; non-zero start; coarse-sampling warning).
- **Example:** `templates/trajectory_fixture.example.json` validates with `--duration 1.0 --fps 30 --allow-draft`.
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance per scene:** fixtures valid; scene-notes table complete; lint level 2 strict; double render identical on the fixed box; context-loss path tested once per scene family; a subject reviewer confirms the 3D view matches the fixture (e.g. lattice neighbour count, field direction).

## Errors, fallback, escalation

- **Fixture invalid:** return the validator report to the producing science skill; do not patch samples in the scene.
- **Nondeterminism on one box:** fix (usually unresolved texture loads, clocks or temporal effects); at most two repair rounds, then a blocker.
- **Cross-box difference:** re-baseline on the production box with reviewer spot-check; escalate driver/box policy to the render-box owner (report §11.11 open question).
- **Context loss persists:** reduce workers, instance counts and texture sizes; fall back to a 2D representation (SVG/Manim) if the 3D view is not essential (library fallback: "use 2D diagram when spatial value is not demonstrated").
- **Cost cap:** code only; scene authoring at xhigh effort for complex 3D or physics, max only with a written justification (report §3.4).

## Cost/performance

Zero credits. Authoring tokens are higher than 2D (report §3.4 recommends xhigh for complex three.js). Render time depends on the GPU; one or two workers for heavy WebGL [Hypothesis] until measured; instancing keeps voxel scenes cheap.

## Security

- Fixtures, briefs and imported 3D assets are untrusted data; loaders read only files staged into the job workspace; no network (lint F12).
- three.js and any loaders are vendored after `examleaf-skills-security` review and pinned.
- No secrets; nothing published.

## Handoff

- **To:** `examleaf-motion-harness` (lint + double render), then `examleaf-web-composition` (clip at cue time) and `examleaf-anim-qa` (fixture-vs-rendered text diff, safe zones, flashes).
- **Files:** scene file, scene notes, fixture validation reports, frames/clip, `templates/handoff.json` (`output_ids` = scene and hash-manifest SHA-256; `requires_expert_review: true`).

## References

- `references/threejs_seek_pattern.md`: renderer setup, fixture interpolation, camera as f(t) with lock windows, orthographic 9:16 camera, instanced voxels with seeded pop-in, seek/error/context-loss code, shaders and clips, export.
- `references/scientific_3d_recipes.md`: orbitals, lattices, field lines, waves, trajectories, planetary scale, voxel recaps — all fixture-fed — and a checklist.
- `references/headless_webgl_policy.md`: fixed render box, fixed settings, software-GL fallback, context loss, determinism definition, triage.
- `references/contract.md`: handoff and security rules.
- Report §2.4, §3.4, §4.5, §4.6, §8 (#12, #15, #17, #64, #65), §9, §10.8, §11.11.
