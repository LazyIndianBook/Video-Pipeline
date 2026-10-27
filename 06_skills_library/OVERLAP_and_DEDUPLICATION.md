# Overlap and deduplication across the three packs

The three packs were authored at different times. The Super Teacher kit (ST, msg 08) came first, then the Video Engine (VE, msg 10), then the Narration sidecar (NA, msg 12). Because of that, several capabilities exist two or three times under similar names. The governing rule is **"One Skill owns each output … Do not have three agents independently rewrite the narration"** (msg 10 §6).

**How each overlap is resolved:**
- **AUTHORITATIVE** means `backlogs/existing_engine_skill_mapping.json` settles it. That file assigns all 15 NA Skills to 8 VE parents, and says nothing about the ST pack.
- **PROPOSAL** means the mapping is silent and this library suggests a canonical owner. Treat every proposal as a recommendation for the project owner to confirm.

**The default rule (PROPOSAL).** Inside the engine pipeline, the VE Skill is the stage owner and the mapped NA Skill authors the specific sub-artifact. ST Skills do not author engine artifacts. Their distinctive rules are folded into the owner's review checklist, and ST stays a standalone kit for script-only work outside the engine.

`SKILLS_MATRIX.csv` columns `engine_counterpart` and `counterpart_basis` record the same decisions row by row.

## Summary

| # | Overlap cluster | Members (prefix `examleaf-` omitted) | Canonical owner(s) | Basis |
|---|---|---|---|---|
| 1 | Script authoring | VE super-teacher · NA super-teacher-scriptwriter · NA dialogue-naturalizer · ST conversational-script · ST lesson-architect | Draft: **super-teacher-scriptwriter**. Wording diff: **dialogue-naturalizer**. Stage: super-teacher. Lesson scope: **VE lesson-plan** | Mapping (VE↔NA); ST PROPOSAL |
| 2 | Voice direction | VE voice-direction · ST voice-director · NA voice-acting-director · NA pacing-controller · NA stem-pronunciation | **voice-acting-director** (delivery), **pacing-controller** (timing), **stem-pronunciation** (readings). Stage: voice-direction | Mapping; ST PROPOSAL |
| 3 | Interaction | VE interaction-design · ST interaction-designer · NA interactive-teaching-director · NA student-psychology-director | **interactive-teaching-director** (prompts/holds/hidden answers). Stage: interaction-design | Mapping; ST PROPOSAL |
| 4 | Analogy & humour | VE analogy-humour · ST analogy-auditor · ST concept-humour · NA educational-storytelling · NA humour-meme-director | **educational-storytelling** (analogy cards), **humour-meme-director** (jokes). Stage: analogy-humour | Mapping; ST PROPOSAL |
| 5 | Science review | ST science-reviewer · VE science-math/-physics/-chemistry/-biology | **science-<subject>** (typed validation + ScienceReport). **ST science-reviewer** kept as independent cross-subject re-solver | Msg 12 §5 (engine science stays authority); ST role PROPOSAL |
| 6 | Review / evaluation | ST script-evaluator · NA narration-quality-reviewer · VE release-review (+ audio-caption-qa, learning-evaluation) | Different outputs: script regressions → **script-evaluator**. Audio defects → **narration-quality-reviewer**. Release decision → **release-review**. Learner studies → **learning-evaluation** | Mapping (NA→audio-caption-qa); rest PROPOSAL |
| 7 | Language | ST language-editor · VE alignment-localize · NA multilingual-director | Localized text: **multilingual-director**. Localized SceneSpec and labels: **alignment-localize** | Mapping; ST PROPOSAL |
| 8 | Confidence / psychology | ST confidence-editor · NA student-psychology-director (· VE super-teacher acceptance) | **student-psychology-director** | Mapping (via interaction-design); ST PROPOSAL |
| 9 | Captions & timing | NA speech-animation-synchronizer · VE alignment-localize · VE audio-caption-qa · VE render-batch · VE web-composition | Timed captions: **speech-animation-synchronizer**. Corrections: **audio-caption-qa**. Packaging only: render-batch / web-composition | PROPOSAL (mapping covers only the first two pairs) |
| 10 | Answer keys & claims | VE claim-research · VE interaction-design · ST lesson-architect · ST interaction-designer · ST science-reviewer | Canonical keys and claims: **claim-research**. Others reference IDs. Independent re-solve: ST science-reviewer | PROPOSAL |
| 11 | Pacing / duration | VE lesson-plan (600 s plan) · NA pacing-controller · ST voice-director | Planned: **lesson-plan**. Measured: **pacing-controller** | PROPOSAL |
| 12 | Cost & regeneration | VE observability-cost · NA cost-regeneration-optimizer | Pipeline ledger: **observability-cost**. Narration jobs: **cost-regeneration-optimizer** | Mapping |
| 13 | Audio mastering | VE audio-caption-qa · NA audio-production-engineer | Master: **audio-production-engineer** | Mapping |
| 14 | Repetition ledger | ST script-evaluator · ST conversational-script · NA dialogue-naturalizer · VE super-teacher (input) | **No owner exists (gap)**. Proposal: script-evaluator owns the ledger, and the others read it | PROPOSAL |
| 15 | Generated media | VE thumbnail-package (optional image service) · VE selective-generation | Paid generation: **selective-generation** | PROPOSAL |

