# Architect plan 3 — lens: exemplar-and-prompt-first

**Lens statement (as written by the architect):** exemplar-and-prompt-first: the strong-model experiments become the product. Their output is a curated bank of golden exemplars with traces. Haiku gets those exemplars few-shot, along with explicit rules, negative examples, checklists and cached stable prefixes (style guide + contract + exemplars), and runs inside deterministic verifiers.

**Thesis:** Yes, run the strong-model experiments first, but don't make long prose documentation the main output. Prose alone rarely moves capability from a strong model to a weak one. What does move it is a set of concrete, verified, retrievable artefacts: about 40 golden scene exemplars with condensed traces, the real Haiku failures paired with their fixes, one slot-schema scene pack per scene type, a rulebook where every rule maps to a detector, and the existing seek-deterministic verifiers acting as the referee. Haiku 5.5 then fills slots in proven templates at medium effort, inside a validator loop, under a cached prefix. Escalation is rare and capped. Done this way, the realistic saving on the LLM line is about 20-25x against Opus 5.5 and about 50x against Fable 5.1, after the Haiku tokenizer penalty and extra retries. The pure 40x/100x list-price ratios are ceilings you cannot reach. Total cost per video falls only about 1.25x, because human review ($26.67 of about $34) does not change.

**Cost claim:** LLM line per 10-minute lesson, at list prices with explicit assumptions: Opus 5.5-only about $8.73, Fable 5.1-only about $20.35. The Haiku 5.5 exemplar system comes to about $0.39 after a +36% tokenizer penalty and 1.8 attempts per scene, which is about 22x cheaper than Opus and about 52x cheaper than Fable. A cascade costs about $0.55 at 3% escalation to Sonnet (about 16x) but about $1.94 at 15% escalation to Opus (about 4.5x). Per 30 s Reel: Opus about $1.55, Fable about $3.62, Haiku about $0.068 (about 23x and 53x). Batch halves every figure without changing the ratios. The one-time strong-model programme is capped at $1,500, or about $1.50 per lesson over 1,000 lessons. The 40x and 100x figures are list-price ceilings on the LLM line only. Total per-lesson cost falls only from about $41 (Opus-only) to about $32.7 (about 1.26x), because about $26.67 of human review and about $0.96 of narration are unchanged. Cutting review time is the bigger lever.

**Biggest risk:** Escalation rate and verifier blind spots. If Haiku fails the deterministic gates often enough that 10-15% of scenes escalate to Opus, the LLM saving falls from about 22x to about 4-5x. Pedagogy and aesthetic defects pass the code gates and land on human reviewers, which raises the cost line that dominates (review). On top of that, the whole plan rests on harness gates that have never run on a real renderer (no FFmpeg or Node 22 on this Mac yet), so Week 1 must prove the verifiers before any parity claim means anything.

---

# Exemplar-and-Prompt-First: getting Haiku to make ExamLeaf videos at Opus quality

## 1. Thesis and the honest one-paragraph answer

[Recommendation] Yes, make the videos with strong models first. But treat those runs as **data-generation experiments**, and their deliverable as a **golden-exemplar bank plus verifiers**. Docs come after that and stay short. A cheap model does not become good because it reads 70,000 words of guidance. It gets close to strong-model quality when four things hold together:
1. it copies from a worked example of the exact scene type it is building;
2. it is told the few rules that matter for that type, each with a counter-example;
3. it fills *slots* in a known-good skeleton instead of writing free code;
4. a deterministic verifier tells it exactly what is wrong, and it tries again a bounded number of times.

Anthropic's own skill guidance points the same way:
- measure on every target model, because Haiku needs more guidance than Opus [N58];
- write evals before documentation and baseline without the skill [N60];
- give exact scripts for fragile steps [N61] and one default rather than many options [N66];
- use validator feedback loops [N62] and plan-validate-execute [N63];
- prefer bundled scripts over generated code [N64].

The repeated-sampling literature adds a crucial caveat: cheap models plus many tries beat strong single shots *only when a real verifier exists* [N88–N92]. ExamLeaf already has unusually good verifiers (seek-contract linter, double-render frame-hash check, cue-sheet schema, fixtures). That is the main reason this lens can work here.

