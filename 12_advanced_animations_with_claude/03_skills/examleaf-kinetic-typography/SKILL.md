---
name: examleaf-kinetic-typography
description: "Use when on-screen words in an ExamLeaf scene or Reel must animate in sync with narration: headlines, key terms, ransom-note titles, handwriting captions, washi-tape labels, quiz prompts and equation callouts, in English, Hinglish, Hindi or Assamese at 1080x1920. Times every unit from the cue sheet's word timings (reveal on, or about 0.05 s before, the word), uses one orchestrated staggered entrance per beat, named and banned fonts, headline holds of at least 1.2 s (longer for Indic text) and the equation hold rule. Splits Devanagari and Bengali-Assamese text into grapheme clusters with a stdlib helper and never animates per code point. Does not write or edit wording, author captions, or draw science glyphs."
---

# examleaf-kinetic-typography

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. `scripts/grapheme_clusters.py --selftest` passes offline (15 cluster cases including Devanagari conjuncts, reph, nukta, Assamese ৰ/ৱ, ZWJ/ZWNJ, plus planning and hold checks). Indic shaping in the render box's headless Chrome is not yet verified (report §11.10).
- **Owns:** the typographic animation plan per scene (units, times, mode, holds) and the type-animation code patterns.
- **Does not own:** the words themselves (approved script via the cue sheet; never edited here), narration captions (`examleaf-speech-animation-synchronizer` authors timed captions; `examleaf-audio-caption-qa` corrects them), fonts and palettes (`examleaf-style-guides`, licensed files in `examleaf-asset-library`), science glyphs such as equations, units and labels' values (fixture renderers: `examleaf-manim-scenes`, `examleaf-svg-scenes`), the cue sheet (`examleaf-cue-sheet`).
- **Why it exists:** [V3] and the frontend-aesthetics cookbook show kinetic typography keyed to word timestamps, "one well-orchestrated page load with staggered reveals" [N53], dominant colours with sharp accents [N52], and distinctive fonts instead of Arial or Inter [N51] that still converge on common choices such as Space Grotesk [N55]. [N60] gives a 1.2 s headline hold (an example figure). [V4-MP] defines three text kinds: ransom-note tiles landing 0.04–0.05 s apart, Caveat Brush handwriting with a red double underline, Patrick Hand labels on washi-taped tags. Report §4.4 warns that per-letter animation can break Devanagari conjuncts (#55). Report §10.7 specifies this skill.

## Invocation

**Trigger when:**
- A scene routed `typographic`, or an illustrative scene with on-screen words, needs those words animated.
- A Reel needs a hook headline, a term card, a quiz prompt or a recap line.
- TTS was regenerated and type timings must be re-planned (#63).
- QA reports tofu, broken conjuncts, unreadably short holds or out-of-sync reveals.

**Do not trigger for:**
- Writing, shortening, translating or "punching up" text (script and localisation skills own wording).
- Full narration subtitles/captions (`examleaf-speech-animation-synchronizer`).
- Typesetting equations, units or numeric values (fixture renderers); this skill only times the reveal and hold of an equation element it is given.
- Generating text inside images (forbidden, #54).

## Inputs

| Input | Type | Source |
|---|---|---|
| Cue sheet | `words[{w,t0,t1,lang?,occurrence?}]`, `cues[{id,at,kind,element_id,word_index,until}]`, `language` | `examleaf-cue-sheet` (schema `04_harness_contract/cue_sheet.schema.json`) |
| On-screen text spec | which words or phrases appear, in which element, in which mode | brief (from the approved storyboard) |
| Style tokens | font roles incl. `devanagari`, `bengali_assamese`, banned list, palette, `animate_indic_per` | `examleaf-style-guides` |
| Hold and motion tokens | `hold_times_s` (headline 1.2; Devanagari/Bengali-Assamese 1.8 [Hypothesis]; per-word floor 0.3 [Hypothesis]; equation +0.5), `motion.reveal_lead_s` 0.05, `ransom_letter_stagger_s` 0.04–0.05 | `04_harness_contract/vertical_safe_zones.tokens.json` |
| Typography sizes | `typography_px_at_1080` minima (label 50, equation 63, heading 59 px; derived, not phone-tested) | same tokens file |

Example type spec:

```json
{"scene_id":"phy-10-03-s04","elements":[
  {"element_id":"headline","mode":"kinetic","words":[0,1,2,3,4,5],"unit":"cluster","zone":"top_title"},
  {"element_id":"label_refraction","mode":"label","words":[16],"unit":"word","zone":"middle_visual",
   "hold_until_cue":"refraction_card_hold"}]}
```

## Outputs and contracts

1. **Type plan** (`templates/type_plan.example.json`): per element `{element_id, mode, unit, units[{text, at, word_index, unit_index, lang}], fully_visible_at, exit_at, hold_s, required_hold_s, font_role, zone, warnings}`. Produced for each element with `grapheme_clusters.py --plan` (cluster or word mode).
2. **Scene code fragments** following `references/type_modes.md`: spans built once in `window.ready`, times from the plan, styles set in `render(t)`.
3. **Glyph test result** for Indic fonts (pass/fail + frame SHA-256), shared with `examleaf-style-guides`.
4. **`handoff.json`** (library schema).

## Dependencies

- Python 3 standard library (`grapheme_clusters.py`); uses `unicodedata` (Unicode version reported in output; 16.0.0 on the authoring machine).
- Browser: `Intl.Segmenter(lang, {granularity: 'grapheme'})` is the in-page splitter; compare its output with the helper on the glyph test sheet, because conjunct handling depends on the ICU build (verify per Chrome version).
- Fonts: licensed, vendored, preloaded with `document.fonts.load` before the first seek (harness rule R05, #55).
- Harness contract and template: `04_harness_contract/contract.md`, `scene_template.html` (its headline builder already applies the 0.05 s lead and a hold warning).

## Execution

1. **Read** the cue sheet and type spec. Confirm every on-screen word exists in `words[]` (by index and `occurrence`), so no text is typed by hand (#63, #11).
2. **Choose the unit:** Latin ransom tiles → per letter; Devanagari/Bengali-Assamese → per grapheme cluster (tiles, opacity pops) or per word (handwriting, labels, continuous headline bar). Never per code point (#55).
3. **Plan each element:**
   ```sh
   python3 12_advanced_animations_with_claude/03_skills/examleaf-kinetic-typography/scripts/grapheme_clusters.py \
     --plan jobs/phy-10-03-s04/inputs/cue_sheet.json --mode cluster --stagger 0.045 \
     --exit-at 7.4 --indic-multiplier 1.5
   ```
   Use the `--exit-at` of the element (next sheet time or hold cue `until`). Any hold warning must be resolved (delay the exit cue via the cue-sheet owner, or reduce on-screen words through the script owner) before authoring.
4. **Orchestrate one staggered entrance per beat** [N53]: one element group enters with a stagger; avoid scattered micro-animations. Ease with back.out for pops, power3.out for slides ([V4-MP]).
5. **Build spans once** in `window.ready` (one span per unit, `lang` attribute set per word, Indic font stack first), then in `render(t)` set opacity/transform from the plan times.
6. **Fonts:** only roles from the style tokens; Arial, Inter and Space Grotesk never as display faces [N51][N55] (Inter only in label/caption/science-text roles per `common.font_policy.inter_allowed_for`); rotate display faces between Reels; preload; line-height ≥ 1.4 for Indic.
7. **Equation elements:** reveal the whole element (mask or fade) on its cue; hold until the narration finishes reading it plus 0.5 s; never scramble or per-symbol animate an equation.
8. **Glyph test** for any new Indic font or Chrome version (`references/indic_text_rules.md` §5).
9. **Lint and double-render** through `examleaf-motion-harness`; hand off.

## Decision rules

- **Sync:** unit `at` = word `t0` − 0.05 s (never after `t0`); clusters of one word spread within the word's span at ≤ the stagger ([V4-MP]).
- **Ransom stagger:** 0.04–0.05 s between tiles ([V4-MP]); tile rotation ±6°, seeded via `rngAt` (never `Math.random`).
- **Holds:** required = max(headline minimum × Indic multiplier if Indic, per-word floor × words); equation = narration end + 0.5 s; important transformations 2–4 s (tokens). No exit animation before the hold ends.
- **Script boundaries:** a code-switched English word inside a Hindi line uses its own `lang` and Latin font; tiles in ransom mode for Indic words use the Indic family (display fonts are Latin-only [Hypothesis; verify per font]).
- **Size:** at least the token minima; split or enlarge, never shrink below (tokens rule).
- **Short text only:** on-screen text is a title, number or punchline word, never full narration sentences ([V4-MP]); long text means a caption, owned elsewhere.

## Edge cases handled

| Master # | Detection | Response |
|---|---|---|
| 50 Short headline hold | `plan` hold warning; template `W_HOLD_SHORT`; anim-qa hold check | Block authoring until exit moves or text shrinks; Indic uses the longer minimum [N60] |
| 55 Indic glyph gaps / broken conjuncts | `--mode codepoint` refused; `per_codepoint_would_split` true; glyph test tofu or dotted circles; `Intl.Segmenter` disagreement with helper | Cluster or word units only; Noto-class fallback font; glyph test sheet before release |
| 63 TTS regenerated | Cue sheet hash changed | Re-run `--plan`; scene code unchanged because all times come from the cue sheet |
| 8 (supporting) Generic fonts | Arial, Inter or Space Grotesk in a display role; same display face in consecutive Reels | Refuse; use style roles [N51][N55] |
| 54 (supporting) Text in images | Request to bake a title into a generated image | Refuse; build in code |
| 11 (supporting) Text edits | Requested wording differs from `words[]` | Refuse; route to the script owner |

## Tests and acceptance

- **Helper:** `python3 scripts/grapheme_clusters.py --selftest` (15 segmentation cases; plan mode lead and hold warning; word mode; code-point mode refused; code-point vs cluster counts).
- **Plan on the harness example:** `--plan 04_harness_contract/cue_sheet.example.json --exit-at 7.4 --indic-multiplier 1.5` produces 46 units and flags the 0.45 s final hold against the 1.8 s requirement — the expected teaching example of #50.
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance per scene:** every on-screen word maps to a cue-sheet word; no hold warning; glyph test passed for the fonts used; lint and double render pass; a native reader confirms Devanagari/Assamese rendering.

## Errors, fallback, escalation

- **Hold too short:** ask the cue-sheet owner to move the exit/transition cue, or the script owner to reduce on-screen words; never speed up the narration to fit (pacing-controller rule).
- **Shaping failure in Chrome:** switch to word units; if still broken, change font family (style-guides MINOR bump); never rasterise text through an image model.
- **Segmenter disagreement:** treat the browser's output as suspect until the glyph test passes; prefer word units.
- **Repair attempts:** at most two; then a structured blocker naming the element, the word index and the failing check.
- **Cost cap:** code only.

## Cost/performance

Zero credits; planning is instant. Per-cluster spans add DOM nodes; keep on-screen text short (it should be short anyway).

## Security

- Text comes only from the approved script via the cue sheet; the helper treats input as data and never evaluates it.
- Fonts are local, licensed, pinned files; no web-font fetch at render time (lint F12).
- Nothing is published.

## Handoff

- **To:** the scene-authoring run (type plan + patterns), `examleaf-motion-harness`, `examleaf-anim-qa` (hold and glyph checks), `examleaf-style-guides` (glyph test results).
- **Files:** type plan JSON per element, glyph test frame hash, `templates/handoff.json` (`output_ids` = plan SHA-256).

## References

- `references/type_modes.md`: ransom, handwriting, label, kinetic headline and equation modes with code patterns.
- `references/indic_text_rules.md`: grapheme clusters, conjuncts, shirorekha, fonts, code-switching, glyph test, helper limits vs UAX #29.
- `references/hold_time_rules.md`: hold formulas, sources and status of every number, QA checks.
- `references/contract.md`: handoff and security rules.
- Report §4.4, §7 (rules 1–7), §8 (#50, #55, #63), §10.7, §11.10.
