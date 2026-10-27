# Architect plan 4 — lens: economics-and-ops-first

> **Historical input (note added 15 Oct 2026).** This is one of the four architect plans that fed the strategy. Where it conflicts with `../STRATEGY_strong_to_cheap_models.md`, the strategy wins. That includes the audit corrections of 15 Oct 2026 (`../../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` M3, M4, M12): Reels never inherit approval (strategy §5.7); the gate order is GA → H-SB → TTS → cascade → A-suite → GF, with GS for every Reel (§5.5); and V5 uses the contract timing rule, not ±150 ms (§2.4).

**Lens statement (as written by the architect):** economics-and-ops-first

**Thesis:** Yes, run the strong-model experiments first. But the 40-100x saving does not come from swapping Opus for Haiku. It comes from moving the creative and debugging work out of the per-video path and into offline, deterministic artefacts: templates, validators, a cue-sheet schema and an exemplar bank. Once that is done, the cheap model only fills small, validated slots. Compared like for like (same workload, same caching and batch), Haiku 5.5 cuts the LLM bill only about 13x, because of tokenizer inflation, higher effort and more retries. The headline 40x appears only against a naive Opus pipeline, and 70-1,000x only against freeform per-video generation like the V1 experiment. Even a near-zero LLM bill cuts total cost per video by only about 4-5%, because about 78% of the ~$34 variable cost is the 85 minutes of human review. So the plan pairs a cheap-model system with a review-minute reduction programme, keeps academic and final approval human, and treats Chinese/open models and fine-tuning as later options gated by evals, not as the main lever.

**Cost claim:** LLM cost per 10-minute lesson on a templated workload (assumed: 30 scenes, 12K input / 1.5K output per call, 1.3x regeneration):
- Opus-only: $6.59 uncached, $4.43 cached, $2.22 batch.
- Cheap Haiku 5.5 system (with tokenizer x1.36, medium-effort output x2 and 2.5 attempts per scene): $0.46 uncached, $0.34 cached, $0.17 batch.
- Cascade (Haiku generation + Opus pre-review + Sonnet escalation on 15% of scenes): $1.34, or $0.67 batch.
- 30-second Reel: Opus $0.57 cached vs Haiku $0.044.

Like for like, that is about 13x. The 39x figure appears only when a naive Opus pipeline is compared with an optimised Haiku one, and 67-1,094x only against freeform V1-style generation ($22.8-$372 per lesson, extrapolated). Total variable cost per lesson moves only from ~$34 to ~$32.62 (−4%), because human review is $26.67. Cutting review from 85 to 40 minutes brings it to ~$18.50 (about 1.8x cheaper). The experiment programme is capped at $1,500 and pays back after ~370 lessons against Opus-only.

**Biggest risk:** Spending the programme on the LLM line, which is about 4% of per-video cost, while human review (about 78%, 85 minutes) stays the same or grows. If cheap models produce plausible-but-wrong science or layout that the validators miss, every 3-13 extra reviewer minutes wipes out the entire $1-4 per lesson LLM saving. The cost model also rests on unmetered token assumptions until week-1 measurements exist.

---

# Economics-and-ops-first plan: strong models offline, cheap models per video, humans where it matters

## 0. Thesis (short version)

[Recommendation] Run the strong-model programme first, but aim it at producing **code and checkable artefacts, not prose**. Every lesson learned from a Fable 5.1 or Opus 5.5 run should become, in this order of preference:

1. a template parameter or default (costs nothing per video);
2. a deterministic validator check;
3. a machine-enforced restriction;
4. a curated exemplar;
5. only as a last resort, prose guidance.

Prose costs tokens on every call and weak models follow it unreliably. Code costs nothing per run and is always followed. This matches Anthropic's skill guidance: prefer pre-made utility scripts [N64], validator loops [N62] and plan-validate-execute with a machine-checkable intermediate file [N63], and match how much freedom you give to how fragile the step is [N61].

Three honest numbers frame everything below (arithmetic in section 6):

