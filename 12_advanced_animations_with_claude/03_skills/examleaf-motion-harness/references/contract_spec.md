# Contract conformance spec

The contract itself is `12_advanced_animations_with_claude/04_harness_contract/contract.md` (owned by the harness-contract folder). This file maps each requirement to how this skill checks it. Rule IDs are those of `lint_seek_contract.js`; levels follow the linter's conformance levels (contract.md §13 as referenced by the scripts).

## 1. Requirement matrix

| Requirement | Level | Lint rule | Edge case | Evidence | Runtime check |
|---|---|---|---|---|---|
| `window.DURATION` set, in seconds | 0 | R01 | #16 | [N72] | frame count = round(DURATION × fps) |
| `window.seek(t)` exported | 0 | R02 | #16 | [N72] | renderer seeks every frame |
| `seek` is async and resolves when frame t is painted | 0 | R03 (warning) | #16 | [N72] | double render identical |
| `window.ready` Promise (cue sheet, fixtures, fonts loaded before first seek) | 1 | R04 | #55, #63 | template §12 | `window.__errors` empty |
| Fonts preloaded (`document.fonts.load` / `ready`) | 1 | R05 | #55 | [Hypothesis] report §8 | first frame identical across passes |
| Cue-sheet loader (`?cues=` path or injected) | 1 | R06 (warning) | #63 | report §5.5 | `window.__cueSource` is `injected` or `path` in production |
| Fixtures frozen (`Object.freeze`) | 1 | R07 (warning) | #12 | report §9 accuracy invariant | QA text diff vs fixtures |
| Error channel `window.__errors` | 1 | R08 | — | template §6 | read after every seek |
| `window.SCENE_META` with contract version | 2 | R09 | — | contract versioning | manifest records it |
| HyperFrames adapter `window.__hf` (duration + seek) | `--hf` | R10 | — | [N68] (contested) | HyperFrames render succeeds |
| No wall clock (`Date.now`, `Date()`, `performance.now`) | all | F01–F03 | #15 | [N68][N18] | double render |
| No unseeded randomness (`Math.random`, `crypto` random) | all | F04, F05 | #17 | [N61] (contested) | double render, reversed seek order |
| No `setInterval`; no self-rescheduling `setTimeout` loops | all | F06, F11 | #15, #19 | [N69] | render does not hang |
| No `requestAnimationFrame` | all | F07 | #19 | [N69] "rAF doesn't fire in beginFrame mode" | render does not hang |
| Never `play()`, no `autoplay` | all | F08, F09 | #15 | [N68] "The renderer never calls play()" | — |
| Finite repeats (GSAP-style `repeat:-1`, WAAPI `Infinity`, CSS `infinite`) | all | F10 | #18 | [V4-MP] | seeking any t gives one state |
| No remote resources | all | F12 | — | contract §5 (offline) | renderer role has no internet |
| ≥2 `<video>` → `SCENE_META.workersMax = 1` | all | F13 / W05 | #20 | [N70] | no black frames |
| CSS animations/transitions not seek-driven | all | W03 (warning) | #15 | [Hypothesis] | drive via Web Animations API `currentTime`, or avoid |
| Canvas 1080×1920 | — | (template constants) | #49 | report §7.9 | anim-qa checks frame size |

## 2. Why each rule exists (short)

- **Seek, never play.** Every verified harness sets t and captures a frame: opus-js-animations renders "frame i as seek(i / fps) across parallel workers" [N18]; HyperFrames "never calls play()" [N68]; the HuggingFace contract requires `window.DURATION` and `async window.seek(t)` [N72].
- **Pure function of t.** "The same time value must always produce the same visual state" [N61] (contested in the evidence set, treated as strong guidance). Parallel workers render frames out of order, so any state carried between frames breaks.
- **rAF hangs.** In BeginFrame mode "rAF doesn't fire" [N69]; a scene that waits on rAF never resolves `seek`.
- **One worker for video.** Chrome cannot seek several video elements at once without exhausting decoders [N70].

## 3. Double-render protocol

1. Clean output directories `frames_a/` and `frames_b/`.
2. Pass A: normal render (production worker count).
3. Pass B: separate harness process, same machine, same pinned browser, same seed (contract.md §11, mandatory from Level 1). Optionally vary something irrelevant — worker count, or reverse seek order for a sample of frames using single-seek stills (`?t=SECONDS` in `scene_template.html`).
4. Hash PNG frames, not the MP4 (encoders may embed differing metadata): `determinism_hash_check.py frames_a frames_b --json --write-manifest frames_a.sha256.json`.
5. Identical → store the manifest; later renders of the unchanged scene on the same box compare against it.
6. Different → the first differing frame index and time localise the fault:
   - frame 0 differs → fonts or images not ready before first seek;
   - scattered frames differ → PRNG called inside `render(t)` or wall-clock reads;
   - frames after a video element appears differ → decoder contention (#20);
   - all frames differ only across machines → WebGL/driver variance (#65).

## 4. Conformance verdicts

| Verdict | Condition |
|---|---|
| `pass` | lint exit 0 at level 2 `--strict` (plus `--hf` for HyperFrames), hashes identical, `window.__errors` empty |
| `pass_with_allowances` | as above, but with `lint-allow` comments, each justified in scene notes and accepted by a reviewer |
| `fail_lint` | any lint error |
| `fail_nondeterministic` | hashes differ on one box |
| `fail_box` | preflight FAIL or cross-box difference under investigation |

## 5. Exit codes (shared by the harness scripts, contract.md §12)

`0` success · `1` violations / differences / preflight FAIL / selftest failure · `2` usage or IO error · `4` render failure in the harness (`E_SEEK_TIMEOUT`, an `error` in `window.__errors`). `reference_analysis.sh` additionally uses `3` for missing FFmpeg. See contract.md §12 for the full table.
