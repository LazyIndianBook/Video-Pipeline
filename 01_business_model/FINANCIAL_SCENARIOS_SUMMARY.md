# FINANCIAL_SCENARIOS_SUMMARY - ExamLeaf nine scenarios, unit economics, break-even, cash, CAC limits, tax warning

> ## READ THIS FIRST - what these numbers are and are not
> - **These are planning scenarios, not sales forecasts or supplier quotations.** (Response, Executive verdict.)
> - Verified public facts (provider tariffs etc.) are separated from **assumptions**. Proposed prices, printing costs, courier costs, CAC, sell-through, staffing allocations, conversion rates and campaign targets are **assumptions** (Response, Research-date note; Runbook "Sources"; workbook `Read_Me`). **None of the modeled print costs are quotes.**
> - Research / model date: **13 October 2026.** Currency INR. 1 lakh = 100,000; 1 crore = 100 lakh.
> - "Sales" = **retained** book copies: paid, net of refunds/returns. Not printed copies, customers or orders. Trade revenue = the publisher's discounted realization, not consumer MRP.
> - Profit = **operating profit before financing and income tax**, after the specified variable and fixed costs. No borrowing interest, no income tax, no input-tax-credit recovery assumed.
> - Output GST of **18% on the entire marketed book-plus-video bundle** is a *prudent modelling scenario, NOT a legal classification opinion* (see section 11 "Tax warning").
> - The three scales fund **different scopes** (500 = two-title pilot with allocated project labour; 5,000 = expanded season; 50,000 = up to six titles, "not all India"). They are **not simple multiples** of one unchanged operation.
> - Static break-even is a *single-cost-tier* calculation; it must be re-costed (printing, staffing, distribution) at every new volume. A positive unit contribution is not total profitability.
> - Everything below the "Response verbatim" labels is copied from `FULL_business_model_launch_financial_plan.md`. Everything labelled "Workbook detail" is generated from `workbook_csv/*__values.csv` (rounded for display as stated) and cross-checked against `toolkit/Model_Assumptions_and_Results.json`.

## 1. Headline interpretation (Response verbatim - Executive verdict)

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

## 2. The nine scenarios

### 2.1 Response verbatim (section 11.1)

#### 11.1 Nine scenarios

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

##### Interpretation

**500 sales:** pay for a controlled test and reusable intellectual property, not an expectation of immediate payback.

**5,000 sales:** enough to demonstrate demand, but not automatically enough to fund a broad catalogue and team.

**50,000 sales:** can support attractive economics, but the conservative case shows why scaling a weak offer can destroy capital.

The cases fund different scopes: a two-title pilot, an expanded season, and a larger catalogue. They are not simple multiples of one unchanged operation.

### 2.2 Workbook detail - full P&L lines for each of the nine cases (INR, rounded to the nearest rupee unless stated)

| Case | Retained books | Copies printed | Landed print INR/copy | Publisher gross realization (incl. modeled GST) | Output GST reserve (18%) | Net publisher revenue (ex-GST) | Print cash / edition expense | Other variable cost | Contribution (total) | Fixed spend | Operating profit | Operating margin | Profit if output GST = 0% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Conservative \| 500 | 500 | 667 | 190 | 189,296 | 28,876 | 160,421 | 126,730 | 82,939 | -49,248 | 750,000 | -799,248 | -498.2% | -770,372 |
| Base \| 500 | 500 | 556 | 160 | 215,075 | 32,808 | 182,267 | 88,960 | 64,861 | 28,445 | 650,000 | -621,555 | -341.0% | -588,746 |
| Optimistic \| 500 | 500 | 516 | 135 | 233,359 | 35,597 | 197,762 | 69,660 | 52,825 | 75,277 | 600,000 | -524,723 | -265.3% | -489,126 |
| Conservative \| 5,000 | 5,000 | 6,667 | 125 | 1,892,962 | 288,757 | 1,604,206 | 833,375 | 829,387 | -58,556 | 1,500,000 | -1,558,556 | -97.2% | -1,269,799 |
| Base \| 5,000 | 5,000 | 5,556 | 105 | 2,150,750 | 328,081 | 1,822,669 | 583,380 | 648,615 | 590,675 | 1,200,000 | -609,325 | -33.4% | -281,245 |
| Optimistic \| 5,000 | 5,000 | 5,155 | 88 | 2,333,588 | 355,971 | 1,977,617 | 453,640 | 528,249 | 995,727 | 1,000,000 | -4,273 | -0.2% | 351,698 |
| Conservative \| 50,000 | 50,000 | 66,667 | 95 | 18,929,625 | 2,887,570 | 16,042,055 | 6,333,365 | 8,293,866 | 1,414,824 | 5,000,000 | -3,585,176 | -22.3% | -697,606 |
| Base \| 50,000 | 50,000 | 55,556 | 78 | 21,507,500 | 3,280,805 | 18,226,695 | 4,333,368 | 6,486,149 | 7,407,178 | 4,000,000 | 3,407,178 | 18.7% | 6,687,983 |
| Optimistic \| 50,000 | 50,000 | 51,547 | 65 | 23,335,875 | 3,559,710 | 19,776,165 | 3,350,555 | 5,282,492 | 11,143,118 | 3,500,000 | 7,643,118 | 38.6% | 11,202,828 |

Source: `Season_P&L` sheet (and `Unit_Economics` for copies/print cost). The last column is the workbook's **separate zero-output-tax sensitivity - "not a recommendation to claim exemption"** (see section 11).

### 2.3 Workbook detail - break-even, peak cash gap and funding requirement (INR lakh unless stated)

| Case | Net revenue | Contribution INR/book | Fixed | Operating profit | Margin (profit / net revenue) | Peak cumulative cash gap | Funding incl. +15% headroom | Static break-even (copies) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Conservative \| 500 | 1.60 | -98.50 | 7.50 | -7.99 | -498.2% | 7.99 | 9.19 | No unit break-even |
| Base \| 500 | 1.82 | 56.89 | 6.50 | -6.22 | -341.0% | 6.22 | 7.15 | 11,426 |
| Optimistic \| 500 | 1.98 | 150.55 | 6.00 | -5.25 | -265.3% | 5.25 | 6.03 | 3,986 |
| Conservative \| 5,000 | 16.04 | -11.71 | 15.00 | -15.59 | -97.2% | 17.96 | 20.65 | No unit break-even |
| Base \| 5,000 | 18.23 | 118.13 | 12.00 | -6.09 | -33.4% | 11.06 | 12.71 | 10,158 |
| Optimistic \| 5,000 | 19.78 | 199.15 | 10.00 | -0.04 | -0.2% | 8.43 | 9.69 | 5,022 |
| Conservative \| 50,000 | 160.42 | 28.30 | 50.00 | -35.85 | -22.3% | 83.06 | 95.52 | 176,701 |
| Base \| 50,000 | 182.27 | 148.14 | 40.00 | 34.07 | 18.7% | 45.29 | 52.09 | 27,001 |
| Optimistic \| 50,000 | 197.76 | 222.86 | 35.00 | 76.43 | 38.6% | 34.40 | 39.56 | 15,705 |

