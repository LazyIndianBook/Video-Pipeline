# Architect plan 2 — lens: verifier-and-cascade-first

> **Historical input (note added 15 Oct 2026).** This is one of the four architect plans that fed the strategy. Where it conflicts with `../STRATEGY_strong_to_cheap_models.md`, the strategy wins. That includes the audit corrections of 15 Oct 2026 (`../../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` M3, M4, M12): Reels never inherit approval (strategy §5.7); the gate order is GA → H-SB → TTS → cascade → A-suite → GF, with GS for every Reel (§5.5); and V5 uses the contract timing rule, not ±150 ms (§2.4).

**Lens statement (as written by the architect):** verifier-and-cascade-first

**Thesis:** Yes, run the strong-model experiments first. But the useful output of that phase is not a pile of prose guides. It is a set of executable checks: verifiers, templates, a failure catalogue in which every entry maps to an automated detector, and calibrated judges. Haiku 5.5 and open models will still fail often. The system stays good by catching those failures cheaply in deterministic code and sending only the failures up a Haiku -> Sonnet -> Opus cascade. Documentation raises the cheap model's first-pass rate; the verifiers are what make failure safe. Honest scale of the saving: about 40-700x against strong models writing bespoke scenes (the [V1] style), but only about 5-10x against Opus driving the same templated system, and the LLM line is about 5% of total per-video cost.

**Cost claim:** 10-minute lesson, LLM line only, using list prices and project-derived token assumptions:
- Opus-bespoke ([V1] extrapolated x7.59): about $23 at low effort, $372 at max.
- Opus-templated (200K/38K text + 300K/60K scene code, x1.3): $5.15.
- Haiku-only (x1.3 tokenizer, 3 attempts): $0.39, with no quality protection.
- Cascade Haiku -> Sonnet -> Opus with judges: $0.99 central (15%/3% escalation), $0.53 optimistic (5%/1%); about half that with the Batch API.

30 s Reel: Opus-templated $0.91, cascade about $0.18, Opus-bespoke $1.14-$18.6.

The 40-100x applies only against strong models doing bespoke generation. Against Opus on the same templated system it is about 5-10x per completed task, after tokenizer inflation, retries and escalation. The LLM line is about $1.72 of a roughly $34 per-video cost, so total cost falls only 2-3%. Rendering, narration and the $26.67 of human review do not change, unless the verifier QA report also cuts review time (85 to 45 minutes would save about $12.55, a 37% total reduction; this is a hypothesis). The $1,000 experiment programme pays back after about 240 lessons against Opus-templated.

**Biggest risk:** The biggest risk is that verifiers and the cheap VLM judge become the definition of quality (Goodhart). Scenes would pass schema, lint, fixture, hash, layout and timing checks yet teach poorly or look generic. Meanwhile escalation creep (above about 15% of work going to Sonnet or Opus) would erase most of the cost advantage. Both have to be measured directly: the escape rate of human-found defects that passed all verifiers, blind non-inferiority scoring against Opus outputs on a holdout set, and tracked escalation rate. All of this depends on fixing the week-1 blocker first: no FFmpeg or Node 22 on this Mac and no real renders yet.

---

# Verifier-and-Cascade-First: making Haiku-class models produce Opus-class ExamLeaf videos

## 1. Thesis

Your instinct is right: build with strong models first and turn what they learn into material that cheap models can use. That is exactly what the skill-authoring guidance describes. Capture the successful approaches and common mistakes into reusable context and code [N30]. Write evaluations before writing extensive documentation [N60]. Test every skill on every model it will run on, because Haiku needs more guidance than Opus [N58].

From this lens, documentation alone will not stop Haiku from producing poor videos. The evidence that cheap models fail in particular, repeatable ways is strong:

- a wide agentic gap: Terminal-Bench 39.2% vs 70.6% for Sonnet [N4]
- stopping early at low effort [N9, N95]
- reporting work as done without running a check [N10]
- skipping a needed tool call when JSON output is requested with thinking off [N13]
- reasoning text leaking into user-facing output [N15]
- refusals with no server-side fallback [N16]

A better guide only lowers how often these happen. What makes cheap models safe is a system where:

