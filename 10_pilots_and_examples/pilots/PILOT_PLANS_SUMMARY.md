# PILOT_PLANS_SUMMARY - four 600-second pilot plans, beat by beat

Generated directly from the JSON files in this folder (`*_600s_plan.json` for the beats; `<id>.json` for the linked 30-second technical scene). Nothing below is invented: every cell is read from the JSON. Source: `ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/examples/` (ChatGPT message 10 deliverable).

**Status of every plan: `blueprint_only`.** Each plan is only a beat plan. Every beat has `script_status = requires_authoring_and_review`; `audio_status = not_generated`; `board_mapping_status = pending current syllabus and ExamLeaf source review`. Complete scripts, teacher-approved answers, narration and event alignment still need producing (`Four_Pilots.md`).

**Verified while writing this file:** the `beats` array is identical (same 11 beats, same starts/durations/purposes/tasks/script_status) in all four plans, and the durations sum to 600 s in each. What differs per pilot is only `id`, `subject`, `technical_scene`, `objective` and `prerequisites`. The beat table is repeated under each pilot below so each pilot can be used on its own.

## Index

| # | Pilot id | Subject | Technical scene | Plan file | Scene file |
|---|---|---|---|---|---|
| 1 | `physics_rc_full_pilot` | physics | `physics_rc` | `physics_rc_600s_plan.json` | `physics_rc.json` |
| 2 | `chemistry_balance_full_pilot` | chemistry | `chemistry_balance` | `chemistry_balance_600s_plan.json` | `chemistry_balance.json` |
| 3 | `mathematics_chain_full_pilot` | mathematics | `mathematics_chain` | `mathematics_chain_600s_plan.json` | `mathematics_chain.json` |
| 4 | `biology_genetics_full_pilot` | biology | `biology_genetics` | `biology_genetics_600s_plan.json` | `biology_genetics.json` |

---

## 1. Physics pilot - `physics_rc_full_pilot`

- **Plan file:** `physics_rc_600s_plan.json`
- **status:** `blueprint_only`  |  **duration_s:** 600  |  **technical_scene:** `physics_rc`
- **objective:** Connect ideal RC charging to its graph and one-time-constant value.
- **board_mapping_status:** pending current syllabus and ExamLeaf source review
- **audio_status:** `not_generated`
- **prerequisites:**
  - Ideal linear resistor and capacitor; constant 10 V source.
  - Capacitor initially uncharged.
  - Model time is explicitly shown as t/(RC); not a footage timestamp.
- **mandatory_reviews:** `academic`, `full_render`, `native_language_when_localized`
- **success_measures:** zero critical science errors; full timed voice listen; mobile visual review; independent item; delayed retrieval; measured human_minutes; measured generation_and_render_cost

### 1.1 The 11 beats (start / duration / end in seconds)

| # | Start (s) | Duration (s) | End (s) | mm:ss span | Purpose | Task | script_status |
|---:|---:|---:|---:|---|---|---|---|
| 1 | 0 | 25 | 25 | 00:00-00:25 | `curiosity` | A concrete misconception and prediction, no sensational statistic. | `requires_authoring_and_review` |
| 2 | 25 | 35 | 60 | 00:25-01:00 | `prerequisite` | Check essential terms and symbols; link a separate foundation route. | `requires_authoring_and_review` |
| 3 | 60 | 60 | 120 | 01:00-02:00 | `intuitive_model` | Make the central relation visible with one focus. | `requires_authoring_and_review` |
| 4 | 120 | 60 | 180 | 02:00-03:00 | `formal_model` | Connect plain language to formal notation and assumptions. | `requires_authoring_and_review` |
| 5 | 180 | 90 | 270 | 03:00-04:30 | `worked_example` | Explain why each step is selected, preserving the diagram. | `requires_authoring_and_review` |
| 6 | 270 | 45 | 315 | 04:30-05:15 | `micro_recap` | Hide the key result and ask for reconstruction. | `requires_authoring_and_review` |
| 7 | 315 | 75 | 390 | 05:15-06:30 | `guided_example` | Fade one step; allow a learner-controlled pause. | `requires_authoring_and_review` |
| 8 | 390 | 65 | 455 | 06:30-07:35 | `independent_practice` | Remove the worked method; show answer only after the attempt. | `requires_authoring_and_review` |
| 9 | 455 | 55 | 510 | 07:35-08:30 | `feedback` | Address the precise likely mistake and provide a changed problem. | `requires_authoring_and_review` |
| 10 | 510 | 50 | 560 | 08:30-09:20 | `exam_conversion` | Return to answer language, units, labels and conditions. | `requires_authoring_and_review` |
| 11 | 560 | 40 | 600 | 09:20-10:00 | `confidence_and_spacing` | Ask what was done independently; assign one delayed retrieval task. | `requires_authoring_and_review` |