---

## 1. Script authoring

| Skill | Inputs → outputs | Distinctive rules |
|---|---|---|
| VE super-teacher | LessonPlan + claims + prior-script ledger → spoken script separate from display text and directions | Begin with a genuine question; no genius/easy/guaranteed-marks language; return missing prerequisites |
| NA super-teacher-scriptwriter | Approved LessonPlan, claim IDs, prerequisites, independent answer key → NarrationPlan draft + change log | State capability; one prerequisite repair; fade support; end with an independent task; reject fabricated teacher biography |
| NA dialogue-naturalizer | Draft + claim-preservation list → minimal wording diff | Never delete *not*, increase/decrease, conditions, negative exponents; check the last 20 scripts for boilerplate |
| ST conversational-script | Lesson brief, claim ledger, answer keys, analogy cards, recent-script ledger → script.md, beat_plan.json, change_log.md | Offer alternative openings, choose one and justify it; exact exam terminology after the plain-language version; no audible student or fake hearing |
| ST lesson-architect | Source packet + learner baseline → lesson_brief.md, claims.json, assessment_key.md | Write the assessment before the hook; list what is out of scope; scope down rather than invent |

**AUTHORITATIVE:** `examleaf-super-teacher` → [`super-teacher-scriptwriter`, `dialogue-naturalizer`].

**PROPOSAL:**
- The narration draft is authored **once**, by super-teacher-scriptwriter, and then minimally edited by dialogue-naturalizer.
- VE super-teacher remains the engine stage contract and does not run as a parallel author.
- ST conversational-script is used only in the standalone ST kit. Its "alternative openings" and "terminology after explanation" rules join the scriptwriter's review checklist.
- ST lesson-architect overlaps **VE lesson-plan** (scope, worked → faded → independent, planned rather than measured timing) and **VE claim-research** (claims.json). Inside the engine, lesson-plan owns the plan and claim-research owns claims. Lesson-architect's "assessment before hook" and "out-of-scope list" rules join lesson-plan's checklist.

## 2. Voice direction

| Skill | Inputs → outputs | Distinctive rules |
|---|---|---|
| VE voice-direction | Approved script + lexicon → plain spoken segments, editorial tags, pronunciation map | Five tones: steady, curious, deliberate, light, reassuring; pedagogical silence outside TTS |
| ST voice-director | Script, lexicon, provider capabilities, scene IDs → narration.txt, performance.json, pronunciation_review.md | Unknown controls must fail validation rather than be spoken; exact waits belong to the renderer; no fake gasps |
| NA voice-acting-director | VoiceIdentity + approved narration → direction records, emphasis, audition list | Vary delivery at semantic boundaries; no artificial ums, deliberate errors or forced laughter |
| NA pacing-controller | Segment text, concepts, actual durations → duration report, hold schedule | Never auto-speed equations to force ten minutes |
| NA stem-pronunciation | Formula AST, locale, glossary → versioned spoken/display/caption mappings | Inverse sine is not reciprocal sine; distinguish mA/MA; never merge molarity and molality |

**AUTHORITATIVE:** `examleaf-voice-direction` → [`voice-acting-director`, `pacing-controller`, `stem-pronunciation`].

**PROPOSAL:**
- ST voice-director is not installed alongside these (its name is close to `voice-direction`).
- Its "unknown controls fail validation" rule belongs to **NA tts-provider-adapter**, which already says "reject unsupported SSML".
- Its "native-language pronunciation audition" belongs to stem-pronunciation.

## 3. Interaction

