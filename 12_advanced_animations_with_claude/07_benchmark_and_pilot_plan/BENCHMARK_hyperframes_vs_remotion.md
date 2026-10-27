# Benchmark protocol: HyperFrames vs Remotion on ExamLeaf vertical lessons

**Status: protocol only. Nothing in this file has been run.** HyperFrames and Remotion are not installed on the build machine and no network was used. Every threshold below is a pre-registered proposal to be frozen at kickoff; every engine-specific command or API is marked **verify**.

Companions: `PILOT_three_test_lessons.md` (the lessons), `record_sheets.md` (blank tables), `../04_harness_contract/` (the contract, lint, hash check, preflight). Citations `[N#]`, `[V#]` are in `../01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`; "engine §10" means `../../04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` section 10. Labels: **[Recommendation]**, **[Hypothesis]**, **verify**. Paths that begin with a number and underscore (for example `10_pilots_and_examples/…`) are relative to the project ROOT, `ExamLeaf_Video_EdTech_Pipeline/`.

---

## 0. Why this benchmark, and what it inherits

**Decision stance (inherited, engine §10).** "Begin the production comparison with HyperFrames. Switch to Remotion when measured developer productivity, reliability, or repair time makes it the better total-cost choice. Do not decide from licence price alone." And: "Do not maintain both by default." Neither engine has been installed or run by the project so far.

**Metric order (inherited, engine §10).** Correctness → reproducibility → memory consumption → render time → ease of repair → total operating cost.

**Protocol rules inherited from `10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md` section 6 and `docs/Four_Pilots.md`.** Identical approved scenes, same fonts, content, audio and frame count, same hardware and concurrency; a warm-up then at least five measured repeats per configuration; cold (first build) and cached builds recorded separately; measure peak RSS, CPU/GPU, wall time, file size, repairs and visual differences; "do not extrapolate the simple native SVG timings as browser-engine benchmarks". Those timings are 27.3–29.4 s per 30 s, 720-frame, 24 fps, 720p job under two-worker concurrency on ChatGPT's Linux sandbox (`PREVIEW_BENCHMARKS.md` section 1). They are not a baseline for this benchmark.

**What this benchmark adds.**
1. **Vertical 1080 × 1920 at 30 fps** as the primary format (the older protocol measured 16:9 and 9:16 at 720p, 24 fps).
2. **Agent cost**: Claude Code tokens per scene and fix-loop count (new in the advanced-animation layer, report sections 3.3 and 3.4).
3. **Contract conformance** (seek-purity, seeded randomness, fonts, cue sheet): `../04_harness_contract/contract.md`.
4. **Video-in-video behaviour** [N70], **Indic text shaping** (report section 4.4, edge case 55), and a **9:16 configuration** check.
5. **Licence and cost** as a recorded input, with Remotion's terms marked **verify**.

**What it cannot show.** Three scenes of 30 s each, one machine, one model. Results are indicative of engine behaviour on this workload. They say nothing about learning outcomes or about ten-minute lessons.

---

## 1. The two arms

| | Arm H: HyperFrames | Arm R: Remotion |
|---|---|---|
| Role | Default master timeline [Recommendation, report section 2.6] | Challenger |
| Requirements | Node.js 22+ and FFmpeg [N8] | Node (version not in evidence): **verify** |
| Scaffold | `npx hyperframes init my-video` [N9] | project created per current docs: **verify** |
| Agent skills | `npx skills add heygen-com/hyperframes` [N58]; plugin `claude plugin install hyperframes@hyperframes` [N10]; 21 skills [N11] | `npx skills add remotion-dev/skills` [N1] (or `npx remotion skills add` [N64]); umbrella `/remotion-best-practices` [N4]; run `/remotion-upgrade` first [N7] |
| Licence | Apache-2.0, no per-render fees [N14] | **verify** (not in evidence set); see section 5, M12 |
| Contract surface | `window.DURATION`, `async window.seek(t)` [N72]; `window.__hf` [N68] (contested: verify) | frame-pure React composition (`contract.md` section 17: verify API) |

