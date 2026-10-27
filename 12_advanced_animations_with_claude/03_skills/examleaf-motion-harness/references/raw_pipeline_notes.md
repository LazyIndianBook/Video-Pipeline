# Raw Canvas / SVG / three.js pipelines

Raw seek pipelines render a scene frame by frame outside a composition framework, then export an image sequence that HyperFrames (or Remotion) places as a clip (report §2.4 [Recommendation]).

## When to use

- three.js 3D (orbitals, lattices, field lines) that is awkward inside a composition framework (`examleaf-threejs-scenes`).
- Procedural doodle and collage drawing (`examleaf-procedural-2d`).
- Anything exported as an image sequence and then placed as a clip.
- ExamLeaf's existing Python SVG → FFmpeg proof renderer is the same pattern for 2D science (`examleaf-svg-scenes`).

## Reference implementation: opus-js-animations (klsoen, MIT [N21])

| Fact | Source |
|---|---|
| Plugin: `/plugin marketplace add klsoen/opus-js-animations` | [N15] |
| Manual: `cp -r opus-js-animations/skills/opus-js-animations ~/.claude/skills/` | [N16] |
| Set `CHROME=/path` if Chrome isn't found | [N17] |
| "headless Chrome renders frame i as seek(i / fps) across parallel workers" | [N18] |
| Voiceover keys read from the environment or `~/.config/opus-js-animations/keys.env`, "never written into your project" | [N19] |
| Audio cut on zero crossings "with no normalising, EQ or fades unless you ask" | [N20] |
| Claims of other-model support untested | [N21] |

Admit it only through `examleaf-skills-security`; ExamLeaf uses its own voice path, so its voiceover features are not used (report §5.3).

## Frame loop (any raw pipeline)

```text
for i in 0 .. round(DURATION * fps) - 1:
    t = i / fps
    await page.evaluate(t => window.seek(t), t)     # resolves when frame t is painted
    errors = await page.evaluate(() => window.__errors)
    if errors has severity 'error': stop and report
    capture PNG -> frames/frame_%05d.png
```

- The capture is triggered by the renderer after `seek` resolves; the scene never signals readiness through rAF [N69].
- Waiting for `window.ready` uses setTimeout polling with a deadline, outside the scene.
- Workers render disjoint frame ranges; this is safe only because each frame is a pure function of t.

## Image sequence → clip

Standard FFmpeg usage, verify on your build:

```sh
ffmpeg -framerate 30 -i frames/frame_%05d.png -c:v libx264 -pix_fmt yuv420p -r 30 clip.mp4
```

- Keep the PNG sequence as the determinism artefact; hash frames, not the MP4.
- For transparent overlays, keep PNG with alpha (or an alpha-capable codec chosen by web-composition); `yuv420p` drops alpha.
- The composition imports the clip at the cue-sheet time; audio is mixed separately (`examleaf-audio-production-engineer`) and loudness is normalised as a mandatory final step because some toolchains do no normalisation unless asked [N20].

## [V1] tools-folder pattern

[V1] gave each run a folder of three.js, Canvas 2D, SVG and frame-conversion tools with **no guides or examples**. ExamLeaf instead supplies the contract, template, tokens and primitives, which should cut fix loops [Hypothesis; measure in the pilot].