- **Like for like, Haiku 5.5 cuts the LLM line about 13x, not 40x.** The 40x list-price ratio gets eaten by tokenizer inflation [N2, N42], higher output at medium effort [N9] and more retries.
- **Against freeform Opus generation the saving is 67-1,000x.** That is V1-style generation from a bare prompt, extrapolated to 10 minutes. This gap is real, but it comes from the architecture, not the model.
- **Total per-video cost falls only about 4% from the model swap.** Human review is ~$26.67 of ~$34. Halving review minutes is worth more than every model optimisation combined.

## 1. Cost structure today, and what each lever can touch

Per 10-minute lesson, from the project's hybrid model. "Other" is derived by subtraction.

| Line | $/lesson | Share | Which lever reduces it |
|---|---|---|---|
| Human review (85 min) | 26.67 | ~78% | Verifiers, flagged-only review UI, derived Reels |
| Render / storage / QA / other (derived: 34 − 26.67 − 0.96 − 1.72) | ~4.65 | ~14% | Render efficiency (out of scope here) |
| LLM (v2 budget, old price list) | 1.72 | ~5% | Model choice, caching, batch, effort |
| Narration | 0.96 | ~3% | TTS choice (separate pipeline) |

[Recommendation] Judge everything by **cost per accepted lesson**: total spend, including retries, escalations and human minutes, divided by lessons that pass both human approvals. Anthropic's own guidance says to judge cost per completed task, not per request.

Repricing the project's own v2 token budget at current prices:

- Sonnet 5.5 at 120K in / 25K out = 0.24 + 0.25 = $0.49
- Opus 5.5 at 60K / 10K = 0.24 + 0.20 = $0.44
- Haiku 5.5 at 20K / 3K = $0.0035
- Sum = $0.93; × 1.3 regeneration allowance = **$1.21**

Note that this budget **contains no animation scene generation at all**. The advanced-animation layer is a new cost line that must be modelled separately (section 6).

## 2. System design: three layers

### Layer A: Offline, strong models plus humans (run rarely, amortised)
- **Fable 5.1 / Opus 5.5 at high to max effort** author and debug scene **templates** (HyperFrames components that obey the seek-deterministic contract), propose cue-sheet schema changes, write validators, diagnose failure clusters, and turn successful runs into skills [N30].
- **Humans** (academic team) author and validate the science **fixtures**, approve style-guide tokens, score experiment outputs blind, and approve every template before it enters the library.
- The output of Layer A is a versioned **Production Kit**: a template library, cue-sheet JSON schemas per scene type, validators, a SKILL.md set, the exemplar bank, the restriction list and the edge-case register.

### Layer B: Per-video, cheap model (Haiku 5.5 by default)
- Turns the approved academic outline plus the narration script into a **cue sheet**: an ordered list of `{scene_type, template_id, params, fixture_ids, narration_span, duration}`.
- Picks only from template IDs that already exist. It **never writes freeform animation code**. Freeform code is exactly where Haiku's agentic gap shows: Terminal-Bench 39.2% vs 70.6% for Sonnet 5.5 [N4, N37].
- Writes the Reel hook/script text and on-screen captions within length limits.
- Fixes its own output in a validator-driven loop, with an attempt cap.

### Layer C: Deterministic code (zero LLM cost, always right or always loud)
- Schema validation, fixture lookup (science visuals only from validated fixtures), the 9:16 safe-zone and text-overflow checks, matching timing to narration timestamps, the seek-determinism linter, the double-render frame-hash check, contrast and token compliance, rendering, and FFmpeg muxing.
- Runs as bundled scripts whose code never enters the model's context [N27].

### Routing rule (cascade) [Recommendation]
1. Haiku 5.5 at **medium** effort [N95]. For each scene, sample k=3 candidates in parallel and let the deterministic verifier pick. With a real verifier, repeated sampling lets a cheap model beat a stronger single-shot model [N88, N89]. Without one it plateaus [N92].
2. If no candidate passes, retry once with the validator errors fed back, at **high** effort (high is the recommended setting for strict instruction following [N95]).
3. Still failing, or `stop_reason: refusal` [N16], escalate the scene to Sonnet 5.5 high. Log the scene type.
4. If any scene type escalates more than 15% of the time over 20 lessons, that is a **Layer A defect**. Fix the template or schema; do not keep paying per video.

