# Video Engine v1 → v2: what changed, what was proved, what is still open

- **v1** = message 02 (`FULL_v1_architecture_and_plan.md`) + `planning_pack_v1/` (README, QA contract, design tokens, 40-Skill CSV, cost workbook). Self-description: "planning artifacts, not an already implemented video engine."
- **v2** = message 10 (`FULL_v2_implementation_and_research.md`) + `implementation_v2/` (tested Python repo, 32 Skill drafts, 8 previews, 56 tests, cost workbook). Self-description: "tested local technical proof, not a production release."
- Both were "checked on 13 October 2026". v2 was prompted by message 09, which added Higgsfield, mandatory public repos, the Super Teacher persona, Instagram/YouTube Shorts with the 3-free-chapters funnel, three cost architectures and four pilot videos, and asked for working scaffolding.

Comparisons are from the sources; mappings and judgements marked *(organizer)* are the organizer's.

---

## 1. At a glance

| Topic | v1 (plan) | v2 (implementation + research) |
|---|---|---|
| Deliverable | Architecture report + planning pack (no code) | Python repo with 8 modules, 5 schemas, 56 passing tests, 8 rendered MP4s, 32 Skill drafts, 7 docs, 7 research files |
| Compositor | HyperFrames first, Remotion "measured alternative" | Same decision, unchanged; but the shipped proof uses **native SVG → CairoSVG → FFmpeg**, "not HyperFrames" |
| Specialist renderers | Manim (math), selective Three.js, Blender only when needed | Same; plus Motion Canvas listed as alternative; none installed |
| Scientific validation | SymPy/SciPy/Pint/RDKit/Biopython proposed | Four **bounded** validators implemented (RC charging, H₂/O₂/H₂O balance, (3x+1)² chain rule, Aa×Aa cross) |
| Skills | 40 proposed custom Skills ("Proposed; not implemented") + existing-Skills table | 32 drafted Skill folders (SKILL.md + contract + handoff template + eval cases), "not agent-evaluated"; 21-entry public directory |
| Generative media | Not routed; HeyGen avatars "do not use as the core engine" | Explicit routing table; default 0 generated seconds; Higgsfield/Runway/Veo/Seedance/Kling/Pika/Luma assessed |
| Short-form | Not covered | `ShortSpec` contract (20–60 s, reflow only), 1–3 complete Shorts per lesson, funnel/access metadata |
| Teaching persona | Learning-science section (§8), voice brief | Super Teacher contract in data (`Cue.role`, `Cue.voice`, `answer_visible`), docs/Super_Teacher_Contract.md |
| Orchestration | Prefect + Docker workers from the start | Local process pool + SQLite → Prefect/Postgres/object storage only after four narrated pilots |
| Narration | Provider shortlist (ElevenLabs, Cartesia, Sarvam, Google Chirp, Kokoro, OpenAI) | One live Runway speech job (eleven_multilingual_v2, voice "Arjun", 32.18 s, 9 credits); fail-closed local adapter; mux/alignment validators |
| Pilots | Phase D: **eight** pilot lessons (one per subject strand and class level); first pilot drift velocity & current | **Four** pilots (one per subject): RC charging, balancing, chain rule, monohybrid cross — only 30 s silent fixtures + 600 s beat plans exist |
| Cost model | One architecture (HyperFrames + commercial AI/TTS) | Three architectures (AI-heavy, hybrid, mostly self-hosted) + Shorts add-on + human-capacity sheet |
| Roadmap | Phases A–G | Phases 0–4 with day/week estimates |

---

## 2. Skills: 40-item v1 backlog → 32 v2 Skills

v1 had eight workstreams (Sources 4, Teaching/script 7, Scientific verification 5, Storyboarding/visual 8, Specialist adapters 2, Narration/localization 5, Production 3, QA/operations/outcomes 6). v2 consolidated "into **32 purpose-specific custom Skills** rather than installing several overlapping 'make a video' agents" in eight groups. **The sources do not publish a mapping**; the table below is the organizer's, based on each Skill's inputs/outputs/steps.