Source: `Dashboard` sheet; identical to `results[]` in `Model_Assumptions_and_Results.json` (profit, contribution, funding, break-even all agree). Workbook caption under the Dashboard table: **"BASE CASE: 500 copies validate execution; 5,000 still do not recover full season costs. At 50,000 copies, positive profit requires disciplined pricing, sell-through, acquisition and collections. This is a model, not a sales forecast."** Dashboard title: "SCALE IS NOT A SUBSTITUTE FOR UNIT ECONOMICS".

Cross-check log (organizer): the response 11.1 table agrees with the Dashboard to 2 decimals for net revenue, contribution/book, fixed costs and profit in all 9 rows; JSON profit, contribution, funding and break-even agree with the Dashboard in all 9 rows. No discrepancies found.

## 3. Inputs

### 3.1 Verified versus estimated (Response verbatim, section 10.1, includes the Tax warning)

#### 10.1 What is verified versus estimated?

| Input | Status |
|---|---|
| Razorpay standard 2% platform fee plus GST | Published provider pricing; promotional periods excluded |
| Amazon Books referral fee of 2% for prices above ₹250 through ₹500 | Published category rate; not the total selling cost |
| Cloudflare delivery at $1 per 1,000 delivered minutes | Published provider tariff |
| Printing, courier cost, CAC, sell-through, staffing and conversion rates | Planning assumptions requiring validation |
| ₹90/USD | Budget conversion assumption, not a live exchange-rate quote |
| 18% output GST on the bundle | Cautious model assumption, not a classification conclusion |

Amazon also charges other fees, and book bundles may have different category treatment. Do not interpret a low or zero referral rate as free distribution. [cite-token: turn480908view0, turn874416view6, turn480908view3]

##### Tax warning

**Do not assume the entire book-plus-premium-video offer is exempt merely because it contains a printed book.**

The actual treatment depends on the supplies, contract and applicable classification. GST guidance distinguishes composite supplies from mixed supplies. The workbook therefore includes a cautious 18% case and a separate zero-output-tax sensitivity—not a recommendation to claim exemption. [cite-token: turn250458view2]

Obtain written advice before finalizing prices and invoices.

### 3.2 Scenario assumptions (Response verbatim, section 10.2)

#### 10.2 Scenario assumptions

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

### 3.3 Workbook detail - complete `Scenario_Inputs` sheet (all 25 assumptions)

| Assumption | Conservative | Base | Optimistic | Unit |
|---|---|---|---|---|
| DTC realized per book, after bundle/coupon mix | 429 | 479 | 499 | INR |
| Marketplace selling price | 449 | 499 | 519 | INR |
| Bulk discount from MRP | 0.3 | 0.25 | 0.2 | rate |
| Combined distributor/retailer discount from MRP | 0.45 | 0.4 | 0.35 | rate |
| Direct-to-consumer unit share | 0.3 | 0.45 | 0.6 | rate |
| Institutional/bulk unit share | 0.2 | 0.2 | 0.2 | rate |
| Trade unit share | 0.35 | 0.25 | 0.15 | rate |
| Marketplace unit share | 0.15 | 0.1 | 0.05 | rate |
| DTC retained books per customer/order | 1.2 | 1.5 | 1.8 | books/order |
| DTC incremental CAC; paid/referral blended | 220 | 120 | 70 | INR/customer |
| DTC courier per order | 85 | 65 | 55 | INR/order |
| Packaging per DTC order / marketplace unit | 14 | 12 | 10 | INR |
| Bulk freight per book | 15 | 10 | 8 | INR/book |
| Trade freight per book | 12 | 8 | 6 | INR/book |
| All-in marketplace selling/closing/fulfillment cash fee | 105 | 90 | 80 | INR/book |
| Marketplace advertising per retained book | 45 | 25 | 15 | INR/book |
| Bulk field servicing / partner acquisition | 10 | 7 | 5 | INR/book |
| Trade field servicing cost | 12 | 8 | 5 | INR/book |
| DTC reverse-logistics/chargeback reserve | 18 | 10 | 5 | INR/book |
| Bulk leakage/collections reserve | 3 | 2 | 1 | INR/book |
| Trade bad debt/claims reserve | 6 | 4 | 2 | INR/book |
| Marketplace reverse-logistics reserve | 25 | 18 | 12 | INR/book |
| Book entitlement activation rate | 0.5 | 0.7 | 0.8 | rate |
| Service/OTP/support per retained book | 12 | 8 | 6 | INR/book |
| Retained copies / all copies printed | 0.75 | 0.9 | 0.97 | rate |

Basis stated for every row: "Planning estimate; replace with paid pilot and supplier/account quotations."  Channel-mix check row = 100% in all three scenarios (DTC + institutional/bulk + trade + marketplace).

Rate rows are fractions (e.g. 0.3 = 30%). Base channel mix: **45% DTC, 20% institutional, 25% trade, 10% marketplace** (conservative 30/20/35/15; optimistic 60/20/15/5).

### 3.4 Workbook detail - print cost and fixed spend by case (`Volume_Inputs`)

| Case | Retained books | Landed print INR/book | Season fixed spend INR |
|---|---:|---:|---:|
| Conservative | 500 | 190 | 750,000 |
| Base | 500 | 160 | 650,000 |
| Optimistic | 500 | 135 | 600,000 |
| Conservative | 5,000 | 125 | 1,500,000 |
| Base | 5,000 | 105 | 1,200,000 |
| Optimistic | 5,000 | 88 | 1,000,000 |
| Conservative | 50,000 | 95 | 5,000,000 |
| Base | 50,000 | 78 | 4,000,000 |
| Optimistic | 50,000 | 65 | 3,500,000 |

Print-cost status (every row): "Estimate incl. cover, binding, activation insert, inbound freight and non-recovered tax."  Fixed-cost scope: "500: two-title pilot; 5,000: expanded season; 50,000: up to six titles, not all India."  The print costs "must be achieved at the actual **per-SKU phased batch sizes**. They are not confirmed quotes." (Response 10.2). Quote **per title, language, and batch** - 50,000 aggregate sales split across many SKUs do not give every SKU the economics of a 50,000-copy run.

