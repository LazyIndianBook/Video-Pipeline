# Style guide: voxel-isometric (three.js voxel and isometric inserts, 9:16)

**Style ID:** `voxel-isometric` | **Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot
**Derived from:** report §4.5 (voxel and isometric 3D), the 3D runs in [V1], and the voxel-island demo shown in [V5]. [V5] is an unverified signal (third-party, leak-based): nothing here depends on it or on any specific model (#57). Skill that implements it: `examleaf-threejs-scenes`.
**Machine-readable twin:** `style_tokens.json` (`styles["voxel-isometric"]`).

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement; [Hypothesis] = untested; "verify" = not confirmed. Edge cases #1-#65 (report §8). Project decisions RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## Digest (read this first; the full guide governs on conflict)

1. three.js with an `InstancedMesh` of unit cubes, an orthographic camera at the true isometric angle, flat baked lighting. No real lights, no shadow maps, no perspective.
2. Voxel positions and species for anything scientific (lattices, organelle blocks) come from a fixture's integer grid. Seeded randomness is for decoration only.
3. Rendering is seek-pure: on `seek(t)` set instance transforms from `t` and render once. Never `setAnimationLoop` or `requestAnimationFrame` (#15, #19).
4. Headless WebGL varies by machine (#65). Render on the pinned render box only; test a software-GL fallback; export a PNG sequence and import it as a clip (#20).
5. Labels are DOM overlays from fixture strings, positioned by projecting voxel centres at time `t`. No text in WebGL.
6. Uses: cubic lattices, stylised cell and organelle schematics, "island of concepts" recaps. Not for bond angles, molecular geometry, hexagonal lattices, field lines, physics simulations, or anything where angle or proportion carries the science.
7. Palette: ExamLeaf tokens; avoid red and amber for species (they carry error and condition meaning); never colour alone for species (add legend tags).
8. Camera: fixed or a slow orbit as a function of `t`, with no movement during label reveals (#64).
9. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px; captions in the bottom zone.
10. Cost: zero credits; render-box time is the cost (log it).

---

## 1. Uses

[Recommendation, report §4.5] ExamLeaf uses voxel-isometric inserts for:

| Use | Example | Source of positions |
|---|---|---|
| **Cubic lattices** | Rock-salt arrangement of an ionic solid; simple cubic metal | Fixture `cells[]` (integer coordinates plus species) |
| **Cell and organelle schematics** | A stylised cell cross-section built from blocks, with compartments as coloured regions | Fixture `regions[]` (integer boxes) |
| **Concept islands** | A recap "map" where each building is one concept from the lesson | The recap's concept list from the approved script; layout seeded |

A voxel insert is a **short insert** (typically 5-12 s) inside a lesson or Reel, not a whole scene. It shows structure and arrangement, never mechanisms or dynamics unless a fixture supplies the states.

## 2. When NOT to use this style

- Bond angles, molecular geometry, VSEPR shapes, orbitals, field lines, wave surfaces: voxels distort angles and curvature. Use the scientific three.js scenes fed from parametric fixtures, or Manim/Blender (report §4.6).
- Non-cubic lattices (hexagonal, body-centred layouts that do not sit on an integer cube grid) unless the fixture supplies a faithful grid mapping and a "schematic" note.
- Physics simulations and anything where proportion, direction or magnitude carries the science.
- Any scene whose job is "read the axis", "read the label", or "do the equation".
- A render box without working WebGL, or a Reel with no time for a 6 s insert.
- Photoreal or text-heavy content; tiny details (a voxel cannot show them).
- Anything that needs a perspective camera or real shadows.

## 3. Look and technique

1. **Geometry.** One `BoxGeometry(1,1,1)` drawn many times with `THREE.InstancedMesh`. Positions via `setMatrixAt`, colours via `setColorAt` (per-instance colour). Verify the exact API against the pinned three.js version before use.
2. **Camera.** `THREE.OrthographicCamera`. True isometric view: azimuth 45°, elevation `atan(1/√2) ≈ 35.264°`. Camera framing is computed from the fixture bounds so the whole structure fits the visual zone with 8% padding (a pure function).
3. **Baked lighting.** No real lights and no shadow maps. Shade each face of a cube by a fixed multiplier: **top 1.00, left 0.80, right 0.62** [Recommendation; classic isometric shading]. Bake it into vertex colours or per-face groups, and use an unlit material so the look is identical everywhere. Contact shadows are darker ground voxels placed by the layout, not computed.
4. **Edges.** A 1 px darker edge via a thin inset on each face colour, or a 1 px gap [Hypothesis]; no post-processing outline pass (it varies by GPU).
5. **Ground.** A one-high plate of ground voxels in two close tints in a checker, so depth reads without text.
6. **No blur, bloom, glow or gloss.** Flat, matte.
7. **Anti-aliasing.** Anti-aliasing differs by GPU and driver (#65). Render the insert at 2× its on-screen size and downscale in compositing to reduce variance [Hypothesis]; verify memory on the render box.
8. **Instance budget.** Keep the instance count within a budget that renders in the time allowed on the pinned box, including the software-GL fallback. Starting cap: 20,000 instances [Hypothesis]; measure.

## 4. Seeded layouts and fixture-bound voxels

- **Fixture-bound voxels** (anything scientific): integer grid coordinates, species and region IDs come from the fixture, read-only. The agent never adds, removes, moves or recolours a scientific voxel (#12). Decoration cannot change an arrangement the lesson teaches.
- **Decorative voxels** (grass, scattered blocks, ground variation, filler "buildings" for a concept island): placed from the stateless keyed PRNG `rnd(sceneId:layout:index)` so the layout is identical on every render and in any seek order (#17):

```js
// [Recommendation] stateless seeded random in [0,1); order-independent.
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function mulberry32(a){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}
const rnd=(key)=>mulberry32(fnv1a(key));
```

- **Concept islands.** Each building is one concept from the approved concept list; the layout (positions of buildings on the island) is seeded; the concept names are fixture or script strings shown as DOM labels. No concept is added by the agent.

## 5. Palette

ExamLeaf light tokens (`#F7F9FC` background, `#14213D` ink, `#526074`, `#185ABD`, `#087986`, `#9A5B00`, `#6E44AA`, `#B42318`) plus the proposed biology green `#1F7A3E` (5.09:1 on the background; needs brand-owner approval). Light theme only (RD-27).

- **Species colours** come from the fixture's colour token (default mapping [Recommendation]: blue, teal, purple, secondary, green). Do **not** use red `#B42318` or amber `#9A5B00` for species: they carry "error marker" and "condition or caution" meaning in the brand palette, and scientific conventions apply (a red oxygen atom is not an error indicator, ROOT/02 D4).
- **Never rely on colour alone.** The accents are close in luminance (blue/purple 1.05, teal/green 1.05 computed). Add a legend tag, a letter mark or a distinct voxel shape/pattern per species (ROOT/02 D4).
- **Identity stable.** A species keeps its colour across the whole lesson.
- Face shading uses the multipliers in §3; check that the darkest face of the darkest species still reads against the ground.

## 6. Camera and motion as functions of `t`

- **Camera path** is a pure function `camera(t)` defined by keyframes in the brief: a fixed isometric view, or a slow orbit of at most **45°** over the insert, plus an optional zoom (`camera.zoom` 1.00 to 1.15, ease `power2.inOut`). Dwell at least **2 s** on any labelled view.
- **No camera movement during label reveals or measurement** (#64). Labels reveal only on a static view.
- **Build-up.** Voxels appear by layer: scale 0 to 1 with `back.out(1.4)`, 0.25-0.35 s, staggered 30-60 ms per layer. One orchestrated entrance per beat [N53].
- **Highlight.** A species is emphasised by raising its brightness from 1.00 to at most 1.25 for 0.4 s (localised, never a full-frame change), then back. One highlight at a time (ROOT/02 D4).
- **Dynamics.** Anything that moves because of science (ions released on melting, a particle path) comes from a fixture with explicit frames or a parametric rule; the agent does not invent motion. Fixed-step replay must be seek-pure (report §10 item 8).
- **Sync.** Reveals land on, or about 0.05 s before, their word; times from `cues[].at` and `words[]` (#63).
- **Idle.** None, or a 1 px drift with finite repeats; off during holds and in the reduced-motion variant.
- **Reduced motion.** No orbit, no zoom, no stagger; the structure appears by a 150-300 ms fade.

## 7. Seek-pure rendering and headless WebGL (#65)

1. Scene exposes `window.DURATION` (equal to the cue sheet `duration`) and `async window.seek(t)`; frames = `DURATION × 30` [N72]. The renderer seeks and never plays [N68].
2. On `seek(t)`: compute instance matrices and colours from `t`, set the camera from `camera(t)`, call `renderer.render(scene, camera)` once, and return. No `setAnimationLoop`, no `requestAnimationFrame`, no `Date.now()`, no `setInterval` (#15, #19).
3. **Pinned render box.** Render voxel inserts on the pinned render box only (`examleaf-render-batch`). Frame hashes are compared only between renders on the same box; cross-machine hash equality is not expected (#65).
4. **Software-GL fallback test.** Run the insert on a software GL path as a CI check. Use the pinned Chrome's own supported option; verify the exact flag on the pinned build and do not guess (no flag is stated in the verified evidence).
5. **Context loss.** If the WebGL context is lost, fail the render with a blocker (`WEBGL_CONTEXT_LOST`); do not continue silently.
6. **Export.** Render to a PNG sequence and import it as a clip or sequence into the HyperFrames master timeline (report §2.4). A PNG sequence adds no video decoder (#20); if exported as video and mixed with other videos, use a single worker.
7. **Cache key** includes the three.js version, the render box ID, the instance data hash and the camera keyframes.
8. Double render of the same insert on the same box must give identical frame hashes.

## 8. Labels, legends and the accuracy note

- Labels are DOM overlays, never WebGL text. Strings come from the fixture (species names, charges, region names; each element marked `data-fx="path.to.field"`, contract §9) and are typeset in Noto Sans semibold (Inter for Latin) at 50-54 px, ink on `#F7F9FC`, with a leader line to the voxel (RD-23 fonts; vendored).
- Anchor positions are computed by projecting each voxel's world centre through `camera(t)` (a pure function); QA checks anchors fall within 4 px of the voxel centre.
- A **legend** maps species to colour and mark. Colour is never the only cue.
- **Accuracy note.** If the fixture says the model is schematic (ion sizes not to scale, organelle shapes simplified), the note text comes from the fixture and is shown for the whole insert. The agent does not write it.
- Indic labels: per word, never per code point (#55); line height at least 1.4; verified fonts (`kinetic-type.md` §8).

## 9. Layout in 1080×1920

Stacked zones inside the platform-safe box (insets only from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them; the assembler blocks the brief if the file is missing; while `platform_insets_px.measured` is false its `applies_until_measured` insets are used and the job manifest records them as provisional):

| Zone | Share of safe-box height | Holds |
|---|---:|---|
| Title | top 22% | one headline or kicker (kinetic or serif) |
| Visual | middle 54% | the voxel canvas, legend, labels, accuracy note |
| Caption | bottom 24% | accessible caption track on an `#F7F9FC` plate |

Side margin at least **96 px**. The voxel canvas occupies the visual zone width; the camera framing keeps 8% padding.

## 10. Sound

Quiet block-place ticks per layer (not per voxel), a soft chime only for a confirmed result under conditional narration, none during `think`, `pause-video`, equation reading or inspection. Loudness -16 LUFS ±1, true peak at most -1 dBTP after the final mux (#39). Music off under reasoning (ROOT/02 G5).

## 11. Writing

The words come from the narration system (#11). Voxel inserts suit sentences like "Here is the arrangement: positive and negative ions alternate in every direction", where the picture is a structure and the sentence names the relationship. They do not carry claims that the fixture does not make. Example hook for a lattice insert (CSV ID 12): "Same salt: why compare the solid with the melt?" The lattice insert shows the fixed arrangement; the melt comparison is a separate data-bound panel.

## 12. Do and don't

**Do**
- Take every scientific voxel from the fixture grid.
- Keep the camera still while labels reveal.
- Add a legend and a schematic note when the fixture requires one.
- Export a PNG sequence from the pinned render box.

**Don't**
- Use a perspective camera, bloom, glow, real shadows or post-processing.
- Colour species red or amber, or distinguish species by colour alone.
- Place text in the WebGL scene.
- Use voxels for angles, curved surfaces, hexagonal lattices or dynamics without a fixture.
- Loop forever or animate off the wall clock (#15, #18).
- Add full-frame flashes (#56).

## 13. Cost

- Credits: zero.
- Compute: GPU or software-GL minutes on the render box; software GL is slower [Hypothesis]. Log render minutes with `examleaf-observability-cost`.
- Tokens: unmeasured; [V1]'s 3D runs cost far more tokens than 2D at the same effort (low about 78K versus max about 625K for one 79 s piece); ExamLeaf inserts built from templates should be far smaller, to be measured. Use effort **high**, **xhigh** only with a written reason (report §3.4).

## 14. QA checklist (`examleaf-anim-qa`)

- [ ] 1080×1920, 30 fps; DURATION equals the cue sheet; lint zero errors.
- [ ] Double-render hashes identical on the same box; software-GL test passes visually.
- [ ] Every scientific voxel matches the fixture grid; decorations are seeded.
- [ ] Label strings equal fixture fields; anchors within 4 px of voxel centres.
- [ ] No camera move during reveals; no flash; reduced-motion variant renders.
- [ ] Species have a legend; no red or amber species colours; contrast of labels at least 4.5:1.
- [ ] Safe box respected; captions in the bottom zone only.
- [ ] PNG sequence imported as a clip without extra video decoders.

## 15. Edge cases handled

#12 (§4), #15 (§7), #17 (§4), #18 (§6), #19 (§7), #20 (§7), #49 (§9), #51 (§9), #54 (§8), #55 (§8), #56 (§6), #57 (header), #63 (§6), #64 (§6), #65 (§7).

## 16. Changelog

- 1.0.0 (15 Oct 2026): first version.
