# 08 · Cost tracking and budgets

**Purpose.** Control spend while the pipeline runs (per-stage caps, stop controls, the budget ledger, provider-job reconciliation), record the right numbers per lesson, and read the four planning workbooks correctly.

**Status of every number here:** "planning estimates and scenarios, not quotes, not benchmarks, not sales forecasts" (research date 13 Oct 2026). The only measured data in any workbook are eight silent 30-second fixture renders (27.3–29.4 s wall time on two local CPU workers), which are **not** a production render benchmark.

**Sources:** [`08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md`](../08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md), [`08_cost_models/CONSOLIDATED_COST_SCENARIOS.md`](../08_cost_models/CONSOLIDATED_COST_SCENARIOS.md) (Parts A–E), [`08_cost_models/COST_MODELS_EXPLAINED.md`](../08_cost_models/COST_MODELS_EXPLAINED.md), the workbooks in [`08_cost_models/workbooks/`](../08_cost_models/README.md), `src/examleaf/budget.py`, `src/examleaf_narration/cache.py`, `docs/Production_Runbook.md`, `docs/Higgsfield_Findings.md`, [`01_business_model/FINANCIAL_SCENARIOS_SUMMARY.md`](../01_business_model/FINANCIAL_SCENARIOS_SUMMARY.md).

---

## 1. Per-stage budgets and stop controls [RD-40]

v1 risk table: "Runaway retries or token consumption → **Per-stage budgets, retry caps, escalation, and stop controls**." The sources give per-video line items (v2 hybrid, `Per Video` sheet), not per-stage caps; this runbook sets the **initial cap for each stage equal to its modeled line** (which already includes the modeled regeneration allowance) and requires an explicit founder approval, recorded in the ledger, to reserve beyond it. Replace every cap with measured values after the four pilots.

| Stage(s) | Modeled line per lesson (v2 hybrid) | Initial cap | Stop controls |
|---|---|---|---|
| LLM work: S2–S7 (mapping, claims, plan, script, reviews), S8 routing | $1.716 (Sonnet 4.6 120k/25k + Opus 4.6 review 60k/10k + Haiku 4.5 routing 20k/3k, +30% regeneration) [RD-04] | $1.72 | VE: at most 2 failed repair attempts, then human escalation; no Skill reruns the whole script for a local edit (NA naturalizer/humour "small editing pass") |
| Narration synthesis S10 | $0.96 (8,000 chars × 1.2 × $0.10/1k) engine view; $0.936 (7,800 chars) narration view [RD-03] | $0.96 | Regenerate only affected segments; second unknown/repeated failure → review; no paid audio for silence |
| Alignment / audio QA S10–S11 | $0.10 | $0.10 | Reject unavailable language resources rather than retrying |
| Generated video (optional) S9 | $4.00 (20 s × 2 attempts × $0.10/s); **default 0 s** | **$0** unless the scene's route (rule 4/5) is approved; then ≤ $4.00 and ≤ 200 cents per scene estimate (`providers.example.json`) | "Zero is allowed; generation is not compulsory"; a failed scientific generative asset is replaced, never regenerated [RD-39] |
| Generated stills (thumbnails/backgrounds) | $0.20 | $0.20 | Deterministic text placed afterwards |
| Encoding / rendering S12 | $0.50 | $0.50 | Renderer failure: one retry after targeted repair, then escalate; render only changed scenes |
| Working storage | $0.20 | $0.20 | Retention policy; long retention compounds |
| Human: academic review | 45 min × $20/h = $15.00 | 45 min | First pilots: 8–16 academic/editorial **hours** per lesson (budget separately; "not a promise" of 85 min) |
| Human: production QA | 20 min × $15/h = $5.00 | 20 min | — |
| Human: repairs/editing | 20 min × $20/h = $6.67 | 20 min | Rising repair minutes trigger an alert |
| **Total variable** | **$34.34** ($30.34 with zero generated video) | | Batch pauses on budget exhaustion |
| Animation authoring (Claude Code), animated scenes S9 / Reels (added 15 Oct 2026; PA-11, RD-43) | **Not in the modeled total.** No pilot data. Provisional ceiling per non-template scene ≈ 78K tokens (the [V1] low-effort whole-video figure, ≈ $3 at API prices) [Hypothesis]; the [V1] max figure (≈ $49 per scene) is excluded by budget | Per scene ≤ 78K tokens; per Reel 3 scenes' worth; per lesson set after the first three pilot scenes; replace with measured p90 after the pilot (RD-40) | Alerts at 50/80 %, hard stop at 100 % of the scene cap; never ultracode; 3 creative rounds + 2 failed repairs then human (§8; 09 §4.1); data-bound scenes from approved templates ≈ 0 agent tokens. Source: `12_advanced_animations_with_claude/02_documentation/09_EFFORT_COST_GOVERNANCE.md` §10–§11 |

