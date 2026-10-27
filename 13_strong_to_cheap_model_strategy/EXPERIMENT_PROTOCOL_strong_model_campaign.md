# Experiment protocol: strong-model campaign and cheap-model ablation for ExamLeaf

**Version:** 1.0 (2026-10-15). **Owner:** founder-engineer. **Reviewers:** the academic team.

This is the runbook that implements §3 of the strategy. Script names under `experiments/` are **to be built in week 1**. Nothing here has been run yet.

**Audit corrections (15 Oct 2026)** against `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`:
- precondition 9 (effort governance) is new
- arm S5 is an attended, founder-approved exception
- per-surface effort defaults are fixed
- integration-run Reels get GA/H-SB/A-suite/GS
- the rater table uses 10 shadow pairs

See strategy D-9, D-11, D-16 and D-17.

**Labels:** [Recommendation] marks a judgement call. [Hypothesis] marks something not yet measured.

---

## 0. Preconditions (week 1, day 1–3). Do not start any paid run until all of these pass.

1. **Toolchain.** Install Node 22 and FFmpeg.
   - Run `12_advanced_animations_with_claude/04_harness_contract/preflight.sh` and save its output to `experiments/preflight_<date>.log`.
2. **Render proof.**
   - Render `scene_template.html` on HyperFrames at 1080×1920.
   - Run `determinism_hash_check.py` on two renders. The two must match.
   - Record the render worker-seconds per output-second.
3. **Ledger.** Create `experiments/ledger/` with the JSONL schema in §4.1.
   - `experiments/cost.py` computes dollars only from the four billed usage fields and the price table in strategy §7.1.
   - It must reproduce strategy §7.3 per-call costs exactly in a self-test.
4. **Controller skeleton** (`experiments/controller.py`). It must:
   - assemble the BP1–BP3 cached prefix plus the tail;
   - hard-fail any Haiku prompt above 60K tokens (the C1-full arm is the one exception);
   - keep every conversation append-only;
   - set effort only through `output_config.effort`;
   - refuse to send a forced `tool_choice` to Opus, Sonnet or Fable;
   - route Haiku refusals straight to tier 2.

   Unit-test each rule.
5. **Token factor.** Run `messages.count_tokens` for `claude-haiku-5-5` and `claude-opus-5-5` on the same 12 prompts: 3 each in English, Hinglish, Hindi and an Assamese caption set.
   - Store the per-language ratio in `model_profiles/`.
   - Apply the factor to both models in all cost work. Do not apply a Haiku-only multiplier.
6. **Haiku request-shape A/B.** On 6 dev scenes × 5 samples, compare:
   - (a) forced tool with no thinking block, against
   - (b) `tool_choice: auto` + one strict tool + adaptive thinking, against
   - (c) `output_config.format` + adaptive thinking with no tools.

   Log `has_thinking_block`, V0 pass rate and F-LEAK / F-TOOLSKIP. Pick the winner for C3.
7. **Haiku vision check.** Send one 6-frame contact sheet to Haiku. Confirm it answers the binary rubric questions coherently. If it does not, V6 runs on Sonnet.
8. **Scene packages frozen** (§1). The academic team approves the script excerpts, fixtures, rubric and thresholds (strategy §6.5). Record the approval in `experiments/APPROVALS.md` with names and dates.
9. **Effort governance (added 15 Oct 2026; strategy D-16).** Section 12's AD-02, AD-11 and AD-24 govern the strong-model arms and the Kit build.
   - Kit slot-fill runs (P, C3–C5, I) need a `kit_cascade` task family in `12_advanced_animations_with_claude/03_skills/examleaf-effort-governor/scripts/effort_policy.py`, carrying the strategy §5.8 caps. That code change is owned by section 12.
   - Do not start those arms until the family exists and its selftest passes.
   - Ultracode stays refused there; S5 runs outside the governor (§2.2).

---

## 1. Scene set (54 packages + integration set)

### 1.1 Archetypes and families

| # | Archetype | Family |
|---|---|---|
| 1 | Hook / title card | Text-card |
| 2 | Definition / key-term card | Text-card |
| 8 | Recap / quiz pause-and-reveal | Text-card |
| 4 | Formula derivation step-reveal | Symbolic |
| 5 | Worked numerical | Symbolic |
| 7 | Chemical equation balancing | Symbolic |
| 3 | Labelled-fixture reveal (heart, eye, ray diagram, circuit) | Fixture-visual |
| 6 | Graph or plot build from fixture data | Fixture-visual |

