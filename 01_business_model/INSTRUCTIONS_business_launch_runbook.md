# INSTRUCTIONS_business_launch_runbook - how to launch ExamLeaf's book-linked business, step by step

> **Status of everything in this file: PROPOSED and UNTESTED.** It is a *proposed operating specification*, "not legal advice, actual customer research, a printer quote, or a guarantee of business results" (Execution Runbook header). Prepared 13 October 2026. Prices, costs, conversion rates, staffing allocations and targets are **assumptions to test**, not observed ExamLeaf performance. The only things the sources call *verified* are public provider tariffs and published facts, flagged where they appear.

## 0. How to use this document

This file merges three sources so you only need one operating checklist. Every operating rule in the Execution Runbook (sections 1-9) and in the response's sections 14-15 is carried here; see section 17 for the traceability map:

| Tag | Source | Where it lives |
|---|---|---|
| **[R sN]** | ChatGPT response, section N (esp. section 14 "Ninety-day launch roadmap and budget", also sections 2, 4, 8, 9, 12, 13, 15) | `FULL_business_model_launch_financial_plan.md` |
| **[RB sN]** | `ExamLeaf_Execution_Runbook.md`, section N (launch operating decisions) | `toolkit/ExamLeaf_Execution_Runbook.md` |
| **[WB sheet]** | Business-model workbook sheets `90-Day_Roadmap`, `90-Day_Budget`, `Read_Me`, `Global_Inputs` etc. | `workbook_csv/` and `toolkit/ExamLeaf_Business_Model.xlsx` |

Suggested way to work: read sections 1-2 once; then run sections 11 (week-by-week) as your calendar; use sections 3-10 as the specification you consult when a week's work touches pricing, the book, activation, privacy or channels; check sections 12-14 monthly. Money questions go to `FINANCIAL_SCENARIOS_SUMMARY.md`; content calendar to `REEL_BACKLOG_36.md`.

## 1. What you are launching - the decision in one page

**Verdict [R Executive verdict]:** "ExamLeaf can become a viable publishing-led education business—but “viral videos + a QR code inside a book” is not a sufficient competitive advantage." The stronger business is *board-specific revision and practice, with reliable solutions and short videos that help students correct the exact mistakes they make.* Use free videos to demonstrate that system; sell the convenience, structure, academic reliability and practice experience - not merely access to information already available elsewhere.

**Recommended launch scope [R Executive verdict; RB s1]:** two initial Class 10 titles (General Science and General Mathematics), three carefully selected free chapters per subject, an optional digital-only purchase, and a two-book bundle. Do **not** begin by funding six books, a native app, a large custom video platform and a nationwide marketing operation simultaneously. Class 12 Physics, Chemistry, Mathematics and Biology are expansion SKUs. Select the print medium from local student/parent/teacher interviews and paid demand, "not an Instagram poll alone". Verify every title against the current ASSEB division, syllabus, medium and edition; do not imply board endorsement.

**How the recommendation differs from the original brief [R sections 1-3]:**

| Your proposal (from prompt `05_USER_prompt_business_model.md`) | Response recommendation |
|---|---|
| First 3 chapters of each subject free | Three *carefully selected* free chapters (foundation + commonly difficult + representative later), plus a complete sample paper with useful solutions. "Three is a testable starting point, not a proven optimum." Not a permanent rule; not necessarily sequential. |
| Physical book unlocks remaining videos via QR/activation code | Book + optional digital-only purchase (INR 299). "Compulsory physical purchase therefore does not automatically maximize profit." A *public* QR is navigation only; paid access needs a *separate protected activation secret*. |
| "Premium, results-oriented brand for serious students" | "Premium" describes the service, not the student's status: "Clear concepts. Deliberate practice. Exam-ready answers." No score guarantees, no "only for intelligent students". |
| Class 10 and Class 12 science | Class 10 General Science + General Mathematics first (not separate Physics/Chemistry/Biology books); Class 12 subjects individually, later. |
| Subscriptions, app, AI evaluation as growth | No monthly subscription initially; postpone native app; AI answer evaluation = separately validated later product. |
| Viral reach as the engine | National viral reach "cannot substitute for relevant demand, a credible product, and distribution"; add teacher, school, search and retail distribution from the start. |

**Financial reality check [R Executive verdict] (details in `FINANCIAL_SCENARIOS_SUMMARY.md`):** 500 retained sales validate demand but do not recover the investment; 5,000 still loses money in the base case (about INR 6.09 lakh loss); 50,000 is potentially profitable (base: about INR 34.07 lakh operating profit, needing about INR 52.09 lakh of funding capacity) but the conservative case loses money even at 50,000. "These are planning scenarios, not sales forecasts or supplier quotations."

## 2. Launch gates - do not spend ahead of these

Principle [RB s7; WB 90-Day_Budget]: **start with a capped discovery/prototype spend of INR 60,000. Do not commit the entire pilot budget from the beginning.** Release the remaining pilot budget only after medium/subject demand, academic quality, tax treatment and a fulfillment proof are validated. Pilot fixed budget INR 6.5 lakh; base project funding in the model is about INR 7.15 lakh including 15% headroom; **suggested available capital ceiling INR 8 lakh, released in stages - "not a mandate to spend it all"**. This is allocated project labour and support reserves, "not an unlimited full-time annual team."

| # | Gate (all must pass before the next spend tranche) | Evidence required | Roadmap week(s) |
|---|---|---|---|
| G1 | Real demand | Interviews with students, parents, teachers and shops; competing books collected; **paid** demand (preorders/partner commitments) - "no claim that an Instagram poll proves demand"; "do not confuse survey enthusiasm with demand" | 1-2, 9 |
| G2 | Academic quality and teacher approval | Syllabus map signed; two prototype chapters approved; blind review of representative papers and all prototype solutions; six free lessons reviewed; zero unresolved critical errors | 3, 6, 7 |
| G3 | Legal / tax / privacy clearance | Written CA advice on GST treatment of book + premium video (the 18% output-GST case is a prudent scenario, not a conclusion); written DPDP/minors applicability review; CCPA advertising applicability reviewed | 2 (start), 7 (approve) |
| G4 | Print proof and real quotes | Three like-for-like written print quotes (same specification: cover, binding, scratch-code insertion, tax, freight, spoilage tolerance, replacement terms, payment schedule); approved print proof; actual per-SKU price and latest viable dispatch date | 2, 7, 8, 9 |
| G5 | Rural and urban delivery test | Real courier-weight data, tracking, receipt/activation checklist for urban and rural pincodes | 9 |
| G6 | Payment + activation + refund tests pass | Payment webhook, duplicate-redemption, refund and two-device recovery tests; free viewing works without forced registration | 5, 8 |
| G7 | Reprint rule | Reprints require demand **by SKU**, positive contribution, available cash, acceptable defect/return rates, and enough time before the intended exam season. "A lower print price does not compensate for stock that never sells." Do not print ahead merely to obtain a cheaper unit quote. | 12 |
| G8 | Day-90 decision | Review academic outcomes and financial gate; continue, revise price/offer, or stop. Class 12 only after title-level approval; expansion requires positive contribution, dependable delivery and evidence of learning. "Expansion follows evidence—not sunk costs." | 13 |

