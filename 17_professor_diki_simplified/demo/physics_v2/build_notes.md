# Build notes: phy-ohm-pd-02, Professor Diki Simplified (the "after" of the physics before-vs-after)

> **Current build: v2 rebuild on design system v2.0.1** (see the "v2 rebuild" section at the end). The before-table, scroll test, hooks and claim line below still hold. Where the v1 sections mention the header lockup, the "AI-generated narration" end-card line, the motif rule, `W_NO_END_CARD` or the light palette, they describe v1 and are superseded by PD-19 to PD-21.

- **Built:** 16 Oct 2026, under PD-01 to PD-16.
- **Original ("before"):** `16_pilot_builds_2026-10-16/physics/opus/` (phy-ohm-ci-01, 69.9 s, 5 scenes).
- **Not narrated yet.** The lead narrates with the stock English voice (PD-05). Every time below is planned (`pilotlib.plan`).
- **Size:** 125 words, 743 characters. Planned 60.63 s, with silence at 13.5 % and the insight at 7.1 s. The hook question ends at 2.9 s and the transfer answer lands at 78 % of the runtime.

## What the original did at each timestamp, and what this build does instead

| Original (video time) | What went wrong (audit id) | This build |
|---|---|---|
| 00:00–00:03 | Empty board, plus a pencil; the question builds word by word (A2-04, A2-06) | Frame 0 holds the complete circuit (R = 10 Ω, V = 2 V, the meter at 0.20 A), the whole hook line and the header. The question ends at 2.9 s. |
| 00:03–00:11 | The loop, resistor and values are drawn stroke by stroke. The circuit is not useful until about 8 s (A2-05). | Nothing is drawn on. By 7.1 s the givens are spoken onto parts that are already visible, and the first result lands by 9.7 s (`insight_beat`). |
| 00:10–00:11 | "V = 2 V" is replaced in place by "4 V", so the 2 V state is destroyed (A2-12) | ChangeValue on the supply plus CompareStates: 2 V \| 4 V and 0.20 A \| ? stay side by side. |
| 00:11–00:22 | "Pause and predict the current at four volts": unanswerable, because 0.2 A was never shown. It asked two tasks, then held a 5.5 s silent plate (A1-01, A2-14, PD-01). | One question, "More current, less, or the same?", with every given on screen. The `think_choice` window is 2.0 s, the ring sits on "I = ? A", and the reveal follows 0.0 s after the window. |
| 00:22–00:23 | The circuit is replaced by two empty cards: the first reset (A2-01) | There are no resets. The 0.40 A lands on the same meter, the × 2 marks go into the compare grid, and the claim line goes up (peak energy). |
| 00:23–00:32 | The rows are written word by word, and "the current" headline has a hole in it (A2-05, A2-06) | Whole lines only. "Twice the push, twice the flow." stays on screen for about 9 s. |
| 00:33–00:45 | A long naming sentence: "That constant is the resistance…" (A1) | V ÷ I = 10 Ω at both points, using the same values slid over from the compare grid. Then V = I × R, with a dashed MapSymbol link from R to the resistor. |
| 00:46–00:50 | "But always is not safe". The loop is redrawn with a gap, so the circuit is open for 3.5 s (A1-02, A2-03) | "Always? Only at constant temperature." The condition badge appears on its word inside a closed loop. |
| 00:50–00:57 | The bulb appears on "filament"; the × 2 is struck without showing a current (A2-12) | The lamp is swapped into the resistor's slot (the wires never move). Heat marks and glow appear, the badge dims, "R ↑" shows, and the current row's × 2 turns red and is struck. It is qualitative on purpose: `lamp.current_doubles: false`, and no lamp number exists (PD-16). |
| 00:57–01:05 | The board resets to empty, then a bare zigzag; the recap drops the result (A2-01, A2-02, A2-13) | Transfer instead (A1-27, PD-06). The lamp swaps back, the supply goes to 6 V, the meter shows "?", and the `think_calc` window is 3.0 s. Then 0.60 A appears with the worked line 6 V ÷ 10 Ω = 0.60 A ✓ and "If you got that, the rule is yours." |
| — | No learner action after 00:22 (A1-M1) | Two learner actions: the predict at 10 s and the transfer at 40 s. The win lands at 47 s. |
| 01:06–01:12 | Spoken "AI-generated narration; script by ExamLeaf.", then 2.2 s of static silence (A1-28, A2-15) | The tease "Next: why a bulb's graph curves. Follow for it.", then "Try the free lesson on Ohm's law." and "Professor Diki Simplified." The end card is the board's final state: wordmark, "Free lesson: Ohm's law", "AI-generated narration", and the motif rule in the 0.8 s tail. |
| whole video | Notebook identity: pencil, shelf, handwriting face. Colour carries no meaning (A2-09, A2-10). | The design system's one type family and lanes. Colour means something (V blue, I green, R and the condition amber, red only on the struck × 2). No decoration tokens (the build gate passed). |

