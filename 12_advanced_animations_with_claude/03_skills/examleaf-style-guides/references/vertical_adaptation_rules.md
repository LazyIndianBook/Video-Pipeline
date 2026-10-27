# Vertical adaptation rules for style guides

[V4-MP] is written for 16:9 at 1920×1080, 30 fps, with text about 90 px from the edges. ExamLeaf is 1080×1920. Report §0.12: "It needs a deliberate 9:16 adaptation, not a crop." This file tells a style author how to restate each rule; per-scene re-layout helpers belong to `examleaf-vertical-adapt` (report §10.15).

## 1. Canvas and zones

- Canvas 1080×1920, fps from the style (30 default). Device scale factor 1.
- Use the zones in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`: `top_title`, `middle_visual`, `bottom_caption`. Their shares and the platform insets are **placeholders** until measured on current Reels and Shorts screenshots (report §7.9, §11.9). A style guide references the tokens; it never hard-codes pixel insets.
- *Resolved 15 Oct 2026 (AD-42; this replaces a stale note that quoted 0.20 / 0.58 / 0.22):* `04_harness_contract/vertical_safe_zones.tokens.json` is the single owner of the zone shares (0.22 / 0.54 / 0.24; the title may grow to 0.30 for a three-row title, taking space from the visual zone) and of `zones.side_margin_min_px` = 96 px. `05_style_guides/style_tokens.json` mirrors them and `validate_style_tokens.py` fails on drift.
- "Text about 90 px from the edges" becomes "text inside the safe band"; top and bottom margins are larger than the sides because platform chrome sits there (report §7.9).
- All science glyphs live in `middle_visual`; captions are protected in `bottom_caption` and owned by `examleaf-speech-animation-synchronizer`.

## 2. Recurring layouts: 16:9 → 9:16

| [V4-MP] 16:9 layout | 9:16 restatement |
|---|---|
| Character bottom-left looking up at a ransom-note title | Title in `top_title`; character at the bottom of `middle_visual`, looking up; no character in the caption zone |
| Photos taped to a kraft board (row of 4–5) | Vertical stack of 2–3 photos, slight alternate rotation; more photos become a second beat |
| A row of objects appearing one per word | A column, or a 2×N grid, filling top to bottom in word order |
| Big central prop with small tags around it | Prop centred in `middle_visual`; tags above and below rather than left and right |
| Flat panorama landscape of torn-paper strips | Taller strips stacked with more sky; horizon in the lower third of `middle_visual` |

## 3. Depth and camera

- Keep layered depth (background → torn-paper middle → props → characters → foreground strip) ([V4-MP]). In 9:16, the foreground strip sits above the caption zone, not at the frame bottom.
- Slow push-in to about 1.03–1.04 stays; pans between stacked layers become vertical pans.
- No push-in, shake or pan during a measurement or label reveal (#64).

## 4. Typography sizes

- Use the `typography_px_at_1080` minima in the safe-zone tokens (essential label, equation, heading). Split or enlarge instead of shrinking.
- One idea per frame matters more in 9:16: a 16:9 frame with two ideas becomes two beats.

## 5. Transitions

- Sheet slides keep their timing (0.5–0.7 s power3.out) and vary direction; vertical slides read naturally on phones.
- "White flash or bloom for explosions" is replaced by a non-flashing paper burst or a dark-sheet drop (#56).
- The incoming sheet still starts about 0.3 s after the previous line's last word ([V4-MP]).

## 6. Storyboards

- [V4-MP] asks for "one 16:9 image with 3×3 panels". ExamLeaf grids show nine **9:16** panels (portrait thumbnails), so reviewers judge the real composition (`examleaf-anim-storyboard-gate`).

## 7. Reels from lessons

- Reels re-seek sub-ranges of time-pure lesson scenes (report §9 step 10). A style must therefore not rely on state built up earlier in the lesson; every scene renders correctly from any `t` (determinism rule).

## 8. Checklist for a style author

- [ ] Canvas 1080×1920 in tokens
- [ ] Composition section written for 9:16, using zone names, not pixels
- [ ] Every [V4-MP]-style layout restated vertically
- [ ] Camera rules exclude measurement and label windows
- [ ] No full-frame flash transition
- [ ] Storyboard panels portrait
