# Style guide: paper-collage-vertical ("Paper-Cutout Storybook Collage", 9:16)

**Style ID:** `paper-collage-vertical` | **Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot; not yet validated on real phones
**Derived from:** [V4-MP], the "Paper-Cutout Storybook Collage" style guide inside the RandomAI master prompt (verbatim local copy: `12_advanced_animations_with_claude/00_reference_videos/master_prompt_paper_collage.md`). That guide targets 16:9 at 1920×1080. This file is a full adaptation to ExamLeaf 1080×1920, not a crop (#49).
**Machine-readable twin:** `style_tokens.json` (`styles["paper-collage-vertical"]`). If this file and the JSON disagree, the JSON is a bug; fix it and bump the version.

**Evidence labels:** [V#]/[N#] are cited from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement. [Hypothesis] = plausible, untested; test in the pilot. "verify" = a fact this guide could not confirm. Edge cases are cited as #1–#65 (report §8). Project decisions are cited as RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## 0. How to read this guide

**Tags on every rule.**
- **KEPT**: the value and meaning are copied from [V4-MP] unchanged.
- **ADAPTED**: changed for ExamLeaf. The original value is given as "was: ..." and the reason as "why: ...".
- **ADDED**: no counterpart in [V4-MP]; needed by ExamLeaf's rules (accuracy, accessibility, determinism, locale, cost).

**Where this style may be used.** Illustrative and narrative scenes only: hooks, analogies, history-of-science stories, recap endings (report §4.1, §9 item 3). Any scene tagged `data-bound` by `examleaf-storyboard-route` (axes, values, equations, structures, labelled diagrams) is NOT drawn in this style. It is built by the SVG/Manim/molecule/biology skills from validated fixtures, and the collage may only frame it (a paper sheet around a fixture-driven panel). A collage scene that shows a science element treats that element as data-bound: geometry comes from the fixture and no wobble, boil, tear, sway or camera effect touches it (#12, #64).

**Cost class.** Tier A (code-only paper shapes, zero credits) is the default. Tier B (own or licensed cutouts) costs only licensing. Tier C (Higgsfield-generated cutouts and backgrounds) is credit-bearing and only runs after the storyboard gate with a credit estimate (#41, #42, #47). See §12.

**Locale.** Launch locale is en-IN only until the W3 medium decision (RD-26). The Hindi/Hinglish/Assamese text rules in §13 are written now so that they are ready, but they are inactive until the locale gate passes.

## Digest (read this first; the full guide governs on conflict)

1. 1080×1920, 30 fps, flat head-on paper diorama. No 3D, gloss, photoreal, heavy blur or glow.
2. Stacked zones inside the platform-safe box: title (top), visual (middle), accessible caption (bottom). Insets come from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them. Side margin at least 96 px.
3. Cutouts: watercolour + coloured-pencil look, white die-cut border 6-12 px, two-layer shadow `0 9px 7px rgba(74,48,22,0.30)` + `0 2px 1.5px rgba(0,0,0,0.20)`.
4. 13-colour storybook palette for artwork. Science-bearing text uses ExamLeaf tokens on an `#F7F9FC` tag, never storybook colours on cream.
5. Three kinds of text only: ransom-note titles (Latin letters per tile; Indic per word), Caveat Brush punchlines (Indic: wipe per word), small labels on washi-taped tags. Short text only.
6. Motion: back.out(2-3) pops pivoting at the feet, power3.out sheets, expo.out whips, ~~boil at 10 fps~~ boil at the tokens' `motion.boil_fps` (8) (16 Oct 2026), finite repeats, seeded PRNG, seek-driven timeline. Reveals land on, or 0.05 s before, the spoken word, times read from the cue sheet.
7. Narration is the Super Teacher's (130-155 wpm, five modes), not a storybook narrator. Storybook warmth only in hooks and recaps.
8. House loudness -16 LUFS integrated, true peak at most -1 dBTP. No music under reasoning.
9. Image models never draw text, numbers, formulas or labels (#54). Number tags on storyboard grids are added in code.
10. Forbidden: infinite repeats, Math.random/Date.now, full-frame flashes, camera effects during label reveals, per-code-point Indic animation, unlicensed or scraped images, stereotypes.

---

## 1. The look in one sentence

**[KEPT]** A hand-made paper collage in a children's-storybook register. Every character and prop is a watercolour and coloured-pencil illustration cut out of paper, with a thin white die-cut border and a soft drop shadow, layered flat on textured paper backgrounds (cream watercolour paper, kraft cardboard, watercolour washes, torn-paper strips). Motion is snappy and playful, like stop-motion, with ransom-note typography, hand-lettered punchlines and pencil doodles.

**[ADAPTED]** For ExamLeaf the audience is Class 10-12 (roughly 15-18 years old) revising for an exam. The look keeps its warmth but the register is "storybook for teenagers", not nursery. why: ROOT/03 forbids baby talk and infantilising tone; the look must never undercut the exam seriousness. [Hypothesis] Keep faces simple and proportions chunky but not toddler-like; test with students.

**[ADDED]** The look never carries science. Everything a learner must read as a fact (labels, numbers, units, formulae, arrows with direction, graph shapes) is a code-built overlay from a fixture (the accuracy invariant, report §9; #12, #54).

## 2. Materials and surfaces

### 2.1 Cutouts

- **[KEPT]** Each character or prop is a separate watercolour and coloured-pencil painting, showing paper grain, soft pigment blooms and loose pencil outlines.
- **[KEPT]** Every cutout has a clean white paper border following its silhouette, like a die-cut sticker: **6-12 px** at rest.
  - **[ADDED]** Measured in output pixels at 1080 px frame width (the 16:9 original's "1080p" and our 1080-wide frame share the same pixel density, so the number is unchanged). Because the border is part of the asset or a code stroke, it scales with the sprite during a pop-in; the 6-12 px check applies at rest scale.
  - **[ADDED]** A generated or painted cutout is rejected if the measured border is outside 6-12 px, if it has a halo, or if its alpha edge is jagged.
- **[KEPT]** Under every cutout, a soft warm drop shadow with two layers:
  - layer 1: `0 9px 7px rgba(74,48,22,0.30)`
  - layer 2: `0 2px 1.5px rgba(0,0,0,0.20)`
  - **[ADDED]** Implementation hint [Recommendation]: stack two `drop-shadow()` filters so the shadow follows the sprite silhouette (`box-shadow` would follow the rectangle). Put the filter on a wrapper and the sway/rotation on the child so the light direction stays fixed (downwards) while the sprite sways.
- **[ADDED]** Provenance: every cutout has an entry in the job's assets manifest (source tier A/B/C, licence or generator job ID, prompt text, SHA-256). Unknown provenance is rejected.

### 2.2 Full-frame backgrounds

All background types in [V4-MP] are **[KEPT]**; all are **[ADAPTED]** to portrait 1080×1920, opaque, and free of any text or pictorial science. why: #49, #54.

1. Cream cold-press watercolour paper with faint fibres, a soft warm vignette and a few faint pencil sparkle doodles in the corners.
2. Brown kraft cardboard or handmade fibrous paper with flecks, used as a pinboard for taped "photos" and paper tags.
3. Watercolour skies: pale blue and cream with loose painted clouds; deep navy night with white splatter-paint stars; gloomy charcoal soot for somber moments; warm amber for dramatic moments.
4. Landscapes built from layered torn-paper strips (hills, ground, sea) with ragged white torn-fibre edges and a slight shadow between layers.

**[ADAPTED]** Portrait composition rules for backgrounds:
- Strips stack vertically: sky at the top, 2-4 torn strips toward the bottom. Keep the title zone and the caption zone visually quiet (low detail, low contrast pattern) so text sits on controlled surfaces (§5.5).
- The caption zone sits on a solid plate (`#F7F9FC` or paper white `#FBF7EE`) added in code, not directly on the artwork. why: contrast has to be measurable (§3.2).
- Corner sparkles and torn edges may bleed to the full frame. Platform UI will cover part of the frame, so nothing that matters sits there (#51).
- **[ADDED]** Navy night and charcoal soot are illustrative backdrops, not a dark theme. RD-27 (light theme only at launch) is unaffected. Text on them is paper white or cream only (13.3:1 and 12.1:1, §3.2), and science labels never sit directly on them: place the label on an `#F7F9FC` tag.
- **[ADDED]** Darkest backdrops (navy, soot) appear only in a sheet transition that takes at least 0.9 s (§9), never as a hard cut from a cream scene (#56).

### 2.3 Craft-table props

**[KEPT]** Washi-tape strips (pink, mustard or teal, semi-transparent) holding photos and tags; cream paper tags and labels; polaroid-style photo cards with thick bottom borders; paper confetti squares and torn paper scraps.
**[ADDED]** All are built in code (SVG/CSS/Canvas), seeded, and need no image model. Tape never covers text on the tag it holds.

### 2.4 Flatness

- **[KEPT]** Everything is flat and seen head-on, like a paper diorama photographed straight on. Avoid 3D rendering, glossy gradients, photorealism, and heavy blur or glow.
- **[ADDED]** Depth comes only from layering, shadows and parallax of flat layers (§7.3). No perspective camera, no real 3D.

## 3. Colour palette

### 3.1 The storybook palette (all 13 hexes)

**[KEPT]** All 13 named colours, unchanged. Contrast ratios below are **[ADDED]**, computed for this guide with the WCAG relative-luminance formula against the listed backgrounds (recompute in `examleaf-anim-qa` on actual frames).

| Name | Hex | On cream `#f3ecdf` | On paper white `#fbf7ee` | On kraft `#b98f5e` | On night navy `#1b2a4a` | Use as text? |
|---|---|---:|---:|---:|---:|---|
| Tomato red | `#d9483b` | 3.62 | 3.98 | 1.45 | 3.35 | Display only (at least 72 px, bold); accent fills; underlines |
| Mustard | `#e0a73a` | 1.83 | 2.01 | 1.36 | 6.61 | Only on ink or navy; never on cream/paper |
| Teal | `#2f7f7a` | 4.03 | 4.43 | 1.61 | 3.01 | Display only (large text) on cream/paper |
| Ultramarine | `#2f4fa8` | 6.37 | 7.00 | 2.55 | 1.90 | Yes on cream/paper |
| Olive | `#7c8a3c` | 3.22 | 3.53 | 1.29 | 3.76 | Fills only |
| Sage | `#9dbb8e` | 1.80 | 1.98 | 1.39 | 6.73 | Fills only; text on navy |
| Blush pink | `#f1a9a0` | 1.64 | 1.80 | 1.53 | 7.40 | Fills; cheeks; text on navy |
| Cream | `#f3ecdf` | 1.00 | 1.10 | 2.50 | 12.10 | Text on ink/navy/ultramarine |
| Paper white | `#fbf7ee` | 1.10 | 1.00 | 2.75 | 13.30 | Text on ink/navy |
| Kraft | `#b98f5e` | 2.50 | 2.75 | 1.00 | 4.84 | Fills; ink text on kraft (5.10) |
| Ink | `#2b2622` | 12.74 | 14.00 | 5.10 | 1.05 | Yes: the default storybook text colour |
| Pencil | `#3a332c` | 10.58 | 11.62 | 4.23 | 1.14 | Doodles; not small text on kraft (4.23 < 4.5) |
| Night navy | `#1b2a4a` | 12.10 | 13.30 | 4.84 | 1.00 | Yes on cream/paper |

- **[KEPT]** The overall feel is warm and muted, like gouache or watercolour on paper. Saturation is gentle; the brightest accents are tomato red and mustard.
- **[ADAPTED]** Usage budget per scene [Recommendation]: one dominant background family, at most two accent hues in the foreground, and only one element in the accent colour at a time during a beat. why: report §7.2 (dominant colour with sharp accents [N52]) and ROOT/02 D4 ("limit emphasis: one dominant highlight at a time").
- **[ADDED]** Do not rely on colour alone for meaning (ROOT/02 D4). The storybook accents sit very close in luminance, so pair colour with shape, position or a label.
- **[ADDED]** Do not use tomato crosses to mark wrong answers. A misconception is corrected by explanation, not a red cross (ROOT/02 I3). Wrong-answer markers, where a script calls for one, use ExamLeaf red `#B42318` on a tag, with the correction beside it.

### 3.2 Contrast rules for text

- **[ADDED]** Normal text: at least 4.5:1 against its immediate background. Essential non-text graphics: at least 3:1 (ROOT/02 D2; WCAG thresholds are starting requirements, not a substitute for testing frames).
- **[ADDED]** Display text (ransom tiles, brush punchlines at 72 px or larger) may use 3:1 pairs. why: a 72 px glyph on a 1080-wide master shows at 24 px on a 360-wide phone, which is the WCAG large-text size (verify the WCAG definition in QA).
- **[ADDED]** Science-bearing text uses the ExamLeaf light tokens on an `#F7F9FC` tag, so the published ratios in ROOT/02 hold exactly: ink `#14213D` 15.15, secondary `#526074` 6.06, blue `#185ABD` 6.15, teal `#087986` 4.87, amber `#9A5B00` 5.14, purple `#6E44AA` 6.48, red `#B42318` 6.23. Do not put ExamLeaf teal on cream `#f3ecdf` (4.37, below 4.5); on paper white it is 4.80.
- **[ADDED]** Check adjacent colours in the real frame, not only each colour against the background (ROOT/02 D2).

## 4. Character design

- **[KEPT]** Cute, round, chunky proportions with big heads. Small solid black dot eyes, simple curved smiles, rosy blush circles on the cheeks. Soft watercolour fills with darker pencil outlines.
- **[KEPT]** Animals and creatures follow the same rules. They are friendly and slightly comic, never scary, even in dramatic moments.
- **[ADAPTED]** Objects can have faces when it is funny (a sleepy sun, a surprised wave), but only in hook, analogy and recap scenes, and **never as the causal explanation** of a science mechanism. why: ROOT/03 §5.3 ("electrons are lazy" is the cautionary example; molecules do not "decide", enzymes do not "want"). Atoms, ions, electrons, molecules, cells and organelles never get faces in an explanation scene.
- **[ADAPTED]** Dramatic examples. was: a panicked animal with sweat drops. now: allowed for light comic beats; no humiliation or fear aimed at the learner or at a wrong answer (ROOT/02 H5: avoid humiliating error messages and threats).
- **[KEPT]** One recurring hero character with a signature outfit, identical across shots by passing an earlier image as a reference, with pose variants.
  - **[ADAPTED]** Poses. was: pointing, crying, cheering, waving. now: pointing, thinking, puzzled, checking (a tick), writing, waving, quiet-win. why: no distress modelling for a stressed audience; "cheering" only when tied to a demonstrated capability ("you can now do X"), never as generic celebration (ROOT/02 H3, ROOT/03 "no fake enthusiasm").
  - **[ADDED]** The hero is a student-age figure in a plain school-style outfit. A gamosa or other cultural accessory is optional and only with native-reviewer sign-off (§14). The hero sheet (one canonical image plus pose atlas) is stored with its SHA-256 and attached as the reference for every generation (#48).
- **[ADDED]** No real persons, no likeness of a teacher, no celebrity or brand characters.

## 5. Typography (only three kinds of text)

**[KEPT]** Exactly three kinds of text appear in artwork: ransom-note titles, hand-lettered brush punchlines, and small labels. **[ADDED]** A fourth, separate system exists but is not artwork: the accessible **caption track** (§5.5), plus **science text** from fixtures (§5.4).

### 5.1 Ransom-note titles

- **[KEPT]** Each letter sits on its own small paper square; each square has its own colour and font; slight random rotation about ±6°; some vertical jitter; a small drop shadow; some letters lowercase.
- **[KEPT]** The nine tile styles and the mixed display fonts (below). Letters slap on one at a time, about 0.04-0.05 s apart, synced to the spoken words.
- **[ADAPTED]** Scope. was: a title can be the whole opening question. now: ransom tiles carry the one to three key words of the hook (for example `CHECK THE AXES`), stacked one word per row. The full question is spoken and, if shown, goes in the caption track. why: vertical width is ~~888 px between 96 px margins~~ the width between the token margins (864 px with the current insets; 16 Oct 2026); at least 112 px tiles fit five per row.
- **[ADAPTED]** Sizes (1080-wide). Tile edge 112-148 px; glyph em 80-110 px (above the heading floor, §5.6); rotation ±6° and jitter ±8 px come from the seeded PRNG keyed by `(scene_id, tile_index)`, never `Math.random` (#17).
- **[ADAPTED]** Timing. Letters land 0.04-0.05 s apart; the whole title is complete no later than the end of its spoken words and then holds at least 1.2 s before the next major transition [N60]. Landing times are derived from `words[].t0` in the cue sheet (the first letter of a word lands on, or 0.05 s before, its onset).
- **[ADAPTED]** Latin only. Per-letter tiles apply to Latin script. Devanagari and Bengali-Assamese titles use one tile per word (a paper strip, rotation ±3°) because per-code-point animation breaks conjuncts and matras (#55, §13).
- **[ADDED]** Tile pair contrast (computed). Pairs at or above 4.5 may be used at any size; pairs marked "display" need a glyph at least 72 px.

| Tile style (letter on tile) | Contrast | Class |
|---|---:|---|
| Black (ink) tile, cream letters | 12.74 | any |
| Black (ink) tile, mustard letters | 6.95 | any |
| Cream tile, red (tomato) letters | 3.62 | display |
| Cream tile, ink letters | 12.74 | any |
| Red (tomato) tile, cream letters | 3.62 | display |
| Ultramarine tile, mustard letters | 3.48 | display |
| Mustard tile, black (ink) letters | 6.95 | any |
| Pink (blush) tile, dark-red letters | 3.42 (ExamLeaf red `#B42318`) | display; the original "dark red" is not in the 13-colour palette, use `#B42318` |
| Pink (blush) tile, blue letters | 3.89 (ultramarine) | display |
| Red polka-dot tile (tomato with cream dots), cream letters | 3.62 | display |
| Blue grid-paper tile (cream with ultramarine grid), ultramarine letters | 6.37 | any |
| Teal tile, cream letters | 4.03 | display |

- **[KEPT]** Display fonts (Latin only): Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One.
  - **[ADDED]** None of these covers Devanagari or Bengali-Assamese (assume Latin only until a glyph test proves otherwise). Licences: verify per font before vendoring; vendor the files and hash them into the render cache key (RD-23). No CDN at render time.
  - **[ADDED]** Use 3-5 different fonts in one title, not all 11 (readability on a phone). Special Elite (typewriter) and Ultra are weakest at small sizes; test on a 360-px-wide display.
  - **[ADDED]** Confusable glyphs (I/l/1, O/0) never appear on a tile that carries a number or code; numbers on tiles use the number-tag style (§5.4).

### 5.2 Hand-lettered brush punchlines

- **[KEPT]** Set in Caveat Brush in dark ink `#2b2622`, revealed letter by letter like handwriting, often followed by a red pencil double underline that draws itself on in two slightly wobbly strokes.
- **[ADAPTED]** Naming. These are "brush captions" in [V4-MP]; here they are punchlines and are **not** the accessibility caption track (#51, §5.5).
- **[ADAPTED]** Sizes. Em 64-88 px; stroke-reveal 0.4-0.9 s; underline strokes 5-6 px in tomato `#d9483b` (3.62:1 on cream, acceptable for an essential graphic at least 3:1).
- **[ADAPTED]** Indic. Caveat Brush has no Devanagari or Bengali-Assamese glyphs. Devanagari punchlines use a Devanagari-capable handwriting-style font (candidate: Kalam; verify coverage) and reveal by a left-to-right mask wipe per word, never letter by letter. Assamese has no verified handwriting font: use Noto Sans Bengali (verify the Assamese letters ৰ and ৱ) with the same per-word wipe.
- **[ADDED]** Hold at least 1.2 s after completion [N60]; Indic text holds longer (§13).

### 5.3 Small labels

- **[KEPT]** Set in Patrick Hand on cream paper tags held by a strip of washi tape; sometimes a red pencil check mark or circle draws on next to them.
- **[ADAPTED]** Size. At least 50 px (the essential-label floor, §5.6); at most four words per label.
- **[ADAPTED]** Patrick Hand is for plain words only. Any label containing a number, unit, symbol, subscript, superscript or formula uses the science-text style (§5.4). why: handwriting faces make I/l/1 and O/0 ambiguous (ROOT/02 glyphs-to-test list).
- **[ADDED]** Red pencil check marks or circles are decoration and may not "grade" anything: no check on a learner answer that the script has not revealed yet (answer-hidden rule, ROOT/03).

### 5.4 Science text (fixture-driven)

**[ADDED]** All science text is code-built from fixture fields: Noto Sans or Inter semibold, KaTeX for formulae (RD-23), ink `#14213D` on an `#F7F9FC` tag, essential size 50-54 px, formula size 63-81 px, with indices checked separately (ROOT/02 D6). A tag is a paper-white card with a die-cut border and the two-layer shadow so it belongs to the collage, but its fill is `#F7F9FC` so the contrast numbers hold. Tape never overlaps the glyphs. The text is never animated per letter and never wobbles (#64). Every such element carries `data-fx="path.to.field"` so `examleaf-anim-qa` can diff the rendered text against the fixture (contract §9). Approved on-screen text from the script bundle is staged as `display_text` and marked `data-fx="display_text.<id>"` the same way [Recommendation].

### 5.5 Caption track and text edge rules

- **[ADAPTED]** Edge margin. was: keep text about 90 px from the frame edges. now: at least **96 px** left and right (the planning-pack `safe_margin_px`, larger than 90) and always inside the left/right insets from `04_harness_contract/vertical_safe_zones.tokens.json` if those are larger. Top and bottom insets come only from that file. why: report §7.9, #51.
- **[KEPT]** On-screen text stays short: a title, a number or a punchline word, never full narration sentences.
- **[ADDED]** Maximum: ransom title 3 words; brush punchline 6 words; label 4 words.
- **[ADDED]** The caption track is accurate, selectable text from the same alignment as the cue sheet (never respelled pronunciation text), in the bottom zone, at most two lines, 50-54 px, ink on `#F7F9FC` (ROOT/02 D7). It never overlaps artwork text. It never reveals an answer before the attempt window ends. While a ransom title or punchline is animating, caption highlighting stays static (no karaoke) so there is not narration + animated diagram + equation + moving captions at once (ROOT/02 D7, #51).

### 5.6 Sizes at 1080 wide

**[ADDED]** Derived from the project tokens and RD-01/RD-18: `Displayed = Source × (360 / 1080)`. The source sizes below are the 1920-wide message-04 ranges multiplied by 1080/1920 (0.5625). The older planning-pack ranges (64-72 / 84-112 / 72-88 at 1920) scale to 36-40 / 47-63 / 40-50 and are used only as a floor for secondary, non-essential text that passes the phone test (RD-01).

| Element | 1080-wide size | On a 360-px phone | Source |
|---|---:|---:|---|
| Essential labels, captions | 50-54 px | 16.7-18 px | 88-96 × 0.5625 = 49.5-54 (RD-18: at least about 50) |
| Main equations (KaTeX) | 63-81 px | 21-27 px | 112-144 × 0.5625 |
| Headings | 59-72 px | 19.7-24 px | 104-128 × 0.5625 = 58.5-72 |
| Brush punchlines | 64-88 px | 21-29 px | display; at or above the heading floor |
| Ransom glyph em | 80-110 px | 26.7-36.7 px | display |
| Secondary text floor | 36-40 px | 12-13.3 px | v1 ranges; non-essential only |

## 6. Pencil doodles

- **[KEPT]** Drawn in ink `#3a332c` with round caps. Types: sparkle crosses in corners; "?" and "!" above characters; speed lines, impact ticks and motion arcs; dashed travel trails; "z z z" and shiver marks. They draw themselves on as strokes, or pop in and wobble.
- **[KEPT]** Decorative doodles are **3-5 px** wide.
- **[ADAPTED]** Functional doodles (a circle or tick that tells the learner where to look) are **6-8 px** wide and use ink `#2b2622`. why: a 4 px stroke is about 1.3 px on a 360-px phone. Pencil `#3a332c` on kraft is only 4.23:1, so on kraft use ink.
- **[ADAPTED]** Doodles never carry science. A hand-drawn arrow may not show the direction of a physical quantity, and speed lines may not depict a real motion the lesson measures; those come from fixtures (#64, report §7.13).
- **[ADDED]** Wobble is seeded, stepped at the boil rate (§8.4), and keyed by `(scene_id, element_id, step)`.

## 7. Composition

### 7.1 Canvas

- **[ADAPTED]** 1080×1920 (9:16) at 30 fps. was: 16:9 at 1920×1080, 30 fps. why: vertical-only decision of 15 Oct 2026, RD-16 superseded (AD-07), #49.
- **[KEPT]** Flat, straight-on camera, generous negative space, one clear idea per frame.
  - **[ADDED]** "One clear idea per frame" is the scene's single attention target (ROOT/02 B2); count unexplained relationships, not objects (ROOT/02 B3). Heuristic [Hypothesis]: keep at least 25% of the visual zone background-only.
- **[KEPT]** Build depth by layering: background, torn-paper middle layers, props, characters, and a foreground strip (hills or ferns) that characters can pop up from behind.
- **[ADAPTED]** The foreground strip sits in the bottom bleed, below or behind the caption plate; it never hides caption text.
- **[KEPT]** A subtle warm vignette over everything. **[ADDED]** Cap: edge darkening at most about 12% [Hypothesis], and contrast is measured on rendered frames, not on the flat tokens.

### 7.2 Stacked zones

**[ADAPTED]** was: a free 16:9 canvas. now: three stacked zones inside the platform-safe box.

| Zone | Share of safe-box height | Holds | Never holds |
|---|---:|---|---|
| Title | top 22% | ransom title (1-3 words), brush punchline, hook keywords | captions; fixture-bound diagram labels |
| Visual | middle 54% | hero, props, cutouts, torn strips, doodles, fixture panels framed as paper sheets, label tags | captions; full-sentence text |
| Caption | bottom 24% | the accessible caption track on a code-built plate | decorative elements over the text; brush punchlines |

- **[ADDED]** The shares mirror `zones.top_title.share`, `zones.middle_visual.share` and `zones.bottom_caption.share` in `04_harness_contract/vertical_safe_zones.tokens.json` (0.22 / 0.54 / 0.24 in token version 1.0.0); if the file changes, the file wins. The safe box itself (top, bottom, left, right insets) also comes only from that file. No inset values are stored here on purpose: exact platform pixel values are not in the verified evidence (report §7.9, §11 item 9). If the file is missing, the brief assembler blocks the brief; while `platform_insets_px.measured` is false the insets named by `applies_until_measured` (currently generic conservative placeholders) are used and recorded as provisional. The agent never guesses.
- **[ADDED]** Elastic title zone [Recommendation]: a three-row ransom title (three rows of 112-148 px tiles do not fit in 22%) may grow the title zone up to 30% of the safe-box height (at the placeholder insets in the token file the usable band is 1220 px tall, so 22% is about 268 px and 30% about 366 px), taking space from the visual zone and never from the caption zone. In that scene keep the top of the visual zone free of content.
- **[ADDED]** Horizontal band: content is centred in the band from `max(96, insets.left)` to `1080 - max(96, insets.right)`, not in the full frame (the token file's right inset is larger than the left, presumably for the platform's right-hand action rail).
- **[ADDED]** Bleed versus safe: backgrounds, torn strips, vignette, corner sparkles and sheet-transition edges may use the full 1080×1920 frame; everything a learner must read or notice stays inside the safe box (#51).

### 7.3 Depth (parallax of flat layers)

**[ADDED]** The [V2] doodle result was "flat" (report §7.12); this style fixes it with flat layers only:
- At least three layers in each illustrative scene: back (sky or board), middle (torn strips, props), front (characters, foreground strip).
- Parallax factors for a slow camera drift [Recommendation]: back 0.25, middle 0.6, characters 1.0, foreground strip 1.4. Camera drift of at most 30 px over the scene (before the parallax factors are applied), as a function of `t`, and zero while any label is revealing or a hold is active (#64).
- Overlap and ordering: each layer overlaps the one behind by at least 24 px with the layer shadow between them (§2.1).

### 7.4 Recurring layouts (vertical remap)

| Original layout (16:9) | **[ADAPTED]** vertical layout |
|---|---|
| A character bottom-left looking up at a ransom-note title | Hero at the bottom-left of the visual zone, gaze up and right toward the title stacked in the title zone |
| Photos taped to a kraft board | Kraft board fills the visual zone; two columns, up to three rows of taped cards, each rotated ±3° (seeded) |
| A row of objects appearing one per word | A column (or 2×N grid) of objects; each lands on its word onset from the cue sheet; at most five per beat |
| A big central prop with small tags around it | Prop at 55-65% of the zone width, centred; at most three tags with leader lines, labels from the script or fixtures |

## 8. Motion language (GSAP vocabulary, seek-driven)

**[ADDED]** Any tween library works if its timeline is driven by `seek(t)` and never plays; whether HyperFrames bundles GSAP is not verified (report §2.3). The vocabulary below is GSAP naming. The authoritative contract is `04_harness_contract/contract.md`.

### 8.1 Entrances and idles

- **[KEPT]** Pop-in with overshoot: from scale 0 and about ±12° rotation to full size with `back.out(2-3)`, pivoting at the bottom (the feet).
  - **[ADDED]** Duration 0.30-0.45 s [Recommendation]. Simple element transitions elsewhere stay in the ROOT/02 150-300 ms range.
- **[KEPT]** Drop-in from above with a bounce, slide-in from off-frame, hops with squash and stretch from the feet.
- **[ADAPTED]** Idle motion. was: never frozen, everything gets a gentle idle sway or bob. now: idle sway or bob of ±1.5-4° and a few pixels with a **finite** number of repeats is kept for characters and props in hook, analogy and recap scenes. It is switched off for: any fixture-driven panel or tag, any element a learner must inspect, every `hold` and `think` window, and the reduced-motion variant. why: ROOT/02 E3 (a decorative change conveys no new meaning, avoid it) and J (reduced-motion version).
- **[ADDED]** Finite repeats are computed from the scene: `repeat = ceil(DURATION / period)` so no tween ever needs `repeat: -1` (#18). The last cycle ends at the rest pose.

### 8.2 Camera

- **[KEPT]** Slow push-ins (scale 1 to about 1.03-1.04 over a scene), stepped shakes on impacts, occasional pans between stacked layers.
- **[ADAPTED]** Pans are vertical (tilt) between stacked layers. Shakes: at most 3 steps, at most 0.4 s, amplitude at most 10 px at 1080 wide [Recommendation]. why: motion sensitivity (ROOT/02 J).
- **[ADAPTED]** No camera effect (push-in, pan, shake) during measurement, axis or label reveals, or on any scene with a fixture-driven diagram (#64). Push-in pivot is the hero or the focal prop so the safe box content stays inside the safe box at the end scale.

### 8.3 Gags

All **[KEPT]**, each **[ADDED]** with an accuracy guard:
- Crowds or objects multiply (1, 2, 4, 8 ...): any count shown as a number or implying a quantity must match the narration and the fixture.
- Things tear in half along matching jagged edges and the halves fall away with scraps: only for narrative metaphors, never to illustrate dissociation, bond breaking or any mechanism.
- Paper-flip swap (scaleX 1 to 0, swap the image, 0 to 1, with a puff of confetti): never swaps a labelled science object for a different one.
- Things shrink in squashy steps.
- Photos get taped onto a board.

### 8.4 Stop-motion boil

- **[KEPT]** Stepped random jitter at 8-10 fps for shivering, nerves, crying, fire flicker and shaking ground.
- **[ADAPTED]** ~~Use **10 fps**: at 30 fps that is exactly 3 frames per step. 8 fps gives a 4-4-4-3 pattern and 9 fps a 4-3-3 pattern (verified by arithmetic), which reads as stutter. Step = `floor(t × 10)`;~~ Boil at the tokens' `motion.boil_fps` (8) in `04_harness_contract/vertical_safe_zones.tokens.json`, the single owner of the rate (16 Oct 2026). Step = `floor(t × boil_fps)`; the jitter for step `k` of element `e` comes from the seeded hash `(scene_id, e, k)`, so seeking in any order gives the same frame (#17).
- **[ADAPTED]** Boil never applies to fixture content or text, and it is off in the reduced-motion variant. "Crying" is not used on learner-facing characters (see §4).

### 8.5 Sync, snappiness, determinism

- **[KEPT]** Every reveal lands on, or about 0.05 s before, the exact spoken word it illustrates. One sentence equals one visual beat. Never put everything on screen at once; reveal it across the scene.
  - **[ADAPTED]** All times are read from `cues[].at` and `words[]` in the cue sheet; nothing is hard-coded, so regenerated narration only needs a re-aligned cue sheet (#63). One sentence = one beat applies to illustrative sentences; a sentence that only carries a fixture-driven fact is a data-bound beat built elsewhere.
- **[KEPT]** Snappy and playful: anticipation, action, follow-through. Never floaty, never corporate, no linear motion.
- **[KEPT]** Seeded randomness only, finite repeats only, and a timeline that can jump to any frame.
  - **[ADDED]** Concrete block in §15.
- **[ADDED]** Motion budget. For lessons, substantial purposeful motion of about 25-35% of runtime is the untested starting budget (ROOT/02 E2); a collage hook or recap may be denser but must be stable during holds and during the prediction window.

## 9. Scene transitions

- **[KEPT]** Default: a new full-frame paper sheet slides over the previous scene. It takes **0.5-0.7 s** with `power3.out` and settles from a slight rotation. Its torn leading edge shows white paper fibres with a drop shadow. Vary the direction each scene.
  - **[ADAPTED]** Directions. was: right, left, top, bottom. now: bottom-up and top-down are the primary directions (they use the long axis), with left and right for variety.
- **[KEPT]** Somber beats: a heavy dark sheet drops from the top (`power2.inOut`, about **0.9 s**, small settle bounce).
- **[KEPT]** Urgency: a fast whip (about **0.4 s**, `expo.out`).
- **[ADAPTED]** Explosions. was: a white flash or bloom. now: **forbidden**. Use a localised paper burst (radial confetti plus a cream sheet that scales up from the impact point over at least 0.5 s). why: #56, report §7.11; section rule G15 in `02_documentation/00_OVERVIEW_and_PRINCIPLES.md` replaces full-frame flashes. The harness tokens (`flash_policy`) ban full-frame flashes and cap flashes at 3 per second (verify against the current WCAG text); the flash QA check in `examleaf-anim-qa` has the final say on luminance thresholds. As a starting rule [Hypothesis] no full-frame mean-luminance change greater than 20% of range inside any 0.25 s window.
- **[KEPT]** Start each incoming sheet about **0.3 s** after the previous line's last word so the punchline lands. **[ADDED]** Never during a `think` hold or `pause-video`; the sheet starts after the hold ends. Never earlier than 1.2 s after a headline completes [N60].
- **[KEPT]** No exit animations: the next sheet is the exit.
- **[ADDED]** Classification: these sheet transitions are scene-level. Within a scene, simple element transitions use 150-300 ms and highlights 300-600 ms (ROOT/02 E4). This resolves the apparent clash between 0.5-0.7 s sheets and the 150-300 ms default.
- **[ADDED]** Reduced-motion variant: sheets become a 150-300 ms cross-dissolve; boil, idle, shakes and push-ins are off.

## 10. Writing style of the narration

**Who owns the words.** The script comes from the Super Teacher system and the scriptwriter skill, reviewed by science and academic approval (#11). The animation agent never writes, edits or "punches up" it. This section tells scriptwriters and brief assemblers what this style suits; it also tells the agent which sentences are one-beat candidates.

| Original rule [V4-MP] | Tag | ExamLeaf rule |
|---|---|---|
| Warm, wry, gentle storybook narrator; dry understatement, never snarky or mean | **ADAPTED** | The Super Teacher: warm toward the student, exacting about the science, playful about the problem. Storybook warmth lives in hooks and recaps (modes CURIOUS and LIGHT). Explanation is STEADY or DELIBERATE; feedback and repair is REASSURING; RD-12 adds FOCUSED for exam strategy. Never sarcastic to the learner. |
| Speaks inclusively ("we", "you") | **KEPT** | Same. |
| Hook: a big question that also appears on screen as the ransom-note title | **ADAPTED** | The hook is a genuine knowledge gap the lesson closes (ROOT/02 I1), for example "Which line has the larger resistance? Check the axes." The key words go on ransom tiles; the answer is never withheld just to extend watch time. |
| Short sentences (about 5-9 words), many fragments, periods, pauses after punchlines, asides | **KEPT** (hooks, recaps) / **ADAPTED** (explanation) | Hooks and recaps keep 5-9 words. Explanation sentences may be longer but carry one idea each and state the decision behind each step (ROOT/03). |
| Rule of three with a deflating third beat | **ADAPTED** | Allowed only as a LIGHT moment under the humour ceiling: up to 3-5 short moments, under about 25 s in total in a ten-minute lesson, zero acceptable. For a Reel of 20-60 s, at most one [Hypothesis]. The joke must end where the explanation resumes; the concept-survives test applies; it may not imply false science. |
| Facts as concrete images and comparisons, not statistics | **ADAPTED** | Comparisons come through a written analogy contract (what maps, what does not, where the explanation returns to science; ROOT/03 §3.3). Facts and numbers are only those in the approved claims. |
| At most one number per sentence | **KEPT** | Same; it also keeps cue-sheet sync clean. |
| Lists of short sensory fragments | **ADAPTED** | Fragments are fine for hooks and recaps; science content stays in full explanatory sentences. |
| Ending: a turn ("Turns out...", "But..."), then a warm, witty closing line tying back to the opening question | **ADAPTED** | Tie back to the opening question, then one independent next action ("Try the next balancing question"). No "full marks guaranteed", no mastery claim, conditional feedback only ("If your atom counts match on both sides, that supports your answer"). |
| Every sentence must work as one visual gag | **ADAPTED** | Every illustrative sentence maps to one visual beat. A gag must not replace an explanation, and decorative movement with no new meaning is removed (ROOT/02 E3). |
| Pacing about 110 wpm; shorten long pauses after recording | **ADAPTED** | 130-155 wpm for ordinary explanation, 145-165 for familiar recap, 105-125 (down to 90-120) for dense symbols (RD-10; validate other languages separately). Never shorten or remove a `think` hold, a `pause-video`, or a processing pause to hit a duration; actual audio governs. |

**Word budget for Reels** (arithmetic from 130-155 wpm, before subtracting holds): 20 s = 43-52 words; 30 s = 65-78; 45 s = 98-116; 60 s = 130-155. Subtract the prediction window (5-8 s, RD-11) and any hold.

**Beat density.** At 140 wpm a 7-word sentence takes about 3 s, so a collage beat lasts about 2-4 s. Fewer and simpler gags than the 110 wpm original.

**Mode to look** [Recommendation]:
- CURIOUS: pop-in of the title tiles, a "?" doodle, a slide-in sheet.
- STEADY: calm props, light idle only, simple sheet or hard cut.
- DELIBERATE: slower push-in, longer settle, 0.9 s sheet only if the beat is somber; no gags.
- LIGHT: one boil gag or one paper-flip, then back to calm.
- REASSURING: gentle idle only, no shakes, no crying poses.
- FOCUSED (RD-12): minimal motion, label tags, longer holds.

## 11. Sound

### 11.1 Music

- **[KEPT]** Palette: a whimsical storybook track of pizzicato strings, ukulele, glockenspiel, soft clarinet and light brushed percussion, about **100 BPM**, instrumental. One bar of 4 beats is 2.4 s, which gives bar-aligned stems that cut to any scene length.
- **[ADAPTED]** Where. was: under the whole piece. now: only in hooks (first 3 s sting or bed), sheet transitions, recap outros and Reel beds. No music under reasoning, derivations, predictions or `think` holds (ROOT/02 G5: core explanation has no background music by default; section decision AD-15 in `02_documentation/`).
- **[KEPT]** The music sits about **15-20 dB under the voice**. **[ADAPTED]** ExamLeaf uses 20–24 dB under speech (one policy since 15 Oct 2026, AD-15 addendum; beds only in hooks, transitions, recaps and outros) while narration is active, with sidechain-style ducking [report §5.4], because many viewers are second-language listeners.
- **[KEPT]** Turn it down or muffle it (low-pass) for somber moments; let it swell slightly on the end card (at most +3 dB [Recommendation]).
- **[ADDED]** Music is generated by `examleaf-audio-compose` (seeded Python, no samples without a licence) or supplied with a licence record. Trending songs and unlicensed audio are never used.

### 11.2 Sound effects

- **[KEPT]** Paper-craft SFX, subtle: soft paper swishes for sheet transitions; light taps for ransom letters; cartoon pops when cutouts appear; a boing for hops; a paper-tear sound when things tear; a thud for drops; a sparkle chime for magic moments.
- **[ADAPTED]** Bigger booms and rumbles. was: only for real drama. now: only in history-of-science narrative scenes, short and band-limited, never under learner-critical narration.
- **[ADDED]** No SFX during `think` holds, `pause-video`, equation reading, or inspection. One tap per ransom letter is too busy at 0.04-0.05 s spacing: play one tap per word (SFX placed by `sfx[]` in the cue sheet).
- **[ADDED]** SFX one-shots are placed from the cue sheet at `at` with `gain_db`; the agent does not hard-code times.

### 11.3 Loudness

- **[ADAPTED]** Final loudness **-16 LUFS integrated (±1) and true peak at most -1 dBTP**. was: about -14 LUFS and peaks below -1.5 dBFS. why: the ExamLeaf narration system masters at -16 LUFS / -1 dBTP (`05_narration_system/INSTRUCTIONS_narration_pipeline.md` and `04_video_engine/planning_pack_v1/design_tokens.json`); these are internal targets, not platform law. Two-pass loudness normalisation on the final mix, re-measured after the final mux (#39). Do not normalise individual scene stems separately.

## 12. Generating the image elements

**[ADAPTED]** The whole section is gated: raster generation (Tier C) happens only after the approved storyboard, under a credit ledger, through `examleaf-mcp-orchestrator`. Higgsfield credits are deducted for every agent generation on any plan, and there is no native credit cap (#41, #42; [N33][N34]).

### 12.1 Asset tiers

- **Tier A** (default, zero credits): paper shapes, torn strips, washi tape, confetti, simple props drawn in SVG/Canvas with seeded wobble and procedural paper texture.
- **Tier B**: cutouts painted or licensed by ExamLeaf; each with a licence record.
- **Tier C**: Higgsfield GPT Image cutouts and backgrounds (the [V4-MP] model ID `gpt_image_2_5` is cited from the master prompt; verify the current ID and options in the tool). Needs an approved estimate first.

### 12.2 Cutouts

- **[KEPT]** Transparent background, 2K, high quality. Single isolated object, centred, whole object visible with generous margin, flat straight-on view, no cast shadow, no ground, no scenery. Attach the approved storyboard grid or an earlier cutout as a reference for consistency. Trim the transparent margins before use.
- **[ADAPTED]** Prompt template (ExamLeaf wording):

```text
Paper-cutout sticker asset for a stop-motion collage, on a FULLY TRANSPARENT
background. Hand-painted watercolour and coloured-pencil storybook
illustration, cut from watercolour paper with a thin clean white paper
border (6-12 px at 1080 px width) following the whole silhouette. Single
isolated object, centred, whole object visible with generous margin, flat
straight-on view, no cast shadow, no ground, no scenery.
NO text, NO letters, NO numerals, NO symbols, NO labels, NO logos, NO
watermarks, NO signatures anywhere in the image. No real people. No
photorealism.
Palette: tomato red, mustard, teal, ultramarine, olive, sage, blush pink,
cream, kraft, ink. Round friendly design, small black dot eyes and rosy
cheeks only where the brief says the object has a face.
Match the character design of the attached hero reference sheet.
SUBJECT: <one concrete object or pose, no science labels>
```

- **[ADDED]** Post-checks (code): alpha present, margins trimmed, border 6-12 px measured, no text detected by an OCR or glyph check (#54), SHA-256 stored with the prompt, generator job ID and credit cost in the ledger.

### 12.3 Backgrounds

- **[KEPT]** Opaque. Types: blank textured cream watercolour paper; blank kraft cardboard; watercolour skies with layered torn-paper hills (no characters); navy starry night with white splatter stars; sooty charcoal sky with a torn-paper ground strip.
- **[ADAPTED]** 9:16, at least 1080×1920. Ask for a 9:16 image if the tool offers it; otherwise generate larger and crop to 9:16, never stretch, never outpaint invented content (see `ShortSpec.layout_strategy = reflow`). Keep the top 22% and bottom 24% low-detail for title and caption. No text of any kind.

### 12.4 Storyboard grid

- **[ADAPTED]** was: one 16:9 image with 3×3 panels, thin cream gutters and a small number tag on each panel. now: one image with 3×3 panels, **each panel 9:16** (a 3×3 grid of 9:16 panels is itself 9:16), thin cream gutters, one panel per beat in order.
- **[ADAPTED]** The **number tags are added in code** after generation, not drawn by the image model (#54). Panels for data-bound beats are drawn as blank placeholder cards ("science fixture goes here" is added in code), so the grid is science-free (see `06_prompts_and_templates/storyboard_request.md`).
- **[ADDED]** The default grid is code-rendered thumbnails (zero credits); a Higgsfield grid is a look-development option, only with approval.

### 12.5 Built in code, never generated

- **[KEPT]** Ransom letters, captions and tags; washi tape, confetti and doodles; underlines; screens and simple interface elements.
- **[ADDED]** All science labels, numbers, units, formulae, arrows with direction, graph or diagram shapes, and the accessibility captions.

## 13. Hindi, Hinglish and Assamese text rules (locale-gated, RD-26)

**[ADDED]** Inactive until the locale gate passes; written now so the style is ready. All language drafts need native-speaker and subject review (ROOT/03 §5.5); do not scatter regional expressions only to signal identity.

1. **Fonts.** Devanagari: a Noto-class family (Noto Sans Devanagari, Noto Serif Devanagari) or another font with verified full coverage. Assamese (Bengali-Assamese script): Noto Sans Bengali, with the Assamese letters ৰ (U+09F0) and ৱ (U+09F1) verified. Latin technical terms inside Indic lines use the Latin font. Verify coverage with a glyph smoke test; never trust a family name. Vendor and hash the fonts (RD-23).
2. **Smoke-test strings** (shaping check only, not teaching content): `क्ष ज्ञ श्र द्ध विद्युत प्रतिरोध` and `ৰ ৱ ক্ষ জ্ঞ অসম`. Render each statically and as the end state of the animation; the two must be pixel-identical (end-state equality test).
3. **Animation unit.** Per word or per grapheme cluster, never per code point (#55). Treat `Intl.Segmenter` grapheme segmentation of Indic conjuncts as [Hypothesis] to be tested in the pinned headless Chrome (report §11 item 10); until it passes, animate per word.
4. **No letter-spacing** and no `text-transform` on Indic text; do not disable ligatures; no synthetic bold or italic for Devanagari (use a real bold weight).
5. **Line height** at least 1.4 for Devanagari and Bengali-Assamese (matras above and below) [Hypothesis].
6. **Ransom tiles.** Word-level paper strips, not letter tiles. **Brush punchlines.** Mask wipe per word.
7. **Mixed script.** Hindi captions in Devanagari with technical terms in Latin script (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md`, step 12). Hinglish in Latin script is allowed when the script was authored that way; do not mix scripts inside a word. Mark each element with the correct `lang`.
8. **Numerals.** Science numbers use Latin digits unless the approved edition says otherwise; never mix digit systems in one expression.
9. **Holds.** At least 1.2 s for Latin headlines [N60]; Indic headlines hold longer: multiplier 1.5 [Hypothesis], tuned in phone tests.
10. **Captions.** From the original script and alignment, not from pronunciation respellings (same PLAYBOOK).

## 14. Indian setting cues and the no-stereotype rule

**[ADDED]** Setting cues are context, not costume. They make the world feel like the learner's: Assam, tea gardens, the Brahmaputra, river islands, paddy fields, bamboo, monsoon rain, school canteens, bicycles, local fruit and food. Use them in backgrounds, props and analogy settings.

Rules:
1. No stereotype. Characters are not defined by ethnicity, region, occupation or class. No tea-garden labourer as a comic or pity figure, no accent or dialect jokes, no tribal or festival costume used as a costume, no poverty or caste cues, no religion-coded imagery unless the lesson is about it.
2. No claims. A background is not a fact source: no measurements, names or statistics from art. Any factual statement about a place comes from the approved claims.
3. Analogies from familiar settings still need an analogy contract (what maps, what does not, where it returns to science). A river is not a circuit; the contract must say where the picture breaks.
4. Native Assamese reviewer sign-off for any cultural accessory (for example a gamosa) and for any region-specific wording.
5. Do not assume one Indian language or shared lifestyle (ROOT/03 master prompt).
6. No humour targeting the learner's marks, accent, appearance, family, caste, religion, gender or finances (ROOT/03 §5).

## 15. Determinism block

**[ADDED]** Concrete rules for scene code in this style. The harness contract (`04_harness_contract/contract.md`) is authoritative; this section only adds what the style needs.

1. Scene exposes `window.DURATION` (seconds, equal to the cue sheet `duration`) and `async window.seek(t)`; frames = `DURATION × 30` [N72]. The renderer seeks and never plays [N68].
2. Every visual state is a pure function of `t` [N61]: no `Date.now()`, `performance.now()`, `setInterval`, `requestAnimationFrame` loops, wall-clock CSS animations or autoplaying video.
3. Randomness is stateless and keyed, so seek order cannot change a frame:

```js
// [Recommendation] stateless seeded random in [0,1); order-independent.
function fnv1a(s){let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,0x01000193)}return h>>>0}
function mulberry32(a){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296}
const rnd=(key)=>mulberry32(fnv1a(key));        // rnd(sceneId+':'+elementId+':'+step)
```

4. Boil step `k = floor(t × boil_fps)` (~~`× 10`~~; boil at the tokens' `motion.boil_fps` (8), 16 Oct 2026); jitter = `rnd(sceneId:elementId:k)`.
5. Timeline tweens are built paused and set by `seek(t)`; every repeat is finite and computed from `DURATION`.
6. Fonts and images are preloaded; `seek` resolves only after fonts and images are ready (a first-frame font swap is a defect). The renderer rejects remote URLs.
7. Video-heavy scenes: one worker (#20). The collage uses still images and sprites, so this rarely applies.
8. Double render of the same scene must give identical frame hashes; QA enforces it (#17).
9. Pin the effort level in the brief (default high for scene code, #1) and never ultracode (#3, #4).

## 16. Forbidden list

1. Text, numbers, symbols or formulae drawn by an image model (#54).
2. Any 3D render, glossy gradient, photoreal image, heavy blur or glow (original rule, kept).
3. Infinite repeats (`repeat: -1`, `infinite` CSS) (#18); wall-clock or unseeded randomness (#15, #17).
4. Full-frame flashes and rapid luminance changes (#56).
5. Camera effects during measurement, axis or label reveals (#64).
6. Per-code-point animation of Indic text (#55).
7. Cropping a 16:9 composition into 9:16 (#49); text outside the safe box (#51).
8. Altering, paraphrasing or adding narration or on-screen wording; researching facts; any science glyph without a fixture field (#11, #12).
9. Face-and-voice imitation of a real teacher; invented teacher history.
10. Unlicensed, scraped, or reference-creator artwork; copying another creator's characters (a reference video is for analysis numbers only).
11. Trending or unlicensed music; voice cloning.
12. Reading folders other than the job workspace (#9); "don't stop until perfect" loops (#60); more than the iteration cap.
13. Stereotypes (§14).

## 17. QA checklist for this style (`examleaf-anim-qa`)

- [ ] Frame size 1080×1920, 30 fps, DURATION equals the cue sheet; lint passes with zero errors.
- [ ] Double-render frame hashes identical.
- [ ] Text and fixture glyphs inside the safe box; caption zone free of artwork text.
- [ ] Contrast of every text pair at least 4.5:1 (display pairs at least 3:1 with glyphs at least 72 px); essential graphics at least 3:1.
- [ ] Essential text at least 50 px; equations 63-81 px; indices checked.
- [ ] Hold times: headlines at least 1.2 s (Indic at least 1.5×); equations until narration ends + 0.5 s and at least 2 s after an important transformation (RD-02).
- [ ] Rendered text equals fixture fields (DOM text dump or OCR).
- [ ] No flash: luminance check passes. Reduced-motion variant renders.
- [ ] Die-cut borders measure 6-12 px; shadows match the two-layer values.
- [ ] Loudness -16 LUFS ±1, true peak at most -1 dBTP, measured after the final mux.
- [ ] No music under reasoning; no SFX during `think`.
- [ ] Assets manifest complete: tier, licence/job ID, hash, prompt.
- [ ] No stereotype flags from the native reviewer.

## 18. Edge cases handled in this guide

#7 (structured brief via digest and paste block), #8 (named fonts and palette), #9 (isolation, §16), #10 (audio rules, §11), #11 (script ownership, §10), #12 (fixtures, §0 and §5.4), #15-#18 (§15), #39 (§11.3), #41/#42 (§12), #47 (§12.4), #48 (§4), #49 (§7), #50 (§5.1, §5.2, §13), #51 (§5.5, §7.2), #54 (§12), #55 (§13), #56 (§9), #60 (§16), #63 (§8.5), #64 (§8.2).

## 19. Changelog

- 1.0.0 (15 Oct 2026): first full adaptation of [V4-MP] to 1080×1920.