The honest cost answer:
- 40x (vs Opus) and 100x (vs Fable) are **list-price ceilings on the LLM line only**.
- After the Haiku 5.5 tokenizer penalty (+30–36% tokens [N2, N42]) and more retries, expect about **22x vs Opus-only** and about **52x vs Fable-only** on the LLM line.
- A cascade with escalation lands at **12–16x** if escalations stay at about 3%, and falls to about **4.5x** if 15% of scenes escalate.
- Total per-video cost drops only about **1.25x**, because human review is about 78% of it and is untouched by model choice.

## 2. System design from this lens: who does what

| Tier | When | Does | Never does |
|---|---|---|---|
| **Strong (Fable 5.1 max, Opus 5.5 high/xhigh)** | Offline, once per scene type and style, then monthly | Authors golden exemplars; writes slot skeletons; adjudicates Haiku failures into negative cards; writes and patches rules; proposes new verifier checks; audits a sample | Run in the per-video path except as a capped escalation; ultracode, ever (V1 ≥2.5M tokens, never finished) |
| **Cheap (Haiku 5.5 medium; later Qwen/DeepSeek/Kimi/GLM through the same pack)** | Per scene, per video | Classifies the scene into an archetype; fills a slot JSON from the cue sheet + brief; generates scene code from the skeleton; repairs it from validator messages; writes on-screen text in the target language | Invent science visuals (fixtures only); change durations (narration sets them); write free-form 3D; exceed 3 attempts; retry a refusal [N16] |
| **Deterministic code** | Every step | Cue sheet and timing; exemplar retrieval (lookup table, not embeddings); prompt assembly with cache breakpoints; linter; double-render hash; duration match; fixture-hash check; safe-zone and text-overflow check; Indic shaping check; render; cost ledger | Judgement calls on pedagogy (humans) |

### 2.1 Prompt layout (cache-first)

[Recommendation] Use four cache breakpoints, the API maximum [N56], ordered from most stable to least:

1. **BP1, system and contract (about 10K tokens):** role; harness contract digest (DURATION, seek(t), seeded PRNG, no wall-clock, no Math.random); the global rulebook (only the rules with severity ≥ high); output protocol; the verification paragraph Anthropic recommends for Haiku [N10].
2. **BP2, style pack (about 6K):** one of the 5 vertical style guides reduced to tokens and do/don't pairs, plus `style_tokens.json`.
3. **BP3, scene-type pack (about 14K):**
   - slot schema;
   - skeleton code;
   - 8–15 numbered MUST/NEVER rules;
   - checklist;
   - **2 golden exemplars** (input brief → slot JSON → final code → 150-word trace);
   - **1 negative exemplar** (bad code → violated rule → detector message → diff).
4. **Variable tail (about 11K fresh):** scene brief from the cue sheet, fixture IDs, language, prior validator output.

The layout respects the platform's behaviour:
- Caches are model-scoped, so each tier has its own prefix.
- Effort is fixed per stage, because changing effort invalidates the cache [N14].
- The whole prompt stays **under 60K tokens**, well below the 100K step where Haiku bills 5x [N5, N20, N82].
- Order scenes so that consecutive calls share BP2/BP3, which keeps the 5-minute TTL warm [N50].
- For batch jobs, use the 1-hour TTL (2x write, pays off after 2 reads [N22, N51]) together with the 50% Batch discount [N21].

### 2.2 Scene archetypes (the unit of transfer)

[Hypothesis] About 12 archetypes cover over 90% of Class 10–12 revision scenes:
- hook/title card;
- definition card;
- fixture-diagram labelled reveal;
- equation derivation (step-by-step);
- process/flow steps;
- compare–contrast split;
- graph/plot build;
- worked numerical;
- misconception bust;
- exam-tip callout;
- recap checklist;
- kinetic quote (Reels).

Each archetype gets one scene pack, in the style of the existing 15 skills: SKILL.md under 500 lines [N59], references one level deep [N65]. Haiku is never asked to "make a video". It is asked to "fill archetype `equation_derivation` v3 for this brief".

