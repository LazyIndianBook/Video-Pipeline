# Consolidated Cost Scenarios

**Section:** `08_cost_models/`. **Research date of every figure:** 13 October 2026. **Currency:** USD before tax for the three engine/narration models; INR (lakh = 100,000) for the business model. **Status:** *planning estimates and scenarios, not quotes, not forecasts, not benchmarks.* The workbooks, the messages and the JSON all say so in their own words (reproduced in `README.md` section 6).

This file gathers **every cost table ChatGPT published** in the four messages, **verbatim**, together with the assumptions that sit behind each table, then the extra tables that exist only in the workbooks (so nothing is hidden in an .xlsx), and finally a **reconciliation** of how the four models relate and where they overlap.

| Part | Model | Source message (section) | Workbook | Scenarios |
|---|---|---|---|---|
| A | Video engine v1 (reusable-component stack) | Message 02, section 13 | `workbooks/v1_engine_...xlsx` | 1 / 100 / 1,000 videos |
| B | Video engine v2 (three architectures) | Message 10, section 11 | `workbooks/v2_engine_...xlsx` | AI-heavy / Hybrid / Self-hosted x 1 / 100 / 1,000 |
| C | Narration sub-system (five methods) | Message 12, section 13 | `workbooks/narration_...xlsx` | 5 methods x 1 / 100 / 1,000 |
| D | Business model (book-linked) | Message 06, sections 10, 11, 14 (+2.1, 4.1, 4.3, 8.4, 15.1) | `workbooks/business_...xlsx` + `model_assumptions_and_results.json` | 3 cases x 500 / 5,000 / 50,000 retained books; break-even; CAC; working capital; pilot budget |
| E | Reconciliation of A-D | (this file) | | overlaps, currency, tax, dating |

**How the verbatim blocks were made.** Each block is copied programmatically from the message file named above it (line range stated), so the numbers are not retyped. Only the private-use citation markers that ChatGPT's export inserts (the `cite...turn...` tokens) were removed. Everything else, including LaTeX such as `\[ ... \]`, bold and tables, is as ChatGPT wrote it.

**Cross-checks performed while building this file (all matched):** every number in the four message tables was compared with the workbook values (e.g. v1 $220.37 / $2,236.76 / $20,567.62; v2 $408.98 / $16,147.60 / $159,226.00 etc.; narration $112.50 / $1,349.93 / $12,599.33 etc.; business nine-scenario profits, 10,158 and 27,001 break-evens, Rs 118 and Rs 187 CAC, Rs 7.15 / 12.71 / 52.09 lakh funding) and the nine `results` in `model_assumptions_and_results.json` against the Dashboard. No numeric discrepancy between message, workbook and JSON was found. The differences that *do* exist are between models (labels, tariffs, rates), and are listed in Part E.

---

## Part A. Video engine v1: cost of one 10-minute video, 1 / 100 / 1,000 videos

**Workbook:** `workbooks/v1_engine_ExamLeaf_Cost_and_Skills.xlsx` (sheets Inputs, UnitCosts, Volumes). **Assumption basis:** "a working reusable-component library, ordinary 2D STEM lessons, cloud model APIs, ElevenLabs narration, and CPU rendering"; no promotions, free tiers, batch discounts or caching savings; 45-minute render time and 4 maintenance hours/month are *not* measured; prices are US East examples, not Mumbai.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/02_ASSISTANT_video_engine_architecture_and_plan_v1.md`, lines 628-718 (section 13, Cost analysis: 1, 100, and 1,000 videos). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 13. Cost analysis: 1, 100, and 1,000 videos

##### What the model represents

The baseline assumes a working reusable-component library, ordinary 2D STEM lessons, cloud model APIs, ElevenLabs narration, and CPU rendering.

It **does not** assume that the first bespoke biology animation costs the same as the hundredth lesson using approved components.

All amounts below are **USD before taxes**, except the separately quoted Sarvam price. No currency conversion, introductory promotion, free tier, or batch discount is assumed.

##### AI token budget per video

| Task | Planning allowance: input/output tokens | Verified rates per million input/output tokens | Estimated cost |
|---|---:|---:|---:|
| Haiku 5.5 extraction/routing | 30,000 / 5,000 | $0.10 / $0.50, within its short-prompt tier | $0.0055 |
| Sonnet 5.5 writing/component adaptation | 120,000 / 25,000 | $2 / $10 | $0.4900 |
| Independent `gpt-6.1-sol` review | 60,000 / 10,000 | $2 / $10, short-context rates | $0.2200 |
| Opus 5.5 escalation reserve | 10,000 / 2,000, amortized | $4 / $20 | $0.0800 |
| **Subtotal** | | | **$0.7955** |
| **Including 30% rewrite/retry allowance** | | | **$1.0342** |

The token workloads are assumptions; the listed prices are from current official pricing documentation.

##### Other variable costs

| Component | Assumption | Cost/video |
|---|---|---:|
| Narration | 8,000 characters × 1.20 regeneration × $0.08/1,000 | **$0.7680** |
| Rendering | 8 vCPU, 16 GB; 45 worker-minutes; 20% retry reserve | **$0.3555** |
| ASR validation | 10 minutes × $0.003/minute | **$0.0300** |
| Working-asset storage | 2 GB for one month × $0.015/GB-month | **$0.0300** |
| Miscellaneous API/request reserve | Planning allowance | **$0.1500** |
| **Variable machine cost, including LLMs** | | **$2.3676** |

The compute calculation uses AWS Fargate’s published US East CPU/memory rate example; storage uses R2 standard pricing. **The 45-minute render duration is not a measured benchmark**, and these are not Mumbai-region prices.

##### Human review and fixed overhead

The baseline allows **45 minutes of academic review at $20/hour** and **15 minutes of production QA at $12/hour**: **$18/video**.

Fixed monthly allowances are **$100 for infrastructure/tools** and **$100 for maintenance**. Four maintenance hours per month is a mature-system planning assumption, not a realistic allowance during active engine development.

Therefore:

\[
\text{Production cost}
=
N(2.3676+18)+200
\]

##### Volume comparison

All three cases use the same one-month accounting period.

| Cost | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|
| Variable machine costs | $2.37 | $236.76 | $2,367.62 |
| Human review | $18.00 | $1,800.00 | $18,000.00 |
| Fixed overhead | $200.00 | $200.00 | $200.00 |
| **Total production cost** | **$220.37** | **$2,236.76** | **$20,567.62** |
| **Average production cost/video** | **$220.37** | **$22.37** | **$20.57** |
| Reviewer hours | 1 | 100 | 1,000 |

**The important conclusion is not “premium videos cost $2.”** Approximately $2.37 is the assumed machine portion. Academic and final-video review dominate the baseline cost.

At 1,000 videos per month, the model requires **1,000 reviewer-hours**, equivalent to **6.25 full-time equivalents at 160 hours/month**. Automation does not eliminate that capacity requirement.

##### Initial implementation budget

An illustrative initial budget is:

**240 engineering hours × $25 + 60 academic-template hours × $25 + 20 design/voice hours × $25 = $8,000.**

That produces first-batch totals of approximately **$8,220**, **$10,237**, and **$28,568** respectively.

This is an initial engine/template budget—not a quote or promise for a fully mature platform. Bespoke diagrams, extensive localization, rights clearance, and complex 3D can increase it substantially.

##### Open-source, commercial, and self-hosted alternatives

| Approach | Economic interpretation | Recommendation |
|---|---|---|
| **HyperFrames + commercial AI/TTS** | Low renderer licensing burden; usage-based model/audio costs | **Best initial balance** |
| **Remotion + commercial AI/TTS** | Similar variable media costs, plus applicable renderer licensing | Choose when saved engineering effort exceeds licensing cost |
| **HyperFrames + self-hosted Kokoro** | Removes the $0.768 narration API line, but adds inference, integration, and maintenance | Test for previews first; production only after audition |
| **More extensively self-hosted AI** | Replaces API bills with hardware utilization, serving, maintenance, and model-quality risk | Consider after real volume and performance measurements exist |

For Remotion, the workbook includes an optional assumption of **20 billable renders/video**. At the published automation rate, this would add **$100, $100, and $200** to the three volume cases when the paid licence applies. The billable-render interpretation must be confirmed.

At 1,000 videos, the baseline LLM-plus-narration API spend is only about **$1,802/month**. That is the relevant ceiling against which additional self-hosted serving and maintenance should be compared—not a hypothetical unlimited API bill.

**Sensitivity:** increasing human review from $18 to $40 adds $22/video. One extra hour of skilled review can matter more than a large percentage reduction in render cost.



### A.1 Supporting voice-provider price points quoted in message 02 (feeds the narration line)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/02_ASSISTANT_video_engine_architecture_and_plan_v1.md`, lines 512-526 (section 10, voice provider shortlist and prices). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

##### 10. Voice and narration

###### Recommended provider shortlist

These are candidates for audition, not an assertion that one has objectively superior naturalness for your students.

