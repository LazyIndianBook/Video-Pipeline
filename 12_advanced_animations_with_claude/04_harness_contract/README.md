# 04_harness_contract: the scene contract and its tools

**Contract version 1.0.0.** Everything here is stdlib Python 3, dependency-free Node, bash 3.2+ or plain HTML. No installs, no network, no CDN.

## What the contract is

Claude writes animation code; it does not output video [N71]. A renderer loads that code in headless Chrome, sets a time `t`, captures a frame, and encodes the frames [N18][N72]. So every scene must be **a pure function of time**: `window.DURATION` (seconds) and `async window.seek(t)` that resolves when frame `t` is fully painted [N72]. No wall clock, no `Math.random` (seeded PRNG instead) [N61], no `setInterval` or rAF-driven state [N69], finite repeats, fonts preloaded before the first seek, 1080 × 1920 at a parameterised fps (default 30), a cue sheet read from a path, fixtures read-only, a single worker for video-heavy scenes [N70].

The same contract serves HyperFrames (default master timeline), Remotion (benchmark challenger, semantic mapping only) and the raw Canvas/SVG/three.js pipeline. Rules, error codes, exit codes, conformance levels (L0 seekable, L1 deterministic, L2 production) and versioning are in `contract.md`. Facts that are contested or unsourced are labelled and collected as "verify" items there.

## File index

| File | What it is | Run it |
|---|---|---|
| `contract.md` | The normative contract: exports, determinism rules (lint rule IDs), fonts, fps and frame math, cue-sheet loading, fixtures, workers, harness duties, exit and error codes, levels, versioning, edge-case traceability, verify list | read |
| `scene_template.html` | A complete runnable scene (229 lines since 15 Oct 2026, no deps): cue-sheet loader with inline fallback, mulberry32 and a stateless `rngAt`, tween timeline (cubic-out, expo-out, easeOutBack), word-keyed text reveal at `t0 − 0.05`, finite pulse, seeded decoration, safe-zone overlay (`?safe=1` or key S), `seek(t)` that resolves after `document.fonts.ready`, `window.__hf` shim | open `scene_template.html?t=2&safe=1` in Chrome |
| `lint_seek_contract.js` | Static contract check; JSON report on stdout, findings on stderr; exit 1 on violations | `node lint_seek_contract.js --level 1 scene.html` |
| `determinism_hash_check.py` | SHA-256 of every frame in two directories; first differing frame and count | `python3 determinism_hash_check.py DIR_A DIR_B` |
| `cue_sheet.schema.json` | JSON Schema draft-07 for the cue sheet (report section 5.5) | read |
| `cue_sheet.example.json` | Valid 7.4 s refraction example, Hindi and English words, 222 frames at 30 fps | read |
| `validate_cue_sheet.py` | **The only cue-sheet validator** (15 Oct 2026: the skill-local copy in `examleaf-cue-sheet` was deleted; `build_cue_sheet.py` imports this file by path). Structure (driven by the schema file) plus semantics: monotonic times, non-overlapping words, cues inside the duration, reveal lead, path safety, hashes | `python3 -B -I validate_cue_sheet.py sheet.json [--production]` |
| `preflight.sh` | PASS/WARN/FAIL table: Node 22+ [N8], FFmpeg and ffprobe, Python 3.11+, Chrome or `CHROME` [N17], Devanagari and Bengali-Assamese fonts, disk, skills symlink [N66][N67]; with `--workspace` (15 Oct 2026, audit M11): secret scan (`sk-ant-`, `AKIA`, private-key blocks, `api_key=`), ultracode-effort scan and unversioned-model-alias scan of the job folder (file names only, never the match) | `bash preflight.sh [--dir PATH] [--workspace JOB_DIR]` |
| `vertical_safe_zones.tokens.json` | 1080 × 1920 canvas, zones (**single owner** of the zone shares and `zones.side_margin_min_px` = 96 since 15 Oct 2026, AD-42), **placeholder** platform insets, minimum text sizes scaled from the 1920-wide master (rule stated inside), hold times, motion numbers, flash policy, audio | read |
| `reference_analysis.sh` | ffprobe fps and duration, FFmpeg scene-change cuts (`select='gt(scene,0.3)',showinfo`), a still per shot, median shot length | `bash reference_analysis.sh video.mp4 out_dir` |
| `import_clip_notes.md` | Importing Manim, SVG, three.js and Blender clips into HyperFrames and Remotion; colour, fps, 48 kHz audio | read |

