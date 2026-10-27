# Build notes: phy-ohm-pd-03, "What is Ohm's law?" explainer (`explainer_60`, PD-24)

Built 17 Oct 2026 from `demo/physics_v2` (design system v2.0.1). It has not been narrated or rendered.

## What changed from physics_v2 (PD-24: shorts are complete explainers)

**Structure.**
- No prediction, no think windows, no transfer question. Those move to the free lesson.
- The spine: hook "What is Ohm's law?" → definition (plain words plus the push/flow picture) → mechanism (2 V gives 0.20 A, 4 V gives 0.40 A) → formal (V = I × R, with R explained) → condition ("When does it hold?" and the hot filament) → one worked example shown (6 V gives 0.60 A) → recap (the claim line plus three points) → `cta_line` → brand line.

**Science (unchanged).**
- 10 Ω; 2, 4 and 6 V give 0.20, 0.40 and 0.60 A; V ÷ I = 10 Ω at every point.
- The filament case stays qualitative (`lamp.current_doubles: false`). No lamp number exists anywhere.

**Lesson graph.**
- New nodes `WRK-ohm-six-volts` and `SIM-flow-speed`, each with its `what_is_lost`.
- The assessment items were removed.

**Fixture.**
- The definition text is "I is proportional to V, at constant temperature."
  - The full sentence overflowed the card.
  - "∝" rendered as a tiny fallback glyph.
- New `display.flow` block for the dash speeds.
- The prompt and option strings were removed.

**Scene.**
- Option chips, think plate and focus rings removed.
- The definition card is shown from the definition's first word.
- The table fills as the board produces each reading.
- The points card appears at the recap and stays on the end card.
- New mechanism animation: current dashes whose speed tracks the meter (1×, 2×, 3×), which narrow at the resistor and slow in the hot filament.

## Story rewrite (PD-25, "a better storyteller, not just a boring teacher")

**The story.**
- It opens on a scene every student knows (old cells, dim torch) and then names the law as the rule behind it.
- One sustained metaphor runs throughout: voltage **pushes**, current **flows**, resistance **holds back** (the "hold-back").
- The mechanism is narrated as action: "Double the push… the meter climbs".
- The condition is the twist: "So does it always double? Watch a bulb." It resolves on the resistor: "the meter lands on point six".
- The moral is the claim line.
- Lecture openers are gone. The formal wording lives on the definition card.

**New graph node.** `CTX-torch-cells`: run-down cells give less voltage, so less current flows. It claims the direction only, because the torch bulb is a filament. It needs subject review.

## Budget

| Measure | Value | Cap |
|---|---|---|
| Words | 104 | ≤ 105 |
| Spoken characters | 601 | — |
| Spoken characters incl. tags | 625 | ≤ 640 |
| Beats | 12 | 10–12 |
| Planned duration (`rate_scale` 0.82) | 60.13 s | 60 ± 1 s |
| Planned silence | 8.1 % | ≤ 10 % |

- Pauses are join, land and inspect only.
- Measured `target_wpm`, taken from the final v2 narration (PD-22), is set on b02 (identical line, 97 wpm), b04 (118), b08 (119) and b12 (identical, 87).

## Beats

| Beat | Slot | Tag | Text | Planned start–end (s) |
|---|---|---|---|---|
| b01 | hook.question_reveal | [curious] | Old cells, dim torch. What is Ohm's law? The rule behind that. | 0.30- |
| b02 | explain.definition (insight) |  | Voltage pushes, resistance holds back, current flows. | 6.04- |
| b03 | explain.definition |  | The flow keeps pace with the push, at constant temperature. | 10.62- |
| b04 | explain.mechanism |  | Two volts, ten ohms: the meter reads point two. | 16.50- |
| b05 | explain.mechanism (payoff) |  | Double the push: four volts. The meter climbs to point four. | 21.57- |
| b06 | explain.formal | [calm] | Voltage equals current times resistance; the hold-back stays ten ohms. | 27.20- |
| b07 | explain.condition |  | So does it always double? Watch a bulb. | 33.83- |
| b08 | explain.condition |  | Its filament heats, resistance rises: the flow falls short. | 38.26- |
| b09 | worked.step |  | Back to the resistor: six volts, the meter lands on point six. | 43.30- |
| b10 | recap.statement |  | Twice the push, twice the flow. | 49.86- |
| b11 | close.next_step | [calm] | Try the free lesson on Ohm's law. | 53.49- |
| b12 | outro.brand |  | Professor Diki Simplified. | 57.16- |

