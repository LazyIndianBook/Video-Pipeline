# Architect plan 1 — lens: library-and-DSL-first

**Lens statement (as written by the architect):** library-and-DSL-first: take the intelligence out of the model and put it into deterministic code. Strong models build, offline, a scene DSL, a component library, archetype recipes, exemplars and validators. Per video, the cheap model only fills slots in a strict schema and occasionally writes a small, sandboxed, linted draw snippet.

**Thesis:** Yes, run the strong-model experiments first. But the deliverable should not be documentation that Haiku reads and tries to imitate. Every learning from Fable 5.1 and Opus 5.5 should be compiled into something a cheap model cannot get wrong, in this order of preference: a component default, then a validator rule, a schema constraint, an exemplar, and only as a last resort a sentence in a guide. Quality then lives in the library, so the cheap model's job shrinks from "write a 400-line animation" to "pick an archetype and fill about 15 typed fields that reference approved script words and validated fixtures". Within the library's coverage, that is how Haiku or an open model gets near-Opus output at about 98x lower marginal LLM cost per lesson. Outside that coverage, quality falls back to whichever model you escalate to. The 40–100x applies only to the LLM line. Human review (about $26.67 of about $34 per lesson today) is unchanged unless it is attacked separately.

**Cost claim:** These figures are the LLM line only, with the project's 30% regeneration allowance included.

**Per 10-minute lesson (about 40 scenes):**
- **Opus-only free-form: about $33.23.** Animation is 40 × $0.60 = $24.00 and script is $1.56, then ×1.3. This is the cheap end of [V1]'s real range, which runs from $23 at low effort to $372 at max effort for 600 s.
- **Haiku DSL slot-fill: about $0.34.** Scenes are 40 × $0.0052 = $0.208 (tokenizer ×1.36 included) and script is $0.053, then ×1.3. That is about 98x cheaper, or about $0.17 through the Batch API.
- **Cascade: about $1.64**, about 20x cheaper. It adds about 10% Opus escalations, one Opus storyboard review and a Sonnet script review.

**Per 30-second Reel:**
- **Opus-only: about $3.53.**
- **Haiku DSL: about $0.041**, about 86x cheaper.
- **Cascade: about $0.38**, about 9x cheaper.

**What 40–100x does not cover.** It applies only to the LLM line. Total per lesson moves from about $65.51 (Opus-only) to about $32.62 (DSL), roughly 2x. Human review (about $26.67) is about 82% of the DSL total and stays unchanged unless addressed separately.

**One-time cost.** The offline programme is capped at $1,000 of LLM spend. That adds about $1.00 per lesson at 1,000 lessons (about 25x effective vs Opus-only) and about $0.10 per lesson at 10,000 lessons (about 75x).

**Biggest risk:** The cheap model's quality ceiling is the library's coverage. If the component library and DSL do not cover a lesson's visual needs, the Haiku system either produces samey, templated videos or escalates so often that the savings fall to cascade level (about 20x, and about 9x on Reels). Building and maintaining that library is ongoing strong-model and engineer work. All of it also rests on a harness that has not rendered a single frame on HyperFrames or Remotion yet; this Mac lacks Node 22 and FFmpeg. So week 1 has to prove the renderer before any DSL work is worth doing.

---

# Library-and-DSL-first: making cheap models produce strong-model-quality ExamLeaf videos

## 1. Thesis

[Recommendation] Do the strong-model work first, but change what it produces. A cheap model that reads a 70,000-word guide and then writes free-form HTML/JS animation will still produce poor output. Long agentic tasks are exactly where Haiku 5.5 is weakest (Terminal-Bench 4.0: 39.2% vs 70.6% for Sonnet 5.5 [N4][N37]). At low effort it also stops early or reports work as done without checking it [N9][N10][N95]. Haiku does well on bounded tasks that have tools and verifiers: tool use nearly doubles its Chartography score, from 46.4% to 86.2% [N41]. At matched max effort it slightly edges Sonnet on FrontierCode Main [N38].

So the strong models should build a **compiler, not a manual**:

- **The scene DSL.** A typed JSON scene spec, with one strict tool per archetype.
- **The component library.** Seek-deterministic, pre-tested JS components that implement the harness contract in `12_advanced_animations_with_claude/04_harness_contract/contract.md`.
- **Archetype recipes** that map Super Teacher beats to scene patterns.
- **The exemplar bank**: gold beat-to-spec pairs.
- **Validators** with error messages written for small models.
- **A short cheap-model skill** (under 500 lines [N59]).