## 3. The experiment programme (strong models, offline)

### 3.1 Fixed scene set ES-40 (frozen before any run)

- **36 regular scenes:** 12 archetypes × 3 variants, spread across Physics, Chemistry, Biology and Maths; English, Hinglish and Hindi on-screen text; at least 2 of the 5 styles per archetype. Include the three pilot scenes in `07_benchmark_and_pilot_plan/`.
- **4 adversarial scenes:**
  - an Assamese/Hindi conjunct-heavy kinetic title;
  - a long chemical equation that overflows the 9:16 safe zone;
  - a brief that asks for a diagram with no validated fixture (correct output: refuse/escalate);
  - a 60 s Reel compression of a 4-step process with beat sync.
- **Split:** 24 scenes go to the **exemplar pool**, 16 are **held-out eval** scenes that are never shown to any model as exemplars (contamination control).

### 3.2 Arms (3 samples each, same brief, same seed policy)

| Arm | Model / effort | Context given | Purpose |
|---|---|---|---|
| A | Fable 5.1 max | full section-12 docs + skills | Ceiling; exemplar author |
| B | Opus 5.5 high | same | Production-grade reference |
| C | Opus 5.5 medium and low | same | Anthropic guidance: measure the capable model at lower effort before building a cascade |
| D | Haiku 5.5 medium, bare | brief + contract only | Baseline [N60]; source of real negative examples |
| E | Haiku 5.5 medium | + long docs (no exemplars) | Tests the "just document it" hypothesis |
| F | Haiku 5.5 medium | + scene pack with 2 golden + 1 negative | This lens |
| G | Haiku 5.5 medium/high | F + validator loop (≤3 attempts) | Full cheap system |
| H (optional) | One open model | Identical G pack | Portability check (prices not in our authoritative list, so no cost claim) |

[Recommendation] Hard caps:
- 700K tokens per Fable/Opus scene run (V1 max used 625K for a 79 s video);
- 60K prompt / 16K output per Haiku attempt;
- no ultracode.

### 3.3 What the run timeline captures (one JSONL row per attempt, in `ROOT/13_exemplar_bank/runs/`)

- **Identity:** `run_id, scene_id, arm, model_id, effort, thinking_mode, sample_idx, attempt_idx, pack_hash, exemplar_ids[], date`.
- **Tokens and cost:** `input_fresh, input_cache_read, input_cache_write, output, thinking_share_est, usd_list, wall_seconds, stop_reason` (record `refusal` separately [N16]).
- **Verifier results:** `schema_ok, lint_violations[], hash_match, duration_delta_ms, fixture_hash_ok, safe_zone_violations[], text_overflow[], indic_shaping_ok, render_ok`.
- **Fix loops:** for each failed gate, the error class (taxonomy code), the validator message shown to the model, and whether the next attempt fixed it.
- **Decisions:** strong arms must end with a `DECISIONS` block. It lists 3–7 choices that a less capable model could get wrong (for example "split the equation into 3 lines because width > 860 px at 64 pt", "staggered reveal tied to word timings, not a fixed 0.3 s"), each tagged with the rule it implies.
- **Human rubric:** blind scores from 2 academic reviewers on 6 axes (scientific accuracy, pedagogy clarity, timing/sync, legibility at phone size, style fidelity, polish), 1–5 each, plus pairwise preference against the arm-B output.
- **Artefact paths and hashes** for code, keyframes and render.

### 3.4 What we learn from the arms

- A vs B vs C tells us whether Fable is needed at all, or whether Opus high is enough to author exemplars at 40% of the price.
- D vs E vs F vs G gives the marginal value of docs, of exemplars and of verifiers.
- [Hypothesis] E ≈ D. Long docs alone add tokens without fixing the dominant failure classes. That would justify this lens. If E ≈ G instead, the lens is wrong and docs-first wins.

## 4. Turning experiment output into artefacts (required document types)

Everything lives in `ROOT/13_exemplar_bank/`. Each artefact is versioned and hash-referenced by the prompt assembler.