**Pinning.** Record the exact version of each engine, its CLI, its skill pack (commit or package digest, not a file blob SHA: engine §11), Node, FFmpeg, Chrome and the OS. Do not invent or assume versions.

**Admission first.** Before installing either engine or skill pack, run the third-party admission process of engine §11 (confirm publisher, inspect repository and scripts, review licences and permissions, pin a real commit or digest, test in isolation, copy only approved components, re-audit upgrades). Do not run `curl | bash` installers. Install each arm in its own isolated directory so neither can read the other's scenes (edge case 9, [V3]). HyperFrames clone, if used: `GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` [N13] (edge case 23).

**Same browser for both arms [Recommendation].** The browser is a confounder. Pin one Chrome binary with `CHROME=/path` [N17] and run both arms with it if the engines allow; if Remotion insists on its own browser, record both builds and note it as a limitation (**verify**).

---

## 2. Step 0: preconditions (all must be true before measuring)

| # | Precondition | How checked |
|---|---|---|
| 0.1 | Render box passes `../04_harness_contract/preflight.sh` (Node 22+, FFmpeg/ffprobe, Python 3.11+, Chrome or `CHROME`, Devanagari and Bengali-Assamese fonts, disk) | exit 0 |
| 0.2 | Both engines admitted (engine §11) and pinned; versions in Sheet A | review record |
| 0.3 | Remotion licence terms read for ExamLeaf's use and recorded with date (M12) | text copied into Sheet H |
| 0.4 | HyperFrames `window.__hf` shape confirmed or marked unusable (contested [N68]); `contract.md` section 3 updated | note in Sheet A |
| 0.5 | Fixtures, state exports, cue sheets, audio and fonts frozen and hashed (section 3.2) | hashes in Sheet A |
| 0.6 | Machine is quiet: plugged in, no other heavy apps, fixed power mode, same display settings for human review | checklist in Sheet A |
| 0.7 | Reviewers assigned: academic reviewer (physics, chemistry, biology) and a native Hindi and Assamese reader for the shaping card | names in Sheet A |

**Note on the author's machine (14 Oct 2026).** `preflight.sh` run on the Mac used to build this folder reported FAIL for three checks: the default `node` is v20.19.4 (an nvm install of v24.6.0 exists and passes when selected), and `ffmpeg` and `ffprobe` are not installed. Fix these before step 0.1. Fonts for Devanagari and Bengali-Assamese (including U+09F0) were present as system fonts.

---

## 3. The test lessons and frozen inputs

### 3.1 Three lessons, one per subject

Taken from the existing fixtures in `../../04_video_engine/implementation_v2/examples/`. Each fixture is a 30 s, 24 fps `technical_preview` with five cues and `answer_visible` flags. Class contexts and assumptions are quoted from the fixtures.

| ID | Subject | Fixture | Title (fixture) | What it exercises in the engine |
|---|---|---|---|---|
| L-PHY | Physics | `physics_rc.json` (RC charging; R = 10000 Ω, C = 0.0001 F, V_s = 10 V) | "Charging takes time" | A graph driven by a model, equation text with subscripts, numeric counters that must match the curve, a prediction gate (answer hidden until 16.5 s) |
| L-CHE | Chemistry | `chemistry_balance.json` (coefficients [2, 1, 2]) | "Same atoms. New counts." | Chemical formulae with subscripts, an atom ledger, discrete state changes, a question gate |
| L-BIO | Biology | `biology_genetics.json` (Aa × Aa) | "A ratio is not a promise." | A grid/table layout, fractions, genotype vs phenotype labels, a "not guaranteed" caveat |

Why these three: they are the engine's own golden fixtures, already carry science checks (`PREVIEW_BENCHMARKS.md` section 2), and the report prescribes "the same three test lessons (one physics, one chemistry, one biology)" (report section 2.6). Mathematics (chain rule) is excluded here because the report puts equations and graphs in Manim CE; add it later as a fourth lesson.

