# Brief anatomy: from L1 prompts to an ExamLeaf L3 brief

This reference explains what each part of the animation brief does and where it comes from. Citations follow the research report (`12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`).

## 1. The three levels ([V2], report §1.1)

| Level | What the creator gives the model | Observed result | ExamLeaf use |
|---|---|---|---|
| L1 | One line ("Use JavaScript to animate a black hole") | "Random": sometimes great, sometimes "ridiculous" | Style exploration in a sandbox only |
| L2 | Reference style + reference video + strict pacing + creative direction + Python music, optional harness | Convincing look; first pass "flat", fixed by iteration | The minimum for production |
| L3 | L2 + MCP orchestration (clips, narration, music) + a rendering harness; human still supplies plan, reference and pacing research | Per-scene raw JS, voices and music on a timeline | ExamLeaf's target, with ExamLeaf's own narration and fixtures |

[V2]'s presenter says the human still provides three things the model "is still not fully capable of handling": the plan, the reference video and the pacing research. ExamLeaf maps them onto existing artifacts (report §1.1 [Recommendation]):

| Human-owned input in [V2] | ExamLeaf artifact | Owner skill |
|---|---|---|
| Plan / idea | Lesson plan + storyboard route + approved storyboard grid | `examleaf-lesson-plan`, `examleaf-storyboard-route`, `examleaf-anim-storyboard-gate` |
| Reference video | House style guide (+ optional reference analysis numbers) | `examleaf-style-guides`, `examleaf-reference-analyzer` |
| Pacing research | Hold schedule + cue sheet | `examleaf-pacing-controller`, `examleaf-cue-sheet` |

## 2. What [V3] and [V4-MP] add

- **Massive, detailed prompt plus a reference for pacing** beats "make a stunning premium video" ([V3], report §1.2).
- **Brand hex codes in the prompt** ([V3]). ExamLeaf passes a brand-tokens file instead of pasting hexes, so tokens stay versioned.
- **"Do not inspect any of my older projects or folders"** ([V3]). ExamLeaf adds a per-job workspace and copies inputs into it.
- **Ask for audio explicitly** ([V3]); in ExamLeaf audio is produced by `examleaf-audio-compose` and mixed by `examleaf-audio-production-engineer`, so the brief says what the scene must not do (no audio decisions), not what to compose.
- **The script is the weak point when the agent writes it** ([V3]). The brief therefore marks the script read-only.
- **A style guide can replace the reference video** ([V4-MP]): look, palette, typography, motion vocabulary, sync rule, transitions, determinism sentence, sound and asset rules.
- **A review checkpoint before spend** ([V4-MP] "Stop after Steps 2 and 3… wait for my approval"). The storyboard gate's approval record is an input to the brief, so no brief exists for an unapproved segment.

## 3. Section-by-section purpose

| Brief section | Purpose | Failure it prevents |
|---|---|---|
| Header (scene, lesson, language, route, style@version, model, effort, cap, workspace) | Pins every variable that changes output quality or cost | Silent medium effort [N22]; unpinned style; runaway loops (#60) |
| What to build | One scene, 1080x1920, seek-pure, from the approved storyboard beat | Agent inventing scope; 16:9 output (#49) |
| Inputs you may read | Closed list of paths with hashes | Context contamination (#9); stale inputs |
| Typography | Allow and ban lists | Convergent "AI slop" fonts [N50][N51][N55] |
| Constraints block | Ten non-negotiable rules | #12, #15–18, #50, #54, #56, #60 |
| Deliverables | Scene file, scene notes (cue → reveal, fixture field → value), lint report | Untraceable on-screen values; unlinted code reaching the renderer |

## 4. Worked example (physics, refraction hook)

Inputs: approved script segment "Put a straw in water. It looks broken. It isn't."; route `illustrative` overlay on a `data-bound` diagram; style `doodle-handdrawn@1.0.0`; cue sheet with cues `straw_in` at 0.42 s, `looks_broken` at 1.80 s, `isnt` at 3.05 s; fixture `fx-refraction-glass` with `n_air`, `n_water`, `angle_i_deg`, `angle_r_deg`.

What the brief makes explicit:
- The doodle straw draws on at `cues.straw_in.at` (about 0.05 s before the word, [V4-MP]).
- The apparent bend is drawn from `angle_r_deg`; the real straw never changes angle (report §7.13: decoration must not contradict the science).
- "It isn't." is a punchline; the next sheet arrives about 0.3 s after the last word ([V4-MP] transition rule) and the punchline text holds at least 1.2 s [N60].
- No refractive index appears unless `fields_on_screen` lists it.

## 5. Ordering for cache reuse (report §3.3 [Recommendation])

Run one main session per scene batch and keep stable context first and byte-identical between scenes:
1. Constraints block (identical for every scene in a lesson).
2. Harness contract excerpt.
3. Style guide (pinned version).
4. Brand tokens.
5. Scene-specific: script segment, cue sheet, fixtures, creative direction.

Precise caching mechanics and prices are not in the verified evidence set; confirm with the Claude API documentation before modelling savings (report §3.3).

## 6. What the brief deliberately leaves out

- **Model narration or voice choices.** Voice comes from `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter` (report §5.3).
- **MCP permissions.** Granted per job by `examleaf-mcp-orchestrator`, never by the brief (report §6.4).
- **Exact pixel insets.** They live in `vertical_safe_zones.tokens.json` and must be measured; the evidence contains no verified values (report §7.9, §11.9).
- **"Make it stunning" adjectives.** [V3] shows they produce generic results; reference-driven layout and typography beat adjectives.