**Addendum (15 Oct 2026; RD-41): review cash is $0.** The founder does academic review, production QA and repairs in-house at no cash cost. The three human rows above keep their **minutes** as capacity caps (45 / 20 / 20 min) but their **cash is $0**. Review-free variable cost per lesson: **≈ $7.67** ($34.34 − $26.67) and **≈ $3.67** with zero generated video, before any animation-authoring spend. `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §7.13 gives the same totals as $7.68 / $3.68 (it rounds the LLM line to $1.72) plus a lean floor of ≈ $0.59 non-LLM [Hypothesis]. Capacity: 85 min/lesson ≈ **1,417 reviewer-hours per 1,000 lessons** (≈ 8.85 FTE-months), so review minutes, not AI, are the **throughput constraint**. Both human approvals stay mandatory: $0 cash removes no gate.

Global stop controls (runbook "Failure/retry policy", VE `observability-cost`, NA `cost-regeneration-optimizer`): validation failure stops **before** render or spend; budget exhaustion pauses the batch; unknown paid-job status is reconciled, never duplicated; auth/rights/language/capability failure is a hard stop; "**Freeze generation when invoice/cost state is unresolved**"; alert on p95 duration, repeated provider failure, spending anomalies and rising human repair minutes.

## 2. The budget ledger, idempotency and provider-job reconciliation

**Budget ledger [TESTED locally, not wired to providers]** (`src/examleaf/budget.py`): SQLite table `jobs(key PRIMARY KEY, cents, state)`, integer cents, `BEGIN IMMEDIATE` transactions.
- `reserve(key, cents)`: negative/empty → error; **same key + same cents → no-op** (idempotent); **same key + different cents → error** ("idempotency key reused with different cost"); if the sum of non-released rows + cents > limit → refused ("budget would be exceeded"); else row `reserved`.
- `settle(key, actual_cents)`: records the actual cost **even if it overruns**, then raises "vendor overrun recorded; production must pause" — "Record an unexpected vendor overrun honestly, then block further spending."
- Build item: a `release` transition for cancelled reservations (no method sets `released` today).

**ProviderJob [TESTED as a contract]:** `idempotency_key` (≥ 8), `provider`, `model`, `provider_job_id`, `state` ∈ planned / reserved / submitted / running / succeeded / failed / unknown, `estimated_cents`, `actual_cents`, `input_sha256`. States submitted/running/succeeded/**unknown** require the provider job ID: "persist provider job ID; do not resubmit an unknown job".

**Submission decisions [TESTED]** (`narration cache.decide_submission`): submitted/running/unknown → reconcile the existing job; succeeded → validate and cache; not-submitted → reserve then submit once; failed → review and authorize a bounded retry.

**Paid-generation call sequence** (`docs/Higgsfield_Findings.md`): model discovery → complete request estimate → attempt reserve → explicit budget → request/job persistence → actual invoice reconciliation. "Some operations do not support cost estimation; those need a separate approved bound rather than an invented price." A documented caller-supplied idempotency key "is useful only where the endpoint actually supports it."

**Reconciliation routine (build item for phase 3):** daily, match every `settled`/`succeeded` job against the provider's usage export or invoice; mismatches freeze generation for that provider until resolved; Runway workspace credits are recorded as credits ("not equivalent to an inferred ElevenAPI dollar price").

## 3. What to record per lesson (`lessons/<…>/costs.json`)

From the runbook ("Track estimated vs actual provider spend, input/output tokens, accepted generated seconds, attempts per accepted asset, cache hits, render worker-seconds, failure class, reviewer/editor minutes and revision count") and the pilot record (message 10 §9):

| Field | Unit | Note |
|---|---|---|
| Tokens in/out per model and per stage | tokens | Model IDs exact; compare to the cap |
| Characters synthesized (all attempts) and accepted | characters | Per segment; retake fraction |
| Generated seconds attempted / accepted | seconds | Default 0 |
| Attempts per accepted asset | count | Audio and visuals |
| Render worker-seconds (cold vs cached), peak memory | s, MB | From the render manifest |
| Cache hits / misses | count | Reason for every invalidation |
| Reviewer minutes by role (academic, production QA, native-language, audio) | minutes | Timed, not estimated |
| Editing / repair minutes | minutes | |
| Repairs: academic defects by severity, pronunciation repairs, revision count | count | |
| Failure classes | list | Validation / renderer / provider transient / unknown job / auth-rights-capability / budget |
| Provider spend estimated vs actual | cents | Per `ProviderJob` |
| Total cost | currency | "Machine cost is not total cost." |
| Student performance on a fresh question (pilots) | % | Immediate and delayed |
| Animation run ledger (added 15 Oct 2026; PA-11) | per run | Model ID (full, pinned), requested and **effective** effort, tokens in/out/cache read/cache write, wall time, rounds, repairs, outcome, credits; fields per `12_advanced_animations_with_claude/02_documentation/09_EFFORT_COST_GOVERNANCE.md` §9.2 |
| Reviewer minutes as capacity (15 Oct 2026; RD-41) | minutes | Cash $0; still timed, because minutes are the throughput limit |

Log minimal metadata, never secrets or student identifiers.

## 4. Headline numbers and their caveats

| Model | Headline | Caveat |
|---|---|---|
| v1 engine | **$2.37 machine + $18.00 human = $20.37 per video**; fixed $200/month; set-up $8,000; 1/100/1,000 videos: $220.37 / $2,236.76 / $20,567.62; 1,000 reviewer-hours = 6.25 FTE | Assumes an established component library; 45-min render "not a measured benchmark"; Fargate US-East, "not Mumbai" |
| v2 engine (three architectures) | Variable per video: AI-heavy **$158.98**, **hybrid $34.34**, mostly self-hosted $37.32; fixed $250 / $300 / $900 per month; set-up $5,000 / $10,000 / $16,000; hybrid at 1/100/1,000: $334.34 / $3,734.27 / $34,642.67 (≈ $44,643 with set-up) | "planning estimates using published tariff inputs — not vendor quotes or measured ten-minute production costs"; AI-heavy "does not assume equal scientific quality"; self-hosted "does not establish that every self-hosted implementation will cost more" |
| Hybrid without generated video | **≈ $30.34** variable per video | The production default [RD-39] |
| Review-free total (added 15 Oct 2026; RD-41) | **≈ $7.67** variable per lesson; **≈ $3.67** with zero generated video | Review cash $0 (in-house); minutes kept as capacity; arithmetic in 13 STRATEGY §7.13 ($7.68 / $3.68 with the LLM line rounded) |
| Human capacity (hybrid) | **85 human minutes per lesson** (45 academic + 20 QA + 20 repair) → 1,000 lessons ≈ 1,417 h ≈ **8.85 FTE-months** at 160 h | "Not a hiring promise"; "'No subject reviewers needed' is not the operating model being recommended" |
| Three-Short package | ≈ **$4.32** per source lesson ($4.316) | Overlaps the business "Reels" line |
| Narration (premium commercial TTS) | **≈ $12.50 variable** per video; $112.50 / $1,349.93 / $12,599.33 at 1/100/1,000 (fixed $100/month); ≈ 583 human hours at 1,000; set-up reserve $4,000 | Narration subsystem only; "Do not add these audio-review costs twice"; other methods $14.75 / $42.40 / $34.87 / $17.06 |
| Business (9 scenarios, ₹ lakh profit, Conservative / Base / Optimistic) | 500 books −7.99 / −6.22 / −5.25; 5,000 books −15.59 / **−6.09** / −0.04; 50,000 books −35.85 / **+34.07** / +76.43; Base contribution ₹118.13/book at 5,000; break-even 10,158 copies (5,000 tier), 27,001 (50,000 tier); max DTC CAC ₹118 (fully loaded ₹187); funding incl. 15% headroom (Base) ₹7.15 / 12.71 / 52.09 lakh | "planning scenarios, not sales forecasts or supplier quotations"; static break-even only within its cost tier; 18% output GST is a prudent scenario, not a classification opinion |
| Business pilot | Fixed budget **₹6.5 lakh**; suggested ceiling **₹8 lakh**; discovery cap **₹60,000**; "Reviewed chapter videos" 40 × ₹3,000 = ₹1.2 lakh | "not a mandate to spend it all"; ₹3,000 derivation not stated |

"**The important conclusion is not 'premium videos cost $2.'**" Human review dominates (88% of v1 variable cost; 78% of v2 hybrid). **[15 Oct 2026, RD-41]** These shares price review at planning rates; with review cash at $0 they are opportunity cost only, and review minutes are the throughput constraint rather than the cash cost driver. "One extra hour of skilled review can matter more than a large percentage reduction in render cost." "Reducing generation from roughly one dollar to a few cents matters less than eliminating avoidable pronunciation and synchronization repairs."

## 5. Exclusions to keep visible

Not inside the engine or narration models: taxes (incl. any tax on imported digital services), audience streaming (the business model reserves it per activated book), long-term asset retention, legal clearance, purchased hardware, royalties, voice buyouts and extended licensing, a larger engineering team, bespoke anatomy, complex mechanisms, extensive localization ("A second language requires new performance, QA and timeline verification"). The business model's lean launch does **not** include the engine/narration set-up ("A full bespoke video platform or 40-Skill engineering project is NOT quietly included").

## 6. Combining engine + narration + business without double counting

Procedure (from [`08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md`](../08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md) §4; the brackets are the organizing team's arithmetic, not ChatGPT outputs):

1. **Choose the scope once:** whole-video model = **v2 hybrid** (`Per Video` column C) [RD-15]; narration = the narration workbook, one method (default premium commercial TTS); business = Base case.
2. **Start** from the engine variable cost: v2 hybrid $34.34 (v1: $20.37).
3. **Delete the engine's audio lines:** v2 `Narration generation` $0.96 and `Alignment/audio allowance` $0.10 (v1: `Narration with regeneration` $0.768).
4. **Add the narration method:** machine part $1.666 (premium TTS) and, depending on the overlap decision, the human part $10.83 (25 review + 10 editing minutes).
5. *(15 Oct 2026, RD-41: review cash is $0, so the human parts in steps 4, 5 and 9 are opportunity cost; the business "Reviewed chapter videos" ₹3,000 line is opportunity cost, not cash.)* **Decide the human overlap in writing.** The engine's academic review covers "the entire final lesson" (including narration) and QA covers "audio, captions, continuity". Floor (all narration minutes already inside the engine's): **$34.95**; ceiling (none inside): **$45.78** per video (v1 basis: $21.27–$32.10). The naive sum $46.84 double counts. Replace the guess with timed minutes from the pilots.
6. **Use one table of unit rates** (academic $20/h, QA $15/h, repair $20/h, narration editor $15/h, performer $30/h — all planning rates) and **one tariff and character count** across the workbooks [RD-03].
7. **One fixed allowance and separate set-up lines:** pick one monthly fixed allowance (or justify both); add engine set-up ($10,000 hybrid) and the narration reserve ($4,000) only if their scopes do not overlap (v1's $8,000 already includes 20 design/voice hours) [RD-21].
8. **Price the pilot as a pilot:** 40 reviewed chapter videos in the business pilot, including fixed and set-up costs, not the 1,000-video average.
9. **Convert to INR** at the business planning rate ₹90/USD: hybrid + premium narration ≈ **₹3,145–₹4,120** per video (floor–ceiling) vs the business line ₹3,000 (= $33.33). If higher, raise `90-Day Budget!B6/C6/D6` (moves the Base case only) and, for the other cases, `Volume Inputs!D4,D6,D7,D9,D10,D12`.
10. **Add set-up as its own business budget line:** v2 hybrid ≈ ₹9.0 lakh, narration ≈ ₹3.6 lakh (v1 ≈ ₹7.2 lakh). The ₹8 lakh pilot ceiling cannot absorb it. Example (message 06 §11.5): a ₹10 lakh engineering project lowers Base 50,000-sale profit from ≈ ₹34.07 lakh to ≈ ₹24.07 lakh.
11. **Do not double count against business lines that already exist:** video delivery (₹21.24–33.98 per retained book), "Fixed hosting, tools, storage", "Reels, free-content packaging, community" (count Shorts once: $4.316 ≈ ₹388 per lesson), commerce/activation development.
12. Keep USD figures **before tax**; apply tax on imported services once, after CA advice.

## 7. What must be replaced with real quotes before committing money

| Item | Placeholder (13 Oct 2026) | Obtain |
|---|---|---|
| Printer | ₹190/160/135 (500), 125/105/88 (5,000), 95/78/65 (50,000) per copy; 50% advance | Three written like-for-like quotes per title, language and batch (256 pp, 7×10 in, 70 GSM, cover, binding, activation insert, freight, tax, spoilage, payment terms, **lead time**) |
| Courier / fulfilment | ₹85/65/55 per order; freight ₹15/10/8 | Aggregator account quotes by weight and pincode; COD/RTO; India Post written eligibility for the packed SKU |
| Marketplace | all-in ₹105/90/80; ads ₹45/25/15 | Fee schedule for the exact category and price band; Flipkart seller quotation (not researched) |
| CAC, conversion, sell-through, activation | ₹220/120/70; 5%; 75/90/97%; 50/70/80% | Observed pilot cohorts; partner commitments |
| GST classification | 18% on the whole bundle; 18% non-recovered hosting tax | Written CA/counsel advice (gate G3) |
| FX | ₹90/USD | Current rate + buffer at spend date |
| Video delivery minutes | 400 per activated book | Pilot analytics |
| TTS tariffs | $0.08 / $0.10 per 1k chars; **Eleven v4 TBD**; Cartesia > 8 M credits | Account/model quotation for the model you will use |
| LLM tariffs | two different label sets (§8) | Current pricing pages for the exact model IDs |
| Render benchmark | 45 min on 8 vCPU/16 GB (US-East Fargate); $0.30–0.50 encode | Timed full-lesson render, with narration, on your compositor and region (phase 1/2) |
| Reviewer, editor, performer rates | $20 / $12–15 / $20–25 / $30 per hour | Quotes from native subject reviewers and editors; voice buyout/licence terms |
| GPU / self-hosting | $0.80–$1/h; RTF 2 | Benchmark on target hardware (only if a self-hosting trigger is shown) |
| Generated video | $0.10/s illustrative route; no Higgsfield whole-lesson quote; Luma unresolved | Exact model/resolution/audio route quote; default zero seconds |
| Remotion billing | 20 billable renders per video assumed | Vendor confirmation of what counts as a billable render |
| Set-up / build budgets | $8,000; $5,000/$10,000/$16,000; $4,000; ₹6.5 lakh | Scoped, quoted work packages |
| Localization | not priced | Per-language native-review and re-recording quotes (Assamese has a separate acceptance gate) |

## 8. Model names and prices are editable inputs [RD-04]

v1 labels "Haiku 5.5 / Sonnet 5.5 / Opus 5.5" plus `gpt-6.1-sol` at $0.10/$0.50, $2/$10, $4/$20 and $2/$10 per million input/output tokens (LLM line $1.03/video). v2 labels "Haiku 4.5 / Sonnet 4.6 / Opus 4.6" at $1/$5, $3/$15, $5/$25 (LLM line ≈ $1.72/video). Both are dated 13 Oct 2026 and neither was independently verified. Keep the **routing roles** fixed (cheap model for extraction/routing, mid model for writing, strong model for independent review/escalation; the independent reviewer is a different agent/model from the author) and treat model names and prices as inputs to re-check on the providers' pricing pages before each phase gate (in Claude Code the `claude-api` skill can list current Anthropic model IDs and prices). Lifecycle dates that move numbers: Gemini 3.8 Flash TTS price doubles from 1 Jan 2027; OpenAI legacy TTS shutdown 6 Jan 2027; Eleven v4 unpriced; promotions excluded. Record a new "Checked" date at every update (message 06: "a monthly syllabus, competitor-price, and service-tariff alert").

**Effort governance (added 15 Oct 2026; PA-12, RD-43).** Every Claude run sets model and effort explicitly; nobody relies on defaults. Pin full model IDs (`claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`), never bare aliases. Scene code: Opus 5.5 at **high**; complex three.js, physics replay or intricate choreography: **xhigh**; max only with a written justification approved in the ledger. **Never ultracode** in production or unattended runs (a launch-script grep for `ultracode` or an alias blocks the batch). Iteration caps: 3 creative rounds per scene, then at most 2 failed repair attempts, then human escalation. Record the effective effort, not only the requested one. Per-surface defaults and the full rule: 09 §4.1.

## 9. Common mistakes (from `08_cost_models`)

1. Reading "$2.37 machine cost" as "videos cost $2" (it is $20.37–$34.34 because of human review). **[15 Oct 2026, RD-41]** With review cash at $0 the cash cost is ≈ $3.67–$7.67 per hybrid lesson, but the 85 review minutes still limit throughput; do not read "$0 review" as "review is optional".
2. Adding narration review on top of engine review without deciding the overlap.
3. Applying 1,000-video averages to a 40-video pilot.
4. Treating the nine business scenarios as forecasts or as 100× multiples of the pilot.
5. Using static break-even outside its cost tier.
6. Deducting the fully loaded marketing CAC (₹186.67) a second time.
7. Forgetting profit ≠ cash (Base 50,000: ₹34.07 lakh profit but ₹52.09 lakh funding capacity; funding needs across cases ₹6.03–95.52 lakh).
8. Editing `90-Day Budget` and expecting Conservative/Optimistic to move (only Base is linked).
9. Taking the 27–29 s proof render times as a production benchmark.
10. Presenting any of these numbers to a partner, lender or investor as a quote or forecast.
11. *(added 15 Oct 2026)* Pricing animation authoring from output tokens alone, or leaving effort at the default: agent loops re-read large contexts, and cost per written token rises with effort and multi-agent work (12/02/09 §2).