Scale guardrails [RB s7]: a 500-copy pilot "may make a loss while creating reusable intellectual property. That is not permission to tolerate negative unit economics indefinitely. Separate validation expenditure from scalable order contribution." At 5,000 retained sales the base model still loses about INR 6.09 lakh on INR 18.23 lakh net publisher revenue; at 50,000 it produces about INR 34.07 lakh operating profit on INR 182.27 lakh net revenue, before financing and income tax, under its stated conditions; conservative 50,000-copy economics lose money. "These are scenarios, not forecasts."

## 3. Offer, pricing and access terms

### 3.1 Launch offers - proposed price tests, not existing ExamLeaf prices [R s2.1; RB s1]

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

Additional operating rules from the Runbook [RB s1]: the INR 499 single-book offer is "delivered for standard serviceable locations"; **show all delivery exceptions before payment**. "Proposed MRP is INR 549, not a claim that the product was previously sold at that price." The financial base uses **INR 479 realized DTC revenue per book** after bundle/coupon mix, not INR 499 on every copy. Avoid permanent fake "today only" promotions.

### 3.2 What to give away free [R s1.2; RB s1]

Sequential free chapters can work when they contain essential foundations. But they can also demonstrate only the easiest part of the subject, fail to address the student’s immediate difficulty, or attract learners who never encounter your strongest teaching.

**Recommended free selection per live subject:**

| Free component | Purpose |
|---|---|
| One foundational chapter | Demonstrate clarity and make later learning accessible. |
| One commonly difficult chapter | Show that ExamLeaf can resolve real confusion. |
| One representative later chapter | Demonstrate that quality extends beyond introductory material. |
| One complete sample paper with useful solutions | Prove the quality of the paid practice product. |
| Short previews of other chapters | Show coverage without interrupting an explanation halfway through its answer. |

Three is a **testable starting point**, not a proven optimum. Three chapters out of ten is a very different offer from three out of twenty.

Do not restrict all Reels to the free chapters. A useful misconception correction from a paid chapter can stand alone and lead to a relevant preview, worksheet, or product demonstration.

Runbook rules [RB s1]: offer three representative **COMPLETE** free chapter lessons per live subject - an essential foundation, a frequently difficult concept, and an example showing later-chapter depth - plus a complete sample paper and its useful solutions. "Do not hold back the end of a worked answer merely to induce a purchase. Do not revoke access to already-promised free lessons." Public lessons must not require a phone number to begin [RB s4]. Do not restrict all Reels to the free chapters [R s1.2].

### 3.3 Access terms to print on the book and product page [R s2.2; RB s2]

My recommended starting policy is:

**Twelve months of access from activation, for the subject and edition purchased, with a clearly printed latest-redemption date.**

Also disclose that:

- Future editions, new boards, and future AI services are not automatically included.
- There is no automatic renewal.
- Shared-family-phone use and legitimate device replacement are supported.
- The printed book remains useful without activating the digital package.

For digital customers upgrading to the corresponding book, credit the **actual earlier digital payment** against the package within a disclosed period. Keep one entitlement and record only the incremental purchase value.

Additional terms from the Runbook [RB s2]:
- One subject/edition entitlement for **12 months from activation**; print a *latest-redemption date* prominently on the book and product page. It covers the edition sold, not every future syllabus and service. **Digital-only access starts on purchase.** No automatic renewal. Clarify the distinction between an *access deadline* and an *activation deadline*.
- **All paid chapters must be ready**, or an honest, specific delivery schedule and appropriate remedy must be visible before payment. "Do not advertise a complete catalogue that substantially remains unmade."
- **Upgrade rule:** a digital purchaser may upgrade to the corresponding book within a disclosed period by receiving credit for the actual earlier digital payment. Maintain **one entitlement**. Record only the incremental cash/revenue on upgrade; do not book a second full digital purchase.
- Books can be bought by parents, gifted, or shared physically. A digital account is attached to the learner/guardian arrangement, **not permanently to a phone**. Permit **two registered devices and one concurrent playback**, with easy recovery and an appeal path. Test shared-family-phone use explicitly.

### 3.4 Alternative models compared [R s2.3]

| Model | Advantage | Main weakness | Verdict |
|---|---|---|---|
| Book-only unlock | Simple positioning; supports physical distribution | Delivery friction; loses digital-only buyers | Too restrictive as the sole route |
| Book + optional digital-only | Accommodates different needs; reveals willingness to pay | Requires careful upgrade and channel policies | **Best initial structure** |
| Everything free, books optional | Broad reach and trust | Harder to recover content costs without strong distribution | Possible later, not the safest starting model |
| Low-priced monthly subscription | Low initial payment | Seasonal use, churn, cancellation friction, weak recurring value | Avoid initially |
| Annual all-subject subscription | Higher advance collection | Large catalogue and support obligations | Consider only after several strong subjects |
| AI evaluation subscription | Potential recurring utility | Accuracy, child-data, support, and inference costs | Separate later product |

## 4. Market facts and positioning to build on

### 4.1 Examination structure, devices, market size [R s3.1-3.3]

#### 3.1 Use the correct examination structure

ASSEB now has **Division I**, formerly SEBA, and **Division II**, formerly AHSEC. Product metadata, syllabus references, and edition labels should reflect the current board structure while retaining familiar search terms where useful. [cite-token: turn973282search1]

For Class 10, build examination-aligned **General Science and General Mathematics** products—not separate Physics, Chemistry, and Biology books simply because your video engine organizes content by scientific discipline. Verify the current syllabus and subject structure before production. [cite-token: turn358323search4, turn973282search7]

For Class 12, Physics, Chemistry, Mathematics, and Biology can become separate titles.

**Recommended launch sequence:** Class 10 Science and Mathematics first, unless paid reservations and teacher partnerships demonstrate a materially stronger Class 12 opportunity.

#### 3.2 Shared-device access matters

ASER 2024’s Assam rural survey found that **91.4% of surveyed 14–16-year-olds had a smartphone at home**. However, **among those able to use a smartphone, only 14.6% owned one themselves**. These are different denominators, and the survey is rural—not an all-Assam personal-device census. [cite-token: turn676578view2]

The practical implication is substantial:

**Do not design the service around the assumption that every student owns a private phone.**