## Scroll test

"Frame one is a live circuit whose meter already reads 0.20 A beside a two-second yes-or-no question about doubling, so a scrolling 16-year-old can bet on the answer before the swipe and stays to see the meter settle it."

## Five hooks considered

| Kind | Hook | Scroll | Honest | Decision |
|---|---|---|---|---|
| pattern_interrupt | "The bulb above you breaks this rule. Watch." | 4 | yes | Rejected. The bulb is not on the board at frame 0, and the hook spends the exception before the rule exists. |
| bold_claim | "Double the push, double the flow. Mostly." | 3 | yes | Rejected. It answers the prediction before it is asked. |
| challenge | "This meter reads point two. Beat it to the next reading." | 4 | yes | Rejected. At 11 words the question ends at about 4.4 s (more than 3.0 s), and it asks for a reading before the 4 V given is shown. |
| **visible_puzzle** | **"Double the voltage. Does current always double?"** | 4 | yes | **Chosen.** Its whole picture is on screen at frame 0 and the question ends at 2.9 s. "Always" opens a second loop, the bulb at about 31 s, so a viewer who calls "yes" at 16 s still has a reason to stay. It does not answer the predict. |
| stakes | "This one line is two marks in your board exam." | 3 | no | Rejected. There is no sourced marking scheme, and it is an exam promise. |

The chosen hook improves on the exemplar's "Double the voltage. Double the current?" (scroll 3). That version has no catch, so its curiosity is used up at the first payoff.

## Quotable line

"Twice the push, twice the flow."
- It is spoken verbatim in the payoff beat b05.
- It is shown whole in the title lane from "Twice" (about 17.8 s) to "Ohm's" (about 27.3 s).
- It is the literal fixture string `display.ui.claim_line`, which compute.py asserts equals the script's `claim_line`.

## Checks (final run)

- `check_script.py`: `OK` (125 words, planned 60.63 s, silence 13.5 %).
- `check_pd_script.py`: `OK` (max re-hook gap 10.8 s, hook question ends at 2.9 s).
- `lint_seek_contract.js --level 1`: `{'files': 1, 'errors': 0, 'warnings': 0, 'ok': True}`.
- `qa_scene.py`: `ok True`.
  - Diagram share is 0.45 and the hero fills 0.922 of the lane (about 0.41 of the frame height).
  - No motion inside the think windows; seek purity 9/9.
  - Its only report is the warning `W_NO_END_CARD` (see below).
- `preview_scene.py`: exit 0. The cue sheet and fixture are both `injected`; 0 blocking issues, 1 warning (`W_NO_END_CARD`).
- `brand_check.py`: `pass`, 0 violations, 8/8 required items.
- `fixtures/compute.py`: `fixture OK (script closure checked)`. Every spoken number phrase maps to a fixture value, and no unfixtured number is spoken.

## Preview frames inspected and fixes