| # | v1 Skill (planning_pack_v1/ExamLeaf_Skills_Inventory.csv) | v1 Pri. | → v2 Skill(s) | Fit |
|---:|---|---|---|---|
| 1 | examleaf-rights-ingest | P0 | examleaf-source-ingest | direct |
| 2 | examleaf-syllabus-map | P0 | examleaf-curriculum-map | direct |
| 3 | examleaf-source-claim-ledger | P0 | examleaf-claim-research | direct |
| 4 | examleaf-prerequisite-graph | P1 | examleaf-curriculum-map (prerequisite vs assessed) + examleaf-lesson-plan (consumes "prerequisite graph") | absorbed |
| 5 | examleaf-lesson-scope | P0 | examleaf-lesson-plan | direct |
| 6 | examleaf-revision-script | P0 | examleaf-super-teacher (+ voice-direction for display vs spoken text) | direct |
| 7 | examleaf-worked-examples | P0 | examleaf-lesson-plan (worked → faded → independent) + examleaf-claim-research (independent answer keys) | absorbed |
| 8 | examleaf-retrieval-challenges | P1 | examleaf-interaction-design | direct |
| 9 | examleaf-misconception-audit | P0 | examleaf-analogy-humour (misconception risk) + science-* Skills | partial |
| 10 | examleaf-confidence-load-audit | P1 | examleaf-super-teacher + examleaf-analogy-humour | partial |
| 11 | examleaf-exam-rubric | P1 | — (only the `exam_conversion` beat in the 600 s plans) | **no v2 Skill** |
| 12 | examleaf-math-verification | P0 | examleaf-science-math | direct (bounded validator tested) |
| 13 | examleaf-physics-verification | P0 | examleaf-science-physics | direct (bounded validator tested) |
| 14 | examleaf-chemistry-verification | P0 | examleaf-science-chemistry | direct (bounded validator tested) |
| 15 | examleaf-biology-verification | P0 | examleaf-science-biology | direct (bounded validator tested) |
| 16 | examleaf-independent-review | P0 | — (kept as an architecture stage + human academic gate + release-review) | **no v2 Skill** |
| 17 | examleaf-storyboard | P0 | examleaf-storyboard-route | direct |
| 18 | examleaf-design-system | P0 | examleaf-asset-library (brand/tokens) + `configs/design_tokens.json` | partial |
| 19 | examleaf-scene-compiler | P0 | examleaf-web-composition (+ examleaf-svg-scenes for the proof) | direct |
| 20 | examleaf-equation-animation | P0 | examleaf-manim-scenes / examleaf-svg-scenes | absorbed |
| 21 | examleaf-graph-geometry | P0 | examleaf-manim-scenes / examleaf-svg-scenes | absorbed |
| 22 | examleaf-physics-animation | P1 | examleaf-svg-scenes (RC fixture) / examleaf-manim-scenes | absorbed |
| 23 | examleaf-chemistry-animation | P1 | examleaf-molecule-scenes | direct |
| 24 | examleaf-biology-animation | P1 | examleaf-biology-scenes | direct |
| 25 | examleaf-manim-adapter | P0 | examleaf-manim-scenes (now P1) | direct |
| 26 | examleaf-threejs-adapter | P2 | — (3D via examleaf-blender-scenes; 3Dmol.js inside molecule-scenes) | **no v2 Skill** |
| 27 | examleaf-narration-normalizer | P0 | examleaf-voice-direction | direct |
| 28 | examleaf-pronunciation-lexicon | P0 | examleaf-voice-direction (pronunciation map) | absorbed |
| 29 | examleaf-tts-batch-cache | P0 | examleaf-voice-synthesis | direct |
| 30 | examleaf-forced-alignment | P0 | examleaf-alignment-localize | direct |
| 31 | examleaf-multilingual-localization | P1 | examleaf-alignment-localize | absorbed |
| 32 | examleaf-render-orchestrator | P0 | examleaf-render-batch | direct (local batch tested) |
| 33 | examleaf-audio-mastering | P0 | examleaf-audio-caption-qa (clipping/loudness) | partial |
| 34 | examleaf-captions-export | P0 | examleaf-audio-caption-qa (corrected VTT) + examleaf-render-batch (MP4/VTT/manifest) | absorbed |
| 35 | examleaf-visual-accessibility-qa | P0 | examleaf-visual-qa | direct |
| 36 | examleaf-science-frame-qa | P0 | examleaf-visual-qa ("compare model state and cue") | absorbed |
| 37 | examleaf-regression-qa | P0 | — (golden fixtures live in `tests/`; no Skill) | **no v2 Skill** |
| 38 | examleaf-rights-security-release | P0 | examleaf-release-review + examleaf-skills-security + examleaf-asset-library | split |
| 39 | examleaf-bulk-cost-ops | P1 | examleaf-observability-cost (now P0) | direct |
| 40 | examleaf-learning-evaluation | P1 | examleaf-learning-evaluation | same name |

