# 05 · Shorts and Reels procedure: recompose complete learning units, never crop

**Scope.** From one **approved** long-form lesson (after GF, stage S14 of [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md)) to 1–3 approved vertical (9:16) Instagram Reels / YouTube Shorts, scheduled with truthful titles, one CTA each, and measured by useful behaviour.

**Sources:** message 10 §10 ([`04_video_engine/FULL_v2_implementation_and_research.md`](../04_video_engine/FULL_v2_implementation_and_research.md)); `ShortSpec` in `04_video_engine/implementation_v2/src/examleaf/interfaces.py`; VE Skills `reel-repurpose`, `thumbnail-package`; message 06 §6–§8, §13, §15 ([`01_business_model/FULL_business_model_launch_financial_plan.md`](../01_business_model/FULL_business_model_launch_financial_plan.md)); [`01_business_model/REEL_BACKLOG_36.md`](../01_business_model/REEL_BACKLOG_36.md); Execution Runbook §5.

**Status.** `ShortSpec` validation and the "vertical is re-laid-out, not cropped" test are [TESTED]; the 36 Reel concepts are "**original creative drafts, not field-tested viral formats**" (all `Status = Draft`); every posting/length rule is a launch experiment, "not algorithm laws" (Meta: ranking uses multiple predictions and signals; no universal Reel length, frequency or viral formula is established). Nothing has been published.

