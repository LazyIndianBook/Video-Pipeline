# Style selection matrix

Five house styles, all 1080×1920. Sources: report §4 and [V4-MP]. Labels: [Recommendation] and [Hypothesis] follow the report.

## 1. The five styles side by side

| | paper-collage-vertical | doodle-handdrawn | editorial-vox | kinetic-type | voxel-isometric |
|---|---|---|---|---|---|
| Source | [V4-MP], [V2] L3 demo | [V2] deer story | [V3] sun-vs-planets | [V3], [N50]–[N55], [N60] | [V5] island (unverified), [V1] 3D runs |
| How it is made | Raster cutouts (Higgsfield GPT Image 2.5, transparent, 2K) on paper textures; text, tape, doodles in code; seek-driven tweens; boil | Canvas/SVG paths with seeded wobble, draw-on, pencil texture, flat fills; no image model | Textured backgrounds, cut-out photos or illustrations, highlighter strokes, serif+sans headline mix, map and number callouts, push-ins | Per-word/per-cluster timeline from word timestamps; masks, slides, scale pops; one orchestrated staggered entrance | three.js instanced boxes, orthographic camera, simple lighting, seeded layout, camera as f(t) |
| Owner skill for primitives | `examleaf-procedural-2d` (+ `examleaf-selective-generation` for cutouts) | `examleaf-procedural-2d` | `examleaf-procedural-2d` + licensed assets | `examleaf-kinetic-typography` | `examleaf-threejs-scenes` |
| Credits | High ([V4] "on the expensive side") | None | Low–medium (licensed or generated photos) | None | None |
| Teaching use | Hooks, analogies, history-of-science stories, recap endings | Default illustrative style for Reels; hooks, analogies | Comparisons and scale stories (planet sizes, orders of magnitude) from validated numbers | Definitions, key terms, formula callouts, quiz prompts, recaps | Crystal lattices, cell organelles, "island of concepts" recap |
| Main risk | Character drift (#48), credit spend (#41–45), image-model text (#54), 16:9 source guide (#49) | "Flat and cartoonish… no depth" ([V2]); ask for parallax | Weak AI script ([V3]); asset licensing | Indic per-letter breakage (#55); short holds (#50) | Headless WebGL variance (#65); context loss |
| Route tag | illustrative | illustrative | illustrative | typographic | illustrative (or data-bound with fixtures) |

## 2. Selection algorithm

```text
if route_tag == "typographic":            -> kinetic-type
elif route_tag == "data-bound":           -> not this library (svg/manim/molecule/biology/threejs scenes)
else (illustrative):
    candidates by purpose:
        hook, analogy        -> doodle-handdrawn, paper-collage-vertical
        story (history)      -> paper-collage-vertical, doodle-handdrawn
        recap                -> paper-collage-vertical, voxel-isometric, kinetic-type
        comparison / scale   -> editorial-vox
        structure (3D)       -> voxel-isometric
    drop paper-collage-vertical if credit_budget == 0 and cutouts are not already in the asset library
    drop any style whose Indic fonts are missing for the lesson language
    prefer the style already used in this lesson segment (consistency)
    tie-break: cheapest (doodle < kinetic < voxel < editorial < collage)
```

[Recommendation] At most two illustrative styles per lesson plus kinetic type; the same style for a whole Reel.

## 3. Style-specific motion vocabulary and SFX

| Style | Motion vocabulary | SFX list |
|---|---|---|
| paper-collage-vertical | Pop-in from scale 0 and ±12° with back.out(2–3) pivoting at the feet; drop-in with bounce; hops with squash and stretch; idle sway ±1.5–4° with finite repeats; boil 8–10 fps; gags: multiply, tear, paper-flip swap, squashy shrink, tape-on; transitions: sheet slide 0.5–0.7 s power3.out, somber drop ~0.9 s, whip ~0.4 s expo.out; push-in to ~1.03–1.04 ([V4-MP]) | Paper swish, light tap, cartoon pop, boing, paper tear, thud, sparkle chime; bigger booms only for real drama ([V4-MP]) |
| doodle-handdrawn | Draw-on strokes, wobble with seeded noise re-seeded at boil rate, pop and wobble, parallax layers for depth ([V2] critique) | Pencil scratch, pop, tap [Recommendation]; STEM one-shots (electric hum, bubbling, click-snap for bonds; report §5.1) |
| editorial-vox | Push-ins, highlighter strokes drawing on, number counters from fixture values, map callouts, cut-out slide-ins | Whoosh, soft hit, paper slide [Recommendation] |
| kinetic-type | One orchestrated staggered entrance per beat [N53]; masks, slides, scale pops; dominant colour with sharp accents [N52]; CSS-only motion preferred for HTML [N54] driven by seek | Tick, swipe, soft pop [Recommendation] |
| voxel-isometric | Camera orbit and dolly as f(t); instanced blocks popping in by seeded order; fixed-step replay for any physics | Block click, low thud [Recommendation] |

Easing defaults across styles: anticipation → action → follow-through, never linear; back.out for pops, power3.out for slides, expo.out for whips ([V4-MP], report §7.4). Durations and leads are tokens in `04_harness_contract/vertical_safe_zones.tokens.json` → `motion`.

## 4. Guide section order (every style guide)

1. The look in one sentence
2. Materials and surfaces
3. Palette (dominant, ink, accents, support; hexes)
4. Characters (if any) and consistency rule
5. Typography by role (Latin and Indic), sizes from the safe-zone tokens
6. Marks and doodles
7. **Composition for 9:16** (zones, recurring vertical layouts, depth layers)
8. Motion language (with finite repeats and the seek rule)
9. Transitions (no full-frame flashes)
10. Sound (music mood, SFX list; loudness is owned by audio skills)
11. Asset rules (what is generated, what is built in code; never text in images)
12. Do / don't

[V4-MP]'s "Writing style of the narration" section is deliberately **not** part of an ExamLeaf style guide: narration comes from the Super Teacher system (report §1.3 ExamLeaf reading).

## 5. Versioning and lifecycle

| Status | Meaning | Allowed use |
|---|---|---|
| draft | Under authoring (the canonical file's `_meta.status` is currently draft for the pilot) | Sandbox pilots only |
| approved | Human style owner signed the change record; `--production` validation passes | Production briefs pin `id@version` |
| deprecated | Superseded | Re-rendering already approved lessons only |

- Semver: MAJOR changes the look of existing scenes; MINOR adds; PATCH fixes text.
- `validate_style_tokens.py --bump-check OLD NEW` fails when a style's content changed without a version bump, or when an approved style changed without a new approval.
- Every render records the style `id@version` and the tokens file SHA-256 in its manifest, so an approved lesson can be re-rendered byte-identically after the library moves on.