| Engine | Recommended position | Current price/capability consideration | Main caution |
|---|---|---|---|
| **ElevenLabs Multilingual v2** | Initial English production candidate | Listed standard API rate: **$0.08/1,000 characters** | Test STEM pronunciation and specific voice rights. |
| **ElevenLabs newer models** | Challenger in the audition | Evaluate newer expressive models against the stable baseline | Do not assume newer means clearer for equations. The checked page still showed a promotion ending 12 October; it is excluded from the cost model. |
| **Cartesia Sonic 3.6** | Strong cost/quality challenger | Pro: **$5/100,000 credits**; Startup: **$49/1.25 million**; one TTS character per credit | Effective cost depends on using the plan allowance; minimum subscriptions matter. |
| **Sarvam Bulbul v3** | Indian-language candidate for documented locales | **₹30/10,000 characters** | Confirm exact model/language support, not just marketing claims. |
| **Google Chirp 3 HD** | Alternative multilingual enterprise provider | **$30/million characters** beyond applicable free allowances | Audition terminology, pacing, and language-specific voice quality. |
| **Kokoro 82M** | Self-hosted preview voice and possible production challenger | Apache-2.0 model weights; no per-character provider fee | Compute, integration, voice suitability, and language limitations remain. |
| **OpenAI speech workflow** | Re-evaluate before adoption | The checked older TTS model card is marked deprecated | Do not deploy the old Skill’s default without selecting a supported replacement. |



### A.2 Workbook-only detail: `Volumes` sheet at full precision (v1)

These rows (reviewer FTE, render-worker hours, machine share) are in the workbook but not in the message table. USD.


| Metric | 1 video | 100 videos | 1,000 videos |
|---|---|---|---|
| Videos | 1 | 100 | 1,000 |
| Variable machine cost | 2.3676 | 236.7617 | 2,367.62 |
| Human review | 18 | 1,800 | 18,000 |
| Fixed overhead for accounting period | 200 | 200 | 200 |
| Optional Remotion licensing | 0 | 0 | 0 |
| TOTAL PRODUCTION COST | 220.3676 | 2,236.76 | 20,567.62 |
| Average production cost per video | 220.3676 | 22.3676 | 20.5676 |
| One-time implementation | 8,000 | 8,000 | 8,000 |
| TOTAL INCLUDING IMPLEMENTATION | 8,220.37 | 10,236.76 | 28,567.62 |
| Reviewer hours required | 1 | 100 | 1,000 |
| Render worker hours required | 0.9 | 90 | 900 |
| Reviewer FTE at 160 h/month | 0.0063 | 0.625 | 6.25 |
| Machine cost share of production | 0.0107 | 0.1059 | 0.1151 |


Optional Remotion licence (not in the totals above; switch `Inputs!B51 = 0`): **$100 / $100 / $200** at 1 / 100 / 1,000 videos if the paid licence applied and 20 billable renders/video were confirmed.

**Unit-cost lines (USD per video), v1 `UnitCosts`:** Haiku extraction/routing 0.0055; Sonnet scripting 0.49; independent OpenAI review 0.22; Opus escalation reserve 0.08; base LLM subtotal 0.7955; LLM with 30% regeneration 1.03415; narration 0.768; rendering 0.35546688; ASR 0.03; storage 0.03; API reserve 0.15; **variable machine cost 2.36761688**; academic review 15; production QA 3; **human review 18**; **total variable 20.36761688**; fixed monthly overhead 200; one-time implementation 8,000.

---

## Part B. Video engine v2: three architectures per finished 10-minute video

**Workbook:** `workbooks/v2_engine_ExamLeaf_Video_Engine_Cost_Model.xlsx` (sheets Inputs, Per Video, Volume Model, Decision). **Assumption basis (message 10):** published tariff inputs + workload assumptions; "planning estimates ... not vendor quotes or measured ten-minute production costs"; default generated-video allowance is zero seconds; no Higgsfield whole-lesson quote is claimed.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/10_ASSISTANT_video_engine_implementation_v2.md`, lines 590-658 (section 11, Production costs: three architectures). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 11. Production costs: three architectures

The workbook contains editable formulas for **1, 100, and 1,000 videos**, plus human-capacity and optional-Shorts calculations.

**All figures below are USD before tax.** They are planning estimates using published tariff inputs—not vendor quotes or measured ten-minute production costs.

##### 11.1 Tariff and workload basis

The illustrative API workload uses:

- Sonnet 4.6: 120,000 input and 25,000 output tokens.
- Opus 4.6 review: 60,000 input and 10,000 output tokens.
- Haiku 4.5 routing: 20,000 input and 3,000 output tokens.
- A 30% LLM regeneration allowance.

At the checked published rates, this gives approximately **$1.72 of LLM usage per lesson**. The token workloads are assumptions, not observations from the local proof.

Narration assumes 8,000 characters, 20% regeneration, and **$0.10 per 1,000 characters**, giving approximately **$0.96**. That tariff is from the checked ElevenLabs API page; the separate Runway audition used workspace credits and is not billed by this calculation.

The generated-video comparison uses an illustrative **$0.10/second provider route**, not a Higgsfield whole-lesson price. Exact requests may have additional model/input/resolution charges.

##### 11.2 Per-video operating assumptions

| Component | Commercial AI-heavy | Recommended hybrid | Mostly self-hosted |
|---|---:|---:|---:|
| Generated video | 600 seconds × 1.8 attempts | Optional 20 seconds × 2 attempts | None |
| Machine cost, including modeled regeneration | **$111.48** | **$7.68** | **$2.32** |
| Academic, production QA, and repair labour | **$47.50** | **$26.67** | **$35.00** |
| **Variable cost/video** | **$158.98** | **$34.34** | **$37.32** |
| Fixed monthly allowance | $250 | $300 | $900 |
| Illustrative one-time setup | $5,000 | $10,000 | $16,000 |

The self-hosted case assumes more maintenance/repair effort and unbenchmarked GPU workloads. It does **not** establish that every self-hosted implementation will cost more than hybrid.

The AI-heavy case does **not** assume equal scientific quality. More spending cannot make an unvalidated generated diagram acceptable.

##### 11.3 Total operating cost by volume

All cases use the same one-month accounting period.

| Architecture | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|
| **Commercial AI-heavy** | **$408.98** | **$16,147.60** | **$159,226.00** |
| **Hybrid** | **$334.34** | **$3,734.27** | **$34,642.67** |
| **Mostly self-hosted** | **$937.32** | **$4,631.50** | **$38,215.00** |

These totals exclude the separately displayed setup investment.

For the hybrid case at 1,000 videos:

- Operating production: approximately **$34,643**.
- Including the illustrative initial setup: approximately **$44,643**.
- Removing the optional generated-video allowance reduces variable cost to approximately **$30.34/video**.

The proposed three-Short package adds approximately **$4.32 per source lesson** under its stated token, voice, rendering, and editorial allowances.

###### Human capacity is the major scaling constraint

The hybrid model includes **85 human minutes per lesson** across academic review, production QA, and repairs.

At 1,000 lessons, that is approximately **1,417 hours**, or **8.85 full-time-equivalent months at 160 hours each**.

“Minimal repetitive work” is realistic. “No subject reviewers needed” is not the operating model being recommended.

###### Exclusions to keep visible

Taxes, audience streaming, long-term asset retention, legal clearance, purchased hardware, royalties, and a larger engineering team are not silently included. New bespoke anatomy, complex mechanisms, or extensive localization can materially increase costs.

The separate local proof had no cloud-render invoice. That is **not evidence that production rendering is free**.



### B.1 Supporting assumption from message 10 section 4: the default for generated video


> *Verbatim extract: `00_source/chatgpt_transcript/messages/10_ASSISTANT_video_engine_implementation_v2.md`, lines 194-208 (section 4, where generative media belongs). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 4. Where generative media belongs

##### 4.1 Route by scientific responsibility

| Scene type | Default production method |
|---|---|
| Formula, derivation, graph, calculation | Deterministic |
| Atom identity, charge, reaction state | Domain-validated deterministic representation |
| Chromosome count, genetic probability, process direction | Explicit reviewed state model |
| Anatomical/spatial structure | Reviewed SVG or licensed/approved 3D model |
| Contextual real-world illustration | Owned/licensed media or selectively generated illustration |
| Thumbnail background, visual metaphor, brand exploration | Optional generation; exact text added afterward |

**The default generated-video allowance should be zero seconds.** Add generated material only when it serves a clear instructional purpose.



### B.2 Workbook-only detail: `Per Video` line items (USD per finished video)

The message table gives machine/human totals only; the workbook breaks them into the lines below.


| Cost category | AI-heavy | Hybrid | Mostly self-hosted |
|---|---|---|---|
| LLM reasoning / independent review | 1.716 | 1.716 | 1.515 |
| Narration generation | 0.96 | 0.96 | 0.05 |
| Generated video clips | 108 | 4 | 0 |
| Generated stills | 0.2 | 0.2 | 0 |
| Encoding/rendering | 0.3 | 0.5 | 0.5 |
| Alignment/audio allowance | 0.1 | 0.1 | 0.05 |
| Working storage | 0.2 | 0.2 | 0.2 |
| Machine subtotal | 111.476 | 7.676 | 2.315 |
| Academic review | 25 | 15 | 20 |
| Production QA | 7.5 | 5 | 5 |
| Repairs / editing | 15 | 6.6667 | 10 |
| Human subtotal | 47.5 | 26.6667 | 35 |
| TOTAL VARIABLE COST | 158.976 | 34.3427 | 37.315 |
| Monthly fixed allowance | 250 | 300 | 900 |
| One-time setup | 5,000 | 10,000 | 16,000 |
| Human minutes/video | 150 | 85 | 110 |


### B.3 Workbook-only detail: `Volume Model` (USD; same one-month period)


| Architecture | Videos | Variable USD/video | Variable USD | Fixed USD | Operating total USD | Average USD/video | Setup USD | Total with setup USD |
|---|---|---|---|---|---|---|---|---|
| AI-heavy | 1 | 158.98 | 158.98 | 250 | 408.98 | 408.98 | 5,000 | 5,408.98 |
| AI-heavy | 100 | 158.98 | 15,897.6 | 250 | 16,147.6 | 161.48 | 5,000 | 21,147.6 |
| AI-heavy | 1,000 | 158.98 | 158,976 | 250 | 159,226 | 159.23 | 5,000 | 164,226 |
| Hybrid | 1 | 34.34 | 34.34 | 300 | 334.34 | 334.34 | 10,000 | 10,334.34 |
| Hybrid | 100 | 34.34 | 3,434.27 | 300 | 3,734.27 | 37.34 | 10,000 | 13,734.27 |
| Hybrid | 1,000 | 34.34 | 34,342.67 | 300 | 34,642.67 | 34.64 | 10,000 | 44,642.67 |
| Self-hosted | 1 | 37.31 | 37.31 | 900 | 937.32 | 937.32 | 16,000 | 16,937.31 |
| Self-hosted | 100 | 37.31 | 3,731.5 | 900 | 4,631.5 | 46.31 | 16,000 | 20,631.5 |
| Self-hosted | 1,000 | 37.31 | 37,315 | 900 | 38,215 | 38.22 | 16,000 | 54,215 |


Capacity and add-ons: hybrid reviewer hours at 1,000 videos **1,416.67 h**; hybrid FTE equivalent **8.85 FTE-months** ("Not a hiring promise; workload allocation"); optional three-Short package **$4.316 per lesson**; optional Remotion paid tier at 1,000 videos **$200/month** ("Only if licence applies; render count needs confirmation"); hybrid with zero generated clips **$30.34 per video** variable.

**Measured, not assumed (the only measured data in the four workbooks, `Measured Proof` sheet):** eight silent 30-second fixture renders at 1280x720 and 720x1280, 27.3-29.4 s render wall time each on two local CPU workers; "not full curriculum pilots", "no teacher approval or student study", 56 tests passed. Explicitly **not** a cloud price or a forecast for 10-minute narrated lessons.

---


## Part C. Narration sub-system: five production methods, 1 / 100 / 1,000 ten-minute videos

**Workbook:** `workbooks/narration_ExamLeaf_Narration_Cost_Model.xlsx` (sheets Summary, Inputs, Methods, Provider Tariffs). **Scope (message 12):** "the narration subsystem, including script-direction allowance, synthesis, audio QA, editing, and the modeled human work. They do not include full academic research, animation production, platform marketing, or audience streaming. Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget." Planning assumptions, not quotations or measured TTS benchmarks.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/12_ASSISTANT_narration_system.md`, lines 641-702 (section 13, Costs for 1, 100, and 1,000 ten-minute videos). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 13. Costs for 1, 100, and 1,000 ten-minute videos