Total of beat durations: **600 s** (matches `duration_s`: 600).

### 1.2 Linked 30-second technical scene (`physics_rc.json`)

- **title:** Charging takes time  |  **kind:** `rc_charge`  |  **status:** `technical_preview`  |  **duration_s:** 30  |  **fps:** 24
- **class_context:** Class 12 circuit-model technical benchmark; board coverage is not yet approved.
- **parameters:** `{"resistance_ohm": 10000, "capacitance_f": 0.0001, "source_v": 10}`
- **source:** https://openstax.org/books/university-physics-volume-2/pages/10-6-rc-circuits (Section 10.6: RC circuits); rights_status `open_reference`; retrieved_at 2026-10-13
- **claim status:** `draft` (draft; not teacher-approved)

| Cue | Start (s) | End (s) | Role | Voice | Answer visible | Caption / on-screen text |
|---:|---:|---:|---|---|---|---|
| 1 | 0 | 6 | explain | steady | no | Voltage rises quickly, then approaches the supply more slowly. |
| 2 | 6 | 11 | explain | steady | no | Keep R, C and the supply fixed. Watch the same model drive the graph. |
| 3 | 11 | 16.5 | question | curious | no | Predict: after one RC, is the capacitor fully charged? |
| 4 | 16.5 | 24 | feedback | steady | yes | No. After one RC, it reaches about 63.2% of the supply. |
| 5 | 24 | 30 | recap | steady | yes | The curve approaches 10 V; it does not jump there instantly. |

---

## 2. Chemistry pilot - `chemistry_balance_full_pilot`

- **Plan file:** `chemistry_balance_600s_plan.json`
- **status:** `blueprint_only`  |  **duration_s:** 600  |  **technical_scene:** `chemistry_balance`
- **objective:** Distinguish coefficients from molecular formulas and verify element counts.
- **board_mapping_status:** pending current syllabus and ExamLeaf source review
- **audio_status:** `not_generated`
- **prerequisites:**
  - Correct starting and product formulas are supplied.
  - Counts are conserved for each element.
  - Discrete schematic states are not a reaction mechanism or lab demonstration.
- **mandatory_reviews:** `academic`, `full_render`, `native_language_when_localized`
- **success_measures:** zero critical science errors; full timed voice listen; mobile visual review; independent item; delayed retrieval; measured human_minutes; measured generation_and_render_cost

### 2.1 The 11 beats (start / duration / end in seconds)

| # | Start (s) | Duration (s) | End (s) | mm:ss span | Purpose | Task | script_status |
|---:|---:|---:|---:|---|---|---|---|
| 1 | 0 | 25 | 25 | 00:00-00:25 | `curiosity` | A concrete misconception and prediction, no sensational statistic. | `requires_authoring_and_review` |
| 2 | 25 | 35 | 60 | 00:25-01:00 | `prerequisite` | Check essential terms and symbols; link a separate foundation route. | `requires_authoring_and_review` |
| 3 | 60 | 60 | 120 | 01:00-02:00 | `intuitive_model` | Make the central relation visible with one focus. | `requires_authoring_and_review` |
| 4 | 120 | 60 | 180 | 02:00-03:00 | `formal_model` | Connect plain language to formal notation and assumptions. | `requires_authoring_and_review` |
| 5 | 180 | 90 | 270 | 03:00-04:30 | `worked_example` | Explain why each step is selected, preserving the diagram. | `requires_authoring_and_review` |
| 6 | 270 | 45 | 315 | 04:30-05:15 | `micro_recap` | Hide the key result and ask for reconstruction. | `requires_authoring_and_review` |
| 7 | 315 | 75 | 390 | 05:15-06:30 | `guided_example` | Fade one step; allow a learner-controlled pause. | `requires_authoring_and_review` |
| 8 | 390 | 65 | 455 | 06:30-07:35 | `independent_practice` | Remove the worked method; show answer only after the attempt. | `requires_authoring_and_review` |
| 9 | 455 | 55 | 510 | 07:35-08:30 | `feedback` | Address the precise likely mistake and provide a changed problem. | `requires_authoring_and_review` |
| 10 | 510 | 50 | 560 | 08:30-09:20 | `exam_conversion` | Return to answer language, units, labels and conditions. | `requires_authoring_and_review` |
| 11 | 560 | 40 | 600 | 09:20-10:00 | `confidence_and_spacing` | Ask what was done independently; assign one delayed retrieval task. | `requires_authoring_and_review` |

