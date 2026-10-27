# 09 · Effort and cost governance

**Purpose.** Rules for choosing model, effort level and iteration budget for every animation task; the ban on ultracode in production; caching discipline; the ledger fields that record tokens, credits and time; alerts and stop rules; and the method for estimating what the animation layer adds to a lesson. Expands report §1.4, §3 and edge cases #1–#6, #57–#62.

**Status.** [PROPOSED]. No ExamLeaf scene has been authored with Claude Code yet, so every per-scene cost is unmeasured. The [V1] figures are one creator's single runs on a subscription, estimated at API prices (report §11 item 7). Prices and limits change: re-check before each phase gate, as `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §8 already requires.

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V#], [N#], ROOT-relative project paths, [Recommendation]/[Hypothesis], master edge cases #1–#65, NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`. One additional local reference is used and labelled **[CAPI]**: the `claude-api` skill bundled with the Claude Code build used to write this document (bundle 2.1.295; its model table is marked "cached: 2026-10-06"). [CAPI] figures are first-party API list prices; **verify on the live pricing page before budgeting**.

**Owning skills.** New: `12_advanced_animations_with_claude/03_skills/examleaf-effort-governor/` (extends `examleaf-observability-cost`). Existing: `examleaf-observability-cost` (pipeline ledger, reconciliation), `examleaf-cost-regeneration-optimizer` (narration jobs) — `06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 12. Paid generation: `12_advanced_animations_with_claude/03_skills/examleaf-mcp-orchestrator/` and `examleaf-selective-generation`.

---

## 0. Summary

1. **Set effort explicitly on every run.** Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to **medium** in Claude Code [N22] (#1). [CAPI] confirms Opus 5.5 and Haiku 5.5 default to medium on the API too.
2. **Defaults by task** (report §3.4): Sonnet 5.5 medium for brief/storyboard text; Opus 5.5 **high** for scene code; xhigh for complex three.js or physics; max only with a written justification; Sonnet/Haiku low–medium for clerical work.
3. **Never ultracode** in unattended or production runs. In [V1] max + ultracode wrote ≥ 2.5M tokens (≥ 4× max), was estimated at ≥ $348, used almost three 5-hour windows and never finished (#3).
4. **Pin full model IDs**; aliases resolve differently across providers [N28] (#6).
5. **Cap iterations:** at most 3 creative rounds per scene against the rubric, and at most 2 failed repair attempts before human escalation (ROOT/07 rule) (#60).
6. **One main session per scene batch**, stable prompt prefix, no mid-session model or effort changes, no multi-agent review fan-out.
7. **Log every run** (model ID, requested and effective effort, tokens, cache, time, rounds, outcome) to the ledger; alert at 50/80 %, stop at 100 % of cap.
8. **The animation layer needs its own cost line.** The current per-lesson LLM cap ($1.72, `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §1) was modelled for script and review work, not scene-code authoring.