## 3. Experiment programme with strong models

### 3.1 Fixed eval set ("Golden-24") [Recommendation]
24 scenes, frozen before any run, drawn from real Assam Board Class 10-12 content and covering:

- **Scene types:** equation derivation, worked numerical, labelled diagram from a fixture (e.g. heart, eye), ray-optics diagram, circuit, graph plotting, process/cycle (e.g. nitrogen cycle), chemical equation balancing, comparison table, mnemonic/recap card, Reel hook, quiz pause.
- **Style:** all 5 vertical style guides at least 4 times each.
- **Language:** English, Hinglish and Hindi on-screen text (the Devanagari layout edge cases).
- **Stress cases:** at least 8 scenes pulled from the 65 documented edge cases (long labels, dense equations, fast narration spans, scenes over 25 s).
- **Plus:** 2 complete lessons and 4 Reels as end-to-end tests.

Keep a **held-out set of 12 more scenes** that no model or doc author ever sees. This guards against overfitting the docs to Golden-24.

### 3.2 Run matrix (measure the capable model at lower effort first, per Anthropic's guidance)

| Run | Model / effort | Seeds | Purpose |
|---|---|---|---|
| R0 | Haiku 5.5 medium, **bare** (schema only) | 3 | Baseline without docs [N60] |
| R1 | Opus 5.5 medium (its default [N93]) | 2 | Is strong-at-low-effort already good enough? |
| R2 | Opus 5.5 high | 2 | Quality/effort curve |
| R3 | Opus 5.5 max | 1 | Ceiling; template authoring |
| R4 | Fable 5.1 max, **only the 8 hardest scenes** | 1 | Ceiling where Opus max fails |
| R5 | Sonnet 5.5 high | 2 | Candidate escalation tier |
| R6 | Haiku 5.5 medium/high **with the Production Kit** | 3 | The actual target |
| R7 | Haiku R6 config on the **held-out 12** | 3 | Generalisation check |

R1-R4 are run in two modes: (a) **authoring**, where the model writes a template plus params for a scene type, and (b) **filling**, where it fills a cue sheet using existing templates. Only (b) is comparable to per-video cheap-model work.

**Banned:** ultracode. V1 spent at least $348 and at least 2.5M tokens without finishing. Every run gets a hard token cap, and a stuck run ends as a logged failure, never as an extended budget.

### 3.3 Timeline ledger: what to capture on every run (JSONL, one row per model call plus one per run)
- **Identity:** run_id, scene_id, run code (R0-R7), model ID, effort, thinking mode, kit version, prompt-prefix hash.
- **Tokens:** input, output, cache-write, cache-read (from the API usage fields); $ computed from the price table, never estimated.
- **Time:** wall clock, time to first token, render time, number of tool calls.
- **Loop:** number of fix iterations; validator results at each iteration (which check failed); whether the final validator pass was real or merely claimed. Haiku can report done without running a check [N10], so record the validator's own exit code, not the model's statement.
- **Failure category:** mapped to an edge-case ID (or "new"), plus refusals and early stops [N9].
- **Output:** cue-sheet hash, render hash, double-render match (yes/no).
- **Human:** blind rubric score per scene (science accuracy 0/1 as a gate; pedagogy, visual clarity, pacing, style compliance 1-5) and reviewer minutes.
- **Decision record:** a short ADR on what was chosen and why, and what was rejected.

[Hypothesis] V1's implied rate is $3 / 78K ≈ $38 per million "tokens", above Opus's $20 output price. So V1's token counts are probably output or non-cached tokens, with the agent loop re-sending context on each turn. The ledger must record all four usage fields so the cost model rests on billed numbers.

### 3.4 Experiment budget (hypotheses until R1 is metered)
Based on V1's per-second cost ($3/79 s ≈ $0.038 per second at low effort; $49/79 s ≈ $0.62 per second at max) and a ~20 s average scene:

