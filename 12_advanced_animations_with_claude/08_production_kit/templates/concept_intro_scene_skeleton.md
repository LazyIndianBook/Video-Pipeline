# concept_intro scene skeleton (Kit 0.1.0, 16 Oct 2026)

A written skeleton, not code. Every `scenes/sNN.html` of a `concept_intro` lesson contains everything below. Build it on `12_advanced_animations_with_claude/04_harness_contract/scene_template.html` (runtime, `DURATION`, `seek(t)`, `ready`, `__errors`, `__cueSource`, `__fixtureSource`). Sizes and zone shares come only from `04_harness_contract/vertical_safe_zones.tokens.json`; the tokens win over every other number here. Rules cited as `R-0nn` are in `../RESTRICTIONS.md`.

## 1. Per zone: what every scene must contain

| Zone (tokens share) | Must contain | Never contains |
|---|---|---|
| `top_title` (22 %) | The current beat's headline: ≤ 6 spoken words looked up as (beat, word, occurrence in beat), each word fading in (opacity only) on its `t0`, ≥ 59 px, style display face (R-008, R-009). The headline persists until the next beat's headline replaces it. Optional style mark (doodle underline and "?"; editorial halftone band behind it) | Any word the beat does not speak; numbers or formulas (those go in middle_visual from the fixture) |
| `middle_visual` (54 %) | Layers L0-L4 of the style (§2). L3 holds the hero: the setup, panel, tally or checklist, every glyph bound with `data-fx`. Ink on screen from the scene's first word to its last (R-001); the previous scene's end state carried over until the first reveal of this scene | An empty container (R-017); a wrapped equation (R-018); any typed number, unit or label (R-014) |
| `bottom_caption` (24 %) | s02: the `think_plate` (`display.ui.think_prompt`) during `meta.think_windows[]`. s05: the end-card lines (`display.ui.endcard_line1/2`, PD-13: brand line and "Free lesson: <topic>"; no disclosure line, PD-20). Otherwise reserved for the lead's captions | A clock, countdown, answer, or promotional text |
| Side margins | ≥ 96 px clear of anything a learner must read; band width 864 px at current insets | Chips or cards bleeding past the margin |

Per-scene runtime obligations (all scenes): reveals and swaps are opacity-only on text and fixture elements; no `transform`, `scale`, `translate` or CSS `transition` on them (R-012); boil and camera drift, if any, apply to decoration only and freeze in think windows and holds; minimum hold 1.2 s per idea; seeded PRNG only.

## 2. Mandatory layers per style

| Layer | `doodle-handdrawn` | `editorial-vox` | `paper-collage-vertical` |
|---|---|---|---|
| L0 background | paper `#F7F9FC` with static seeded grain (a cached static layer, not a per-frame `feTurbulence`) | `#F7F9FC` with static grain (multiply 3-5 %) | full-frame paper background (sky or board) |
| L1 far | **shelf** (books, window) at 18 % accent tint, 0.6× line weight | **halftone dot band** behind top_title only | back layer: sky or board torn strip |
| L2 mid | **tinted wobbly board** (28 % tint) with a **3-5 stroke 45° hatch shadow** | **tinted panel card** (18 % accent) with a **flat 8/8 hard shadow** at ink 18 %, no blur | middle layer: torn strips and props with paper shadow |
| L3 subject | fixture panel flat on the board; never wobbled, boiled or drifted | fixture card content; keylined cut-out molecules or objects (6 px white keyline) | hero cutout plus the fixture sheet; sheet never under art |
| L4 frame | **pencil cropped by the left frame edge** (1.2× line weight) | (none required) | foreground strip (grass mound, leaf) cropped by the frame |
| Headline face | **hand-lettered**: Kalam or Caveat when vendored; pilot fallback Chalkboard SE; never Inter or system-ui | **serif claim words** (Noto Serif; pilot fallback Georgia with lining figures) + sans connecting words | word strips or ransom tiles (Latin) on paper squares |
| Science text | label stack (Inter/Noto Sans), never the handwriting face | Noto Sans or Inter, tabular figures; formulas from `parts[]` with true subscripts (R-006) | label stack on `#F7F9FC` tags |

Tag every layer root with `data-layer="L0".."L4"` so PK-D08 can find it. A scene missing a mandatory layer fails the style check (R-009). Fonts are not vendored yet (`05_style_guides/README.md` §12): the fallbacks above are pilot-only.

## 3. Cue-naming convention

- **Element ids:** lowercase snake case `<role>_<thing>`, stable across scenes so a later scene can reuse an earlier setup:
  - setup parts by noun: `resistor`, `ammeter`, `bulb`, `f_H2`, `f_H2O`, `mol_O2`
  - values and chips: `v1_chip`, `col1_i`, `r_chip`
  - relations: `rel_*`, `ratio_v`, `ratio_i`; condition: `cond_chip`; equation box: `equation`
  - chemistry: `coef_<species>`, `row_<Element>`, `tally_left`, `tally_right`
  - confront: `swap_*` (the swapped part), `chg_*` (change glyph), `strike_*` (struck shortcut), `name_*`
  - recap: `row1..rowN`, `tick1..tickN`; UI: `think_plate`, `disclosure`; headline words `hl_*`; containers `setup`, `card_*`
- **Anchor words:** the first word in the beat that names the thing being revealed ("resistor" → `resistor`; "temperature" → `cond_chip`; "rises" → `chg_r`; "doubles" → `strike_x2`; "two" of "two in front of water" → `coef_H2O`). `occurrence` counts that exact surface form within the beat only ("four" and "Four" are different forms; COMPARISON L-04).
- **Lead:** every reveal cue has `lead_s: 0.05`, so `at = t0 − 0.05`; the validator rejects later and warns above 0.10 s early. Emphasis cues use the same anchor rule; a hold cue runs to `until`.
- **First cue** of each beat lands on its first content word; if that word is more than 1 s into the beat, the previous panel stays on screen until then (R-001).

## 4. The state table rule

Every fixture state the narration mentions is a named fixture field that the scene binds; the scene never computes, types or interpolates a state.

1. List the states the script speaks before writing scenes, e.g. physics `reading_v1`, `reading_v2`, `filament_hot`; chemistry `unbalanced`, `step1`, `balanced`; biology `reactants`, `products`.
2. `compute.py` emits each state under `display.<kind>.<state>` (strings) and `results.<state>` (numbers), with an `assert` per spoken value. Example (chemistry/opus fixture): `display.coefficients.step1.H2O = "2"`, `display.counts.step1.right.O = "2"`.
3. Every state-bearing element carries `data-state` and reads its text from `data-fx="display.counts.<state>…"`; a scene spec `states: {cue_id: state_key}` switches all of them on the same cue (R-004, R-005, R-015).
4. A relation mark (`=` teal, `≠` amber), a "short" highlight and the headline are state-bearing too; they switch with the tally.
5. During the predict window no state that answers the question is visible (R-007, R-016).
