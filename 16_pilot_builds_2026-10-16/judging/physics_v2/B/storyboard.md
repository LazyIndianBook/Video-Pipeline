# Storyboard: phy-ohm-ci-01 (Ohm's law, Class 10), the builder_v2, doodle-handdrawn, 1080x1920

Zones (tokens file, placeholder insets 250/450/60/120, unmeasured): top_title y 250-518 (headline, Kalam, 66 px); middle_visual y 518-1177 (hero, 888 x 659 px, x 96-984); bottom_caption y 1177-1470 (think plate in s02, disclosure in s05 only). Synthetic durations come from the preview sheets; the lead's narration gives real timing.

Depth layers (every scene): L0 paper (stage background, `data-layer="L0"`); L1 shelf (books, tint #CFDCF1); L2 board (tint #B9CCEA, three hatch strokes at its bottom-right); L3 circuit, chips and cards (flat, `data-fx` on every glyph); L4 pencil cropped by the left frame edge.

## Scene table

| Scene | Beat(s), slot | Top (headline) | Middle (hero), reveal cue -> anchor word | Bottom | Notes |
|---|---|---|---|---|---|
| s01 hook | b01 hook.question_reveal | "twice the voltage?" (words 16-18, per word) | board, shelf, wires, cell on "Here's"; r_chip on "ten-ohm"; resistor on "resistor"; v1_chip on "two"; v2_chip on "four" (emphasis on 2nd "volts"); ammeter, i_label, qmark on "current" | none | Circuit centred in the zone; no answer shown (the ammeter is a question mark) |
| s02 predict | b02 check.predict, think 5 s | "predict the current" | board, shelf, wires, cell, resistor, r_chip on "Predict"; v2_chip on "four"; ammeter, i_label, qmark on "current" | "Pause. Predict." plate for the think window (meta.think_windows[0]), boil frozen | No 2 V chip (only 4 V is asked); no 0.4 A on screen |
| s03 ratio | b03 explain.ladder_step, b04 worked.step | "twice the current", then "voltage over current" | circuit as s01 (board, shelf, wires, cell, resistor, ammeter, i_label on "At"/"current"); card1 on "two" (V, I rows on "two", "amperes"); card2 on "four" (V, I rows on "four", "amperes" occ 2); rel_x2 (x2) on "Twice" (emphasis on "twice" occ 2); cond_chip on "constant"; r_chip and ratio_1, ratio_2 on "ten" (occ 1, 2); eq_box on "multiplied" | none | Ratio rows are the worked recount (two readings, both give 10 ohm) |
| s04 confront | b05 misconception.confront | "resistance rises" | board, shelf, wires, cell on "Always" (same ids as s01/s03); name_lamp on "filament"; swap_lamp (replaces the resistor) on "lamp"; chg_r (R up) on "rises"; strike_x2 (struck x2) on "doubling"; ammeter, i_label on "current" | none | Answers the predict prompt in sentence 1 ("Always is not safe") and names the evidence in sentence 2 |
| s05 recap | b06 recap.statement, b07 outro.disclosure | "constant temperature" | five rows, each with a tick: cond_row on "constant" (tick1 "temperature"); rel_row on "proportional" (tick2 "voltage"); eq_row on "equals" (tick3 "resistance"); lamp_row on "lamp" and chg_row on "rises" (tick4 "rises"); strike_row on "breaks" (tick5 "rule") | disclosure on "AI-generated" (text from meta.beats_text, verbatim) | Nothing promotional; recap rows repeat every condition, relation, equation and glyph from s03/s04 |

## State table (fixture field -> beats where it is on screen)

Only display strings are shown on screen; numbers come from `results.*` in the asserts. "-" means not on screen in that beat.

| Fixture field | Text | b01 | b02 | b03 | b04 | b05 | b06 | b07 |
|---|---|---|---|---|---|---|---|---|
| display.r_label + r_value | "R = 10 Ω" | r_chip (on "ten-ohm") | r_chip (on "Predict") | - | r_chip (on "ten") | - (not in s04) | - | - |
| display.v_label + v1_value | "V = 2 V" | v1_chip (on "two") | - | col1_v (on "two") | - | - | - | - |
| display.v_label + v2_value | "V = 4 V" | v2_chip (on "four") | v2_chip (on "four") | col2_v (on "four") | - | - | - | - |
| display.i1_value | "I = 0.2 A" | - | - | col1_i (on "amperes") | - | - | - | - |
| display.i2_value | "I = 0.4 A" | - | - | col2_i (on "amperes", occ 2) | - | - | - | - |
| display.i_label | "I =" | i_label (on "current") | i_label (on "current") | i_label (on "current") | - | i_label (on "current") | - | - |
| display.ratio_label + ratio_value | "V / I = 10 Ω" | - | - | - | ratio_1, ratio_2 (on "ten") | - | - | - |
| display.times_two | "×2" | - | - | rel_x2 (on "Twice"; emphasis on "twice") | - | strike_x2 (on "doubling"; struck) | strike_row (on "breaks"; struck) | - |
| display.condition | "constant temperature" | - | - | cond_chip (on "constant") | - | - | cond_row (on "constant") | - |
| display.equation | "V = I × R" | - | - | - | eq_box (on "multiplied") | - | eq_row (on "equals") | - |
| display.relation | "×2 voltage → ×2 current" | - | - | - | - | - | rel_row (on "proportional") | - |
| display.lamp_name | "filament lamp" | - | - | - | - | name_lamp (on "filament") | lamp_row (on "lamp") | - |
| display.rise_glyph | "R ↑" | - | - | - | - | chg_r (on "rises") | chg_row (on "rises") | - |
| display.ui.think_prompt | "Pause. Predict." | - | think_plate (window) | - | - | - | - | - |
| beats_text headline | words | b01 | b02 | b03 "twice the current" | b04 "voltage over current" | b05 "resistance rises" | b06 "constant temperature" | none |
| beats_text disclosure | verbatim | - | - | - | - | - | - | disclosure (on "AI-generated") |

## Checks run on this storyboard

- Every cue anchor is a word of its beat (check_script), every element id exists in its scene (no W_CUE_NO_ELEMENT), and every data-rv element has a reveal cue (no W_ELEMENT_NO_CUE).
- Every spoken number is a fixture assert (compute.py); the only spoken numbers are 2, 4, 10 (ohm), 0.2 and 0.4 (A) and "twice".
