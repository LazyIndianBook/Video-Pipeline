# Strong-to-cheap model strategy: making Haiku-class and open models produce Opus/Fable-quality ExamLeaf videos

**Prepared:** 2026-10-15 for the ExamLeaf founder and academic team.
**Scope:** Vertical 9:16 STEM revision lessons (about 10 min) and 20–60 s Reels for Assam Board Class 10–12. Covers the advanced-animation layer (`12_advanced_animations_with_claude/`) and the text tasks that feed it.

**Labels:**
- **[Recommendation]** marks a judgement call.
- **[Hypothesis]** marks a number or claim that is not measured yet.
- Unlabelled facts carry a citation.

**Citation codes:**
- **[N#]**: the verified evidence list (see the sources document).
- **[D#]**: Anthropic API reference notes I checked against the bundled Claude API skill (cached 2026-10-06).
- **[P#]**: ExamLeaf project files.
- **[V1]**: the Devarf reference experiment.

**Nothing below has been metered on ExamLeaf.** No ExamLeaf scene has been rendered on real HyperFrames or Remotion, and this Mac lacks FFmpeg and Node 22. Every token count and attempt rate here is an assumption until the week-1 meters replace it.

**Audit corrections (15 Oct 2026).** This document was corrected against `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` (major findings M3, M4, M12 and the section-13 minor findings). Edited lines say "corrected 15 Oct 2026". The gate order is fixed in §2.1 and §5.5, Reel approvals in §5.7, and the verifier stack in §2.4. The cost framing is recomputed in §7.14. New decisions D-16…D-21 are in §11.1.

---

## 0. Executive answer

1. **What I think, and the proper way to go.** Yes, do the experiments with strong models first. But don't aim them at writing a long manual for Haiku to read.
   - Use Fable 5.1 and Opus 5.5 as **offline compilers**. They build a *Production Kit*:
     - parameterised scene templates with strict slot schemas
     - deterministic verifiers with error messages a small model can act on
     - a failure catalogue, where every entry is linked to the check that detects it
     - golden and negative exemplars
     - one short skill per archetype
     - a sealed eval set
   - The cheap model then fills slots inside that Kit. **Only verifier verdicts advance work.** The cheap model's own claim that it is "done" is never trusted.
   - Failures climb a cascade: Haiku, then Haiku at higher effort, then Sonnet, then Opus, then a human.
2. **Documentation alone will not stop Haiku producing poor videos.** Haiku 5.5 is weak exactly where free-form video generation needs strength:
   - long agentic work: Terminal-Bench 39.2% vs 70.6% for Sonnet [N4]
   - stopping early at low effort [N9][N95]
   - claiming work is done without checking [N10]
   - skipping a needed tool call when JSON is requested [N13]
   - reasoning text leaking into output [N15]
   - refusing with no fallback [N16]

   Prose only lowers how often these happen. Code, schemas and verifiers make whole classes of error impossible, or catch them before a human sees them.
3. **Build the Kit first, choose the model second.** The Kit makes *every* model cheaper and more reliable, Opus included. Following Anthropic's guidance, measure Opus 5.5 at **low** effort on the Kit before building a cross-model cascade, and judge **cost per completed task**, not cost per request.
   - If Opus-low on the Kit passes parity, the cascade's extra machinery saves about $3–4.5 per lesson at most (§7).
4. **Honest LLM-line ratios** [Hypothesis, central workload in §7]:
   - **Per call:** Opus 5.5 to Haiku 5.5 is 38x, and Fable 5.1 to Haiku 5.5 is 94x.
   - **Per 10-minute lesson, like for like** (the same Kit for every model):
     - about **19x** if Haiku does all text and scenes and passes
     - about **5x** for the protected cascade (central case)
     - about **4x** in the pessimistic case
5. **Where 40–100x is real, it comes mostly from architecture, not model price.**
   - Against bespoke, free-form strong-model generation of the [V1] kind, the cascade is 11–344x cheaper per lesson. The range is wide because [V1]'s dollars and tokens don't reconcile (§7.7).
   - Fable-on-the-Kit against Haiku-on-the-Kit is 46x, but only if Haiku needs no escalation.
6. **Total cost per video barely moves from the model swap** *(superseded for ExamLeaf on 15 Oct 2026: the founder has set human review to $0; see §7.13. Corrected 15 Oct 2026 in §7.14, using one price basis (5.5 tariffs) and generated clips at $0 per RD-39. The cascade is about 4% below today's pipeline and about 60% below an Opus-only Kit. At the lean floor, which applies to Path B TTS content only, the best documented ratio is ≈7× against an Opus-only Kit (≈6.2× from 1 Jan 2027) and 14–27× against bespoke [V1]-low generation (12–23× from 2027). 40–100× appears only against [V1]-max bespoke runs.)*
   - The LLM line is about 5% of the project's $34.34 hybrid variable cost [P1].
   - The cascade changes the total by about **−2% against today** and about **−12% against an Opus-only Kit**.
   - The real levers are human review ($26.67 for 85 minutes [P1]) and the $4.00 generated-clip allowance:
     - cutting 25 review minutes saves $7.84 per lesson
     - setting generated clips to zero, which the cost model itself recommends [P4], saves $4.00
7. **Architecture** (§2): the verifier-and-cascade design is the spine. Two further ideas are grafted on:
   - from the DSL plan, **constrained slot-fill templates** with no free on-screen text, no free science glyphs, no time literals and no free colours
   - from the economics plan, **cost per accepted lesson** as the headline metric

   Humans keep every approval. GA (academic, bound to the script-bundle hash) and the H-SB storyboard gate come before any synthesis. GF (full video) comes after the A-suite, and every Reel gets its own GS (corrected 15 Oct 2026; §5.5, §5.7). Best-of-N sampling is used only where a real verifier exists [N88–N92].
8. **Experiment programme** (§3 and the protocol document): six weeks.
   - **Budget:** an LLM cap of about $1,000, about 54 rater-hours, about 16 academic approval hours, and about 185 engineer-hours [Hypothesis].
   - **What it tests:**
     - the founder's "just document it" idea directly, with a full-manual arm
     - the text tasks: scripts in English, Hinglish, Hindi and Assamese captions; beat segmentation; Reel hooks
     - a sealed holdout of 24 scenes
     - one "Ultra" ceiling probe ($50): an attended, founder-approved exception with a provider-side spend limit that can never enable ultracode in production (D-9, corrected 15 Oct 2026)
9. **Week 1 is a blocker, not a formality.**
   - Install Node 22 and FFmpeg, and render one scene deterministically.
   - Meter real tokens. Run `count_tokens` on identical ExamLeaf prompts (including Hindi and Assamese) for `claude-haiku-5-5` and `claude-opus-5-5`.
   - Don't believe any ratio in this document until those meters exist.
10. **API facts that change the design** [D1–D9]:
    - Forced `tool_choice` (`any`/`tool`) returns HTTP 400 on Opus 5.5, Sonnet 5.5 and Fable 5.1.
    - On Haiku 5.5, forced tool choice is accepted but the response then has no thinking block.
    - Effort lives in `output_config.effort`. On the Messages API, Sonnet 5.5 defaults to `high`; in Claude Code all three 5.5 models default to medium. Set effort explicitly everywhere (per-surface defaults in D-17, corrected 15 Oct 2026).
    - Repair loops must be append-only. Editing history and then replaying thinking blocks returns 400.
    - Per-message effort (beta) can raise effort without breaking the cache.
    - Haiku's price rises 5x above 100K prompt tokens [N20][N82].
    - The minimum cacheable prefix is 512 tokens on the 5.5 family.
11. **Chinese and open models** (§8) belong in the same harness as a **hedge**, not as a cost plan.
    - Even at $0 they could save at most about $0.29 per lesson against Haiku. With review at $0, that is about 5% of the D2 total at today's floor, about 13% with clips at $0, and up to about a third at the lean floor (corrected 15 Oct 2026; the earlier "under 1%" assumed paid review; §7.14).
    - Their real value is vendor independence, data residency, and a fine-tuning path once a few hundred accepted traces exist [N78].
    - Send them curriculum content only, never student data.
12. **How to decide.** Make go/no-go decisions per archetype family, using:
    - cost per accepted lesson
    - escape rate (human-found defects that passed every verifier)
    - Wilson lower bounds, not point estimates

    An archetype that Haiku can't pass runs on Opus-low through the same Kit. The Kit, the eval set and the traces are kept either way, so none of the work is wasted.

---

## 1. Why documentation alone cannot distil Opus into Haiku, and what can

### 1.1 What the strong model is actually doing in a good run

When Opus 5.5 at max effort makes a good 79-second animation from a bare prompt [V1], it does far more than follow instructions:

- plans a scene graph over many turns
- invents layouts that fit a 9:16 safe zone
- notices its own overflow and timing bugs, then re-renders and fixes them
- keeps going until the output is coherent

That is long-horizon agentic work with self-verification and taste. A guide can describe the *outcome* of those decisions ("split the equation into three lines when it is wider than the safe zone"). It cannot give a small model the ability to *notice* the problem, *recover* from its own mistakes, or *persist*.

The evidence on Haiku 5.5 is specific:

| Behaviour | Evidence | What a longer guide does |
|---|---|---|
| Weak on long agentic tasks | Terminal-Bench 4.0: 39.2% vs 70.6% for Sonnet 5.5 [N4][N37] | Adds tokens; does not close the gap |
| Stops early at low effort | Moving low→medium roughly halved early stopping, but more than doubled output tokens [N9][N95] | Can't fix it; effort and required-field checks can |
| Says "done" without checking | [N10] (contested) | A verification paragraph helps a little [N10]; only external verifiers make it safe |
| Skips a needed tool call with JSON output and thinking off | [N13] | Use the right request shape (§2.5) |
| Reasoning leaks into user-facing text | More common with thinking off or low effort [N15] | Use adaptive thinking plus a string check on on-screen text |
| Refusals with no server-side fallback | Retrying usually refuses again [N16] | Route the scene to another model; never retry on Haiku |

The same evidence shows where Haiku is strong: **bounded tasks with tools and verifiers.**

- Tool use nearly doubles its Chartography score, from 46.4% to 86.2% [N41].
- At max effort it edges Sonnet on FrontierCode Main, 46.4% vs 46.2% [N38]. That figure is at max effort. ExamLeaf will run Haiku at medium, and medium scores much lower on some benchmarks (GDPval-AA 1277 vs 1620 [N36]).
- So the effort level is a measurement to make on ExamLeaf scenes (§3, arm C3), not a benchmark to import.

### 1.2 What the evidence says works

- **Verification plus repeated sampling.** A cheaper model with many samples beat a stronger single-shot system: 56% vs 43% on SWE-bench Lite with 250 samples [N88][N89]. Coverage grows log-linearly with samples [N90][N91]. But without automatic verifiers, majority voting and reward models plateau [N92]. **No verifier, no best-of-N.**
- **A renderer in the loop.** On ManimBench, a 30B open model (Qwen 3 Coder) with renderer-in-the-loop plus documentation reached 94% render success and 85.7% visual similarity, beating GPT-4.1 by 3 points [N67–N69]. Two caveats:
  - that model was **trained** for the task (SFT and GRPO [N70–N72])
  - an untrained model with the same loop will be well below it [Hypothesis]
- **Distillation, later.**
  - Fine-tuned small models have cut cost up to 30x [N73] and recovered about 90% of teacher accuracy at about 5x lower cost [N75], from as few as 446 demonstrations [N78].
  - They also regress out of distribution [N77].
  - This is a month-3+ option, fed by the traces this programme collects.
- **Anthropic's skill guidance** points the same way:
  - write evals before documentation and baseline without the skill [N60]
  - test the skill on every model it will run on; Haiku needs more guidance, Opus may over-explain [N58]
  - exact scripts for fragile steps [N61]; pre-made scripts over generated code [N64]
  - validator feedback loops [N62]; plan-validate-execute through a machine-checkable intermediate file [N63]
  - one default path with an escape hatch [N66]
  - SKILL.md under 500 lines [N59], references one level deep [N65]
  - distil successful approaches and common mistakes into reusable context **and code** [N30]

### 1.3 The five transfer mechanisms, ranked by how reliably they transfer to a cheap model

| # | Mechanism | What it moves from strong to cheap | Failure classes it removes | Per-video cost | ExamLeaf form |
|---|---|---|---|---|---|
| M1 | **Deterministic library: templates plus slot schemas** (a light DSL) | Layout, motion, easing, safe zones, timing and style decisions, frozen into code | Overflow and safe-zone errors (when templates own layout), non-determinism, off-token colours, cue drift, invented glyphs, misspelt on-screen terms | ~0 | HyperFrames components obeying `04_harness_contract/contract.md`, each with a `params.schema.json`; a scene spec is template ID + params + cue bindings |
| M2 | **Golden exemplars plus retrieval** | Worked examples of *this archetype in this style* | Under-specification, wrong param combinations, weak composition | Cached prefix tokens | 2 golden cards + 1 negative card per call, chosen by a lookup table |
| M3 | **Explicit rules, checklists and negative examples** | The few must/never rules that matter, each with a counter-example | Repeat mistakes the schema can't express | Cached prefix tokens | 8–15 numbered rules per archetype; every rule linked to a detector or marked human-only |
| M4 | **Verifiers, repair loops and the cascade** | The strong model's *self-checking*, turned into external code | False "done", early stop, tool skip, leakage, determinism, science-value errors | Render seconds and a few cents | V0–V8 stack (§2.3); append-only repair turns; best-of-N; escalation |
| M5 | **Strong models as offline compilers and judges** | Taste and invention, used once per archetype instead of once per scene | Novel visuals the Kit can't express (as new templates), plus calibration of the judge | Amortised | Fable and Opus author templates and verifier rules, mine traces weekly, and audit a 5% shadow sample |

### 1.4 The closure rule (the promotion ladder) [Recommendation]

Every learning, edge case or failure tag gets an owner, in this order:

1. **Template default or behaviour.** The cheap model never sees it.
2. **Schema constraint.** The cheap model cannot express the mistake.
3. **Validator rule with a fix hint.** The mistake is caught and the model is told exactly which edit to make.
4. **Exemplar,** golden or negative.
5. **Rule sentence in the skill,** only as a last resort.

A rule with no detector and no human gate is **deleted**: a rule that can't be checked is just noise to a small model.

Track every item in `EDGE_CASE_CLOSURE_MATRIX.csv`. It covers the 65 existing edge cases, the 31 negative tests [P6] and every new failure tag. Target: **at least 80% closed at rungs 1–3** before Haiku goes to production.

### 1.5 What to keep from the founder's plan and what to change

| Founder's instinct | Keep / change |
|---|---|
| Make the videos with strong models first | **Keep.** These runs provide the quality ceiling, the gold references and the failure data. |
| Record a proper timeline of each run | **Keep and make it stricter.** Log one ledger row per model call with *billed* usage fields (§3.4). [V1]'s token and dollar figures cannot be reconciled, which shows why. |
| Document everything in depth | **Change.** Documentation is a by-product. The deliverables are code, schemas, verifiers, exemplars and the eval set. Prose is the last rung of the ladder. |
| Cheap models then produce similar quality | **Reframe.** "Similar quality" is a claim about the Kit's coverage plus the verifiers, measured on a sealed holdout. It is not a property of Haiku. |
| 40–100x lower cost | **Reframe.** That holds on the LLM line against bespoke strong-model generation. Total cost falls only if review minutes fall. *(Superseded 15 Oct 2026: with review at $0, see §7.13–§7.14.)* |
| Use "Opus 5.5 Ultra" | **One capped probe only** (§3.3, arm S5). In [V1], max effort plus ultracode used at least 2.5M tokens and at least $348 and never finished. |

### 1.6 The honest ceiling

A cheap model on the Kit can only produce what the templates can express.

- Novel pedagogy (a new kind of diagram, an unusual metaphor) either escalates to a strong model or becomes a backlog item for a new template.
- Visual sameness across 1,000 lessons is a structural risk. It is mitigated by bounded variants, seeded variation and a monotony rubric item (§6), and it never disappears.
- The eval set and the Kit are the portable assets. When Haiku 5.5 is replaced, re-run the eval; don't rewrite the docs.

---

## 2. Target architecture

### 2.1 Diagram

```
 OFFLINE (weeks 1-4, then monthly)                       PER LESSON / PER REEL (gate order corrected 15 Oct 2026)
 ┌────────────────────────────────────┐   Production Kit  ┌───────────────────────────────────────────────┐
 │ Fable 5.1 / Opus 5.5 (high, capped)│  (git-versioned)  │ [GATE GA] academic approval of the script     │
 │  - author templates + slot schemas │ ───────────────▶  │   bundle + fixtures, bound to the bundle hash │
 │  - write verifier rules + messages │                   │ 1 route beat -> archetype (table + Haiku low, │
 │  - curate golden/negative cards    │                   │   strict enum, "unknown" allowed; token-only) │
 │  - mine traces weekly              │                   │ [GATE H-SB] storyboard grid + beats +         │
 │ Humans: fixtures, rubric, approvals│                   │   estimate, bound to hashes (12/05 §1)        │
 └────────────────────────────────────┘                   │ Deterministic controller (Python, no LLM);    │
                                                          │ nothing below runs before H-SB:               │
                                                          │ 2 TTS + word timings                          │
                                                          │ 3 build cue sheet from TTS word timings       │
                                                          │ 4 assemble cached prompt (BP1-BP4)            │
                                                          │ 5 token guard (<60K; never >100K on Haiku)    │
                                                          └───────────────┬───────────────────────────────┘
                                                                          ▼
                    ┌──────────────── tier 1: Haiku 5.5, effort medium, adaptive thinking,
                    │                 output_config.format = archetype slot schema, k=1 or k=3
                    ▼
     ┌───────────────────────────────────────────────────────────────────────────────┐
     │ VERIFIERS (code): V0 schema · V1 contract lint · V2 fixture/text diff ·       │
     │ V3 double + reverse-order render hash at K seek points ·                      │
     │ V4 layout/safe-zone/Indic fit · V5 cue timing (contract rule) ·               │
     │ V6 keyframe judge (Haiku vision, Sonnet audit) · V7 SSIM                      │
     └───────────┬───────────────────────────────────────────────┬───────────────────┘
          pass   │                                        fail   │ append-only repair (≤2), best-of-3
                 ▼                                               ▼
     render final ×2 + reverse-order render,    tier 1b Haiku xhigh (per-message effort)
     frame-hash check (AD-21)                    → tier 2 Sonnet 5.5 medium → tier 3 Opus 5.5 medium/high
                 │                               → human ticket + backlog item (new template/rule)
                 ▼
     full A-suite (12/10 A1–A17) + 07/06 release checks → QA report
                 ▼
     [GATE GF] academic + production, two identities, bound to the video hash
     (each Reel: its own H-SB, full A-suite and [GATE GS] on the Reel hash, §5.7)
                 ▼
     ledger.jsonl (every call, billed usage, verdicts, escapes) → weekly trace mining → Kit vN+1
```

**Gate order (corrected 15 Oct 2026, audit M4).** GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF, with GS for every Reel. Academic approval never comes after rendering. Before H-SB only token-only planning and code-rendered thumbnails may run (12/05 §1). The earlier diagram put "HUMAN GATE 1 (academic: script, fixtures, storyboard)" after the final render and had no H-SB step.

### 2.2 Who does what

| Actor | Does | Never does |
|---|---|---|
| **Fable 5.1 / Opus 5.5 (offline)** | Authors templates, slot schemas, verifier rules, error catalogue, golden and negative cards; writes ADRs from run evidence; mines escalations weekly; shadow-audits 5% of scenes | Runs per scene in steady state (except as tier 3); ultracode outside the single attended, founder-approved probe (D-9) |
| **Deterministic code** | Routing table, cue-sheet build (`validate_cue_sheet.py`), prompt assembly with cache breakpoints, token guard, V0–V5 and V7, rendering, contact sheets, cost ledger, QA report | Taste judgements |
| **Haiku 5.5 (per scene)** | Picks a template ID from at most 3 allowed for the beat; fills the slot JSON; repairs against verifier messages; writes Reel hooks and caption text within limits (once the text arms pass). That text is new script and goes to GA before use (§5.7, corrected 15 Oct 2026) | Writes free on-screen text (uses `text_ref` spans of the approved script); invents science values; sets times, colours or fonts; writes free-form animation code; declares completion |
| **Haiku 5.5 vision (V6)** | Binary rubric questions on a 6-keyframe contact sheet | Signs off science (humans do that) |
| **Sonnet 5.5** | Tier 2 escalation; script review when Haiku authors text; 10% judge audit | Runs as a default tier |
| **Humans** | Validate fixtures; approve script excerpts, thresholds and templates; GA (academic, before any synthesis); H-SB (storyboard and estimate); GF (full video); GS (each Reel); blind rating during experiments | Get replaced by any model verdict on science |

### 2.3 Templates, not a full DSL compiler [Recommendation]

The judges found the full DSL plan the strongest on edge-case closure but the heaviest to build. The synthesis keeps its **constraints** and drops the **compiler**:

- A **template** is one HyperFrames component that obeys the seek-deterministic contract (`DURATION`, pure `seek(t)`, seeded PRNG). It ships with:
  - `params.schema.json`
  - text limits per script (Latin, Devanagari, Assamese), measured with real font metrics
  - golden frame hashes at t = 0, mid and end
  - a self-test
- A **scene spec** is `{template_id, variant, variation_seed, params, cue_bindings[], fixture_ids[], text_refs[]}`. The spec is the plan-validate-execute intermediate file [N63].
- **Hard constraints that make whole error classes impossible:**
  - **No free on-screen text.** `text_ref` points to spans of the approved script, whose hash is already in the cue sheet, or to academic-approved glossary IDs.
  - **No free science glyphs.** Fixture IDs and parts must exist in the validated fixture registry.
  - **No time literals.** Steps bind to cue IDs from narration timings.
  - **No colours or sizes.** Style comes from `05_style_guides/style_tokens.json`.
  - **Bounded variety.** Each template has a few enumerated variants plus a `variation_seed`.
- **The free-code escape hatch is not used in v1.** A bounded `draw(ctx, t, params, rng)` snippet (no more than 80 lines, whitelisted API, linted, hash-checked, at most 2 per scene) is a v2 option, and only if the escalation logs show a recurring need.
- **Scope for the first six weeks:** **8 archetypes**, the top 8 by expected frequency (§3.2). More are added only when the "unknown archetype" rate exceeds 5% [Recommendation threshold].
- **Route to the existing renderers (added 15 Oct 2026, audit M12).**
  - Fixture-visual archetypes are filled as slot specs for the existing tested adapters. They are not re-implemented as HyperFrames templates. This covers archetype (3), labelled-fixture reveal, and (6), graph/plot from fixture data. The adapters are:
    - the native SVG renderer (`examleaf-svg-scenes`, the reference/regression renderer under AD-01)
    - Manim CE (`examleaf-manim-scenes`) for equation transformations and graphs whose symbols must stay in correspondence (12/07 §1)
  - Symbolic archetypes (4, 5, 7) go to the same adapters wherever an approved SVG/Manim template exists [Recommendation].
  - HyperFrames Kit templates are limited to the text-card and illustrative layers.

### 2.4 Verifier stack (cheapest first)

Every rule has:
- an ID
- a measured false-positive rate on the dev set
- an error message written for a small model: field path, expected, got, and the one edit to make

| ID | Check | Implementation | Blocks? |
|---|---|---|---|
| V0 | Slot JSON validates; required completion fields present (this catches early stops) | Structured outputs plus a semantic validator: array lengths, cue IDs exist, `text_ref`s resolve to the approved script hash, density limits | Yes |
| V1 | Seek-contract lint: no `Date`, no unseeded `Math.random`, no timers or network; tokens only | Existing `lint_seek_contract.js` [P5] | Yes |
| V2 | Fixture and text diff: every science value and label comes from a fixture or approved text; DOM text sampled at t is diffed against them; on-screen strings must be a subset of brief strings (catches leaked reasoning [N15]) | **Existing:** `12_advanced_animations_with_claude/03_skills/examleaf-anim-qa/scripts/text_fixture_diff.py` (A7; passes selftest). Extend it for the slot-fill path (strings ⊂ brief); do not rewrite it (corrected 15 Oct 2026; was "New") | Yes, and must be total: no science escapes ever |
| V3 | Double render plus a **reverse-order render** at K seek points with frame-hash equality (AD-21; A3); full double + reverse-order render once on the final scene (reverse order added 15 Oct 2026) | Existing `determinism_hash_check.py` [P5] | Yes |
| V4 | Layout QA from DOM boxes at sampled t: safe zone (`vertical_safe_zones.tokens.json`), overflow, overlap, minimum font size, contrast, Indic shaping and fit per script | **Existing:** `examleaf-anim-qa/scripts/safe_zone_check.py` (A4/A5/A14; passes selftest), plus A13 contrast (`examleaf-visual-qa`) and A8 Indic shaping (`examleaf-kinetic-typography`). Extend these; do not rewrite them (corrected 15 Oct 2026; was "New") | Yes |
| V5 | Timing uses the **contract rule** (`04_harness_contract/contract.md` §8; 12/10 A10). Each reveal lands on its word's t0 or up to 0.05 s before it (± 1 frame). A late reveal (`at > word.t0`) **fails**; a reveal more than 0.10 s early warns. Scene length equals audio length ± 1 frame. The ±150 ms band is kept only as an alignment-quality metric [Hypothesis, to calibrate], never as the pass rule (corrected 15 Oct 2026) | Existing reveal-sync check (`safe_zone_check.py --cues`) and the harness cue-sheet validator; extend these | Yes |
| V6 | Keyframe judge: Haiku vision answers binary rubric questions on a 6-frame contact sheet; Sonnet audits 10% of scenes plus every disagreement | New, calibrated in week 3 | Flags; blocks only for calibrated questions |
| V7 | SSIM regression against the archetype's golden frames (detects template drift) | New | Flags |
| V8 | Human gates in order: GA (before synthesis), H-SB (before TTS, paid assets and scene code), GF on the full video, GS on every Reel; plus the QA report with flagged timestamps (corrected 15 Oct 2026) | Existing process (07/06; 12/05; 12/10 §3) | Yes |

**Must-reject set:** all 31 existing negative tests [P6], plus every negative card. Every verifier release must reject 31 of 31.

**Relation to the existing gates (added 15 Oct 2026, audit M12).** V0–V8 are the Kit's inner-loop checks. They run **in addition to** the animation A-suite (A1–A17 in `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`) and the release checks in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`. They never replace them. Before GF or GS, Kit output must also pass:
- **Answer-hidden window:** no answer is revealed during a prediction or think pause (RD-11; A5 prediction-prompt hold; A10 rule 1).
- **Flash and luminance:** A6, using `examleaf-anim-qa/scripts/flash_check.py`.
- **Licences:** asset provenance and licence (A16).
- **Loudness:** loudness and peak, re-measured after mux (A9).
- **Captions:** caption fidelity and reveal sync (A10).
- **The rest of the suite:**
  - science re-check at every semantic event (A12)
  - contrast and phone readability (A13)
  - camera-fx guard (A14)
  - non-empty frames (A15)
  - media probe (A11)
  - ledger completeness (A17)

A verifier pass never substitutes for any of these. No LLM verdict (V6) can waive one.

*Addendum (15 Oct 2026).* Owners in Content Engine v2: V0, V6, V7 → `examleaf-kit-verify`; V1, V3 → `examleaf-motion-harness`; V2, V4, V5 → `examleaf-anim-qa` (`15_content_engine_v2/subsystems/SKILLS_and_KIT_MAP_v2.md` §3).

### 2.5 API settings that matter (corrections to earlier drafts)

**One rule above all: in the slot-fill path there are no tools to skip.** The cheap model returns the scene spec through `output_config.format` (a JSON schema), with adaptive thinking on. Forced `tool_choice` is not used anywhere in production.

| Setting | Fable 5.1 / Opus 5.5 / Sonnet 5.5 | Haiku 5.5 |
|---|---|---|
| Forced `tool_choice` (`any`/`tool`) | **Returns HTTP 400** [D1]. Where a tool is genuinely needed, use `tool_choice: auto` with one strict tool and a prompt sentence naming it; or use `output_config.format` with thinking on. Treat a missing call as F-TOOLSKIP and retry with an appended instruction. | Accepted, but the response then starts with the tool call and has **no thinking block** [D2]. That is thinking-off in practice, which brings back the risks in [N13] and [N15]. **Week-1 A/B:** "forced tool, no thinking" vs "auto + strict + adaptive thinking". Log `has_thinking_block` on every call. |
| Effort | `output_config.effort` (not a top-level field) [D3]. Opus 5.5 defaults to medium; **Sonnet 5.5 defaults to high on the Messages API (medium in Claude Code; D-17): set medium explicitly** for tier 2 [D3]. | Defaults to medium [D3][N93]. Start at medium; choose the production level from the C3 sweep (low, medium, high, xhigh) by cost per accepted scene, not by benchmarks run at max effort. |
| Raising effort for a retry | Per-message effort (beta `mid-conversation-output-config-2026-07-01`) changes effort without resetting the cache [D4]. Changing the *top-level* effort invalidates the messages cache [N14]. | Same beta; requires thinking on [D4]. This is how the "Haiku xhigh" rung works. |
| Thinking | Opus 5.5 can't disable thinking [D7]. On Sonnet 5.5, thinking off is only possible via `between_tools` [D7]. | Adaptive is on by default; keep it on. |
| Repair loops | **Append-only.** Replaying thinking blocks after editing `system`, `tools` or earlier messages returns 400 (enforced for accounts created on or after 2026-08-31) [D5]. Validator feedback goes in a *new* user turn; earlier turns are never edited. | Same [D5]. |
| Caching | Minimum cacheable prefix is **512 tokens** on the 5.5 family and Fable 5.1 [D6]. The 4,096 figure in [N54] is for Opus 4.6/4.5 and doesn't apply. At most 4 breakpoints [N56]; lookback of 20 blocks [N55]. Caches are model-scoped, so an escalation pays its own cache write. | Same. Watch the 100K tier: cached tokens count toward the prompt size [N20]. |
| Strict schema limits | Per request: at most 20 strict tools [N44], 24 optional parameters [N45], 16 `anyOf`/type-array parameters [N46], `minItems` of 0 or 1 only [N48], 180 s compile timeout [N47]. Use `output_config.format`, not the deprecated `output_format` [N49]. These are **per-request** limits, not a cap on library size: each call sees one archetype schema. | Same. Compiled grammars stay cached for 24 h [N43], so keep schemas stable. |
| Refusals | Server-side `fallbacks` (beta) are available on Opus 5.5, Sonnet 5.5 and Fable 5.1, but not on the Batches API [D9]. | No server-side fallback [N16][D9]. The controller routes the scene to tier 2 without retrying on Haiku. |
| Data retention | Fable 5.1 requires 30-day retention, so it is not available under zero data retention [D10]. Only curriculum content goes to Fable. | — |

---

## 3. The experiment programme with Fable 5.1 and Opus 5.5

The full runbook is in the protocol document. This section explains the design.

### 3.1 What the programme must produce

The programme must produce four things:

- **(a) gold references** with human ratings
- **(b) labelled failures**, from cheap models on real ExamLeaf scenes
- **(c) the measured cost–quality frontier** for each model × effort × prompt tier × harness combination
- **(d) the Kit itself**

Don't run it to "make great videos with Opus". The point is to manufacture the evidence and the assets that let a cheap model be trusted.

### 3.2 Fixed scene set: 54 scene packages, frozen before any run

There are **8 archetypes**, grouped into 3 families:

| Family | Archetypes |
|---|---|
| Text-card | (1) hook/title card, (2) definition/key-term card, (8) recap or quiz pause-and-reveal |
| Symbolic | (4) formula derivation step-reveal, (5) worked numerical, (7) chemical equation balancing |
| Fixture-visual | (3) labelled-fixture reveal (e.g. heart, eye, ray diagram, circuit), (6) graph/plot build from fixture data |

*Routing note (15 Oct 2026):* fixture-visual archetypes are filled for the existing SVG/Manim adapters, not built as new HyperFrames templates (§2.3).

For each archetype:

- **Dev set:** 3 scenes (24 in total). These are visible to Kit authors, and the golden exemplars come from here.
- **Sealed holdout:** 3 scenes (24 in total). These are never shown to anyone writing templates, skills or exemplars.
- **Spread:** Physics, Chemistry, Biology and Maths; all 5 style guides; English, Hinglish and Hindi on-screen text.

**Adversarial set (6 scenes):**
1. An Assamese/Devanagari conjunct-heavy title.
2. A long chemical equation that overflows the 9:16 safe zone.
3. A brief that needs a diagram with no validated fixture. The correct output is to escalate.
4. A dense cue burst (more than 3 cues per second).
5. A 60 s Reel compression of a 4-step process.
6. A chemistry or biology brief likely to trigger a false-positive refusal.

**Integration set:**
- the Ohm's-law 600 s blueprint (`02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md`)
- the three pilot lessons (`07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md`)
- 6 Reels from `01_business_model/REEL_BACKLOG_36.md`

**Setup cost (often forgotten).** Each package needs an academic-approved script excerpt, TTS narration, word timings, a real cue sheet and validated fixtures.
- TTS cost is negligible: about $0.03 per 20 s scene at the project's $0.10 per 1,000 characters [P1].
- Academic approval is about 10 minutes per package, so about 9 hours in total.
- Engineering is about 0.5 hours per package, so about 27 hours [Hypothesis].

### 3.3 The run matrix (model × effort × prompt tier × harness)

| Arm | Model / effort | Prompt tier | Harness | Scenes × samples | Purpose |
|---|---|---|---|---|---|
| S0 / S1 / S2 | Opus 5.5 low / medium / high | Brief + contract + style guide | Agentic, free-form code (Agent SDK) | Dev 24 × 1 each | Bespoke frontier; harvest techniques |
| S3 | Fable 5.1 high | Same | Agentic, free-form | 8 hardest × 1 | Ceiling where Opus struggles |
| S4 | Opus 5.5 max | Same | Agentic, free-form | 8 hardest × 1 | Ceiling; template ideas |
| S5 | "Opus 5.5 Ultra" probe: Opus 5.5 max + ultracode | Same | Agentic | 1 hardest × 1, **$50 provider-side spend limit**; logged as `capped` if unfinished. It is an **attended, founder-approved exception** (D-9): it runs in an isolated experiment sandbox outside the production governor, on a dedicated key, with a human present throughout (corrected 15 Oct 2026) | Answers the founder's question with one data point instead of an open-ended spend. No result can enable ultracode in production |
| B | Fable 5.1 high (design, critique); Opus 5.5 high (build) | S-arm outputs, ratings, failures | Offline authoring | 8 archetypes | Templates, schemas, verifiers, cards; re-express the gold scenes as specs and re-render them (compiled-gold check) |
| P-low / P-med | Opus 5.5 low / medium | **Kit** (slot-fill) | Single call + verifiers | Dev 24 × 1 each | Anthropic's "most capable model at lower effort" baseline; the fair comparison |
| C0 | Haiku 5.5 medium | Brief + contract only (bare) | Agentic, free-form | Dev 24 × 3 | The "crappy" floor [N60] |
| C1-trim | Haiku 5.5 medium | Trimmed docs (under 60K) | Agentic, free-form | Dev 24 × 3 | Do docs help at all? |
| C1-full | Haiku 5.5 medium | **The full section-12 manual**, accepting the over-100K price tier and logging it | Agentic, free-form | Dev 24 × 3 | Tests the founder's "big manual" hypothesis as stated |
| C2 | Haiku 5.5 medium | Scene pack: skeleton, rules, 2 golden + 1 negative card | Agentic, writes code from skeleton | Dev 24 × 3 | Marginal value of exemplars without templates |
| C3 | Haiku 5.5 **low / medium / high / xhigh**; k = 1 and k = 3 | **Kit** slot-fill + verifier loop | Controller | Dev 24 × 5 per effort | Main result; selects the production effort by cost per accepted scene |
| C4 | Haiku 5.5 at the selected effort | Kit | Full cascade | **Sealed holdout 24 × 5** + adversarial 6 × 5 | The go/no-go evidence |
| C5 | Sonnet 5.5 medium (set explicitly) | Kit | Controller | Dev 24 × 3 | Calibrates tier 2 |
| O1 / O2 | One hosted Chinese API model; one self-hosted open-weights model | Kit (same schema; JSON mode if no strict schema support) | Controller | Dev 24 × 3 | Portability and hedge (§8) |
| T0 | Today's mix (Sonnet author + Opus review) vs Haiku author + Sonnet review vs Haiku alone | Super Teacher section-script skill | Single calls | 6 English sections × 3 arms | Can text move to Haiku? |
| T1 | Same 3 arms | Hinglish and Hindi register; Assamese captions | Single calls | 6 Hinglish + 6 Hindi sections; 4 Assamese caption sets × 2 arms | Language parity |
| T2 | Haiku low vs Sonnet medium | Beat segmentation + archetype routing | Strict enum | 3 lesson scripts, against academic gold labels | Routing accuracy |
| T3 | Same 3 arms as T0 | Reel hooks and captions | Single calls | 12 hooks × 3 arms | Hook quality |
| T4 | Haiku | On-screen caption fit per script | Code-checked | All T1 outputs | Fit by font metrics |
| I | Cascade (2 runs) + Opus-Kit shadow (run 1 only) | Kit | Full pipeline + every human gate (GA, H-SB, GF; GS per Reel; corrected 15 Oct 2026) | 4 lessons + 6 Reels | Cost per accepted lesson; **review minutes** |

**Guards for the agentic Haiku arms (C0–C2)** [Recommendation]. The Agent SDK adds its own system and tool prompt, and context grows every turn. The wrapper therefore:
- logs prompt tokens per turn
- warns at 60K
- triggers server-side compaction (beta `compact-2026-01-12`) or ends the run at 80K
- hard-stops at 100K

C1-full is the one exception: it is allowed past 100K, and every turn above 100K is priced at the higher tier ($0.50/$2.50 [N82]) and tagged `TIER_100K`.

**Hard caps on the strong arms:**

| Arm | Cap per scene |
|---|---|
| Opus max | $15 |
| Fable high | $15 |
| Opus high | $8 |
| Ultra probe (S5) | $50 total, as a provider-side spend limit on a dedicated key (D-9) |

Advisory task budgets (beta) are also set where supported [D12]. The run wrapper kills runs at the cap from billed usage, and a capped run is logged as a failure. It never gets an extended budget. For S5, the hard stop is the provider-side limit and the wrapper meter is only a second line, because prompt-level budgets are not hard limits (12 AD-20) (added 15 Oct 2026).

### 3.4 What the timeline captures

One ledger row per model call and one per work unit go to `experiments/ledger/*.jsonl`. The full schema is in the templates document. The essentials:

- **Identity:** run, arm, scene, archetype, model ID, effort, thinking mode, `has_thinking_block`, Kit version and git SHA, prompt-prefix hash, exemplar IDs.
- **Billed usage, split into four fields:** `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, `output_tokens`. The ledger computes dollars from the price table and never estimates them.
  - [V1] is the cautionary example. $3 for 78K tokens is about $38 per million, and $49 for 625K is about $78 per million. Both are above Opus 5.5's $20 per million output price. So [V1]'s token counts can't include every billed token.
- **Time:** wall seconds, time to first token, render seconds.
- **Loop:** attempt number, repair turn, best-of-N index, verifier results per rule (pass/fail, rule ID, field path), escalation source.
- **Outcome:** `stop_reason` (refusals recorded separately with category [N16]); final status (`pass`, `escalated`, `abandoned`, `capped`); the verifier's own exit code, never the model's claim [N10].
- **Failure tags** (fixed taxonomy): F-SYNC, F-OVERFLOW, F-SAFEZONE, F-SCIENCE, F-NONDET, F-EARLYSTOP, F-FALSEDONE, F-LEAK, F-TOOLSKIP, F-REFUSAL, F-STYLE, F-DENSITY, F-MONOTONY, F-INDIC, F-TIER100K, F-CAPPED.
- **Outputs:** spec hash, code hash, render hashes (two), keyframe paths.
- **Human:** blind rubric scores from 2 raters, defects, reviewer minutes.
- **Decisions** (strong arms only): a closing `DECISIONS` block of 3–7 choices a weaker model could get wrong, each with the rule it implies.

### 3.5 Mining traces into rules

The weekly procedure (protocol §6) runs as a pipeline:

1. **Cluster** failures by tag and rule ID.
2. **Ask the strong model** "which template default, schema constraint or validator would have prevented this?". Do not ask for a longer prompt [N30].
3. **Apply the closure rule** (§1.4).
4. **Write a negative card** from the real failure, never a synthetic one.
5. **Re-run** the dev suite and the 31 negative tests.
6. **Record an ADR** that cites the run IDs.

Any human-found defect that passed V0–V7 is an **escape**. Each escape must end in a new rule or a documented acceptance.

---

## 4. Artefacts to produce from the experiments

Everything lives in `12_advanced_animations_with_claude/08_production_kit/`. It is versioned, hash-referenced by the prompt assembler, and every item is tied to ledger run IDs. The fill-in templates are in the templates document. The required sections are:

### 4.1 Guide: one skill per archetype (`skills/examleaf-fill-<archetype>/SKILL.md`)

- **Frontmatter:** `name`, `description` [N23]. Only these preload [N24].
- **Body:** under 500 lines [N59], references one level deep [N65], rarely used paths split into separate files [N28].
- **Sections, in order:**
  1. When to use / when not
  2. The single default path plus one escape hatch [N66]
  3. Slot table (field, type, enum, default, meaning)
  4. 8–15 numbered MUST/NEVER rules, each with a detector ID
  5. Pre-submit checklist (at most 10 yes/no items)
  6. How to read validator errors
  7. The verification paragraph: "You are not done until the validator returns 0; do not claim completion" [N10]
  8. Escalation triggers ("say UNKNOWN_ARCHETYPE")
  9. Links to golden/negative card IDs
  10. At least 3 evals [N60]
- **Testing:** the skill is tested on Haiku, Sonnet and Opus [N58].

### 4.2 Restrictions (`RESTRICTIONS.md` + `restrictions.json`)

- Each restriction has:
  - an ID
  - a statement
  - the enforcement point (schema, lint rule, verifier ID, or `HUMAN-ONLY`)
  - the negative test that proves it
  - severity
- **Hard forbids:**
  - free on-screen text, free glyphs, time literals
  - `Math.random`, `Date`, timers, network, CSS keyframes that can't be seeked
  - colours and fonts outside the tokens
  - editing the approved script
  - generated video clips unless a ticket justifies them
- A restriction with no enforcement is labelled `advisory` and reviewed for promotion to a check.

### 4.3 Edge-case register (extends `02_documentation/12_EDGE_CASES_master_table.md`)

Columns:
- ID
- trigger
- symptom
- detector (V-rule or `HUMAN-ONLY`)
- closure rung (1–5)
- artefact path
- regression test
- first-seen run ID
- frequency (n/attempts) by model and effort
- cheap-tier handling (`handle` / `escalate` / `refuse`)
- status

### 4.4 Learnings ledger and ADRs (extends `14_DECISIONS_and_OPEN_QUESTIONS.md`)

Dated entries:
- claim
- evidence (run IDs, n, effect)
- alternatives rejected
- promoted to (template / schema / validator / exemplar / prose)
- revisit trigger
- status (`adopted` / `rejected` / `watch`)

### 4.5 Exemplar bank (`exemplars/golden/<archetype>/`, `exemplars/negative/<rule_id>/`)

**Golden card:**
- provenance (arm, model, effort, cost, Kit hash)
- input brief
- slot JSON
- render keyframes
- a condensed trace of at most 150 words
- the DECISIONS block
- a fixed-vs-varies slot map
- the verifier report
- two human rubric sheets, both ≥ 4 on accuracy and legibility

**Negative card:**
- the real failing output
- the violated rule
- the exact detector message
- the minimal corrective diff
- the observed frequency

**Retrieval rule:** at most 2 golden + 1 negative per call, chosen by lookup table, never the whole bank.

### 4.6 Scene templates (`templates/<template_id>/`)

- `component.js` (contract-compliant)
- `params.schema.json` (within the strict-schema limits)
- `TEMPLATE.md`: when to use / when not; parameters; cue behaviour; layout and safe-zone behaviour; text limits per script; variants; known failure modes
- 2 exemplar specs
- golden hashes
- a self-test

### 4.7 Verifier suite (`verify/` + `VERIFIER_SPEC.md` + `ERROR_CODES.md`)

Per rule:
- property
- threshold
- implementation path
- false-positive and false-negative rates on the dev and negative sets
- message template (field path, expected, got, one fix)
- owner

### 4.8 Capability ledger (`CAPABILITY_LEDGER.csv`)

One row per task × archetype, recording which tier is approved:
- task
- archetype/family
- approved tier and effort
- k
- attempt cap
- escalation rule
- holdout result with Wilson lower bound
- escape rate
- cost per accepted unit
- date
- evidence run IDs
- next review

This is the document that answers "which task needs which model".

### 4.9 Supporting documents

- **Model profile** per model (`model_profiles/<model>.md`): pinned ID, effort, thinking, request shape, measured token factor against Opus on ExamLeaf prompts, quirks, pass rates.
- **Eval spec:** the sets, rubric, thresholds, and how to re-run.

---

## 5. Cheap-model operating procedure

### 5.1 Prompt layout (cache-first, most stable content first)

| Breakpoint | Content | Size [Hypothesis] |
|---|---|---|
| BP1 | Role; contract digest; global restrictions (severity high only); output protocol; verification paragraph | ~6K |
| BP2 | Style pack: tokens and do/don't pairs for one of the 5 styles | ~3K |
| BP3 | Archetype pack: slot schema summary, rules, checklist, 2 golden + 1 negative card | ~6K |
| Tail (uncached) | Beat text span IDs, cue-sheet excerpt, fixture IDs, language, prior validator messages | ~3K |

- **Total target:** about 18K per call. The assembler hard-fails above 60K, which keeps every call far below Haiku's 100K price step [N20][N82]. Treat the 1M window [N6] as a trap for this workload.
- **Queue order:** sort scene queues by archetype × style so consecutive calls share BP2/BP3 within the 5-minute TTL, which refreshes free on each use [N50].
- **Batch jobs:** use the 1-hour TTL. The write costs 2x but pays back after two reads [N22][N51]. It stacks with the 50% batch discount [N21].
- **Cache-hit check:** watch `cache_read_input_tokens`. If it is zero on repeated prefixes, a silent invalidator is present.

### 5.2 Request shape (tier 1)

- **Model and thinking:** `model: claude-haiku-5-5`, `thinking: {type: adaptive}`.
- **Effort:** `output_config.effort` set to the C3-selected level (start at medium).
- **Output schema:** `output_config.format` set to the archetype schema.
- **Tools:** none.
- **Token limit:** `max_tokens` around 16K (don't set it low; truncation costs a retry).
- **Fallback:** if the week-1 A/B shows that structured outputs plus adaptive thinking under-performs, the alternative is `tool_choice: auto` with one strict tool and a prompt instruction naming it. A missing call is tagged F-TOOLSKIP and retried with an appended instruction.

### 5.3 Per-scene procedure

1. **Route (code).** The beat maps to up to 3 allowed archetypes. Haiku at low effort picks from a strict enum that includes `UNKNOWN`. `UNKNOWN` goes to tier 3, and the case is logged as library backlog.
2. **Plan (Haiku).** Haiku emits the slot JSON. V0 runs immediately.
3. **Execute (code).** The template compiles the scene. V1–V5 run at K seek points. Rendering is seek-deterministic, so verification renders sampled frames, not the full video.
4. **Repair.** Up to **2** append-only repair turns, each containing only the failing rule messages plus that rule's 2-line negative example.
5. **Best-of-N.** Applies to archetypes whose measured first-pass rate is below 70% [Recommendation threshold], or after the repairs are exhausted.
   - Draw k = 3 fresh samples in parallel. Keep those that pass V0–V5, and rank them by V6.
   - Never sample without a verifier [N92].
6. **Tier 1b.** Haiku at xhigh via a per-message effort message [D4]: one attempt, and only on archetypes where the capability ledger shows that this rung pays off.
7. **Tier 2.** Sonnet 5.5 at medium (set explicitly), given the failure dossier (rule IDs, last diff, Haiku attempts). Up to 2 attempts. Server-side `fallbacks` are allowed on real-time calls [D9].
8. **Tier 3.** Opus 5.5 at medium, raised to high for the second attempt. Up to 2 attempts.
9. **Human ticket.** The failure dossier is logged as a candidate failure-catalogue entry.

### 5.4 Escalation triggers (any one is enough)

- Attempt caps exhausted.
- `stop_reason: refusal` on Haiku: route to tier 2 immediately, with no retry [N16].
- `UNKNOWN` archetype.
- A V2 failure that persists after one repair (a science-value mismatch is treated as a template or fixture problem, not something to sample around).
- A per-scene spend ceiling reached: $0.02 at tier 1, $0.25 at tier 2, $0.60 at tier 3 [Recommendation].

### 5.5 Per-lesson steps (gate order corrected 15 Oct 2026, audit M4)

1. **GA.** The approved outline, the script bundle and the fixtures go through academic approval, bound to the bundle hash. Nothing is synthesised before this.
2. **Routing (token-only).** Beats are routed to archetypes (§5.3 step 1). `examleaf-anim-storyboard-gate` builds the grid, beats and estimate from code-rendered thumbnails.
3. **H-SB storyboard gate.** The founder (cost) and the academic lead (fit with the approved script) approve visuals, scope and estimate. The approval is bound to hashes (12/05 §1). No TTS, paid asset or scene-code job runs before it.
4. TTS runs, then word timings, then the cue sheet.
5. Scenes go through the cascade (§5.3) and V0–V7.
6. The lesson is assembled. V3 runs on the full render (two renders plus a reverse-order render, with a hash comparison). V6 runs on transitions.
7. **A-suite.** The full 12/10 A1–A17 suite and the 07/06 checks run (§2.4).
8. The QA report is produced: auto-fixed failures, escalations, low-confidence timestamps, the spec diff against the outline.
9. **GF** (full video). Academic and production approvals come from different identities and are bound to the video hash. Each Reel then follows §5.7 and **GS**.
10. Everything is logged to the ledger.

In one line: GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF, with GS for every Reel. Academic approval never comes after rendering. *(The earlier list ran gate 1 → TTS with no H-SB step.)*

### 5.6 Text tasks

- **Until T0–T3 pass,** text stays on today's mix (Sonnet authors, Opus reviews, Haiku routes).
- **Once a text task passes** its arm, Haiku authors and Sonnet reviews. Section scripts are generated as separate calls, each well under 100K, never as one 120K call.
- **On-screen text** in scenes is never generated: it is a `text_ref` into the approved script.

### 5.7 Reels (corrected 15 Oct 2026, audit M3)

[Recommendation] Derive Reels from the approved lesson's cue sheet with a deterministic cut-down. **A Reel never inherits approval.** Each Reel is a new hashed artefact (07/05 principle 5; 12/10 §7):

- **New wording is new script.** Any LLM-drafted hook, shortened payoff, caption line or CTA is new script. It follows S5 rules, goes through the narration sub-pipeline if spoken, and goes to **GA** before use (07/05 SH4).
- **Storyboard gate.** Every Reel gets its own H-SB grid and estimate (12 AD-12).
- **Full A-suite** on the Reel: 12/10 A1–A17 plus V0–V8.
- **GS.** Academic and production approvals come from two different identities and are bound to the Reel's hash.
- **What a deterministic cut-down may shorten.** If the Reel reuses only approved segments, the approved claim IDs carry over. Reviewers then check the retained conditions, the cut points and the new hook/caption text instead of re-checking every claim. That shortens review. It removes no gate.

The ≈$0.03 LLM figure in §7.5 stands. Review time is not zero.

*(Earlier text said the Reel "inherits the lesson's science approval and keeps one short human check". That contradicted 07/05 and 12 AD-12 and is withdrawn.)*

### 5.8 Caps summary [Recommendation]

| Tier | Attempts | k | Effort | Ceiling per scene |
|---|---|---|---|---|
| 1 Haiku | 1 + 2 repairs | 1, or 3 on hard archetypes | C3-selected (start medium) | $0.02 |
| 1b Haiku | 1 | 1 | xhigh (per-message) | included above |
| 2 Sonnet 5.5 | 2 | 1 | medium (explicit) | $0.25 |
| 3 Opus 5.5 | 2 | 1 | medium, then high | $0.60 |

**Lesson-level circuit breaker:** if more than 20% of a lesson's scenes escalate past tier 1, stop. Run the remaining scenes on Opus-low via the Kit and open a Kit defect.

**Governance scope (added 15 Oct 2026).** These caps are the proposed `kit_cascade` task family (D-16). They do not run under AD-02/AD-11/AD-24, which govern the strong-model phase. No cheap-model Kit run starts until that family exists in `examleaf-effort-governor/scripts/effort_policy.py`, which the section-12 owner changes. Until then the governor refuses this cascade.

---

## 6. Evals and the parity definition

### 6.1 Rubric (1–5, two blind raters; science is a 0/1 gate)

| Item | Scale |
|---|---|
| Scientific correctness | 0/1 gate: any error fails the scene |
| Narration sync | 1–5 |
| Legibility on a phone | 1–5 |
| Pedagogical clarity (the Super Teacher beat is served) | 1–5 |
| Motion quality | 1–5 |
| Style adherence | 1–5 |
| Variety / monotony | Rated across a lesson |

Raters see anonymised outputs in random order (protocol §5).

### 6.2 Judge calibration

- The V6 judge asks binary questions only, for example: "Is the highlighted term the one being spoken?", "Is any element unreadable at phone size?".
- In week 3, its answers are compared against human labels on the dev set. **Drop any question whose agreement is below 80%** [Recommendation].
- Sonnet audits 10% of scenes plus every disagreement between the judge and the verifiers.
- **Week-1 check:** confirm Haiku 5.5's image input works at contact-sheet resolution. If it doesn't, V6 runs on Sonnet.
- A judge never signs off on science.

### 6.3 Hard gates

| Gate | Requirement |
|---|---|
| Determinism | 100% double-render frame-hash match |
| Fixture/text diff (V2) | Total: zero science-value escapes, ever |
| Negative tests | 31 of 31 rejected |

### 6.4 Statistics that mean something [Recommendation]

- **Unit of analysis.** The scene is the unit; the 5 samples of one scene are correlated.
- **Wilson intervals.** Report a Wilson 95% interval and require the **lower bound** to clear each threshold.
- **What 24 holdout scenes can show:**
  - 24/24 scenes gives a lower bound of 0.86.
  - 22/24 gives 0.74.
  - At the sample level, 115/120 gives 0.906.
- **Families.** Family-level decisions on 9 or 6 holdout scenes are **provisional** (8/9 has a lower bound of only 0.57). They are confirmed in production by sequential monitoring:
  - an archetype is "confirmed" once its running Wilson lower bound on final pass is ≥ 0.87 at n ≥ 40 production scenes (39/40)
  - until then it keeps a 20% Opus-Kit shadow instead of 5%
- **Option.** If the team wants firm per-archetype decisions at launch, expand the holdout to 5 scenes per archetype (40) in month 2.

### 6.5 Go thresholds for production Haiku

Measured on C4: sealed holdout, cascade, selected effort. All values are [Recommendation], for the academic team to ratify before the data arrives.

| Metric | Threshold |
|---|---|
| Sample-level final pass (V0–V5 within caps, before escalation) | Wilson LB ≥ 0.90 (≥ 115/120) |
| Scene-level: scenes passing in ≥ 4 of 5 samples | ≥ 22/24 |
| Science escapes reaching humans | 0 |
| Rubric difference vs the Opus-Kit reference on the same holdout | Lower 95% bound of the paired difference ≥ −0.3 on every 1–5 item |
| Blind pairwise, Haiku-cascade win or tie vs Opus-Kit | ≥ 50% point estimate on correctness and sync; reported with its interval |
| Escalation rate past tier 1 | ≤ 15% (point estimate); above this the cascade costs more than Opus-low on the Kit |
| Holdout pass vs dev pass | Within 5 points; otherwise the Kit is overfitted |
| Pilot human review minutes | Not above the 85-minute baseline |

### 6.6 When Haiku is "good enough"

An archetype is promoted to "Haiku tier" in the capability ledger when **all** of the following hold:

1. Its family passes §6.5.
2. Its escape rate in the pilot is ≤ 0.5 defects per lesson.
3. Its cost per accepted scene, *including escalations*, is below Opus-low on the Kit.

Otherwise the archetype stays on Opus-low (or Sonnet) on the Kit. That is a cost decision, not a failure.

### 6.7 Drift control

- **Weekly shadow:** 5% of production scenes are re-run on Opus via the Kit and compared pairwise.
- **Kit edits:** any Kit edit triggers the dev suite plus the 31 negative tests.
- **Model changes:** any pinned model change, open models included, triggers the full holdout plus 24 human spot-ratings.
- **Automation bias:** seed one known defect per 10 lessons and track the reviewer catch rate.

---

## 7. Cost model (explicit arithmetic)

### 7.1 Prices used (per million tokens)

| Model | Input | Output | Cache read | 5-min write | 1-h write |
|---|---|---|---|---|---|
| Fable 5.1 [N17] | $10 | $50 | $0.25 | $12.50 | $20 |
| Opus 5.5 [N18] | $4 | $20 | $0.20 | $5 | $8 |
| Sonnet 5.5 [N19] | $2 | $10 | $0.20 (see note) | $2.50 | $4 |
| Haiku 5.5, prompt ≤ 100K [N20] | $0.10 | $0.50 | $0.01 | $0.125 | $0.20 |
| Haiku 5.5, prompt > 100K [N82] | $0.50 | $2.50 | — | — | — |

- **Batch:** −50% on input and output [N21].
- **Sonnet cache-read conflict:** the supplied price block and the bundled API reference [D11] say $0.20. The pricing-page row [N19] and a news report of a price cut [N84] say $0.10. I use the conservative $0.20. The difference is under $0.01 per lesson for the cascade (≈54K cached Sonnet tokens). It is ≈$0.07 for Sonnet-only C (30 × 1.5 × 15K = 675K cached tokens) (corrected 15 Oct 2026).
- **Tokenizer:** no Haiku-only inflation factor is applied.
  - [N2] and [N42] compare Haiku 5.5 with **Haiku 4.5**.
  - Opus 5.5 already uses the newer tokenizer family introduced with Opus 4.7 [D8].
  - The cross-model factor is measured in week 1 with `count_tokens` on identical ExamLeaf prompts (English, Hinglish, Hindi, Assamese) for both models, then applied to both.

### 7.2 Workload assumptions [Hypothesis; replaced in weeks 1–4 by ledger data]

- **Scenes:** 30 per 10-minute lesson (about 20 s each); 4 per 30 s Reel.
- **Kit call:** 15K cached prefix + 3K fresh input + 3K output (including thinking). The same for every model.
  - Sensitivity: suppose Haiku's output doubles at medium [N9]. The Haiku per-call cost then rises 1.77x ($0.00345 vs $0.00195). The D2 lesson ratio falls from 19.4x to 13.9x (≈1.4x), and the scene-line ratio from 15.2x to 10.2x (≈1.5x) (corrected 15 Oct 2026; earlier text said 1.8x and 1.6x).
- **Calls per scene:** Fable 1.2, Opus 1.3, Sonnet 1.5, Haiku 2.6. Haiku's figure is 2.0 attempts plus best-of-3 on 30% of scenes (0.6 extra calls).
- **Cache writes:** 8 archetype prefixes × 15K = 120K tokens per lesson, counted once per lesson. This is conservative, because archetype-sorted queues across lessons amortise it further.
- **Text** (project v2 workload): 200K input / 38K output per lesson, with a 1.3 regeneration factor. Reel standalone text: 40K / 7.6K.
- **Judges (V6):** 39 judged candidates × $0.00065 on Haiku (5K in, 0.3K out), plus Sonnet audits of 3 scenes × $0.015 (5K in, 0.5K out), giving **$0.070 per lesson**. Applied to every Kit scenario.

### 7.3 Cost per Kit call

| Model | Cache read | Fresh input | Output | **Per call** | vs Haiku |
|---|---|---|---|---|---|
| Fable 5.1 | 15K × 0.25 = $0.00375 | 3K × 10 = $0.0300 | 3K × 50 = $0.1500 | **$0.18375** | 94x |
| Opus 5.5 | 15K × 0.20 = $0.0030 | 3K × 4 = $0.0120 | 3K × 20 = $0.0600 | **$0.0750** | 38x |
| Sonnet 5.5 | 15K × 0.20 = $0.0030 | 3K × 2 = $0.0060 | 3K × 10 = $0.0300 | **$0.0390** | 20x |
| Haiku 5.5 | 15K × 0.01 = $0.00015 | 3K × 0.10 = $0.0003 | 3K × 0.50 = $0.0015 | **$0.00195** | 1x |

Per-call ratios sit just under the list ratios (40x and 100x) because cache reads are discounted differently per model [N53].

### 7.4 Per 10-minute lesson, LLM line

**Scene lines:**

| Model | Scene calls | Cache writes (120K tokens) | **Scenes total** |
|---|---|---|---|
| Fable 5.1 | 30 × 1.2 × $0.18375 = $6.615 | 120K × $12.50 = $1.50 | **$8.115** |
| Opus 5.5 | 30 × 1.3 × $0.075 = $2.925 | 120K × $5 = $0.60 | **$3.525** |
| Sonnet 5.5 | 30 × 1.5 × $0.039 = $1.755 | 120K × $2.50 = $0.30 | **$2.055** |
| Haiku 5.5 | 30 × 2.6 × $0.00195 = $0.152 | 120K × $0.125 = $0.015 | **$0.167** |

**Text lines** (all with the 1.3 regeneration factor):

| Text option | Arithmetic | **Cost** |
|---|---|---|
| Fable | ($2.00 + $1.90) × 1.3 | **$5.07** |
| Opus | (200K × $4 = $0.80; 38K × $20 = $0.76) → $1.56 × 1.3 | **$2.028** |
| Sonnet | ($0.40 + $0.38) × 1.3 | **$1.014** |
| Haiku | ($0.02 + $0.019) × 1.3 | **$0.051** |
| Today's mix | Sonnet 120K/25K = $0.49; Opus 60K/10K = $0.44; Haiku 20K/3K = $0.0035 → $0.9335 × 1.3 | **$1.214** |
| Haiku author + Sonnet review | Haiku 140K/28K = $0.028; Sonnet 60K/10K = $0.22 → $0.248 × 1.3 | **$0.322** |

**Expected escalation, central case** (10% of scenes go to Haiku-xhigh, 8% to Sonnet, 2% to Opus):

| Rung | Arithmetic | Cost |
|---|---|---|
| Haiku-xhigh | 3 scenes × 2 calls × $0.00345 (6K output) | $0.021 |
| Sonnet | 2.4 scenes × 1.5 × $0.039 + one 15K write × $2.50 | $0.178 |
| Opus | 0.6 scenes × 1.5 × $0.075 + one write $0.075 | $0.143 |
| **Total** | | **$0.341** |

**Shadow:** 5% of scenes on the Opus Kit is about **$0.18**.

| Scenario (LLM line per lesson) | Arithmetic | **Total** | Ratio vs Opus-only Kit |
|---|---|---|---|
| A. Fable-only on the Kit | 5.07 + 8.115 + 0.07 | **$13.26** | 0.42x |
| B. Opus-only on the Kit | 2.028 + 3.525 + 0.07 | **$5.62** | 1x |
| C. Sonnet-only on the Kit | 1.014 + 2.055 + 0.07 | **$3.14** | 1.8x |
| D1. Haiku + system, text on today's mix (until T-arms pass) | 1.214 + 0.167 + 0.07 | **$1.45** | 3.9x |
| D2. Haiku + system, all text on Haiku (only if T-arms pass) | 0.051 + 0.167 + 0.07 | **$0.29** | 19.4x |
| E. **Cascade, central** (Haiku author + Sonnet review; escalation; shadow) | 0.322 + 0.167 + 0.07 + 0.341 + 0.18 | **$1.08** | 5.2x |
| E-pess. Cascade, pessimistic (3.5 Haiku calls per scene; 15% Sonnet, 5% Opus, 15% Haiku-xhigh) | 0.322 + 0.220 + 0.09 + 0.575 + 0.18 | **$1.39** | 4.0x |
| E-today. Cascade with text on today's mix | 1.214 + 0.167 + 0.07 + 0.341 + 0.18 | **$1.97** | 2.9x |

**Scene line only:** Opus Kit scenes plus judge ($3.595) vs Haiku scenes plus judge ($0.237) is 15x. Against the full cascade scene line ($0.758) it is 4.7x.

**Opus-low on the Kit** (the cascade's real competitor): assume 1.5K output instead of 3K [Hypothesis].
- Call: $0.003 + $0.012 + $0.030 = $0.045.
- Lesson: 30 × 1.3 × $0.045 = $1.755, plus $0.60 writes, $2.028 text and $0.07 judge, about **$4.45**.
- The cascade saves **$3.37 per lesson** against it.

### 7.5 Per 30-second Reel (4 scenes; standalone text 40K / 7.6K)

| Scenario | Arithmetic | **Total** | Ratio vs Opus |
|---|---|---|---|
| Opus-only Kit | Text $0.312 × 1.3 = $0.406; scenes 4 × 1.3 × 0.075 = $0.39 + writes 3 × 15K × $5 = $0.225; judge $0.018 | **$1.04** | 1x |
| Haiku + system (text on Haiku) | Text $0.0078 × 1.3 = $0.010; scenes 4 × 2.6 × 0.00195 = $0.020 + writes $0.0056; judge $0.018 | **$0.054** | 19x |
| Cascade, central | Text (Haiku author $0.0056 + Sonnet review $0.044) × 1.3 = $0.065; scenes $0.026; judge $0.018; expected escalation including probability-weighted cache writes $0.047; shadow $0.020 | **$0.175** | 5.9x |
| Derived Reel (cut down from the approved lesson; LLM writes hook and captions only; that text still goes to GA and the Reel to H-SB, the A-suite and GS, §5.7) | Haiku 8K/1K = $0.0013 + Sonnet check 8K/1K = $0.026 | **≈ $0.03** | — |

[Recommendation] Make the derived Reel the default. The project's three-Short package costs about $4.32 per lesson, about $1.44 per Short [P4], and at that point the LLM line no longer matters.

### 7.6 Batch and caching

- **Batch API** halves both sides, so ratios don't change:
  - Haiku-only lesson: ≈ $0.15
  - cascade: ≈ $0.71–0.80. Escalations stay real-time: (0.322 + 0.167 + 0.07 + 0.18) / 2 + 0.341 = $0.71, or ≈$0.80 if the shadow also runs real-time (corrected 15 Oct 2026; was $0.60–0.70).
- **What can't be batched:** repair turns and escalations run in sequence, and batch turnaround (up to 24 h) can exceed the 1-hour cache TTL. So batch only **round 1** (all scenes, k samples) and **round 2** (failures with errors attached). Escalations run in real time. Server-side refusal fallbacks are rejected on Batches [D9].
- **1-hour writes in batch** cost 2x instead of 1.25x. On Haiku that is 120K × $0.20 = $0.024 vs $0.015, which is immaterial.
- **Pre-warming:** `max_tokens: 0` pre-warms the cache with no output billed [N57] (contested; verify).

### 7.7 Bespoke strong-model generation ([V1]-style), unreconciled

Scaling [V1] from 79 s to 600 s (×7.59):

| [V1] run | Token-based floor (incomplete token counts, all priced at the $20/M Opus output price; corrected 15 Oct 2026, was "upper bound") | [V1]-dollar-based | Ratio vs cascade E ($1.08) | Ratio vs D2 ($0.29) |
|---|---|---|---|---|
| Low effort | 7.59 × 78K = 592K tokens → **$11.85** | 7.59 × $3 = **$22.8** | 11–21x | 41–79x |
| Max effort | 7.59 × 625K = 4.74M → **$94.9** | 7.59 × $49 = **$372** | 88–344x | 327–1,283x |
| Max + ultracode | ≥ 2.5M tokens, ≥ $348, **never finished** | — | not meaningful | — |

The dollar figures exceed the token-based floor, so [V1]'s token counts are incomplete (likely cache reads or sub-agent turns were excluded). Treat the whole row as **unreconciled until week-1 metering**. Linear extrapolation is probably optimistic, because context grows with length [Hypothesis].

### 7.8 Chinese and open models (formula, not prices)

No authoritative prices were supplied for DeepSeek, Qwen, Kimi or GLM, so none are assumed.

- **Hosted API cost per lesson** = Σ calls × (cache-read price × cached tokens + input price × fresh tokens + output price × output tokens), using the provider's caching rules and your measured token factor. The ceiling on the benefit is the Haiku line it replaces: **at most $0.29 per lesson** (D2). With review at $0, that is ≈5% of the D2 total at today's floor ($6.25), ≈13% with clips at $0 ($2.25), and ≈33% at the lean floor ($0.88; ≈28% at the 2027 TTS price). (Corrected 15 Oct 2026; earlier text said under 1%.)
- **Self-hosted cost per lesson** = GPU-hours per lesson × GPU rate. The project's narration model assumes $0.80 per GPU-hour (an assumption, not a quote) [P1].
  - Break-even against Haiku D2: 0.29 / 0.80 = **0.36 GPU-hours, about 22 minutes, per lesson**.
  - The D2 workload processes about 1.9M tokens per lesson (mostly reusable prefill) and generates about 0.28M.
  - Meeting the break-even needs roughly 210 generated tokens per second in aggregate, plus prefill, sustained [Hypothesis; measure in arm O2].
- **Bottom line:** open models are a hedge and a fine-tuning path, not a cost lever.

### 7.9 Total cost per lesson: separate the LLM line from everything else

Project hybrid line items [P1]:

| Line | Cost |
|---|---|
| LLM | $1.716 |
| Narration | $0.96 |
| Generated clips | $4.00 |
| Stills | $0.20 |
| Encoding/render | $0.50 |
| Alignment | $0.10 |
| Storage | $0.20 |
| Human review: academic $15 + QA $5 + repairs $6.67 (85 minutes) | $26.67 |
| **Total** | **$34.34** |

**Non-LLM total: $32.63.**

**Render line, re-derived as render-seconds × rate:**
- The project's cloud example is 8 vCPU / 16 GB, 45 worker-minutes, 20% retry, $0.3555 [P2]. That is $0.00658 per worker-minute.
- The only measured data: 30 s fixture renders at 720×1280 took 27.3–29.4 s wall on two CPU workers [P3], roughly 1–2 worker-seconds per output second.
- One lesson needs about 1,500 output-seconds:
  - final render ×2 for the hash check: 1,200 s
  - seek-sampled candidate frames: about 70 s
  - 20% re-renders
- That is about 3,000 worker-seconds, 50 worker-minutes, **≈ $0.33** at 720p.
- If 1080×1920 costs 2–3x [Hypothesis], the line is **$0.66–1.00**. Keep the $0.50 allowance and add a +$0.50 sensitivity until week 1 meters it.

| Scenario | LLM | **Total per lesson** | vs today ($34.34) | vs Opus-only Kit |
|---|---|---|---|---|
| Today (workbook, 4.6-era tariffs) | $1.716 | **$34.34** | — | — |
| Opus-only Kit (B) | $5.62 | **$38.25** | +11% | — |
| Fable-only Kit (A) | $13.26 | **$45.89** | +34% | +20% |
| Opus bespoke, [V1]-low extrapolated | $11.85–22.8 | **$44.5–55.4** | +30–61% | — |
| Haiku + system, text on today's mix (D1) | $1.45 | **$34.08** | −0.8% | −11% |
| **Cascade, central (E)** | $1.08 | **$33.71** | **−1.8%** | **−11.9%** |
| Haiku + system, all text on Haiku (D2) | $0.29 | **$32.92** | −4.1% | −13.9% |
| E + render at the high end (+$0.50) | $1.08 | $34.21 | −0.4% | — |
| E + generated clips set to $0 | $1.08 | **$29.71** | −13.5% | — |
| E + review cut from 85 to 60 minutes (−$7.84 at $0.3137/min) | $1.08 | **$25.87** | −24.7% | — |
| E + clips $0 + review 60 minutes | $1.08 | **$21.87** | −36.3% | — |

**Review capacity:** 1,000 lessons at 85 minutes is 8.85 FTE-months [P1]. At 60 minutes it is about 6.2.

*Note (15 Oct 2026): this table is superseded by §7.13–§7.14. Its "Today" row ($1.716) is the RD-04 v2 workbook priced at Haiku 4.5 / Sonnet 4.6 / Opus 4.6 tariffs, while the Kit rows use the verified 5.5 tariffs. On one basis, today's LLM line is $1.214 (§7.4). RD-39 already sets generated clips to $0.*

### 7.10 Ongoing costs that earlier drafts left out

Fixed and semi-fixed amounts become per-lesson costs depending on volume:

| Ongoing item | Monthly | Per lesson at 100/month | Per lesson at 1,000/month |
|---|---|---|---|
| 5% Opus shadow (already in E) | — | $0.18 | $0.18 |
| Friday trace mining (≤ $40/week while stabilising; $10/week after) | $173 → $43 | $1.73 → $0.43 | $0.17 → $0.04 |
| Template backlog (2 templates × ~$10 strong-model build, plus engineer time) | $20 + eng | $0.20 | $0.02 |
| Holdout re-run per Kit or model change (Haiku ≈ $1.10 + 24 human spot-ratings ≈ 1.6 h × $18.82 ≈ $30), 2 per month | $62 | $0.62 | $0.06 |
| Extra render compute for double renders and k-sampling | in §7.9 | — | — |

At 100 lessons per month, these overheads ($1.25–2.55 per lesson) can cancel most of the $3.37 saving against Opus-low on the Kit. **[Recommendation] Cut mining to $10 per week once the escape rate is stable.**

### 7.11 Programme cost and break-even

| Item | Amount |
|---|---|
| LLM, itemised in protocol §2.6 (S arms $435 incl. the Ultra probe, build $220, Kit/text arms $20, Haiku arms $40, judge calibration $5, pilot $40, open models ≤ $50 cap) | ~$810; **cap $1,000** (reconciled 15 Oct 2026; earlier text said S arms ~$385 and misc ~$55) |
| Rater time: ≈ 54 h × $18.82/h (the project's blended review rate, $26.67 / 85 min) | ≈ $1,016 |
| Academic approvals: ≈ 16 h (54 packages, rubric and thresholds, 8 templates) | ≈ $301 |
| Engineering: ≈ 185 h [Hypothesis; earlier drafts' 40 h was too low] | 185 × your rate |
| **Subtotal excluding engineering, at the $1,000 LLM cap** | **≈ $2,317** (≈ $2,127 at the itemised $810) |

**Break-even:**
- Against the Opus-only Kit (saving $4.54 per lesson): $2,317 / $4.54 ≈ **510 lessons** at the cap (≈ 469 at the itemised $2,127), plus 185 h × rate / $4.54.
- Against Opus-low on the Kit (saving $3.37): **≈ 690 lessons** at the cap (≈ 631 itemised), plus engineering.
- *Superseded by §7.13 item 4 (15 Oct 2026): rater and academic hours are no longer cash.*
- Against today's pipeline there is **no LLM saving to pay it back**. Today has no animation layer, and E costs about the same LLM dollars.

So the programme pays for itself in three ways:

1. It makes Opus-grade animation affordable at today's LLM line.
2. It cuts review minutes. Every 10 minutes saved is $3.14 per lesson, so 10,000 lessons × $3.14 dwarfs everything above.
3. It hedges against vendor lock-in.

If the team wants neither animation nor a review-time reduction, don't run it.

### 7.12 What 40–100x does and does not apply to

| Claim | Holds? |
|---|---|
| Haiku is 40x cheaper than Opus and 100x cheaper than Fable per token | Yes, as list price [N20] |
| ...per Kit call | ~38x / ~94x |
| ...per lesson, like for like, Haiku does everything and passes | ~19x vs Opus; ~46x vs Fable |
| ...per lesson, protected cascade | ~5x (central), ~4x (pessimistic) |
| ...vs bespoke strong-model generation | 11–344x for the cascade; mostly an **architecture** effect |
| ...on total cost per video | **No.** −2% vs today, −12% vs an Opus-only Kit; review minutes and generated clips are the levers. *(Superseded 15 Oct 2026, §7.14. With review at $0, clips at $0 and one price basis: −4% vs today and −60% vs an Opus-only Kit. At the lean floor, Path B only: at most ≈7× vs an Opus-only Kit and 14–27× vs bespoke [V1]-low. 40–100× only vs [V1]-max bespoke runs.)* |

### 7.13 Addendum (15 Oct 2026): human review at $0 (founder/team review, no cash cost)

The founder has decided that academic review, production QA and repairs are done in-house at **no cash cost**. The §7.9 totals therefore change: the $26.67 review line is removed and the non-LLM floor becomes the remaining items. Three floors are shown: **today's floor** ($5.96 = narration $0.96 + generated clips $4.00 + stills $0.20 + render $0.50 + alignment $0.10 + storage $0.20), **clips set to zero** ($1.96, which the cost model already recommends [P4]), and a **lean floor** (≈$0.59: Gemini-class TTS ≈$0.14 per the narration research, stills $0.20, own-hardware render residual ≈$0.10, alignment $0.10, storage $0.05) [Hypothesis]. *Corrected 15 Oct 2026:*
- The TTS price is $0.14 only through 31 Dec 2026. It is $0.28 from 1 Jan 2027, which makes the lean floor ≈$0.73 (08 CONSOLIDATED E.6).
- Every floor here assumes TTS narration, so it applies to **Path B** content only.
- Path A, the RD-39 baseline and the 2027 column are in §7.14. LLM lines are unchanged from §7.4.

| Scenario | LLM line | Total, today's floor ($5.96) | Total, clips $0 ($1.96) | Total, lean floor (≈$0.59) |
|---|---|---|---|---|
| Today (workbook mix, 4.6-era tariffs; superseded) | $1.72 | $7.68 | $3.68 | $2.31 |
| **Today, same mix at 5.5 tariffs** (added 15 Oct 2026; the clips-$0 column is the RD-39 runbook baseline) | $1.214 | **$7.17** | **$3.17** | **$1.80** |
| Fable-only Kit (A) | $13.26 | **$19.22** | **$15.22** | **$13.85** |
| Opus-only Kit (B) | $5.62 | **$11.58** | **$7.58** | **$6.21** |
| Opus-low on Kit | $4.45 | **$10.41** | **$6.41** | **$5.04** |
| Sonnet-only Kit (C) | $3.14 | **$9.10** | **$5.10** | **$3.73** |
| Haiku + system, text on today's mix (D1) | $1.45 | **$7.41** | **$3.41** | **$2.04** |
| Cascade, central (E) | $1.08 | **$7.04** | **$3.04** | **$1.67** |
| Cascade, pessimistic (E-pess) | $1.39 | **$7.35** | **$3.35** | **$1.98** |
| Haiku + system, all text on Haiku (D2) | $0.29 | **$6.25** | **$2.25** | **$0.88** |
| Opus bespoke, [V1]-low extrapolated (low end) | $11.85 | **$17.81** | **$13.81** | **$12.44** |
| Opus bespoke, [V1]-low extrapolated (high end) | $22.80 | **$28.76** | **$24.76** | **$23.39** |

**Ratios on total cost per lesson with review free** (lean floor at the 2026 TTS price; the 2027 values and the today-based ratios are in §7.14):

| Comparison | Today's floor | Clips $0 | Lean floor |
|---|---|---|---|
| Opus-only Kit → Cascade (E) | 1.64× (−39%) | 2.49× (−60%) | 3.7× (−73%) |
| Opus-only Kit → Haiku-all (D2) | 1.85× (−46%) | 3.37× (−70%) | 7.1× (−86%) |
| Fable-only Kit → Haiku-all (D2) | 3.1× | 6.8× | 15.7× |
| Opus bespoke ([V1]-low, extrapolated) → Cascade (E) | 2.5–4.1× | 4.5–8.1× | 7–14× |
| Opus bespoke ([V1]-low, extrapolated) → Haiku-all (D2) | 2.8–4.6× | 6.1–11.0× | 14–27× |

**What changes in the conclusions**

1. **The model swap now matters in cash.** With review free, the LLM line is no longer about 5% of the per-lesson total. For scenarios E through B it is:
   - 15–49% at today's floor
   - 36–74% with clips at $0
   - 65–90% at the lean floor; the Fable-only Kit reaches 96%

   (Corrected 15 Oct 2026; earlier text gave only today's-floor range.) The cascade cuts the total by about 39% against an Opus-only Kit at today's floor and by about 60% once generated clips are zero. Against today's pipeline on one price basis it is only ≈2% at today's floor and ≈4% with clips at $0 (§7.14). Against bespoke strong-model generation of the [V1] kind, the total drops 4.5–8.1× (clips $0). That is the regime the founder's 40–100× intuition comes from.
2. **40–100× on total still needs the floor to shrink.** The LLM line can fall 19× (D2) or more, but narration, render, stills, alignment and storage do not fall with it. Only at the lean floor (cheap TTS, own render hardware, no generated clips) does Haiku-all reach about 7× against an Opus-only Kit and 14–27× against bespoke generation. At the 2027 TTS price these become ≈6.2× and 12–23×. These are the maxima the tables support. 40–100× appears only against [V1]-max bespoke runs (§7.14). So the order of levers is:
   - (a) build the Kit (makes every model cheaper)
   - (b) zero the generated-clip allowance
   - (c) move narration to the cheapest TTS that passes the native-speaker gate
   - (d) render on owned hardware
   - (e) then use the cheap-model cascade. At the lean floor it is worth ≈3.7× (cascade) to ≈7× (Haiku-all) against an Opus-only Kit, not a further order of magnitude (corrected 15 Oct 2026).
3. **Free is not infinite.** Review has no cash cost but it still has a capacity cost: 85 minutes per lesson is about 1,417 hours per 1,000 lessons (8.85 full-time months). The verifier QA report and the anim-qa checks are now a **throughput** lever rather than a dollar lever: every 10 minutes saved per lesson is about 167 hours per 1,000 lessons of founder time. Keep the review-minutes track in the pilot for that reason. Path A lessons also need performer time, and every lesson and Reel now needs storyboard-review minutes (§7.14).
4. **The programme pays back faster.** Rater-hours and academic approval hours are no longer cash: programme cost is ≈$810 LLM (cap $1,000) plus engineering time. Against an Opus-only Kit the LLM saving is $4.54 per lesson, so the LLM cap is recovered in about 220 lessons; against Opus-low on the Kit ($3.37 saving) in about 297 lessons; against bespoke generation it is recovered in the first 93–46 lessons.
5. **Nothing else in the decision table changes** (except the open-model share in §0 item 11 and §7.8, corrected 15 Oct 2026). The Kit-first order, verifier-only advancement, the cascade, the human gates (GA, H-SB, GF, GS), the week-1 metering blocker and the open-model hedge all stand. §7.12's last row becomes: "on total cost per video: yes, meaningfully, once review is free and clips are zero. At the lean floor (Path B), at most ≈7× vs an Opus-only Kit and 14–27× vs bespoke [V1]-low. 40–100× only vs [V1]-max bespoke runs" (corrected 15 Oct 2026; earlier text said "40–100× only at the lean floor").

### 7.14 Addendum (15 Oct 2026): audit corrections to the cost framing

Source: `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` §3, "Section 13 cost framing overstates the savings". Every figure is still a [Hypothesis] until the week-1 meters exist. The LLM lines are unchanged from §7.4.

**(a) One price basis and the RD-39 baseline.**
- §7.9 and §7.13 used a "Today" LLM line of $1.716. That is the RD-04 v2 workbook at 4.6-era tariffs. The Kit rows use the verified 5.5 tariffs.
- On one basis, today's mix costs $0.9335 × 1.3 = **$1.214** (§7.4).
- The runbook already sets generated clips to 0 s (RD-39). The **clips-$0 column is therefore the baseline**, and the $4.00 clip allowance is kept only as a sensitivity.

**(b) TTS price change.** The lean floor's TTS line is $0.1392 through 31 Dec 2026 and $0.2784 from 1 Jan 2027 (08 CONSOLIDATED E.6). The lean floor is therefore ≈$0.59 now and ≈$0.73 from 2027. Scaled production falls after 1 Jan 2027, so plan with the 2027 column.

**Totals per lesson, review at $0, Path B (TTS) content:**

| Scenario | LLM | Today's floor, clips $4 (sensitivity) $5.96 | **Clips $0 (RD-39 baseline) $1.96** | Lean floor 2026 $0.59 | **Lean floor from 1 Jan 2027 $0.73** |
|---|---|---|---|---|---|
| Today, 5.5 tariffs | $1.214 | $7.17 | **$3.17** | $1.80 | **$1.94** |
| Today, 4.6-era tariffs (old basis, for reference) | $1.716 | $7.68 | $3.68 | $2.31 | $2.45 |
| Fable-only Kit (A) | $13.26 | $19.22 | **$15.22** | $13.85 | **$13.99** |
| Opus-only Kit (B) | $5.62 | $11.58 | **$7.58** | $6.21 | **$6.35** |
| Opus-low on Kit | $4.45 | $10.41 | **$6.41** | $5.04 | **$5.18** |
| Sonnet-only Kit (C) | $3.14 | $9.10 | **$5.10** | $3.73 | **$3.87** |
| Haiku + system, text on today's mix (D1) | $1.45 | $7.41 | **$3.41** | $2.04 | **$2.18** |
| Cascade, central (E) | $1.08 | $7.04 | **$3.04** | $1.67 | **$1.81** |
| Cascade, pessimistic (E-pess) | $1.39 | $7.35 | **$3.35** | $1.98 | **$2.12** |
| Haiku + system, all text on Haiku (D2) | $0.29 | $6.25 | **$2.25** | $0.88 | **$1.02** |
| Opus bespoke, [V1]-low extrapolated | $11.85–22.80 | $17.81–28.76 | **$13.81–24.76** | $12.44–23.39 | **$12.58–23.53** |
| Opus bespoke, [V1]-max, token-based floor only | ≥ $94.9 | ≥ $100.86 | **≥ $96.86** | ≥ $95.49 | **≥ $95.63** |

**Ratios on total cost:**

| Comparison | Today's floor | **Clips $0** | Lean 2026 | **Lean 2027** |
|---|---|---|---|---|
| Today (5.5) → Cascade (E) | 1.02× (−2%) | **1.04× (−4%)** | 1.08× (−7%) | **1.07× (−7%)** |
| Today (5.5) → Haiku-all (D2) | 1.15× (−13%) | **1.41× (−29%)** | 2.05× (−51%) | **1.91× (−47%)** |
| Today (5.5) → D1 | D1 is 3% dearer | **D1 is 7% dearer** | D1 is 13% dearer | **D1 is 12% dearer** |
| Opus-only Kit → Cascade (E) | 1.64× | **2.49×** | 3.7× | **3.5×** |
| Opus-only Kit → Haiku-all (D2) | 1.85× | **3.37×** | 7.1× | **6.2×** |
| Fable-only Kit → Haiku-all (D2) | 3.1× | **6.8×** | 15.7× | **13.7×** |
| Bespoke [V1]-low → Cascade (E) | 2.5–4.1× | **4.5–8.1×** | 7.4–14.0× | **7.0–13.0×** |
| Bespoke [V1]-low → Haiku-all (D2) | 2.8–4.6× | **6.1–11.0×** | 14.1–26.6× | **12.3–23.1×** |
| Bespoke [V1]-max (token floor) → Cascade (E) | ≥ 14× | **≥ 32×** | ≥ 57× | **≥ 53×** |
| Bespoke [V1]-max (token floor) → Haiku-all (D2) | ≥ 16× | **≥ 43×** | ≥ 109× | **≥ 94×** |

**(c) Where 40–100× applies.** It does not apply against today's pipeline. Against today the cascade saves ≈4% and Haiku-all ≈29% on the RD-39 baseline. It does not apply against an Opus-only Kit either: the maximum there is ≈7×, falling to ≈6.2× from 2027. It does not apply against bespoke [V1]-low generation, where the range is 14–27×, or 12–23× from 2027. It appears only against bespoke [V1]-max runs, whose own figures are unreconciled (§7.7). Read the earlier "40–100× at the lean floor" wording in this light.

**(d) Open models.** At most $0.29 per lesson. That is ≈5% of D2 at today's floor, ≈13% at clips $0, ≈33% at the 2026 lean floor and ≈28% at the 2027 lean floor. They are still a hedge, not a cost plan.

**(e) Path A (teacher performance + STS + cutaways).** The playbook (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §7.1, Step 4) makes every full lesson Path A. In Path A a teacher performs the lesson, speech-to-speech converts it, and 1–3 real teacher cutaways are filmed. Every floor above assumes Path B TTS, so **the lean floor applies only to Path B content**: Reels, recaps, and any lesson explicitly approved as Path B. Path A rows:

| Line, per 10-minute lesson | Path A value | Source |
|---|---|---|
| Speech-to-speech conversion (replaces TTS) | $1.224 (8.5 min × 1.2 retry × $0.12/min) | 08 COST_MODELS_EXPLAINED narration machine cost |
| Performer | 0.75 recording h: $0 cash if in-house, $22.50 at the 08 rate of $30/h | 08 CONSOLIDATED narration inputs |
| Teacher cutaways (1–3 per lesson) | unknown; filming time not modelled | PLAYBOOK |
| Higgsfield credits (paper-collage style only) | unknown; per-model credit costs unverified (12 Q5); doodle default uses none (AD-31) | 12/05 |
| Storyboard-review minutes (H-SB) | unmeasured (12/05 `storyboard_review: null`) | 12/05 |
| **Path A floor, clips $0, performer in-house** | **≈ $2.22** + unknowns | 1.96 − 0.96 + 1.224 |
| **Path A lean floor, performer in-house** | **≈ $1.67** + unknowns (STS is not subject to the Gemini 2027 change) | 0.59 − 0.14 + 1.224 |

Path A totals with performer in-house and the unknowns at zero:

| Scenario | Clips $0 | Lean |
|---|---|---|
| Today (5.5) | $3.44 | $2.89 |
| Opus-only Kit (B) | $7.84 | $7.29 |
| Cascade (E) | $3.30 | $2.75 |
| Haiku-all (D2) | $2.51 | $1.96 |

On Path A lessons, Opus-only Kit → D2 is ≈3.1–3.7× and Opus-only Kit → E is ≈2.4–2.6×. Add $22.50 per lesson if the performer is paid.

**Path A capacity.**
- Review is 85 min and the performer adds ≈45 min, so a lesson needs ≈130 min.
- That is ≈2,167 h per 1,000 lessons (≈13.5 FTE-months at the 160 h/month implied by §7.13 item 3).
- Storyboard-review minutes and cutaway filming come on top and are unmeasured.

**(f) Other corrections made on 15 Oct 2026:**
- **§7.6:** the batched cascade is ≈$0.71–0.80.
- **§7.7:** "token-based upper bound" is now "token-based floor".
- **§7.11:** the S-arm budget is $435 and judge calibration $5, as in the protocol. $2,317 is labelled "at the $1,000 cap"; the itemised figure is $2,127.
- **§7.1:** the Sonnet cache-read difference is under $0.01 for the cascade and ≈$0.07 for Sonnet-only C.
- **§7.2:** the sensitivity figures are 1.77×, 19.4→13.9 and 15.2→10.2.
- **§7.13 item 1:** the LLM-share ranges are given per floor, and the bespoke range is 4.5–8.1×.
- **Protocol §5 item 7:** the rater table uses 10 shadow pairs, not 20 (53.7 h ≈ 54 h; ≈$1,011 vs the rounded $1,016 kept in §7.11).
- **README:** cache reads are 2.5–10% of the input price ($0.25 / $0.20 / $0.20 / $0.01).

---

## 8. Chinese and open models

### 8.1 When they fit

- **Vendor independence:** a second, working stack that runs the same Kit.
- **Data residency or offline operation.**
- **Fine-tuning:** a trainable student once there are at least 400–500 accepted traces. Comparable work used 446 demonstrations [N78], and render-in-the-loop training reached 94% render success [N68].
- **They do not fit as a cost lever** (§7.8).

### 8.2 Concrete shortlist [Recommendation; verify current versions, licences and terms at test time]

| Route | Candidates | Why | Main checks |
|---|---|---|---|
| **Hosted Chinese APIs** | DeepSeek (its own API), Qwen (Alibaba Cloud Model Studio), Kimi (Moonshot AI), GLM (Zhipu/Z.ai) | Low list prices; strong coding models; tool-calling or JSON modes | Jurisdiction and retention terms; whether data is used for training; strict JSON-schema support; caching and batch availability; rate limits; uptime from India |
| **Self-hosted open weights** | Qwen3-Coder-30B-class (the family in ManimBench [N68]); a mid-size Qwen instruct model; GLM open-weights; DeepSeek open weights only if multi-GPU is acceptable | Fine-tuning path; no data leaves your infrastructure | GPU cost and throughput vs the 0.36 GPU-h break-even; licence for commercial use; grammar-constrained decoding for the slot schema |
| **Indic control** (not Chinese) | An India-focused open model family, if available | Hindi, Hinglish and Assamese register control for the T1 arm | Licence; quality on Assamese |

### 8.3 Risks

- **Data:** send curriculum content only, never student data. Review terms before any hosted call.
- **Licence:** some open weights restrict commercial use or require attribution.
- **Tool-use and JSON reliability:** Anthropic's strict-schema guarantees don't transfer. Expect more V0 failures; use grammar-constrained decoding on self-hosted models.
- **Availability:** rate limits, regional outages, model deprecations.
- **Safety behaviour:** refusal patterns on chemistry and biology differ. Run the adversarial set.
- **Tokenizers:** counts for Devanagari and Assamese can be much higher. Measure them; don't assume.

### 8.4 How to test (arms O1 and O2, week 6)

1. Same Kit, same controller, same verifiers.
2. Dev 24 × 3 samples, then the holdout only if dev passes.
3. Run T1 Hindi, Hinglish and Assamese caption sets.
4. Measure token factors with each provider's counter on the same prompts.
5. Compute cost per accepted scene with the provider's real invoice.
6. Do the data and licence review **before** the first call.

---

## 9. Risks, failure modes, and what NOT to do

### 9.1 Main risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Optimising the wrong line:** the LLM line is about 5% of cost; review is about 78% *(superseded 15 Oct 2026: review is $0 cash (§7.13), so review minutes are a capacity constraint and the LLM line is 15–90% of the cash total for scenarios E–B, §7.13–§7.14)* | Make cost per accepted lesson (LLM + human minutes) the headline metric; run a review-minutes track in the pilot |
| 2 | **Verifier Goodhart:** passes every gate but teaches poorly or looks dull | Escape rate; blind rubric; V6; rotating holdout; humans stay final. Verifiers guard correctness; taste lives in the templates |
| 3 | **Escalation creep:** at 20% escalation past tier 1 the cascade approaches Opus-low cost | Per-archetype escalation KPI; above 15% over 20 lessons is a Kit defect to fix once, not to keep paying for per video |
| 4 | **Library ceiling and sameness** | Variants, seeds, monotony rubric, monthly template backlog fed by escalations |
| 5 | **Overfitting to the dev set** | Sealed holdout; out-of-distribution regression is real [N77]; rotate holdout quarterly |
| 6 | **Exemplar cloning:** stale labels, wrong counts | Slot maps; V2 strings ⊂ brief; 2 diverse exemplars |
| 7 | **API shape errors:** forced tool choice 400, edited history 400, effort cache resets, Sonnet default high | §2.5 settings in the controller, with unit tests in week 1 |
| 8 | **Pricing cliffs:** Haiku > 100K tier; cache misses | Token guard at 60K; archetype-sorted queues; cache-read ratio on the dashboard |
| 9 | **Refusals on chemistry or biology** [N16] | Route to tier 2 with no retry; adversarial scene; track by category |
| 10 | **Nothing rendered yet** | Week-1 blocker: every gate number is fiction until a scene renders deterministically |
| 11 | **Reviewer automation bias** | Seeded defects; catch-rate KPI |
| 12 | **Model churn** | Pinned IDs; holdout re-run is a release gate |
| 13 | **Skill supply chain** | Install and audit only trusted skills [N29] |
| 14 | **Contested evidence** | Several Haiku figures are contested ([N3], [N5], [N10], [N35], [N36]); re-measure on ExamLeaf rather than cite |

### 9.2 What NOT to do [Recommendation]

1. Don't hand Haiku a 70,000-word manual and ask for free-form HTML/JS. Arm C1-full measures this so the team can see the result, not argue about it.
2. Don't use ultracode or open-ended max-effort runs beyond the single attended, founder-approved $50 probe (D-9). Never use ultracode in production.
3. Don't run best-of-N without a verifier [N92].
4. Don't trust "done": a model's self-report never advances state [N10].
5. Don't edit conversation history in repair loops [D5].
6. Don't change top-level effort mid-conversation [N14]. Use per-message effort.
7. Don't use forced `tool_choice` on Opus, Sonnet or Fable [D1].
8. Don't let any model write on-screen science text, formulas or diagrams outside fixtures.
9. Don't let an LLM judge sign off on science, and don't remove or reorder any human gate (GA → H-SB → … → GF; GS for every Reel). Reels never inherit approval (§5.7).
10. Don't send prompts above 100K to Haiku (C1-full is the one deliberate exception).
11. Don't quote 40–100x as a total-cost reduction, except explicitly against [V1]-max bespoke runs (§7.14).
12. Don't fine-tune before about 400 accepted traces exist, and never without the holdout.
13. Don't send student data to hosted third-party APIs.

---

## 10. Rollout plan (6 weeks, with gates)

| Week | Deliverables | Exit gate |
|---|---|---|
| **1. Unblock and meter** | Node 22 + FFmpeg; `preflight.sh` passes; one template renders on HyperFrames with a double-render hash match. Ledger and cost calculator built from usage fields. Controller skeleton: token guard, §2.5 request shapes, append-only repair. `count_tokens` factor (Haiku vs Opus, 4 languages). Haiku A/B: forced tool vs auto + strict + thinking. Confirm Haiku image input. Freeze 54 packages (academic approves excerpts and fixtures). `kit_cascade` family requested from the section-12 owner (D-16). Ratify rubric and §6.5 thresholds. Run S0, P-low baseline on 6 scenes, and C0 | One scene renders deterministically; 31/31 negative tests run through V0–V3; first metered tokens replace §7.2 |
| **2. Strong-model arms** | S0–S5 within caps; T0–T3 text arms; blind rating; failure taxonomy counts; Fable drafts the 8 archetype slot schemas | Every dev scene has a rated strong reference; Ultra probe logged |
| **3. Build the Kit** | 8 templates with self-tests and golden hashes; V2, V4, V5 extended from the existing `examleaf-anim-qa` scripts and the contract timing rule (corrected 15 Oct 2026; were "built"); V6 calibrated; error catalogue; golden and negative cards; skills; closure matrix; compiled-gold re-rating | Compiled golds rated within 0.5 of the originals; judge-agreement report; ≥ 80% of closures at rungs 1–3 on the existing edge cases |
| **4. Cheap-model tuning** | C1-trim, C1-full, C2, C3 (4 efforts, k = 1 and 3); C5 Sonnet; P-med; two mining iterations; capability ledger v0 | Production effort chosen by cost per accepted scene; ablation table (C0 → C3) published |
| **5. Holdout and pilot** | C4 sealed holdout + adversarial; integration run 1 (cascade + Opus shadow) with both human gates; review minutes timed using the QA report | §6.5 metrics computed with Wilson bounds; measured cost per accepted lesson |
| **6. Decide and harden** | Integration run 2; O1 and O2 open-model arms; go/no-go ADR per family; production SOP; drift shadow; update `08_cost_models` with measured numbers | Decision per family: Haiku tier, Opus-low tier, or Sonnet tier. Backed by measured cost per accepted lesson and escape rate, not list-price ratios |

---

## 11. Decisions table and open questions

### 11.1 Decisions

| # | Decision | Choice | Evidence | Revisit when |
|---|---|---|---|---|
| D-1 | What strong models produce | A Production Kit (code, schemas, verifiers, cards, eval), not a manual | [N30][N58–N66]; §1 | C1-full ≈ C3 in the ablation |
| D-2 | Architecture spine | Verifier + cascade, with constrained slot-fill templates | Judges' synthesis; [N62][N63][N88–N92] | Escalation > 15% persists |
| D-3 | Full DSL compiler | Not in v1; templates + slot schemas only | Build effort | > 3 recurring "custom draw" escalations per week |
| D-4 | Haiku output path | `output_config.format` + adaptive thinking; no forced tools | [D1][D2][N13] | Week-1 A/B shows otherwise |
| D-5 | Haiku effort | Start medium; production level set by the C3 sweep (low to xhigh) | [N9][N95]; no import from max-effort benchmarks | Each model release |
| D-6 | Higher-effort rung | Haiku xhigh via per-message effort before Sonnet | [D4] | Rung's cost per accepted scene > Sonnet's |
| D-7 | Tokenizer handling | No Haiku-only factor; measure both models with `count_tokens` | [D8][N2][N42] | — |
| D-8 | Text tasks | Today's mix until T0–T3 pass; then Haiku author + Sonnet review | Critic must-fix; §7.4 | Per-task pass |
| D-9 | Ultracode | One probe (S5), run as an **attended, founder-approved exception**. The founder approves the specific run in writing in `experiments/APPROVALS.md`. A human is present for the whole run. It runs in an isolated experiment sandbox outside the production governor, on a dedicated key with a **$50 provider-side spend limit** that is the hard stop; the wrapper meter is a second line only. **No probe result can enable ultracode in production.** Banned everywhere else (corrected 15 Oct 2026) | [V1]; 12 AD-02, AD-20; NT-01 | Never for production. The earlier "probe finishes under cap with a better rating" trigger is withdrawn. 12 edge case #3 ("sandbox only, low effort") should be aligned by its owner |
| D-10 | Statistics | Scene-level Wilson LBs; family decisions provisional; sequential confirmation at n ≥ 40 | §6.4 | Holdout expanded to 40 |
| D-11 | Reels | Derived from the approved lesson cue sheet by default. **No inherited approval**: new wording → GA; each Reel gets H-SB, the full A-suite and GS on its own hash; claim IDs carry over only to shorten review (corrected 15 Oct 2026) | [P4]; §5.7, §7.5; 07/05; 12 AD-12 | Reel-only content needs bespoke scenes |
| D-12 | Generated clips | Default allowance zero | [P4] | A pedagogical case is approved |
| D-13 | Open models | Hedge arm in week 6; no cost claims | §7.8, §8 | Price quotes + Indic pass |
| D-14 | Sonnet cache-read price | Use $0.20 (conservative); flag the conflict | [N19][N84][D11] | Invoice confirms |
| D-15 | Minimum cache length | 512 tokens on the 5.5 family and Fable 5.1 (closes the old open question) | [D6] | — |
| D-16 | Effort-policy scope (added 15 Oct 2026) | Section 12's AD-02, AD-11 and AD-24 govern the **strong-model phase**: scene code at explicit high, 3 authoring loops, Opus-high in the pilot. That covers the S arms, the Kit build (B), template authoring and tier-3 escalations. Kit slot-fill production runs under a new **`kit_cascade`** task family with its own caps: tier 1 Haiku 1 + 2 repairs (k ≤ 3); tier 1b 1; tier 2 Sonnet 2; tier 3 Opus 2; per-scene ceilings $0.02 / $0.25 / $0.60; the lesson circuit breaker at 20%; ultracode refused. **Text only here.** The `effort_policy.py` change and the matching AD row in `12/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md` belong to the section-12 owner. No cheap-model Kit run starts before they land | Audit (effort/ultracode); 12 AD-02, AD-11, AD-24; §5.8 | Week-4 effort selection |
| D-17 | Per-surface effort defaults, stated once (added 15 Oct 2026) | **Claude Code:** Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to medium (12 [N22]). **Messages API:** Opus 5.5 and Haiku 5.5 default to medium; **Sonnet 5.5 defaults to high** ([D3], [N93]). Rule for both surfaces: always set effort explicitly and log the requested and effective levels; never compare token baselines taken at defaults | [D3]; [N93]; 12/09 §0 | Any model release |
| D-18 | Kit gate order (added 15 Oct 2026) | GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF; GS for every Reel. Academic approval is never after rendering | 12/05 §1; 07/06; audit M4 | Never |
| D-19 | Verifier stack scope (added 15 Oct 2026) | V0–V8 run in addition to 12/10 A1–A17 and 07/06. V2 and V4 extend the existing `examleaf-anim-qa` scripts. V5 uses the contract timing rule (late = fail; ±150 ms is a quality metric only). V3 includes the reverse-order render (AD-21). Fixture-visual archetypes route to the SVG/Manim adapters | Audit M12; 12/10; contract §8 | Week-3 verifier calibration |
| D-20 | Cost baseline (added 15 Oct 2026) | Compare against today at 5.5 tariffs ($1.214) with clips $0 (RD-39). Plan the lean floor at the 2027 TTS price ($0.73). The lean floor applies to Path B content only; Path A lessons use the §7.14 Path A rows | §7.14; RD-39; 08 E.6 | Week-1 meters |
| D-21 | Section-13 skill registration (added 15 Oct 2026) | The eight `examleaf-fill-<archetype>` skills and `templates/` are **PROPOSED, not built**. Owners: `examleaf-motion-harness` (contract), `examleaf-style-guides` (style slots), `examleaf-anim-brief` (brief). Registered in the 06 README and OVERLAP addenda. Do not add the fill skills to `SKILLS_MATRIX.csv` until their archetype passes C4 | Audit cross-section-consistency-7; 06 OVERLAP | An archetype passes C4 |

### 11.2 Open questions

1. What are the real tokens per Kit call and calls per scene? Week-1 and week-4 meters.
2. What is the Haiku-vs-Opus token factor on Hindi and Assamese prompts?
3. Does Haiku vision work well enough for V6 contact sheets?
4. ~~What timing tolerance does V5 need: is ±150 ms right for Super Teacher narration?~~ Closed 15 Oct 2026: V5 uses the contract rule (late = fail). Still open: whether ±150 ms is the right *quality* band for alignment drift.
5. How much do HyperFrames renders at 1080×1920 cost per lesson, and does the Remotion benchmark change the backend?
6. How many review minutes does the QA report actually save? This is the biggest lever and is completely unmeasured.
7. Should the holdout be expanded to 40 scenes in month 2 for per-archetype decisions?
8. Which hosted open-model provider passes the data and licence review?
9. Will archetype coverage hold above 95% of beats, or will the "unknown" rate force more templates?
10. What engineer rate should go into the break-even?

---

## Appendix A: Critic's must-fix list, and where each item is addressed

| # | Item | Where |
|---|---|---|
| 1 | Forced `tool_choice` | §2.5, §5.2, D-4; protocol §3 (week-1 A/B; `has_thinking_block` logged) |
| 2 | Tokenizer factor | §7.1, D-7; all §7 tables recomputed without a Haiku-only factor (D2 ≈ $0.29) |
| 3 | [V1] dollars | §7.7: token-based bounds shown next to dollar-based figures; labelled unreconciled |
| 4 | Text arms | §3.3 T0–T4; D1/E-today scenarios in §7.4 |
| 5 | Statistics | §6.4, §6.5: 24-scene sealed holdout, Wilson LBs, family-level decisions |
| 6 | Rater hours | §7.11 (≈ 54 h counted in the protocol) |
| 7 | Pilot cap | Protocol §2.4: cascade $10.74 + shadow on run 1 only $28.72 → cap $45 |
| 8 | Ongoing costs | §7.10; render line re-derived in §7.9 |
| 9 | API details | §2.5, D-15 |
| 10 | C1-full | §3.3; agentic token guard and compaction rule |
| 11 | Haiku effort | §1.1, D-5, D-6; xhigh in the C3 sweep; Haiku-xhigh rung |
| 12 | Ultra probe and open-model shortlist | §3.3 S5; §8.2 |