**Addendum (15 Oct 2026; RD-16 SUPERSEDED, RD-43, RD-45, RD-46).** The lesson master is now itself vertical (1080×1920 @ 30 fps), so a Reel/Short is **1–3 recomposed complete units** taken from the approved vertical lesson scenes (re-seek sub-ranges and re-time on the Short's own timeline), never a crop and never "3–5 Reels cut" from a lesson. **HyperFrames is the default compositor** for the animation layer [Recommendation, `12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` §4.1]; the RD-07 benchmark still decides the production compositor. Each Reel passes the storyboard gate H-SB before any paid generation, the A1–A17 suite, GS with two identities bound to the Reel's hash, and the AI-voice disclosure gate (06 §6.4).

---

## 1. Principles

1. **Recompose, don't crop.** "Vertical content is re-authored/reflowed, never blindly cropped or generatively outpainted to invent scientific details." "**A crop that removes a graph axis or condition is a scientific defect, not a cosmetic issue.**" (`ShortSpec.layout_strategy` must be `reflow`; `crop` is rejected.)
2. **Select genuinely complete learning units.** "For each approved lesson, initially select **one to three genuinely complete Shorts**: **One misconception → one prediction → one explanatory payoff → one relevant CTA.** Do not require twenty outputs because a platform workflow advertises twenty." Produce fewer useful Shorts rather than cutting arbitrary segments (reel-repurpose fallback).
3. **Deliver the answer in the Short.** "The CTA offers useful next practice rather than withholding essential information." Never hold back the end of a worked answer to induce a purchase.
4. **One payoff, one next action.** "Do not ask viewers to like, follow, comment, save, tag three people, and buy — all in the same clip."
5. **Same science gates as the lesson.** Each Short is a new artefact with its own hash: it goes through QA again and needs its own academic and production approvals (gate **GS**).
6. **Platform enforces access.** `access_tier` and `destination_resource_id` describe where the Short points; entitlement lives in the platform. No activation secrets anywhere in the Short, its cover or its metadata.

---

## 2. Procedure

### SH1 · Select the units

- **Do:** from the approved lesson's beats, pick 1–3 self-contained units, each built around a single misconception, a prediction and a complete payoff. Good sources are the curiosity beat, the misconception beat and the exam-conversion beat. Prefer concepts in the backlog (§5). A useful misconception correction from a **paid** chapter can stand alone and lead to a relevant preview, worksheet or product demonstration ("Do not restrict all Reels to the free chapters").
- **Owner:** VE **reel-repurpose** (proposes); social/growth lead + academic owner choose.
- **Input:** approved lesson (export record, approved script, claims, scene specs, timeline).
- **Output:** a candidate list with claim IDs and the conditions each unit must keep.

### SH2 · Write the ShortSpec

`ShortSpec` fields (all required unless noted) — [`12_GLOSSARY_and_DATA_CONTRACTS.md`](12_GLOSSARY_and_DATA_CONTRACTS.md) §3.11:

| Field | Rule |
|---|---|
| `id` | Short ID (use the Reel backlog **CSV ID** in the tracker when the Short implements a backlog concept) |
| `source_lesson_id` | The approved lesson |
| `source_claim_ids` | ≥ 1 approved claim IDs |
| `target_seconds` | **20–60** (schema-enforced) [RD-19] |
| `hook` | The question, contradiction or unfinished task shown in 0–3 s |
| `complete_payoff` | The full explanation delivered in the Short |
| `retained_conditions` | Every assumption/condition that must stay visible (e.g. "same voltage", "complete dominance", "real x") |
| `destination_resource_id` | The platform resource the CTA points to (free lesson, checkpoint, worksheet, product page) |
| `access_tier` | `free` / `book_entitlement` / `preview` |
| `layout_strategy` | `reflow` (default; `crop` rejected) |
| `approval_status` | `pending` until GS |
| `ai_voice_disclosure` (added 15 Oct 2026, RD-45) | Exact Path A or Path B line (06 §6.4); most Reels are Path B: "AI-generated narration; script by X; reviewed by Y." Empty = cannot publish |
| `performer_credit` (added 15 Oct 2026, RD-45) | Performer (Path A) or `none` (Path B); script author; reviewer |

**Build note (15 Oct 2026):** the engine's `ShortSpec` (`interfaces.py`) is a strict model that rejects unknown fields and does not yet have `ai_voice_disclosure` or `performer_credit`; add both to the model and its schema before the first Short is exported.

**Note (15 Oct 2026; RD-49, CE-L1, CE-68): `access_tier` and `destination_resource_id` are retired from the pipeline contract.** The pipeline is commercially agnostic. The two rows above, the "free / book_entitlement / preview" values, the product-page destination example, and Principle 6's wording that these fields "describe where the Short points" describe v1 only. In Content Engine v2 (`15_content_engine_v2/`) the Short (`format/short`) carries no access, entitlement, destination or CTA-routing field. The exporter writes the neutral metadata sidecar only (`15_content_engine_v2/subsystems/PACKAGING_and_DISTRIBUTION_REGISTRY.md` §6), a next step is the title of an approved artefact (`next_step_ref`), and the platform attaches entitlement and any destination outside the pipeline, joined by artefact id. `v1-import` drops both fields from v1 Shorts. The engine code and schema in `04_video_engine/implementation_v2/` (`interfaces.py`, `schemas/ShortSpec.schema.json`) are not edited here; removing the fields there is a P1 build item at maturity level 1 (`15_content_engine_v2/MATURITY_MODEL_and_ROADMAP.md`). Until then a v1 Short that already carries the two fields is grandfathered (Architecture §10.1) and must not be re-released or used as the source of a derived format with them attached.

- **Automated check:** `ShortSpec` validation (duration range, reflow, claims present).

### SH3 · Vertical recomposition (1080×1920 master; RD-16 SUPERSEDED 15 Oct 2026 → vertical-only)

- **Do:** re-lay out the scene for 9:16 from the **same verified state data** (same-state rule); keep axes, units, labels, conditions and the question visible; place labels beside objects; one dominant highlight; protected caption area; apply the phone-readability rule to the vertical master (`Displayed = Source × (360 / 1080)`; essential text must stay at least as readable as the landscape essential-label target) [RD-18]. "Use licensed audio and original visual assets. Do not distort a scientific diagram to follow a trend."
- **Owner:** the routed scene Skill (svg-scenes or the selected compositor via web-composition); VE **render-batch** renders.
- **Check [TESTED pattern]:** `test_vertical_not_crop`-type test for each new template; media probe.

### SH4 · Narration for the Short

- **Do:** reuse the **accepted** narration segments of the selected unit where they stand alone (their hashes are traceable). Any new or changed spoken wording (a hook line, a shortened payoff, the CTA line) is new script: it follows S5 rules, goes through the narration sub-pipeline (doc 04: lexicon, compile, synthesis, ASR, alignment, mastering) and the changed wording needs academic approval. Music optional and never necessary to make the explanation work; licensed audio only.
- **Timing:** the Short's own timeline (sample-based; protected pause for the prediction if one is used; answer revealed only after it).

### SH5 · Structure and timing (message 06 §6.2)

| Seconds | Purpose | Example (I-V graph) |
|---|---|---|
| **0–3** | Identify the problem (hook) | "Which line represents the larger resistance? Check the axes." |
| **3–8** | Invite a prediction or point out the tempting error | Viewer commits before the reveal |
| **8–30** | Deliver a complete explanation | Compare current at the same voltage; R = V/I is smaller for the steeper I-vs-V line |
| **Final seconds** | One relevant next action | "Try the three-question graph check." |

Most clips 20–45 s for one concept or mistake; more complex explanations up to the 60 s ShortSpec cap; anything needing more is not a Short — link the full lesson instead [RD-19].

### SH6 · Title, cover and caption package

- **Owner:** VE **thumbnail-package** (title options, editable SVG cover, description; "No false marks claims; no source diagrams made incorrect to increase clicks"; fallback: simple deterministic type/diagram cover). Any generated background goes through **selective-generation** with exact text placed deterministically afterwards.
- **Truthful titles and covers** (message 06 §6.3): "The title must accurately describe what the viewer receives. A 60-second checklist is not 'the complete chapter mastered in one minute.'"

| Content | Proposed title | Cover |
|---|---|---|
| Electricity | "HSLC Electricity: Read the Graph Before Using the Formula" | **CHECK THE AXES** |
| Algebra | "This Cancellation Can Remove a Valid Answer" | **WHERE DID IT GO?** |
| Chemistry | "Balance the Equation Without Changing the Substance" | **COEFFICIENT OR SUBSCRIPT?** |
| Biology | "Chromosome Count and DNA Amount: Keep Them Separate" | **TWO DIFFERENT COUNTS** |
| Product demonstration | "How One ExamLeaf Question Links to Its Explanation" | **QUESTION → REPAIR → RETRY** |

- **Caption formula:** **audience + useful promise + necessary condition + one CTA**. Cover text short, readable, topic-specific. Make class, board, topic and medium clear (the first funnel objection is "Is this relevant to my exam?").
- **Never:** guaranteed-marks claims, "only for intelligent students", invented statistics ("90% of students get this wrong"), fake urgency, generated testimonials, opaque virality scores.

### SH7 · QA and approval (gate GS)

- Re-run S13 checks on the Short: contrast, phone readability, axes/units/conditions present (a missing axis or condition is a **Critical** defect), answer not leaked before the payoff, caption fidelity, audio.
- **Animated Reels (15 Oct 2026, RD-43):** A1–A17 and the H-RV rubric (06 §3.1); H-SB must have approved the Reel's grid and estimate before any paid generation (RD-46). A Reel reusing approved lesson claims may shorten review but never removes a gate.
- **GS:** academic + production approvals bound to the **Short's** hash (runbook step 11: "Repeat QA and approval"); stage map row 19: reel-repurpose → stages 15–18 again.
- Output: `lessons/<…>/shorts/<short_id>/` (ShortSpec, vertical MP4, captions, approvals, export record).

### SH8 · Auditable content record and scheduling

One row per Reel in the tracker (Execution Runbook §5): **chapter ID, claim source, science approval, script, 9:16 scene, caption, target class/medium, CTA destination, experiment ID, release status.** "No automatic publication of unreviewed science, misleading claims, or generated testimonials." Publish only approved hashes, through the publisher identity, and only after the **disclosure gate** (added 15 Oct 2026, RD-45; 06 §6.4): description line, YouTube altered/synthetic toggle, Meta AI label, C2PA not stripped. Re-layout and publish suitable material to **YouTube Shorts** as well (YouTube's related-video link from a Short to a long video is subject to account access requirements).

---

## 3. Cadence and launch order

| Rule | Value | Status |
|---|---|---|
| Frequency | **Four or five reviewed Reels per week** | Launch experiment |
| Launch with | The **17 Class 10** concepts (all P0) and the trust formats | Business W4 onward, **only once their source lessons are GF-approved** [RD-38] |
| Trust items | #34 (answer quality; points to "a complete solved paper") and #36 (book-to-video repair; uses "the actual finished product", access duration shown, "no fabricated results") after specimen pages and print proofs exist (business W7–W9); #35 (confidence check) any time | Organizer inference recorded in `REEL_BACKLOG_36.md` |
| Class 12 | 16 concepts (P1) wait until the matching Class 12 title exists: "do not publish Class 12 purchase CTAs before that product exists" | Business rule |
| Paid boosting | "No paid reach boost merely because a Reel gets views." | Business W4 stop rule |

## 4. Metrics: what to track and what not to optimize

**Track** (with appropriate privacy controls; aggregated; no behavioural retargeting of children): **qualified visits** (not plays), **checkpoint attempts**, completion of useful practice, **book activation**, retained purchases; contribution by topic/format cohort and destination. Funnel stages: Reel discovery → free lesson (meaningful participation) → practice (attempts and answer quality) → registration (lawful, after value) → product page → checkout → delivery → activation (valid first-attempt success) → practice cycle → referral.

**Do not optimize** the production agent against an opaque virality score or Higgsfield-style "brain_activity / Virality Predictor" scoring (never calibrated against ExamLeaf learning or sales). "A title that increases clicks but attracts the wrong students or misrepresents the lesson is not a successful result." Repeated plays are not unique accounts; visits are not students; students are not purchasers (illustration: 1,000,000 reached × 20% relevant × 2% visit × 50% qualify × 5% purchase = 100 buyers ≈ 150 books).

**Experiments:** prediction-first vs worked-example opening on comparable topics and destinations; product proof vs generic motivational hook; predefine the primary outcome and denominators; measure retained sales and contribution, not only clicks; "do not announce a winner after two purchases or one unusually viral post."

## 5. The 36-Reel backlog (pointer)

[`01_business_model/REEL_BACKLOG_36.md`](../01_business_model/REEL_BACKLOG_36.md) (CSV: [`01_business_model/toolkit/ExamLeaf_36_Reel_Backlog.csv`](../01_business_model/toolkit/ExamLeaf_36_Reel_Backlog.csv)). Use the **CSV ID** as the stable ID (the response numbering differs).

| Group | Count | Priority | Examples (CSV ID: topic) | When |
|---|---:|---|---|---|
| A · Class 10 acquisition | 17 | P0 | 1 Ohm's law conditions; 2 I-V graph interpretation; 10 balancing equations; 18 lost algebraic solution; 28 inheritance probabilities | Launch first |
| B · Class 12 backlog | 16 | P1 | 7 drift velocity; 8 capacitor energy; 23 chain rule; 30 chromosome vs DNA count; 31 DNA replication direction | When the Class 12 product exists |
| C · Trust and conversion | 3 | P0 | 34 answer quality; 35 confidence check; 36 book-to-video repair | §3 above |

Counts from the CSV: target durations 30–55 s (mean 41.8 s) — all inside the 20–60 s ShortSpec range; funnel objectives mostly free lesson (15) and practice (13). Every concept must be matched to the current syllabus and reviewed (scientific + editorial) before publishing; each row's "Scientific/editorial check" column lists the specific trap.

## 6. Cost pointer

Optional **three-Short package ≈ $4.32 per source lesson** ($4.316 ≈ ₹388 at ₹90/USD) under the v2 cost model's token, voice, rendering and editorial allowances [PROPOSED estimate]. The business budget's "Reels, free-content packaging, community" line (₹50,000 in the pilot) covers the same subject matter: **count Shorts once** ([`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) §6).