**4.1 Golden Exemplar Card** (`golden/<archetype>/<id>.md` + code file). Required sections:
1. ID, archetype, style, subject, language, provenance (arm, model, effort, date, pack hash, cost, tokens);
2. exact input brief;
3. slot JSON;
4. final scene code;
5. condensed trace, at most 150 words: plan → the 2–3 errors hit → how each was fixed;
6. the DECISIONS list;
7. "What is fixed vs what varies" (slot map);
8. validator report (all gates green, hash pair);
9. two human rubric sheets, both ≥4 on accuracy and legibility;
10. fixture IDs and licence notes.

Promotion requires both reviewers' sign-off. [Recommendation] Target 2–3 cards per archetype per style family, about 40 cards to start.

**4.2 Negative Exemplar Card** (`negative/<rule_id>/<id>.md`). Required sections:
1. the real failing output, from arm D/E/F/G only (never synthetic);
2. the violated rule ID;
3. the detector and its exact message;
4. the minimal corrective diff;
5. frequency observed (n/attempts).

One negative card is placed in each pack, choosing the archetype's most frequent failure.

**4.3 Scene-Type Pack** (one skill per archetype). Required sections:
1. purpose;
2. use when / don't use when;
3. slot schema (strict JSON; keep to the structured-output limits: ≤24 optional params, ≤16 anyOf, minItems only 0/1 [N45, N46, N48]);
4. skeleton code with `/* SLOT: name */` markers;
5. **one** default approach plus a single escape hatch [N66];
6. numbered MUST/NEVER rules, 8–15 of them;
7. a pre-submit checklist, at most 10 items, phrased as yes/no;
8. golden and negative card IDs;
9. relevant edge cases from the 65-row table;
10. escalation triggers;
11. at least 3 evals [N60].

**4.4 Rulebook** (`RULES.md`, IDs R-001…). Each rule needs: statement, rationale, **detector** (linter rule, script, or explicitly `HUMAN-ONLY`), positive and negative example, severity, and source run IDs. [Recommendation] A rule with no detector and no human gate gets deleted. Unverifiable rules are noise to a small model.

**4.5 Restrictions list** (`RESTRICTIONS.md`): the hard "cheap tier may not" list from §2, each with its enforcement point.

**4.6 Edge-case register:** extend `12_EDGE_CASES_master_table.md` with columns `observed_in_runs`, `cheap_tier_handling` (handle / refuse / escalate) and `detector`.

**4.7 Learnings ledger** (`LEARNINGS.md`, dated): claim → evidence (run IDs, n) → change made to which pack/rule → status (adopted, rejected, watch). Use it to distill successful approaches and common mistakes into skills, as Anthropic suggests [N30].

**4.8 Verifier suite and eval set:** the existing harness scripts, plus new checks born from failures (text-overflow, Indic shaping, fixture hash), plus `evals/heldout/` with the 16 held-out briefs and their gold references.

## 5. Cheap-model operating procedure (per lesson)

1. **Deterministic prep:** narration produces word timings → cue sheet → per-scene briefs with an `archetype` field, chosen by Haiku at low effort with a strict enum. Unknown archetype → escalate.
2. **Assembly:** the script picks the pack for archetype × style, the 2 golden cards whose subject/language match best (lookup by tags), and 1 negative card. It then builds BP1–BP3 plus the tail.
3. **Plan step (plan-validate-execute [N63]):** Haiku 5.5, **medium effort, adaptive thinking**, emits the slot JSON through a strict tool. Don't combine thinking-off with JSON output; it can skip needed tool calls [N13]. A schema check runs immediately.
4. **Execute step:** Haiku fills the skeleton → code.
5. **Verify loop:** run lint → render twice and compare hashes → check duration → check fixture hash → safe-zone, overflow and shaping checks. On failure, return the *exact* validator message plus the rule ID and its 2-line negative example, then retry. **At most 3 attempts.** Bump to high effort only on attempt 3, using a separately cached high-effort prefix [N14, N95].
6. **Escalation:** after 3 failures, a `refusal` stop reason [N16] or an unknown archetype, send the case once to Sonnet 5.5 high. If that fails, mark the scene for human attention. Every escalation becomes a candidate negative or golden card.
7. **Self-report guard:** Haiku may claim success without checking [N10]. Ignore the model's claim; only the gates decide.
8. **Batch:** run storyboard-approved lessons overnight through the Batch API with the 1-hour cache.
9. **Humans:** storyboard gate before any paid generation, then the academic and full-video approvals, exactly as now.

