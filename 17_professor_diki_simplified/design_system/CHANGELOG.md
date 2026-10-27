# Professor Diki Simplified design system: changelog

## v2.0.2 (16 Oct 2026): headline chips may carry six words

`type.headline.max_words` 5 → 6: a six-word claim line ("Twice the push, twice the flow") fits two chip rows at the headline size, and the claim line must match the spoken words exactly. Nothing else changed.

## v2.0.1 (16 Oct 2026): light bands, science-safe headline chips, cell reveals

- **No dark colour blocks** (founder: "if possible don't use dark colours"; PD-17 backgrounds stay light). The physics table changed from navy `#1B2A4A` blueprint to a LIGHT blueprint: sky `#A9C0E2` grid paper with cream rules. The chemistry lip changed from royal to mustard `#E0A73A`, and the counter from deep teal `#2F7F7A` to mid-tone `#7FB5AE`, still speckled. `build_tokens.py` now fails any band below relative luminance `world.band_min_luminance` 0.18, and it records band luminance and sparkle contrast. Dark remains only on small chips and the brand sticker. `brand/endcard.svg` and `brand/_preview/brand_assets.png` were updated to match.
- **Headline chips never borrow a science hue.** `chips.headline_styles` = black, mustard, grid, teal, cream (new `cream` chip style). Brick (mismatch) and royal (voltage) are out of the cycle. The cycle step is coprime to the style count, so neighbours differ.
- **card.js cell-level reveals.** A table cell spec may carry `at` (`{fx, dec?, role?, at?}`). The cell appears whole on its reference (verb Card) inside a ruled, dashed empty slot. Cells and rows without `at` behave as before. Only table cells honour `at`. The Ohm example shows V and I from frame 0 and reveals the V ÷ I cells (rows 1 and 2) at the ratio beat, cue c09.

## v2.0.0 (16 Oct 2026): the paper cut-out collage house style for every subject

