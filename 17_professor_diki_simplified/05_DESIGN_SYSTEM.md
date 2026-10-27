# 05 · Professor Diki Simplified: unified visual design system v2.0.1 (paper cut-out collage)

**Status (16 Oct 2026).** The code is in `design_system/`. This version follows founder decisions PD-19, PD-20 and PD-21 (`DECISIONS_PD.md`). Every video now uses the look of the biology Opus pilot, which the founder calls "Vox style". The v1.1.0 look (white panels on a pastel page) is withdrawn. v2.0.1 (same day) makes three changes: light bands only, no science hues in headline chips, and cell-level table reveals. The Ohm example builds clean: lint level 1 passes and the gates are empty. `qa_scene.py --samples 31` reports `PASS | purity 31/31 | errors 0 | blocking 0`. `brand_check.py` passes on the example. `preview_scene.py` renders 30 PNGs with 0 warnings. The chemistry and biology components were checked on scratch scenes: no errors and pure DOM. The change history is in `design_system/CHANGELOG.md`.

Reference look: `16_pilot_builds_2026-10-16/biology/opus/scenes/_src/` (`build_scenes.py`, `engine.js`) and the 1 fps frames in `audit/frames/biology/` (t005, t018, t036, t052).

## 1. Principles

1. **One house style for every subject.** The stage is a full-bleed torn-paper world: a paper sky with soft cloud washes, torn bands, paper grain, a vignette and four corner sparkles. Objects are cut-out stickers with a thick cream outline and a soft double shadow. Headlines are ransom-note word chips. Results and structure sit on taped paper sheets. Only the world's bands change with the subject.
2. **One scene, one board.** A short is one scene file and one cue sheet. The world and the hero object never reset. The picture is complete at frame 0. The end card is the final state of the same board.
3. **Brand at the start and the end only (PD-21).** The opening ident is a brand sticker over the complete board from frame 0, gone by 2.46 s. The end card carries the wordmark sticker. Lesson frames carry no brand mark, and there is no header.
4. **No "AI-generated" line, on screen or spoken (PD-20).** The end card is the brand line plus "Free lesson: <topic>". The AI declaration lives in the upload metadata. The build gate rejects the string anywhere in a scene.
5. **Colour means something, inside the collage palette.** Voltage is royal blue, current is teal, resistance and conditions are mustard, and a mismatch is brick and always comes with a shape (a strike line or `≠`). For atoms, H is cream, O orange, C charcoal and N violet. In biology, material is a green solid arrow and energy is a mustard dashed wave.
6. **Every glyph comes from the fixture** (`data-fx`), including the end-card lines.
7. **Small deterministic motion.** Verbs have fixed durations: pop 0.94 → 1, slide 24 px, chips and tape. There is no elastic, back, bounce or spring easing, and measured quantities never overshoot. Everything is driven by `seek(t)`: no CSS animation, no rAF, no clock and no unseeded randomness.
8. **Big and legible.** Labels ≥ 52 px, equations ≥ 72 px with true subscripts, chips at the 64 px headline size. At 1/3 scale on a 360 px phone a label is ≥ 17 px.

## 2. Palette, roles and measured contrast (`tokens.json`, ratios written by `tools/build_tokens.py`)

| Paint | Hex | Role |
|---|---|---|
| cream / paper / outline | `#F3ECDF` / `#FBF7EE` / `#FFFDF7` | page base / sheets / sticker and chip die-cut border |
| grid paper | `#F7F9FC` + rules `rgba(47,79,168,.22)` 20 px | grid chips, chemistry bench |
| ink / black | `#3A332C` / `#2B2622` | text, wires, sparkles / black chip, brand plaque |
| mustard / brick / teal / royal / navy | `#E0A73A` / `#D9483B` (chip `#C94236`) / `#2F7F7A` / `#2F4FA8` / `#1B2A4A` | chips and sticker bodies (navy only on the battery end); never a band |
| sky / soil / soil dark / grass / olive | `#A9C0E2` / `#B98F5E` / `#4A3016` / `#9DBB8E` / `#7C8A3C` | world bands, washes |
| tape | pink `rgba(241,169,160,.72)`, mustard `rgba(224,167,58,.62)`, teal `rgba(47,127,122,.45)` | washi strips (the reference alphas) |
| atoms | H `#FBF7EE`, O `#EE8A3C`, C `#3A332C`, N `#7B5CC0` | stickers; the letter is always drawn |

