# Documentation templates for the ExamLeaf Production Kit

These are fill-in templates for the artefacts listed in strategy §4. Copy each one into `12_advanced_animations_with_claude/08_production_kit/`.

**Rules for every field:**
- Every field marked **(req)** is required.
- Every claim must cite a `run_id` from `experiments/ledger/`, or be labelled `[Hypothesis]`.
- No artefact is merged without its linked test.

---

## 1. Guide: per-archetype skill (`skills/examleaf-fill-<archetype>/SKILL.md`)

Keep the skill body under 500 lines. References must point one level deep only. Test the skill on Haiku, Sonnet and Opus before release.

```markdown
---
name: examleaf-fill-<archetype>                     # (req) lowercase, hyphenated
description: Fill the <archetype> scene template for an ExamLeaf vertical lesson beat. Use when the routed archetype is <archetype>.   # (req) one sentence: what + when
---

# Fill <archetype> (Kit v<x.y.z>)

## 1. When to use / when not  (req)
- Use when: <routed archetype = X; beat type = Y>
- Do not use when: <no fixture exists → output UNKNOWN_ARCHETYPE>; <more than N reveals needed → ESCALATE>

## 2. Default path  (req, exactly one) + escape hatch (req, exactly one)
Default: choose template `<template_id>` variant from {<enum>}; bind steps to cue IDs in order.
Escape hatch: if <condition>, set `"escalate": "<reason_code>"` and stop.

## 3. Slot table  (req)
| Field | Type | Allowed values / default | Meaning |
|---|---|---|---|

## 4. Rules  (req, 8–15; each links a detector)
1. MUST bind every step to an existing cue ID. — detector V0-CUE-EXISTS
2. NEVER write on-screen text; use `text_ref` spans only. — detector V2-TEXT-SUBSET
...

## 5. Pre-submit checklist  (req, ≤10 yes/no)
- [ ] Every `text_ref` resolves to the approved script?
...

## 6. Reading validator errors  (req)
Each error has `code`, `path`, `expected`, `got`, `fix`. Apply only the `fix`. Change nothing else.

## 7. Verification  (req)
You are not done until the validator returns 0 errors. Never state that the scene is complete.

## 8. Escalate when  (req)
<3 failed attempts handled by controller>; UNKNOWN_ARCHETYPE; missing fixture; refusal.

## 9. References  (req)
- Golden: G-<arch>-01, G-<arch>-02   - Negative: N-<rule>-01
- Template card: ../../templates/<template_id>/TEMPLATE.md

## 10. Evals  (req, ≥3)
| Eval ID | Input package | Expected | Pass rule |
```

**Example row (§10 Evals):**

