# Style guide: doodle-handdrawn (pure-code hand-drawn doodle, 9:16)

**Style ID:** `doodle-handdrawn` | **Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot
**Derived from:** the doodle style in [V2] (RandomAI, L2 demo, a story animated entirely in JavaScript), plus the report's §4.2 and §7. Re-laid out for ExamLeaf 1080×1920.
**Machine-readable twin:** `style_tokens.json` (`styles["doodle-handdrawn"]`).
**ExamLeaf default style for Reels:** [Recommendation] (report §4.2). Reasons in §1.

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement; [Hypothesis] = untested; "verify" = not confirmed. Edge cases are #1-#65 (report §8). Project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## Digest (read this first; the full guide governs on conflict)

1. Pure code: SVG/Canvas paths with seeded wobble, stroke-dash draw-on, ~~boil at 10 fps~~ boil at the tokens' `motion.boil_fps` (8) (16 Oct 2026), a pencil-texture overlay, flat fills. No image model, no credits.
2. Flat is a known failure ([V2] critique). Use the depth rules in §3: at least three layers, parallax factors, overlap, hatch shadows, line-weight hierarchy, a foreground frame.
3. Palette is the ExamLeaf light tokens (`#F7F9FC`, `#14213D`, `#526074`, `#185ABD`, `#087986`, `#9A5B00`, `#6E44AA`, `#B42318`) plus one proposed biology green (`#1F7A3E`). Subject accents decorate; they never encode a quantity.
4. Fonts: Inter/Noto Sans for labels and captions, a Devanagari-capable handwriting font for doodle titles (candidate Kalam; verify), KaTeX for formulae. Banned as display: Arial, Inter, Space Grotesk, system-ui.
5. Stacked zones in the platform-safe box (insets from `04_harness_contract/vertical_safe_zones.tokens.json`): title 22%, visual 54%, caption 24% (mirroring the token file's `zones`); side margin at least 96 px.
6. Motion: draw-on, pop with `back.out(1.7)`, finite wiggles, hatch-in shadows; all reveals on the cue-sheet word; every loop finite; seeded stateless PRNG; seek-driven.
7. Doodle frames hooks, analogies and recaps. Axes, values, equations and labelled structures come from fixtures and are never wobbled.
8. Writing: Super Teacher voice, script from the narration system; 0-3 s hook, 3-8 s prediction window, payoff, one CTA.
9. House loudness -16 LUFS, true peak at most -1 dBTP; SFX light; no music under reasoning.
10. Cost: zero credits.

---

## 1. Why this is the default Reel style [Recommendation]

- **Cheapest.** No image-model calls, so no credit ledger, no character drift (#41, #42, #48), no Higgsfield dependency.
- **Deterministic.** Strokes are computed from seeds and time, so frames are reproducible and can be re-seeked for any cut (#17).
- **Honest to the science.** Hand-drawn framing around a clean fixture panel reads as a teacher's marker on a board. It does not pretend the doodle is data.
- **Fast to iterate.** Reel scenes are 20-60 s (RD-19). A doodle hook is small enough to fit the iteration cap of three fix loops.
- **Switch when needed.** Use `paper-collage-vertical` for story or analogy scenes that need painted charm; `editorial-vox` for comparisons and scale stories; `kinetic-type` for text-only hooks; `voxel-isometric` for lattices, organelles or concept islands. The route tag decides first (README §2).

## 2. The look and how it is produced

### 2.1 Strokes ([V2], report §4.2)

- **Wobble.** Resample each path into segments of about 12-20 px; offset each vertex along the normal by a seeded value of amplitude **0.8-2.5 px** (1080-wide); keep endpoints anchored so closed shapes stay closed; smooth the polyline into a curve. Amplitude above 2.5 px reads as shaky and hurts legibility on a phone.
- **Boil.** Re-seed the wobble at a boil rate. ~~Default **10 fps** (exactly 3 frames per step at 30 fps). 8 fps gives a 4-4-4-3 frame pattern and 9 fps gives 4-3-3, which look uneven (checked by arithmetic); allowed range remains 8-10 fps.~~ Boil at the tokens' `motion.boil_fps` (8) in `04_harness_contract/vertical_safe_zones.tokens.json`, the single owner of the rate (16 Oct 2026); `motion.boil_fps_allowed` keeps 8-10 for a deliberate nervous beat. Step `k = floor(t × boil_fps)`; jitter keyed by `(scene_id, element_id, k)` (seeded, stateless; see §12). Boil amplitude **0.8-1.5 px**; up to 3 px for a deliberate "nervous" beat.
- **Draw-on.** Reveal strokes with `stroke-dasharray = L` and `stroke-dashoffset` from `L` to 0, where `L` is the path length. Duration `d = clamp(L / 1100 px/s, 0.25 s, 1.2 s)` [Recommendation]; ease `power1.inOut`. Round caps and joins.
- **Stroke widths** (1080-wide): outline 5 px; detail 3 px; emphasis 7 px; functional marks (circle, tick, underline that tells the learner where to look) 6-8 px. why: a 3 px line is 1 px on a 360-px phone.
- **Off-register fills.** Flat colour fills sit 2-6 px off the outline (seeded per element) after the outline finishes drawing; the fill fades in over 150-300 ms. This is the main "hand-made" cue and costs nothing.
- **Pencil texture.** A static procedural grain overlay (multiply, 6-10% opacity) over the whole frame, generated from a fixed seed so every render is identical. In SVG, `feTurbulence` takes a `seed` attribute; use a fixed integer. Do not boil the texture (three pre-seeded variants cycled at the boil rate are allowed if testing shows the static grain looks dead) [Hypothesis]. Keep texture off the caption plate and off fixture panels.
- **Performance (16 Oct 2026, pilot gap L-16).** The paper/pencil texture is a **static cached layer**: render it once (a pre-rendered image or a canvas drawn at load) and never run a full-stage `feTurbulence` (or any full-stage filter) per frame. Boil only small stroked elements, never the whole stage. Measured in the pilot: a full-stage `feTurbulence` texture re-rasterised every frame cost ≈ 320 ms per captured frame, against ≈ 80 ms for the same scene type without it (4×).
- **Paper.** Plain `#F7F9FC` with the grain. No paper photo textures.

### 2.2 Flat fills, not flat pictures

Fills are flat. The picture is not flat: §3 requires explicit depth cues, because [V2] criticised its first pass as "flat and cartoonish" and "strictly 2D... no depth" (fixed in [V2] only by iterating with the model).

## 3. Depth rules (the fix for the [V2] "flat" critique)

Every illustrative scene must satisfy all of these; `examleaf-anim-qa` can check items 1-3 from the scene graph.

1. **At least four layers** (back to front):

| Layer | Content | Parallax factor | Line weight | Value |
|---|---|---:|---|---|
| L0 | Paper and grain | 0 | none | `#F7F9FC` |
| L1 far | Distant shapes (hills, a window, a shelf) | 0.25 | 0.6× outline | 18% tint of the subject accent |
| L2 mid | Props and secondary characters | 0.6 | 0.8× outline | 28% tint |
| L3 subject | The hero, the key prop, any fixture panel | 1.0 | 1.0× outline (5 px) | full ink `#14213D` |
| L4 frame | A foreground framing element (leaf, desk edge, hand) partly cropped by the frame | 1.4 | 1.2× outline | full ink |

2. **Camera drift** is a function of `t`: total pan at most **30 px** across the scene [Recommendation]. It is zero during any hold, think window, label reveal or measurement (#64). Parallax factors multiply the drift.
3. **Overlap.** Each layer overlaps the one behind by at least 24 px, with a contact shadow between them.
4. **Contact shadows and hatching.** Light comes from the top left, fixed. A shadow is 3-5 diagonal hatch strokes at 45° (spacing 10-14 px, ink at 60% opacity) on the shadow side, drawn on after the object (150-300 ms). No blurred shadows (this style is flat and hand-drawn).
5. **Size diminution.** Distant repeats are 0.6-0.8× the near size.
6. **Value and weight hierarchy.** Far is lighter and thinner, near is darker and thicker. Never the reverse.
7. **Horizon.** If the scene has a ground plane, put the horizon at 55-62% of the visual zone height; put the subject plane below it.
8. **Fixture geometry is sacred.** Depth cues apply only to decoration. A fixture-bound element (an axis, a ray, a labelled structure) is drawn flat by its own skill and sits on L3 with parallax 1.0 and no drift during its reveal (report §7.13, #64).

## 4. Palette

### 4.1 Tokens (from `02_learning_psychology/palette_and_typography_tokens.json`, RD-27: light theme only at launch)

| Role | Hex | Contrast on `#F7F9FC` | Use in this style |
|---|---|---:|---|
| Background | `#F7F9FC` | n/a | Paper |
| Ink / main text | `#14213D` | 15.15 | Outlines at L3, text, equations |
| Secondary | `#526074` | 6.06 | Far-layer outlines, supporting text |
| Blue (primary explanatory) | `#185ABD` | 6.15 | Physics accent; explanatory emphasis |
| Teal (relationship/highlight) | `#087986` | 4.87 | Chemistry accent; relationship highlights |
| Amber (condition or caution) | `#9A5B00` | 5.14 | Only for a condition or caution (for example "same voltage") |
| Purple (secondary relationship) | `#6E44AA` | 6.48 | Mathematics accent |
| Red (error marker) | `#B42318` | 6.23 | Only as an error marker; never for generic decoration |

### 4.2 Subject accents [Recommendation]

Physics = blue `#185ABD`. Chemistry = teal `#087986`. Mathematics = purple `#6E44AA`. Biology = green `#1F7A3E`.
- **Biology green is a proposed new token**, not in ROOT/02. Computed contrast 5.09:1 on `#F7F9FC`. It needs brand-owner approval; until then biology scenes use teal and a label.
- Subject accents colour the hook underline, the tag border and the doodle fills only. They do not encode a quantity: "a quantity does not change colour because the scene changed" and "respect scientific conventions" (ROOT/02 D4).
- Tints for fills (mix of the accent into `#F7F9FC`): 18% tints blue `#CFDCF1`, teal `#CCE2E7`, amber `#E6DDCF`, purple `#DED8ED`, red `#EBD2D3`, green `#D0E2DA`, secondary `#D9DDE4`; 28% tints blue `#B9CCEA`, teal `#B4D5DB`, amber `#DDCDB5`, purple `#D1C6E5`, green `#BBD5C7`. Ink `#14213D` on every tint is at least 9.8:1 (computed). Use "a pale highlight area with dark text, not a large saturated block behind a long explanation" (ROOT/02 D4).
- **Accents look alike in luminance.** Pairs such as blue/purple (1.05) and teal/green (1.05) are almost indistinguishable by lightness (computed), so never distinguish two things by accent colour alone: add a label, a line pattern or a shape (ROOT/02 D4).
- One dominant highlight at a time. Dominant ink + paper, one subject accent, at most one condition/error accent per beat [N52].

## 5. Fonts

All fonts are vendored, hashed into the cache key and licence-checked before use (RD-23); no CDN at render time. Licences: verify per font.

| Role | Family (candidate) | Latin | Devanagari | Bengali-Assamese | Note |
|---|---|---|---|---|---|
| Labels, captions | Inter (Latin), Noto Sans family for scripts | yes | via Noto Sans Devanagari (verify) | via Noto Sans Bengali (verify ৰ ৱ) | RD-23 production fonts |
| Doodle titles, handwriting | Kalam | yes | yes (verify) | no verified font | Per-word wipe reveal for all scripts |
| Latin-only hand lettering | Caveat | yes | no | no | Hooks in English only |
| Formulae | KaTeX fonts | yes | n/a | n/a | Data-bound, from fixtures |

- **Allow:** the table above.
- **Ban as display or title:** Arial, Helvetica, Roboto, system-ui, Space Grotesk (the common convergence choice [N51][N55]), Inter (acceptable for labels and captions, banned as the hook headline face), Comic Sans, Papyrus.
- **Indic.** Per word or per grapheme cluster, never per code point (#55). See `kinetic-type.md` §8 and `paper-collage-vertical.md` §13 for the full rules and the end-state equality test.
- **Glyphs to test:** I/l/1, O/0, minus signs, decimal points, subscripts, superscripts and Greek letters (ROOT/02). A handwriting font never sets a number, unit or formula.

## 6. Layout in 1080×1920

Same stacked zones as the other styles (insets from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them; the assembler blocks the brief if the file is missing; while `platform_insets_px.measured` is false its `applies_until_measured` insets are used and the job manifest records them as provisional):

| Zone | Share of safe-box height | Holds |
|---|---:|---|
| Title | top 22% | hook words (1-3 words, 96-140 px), underline, "?" or "!" doodle |
| Visual | middle 54% | doodles, hero, props, fixture panels (placed by the data-bound skill), tags |
| Caption | bottom 24% | accessible caption track, 50-54 px, ink on an `#F7F9FC` plate, at most 2 lines |

- Side margin at least **96 px**, and inside the file's left/right insets if larger (#51).
- Text sizes (1080-wide, from RD-01/RD-18): essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; secondary non-essential floor 36-40 px.
- Layouts: (a) hero low-left looking up at the title; (b) a vertical "two columns" compare with a doodle divider (counters, scales); (c) a central prop with up to three tags; (d) a checklist column (one tick per spoken item).

## 7. Motion vocabulary

All timings are [Recommendation] starting values; simple transitions stay in the ROOT/02 150-300 ms range, highlights 300-600 ms.

| Move | Spec |
|---|---|
| Draw-on | stroke-dash, `power1.inOut`, `d = clamp(L/1100, 0.25, 1.2)` s |
| Fill-in | opacity 0 to 1 over 150-300 ms after outline completes, off-register |
| Pop | scale 0.6 to 1 with `back.out(1.7)` over 0.30-0.40 s, pivot at the base |
| Underline | one stroke, 0.30-0.40 s, wobble keyed by seed |
| Circle / tick (functional) | 0.40-0.50 s, 6-8 px stroke |
| Hatch-in shadow | 3-5 strokes staggered 40-60 ms |
| Nudge / wiggle | ±2°, 0.4 s, finite repeats (`ceil(DURATION / period)`) |
| Erase | reverse draw-on 0.25 s, or a scribble-out for a deliberate gag |
| Camera drift | slow pan as a function of `t`, at most 30 px, off during holds |
| Scene cut | hard cut or a 150-300 ms slide on a cue; no flashes (#56) |

- **Sync [Recommendation, from [V4-MP]].** A reveal lands on, or about 0.05 s before, its word; times come from `cues[].at` and `words[]` in the cue sheet, never hard-coded (#63). One sentence is one visual beat.
- **Never frozen, never infinite.** Decorative idle (a breathing wiggle) is allowed on hook, analogy and recap characters, with finite repeats, and is off during holds, `think` windows and the reduced-motion variant (ROOT/02 E3, #18).
- **Reduced motion.** Boil, idle, drift and wiggles off; strokes appear by fade.
- **No camera effects during label reveals** (#64).

## 8. Sound

- **SFX palette** (synthesised, seeded, by `examleaf-audio-compose`; gains placed from the cue sheet `sfx[]`): pencil scratch on draw-on (one per stroke group, not per stroke); soft tick for a tick-mark; pop; paper rustle for a scene cut; light whoosh for a slide; marker squeak for a circle; a soft chime only for a confirmed result and only under conditional narration ("if your result matches..."). Report §5.1 lists STEM-specific sounds (electric hum, bubbling, bond click) for later.
- **Silence rules.** No SFX during `think` or `pause-video`, equation reading or inspection.
- **Music.** Optional for a Reel and never needed to make the explanation work (REEL_BACKLOG rules; ROOT/02 G5); bed only in the hook and CTA, not under reasoning.
- **Loudness.** -16 LUFS integrated (±1), true peak at most -1 dBTP, measured after the final mux (#39).

## 9. Writing and hooks

**Ownership.** Scripts come from the Super Teacher system, never from the animation agent (#11). This section tells scriptwriters and brief assemblers what suits the style.

**Voice.** Super Teacher: warm toward the student, exacting about the science, playful about the problem; five delivery modes (curious, steady, deliberate, light, reassuring; RD-12 adds focused). Ordinary explanation 130-155 wpm; recap 145-165; dense 105-125. No fake enthusiasm; retired phrases ("mind blown", "super easy") stay out (ROOT/03). Humour: zero is acceptable; at most one light moment in a Reel [Hypothesis].

**Reel structure** (REEL_BACKLOG §4; `05_SHORTS_and_REELS_PROCEDURE.md` SH5; target 20-60 s per RD-19):

| Seconds | Purpose | Doodle's job |
|---|---|---|
| 0-3 | Identify the problem (hook) | Hook words with an underline; a "?" doodle |
| 3-8 | Invite a prediction or point out the tempting error | A doodle choice frame; default `think` = 6 s with the answer hidden (RD-11) |
| 8-30+ | Complete explanation | Handed to data-bound skills; doodle is the frame and transitions |
| Final seconds | One next action | CTA card with a tick-list doodle |

**Hooks that suit this style** (CSV ID in the tracker; hook text as in the backlog; every one still needs science review):

| CSV ID | Hook | Doodle role | Data-bound part (not doodled) |
|---|---|---|---|
| 30 | Chromosome count and DNA amount are different counters. | Two doodle "counters" side by side, values hidden as "?" | The 2n=4 stage-by-stage counts and labels |
| 1 | Does twice the voltage ALWAYS mean twice the current? | Tempting-shortcut doodle (a ×2 arrow with a "?") | The matched resistor cases and the condition label |
| 35 | It feels clear. Can you do the next one without the video? | A hidden-notes doodle; a "cover it up" gesture | The fresh question |
| 18 | This cancellation quietly deletes an answer. | A scribble-out gag on an eraser | The equation and the excluded case |
| 5 | The arithmetic is right. Why is the answer still wrong? | A magnifier circling a blank | The single wrong sign in the worked solution |

## 10. Mixed scenes (doodle plus fixture panel)

A scene that frames a fixture panel is a mixed scene. The panel is produced by the data-bound skill or inserted by fixture-driven code; the doodle draws a hand-drawn border, arrows that carry no scientific direction, and callouts that use text from the script. The panel is not wobbled, boiled or drifted, and every science glyph in it carries `data-fx="path.to.field"` (contract §9). Placement respects the safe box; the panel keeps its own axes and labels at the sizes in §6.

## 11. Do and don't

**Do**
- Draw the idea, then reveal the label on its word.
- Keep one attention target per beat and a stable layout; add motion only for a change in meaning (ROOT/02 E3).
- Use the depth rules in §3 in every scene.
- Hold a headline for at least 1.2 s [N60] (Indic longer), equations until narration ends plus 0.5 s and at least 2 s after an important transformation (RD-02).
- Leave an honest gap for the learner's prediction.

**Don't**
- Wobble, boil or drift anything a fixture owns (#64, #12).
- Animate Indic text per code point (#55).
- Use `Math.random`, `Date.now`, `setInterval`, `requestAnimationFrame` loops or infinite repeats (#15, #17, #18, #19).
- Add full-frame flashes (#56).
- Ask an image model for any element (#54).
- Mark a wrong answer with a red cross; correct by explanation (ROOT/02 I3).
- Use the red `#B42318` or amber `#9A5B00` as decoration.
- Put text outside the safe box or over the caption plate (#51).

## 12. Determinism

Same block as `paper-collage-vertical.md` §15: `window.DURATION`, `async window.seek(t)`, stateless keyed PRNG (`rnd(sceneId:elementId:step)`), boil step `floor(t × boil_fps)`, finite computed repeats, preloaded fonts, double-render frame-hash equality. `04_harness_contract/contract.md` is authoritative.

## 13. Cost

- **Credits: zero.** No image-model or MCP call is required or allowed in this style without a separate approval (#41, #42).
- **Tokens:** not measured. [Hypothesis] Scenes built from templates and skills land well below the [V1] from-scratch range; measure in the pilot and log with `examleaf-observability-cost`.
- **Render:** CPU only; no WebGL, no video decoders.

## 14. QA checklist (`examleaf-anim-qa`)

- [ ] 1080×1920, 30 fps; DURATION equals the cue sheet; lint zero errors; double-render frame hashes identical.
- [ ] Safe box respected; captions in the bottom zone only.
- [ ] Text contrast at least 4.5:1; graphics at least 3:1; adjacent accent pairs not relied on for meaning.
- [ ] Fixture text equals rendered text; nothing wobbles that a fixture owns.
- [ ] Depth rules 1-3 pass (layers, drift at most 30 px, overlap).
- [ ] Hold times met; no flash; reduced-motion variant renders.
- [ ] Loudness -16 LUFS ±1, true peak at most -1 dBTP after mux; no SFX in think windows.

## 15. Edge cases handled

#7 (digest + brief), #8 (palette and fonts named), #12 (§10), #17-#19 (§2, §7, §12), #41/#42 (§13), #49 (§6), #50 (§11), #51 (§6), #54 (§11), #55 (§5), #56 (§7), #60 (via brief), #63 (§7), #64 (§3, §7).

## 16. Changelog

- 1.0.0 (15 Oct 2026): first version.