| Frames | Found | Fix |
|---|---|---|
| 001.00, 015.24, 019.55, 038.72, 045.26, 058.49 (first pass) | At the lamp, the line "V × 2 I × 2" read as "V × 2I". The think ring crowded the lone "?" glyph on the board and in the result lane. | `lampx` became a two-row grid (V × 2 over I × 2, with the I row struck). The ring now goes around the whole "I = ? A" readout, and the result-lane ring was dropped. |
| 003.45, 009.28, 027.33, 030.10, 032.70, 036.95, 050.07, 053.94, 056.29 | At 56.29 the "Free lesson" line overlapped the fading worked line | The free-lesson reveal now waits until 0.5 s after the "free" cue. Re-checked at 56.29: clean. |
| 000.00, 015.24, 038.72, 056.29, 058.49, 059.90 (final) | Frame 0 is complete. The predict plate shows its givens. The exception is legible. The end card has its three lines plus the motif rule. | — |

## What remains for review

1. **New graph nodes:**
   - SIM-push-flow (`what_is_lost` stated);
   - ASM-transfer-six-volts.
   Both need academic sign-off.
2. **CLM-filament:**
   - NCERT ("Electricity", sections "Ohm's Law" and "Heating Effect of Electric Current") gives the condition and the hot filament. It does not state in one sentence that filament resistance rises with temperature, so this needs subject review.
   - The claim stays qualitative. No lamp current appears anywhere.
3. **The tease** "Next: why a bulb's graph curves" is honest only if that short is in the release plan. If it is not, cut b12 and re-time (about −3.8 s, so add words elsewhere).
4. **`W_NO_END_CARD`:**
   - `diki_runtime.js` keys its end card on a v1 `outro.disclosure` slot, while v2 ends on `outro.brand`.
   - This scene therefore builds its own end card from literal fixture lines, and parks the runtime's lockup-name spans hidden so that the header is one data-fx string (PD-13).
   - The runtime needs a v2 branch (design-system owner).
5. **Palette moved mid-build:**
   - `tokens.json` changed to v1.1.0 "LIGHT VIVID", citing a PD-17 that is not in DECISIONS_PD.md, at 19:21 on 16 Oct.
   - The scene inlines whatever tokens exist at build time, so these frames are the light palette, not PD-15's dark one.
   - The lead should confirm PD-17 and rebuild if the tokens change again.
6. **Header code:**
   - "OHM 01" as briefed.
   - `brand/strings.json` `lesson_code_pattern` expects a code like "PHY-OHM-01". `brand_check` does not test the pattern; pick one.
7. **Hero fill:** 0.92 of the diagram lane, which is 45 % of the frame, so the circuit spans about 41 % of the frame height. It cannot pass 45 % of the frame without leaving its lane.
8. **No spoken exam line.** It was cut for time. The exam form is on screen instead: the title "V = I × R at constant temperature" during the win.
9. **Ledger:** no recent-openings ledger was supplied. The original physics opening was also a doubling question, so check the hook kind against the batch.
10. **After TTS:** re-measure the hook question end (≤ 3.0 s), the silence share (13.5 % planned; George adds 0.4–0.66 s at full stops) and the total (60.63 s planned, so +0.37 s of margin).

## v2 rebuild (design system v2.0.1, paper cut-out collage; PD-17 to PD-21)

### What changed

**Base and scene.** I re-copied `design_system/diki_scene_base.html` (v2) to `scenes/s01.src.html` and ported the scene block with `subject: 'physics'` and `card: true` (layout `carded`).
- The hook, beats, cues, timings and the 125-word script are unchanged.
- The circuit is now the v2 sticker component, with the same `set()` API and the same StateTable.
- "R ↑" is now a resistance chip placed beside the lamp label (verb Pop).

**Brand (PD-21).**
- The header lockup is gone, and so is `display.ui.header`.
- The runtime's opening ident shows the brand over the complete board from frame 0 and is gone by 2.46 s.
- The runtime end card triggers on the `outro.brand` beat. It shows `display.ui.endcard_line1` ("Professor Diki Simplified") as the wordmark sticker and `endcard_line2` ("Free lesson: Ohm's law") as a chip.
- My own end card and motif rule were removed. `W_NO_END_CARD` is gone.

**Disclosure (PD-20).** Removed everywhere:
- `display.ui.endcard_line3`;
- `on_screen.disclosure`;
- `outro.end_card.disclosure_line`.

