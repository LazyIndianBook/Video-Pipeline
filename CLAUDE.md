# Video Pipeline: rules for Claude Code

This repository produces the ExamLeaf / Professor Diki Simplified videos: the research, the decision registers, the skills, the lesson scripts and scenes, and the tooling that narrates, renders and checks them. Rendered media is not in git (`.gitignore`); rebuild it with the pipeline (below).

## Where the rules live (the newest decision wins)

- `17_professor_diki_simplified/DECISIONS_PD.md`: PD-01…PD-29a, binding for shorts (house style, script, pace, voice).
- `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`: RD-01…RD-55, the runbook register.
- `15_content_engine_v2/DECISIONS_CE.md`: CE-01…CE-124, the engine specification.
- Record each new decision in the register it belongs to, with its date and source, and update that section's README.

## Standing rules

1. `00_source/` is read-only provenance. Never edit it.
2. Shorts follow PD-19…PD-28a. The house style is paper cut-out collage, never flat or dark. No "AI-generated" line appears on screen or in the speech; the declaration goes in the upload metadata (PD-20). The brand appears only as the opening ident and on the end card (PD-21). Each short is a complete, definition-led explainer with no quiz devices (PD-24). Tell it as a story (PD-25), follow the "100 Seconds" method (PD-26), use plain continuous speech (PD-27), and keep it fast and packed: 150–205 words per 60 s (PD-28, PD-28a).
3. Science comes from fixtures. On-screen values must equal the fixture values (QA A3).
4. The voice is local VoxCPM2 through MLX Audio, cloned from the founder's voice; ElevenLabs is retired (PD-29, RD-55). Until `~/Movies/DikiStudio/voice/reference.wav` exists, test builds use the designed test voice (PD-29a), and those builds are never released. Never commit the founder's voice recording.
5. Every video must pass `qa.py` (A1–A21) and receive two human approvals bound to its hashes before release. Nothing in this repository is approved for release yet.
6. On the 16 GB Mac, run one narration or render job at a time, and never two renders at once.
7. Install nothing system-wide. The tooling runs from `~/Movies/DikiStudio/.venv` (`05_narration_system/local_voice_voxcpm2/SETUP.md`).
8. Ultracode is banned in production and in unattended runs (RD-48).

## Making a video

```sh
PY=~/Movies/DikiStudio/.venv/bin/python; T=16_pilot_builds_2026-10-16/tooling; V=<video folder>
$PY $T/check_script.py $V/script.json          # plan, word band, pauses, givens
$PY $T/preview_scene.py $V/script.json s01     # look at every preview PNG
$PY $T/narrate_voxcpm.py $V/script.json        # local voice per beat; listen to any LISTEN beat, then --redo it
$PY $T/narrate.py $V/script.json               # timeline, mix, captions, cue sheets (add --tempo to fit 60 s)
$PY $T/render.py $V/script.json                # about 12 min per 60 s short on this Mac
$PY $T/qa.py $V/script.json                    # A1–A21 → $V/qa/report.md
sh 17_professor_diki_simplified/tests/run_all.sh
```

Full builder steps are in `17_professor_diki_simplified/07_PIPELINE_CHANGES.md` §4.

## Rebuilding media

Git ignores videos (`*.mp4` and the like), frames cut from them (`frames/`, `_scratch/`), scene previews (`_preview/`) and narration audio under `narration/`. They stay on the machine that made them. The narration timings (`align.json`, `timeline.json`), cue sheets, QA reports and contact sheets are versioned. A build's media comes back from the commands above: `narrate_voxcpm.py` re-voices only beats that are missing from its cache.
