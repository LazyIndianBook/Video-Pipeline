# 16 · Pilot builds (16 Oct 2026): three real videos, strong tier vs cheap tier

**Question from the founder.** Make three videos (Physics, Chemistry, Biology) with Opus and with Haiku, check the pipeline properly, find out whether a low-cost model can produce "super fine" videos when it follows our skills, guides and pipeline, and fill the gaps.

**What this folder is.** The first time anything in this project has actually rendered a vertical lesson end to end: Lesson Graph → executable fixture → script (beats bound to graph nodes) → storyboard → seek-deterministic HTML scenes → per-beat ElevenLabs v4 narration with provider word timings → per-scene cue sheets (validated) → headless-Chrome frame capture at 1080×1920/30 fps → FFmpeg encode and mux → QA suite (lint, cue sheets, fixture text, safe zones, flash, loudness, transcript, pacing, determinism). Each subject is built twice from the same brief: `opus/` (reference tier, Opus 5.5) and `haiku/` (kit tier, Haiku 5.5). The lead (Fable) wrote the contract and tooling, narrated, rendered, ran QA and judged.

| Path | What |
|---|---|
| `PILOT_CONTRACT.md` | The single brief every builder follows: layout, script schema, scene rules, checks, build notes |
| `<subject>/brief.md` | Topic, level, fixture, misconception, style, voice, budget |
| `<subject>/<tier>/` | The build: `lesson_graph.json`, `fixtures/`, `script.json`, `storyboard.md`, `scenes/`, `build_notes.md`, then `narration/`, `cues/`, `render/`, `qa/` added by the lead |
| `tooling/` | `pilotlib.py` (cue sheets, Chrome injection), `check_script.py`, `preview_scene.py`, `narrate.py` (cached per beat; never re-bills an unchanged beat), `narrate_voxcpm.py` (27 Oct 2026, PD-29: the local VoxCPM2 voice that fills that cache; ElevenLabs is retired), `render.py` (contract §11 harness), `qa.py` |
| `COMPARISON_and_GAPS.md` | Judges' verdicts per subject and tier, the gaps found, the fixes applied, and the cheap-tier re-run |

**Result in one paragraph (16 Oct 2026, end of day).** Seven videos rendered and passed all ten QA checks with byte-identical re-renders: three Opus 5.5 references, three Haiku 5.5 builds from the guides alone, and one Haiku rebuild of physics with the new Production Kit. Eight blind Opus judges scored the reference above the guides-only Haiku build on every lens (104 to 75 of 150 across the six first-round verdicts); the science was correct in every build, the gap was visual richness, the confrontation of the misconception, and empty screen time. The Kit closed the measurable half of the gap in one iteration (physics visual lens 10 → 14, empty seconds 11 → 4.5) and none of the judgement half (pedagogy 14 → 14, style 2 → 2), which now goes into template code and detectors rather than prose. Twenty pipeline gaps found by the lead and the builders were fixed in the tooling and promoted into sections 05, 06, 07, 12, 13 and 15; two of them (a 0.6 s video lead and GPU raster nondeterminism) would have shipped unnoticed without the judges. Videos: `deliverables/`. Report: `COMPARISON_and_GAPS.md`. Verdicts: `judging/SUMMARY.md`.

| Also here | What |
|---|---|
| `deliverables/` | The seven MP4s under descriptive names, with `SHA256.txt` |
| `judging/` | Blind A/B folders per subject (tier names scrubbed), the eight verdict JSONs, `mapping.json` (unblinding), `SUMMARY.md` |
| `physics/haiku_v2/` | The Haiku rebuild against the Production Kit v0.1.0 |
| `tooling/JUDGE_RUBRIC.md`, `prepare_judging.py`, `compile_verdicts.py` | The judging protocol and its scripts |

**Constraints that shaped the pilot.** Narration is Path B with a stock English ElevenLabs voice (George): the account is on the Free plan, which blocks library voices through the API and allows 10,000 characters a month, so each video carries at most 1,000 spoken characters (60–70 s). No human approvals were taken; nothing here is releasable. Tooling runs inside the project venv and the installed Google Chrome, so nothing was installed system-wide.