1. **Deterministic code does everything it can.** That covers templates, fixtures, timing and rendering.
2. **Every model output passes through machine verifiers before anyone sees it.** The model's own claim of "done" is never trusted.
3. **Only failures go up the cascade**, with a failure dossier attached: Haiku -> Sonnet -> Opus -> human ticket.
4. **Best-of-N sampling is used only where a real verifier exists.** Repeated sampling scales coverage log-linearly [N88-N91] but plateaus without automatic verifiers [N92].

The repeated-sampling result is the core argument. DeepSeek-Coder-V2 went from 15.9% to 56% on SWE-bench Lite with 250 samples, beating the 43% single-sample state of the art [N88, N89]. That works only because unit tests verify the samples. ExamLeaf already has the equivalent of unit tests for video: the seek-deterministic harness contract, a linter, a double-render frame-hash check, 31 negative tests and 65 edge cases. The plan is to finish that verifier stack, calibrate it on strong-model outputs, and let cheap models search against it.

[Recommendation] Follow Anthropic's own guidance and measure Opus 5.5 at **low** effort on the templated system before building the cascade. If Opus-low already costs under about $1 per lesson, the cascade's extra complexity may not pay for itself at your volumes.

## 2. System design: who does what

### 2.1 Three layers

| Layer | Runs when | Does | Never does |
|---|---|---|---|
| **Strong models (Fable 5.1, Opus 5.5 high/max)** | Offline, once per archetype or skill version; at runtime only as tier-3 escalation | Author scene templates, parameter schemas, skills, exemplars, verifier rules, negative tests; label and calibrate the judge; mine failure traces from cheap-model runs | Run per scene in steady state |
| **Cheap models (Haiku 5.5; optionally Qwen, DeepSeek, Kimi, GLM through the same adapter)** | Per lesson and per Reel | Fill cue sheets (JSON) against a fixed schema; choose a template and set its parameters; write short scene-specific glue code inside allowlisted APIs; repair against verifier error messages; judge keyframes on a binary checklist | Invent science values; write a renderer; pick colours or fonts outside the tokens; declare work done |
| **Deterministic code** | Always | Controller state machine, token-budget guard, schema validation, linter, fixture diff, double-render hash, layout QA, audio-cue alignment, render, contact-sheet extraction, cost ledger | Make taste judgements (those go to the VLM judge and then humans) |

### 2.2 The verifier stack (V0-V8), cheapest first

Every rule has an ID, a measured false-positive rate on the golden set, and an error message written for Haiku: file and line, expected, got, and exactly which edit to make. Validator feedback loops greatly improve output quality [N62], and a machine-checkable intermediate file catches errors early [N63].

| ID | Check | Cost | Catches |
|---|---|---|---|
| V0 | JSON-schema validation of the cue sheet and template parameters | ~0 | Malformed output, missing fields, early stops (required completion fields absent) |
| V1 | Harness-contract linter: `DURATION` present, `seek(t)` pure, seeded PRNG only; bans `Date.now`, unseeded `Math.random`, timers, network calls and non-token colours or fonts | ~0 | Nondeterminism, off-brand styling |
| V2 | Fixture diff: every science value (coefficients, resistances, axis ranges, labels) must reference a fixture ID; text pulled from the DOM at sampled `t` is diffed against the fixture and the script | ~0 | Hallucinated science, the most important failure |
| V3 | Double render at K seek points with frame-hash equality | Render seconds | Hidden state, order dependence |
| V4 | Layout QA from DOM bounding boxes at sampled `t`: 9:16 safe area, caption zone free, minimum font size, overflow, overlap, token contrast | ~0 | Clipping and collisions, the commonest vertical-video defects |
| V5 | Timing: cue-sheet events vs narration word timestamps within ±150 ms [Hypothesis threshold]; scene length = audio length | ~0 | Drift between narration and visuals |
| V6 | VLM judge: Haiku vision scores a 6-keyframe contact sheet against a binary rubric (e.g. "Is the highlighted term the one being spoken?", "Is any element unreadable?"). Sonnet audits a random 10% plus every Haiku/verifier disagreement | ~$0.0007 per scene-attempt (Haiku) | Pedagogical and aesthetic problems that code cannot see |
| V7 | Perceptual regression (SSIM) against the archetype exemplar for templated scenes | ~0 | Template drift after skill edits |
| V8 | Human approvals (academic; full video), unchanged, but reviewers receive the QA report and the list of flagged timestamps | Human minutes | Everything else |