## Frames inspected

000.00, 005.00, 012.00, 020.00, 030.00, 040.00, 048.00, 058.00.

Fixed after looking:
- The definition card overflowed (W_CARD_OVERFLOW), and the "∝" glyph rendered too small. Both were fixed by the shorter definition text.
- After the story rewrite, the R → resistor link lingered into the mechanism beat. It now ends on "pace".

## Open for review

1. **New nodes.** `SIM-flow-speed` (the dash speed is a picture, not the drift speed) and `WRK-ohm-six-volts` need academic sign-off, as does `CLM-filament` (reliability note).
2. **Lamp slowdown.** The lamp's 0.7× dash speed is a visual "less than double", not a value. Confirm it is acceptable under PD-16.
3. **Hook beat length.** `check_script` warns that the hook *beat* ends at 5.3 s. The question itself ends at about 1.8 s, and the promise follows in the same beat by design.
4. **Format warning.** `check_script` also warns "no misconception.confront beat". The bounded exception sits in `explain.condition` per the `explainer_60` spine.
5. **Pronunciation.** "R" in b06 is spoken as a letter. Confirm the voice says "R" and not "are".

6. **check_pd_script.py.**
   - `references/banned_phrases.txt` gained six un-tabbed lines on 17 Oct 00:10 ("states that", "is defined as", …), so the checker crashes on load.
   - A scratch copy with those six lines formatted as block rules shows that this script contains none of them.
   - The same copy fails two rules:
     - "payoff_beat must be on reveal.answer": the explainer slots are not handled yet.
     - SQ-41 "hook question ends ≤ 3.0 s": the PD-25 scene-first opening puts the question at 3.3 s unscaled, about 4 s at 0.82.
   - The lead should decide whether SQ-41 applies to `explainer_60`. If it does, swap the hook to "What is Ohm's law? The rule behind a dim torch." (question first).
7. **CTX-torch-cells** needs review.

## After the final render: b08 / b08b stillness (QA A15, 17 Oct 2026)

**What QA found.** The narrated script split b08 and added b08b ("Keep it cool, and the rule holds.", cue c24b). With the board unchanged, the screen sat still for 6.5 s from 37.5 s.

**Fix (scene only; no script or cue-sheet change).** On "cool" (c24b, 41.6 s in the narrated cue sheet):
- the lamp swaps back to the resistor in place;
- heat and "R ↑" go;
- the condition chip's strike ends and its dimming returns to 0;
- the result sheet returns to V = I × R;
- the current dashes ramp back to the 4 V speed.

b09 now only changes V to 6 V and I to 0.60 A on its existing cues. A halo on the resistor marks "Back to the resistor" (c25).

**Words with no cue.** "steady" and "holds" have no cue, and the cached cue sheet is fixed. Their halos are timed from beat ends:

| Word | Reference | Target | Narrated time |
|---|---|---|---|
| "steady" | `beat:b08.end-0.9` | condition chip | 39.79 s |
| "holds" | `beat:b08b.end-0.6` | ammeter | 43.15 s |

The changes now land at 37.5, 39.8, 41.6, 43.1 and 44.5 s, so no gap exceeds 3 s.

**Frames inspected:** 038.00, 041.00, 043.00, 045.00 (synthetic timing).

**Checks:**
- `build_scene.py`: lint ok, gates `[]`.
- `preview_scene.py`: exit 0, 0 blocking.
- `qa_scene.py`: PASS, purity 9/9.
- `brand_check.py`: pass.
- `check_script.py`: OK.