| Science role | Text (on paper / cream) | Chip / sticker fill | Notes |
|---|---|---|---|
| voltage | `#2F4FA8` 7.00 / 6.37 | royal chip, cream text 7.00 | battery sticker royal |
| current | `#2A736F` 5.20 / **4.73** | teal chip, `#FFFDF7` text 4.65 | ammeter ring teal |
| resistance = condition | `#86611F` 5.25 / 4.78 | mustard chip, black text 6.95 | darker text variant of mustard (mustard itself is 2.01 on cream) |
| mismatch | `#B83C30` 5.27 / 4.80 | brick chip `#C94236`, cream text **4.55** | always with a strike or `≠` |
| ink / muted | 11.62 / 10.58 · 5.80 / 5.28 | | |

**Lowest measured.** Text: brick chip 4.55, teal chip 4.65, current on cream 4.73. Graphics: ink line on the biology grass_dark band 3.29, material arrow on the grass tint 3.46, energy wave on cream 3.60. The build checks 121 ratios (ratios, band luminances and sparkle contrasts). **Bands must be light or mid-tone** (relative luminance ≥ 0.18, PD-17); dark is allowed only on small chips and the brand sticker. Band luminance: physics bench 0.31, trim 0.44, table 0.52; chemistry bench 0.95, lip 0.44, counter 0.41; biology grass 0.45, grass_dark 0.23, soil 0.31. Text is checked on paper, cream, grid and outline; chips fg on bg; atoms, the brand sticker and biology tints at ≥ 4.5. Ink strokes are checked on every board band, and colour strokes on paper, cream and outline, at ≥ 3. Colour strokes never touch a band directly: they ride on a cream outline (stickers, two-tone connectors, strike lines). Band ratios are recorded only, because text never sits on a band.

## 3. Worlds (`tokens.world.subjects`, built once in `ready()` from fixed seeds)

All three share the base: a cream page; the paper sky (sky washes plus cream clouds, displaced by a fixed-seed `feTurbulence`/`feDisplacementMap` wash); fractal paper grain at 0.5; a vignette; four ink sparkles (cream only if a band were dark; none is). Each band is a torn strip. Its top edge is a lane reference such as `diagram.y0+8`. The edge jitter is seeded at ±9 px every 24 px, with a cream fibre edge and a 3 px shadow.

| Subject | Bands (top → bottom) | Look |
|---|---|---|
| physics | **bench** kraft `#B98F5E` with wood grain under the board · **trim** mustard strip · **table**: light blueprint, sky `#A9C0E2` grid paper with cream rules, holding the result and card sheets | the circuit lies on a workbench; sheets sit on a light blueprint table |
| chemistry | **bench** grid paper with royal rules under the board · **lip** mustard · **counter** mid-tone teal `#7FB5AE`, speckled | lab-notebook bench; atoms are stickers on grid paper |
| biology | **grass** `#9DBB8E` and **grass_dark** `#7C8A3C` under the board · **soil** `#B98F5E` speckled | the reference: sky, torn grass, soil |

## 4. Chips, stickers, tape, sheets

