# Judging summary (unblinded)

| Subject | Lens | Totals by tier | Winner | Dimensions by tier | Empty middle-zone seconds |
|---|---|---|---|---|---|
| biology | pedagogy | opus 19; haiku 14 | opus | opus {'D1': 5, 'D2': 5, 'D3': 4, 'D7': 5}; haiku {'D1': 4, 'D2': 3, 'D3': 4, 'D7': 3} | - |
| biology | visual | opus 17; haiku 12 | opus | opus {'D4': 4, 'D5': 4, 'D6': 5, 'D7': 4}; haiku {'D4': 2, 'D5': 3, 'D6': 4, 'D7': 3} | opus 6; haiku 11 |
| chemistry | pedagogy | haiku 13; opus 19 | opus | haiku {'D1': 3, 'D2': 3, 'D3': 4, 'D7': 3}; opus {'D1': 5, 'D2': 4, 'D3': 5, 'D7': 5} | - |
| chemistry | visual | haiku 12; opus 15 | opus | haiku {'D4': 2, 'D5': 3, 'D6': 5, 'D7': 2}; opus {'D4': 4, 'D5': 4, 'D6': 3, 'D7': 4} | haiku 8; opus 1 |
| physics | pedagogy | haiku 14; opus 19 | opus | haiku {'D1': 4, 'D2': 3, 'D3': 4, 'D7': 3}; opus {'D1': 5, 'D2': 5, 'D3': 5, 'D7': 4} | - |
| physics | visual | haiku 10; opus 15 | opus | haiku {'D4': 2, 'D5': 2, 'D6': 4, 'D7': 2}; opus {'D4': 4, 'D5': 3, 'D6': 4, 'D7': 4} | haiku 11; opus 5 |
| physics_pd | craft | diki_v2 31; opus 15 | diki_v2 | diki_v2 {'D1': 4, 'D2': 4, 'D3': 4, 'D4': 4, 'D5': 4, 'D6': 3, 'D7': 4, 'D8': 4}; opus {'D1': 3, 'D2': 2, 'D3': 2, 'D4': 2, 'D5': 2, 'D6': 1, 'D7': 2, 'D8': 1} | diki_v2 0.6; opus 13.8 |
| physics_pd | pull | diki_v2 33; opus 16 | diki_v2 | diki_v2 {'D8': 4, 'D1': 5, 'D2': 4, 'D3': 4, 'D4': 5, 'D5': 4, 'D6': 3, 'D7': 4}; opus {'D8': 1, 'D1': 4, 'D2': 2, 'D3': 2, 'D4': 2, 'D5': 2, 'D6': 1, 'D7': 2} | diki_v2 0.6; opus 13.6 |
| physics_pd | teaching | diki_v2 34; opus 16 | diki_v2 | diki_v2 {'D1': 5, 'D2': 4, 'D3': 4, 'D4': 5, 'D5': 4, 'D6': 3, 'D7': 5, 'D8': 4}; opus {'D1': 4, 'D2': 2, 'D3': 2, 'D4': 2, 'D5': 2, 'D6': 1, 'D7': 2, 'D8': 1} | diki_v2 0.0; opus 8.4 |
| physics_v2 | pedagogy | opus 17; haiku_v2 14 | opus | opus {'D1': 5, 'D2': 4, 'D3': 4, 'D7': 4}; haiku_v2 {'D1': 4, 'D2': 3, 'D3': 4, 'D7': 3} | - |
| physics_v2 | visual | opus 17; haiku_v2 14 | opus | opus {'D4': 4, 'D5': 4, 'D6': 5, 'D7': 4}; haiku_v2 {'D4': 2, 'D5': 4, 'D6': 5, 'D7': 3} | opus 8.0; haiku_v2 4.5 |

## Gap rules proposed by the judges (for the weaker build)