## 6. Quality gates and evals

| Gate | Check | Owner |
|---|---|---|
| G0 | Slot JSON validates against the strict schema | code |
| G1 | Seek-contract lint is clean | code |
| G2 | Double-render frame hashes are identical | code |
| G3 | Scene duration = cue-sheet duration ±1 frame | code |
| G4 | Every science glyph comes from a fixture (hash match) | code |
| G5 | Safe zone, text overflow, Indic shaping, minimum font size | code |
| G6 | Keyframe rubric judge (Haiku judge at high effort, with a 10% Opus audit sample) | model |
| G7 | Storyboard approval | human |
| G8 | Academic and full-video approval | human |

Promotion criteria for running Haiku in production (all measured on the 16 held-out scenes, 3 samples each):
- G0–G5 pass rate ≥95% within 3 attempts;
- escalation rate ≤5%;
- mean human rubric no more than 0.3 points below arm B on any axis;
- blind pairwise preference for Haiku vs Opus-high of at least 40%;
- zero G4 failures reaching humans.

[Recommendation] These thresholds are proposals for the academic team to ratify before data arrives.

Drift control:
- every week, re-run 5% of production scenes on Opus high as a shadow;
- any pack edit triggers the full held-out suite;
- every model swap (including open models) re-runs everything, because performance depends on the model [N58].

## 7. Cost model (LLM line), explicit arithmetic

**Prices** (authoritative, per MTok, input / output / cache read / 5-minute cache write):
- Fable $10 / $50 / $0.25 / $12.50
- Opus 5.5 $4 / $20 / $0.20 / $5
- Sonnet 5.5 $2 / $10
- Haiku 5.5 $0.10 / $0.50 / $0.01 / $0.125 (under 100K prompt)

**Workload assumptions:**
- **Text/planning** (project cost model): 200K input / 38K output per lesson, ×1.3 regeneration = **260K / 49.4K**. Reel = 15% of that = 39K / 7.41K. [Hypothesis]
- **Scenes:** 24 per 10-minute lesson (about 25 s each), 4 per 30 s Reel. [Hypothesis]
- **Per scene attempt:** 30K cached prefix + 11K fresh input + 8K output (including thinking). [Hypothesis]
- **Attempts per scene:** Fable 1.2, Opus 1.3, Haiku 1.8. [Hypothesis, measured in arm G]
- **Haiku tokenizer:** +36% on every Haiku token count [N2], the worst case; N42 says about 30%.
- **Cache write:** one per lesson.

### 7.1 Per 10-minute lesson

**Opus-only:**
- text = 260K×$4 + 49.4K×$20 = $1.040 + $0.988 = **$2.028**
- scene attempt = 11K×$4 + 8K×$20 + 30K×$0.20 = $0.044 + $0.160 + $0.006 = $0.210; ×1.3 attempts × 24 scenes = **$6.552**
- cache write = 30K×$5 = $0.150
- **Total ≈ $8.73**

**Fable-only:**
- text = $2.60 + $2.47 = $5.07
- scene attempt = $0.11 + $0.40 + $0.0075 = $0.5175; ×1.2 × 24 = $14.90
- cache write = $0.375
- **Total ≈ $20.35**

**Haiku system (this lens):**
- text = 353.6K×$0.10 + 67.2K×$0.50 = $0.0354 + $0.0336 = **$0.069**
- scene attempt = 14.96K×$0.10 + 10.88K×$0.50 + 40.8K×$0.01 = $0.0015 + $0.0054 + $0.0004 = $0.00734; ×1.8 × 24 = **$0.317**
- cache write = 40.8K×$0.125 = $0.005
- **Total ≈ $0.39**

