# Build notes: phy-ohm-pd-04, "What is Ohm's law?" (`explainer_60`, `pace: fast`, profile `pds-60-method-1.0`)

Rebuilt 17 Oct 2026 under PD-27 (plain continuous speech) and PD-28 (fast and packed). A second round of coordinator fixes followed the same day:
- the founder's own opening;
- words before symbols in b05, and a plainer b04;
- nothing learner-critical below the 50 px floor.

The short is **not narrated and not rendered**: the ElevenLabs quota is exhausted until 15 Nov 2026. `narrate.py` and `render.py` were not run.

## Second-round changes (coordinator, 17 Oct 2026)

| Item | Before | Now |
|---|---|---|
| b01 | "Something pushes electricity through a wire. That push is voltage…" | the founder's words: "When electricity passes through a wire, something pushes it along. That push is called voltage, and we measure it in volts." |
| b04 | "…current grows in step with the push, while…" | "Ohm's law says the current goes up with the push, as long as the temperature stays the same." |
| b05 | "So V equals I R…" | "So voltage equals current times resistance: V equals I R. Then I is V over R, and R is V over I." The words come first, with halos on the V, I and R chips on the board. |
| NCERT sheet | 40 px quote, 32 px source, b04 only | **50 px** quote in two pages (page 1 in b04, page 2 in b05) and a **44 px** source line, "NCERT Class 10 Science, Chapter 12 Electricity, §12.3", on one taped sheet spanning the result and card lanes for **b04 and b05**; then the normal lanes return. |
| Graph | 38 px ticks on a sheet over both lanes | the **whole card lane**: axis words "V (V)" and "I (A)" at **50 px**, tick numerals at **44 px**, origin + (0.20, 2), (0.40, 4), (0.60, 6) and the line through them. "V–I graph (NCERT §12.3)", then "slope = V ÷ I = R = 10 Ω", on the result sheet at 54–56 px. The filament label is 44 px in two lines. |

**Refit to 60 s (filler only).** The new wording added about 10 words. I removed these to fit:
- "and" in b02 (now a semicolon);
- "a little" and "measured" in b03 ("in ohms" stays);
- "a current of" in b06;
- "Plot … and you get" in b09 ("Voltage against current makes a straight line through zero.").

The pauses after b06 and b08 became joins. No fact, unit, number or condition was removed.

**Formula on the NCERT page (third round).** Page 2 of the NCERT sheet carries the formula line "V = I R · I = V / R · R = V / I" beneath the second half of the sentence. It is 50 px, in the equation font, with V, I and R in their colour roles, and it appears whole on "V" of "V equals I R" (cue c14d). The result sheet and the calculation take over from b06, as before.

The sheet was tightened to fit, and it measures within its 422 px:
- padding 18/10 px;
- source line-height 1.05;
- statement line-height 1.1.

Frames inspected: 18, 22 and 26 s. At 22 s the two pages are mid cross-fade (the b05 start); that is transient.

I = V ÷ R is then built on the result sheet in b06. All three forms are on the answer sheet (point 1), and V ÷ I = R is on the graph's slope line. If the lead wants the symbol forms on the sheet during b05, the alternative is to lift the NCERT sheet at "V equals I R".

## Fourth round: b01 stillness (QA on the local-voice render, 17 Oct 2026)

QA found no visual change for 6.5 s from 0.5 s during b01. These are scene and cue changes only; the text is unchanged:
- c00 "passes" (new): the current dashes start at the 2 V pace.
- c01 "pushes" (now a reveal): a link from the V chip to the battery, plus a scale-only pop on the battery sticker (0.94 → 1; the preserved sticker never fades).
- c02 "voltage": the V chip pops, and the Voltage card appears with its link. The card now reads "potential difference: energy per unit charge. 1 V = 1 J/C".
- c03 "volts": halo on V = 2 V (unchanged).
- c04 "flow" (b02): now a halo on the running dashes.

Frames inspected at 1, 3, 5 and 7 s. The largest gap between discrete changes over the whole timeline is 2.31 s. All checks were re-run: check_script OK, check_pd_script OK, compute OK, build lint ok with no gates, preview exit 0, qa_scene PASS 9/9, brand pass.