- **biology/pedagogy:** misconception.confront must carry its evidence inside the beat (a fixture value or the worked count), not a bare 'that idea fails', and must state the full why_wrong from the graph node (water and minerals) _(02 pedagogy rules, misconception.confront slot; SCRIPTING_REGISTRY §15 misconception example)_
- **biology/pedagogy:** a worked.step that balances an equation ends by stating the inference it licenses for the objective (e.g. only CO2 carries carbon, so glucose's carbon came from air) _(SCRIPTING_REGISTRY §15 worked.step template)_
- **biology/pedagogy:** recap.statement restates the one idea already taught; no first appearance of a new number; percentages name their basis ('by mass') _(02 pedagogy rules, recap.statement; SCRIPTING_REGISTRY §15 number phrasing)_
- **biology/pedagogy:** hook.question_reveal opens on the surprise/scale image and the question, not a teaching statement ('Green plants make their own food') _(02 pedagogy rules, hook.question_reveal example)_
- **biology/visual:** Headlines must be ransom-note tiles (one tile per letter or word, 1-3 words, landing on words[].t0 - 0.05), never plain sans text _(05_style_guides/paper-collage-vertical.md §5.1 and Digest item 5: add a worked HTML example and a QA check that fails a headline without ransom tiles)_
- **biology/visual:** Every illustrative scene needs at least three textured layers (wash or kraft background, torn-paper strips, die-cut cutouts with washi-taped tags); a plain cream fill fails _(paper-collage-vertical.md §2.2, §7.3 and the §17 QA checklist (add a 'style recognisable' item))_
- **biology/visual:** No empty middle zone longer than 1 s: the scene opens with its anchor prop already in place, and the outro keeps the recap visual under the disclosure _(paper-collage-vertical.md §8.5 and §9 (scene openings and the outro), plus an empty-zone check in examleaf-anim-qa)_
- **chemistry/pedagogy:** A worked.step that balances an equation must change one coefficient at a time, say the element that moves, and recount on screen after each change. The fixture must compute and expose every intermediate state (e.g. results.step1) so the tally updates on the coefficient's anchor word. _(02 pedagogy rules, worked.step slot; fixture authoring guide, 'intermediate states' section)_
- **chemistry/pedagogy:** Any on-screen count or tally must reflect the equation currently shown. When a coefficient appears, the matching tally and headline update in the same beat; a balanced equation may never sit above an unbalanced tally. _(Storyboard/scene authoring guide, state-consistency rule; QA A3 (fixture-equals-screen) extended to check the state)_
- **chemistry/pedagogy:** Chemical formulas must render subscripts as real lowered subscripts (fixture 'parts' with a 'sub' field, rendered as <sub> or an offset span), never as Unicode ₂ in a font that draws it on the baseline. Coefficients must be full-size and in the accent colour. _(editorial-vox style guide, typography: chemical formulas; brief template 'display strings' line)_
- **chemistry/pedagogy:** misconception.confront should both show why the trap looks right (e.g. the counts match for H2O2) and show the evidence that it is wrong (a different molecule or name), side by side with the correct fix. _(02 pedagogy rules, misconception.confront slot, with a worked example)_
- **chemistry/visual:** Chemical formulas use real subscript markup (<sub>, or verified U+2080-2089 glyphs) with digits at 60-70% size and lowered at least 0.25 em. Old-style or proportional figures are banned in formulas. The QA glyph test renders H₂O, 2H₂O and H₂O₂ at 1080 width and fails if a subscript bottom sits on the baseline. _(12_advanced_animations_with_claude/05_style_guides/editorial-vox.md §5 Typography (Glyph tests bullet) and §14 QA checklist)_
- **chemistry/visual:** Every element that encodes state (tally counts, circles, the =/≠ relation, the highlight) is a pure function of the current equation state. When a coefficient appears, the tally re-derives from results.<state> on the same cue, and a 'short' highlight is removed once its row balances. _(editorial-vox.md §7 Number callouts and scale integrity (new item 8) and §8 Motion vocabulary, Sync bullet)_
- **chemistry/visual:** Minimum look per scene: grain background, halftone band behind the title, tinted panel card with a flat 8/8 hard shadow, and at least three depth layers. Support text in Noto Sans or Inter, never a system fallback. A scene on plain paper only fails the style check. _(editorial-vox.md §3 Materials and surfaces and §14 QA checklist)_
- **chemistry/visual:** The middle visual zone is never empty for more than 0.5 s. Each scene opens with its visual on the first anchor word, the outro keeps the recap visual under the disclosure, and a scene headline persists across its beats until the next headline replaces it. _(editorial-vox.md §6 Layout in 1080x1920 and §8 Holds bullet; mirror in 04_harness_contract/vertical_safe_zones.tokens.json hold_times_s)_
- **physics/pedagogy:** A misconception.confront beat must show the counter-example in the same setup as the worked example (here the lamp swapped into the same circuit) with at least one fixture-bound change glyph (for example 'R ↑', a struck '×2') revealed on the causal words. A bare icon with only a headline does not count as evidence. _(15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md §3 (Slot sources, misconception.confront row) and 12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md (storyboard gate checklist))_
- **physics/pedagogy:** When the brief names a condition (for example constant temperature), the condition must be a fixture display string that appears on screen on the word where it is first spoken, and again in the recap visual. Speaking it is not enough. _(15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md §15 (Script QA checks), as a new check: condition glyph present)_
- **physics/pedagogy:** In concept_intro, the confront beat's first sentence answers the predict prompt's open half verbatim ('always is not safe'), and the hook puts the question in the first 3 s, before the setup. _(15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md §4 (Script grammar per format, concept_intro) and §9 (hook scripting))_
- **physics/pedagogy:** No scene may hold an empty hero container for more than 1.5 s while science is being spoken. The first cue of each beat must land within 1 s of its first content word. _(12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md (cue timing rules))_
- **physics/visual:** The middle visual zone must never sit empty or decoration-only for more than 0.5 s inside a beat. If the first cue word comes more than 1 s after the beat starts, carry the previous panel over or reveal a lead element on the beat's first word. QA samples the middle zone at 2 fps and fails a run of more than 0.5 s with no explanatory ink. _(05_style_guides/doodle-handdrawn.md §7 (Sync) plus §14 QA checklist; examleaf-anim-qa as a new check A10)_
- **physics/visual:** Ship a doodle scene skeleton with L1 shelf, L2 tinted board with hatch shadow and L4 cropped pencil already built, and require the hook headline in Kalam or Caveat at 96-140 px (QA fails a headline whose font-family is Inter or another sans). _(05_style_guides/doodle-handdrawn.md §3 (Depth rules: worked template) and §5 (Fonts), with 04_harness_contract/scene_template.html)_
- **physics/visual:** Every relationship or equation the narration states must appear on screen on its word, and a misconception scene must show the evidence (the changed quantity with an arrow chip, and the struck shortcut) instead of an isolated prop. _(05_style_guides/doodle-handdrawn.md §9 (Reel structure table: 'Doodle's job' column) and §11 Do/Don't)_
- **physics/visual:** The muxed MP4 must contain the timeline's pre-roll, so video duration equals timeline total_duration_s within 1 frame and no reveal starts before its word minus reveal_lead_s. QA extracts frames at cue-0.2 s and fails if the element is already visible. _(04_harness_contract/contract.md (seek/mux section) and examleaf-anim-qa check A9)_
- **physics_pd/craft:** Keep one persistent circuit from frame 0 to the end: put the 2 V / 4 V cards and the V/I row beside it and swap the lamp into the resistor's slot instead of redrawing in scenes s03–s05.
- **physics_pd/craft:** Make frame 0 complete (circuit, R = 10 Ω, V = 2 V, I = 0.2 A, question chip) and finish the hook question by 3 s; b01 is 27 words and the question ends near 4.0 s.
- **physics_pd/craft:** Show the baseline current before the predict, ask a choose-type 'more, less or same?' with the options on screen, drop 'decide whether always is safe', and cut the 5 s silent hold to about 2 s with a ring on I = ?.
- **physics_pd/craft:** Add a transfer (e.g. 6 V across the same 10 Ω) with a think window, the worked answer on the board and spoken feedback.
- **physics_pd/craft:** Delete the spoken and on-screen 'AI-generated narration; script by ExamLeaf' line; close on the brand end card and the free-lesson line.
- **physics_pd/craft:** Colour by meaning (V blue, I teal, R/Ω amber, a red strike on a labelled 'I × 2'), use the empty lower 40 % of the frame for a structured card tied to the circuit, and drop the decorative pencil and books.
- **physics_pd/craft:** Rewrite in short contrastive sentences with one quotable line, add energy marks and purpose-labelled pauses[], and trim to 60 ± 1 s with silence under 15 %.
- **physics_pd/pull:** Complete frame 0: show the circuit with R = 10 Ω, V = 2 V and a live 0.20 A meter reading, put the question on screen, and finish speaking it by 3 s. Show 'Here is a resistor of ten ohms with two volts across it' in the picture instead of narrating it.
- **physics_pd/pull:** Make the prediction answerable from the board: show the 2 V current first, make it a quick choice (more / less / same) with a short think plate instead of a 5 s silent 'Pause. Predict.' hold, and either drop 'decide whether always is safe' or put its givens on the board.
- **physics_pd/pull:** Keep one persistent board: grow a V | I | V ÷ I table under the circuit and swap the bulb into the resistor's slot, instead of tearing down to empty cards, a bare loop and a lone squiggle.
- **physics_pd/pull:** Name the payoff on its word ('Ohm's law' with a definition card) and give it a short contrastive line a student would repeat.
- **physics_pd/pull:** Add a transfer on the same board (same resistor, 6 V, what does the meter read?) with a think window and a confirmation.
- **physics_pd/pull:** Remove the spoken and on-screen 'AI-generated narration; script by ExamLeaf' (PD-20, F01). Close on a recap card, a next step and the brand end card.
- **physics_pd/pull:** Cut to 60 ± 1 s with short contrastive sentences (b01 and b04 are 27 words each), keep silence under 15 %, and land a turn every 8-12 s (today the gaps are 23.8 s and 25.5 s).
- **physics_pd/teaching:** Delete b07: no 'AI-generated narration' and no 'ExamLeaf', spoken or on screen; close on the brand end card and a free-lesson line instead.
- **physics_pd/teaching:** Keep one persistent circuit from frame 0 to the end card: put the V, I and V/I values beside the meter (or in a table under it) instead of replacing the circuit with cards, and swap the lamp into the resistor's slot instead of redrawing the loop.
- **physics_pd/teaching:** Make the prediction answerable: show the meter at 0.2 A for 2 V before switching to 4 V, ask more / less / same, cut the hold from 5.5 s to about 2 s and reveal 0.4 A on the meter straight after; drop 'decide whether always is safe' or ask it only once the bulb is on the board.
- **physics_pd/teaching:** Add a transfer (same resistor at a new voltage, I = ?) with a short think window and feedback on the board.
- **physics_pd/teaching:** Land a usable idea before 10 s (the 2 V, 10 Ω, 0.2 A reading at frame 0) and give an intuition before the terms; turn textbook sentences ('current multiplied by resistance', 'resistance is the constant ratio') into short spoken lines.
- **physics_pd/teaching:** Trim to 60 ± 1 s and keep silence at or below 15 %: remove the 2.2 s dead tail and the empty-board openings of scenes 1 and 5, and put a turn every 8-12 s (B runs 31.8 s, 14.6-46.4 s, without one).
- **physics_pd/teaching:** Tie the struck '×2' in the filament beat to the current (I × 2) so a phone viewer can read what failed to double.
- **physics_v2/pedagogy:** Hook question must be the first spoken sentence and land within 0–3 s; the setup comes after it _(02 pedagogy rules, hook.question_reveal slot; SCRIPTING_REGISTRY §15 hook template)_
- **physics_v2/pedagogy:** No orphan label glyphs: every 'I =' / 'V =' on screen must carry a fixture value or an explicit '?', and an ammeter carries its 'A' symbol _(storyboard template state table + style guide doodle-handdrawn circuit kit)_
- **physics_v2/pedagogy:** Recap checklist ticks only rules that hold; the exception row uses a distinct 'fails here' mark (cross or amber), never the same tick as the law _(style guide recap.statement template)_
- **physics_v2/pedagogy:** A claim's fixture_ids are allowed only if the fixture holds values for that claim; a heating-effect claim cites its own NCERT section and carries a reliability_note _(lesson_graph schema guide, claim node rules)_
- **physics_v2/pedagogy:** Define or avoid new terms in the recap (e.g. 'ohmic'): the recap may only use words already taught _(SCRIPTING_REGISTRY §15 register l9_10)_
- **physics_v2/visual:** Add a QA check that wobble on non-fixture strokes (board, wires, frame) is 0.8-2.5 px, and fail a scene whose strokes are all straight _(05_style_guides/doodle-handdrawn.md §14 QA checklist (tie to §2.1 Wobble))_
- **physics_v2/visual:** The hero or fixture panel must fill at least 70% of the middle_visual zone height; do not put a short strip at the top of the zone _(05_style_guides/doodle-handdrawn.md §6 Layout, plus a min_fill key under zones.middle_visual in 04_harness_contract/vertical_safe_zones.tokens.json)_
- **physics_v2/visual:** L4 must be a recognisable cropped object (pencil, desk edge, hand), with a worked example; a bare line does not count _(05_style_guides/doodle-handdrawn.md §3 depth rule 1, L4 row)_
- **physics_v2/visual:** A query label carries an explicit '?' (for example 'I = ?') and is removed or filled when the value is revealed; no dangling 'I =' _(05_style_guides/doodle-handdrawn.md §10 Mixed scenes)_
- **physics_v2/visual:** The hook headline must be visible within 0-3 s even when the hook question comes late in the sentence _(05_style_guides/doodle-handdrawn.md §9 Reel structure table, 0-3 s row)_

## Blocking defects

- **biology/pedagogy/haiku:** b06 'Soil supplies water.' omits minerals, contradicting MIS-plants-eat-soil.why_wrong and implying soil gives only water
- **biology/pedagogy/haiku:** b07 'About forty percent of glucose is carbon' lacks 'by mass' (by atom count it is 25%); on screen s05 shows a bare '40%' and 'carbon' with no basis
- **biology/visual/opus:** s04 opens with about 2.2 s of empty sky (39.8 to about 42.0 s) before the pot appears; s02 has about 1.4 s of empty kraft board before the log
- **biology/visual/haiku:** Not recognisable as paper-collage-vertical (plain sans headlines, no ransom tiles, no torn or textured layers)
- **biology/visual/haiku:** About 5.4 s of empty middle zone in the outro and about 2.1 s at the s04 opening (42.3 to 44.4 s)
- **biology/visual/haiku:** s04 headline wraps with a single orphaned 'air' line
- **chemistry/pedagogy/haiku:** Subscripts render as baseline digits throughout, so coefficient and subscript are visually indistinguishable in 2H2O (s03-s05)
- **chemistry/pedagogy/haiku:** End of s03 (~40.9-42.9 s): the balanced equation shows over the stale unbalanced tally with 'Oxygen is short on the right'; no recount until s05
- **chemistry/visual/haiku:** Subscripts render as baseline digits in every formula, s01-s05 (H2O, H2O2, 2H2O).
- **chemistry/visual/haiku:** The end of s03 (about 40.9-42.9 s) shows the balanced 2H2 + O2 -> 2H2O over an unbalanced tally (O 1, 'short' highlight).
- **chemistry/visual/haiku:** The video track leads the audio by about 0.6 s at every cue (video 72.73 s vs timeline 73.33 s; e.g. tally_right at 32.13 s vs 'Right' at 32.76 s).
- **chemistry/visual/haiku:** No narration captions in bottom_caption (shared with B; the storyboard defers them to the lead).
- **chemistry/visual/opus:** QA A9: re-render is not deterministic (deterministic false).
- **chemistry/visual/opus:** The video track leads the audio by about 0.6 s at every cue (video 72.60 s vs timeline 73.20 s; e.g. coef_H2O at 36.70 s vs 'two' at 37.34 s).
- **chemistry/visual/opus:** No narration captions in bottom_caption (shared with A; the storyboard defers them to the lead).
- **physics/pedagogy/haiku:** s04 (44.3-55.8 s): the misconception is asserted, not confronted. There is no circuit, no R-change glyph and no current comparison, and an empty circle sits on screen for about 4.6 s during 'Ohm's law is always true'.
- **physics/pedagogy/haiku:** The constant-temperature condition, the one rule the brief asks the learner to remember, is never on screen. In s05, an empty card holds for about 5.8 s while the recap rule is spoken (s05_t000-t004).
- **physics/visual/haiku:** The video track runs about 0.6 s ahead of the narration: the mp4 is 73.27 s against a 73.87 s timeline, and every sampled reveal is visible before its word.
- **physics/visual/haiku:** The middle zone is empty for about 11 s (mp4 43.5-48.3 s in s04 and 55.0-60.9 s in the s05 recap).
- **physics/visual/haiku:** The recap never shows V = I × R although it is spoken, and the s05 card is static from 61 to 73 s.
- **physics/visual/haiku:** The filament scene shows no evidence: no circuit, no R-up and no current comparison.
- **physics/visual/opus:** The video track runs about 0.6 s ahead of the narration: the mp4 is 71.33 s against a 71.93 s timeline, and every sampled reveal is visible before its word.
- **physics_pd/craft/diki_v2:** transcript-vs-script check A7 did not run (STT HTTP 429): the spoken text is unverified until it is re-run
- **physics_pd/craft/diki_v2:** academic review still required for SIM-push-flow, CLM-filament and ASM-transfer-six-volts (script.json requires.review)
- **physics_pd/craft/opus:** 'AI-generated narration; script by ExamLeaf' spoken and shown (b07, 66.0–69.9 s)
- **physics_pd/craft/opus:** runtime 71.93 s
- **physics_pd/craft/opus:** board wiped three times; empty board at 0–4 s and 57.4–59.5 s
- **physics_pd/craft/opus:** no transfer, feedback, end card or CTA (qa A12, A18)
- **physics_pd/craft/opus:** 5.5 s silent predict hold; silence 17.5 % of runtime
- **physics_pd/craft/opus:** prediction asked before its givens (no baseline current; 'is always safe' unanswerable from the board)
- **physics_pd/pull/opus:** spoken and on-screen 'AI-generated narration; script by ExamLeaf.' (b07, 66.0-69.2 s; s05_t014)
- **physics_pd/pull/opus:** no transfer question
- **physics_pd/pull/opus:** board torn down three times inside the lesson (22.4 s, 46.3 s, 57.4 s); five scenes instead of one
- **physics_pd/pull/opus:** silence is 17.5 % of runtime
- **physics_pd/pull/opus:** runtime 71.93 s, outside 60 ± 1 s
- **physics_pd/pull/opus:** prediction asked without its givens: no 2 V current is shown, and nothing on the board supports 'always is safe'
- **physics_pd/pull/opus:** no brand end card: the opening ident, end-card brand line, free-lesson line and spoken outro are all missing (qa A12)
- **physics_pd/teaching/diki_v2:** Before sign-off, not a lesson defect: qa A7 did not run (STT HTTP 429), so the spoken text is unverified against the script.
- **physics_pd/teaching/diki_v2:** Before sign-off, not a lesson defect: script.requires.review asks for academic review of SIM-push-flow, CLM-filament and ASM-transfer-six-volts.
- **physics_pd/teaching/diki_v2:** Minor machine-check fails to clear: A13 (0.63 s unscripted gap at 28.8 s), A15 (3.5 s with no visible change from 22.5 s), A19 (CTA b13 at 182 wpm).
- **physics_pd/teaching/opus:** Spoken and on-screen 'ExamLeaf' and AI-disclosure line (b07, 66.0-71.9 s).
- **physics_pd/teaching/opus:** No transfer question.
- **physics_pd/teaching/opus:** Runtime 71.93 s; silence 17.5 %.
- **physics_pd/teaching/opus:** Board torn down three times (22.4, 46.3, 57.4 s); empty frame 0 and an empty board until 3.7 s.
- **physics_pd/teaching/opus:** Prediction asked without its givens; 5.5 s silent hold; answer 14 s later.
- **physics_pd/teaching/opus:** No brand end card (qa A12 lists missing end-card items); 11 of 21 machine checks fail.
- **physics_v2/pedagogy/haiku_v2:** s03–s04: a blank ammeter circle with an orphan 'I =' label that is never filled, while the cards show I = 0.2 A / 0.4 A. It reads as an unfinished equation.
- **physics_v2/pedagogy/haiku_v2:** s05 recap: the same approval tick is placed beside 'filament lamp R ↑' and beside the struck '×2'. A learner can read this as the lamp obeying the rule.
- **physics_v2/visual/opus:** Middle visual zone is an empty board for 0-3.5 s of the hook; the circuit only starts on 'current' at 3.72 s, so a scrolling viewer sees nothing explanatory at first
- **physics_v2/visual/haiku_v2:** Does not read as doodle-handdrawn: no wobble, flat rounded-rect board, L4 is a stray line at the left edge
- **physics_v2/visual/haiku_v2:** 'I =' label next to a blank ammeter left unfilled through s02-s04
- **physics_v2/visual/haiku_v2:** Circuit squashed to about 40% of the visual zone height, leaving the lower visual zone empty in s01, s02 and s04
- **physics_v2/visual/haiku_v2:** Title zone empty for the first 6.3 s of the hook