- **Chips** (`D.chip`, `D.chipRow`, `.chip-<style>` in `tokens.css`). One word per chip, a 6 px cream border, the soft double shadow `0 9px 7px rgba(74,48,22,.30), 0 2px 1.5px rgba(0,0,0,.20)`, and a ±3° rotation plus ±4 px dy from the seeded PRNG by chip index. Headline chips cycle black/sans, mustard/Georgia, grid/Courier New, teal/Georgia and cream/sans, with a step coprime to the count. Brick (mismatch) and royal (voltage) are never headline chips, so each of them only ever carries its science meaning. Label chips take their colour from meaning (`chips.roles`).
- **Stickers** (`D.sticker`, SVG filters `#cut` and `#cut-sm`). The shape is dilated by 8 px (or 5 px) and flooded cream, with the two shadows. The physics parts, atoms, carbon token and heat rays are all stickers.
- **Brand sticker** (`D.brandSticker`). A black plaque with a cream outline and pink washi: "Professor Diki" in Georgia bold cream (14.0:1), "Simplified" in sans heavy mustard (6.95:1). It is drawn differently from the headline chips, so the brand never reads as part of the question.
- **Tape** (`.tape-pink|mustard|teal`): 110 × 32 px strips at −4…−6°, half over a sheet edge.
- **Sheets** (`.sheet`, `D.sheetEl`): cream paper with an 8 px die-cut outline, the shadow and two washi strips. They are used for the result lane, the card lane, the think plate, the chemistry formula and ledger, and the biology compartments (tinted sky, grass, butter and blush).
- **Fonts**, installed on this Mac only. The reference's `--font` stack listed "Noto Sans" first, but it rendered as **Kohinoor Devanagari** (the first installed family), so v2 names that font first. Chips mix it with **Georgia** and **Courier New** exactly as the reference tiles do. STIX Two Text covers ≠ × Ω. No remote fonts are used.

## 5. Lanes (x 96…960; usable y 250…1470, insets still placeholders)

```
y    0 ┌─────────────────────────────── paper sky ─┐
  136 │  [ Professor Diki Simplified ]  opening ident (frame 0 → gone by 2.46 s)
  250 │  [Does][current][always] [double?]   title lane: headline chips | think plate | end-card wordmark
  456 │~~~~~~~~~~~~~~ torn bench edge ~~~~~~~~~~~~~│
      │   BOARD: the hero lives here (world region) │ diagram lane (default 864 px = 0.45; carded 584 px = 0.304)
 1040 │~~~~~~~~~~ trim / table edge ~~~~~~~~~~~~~~~│
 1048 │ ▭ taped sheet: result / "Free lesson" chip  │ result lane
 1202 │ ▭ taped sheet: ONE card (table/def/points)  │ card lane (layout 'carded', PD-18)
 1470 │   table / soil band (nothing to read)       │
 1920 └─────────────────────────────────────────────┘
```

| Layout | title | diagram | result | card / caption |
|---|---|---|---|---|
| default | 250–450 | 456–1320 (0.45) | 1328–1470 | none |
| captioned | 250–450 | 456–1176 (0.375) | 1182–1326 | caption chip 1332–1470 |
| carded | 250–450 | 456–1040 (0.304) | 1048–1194 | card sheet 1202–1470 |

There is no lockup lane. The title lane takes the 48 px back, so two chip rows fit in 200 px. The ident (`lanes.ident`, y 136–240) is not a lane: it is an absolutely placed sticker above the title lane.

## 6. Motion verbs (`diki_runtime.js`; fixed durations; ease `out` = cubic out, `standard` = cubic in-out)

| Verb | s | Use | Notes |
|---|---|---|---|
| **Pop** (new) | 0.26 | a sticker, chip or sheet appears | opacity + scale 0.94 → 1; leaving reverses it |
| **Slide** (new) | 0.30 | something arrives from a side | opacity + 24 px travel |
| **Chips** (new) | 0.26 | a headline phrase | the whole phrase together, 30 ms stagger (≤ 40 ms), never word by word |
| **Tape** (new) | 0.20 | a washi strip appears on an element's top edge | opacity + scale |
| Reveal | 0.24 | appear in place | opacity only |
| Headline | 0.26 | title-lane ownership crossfade | headline, think plate, wordmark |
| Badge | 0.26 | a condition chip | Pop + one Emphasize |
| PreserveObject | none | declares the hero | `W_PERSIST_BROKEN` if hidden at any time, end card included |
| ChangeValue | 0.60 | a measured value changes | tween, fixed decimals, no overshoot |
| CompareStates / EquationTransform / RevealMismatch | 0.50 / 0.70 / 0.60 | the result sheet | term ids are identities |
| SwapPart | 0.70 | a part replaced in place | StateTable step |
| MapSymbol | 0.30 | symbol ↔ object | two-tone dashed link through the side gutter, plus halos |
| PauseForPrediction | think window | answer slot | dashed ink ring; nothing else moves |
| Emphasize | 0.32 | pointing | one halo bump behind the element (butter `#FFE08A` at 0.7); no scale, no wobble |
| StrikeThrough | 0.24 | a condition that no longer holds | brick line on a cream outline |
| TracePath / EndMotif / Card | 0.80 / 0.60 / 0.24 | a mechanism path / spare / card rows | Card rows appear whole |