This matches Anthropic's own skill guidance: exact scripts for fragile steps [N61], pre-made utility scripts over generated code [N64], plan-validate-execute through a machine-checkable intermediate file [N63], and validator feedback loops [N62]. The scene spec is that intermediate file. It is also what the ManimBench result points to: a 30B open model (Qwen 3 Coder) with renderer-in-the-loop plus documentation reached 94% render success and beat GPT-4.1 by 3 pp on visual similarity [N68][N69].

**Honest ceiling.** The cheap model can only produce what the library can express. "Similar quality" is a claim about the library's coverage, not about Haiku. Novel visuals still need a strong model, either as an escalation or as a new component built offline.

## 2. System design: who does what

### 2.1 Three layers

| Layer | Who | When | What |
|---|---|---|---|
| **Offline: library authoring** | Fable 5.1 (design, critique), Opus 5.5 at high, max for hard components | Weeks 1–3, then about 5 new components per month | DSL grammar; components; archetype recipes; exemplars; validators; error-message catalogue; edge-case closures; cheap-model skill |
| **Per video: slot filling** | Haiku 5.5 at medium (or an open model) | Every scene | Choose an archetype from 3 or fewer allowed options; fill a strict-schema spec; rarely, write a bounded `draw()` snippet |
| **Deterministic code** | Python/JS, no LLM | Every scene | Beat→archetype routing table; cue-sheet build (existing `validate_cue_sheet.py`); `compile_scene.py` (spec → contract HTML); lint (`lint_seek_contract.js`); determinism double-render hash (`determinism_hash_check.py`); safe-zone, text-fit, contrast and collision checks; render |
| **Escalation** | Opus 5.5 at medium, writing in the DSL, not free code | About 10% of scenes, plus one storyboard review per lesson | Specs the cheap model failed 3 times; storyboard sanity check |
| **Humans** | Academic reviewer, video reviewer | Unchanged: two approvals | Storyboard gate (frames plus spec diff) and final video |

### 2.2 What a scene spec looks like

```json
{"scene_id":"phy-10-03-s04","archetype":"ray_diagram","style":"doodle-handdrawn",
 "fixture":"fx.optics.refraction_air_water.v2","variation_seed":4127,
 "steps":[
  {"at_cue":"headline_in","do":"title.reveal","text_ref":"script:w1-3"},
  {"at_cue":"label_normal","do":"fixture.reveal_part","part":"normal_line"},
  {"at_cue":"ray_bend","do":"fixture.animate_ray","part":"ray_refracted","ease":"standard"},
  {"at_cue":"label_refraction","do":"label.pop","anchor":"ray_refracted","text_ref":"script:w17"}]}
```

Design rules that remove whole classes of failure before they happen:

- **No free on-screen text.** `text_ref` points to spans of the approved script (whose hash is already in the cue sheet) or to an academic-approved glossary ID. The model cannot misspell "refraction" or invent a formula.
- **No free science glyphs.** `fixture` and `part` must exist in the validated fixture registry, which follows the existing rule that science visuals come only from validated fixtures.
- **No times.** Steps bind to `at_cue` IDs from the cue sheet. Duration comes from narration (contract §5.5).
- **No colours or sizes.** The style is a token set from `05_style_guides/style_tokens.json`. Components own layout and safe zones.
- **Bounded variety.** `variation_seed` plus a small set of enumerated variants per component (enter direction, emphasis style), so 1,000 lessons don't look stamped from one mould.
- **Bounded snippet escape hatch.** `{"do":"custom.draw","snippet_id":...}`. The snippet is a pure `draw(ctx, t, params, rng)` of 80 lines or fewer, drawing only on a whitelisted API, with no `Date`, `Math.random`, DOM or network access. It is linted, double-render hashed, and capped at 2 snippets per scene.

### 2.3 Fit the schema to API limits

Strict structured outputs have hard caps: 20 strict tools per request [N44], 24 optional parameters in total [N45], 16 `anyOf`/type-array parameters [N46], `minItems` of 0 or 1 only [N48], and a 180 s compile timeout [N47]. Compiled grammars are cached for 24 h [N43].