### 1.2 Per archetype

- **Dev set: 3 scenes.** These are IDs `DEV-<arch>-<n>`.
- **Sealed holdout: 3 scenes.** These are IDs `HO-<arch>-<n>`.
  - Store them encrypted, or in a folder only the run wrapper reads.
  - Kit authors (human or model) never see them.
- **Spread rules across the full set.** Each subject (Physics, Chemistry, Biology, Maths) appears at least 10 times. Each of the 5 style guides appears at least 8 times. On-screen text is in English, Hinglish and Hindi, with each language at least 12 times.

### 1.3 Adversarial set: 6 scenes (`ADV-1..6`)

1. An Assamese or Devanagari conjunct-heavy title.
2. A long chemical equation that overflows the safe zone.
3. A brief with no validated fixture. The correct outcome is an escalation.
4. More than 3 cues per second.
5. A 60 s Reel compression of a 4-step process.
6. A chemistry or biology brief likely to trigger a false-positive refusal.

### 1.4 Package contents

Each package lives in `experiments/scenes/<id>/`. It contains:

- `brief.md`, written from `06_prompts_and_templates/brief_template.md`
- `script_excerpt.txt`, academic-approved, with its sha256
- `narration.wav`
- `word_timings.json`
- `cue_sheet.json`, which must pass `validate_cue_sheet.py`
- `fixtures.json` (fixture IDs only)
- `language`, `style`, `subject`
- `difficulty` (1–3; the "8 hardest" set is the 8 dev scenes with difficulty 3)

### 1.5 Integration set

- The Ohm's-law 600 s blueprint.
- The 3 pilot lessons from `07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md`. Together with the Ohm's-law lesson, this makes 4 lessons.
- 6 Reels from `01_business_model/REEL_BACKLOG_36.md`.

### 1.6 Setup effort [Hypothesis]

- Academic approval: about 10 minutes per package, so about 9 hours.
- Engineering: about 0.5 hours per package (TTS, alignment, cue sheet), so about 27 hours.
- TTS cost is about $0.03 per 20 s scene.

---

## 2. Run matrix, settings and budget

### 2.1 Common settings

- **Pinned model IDs:** `claude-fable-5-1`, `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`.
- **Effort:** always set `output_config.effort` explicitly. Sonnet 5.5 defaults to `high` on the Messages API and to medium in Claude Code, and Opus 5.5 and Haiku 5.5 default to medium on both (strategy D-17; corrected 15 Oct 2026). Log the requested and effective levels.
- **Thinking:**
  - Adaptive on Haiku.
  - Omit the parameter on Opus 5.5 and Fable 5.1. Thinking is always on for those models, and an explicit "disabled" setting returns a 400.
  - On Sonnet, use adaptive.
- **Seeds:** the run's sample index sets `variation_seed`. Agentic arms get the same brief text for every sample.
- **Caps:** enforced by the wrapper from billed usage. A run that hits its cap is killed and logged with `final_status=capped`. S5 is the exception: its hard stop is a provider-side spend limit, and the wrapper meter is a second line only (12 AD-20: prompt-level budgets are not hard limits).

### 2.2 Agentic arms (S0–S5, C0–C2)

**Harness.** These run through the Claude Agent SDK with file and bash tools, inside a sandbox containing the harness contract, `scene_template.html` and the linter.

**Wrapper.** `experiments/run_agentic.py --arm <ARM> --scene <ID> --model <MODEL> --effort <E> --cap-usd <X> --docs <bare|trim|full|pack>`. It must:

- record one ledger row per model turn;
- record per-turn prompt tokens;
- for Haiku arms, warn at 60K prompt tokens, compact or stop at 80K, and hard-stop at 100K. C1-full is the exception: it may exceed 100K, and every such turn is priced at $0.50/$2.50 and tagged F-TIER100K;
- set an advisory task budget where supported;
- at the end, run V0–V5 itself. The model's own verdict is ignored.

