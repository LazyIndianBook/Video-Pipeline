# HyperFrames notes

HyperFrames is ExamLeaf's default composition and render harness (report §2.3, §2.6 [Recommendation]: "HyperFrames is the master timeline").

## Verified facts (evidence set)

| Fact | Source |
|---|---|
| Requires Node.js 22+ and FFmpeg | [N8] |
| Scaffold: `npx hyperframes init my-video` | [N9] |
| Claude Code plugin: `claude plugin install hyperframes@hyperframes` (add the marketplace first) | [N10] |
| Agent skills: `npx skills add heygen-com/hyperframes` (tutorial source) | [N58] |
| "HyperFrames ships 21 skills agents load on demand" | [N11] |
| Codex archive build fails above Codex's 100 MB upload limit | [N12] |
| Clone with `GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` to skip LFS payloads | [N13] |
| Apache 2.0, "no per-render fees or commercial-use thresholds" | [N14] |
| Compositions expose `window.__hf` with duration and seek; "the renderer never calls play()" | [N68] (contested) |
| "rAF doesn't fire in beginFrame mode" | [N69] |
| "drop back to a single worker for video-heavy renders" | [N70] |

## Not verified (report §11.4)

- The exact `window.__hf` shape. The scene template defines `window.__hf = { get duration(), seek: t => window.seek(t) }` as an adapter so a scene satisfies both the HuggingFace contract [N72] and HyperFrames [N68]; confirm against the installed version before the pilot.
- Preview and render CLI commands (the tutorial gives none [N58]). Record the verified commands in `contract.md` after the pilot install; this skill runs whatever is recorded there.
- Bundled tween library (GSAP or other), worker settings, 9:16 presets, font and Indic shaping in its Chrome build, the list of its 21 skills.

## ExamLeaf usage rules [Recommendation]

1. Advanced-layer scenes are plain HTML/CSS/JS implementing the contract; HyperFrames places them on the master timeline with Manim, SVG, three.js and Blender clips (report §2.6).
2. Lint with `--hf` for HyperFrames targets.
3. Any tween library is acceptable only if its timeline is driven by `seek(t)` (paused timeline, time set explicitly), never by playing (report §2.3 GSAP note). GSAP has its own standard licence, not MIT (library install guide §7).
4. Video-heavy compositions: `SCENE_META.workersMax = 1` [N70].
5. Disable on-demand skill auto-install in production; admit HyperFrames skills through `examleaf-skills-security` (library install guide §6).
6. Do not install both compositor suites by default (VE skills README); Remotion is a benchmark challenger only.

## Failure signatures

| Symptom | Likely cause | Fix |
|---|---|---|
| Render never finishes | rAF wait in scene, or `window.ready` never resolves | Lint F07; check `window.__errors` |
| Black or repeated frames in clips | Several videos seeking in parallel | One worker [N70] |
| Install fails | Node < 22 or no FFmpeg | Preflight [N8] |
| Clone slow or fails | LFS payloads | `GIT_LFS_SKIP_SMUDGE=1` [N13] |
| Codex build fails | Archive over 100 MB | Trim assets [N12] |
