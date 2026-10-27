# Kit card: concept_intro, chemistry equation scenes (editorial-vox) (Opus reference)

## 1. When to use / when not
Use for a 60–70 s `concept_intro` where the science is counts read from formulas (balancing, atom conservation). 

## 2. Default path + escape hatch
Default: edit `scenes/_build/sNN.part.html`, run `python3 scenes/_build/build.py` (pastes `core.html` = template runtime + chemistry helpers; inlines fallbacks). Escape hatch: edit a built `sNN.html`'s `[SCENE]` block.

## 3. Slot table
| Archetype | Fixed | Varies |
|---|---|---|
| Equation reveal (s01, s02) | card 72/584/936×150; `CELLS` [212,92,190,100,270]; molecules at y 950, scale 1.75 | equation key, coefficient state, which ids get a reveal |
| Tally (s03) | rows H/O at y 790/960; circles + numeral + relation from `results.<state>` | states list; which cue ids switch the state |
| A-vs-B (s04) | two 290 px frames, a divider at 858 | species keys, number of copies, highlighted part |
| Recap + outro (s05) | chips at y 1046; disclosure in caption zone, 2 lines | headline words |

## 4. Rules a cheap model will skip unless told
1. Headline = `[word, occurrence, isClaim]` looked up in the cue sheet **within its beat** (`sheet.beats`). Text comes from the sheet, never typed. Pick early words or the title stays empty.
2. Formulas are built from `display.species.<key>.parts[i].symbol/sub` spans, and coefficients from `display.coefficients.<state>.<key>`. Never type "H₂O".
3. Molecule atoms, tally circles and copies come from `parameters.species` and `results` counts (a circle count is data).
4. A state switch (unbalanced → step1 → balanced) is keyed on a **reveal cue's `at`**, never on seconds.
5. During the predict window show no counts anywhere, not even in the hook.
6. "Pause. Predict." is `display.ui.think_prompt` and starts at the last word's `t1`.
7. Highlighter swipes on HTML use `clip-path`. `scaleX` on a group moves its children.
8. Measure positions (`relBox`) in `afterLayout()`, after fonts load and `data-fx` is filled.
9. Hide containers until their first content reveals (no empty card).
10. One highlight at a time; ≠ in amber, = in teal; no red cross.

## 5. Pre-submit checklist
Lint ok ×5? check_script OK? preview exit 0, both sources `injected`? All glyphs `data-fx`? Labels ≥50, equations ≥63 px? PNGs opened?

## 6. Reading validator errors
`E_WORD_MISSING` headline word/occurrence not in that beat; `W_REVEAL_MISSING` `data-reveal` element without a cue; `E_CUES_INVALID` (s03) missing coefficient reveal.

## 7. Verification (exact commands run)
`node 12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js --level 1 …/scenes/s0N.html` (all `"ok": true`); `$PY tooling/check_script.py chemistry/opus/script.json` → `chars 790/1000 | words 145 | estimated 69 s` `OK`; `$PY tooling/preview_scene.py chemistry/opus/script.json s0N` → errors 0, blocking 0, exit 0 (×5). Two preview iterations.

## 8. Escalate when
Brackets/charges in a formula, or a non-H₂/O₂/H₂O/H₂O₂ shape (`E_LAYOUT`).

## 9. Three mistakes caught in preview
1. s05: the coefficient highlighters sat about 80 px left of the coefficients mid-swipe, because `scaleX` on the parent moved the rects. Fixed with `clip-path`.
2. s04: "hydrogen peroxide" wrapped onto 2 lines, spilled out of frame A and crossed the divider. Fixed with nowrap.
3. s01: the card was empty for about 4 s before the first formula, and the molecules were too small (the H₂O₂ drawing hid its H atoms). Fixed by hiding the card until the first formula, scaling the molecules up and pushing the H atoms out.

## 10. Decisions the guides did not make
UI strings in the fixture (`display.ui`). Disclosure punctuation is lost in the cue-sheet words, so it is shown as two lines. Headline only on the first beat of a scene ("one headline per scene"). Georgia stands in for Noto Serif. No captions (the lead owns those).
