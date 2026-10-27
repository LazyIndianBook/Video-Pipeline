# 04 · Harness contract and determinism

**Purpose.** The technical contract every animation scene must satisfy so that any renderer (HyperFrames, Remotion, a raw Chrome seek pipeline) produces the same frames every time: the time-in/pixels-out interface, the traps that break it, a reference scene skeleton, the cue-sheet loader, canvas and font rules, the double-render determinism test, the lint rules, the harness decision table, how clips from Manim/SVG/three.js/Blender enter the master timeline, the render-box policy and the 9:16 export settings.

**Normative files.** `12_advanced_animations_with_claude/04_harness_contract/contract.md` (the contract text), `scene_template.html` (reference scene), `lint_seek_contract.js` (linter), `determinism_hash_check.py` (hash test), `cue_sheet.schema.json` + `cue_sheet.example.json`, `preflight.sh`, `vertical_safe_zones.tokens.json`, `reference_analysis.sh`, `README.md`, all in `12_advanced_animations_with_claude/04_harness_contract/`. If this document and those files disagree, the files win and this document is corrected.

**Conventions.** As in doc 00. Edge cases #1–#65 from report §8.

---

## 1. The contract in one paragraph

A scene is a web page (or a Python/three.js program behind an equivalent interface) that declares its length in seconds and can draw **the exact state at any time `t` on request**. The renderer never plays it; it calls `seek(t)` for `t = i / fps`, waits for the returned promise, and captures the frame (opus-js-animations "renders frame i as seek(i / fps) across parallel workers" [N18]; HyperFrames "never calls play()" [N68] (contested); the HuggingFace contract: "The scene must set `window.DURATION` and expose `async window.seek(t)`" [N72]). The scene is therefore a **pure function of time** [N61] (contested): same `t` → same ~~pixels~~ DOM, style and canvas state, regardless of which frames were drawn before, in which order, or in which worker.

**Amended 16 Oct 2026 (pilot gap L-01).** On Chrome 155/macOS the *pixels* also depend on the seek-and-capture history for layers with CSS `transform` (raster-scale cache): reverse-order or sampled captures differ by a few LSBs (PSNR ≈ 45 dB) with identical DOM state, and no Chrome flag tested removes it. An identical procedure (fresh page, every frame seeked AND captured in order) is byte-identical across runs; the pilot's MP4 SHA-256 matched across runs. Pixel determinism is therefore defined as *identical procedure, identical bytes* (contract §2.2, §11). Mitigation: headline and word reveals use `opacity` (and SVG attribute or canvas positions), not CSS `transform` scale, where byte-identity matters; one render per machine at a time (L-02).

---

## 2. Contract clauses