| Arm | Model / effort | Docs | Scenes × samples | Cap per scene | Budget [Hypothesis] |
|---|---|---|---|---|---|
| S0 | Opus 5.5 low | Contract + style guide | Dev 24 × 1 | $2 | ~$18 (24 × $0.40–0.76) |
| S1 | Opus 5.5 medium | Same | Dev 24 × 1 | $4 | ~$48 |
| S2 | Opus 5.5 high | Same | Dev 24 × 1 | $8 | ~$120 |
| S3 | Fable 5.1 high | Same | 8 hardest × 1 | $15 | ~$100 |
| S4 | Opus 5.5 max | Same | 8 hardest × 1 | $15 | ~$99 (8 × $3.16–12.4) |
| S5 | Opus 5.5 max + ultracode ("Ultra" probe). **Attended, founder-approved exception (strategy D-9):** written founder approval of this run in `experiments/APPROVALS.md`; a human present throughout; an isolated experiment sandbox outside the production governor; a dedicated key with a $50 provider-side spend limit. No result can enable ultracode in production (corrected 15 Oct 2026) | Same | 1 hardest × 1 | $50 total (provider-side) | ≤ $50 |
| C0 | Haiku 5.5 medium | Bare | Dev 24 × 3 | $0.50 | ~$2 |
| C1-trim | Haiku 5.5 medium | Trimmed section-12 digest, under 60K | Dev 24 × 3 | $0.50 | ~$2 |
| C1-full | Haiku 5.5 medium | Full section-12 documentation set | Dev 24 × 3 | $2 | ~$16 |
| C2 | Haiku 5.5 medium | Scene pack (skeleton, rules, 2 golden + 1 negative card) | Dev 24 × 3 | $0.50 | ~$2 |

S-arm prompts end with this instruction: "Before finishing, output a DECISIONS block listing 3–7 choices a less capable model could get wrong, each with the rule it implies."

### 2.3 Kit arms (single call + controller)

**Command.** `experiments/run_kit.py --arm <ARM> --set <dev|holdout|adv> --model <M> --effort <E> --k <1|3> --samples <n>`

**Haiku request (tier 1), default shape (c).** Use shape (c) unless the A/B in §0.6 chose otherwise.

```python
client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": EFFORT,
                   "format": {"type": "json_schema", "schema": ARCHETYPE_SCHEMA}},
    system=[BP1_block, BP2_block, BP3_block_with_cache_control],   # stable, byte-identical
    messages=[{"role": "user", "content": TAIL}],                  # repairs are APPENDED as new turns
)
```

**Repair turn.** Append a new user message containing:

- the failing rule IDs;
- each rule's exact message (field path, expected, got, one fix);
- each rule's 2-line negative example.

Never edit earlier turns. Replaying thinking blocks after an edit returns 400.

**Per-message effort rung (tier 1b).** Append the system message `{"role": "system", "content": [], "output_config": {"effort": "xhigh"}}` with beta `mid-conversation-output-config-2026-07-01`. This raises effort without breaking the cache. Verify the exact shape against the current docs during week 1.

**Tier 2: Sonnet 5.5.** Same shape, with `output_config.effort="medium"` set explicitly. Server-side `fallbacks` may be enabled on real-time calls only, because batch calls reject them.

**Tier 3: Opus 5.5.** Same shape, at effort `medium`, raised to `high` on the second attempt. Never send a forced `tool_choice`.

| Arm | Model / effort | Set × samples | Notes | Budget |
|---|---|---|---|---|
| P-low | Opus 5.5 low | Dev 24 × 1 | Fair baseline ("capable model at lower effort") | ~$2 |
| P-med | Opus 5.5 medium | Dev 24 × 1 | Parity reference on dev | ~$3 |
| C3 | Haiku 5.5 at low, medium, high and xhigh; k = 1 and 3 | Dev 24 × 5 per effort | Picks the production effort by cost per accepted scene | ~$10 |
| C4 | Haiku 5.5 at the chosen effort, full cascade | Holdout 24 × 5 + Adv 6 × 5 | Go/no-go evidence. An Opus-Kit reference (medium) is also run on holdout 24 × 1 | ~$6 |
| C5 | Sonnet 5.5 medium | Dev 24 × 3 | Calibrates tier 2 | ~$5 |
| O1 | Hosted Chinese API model (one, from strategy §8.2) | Dev 24 × 3 | JSON mode or tool schema; data review first | ≤ $25 cap |
| O2 | Self-hosted open-weights model | Dev 24 × 3 | Grammar-constrained decoding; log GPU-seconds | ≤ $25 compute |

Haiku arms (C0–C4) together with mining iterations total about $40.

### 2.4 Text arms and integration