Make free viewing easy, permit account recovery, accommodate parent purchasing, avoid unnecessary app installation, and ensure the physical book remains valuable offline.

#### 3.3 Do not underwrite the business using an inflated national market size

The relevant market is:

```text
Board cohort
  × subject eligibility
  × print medium
  × reachable geography
  × ability and willingness to pay
```

The total number of Class 12 students is **not** the market for four science-subject books.

I did not reconcile the exact 2026 Assam participation figures to an official class-and-stream census. Before a large print commitment, obtain current **district, stream, and medium-level counts** and build the serviceable market from actual school and retail coverage.

A practical initial market estimate is more useful than a national EdTech valuation: count the students your signed or actively engaged schools, coaching partners, bookstores, and DTC channels can realistically reach.

### 4.2 Competitors and the differentiation to claim [R s3.4]

| Competitor | Verified example or strength | What ExamLeaf should learn |
|---|---|---|
| **Oswaal** | Its current catalogue lists Class 10 Science sample papers around ₹449 and Class 12 Physics at ₹499; current products advertise digital/AI-related features | Digital additions and premium presentation are already competitive expectations |
| **Arihant** | Its iSucceed range combines sample papers and revision aids; one checked 2027 ISC five-book bundle was listed at ₹962 | Strong discounting and feature-rich bundles create price pressure; compare exact board/SKU, not only brand |
| **PW ASSEB** | Assam-specific Class 10 free and paid learning offerings | “Assam-specific videos” alone are not a defensible differentiation |
| **Local publishers, coaching notes, bookstores** | Exact local shelf pricing and adoption were not independently audited here | Obtain and review physical copies; local trust and distribution may matter more than online aesthetics |

The Oswaal and Arihant examples concern different products and, in some cases, different boards. They are **pricing and feature references**, not like-for-like proof that ExamLeaf should charge the same amount. [cite-token: turn140858view0, turn509123view0, turn660650view6, turn480908view6]

##### ExamLeaf’s strongest proposed differentiation

> **Assam-board practice with clear solutions, short misconception-specific explanations, and a visible route from a wrong answer to an independently correct one.**

The defensible assets would be the checked question-and-solution library, board-specific editorial process, teacher relationships, distribution, corrections system, and evidence of useful learning—not the QR technology.

## 5. Product specification - the physical book [R s4; RB s1]

**Step 1 - quote the prototype specification.** 
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

Runbook version of the same pagination hypothesis [RB s1]: "A 256-page prototype might allocate 16 front matter, 56 revision, 24 diagnostic/topic practice, 64 to eight papers, 80 solutions, and 16 trackers/checklists. This is a pagination hypothesis, not a promise that every Class 12 subject will fit. Quote longer mathematics and derivation-heavy books separately." (Labelling differs slightly: the response puts the diagnostic in the 16-page front section and calls the 24 pages "topic practice and common errors"; page totals are identical.) Workbook prototype inputs [WB Global_Inputs]: 256 pages, 7 x 10 inch trim, 70 GSM interior paper - "Check physical pagination before a fixed page commitment"; "Compare opacity and writing comfort on actual proofs."

**Step 2 - hold the product quality standards.**

The paid book should include **all essential solutions in print**. Digital explanations should add diagnosis, visualization, alternative approaches, and extra practice.

Use:

**Foundation → Board-standard → Stretch**

rather than implying that only “toppers” deserve the difficult material.

Clearly distinguish an **official marking scheme** from an **ExamLeaf-authored answer rubric**. Publish an errata page, edition number, syllabus version, and a method for reporting errors.

The useful QR destinations are specific:

> “Why this sign is negative.”

> “How to choose the law.”

> “How to interpret this diagram.”

Not simply a generic chapter homepage containing a long playlist.

Runbook adds [RB s1]: printed books must be useful *without internet* - quick revision, complete questions, substantive solutions, answer conditions, diagrams and error analysis. **Do not move essential printed solutions behind a paywall.** Use Foundation / Board-standard / Stretch rather than defining students as weak versus toppers.

**Step 3 - get printing quotes the right way.**

Obtain three written quotations for the **same specification**, including cover, binding, scratch-code insertion, tax, freight, spoilage tolerance, replacement terms, and payment schedule.

Public short-run printing rates can be considerably higher than an attractive bulk offset assumption; one checked printer separately prices printing and binding. That is why the model’s ₹105 or ₹78 costs must not be treated as obtained quotations. [cite-token: turn673898search10]

Quote **per title, language, and batch**. Fifty thousand aggregate sales split across numerous SKUs do not give every SKU the economics of a 50,000-copy run.

## 6. Activation, security and student-friendly access [R s9.1-9.2; RB s3]

### 6.1 Principle and flow

A public QR code should open the relevant chapter page.

A **separate protected activation secret** should grant paid access.

Recommended implementation:

```text
Purchase / issued physical code
            ↓
Learner or guardian account
            ↓
Consent and eligibility checks
            ↓
Atomic one-time redemption
            ↓
Subject + edition entitlement
            ↓
Short-lived authorized video token
```

Generate strong random codes, store hashes rather than exposed secrets, rate-limit attempts, and record SKU, edition, batch, issuing status and redemption history.

Test duplicate claims, delayed payment webhooks, gifts, refunds, scratched codes, wrong-account redemption, and device replacement.

### 6.2 Build specification (Runbook section 3, merged)

1. **Public QR codes provide navigation. They do NOT confer access.** Put a separate random secret under a scratch panel or inside protected packaging.
2. Generate a cryptographically strong random secret (for example **128 bits encoded in readable base32**); store its **hash**, serial, SKU, edition, print batch, issuing status, redemption deadline and audit history. Do not print sequential claimable tokens. Rate-limit redemption attempts and prevent code brute-force.
3. Code states: `generated -> printed -> issued -> redeemed`. Also support `suspended`, `revoked` and `expired`, with human-reviewed overrides. "An issued code is not proof of a retail sale; retailer sell-through must be measured separately."
4. Redemption transaction: `authenticated account -> consent/age-policy check -> hash lookup -> eligibility check -> atomic unique redemption -> subject entitlement -> user receipt`. Two simultaneous claims must not create two grants. Audit without exposing the token in analytics or application logs.
5. Direct sales: either auto-grant to the explicitly selected learner **OR** redeem the physical code; never accidentally grant two unrelated licences. A gift order should preserve an unclaimed recipient entitlement. The payment webhook must be **signature-verified, idempotent, and reconciled** with the captured payment state.
6. Video request: `entitlement check -> short-lived signed playback token -> private video player`.
7. Refunds and remedies: handle refunds with clear entitlements and channel rules. Damaged books, missing/scraped codes and legitimate account recovery need remedies. Record returned scratched-code copies as non-resellable unless properly reissued. Do not deny mandatory consumer rights through a blanket digital-code clause.
8. Test before launch [R s9.1]: duplicate claims, delayed payment webhooks, gifts, refunds, scratched codes, wrong-account redemption, device replacement.
9. Specific QR destinations only: e.g. "Why this sign is negative", "How to choose the law", "How to interpret this diagram" - not a generic chapter homepage with a long playlist [R s4.2].

