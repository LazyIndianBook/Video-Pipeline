# Instructions: how to use the cost models

**Section:** `08_cost_models/`. **Applies to:** the four workbooks in `workbooks/` (v1 engine, v2 engine, narration, business). **Date basis of every default:** 13 October 2026.
**Companion files:** `README.md` (what is here), `COST_MODELS_EXPLAINED.md` (every sheet, input cell and formula), `CONSOLIDATED_COST_SCENARIOS.md` (all published tables and the reconciliation).

> **Three rules before you touch anything.** (1) Every default in these workbooks is a *planning estimate, not a quote, not a benchmark and not a forecast*; the workbooks say so in their own words (section 5 lists what must be replaced). (2) Change **one input at a time** and write down the output you expect before you look at it. (3) Never edit the files in `00_source/`; work on a copy of the workbook you need.

> **15 Oct 2026 addendum (RD-41, audit M6).** The founder has set review cash to **$0** (academic review, QA and repairs done in-house); review minutes are tracked as capacity, not money. To model this in a working copy, set the review/QA/repair **rates** to 0 and leave the **minutes** in place so the capacity rows (reviewer hours, FTE) still compute. Review-free totals (v1 $2.37, v2 hybrid $7.68, hybrid + premium narration $8.28 per video) and the relabelling of the business Rs 3,000 line as opportunity cost are in `README.md` §3.1 and `CONSOLIDATED_COST_SCENARIOS.md` E.8; the strong-to-cheap scenarios are in `13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §7.13. The originals and the steps below are unchanged; read every "human review dominates" line below as describing the workbook's cash model.

---

## 1. Set up a working copy

1. Copy the workbook you need out of `workbooks/` to a working folder, e.g. `cp workbooks/business_ExamLeaf_Business_Model.xlsx ~/cost_work/ExamLeaf_Business_Model_working.xlsx`. Keep the originals in `workbooks/` untouched so you can always return to the 13 October 2026 baseline.
2. Open in Excel, LibreOffice Calc or Numbers and let it **recalculate on open** (the files were produced by ChatGPT in a sandbox; the cached values in the `__values.csv` files are what Excel had stored). Check that the recalculated headline matches the table in `README.md` section 3 before editing; if it does not, stop and compare with the `csv/` folder.
3. **Do not rename or delete sheets**: formulas refer to sheets by name (`'Global Inputs'`, `'Unit Economics'`, `'Per Video'`, ...). Do not insert rows above the input blocks; the formulas use fixed cell addresses (e.g. `Inputs!B13`).
4. **Which cells are inputs.** v1 engine: blue cells in `Inputs!B5:B55`. v2 engine: `Inputs!B6:B66`. Narration: `Inputs!B6:B27` and the per-method inputs `Methods!B6:H10`. Business: blue-on-pale-yellow cells in `Global Inputs`, `Scenario Inputs`, `Volume Inputs`, `90-Day Budget` (and the small editable blocks on `Price & CAC` and `Funnel`). Everything else is a formula; do not overwrite formulas.
5. **Threaded comments.** Excel shows a note on each assumption (source and caveat). LibreOffice shows them as plain comments. The same text is in `COST_MODELS_EXPLAINED.md`.
6. **Integrity checks that exist in the files.** Business `Scenario Inputs!B30:D30` (channel mix must be 100%); `Global Inputs!B45:C45` (monthly shares must be 100%); `Unit Economics` row 13 (channel share check). Keep them at 1 when you edit shares.
7. **Independent cross-check.** `model_assumptions_and_results.json` holds the nine business results computed outside Excel; after any change to the business inputs you can recompute the Base 5,000 case by hand with the formulas in `COST_MODELS_EXPLAINED.md` section 4.5.

---

## 2. Which sheets and cells to edit first

Edit in this order: the inputs that move the answer most and that you can replace soonest with real numbers. Cell addresses are exact.

### 2.1 Video engine (v1 `Inputs`, v2 `Inputs`)

| Priority | What | v1 cells | v2 cells | Replace the placeholder with | Why first |
|---:|---|---|---|---|---|
| 1 | Human review minutes | `B37` academic min (45), `B39` QA min (15) | `B45:B47` academic (75/45/60), `B48:B50` QA (30/20/20), `B51:B53` repairs (45/20/30) | **Timed minutes from a real pilot lesson**, reviewer by reviewer | Human review is 88% of v1 variable cost and 78% of v2 hybrid; it also sets headcount (hybrid: 1,417 h = 8.85 FTE-months at 1,000 videos) |
| 2 | Labour rates | `B38` $20/h, `B40` $12/h, `B43` $25/h, `B46`/`B48`/`B50` $25/h | `B29` $20/h, `B30` $15/h, `B31` $20/h | Actual quotations from your academic reviewers and editors (the workbooks call them "planning labour rates") | Multiplies priority 1 |
| 3 | Narration | `B6` 8,000 chars, `B7` 20%, `B8` $0.08 | `B20` 8,000, `B21` 1.2, `B22` $0.10 | The actual provider-input character count of a finished script, and **one** agreed tariff (v1 uses $0.08, v2 and the narration workbook $0.10) | Small in dollars (about $1) but inconsistent across files |
| 4 | Render time and compute | `B26`:`B28` 8 vCPU / 16 GB / **45 min**, `B29` retry 20%, `B30`:`B31` AWS Fargate **US East** rates | `B60:B62` encode allowances $0.30/$0.50/$0.50 | A timed render of a full lesson with the chosen renderer on the chosen machine and region | The 45 minutes is "not a measured benchmark"; the `Measured Proof` sheet is 30-second silent clips and is not a substitute |
| 5 | Token budgets | `B9:B24` (Haiku/Sonnet/Sol/Opus in/out) | `B7:B8`, `B11:B12`, `B15:B16` (Sonnet/Opus/Haiku) | Metered token usage from a pilot lesson (input and output counts per call) | Assumptions, not observations; small in dollars ($1-2) |
| 6 | LLM tariffs and regeneration | `B11:B12`, `B15:B16`, `B19:B20`, `B23:B24`, `B25` 30% | `B9:B10`, `B13:B14`, `B17:B18`, `B19` 30% | Current pricing pages for the models you actually use (model labels differ between v1 and v2, see section 6) | Time-limited |
| 7 | Generated video | not in v1 | `B23` $0.10/s, `B24`/`B26` seconds (600 / 20), `B25`/`B27` attempts, `B28` stills | **Set `B26` = 0** unless generated clips are approved for a scene; `B24` only for the AI-heavy comparison | Default recommendation is zero generated seconds; this is $108 of the AI-heavy $158.98 |
| 8 | Fixed monthly and set-up | `B41`:`B43` ($100 + 4 h x $25), `B45:B50` (320 h x $25), `B55` | `B54:B59` ($250/$300/$900; $5,000/$10,000/$16,000) | Actual tool subscriptions; a scoped build quotation (the $8,000 is "illustrative ... not a promise of a mature system") | Dominates the 1-video case |
| 9 | Volume and period | `Volumes!B5:D5`, `Inputs!B44` period | `Volume Model!B5:B13`, `Inputs!B44` | Your planned monthly volume and programme length | Fixed cost is per period, not per video |
| 10 | Optional Remotion | `B51` switch (0), `B52:B54` | `B36:B38` | Only if you choose Remotion and have confirmed what a "billable render" is | Adds $100-$200/month |

### 2.2 Narration (`Inputs`, `Methods`)

| Priority | What | Cells | Replace with |
|---:|---|---|---|
| 1 | Review and editing minutes per method | `Methods!E6:F10` (premium TTS: 25 + 10) | Timed audio-review and edit minutes from an audition on **your** scripts, by a native subject reviewer. Doubling premium review minutes adds $8,333 at 1,000 videos (`Summary!B15` = $20,932.67) |
| 2 | Labour rates | `Inputs!B16` $20 review, `B17` $15 editing, `B18` $30 performer | Real quotations ("Obtain actual native subject-reviewer quotations") |
| 3 | Which method | `Methods!B6:H10` (fractions, record hours, GPU flag, fixed/month) | Your chosen mix; for a new mix copy a row and edit it, then add it to `Summary` |
| 4 | Speech minutes and characters | `Inputs!B7` 8.5 min, `B9` 7,800 characters, `B10` 20% retry | Actual transcript length and your measured regeneration rate |
| 5 | Provider tariffs | `Inputs!B11` $0.10/1k (v2/v3 reference), `B12` $0.12/min, `B24:B27` Gemini | The tariff of the model you will really use; Eleven v4 has **no** verified price ("TBD"); Cartesia needs an overage quote above 8 million credits |
| 6 | GPU and set-up | `Inputs!B19:B20`, `B21` $4,000 | A benchmark of the self-hosted model; a scoped quotation. `B21` is outside the operating totals |

### 2.3 Business (`Global Inputs`, `Scenario Inputs`, `Volume Inputs`, `90-Day Budget`)

Read order from the workbook: Dashboard, then Global Inputs, Scenario Inputs, Unit Economics, Cash Flow.

| Priority | What | Cells | Replace with |
|---:|---|---|---|
| 1 | **Print cost per copy** | `Volume Inputs!C4:C12` (Rs 190 ... 65) | **Three like-for-like written printer quotations per title, language and run** (roadmap week 2), at the true per-SKU batch size; also payment terms in `Global Inputs!B14:B16` (50% advance; lots 40% / 35% / remainder) |
| 2 | Customer acquisition cost | `Scenario Inputs!B13:D13` (Rs 220 / 120 / 70) | Observed paid/referral CAC from the pilot; use the `Price & CAC` grid and `B21` (maximum CAC) as the ceiling |
| 3 | Courier, packaging, marketplace fees, reserves | `Scenario Inputs!B14:D25` | Courier/aggregator account quotes (serviceable pincodes, weight, COD/RTO), marketplace fee schedule for books, observed returns |
| 4 | Sell-through and activation | `Scenario Inputs!B28:D28` (75/90/97%), `B26:D26` (activation 50/70/80%) | Observed sell-through by SKU; activation from the redemption logs |
| 5 | Prices and channel mix | `Scenario Inputs!B4:D11`, `Global Inputs!B4` MRP 549, `B13` 299 | Paid pilot results; partner commitments for bulk/trade shares |
| 6 | Tax | `Global Inputs!B5` (18%), `B11` (18% on hosting), `B6:B7` (gateway) | **Written GST classification advice** for the marketed book-and-video bundle; negotiated gateway rate |
| 7 | FX and streaming | `Global Inputs!B8` (Rs 90/USD), `B9` ($1 per 1,000 min), `B10` (400 min/book) | Current rate with buffer; actual viewing minutes per activated book |
| 8 | Fixed budgets | `90-Day Budget!B4:D13` (feeds Base-case fixed spend); Conservative/Optimistic fixed spend are typed in `Volume Inputs!D4,D6,D7,D9,D10,D12` | Real contracts and allocations; **re-derive row 6 ("Reviewed chapter videos", Rs 3,000 each) from the engine/narration workbooks** (section 4) |
| 9 | Seasonality | `Global Inputs!B33:C44` | The actual board exam timetable and title readiness (no official date is assumed) |
| 10 | Funnel | `Funnel!B4:B13`, `C18:C21`, `B25:D25` | Pilot funnel data; deduplicated stages |

---

## 3. How to run a sensitivity

**Generic procedure (works in every workbook).**

1. Pick the output you care about: engine `Total variable cost` (`UnitCosts!B20` v1, `Per Video!C17` v2 hybrid) or the 1,000-video total (`Volumes!D10`, `Volume Model!F10`); narration `Summary!D6`; business `Dashboard!F` (profit), `Dashboard!J` (break-even) and `Dashboard!H` (peak gap).
2. Write the baseline value. Change **one** input. Read the output. Write the difference. Restore the input.
3. Repeat for the next input; rank inputs by absolute change. The ones at the top are the ones to replace with real data first (section 2).
4. For a two-way view use Excel's *Data > What-If Analysis > Data Table*, or build a small grid by hand. The business workbook already contains one two-way grid (`Price & CAC`: realized price x CAC).
5. For break-even or maximum-CAC questions use *Goal Seek* on the output cell (e.g. set `Unit Economics!F43` to the contribution you need by changing `Scenario Inputs!C13`).
6. For scenario comparisons use the built-in cases (3 engine architectures; 5 narration methods; 9 business cases) rather than overwriting inputs.

**Worked sensitivities with expected results.** These were computed by re-implementing the workbook formulas (the re-implementation reproduces the stored baselines exactly: v1 $20.3676, v2 hybrid $34.3427, narration premium $12.4993, business Base 5,000 contribution Rs 118.1349 and break-even 10,158), so you can use them to check that your own edit works.

| Workbook | Edit (one at a time) | Expected result |
|---|---|---|
| v1 engine | Raise human review so `UnitCosts!B19` = $40 (the workbook's own sensitivity) | Variable cost $42.37/video (+$22); 1,000 videos $42,567.62 |
| v1 engine | `Inputs!B37` 45 -> 60 minutes | Human review $23.00; variable $25.37; 1,000 videos $25,567.62 |
| v1 engine | `Inputs!B40` QA rate $12 -> $15 | Human review $18.75; variable $21.12 |
| v1 engine | `Inputs!B28` render 45 -> 90 min | Rendering $0.7109; variable $20.72 (+$0.36): render time barely matters |
| v1 engine | `Inputs!B8` TTS $0.08 -> $0.10 | Narration $0.960; variable $20.56 |
| v1 engine | `Inputs!B25` LLM regeneration 30% -> 100% | LLM $1.591; variable $20.92 |
| v1 engine | `Inputs!B51` Remotion switch 0 -> 1 | Totals $320.37 / $2,336.76 / $20,767.62 (+$100 / +$100 / +$200) |
| v2 engine | `Inputs!B26` hybrid generated seconds 20 -> 0 | Hybrid variable $30.34 (message 10: "approximately $30.34/video") |
| v2 engine | `Inputs!B46` hybrid academic review 45 -> 60 min | Hybrid variable $39.34; reviewer hours at 1,000 1,667 |
| v2 engine | `Inputs!B52` hybrid repairs 20 -> 40 min | Hybrid variable $41.01 |
| v2 engine | Hybrid minutes 85 -> 120 (`B46`=60, `B49`=30, `B52`=30) | Hybrid variable $45.18; 2,000 h = 12.5 FTE-months at 1,000 |
| v2 engine | `Inputs!B11:B12` Opus review tokens x2 | Hybrid LLM $2.431; variable $35.06 |
| v2 engine | `Inputs!B22` TTS tariff $0.10 -> $0.20 | Hybrid variable $35.30 |
| Narration | Premium: `Methods!E6` review 25 -> 50 min | `Summary!D6` = $20,932.67 (workbook's own sensitivity); hours at 1,000 1,000 |
| Narration | `Inputs!B11` $0.10 -> $0.20 per 1,000 chars | Premium variable $13.44; 1,000 videos $13,535.33 |
| Narration | `Inputs!B16` reviewer rate $20 -> $30 | Premium variable $16.67; 1,000 videos $16,766.00 |
| Narration | `Methods!F6` editing 10 -> 20 min | Premium variable $15.00; hours at 1,000 750 |
| Business Base 5,000 | `Volume Inputs!C8` print cost Rs 105 -> 115 | Contribution Rs 107.02; break-even 11,213 copies; profit Rs -664,885. (Each Rs 1 of print cost costs Rs 1.11 per retained book because the unsold copies are charged to the retained ones) |
| Business Base 5,000 | `Scenario Inputs!C13` CAC Rs 120 -> 220 | Contribution Rs 88.13; break-even 13,616; profit Rs -759,325 |
| Business Base 5,000 | `Scenario Inputs!C28` sell-through 90% -> 75% | Copies printed 6,667; contribution Rs 94.80; break-even 12,658; profit Rs -725,980 |
| Business Base 5,000 | `Scenario Inputs!C4` DTC realized price Rs 479 -> 449 | Contribution Rs 107.01; break-even 11,214 |
| Business Base 5,000 | `Scenario Inputs!C12` DTC basket 1.5 -> 1.2 | Contribution Rs 103.36; break-even 11,610 |
| Business Base 5,000 | `Scenario Inputs!C26` activation 70% -> 80% | Contribution Rs 113.89; break-even 10,537 (more activation = more streaming cost) |
| Business Base 5,000 | `90-Day Budget!C13` contingency +Rs 1,00,000 (fixed spend Rs 13 lakh) | Break-even 11,005; profit Rs -709,325; contribution unchanged |
| Business Base 50,000 | Add a separate Rs 10 lakh engineering project (e.g. raise `90-Day Budget!D10` or D13 by Rs 10,00,000) | Profit falls from Rs 34.07 lakh to Rs 24.07 lakh (message 06 section 11.5) and the funding need rises; see section 4.3 step 3 |
| Business (all) | Read `Season P&L` column M | Profit if output GST were 0%: the workbook's built-in tax sensitivity |

**Record what you learn** in a small table (input, baseline, changed, output baseline, output changed, delta) next to the working copy; writing down the expected change before you look at the result is what turns the model into a decision tool.

---


## 4. Combine engine + narration + business without double counting

The three USD workbooks price overlapping work (the same narration, the same audio review) and the INR workbook prices only one thing from them (the "Reviewed chapter videos" line). ChatGPT warned twice not to add the narration review on top of the engine review, but gave no recipe. This is the recipe; the evidence for each step is the overlap table in `CONSOLIDATED_COST_SCENARIOS.md` section E.2.

### 4.1 Decide the scope of each model, once

| Decision | Recommended default | Why |
|---|---|---|
| Whole-video model (one of) | **v2 hybrid** (`Per Video` column C) for the architecture comparison; v1 for the simple reusable-component baseline | v2 is the later, three-architecture model and already includes encode, alignment/audio and repair lines; v1 is cheaper because it assumes an established component library and fewer human minutes |
| Narration model | `narration` workbook, one method (default premium commercial TTS, `Methods` row 6) | It is the only model that prices voice methods, rates and tariffs separately |
| Business model | `business` workbook, Base case | It is the only model with INR, GST, print, channel and cash |

### 4.2 Roll-up steps (USD per finished 10-minute video, variable cost)

1. **Start from the whole-video engine variable cost.** v2 hybrid: $34.34 (`Per Video!C17`); v1: $20.37 (`UnitCosts!B20`).
2. **Delete the engine's audio lines.** v2: `Narration generation` ($0.96, `Per Video!C6`) and `Alignment/audio allowance` ($0.10, `C10`). v1: `Narration with regeneration` ($0.768, `UnitCosts!B11`; v1 has no separate alignment line, its ASR line `B13` is $0.03 and may be kept or dropped, but be consistent).
3. **Add the narration model's cost for the chosen method.** Machine part (`Methods!I`): $1.666 for premium TTS; human part (`Methods!J`): $10.83 (25 review + 10 editing minutes).
4. **Settle the human overlap explicitly.** The engine's academic review (45 min) already covers "the entire final lesson", which includes the narration; the engine's QA covers "audio, captions, continuity". Decide how many of the narration's 35 minutes are *already inside* the engine minutes:
   * all of them (floor): add only the narration machine part. v2 hybrid = **$34.95**; 
   * none of them (ceiling): add machine + human. v2 hybrid = **$45.78**;
   * in between: add `(35 - minutes already counted)` x the blended rate.
   Put the decision in writing next to the numbers; a pilot with timed minutes replaces the guess.
   *(15 Oct 2026: under RD-41 floor and ceiling are the same in cash, $8.28 for v2 hybrid; the overlap decision still sets review-minute capacity.)*
5. **Use one set of unit rates.** The engine files use QA $12/h (v1) or $15/h (v2), repairs $20/h; the narration file uses reviewer $20/h, editor $15/h. Pick one table of rates and edit all workbooks to it before comparing totals.
6. **Use one narration tariff and one character count** (v1: $0.08, 8,000 chars; v2: $0.10, 8,000; narration: $0.10, 7,800). Edit v1 `B8`, v2 `B22`, narration `Inputs!B11` and the character cells to the same values.
7. **Fixed monthly and set-up: choose one of each.** Engine fixed ($200 / $300) and narration fixed ($100) both cover storage, tools and orchestration; use one allowance (or the larger) and state it. Engine set-up ($8,000 / $10,000) and the narration reserve ($4,000) have different scopes; add both only if the engine template hours do not already include voice/audio work (v1 includes 20 design/voice hours).
8. **Do not add engine volume economics to the pilot.** Compute the pilot's video count from the business plan (40 reviewed chapter videos in the pilot) and price *that* count, including fixed and set-up, not the 1,000-video average.

### 4.3 Bring the result into the business model (USD to INR)

1. Convert at the business workbook's planning rate (`Global Inputs!B8` = Rs 90/USD): combined hybrid + premium narration = Rs 3,145 to Rs 4,120 per video (floor to ceiling); v1-based = Rs 1,914 to Rs 2,889.
2. Compare with `90-Day Budget!B6` ("Reviewed chapter videos", 40 x Rs 3,000 = Rs 1,20,000, "including allocated human review and machine costs"). Rs 3,000 = $33.33. *(15 Oct 2026: under RD-41 treat B6 as opportunity cost; its cash part is ≈ Rs 745 per video, ≈ Rs 29,800 for 40 videos.)* If your roll-up is higher, raise B6/C6/D6; that changes the **Base** fixed spend only (via `Volume Inputs!D5,D8,D11`). If you also want Conservative/Optimistic to move, edit `Volume Inputs!D4,D6,D7,D9,D10,D12` by the same amount.
3. **Add the engine and narration one-time budgets as a separate line.** The business model's lean launch contains *no* engine R&D ("A full bespoke video platform or 40-Skill engineering project is NOT quietly included in the lean launch"). At Rs 90/USD: v2 hybrid $10,000 = Rs 9.0 lakh; narration $4,000 = Rs 3.6 lakh; v1 $8,000 = Rs 7.2 lakh. Add as a new row in `90-Day Budget` (or raise B13) so the cash flow and break-even see it; the pilot ceiling of Rs 8 lakh cannot absorb it. The example in message 06: a Rs 10 lakh engineering project lowers Base 50,000 profit from Rs 34.07 lakh to Rs 24.07 lakh.
4. **Do not double count against business lines that already exist:** streaming/viewer delivery (`Unit Economics` row 26, per activated book), `90-Day Budget` row 9 (fixed hosting, tools, storage) versus engine fixed overhead, and row 7 (Reels) versus the engine's optional three-Short package ($4.316 per lesson = Rs 388): count Shorts in one place.
5. Keep engine/narration **USD before tax**; apply tax treatment of imported services once, outside the models, after CA advice.

---

## 5. What must be replaced with real quotes before any commitment

Everything in the workbooks is an estimate; these are the items where the estimate is weakest or the money is largest. "Source status" is the workbook's own label.

| Item | Where in the workbooks | Placeholder (13 Oct 2026) | Source status in the workbook | Obtain |
|---|---|---|---|---|
| **Printer** | business `Volume Inputs!C4:C12`; `Global Inputs!B14:B16` | Rs 190/160/135 (500), 125/105/88 (5,000), 95/78/65 (50,000) per copy; 50% advance; 3 lots | "Planning assumption, not an obtained quotation ... depend on copies PER SKU and batch"; "not confirmed quotes" | Three written quotes for the same spec (256 pp, 7 x 10 in, 70 GSM, cover, binding, activation insert, freight, tax, spoilage tolerance, payment terms) per title, language, batch |
| **Courier / fulfilment** | business `Scenario Inputs` rows 14-17, 22-25 | Rs 85/65/55 per order; freight Rs 15/10/8; reserves | "Unquoted planning assumption" | Courier/aggregator account quotes by weight and pincode, COD/RTO rates; India Post written eligibility for the packed SKU |
| **Marketplace** | `Scenario Inputs` rows 18-19, 25 | all-in fee Rs 105/90/80; ads Rs 45/25/15 | "All-in model fee is an assumption, not the referral percentage" | Marketplace fee schedule for the exact category and price band |
| **CAC and conversion** | `Scenario Inputs` row 13; `Funnel` | Rs 220/120/70; 5% paid-order rate | "Incremental per-customer acquisition cost sensitivity, not observed ExamLeaf costs"; "not an industry benchmark" | Observed pilot CAC and funnel; keep deduplicated stages |
| **Sell-through, activation, trade/bulk shares** | `Scenario Inputs` rows 8-11, 26, 28 | 75/90/97%; 50/70/80% | "Unquoted planning assumption" | Partner commitments and observed sell-through by SKU |
| **GST classification** | `Global Inputs!B5`, `B11` | 18% on the whole bundle; 18% non-recovered hosting tax | "NOT legal classification"; "Obtain written advice" | Written CA/counsel review of the marketed book + video package |
| **FX** | `Global Inputs!B8` | Rs 90/USD | "Budget buffer, NOT a current FX quote" | Current rate plus buffer at the date of spend |
| **Video delivery** | `Global Inputs!B9:B10` | $1 per 1,000 min (published); 400 min per activated book | rate "Published"; minutes "Planning assumption" | Actual viewing minutes per activated book from pilot analytics |
| **TTS tariffs** | v1 `B8`; v2 `B22`; narration `B11`, `B12`, `B24:B27` | $0.08 / $0.10 per 1,000 characters; $0.12/min speech-to-speech; Gemini $0.50/$9 now, $1/$18 from 1 Jan 2027 | "v2/v3 published reference ... NOT a verified Eleven v4 quote"; Eleven v4 "TBD"; Cartesia "Obtain higher tier / overage quote"; OpenAI old TTS "Do not use for new production" | Account/model quotation from the provider you will use; check lifecycle notices |
| **LLM tariffs** | v1 `B11:B24`; v2 `B9:B18` | see section 6 | "Published API tariff" but model names differ between files | Current pricing page for the exact model IDs |
| **Render benchmark** | v1 `B26:B31`; v2 `B60:B62`; v2 `Measured Proof` | 45 min on 8 vCPU / 16 GB (US East Fargate); $0.30-$0.50 encode | "45 minutes is an unmeasured planning assumption"; "Fargate is a US East rate example, not Mumbai pricing"; Measured Proof = 30-s silent clips | A timed full-lesson render, with narration, on your renderer and region |
| **Reviewer, editor, performer rates** | v1 `B38,B40,B43`; v2 `B29:B31`; narration `B16:B18` | $20 / $12-15 / $20-25 / $30 per hour | "Planning labour rate"; "Labour assumption, not a market survey"; "Illustrative; licensing/buyout fees require a separate agreement" | Quotations from native subject reviewers and editors; voice buyout/licence terms |
| **GPU / self-hosting** | v2 `B32:B34`; narration `B19:B20` | $0.80-$1/h; real-time factor 2 | "No GPU benchmark or supplier quote obtained"; "No local neural TTS benchmark performed" | A benchmark of the chosen model on the chosen hardware |
| **Generated video** | v2 `B23:B28` | $0.10/s, 600 s x 1.8 attempts (AI-heavy) | "Runway illustrative route ... not Higgsfield quote" | Exact model/resolution/audio route quote; default zero seconds |
| **Remotion billing** | v1 `B54`; v2 `B38` | 20 billable renders per video | "Unconfirmed accounting assumption" | Vendor confirmation of what counts as a billable render |
| **Set-up / build budgets** | v1 `B45:B50`; v2 `B57:B59`; narration `B21`; business `90-Day Budget` | $8,000; $5,000/$10,000/$16,000; $4,000; Rs 6.5 lakh pilot | "Illustrative ... not a promise of a mature system"; "Planning allocation, not a supplier or employment quote" | Scoped, quoted work packages |
| **Localization** | not priced | excluded ("extra localization", "additional languages") | "A second language requires new performance, QA and timeline verification" | Per-language native-review and re-recording quotes (Assamese needs a separate acceptance gate) |

---

## 6. Model lifecycle: the names and prices in the workbooks are as of 13 October 2026

* **Claude model names and prices are a snapshot.** v1 labels its LLMs "Haiku 5.5", "Sonnet 5.5", "Opus 5.5" plus OpenAI `gpt-6.1-sol` at $0.10/$0.50, $2/$10, $4/$20 and $2/$10 per million input/output tokens. v2 (message 10) uses "Haiku 4.5", "Sonnet 4.6", "Opus 4.6" at $1/$5, $3/$15, $5/$25. Those are different price lists for different labels in two ChatGPT outputs on the same research date, so the LLM cost moves from $1.03 (v1) to $1.72 (v2) per video. Treat both as unverified: re-read the provider pricing pages, confirm the exact model IDs you will deploy (models are retired and re-priced on published schedules), and overwrite the tariff cells (v1 `B11:B24`, v2 `B9:B18`). In Claude Code the `claude-api` skill can list current model IDs and prices.
* **No discounts are modelled.** v1: "No promotional prices, free tiers, batch discounts or caching savings assumed." Real invoices may be lower; prices may also rise (Gemini 3.8 Flash TTS doubles from 1 Jan 2027).
* **Deprecations.** OpenAI `tts-1`, `tts-1-hd` and listed `gpt-4o-mini-tts` snapshots shut down 6 Jan 2027; the replacement is a realtime model with different semantics. Check "Deprecation gate" (v1 ReadMe) before adopting any speech Skill default.
* **Time-limited tariffs.** ElevenLabs: a promotion ending 12 October was excluded; Eleven v4 unpriced. Cartesia plan allowances do not scale to 1,000 lessons. Re-check every URL in the `Source` columns on the day you commit money.
* **Accounting caveats that age.** Fargate US-East rates; R2 storage; Cloudflare Stream $1 per 1,000 delivered minutes; Razorpay 2% + GST (promotion excluded); Amazon India books referral fee; India Post slabs. All "checked 13 October 2026".
* **Refresh routine.** Message 06's closing line recommends "a monthly syllabus, competitor-price, and service-tariff alert". At minimum: before each stage gate in the 90-day roadmap, re-open `Inputs`, update tariffs and dates, and record the new "Checked" date.

---

## 7. Common mistakes this directory is designed to prevent

1. Reading "machine cost $2.37 per video" as "videos cost $2". It is $20.37 (v1) to $34.34 (v2 hybrid): human review dominates. *(15 Oct 2026: in the workbook's cash model. Under RD-41 review cash is $0, so cash is $2.37 to $7.68, and review minutes are the throughput constraint.)*
2. Adding narration review to engine review (section 4), or adding engine volume economics to a 40-video pilot.
3. Treating the nine business scenarios as 100x multiples of the pilot ("Higher cases fund an expanded season; they are not simply 100x the pilot") or as forecasts.
4. Using the static break-even outside its cost tier ("Do not interpret a positive unit contribution as total profitability or use static break-even outside the modeled cost tier").
5. Deducting the fully loaded marketing CAC (Rs 186.67) in profit a second time.
6. Forgetting that profit is not cash: Base 50,000 shows a Rs 34.07 lakh profit yet needs Rs 52.09 lakh of funding capacity; Base 5,000 loses Rs 6.09 lakh but needs Rs 12.71 lakh; across all nine cases the funding need (peak gap + 15% headroom) runs from Rs 6.03 to Rs 95.52 lakh.
7. Editing `90-Day Budget` and expecting Conservative/Optimistic to move (only Base is linked).
8. Editing descriptive cells that no formula reads (v2 `B6`, `B39`; narration `B6`, `B8`; business `Global Inputs!B20:B26`).
9. Taking the `Measured Proof` render times (27-29 s for 30 s of silent 2D video) as a production render benchmark.
10. Presenting any number from these files to a partner, lender or investor as a quote or forecast.

---

## 8. Where to go next

* Understand a number: `COST_MODELS_EXPLAINED.md` (sheet and cell level).
* See the published tables and the reconciliation: `CONSOLIDATED_COST_SCENARIOS.md`.
* Why the plan is built this way: `../04_video_engine/` (architecture, v1 to v2 evolution), `../05_narration_system/` (voice, provider comparison, pipeline), `../06_skills_library/` (the 40 / 32 / 15 Skill backlogs behind the set-up budgets), `../01_business_model/` (business plan, runbook, Reel backlog), `../09_research_and_evidence/` (evidence register, cited sources).
