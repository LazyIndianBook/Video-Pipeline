# Doodle recipes (doodle-handdrawn)

Source: [V2] (the deer story was entirely code; "convincing hand-drawn look") and the pencil-doodle rules in [V4-MP] §6. The doodle style is the cheapest house style — no credits — and the default illustrative style for Reels (report §4.2 [Recommendation]).

## 1. Stroke rules

- Ink `#3a332c` (pencil) or the style's ink token; 3–5 px; round caps and joins ([V4-MP]).
- Strokes are SVG paths (or Canvas paths) built once from point lists; `wobblePath` adds seeded jitter that re-seeds at the boil rate (8–10 fps).
- Reveal by `drawOn` (dash offset) or pop-and-wobble.
- A light pencil-texture overlay (procedural grain built once, or a vendored scan) sits above fills, below text.

## 2. Mark vocabulary ([V4-MP])

| Mark | Recipe |
|---|---|
| Sparkle crosses in corners | Two short strokes, drawOn 0.2 s each, then boil |
| "?" and "!" above characters | Handwriting glyph path or font glyph in a doodle font, pop + finite wobble |
| Speed lines, impact ticks, motion arcs | 3–6 strokes, staggered drawOn 0.04–0.06 s apart, fade after 0.6 s |
| Dashed travel trails | `stroke-dasharray` dashes + drawOn of a mask path |
| "z z z", shiver marks | Boil at 8 fps, finite duration |

## 3. Depth (fixing [V2]'s "flat and cartoonish… no depth")

[V2]'s first pass was "strictly 2D… no depth"; the fix was iteration. Ask for depth up front:
- three to five layers with `layerOffset(camera(t), depth)` parallax;
- a foreground element that partially occludes the subject;
- soft contact shadows (flat ellipses, 15–25 % ink);
- scale contrast (big foreground, small background).

## 4. Science-safe doodles (report §7.13, §9 accuracy invariant)

- A doodle arrow that *teaches* (force direction, light ray, current) is not decoration: its geometry comes from fixture fields (angle, direction, magnitude) and it is **never boiled or wobbled at the tip**. Wobble only the shaft by ≤1.5 px, or not at all.
- Graphs, axes, scales and labels are not doodles; they come from `examleaf-svg-scenes` / `examleaf-manim-scenes` and are composited.
- A doodle may illustrate an analogy (a ball rolling down a hill) but must not show a number or ratio the fixture does not hold.
- No camera push-in or shake during the window where a fixture-bound element is revealed or held (#64).

## 5. Beat recipe (Reel, ~20–60 s)

```text
hook (0-3 s): one big doodle subject draws on in <=0.8 s, question in kinetic type (top_title)
beats:        one sentence = one beat; each beat adds 1-3 strokes or a pop-in on its word
idle:         every visible stroke boils at 8 fps for a finite duration; characters sway finitely
transition:   paper-sheet slide or a wipe drawn as a thick pencil stroke (power3.out, ~0.5 s)
end card:     recap line holds >= 1.2 s (longer for Indic), CTA outside platform UI zones
```

## 6. Performance

- Build all paths, lengths, textures and seeded layouts in `window.ready`; `render(t)` only sets attributes.
- Prefer SVG for strokes (crisp at 1080×1920) and Canvas for many particles.
- Keep path point counts modest (tens, not thousands) so `wobblePath` stays cheap per frame.

## 7. Don't

- No `Math.random`, `Date.now` or rAF (lint F04, F01, F07).
- No infinite boil or sway (lint F10).
- No per-code-point handwriting animation for Devanagari or Bengali-Assamese; animate per word or grapheme cluster (`examleaf-kinetic-typography`).
