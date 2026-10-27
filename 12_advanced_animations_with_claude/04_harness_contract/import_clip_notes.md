# Importing Manim, SVG, three.js and Blender clips into the master timeline

How clips made by other tools enter the **HyperFrames master timeline** (default) and a **Remotion** composition (benchmark challenger). Companion to `contract.md`.

Labels: **[Recommendation]**, **[Hypothesis]**, **verify** / **verify API** = not in the evidence set; confirm against the pinned tool version before relying on it. Citations `[N#]`, `[V#]` are in `../01_research/`.

**Why clips at all.** HyperFrames is the master timeline; Manim CE, SVG, three.js and Blender produce clips or PNG sequences that are imported into it (report section 2.6). Data-bound science (equations, graphs, structures) still comes from validated fixtures [Recommendation, report section 0 item 11].

---

## 1. Rules that apply to every clip

1. **PNG sequences first, MP4 second.** A PNG sequence needs no decoder, is frame-exact and keeps the master scene a pure function of `t`. MP4 clips are allowed but put the scene on one worker (`SCENE_META.workersMax = 1`, contract section 10) [N70].
2. **Same canvas.** 1080 × 1920 unless the clip is an inset with a declared size. Never scale a raster clip up.
3. **Same fps.** Clip fps equals the master fps (default 30), or an integer divisor of it. Render from the model at 30 fps; do **not** frame-rate-convert a rendered clip. The engine fixtures are 24 fps and their physics, chemistry and biology state is a function of time, so re-render at 30 from the same state rather than resample 24 to 30.
4. **No audio inside a clip.** Strip it. Audio is mixed once, outside (section 6).
5. **Deterministic producers.** Seeded randomness, fixed-step or closed-form physics, no wall clock. Record seeds and versions in the clip manifest.
6. **Science stays traceable.** A clip that shows a value, label or equation is data-bound: it is built from the fixture and the fixture hash goes into the manifest. A decorative clip must not encode data (contract section 9).
7. **No camera effects on measurement or label reveals** (#64).
8. **One manifest per clip** (section 2). The master scene refuses a clip without one.

---

## 2. Clip manifest (`clip.json`, [Recommendation])

```json
{
  "clip_id": "phy-10-03-s04-ray-bend",
  "kind": "png_sequence",
  "path": "clips/phy-10-03-s04-ray-bend/frame_%05d.png",
  "frames": 90, "fps": 30, "width": 1080, "height": 1920,
  "alpha": true, "colour": "sRGB 8-bit RGBA",
  "producer": { "tool": "manim-ce", "version": "<record the real version>", "command": "<exact command>", "seed": 20261014 },
  "fixture_sha256": "<hash of the fixture it was built from, or null for decorative>",
  "frames_sha256_manifest": "clips/phy-10-03-s04-ray-bend/frames.sha256.json",
  "created": "<ISO date>"
}
```

`frames.sha256.json` comes from `python3 determinism_hash_check.py DIR DIR --write-manifest FILE` (comparing a directory with itself writes its manifest; the check passes trivially). Re-rendering a clip twice and comparing the two directories is the producer-side determinism test.

---

## 3. Producers

### 3.1 Manim CE (equations, graphs; best for data-bound math)

- Install: `pip install manim`; verify with `manim --version` [N46]. Use **Manim CE only**. CE and ManimGL are separate, incompatible frameworks [N48] (#28). `examleaf-manim-scenes` is CE. The ARM-macOS cairo prerequisite in [N47] is for ManimGL (#29); CE may have its own system dependencies: **verify**.
- Vertical output: set pixel width 1080, pixel height 1920 and frame rate 30 in the scene or CLI, and make the Manim frame width and height match the 9:16 aspect so shapes are not stretched. Option names (`-r/--resolution`, `--fps`, config fields): **verify** on your Manim CE version.
- Transparent background and PNG output (`--transparent`, `--format=png` or equivalent): **verify** the exact flags and whether alpha is straight or premultiplied (section 6.1).
- Parallel test runs: 4–6 workers; many workers cause out-of-memory errors [N49].
- Equations and axis labels come from the fixture, never typed into the Manim script.

### 3.2 SVG (existing Python SVG → PNG → FFmpeg proof renderer)

- The engine already rasterises SVG with CairoSVG for every frame (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` section 1). Rasterise at 1080 × 1920 and 30 fps from the typed scientific state; keep the vertical layout recomposed, not cropped (the engine has a `test_vertical_not_crop` test).
- Fonts: the proof renderer uses a stand-in font (DejaVu Sans) "for offline proof only"; production brand fonts must be licensed and pinned. Indic text through CairoSVG: **verify** shaping before relying on it (benchmark shaping test card).

### 3.3 three.js and raw Canvas (3D, procedural)

- Use the raw frame pipeline: headless Chrome renders frame `i` as `seek(i / fps)` [N18]. The three.js scene obeys the same contract as any scene: `DURATION`, `async seek(t)`, seeded layouts, orthographic or perspective camera as a function of `t`, physics as closed form or fixed-step replay from 0.
- Export a PNG sequence, not a video.
- **WebGL variance (#65) [Hypothesis].** Render on the one fixed render box; record GPU, driver and browser version in the manifest; run a software-GL comparison before trusting another machine. Flag names: **verify**.

### 3.4 Blender (rare hero 3D)

- Scripted Python, seeded, rendered offline and headless via `examleaf-blender-scenes`. A Blender MCP is an optional authoring aid only (report section 4.6); no verified install evidence exists.
- Output PNG sequence, 1080 × 1920, 30 fps. Command-line options for background mode, output path, format and frame range: **verify** on your Blender build.
- Colour management: set the view transform so rendered pixel values are not tone-mapped differently from the other clips (a "Standard" style transform is the usual choice): **verify** in your Blender version and compare against a known swatch.

---

## 4. Into the HyperFrames master timeline

The master timeline is a scene written to `contract.md`. A clip is just a layer whose frame is a pure function of `t`.

### 4.1 Portable method (works under the contract, no engine API needed)

```js
// Pure mapping from master time to a clip frame index. Hold the last frame; -1 = not started (hide).
const EPS = 1e-6;
function clipFrame(t, clipStart, clipFps, nFrames) {
  if (t < clipStart - EPS) return -1;
  const i = Math.floor((t - clipStart) * clipFps + EPS);
  return Math.min(i, nFrames - 1);
}
```

Tested in Node: 1:1 mapping for 900 frames at matching fps with no off-by-one from `i / fps`; a 15 fps clip on a 30 fps master repeats each frame twice; before start returns -1; after the end holds the last frame.

In `render(t)`: compute `k = clipFrame(t, clipStart, fps, frames)`; if `k < 0` hide the `<img>`; else set `img.src` to the padded frame path and `await img.decode()` inside `seek` (contract section 2.2, item 3). Keep at most a few decoded frames: one 1080 × 1920 RGBA frame is 8,294,400 bytes (about 7.9 MiB) in memory. Clip start times come from the cue sheet (`cues[].at`, kind `reveal`), never hard-coded.

### 4.2 MP4 clips (video-in-video)

- `<video muted playsinline>`, never `autoplay`, never `.play()` (lint F08, F09). Seek with `video.currentTime = t − clipStart` and wait for `seeked` using a `setTimeout` poll with a deadline, not rAF [N69].
- Declare `SCENE_META.workersMax = 1` [N70]; lint F13 enforces it for two or more videos.
- Frame-accurate seeking of inter-frame codecs in Chrome is not guaranteed **[Hypothesis]**. If you must use MP4, re-encode the clip intra-only or all-intra so every frame is a keyframe (FFmpeg: a GOP size of 1; **verify** the flags on your build), and compare its frames against the PNG-sequence version in the benchmark's video-in-video test.

### 4.3 HyperFrames-native clip declaration

How HyperFrames declares a clip on its own timeline (attributes, start and duration properties, track order) is **not in the evidence set**. [V2] shows scenes and audio on a timeline in a HyperFrames side panel, and the repo "ships 21 skills agents load on demand" [N11]. **verify API:** after the third-party admission review, read the HyperFrames skills (`npx skills add heygen-com/hyperframes` [N58]) and the pinned docs, then record the exact clip declaration here. Until then use the portable method in 4.1, which does not depend on it.

---

## 5. Into Remotion (benchmark challenger)

Everything here is **verify API**: the names are general knowledge of Remotion, not evidence. Confirm in `/remotion-best-practices` [N4] and the pinned docs, and run `/remotion-upgrade` first to avoid version drift [N7] (#25).

| Need | Likely Remotion building block (verify) |
|---|---|
| PNG-sequence frame by index | an image component driven by the current frame; static files via its static-file helper |
| Place a clip at a cue time | a sequence wrapper with a `from` frame computed as `round(cueAt × fps)` |
| MP4 inside the composition | its offthread or standard video component |
| Clip fps ≠ composition fps | compute the clip frame index with `clipFrame` semantics; do not rely on automatic playback-rate conversion |
| 1080 × 1920 | composition width and height (benchmark item) |

Remotion's licence terms for commercial use are not in the evidence set: **verify** (benchmark item).

---

## 6. Colour, fps and audio

### 6.1 Colour

- Clips and stills: **sRGB, 8-bit**. PNG sequences keep RGB exactly; do not pass a clip through YUV on the way in.
- Alpha: choose straight (non-premultiplied) alpha for PNG sequences and **verify** that both engines composite it the same way: composite one clip with a soft edge over a known background in HyperFrames and Remotion and compare the edge pixels for halos (benchmark item).
- Final encode: H.264, `yuv420p`, 8-bit, as in the existing previews (High profile; `10_pilots_and_examples/PREVIEW_BENCHMARKS.md` section 3). Tag the stream as BT.709 and the correct range at the final encode only (FFmpeg colour options: **verify** on your build). Convert RGB to YUV exactly once.
- Determinism is judged on the PNG frame hashes before encoding, not on the MP4.

### 6.2 Frame rate

- Master fps is a parameter (default 30). Clip fps = master fps, or an integer divisor (a 15 fps clip on a 30 fps master shows each frame twice, which suits deliberately held stop-motion motion).
- Avoid 29.97 vs 30 mismatches. For MP4 clips check `r_frame_rate` against `avg_frame_rate` with `reference_analysis.sh` (variable fps shows up as a difference); re-encode to constant fps first.
- Never retime by resampling. Re-render from the model at the master fps.
- Clip length in frames = `round(duration × fps)`; the manifest stores it and the master checks it.

### 6.3 Audio

- Master audio **sample rate 48 kHz**. Narration is resampled once to 48 kHz; SFX and music beds are rendered or converted to 48 kHz. Do not resample repeatedly.
- Analysis timings are seconds. When you compute them with librosa, load with `sr=None` or use the same `sr` for loading and for converting frames to seconds; a mismatch makes cues drift against the video [N81] (#35). Use `units='time'` for beats [N39] (#33); an empty beat list is possible for silent or beatless audio [N41] (#34).
- Audio length is exactly `N / fps` seconds: pad or trim the mix so audio and video end together.
- Loudness: [V4-MP] says about −14 LUFS integrated with peaks under −1.5 dBFS (a sample-peak figure); the planning pack tokens say −16 LUFS and −1 dBTP. ~~**Conflict, unresolved here** (see `vertical_safe_zones.tokens.json` `audio.loudness_conflict`).~~ **Resolved (15 Oct 2026 update; decided per AD-04/AD-37):** the current key is `vertical_safe_zones.tokens.json` → `audio.loudness`: house standard −16 LUFS ±1 integrated, true peak ≤ −1 dBTP, measured after the final mux; −14 LUFS only as the Reels A/B variant (`audio.loudness.reels_test_variant`, still under −1 dBTP). `examleaf-audio-production-engineer` applies it as the final mix step; some toolchains do no normalisation unless asked [N20] (#39). Music beds follow `audio.music_policy` (muted under teaching; 20–24 dB under speech in hooks/transitions/recaps/outros only).
- Mux after the determinism test passes, never before.

---

## 7. Per-clip checklist before import

1. `clip.json` present and valid; `frames` equals `round(duration × fps)`.
2. First and last frame exist; no gaps in numbering.
3. Every frame is 1080 × 1920 (or the declared inset size), sRGB.
4. Two producer-side renders of the clip produce identical frame hashes.
5. Fixture hash recorded for any data-bound clip; none for decorative.
6. Alpha edges inspected on a light and a dark background.
7. Imported through `clipFrame` (or the verified engine declaration); lint passes.
8. Single worker declared if any MP4 is used.

## 8. To verify (collected)

Manim CE flags and alpha behaviour; Blender CLI options and colour-management setting; FFmpeg intra-only and colour-tag flags; HyperFrames clip declaration; Remotion component names and composition size settings; software-GL flag; straight vs premultiplied alpha in both engines; Remotion licence.
