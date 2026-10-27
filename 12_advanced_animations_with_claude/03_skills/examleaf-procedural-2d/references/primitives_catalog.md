# Primitives catalog (Canvas/SVG, functions of t)

Every primitive below is a **pure function of time `t`** plus immutable data built once in `window.ready`. None reads the wall clock, none keeps state between frames, all randomness is `rngAt(seed, i)` from `scripts/seeded_prng.js` (same formulas as `04_harness_contract/scene_template.html` §7). Values marked [V4-MP] come from the paper-collage master prompt; token names refer to `04_harness_contract/vertical_safe_zones.tokens.json` → `motion`.

The snippets are plain ES2017 and were extracted and executed under Node in authoring (see §11); DOM/Canvas calls are illustrative and must pass `lint_seek_contract.js`.

## 1. Core helpers

```js
const clamp01 = x => Math.min(1, Math.max(0, x));
const lerp = (a, b, u) => a + (b - a) * u;
const prog = (t, at, dur) => clamp01((t - at) / dur);          // 0 before `at`, 1 after `at + dur`

// Easing (anticipation -> action -> follow-through; never linear, [V4-MP]).
const E = {
  cubicOut:  u => 1 - Math.pow(1 - u, 3),
  power3Out: u => 1 - Math.pow(1 - u, 4),                       // GSAP "power3" = quartic
  power2InOut: u => u < 0.5 ? 8 * u * u * u * u : 1 - Math.pow(-2 * u + 2, 4) / 2,
  expoOut:   u => u === 1 ? 1 : 1 - Math.pow(2, -10 * u),
  backOut:   (u, s = 2.5) => 1 + (s + 1) * Math.pow(u - 1, 3) + s * Math.pow(u - 1, 2),  // s in 2-3 for pops
};
```

GSAP's names are used as vocabulary only; no tween library is required. If a library is used, its timeline must be paused and set from `seek(t)`.

## 2. Pop-in with overshoot, pivoting at the feet ([V4-MP])

```js
// From scale 0 and about +-12 deg to full size with back.out(2-3); transform-origin: 50% 100%.
function popIn(t, at, seed, i, dur = 0.45) {
  const u = prog(t, at, dur);
  const rot0 = (rngAt(seed, i) * 2 - 1) * 12;
  return { scale: u === 0 ? 0 : E.backOut(u, 2.5), rotDeg: lerp(rot0, 0, E.cubicOut(u)), origin: '50% 100%' };
}
```

## 3. Finite idle sway / bob (#18)

```js
// Gentle sway +-A deg with period T, exactly n cycles after `from`, then rest. Never infinite.
function idleSway(t, from, { A = 2.5, T = 2.4, n = 6, phase = 0 } = {}) {
  const d = t - from;
  if (d <= 0 || d >= n * T) return 0;
  const env = Math.min(1, d / 0.4, (n * T - d) / 0.4);           // ease in/out of the finite loop
  return A * env * Math.sin(2 * Math.PI * d / T + phase);
}
```

[V4-MP] says "never frozen": every visible element gets some idle motion, but with a finite repeat count. `n` comes from the style tokens (`motion.idle_repeats_max`).

## 4. Stop-motion boil (8–10 fps)

```js
// Jitter that changes only once per boil step; stateless, so any seek order gives the same frame.
function boil(t, seed, k, { fps = 8, amp = 2 } = {}) {
  return ExamLeafPRNG.wobble(seed, k, t, fps, amp);              // [dx, dy]
}
```

Use for shivering, nerves, crying, fire flicker and shaking ground ([V4-MP]). Never boil a science glyph that encodes a value (arrow tips, graph points, labels).

## 5. Wobble stroke + draw-on (pencil doodle)