### 6.3 Proportionate protection [R s9.2; RB s3]

Cloudflare Stream supports private playback through signed tokens and origin restrictions. These help control access; they do not prevent screen recording. [cite-token: turn874416view7]

A reasonable starting policy is **two registered devices and one concurrent stream**, with accessible support.

Avoid intrusive fingerprinting, visible student phone-number watermarks, and punitive lockouts on shared family devices.

Runbook adds: Cloudflare documents signed URLs and origin restrictions; "These reduce casual sharing but do not prevent screen recording. Avoid invasive device fingerprinting and student-identity watermarks. Protect the learning environment from accidental name/phone exposure." Targets: valid first-attempt activation of at least 97% (section 12).

## 7. Privacy, minors and communications [R s9.3; RB s4]

The DPDP Rules have phased commencement, including important rules commencing eighteen months after publication. They include provisions on verifiable parental consent and limited educational exceptions. Do not assume that every provision is already operative—or that ExamLeaf automatically qualifies for an exception. [cite-token: turn658056view4, turn658056view5]

Have counsel review the actual registration, progress-tracking, analytics, and advertising design.

**Do not build the funnel around behavioural retargeting of children.** Meta already restricts teen advertising targeting; design paid acquisition around appropriate adult purchaser/contextual routes rather than student profiling. [cite-token: turn660650view3]

A phone OTP alone does not establish that someone is an adult or necessarily satisfy parental-verification requirements.

Runbook specification [RB s4]:
1. Build for minors' privacy from the start. Use guardian-mediated registration and legally reviewed verifiable consent where required. "A phone OTP alone does not establish adult age or necessarily satisfy parental verification." Do not demand Aadhaar images or biometric records merely because they seem convenient.
2. "The DPDP Rules have phased commencement; not every rule is already operational on the research date. Limited educational exemptions are not a blanket licence for a commercial publisher. Obtain a written applicability review."
3. Do not deploy student behavioural ad pixels, lookalike audiences built from child accounts, or profiling for targeted ads to minors. Prefer aggregate campaign measurements and consent-limited essential progress records. Paid acquisition should focus on appropriate adult purchaser/contextual channels, "not hidden child retargeting."
4. Public lessons should not require a phone number to begin. Offer registration for saving progress or buying *after value is demonstrated*.
5. WhatsApp messages require proper permission, category expectations and opt-out. Keep order messages distinct from marketing consent. Avoid groups that expose pupils' phone numbers.

## 8. Messaging, trust and compliance rules [R s5]

#### 5.1 “Premium” should describe the service, not the student’s status

Recommended positioning:

> **Clear concepts. Deliberate practice. Exam-ready answers.**

Supporting message:

> “Built for students who want to practise seriously—even when a topic currently feels difficult.”

Avoid “only for intelligent students,” “weak students cannot understand this,” and “buy this to become a topper.”

#### 5.2 Trust must be demonstrated before it is requested

A strong trust-building experience is:

> Student attempts a question → ExamLeaf identifies the relevant mistake → the explanation resolves it → the student completes a related question without help.

A pleasant feeling of clarity is not sufficient evidence. Research has shown that perceived learning and measured learning can diverge, although the cited experiment was in university Physics rather than ExamLeaf’s market. [cite-token: turn658056search2]

**Proposed trust signals:** visible academic reviewers, a complete specimen paper, real page photographs, clear content coverage, an accessible corrections log, transparent access terms, and responsive support.

#### 5.3 Address three different decision-makers

| Decision-maker | Main question | Best evidence to show |
|---|---|---|
| Student | “Will this help me solve questions I currently get wrong?” | One strong explanation followed by a successful independent attempt |
| Parent | “What exactly are we paying for, and is it reliable?” | Full inclusions, sample pages, access period, delivery and support terms |
| Teacher/coaching partner | “Are the questions, solutions, and board alignment trustworthy?” | Specimen book, syllabus mapping, reviewer process, error-reporting channel |

#### 5.4 Use confidence-building feedback, not promises

Prefer:

> “Your method is correct; recheck the substitution.”

> “You identified the right relationship. Now include its condition.”

> “Try a fresh question before deciding that the chapter is secure.”

Avoid invented statistics such as “90% of students get this wrong” and unsupported claims such as “guaranteed 95%.”

CCPA’s education/coaching advertising guidance addresses misleading score guarantees, success claims, hidden information, false urgency, and the use of student success stories. Have the precise applicability to ExamLeaf reviewed before launch. [cite-token: turn250458view3]

## 9. Channel plan

### 9.1 Platform roles [R s8.1]

**Instagram:** discovery and short proof of teaching quality.

**YouTube:** searchable free chapter lessons and Shorts-to-long-video handoff. YouTube provides a related-video feature for Shorts, subject to the relevant account access requirements. [cite-token: turn673898search1]

**ExamLeaf website:** curriculum navigation, sample pages, checkout, activation, and paid lessons.

**WhatsApp:** permissioned order/support messages and optional revision reminders—not compulsory student groups. WhatsApp’s policy requires appropriate permission, expectations, and opt-out handling. [cite-token: turn874416view4]

**Native app:** postpone until the website’s usage and support data reveal a need that justifies it.

### 9.2 Student journey, friction removal and what to measure at each stage [R s8.2]

| Stage | Likely objection | Proposed implementation | Measure |
|---|---|---|---|
| Reel discovery | “Is this relevant to my exam?” | Class, board, topic and medium are clear | Qualified visits, not only plays |
| Free lesson | “Will this explain it properly?” | Begin immediately; no compulsory phone capture | Meaningful participation |
| Practice | “Did I actually understand?” | One independent question and feedback | Attempts and answer quality |
| Registration | “Why do you need my details?” | Offer saved progress or purchase utility after value | Lawfully completed registrations |
| Product page | “Why buy when videos are free?” | Show the full practice system, specimen and inclusions | Product-to-checkout rate |
| Checkout | “What is the final cost?” | Upfront delivery, access and refund information | Paid, retained orders |
| Delivery | “Where is the book?” | Tracking and realistic dispatch commitments | Delivery failures and contacts |
| Activation | “Will this code work on our phone?” | Simple redemption and recovery | Valid first-attempt success |
| Practice cycle | “What should I do next?” | Question → targeted explanation → retry | Independent practice |
| Referral | “Is it worth recommending?” | Ask after a useful experience | Retained referred purchases |