`StateTable`, the time references (`cue:c04`, `beat:b03.start`, `think:b02.end`, `end`, plus offsets) and the one-owner-per-property rule are unchanged from v1.1.

## 7. Components (`mount(container, fixture, opts)` + `set(state)`; same public APIs as v1.1)

- **`physics_circuit.js`**: ink loop on the bench. A royal battery sticker (cream ± marks drawn as shapes), a mustard resistor capsule with colour bands, and a filament lamp in the same slot (glass, ink filament, butter glow, brick and mustard heat rays). The ammeter is a teal-ring sticker with the fixture "A". Every label is a chip: R and lamp labels are mustard above the top wire, the condition chip sits under the load, the I chip (teal) beside the ammeter, and the V chip (royal) left of the battery. These rows never touch in the 584 px carded lane. `set({v,i,load,heat,badge,badgeDim,fx})` is unchanged; `badgeDim` turns the chip to muted grid paper.
- **`chemistry_species.js`**: the formula on a taped sheet with true subscripts, every atom a `cut-sm` sticker, and the ledger on a taped sheet. Counts are derived from the coefficients and checked against the fixture.
- **`biology_tracer.js`**: compartments as tinted taped sheets (sky, grass, butter, blush) with name chips. The material arrows are two-tone and solid; the energy wave is two-tone and dashed, with a mustard label chip. The carbon token is the charcoal C sticker, and the scale note is a grid-blue chip.
- **`equation.js`**: the result sheet. Terms are role-coloured text; positions are SVG attributes.
- **`badge.js`**: badges are now label chips (condition, assumption, mismatch, result, scale), each mapped to a chip role.
- **`caption.js`**: a single paper chip per chunk. Outro beats are never captioned.
- **`card.js`**: the card sheet with tape. The API is unchanged (definition / points / table; `border` is accepted and ignored). Rows appear whole. The table draws ruled row slots, so a table that is still filling up is never an empty box. A table cell may carry its own `at` (`{fx, dec?, role?, at?}`); that cell appears whole on its reference inside a dashed empty slot. The Ohm table shows V and I from frame 0 and the V ÷ I cells at c09. The definition term is a black chip, and the points have black number discs.
- **Chrome** (runtime and base):
  - the world;
  - the opening ident (text from `tokens.brand.wordmark`, checked against the static markup, `E_BRAND` on mismatch);
  - headline chips from `meta.beats_text`, with the hook up at frame 0;
  - the think plate (a taped sheet with `display.ui.think_prompt`);
  - the end card.

  The end card triggers on the **last beat whose slot is `outro.brand` (v2) or `outro.disclosure` (v1 compatibility)**. That beat's text is never shown. It shows the wordmark sticker from `display.ui.endcard_line1` (must equal the brand, `E_BRAND`) in the title lane, and the black chip `display.ui.endcard_line2` ("Free lesson: <topic>", `W_ENDLINE` otherwise) on the result sheet.

## 8. Gates and QA