[Recommendation]
- Use **one strict tool per archetype**, capped at 20 archetypes.
- Make fields required, with explicit enum defaults rather than optional fields.
- Use no nullable unions.
- Enforce array lengths in the semantic validator, not in the schema.
- Use `output_config.format`, not the deprecated `output_format` [N49].
- With thinking off, Haiku may skip a needed tool call when JSON output is also requested [N13]. So force `tool_choice` on the archetype tool, or use adaptive thinking.

## 3. Experiment programme with strong models

### 3.1 Fixed scene set: "Gold-24 + Holdout-6"

[Recommendation] Freeze 30 scenes drawn from the three pilot lessons in `07_benchmark_and_pilot_plan/` and the Reel backlog. Each has an approved script excerpt, a real cue sheet and the fixtures it needs. Six scenes stay hidden from everyone building the library, as an anti-overfit holdout (fine-tuned and templated systems regress out of distribution [N77]).

The 24 cover these archetypes:

1. Hook / title card
2. Definition card
3. Labelled-fixture reveal
4. Ray diagram (refraction)
5. Circuit build-up
6. Balancing a chemical equation
7. Graph plot with moving point
8. Algebra step-through
9. Number line
10. Comparison table
11. Cyclic process (water/carbon cycle)
12. Cause→effect chain
13. Kinetic-type emphasis
14. Recap list
15. Quiz pause and reveal
16. Common-mistake callout
17. Unit conversion
18. Vector/force arrows
19. 3D voxel insert
20. Devanagari-heavy labels
21. Assamese-script labels
22. Code-switched Hinglish labels
23. Dense cue burst (more than 3 cues per second)
24. Long-label overflow stress case

### 3.2 Arms (run in this order, per Anthropic guidance to measure the capable model at lower effort before building a cascade)

| Arm | Model / effort | Input | Purpose |
|---|---|---|---|
| E0 | Haiku 5.5 medium, free-form code, harness contract only | brief + cue sheet | The "crappy" floor: the no-skill baseline [N60] |
| E1 | Opus 5.5 at low / medium / high, free-form | same | Does a cheaper effort level of a capable model already suffice? |
| E2 | Fable 5.1 high; Opus 5.5 max on the 8 hardest | same + style guide | **Quality ceiling**: the gold renders humans rate |
| E3 | Fable 5.1 + Opus 5.5 high | E0–E2 outputs, ratings, failure logs | **Build**: DSL v0, components, recipes; re-express each gold scene as a DSL spec; check that `compile(gold_spec)` reproduces the gold render closely enough for a human to rate it the same |
| E4 | Haiku 5.5 at low / medium / high, DSL slot-fill, k = 1 and k = 3 samples | beat + cue sheet + cached library prefix | Main result |
| E5 | One open model first (Qwen 3 Coder 30B class), then DeepSeek / Kimi / GLM via the same tool schema | same | Portability; vendor hedge |
| E6 | Cascade (E4 plus Opus escalation and review) | same | Final operating configuration |

Ultracode is banned. In [V1] it burned at least 2.5M tokens (at least $348) and never finished.

### 3.3 What every run logs (the "timeline")

One JSONL line per model turn, written to `experiments/ledger/*.jsonl`:

- **Identity:** `run_id`, `arm`, `scene_id`, `model`, `effort`, `thinking` mode, prompt hash, DSL version, library git SHA, skill version.
- **Tokens per turn:** `input_fresh`, `cache_read`, `cache_write`, `output`. These must be split. [V1]'s 625K tokens ≈ $49 implies about $78/MTok blended, which is above Opus's $20 output price, so its "tokens" figure cannot include all billed tokens. Log the billed breakdown, not one total.
- **Timing and process:** wall time; tool-call count; validator result per attempt (code and field path); fix-loop count; final status (`pass` / `escalated` / `abandoned`).
- **Render evidence:** render frame hashes (two renders); rubric scores from two raters (see §5).
- **Decision log** (strong arms only): every non-obvious design choice with its rationale. These become ADRs and component defaults.
- **Failure tags** from a fixed taxonomy:

| Tag | Meaning |
|---|---|
| F-SYNC | Cue drift |
| F-OVERFLOW | Text overflows its box |
| F-SAFEZONE | Content outside the safe zone |
| F-SCIENCE | Fixture misuse or invented glyph |
| F-NONDET | Non-deterministic render |
| F-EARLYSTOP | Stopped early [N9] |
| F-FALSEDONE | Reported done without checking [N10] |
| F-LEAK | Reasoning text leaked into output [N15] |
| F-TOOLSKIP | Skipped a needed tool call [N13] |
| F-REFUSAL | Refused [N16] |
| F-STYLE | Style drift |
| F-DENSITY | Too many reveals |
| F-MONOTONY | Sameness across scenes |