```js
// points: [[x,y],...] built once. Returns an SVG path "d" with per-point wobble that boils.
function wobblePath(points, t, seed, { fps = 8, amp = 1.5 } = {}) {
  return points.map(([x, y], k) => {
    const [dx, dy] = ExamLeafPRNG.wobble(seed, k, t, fps, amp);
    return (k ? 'L' : 'M') + (x + dx).toFixed(2) + ' ' + (y + dy).toFixed(2);
  }).join(' ');
}
// Draw-on: stroke-dasharray = L, stroke-dashoffset from L to 0. L measured once (getTotalLength) in ready().
function drawOn(t, at, dur, L) {
  return { dasharray: L, dashoffset: L * (1 - E.cubicOut(prog(t, at, dur))) };
}
```

Doodle strokes: ink `#3a332c`, 3–5 px, round caps ([V4-MP]). Measure path length once; the wobble changes length slightly, so draw-on uses the base length.

## 6. Paper texture (built once)

```js
// Grain is generated ONCE in ready() with a stateful stream in a fixed order, then reused every frame.
function makePaperTexture(w, h, seed, { base = '#f3ecdf', grain = 10 } = {}) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const g = c.getContext('2d'); g.fillStyle = base; g.fillRect(0, 0, w, h);
  const img = g.getImageData(0, 0, w, h), r = ExamLeafPRNG.mulberry32(seed);
  for (let p = 0; p < img.data.length; p += 4) {
    const n = (r() - 0.5) * grain;
    img.data[p] += n; img.data[p + 1] += n; img.data[p + 2] += n;
  }
  g.putImageData(img, 0, 0);
  return c;                                                      // drawImage(c, 0, 0) inside render(t)
}
```

Backgrounds rotate between cream watercolour paper, kraft board, watercolour skies, night navy with splatter stars and charcoal soot ([V4-MP]); vendored scans from the asset library are an alternative to procedural grain.

## 7. Die-cut border + two-layer warm shadow ([V4-MP] values)

```html
<!-- White die-cut border that follows the silhouette: dilate the alpha, flood white, put the art on top. -->
<svg width="0" height="0" style="position:absolute">
  <filter id="diecut" x="-10%" y="-10%" width="120%" height="120%">
    <feMorphology in="SourceAlpha" operator="dilate" radius="8" result="grow"/>   <!-- 6-12 px at 1080p -->
    <feFlood flood-color="#fbf7ee"/>
    <feComposite in2="grow" operator="in" result="border"/>
    <feMerge><feMergeNode in="border"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</svg>
<style>
  .cutout { filter: url(#diecut)
            drop-shadow(0 9px 7px rgba(74,48,22,0.30))
            drop-shadow(0 2px 1.5px rgba(0,0,0,0.20)); }
</style>
```

The shadow numbers are [V4-MP]'s box-shadow-style values; CSS `drop-shadow` blur behaves slightly differently, so compare one rendered frame against the style test sheet. Filters are static (no animation), so they are seek-safe. Prefer pre-baking the border into the cutout PNG when an asset is reused across many scenes (faster renders).

## 8. Paper-sheet transition ([V4-MP])

```js
// New full-frame sheet slides over the previous scene; 0.5-0.7 s, power3.out, settles from a slight rotation.
// Starts about 0.3 s after the previous line's last word. No exit animations: the next sheet is the exit.
function sheetIn(t, at, dir, { dur = 0.6, W = 1080, H = 1920, rot0 = 3 } = {}) {
  const u = E.power3Out(prog(t, at, dur));
  const off = { right: [W, 0], left: [-W, 0], top: [0, -H], bottom: [0, H] }[dir];
  return { x: off[0] * (1 - u), y: off[1] * (1 - u), rotDeg: rot0 * (1 - u) };
}
```

