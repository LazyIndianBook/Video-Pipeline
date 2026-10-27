# Hold-time rules

A hold is the time an element is fully readable before it changes or leaves. The rules below list each number with its source and status. Values live in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` → `hold_times_s`; the style tokens may raise but never lower them.

## 1. Rules

| Element | Minimum hold | Source | Status |
|---|---|---|---|
| Primary headline | 1.2 s fully readable before the next major transition | [N60] | Example figure, not a tested threshold |
| Headline in Devanagari or Bengali-Assamese | 1.8 s (1.5 × 1.2) | tokens; report §7.5 "longer for Hindi" | [Hypothesis]; calibrate with a reading test |
| Longer text | max(headline minimum, 0.3 s × word count) | tokens `per_word_floor_s` | [Hypothesis]; calibrate |
| Equation | until the narration finishes reading it, plus 0.5 s | report §7.5 | [Recommendation] |
| Important transformation (e.g. an equation rearranging) | 2–4 s after it completes | tokens (from `palette_and_typography_tokens.json`) | Source pilot target |
| Punchline before the next sheet | next sheet starts about 0.3 s after the line's last word | [V4-MP] | Style rule |

The Indic minimum applies by the **script of the text shown**, not the lesson language: a Latin label such as "refraction" inside a Hindi lesson uses the 1.2 s minimum; a Devanagari headline uses 1.8 s.

General: **no exit animation before a hold ends** (tokens `no_exit_animation_before_hold_ends: true`).

## 2. Formulas

```text
fully_visible_at = last unit at + entrance duration
hold_s           = exit_at - fully_visible_at
required_hold_s  = max(headline_min × (indic_multiplier if Indic else 1), per_word_floor × words)
equation_exit_at >= narration_end_of_equation + 0.5
pass if hold_s >= required_hold_s
```

`exit_at` is the time the element starts to leave or is covered: the next sheet transition, the element's `hold` cue `until`, or the scene end.

`grapheme_clusters.py --plan … --exit-at T --hold-min 1.2 --indic-multiplier 1.5` computes `fully_visible_at`, `hold_s`, `required_hold_s` and warns when the hold is short. (The per-word floor is applied by QA; add it to the plan when the line has more than four words.)

## 3. Worked example (harness example cue sheet)

The example Hindi sheet ends at 7.4 s; the last word "हैं" starts at 6.65 s. With cluster units, a 0.045 s stagger and a 0.35 s entrance, the line is fully visible at 6.95 s, so the final hold is 0.45 s against a required 1.8 s. Fixes, in order of preference:
1. move the next transition later (cue-sheet owner), if the scene can extend into a pause;
2. show fewer words on screen (only the key term "refraction" as a label, held to the end);
3. never speed up narration or shorten the approved script to make room (pacing-controller rule).

## 4. Who checks

- This skill: at planning time (warnings must be resolved before authoring).
- Scene template: `W_HOLD_SHORT` warning at runtime in `window.__errors`.
- `examleaf-anim-qa`: hold-time check on rendered frames.
- `examleaf-pacing-controller`: owns the measured narration timing and hold schedule; this skill consumes it.

## 5. Regeneration (#63)

When TTS is regenerated, word times move. Re-align → rebuild the cue sheet → re-run `--plan` → re-check holds → re-render. Scene code stays unchanged because no time is hard-coded.