| Run | Arithmetic | Cost |
|---|---|---|
| R1 Opus medium | 24 × 2 × ~$2 | ~$96 |
| R2 Opus high | 24 × 2 × ~$5 | ~$240 |
| R3 Opus max | 24 × ~$12.4 | ~$298 |
| R4 Fable max (2.5x Opus prices) | 8 × ~$31 | ~$248 |
| R5 Sonnet high | 48 × ~$1.25 | ~$60 |
| R0/R6/R7 Haiku, all seeds | | ~$60 |
| Two end-to-end lessons, Opus high | 2 × ~$60 | ~$120 |
| **Total** | | **≈ $1,120** |

**Hard cap $1,500.** Per-run caps: $20 per scene for Opus max, $40 per scene for Fable.

## 4. Turning experiment outputs into artefacts for cheap models

Every artefact is versioned in a `production_kit/` folder and tied to the ledger runs that justify it. Required documents and their sections:

1. **Scene-type playbook** (one per scene type, ~12). Sections: purpose and when to use; the template_id to use (exactly one default, with an escape hatch [N66]); the cue-sheet field table with types and allowed ranges; 2 golden exemplars (input → cue sheet → frame thumbnails); top 5 anti-patterns from the ledger, each with a fix; the validator checks that apply; budget (max_tokens, attempt cap, escalation trigger).
2. **SKILL.md per task** (cue-sheet fill, Reel script, caption fit). YAML frontmatter with name and description [N23]. Body under 500 lines [N59], one level of references [N65], rarely used paths split into their own files [N28]. A mandatory **verification paragraph** to counter false "done" claims [N10]. The current date where relevant [N11]. No blanket "always search" [N12].
3. **Restrictions file**: machine-readable hard rules, each paired with the validator that enforces it. Examples: no Math.random or Date.now (use the seeded PRNG), no CSS animation that cannot be seeked, only fixture IDs from the registry, maximum characters per line per language, safe-zone margins. A rule with no enforcement is marked "advisory" and reviewed for promotion to a check.
4. **Edge-case register** (extend the existing 65). Sections: ID, trigger, symptom, the check that detects it, fix recipe, regression test (point to one of the 31 negative tests, or add one), first-seen run_id.
5. **Exemplar bank**: only outputs that passed **both** the validators and human review, each with a "why this is good" annotation. Exemplars sit in the cacheable prompt prefix.
6. **Verifier suite (code)**: schema, linter, determinism double-render, fixture match, layout/overflow, matching scenes to narration timestamps, contrast, and a narration-text check for leaked reasoning [N15]. Each check returns machine-readable errors that are fed back to the model.
7. **Cost card per task**: model, effort, thinking mode, tool_choice, max_tokens, k samples, attempt cap, escalation rule, and expected $ per call.
8. **Learnings log + ADRs**: dated, linked to run_ids, with a "promoted to" field (template / validator / restriction / exemplar / prose).
9. **Eval spec**: Golden-24 plus held-out-12, the rubric, thresholds (section 7), and how to rerun it.

Distillation rule [Recommendation]: when Opus max solves a scene that Haiku fails, ask the strong model **which template parameter or check would have prevented the failure** [N30]. Do not ask for a longer prompt. Test docs on every model they will run on [N58].

## 5. Cheap-model operating procedure (per lesson)

1. **Inputs are frozen first:** the academic-approved outline (human gate 1), the narration script with timestamps, and the fixture IDs.
2. **Prompt layout, cache-friendly:** tools → system (SKILL core, style tokens, schema) → exemplars → [cache breakpoint] → per-scene variables. At most 4 breakpoints [N56]; 20-block lookback [N55]. Caches are model-scoped, so an escalation to Sonnet pays its own cache write.
3. **Stay under 100K tokens per prompt.** Above that, Haiku prices jump to $0.50/$2.50 [N20, N82]. Treat the 1M window [N6] as a trap for this workload.
4. **Fixed effort per task.** Changing effort mid-conversation invalidates the cache [N14]. Use medium by default and high only for retries.
5. **Structured output:** keep each scene-type schema small. Limits: at most 20 strict tools [N44], 24 optional parameters [N45], 16 anyOf [N46], minItems only 0 or 1 [N48]. Use the `output_config.format` parameter [N49]. Compiled grammars are cached for 24 h [N43], so keep schemas stable. If a tool call is needed alongside JSON, use adaptive thinking or force tool_choice [N13].
6. **Generation round 1 (Batch API, 50% off [N21]):** all scenes, k=3 each. Use the 1-hour cache TTL, because batch timing can outlive 5 minutes. The 1-hour write costs 2x but pays back after two reads [N22, N51].
7. **Verify** in Layer C and pick the best passing candidate per scene.
8. **Round 2 batch:** failures only, with validator errors attached, at high effort.
9. **Escalate** remaining failures and refusals to Sonnet 5.5 (real-time is fine; volume is small).
10. **Render twice** and check frame-hash determinism.
11. **Human gate 2:** a full-video review in a UI that shows the validator report, highlights scenes that were escalated or flagged, and shows the scene-level diff against the approved outline.
12. **Reels are derived** from the approved lesson's cue sheet by a deterministic cut-down. The LLM writes only the hook and caption text. Reels inherit the lesson's scientific approval; one short human check per Reel remains.

