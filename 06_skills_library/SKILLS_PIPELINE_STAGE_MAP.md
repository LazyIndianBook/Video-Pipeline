# Skills by pipeline stage: who fires and who owns the output

This file lists, for each pipeline stage, the Skills that fire, the order they fire in, and the **single owner of each output artifact**.

**How ownership was decided:**
- **Authoritative.** `backlogs/existing_engine_skill_mapping.json` says which Narration (NA) Skills each Video Engine (VE) Skill delegates to. Message 12 §5 adds that the engine Super Teacher workflow *delegates* naturalization and delivery preparation, engine science review stays the authority for the explanation and answer key, the renderer receives measured narration events, and release requires audio-specific approval evidence.
- **Proposal (this library).** The VE Skill is the **stage owner**: it is accountable for the stage and emits `templates/handoff.json`. Where the mapping delegates, the NA Skill **authors the specific sub-artifact** named in its contract, and the VE Skill must not re-author it. Super Teacher (ST) Skills are **not run as second authors** inside the engine pipeline. Each one is either a *review lens* or a *standalone alternative* for script-only work outside the engine. Rows marked PROPOSAL are where the mapping file says nothing.
- "Runbook step" is the step number in the VE pack's `docs/Production_Runbook.md`, which is the real execution order. Stages below follow the requested list, so QA appears before render-batch even though the runbook renders first and QAs the rendered output.

Prefix `examleaf-` is omitted. VE = Video Engine, NA = Narration, ST = Super Teacher.

