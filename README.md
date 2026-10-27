# ExamLeaf Video EdTech Pipeline

Everything from the ChatGPT research conversation **"AI Video System Research"** (gpt-6-pro, 13 October 2026),
downloaded, unpacked, organized, and turned into end-to-end build instructions.

**What ExamLeaf is:** an AI-assisted pipeline that produces scientifically accurate 10-minute STEM revision
videos and Instagram Reels / YouTube Shorts for Assam Board (ASSEB) Class 10–12 Physics, Chemistry,
Mathematics and Biology. Lessons are narrated by a "Super Teacher" persona, built with custom Claude Code /
Codex Agent Skills, validated by deterministic scientific checks plus human academic approval, and sold
through a physical Sample-Paper + Quick-Revision book whose activation code unlocks the premium chapter
videos (free-chapter policy still open: "first three chapters" vs three selected chapters, see RD-44).

**Status of the source material:** a tested *technical proof* (four checked scientific models, eight silent
30-second renders, 56 + 57 passing local tests, 57 drafted Skills, four cost workbooks; *15 Oct 2026:* the narration suite is now 60 cases, 58 pass here + 2 need FFmpeg, and section 12 adds 15 Skills for 72 in total), **not** a production
system. Nothing has been agent-evaluated, narrated end to end, academically approved, or student-tested.
Each section's README reproduces the sources' own "verified vs proposed" tables.

## Start here