### 9.3 Instagram / YouTube Shorts operating rules [R s6.1-6.3; RB s5]

Full table of starting rules, Reel structure and truthful title/thumbnail examples are in `REEL_BACKLOG_36.md` section 4; the 36 concepts are in sections 2-3 there. Headlines: four or five reviewed Reels per week; most clips 20-45 seconds, complex ones 45-75; every Reel needs **one complete useful payoff and one next action**; these are "testing settings, not algorithm laws" [RB s5] - use the professional dashboard's own guidance and compare topic/format cohorts. Launch with the Class 10 and trust formats; do not publish Class 12 purchase CTAs before that product exists.

### 9.4 Why reach alone does not sell, and the 5,000-book base-channel plan [R s8.3-8.4]

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

| Channel | Retained books | Illustrative requirement |
|---|---:|---|
| DTC | 2,250 | 1,500 customers at 1.5 books/order |
| Institutional/bulk | 1,000 | 20 partners selling/distributing 50 copies each |
| Trade/bookstores | 1,250 | 25 outlets selling 50 copies each |
| Marketplace | 500 | Actual fulfilled, retained sales |
| **Total** | **5,000** | Not a commitment already secured |

At a 5% qualified-free-learner-to-order rate, the DTC portion requires **30,000 qualified learners**. At 3%, it requires 50,000; at 8%, 18,750.

This is why teacher, search, school, and retail distribution should complement social media from the beginning.

### 9.5 Distribution, referrals and partnerships [R s12]

#### Direct-to-consumer (DTC)

Lead with the two-book bundle and a strong specimen. Keep standard shipping terms simple and disclose remote-area exceptions before payment.

Begin with prepaid orders. Add COD only after measuring confirmation, return-to-origin, and support costs by location and channel.

India Post’s Gyan Post may offer economical eligible-book delivery, but eligibility and the actual packed weight must be confirmed for this product. It is not a blanket justification for assuming a ₹25 delivery cost everywhere. [cite-token: turn874416view2, turn686545search8]

#### Schools and coaching centres

Provide a specimen, syllabus map, sample lesson, and an actual question-solving demonstration.

Offer two clean arrangements: **institutional bulk pricing** or a **disclosed referral arrangement**. Do not combine them automatically.

For independent commercial partners, test a modest commission against actual contribution. Avoid covert sales payments to teachers steering students they assess; obtain necessary institutional approval and respect applicable employment restrictions.

#### Bookstores

Start with a small number of relevant outlets and capped opening stock. Agree on discounts, payment dates, returns, damaged-code handling, display copies, and edition expiry in writing.

Measure **sell-through**, not distributor dispatches.

#### Amazon and Flipkart

Use marketplaces for convenience and demand capture—not as the only acquisition engine.

Amazon’s fee schedule needs to be calculated using the actual price, category, fulfillment route, packed weight and returns. Flipkart should be similarly costed using the actual seller-account quotation. [cite-token: turn886284view2]

Do not assume the same all-in fee for single books and multi-book bundles.

#### Student referrals

A proposed pilot is a small buyer discount and a capped referrer credit after the refund window.

Accounting must remain clean:

**Buyer discount → lower realized selling price.**

**Referrer reward → marketing cost/liability.**

Do not count either twice. Avoid rewards tied to fabricated reviews or pressure to expose classmates’ contact details.

### 9.6 Marketing and partnership controls [RB s5]

1. Publish around four or five carefully reviewed Reels per week at launch; start with 20-45-second single-concept formats, longer where explanation needs them.
2. Every Reel needs one complete useful payoff and one next action. A related free lesson or independent challenge is usually better than asking for a purchase before any teaching. Re-layout scientific scenes for vertical viewing rather than simply cropping out labels.
3. Keep an **auditable content record**: chapter ID, claim source, science approval, script, 9:16 scene, caption, target class/medium, CTA destination, experiment ID, release status. **No automatic publication of unreviewed science, misleading claims, or generated testimonials.**
4. Pilot student referrals with a **capped reward**. Put the new buyer's discount in realized selling price; put the referrer's reward in marketing cost/liability. **Never count either twice.** Pay after the relevant refund window. Prevent self-referral abuse proportionately, without invasive tracking.
5. Independent coaching/retail partners may have disclosed contractual commissions. Avoid covert commissions to teachers for steering pupils they assess, and respect institution and public-employment restrictions. Fixed payment for genuine academic review is distinct from paid product endorsement. **Do not add a teacher affiliate fee on top of a full trade discount by accident.**
6. Offer schools/coaching centres two clean arrangements - institutional bulk pricing *or* a disclosed referral arrangement - never combined automatically [R s12].

## 10. Operating stack and automation [R s13]

#### Recommended initial stack

| Function | Initial implementation |
|---|---|
| Store, product pages, orders | WooCommerce on managed hosting |
| Payments | Razorpay |
| Accounts and entitlements | One account system plus a small, tested activation extension |
| Free lessons | YouTube, embedded where appropriate |
| Paid videos | Private hosted delivery with signed playback |
| Fulfillment | Courier/aggregator workflow, initially supervised; automate after validation |
| Social publishing | Native scheduling and approved publishing tools |
| Accounting | Suitable accounting software with accountant-reviewed tax treatment |
| Analytics | Aggregated funnel data and legally approved first-party records |
| Support | Help pages, ticket inbox, permissioned WhatsApp support |

WooCommerce provides an open-source commerce foundation, but hosting, extensions, development and maintenance are not costless. [cite-token: turn973282view0]

##### Automate repetitive work—not academic approval

A suitable content workflow is:

```text
Approved chapter and question IDs
        ↓
Long-form explanation
        ↓
Select one useful misconception/question
        ↓
Re-layout into vertical composition
        ↓
Generate caption and one matching CTA
        ↓
Scientific + editorial approval
        ↓
Schedule publication
        ↓
Aggregate performance by topic and destination
```

Keep humans responsible for scientific accuracy, syllabus fit, disputed answers, misleading claims, sensitive support cases, refund exceptions, and large stock commitments.

Do not crop a horizontal animation into a Reel if it removes axes, conditions, units, or necessary context.

Cost reminder [R s11.5; RB s6]: the pilot budget assumes a lean, reusable 2D production workflow - not a bespoke platform with every custom Skill. A separate INR 10 lakh engineering project would reduce the base 50,000-sale profit from about INR 34.07 lakh to INR 24.07 lakh; any such R&D needs its own budget. (See `../04_video_engine`, `../06_skills_library`, `../08_cost_models` for the video-engine, skills and narration systems that feed this stack.)

## 11. The 90-day roadmap and budget - week by week (response section 14 merged with workbook `90-Day_Roadmap`)