### 3.4 Budget for the programme (LLM only; human rating time is the real cost)

**E1:** 24 scenes × 3 efforts × about $1.00 per scene ≈ **$72**.

**E2, Fable 5.1 high:** about **$41** for 24 scenes. Per scene:

| Item | Arithmetic | Cost |
|---|---|---|
| Cache reads | 100K × $0.25/M | $0.025 |
| Fresh input | 20K × $10/M | $0.20 |
| Output | 30K × $50/M | $1.50 |
| **Per scene** | | **$1.73** |

**E2, Opus 5.5 max:** about **$74**. Using [V1]'s max-effort rate ($49 / 79 s ≈ $0.62/s), a 15 s scene costs about $9.30, and 8 scenes cost about $74.

**E3 build:** about **$320**. Fable design sessions: 10 × about $10 = $100. Opus high component builds: 15 × a $8 cap = $120. Validators and recipes: about $100.

**E4:** about **$18**. Haiku: 24 scenes × 3 efforts × 5 samples × about $0.005, repeated over about 10 iterations.

**E5:** open-model hosting cost depends on the provider. Not priced here.

**Total cap: $1,000 of LLM spend.** Human rating is 30 scenes × about 6 arms × 2 raters × about 2 min ≈ 12 hours, plus about 40 engineer hours.

## 4. Turning experiment outputs into artefacts for cheap models

### 4.1 The closure rule

[Recommendation] Every learning and every edge case gets an owner, in this order:

1. **Component default** (the model never sees it)
2. **Validator rule** with a fix hint
3. **Schema constraint** (the model cannot express the mistake)
4. **Exemplar**
5. **Guide sentence**

Keep an `EDGE_CASE_CLOSURE_MATRIX.csv` covering the existing 65 edge cases (in `02_documentation/12_EDGE_CASES_master_table.md`), the 31 negative tests, and new failure tags. Columns: `id`, `source run`, `closure type`, `artefact path`, `test id`. Target: at least 80% closed by types 1–3. Prose is what cheap models ignore.

### 4.2 Document types and required sections

| Artefact | Path (proposed) | Required sections |
|---|---|---|
| **DSL reference** + `scene_spec.schema.json` (one strict tool per archetype) | `13_scene_dsl/DSL_REFERENCE.md` | Purpose; grammar; every field (type, enum, default, meaning); invariants the validator enforces; cue-binding semantics; snippet sandbox API; versioning and migration; 1 minimal and 1 maximal example |
| **Component card**, one per component | `13_scene_dsl/components/<name>/COMPONENT.md` + `component.js` + `params.schema.json` + `golden/` + `selftest` | What it shows; **when to use / when not to**; parameters table; cue/timing behaviour; safe-zone and layout behaviour; text limits **per script** (Latin / Devanagari / Assamese, measured with real font metrics); variants; known failure modes; 2 exemplar specs; golden-frame hashes at t = 0, mid and end |
| **Archetype recipe**, up to 20 | `13_scene_dsl/archetypes/<name>.md` | Pedagogical intent (Super Teacher beat it serves); required slots; allowed components and order; max cue density; Reel vs lesson differences; 3 exemplars; anti-patterns with the validator code that catches each |
| **Routing table** (code, not prose) | `13_scene_dsl/routing.json` | Beat type → up to 3 allowed archetypes; language → font and text-limit profile; style → token set |
| **Exemplar bank** | `13_scene_dsl/exemplars/*.json` | Beat text, cue sheet excerpt, gold spec, provenance (arm, model, rating), rating ≥ 4/5. Retrieved by archetype (3 per call), never the whole bank |
| **Validator suite** + **error catalogue** | `13_scene_dsl/validate/` + `ERROR_CODES.md` | Each code: field path, plain-English cause, **one concrete fix**, example. Written for a 30B model: short, imperative, no hedging |
| **Restrictions list** | `13_scene_dsl/RESTRICTIONS.md` | Hard forbids (free text, free glyphs, time literals, `Math.random`, CSS keyframes, editing approved script), each linked to the test that enforces it |
| **Cheap-model skill** | `03_skills/examleaf-scene-fill/SKILL.md` | Under 500 lines [N59]; one default path plus one escape hatch [N66]; references one level deep [N65]; procedure; how to read validator errors; when to escalate; a verification step ("you are not done until the validator returns 0") [N10] |
| **Model profile**, per cheap model | `13_scene_dsl/model_profiles/<model>.md` | Effort, thinking mode, tool_choice, sample count k, prompt deltas, measured pass rates, known quirks (for example, refusals [N16]); re-measured on every model release |
| **Learnings log / ADRs** | extend `14_DECISIONS_and_OPEN_QUESTIONS.md` | Decision, evidence (`run_id`s), alternatives rejected, closure artefact |

