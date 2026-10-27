# Cost Models Explained, sheet by sheet

**Section:** `08_cost_models/` of the ExamLeaf Video Engine project.
**Research / model date:** 13 October 2026 (every workbook states "checked/verified 13 October 2026").
**Status of everything below:** planning estimates, not quotes. Every workbook says so itself; the caveats are reproduced in each sheet's entry and in `README.md`.

This file walks through **all 34 sheets of the four ChatGPT-generated Excel workbooks** in `workbooks/` (the brief mentioned 35 sheets / 16 business sheets; the actual workbook files contain 6 + 7 + 6 + 15 = **34 sheets**, and the 68 CSV files in `csv/` are exactly 34 sheets x 2, a `__values.csv` and a `__formulas.csv` each). For each sheet it gives: what the sheet contains, its **editable inputs** (with the Excel cell address), its **key outputs** (with the numbers as stored in the workbook), and the **formula logic in plain English** (read from the `__formulas.csv` files).

## How to read this file

* **Cell addresses.** In every CSV, line *n* is Excel row *n* and the first column is column A. So the "Value" column of an Inputs sheet is column **B**, e.g. `Inputs!B13`. Formulas below use the same addresses.
* **values vs formulas CSVs.** `__values.csv` holds the numbers Excel had calculated when ChatGPT saved the file; `__formulas.csv` holds the formula text (`=...`) for formula cells and the constant for constant cells. For text-only sheets the two files are byte-identical (stated per sheet).
* **Colour convention.** v1 engine workbook: "Edit blue Inputs cells." Business workbook: "Blue text on pale yellow = assumptions. Green = linked formulas. Black = same-sheet calculations." Narration workbook: "Editable inputs in blue." (The CSVs carry no colour, open the .xlsx to see it.)
* **Threaded cell comments.** Three workbooks carry Excel threaded comments (v2 engine, narration, business) that are **not** in the CSVs. They are extracted into the "Cell comments" subsection of each workbook below, so nothing is lost.
* **Numbers.** Shown rounded for readability (the CSV holds full precision). USD for the three engine/narration workbooks, INR for the business workbook (lakh = 100,000).
* **Where the headline tables came from.** The four chat messages quote the workbook outputs; they are reproduced verbatim in `CONSOLIDATED_COST_SCENARIOS.md`. Editing instructions are in `INSTRUCTIONS_how_to_use_cost_models.md`.

## The four workbooks at a glance

| # | File in `workbooks/` | Original name | Source message / pack | Sheets | Currency | What it prices |
|---|---|---|---|---:|---|---|
| 1 | `v1_engine_ExamLeaf_Cost_and_Skills.xlsx` | `ExamLeaf_Cost_and_Skills.xlsx` | Message 02 (video engine architecture and plan v1); original sandbox path `/mnt/data/ExamLeaf_Video_Engine/ExamLeaf_Cost_and_Skills.xlsx`; also described in the Video Engine Planning Pack (`ExamLeaf_Video_Engine_Planning_Pack.zip`) | 6 | USD pre-tax | One 10-minute video made with the recommended reusable-component stack (HyperFrames + SVG/KaTeX/GSAP + Python checks + FFmpeg); 1 / 100 / 1,000 videos; plus the 40-Skill inventory |
| 2 | `v2_engine_ExamLeaf_Video_Engine_Cost_Model.xlsx` | `ExamLeaf_Video_Engine_Cost_Model.xlsx` | Message 10 (video engine implementation v2); original path `/mnt/data/ExamLeaf_Video_Engine_Cost_Model.xlsx`; companion to the Implementation pack (`ExamLeaf_Video_Engine_Implementation.zip`) | 7 | USD pre-tax | Three architectures (AI-heavy, Hybrid, Mostly self-hosted) per video and at 1 / 100 / 1,000; human capacity; Shorts add-on; the 8-fixture render proof; 32-Skill backlog; public tools directory |
| 3 | `narration_ExamLeaf_Narration_Cost_Model.xlsx` | `ExamLeaf_Narration_Cost_Model.xlsx` | Message 12 (narration system); original path `/mnt/data/ExamLeaf_Narration_Cost_Model.xlsx`; companion to `ExamLeaf_Narration_System.zip` | 6 | USD pre-tax | The narration sub-system only: five voice-production methods at 1 / 100 / 1,000; provider tariff references; 15 narration Skills; source ledger |
| 4 | `business_ExamLeaf_Business_Model.xlsx` | `ExamLeaf_Business_Model.xlsx` | Message 06 (business model, launch and financial plan); original path `/mnt/data/ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx`; byte-identical copy inside `ExamLeaf_Business_Launch_Toolkit.zip` (which also supplies `model_assumptions_and_results.json`) | 15 | INR (lakh on Dashboard/P&L) | The book-linked business: nine scenarios (3 cases x 500 / 5,000 / 50,000 retained books), unit economics, season P&L, 12-month cash flow, price/CAC sensitivity, digital-only offer, funnel, 90-day budget and roadmap, 36-Reel backlog, source ledger |

### How the sheets feed each other (dependency map)

```
v1 engine     Inputs --> UnitCosts --> Volumes            (CustomSkills, ExistingSkills, ReadMe: text only)
v2 engine     Inputs --> Per Video --> Volume Model --> Decision   (Measured Proof, Skill Backlog, Public Directory: text/data only)
narration     Inputs --> Methods --> Summary (+ chart)    Inputs --> Provider Tariffs   (Skills, Sources: text only)
business      Global Inputs + Scenario Inputs + Volume Inputs (+ 90-Day Budget B14/C14/D14 for the Base fixed spend)
                   --> Unit Economics --> Season P&L --> Dashboard
                   --> Cash Flow (monthly, 9 blocks) --> Dashboard (peak gap, funding)
              Unit Economics --> Price & CAC, Funnel     Global Inputs --> Digital Offer
              Read Me, 90-Day Roadmap, Reel Backlog, Sources: text only
```

There are **no formulas linking the four workbooks to each other**; the only numeric seam between engine/narration (USD) and business (INR) is the business line "Reviewed chapter videos" (see the business section and the reconciliation in `CONSOLIDATED_COST_SCENARIOS.md`).

---

# WORKBOOK 1: v1 engine cost model, `v1_engine_ExamLeaf_Cost_and_Skills.xlsx`

**Original file name:** `ExamLeaf_Cost_and_Skills.xlsx` (raw copy: `00_source/downloads/ExamLeaf_Video_Engine/`).
**From:** message `02_ASSISTANT_video_engine_architecture_and_plan_v1.md` (section 13 quotes this workbook; the message links it as "Editable cost model and Skills inventory - Excel").
**CSV folder:** `csv/v1_engine_ExamLeaf_Cost_and_Skills/` (12 files = 6 sheets x values/formulas).
**Sheets (in tab order):** Inputs, UnitCosts, Volumes, CustomSkills, ExistingSkills, ReadMe.
**One-paragraph summary:** the baseline cost of one finished 10-minute STEM revision video made from a reusable-component library: about **$2.37 of machine cost + $18 of human review = $20.37 per video**, plus **$200/month fixed overhead** and an **$8,000 one-time build budget**. Human review, not AI, dominates the cost.

## Sheet 1.1 `Inputs`
**Contains:** 51 assumptions (rows 5-55), columns A = assumption, B = value (the editable blue cell), C = units/qualification, D = source (a URL for published tariffs, or "ExamLeaf planning assumption; not a benchmark or supplier quote."). Title row: "Verified 13 October 2026. Blue values are editable. USD, before taxes. Sources and estimate status are explicit."
**Editable cells:** every value in column B. Published tariffs (ElevenLabs, Claude/OpenAI token prices, AWS Fargate, Cloudflare R2, Remotion) are inputs with URLs; token budgets, render time, labour rates and set-up hours are assumptions.
**Formula logic:** none (constants only; `__values.csv` and `__formulas.csv` are identical for this sheet).


| Cell | Assumption / rate | Value | Units / qualification | Source |
|---|---|---|---|---|
| B5 | Video duration | 10 | minutes | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B6 | Narration characters | 8,000 | characters/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B7 | TTS regeneration allowance | 0.2 | fraction | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B8 | TTS standard price | 0.08 | USD/1,000 characters | https://elevenlabs.io/pricing/api |
| B9 | Haiku input budget | 30,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B10 | Haiku output budget | 5,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B11 | Haiku input price | 0.1 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B12 | Haiku output price | 0.5 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B13 | Sonnet input budget | 120,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B14 | Sonnet output budget | 25,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B15 | Sonnet input price | 2 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B16 | Sonnet output price | 10 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B17 | Sol input budget | 60,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B18 | Sol output budget | 10,000 | tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B19 | Sol input price | 2 | USD/million tokens | https://developers.openai.com/api/docs/pricing |
| B20 | Sol output price | 10 | USD/million tokens | https://developers.openai.com/api/docs/pricing |
| B21 | Opus escalation input allowance | 10,000 | amortized tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B22 | Opus escalation output allowance | 2,000 | amortized tokens/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B23 | Opus input price | 4 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B24 | Opus output price | 20 | USD/million tokens | https://platform.claude.com/docs/en/about-claude/pricing |
| B25 | LLM regeneration allowance | 0.3 | fraction | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B26 | Worker vCPU | 8 | vCPU | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B27 | Worker RAM | 16 | GB | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B28 | Render wall time | 45 | worker minutes/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B29 | Render retry allowance | 0.2 | fraction | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B30 | CPU price | 0.000011244 | USD/vCPU-second; US East example | https://aws.amazon.com/fargate/pricing/ |
| B31 | RAM price | 0.000001235 | USD/GB-second; US East example | https://aws.amazon.com/fargate/pricing/ |
| B32 | ASR validation price | 0.003 | USD/minute | https://developers.openai.com/api/docs/pricing |
| B33 | Retained working assets | 2 | GB/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B34 | Storage price | 0.015 | USD/GB-month | https://developers.cloudflare.com/r2/pricing/ |
| B35 | Storage duration | 1 | months | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B36 | Miscellaneous API / request reserve | 0.15 | USD/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B37 | Academic review time | 45 | minutes/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B38 | Academic reviewer rate | 20 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B39 | Production QA time | 15 | minutes/video | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B40 | Production QA rate | 12 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B41 | Fixed infrastructure / tools | 100 | USD/month; allowance | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B42 | Maintenance engineering time | 4 | hours/month; mature-system allowance | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B43 | Maintenance rate | 25 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B44 | Production accounting period | 1 | months for compared volume | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B45 | Setup engineering time | 240 | hours | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B46 | Setup engineering rate | 25 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B47 | Setup academic template time | 60 | hours | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B48 | Setup academic template rate | 25 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B49 | Setup design / voice time | 20 | hours | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B50 | Setup design / voice rate | 25 | USD/hour | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B51 | Optional Remotion paid-license switch | 0 | 0 = HyperFrames baseline; 1 = paid Remotion | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B52 | Remotion automation minimum | 100 | USD/month, when license applies | https://www.remotion.dev/docs/license/pricing |
| B53 | Remotion per billable render | 0.01 | USD/render, when license applies | https://www.remotion.dev/docs/license/pricing |
| B54 | Billable Remotion renders per video | 20 | assumption; confirm billing definition | ExamLeaf planning assumption; not a benchmark or supplier quote. |
| B55 | Optional developer subscriptions | 0 | USD/month; enter actual incremental seats | ExamLeaf planning assumption; not a benchmark or supplier quote. |


**Model labels used in this workbook.** The LLM lines are labelled in `UnitCosts` as "Haiku 5.5", "Sonnet 5.5", "gpt-6.1-sol" (OpenAI independent review) and "Opus 5.5", at the prices above (Haiku $0.10/$0.50, Sonnet $2/$10, Sol $2/$10, Opus $4/$20 per million input/output tokens). Model names and prices are as of 13 October 2026 and **will change**; the v2 workbook (workbook 2) uses different model labels and prices. See the lifecycle warning in `INSTRUCTIONS_how_to_use_cost_models.md`.

**Remotion switch.** `Inputs!B51 = 0` (HyperFrames baseline, no paid renderer licence). Set to 1 only if Remotion's commercial licence applies; the licence is then `MAX($100/month minimum x period, $0.01 x 20 billable renders x videos)`. The 20 renders/video is an "assumption; confirm billing definition".

## Sheet 1.2 `UnitCosts`
**Contains:** cost per finished 10-minute video, line by line (rows 5-22). Column A = component, B = USD/video, C = basis/scope. Title note: "Established reusable templates; not a cost guarantee for bespoke diagrams or 3D. No promotional prices, free tiers, batch discounts or caching savings assumed."
**Editable cells:** none (all column B cells are formulas on `Inputs`).


| Cell | Component | USD | Formula logic in plain English | Basis / scope (column C) |
|---|---|---|---|---|
| B5 | Haiku extraction / routing | 0.0055 | (Haiku input tokens x Haiku input price + Haiku output tokens x Haiku output price) / 1,000,000   [Inputs B9..B12] | Haiku 5.5; prompts remain within short-context tier. |
| B6 | Sonnet scripting / component adaptation | 0.49 | (Sonnet in x price + Sonnet out x price) / 1,000,000   [Inputs B13..B16] | Sonnet 5.5; total tokens across bounded calls. |
| B7 | Independent OpenAI review | 0.22 | (Sol in x price + Sol out x price) / 1,000,000, the independent OpenAI review   [Inputs B17..B20] | gpt-6.1-sol; short-context rates. |
| B8 | Opus escalation reserve | 0.08 | (Opus escalation in x price + out x price) / 1,000,000, an amortised reserve   [Inputs B21..B24] | Opus 5.5 amortized reserve, not required on every scene. |
| B9 | Base LLM subtotal | 0.7955 | SUM of the four LLM lines above (rows 5-8) | Before regeneration allowance. |
| B10 | LLM cost with regeneration | 1.0342 | Base LLM subtotal x (1 + LLM regeneration allowance 30%)   [Inputs B25] | Includes a 30% retry/rewrite reserve. |
| B11 | Narration with regeneration | 0.768 | Narration characters x (1 + TTS regeneration 20%) x TTS price per 1,000 characters / 1000 = 8,000 x 1.2 x $0.08 / 1000   [Inputs B6..B8] | ElevenLabs Multilingual v2 standard character price. |
| B12 | Rendering with retries | 0.3555 | (vCPU x CPU $/vCPU-second + GB RAM x RAM $/GB-second) x render minutes x 60 x (1 + retry allowance 20%) = (8 x 0.000011244 + 16 x 0.000001235) x 45 x 60 x 1.2   [Inputs B26..B31] | Fargate US East rate example. 45 minutes is an unmeasured planning assumption. |
| B13 | ASR validation | 0.03 | Video duration (10 min) x ASR price $0.003/min   [Inputs B5, B32] | Validation transcription only; alignment accuracy must still be checked. |
| B14 | Working-asset storage | 0.03 | Retained GB (2) x storage price ($0.015/GB-month) x months (1)   [Inputs B33..B35] | 2 GB retained for one month; archive growth is recurring. |
| B15 | API / request reserve | 0.15 | Miscellaneous API / request reserve (flat $0.15)   [Inputs B36] | Planning reserve, not a quoted service bundle. |
| B16 | VARIABLE MACHINE COST | 2.3676 | SUM of rows 10-15 (LLM with regeneration + narration + rendering + ASR + storage + reserve). Excludes humans, fixed overhead and initial engine development | Excludes humans, fixed overhead and initial engine development. |
| B17 | Academic review | 15 | Academic review minutes / 60 x academic rate = 45/60 x $20   [Inputs B37, B38] | Review approved claims, script, derivations and the entire final lesson. |
| B18 | Production QA | 3 | Production QA minutes / 60 x QA rate = 15/60 x $12   [Inputs B39, B40] | Mobile, audio, captions, continuity and export review. |
| B19 | HUMAN REVIEW COST | 18 | SUM of rows 17-18 (one reviewer-hour in the base scenario) | One reviewer-hour in the base scenario. |
| B20 | TOTAL VARIABLE COST | 20.3676 | Variable machine cost (row 16) + human review cost (row 19) | Established engine and component library. |
| B21 | Fixed monthly overhead | 200 | Infrastructure allowance ($100) + maintenance hours x rate (4 x $25) + optional developer subscriptions ($0)   [Inputs B41, B42 x B43, B55] | Infrastructure allowance + maintenance + optional developer subscriptions. |
| B22 | One-time implementation budget | 8,000 | Setup engineering 240 h x $25 + academic template 60 h x $25 + design/voice 20 h x $25   [Inputs B45..B50] | Illustrative 320-hour setup. A mature platform may cost substantially more. |


**Key outputs and what they mean.**

* `UnitCosts!B16` **variable machine cost = $2.3676 per video** (LLMs $1.0342 + narration $0.768 + rendering $0.3555 + ASR $0.03 + storage $0.03 + reserve $0.15).
* `UnitCosts!B19` **human review = $18.00 per video**; `B20` **total variable = $20.3676 per video**. Human review is 88% of the per-video variable cost.
* `UnitCosts!B21` **fixed monthly overhead = $200**; `B22` **one-time implementation = $8,000** ("Illustrative 320-hour setup. A mature platform may cost substantially more.").
* The production-cost formula quoted in message 02 is `Production cost = N x (2.3676 + 18) + 200`, i.e. `N x (B16 + B19) + B21`.

## Sheet 1.3 `Volumes`
**Contains:** the same one-month accounting period priced at **1, 100 and 1,000 videos** (columns B, C, D). Title: "USD, pre-tax. Same one-month accounting period. Reusable-component baseline; initial implementation is shown separately."
**Editable cells:** row 5 (Videos: 1 / 100 / 1000) can be changed to any volume; everything else is a formula.


| Row | Metric | 1 video | 100 videos | 1,000 videos | Formula logic |
|---|---|---|---|---|---|
| 5 | Videos | 1 | 100 | 1,000 | Input: number of videos |
| 6 | Variable machine cost | 2.3676 | 236.7617 | 2,367.62 | Videos x variable machine cost per video (UnitCosts B16) |
| 7 | Human review | 18 | 1,800 | 18,000 | Videos x human review cost per video (UnitCosts B19) |
| 8 | Fixed overhead for accounting period | 200 | 200 | 200 | Fixed monthly overhead (UnitCosts B21) x accounting-period months (Inputs B44). Not multiplied by videos |
| 9 | Optional Remotion licensing | 0 | 0 | 0 | Remotion switch (Inputs B51) x MAX(monthly minimum $100 x period, $0.01 x billable renders/video 20 x videos). Zero while the switch is 0 |
| 10 | TOTAL PRODUCTION COST | 220.3676 | 2,236.76 | 20,567.62 | SUM of rows 6-9 |
| 11 | Average production cost per video | 220.3676 | 22.3676 | 20.5676 | Total production cost / videos |
| 12 | One-time implementation | 8,000 | 8,000 | 8,000 | One-time implementation (UnitCosts B22) |
| 13 | TOTAL INCLUDING IMPLEMENTATION | 8,220.37 | 10,236.76 | 28,567.62 | Total production cost + one-time implementation |
| 14 | Reviewer hours required | 1 | 100 | 1,000 | Videos x (academic review min + QA min) / 60, the reviewer hours required |
| 15 | Render worker hours required | 0.9 | 90 | 900 | Videos x render minutes x (1 + retry 20%) / 60, the render-worker hours required |
| 16 | Reviewer FTE at 160 h/month | 0.00625 | 0.625 | 6.25 | Reviewer hours / (160 hours x months), reviewer full-time equivalents |
| 17 | Machine cost share of production | 0.0107 | 0.1059 | 0.1151 | Variable machine cost / total production cost |


**Key outputs.** Total production cost: **$220.37 / $2,236.76 / $20,567.62** (average $220.37 / $22.37 / $20.57 per video). Including the $8,000 implementation: **$8,220.37 / $10,236.76 / $28,567.62**. At 1,000 videos: 1,000 reviewer hours = 6.25 FTE at 160 h/month, 900 render-worker hours. Machine cost is only 1.07% / 10.6% / 11.5% of production cost.