**Calendar frame [R s14]:** starting on the research date (13 October 2026), a 90-day window reaches approximately **11 January 2027**. "That makes a broad rushed catalogue particularly risky. The roadmap below does not assume an unverified 2027 exam timetable." Workbook title: "90-DAY LAUNCH | SEQUENCED GATES, NOT A MANDATE TO LAUNCH SIX TITLES". Week 1 = days 1-7, ... Week 13 = days 85-90. Verify the actual Assam exam dates before fixing print and dispatch dates.

**Source merge:** the response gives *Priority* and *Gate* per week; the workbook gives *Days, Owner, Work, Deliverable, Gate / stop rule*. Both gate columns are kept (they are complementary, not identical). "The complete workbook assigns owners and deliverables to each week." [R s14]

### 11.1 Calendar at a glance

| Week | Days | Owner (workbook) | Priority (response) |
|---|---|---|---|
| 1 | 1–7 | Founder + academic lead | Interview students, parents, teachers and shops; collect competing books |
| 2 | 8–14 | Academic lead + founder | Test two lessons, sample pages and price cards; obtain three print quotes |
| 3 | 15–21 | Academic editors | Lock two titles, syllabus map and content extent |
| 4 | 22–28 | Video + design team | Establish reusable visuals; begin four or five Reels/week |
| 5 | 29–35 | Editors + developers | Build checkout, accounts, redemption and refund flow |
| 6 | 36–42 | QA + partnerships | Complete six free chapters; test low-cost phones and partner specimens |
| 7 | 43–49 | Publisher + finance | Review print proofs and full solutions; finalize access/tax terms |
| 8 | 50–56 | Editorial + video lead | Complete the paid catalogue promised at launch |
| 9 | 57–63 | Founder + fulfillment | Authorize first short print batch; test urban/rural dispatch |
| 10 | 64–70 | Support + academic lead | Fulfill pilot purchases and repair activation friction |
| 11 | 71–77 | Growth + partnerships | Test referrals and digital-only versus bundle paths |
| 12 | 78–84 | Finance + operations | Reconcile sales, returns, stock and receivables |
| 13 | 85–90 | Founder + review board | Decide to continue, change the offer, or stop |

### 11.2 Weekly work orders

#### Week 1 (days 1–7) - owner: Founder + academic lead

- **Priority [R s14]:** Interview students, parents, teachers and shops; collect competing books
- **Work [WB 90-Day_Roadmap]:** Interview 15 students, 5 parents, 5 teachers and 4 shops. Collect actual competing books. Confirm medium and board/year.
- **Deliverable [WB]:** Interview notes; competitor shelf sheet; source/rights register.
- **Gate [R s14]:** Confirm real pain points and medium
- **Gate / stop rule [WB]:** No claim that an Instagram poll proves demand.

#### Week 2 (days 8–14) - owner: Academic lead + founder

- **Priority [R s14]:** Test two lessons, sample pages and price cards; obtain three print quotes
- **Work [WB 90-Day_Roadmap]:** Complete remaining interviews; test two free chapter prototypes, price cards and real book pages; obtain 3 like-for-like print quotes.
- **Deliverable [WB]:** Two approved prototypes; costed specification; tax/privacy review started.
- **Gate [R s14]:** Do not confuse survey enthusiasm with demand
- **Gate / stop rule [WB]:** Discovery/prototype spending cap INR 60,000 until gate passed.

#### Week 3 (days 15–21) - owner: Academic editors

- **Priority [R s14]:** Lock two titles, syllabus map and content extent
- **Work [WB 90-Day_Roadmap]:** Lock two Class 10 titles and one medium. Define 8-paper pagination and all printed solutions. Design first 3 free chapters by diagnostic value.
- **Deliverable [WB]:** Signed syllabus map and manuscript plan; no unreviewed 'official' claims.
- **Gate [R s14]:** Academic team can complete the promised product
- **Gate / stop rule [WB]:** Stop a title that cannot be accurately completed before promised delivery.

#### Week 4 (days 22–28) - owner: Video + design team

- **Priority [R s14]:** Establish reusable visuals; begin four or five Reels/week
- **Work [WB 90-Day_Roadmap]:** Build reusable diagrams and vertical Reel templates; publish 4–5 Class 10 Reels and free lesson 1 per title.
- **Deliverable [WB]:** Track qualified visits and question attempts, not only plays.
- **Gate [R s14]:** Measure qualified visits and attempts
- **Gate / stop rule [WB]:** No paid reach boost merely because a Reel gets views.

#### Week 5 (days 29–35) - owner: Editors + developers

- **Priority [R s14]:** Build checkout, accounts, redemption and refund flow
- **Work [WB 90-Day_Roadmap]:** Continue manuscripts/videos; implement checkout, entitlement database, refund/coupon rules and guardian flow.
- **Deliverable [WB]:** Test payment webhook and free viewing without forced registration.
- **Gate [R s14]:** Payment and entitlement tests pass
- **Gate / stop rule [WB]:** No third-party behavioural pixels on student learning pages.

#### Week 6 (days 36–42) - owner: QA + partnerships

- **Priority [R s14]:** Complete six free chapters; test low-cost phones and partner specimens
- **Work [WB 90-Day_Roadmap]:** Finish six free lessons; test on low-cost phones; prepare teacher specimen and short book walkthrough. Recruit permissioned partners.
- **Deliverable [WB]:** Academic review; low-data/mobile test; partner terms.
- **Gate [R s14]:** Usability and academic review pass
- **Gate / stop rule [WB]:** No covert teacher commission or compulsory pupil purchase.

#### Week 7 (days 43–49) - owner: Publisher + finance

- **Priority [R s14]:** Review print proofs and full solutions; finalize access/tax terms
- **Work [WB 90-Day_Roadmap]:** Blind-review representative papers and all prototype solutions; compare printer proofs; approve tax/invoicing/access terms.
- **Deliverable [WB]:** Print-ready proof and approved unit economics.
- **Gate [R s14]:** Credible delivery commitments
- **Gate / stop rule [WB]:** Accept transparent preorders only against a credible dispatch date.

#### Week 8 (days 50–56) - owner: Editorial + video lead

- **Priority [R s14]:** Complete the paid catalogue promised at launch
- **Work [WB 90-Day_Roadmap]:** Complete the paid catalogue promised for launch and the first two print masters; test scratch-code sequence and two-device recovery.
- **Deliverable [WB]:** Release candidate books/videos; duplicate-redemption and refund tests.
- **Gate [R s14]:** No undisclosed major missing chapters
- **Gate / stop rule [WB]:** Do not sell all-chapter access while undisclosed major chapters are missing.

#### Week 9 (days 57–63) - owner: Founder + fulfillment

