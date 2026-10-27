# Interpreting reference metrics for 9:16 ExamLeaf content

The analyzer reports numbers. This reference explains how the brief and the style guide use them. The model never watches the reference; it reads these numbers (Opus 5.5 outputs text only [N71]).

## 1. Pacing

| Metric | Meaning | How ExamLeaf uses it |
|---|---|---|
| `shots.median_s` | Typical shot length | Upper bound for beat spacing within a scene. [V4-MP] says one sentence = one visual beat; narration sets the real spacing |
| `shots.p10_s` / `p90_s` | Fast and slow extremes | p10 under about 0.5 s signals flash-cut material; do not copy it for students (#56) |
| `shots.cv` | Regularity (std/mean) | Low cv = metronomic cutting (music-led reels); high cv = narrative pacing |
| `shots.cuts_per_minute` | Transition density | Budget for sheet transitions per minute in collage and editorial styles |
| `shots.histogram` | Distribution buckets | Compare reference vs ExamLeaf draft render in QA |

**Rule:** reference pacing is a ceiling, not a target. ExamLeaf narration sets duration (report §5.5: "duration derives from the narration"), and teaching content needs longer holds than entertainment references.

## 2. Holds

- `holds.median_s` from freezedetect approximates static text time in the reference.
- Floors that override it: headlines ≥1.2 s [N60]; longer for Hindi and Assamese (multiplier measured in the pilot, report §7.5); equations until the narration finishes plus 0.5 s [Recommendation].
- If the reference holds text for less than 1.2 s, note it as a difference, not a target.

## 3. Palette

- `palette.overall` gives the reference's mood: warm vs cool, muted vs saturated, light vs dark.
- ExamLeaf rule: dominant colour with sharp accents rather than an even palette [N52]. Map the reference's top swatch to the dominant role and one or two strong minority swatches to accents, then snap to the nearest approved brand or style token. Never import reference hexes directly into brand tokens.
- [V4-MP]'s palette (cream #f3ecdf, tomato #d9483b, mustard #e0a73a, teal #2f7f7a, ink #2b2622, …) is an example of this structure: warm muted base, brightest accents tomato and mustard.

## 4. Layout and orientation

- `probe.orientation: landscape` or `letterbox.letterboxed: true` means the layout does not transfer to 1080×1920. Send it to `examleaf-vertical-adapt`: stacked layouts with top title, middle visual and bottom caption zones (report §10.15).
- [V4-MP]'s "about 90 px from edges" rule is for 16:9 and must be adapted with larger top and bottom margins; exact insets come from `vertical_safe_zones.tokens.json`, which must be measured (report §7.9, §11.9).

## 5. Typography (stills, human review)

[V3] stresses studying "layout structure and its exact typography treatment". Stills support that study:
- Note type roles (headline, label, number callout), not font files.
- Identify the font *category* (slab, grotesque, brush, mono) and choose an allowed font from the style tokens; never copy a font the reference uses without a licence.
- Note whether the reference animates per letter. For Devanagari and Bengali-Assamese, ExamLeaf animates per word or grapheme cluster only (#55).

## 6. Writing the numbers into a brief

Example block the brief may quote:

```text
Reference pacing (reference_a.mp4, analysis only): median shot 2.4 s (p10 1.1 s, p90 4.2 s),
14 cuts/min, static holds median 1.6 s. Palette mood: warm cream dominant, tomato and mustard accents.
Use as a ceiling for transition density; narration sets beat timing; headline holds stay >= 1.2 s.
```

## 7. Copyright and rights

- The reference is used to measure; it is not copied. Do not trace characters, reuse frames, re-create distinctive artwork, or pass stills to an image model as a reference image.
- Stills stay in the quarantine folder; they are excluded from `examleaf-asset-library`.
- When the reference is ExamLeaf's own earlier work, the same JSON is fine to reuse, and its frames may become assets only through the asset library's normal rights process.