### 3.5 Workbook detail - complete `Global_Inputs` sheet

| Input | Value | Unit | Interpretation / limitation | Source / basis |
|---|---|---|---|---|
| MRP per subject book | 549 | INR | Proposed test price, not observed ExamLeaf sales. | Planning assumption |
| Bundle output GST | 0.18 | rate | Prudent 18% stress/base tax input, NOT legal classification. All cases use it. | https://gstcouncil.gov.in/sites/default/files/e-version-gst-flyers/Composite%20supply%20%26%20Mixed%20Supply-050819.pdf |
| Payment gateway fee | 0.02 | rate | Standard domestic pricing; promotional free period excluded. | https://razorpay.com/pricing/ |
| GST on gateway fee | 0.18 | rate | Applied to gateway service fee; no input credit assumed. | https://razorpay.com/pricing/ |
| Planning INR per USD | 90 | INR/USD | Budget buffer, NOT a current FX quote. | Planning assumption |
| Stream delivery per 1,000 min | 1 | USD | Published usage price; storage separate in fixed infrastructure. | https://developers.cloudflare.com/stream/pricing/ |
| Delivered minutes per activated book | 400 | minutes | Lifetime-of-edition delivery reserve, including repeat viewing; not just first month. | Planning assumption |
| Non-recovered tax on hosting | 0.18 | rate | Prudent cash-cost allowance; actual invoice/credit treatment to be checked. | Planning assumption |
| Funding headroom | 0.15 | rate | Added to modeled peak cash deficit, not expensed in P&L. | Planning assumption |
| Digital-only subject price | 299 | INR | One-time edition access; no assumed digital revenue in book scenarios. | Planning assumption |
| Printer advance | 0.5 | rate | 50% one month before receipt; balance on receipt. Obtain written terms. | Planning assumption |
| First print lot share | 0.4 | rate | Print receipts in months 2, 4 and 5; other lots are 35% and remainder. | Planning assumption |
| Second print lot share | 0.35 | rate | Inventory is not all printed upfront. | Planning assumption |
| Digital acquisition cost | 80 | INR/customer | Incremental paid/referral acquisition, excludes fixed organic production. | Planning assumption |
| Digital support/refunds reserve | 12 | INR/customer | Provision for user support and refund leakage, not unlimited support. | Planning assumption |
| Digital activation usage rate | 1 | rate | Digital purchasers conservatively assumed active. | Planning assumption |
| DTC single test price | 499 | INR | Standard-service delivered price; disclose remote-area exceptions before payment. | Planning assumption |
| Two-book delivered bundle | 949 | INR | Customer offer; actual realized per-book input reflects coupons and order mix. | Planning assumption |
| Science/maths prototype pages | 256 | pages | Check physical pagination before a fixed page commitment. | Planning assumption |
| Prototype trim width | 7 | inches | Proposed 7 x 10 inch interior. | Planning assumption |
| Prototype trim height | 10 | inches | Proposed 7 x 10 inch interior. | Planning assumption |
| Interior paper | 70 | GSM | Compare opacity and writing comfort on actual proofs. | Planning assumption |
| Metres per inch | 0.0254 | m/in | Exact conversion. | Definition |

**Cash timing profile** (workbook heading: "CASH TIMING | MONTH 1 IS START OF CONTENT BUILD; NOT A VERIFIED DEMAND FORECAST"):

| Relative month | Retained sales share | Fixed spend share |
|---:|---:|---:|
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

Share checks: retained sales shares sum to 1; fixed spend shares sum to 1.0000000000000002 (floating-point).

## 4. Unit economics

### 4.1 Base economics at 5,000 retained sales (Response verbatim, section 10.3)

#### 10.3 Base economics at 5,000 retained book sales

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

### 4.2 Workbook detail - full `Unit_Economics` sheet, INR per retained book unless stated (all nine cases)