- **Priority [R s14]:** Authorize first short print batch; test urban/rural dispatch
- **Work [WB 90-Day_Roadmap]:** Authorize only the first short batch against paid demand/partner commitments. Test dispatch to urban and rural pincodes.
- **Deliverable [WB]:** Real courier-weight data; delivery tracking; receipt/activation checklist.
- **Gate [R s14]:** Actual weight, price and delivery evidence
- **Gate / stop rule [WB]:** Check actual per-SKU print price and latest viable dispatch date.

#### Week 10 (days 64–70) - owner: Support + academic lead

- **Priority [R s14]:** Fulfill pilot purchases and repair activation friction
- **Work [WB 90-Day_Roadmap]:** Fulfill pilot buyers; repair activation friction; collect voluntary learning feedback; seed 10–20 outlets with capped stock.
- **Deliverable [WB]:** Delivered orders; first-week practice/activation reports.
- **Gate [R s14]:** No unresolved critical content/access issue
- **Gate / stop rule [WB]:** No further ad scale while refund or academic issues remain.

#### Week 11 (days 71–77) - owner: Growth + partnerships

- **Priority [R s14]:** Test referrals and digital-only versus bundle paths
- **Work [WB 90-Day_Roadmap]:** Promote best-converting Reel families; launch disclosed referral pilot; compare digital-only vs bundle paths.
- **Deliverable [WB]:** Contribution by cohort/channel; 3/7-day support and refund metrics.
- **Gate [R s14]:** Positive contribution by acquisition cohort
- **Gate / stop rule [WB]:** One reward/commission path per sale; no incentive stacking.

#### Week 12 (days 78–84) - owner: Finance + operations

- **Priority [R s14]:** Reconcile sales, returns, stock and receivables
- **Work [WB 90-Day_Roadmap]:** Reconcile all channels and printer stock; test second order/subject bundle; set reprint by demand and lead time.
- **Deliverable [WB]:** Actual CAC, sell-through, margin, cash and partner receivables.
- **Gate [R s14]:** Reprint justified by actual demand
- **Gate / stop rule [WB]:** Do not print ahead merely to obtain a cheaper unit quote.

#### Week 13 (days 85–90) - owner: Founder + review board

- **Priority [R s14]:** Decide to continue, change the offer, or stop
- **Work [WB 90-Day_Roadmap]:** Review academic outcomes and financial gate. Continue, revise price/offer or stop. Class 12 expansion only after title-level approval.
- **Deliverable [WB]:** Next-season plan; corrections log; source and customer-data audits.
- **Gate [R s14]:** Expansion follows evidence—not sunk costs
- **Gate / stop rule [WB]:** Expansion requires positive contribution, dependable delivery and evidence of learning.

Ambiguities to resolve yourself (not stated in the sources):
- **Print lead time.** Week 9 authorizes the first short batch and week 10 fulfils pilot purchases. The sources give no printer lead time; the week-9 gate ("Check actual per-SKU print price and latest viable dispatch date") and the three written quotes (which should state delivery/payment terms) are where this must be nailed down.
- **Exam dates.** The roadmap does not assume a 2027 exam timetable. Fix the real Assam board schedule first, then back-plan print and dispatch.
- **Interview counts** (15 students, 5 parents, 5 teachers, 4 shops) come only from the workbook; the response says only "interview students, parents, teachers and shops".

### 11.3 Budget for the two-title pilot - and how to release it

Response table [R s14] and workbook sheet `90-Day_Budget` agree line for line (pilot column; organizer checked all 10 lines and the total). The workbook also gives the 5,000-book and 50,000-book season budgets and a scope note per line.

| Fixed project allocation | 500-book pilot (INR) = response "Fixed pilot budget" | 5,000-book season (INR) | 50,000-book season (INR) | Scope / assumption [WB] |
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

Rules that come with the budget [R s14; WB; RB s7]:
- "Printing and other variable costs are additional, with sales receipts incorporated in the cash model." The labour allocation is for a defined project workload - not an unlimited full-time team.
- **Suggested available capital ceiling: INR 8 lakh, released in stages. Begin with only INR 60,000 for discovery and prototypes.** Release the remainder only when the gates in section 2 are met.
- Reviewed chapter videos: pilot basis is "40 x INR 3,000, including allocated human review and machine costs; reusable 2D templates." Fixed organic acquisition (Reels/community) is excluded from incremental CAC but included in profit. Video delivery is reserved separately per activated book (not in "Fixed hosting, tools, storage").
- Assumes commissioned content with agreed paid-up publishing/usage rights; royalties, licences or extra staff must be added. Funding headroom (15%) is liquidity, not P&L expense.
- Printing, courier, CAC, sell-through and conversion numbers in the cash model are estimates until replaced by quotes and observed cohort data.

## 12. Metrics, targets and experiments

### 12.1 Proposed operating targets - management targets to test, not industry benchmarks [R s15.1]

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

### 12.2 What to measure [RB s8]
- **Commercial:** retained sales, publisher realization, contribution by SKU/channel, paid/referral CAC, fully loaded marketing CAC, books per order, sell-through, ageing stock, receivable days, refund/COD loss, and unrestricted cash.
- **Learning:** attempted tasks, independent answer quality, delayed recall/transfer, correction behaviour and confidence calibration. **Video completion is not mastery.** Research supports retrieval practice, "but does not prove a specific ExamLeaf exam-score gain."
- **Operational:** valid first-attempt activation success, delivery performance, support contacts per hundred orders, academic defects, refund reasons, and time to correct an error.
- Definitions: retained book sales are net of refunds and returns; orders, customers, activation accounts and printed copies are different metrics. Incremental CAC includes paid/referral acquisition, not customer discounts or fixed creative work; organic creative work is separately expensed; the `Funnel` sheet shows the fuller marketing CAC (INR 186.67 in the base 5,000 case) so organic traffic is not treated as costless.

### 12.3 Experiments [R s15.2; RB s8]

Test **selected versus sequential free-chapter curation**, **one-book versus two-book presentation**, **digital-only availability**, and **product-proof versus generic motivational marketing**.

For Reels, compare a prediction-first opening with a worked-example opening using comparable topics and destinations.

Define the primary outcome before running each test. Measure retained sales and contribution, not only clicks. Do not announce a winner after two purchases or one unusually viral post.

A/B tests listed by the Runbook: selected versus sequential free-chapter curation; one-subject versus two-book offer; digital-only availability; worked-example versus prediction-first Reel; product proof versus vague motivational hook. "Predefine the outcome and denominators. Use adequate observations and report uncertainty rather than claiming a winner after two orders."

## 13. Failure modes and responses [R s15.3]

