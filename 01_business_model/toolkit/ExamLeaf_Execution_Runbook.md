# ExamLeaf launch operating decisions
Prepared 13 October 2026. This companion is a proposed operating specification, not legal advice, actual customer research, a printer quote, or a guarantee of business results.

## 1. Product and scope
Launch two Class 10 products: General Science and General Mathematics. Select the print medium using local student/parent/teacher interviews and paid demand, not an Instagram poll alone. Class 12 Physics, Chemistry, Mathematics and Biology are expansion SKUs. Verify every title against the current ASSEB division, syllabus, medium and edition; do not imply board endorsement.

Recommended initial offers: one subject book plus the stated digital package at INR499 delivered for standard serviceable locations; two books at INR949; optional digital-only subject edition at INR299. Proposed MRP is INR549, not a claim that the product was previously sold at that price. Show all delivery exceptions before payment. The financial base uses INR479 realized DTC revenue per book after bundle/coupon mix, not INR499 on every copy.

Offer three representative COMPLETE free chapter lessons per live subject: an essential foundation, a frequently difficult concept and an example showing later-chapter depth. Also provide a complete sample paper and its useful solutions. Do not hold back the end of a worked answer merely to induce a purchase. Do not revoke access to already-promised free lessons. Three is a testable starting point, not a proven optimum.

Printed books must be useful without internet: quick revision, complete questions, substantive solutions, answer conditions, diagrams and error analysis. Do not move essential printed solutions behind a paywall. Use Foundation / Board-standard / Stretch rather than defining students as weak versus toppers.

A 256-page prototype might allocate 16 front matter, 56 revision, 24 diagnostic/topic practice, 64 to eight papers, 80 solutions, and 16 trackers/checklists. This is a pagination hypothesis, not a promise that every Class 12 subject will fit. Quote longer mathematics and derivation-heavy books separately.

## 2. Digital access offer
Proposed policy: one subject/edition entitlement for 12 months from activation; print a latest-redemption date prominently on the book and product page. It covers the edition sold, not every future syllabus and service. Digital-only starts on purchase. No automatic renewal. Clarify the distinction between an access deadline and an activation deadline.

All paid chapters must be ready, or an honest, specific delivery schedule and appropriate remedy must be visible before payment. Do not advertise a complete catalogue that substantially remains unmade.

A digital purchaser may upgrade to the corresponding book within a disclosed period by receiving credit for the actual earlier digital payment. Maintain one entitlement. Record only the incremental cash/revenue on upgrade; do not book a second full digital purchase.

Books can be bought by parents, gifted, or shared physically. A digital account is attached to the learner/guardian arrangement, not permanently to a phone. Permit two registered devices and one concurrent playback, with easy recovery and an appeal path. Test shared-family-phone use explicitly.

## 3. Activation architecture
Public QR codes provide navigation. They do NOT confer access. Put a separate random secret under a scratch panel or inside protected packaging.

Generate a cryptographically strong random secret (for example 128 bits encoded in readable base32); store its hash, serial, SKU, edition, print batch, issuing status, redemption deadline and audit history. Do not print sequential claimable tokens. Rate-limit redemption attempts and prevent code brute-force.

Suggested states: generated -> printed -> issued -> redeemed. Also support suspended, revoked and expired, with human-reviewed overrides. An issued code is not proof of a retail sale; retailer sell-through must be measured separately.

Redemption transaction: authenticated account -> consent/age-policy check -> hash lookup -> eligibility check -> atomic unique redemption -> subject entitlement -> user receipt. Two simultaneous claims must not create two grants. Audit without exposing the token in analytics or application logs.

For direct sales, either auto-grant to the explicitly selected learner OR redeem the physical code; never accidentally grant two unrelated licences. A gift order should preserve an unclaimed recipient entitlement. The payment webhook must be signature-verified, idempotent, and reconciled with the captured payment state.

Video request: entitlement check -> short-lived signed playback token -> private video player. Cloudflare documents signed URLs and origin restrictions. These reduce casual sharing but do not prevent screen recording. Avoid invasive device fingerprinting and student-identity watermarks. Protect the learning environment from accidental name/phone exposure.

Handle refunds with clear entitlements and channel rules. Damaged books, missing/scraped codes and legitimate account recovery need remedies. Record returned scratched-code copies as non-resellable unless properly reissued. Do not deny mandatory consumer rights through a blanket digital-code clause.

## 4. Privacy and communication
Build for minors' privacy from the start. Use guardian-mediated registration and legally reviewed verifiable consent where required. A phone OTP alone does not establish adult age or necessarily satisfy parental verification. Do not demand Aadhaar images or biometric records merely because they seem convenient.

The DPDP Rules have phased commencement; not every rule is already operational on the research date. Limited educational exemptions are not a blanket licence for a commercial publisher. Obtain a written applicability review.

Do not deploy student behavioural ad pixels, lookalike audiences built from child accounts, or profiling for targeted ads to minors. Aggregate campaign measurements and consent-limited essential progress records are preferable. Paid acquisition should focus on appropriate adult purchaser/contextual channels, not hidden child retargeting.

Public lessons should not require a phone number to begin. Offer registration for saving progress or buying after value is demonstrated. WhatsApp messages require proper permission, category expectations and opt-out. Keep order messages distinct from marketing consent. Avoid groups that expose pupils' phone numbers.

## 5. Marketing and partnership controls
Publish around four or five carefully reviewed Reels per week at launch. Start with 20–45-second single-concept formats, with longer clips where explanation needs them. These are testing settings, not algorithm laws. Use the professional dashboard's own guidance and compare topic/format cohorts.