### 3.2 What is frozen and hashed (identical in both arms)

| Input | Rule | Recorded |
|---|---|---|
| Fixture JSON | untouched copy of the file above | sha256 |
| **State export** | the engine's validated state for the lesson (see 3.3), the only source of science glyphs; scenes read it read-only (`data-fx`) | sha256 + reviewer initials |
| Cue sheet | one per lesson, validated by `validate_cue_sheet.py`; same file in both arms | sha256 |
| Audio | one 48 kHz audio file per lesson, same in both arms (see 3.4) | sha256 |
| Fonts | pinned local font files: one Latin family, one Devanagari, one Bengali-Assamese; loaded by `@font-face` from local files; no system fallback allowed in the render | file sha256s; `fc-match`-style listing is not a substitute |
| Frame parameters | 1080 × 1920, **30 fps**, 30 s, **900 frames** | in manifest |
| Encoder settings | one command line for both arms, final encode only after hashing frames | recorded text |
| Brief and constraints | one brief per lesson, identical except an engine-specific constraints block (section 6.2) | sha256 |
| Hardware and concurrency | section 4 | Sheet A |

### 3.3 State export (required, not yet implemented)

Scenes may show only values that come from the engine's validated model. The engine does not currently export that state as a file for the browser. **The engine owner or benchmark team must produce `<id>.state.json` from the validated model, and the academic reviewer must sign it before any scene is written.** If the engine cannot export it, hand-write it, then have `examleaf-science-reviewer` and a human reviewer check every field. Required content, taken from the science checks recorded in `PREVIEW_BENCHMARKS.md` section 2 and the fixture text:

- **L-PHY:** parameters with units; `V_C(0) = 0`; at one time constant `V_C / V_s = 1 − e⁻¹ ≈ 63.2 %`; the curve as sampled points in `t/(RC)` (the fixture says model time is shown as `t/(RC)`, not footage time); Kirchhoff voltage law `V_s = IR + V_C`; label and unit strings; assumptions (ideal linear R and C, constant 10 V source, capacitor initially uncharged).
- **L-CHE:** formulae and coefficients (`2 H₂ + O₂ → 2 H₂O`, from coefficients [2, 1, 2] and the approved formulas), atom ledger per side for the final state (reactants H 4, O 2; products H 4, O 2) **and for every intermediate state the scene shows** (for example the state after "two water molecules" and before the hydrogen coefficient); label strings; assumption (formulas supplied and correct; schematic states, not a mechanism).
- **L-BIO:** parents Aa and Aa; gametes A and a, equal probability; genotype probabilities AA 1/4, Aa 1/2, aa 1/4; dominant-phenotype probability 3/4 under complete dominance; label strings; assumption text including "probabilities are not guaranteed counts in four offspring". Any example outcome of four offspring that a scene might draw must be an explicit, reviewed entry marked "illustrative outcome"; otherwise the scene shows none.

### 3.4 Audio and cue sheets when no narration exists

No approved narration exists for these fixtures (`delivery_status.json`: voice import and alignment not validated). So:

- **Audio [Recommendation]:** generate one deterministic placeholder bed per lesson at 48 kHz (seeded Python, tone or silence), hash it, and label it NOT SPEECH. The benchmark measures the audio-mux path, not voice quality. If approved narration is available by then, use it instead (same file in both arms).
- **Cue sheet:** `alignment_source: "synthetic_even_spacing"`, `narration_audio_sha256` set to the placeholder's hash (or null if none), by this deterministic rule so both arms get identical sheets: for each fixture cue `[start, end]` with `k` words (split on whitespace and em dashes, strip trailing punctuation), the speaking window is `[start + 0.20, end − 0.40]`, word `i` gets `t0 = window_start + i × slot` and `t1 = t0 + 0.9 × slot` with `slot = window_length / k`, rounded to 3 decimals. This rule was run on the three fixtures and all three sheets validated (`validate_cue_sheet.py`, 0 errors, 900 frames each; the only warning is the null audio hash). Such sheets fail `--production` by design: these are technical proofs, not releasable lessons.
- Reveal cues are added per scene brief at `word.t0 − 0.05` (contract section 8).