##### 13.1 Scope and assumptions

These estimates cover the **narration subsystem**, including script-direction allowance, synthesis, audio QA, editing, and the modeled human work.

They do **not** include full academic research, animation production, platform marketing, or audience streaming. Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget.

All values are **USD before tax**, using one monthly accounting period.

###### Baseline inputs

| Input | Assumption |
|---|---:|
| Finished media length | 10 minutes |
| Active speech | 8.5 minutes |
| Transcript length | 7,800 characters |
| Generation/retry allowance | 20% |
| LLM narration editing/direction | $0.60/video |
| ASR/alignment/automatic QA allowance | $0.08/video |
| Storage/export allowance | $0.05/video |
| Academic audio reviewer | $20/hour |
| Audio editor | $15/hour |
| Performer | $30/recording hour |
| Illustrative GPU cost | $0.80/hour |
| Self-hosted real-time factor | 2 compute seconds per generated audio second |

Personnel rates, processing times, retry rate, and GPU figures are **editable planning assumptions, not quotations or measured TTS benchmarks**.

##### 13.2 Provider generation costs

The reference commercial calculation uses **$0.10 per 1,000 characters**, a published v2/v3 rate—not an invented Eleven v4 price. With 20% regeneration:

\[
7{,}800\times1.2/1{,}000\times\$0.10=\$0.936
\]

The published speech-to-speech reference is **$0.12 per generated minute**, before separate performer and review costs.

Gemini 3.8 Flash TTS currently lists **$0.50/million input tokens and $9/million audio output tokens**, with scheduled increases to **$1 and $18 from 1 January 2027**. Its pricing specifies 25 audio tokens per second. Under the workbook’s workload, synthesis is approximately **$0.139 now** or **$0.278 at the scheduled rate**, before QA and labour.

Cartesia’s plans list **$5/100,000 credits, $49/1.25 million, and $299/8 million**. At 9,360 generated characters per lesson, 100 lessons fit within 1.25 million credits, but 1,000 lessons require 9.36 million—beyond the 8-million allowance. Obtain the actual overage or higher-tier quote rather than extrapolating a false fixed price.

##### 13.3 Five production methods

| Method | Variable cost/video | Monthly fixed allowance | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|---:|---:|
| **Premium commercial TTS** | **$12.50** | $100 | **$112.50** | **$1,349.93** | **$12,599.33** |
| Primarily self-hosted | $14.75 | $300 | $314.75 | $1,775.20 | $15,052.00 |
| Human recorded | $42.40 | $100 | $142.40 | $4,339.67 | $42,496.67 |
| Human performance + speech-to-speech | $34.87 | $125 | $159.87 | $3,612.07 | $34,995.67 |
| Hybrid: 80% TTS, 20% performed/converted | $17.06 | $150 | $167.06 | $1,855.69 | $17,206.93 |

The table assumes different review/editing workloads for each method. **It does not prove that self-hosting inherently costs more.** At equal labour requirements, it can be cheaper; actual retakes and maintenance decide the result.

###### The dominant cost

The premium case allows **25 minutes of academic audio review and ten minutes of editing per video**. At 1,000 videos, that is approximately **583 human hours**.

Reducing generation from roughly one dollar to a few cents matters less than eliminating avoidable pronunciation and synchronization repairs.

An illustrative **$4,000 initial narration-subsystem implementation reserve** is separate. Voice buyouts, broader licences, substantial new localization, and hardware purchases require additional budgeting.



### C.1 Supporting lifecycle fact from message 12 section 2.4 (OpenAI speech)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/12_ASSISTANT_narration_system.md`, lines 121-131 (section 2.4, OpenAI speech migration). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 2.4 OpenAI speech: a migration issue must be handled now

The current official deprecation notice schedules `tts-1`, `tts-1-hd`, and the listed `gpt-4o-mini-tts` snapshots for removal on **6 January 2027**. It names **`gpt-realtime-2.1-mini`** as the recommended replacement. Older guides and public Skills still contain legacy examples.

Therefore:

**Do not start a new ExamLeaf catalogue on an old TTS snapshot merely because a Skill still uses it.**

The replacement is a realtime model with a different integration context. Its documentation lists text and audio pricing, but it should not be treated as a proven drop-in prerecorded-narration replacement without an exact-script audition and endpoint test.

The supplied OpenAI recipe is consequently an **offline migration fixture**. The code blocks it for new production.



### C.2 Workbook-only detail: machine vs human split per method (`Methods` sheet; USD per video)


| Method | TTS fraction | Record hours | STS fraction | Review min | Edit min | GPU flag | Fixed / month | Machine / video | Human / video | Variable / video | Human min / video |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Premium commercial TTS | 1 | 0 | 0 | 25 | 10 | 0 | 100 | 1.666 | 10.8333 | 12.4993 | 35 |
| Primarily self-hosted | 0 | 0 | 0 | 30 | 15 | 1 | 300 | 1.002 | 13.75 | 14.752 | 45 |
| Human recorded | 0 | 1 | 0 | 20 | 20 | 0 | 100 | 0.73 | 41.6667 | 42.3967 | 100 |
| Human performance + STS | 0 | 0.75 | 1 | 20 | 15 | 0 | 125 | 1.954 | 32.9167 | 34.8707 | 80 |
| Hybrid: 80% TTS / 20% performed | 0.8 | 0.15 | 0.2 | 25 | 10 | 0 | 150 | 1.7236 | 15.3333 | 17.0569 | 44 |


Inputs behind it (narration `Inputs`): active spoken 8.5 min; transcript 7,800 characters; retry allowance 20%; premium TTS $0.10 per 1,000 characters (v2/v3 reference, **not** an Eleven v4 quote); speech-to-speech $0.12 per generated minute; LLM direction $0.60 + ASR/QA $0.08 + storage/export $0.05 per video; academic audio review $20/h; audio editor $15/h; performer $30/recording hour; GPU $0.80/h at real-time factor 2; setup reserve $4,000 (separate); Gemini 25 audio tokens/s, 2,500 input tokens/script.

Summary-sheet extras: initial setup **$4,000** (not in operating totals); **Premium at 1,000 including setup $16,599.33**; **Premium at 1,000 with review time doubled $20,932.67**.

### C.3 Provider generation costs in the workbook (`Provider Tariffs`, USD for the modeled lesson)