| Skill | Inputs → outputs | Distinctive rules |
|---|---|---|
| VE interaction-design | Target task + script → Cue[], answer-hidden periods, hints and answer keys | A question can never have `answer_visible=true`; cues must be contiguous |
| ST interaction-designer | Objectives, script, answer keys, player type → interactions.json, timing_changes.md | Each prompt carries expected_answer, acceptable_variations, hint, reveal_trigger, retry; rhetorical vs real prompts; stop narration during tasks |
| NA interactive-teaching-director | Question bank, segments → Q/A segments with dependency IDs and Pause nodes | Exact static hold plus optional user pause; no silence is synthesized as paid audio |
| NA student-psychology-director | Objectives, questions, misconceptions, keys → support progression, feedback | Never an unconditional "You got it right" in a prerecorded lesson |

**AUTHORITATIVE:** `examleaf-interaction-design` → [`student-psychology-director`, `interactive-teaching-director`].

**PROPOSAL:** ST interaction-designer's prompt schema (expected_answer, acceptable_variations, reveal_trigger, retry) is the most complete, so adopt it as the field list for interactive-teaching-director's output. Do not install `interaction-designer` next to `interaction-design`.

## 4. Analogy and humour

| Skill | Output | Distinctive rules |
|---|---|---|
| VE analogy-humour | Analogy mapping/limit cards; optional jokes | Reject "electrons want/are lazy" as causes; zero jokes is valid |
| ST analogy-auditor | analogy_cards.json, rejected_analogies.md | Compare at least two candidates, including *no analogy*; the learner restates the relation without the story |
| ST concept-humour | humour_candidates.json, chosen_edits.md | At most 3 candidates plus a no-joke option; record literal_science_risk and translation_risk; never place a joke over the first dense derivation |
| NA educational-storytelling | Mapping, boundary, return-to-science line | One predictive question per analogy; no human intentions as causes |
| NA humour-meme-director | Up to a few removable lines | Reject mocking caste, gender, accent, economic status; no unlicensed reaction clips |

**AUTHORITATIVE:** `examleaf-analogy-humour` → [`educational-storytelling`, `humour-meme-director`].

**PROPOSAL:** The ST card fields become the required output fields of the NA owners:
- From analogy-auditor: target_relation, familiar_relation, mapping, non_mapping, likely_misconception, formal_return, learner_check.
- From concept-humour: concept_anchor, comedic_mechanism, literal_science_risk, translation_risk.

The ST Skills then serve as review lenses only.

## 5. Science review

The VE science-* Skills are per-subject, typed and partly deterministic. Each has a tested helper in its own domain:
- math: chain-rule validator
- physics: RC model check
- chemistry: H2/O2/H2O count check
- biology: Aa×Aa probability check

ST science-reviewer is a *cross-subject, independent re-solve* of the finished script. It checks the literal implications of humour and analogies, checks intermediate states, rates findings critical/major/minor, and never lets an aggregate score pass a critical error.

These are **complementary, not duplicates**. Message 12 §5 makes the engine science reviewers the authority on explanation and answer key.

**PROPOSAL:** Keep ST science-reviewer as the independent reviewer that fills v1 #16 `independent-review`, which has no VE owner. Its condition (also from v1 §6) is that it is run by a different agent/model than the author and that disagreements escalate to the human academic lead. "Two models agreeing is not scientific validation."

## 6. Review and evaluation

| Skill | What it judges | Output |
|---|---|---|
| ST script-evaluator | Script regressions, repetition, naturalness, learner actions; designs learner experiments | release_review.md, regression_report.json, experiment_plan.md |
| NA narration-quality-reviewer | Audio vs transcript, critical words, signal, cue moments | Severity-ranked issues + hash-bound evidence |
| VE release-review | Approvals bound to artifact hashes; rights, language, syllabus | Release manifest or blockers |
| VE audio-caption-qa / visual-qa | Media and frames | QA reports |
| VE learning-evaluation | Actual learning | Pilot plan and results |

**AUTHORITATIVE:** narration-quality-reviewer is a delegate of audio-caption-qa.

**PROPOSAL:**
- The outputs differ, so all are kept.
- ST script-evaluator's file is named `release_review.md`, which collides with VE release-review. Rename that output to a *script-stage pre-review*: it feeds release-review and never replaces it.
- Its `experiment_plan.md` feeds learning-evaluation.

## 7. Language

**AUTHORITATIVE:** `examleaf-alignment-localize` → [`speech-animation-synchronizer`, `multilingual-director`].

**PROPOSAL:**
- multilingual-director owns localized *text*, the back-check and native-review issues. It runs **before** voice direction for each locale.
- alignment-localize owns the localized SceneSpec and label reflow.
- ST language-editor contributes its rules: no demographic language assumptions, code-switch only at meaningful boundaries, translate the *function* of humour, `terminology.csv`. It does not author a second translation.
- NA adds "do not substitute Bengali for Assamese".