**Two caveats stated on the sheet (verbatim).**

* "Sensitivity: increasing review to $40/video adds $22/video. Bespoke diagrams, additional languages, heavy Blender rendering, rights clearance, taxes and large platform maintenance are not covered by this baseline."
* "Remotion switch defaults to 0. When enabled, 20 billable renders/video is an editable assumption, not a verified billing interpretation. Confirm partial-scene/still billing with the vendor before purchase." (With the switch on, the Remotion line is $100 / $100 / $200 at 1 / 100 / 1,000 videos.)

## Sheet 1.4 `CustomSkills`
**Contains:** "EXAMLEAF | 40 CUSTOM SKILLS": a complete **proposed** inventory of 40 custom Claude/Codex Skills (header row 4, Skills in rows 5-44; columns ID, Custom Skill, Workstream, Priority, Status, Inputs, Outputs, Release test / boundary). Subtitle: "A complete proposed v1 inventory, not a claim that these Skills exist or have been implemented. P0 = pilot core; P1 = scaling; P2 = selective extension." Every row's Status is **"Proposed; not implemented"**. No formulas (values = formulas file). It carries **no cost numbers**; it is the scope behind the $8,000 build budget. The full text of every column is in `csv/v1_engine_ExamLeaf_Cost_and_Skills/ExamLeaf_Cost_and_Skills__CustomSkills__values.csv`; the Skills themselves are catalogued in `06_skills_library/`.


| ID | Custom Skill | Workstream | Priority | Status |
|---|---|---|---|---|
| 1 | examleaf-rights-ingest | Sources | P0 | Proposed; not implemented |
| 2 | examleaf-syllabus-map | Sources | P0 | Proposed; not implemented |
| 3 | examleaf-source-claim-ledger | Sources | P0 | Proposed; not implemented |
| 4 | examleaf-prerequisite-graph | Sources | P1 | Proposed; not implemented |
| 5 | examleaf-lesson-scope | Pedagogy | P0 | Proposed; not implemented |
| 6 | examleaf-revision-script | Pedagogy | P0 | Proposed; not implemented |
| 7 | examleaf-worked-examples | Pedagogy | P0 | Proposed; not implemented |
| 8 | examleaf-retrieval-challenges | Pedagogy | P1 | Proposed; not implemented |
| 9 | examleaf-misconception-audit | Pedagogy | P0 | Proposed; not implemented |
| 10 | examleaf-confidence-load-audit | Pedagogy | P1 | Proposed; not implemented |
| 11 | examleaf-exam-rubric | Pedagogy | P1 | Proposed; not implemented |
| 12 | examleaf-math-verification | Science | P0 | Proposed; not implemented |
| 13 | examleaf-physics-verification | Science | P0 | Proposed; not implemented |
| 14 | examleaf-chemistry-verification | Science | P0 | Proposed; not implemented |
| 15 | examleaf-biology-verification | Science | P0 | Proposed; not implemented |
| 16 | examleaf-independent-review | Science | P0 | Proposed; not implemented |
| 17 | examleaf-storyboard | Visuals | P0 | Proposed; not implemented |
| 18 | examleaf-design-system | Visuals | P0 | Proposed; not implemented |
| 19 | examleaf-scene-compiler | Visuals | P0 | Proposed; not implemented |
| 20 | examleaf-equation-animation | Visuals | P0 | Proposed; not implemented |
| 21 | examleaf-graph-geometry | Visuals | P0 | Proposed; not implemented |
| 22 | examleaf-physics-animation | Visuals | P1 | Proposed; not implemented |
| 23 | examleaf-chemistry-animation | Visuals | P1 | Proposed; not implemented |
| 24 | examleaf-biology-animation | Visuals | P1 | Proposed; not implemented |
| 25 | examleaf-manim-adapter | Adapters | P0 | Proposed; not implemented |
| 26 | examleaf-threejs-adapter | Adapters | P2 | Proposed; not implemented |
| 27 | examleaf-narration-normalizer | Audio | P0 | Proposed; not implemented |
| 28 | examleaf-pronunciation-lexicon | Audio | P0 | Proposed; not implemented |
| 29 | examleaf-tts-batch-cache | Audio | P0 | Proposed; not implemented |
| 30 | examleaf-forced-alignment | Audio | P0 | Proposed; not implemented |
| 31 | examleaf-multilingual-localization | Audio | P1 | Proposed; not implemented |
| 32 | examleaf-render-orchestrator | Operations | P0 | Proposed; not implemented |
| 33 | examleaf-audio-mastering | Operations | P0 | Proposed; not implemented |
| 34 | examleaf-captions-export | Operations | P0 | Proposed; not implemented |
| 35 | examleaf-visual-accessibility-qa | QA | P0 | Proposed; not implemented |
| 36 | examleaf-science-frame-qa | QA | P0 | Proposed; not implemented |
| 37 | examleaf-regression-qa | QA | P0 | Proposed; not implemented |
| 38 | examleaf-rights-security-release | QA | P0 | Proposed; not implemented |
| 39 | examleaf-bulk-cost-ops | Operations | P1 | Proposed; not implemented |
| 40 | examleaf-learning-evaluation | Evaluation | P1 | Proposed; not implemented |


Priority counts: P0 = 29, P1 = 10, P2 = 1 (total 40).


## Sheet 1.5 `ExistingSkills`
**Contains:** "EXAMLEAF | EXISTING SKILLS": six maintainers' existing public Skill collections ChatGPT recommended as starting points (columns Maintainer, Selected existing resources, Use, Caveat / licensing, Repository / docs, Verified manifest / example). Banner: "Verified resources are starting points, not automatically safe or correct for school science. Pin reviewed commits and maintain negative tests." No formulas, no cost numbers.


| Maintainer | Selected existing resources | Caveat / licensing | Repository |
|---|---|---|---|
| HyperFrames official | hyperframes; hyperframes-core; hyperframes-animation; hyperframes-keyframes; hyperframes-cli; hyperframes-audio; hyperframes-registry; hyperframes-studio | 21 entries in checked manifest; repo Apache-2.0, dependency and asset licenses separate | https://github.com/heygen-com/hyperframes |
| Remotion official | remotion-best-practices; remotion-create; remotion-render; remotion-captions; remotion-multimedia; remotion-docs | 12 entries in checked Skills README; runtime pricing is separate from Skill availability | https://github.com/remotion-dev/skills |
| Anthropic official | skill-creator; webapp-testing | Repository contains mixed terms: many Apache-2.0 Skills; document Skills are source-available, not blanket Apache-2.0 | https://github.com/anthropics/skills |
| OpenAI official | playwright; speech | Individual Skill licenses; checked speech Skill defaults to a model now marked deprecated | https://github.com/openai/skills |
| K-Dense community | sympy and selected RDKit / Biopython / scientific-visualization guidance | Repository advertises 177 Skills; review individual Skill license fields and code before adopting | https://github.com/K-Dense-AI/scientific-agent-skills |
| Manim Community | Official API docs; manim-voiceover plugin | No first-party general-purpose Claude Skill verified in this review; plugin is not itself an agent Skill | https://docs.manim.community/en/stable/ |


## Sheet 1.6 `ReadMe`
**Contains:** the workbook's own guidance and caveats (rows 4-20; 16 topics). Row 2 states: *"Research date: 13 October 2026. This workbook is an editable planning artifact, not a benchmark, purchasing quote or deployed production system."* All rows reproduced verbatim:


| Topic | Guidance |
|---|---|
| Recommended baseline | HyperFrames + SVG/KaTeX/GSAP + Python science checks + selective Manim + FFmpeg. Remotion is the React alternative. Keep source data renderer-independent. |
| How to use | Edit blue Inputs cells. UnitCosts and Volumes recalculate. Sources are recorded alongside every raw input. USD before tax; no live currency conversion assumed. |
| Verified prices versus estimates | Provider token, voice, storage, CPU/RAM and Remotion prices are cited. Token budgets, render duration, staffing rates and setup effort are assumptions requiring pilot measurements. |
| Scientific approval | Every released lesson requires academic approval of the source/claim/script package and review of the entire final rendered lesson. Model agreement is not proof. |
| No benchmark claim | No candidate renderer, voice, locale or model was benchmarked or auditioned as part of this report. Run a representative pilot before committing. |
| Volumes comparison | 1, 100 and 1,000 videos are compared over the same editable accounting period. Fixed cost is not multiplied per video. Staff capacity is shown explicitly. |
| Excluded / additional costs | Taxes, rights purchases, playback product development, heavy bespoke 3D, source cleanup, additional languages, and engineering beyond the maintenance allowance require separate budgets. |
| Remotion option | Paid licensing is disabled in the HyperFrames baseline. Toggle only when the organization and usage need it. Confirm what counts as a billable partial render or still. |
| Storage / compute scope | Fargate is a US East rate example, not Mumbai pricing. Render time is an estimate. Storage assumes 2 GB per video for one month; prolonged retention compounds. |
| TTS scope | 8,000 narration characters plus 20% regeneration, regular ElevenLabs Multilingual v2 price. Character counts and pronunciation review differ by locale. |
| Assamese localization gate | Do not infer locale support from marketing. Verify the exact model API enum and perform native-speaker review. Sarvam marketing and model-specific lists were inconsistent. |
| Skills inventory | 40 proposed custom Skills are marked as not implemented. Existing Skills are curated references; do not install entire repositories without license/security review. |
| Deprecation gate | Check model availability and pinned Skill defaults before deployment. The checked OpenAI speech Skill used a TTS model whose model card was marked deprecated. |
| Implementation budget | $8,000 is an illustrative 320-hour initial build/template budget. This is not a promise of a mature system at that price. |
| Learning outcomes | Evaluate unprompted solving, delayed recall, transfer and confidence calibration. Completion/watch time is a secondary measure. |
| Source retention | Keep source URLs, retrieval dates, license snapshots, dependency lockfiles and benchmark receipts with the release manifest. |


### Cell comments in workbook 1
This workbook contains **no** cell comments.

---

# WORKBOOK 2: v2 engine cost model, `v2_engine_ExamLeaf_Video_Engine_Cost_Model.xlsx`

**Original file name:** `ExamLeaf_Video_Engine_Cost_Model.xlsx` (raw copy: `00_source/downloads/`).
**From:** message `10_ASSISTANT_video_engine_implementation_v2.md` (section 11 "Production costs: three architectures" quotes this workbook; the message links it as "Download the editable production-cost model").
**CSV folder:** `csv/v2_engine_ExamLeaf_Video_Engine_Cost_Model/` (14 files = 7 sheets x values/formulas).
**Sheets (tab order):** Inputs, Per Video, Volume Model, Decision, Measured Proof, Skill Backlog, Public Directory. (The CSV file names replace spaces with underscores: `Per_Video`, `Volume_Model`, ...)
**One-paragraph summary:** compares **three production architectures** per finished 10-minute video. Variable cost: **AI-heavy $158.98**, **Hybrid $34.34** (the recommended one), **Mostly self-hosted $37.32**; fixed $250 / $300 / $900 a month; set-up $5,000 / $10,000 / $16,000. At 1,000 videos the operating totals are **$159,226 / $34,643 / $38,215**. The decisive constraint is human review capacity (hybrid: 85 human minutes per video = about 1,417 hours = 8.85 FTE-months at 1,000 videos).

## Sheet 2.1 `Inputs`
**Contains:** 61 inputs (rows 6-66). Columns: A = input, B = value (editable), C = unit, D = **evidence class** (Published API tariff / Workload assumption / Assumption / Planning labour rate / Unquoted compute assumption / Unbenchmarked assumption / Published conditional licence / Unconfirmed accounting assumption / Illustrative setup budget / Optional allowance / Capacity assumption / Runway illustrative route), E = source or qualification. Banner: "USD, before tax. Published tariffs are inputs; workloads, rates of regeneration, labour and setup budgets are assumptions. No Higgsfield whole-lesson quote is claimed." The workbook also carries a cell comment on `B6`: "Planning assumptions and official source links are supplied in the source column."
**Formula logic:** none (constants).
**Inputs that no formula reads (descriptive only):** `B6` Lesson duration (600 s) and `B39` Optional Shorts per lesson (3). Changing them changes nothing; the Shorts package cost is driven by `B40:B43` (see Volume Model).


| Cell | Input | Value | Unit | Evidence class | Source / qualification |
|---|---|---|---|---|---|
| B6 | Lesson duration | 600 | seconds | Production assumption | User target ~10 minutes |
| B7 | Sonnet input | 120,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B8 | Sonnet output | 25,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B9 | Sonnet input tariff | 3 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B10 | Sonnet output tariff | 15 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B11 | Opus review input | 60,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B12 | Opus review output | 10,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B13 | Opus input tariff | 5 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B14 | Opus output tariff | 25 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B15 | Haiku input | 20,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B16 | Haiku output | 3,000 | tokens/video | Workload assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B17 | Haiku input tariff | 1 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B18 | Haiku output tariff | 5 | USD/million tokens | Published API tariff | https://platform.claude.com/docs/en/about-claude/pricing |
| B19 | LLM regeneration uplift | 0.3 | fraction | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B20 | Narration characters | 8,000 | characters/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B21 | Narration regeneration multiplier | 1.2 | multiple | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B22 | TTS tariff | 0.1 | USD/1,000 characters | Published API tariff | https://elevenlabs.io/pricing/api |
| B23 | Generated clip tariff | 0.1 | USD/second | Runway illustrative route | https://docs.dev.runwayml.com/guides/pricing/ \| Gemini Omni Flash listed rate; not Higgsfield quote; model features and surcharges vary |
| B24 | AI-heavy generated seconds | 600 | seconds/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B25 | AI-heavy clip attempt multiplier | 1.8 | multiple | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B26 | Hybrid generated seconds | 20 | seconds/video | Optional allowance | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. Zero is allowed; generation is not compulsory. |
| B27 | Hybrid clip attempt multiplier | 2 | multiple | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B28 | Generated still allowance | 0.2 | USD/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B29 | Academic reviewer rate | 20 | USD/hour | Planning labour rate | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B30 | Production QA rate | 15 | USD/hour | Planning labour rate | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B31 | Repair/editor rate | 20 | USD/hour | Planning labour rate | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B32 | Self-hosted GPU rate | 1 | USD/worker-hour | Unquoted compute assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B33 | Self-hosted model GPU time | 0.8 | worker-hour/video | Unbenchmarked assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B34 | Self-hosted voice GPU time | 0.05 | worker-hour/video | Unbenchmarked assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B35 | Hours per FTE-month | 160 | hours | Capacity assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B36 | Optional paid Remotion fee | 0.01 | USD/billable render | Published conditional licence | https://www.remotion.dev/docs/license/pricing |
| B37 | Remotion monthly minimum | 100 | USD/month | Published conditional licence | https://www.remotion.dev/docs/license/pricing |
| B38 | Billable renders per video | 20 | renders/video | Unconfirmed accounting assumption | Confirm contract definition; finished lesson may have multiple billed renders. |
| B39 | Optional Shorts per lesson | 3 | shorts | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B40 | Shorts total additional TTS chars | 1,800 | characters | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B41 | Shorts additional LLM | 0.2 | USD/lesson | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B42 | Shorts additional rendering | 0.15 | USD/lesson | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B43 | Shorts total editorial review | 15 | minutes/lesson | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B44 | Accounting period | 1 | months | Assumption | Same one-month project period for 1/100/1000 comparison; change monthly overhead allocation for longer programmes. |
| B45 | AI-heavy academic review | 75 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B46 | Hybrid academic review | 45 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B47 | Self-host academic review | 60 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B48 | AI-heavy production QA | 30 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B49 | Hybrid production QA | 20 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B50 | Self-host production QA | 20 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B51 | AI-heavy repairs | 45 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B52 | Hybrid repairs | 20 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B53 | Self-host repairs | 30 | minutes/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B54 | AI-heavy monthly fixed | 250 | USD/month | Assumption | Storage/tools/orchestration and modest maintenance allowance; no viewer delivery or full engineering team. |
| B55 | Hybrid monthly fixed | 300 | USD/month | Assumption | Storage/tools/orchestration and modest maintenance allowance; no viewer delivery or full engineering team. |
| B56 | Self-host monthly fixed | 900 | USD/month | Assumption | Higher administration/maintenance allowance; GPU usage is charged separately above, not an always-on fleet. |
| B57 | AI-heavy setup | 5,000 | USD one-time | Illustrative setup budget | Initial integration/templates only; not quotation or complete curriculum production. |
| B58 | Hybrid setup | 10,000 | USD one-time | Illustrative setup budget | Initial engine/templates only; actual authoring and specialist asset requirements may exceed this. |
| B59 | Self-host setup | 16,000 | USD one-time | Illustrative setup budget | Serving/integration/templates only; no owned GPU purchase included. |
| B60 | AI-heavy encode | 0.3 | USD/video | Unbenchmarked cloud allowance | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B61 | Hybrid encode | 0.5 | USD/video | Unbenchmarked cloud allowance | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B62 | Self-host encode | 0.5 | USD/video | Unbenchmarked cloud allowance | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B63 | AI-heavy alignment/audio | 0.1 | USD/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B64 | Hybrid alignment/audio | 0.1 | USD/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B65 | Self-host alignment/audio | 0.05 | USD/video | Assumption | ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload. |
| B66 | Working asset storage | 0.2 | USD/video per model period | Assumption | Working assets; audience streaming/egress and long-term retention excluded. |


**Model labels.** Message 10 states the LLM workload as "Sonnet 4.6: 120,000 input and 25,000 output tokens; Opus 4.6 review: 60,000 and 10,000; Haiku 4.5 routing: 20,000 and 3,000; 30% regeneration allowance", at the tariffs in rows 9-10 (Sonnet $3/$15), 13-14 (Opus $5/$25) and 17-18 (Haiku $1/$5) per million tokens. These labels and prices differ from workbook 1 (which labels Haiku/Sonnet/Opus "5.5" at $0.10/$0.50, $2/$10, $4/$20 and adds a `gpt-6.1-sol` review). Both are as of 13 October 2026.

## Sheet 2.2 `Per Video`
**Contains:** cost per finished 10-minute video for the three architectures (columns B = AI-heavy, C = Hybrid, D = Mostly self-hosted), rows 5-20. Footer: "Quality is not assumed equal. AI-heavy scenes can fail scientific requirements regardless of spend. Self-hosted labour and GPU time are unmeasured scenarios. Zero generated clips is the default unless their instructional value is approved."
**Editable cells:** none (all formulas on Inputs).


