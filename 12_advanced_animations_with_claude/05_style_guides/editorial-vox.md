# Style guide: editorial-vox (editorial explainer, comparisons and scale stories, 9:16)

**Style ID:** `editorial-vox` | **Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot
**Derived from:** the Vox-style editorial look in [V3] (RandomAI, the sun-versus-planets orchestrated demo in Remotion), report §4.3 and §7. "Vox-style" names a technique (textured backgrounds, cut-outs, highlighters, serif and sans headlines, number callouts). This style uses no logo, wordmark, colour scheme or exact layout of any named outlet and must never be presented as one (see §12).
**Machine-readable twin:** `style_tokens.json` (`styles["editorial-vox"]`).

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement; [Hypothesis] = untested; "verify" = not confirmed. Edge cases #1-#65 (report §8). Project decisions RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## Digest (read this first; the full guide governs on conflict)

1. Use for comparisons and scale stories whose numbers come from validated fixtures: matched A/B cases, one-unit-versus-tenfold ideas, orders of magnitude. Not for graphs, equations or labelled structures (those are data-bound).
2. Textured `#F7F9FC` paper, licensed or own cut-outs with a keyline and a flat hard shadow, highlighter strokes, a bold serif headline mixed with a sans supporting line, big number callouts, slow push-ins.
3. Every number, unit, ratio and label is a fixture field. Sizes and positions are computed from fixture values by a pure function of `t`; the encoding (length, area, log or linear) is declared and shown.
4. 9:16 layout: A over B in equal matched frames, a divider, a common scale; or a vertical ladder for orders of magnitude.
5. Palette: ExamLeaf light tokens only; highlighters are 22-28% tints of those accents. Light theme only (RD-27).
6. Fonts: Noto Serif family for headlines (Devanagari and Bengali variants), Noto Sans/Inter semibold for support, tabular numerals for callouts. Banned as display: Arial, Inter, Space Grotesk, system-ui.
7. Images: ExamLeaf-owned or recorded-licence only. No scraping, no model-made photoreal, no real faces without a release, no maps unless an approved asset.
8. The script comes from the narration system, never from the agent ([V3]: the AI-written script was the weak point).
9. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px; captions in the bottom zone.
10. Motion: one staggered entrance per beat [N53], slide/push-in/wipe, no flashes, no camera effects during label reveals; reduced-motion variant required.

---

## 1. What this style is for

[Recommendation, report §4.3] Comparisons and scale stories driven by validated numbers, in the illustrative or narrative layer of a lesson or Reel:
- Two matched cases with one thing changed (same solution, two pH values; same circuit, two voltages).
- Orders of magnitude (a ladder of sizes, amounts, times), a "this is how big a tenfold step is" visual.
- "Tempting reading versus actual reading" contrasts built on a single numeric fact.

It is the right choice when the scene's job is "see the ratio", and the wrong one when the job is "read the axis" (SVG/Manim), "see the structure" (molecule/biology skills), or "feel the story" (collage).

**Accuracy invariant.** Any glyph that encodes science is traceable to a fixture field (report §9). The editorial look must not distort what the numbers say (report §7.13): a push-in must not hide a unit, a highlighter must not obscure a digit, a decoration must not change a ratio.

## 2. The look in one paragraph

A quiet textured paper background, a few cut-out subjects with a thin white keyline and a flat offset shadow, one bold headline that mixes a heavy serif for the claim words with a sans for the connecting words, a very large number with its unit, a highlighter swipe on the single phrase that matters, and slow, deliberate push-ins. Everything is flat and head-on; depth is by overlap and shadow only. It should feel like a well-edited explainer, not a template.

## 3. Materials and surfaces