Skills should be tested on every model that will run them: Haiku may need more guidance, Opus may over-explain [N58]. Write the evals before writing much documentation, with at least three per skill [N60]. Gold-24 is that eval set.

## 5. Cheap-model operating procedure (per scene)

1. **Code:** route the beat to its allowed archetypes. Build the cue sheet. Fetch the fixture IDs and the 3 exemplars for that archetype.
2. **Haiku 5.5, effort medium** (fixed per pipeline, because changing effort invalidates the cache [N14]):
   - Cached prefix (about 12K tokens: skill, DSL summary, archetype tool schema) followed by the fresh scene payload (about 3K tokens).
   - Forced tool call. Adaptive thinking on.
   - Prompt stays well under 100K tokens to avoid the 5x price tier [N5][N82].
3. **Code:** schema check, semantic lint, compile, contract lint, double-render hash, then automated visual checks (safe zone, text box fit, overlap/collision, blank frames, contrast). Errors go back as `ERROR_CODES` entries.
4. **Retry** with the error, up to 3 attempts. [Hypothesis] Run k = 3 in parallel for archetypes with a first-pass rate below 70%, and take the first that passes every check plus the highest rubric-proxy score. Repeated sampling with a real verifier beats a stronger single shot [N88][N89]. Without a verifier it plateaus [N92], so never sample without the validator.
5. **Escalate** to Opus 5.5 medium, writing in the DSL, on: 3 failures, a `refusal` stop_reason (no server-side fallback; retrying usually refuses again [N16]), or a request for a visual that no archetype covers. Escalations needing a new component are logged as library backlog.
6. **Per lesson:** Opus reviews all specs and storyboard frames once. Then the human storyboard gate, then the final human approval.

## 6. Quality gates and evals

| Gate | Check | Blocking? |
|---|---|---|
| G0 | Strict schema | Yes |
| G1 | Semantic lint: cues exist, text_refs resolve to the approved script hash, fixtures exist, density limits | Yes |
| G2 | Contract lint plus double-render frame-hash equality | Yes |
| G3 | Automated visual checks: safe zone, text fit, overlap, contrast, blank frames | Yes |
| G4 | Opus storyboard review; 10% of scenes randomly sampled for VLM rubric scoring | Flags only |
| G5 | Two human approvals | Yes (unchanged) |

**Rubric (1–5, two raters):** scientific correctness, narration sync, legibility on a phone, motion quality, style adherence, variety.

**Primary eval:** a blind pairwise comparison on Holdout-6 plus Gold-24: Haiku-DSL vs E2 gold.

[Hypothesis] **Go/no-go targets for week 6:**

| Metric | Target |
|---|---|
| Render success within 3 attempts | ≥ 95% |
| G0–G3 first-pass rate | ≥ 70% |
| Escalation rate | ≤ 15% |
| Pairwise win-or-tie on correctness and sync | ≥ 80% |
| Pairwise win-or-tie on motion appeal | ≥ 60% |
| Human review minutes per lesson | No higher than the 85-minute baseline |

These are targets, not measured results. The eval suite is the portable asset: when Haiku 5.5 is replaced, re-run it rather than re-documenting.

## 7. Cost model

**Assumptions** (labelled [Hypothesis] unless they come from project files):

- A 10-min lesson has about 40 scenes of about 15 s. A 30 s Reel has 4 scenes.
- **Script/pedagogy workload** (project v2 model): Sonnet 120K/25K, Opus review 60K/10K, Haiku 20K/3K, totalling 200K input / 38K output, plus a 30% regeneration allowance. Applied to every scenario.
- **Haiku tokenizer padding:** Haiku token counts are padded ×1.36 for the newer tokenizer [N2][N42].