Every Reel needs one complete useful payoff and one next action. A related free lesson or independent challenge is usually better than asking for a purchase before any teaching. Re-layout scientific scenes for vertical viewing rather than simply cropping out labels.

Use an auditable content record: chapter ID, claim source, science approval, script, 9:16 scene, caption, target class/medium, CTA destination, experiment ID, release status. No automatic publication of unreviewed science, misleading claims, or generated testimonials.

Pilot student referrals with a capped reward. Put the new buyer's discount in realized selling price; put the referrer's reward in marketing cost/liability. Never count either twice. Pay after the relevant refund window. Prevent self-referral abuse proportionately, without invasive tracking.

Independent coaching/retail partners may have disclosed contractual commissions. Avoid covert commissions to teachers for steering pupils they assess, and respect institution and public-employment restrictions. Fixed payment for genuine academic review is distinct from paid product endorsement. Do not add a teacher affiliate fee on top of a full trade discount by accident.

## 6. Finance definitions and safeguards
Retained book sales are net of refunds and returns. Orders, customers, activation accounts and printed copies are different metrics. Trade revenue is the publisher's discounted realization, not the consumer MRP.

The model reserves 18% output GST on the entire marketed offer as a prudent scenario, NOT a legal conclusion. It assumes no input-tax-credit recovery. Current exemption and bundle classification require a CA review before setting invoices and final margins. The nil-output-tax sensitivity is not a recommendation to claim exemption.

Printing costs are estimates. Obtain quotes for the actual title count, page extent, colour coverage, trim, GSM, binding, cover, scratch panel, freight, taxes, defect tolerance and payment schedule. Aggregate sales across many SKUs do not qualify every title for one large-print-run rate.

Base print costs are INR160, INR105 and INR78 at the three project scales; base sell-through is 90%. The model charges all unsold stock to the edition, without salvage. It includes full-edition video delivery reserves rather than only the first month of hosting.

Incremental CAC includes paid/referral acquisition, not customer discounts or fixed creative work. Organic creative work is separately expensed. The Funnel tab shows a fuller marketing CAC so organic traffic is not treated as costless.

Fixed budgets assume commissioned content with agreed paid-up publishing/usage rights and defined contractor workloads. Royalties, licensing obligations or additional staff not covered by those agreements must be added. A full bespoke video platform or 40-Skill engineering project is NOT quietly included in the lean launch: the MVP uses reusable standard 2D tools. Any separate R&D programme needs its own budget and reduces profit.

The cash model uses three print receipts, 50% advance one month earlier, and two-month trade collection lag. Tax and lifetime-of-entitlement usage are restricted cash reserves at sale. A 15% funding buffer is not an additional P&L expense. Actual GST settlement dates, revenue deferral, interest, working-capital covenants and income taxes require a full accountant-led plan.

## 7. Launch gates
Start with a capped discovery/prototype spend of INR60,000. Do not commit the entire pilot budget from the beginning. Obtain paid demand, teacher approval, a print proof, legal/tax clearance, and a rural/urban delivery test.

The pilot fixed budget is INR6.5 lakh. Base project funding in the model is approximately INR7.15 lakh including headroom; a maximum available pilot envelope of INR8 lakh is a sensible planning cap. This is allocated project labour and support reserves, not an unlimited full-time annual team.

A 500-copy pilot may make a loss while creating reusable intellectual property. That is not permission to tolerate negative unit economics indefinitely. Separate validation expenditure from scalable order contribution.

At 5,000 retained sales, the base model still loses about INR6.09 lakh on INR18.23 lakh net publisher revenue. At 50,000 it produces about INR34.07 lakh operating profit on INR182.27 lakh net revenue, before financing and income tax, under its stated conditions. Conservative 50,000-copy economics lose money. These are scenarios, not forecasts.

Reprints require demand by SKU, positive contribution, available cash, acceptable defect/return rates, and enough time before the intended exam season. A lower print price does not compensate for stock that never sells.

## 8. What to measure
Commercial: retained sales, publisher realization, contribution by SKU/channel, paid/referral CAC, fully loaded marketing CAC, books per order, sell-through, ageing stock, receivable days, refund/COD loss, and unrestricted cash.

Learning: attempted tasks, independent answer quality, delayed recall/transfer, correction behaviour and confidence calibration. Video completion is not mastery. Research supports retrieval practice, but does not prove a specific ExamLeaf exam-score gain.

Operational: valid first-attempt activation success, delivery performance, support contacts per hundred orders, academic defects, refund reasons, and time to correct an error.

A/B tests: selected versus sequential free-chapter curation; one-subject versus two-book offer; digital-only availability; worked-example versus prediction-first Reel; product proof versus vague motivational hook. Predefine the outcome and denominators. Use adequate observations and report uncertainty rather than claiming a winner after two orders.

## 9. Expansion sequence
First: one cohort, one print medium, two thoroughly checked titles.
Then: repeatable Assam distribution, Class 12 subject-by-subject, and additional media only where reviewer capability and demand justify them.
Next: question banks and guides sharing the source/solution library.
Later: a separately validated AI answer-review pilot with rubric-specific accuracy tests, clear uncertainty, protected child data, capped use and human escalation.

A new board requires syllabus, paper-pattern, marking and language adaptation; translating the cover is not expansion. Keep the general scientific animation library separate from board-specific assessment rules.

## Sources
The workbook Sources sheet lists the primary/provider links and validation limitations. The book/printing/CAC/conversion/staffing forecasts are planning estimates, not quotations or audited ExamLeaf performance.
