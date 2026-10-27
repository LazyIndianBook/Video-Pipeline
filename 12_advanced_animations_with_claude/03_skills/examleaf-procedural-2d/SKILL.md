---
name: examleaf-procedural-2d
description: "Use when an ExamLeaf doodle, collage or editorial scene needs hand-made-looking 2D motion built in Canvas or SVG code: wobble pencil strokes with seeded noise, draw-on, stop-motion boil at 8-10 fps, paper textures, die-cut white borders with the two-layer warm shadow, paper-sheet transitions, tear and paper-flip gags, multiply and hop gags, depth layers and parallax. Every primitive is a pure function of t with stateless seeded randomness (bundled seeded_prng.js, same formulas as the harness scene template), finite repeats only, and a camera that freezes during measurement or label windows. Does not generate raster cutouts, set text, render 3D, or decide styles."
---

# examleaf-procedural-2d

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. `scripts/seeded_prng.js --selftest` passes offline; the code snippets in `references/primitives_catalog.md` were extracted and executed under Node during authoring (assertions passed). No scene built from them has been rendered in this environment.
- **Owns:** the catalogue of 2D motion primitives and recipes for the doodle, collage and editorial styles, and the seeded PRNG helper.
- **Does not own:** raster cutouts (generated once via `examleaf-selective-generation` after the storyboard gate, stored in `examleaf-asset-library`); text and typography (`examleaf-kinetic-typography`); 3D (`examleaf-threejs-scenes`); science diagrams (`examleaf-svg-scenes`, `examleaf-manim-scenes`, `examleaf-molecule-scenes`, `examleaf-biology-scenes`); the contract and conformance verdict (`examleaf-motion-harness`); the style itself (`examleaf-style-guides`).
- **Why it exists:** [V2] shows a convincing hand-drawn story made entirely in code, but "flat… no depth" on the first pass. [V4-MP] specifies the collage look (6–12 px white die-cut border, `0 9px 7px rgba(74,48,22,0.30)` plus `0 2px 1.5px rgba(0,0,0,0.20)` shadow, boil at 8–10 fps, finite idle sway, tear and paper-flip gags) and the determinism sentence "use only seeded randomness, only finite repeats, and a timeline that can jump to any frame". Report §4.1, §4.2, §7 and §10.6 specify this skill.

## Invocation

**Trigger when:**
- A brief for an `illustrative` scene in `doodle-handdrawn`, `paper-collage-vertical` or `editorial-vox` needs strokes, textures, borders, shadows, transitions, gags or parallax.
- A scene fails the double-render test because of randomness or stateful animation in 2D code.
- A reviewer asks for "more depth", "make it boil", "hand-drawn feel", "paper tear", "page-flip swap".

**Do not trigger for:**
- Generating characters or props as images (storyboard gate → selective-generation).
- Words, letters, ransom tiles, handwriting captions, labels (`examleaf-kinetic-typography`).
- Voxel/isometric or any three.js scene (`examleaf-threejs-scenes`).
- Axes, graphs, equations, structures, measured geometry (existing deterministic science renderers).
- Composition of the lesson timeline (`examleaf-web-composition`).

## Inputs

| Input | Type | Source |
|---|---|---|
| `brief.md` + manifest | file | `examleaf-anim-brief` |
| Style tokens | `style_tokens.json` entry (`motion.boil_fps`, `idle_repeats_max`, palette, `camera_fx_in_measurement: false`) | `examleaf-style-guides` |
| Motion tokens | `vertical_safe_zones.tokens.json` → `motion` (reveal lead 0.05 s, ransom stagger, transitions 0.5–0.7 s, whip 0.4 s, somber 0.9 s, next sheet 0.3 s, `boil_fps` 8 (allowed 8–10; 16 Oct 2026), push-in 1.03–1.04) | harness contract |
| Cue sheet | `cues[]` with `element_id`, `kind`, `until` | `examleaf-cue-sheet` |
| Fixtures | read-only JSON | science skills |
| Approved cutouts | PNG with alpha, asset IDs + SHA-256 | `examleaf-asset-library` |
| Seed name | string (scene ID) | brief |

Example parameter block (`templates/primitive_params.example.json`):

