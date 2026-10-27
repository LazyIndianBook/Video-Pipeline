# 08_cost_models: the four ExamLeaf cost workbooks, explained, consolidated and ready to edit

**Project:** ExamLeaf Video Engine, an AI-assisted pipeline for 10-minute STEM revision videos and Reels for Assam Board Class 10-12, with a narration system and a book-linked business model.
**Research / model date:** **13 October 2026**. Every price, tariff, model name and date in this section is as of that day.
**Status of all numbers:** **planning estimates and scenarios, not quotes, not benchmarks, not sales forecasts.** The full list of the "not a quote" caveats, reproduced word for word, is in section 6 below.

## 1. What this section is

ChatGPT produced **four editable Excel cost workbooks** (34 sheets in total; the original brief mentioned 35 sheets and 16 business sheets, the files contain 6 + 7 + 6 + 15 = 34) while researching the project. This section keeps all of them, makes every sheet readable without Excel, reproduces every published cost table next to its assumptions, reconciles the four models, and tells you how to edit and combine them.

| Workbook | What it answers | Currency |
|---|---|---|
| **v1 engine** | What one 10-minute video costs with a reusable-component stack, at 1 / 100 / 1,000 videos | USD, pre-tax |
| **v2 engine** | The same under three architectures (AI-heavy, Hybrid, Mostly self-hosted), plus reviewer capacity, Shorts add-on and the only measured render data | USD, pre-tax |
| **narration** | What the narration sub-system costs under five voice-production methods | USD, pre-tax |
| **business** | Whether the book-linked business makes money at 500 / 5,000 / 50,000 retained copies, how much cash it needs, break-even, CAC limits, the 90-day pilot budget | INR (Rs lakh = 100,000); `Rs` below = rupee |

## 2. Where each workbook came from

All four came out of one ChatGPT research conversation (share `6acf03ec-b480-83ee-a000-3701059934d9`, exported under `00_source/chatgpt_transcript/`). The raw files are in `00_source/downloads/` and were copied here unmodified with `cp`.

| File in `workbooks/` | Original name | Produced in (message file in `00_source/chatgpt_transcript/messages/`) | Delivery pack it belongs to | Sandbox path ChatGPT gave | Raw copy in `00_source/` |
|---|---|---|---|---|---|
| `v1_engine_ExamLeaf_Cost_and_Skills.xlsx` | `ExamLeaf_Cost_and_Skills.xlsx` | `02_ASSISTANT_video_engine_architecture_and_plan_v1.md` (section 13 quotes it) | Video Engine Planning Pack (`ExamLeaf_Video_Engine_Planning_Pack.zip`) | `/mnt/data/ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx` | `downloads/ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx` |
| `v2_engine_ExamLeaf_Video_Engine_Cost_Model.xlsx` | `ExamLeaf_Video_Engine_Cost_Model.xlsx` | `10_ASSISTANT_video_engine_implementation_v2.md` (section 11 quotes it) | Video Engine Implementation (`ExamLeaf_Video_Engine_Implementation.zip`) | `/mnt/data/ExamLeaf_Video_Engine_Cost_Model.xlsx` | `downloads/ExamLeaf_Video_Engine_Cost_Model.xlsx` |
| `narration_ExamLeaf_Narration_Cost_Model.xlsx` | `ExamLeaf_Narration_Cost_Model.xlsx` | `12_ASSISTANT_narration_system.md` (section 13 quotes it) | Narration System (`ExamLeaf_Narration_System.zip`; restated in its `docs/Costs_and_Methods.md`) | `/mnt/data/ExamLeaf_Narration_Cost_Model.xlsx` | `downloads/ExamLeaf_Narration_Cost_Model.xlsx` |
| `business_ExamLeaf_Business_Model.xlsx` | `ExamLeaf_Business_Model.xlsx` | `06_ASSISTANT_business_model_launch_financial_plan.md` (sections 10, 11, 14 quote it) | Business Launch Toolkit (`ExamLeaf_Business_Launch_Toolkit.zip`) | `/mnt/data/ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx` | `downloads/ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx` (byte-identical copy in `extracted/ExamLeaf_Business_Launch_Toolkit/`) |
| `model_assumptions_and_results.json` | `Model_Assumptions_and_Results.json` | `06_...` (toolkit ZIP) | Business Launch Toolkit | inside the ZIP | `extracted/ExamLeaf_Business_Launch_Toolkit/Model_Assumptions_and_Results.json` |
| `csv/` (68 files) | `<workbook>__<sheet>__values.csv` / `__formulas.csv` | exported from the four workbooks | none (derived) | none | `00_source/spreadsheets_as_csv/` |

Each workbook is a ChatGPT-generated file: the cached values were calculated by ChatGPT's tooling and were **not** re-opened in Excel when building this section (the CSVs were read; the formulas were then re-implemented independently and reproduce the stored baselines exactly: v1 $20.3676, v2 hybrid $34.3427, narration premium $12.4993, business Base 5,000 contribution Rs 118.1349 and break-even 10,158).

## 3. Headline numbers (all planning estimates)