| # | Clause | Rationale / evidence | Edge case | Checked by |
|---|---|---|---|---|
| C1 | Set `window.DURATION` (seconds, a finite number > 0) **before** the renderer's first call; its value equals the cue sheet's `duration` | Frame count = `DURATION × fps` [N72] | #16 | Linter; runtime probe |
| C2 | Expose `window.seek = async (t) => {…}` which draws the state at `t` and resolves only when the DOM/canvas reflects it | [N72] | #16 | Linter; runtime probe |
| C3 | HyperFrames compatibility: if the harness expects `window.__hf` with duration and seek [N68] (contested), a shim maps it to C1/C2. Scene authors write C1/C2 only | Keeps scenes harness-agnostic | #16 | Adapter test |
| C4 | Never call `play()` on anything; never autoplay media | "The renderer never calls play()" [N68] | #15 | Linter |
| C5 | No wall clock: no `Date.now()`, `new Date()`, `performance.now()`, `setInterval`, timer-driven animation, or CSS `@keyframes`/`transition` for timed motion | The renderer seeks; real time does not advance between frames | #15 | Linter |
| C6 | No `requestAnimationFrame` for animation or polling; never await rAF inside `seek` | "rAF doesn't fire in beginFrame mode" [N69]; rAF polling hangs | #19 | Linter |
| C7 | Randomness only from the provided **stateless** seeded hash (`rand(key, step)`); no `Math.random`; no RNG whose state carries between `seek` calls | Same `t` must give same state in any order [N61]; [V4-MP] "only seeded randomness" | #17 | Linter; reverse-order hash test |
| C8 | Finite repeats only; every loop, sway or boil is computed from `t` and ends at a defined time | [V4-MP] "only finite repeats" | #18 | Linter (`repeat: -1`, `loop`, `Infinity`) |
| C9 | All timings come from `cues/<scene_id>.json`; no time literals for reveals in scene code | Re-sync on TTS regeneration | #63 | Linter (warn on numeric literals near reveal code) |
| C10 | All science values come from `fixtures/`; fixtures are frozen at load | Accuracy invariant | #12 | DOM-text diff in QA |
| C11 | Canvas **1080×1920**, `devicePixelRatio` treated as 1, no responsive layout | Vertical only | #49 | Runtime probe |
| C12 | Fonts only from `assets/fonts/` via local `@font-face`; `seek` awaits `document.fonts.ready` before drawing; glyph coverage verified (§6) | Offline render rule; tofu | #55 | Linter; QA test card |
| C13 | No network: no CDN scripts, remote fonts, `fetch` to http(s), remote images or media | "Production renders use staged local assets" (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2) | — | Linter; render box has no network |
| C14 | At most one `<video>` element per scene; video-heavy scenes render with a single worker; prefer PNG sequences for imported clips | Parallel seeking "without running out of decoders" fails; "drop back to a single worker for video-heavy renders" [N70] | #20 | Linter (count) + render config |
| C15 | Physics or simulation state at `t` comes from a fixed-step replay from 0 or from a table precomputed deterministically at load | No real-time stepping | #15 | Reverse-order hash test |
| C16 | No camera effects (shake, push-in, wobble) on science elements or during their reveal | Geometry must not be misread | #64 | Human QA; route tags |
| C17 | No full-frame flashes | Photosensitivity | #56 | anim-qa flash check |
| C18 | `seek(t)` clamps `t` to `[0, DURATION]` and is idempotent | Robustness | #16 | Runtime probe |

**About CSS animations.** [N54] advises "Prioritize CSS-only solutions for HTML", but that cookbook targets live web pages. In a seek-only renderer, CSS animations and transitions advance on the document timeline, which is real time unless the harness virtualises it; whether HyperFrames or Remotion do so for CSS is not in the evidence. [Recommendation] Use CSS for static styling only and compute every animated property from `t` in JavaScript. Revisit if the benchmark proves a harness virtualises CSS time deterministically.