## Changes from the first v4 draft (first round)

| | First v4 (rejected) | Now |
|---|---|---|
| Register | clipped captions ("Ohm's law: what's this meter reading? Let's calculate.", "resistance, ten ohms.") | one teacher talking in full sentences: plain word, then the term, then the unit |
| Pace | 125 words, rate_scale 0.95, about 126 wpm | 166 words, `pace: fast`, rate_scale 1.2, about 178 wpm while speaking |
| Content | 2 V → 0.20 A and 4 V → 0.40 A | **plus** the NCERT §12.3 statement verbatim; V = I R, I = V/R and R = V/I; the unit meanings; **20 Ω → 0.10 A**; the **V–I graph** (slope R); the hot filament bending the line |
| Pauses | join, land, one inspect | join (0.2 s) and land (0.5 s) only; planned silence 3.8 % (≤ 8 %) |

## Pass 1: specification

**Outcome.** The viewer can:
- say what voltage, current and resistance are, with their units (1 V = 1 J/C, 1 A = 1 C/s, 1 Ω = 1 V/A);
- state Ohm's law in plain words and recognise NCERT §12.3's statement with its condition;
- use V = I R, I = V/R and R = V/I on three cases: 2 V and 10 Ω → 0.20 A; 4 V → 0.40 A; 2 V and 20 Ω → 0.10 A;
- read the V–I graph as a straight line through the origin whose slope is R;
- know that a hot filament bends the line.

**Prerequisite boundary.** Class 10. Knows a cell, a wire and a bulb, and has heard "volt" and "amp". Coulomb and joule appear only on the unit cards.

**Dependency map.**
1. Voltage (b01), current (b02) and resistance (b03), each before it is used.
2. The law with its condition (b04), before the formula (b05).
3. The formula, before any number (b06).
4. Case 1 (b06), before the two changes (b07 and b08) on the same board.
5. The three points, before the graph (b09).
6. The straight line, before the bend (b10).
7. Everything, before the claim (b11).

**Ledgers.** These are in `artefacts.ledgers` in script.json.

| Term | Plain words (spoken first) | Card | Unit meaning | Node |
|---|---|---|---|---|
| voltage | something pushes; that push | Voltage: "the push, or potential difference." | 1 V = 1 J/C | DEF-potential-difference, DEF-units |
| current | the flow | Current: "the charge flowing each second." | 1 A = 1 C/s | DEF-current, DEF-units |
| resistance | holds the flow back a little | Resistance: "how much it holds the flow back." | 1 Ω = 1 V/A | DEF-resistance, DEF-units |
| Ohm's law | current grows in step with the push, while the temperature stays the same | NCERT §12.3, verbatim | — | CLM-ncert-ohm |
| slope | (the steepness of the line) is the resistance | "slope = V ÷ I = R = 10 Ω" | Ω | REP-vi-graph |

**Fixture additions.** All asserted in `fixtures/compute.py`:
- `parameters.r2` = 20 and `results.i_r2` = 0.1 (2/20);
- `results.ratio_r`;
- `results.graph` = [[0, 0], [0.2, 2], [0.4, 4], [0.6, 6]] (every point on V = R I);
- `display.units` = "1 A = 1 C/s", "1 V = 1 J/C" and "1 Ω = 1 V/A";
- `display.card.ncert` (the tag, the statement verbatim, the source);
- `display.card.graph`;
- `display.condition` = "same temperature".

compute.py asserts:
- 2/10 = 0.2, 4/10 = 0.4, 6/10 = 0.6 and 2/20 = 0.1;
- V = I R together with both rearrangements;
- the unit strings and the NCERT sentence, verbatim;
- the script closure: it speaks "two volts", "four volts", "ten ohms", "twenty ohms", "point two", "point four" and "point one", and no other number word.

**Graph nodes.**
- Added: CLM-ncert-ohm (verbatim, NCERT Class 10 Science, Ch. 12 Electricity, §12.3), DEF-units, WRK-ohm-double-r and REP-vi-graph (NCERT §12.3, Activity 12.1, the V–I graph).
- Section numbers added to the NCERT sources: 12.1, 12.2 and 12.3.
- CLM-filament reworded: the hot filament resists more, so its line is not straight.