- **Background.** `#F7F9FC` with a static procedural grain (multiply, 3-5% opacity, fixed seed) and an optional halftone dot band (dots at least 6 px, ink at 6-8% opacity) behind the title zone only. Light theme only at launch (RD-27). No dark slabs; a dark panel is a tinted `#14213D` card with paper-white text only if the QA contrast check passes and the brand owner approves.
- **Panels.** Cards in an 18% tint of one accent (§4) with ink text. Pale highlight area with dark text rather than a large saturated block (ROOT/02 D4).
- **Cut-outs.** A subject with its background removed (mask supplied with the asset), a **6 px white keyline** and a **flat hard shadow** offset 8 px right and 8 px down at ink 18% opacity, no blur. [Recommendation] This differs from the collage's soft two-layer shadow on purpose, so the two styles read as different.
- **Illustrations.** Flat vector illustrations created in code or supplied under a recorded licence.
- **Depth.** Overlap plus the hard shadow. At least three layers (background, panel, subject) [Recommendation].

## 4. Palette

Tokens from `02_learning_psychology/palette_and_typography_tokens.json`:

| Role | Hex | Contrast on `#F7F9FC` |
|---|---|---:|
| Background | `#F7F9FC` | n/a |
| Ink | `#14213D` | 15.15 |
| Secondary | `#526074` | 6.06 |
| Blue | `#185ABD` | 6.15 |
| Teal | `#087986` | 4.87 |
| Amber (condition or caution) | `#9A5B00` | 5.14 |
| Purple | `#6E44AA` | 6.48 |
| Red (error marker only) | `#B42318` | 6.23 |

- **Dominant plus accent** [N52]: ink and paper dominate; one accent per scene (the subject accent: Physics blue, Chemistry teal, Mathematics purple, Biology green `#1F7A3E` as a proposed new token, contrast 5.09:1, needs brand-owner approval).
- **Highlighter** = a multiply-blended 22-28% tint of an ExamLeaf accent: 28% tints blue `#B9CCEA`, teal `#B4D5DB`, amber `#DDCDB5`, purple `#D1C6E5`, green `#BBD5C7`. Ink on each is at least 9.8:1 (computed). Amber is used only when the highlighted phrase is a condition.
- **Compare** with two accents (A and B): pair colour with a letter, position and a shape. Accent pairs are close in luminance (blue/purple 1.05, teal/green 1.05 computed), so colour alone never tells A from B (ROOT/02 D4).
- Identity stable: a quantity keeps its colour across scenes.

## 5. Typography

All fonts vendored, hashed, licence-checked before use (RD-23). No CDN at render time. Licences: verify.

| Role | Family (candidate) | Latin | Devanagari | Bengali-Assamese |
|---|---|---|---|---|
| Headline claim words | Noto Serif (Bold or Black) | yes | Noto Serif Devanagari (verify) | Noto Serif Bengali (verify ৰ ৱ) |
| Connecting words, sub-heads | Noto Sans semibold | yes | Noto Sans Devanagari (verify) | Noto Sans Bengali (verify) |
| Labels, captions | Inter (Latin) or Noto Sans | yes | as above | as above |
| Number callouts | Noto Sans or Inter with tabular figures | yes | Latin digits unless the edition says otherwise | Latin digits unless the edition says otherwise |