| Line (INR per retained book) | Conservative \| 500 | Base \| 500 | Optimistic \| 500 | Conservative \| 5,000 | Base \| 5,000 | Optimistic \| 5,000 | Conservative \| 50,000 | Base \| 50,000 | Optimistic \| 50,000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Retained books | 500 | 500 | 500 | 5,000 | 5,000 | 5,000 | 50,000 | 50,000 | 50,000 |
| Total copies printed | 667 | 556 | 516 | 6,667 | 5,556 | 5,155 | 66,667 | 55,556 | 51,547 |
| Landed print per copy | 190.00 | 160.00 | 135.00 | 125.00 | 105.00 | 88.00 | 95.00 | 78.00 | 65.00 |
| Fixed season spend | 750,000 | 650,000 | 600,000 | 1,500,000 | 1,200,000 | 1,000,000 | 5,000,000 | 4,000,000 | 3,500,000 |
| DTC share | 30.0% | 45.0% | 60.0% | 30.0% | 45.0% | 60.0% | 30.0% | 45.0% | 60.0% |
| Bulk share | 20.0% | 20.0% | 20.0% | 20.0% | 20.0% | 20.0% | 20.0% | 20.0% | 20.0% |
| Trade share | 35.0% | 25.0% | 15.0% | 35.0% | 25.0% | 15.0% | 35.0% | 25.0% | 15.0% |
| Marketplace share | 15.0% | 10.0% | 5.0% | 15.0% | 10.0% | 5.0% | 15.0% | 10.0% | 5.0% |
| Channel share check | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| DTC realized price incl. modeled GST | 429.00 | 479.00 | 499.00 | 429.00 | 479.00 | 499.00 | 429.00 | 479.00 | 499.00 |
| Bulk publisher realization | 384.30 | 411.75 | 439.20 | 384.30 | 411.75 | 439.20 | 384.30 | 411.75 | 439.20 |
| Trade publisher realization | 301.95 | 329.40 | 356.85 | 301.95 | 329.40 | 356.85 | 301.95 | 329.40 | 356.85 |
| Marketplace gross selling price | 449.00 | 499.00 | 519.00 | 449.00 | 499.00 | 519.00 | 449.00 | 499.00 | 519.00 |
| Weighted publisher realization, gross | 378.59 | 430.15 | 466.72 | 378.59 | 430.15 | 466.72 | 378.59 | 430.15 | 466.72 |
| Publisher revenue excluding GST | 320.84 | 364.53 | 395.52 | 320.84 | 364.53 | 395.52 | 320.84 | 364.53 | 395.52 |
| Print cost of retained copy | 190.00 | 160.00 | 135.00 | 125.00 | 105.00 | 88.00 | 95.00 | 78.00 | 65.00 |
| Unsold edition write-off / retained copy | 63.46 | 17.92 | 4.32 | 41.67 | 11.68 | 2.73 | 31.67 | 8.67 | 2.01 |
| Total print burden / retained copy | 253.46 | 177.92 | 139.32 | 166.68 | 116.68 | 90.73 | 126.67 | 86.67 | 67.01 |
| Full entitlement streaming reserve | 21.24 | 29.74 | 33.98 | 21.24 | 29.74 | 33.98 | 21.24 | 29.74 | 33.98 |
| Support / servicing | 12.00 | 8.00 | 6.00 | 12.00 | 8.00 | 6.00 | 12.00 | 8.00 | 6.00 |
| DTC gateway cost / book | 10.12 | 11.30 | 11.78 | 10.12 | 11.30 | 11.78 | 10.12 | 11.30 | 11.78 |
| DTC shipping, packing, gateway, returns | 110.62 | 72.64 | 52.89 | 110.62 | 72.64 | 52.89 | 110.62 | 72.64 | 52.89 |
| Bulk freight, field, claims | 28.00 | 19.00 | 14.00 | 28.00 | 19.00 | 14.00 | 28.00 | 19.00 | 14.00 |
| Trade freight, field, bad debt | 30.00 | 20.00 | 13.00 | 30.00 | 20.00 | 13.00 | 30.00 | 20.00 | 13.00 |
| Marketplace fees, packing, returns | 144.00 | 120.00 | 102.00 | 144.00 | 120.00 | 102.00 | 144.00 | 120.00 | 102.00 |
| Weighted fulfillment / channel servicing | 70.89 | 53.49 | 41.58 | 70.89 | 53.49 | 41.58 | 70.89 | 53.49 | 41.58 |
| DTC CAC / retained book | 183.33 | 80.00 | 38.89 | 183.33 | 80.00 | 38.89 | 183.33 | 80.00 | 38.89 |
| Weighted DTC acquisition | 55.00 | 36.00 | 23.33 | 55.00 | 36.00 | 23.33 | 55.00 | 36.00 | 23.33 |
| Weighted marketplace advertising | 6.75 | 2.50 | 0.75 | 6.75 | 2.50 | 0.75 | 6.75 | 2.50 | 0.75 |
| Total incremental acquisition | 61.75 | 38.50 | 24.08 | 61.75 | 38.50 | 24.08 | 61.75 | 38.50 | 24.08 |
| Total non-print variable cost | 165.88 | 129.72 | 105.65 | 165.88 | 129.72 | 105.65 | 165.88 | 129.72 | 105.65 |
| Contribution before acquisition | -36.75 | 95.39 | 174.64 | 50.04 | 156.63 | 223.23 | 90.05 | 186.64 | 246.95 |
| Contribution after acquisition | -98.50 | 56.89 | 150.55 | -11.71 | 118.13 | 199.15 | 28.30 | 148.14 | 222.86 |
| Contribution margin | -30.7% | 15.6% | 38.1% | -3.7% | 32.4% | 50.3% | 8.8% | 40.6% | 56.3% |
| Static tier break-even copies | No unit break-even | 11,426 | 3,986 | No unit break-even | 10,158 | 5,022 | 176,701 | 27,001 | 15,705 |
| DTC contribution after CAC | -217.10 | 37.64 | 151.80 | -130.31 | 98.88 | 200.39 | -90.31 | 128.89 | 224.11 |
| Bulk contribution | 10.98 | 114.28 | 178.90 | 97.76 | 175.53 | 227.49 | 137.77 | 205.54 | 251.21 |
| Trade contribution | -60.81 | 43.50 | 110.11 | 25.97 | 104.74 | 158.70 | 65.98 | 134.75 | 182.42 |
| Marketplace contribution | -95.19 | 62.23 | 143.53 | -8.41 | 123.47 | 192.12 | 31.60 | 153.48 | 215.84 |

Note: "Static tier break-even copies" = fixed season spend / contribution after acquisition, rounded up; shown as "No unit break-even" where contribution after acquisition is not positive. "Contribution margin" = contribution after acquisition / publisher revenue excluding GST.

### 4.3 How the model computes the per-book lines (read off `workbook_csv/*Unit_Economics__formulas.csv`)

| Line | Computation in the workbook (symbolic) |
|---|---|
| Total copies printed | ROUNDUP(retained books / sell-through) |
| Bulk publisher realization | MRP x (1 - bulk discount) |
| Trade publisher realization | MRP x (1 - combined distributor/retailer discount) |
| Weighted publisher realization, gross | DTC share x DTC price + bulk share x bulk realization + trade share x trade realization + marketplace share x marketplace price |
| Publisher revenue excluding GST | weighted gross realization / (1 + 18%) |
| Unsold edition write-off / retained copy | (copies printed - retained books) x print cost / retained books |
| Full entitlement streaming reserve | activation rate x (USD 1 / 1,000 delivered minutes) x INR 90/USD x 400 delivered minutes x (1 + 18% non-recovered tax) |
| DTC gateway cost / book | DTC price x 2% x (1 + 18% GST on fee) |
| DTC shipping, packing, gateway, returns | (courier + packaging) / books per order + gateway cost + DTC reverse-logistics reserve |
| Bulk freight, field, claims | bulk freight + bulk field servicing + bulk leakage reserve |
| Trade freight, field, bad debt | trade freight + trade field cost + trade bad-debt/claims reserve |
| Marketplace fees, packing, returns | all-in marketplace cash fee + packaging + marketplace reverse-logistics reserve |
| DTC CAC / retained book | DTC CAC per customer / books per order |
| Contribution before acquisition | publisher revenue ex-GST - total print burden - streaming reserve - support - weighted fulfillment |
| Contribution after acquisition | contribution before acquisition - (weighted DTC acquisition + weighted marketplace advertising) |
| Channel contribution (DTC) | DTC price/(1+GST) - print burden - streaming - support - DTC fulfillment - DTC CAC per book |

Worked check at Base | 5,000: streaming reserve = 0.7 x 0.001 x 90 x 400 x 1.18 = INR 29.736; DTC gateway = 479 x 0.02 x 1.18 = INR 11.3044; DTC shipping/packing/gateway/returns = (65 + 12)/1.5 + 11.3044 + 10 = INR 72.64.

## 5. Channel contribution (Response verbatim, section 10.4)

#### 10.4 Channel contribution matters more than headline discounts

At the same base 5,000-copy cost tier:

| Channel | Contribution per retained book |
|---|---:|
| DTC, after modeled CAC | **₹98.88** |
| Institutional/bulk | **₹175.53** |
| Trade/bookstores | **₹104.74** |
| Marketplace, after modeled advertising | **₹123.47** |