## 8. Confidence and student psychology

ST confidence-editor rewrites feedback as observed or conditional success, then a specific issue, then a next step. It removes "easy/obvious" and score promises. NA student-psychology-director separates followed-with-support from independent performance and rejects unconditional praise. VE super-teacher's acceptance test bans "genius/easy/guaranteed marks".

**PROPOSAL:** **student-psychology-director** owns feedback and progress text. Confidence-editor's error taxonomy becomes its checklist: arithmetic, representation, strategy, terminology, prerequisite.

## 9. Captions and timing

Captions appear in five places:
- speech-animation-synchronizer: "captions, protected holds"
- alignment-localize: word/event timings
- audio-caption-qa: "corrected VTT"
- render-batch: "MP4/VTT/manifest"
- web-composition: "insert pauses and captions"

**PROPOSAL:**
- **speech-animation-synchronizer** authors caption timing from the measured sample-index timeline.
- **audio-caption-qa** issues corrections. Per its fallback, it "return[s] to narration source; do not caption an ASR error as correct".
- render-batch and web-composition only *package* and *place* captions; they never re-author them.

## 10. Answer keys and claims

Answer keys appear in claim-research (independent answer keys), interaction-design (hints and answer keys), ST lesson-architect (`assessment_key.md`), ST interaction-designer (`expected_answer`) and ST science-reviewer (`independently_solved_answers.md`).

**PROPOSAL:** **claim-research** owns the canonical keys and Claim[] list. Interaction Skills reference them by ID. ST science-reviewer's re-solve is a *comparison* artifact and is deliberately independent.

## 11–15. Smaller overlaps

- **Pacing (PROPOSAL).** lesson-plan owns the *planned* 600 s. pacing-controller owns the *measured* durations and hold schedule. ST voice-director's "measure generated audio; edit wording instead of speeding" is the same rule pacing-controller applies.
- **Cost (AUTHORITATIVE).** observability-cost → cost-regeneration-optimizer.
- **Mastering (AUTHORITATIVE).** audio-caption-qa → audio-production-engineer.
- **Repetition ledger (gap).** Four Skills read or check a "recent/prior/last-20 scripts" ledger, but none owns it. Proposal: ST script-evaluator maintains it as data; the others consume it.
- **Generated media (PROPOSAL).** thumbnail-package's "optional reviewed image service" goes through selective-generation, so there is one owner of paid generation, the cost reservation and job persistence.

## Installation hazards (near-duplicate names)

Do not activate both members of these pairs as authors. Trigger descriptions are generic enough that a client may pick the wrong one.

| Pair | Pack | Recommendation |
|---|---|---|
| `examleaf-interaction-design` / `examleaf-interaction-designer` | VE / ST | Engine: install VE (+ NA delegates). Standalone script kit: install ST |
| `examleaf-voice-direction` / `examleaf-voice-director` | VE / ST | Same as above |
| `examleaf-super-teacher` / `examleaf-super-teacher-scriptwriter` | VE / NA | Both may be installed: VE is the stage entry and NA authors. Ensure only the scriptwriter writes the draft |
| `examleaf-science-reviewer` / `examleaf-science-*` | ST / VE | Complementary. Run them as different agents |

No two folders share an exact name; all 57 are unique.


## Addendum (15 Oct 2026): the 15 advanced-animation skills

Ownership resolutions (decisions AD-34…AD-40 in `../12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`):