| Arm | Task | Arms compared | Items |
|---|---|---|---|
| T0 | Super Teacher section script (English) | Today's mix (Sonnet author + Opus review) / Haiku author + Sonnet review / Haiku alone | 6 sections × 3 |
| T1 | Same task in Hinglish and Hindi; Assamese captions | Same 3 arms; captions use 2 arms | 6 + 6 sections × 3; 4 caption sets × 2 |
| T2 | Beat segmentation + archetype routing (strict enum, includes `UNKNOWN`) | Haiku low / Sonnet medium | 3 lesson scripts against academic gold labels |
| T3 | Reel hooks and captions | 3 arms as T0 | 12 × 3 |
| T4 | Caption fit per script | Code check on T1 outputs | All |

Text-arm LLM budget is about $15, including C5.

**Integration (I).** 4 lessons + 6 Reels × 2 runs through the cascade with every human gate. The Opus-Kit shadow runs on run 1 only.
- Gate order (strategy §5.5): GA → H-SB → TTS → cascade → A-suite → GF.
- Each Reel gets GA for any new wording, its own H-SB, the full A-suite and GS on its own hash. There is no inherited approval (strategy §5.7; corrected 15 Oct 2026).

- Cascade cost: 2 × (4 × $1.08 + 6 × $0.175) = **$10.74**.
- Shadow cost: 4 × $5.62 + 6 × $1.04 = **$28.72**.
- Pilot LLM total: **$39.46**, against a **cap of $45**.

### 2.5 Kit build (B)

| Item | Budget |
|---|---|
| Fable design sessions: 6 × ~$10 | $60 |
| Opus high template builds: 8 × $10 cap | $80 |
| Validators and error catalogue | $40 |
| Re-express the 24 dev gold scenes as specs | ~$7 |
| Weekly mining: 4 × $8 | $32 |
| **Total** | **≈ $220** |

### 2.6 Budget roll-up

| Line | Amount |
|---|---|
| S arms | $435 |
| Build | $220 |
| Kit arms P + C5 + text | $20 |
| Haiku arms | $40 |
| Judge calibration | $5 |
| Pilot | $40 |
| Open-model caps | $50 |
| **Total** | **≈ $810** |
| **LLM cap** (includes contingency) | **$1,000** |

Stop the campaign and review if spend passes $800 before week 5.

---

## 3. Week-by-week execution

| Week | Runs | Human work |
|---|---|---|
| 1 | §0 preconditions; S0 on 6 scenes; P-low on 6 scenes; C0 on 6 scenes; A/B in §0.6 | Approve packages, rubric and thresholds; rater training (1 h, using 5 calibration scenes) |
| 2 | S0 (rest), S1, S2, S3, S4, S5; T0–T3 | Blind rating of S arms and T arms |
| 3 | B; compiled-gold re-render; V6 calibration | Rate compiled golds; label judge-calibration items |
| 4 | C1-trim, C1-full, C2, C3, C5, P-med; mining ×2 | Rate C sample (12 per arm), C3-medium dev, C5 sample |
| 5 | C4 holdout + adversarial + Opus-Kit holdout reference; I run 1 | Rate C4 and the reference, plus pairwise; full gate reviews (timed) |
| 6 | I run 2; O1, O2 | Gate reviews (timed); rate open-model samples; go/no-go meeting |

---

## 4. Capture templates

### 4.1 Ledger row: one per model call (`experiments/ledger/<date>.jsonl`)

```json
{"ts":"2026-10-20T10:31:05Z","run_id":"C3-DEV-5-2-med-s3","arm":"C3","phase":"kit",
 "scene_id":"DEV-5-2","archetype":"worked_numerical","family":"symbolic","set":"dev",
 "model":"claude-haiku-5-5","effort":"medium","thinking":"adaptive","has_thinking_block":true,
 "request_shape":"format+adaptive","kit_version":"0.3.1","kit_sha":"a1b2c3d","prefix_sha256":"…",
 "exemplar_ids":["G-5-01","G-5-02","N-V4-OVERFLOW-03"],"sample_idx":3,"attempt_no":2,
 "repair_turn_no":1,"best_of_n_index":null,"tier":"1",
 "usage":{"input_tokens":3120,"cache_read_input_tokens":14980,"cache_creation_input_tokens":0,"output_tokens":2875},
 "prompt_tokens_total":18100,"price_tier":"<=100K","usd":0.00195,"wall_s":6.2,"ttft_s":0.9,
 "stop_reason":"end_turn","refusal_category":null,
 "verifier":{"V0":"pass","V1":"pass","V2":"pass","V3":"pass","V4":"fail:V4-OVERFLOW@params.steps[2].label","V5":"pass"},
 "failure_tags":["F-OVERFLOW"],"escalated_from":null,"notes":""}
```