Total of beat durations: **600 s** (matches `duration_s`: 600).

### 2.2 Linked 30-second technical scene (`chemistry_balance.json`)

- **title:** Same atoms. New counts.  |  **kind:** `atom_balance`  |  **status:** `technical_preview`  |  **duration_s:** 30  |  **fps:** 24
- **class_context:** Class 10 chemistry / Class 12 prerequisite repair; not a Class 12 chapter pilot.
- **parameters:** `{"coefficients": [2, 1, 2]}`
- **source:** https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations (Section 4.1: writing and balancing chemical equations); rights_status `open_reference`; retrieved_at 2026-10-13
- **claim status:** `draft` (draft; not teacher-approved)

| Cue | Start (s) | End (s) | Role | Voice | Answer visible | Caption / on-screen text |
|---:|---:|---:|---|---|---|---|
| 1 | 0 | 6 | explain | steady | no | Balance the quantities without replacing the substances. |
| 2 | 6 | 11 | explain | steady | no | Two water molecules fix oxygen—but change the hydrogen total. |
| 3 | 11 | 16.5 | question | curious | no | Your turn: how many hydrogen molecules supply four H atoms? |
| 4 | 16.5 | 24 | feedback | steady | yes | Two H₂ molecules. Now every element matches on both sides. |
| 5 | 24 | 30 | recap | steady | yes | Change coefficients, not the specified chemical formulas. |

---

## 3. Mathematics pilot - `mathematics_chain_full_pilot`

- **Plan file:** `mathematics_chain_600s_plan.json`
- **status:** `blueprint_only`  |  **duration_s:** 600  |  **technical_scene:** `mathematics_chain`
- **objective:** Differentiate a squared linear expression using the chain rule.
- **board_mapping_status:** pending current syllabus and ExamLeaf source review
- **audio_status:** `not_generated`
- **prerequisites:**
  - Real x; polynomial function.
  - The tangent and displayed derivative share the same symbolic model.
- **mandatory_reviews:** `academic`, `full_render`, `native_language_when_localized`
- **success_measures:** zero critical science errors; full timed voice listen; mobile visual review; independent item; delayed retrieval; measured human_minutes; measured generation_and_render_cost

### 3.1 The 11 beats (start / duration / end in seconds)

| # | Start (s) | Duration (s) | End (s) | mm:ss span | Purpose | Task | script_status |
|---:|---:|---:|---:|---|---|---|---|
| 1 | 0 | 25 | 25 | 00:00-00:25 | `curiosity` | A concrete misconception and prediction, no sensational statistic. | `requires_authoring_and_review` |
| 2 | 25 | 35 | 60 | 00:25-01:00 | `prerequisite` | Check essential terms and symbols; link a separate foundation route. | `requires_authoring_and_review` |
| 3 | 60 | 60 | 120 | 01:00-02:00 | `intuitive_model` | Make the central relation visible with one focus. | `requires_authoring_and_review` |
| 4 | 120 | 60 | 180 | 02:00-03:00 | `formal_model` | Connect plain language to formal notation and assumptions. | `requires_authoring_and_review` |
| 5 | 180 | 90 | 270 | 03:00-04:30 | `worked_example` | Explain why each step is selected, preserving the diagram. | `requires_authoring_and_review` |
| 6 | 270 | 45 | 315 | 04:30-05:15 | `micro_recap` | Hide the key result and ask for reconstruction. | `requires_authoring_and_review` |
| 7 | 315 | 75 | 390 | 05:15-06:30 | `guided_example` | Fade one step; allow a learner-controlled pause. | `requires_authoring_and_review` |
| 8 | 390 | 65 | 455 | 06:30-07:35 | `independent_practice` | Remove the worked method; show answer only after the attempt. | `requires_authoring_and_review` |
| 9 | 455 | 55 | 510 | 07:35-08:30 | `feedback` | Address the precise likely mistake and provide a changed problem. | `requires_authoring_and_review` |
| 10 | 510 | 50 | 560 | 08:30-09:20 | `exam_conversion` | Return to answer language, units, labels and conditions. | `requires_authoring_and_review` |
| 11 | 560 | 40 | 600 | 09:20-10:00 | `confidence_and_spacing` | Ask what was done independently; assign one delayed retrieval task. | `requires_authoring_and_review` |