| Gate | Where | Fails on |
|---|---|---|
| Brand | `build_scene.py`, anywhere in the output | "ExamLeaf", "AI-generated" (case-insensitive) |
| Structural bans | `build_scene.py`, `tokens.gates.banned_patterns` | CSS `transition:` / `animation:` / `@keyframes`, `requestAnimationFrame`, `Date.now` / `new Date(`, `Math.random`, remote URLs and `@import`, elastic/back/bounce/spring easings, Unicode subscripts U+2080–209C |
| Seek lint | `lint_seek_contract.js --level 1` | contract violations |
| Tokens | `build_tokens.py` | contrast, type floors, lanes, ident ≤ 2.5 s, chip stagger ≤ 40 ms, verb ranges |
| Scene QA | `qa_scene.py` | any error; `W_FILL_LOW` (hero < 0.70), `W_DIAGRAM_SHARE`, `W_PERSIST_BROKEN`, `W_MOTION_IN_THINK`, `W_VERB_DURATION`, overflows, `W_END_CARD_SHORT` (< 1.5 s), `W_NO_HERO`, `W_CARD_*`, `W_LAYOUT`, **`W_WORLD_MISSING`** (no `#world` with ≥ 2 bands at t = 0), **`W_IDENT_MISSING`** (ident absent, not the brand, or not fully visible at t = 0), **`W_IDENT_LATE`** (still visible at 2.5 s); any seek-purity mismatch |

The A2 decoration ban list (washi, polaroid, ransom, grain, pencil, boil, wobble…) is gone; PD-19 reverses it. Wobble on science objects is still absent, because no verb produces it.

## 9. How a builder uses it

Read in this order: this file, `tokens.json`, `diki_scene_base.html`, `diki_scene.css`, `diki_runtime.js` (verb headers), the subject component, and `examples/ohm_demo/s01.src.html`.

1. Copy the base to `<video>/s01.src.html` and fix the relative paths. Set `subject` (this picks the world) and `card` or `captions`. In the SCENE BLOCK: mount the hero, call `D.hero` and `PreserveObject`, write the `StateTable`, then the equation `drive([...])`, then `MapSymbol` and `PauseForPrediction`. Optionally add `D.Pop`, `D.Slide` or `D.Tape` for supporting stickers.
2. In `script.json`, put one scene with every beat. The last beat is `outro.brand`, spoken "Professor Diki Simplified.". In the fixture: `display.ui.think_prompt`, `endcard_line1` = "Professor Diki Simplified", `endcard_line2` = "Free lesson: <topic>". No `display.ui.header`, no lesson code, no disclosure string.
3. `python3 tools/build_scene.py s01.src.html s01.html --fixture fixtures/fixture.json --script script.json --scene s01`
4. `$PY tools/qa_scene.py s01.html`, then `$PY …/16_pilot_builds_2026-10-16/tooling/preview_scene.py script.json s01 --times 0,0.5,0.97`. Open the PNGs for frame 0, the plate, the reveal, the exception, the transfer and the end card.

Scenes written against v1.1 need small edits: link `diki_scene.css`; use the new stage markup (`#world`, `#ident`, `#wordmark[data-fx]`, `#endline-wrap`); drop `#lane-lockup`; rename the outro slot.

## 10. Still missing

- Platform insets are still `measured:false`. The ident band (y 136–240) sits inside the placeholder top inset, so it may sit under platform UI for its 2.46 s.
- `brand/strings.json` still names `header_lockup.svg` as an asset; the file is now `opening_ident.svg`. The strings owner must update it. `DECISIONS_PD.md` was not edited.
- `demo/physics_v2` was built against v1.1 and will need the small edits above. It was not touched.
- Headline chips no longer use brick or royal. Teal and mustard are still in the cycle, so a headline word can sit on a current- or resistance-coloured chip without meaning it. A per-word role map would close this; it is not built.
- No pixel double-render hash test was run; only DOM purity was checked. The world uses static `feTurbulence` (the wash and the grain). The pilot notes saw ≤ 12-level pixel noise from turbulence under load; recheck before relying on frame hashes.
- The chemistry and biology components have no tuned example lesson yet. They were smoke-rendered only.
- The demo lamp current (0.32 A) is illustrative and must be sourced before release.
- Still to build: graph/axes, a ray-optics bench, a particle field and a units ledger.