| # | Stage | Runbook step | Fires, in order | Output artifact → **owner** | Basis |
|---|---|---|---|---|---|
| 1 | Source ingest | 1 | VE source-ingest | Native-text JSON + source SHA + flagged pages → **source-ingest** | VE (sole) |
| 2 | Curriculum map | 1 | VE curriculum-map → human academic reviewer approves coverage | Versioned coverage map → **curriculum-map** | VE (sole) |
| 3 | Claim research | 2 | VE claim-research | SourceRef[], Claim[], independent answer keys → **claim-research** | VE (sole). ST lesson-architect also emits `claims.json`, but under the engine pipeline it **consumes** claim-research output (PROPOSAL) |
| 4 | Lesson plan | 2–3 | VE lesson-plan · (ST lesson-architect only if running the ST kit standalone) | LessonPlan + beat schedule + 600 s plan → **lesson-plan**. ST `lesson_brief.md`/`assessment_key.md` are the standalone equivalent | PROPOSAL |
| 5 | Super-teacher script | 3 | VE super-teacher (stage entry) → NA super-teacher-scriptwriter → NA dialogue-naturalizer · review lens: ST conversational-script rules, ST confidence-editor | NarrationPlan draft + change log → **super-teacher-scriptwriter**. Minimal wording diff → **dialogue-naturalizer**. Stage handoff → **super-teacher** | Mapping (authoritative). The ST lens is a PROPOSAL |
| 6 | Analogy / humour | 3 | VE analogy-humour (stage entry) → NA educational-storytelling → NA humour-meme-director · review lens: ST analogy-auditor, ST concept-humour | Analogy mapping/boundary/return line → **educational-storytelling**. Removable humour lines → **humour-meme-director** | Mapping. ST lens PROPOSAL |
| 7 | Interaction design | 3 | VE interaction-design (stage entry) → NA interactive-teaching-director → NA student-psychology-director · review lens: ST interaction-designer, ST confidence-editor | Question/answer segments + Pause nodes + hidden answers → **interactive-teaching-director**. Support progression + feedback text → **student-psychology-director**. Cue[] handoff → **interaction-design** | Mapping. ST lens PROPOSAL |
| 8 | Science validation | 2, 4, 5 | VE science-math / science-physics / science-chemistry / science-biology (whichever the subject needs) → ST science-reviewer as independent cross-subject re-solve → **human academic approval** | ScienceReport + approved typed data → **science-<subject>**. Independent findings → **ST science-reviewer** (fills v1 #16 "independent-review", which has no VE owner) | VE authority confirmed by msg 12 §5. ST role PROPOSAL |
| 9 | Storyboard route | 5 | VE storyboard-route | SceneSpec + adapter decision + cost cap → **storyboard-route** | VE (sole) |
| 10 | Scene rendering | 5 | One per scene, chosen by storyboard-route: VE svg-scenes (default, tested) · manim-scenes (P1) · molecule-scenes (P1) · biology-scenes (P1) · blender-scenes (P2, opt-in, isolated) → VE web-composition (P1, one engine: HyperFrames **or** Remotion) | Scene insert/media → **the routed scene Skill**. Composed long/vertical video → **web-composition** | VE. "Use one engine" |
| 11 | Voice direction | 6 (pre) | VE voice-direction (stage entry) → NA voice-acting-director → NA pacing-controller (estimate) · lens: ST voice-director | Direction records + emphasis → **voice-acting-director**. Duration estimate + hold schedule → **pacing-controller** | Mapping |
| 12 | Pronunciation | 6 (pre) | VE voice-direction (stage entry) → NA stem-pronunciation · lens: ST voice-director `pronunciation_review.md` | Versioned spoken/display/caption mappings + test corpus → **stem-pronunciation** (replaces VE voice-direction's "pronunciation map") | Mapping |
| 13 | Voice synthesis | 6 | VE observability-cost / NA cost-regeneration-optimizer reserve budget & check cache → VE voice-synthesis (stage entry) → NA tts-provider-adapter → (provider worker sends once) → NA pacing-controller (measure actual) | Provider requests + job record → **tts-provider-adapter**. Audio assets + job/cost manifest → **voice-synthesis** | Mapping |
| 14 | Alignment / localize | 7 (and before 11 for non-English) | Localization *text* first: NA multilingual-director (before stage 11 for each locale) · lens: ST language-editor → after audio: VE alignment-localize (stage entry) → NA speech-animation-synchronizer | Localized script + back-check → **multilingual-director**. Sample-index timeline, cue frames, captions, protected holds → **speech-animation-synchronizer**. Localized SceneSpec → **alignment-localize** | Mapping. Ordering note PROPOSAL |
| 15 | Audio / caption QA | 9 | VE audio-caption-qa (stage entry) → NA audio-production-engineer (master) → NA narration-quality-reviewer → human listen | Mastered WAV + measurements → **audio-production-engineer**. Severity-ranked narration issues → **narration-quality-reviewer**. Media QA report + corrected VTT → **audio-caption-qa** | Mapping |
| 16 | Visual QA | 9 | VE visual-qa → human frame review | Structured defects (severity/time) → **visual-qa** | VE (sole) |
| 17 | Render batch | 8 | VE render-batch (with observability-cost reservation) | MP4/VTT/manifest + retry diagnostics → **render-batch** | VE (sole) |
| 18 | Release review | 10 | ST script-evaluator (script-stage pre-review, optional) → VE release-review → **human academic + full-video approval on artifact hash** | Release manifest or blockers → **release-review**. Script regression report → **ST script-evaluator** | VE. ST role PROPOSAL |
| 19 | Reel repurpose | 11 | VE reel-repurpose → stages 15–18 again for the Short | ShortSpec + vertical scene + caption/CTA draft → **reel-repurpose** | VE (sole) |
| 20 | Thumbnail package | 11–12 | VE thumbnail-package (optional image via provider worker) | Title options, SVG cover, description → **thumbnail-package** | VE (sole) |
| 21 | Observability / cost | throughout (6, 8) | VE observability-cost (pipeline ledger) ⇄ NA cost-regeneration-optimizer (narration jobs) | Cost dashboard + reconciliation → **observability-cost**. Narration usage ledger, scoped invalidation, retry decision → **cost-regeneration-optimizer** | Mapping |
| 22 | Skills security | before admitting any public Skill/MCP/plugin | VE skills-security | Approval record, pinned commit/digest, allowlist → **skills-security** | VE (sole) |
| 23 | Learning evaluation | after release (pilots) | VE learning-evaluation · input from ST script-evaluator `experiment_plan.md` | Pilot evaluation plan + results → **learning-evaluation** | VE. ST input PROPOSAL |
| 24 | Asset library | throughout (5, 6) | VE asset-library | AssetManifest + hash/licence/attribution ledger → **asset-library** | VE (sole) |
| 25 | Selective generation | 6 (optional) | VE storyboard-route approves purpose → observability-cost reserves → VE selective-generation (provider worker) → asset-library records | Generated AssetManifest + reviewed clip → **selective-generation**. "Zero generated seconds is allowed" | VE (sole) |

## Coverage check

| Pack | Skills placed | Not placed |
|---|---|---|
| VE (32) | All 32: stages 1–25 (scene rendering holds 6 Skills, science validation holds 4) | – |
| NA (15) | All 15: stages 5, 6, 7, 11, 12, 13, 14, 15, 21 | – |
| ST (10) | All 10 as lens or alternative: lesson-architect 4, conversational-script 5, confidence-editor 5/7, analogy-auditor 6, concept-humour 6, interaction-designer 7, science-reviewer 8, voice-director 11/12, language-editor 14, script-evaluator 18/23 | – |

## Human gates that no Skill replaces

- Academic approval of coverage (stage 2).
- Academic approval of the script, answers and model assumptions (stage 8, runbook step 4).
- Native-language review (stages 12 and 14).
- Full listen (stage 15) and human frame review (stage 16).
- Academic + full-video approval bound to artifact hashes (stage 18), repeated for each Short (stage 19).

Any material change invalidates the relevant approval. Escalation rules:
- VE: "at most two repair attempts and a cost cap".
- NA: "a second unknown or repeated failure requires review, not blind regeneration".


## Addendum (15 Oct 2026): where the 15 advanced-animation skills fire

Inserted between stage 9 (Storyboard route) and stage 10 (Scene rendering) for scenes routed `illustrative/narrative` or `typographic`, and alongside stage 10 for `data-bound` scenes that need a 3D insert. Order within a job:

| Step | Fires | Output → owner |
|---|---|---|
| 9a | `examleaf-effort-governor` | run-config (model ID, effort, iteration cap) → effort-governor; tokens logged to observability-cost |
| 9b | `examleaf-style-guides` → `examleaf-reference-analyzer` (if a reference video exists) → `examleaf-vertical-adapt` | pinned style + tokens; reference JSON; zone rectangles |
| 9c | `examleaf-cue-sheet` (reads alignment from speech-animation-synchronizer; beats from `examleaf-audio-analysis` if a bed exists) | cue_sheet.json |
| 9d | `examleaf-anim-brief` | brief.md + constraints block |
| 9e | `examleaf-anim-storyboard-gate` (grid via code thumbnails, or via `examleaf-mcp-orchestrator` + `examleaf-selective-generation` when Higgsfield is approved) → ⛔ human approval | grid, beats.json, estimate.json, approval record |
| 10′ | scene authoring in Claude Code against `examleaf-motion-harness` contract: `examleaf-procedural-2d` / `examleaf-kinetic-typography` / `examleaf-threejs-scenes` (illustrative), or `examleaf-svg-scenes` / `examleaf-manim-scenes` (data-bound) | scene files + lint + determinism hash |
| 10″ | `examleaf-audio-compose` (beds/SFX for hooks, transitions, recaps, outros only) → `examleaf-audio-production-engineer` | stems; master |
| 15′ | `examleaf-anim-qa` (feeds `examleaf-visual-qa` and `examleaf-audio-caption-qa`) | animation QA report |
| 18 | `examleaf-release-review` → ⛔ academic + full-video approval on hashes | unchanged |
| 19′ | `examleaf-reel-repurpose` + `examleaf-vertical-adapt` (sub-range re-seek, beat re-time) | ShortSpec + vertical scene |

Human gates unchanged; new mandatory gate: storyboard approval before any paid generation or scene authoring (9e).
