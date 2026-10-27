# Safe zones for 9:16 animation QA

## 1. What is (not) known

- Report §7 rule 9 [Recommendation]:
  - canvas 1080×1920;
  - keep text and critical diagram parts inside a central safe area that avoids the top status and title strip and the bottom caption, CTA and UI overlays used by Reels and Shorts;
  - "**Measure exact insets per platform against current app screenshots and store them as tokens. Exact pixel values were not in the verified evidence.**"
- [V4-MP] §5 says to keep text about 90 px from the frame edges, at 16:9 1920×1080. ExamLeaf keeps an absolute side minimum on the left and right (*15 Oct 2026: one value, `zones.side_margin_min_px` = **96 px** in the harness token file, the larger of [V4-MP]'s 90 px and the planning pack's 96 px; earlier text said 90 px*), and uses the larger measured platform insets at the top and bottom (report §7.9: "Adapt the [V4-MP] '90 px from edges' rule to larger top and bottom margins").
- Platform insets for Instagram Reels and YouTube Shorts are open question 9 (report §11).

## 2. Token file (owned by the harness author)

`12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`. The checker accepts either shape:

```json
{"canvas": {"width": 1080, "height": 1920},
 "insets": {"top": null, "bottom": null, "left": null, "right": null}}
```

```json
{"canvas": {"width": 1080, "height": 1920},
 "platforms": {"instagram_reels": {"insets": {"top": null, "bottom": null, "left": null, "right": null}},
               "youtube_shorts":  {"insets": {"top": null, "bottom": null, "left": null, "right": null}}}}
```

- `null` means **unmeasured**. The checker reports which sides are missing; unmeasured is major in development and critical with `--require-measured` (release).
- With several platforms and `--platform all`, the checker takes the **union** of unsafe areas: the maximum inset per side. One render then works on every target platform. Use `--platform <name>` only for a platform-exclusive Reel.
- If the harness file uses another shape, both `safe_zone_check.py` and `examleaf-vertical-adapt/scripts/layout_zones.py` refuse it with "unrecognised token shape". Align the loader, or the file, deliberately. The two loaders are kept identical by hand, because the skills install independently.

## 3. How to measure insets (procedure for the token owner)

1. For each platform, take current-app screenshots on at least two phone sizes, with captions on, of a 1080×1920 test card showing a 10 px ruler grid.
2. Record the largest top and bottom overlay extents (status bar, title and handle, buttons, caption tray, CTA) in canvas pixels. Also record right-side button columns.
3. Store the values with `measured_on`, the device list and the app versions. Re-measure when the apps change their UI.
4. Until all four sides are measured for every target platform, releases fail Q3 unless a reviewer signs a phone review (major waiver), and **never** for science roles.

## 4. What must be inside, and what may bleed

| Role | Rule |
|---|---|
| `label`, `equation`, `critical` (science) | Fully inside the safe rect; else **critical** |
| `headline`, `text`, `caption` | Fully inside the safe rect; else **major** |
| `decor` (paper textures, torn strips, vignette, foreground ferns) | May bleed to and beyond the canvas edges |

Zones from `examleaf-vertical-adapt` (title, visual, caption) sit inside the safe rect. Elements that declare a `zone` must lie inside it; a violation is minor (layout consistency).

## 5. Captions

- Caption timing and text belong to `examleaf-speech-animation-synchronizer` (authoring) and `examleaf-audio-caption-qa` (corrections).
- This skill checks placement:
  - the caption box sits inside the caption zone and the safe rect;
  - it never covers a science element while both are visible (major);
  - platform-native captions also occupy the bottom area, which is why bottom insets are large. Measure with captions on.

## 6. Overlay review (human, Q16)

Draw the safe rect and zones from `zones.json` as a semi-transparent debug layer in a QA render. This is a harness debug flag defined by the harness author, never in the delivered render. Review it at phone size:
- every label is readable;
- nothing important sits under a simulated UI overlay;
- Indic text is shaped correctly;
- there is one idea per frame ([V4-MP] §7).

Record the reviewer and device.

## 7. Element dump expectations

`elements.json` is produced by seeking the scene to each cue boundary plus the first and last frames, and reading `getBoundingClientRect()` for elements tagged `data-qa-role` (`templates/dom_dump_snippet.js`). The visible intervals are assembled across samples. Boxes are in canvas pixels; the scene renders at 1080×1920 with no CSS scaling of the root. If the harness renders scaled, convert before checking.