**Headlines.** My title-lane lines became runtime ransom chips from `on_screen.headline`, and every word in them is spoken in its beat:

| Beat | Chips |
|---|---|
| b01 | "Does current always double?" |
| b05 | "Twice the push, twice the flow" (the claim line) |
| b07 | "Ohm's law" |
| b08 | "Always?" |
| b09 | "Resistance rises" |
| b10 | "Your turn" |
| b11 | "The rule is yours" |
| b12 | "Why a bulb's graph curves" |

**Cards (PD-18).** All card strings are under `display.card.*`, written and asserted by compute.py.
- **Table** V | I | V ÷ I.
  - From frame 0 it shows trial 1's V and I.
  - Row 2's V lands on "four" (c10) and its I on the reveal (c13).
  - The V ÷ I cells for rows 1 and 2 land only on "over" (c20), where the ratio is first computed.
  - Row 3 fills on "six" (c35, c37), and its ratio lands on "rule" (c38).
  - The table is up from frame 0 to c23, and again from c33 to c39.
- **Definition.** "Ohm's law" / "V = I × R, at constant temperature." (CLM-resistance-constant plus the condition from CLM-ohm-proportional). It is up from c23 to c33.
- **Points.** They land from c39 and stay on the end card as the answer sheet:
  1. "Double V, double I." (CLM-ohm-proportional)
  2. "6 V ÷ 10 Ω = 0.60 A." (ASM-transfer-six-volts)
  3. "Only at constant temperature." (condition; CLM-filament as the bounded case)

**Result sheet.** The `blank` step at "free" was removed. The worked line "6 V ÷ 10 Ω = 0.60 A ✓" now stays until the runtime fades it for the free-lesson chip.

**Science.** The filament case is still qualitative (`results.lamp.current_doubles: false`). No lamp current number exists anywhere.

**Script cards field.** `visual_op: "Card"` makes `check_script.py` fail: `pilotlib.VISUAL_OPS` predates v2 and has no Card, Pop, Slide, Chips or Tape. The card landings are therefore recorded per beat in `card: {verb: "Card", what}` on b01, b04, b05, b07, b10, b11 and b12, and are flagged under `requires.tooling`.

### Checks (v2, final run)

- `check_script.py`: `OK`, with no PD-20/PD-21 warnings (125 words, planned 60.63 s, silence 13.5 %).
- `check_pd_script.py`: `OK`.
- `build_scene.py`: lint level 1 `{'files': 1, 'errors': 0, 'warnings': 0, 'ok': True}`, gate failures `[]`.
- `qa_scene.py`: `qa_scene: PASS | purity 9/9 | errors 0 | blocking 0`.
  - Layout carded; diagram share 0.304; hero fill 0.822.
  - The world bands (bench, trim, table) and the ident are present.
  - End card 1.74 s on the synthetic sheet.
  - One warning: `W_HEADLINE_LONG` (b05 claim chips are 6 words, against a cap of 5).
- `preview_scene.py`: exit 0; cue sheet and fixture both `injected`; 0 blocking; 1 warning (`W_HEADLINE_LONG`).
- `brand_check.py`: `pass`, 0 violations. All 7 required items are true, including `opening_ident_text`, `end_card.brand_line` and `end_card.free_lesson_line`.
- `compute.py`: `fixture OK (script closure checked)`.

### Frames inspected (`scenes/_preview/`) against the reference (`design_system/examples/ohm_demo` 000.00, 013.32, 023.85, 034.77, 046.27)

| Frame | What it shows |
|---|---|
| 000.00 | ident, hook chips, complete circuit, table with trial 1 |
| 015.24 | predict plate; row 2 I slot empty |
| 019.55 | claim chips; × 2 marks |
| 028.71 | definition card |
| 038.72 | exception: lamp, "R ↑", dimmed condition chip, struck × 2 |
| 045.26 | transfer plate; table row 3 empty I slot |
| 050.07 | 0.60 A, table complete |
| 053.94 | points card |
| 059.90 | end card: wordmark, free-lesson chip, points |