[Hypothesis] Haiku 5.5 accepts image input at the resolution needed for V6. Verify this in week 1. If it does not, use Sonnet for V6; per scene it still costs cents.

### 2.3 The cascade controller

The controller is deterministic code, not an agent. For each work unit (one scene, or one script section):

1. **Budget guard.** Count prompt tokens. Refuse to send any Haiku prompt above 100K tokens, because pricing jumps to $0.50/$2.50 above that [N20, N82]. The project's current 120K-input script-authoring call must be split into section-level calls.
2. **Tier 1, Haiku 5.5.** Medium effort with adaptive thinking [N95, N9]; high effort for strict-format steps. Effort stays fixed per tier, because changing effort invalidates the prompt cache [N14]. Run V0-V5.
3. **Repair loop.** Up to 2 repair turns, each feeding back only the failing rule messages.
4. **Best-of-N.** If the unit still fails, draw N=3 fresh samples (in parallel, through the Batch API when offline [N21]). Keep the first that passes V0-V5. Rank survivors with V6.
5. **Tier 2, Sonnet 5.5**, given the failure dossier: rule IDs, the last diff, and the Haiku attempts. Same verifiers.
6. **Tier 3, Opus 5.5** at high effort. Same verifiers.
7. **Human ticket**, logged as a candidate new failure-catalogue entry.

Hard rules:

- A `stop_reason: refusal` on Haiku is never retried on Haiku, because a retry usually refuses again [N16]. Route it straight to tier 2 and log it. Chemistry topics are the likeliest false positives.
- The model's own completion claims are ignored. Only verifier verdicts advance state [N10].
- Do not combine JSON structured output with thinking off on tool-using steps. Use adaptive thinking, or force `tool_choice` [N13].
- Keep strict schemas inside API limits: at most 20 strict tools [N44], 24 optional parameters [N45], 16 `anyOf` parameters [N46], and `minItems` of only 0 or 1 [N48]. Use `output_config.format`, not the deprecated parameter [N49].
- Cache the static prefix (skill body, style tokens, archetype spec, exemplars) with explicit breakpoints (at most 4 [N56]). Order calls so that sibling scenes reuse the cache within its 5-minute lifetime [N50].

## 3. The experiment programme with strong models

The goal is not "make great videos with Opus". It is to produce, under controlled conditions, three things: (a) gold outputs, (b) labelled failures, and (c) the measured cost and quality frontier for every model and effort pair. Everything is logged to one timeline.

### 3.1 Fixed scene set

**Golden 24:** 6 archetypes x 4 instances, chosen across Physics, Chemistry, Maths and Biology and across the 5 style guides.

| Archetype | Example | Primary verifiers |
|---|---|---|
| A1 Hook or title card | "Why does your phone charger get warm?" | V0, V1, V4, V6 |
| A2 Formula derivation, step-reveal | V = IR rearrangements | V2, V5 |
| A3 Graph or plot build | V-I characteristic from fixture data | V2, V4 |
| A4 Diagram from fixture | Series/parallel circuit; ray diagram | V2, V3, V4 |
| A5 Equation balancing or transformation | Balancing a combustion equation | V2, V5 |
| A6 Recap or quiz card | 3-question recall check | V0, V4, V6 |

**Holdout 12:** 2 per archetype, never shown to anyone writing skills. These detect overfitting.

**Integration set:** the Ohm's-law 600 s blueprint lesson already in `02_learning_psychology/` plus 4 Reels from `01_business_model/REEL_BACKLOG_36.md`.

The 31 existing negative tests become the "must-reject" set: every verifier must flag every one of them.

### 3.2 Runs

