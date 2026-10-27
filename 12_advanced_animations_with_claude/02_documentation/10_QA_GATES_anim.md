# 10 · QA gates for animated scenes

**Purpose.** Every automated check and every human gate that an animated scene, lesson or Reel passes before release; the review rubric; what blocks release; and how the new checks plug into `examleaf-visual-qa`, `examleaf-audio-caption-qa`, `examleaf-release-review` and the two mandatory human approvals in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`.

**Status.** [PROPOSED]. The new checks are specifications for `12_advanced_animations_with_claude/03_skills/examleaf-anim-qa/` and the scripts in `12_advanced_animations_with_claude/04_harness_contract/`. Existing checks marked [TESTED] are tested only as described in the ROOT/07 runbook.

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V#], [V4-MP], [N#], ROOT-relative project paths, [Recommendation]/[Hypothesis], master edge cases #1–#65, NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

**Two sentences that override everything below** (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`): "A single critical scientific error should block release regardless of the overall visual score." "Automated checks … cannot determine scientific validity or genuine student learning from visual polish alone."

---

## 0. Summary

- **Seventeen automated checks** (A1–A17) run in three bands: before render (contract, preflight, fixtures, fonts), after render (determinism, frames, text, holds, safe zones, flashes, science), and after mux (loudness, captions, media probe).
- **Human gates:** storyboard approval with a cost estimate (new), the existing academic approval GA, a director's rubric review (new), and the existing **GF** (academic + different production reviewer, full watch, bound to the hash) or **GS** for each Short.
- **Release blocks** on any Critical defect, any failed hard check, missing approvals, or unlicensed assets. No aggregate score can hide a Critical.

---

## 1. Gate map for an animated scene

| Band | ID | Check | Tool / file | Threshold or rule | Edge cases | Owner | Blocks |
|---|---|---|---|---|---|---|---|
| Pre-render | A1 | Harness contract lint | `12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js` | Zero violations | #15–#19, #63 | `examleaf-motion-harness` | Render |
| Pre-render | A2 | Render-box preflight | `12_advanced_animations_with_claude/04_harness_contract/preflight.sh` | All requirements present | #21, #22, NEW-16, NEW-20 | `examleaf-render-batch` | Render |
| Pre-render | A8a | Glyph coverage | `qa/glyph_coverage.json` (doc 08 §5.2) | No missing code points | #55, NEW-3 | `examleaf-kinetic-typography` | Render |
| Pre-render | A12a | Science validators on fixtures | `examleaf.cli validate` for supported templates; subject validators | All checks pass | #12 | `examleaf-science-<subject>` | Render |
| Pre-render | A17a | Budget headroom; effort/model audit | `examleaf-effort-governor` | Within caps; no ultracode, no alias | #1–#6, #60 | `examleaf-effort-governor` | Authoring |
| Post-render | A3 | Double-render determinism | `12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py` | Identical PNG frame hashes before encode, incl. a reverse-order render (2D); tolerance for 3D across boxes | #17, #65, NEW-12 | `examleaf-motion-harness` | Composition |
| Post-render | A4 | Safe-zone overlay | DOM boxes vs `vertical_safe_zones.tokens.json` | No essential element outside the safe area or in the caption reserve | #49, #51, NEW-1 | `examleaf-anim-qa` | Release |
| Post-render | A5 | Hold-time | DOM state per frame + cue sheet | Headline ≥ 1.2 s; equation ≥ narration end + 0.5 s; 2–4 s after transform | #50 | `examleaf-anim-qa` | Release |
| Post-render | A6 | Flash and luminance | Frame luminance series | No full-frame flashes; flash threshold per verified standard | #56 | `examleaf-anim-qa` | Release |
| Post-render | A7 | Fixture-vs-rendered text | DOM text dump; OCR/human for raster | Exact match to fixture fields; no text in generated rasters | #12, #54, NEW-17 | `examleaf-anim-qa` | Release |
| Post-render | A8b | Indic shaping | Test card + native reader | No broken intermediate frames | #55, NEW-18 | `examleaf-kinetic-typography` + human | Release (Indic editions) |
| Post-render | A12b | Science-frame QA | Displayed values vs model at each cue | Agree at every semantic event | #12, #64 | `examleaf-visual-qa` | Release |
| Post-render | A13 | Contrast and phone readability | Existing visual QA | ≥ 4.5:1 text; ≥ 3:1 essential graphics; 360 px rule | NEW-31 | `examleaf-visual-qa` | Release |
| Post-render | A14 | Camera-fx guard | Transform log vs cue kinds | No camera move during measure/label cues | #64 | `examleaf-anim-qa` | Release |
| Post-render | A15 | Non-empty frames | Frame statistics | No unexpected uniform/black frames | NEW-21, NEW-22 | `examleaf-anim-qa` | Composition |
| Post-render | A16 | Asset provenance and licence | `AssetManifest` ledger | Every font, SFX, bed, texture, clip licensed and hashed | NEW-2, NEW-7, NEW-25 | `examleaf-asset-library` | Release |
| Post-mux | A9 | Loudness and peak | Audio QA | −16 LUFS ± 1; TP ≤ −1 dBTP (pass ≤ −0.9); re-measured after mux | #39, NEW-9 | `examleaf-audio-production-engineer` → `examleaf-audio-caption-qa` | Release |
| Post-mux | A10 | Caption and reveal sync | Timeline vs captions vs DOM reveal frames | Captions match narration; reveals on or ≤ 0.05 s before word (± 1 frame) | #63, NEW-14 | `examleaf-audio-caption-qa` + `examleaf-anim-qa` | Release |
| Post-mux | A11 | Media probe | ffprobe-based `media_check()` | Resolution equal to the aspect declared by the Format Spec (default 1080×1920, AD-07; 1920×1080 only when the format declares 16:9 and 16:9 safe-zone tokens exist), 30 fps, frames = round(duration × fps), h264, yuv420p, audio present | #10, #16, NEW-13 | `examleaf-render-batch` | Release |
| Any | A17b | Ledger completeness | `anim/ledger/*.json` | Every run recorded; no missing sub-agent counts | NEW-26 | `examleaf-effort-governor` | Release record |

