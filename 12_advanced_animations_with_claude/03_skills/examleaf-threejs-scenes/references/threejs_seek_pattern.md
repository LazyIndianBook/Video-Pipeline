# three.js seek pattern

A three.js scene in ExamLeaf is a pure function of `t`: camera, object transforms and material uniforms are computed from `t`, fixture data and seeded layouts, then one frame is rendered inside `window.seek(t)`. There is no render loop. The three.js revision is not pinned in the evidence set: vendor one reviewed build (no CDN, lint F12), pin it through `examleaf-skills-security`, and verify every API named here against that revision. The pure helpers in §2–§3 were executed under Node during authoring; the three.js calls in §1 and §4–§7 were not run here.

## 1. Renderer setup (once, in `window.ready`)

```js
import * as THREE from './vendor/three.module.js';                 // vendored, pinned revision
const W = 1080, H = 1920;
const canvas = document.getElementById('gl');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true,
                                           powerPreference: 'high-performance' });
renderer.setPixelRatio(1);                                         // never devicePixelRatio: fixed render box
renderer.setSize(W, H, false);
// No renderer.setAnimationLoop(...) and no requestAnimationFrame: both are real-time loops (lint F07) [N69].
// No THREE.Clock / getDelta(): wall clock (lint F01-F03 catch Date/performance; Clock uses them internally).
```

- `preserveDrawingBuffer: true` keeps the last frame readable for the capture after `seek` resolves.
- `antialias` is a GPU/driver-dependent feature; keep it fixed per render box and record it in the manifest (#65).

## 2. Fixture replay: interpolate fixed-step samples (pure)

```js
// fx: validated by validate_trajectory_fixture.py (fixed dt, t starts at 0, units present, frozen).
function sampleAt(fx, t) {
  const n = fx.samples.length, dt = fx.dt;
  const u = Math.min(Math.max(t / dt, 0), n - 1);                  // clamp: never extrapolate beyond the fixture
  const i = Math.min(Math.floor(u), n - 2), f = u - i;
  const a = fx.samples[i], b = fx.samples[i + 1];
  return a.map((v, k) => v + (b[k] - v) * f);                      // linear; same t -> same state, any order
}
// Map physical time to scene time explicitly when the replay is slowed down or sped up:
const physT = (t, cueAt, timeScale) => Math.max(0, (t - cueAt) * timeScale);   // timeScale stated in scene notes
```

The replay never steps an integrator inside `seek`. If the lesson needs a different trajectory, the science skill recomputes the fixture; the scene does not "simulate".

## 3. Camera as a function of t (pure)

```js
// Slow orbit around a target, dolly in, both eased; frozen inside lock windows (measurement or label reveals, #64).
function effectiveT(t, locks) { let lost = 0; for (const [a, b] of locks) { if (t <= a) break; lost += Math.min(t, b) - a; } return t - lost; }
function orbitCamera(t, { D, r0 = 14, r1 = 11, a0 = -0.6, a1 = 0.6, h = 6, locks = [] }) {
  const te = effectiveT(t, locks);
  const locked = locks.reduce((s, [a, b]) => s + (b - a), 0);
  const u = Math.min(1, Math.max(0, te / Math.max(1e-6, D - locked)));
  const e = u * u * (3 - 2 * u);                                   // smoothstep: no linear motion
  const ang = a0 + (a1 - a0) * e, r = r0 + (r1 - r0) * e;
  return { x: r * Math.sin(ang), y: h, z: r * Math.cos(ang) };
}
```

Apply in `seek`: `const c = orbitCamera(t, P); camera.position.set(c.x, c.y, c.z); camera.lookAt(0, 0, 0);`

## 4. Orthographic camera for voxel / isometric scenes (9:16)

```js
const aspect = W / H;                                              // 0.5625
const viewH = 24;                                                  // world units visible vertically (scene choice)
const cam = new THREE.OrthographicCamera(-viewH * aspect / 2, viewH * aspect / 2, viewH / 2, -viewH / 2, 0.1, 200);
cam.position.set(20, 20, 20); cam.lookAt(0, 0, 0);                  // classic isometric-style view
cam.updateProjectionMatrix();
```

## 5. Seeded layouts and instanced voxels

```js
// Build once: positions from a fixture (lattice) or a seeded procedural layout (decorative island only).
const geo = new THREE.BoxGeometry(1, 1, 1);
const mat = new THREE.MeshLambertMaterial({ color: 0xffffff });
const mesh = new THREE.InstancedMesh(geo, mat, cells.length);
const order = ExamLeafPRNG.shuffled(SEED, cells.map((_, i) => i));   // seeded pop-in order, built once
const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), S = new THREE.Vector3(), Pv = new THREE.Vector3();

// In seek(t): every instance's scale is a pure function of t (pop-in by seeded order after the cue).
function applyVoxels(t, startAt, perVoxel = 0.012, dur = 0.25) {
  order.forEach((idx, k) => {
    const p = Math.min(1, Math.max(0, (t - (startAt + k * perVoxel)) / dur));
    const s = p === 0 ? 1e-4 : 1 + 2.5 * Math.pow(p - 1, 2) + 3.5 * Math.pow(p - 1, 3);   // back.out(2.5)
    Pv.set(...cells[idx].pos); S.set(s, s, s); M.compose(Pv, Q, S); mesh.setMatrixAt(idx, M);
  });
  mesh.instanceMatrix.needsUpdate = true;
}
```

Decorative layouts may be procedural; anything that teaches (a lattice, an organelle count) comes from a fixture.

## 6. Seek, error channel and context loss

```js
window.seek = async function (t) {
  await window.ready;
  if (contextLost) throw new Error('E_WEBGL_CONTEXT_LOST');          // never render a silently blank frame
  const tc = Math.min(Math.max(t, 0), window.DURATION);
  applyState(tc);                                                  // camera, fixtures, voxels, uniforms (uTime = tc)
  renderer.render(scene, camera);
};
let contextLost = false;
canvas.addEventListener('webglcontextlost', e => {
  e.preventDefault(); contextLost = true;
  window.__errors.push({ code: 'E_WEBGL_CONTEXT_LOST', severity: 'error', message: 'WebGL context lost', t: null });
});
canvas.addEventListener('webglcontextrestored', () => { rebuildGpuResources(); contextLost = false; });
```

The harness treats any `error` in `window.__errors` as a failed frame range and re-renders it after restoration; it never stitches blank frames. three.js offers `renderer.forceContextLoss()` for testing this path (verify in the pinned revision).

## 7. Shaders and animation clips

- Shader time is a uniform set from `t` (`material.uniforms.uTime.value = t`), never from a clock.
- Imported animation clips are positioned with the mixer's absolute time setter (`mixer.setTime(t)` in current three.js; verify), never advanced with `update(delta)`.
- No post-processing passes that accumulate across frames (temporal AA, motion blur buffers): they make frame t depend on frame t−1.

## 8. Export

Render through the harness into `frames/frame_%05d.png`, run the double-render hash test (`examleaf-motion-harness`), then encode a clip with FFmpeg (standard usage, verify on your build):

```sh
ffmpeg -framerate 30 -i frames/frame_%05d.png -c:v libx264 -pix_fmt yuv420p clip.mp4
```

Keep PNGs with alpha when the clip is an overlay; `yuv420p` drops alpha. HyperFrames places the clip at its cue time (report §2.6).
