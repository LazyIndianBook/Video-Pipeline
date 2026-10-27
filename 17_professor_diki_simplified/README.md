# 17 · Professor Diki Simplified: audit and improvement cycle for the Opus videos (16 Oct 2026)

**Mandate (founder, 16 Oct 2026).** Audit the Opus-generated videos end to end, redesign the teaching, the 60-second format, the animation system, the brand and audio identity, fix the production system so defects cannot return, demonstrate before-vs-after on a weak Opus video, and deliver a scorecard and roadmap. Scope: Opus output and its workflow only. Audience-facing brand: **Professor Diki Simplified** (ExamLeaf stays the publisher).

**Inputs.** `00_INPUTS_digest.md` (the mandate, the external audit of our MP4s, the growth playbook and its 24 briefs, our own evidence). Objective measurements and 1-fps frames of the three Opus videos: `audit/measurements.json`, `audit/frames/`.

| Deliverable | Where |
|---|---|
| 1 Complete video audit | `audit/A1…A6_*.md` (six lenses) and `01_VIDEO_AUDIT.md` (consolidated, timestamped, root-caused, severity) |
| 2 Prioritised improvement plan | `02_IMPROVEMENT_PLAN.md` |
| 3 New scriptwriting framework | `03_PROFESSOR_DIKI_SCRIPT_FRAMEWORK.md` + skill `skills/professor-diki-script/` |
| 4 60-second video redesign | `04_SIXTY_SECOND_FORMAT.md` + Format Spec `format/concept_short_60` |
| 5 Unified visual design system | `05_DESIGN_SYSTEM.md` + `design_system/` (tokens, CSS, scene base, components, motion verbs) |
| 6 Brand and audio identity | `06_BRAND_and_AUDIO_IDENTITY.md` + `brand/` (wordmark, end motif, disclosure strings) |
| 7 Claude Skills and pipeline changes | `07_PIPELINE_CHANGES.md` + `DIKI_CONTRACT.md` + edits in 12/, 15/, 16/tooling (QA A11–A21, voice calibration, tempo), `tests/` (12 regression tests, `run_all.sh`), `brand/MIGRATION_LOG.md` |
| 8 Before-vs-after demonstration | `demo/physics_v2/` (script, scene on design system v2, narration, render, QA) + `08_BEFORE_AFTER.md` (comparison, blind judging in `16_pilot_builds_2026-10-16/judging/physics_pd/`, scorecards) |
| 9 Video quality scorecard | `09_SCORECARD.md` + `tooling/scorecard.py` + judge rubric and brief `tooling/JUDGE_RUBRIC_PD.md`, `tooling/JUDGE_PROMPT_PD.md` |
| 10 Implementation roadmap | `10_ROADMAP.md` |
| 11 The 60-second explainer method (PD-26, "100 Seconds" profile) | `11_SIXTY_SECOND_EXPLAINER_METHOD.md` + `demo/physics_v4_method/` (plain, fast, packed, NCERT: 166 words, built and checked 17 Oct; narration after the quota reset) |

**Status (16 Oct 2026, late evening).** Decisions PD-01 to PD-23 in `DECISIONS_PD.md`; the founder's later steers (collage house style, no "AI-generated" line, brand only at the start and end, light colours, structured elements) are PD-17 to PD-21 and overrule the earlier audit proposals they name. Design system v2.0.2 (paper cut-out collage for every subject) is live in `design_system/`. The physics demo is rebuilt on it, narrated once with ElevenLabs v4 (102 words for the calibrated voice, PD-22), rendered deterministically and judged blind against the original Opus physics; results in `08_BEFORE_AFTER.md`. Regression suite: `tests/run_all.sh` → OK. **17 Oct:** after the judged before-vs-after, the founder set PD-24 (shorts are complete explainers, no questions): format `format/explainer_60.md`, framework §6b, tooling by format; the explainer demo is `demo/physics_v3_explainer/` (story script PD-25; rendered `render/phy-ohm-pd-03.mp4`, 59.0 s, 17/2/2 checks). **27 Oct:** the founder replaced ElevenLabs with a local voice system (PD-29): VoxCPM2 in the founder's cloned voice, run through `narrate_voxcpm.py` (setup: `05_narration_system/local_voice_voxcpm2/SETUP.md`). `demo/physics_v4_method/` is narrated once the founder's reference recording exists; it no longer waits on the ElevenLabs quota. Until then, the designed test voice `male_30s` (PD-29a) voices test builds: `demo/physics_v4_method_testvoice/` runs 60.2 s and passes QA with 18 pass, 3 warn, 0 fail (not for release).

Status lines are kept at the top of each deliverable file.