Related: `../07_benchmark_and_pilot_plan/` (benchmark, pilot, record sheets) and `../01_research/` (report and sources).

## Quick start

```sh
bash preflight.sh --dir /path/for/frames --workspace /path/to/job   # is the box ready? (+ secret/ultracode/alias scans)
node lint_seek_contract.js --level 1 scene.html # contract lint
python3 -B -I validate_cue_sheet.py scene.cues.json --production   # cue sheet (the only validator)
# render twice with your harness into DIR_A and DIR_B, then:
python3 determinism_hash_check.py DIR_A DIR_B   # exit 0 = every frame identical
```

Serve the scene folder over local HTTP when using `?cues=` (a `file://` page could not `fetch` it in the Chrome tested; see `contract.md` section 8).

## How the skills use these files

| Skill (report section 10) | Uses | For |
|---|---|---|
| **`examleaf-motion-harness`** (item 5, extends `examleaf-web-composition`) | `contract.md` (embed or link from SKILL.md), `scene_template.html` (the starting copy for every scene), `lint_seek_contract.js` (pre-render gate), `determinism_hash_check.py` (double-render test), `preflight.sh` (render-box check), `import_clip_notes.md`, tokens | Writing and gating scenes. Edge cases 14–24, 26, 65. |
| **`examleaf-cue-sheet`** (item 11, extends the speech-animation synchronizer and alignment skill) | `cue_sheet.schema.json`, `cue_sheet.example.json`, `validate_cue_sheet.py` (imported by path by `build_cue_sheet.py`; the skill has no validator of its own since 15 Oct 2026), `contract.md` section 8 | Merging word timings, beats and SFX into the canonical sheet; re-validating after every TTS regeneration; `--production` before release. Edge cases 33, 35, 63. |
| **`examleaf-anim-qa`** (item 14, extends visual-QA and audio-caption-QA) | `lint_seek_contract.js --level 2`, `determinism_hash_check.py`, `validate_cue_sheet.py --production`, the tokens (safe zones, minimum sizes, hold times, flash policy), the `data-fx` rule in `contract.md` section 9, the template's overlay (`?safe=1`) | Safe-zone, hold-time, flash and determinism checks, fixture-vs-DOM text diff, `__cueSource` and `__errors` review. Edge cases 12, 17, 39, 50, 51, 56. |
| **`examleaf-vertical-adapt`** (item 15) | `vertical_safe_zones.tokens.json` (zones, insets, type-size scaling rule, hold times), `scene_template.html` (zones built from the tokens), `contract.md` section 5, the Reel cut list in `../07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md` section 3 | Re-laying 16:9 guides and references into top title / middle visual / bottom caption, and cutting sub-range Reels. Edge cases 49, 51. |
| **`examleaf-reference-analyzer`** (item 2) | `reference_analysis.sh` | Turning a reference video into numbers: fps, duration, cut times, median shot length, a still per shot, a variable-fps flag. Feeds the brief. Analysis only; never reuse the reference's assets. |

## Test evidence (build machine: macOS arm64, Python 3.14.2, Node 20.19.4 and 24.6.0, Chrome 155.0.8059.41)

| Script | `--selftest` | Result |
|---|---|---|
| `lint_seek_contract.js` | 28 assertions: good sample clean (strict, level 2, `--hf`), 22 rule IDs found in the bad sample, level 0 vs 1, line numbers | 0 failed, exit 0 (also on Node 24.6.0 and 14.21.3) |
| `determinism_hash_check.py` | 7 assertions: identical, differing, missing, extra, natural sort, empty dirs, glob | 0 failed, exit 0 |
| `validate_cue_sheet.py` | 25 assertions: schema keywords, example valid, 19 mutations rejected, boundary cases | 0 failed, exit 0 |
| `preflight.sh` | 13 helper assertions (15 Oct 2026: +4 scanner tests on synthetic files, including "this script does not match its own patterns"); lists the 11 checks; never evaluates the environment | 0 failed, exit 0 |
| `reference_analysis.sh` | 13 assertions on an embedded showinfo sample (parser, de-duplication, shot table, median and mean, fps fractions, JSON helpers) | 0 failed, exit 0 |

