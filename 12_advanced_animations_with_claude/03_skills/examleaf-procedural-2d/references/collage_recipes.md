# Collage recipes (paper-collage-vertical)

Source: [V4-MP] style guide, adapted to 1080×1920 (report §4.1, §1.3 ExamLeaf reading). Primitive names refer to `primitives_catalog.md`. Use for hooks, analogies, history-of-science stories and recap endings — never for labelled science, which comes from fixtures and existing renderers.

## 1. Asset split: generated vs code

| Element | Made by | Notes |
|---|---|---|
| Characters, creatures, props as watercolour/coloured-pencil cutouts | Generated once (Higgsfield GPT Image via `examleaf-selective-generation`, transparent, 2K) after storyboard approval | Trim transparent margins before use; pass the hero reference image for consistency (#48) |
| Paper backgrounds | Vendored scans or `makePaperTexture` | Cream watercolour, kraft board, watercolour skies, night navy, charcoal soot |
| Die-cut white border, warm shadow | Code (`#diecut` filter + two drop-shadows) | 6–12 px border at 1080 px width; shadow values from [V4-MP] |
| Ransom titles, brush captions, tags | Code (`examleaf-kinetic-typography`) | Never generated (#54) |
| Washi tape, confetti, torn scraps, doodles, UI | Code | [V4-MP] "built in code, not generated as images" |
| Any label, number, formula, arrow that encodes science | Fixtures through existing renderers | Accuracy invariant (report §9) |

## 2. Layer stack (9:16)

```text
z0  background paper (depth 0.2)          full frame
z1  torn-paper middle strips (0.5)        lower half of middle_visual
z2  props (0.8)                           middle_visual
z3  characters (1.0)                      bottom of middle_visual, feet on the strip
z4  foreground strip, ferns/hills (1.3)   just above bottom_caption (characters pop up from behind it)
z5  vignette (static, subtle, warm)
z6  text layer (kinetic typography)       top_title / tags near props
```

Captions live in `bottom_caption` and are owned by `examleaf-speech-animation-synchronizer`; collage art never covers that zone.

## 3. Beat recipe: "one sentence = one visual beat"

```text
for each sentence (from the cue sheet):
  reveal element(s) at cue.at  (on, or about 0.05 s before, the word [V4-MP])
  popIn() characters/props pivoting at the feet; drop-in or slide-in for variety
  idleSway() everything visible, finite n
  optional gag (multiply, tear, paperFlip, squashy shrink, tape-on) on its own cue
next sentence starts a new sheet about 0.3 s after the previous line's last word (sheetIn, vary direction)
```

## 4. Recurring layouts, vertical versions

| Layout | Vertical recipe |
|---|---|
| Hero looks up at a ransom title | Title in `top_title`; hero bottom-left of `middle_visual`, head tilted up; sparkle doodles in corners |
| Photos taped to kraft board | 2–3 polaroid cards stacked, alternating ±4° rotation, washi tape strips (pink, mustard or teal, semi-transparent) drawn in code; cards tape on one per word |
| Row of objects, one per word | Column top→bottom, or 2×N grid; each object `popIn` on its word |
| Big central prop with tags | Prop centred; Patrick Hand tags above and below on washi tape; red pencil check marks draw on |

## 5. Gags (each on a cue, each finite)

- **Multiply:** `copiesAt(t, cueTimes)` doubles 1 → 2 → 4 → 8; copies are placed by a seeded layout built once.
- **Tear:** `tearEdge` (seeded jagged polyline, built once) + `tearHalves` after the cue; add 4–6 seeded scraps that fall with the halves.
- **Paper-flip swap:** `paperFlip` (scaleX 1 → 0 → 1, swap at the midpoint) with a seeded confetti puff.
- **Squashy shrink:** discrete scale steps on cue times (e.g. 1 → 0.8 → 0.6), each with `backOut`.
- **Tape-on:** photo drops in, then a tape strip draws on across a corner.

## 6. Camera

- Slow push-in to about 1.03–1.04 over the scene via `camera()` ([V4-MP]).
- Stepped shakes only on impacts, and never inside a lock window (#64): `camera()` and shakes are suspended while a measurement or label is being revealed or held.

## 7. Character consistency (#48)

1. One canonical hero image approved in the storyboard gate.
2. Every later cutout request attaches it as the reference image and names the pose (pointing, crying, cheering, waving).
3. Assets record provider, model and job metadata in the asset library (its acceptance rule).
4. A reviewer compares the new pose against the hero sheet before use.

## 8. Cost notes

- The collage style is credit-heavy ([V4]); the storyboard gate estimates every cutout. Reuse approved cutouts across lessons through the asset library.
- Everything except cutouts is code, so iteration on motion costs tokens, not credits.

## 9. Don't

- No 3D rendering, glossy gradients, photorealism, heavy blur or glow ([V4-MP]).
- No text inside generated images (#54).
- No full-frame white flash (#56).
- No infinite idle loops (#18); no `Math.random` (#17).
- No decoration that changes a taught angle, ratio or direction (report §7.13).
