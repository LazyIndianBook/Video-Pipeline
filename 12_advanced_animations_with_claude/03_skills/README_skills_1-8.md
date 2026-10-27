# Advanced-animation skills 1–8

Eight Claude Agent Skills for ExamLeaf's code-to-video animation layer. They follow the library contract in `06_skills_library/INSTRUCTIONS_install_and_use_skills.md` (§4–5): YAML `name` = folder name, a "Use when…" description, typed I/O, approved dependencies, required evidence, forbidden transformations, acceptance tests and escalation. Each folder holds `SKILL.md`, `references/` (at least two in-depth documents plus `contract.md`), `templates/` (with `handoff.json` in the library's VE schema), `evals/cases.json` (`"status": "authored_not_agent_executed"`, at least 3 positive and 3 negative cases) and `scripts/` (offline `--selftest`).

**Status: authored, not agent-evaluated.** A passing selftest is helper evidence only, not evidence of agent behaviour. Skills 9–15 (`examleaf-audio-compose`, `examleaf-audio-analysis`, `examleaf-cue-sheet`, `examleaf-mcp-orchestrator`, `examleaf-effort-governor`, `examleaf-anim-qa`, `examleaf-vertical-adapt`) are in this folder too and are documented by their own README.

Citations: [V#] reference videos, [V4-MP] master prompt, [N#] verified web evidence, as in `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. Edge-case numbers refer to report §8.

## Pipeline position

```text
script approved ⛔ → storyboard-route → [4] anim-storyboard-gate ⛔ → (assets via mcp-orchestrator/selective-generation)
   → [3] style-guides (style pin) + [2] reference-analyzer (numbers) → narration → alignment → cue-sheet
   → [1] anim-brief → scene authoring with [6] procedural-2d / [7] kinetic-typography / [8] threejs-scenes
   → [5] motion-harness (lint + double render) → web-composition → anim-qa → release-review ⛔
```

## The skills

### 1. `examleaf-anim-brief`
- **Purpose:** assemble the L2/L3 structured brief for one scene (report §10.1).
- **Inputs → outputs:** approved script (read-only, hash), route tag, pinned style, cue sheet, brand tokens, optional reference analysis, fixtures, holds, effort, iteration cap, workspace → `brief.md` (canonical `06_prompts_and_templates/brief_template.md` or fallback skeleton) with the ten-rule constraints block + `brief_manifest.json`.
- **Owns:** the brief and its manifest. **Complements:** `examleaf-storyboard-route`, `examleaf-pacing-controller` (consumes holds), `examleaf-effort-governor` (consumes model/effort/cap).
- **Edge cases:** #7, 8, 9, 11, 12, 50, 60 (supporting #1, 3, 63).
- **Script:** `scripts/build_brief.py` — validates inputs and renders the brief. Selftest: `python3 examleaf-anim-brief/scripts/build_brief.py --selftest`.

### 2. `examleaf-reference-analyzer`
- **Purpose:** turn a reference video into measured pacing and style numbers (report §7.10, §10.2).
- **Inputs → outputs:** local reference mp4 + rights note → `reference_analysis.json` (fps, VFR flag, duration, orientation, letterbox crop, shot lengths and cut rhythm, static-hold estimates, palette swatches, quarantined stills, commands, FFmpeg version); `rights: analysis_only`.
- **Owns:** the analysis JSON and quarantined stills. **Complements:** `examleaf-style-guides`, `examleaf-anim-brief`, `examleaf-vertical-adapt`; related shell wrapper `04_harness_contract/reference_analysis.sh`.
- **Edge cases:** variable fps, letterboxed 16:9, missing ffprobe/FFmpeg, copyrighted references (analysis only), #49, #50, #56.
- **Script:** `scripts/analyze_reference.py` — wraps ffprobe and FFmpeg (scene-change `select` + `showinfo`, `cropdetect`, `freezedetect`; standard usage, verify on your build) and parses their logs; explains and exits 2 if FFmpeg is missing. Selftest (synthetic logs, no FFmpeg needed): `python3 examleaf-reference-analyzer/scripts/analyze_reference.py --selftest`.

### 3. `examleaf-style-guides`
- **Purpose:** versioned library rules for the five 9:16 house styles: selection, versioning, application (report §4, §10.3).
- **Inputs → outputs:** route tag, purpose, format, language, credit budget, `05_style_guides/style_tokens.json` → style decision (`id@version`, fonts, holds reference, warnings) + validation report + change records.
- **Owns:** selection/versioning rules and validation of the canonical tokens (the guide texts and tokens live in `05_style_guides/`). **Complements:** `examleaf-asset-library` (owns brand tokens and licences), `examleaf-vertical-adapt` (per-scene re-layout).
- **Edge cases:** #49, 54, 55, 56 (supporting #8, 18, 64).
- **Script:** `scripts/validate_style_tokens.py` — validates the canonical file (canvas, forbidden flags, determinism flags, display-font bans and Inter roles, Indic coverage and units, holds, iteration cap, accents, boil range, finite repeats, semver; `--production`; `--bump-check OLD NEW`). Selftest: `python3 examleaf-style-guides/scripts/validate_style_tokens.py --selftest`. Real run: `python3 examleaf-style-guides/scripts/validate_style_tokens.py` (defaults to `../05_style_guides/style_tokens.json`).

### 4. `examleaf-anim-storyboard-gate`
- **Purpose:** 3×3 portrait storyboard grid per segment, token and credit estimate, hard stop for human approval (report §6.1, §9 step 4, §10.4).
- **Inputs → outputs:** routed scenes, script hash, style pin, caps, operator-verified prices → `beats.json`, `grid_<n>.png`, `estimate.json` (expected and worst case vs job cap and plan balance), `approval_record.json` (approved=false, bound to hashes).
- **Owns:** grid, beats, estimate and approval record. **Extends:** `examleaf-storyboard-route` (which keeps routing). **Complements:** `examleaf-mcp-orchestrator` / `examleaf-selective-generation` (paid calls), `examleaf-observability-cost` (ledger).
- **Edge cases:** #41, 42, 45, 47, 48 (supporting #54, 60).
- **Script:** `scripts/estimate_and_gate.py` — estimate + beats + approval stub; `--verify-approval` gate for downstream steps. Selftest: `python3 examleaf-anim-storyboard-gate/scripts/estimate_and_gate.py --selftest`.

### 5. `examleaf-motion-harness`
- **Purpose:** one seek contract for HyperFrames, Remotion and raw pipelines, enforced by lint and a double-render frame-hash test (report §2, §10.5).
- **Inputs → outputs:** scene file, validated cue sheet, fixtures, target, level, render-box fingerprint → lint report, hash report + frame manifest, render manifest, conformance verdict.
- **Owns:** the conformance verdict. **Extends:** `examleaf-web-composition` (which keeps engine choice and composition). Canonical contract: `04_harness_contract/contract.md`.
- **Edge cases:** #14–24, 26, 65 (supporting #55).
- **Scripts:** `scripts/lint_seek_contract.js` (Node ≥ 18, no deps) and `scripts/determinism_hash_check.py` (stdlib) — byte-identical copies of the canonical `04_harness_contract/` files; drift check `cmp` in the SKILL. Selftests: `node examleaf-motion-harness/scripts/lint_seek_contract.js --selftest`; `python3 examleaf-motion-harness/scripts/determinism_hash_check.py --selftest`.

### 6. `examleaf-procedural-2d`
- **Purpose:** Canvas/SVG primitives for doodle, collage and editorial scenes, all functions of t (report §4.1–4.2, §10.6).
- **Inputs → outputs:** brief, style and motion tokens, cue sheet, fixtures, approved cutouts → seek-pure scene code + scene notes (cue per primitive, seeds, finite counts, science-bound elements).
- **Owns:** the primitives catalogue and recipes. **Complements:** `examleaf-kinetic-typography` (text), `examleaf-selective-generation` (cutouts), science renderers (diagrams).
- **Edge cases:** #17, 18, 64 (supporting #15, 48, 56).
- **Script:** `scripts/seeded_prng.js` — mulberry32 stream, stateless `rngAt` (same formulas as `scene_template.html`), FNV-1a seeds, value noise, boil and wobble helpers. Selftest: `node examleaf-procedural-2d/scripts/seeded_prng.js --selftest`.

### 7. `examleaf-kinetic-typography`
- **Purpose:** word- and grapheme-cluster-timed type animation from the cue sheet in ransom, handwriting, label, kinetic-headline and equation modes, Hindi/Assamese-safe (report §4.4, §10.7).
- **Inputs → outputs:** cue sheet, type spec, style and hold tokens → type plan per element (units, times, holds, warnings) + type code patterns + glyph test result.
- **Owns:** the type animation plan. **Complements:** `examleaf-speech-animation-synchronizer` (captions), `examleaf-style-guides` (fonts), fixture renderers (equation glyphs).
- **Edge cases:** #50, 55, 63 (supporting #8, 11, 54).
- **Script:** `scripts/grapheme_clusters.py` — Devanagari/Bengali-Assamese grapheme clusters via `unicodedata` (limits vs full UAX #29 documented) and `--plan` timing with hold checks; refuses code-point mode. Selftest: `python3 examleaf-kinetic-typography/scripts/grapheme_clusters.py --selftest`.

### 8. `examleaf-threejs-scenes`
- **Purpose:** seek-pure three.js for orbitals, lattices, field lines, waves, trajectory replays and voxel recaps, fed only by fixtures (report §2.4, §4.5–4.6, §10.8).
- **Inputs → outputs:** brief, validated fixtures, cue sheet, style tokens, render-box fingerprint → scene file, scene notes (value → fixture field), fixture validation reports, PNG sequence → clip.
- **Owns:** three.js scene patterns, 3D recipes, headless WebGL policy, fixture validator. **Complements:** `examleaf-molecule-scenes` (molecules), `examleaf-blender-scenes` (hero 3D), science skills (fixtures).
- **Edge cases:** #15, 17, 65, WebGL context loss (supporting #12, 64).
- **Script:** `scripts/validate_trajectory_fixture.py` — provenance, units, finite values, monotonic time, fixed step, t₀ = 0, coverage, sampling vs fps. Selftest: `python3 examleaf-threejs-scenes/scripts/validate_trajectory_fixture.py --selftest`.

## Run every selftest (from this folder, offline)

```sh
python3 examleaf-anim-brief/scripts/build_brief.py --selftest
python3 examleaf-reference-analyzer/scripts/analyze_reference.py --selftest
python3 examleaf-style-guides/scripts/validate_style_tokens.py --selftest
python3 examleaf-anim-storyboard-gate/scripts/estimate_and_gate.py --selftest
node    examleaf-motion-harness/scripts/lint_seek_contract.js --selftest
python3 examleaf-motion-harness/scripts/determinism_hash_check.py --selftest
node    examleaf-procedural-2d/scripts/seeded_prng.js --selftest
python3 examleaf-kinetic-typography/scripts/grapheme_clusters.py --selftest
python3 examleaf-threejs-scenes/scripts/validate_trajectory_fixture.py --selftest
```

All nine exited 0 on 2026-10-15 (Python 3.14.2, Node 20.19.4, no FFmpeg installed).

## Ownership notes (one owner per output)

| Output | Owner here | Must not be re-authored by |
|---|---|---|
| Brief + manifest | anim-brief | storyboard-route, scene authoring |
| Reference analysis JSON | reference-analyzer | style-guides (reads it) |
| Style decision, tokens validation | style-guides | asset-library owns brand tokens; vertical-adapt owns scene re-layout |
| Grid, beats, estimate, approval record | anim-storyboard-gate | storyboard-route (routing only), selective-generation (paid calls only) |
| Conformance verdict | motion-harness | web-composition (composition only); anim-qa should call the same hash script |
| 2D primitives | procedural-2d | — |
| Type plan | kinetic-typography | speech-animation-synchronizer owns captions |
| three.js scenes | threejs-scenes | molecule-scenes owns molecules; blender-scenes owns hero 3D |

Installation follows the library guide: copy only the reviewed, stage-relevant folders into `.claude/skills/`; never mass-load; run the eval cases before relying on a skill.