| Eval ID | Input package | Expected | Pass rule |
|---|---|---|---|
| EV-5-01 | DEV-5-1 (Ohm's-law numerical, Hinglish, doodle) | 4 steps bound to cues c3–c6; `text_ref` for "V = IR" | V0–V5 exit 0 within 3 attempts in ≥ 4/5 samples |

---

## 2. Restrictions (`RESTRICTIONS.md` and machine-readable `restrictions.json`)

Every restriction needs a way to enforce it. A restriction without enforcement is marked `advisory` and reviewed monthly for promotion to a check.

| Field | Req | Meaning |
|---|---|---|
| `id` | req | `R-###` |
| `statement` | req | One imperative sentence |
| `applies_to` | req | `cheap-tier` / `all-tiers` / `templates` / `humans` |
| `enforcement` | req | `schema:<path>` / `lint:<rule>` / `verifier:<V-id>` / `HUMAN-ONLY` / `advisory` |
| `negative_test` | req | ID in `06_prompts_and_templates/negative_tests.md` or a new `NT-###` |
| `severity` | req | `block` / `flag` |
| `rationale` | req | Why, with run IDs or a source |
| `since_kit` | req | Kit version |
| `owner` | req | Person |

**Example rows:**

| id | statement | applies_to | enforcement | negative_test | severity | rationale | since_kit | owner |
|---|---|---|---|---|---|---|---|---|
| R-001 | Never put on-screen text that is not a `text_ref` span of the approved script or a glossary ID | cheap-tier | schema:`steps[].text_ref` (no free-text field exists) + verifier:V2-TEXT-SUBSET | NT-032 | block | Prevents misspellings and leaked reasoning [N15]; runs C0-* show F-LEAK | 0.1.0 | Founder |
| R-007 | Never use `Math.random`, `Date`, timers or network in scene code | all-tiers | lint:`no-nondeterminism` (`lint_seek_contract.js`) + verifier:V3 | existing #4 | block | Seek-deterministic contract §5 | 0.1.0 | Founder |
| R-019 | Never send a Haiku prompt above 60K tokens | controller | code:`token_guard` | NT-040 | block | 100K price tier [N20][N82] | 0.1.0 | Founder |

---

## 3. Edge-case register entry (extends `02_documentation/12_EDGE_CASES_master_table.md`)

| Field | Req | Meaning |
|---|---|---|
| `id` | req | Existing `EC-##` or new `EC-###` |
| `trigger` | req | Input condition that causes it |
| `symptom` | req | What a viewer or reviewer sees |
| `detector` | req | V-rule ID, or `HUMAN-ONLY` |
| `closure_rung` | req | 1 template default · 2 schema · 3 validator · 4 exemplar · 5 prose |
| `artefact_path` | req | File that implements the closure |
| `regression_test` | req | Test ID |
| `first_seen_run` | req | `run_id` |
| `frequency` | req | n/attempts per model × effort (from ledger) |
| `cheap_tier_handling` | req | `handle` / `escalate` / `refuse` |
| `status` | req | `open` / `closed` / `accepted-risk` |
| `notes` | opt | |

**Example row:**

| id | trigger | symptom | detector | closure_rung | artefact_path | regression_test | first_seen_run | frequency | cheap_tier_handling | status |
|---|---|---|---|---|---|---|---|---|---|---|
| EC-071 | Devanagari label > 14 grapheme clusters at 64 px in `fixture_reveal` | Label overflows callout box; conjunct clipped | V4-INDIC-FIT | 1 (template auto-wraps by grapheme cluster, and shrinks to min 48 px) | `templates/fixture_reveal/component.js` | NT-051 | C3-DEV-3-2-med-s1 | Haiku-med 7/15; Opus-med 1/24 (pre-fix) | handle | closed |

---

## 4. Learnings ledger entry (`LEARNINGS.md`, plus an ADR in `14_DECISIONS_and_OPEN_QUESTIONS.md`)

```markdown
### L-### — <short claim>            (req)
- Date: YYYY-MM-DD                       (req)
- Claim: <one sentence>                  (req)
- Evidence: run_ids <…>; n=<…>; effect=<…> (95% CI <…>)   (req)
- Models/efforts affected: <…>           (req)
- Alternatives considered and rejected: <…>   (req)
- Promoted to: template | schema | validator | exemplar | prose — path <…>   (req)
- Revisit trigger: <metric/threshold or event>   (req)
- Status: adopted | rejected | watch     (req)
- ADR: ADR-###                           (req if adopted)
```

**Example:**
- **L-014: Best-of-3 beats a third repair turn on `equation_balance`.**
- **Date:** 2026-11-05.
- **Evidence:** C3-DEV-7-* runs. Pass-within-caps was 0.87 with best-of-3 against 0.73 with a third repair, n = 15 scene-samples each. [Illustrative format, not a result.]
- **Models/efforts affected:** Haiku medium.
- **Alternatives considered and rejected:** raising effort to high (cost per accepted scene was higher).
- **Promoted to:** capability ledger row `equation_balance` (k = 3).
- **Revisit trigger:** first-pass rate rises above 70%.
- **Status:** adopted.
- **ADR:** ADR-021.

---

## 5. Exemplar cards

### 5.1 Golden card (`exemplars/golden/<archetype>/G-<arch>-##.md` + `.spec.json` + `keyframes/`)

| Field | Req | Meaning |
|---|---|---|
| `id`, `archetype`, `template_id`, `style`, `subject`, `language` | req | Tags used for lookup retrieval |
| `provenance` | req | arm, model, effort, date, Kit hash, cost USD, tokens |
| `input_brief` | req | Exact brief text and package ID (dev set only, never holdout) |
| `slot_json` | req | The accepted spec |
| `keyframes` | req | t = 0, mid, end, plus any cue-critical frames |
| `trace_150w` | req | Plan, then the 2–3 errors hit, then how each was fixed (≤ 150 words) |
| `decisions` | req | DECISIONS block items, each tagged with a rule ID |
| `fixed_vs_varies` | req | Slot map: which fields copy across briefs and which must change |
| `verifier_report` | req | V0–V7 all green; hash pair |
| `human_scores` | req | Two rater sheets, both ≥ 4 on accuracy and legibility |
| `fixtures_licence` | req | Fixture IDs and licence notes |
| `approved_by` | req | Academic reviewer and date |

**Example (header only):** `G-6-01`.
- **Tags:** `graph_build`, `editorial-vox`, Physics, English.
- **Provenance:** P-med; claude-opus-5-5; medium; 2026-10-29; Kit 0.4.0; $0.098.
- **Fixed vs varies:** axis style fixed; data series comes from fixture `fx.vi_curve.ohmic.v1`; labels vary through `text_ref`.

### 5.2 Negative card (`exemplars/negative/<rule_id>/N-<rule>-##.md`)

| Field | Req | Meaning |
|---|---|---|
| `id`, `rule_id` | req | Violated rule |
| `source_run` | req | Real failing `run_id`. Never synthetic. |
| `bad_output` | req | Minimal excerpt of the failing spec or code |
| `detector_message` | req | Exact text the validator returned |
| `corrective_diff` | req | Minimal diff that makes it pass |
| `frequency` | req | n/attempts at the time of writing |
| `archetypes` | req | Where to include it |

**Example row:**

| id | rule_id | source_run | detector_message | corrective_diff | frequency |
|---|---|---|---|---|---|
| N-V0-CUE-02 | V0-CUE-EXISTS | C3-DEV-4-1-med-s2 | `V0-CUE-EXISTS at steps[3].at_cue: expected one of [c4,c5,c6], got "c7". Fix: use "c6" (last cue in scene).` | `- "at_cue":"c7"` → `+ "at_cue":"c6"` | 9/45 |

---

## 6. Capability ledger row (`CAPABILITY_LEDGER.csv`)

| Field | Req | Meaning |
|---|---|---|
| `task` | req | `scene_fill` / `section_script` / `beat_routing` / `reel_hook` / `caption` / `judge` |
| `archetype_or_family` | req | e.g. `worked_numerical` or `symbolic` |
| `language` | req | `en` / `hi-Latn` (Hinglish) / `hi` / `as` / `any` |
| `approved_tier` | req | `haiku` / `haiku-xhigh` / `sonnet` / `opus-low` / `opus` / `human` |
| `effort` | req | Exact `output_config.effort` value |
| `request_shape` | req | `format+adaptive` / `auto+strict+adaptive` / … |
| `k` | req | Samples per round |
| `attempt_cap` | req | Including repairs |
| `escalation_rule` | req | Next tier and triggers |
| `holdout_result` | req | k/n scenes, Wilson LB |
| `escape_rate` | req | Defects per lesson that passed V0–V7 |
| `cost_per_accepted_unit_usd` | req | Measured, including escalations |
| `status` | req | `provisional` / `confirmed` (n ≥ 40, LB ≥ 0.87) / `revoked` |
| `evidence_runs` | req | run IDs |
| `date`, `next_review` | req | |

**Example row (format only; values are placeholders until C4):**

`scene_fill,symbolic,any,haiku,medium,format+adaptive,1,3,"haiku-xhigh→sonnet-medium→opus-medium; refusal→sonnet",22/24 LB 0.74,0.3,0.0061,provisional,"C4-HO-4-*,C4-HO-5-*,C4-HO-7-*",2026-11-12,2026-12-12`

---

## 7. Verifier spec (`VERIFIER_SPEC.md`, one block per rule, plus `ERROR_CODES.md`)

| Field | Req | Meaning |
|---|---|---|
| `rule_id` | req | `V<n>-<NAME>` |
| `property` | req | What must be true |
| `stage` | req | V0…V7 |
| `implementation` | req | Script path and function |
| `inputs` | req | Spec, DOM samples at t, frames, cue sheet, fixtures |
| `threshold` | req | Exact numeric tolerance |
| `fp_rate_dev`, `fn_rate_negative` | req | Measured on the dev set and the negative suite |
| `message_template` | req | `{code} at {path}: expected {expected}, got {got}. Fix: {one_fix}` |
| `blocking` | req | yes/no |
| `cost` | req | ~0 / render seconds / LLM $ |
| `owner`, `since_kit` | req | |

**Example block:**

```yaml
rule_id: V5-CUE-SYNC
property: Every step's visible onset lands on its bound cue's word t0 or up to 0.05 s before it, never late (04_harness_contract/contract.md §8; 12/10 A10). Corrected 15 Oct 2026: was ±150 ms
stage: V5
implementation: extend examleaf-anim-qa/scripts/safe_zone_check.py --cues (existing reveal-sync check); no new verifier
inputs: [cue_sheet.json, word_timings.json, DOM samples at 30 fps around each cue]
threshold: "word_start - 0.05 s - 1 frame <= onset <= word_start + 1 frame; onset > word_start fails; > 0.10 s early warns. |onset - word_start| <= 150 ms is logged as a quality metric only [Hypothesis; calibrate in week 3]"
fp_rate_dev: "TBD (week 3)"
fn_rate_negative: "TBD (must reject NT-012, NT-013)"
message_template: "V5-CUE-SYNC at steps[{i}]: expected onset in [{word_start}-0.05s, {word_start}] (cue {cue_id}), got {onset}. Fix: bind to cue {nearest_cue} or remove the step."
blocking: yes
cost: "~0 (seek-sampled frames)"
owner: Founder
since_kit: 0.2.0
```

---

## 8. Experiment record (`experiments/records/EXP-###.md`)

One record per arm per week. The ledger holds the rows; this file holds the summary.

```markdown
# EXP-### — <arm> on <set>             (req)
- Dates / operator: <…>                 (req)
- Hypothesis being tested: <…>          (req)
- Config: model <id>, effort <…>, thinking <…>, request_shape <…>, k <…>, attempt_cap <…>,
  docs tier <bare|trim|full|pack|kit>, Kit version/sha <…>, caps <$/scene>   (req)
- Scene set: <ids or set name>; samples per scene <…>   (req)
- Preconditions verified: preflight log <path>; token guard on; append-only on   (req)
- Results (req):
  | Metric | Value | 95% CI (Wilson / bootstrap) |
  |---|---|---|
  | Scenes passing (≥4/5 samples) | | |
  | Sample pass-within-caps | | |
  | Mean rubric by item (rated subset) | | |
  | Escalation rate by tier | | |
  | Cost per accepted scene (USD, billed) | | |
  | Cache-read ratio | | |
  | Failure-tag distribution | | |
  | Refusals (by category) | | |
- Deviations from protocol: <…>         (req, "none" allowed)
- Interpretation (label [Recommendation]/[Hypothesis]): <…>   (req)
- Closures created: EC/R/V/N IDs <…>    (req)
- Next action and owner: <…>            (req)
```

**Example header:**
- **Record:** EXP-012, C3 on dev.
- **Config:** Haiku 5.5; efforts low, medium, high and xhigh; adaptive thinking; `format+adaptive`; k ∈ {1, 3}; cap 3; Kit 0.4.0; $0.02 per scene.
- **Scene set:** DEV-* (24); 5 samples per scene.

---

## 9. Model profile (`model_profiles/<model>.md`): short form

| Field | Req |
|---|---|
| Pinned model ID; provider; data and retention terms | req |
| Request shape that works (effort, thinking, format or tool) | req |
| Token factor vs `claude-opus-5-5` on ExamLeaf prompts, per language (count_tokens) | req |
| Known quirks with evidence (early stop, false done, leaks, tool skip, refusals) | req |
| Pass rates per family (dev and holdout), cost per accepted scene | req |
| Price-tier cliffs and caching rules | req |
| Date last re-measured; trigger for re-measure | req |

**Example row (format only):** `claude-haiku-5-5`, Anthropic API.
- **Request shape:** `output_config.effort=medium`, adaptive thinking, `format+adaptive`.
- **Token factor:** en 1.0x / hi TBD / as TBD (week 1).
- **Quirks:** forced `tool_choice` gives no thinking block [D2]; no refusal fallback [N16].
- **Price-tier cliff:** prompts above 100K are billed at $0.50/$2.50.