- **Mix rule.** One headline per scene, at most 2 lines. The 1-3 key claim words go in the serif at 96-128 px; connecting words go in the sans at 56-64 px, baseline-aligned. This is the "bold serif plus sans" mix from [V3].
- **Sizes (1080-wide)**, derived from RD-01/RD-18 (message-04 ranges × 0.5625): essential labels and captions 50-54 px; headings 59-72 px minimum; equations 63-81 px; the editorial headline claim words 96-128 px (display); number callout 160-240 px with its unit at 56-72 px.
- **Tabular figures** (`font-variant-numeric: tabular-nums` where the font provides them; verify) so a changing number does not jitter.
- **Ban as display:** Arial, Helvetica, Roboto, system-ui, Space Grotesk [N51][N55], Inter as a headline face.
- **Indic.** Per word or per grapheme cluster, never per code point (#55); line height at least 1.4; no letter-spacing; end-state equality test (`paper-collage-vertical.md` §13).
- **Glyph tests:** I/l/1, O/0, minus signs, decimal points, subscripts, superscripts, Greek letters.

## 6. Layout in 1080×1920

Stacked zones inside the platform-safe box (insets only from `04_harness_contract/vertical_safe_zones.tokens.json`; do not invent them; the assembler blocks the brief if the file is missing; while `platform_insets_px.measured` is false its `applies_until_measured` insets are used and the job manifest records them as provisional):

| Zone | Share of safe-box height | Holds |
|---|---:|---|
| Title | top 22% | headline (serif plus sans mix), kicker line |
| Visual | middle 54% | the comparison, ladder, cut-outs, number callouts |
| Caption | bottom 24% | accessible caption track on an `#F7F9FC` plate, at most 2 lines, 50-54 px |

Side margin at least **96 px**.

**Comparison layout** (matched views with a common scale, ROOT/02 E1): two equal frames, A above B, 40-46% of the visual zone height each, separated by a divider labelled "vs" or an operator drawn in code. Same scale, same units, same frame size; the thing that differs is the only thing that differs.

**Ladder layout** (orders of magnitude): a vertical axis with ticks at each order; objects sit at their fixture value; the axis is **logarithmic** unless the fixture says linear, and the on-screen note says which. Each tick label is a fixture field.

## 7. Number callouts and scale integrity

1. **Source.** The numeral, unit and descriptor are strings from the fixture (for example `value_display`, `unit_display`), each element marked `data-fx="path.to.field"` (contract §9). The agent does not round, reformat or localise them.
2. **Show the encoding.** Declare how a number maps to size: length, diameter, area or volume. If a visual is area-proportional, the on-screen note says so. If it is not to scale, the on-screen note says "not to scale". These notes are text from the brief or fixture (`encoding_note`), not typed by the agent.
3. **Pure function.** Positions and sizes are computed from fixture numbers by a pure function of `t`; no hand-tuned pixel values that imply a ratio.
4. **Range.** If values span more than three orders of magnitude, use the log ladder. Do not draw a tiny object as a speck without a callout.
5. **Reveal, don't count up.** Prefer a mask-wipe or a pop over a count-up; intermediate numerals of a count-up are decorative and could be misread. A count-up is allowed only for non-exam-critical magnitudes, at most 0.8 s, and must land on the exact fixture string (note it in `scene_notes.md`).
6. **Units** are always shown beside the number; the minus sign and decimal point are tested glyphs.
7. **Ratios are fixture fields.** "Tenfold" or "100 times" on screen is a fixture field, never an inference by the agent (#12).

## 8. Motion vocabulary

All values are [Recommendation] starting points; simple transitions stay at ROOT/02's 150-300 ms and highlights at 300-600 ms.

| Move | Spec |
|---|---|
| Staggered entrance | One orchestrated entrance per beat [N53]: group items enter with 60-90 ms stagger; `power3.out`; 0.3-0.5 s total |
| Slide | `power3.out`, 0.30-0.50 s |
| Pop (cut-out, number) | scale 0.85 to 1 with `back.out(1.4)`, 0.30 s |
| Highlighter | left-to-right multiply swipe, `power2.out`, 0.35-0.50 s, seeded rough ends, two passes allowed |
| Underline / box | draw-on 0.30-0.40 s |
| Push-in | scale 1.00 to 1.05-1.08 over a beat, pivot at the focal point; ends before a label reveal or measurement |
| Cuts | hard cut on a sentence boundary, or a 150-300 ms slide; no whip pans, no flashes (#56) |
| Idle | none by default; a 1-2 px drift is allowed on cut-outs with finite repeats |

- **No camera effects during label reveals or measurement** (#64). A push-in must never be running while a number or unit is revealing.
- **Minimum size at the smallest scale.** Because a push-in scales text up, size text for scale 1.00.
- **One dominant highlight at a time** (ROOT/02 D4).
- **Sync.** A reveal lands on, or about 0.05 s before, its word; times from `cues[].at` and `words[]`; one sentence is one beat; nothing hard-coded (#63).
- **Holds.** Headlines at least 1.2 s [N60] (Indic longer, multiplier 1.5 [Hypothesis]); an important comparison holds 2-4 s, longer when needed (RD-02); equations until narration ends plus 0.5 s.
- **Reduced motion.** No push-in, no drift, highlighters appear by fade.

## 9. Images, licensing and provenance

1. Allowed sources: ExamLeaf-owned or commissioned art; assets with a recorded licence that permits commercial educational use.
2. Not allowed: scraped or screen-grabbed images; reference-creator artwork (a reference video is for analysis numbers only); model-generated photoreal; real persons' faces without a release; logos; maps (political boundaries are sensitive) unless an approved asset is supplied.
3. Each asset has a manifest entry: source, licence ID or terms, attribution text if required, hash, date.
4. Image models never draw text, numerals or formulas (#54); all text is code-built.
5. If Tier C generation is used for a cut-out (credits), it follows the gate in `paper-collage-vertical.md` §12 and the estimate/approval rules in `06_prompts_and_templates/`.

## 10. Sound

- Light, short SFX placed from the cue sheet: soft thud when a number lands; highlighter swipe; slide whoosh; tick on a divider. Gains set in the cue sheet; no SFX during `think` or equation reading.
- Music: optional for a Reel, off under reasoning (ROOT/02 G5); a bed in the hook or outro only.
- Loudness -16 LUFS integrated (±1), true peak at most -1 dBTP after the final mux (#39).

## 11. Writing

The script comes from the narration system. Editorial writing patterns that fit the Super Teacher voice (ROOT/03):
- **Claim, compare, so what.** State what is being compared, show the matched cases, then say what the difference means in the model.
- **State the decision.** "We keep the solution the same and change only the pH" (ROOT/03: reveal the instructional decision).
- **One number per sentence** [V4-MP rule retained; it keeps sync clean].
- **Conditional wording** for feedback; no promised marks; no "everything you know is wrong" headlines.
- **No personification as causal explanation** (ROOT/03 §5.3).
- Humour is optional; zero is acceptable.

Example hooks that suit the style (CSV ID in the tracker): 11 "One pH unit: one small change?"; 21 "Double a length, what happens to the area?" (the response numbers it 13; the CSV ID is the stable one); 1 "Does twice the voltage ALWAYS mean twice the current?" (when the comparison panel is the point). Each still needs science review.

## 12. Do and don't

**Do**
- Compute every size from a fixture value.
- Keep A and B frames identical in size and scale.
- Declare and show the encoding (length, area, log, linear, not to scale).
- Keep a clean unit beside every number.
- Record image provenance.

**Don't**
- Use any outlet's logo, wordmark or exact look; call the output "Vox".
- Hand-tune a size so a ratio looks nicer.
- Run a push-in or highlighter over a number while it reveals (#64).
- Highlight more than one phrase at a time.
- Use a red cross for a wrong reading; correct by explanation (ROOT/02 I3).
- Add full-frame flashes (#56).
- Let the agent write the headline copy: the headline is script or approved on-screen text (#11).

## 13. Cost

- Credits: zero unless Tier C cut-outs are approved (then the estimate and ledger rules apply, #41, #42).
- Render: CPU, no WebGL. Images are stills.
- Tokens: unmeasured [Hypothesis]; log in the pilot.

## 14. QA checklist (`examleaf-anim-qa`)

- [ ] 1080×1920, 30 fps; DURATION equals the cue sheet; lint zero errors; double-render hashes identical.
- [ ] Safe box respected; captions in the bottom zone.
- [ ] Every rendered number, unit and label equals a fixture field.
- [ ] A and B frames equal size and scale; encoding note present when needed.
- [ ] Contrast at least 4.5:1 for text, 3:1 for graphics; ink on highlighter at least 4.5:1.
- [ ] No camera effect during reveals; no flashes; reduced-motion variant renders.
- [ ] Asset manifest complete; no unlicensed images.
- [ ] Loudness -16 LUFS ±1, true peak at most -1 dBTP.

## 15. Edge cases handled

#8 (named fonts and palette), #11 ([V3] weak script), #12 (§1, §7), #17-#19 (determinism as in the collage guide §15), #49 (§6), #50 (§8), #51 (§6), #54 (§9), #55 (§5), #56 (§8), #60 (via brief), #63 (§8), #64 (§8).

## 16. Changelog

- 1.0.0 (15 Oct 2026): first version.