"Blocks" names the first stage the failure stops. Everything that blocks earlier also blocks release.

---

## 2. Automated checks in detail

### A1 · Harness contract lint (#15–#19, #63)

Run `node 12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js --level 1 <scene files>` (exit 0 clean, 1 violations; rule IDs F01–F13 errors, W01–W05 warnings, contract §4) and `python3 12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py <sheet> --production`. The linter is a regex scanner, not a parser, so the double-render hash (A3) is the real proof. The checks, against `12_advanced_animations_with_claude/04_harness_contract/contract.md`:
1. `window.DURATION` is defined and `async window.seek(t)` exists [N72]; for HyperFrames, its seek interface [N68] (contested) is satisfied by the adapter.
2. No animation driven by `Date.now`, `performance.now`, `setInterval`, timer-scheduled state changes, or `requestAnimationFrame` loops [N68][N69] (#15, #19).
3. No `Math.random`; only the harness's seeded PRNG [N61] (#17).
4. No infinite repeats (`repeat: -1` or equivalent); finite repeats only ([V4-MP] §8) (#18).
5. No `video.play()`; video elements are seeked.
6. No hard-coded cue times: numeric time literals used in reveal logic are flagged; times must come from `cues[]` (#63) [Recommendation].
7. No network fetches at render time (fonts, scripts, media) (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14) (NEW-16).
8. Runtime probe: `seek(t)` called twice at the same `t` in different orders produces identical DOM/canvas state [Recommendation].

### A2 · Preflight (#21, #22)

Node 22+ and FFmpeg for HyperFrames [N8]; Chrome found or `CHROME=/path` set where the opus-js-animations pattern is used [N17]; vendored fonts present and hashed; Manim CE and LaTeX if a Manim insert is routed (NEW-20); free disk and memory for the planned worker count (NEW-6). Fail closed.

### A3 · Double-render determinism (#17, #65, NEW-12)

1. Render the scene twice, in two separate harness processes, into two empty directories, same box, browser and seed (contract §11); add a reverse-order render (AD-21 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`).
2. Compare the **PNG frames before encoding**: `python3 12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py DIR_A DIR_B` (exit 0 identical; exit 1 names the first differing frame). Never compare MP4 bytes; container metadata can differ (NEW-12). *(15 Oct 2026) Superseded for v2 by CE-38: with the pinned bitexact encode, Q-DET also compares MP4 bytes; A3 frame comparison stays the diagnostic.*
3. 2D scenes: every frame hash identical.
4. 3D scenes: identical on the same render box; across boxes, per-pixel difference within a tolerance set in the pilot (#65) [Hypothesis].
5. Any mismatch → locate the first differing frame and its active cues; likely causes are unseeded randomness, time-dependent state, or font fallback.

### A4 · Safe-zone overlay (#49, #51, NEW-1, NEW-27)

1. At frame 0, the last frame and every cue boundary (the same sampling as the engine's `layout_check()`, `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.2), collect bounding boxes of all text and essential elements from the DOM.
2. Compare with `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (platform UI insets, caption reserve).
3. Fail if an essential element intersects a platform-UI zone or the caption reserve; warn for decorative elements.
4. Render an overlay PNG per sampled frame for the human reviewer.
5. The tokens file marks its insets `measured: false` (PLACEHOLDERS until measured; `measured_on` and `device_list` added on measurement). Unmeasured or stale insets are a warning, not a pass (NEW-27).

### A5 · Hold-time (#50)

For each text element, compute its *fully readable interval* (opacity 1, final position, not occluded) from per-frame DOM state, using the values in `vertical_safe_zones.tokens.json` `hold_times_s` and the cue sheet's `hold` cues (`until`):

| Element | Minimum |
|---|---|
| Primary headline / hook title | ≥ 1.2 s [N60]; Hindi/Assamese longer (doc 08 §6) |
| Equation | until `t1` of the last word reading it + 0.5 s (report §7.5) |
| After an important transformation / completed diagram | 2–4 s (RD-02) |
| Prediction prompt | whole think pause (RD-11) |
| Question / target quantity in a calculation | throughout the calculation step |

Fail for science text; warn for decorative expressive text.

### A6 · Flash and luminance (#56)

[V1] warns its videos contain "bright, fast flashes". The report recommends banning full-frame flashes for students and limiting rapid luminance changes (§7.11) [Recommendation].
1. Compute mean relative luminance per frame and per screen region.
2. Flag any frame-to-frame change above a threshold in a large area, and count flash pairs per second.
3. The tokens file sets `flash_policy`: full-frame flash banned, `max_flashes_per_second: 3`, flagged "verify against the current WCAG text". The WCAG 2.3.1 general-flash and red-flash thresholds are **not in the evidence set**; confirm them before treating the check as a standard.
4. The [V4-MP] "white flash or bloom for explosions" transition is not used in ExamLeaf.

### A7 · Fixture-vs-rendered text (#12, #54, NEW-17)

1. Every science glyph carries `data-fx="path.to.field"` (contract §9); `examleaf-anim-qa` dumps the DOM text of each such element at every cue boundary.
2. Compare each string with the fixture field: exact match after Unicode normalisation; units and symbols included.
3. For text inside raster or clip layers (Manim, three.js textures, Blender), use the clip's symbol manifest plus OCR or a human check. OCR engines are not verified here; a human check is the fallback (NEW-17).
4. **Generated rasters must contain no text** ([V4-MP] §12: text "built in code, not generated as images"; #54). Run OCR on every generated asset; any detected text fails.
5. The accuracy invariant (report §9): any glyph that encodes science must trace to a fixture field. Text with no field ID in a data-bound scene fails.

### A8 · Indic glyphs and shaping (#55, NEW-3, NEW-18)

A8a before render: coverage of every code point in the assigned font (doc 08 §5.2). A8b after render: the per-script test card and a native reader's review of intermediate frames (doc 08 §7.6); lint rule: no per-code-point splitting of Indic strings.

### A9 · Loudness and peak (#39, NEW-9)

On the **final muxed** file: integrated loudness −16 LUFS ± 1; true peak ≤ −1 dBTP (pass ≤ −0.9) (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1); clipping, DC offset, unexpected silence with protected intervals supplied; music absent from `core_explanation` segments (doc 06 §7.6).

### A10 · Caption and reveal sync (#63, NEW-14)

1. Captions: text from the narration source, timing from `audio/timeline.json`; never reveal an answer during a response window (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12).
2. Reveals: for each semantic cue, the frame where the element first becomes visible must be within `[word.t0 − 0.05 s − 1 frame, word.t0 + 1 frame]` ([V4-MP] sync rule).
3. Cue sheet staleness: the sheet's `narration_audio_sha256` and `script_sha256` equal the accepted audio and approved script (#63); the render manifest shows `__cueSource` = "injected" or "path" with no `W_*_FALLBACK` entries (contract §8).
4. A/V offset: measure the first audible onset against its expected sample; a constant offset suggests encoder delay (NEW-14) [Hypothesis].

### A11 · Media probe (#10, #16, NEW-13)

Existing `media_check()` rules (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.2): dimensions, duration within 0.03 s, exact frame count, codec h264, pix_fmt yuv420p, audio stream present. Production values for this layer: **30 fps** and a resolution that **must equal the aspect declared by the Format Spec**. The default is **1080×1920** (AD-07). **1920×1080 is accepted only when the Format Spec declares 16:9 and 16:9 safe-zone tokens exist** (the A4 tokens for that aspect are registered and measured); a 16:9 file for a format that declares 9:16, or a 16:9 file with no 16:9 safe-zone tokens, fails A11. The expected resolution is read from the EPP (`resolved.resolution`), not hard-coded. *15 Oct 2026 (audit M1, science-safety-13): RD-16 is SUPERSEDED (vertical-only for the legacy formats, `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`), so A11 no longer accepts 1920×1080 by default. **Amended 15 Oct 2026 (Content Engine v2, CE-L7, CE-46, CE-69):** aspect is a Format Spec field, so A11 no longer rejects 1920×1080 outright; the rule above applies. Earlier text allowed 1920×1080 "while RD-16 stands" and, between the two amendments, "1080×1920 at 30 fps only".* `audio_present` false is a Critical for release (#10).

### A12 · Science re-check (#12, #64)

A12a re-runs the subject validators on the fixtures used by the render (hashes must match the GA-approved bundle). A12b is the existing science-frame QA: "the displayed number, the graph state and the narration must agree at each event" (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §3). For animated scenes add: axes and units visible on every sampled frame; scales unchanged between compared states; arrow directions as in the fixture; decorative wobble amplitude zero on data-bound strokes (NEW-28).

### A13 · Contrast and phone readability (NEW-31)

Existing rules: ≥ 4.5:1 for text against its actual adjacent background, ≥ 3:1 for essential graphics, adjacent-accent pairs checked, essential text readable at 360 px display width (`Displayed = Source × 360 / master width`; RD-18). Run on real frames of every style, including collage tiles and paper textures.

### A14 · Camera-fx guard (#64)

The harness logs composition-wide transforms (push-in, shake, pan) per frame. Fail if any is non-identity while a science element (one carrying `data-fx`) is being revealed or emphasised, or during a `hold` cue on a science element. The cue-sheet schema has no "measure" tag, so science is identified by `data-fx`.

### A15 · Non-empty frames (NEW-21, NEW-22)

Fail on uniform or all-black frames not declared in the cue sheet; on WebGL context-loss events in the render log; and on frames whose content hash equals the previous frame for longer than the longest declared hold plus a margin (a stalled render) [Recommendation].

### A16 · Asset provenance and licence (NEW-2, NEW-7, NEW-25)

Every font, SFX, music bed, SoundFont, texture, mesh, generated image and clip has an `AssetManifest` entry with `content_sha256`, `origin`, `licence`, `attribution`; generated assets carry provider, model and job ID (`07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §3.8). An unlicensed asset is **Critical** (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §4). Reference videos are analysis inputs only, never assets (report §10 item 2).

### A17 · Ledger (#1–#6, #60, NEW-26)

A17a before authoring: caps, effort and model audit (doc 09 §4, §10). A17b after: every run recorded with tokens and outcome; missing sub-agent counts flagged.

---

## 3. Human gates

| Gate | When | Who | Decides | Bound to | Source |
|---|---|---|---|---|---|
| **GA** Academic approval | Before storyboard and synthesis | Academic owner (+ native editor for localised scripts) | Claims, script, answer keys, model assumptions, **planned scientific visuals** | Script bundle hash | `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` GA |
| **H-SB** Storyboard gate (specified in `12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md`) | After the 3×3 grid, before paid assets and scene code | Pilots: founder (cost) and academic lead (fit with the approved script), per doc 05 §1; the animation director prepares it | Visuals, scope, route tags, token/credit estimate | Grid, `beats.json`, `estimate.json` hashes | [V4] review checkpoint ("Stop after Steps 2 and 3… wait for my approval"); #47 |
| **H-RV** Director rubric review | After automated QA passes | Production director | Rubric §4; accept or send back (counts against caps) | Scene render hash | [Recommendation] |
| Native reader | Indic editions | Native-language reviewer | Shaping, wording, numerals | Render hash | doc 08 §7.6; `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §18 |
| **GF** Final video review | After all QA | Academic owner **and** a different production reviewer, full watch | The four release questions (scientific, instructional, perceptual, emotional) | SHA-256 of `final.mp4` | `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §5 |
| **GS** Short approval | Each Reel/Short | Same two roles | Same questions, plus "complete payoff", retained conditions | SHA-256 of the Short | `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` SH7 |

Approvals come only from the authenticated approval service; agents never write approvals; local JSON is a policy demonstration (RD-17, RD-32).

---

## 4. Review rubric (director, H-RV; also the evidence for GF)

Score each criterion as **Pass**, **Minor**, **Major** or **Critical** using the house severity classes (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §4). No aggregate score; the worst cell decides.

| # | Criterion | Critical when | Major when | Minor when | Source |
|---|---|---|---|---|---|
| R1 | **Science accuracy** | Any wrong value, label, unit, direction, shape or condition; decoration contradicts the science; science-looking text not traceable to a fixture field (15 Oct 2026) | — (any science error is Critical) | — | Report §7.13; ROOT/07 06 §4 |
| R2 | **Instructional function** | Answer revealed before the learner's attempt (any early answer reveal is Critical, never Major; 15 Oct 2026) | Animation is decorative where the learner must inspect; too dense to follow | One unnecessary flourish | `02_learning_psychology/INSTRUCTIONS_production_rules.md` E1–E3 |
| R3 | **Readability** | Essential symbol unreadable at phone size | Hold too short; safe-zone intrusion | Slight crowding | A4, A5, A13 |
| R4 | **Sync** | Reveal contradicts narration (shows the wrong item) | Reveal off its word by more than ~0.2 s | Off by 0.05–0.2 s | [V4-MP] sync rule |
| R5 | **Audio** | Missing narration or audio stream | Music under core explanation; loudness out of range | SFX slightly loud | Doc 06 |
| R6 | **Accessibility and safety** | Photosensitive flashing; **any** full-frame flash (15 Oct 2026) | Colour-only encoding; captions missing | Caption line breaks | A6, A13; ROOT/02 D4, D7 |
| R7 | **Craft: brief adherence** | — | Generic look (#8), style guide ignored, flat where depth was briefed | Easing or timing nit | [N50]–[N53]; [V2] critique "flat and cartoonish" |
| R8 | **Craft: motion** | — | Linear or floaty motion against the style; scattered micro-animations | One overlong idle | [V4-MP] §8; [N53] |
| R9 | **Emotional tone** | Humiliating or mocking content | Fake urgency; identity praise | Overly cute | ROOT/07 06 §4 Super Teacher gate |
| R10 | **Vertical composition** | Crop removes an axis or condition | Cramped 16:9 layout squeezed into 9:16 (#49) | Minor imbalance | `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` §1 |

Every Critical and Major cell records the frame time, the element ID and the smallest repair at the owning stage (S16 repair loop).

---

## 5. What blocks release

Release (GF or GS) is blocked if **any** of these holds:
1. Any Critical in the rubric, or any failed science check (A12).
2. A1 lint failure, A3 determinism failure, A11 media probe failure, A15 empty frames.
3. A4 essential safe-zone violation; A5 science-text hold violation; A6 flash violation; A7 text mismatch or text in a generated raster.
4. A9 loudness/peak outside tolerance; A10 caption error that changes meaning or an answer revealed early.
5. A16 unlicensed or unprovenanced asset.
6. Missing GA, GF (both roles, different identities, full watch) or GS; any approval bound to a different hash.
7. Any item of the Super Teacher release gate: "an unresolved critical scientific claim, misleading analogy, humiliating line, incorrect answer, inaccessible essential symbol, deceptive personal response, missing rights, or untested critical pronunciation" (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §4).
8. Engine `release-check` reasons 1–10 (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §6.1) and narration evidence keys (§6.2).

Major defects are repaired and re-reviewed; Minor defects are tracked.

**Severity alignment, 15 Oct 2026 (audit science-safety-6 and -12).** Three defects are **Critical and never waivable** in both the scripts and this document: untraceable science-looking text (`text_fixture_diff.py`, A7/R1), any full-frame flash (`flash_check.py`, A6/R6; a flashing tile above 3/s stays Major because the area condition needs a human), and an early answer reveal (`safe_zone_check.py --cues` using the cue sheet's `meta.answer_protection`, A10/R2). `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §4 was aligned the same day (early answer reveal moved from Major to Critical), so the runbook and this layer now agree.

---

## 6. Integration with existing skills

| New check | Extends | Output |
|---|---|---|
| A1, A3, A15 | `examleaf-web-composition` / `examleaf-render-batch` via `examleaf-motion-harness` | `qa/anim_contract.json`, `qa/determinism.json` |
| A4, A5, A6, A7, A14 | `examleaf-visual-qa` via `examleaf-anim-qa` | `qa/anim_visual.json` + overlay PNGs |
| A8 | `examleaf-visual-qa` via `examleaf-kinetic-typography` | `qa/glyph_coverage.json`, `qa/indic_shaping.md` |
| A9, A10 | `examleaf-audio-caption-qa` (+ `examleaf-audio-production-engineer`) | `qa/audio_caption_qa.json` |
| A12 | `examleaf-science-<subject>`, `examleaf-visual-qa` | `science/science_report.json`, `qa/visual_qa.json` |
| A16 | `examleaf-asset-library` | asset ledger |
| A17 | `examleaf-observability-cost` via `examleaf-effort-governor` | `costs.json` |

`examleaf-release-review` assembles these reports into the release evidence for GF/GS; "it never approves" (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` GF).

**`qa/anim_qa.json` (summary record, minimum):** `scene_id`, `render_sha256`, `frame_hash_list_sha256`, `checks[{id, passed, severity, details, frames[]}]`, `rubric{R1…R10}`, `reviewer_role`, `tool_versions`, `created_at`. One record per scene; a lesson-level roll-up lists every scene.

---

## 7. What re-runs when something changes

| Change | Re-run | Approvals invalidated |
|---|---|---|
| Fixture value or science assumption | A12, A7, A3, all renders using it, A4–A6 | GA and GF (S15 table) |
| Narration segment regenerated | Cue sheet rebuild, renders of affected scenes, A3, A5, A10, A9 | GF |
| Scene code or style token | A1, A3, A4–A7, A13–A15 | GF |
| Font file or version | A8, A3, A4, A13 | GF |
| Music bed, SFX, mix | A9, A10, A16 | GF |
| Harness, Chrome, three.js, Manim or render box | A2, A3 on all affected scenes (cache keys change) | GF |
| Short cut from an approved lesson | Full A-suite on the Short | GS (new artefact) |

---

## 8. Evidence package for GF/GS

1. `final.mp4` (or the Short) with SHA-256.
2. Render manifests, clip manifests, frame-hash lists.
3. `qa/*.json` from §6 and overlay images for flagged frames.
4. Science report and fixture hashes matching the GA bundle.
5. Narration evidence keys (academic listening, voice rights, native review, caption review, sync review, mastering).
6. Asset ledger extract for every asset in the video.
7. Rubric record (H-RV) and storyboard approval (H-SB).
8. Cost ledger summary (`costs.json`).

Reviewers watch the **whole** video, with narration and captions, including on representative small phones; "Sampling frames can support automated QA. It does not replace watching the whole final video" (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §5).