| Model | Headline | Where to read more |
|---|---|---|
| **v1 engine** (USD) | **$2.37 machine + $18.00 human = $20.37 per video**; fixed $200/month; set-up $8,000. Total production cost for 1 / 100 / 1,000 videos in a month: **$220.37 / $2,236.76 / $20,567.62** (average $220.37 / $22.37 / $20.57); including set-up $8,220 / $10,237 / $28,568. 1,000 videos = 1,000 reviewer-hours = 6.25 FTE | `CONSOLIDATED` Part A |
| **v2 engine** (USD) | Variable per video: **AI-heavy $158.98, Hybrid $34.34, Mostly self-hosted $37.32**; fixed $250 / $300 / $900 per month; set-up $5,000 / $10,000 / $16,000. Operating total at 1 / 100 / 1,000: AI-heavy $408.98 / $16,147.60 / $159,226; **Hybrid $334.34 / $3,734.27 / $34,642.67**; Self-hosted $937.32 / $4,631.50 / $38,215. Hybrid at 1,000: 85 human minutes per video = 1,417 hours = **8.85 FTE-months**; three-Short package **$4.32** per lesson | Part B |
| **narration** (USD) | Variable per video / 1 / 100 / 1,000 videos: **Premium commercial TTS $12.50 / $112.50 / $1,349.93 / $12,599.33**; Primarily self-hosted $14.75 / $314.75 / $1,775.20 / $15,052; Human recorded $42.40 / $142.40 / $4,339.67 / $42,496.67; Human performance + STS $34.87 / $159.87 / $3,612.07 / $34,995.67; Hybrid 80% TTS $17.06 / $167.06 / $1,855.69 / $17,206.93. Dominant cost: **583 human hours at 1,000 videos** (premium); set-up reserve $4,000 | Part C |
| **business** (Rs lakh) | Profit, Conservative / Base / Optimistic: **500 books -7.99 / -6.22 / -5.25; 5,000 books -15.59 / -6.09 / -0.04; 50,000 books -35.85 / +34.07 / +76.43**. Base contribution Rs 118.13 per book at 5,000; **break-even 10,158 copies (5,000-tier) and 27,001 (50,000-tier)**; max DTC CAC Rs 118 (fully loaded Rs 187); funding incl. 15% headroom (Base) **Rs 7.15 / 12.71 / 52.09 lakh**; pilot fixed budget **Rs 6.5 lakh**, suggested ceiling **Rs 8 lakh**, discovery cap **Rs 60,000** | Part D |
| **Seam** | The only link between the USD and INR models: business `90-Day Budget` row 6, "Reviewed chapter videos", Rs 3,000 per video (= $33.33 at Rs 90/USD). *15 Oct 2026: read as opportunity cost under RD-41, see 3.1* | Part E |

### 3.1 Addendum (15 Oct 2026): review cash is $0 (RD-41)

**Decision (founder, 15 Oct 2026; RD-41 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`, first recorded in `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §7.13):** academic review, production QA and repairs are done in-house at **$0 cash**. Review minutes are kept as a **capacity** metric (v2 hybrid 85 min/lesson ≈ 1,417 h per 1,000 lessons ≈ 8.85 FTE-months; v1 60 min ≈ 1,000 h). Source: `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` finding M6. **The workbooks and every original number above are left unchanged**; this addendum only re-reads them.