| Provider / method | Pricing basis | Example synthesis cost | Scope | Lifecycle / limit |
|---|---|---|---|---|
| ElevenLabs v2/v3 reference | $0.10 / 1,000 chars | 0.936 | 9,360 generated characters | Reference budget, not verified v4 tariff |
| Eleven v4 | Account/model quote required | TBD | Latest expressive audition candidate | Do not infer from v2/v3 or approximate $/minute marketing |
| Gemini 3.8 Flash TTS — now | $0.50 input / $9 output per million | 0.1392 | 612 generated seconds + estimated text | Current through 2026-12-31 per published schedule |
| Gemini 3.8 Flash TTS — scheduled | $1 input / $18 output per million | 0.2784 | Same workload | Scheduled from 2027-01-01; recheck |
| Cartesia Pro | $5 / 100,000 credits | Plan, not variable invoice | 1 character = 1 TTS credit | Allowance, concurrency and model constraints apply |
| Cartesia Startup | $49 / 1.25 million credits | $49 plan fits 936,000 chars | 100 lessons at the modeled length | Does not price 1,000 lessons |
| Cartesia Scale | $299 / 8 million credits | 9.36 million exceeds this allowance | 1,000 modeled lessons | Obtain higher tier / overage quote |
| OpenAI realtime2.1-mini | $0.60 / M text input; $20 / M audio output | Usage-dependent | Do not transplant Gemini token/second rate | New adapter and exact-script audition required |
| OpenAI old TTS models | Legacy migration fixture | Do not use for new production | Model shutdown 2027-01-06 | Official notice 2026-10-01 |
| Eleven speech-to-speech | $0.12 / generated minute | 1.224 | 10.2 generated minutes with retry allowance | Voice rights + human reference production separate |
| Human performance | Illustrative $30 / recording hour | Not a market quote | Recording time is NOT finished audio time | Buyouts, licensing and retakes must be quoted |
| Self-hosted inference | Illustrative $0.80 / GPU hour | 0.272 | RTF 2, including 20% regeneration | No local neural TTS benchmark performed |


Hours at 1,000 videos (human audio work): Premium 583.33 h; Primarily self-hosted 750 h; Human recorded 1,666.67 h; Human performance + STS 1,333.33 h; Hybrid 733.33 h.

---

## Part D. Business model: nine scenarios, break-even, CAC, working capital, pilot budget

**Workbook:** `workbooks/business_ExamLeaf_Business_Model.xlsx` and `model_assumptions_and_results.json`. **Currency:** INR; money columns in the nine-scenario table are **Rs lakh**; revenue excludes modeled output GST; profit is before financing and income tax. **Status (message 06):** "These are planning scenarios, not sales forecasts or supplier quotations."

### D.0 Executive verdict, as published


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 5-27 (Executive verdict). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### Executive verdict

**ExamLeaf can become a viable publishing-led education business—but “viral videos + a QR code inside a book” is not a sufficient competitive advantage.**

The stronger business is:

> **Board-specific revision and practice, with reliable solutions and short videos that help students correct the exact mistakes they make.**

Use free videos to demonstrate that system. Sell the convenience, structure, academic reliability, and practice experience—not merely access to information already available elsewhere.

I recommend **two initial Class 10 titles, three carefully selected free chapters per subject, an optional digital-only purchase, and a two-book bundle**. Do not begin by funding six books, a native app, a large custom video platform, and a nationwide marketing operation simultaneously.

The financial conclusions are important:

| Scale | Interpretation under the model developed here |
|---|---|
| **500 retained book sales** | A product-validation exercise, not enough to recover the initial content and launch investment. |
| **5,000 retained book sales** | Meaningful demand, but the base case still loses money after properly allocating content, staffing, and launch costs. |
| **50,000 retained book sales** | Potentially profitable—but only with controlled acquisition costs, good inventory sell-through, sufficient working capital, and disciplined distribution. |

In the **base operating scenario**, 50,000 retained sales produce approximately **₹1.82 crore of publisher revenue excluding modeled GST and ₹34.07 lakh of operating profit**, before financing and income tax. However, that scenario needs approximately **₹52.09 lakh of funding capacity**, including modeled working-capital headroom. The conservative scenario loses money even at 50,000 sales.

These are **planning scenarios, not sales forecasts or supplier quotations**.



### D.1 What is verified versus estimated; the tax warning; scenario assumptions; base economics; channel contribution (message 06 section 10)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 540-617 (section 10, Pricing and unit economics). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 10. Pricing and unit economics

##### 10.1 What is verified versus estimated?

| Input | Status |
|---|---|
| Razorpay standard 2% platform fee plus GST | Published provider pricing; promotional periods excluded |
| Amazon Books referral fee of 2% for prices above ₹250 through ₹500 | Published category rate; not the total selling cost |
| Cloudflare delivery at $1 per 1,000 delivered minutes | Published provider tariff |
| Printing, courier cost, CAC, sell-through, staffing and conversion rates | Planning assumptions requiring validation |
| ₹90/USD | Budget conversion assumption, not a live exchange-rate quote |
| 18% output GST on the bundle | Cautious model assumption, not a classification conclusion |

Amazon also charges other fees, and book bundles may have different category treatment. Do not interpret a low or zero referral rate as free distribution.

###### Tax warning

**Do not assume the entire book-plus-premium-video offer is exempt merely because it contains a printed book.**

The actual treatment depends on the supplies, contract and applicable classification. GST guidance distinguishes composite supplies from mixed supplies. The workbook therefore includes a cautious 18% case and a separate zero-output-tax sensitivity—not a recommendation to claim exemption.

Obtain written advice before finalizing prices and invoices.

##### 10.2 Scenario assumptions

All scenarios use the same cautious output-tax assumption.

| Assumption | Conservative | Base | Optimistic |
|---|---:|---:|---:|
| Average DTC realization/book | ₹429 | ₹479 | ₹499 |
| DTC books/order | 1.2 | 1.5 | 1.8 |
| Incremental DTC CAC/customer | ₹220 | ₹120 | ₹70 |
| DTC courier/order | ₹85 | ₹65 | ₹55 |
| Combined trade discount from MRP | 45% | 40% | 35% |
| Inventory sell-through | 75% | 90% | 97% |
| Landed print cost: 500-sale project | ₹190 | ₹160 | ₹135 |
| Landed print cost: 5,000-sale project | ₹125 | ₹105 | ₹88 |
| Landed print cost: 50,000-sale project | ₹95 | ₹78 | ₹65 |

The print costs must be achieved at the actual **per-SKU phased batch sizes**. They are not confirmed quotes.

Base channel mix is **45% DTC, 20% institutional, 25% trade, 10% marketplace**.

##### 10.3 Base economics at 5,000 retained book sales

“Retained” means paid sales remaining after refunds/returns. It does not mean copies merely dispatched to a distributor.

| Per retained book | Base model |
|---|---:|
| Weighted publisher realization including modeled GST | ₹430.15 |
| Publisher revenue excluding modeled GST | **₹364.53** |
| Printed-copy cost | ₹105.00 |
| Unsold-edition write-off allocation | ₹11.68 |
| Full-entitlement streaming reserve | ₹29.74 |
| Support/servicing reserve | ₹8.00 |
| Weighted shipping, packaging, payment/channel fees and claims | ₹53.49 |
| Incremental acquisition/marketplace advertising | ₹38.50 |
| **Contribution after variable costs** | **₹118.13** |
| **Contribution margin on net publisher revenue** | **32.4%** |

At 90% sell-through, 5,000 retained sales require approximately **5,556 printed copies**. The model fully expenses unsold edition stock rather than assuming it will eventually sell.

The streaming reserve covers the modeled usage over the access obligation—not just the first month. Fixed video storage and tooling are separately budgeted.

##### 10.4 Channel contribution matters more than headline discounts

At the same base 5,000-copy cost tier:

| Channel | Contribution per retained book |
|---|---:|
| DTC, after modeled CAC | **₹98.88** |
| Institutional/bulk | **₹175.53** |
| Trade/bookstores | **₹104.74** |
| Marketplace, after modeled advertising | **₹123.47** |

These are model outputs, not channel guarantees. Institutional economics are attractive partly because consolidated delivery and lower acquisition friction can offset the discount.

**Do not stack a full retailer/distributor discount, a teacher commission, a referral payout, and paid-ad acquisition on the same order without recalculating contribution.**



### D.2 Nine scenarios, break-even, CAC limits, working capital (message 06 section 11)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 621-693 (section 11, Revenue, profit, break-even, and cash flow). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 11. Revenue, profit, break-even, and cash flow

##### 11.1 Nine scenarios

All money columns below are in **₹ lakh**. Revenue excludes modeled output GST. Profit is before financing and income tax, after the specified variable and fixed costs.

| Retained books | Scenario | Net publisher revenue | Contribution/book | Fixed costs | Operating profit/loss |
|---:|---|---:|---:|---:|---:|
| 500 | Conservative | 1.60 | −₹98.50 | 7.50 | **−7.99** |
| 500 | Base | 1.82 | ₹56.89 | 6.50 | **−6.22** |
| 500 | Optimistic | 1.98 | ₹150.55 | 6.00 | **−5.25** |
| 5,000 | Conservative | 16.04 | −₹11.71 | 15.00 | **−15.59** |
| 5,000 | Base | 18.23 | ₹118.13 | 12.00 | **−6.09** |
| 5,000 | Optimistic | 19.78 | ₹199.15 | 10.00 | **−0.04** |
| 50,000 | Conservative | 160.42 | ₹28.30 | 50.00 | **−35.85** |
| 50,000 | Base | 182.27 | ₹148.14 | 40.00 | **34.07** |
| 50,000 | Optimistic | 197.76 | ₹222.86 | 35.00 | **76.43** |

###### Interpretation

**500 sales:** pay for a controlled test and reusable intellectual property, not an expectation of immediate payback.

**5,000 sales:** enough to demonstrate demand, but not automatically enough to fund a broad catalogue and team.

**50,000 sales:** can support attractive economics, but the conservative case shows why scaling a weak offer can destroy capital.

The cases fund different scopes: a two-title pilot, an expanded season, and a larger catalogue. They are not simple multiples of one unchanged operation.

##### 11.2 Break-even

\[
\text{Static break-even copies}
=
\frac{\text{Fixed costs}}{\text{Contribution per retained copy}}
\]

The base 5,000-copy cost structure gives approximately **10,158 copies** to cover ₹12 lakh of fixed costs.

The larger base structure, with ₹40 lakh of fixed costs and ₹148.14 contribution, gives approximately **27,001 copies**.

