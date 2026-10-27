# Kit card: concept_intro doodle scenes (reference build phy-ohm-ci-01, Opus)

## 1. When to use / when not
Use for a 60-70 s vertical concept intro with one small diagram and a few fixture numbers. Not for plotted data or Indic text.

## 2. Default path + escape hatch
Default: copy `scenes/s01.html`; change only the `#title` headline groups, the L3 markup (`data-par="0"`) and the `scene-spec` JSON. Runtime, CSS and L0/L1/L2/L4 are identical in all scenes. Escape hatch: a new behaviour is one new `scene-spec` field handled in the runtime; never a hard-coded time.

## 3. Slot table
| Archetype | Fixed | Varies |
|---|---|---|
| Hook (s01) | headline + drawn "?" + underline | words `w:occ`; reveal map; `swaps` |
| Predict (s02) | hook end state; `think_plate` hold on last word | headline; drawn "?" by a fixture label |
| Compare (s03) | two cards, ×2 in a ≥150 px gap, boxed equation | rows, amber condition chip |
| Exception (s04) | same loop, swapped part, struck value | labels |
| Recap+outro (s05) | ticks, `disclosure.lines` | rows |

## 4. Rules a cheap model will skip unless told
1. On-screen text is only `data-fx` fixture fields or words looked up in the cue sheet by (beat, word, occurrence in beat). That includes "Pause. Predict." (spoken in b02) and the disclosure.
2. Spell numbers as words in `text` ("zero point two amperes"), digits only on screen from the fixture.
3. Put the beat's condition ("constant temperature") in the same beat as any claim that needs it (SQ-20).
4. Only reveal-cue targets start hidden; everything else shows from t = 0, so carry the previous scene's end state.
5. A value replaced in place must multiply its own reveal opacity by the fade (mistake 1).
6. Science glyphs never wobble or boil; only decoration boils (10 fps). L3 never drifts.
7. Think window: start after the last word's `t1`, freeze boil and drift, show no clock.
8. Amber only for a condition, blue for the subject accent, no red.

## 5. Pre-submit checklist
Lint, check and previews clean? Every frame opened? No empty first frame? Nothing touching an outline? Answer hidden in s02?

## 6. Decisions the guides did not make
- Headline face: Chalkboard SE (style bans system-ui for display; the contract says system stack). Numbers stay in the label stack.
- Headline 84 px: the style says hook 96-140 px with max 3 words, but 96 px wraps on 864 px.
- Boil 10 fps (style guide) over 8 fps (procedural-2d).
- Circuit wobble static, never boiled (labelled structure).
- Disclosure split over two lines because the cue-sheet words lose the ";".
- No captions drawn; assumed the lead's VTT.

## 7. Three mistakes caught in preview
1. s01: "V = 2 V" visible at t = 0 (swap fade overwrote reveal opacity).
2. s03: the ×2 chips were squeezed into an 84 px gap and touched both card outlines. I narrowed the cards to 340 px, which left a 164 px gap.
3. s01/s02/s04: the paper-coloured backings behind the resistor and cell showed as white blocks on the tinted board. Also, s05 opened on an empty board and the struck ×2 in s04 crowded the ammeter. I added a conductor doodle on "So" and moved the ×2.

## 8. Checks run (final, all clean; escalate on `E_TEXT_WORD_MISSING` or `W_CUE_NO_ELEMENT`)
`lint_seek_contract.js --level 1` (ok, 0/0, all five); `check_script.py` (841/1000 chars, ~68 s, OK); `preview_scene.py` per scene (exit 0, injected/injected, 0 errors); `compute.py` asserts pass.