| Row | Cost category (USD/video unless noted) | AI-heavy | Hybrid | Mostly self-hosted | Formula logic in plain English |
|---|---|---|---|---|---|
| 5 | LLM reasoning / independent review | 1.716 | 1.716 | 1.515 | AI-heavy and Hybrid: ((Sonnet in x tariff + Sonnet out x tariff + Opus review in x tariff + out x tariff + Haiku in x tariff + out x tariff) / 1,000,000) x (1 + 30% regeneration uplift)   [Inputs B7..B19]. Self-hosted: self-hosted GPU $/h x model GPU hours (1 x 0.8) + (Opus review tokens x tariffs / 1,000,000) x 1.3, i.e. the Sonnet drafting and Haiku routing are replaced by GPU time while the independent Opus review stays on the API |
| 6 | Narration generation | 0.96 | 0.96 | 0.05 | AI-heavy and Hybrid: narration characters x regeneration multiplier x TTS tariff / 1000 = 8,000 x 1.2 x $0.10 / 1000. Self-hosted: GPU $/h x voice GPU hours = 1 x 0.05   [Inputs B20..B22, B32, B34] |
| 7 | Generated video clips | 108 | 4 | 0 | AI-heavy: generated seconds (600) x clip tariff ($0.10/s) x attempt multiplier (1.8). Hybrid: 20 s x $0.10 x 2. Self-hosted: 0   [Inputs B23..B27] |
| 8 | Generated stills | 0.2 | 0.2 | 0 | Generated-still allowance $0.20 (AI-heavy, Hybrid); 0 for Self-hosted   [Inputs B28] |
| 9 | Encoding/rendering | 0.3 | 0.5 | 0.5 | Flat encoding/rendering allowances $0.30 / $0.50 / $0.50   [Inputs B60..B62] |
| 10 | Alignment/audio allowance | 0.1 | 0.1 | 0.05 | Flat alignment/audio allowances $0.10 / $0.10 / $0.05   [Inputs B63..B65] |
| 11 | Working storage | 0.2 | 0.2 | 0.2 | Working-asset storage $0.20 for all three   [Inputs B66] |
| 12 | Machine subtotal | 111.476 | 7.676 | 2.315 | SUM of rows 5-11 (machine subtotal) |
| 13 | Academic review | 25 | 15 | 20 | Academic review minutes (75 / 45 / 60) / 60 x academic rate $20/h   [Inputs B45..B47, B29] |
| 14 | Production QA | 7.5 | 5 | 5 | Production QA minutes (30 / 20 / 20) / 60 x QA rate $15/h   [Inputs B48..B50, B30] |
| 15 | Repairs / editing | 15 | 6.6667 | 10 | Repair/editing minutes (45 / 20 / 30) / 60 x repair rate $20/h   [Inputs B51..B53, B31] |
| 16 | Human subtotal | 47.5 | 26.6667 | 35 | SUM of rows 13-15 (human subtotal) |
| 17 | TOTAL VARIABLE COST | 158.976 | 34.3427 | 37.315 | Machine subtotal + human subtotal (total variable cost per video) |
| 18 | Monthly fixed allowance | 250 | 300 | 900 | Monthly fixed allowance $250 / $300 / $900   [Inputs B54..B56] |
| 19 | One-time setup | 5,000 | 10,000 | 16,000 | One-time setup $5,000 / $10,000 / $16,000   [Inputs B57..B59] |
| 20 | Human minutes/video | 150 | 85 | 110 | Academic + QA + repair minutes per video (150 / 85 / 110) |


**Reading the table.** The AI-heavy architecture is dominated by $108 of generated video clips (600 s x $0.10 x 1.8 attempts) and still needs 150 human minutes. Hybrid keeps only an optional 20 generated seconds ($4) and the most automation of review work. Self-hosted removes almost all API cost ($2.32 machine) but assumes 110 human minutes and unbenchmarked GPU time. **Machine cost is the small number; human minutes decide the total.**

## Sheet 2.3 `Volume Model`
**Contains:** "VOLUME COMPARISON | same one-month operating period": 3 architectures x 3 volumes (rows 5-13) plus a capacity/add-on block (rows 16-21).
**Editable cells:** none (the volumes 1/100/1000 in column B of rows 5-13 are constants and can be edited).


| Row | Architecture | Videos | Variable USD/video | Variable USD | Fixed USD | Operating total USD | Average USD/video | Setup USD | Total with setup USD |
|---|---|---|---|---|---|---|---|---|---|
| 5 | AI-heavy | 1 | 158.976 | 158.976 | 250 | 408.976 | 408.976 | 5,000 | 5,408.98 |
| 6 | AI-heavy | 100 | 158.976 | 15,897.6 | 250 | 16,147.6 | 161.476 | 5,000 | 21,147.6 |
| 7 | AI-heavy | 1,000 | 158.976 | 158,976 | 250 | 159,226 | 159.226 | 5,000 | 164,226 |
| 8 | Hybrid | 1 | 34.3427 | 34.3427 | 300 | 334.3427 | 334.3427 | 10,000 | 10,334.34 |
| 9 | Hybrid | 100 | 34.3427 | 3,434.27 | 300 | 3,734.27 | 37.3427 | 10,000 | 13,734.27 |
| 10 | Hybrid | 1,000 | 34.3427 | 34,342.67 | 300 | 34,642.67 | 34.6427 | 10,000 | 44,642.67 |
| 11 | Self-hosted | 1 | 37.315 | 37.315 | 900 | 937.315 | 937.315 | 16,000 | 16,937.31 |
| 12 | Self-hosted | 100 | 37.315 | 3,731.5 | 900 | 4,631.5 | 46.315 | 16,000 | 20,631.5 |
| 13 | Self-hosted | 1,000 | 37.315 | 37,315 | 900 | 38,215 | 38.215 | 16,000 | 54,215 |


**Formula logic.** `D = Videos x Variable USD/video` (Per Video row 17); `E` Fixed = monthly fixed allowance (Per Video row 18) x accounting-period months (`Inputs!B44`); `F` Operating total = D + E; `G` Average USD/video = F / Videos; `H` Setup = Per Video row 19; `I` Total with setup = F + H.

**Capacity / add-on block (rows 16-21):**


| Cell | Metric | Value | Unit | Qualification (column D) | Formula logic |
|---|---|---|---|---|---|
| B17 | Hybrid reviewer hours at 1,000 | 1,416.67 | hours | Includes academic, QA and repair time | Per Video C20 (85 human minutes) x 1,000 videos / 60. The hybrid architecture at 1,000 videos |
| B18 | Hybrid FTE equivalent at 1,000 | 8.8542 | FTE-month | Not a hiring promise; workload allocation | Reviewer hours / hours per FTE-month (`Inputs!B35` = 160). Described as 'Not a hiring promise; workload allocation' |
| B19 | Optional three-Short package | 4.316 | USD/lesson | Additional cost for total three reviewed Shorts | Shorts additional LLM $0.20 + (1,800 chars x 1.2 x $0.10 / 1000 = $0.216) + additional rendering $0.15 + 15 editorial-review minutes / 60 x QA rate $15 (= $3.75)   [Inputs B41, B40, B21, B22, B42, B43, B30]. For 'total three reviewed Shorts' |
| B20 | Optional Remotion paid tier at 1,000 | 200 | USD/month | Only if licence applies; render count needs confirmation | MAX(Remotion monthly minimum $100 x period, 1,000 videos x 20 billable renders x $0.01)   [Inputs B37, B44, B38, B36]. Only if the licence applies; render count needs confirmation |
| B21 | Hybrid with zero generated clips: variable | 30.3427 | USD/video | Removes only optional generation allowance | Hybrid total variable (Per Video C17) minus the hybrid generated-clips line (Per Video C7). Removes only the optional generation allowance |


**Key outputs (message 10 quotes these).** Operating totals at 1 / 100 / 1,000 videos: AI-heavy **$408.98 / $16,147.60 / $159,226**; Hybrid **$334.34 / $3,734.27 / $34,642.67**; Self-hosted **$937.32 / $4,631.50 / $38,215**. Including setup at 1,000: AI-heavy $164,226, Hybrid **$44,642.67**, Self-hosted $54,215. Average cost per video at 1,000: $159.23 / $34.64 / $38.22.

## Sheet 2.4 `Decision`
**Contains:** a small dashboard (rows 5-8) with Machine USD/video, Human USD/video and Operating USD at 1,000 for each architecture, plus the banner text.
**Editable cells:** none.


| Architecture | Machine USD/video | Human USD/video | Operating USD @ 1,000 |
|---|---|---|---|
| AI-heavy | 111.476 | 47.5 | 159,226 |
| Hybrid | 7.676 | 26.6667 | 34,642.67 |
| Self-hosted | 2.315 | 35 | 38,215 |


**Formula logic.** Machine = `Per Video` row 12; Human = `Per Video` row 16; Operating @1,000 = `Volume Model` F7 / F10 / F13.

**Banner text (verbatim):** "Recommended architecture: deterministic scientific state + reusable SVG/web scenes + selective specialist rendering. HyperFrames is the production candidate; the shipped proof uses native SVG/CairoSVG/FFmpeg, not HyperFrames."

**Footer (verbatim):** "Do not confuse machine expense with total production cost. The prototype has no separate cloud invoice; its measured local wall time is not a cloud price or a forecast for 10-minute narrated lessons. Prices checked 13 October 2026. Taxes, viewer delivery, legal costs, hardware purchase and royalties are outside this production model."

## Sheet 2.5 `Measured Proof`
**Contains:** the **only measured (not assumed) data in any of the four workbooks**: eight 30-second silent fixture renders from the working prototype described in message 10 (four subjects x two aspect ratios). Columns: Fixture, Aspect, Duration seconds, Frames, Render wall seconds, Width, Height, Status. No formulas.


| Fixture | Aspect | Duration seconds | Frames | Render wall seconds | Width | Height | Status |
|---|---|---|---|---|---|---|---|
| biology_genetics | 16:9 | 30 | 720 | 27.425 | 1280 | 720 | Render passed; audio and expert release pending |
| biology_genetics | 9:16 | 30 | 720 | 27.951 | 720 | 1280 | Render passed; audio and expert release pending |
| chemistry_balance | 16:9 | 30 | 720 | 28.67 | 1280 | 720 | Render passed; audio and expert release pending |
| chemistry_balance | 9:16 | 30 | 720 | 29.375 | 720 | 1280 | Render passed; audio and expert release pending |
| mathematics_chain | 16:9 | 30 | 720 | 27.372 | 1280 | 720 | Render passed; audio and expert release pending |
| mathematics_chain | 9:16 | 30 | 720 | 27.576 | 720 | 1280 | Render passed; audio and expert release pending |
| physics_rc | 16:9 | 30 | 720 | 27.338 | 1280 | 720 | Render passed; audio and expert release pending |
| physics_rc | 9:16 | 30 | 720 | 28.102 | 720 | 1280 | Render passed; audio and expert release pending |


Render wall time ranges from 27.338 s to 29.375 s per 30-second clip (mean 27.98 s). Footer (verbatim): "Eight silent 30s files; two render workers. Simple fixed models, not full curriculum pilots. Scientific checks are bounded; no teacher approval or student study. Current test log: 56 passed. Separate live speech audition is recorded outside these render metrics."

**Do not use these as a render-cost benchmark.** They are local CPU wall times for simple fixed 2D models (no narration audio, no expert release), not a cloud price and not a forecast for 10-minute narrated lessons (the Decision sheet says so explicitly). Replace with a real pilot benchmark (see `INSTRUCTIONS_how_to_use_cost_models.md`).

## Sheet 2.6 `Skill Backlog`
**Contains:** the **32 custom Skill drafts** of the v2 implementation (columns Skill, Priority, Purpose, Inputs, Outputs, Status, Cost/performance). It is the engine's Skill scope, with a per-Skill cost/performance note (e.g. "Local CPU; zero model calls", "Pay per generated character; regenerate only changed segments"). No formulas. Status values distinguish what was actually tested from what is only proposed: *Implemented and tested for four bounded fixtures* (`examleaf-svg-scenes`), *tested* local pieces (science-math chain-rule validator, physics RC cross-check, chemistry H2/O2/H2O counts, biology single-locus probability, batch/cache/atomic output, cents ledger, release policy tests), *Packaged remote adapter unimplemented* (`examleaf-voice-synthesis`), and *Proposed agent workflow; not model-evaluated* for the rest. Cross-reference: `06_skills_library/`.


| Skill | Priority | Status | Cost / performance note |
|---|---|---|---|
| examleaf-source-ingest | P0 | Native-text CLI tested on synthetic PDF; textbook/syllabus ingestion not end-to-end validated | Local CPU; zero model calls |
| examleaf-curriculum-map | P0 | Proposed agent workflow; not model-evaluated | Small retrieval/model job; cache by syllabus hash |
| examleaf-claim-research | P0 | Proposed agent workflow; not model-evaluated | Research token budget; retrieve relevant spans, not whole books repeatedly |
| examleaf-lesson-plan | P0 | Proposed agent workflow; not model-evaluated | One structured planning call; no media generation |
| examleaf-super-teacher | P0 | Proposed agent workflow; not model-evaluated | One draft plus bounded repair; not a fresh long prompt per scene |
| examleaf-analogy-humour | P0 | Proposed agent workflow; not model-evaluated | Small editorial pass; no separate generative clip required |
| examleaf-interaction-design | P0 | Proposed agent workflow; not model-evaluated | No compulsory API calls; validated data |
| examleaf-science-math | P0 | Bounded chain-rule validator tested; not a general theorem prover | Local computation; expert checks remain |
| examleaf-science-physics | P0 | RC analytic/SciPy cross-check tested; broader models proposed | Local CPU; cache solution by parameters |
| examleaf-science-chemistry | P0 | Bounded H2/O2/H2O count checks tested; mechanisms not implemented | Local RDKit; expert review for chemistry reasoning |
| examleaf-science-biology | P0 | Single-locus probability model tested; anatomy/process validators proposed | Mostly local rules plus expert review |
| examleaf-storyboard-route | P0 | Proposed agent workflow; not model-evaluated | One bounded planning pass; cheap deterministic routing |
| examleaf-svg-scenes | P0 | Implemented and tested for four bounded fixtures | CPU; actual preview benchmarks provided |
| examleaf-manim-scenes | P1 | Proposed agent workflow; not model-evaluated | Specialist render cost; reuse approved inserts |
| examleaf-web-composition | P1 | Proposed agent workflow; not model-evaluated | Renderer infrastructure; Remotion eligibility may add licensing |
| examleaf-blender-scenes | P2 | Proposed agent workflow; not model-evaluated | High setup/render cost; opt-in only |
| examleaf-molecule-scenes | P1 | Proposed agent workflow; not model-evaluated | Local 2D cheap; 3D only when useful |
| examleaf-biology-scenes | P1 | Proposed agent workflow; not model-evaluated | Asset authoring dominates initial cost |
| examleaf-voice-direction | P0 | Proposed agent workflow; not model-evaluated | No required media call; reduces repeat synthesis |
| examleaf-voice-synthesis | P0 | Packaged remote adapter unimplemented; standalone live speech probe separate | Pay per generated character; regenerate only changed segments |
| examleaf-alignment-localize | P0 | Proposed agent workflow; not model-evaluated | Alignment plus localization review cost; TTS regenerated only per changed language |
| examleaf-render-batch | P0 | Local batch/cache/atomic output tested; distributed queue proposed | Actual CPU measurements; local proof not cloud-priced |
| examleaf-visual-qa | P0 | Proposed agent workflow; not model-evaluated | Automated preflight plus human visual review |
| examleaf-audio-caption-qa | P0 | Proposed agent workflow; not model-evaluated | Small compute; full-listen time budgeted |
| examleaf-release-review | P0 | Local policy tests pass; identity-authenticated approval service not implemented | Mandatory reviewer time; not replaced by LLM vote |
| examleaf-reel-repurpose | P0 | Proposed agent workflow; not model-evaluated | Reuse expensive assets; new editorial approval still required |
| examleaf-thumbnail-package | P1 | Proposed agent workflow; not model-evaluated | Near-zero render cost; optional generated illustration capped |
| examleaf-observability-cost | P0 | Local cents ledger tested; provider reconciliation proposed | Local metrics; avoid logging confidential prompts |
| examleaf-skills-security | P0 | Proposed agent workflow; not model-evaluated | One-time audit plus upgrade revalidation; not full automatic security proof |
| examleaf-learning-evaluation | P1 | Proposed agent workflow; not model-evaluated | Human research time; no emotion surveillance |
| examleaf-asset-library | P0 | Proposed agent workflow; not model-evaluated | High first-use effort; very low amortized reuse cost |
| examleaf-selective-generation | P1 | Proposed agent workflow; not model-evaluated | Spend bounded per scene; zero generated seconds is allowed |


Count: 32 Skills (P0 = 24, P1 = 7, P2 = 1).


## Sheet 2.7 `Public Directory`
**Contains:** the **21-row public Skills / tools / services directory** (columns Solution, Type, Origin, Use, Licence / terms, Verification, Source URL, Snapshot): Higgsfield (skills, CLI, MCP, API), Remotion skills, HyperFrames, ElevenLabs skills, Anthropic skills, Blender MCP, Manim community skills, K-Dense scientific skills, Playwright MCP, skills.sh, MCP registry, Claude plugin marketplace, Runway, Pika, Luma, Kling/Seedance/Veo, Motion Canvas, Blender. Every row's Verification column is "Documentation inspected; not installed or executed" (two exceptions: playwright-mcp "Discovery/documentation reference; not executed as MCP"; runway "Read-only authentication tested; speech job separately recorded; generative video not tested"). It prices nothing itself but carries the licence/cost gates that feed the engine cost model (e.g. "Remotion engine has conditional commercial licence"; "Pika: API Club membership plus usage"; "Luma: current final rate not resolved"; "Higgsfield: no verified whole-lesson quote"). No formulas.


| Solution | Type | Origin | Licence / terms | Verification |
|---|---|---|---|---|
| higgsfield-skills | Agent Skills | Official Higgsfield | Repository MIT; service and model terms separate | Documentation inspected; not installed or executed |
| higgsfield-cli | CLI | Official Higgsfield | CLI MIT; SaaS billing/rights separate | Documentation inspected; not installed or executed |
| higgsfield-mcp | MCP server | Official Higgsfield | Hosted service terms; subscription credits; Unlimited web mode not presumed to apply | Documentation inspected; not installed or executed |
| higgsfield-api | HTTP API | Official Higgsfield | Separate pay-per-generation API economics; no verified whole-lesson quote | Documentation inspected; not installed or executed |
| remotion-skills | Agent Skills | Official Remotion | Review Skill licence separately; Remotion engine has conditional commercial licence | Documentation inspected; not installed or executed |
| hyperframes | Engine + Agent Skills | Official HeyGen | Apache-2.0 engine; inspect optional runtime/assets separately | Documentation inspected; not installed or executed |
| elevenlabs-skills | Agent Skills | Official ElevenLabs | MIT Skills; commercial voice rights and API terms separate | Documentation inspected; not installed or executed |
| anthropic-skills | Agent Skills + marketplace | Official Anthropic | Many Apache-2.0; docx/pdf/pptx/xlsx source-available under distinct terms | Documentation inspected; not installed or executed |
| blender-mcp | MCP server + Blender add-on | Community; NOT Blender Foundation | MIT bridge; Blender GPL; imported asset licences separate | Documentation inspected; not installed or executed |
| manim-community-skills | Agent Skills | Community | MIT Skill repository; Manim Community MIT | Documentation inspected; not installed or executed |
| scientific-agent-skills | Agent Skills | Community K-Dense | Check individual Skill licence/dependencies; no blanket asset clearance | Documentation inspected; not installed or executed |
| playwright-mcp | MCP server | Official Microsoft | Apache-2.0 repository; browser separately distributed | Discovery/documentation reference; not executed as MCP |
| skills-sh | Skill directory | Vercel ecosystem | Per referenced repository | Documentation inspected; not installed or executed |
| mcp-registry | MCP directory | MCP ecosystem | Per service/server | Documentation inspected; not installed or executed |
| claude-plugin-marketplace | Plugin marketplace | Official Anthropic | Per plugin | Documentation inspected; not installed or executed |
| runway | Hosted APIs + connected MCP | Official Runway | Hosted API/voice/model terms separate; account capability gating | Read-only authentication tested; speech job separately recorded; generative video not tested |
| pika | Hosted generation API | Official Pika | API Club membership plus usage; review model/output terms | Documentation inspected; not installed or executed |
| luma | Hosted generation API | Official Luma | Service terms; all-in current quote unresolved | Official API existence/docs checked; pricing unresolved |
| kling-seedance-veo | Models behind provider APIs | Multiple model owners/providers | Provider-specific prices/access/terms; aggregator access is not direct-owner API access | Documentation inspected; not installed or executed |
| motion-canvas | Animation engine | Official project | MIT | Documentation inspected; not installed or executed |
| blender | 3D application + Python API | Blender Foundation | GPL software; output artwork not automatically GPL; third-party models separate | Documentation inspected; not installed or executed |


Full `Use`, `Source URL` and `Snapshot` text: `csv/v2_engine_ExamLeaf_Video_Engine_Cost_Model/ExamLeaf_Video_Engine_Cost_Model__Public_Directory__values.csv`.


### Cell comments in workbook 2
62 threaded comments, all on `Inputs!B6:B66`. They repeat the "Evidence class | Source / qualification" strings of columns D and E (so nothing in them is missing from the table above). The one comment that is not a repeat is `Inputs!B6`: *"Planning assumptions and official source links are supplied in the source column."* The standard text of the assumption rows is: **"ExamLeaf planning assumption; not a quote or benchmark. Replace with measured workload."**