These are **static cost-tier calculations**. Requote printing, staffing and distribution when crossing a scale threshold; do not present either as a guaranteed real-world break-even point.

##### 11.3 CAC limits

At the base DTC economics, maintaining **₹100 contribution per book** permits approximately **₹118 CAC per customer/order** at a 1.5-book basket.

That is why I would initially require paid/referral CAC to settle around **₹100–₹120 or lower**, subject to actual costs.

The workbook also allocates fixed social/creative production to DTC. On that basis, the base 5,000-copy **fully loaded marketing CAC is approximately ₹187/customer**, not ₹120.

The fixed creative cost is already in operating profit; do not deduct that fuller KPI a second time.

##### 11.4 Working capital

The cash model uses phased print orders, 50% printer advances, delayed trade collections, tax reserves, and full digital-service usage reserves.

| Base project | Modeled funding requirement, including 15% headroom |
|---|---:|
| 500 retained sales | **₹7.15 lakh** |
| 5,000 retained sales | **₹12.71 lakh** |
| 50,000 retained sales | **₹52.09 lakh** |

Profitability does not eliminate cash needs. Printing and content are paid before many sales; trade payments can arrive after stock has moved.

Use preorder/bulk advances where appropriate, short initial trade-credit limits, SKU-level reprints, and strict receivable follow-up. Do not print 50,000 copies upfront to obtain a lower unit price.

##### 11.5 Costs that must not disappear into “AI automation”

The pilot budget assumes a lean, reusable 2D production workflow—not a complete bespoke platform with every custom Skill discussed earlier.

A separate **₹10 lakh engineering project**, for example, would reduce the base 50,000-sale profit from approximately ₹34.07 lakh to ₹24.07 lakh before other effects. Budget such work explicitly.

The model also assumes commissioned content with agreed paid-up rights. Royalties, third-party licences, additional staff, borrowing costs, and any obligations not included in those contracts must be added.



### D.3 The 90-day pilot budget and weekly gates (message 06 section 14)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 790-831 (section 14, Ninety-day launch roadmap and budget). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 14. Ninety-day launch roadmap and budget

Starting on the research date, a 90-day window reaches approximately **11 January 2027**. That makes a broad rushed catalogue particularly risky. The roadmap below does not assume an unverified 2027 exam timetable.

##### Budget for the two-title pilot

| Fixed project allocation | Budget |
|---|---:|
| Manuscripts and independent academic review | ₹1,60,000 |
| Editing, pagination, design and proofs | ₹60,000 |
| Reviewed chapter videos | ₹1,20,000 |
| Reels, free-content packaging and community work | ₹50,000 |
| Commerce and activation development | ₹60,000 |
| Fixed hosting, tools and storage | ₹15,000 |
| Allocated founder/operational workload | ₹1,15,000 |
| Legal, tax, accounts and rights administration | ₹25,000 |
| Partner specimens, visits and travel | ₹30,000 |
| QA/project contingency | ₹15,000 |
| **Fixed pilot budget** | **₹6,50,000** |

Printing and other variable costs are additional, with sales receipts incorporated in the cash model. The labor allocation is for a defined project workload—not an unlimited full-time team.

**Suggested available capital ceiling: ₹8 lakh**, released in stages. Begin with only **₹60,000 for discovery and prototypes**.

##### Week-by-week execution

| Week | Priority | Gate |
|---|---|---|
| 1 | Interview students, parents, teachers and shops; collect competing books | Confirm real pain points and medium |
| 2 | Test two lessons, sample pages and price cards; obtain three print quotes | Do not confuse survey enthusiasm with demand |
| 3 | Lock two titles, syllabus map and content extent | Academic team can complete the promised product |
| 4 | Establish reusable visuals; begin four or five Reels/week | Measure qualified visits and attempts |
| 5 | Build checkout, accounts, redemption and refund flow | Payment and entitlement tests pass |
| 6 | Complete six free chapters; test low-cost phones and partner specimens | Usability and academic review pass |
| 7 | Review print proofs and full solutions; finalize access/tax terms | Credible delivery commitments |
| 8 | Complete the paid catalogue promised at launch | No undisclosed major missing chapters |
| 9 | Authorize first short print batch; test urban/rural dispatch | Actual weight, price and delivery evidence |
| 10 | Fulfill pilot purchases and repair activation friction | No unresolved critical content/access issue |
| 11 | Test referrals and digital-only versus bundle paths | Positive contribution by acquisition cohort |
| 12 | Reconcile sales, returns, stock and receivables | Reprint justified by actual demand |
| 13 | Decide to continue, change the offer, or stop | Expansion follows evidence—not sunk costs |



### D.4 Offers, specification, printing and channel plan behind the numbers (message 06 sections 2.1, 4.1, 4.3, 8.4, 15.1)


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 99-114 (section 2.1, Launch offers). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 2.1 Launch offers

These are **proposed price tests**, not existing ExamLeaf prices.

| Offer | Proposed price | What it contains | Recommendation |
|---|---:|---|---|
| Free learning | ₹0 | Three complete chapter lessons, diagnostic questions, one sample paper and solutions | No registration required to begin watching |
| Digital-only subject edition | **₹299** | Remaining chapter lessons, selected practice resources, progress/checkpoint features where lawfully implemented | Offer alongside the book |
| One subject book + digital access | **₹499** | Printed revision/practice book, complete printed solutions, corresponding digital package | Main product |
| Two-book Class 10 bundle | **₹949** | General Science + General Mathematics, both digital packages | Preferred DTC basket |
| Institutional/bulk purchase | Negotiated | Same legitimate product, bulk delivery and defined support | Discount according to order economics |
| Monthly subscription | Not initially | Would require an ongoing service proposition | Postpone |

A proposed MRP of **₹549** can be tested, but do not present it as a previously charged price unless that is true. Avoid permanent fake “today only” promotions.

The financial base case uses **₹479 average DTC realization per book**, allowing for the actual mix of bundles and coupons. It does not assume every copy sells for ₹499.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 209-229 (section 4.1, A workable first specification). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 4.1 A workable first specification

Start by quoting a **256-page, approximately 7 × 10-inch book**, with a predominantly black-and-white interior, readable diagrams, suitable writing space, durable binding, and a restrained colour cover.

This is a prototype specification, not a final requirement for every subject.

| Section | Illustrative page allocation |
|---|---:|
| How to use the system, syllabus map, diagnostic | 16 |
| Quick revision notes, formulas, conditions, diagrams | 56 |
| Topic practice and common errors | 24 |
| Eight full sample papers | 64 |
| Detailed solutions | 80 |
| Trackers, answer checklists, revision plan | 16 |
| **Total** | **256** |

Actual pagination must determine whether that allocation is educationally adequate.

**Do not promise 30 fully solved papers, extensive revision notes, and spacious solutions inside this extent without testing the manuscript.** More papers are not automatically more useful than fewer, better-explained papers.

For longer Mathematics or derivation-heavy Class 12 titles, increase the extent and reprice rather than compressing the text.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 253-259 (section 4.3, Printing decisions that protect margin). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 4.3 Printing decisions that protect margin

Obtain three written quotations for the **same specification**, including cover, binding, scratch-code insertion, tax, freight, spoilage tolerance, replacement terms, and payment schedule.

Public short-run printing rates can be considerably higher than an attractive bulk offset assumption; one checked printer separately prices printing and binding. That is why the model’s ₹105 or ₹78 costs must not be treated as obtained quotations.

Quote **per title, language, and batch**. Fifty thousand aggregate sales split across numerous SKUs do not give every SKU the economics of a 50,000-copy run.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 476-488 (section 8.4, The 5,000-book base-channel plan). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 8.4 The 5,000-book base-channel plan

| Channel | Retained books | Illustrative requirement |
|---|---:|---|
| DTC | 2,250 | 1,500 customers at 1.5 books/order |
| Institutional/bulk | 1,000 | 20 partners selling/distributing 50 copies each |
| Trade/bookstores | 1,250 | 25 outlets selling 50 copies each |
| Marketplace | 500 | Actual fulfilled, retained sales |
| **Total** | **5,000** | Not a commitment already secured |

At a 5% qualified-free-learner-to-order rate, the DTC portion requires **30,000 qualified learners**. At 3%, it requires 50,000; at 8%, 18,750.

This is why teacher, search, school, and retail distribution should complement social media from the beginning.


> *Verbatim extract: `00_source/chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md`, lines 838-853 (section 15.1, Proposed operating targets). ChatGPT's inline citation markers are removed; headings are demoted one level group so they nest in this file; the wording, numbers and tables are unchanged.*

#### 15.1 Proposed operating targets

These are **management targets to test**, not industry benchmarks.

| Metric | Initial target or rule |
|---|---|
| Qualified free learner → paid order | Test a **3–8%** range |
| Incremental DTC CAC | Approximately **₹100–₹120 or below** at confirmed base economics |
| Valid first-attempt activation | **At least 97%** |
| DTC activation by day seven | Test **60–75% of delivered eligible books** |
| Inventory sell-through | Plan around **90%**, stress at 75% |
| Academic release defects | **Zero unresolved critical errors** |
| Stock decisions | By SKU and lead time, not aggregate follower count |
| Learning success | Independent and delayed performance—not video completion alone |

For bookstore sales, activation divided by copies shipped to the retailer is not a valid student-activation rate. First establish retailer sell-through.



### D.5 Workbook-only detail

**D.5.1 Dashboard: the nine cases including peak funding gap, +15% funding and static break-even** (message 06 quotes only the profit table and three funding figures; this is the full set. Rs lakh unless stated.)


