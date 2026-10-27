# phy-ohm-pd-02 storyboard: one board, hook to end card (design system v2.0.1, paper cut-out collage)

One scene (`scenes/s01.html`, PD-03), layout `carded` (PD-18):

| Lane | y (px) | What it holds |
|---|---|---|
| title | 250–450 | headline chips, think plate, end-card wordmark |
| diagram | 456–1040 | the sticker circuit on the kraft bench; it fills 0.82 of the lane |
| result | 1048–1194 | the result sheet |
| card | 1202–1470 | the card sheet: one card at a time |

- **World:** the physics world (sky paper, kraft bench, mustard trim, blueprint table).
- **Brand (PD-21):** the opening ident (from frame 0 until 2.46 s) and the end card. Nothing else is brand-shaped.
- **No disclosure line (PD-20).**
- **Times** are planned (`pilotlib.plan`, lead-in 0.3 s). Real times come from the narration timeline. Cue ids match `script.json`.

## State table

| t (s) | Beat · anchor | Verb | Board (circuit) | Result sheet | Card sheet | Title lane (chips) |
|---|---|---|---|---|---|---|
| 0.0 | frame 0 | PreserveObject, Card | complete loop: R = 10 Ω, V = 2 V, I = 0.20 A | `A`: V = 2 V / I = 0.20 A | **table** V \| I \| V ÷ I: row 1 = 2, 0.20, ruled empty ratio slot; rows 2–3 are empty ruled slots | ident "Professor Diki Simplified" over "Does current always double?" |
| 0.3–2.9 | b01 · "voltage", "current" | Emphasize | halos on V and I | = | = | ident pops out by 2.46 s |
| 3.7–6.9 (re-timed) | b02 · c03 "pushes" | MapSymbol | dashed voltage-blue link from the V chip to the battery sticker (until "flows") | = | = | = |
| | b02 · c04 "resistance" | MapSymbol | dashed amber link from the R chip to the resistor (until c06) | = | = | = |
| | b02 · c05 "flows" | TracePath, Pop | two-tone current-colour trace runs ON the wire from the + terminal → ammeter → resistor → back to − (0.8 s, breaks at each sticker); an arrowhead into the − terminal; both hold until "four" (c10) and are gone before the window | = | = | = |
| 6.9–9.7 (re-timed) | b03 · c07 "Two", c08 "ten", c09 "amperes" (`insight_beat`) | Emphasize (pad 24, 0.35 s) | a clear butter halo on the V chip, then the R chip, then the I chip | halo on 0.20 A | halo on the table's I cell (pad 18) | = |
| 10.2 | b04 · c10 "four" | ChangeValue, CompareStates, Card | V 2 → 4 V; I → "?" | `ABq`: 2 V \| 4 V / 0.20 A \| ? | row 2 V cell "4" | = |
| ~12.0 / 13.0 / 14.5 | b04 · c42 "More", c43 "less", c12 "same" | EquationTransform, Pop | V = 4 V, I = ? | the 2 V \| 4 V grid steps aside; three option chips "more", "less", "same" land one per word (fixture `display.ui.options`) | row 2: V 4, I slot empty | hook chips |
| 15.0–17.0 (2.0 s) | b04 think_choice | PauseForPrediction | dashed ring on "I = ? A"; nothing else moves | the three chips, still | = | taped plate "More, less or same?" |
| ~17.0 | b05 start "More" | Pop, Emphasize | = | tick chip on "more" + halo; "less" and "same" fade | = | hook chips |
| 16.6 | b05 · c13 "four" (`payoff_beat`) | ChangeValue, CompareStates, Card | I → 0.40 A | `AB` | row 2 I cell "0.40" | = |
| ~17.8 | b05 · "Twice" | Chips | = | = | = | **claim chips "Twice the push, twice the flow"** (to ~27.3 s) |
| ~18.3 / 19.4 | c15 "push", c16 "flow" | CompareStates | = | × 2 on the V row, then on the I row | = | = |
| 24.6 | b07 · c20 "over" | EquationTransform, Card | = | `ratio`: 2 V ÷ 0.20 A = 10 Ω / 4 V ÷ 0.40 A = 10 Ω | V ÷ I cells "10", "10" (first computed here) | = |
| ~26.1 / 26.6 | b07 · c21 "ten", c22 "ohms" | Emphasize (pad 24 / 16) | halo on the R chip | halo on 10 Ω | halos on both V ÷ I cells | = |
| ~27.3 | b07 · c23 "Ohm's" | Card, Chips | = | = | **definition** "Ohm's law" / "V = I × R, at constant temperature." | "Ohm's law" |
| ~29.0 / 30.2 | c24 "equals", c25 "resistance" | EquationTransform, MapSymbol | resistor halo, dashed link to R | `named`: V = I × R | definition | = |
| 31.4 / ~32.4 | b08 · "Always", c27 "constant" | Chips, Badge | the "constant temperature" chip pops into the loop | V = I × R | definition | "Always?" |
| 33.9 | b09 · c28 "bulb" | SwapPart | resistor → filament lamp in the same slot; I → "?" (no lamp number, PD-16) | = | definition | = |
| ~35.6 | c29 "heats" | SwapPart | heat rays and glow; the condition chip dims | = | = | "Resistance rises" (on "resistance") |
| ~36.9 | c30 "rises" | Pop | "R ↑" chip beside the lamp label | = | = | = |
| ~38.0 / 38.8 | c31 "current", c32 "double" | RevealMismatch, StrikeThrough | = | `lampx`: V × 2 / I **× 2** in brick red, struck | = | = |
| 39.7 | b10 · c33 "turn" | Card, Chips | = | = | the **table** returns (rows 1–2 full, row 3 empty) | "Your turn" |
| ~40.5 | c34 "resistor" | SwapPart, EquationTransform | lamp → resistor; rays and "R ↑" go | V = I × R (the tool) | = | = |
| ~41.7 | c35 "six" | ChangeValue, Card | V 4 → 6 V; I "?" | = | row 3 V cell "6" | = |
| 44.1–47.1 | b10 think_calc 3.0 s | PauseForPrediction | ring on "I = ? A" | V = I × R | row 3 I slot empty | plate "Your turn: I = ?" |
| ~47.5 | b11 · c37 "six" | ChangeValue, EquationTransform, Card | I → 0.60 A | `calc`: 6 V ÷ 10 Ω = 0.60 A | row 3 I cell "0.60" | "The rule is yours" (on "the") |
| ~50.0 | c38 "rule" | EquationTransform, Card, Emphasize | = | `conf`: … = 0.60 A ✓ | row 3 V ÷ I "10" | = |
| ~53.6 (re-timed) | b13 · c40 "free" | Card (rows on their offsets) | = | = | **points**: 1 "Double V, double I." 2 (+0.5 s) "6 V ÷ 10 Ω = 0.60 A." 3 (+1.0 s) "Only at constant temperature." | "The rule is yours" stays |
| 58.5 | b14 · "Professor" | Pop (runtime end card) | = (final state: 6 V, 0.60 A, resistor, condition chip) | gives way to the chip "Free lesson: Ohm's law" | points stay as the answer sheet | wordmark sticker "Professor Diki Simplified" |

## Rules this board keeps

- **Persistence.** The circuit is never hidden, end card included (`PreserveObject`). The end card is the board's final state.
- **One owner per property.**
  - The circuit is driven by one `StateTable`.
  - The result sheet is driven by one `equation.drive`.
  - Each card has one `D.Card` window set. Table cells reveal through card.js.
  - The runtime owns the ident, the chips, the plate and the end card. The scene only toggles which of the two prompt spans the plate shows.
- **Literal text.** Every card string is a fixture value under `display.card.*`. The end card uses `display.ui.endcard_line1/2`. The chips are the script's `on_screen.headline`, and every word in them is spoken in its beat.

**Pauses (final, mid-band PD-01):** think_choice 2.0 s, think_calc 3.0 s, every land 0.6 s, inspect 1.0 s, joins unchanged; tail 0.9 s (the 0.70 s motif is no longer clipped). Planned 60.85 s at rate_scale 0.82; synthetic preview sheet 60.05 s.
