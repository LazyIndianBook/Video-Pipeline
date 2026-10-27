# Run log (`runs.jsonl`) schema

One JSON object per line, appended by `scripts/effort_policy.py`, with keys sorted. The file lives at `jobs/<lesson_job>/runs.jsonl`. It is the **effective-level log** that this skill owns. Totals are posted to `examleaf-observability-cost`, which owns the dashboard, money conversion and reconciliation.

## 1. `planned` event (written by `plan --log`)

| Field | Type | Meaning |
|---|---|---|
| `event` | `"planned"` | |
| `run_id` | 16-hex | `sha256(job|scene|task|round)[:16]`; the same inputs give the same ID |
| `job_id`, `scene_id`, `task` | string | |
| `model_alias` | `opus`, `sonnet` or `haiku` | After any #61 reroute |
| `model_id` | string or null | Pinned full ID; null only in sandbox mode |
| `effort_requested` | low … max | Never ultracode |
| `effort_effective` | level or null | Expected effective level from `supported_efforts` ([N23]); null = unknown, fill at record |
| `ultracode` | `false` | Always false; anything else is a defect |
| `round` | int | Authoring loop number (≤ 3) |
| `per_run_cap` | int or null | Tokens |
| `warnings` | string[] | Override, fallback, budget alert, #58, #61, #6 sandbox |

## 2. `completed` event (written by `record`)

| Field | Type | Meaning |
|---|---|---|
| `event` | `"completed"` | |
| `run_id` | 16-hex | Joins to `planned` |
| `task` | string | |
| `tokens_in`, `tokens_out` | int | From the runner's usage report; `tokens_out` includes thinking on 5.5 models [N26] |
| `cache_read`, `cache_write` | int or null | If reported |
| `tokens_total` | int | in + out |
| `effort_effective` | level | **As observed** in the session, not assumed (#2) |
| `status` | `ok`, `failed`, `stopped` or `escalated` | |
| `alerts` | string[] | Cap exceeded; lesson budget % or exceeded; > ~78K in one run ([V1] low whole video) |

## 3. Alert rules

| Alert | Trigger | Effect |
|---|---|---|
| Run exceeded its cap | `tokens_total > per_run_tokens[task]` | `record` exits 1: freeze further runs for this scene, escalate |
| Lesson budget exceeded | used + total > `per_lesson_tokens` | Exit 1: pause the lesson's animation runs |
| Lesson budget at N% | ≥ `alert_fraction` × cap | Logged; ops notified via observability-cost |
| Heavier than [V1] low video | total > 78,000 | Logged: review the brief and templates |
| Ultracode reported | `effective == "ultracode"` | Refused; batch stop; launch-script audit |

## 4. Example lines

```json
{"effort_effective": "high", "effort_requested": "high", "event": "planned", "job_id": "L-phy10-03", "model_alias": "opus", "model_id": "<pinned>", "per_run_cap": 60000, "round": 1, "run_id": "9f2c4e1a7b3d5c80", "scene_id": "phy-10-03-s01", "task": "scene_code_2d", "ultracode": false, "warnings": []}
{"alerts": [], "cache_read": 30100, "cache_write": 9800, "effort_effective": "high", "event": "completed", "run_id": "9f2c4e1a7b3d5c80", "status": "ok", "task": "scene_code_2d", "tokens_in": 41200, "tokens_out": 18750, "tokens_total": 59950}
```

The numbers above are illustrative, not measured.

## 5. Posting to observability-cost

Per lesson, post:
- token totals per `task` and `model_id`;
- run count;
- rounds per scene (median, max);
- the number of runs with fallback warnings;
- alert counts.

These map to the `costs.json` fields "Tokens in/out per model and per stage" (model IDs exact; compare to the cap) and "Failure classes" in `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §3. Log minimal metadata: never prompts, fixtures, secrets or student identifiers.

## 6. Integrity checks (pilot)

- Every `completed` line has a matching `planned` line.
- No `round` > 3 without an `escalated` status on round 3.
- For each run, `effort_effective` (completed) equals `effort_requested` (planned) unless a planned warning announced the fallback.
- `model_id` is constant across a lesson's scene-code runs, unless a recorded model switch re-ran QA (AD-03).