**Review-free cash totals (USD, variable per video, pre-tax; arithmetic on the workbook lines, team's own, not a ChatGPT output):**

| Model / combination | Workbook variable | Review-free cash | How |
|---|---:|---:|---|
| v1 engine | $20.37 | **$2.37** | drop `UnitCosts` human review $18.00 |
| v2 AI-heavy / Hybrid / Self-hosted | $158.98 / $34.34 / $37.32 | **$111.48 / $7.68 / $2.32** | `Per Video` machine subtotal only |
| v2 Hybrid, generated clips $0 | $30.34 | **$3.68** | $7.68 − $4.00 clips |
| Narration, premium TTS | $12.50 | **$1.67** | `Methods` machine column (review + editing in-house) |
| Narration, human recorded / human performance + STS / 80% TTS + 20% performed | $42.40 / $34.87 / $17.06 | **$30.73 / $24.45 / $6.22** if the performer is paid at the workbook's $30/h; machine-only $0.73 / $1.95 / $1.72 if the performer is in-house | performer fee is not review, so RD-41 does not zero it |
| v2 Hybrid + premium-TTS narration (`CONSOLIDATED` Part E.3) | $34.95 floor to $45.78 ceiling | **$8.28** (floor and ceiling collapse; ≈ Rs 745 at Rs 90/USD) | $34.34 − $26.67 human − $0.96 engine TTS − $0.10 engine audio + $1.666 narration machine |
| Same, generated clips $0 | | **$4.28** (≈ Rs 385) | − $4.00 |
| v1 + premium-TTS narration | $21.27 to $32.10 | **$3.27** | $2.37 − $0.768 + $1.666 |

Monthly totals with fixed costs (one month): v1 $202.37 / $436.76 / $2,567.62 at 1 / 100 / 1,000; v2 Hybrid $307.68 / $1,067.60 / $7,976 (clips $0: $3,976 at 1,000); premium narration $101.67 / $266.60 / $1,766; hybrid + narration ≈ $8,582 at 1,000 with a single $300 fixed allowance. Set-up budgets are unchanged. For the strong-to-cheap model scenarios with review free (today $7.68, clips $0 $3.68, lean floor ≈ $2.31 for today's LLM mix) use **13 §7.13**, which is the canonical review-free table.

**What this changes in the readings above.**
- The "88% of v1 / 78% of v2 hybrid" review share and "human review dominates" statements describe the **workbook's cash model** and remain arithmetically correct for it. Under RD-41 the review share of **cash** is 0%; the principle becomes **"review minutes, not AI, are the throughput constraint"**. The dominant cash items become generated clips (v2 hybrid $4.00 of $7.68), the LLM line ($1.72) and narration (≈ $1).
- **Business `90-Day Budget` row 6 ("Reviewed chapter videos", 40 × Rs 3,000 = Rs 1,20,000):** relabel as an **opportunity cost** (allocated founder/team time plus machine cost), not a cash outlay. Under RD-41 the cash part is ≈ 40 × Rs 745 ≈ **Rs 29,800** (hybrid + premium-TTS machine cost; ≈ Rs 15,400 with clips $0); the remaining ≈ Rs 90,200 is in-house review time. The workbook cell B6 is not edited; if you edit it, the pilot's cash need falls by up to that amount and Base-case fixed spend changes with it.
- **TTS price change, 1 Jan 2027:** the Gemini 3.8 Flash TTS line used in the lean floor (≈ $0.14 per lesson) doubles to ≈ $0.28 (`CONSOLIDATED_COST_SCENARIOS.md` Part E.6), so 13 §7.13's lean floor moves from ≈ $0.59 to ≈ $0.73 and its lean-floor ratios fall (audit: ≈ 6.2× vs Opus-only Kit, 12–23× vs bespoke). The lean floor also assumes TTS (Path B); full lessons performed by a teacher plus STS (Path A, `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md`) carry the performer/STS line above.
- **Sheet count:** 34 sheets (6 + 7 + 6 + 15) is correct, as this README already says. The "35 sheets" figure still appears in `00_source/README.md` line 37 (spreadsheets_as_csv row); `00_source/` is read-only, so it is recorded here and not edited (audit factual-and-arithmetic-correctness-12).

## 4. Every file placed here

### 4.1 Documents and data at the top level

| File | What it is |
|---|---|
| `README.md` | This file: what the section is, provenance, file list, how to use, caveats, cross-references, gaps |
| `COST_MODELS_EXPLAINED.md` | All 34 sheets, sheet by sheet: contents, editable input cells (with addresses), key outputs with numbers, plain-English formula logic; cell comments extracted from the .xlsx; edit-impact table |
| `CONSOLIDATED_COST_SCENARIOS.md` | Every published cost table reproduced verbatim from messages 02, 10, 12, 06 with assumptions; workbook-only tables; reconciliation (overlaps, currency, GST, dating) |
| `INSTRUCTIONS_how_to_use_cost_models.md` | Which cells to edit first; sensitivities with expected results; combining engine + narration + business without double counting; what needs real quotes; model-lifecycle caveats |
| `model_assumptions_and_results.json` | Copy of `Model_Assumptions_and_Results.json` from the Business Launch Toolkit: the business model's global inputs, 3 scenarios, 9 results |

### 4.2 `workbooks/` (4 Excel files, unmodified copies)


| File | Original name | Size | Sheets |
|---|---|---|---|
| `workbooks/v1_engine_ExamLeaf_Cost_and_Skills.xlsx` | `ExamLeaf_Cost_and_Skills.xlsx` | 22,240 bytes | 6 (Inputs, UnitCosts, Volumes, CustomSkills, ExistingSkills, ReadMe) |
| `workbooks/v2_engine_ExamLeaf_Video_Engine_Cost_Model.xlsx` | `ExamLeaf_Video_Engine_Cost_Model.xlsx` | 31,774 bytes | 7 (Inputs, Per Video, Volume Model, Decision, Measured Proof, Skill Backlog, Public Directory) |
| `workbooks/narration_ExamLeaf_Narration_Cost_Model.xlsx` | `ExamLeaf_Narration_Cost_Model.xlsx` | 29,574 bytes | 6 (Summary, Inputs, Methods, Provider Tariffs, Skills, Sources) |
| `workbooks/business_ExamLeaf_Business_Model.xlsx` | `ExamLeaf_Business_Model.xlsx` | 104,052 bytes | 15 (Read Me, Dashboard, Global Inputs, Scenario Inputs, Volume Inputs, Unit Economics, Season P&L, Cash Flow, Price & CAC, Digital Offer, Funnel, 90-Day Budget, 90-Day Roadmap, Reel Backlog, Sources) |


### 4.3 `csv/` (68 files, 4 sub-folders, unmodified copies of `00_source/spreadsheets_as_csv/`)

Naming: `<workbook>__<sheet>__values.csv` holds the calculated values, `<workbook>__<sheet>__formulas.csv` holds formula text. "Same?" says whether the two files are byte-identical (text/constant sheets have no formulas).


**`csv/v1_engine_ExamLeaf_Cost_and_Skills/`** (12 files = 6 sheets x 2)

| Sheet | Values file | Formulas file | Same? |
|---|---|---|---|
| Inputs | `ExamLeaf_Cost_and_Skills__Inputs__values.csv` | `ExamLeaf_Cost_and_Skills__Inputs__formulas.csv` | yes (no formulas) |
| UnitCosts | `ExamLeaf_Cost_and_Skills__UnitCosts__values.csv` | `ExamLeaf_Cost_and_Skills__UnitCosts__formulas.csv` | no (has formulas) |
| Volumes | `ExamLeaf_Cost_and_Skills__Volumes__values.csv` | `ExamLeaf_Cost_and_Skills__Volumes__formulas.csv` | no (has formulas) |
| CustomSkills | `ExamLeaf_Cost_and_Skills__CustomSkills__values.csv` | `ExamLeaf_Cost_and_Skills__CustomSkills__formulas.csv` | yes (no formulas) |
| ExistingSkills | `ExamLeaf_Cost_and_Skills__ExistingSkills__values.csv` | `ExamLeaf_Cost_and_Skills__ExistingSkills__formulas.csv` | yes (no formulas) |
| ReadMe | `ExamLeaf_Cost_and_Skills__ReadMe__values.csv` | `ExamLeaf_Cost_and_Skills__ReadMe__formulas.csv` | yes (no formulas) |


**`csv/v2_engine_ExamLeaf_Video_Engine_Cost_Model/`** (14 files = 7 sheets x 2)

| Sheet | Values file | Formulas file | Same? |
|---|---|---|---|
| Inputs | `ExamLeaf_Video_Engine_Cost_Model__Inputs__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Inputs__formulas.csv` | yes (no formulas) |
| Per Video | `ExamLeaf_Video_Engine_Cost_Model__Per_Video__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Per_Video__formulas.csv` | no (has formulas) |
| Volume Model | `ExamLeaf_Video_Engine_Cost_Model__Volume_Model__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Volume_Model__formulas.csv` | no (has formulas) |
| Decision | `ExamLeaf_Video_Engine_Cost_Model__Decision__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Decision__formulas.csv` | no (has formulas) |
| Measured Proof | `ExamLeaf_Video_Engine_Cost_Model__Measured_Proof__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Measured_Proof__formulas.csv` | yes (no formulas) |
| Skill Backlog | `ExamLeaf_Video_Engine_Cost_Model__Skill_Backlog__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Skill_Backlog__formulas.csv` | yes (no formulas) |
| Public Directory | `ExamLeaf_Video_Engine_Cost_Model__Public_Directory__values.csv` | `ExamLeaf_Video_Engine_Cost_Model__Public_Directory__formulas.csv` | yes (no formulas) |


**`csv/narration_ExamLeaf_Narration_Cost_Model/`** (12 files = 6 sheets x 2)

| Sheet | Values file | Formulas file | Same? |
|---|---|---|---|
| Summary | `ExamLeaf_Narration_Cost_Model__Summary__values.csv` | `ExamLeaf_Narration_Cost_Model__Summary__formulas.csv` | no (has formulas) |
| Inputs | `ExamLeaf_Narration_Cost_Model__Inputs__values.csv` | `ExamLeaf_Narration_Cost_Model__Inputs__formulas.csv` | yes (no formulas) |
| Methods | `ExamLeaf_Narration_Cost_Model__Methods__values.csv` | `ExamLeaf_Narration_Cost_Model__Methods__formulas.csv` | no (has formulas) |
| Provider Tariffs | `ExamLeaf_Narration_Cost_Model__Provider_Tariffs__values.csv` | `ExamLeaf_Narration_Cost_Model__Provider_Tariffs__formulas.csv` | no (has formulas) |
| Skills | `ExamLeaf_Narration_Cost_Model__Skills__values.csv` | `ExamLeaf_Narration_Cost_Model__Skills__formulas.csv` | yes (no formulas) |
| Sources | `ExamLeaf_Narration_Cost_Model__Sources__values.csv` | `ExamLeaf_Narration_Cost_Model__Sources__formulas.csv` | yes (no formulas) |


**`csv/business_ExamLeaf_Business_Model/`** (30 files = 15 sheets x 2)

| Sheet | Values file | Formulas file | Same? |
|---|---|---|---|
| Read Me | `ExamLeaf_Business_Model__Read_Me__values.csv` | `ExamLeaf_Business_Model__Read_Me__formulas.csv` | yes (no formulas) |
| Dashboard | `ExamLeaf_Business_Model__Dashboard__values.csv` | `ExamLeaf_Business_Model__Dashboard__formulas.csv` | no (has formulas) |
| Global Inputs | `ExamLeaf_Business_Model__Global_Inputs__values.csv` | `ExamLeaf_Business_Model__Global_Inputs__formulas.csv` | no (has formulas) |
| Scenario Inputs | `ExamLeaf_Business_Model__Scenario_Inputs__values.csv` | `ExamLeaf_Business_Model__Scenario_Inputs__formulas.csv` | no (has formulas) |
| Volume Inputs | `ExamLeaf_Business_Model__Volume_Inputs__values.csv` | `ExamLeaf_Business_Model__Volume_Inputs__formulas.csv` | no (has formulas) |
| Unit Economics | `ExamLeaf_Business_Model__Unit_Economics__values.csv` | `ExamLeaf_Business_Model__Unit_Economics__formulas.csv` | no (has formulas) |
| Season P&L | `ExamLeaf_Business_Model__Season_P&L__values.csv` | `ExamLeaf_Business_Model__Season_P&L__formulas.csv` | no (has formulas) |
| Cash Flow | `ExamLeaf_Business_Model__Cash_Flow__values.csv` | `ExamLeaf_Business_Model__Cash_Flow__formulas.csv` | no (has formulas) |
| Price & CAC | `ExamLeaf_Business_Model__Price_&_CAC__values.csv` | `ExamLeaf_Business_Model__Price_&_CAC__formulas.csv` | no (has formulas) |
| Digital Offer | `ExamLeaf_Business_Model__Digital_Offer__values.csv` | `ExamLeaf_Business_Model__Digital_Offer__formulas.csv` | no (has formulas) |
| Funnel | `ExamLeaf_Business_Model__Funnel__values.csv` | `ExamLeaf_Business_Model__Funnel__formulas.csv` | no (has formulas) |
| 90-Day Budget | `ExamLeaf_Business_Model__90-Day_Budget__values.csv` | `ExamLeaf_Business_Model__90-Day_Budget__formulas.csv` | no (has formulas) |
| 90-Day Roadmap | `ExamLeaf_Business_Model__90-Day_Roadmap__values.csv` | `ExamLeaf_Business_Model__90-Day_Roadmap__formulas.csv` | yes (no formulas) |
| Reel Backlog | `ExamLeaf_Business_Model__Reel_Backlog__values.csv` | `ExamLeaf_Business_Model__Reel_Backlog__formulas.csv` | yes (no formulas) |
| Sources | `ExamLeaf_Business_Model__Sources__values.csv` | `ExamLeaf_Business_Model__Sources__formulas.csv` | yes (no formulas) |


Total CSV files: **68** (34 sheets x 2). The file count for the whole section is in the verification log at the end of section 9.


## 5. How to use this section (step by step)

1. **Orient (10 minutes).** Read sections 1-3 here, then the one-paragraph summary at the top of each workbook entry in `COST_MODELS_EXPLAINED.md`. Remember: engine and narration are USD per video; business is INR per retained book; they are separate models (`CONSOLIDATED_COST_SCENARIOS.md` Part E explains the seams).
2. **Pick your question and open the right file.**

| I want to know... | Open |
|---|---|
| What does a 10-minute video cost, and why is it not $2? | `CONSOLIDATED_COST_SCENARIOS.md` Part A and B; `COST_MODELS_EXPLAINED.md` sheets 1.2, 1.3, 2.2, 2.3 |
| Which architecture (AI-heavy / hybrid / self-hosted) and how many reviewers? | `CONSOLIDATED_COST_SCENARIOS.md` Part B; sheets 2.2-2.4 |
| What narration costs under each voice method, and which tariffs are time-limited? | Part C; sheets 3.1-3.4; `INSTRUCTIONS` section 6 |
| Does the book business make money, how much cash does it need, what CAC can it afford? | Part D; sheets 4.5-4.12 |
| How do the models combine without double counting? | `CONSOLIDATED` Part E; `INSTRUCTIONS` section 4 |
| What does cell X do / which cell do I edit? | `COST_MODELS_EXPLAINED.md` (input tables have cell addresses); `INSTRUCTIONS` section 2 |
| What must I get a real quote for? | `INSTRUCTIONS` section 5 |

3. **Make a working copy** of the workbook you need from `workbooks/` (never edit the originals or anything in `00_source/`), open it in Excel/LibreOffice/Numbers, let it recalculate, and confirm the headline numbers in section 3 appear (`INSTRUCTIONS` section 1).
4. **Replace the highest-leverage placeholders first** (`INSTRUCTIONS` section 2): human review minutes and rates (engine, narration); print cost per copy, CAC, sell-through (business). These move the answer most and are the soonest to replace with real data.
5. **Run sensitivities one input at a time** (`INSTRUCTIONS` section 3, which lists 28 edits with the exact results you should see, so you can check your edit worked). Use the built-in scenario sets (3 architectures; 5 narration methods; 9 business cases) and the `Price & CAC` grid.
6. **Combine the models only with the roll-up recipe** (`INSTRUCTIONS` section 4): delete the engine's audio lines, add the narration method, decide the human-minutes overlap in writing (floor to ceiling for v2 hybrid: **$34.95 to $45.78 per video**, arithmetic aid from `CONSOLIDATED` E.3), then convert to INR at Rs 90/USD and compare with the business model's Rs 3,000 per "Reviewed chapter video".
7. **Replace estimates with quotes before committing money** (printer, courier, marketplace, CAC, GST advice, TTS and LLM tariffs, render benchmark, reviewer/performer rates, GPU, generated video, Remotion billing definition): table in `INSTRUCTIONS` section 5.
8. **Re-date everything.** Model names, tariffs and promotions are as of 13 October 2026; record a new "Checked" date whenever you update (`INSTRUCTIONS` section 6).
9. **Respect the gates.** The business roadmap authorises Rs 60,000 for discovery and prototypes first and releases the rest of the Rs 6.5 lakh pilot only after demand, academic quality, tax treatment and a fulfilment proof are validated; suggested ceiling Rs 8 lakh, "not a mandate to spend it all".

## 6. The "planning estimates, not quotes" caveats, reproduced

These are the workbooks' and messages' own words, grouped by source, so that no caveat is lost. Nothing here is paraphrased except where marked.

### 6.1 v1 engine workbook (`ExamLeaf_Cost_and_Skills.xlsx`) and message 02

* ReadMe: "Research date: 13 October 2026. This workbook is an editable planning artifact, not a benchmark, purchasing quote or deployed production system."
* ReadMe, Verified prices versus estimates: "Provider token, voice, storage, CPU/RAM and Remotion prices are cited. Token budgets, render duration, staffing rates and setup effort are assumptions requiring pilot measurements."
* ReadMe, No benchmark claim: "No candidate renderer, voice, locale or model was benchmarked or auditioned as part of this report. Run a representative pilot before committing."
* ReadMe, Excluded / additional costs: "Taxes, rights purchases, playback product development, heavy bespoke 3D, source cleanup, additional languages, and engineering beyond the maintenance allowance require separate budgets."
* ReadMe, Storage / compute scope: "Fargate is a US East rate example, not Mumbai pricing. Render time is an estimate. Storage assumes 2 GB per video for one month; prolonged retention compounds."
* ReadMe, TTS scope: "8,000 narration characters plus 20% regeneration, regular ElevenLabs Multilingual v2 price. Character counts and pronunciation review differ by locale."
* ReadMe, Implementation budget: "$8,000 is an illustrative 320-hour initial build/template budget. This is not a promise of a mature system at that price."
* ReadMe, Remotion option / Assamese gate / Deprecation gate: "Confirm what counts as a billable partial render or still."; "Do not infer locale support from marketing. Verify the exact model API enum and perform native-speaker review."; "Check model availability and pinned Skill defaults before deployment."
* UnitCosts banner: "Established reusable templates; not a cost guarantee for bespoke diagrams or 3D. No promotional prices, free tiers, batch discounts or caching savings assumed."
* Volumes: "Bespoke diagrams, additional languages, heavy Blender rendering, rights clearance, taxes and large platform maintenance are not covered by this baseline." and "20 billable renders/video is an editable assumption, not a verified billing interpretation."
* Inputs, every assumption row: "ExamLeaf planning assumption; not a benchmark or supplier quote."
* Message 02: "Tool rankings are recommendations for your use case—not results of a renderer benchmark or voice audition performed here. ... Rendering time, staffing, and development costs are explicitly identified as planning assumptions."; "The 45-minute render duration is not a measured benchmark, and these are not Mumbai-region prices."; "Four maintenance hours per month is a mature-system planning assumption, not a realistic allowance during active engine development."; "This is an initial engine/template budget—not a quote or promise for a fully mature platform."; "The important conclusion is not “premium videos cost $2.”"

### 6.2 v2 engine workbook (`ExamLeaf_Video_Engine_Cost_Model.xlsx`) and message 10

* Inputs banner: "USD, before tax. Published tariffs are inputs; workloads, rates of regeneration, labour and setup budgets are assumptions. No Higgsfield whole-lesson quote is claimed."
* Inputs, every workload/labour/compute row: "ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload."
* Per Video footer: "Quality is not assumed equal. AI-heavy scenes can fail scientific requirements regardless of spend. Self-hosted labour and GPU time are unmeasured scenarios. Zero generated clips is the default unless their instructional value is approved."
* Decision footer: "Do not confuse machine expense with total production cost. The prototype has no separate cloud invoice; its measured local wall time is not a cloud price or a forecast for 10-minute narrated lessons. Prices checked 13 October 2026. Taxes, viewer delivery, legal costs, hardware purchase and royalties are outside this production model."
* Measured Proof footer: "Eight silent 30s files; two render workers. Simple fixed models, not full curriculum pilots. Scientific checks are bounded; no teacher approval or student study."
* Setup rows: "Initial integration/templates only; not quotation or complete curriculum production."; "Initial engine/templates only; actual authoring and specialist asset requirements may exceed this."; "Serving/integration/templates only; no owned GPU purchase included."
* Message 10: "All figures below are USD before tax. They are planning estimates using published tariff inputs—not vendor quotes or measured ten-minute production costs."; "The token workloads are assumptions, not observations from the local proof."; "The self-hosted case ... does not establish that every self-hosted implementation will cost more than hybrid."; "The AI-heavy case does not assume equal scientific quality."; "The separate local proof had no cloud-render invoice. That is not evidence that production rendering is free."; exclusions: "Taxes, audience streaming, long-term asset retention, legal clearance, purchased hardware, royalties, and a larger engineering team are not silently included."

### 6.3 Narration workbook (`ExamLeaf_Narration_Cost_Model.xlsx`) and message 12

* Summary: "Assumptions, not vendor quotes, controlled provider benchmarks, or guaranteed quality equivalence."; "Do not add these audio-review costs twice if already included in your full video-production budget."; "Tax, voice buyouts, extended licensing, audience streaming, full animation, broad academic research and extra localization."; "One locale/version per case. A second language requires new performance, QA and timeline verification."
* Inputs banner: "USD, before tax | Editable inputs in blue. Reference tariffs and workload assumptions are explicitly separate. Checked 13 October 2026."; cautions such as "NOT a verified Eleven v4 quote", "Obtain actual native subject-reviewer quotations", "No GPU benchmark or supplier quote obtained", "Optional separate initial implementation reserve; not in operating totals."
* Provider Tariffs banner: "Public rates can change. Model, plan, minimum spend and licensing are not interchangeable. Legacy model prices must not drive a new launch."
* Message 12 section 13: "Personnel rates, processing times, retry rate, and GPU figures are editable planning assumptions, not quotations or measured TTS benchmarks."; "It does not prove that self-hosting inherently costs more."; "Obtain the actual overage or higher-tier quote rather than extrapolating a false fixed price."; "Voice buyouts, broader licences, substantial new localization, and hardware purchases require additional budgeting."

### 6.4 Business workbook (`ExamLeaf_Business_Model.xlsx`), JSON and message 06

* Read Me: "18% on the entire marketed bundle is a prudent modelling scenario, NOT a classification opinion. Obtain written advice."; "Evidence: Verified provider tariffs are distinguished from unquoted planning assumptions. Replace printer/courier/account inputs."; "Do not interpret a positive unit contribution as total profitability or use static break-even outside the modeled cost tier."; "500 is a two-title pilot with allocated project labour. Higher cases fund an expanded season; they are not simply 100x the pilot."; "Static contribution / fixed-cost calculation only; per-SKU print pricing, staffing and channel mix must be re-costed at any new volume."; "No legal classification opinion; no corporate/income tax or borrowing interest included. CA/counsel review required."
* Global Inputs: "Proposed test price, not observed ExamLeaf sales."; "Budget buffer, NOT a current FX quote."; "Prudent 18% stress/base tax input, NOT legal classification. All cases use it."; cash timing "NOT A VERIFIED DEMAND FORECAST"; seasonality "no official exam date is assumed".
* Scenario Inputs: "ALL REQUIRE PILOT VALIDATION"; "Planning estimate; replace with paid pilot and supplier/account quotations."; "Unquoted planning assumption ... Review before committing stock or ad spend."
* Volume Inputs: "PRINT QUOTES MUST BE PER TITLE / LANGUAGE / RUN"; "Planning assumption, not an obtained quotation or demand forecast. Printing economies depend on copies PER SKU and batch, not aggregate sales."
* Dashboard: "This is a model, not a sales forecast." Price & CAC: "Management target of INR100 contribution per book, not a market norm."; "no established elasticity or conversion lift assumed." Funnel: "Illustrative funnel assumptions, not platform benchmarks."; "not signed partner commitments."; "not guaranteed rates." 90-Day Budget: "Planning allocation, not a supplier or employment quote."
* Sources: "Printing, shipping, CAC, sell-through, salaries, conversions and production workloads are estimates. Replace with quotes and observed cohort data. No virality or demand forecast claimed."; "Not an ExamLeaf quote; none of the modeled unit costs are represented as quoted."
* Message 06: "These are planning scenarios, not sales forecasts or supplier quotations."; "Printing, courier cost, CAC, sell-through, staffing and conversion rates: Planning assumptions requiring validation"; "The print costs must be achieved at the actual per-SKU phased batch sizes. They are not confirmed quotes."; "These are model outputs, not channel guarantees."; "These are static cost-tier calculations. Requote printing, staffing and distribution when crossing a scale threshold; do not present either as a guaranteed real-world break-even point."; "Obtain written advice before finalizing prices and invoices."; "The biggest unresolved commercial inputs are actual per-SKU printer quotes, courier/account charges, language demand, partner sell-through, and observed customer acquisition costs."

## 7. Cross-references to other sections


| Section | File / folder | Relation to 08_cost_models |
|---|---|---|
| 01_business_model | `01_business_model/README.md` | Business plan and launch: this section's Part D/sheets 4.x are the numbers behind it |
| 01_business_model | `01_business_model/FINANCIAL_SCENARIOS_SUMMARY.md` | Prose summary of the nine scenarios |
| 01_business_model | `01_business_model/FULL_business_model_launch_financial_plan.md` | Full message 06 (sections 10, 11, 14 are reproduced in CONSOLIDATED Part D) |
| 01_business_model | `01_business_model/INSTRUCTIONS_business_launch_runbook.md` | Launch runbook (pilot gates, Rs 60,000 discovery cap, Rs 8 lakh ceiling) |
| 01_business_model | `01_business_model/toolkit` | Toolkit copy of the business workbook, JSON, runbook, source ledger, Reel backlog |
| 01_business_model | `01_business_model/workbook_csv` | Sibling copy of the business CSVs |
| 01_business_model | `01_business_model/toolkit/ExamLeaf_Business_Model.xlsx` | The same business workbook as shipped in the toolkit (byte-identical to workbooks/business_...) |
| 04_video_engine | `04_video_engine/planning_pack_v1/ExamLeaf_Cost_and_Skills.xlsx` | The same v1 workbook as shipped in the Planning Pack |
| 04_video_engine | `04_video_engine/implementation_v2/ExamLeaf_Video_Engine_Cost_Model.xlsx` | The same v2 workbook as shipped in the Implementation pack |
| 05_narration_system | `05_narration_system/narration_system_v1/ExamLeaf_Narration_Cost_Model.xlsx` | The same narration workbook as shipped in the Narration System pack |
| 05_narration_system | `05_narration_system/narration_system_v1/docs/Costs_and_Methods.md` | ChatGPT's own prose restatement of the narration cost tables |
| 04_video_engine | `04_video_engine/README.md` | Video engine section |
| 04_video_engine | `04_video_engine/FULL_v1_architecture_and_plan.md` | Full message 02 (section 13 cost analysis) |
| 04_video_engine | `04_video_engine/FULL_v2_implementation_and_research.md` | Full message 10 (section 11 production costs) |
| 04_video_engine | `04_video_engine/V1_vs_V2_evolution.md` | Why v1 ($20.37) and v2 ($34.34 hybrid) differ |
| 04_video_engine | `04_video_engine/ARCHITECTURE_consolidated.md` | Architecture behind the three cost architectures |
| 04_video_engine | `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` | How to build and run the prototype that produced the Measured Proof sheet |
| 04_video_engine | `04_video_engine/SKILLS_INDEX_video_engine_32.md` | The 32 Skills in the v2 Skill Backlog sheet |
| 05_narration_system | `05_narration_system/README.md` | Narration section |
| 05_narration_system | `05_narration_system/FULL_narration_system.md` | Full message 12 (section 13 costs) |
| 05_narration_system | `05_narration_system/TTS_PROVIDER_COMPARISON.md` | Provider facts behind the Provider Tariffs sheet |
| 05_narration_system | `05_narration_system/INSTRUCTIONS_narration_pipeline.md` | How the narration pipeline runs |
| 05_narration_system | `05_narration_system/SKILLS_INDEX_narration_15.md` | The 15 Skills in the narration Skills sheet |
| 06_skills_library | `06_skills_library/README.md` | Skills library |
| 06_skills_library | `06_skills_library/SKILLS_MATRIX.csv` | All Skills (40 v1 + 32 v2 + 15 narration + existing/public) |
| 06_skills_library | `06_skills_library/backlogs` | Sibling copies of the CustomSkills / ExistingSkills / Skill Backlog / Skills CSVs |
| 06_skills_library | `06_skills_library/public_skills_directory` | Sibling copy of the Public Directory CSV and the public-tools directories |
| 06_skills_library | `06_skills_library/OVERLAP_and_DEDUPLICATION.md` | Overlap between the 40 / 32 / 15 Skill sets (the labour-side counterpart of the cost overlap in Part E) |
| 09_research_and_evidence | `09_research_and_evidence/EVIDENCE_REGISTER.md` | Evidence register: where each cited price/tariff/fact came from |
| 09_research_and_evidence | `09_research_and_evidence/cited_source_links.md` | All source URLs cited in the transcript (pricing pages behind the Source columns) |
| 09_research_and_evidence | `09_research_and_evidence/ledgers` | Source ledgers per pack (business toolkit, narration, planning pack, spreadsheet sheets) |
| 00_source | `00_source/chatgpt_transcript/cited_source_links.md` | Raw cited links (original) |


Also: `07_end_to_end_pipeline_instructions/` (how cost gates fit the end-to-end pipeline) and `10_pilots_and_examples/` (pilot lessons whose timed review minutes should replace the placeholders here).

## 8. Gaps, discrepancies and open points found while building this section

1. **Sheet counts.** The brief said 35 sheets and 16 business sheets; the files contain **34 sheets (6 + 7 + 6 + 15)**, matching the 68 CSVs exactly. Nothing is missing. *(15 Oct 2026: `00_source/README.md` line 37 still says "35 sheets, 68 files"; correct figure is 34; `00_source/` is not edited.)*
2. **Comments are not in the CSVs.** 3 workbooks carry Excel threaded comments (v2: 62; narration: 22; business: 145; v1: none). They were extracted and are reproduced in `COST_MODELS_EXPLAINED.md`; most repeat the Source/caveat columns; the comments subsection of each workbook entry lists every distinct comment text and the cells it sits on.
3. **The workbooks are not linked.** No formula connects the four files. The only numeric seam is business `90-Day Budget` row 6 (Rs 3,000 per reviewed chapter video); **the workbook does not say how Rs 3,000 was derived** (it equals $33.33 at Rs 90/USD, between the v1 and v2-hybrid per-video costs and below the upper end of the combined engine + narration bracket).
4. **Engine v1 and v2 use different LLM labels and tariffs** ("Haiku/Sonnet/Opus 5.5" + `gpt-6.1-sol` vs "Haiku 4.5 / Sonnet 4.6 / Opus 4.6"), different TTS tariffs ($0.08 vs $0.10 per 1,000 characters), characters (8,000 vs 7,800 in the narration workbook) and QA rates ($12 vs $15). Neither set was independently verified here; reconcile before combining (`INSTRUCTIONS` sections 4 and 6).
5. *(15 Oct 2026: under RD-41 the overlap no longer changes cash, because review is $0; the bracket collapses to $8.28, see 3.1. It still matters for review-minute capacity.)* **Audio review labour overlaps** between engine and narration workbooks; ChatGPT warned twice but gave no recipe. This section supplies one and a floor-to-ceiling bracket ($34.95 to $45.78 per video for hybrid + premium TTS) which is the team's arithmetic, **not** a ChatGPT output.
6. **Engine and narration set-up budgets are not in the business model** ($4,000 to $16,000, i.e. Rs 3.6 to 14.4 lakh), and the Rs 8 lakh pilot ceiling cannot absorb them.
7. **Only measured data:** v2 `Measured Proof` (8 silent 30-second 2D renders, 27.3 to 29.4 s each on local CPUs). No renderer, voice, GPU or LLM workload has been benchmarked for a 10-minute narrated lesson; all token budgets, render times, review minutes and regeneration rates are assumptions.
8. **Unpriced or unresolved in the source:** Eleven v4 ("TBD"), Cartesia above 8 million credits, Luma API final rate, Higgsfield whole-lesson quote, Remotion billable-render definition, Sarvam Assamese support, GST classification of the bundle, printer quotes, courier/marketplace account fees, demand.
9. **Descriptive-only input cells** (no formula reads them): v2 `Inputs!B6`, `B39`; narration `Inputs!B6`, `B8`; business `Global Inputs!B20:B26`.
10. **Business Base case is the only one linked to the 90-Day Budget** (`Volume Inputs!D5, D8, D11`); Conservative and Optimistic fixed spends are typed constants.
11. **Cash flow vs P&L:** the P&L expenses all printed copies; the cash model pays for them with a 50% advance, so final cumulative cash equals operating profit (e.g. Base 5,000: -Rs 6,09,325). Funding need (peak gap + 15%) is larger than the loss in every scenario where it is negative.
12. **Not done here:** no network access and no package installation were used; the .xlsx files were not recalculated in Excel; numbers are read from the CSVs and independently re-derived. No new quotations were obtained.

## 9. Provenance and integrity check

* Every file under `workbooks/`, `csv/` and `model_assumptions_and_results.json` was copied with `cp` from `00_source/` and verified byte-identical with `cmp` (result recorded below). Nothing under `00_source/` was modified.
* `COST_MODELS_EXPLAINED.md`, `CONSOLIDATED_COST_SCENARIOS.md` and `INSTRUCTIONS_how_to_use_cost_models.md` were generated from the CSVs, the workbooks' embedded comments and the message files; the verbatim blocks are copied programmatically (citation markers removed) with their source line ranges stated.


**Verification log (re-run when this README was generated).** 73 of 73 placed data files (4 workbooks + 68 CSVs + 1 JSON) compared byte-identical to their `00_source/` originals (`filecmp`, equivalent to `cmp`); the 68 CSVs placed are exactly the 68 files in `00_source/spreadsheets_as_csv/` (none missing, none extra). `00_source/` itself was only read.

Total files in `08_cost_models/` including this README and the three generated documents: **77** (73 copied data files + `README.md`, `COST_MODELS_EXPLAINED.md`, `CONSOLIDATED_COST_SCENARIOS.md`, `INSTRUCTIONS_how_to_use_cost_models.md`).
