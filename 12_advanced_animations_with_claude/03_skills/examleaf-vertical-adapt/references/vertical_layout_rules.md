# Vertical (9:16) layout rules

**Canvas:** 1080×1920 at 30 fps (house contract; section AD-07). **Sources:** [V4-MP] §5 and §7–§9 (written for 16:9 1920×1080); report §7 rule 9 [Recommendation]; report §0 item 12 ("needs a deliberate 9:16 adaptation, not a crop").

## 1. The zone model

```text
┌──────────── 1080 ────────────┐
│  top inset (platform UI)     │  measured token, union over platforms
│ ┌──────────────────────────┐ │
│ │ TITLE zone   (~18%)      │ │  ransom title, question hook, number
│ ├──────────────────────────┤ │  gutter
│ │                          │ │
│ │ VISUAL zone  (~57%)      │ │  characters, props, diagrams (fixture-driven), doodles
│ │                          │ │
│ ├──────────────────────────┤ │  gutter
│ │ CAPTION zone (~25%)      │ │  burned-in captions / labels row / tags
│ └──────────────────────────┘ │
│  bottom inset (captions, CTA)│  measured token
└──────────────────────────────┘
   side ≥ max(inset, side_margin_min_px = 96 px)
```

- The zones are stacked inside the **safe rect** (canvas minus insets). The shares are read from the harness token file (`zones.top_title/middle_visual/bottom_caption.share` = 0.22 / 0.54 / 0.24, [Recommendation]); `--ratios` is an experiment override only and `--gutter 24` is a starting value, to be tuned in the pilot. *15 Oct 2026 (AD-42): the old script default 0.18 / 0.57 / 0.25 is withdrawn; the token file is the single owner.*
- **Bleed rect** (the whole canvas) is for decor only: paper textures, torn strips, vignette, foreground ferns. [V4-MP]'s depth stack (background → torn-paper middle layers → props → characters → foreground strip) still applies. Only text and critical science must stay in zones.
- **Side margin:** [V4-MP] keeps text "about 90 px from the frame edges" at 1920 wide. At 1080 wide, ExamLeaf keeps an **absolute minimum** of `zones.side_margin_min_px` = **96 px** (15 Oct 2026, AD-42: the larger of [V4-MP]'s 90 px and the planning pack's 96 px; earlier text said 90 px), which is proportionally larger and suits phones. Top and bottom use the larger measured platform insets.

## 2. Insets: tokens, never constants

- No verified pixel values exist (report §7.9; open question 9). The harness token file holds `null` until a human measures current app screenshots per platform.
- `layout_zones.py` refuses unmeasured tokens unless explicit `--provisional-insets` are passed, and then marks the output `provisional: true`.
- Use the **union** of platforms (`--platform all`) so one render serves Reels and Shorts.

## 3. Mapping [V4-MP] recurring layouts to vertical

| 16:9 layout ([V4-MP] §7) | Vertical adaptation [Recommendation] |
|---|---|
| A character bottom-left looking up at a ransom-note title | Title in the TITLE zone (ransom tiles may wrap to 2 lines, about 6–9 letters per line); the character at the lower left of the VISUAL zone, looking up; the eye line crosses the gutter |
| Photos taped to a kraft board | 2-column stack of photos in the VISUAL zone, taped at slight rotations; tags in the CAPTION zone or under each photo |
| A row of objects appearing one per word | A **column** (top → bottom) or a 2-wide grid in reading order; still one object per word on its cue |
| A big central prop with small tags around it | Prop centred in the VISUAL zone; tags above and below (not left and right) to respect the width; leader lines short |
| Flat straight-on camera, generous negative space, one idea per frame | Unchanged. Vertical frames crowd faster, so cut elements rather than shrink them |
| Slow push-in 1 → ~1.03–1.04 | Centre on the VISUAL zone; check edges at 1.04; never during label or measurement reveals (#64) |
| Ransom title with ±6° tiles | Same tiles, a smaller count per line; keep tiles inside the TITLE zone at their maximum rotation |
| Hand-lettered caption with double underline | CAPTION zone or under the title; the underline draws on inside the zone |
| Small labels on washi-taped tags | Next to their object in the VISUAL zone if readable; otherwise a labels row in the CAPTION zone, connected by short leader lines |

## 4. Typography

- Keep on-screen text short: a title, a number or a punchline word, never full narration sentences ([V4-MP] §5). Captions carry the sentences.
- Minimum sizes come from the style guide and design tokens. The learning-psychology extraction records two ranges for label, equation and heading sizes (message-04 values vs planning-pack values; `02_learning_psychology/palette_and_typography_tokens.json` `differences_noted`). *15 Oct 2026:* this is resolved by **RD-01** (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`): message-04 ranges for essential text, planning-pack ranges only as a floor for secondary text; earlier wording called it unresolved. It refuses to shrink text below the style guide's minimum to fit.
- Indic scripts need more vertical room (matras above and below). Leave line-height headroom in the TITLE and CAPTION zones, and animate per word or grapheme cluster (report §4.4; `examleaf-kinetic-typography`).

## 5. Diagrams and data-bound inserts

- A 16:9 Manim, SVG or three.js clip placed in the VISUAL zone uses **contain**: `layout_zones.py --fit WxH --zones zones.json` gives a uniform scale, a centred position and `crop: false`.
- If the contained diagram's labels would fall below minimum size, **re-compose**:
  - split it into stacked sub-diagrams across beats (one idea per frame); or
  - render a vertical variant from the same fixture through the data-bound skill.
- Never stretch, squash or crop a scientific diagram. Never let decoration change an angle, ratio or direction the lesson teaches (report §7.13).

## 6. Motion in a tall frame

- **Transitions** ([V4-MP] §9): sheet slides of 0.5–0.7 s power3.out with varying direction; dark-sheet drop about 0.9 s; whip about 0.4 s; no exit animations.
  - A vertical slide covers 1920 px in the same time, so it reads faster. [Recommendation]: horizontal slides for text-heavy sheets; vertical drops for somber beats (the dark sheet from the top).
  - The "white flash or bloom" is replaced (house rule G15; anim-qa flash test).
- **Idle sway and boil:** unchanged, with finite repeats and seeded randomness (#17, #18; harness contract).
- **Shake:** stepped shakes on impacts only, never while labels or equations are visible (#64).

## 7. Captions and platform UI

- Burned-in captions sit in the CAPTION zone. The bottom inset reserves the platform's own caption tray and CTA buttons, so measure with captions on.
- Captions never cover a science element while both are visible (anim-qa Q7).
- One caption style per video. Caption text and timing come from `examleaf-speech-animation-synchronizer`.

## 8. Checklist before hand-off

- [ ] `zones.json` from the current token hash; provisional only in development.
- [ ] Every element group mapped to a zone; the plan shows `crop: false` and uniform scale.
- [ ] Push-in checked at the maximum scale; no camera fx on label spans.
- [ ] Text sizes at or above the style guide's minimum; Indic headroom kept.
- [ ] The phone overlay review is scheduled with anim-qa.