These are model outputs, not channel guarantees. Institutional economics are attractive partly because consolidated delivery and lower acquisition friction can offset the discount.

**Do not stack a full retailer/distributor discount, a teacher commission, a referral payout, and paid-ad acquisition on the same order without recalculating contribution.**

### Workbook detail - contribution per retained book by channel, all nine cases (INR)

| Channel | Conservative \| 500 | Base \| 500 | Optimistic \| 500 | Conservative \| 5,000 | Base \| 5,000 | Optimistic \| 5,000 | Conservative \| 50,000 | Base \| 50,000 | Optimistic \| 50,000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DTC contribution after CAC | -217.10 | 37.64 | 151.80 | -130.31 | 98.88 | 200.39 | -90.31 | 128.89 | 224.11 |
| Bulk contribution | 10.98 | 114.28 | 178.90 | 97.76 | 175.53 | 227.49 | 137.77 | 205.54 | 251.21 |
| Trade contribution | -60.81 | 43.50 | 110.11 | 25.97 | 104.74 | 158.70 | 65.98 | 134.75 | 182.42 |
| Marketplace contribution | -95.19 | 62.23 | 143.53 | -8.41 | 123.47 | 192.12 | 31.60 | 153.48 | 215.84 |

Reading: in the **Conservative** case DTC loses money on every retained book at every scale (-217.10 at 500; -130.31 at 5,000; -90.31 at 50,000); trade (-60.81) and marketplace (-95.19) also lose money at 500, and marketplace (-8.41) still loses at 5,000. At the base 5,000 tier institutional/bulk is the most contributive channel (175.53) and DTC the least (98.88). Response caution: "Institutional economics are attractive partly because consolidated delivery and lower acquisition friction can offset the discount." (Organizer remark: DTC is the channel that Instagram/YouTube acquisition mostly feeds, so social reach alone does not reach the best-contribution channel.)

## 6. Break-even

### 6.1 Response verbatim (sections 11.2 and 11.3)

#### 11.2 Break-even

```text
Static break-even copies = Fixed costs / Contribution per retained copy
```

The base 5,000-copy cost structure gives approximately **10,158 copies** to cover ₹12 lakh of fixed costs.

The larger base structure, with ₹40 lakh of fixed costs and ₹148.14 contribution, gives approximately **27,001 copies**.

These are **static cost-tier calculations**. Requote printing, staffing and distribution when crossing a scale threshold; do not present either as a guaranteed real-world break-even point.

#### 11.3 CAC limits

At the base DTC economics, maintaining **₹100 contribution per book** permits approximately **₹118 CAC per customer/order** at a 1.5-book basket.

That is why I would initially require paid/referral CAC to settle around **₹100–₹120 or lower**, subject to actual costs.

The workbook also allocates fixed social/creative production to DTC. On that basis, the base 5,000-copy **fully loaded marketing CAC is approximately ₹187/customer**, not ₹120.

The fixed creative cost is already in operating profit; do not deduct that fuller KPI a second time.

### 6.2 Workbook detail - maximum DTC CAC for a INR 100/book contribution target (`Price_&_CAC`)

| Item | Value |
|---|---:|
| Target contribution / book | 100.00 |
| Base DTC basket | 1.50 |
| Base DTC contribution BEFORE acquisition / book | 178.88 |
| Maximum CAC / order | 118.32 |

Computation: Maximum CAC/order = MAX(0, (contribution before acquisition per book - target contribution per book) x basket) = (178.88 - 100) x 1.5 = **INR 118.32 per customer/order** (base 5,000-book cost tier, 1.5-book basket). Fully loaded base 5,000 marketing CAC is INR 186.67 per DTC customer (INR 120 incremental + INR 100,000 fixed creative spend allocated to DTC / 1,500 DTC customers = INR 66.67) - **do not deduct this fuller KPI again in profit; fixed creative cost is already in operating profit.**

### 6.3 Workbook detail - DTC contribution sensitivity to realized price and CAC (INR per retained book, 5,000-book base cost tier)

| Realized price \ CAC per customer | 50 | 100 | 150 | 200 | 250 |
|---:|---:|---:|---:|---:|---:|
| 349 | 38.45 | 5.11 | -28.22 | -61.55 | -94.89 |
| 399 | 79.64 | 46.31 | 12.97 | -20.36 | -53.69 |
| 449 | 120.83 | 87.50 | 54.17 | 20.83 | -12.50 |
| 479 | 145.55 | 112.22 | 78.88 | 45.55 | 12.22 |
| 499 | 162.03 | 128.69 | 95.36 | 62.03 | 28.69 |
| 549 | 203.22 | 169.89 | 136.55 | 103.22 | 69.89 |

Workbook caveats: "This table is DTC only. It does not include fixed-cost recovery. At lower price, recalibrate conversion and basket size rather than assuming demand rises automatically. Per-order CAC and per-book contribution are different units."

### 6.4 Static break-even by case (summary)

Break-even copies = fixed season spend / contribution after acquisition. Values (from Dashboard / JSON): Conservative 500: none (negative contribution); Base 500: 11,426; Optimistic 500: 3,986; Conservative 5,000: none; **Base 5,000: 10,158**; Optimistic 5,000: 5,022; Conservative 50,000: 176,701; **Base 50,000: 27,001**; Optimistic 50,000: 15,705. The response text quotes the two bold figures (about 10,158 copies to cover INR 12 lakh; about 27,001 copies for INR 40 lakh at INR 148.14 contribution). **"These are static cost-tier calculations. Requote printing, staffing and distribution when crossing a scale threshold; do not present either as a guaranteed real-world break-even point."**

## 7. Working capital and cash flow

### 7.1 Response verbatim (section 11.4)

#### 11.4 Working capital

The cash model uses phased print orders, 50% printer advances, delayed trade collections, tax reserves, and full digital-service usage reserves.

| Base project | Modeled funding requirement, including 15% headroom |
|---|---:|
| 500 retained sales | **₹7.15 lakh** |
| 5,000 retained sales | **₹12.71 lakh** |
| 50,000 retained sales | **₹52.09 lakh** |

Profitability does not eliminate cash needs. Printing and content are paid before many sales; trade payments can arrive after stock has moved.

Use preorder/bulk advances where appropriate, short initial trade-credit limits, SKU-level reprints, and strict receivable follow-up. Do not print 50,000 copies upfront to obtain a lower unit price.

### 7.2 Cash-flow conventions (workbook `Read_Me` + Execution Runbook section 6)