**Consistency with the section decisions** in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`: this document implements AD-02 (effort policy), AD-03 (pinned IDs, model-agnostic), AD-11 (3 authoring loops; ≤ 2 repairs after QA), AD-20 (pipeline-enforced ledgers), AD-23 (bespoke code only for illustrative scenes, promoted to templates) and AD-24 (Opus vs Sonnet A/B in the pilot). Where wording differs, doc 14 records the decision.

---

## 1. Verified mechanics

| Fact | Detail | Source | Edge case |
|---|---|---|---|
| Default effort | "`high` on every model that supports effort, except that Opus 5.5, Sonnet 5.5, and Haiku 5.5 default to `medium`" | [N22] | #1 |
| Unsupported level | "Claude Code falls back to the highest supported level at or below the one you set" (e.g. xhigh runs as high on Opus 4.6) | [N23] | #2 |
| Ultracode launch | `claude --effort ultracode` "starts the session at `xhigh` effort with ultracode on" | [N24] | #3 |
| Ultracode cannot persist | "The persisted `effortLevel` setting and the `CLAUDE_CODE_EFFORT_LEVEL` environment variable don't accept `ultracode`" | [N25] | #4 |
| Thinking always on | "You can't turn thinking off on Opus 5.5, Sonnet 5.5, Haiku 5.5, or the Fable models" | [N26] | #5 |
| 4.6 fixed budget switch | `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` + `MAX_THINKING_TOKENS` on 4.6 models only (contested; not applicable to 5.5) | [N27] | — |
| Alias drift | Aliases "resolve to the newest version on the Anthropic API and to an earlier version on some other providers" | [N28] | #6 |
| Haiku long prompts | Haiku 5.5 prompts over 100K tokens cost more per token | [N28]; [CAPI]: $0.10/$0.50 per MTok up to 100K, $0.50/$2.50 beyond | #61 |
| Context and output | 1M-token context, up to 128K output tokens (as of the tutorial; recheck) | [N73]; [CAPI] lists 1M / 128K for Opus 5.5 and Sonnet 5.5 | #58 |
| Max plan | "From $100" per month | [N74] | — |
| Model IDs | `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`; use exactly, no date suffix | [CAPI] | #6 |
| API list prices (input/output per MTok) | Opus 5.5 $4 / $20; Sonnet 5.5 $2 / $10; Haiku 5.5 $0.10 / $0.50 (≤ 100K prompt); Fable 5.1 $10 / $50 | [CAPI]; these match the v1 workbook labels in `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §8 for Haiku/Sonnet/Opus 5.5 | — |
| Cache economics (API) | Writes 1.25× base input for the 5-minute TTL, 2× for 1-hour; reads ≈ 0.1× base, **0.05× on Opus 5.5** ($0.20/MTok); any byte change in the prefix invalidates what follows | [CAPI] | NEW-32 |
| Cache breakers (API) | Changing `thinking` or top-level effort between requests invalidates the messages cache; switching models mid-conversation breaks it (caches are per model) | [CAPI] | NEW-32 |

What is **not** verified: how Claude Code's subscription usage windows convert tokens into limit consumption; precise caching behaviour inside Claude Code sessions and across sub-agents (report §3.3, §11 item 1); any official cost per effort level.

---

## 2. What [V1] measured

Setup: Claude Code 2.1.287, Opus 5.5, terminal, one folder per run with a tools folder (three.js, Canvas 2D, SVG, frame converters) and **no guides or examples**; one prompt; a 79-second song clip; costs are estimates at API prices; the author paid nothing extra on a subscription [V1].

| Run | Visual | Wall time | Tokens | Est. API price | Implied $ per 1M tokens |
|---|---|---|---|---|---|
| Low | 2D | ~42 min | ~78K | ~$3 | ≈ $38 |
| Medium – xhigh | 3D | between low and max (not stated per run) | not stated | not stated | — |
| Max | 3D | ~3 h | ~625K | ~$49 | ≈ $78 |
| Max + ultracode (by mistake) | 2D character on 3D card stage | never finished; almost three 5-hour windows | ≥ 2.5M ("some agent logs are missing their final counts") | ≥ $348 | ≈ $139 |

The last column is this document's arithmetic. Two readings follow, both [Hypothesis]:
1. **"Tokens" in [V1] are tokens written, not all tokens processed.** At [CAPI] Opus 5.5 output pricing ($20/MTok), 625K written tokens alone would cost about $12.50, well below $49. The gap is consistent with large input/context re-reads in an agentic loop. Do not price agent work from output tokens alone.
2. **Cost per written token rises with effort and with multi-agent work** (≈ $38 → $78 → $139 per 1M). More effort means more turns re-reading a larger context; ultracode multiplies that across agents that "each … built its own cache" and restarted fresh after the limit [V1].

**Effort did change the result:** low produced 2D, medium to max produced 3D, and the author judged low "still good" [V1]. Quality comes mostly from the brief (report §0 item 14), so the governor spends effort on hard scenes only.

**ExamLeaf's unit is a scene built from templates, contracts, style guides and fixtures**, not a whole video built from nothing. Scene costs should land far below these figures [Hypothesis, report §3.3]. Measure in the pilot (`12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/`).

---

## 3. Per-task settings

From report §3.4 [Recommendation], with model IDs from [CAPI] (verify before pinning).