Total of beat durations: **600 s** (matches `duration_s`: 600).

### 3.2 Linked 30-second technical scene (`mathematics_chain.json`)

- **title:** Two layers. One derivative.  |  **kind:** `chain_rule`  |  **status:** `technical_preview`  |  **duration_s:** 30  |  **fps:** 24
- **class_context:** Class 12: differentiation technical benchmark.
- **parameters:** `{"a": 3, "b": 1}`
- **source:** https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule (Section 3.6: the chain rule); rights_status `open_reference`; retrieved_at 2026-10-13
- **claim status:** `draft` (draft; not teacher-approved)

| Cue | Start (s) | End (s) | Role | Voice | Answer visible | Caption / on-screen text |
|---:|---:|---:|---|---|---|---|
| 1 | 0 | 6 | explain | steady | no | First change the inside. Then square its result. |
| 2 | 6 | 11 | explain | steady | no | Let u = 3x + 1. The outside function is y = u². |
| 3 | 11 | 16.5 | question | curious | no | The outside gives 2u. What factor comes from the inside? |
| 4 | 16.5 | 24 | feedback | steady | yes | Multiply by 3: dy/dx = 6(3x + 1). |
| 5 | 24 | 30 | recap | light | yes | The inside function is not on leave. Account for both layers. |

---

## 4. Biology pilot - `biology_genetics_full_pilot`

- **Plan file:** `biology_genetics_600s_plan.json`
- **status:** `blueprint_only`  |  **duration_s:** 600  |  **technical_scene:** `biology_genetics`
- **objective:** Distinguish genotype probabilities from guaranteed small-sample counts.
- **board_mapping_status:** pending current syllabus and ExamLeaf source review
- **audio_status:** `not_generated`
- **prerequisites:**
  - One Mendelian locus with two alleles and equal gamete probabilities.
  - Random gamete union; complete dominance for phenotype mapping.
  - Probabilities are not guaranteed counts in four offspring.
- **mandatory_reviews:** `academic`, `full_render`, `native_language_when_localized`
- **success_measures:** zero critical science errors; full timed voice listen; mobile visual review; independent item; delayed retrieval; measured human_minutes; measured generation_and_render_cost

### 4.1 The 11 beats (start / duration / end in seconds)

| # | Start (s) | Duration (s) | End (s) | mm:ss span | Purpose | Task | script_status |
|---:|---:|---:|---:|---|---|---|---|
| 1 | 0 | 25 | 25 | 00:00-00:25 | `curiosity` | A concrete misconception and prediction, no sensational statistic. | `requires_authoring_and_review` |
| 2 | 25 | 35 | 60 | 00:25-01:00 | `prerequisite` | Check essential terms and symbols; link a separate foundation route. | `requires_authoring_and_review` |
| 3 | 60 | 60 | 120 | 01:00-02:00 | `intuitive_model` | Make the central relation visible with one focus. | `requires_authoring_and_review` |
| 4 | 120 | 60 | 180 | 02:00-03:00 | `formal_model` | Connect plain language to formal notation and assumptions. | `requires_authoring_and_review` |
| 5 | 180 | 90 | 270 | 03:00-04:30 | `worked_example` | Explain why each step is selected, preserving the diagram. | `requires_authoring_and_review` |
| 6 | 270 | 45 | 315 | 04:30-05:15 | `micro_recap` | Hide the key result and ask for reconstruction. | `requires_authoring_and_review` |
| 7 | 315 | 75 | 390 | 05:15-06:30 | `guided_example` | Fade one step; allow a learner-controlled pause. | `requires_authoring_and_review` |
| 8 | 390 | 65 | 455 | 06:30-07:35 | `independent_practice` | Remove the worked method; show answer only after the attempt. | `requires_authoring_and_review` |
| 9 | 455 | 55 | 510 | 07:35-08:30 | `feedback` | Address the precise likely mistake and provide a changed problem. | `requires_authoring_and_review` |
| 10 | 510 | 50 | 560 | 08:30-09:20 | `exam_conversion` | Return to answer language, units, labels and conditions. | `requires_authoring_and_review` |
| 11 | 560 | 40 | 600 | 09:20-10:00 | `confidence_and_spacing` | Ask what was done independently; assign one delayed retrieval task. | `requires_authoring_and_review` |