### 7.1 Per 10-minute lesson

**A. Opus 5.5 only** (high effort, free-form scene code against the harness, no library). Per scene, with a conservative 1.5 attempts built in (cache writes ignored as minor):

| Item | Arithmetic | Cost |
|---|---|---|
| Cache reads | 100K × $0.20/M | $0.02 |
| Fresh input | 20K × $4/M | $0.08 |
| Output | 25K × $20/M | $0.50 |
| **Per scene** | | **$0.60** |

| Line | Arithmetic | Cost |
|---|---|---|
| Animation | 40 scenes × $0.60 | $24.00 |
| Script (Opus) | 200K × $4/M + 38K × $20/M = $0.80 + $0.76 | $1.56 |
| **Total** | ($24.00 + $1.56) × 1.3 | **$33.23** |

Cross-check against [V1]: low effort ran at $0.038/s, so 600 s ≈ $23. Max effort ran at $0.62/s, so 600 s ≈ $372. Scenario A therefore sits at the *cheap* end of what Opus has actually cost. All ratios below are understated, not inflated.

**B. DSL-first cheap system** (Haiku 5.5 medium). Per attempt:

| Item | Arithmetic | Cost |
|---|---|---|
| Cached prefix | 12K × $0.01/M | $0.00012 |
| Fresh input | 3K × $0.10/M | $0.0003 |
| Output (spec plus thinking) | 3.2K × $0.50/M | $0.0016 |
| **Per attempt** | | **$0.00202** |

Per scene:

| Item | Arithmetic | Cost |
|---|---|---|
| Spec attempts | 1.5 × $0.00202 | $0.00303 |
| Snippets (20% of scenes, 2 attempts × 4K output) | 0.2 × 2 × 4K × $0.50/M | $0.0008 |
| Subtotal | | $0.00383 |
| **Per scene** (×1.36 tokenizer) | | **$0.0052** |

| Line | Arithmetic | Cost |
|---|---|---|
| Scenes | 40 × $0.0052 | $0.208 |
| Script (Haiku, split into calls under 100K) | (200K × $0.10/M + 38K × $0.50/M) × 1.36 = ($0.02 + $0.019) × 1.36 | $0.053 |
| **Total** | ($0.208 + $0.053) × 1.3 | **$0.34** |

**33.23 / 0.34 ≈ 98x.** Running the non-interactive spec generation through the Batch API (50% off [N21]) brings it to about $0.17.

**C. Cascade** (B plus about 10% Opus escalation, an Opus storyboard review and a Sonnet script review):

| Line | Arithmetic | Cost |
|---|---|---|
| Haiku scenes | as in B | $0.208 |
| 4 Opus DSL escalations | each 12K × $0.20/M + 3K × $4/M + 6K × $20/M = $0.134 | $0.538 |
| Opus storyboard review | 40K × $4/M + 4K × $20/M | $0.24 |
| Script (Haiku) | as in B | $0.053 |
| Sonnet script review | 60K × $2/M + 10K × $10/M | $0.22 |
| **Total** | $1.259 × 1.3 | **$1.64** |

**33.23 / 1.64 ≈ 20x.**

### 7.2 Per 30-second Reel

**A:** script at 1/5 of the lesson workload = 40K × $4/M + 7.6K × $20/M = $0.31. Animation = 4 × $0.60 = $2.40. Total ($0.31 + $2.40) × 1.3 = **$3.53**.

**B:** scenes 4 × $0.0052 = $0.021, plus script $0.011. Total ($0.021 + $0.011) × 1.3 = **$0.041**, about **86x**.

**C:**

| Line | Cost |
|---|---|
| Haiku scenes | $0.021 |
| 1 Opus escalation | $0.134 |
| Opus review (10K × $4/M + 2K × $20/M) | $0.08 |
| Script (Haiku) | $0.011 |
| Sonnet review (12K × $2/M + 2K × $10/M) | $0.044 |
| **Total** (×1.3) | **$0.38**, about **9x** |

A fixed escalation dominates a small job.

### 7.3 What the 40–100x does and does not apply to

**It applies to the per-video LLM line only.**

**Total per lesson.** The project's hybrid cost is about $34 per lesson, which includes $1.72 of LLM. That leaves about $32.28 of non-LLM cost: narration $0.96, render, storage, and human review of about $26.67.

