# A2: Visual explanation and animation audit (three Opus videos)

Auditor A2, 16 Oct 2026. Evidence: 1-fps frames in `audit/frames/` (540×960 files; sizes below are at 1080×1920). I opened every physics frame (t001–t072) and the frames around every scene boundary, the hook, the think window and the ending in chemistry and biology. Root causes come from `16_pilot_builds_2026-10-16/<subject>/opus/` (storyboard, scenes, build_notes), `05_style_guides/` and `vertical_safe_zones.tokens.json`. Full records are in `A2_findings.json` (19 findings: 2 critical, 12 major, 5 minor).

## 1. Verdict

The screen does not hold one explanation. Each video is five separately built slides joined by hard cuts. Each slide starts empty, draws itself while the voice is already talking, and is thrown away at the next cut. The science on screen is correct and fixture-bound, and several single moments are strong. What the videos lack is continuity: one diagram that stays put while only the quantity that matters changes. The explanation also fills only 17–29% of the frame, and the three videos look like three channels.

## 2. Persistence and resets (A2-01, A2-02, A2-03, critical/major)

| Video | Object lifecycle (frame evidence) |
|---|---|
| Physics | The circuit holds from 4–22 s. At 22.4 it is replaced by two empty cards (t022→t023). At 46.3 the cards give way to a loop *with a gap*, an open circuit, for 3.5 s (t047–t049). At 57.4 the board is cleared (t057), then a lone zigzag shows (t059–t060), then a checklist. |
| Chemistry | The molecules hold from 3–21 s. At 21.5 they are replaced by a separate atom ledger (t021→t023). At 49.2 the screen cuts to a blank page with a divider (t050). At 59.8 the equation and molecules are rebuilt. |
| Biology | The representation changes five times: tree (t006), polaroid choices (t012), seedling with equation (t020), *empty sky* (t040–t041), pot with pie (t047), small tree with equation (t056). |

**Root cause.** `render/concat.txt` hard-cuts independent `s0N.mp4` files, and each `s0N.html` owns its own L3 markup. The kit card's rule "carry the previous scene's end state" (physics `build_notes.md` §4 rule 4) is prose only. The contract has no state hand-off, and QA checks A1–A10 have no persistence or empty-screen check. Every element of a new scene is a reveal target cued to a later word (for example, physics s04 `bulb <- filament`), so each scene opens blank. QA passed all three anyway.

**Fix.** Build one persistent board per video. Beats add, change or remove named elements, and a removal must state a reason. Add a frame-0 rule: the carried board is visible at the start of every beat. Add the QA gates `persistence_check` (hero-element IoU ≥ 0.8 across beat boundaries unless an explicit replace event exists), `empty_middle_seconds = 0`, and a closed-loop check for circuit fixtures.

## 3. Hook frame, staged builds, slow writing (A2-04, A2-05, A2-06, major)

- **Hook, 0–3 s.** Physics t001 shows an empty board and a pencil, and t002 shows "twice the". Chemistry t001 shows only a halftone band, and its question "Did an atom vanish" first appears at **t011**. Biology t001 shows empty sky and ground. The cause is that every on-screen word is revealed at its spoken `t0` (`s01.html buildHeadlines`, tokens `motion.reveal_rule`), and the hook object is cued to a word seconds later (physics `circuit <- current`, 3.3 s, then drawn over about 1.2 s). No rule requires frame 0 to carry content.
- **Staged builds.** In physics the circuit is useful only at about 8 s and the ratio cards only at about 31 s (empty cards at t023, rows written word by word from t024 to t031). Stroke draw time is `Math.min(1.2, Math.max(0.25, len/1100))` for every stroke (s01 runtime). Chemistry builds its equation formula by formula (t002–t009).
- **Word-by-word headlines.** Physics s03 reads "the current" for 9 s with a hole where "twice" lands (t025–t031), because `data-words="twice:2 the:1 current:1"` uses the second spoken "twice". Other fragments: "That constant" (t041), "always is" (t048), "Did an atom", "plants", "carbon". The headline becomes a karaoke copy of the audio instead of a claim.

**Fix.** Use a hook component: frame 0 shows the whole question object plus the full question. Set a reveal budget: structure appears whole in ≤ 300 ms, only the changing value animates, and draw-on is allowed only when drawing *is* the mechanism. Headlines are pre-composed claims of ≤ 5 words, shown whole and timed by word matching. Add the QA gates `time_to_useful ≤ 1.5 s` and "no partial headline visible > 0.5 s".