**New in v2 with no v1 counterpart:** examleaf-analogy-humour, examleaf-interaction-design (partly retrieval-challenges), examleaf-blender-scenes (v1: "Add a Blender adapter only when a real lesson requires it"), examleaf-reel-repurpose, examleaf-thumbnail-package, examleaf-skills-security, examleaf-asset-library, examleaf-selective-generation.

**v1 Skill contract → v2 Skill folder:** v1 required `SKILL.md` (purpose/trigger, typed I/O, approved dependencies/commands, required source evidence, forbidden transformations, acceptance tests, escalation conditions) + `scripts/` + `references/` + `evals/` (correct, deliberately incorrect, regression fixtures). v2 folders have `SKILL.md`, `references/contract.md`, `templates/handoff.json`, `evals/cases.json` — **no per-Skill `scripts/`** ("Shared deterministic scripts are in `src/examleaf` and `scripts`; duplicating executables into every Skill would create drift"), and one positive + one generic negative eval case each rather than full regression fixtures.

---

## 3. Compositor decision

Unchanged in substance. v1: "Approve HyperFrames as the initial compositor candidate… Keep Remotion as the measured alternative, not a parallel default." v2: "Use HyperFrames as the initial production candidate, preserve Remotion as the measured alternative." Both require the same-fixture benchmark (correctness → reproducibility → memory → render time → repair → cost). v2 adds the concrete protocol (identical fixtures in both aspects, warm-up + ≥5 repeats, cold vs cached, peak RSS/CPU/GPU) and makes the four implemented science fixtures the "golden" inputs. **Still not done in either version:** neither HyperFrames nor Remotion was installed or benchmarked. v2's own proof renderer (native SVG/CairoSVG) is a third path, described as "a reference adapter, not a new general-purpose animation framework."

---

## 4. Cost models compared

### 4.1 Per-video inputs

| Input | v1 workbook (`ExamLeaf_Cost_and_Skills.xlsx`) | v2 workbook (`ExamLeaf_Video_Engine_Cost_Model.xlsx`, hybrid column) |
|---|---|---|
| LLM models & tariffs (USD / M tokens in/out) | Haiku 5.5 $0.10/$0.50; Sonnet 5.5 $2/$10; `gpt-6.1-sol` independent review $2/$10; Opus 5.5 escalation $4/$20 | Haiku 4.5 $1/$5; Sonnet 4.6 $3/$15; Opus 4.6 review $5/$25 |
| LLM workload (in/out tokens) | Haiku 30k/5k; Sonnet 120k/25k; Sol 60k/10k; Opus 10k/2k | Haiku 20k/3k; Sonnet 120k/25k; Opus 60k/10k |
| LLM cost incl. 30 % regeneration | **$1.0342** | **$1.716** |
| Narration | 8,000 chars × 1.2 × **$0.08**/1k = **$0.768** | 8,000 × 1.2 × **$0.10**/1k = **$0.96** |
| Rendering | Fargate 8 vCPU/16 GB × 45 min + 20 % = $0.3555 | encode allowance $0.50 |
| Generated video | none | 20 s × 2 attempts × $0.10/s = $4.00 (optional) |
| Generated stills | none | $0.20 |
| ASR / alignment-audio | ASR $0.03 | alignment/audio $0.10 |
| Storage | 2 GB × $0.015 = $0.03 | $0.20 |
| Misc reserve | $0.15 | — |
| **Machine subtotal** | **$2.3676** | **$7.676** (hybrid) / $111.476 (AI-heavy) / $2.315 (self-hosted) |
| Human time | 45 min academic @ $20 + 15 min QA @ $12 = **$18** (60 min) | 45 min academic @ $20 + 20 min QA @ $15 + 20 min repairs @ $20 = **$26.67** (85 min) |
| **Variable / video** | **$20.37** | **$34.34** hybrid; $158.98 AI-heavy; $37.32 self-hosted |
| Fixed / month | $200 ($100 infra + 4 h × $25 maintenance) | $300 hybrid; $250 AI-heavy; $900 self-hosted |
| One-time setup | $8,000 (240 eng h + 60 academic h + 20 design/voice h, all @ $25) | $10,000 hybrid; $5,000 AI-heavy; $16,000 self-hosted |
| Remotion option | +$100/$100/$200 at 1/100/1,000 (20 billable renders/video assumed) | same assumption (+$200/month at 1,000) |

