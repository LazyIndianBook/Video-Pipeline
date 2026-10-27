# ExamLeaf Narration System — implementation starter

**Status: offline-tested sidecar, not a finished production speech service.** Created13October2026. Integrates with the prior ExamLeaf Video Engine through manifests, not by changing its scientific renderers.

## Deliverables
15 original narration Skill drafts;40 explicit English STEM speech mappings; Pydantic contracts and JSON schema; four current/snapshot provider-profile recipes plus one legacy migration fixture covering four providers; deterministic sample-index timeline; protected response windows; prototype captions; waveform and two-pass loudness tooling; cache/invalidation checks;57 passing local tests; public directory and voice/evaluation guides.

Two live Eleven v3 auditions were generated through the connected Runway service. They were not transferred into this runtime, listened to or mastered here. Local signal fixtures demonstrate engineering timing only. No new voice clone was created.

## Run
Requires Python3.11+ and a reviewed FFmpeg build on PATH. The environment used Python3.13.5; exact recorded package versions are in outputs/environment.json; see outputs/environment.json for the captured versions. Dependency ranges in pyproject are not a fully hashed reproducible lock. Pin target deployment wheels/container before production.

```bash
python -m venv .venv
# Activate your environment.
python -m pip install -e '.[test]'
PYTHONPATH=src python scripts/build_examples.py
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m examleaf_narration.cli validate examples/teacher.json
PYTHONPATH=src python -m examleaf_narration.cli compile examples/teacher.json --lexicon configs/pronunciation.json --profile configs/gemini_38.json --out outputs/request_preview.json
```

The compile command sends **zero network requests**. Placeholder IDs and ENV markers are configuration templates, not credentials. Production HTTP transport, billing ledger and authentication are not implemented. Do not blindly execute request JSON.

```bash
PYTHONPATH=src python -m examleaf_narration.cli qa outputs/timing_fixture_NOT_SPEECH.wav --out outputs/local_qa.json
PYTHONPATH=src python -m examleaf_narration.cli release-check outputs/timeline.json
```

The release check intentionally exits2. It requires true speech and an authenticated approval service; local self-asserted booleans cannot approve a production lesson.

## Next engineering steps
1. Cast native-appropriate licensed voices and approve the corpus.
2. Implement one provider transport, persist actual usage/jobs and test failure/recovery.
3. Import independent ASR and actual forced alignment; validate numbers and language resources.
4. Connect timeline.events to the existing renderer; re-align or remap after any audio trim/time change.
5. Complete four narrated subject pilots with full academic, native-language, caption and listening reviews.
6. Only then expand the batch queue and commercial catalogue.

See docs/Provider_Lifecycle.md, docs/Implementation_Roadmap.md, docs/Architecture.md, docs/Voice_Identity_Guide.md, docs/Audition_and_Evaluation.md, research/Public_Narration_Directory.md and configs/existing_engine_skill_mapping.json. Custom Skills are authored but have not been run through Claude/Codex evaluations. No font, model-weight, third-party repository or reference-performer audio files are redistributed.