Result: the house style matches the reference, with no overlaps and no empty lanes. The region below y 1470 is the blueprint world, as in the reference. Nothing needed fixing after looking.

### Still open (v2)

1. **`W_HEADLINE_LONG` on the claim chips.** "Twice the push, twice the flow" is 6 words, and the headline cap is 5. It is non-blocking and fits in two chip rows. Shortening it would break the verbatim quotable line, so it was kept. Decide whether to waive the cap or change the line.
2. **`pilotlib.VISUAL_OPS` needs "Card"** (plus Pop, Slide, Chips and Tape) before `visual_op: "Card"` can be used. Then move the `card` fields into `visual_op`.
3. **Hero size.** In the carded layout the diagram lane is 30.4 % of the frame and the hero fills 0.82 of it. This is the v2 floor (0.30), but the circuit is smaller than in v1.
4. **Earlier items 1, 2, 3, 8, 9 and 10 still stand:**
   - the new nodes;
   - CLM-filament review;
   - the tease must be scheduled;
   - no spoken exam line (the definition card and point 3 now carry the exam form);
   - the ledger;
   - re-measure after TTS.

   Items 4, 5 and 6 are resolved by v2:
   - the runtime end card works;
   - the palette is owned by v2;
   - the header is retired.

## Re-timed after narration (16 Oct 2026)

### What was measured

The coordinator narrated the 125-word script with George on eleven_v4 dialogue, using the direction-sheet tags.
- It measured **70.0 s**: 61.5 s of speech plus 8.5 s of gaps. The pauses landed as planned.
- The voice speaks at **122 wpm** overall. The rate table assumed 130–160.

Measured per beat (words / clip s / wpm):

| Beat | b01 | b02 | b03 | b04 | b05 | b06 | b07 | b08 | b09 | b10 | b11 | b12 | b13 | b14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Words | 7 | 10 | 7 | 11 | 9 | 9 | 14 | 5 | 12 | 11 | 11 | 9 | 7 | 3 |
| Clip (s) | 3.44 | 5.76 | 3.84 | 5.44 | 4.40 | 4.40 | 7.12 | 3.04 | 5.60 | 4.88 | 4.16 | 4.48 | 2.56 | 2.40 |
| wpm | 122 | 104 | 109 | 121 | 123 | 123 | 118 | 99 | 129 | 135 | 159 | 121 | 164 | 75 |

Added `voice.rate_scale: 0.82` to script.json. At that scale the 125-word script planned **71.69 s**.

### Changes (whole clauses only; the claim line, slot order, emphasis words, insight/payoff beats and pause purposes are unchanged)

| Beat | Was | Now |
|---|---|---|
| b01 | "Double the voltage. Does current always double?" (question ended at 3.7 s measured) | "Voltage doubles. Current always doubles?" (ends 2.6 s planned at 0.82). Chips: "Current always doubles?" |
| b02 | "Voltage pushes, resistance holds back, current flows. Watch the meter." | "Voltage pushes, resistance holds back, current flows." (cue c06 → "current") |
| b06 | "Why? Only the voltage changed, so current kept pace." | "Why? Only the voltage changed." (cue c19 → "changed"; the compare grid still shows current × 2) |
| b07 | "… That's Ohm's law: voltage equals …" | "Voltage over current stays ten ohms. Ohm's law: voltage equals current times resistance." |
| b09 | "Swap in a bulb. It heats, resistance rises, and current won't double." | "A hot bulb? Resistance rises, current won't double." (cue c29 → "Resistance") |
| b12 | "Next: why a bulb's graph curves. Follow for it." | **Cut.** The tease was optional, and this resolves the open "is the next short scheduled" item. The points card now lands on b13 "free" (c40). |
| Pauses | b04 think_choice 2.0 s, b05 land 0.6 s, b10 think_calc 3.0 s | Moved to the low end of their PD-01 ranges: b04 1.8 s, b05 0.5 s, b10 2.7 s. The purposes are unchanged. |

### Result