**Ratios:**
- Opus/Haiku = **22.3x** (39.2x if there were no tokenizer penalty and equal attempts: the list ceiling)
- Fable/Haiku = **52x**

**Cascade** (Haiku first; escalated scenes spend 3 Haiku attempts, then 1.3 uncached attempts on the bigger model):
- 3% → Sonnet: **$0.55** (15.9x vs Opus)
- 5% → Sonnet: $0.65 (13.3x)
- 3% → Opus: $0.70 (12.5x)
- 15% → Opus: **$1.94 (4.5x)**

Escalation rate is the single biggest cost lever. Every Opus escalation costs as much as about 37 Haiku attempts.

### 7.2 Per 30 s Reel

| System | Arithmetic | Total |
|---|---|---|
| Opus-only | text 39K×$4 + 7.41K×$20 = $0.304; scenes 4×1.3×$0.210 = $1.092; write $0.150 | **$1.55** |
| Fable-only | — | **$3.62** |
| Haiku system | — | **$0.068** (22.6x vs Opus; 53x vs Fable) |
| Cascade, 3% Sonnet | — | $0.095 (16.3x) |
| Cascade, 15% Opus | — | $0.33 (4.7x) |

### 7.3 Batch and amortisation

- **Batch:** 50% off every tier [N21]. It halves absolute costs but leaves the ratios unchanged. Haiku lesson ≈ $0.20 batched.
- **Offline programme (one-time):**
  - per ES-40 scene: Fable max (about 120K output, 80K fresh input, 400K cached ≈ $6.90, ×2 samples), plus Opus high (about $2.80, ×2), plus Opus medium (about $1.50) ≈ $21;
  - 40 scenes ≈ **$840**;
  - Haiku/open ablations (40 scenes × 6 variants × 3 samples ≈ 720 attempts) ≈ **$10**;
  - distillation and authoring passes ≈ $100;
  - **budget cap $1,500** with contingency.
  - Amortised: **$1.50/lesson over 1,000 lessons**, or $7.50 over 200. That is cheaper than the Opus-only premium after about 180 lessons.
  - The real offline cost is **academic reviewer time** for rubric-scoring about 40 goldens plus all arm outputs. Budget roughly 25–35 reviewer-hours. [Hypothesis]
- **[V1] caveat:** the V1 dollar figures ($3, $49, ≥$348) imply about $38–139 per MTok, above Opus 5.5 list output ($20). Use V1 **token counts** as the sizing signal for agentic runs, not its dollars.

### 7.4 What 40–100x does and doesn't apply to

- Non-LLM variable cost per lesson ≈ $34 − $1.72 = **$32.28**: narration about $0.96, render/credits, and human review **$26.67** (85 minutes).
- Opus-only lesson ≈ $32.28 + $8.73 = **$41.01**. Haiku system ≈ $32.28 + $0.39 = **$32.67**. The **total falls about 1.26x, not 40x.** Against today's mixed $34 it falls about 1.04x.
- For Reels the LLM line matters relatively more. The project's three-Short package is about $4.32 per lesson, about $1.44 per Short all-in, so an Opus-only $1.55 LLM line would roughly double a Short's cost, while Haiku's $0.07 is noise.
- [Hypothesis] Exemplars cut review time indirectly: fewer defects reach humans, and reviewers can check against a known archetype. That has to be measured (minutes per lesson in pilots), not assumed. Only a review-time reduction moves total cost meaningfully. Within this lens, cutting 85 to 60 minutes saves about $7.85 per lesson, which is more than the entire Opus-to-Haiku LLM saving.

## 8. Risks and failure modes