| Phase | Model x effort | Scope | Repeats | Purpose |
|---|---|---|---|---|
| P0 | Opus 5.5 low, medium | Golden 24, bespoke (no templates) | 1 | Baseline, per Anthropic's "measure capable model at lower effort first" |
| P1 | Opus 5.5 high, max; Fable 5.1 high | 6 scenes (one per archetype), bespoke | 1 | Find the quality ceiling; harvest techniques. Hard cap $60 per scene. No ultracode: in [V1] it used at least 2.5M tokens, cost at least $348 and never finished |
| P2 | Opus 5.5 high | All 6 archetypes | Iterative | Strong model writes the template, parameter schema, SKILL.md and exemplars for each archetype, using P1 outputs as reference |
| P3 | Opus low/medium/high; Fable medium | Golden 24, templated | 3 | Variance and cost on the templated path (this is the fair comparison baseline) |
| P4 | Haiku 5.5 low/medium/high; Sonnet 5.5 medium; one open model | Golden 24 + Holdout 12, templated | Haiku N=10, others 3 | Failure mining: pass@1, pass@3, pass@10, failure codes |
| P5 | Full cascade | Integration set | 2 | End-to-end cost per accepted lesson and Reel; blind human comparison against P3 Opus outputs |

### 3.3 What the timeline captures

One JSONL record per model call and one per work unit (`experiments/timeline.jsonl`):

```
run_id, phase, work_unit_id, archetype, model_id (pinned), effort, thinking_mode,
skill_version, prompt_sha256, cache_read_tokens, cache_write_tokens, input_tokens,
output_tokens, usd_cost, wall_seconds, attempt_no, repair_turn_no, best_of_n_index,
verifier_results{V0..V7: pass/fail + rule_ids}, judge_score, judge_model,
escalated_from, stop_reason, refusal_category, human_score_1to5, human_defects[],
failure_codes[], decision_note, artefact_paths{cue_sheet, code, keyframes, mp4}
```

Rules:

- Two humans score each P1, P3 and P5 output blind, on the same rubric V6 uses. Those labels calibrate the judge.
- Every decision ("chose GSAP-free easing", "dropped 3D tilt from A4") gets a `decision_note` and an ADR entry citing run IDs.
- Every human-found defect that passed V0-V7 counts as an **escape** and must produce either a new rule or a documented acceptance.

### 3.4 Experiment budget [Hypothesis]

| Phase | Arithmetic | Estimate |
|---|---|---|
| P1 | 6 scenes x about $18 (Opus max, from [V1] scaled to about 30 s) + 6 x about $45 (Fable at 2.5x Opus price for similar tokens) | about $380 |
| P3 | 72 runs x about $1.70 for the effort mix + Fable about $55 | about $175 |
| P4 | Haiku and Sonnet runs, under the cheap rates | under $30 |
| P0, P2, P5 | | about $150 |

**Cap: $1,000.** That is about $1 per lesson amortised over 1,000 lessons. It matters, and it is part of the break-even in section 6.

## 4. Turning experiment outputs into artefacts for cheap models

Each artefact type has required sections. Any document whose rules cannot be checked by a verifier gets a matching V-rule, or is labelled "advisory".

1. **`ARCHETYPE_SPEC_<A#>.md`.** Purpose and learning objective; inputs (fixture IDs, cue fields); template file path; parameter schema (strict-API compatible); allowed variations; **forbidden moves**; required verifiers; 2-3 exemplar links; known failures (catalogue IDs); escalation notes.
2. **`skills/<task>/SKILL.md`.** Frontmatter with `name` and `description` [N23], under 500 lines [N59], references one level deep [N65]. Sections, in order:
   1. When to use
   2. The single default path, with one escape hatch [N66]
   3. Numbered steps, where fragile steps are exact script calls [N61, N64]
   4. "Run `qa/verify.sh <scene>` and paste its output; do not claim completion" [N10]
   5. Stop condition
   6. Links to `reference/` files

   The body is sized so that SKILL.md plus spec plus exemplars stays well under 100K tokens.