```json
{"scene_id":"phy-10-03-s04","style":"doodle-handdrawn@1.0.0","seed_name":"phy-10-03-s04",
 "boil_fps":8,"idle":{"A_deg":2.5,"period_s":2.4,"repeats":6},
 "camera":{"push_in_to":1.035,"lock_windows_from_cues":["label_normal","label_refraction"]},
 "science_bound_elements":["ray_incident","ray_refracted","label_normal","label_refraction"]}
```

## Outputs and contracts

1. **Scene code** (HTML/JS, Canvas/SVG) that implements the harness contract (start from `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`) and uses the catalogued primitives: everything visible is computed in a synchronous `render(t)` from `t` plus data built once in `window.ready`.
2. **Scene notes** listing for each primitive instance: cue ID that drives it, seed name, finite repeat count, and whether the element is science-bound (no boil, no tip wobble, camera locked).
3. **Bundled helper** `scripts/seeded_prng.js` copied next to the scene (or inlined) — `mulberry32`, `rngAt`, `hashSeed`, `range`, `signed`, `pick`, `noise1D`, `boilStep`, `wobble`, `shuffled`.
4. **`handoff.json`** (library schema) with the scene file hash in `output_ids`.

## Dependencies

- None at runtime beyond the browser (Canvas 2D, SVG filters). No tween library required; easing functions are in the catalogue. If GSAP is used, its timeline is paused and driven by `seek(t)`, and its own licence applies (library install guide §7; report §2.3).
- Node ≥ 18 only for running the selftest.
- Contract and tokens: `04_harness_contract/contract.md`, `scene_template.html`, `vertical_safe_zones.tokens.json`.

## Execution