| Case | Books | Net revenue | Contribution Rs/book | Fixed | Profit | Margin (ratio) | Peak cash gap | Funding +15% | Static break-even (copies) |
|---|---|---|---|---|---|---|---|---|---|
| Conservative \| 500 | 500 | 1.6 | -98.5 | 7.5 | -7.99 | -4.9822 | 7.99 | 9.19 | No unit break-even |
| Base \| 500 | 500 | 1.82 | 56.89 | 6.5 | -6.22 | -3.4101 | 6.22 | 7.15 | 11,426 |
| Optimistic \| 500 | 500 | 1.98 | 150.55 | 6 | -5.25 | -2.6533 | 5.25 | 6.03 | 3,986 |
| Conservative \| 5,000 | 5,000 | 16.04 | -11.71 | 15 | -15.59 | -0.9715 | 17.96 | 20.65 | No unit break-even |
| Base \| 5,000 | 5,000 | 18.23 | 118.13 | 12 | -6.09 | -0.3343 | 11.06 | 12.71 | 10,158 |
| Optimistic \| 5,000 | 5,000 | 19.78 | 199.15 | 10 | -0.04 | -0.0022 | 8.43 | 9.69 | 5,022 |
| Conservative \| 50,000 | 50,000 | 160.42 | 28.3 | 50 | -35.85 | -0.2235 | 83.06 | 95.52 | 176,701 |
| Base \| 50,000 | 50,000 | 182.27 | 148.14 | 40 | 34.07 | 0.1869 | 45.29 | 52.09 | 27,001 |
| Optimistic \| 50,000 | 50,000 | 197.76 | 222.86 | 35 | 76.43 | 0.3865 | 34.4 | 39.56 | 15,705 |


Profit if output GST were 0% (Season P&L column M, INR): Conservative 500 -7,70,372; Base 500 -5,88,746; Optimistic 500 -4,89,126; Conservative 5,000 -12,69,799; Base 5,000 -2,81,245; **Optimistic 5,000 +3,51,698**; Conservative 50,000 -6,97,606; Base 50,000 +66,87,983; Optimistic 50,000 +1,12,02,828. (A sensitivity only; "not a recommendation to claim exemption".)

**D.5.2 Per-retained-book unit economics for all nine cases** (INR; full table with formulas in `COST_MODELS_EXPLAINED.md`, sheet 4.5):


| Line | Conservative \| 500 | Base \| 500 | Optimistic \| 500 | Conservative \| 5,000 | Base \| 5,000 | Optimistic \| 5,000 | Conservative \| 50,000 | Base \| 50,000 | Optimistic \| 50,000 |
|---|---|---|---|---|---|---|---|---|---|
| Total copies printed | 667 | 556 | 516 | 6,667 | 5,556 | 5,155 | 66,667 | 55,556 | 51,547 |
| Weighted publisher realization, gross | 378.59 | 430.15 | 466.72 | 378.59 | 430.15 | 466.72 | 378.59 | 430.15 | 466.72 |
| Publisher revenue excluding GST | 320.84 | 364.53 | 395.52 | 320.84 | 364.53 | 395.52 | 320.84 | 364.53 | 395.52 |
| Total print burden / retained copy | 253.46 | 177.92 | 139.32 | 166.68 | 116.68 | 90.73 | 126.67 | 86.67 | 67.01 |
| Full entitlement streaming reserve | 21.24 | 29.74 | 33.98 | 21.24 | 29.74 | 33.98 | 21.24 | 29.74 | 33.98 |
| Support / servicing | 12 | 8 | 6 | 12 | 8 | 6 | 12 | 8 | 6 |
| Weighted fulfillment / channel servicing | 70.89 | 53.49 | 41.58 | 70.89 | 53.49 | 41.58 | 70.89 | 53.49 | 41.58 |
| Total incremental acquisition | 61.75 | 38.5 | 24.08 | 61.75 | 38.5 | 24.08 | 61.75 | 38.5 | 24.08 |
| Total non-print variable cost | 165.88 | 129.72 | 105.65 | 165.88 | 129.72 | 105.65 | 165.88 | 129.72 | 105.65 |
| Contribution before acquisition | -36.75 | 95.39 | 174.64 | 50.04 | 156.63 | 223.23 | 90.05 | 186.64 | 246.95 |
| Contribution after acquisition | -98.5 | 56.89 | 150.55 | -11.71 | 118.13 | 199.15 | 28.3 | 148.14 | 222.86 |
| Contribution margin | -0.31 | 0.16 | 0.38 | -0.04 | 0.32 | 0.5 | 0.09 | 0.41 | 0.56 |
| Static tier break-even copies | No unit break-even | 11,426 | 3,986 | No unit break-even | 10,158 | 5,022 | 176,701 | 27,001 | 15,705 |
| DTC contribution after CAC | -217.1 | 37.64 | 151.8 | -130.31 | 98.88 | 200.39 | -90.31 | 128.89 | 224.11 |
| Bulk contribution | 10.98 | 114.28 | 178.9 | 97.76 | 175.53 | 227.49 | 137.77 | 205.54 | 251.21 |
| Trade contribution | -60.81 | 43.5 | 110.11 | 25.97 | 104.74 | 158.7 | 65.98 | 134.75 | 182.42 |
| Marketplace contribution | -95.19 | 62.23 | 143.53 | -8.41 | 123.47 | 192.12 | 31.6 | 153.48 | 215.84 |


**D.5.3 DTC price x CAC sensitivity** (Rs contribution per retained book, Base 5,000 cost tier; CAC is per customer/order, contribution per book):


| Realized price \ CAC | 50 | 100 | 150 | 200 | 250 |
|---|---|---|---|---|---|
| 349 | 38.45 | 5.11 | -28.22 | -61.55 | -94.89 |
| 399 | 79.64 | 46.31 | 12.97 | -20.36 | -53.69 |
| 449 | 120.83 | 87.5 | 54.17 | 20.83 | -12.5 |
| 479 | 145.55 | 112.22 | 78.88 | 45.55 | 12.22 |
| 499 | 162.03 | 128.69 | 95.36 | 62.03 | 28.69 |
| 549 | 203.22 | 169.89 | 136.55 | 103.22 | 69.89 |


Maximum DTC CAC at a Rs 100/book contribution target and 1.5-book basket: **Rs 118.32** per customer/order (Base DTC contribution before acquisition Rs 178.88 per book). Fully loaded marketing CAC (Base 5,000): **Rs 120 + Rs 1,00,000 / 1,500 customers = Rs 186.67** ("Do NOT deduct this fully loaded KPI again in profit").

**D.5.4 Fixed project / season budgets** (Rs; `90-Day Budget`; the Base-case fixed spend in the nine scenarios):


| Category | 500-book pilot | 5,000-book season | 50,000-book season | Scope / assumption |
|---|---|---|---|---|
| Manuscripts + independent academic review | 160,000 | 250,000 | 600,000 | Contract authoring and subject review; source rights required. |
| Editing, pagination, cover and print proofs | 60,000 | 100,000 | 250,000 | Do not replace quality checks with generated layouts. |
| Reviewed chapter videos | 120,000 | 200,000 | 450,000 | Pilot: 40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates. |
| Reels, free-content packaging, community | 50,000 | 100,000 | 350,000 | Fixed organic acquisition cost; excluded from incremental CAC but included in profit. |
| Commerce / activation development | 60,000 | 100,000 | 250,000 | Lean existing-commerce stack; no custom native app. |
| Fixed hosting, tools, storage | 15,000 | 40,000 | 120,000 | Video delivery is separately reserved per activated book. |
| Allocated founder / operational staff time | 115,000 | 260,000 | 1,450,000 | Allocated project/season workload, not a promise of unlimited full-time staffing. |
| Legal, tax, accounts and rights administration | 25,000 | 50,000 | 130,000 | GST classification and minors/privacy review are launch gates. |
| Partner launch visits, specimens, travel | 30,000 | 70,000 | 300,000 | Fixed launch work; per-sale field servicing also separately modeled. |
| QA and project contingency | 15,000 | 30,000 | 100,000 | Expected spending allowance; funding headroom is additional liquidity, not P&L expense. |
| Total fixed budget | 650,000 | 1,200,000 | 4,000,000 |  |


**D.5.5 Funnel illustration and channel plan.** 1,000,000 unique accounts reached x 20% matching x 2% visit x 50% qualified x 5% paid-order = **100 paid DTC customers / 150 books**. 5,000-book base channel plan: DTC 2,250 books (1,500 customers at 1.5 books), institutional/bulk 1,000 (20 partners x 50), trade 1,250 (25 outlets x 50), marketplace 500. Qualified learners needed for the DTC plan: **50,000 at 3%, 30,000 at 5%, 18,750 at 8%**.

**D.5.6 Optional digital-only subject (Rs 299; not in any book scenario):** revenue excl. GST Rs 253.39; gateway Rs 7.06; full-edition delivery reserve Rs 42.48; support/refund Rs 12; acquisition Rs 80; **contribution before fixed creation costs Rs 111.85 (44.1%)**.

**D.5.7 Cash flow shape (monthly blocks, `Cash Flow`).** Minimum cumulative cash (the "peak gap") and month reached: Conservative 500 -7.99 (m12); Base 500 -6.22 (m12); Optimistic 500 -5.25 (m12); Conservative 5,000 -17.96 (m5); Base 5,000 -11.06 (m4); Optimistic 5,000 -8.43 (m3); Conservative 50,000 -83.06 (m4); Base 50,000 -45.29 (m3); Optimistic 50,000 -34.40 (m2). Full 12-month tables for the Base 5,000 case: `COST_MODELS_EXPLAINED.md` sheet 4.7.