---

# WORKBOOK 3: narration cost model, `narration_ExamLeaf_Narration_Cost_Model.xlsx`

**Original file name:** `ExamLeaf_Narration_Cost_Model.xlsx` (raw copy: `00_source/downloads/`).
**From:** message `12_ASSISTANT_narration_system.md` (section 13 "Costs for 1, 100, and 1,000 ten-minute videos" quotes this workbook; the message links it as "Download the editable narration cost model"). The narration pack (`ExamLeaf_Narration_System.zip`) also contains `docs/Costs_and_Methods.md`, which restates the same tables.
**CSV folder:** `csv/narration_ExamLeaf_Narration_Cost_Model/` (12 files = 6 sheets x values/formulas).
**Sheets (tab order):** Summary, Inputs, Methods, Provider Tariffs, Skills, Sources. (CSV: `Provider_Tariffs`.)
**One-paragraph summary:** prices **only the narration sub-system** (script-direction allowance, synthesis, audio QA, editing, modeled human work) for one 10-minute video (8.5 minutes of speech, 7,800 characters) under **five production methods**. Premium commercial TTS costs **$12.50 per video** (about $12,599 at 1,000 videos); the dominant cost is human audio review/editing (**583 hours at 1,000 videos**), not synthesis (about $0.94). Scope warning on the Summary sheet: "Narration subsystem only; not whole-video production."

## Sheet 3.1 `Summary`
**Contains:** the five methods priced at 1 / 100 / 1,000 videos (rows 6-10), setup and review sensitivities (rows 13-15), a clustered **bar chart "Operating cost by volume - USD"** (series = 1 / 100 / 1,000 videos for the five methods, from `Summary!A6:D10`), and four standing caveats (rows 16-19).
**Editable cells:** none (all formulas on Methods/Inputs).


| Row | Method | 1 video | 100 videos | 1,000 videos | Variable / video | Monthly fixed | Hours at 1,000 |
|---|---|---|---|---|---|---|---|
| 6 | Premium commercial TTS | 112.4993 | 1,349.93 | 12,599.33 | 12.4993 | 100 | 583.3333 |
| 7 | Primarily self-hosted | 314.752 | 1,775.2 | 15,052 | 14.752 | 300 | 750 |
| 8 | Human recorded | 142.3967 | 4,339.67 | 42,496.67 | 42.3967 | 100 | 1,666.67 |
| 9 | Human performance + STS | 159.8707 | 3,612.07 | 34,995.67 | 34.8707 | 125 | 1,333.33 |
| 10 | Hybrid: 80% TTS / 20% performed | 167.0569 | 1,855.69 | 17,206.93 | 17.0569 | 150 | 733.3333 |


**Formula logic.** For method *m* (row 6-10 of `Methods`): `1 video = Variable/video + Monthly fixed`; `100 videos = Variable x 100 + Fixed`; `1,000 videos = Variable x 1000 + Fixed`; `Variable / video` = Methods!K; `Monthly fixed` = Methods!H; `Hours at 1,000` = Methods!L (human minutes per video) x 1000 / 60. One-month accounting window for all volumes: fixed cost is not multiplied per video.

| Row | Item | Value | Formula logic |
|---|---|---:|---|
| 13 | Add initial subsystem setup separately | 4,000 | `Inputs!B21` (illustrative one-time reserve; **not** in the operating totals) |
| 14 | Premium / 1,000 including initial setup | 16,599.33 | Premium 1,000-video total (D6) + setup |
| 15 | Premium / 1,000 with review time doubled | 20,932.67 | D6 + review minutes (Methods!E6 = 25) / 60 x academic reviewer rate ($20) x 1,000, i.e. adds another $8,333.33 |

**Caveats printed on the sheet (rows 16-19, verbatim):**

* *All variants:* "Assumptions, not vendor quotes, controlled provider benchmarks, or guaranteed quality equivalence."
* *Accounting:* "Do not add these audio-review costs twice if already included in your full video-production budget."
* *Excluded:* "Tax, voice buyouts, extended licensing, audience streaming, full animation, broad academic research and extra localization."
* *Scaling:* "One locale/version per case. A second language requires new performance, QA and timeline verification."

## Sheet 3.2 `Inputs`
**Contains:** 22 narration assumptions (rows 6-27). Columns A = assumption, B = value (editable, blue), C = unit, D = source (URL or "Planning assumption"), E = caution. Banner: "USD, before tax | Editable inputs in blue. Reference tariffs and workload assumptions are explicitly separate. Checked 13 October 2026." Every `B` cell also carries a cell comment "Source: ... Checked: 13 October 2026. <caution>" (identical to columns D-E; listed below).
**Formula logic:** none (constants).
**Inputs that no formula reads (descriptive only):** `B6` Media duration (10 min) and `B8` Spoken word budget (1,200 words). The cost basis is the **active spoken duration `B7` (8.5 min)** and the **canonical transcript length `B9` (7,800 characters)**.


| Cell | Assumption | Value | Unit | Source | Caution |
|---|---|---|---|---|---|
| B6 | Media duration | 10 | minutes | Planning assumption | Not all media time is spoken. |
| B7 | Active spoken duration | 8.5 | minutes | Planning assumption | Narration-only cost basis; response windows are inserted locally. |
| B8 | Spoken word budget | 1,200 | words | Planning assumption | Pacing varies with complexity and language. |
| B9 | Canonical transcript length | 7,800 | characters | Planning assumption | Count actual final provider input in deployment. |
| B10 | Generation/retry allowance | 0.2 | fraction | Planning assumption | Extra generated audio, not a guarantee of acceptance. |
| B11 | Premium TTS reference tariff | 0.1 | USD / 1,000 characters | https://elevenlabs.io/pricing/api | v2/v3 published reference used for budget; NOT a verified Eleven v4 quote. |
| B12 | Speech-to-speech tariff | 0.12 | USD / generated minute | https://elevenlabs.io/pricing/api | Confirm selected account/model; reference usage price. |
| B13 | LLM writing/direction allowance | 0.6 | USD / video | Planning assumption | Incremental narration editing/direction only; not whole academic research. |
| B14 | ASR/alignment/automatic QA allowance | 0.08 | USD / video | Planning assumption | Service/compute budget, not a provider price guarantee. |
| B15 | Storage/export allowance | 0.05 | USD / video | Planning assumption | Excludes audience streaming and indefinite storage. |
| B16 | Academic audio review rate | 20 | USD / hour | Planning assumption | Obtain actual native subject-reviewer quotations. |
| B17 | Audio editing rate | 15 | USD / hour | Planning assumption | Labour assumption, not a market survey. |
| B18 | Performer rate | 30 | USD / hour | Planning assumption | Illustrative; licensing/buyout fees require a separate agreement. |
| B19 | GPU price | 0.8 | USD / compute hour | Planning assumption | No GPU benchmark or supplier quote obtained. |
| B20 | GPU real-time factor | 2 | compute sec / generated sec | Planning assumption | Unbenchmarked; 2 means slower than real time. |
| B21 | Initial subsystem setup | 4,000 | USD one-time | Planning assumption | Optional separate initial implementation reserve; not in operating totals. |
| B22 | Gemini input token estimate | 2,500 | tokens / script | Planning assumption | Includes direction; actual billed token count governs. |
| B23 | Gemini audio tokens / sec | 25 | tokens / second | https://ai.google.dev/gemini-api/docs/pricing | Model pricing calculation convention; verify usage records. |
| B24 | Gemini 3.8 current input | 0.5 | USD / million input tokens | https://ai.google.dev/gemini-api/docs/pricing | Before scheduled 2027-01-01 rate change. |
| B25 | Gemini 3.8 current output | 9 | USD / million audio tokens | https://ai.google.dev/gemini-api/docs/pricing | Before scheduled 2027-01-01 rate change. |
| B26 | Gemini 3.8 future input | 1 | USD / million input tokens | https://ai.google.dev/gemini-api/docs/pricing | Scheduled from 2027-01-01; recheck before use. |
| B27 | Gemini 3.8 future output | 18 | USD / million audio tokens | https://ai.google.dev/gemini-api/docs/pricing | Scheduled from 2027-01-01; recheck before use. |


## Sheet 3.3 `Methods`
**Contains:** the five production methods as rows 6-10. Columns A-H are the **editable per-method inputs**: TTS fraction (B), Record hours (C), STS (speech-to-speech) fraction (D), Review min (E), Edit min (F), GPU flag (G), Fixed / month (H). Columns I-L are formulas. Banner: "Operating assumptions for mature workflows. Novel STEM terms, native-language validation and first-use performances can require additional work."


| Method | TTS fraction | Record hours | STS fraction | Review min | Edit min | GPU flag | Fixed / month | Machine / video | Human / video | Variable / video | Human min / video |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Premium commercial TTS | 1 | 0 | 0 | 25 | 10 | 0 | 100 | 1.666 | 10.8333 | 12.4993 | 35 |
| Primarily self-hosted | 0 | 0 | 0 | 30 | 15 | 1 | 300 | 1.002 | 13.75 | 14.752 | 45 |
| Human recorded | 0 | 1 | 0 | 20 | 20 | 0 | 100 | 0.73 | 41.6667 | 42.3967 | 100 |
| Human performance + STS | 0 | 0.75 | 1 | 20 | 15 | 0 | 125 | 1.954 | 32.9167 | 34.8707 | 80 |
| Hybrid: 80% TTS / 20% performed | 0.8 | 0.15 | 0.2 | 25 | 10 | 0 | 150 | 1.7236 | 15.3333 | 17.0569 | 44 |


