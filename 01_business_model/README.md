# 01_business_model - ExamLeaf business model, launch strategy and financial plan

**What this section is.** The complete business, marketing, funnel, pricing, activation-security and financial plan that ChatGPT produced for ExamLeaf (message 06), together with the user's prompt, the downloadable launch toolkit (editable Excel model, 36 Reel backlog, execution runbook, assumptions JSON, source ledger) and every sheet of that Excel model exported as CSV. Plus four organizer-written working documents that make the material usable (full cleaned text, a merged launch runbook, a readable 36-Reel backlog, and a financial summary).

**One-paragraph verdict (from the response).** ExamLeaf can become a viable publishing-led education business, but "viral videos + a QR code inside a book" is not enough. Launch two Class 10 titles (General Science, General Mathematics), with three *carefully selected* free chapters per subject, an optional INR 299 digital-only edition, INR 499 book + digital access and an INR 949 two-book bundle. Treat 500 retained sales as a validation exercise (base case loses about INR 6.22 lakh), 5,000 as meaningful demand that still loses about INR 6.09 lakh in the base case, and 50,000 as potentially profitable (base: about INR 34.07 lakh operating profit, needing about INR 52.09 lakh of funding capacity) - while the conservative case loses money even at 50,000. These are **planning scenarios, not sales forecasts or supplier quotations.**

## 1. Provenance - exactly where this came from

| What | Source path (under `00_source/`) |
|---|---|
| User's prompt | `chatgpt_transcript/messages/05_USER_prompt_business_model.md` |
| Assistant progress note | `chatgpt_transcript/messages/05a_ASSISTANT_progress_note.md` |
| Assistant response (about 50.8K characters) | `chatgpt_transcript/messages/06_ASSISTANT_business_model_launch_financial_plan.md` |
| Toolkit pack (5 files) | `extracted/ExamLeaf_Business_Launch_Toolkit/` (the same 5 files also exist as `downloads/ExamLeaf_Business_Launch_Toolkit.zip`; the workbook also as `downloads/ExamLeaf_Business_Plan/ExamLeaf_Business_Model.xlsx` - byte-identical, checked with `cmp`/`unzip -l`) |
| Workbook as CSV (15 sheets x values + formulas = 30 files) | `spreadsheets_as_csv/ExamLeaf_Business_Model__*.csv` |

Nothing under `00_source/` was modified; all copies were verified byte-identical with `cmp`/`diff`.

### Known gap - the user's original brief is missing

The prompt (message 05) attaches **"Pasted text(1).txt" (14,505 bytes, text/plain, `is_big_paste: true`)** - the user's original business-model brief. **It could not be retrieved from the ChatGPT share link and is not in this project.** What survives: (a) the prompt text itself in `prompt/` (5,476 characters; the attachment is referenced only as metadata - id `file_00000000ec8c820ba11e5201d4b98d83`, library id `libfile_c00fe37693048191a53c4a47628ea00d`); (b) the response's paraphrase of the brief: "Your brief proposes three free chapters, a physical book that unlocks the remaining videos, and an integrated practice-and-revision experience. It also explicitly invites alternatives to compulsory physical purchase." - tagged in the response with a file-citation token for lines L21-L32 of the attachment, preserved in the full text as `[cite-token: turn2file0, L21-L32]`. The organizing task note also quotes a surviving snippet beginning "Offer the first 3 chapters of every subject completely free..."; **that exact string does not occur in any file under `00_source/`** (searched for "completely free" and "Offer the first 3"), so it is recorded here as reported, not as verified text. Anything else the brief said is unknown. If you can export the original attachment, add it to `prompt/` and re-check section 1 of the plan against it.

## 2. Every file in this section

**Authored / cleaned documents (5):**

| File | One-line description |
|---|---|
| `README.md` | This file: provenance, inventory, how to use, verified-versus-proposed, cross-references, gaps. |
| `FULL_business_model_launch_financial_plan.md` | Cleaned, unshortened full text of ChatGPT message 06 (verdict, pricing, Assam market, book spec, psychology, Instagram strategy, 36 Reels, funnel, activation, unit economics, 9 scenarios, break-even, cash flow, distribution, automation stack, 90-day roadmap + budget, metrics, failure modes, expansion). Integrity-checked: all 76 headings, 242 table rows and every number preserved; only LaTeX markup and 21 citation tokens reformatted. |
| `INSTRUCTIONS_business_launch_runbook.md` | Step-by-step launch runbook merging response section 14 (week-by-week roadmap + budget) with `ExamLeaf_Execution_Runbook.md` and the workbook roadmap/budget: gates, offer/pricing table, access terms, activation flow, privacy, channel plan, 13 weekly work orders, budget, metric targets, failure-to-response table, expansion sequence. |
| `REEL_BACKLOG_36.md` | All 36 Reel concepts as readable tables: every CSV column merged with the response's numbering and wording, counts, production rules. |
| `FINANCIAL_SCENARIOS_SUMMARY.md` | The 9-scenario table, base unit economics at 5,000, channel contribution, break-even, working capital, CAC limits, tax warning, digital-only economics, funnel math, monthly cash flow - response numbers verbatim plus workbook detail, with all "scenarios, not forecasts" caveats. |