**D.5.8 `model_assumptions_and_results.json`.** Python-side mirror; its nine `results[]` records give, e.g., Base 5,000: `contrib` 118.1349, `profit` -609,325.41, `break_even` 10,158, `peak` 1,105,535.66, `funding` 1,271,366.01 (INR), identical to the Dashboard. File: `model_assumptions_and_results.json` in this section.

---


## Part E. Reconciliation: how the four models relate

> **Authorship note.** Parts A-D reproduce what ChatGPT published. Part E is the **organizing team's own reconciliation**, computed only from numbers in the workbooks and messages (formulas shown). ChatGPT did **not** publish a combined engine + narration + business total; the brackets below are arithmetic aids, not model outputs, and carry the same "planning estimate, not a quote" status as their inputs.

### E.1 What each model prices, and where they touch

| | v1 engine | v2 engine | Narration | Business |
|---|---|---|---|---|
| Question answered | What does one 10-min video cost with reusable components? | What does it cost under three architectures, incl. generated video, and how many reviewers? | What does the narration sub-system cost under five voice methods? | Does the book-linked business make money at 500 / 5,000 / 50,000 retained copies, and how much cash is needed? |
| Unit | per finished video; 1 / 100 / 1,000 | per finished video; 1 / 100 / 1,000 | per finished video; 1 / 100 / 1,000 | per retained book; 500 / 5,000 / 50,000 |
| Currency / tax | USD, pre-tax | USD, pre-tax | USD, pre-tax | INR; 18% GST modeled |
| Headline variable cost | $20.37 / video ($2.37 machine + $18 human) | $158.98 AI-heavy / **$34.34 hybrid** / $37.32 self-hosted | $12.50 / video premium TTS (range $12.50-$42.40) | Contribution Rs 118.13 / book (Base 5,000) |
| Monthly fixed | $200 | $250 / $300 / $900 | $100-$300 | Rs 6.5 lakh / 12 lakh / 40 lakh per season (Base) |
| One-time set-up | $8,000 | $5,000 / $10,000 / $16,000 | $4,000 | inside fixed budgets; **no engine R&D included** |
| Human labour | 60 min/video (45 academic + 15 QA) | 150 / 85 / 110 min/video | 35-100 min/video (audio review, editing, recording) | allocated staff time in the 90-Day Budget |
| Viewer delivery (streaming) | excluded | excluded | excluded ("audience streaming") | **included**: Rs 21-34 per retained book (400 minutes, $1/1,000 min) |

**The seams.** (1) The three USD models describe production of the *same* video, so they overlap heavily (E.2). (2) The business workbook has exactly one place where video production enters: `90-Day Budget` row 6 "Reviewed chapter videos" (E.4). (3) Nothing links the workbooks by formula; every connection below is a human judgment.

### E.2 Overlapping lines between v1 engine, v2 hybrid engine and narration (USD per video)

| Line | v1 engine | v2 hybrid | Narration (premium TTS) | Comment |
|---|---:|---:|---:|---|
| TTS synthesis | 0.768 (8,000 chars x 1.2 x $0.08/1k) | 0.96 (8,000 x 1.2 x $0.10/1k) | 0.936 (7,800 x 1.2 x $0.10/1k) | **Same item, three values**: tariff $0.08 vs $0.10; 8,000 vs 7,800 characters. Use one |
| LLM / script work | 1.034 (Haiku+Sonnet+Sol+Opus, +30%) | 1.716 (Sonnet+Opus+Haiku, +30%) | 0.60 (narration editing/direction allowance) | Narration's $0.60 is "incremental narration editing/direction only"; the engine's LLM line already includes writing the script. Partial overlap |
| ASR / alignment / audio QA (machine) | 0.03 | 0.10 | 0.08 | Overlap: all three price automatic checking of the audio |
| Storage | 0.03 (+0.15 API reserve) | 0.20 | 0.05 | Overlap |
| Rendering / encoding | 0.3555 | 0.50 | not priced | Engine only |
| Generated clips / stills | not priced | 4.00 + 0.20 (hybrid) | not priced | v2 only; default can be zero |
| Academic review | 15.00 (45 min @ $20) | 15.00 (45 min @ $20) | 8.33 (25 min @ $20, "academic audio review") | **Labour overlap**: engine review covers "the entire final lesson", which includes listening to the narration. Do not add the narration's 25 minutes on top without deciding how many of the engine's 45 minutes are audio |
| Production QA | 3.00 (15 min @ $12) | 5.00 (20 min @ $15) | 2.50 (10 min editing @ $15) | **Labour overlap**: QA includes "audio, captions, continuity"; different hourly rates ($12 vs $15) |
| Repairs / editing | not priced | 6.67 (20 min @ $20) | included in the 10 min editing | v2 only; overlaps narration editing |
| **Variable total** | **20.37** | **34.34** | **12.50** | |
| Monthly fixed | 200 | 300 | 100 | Both cover tools/storage/orchestration; choose one, or justify both |
| One-time set-up | 8,000 | 10,000 | 4,000 | v1 includes 20 design/voice hours; narration $4,000 is a separate "narration-subsystem" reserve |

Both ChatGPT documents say the same thing: narration Summary sheet, *"Do not add these audio-review costs twice if already included in your full video-production budget."*; message 12 section 13.1, *"Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget."* ChatGPT gave no recipe; the recipe is in `INSTRUCTIONS_how_to_use_cost_models.md` section 4.

### E.3 Bracketing the combined cost (arithmetic aid, USD per video, variable only)