| Scenario | Total per lesson |
|---|---|
| A | $32.28 + $33.23 = $65.51 |
| B | $32.28 + $0.34 = $32.62 |
| C | $32.28 + $1.64 = $33.92 |

So the total-cost ratio between A and B is about **2x, not 98x**. Human review is about 82% of B's total.

**The honest framing:** the DSL lets you *add* Opus-grade animation for almost no change in the LLM line versus today. It does not make videos 40–100x cheaper overall.

[Hypothesis] **Reducing review time.** Pre-validated components and spec-level diffs could cut storyboard review time. 85 → 60 minutes would save $26.67 × 25/85 ≈ $7.84 per lesson, which is 23x B's whole LLM line.

**Amortised offline cost.** The $1,000 programme cap is $1.00 per lesson at 1,000 lessons, which makes the effective B cost $1.34 (about 25x vs A). At 10,000 lessons it is $0.44 (about 75x). Add library maintenance: about 5 new components per month at an $8 cap each.

## 8. Risks and failure modes

1. **Library ceiling and sameness.** Everything looks templated, and novel pedagogy needs new components. Mitigations: variants and seed variation; an F-MONOTONY rating; a monthly component backlog fed by escalation logs.
2. **The library becomes the bottleneck.** Building components is strong-model plus engineer work. Budget it as ongoing product work, not a one-off.
3. **Overfitting to Gold-24.** Mitigations: Holdout-6, rotated quarterly; out-of-distribution regression is real [N77].
4. **Nothing has rendered yet.** This Mac lacks FFmpeg and Node 22, and the HyperFrames vs Remotion benchmark is pending. The whole plan rests on the harness actually rendering, so de-risk it in week 1. [Recommendation] Build one compile backend (HyperFrames default) and keep the DSL renderer-agnostic. Add a Remotion backend only if the benchmark demands it.
5. **Validators pass but the lesson is bad pedagogy.** G5 humans stay. The rubric includes pedagogy.
6. **Haiku quirks:** early stopping and false "done" [N9][N10], reasoning leakage [N15], tool skips with JSON output [N13], refusals with no fallback [N16], the price tier above 100K tokens [N5], tokenizer inflation [N2]. Each is closed by procedure (§5) or by measurement in the model profile. Several sources are flagged as contested, so re-verify before relying on them.
7. **Open-model operations.** Hosting cost, data residency and tool-schema compatibility are unmeasured. Treat E5 as a hedge, not a plan dependency. Fine-tuning on accepted specs is a later option: distillation recovered about 90% of teacher accuracy at 5x lower cost [N75] from as few as 446 demonstrations [N78]. It is only worth it once there are hundreds of rated specs.
8. **Skill supply chain.** Install and audit skills only from trusted sources [N29].

## 9. Six-week rollout

**Week 1: foundation and baselines**
- Install Node 22 and FFmpeg; pass `preflight.sh`; render `scene_template.html` on HyperFrames.
- Freeze Gold-24 and Holdout-6 with real cue sheets.
- Stand up the run ledger.
- Run E0 (Haiku free-form) and E1 (Opus low/medium/high).

**Week 2: gold runs and DSL draft**
- Run E2 gold renders (Fable high; Opus max on the 8 hardest).
- Two-rater rubric; failure taxonomy counts.
- Fable drafts DSL v0, an archetype list of up to 20, and a component inventory.

**Week 3: library build**
- Opus high builds 12–15 components with self-tests and golden frames.
- Build `compile_scene.py`, the validators and `ERROR_CODES.md`.
- Re-express the gold scenes as specs (the exemplars).
- Gate: compiled gold specs are rated within 0.5 of the original gold.
- Fill the edge-case closure matrix.

**Week 4: cheap-model tuning**
- Run E4 (Haiku at low/medium/high, k = 1 and k = 3).
- Iterate error messages and the skill, never by adding prose first (closure order).
- Run E5 with one open model.
- Write the model profiles.

**Week 5: holdout and first full lesson**
- Holdout-6 blind pairwise eval.
- Set the cascade thresholds.
- Produce one full pilot lesson (about 40 scenes) end-to-end under C, measuring human review minutes against the 85-minute baseline.

**Week 6: decision**
- Two more pilot lessons and 5 Reels.
- Check the go/no-go targets (§6).
- Freeze library v1 and write the operations runbook.
- Decide B vs C as the default, and whether to fund a review-time reduction track.