**`prompt/` (2 files, copied verbatim):**

| File | Description |
|---|---|
| `prompt/05_USER_prompt_business_model.md` | The user's request: 10 research areas (model validation, viral Instagram strategy, student psychology, content, funnel, physical book, pricing/financials for 500 / 5,000 / 50,000 books, marketing and distribution, automation, risks) and the required deliverables. |
| `prompt/05a_ASSISTANT_progress_note.md` | ChatGPT's 201-character interim note: 500 sales mainly validate demand; even 5,000 may not break even; CAC, fulfilment, discounts, sell-through and tax treatment are decisive. |

**`toolkit/` (5 files, `cp -R` of the extracted pack, byte-identical):**

| File | Description |
|---|---|
| `toolkit/ExamLeaf_Business_Model.xlsx` | Editable Excel model and launch workbook: 15 sheets (see the workbook_csv list below), nine financial scenarios, cash flow, sensitivity, budget, roadmap, Reel backlog, source ledger. |
| `toolkit/ExamLeaf_36_Reel_Backlog.csv` | 36 Reel concepts, 13 columns (ID, Audience, Strand, Topic, hook/cover, visual treatment, caption first line, single CTA, funnel objective, target duration, scientific/editorial check, launch priority, status). |
| `toolkit/ExamLeaf_Execution_Runbook.md` | The pack's own 9-section operating-decisions document (product scope, access offer, activation architecture, privacy, marketing controls, finance definitions, launch gates, metrics, expansion). |
| `toolkit/Model_Assumptions_and_Results.json` | Machine-readable snapshot of global inputs, the three scenarios' inputs and the nine results (prepared 2026-10-13). |
| `toolkit/Research_Source_Ledger.csv` | 30 sources/limitations (topic, type, URL, what it supports, limit) checked 13 October 2026. |

**`workbook_csv/` (30 files, copied byte-identical).** Each sheet exists twice: `ExamLeaf_Business_Model__<Sheet>__values.csv` (computed numbers) and `ExamLeaf_Business_Model__<Sheet>__formulas.csv` (cell formulas, so you can see how every number is computed). The 15 sheets:

| Sheet (both `__values.csv` and `__formulas.csv`) | Content |
|---|---|
| `Read_Me` | model conventions, definitions (retained sales, tax caution, cost basis, inventory write-off), reading order, cash-flow convention, budget meaning, QA statement |
| `Dashboard` | nine-case summary: net revenue, contribution per book, fixed spend, profit, margin, peak cash gap, funding +15%, static break-even; profit chart data |
| `Global_Inputs` | global tariffs and assumptions (MRP, 18% GST, 2% gateway, INR 90/USD, Cloudflare USD 1 per 1,000 min, 400 delivered minutes, 15% headroom, digital price INR 299, printer advance, print-lot shares, prototype 256 pp / 7x10 in / 70 GSM) and the 12-month cash timing profile |
| `Scenario_Inputs` | the 25 Conservative / Base / Optimistic assumptions (DTC price, mix, CAC, courier, discounts, reserves, activation, sell-through) |
| `Volume_Inputs` | retained books, landed print cost per copy and fixed season spend for each of the nine cases |
| `Unit_Economics` | per-retained-book economics for all nine cases: realization, print burden, streaming reserve, fulfilment, acquisition, contribution, static break-even, channel contribution |
| `Price_&_CAC` | DTC contribution sensitivity grid (price x CAC) at the base 5,000-book cost tier and the maximum-CAC calculator for a INR 100/book target |
| `Funnel` | deduplicated funnel illustration (1,000,000 reach to 100 buyers), the 5,000-book channel plan, qualified learners needed at 3/5/8% and the fully loaded marketing CAC |
| `Digital_Offer` | optional INR 299 digital-only subject unit economics (contribution about INR 111.85, 44.1%) |
| `Season_P&L` | nine-case season P&L in INR including output-GST reserve, print expense, other variable cost, fixed spend, operating profit and the zero-output-GST sensitivity |
| `Cash_Flow` | 12-month cash flow per case (print receipts and advances, trade collections with a 2-month lag, GST and usage reserves, fixed cash, cumulative cash, receivables) |
| `90-Day_Roadmap` | 13-week plan: days, owner, work, deliverable, gate / stop rule |
| `90-Day_Budget` | fixed project / season budgets by category for the 500-book pilot, 5,000-book season and 50,000-book season with scope notes |
| `Reel_Backlog` | the 36 Reel concepts with a sheet title row (same 13 columns as toolkit/ExamLeaf_36_Reel_Backlog.csv) |
| `Sources` | source ledger: 30 public sources / planning limitations checked 13 October 2026 (same rows as toolkit/Research_Source_Ledger.csv) |

