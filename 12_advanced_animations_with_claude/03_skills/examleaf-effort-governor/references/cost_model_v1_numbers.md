# [V1] effort numbers and how to use them

**Source:** [V1] Devarf, "I Had Opus 5.5 Make the Same Music Video at Every Effort", Claude Code 2.1.287, Opus 5.5, terminal, 2–4 Oct 2026. These are one creator's single runs, estimated at API prices; he paid nothing extra on a subscription. "Per-level values for medium, high and xhigh were not stated in the transcript, and the ultracode token count is a lower bound" (report §11 item 7).

## 1. The measured table

| Run | Visual | Wall time | Tokens | Est. API price |
|---|---|---|---|---|
| Low | 2D | ~42 min | ~78K | ~$3 |
| Medium–xhigh | 3D | between low and max (not stated) | — | — |
| Max | 3D | ~3 h | ~625K | ~$49 |
| Max + ultracode | 2D character on a 3D playing-card stage | did not finish | ≥2.5M (some agent logs missing counts) | ≥$348 |

**Task:** "a full music video, like a real official one", motion graphics only, for a 79-second song clip. It was built from scratch with a tools folder (three.js, Canvas 2D, SVG, frame conversion) and **no guides or examples**, after a custom audio-analysis step at high effort. All six runs delivered the full 79 s with the original audio matched.

## 2. Derived ratios (arithmetic on the table, not new measurements)

| Ratio | Value | How |
|---|---|---|
| Tokens, max vs low | ~8× | 625K / 78K |
| Est. price, max vs low | ~16× | $49 / $3 |
| Wall time, max vs low | ~4.3× | 180 / 42 min |
| Ultracode vs max, tokens | ≥4× | 2.5M / 625K |
| Ultracode vs max, est. price | ≥7× | $348 / $49 |
| Implied blended est. price per 1K tokens | ~$0.04 (low), ~$0.08 (max), ≥$0.14 (ultracode) | price / tokens |

The implied per-1K figures are **not prices**: they blend input, output, thinking and cache in unknown proportions. Use them only to see that higher effort shifts the mix towards expensive tokens. Never use them for billing. observability-cost prices tokens from the current official price sheet.

## 3. How ExamLeaf uses these numbers

1. **As ceilings, not forecasts.**
   - A single ExamLeaf scene-code run that exceeds ~78K tokens (the whole low-effort video) triggers a "review the brief" alert in `effort_policy.py record`.
   - A per-run cap configured above ~625K (the whole max video) triggers a warning at plan time.
2. **As the case against ultracode.** The ultracode row is the evidence for refusing ultracode outright (#3) rather than budgeting it.
3. **As the case for explicit effort.** The token curve is steep, so leaving effort to defaults (medium on 5.5 [N22]) or bumping it casually changes cost by multiples.
4. **As a pilot hypothesis.** Template-based scenes (harness, style, data pre-supplied) "should land far below these figures" ([Hypothesis], report §3.3). The pilot (`12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/`) measures tokens per scene for the three test lessons. Replace every cap with measured p50/p95 values after it.

## 4. How not to use them

- Do not divide 625K tokens by 79 s and multiply by a lesson length. Lessons are mostly data-bound SVG and Manim scenes, which use no animation LLM at render time. Only illustrative scenes (hooks, analogies, recaps) get bespoke Claude code (section 00 §7).
- Do not treat the $ figures as ExamLeaf costs. They are one creator's API-price estimates, he was on a subscription, and Max plans start "From $100" per month [N74]. [V1] burned almost three 5-hour windows with one ultracode run, so the subscription limits are a second budget besides money.
- Do not assume medium, high or xhigh sit on a straight line between low and max. The per-level values were not stated.

## 5. Budget-cap worksheet (founder fills in; `templates/budget_caps.json`)

| Cap | Initial value | Basis | Replace with |
|---|---|---|---|
| `per_run_tokens.scene_code_2d` | founder sets | Must stay well under ~78K ([V1] low whole video) | Pilot p95 per scene × 1.2 |
| `per_run_tokens.scene_code_complex` | founder sets | Justify if > 78K; warn above ~625K | Pilot p95 |
| `per_run_tokens.brief_text` / `storyboard_text` / `prompt_assembly` | founder sets | Sonnet medium text work | Pilot p95 |
| `per_run_tokens.render_debug` | founder sets | Logs + failing frame time only | Pilot p95 |
| `per_run_tokens.batch_clerical` | founder sets | Haiku prompts must stay < 100K [N28] | Pilot p95 |
| `per_lesson_tokens` | founder sets | Separate from the $1.72 S2–S8 LLM line (`08_COST_TRACKING_and_BUDGETS.md` §1), which excludes animation | Pilot total per lesson × 1.2 |
| `alert_fraction` | 0.8 | Early warning | Keep unless noisy |

No number is pre-filled. "No cap, no run" in production mode is deliberate: an invented cap would look like a measurement.
