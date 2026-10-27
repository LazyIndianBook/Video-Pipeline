---
name: examleaf-motion-harness
description: "Use when an ExamLeaf advanced-animation scene (HTML/JS, Canvas, SVG, three.js, Remotion component or raw frame pipeline) must be proven seek-deterministic before it is rendered or composed at 1080x1920. Extends examleaf-web-composition by owning contract conformance only: window.DURATION, async window.seek(t), window.ready with font preload and cue-sheet loading, the contested HyperFrames window.__hf adapter, no play(), no wall clock, no rAF loops, seeded PRNG, finite repeats, single worker for video-heavy scenes. Runs the bundled lint_seek_contract.js and a double-render frame-hash test, plus render-box preflight. Does not compose timelines, choose engines, write scene art or approve output."
---

# examleaf-motion-harness

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. Both bundled scripts pass `--selftest` offline. No real scene has been rendered in this environment (no FFmpeg or headless renderer installed here).
- **Extends:** `examleaf-web-composition`, which still owns engine choice, timeline assembly, captions placement and export. This skill owns the **conformance verdict** per scene: lint report + double-render hash report + render manifest.
- **Canonical contract:** `12_advanced_animations_with_claude/04_harness_contract/contract.md` with `scene_template.html`, `cue_sheet.schema.json`, `vertical_safe_zones.tokens.json` and `preflight.sh`. This skill does not restate or fork the contract; it checks scenes against it.
- **Bundled scripts are copies:** `scripts/lint_seek_contract.js` and `scripts/determinism_hash_check.py` are byte-identical copies of the canonical files in `04_harness_contract/`, bundled so the skill works after being copied into `.claude/skills/`. The `04_harness_contract/` copy wins on any difference; drift is a blocker (see Tests).
- **Why it exists:** Opus 5.5 "outputs text only" [N71]; a renderer seeks each frame by time and never plays [N18][N68][N72]. A scene that reads the wall clock, uses unseeded randomness or rAF polling renders frozen, garbled or not at all (report §2.1, §8 #14–24). Report §10.5 specifies this skill.

## Invocation

**Trigger when:**
- A scene file arrives from an authoring run and has not passed lint and the double-render test.
- A scene, its fixtures, its cue sheet or the render box changed (new Chrome, GPU driver, fonts, Node).
- A render hangs, produces black or frozen frames, or two renders differ.
- A new render box is being commissioned (preflight).

**Do not trigger for:**
- Choosing HyperFrames vs Remotion or assembling the lesson timeline (`examleaf-web-composition`).
- Visual, safe-zone, flash, hold-time or science-text QA of rendered frames (`examleaf-anim-qa`, `examleaf-visual-qa`).
- Writing scene art or primitives (`examleaf-procedural-2d`, `examleaf-kinetic-typography`, `examleaf-threejs-scenes`).
- Manim CE or Blender inserts; they have their own deterministic renderers (`examleaf-manim-scenes`, `examleaf-blender-scenes`) and enter the timeline as clips.

## Inputs

| Input | Type | Rule |
|---|---|---|
| `scene_file` | path (.html/.js) | from the authoring run, inside the job workspace |
| `cue_sheet` | path | validated by `04_harness_contract/validate_cue_sheet.py` (production mode rejects synthetic or example timing) |
| `fixtures[]` | paths | read-only props; frozen in the scene |
| `target` | `hyperframes` / `remotion` / `raw` | from web-composition |
| `level` | 0 / 1 / 2 | contract conformance level; production = 2 |
| `render_box` | `{os, chrome_path, chrome_version, node_version, ffmpeg_version, gpu, fonts_sha256}` | from preflight |
| `fps` | number | from the cue sheet (default 30) |

Example request:

```json
{"scene_id":"phy-10-03-s04","scene_file":"jobs/phy-10-03-s04/scene/scene.html",
 "cue_sheet":"jobs/phy-10-03-s04/inputs/cue_sheet.json","fixtures":["jobs/phy-10-03-s04/inputs/fx-refraction-glass.json"],
 "target":"hyperframes","level":2,"fps":30,"workers":4}
```

## Outputs and contracts

1. **Lint report** (JSON on stdout of `lint_seek_contract.js`): `{tool, contract_version, level, hf, strict, reports[{file, ok, errors, warnings, required{}, violations[{rule, severity, line, col, message, edge_case, source}]}], summary}`.
2. **Hash report** (`determinism_hash_check.py --json`): `{identical, frames_a, frames_b, frames_compared, differing_count, only_in_a, only_in_b, first_difference}` plus a `{frame: sha256}` manifest via `--write-manifest`.
3. **Render manifest** (`templates/render_manifest.json`): scene ID, contract version, level, target, fps, DURATION, frame count = round(DURATION × fps) [N72], workers, render box fingerprint, lint report SHA-256, hash-manifest SHA-256, verdict.
4. **Conformance verdict:** `pass` only when lint has zero errors (zero warnings with `--strict` in production) and the two renders are identical.
5. **`handoff.json`** (library schema).

## Dependencies

- Node.js: the linter needs Node ≥ 18 and no packages; HyperFrames itself needs Node 22+ [N8].
- Python 3 standard library (hash check).
- FFmpeg (HyperFrames requirement [N8]; encoding of image sequences).
- Chrome/Chromium for headless rendering; set `CHROME=/path` when autodetect fails [N17].
- Engine-specific: HyperFrames (Apache-2.0, no per-render fees [N14]); Remotion (licence: verify before commercial use, report §2.2); raw seek pipelines such as opus-js-animations (MIT [N21]). Third-party skills/plugins are admitted only after `examleaf-skills-security` review (report §9 step 11).
- Versions: pin and record in the render manifest; none are pinned in the evidence beyond Node 22+ [N8].

## Execution

1. **Preflight the render box** (once per box and after any upgrade):
   ```sh
   bash 12_advanced_animations_with_claude/04_harness_contract/preflight.sh --dir jobs/phy-10-03-s04/frames
   ```
   It checks Node ≥ 22 [N8], npx, FFmpeg/ffprobe, Python, Chrome or `$CHROME` [N17], Devanagari and Bengali-Assamese font coverage, disk space and the skills symlink [N66][N67]. Any FAIL stops here.
2. **Validate the cue sheet:** `python3 12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py jobs/phy-10-03-s04/inputs/cue_sheet.json --production --json` (exit 0 valid; production mode rejects synthetic or example timing and null hashes).
3. **Lint the scene** at the production level:
   ```sh
   node 12_advanced_animations_with_claude/03_skills/examleaf-motion-harness/scripts/lint_seek_contract.js \
     --level 2 --strict [--hf] jobs/phy-10-03-s04/scene/scene.html
   ```
   Use `--hf` for HyperFrames targets (the `window.__hf` shape is contested [N68]; the adapter in `scene_template.html` maps it to `window.seek`). Exit 0 = conformant; 1 = violations (each with rule ID, line, edge case); 2 = usage error.
4. **Render pass A** with a harness that meets `contract.md` §11: load with fixed `fps`, `cues`, `fixture` and `seed` parameters; `await window.ready`; for each frame `await window.seek(i / fps)` and capture a PNG; poll with `setTimeout` and a deadline (30 s per seek, 60 s ready — [Recommendation] defaults, exit 4 on timeout); workers = min(requested, `SCENE_META.workersMax`), one for video-heavy scenes [N70]; write the render manifest. HyperFrames and Remotion CLI render commands are not in the verified evidence [N58]; record the command actually used in the manifest after the pilot install.
5. **Render pass B** in a separate harness process on the same machine, same pinned browser and same seed (contract §11). Optionally also change one thing that must not matter — worker count (e.g. 4 vs 1) or seek order (a reversed sample via the template's `?t=SECONDS` single-seek mode); order dependence reveals stateful PRNG use inside `render(t)`.
6. **Compare frames** (PNG, never the encoded MP4, whose metadata can differ):
   ```sh
   python3 12_advanced_animations_with_claude/03_skills/examleaf-motion-harness/scripts/determinism_hash_check.py \
     jobs/phy-10-03-s04/frames_a jobs/phy-10-03-s04/frames_b --json \
     --write-manifest jobs/phy-10-03-s04/frames_a.sha256.json
   ```
   Exit 0 = identical; 1 = differences (first differing frame reported); 2 = IO error.
7. **Read `window.__errors`** after every seek (the template's error channel). Any `error` entry fails the scene even if frames match.
8. **Write the render manifest** and hand the frames or clip to `examleaf-web-composition`.

## Decision rules

- **Production = level 2 + `--strict`.** Warnings (setTimeout, CSS animations, missing cue loader) must be fixed or explicitly allowed with `lint-allow: RULEID` on that line plus a reason in the scene notes.
- **Identical or nothing.** Same box, same inputs → byte-identical PNG frames. No tolerance on the same box.
- **Cross-machine (#65):** WebGL output may differ across GPUs and drivers [Hypothesis]. Policy: one fixed render box per lesson; re-baseline hashes when the box changes; keep a software-GL fallback test on record (Chrome's software rendering path; flag names vary by version, verify).
- **Seek purity:** state for time t is computed from t and immutable data built once in `window.ready`. Stateful `mulberry32` streams are used only while building data in a fixed order; `rngAt(seed, i)` (stateless) is used inside `render(t)` (scene_template.html §7).
- **Never play:** no `.play()`, no `autoplay`, no real-time media; videos are positioned by setting their time inside `seek` [N68].
- **Waiting:** never on rAF [N69]; the renderer polls with `setTimeout` plus a deadline from outside the scene.
- **Iteration cap:** at most two repair rounds on a failing scene, then a structured blocker back to the authoring run.

## Edge cases handled

| Master # | Detection | Response |
|---|---|---|
| 14 Expecting an MP4 from the model | Request asks the model to "output the video" | Explain: the model writes code [N71]; this skill renders through the harness |
| 15 Wall-clock animation | Lint F01–F03, F08, F09, W03 | Fail; rewrite as f(t) [N68][N18] |
| 16 Missing seek contract | Lint R01, R02 (R03 async warning) | Fail before render [N72] |
| 17 Unseeded randomness | Lint F04, F05; hash mismatch across passes | Fail; seeded PRNG / `rngAt`; re-run double render [N61] |
| 18 Infinite repeats | Lint F10 (JS and CSS) | Fail; finite repeat counts ([V4-MP]) |
| 19 rAF polling | Lint F07, F11 (self-rescheduling setTimeout), W01 | Fail; deadline-bounded setTimeout polling outside the scene [N69] |
| 20 Multiple video elements | Lint F13 / W05 | Require `SCENE_META.workersMax = 1` [N70] |
| 21 Chrome not found | preflight FAIL | Set `CHROME=/path` [N17] |
| 22 Old Node / no FFmpeg | preflight FAIL | Install via the approved environment; Node 22+ [N8] |
| 23 Heavy clone | Slow or failing HyperFrames checkout | `GIT_LFS_SKIP_SMUDGE=1` when cloning [N13] |
| 24 Archive too big | Codex build of the repo fails | Keep frames and media outside the archive; trim assets under the 100 MB limit [N12] |
| 26 Skills invisible to Claude | preflight skills-symlink check | Check `.claude/skills` → `.agents/skills` symlink after installs; handle Windows and pre-existing folders manually [N66][N67] |
| 65 Headless WebGL variance | Hashes differ between boxes, identical on one box | Fixed render box; re-baseline; software-GL fallback test [Hypothesis] |
| 53 Parser expects a fenced html block [N56] (contested) — added 15 Oct 2026 (audit completeness-9) | Intake finds no scene file under `scenes/<scene_id>/`, or the final message is not the brief's JSON status object (e.g. code pasted in a fenced block instead) | Reject the run at intake with a structured error; never extract code from chat text; re-run once under the iteration cap with the output-format reminder from the brief (`examleaf-anim-brief`) |
| 55 (supporting) Fonts not preloaded | Lint R05; first frames in fallback font differ between passes | Preload via `document.fonts.load`/`ready` before first seek |

## Tests and acceptance

- **Selftests:** `node scripts/lint_seek_contract.js --selftest` (good sample passes strict level 2 with `--hf`; bad sample reports 22 rule IDs; level 0/1 behaviour; line numbers) and `python3 scripts/determinism_hash_check.py --selftest` (identical, differing, missing/extra, natural ordering, empty directories not identical, glob filtering).
- **Drift check** (must print nothing):
  ```sh
  cmp scripts/lint_seek_contract.js ../../04_harness_contract/lint_seek_contract.js
  cmp scripts/determinism_hash_check.py ../../04_harness_contract/determinism_hash_check.py
  ```
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance per scene:** lint exit 0 at level 2 strict; double render identical; `window.__errors` empty; frame count = round(DURATION × fps); manifest written with box fingerprint.

## Errors, fallback, escalation

- **Lint failure:** return violations to the authoring run with rule IDs and line numbers; at most two repair rounds.
- **Hash mismatch:** report the first differing frame; inspect that t for PRNG, font or image-decode timing; re-render once after the fix.
- **Render hang:** suspect rAF or an unresolved `window.ready`; check `window.__errors`; never "fix" by adding sleeps inside `render(t)`.
- **Engine failure** (HyperFrames or Remotion): keep the portable scene; the native SVG proof renderer remains the reference (web-composition fallback). Never silently switch engines.
- **Escalate** cross-machine WebGL differences, licence questions (Remotion) and preflight FAILs to the render-box owner.
- **Cost cap:** CPU/GPU render minutes only; logged by `examleaf-render-batch` / `examleaf-observability-cost`.

## Cost/performance

Lint is milliseconds. The double render doubles render time for each scene's first conformant build; later re-renders of unchanged scenes can compare against the stored hash manifest instead. Video-heavy scenes render slower at one worker [N70]; budget for it rather than parallelising.

## Security

- Scene code is model-written and untrusted: render it in the renderer role with read-only staged inputs, no secrets and no internet after staging. The linter rejects remote resources (rule F12), so scenes render offline.
- No API keys in scenes, manifests or the repo; provider keys live in the environment or user config [N19].
- Third-party harness skills and plugins (HyperFrames plugin [N10], Remotion skills [N1], opus-js-animations [N15]) pass `examleaf-skills-security` before install; HyperFrames' on-demand auto-install must be disabled in production (library install guide §6).
- Nothing is published.

## Handoff

- **To:** `examleaf-web-composition` (frames/clip + render manifest), `examleaf-anim-qa` (frames + hash manifest for its determinism and visual checks), `examleaf-render-batch` (box fingerprint).
- **Files:** lint report, hash report, `frames_a.sha256.json`, render manifest, `templates/handoff.json` with `output_ids` = manifest and hash-manifest SHA-256.

## References

- `references/contract_spec.md`: conformance matrix (requirement → lint rule → level → edge case → test) and the double-render protocol.
- `references/hyperframes_notes.md`: HyperFrames requirements, install paths, seek model and open questions.
- `references/remotion_notes.md`: Remotion skills, symlink caveats, frame model and licence caveat.
- `references/raw_pipeline_notes.md`: raw Canvas/SVG/three.js seek pipelines and image-sequence export.
- `references/contract.md`: handoff and security rules.
- Report §2, §3.4, §8 (#14–24, 26, 55, 65), §9 steps 6–7, §10.5, §11.4.