## Pass 2: three openings

| # | Opening | Topic | Uncertainty | Pay-off | Verdict |
|---|---|---|---|---|---|
| A | "Ohm's law: what's this meter reading? Let's calculate." | 5 | 4 | 5 | Rejected by the founder: a clipped fragment (PD-27). |
| **B** | **"What is Ohm's law? When electricity passes through a wire, something pushes it along. That push is called voltage, and we measure it in volts."** | 5 | 3 | 5 | **Chosen.** These are the founder's own words, a question followed at once by the first definition in plain full sentences. The question ends at about 1.6 s planned (1.8 s unscaled in check_pd). It is answered by b04 (the law), and the claim (b11) closes it. |
| C | "This meter shows a question mark. Ohm's law tells us the number, so let's find it." | 4 | 4 | 5 | A good puzzle, but it delays the first definition by about 5 s and is not the founder's opening. |

`promise_line` = "What is Ohm's law?".

## Pass 4: compression

The founder's draft ran to about 240 words; the plan holds 166 at rate_scale 1.2. The second-round refit is described at the top of this file. The cuts are logged in `artefacts.repair_log`:
- The NCERT sentence moved, verbatim, to the card. The voice keeps the plain version with its condition.
- The three formula sentences became one line with both rearrangements.
- "Here the battery pushes…, which is point two amperes" became "Two volts over ten ohms gives point two amperes."
- The filament beat became one sentence with "because". The condition stays spoken in b04, struck on the chip in b10, and kept as point 3 of the answer sheet.

No sentence is over 18 words, and 16 of 18 have 14 words or fewer. The PD-27 checker reports 0 warnings.

## Review questions (method §6), with beat ids