**What NOT to automate** [Recommendation]: academic approval (gate 1); final full-video approval (gate 2); fixture authoring and validation; changes to style guides or templates; acceptance of new exemplars; any science-correctness verdict by an LLM judge. An LLM judge may pre-filter pedagogy and pacing; it never signs off science.

## 6. Cost model (explicit arithmetic)

### 6.1 Workload assumptions per 10-minute lesson [Hypothesis, to be replaced by ledger data in week 2]
- **Text work:** the project's v2 budget split into script 120K/25K, review 60K/10K, routing 20K/3K. Total 200K input, 38K output.
- **Scenes:** 30 per lesson. Each call is 12K input (10K stable prefix, 2K variable) and 1.5K output.
- **Attempts per scene:** Opus 1.5; Haiku 2.5 (k-sampling plus retries).
- **Haiku penalties:** all tokens × 1.36 for tokenizer inflation [N2]. This is a conservative stand-in, since N2 measures against Haiku 4.5, not Opus 5.5. Output tokens are a further × 2 for medium effort plus the verification paragraph [N9, N10].
- **Regeneration allowance:** × 1.3 on everything.
- **Prices:** Opus $4/$20 with $0.20 cache read and $5 cache write. Haiku $0.10/$0.50 with $0.01 cache read and $0.125 write. Sonnet $2/$10. Batch halves all of these.

### 6.2 Lesson, Opus-only (templated workload)
- **Text:** 200K × $4/M = $0.80; 38K × $20/M = $0.76. Subtotal **$1.56**.
- **Scenes, uncached:** 45 calls × 12K = 540K × $4/M = $2.16; 45 × 1.5K = 67.5K × $20/M = $1.35. Subtotal **$3.51**.
- **Total uncached:** (1.56 + 3.51) × 1.3 = **$6.59**.
- **With caching on scene prefixes:** 450K reads × $0.20/M = $0.09; 90K × $4/M = $0.36; write 10K × $5/M = $0.05; output $1.35. Scenes = $1.85. Total = (1.56 + 1.85) × 1.3 = **$4.43**. With batch: **$2.22**.

### 6.3 Lesson, cheap-model system (Haiku 5.5 throughout)
- **Text:** 272K × $0.10/M = $0.027; 38K × 1.36 × 2 = 103.4K × $0.50/M = $0.052. Subtotal **$0.079**.
- **Scenes:** 75 calls, each 16.32K input (13.6K cached, 2.72K variable).
  - Reads: 1.02M × $0.01/M = $0.010
  - Variable: 204K × $0.10/M = $0.020
  - Write: $0.002
  - Output: 75 × 1.5K × 2.72 = 306K × $0.50/M = $0.153
  - Subtotal **$0.185**
- **Total cached real-time:** (0.079 + 0.185) × 1.3 = **$0.34**. With batch: **$0.17**. Uncached: **$0.46**.