### 4.2 Work-unit row: one per scene per sample (`experiments/units/<date>.jsonl`)

Fields:

- `unit_id`, `scene_id`, `arm`, `sample_idx`
- `calls[]`: the `run_id`s of every call in the unit
- `total_usd`, `total_wall_s`, `render_worker_s`
- `final_status`: one of `pass`, `escalated`, `abandoned`, `capped`
- `final_tier`
- `verifier_exit_code`
- `spec_sha`, `code_sha`, `render_hash_a`, `render_hash_b`, `hash_match`
- `keyframes[]`, `contact_sheet`
- `judge`: score per question, plus `judge_model`
- `human`: per rater, each item from the strategy §6.1 rubric, plus `defects[]` and `minutes`
- `escape`: true if a human found a defect that passed V0–V7
- `decisions_block` (S arms only)

### 4.3 Lesson row (integration)

Fields:

- `lesson_id`, `run_no`, `kit_version`
- `scenes`, `scenes_escalated_by_tier`
- LLM spend split into `llm_usd_text`, `llm_usd_scenes`, `llm_usd_escalation`, `llm_usd_judge`
- `render_worker_min`
- `gate1_minutes`, `gate2_minutes`, `defects_found[]`, `seeded_defect_caught`
- `accepted` (both gates passed)
- `cost_per_accepted_lesson`

### 4.4 Decision record (ADR stub)

Fields:

- `ADR-###`
- title
- decision
- evidence (run IDs, n, effect size with interval)
- alternatives rejected
- promoted to (template / schema / validator / exemplar / prose)
- revisit trigger

---

## 5. Blind review procedure

1. **Anonymise.** `experiments/anonymise.py` copies renders to `review/<random_id>.mp4` and writes the key to a file raters cannot open. The process strips model names, arm and file metadata.
2. **Order.** Items are shown in a random order per rater. Each rater sees an item at most once per arm family.
3. **Who rates.**
   - Two raters per item.
   - The science item is rated by an academic reviewer.
   - Legibility and motion are rated on a phone at native 9:16 size.
4. **Pairwise judgement.** Raters see the same scene from two arms side by side, with left/right randomised, and choose one of: A better / tie / B better. They judge correctness and sync, and separately, appeal.
5. **Adjudication.** A third rater adjudicates any item where the two raters differ by 2 or more points on any item, or disagree on science.
6. **Rated item list (scene items).** These counts make the hour estimate auditable.

   | Item group | Items |
   |---|---|
   | S0 / S1 / S2 | 24 + 24 + 24 |
   | S3, S4 | 8 + 8 |
   | S5 | 1 |
   | Compiled gold | 24 |
   | P-low, P-med | 24 + 24 |
   | C0, C1-trim, C1-full, C2 (12 dev scenes each, 1 sample) | 48 |
   | C3-medium dev | 24 |
   | C4 holdout (Haiku) + Opus-Kit reference | 24 + 24 |
   | C5 | 8 |
   | O1, O2 | 8 + 8 |
   | Adversarial (Haiku and reference) | 12 |
   | **Total** | **317** |

7. **Rater hours.**

   | Activity | Arithmetic | Hours |
   |---|---|---|
   | Scene ratings | 317 × 2 raters × 2 min | 21.1 |
   | Pairwise | 48 pairs (24 dev C3 vs P-med + 24 holdout) × 2 × 1.5 min | 2.4 |
   | Adjudication | ~15% of items × 3 min | 2.4 |
   | Text items | 62 sections and caption sets × 2 × 5 min = 10.3; 36 hooks × 2 × 1 min = 1.2; T2 gold labels = 1.5 | 13.0 |
   | Pilot gate reviews (timed) | 8 lessons × 85 min + 12 Reels × 10 min (GS) + 10 shadow pairs × 2 × 1.5 min (corrected 15 Oct 2026: §2.4 produces 10 shadow outputs, not 20) | 13.8 |
   | Training | | 1.0 |
   | **Total** | | **≈ 54** (53.7) |

   At $18.82/h this is ≈ $1,011. The strategy §7.11 keeps the rounded $1,016. With review at $0 (strategy §7.13), these are capacity hours, not cash. If that is too much, the first cuts are C1-trim and C2 ratings (rely on verifier metrics instead) and S0 ratings (6 scenes instead of 24). Together those save about 6.5 h.