- Phased print orders: **three print receipts (months 2, 4, 5), 50% printer advance one month earlier**, balance on receipt; first lot 40%, second lot 35%, remainder in the third. Inventory is not all printed up front.
- **Trade cash arrives two months later** (60-day trade collection lag). Receivables tracked in a `Trade receivable` column.
- **Tax and full digital-service usage are treated as restricted reserves at the time of sale** (GST reserved; streaming reserve in "Other variable/reserved").
- Month 1 = start of content build; retained-sales and fixed-spend shares by month are in section 3.5. Not a verified demand forecast.
- The 15% funding buffer is **not** an additional P&L expense: funding = peak cumulative cash deficit x 1.15.
- Remaining stock is expensed at edition end (fully written off; no salvage). Revenue recognition for future digital obligations needs accountant review. Actual GST settlement dates, revenue deferral, interest, working-capital covenants and income taxes require a full accountant-led plan.
- Workbook QA statement: "Nine case P&Ls independently reconciled to monthly cash-flow totals; no negative stock; formula-error scan clear."

### 7.3 Workbook detail - monthly cash flow, Base case at each scale (INR, rounded to nearest rupee)

**Base | 500 retained books**

| Month | Retained sales | Print receipts | Closing stock | Gross invoiced | Trade invoiced | Cash receipts | GST reserved | Printer cash | Other variable/reserved | Fixed cash | Net usable cash | Cumulative cash | Trade receivable |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 17,760 | 0 | 227,500 | -245,260 | -245,260 | 0 |
| 2 | 0 | 222 | 222 | 0 | 0 | 0 | 0 | 17,760 | 0 | 162,500 | -180,260 | -425,520 | 0 |
| 3 | 50 | 0 | 172 | 21,508 | 4,118 | 17,390 | 3,281 | 15,600 | 6,486 | 65,000 | -72,977 | -498,497 | 4,118 |
| 4 | 150 | 195 | 217 | 64,522 | 12,352 | 52,170 | 9,842 | 26,720 | 19,458 | 32,500 | -36,351 | -534,848 | 16,470 |
| 5 | 175 | 139 | 181 | 75,276 | 14,411 | 64,982 | 11,483 | 11,120 | 22,702 | 32,500 | -12,822 | -547,670 | 26,764 |
| 6 | 75 | 0 | 106 | 32,261 | 6,176 | 38,438 | 4,921 | 0 | 9,729 | 32,500 | -8,713 | -556,383 | 20,588 |
| 7 | 25 | 0 | 81 | 10,754 | 2,059 | 23,106 | 1,640 | 0 | 3,243 | 26,000 | -7,777 | -564,160 | 8,235 |
| 8 | 13 | 0 | 68 | 5,592 | 1,071 | 10,698 | 853 | 0 | 1,686 | 26,000 | -17,842 | -582,002 | 3,129 |
| 9 | 12 | 0 | 56 | 5,162 | 988 | 6,232 | 787 | 0 | 1,557 | 13,000 | -9,112 | -591,113 | 2,059 |
| 10 | 0 | 0 | 56 | 0 | 0 | 1,071 | 0 | 0 | 0 | 13,000 | -11,929 | -603,043 | 988 |
| 11 | 0 | 0 | 56 | 0 | 0 | 988 | 0 | 0 | 0 | 13,000 | -12,012 | -615,055 | 0 |
| 12 | 0 | 0 | 56 | 0 | 0 | 0 | 0 | 0 | 0 | 6,500 | -6,500 | -621,555 | 0 |

**Base | 5,000 retained books**

| Month | Retained sales | Print receipts | Closing stock | Gross invoiced | Trade invoiced | Cash receipts | GST reserved | Printer cash | Other variable/reserved | Fixed cash | Net usable cash | Cumulative cash | Trade receivable |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 116,655 | 0 | 420,000 | -536,655 | -536,655 | 0 |
| 2 | 0 | 2,222 | 2,222 | 0 | 0 | 0 | 0 | 116,655 | 0 | 300,000 | -416,655 | -953,310 | 0 |
| 3 | 500 | 0 | 1,722 | 215,075 | 41,175 | 173,900 | 32,808 | 102,112 | 64,861 | 120,000 | -145,882 | -1,099,192 | 41,175 |
| 4 | 1,500 | 1,945 | 2,167 | 645,225 | 123,525 | 521,700 | 98,424 | 175,035 | 194,584 | 60,000 | -6,344 | -1,105,536 | 164,700 |
| 5 | 1,750 | 1,389 | 1,806 | 752,762 | 144,112 | 649,825 | 114,828 | 72,922 | 227,015 | 60,000 | 175,059 | -930,477 | 267,638 |
| 6 | 750 | 0 | 1,056 | 322,612 | 61,762 | 384,375 | 49,212 | 0 | 97,292 | 60,000 | 177,871 | -752,606 | 205,875 |
| 7 | 250 | 0 | 806 | 107,538 | 20,588 | 231,062 | 16,404 | 0 | 32,431 | 48,000 | 134,228 | -618,378 | 82,350 |
| 8 | 125 | 0 | 681 | 53,769 | 10,294 | 105,238 | 8,202 | 0 | 16,215 | 48,000 | 32,820 | -585,558 | 30,881 |
| 9 | 125 | 0 | 556 | 53,769 | 10,294 | 64,062 | 8,202 | 0 | 16,215 | 24,000 | 15,645 | -569,913 | 20,588 |
| 10 | 0 | 0 | 556 | 0 | 0 | 10,294 | 0 | 0 | 0 | 24,000 | -13,706 | -583,619 | 10,294 |
| 11 | 0 | 0 | 556 | 0 | 0 | 10,294 | 0 | 0 | 0 | 24,000 | -13,706 | -597,325 | 0 |
| 12 | 0 | 0 | 556 | 0 | 0 | 0 | 0 | 0 | 0 | 12,000 | -12,000 | -609,325 | 0 |

**Base | 50,000 retained books**