### 6.4 Lesson, cascade (Haiku generation + Opus pre-review + Sonnet escalation on 15% of scenes)
- **Haiku text without review:** 190K × $0.10/M + 76K × $0.50/M = $0.057.
- **Haiku scenes:** $0.185.
- **Opus pre-review** (60K/10K): $0.44.
- **Sonnet escalation:** 4.5 scenes × 2 calls = 9 calls × 12K = 108K × $2/M = $0.216, plus 13.5K × $10/M = $0.135, so $0.35.
- **Total:** (0.057 + 0.185 + 0.44 + 0.35) × 1.3 = **$1.34**. With batch: **$0.67**.
- The Opus pre-review ($0.44) is worth paying only if it saves more than **1.4 human minutes** ($0.44 ÷ $0.314 per minute). The week-5 pilot measures this.

### 6.5 30-second Reel (derived from a lesson; 4 scenes)
- **Opus cached:**
  - Input: script 10K × $4/M = $0.04; review 8K × $4/M = $0.032; 6 scene calls ($0.012 reads + $0.048 variable + $0.05 write) = $0.11. Input subtotal $0.182.
  - Output: 13K × $20/M = $0.26.
  - Total: (0.182 + 0.26) × 1.3 = **$0.57** (uncached **$0.81**).
- **Haiku cached:**
  - Script: $0.0014 + $0.0027.
  - 10 scene calls: $0.0014 + $0.0027 + $0.0017 write + $0.0204 output.
  - Review: $0.0011 + $0.0027.
  - Sum $0.034 × 1.3 = **$0.044**.
- **Ratio:** about 13x. If the cut-down is fully deterministic, the Reel's LLM cost is only the hook text, under $0.01.

### 6.6 The ratios, honestly
| Comparison | Ratio |
|---|---|
| Like for like, cached real-time: 4.43 / 0.34 | **13x** |
| Uncached vs uncached: 6.59 / 0.46 | 14x |
| Batch vs batch: 2.22 / 0.17 | 13x |
| Naive Opus (uncached, real-time) vs optimised Haiku (batch + cache): 6.59 / 0.17 | **39x** (about 2.7x of this is caching and batch, not the model) |
| Freeform Opus, V1 extrapolated linearly to 600 s [Hypothesis; probably worse than linear because context grows]: low $0.038 × 600 = $22.8, max $0.62 × 600 = $372, vs $0.34 | **67x to 1,094x** |
| Cascade vs Opus-only cached: 4.43 / 1.34 | 3.3x |

### 6.7 What 40-100x applies to
It applies to the **LLM line only**. Total variable cost per lesson:

| Scenario | Arithmetic | Total | vs $34 |
|---|---|---|---|
| Cheap-model system, review unchanged | 26.67 + 0.96 + 4.65 + 0.34 | **$32.62** | −4% |
| LLM cost at $0 | | $32.28 | −5% |
| Cheap-model system + review cut from 85 to 40 min | 40 × $0.314 = $12.55; 12.55 + 0.96 + 4.65 + 0.34 | **$18.50** | about 1.8x cheaper |

Across 1,000 lessons, cutting review to 40 minutes also takes the 8.85 FTE-months of review down to about 4.2.

### 6.8 Payback
The experiment cap is $1,500, roughly $1.50 per lesson over 1,000 lessons. Against Opus-only cached templated work, it saves $4.09 per lesson, so it pays back after about 370 lessons. Against the old budget repriced at current prices ($1.21), the saving is $0.87 per lesson, about 1,700 lessons to pay back. **The programme justifies itself through animation becoming affordable at all (vs $23-372 freeform) and through fewer review minutes, not through the LLM line alone.**

### 6.9 Chinese/open models and fine-tuning
- **No authoritative prices were supplied for DeepSeek, Qwen, Kimi or GLM, so none are assumed here.** Even at $0, they could save at most the remaining ~$0.34 per lesson, about 1% of total.
- [Recommendation] Run them through the same harness in week 6 only for vendor independence or data-residency reasons. Check Hindi and Hinglish quality, and apply the same safety and refusal checks.
- **Fine-tuning:** the strongest evidence is a fine-tuned Qwen 3 Coder 30B reaching 94% render success on Manim [N68], 3 points ahead of GPT-4.1 on visual similarity [N69]. GRPO also made models more responsive to renderer feedback [N72]. Distillation elsewhere achieved up to 30x lower cost [N73] with only 446 demonstrations [N78], but out-of-distribution regressions are documented [N77].
- [Hypothesis] Consider fine-tuning only after at least 500 accepted ledger traces, and only for a scene type where Haiku with the Kit is still below threshold after two doc iterations.