## 4. Causal role of each visual change (A2-12, major)

- **Physics.** At t010→t011, V = 2 V is replaced *in place* by 4 V (scene-spec `swaps`). That destroys the state the learner must compare, and the cards later rebuild both states. At t055, "×2" is struck through but the ammeter stays blank and no lamp current appears. The fixture `FIX-ohm-two-points` has no lamp values, so the exception is asserted, not shown.
- **Chemistry.** The s01 molecules are not the atoms counted in s03. A separate ledger re-encodes them as small circles, which the external audit also flagged.
- **Biology.** The 40% pie (t047–t051) is a mass-fraction detour. The missing causal image is a tracer that follows carbon from air to leaf to glucose to wood.

**Fix.** Use a CompareStates verb (before and after side by side, kept). Every change cue must declare `changes` (the quantity) and `because` (the beat). A misconception beat must change a fixture value on screen. Add lamp fixture data and a carbon-tracer component.

## 5. Frame share and legibility (A2-07, A2-08, A2-18, major/minor)

- **Measured share of the frame.** In physics the board is about 904×574 px (25% of the frame), the circuit ink about 17%, and everything below y≈1200 is empty in 60 of 72 frames. In chemistry the ledger is about 930×450 (20%), and the lower 45% is empty from t023 to t049. In biology the art is about 26–29%, and the rest is decorative bleed.
- **Cause.** The tokens use *placeholder* insets: top 250, bottom 450, `measured:false`. With shares of 0.22/0.54/0.24, the middle zone is y 518–1177, only 27% of the frame area. The caption lane is reserved for captions that were never drawn (physics build_notes §6).
- **Legibility.** The biology glucose formula uses Unicode subscript code points ("C₆H₁₂O₆" in the fixture). At 72 px the subscripts are about 20 px tall, about 7 px on a 360 px phone (t038, t060). The chemistry ledger atoms are circles about 36 px wide. The token minimums cover only labels, equations and headings, with no subscript floor.
- **Crowding.** The "constant temperature" chip straddles the board edge and the shelf (t036), and V = I × R sits on the board's bottom edge (t044).

**Fix.** Measure the insets. Make the diagram area ≥ 45% of the frame, and give the caption lane back to the diagram when captions are not burnt in. Use one formula component (KaTeX or `<sub>` ≥ 0.65 em, ≥ 40 px rendered). Add the QA checks `content_area ≥ 40%` and `glyph_size`, plus an overlap detector.

## 6. Colour semantics (A2-09, major)

- **Physics.** Voltage, current and resistance are all ink. Blue marks the underline, the ×2 arrows and the ticks. Amber marks both a condition ("constant temperature") and a change ("R ↑").
- **Chemistry.** Teal carries five roles: oxygen atoms, "=", coefficients, the tick and the panel tint. Amber marks "≠".
- **Biology.** Tile colours vary word by word. Red, the error token, sits on "air" (the correct answer) and on "food".
- **Across videos.** Teal means oxygen in one video and decoration in another.

**Root cause.** `doodle-handdrawn.md` §1 item 3 says "Subject accents decorate; they never encode a quantity". `editorial-vox.md` §4 allows one accent per scene. The palette has hue names but no roles.

**Fix.** Define semantic colour roles in the tokens: voltage, current, resistance, changed, condition, mismatch, and the elements H, O and C. Each role keeps one hue across all subjects, and each hue carries one role per video. Add a role-colour lint.

## 7. Identity, typography, decoration, transitions (A2-10, A2-11, A2-16, A2-17)

**Three identities: a mistake for a brand (critical).** Physics is a doodle notebook with a pencil, a shelf and a comic-like headline (Chalkboard SE as a fallback, because Kalam is not vendored; README §12). Chemistry is editorial, with a halftone band and serif/sans claims. Biology is a storybook collage with ransom tiles and washi tape. They differ in background, headline system, layout grammar and motion character. The cause is that `brief.md` line 9 assigns a style per subject and the README tie-breaker (2) allows "one illustrative style per lesson", with no brand layer above. For "Professor Diki Simplified" this must become one system.

**Typography.** Physics headlines leave widows ("resistance" t042, "voltage" t064). Biology headlines use 5 tiles across 4 faces, above the 3-word cap in paper-collage §5.1.