1. **Exemplar overfitting / copy-paste:** Haiku clones the exemplar's layout even when the brief differs (wrong label count, stale text). *Mitigation:* slot map in every card; a G5 check that on-screen strings ⊂ brief strings; 2 diverse exemplars, not 1.
2. **Out-of-distribution scenes:** small-model gains regress off-distribution [N77]. *Mitigation:* the archetype classifier must be allowed to say "unknown" → escalate; track the unknown rate and add archetypes when it exceeds 5%.
3. **Escalation creep:** at 15% escalation the economics collapse to about 4.5x. *Mitigation:* the escalation rate is a dashboard KPI; every escalation feeds a card within the week.
4. **Verifier gaps:** gates are code-level; pedagogy and aesthetic errors pass G0–G5. Repeated sampling without a real verifier plateaus [N92]. *Mitigation:* G6 rubric judge plus a 10% Opus audit; humans stay at G7/G8.
5. **Science errors:** the cheap tier invents a formula or diagram. *Mitigation:* fixtures only (G4), formula strings from the validated script, never generated.
6. **Prompt bloat past 100K:** 5x price step [N5]. *Mitigation:* the assembler hard-fails at 60K.
7. **Cache misses:** effort changes [N14], shuffled scene order, model swaps. *Mitigation:* fixed effort per stage, archetype-sorted queues, cost ledger alerts.
8. **Haiku behaviours:** early stopping at low effort [N9, N95], false "done" claims [N10], reasoning leaking into on-screen text [N15], refusals with no fallback [N16]. *Mitigation:* medium default; gates as the only source of truth; G5 string check; refusal routes to Sonnet.
9. **Open-model portability:** different tokenizers, caching semantics and prices (not in the authoritative list, so no cost claim here), plus data-handling questions. *Mitigation:* arm H before any switch; same held-out bar.
10. **Rot:** style-guide or contract edits silently invalidate goldens. *Mitigation:* pack hashes in cards; CI re-validates every golden on edit.
11. **Unvalidated foundation:** nothing is agent-evaluated or rendered on real HyperFrames/Remotion yet; this Mac lacks FFmpeg and Node 22. Week 1 must fix the environment, or every gate number is fiction.
12. **Lens limit:** if arm G misses parity by a wide margin, the next step is distillation or fine-tuning (about 446 demos sufficed elsewhere [N78]; a render-in-the-loop small model reached 94% render success [N68]). The golden bank and run logs are exactly that training set, so none of this work is wasted.

## 9. Six-week rollout

**Week 1: foundation and freeze.**
- Install Node 22 and FFmpeg; pass `preflight.sh`; render the template scene on HyperFrames (Remotion benchmark in parallel).
- Freeze ES-40, the 12-archetype taxonomy, the rubric, the promotion thresholds and the JSONL run schema.
- Build the cost ledger and the prompt assembler with the 60K hard cap.
- Exit: one scene renders deterministically end to end.

**Week 2: strong-model arms.**
- Run arms A, B and C on the 24 exemplar-pool scenes (3 samples, hard token caps).
- Capture DECISIONS blocks; human-score everything blind.
- Decide whether Fable is needed or Opus high suffices as author.
- Exit: about 40 candidate goldens, a cost and time table per arm.

**Week 3: baselines and the negative bank.**
- Run arms D and E on all 40 scenes; cluster failures into a taxonomy.
- Write negative cards from real failures and draft the rulebook, with every rule mapped to a detector.
- Add the missing detectors (overflow, shaping, fixture hash, string ⊂ brief).
- Exit: rulebook v1 and verifier suite v1.

**Week 4: scene packs.**
- Author 12 packs (slot schema, skeleton, rules, checklist, 2 goldens + 1 negative, ≥3 evals).
- Run arm F then arm G on the held-out 16; iterate on packs (not docs) for 2 cycles.
- Exit: arm-G pass rate, escalation rate and rubric deltas recorded.

**Week 5: pilot lessons.**
- Produce the 3 pilot lessons and 6 Reels end to end with the cheap system (Batch + 1-hour cache), with an Opus-high shadow for comparison.
- Measure real tokens, attempts, escalation, wall time and **human review minutes**.
- Optional arm H with one open model.
- Exit: measured cost per lesson and Reel replaces the §7 hypotheses.

**Week 6: decision and hardening.**
- Go/no-go against the promotion criteria. If go: production SOP, drift shadow, weekly card intake from escalations, pack versioning CI.
- If no-go: identify failing archetypes, keep Opus on those only, and open a distillation track using the bank.
- Publish the measured cost model back into `08_cost_models/`.