| Cluster | Owner of the output | Extender / guard | Rule |
|---|---|---|---|
| Storyboard routing vs storyboard gate | `examleaf-storyboard-route` (routing tags) | `examleaf-anim-storyboard-gate` (3×3 grid, estimate.json, approval record) | The gate never re-routes. |
| Composition vs harness conformance | `examleaf-web-composition` (composed video) | `examleaf-motion-harness` (contract lint, determinism hash) | Harness proves; composition composes. |
| Word timings vs cue sheet | `examleaf-speech-animation-synchronizer` / `examleaf-alignment-localize` (alignment, captions) | `examleaf-cue-sheet` (merged cue sheet JSON) | Cue sheet reads cue frames; never re-aligns. |
| Cost ledger vs effort policy | `examleaf-observability-cost` (money ledger) | `examleaf-effort-governor` (model/effort/iteration policy, effective-level log); `examleaf-mcp-orchestrator` (credit sub-ledger) | Sub-ledgers report into the money ledger. |
| Paid generation | `examleaf-selective-generation` (decision to spend) | `examleaf-mcp-orchestrator` (MCP permissions, estimate-before-call, idempotent jobs, reconciliation) | AD-34. |
| Visual/audio QA vs animation QA | `examleaf-visual-qa`, `examleaf-audio-caption-qa` (verdicts) | `examleaf-anim-qa` (safe zones, hold times, flash, determinism, fixture-text diff, Indic glyphs) | `audio-caption-qa` cites `anim-qa`'s measurements rather than issuing a second loudness verdict. |
| 3D molecules | `examleaf-molecule-scenes` | `examleaf-threejs-scenes` (orbitals, lattices, fields, waves, voxels) | Molecules never move to three.js. |
| Brand colours vs style tokens | `examleaf-asset-library` (brand kit) | `examleaf-style-guides` (style tokens, five house styles) | Proposed subject colours wait for brand approval (AD-39). |
| Mastering vs composed beds | `examleaf-audio-production-engineer` (master) | `examleaf-audio-compose` (stems + SFX), `examleaf-audio-analysis` (beat grid) | Loudness is measured once, at the master. |
| Reel recomposition vs vertical layout | `examleaf-reel-repurpose` (ShortSpec, recut) | `examleaf-vertical-adapt` (zone rectangles, 16:9→9:16 rules, sub-range re-seek) | Reel repurpose calls vertical-adapt for geometry. |
| Data-bound text vs kinetic type | `examleaf-svg-scenes` / `examleaf-manim-scenes` (labels, equations from fixtures) | `examleaf-kinetic-typography` (titles, hooks, callouts timed to narration) | Kinetic type never renders a science glyph that is not a fixture field. |
| Scene authoring 2D | `examleaf-svg-scenes` (validated diagrams) | `examleaf-procedural-2d` (doodle/collage primitives for illustrative scenes) | Illustrative only; never axes or values. |
| Brief assembly | `examleaf-storyboard-route` + `examleaf-pacing-controller` (inputs) | `examleaf-anim-brief` (brief.md + constraints block), `examleaf-reference-analyzer` (measured reference numbers) | The brief never alters approved script text. |

Near-name hazards added: `examleaf-anim-qa` vs `examleaf-visual-qa`; `examleaf-cue-sheet` vs `examleaf-speech-animation-synchronizer`. Activate the owner and the extender together, never the extender alone.


## Addendum (15 Oct 2026): Section 13 registration (Production Kit fill skills and templates)

Source: `../13_strong_to_cheap_model_strategy/STRATEGY_strong_to_cheap_models.md` §4.1, §4.6 and D-21; audit finding cross-section-consistency-7 in `../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`. The eight `examleaf-fill-<archetype>` skills and the Kit `templates/` are **PROPOSED, not built**. They are not in `SKILLS_MATRIX.csv`.

| Cluster | Owner of the output | Extender | Rule |
|---|---|---|---|
| Kit template conformance | `examleaf-motion-harness` (contract, lint, determinism hash) | `examleaf-fill-<archetype>` (slot JSON only) | A template that fails the contract is not a Kit template. Fill skills never write scene code. |
| Style slots | `examleaf-style-guides` (tokens, five house styles) | `examleaf-fill-<archetype>` | Slot schemas carry no colours, sizes or fonts; style comes from tokens. |
| Brief | `examleaf-anim-brief` (brief.md + constraints block) | `examleaf-fill-<archetype>` | The fill call consumes the brief; it never alters approved script text (`text_ref` only). |
| Template promotion | `examleaf-procedural-2d` / `examleaf-kinetic-typography` (12 AD-23: illustrative and text layers) | Section 13 Kit build (arm B) | One template library, not two. Kit templates are promoted through the AD-23 owners. |
| Fixture-visual and symbolic scenes | `examleaf-svg-scenes` / `examleaf-manim-scenes` | `examleaf-fill-<archetype>` (slot spec for the adapter) | Fixture-visual archetypes are not re-implemented as HyperFrames templates. Symbolic archetypes go to these adapters where an approved SVG/Manim template exists [Recommendation] (STRATEGY §2.3). |
| Kit verifiers | `examleaf-anim-qa` (A4–A7, A14) and `examleaf-motion-harness` (A1, A3) | Section 13 V0–V8 | V2/V4/V5 extend the existing scripts. V0–V8 run in addition to A1–A17, never instead. |
| Cascade effort and caps | `examleaf-effort-governor` | Proposed `kit_cascade` family (STRATEGY D-16) | No cheap-model Kit run before the family exists. Ultracode is refused in production. |

Near-name hazard to watch once built: `examleaf-fill-<archetype>` vs the scene-authoring owners above. Activate a fill skill only with its owners.