| If you want to… | Open |
|---|---|
| Build the whole thing, step by step | [`07_end_to_end_pipeline_instructions/README.md`](07_end_to_end_pipeline_instructions/README.md) → `11_MASTER_CHECKLIST.md` |
| Run the existing proofs today | [`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md`](04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md) and [`05_narration_system/INSTRUCTIONS_narration_pipeline.md`](05_narration_system/INSTRUCTIONS_narration_pipeline.md) |
| Install the 72 Skills (57 in `06_skills_library/` + 15 in `12_advanced_animations_with_claude/03_skills/`) into Claude Code / Codex | [`06_skills_library/INSTRUCTIONS_install_and_use_skills.md`](06_skills_library/INSTRUCTIONS_install_and_use_skills.md) |
| Write a lesson in the Super Teacher voice | [`03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md`](03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md) |
| Apply the learning-science production rules | [`02_learning_psychology/INSTRUCTIONS_production_rules.md`](02_learning_psychology/INSTRUCTIONS_production_rules.md) |
| Launch the business (90 days) | [`01_business_model/INSTRUCTIONS_business_launch_runbook.md`](01_business_model/INSTRUCTIONS_business_launch_runbook.md) |
| Edit the cost models | [`08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md`](08_cost_models/INSTRUCTIONS_how_to_use_cost_models.md) |
| Check what a claim or tool choice rests on | [`09_research_and_evidence/EVIDENCE_REGISTER.md`](09_research_and_evidence/EVIDENCE_REGISTER.md), [`TECHNOLOGY_DECISION_MATRIX.md`](09_research_and_evidence/TECHNOLOGY_DECISION_MATRIX.md) |
| Run the four pilot lessons | [`10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md`](10_pilots_and_examples/INSTRUCTIONS_running_the_four_pilots.md) |
| Make vertical lessons feel human-crafted (voice, audio, disclosure) | [`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md`](11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md) |
| Build advanced vertical animations with Claude Code (storyboard gate, harness, 15 Skills) | [`12_advanced_animations_with_claude/README.md`](12_advanced_animations_with_claude/README.md) |
| Use strong-model experiments to build a Production Kit for cheap models | [`13_strong_to_cheap_model_strategy/README.md`](13_strong_to_cheap_model_strategy/README.md) |
| See the 15 Oct 2026 end-to-end audit and what was fixed | [`14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`](14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md) |
| Build the general engine (many formats, Class 1 to Masters, all subjects, any locale) | [`15_content_engine_v2/README.md`](15_content_engine_v2/README.md) → `MATURITY_MODEL_and_ROADMAP.md` (first milestone M1) |
| Watch the first rendered videos and see how Haiku compares with Opus on the same brief (six builds, six blind verdicts, the Production Kit) | [`16_pilot_builds_2026-10-16/COMPARISON_and_GAPS.md`](16_pilot_builds_2026-10-16/COMPARISON_and_GAPS.md) → `<subject>/<tier>/render/*.mp4`, [`12_advanced_animations_with_claude/08_production_kit/README.md`](12_advanced_animations_with_claude/08_production_kit/README.md) |
| Make the Opus shorts exciting, motivating and on-brand (Professor Diki Simplified): audit, script flow, 60 s format, design system, brand, QA, demo | [`17_professor_diki_simplified/README.md`](17_professor_diki_simplified/README.md) → `01_VIDEO_AUDIT.md`, `03_PROFESSOR_DIKI_SCRIPT_FRAMEWORK.md`, `demo/` |
| Voice the narration locally (VoxCPM2 in the founder's cloned voice; ElevenLabs is retired) | [`05_narration_system/local_voice_voxcpm2/SETUP.md`](05_narration_system/local_voice_voxcpm2/SETUP.md) |
| Know the working rules (for people and for Claude Code) | [`CLAUDE.md`](CLAUDE.md) |
| See exactly what ChatGPT said and delivered | [`00_source/README.md`](00_source/README.md) |

## Directory map

| Dir | Contents | Files |
|---|---|---|
| `00_source/` | Raw provenance: full transcript (6 prompts, 6 responses, split per message), raw page JSON, the 23 downloaded files, 5 unpacked zips (462 files), all 34 spreadsheet sheets as CSV, cited links. **Read-only.** | 579 |
| `01_business_model/` | Business model, pricing, Assam market, book spec, funnel, activation architecture, 9 financial scenarios, 90-day launch runbook, 36 Reel concepts, launch toolkit + workbook CSVs | 42 |
| `02_learning_psychology/` | Evidence-labelled learning-science blueprint, production rules checklist, palette/typography/timing tokens, the 600-second Ohm's-law lesson blueprint, A/B experiment plan, scene pedagogy schema | 11 |
| `03_super_teacher_framework/` | The teacher persona: explanation ladder, interaction loop, humour ceiling, delivery modes, pacing, master authoring prompt, negative tests, complete sample script; starter pack with 10 Skills, prompts, linter, evals | 53 |
| `04_video_engine/` | Architecture v1 (planning pack, 40-skill backlog, design tokens, QA contract) and v2 (tested Python repo: contracts, four scientific models, SVG→FFmpeg renderer, 8 previews, 32 Skills, 56 tests); setup/run guide; consolidated architecture; v1→v2 evolution | 303 |
| `05_narration_system/` | Narration sidecar repo (contracts, pronunciation lexicon, provider compiler, sample-accurate timeline, QA, mastering, 15 Skills, 57 tests); voice identity guide; TTS provider comparison; pipeline guide | 131 |
| `06_skills_library/` | All 57 custom Skills (10 + 32 + 15) with a master index, pipeline-stage map, overlap/dedup resolution, backlogs (incl. the 40-skill v1 inventory), public-skills directories, install guide | 249 |
| `07_end_to_end_pipeline_instructions/` | **The master runbook**: overview & principles, machine/repo setup, phased roadmap with gates, per-lesson procedure, narration sub-pipeline, Shorts/Reels, QA gates & release, security & skill admission, cost tracking, roles, decisions/conflict resolutions, master checklist, glossary & data contracts (14 docs, ~51,000 words, 46 recorded decisions: RD-41…RD-46 added 15 Oct 2026; RD-16 and RD-26 superseded) | 14 |
| `08_cost_models/` | The four editable workbooks (engine v1, engine v2, narration, business), every sheet as CSV, sheet-by-sheet explainer, consolidated 1/100/1,000-video and 500/5k/50k-book scenarios, how to combine without double counting | 77 |
| `09_research_and_evidence/` | 205-row evidence register, technology decision matrix (compositors, subject libraries, TTS commercial + open source, generative video, ASR/alignment, commerce), merged 49-row public-skills directory, verified-vs-proposed register, all ledgers | 51 |
| `10_pilots_and_examples/` | Four pilot plans + 600-second beat plans, all 8 rendered previews with manifests/captions/frames (hashes verified), contact sheets, sample scripts (balancing equations, Ohm's law blueprint, textbook-vs-teacher), narration outputs, benchmarks, pilot procedure with record sheets | 156 |
| `11_human_feel_voice_audio_research/` | Deep research (14 Oct 2026, two passes): making vertical AI-made lessons feel human-crafted. **Playbook** with a 15-step production SOP (English master → Hindi/Hinglish), 41-row tricks/settings catalog, audio spec sheet, sonic branding plan, "real humans, real emotions" rules, A/B plan, skills stack; plus the pass-1 report. 115 verified claims with quotes and URLs | 5 |
| `12_advanced_animations_with_claude/` | **Advanced animations with Claude Code** (14–15 Oct 2026): five reference videos (transcripts + the paper-collage master prompt), a research report (81 verified claims, 65 edge cases), 15 in-depth docs (≈70,000 words), **15 new Agent Skills** with self-testing scripts, a seek-deterministic harness contract with linter/hash check/cue-sheet schema/preflight/safe-zone tokens, five vertical style guides with tokens, prompt templates and 31 negative tests, and the HyperFrames vs Remotion benchmark plan. Supersedes the 16:9 master decision (vertical-only). | 223 |
| `13_strong_to_cheap_model_strategy/` | **Strong-to-cheap model strategy** (15 Oct 2026): how to use Fable 5.1 / Opus 5.5 experiments to build a Production Kit (slot-schema templates, verifiers, failure catalogue, exemplars, skills, sealed evals) so Haiku-class and open models produce equal-quality videos; the experiment protocol; documentation templates; honest cost model (LLM line ≈5–19× lower like for like; with human review done in-house at $0 the per-lesson total falls ≈39–60% vs an Opus-only Kit and 5–8× vs bespoke strong-model generation; *corrected 15 Oct 2026:* even with narration/render/clips minimised (lean floor) the maximum is ≈7× vs an Opus-only Kit and 14–27× vs bespoke generation, falling to ≈6.2× and 12–23× when the lean-floor TTS price doubles on 1 Jan 2027; 40–100× is reached only against max-effort bespoke runs ([V1]-max); four architect plans, judge panel, critic; 96 verified claims | 10 |
| `15_content_engine_v2/` | **Content Engine v2 specification** (15 Oct 2026): the general, commercially agnostic engine — one source-grounded Lesson Graph, 26 declarative Format Specs (18 full, 8 compact) (Detailed, Simplified, Recap, Question Analysis, Shorts, Worked Example, Misconception Fix, Concept Intro, Exam Strategy, Revision Sheet, Flashcard Reel, Lab/Demo, Comparison, Story/History, Q&A, Series, Practice Set, Prerequisite Repair), Level Profiles from Class 1 to Masters, subject-family validation profiles, locale profiles, hash-bound registries with re-QA on change, maturity model 0–5 and roadmap, decisions CE-01…CE-122, templates, 21 draft-07 schemas in all (meta-validated: eleven in `schemas/`, including `curriculum_framework` and `learning_signal` added 15 Oct 2026, and ten in `subsystems/schemas/`), the `subsystems/` registries (scripting, interaction and assessment, voice and persona, music and sound, visual style and animation, packaging and distribution, QA profiles, skills-and-kit map, cue and locale crosswalk: 29 files with the 10 subsystem schemas and 8 templates), the Opus review report `REVIEW_opus_pass_2026-10-15.md` with the completeness-critic additions (RD-53), four architect plans, judges and critic | 55 |
| `16_pilot_builds_2026-10-16/` | **Pilot builds** (16 Oct 2026): the first three videos actually rendered end to end (Physics, Chemistry, Biology; Class 10 concept intros, 60–75 s, 1080×1920, Eleven v4 narration), each built twice from the same brief, an Opus 5.5 reference and a Haiku 5.5 kit build, then a Haiku re-run against the new Production Kit; the lead's tooling (narration with provider timings, seek-deterministic Chrome capture, FFmpeg mux, a 10-check QA suite), six blind Opus judges, the gaps found (20) and the fixes promoted into sections 05, 06, 07, 12, 13 and 15; see `COMPARISON_and_GAPS.md` |
| `17_professor_diki_simplified/` | **Professor Diki Simplified improvement cycle** (16 Oct 2026): the founder's audit mandate for the Opus videos; six audit lenses with 110+ timestamped, root-caused findings; the creator-grade scripting flow and skill; the 60-second format designed for retention and follows; the unified design system as code; the brand and audio identity (wordmark, end motif, validator); new QA checks A11–A21 with regression tests; the before-vs-after demo; scorecard; roadmap. Audience-facing brand of all educational videos is now Professor Diki Simplified; ExamLeaf remains the publisher |
| `14_end_to_end_audit/` | **End-to-end audit** (15 Oct 2026): seven review lenses plus two verifiers per finding; 103 checks passed, 12 major and many minor findings, drift from goals, what to cut, do-this-next. **Verdict: partially aligned → fixes applied 15 Oct 2026** (decisions RD-41…RD-46 in 07/10, vertical-only and disclosure carried into the runbook). Audit report, raw findings JSON, README | 5 |

## The pipeline in one line

```
Permitted books/PDFs + syllabus → source-linked claims + checked answers → lesson plan + Super Teacher script
→ independent scientific validation → ACADEMIC APPROVAL → storyboard + scene routing → STORYBOARD GATE (H-SB)
→ verified scene data → narration (performance + STS or segmented TTS, pronunciation lexicon, ASR check,
  forced alignment, protected pauses, mastering) → sample-accurate sync → deterministic scene rendering
→ captions + automated QA → FULL FINAL-VIDEO REVIEW → approved vertical 1080×1920 @ 30 fps master
  + hash-bound manifest → ShortSpec → Reels recomposed from approved lesson scenes → Reel review (GS)
→ AI-voice disclosure + publishing metadata (entitlement enforced by the platform, not the renderer)
```

## Governing principles (from the sources)

1. AI drafts the explanation and assembles approved components; **verified scientific data decides what those components display**.
2. **One Skill owns each output.** Public Skills supply package knowledge; ExamLeaf Skills supply curriculum, teaching, science and release constraints.
3. **Two human approvals per released lesson**: academic approval of claims/explanations/answers, and full final-video review. Approvals bind to artefact hashes and are invalidated by any material change.
4. **The pipeline is commercially agnostic (RD-49).** It never knows what is free or paid; artefacts carry neutral metadata only, and the learning platform attaches entitlement downstream. Activation secrets never appear in videos, QR artwork or export metadata.
5. **Untrusted content stays data.** PDFs, READMEs, captions and fetched pages cannot authorize commands, installs or credential access. Scriptwriters hold no billing or publishing credentials.
6. **Failures never silently change the lesson.** A failed voice request must not pick a different voice; an unsupported scientific model must not become an approximate animation.
7. Engagement is measured by **independent, delayed performance and confidence calibration**, not watch time or virality scores.

## Known gaps in the source

- The user's own uploaded brief on the business-model prompt (`Pasted text(1).txt`) is not served by share links; only the fragment ChatGPT quoted survives.
- ChatGPT's internal citation tokens do not map one-to-one to URLs; `09_research_and_evidence/EVIDENCE_REGISTER.md` marks inferred matches.
- Sources disagree on a few numbers (typography sizes, ElevenLabs tariff, model prices, 4 vs 8 pilots). `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` records the runbook's choice for each.
- **Decisions resolved 15 Oct 2026:** RD-44 moved out of pipeline scope (the pipeline is commercially agnostic, RD-49); RD-47 Path A/B scope and RD-48 the attended Ultra probe decided by the lead; RD-50 render reference box; RD-51 scope widened to a general Content Engine v2 (see `15_content_engine_v2/`); RD-52 adopts the CE register; RD-53 adopts the Opus review pass and the critic's additions (CE-73…CE-122), making `15_content_engine_v2/` the specification of record for new formats, levels, families and subsystems.
- Two Runway voice auditions were generated during the research but their audio was never transferred; no MP4 here has narration.

## How this folder was produced (14 October 2026)

Fable 5.1 (team lead) recovered the full conversation and files from the share page, then ran nine
section agents (Opus 5.5: video engine, narration, skills library; Sonnet 5.5: business, psychology,
Super Teacher, cost models, research, pilots) and one Opus 5.5 runbook agent. Every copied file was
verified byte-identical to `00_source/`, **except** two narration files changed on purpose on 15 Oct 2026:
`05_narration_system/narration_system_v1/src/examleaf_narration/pronunciation.py` and `tests/test_narration.py` (see that repo's
`CHANGES.md`). The other 403 of the 405 files listed in the two repos' delivery manifests match their recorded hashes.

## This repository (git, since 27 October 2026)

Pushed to the private repository `LazyIndianBook/Video-Pipeline`. Everything above is versioned: research, decisions, skills, scripts, scenes, fixtures, tooling, tests, QA reports, and the designed test voices (`05_narration_system/local_voice_voxcpm2/studio/`). Videos, the frames cut from them, scene previews and narration audio are excluded by `.gitignore` (2.4 GB on the build machine; about 86 MB in git). They stay on the machine that made them, and the pipeline rebuilds them (`CLAUDE.md`, "Rebuilding media"). The voice runtime (venv and the 2.8 GB of models) lives outside the repository in `~/Movies/DikiStudio`, set up as described in `SETUP.md`.