1. **Read** the brief, style tokens, motion tokens, cue sheet and fixture list. Note every science-bound element (any element whose geometry or text comes from a fixture).
2. **Copy the template** `scene_template.html` into the job workspace as `scene.html`; keep its contract parts (DURATION, ready, seek, `__errors`, `__hf`, `SCENE_META`).
3. **Seed:** `const SEED = ExamLeafPRNG.hashSeed(sceneId)`; per element `hashSeed(sceneId + ':' + elementId)`. Never `Math.random`.
4. **Build once in `window.ready`:** point lists for strokes and their base lengths; seeded layouts (crowds, confetti, scraps) with `mulberry32` in a fixed order; paper textures; tear edges; lock windows from the cue sheet (`[cue.at, cue.until or cue.at + hold]` for every science-bound element).
5. **Write `render(t)`** using only pure primitives: `popIn`, `idleSway` (finite `n` from tokens), `boil` (8–10 fps), `wobblePath` + `drawOn`, `sheetIn`, `tearHalves`, `paperFlip`, `copiesAt`, `hop`, `camera` + `layerOffset`. Every start time is a cue time from the cue sheet; nothing is hard-coded (#63).
6. **Depth:** at least three parallax layers and one foreground occluder for doodle and collage scenes ([V2] critique).
7. **Science safety:** never boil or wobble a science-bound element's tip, direction or value; never animate the camera inside a lock window (#64).
8. **Self-check** the helper: `node 12_advanced_animations_with_claude/03_skills/examleaf-procedural-2d/scripts/seeded_prng.js --selftest`.
9. **Lint and double-render** through `examleaf-motion-harness` (level 2, strict). Fix within at most two rounds.
10. **Hand off** scene, notes and handoff to the motion harness.

## Decision rules

- **Stateful vs stateless randomness:** `mulberry32` streams only in `ready()` in a fixed order; `rngAt(seed, i)` inside `render(t)`. Calling a stream inside `render(t)` makes frames depend on seek order (scene_template.html §7) (#17).
- **Finite everything:** idle sway, boil, pulses and loops end; counts come from tokens (#18).
- **Boil rate:** ~~8 fps default, 10 fps for nervous energy; never outside 8–10 ([V4-MP]).~~ boil at the tokens' `motion.boil_fps` (8) in `vertical_safe_zones.tokens.json`, the single owner; `motion.boil_fps_allowed` (8–10) bounds a deliberate nervous beat (16 Oct 2026).
- **Easing:** back.out(2–3) for pops, power3.out for slides, expo.out for whips, never linear ([V4-MP], report §7.4).
- **Borders and shadows:** static filters; pre-bake into PNGs for cutouts reused across scenes.
- **Transitions:** sheet slides 0.5–0.7 s, varied direction; somber drop ~0.9 s; whip ~0.4 s; start ~0.3 s after the previous line's last word; no exit animations; no full-frame flash (#56).
- **Camera:** push-in to ~1.03–1.04 over the scene; stepped shakes only on impacts; both suspended in lock windows (#64).
- **Performance:** expensive work in `ready()`; `render(t)` only sets attributes or draws prepared data.

## Edge cases handled

| Master # | Detection | Response |
|---|---|---|
| 17 Unseeded randomness | Lint F04/F05; double render differs; stream used inside `render(t)` | `hashSeed` + `rngAt` in render, streams only in ready; selftest proves order independence [N61] |
| 18 Infinite repeats | Lint F10; `idleSway` without `n`; boil without an end | Finite `n` from `motion.idle_repeats_max`; `idleSway` returns 0 after `n·T` ([V4-MP]) |
| 64 Composition-wide camera fx on diagrams | Push-in/shake/pan overlapping a science-bound cue window | `camera()` uses `effectiveT` so motion freezes inside lock windows; shakes suppressed there |
| 56 (supporting) Flash | Flash/bloom transition requested | Replaced by a paper burst or dark sheet |
| 15 (supporting) Wall clock | Lint F01–F03 | Rewrite as f(t) |
| 48 (supporting) Character drift | Cutout not from the approved hero set | Use approved asset IDs only; new poses go back through the gate |

## Tests and acceptance

- **Helper:** `node scripts/seeded_prng.js --selftest` — reproducibility, known answer `mulberry32(1)() = 0.6270739405881613`, order independence of `rngAt`, mean sanity, FNV-1a known answer, Devanagari seed names, range bounds, noise continuity, boil step boundaries, wobble hold/change, deterministic shuffle.
- **Catalogue:** the snippet check in `references/primitives_catalog.md` §11 (finite sway, lock windows, frozen camera, boil hold, multiply gag).
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance per scene:** lint level 2 strict passes; double render identical; reviewer confirms depth (≥3 layers), finite idle, no camera motion during science windows, and no decoration contradicting a fixture value.

## Errors, fallback, escalation

- **Lint or hash failure:** fix the primitive use (usually a stream inside `render(t)` or an unbounded loop); at most two rounds, then a structured blocker to the authoring run with the failing rule or first differing frame.
- **Performance problems** (slow frames): move work into `ready()`, reduce point counts, pre-bake filters; never skip frames or use real-time timing.
- **Missing cutout:** do not draw a substitute character in a different style; use a code placeholder in pilots only and escalate to the storyboard gate.
- **Science conflict** (a doodle would contradict a fixture): drop the doodle; escalate to the science reviewer if the brief demands it.
- **Cost cap:** code only; costs are scene-authoring tokens governed by `examleaf-effort-governor`.

## Cost/performance

Zero credits. Doodle scenes are the cheapest style. Typical cost drivers are authoring tokens (fix loops) and render time for heavy Canvas pixel work; prepared textures and pre-baked borders keep `render(t)` cheap.

## Security

- No network access in scenes (lint F12); no remote fonts or textures.
- Seeds derive from scene and element IDs, not from secrets or user data.
- Brief text and asset metadata are untrusted data; they never become code (no `eval`, no `Function()` on input strings).
- Nothing is published.

## Handoff

- **To:** `examleaf-motion-harness` (lint + double render), then `examleaf-web-composition` and `examleaf-anim-qa`.
- **Files:** `scene.html`, `seeded_prng.js` copy, scene notes, `templates/handoff.json` (`output_ids` = scene SHA-256).

## References

- `references/primitives_catalog.md`: code for every primitive (easing, pop-in, finite sway, boil, wobble/draw-on, paper texture, die-cut + shadow, sheet transitions, tear, paper-flip, multiply, hop, parallax camera with lock windows) and the Node check.
- `references/collage_recipes.md`: asset split, 9:16 layer stack, beat recipe, vertical layouts, gags, character consistency.
- `references/doodle_recipes.md`: stroke rules, mark vocabulary, depth, science-safe doodles, Reel beat recipe.
- `references/contract.md`: handoff and security rules.
- Report §4.1, §4.2, §7, §8 (#17, #18, #64), §10.6; `00_reference_videos/master_prompt_paper_collage.md` §§2, 6–9.