| Failure | Response |
|---|---|
| Viral views, few relevant visits | Narrow board/class/topic cues; change distribution, not merely editing speed |
| Free lessons used but no purchase | Review product value, price and practice needs; do not punish free learners |
| Paid acquisition exceeds contribution | Stop scaling; improve basket, channel mix, offer or costs |
| High print inventory | Shorter reprints, fewer SKUs, paid demand and capped trade stock |
| Weak teacher adoption | Audit scientific quality and local fit before offering a larger commission |
| Code sharing | Secure issuance and redemption, reasonable device controls, easy legitimate recovery |
| Students prefer free YouTube | Make the paid practice/solution system meaningfully better organized and dependable |
| Missing chapters or repeated errors | Pause promotion and repair the product |
| Seasonality | Maintain cash reserves; develop reusable guides/question banks only after core validation |
| Attractive accounting profit, cash shortage | Shorten collections, phase printing, reserve tax and future service obligations |

## 14. Expansion sequence [R s15.4; RB s9]

**First:** one cohort, one print medium, two excellent titles.

**Then:** dependable Assam distribution and Class 12 subjects introduced individually.

**Next:** guides and question banks that reuse the verified source and solution library.

**Later:** AI answer evaluation as a separately validated service with rubric-specific testing, protected child data, uncertainty handling, capped usage, and human escalation.

A new board requires new syllabus and assessment alignment. Translating the cover and reusing the same paper set is not a credible expansion strategy.

Runbook additions [RB s9]: Class 12 subject-by-subject and additional media "only where reviewer capability and demand justify them"; "Keep the general scientific animation library separate from board-specific assessment rules." A new board requires syllabus, paper-pattern, marking and language adaptation; translating the cover is not expansion. The AI answer-review pilot needs rubric-specific accuracy tests, clear uncertainty, protected child data, capped use and human escalation.

## 15. Finance definitions and safeguards to keep with you [RB s6]

(Numbers and scenario tables are in `FINANCIAL_SCENARIOS_SUMMARY.md`; this is the rule set.)
- Retained book sales are net of refunds and returns. Orders, customers, activation accounts and printed copies are different metrics. Trade revenue is the publisher's discounted realization, not the consumer MRP.
- The model reserves **18% output GST on the entire marketed offer as a prudent scenario, NOT a legal conclusion**; no input-tax-credit recovery. Current exemption and bundle classification require a CA review before setting invoices and final margins. "The nil-output-tax sensitivity is not a recommendation to claim exemption."
- Printing costs are estimates. Obtain quotes for the actual title count, page extent, colour coverage, trim, GSM, binding, cover, scratch panel, freight, taxes, defect tolerance and payment schedule. "Aggregate sales across many SKUs do not qualify every title for one large-print-run rate." Base print costs INR 160 / 105 / 78 at the three scales; base sell-through 90%; all unsold stock is charged to the edition with no salvage; full-edition video delivery reserves rather than only the first month of hosting.
- Fixed budgets assume commissioned content with agreed paid-up publishing/usage rights and defined contractor workloads. A full bespoke video platform or 40-Skill engineering project is **not** quietly included.
- Cash model: three print receipts, 50% advance one month earlier, two-month trade collection lag; tax and lifetime-of-entitlement usage are restricted cash reserves at sale; the 15% funding buffer is not a P&L expense. "Actual GST settlement dates, revenue deferral, interest, working-capital covenants and income taxes require a full accountant-led plan."

## 16. Final recommendation [R Final recommendation]

**Proceed with ExamLeaf—but launch it as a disciplined publishing and practice business, not as a bet on virality.**

The immediate investment should create **two trustworthy products, a frictionless free demonstration, reliable fulfillment and activation, and a measured route to repeatable contribution**.

The biggest unresolved commercial inputs are actual per-SKU printer quotes, courier/account charges, language demand, partner sell-through, and observed customer acquisition costs. Those should be resolved before large inventory commitments—not hidden behind optimistic assumptions.

**The best evidence that ExamLeaf deserves to grow will be students solving better, partners reordering, customers recommending it voluntarily, and each additional order contributing enough to sustain the next edition.**

A monthly syllabus, competitor-price, and service-tariff alert would help keep the operating model current.

## 17. Traceability and open items

**Where each part came from**

| Section here | Response | Runbook | Workbook |
|---|---|---|---|
| 1 Decision | Executive verdict; s1-3 | s1 | - |
| 2 Gates | s14 gates; s11.4 | s7 | 90-Day_Roadmap; 90-Day_Budget note |
| 3 Offer/pricing/access | s1.2, s2.1-2.3 | s1, s2 | Global_Inputs (prices) |
| 4 Market/positioning | s3.1-3.4 | s1 | Sources |
| 5 Book spec | s4.1-4.3 | s1 | Global_Inputs (pages, trim, GSM) |
| 6 Activation | s9.1-9.2, s4.2 | s3 | - |
| 7 Privacy | s9.3 | s4 | Funnel (no third-party pixels note) |
| 8 Messaging | s5.1-5.4 | s5 | - |
| 9 Channels | s8.1-8.4, s6, s12 | s5 | Funnel |
| 10 Stack | s13, s11.5 | s6 | - |
| 11 Roadmap/budget | s14 | s7 | 90-Day_Roadmap, 90-Day_Budget |
| 12-14 Metrics/failures/expansion | s15.1-15.4 | s8, s9 | - |
| 15 Finance rules | s10-11 | s6 | Read_Me |

**Open items / gaps (carried from the sources):**
1. The user's original brief ("Pasted text(1).txt", 14,505 bytes) could not be retrieved; only the snippet quoted in the response survives. See `README.md`.
2. All numbers are assumptions until replaced by printer quotes, courier/account charges, language-demand evidence, partner sell-through and observed CAC [R Final recommendation].
3. Official 2026 Assam class/stream/medium/district counts were not reconciled [R s3.3; Sources ledger "Market size"].
4. GST classification, DPDP/minors applicability and CCPA advertising applicability all require written professional review (gate G3).
5. Citation handles like `[cite-token: turn...]` in `FULL_business_model_launch_financial_plan.md` do not resolve to URLs in `00_source/chatgpt_transcript/cited_source_links.md`; use `toolkit/Research_Source_Ledger.csv` for the public sources.

6. Runbook closing note [RB Sources]: "The workbook Sources sheet lists the primary/provider links and validation limitations. The book/printing/CAC/conversion/staffing forecasts are planning estimates, not quotations or audited ExamLeaf performance."

**Related sections (by directory name):** `../02_learning_psychology` (retrieval-practice evidence, feedback language), `../03_super_teacher_framework`, `../04_video_engine`, `../05_narration_system`, `../06_skills_library`, `../07_end_to_end_pipeline_instructions`, `../08_cost_models`, `../09_research_and_evidence`, `../10_pilots_and_examples`.