- Word count went from 125 to **102**. Planned **59.65 s** at scale 0.82, with silence at 12.7 %.
- Characters to re-bill (the spoken text of the edited beats b01, b02, b06, b07 and b09): **262**. b12 is gone, and the other beats' text is unchanged.

### Checks

- `check_script.py`: one problem, `spoken words 102 outside 120-135 (PD-07)`. That word band assumes 140–155 wpm. At the measured 122 wpm, 60 s holds about 100–106 words. So the band needs to scale with `rate_scale` (about 98–111 at 0.82) or be re-decided. Every other check_script rule passes.
- `check_pd_script.py`: `OK`. Note that it reads the JSON directly and therefore plans at scale 1.0, so its "hook question ends 2.2 s" is the unscaled figure. At 0.82 the question ends at 2.6 s.
- `compute.py`: `fixture OK (script closure checked)`.
- `build_scene.py`: lint `{'files': 1, 'errors': 0, 'warnings': 0, 'ok': True}`, gates `[]`.
- `qa_scene.py`: `PASS | purity 9/9 | errors 0 | blocking 0`.
- `preview_scene.py`: exit 0, both sources injected, errors 0, blocking 0.
- `brand_check.py`: pass.

### Frames re-inspected

000.00, 017.92, 038.98, 056.82, 057.23 and 058.92 are clean.

Frame 017.92 shows the meter mid-tween at "I = 0.30 A". The runtime's ChangeValue tweens from the last shown number (0.20) to 0.40, so for about 0.3 s an intermediate value is on screen. This is design-system behaviour (the reference example does the same). Consider a no-tween option for values revealed from "?".

## Motion in b02–b03 (after render QA A15, 16 Oct 2026)

QA A15 found no visible change for 6.0 s from 0.5 s, during b02 and b03. The auto-emphasis halos were too faint on the wood.

I changed only the scene (`scenes/s01.src.html`). The script text and cue ids are unchanged, so nothing is re-billed. No cue was added; everything hangs on the existing cues:

| Cue | Word | Verb | What it shows |
|---|---|---|---|
| c03 | "pushes" | MapSymbol | V chip → battery, in voltage blue |
| c04 | "resistance" | MapSymbol | R chip → resistor, in amber |
| c05 | "flows" | TracePath (0.8 s) | Current drawn as a two-tone teal line ON the wire: from the + terminal, through the ammeter side and the resistor side, into the − terminal. It breaks at each sticker. |
| c05 + 0.8 | — | Pop | An arrowhead lands on the − terminal. The trace and the arrowhead hold until "four" (c10), then leave before the think window. |
| c07, c08, c09 | "Two", "ten", "amperes" | Emphasize (pad 24, 0.35 s) | Clear halos on the V, R and I chips; c09 also halos the table's I cell. |

**Change density.** Changes now land at 0.0 s (frame 0), 0.9 s, about 2.5 s (the ident leaves), 2.9 s, 3.4 s, 4.7 s, 5.2–6.0 s, 5.8 s, 6.8 s and 8.6 s. The c09 halo at 8.6 s is followed by the c10 change at 10.0 s, so no still gap runs longer than 3 s.

**Think windows.** Nothing moves in either window: `motion_in_think: []`.

**Frames inspected:** 001.50, 003.19, 003.65, 005.48, 005.60, 006.14, 006.20, 008.00 and 008.65.
- The first trace sat under the ink wire, and its arrowhead pointed the wrong way.
- I redrew it on top of the wire with gaps at the parts, and the arrowhead now points into the − terminal.

**Checks:**
- `build_scene.py`: lint `{'files': 1, 'errors': 0, 'warnings': 0, 'ok': True}`, gates `[]`.
- `preview_scene.py`: exit 0, 0 errors, 0 blocking.
- `qa_scene.py`: `PASS | purity 9/9 | errors 0 | blocking 0`.
- `brand_check.py`: pass.
- `check_script.py`: `OK`, planned 59.65 s, silence 12.7 %. The word band has been recalibrated, so this check now passes.
- `check_pd_script.py`: `OK`.

## Three-way prediction chips, pause re-centring and tail (after final render QA, 16 Oct 2026)

