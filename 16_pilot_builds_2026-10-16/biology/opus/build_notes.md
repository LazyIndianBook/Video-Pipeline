# Kit card: concept_intro, paper-collage-vertical (bio-photosyn-ci-01, reference tier)

## 1. When to use / when not
60–70 s vertical intro, one equation, one misconception. Not for graphs or Indic headlines.

## 2. Default path + escape hatch
Edit `script.json`, `compute.py`, art in `scenes/_src/build_scenes.py`; run it (inlines `engine.js`, takes headlines and disclosure from the script). Escape hatch: hand-edit one `sNN.html`, then copy the change back into `_src`.

## 3. Slot table (scene archetypes)
| Archetype | Varies | Fixed |
|---|---|---|
| Hook prop (s01) | hero cutout, scale prop, doodle | push-in ≤ 1.03 on the art box only, no fixture text |
| Predict board (s02) | 3 option cards (pictures, no text), headline words | answer hidden, `pause_chip` hold cue on "predict", boil frozen from that cue |
| Equation build (s03) | illustration props, pieces | sheet follows its first piece (`data-follow`), pieces fade 250 ms opacity-only, no camera |
| Misconception (s04) | two columns, data pie | pie wedge drawn from `results.carbon_mass_fraction`, no red cross |
| Recap + outro (s05) | hero, full equation | disclosure = approved b07 text, verified word by word against the cue sheet |

## 4. Rules a cheap model will skip unless told
1. Run `compute.py` before speaking numbers: the brief's O 24/24 is wrong (18/18).
2. No unfixtured number in the hook ("fifty" became "a herd"); draw one elephant, not a countable row.
3. Cut "not mainly from the soil" from the hook: it leaks the predict answer.
4. Don't claim "most dry mass is carbon": the fixture says 40 % of glucose.
5. Headline = in-order subsequence of spoken words. Speak "Pause and predict" so the chip is legal.
6. Band width is 864 px (right inset 120), not 888.
7. Fixture-text tags: opacity-only fades, integer pixel positions.
8. Art must not hide under science panels; no `feTurbulence` in cutout filters.

## 5. Pre-submit checklist
Lint ok ×5 · check_script OK · preview exit 0 ×5, cueSource injected · engine `layoutCheck` silent (outside-zone, overlap, size) · PNGs opened · DOM determinism script passes.

## 6. Reading validator errors
`W_TEXT_OVERLAP`: raise the tile row gap. `W_ELEMENT_NO_CUE`: id missing from script cues. `E_TEXT_NOT_SPOKEN`: approved text not in the sheet.

## 7. Verification (exact commands, from `16_pilot_builds_2026-10-16/`)
- `node ../12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js --level 1 biology/opus/scenes/sNN.html`
- `$PY tooling/check_script.py biology/opus/script.json`
- `$PY tooling/preview_scene.py biology/opus/script.json sNN`
- DOM-state purity across seek orders (scratch Playwright script).

## 8. Three mistakes caught in preview
1. s03: the roots and soil sat under the equation sheet, and later under the chlorophyll tag. The layout was rebuilt: illustration 0–300, sheet 318–656.
2. s05: the recap tree floated in the sky. Added a grass mound.
3. Headline tile rows overlapped (rotation plus jitter); the engine's `layoutCheck` flagged it. Also fixed: muddy grey sky wash, crowded s04 column, bad disclosure line break.

## 9. Guide gaps (escalate)
- Boil rate: brief/template say 8 fps, style guide §8.4 says 10. I used 8.
- Text size: the task said headline ≥ 56 px and labels ≥ 44 px; tokens say 59/50/63. I used tokens (70/54/72).
- Style guide §5.1 says 888 px between margins; tokens give 864.
- Contract §3 "nothing else on screen" conflicts with the mandated "Pause. Predict." and the style guide's caption track (I burned in no captions).
- Cue-sheet words drop punctuation, so the disclosure can't be shown verbatim from words alone.
- No guide owns scene-to-scene paper-sheet transitions (s0N files are hard cuts).
- Pixel hashes from two seek orders differed by ≤ 12 levels under machine load, even though DOM state is pure. Removing `feTurbulence` from the cutout filter reduced it. Recheck on a quiet machine.