### 4.2 Totals for the same one-month period (USD, pre-tax, excluding setup)

| Volume | v1 baseline | v2 AI-heavy | v2 hybrid (recommended) | v2 mostly self-hosted |
|---|---:|---:|---:|---:|
| 1 video | $220.37 | $408.98 | $334.34 | $937.32 |
| 100 videos | $2,236.76 | $16,147.60 | $3,734.27 | $4,631.50 |
| 1,000 videos | $20,567.62 | $159,226.00 | $34,642.67 | $38,215.00 |
| Reviewer hours @ 1,000 | 1,000 h = 6.25 FTE | — | 1,417 h = 8.85 FTE | — |
| Incl. setup @ 1,000 | $28,567.62 | $164,226 | $44,642.67 | $54,215 |

**Why v2 is higher *(organizer)*:** +$0.68 LLM (different model tier/tariffs), +$0.19 narration (tariff $0.08 → $0.10), +$4.20 optional generated media, +$8.67 human (repair time now explicit, QA rate $12 → $15, QA 15 → 20 min), +$100/month fixed. Without the optional generated video v2 hybrid is $30.34/video. Both versions agree on the conclusion: **human academic/QA review dominates cost** (v1: "Approximately $2.37 is the assumed machine portion"; v2: "Human capacity is the major scaling constraint").

### 4.3 Inconsistencies to resolve before using either number *(organizer flag; not resolved here)*
- Same check date, different LLM model generations and tariffs (v1 "Haiku/Sonnet/Opus 5.5" at $0.10–$4 input; v2 "Haiku 4.5/Sonnet 4.6/Opus 4.6" at $1–$5 input). Re-check current pricing before budgeting.
- Same check date, different ElevenLabs API rate ($0.08 vs $0.10 per 1,000 characters).
- v1 uses an OpenAI model as the independent reviewer; v2 uses Opus.
- Detailed cost reconciliation belongs to `08_cost_models`.

---

## 5. What v2 proved that v1 only proposed

| v1 proposal | v2 evidence (as the sources state it) |
|---|---|
| Typed, renderer-independent LessonSpec/SceneSpec | Strict pydantic `SceneSpec`, `LessonPlan`, `AssetManifest`, `ProviderJob`, `ShortSpec`, `Approval`, with negative tests (bad subject, unknown source, cue gap, answer visible during question, generated asset without provenance, unknown job without ID, crop strategy) |
| Python scientific validation before animation | Four bounded validators with independent cross-checks (SciPy ODE vs analytic, error 1.9e-10 V; finite difference; RDKit atom counts; exact fractions); out-of-scope inputs rejected (including a code-injection SMILES) |
| "Same data drives all representations" | Graph marker, counter and caption all computed from `rc_state`; regression test `test_feedback_frame_matches_number` added after a real desynchronisation was found |
| Deterministic, frame-indexed rendering | `render_svg` pure function of frame; `test_renderer_reproducible` |
| 16:9 + 9:16 output | 8 real MP4s (30 s, 720 frames, 24 fps, 1280×720 / 720×1280, H.264 yuv420p), vertical re-laid-out (`test_vertical_not_crop`) |
| Native-text-first PDF extraction with hashes | `extract-pdf` tested on a synthetic PDF |
| Scene cache by content hash; immutable manifests | Cache key + MP4 hash check; atomic writes; per-render manifests; `DELIVERY_MANIFEST.json` |
| Per-lesson spending caps, idempotent jobs | SQLite cents ledger: idempotent reservation, cost-mismatch rejection, overrun recorded then pause |
| Two human approvals bound to the final artefact | `release-check` blocks without narration and without academic + full-watch production approvals bound to the exact hash (policy demo, not authentication) |
| Narration via provider | One live speech operation returned audio (Runway, 32.18 s, 9 credits) — **not** downloaded, synchronized or reviewed |