**A15 found 4.0 s with no change from 13.5 s, inside b04.** The prediction is now a visible three-way choice (A6: commit before reveal).

Cues added in `script.json`, without changing any spoken text:
- c42 on "More";
- c43 on "less";
- c12 re-pointed to the option chip on the second "same".

The option chips:
- The chips read "more", "less" and "same". They are literal fixture strings under `display.ui.options`, bound with data-fx, and asserted in compute.py.
- They land on the result sheet. The title lane is full: the headline chip rows span y 260–440, measured. The 2 V | 4 V grid steps aside on "More", and the board and the table keep every given visible.
- They hold still through the think window. Only the existing focus ring is active there (`motion_in_think: []`).

At the reveal:
- On the reveal's "More" (b05 start), a teal ✓ chip and a halo land on "more", and the other two chips fade.
- On "four" (c13), the chips hand the sheet back to the grid showing 0.40 A.

**Fix after looking.** The tick covered the "e" of "more", so I moved it clear.

**Frames inspected:** 012.50, 013.50, 014.82, 015.50, 017.00, 017.40, 018.22, 018.68 and 019.50.

**Fields changed in `script.json` (no spoken text changed, so nothing is re-billed):**
- `tail_s` and `outro.tail_s` are now 0.9 s.
- Pauses moved to the middle of their PD-01 bands, because clip trimming removed 2.6 s of hidden silence:

  | Pause | Was | Now |
  |---|---|---|
  | b04 think_choice | 1.8 s | 2.0 s |
  | b10 think_calc | 2.7 s | 3.0 s |
  | Lands after b03, b05, b09, b11 | 0.5 s | 0.6 s |
  | Inspect after b07 | 0.8 s | 1.0 s |
  | Joins | — | unchanged |

**Checks:**
- `check_script.py`: `planned 60.85 s (target 60 ± 1) | planned silence 14.3%`, `OK`.
- `check_pd_script.py`: `OK`.
- `compute.py`: `fixture OK (script closure checked)`.
- `build_scene.py`: lint `{'files': 1, 'errors': 0, 'warnings': 0, 'ok': True}`, gates `[]`.
- `preview_scene.py`: exit 0, `errors: 0 | blocking: 0`.
- `qa_scene.py`: `PASS | purity 9/9 | errors 0 | blocking 0`.
- `brand_check.py`: pass.

## b07 stillness and the b13 tag (final render QA, 16 Oct 2026)

**A15: b07 sat still for 3.5 s from 22.5 s.** No spoken text changed.
- Cue c21 ("ten") now targets the R chip, `r_label`. The scene adds a pad-24 halo there.
- Cue c22 ("ohms") keeps its 10 Ω term on the result sheet. The scene adds pad-16 halos on the two V ÷ I cells in the table, which landed on "over" (c20).
- The chain is now: c20 at "over" (the ratio transform and the table cells), c21 at "ten", c22 at "ohms", then the definition card at c23 ("Ohm's"). No gap is longer than 3 s.
- Frames inspected: 023.00, 024.50, 024.80, 026.00, 026.20, 026.75.

**A19: b13 ran at 182 wpm.**
- I changed its tag from `[warm]` to `[calm]`. The text is identical ("Try the free lesson on Ohm's law.", 33 characters), so only that beat is re-billed.
- The direction sheet lists `[warm]` for the close, but `[warm]` is what produced the rushed delivery. `[calm]` is the sheet's slow tag (125–135 wpm, formula and exam lines).
- The sheet also says not to tag two same-intention beats in a row; `[calm]` follows b11's `[warm]`, so that rule still holds.

**Pauses.** On this pass, `script.json` carried the narrated pause values: think 1.8 s and 2.7 s, lands 0.5 s, inspect 0.8 s. They were left as found, so `check_script` now plans 59.75 s.

**Checks:** `build_scene` lint ok and gates `[]`; `preview_scene` exit 0 with 0 blocking; `qa_scene` PASS with purity 9/9 and no motion in the think windows; `brand_check` pass; `check_script` OK; `check_pd_script` OK.
