# Indic text rules (Devanagari, Bengali-Assamese)

## 1. Why never per code point (#55)

A Devanagari or Bengali-Assamese "letter" on screen is often several code points: consonant + virama + consonant (conjunct), consonant + dependent vowel sign, nukta forms, reph, anusvara and chandrabindu. Animating code points separately draws a half-letter, a floating vowel sign or a dotted-circle placeholder, and breaks conjuncts (report §4.4 [Hypothesis], §8 #55).

Examples from the helper's selftest:

| Text | Code points | Clusters (helper) |
|---|---|---|
| क्षत्रिय | 8 | क्ष · त्रि · य |
| हिन्दी | 6 | हि · न्दी |
| प्रकाश | 6 | प्र · का · श |
| ज्ञान | 5 | ज्ञा · न |
| धर्म (reph) | 4 | ध · र्म |
| অসমীয়া (Assamese) | 7 (decomposed) | অ · স · মী · য়া |
| নমস্কাৰ (Assamese ৰ) | 7 | ন · ম · স্কা · ৰ |
| ৱাৰ্তা (Assamese ৱ) | 6 | ৱা · ৰ্তা |

Note the pre-base vowel sign ि in हि and त्रि: it is stored after the consonant but drawn before it, so it must stay in the same unit.

## 2. Units by mode

| Mode | Latin | Devanagari / Bengali-Assamese |
|---|---|---|
| Ransom tiles | letter | grapheme cluster (one tile each) |
| Kinetic pop | letter or word | grapheme cluster with zero spacing, or word |
| Handwriting | letter (clip) | word (mask wipe) |
| Label | word | word |
| Equation | whole element | whole element |

## 3. The helper and its limits

`scripts/grapheme_clusters.py` implements the parts of UAX #29 that matter for these scripts:
- marks (Mn, Mc, Me) and ZWJ/ZWNJ attach to the previous cluster;
- consonant + virama [+ ZWJ] + consonant stays one cluster (approximation of the Indic conjunct rule added in Unicode 15.1, GB9c), using hard-coded consonant ranges for Devanagari and Bengali-Assamese and "combining class 9" as the virama;
- ZWNJ after a virama ends the conjunct (explicit half-form);
- it does **not** implement Hangul, emoji sequences, regional indicators, Prepend or other Indic scripts.

In the page, use `Intl.Segmenter(lang, { granularity: 'grapheme' })`. Whether a given Chrome build keeps conjuncts together depends on its ICU version (verify). If the browser splits a conjunct that the helper keeps, use word units for that build.

## 4. Fonts and layout

- Noto-class families with full coverage are the safe default (report §8 #55 [Hypothesis]); candidate stylised families need the glyph test (`examleaf-style-guides/references/font_policy_indic.md`).
- Assamese needs ৰ (U+09F0) and ৱ (U+09F1); do not substitute Bengali spellings for Assamese.
- Line-height ≥ 1.4 (marks above and below the line clip otherwise; safe-zone tokens `indic_note`).
- Set `lang` on each word span (`hi`, `as`, `en`), so the browser picks script-appropriate shaping and fallback.
- Code-switched words (e.g. "normal", "refraction" inside a Hindi sentence, as in the cue-sheet example) keep `lang: en-IN` and a matching-weight Latin font.
- Numbers: use the digits the approved script uses (Latin digits or Devanagari/Bengali digits); never convert digit systems in animation.

## 5. Glyph test (per font and per Chrome build)

Render through the harness at 1080×1920 a frame containing: all consonants and independent vowels; every vowel sign on one consonant; common conjuncts (क्ष, त्र, ज्ञ, श्र, द्ध, न्द; ক্ষ, ক্ত, ন্দ, স্ক, ঙ্গ); reph forms; nukta forms (ड़, ढ़; ড়, ঢ়, য়); Assamese ৰ ৱ; one mixed Hindi-English line; one ransom-tile row and one word-wipe row. Pass = no tofu, no dotted circles, conjuncts formed, vowel signs placed, no clipping; reviewed by a native reader; frame SHA-256 recorded.

## 6. Pacing for Indic text

- Hold longer than Latin (report §7.5); the tokens carry Devanagari and Bengali-Assamese headline minima of 1.8 s as a [Hypothesis] (1.5 × 1.2 s) to be calibrated with target students.
- Fewer words per frame: one idea per frame matters more because Indic words are visually denser at the same size.
