# 12 · Advanced Animations with Claude (research, documentation, 15 skills, harness, styles, prompts, benchmark)

**What this section is.** An end-to-end capability for producing advanced animation for ExamLeaf's vertical (1080×1920) STEM lessons and Reels with Claude Code: motion graphics, hand-drawn/doodle and paper-collage 2D drawn in JavaScript, kinetic typography, three.js and Blender 3D, Manim mathematics, Python-composed music and SFX, audio analysis for beat sync, MCP orchestration (Higgsfield storyboards and cutouts, Blender, voice), effort-level and cost governance, reference-video-driven structured prompting, storyboard review gates, and every edge case we could source. Built on 14–15 October 2026 from the five reference videos the user supplied plus 81 verified web claims.

**One-sentence model.** Claude writes scene code; a deterministic seek-based renderer turns time into pixels; narration timing (not the model) sets duration; validated fixtures (not the model) supply every science glyph; humans approve the storyboard and the final video.

**Status.** Everything here is drafted and offline self-tested (every script's `--selftest` passes on this Mac; the template scene was shown to render byte-identical frames across Chrome processes). Nothing has been agent-evaluated, benchmarked against HyperFrames or Remotion, or used on a real lesson. This Mac also fails the preflight (Node 20 active, no FFmpeg/ffprobe), so install those before trying any render.

## Start here

| If you want to… | Open |
|---|---|
| Understand the whole layer and how to read it | `02_documentation/00_OVERVIEW_and_PRINCIPLES.md` |
| Set up a machine, the harness, and the skills | `02_documentation/01_SETUP_environment_harnesses_skills.md` then `04_harness_contract/preflight.sh` |
| Write a brief that gets professional output | `02_documentation/02_PROMPTING_the_structured_brief.md` + `06_prompts_and_templates/brief_template.md` |
| See a complete worked example | `02_documentation/13_END_TO_END_WALKTHROUGH.md` |
| Check an edge case | `02_documentation/12_EDGE_CASES_master_table.md` (65 sourced + new ones) |
| Install or read a skill | `03_skills/README_skills_1-8.md`, `03_skills/README_skills_9-15.md` |
| Prove a scene is deterministic | `04_harness_contract/contract.md`, `lint_seek_contract.js`, `determinism_hash_check.py` |
| Pick or adapt a visual style | `05_style_guides/README.md` |
| Run the HyperFrames vs Remotion benchmark | `07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md` |
| See what the videos actually said | `00_reference_videos/INDEX.md` and `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md` |

## Folder map (see master README for current count)

| Folder | Contents | Files |
|---|---|---|
| `00_reference_videos/` | The five YouTube videos: metadata, descriptions with chapters, plain and timed transcripts (yt-dlp auto-captions); the verbatim paper-collage master prompt and style guide linked from video 4 | 22 |
| `01_research/` | The cited research report (≈10,500 words; harness decision table; Claude Code effort/ultracode/cost facts; styles; audio; MCPs; craft rules; 65 edge cases; integration; 15 proposed skills; open questions) and every claim with quote, URL and verification status | 3 |
| `02_documentation/` | Fifteen in-depth docs (≈70,000 words): overview and principles; setup; prompting; style guides (vertical); harness contract and determinism; storyboard gate and MCP budgets; audio compose/analyze/sync; three.js, Manim, Blender; kinetic typography and Indic text; effort and cost governance; QA gates; integration with the ExamLeaf pipeline (18 proposed runbook amendments); the master edge-case table; the end-to-end walkthrough; decisions (AD-01…AD-40) and open questions | 15 |
| `03_skills/` | Fifteen Claude Agent Skills (`examleaf-` prefix): anim-brief, reference-analyzer, style-guides, anim-storyboard-gate, motion-harness, procedural-2d, kinetic-typography, threejs-scenes, audio-compose, audio-analysis, cue-sheet, mcp-orchestrator, effort-governor, anim-qa, vertical-adapt. Each: in-depth SKILL.md (1,600–2,800 words), ≥2 references, templates with `handoff.json`, ≥7 eval cases, offline self-testing scripts | 150 |
| `04_harness_contract/` | The normative scene contract; a runnable template scene; the seek-contract linter; the determinism hash check; the cue-sheet JSON Schema, example and validator; the machine preflight; vertical safe-zone and loudness tokens; FFmpeg reference-analysis wrapper; clip-import notes | 12 |
| `05_style_guides/` | Five house styles for 9:16 (paper-collage-vertical, a full KEPT/ADAPTED rewrite of the master prompt's guide; doodle-handdrawn; editorial-vox; kinetic-type; voxel-isometric) and machine-readable `style_tokens.json` | 7 |
| `06_prompts_and_templates/` | The structured brief template; the ExamLeaf version of the master prompt; storyboard request and review checkpoint wording; five fully filled per-style prompts using real hooks from the Reel backlog; 31 negative tests the animation agent must refuse | 11 |
| `07_benchmark_and_pilot_plan/` | HyperFrames vs Remotion benchmark protocol, the three pilot lesson scenes, and blank record sheets | 3 |

## Where this plugs into the rest of the project

- The 15 skills are registered in `../06_skills_library/` (matrix rows, README addendum, ownership addendum in `OVERLAP_and_DEDUPLICATION.md`, firing order in `SKILLS_PIPELINE_STAGE_MAP.md`). They live **canonically here** and are not copied there.
- The runbook decision RD-16 (16:9 master) is superseded by vertical-only output; see the addendum in `../07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` and the proposed amendments PA-01…PA-18 in `02_documentation/11_INTEGRATION_with_ExamLeaf_pipeline.md` §7.
- Loudness follows the house standard (−16 LUFS / −1 dBTP); the master prompt's −14 LUFS is kept only as a Reels A/B variant (AD-04, AD-37).
- Voice stays with `../05_narration_system/` and the human-crafted playbook in `../11_human_feel_voice_audio_research/`; the animation layer only consumes word timings through the cue sheet.

## Things to know before relying on it

- **Effort.** Opus 5.5 and Sonnet 5.5 default to *medium* effort; set high explicitly (xhigh for 3D). Never run ultracode in production: the reference test burned ≥2.5M tokens (≈$348 at API prices) and never finished.
- **"Claude Motion"** is not an official product name in any verified source; it is used here only as the name of this code-to-video layer.
- **Fable 5.5** material from video 5 is a leak-based, unverified capability signal; the harness is model-agnostic on purpose.
- **Safe-zone pixel insets are placeholders** until measured on phones; the scripts refuse to certify until `measured` is true (or an explicit provisional value is passed).
- **Brand and subject colours** in the style tokens are proposals pending `examleaf-asset-library` approval (AD-39).
- **A narration-system bug** (Hindi/Assamese word splitter fragmented words) was found while building the cue-sheet skill and **fixed on 15 Oct 2026** in section 05 (AD-40; `05_narration_system/narration_system_v1/CHANGES.md`). The cue-sheet builder's tokenizer now follows the same rules (ZWJ/ZWNJ dropped inside words, never splitting them).
- Two reference analysers exist by accident of parallel work; the Python one in the skill is canonical (AD-35). The harness scripts are canonical and the skill copies must stay byte-identical (AD-36).

**Changes from the end-to-end audit, 15 Oct 2026** (`../14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md`; decisions AD-41…AD-45 in `02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`):
- **One cue-sheet validator** (M7, AD-43): `04_harness_contract/validate_cue_sheet.py`. The skill copy was deleted. `build_cue_sheet.py` now emits `schema_version`, `language`, `narration_audio_sha256` and `script_sha256` (the spec needs `language` and `script`), maps narration kinds to the schema enum, and its selftest runs the output through the harness validator with `--production`.
- **Storyboard approval** (M10, AD-44, RD-46): two roles (founder for cost, academic lead for science fit, two identities) plus fixture, style and hero hashes. The **runner**, not the agent, verifies the record against the authenticated approval service and then runs `--verify-approval`. Jobs deny `Edit(./storyboard/**)`; style and contract files are staged as hashed copies inside the job folder, so `Read(../**)` stays denied and the brief's reads still work.
- **`preflight.sh --workspace <job>`** (M11) now scans for secrets (`sk-ant-`, `AKIA`, private keys, `api_key=`), ultracode effort settings and unversioned model aliases. Doc 01 §9 marks each check implemented or proposed (Manim variant, repository weight and provider-key variables are still proposed).
- **Safe zones** (AD-42): `04_harness_contract/vertical_safe_zones.tokens.json` alone owns the zone shares (0.22 / 0.54 / 0.24) and `zones.side_margin_min_px` = **96 px** (90/60/96 reconciled). `layout_zones.py` and `safe_zone_check.py` read it; the template mirrors it; `validate_style_tokens.py` fails on drift.
- **Loudness and music**: [V4-MP]'s −1.5 is a **sample-peak dBFS** figure, not dBTP (AD-37 corrected). One music policy: muted under teaching; beds only in hooks, transitions, recaps and outros at **20–24 dB under speech**; owned sonic logo commissioned from a composer; code-composed beds for Reel hooks, SFX and prototypes (AD-15 addendum).
- **Vertical only**: A11 accepts only 1080×1920; RD-16 is superseded and the 15 Oct vertical decision is cited as the authority (AD-07, C1, Q16, style tokens). The proof renderer only does `--aspect 9:16` at **720×1280 @ 24 fps** today; a 1080×1920 @ 30 fps mode is a P1 build item (doc 13 B.6).
- **anim-qa** (AD-45): untraceable science text, any full-frame flash and an early answer reveal are **critical** (never waivable) in the scripts and doc 10.
- **Effort governor** (AD-41): new `kit_cascade` task family with its own caps for section 13's Kit (Haiku authors scene code only there). Ultracode is still refused everywhere, and the attended S5 probe is not an exception in code.
- **Negative tests**: NT-32 (disclosure removal), NT-33 (fake "I heard you" sensing) and NT-34 (activation secret on screen), run in chat and as Kit slot values.
- **This Mac**: use `python3` (there is no `python`), a venv pinned to 3.13 or 3.11, and Node 24 via `nvm use 24`. **ffmpeg and ffprobe are both missing.** Doc 01 §10 has a minimal frame-capture command for the determinism gate, marked "verify".
- Selftests: run as `python3 -B -I <script> --selftest`, `node <script> --selftest` or `bash <script> --selftest`.

## How it was produced

Fable 5.1 (lead) fetched the five videos' transcripts and the master prompt, ran a deep-research workflow (10 Sonnet search angles → 30 sources read → two-lens adversarial verification of 110 claims, 81 survived → Opus synthesis), then a six-agent build (Opus: docs 00–05+14, docs 06–13, skills 1–8, skills 9–15; Sonnet: harness contract code + benchmark plan, style guides + prompt templates), followed by a lead audit (structure, self-tests, JSON validity, edge-case coverage, cross-team reconciliation AD-33…AD-40) and registration in the skills library and runbook.
