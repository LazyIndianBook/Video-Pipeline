# ExamLeaf scene harness contract

**Contract version 1.0.0** · Status: normative for every scene produced by the "Advanced Animations with Claude" layer · Date: 14 Oct 2026

**How to read this file.** MUST, MUST NOT, SHOULD and MAY are used in the usual RFC 2119 sense. Citations `[N#]` and `[V#]` point at `../01_research/RESEARCH_REPORT_advanced_animations_with_claude.md` and `../01_research/SOURCES_and_claims.md`. Labels follow the report: **[Recommendation]** is design judgement, **[Hypothesis]** is plausible but unverified, **verify** means "check against the pinned tool version before relying on it". `#NN` is a row of the report's section 8 edge-case table. Paths that begin with a number and underscore (for example `04_video_engine/…`) are relative to the project ROOT, `ExamLeaf_Video_EdTech_Pipeline/`. Nothing here is a command or version that the evidence set does not contain, except where marked **verify**.

**One-sentence contract.** A scene is a self-contained page that is a pure function of time: given `t` it paints exactly one frame, the same frame every time, in any order, offline.

---

## 1. Scope and terms

| Term | Meaning |
|---|---|
| Scene | One HTML/JS page (plain DOM, Canvas, SVG or three.js) written by Claude Code against this contract. Claude outputs text only [N71]; a renderer executes the scene and produces the video [N18][N72]. (#14) |
| Harness | The program that drives a headless browser: loads the scene, calls `seek(t)` for each frame, captures it, encodes the video. HyperFrames is the default harness; Remotion is benchmarked; a raw Chrome frame pipeline is the third option (report section 2). |
| `t` | Scene time in seconds from scene start. |
| `fps` | Output frames per second. A parameter, default 30. |
| `N` | Frame count, `N = round(DURATION × fps)` [N72]. Frame `i` (0-based) is captured at `t = i / fps`, computed from the integer `i` [N18]. |
| Cue sheet | The JSON file of word times, beats, cues and SFX for one scene (`cue_sheet.schema.json`, report section 5.5). |
| Fixture | The validated science data for the scene (values, units, geometry, labels). Read-only. |
| Level | Conformance level L0, L1, L2 (section 13). |

**Non-goals.** This file does not specify HyperFrames' or Remotion's internal APIs. Where an engine-specific shape matters it is labelled **verify**.

---

## 2. Required exports (Level 0)

A scene MUST define, on `window`:

### 2.1 `window.DURATION`

- A finite number greater than 0: the scene length in **seconds** [N72].
- MUST be set by the time `window.ready` resolves (section 2.3). If the scene reads the duration from a cue sheet, a synchronous default MAY be set at load and replaced when the sheet arrives; a harness that sees `window.ready` MUST wait for it before reading `DURATION`.
- MUST NOT change after `ready` has resolved.
- [Recommendation] Choose `DURATION × fps` to be an integer. If it is not, `N = round(DURATION × fps)` and the last frame time is `(N − 1) / fps`.
- Duration derives from the narration, not the other way round (report section 5.5).

### 2.2 `async window.seek(t)`

- `t`: a finite number of seconds. The scene MUST clamp to `[0, DURATION]`. A non-finite `t` MUST reject with code `E_BAD_T`.
- Returns a Promise. It MUST resolve only when frame `t` is fully painted [N72], defined operationally as all of:
  1. every DOM, SVG and canvas change needed for `t` has been applied;
  2. fonts used by the frame are loaded (`document.fonts.ready` awaited; section 6);
  3. images used by the frame are decoded (`img.decode()` awaited);
  4. video elements used by the frame have fired `seeked` for their target time (section 10);
  5. no asynchronous work is still pending that could change pixels.
- **Pure function of `t`.** `seek(t)` MUST produce the same ~~pixels~~ DOM, style and canvas state for the same `t` regardless of call history: `seek(5); seek(2)` and a fresh page with `seek(2)` MUST give the same ~~frame~~ state (verified for the template: forward, reverse and shuffled orders gave identical DOM and canvas state).
- **Pixels are procedure-deterministic, not order-free (16 Oct 2026, pilot gap L-01).** On Chrome 155/macOS the captured pixels also depend on the seek-and-capture history for layers with CSS `transform` (the compositor's raster-scale cache): a reverse-order or sampled check differs by a few LSBs (PSNR ≈ 45 dB) even when the DOM state is identical. No Chrome flag tested removes it. An identical procedure (fresh page, every frame seeked AND captured in order `0 … N−1`) is byte-identical across runs; the pilot's MP4 SHA-256 matched across runs. So pixel determinism is defined by that procedure (section 11), not by arbitrary seek order. Mitigation: where byte-identity matters, reveal headline and word text with `opacity` (and SVG attribute or canvas positions), not CSS `transform` translate/scale (the template does); render one scene per machine at a time (section 11 item 13).
- **Idempotent.** Calling `seek(t)` twice with no other call between is a no-op the second time.
- **Serialised.** Overlapping calls MUST NOT interleave: the scene queues them in call order.
- MUST NOT wait on `requestAnimationFrame`. rAF does not fire in BeginFrame mode and the render hangs [N69] (#19). The capture that forces a paint is the harness's job. The exact BeginFrame sequence is not in the evidence set: **verify** on the pinned harness.
- MUST NOT start or advance anything in real time (section 4).

### 2.3 Optional-but-recommended exports (required from Level 1)

| Export | Type | Meaning |
|---|---|---|
| `window.ready` | Promise | Resolves when the cue sheet and fixture are loaded, fonts preloaded, DOM built and `DURATION` final. Rejects with a coded error otherwise. `seek` awaits it internally. |
| `window.FPS` | number | The render fps the scene was given. |
| `window.FRAME_COUNT` | number | Convenience copy of `round(DURATION × FPS)`. The harness computes its own `N` and MUST NOT trust this over `round(DURATION × fps)`. |
| `window.SCENE_META` | object | `{ contract: "1.0.0", videoCount: n, workersMax?: 1, notes? }` (section 10, 14). |
| `window.__errors` | array | Error channel (section 12). |
| `window.__cueSource` | string | `"injected"`, `"path"`, `"inline"` or `"inline-fallback"` (section 8). |
| `window.__fixtureSource` | string | Same values, for the fixture. |

---

## 3. HyperFrames adapter: `window.__hf`

HyperFrames compositions expose `window.__hf` with a duration and a seek, and "the renderer never calls play()" [N68] (**contested** in the evidence set).

- A scene intended for HyperFrames SHOULD also expose `window.__hf = { duration, seek(t) }` as a thin adapter over the portable pair of section 2. The template does:
  `window.__hf = window.__hf || { get duration(){ return window.DURATION; }, seek: t => window.seek(t) }`.
- The exact property names, whether `duration` is a number or a function, and whether HyperFrames wants its own timeline registration are **unverified**. Do not rely on the shim: **verify** against the pinned HyperFrames version (benchmark step 0) and record the confirmed shape here in a new contract version.
- If the harness already defines `window.__hf` before the scene runs, the scene MUST NOT overwrite it (the template guards with `||`).
- The portable pair (`DURATION`, `seek`) stays the source of truth for Remotion and the raw pipeline.

---

## 4. Determinism rules

The lint tool `lint_seek_contract.js` enforces these. Rule IDs match its output. "Edge" is the report's section 8 row.

| ID | Rule | Edge | Source |
|---|---|---|---|
| F01–F03 | MUST NOT read the wall clock: `Date.now()`, `new Date()` with no argument, `performance.now()`. Use the `t` passed to `seek`. | #15 | [N68][N18] |
| F04–F05 | MUST NOT use `Math.random()` or `crypto.getRandomValues/randomUUID`. Use a **seeded PRNG** (mulberry32 in the template) built once at load, or the stateless `rngAt(seed, i)`. Never draw from a stateful stream inside `render(t)`: draw order would then depend on seek order. | #17 | [N61] (contested; treat as strong guidance) |
| F06–F07 | MUST NOT use `setInterval` or `requestAnimationFrame` (or `cancelAnimationFrame`) to drive state. | #19 | [N69] |
| F08–F09 | MUST NOT call `.play()` or set `autoplay`. The renderer never plays [N68]; seek `video.currentTime` or a timeline's time instead. | #15 | [N68] |
| F10 | Repeats MUST be finite: no `repeat: -1`, `Infinity`, `iterations: Infinity`, `animation-iteration-count: infinite`. Idle motion is a finite damped pulse or a finite repeat count. | #18 | [V4-MP] |
| F11, W01 | `setTimeout` MUST NOT drive animation or re-schedule its own function. It MAY be used for deadline-bounded polling that never changes visual state (annotate the line `lint-allow: W01`). | #19 | [N69] |
| F12 | MUST render offline. No CDN, no remote `src`/`href`/`url()`/`fetch`/`import`. Everything the scene needs lives next to it. [Recommendation] The harness also blocks outbound requests during render (how: **verify**). | n/a | [Recommendation] |
| F13, W05 | Scenes with 2 or more `<video>` elements MUST declare `SCENE_META.workersMax = 1` (section 10). | #20 | [N70] |
| W03, F14 | CSS `@keyframes`, `animation`, `transition` run on the document timeline, not on `seek(t)`, so frames depend on wall-clock time. ~~Avoid them, or drive them through the Web Animations API (`animation.pause(); animation.currentTime = t * 1000`). **[Hypothesis]**: confirm in the benchmark before using.~~ Set every animated property from `seek(t)` instead. W03 (warning) at `--level 0`; **F14 (error) at `--level 1` and above** (16 Oct 2026, pilot gap L-14). Driving them through the Web Animations API `currentTime` stays **[Hypothesis]** and needs `lint-allow: F14` with a reason. | #15 | [Hypothesis] |
| n/a | **Time-pure effects only.** No composition-wide shake or push-in during measurements or label reveals (#64). | #64 | [Recommendation] |
| n/a | **Stateless physics.** Physics is a closed-form function of `t`, or a fixed-step replay from `t = 0` to `t`. Never integrate incrementally across `seek` calls. | #15 | [Recommendation] |
| n/a | **No audio in the scene.** Narration, music and SFX are mixed outside (48 kHz) and muxed by the pipeline; the cue sheet `sfx[]` is for that mixer. WebAudio output is real-time and non-reproducible. | #10, #63 | [Recommendation] |

`lint-allow: RULEID` on the same line silences one finding. Use it sparingly and say why.

The linter is a regex scanner, not a JavaScript parser. It cannot see `window["Math"]["random"]` or a library that calls `Date.now` internally. The **double-render hash test (section 11)** is the real proof; lint is the cheap early filter.

---

## 5. Self-containment, fixed layout, colour

- **Offline.** No network at render time (F12). Third-party libraries are copied next to the scene after the admission review in `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` section 11. Pin versions.
- **Canvas.** The scene is laid out in fixed pixels for **1080 × 1920** (9:16). The harness MUST set the viewport to 1080 × 1920 and device scale factor 1. The scene MUST NOT lay out from `vw`, `vh`, `innerWidth` or `innerHeight`. The exact flag or API names for the pinned browser: **verify**.
- **Colour.** sRGB, 8-bit. The harness MUST record the browser version in the manifest. How to force a colour profile in headless Chrome: **verify**.
- **Tokens.** Safe zones, minimum text sizes and hold times come from `vertical_safe_zones.tokens.json`. Insets there are **PLACEHOLDERS**: no verified pixel values exist (report section 7 rule 9).
- **Folder budget.** [Recommendation] Keep a scene folder under 100 MB. A Codex archive build fails above Codex's 100 MB upload limit [N12] (#24); this matters only if you build that way.

---

## 6. Fonts (#55)

- Fonts MUST be present before the first `seek` returns. A frame painted with a fallback font is a different frame.
- Production fonts are licensed, pinned local files loaded by `@font-face` with `url("fonts/…")`. No CDN, no Google Fonts at render time.
- The scene MUST explicitly load each family and weight it uses with sample text that exercises its glyphs: `await document.fonts.load('700 40px "Noto Sans Devanagari"', 'प्रकाश क्ष ज्ञ')`. `document.fonts.ready` alone resolves when nothing is currently loading, so it does not trigger loads for faces no element has requested yet (standard CSS Font Loading behaviour; **verify** on the pinned Chrome).
- `document.fonts.load()` cannot tell you whether a *system-installed* font exists or whether a glyph fell back. Verify coverage out of band: `preflight.sh` (fc-list on U+0915 Devanagari, U+0995 Bengali, U+09F0 Assamese RA) and the Indic shaping test card in the benchmark. Report: [Hypothesis] per report section 4.4.
- **Indic text.** Animate per **word** or per grapheme cluster, never per code point (conjunct breakage). The template uses one `inline-block` span per word. If letter animation is needed, segment with `Intl.Segmenter` at grapheme granularity (**verify** support and Devanagari/Bengali behaviour on the pinned Chrome).
- Set `lang` on text containers (`hi`, `as`, `bn`, `en`) so font selection and line breaking follow the script.
- Line height at least 1.4 for Devanagari and Bengali-Assamese (marks above and below the line). Observed on the build machine: a Hindi sample (`प्रकाश`) shaped correctly with a macOS system font in Chrome 155, using the template.

---

## 7. Canvas, fps and frame math

- Canvas: **1080 × 1920**. fps: **parameter**, default **30**. The engine fixtures are authored at 24 fps; that does not constrain the render fps because cue times are in seconds.
- Time is continuous. Scene code MUST NOT snap time to frames. It compares times with a tolerance `EPS = 1e-6 s` so that float error in `i / fps` cannot flip a reveal by one frame (the template's `Timeline.at` and boil step do this).
- `N = round(DURATION × fps)`. Frame `i` is captured at `t = i / fps` using the integer `i` [N18]. The harness MUST NOT accumulate `t += 1/fps`.
- The cue sheet's `fps` is the intended fps. If the render fps differs, the render fps wins and the scene logs `W_FPS_MISMATCH`. Cue times are never rescaled.
- Example: the 7.4 s example sheet at 30 fps gives 222 frames. Verified in the template: `DURATION = 7.4`, `FRAME_COUNT = 222`.

---

## 8. Cue sheet loading

The scene MUST NOT hard-code reveal times. It reads `cues[].at` and `words[].t0` (report section 5.5).

**Precedence (the template implements this):**
1. `window.__CUE_SHEET__`, injected by the harness before the scene runs (`source = "injected"`). How a harness injects it (for example a pre-navigation script hook) is engine-specific: **verify**.
2. `?cues=<relative path>` fetched with `fetch` (`source = "path"`).
3. The inline `<script type="application/json" id="cue-sheet-inline">` block (`source = "inline"`).

**file:// caveat (observed).** In headless Chrome 155 on the build machine, `fetch("cue_sheet.example.json")` from a `file://` page failed with "Failed to fetch". The same page served from `http://127.0.0.1` loaded it (`source = "path"`, 222 frames). Serve the scene folder over local HTTP, or inject the sheet. [Observation on one machine; recheck on yours.]

**Failure policy.**
- If `?cues=` was given and fails, the template logs `W_CUES_FALLBACK`, sets `__cueSource = "inline-fallback"` and continues, so authors can still preview. With `?strict=1` it rejects with `E_CUES_LOAD`.
- **Production renders MUST require `__cueSource ∈ {"injected","path"}` and no `W_*_FALLBACK` entries.** A silent fallback would hide a regenerated-narration mismatch (#63).
- Validate the sheet before rendering: `python3 validate_cue_sheet.py SHEET.json --production`. The scene only does light sanity checks.

**Rules.**
- A reveal lands **on its word's `t0`, or up to 0.05 s before it** [V4-MP]. The template reveals at `t0 − 0.05`. The validator rejects a reveal with `at > word.t0` and warns above 0.10 s early.
- A cue whose `element_id` is not in the DOM MUST be reported (`W_CUE_NO_ELEMENT`), never ignored silently.
- If narration is regenerated: re-align, rebuild the sheet, re-validate, re-render. Scene code does not change (#63).
- The sheet's `script_sha256` ties the timings to the approved script. The animation agent never edits approved text.
- **Optional `meta` fields (16 Oct 2026, pilot gaps L-03, L-05).** `words[]` strips punctuation and says nothing about pauses, so the builder MAY add: `meta.beats_text[]` = `{id, slot, text, headline, start, end, word_range}` per script beat (`text` verbatim with punctuation intact, for disclosure lines and headlines); `meta.think_windows[]` = `{beat, seconds, start, end}` per predict pause (when the "Pause. Predict." plate shows). Times are scene-local seconds. A scene that shows verbatim text reads it from `beats_text`, never from re-joined `words[]`. The schema documents these under `meta` and does not restrict `meta`.
- **Scene boundaries sit on the frame grid.** Each scene start is snapped down to a whole frame of the narration timeline, and scene-local time (all `t0`, `at`, `start`, `end`) starts at the snapped scene start, so `duration × fps` is an integer (16 Oct 2026, L-05).

---

## 9. Fixtures: read-only, traceable

Accuracy invariant (report section 9): any glyph that encodes science is traceable to a fixture field.

- The scene receives the fixture from `window.__FIXTURE__`, `?fixture=<path>` or an inline block, with the same precedence and failure policy as the cue sheet.
- The scene MUST deep-freeze it (`Object.freeze`) and MUST NOT mutate, round, reformat or "fix" any value. No unit conversions that change displayed values.
- Every science glyph on screen (numbers, units, chemical formulae, labels, equation text, axis names) MUST come from a fixture field and MUST be marked `data-fx="path.to.field"` on its DOM element, so `examleaf-anim-qa` can diff rendered text against the fixture. Static labels and units are science too: the template reads `display.r_label` and `display.r_unit` from the fixture.
- Decorative layers (confetti, boil, paper textures) MUST NOT encode data: no position, size, count or colour that a student could read as a value.
- Decoration MUST NOT contradict the science: a wobble must not change an angle, ratio or direction the lesson teaches (report section 7 rule 13).
- A missing fixture field is an error (`E_FIXTURE_MISSING`), never a default.

---

## 10. Video-heavy scenes and workers (#20, #65)

- Chrome cannot seek several video elements at once without running out of decoders; video-heavy compositions should drop to a single worker [N70] (#20).
- **[Recommendation] threshold (the report does not define "video-heavy"):** 2 or more `<video>` elements in one scene, or any scene that imports MP4 clips, is video-heavy. It MUST declare `window.SCENE_META.workersMax = 1`. The harness MUST use `min(requested, workersMax)` workers. Lint rule F13 enforces the declaration; W05 prompts for it when there is one video.
- Scenes without video MAY render with parallel workers: the raw pipeline renders "frame i as seek(i / fps) across parallel workers" [N18]. Fix the worker count in the benchmark and the manifest.
- **Prefer PNG sequences over `<video>`** for imported clips (`import_clip_notes.md`): no decoder, frame-exact, and the scene stays a pure function of `t`.
- **Headless WebGL variance (#65) [Hypothesis].** GPU and driver differences can change 3D frames between machines. Render three.js clips on one fixed render box, record GPU and driver in the manifest, and run a software-GL fallback comparison before trusting a second machine. The flag for software GL: **verify**.

---

## 11. Harness obligations

A conforming harness (HyperFrames wrapper, Remotion adapter, or raw pipeline) MUST:

1. **Preflight.** Run `preflight.sh`: Node 22+ and FFmpeg [N8] (#22), Chrome or `CHROME` [N17] (#21), Indic fonts (#55), disk space. FAIL stops the job (exit 1).
2. **Honour `CHROME=/path`** to choose the browser binary [N17] (#21).
3. **Lint** the scene (`lint_seek_contract.js --level N`) and **validate** the cue sheet before rendering. Violations stop the job (exit 1).
4. **Load** the page with the parameters (`fps`, `cues`, `fixture`, `seed`), then `await window.ready` if present, then read `window.DURATION`. Missing `DURATION` is `E_NO_DURATION`.
5. **Render loop.** For `i` in `0 … N−1`: `await window.seek(i / fps)`, capture, write the frame. Frames are PNG (lossless) until the final encode.
6. **Poll with `setTimeout` loops and a deadline, never rAF** [N69] (#19). Default per-seek timeout **30 s**, ready timeout **60 s** [Recommendation: tune from the benchmark]. A timeout is `E_SEEK_TIMEOUT`, exit 4.
7. **Read `window.__errors` after every seek.** Any entry with `severity: "error"` fails the render (exit 4). Warnings are copied into the manifest.
8. **Workers.** Use `min(requested, SCENE_META.workersMax ?? requested)`; 1 for video-heavy scenes [N70].
9. **Seed.** Pass a fixed integer seed, never one derived from time. Record it.
10. **Write a manifest** next to the frames (below).
11. **Encode** after the determinism test passes. Audio: 48 kHz, mixed outside the scene, muxed by the pipeline (`import_clip_notes.md` section 6).
12. **No network** during render (F12). Block it at the harness (**verify** how).
13. **One render per machine at a time** (16 Oct 2026, pilot gap L-02), or full per-scene browser isolation. Two concurrent renders gave 2 mismatched frames of 831 in one pilot scene; serial renders matched.

**Render manifest** (JSON, one per render): scene path and sha256; cue sheet sha256 and `__cueSource`; fixture sha256 and `__fixtureSource`; `fps`, `DURATION`, `N`; viewport; workers; seed; lint report (or its hash); `window.__errors`; browser name and version; Node version; FFmpeg version; OS and architecture; GPU and driver if WebGL is used; per-frame sha256 file (`determinism_hash_check.py --write-manifest`); timings (ready ms, mean seek ms, total ms); harness name and version.

**Double-render determinism test (mandatory from Level 1).** Determinism means *identical procedure, identical bytes* (section 2.2, 16 Oct 2026). The harness MUST verify by re-running the identical procedure (fresh page, every frame seeked and captured in order `0 … N−1`) and comparing every frame hash. A reverse-order, shuffled or sampled re-render is not a valid check: on Chrome 155 it differs by a few LSBs on transformed layers without any scene defect.
1. Render the whole scene twice, in two separate harness processes, into two empty directories, same machine, same pinned browser, same seed, same in-order procedure, one render at a time (item 13).
2. `python3 determinism_hash_check.py DIR_A DIR_B`. Exit 0 means every frame is byte-identical. Exit 1 reports the first differing frame index.
3. Hash **frames**, not the encoded MP4: encoders may embed metadata that differs between runs.
4. Benchmark runs compare every repeat against repeat 1 (`../07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md`).
5. Evidence from the template (not a harness run): five frames captured by two separate headless Chrome 155 processes (`--screenshot`, not BeginFrame) were byte-identical on the build machine. That shows the template is deterministic in that setup; it says nothing about a full harness.

**Setup notes.**
- HyperFrames clone: `GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` skips LFS payloads [N13] (#23). Do this only after the third-party admission review (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` section 11).
- After `npx skills add …`, confirm `.claude/skills` exists as a symlink to `.agents/skills` [N66][N67] (#26). `preflight.sh` warns when it does not.

---

## 12. Exit codes and error reporting

**Exit codes** (shared by every script in this folder and recommended for harness wrappers):

| Code | Meaning | Used by |
|---:|---|---|
| 0 | OK | all |
| 1 | Check failed: lint errors, invalid cue sheet, frame hashes differ, preflight FAIL, selftest failed | `lint_seek_contract.js`, `validate_cue_sheet.py`, `determinism_hash_check.py`, `preflight.sh` |
| 2 | Usage or I/O error: bad arguments, unreadable input | all |
| 3 | A required external tool is missing (ffmpeg, ffprobe) | `reference_analysis.sh` |
| 4 | Render failure: seek rejected or timed out, scene reported an error, browser crashed | harness wrappers |
| 5 | Reserved for orchestration policy stops (budget or iteration cap reached) | `examleaf-effort-governor` |

**Scene error channel.** `window.__errors` is an array of `{ code, severity: "error" | "warning", message, t }`. Scenes MUST report, never swallow. A failing `seek` rejects with an `Error` whose `.code` matches.

| Code | Severity | Raised when |
|---|---|---|
| `E_NO_DURATION` | error | harness: `DURATION` missing or not finite after `ready` |
| `E_BAD_T` | error | `seek` got a non-finite `t` |
| `E_CUES_LOAD`, `E_FIXTURE_LOAD` | error | path load failed in strict mode |
| `E_CUES_INVALID` | error | sheet fails the scene's sanity check |
| `E_FIXTURE_MISSING` | error | a `data-fx` path is absent from the fixture |
| `E_FONT_LOAD` | error | a declared font failed to load |
| `E_ASSET_LOAD` | error | an image failed to decode |
| `E_READY` | error | any other failure while building the scene |
| `E_SEEK_TIMEOUT` | error | harness: `seek` exceeded the deadline |
| `W_CUES_FALLBACK`, `W_FIXTURE_FALLBACK` | warning | path load failed, inline copy used (not valid for production) |
| `W_FPS_MISMATCH` | warning | cue sheet fps differs from render fps |
| `W_HOLD_SHORT` | warning | headline hold below the token minimum |
| `W_CUE_NO_ELEMENT` | warning | a cue targets a missing element |
| `W_TITLE_TRUNCATED` | warning | headline had more words than the template shows |

Human-readable text goes to stderr; machine-readable JSON to stdout (the lint, validator `--json`, hash check `--json`).

---

## 13. Conformance levels

| Level | Name | Requirements | Proven by |
|---|---|---|---|
| **L0** | Seekable | `window.DURATION` and `async window.seek(t)` per [N72]; no wall clock, rAF, `setInterval`, `.play()`, infinite repeats; offline. | `node lint_seek_contract.js --level 0 SCENE` exits 0 |
| **L1** | Deterministic | L0 plus: `window.ready`; seeded PRNG only; fonts preloaded; cue sheet from a path (or injected) and valid; fixture frozen and read-only; `__errors` channel; single worker declared when video is present; no CSS animation/transition (F14); **double-render hash identical** ~~.~~ for every frame when the identical in-order procedure is re-run (section 11; reverse or sampled orders are not the test, 16 Oct 2026). | `lint --level 1`; `validate_cue_sheet.py`; `determinism_hash_check.py` exit 0 |
| **L2** | Production | L1 plus: `SCENE_META.contract`; layout from the safe-zone tokens; headline and equation hold times met; `data-fx` on every science glyph and a fixture-vs-DOM text diff with zero mismatches; flash check; `validate_cue_sheet.py --production`; `examleaf-anim-qa` green; (`--hf`) a `window.__hf` adapter for HyperFrames scenes. | `lint --level 2 [--hf]`; `examleaf-anim-qa` |

A scene's level is the highest level whose checks all pass. Release requires L2 and the project's human gates; no overall score may hide a critical science error (`04_video_engine` acceptance gates).

---

## 14. Versioning

- **Contract version** is semantic: `MAJOR.MINOR.PATCH`. Current: **1.0.0**.
  - MAJOR: a change that can break an existing conforming scene (a required export or its meaning changes).
  - MINOR: a new optional export, rule at warning severity, error code or level-2 check.
  - PATCH: clarification, typo, new example.
- Scenes declare it: `window.SCENE_META.contract = "1.0.0"`. A harness that implements `X.Y` accepts scenes declaring `X.y` with `y ≤ Y`, and MUST refuse a different MAJOR.
- Other versioned artefacts: `cue_sheet.schema.json` (`schema_version: "1.0"` inside each sheet), `vertical_safe_zones.tokens.json` (`token_version`), `lint_seek_contract.js` (prints `contract_version`). Any change to a rule or schema MUST re-run all `--selftest`s and add a row below.
- The cue-sheet and token versions are independent of the contract version.

| Contract | Date | Change |
|---|---|---|
| 1.0.0 | 14 Oct 2026 | Initial. L0 per [N72]; L1/L2 added by ExamLeaf; `window.__hf` shape recorded as contested [N68]. |
| 1.0.0 (amended) | 16 Oct 2026 | Pilot gaps: pixel determinism defined by the identical in-order procedure (2.2, 11, 13; L-01); one render per machine (11.13; L-02); F14 = CSS animation/transition is an error from L1 (4; L-14); optional `meta.beats_text[]`, `meta.think_windows[]` and frame-grid scene boundaries (8; L-03, L-05). Version number not bumped so pilot scenes declaring 1.0.0 stay valid; bump at the next release. |

---

## 15. Traceability to the report's edge cases

| # | Edge case | Where handled |
|---|---|---|
| 14 | Expecting an MP4 from the model | Section 1: scene is code, harness renders [N71] |
| 15 | Wall-clock animation | F01–F03, F08–F09, W03; sections 2.2, 4 |
| 16 | Missing seek contract | R01–R03 at L0; section 2 |
| 17 | Unseeded randomness | F04–F05; section 4; hash test (section 11) |
| 18 | Infinite repeats | F10; finite `pulse` in the template |
| 19 | rAF polling | F06–F07, F11, W01; sections 2.2, 11.6 |
| 20 | Multiple video elements | F13, W05; section 10 |
| 21 | Chrome not found | Section 11.2; `preflight.sh` |
| 22 | Old Node / no FFmpeg | `preflight.sh` |
| 23 | Heavy clone | Section 11 setup notes [N13] |
| 24 | Archive too big | Section 5 folder budget [N12] |
| 26 | Skills invisible to Claude | Section 11 setup notes; `preflight.sh` check 8 |
| 55 | Indic glyph gaps | Section 6; `preflight.sh` fonts check |
| 63 | TTS regenerated | Section 8; `script_sha256` |
| 64 | Time-wide effects | Section 4 |
| 65 | Headless WebGL variance | Section 10 |

---

## 16. Open items to verify

1. `window.__hf` exact shape and clip/timeline attributes [N68] (contested): HyperFrames, pinned version.
2. BeginFrame capture sequence and how a harness injects `window.__CUE_SHEET__` before scene scripts.
3. Chrome flags for device scale factor 1, sRGB profile and software GL.
4. `document.fonts` loading semantics and `Intl.Segmenter` behaviour for Devanagari and Bengali-Assamese on the pinned Chrome.
5. CSS animations driven through the Web Animations API `currentTime` (W03).
6. How each engine blocks network access during render.
7. Remotion mapping (section 17): all API names.
8. Timeout defaults (30 s per seek, 60 s ready) and the "video-heavy" threshold: tune from the benchmark.
9. Hindi/Assamese hold multiplier (1.5x) and all safe-zone insets: measure.
10. Whether [N61] (pure function of time) holds in every engine; it is flagged contested.

---

## 17. Remotion mapping (informative, **verify API**)

Remotion is frame-based React. It satisfies the *semantics* of this contract rather than the `seek(t)` surface. The names below come from general knowledge of Remotion, not from the evidence set; check each against the pinned version and the `/remotion-best-practices` skill [N4] before use.

| Contract clause | Remotion equivalent (verify) |
|---|---|
| `DURATION` | composition `durationInFrames` and `fps`; derived from the same cue sheet duration |
| `seek(t)` | the current frame is the only input (`useCurrentFrame`); `t = frame / fps` |
| Seeded PRNG | Remotion's seeded `random(seed)` helper, or the same mulberry32 |
| No wall clock / rAF | the same rules; pure of `frame` |
| Cue sheet | input props or fetched at build; same JSON and schema |
| Fonts | font loading API with `delayRender`-style gating (verify) |
| Video-in-video | its video components; behaviour is a benchmark item |
| 1080 × 1920 | composition width and height (benchmark item) |

The benchmark writes the Remotion version of each scene from the same brief, cue sheet and fixture; it does not port the HTML scene.

---

## Appendix A. Smallest conforming scene (Level 0)

```html
<canvas id="c" width="1080" height="1920"></canvas>
<script>
  window.DURATION = 3;                         // seconds [N72]
  window.seek = async (t) => {                 // pure function of t [N72]
    const g = document.getElementById('c').getContext('2d');
    g.fillStyle = '#F7F9FC'; g.fillRect(0, 0, 1080, 1920);
    g.fillStyle = '#185ABD'; g.fillRect(100 + 300 * Math.min(t / 3, 1), 900, 120, 120);
    await document.fonts.ready;                // nothing to paint after this
  };
</script>
```

Run `node lint_seek_contract.js --level 0 file.html`. For L1 and L2 start from `scene_template.html`.