Additional checks done:
- `scene_template.html` passes `lint_seek_contract.js --level 2 --hf --strict` (0 errors, 0 warnings). Its inline cue sheet validates.
- In headless Chrome 155 the template gave identical DOM and canvas state for forward, reverse and shuffled seek orders, clamped out-of-range `t`, serialised overlapping seeks, and rejected `NaN` with `E_BAD_T`. Five frames captured by two separate Chrome processes were byte-identical (`determinism_hash_check.py` exit 0). That is `--screenshot` capture, not a BeginFrame harness.
- `fetch("cue_sheet.example.json")` from a `file://` page failed in this Chrome; from `http://127.0.0.1` it worked (222 frames, 7.4 s). Strict mode rejected cleanly.
- A Hindi caption shaped correctly (conjunct `प्र` formed) with a macOS system font. This is not a substitute for the native-reader card in the benchmark.
- `reference_analysis.sh`: the glue (probe, scene-change parse, stills, JSON) ran end to end against stub `ffmpeg`/`ffprobe` commands. It was **not** run with real FFmpeg, which is not installed on the build machine.
- `preflight.sh` run for real on the build machine: FAIL on three checks (active Node is 20.19.4, no ffmpeg, no ffprobe); with Node 24.6.0 selected Node passes. Chrome, fonts (including U+09F0) and disk passed.

## Not verified (see `contract.md` section 16)

HyperFrames' `window.__hf` shape [N68] (contested), BeginFrame capture sequence, Chrome flags, how each engine blocks network access, Remotion's licence and APIs, the timeout and "video-heavy" thresholds, the Indic hold multiplier, all safe-zone insets (placeholders), and the real FFmpeg showinfo format on your build.

## Conflicts surfaced, not resolved

- ~~Type sizes: the source tokens carry two ranges (message 04 vs planning pack). Both are scaled in the tokens file; minimums use the larger.~~ *Resolved: RD-01 (07/10) picks the message-04 ranges; planning-pack ranges are only a floor for secondary text (note updated 15 Oct 2026).*
- ~~Loudness: about −14 LUFS and −1.5 dBTP ([V4-MP]) vs −16 LUFS and −1 dBTP (planning pack).~~ *Resolved per AD-04/AD-37 (corrected 15 Oct 2026): house −16 LUFS / −1 dBTP; [V4-MP]'s −1.5 is a sample-peak dBFS figure, not dBTP; −14 LUFS is only the Reels A/B variant. Key: `audio.loudness`; music levels: `audio.music_policy`.*
- fps: engine fixtures are 24 fps; the contract renders at a parameter (default 30). Cue times are in seconds, so this is safe.


## Integration note (15 Oct 2026)

- `03_skills/examleaf-reference-analyzer/scripts/analyze_reference.py` is the **canonical** reference analyser (richer output, self-tested, JSON report). `reference_analysis.sh` is the thin shell equivalent for quick manual use. Both exit **2** when FFmpeg/ffprobe is missing.
- `lint_seek_contract.js` and `determinism_hash_check.py` in this folder are canonical; the copies under `03_skills/examleaf-motion-harness/scripts/` must stay byte-identical (`cmp`), and that skill documents the drift check. ~~`03_skills/examleaf-cue-sheet/scripts/validate_cue_sheet.py` is a separate, skill-owned validator that must agree with `cue_sheet.schema.json`.~~ *15 Oct 2026 (audit M7): that copy was deleted; `validate_cue_sheet.py` here is the only validator, and the cue-sheet builder's selftest runs its output through it with `--production`.*
- The `audio` block in `vertical_safe_zones.tokens.json` now records the loudness decision (AD-04): −16 LUFS / −1 dBTP house standard; −14 LUFS only as a Reels A/B variant. *Corrected 15 Oct 2026: the variant's −1.5 is `sample_peak_dbfs` (original [V4-MP]), not dBTP; the variant stays under −1 dBTP. Music: one `audio.music_policy` (muted under teaching; 20–24 dB under speech in hooks, transitions, recaps and outros).*