3. **`FAILURE_CATALOGUE.md`** (extends the 65 edge cases). ID; symptom; **detector** (V-rule ID, or "human-only"); minimal reproduction; root cause; fix pattern written as an instruction to Haiku; affected models and efforts; frequency observed in P4; status.
4. **`VERIFIER_SPEC.md`.** Rule ID; property; threshold; false-positive and false-negative rates on golden plus negative sets; error-message template; owner.
5. **`EXEMPLAR_PACK/<A#>/`.** Brief -> cue sheet -> code -> keyframes -> verifier report -> human score. These are few-shot material and also regression baselines for V7.
6. **`RESTRICTIONS.md`.** API allowlist and denylist, the token-only colour and font list, maximum element counts, banned effects (for example motion blur, which breaks hash determinism [Hypothesis]).
7. **`JUDGE_RUBRIC.md` plus `JUDGE_CALIBRATION.md`.** Binary questions; the prompt; agreement with human labels per question. Drop any question whose agreement is below 80% [Recommendation threshold].
8. **`ESCALATION_POLICY.md`.** Repair-turn and N limits per tier; refusal routing; per-unit cost ceilings; when to page a human.
9. **`LEARNINGS/ADR-###.md`.** Decision, evidence (run IDs), consequence, revisit trigger.
10. **`MODEL_CARD_<model>.md`.** Pinned ID, effort defaults, tokenizer inflation measured on our own prompts (Haiku 5.5 tokenizer adds roughly 30-36% vs Haiku 4.5 [N2, N42]), known quirks, pass rates per archetype.

[Recommendation] Write artefacts 3, 4 and 7 before artefact 2. Evals before documentation [N60].

## 5. Cheap-model operating procedure (per lesson)

1. Deterministic pre-step: load the approved academic script, the fixtures, and the narration word timestamps once TTS is done.
2. Haiku segments the script into scenes and assigns an archetype per scene. V0 checks the schema; a coverage check confirms every learning objective maps to a scene.
3. Each scene is a work unit through the cascade in section 2.3. Sibling scenes are batched to share the cached prefix.
4. Assemble, render, run V3 and V7 at lesson level, then a lesson-level V6 pass on transitions.
5. Generate the QA report for reviewers: failures auto-fixed, escalations, judge low-confidence timestamps.
6. Human gates 1 and 2.
7. Log everything to the timeline. Weekly failure mining (Sonnet reads new escapes and drafts catalogue entries; a human accepts them).

Model updates: when any pinned model ID changes, re-run Golden 24 + Holdout 12 before switching. Treat it as a dependency upgrade.

Open or Chinese models: they go through the same adapter and verifiers. Gate them on four things: data residency, licence, whether caching and batch exist (pricing assumptions differ), and tokenizer inflation measured on our prompts. ManimBench shows sub-30B open models reaching 94% render success with renderer feedback in the loop, after GRPO training [N68, N72]. That supports verifier-in-the-loop, but those models were trained for it. [Hypothesis] Untrained open models will be well below that.

Fine-tuning becomes an option only after about 400 or more accepted traces exist. The BabyAI study used 446 [N78]. Fine-tuning has been reported to cut cost 5-30x [N73, N75] but can regress out of distribution [N77]. Not in the 6-week scope.

## 6. Cost model

### 6.1 Workload assumptions [Hypothesis; replace with P3/P4 meter readings]

