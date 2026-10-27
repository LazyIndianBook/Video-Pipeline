# Flash and luminance test method

**Why.** [V1]'s description warns "some of these videos have bright, fast flashes". Report §7 rule 11 [Recommendation]: "For students, ban full-frame flashes and limit rapid luminance changes; check them in visual QA." [V4-MP] §9 uses "a white flash or bloom for explosions", and section rule G15 replaces it with a non-flashing transition. Edge case #56.

## 1. The external rule (VERIFY)

WCAG 2.x Success Criterion 2.3.1 ("Three Flashes or Below Threshold") is the accessibility reference. The defaults in `scripts/flash_check.py` follow its "general flash" definition **as recalled by this author**:
- a flash is a pair of opposing changes in relative luminance of **10% or more** of maximum relative luminance, where the darker image is below **0.80**;
- content fails when it has **more than three** such flashes in **any one-second period**;
- an area condition exempts small flashing areas;
- a separate red-flash rule exists.

None of this is in the section's verified evidence set (`01_research/SOURCES_and_claims.md`). **Verify the exact thresholds, the area condition and the red-flash definition against the current W3C text before relying on this test for compliance.** If the W3C text differs, change `--delta` and `--dark-limit` and record the change in this file.

## 2. Luminance per frame

- Frames are decoded from PPM (P3/P6) or PGM (P2/P5). 16-bit maxval is supported.
- Each sRGB channel is linearised: `c ≤ 0.04045 → c/12.92`, else `((c + 0.055)/1.055)^2.4`.
- Relative luminance `Y = 0.2126 R + 0.7152 G + 0.0722 B`; for grey frames, `Y = lin(v)`.
- The **tile mean** of Y is computed over an N×N grid (`--grid`, default 1 = whole frame). The whole-frame series is always computed as the mean of the tiles.
- CSV input (`frame,luminance`) must already be linear relative luminance. `--encoding srgb8` accepts gamma-encoded 8-bit means, which is an approximation: the mean of encoded values is not the encoded mean of linear values.

## 3. Transitions and flashes (the algorithm)

1. Walk the series, keeping the running maximum and minimum since the last transition.
2. A **rise** completes when `Y − min ≥ delta` (while not already rising). A **fall** completes when `max − Y ≥ delta` (while not already falling). This hysteresis ignores small wiggles and counts each big swing once.
3. A transition counts only if its darker side is below `dark_limit`. This filters bright-on-bright changes.
4. In every sliding 1 s window (`fps` frames), flashes = ⌊transitions / 2⌋, a pair of opposing changes being one flash. Report the maximum and where its window starts.

Selftest anchors (30 fps):
- a 5 Hz square wave between 0.1 and 0.9 gives 10 transitions/s, so 5 flashes/s;
- one bloom (0.2 → 0.95 → 0.2) gives 1 flash;
- a ±0.03 flicker gives none;
- 0.85 ↔ 0.95 gives none, because the darker side is ≥ 0.80.

## 4. ExamLeaf severities (house rule stricter than WCAG)

| Finding | Severity | Why |
|---|---|---|
| > 3 flashes in any 1 s on the **whole frame** | **critical** | Fails the WCAG count over the largest possible area |
| Any whole-frame flash, even one | **critical** (15 Oct 2026; was major) | House ban on full-frame flashes (G15), never waivable; matches 07/06 §4 and `flash_check.py`. Swap the transition rather than seeking a waiver |
| > 3 flashes/s in **one tile** only | **major** | The area condition is not implemented; a human judges the area |
| Otherwise | pass | |

## 5. Frame extraction

Standard FFmpeg usage (verify on your build):

```sh
ffmpeg -i render.mp4 -vf scale=270:480 -pix_fmt rgb24 qa/frames/f%05d.ppm
```

- Downscaling to 270×480 (a quarter size) keeps the test fast. It averages encoded pixels, which slightly smooths tiny flashes. For a scene that fails narrowly, re-run at full size.
- Keep the source fps: do not drop frames. `--fps` must equal the render fps (30 in the house contract).
- Frames must come from the **final render**, not a preview, because transitions and the vignette change luminance.

## 6. Known limits

- No red-flash test, and no visual-angle or area maths. Tiles are a coarse proxy.
- Saturated colour changes at constant luminance are not flashes under this measure, but can still be uncomfortable. The human reviewer judges them.
- Pattern and stripe hazards are not covered.
- The test is per scene. Run it on the composed Reel as well, because a transition *between* scenes (a dark sheet dropping onto a bright scene) can create a pair across the boundary.

## 7. Fixes that usually work

- Replace "white flash or bloom" with a paper-sheet drop, a soft vignette darken or a camera shake that is not on a label (#64).
- Lengthen strobing elements (fire flicker, "boil" at 8–10 fps [V4-MP]) to a smaller amplitude or a smaller area.
- Keep stepped boil jitter geometric, not luminous: move the shape, not its brightness.
