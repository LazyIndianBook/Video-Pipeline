# phy-ohm-pd-03 storyboard: "What is Ohm's law?" as a story that teaches (`explainer_60`, PD-24, PD-25)

## Format

- One scene and one persistent sticker circuit.
- Design system v2.0.1 collage, carded layout.
- Brand only on the opening ident (from frame 0 until 2.46 s) and the end card.
- No questions to the learner, no think windows.
- One sustained metaphor: voltage **pushes**, current **flows**, resistance **holds back** (the "hold-back").

Planned at `rate_scale` 0.82, with measured `target_wpm` on b02, b04, b08 and b12: **60.13 s**, silence 8.1 %.

## Script and planned start (s)

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

## State table

| Beat · anchor (cue) | Verb | Board | Result sheet | Card sheet | Title chips |
|---|---|---|---|---|---|
| frame 0 | PreserveObject | complete loop: 10 Ω, V = 2 V, I = 0.20 A | V = 2 V / I = 0.20 A | table head + ruled empty slots | ident + "What is Ohm's law?" |
| b01 "cells" c01, "rule" c02 | Emphasize | halos on the cell, then the ammeter | = | = | = |
| b02 first word | Card | = | = | **definition** "Ohm's law" / "I is proportional to V, at constant temperature." (formal wording on the card) | = |
| b02 "pushes" c03, "holds" c04, "flows" c05 | MapSymbol ×2, flow | V chip → battery; R chip → resistor; on "flows" the **current dashes** start, round the loop from + to −, narrowing beside the resistor, at the 0.20 A speed | = | definition | = |
| b03 "pace" c06, "constant" c07 | Emphasize, Badge | halo on I; the condition chip pops in | = | = | "The flow keeps pace" |
| b04 "Two" c08, "ten" c09, "reads" c10 | Emphasize, Card | halos on V, R, I | halo on 0.20 A | **table** row 1: 2, 0.20 | = |
| b05 "four" c11, "climbs" c12 (payoff) | ChangeValue, CompareStates, Card | V → 4 V; I → 0.40 A; **dashes double their speed** | 2 V \| 4 V, then 0.20 A \| 0.40 A | row 2: 4, 0.40 | "Double the push" |
| b05 "point" c13, "four" c14 | CompareStates | = | × 2 on V, then on I | = | = |
| b06 "equals" c15, "resistance" c16, "hold-back" c17, "ten" c18 | EquationTransform, MapSymbol, Emphasize, Card | halo on the resistor | V = I × R, with R linked to the resistor | V ÷ I cells 10, 10 + halos | "Voltage equals current times resistance" |
| b07 "always" c19, "bulb" c20 (the twist) | Emphasize, SwapPart | halo on the condition chip; resistor → filament lamp in the same slot; I → ? | = | = | "Does it always double?" |
| b08 "heats" c21, "rises" c22, "flow" c23, "short" c24 | SwapPart, StrikeThrough, Pop, RevealMismatch | heat rays and glow; the condition chip **struck**; "R ↑"; **dashes slow** (qualitative) | V × 2 / I **× 2** in brick, struck | = | "Resistance rises" |
| b09 "resistor" c25, "six" c26, "lands" c27, "six" c28 (pay-off scene) | SwapPart, ChangeValue, EquationTransform, Card | lamp → resistor, I 0.40 A; V → 6 V; I → 0.60 A; **dashes three times the 2 V speed** | 6 V ÷ 10 Ω = 0.60 A | row 3: 6, 0.60, 10 | "Back to the resistor" |
| b10 "Twice" c29 (the moral) | Card, CompareStates | = | × 2 grid again | **points** 1–3 (+0.5 s each), kept on the end card | "Twice the push, twice the flow" |
| b11 "free" c31 / b12 "Professor" c32 | runtime end card | final state; dashes still flowing | "Free lesson: Ohm's law" chip | points | wordmark sticker |

## Motion

- The current dashes move from b02 "flows" to the end. Their speed is `display.flow.px_per_a` × the meter reading.
- The hot filament runs at `display.flow.lamp_factor` 0.7 × the 4 V speed. This is a qualitative picture, never a value.
- The motion is integrated from piecewise-linear keyframes, so it is seek-pure.
- During speech nothing is still for longer than 3 s.

**17 Oct, after render:** on b08b "cool" (c24b) the lamp swaps back to the resistor, the condition chip is restored (strike ends) and the dashes return to the 4 V speed; halos on "steady" (condition chip, `beat:b08.end-0.9`) and "holds" (ammeter, `beat:b08b.end-0.6`); b09 changes only V → 6 V and I → 0.60 A, with a halo on the resistor at c25.