## 7. Quality gates and evals

**Gate thresholds** [Recommendation; thresholds are starting points]:
- **Determinism:** 100% double-render frame-hash match. Any miss blocks.
- **Science:** 0 errors in the academic gate. Any error blocks, and the scene type is frozen until the root cause is promoted into a validator or template.
- **Haiku with the Kit vs Opus medium on Golden-24:** first-pass validator pass rate ≥ 80%; pass@3 ≥ 95%; human blind A/B "not worse" in ≥ 90% of pairs.
- **Generalisation:** on the held-out 12, pass@3 within 5 percentage points of Golden-24. Otherwise the docs are overfitted.
- **Operations:** escalation rate ≤ 15% per scene type; refusal rate tracked [N16].
- **Review:** minutes per lesson ≤ the current 85 in the pilot, with a target of 40 by week 6 of production.
- **The headline metric** for every change: cost per accepted lesson, LLM plus human.

**Re-run Golden-24 on every Kit version and every model-ID change.** Model labels and prices change on published schedules.

## 8. Risks and failure modes
1. **Optimising the wrong line.** The LLM line is about 4% of cost; review is about 78%.
2. **Silent plausible-but-wrong output** from Haiku inflates review minutes. That can wipe out the $1-4 per lesson LLM saving after only 3-13 extra minutes. Mitigation: the verifier suite and flagged-scene review.
3. **The token model is entirely assumption** until it is metered. V1's tokens-to-dollars ratio is not reproducible, and this Mac lacks FFmpeg and Node 22, so no real renders exist yet.
4. **Tokenizer, effort and retry inflation** turn 40x into about 13x [N2, N9].
5. **Early stopping at low effort** [N9] and false "done" claims [N10]. Use medium effort and trust only the validator's exit codes.
6. **Cache misses.** Effort changes [N14], prefix drift, batch latency beyond TTL, prefixes too short to cache. Monitor the cache-read ratio in the ledger.
7. **Safety-classifier refusals on chemistry or biology content** with no server-side fallback [N16]. Route refusals to Sonnet and log them.
8. **Docs overfit to Golden-24.** The held-out set guards against this.
9. **Reviewer automation bias**: humans approving because the validators passed. Mitigation: seed 1 known defect per 10 lessons and track the catch rate.
10. **Model retirement or repricing** invalidates the Kit. The eval re-run is mandatory on any ID change.
11. **Runaway strong-model runs** (the V1 ultracode case). Hard caps apply.

## 9. Six-week rollout
- **Week 1: Unblock and measure.** Install Node 22 and FFmpeg. Render 3 real HyperFrames scenes. Build the ledger (JSONL plus a $ calculator from usage fields) and the eval runner. Freeze Golden-24 and the held-out 12. Run R0 (bare Haiku) and R1 (Opus medium) and replace the section 6 assumptions with metered numbers.
- **Week 2: Strong-model programme.** Run R2-R5 within the $1,500 cap. Academic team does the blind rubric scoring. Cluster failures against the 65 edge cases. Write ADRs.
- **Week 3: Distill.** Promote learnings into templates, validators and restrictions first, then exemplars and SKILL.md files. Write the 12 playbooks and cost cards. Run R6 #1.
- **Week 4: Iterate and wire up ops.** Two doc-iteration rounds on R6 failures. Add k=3 sampling, batch rounds, the 1-hour cache and cascade routing. Run R7 on the held-out set. Produce 1 full lesson and 3 Reels end-to-end.
- **Week 5: Pilot.** 5 lessons and 15 Reels through the cheap system with both human gates. Measure review minutes using the flagged-scene UI. Decide whether the Opus pre-review is worth more than 1.4 minutes per lesson.
- **Week 6: Decision gate.** Freeze Kit v1. Route permanently failing scene types to Sonnet. Optional open-model trial on the eval set. Go/no-go for a 50-lesson batch using cost per accepted lesson.