## 3. How to use this material (step by step)

1. **Understand the decision (15 minutes).** Read the verdict above, then `FULL_business_model_launch_financial_plan.md` sections "Executive verdict" and 1-3, or the one-page summary in `INSTRUCTIONS_business_launch_runbook.md` section 1 (it also shows how the plan differs from your original proposal: curated rather than first-three free chapters, optional digital-only, separate activation secret).
2. **Check the money before you commit.** Open `FINANCIAL_SCENARIOS_SUMMARY.md`. Note that 500 and 5,000 retained sales lose money in the base case; the plan only turns profitable at scale with controlled CAC, about 90% sell-through and adequate working capital. Then open `toolkit/ExamLeaf_Business_Model.xlsx` (or the CSVs), read Dashboard -> Global Inputs -> Scenario Inputs -> Unit Economics -> Cash Flow, and replace every *assumption* with a real quote as it arrives (printer quotes, courier account rates, observed CAC, sell-through).
3. **Get professional sign-off on the three legal items** before pricing and invoices are final: GST treatment of the book + premium-video bundle (the model's 18% is a prudent scenario, not an opinion), DPDP / minors' verifiable-consent applicability, and CCPA education-advertising applicability.
4. **Run the launch.** Follow `INSTRUCTIONS_business_launch_runbook.md` section 2 (gates) and section 11 (13 weekly work orders with owner, deliverable, gate and stop rule). Spend only INR 60,000 on discovery/prototypes first; release the rest of the INR 6.5 lakh pilot budget (INR 8 lakh ceiling) only as gates pass.
5. **Build the activation and access system** from `INSTRUCTIONS_business_launch_runbook.md` section 6 (public QR for navigation; separate hashed random secret for entitlement; atomic redemption; signed short-lived video tokens; two devices / one concurrent stream). Hand this section to your developer.
6. **Produce and publish content** from `REEL_BACKLOG_36.md`: begin with the 17 Class 10 concepts (priority P0) plus the trust concepts; four or five reviewed Reels per week; every Reel one payoff and one CTA; keep an auditable content record. Production of the underlying lessons is covered in `../04_video_engine`, `../05_narration_system` and `../07_end_to_end_pipeline_instructions`.
7. **Measure** with the targets in `INSTRUCTIONS_business_launch_runbook.md` section 12 (e.g. qualified free learner to paid order 3-8%, incremental DTC CAC about INR 100-120 or below, valid first-attempt activation of at least 97%, sell-through planned at 90% and stressed at 75%) and run the listed experiments. These are management targets to test, not industry benchmarks.
8. **Decide at day 90.** Continue, revise price/offer, or stop; expand (Class 12 subject by subject, guides/question banks, then AI answer evaluation) only on evidence of positive contribution, dependable delivery and learning.
9. **Keep it current.** The response recommends a monthly syllabus, competitor-price and service-tariff alert; recheck the ledger prices (Oswaal, Arihant, PW, Razorpay, Amazon, Cloudflare, India Post) at launch.

## 4. Verified versus proposed / untested - exactly as the sources state

**Verified public facts** (response citations; the public sources and their stated limits are in `toolkit/Research_Source_Ledger.csv`, snapshot 13 October 2026): ASSEB's Division I / Division II naming (formerly SEBA / AHSEC); ASER 2024 Assam rural survey - 91.4% of 14-16-year-olds have a smartphone at home but only 14.6% of those able to use one own one (different denominators; rural only, not an all-Assam personal-phone rate); Oswaal catalogue examples (Class 10 Science sample papers around INR 449, Class 12 Physics INR 499 - CBSE products, not Assam equivalents); one checked Arihant 2027 ISC five-book bundle at INR 962; PW's dedicated ASSEB Class 10 offering; Meta's statements on ranking, creator Best Practices and teen-ad restrictions; YouTube Shorts related-video feature; WhatsApp business permission policy; provider tariffs - Razorpay 2% + GST (promos excluded), Amazon books referral 2% for prices above INR 250 to INR 500 (additional fees apply), Cloudflare Stream USD 1 per 1,000 delivered minutes and signed-token / origin controls (which do not prevent screen recording); India Post Gyan Post (eligibility must be confirmed); published GST composite / mixed supply guidance; DPDP Rules phased commencement; CCPA education-advertising guidance; research on retrieval practice and on perceived versus measured learning (university context).

**Proposed / assumptions - explicitly not verified:** every ExamLeaf price (INR 549 MRP, 499, 949, 299, 479 realized DTC); all printing costs (INR 160 / 105 / 78 base) - "none of the modeled unit costs are represented as quoted"; courier, packaging, marketplace all-in fees, CAC, conversion rates, basket size, sell-through, activation rate, staffing and project allocations; INR 90/USD; 400 delivered minutes per activated book; 18% output GST and non-recovered tax; the 12-month access policy; the 256-page pagination; the 36 Reel concepts ("original creative drafts, not field-tested viral formats"); the free-chapter count ("a testable starting point, not a proven optimum"); the Instagram posting/length rules ("launch experiments", not algorithm laws); all operating targets ("management targets to test, not industry benchmarks"). Not reconciled: exact 2026 Assam class/stream/medium participation counts; local shelf pricing and adoption (not audited).

**Untested:** nothing in this plan has been piloted - no demand, conversion, virality or learning-outcome result for ExamLeaf exists in these sources. Research supports retrieval practice but "does not prove a specific ExamLeaf exam-score gain."

## 5. Open gaps and ambiguities noticed while organizing

1. **Missing original brief** ("Pasted text(1).txt") - see section 1.
2. **Citation handles unresolved.** The 21 `[cite-token: turn...]` markers in the full text are ChatGPT-internal handles. They do not appear in `00_source/chatgpt_transcript/cited_source_links.md` (that file lists only the learning-science, tooling, voice and skill sources). The public URLs for this section's claims are in `toolkit/Research_Source_Ledger.csv`, but the ledger has no token-to-row mapping, so a specific token cannot be tied to a specific row with certainty.
3. **Two numbering schemes for the 36 Reels** (response section 7 order versus CSV strand order); `REEL_BACKLOG_36.md` carries both.
4. **Pagination labels** differ slightly between response section 4.1 and the runbook (diagnostic in the 16-page front block versus the 24-page practice block); totals are identical (256).
5. **Print lead time** is not stated anywhere: roadmap week 9 authorizes the first print batch and week 10 fulfils pilot orders. Resolve through the three written print quotes.
6. **No exam dates assumed.** The 90-day window ends about 11 January 2027; the actual 2027 Assam exam timetable was not verified.
7. **Dead download links.** The response's `sandbox:/mnt/data/...` links no longer work; the same files are in `toolkit/`.
8. **Consistency checks that passed:** the response's nine-scenario table matches the workbook Dashboard and the JSON in all rows; the response's pilot budget matches the `90-Day_Budget` pilot column line for line; the Reel CSV and the workbook `Reel_Backlog` sheet are identical apart from the sheet title row.

## 6. Cross-references to other sections

- `../02_learning_psychology` - learning-science evidence (retrieval practice, feedback, perceived versus measured learning) behind the Reel formats and positioning in this plan.
- `../03_super_teacher_framework` and `../05_narration_system` - the narration persona and voice system for the free and paid chapter videos this business sells.
- `../04_video_engine` - the video engine that would produce the chapter videos and vertical Reels; this plan budgets only a lean, reusable 2D workflow (INR 3,000 per reviewed chapter video, 40 videos, in the pilot budget).
- `../06_skills_library` - the custom Skills; the plan explicitly does **not** include a 40-Skill engineering project in its launch budget.
- `../07_end_to_end_pipeline_instructions` - the end-to-end production pipeline; the content workflow in `INSTRUCTIONS_business_launch_runbook.md` section 10 (approved chapter and question IDs to scheduled Reel) should be wired to it.
- `../08_cost_models` - video-engine, skills and narration cost models; these are separate from this book-and-launch model (a separate INR 10 lakh engineering project would cut base 50,000-sale profit from about INR 34.07 lakh to INR 24.07 lakh).
- `../09_research_and_evidence` - source ledgers and verified-evidence index (this section's ledger: `toolkit/Research_Source_Ledger.csv`).
- `../10_pilots_and_examples` - pilots and worked examples; relevant to the roadmap's "two approved prototypes" (week 2) and six free lessons (week 6).


## Open business decision (moved here from the pipeline on 15 Oct 2026)

- **Free-chapter policy and digital-only SKU (formerly RD-44).** "First 3 chapters free" (founder brief) versus "three carefully selected chapters" (this plan, §1.2) and whether the optional ₹299 digital-only edition is in the launch. This is a business/platform decision; the production pipeline is commercially agnostic (RD-49) and is unaffected either way.
