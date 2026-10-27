# 13 · Strong-to-cheap model strategy (Fable / Opus experiments → Haiku-class production)

**The question (15 Oct 2026):** should ExamLeaf make the first videos, timelines and experiments with strong models (Fable 5.1, Opus 5.5 at high/max, possibly ultracode), document everything in depth (guides, ways of preparing, edge cases, restrictions, learnings), so that cheaper models (Haiku 5.5, Chinese/open models) can then produce videos of similar quality at 40–100× lower cost without getting "crappy"? What is the proper way?

**The answer in one paragraph.** Yes, run the strong-model experiments first, but aim them at building a *Production Kit* (parameterised scene templates with strict slot schemas, deterministic verifiers with actionable error messages, a failure catalogue linked to the check that detects each failure, golden and negative exemplars, one short skill per scene archetype, a sealed eval set), not at writing a manual for Haiku to read. The cheap model then only fills slots; work advances only on verifier verdicts, never on the model's own claim of being done; failures climb a cascade (Haiku → Haiku at higher effort → Sonnet → Opus → human). Every human gate stays, in this order: GA (academic, on the script-bundle hash) → H-SB storyboard gate → TTS → cascade → A-suite → GF. Every Reel gets its own GS and never inherits approval (corrected 15 Oct 2026). The 40–100× ratio is real per call (Haiku is 38× cheaper than Opus 5.5 and 94× cheaper than Fable 5.1) but, like for like on the same Kit, the LLM line per lesson drops about 19× if Haiku passes everything and about 5× for the protected cascade. **Update (15 Oct 2026): the founder has set human review to $0 (done in-house).** With review free, the per-lesson total is LLM line + a non-LLM floor (narration, clips, stills, render, alignment, storage). *Corrected 15 Oct 2026, all [Hypothesis] and unmetered:*
- **Baseline.** On one price basis (5.5 tariffs; today's LLM line $1.214, not the 4.6-era $1.716) and with generated clips at $0 per RD-39, the cascade is only about **4% below today's pipeline** ($3.17 → $3.04).
- **Against an Opus-only Kit** the cascade is about 60% cheaper ($7.58 → $3.04).
- **Against bespoke [V1]-low strong-model generation** the total drops 4.5–8.1×.
- **At the lean floor.** With cheap TTS, owned render hardware and no generated clips, the best the tables support is ≈7× against an Opus-only Kit and 14–27× against bespoke [V1]-low. The TTS price doubles on 1 Jan 2027, which makes these ≈6.2× and 12–23×.
- **40–100×** appears only against [V1]-max bespoke runs.
- **Path B only.** The lean floor applies to TTS content (Reels, recaps). Full lessons are Path A under the playbook: teacher performance plus speech-to-speech plus cutaways, a floor of ≈$1.67–2.22 plus performer time (§7.14).

Review is free in cash but not in capacity (85 min/lesson ≈ 8.85 full-time months per 1,000 lessons; Path A adds ≈45 performer minutes, ≈13.5 months, and storyboard-review minutes are still unmeasured), so the verifier QA report remains the throughput lever. Full arithmetic in `STRATEGY_strong_to_cheap_models.md` §7.13 and §7.14. Every ratio is unmetered until the week-1 meters exist.

## Files

| File | What it is |
|---|---|
| `STRATEGY_strong_to_cheap_models.md` | The in-depth strategy (≈17,400 words by `wc -w` after the 15 Oct 2026 audit corrections; ≈13,500 before them): executive answer; why documentation alone cannot distil Opus into Haiku and the five transfer mechanisms that can; target architecture; the strong-model experiment programme; the artefacts to produce (guide, restrictions, edge-case register, learnings ledger, exemplar bank, scene DSL/templates, verifier suite, capability ledger); cheap-model operating procedure; evals and the parity definition; the cost model with explicit arithmetic; Chinese and open models; risks and what not to do; 6-week rollout with gates; decisions and open questions; appendix mapping the critic's must-fix items |
| `EXPERIMENT_PROTOCOL_strong_model_campaign.md` | The runbook for the strong-model campaign: fixed scene set, model × effort × prompt-tier × harness matrix, exact settings per run, capture templates for the "timeline", blind review, trace-mining procedure, exit criteria, budget (≈$810 itemised, $1,000 LLM cap, ≈54 rater-hours) |
| `DOCUMENTATION_TEMPLATES.md` | Fill-in templates with required fields and an example row for: Guide, Restrictions, Edge-case register entry, Learnings ledger entry, Exemplar card, Capability ledger row, Verifier spec, Experiment record |
| `SOURCES_and_claims.md` | Every [N#] claim behind the strategy with quote, URL and verification status |
| `architect_plans/PLAN_1…4_*.md` | The four independent Opus 5.5 architect plans (library-and-DSL-first; verifier-and-cascade-first; exemplar-and-prompt-first; economics-and-ops-first), each ≈4,000 words with its own cost arithmetic |
| `judges_and_critic/JUDGES_and_CRITIC.md` | Three Sonnet 5.5 judges' verdicts (two chose verifier-and-cascade-first, one economics-and-ops-first) and the Opus 5.5 completeness critic's 12 must-fix items that the final strategy addresses |

## How it was produced

Fable 5.1 (lead) loaded the Claude API reference for authoritative prices (Fable 5.1 $10/$50, Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 $0.10/$0.50 per million tokens; batch 50% off; cache reads $0.25 / $0.20 / $0.20 / $0.01, i.e. 2.5–10% of input price), then ran a research-plus-judge-panel workflow (44 agents):

| Phase | Agents | Result |
|---|---|---|
| Research, 6 angles (cheap-model landscape incl. DeepSeek/Qwen/Kimi/GLM; small-model reliability techniques; cascades and routing; distilling workflows into skills; automatic video-quality evaluation; frontier-to-small case studies) | 6 Sonnet | 61 unique sources |
| Fetch, extract and two-lens adversarial verification | 8 + 20 Sonnet | 24 sources read, 158 claims, 96 of 100 verified claims survived |
| Design: four architects, one lens each | 4 Opus | four complete plans |
| Judge panel | 3 Sonnet | scores, best ideas, fatal flaws, winner per judge |
| Synthesis → completeness critic → revision | 3 Opus | the final strategy, protocol and templates |

## Caveats

- Nothing has been metered on ExamLeaf scenes; token counts and attempt rates are assumptions until week 1 of the protocol replaces them.
- The reference experiment's dollars and tokens do not fully reconcile, so the "cheaper than bespoke strong-model generation" range is wide (11–344×).
- Chinese/open-model prices and benchmarks are as published on the research date and must be re-verified before any procurement.
- This Mac still lacks FFmpeg and Node 22, which blocks the first render in the protocol.

## Audit corrections (15 Oct 2026)

Applied against `../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` (§3, §6 item 4 and the section-13 minors). Edits are dated in place.

| Finding | What changed | Where |
|---|---|---|
| M3 Reels skipped their second approval | Reels never inherit approval. LLM-drafted hook/CTA/caption text is new script and goes to GA. Each Reel gets its own H-SB, the full A-suite and GS, bound to the Reel's hash by two identities. A deterministic cut-down may shorten review (approved claim IDs carry over) but removes no gate | STRATEGY §5.7, §2.2, §7.5, D-11; PROTOCOL §2.4; PLAN_4 banner |
| M4 academic approval after rendering, no storyboard gate | Diagram redrawn and steps rewritten: GA (bundle hash) → H-SB → TTS → cascade → A-suite → GF, with GS for Reels | STRATEGY §2.1, §5.5, V8, D-18 |
| M12 verifier stack | V2 = existing `text_fixture_diff.py`; V4 = existing `safe_zone_check.py` (extend, not "New"). V5 uses the contract rule (reveal at word t0 or up to 0.05 s before; late = fail), with ±150 ms as a quality metric only. V3 adds the reverse-order render (AD-21). V0–V8 run in addition to 12/10 A1–A17 and 07/06 (answer-hidden window, flash, licences, loudness, captions). Fixture-visual archetypes route to the existing SVG/Manim adapters | STRATEGY §2.3, §2.4, §3.2, D-19; TEMPLATES V5 example; PLAN_2 banner |
| Cost framing (section-13 minors) | Today re-priced at 5.5 tariffs ($1.214) and shown next to the old $1.716. Clips-$0 (RD-39) is the baseline. Lean-floor TTS is $0.14 now and $0.28 from 1 Jan 2027, with both ratio sets shown. "40–100× at the lean floor" is corrected to ≈7× / 14–27× (40–100× only vs [V1]-max). Open models are now 5–33% of the D2 total. "Upper bound" is renamed "token-based floor". The batched cascade is $0.71–0.80. The S-arm budget is $435, as in the protocol. $2,317 is labelled "at the $1,000 cap". Cache reads are 2.5–10%. Approximations are recomputed. A Path A row is added and the lean floor scoped to Path B | STRATEGY §0, §7.1–§7.13, new §7.14, D-20; PROTOCOL §5 item 7 (10 shadow pairs) |
| Effort/ultracode | D-16 scopes AD-02/AD-11/AD-24 to the strong-model phase and defines a `kit_cascade` family with its own caps. This is text only; the `effort_policy.py` change is owned by section 12, and no Kit run starts before it. D-9 makes S5 an attended, founder-approved exception with a provider-side $50 limit that can never enable ultracode in production. D-17 states the per-surface effort defaults once | STRATEGY §5.8, §3.3, §9.2, D-9, D-16, D-17; PROTOCOL §0 item 9, §2.1, §2.2 |
| Section 13 not registered | The eight `examleaf-fill-<archetype>` skills and `templates/` are PROPOSED, not built. Owners: `examleaf-motion-harness` (contract), `examleaf-style-guides` (style slots), `examleaf-anim-brief` (brief) | D-21; `../06_skills_library/README.md` and `OVERLAP_and_DEDUPLICATION.md` addenda |

**Not changed here (owned elsewhere):**
- The `kit_cascade` code in `effort_policy.py`, the matching AD row in 12/14 and 12 edge case #3 (ultracode in sandbox) belong to section 12.
- The 07/10 addendum and 07/README row registering section 13 belong to section 07.
- RD-04's verified-price update belongs to section 07.
