# ExamLeaf Super Teacher — authoring starter pack

Version: 1.0 • research checked 13 October 2026

This pack contains original instructional materials and ten custom Skill drafts, not an installed plugin or completed production platform. No audio or video was synthesized. Claude/Codex model evaluations and student-learning experiments have not been run. The local linter tests are structural tests only.

## Contents
- `Super_Teacher_Guide.md`: original personality and production standard.
- `examples/Complete_Sample_Script.md`: full original chemistry lesson.
- `examples/sample_lesson.json`: 16 planned beats over 600 seconds, clean narration and visual directions.
- `skills/`: ten portable Skill folders with local contract references and evaluation prompts.
- `prompts/`: master authoring, conversational repair and independent review prompts.
- `references/`: evidence/capability ledger and an analogy-card example.
- `tools/lint_script.py`: standard-library-only structural checker.
- `evals/`: local checker tests and test report.

## Use
Read the guide and research limits first. Copy the desired Skill directories from `skills/` into `.claude/skills/` in a Claude Code repository, or `.agents/skills/` for Codex. These are alternatives; keep one canonical source and avoid duplicate drifting copies. No installation is performed by this pack. Confirm discovery against your current client documentation.

In Claude Code, invoke an installed skill by its slash command, for example `/examleaf-lesson-architect`. In Codex select/name the skill using the supported interface. Do not assume Claude-specific frontmatter or invocation controls transfer unchanged.

Run locally from this directory:
```bash
python tools/lint_script.py examples/sample_lesson.json
python -m unittest discover -s evals -p 'test_*.py'
```

The sample's 600-second timeline is planned, not measured audio. Inspect the generated voice, captions and animation and revise durations. External learner pauses add study time.

## Production safeguards
Use permitted source packets, pin tool/model versions, keep answer keys independent of creative drafting, and get human academic and final rendered-video approval. Record native-language review, narration consent/licensing and asset permissions. A passing linter does not establish correctness, accessibility or learning efficacy.

## Research and third-party material
See `references/Research_Ledger.md` for consulted primary research, academic reviews and official documentation. The pack does not redistribute third-party Skills, textbooks, model weights, fonts or media assets.
