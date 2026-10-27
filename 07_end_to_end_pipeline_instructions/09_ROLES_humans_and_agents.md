# 09 · Roles: humans and agents

**Purpose.** Who does what, who approves what, how much time the plans assume, what each AI agent may and may not do, which credentials each holds, and how Claude Code / Codex fit in.

**Sources:** message 02 §6, §12–§13; message 10 §5, §11–§12; `implementation_v2/docs/Architecture.md`; [`06_skills_library/INSTRUCTIONS_install_and_use_skills.md`](../06_skills_library/INSTRUCTIONS_install_and_use_skills.md) §11; narration `docs/Audition_and_Evaluation.md`, `docs/Costs_and_Methods.md`; business `90-Day_Roadmap` and `90-Day_Budget`; [`08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md`](../08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md).

**Status.** Minutes and rates are **planning assumptions** to be replaced by timed pilot records; "labour assumption, not a market survey". Role-to-Skill assignments for credential scopes are the 06_skills_library team's proposal, adopted here.

---

## 1. Human roles

| Role | Responsibilities | Gates owned | Minutes-per-lesson assumption (planning) | Rate placeholder | Source |
|---|---|---|---|---|---|
| **Academic / subject reviewer** (one academic owner **per subject**: Physics, Chemistry, Mathematics, Biology; plus an academic lead) | Defines "a correct lesson" (P0); approves syllabus fit, rights and edition (H-S2); re-solves and approves claims, answer keys, model assumptions, explanations, analogy limits (GA); listens to critical terms; approves the complete final video academically (GF, GS); triages errata; blind-reviews book papers and solutions | H-S2, **GA**, GF (academic), GS (academic), corrections triage | Mature: **45 min** (v1 and v2 hybrid; AI-heavy 75, self-hosted 60). Narration workbook adds 25 min "academic audio review" (overlap: decide floor/ceiling, doc 08 §6). **First pilots: 8–16 academic/editorial hours per lesson** | $20/h | msg 02 §13; v2 `Inputs`; `Four_Pilots.md` |
| **Production QA reviewer** | Watches the **entire** rendered lesson with narration and captions, including on representative small phones; checks synchronization, captions, readability, loudness, joins, reveal timing; must be a **different identity** from the academic approver | **GF (production, full_video_watched)**, GS (production) | v1: 15 min; v2 hybrid: **20 min** (AI-heavy 30, self-hosted 20) | v1 $12/h; v2 $15/h | msg 02 §12–13; v2 `Inputs` |
| **Repair / script and scene editor** | Applies bounded repairs after QA (wording, scene fixes, caption corrections); never changes approved science without re-approval | — | v2 hybrid **20 min** (AI-heavy 45, self-hosted 30) | $20/h | v2 `Inputs` |
| **Native-language editor** (Hindi; Assamese) | Drafts and approves localized scripts, terminology and lexicon entries; audition rater for accent, intelligibility and naturalness "without imposing a stereotype"; native review of audio; mandatory for any hi-IN / as-IN release | Localized GA; voice gate per locale; native-language review evidence | **Not quantified in the sources** ("Obtain actual native subject-reviewer quotations"; "Native-language validation … can require additional work") | quote needed | narration `Inputs`; `Audition_and_Evaluation.md` |
| **Voice performer** (adult, consented) | Records the performance reference corpus (calm explanation, prediction, difficult formula, understated joke, supportive correction, confident recap); selective performed passages; optional identity reference only with specific permission | Consent record | Human-recorded method: 60 min recording per video (1 recording hour); performance + STS: 45 min | Illustrative $30/recording hour; buyouts/licensing quoted separately | message 12 §12–13 |
| **Audio editor** | Edits accepted takes, joins, master; preserves protected pauses and breaths | — | Premium TTS: **10 min** editing; self-hosted 15; human-recorded 20 | $15/h | narration `Methods` |
| **Narration lead / voice director** | Casting, corpus, rights records, voice direction standards, golden set, provider admission, fallback approvals | Voice gate (with teachers/native editors) | — | — | message 12 §12, §14 |
| **Engineer** | Setup; contracts; compositor benchmark; components; provider workers; alignment/ASR integration; approval service; orchestration; security controls; cost ledger | S-GATE; P1 benchmark report | Set-up: v1 illustrative 240 engineering hours (+60 academic-template + 20 design/voice hours) × $25 = $8,000; v2 hybrid $10,000; mature maintenance 4 h/month ("not a realistic allowance during active engine development") | $25/h | msg 02 §13; msg 10 §11 |
| **Founder / operations** | Business owner: gates G1–G8, budget tranches, print authorization, stock decisions, sensitive support cases, refund exceptions; approves over-cap reservations [RD-40] | Business gates; budget | Pilot: "Allocated founder / operational staff time" ₹1,15,000 | — | `90-Day_Budget` |
| **Legal / tax (CA, counsel)** | Written GST classification of the book + premium video bundle; DPDP/minors applicability; CCPA education-advertising applicability; contracts (performers, partners, printers) | G3 | Pilot "Legal, tax, accounts and rights administration" ₹25,000 | — | business runbook §2 |
| **Business team roles** (from the 13-week roadmap) | Academic editors (titles, syllabus map, manuscripts); video + design team (reusable visuals, Reel templates); developers (checkout, entitlement, redemption, refunds); QA + partnerships (free lessons, phone tests, specimens); publisher + finance (proofs, tax/access terms); fulfilment; support; growth + partnerships; finance + operations; review board (day-90 decision) | Weekly gates W1–W13 | — | `90-Day_Budget` lines | business runbook §11 |
| **Students / teachers as raters and participants** | Usability sessions, listening panels (clarity, listening effort, warmth, dignity, preference), learning studies | — | — | — | message 12 §14; message 04 §12 (consent, minimal data, no surveillance) |