**About tween libraries.** A GSAP-style timeline is acceptable if it is created **paused** and positioned from `seek(t)` (for GSAP, by setting the timeline's time; verify the method names against the pinned GSAP version). Never let a library's own ticker drive the scene. Record GSAP's licence if vendored ("not MIT", `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5).

---

## 3. Reference scene skeleton

The authoritative template is `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`. The skeleton below shows the pattern every scene follows; it uses only standard Web APIs.

```html
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  /* Fonts: local files only (C12, C13) */
  @font-face { font-family: "SciSans"; src: url("../../assets/fonts/Inter-SemiBold.woff2") format("woff2"); }
  @font-face { font-family: "Hand"; src: url("../../assets/fonts/PatrickHand-Regular.woff2") format("woff2"); }
  html, body { margin: 0; background: #F7F9FC; }
  #stage { position: relative; width: 1080px; height: 1920px; overflow: hidden; }   /* C11 */
  .label { position: absolute; font: 600 56px "SciSans"; color: #14213D; opacity: 0; }
  /* No @keyframes, no transition: properties are set from t in JS (C5) */
</style>
</head>
<body>
<div id="stage">
  <canvas id="bg" width="1080" height="1920"></canvas>
  <div id="title" class="label" style="font-family: Hand"></div>
  <div id="r_label" class="label"></div>
</div>

<!-- Staged, read-only inputs embedded by the job runner (no fetch at render time, C13) -->
<script id="cues" type="application/json">{"scene_id":"s03","fps":30,"duration":7.4,"words":[],"beats":[],"cues":[{"id":"title","at":0.40,"kind":"reveal"},{"id":"ray_refracted","at":3.15,"kind":"reveal"}],"sfx":[]}</script>
<script id="fixture" type="application/json">{"theta_i_deg":45.0,"theta_r_deg":32.1,"labels":{"r":"r"}}</script>
<script id="text" type="application/json">{"title":"<approved on-screen title from the script bundle>"}</script>

<script>
(() => {
  "use strict";
  const CUES = JSON.parse(document.getElementById("cues").textContent);
  const FIX  = Object.freeze(JSON.parse(document.getElementById("fixture").textContent));   // C10
  const TEXT = Object.freeze(JSON.parse(document.getElementById("text").textContent));      // approved text, read-only
  const SEED = 20261014;                                       // from the brief, never random

  window.DURATION = CUES.duration;                              // C1

  // ---- Stateless seeded randomness (C7): same (key, step) -> same value, in any order.
  function mulberry32(a) {
    return function () {
      let t = (a += 0x6D2B79F5);
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function fnv1a(s) { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); } return h >>> 0; }
  const rand = (key, step = 0) =>
    mulberry32((SEED ^ fnv1a(String(key)) ^ Math.imul(step | 0, 0x9E3779B1)) >>> 0)();

  // ---- Time helpers
  const clamp01 = x => Math.min(1, Math.max(0, x));
  const prog = (t, start, dur) => clamp01((t - start) / dur);
  const backOut = (x, s = 2.5) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);  // back.out
  const power3Out = x => 1 - Math.pow(1 - x, 3);                                              // power3.out
  const cue = id => {                                                                          // C9: fail loudly
    const c = CUES.cues.find(c => c.id === id);
    if (!c) throw new Error("missing cue " + id);
    return c.at;
  };

  // ---- Finite idle sway (C8): ends exactly at a zero crossing, computed from t.
  function sway(t, start, periods, period, ampDeg) {
    const end = start + periods * period;
    if (t < start || t >= end) return 0;
    return ampDeg * Math.sin(2 * Math.PI * (t - start) / period);
  }

  // ---- Boil at 9 fps (C7): pose changes only when the step changes.
  function boil(t, id, px) {
    const step = Math.floor(t * 9);
    return [(rand(id + ":x", step) - 0.5) * 2 * px, (rand(id + ":y", step) - 0.5) * 2 * px];
  }

  const title = document.getElementById("title");
  const rLabel = document.getElementById("r_label");
  const bg = document.getElementById("bg").getContext("2d");

  function draw(t) {
    // Background (illustrative layer) — boil allowed here.
    bg.clearRect(0, 0, 1080, 1920);
    const [jx, jy] = boil(t, "doodle_star", 2);
    bg.fillStyle = "#14213D";
    bg.fillRect(140 + jx, 300 + jy, 12, 12);

    // Title pop on its cue, with finite sway afterwards.
    const p = prog(t, cue("title") - 0.05, 0.35);              // lands ~0.05 s before the word
    title.textContent = TEXT.title;                             // never typed by the agent (#11)
    title.style.opacity = p > 0 ? 1 : 0;
    const s = p > 0 ? backOut(p) : 0;
    const rot = sway(t, cue("title") + 0.4, 3, 1.2, 2);
    title.style.transform = `translate(180px, 260px) scale(${s}) rotate(${rot}deg)`;

    // Science element: refracted ray angle from the fixture; NO boil, NO sway (C10, C16).
    const q = prog(t, cue("ray_refracted") - 0.05, 0.6);
    const ang = FIX.theta_r_deg * Math.PI / 180;
    const len = 520 * power3Out(q);
    const x0 = 540, y0 = 960;                                    // boundary point (layout token in a real scene)
    bg.strokeStyle = "#185ABD"; bg.lineWidth = 8; bg.lineCap = "round";
    if (q > 0) { bg.beginPath(); bg.moveTo(x0, y0); bg.lineTo(x0 + Math.sin(ang) * len, y0 + Math.cos(ang) * len); bg.stroke(); }
    rLabel.textContent = FIX.labels.r;
    rLabel.style.opacity = q >= 1 ? 1 : 0;
    rLabel.style.transform = `translate(${x0 + 60}px, ${y0 + 220}px)`;
  }

  let fontsReady = null;
  window.seek = async (t) => {                                  // C2, C12, C18
    if (!fontsReady) fontsReady = document.fonts.ready;
    await fontsReady;
    const tt = Math.min(Math.max(Number(t) || 0, 0), window.DURATION);
    draw(tt);
    // Do NOT await requestAnimationFrame here (C6, [N69]); the renderer captures after resolve.
  };
})();
</script>
</body>
</html>
```

What the skeleton demonstrates:

1. **Stateless randomness.** `rand(key, step)` builds a fresh generator from `(seed, key, step)` each call, so seeking to frame 900 then frame 3 gives the same values as frame 3 then frame 900. A *stateful* seeded PRNG (one generator called repeatedly as frames render) is still non-deterministic under parallel or out-of-order rendering; this is the subtle half of #17.
2. **Finite repeats.** `sway` ends exactly on a zero crossing, so there is no jump when it stops (#18).
3. **Boil** changes pose only when `floor(t × 9)` changes ([V4-MP] 8–10 fps).
4. **Science elements** read the fixture and never receive jitter, sway or camera effects (#64).
5. **Cue lookup fails loudly** when an ID is missing, instead of silently drawing at a default time (#16, #63).
6. **No awaits on rAF** inside `seek` (#19).

The on-screen strings arrive in staged, read-only data blocks (`text` from the approved script bundle, `fixture` from validated science data); the agent never types them into code (#11, #12).

---

## 4. The cue-sheet loader

### 4.1 Shape

The schema is `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`, with an example in `cue_sheet.example.json`. The fields from report §5.5:

```json
{"scene_id":"phy-10-03-s04","fps":30,"duration":7.4,
 "words":[{"w":"refraction","t0":1.12,"t1":1.71}],
 "beats":[0.0,0.6,1.2],
 "cues":[{"id":"label_n1","at":1.07,"kind":"reveal"}],
 "sfx":[{"file":"pop.wav","at":1.07,"gain_db":-12}]}
```

`examleaf-cue-sheet` builds it from `lessons/<…>/audio/alignment.json` (word timings from `examleaf-alignment-localize` / `examleaf-speech-animation-synchronizer`), the beat grid from `examleaf-audio-analysis`, and SFX placements from the storyboard beats.

### 4.2 Loader rules

| Rule | Why | Edge case |
|---|---|---|
| All times in **seconds** relative to scene start | librosa beats default to frames; must use `units='time'` [N39] | #33 |
| Word, beat and audio timings computed at **one sample rate**, recorded in the cue sheet's provenance | `librosa.load` resamples to 22050 Hz unless `sr=None`; mixed rates drift [N81] | #35 |
| `duration` equals narration duration including protected pauses | Duration derives from narration [N72] | #16 |
| Every `cues[].at` in `[0, duration]`; words monotonic (`t0 ≤ t1`, non-decreasing) | Existing alignment checks (monotonic timestamps) | #16 |
| Empty `beats` allowed; scenes fall back to the narration sentence grid | Silent or beatless audio yields an empty list and 0 BPM [N41] | #34 |
| Tempo values stored as plain floats | librosa returns tempo as an ndarray even for mono [N38] | #32 |
| Cue sheet is regenerated whenever narration is regenerated; scene code is not edited | Timings change on TTS regeneration | #63 |
| `reveal` cues use `at = word.t0 − 0.05` by default ([V4-MP] sync rule) | One to two frames early at 30 fps | — |
| Answer-reveal cues are never earlier than the interaction's `answers_after` | Existing "answer hidden until the window ends" QA | — |

### 4.3 Frame mapping

- `fps = 30` (vertical-only decision of 15 Oct 2026, RD-16 superseded). Frame `i` is rendered at `t = i / fps`.
- [Recommendation] Frame count `N = ceil(DURATION × fps)` so the last frame starts before `DURATION`; record `N` in the render manifest. The audio mux then follows the existing rule: "Conform the timeline; do not silently stretch speech", with a 0.05 s tolerance (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S12).
- A reveal "lands" on the first frame whose time is ≥ its cue time.

---

## 5. Canvas, layout and safe zones

1. The stage is exactly 1080×1920 CSS pixels; canvases are 1080×1920 device pixels; the renderer's viewport is set to match with a device scale factor of 1 (C11).
2. Layout positions for titles, content and captions come from `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (token names `title_band`, `content_safe`, `caption_band`; pixel values measured, not invented; open question Q9).
3. Essential text sizes follow the phone rule on a 1080-wide master (about 50 px minimum source for essential labels, RD-18 derivation).
4. `examleaf-anim-qa` overlays the safe zones on sampled frames (every cue boundary and the first/last frame) and flags essential elements outside `content_safe` (#51).

---

## 6. Fonts: preload and glyph checks (#55)

1. **Local only.** `@font-face` with relative URLs into `assets/fonts/`; the linter rejects `http(s)://` font URLs and `@import` of remote stylesheets.
2. **Await before drawing.** `seek` awaits `document.fonts.ready` before the first draw (skeleton §3). For fonts used only later in a scene, call `document.fonts.load('<size> "<family>"', '<sample text>')` at load time so all faces are ready before any frame.
3. **Coverage is not proven by `document.fonts.check`.** That method reports whether the fonts that *would* be used are loaded; it does not prove that the chosen face contains every glyph, because the browser may fall back to another face silently. Glyph coverage must be checked separately:
   - offline, by reading the font's character map (cmap) with a reviewed font tool (tool and version to pin and admit; verify);
   - in the harness, by rendering the test card (doc 01 §3.3) and comparing it against a reference render approved by the native-language editor.
4. **Text shaping.** Devanagari and Bengali–Assamese shaping depends on the pinned Chrome build; any Chrome upgrade re-runs the test card.
5. **Animation granularity.** Per word by default; per grapheme cluster only after verification (doc 03 §4.4).

---

## 7. The double-render determinism test

### 7.1 Procedure (implemented by `12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py`; that file is authoritative)

1. **Render A:** all frames in forward order, fresh browser, on the designated render box.
2. **Render B:** the same frames in forward order in a new browser process.
3. ~~**Render C (order test):** a subset of frames in **reverse** order (or a seeded shuffled order) in a new process. This catches stateful RNGs and accumulated state that a plain forward re-render cannot catch.~~ **Render C (order test, 16 Oct 2026):** compare **DOM, style and canvas state** (not pixels) for a reverse or seeded shuffled subset; this still catches stateful RNGs and accumulated state. Pixel hashes of a reversed or sampled render are not a valid check on Chrome 155 (L-01). Renders A, B and C run one at a time on the machine (L-02).
4. **Hash** each frame: SHA-256 of the decoded pixel data, or of the PNG file when both renders use the same encoder with no timestamps in metadata.
5. **Compare** per frame index: A = B for all frames; C = A for its subset.
6. **Report** `logs/determinism.json`: scene ID, environment hash (OS, Chrome, fonts, harness version), frame count, mismatching indices, first mismatch time, verdict.

### 7.2 Frame selection

- Scenes up to 20 s: every frame.
- Longer scenes: first and last frames, every cue boundary frame and the frames either side of it, and a seeded random sample (sample size set in the script).

### 7.3 Pass criteria

| Scene type | Criterion |
|---|---|
| 2D DOM/Canvas/SVG | 100% identical frame hashes A=B on the same box (identical in-order procedure, every frame) ~~and C=A~~; C=A on DOM/canvas state (16 Oct 2026) |
| WebGL (three.js, voxel) | 100% identical on the designated box; cross-box comparisons not required (#65) |
| Scenes with `<video>` | Same, rendered with one worker (#20); if hashes differ only on video frames, replace the video with a PNG sequence |

A determinism failure is **release-blocking** (AD-21): non-deterministic frames mean approvals bound to hashes cannot be trusted.

### 7.4 Reading a failure

| Pattern | Likely cause | Fix | Edge case |
|---|---|---|---|
| A ≠ B on scattered frames | `Math.random`, wall clock, unawaited font or image load | Stateless RNG; await fonts/images | #15, #17, #55 |
| A = B but C ≠ A | Stateful RNG, accumulated physics, tweens relying on previous frame | Compute from `t`; fixed-step replay table | #17, #18 |
| A = B, C's DOM state = A, C's pixels differ by a few LSBs | Chrome raster-scale cache on CSS-`transform` layers (16 Oct 2026, L-01); not a scene defect | Not a failure; to make order-free, reveal text with `opacity` instead of `transform` | #15 |
| A ≠ B on a few frames only when another render ran at the same time | Concurrent renders on one machine (16 Oct 2026, L-02) | One render per machine, re-run | #15 |
| Mismatch only after a certain time | Infinite tween or loop drifting | Finite repeats from `t` | #18 |
| Render hangs | rAF-based polling or awaiting rAF in `seek` | `setTimeout` polling with a deadline in the harness, never rAF [N69] | #19 |
| Black or frozen video frames | Parallel video decoding | One worker; PNG sequence | #20 |
| WebGL frames differ between boxes | GPU/driver | Per-box baseline; software-GL policy | #65 |

---

## 8. Lint rules

`12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js` statically checks scene files. The rule set below is the intended behaviour; the script is authoritative.

| ID | Pattern or check | Severity | Clause | Edge case |
|---|---|---|---|---|
| L01 | `window.DURATION` not assigned | error | C1 | #16 |
| L02 | `window.seek` not assigned an async function | error | C2 | #16 |
| L03 | `Math.random` | error | C7 | #17 |
| L04 | `Date.now`, `new Date(`, `performance.now` | error | C5 | #15 |
| L05 | `requestAnimationFrame` | error | C6 | #19 |
| L06 | `setInterval` | error | C5 | #15 |
| L07 | `setTimeout` in scene code | warn (allowed only in harness polling with a deadline) | C5 | #15, #19 |
| L08 | `.play(` or `autoplay` attribute | error | C4 | #15 |
| L09 | `repeat: -1`, `Infinity` in repeat counts, `loop` attribute on media, `iteration-count: infinite` | error | C8 | #18 |
| L10 | CSS `@keyframes`, `animation:` or `transition:` with non-zero duration | warn at `--level 0`; **error from `--level 1`** (script rule F14, 16 Oct 2026, L-14) | C5 | #15 |
| L11 | `http://` or `https://` in `src`, `href`, `url(`, `@import`, `fetch(` | error | C13 | — |
| L12 | Remote font hosts in any URL | error | C12 | #55 |
| L13 | More than one `<video>` element | error (or force workers = 1 and warn) | C14 | #20 |
| L14 | Canvas or stage size other than 1080×1920 | error | C11 | #49 |
| L15 | `document.fonts` not awaited in `seek` path | warn | C12 | #55 |
| L16 | Numeric time literals passed to reveal helpers instead of `cue(...)` | warn | C9 | #63 |
| L17 | Writes to fixture objects (assignment to a frozen fixture path) | error | C10 | #12 |
| L18 | Science-tagged elements (`data-sci="1"`) receiving boil, sway or camera transforms | error | C16 | #64 |
| L19 | Full-frame white overlays with opacity animations under 0.5 s | warn (flash check confirms) | C17 | #56 |
| L20 | Global mutable state updated inside `draw`/`seek` (e.g. `x += …` on module variables) | warn | C7, C15 | #17 |
| L21 | Missing `<meta charset="utf-8">` | warn | C12 | #55 |
| L22 | Secrets-like strings (API keys) anywhere | error | — | #40 |

Lint runs inside every fix loop (doc 02 §3.16) and again in `examleaf-anim-qa`.

---

## 9. Harness decision table (report §2.6)

| Criterion | HyperFrames | Remotion | Raw Canvas/SVG/three.js | Manim CE | Blender (MCP/scripted) |
|---|---|---|---|---|---|
| 9:16 vertical | Yes (HTML viewport you set) [Hypothesis] | Yes (composition size) [Hypothesis] | Yes (canvas size) | Yes (config frame size) [Hypothesis] | Yes (render resolution) |
| Deterministic | Seek-only renderer [N68] | Frame-based React [Hypothesis] | Seek per frame [N18][N72] | Scripted, deterministic [Hypothesis] | Deterministic if scripted and seeded [Hypothesis] |
| Science accuracy (data-bound) | Good when fed validated JSON | Good (typed props) | Good for custom diagrams | **Best for equations and graphs** | Selective spatial assets only |
| Agent skill support | 21 skills [N11] plus a plugin [N10] | Umbrella plus render/maps/upgrade [N4]–[N7] | opus-js-animations [N15] | manim_skill [N44] | Unverified MCP |
| Licence/cost | Apache-2.0, no per-render fee [N14] | **Verify** (not in evidence) | MIT [N21] | Open source [Hypothesis] | Open source [Hypothesis] |
| Requirements | Node 22+, FFmpeg [N8] | Node (version not in evidence) | Chrome/Chromium [N17] | Python, cairo on ARM for GL [N47] | Blender install |
| Video-in-video | Single worker [N70] | Benchmark | Avoid | n/a | n/a |
| Role | **Default lesson/reel composer** | Benchmark challenger | 3D and procedural inserts | Equation/graph inserts | Rare hero 3D |

**Decision** (AD-01, aligned with RD-07): HyperFrames is the master timeline; Remotion is benchmarked on the same three test lessons (one physics, one chemistry, one biology) measuring render time, determinism (identical frame hashes across two renders), agent token cost per scene, fix-loop count and reviewer edit time; exactly one compositor is selected afterwards, and the native SVG adapter remains the reference and regression renderer. Protocol: `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md`; pilot: `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md`; records: `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/record_sheets.md`.

---

## 10. Importing clips into the master timeline

### 10.1 Principle

Every non-HTML source renders to a **frame-exact clip** at 1080×1920 (or a declared sub-rectangle) and 30 fps, with a clip manifest, and the master timeline maps scene time to clip frame index: `frame = floor((t − clip_start) × 30)`. Imported clips are therefore pure functions of `t` too.

### 10.2 Per source

| Source | Produced by | Output for import | Notes | Edge cases |
|---|---|---|---|---|
| Existing SVG proof renderer | `examleaf-svg-scenes`; CLI `PYTHONPATH=src python -m examleaf.cli render <scene.json> --aspect 9:16 --out <dir>` (existing, tested for the four fixtures) | MP4 (existing) → convert to PNG sequence for frame-exact import, or use as a single video element | The proof adapter renders 720×1280 at 24 fps; production is 1080×1920 at 30 fps, and "24 fps only for the proof fixtures" (RD-16). Production-format output from the SVG path is a P1 build item; until then proof renders are reference/regression only, not import material | #20 |
| Manim CE | `examleaf-manim-scenes` | PNG sequence (transparent where needed) | 9:16 frame config to confirm [Hypothesis]; 4–6 workers [N49]; CE only [N48] | #28, #30 |
| three.js | `examleaf-threejs-scenes` via raw seek pipeline [N18] | PNG sequence | GPU/software-GL policy | #65 |
| Blender | `examleaf-blender-scenes`, scripted, seeded, headless | PNG sequence (with alpha if composited) | Blender MCP only as an authoring aid (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §6) | — |
| Procedural/collage HTML scenes | `examleaf-procedural-2d` | Native HTML scene in HyperFrames (no conversion) | Contract C1–C18 | #15–#19 |
| Generated raster assets | `examleaf-mcp-orchestrator` (approved only) | Still images in `assets/` with AssetManifest | No text in images | #54 |

### 10.3 Clip manifest fields [Recommendation]

`clip_id`, `source_skill`, `source_hash` (scene spec + fixture hashes), `renderer_version`, `environment_hash`, `fps` (must be 30), `frame_count`, `width`, `height`, `alpha` (yes/no), `duration_s`, `frames_dir` or `file`, `sha256_per_frame_list` (or a rolling digest), `color_space`, `start_in_master` (seconds, from the cue sheet).

### 10.4 Import rules

1. Frame rate must match 30 fps; no resampling of frame rate inside the master timeline.
2. Prefer PNG sequences over MP4 to avoid parallel video decoding (#20); if a video element is unavoidable, force one worker.
3. Clip audio is never used; all audio comes from the mixed stems.
4. The clip's science content is validated by its own skill; the master timeline may position, scale (uniformly) and fade a clip, but never distort it (no non-uniform scaling that changes angles or ratios) (#64).

---

## 11. Render-box policy (#65)

1. **One reference render box**: a Linux container or WSL2 image pinned by digest (RD-24), with pinned Node 22+, FFmpeg build, Chrome build, Python 3.13, fonts and harness packages.
2. **Environment hash** (OS, Chrome, FFmpeg, Node, Python, package lock hashes, font hashes, harness version) is recorded with every render and enters the render cache key, mirroring the existing engine's cache key (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` "engine key = SHA-256 of scene JSON + aspect + environment …").
3. **No internet after staging** (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2); no secrets on the box.
4. **WebGL**: designated GPU box or software GL, per the decision recorded from doc 01 §2.6; per-box determinism baselines.
5. **Upgrades** (Chrome, fonts, harness, model used to author scenes) re-run the determinism test and the font test card; "Upgraded model/voice/library versions cannot pass solely because an earlier version passed" (`07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` §7).
6. **Concurrency**: workers sized to the box; one worker for video-heavy scenes (#20); Manim 4–6 workers (#30).

---

## 12. Export settings for 9:16

| Setting | Value | Source |
|---|---|---|
| Resolution | 1080×1920 | Vertical-only decision 15 Oct 2026 (supersedes RD-16) |
| Frame rate | 30 fps constant | Vertical-only decision 15 Oct 2026 (supersedes RD-16) |
| Video codec | H.264, yuv420p | Vertical-only decision 15 Oct 2026 (supersedes RD-16) |
| Audio codec | AAC in MP4 for delivery; 48 kHz WAV stems and mixed WAV archived | section 11 playbook audio spec; narration master spec |
| Video bitrate / quality | **verify** per platform and pilot listening/viewing tests (no verified figure in the evidence) | — |
| Audio bitrate | **verify** | — |
| Loudness | Lessons −16 LUFS integrated ±1, ≤ −1 dBTP, re-measured after final mux; Reels: test −14 vs −16 (AD-04) | `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1; [V4-MP] |
| Captions | VTT + SRT (existing) | Vertical-only decision 15 Oct 2026 (supersedes RD-16) |
| Container | MP4 with the index at the front for streaming (standard `-movflags +faststart`) | standard usage |

Example encode from a PNG sequence and a mixed WAV (standard FFmpeg usage; quality settings deliberately omitted until verified):

```sh
ffmpeg -framerate 30 -i renders/<scene>/frames/%06d.png \
       -i audio/mix_48k.wav \
       -c:v libx264 -pix_fmt yuv420p -r 30 \
       -c:a aac -ar 48000 \
       -movflags +faststart -shortest \
       renders/<scene>/<scene>_1080x1920.mp4
```

After encoding: run ffprobe (resolution, fps, duration, audio present), re-measure loudness on the encoded file (existing narration rule), compute the SHA-256, and write the render manifest (existing fields plus `environment_hash`, `determinism_verdict`, `brief_sha256`, `storyboard_approval_id`).

**`-shortest` caution:** it trims to the shorter stream; if the audio is shorter than the video because a protected pause was dropped, this hides a defect. The mux step must first compare durations with the existing 0.05 s tolerance and fail on mismatch rather than trim silently.

---

## 13. Failure catalogue

| Symptom | Cause | Fix | Edge case |
|---|---|---|---|
| Frozen or garbled frames | Wall-clock or played animation | Pure function of `t` | #15 |
| Render fails or wrong length | No `DURATION`/`seek` | Contract lint before render | #16 |
| Frames differ between renders | Unseeded or stateful randomness | Stateless RNG; reverse-order test | #17 |
| Inconsistent state when seeking | Infinite tweens | Finite repeats from `t` | #18 |
| Render hangs | rAF polling | `setTimeout` polling with a deadline | #19 |
| Decoder errors, black frames | Multiple video elements in parallel | One worker; PNG sequences | #20 |
| Renderer won't start | Chrome not found | `CHROME=/path` [N17] | #21 |
| HyperFrames fails | Node < 22 or no FFmpeg | Preflight [N8] | #22 |
| Tofu boxes, broken conjuncts | Missing glyphs; per-code-point animation | Coverage check; per-word animation | #55 |
| Reveals out of sync after re-voicing | Hard-coded times | Cue-sheet driven; re-align | #63 |
| Graph misread during reveal | Camera effects on science | No camera fx on science | #64 |
| 3D frames differ by machine | GPU/driver variance | Fixed box; software-GL test | #65 |
| Silent final video | Audio not requested or not muxed | Mandatory audio stems; mux check | #10 |
| Loudness jumps between scenes | No normalisation by default [N20] | Final normalisation; re-measure | #39 |
| Model returns no video | Model is text-only [N71] | The renderer executes the code | #14 |