- **Text, per lesson.** The project's existing workload: author 120K in / 25K out; review 60K / 10K; routing 20K / 3K. Total 200K in / 38K out.
- **Scene code, per lesson.** 20 scenes x (15K in / 3K out). Total 300K in / 60K out.
- **Reel (30 s).** Text 30K / 5K; 4 scenes = 60K / 12K.
- **Haiku adjustments.** 1.3x tokens for tokenizer inflation [N42].
- **Attempts.** Opus 1.3 (the project's 30% regeneration allowance). Haiku-only 3.0. Haiku inside the cascade 2.2 on average. Sonnet and Opus escalations 1.5.
- Prices are list prices, without batch or caching unless stated.

### 6.2 10-minute lesson

**Opus-only, bespoke (the [V1] style, extrapolated).** 600/79 = 7.59x the 79 s video: low effort 7.59 x $3 ≈ **$23**; max effort 7.59 x $49 ≈ **$372**.

**Opus-only, templated system.**

| Item | Input | Output | Total |
|---|---|---|---|
| Text | 200K x $4/M = $0.80 | 38K x $20/M = $0.76 | $1.56 |
| Scenes | 300K x $4/M = $1.20 | 60K x $20/M = $1.20 | $2.40 |

$3.96 x 1.3 = **$5.15**.

**Haiku-only, templated.** One attempt:

| Item | Input | Output | Total |
|---|---|---|---|
| Text | 260K x $0.10/M = $0.026 | 49.4K x $0.50/M = $0.0247 | $0.051 |
| Scenes | 390K x $0.10/M = $0.039 | 78K x $0.50/M = $0.039 | $0.078 |

$0.129 per attempt x 3 attempts = **$0.39**. This has no escalation, so quality is unprotected.

**Cascade, central case** (15% of work escalates to Sonnet, 3% to Opus):

| Component | Arithmetic | Cost |
|---|---|---|
| Haiku | $0.129 x 2.2 | $0.283 |
| Sonnet | full pass = (200K x $2 + 38K x $10) + (300K x $2 + 60K x $10) = $1.98; x 0.15 x 1.5 | $0.446 |
| Opus | $3.96 x 0.03 x 1.5 | $0.178 |
| Haiku judge | 44 scene-attempts x $0.00067 (5.2K in, 0.3K out) | $0.030 |
| Sonnet audit | 4 scenes x $0.0134 | $0.054 |
| **Total** | | **≈ $0.99** |

**Cascade, optimistic** (5% Sonnet x 1.2, 1% Opus x 1.2): $0.283 + $0.119 + $0.048 + $0.084 = **≈ $0.53**.

**Ratios.** The cascade is 5.2x (central) to 9.7x (optimistic) cheaper than Opus-templated. Against Opus-bespoke it is 23-43x cheaper at low effort and 375-700x at max effort. The Batch API halves both sides of a fair comparison [N21], so it does not change the ratios. It does halve absolute cost, to about $0.27-0.50 per lesson.

### 6.3 30 s Reel

| Scenario | Arithmetic | Cost |
|---|---|---|
| Opus-bespoke | 30/79 x $3 to $49 | $1.14 to $18.6 |
| Opus-templated | (0.12 + 0.10 + 0.24 + 0.24) x 1.3 | $0.91 |
| Haiku-only | 0.0228 per attempt x 3 | $0.068 |
| Cascade | Haiku 0.0228 x 2.2 = $0.050; Sonnet $0.35 x 0.225 = $0.079; Opus $0.70 x 0.045 = $0.032; judges $0.019 | ≈ $0.18 |

Ratios: 5x against Opus-templated; 6-100x against Opus-bespoke (low to max).

### 6.4 What 40-100x actually applies to

- **The 40x and 100x figures are list-price ratios** (Opus and Fable vs Haiku). On a cost-per-completed-task basis they shrink in three steps:
  - tokenizer inflation (1.3x) takes 40x down to about 31x
  - Haiku needing more attempts (3 vs 1.3) takes it to about 13x
  - paying for escalations and judges takes it to about 5-10x
- **The 40-100x saving is real only against strong models doing bespoke generation.** Most of that saving comes from templates and deterministic code, not from swapping the model.
- **The LLM line is small.** In the existing hybrid model of about $34 per lesson, LLM is $1.72, narration $0.96, human review $26.67 and the rest about $4.65.
  - Bringing LLM to $0.53-0.99 moves the total to about $33.0-33.3, a **2-3% reduction**.
  - Rendering, narration and credits do not change.
- **The real lever is human review minutes.** At $26.67 / 85 min = $0.314 per minute, cutting review to 45 minutes would save 40 x $0.314 = $12.55, a 37% total reduction. [Hypothesis] The QA report and flagged timestamps let reviewers check flags instead of watching every frame. The two human gates stay in place either way.
- **Break-even.** Moving from Opus-templated to the central cascade saves $5.15 - $0.99 = $4.16 per lesson, so a $1,000 experiment programme pays back after about 240 lessons.

## 7. Quality gates and evals

Ship criteria per archetype. All values are [Recommendation] thresholds to be confirmed in P3/P4.

| Metric | Target |
|---|---|
| Cascade final pass on Golden + Holdout (V0-V7) | ≥ 98% |
| **Escape rate** (human-found defects per lesson that passed V0-V7) | ≤ 0.5, and no science-value escapes ever (V2 must be total) |
| Blind human score, cascade vs Opus-templated | Non-inferior, mean difference ≥ -0.3 on a 5-point scale, n ≥ 24 scenes |
| Judge agreement with humans, per rubric question | ≥ 80%; questions below are dropped |
| Escalation rate to Sonnet | ≤ 15% (above that, the cascade costs more than Opus-low; re-measure) |
| Negative tests rejected | 31 of 31 |
| Holdout pass within 5 points of Golden pass | Yes; otherwise the skills are overfitted |
| Determinism (V3 double-render hash) | 100% |

## 8. Risks and failure modes

1. **Verifier Goodhart.** Scenes pass every rule yet teach poorly or look dull. *Mitigation:* the escape metric, human blind scoring, V6, and rotating holdouts. Verifiers protect correctness, not inspiration; inspiration lives in the templates the strong models write.
2. **Judge miscalibration.** A cheap VLM rubber-stamps defects. *Mitigation:* Sonnet audit on 10% plus disagreements; per-question agreement tracking; humans remain final.
3. **Escalation creep.** If 30% of work escalates, the cascade costs about $1.6 per lesson and the ratio falls toward 3x. *Mitigation:* mine escalations weekly into skills and templates. If escalation still exceeds 15%, run that archetype on Sonnet or Opus-low directly.
4. **Pricing cliffs.** The 100K-token Haiku tier [N20], cache invalidation when effort changes [N14], and the tokenizer [N42]. *Mitigation:* the controller's token guard and fixed effort per tier.
5. **Refusals** on chemistry or biology content [N16]. *Mitigation:* route to tier 2 without retry; track by category.
6. **Silent early stops and false "done" claims** [N9, N10]. *Mitigation:* V0 required fields; ignore self-reports.
7. **Template sameness.** Viewers notice repetition. *Mitigation:* allowed-variation parameters per archetype; quarterly strong-model refresh of templates.
8. **Model churn.** Pinned IDs retire. *Mitigation:* the golden re-run is a release gate.
9. **Single-run evidence.** [V1] is one prompt and one run; every token figure here is an assumption until P3/P4 meters exist.
10. **Environment.** No FFmpeg and no Node 22 on this Mac, and no real HyperFrames or Remotion renders yet. V3-V7 cannot run until that is fixed. This is the week-1 blocker.
11. **Skill supply chain.** Install third-party skills only after audit [N29].

## 9. Six-week rollout

| Week | Deliverables | Exit check |
|---|---|---|
| 1 | Install Node 22 and FFmpeg; first real HyperFrames render; controller skeleton with token guard; V0, V1, V3 wired from existing linter and hash check; `timeline.jsonl` schema; Golden 24 and Holdout 12 frozen; rubric drafted; confirm Haiku image input | 31 negative tests run through V0-V3; one scene renders deterministically |
| 2 | P0 and P1 runs (capped); P3 started; two-person blind scoring; V2 fixture diff, V4 layout, V5 timing | Every Golden scene has an Opus reference and human labels |
| 3 | P2: 6 archetype templates, specs, skills, exemplars; failure catalogue v1 linked to detectors; V6 judge calibrated; V7 baselines | Judge agreement report; skills under 500 lines with ≥ 3 evals each |
| 4 | P4: Haiku low/medium/high x N=10, Sonnet, one open model; two failure-mining iterations updating skills and verifiers | pass@1 and pass@3 per archetype; escalation-rate estimate |
| 5 | P5: cascade on Ohm's-law lesson + 4 Reels, run twice; blind comparison against Opus-templated; measured cost per accepted lesson; reviewer QA-report trial (timed) | Section 7 metrics computed with real numbers |
| 6 | Go/no-go ADR. Options: cascade, Opus-low-templated, or a per-archetype mix. Harden escalation policy; 10-lesson pilot; update `08_cost_models` with measured tokens and review minutes | A decision backed by measured cost per accepted lesson and escape rate, not list-price ratios |

**Bottom line.** Use the strong models to build the rails: templates, verifiers, a failure catalogue and a calibrated judge. Then let cheap models run on those rails and pay for strong models only when a verifier says the cheap model failed. Expect about 5-10x LLM savings against a fair Opus baseline and 40x or more against bespoke strong-model generation. To move total per-video cost, aim the same verifier stack at the 85 minutes of human review.