**Decoration with no meaning.** The shelf of books, the pencil, hatch shadows, boiling board outlines and underline, paper grain, the halftone band, torn strips, corner sparkles, washi tape, polaroids, the kraft board and ransom-tile colours all carry nothing. The physics circuit is also statically wobbled: `pathD(..., WOBBLE_AMP=1.6)` is applied to every stroke, including `#circuit`, against README Rule 0 ("never wobbled").

**Transitions.** All are hard cuts. Biology's background strips change layout at every cut (t006→t008, t018→t020), and no transition expresses a relation.

## 8. Think window, recap, final 2 s (A2-13, A2-14, A2-15, A2-19)

- **Think window.** Chemistry is good: halos on the O atoms and brackets per side (t018). Physics shows the static circuit with "I = ?" (t019) and no visual for the second ask, "whether always is safe". Biology asks about carbon but shows soil, water and air with no carbon (t016). The same "Pause. Predict." plate appears in all three for a fixed 5 s (`think_window_s 5`).
- **Recap.** Chemistry's recap is a real summary: the balanced equation, molecule copies equal to the coefficients, and H 4 = 4, O 2 = 2 (t063). Physics drops the 2→4 V, 0.2→0.4 A result and the lamp boundary, leaving ticks, the equation and a bare zigzag (t061–t072). Biology shrinks the tree and repeats the equation without the carbon path (t056). The cause is the kit's recap archetype ("ticks, disclosure.lines"), with recaps built from scratch.
- **Final 2 s.** All three end on a static frame reading "AI-generated narration / script by ExamLeaf", with 2.2 s of silence. There is no Professor Diki Simplified mark and no closing question (contract §3 disclosure text).
- **Chemistry worked step.** The headline "never created or destroyed" stays up while the equation is balanced, and "Balanced" is shown only by a 50 px tick (t049).

**Fix.** The recap is the final state of the board, with the changed quantity highlighted plus one result line (QA: ≥ 70% of explanation elements present). The think frame shows the givens and an answer slot. The end card runs ≤ 1.5 s with the brand mark and a transfer question. Add an OCR gate that fails on "ExamLeaf".

## 9. What the visuals do well (keep)

- Every number on screen comes from a fixture, so there are no hallucinated values (QA A3).
- Physics: the ×2 arrows between paired states, "V / I = 10 Ω" in *both* cards, an equation that holds after it is read, and the condition shown as a chip.
- Chemistry: the coefficient pops into the equation and the tally updates at once (= teal, ≠ amber, t038–t047). The H₂O₂ vs 2H₂O side-by-side with the changed subscript highlighted (t058) is the strongest teaching image of the set.
- The think windows freeze motion and hide the answer. The chemistry halos and brackets scaffold the count.
- Misconceptions are corrected by explanation, never with a red cross. There are no flashes, contrast is high, and text stays inside the margins.
- Biology's stoma magnifier and the roots with water drops tie inputs to plant parts. The pie wedge geometry is fixture-driven.

## 10. Unified visual direction for one brand (≈200 words)

**One board, three lanes.** A fixed **diagram area** (about y 380–1340, ≥ 45% of the frame) holds one persistent object per video: circuit, equation-with-atoms or plant. It never leaves; it changes. A **result area** below it (y 1340–1520) carries the running result: "I = 0.4 A", "O: 2 = 2", "6 C from CO₂". A slim **title lane** above it shows one claim of ≤ 5 words, whole, never word by word. The caption lane exists only when captions are burnt in.

**One type family.** One vendored sans (e.g. Inter or Noto Sans, 600/800) for everything, plus KaTeX for math. Headings 64–80 px, labels ≥ 52 px, equations ≥ 72 px, subscripts ≥ 40 px.

**Semantic colour.** Ink and paper by default. Fixed roles across subjects: voltage blue, current teal, resistance amber-brown, "changed" as a highlight, mismatch red only, and fixed element colours.

**Motion verbs only.** Place, ChangeValue, CompareStates, TracePath, SwapPart, Highlight, EquationTransform, PauseForPrediction. Use 180–300 ms reveals and 400–900 ms transforms, with no draw-on of structure and no cuts.

**Drop.** Per-subject styles, boil, wobble on science, the pencil, the shelf, halftone, washi tape, ransom tiles, polaroids, decorative bleed, word-by-word headlines and on-screen "ExamLeaf". Close on a 1.5 s Professor Diki Simplified end card.