Decisions: PD-19 (house style), PD-20 (no "AI-generated" line), PD-21 (brand at the start and the end only); see `../DECISIONS_PD.md`.
Reference look: `16_pilot_builds_2026-10-16/biology/opus` (the founder's "Vox style" pilot).

### Reversed from A2 (audit/A2_visual_explanation.md §7 and §10 "Drop"), and why

A2 judged the pilots' collage vocabulary to be decoration with no meaning. It dropped washi tape, ransom tiles, polaroids, paper grain, torn strips, corner sparkles, the kraft board and the decorative bleed. v1.0/v1.1 enforced that with a build-gate ban list and flat white panels on a pastel page. The founder saw the result and rejected it: "still looks boring, not vibrant"; "check out its vibrant background and everything"; "can't we make every video like the attached one" (PD-19, 16 Oct 2026). v2.0.0 therefore **reverses**:

- the decoration ban (`decoration.banned_tokens`: feTurbulence, washi, polaroid, ransom, halftone, pencil, shelf, boil, wobble, Kalam, Chalkboard, Marker Felt, backOut, elastic). It is replaced by **structural bans only** (`gates.banned_patterns`): CSS transition/animation/keyframes, requestAnimationFrame, Date.now/new Date, Math.random, remote URLs, overshoot easings, Unicode subscripts, plus the brand gate ("ExamLeaf", "AI-generated").
- "depth from flat panels and one soft shadow only". Depth now comes from the torn-paper world, stickers with cream outlines, the soft double shadow and paper grain.
- the per-subject pastel page plus white board. Each subject gets its own torn-paper world in one shared vocabulary.
- the single-font headline. Headlines are ransom chips mixing sans (Kohinoor Devanagari, the reference's effective face), Georgia and Courier New.

A2's teaching rules are **kept**:
- one persistent board, with no resets or teardown;
- a complete picture at frame 0;
- whole-phrase headlines (chips appear together, ≤ 40 ms stagger), never word-by-word karaoke;
- nothing empty;
- labels ≥ 52 px, equations ≥ 72 px, true subscripts;
- colour by meaning, with red always paired with a shape;
- every string from the fixture;
- seek-determinism;
- no elastic, back, bounce or spring easing, and no overshoot on measured values;
- no wobble on science objects (no verb produces it).

### Added
- `tokens.json` v2.0.0:
  - the collage palette and text roles, with darkened text variants for current, resistance/condition and mismatch;
  - chip styles and chip roles; sticker outline and shadow; tape; sheet; the brand sticker;
  - world definitions per subject (physics bench/trim/blueprint table, chemistry grid bench/lip/teal counter, biology grass/soil);
  - Kohinoor/Georgia/Courier fonts; ident placement; motion `pop_scale0`, `slide_px`, `chip_stagger_s`.
- `tools/build_tokens.py` checks text on paper, cream, grid and outline; chip fg/bg; atoms; the brand sticker; biology tints (≥ 4.5); ink on board bands; colour strokes on paper and outline (≥ 3). It writes 102 ratios. Lowest text: brick chip 4.55. Lowest graphic: ink on biology grass_dark 3.29.
- `diki_scene.css`: hand-written stage styles, now one shared file (v1 copied the stage CSS into every scene).
- Runtime:
  - the world layer, built once from fixed seeds;
  - the paper backdrops of the result and card lanes, as a layer under the halos;
  - the opening ident; headline chips; the think plate as a taped sheet;
  - the end card: wordmark sticker plus the "Free lesson" chip, triggered by the last `outro.brand` or `outro.disclosure` beat. Its text is never shown.
  - verbs `Pop`, `Slide`, `Chips`, `Tape`;
  - helpers `D.chip`, `D.chipRow`, `D.brandSticker`, `D.place`, `D.sticker`, `D.sheetEl`, `D.backdrop`, `D.effOpacity`.
- `qa_scene.py`: `W_WORLD_MISSING`, `W_IDENT_MISSING`, `W_IDENT_LATE`, and a one-line result summary.
- `brand/opening_ident.svg` (replaces `header_lockup.svg`); restyled `wordmark.svg` and `endcard.svg`; `brand/_preview/brand_assets.png`.

### Changed
- Lanes: no lockup lane. The title lane is 250–450 (two chip rows) in every layout. Default diagram 456–1320 (0.45). Carded: diagram 456–1040 (0.304), result 1048–1194, card 1202–1470.
- Components restyled with the same public APIs:
  - circuit: stickers and chips;
  - species: atom stickers, formula and ledger on sheets;
  - tracer: tinted taped compartments, two-tone arrows, C sticker;
  - badge: now a chip;
  - caption: a paper chip;
  - card: a taped sheet with ruled table slots;
  - equation: on the result sheet.
- `Emphasize` halo is butter `#FFE08A` at 0.7. `StrikeThrough` and `MapSymbol` are two-tone (a cream outline under the coloured stroke). `PreserveObject` is now checked through the end card.
- Overlay geometry and the badge class/colour are written in full every frame, so the DOM is identical after any seek history.
- `build_scene.py` inline comments name only the file, so a source path can never leak a brand string into a scene.
- `examples/ohm_demo`:
  - rebuilt on v2;
  - the script's last beat is `outro.brand` "Professor Diki Simplified.";
  - the fixture drops `lesson_code` and any disclosure text and adds `endcard_line1` / `endcard_line2`;
  - the table card is up from frame 0 and fills as readings land.

### Removed
- `#lane-lockup`, `#lockup`, `#end-motif`, `#disclosure`; `display.ui.lesson_code` and `display.ui.header` on screen; any read of an outro disclosure text.

## v1.1.0 (16 Oct 2026)
LIGHT VIVID system (PD-17): white board panels on a pastel subject page, navy ink, card lane (PD-18). Withdrawn by PD-19.

## v1.0.0 (16 Oct 2026)
First unified system (PD-15, dark vivid). Superseded by v1.1.0.