| Month | Retained sales | Print receipts | Closing stock | Gross invoiced | Trade invoiced | Cash receipts | GST reserved | Printer cash | Other variable/reserved | Fixed cash | Net usable cash | Cumulative cash | Trade receivable |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 866,658 | 0 | 1,400,000 | -2,266,658 | -2,266,658 | 0 |
| 2 | 0 | 22,222 | 22,222 | 0 | 0 | 0 | 0 | 866,658 | 0 | 1,000,000 | -1,866,658 | -4,133,316 | 0 |
| 3 | 5,000 | 0 | 17,222 | 2,150,750 | 411,750 | 1,739,000 | 328,081 | 758,355 | 648,615 | 400,000 | -396,050 | -4,529,366 | 411,750 |
| 4 | 15,000 | 19,445 | 21,667 | 6,452,250 | 1,235,250 | 5,217,000 | 984,242 | 1,300,026 | 1,945,845 | 200,000 | 786,888 | -3,742,479 | 1,647,000 |
| 5 | 17,500 | 13,889 | 18,056 | 7,527,625 | 1,441,125 | 6,498,250 | 1,148,282 | 541,671 | 2,270,152 | 200,000 | 2,338,145 | -1,404,334 | 2,676,375 |
| 6 | 7,500 | 0 | 10,556 | 3,226,125 | 617,625 | 3,843,750 | 492,121 | 0 | 972,922 | 200,000 | 2,178,707 | 774,373 | 2,058,750 |
| 7 | 2,500 | 0 | 8,056 | 1,075,375 | 205,875 | 2,310,625 | 164,040 | 0 | 324,307 | 160,000 | 1,662,277 | 2,436,651 | 823,500 |
| 8 | 1,250 | 0 | 6,806 | 537,688 | 102,938 | 1,052,375 | 82,020 | 0 | 162,154 | 160,000 | 648,201 | 3,084,852 | 308,812 |
| 9 | 1,250 | 0 | 5,556 | 537,688 | 102,938 | 640,625 | 82,020 | 0 | 162,154 | 80,000 | 316,451 | 3,401,303 | 205,875 |
| 10 | 0 | 0 | 5,556 | 0 | 0 | 102,938 | 0 | 0 | 0 | 80,000 | 22,938 | 3,424,240 | 102,938 |
| 11 | 0 | 0 | 5,556 | 0 | 0 | 102,938 | 0 | 0 | 0 | 80,000 | 22,938 | 3,447,178 | 0 |
| 12 | 0 | 0 | 5,556 | 0 | 0 | 0 | 0 | 0 | 0 | 40,000 | -40,000 | 3,407,178 | 0 |

The other six cases (Conservative and Optimistic at each scale) are in `workbook_csv/ExamLeaf_Business_Model__Cash_Flow__values.csv`; formulas in `..__Cash_Flow__formulas.csv`.

### 7.4 Peak cash gap and funding, all nine cases (INR lakh)

| Case | Peak cumulative cash gap | Funding requirement incl. 15% headroom |
|---|---:|---:|
| Conservative \| 500 | 7.99 | 9.19 |
| Base \| 500 | 6.22 | 7.15 |
| Optimistic \| 500 | 5.25 | 6.03 |
| Conservative \| 5,000 | 17.96 | 20.65 |
| Base \| 5,000 | 11.06 | 12.71 |
| Optimistic \| 5,000 | 8.43 | 9.69 |
| Conservative \| 50,000 | 83.06 | 95.52 |
| Base \| 50,000 | 45.29 | 52.09 |
| Optimistic \| 50,000 | 34.40 | 39.56 |

## 8. Costs that must not disappear into "AI automation" (Response verbatim, section 11.5)

#### 11.5 Costs that must not disappear into “AI automation”

The pilot budget assumes a lean, reusable 2D production workflow—not a complete bespoke platform with every custom Skill discussed earlier.

A separate **₹10 lakh engineering project**, for example, would reduce the base 50,000-sale profit from approximately ₹34.07 lakh to ₹24.07 lakh before other effects. Budget such work explicitly.

The model also assumes commissioned content with agreed paid-up rights. Royalties, third-party licences, additional staff, borrowing costs, and any obligations not included in those contracts must be added.

Runbook section 6 adds: "A full bespoke video platform or 40-Skill engineering project is NOT quietly included in the lean launch: the MVP uses reusable standard 2D tools. Any separate R&D programme needs its own budget and reduces profit." Fixed budgets "assume commissioned content with agreed paid-up publishing/usage rights and defined contractor workloads. Royalties, licensing obligations or additional staff not covered by those agreements must be added." (See `../08_cost_models` for the video-engine, skills and narration cost models, which are *separate* from this book-and-launch model.)

## 9. Fixed project / season budgets (workbook `90-Day_Budget`; pilot column = Response section 14 budget)

| Category | 500-book pilot (INR) | 5,000-book season (INR) | 50,000-book season (INR) | Scope / assumption |
|---|---:|---:|---:|---|
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

Workbook note: "90-day release discipline: authorize INR 60,000 for discovery/prototypes first. Release the remaining pilot budget only after medium/subject demand, academic quality, tax treatment and a fulfillment proof are validated. Suggested available capital ceiling: INR 8 lakh; not a mandate to spend it all." Heading: "FIXED PROJECT / SEASON BUDGETS | INR; CASH STOCK & VARIABLE SALES COSTS ARE SEPARATE". Printing and other variable costs are additional; the labor allocation is for a defined project workload, not an unlimited full-time team. The week-by-week plan that spends this budget is in `INSTRUCTIONS_business_launch_runbook.md`.

## 10. Optional digital-only subject economics (workbook `Digital_Offer`; not added to book-scenario revenue)

| Metric | INR per paid subject customer (margin as %) |
|---|---:|
| Digital selling price incl. modeled GST | 299.00 |
| Revenue excluding GST | 253.39 |
| Gateway cash cost | 7.06 |
| Full-edition delivery reserve | 42.48 |
| Support and refund reserve | 12.00 |
| Incremental acquisition | 80.00 |
| Contribution before fixed creation costs | 111.85 |
| Contribution margin | 44.1% |

Response (section 1.2): "In the illustrative model, a ₹299 digital-only subject purchase contributes about **₹112 before fixed content costs**, after the specified usage, support, payment, and acquisition allowances. Compulsory physical purchase therefore does not automatically maximize profit." Workbook note: "Book upgrade: credit the actual digital payment against the same-subject book bundle within a disclosed period. Keep one entitlement; do not count the upgrade as a second full digital sale. Test incremental contribution and cannibalisation, not only conversion. No recurring subscription is assumed." Digital acquisition cost assumed INR 80/customer; support/refund reserve INR 12/customer; digital purchasers assumed 100% active.

## 11. Tax warning (Response verbatim) and the GST sensitivity

##### Tax warning

**Do not assume the entire book-plus-premium-video offer is exempt merely because it contains a printed book.**

The actual treatment depends on the supplies, contract and applicable classification. GST guidance distinguishes composite supplies from mixed supplies. The workbook therefore includes a cautious 18% case and a separate zero-output-tax sensitivity—not a recommendation to claim exemption. [cite-token: turn250458view2]

Obtain written advice before finalizing prices and invoices.