### 3.5 Required feature coverage (both arms implement all of it)

Each scene, in each arm, MUST include the same features, so the engines are exercised equally:

| Feature | Detail |
|---|---|
| Kinetic headline | the fixture `title`, animated per word from the cue sheet, reveal on or 0.05 s before the word (contract section 8) |
| Data-bound visual | the lesson's diagram, graph or grid built from the state export; every science glyph tagged `data-fx` (HTML arm) or an equivalent traceable prop (Remotion arm) |
| Prediction gate | the answer visual is absent until the feedback cue (the fixtures' `answer_visible` flags); a frame at 16.4 s must not show it |
| Imported clip | one PNG-sequence clip of the data-bound visual rendered by another tool (Manim CE or the SVG renderer), imported per `../04_harness_contract/import_clip_notes.md` |
| Text | Latin headline plus caption; plus one **Hindi** and one **Assamese** caption line for the shaping test (translations are for shaping tests only, unreviewed, never published) |
| Decoration | a seeded decorative layer (the template's confetti and boil) to test seeded randomness; must not encode data |
| Transition | one 0.5–0.7 s paper-style slide at the question-to-feedback boundary [V4-MP] |
| Audio | placeholder bed muxed at 48 kHz, same loudness step in both arms |
| Safe zones | layout from `vertical_safe_zones.tokens.json` (placeholder insets) |

---

## 4. Environment and concurrency

- **One machine**, plugged in, quiet, same fixed power mode. Record in Sheet A: model, CPU, core count, RAM, GPU, OS build, Chrome, Node, FFmpeg, engine versions, free disk, date.
- **Concurrency settings, frozen at kickoff and identical across arms:** C1 = 1 worker; C2 = W workers, where W is chosen once (a suggestion: min(4, physical cores ÷ 2), **[Recommendation]**) and recorded. Video-in-video tests run only at C1 [N70].
- **Cold vs cached.** *Cold* = the first render after (a) a fresh install into an empty directory and (b) deleting every cache directory the engine documents (names: **verify**; record what you deleted). *Cached* = the same command repeated with caches intact. A machine reboot is not required; a full-disk-cache purge is not required.
- **Run schedule per configuration** (lesson × arm × concurrency, 9:16): run 0 = cold (recorded as cold); run 1 = warm-up (discarded); runs 2–6 = five measured cached repeats.
- **Order.** Alternate arms (H R R H H R …) and rotate lesson order between arms so thermal drift and learning effects cancel [Recommendation]. Authoring order is counterbalanced the same way (section 6.2).
- **Optional 16:9 smoke test:** one cold and one cached render per lesson per arm at 1920 × 1080 to stay comparable with the older protocol. Not scored.

**Render count.** 3 lessons × 2 arms × 2 concurrency settings = 12 configurations; 7 renders each (cold, warm-up, 5 repeats) = 84 renders, plus 12 video-in-video renders (section 6.5), plus the optional 16:9 smoke set.

---

## 5. Metrics

"Gate" means a hard pass/fail (section 7). Sheet letters refer to `record_sheets.md`.

| ID | Metric | How measured | Unit | Gate | Sheet |
|---|---|---|---|---|---|
| M1 | **Correctness** | (a) text diff of every `data-fx` DOM element, or Remotion equivalent, against the state export; (b) human check of frames at fixed timestamps (below) against the state export; (c) prediction gate: answer absent at 16.4 s | mismatches; defects by severity | **G1** | D, E |
| M2 | **Determinism** | `determinism_hash_check.py`: every measured repeat compared with measured repeat 1; also cold vs repeat 1 (cache transparency); also C1 vs C2 frames (worker invariance, **[Hypothesis]**: should be identical) | frames identical Y/N; first differing frame | **G2** | B |
| M3 | Render time, cold | wall clock of run 0 | s | no | B |
| M4 | Render time, cached | wall clock of runs 2–6; report median and range | s | no | B |
| M5 | Peak memory | peak summed RSS of the whole render process tree, sampled at 1 Hz or better (a browser spawns many processes, so single-process tools under-report; the tool is your choice, record which, **verify**) | MB | no | B |
| M6 | CPU / GPU use | mean and peak CPU of the tree; GPU use if WebGL is present (tool: **verify**) | % | no | B |
| M7 | Output size | frames directory and final MP4 | MB | no | B |
| M8 | **Agent tokens per scene** | from the Claude Code session usage report for the authoring session(s) of that scene (command: **verify**): input, output, cache read, cache write; model ID; effort; wall time | tokens | no | C |
| M9 | **Fix-loop count** | number of render → inspect → agent-edit cycles after first generation; cap 3 | count | no (cap) | C |
| M10 | **Reviewer edit time** | stopwatch minutes a human spends editing or correcting the scene, separate from review time | minutes | no | C |
| M11 | Defects and repairs | academic and visual defects with severity (Critical / Major / Minor per engine `docs/Production_Runbook.md`: Critical = wrong science, misleading visual, missing critical text, unlicensed asset, unauthorised spend) | count per severity | via G1 | E |
| M12 | **Licence and cost** | HyperFrames Apache-2.0, no per-render fees [N14]. Remotion: record the **current** licence text and pricing page with date (**verify**). A claim in engine §10 step 8 (not evidence-set verified): "$0.01 per billable render with a $100 monthly minimum when the paid licence applies", with the cost models assuming 20 billable renders per video: confirm the billing definition with the vendor. Compute cost at 1, 100 and 1,000 videos per month. | USD, text | **G8** | H |
| M13 | **Video-in-video behaviour** | section 6.5 | frame errors | **G5** | G |
| M14 | **Indic text shaping** | section 6.6 | defects | **G4** | F |
| M15 | **9:16 configuration** | `ffprobe` of the final MP4 and of frame dimensions: 1080 × 1920, 900 frames, no scaling or crop step in the pipeline; record the exact config lines each engine needs (**verify**) | pass/fail + text | **G3** | A |
| M16 | **Contract conformance** | Arm H: `lint_seek_contract.js --level 1` (and `--hf` if used) exit 0, plus the contract's runtime checks; Arm R: the same semantic checks by hand (pure of frame, seeded randomness, fonts, cue sheet) | pass/fail | **G7** | D |
| M17 | Reliability | failures, hangs and manual interventions across all renders, each with a cause | count | **G6** | B |
| M18 | Setup effort (optional) | steps and minutes from an empty directory to the first successful render, and every setup error met | steps, min | no | A |
| M19 | Review surface (optional) | reviewer's 1–5 rating of the engine's preview/Studio for reviewing a scene [V2][V3] | 1–5 | no | C |

**Fixed human-check timestamps for M1(b)** (frames at `t` seconds; the same list for both arms): 0.5, 3.0, 5.9, 6.1, 10.9, 11.1, 16.4, 16.6, 23.9, 24.1, 29.9. These straddle every cue boundary in the fixtures (6, 11, 16.5, 24 s) so reveal timing and the prediction gate are tested.

---

## 6. Procedures

### 6.1 Prepare (once per lesson)

State export written and signed (3.3); fixture, state, cue sheet, audio, fonts hashed (3.2); PNG-sequence clip rendered by its producer, twice, hashes equal (`import_clip_notes.md` section 7); clip manifests written.

### 6.2 Author the scene (agent protocol, per arm, per lesson)

Goal: measure how much agent effort each engine needs for the same brief.

- **Model and effort.** Pin the full model ID (aliases drift, [N28]) and set effort **explicitly to `high`** (Opus 5.5 and Sonnet 5.5 default to medium [N22]); `xhigh` only with a written reason in Sheet C [report section 3.4]. **Never ultracode** [V1][N24].
- **Fresh workspace** per arm per lesson, containing only: the brief, the state export, the cue sheet, the font files, the clip and its manifest, the safe-zone tokens, `contract.md`, and that arm's skill pack. No sibling folders, no earlier scenes ("do not inspect any of my older projects or folders", [V3]; edge case 9).
- **Same brief** for both arms. The only difference is an engine-specific constraints block (how to expose the composition, how to import the clip). The brief states the required features (3.5), the contract level to reach (L1), and the iteration cap.
- **Order counterbalanced:** L-PHY H first, L-CHE R first, L-BIO H first (swap on a replicate).
- **Scene text.** The agent never writes or edits science text; it reads the state export (report section 9, step 2).
- **Iteration cap: 3 fix loops.** One fix loop = render, inspect (lint, hash check, human look), then one agent edit session. After the third failed loop the scene is recorded "failed for this arm" and the failure cause is logged.
- **Token capture.** Record usage per session (M8). No subagents unless both arms use the same count; no unattended "don't stop until perfect" instructions [V2][V1].
- **No generated assets.** All visuals are code or clips from the producers; Higgsfield credits are zero by design (credits have no native cap, [N33][N34]).
- **Replicate (optional, budget permitting):** author L-CHE a second time in each arm to estimate agent variance. One run per cell is a small sample; do not over-read a difference between two single runs.

### 6.3 Render and measure

1. Render with the arm's documented command (**verify**: neither command is in the evidence set), wrapped by a timer and the memory sampler (M5). Use the contract harness rules where the engine allows: `CHROME` pinned [N17]; polling not rAF [N69]; one worker for video-heavy scenes [N70].
2. Write PNG frames first; hash them; then encode and mux. Record wall time of the render step (frames) and of the encode step separately.
3. Follow the run schedule in section 4. Log every run in Sheet B even if it fails.

### 6.4 Determinism (M2)

For each configuration: `python3 ../04_harness_contract/determinism_hash_check.py REPEAT_K_DIR REPEAT_2_DIR` for K = 3…6; cold vs repeat 2; for each arm and lesson, C1 vs C2. Hash frames, not MP4s. Any non-identical pair is a G2 failure for that arm until explained; if the cause is a scene defect (for example unseeded randomness the lint missed), that counts as a fix loop and the determinism runs are repeated.

### 6.5 Video-in-video (M13)

- Variants per arm (lesson L-BIO's scene, C1 only): **V2** = two MP4 clips visible at once; **V4** = four. The clips are the PNG-sequence clip re-encoded as intra-only constant-fps MP4 (FFmpeg flags: **verify**), each with a burned-in large frame counter (a deterministic generator script is part of the setup).
- Reference: the same scene with PNG sequences. Compare the MP4 variant's frames with the reference at every frame: no black frames, no duplicated or skipped frame numbers, no desynchronised clips. Pixel-level difference thresholds are set from a calibration (compare two renders of the *same* variant to find the noise floor), not invented. ffmpeg's `psnr`/`ssim` filters are one option (**verify**).
- Record decoder errors, hangs and the single-worker penalty [N70]. Try the documented mitigation first (HyperFrames: single worker [N70]; Remotion: its equivalent, **verify**).
- Three measured repeats per variant (not five).

### 6.6 Indic shaping card (M14)

A fixed test scene rendered in both arms with the pinned Devanagari and Bengali-Assamese fonts (3.2), each string on its own line at the token heading size and at the minimum label size (`vertical_safe_zones.tokens.json`), static and with per-word reveal:

| Group | Strings (copy exactly; native reader confirms they are correct text before use) |
|---|---|
| Devanagari conjuncts and reph | क्षेत्र, ज्ञान, प्रकाश, धर्म, विद्युत् धारा, द्वितीय |
| Devanagari marks | अपवर्तन (refraction), ट्रांसफ़ॉर्मर (anusvara, nukta, candra-O), माँ (chandrabindu) |
| Bengali-Assamese conjuncts | বিজ্ঞান, ক্ষেত্ৰ, প্ৰকাশ |
| Assamese letters (U+09F0, U+09F1) | ৰসায়ন, ৱাট |
| Mixed script and numerals | `प्रकाश का refraction`, `R = 10000 Ω`, `H₂O`, `বিজ্ঞান 10` |

Pass test: **no tofu boxes, no broken or detached conjuncts, marks (matras, nukta, reph, virama) in the right place, no clipped ascenders or descenders, and per-word animation never splits a word.** A native Hindi reader and a native Assamese reader sign Sheet F. Compare each arm's render against a reference screenshot of the same strings in plain Chrome with the same font files. Letter-by-letter animation is a separate optional row (grapheme-cluster segmentation: **verify**; never per code point). Hypothesis being tested: shaping is the browser's, so both arms should be identical; any difference points at font loading or a text-layout wrapper.

### 6.7 9:16 check (M15)

`ffprobe` the final MP4 (width, height, frame rate, frame count) and a sample frame file. Confirm no crop or scale filter was applied after rendering. Record the lines in each engine's config that set the size (HyperFrames: **verify**, [Hypothesis] an HTML viewport you set; Remotion: **verify**, [Hypothesis] composition width and height).

### 6.8 Licence capture (M12)

Copy the current Remotion licence terms and the pricing or automation page with the date and URL into Sheet H. Note whether ExamLeaf's size and use (a revenue-bearing education business rendering at volume, possibly automated) falls in the free or the paid tier. Do not infer from the figures in engine §10, which are unverified. Compute annual cost at 1, 100 and 1,000 videos per month. Licence price alone never decides (engine §10).

---

## 7. Pass/fail criteria (pre-registered; freeze at kickoff)

An arm **passes** only if it meets every gate. Gates G1–G8 are hard; margins in section 8 are used only to choose between arms that both pass.

| Gate | Criterion | Evidence |
|---|---|---|
| **G1 Correctness** | zero Critical defects; zero `data-fx` text mismatches against the state export; the prediction-gate frame at 16.4 s shows no answer, in all three lessons. "A single critical scientific error should block release regardless of the overall visual score" (`INSTRUCTIONS_running_the_four_pilots.md` section 8). | Sheets D, E |
| **G2 Determinism** | 100 % of frames identical for every pair compared in 6.4, all lessons, both concurrency settings. A single differing frame fails. | Sheet B |
| **G3 Vertical** | final MP4 is 1080 × 1920, 900 frames, 30 fps, produced without a crop or scale step | Sheet A, ffprobe |
| **G4 Indic shaping** | zero defects on the card at both sizes for both scripts, signed by native readers | Sheet F |
| **G5 Video-in-video** | with the documented single-worker mitigation, V2 and V4 show no black, duplicated or skipped frames across all repeats. If the arm fails only here, it may pass **conditionally** under a written PNG-sequence-only policy (no MP4 imports); record that policy. | Sheet G |
| **G6 Reliability** | zero unexplained failures or hangs across all scored renders; every failure has a cause found within one investigation | Sheet B |
| **G7 Contract** | Arm H: lint exit 0 at Level 1 and runtime checks pass; Arm R: equivalent semantic checks pass | Sheet D |
| **G8 Licence** | commercial use for ExamLeaf is permitted under the current terms, recorded with date. An unresolved Remotion licence blocks selecting Remotion; it does not block the measurement. | Sheet H |

Scene-level failure (3 fix loops exhausted without meeting G1, G2 or G7) counts against the arm under G6 and is reported in the decision memo with its cause.

---

## 8. Decision rule

**Choose one engine.** Apply in order:

1. **Only one arm passes all gates:** choose it.
2. **Both arms pass:** compare in the inherited metric order: reproducibility (already a gate, so equal), then memory (M5), render time (M3, M4), ease of repair (M8, M9, M10, M11), then total operating cost (render time × machine cost + human minutes + licence cost; engine §10 step 8). **HyperFrames is the default and wins unless Remotion beats it by a clear margin.** Proposed margins **[Hypothesis, freeze at kickoff or replace]:** Remotion must show a median reduction of at least 25 % in the repair composite (agent tokens, fix loops and reviewer minutes, each normalised to the HyperFrames median and averaged) **and** must not exceed 1.25× HyperFrames' median cached render time or peak memory, **and** its licence cost must be known. Otherwise choose HyperFrames. Do not decide on licence price alone.
3. **Neither passes: STOP.** Do not start pilot scene production on either engine. Record the failure matrix (gate × arm × cause). Allow **one timeboxed remediation round per failed gate** (examples: a font-loading fix, a worker-count setting, a missing seed), then re-run only the failed gates. If a gate still fails, escalate to the project owner with the matrix and consider the contract-conformant raw Chrome frame pipeline [N18] (or the engine's existing Python SVG → FFmpeg renderer for 2D) as the interim compositor, because the contract, cue sheets and fixtures are engine-agnostic.
4. **After the decision:** archive the other arm's scenes and notes ("do not maintain both by default", engine `docs/Architecture.md`); update `contract.md` with anything learned (for example the confirmed `__hf` shape) as a new contract version; hand the winning arm's scenes to the pilot (`PILOT_three_test_lessons.md`).

**What counts as a tie.** Differences smaller than the run-to-run spread (the range across the five cached repeats) are ties. Ties go to HyperFrames.

---

## 9. Confounders and how they are controlled

| Confounder | Control |
|---|---|
| Different browser builds | one pinned Chrome for both arms if possible; otherwise recorded as a limitation |
| Thermal drift, background load | quiet machine; alternate arm order; report medians and ranges |
| Cache state | explicit cold and cached definitions; warm-up discarded |
| Agent variance, one run per cell | optional replicate; fix-loop cap; same brief; do not over-read single differences |
| Learning effects (the second engine benefits from the first's brief) | counterbalanced order; fresh workspace; nothing carried over except the shared brief |
| Reviewer bias | reviewers judge frames without being told which arm made them where practical; Studio/preview used only for M19 |
| Font fallback | pinned local fonts; render fails if a family does not load (`E_FONT_LOAD`) |
| Network | none during render; no CDN (contract F12) |
| Placeholder audio and synthetic cue timings | same files in both arms; the benchmark does not assess sync quality or voice |
| Small sample (three 30 s scenes) | indicative only; no claim about ten-minute lessons or learning outcomes |

---

## 10. Budgets and stop rules

- Per scene: **3 fix loops maximum**; no ultracode [V1][N24]; effort `high` unless justified; a per-scene token cap set at kickoff from `examleaf-effort-governor`. [V1] is an upper-bound reference only (about 78K tokens at low to about 625K at max for one 79 s from-scratch piece); scenes built from the contract, tokens and a template are expected to land far below that **[Hypothesis]**. Measure it here.
- Image and video generation credits: zero.
- Stop the benchmark and escalate if any arm produces a Critical science defect that the arm's own tooling cannot detect (that is a finding about review, not only about the engine).

---

## 11. Deliverables

1. Filled `record_sheets.md` (all sheets), one file per arm per lesson plus the roll-up.
2. Frame hash manifests and render manifests for every run (contract section 11).
3. Scene folders and agent session logs (token counts, fix-loop notes) for each arm.
4. The Indic card renders and the native readers' sign-off.
5. A one-page decision memo: gate matrix, chosen engine, margins used, licence note, open issues, what to change in `contract.md`.
6. Raw timing logs so anyone can recompute medians and ranges.

---

## 12. What remains unverified until this benchmark runs

HyperFrames' `window.__hf` shape [N68], its worker and 9:16 settings, bundled tween library, Indic shaping in its Chrome build; Remotion's licence, required Node version, composition sizing, font loading and video-in-video behaviour; whether either engine blocks network access during render; whether a single worker really removes the decoder failures [N70] at four simultaneous clips; and whether the cache changes pixels.
