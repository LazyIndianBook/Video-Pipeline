# Font policy and Indic coverage

## 1. Why fonts are named and banned

- Claude "defaults to safe choices unless explicitly encouraged otherwise" [N50].
- "Avoid generic fonts like Arial and Inter" [N51].
- Outputs "still tend to converge on common choices (Space Grotesk, for example)" [N55]: ban or rotate it.
- Result: every style names families per role from `fonts_registry` and inherits `common.font_policy.ban_as_display` in `05_style_guides/style_tokens.json` (Arial, Helvetica, Roboto, system-ui, generic sans-serif, Space Grotesk, Inter, Times New Roman, Comic Sans, Papyrus; [N51][N55] for Arial/Inter/Space Grotesk, the rest Recommendation).
- House decision recorded in the tokens: Inter is banned as a display face but allowed for labels, captions and science text (`inter_allowed_for`). The validator enforces both halves.

Note: `vertical_safe_zones.tokens.json` → `font_policy.latin` records that an older ExamLeaf source suggested Inter or a Noto Sans family; for display roles [N51] overrides that in the animation layer. The engine's offline proof renderer uses DejaVu Sans for measurement only (`04_video_engine/implementation_v2/configs/design_tokens.json`); that is not a production font choice.

## 2. Roles

| Role | Use | Example families (verify licence and pin) |
|---|---|---|
| display | Titles, ransom-note tiles (Latin) | [V4-MP] list: Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One |
| handwriting | Brush captions (Latin) | Caveat Brush ([V4-MP]) |
| label | Tags and small labels (Latin) | Patrick Hand ([V4-MP]) |
| body / labels / captions / science text | Plain text roles | Named per style; Inter allowed here only (house policy `inter_allowed_for`); never Arial |
| devanagari | All Hindi words, including inside mixed lines | Noto-class Devanagari family (report §8 #55 [Hypothesis]); candidates such as Noto Sans Devanagari, Noto Serif Devanagari, Kalam (handwriting-like) — verify coverage and licence |
| bengali_assamese | All Assamese (and Bengali) words | Noto-class Bengali-script family (e.g. Noto Sans Bengali, Noto Serif Bengali); candidates such as Hind Siliguri or Tiro Bangla — verify coverage of U+09F0 (ৰ) and U+09F1 (ৱ) and licence |

The candidate names are starting points for the pilot, not verified choices; the report lists Indic typography in headless Chrome as an open question (§11.10).

## 3. Script-specific rules

1. **Ransom-note tiles are Latin-only.** The [V4-MP] display fonts do not cover Devanagari or Bengali script [Hypothesis; verify per font]. For Indic words, use the `devanagari` / `bengali_assamese` family on tiles (one tile per word or grapheme cluster), or switch to the label/handwriting mode.
2. **Never animate per code point.** Per-letter animation breaks conjuncts and matras (report §4.4, #55). Unit = word (default) or grapheme cluster (`examleaf-kinetic-typography` helper).
3. **Line height ≥ 1.4** for Indic text; marks above and below the line clip otherwise (safe-zone tokens `indic_note`).
4. **Code-switched lines** (Hinglish, English technical terms inside Hindi or Assamese sentences, as in the cue-sheet example "normal", "refraction"): use a font stack with the Indic family first and a Latin family that matches its weight second, or set the English word's span explicitly. Check the baseline alignment on the test sheet.
5. **Assamese is not Bengali.** Do not substitute Bengali spellings or glyphs for Assamese ones (narration library rule: "do not substitute Bengali for Assamese"). ৰ and ৱ must render.
6. **Hold longer.** Indic headlines use the `hold_times_s` Devanagari/Bengali-Assamese minima from the safe-zone tokens (a [Hypothesis] until the pilot reading test calibrates them).

## 4. Coverage verification (test sheet)

Render one 1080×1920 frame per Indic family through the harness (same headless Chrome build as production) containing:
- every consonant and independent vowel of the script;
- every dependent vowel sign on one consonant (कि की कु कू के कै को कौ…, কি কী কু কূ কে কৈ কো কৌ…);
- common conjuncts (क्ष, त्र, ज्ञ, श्र, द्ध, न्द; ক্ষ, ক্ত, ন্দ, স্ক, ঙ্গ) and reph forms (र्क, ৰ্ক);
- Assamese-specific ৰ ৱ and a sample word such as অসমীয়া;
- nukta forms (ड़, ढ़; ড়, ঢ়, য়);
- one mixed line with an English term.

Pass criteria (human review): no tofu boxes, no dotted-circle placeholders, conjuncts formed, matras positioned, no clipping at line-height 1.4. Record the frame SHA-256 in the change record and set that family's `script_coverage.<script>` from `claimed_verify` to `yes` in `fonts_registry` (MINOR version bump). The tokens' `common.font_policy.smoke_test_strings` give a minimal line per script for quick checks; the full sheet above is the release test.

A quick automatic pre-check in the page is `document.fonts.load('64px "<family>"', '<sample>')` before seeking, so a missing font fails loudly instead of silently falling back; it does not prove shaping is correct, so the human check stays.

## 5. Loading and determinism

- Fonts are vendored files with recorded SHA-256 in the asset library, loaded with `@font-face` from the job workspace; no network fonts at render time.
- The harness preloads fonts before the first frame resolves (`document.fonts.ready`), otherwise the first frames render in a fallback font and double-render hashes differ (#55, #17; see `examleaf-motion-harness`).

## 6. Fallback when coverage fails

1. Switch the role to a Noto-class family with full coverage (MINOR version bump).
2. If no stylistic family passes, use plain Noto for Indic text and keep the stylised font for Latin only.
3. Never ship a frame with tofu; never convert Indic text into an image made by an image model (#54).