**Formula logic (identical in each row, with that row's own inputs):**

* **Machine / video (I)** = `(LLM writing/direction $0.60 + ASR/alignment/QA $0.08 + storage/export $0.05)` + `TTS fraction x (7,800 characters x (1 + 20% retry) / 1000 x $0.10)` + `STS fraction x (8.5 min x (1 + 20%) x $0.12/min)` + `GPU flag x (8.5 min x 60 x (1 + 20%) x real-time factor 2 / 3600 x $0.80/GPU-hour)`. The three fixed allowances sum to $0.73; the TTS term is $0.936; the STS term is $1.224; the GPU term is $0.272.   [Inputs B13..B15, B9..B12, B7, B19, B20]
* **Human / video (J)** = `Record hours x performer rate $30` + `Review minutes / 60 x academic reviewer rate $20` + `Edit minutes / 60 x audio editor rate $15`.   [Inputs B16..B18]
* **Variable / video (K)** = I + J.
* **Human min / video (L)** = `Record hours x 60 + Review min + Edit min` (so "Human recorded" is 60 + 20 + 20 = 100 minutes).

**Reading the table.** Premium commercial TTS: $1.666 machine + $10.83 human = **$12.499**; 35 human minutes. Primarily self-hosted: $1.002 machine (no TTS fee, GPU $0.272) + $13.75 human; 45 minutes. Human recorded: $0.73 + $41.67; 100 minutes. Human performance + STS: $1.954 + $32.92; 80 minutes. Hybrid (80% TTS / 20% performed): $1.7236 + $15.33; 44 minutes.

## Sheet 3.4 `Provider Tariffs`
**Contains:** 12 provider/method tariff references (rows 6-17; columns Provider / method, Pricing basis, Example synthesis cost, Scope, Lifecycle / limit, Source). Banner: "Public rates can change. Model, plan, minimum spend and licensing are not interchangeable. Legacy model prices must not drive a new launch." Only the "Example synthesis cost" cells are formulas.


| Row | Provider / method | Pricing basis | Example synthesis cost (USD) | Scope | Lifecycle / limit | Formula logic |
|---|---|---|---|---|---|---|
| 6 | ElevenLabs v2/v3 reference | $0.10 / 1,000 chars | 0.936 | 9,360 generated characters | Reference budget, not verified v4 tariff | `Inputs!B9 x (1 + B10) / 1000 x B11` = 7,800 x 1.2 / 1000 x $0.10 |
| 7 | Eleven v4 | Account/model quote required | TBD | Latest expressive audition candidate | Do not infer from v2/v3 or approximate $/minute marketing | text / constant (no formula) |
| 8 | Gemini 3.8 Flash TTS — now | $0.50 input / $9 output per million | 0.1392 | 612 generated seconds + estimated text | Current through 2026-12-31 per published schedule | `(active minutes x 60 x 25 tokens/s x current output $9 + 2,500 input tokens x current input $0.50) x (1 + retry) / 1,000,000` = (8.5 x 60 x 25 x 9 + 2,500 x 0.5) x 1.2 / 1e6 |
| 9 | Gemini 3.8 Flash TTS — scheduled | $1 input / $18 output per million | 0.2784 | Same workload | Scheduled from 2027-01-01; recheck | Same workload at the scheduled 2027-01-01 rates ($1 input / $18 output) |
| 10 | Cartesia Pro | $5 / 100,000 credits | Plan, not variable invoice | 1 character = 1 TTS credit | Allowance, concurrency and model constraints apply | text / constant (no formula) |
| 11 | Cartesia Startup | $49 / 1.25 million credits | $49 plan fits 936,000 chars | 100 lessons at the modeled length | Does not price 1,000 lessons | text / constant (no formula) |
| 12 | Cartesia Scale | $299 / 8 million credits | 9.36 million exceeds this allowance | 1,000 modeled lessons | Obtain higher tier / overage quote | text / constant (no formula) |
| 13 | OpenAI realtime2.1-mini | $0.60 / M text input; $20 / M audio output | Usage-dependent | Do not transplant Gemini token/second rate | New adapter and exact-script audition required | text / constant (no formula) |
| 14 | OpenAI old TTS models | Legacy migration fixture | Do not use for new production | Model shutdown 2027-01-06 | Official notice 2026-10-01 | text / constant (no formula) |
| 15 | Eleven speech-to-speech | $0.12 / generated minute | 1.224 | 10.2 generated minutes with retry allowance | Voice rights + human reference production separate | `Active minutes x (1 + retry) x $0.12` = 8.5 x 1.2 x 0.12 |
| 16 | Human performance | Illustrative $30 / recording hour | Not a market quote | Recording time is NOT finished audio time | Buyouts, licensing and retakes must be quoted | text / constant (no formula) |
| 17 | Self-hosted inference | Illustrative $0.80 / GPU hour | 0.272 | RTF 2, including 20% regeneration | No local neural TTS benchmark performed | `Active minutes x 60 x (1 + retry) x real-time factor / 3600 x GPU $/h` = 8.5 x 60 x 1.2 x 2 / 3600 x 0.8 |


**Facts to carry forward (all as of 13 October 2026):**

* ElevenLabs $0.10/1,000 characters is the published **v2/v3** reference and is "NOT a verified Eleven v4 quote"; Eleven v4 needs an account/model quote ("TBD").
* Gemini 3.8 Flash TTS: $0.50 input / $9 audio output per million tokens through 2026-12-31; **$1 / $18 from 2027-01-01**. 25 audio tokens per second. Modeled synthesis $0.1392 now, $0.2784 scheduled (generation only, excl. QA and labour).
* Cartesia: Pro $5 / 100,000 credits; Startup $49 / 1.25 million credits (fits the 936,000 characters of 100 lessons); Scale $299 / 8 million credits (**1,000 lessons need 9.36 million credits, which exceeds it; obtain a higher-tier / overage quote** rather than a linear $299). 1 character = 1 credit.
* OpenAI old TTS models (`tts-1`, `tts-1-hd`, listed `gpt-4o-mini-tts` snapshots): "Legacy migration fixture. Do not use for new production." Shutdown 2027-01-06, official notice 2026-10-01. Replacement `gpt-realtime-2.1-mini` is $0.60 per million text input / $20 per million audio output, "Usage-dependent", needs a new adapter and exact-script audition; "do not transplant Gemini token/second rate".
* Eleven speech-to-speech $0.12 per generated minute ($1.224 for 10.2 minutes with retry); voice rights and the human reference production are separate.
* Human performance $30 per recording hour is "Not a market quote"; "Recording time is NOT finished audio time"; buyouts, licensing and retakes must be quoted.
* Self-hosted inference $0.80/GPU-hour, $0.272 per lesson at real-time factor 2 including 20% regeneration; "No local neural TTS benchmark performed".

## Sheet 3.5 `Skills`
**Contains:** the **15 custom narration Skills** (columns Skill, Purpose, Input, Output, Validation status). Banner: "Authored instructions and evaluation cases. They have not been tested by running Claude Code/Codex agents. Deterministic code tests are separate." Every row's validation status is **"Authored, not agent-evaluated"**. No cost numbers, no formulas. Cross-reference: `05_narration_system/`, `06_skills_library/`.


| Skill | Purpose | Validation status |
|---|---|---|
| super-teacher-scriptwriter | Convert approved academic claims into teachable conversational narration | Authored, not agent-evaluated |
| dialogue-naturalizer | Remove robotic phrasing without changing scientific meaning | Authored, not agent-evaluated |
| educational-storytelling | Use a small helpful story or analogy with explicit limits | Authored, not agent-evaluated |
| humour-meme-director | Add optional concept-linked humour without ridicule | Authored, not agent-evaluated |
| student-psychology-director | Build competence through real attempts and specific feedback | Authored, not agent-evaluated |
| interactive-teaching-director | Create task-specific prompts, hidden answers and response windows | Authored, not agent-evaluated |
| voice-acting-director | Apply a stable identity and purpose-linked delivery | Authored, not agent-evaluated |
| pacing-controller | Control cognitive pace without rigid scene slots | Authored, not agent-evaluated |
| stem-pronunciation | Create explicit context-aware readings of notation | Authored, not agent-evaluated |
| multilingual-director | Produce audience-appropriate language without semantic drift | Authored, not agent-evaluated |
| tts-provider-adapter | Compile capability-checked provider payloads | Authored, not agent-evaluated |
| speech-animation-synchronizer | Use measured audio timing for educational visuals | Authored, not agent-evaluated |
| audio-production-engineer | Produce clear dialogue masters without erasing useful dynamics | Authored, not agent-evaluated |
| narration-quality-reviewer | Detect text, signal, timing and performance defects | Authored, not agent-evaluated |
| cost-regeneration-optimizer | Minimize duplicate generation and track actual costs | Authored, not agent-evaluated |


## Sheet 3.6 `Sources`
**Contains:** the source and assumption ledger (header row 4, entries in rows 5-18; columns Topic, Source URL, As of, Use). Banner: "URLs support capability or tariff facts only. Research-read does not mean successfully executed or scientifically benchmarked." All entries are "as of 2026-10-13". No formulas.


| Topic | Source URL / file | As of | Use |
|---|---|---|---|
| Topic | Source URL | As of | Use |
| Eleven pricing | https://elevenlabs.io/pricing/api | 2026-10-13 | Reference character and speech-to-speech usage rates |
| Eleven v4 | https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 | 2026-10-13 | Capabilities, differences, expression; no copied v2 settings |
| Eleven languages | https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support | 2026-10-13 | Model-specific Assamese/Hindi coverage; not native QA |
| Cartesia pricing | https://cartesia.ai/pricing | 2026-10-13 | Plans, allowances; large usage still needs quote |
| Gemini pricing | https://ai.google.dev/gemini-api/docs/pricing | 2026-10-13 | Current and scheduled tariff; token conversion |
| Gemini TTS | https://ai.google.dev/gemini-api/docs/speech-generation | 2026-10-13 | Current3.8 schema and output formats |
| OpenAI lifecycle | https://developers.openai.com/api/docs/deprecations | 2026-10-13 | New-production block for deprecated old TTS |
| OpenAI replacement | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini | 2026-10-13 | Replacement pricing; no drop-in guarantee |
| WhisperX | https://github.com/m-bain/whisperX | 2026-10-13 | Word alignment boundary and language resource needs |
| MFA | https://montreal-forced-aligner.readthedocs.io/en/latest/ | 2026-10-13 | Dictionary/acoustic-model alignment pipeline |
| FFmpeg | https://ffmpeg.org/ffmpeg-filters.html#loudnorm | 2026-10-13 | Two-pass loudness and true-peak processing |
| Local tests | outputs/tests.txt | 2026-10-13 | 57 tests; signal fixtures, not a speech-quality benchmark |
| Live auditions | docs/Audition_and_Evaluation.md | 2026-10-13 | Two Runway outputs;18 workspace credits; no local listening score |


### Cell comments in workbook 3
22 threaded comments, one on each of `Inputs!B6:B27`. Each reads "Source: <URL or Planning assumption> / Checked: 13 October 2026. / <caution>", i.e. it duplicates columns D-E of the Inputs table above (nothing extra). Two of them are the key cost warnings: `Inputs!B11` "v2/v3 published reference used for budget; NOT a verified Eleven v4 quote." and `Inputs!B21` "Optional separate initial implementation reserve; not in operating totals."

---

# WORKBOOK 4: business model, `business_ExamLeaf_Business_Model.xlsx`

**Original file name:** `ExamLeaf_Business_Model.xlsx` (raw copy: `00_source/downloads/ExamLeaf_Business_Plan/`; a byte-identical copy is also in `00_source/extracted/ExamLeaf_Business_Launch_Toolkit/`).
**From:** message `06_ASSISTANT_business_model_launch_financial_plan.md` (sections 10, 11 and 14 quote this workbook; the message links it as "Editable financial model and launch workbook - Excel" and the "Complete launch toolkit - ZIP"). The same ZIP supplies `model_assumptions_and_results.json` (the Python-side copy of the assumptions and the nine results, copied into this section), `ExamLeaf_Execution_Runbook.md`, `Research_Source_Ledger.csv` and `ExamLeaf_36_Reel_Backlog.csv`.
**CSV folder:** `csv/business_ExamLeaf_Business_Model/` (30 files = 15 sheets x values/formulas; the brief said 16 sheets, the workbook has **15**).
**Sheets (tab order):** Read Me, Dashboard, Global Inputs, Scenario Inputs, Volume Inputs, Unit Economics, Season P&L, Cash Flow, Price & CAC, Digital Offer, Funnel, 90-Day Budget, 90-Day Roadmap, Reel Backlog, Sources. (CSV names use underscores and `__`: `Read_Me`, `Season_P&L`, `Price_&_CAC`, `90-Day_Budget`.)
**One-paragraph summary:** an INR model of the book-linked business for **one edition / operating season** (not a 90-day forecast). Three cost cases (Conservative / Base / Optimistic) x three scales (500 / 5,000 / 50,000 retained book copies) = **nine scenarios**. Headline: 500 and 5,000 retained copies do **not** recover the season's fixed costs in the Base case (profit -Rs 6.22 lakh and -Rs 6.09 lakh); 50,000 gives +Rs 34.07 lakh Base but -Rs 35.85 lakh Conservative. "Scale is not a substitute for unit economics."

**Sales definition (Read Me):** "Paid, retained book copies net of refunded/returned orders; not printed copies, customers or orders." Cost basis: "Supplier cash costs include non-recovered taxes; input-tax credit is not assumed. No financing cost or income tax." Unsold copies are fully written off at edition end (no salvage).

## Sheet 4.1 `Read Me`
**Contains:** the workbook's guardrails (rows 3-21; 19 entries), reproduced verbatim:


| Topic | Guidance |
|---|---|
| Prepared | 13 October 2026 |
| Currency | INR; Dashboard and P&L explicitly identify lakh amounts. |
| Sales definition | Paid, retained book copies net of refunded/returned orders; not printed copies, customers or orders. |
| Period | One edition/operating season; not a 90-day forecast. 90-day pilot has a separate budget. |
| Tax caution | 18% on the entire marketed bundle is a prudent modelling scenario, NOT a classification opinion. Obtain written advice. |
| Cost basis | Supplier cash costs include non-recovered taxes; input-tax credit is not assumed. No financing cost or income tax. |
| Evidence | Verified provider tariffs are distinguished from unquoted planning assumptions. Replace printer/courier/account inputs. |
| Editable fields | Blue text on pale yellow = assumptions. Green = linked formulas. Black = same-sheet calculations. |
| Inventory | Unsold copies are fully written off at edition end. This is conservative; no salvage revenue is assumed. |
| Guardrail | Do not interpret a positive unit contribution as total profitability or use static break-even outside the modeled cost tier. |
| Read first | Dashboard → Global Inputs → Scenario Inputs → Unit Economics → Cash Flow. |
| Cash-flow convention | Tax and full digital service usage are treated as restricted reserves at sale. Trade cash arrives two months later. Three print lots, 50% advance. |
| Budget meaning | 500 is a two-title pilot with allocated project labour. Higher cases fund an expanded season; they are not simply 100x the pilot. |
| Break-even caveat | Static contribution / fixed-cost calculation only; per-SKU print pricing, staffing and channel mix must be re-costed at any new volume. |
| Cash versus profit | Inventory purchases consume cash before sales. Remaining stock is expensed at edition end. Revenue recognition for future digital obligations needs accountant review. |
| Legal/tax | No legal classification opinion; no corporate/income tax or borrowing interest included. CA/counsel review required. |
| Reels | 36 original drafts with hooks, captions, visuals, CTA, scientific QA and priority. P1 Class 12 ideas are later-stage, not day-one commitments. |
| Access | Proposed one-time edition access, not lifetime support. All promised chapters must be complete or explicitly scheduled before payment. |


Cell comment on `Read Me!B7` (the 18% GST row): *"Tax input is an explicit planning assumption, not a legal opinion. Get a written classification review."* and *"Planning assumption only. GST treatment of the marketed book-and-video package must be reviewed."* (with the GST Council "Composite supply and mixed supply" flyer URL).

## Sheet 4.2 `Global Inputs`
**Contains:** 23 global constants (rows 4-26; columns Input, Value, Unit, Interpretation / limitation, Source / basis) and the 12-month **cash timing** profile (rows 30-45). Title: "VERIFIED TARIFFS + EXPLICIT ESTIMATES".
**Editable cells:** all of column B (rows 4-26) and `B33:C44` (the monthly shares).
**Unused by any formula (descriptive only):** `B20` DTC single test price (499), `B21` two-book bundle (949), `B22` pages (256), `B23`/`B24` trim 7 x 10 in, `B25` paper 70 GSM, `B26` metres per inch. Changing them changes no output (the DTC price that drives the model is `Scenario Inputs` row 4).


| Cell | Input | Value | Unit | Interpretation / limitation | Source / basis |
|---|---|---|---|---|---|
| B4 | MRP per subject book | 549 | INR | Proposed test price, not observed ExamLeaf sales. | Planning assumption |
| B5 | Bundle output GST | 0.18 | rate | Prudent 18% stress/base tax input, NOT legal classification. All cases use it. | https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf |
| B6 | Payment gateway fee | 0.02 | rate | Standard domestic pricing; promotional free period excluded. | https://razorpay.com/pricing/ |
| B7 | GST on gateway fee | 0.18 | rate | Applied to gateway service fee; no input credit assumed. | https://razorpay.com/pricing/ |
| B8 | Planning INR per USD | 90 | INR/USD | Budget buffer, NOT a current FX quote. | Planning assumption |
| B9 | Stream delivery per 1,000 min | 1 | USD | Published usage price; storage separate in fixed infrastructure. | https://developers.cloudflare.com/stream/pricing/ |
| B10 | Delivered minutes per activated book | 400 | minutes | Lifetime-of-edition delivery reserve, including repeat viewing; not just first month. | Planning assumption |
| B11 | Non-recovered tax on hosting | 0.18 | rate | Prudent cash-cost allowance; actual invoice/credit treatment to be checked. | Planning assumption |
| B12 | Funding headroom | 0.15 | rate | Added to modeled peak cash deficit, not expensed in P&L. | Planning assumption |
| B13 | Digital-only subject price | 299 | INR | One-time edition access; no assumed digital revenue in book scenarios. | Planning assumption |
| B14 | Printer advance | 0.5 | rate | 50% one month before receipt; balance on receipt. Obtain written terms. | Planning assumption |
| B15 | First print lot share | 0.4 | rate | Print receipts in months 2, 4 and 5; other lots are 35% and remainder. | Planning assumption |
| B16 | Second print lot share | 0.35 | rate | Inventory is not all printed upfront. | Planning assumption |
| B17 | Digital acquisition cost | 80 | INR/customer | Incremental paid/referral acquisition, excludes fixed organic production. | Planning assumption |
| B18 | Digital support/refunds reserve | 12 | INR/customer | Provision for user support and refund leakage, not unlimited support. | Planning assumption |
| B19 | Digital activation usage rate | 1 | rate | Digital purchasers conservatively assumed active. | Planning assumption |
| B20 | DTC single test price | 499 | INR | Standard-service delivered price; disclose remote-area exceptions before payment. | Planning assumption |
| B21 | Two-book delivered bundle | 949 | INR | Customer offer; actual realized per-book input reflects coupons and order mix. | Planning assumption |
| B22 | Science/maths prototype pages | 256 | pages | Check physical pagination before a fixed page commitment. | Planning assumption |
| B23 | Prototype trim width | 7 | inches | Proposed 7 x 10 inch interior. | Planning assumption |
| B24 | Prototype trim height | 10 | inches | Proposed 7 x 10 inch interior. | Planning assumption |
| B25 | Interior paper | 70 | GSM | Compare opacity and writing comfort on actual proofs. | Planning assumption |
| B26 | Metres per inch | 0.0254 | m/in | Exact conversion. | Definition |


**Cash timing (rows 32-45).** Month 1 is the start of the content build. "NOT A VERIFIED DEMAND FORECAST". Comment on `B33:C33`: *"Seasonality is an illustrative planning distribution. Set actual board deadlines, title readiness and order pipeline; no official exam date is assumed."*


| Relative month | Retained sales share | Fixed spend share |
|---|---|---|
| 1 | 0 | 0.35 |
| 2 | 0 | 0.25 |
| 3 | 0.1 | 0.1 |
| 4 | 0.3 | 0.05 |
| 5 | 0.35 | 0.05 |
| 6 | 0.15 | 0.05 |
| 7 | 0.05 | 0.04 |
| 8 | 0.025 | 0.04 |
| 9 | 0.025 | 0.02 |
| 10 | 0 | 0.02 |
| 11 | 0 | 0.02 |
| 12 | 0 | 0.01 |
| Share checks | 1 | 1 |


Row 45 "Share checks" = `SUM(B33:B44)` = 1 and `SUM(C33:C44)` = 1.0000000000000002 (both must equal 1; the workbook does not enforce it). Sales fall in months 3-9 (peaking in month 5 at 35%); 35% of fixed spend is in month 1 and 25% in month 2.

## Sheet 4.3 `Scenario Inputs`
**Contains:** 25 scenario assumptions (rows 4-28) in three columns, B = Conservative, C = Base, D = Optimistic, plus unit and basis, and the channel-mix check (row 30). Title: "SCENARIO ASSUMPTIONS | ALL REQUIRE PILOT VALIDATION". Every row's basis: "Planning estimate; replace with paid pilot and supplier/account quotations."
**Editable cells:** `B4:D28`. Row 30 is a formula: `SUM(B8:B11)` etc. (must equal 100%).
**Cell comment on every input:** "Unquoted planning assumption. <row name>. Review before committing stock or ad spend."


| Row | Assumption | Conservative (B) | Base (C) | Optimistic (D) | Unit |
|---|---|---|---|---|---|
| 4 | DTC realized per book, after bundle/coupon mix | 429 | 479 | 499 | INR |
| 5 | Marketplace selling price | 449 | 499 | 519 | INR |
| 6 | Bulk discount from MRP | 0.3 | 0.25 | 0.2 | rate |
| 7 | Combined distributor/retailer discount from MRP | 0.45 | 0.4 | 0.35 | rate |
| 8 | Direct-to-consumer unit share | 0.3 | 0.45 | 0.6 | rate |
| 9 | Institutional/bulk unit share | 0.2 | 0.2 | 0.2 | rate |
| 10 | Trade unit share | 0.35 | 0.25 | 0.15 | rate |
| 11 | Marketplace unit share | 0.15 | 0.1 | 0.05 | rate |
| 12 | DTC retained books per customer/order | 1.2 | 1.5 | 1.8 | books/order |
| 13 | DTC incremental CAC; paid/referral blended | 220 | 120 | 70 | INR/customer |
| 14 | DTC courier per order | 85 | 65 | 55 | INR/order |
| 15 | Packaging per DTC order / marketplace unit | 14 | 12 | 10 | INR |
| 16 | Bulk freight per book | 15 | 10 | 8 | INR/book |
| 17 | Trade freight per book | 12 | 8 | 6 | INR/book |
| 18 | All-in marketplace selling/closing/fulfillment cash fee | 105 | 90 | 80 | INR/book |
| 19 | Marketplace advertising per retained book | 45 | 25 | 15 | INR/book |
| 20 | Bulk field servicing / partner acquisition | 10 | 7 | 5 | INR/book |
| 21 | Trade field servicing cost | 12 | 8 | 5 | INR/book |
| 22 | DTC reverse-logistics/chargeback reserve | 18 | 10 | 5 | INR/book |
| 23 | Bulk leakage/collections reserve | 3 | 2 | 1 | INR/book |
| 24 | Trade bad debt/claims reserve | 6 | 4 | 2 | INR/book |
| 25 | Marketplace reverse-logistics reserve | 25 | 18 | 12 | INR/book |
| 26 | Book entitlement activation rate | 0.5 | 0.7 | 0.8 | rate |
| 27 | Service/OTP/support per retained book | 12 | 8 | 6 | INR/book |
| 28 | Retained copies / all copies printed | 0.75 | 0.9 | 0.97 | rate |


Row 30 "Channel mix check (must equal 100%)": 1 / 1 / 1. Base channel mix is 45% DTC, 20% institutional/bulk, 25% trade, 10% marketplace (message 06 section 10.2).

## Sheet 4.4 `Volume Inputs`
**Contains:** the nine cases (rows 4-12): retained books, **landed print cost per copy**, **season fixed spend**, with the print-cost status ("Estimate incl. cover, binding, activation insert, inbound freight and non-recovered tax.") and fixed-cost scope ("500: two-title pilot; 5,000: expanded season; 50,000: up to six titles, not all India."). Title: "PRINT QUOTES MUST BE PER TITLE / LANGUAGE / RUN".
**Editable cells:** `B4:D12`. **Linked cells:** the three **Base** fixed-spend cells `D5`, `D8`, `D11` are formulas pointing to `90-Day Budget` `B14`, `C14`, `D14` (the budget totals). The Conservative and Optimistic fixed-spend cells are hard-coded numbers; editing the 90-Day Budget therefore changes the Base case only.
**Cell comment on `B4:D12`:** "Planning assumption, not an obtained quotation or demand forecast. Printing economies depend on copies PER SKU and batch, not aggregate sales."


| Row | Case | Retained books | Landed print INR/book | Season fixed spend INR | Source of fixed spend |
|---|---|---|---|---|---|
| 4 | Conservative | 500 | 190 | 750,000 | constant |
| 5 | Base | 500 | 160 | 650,000 | ='90-Day Budget'!B14 |
| 6 | Optimistic | 500 | 135 | 600,000 | constant |
| 7 | Conservative | 5,000 | 125 | 1,500,000 | constant |
| 8 | Base | 5,000 | 105 | 1,200,000 | ='90-Day Budget'!C14 |
| 9 | Optimistic | 5,000 | 88 | 1,000,000 | constant |
| 10 | Conservative | 50,000 | 95 | 5,000,000 | constant |
| 11 | Base | 50,000 | 78 | 4,000,000 | ='90-Day Budget'!D14 |
| 12 | Optimistic | 50,000 | 65 | 3,500,000 | constant |


## Sheet 4.5 `Unit Economics`
**Contains:** the engine room: **INR per retained book** for each of the nine cases (columns B-J = Conservative/Base/Optimistic at 500, then 5,000, then 50,000), rows 4-50. Title: "UNIT ECONOMICS | INR PER RETAINED BOOK UNLESS STATED".
**Editable cells:** none (every cell links to Global / Scenario / Volume Inputs).


| Row | Line | Conservative \| 500 | Base \| 500 | Optimistic \| 500 | Conservative \| 5,000 | Base \| 5,000 | Optimistic \| 5,000 | Conservative \| 50,000 | Base \| 50,000 | Optimistic \| 50,000 |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | Retained books | 500 | 500 | 500 | 5,000 | 5,000 | 5,000 | 50,000 | 50,000 | 50,000 |
| 5 | Total copies printed | 667 | 556 | 516 | 6,667 | 5,556 | 5,155 | 66,667 | 55,556 | 51,547 |
| 6 | Landed print per copy | 190 | 160 | 135 | 125 | 105 | 88 | 95 | 78 | 65 |
| 7 | Fixed season spend | 750,000 | 650,000 | 600,000 | 1,500,000 | 1,200,000 | 1,000,000 | 5,000,000 | 4,000,000 | 3,500,000 |
| 9 | DTC share | 0.3 | 0.45 | 0.6 | 0.3 | 0.45 | 0.6 | 0.3 | 0.45 | 0.6 |
| 10 | Bulk share | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |
| 11 | Trade share | 0.35 | 0.25 | 0.15 | 0.35 | 0.25 | 0.15 | 0.35 | 0.25 | 0.15 |
| 12 | Marketplace share | 0.15 | 0.1 | 0.05 | 0.15 | 0.1 | 0.05 | 0.15 | 0.1 | 0.05 |
| 13 | Channel share check | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 15 | DTC realized price incl. modeled GST | 429 | 479 | 499 | 429 | 479 | 499 | 429 | 479 | 499 |
| 16 | Bulk publisher realization | 384.3 | 411.75 | 439.2 | 384.3 | 411.75 | 439.2 | 384.3 | 411.75 | 439.2 |
| 17 | Trade publisher realization | 301.95 | 329.4 | 356.85 | 301.95 | 329.4 | 356.85 | 301.95 | 329.4 | 356.85 |
| 18 | Marketplace gross selling price | 449 | 499 | 519 | 449 | 499 | 519 | 449 | 499 | 519 |
| 19 | Weighted publisher realization, gross | 378.5925 | 430.15 | 466.7175 | 378.5925 | 430.15 | 466.7175 | 378.5925 | 430.15 | 466.7175 |
| 20 | Publisher revenue excluding GST | 320.8411 | 364.5339 | 395.5233 | 320.8411 | 364.5339 | 395.5233 | 320.8411 | 364.5339 | 395.5233 |
| 22 | Print cost of retained copy | 190 | 160 | 135 | 125 | 105 | 88 | 95 | 78 | 65 |
| 23 | Unsold edition write-off / retained copy | 63.46 | 17.92 | 4.32 | 41.675 | 11.676 | 2.728 | 31.6673 | 8.6674 | 2.0111 |
| 24 | Total print burden / retained copy | 253.46 | 177.92 | 139.32 | 166.675 | 116.676 | 90.728 | 126.6673 | 86.6674 | 67.0111 |
| 26 | Full entitlement streaming reserve | 21.24 | 29.736 | 33.984 | 21.24 | 29.736 | 33.984 | 21.24 | 29.736 | 33.984 |
| 27 | Support / servicing | 12 | 8 | 6 | 12 | 8 | 6 | 12 | 8 | 6 |
| 29 | DTC gateway cost / book | 10.1244 | 11.3044 | 11.7764 | 10.1244 | 11.3044 | 11.7764 | 10.1244 | 11.3044 | 11.7764 |
| 30 | DTC shipping, packing, gateway, returns | 110.6244 | 72.6377 | 52.8875 | 110.6244 | 72.6377 | 52.8875 | 110.6244 | 72.6377 | 52.8875 |
| 31 | Bulk freight, field, claims | 28 | 19 | 14 | 28 | 19 | 14 | 28 | 19 | 14 |
| 32 | Trade freight, field, bad debt | 30 | 20 | 13 | 30 | 20 | 13 | 30 | 20 | 13 |
| 33 | Marketplace fees, packing, returns | 144 | 120 | 102 | 144 | 120 | 102 | 144 | 120 | 102 |
| 34 | Weighted fulfillment / channel servicing | 70.8873 | 53.487 | 41.5825 | 70.8873 | 53.487 | 41.5825 | 70.8873 | 53.487 | 41.5825 |
| 36 | DTC CAC / retained book | 183.3333 | 80 | 38.8889 | 183.3333 | 80 | 38.8889 | 183.3333 | 80 | 38.8889 |
| 37 | Weighted DTC acquisition | 55 | 36 | 23.3333 | 55 | 36 | 23.3333 | 55 | 36 | 23.3333 |
| 38 | Weighted marketplace advertising | 6.75 | 2.5 | 0.75 | 6.75 | 2.5 | 0.75 | 6.75 | 2.5 | 0.75 |
| 39 | Total incremental acquisition | 61.75 | 38.5 | 24.0833 | 61.75 | 38.5 | 24.0833 | 61.75 | 38.5 | 24.0833 |
| 41 | Total non-print variable cost | 165.8773 | 129.723 | 105.6498 | 165.8773 | 129.723 | 105.6498 | 165.8773 | 129.723 | 105.6498 |
| 42 | Contribution before acquisition | -36.7462 | 95.3909 | 174.6368 | 50.0388 | 156.6349 | 223.2288 | 90.0465 | 186.6436 | 246.9457 |
| 43 | Contribution after acquisition | -98.4962 | 56.8909 | 150.5535 | -11.7112 | 118.1349 | 199.1455 | 28.2965 | 148.1436 | 222.8624 |
| 44 | Contribution margin | -0.307 | 0.1561 | 0.3806 | -0.0365 | 0.3241 | 0.5035 | 0.0882 | 0.4064 | 0.5635 |
| 45 | Static tier break-even copies | No unit break-even | 11,426 | 3,986 | No unit break-even | 10,158 | 5,022 | 176,701 | 27,001 | 15,705 |
| 47 | DTC contribution after CAC | -217.0984 | 37.6385 | 151.801 | -130.3134 | 98.8825 | 200.393 | -90.3057 | 128.8911 | 224.1099 |
| 48 | Bulk contribution | 10.978 | 114.2847 | 178.8994 | 97.763 | 175.5287 | 227.4914 | 137.7707 | 205.5373 | 251.2083 |
| 49 | Trade contribution | -60.8102 | 43.4965 | 110.1113 | 25.9748 | 104.7405 | 158.7033 | 65.9825 | 134.7492 | 182.4202 |
| 50 | Marketplace contribution | -95.1915 | 62.2254 | 143.5265 | -8.4065 | 123.4694 | 192.1185 | 31.6012 | 153.478 | 215.8354 |


**Formula logic, row by row** (cell references are to column B; each of the other eight columns repeats the same formula with its own case column; "SI" = Scenario Inputs, "GI" = Global Inputs, "VI" = Volume Inputs):

| Row | Line | Plain-English logic |
|---|---|---|
| 4 | Retained books | `VI` retained books for the case |
| 5 | Total copies printed | ROUNDUP(retained books / sell-through `SI` row 28, 0): you must print more than you retain |
| 6, 7 | Landed print per copy; fixed season spend | Straight from `VI` |
| 9-12 | DTC / Bulk / Trade / Marketplace share | `SI` rows 8-11; row 13 is the check (=1) |
| 15 | DTC realized price incl. modeled GST | `SI` row 4 |
| 16 | Bulk publisher realization | MRP (`GI!B4` = 549) x (1 - bulk discount `SI` row 6) |
| 17 | Trade publisher realization | MRP x (1 - distributor/retailer discount `SI` row 7) |
| 18 | Marketplace gross selling price | `SI` row 5 |
| 19 | Weighted publisher realization, gross | channel shares x channel prices (rows 9-12 x rows 15-18) |
| 20 | Publisher revenue excluding GST | row 19 / (1 + GST 18%) |
| 22 | Print cost of retained copy | = landed print per copy |
| 23 | Unsold edition write-off / retained copy | (copies printed - retained) x landed print / retained: **the unsold copies' print cost charged to the retained ones, no salvage** |
| 24 | Total print burden / retained copy | row 22 + row 23 |
| 26 | Full entitlement streaming reserve | activation rate `SI` row 26 x (400 delivered minutes / 1000) x $1 per 1,000 min x Rs 90/USD x (1 + 18% non-recovered tax). e.g. Base 0.7 x 0.4 x 1 x 90 x 1.18 = Rs 29.74 |
| 27 | Support / servicing | `SI` row 27 |
| 29 | DTC gateway cost / book | DTC price x 2% gateway x (1 + 18% GST on the fee) |
| 30 | DTC shipping, packing, gateway, returns | (courier + packaging per order) / books per order + gateway cost + DTC reverse-logistics reserve |
| 31 | Bulk freight, field, claims | bulk freight + bulk field servicing + bulk leakage/collections reserve |
| 32 | Trade freight, field, bad debt | trade freight + trade field servicing + trade bad-debt/claims reserve |
| 33 | Marketplace fees, packing, returns | all-in marketplace fee + packaging + marketplace reverse-logistics reserve |
| 34 | Weighted fulfillment / channel servicing | channel shares x rows 30-33 |
| 36 | DTC CAC / retained book | DTC CAC per customer / books per order |
| 37 | Weighted DTC acquisition | DTC share x row 36 |
| 38 | Weighted marketplace advertising | marketplace share x marketplace ads per book |
| 39 | Total incremental acquisition | row 37 + row 38 |
| 41 | Total non-print variable cost | rows 26 + 27 + 34 + 39 |
| 42 | Contribution before acquisition | row 20 - row 24 - row 26 - row 27 - row 34 |
| 43 | **Contribution after acquisition** | row 42 - row 39 (the per-book number the Dashboard and the break-even use) |
| 44 | Contribution margin | row 43 / row 20 |
| 45 | **Static tier break-even copies** | IF row 43 > 0: ROUNDUP(fixed season spend / row 43, 0), else the text "No unit break-even" |
| 47 | DTC contribution after CAC | DTC price / (1 + GST) - print burden - streaming - support - DTC shipping etc. (row 30) - CAC per book (row 36) |
| 48 | Bulk contribution | bulk realization / (1 + GST) - print burden - streaming - support - row 31 |
| 49 | Trade contribution | trade realization / (1 + GST) - print burden - streaming - support - row 32 |
| 50 | Marketplace contribution | marketplace price / (1 + GST) - print burden - streaming - support - row 33 - marketplace ads |

**Key outputs.** Base 5,000: weighted gross realization Rs 430.15, revenue excl. GST Rs 364.53, print burden Rs 116.68 (Rs 105 + Rs 11.68 write-off), streaming Rs 29.74, support Rs 8, fulfillment Rs 53.49, acquisition Rs 38.50 -> **contribution Rs 118.13/book (32.4% margin)**, break-even **10,158** copies. Channel contribution at the base 5,000 cost tier: DTC after CAC Rs 98.88, Bulk Rs 175.53, Trade Rs 104.74, Marketplace Rs 123.47. Static break-evens by case: No unit break-even (Conservative 500), 11,426 (Base 500), 3,986 (Optimistic 500), No unit break-even (Conservative 5,000), 10,158 (Base 5,000), 5,022 (Optimistic 5,000), 176,701 (Conservative 50,000), **27,001** (Base 50,000), 15,705 (Optimistic 50,000).

## Sheet 4.6 `Season P&L`
**Contains:** one row per case (rows 4-12), INR (not lakh). Title: "ALL MONEY COLUMNS IN INR; NO DIGITAL-ONLY SALES ASSUMED". Presented transposed here (one column per case):


| Col | Metric (INR) | Conservative \| 500 | Base \| 500 | Optimistic \| 500 | Conservative \| 5,000 | Base \| 5,000 | Optimistic \| 5,000 | Conservative \| 50,000 | Base \| 50,000 | Optimistic \| 50,000 |
|---|---|---|---|---|---|---|---|---|---|---|
| B | Retained books | 500 | 500 | 500 | 5,000 | 5,000 | 5,000 | 50,000 | 50,000 | 50,000 |
| C | Publisher gross realization | 189,296.25 | 215,075 | 233,358.75 | 1,892,962.5 | 2,150,750 | 2,333,587.5 | 18,929,625 | 21,507,500 | 23,335,875 |
| D | Output GST reserve | 28,875.7 | 32,808.05 | 35,597.1 | 288,756.99 | 328,080.51 | 355,970.97 | 2,887,569.92 | 3,280,805.08 | 3,559,709.75 |
| E | Net publisher revenue | 160,420.55 | 182,266.95 | 197,761.65 | 1,604,205.51 | 1,822,669.49 | 1,977,616.53 | 16,042,055.08 | 18,226,694.92 | 19,776,165.25 |
| F | Print cash / edition expense | 126,730 | 88,960 | 69,660 | 833,375 | 583,380 | 453,640 | 6,333,365 | 4,333,368 | 3,350,555 |
| G | Other variable cost | 82,938.66 | 64,861.49 | 52,824.92 | 829,386.6 | 648,614.9 | 528,249.2 | 8,293,866 | 6,486,149 | 5,282,492 |
| H | Contribution | -49,248.11 | 28,445.46 | 75,276.73 | -58,556.09 | 590,674.59 | 995,727.33 | 1,414,824.08 | 7,407,177.92 | 11,143,118.25 |
| I | Fixed spend | 750,000 | 650,000 | 600,000 | 1,500,000 | 1,200,000 | 1,000,000 | 5,000,000 | 4,000,000 | 3,500,000 |
| J | Operating profit | -799,248.11 | -621,554.54 | -524,723.27 | -1,558,556.09 | -609,325.41 | -4,272.67 | -3,585,175.92 | 3,407,177.92 | 7,643,118.25 |
| K | Operating margin | -4.9822 | -3.4101 | -2.6533 | -0.9715 | -0.3343 | -0.002160517 | -0.2235 | 0.1869 | 0.3865 |
| L | Units printed | 667 | 556 | 516 | 6,667 | 5,556 | 5,155 | 66,667 | 55,556 | 51,547 |
| M | Profit if output GST 0% | -770,372.41 | -588,746.49 | -489,126.17 | -1,269,799.1 | -281,244.9 | 351,698.3 | -697,606 | 6,687,983 | 11,202,828 |


**Formula logic.** Publisher gross realization = Unit Economics row 19 x retained books; Net publisher revenue = Unit Economics row 20 x books; **Output GST reserve = gross - net**; **Print cash / edition expense = copies printed x landed print per copy** (all copies, including unsold, are expensed); Other variable cost = Unit Economics row 41 x books; **Contribution = net revenue - print - other variable**; Fixed spend = Unit Economics row 7; **Operating profit = Contribution - Fixed spend**; Operating margin = profit / net revenue; Units printed = Unit Economics row 5; **Profit if output GST 0% = Operating profit + Output GST reserve** (the zero-output-tax sensitivity; "not a recommendation to claim exemption"). Profit is before financing cost and income tax.

## Sheet 4.7 `Cash Flow`
**Contains:** **nine 12-month cash-flow blocks** (one per case; each = a title row, a header row and 12 month rows; blocks start at rows 3, 19, 35, 51, 67, 83, 99, 115, 131). Title: "PRINT DEPOSITS, 60-DAY TRADE COLLECTIONS & FULL USAGE RESERVES". Columns: Month, Retained sales, Print receipts, Closing stock, Gross invoiced, Trade invoiced, Cash receipts, GST reserved, Printer cash, Other variable/reserved, Fixed cash, Net usable cash, Cumulative cash, Trade receivable.
**Editable cells:** none (all formulas), but they read the cash-timing shares and printer terms from `Global Inputs`.

**Formula logic (each column, for month *m*, case column *c* of Unit Economics):**

| Col | Meaning | Logic |
|---|---|---|
| B | Retained sales | ROUND(retained books x sales share[m], 0); month 9 takes the remainder so the total equals the case's retained books |
| C | Print receipts | Month 2 = ROUND(copies printed x first lot share 40%), month 4 = ROUND(copies x second lot share 35%), month 5 = the remainder (25%); other months 0. Three print lots |
| D | Closing stock | cumulative print receipts - cumulative retained sales |
| E | Gross invoiced | sales x weighted gross realization (UE row 19, includes GST) |
| F | Trade invoiced | sales x trade share x trade realization |
| G | Cash receipts | E - F + the trade invoices of two months earlier: **trade cash arrives two months later** (60-day collection) |
| H | GST reserved | E x 18% / 1.18: output GST is set aside as a restricted reserve at sale |
| I | Printer cash | (this month's print receipts x (1 - 50%) + next month's print receipts x 50%) x landed print per copy: **50% advance one month before receipt, balance on receipt** |
| J | Other variable/reserved | sales x total non-print variable cost (UE row 41), including the full streaming-usage reserve at the time of sale |
| K | Fixed cash | fixed-spend share[m] x season fixed spend |
| L | Net usable cash | G - (H + I + J + K) |
| M | Cumulative cash | running sum of L; the **minimum of this column is the peak funding gap** the Dashboard reads |
| N | Trade receivable | cumulative trade invoiced - trade cash collected so far |

Because every printed copy is paid for in cash, the **final cumulative cash equals the Season P&L operating profit** (e.g. Base 5,000: -Rs 6,09,325).

**Summary of the nine blocks** (computed from the values CSV; lakh = 100,000):


| Block | Rows | Min cumulative cash (Rs lakh) | Month of minimum | Cumulative cash at month 12 (Rs lakh) | Copies printed | GST reserved (INR) | Printer cash (INR) | Other variable (INR) | Fixed cash (INR) |
|---|---|---|---|---|---|---|---|---|---|
| Conservative \| 500 retained books | 5-16 | -7.99 | 12 | -7.99 | 667 | 28,876 | 126,730 | 82,939 | 750,000 |
| Base \| 500 retained books | 21-32 | -6.22 | 12 | -6.22 | 556 | 32,808 | 88,960 | 64,861 | 650,000 |
| Optimistic \| 500 retained books | 37-48 | -5.25 | 12 | -5.25 | 516 | 35,597 | 69,660 | 52,825 | 600,000 |
| Conservative \| 5,000 retained books | 53-64 | -17.96 | 5 | -15.59 | 6,667 | 288,757 | 833,375 | 829,387 | 1,500,000 |
| Base \| 5,000 retained books | 69-80 | -11.06 | 4 | -6.09 | 5,556 | 328,081 | 583,380 | 648,615 | 1,200,000 |
| Optimistic \| 5,000 retained books | 85-96 | -8.43 | 3 | -0.04 | 5,155 | 355,971 | 453,640 | 528,249 | 1,000,000 |
| Conservative \| 50,000 retained books | 101-112 | -83.06 | 4 | -35.85 | 66,667 | 2,887,570 | 6,333,365 | 8,293,866 | 5,000,000 |
| Base \| 50,000 retained books | 117-128 | -45.29 | 3 | 34.07 | 55,556 | 3,280,805 | 4,333,368 | 6,486,149 | 4,000,000 |
| Optimistic \| 50,000 retained books | 133-144 | -34.40 | 2 | 76.43 | 51,547 | 3,559,710 | 3,350,555 | 5,282,492 | 3,500,000 |


Dashboard "Peak gap" = -(min cumulative cash) in lakh, "Funding +15%" = peak gap x (1 + 15% funding headroom `GI!B12`). Cumulative cash turns positive in the Optimistic 50,000 case from month 5 and in the Base 50,000 case from month 6; in the Optimistic 5,000 case only in months 8-11 (it ends at -Rs 4,273); in no other case.

**Worked example: Base | 5,000 retained books** (rows 67-80). Reading the block shows the cash shape: printing and content are paid before sales, the peak deficit of **-Rs 11.06 lakh is reached in month 4**, and the model ends at -Rs 6.09 lakh:


| Month | Retained sales | Print receipts | Closing stock | Gross invoiced | Trade invoiced | Cash receipts | GST reserved | Printer cash | Other variable/reserved | Fixed cash | Net usable cash | Cumulative cash | Trade receivable |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 116,655 | 0 | 420,000 | -536,655 | -536,655 | 0 |
| 2 | 0 | 2,222 | 2,222 | 0 | 0 | 0 | 0 | 116,655 | 0 | 300,000 | -416,655 | -953,310 | 0 |
| 3 | 500 | 0 | 1,722 | 215,075 | 41,175 | 173,900 | 32,808.05 | 102,112.5 | 64,861.49 | 120,000 | -145,882.04 | -1,099,192.04 | 41,175 |
| 4 | 1,500 | 1,945 | 2,167 | 645,225 | 123,525 | 521,700 | 98,424.15 | 175,035 | 194,584.47 | 60,000 | -6,343.62 | -1,105,535.66 | 164,700 |
| 5 | 1,750 | 1,389 | 1,806 | 752,762.5 | 144,112.5 | 649,825 | 114,828.18 | 72,922.5 | 227,015.22 | 60,000 | 175,059.11 | -930,476.56 | 267,637.5 |
| 6 | 750 | 0 | 1,056 | 322,612.5 | 61,762.5 | 384,375 | 49,212.08 | 0 | 97,292.24 | 60,000 | 177,870.69 | -752,605.87 | 205,875 |
| 7 | 250 | 0 | 806 | 107,537.5 | 20,587.5 | 231,062.5 | 16,404.03 | 0 | 32,430.75 | 48,000 | 134,227.73 | -618,378.14 | 82,350 |
| 8 | 125 | 0 | 681 | 53,768.75 | 10,293.75 | 105,237.5 | 8,202.01 | 0 | 16,215.37 | 48,000 | 32,820.11 | -585,558.02 | 30,881.25 |
| 9 | 125 | 0 | 556 | 53,768.75 | 10,293.75 | 64,062.5 | 8,202.01 | 0 | 16,215.37 | 24,000 | 15,645.11 | -569,912.91 | 20,587.5 |
| 10 | 0 | 0 | 556 | 0 | 0 | 10,293.75 | 0 | 0 | 0 | 24,000 | -13,706.25 | -583,619.16 | 10,293.75 |
| 11 | 0 | 0 | 556 | 0 | 0 | 10,293.75 | 0 | 0 | 0 | 24,000 | -13,706.25 | -597,325.41 | 0 |
| 12 | 0 | 0 | 556 | 0 | 0 | 0 | 0 | 0 | 0 | 12,000 | -12,000 | -609,325.41 | 0 |


## Sheet 4.8 `Dashboard`
**Contains:** the nine-case summary (rows 4-12), a one-line verdict (row 15) and a small profit-by-scale table (rows 18-21) that feeds a clustered **bar chart** (Conservative / Base / Optimistic profit for 500 / 5,000 / 50,000 retained books). Title: "SCALE IS NOT A SUBSTITUTE FOR UNIT ECONOMICS".
**Editable cells:** none.


| Case | Books | Net revenue ₹ lakh | Contribution ₹/book | Fixed ₹ lakh | Profit ₹ lakh | Margin | Peak gap ₹ lakh | Funding +15% ₹ lakh | Static break-even |
|---|---|---|---|---|---|---|---|---|---|
| Conservative \| 500 | 500 | 1.6042 | -98.4962 | 7.5 | -7.9925 | -4.9822 | 7.9925 | 9.1914 | No unit break-even |
| Base \| 500 | 500 | 1.8227 | 56.8909 | 6.5 | -6.2155 | -3.4101 | 6.2155 | 7.1479 | 11,426 |
| Optimistic \| 500 | 500 | 1.9776 | 150.5535 | 6 | -5.2472 | -2.6533 | 5.2472 | 6.0343 | 3,986 |
| Conservative \| 5,000 | 5,000 | 16.0421 | -11.7112 | 15 | -15.5856 | -0.9715 | 17.9573 | 20.6509 | No unit break-even |
| Base \| 5,000 | 5,000 | 18.2267 | 118.1349 | 12 | -6.0933 | -0.3343 | 11.0554 | 12.7137 | 10,158 |
| Optimistic \| 5,000 | 5,000 | 19.7762 | 199.1455 | 10 | -0.0427 | -0.0022 | 8.4266 | 9.6906 | 5,022 |
| Conservative \| 50,000 | 50,000 | 160.4206 | 28.2965 | 50 | -35.8518 | -0.2235 | 83.0606 | 95.5197 | 176,701 |
| Base \| 50,000 | 50,000 | 182.2669 | 148.1436 | 40 | 34.0718 | 0.1869 | 45.2937 | 52.0877 | 27,001 |
| Optimistic \| 50,000 | 50,000 | 197.7617 | 222.8624 | 35 | 76.4312 | 0.3865 | 34.4023 | 39.5627 | 15,705 |


**Formula logic.** Net revenue = Season P&L E / 100,000; Contribution = Unit Economics row 43; Fixed = Season P&L I / 100,000; Profit = Season P&L J / 100,000; Margin = Season P&L K; **Peak gap = MAX(0, -MIN of that case's Cash Flow cumulative cash) / 100,000**; **Funding +15% = Peak gap x (1 + Global Inputs B12)**; Static break-even = Unit Economics row 45.

**Verdict line (row 15, verbatim):** "BASE CASE: 500 copies validate execution; 5,000 still do not recover full season costs. At 50,000 copies, positive profit requires disciplined pricing, sell-through, acquisition and collections. This is a model, not a sales forecast."

**Profit by scale (rows 18-21; chart source), Rs lakh:**


| Retained books | Conservative profit ₹ lakh | Base profit ₹ lakh | Optimistic profit ₹ lakh |
|---|---|---|---|
| 500 | -7.9925 | -6.2155 | -5.2472 |
| 5,000 | -15.5856 | -6.0933 | -0.0427 |
| 50,000 | -35.8518 | 34.0718 | 76.4312 |


## Sheet 4.9 `Price & CAC`
**Contains:** a DTC-only sensitivity grid (rows 3-9) and the maximum-CAC calculation (rows 17-21). Title: "DTC CONTRIBUTION SENSITIVITY | INR PER RETAINED BOOK, 5,000-BOOK BASE COST TIER".
**Editable cells:** the realized-price column `A4:A9` (349, 399, 449, 479, 499, 549) and the CAC row `B3:F3` (50, 100, 150, 200, 250), and `B18` (target contribution, Rs 100). Comments: `A4` "Proposed price tests; no established elasticity or conversion lift assumed."; `B3` "Incremental per-customer acquisition cost sensitivity, not observed ExamLeaf costs."; `B18` "Management target of INR100 contribution per book, not a market norm."

**Grid: DTC contribution per retained book (Rs) by realized price (rows) and CAC per customer (columns)**


| Realized price \ CAC/customer | 50 | 100 | 150 | 200 | 250 |
|---|---|---|---|---|---|
| 349 | 38.45 | 5.11 | -28.22 | -61.55 | -94.89 |
| 399 | 79.64 | 46.31 | 12.97 | -20.36 | -53.69 |
| 449 | 120.83 | 87.5 | 54.17 | 20.83 | -12.5 |
| 479 | 145.55 | 112.22 | 78.88 | 45.55 | 12.22 |
| 499 | 162.03 | 128.69 | 95.36 | 62.03 | 28.69 |
| 549 | 203.22 | 169.89 | 136.55 | 103.22 | 69.89 |


**Formula logic.** For price *P* and CAC *C*: `P / (1 + GST 18%)` - print burden per retained book at the Base 5,000 tier (Unit Economics F24) - streaming reserve (F26) - support (F27) - (Base courier + packaging per order) / Base books per order (SI C14, C15, C12) - `P x 2% x (1 + 18%)` gateway cost - Base DTC reverse-logistics reserve (SI C22) - `C / Base books per order 1.5`. Note the units: **CAC is per customer/order, contribution is per book** ("Per-order CAC and per-book contribution are different units").

**Footer (row 12, verbatim):** "This table is DTC only. It does not include fixed-cost recovery. At lower price, recalibrate conversion and basket size rather than assuming demand rises automatically. Per-order CAC and per-book contribution are different units."

**Maximum DTC CAC with a Rs 100/book contribution target (rows 17-21):**


| Cell | Item | Value | Formula logic |
|---|---|---|---|
| B18 | Target contribution / book | 100 | input |
| B19 | Base DTC basket (books per order) | 1.5 | = Scenario Inputs C12 |
| B20 | Base DTC contribution BEFORE acquisition / book | 178.8825 | = Unit Economics F47 + F36 (DTC contribution after CAC + CAC per book) |
| B21 | **Maximum CAC / order** | 118.3237 | = MAX(0, (B20 - B18) x B19) = (178.88 - 100) x 1.5 |


So at Base DTC economics, a Rs 100/book contribution target permits roughly **Rs 118 CAC per customer/order**; message 06 says to require paid/referral CAC "around Rs 100-120 or lower".

## Sheet 4.10 `Digital Offer`
**Contains:** economics of the optional **digital-only subject** at Rs 299 per paid customer (rows 4-11). Title: "OPTIONAL DIGITAL-ONLY SUBJECT | NOT ADDED TO BOOK-SCENARIO REVENUE" (digital-only revenue is **not** in any of the nine scenarios). **Editable cells:** none here (reads `Global Inputs` B5-B13, B17-B19).


| Row | Metric (INR per paid subject customer) | Value | Formula logic |
|---|---|---|---|
| 4 | Digital selling price incl. modeled GST | 299 | = Global Inputs B13 (digital-only subject price 299) |
| 5 | Revenue excluding GST | 253.3898 | = price / (1 + GST 18%) |
| 6 | Gateway cash cost | 7.0564 | = price x 2% x (1 + 18%) payment-gateway cost |
| 7 | Full-edition delivery reserve | 42.48 | = 400 delivered minutes / 1000 x $1 x Rs 90 x (1 + 18%) x digital activation rate (1) |
| 8 | Support and refund reserve | 12 | = Global Inputs B18 (12) |
| 9 | Incremental acquisition | 80 | = Global Inputs B17 (80) |
| 10 | Contribution before fixed creation costs | 111.8534 | = row 5 - SUM(rows 6-9) |
| 11 | Contribution margin | 0.4414 | = row 10 / row 5 |


**Note (row 14, verbatim):** "Book upgrade: credit the actual digital payment against the same-subject book bundle within a disclosed period. Keep one entitlement; do not count the upgrade as a second full digital sale. Test incremental contribution and cannibalisation, not only conversion. No recurring subscription is assumed." The Rs 111.85 is *before fixed creation costs* (the video/content creation cost is in the 90-Day Budget).

## Sheet 4.11 `Funnel`
**Contains:** a deduplicated funnel illustration (rows 4-14), the 5,000-book channel plan (rows 17-21), the conversion sensitivity (rows 24-26) and the fully loaded CAC (rows 29-32). Title: "DEDUPLICATED STAGES, NOT REEL VIEWS = CUSTOMERS".
**Editable cells:** `B4, B5, B7, B9, B11, B13` (stage values), `C18:C21`, `B25:D25`. Comments: `B4` "Illustrative funnel assumptions, not platform benchmarks. Deduplicate and validate denominators."; `C18` "Planning order/bulk/outlet productivity assumptions; not signed partner commitments."; `B25` "Conversion sensitivity; not guaranteed rates."


| Cell | Stage | Value | Definition / caveat |
|---|---|---|---|
| B4 | Unique accounts reached | 1,000,000 | Illustration only; not guaranteed reach |
| B5 | Share matching geography/class/medium | 0.2 | Estimate; do not profile minors with third-party advertising pixels |
| B6 | Eligible accounts | 200,000 | Derived |
| B7 | Visit rate among eligible accounts | 0.02 | Test assumption |
| B8 | Attributed visits | 4,000 | Deduplicate where lawful/possible |
| B9 | Qualified free-lesson rate among visits | 0.5 | Meaningful lesson participation, not autoplay start |
| B10 | Qualified free learners | 2,000 | Derived |
| B11 | Paid-order rate among qualified learners | 0.05 | Test assumption; not an industry benchmark |
| B12 | New paid DTC customers | 100 | Derived |
| B13 | Retained books per order | 1.5 | Planning assumption |
| B14 | Retained DTC books | 150 | Derived |


Derived: Eligible accounts = reached x matching share; Attributed visits = eligible x visit rate; Qualified free learners = visits x qualified rate; New paid DTC customers = qualified x paid-order rate; Retained DTC books = customers x books per order. **1,000,000 accounts reached produce only 100 paid DTC customers / 150 books** under these test assumptions.

**5,000-book base channel plan (rows 17-21):**


| Channel | Books | Order / outlet assumption | Accounts required | Formula logic |
|---|---|---|---|---|
| DTC | 2,250 | 1.5 | 1,500 | Books = Unit Economics F4 x channel share (F9..F12); Accounts required = Books / assumption |
| Institutional/bulk | 1,000 | 50 | 20 | Books = Unit Economics F4 x channel share (F9..F12); Accounts required = Books / assumption |
| Trade | 1,250 | 50 | 25 | Books = Unit Economics F4 x channel share (F9..F12); Accounts required = Books / assumption |
| Marketplace | 500 | 1 | 500 | Books = Unit Economics F4 x channel share (F9..F12); Accounts required = Books / assumption |


**Conversion sensitivity (rows 24-26):** qualified learners needed for the DTC plan = DTC accounts required (D18 = 1,500 customers) / qualified-to-order rate: **50,000 at 3%, 30,000 at 5%, 18,750 at 8%**.

**Fully loaded CAC (rows 29-32):** DTC incremental CAC for the Base season (Rs 120, = Scenario Inputs C13) + fixed social/creative spend allocated to DTC (Rs 1,00,000, = 90-Day Budget C7) / DTC customers (1,500) = **Rs 186.67 per DTC customer**. Note (verbatim): "Do NOT deduct this fully loaded KPI again in profit: fixed creative spending is already expensed."

## Sheet 4.12 `90-Day Budget`
**Contains:** fixed project / season budgets in INR for the 500-book pilot, 5,000-book season and 50,000-book season (rows 4-13) with totals (row 14) and the release discipline note (row 17). Title: "FIXED PROJECT / SEASON BUDGETS | INR; CASH STOCK & VARIABLE SALES COSTS ARE SEPARATE".
**Editable cells:** `B4:D13`. Row 14 `B14:D14 = SUM(B4:B13)` and feeds `Volume Inputs` D5 / D8 / D11 (Base fixed spend) and, via `C7`, the Funnel's fully loaded CAC. Each line carries the comment "Planning allocation, not a supplier or employment quote." plus its scope text.


| Row | Category | 500-book pilot (B) | 5,000-book season (C) | 50,000-book season (D) | Scope / assumption |
|---|---|---|---|---|---|
| 4 | Manuscripts + independent academic review | 160,000 | 250,000 | 600,000 | Contract authoring and subject review; source rights required. |
| 5 | Editing, pagination, cover and print proofs | 60,000 | 100,000 | 250,000 | Do not replace quality checks with generated layouts. |
| 6 | Reviewed chapter videos | 120,000 | 200,000 | 450,000 | Pilot: 40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates. |
| 7 | Reels, free-content packaging, community | 50,000 | 100,000 | 350,000 | Fixed organic acquisition cost; excluded from incremental CAC but included in profit. |
| 8 | Commerce / activation development | 60,000 | 100,000 | 250,000 | Lean existing-commerce stack; no custom native app. |
| 9 | Fixed hosting, tools, storage | 15,000 | 40,000 | 120,000 | Video delivery is separately reserved per activated book. |
| 10 | Allocated founder / operational staff time | 115,000 | 260,000 | 1,450,000 | Allocated project/season workload, not a promise of unlimited full-time staffing. |
| 11 | Legal, tax, accounts and rights administration | 25,000 | 50,000 | 130,000 | GST classification and minors/privacy review are launch gates. |
| 12 | Partner launch visits, specimens, travel | 30,000 | 70,000 | 300,000 | Fixed launch work; per-sale field servicing also separately modeled. |
| 13 | QA and project contingency | 15,000 | 30,000 | 100,000 | Expected spending allowance; funding headroom is additional liquidity, not P&L expense. |
| 14 | Total fixed budget | 650,000 | 1,200,000 | 4,000,000 |  |


**Release discipline (row 17, verbatim):** "90-day release discipline: authorize INR 60,000 for discovery/prototypes first. Release the remaining pilot budget only after medium/subject demand, academic quality, tax treatment and a fulfillment proof are validated. Suggested available capital ceiling: INR 8 lakh; not a mandate to spend it all."

**Engine seam.** Row 6, "Reviewed chapter videos", is the only line where the business model prices video production: "Pilot: 40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates." (Rs 1,20,000 pilot; Rs 2,00,000 and Rs 4,50,000 for the larger seasons.) The workbook does not show how Rs 3,000 was derived from the engine workbooks (Rs 3,000 is about $33.33 at the Rs 90/USD planning rate). Row 7 ("Reels, free-content packaging, community") is a *fixed organic acquisition cost* that overlaps in subject matter with the engine's optional Shorts package; see the reconciliation in `CONSOLIDATED_COST_SCENARIOS.md`.

## Sheet 4.13 `90-Day Roadmap`
**Contains:** the 13-week launch plan (columns Week, Days, Owner, Work, Deliverable, Gate / stop rule). Title: "SEQUENCED GATES, NOT A MANDATE TO LAUNCH SIX TITLES". Text only (values = formulas file). Cost-relevant gates: week 2 "Discovery/prototype spending cap INR 60,000 until gate passed" and "obtain 3 like-for-like print quotes"; week 7 "Print-ready proof and approved unit economics"; week 9 "Check actual per-SKU print price and latest viable dispatch date" and "Real courier-weight data"; week 12 "Do not print ahead merely to obtain a cheaper unit quote".


| Week | Days | Owner | Work | Deliverable | Gate / stop rule |
|---|---|---|---|---|---|
| 1 | 1–7 | Founder + academic lead | Interview 15 students, 5 parents, 5 teachers and 4 shops. Collect actual competing books. Confirm medium and board/year. | Interview notes; competitor shelf sheet; source/rights register. | No claim that an Instagram poll proves demand. |
| 2 | 8–14 | Academic lead + founder | Complete remaining interviews; test two free chapter prototypes, price cards and real book pages; obtain 3 like-for-like print quotes. | Two approved prototypes; costed specification; tax/privacy review started. | Discovery/prototype spending cap INR 60,000 until gate passed. |
| 3 | 15–21 | Academic editors | Lock two Class 10 titles and one medium. Define 8-paper pagination and all printed solutions. Design first 3 free chapters by diagnostic value. | Signed syllabus map and manuscript plan; no unreviewed 'official' claims. | Stop a title that cannot be accurately completed before promised delivery. |
| 4 | 22–28 | Video + design team | Build reusable diagrams and vertical Reel templates; publish 4–5 Class 10 Reels and free lesson 1 per title. | Track qualified visits and question attempts, not only plays. | No paid reach boost merely because a Reel gets views. |
| 5 | 29–35 | Editors + developers | Continue manuscripts/videos; implement checkout, entitlement database, refund/coupon rules and guardian flow. | Test payment webhook and free viewing without forced registration. | No third-party behavioural pixels on student learning pages. |
| 6 | 36–42 | QA + partnerships | Finish six free lessons; test on low-cost phones; prepare teacher specimen and short book walkthrough. Recruit permissioned partners. | Academic review; low-data/mobile test; partner terms. | No covert teacher commission or compulsory pupil purchase. |
| 7 | 43–49 | Publisher + finance | Blind-review representative papers and all prototype solutions; compare printer proofs; approve tax/invoicing/access terms. | Print-ready proof and approved unit economics. | Accept transparent preorders only against a credible dispatch date. |
| 8 | 50–56 | Editorial + video lead | Complete the paid catalogue promised for launch and the first two print masters; test scratch-code sequence and two-device recovery. | Release candidate books/videos; duplicate-redemption and refund tests. | Do not sell all-chapter access while undisclosed major chapters are missing. |
| 9 | 57–63 | Founder + fulfillment | Authorize only the first short batch against paid demand/partner commitments. Test dispatch to urban and rural pincodes. | Real courier-weight data; delivery tracking; receipt/activation checklist. | Check actual per-SKU print price and latest viable dispatch date. |
| 10 | 64–70 | Support + academic lead | Fulfill pilot buyers; repair activation friction; collect voluntary learning feedback; seed 10–20 outlets with capped stock. | Delivered orders; first-week practice/activation reports. | No further ad scale while refund or academic issues remain. |
| 11 | 71–77 | Growth + partnerships | Promote best-converting Reel families; launch disclosed referral pilot; compare digital-only vs bundle paths. | Contribution by cohort/channel; 3/7-day support and refund metrics. | One reward/commission path per sale; no incentive stacking. |
| 12 | 78–84 | Finance + operations | Reconcile all channels and printer stock; test second order/subject bundle; set reprint by demand and lead time. | Actual CAC, sell-through, margin, cash and partner receivables. | Do not print ahead merely to obtain a cheaper unit quote. |
| 13 | 85–90 | Founder + review board | Review academic outcomes and financial gate. Continue, revise price/offer or stop. Class 12 expansion only after title-level approval. | Next-season plan; corrections log; source and customer-data audits. | Expansion requires positive contribution, dependable delivery and evidence of learning. |


## Sheet 4.14 `Reel Backlog`
**Contains:** "36 REEL CONCEPTS | ORIGINAL DRAFTS, NOT CLAIMS OF GUARANTEED VIRALITY" (columns ID, Audience, Strand, Topic, Opening hook / cover, Visual treatment, Caption first line, Single CTA, Funnel objective, Target duration sec, Scientific/editorial check, Launch priority, Status). 36 reels: 20 P0 and 16 P1 (P1 = Class 12, later-stage); all Status = Draft; total target duration 1505 seconds. Text only; **no cost numbers**. The cost of producing them sits in `90-Day Budget` row 7 (and, on the engine side, the Shorts package). Full text: `csv/business_ExamLeaf_Business_Model/ExamLeaf_Business_Model__Reel_Backlog__values.csv`; the 36 reels are written up in `01_business_model/REEL_BACKLOG_36.md`.


| ID | Audience | Strand | Topic | Funnel objective | Sec | Priority |
|---|---|---|---|---|---|---|
| 1 | Class 10 | Physics | Ohm's law conditions | Free lesson | 35 | P0 |
| 2 | Class 10 | Physics | I-V graph interpretation | Practice | 30 | P0 |
| 3 | Class 10 | Physics | Circuit power comparison | Free lesson | 45 | P0 |
| 4 | Class 10 | Physics | Mirror image prediction | Practice | 40 | P0 |
| 5 | Class 10 | Physics | Lens sign convention | Worksheet | 35 | P0 |
| 6 | Class 12 | Physics | Gauss law | Free lesson | 45 | P1 |
| 7 | Class 12 | Physics | Drift velocity | Free lesson | 50 | P1 |
| 8 | Class 12 | Physics | Capacitor energy | Practice | 55 | P1 |
| 9 | Class 12 | Physics | Lenz's law | Free lesson | 45 | P1 |
| 10 | Class 10 | Chemistry | Balancing equations | Practice | 30 | P0 |
| 11 | Class 10 | Chemistry | pH scale | Free lesson | 35 | P0 |
| 12 | Class 10 | Chemistry | Ionic conductivity | Free lesson | 40 | P0 |
| 13 | Class 10 | Chemistry | Oxidation and reduction | Worksheet | 35 | P0 |
| 14 | Class 12 | Chemistry | Nernst equation | Free lesson | 55 | P1 |
| 15 | Class 12 | Chemistry | Chemical kinetics | Practice | 40 | P1 |
| 16 | Class 12 | Chemistry | Organic reaction conditions | Worksheet | 45 | P1 |
| 17 | Class 12 | Chemistry | Coordination compounds | Practice | 45 | P1 |
| 18 | Class 10 | Mathematics | Lost algebraic solution | Free lesson | 35 | P0 |
| 19 | Class 10 | Mathematics | Trigonometric identities | Practice | 40 | P0 |
| 20 | Class 10 | Mathematics | Arithmetic progressions | Worksheet | 35 | P0 |
| 21 | Class 10 | Mathematics | Similar figures | Practice | 35 | P0 |
| 22 | Class 12 | Mathematics | Inverse functions | Free lesson | 50 | P1 |
| 23 | Class 12 | Mathematics | Chain rule | Practice | 35 | P1 |
| 24 | Class 12 | Mathematics | Integration constant | Free lesson | 40 | P1 |
| 25 | Class 12 | Mathematics | Conditional probability | Practice | 45 | P1 |
| 26 | Class 10 | Biology | Plant transport | Free lesson | 40 | P0 |
| 27 | Class 10 | Biology | Reflex actions | Worksheet | 45 | P0 |
| 28 | Class 10 | Biology | Inheritance probabilities | Free lesson | 45 | P0 |
| 29 | Class 10 | Biology | Stomata | Practice | 40 | P0 |
| 30 | Class 12 | Biology | Chromosome vs DNA count | Practice | 55 | P1 |
| 31 | Class 12 | Biology | DNA replication direction | Free lesson | 55 | P1 |
| 32 | Class 12 | Biology | Microbes and immunity | Free lesson | 40 | P1 |
| 33 | Class 12 | Biology | Ecological pyramids | Practice | 45 | P1 |
| 34 | Both classes | Study method | Answer quality | Book proof | 35 | P0 |
| 35 | Both classes | Study method | Confidence check | Trust / practice | 40 | P0 |
| 36 | Both classes | Product proof | Book-to-video repair | Purchase | 45 | P0 |


## Sheet 4.15 `Sources`
**Contains:** the source ledger: "PUBLIC SOURCES CHECKED 13 OCTOBER 2026 + OPEN VALIDATION GAPS" (columns Topic, Source type, URL, What it supports, Important limitation). Text only. Every row is reproduced below (and is in the CSV); the cost-relevant caveats are the Razorpay, Amazon, India Post, printer, Cloudflare, GST and "Model costs and conversions" rows.


| Topic | Source type | URL | What it supports | Important limitation |
|---|---|---|---|---|
| ASSEB structure | Official board | https://asseb.in/ | Current Division I/II naming; former SEBA/AHSEC. | Verified public source; no board endorsement implied. |
| Assam curriculum | Official Division I | https://site.sebaonline.org/ | Current syllabus/notifications; confirm class, medium, year before publication. | Download authoritative curriculum and record version before writing. |
| Assam rural digital access | ASER 2024 state report | https://asercentre.org/wp-content/uploads/2022/12/Assam-1.pdf | Rural ages 14–16; 91.4% home smartphone; 14.6% own among smartphone-capable. | Survey denominator differs by question; not an all-Assam personal-phone rate. |
| Oswaal current catalogue | Publisher | https://oswaalbooks.com/ | Current sample-paper products and publisher-advertised digital/AI features. | Snapshot 13 Oct 2026; CBSE products are not exact Assam equivalents. |
| Oswaal Physics | Publisher product | https://oswaalbooks.com/products/cbse-15-sample-question-papers-class-12-board-exam-physics-2026-27-based-on-latest-cbse-sqp-dated-21-sep-2026-new-questions-typologies-with-oswaal-ai | Class 12 Physics 15 SQP 2026–27; listed INR 499 when checked. | Recheck price, availability and inclusions at launch. |
| Arihant | Publisher | https://arihantbooks.com/ | Sample-paper/All in One formats, solutions and revision aids. | Exact SKU, board and discount must be compared, not brand-wide price assumptions. |
| PW Assam | Provider | https://www.pw.live/asseb/class-10 | Dedicated ASSEB Class 10 page, free content and paid offerings. | Evidence that Assam digital education is not an uncontested market. |
| Instagram creator guidance | Meta | https://about.fb.com/news/2024/10/best-practices-education-hub-creators-instagram/ | Professional-dashboard Best Practices provides personalized guidance. | Does not establish a universal posting frequency or viral formula. |
| Instagram ranking | Meta | https://about.fb.com/news/2023/06/how-ai-ranks-content-on-facebook-and-instagram/ | Multiple ranking predictions/signals and personalization. | Do not claim exact signal weights or guaranteed distribution. |
| Teen advertising | Meta | https://about.fb.com/news/2023/01/age-appropriate-ads-for-teens/ | Teen advertising restrictions. | Design no behavioural retargeting to minors; recheck account policies. |
| YouTube Shorts handoff | YouTube Help | https://support.google.com/youtube/answer/14075157?hl=en | Related video link from Short to channel content. | Feature requires appropriate account access. |
| WhatsApp permission | WhatsApp | https://business.whatsapp.com/policy | Permission, expectation and opt-out policy. | Message templates/categories and pricing must be checked for actual account. |
| Gateway | Razorpay | https://razorpay.com/pricing/ | Standard 2% + GST pricing; promo excluded. | Actual payment-method/negotiated rates may differ. |
| Marketplace | Amazon India | https://sell.amazon.in/fees-and-pricing | Books referral at >INR250–500 is 2%; additional fees apply. | All-in model fee is an assumption, not the referral percentage. |
| Book post eligibility | India Post | https://www.indiapost.gov.in/mailproducts/domesticservices/gyanpost | Gyan Post eligibility and conditions. | Obtain written eligibility for the exact marketed book/insert/pack. |
| Postal tariffs | India Post | https://www.indiapost.gov.in/mailproducts/domesticservices/domestictariff | Published Gyan Post slabs when eligible. | Weigh actual packed SKU; no all-India exam-date delivery guarantee. |
| Print-price reality check | Printer | https://www.bulkprintouts.com/book-printing.html | Public short-run print and binding prices; different from ExamLeaf offset specification. | Not an ExamLeaf quote; none of the modeled unit costs are represented as quoted. |
| Video delivery | Cloudflare | https://developers.cloudflare.com/stream/pricing/ | USD1/1,000 delivered minutes; USD5/1,000 stored-minute capacity. | Model adds planning FX/tax and full-edition usage reserve. |
| Video access control | Cloudflare docs | https://developers.cloudflare.com/stream/viewing-videos/securing-your-stream/ | Signed tokens and origin restrictions. | Access control reduces casual sharing; does not prevent screen recording. |
| Commerce | WooCommerce | https://woocommerce.com/woocommerce/ | Open-source commerce and integration capabilities. | Hosting, plugins and developer upkeep are not free. |
| Fulfillment API | Shiprocket | https://apidocs.shiprocket.in/ | Official API documentation endpoint. | Obtain serviceable-pincode, weight, fee and COD/RTO account quotes. |
| GST current notification | Ministry of Finance / PIB | https://www.pib.gov.in/PressReleasePage.aspx?PRID=2168426 | 2025 rate/exemption notifications supersede older goods-rate notifications. | Review current 10/2025 notification and later amendments with a CA. |
| GST bundle classification | GST Council / NACIN | https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf | Principal-supply versus mixed-supply logic. | No automatic nil-rate assumption for a valuable book/video package. |
| DPDP rules | MeitY / Gazette | https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf | Phased commencement; verifiable parental consent and limited exceptions. | Legal review of ExamLeaf status; do not assume an institutional exemption. |
| DPDP Act | MeitY | https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf | Children and targeted-advertising/behavioural-monitoring provisions. | Track commencement notifications; build privacy-preserving defaults now. |
| Education advertising | CCPA / PIB | https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2073013&lang=2&reg=48 | No misleading educational guarantees, false urgency or deceptive success stories. | Scope and detailed compliance to be reviewed for books plus instruction. |
| Retrieval learning | Meta-analysis | https://pubmed.ncbi.nlm.nih.gov/33683913/ | Testing/quizzing supports classroom learning on average. | Not a promise of a given ExamLeaf score improvement. |
| Confidence vs learning | Primary experiment | https://www.pnas.org/doi/10.1073/pnas.1821936116 | Feeling of learning can diverge from measured learning. | University context; not a direct ExamLeaf business conversion study. |
| Market size | Planning limitation | https://asseb.in/ | Use official class/stream/medium/district counts before a large production order. | Exact 2026 participation figures were not reconciled to an official result census. |
| Model costs and conversions | ExamLeaf planning assumptions | Not an external source | Printing, shipping, CAC, sell-through, salaries, conversions and production workloads are estimates. | Replace with quotes and observed cohort data. No virality or demand forecast claimed. |


### Cell comments in workbook 4 (145 threaded comments)
All comments are repeated below, grouped by identical text. Each reinforces the "this is an assumption, not a quote" message and is **not** present in the CSV files.

| Sheet | Cell(s) | Comment text (threaded cell note embedded in the .xlsx) |
|---|---|---|
| Read Me | B7 | Tax input is an explicit planning assumption, not a legal opinion. Get a written classification review. |
| Read Me | B7 | Planning assumption only. GST treatment of the marketed book-and-video package must be reviewed. Source: https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf |
| Global Inputs | B4 | Source: Planning assumption. Proposed test price, not observed ExamLeaf sales. |
| Global Inputs | B5 | Source: https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf. Prudent 18% stress/base tax input, NOT legal classification. All cases use it. |
| Global Inputs | B6 | Source: https://razorpay.com/pricing/. Standard domestic pricing; promotional free period excluded. |
| Global Inputs | B7 | Source: https://razorpay.com/pricing/. Applied to gateway service fee; no input credit assumed. |
| Global Inputs | B8 | Source: Planning assumption. Budget buffer, NOT a current FX quote. |
| Global Inputs | B9 | Source: https://developers.cloudflare.com/stream/pricing/. Published usage price; storage separate in fixed infrastructure. |
| Global Inputs | B10 | Source: Planning assumption. Lifetime-of-edition delivery reserve, including repeat viewing; not just first month. |
| Global Inputs | B11 | Source: Planning assumption. Prudent cash-cost allowance; actual invoice/credit treatment to be checked. |
| Global Inputs | B12 | Source: Planning assumption. Added to modeled peak cash deficit, not expensed in P&L. |
| Global Inputs | B13 | Source: Planning assumption. One-time edition access; no assumed digital revenue in book scenarios. |
| Global Inputs | B14 | Source: Planning assumption. 50% one month before receipt; balance on receipt. Obtain written terms. |
| Global Inputs | B15 | Source: Planning assumption. Print receipts in months 2, 4 and 5; other lots are 35% and remainder. |
| Global Inputs | B16 | Source: Planning assumption. Inventory is not all printed upfront. |
| Global Inputs | B17 | Source: Planning assumption. Incremental paid/referral acquisition, excludes fixed organic production. |
| Global Inputs | B18 | Source: Planning assumption. Provision for user support and refund leakage, not unlimited support. |
| Global Inputs | B19 | Source: Planning assumption. Digital purchasers conservatively assumed active. |
| Global Inputs | B20 | Source: Planning assumption. Standard-service delivered price; disclose remote-area exceptions before payment. |
| Global Inputs | B21 | Source: Planning assumption. Customer offer; actual realized per-book input reflects coupons and order mix. |
| Global Inputs | B22 | Source: Planning assumption. Check physical pagination before a fixed page commitment. |
| Global Inputs | B23, B24 | Source: Planning assumption. Proposed 7 x 10 inch interior. |
| Global Inputs | B25 | Source: Planning assumption. Compare opacity and writing comfort on actual proofs. |
| Global Inputs | B26 | Source: Definition. Exact conversion. |
| Global Inputs | B33, C33 | Seasonality is an illustrative planning distribution. Set actual board deadlines, title readiness and order pipeline; no official exam date is assumed. |
| Scenario Inputs | B4, C4, D4 | Unquoted planning assumption. DTC realized per book, after bundle/coupon mix. Review before committing stock or ad spend. |
| Scenario Inputs | B5, C5, D5 | Unquoted planning assumption. Marketplace selling price. Review before committing stock or ad spend. |
| Scenario Inputs | B6, C6, D6 | Unquoted planning assumption. Bulk discount from MRP. Review before committing stock or ad spend. |
| Scenario Inputs | B7, C7, D7 | Unquoted planning assumption. Combined distributor/retailer discount from MRP. Review before committing stock or ad spend. |
| Scenario Inputs | B8, C8, D8 | Unquoted planning assumption. Direct-to-consumer unit share. Review before committing stock or ad spend. |
| Scenario Inputs | B9, C9, D9 | Unquoted planning assumption. Institutional/bulk unit share. Review before committing stock or ad spend. |
| Scenario Inputs | B10, C10, D10 | Unquoted planning assumption. Trade unit share. Review before committing stock or ad spend. |
| Scenario Inputs | B11, C11, D11 | Unquoted planning assumption. Marketplace unit share. Review before committing stock or ad spend. |
| Scenario Inputs | B12, C12, D12 | Unquoted planning assumption. DTC retained books per customer/order. Review before committing stock or ad spend. |
| Scenario Inputs | B13, C13, D13 | Unquoted planning assumption. DTC incremental CAC; paid/referral blended. Review before committing stock or ad spend. |
| Scenario Inputs | B14, C14, D14 | Unquoted planning assumption. DTC courier per order. Review before committing stock or ad spend. |
| Scenario Inputs | B15, C15, D15 | Unquoted planning assumption. Packaging per DTC order / marketplace unit. Review before committing stock or ad spend. |
| Scenario Inputs | B16, C16, D16 | Unquoted planning assumption. Bulk freight per book. Review before committing stock or ad spend. |
| Scenario Inputs | B17, C17, D17 | Unquoted planning assumption. Trade freight per book. Review before committing stock or ad spend. |
| Scenario Inputs | B18, C18, D18 | Unquoted planning assumption. All-in marketplace selling/closing/fulfillment cash fee. Review before committing stock or ad spend. |
| Scenario Inputs | B19, C19, D19 | Unquoted planning assumption. Marketplace advertising per retained book. Review before committing stock or ad spend. |
| Scenario Inputs | B20, C20, D20 | Unquoted planning assumption. Bulk field servicing / partner acquisition. Review before committing stock or ad spend. |
| Scenario Inputs | B21, C21, D21 | Unquoted planning assumption. Trade field servicing cost. Review before committing stock or ad spend. |
| Scenario Inputs | B22, C22, D22 | Unquoted planning assumption. DTC reverse-logistics/chargeback reserve. Review before committing stock or ad spend. |
| Scenario Inputs | B23, C23, D23 | Unquoted planning assumption. Bulk leakage/collections reserve. Review before committing stock or ad spend. |
| Scenario Inputs | B24, C24, D24 | Unquoted planning assumption. Trade bad debt/claims reserve. Review before committing stock or ad spend. |
| Scenario Inputs | B25, C25, D25 | Unquoted planning assumption. Marketplace reverse-logistics reserve. Review before committing stock or ad spend. |
| Scenario Inputs | B26, C26, D26 | Unquoted planning assumption. Book entitlement activation rate. Review before committing stock or ad spend. |
| Scenario Inputs | B27, C27, D27 | Unquoted planning assumption. Service/OTP/support per retained book. Review before committing stock or ad spend. |
| Scenario Inputs | B28, C28, D28 | Unquoted planning assumption. Retained copies / all copies printed. Review before committing stock or ad spend. |
| Volume Inputs | B4 ... D12 (27 cells) | Planning assumption, not an obtained quotation or demand forecast. Printing economies depend on copies PER SKU and batch, not aggregate sales. |
| Price & CAC | A4 | Proposed price tests; no established elasticity or conversion lift assumed. |
| Price & CAC | B3 | Incremental per-customer acquisition cost sensitivity, not observed ExamLeaf costs. |
| Price & CAC | B18 | Management target of INR100 contribution per book, not a market norm. |
| Funnel | B4 | Illustrative funnel assumptions, not platform benchmarks. Deduplicate and validate denominators. |
| Funnel | C18 | Planning order/bulk/outlet productivity assumptions; not signed partner commitments. |
| Funnel | B25 | Conversion sensitivity; not guaranteed rates. |
| 90-Day Budget | B4 | Planning allocation, not a supplier or employment quote. Contract authoring and subject review; source rights required. |
| 90-Day Budget | B5 | Planning allocation, not a supplier or employment quote. Do not replace quality checks with generated layouts. |
| 90-Day Budget | B6 | Planning allocation, not a supplier or employment quote. Pilot: 40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates. |
| 90-Day Budget | B7 | Planning allocation, not a supplier or employment quote. Fixed organic acquisition cost; excluded from incremental CAC but included in profit. |
| 90-Day Budget | B8 | Planning allocation, not a supplier or employment quote. Lean existing-commerce stack; no custom native app. |
| 90-Day Budget | B9 | Planning allocation, not a supplier or employment quote. Video delivery is separately reserved per activated book. |
| 90-Day Budget | B10 | Planning allocation, not a supplier or employment quote. Allocated project/season workload, not a promise of unlimited full-time staffing. |
| 90-Day Budget | B11 | Planning allocation, not a supplier or employment quote. GST classification and minors/privacy review are launch gates. |
| 90-Day Budget | B12 | Planning allocation, not a supplier or employment quote. Fixed launch work; per-sale field servicing also separately modeled. |
| 90-Day Budget | B13 | Planning allocation, not a supplier or employment quote. Expected spending allowance; funding headroom is additional liquidity, not P&L expense. |

**Embedded chart.** `Dashboard` holds one clustered bar chart plotting `Dashboard!A19:D21` (profit in Rs lakh for Conservative / Base / Optimistic at 500 / 5,000 / 50,000 retained books).

**`model_assumptions_and_results.json` (copied into this section).** The Python-side mirror of the workbook: `global` (MRP 549, GST 0.18, gateway 0.02, gateway GST 0.18, FX 90, stream $1 per 1,000 min, 400 delivered minutes, infra tax 0.18, funding buffer 0.15, digital price 299), `scenarios` (per-case parameters incl. `printcosts` [500, 5,000, 50,000] and `fixed` [500, 5,000, 50,000]) and `results` (nine records: print_qty, print_cost, gross_unit, net_unit, digital_unit [streaming reserve], payment_unit, fulfillment_unit, acq_unit, nonprint_unit, print_unit, contrib, fixed, revenue, profit, break_even [null where "No unit break-even"], peak, funding). The nine `results` agree with the workbook's Dashboard (e.g. Base 5,000: contrib 118.13, profit -609,325.41, break-even 10,158, peak 1,105,535.66, funding 1,271,366.01), which is a useful independent cross-check when you edit the workbook.

---

## Appendix: edit-impact quick reference (all four workbooks)

| If you change... | ...these outputs move |
|---|---|
| v1 `Inputs!B37:B40` (review/QA minutes and rates) | `UnitCosts!B17:B20`, all of `Volumes`. Human review is 88% of v1 cost, so this is the biggest lever |
| v1 `Inputs!B28` (render minutes) | `UnitCosts!B12`, `Volumes!B15` (worker hours). 45 minutes is unmeasured |
| v1 `Inputs!B51` (Remotion switch) | `Volumes` row 9 only |
| v2 `Inputs!B45:B53` (minutes per architecture) | `Per Video` rows 13-16, 20; `Volume Model`; `Decision` |
| v2 `Inputs!B24:B27` (generated seconds and attempts) | `Per Video` row 7 (AI-heavy $108, Hybrid $4) |
| v2 `Inputs!B44` (accounting period) | fixed cost in `Volume Model` column E |
| Narration `Methods!B6:H10` (per-method inputs) | `Methods!I:L`, then `Summary` and the chart |
| Narration `Inputs!B16:B18` (labour rates) | all human costs in `Methods!J`, `Summary` row 15 |
| Business `Volume Inputs!C4:C12` (print cost) | `Unit Economics` rows 6, 22-24, Season P&L F, Cash Flow printer cash |
| Business `Scenario Inputs!B13:D13` (CAC) | `Unit Economics` rows 36-47, `Price & CAC!B20`, Dashboard profit and break-even |
| Business `90-Day Budget!B4:D13` | `Volume Inputs` Base fixed spend only, Funnel fully loaded CAC (via C7), Dashboard Base rows |
| Business `Global Inputs!B33:C44` (monthly shares) | `Cash Flow` only (timing); P&L and Dashboard profit do not change, peak gap does |