---

## 6. Trace-mining procedure (every Friday, about 2 h, capped at $40 per week while stabilising and $10 per week after)

1. **Pull failures.** `experiments/mine.py --since <last_friday>` lists failures by `failure_tag × rule_id × archetype × model × effort`, with counts and example `unit_id`s. It also lists escapes and escalations.
2. **Select.** Take the top 5 clusters by (frequency × severity), plus every escape.
3. **Diagnose.** Give an Opus 5.5 high session, capped at $8, the failing spec, the verifier messages and the golden card. Ask:

   > "Which template default, schema constraint or validator rule would have made this failure impossible or caught it with an actionable message? Propose the smallest change. Do not propose longer prompts."

4. **Apply the closure rule** (strategy §1.4) and pick the lowest rung that works. Then:
   - write the change;
   - write a negative card from the *real* failing output;
   - add or extend a regression test in the negative suite.
5. **Validate.** Re-run, in order:
   - the dev suite on the affected archetype (C3 config, 3 samples);
   - the 31 negative tests;
   - the full dev suite if a shared component changed.

   **Holdout is not run here**, except at version gates.
6. **Record.**
   - A learnings-ledger entry and an ADR, citing run IDs.
   - Update `EDGE_CASE_CLOSURE_MATRIX.csv`.
   - Bump `kit_version`.
7. **Rule hygiene.** Delete any rule that has no detector and no human gate. If the skill has grown past 500 lines, split it.

---

## 7. Analysis and exit criteria

### 7.1 Ablation table (week 4)

For C0, C1-trim, C1-full, C2, C3 and P-low, report:

- V0–V5 pass@1 and pass-within-caps;
- the failure-tag distribution;
- mean rubric (rated subset);
- cost per accepted scene.

**Interpretation rule [Recommendation]:**

| Result | Meaning |
|---|---|
| C1-full ≈ C3 on pass rate and rubric | The "big manual" hypothesis holds. Simplify the Kit. |
| C1 ≈ C0 | Docs alone add cost without quality. |
| C3 ≫ C2 | Templates are doing the work. |

### 7.2 Effort selection (week 4)

For each Haiku effort level, compute cost per accepted scene, including its expected escalations at measured rates.

- Choose the cheapest effort whose dev pass-within-caps Wilson lower bound is at least 0.85 at the scene level.
- Record a separate result per family where they differ.

### 7.3 Go/no-go (week 5–6), per family

Apply the thresholds from strategy §6.5 to C4.

**Statistics.**

- **Unit of analysis = scene.** Wilson 95% interval, with the lower bound used for each decision.
- **Sample-level threshold:** at least 115/120 passes, giving a lower bound of 0.906.
- **Scene-level threshold:** at least 22/24 scenes passing in 4 or more of their 5 samples.
- **Rubric:** the paired difference against the Opus-Kit reference must have a lower 95% bootstrap bound of at least −0.3.
- **Science escapes:** zero.

**Outcomes per family:**

| Outcome | Condition | What happens |
|---|---|---|
| Go-Haiku | All thresholds met | Provisional. Confirmed in production at n ≥ 40 scenes per archetype with a running lower bound ≥ 0.87. Opus shadow stays at 20% until confirmed. |
| Go-Opus-low | Haiku misses, P-low passes | This family runs on Opus 5.5 low through the Kit. |
| No-go | Neither passes | This family stays on the bespoke-plus-human path. Fix the Kit, then re-test. |

### 7.4 Campaign exit (end of week 6)

The campaign is finished when all of the following hold:

- The capability ledger has a row for every task × family, with evidence.
- Measured cost per accepted lesson and per Reel replaces the strategy §7.2 hypotheses.
- Review minutes are measured for both pilot runs.
- The Ultra probe result is logged. It cannot enable ultracode in production (strategy D-9).
- The open-model arms are logged (not necessarily passed).
- `08_cost_models` is updated with the measured figures.
- A go/no-go ADR is signed by the founder and an academic lead.

### 7.5 Stop rules

Stop the campaign and reconvene if any of these happens:

- Spend passes $800 before week 5.
- No scene renders deterministically by day 5.
- A science-value escape occurs in any Kit arm.
- Rater agreement on the science gate falls below 90% (in that case, retrain raters and re-rate).