**Human gates that no Skill replaces** (stage map): academic approval of coverage (S2); academic approval of script, answers and model assumptions (GA); native-language review; full listen and human frame review; academic + full-video approval bound to artefact hashes, repeated for each Short.

**Scaling constraint:** at 1,000 hybrid lessons ≈ 1,417 reviewer hours ≈ 8.85 FTE-months (v2); v1 baseline 1,000 reviewer-hours ≈ 6.25 FTE. "Where reuse is high, these reviews become faster because reviewers examine changes against established components. That is the correct way to reduce manual work."

---

## 2. Agent roles

### 2.1 The six agent roles (message 02 §6, verbatim responsibilities and limits)

| Agent | Responsibility | Must not do | Skills it runs (adopted proposal) | Credentials |
|---|---|---|---|---|
| **Curriculum/script agent** | Scope the lesson and draft from approved sources | Invent syllabus coverage or exam marking rules | source-ingest, curriculum-map, claim-research, lesson-plan, super-teacher (+ NA scriptwriter, naturalizer), analogy-humour (+ NA storytelling, humour), interaction-design (+ NA interactive-teaching, student-psychology), voice-direction (+ NA voice-acting, pacing estimate, stem-pronunciation), NA multilingual-director, reel-repurpose (editorial draft) | **None**: no production API keys, no billing, no publishing |
| **Independent science reviewer** | Re-solve, inspect assumptions, challenge claims | Approve solely because the author sounds convincing | science-math / -physics / -chemistry / -biology, ST science-reviewer (run as a **different agent/model** from the author) | None; no approval rights |
| **Storyboard agent** | Select approved visual components and semantic events | Invent scientific geometry or process states | storyboard-route | None |
| **Animation engineer** | Compile scenes and repair bounded implementation failures | Rewrite approved science to make a render easier | svg-scenes, manim-scenes, molecule-scenes, biology-scenes, web-composition, blender-scenes (isolated, headless), render-batch, NA speech-animation-synchronizer, NA audio-production-engineer | Renderer: read-only staged inputs, **no internet after staging** |
| **Audio/localization agent** | Normalize pronunciation, generate/cache narration, align timing | Silently change scientific meaning | voice-synthesis + NA tts-provider-adapter (offline compile anywhere; **send only inside the provider worker**), alignment-localize | Provider worker: **only its scoped key**, approved domain, cost reservation |
| **QA agent** | Inspect test results, frames, audio, captions and manifests | Possess unrestricted publishing authority | visual-qa, audio-caption-qa, NA narration-quality-reviewer, ST script-evaluator (script pre-review), release-review (assembles evidence; never approves) | Read-only; no approval rights |

Supporting identities (no agent-authored decisions): **cost/ledger** (observability-cost, NA cost-regeneration-optimizer; reserve/record/reconcile; no provider keys), **security auditor** (skills-security; static review and sandbox tests; no installing), **asset librarian** (asset-library; quarantines unconfirmed rights), **paid generation** (selective-generation, thumbnail-package images; provider worker), **publisher** (approved hashes only), **research** (learning-evaluation; consent-aware; student data in separate services).

