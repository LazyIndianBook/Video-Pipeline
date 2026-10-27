# Style guide: kinetic-type (kinetic typography, 9:16)

**Style ID:** `kinetic-type` | **Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot
**Derived from:** the SaaS-style motion-graphics practice in [V3] and the frontend-aesthetics guidance behind [N50]-[N55] and [N60] (report §4.4, §7). Skill that implements it: `examleaf-kinetic-typography`. Route tag served: `typographic`.
**Machine-readable twin:** `style_tokens.json` (`styles["kinetic-type"]`).

**Evidence labels:** [V#]/[N#] from `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`. [Recommendation] = design judgement; [Hypothesis] = untested; "verify" = not confirmed. Edge cases #1-#65 (report §8). Project decisions RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## Digest (read this first; the full guide governs on conflict)

1. Text is timed from the cue sheet's `words[]` (`t0`, `t1`). Nothing is hard-coded. Each reveal lands on, or about 0.05 s before, its word.
2. Three modes: ransom (tiles), handwriting (reveal), label (pop). Latin may animate per letter; Devanagari and Bengali-Assamese animate per word or grapheme cluster, never per code point (#55).
3. One staggered entrance per beat [N53]. Dominant colour plus at most two accents [N52]. One highlighted keyword at a time.
4. Fonts: a named allow-list; ban Arial, Helvetica, Roboto, system-ui, Space Grotesk, and Inter as a display face [N51][N55]; rotate display faces between Reels.
5. Hold a headline at least 1.2 s [N60]; Indic text longer (multiplier 1.5 [Hypothesis]); equations until narration finishes reading them plus 0.5 s and at least 2 s after an important transformation (RD-02).
6. Only words from the approved script or approved on-screen text appear. Equations and science statements are never kinetic text; formulae arrive from fixtures as a unit.
7. Captions stay in the caption zone and stay static while kinetic text moves (#51). Kinetic text carries 1-3 key words, not the sentence.
8. Safe box from `04_harness_contract/vertical_safe_zones.tokens.json`; side margin at least 96 px.
9. Determinism: seek-driven, stateless seeded PRNG, finite repeats, no wall-clock CSS animation. Reduced-motion variant required.
10. Cost: zero credits.

---

## 1. Purpose

Kinetic type does four jobs in ExamLeaf:
1. **Hooks** (the first 0-3 s of a Reel): the 1-3 words that name the problem (for example `CHECK THE AXES`).
2. **Key-term pops** during narration: a term appears as it is spoken and stays while it is explained.
3. **Step and condition labels**: short tags such as "same voltage" (a condition, in amber).
4. **CTA cards**: one line and one action.

It is the wrong tool for: equations (data-bound, KaTeX from fixtures, animated as a unit by the equation skill), graph labels, structure labels, or any sentence that states a scientific fact. Those are fixture-driven (report §9; #12).

## 2. Inputs and identity checks

1. **Cue sheet** (`cue_sheet.json`; schema in `04_harness_contract/contract.md`; shape in report §5.5): `words[]` with `w`, `t0`, `t1`; `cues[]` with `id`, `at`, `kind`; `sfx[]`; `duration`.
2. **Display text.** The words shown come from the approved `display_text` fields of the script bundle (kept separate from `spoken_text`, ROOT/03). Mapping from display token to cue: `cues[].id` and `element_id`. Treat the display text like fixture data: mark each element `data-fx="display_text.<id>"` so QA can diff it [Recommendation].
3. **Identity check.** Every displayed token must exist in the approved script bundle (or its approved on-screen text list), in the same order. Any new, changed or reordered word is a blocker: return `blockers.json` and stop (#11).
4. **Timing source.** If the cue sheet is missing, stale (hash mismatch) or lacks a word, stop; do not estimate times (#63).

## 3. Modes

### 3.1 Ransom mode

- **Look.** Tiles with a letter (Latin) or a word (Indic) on each; rotation ±6° for letter tiles and ±3° for word strips; vertical jitter ±8 px; flat hard shadow 6 px at ink 18% (no blur). Tile colours from ExamLeaf tokens only: ink, blue, teal, purple, secondary, amber (conditions) with paper-white `#F7F9FC` letters, or paper tiles with ink letters. Paper-white on ink 15.15, on blue 6.15, on teal 4.87, on purple 6.48, on secondary 6.06, on amber 5.14 (each is the token ratio against `#F7F9FC`).
- **Unit.** Latin: per letter. Indic: per word strip.
- **Timing.** The first letter of a word lands at `max(0, t0 - 0.05)`; letters stagger **0.04-0.05 s**; the whole word is settled by `max(t1, t0 + n_letters × 0.045)` (if the word is spoken faster than the stagger allows, compress the stagger to a minimum of 0.02 s, then fall back to a word-level pop).
- **Sizes (1080-wide).** Tile edge 112-148 px; glyph em 80-110 px; at most 3 words, one word per row.
- **Use.** The hook words only.

### 3.2 Handwriting mode

- **Look.** Words reveal as if written: Latin by letter-by-letter reveal or a left-to-right mask wipe; Indic and Bengali-Assamese **always** by a per-word left-to-right mask wipe with a soft pen edge (never per code point). Colour: ink on paper, with an optional accent underline drawn after the word (0.30-0.40 s).
- **Duration.** Wipe time per word `min(word duration, 0.6 s)`.
- **Fonts.** A handwriting-style face with verified coverage (candidate Kalam for Latin and Devanagari; verify; no verified Assamese handwriting font, use Noto Sans Bengali with the wipe).
- **Sizes.** Em 64-88 px.
- **Use.** Punchline words, "now try it yourself" prompts, conditional wording.

### 3.3 Label mode

- **Look.** A short tag (at most 4 words) on a paper card with a keyline and a 2-3 px accent border; sans semibold (Noto Sans or Inter), ink on `#F7F9FC`.
- **Motion.** Pop with `back.out(1.4)` 0.25-0.30 s, or a slide of 20-30 px with `power3.out`; one tag at a time per beat.
- **Sizes.** 50-54 px (essential label floor, RD-18).
- **Use.** Key terms, conditions ("same voltage"), step names.

## 4. Timing rules

1. **Sync.** Reveal on the spoken word: the cue time `at` is in `[t0 - 0.05, t0]` (the cue-sheet validator rejects `at > t0` and warns above 0.10 s early; the template reveals at `t0 - 0.05`) [V4-MP sync rule; report §7.7; `04_harness_contract/contract.md` §8]. The entrance may then run on for up to about 0.30 s. One sentence is one beat.
2. **One staggered entrance per beat** [N53]. A beat has exactly one entrance group (the line or tag set that enters together, staggered 40-90 ms between items). No other element begins an entrance inside the group's window (at most 0.8 s). Scattered micro-animations are avoided.
3. **Dominant colour plus sharp accents** [N52]: ink and paper dominate; one subject accent; amber only when the text is a condition; red only as an error marker.
4. **Highlight.** One keyword at a time gets the accent (colour change or highlighter swipe, 300-600 ms), then returns to ink before the next highlight (ROOT/02 D4).
5. **Easing.** Anticipation, action, follow-through; never linear. Use `back.out` for pops, `power3.out` for slides, `expo.out` for whips ([V4-MP] vocabulary, report §7.4).
6. **Exits.** None by default; the next line replaces the previous with a 150-300 ms fade or slide (ROOT/02 E4 simple transition).
7. **Do not animate over a `think` window.** During `think` and `pause-video`, the prompt text stays still; the answer is hidden (ROOT/03).

## 5. Colour and contrast

- Palette: ExamLeaf light tokens (`#F7F9FC`, `#14213D`, `#526074`, `#185ABD`, `#087986`, `#9A5B00`, `#6E44AA`, `#B42318`); biology green `#1F7A3E` is a proposed new token (5.09:1 on the background; needs brand-owner approval). Light theme only (RD-27).
- Text at least 4.5:1; essential graphics at least 3:1. Check adjacent colours in the rendered frame: the accents sit very close in luminance (blue/purple 1.05, teal/green 1.05 computed), so colour alone never carries meaning (ROOT/02 D4).
- Highlighter and card tints are 18-28% mixes of an accent into the background; ink on those is at least 9.8:1 (computed).

## 6. Fonts: allow and ban

All fonts are vendored, hashed into the cache key and licence-checked before use (RD-23). No CDN at render time. Licence: verify per font.

**Allow (display)**: Latin: Bebas Neue, Alfa Slab One, Bowlby One, Bungee, Titan One, Lilita One, Abril Fatface, Playfair Display (the display faces named in [V4-MP]), Noto Serif Bold/Black; Indic display candidates to verify: Rozha One and Yatra One (Devanagari serif display), Baloo 2 (Devanagari), Noto Serif/Sans Devanagari and Bengali.
**Allow (support, labels, captions)**: Noto Sans family, Inter (labels and captions only, RD-23), KaTeX fonts for formulae.
**Ban as display**: Arial, Helvetica, Roboto, system-ui, generic `sans-serif`, Space Grotesk (a documented convergence choice [N55]), Inter as a headline face [N51], Times New Roman, Comic Sans, Papyrus.
**Rotate.** Repeated generations converge on the same picks [N55]; do not reuse the same display face in two consecutive Reels of one batch [Recommendation].
**Coverage.** A font passes only after a glyph smoke test (see §8). Never assume a family covers a script.

## 7. Hold times

| Item | Hold |
|---|---|
| Headline (1-3 words), Latin | at least **1.2 s** after it has fully landed [N60] |
| Longer copy | `hold_s = max(1.2 s, 0.3 s × word_count)` (`hold_times_s.per_word_floor_s` in the harness tokens) [Hypothesis] |
| Indic or Bengali-Assamese headline | the Latin hold × **1.5** [Hypothesis, tune in phone tests] (so at least 1.8 s) |
| Equation (from a fixture) | until the narration has finished reading it, plus **0.5 s** [report §7.5]; and at least **2 s** after an important transformation (RD-02: 2-4 s, longer when necessary; 1-3 s for minor ones; 1-2 s for a spoken contrast) |
| Simple prediction | 5-8 s, default `think` = 6 s, answer hidden (RD-11) |

No major transition inside a hold (#50). Equations are never kinetic text: the data-bound equation skill animates them as a unit; kinetic type may only sit beside them.

## 8. Indic and mixed-script rules (#55; locale-gated by RD-26)

1. **Unit of animation:** a word, or a grapheme cluster, never a code point. Devanagari conjuncts (for example the cluster in `क्ष`) and Bengali-Assamese conjuncts break if split.
2. **Segmentation.** Use whole words. Treat `Intl.Segmenter` grapheme segmentation of Indic conjuncts as [Hypothesis] to be confirmed in the pinned headless Chrome (report §11 item 10); until it passes, animate per word.
3. **No `letter-spacing`**, no `text-transform`, no disabled ligatures, no synthetic bold or italic. Use real weights.
4. **Line height** at least 1.4 (matras above and below) [Hypothesis].
5. **Fonts.** Noto Sans/Serif Devanagari and Noto Sans/Serif Bengali (verify the Assamese letters ৰ U+09F0 and ৱ U+09F1). Latin technical terms inside an Indic line use the Latin font; one `lang` attribute per run.
6. **Smoke-test strings** (shaping check only): `क्ष ज्ञ श्र द्ध विद्युत प्रतिरोध` and `ৰ ৱ ক্ষ জ্ঞ অসম`.
7. **End-state equality test.** The last frame of an animated word must be pixel-identical to the same word rendered statically; any difference is a shaping bug.
8. **Mode mapping.** Ransom becomes word strips; handwriting becomes a per-word mask wipe; label is unchanged.
9. **Digits.** Latin digits for science numbers unless the approved edition says otherwise; never mix systems in one expression.
10. **Language and review.** Hindi, Hinglish and Assamese text are drafts until a native speaker and a subject reviewer approve them (ROOT/03 §5.5). Hinglish in Latin script is allowed when the script was written that way; captions come from the original script, not from pronunciation respellings.

## 9. Caption interplay (#51)

1. The accessible caption track (accurate, selectable, from the same alignment) lives in the bottom caption zone and is never replaced by kinetic text (ROOT/02 D7).
2. Kinetic text carries 1-3 key words; it does not show the whole sentence that the captions show. The same word sequence is not displayed twice at once.
3. While kinetic text animates, caption highlighting stays static (no karaoke), so the learner is not asked to track narration + animated text + equation + moving captions together (ROOT/02 D7).
4. Kinetic text stays in the title and visual zones; nothing overlaps the caption plate.

## 10. Layout in 1080×1920

Stacked zones inside the platform-safe box (insets only from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them; the assembler blocks the brief if the file is missing; while `platform_insets_px.measured` is false its `applies_until_measured` insets are used and the job manifest records them as provisional):

| Zone | Share of safe-box height | Holds |
|---|---:|---|
| Title | top 22% | hook words (ransom or display type) |
| Visual | middle 54% | key-term pops, labels, fixture panels placed by other skills |
| Caption | bottom 24% | captions only |

- Side margin at least **96 px**.
- Elastic title zone [Recommendation]: three stacked rows of ransom tiles (3 × 112-148 px) do not fit in 22%; the title zone may grow to 30% of the safe-box height, taking space from the visual zone and never from the caption zone. Keep the top of the visual zone free in that scene, or place the second phrase in the visual zone as display type.
- Hook display type 96-150 px; supporting line 56-64 px; labels and captions 50-54 px; heading floor 59 px; equations (if beside) 63-81 px.
- At most 3 lines. Measure each line with the loaded font against the safe width; shrink within the size range, then wrap; if the text still cannot fit at 96 px, split the hook across two beats.
- Stacking: one word per row for ransom; left-aligned or centred consistently within a scene.

## 11. Motion vocabulary

Starting values [Recommendation]; simple transitions stay at 150-300 ms and highlights at 300-600 ms (ROOT/02 E4).

| Move | Spec |
|---|---|
| Mask reveal up | clip mask + translateY 40 px to 0, `power3.out`, 0.30-0.45 s |
| Slide in | 20-60 px, `power3.out`, 0.30 s |
| Pop | scale 0.85 to 1, `back.out(2)`, 0.25-0.35 s |
| Tracking settle | letter-spacing change is **not used on Indic**; for Latin only, 6% to 0 over 0.3 s |
| Emphasis | scale 1.00 to 1.08 to 1.00 over 0.35 s, once |
| Underline | draw-on 0.30-0.40 s |
| Highlighter | multiply swipe 0.35-0.50 s |
| Word swap | cross-slide 0.25-0.30 s |
| Whip (urgency) | `expo.out` about 0.4 s |

- **HTML note.** [N54] prefers CSS-only motion for HTML. Under seek rendering, wall-clock CSS animations are not allowed. Use declarative keyframes only if the harness seeks the Web Animations timeline (verify in the benchmark); otherwise drive a tween timeline from `seek(t)`.
- **No camera effects during label reveals** (#64). **No flashes** (#56). **Reduced motion:** no emphasis scale, no whips, no slide; reveal by 150-300 ms fade.
- Every repeat is finite; none is `repeat: -1` (#18).

## 12. Sound

- Light SFX from the cue sheet `sfx[]`: a soft tick on each word-level entrance (not on each letter), a whoosh on a slide, a pop on a label. Gains in the cue sheet.
- None during `think`, `pause-video`, equation reading or inspection.
- Music: optional in the hook or CTA, off under reasoning (ROOT/02 G5).
- Loudness -16 LUFS ±1, true peak at most -1 dBTP after the final mux (#39).

## 13. Writing

The words come from the narration system (#11). Hook patterns that suit this style are the backlog's truthful covers (REEL_BACKLOG §4):

| Topic | Cover text (kinetic hook) |
|---|---|
| Electricity | `CHECK THE AXES` |
| Algebra | `WHERE DID IT GO?` |
| Chemistry | `COEFFICIENT OR SUBSCRIPT?` |
| Biology | `TWO DIFFERENT COUNTS` |
| Product demonstration | `QUESTION -> REPAIR -> RETRY` |

Rules: the cover text accurately describes what the viewer gets; the hook is a genuine knowledge gap; no manipulative or false-urgency wording; no mastery claims; the answer is not withheld just to extend watch time (ROOT/02 I1).

## 14. Do and don't

**Do**
- Time every reveal from the cue sheet and keep the stagger inside one entrance group.
- Keep 1-3 key words on screen and let the captions carry the sentence.
- Test Indic strings statically and animated before use.
- Rotate display fonts.

**Don't**
- Animate a formula letter by letter.
- Add text that is not in the approved script bundle.
- Use `letter-spacing` or per-code-point splits on Indic text.
- Put kinetic text over the caption zone, or run karaoke captions at the same time (#51).
- Use full-frame flashes or camera effects during reveals (#56, #64).

## 15. Determinism

`window.DURATION` equals the cue sheet `duration`; `async window.seek(t)` sets every state; stateless keyed PRNG for jitter (`rnd(sceneId:elementId:step)`); finite repeats; fonts preloaded before the first frame resolves; double-render frame hashes identical (see `paper-collage-vertical.md` §15; `04_harness_contract/contract.md` is authoritative).

## 16. Cost

Zero credits. CPU rendering only.

## 17. QA checklist (`examleaf-anim-qa`)

- [ ] 1080×1920, 30 fps; DURATION equals the cue sheet; lint zero errors; double-render hashes identical.
- [ ] Every displayed token exists in the approved script bundle, in order.
- [ ] Every reveal cue `at` is in [t0 - 0.05, t0] of its word (the validator rejects later); entrances settle within about 0.30 s.
- [ ] Holds met (1.2 s, Indic ×1.5, equation rule).
- [ ] No banned font; every glyph rendered (no tofu); end-state equality test passes for Indic words.
- [ ] Safe box respected; captions static during kinetic text; no overlap with the caption plate.
- [ ] Contrast at least 4.5:1; one highlight at a time.
- [ ] No flash; reduced-motion variant renders.
- [ ] Loudness -16 LUFS ±1, true peak at most -1 dBTP.

## 18. Edge cases handled

#8 (fonts and palette), #11 (§2), #12 (§1), #17-#19 (§15, §11), #50 (§7), #51 (§9), #55 (§8), #56 (§11), #63 (§2, §4), #64 (§11).

## 19. Changelog

- 1.0.0 (15 Oct 2026): first version.
