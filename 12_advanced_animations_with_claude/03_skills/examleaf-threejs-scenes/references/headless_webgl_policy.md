# Headless WebGL policy

Edge case #65 (report §8): "3D frames differ by machine" because of GPU and driver differences [Hypothesis]; prevention: "fixed render box; software GL fallback test". Report §11.11 leaves the final decision open (single render box vs software-GL policy). This policy is the working [Recommendation] until the pilot measures it.

## 1. One fixed render box per lesson

- All WebGL scenes of a lesson render on one box with a recorded fingerprint: OS, Chrome version and path (`CHROME` [N17]), GPU model, driver version, three.js revision, font hashes.
- `preflight.sh` passes on that box before any render.
- The determinism baseline (frame-hash manifest) is valid **only** for that fingerprint. Any change (driver update, Chrome update, new box) requires a re-baseline: render twice, compare, store the new manifest, and have a reviewer spot-check frames against the old ones.

## 2. Settings that must be fixed

| Setting | Value | Why |
|---|---|---|
| Pixel ratio | 1 | device-dependent otherwise |
| Canvas size | 1080×1920 | contract canvas |
| `antialias` | fixed per box (record it) | GPU-dependent sampling |
| `preserveDrawingBuffer` | true | capture after `seek` resolves |
| Precision | default high precision; record any shader `precision` qualifiers | mobile-class GPUs differ |
| Temporal effects | none (no TAA, motion-blur accumulation, frame feedback) | frame t must not depend on t−1 |
| Time | uniforms from `t` only | no clocks |
| Workers | start with 1–2 WebGL workers [Hypothesis] | each worker holds a GPU context; too many risks context loss; measure in the pilot |

## 3. Software-GL fallback test

Keep one recorded run of each 3D scene through Chrome's software rendering path (flag names differ between Chrome versions; verify on the box) to know whether the scene can be rendered without a GPU if the box fails. Software output is not expected to be byte-identical to GPU output; it is a fallback with its own baseline and a reviewer's visual sign-off.

## 4. Context loss

- Listen for `webglcontextlost` / `webglcontextrestored` on the canvas (seek pattern §6).
- On loss: push an `error` into `window.__errors`, make `seek` reject, and let the harness re-render the affected frame range after restoration. Never write blank or partial frames into the sequence.
- Test the path once per scene family with three.js's `forceContextLoss()` (verify in the pinned revision).
- Frequent losses → reduce workers, texture sizes and instance counts; dispose unused geometries and textures.

## 5. What "deterministic" means for 3D

- **Same box, same fingerprint, same inputs → byte-identical PNGs.** Required (double-render test, `examleaf-motion-harness`).
- **Different box → may differ.** Accepted only after re-baselining and a visual review; never mix frames from two boxes inside one clip.
- **Hash tolerance:** none on the same box. Perceptual comparison tools are a possible future addition for cross-box review [Hypothesis]; they are not part of the release gate.

## 6. Failure triage

| Symptom | Likely cause | Action |
|---|---|---|
| Hashes differ between two runs on one box | randomness, clock, temporal effect, unresolved texture load | Lint; check `window.ready` waits for textures; remove temporal effects |
| Identical on box A, differ A vs B | GPU/driver variance (#65) | Re-baseline on the production box; never mix |
| Black frames | context loss or drawing buffer not preserved | Context-loss handler; `preserveDrawingBuffer: true` |
| Render hangs | `setAnimationLoop`/rAF in scene | Lint F07; use `seek` only [N69] |
| Different first frame | fonts/textures not ready | Await all loads in `window.ready` |