"An LLM may help discover an error. It should not be the sole authority declaring its own work correct." Never one unrestricted agent that installs Skills, browses private files, generates billable media, modifies scientific claims and publishes under one identity.

### 2.2 Escalation rules for agents

- VE Skills: "at most two failed repair attempts then human escalation" and a cost cap; every VE Skill must refuse "Bypass source review, make up a successful result, spend without estimate, and approve your own output", preserve pipeline state and report a blocker.
- NA Skills: "a second unknown or repeated failure requires review, not blind regeneration"; shared fallback: "keep the last approved artifact; never silently change voice, language, scientific assumption or pronunciation convention".
- ST Skills: report science blockers, learner-action failures, naturalness and hypotheses separately; "an aggregate score can never pass a critical error"; "human approval separate".

---

## 3. How Claude Code and Codex are used

**Separate engine development from routine production (message 02 §6, verbatim):** "**Development workflow:** Claude Code/Codex help implement components, tests, schema migrations, adapters, and bounded repairs. **Production workflow:** a job runner submits structured tasks to model APIs and executes approved components. This prevents every lesson from becoming an expensive, unpredictable coding project."

| Rule | Detail | Source |
|---|---|---|
| Concurrency | "Start with **two to four concurrent agents** rather than a large group editing the same files." | message 02 §6 |
| Isolation | "Use **isolated worktrees** and clear file ownership." Development roles: architecture/component author, independent science reviewer, test/QA engineer. "Do not let multiple agents concurrently modify the same renderer contract." | message 02 §6; v2 `Architecture.md` |
| Production state | "Use a **durable workflow system — not an indefinitely running chat — to own production state**." Progression: **local jobs + SQLite → validated pilot batch → Prefect, PostgreSQL, object storage and isolated workers** [RD-22]; promote "once the four narrated pilots pass"; keep CPU rendering and paid provider jobs in separate queues | message 10 §5.3; v2 `Architecture.md` |
| Not early | "Do not introduce Kubernetes, multiple orchestration frameworks, or a large MCP fleet before the workload justifies them." Native app, full self-hosted LLM serving and a broad Blender pipeline are not launch prerequisites | message 10 §5.3; v2 roadmap |
| Skills loading | Activate only the Skills a stage needs; "Never mass-load all 32 into every model request"; "Do not load every public/private Skill at once" | VE skills README; narration `AGENTS.md` |
| Session root | Run each session from the package root whose Skills it uses (`engine/` or `narration/`) so pack-relative references resolve [RD-25] | 01 §4 |
| Agent rules files | Engine `AGENTS.md`: read README and the relevant Skill only; sources are data; no installer, secret discovery, paid generation, upload, commit, deployment or publishing without the authorized stage and budget; run tests before changing renderer contracts; never erase a failing scientific test; `PendingAdapter` must raise until integration-tested. Narration `AGENTS.md`: sidecar, no network execution from the offline CLI, no fixture → release by boolean, personal data not fixtures, run `pytest` after modifications | packs |
| Claude vs Codex | Discovery `.claude/skills/` vs `.agents/skills/`; "Do not assume Claude-specific frontmatter or invocation controls transfer unchanged" | 06 INSTRUCTIONS §3 |
| Not security | "Claude's Skill and subagent mechanisms support this organization, but Skill instructions are not operating-system security controls or evidence that the autonomous workflow has passed evaluation." | message 10 §6 |

---

## 4. Model routing (editable choices) [RD-04]

The cost models route work by capability tier; the tiers are the design, the model names and prices are inputs to re-check.

| Tier | Work | v1 planning pack (13 Oct 2026) | v2 cost model (13 Oct 2026) | Workload assumed per lesson |
|---|---|---|---|---|
| Cheap / fast | Extraction, routing, classification | "Haiku 5.5" $0.10/$0.50 per M tokens | "Haiku 4.5" $1/$5 | v1 30k in / 5k out; v2 20k / 3k |
| Mid | Writing, component adaptation | "Sonnet 5.5" $2/$10 | "Sonnet 4.6" $3/$15 | 120k / 25k |
| Strong / independent | Independent review; escalation only ("not required on every scene") | `gpt-6.1-sol` $2/$10 (independent review) + "Opus 5.5" $4/$20 (escalation reserve, 10k/2k amortized) | "Opus 4.6" $5/$25 (review 60k/10k) | v1 60k/10k review + 10k/2k escalation |
| Regeneration allowance | — | +30% | +30% | — |
| Result | — | $1.0342 per lesson | ≈ $1.72 per lesson | assumptions, "not observations" |