1. **Promise and pay-off.** The promise is b01 "What is Ohm's law?". It is answered in b04 (plain law plus condition, with NCERT's words on the sheet) and paid in b11 "Twice the push, twice the flow." with the answer sheet.
2. **What the viewer is doing during the definitions.** The meter shows "I = ? A" from frame 0 to b06, and each definition card links to its object (b01 V, b02 meter, b03 resistor). The viewer is gathering what the meter needs.
3. **Visible action behind each term.**
   - voltage: card plus link to V (b01);
   - current: dashes plus card plus link to the meter (b02);
   - resistance: halo on the resistor plus card plus link (b03);
   - condition: the chip pops (b04);
   - "across the ends": the bracket (b04);
   - formula: halos on the V, I and R chips as the words and then the symbols are spoken (b05), I = V ÷ R built with values (b06), all three forms on the answer sheet (b11);
   - slope: "slope = V ÷ I = R = 10 Ω" on the result sheet over the graph (b09);
   - exception: the lamp, heat, the struck chip and the brick curve (b10).
4. **Transitions.**
   - "The flow…" (b02) continues the push from b01;
   - "holds the flow back" (b03);
   - "as long as the temperature…" (b04);
   - "So voltage equals current times resistance: V equals I R. Then…" (b05);
   - b06 applies b05;
   - "Double the push" (b07);
   - "Keep two volts, double the resistance" (b08);
   - "Voltage against current makes… Its slope…" (b09);
   - "But … because" (b10).
5. **Does every beat add something?**
   - b01–b03 each add a quantity with its unit;
   - b04 adds the law and its condition;
   - b05 adds the formula;
   - b06–b08 are the three cases;
   - b09 is the representation;
   - b10 is the exception;
   - b11 is the pay-off;
   - b12 is the next gain;
   - b13 is the brand.
6. **Is the student's action answerable in the flow?** There is no question to the student (PD-24). Each case is answered on the board, and the sheet builds I = V ÷ R with units before every reading.
7. **Is the energy made by progress?** Yes. The peak is b07 (double V); b06, b08 and b10 are high; b05 (the formula) is the calm trough at 156 wpm planned. Every unit is spoken, and none is rushed.
8. **Does the ending complete the short?** Yes. The claim, then the answer sheet, then "Try more cases in the free lesson." (`cta_line`), then the brand.

## Checks (final state, 17 Oct 2026)

- `check_script.py`: **OK** (2 warnings). Words 166 (150–185), 897 characters, planned **60.68 s** (60 ± 1 at rate_scale 1.2), planned silence **2.1 %** (≤ 8 %). The warnings:
  - "no misconception.confront beat": the exception lives in `explain.condition`, per the explainer spine.
  - "hook question ends at 8.11 s": this measures the whole hook *beat* (the founder's three sentences). The question itself ends at about 1.6 s (check_pd: 1.8 s unscaled).
- `check_pd_script.py`: **OK**, with 0 PD-27 warnings and 0 M-warnings (max re-hook gap 10.4 s). Its plan line (72.0 s) ignores `voice.rate_scale`.
- `fixtures/compute.py`: **fixture OK (script closure checked)**.
- `build_scene.py`: lint ok (0 errors, 0 warnings); gate_failures [].
- `preview_scene.py`: exit 0; cue sheet and fixture both injected; 0 errors.
- `qa_scene.py`: **PASS**, purity 9/9, 0 blocking.
- `brand_check.py`: **pass**.
- Change density (own measurement on the built scene): largest gap 2.31 s (≤ 2.5 s).

## Frames inspected and fixed

Frames: 0, 5, 12, 16, 20, 25, 30, 35, 40, 45, 50 and 58 s (`scenes/_preview/contact_sheet_v4.png`), plus 50.9, 52.35, 52.86 and 53.27 s for the bend.

- **NCERT sheet.** At 50 px the whole sentence needs about 6 lines plus a 2-line 44 px source, which is more than the 422 px the two lanes give. It is therefore shown in two pages on the same sheet (b04, then b05), split once, with "…" as the page-turn mark. compute.py asserts that page 1 + page 2 = the verbatim statement. A guard is added (W_CARD_OVERFLOW if it overflows the sheet).
- **Points card.** It overflowed, so point 3 is now "Same temperature only."
- **Graph.**
  - The axis words were moved clear of the ticks: "V (V)" beside the top of the axis, "I (A)" at the right end. The ticks are numerals only.
  - The round line caps showed a dot before the line was traced; they are now butt caps.
  - The slope words now sit on the result sheet at 56 px.
  - "filament lamp" (44 px, two lines) sits in the upper left, clear of the I axis and the points.
- **Exception timing.** The bend first landed on the last word, about 0.5 s before the sheet lifted. b10 now says "bends" mid-sentence, and the sheet stays until 0.6 s into the claim.
- **Stillness.** b03 and b04 each had a 2.66 s still stretch. Halos on "back" (c08b) and "push" (c12b) fix them.
- **Known transient.** During the 0.3 s lamp/resistor cross-fade, the "filament lamp" and "R = 10 Ω" chips overlap. This is the component's in-place SwapPart by design.

## What remains for review

1. **CLM-ncert-ohm.** Check the verbatim sentence against the current NCERT edition. Also confirm the V–I graph's figure number for REP-vi-graph; it is "to be confirmed" in the node.
2. **Text sizes.** The NCERT sentence is now 50 px, its source line 44 px, the graph axis words 50 px and the ticks and filament label 44 px. The coordinator's 44 px allowance covers the source line, the ticks and the filament label; everything else learner-critical is at 50 px or above. Open: whether the two-page NCERT split is acceptable, or whether the lead prefers lifting the sheet at "V equals I R" so the symbol forms show on the result sheet during b05.
3. **New nodes.** DEF-current, DEF-resistance, DEF-potential-difference, DEF-units, SIM-ideal-cell, WRK-ohm-double-r and REP-vi-graph. Also confirm "Each wire holds the flow back" as the plain wording for resistance, and the filament curve as a qualitative shape only (PD-16: no lamp values).
4. **Pronunciation.** Check that "V equals I R", "I is V over R" and "R is V over I" are read as letters on the fast read.
5. **After narration.**
   - Measure rate_scale on this script at the fast pace (PD-28). Narrate first; then, if the natural read is slower, apply tempo up to 1.3.
   - Measure dead time (≤ 8 %) and the A7 transcript match.
   - Re-time the cues from the measured words.
6. **M11 route.** "More cases in the free lesson" must exist; 6 V → 0.60 A is in the fixture.