Total of beat durations: **600 s** (matches `duration_s`: 600).

### 4.2 Linked 30-second technical scene (`biology_genetics.json`)

- **title:** A ratio is not a promise.  |  **kind:** `mendel_cross`  |  **status:** `technical_preview`  |  **duration_s:** 30  |  **fps:** 24
- **class_context:** Class 12 inheritance technical benchmark.
- **parameters:** `{"parent1": "Aa", "parent2": "Aa"}`
- **source:** https://openstax.org/books/biology-2e/pages/12-2-characteristics-and-traits (Section 12.2: characteristics and traits); rights_status `open_reference`; retrieved_at 2026-10-13
- **claim status:** `draft` (draft; not teacher-approved)

| Cue | Start (s) | End (s) | Role | Voice | Answer visible | Caption / on-screen text |
|---:|---:|---:|---|---|---|---|
| 1 | 0 | 6 | explain | steady | no | Each parent can contribute A or a with equal probability. |
| 2 | 6 | 11 | explain | steady | no | Combine one allele from each parent; keep genotype and trait distinct. |
| 3 | 11 | 16.5 | question | curious | no | Under complete dominance, what fraction shows the dominant trait? |
| 4 | 16.5 | 24 | feedback | steady | yes | Three quarters: AA and Aa show the dominant trait in this model. |
| 5 | 24 | 30 | recap | steady | yes | A 3:1 expectation does not guarantee three out of exactly four. |

---

## Shared beat template (the 11 beats common to all four plans)

The same 11 beats, shown once. These windows are a **hypothesis**, not a compulsory timing formula. They are not the same breakdown as the nine-segment 10-minute template in message 02 section 11 (0:00-0:25 diagnostic question ... 9:30-10:00 confidence checkpoint), which has different boundaries; the Ohm's-law blueprint (message 04 section 11, `../sample_scripts/BLUEPRINT_ohms_law_600_seconds.md`) uses yet another 41-beat breakdown. Student-controlled pauses add study time beyond the 600 s of media.

| Window | Duration | Purpose | Task |
|---|---:|---|---|
| 0:00-0:25 | 25 s | `curiosity` | A concrete misconception and prediction, no sensational statistic. |
| 0:25-1:00 | 35 s | `prerequisite` | Check essential terms and symbols; link a separate foundation route. |
| 1:00-2:00 | 60 s | `intuitive_model` | Make the central relation visible with one focus. |
| 2:00-3:00 | 60 s | `formal_model` | Connect plain language to formal notation and assumptions. |
| 3:00-4:30 | 90 s | `worked_example` | Explain why each step is selected, preserving the diagram. |
| 4:30-5:15 | 45 s | `micro_recap` | Hide the key result and ask for reconstruction. |
| 5:15-6:30 | 75 s | `guided_example` | Fade one step; allow a learner-controlled pause. |
| 6:30-7:35 | 65 s | `independent_practice` | Remove the worked method; show answer only after the attempt. |
| 7:35-8:30 | 55 s | `feedback` | Address the precise likely mistake and provide a changed problem. |
| 8:30-9:20 | 50 s | `exam_conversion` | Return to answer language, units, labels and conditions. |
| 9:20-10:00 | 40 s | `confidence_and_spacing` | Ask what was done independently; assign one delayed retrieval task. |
