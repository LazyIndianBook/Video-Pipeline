# ExamLeaf Video Engine — initial implementation and research

**Date:** 13 October 2026. **Status:** tested local technical proof, not a production release.

## What is actually implemented
- Strict typed source/claim/scene/cue/asset/job/short/review contracts.
- Native PDF text extraction with file hashes and page references (tested on a synthetic PDF; not the full ExamLeaf books).
- Four bounded scientific model checks: RC charging, H2/O2/H2O atom balance, the derivative of (3x+1)^2, and a single-locus Aa×Aa cross.
- Frame-driven native SVG → CairoSVG → FFmpeg rendering, independently reflowed for 16:9 and 9:16.
- Eight real 30-second silent MP4s, captions, sampled SVG/PNG frames and hash-based manifests.
- Two-worker local batch execution, cache integrity checks, atomic output files, a cents-based budget ledger, fail-closed provider interfaces and a local release-policy demonstration.
- 56 passing unit/contract/media integration tests. See outputs/tests.txt.
- 32 original Skill instruction drafts with input/output contracts, steps, references, handoff templates and authored evaluation cases. These Skills have NOT been run or evaluated in Claude/Codex.

## What is not implemented or approved
The four 600-second plans are outlines, NOT complete narrated ten-minute videos. HyperFrames, Remotion, Manim and Blender were researched but not installed or run. Distributed scheduling, cloud deployment, native TTS provider adapters, forced alignment, authenticated human-review service and platform publishing remain proposed. No teacher approval or student study was performed. Canvas-bounds checks do not prove every overlap/accessibility property.

A separate connected Runway speech call returned an audio asset (32.182857 seconds, 9 workspace credits). Its local download was blocked by the environment and it is not synchronized into the previews. This confirms one connector speech operation, not the packaged provider adapter, final voice quality, Assamese support or video generation. See outputs/live_speech_probe.json.

Browser preview automation was attempted but local HTTP navigation was blocked by administrator policy. That limitation was not bypassed. See outputs/browser_smoke.json. Media decoding/probing tests passed independently.

## Run the offline proof
Python 3.11+ is declared; the observed environment used Python 3.13.5 on Linux. The reference font path is Debian/Linux-specific. Use Linux/WSL for the supplied proof; a native macOS/Windows port must configure the equivalent DejaVu path in visuals.py and rerun the tests. Install FFmpeg/ffprobe, Cairo and DejaVu Sans through trusted OS package channels. Font binaries are not included.

```sh
python -m venv .venv
# Activate your virtual environment using the command appropriate for your OS.
python -m pip install -e '.[chemistry,test]'
PYTHONPATH=src python -m examleaf.cli validate examples/physics_rc.json
PYTHONPATH=src python -m examleaf.cli batch --workers 2
PYTHONPATH=src pytest -q
python -m http.server 8000 --bind 127.0.0.1
# Open http://127.0.0.1:8000/preview.html on your machine.
```
The PYTHONPATH examples are POSIX shell syntax for the Linux reference environment. Dependency installation was not executed in this network-restricted environment; preinstalled versions were used and are recorded in manifests. Use a reviewed fully hashed lock/container digest before production.

The batch command accepts only the four supported example scene JSONs and ignores *_600s_plan.json. Do not place unrelated JSON schemas in examples/ and expect automatic support.

```sh
PYTHONPATH=src python -m examleaf.cli render examples/chemistry_balance.json --aspect 9:16 --out outputs
PYTHONPATH=src python -m examleaf.cli extract-pdf your-permitted-source.pdf --out source-native.json
PYTHONPATH=src python -m examleaf.cli release-check outputs/physics_rc_16x9.mp4 outputs/physics_rc_16x9.manifest.json
```
The last command MUST currently exit with a blocking result: previews lack narration and genuine academic/full-video approval. Do not bypass it by fabricating JSON reviewer identities. Production needs an authenticated approval service.

## Where to start
- docs/Architecture.md — exact target architecture, routing and staged ownership.
- docs/Production_Runbook.md — workflows, budgets, retries and release checks.
- docs/Four_Pilots.md — measurable full-lesson pilot plan and actual preview benchmarks.
- docs/Super_Teacher_Contract.md — teacher identity and narration constraints.
- docs/Security_and_Installation.md — public Skill/MCP admission process.
- research/Public_Skills_Directory.md and CSV — verified public shortlist and limitations.
- research/custom_skills.csv — full 32-Skill backlog.
- research/subject_libraries.csv — subject-specific modules and boundaries.
- ExamLeaf_Video_Engine_Cost_Model.xlsx — editable assumptions and calculations.

## Engineering boundaries
The native renderer is a reference adapter, not a new general-purpose animation framework. The mathematics fixture deliberately rejects parameters other than its reviewed worked example. Science checks prove only specified model invariants, not universal correctness, source rights or board fit. No arbitrary expression evaluation from uploaded content is implemented. Cache keys currently hash all source files (safe but broad invalidation); production should move to tested adapter-scoped dependency hashes. Reproducibility is observed within this environment, not guaranteed byte identity across GPUs/OSes.

## Rights
Original scaffold and drafted Skills are provided for ExamLeaf adaptation. Third-party package, font, model, voice and asset rights remain separate. No third-party Skills, fonts, credentials, temporary signed audio URL or source textbook is bundled. Source references support original examples; they do not authorize copying a complete textbook or illustration set.