## 6. What is still only proposed (open items carried from v1 into v2)

From the v2 README "What is not implemented or approved" and message 10's tested-status table:
1. Four complete narrated ~10-minute pilot lessons (only 600 s beat plans; scripts "requires_authoring_and_review").
2. HyperFrames / Remotion / Manim / Blender execution and the compositor benchmark.
3. Native TTS provider adapters, forced alignment, pronunciation lexicon, narration import/sync.
4. Distributed scheduling / Prefect / Postgres / object storage / cloud deployment.
5. Authenticated human-review service, append-only audit log, artifact signatures; platform publishing.
6. Agent evaluation of any of the 32 Skills in Claude Code or Codex.
7. Teacher approval of any content; any student-learning study.
8. Browser preview validation (blocked by environment).
9. Phone-readability acceptance (the preview's finer labels "are not claimed to pass").
10. Adapter-scoped cache keys (current keys invalidate on any source change).
11. Assamese/localized voice support (blocked until a real model-specific request succeeds and native review passes — stated in both versions).
12. An authenticated, all-in Higgsfield price for a ten-minute lesson ("not obtained").
13. v1 items with no v2 Skill: exam-rubric, independent-review, threejs-adapter, regression-qa (see §2).

## 7. Other changes worth knowing

| Topic | v1 | v2 |
|---|---|---|
| Narration length target | ~1,150–1,300 words; 130–150 wpm | ~1,100–1,250 words; 130–155 active wpm; 3–4 predictions; 2–3 learner-controlled practice pauses |
| 10-minute structure | 9 segments (0:00–0:25 problem … 9:30–10:00 confidence checkpoint) | 11 beats (curiosity 25 s … confidence_and_spacing 40 s) in every `*_600s_plan.json` |
| Canvas / fps | 1920×1080 @ 30 fps master (design tokens) | proof 1280×720 & 720×1280 @ 24 fps; production target 1920×1080 & 1080×1920 @ 24 or 30 fps "chosen consistently" |
| Fonts | Inter (SIL OFL) + Noto Sans + KaTeX fonts | DejaVu Sans "for offline proof only"; production brand fonts must be licensed and pinned |
| Palette | 8 roles + dark variant + contrast ratios | same 7 colours + `line #D9E1EC`, `card #FFFFFF`; no dark variant |
| Voice tags | voice brief ("conversational but authoritative…") | editorial tags STEADY/CURIOUS/DELIBERATE/LIGHT/REASSURING in `Cue.voice` |
| Audio mastering | −16 LUFS, ≤ −1 dBTP, no background music in core explanation | no music in core explanation by default (Super Teacher contract); mastering target not restated |
| Batch target size | Phase E: 30–50 lessons | Phase 3: 20–30 lessons |
| Scene hosting of humour/analogy | not addressed | analogy contract: explicit mapping, limit, misconception risk, return to the model; zero jokes allowed |

## 8. Internal inconsistencies noticed in the sources *(organizer flag)*
- Progress note 09b says "silent **24**-second engineering tests" and "**55** tests passing"; the final README/message 10/`outputs/tests.txt` say **30**-second MP4s and **56** passed. The delivered files are 30 s / 720 frames, and the suite has 56 tests.
- v1 phase D calls for **eight** pilot lessons; v2 reduces this to **four**.
- Pricing differences in §4.3.
- Message 10 says the HyperFrames "live manifest and cached README did not agree on the number of available Skills"; v1 counted 21 manifest entries — consistent with v2's directory snapshot ("21 manifest entries, cached README count differs").