Variants: somber dark sheet drop (power2InOut, ~0.9 s, small settle), urgency whip (expoOut, ~0.4 s). Vary direction per scene. The [V4-MP] "white flash or bloom for explosions" is **not** used (flash ban, #56); use a paper burst instead.

## 9. Gags

```js
// Tear along a seeded jagged edge; halves fall away after `at`.
function tearEdge(seed, H, { teeth = 18, jag = 22, x0 = 540 } = {}) {   // built once
  const pts = [];
  for (let k = 0; k <= teeth; k++) pts.push([x0 + (rngAt(seed, k) * 2 - 1) * jag, (H * k) / teeth]);
  return pts;                                                    // left half = polygon(0,0 .. pts .. 0,H); right = mirror
}
function tearHalves(t, at, { dur = 0.8, drop = 260, spin = 9 } = {}) {
  const u = E.cubicOut(prog(t, at, dur));
  return { left: { x: -40 * u, y: drop * u * u, rotDeg: -spin * u }, right: { x: 40 * u, y: drop * u * u, rotDeg: spin * u } };
}

// Paper-flip swap: scaleX 1 -> 0, swap the image, 0 -> 1, with a seeded confetti puff.
function paperFlip(t, at, dur = 0.4) {
  const u = prog(t, at, dur);
  return { scaleX: Math.abs(Math.cos(Math.PI * u)), showB: u >= 0.5 };
}

// Multiply gag: 1 -> 2 -> 4 -> 8 copies, each doubling on its own cue time.
const copiesAt = (t, cueTimes) => Math.pow(2, cueTimes.filter(c => t >= c).length);

// Squashy hop from the feet.
function hop(t, at, { dur = 0.5, height = 60 } = {}) {
  const u = prog(t, at, dur);
  const y = -height * 4 * u * (1 - u);
  const squash = u < 0.12 ? 1 - 0.18 * Math.sin(Math.PI * u / 0.12) : u > 0.88 ? 1 - 0.18 * Math.sin(Math.PI * (u - 0.88) / 0.12) : 1;
  return { y, scaleY: squash, scaleX: 2 - squash };
}
```

## 10. Depth layers, parallax and a camera that respects measurement windows (#64)

```js
// Layers: background (depth 0.2) -> torn-paper middle (0.5) -> props (0.8) -> characters (1.0) -> foreground strip (1.3).
// Camera push-in and pans are suspended inside lock windows (measurement or label reveals), so diagrams are never
// distorted while they are being read. effectiveT is a pure function of t: time spent inside locks does not count.
function effectiveT(t, locks) {                                  // locks: [[t0, t1], ...] sorted, non-overlapping
  let lost = 0;
  for (const [a, b] of locks) { if (t <= a) break; lost += Math.min(t, b) - a; }
  return t - lost;
}
function camera(t, locks, { D, s1 = 1.035, panY = 0 } = {}) {    // push-in to ~1.03-1.04 over the scene [V4-MP]
  const lockedTotal = locks.reduce((s, [a, b]) => s + (b - a), 0);
  const u = clamp01(effectiveT(t, locks) / Math.max(1e-6, D - lockedTotal));
  return { scale: lerp(1, s1, u), y: panY * u };
}
const layerOffset = (cam, depth) => ({ y: cam.y * depth, scale: 1 + (cam.scale - 1) * depth });
```

Lock windows come from the cue sheet: every cue whose `element_id` is a fixture-bound element (labels, values, arrows, graphs) locks from its `at` to its hold end (`until`) or `at` + the headline hold. Stepped impact shakes are also suppressed inside locks.

## 11. Verification snippet (run under Node)

```js
const P = require('../scripts/seeded_prng.js'); global.ExamLeafPRNG = P; const rngAt = P.rngAt;
// paste sections 1-5 and 8-10 here, then:
console.assert(idleSway(100, 0) === 0, 'sway is finite');
console.assert(effectiveT(5, [[1, 2], [3, 3.5]]) === 3.5, 'locks remove 1.5 s');
console.assert(camera(1.5, [[1, 2]], { D: 10 }).scale === camera(1.0, [[1, 2]], { D: 10 }).scale, 'camera frozen in lock');
console.assert(JSON.stringify(boil(1.01, 7, 3)) === JSON.stringify(boil(1.12, 7, 3)), 'boil holds within a step');
console.assert(copiesAt(2.5, [1, 2, 3]) === 4, 'multiply gag');
```