Runbook section 6: "The model reserves 18% output GST on the entire marketed offer as a prudent scenario, NOT a legal conclusion. It assumes no input-tax-credit recovery. Current exemption and bundle classification require a CA review before setting invoices and final margins. The nil-output-tax sensitivity is not a recommendation to claim exemption." Workbook Read_Me: "Supplier cash costs include non-recovered taxes; input-tax credit is not assumed."

Effect of the zero-output-tax sensitivity on operating profit (INR, `Season_P&L` last column vs. base 18% case): Base 5,000 moves from -609,325 to -281,245; Base 50,000 moves from 3,407,178 to 6,687,983; Optimistic 5,000 moves from -4,273 to 351,698. Full table in section 2.2. **Obtain written CA advice before finalizing prices and invoices.**

## 12. Funnel arithmetic (Response verbatim sections 8.3 and 8.4, plus workbook `Funnel`)

#### 8.3 Why viral reach can still produce few sales

An **illustration**, not a benchmark:

```text
1,000,000 reached accounts
  × 20% relevant
  × 2% visit
  × 50% qualify
  × 5% purchase
  = 100 buyers
```

At 1.5 books per order, that is **150 books**.

Repeated Reel plays are not unique accounts, visits are not students, and students are not necessarily purchasers.

The lesson is not that Reels are ineffective. It is that **national viral reach cannot substitute for relevant demand, a credible product, and distribution**.

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

**Workbook `Funnel` sheet ("DEDUPLICATED STAGES, NOT REEL VIEWS = CUSTOMERS"):**

| Stage | Value | Definition / caveat |
|---|---|---|
| Unique accounts reached | 1,000,000 | Illustration only; not guaranteed reach |
| Share matching geography/class/medium | 20% | Estimate; do not profile minors with third-party advertising pixels |
| Eligible accounts | 200,000 | Derived |
| Visit rate among eligible accounts | 2% | Test assumption |
| Attributed visits | 4,000 | Deduplicate where lawful/possible |
| Qualified free-lesson rate among visits | 50% | Meaningful lesson participation, not autoplay start |
| Qualified free learners | 2,000 | Derived |
| Paid-order rate among qualified learners | 5% | Test assumption; not an industry benchmark |
| New paid DTC customers | 100 | Derived |
| Retained books per order | 1.5 | Planning assumption |
| Retained DTC books | 150 | Derived |

Qualified learners needed for the DTC plan (1,500 DTC customers): at 3% conversion = 50,000; at 5% = 30,000; at 8% = 18,750. DTC incremental CAC (base season) = INR 120; fixed social/creative spend allocated to DTC = INR 100,000; fully loaded marketing CAC per DTC customer = INR 186.67. Note on sheet: "Do NOT deduct this fully loaded KPI again in profit: fixed creative spending is already expensed."

## 13. Inputs that are still unresolved (replace before any large print commitment)

From the Response "Final recommendation": "The biggest unresolved commercial inputs are actual per-SKU printer quotes, courier/account charges, language demand, partner sell-through, and observed customer acquisition costs. Those should be resolved before large inventory commitments - not hidden behind optimistic assumptions."

From the Research_Source_Ledger / workbook `Sources` "Limit" column (selected, all copied in `toolkit/Research_Source_Ledger.csv`):
- Printing: the one public printer rate checked (bulkprintouts.com) prices short-run print and binding separately and "is not an ExamLeaf quote; none of the modeled unit costs are represented as quoted." Get three written quotes for the same specification.
- Couriers: "Obtain serviceable-pincode, weight, fee and COD/RTO account quotes" (Shiprocket); India Post Gyan Post "eligibility and the actual packed weight must be confirmed for this product. It is not a blanket justification for assuming a ₹25 delivery cost everywhere."
- Marketplace: Amazon referral fee 2% for books above INR 250 up to INR 500 is a published category rate; "All-in model fee is an assumption, not the referral percentage" (model uses INR 80-105 all-in). Flipkart must be costed from the actual seller-account quotation.
- Payment gateway: Razorpay standard 2% + GST; promotions excluded; "Actual payment-method/negotiated rates may differ."
- Video: Cloudflare Stream USD 1 per 1,000 delivered minutes (storage USD 5 per 1,000 stored-minute capacity); model adds planning FX of INR 90/USD ("Budget buffer, NOT a current FX quote"), 18% non-recovered tax and 400 delivered minutes per activated book.
- Market size: "Exact 2026 participation figures were not reconciled to an official result census"; obtain official class/stream/medium/district counts.
- Competitor prices (Oswaal Class 10 Science sample papers around ₹449 and Class 12 Physics ₹499 [workbook ledger: 15 SQP, listed INR 499 when checked 13 Oct 2026]; one checked Arihant 2027 ISC five-book bundle listed at ₹962) are pricing/feature references for *different products/boards*, not like-for-like.

## 14. How to change the model (no code needed)

1. Open `toolkit/ExamLeaf_Business_Model.xlsx` in Excel or LibreOffice (the same sheets exist as CSV in `workbook_csv/`; `__values` = computed numbers, `__formulas` = cell formulas).
2. Read in the order the workbook itself prescribes: **Dashboard -> Global Inputs -> Scenario Inputs -> Unit Economics -> Cash Flow.**
3. Edit only the assumption cells ("Blue text on pale yellow = assumptions. Green = linked formulas. Black = same-sheet calculations."): `Global Inputs` (MRP, tax rate, gateway, FX, streaming, buffers), `Scenario Inputs` (prices, mixes, CAC, courier, reserves, sell-through), `Volume Inputs` (print cost per copy and fixed spend per case).
4. Replace each estimate with a real quote or observed cohort number as it arrives (printer quotes, courier account rates, pilot CAC, sell-through). Keep verified tariffs and estimates visibly separate, as the model does.
5. Re-read the Dashboard. A case is only attractive if contribution after acquisition is positive *and* the funding requirement is financeable *and* the static break-even is inside the volume you can realistically reach at that cost tier.
6. `toolkit/Model_Assumptions_and_Results.json` is a static snapshot of the same inputs and results (prepared 2026-10-13) - useful for re-implementing the model elsewhere; it does not update when the workbook changes.

## 15. Related sections

`INSTRUCTIONS_business_launch_runbook.md` (budget release gates, pricing/offer table, roadmap); `REEL_BACKLOG_36.md`; `README.md`; `../08_cost_models` (video-engine, skills and narration cost models - separate from this book-and-launch model); `../09_research_and_evidence` (verified-source ledgers); `../07_end_to_end_pipeline_instructions`; `../02_learning_psychology` (evidence behind retrieval practice claims).
