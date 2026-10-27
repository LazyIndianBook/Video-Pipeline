# ExamLeaf authored Skills
32 original task-specific instruction packages. **Not yet evaluated in Claude Code or Codex.** Some call locally tested deterministic helpers; this is a separate evidence level.

Copy only the needed folder into `.claude/skills/` for Claude Code or `.agents/skills/` for Codex after reviewing it. Keep one canonical source tree here. Never mass-load all 32 into every model request. Do not install both compositor suites by default.

Every Skill contains SKILL.md, references, an output handoff template and authored positive/negative evaluation cases. Shared deterministic scripts are in `src/examleaf` and `scripts`; duplicating executables into every Skill would create drift.