Method: start from the whole-video engine model, **remove the engine's audio lines**, then add the narration workbook's premium-TTS figure either as machine-only (assumes the narration human minutes are fully inside the engine's human minutes) or in full (assumes none are).

| Combination | Floor: narration human time already inside engine review | Ceiling: narration human time additional | Naive sum (double counts) |
|---|---:|---:|---:|
| v2 hybrid + premium-TTS narration | 34.95 = 34.34 - 0.96 (TTS) - 0.10 (alignment/audio) + 1.666 (narration machine) | 45.78 = same, + 12.499 (narration machine + human) | 46.84 = 34.34 + 12.50 |
| v1 engine + premium-TTS narration | 21.27 = 20.37 - 0.768 (TTS) + 1.666 | 32.10 = 20.37 - 0.768 + 12.499 | 32.87 = 20.37 + 12.50 |


So for the recommended hybrid architecture the whole-video variable cost lies in a **$34.95 to $45.78 per video** bracket (the naive sum, $46.84, overstates by the engine's own TTS and audio lines). At 1,000 videos in one month: floor $35,249 and ceiling $46,082 with a single $300 fixed allowance (+$10,000 engine set-up, and +$4,000 narration reserve if its scope is not already in the engine set-up). These brackets need a pilot with timed review minutes to narrow.

### E.4 Engine to business seam (USD to INR; no double counting with the book P&L)

* **The one numeric link.** `90-Day Budget` row 6 prices "Reviewed chapter videos" at **Rs 3,000 per video** ("Pilot: 40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates") = Rs 1,20,000 for the pilot. At the planning rate of Rs 90/USD that is **$33.33 per video**. For comparison at the same rate: v1 variable $20.37 = Rs 1,833; v2 hybrid $34.34 = Rs 3,091; v2 AI-heavy $158.98 = Rs 14,308; v2 self-hosted $37.32 = Rs 3,358; combined hybrid + narration bracket $34.95-$45.78 = Rs 3,145-Rs 4,120. *(15 Oct 2026: under RD-41 read this line as an **opportunity cost**, not cash; cash part ≈ Rs 745 per video; see E.8.)* **The workbook does not say how Rs 3,000 was derived**; it sits between v1 and v2-hybrid but below the upper end of the combined bracket. Treat it as a placeholder to be tested in the pilot, and re-cost it from the engine workbooks once review minutes are measured. Implied video counts if Rs 3,000 held: 40 (pilot), about 67 (Rs 2,00,000 season) and 150 (Rs 4,50,000 season): derived by division, not stated in the workbook.
* **What the business model already contains (do not add again from the engine side):** video delivery/streaming (Rs 21.24-33.98 per retained book: 400 delivered minutes x $1 per 1,000 minutes x Rs 90 x 1.18 x activation rate); "Fixed hosting, tools, storage" (Rs 15,000 / 40,000 / 1,20,000); "Reels, free-content packaging, community" (Rs 50,000 / 1,00,000 / 3,50,000; the engine's optional three-Short package is $4.316 = Rs 388 per lesson, so the Short production cost in the engine model and the Reels line overlap in subject matter: count Shorts once); commerce/activation development.
* **What the business model does NOT contain.** The engine set-up budgets ($5,000-$16,000; $8,000 in v1) and the narration reserve ($4,000): at Rs 90/USD, v1 $8,000 = Rs 7.2 lakh; v2 hybrid $10,000 = Rs 9.0 lakh; narration $4,000 = Rs 3.6 lakh; hybrid + narration = Rs 12.6 lakh; AI-heavy $5,000 = Rs 4.5 lakh; self-hosted $16,000 = Rs 14.4 lakh. Message 06 section 11.5: *"A separate **₹10 lakh engineering project**, for example, would reduce the base 50,000-sale profit from approximately ₹34.07 lakh to ₹24.07 lakh before other effects. Budget such work explicitly."* The Execution Runbook in the toolkit says: *"A full bespoke video platform or 40-Skill engineering project is NOT quietly included in the lean launch: the MVP uses reusable standard 2D tools. Any separate R&D programme needs its own budget and reduces profit."* Any such R&D is an extra deduction from every scenario's profit and adds to the funding need.
* **Scale mismatch to keep in mind.** The engine models 1,000 videos a month; the business pilot budget funds about 40 videos in a 90-day window. Do not apply engine volume economics (e.g. $20.57/video average at 1,000) to the pilot, where fixed costs and set-up dominate (v1: $8,220 for the first video; v2 hybrid: $10,334).

### E.5 Currency, tax and timing assumptions (one place)

| Item | Where | Value | Status |
|---|---|---|---|
| Currency of engine + narration models | all three USD workbooks | USD, **before tax**; "no live currency conversion assumed" (v1 ReadMe) | not a quote |
| Planning FX | business `Global Inputs!B8` | **Rs 90 per USD** | "Budget buffer, NOT a current FX quote." Used only for the Cloudflare streaming reserve in the business model; use it for the engine-to-business conversion above for consistency |
| Output GST | business `Global Inputs!B5` | **18% on the entire marketed bundle** (all nine cases) | "Prudent 18% stress/base tax input, NOT legal classification"; "NOT a classification opinion. Obtain written advice." A zero-output-tax sensitivity is shown (Season P&L column M) |
| GST on gateway fee | `Global Inputs!B6:B7` | 2% fee + 18% GST on the fee, no input credit | verified standard Razorpay pricing; promotional period excluded |
| Non-recovered tax on hosting | `Global Inputs!B11` | 18% | planning allowance; "actual invoice/credit treatment to be checked" |
| Tax in the engine / narration models | all USD workbooks | none | any tax on imported digital services, TDS, or input credit on API/SaaS bills is **not modeled**; budget it separately with a CA |
| Income tax, financing | business | none | "No financing cost or income tax." |
| Research / verification date | every workbook and message | **13 October 2026** | prices will drift; see lifecycle list below |
| Accounting period | engine + narration | one month for 1 / 100 / 1,000 videos | fixed cost not multiplied per video |
| Accounting period | business | one edition / operating season (not 90 days) | 90-day pilot has its own budget |

### E.6 Time-limited facts that change the numbers (all dated 13 October 2026)

* Gemini 3.8 Flash TTS: $0.50 / $9 per million tokens through 31 Dec 2026; **$1 / $18 from 1 Jan 2027** (synthesis $0.1392 now, $0.2784 scheduled per lesson).
* OpenAI old TTS models (`tts-1`, `tts-1-hd`, listed `gpt-4o-mini-tts` snapshots): **shutdown 6 Jan 2027** (notice 1 Oct 2026); replacement `gpt-realtime-2.1-mini` ($0.60 / M text in, $20 / M audio out) not a proven drop-in.
* ElevenLabs: $0.10 / 1,000 characters is the v2/v3 reference; **Eleven v4 has no verified price** ("TBD"). Message 02 noted a promotion on the checked page "ending 12 October" which was **excluded** from the model, so real invoices might be lower. v1 uses $0.08 (Multilingual v2 standard), v2 and narration use $0.10.
* Cartesia: 1,000 lessons need 9.36 million credits, above the 8-million Scale plan: a higher-tier/overage quote is required; message 12 labels its recipe Sonic 3.5 snapshot, not 3.6.
* Claude / OpenAI model names and prices: v1 uses labels "Haiku 5.5 / Sonnet 5.5 / Opus 5.5" and `gpt-6.1-sol` at $0.10-$0.50, $2-$10, $4-$20, $2-$10; v2 uses "Haiku 4.5 / Sonnet 4.6 / Opus 4.6" at $1/$5, $3/$15, $5/$25. They are different price lists for different labels, both "as of 13 October 2026". The LLM line moves from $1.03 (v1) to $1.72 (v2). Re-check current model names, availability and tariffs on the provider pricing pages before using any LLM figure.
* Remotion billing definition (20 billable renders per video) unconfirmed; Fargate rates are **US East examples, not Mumbai**; render time (45 min) and all GPU figures are unbenchmarked; Sarvam Bulbul v3 quoted at Rs 30 per 10,000 characters (message 02), and its Assamese support is unconfirmed.
* Printing, courier, CAC, sell-through, conversion: "planning assumptions requiring validation"; print costs "must be achieved at the actual per-SKU phased batch sizes. They are not confirmed quotes."

### E.7 Reading the four models together: a one-paragraph synthesis

*(15 Oct 2026: true of the workbooks' cash model; under RD-41 review cash is $0 and the sentence reads "review minutes, not AI, are the throughput constraint"; see E.8.)* Human review, not AI, is the cost driver in every engine model (88% of v1 variable cost; 78% of v2 hybrid; 583 hours at 1,000 videos for premium narration alone), so the useful decisions are about reviewer minutes and quality gates. Narration synthesis is about $1 per video and is not worth optimising before pronunciation/sync repair time is controlled. On the business side, 500 and 5,000 retained books do not recover season costs in the Base case, 50,000 does only with Base-or-better unit economics (Conservative loses Rs 35.85 lakh), and every scenario needs Rs 6-95 lakh of working capital, so the engine's set-up money (Rs 3.6-14.4 lakh) is material relative to the Rs 8 lakh suggested pilot ceiling. None of this has been validated by a pilot; every number is a planning estimate.

### E.8 Addendum (15 Oct 2026): review cash is $0 (RD-41)

**Decision (founder, 15 Oct 2026; RD-41 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`, first recorded in `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §7.13):** academic review, production QA and repairs are done in-house at **$0 cash**. Review minutes are kept as a **capacity** metric (v2 hybrid 85 min/lesson ≈ 1,417 h per 1,000 lessons ≈ 8.85 FTE-months; v1 60 min ≈ 1,000 h). Source: `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` finding M6. **The workbooks and every original number above are left unchanged**; this addendum only re-reads them.

**Review-free cash totals (USD, variable per video, pre-tax; arithmetic on the workbook lines, team's own, not a ChatGPT output):**

| Model / combination | Workbook variable | Review-free cash | How |
|---|---:|---:|---|
| v1 engine | $20.37 | **$2.37** | drop `UnitCosts` human review $18.00 |
| v2 AI-heavy / Hybrid / Self-hosted | $158.98 / $34.34 / $37.32 | **$111.48 / $7.68 / $2.32** | `Per Video` machine subtotal only |
| v2 Hybrid, generated clips $0 | $30.34 | **$3.68** | $7.68 − $4.00 clips |
| Narration, premium TTS | $12.50 | **$1.67** | `Methods` machine column (review + editing in-house) |
| Narration, human recorded / human performance + STS / 80% TTS + 20% performed | $42.40 / $34.87 / $17.06 | **$30.73 / $24.45 / $6.22** if the performer is paid at the workbook's $30/h; machine-only $0.73 / $1.95 / $1.72 if the performer is in-house | performer fee is not review, so RD-41 does not zero it |
| v2 Hybrid + premium-TTS narration (Part E.3) | $34.95 floor to $45.78 ceiling | **$8.28** (floor and ceiling collapse; ≈ Rs 745 at Rs 90/USD) | $34.34 − $26.67 human − $0.96 engine TTS − $0.10 engine audio + $1.666 narration machine |
| Same, generated clips $0 | | **$4.28** (≈ Rs 385) | − $4.00 |
| v1 + premium-TTS narration | $21.27 to $32.10 | **$3.27** | $2.37 − $0.768 + $1.666 |

Monthly totals with fixed costs (one month): v1 $202.37 / $436.76 / $2,567.62 at 1 / 100 / 1,000; v2 Hybrid $307.68 / $1,067.60 / $7,976 (clips $0: $3,976 at 1,000); premium narration $101.67 / $266.60 / $1,766; hybrid + narration ≈ $8,582 at 1,000 with a single $300 fixed allowance. Set-up budgets are unchanged. For the strong-to-cheap model scenarios with review free (today $7.68, clips $0 $3.68, lean floor ≈ $2.31 for today's LLM mix) use **13 §7.13**, which is the canonical review-free table.

**What this changes in the readings above.**
- The "88% of v1 / 78% of v2 hybrid" review share and "human review dominates" statements describe the **workbook's cash model** and remain arithmetically correct for it. Under RD-41 the review share of **cash** is 0%; the principle becomes **"review minutes, not AI, are the throughput constraint"**. The dominant cash items become generated clips (v2 hybrid $4.00 of $7.68), the LLM line ($1.72) and narration (≈ $1).
- **Business `90-Day Budget` row 6 ("Reviewed chapter videos", 40 × Rs 3,000 = Rs 1,20,000):** relabel as an **opportunity cost** (allocated founder/team time plus machine cost), not a cash outlay. Under RD-41 the cash part is ≈ 40 × Rs 745 ≈ **Rs 29,800** (hybrid + premium-TTS machine cost; ≈ Rs 15,400 with clips $0); the remaining ≈ Rs 90,200 is in-house review time. The workbook cell B6 is not edited; if you edit it, the pilot's cash need falls by up to that amount and Base-case fixed spend changes with it.
- **TTS price change, 1 Jan 2027:** the Gemini 3.8 Flash TTS line used in the lean floor (≈ $0.14 per lesson) doubles to ≈ $0.28 (Part E.6), so 13 §7.13's lean floor moves from ≈ $0.59 to ≈ $0.73 and its lean-floor ratios fall (audit: ≈ 6.2× vs Opus-only Kit, 12–23× vs bespoke). The lean floor also assumes TTS (Path B); full lessons performed by a teacher plus STS (Path A, `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md`) carry the performer/STS line above.
- **Sheet count:** 34 sheets (6 + 7 + 6 + 15) is correct, as `README.md` already says. The "35 sheets" figure still appears in `00_source/README.md` line 37 (spreadsheets_as_csv row); `00_source/` is read-only, so it is recorded here and not edited (audit factual-and-arithmetic-correctness-12).