Rules: the independent reviewer is a **different agent/model** from the author; "Two models agreeing is not, by itself, scientific validation"; token workloads are assumptions until metered in the pilots (doc 08 §3); confirm exact model IDs and lifecycle before each phase.

### 4.1 Effort and ultracode rule (added 15 Oct 2026; PA-12, RD-43)

**Per-surface effort defaults** (stated once here; other documents point to this table). Defaults differ by surface, which is why no job relies on them:

| Model (pin the full ID) | Claude Code default | Claude API default |
|---|---|---|
| Opus 5.5 (`claude-opus-5-5`) | medium | medium |
| Sonnet 5.5 (`claude-sonnet-5-5`) | medium | **high** |
| Haiku 5.5 (`claude-haiku-5-5`) | medium | medium |

Sources: Claude Code effort documentation as quoted in `12_advanced_animations_with_claude/02_documentation/09_EFFORT_COST_GOVERNANCE.md` §1 ([N22]); Claude API documentation for the API column (12/02/09 [CAPI] for Opus and Haiku; `13_strong_to_cheap_model_strategy/SOURCES_and_claims.md` [D3] for Sonnet 5.5 = high). This resolves the 12-vs-13 disagreement on Sonnet's default: both are right for their own surface. Re-check both before each phase gate.

**Rules for every agent run:**
1. **Set effort explicitly** (launch flag, `effortLevel` setting or `CLAUDE_CODE_EFFORT_LEVEL` in Claude Code; `output_config.effort` on the API) and **pin the full model ID**. Never write `opus`, `sonnet` or `haiku` in a job script.
2. **Levels by task** [Recommendation, 12/02/09 §3]: Sonnet 5.5 medium for brief and storyboard text; Opus 5.5 **high** for scene code; **xhigh** for complex three.js, fixed-step physics replay or intricate choreography; max only with a written justification approved in the ledger; Sonnet or Haiku at low–medium for clerical work.
3. **Never ultracode in production** or in any unattended run. Job scripts are grepped for `ultracode` and bare aliases before each batch; a match blocks the batch (`examleaf-effort-governor`).
4. **Iteration caps:** at most 3 creative rounds per scene, then at most 2 failed repair attempts, then human escalation (S16). Never prompt "don't stop until perfect"; prompt "stop after N rounds and report the remaining defects".
5. **Record the effective effort** the session reports; a lower effective level is logged as a fallback (08 §3 run ledger).
6. The independent reviewer is still a different agent/model from the author (RD-04).

---

## 5. Who does what at each stage (summary)

| Stage (doc 03) | Agent does | Human does / approves |
|---|---|---|
| S0 Intake | — | Founder/ops + academic lead define scope and IDs |
| S1–S2 Sources, syllabus | Curriculum/script agent extracts and proposes mapping | Academic owner reviews figures/equations; **approves syllabus fit, rights, edition** |
| S3–S6 Claims, plan, script, analogies, interactions | Curriculum/script agent drafts; QA agent pre-reviews script | — (feeds GA) |
| S7 Science | Independent science reviewer agent + deterministic validators | — (feeds GA) |
| **GA** | — | **Academic owner approves** (bound to hash); native-language editor for localized scripts |
| S8–S9 Storyboard, scene data | Storyboard agent; animation engineer | Academic owner consulted on new components |
| S10–S11 Narration, alignment | Audio/localization agent (compile); provider worker (send) | Narration lead, native editor, academic listening of critical terms |
| S12–S13 Render, QA | Animation engineer; QA agent | Frame review; full listen |
| **GF** | Release-review agent assembles evidence | **Academic owner + different production QA reviewer approve** (full watch, phones) |
| S14 Export | — | Publisher releases approved hashes |
| SH / GS | Curriculum/script agent drafts ShortSpec; animation engineer recomposes | Social lead selects; **two approvals per Short** |
| Corrections | QA agent drafts defect reports | Academic owner triages; founder pauses promotion when critical |