| Task | Model (pin) | Effort | Iteration cap | Notes |
|---|---|---|---|---|
| Brief assembly, storyboard text, prompt assembly | Sonnet 5.5 (`claude-sonnet-5-5`) | medium | 2 rounds | Structure matters more than depth |
| Scene code: 2D motion, kinetic type, collage, doodle | Opus 5.5 (`claude-opus-5-5`) | **high** (explicit) | 3 creative rounds; 2 failed repairs | [V2]: high or xhigh; "99% of the time you won't need anything more than extra" |
| Complex three.js, fixed-step physics replay, intricate choreography | Opus 5.5 | xhigh | 3 rounds; 2 failed repairs | max only with a written justification approved in the ledger |
| Debugging a render failure | Opus 5.5 | high | 2 attempts (ROOT/07) | Give logs plus the failing frame time |
| Batch re-renders, caption fixes, file operations | Sonnet 5.5 or Haiku 5.5 | low–medium | 1 | No creative judgement; keep Haiku prompts < 100K tokens (#61) |
| Audio composition script (Python) | Opus 5.5 | high | 2 rounds | Output is code; determinism tests decide |
| Any task | — | **never ultracode** in unattended or production runs | — | [V1]; [N24]; sandbox only, separate budget |

**Independent review stays a different model or agent** (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` RD-04: "independent reviewer ≠ author model"). Science checks are deterministic validators plus humans, never an LLM vote.

---

## 4. Setting model and effort explicitly

1. **Launch** each job headless in the terminal, one workspace per job ([V1], [V2]).
2. **Effort:** set it explicitly through one of the mechanisms the docs name: the `--effort` launch flag (shown with `ultracode` in [N24]; verify it accepts `high`/`xhigh` on the installed Claude Code version), the persisted `effortLevel` setting, or the `CLAUDE_CODE_EFFORT_LEVEL` environment variable ([N25] names both; verify accepted values). The job wrapper sets it; humans do not rely on defaults.
3. **Model:** pin the full model ID through the model flag or setting (verify the exact flag name for the installed version). Never write `opus` or `sonnet` in job scripts [N28].
4. **Record the effective level** (#2): store what the session reports, not only what was requested. If the session reports a lower level, the governor marks the run `effort_fallback: true` [N23].
5. **For API-side batch work** (e.g. bulk caption tasks run through the Messages API), effort is `output_config.effort` with levels low/medium/high/xhigh/max and thinking cannot be disabled on Opus 5.5 [CAPI].
6. **Audit job scripts** before each batch: grep for `ultracode` and alias names; a match blocks the batch (#3, #4, #6). *15 Oct 2026: implemented as `bash 12_advanced_animations_with_claude/04_harness_contract/preflight.sh --workspace <job folder>` (ultracode-effort and unversioned-alias scans, plus a secret scan; audit M11).*

---

## 5. Ultracode policy

1. **Banned** in production and in any unattended run.
2. It cannot become a default by accident: settings and environment do not accept it [N25]. The only path is the launch flag [N24], so the script audit (§4 step 6) is a complete control for job scripts.
3. **Sandbox use** (only to evaluate it): separate workspace, low effort (the author's untested suggestion [V1]), a hard token cap, a wall-time cap, and a named human watching. Record results as an experiment, not as production cost.
4. **Why:** multi-agent review loops, per-agent caches and fresh restarts multiplied cost in [V1]; it is "not a higher effort level" but a multi-agent mode (report §0 item 3).
5. *15 Oct 2026 (audit "Effort and ultracode conflicts"; AD-41):* `effort_policy.py` refuses ultracode in **every** mode, sandbox included, and in both task families (`strong` and the new `kit_cascade` for section 13's Kit slot-fill, with its own caps). An item-3 sandbox experiment, including section 13's attended S5 "Ultra" probe, is therefore **not** a policy exception in code: it needs founder approval and a provider-side spend limit, runs outside the governor and never touches production.

---

## 6. Thinking cost

Thinking cannot be switched off on the 5.5 models or Fable [N26] (#5). Consequences:
- Budget for thinking tokens even on clerical tasks; lower effort is the only control ([CAPI]: effort is "the only control" on Opus 5.5).
- Route clerical work to Sonnet or Haiku at low effort.
- Thinking display is omitted by default on current models [CAPI], so a long silent pause is normal; wall-time caps must allow for it.

---

## 7. Iteration caps (#60)

[V2]'s L3 prompt included "don't stop working until the animation matches the exact quality of the reference video". That is an unbounded loop (report §1.1: "a cost hazard").

| Loop | Cap | Stop condition | Escalation |
|---|---|---|---|
| Creative rounds per scene | **3** [Recommendation; report §3.4 example] | Rubric pass (`12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` §4) | Human director decides: accept, simplify, or reroute |
| Failed repair attempts (render, lint, determinism) | **2** | Check passes | Human escalation (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S16: "at most two failed repair attempts then human escalation") |
| Renderer crash | 1 retry after a targeted repair | Render passes | Escalate (S16) |
| Storyboard revisions | 2 | Human approval | Re-brief |
| Paid generation retries | 0 without reconciliation | Unknown job reconciled first (#43) | Founder approval for overruns |

**Prompt rule:** never "don't stop until perfect". Use "Stop after N rounds; report the rubric scores and the remaining defects."

A round is one agent attempt that produces a renderable scene plus its automated QA report. Repairs to the same defect count against the repair cap, not the creative cap.

---

## 8. Caching and session strategy

### 8.1 Rules [Recommendation unless cited]

1. **One main session per scene batch** (one lesson segment or one Reel). Do not fan out to parallel agents that each rebuild context ([V1]: each sub-agent "built its own cache"; unfinished agents restarted fresh).
2. **Stable prefix first, unchanged across scenes** (report §3.3): harness contract (`12_advanced_animations_with_claude/04_harness_contract/contract.md`), style guide (`12_advanced_animations_with_claude/05_style_guides/`), brand and style tokens, the brief template (`12_advanced_animations_with_claude/06_prompts_and_templates/`). Per-scene volatile material (cue sheet, fixture values, storyboard panel) comes after.
3. **No mid-session changes** to model or effort; on the API both break the cache [CAPI] (NEW-32). If a hard scene needs xhigh, run it in its own session.
4. **Isolation:** "do not inspect any of my older projects or folders" ([V3]) (#9). Reading sibling folders contaminates output and bloats context.
5. **Split long scene files** so no single generation approaches the output limit [N73] (#58).
6. **Cache economics on the API** [CAPI]: a 5-minute-TTL write costs 1.25× and is repaid by the second read; requests sharing a prefix that start less than 5 minutes apart keep it warm. For bursty batch jobs with 5–60-minute gaps, the 1-hour TTL (2× write) may pay off. This applies to API-run pipelines; for Claude Code subscription sessions the mechanics are not verified — measure.

### 8.2 Sub-agents

Allowed only for bounded, read-only lookups (e.g. finding a fixture field). Not allowed for parallel "review" of scene videos: QA is deterministic scripts plus humans (doc 10). Every sub-agent run must report tokens to the ledger; missing counts are a defect (NEW-26, from [V1]'s missing agent logs).

---

## 9. The ledger

### 9.1 Where records go

- Per-run records: each job writes `logs/run.json` per Claude Code invocation in its job folder (`12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` §7.5); `examleaf-effort-governor` copies it to `lessons/<…>/anim/ledger/<run_id>.json` with the fields below. The skill's own effective-level log is `runs.jsonl` (planned and completed events) and its caps file is `budget_caps.json` (`per_run_tokens` per task, `per_lesson_tokens`, `alert_fraction`), set by the founder (`12_advanced_animations_with_claude/03_skills/examleaf-effort-governor/`).
- Rolled up into `lessons/<…>/costs.json` (fields in `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §3), owned by `examleaf-observability-cost`.
- Paid jobs (Higgsfield or other MCP) also use `ProviderJob` and the SQLite `BudgetLedger` (`07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §3.9, §3.15): reserve before submitting, settle actuals even on overrun, never resubmit an unknown job. AD-20 reuses `04_video_engine/implementation_v2/src/examleaf/budget.py` with one ledger instance per unit (cents, credits, kilotokens); the `unit` column and a `release` transition are build items.

### 9.2 Per-run record fields

| Field | Type | Note |
|---|---|---|
| `run_id`, `lesson_id`, `scene_id`, `short_id` | str | Join keys |
| `task_type` | enum | brief · storyboard · scene_code · threejs · audio_script · debug · clerical |
| `claude_code_version` | str | e.g. as reported by the CLI |
| `model_id` | str | Full ID; `alias_used` must be false |
| `effort_requested`, `effort_effective`, `effort_fallback` | str, str, bool | #1, #2 |
| `ultracode` | bool | Must be false; true blocks the batch |
| `session_id`, `subagent_count`, `subagent_tokens_missing` | str, int, bool | NEW-26 |
| `tokens_input`, `tokens_output`, `tokens_cache_read`, `tokens_cache_write` | int | From the session usage report or telemetry (mechanism: verify for the installed version) |
| `est_cost_api_usd` | float | Tokens × [CAPI] prices at the recorded price date; labelled estimate |
| `plan_window_fraction` | float or null | Manual entry if on a subscription |
| `wall_time_s` | float | Authoring time |
| `round`, `repair_attempt` | int | §7 caps |
| `outcome` | enum | rubric_pass · rubric_fail · repair_escalated · aborted_cap |
| `rubric_scores` | object | From doc 10 §4 |
| `render_seconds`, `render_box` | float, str | From the render manifest |
| `credits_estimated`, `credits_actual`, `provider_job_ids` | int, int, list | MCP only (#41–#45) |
| `reviewer_minutes` | object | Timed by role (`07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §3) |
| `price_table_date` | date | Re-check before each phase gate |

### 9.3 What the governor does with it

1. **Before a run:** check the remaining scene, lesson and batch caps; refuse to start if the expected spend exceeds them.
2. **During a run:** enforce wall-time and round caps (the job wrapper kills the session at cap).
3. **After a run:** write the record; update roll-ups; raise alerts (§10).
4. **Weekly:** compare estimated and actual spend; feed `examleaf-observability-cost` reconciliation (the daily provider reconciliation in `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §2 applies to paid MCP jobs).

---

## 10. Budget alerts and stop rules

| Trigger | Action | Basis |
|---|---|---|
| Scene reaches 50 % of its token cap | Optional info alert to the director | [Recommendation]; the governor skill's single configurable alert is `alert_fraction` (default 0.8) |
| Scene reaches 80 % | Warning; agent told to finish the current round and report | [Recommendation] |
| Scene reaches 100 % | **Hard stop**; human decides | `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §1 "Batch pauses on budget exhaustion" |
| Reserving beyond a cap | Founder approval recorded in the ledger | RD-40 |
| `ultracode: true`, alias in a job script, or `effort_effective` ≠ requested | Block batch | #3, #4, #6, #2 |
| Credits: estimate missing, or job unknown | Freeze generation for that provider until reconciled | "Freeze generation when invoice/cost state is unresolved" (`examleaf-observability-cost`); #42, #43 |
| One lesson consumes more than one 5-hour usage window | Pause and review | [Recommendation], from [V1]'s three-window run |
| Rising human repair minutes | Alert | `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §1 |
| Repeated identical failure | Stop; no blind regeneration | NA rule: "a second unknown or repeated failure requires review" |

**Provisional caps before pilot data** [Hypothesis]: per scene, the [V1] **low-effort whole-video** figure (~78K tokens) is a generous ceiling for one scene built from templates; per Reel, 3 scenes' worth; per lesson, set after the first three pilot scenes. Replace all with measured p90 values after the pilot (RD-40 pattern).

---

## 11. Estimating the animation cost of a lesson

### 11.1 Method

```
For each scene s in the lesson:
  route(s) ∈ {data-bound, spatial-hero, illustrative-narrative, typographic}
  if route(s) == data-bound and an approved template exists:  agent tokens ≈ 0 (render only)
  else: tokens(s) = rounds(s) × tokens_per_round(task_type(s), effort(s))
cost_api_est = Σ_s [ in(s)·p_in + out(s)·p_out + cache_read(s)·p_read + cache_write(s)·p_write ]
cost_total   = cost_api_est + credits·credit_price + render_minutes·render_rate + reviewer_minutes·rates
```

- `p_in`, `p_out`, `p_read`, `p_write` from [CAPI] for the pinned model (verify live). On a subscription, still compute `cost_api_est` for comparability, as [V1] did, and record plan-window usage separately.
- `tokens_per_round` comes from pilot measurements by task type and effort. Until then, use §10's provisional ceiling.
- Human rates and minutes follow `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §6 (one table of unit rates). "Machine cost is not total cost."

### 11.2 Upper-bound arithmetic from sourced numbers only

Suppose a lesson needs 7 non-template scenes (a hook, an analogy, a recap and four typographic or illustrative inserts). Using [V1]'s whole-video estimates as per-scene ceilings:
- at [V1] **low** (~$3 each): ≤ ~$21 per lesson;
- at [V1] **max** (~$49 each): ≤ ~$343 per lesson.

Both are deliberately pessimistic, because each [V1] figure is a whole 79-second video built from nothing. Even the low bound is about 12× the current per-lesson LLM cap of $1.72 (`07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` §1). Conclusions:
1. The runbook needs a **separate "animation authoring" cost line**, capped after the pilot (proposed amendment in `12_advanced_animations_with_claude/02_documentation/11_INTEGRATION_with_ExamLeaf_pipeline.md` §7).
2. **Max effort is excluded by budget**, not only by taste.
3. **Template reuse is the main lever**: once a scene template is approved, later lessons re-render it with new fixtures at near-zero agent cost.

### 11.3 Reels

`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` §6 models a three-Short package at ≈ $4.32 per source lesson, before any Claude-authored animation. Reels that re-seek lesson scenes (doc 11 §6) add little agent cost; Reels with new illustrative hooks add one scene each. Count Shorts once against the business "Reels" line.

### 11.4 Credits (Higgsfield and other MCPs)

- Every agent generation deducts credits whatever the plan [N33]; "There's no native credit cap" [N34] (#41, #42).
- Plan prices in the evidence are competitor-authored and unverified ($15/month for 200 credits; $34/month for 1,000) [N75]; premium video models cost 40–70 credits per generation [N76] and can exhaust Starter in 3–5 days [N77] (#45). ExamLeaf avoids premium video entirely (report §6.1).
- Per-scene generated-asset cap: `max_scene_estimate_cents: 200` (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S8); generated video default 0 s (RD-39).
- Storyboard grids from code thumbnails cost no credits; prefer them (doc 11 step 4).

---

## 12. Model changes

- **Fable 5.5 claims are unverified** ([V5]; #57). [CAPI] lists Fable 5.1 at $10/$50 per MTok, 2.5× Opus 5.5. Treat any Fable upgrade as a model-slot change: re-run the determinism and science-accuracy QA, re-measure tokens per round, and update caps before switching (report §1.5).
- **Release-date and limit claims** must be verified with Anthropic (#59, #58).
- **Plugins with another model** are untested (#62): re-run the pilot scenes before switching.

---

## 13. Edge cases owned here

| # | Edge case | Section |
|---|---|---|
| #1 | Silent medium effort | §0, §4 |
| #2 | Requested level unsupported | §4 step 4 |
| #3 | Ultracode runaway | §5 |
| #4 | Ultracode set as default | §5 step 2; §4 step 6 |
| #5 | Thinking cost | §6 |
| #6 | Alias drift | §4 step 3 |
| #9 | Context contamination | §8.1 rule 4 |
| #41–#45 | Credits, caps, late results, throttling, plan exhaustion | §10, §11.4 (detail in `12_advanced_animations_with_claude/03_skills/examleaf-mcp-orchestrator/`) |
| #57 | Fable 5.5 assumptions | §12 |
| #58 | Context/output limits change | §8.1 rule 5 |
| #59 | Release-date claims | §12 |
| #60 | "Don't stop until perfect" | §7 |
| #61 | Haiku long prompts | §3 |
| #62 | Plugin with another model | §12 |
| NEW-26 | Sub-agent logs missing token counts | §8.2 |
| NEW-32 | Mid-session model/effort change breaks cache | §8.1 rule 3 |

---

## 14. Open questions (verify)

1. Claude Code flags and settings that accept each effort level and the model ID on the installed version.
2. How to read token usage, cache reads and writes from Claude Code sessions (including sub-agents) for the ledger.
3. How subscription usage windows relate to tokens; whether ExamLeaf should run animation authoring on a subscription or on API billing.
4. Live prices for the pinned models and cache multipliers (re-check [CAPI] against the pricing page).
5. Pilot measurements: tokens per round by task type and effort; rounds per accepted scene; reviewer minutes per animated scene.
