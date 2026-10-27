# Estimate method

The estimate must be honest, reproducible and conservative. Every number has a stated source; nothing is invented.

## 1. Tokens

```text
tokens_expected   = Σ_scenes est_tokens
tokens_worst_case = tokens_expected × (1 + max_repair_attempts)
```

- **est_tokens source, in priority order:**
  1. `examleaf-observability-cost` history for the same style, route and effort (median per scene).
  2. `token_defaults_by_effort` agreed with `examleaf-effort-governor` and recorded with the job (the helper warns).
  3. None → the estimate is **blocked**. No basis, no number.
- **Reference points (not defaults):** [V1] measured about 78K tokens at low effort and about 625K at max for one 79 s music video built from scratch with no guides (report §1.4). An ultracode run wrote at least 2.5M tokens and never finished. ExamLeaf scenes use templates, skills and pre-supplied data, so they should land far below these figures [Hypothesis]; measure in the pilot.
- Effort matters: Opus 5.5 silently defaults to medium [N22]; scene code uses explicit high, complex 3D xhigh (report §3.4). Thinking cannot be switched off on 5.5 models [N26], so some thinking cost is always present.
- Converting tokens to money needs current per-token prices; they are not in the verified evidence set. Use the `claude-api` reference or the billing console at estimate time and record the source; never hard-code.

## 2. Credits

```text
image_generations_expected = Σ_scenes new_cutouts + (grids if any scene uses a generated grid else 0)
credits_expected           = image_generations_expected × credits_per_image
credits_worst_case         = credits_expected × (1 + max_repair_attempts)
```

- **credits_per_image:** from the operator's verified provider configuration (the provider dashboard or the mcp-orchestrator price table), recorded in `pricing.source`. The evidence set has no verified per-image credit price for GPT Image via Higgsfield (report §11.5). Unknown → blocked for paid panels.
- **Plan facts with their status:**
  - every agent generation deducts credits regardless of plan [N33];
  - no native credit cap; prompt limits are not hard limits [N34];
  - Starter $15/month for 200 credits and Plus $34/month for 1,000 credits are competitor-authored, unverified [N75];
  - premium video models use 40–70 credits per generation [N76] — excluded from this pipeline;
  - unlimited covers lower-tier models only [N79] and may be throttled [N80].
- **Caps:** `caps.credits` is the job cap (mandatory when credits are needed, #42). `caps.credits_remaining_on_plan` is the balance the operator reads before the gate (#45). Worst case must fit both, or the reviewer writes an override reason.

## 3. Why worst case = (1 + repairs) × expected

The library allows at most two repair attempts per failed unit. A repair may cost as much as the original (a regenerated cutout, a re-run scene). Using the full multiplier is conservative and simple; the ledger reports actuals afterwards so the next estimate can use measured repair rates.

## 4. What the estimate does not include

- Narration synthesis (owned and estimated by the narration path: `examleaf-voice-synthesis`, `examleaf-cost-regeneration-optimizer`).
- Music and SFX (code-composed by `examleaf-audio-compose`; CPU only).
- Render minutes (logged by `examleaf-render-batch` and `examleaf-observability-cost`).
These appear in the lesson budget elsewhere; the gate covers the visual layer's model tokens and image credits.

## 5. Reconciliation

After the segment ships, `examleaf-observability-cost` compares estimate vs actual per scene (tokens, effort, model ID, credits, fix loops). Large misses update `token_defaults_by_effort` and the price table — through their owners, not by editing old estimates.

## 6. Worked example (selftest numbers)

Segment with two code-thumbnail scenes, 60K and 80K estimated tokens, two repairs allowed:
- tokens_expected 140,000; tokens_worst_case 420,000; credits 0 → `awaiting_approval`.

Same segment with one collage scene needing 3 new cutouts and a generated grid, at an operator price of 5 credits per image (example value, not a real price):
- generations 4; credits_expected 20; credits_worst_case 60 → `over_cap` against a 50-credit job cap; fits a 60-credit cap.
