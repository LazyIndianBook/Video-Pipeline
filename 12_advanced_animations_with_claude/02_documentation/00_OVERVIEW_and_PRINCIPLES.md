# 00 · Advanced animations with Claude: overview and governing principles

**What this document is.** The entry point to section 12. It defines what "advanced animations with Claude" means for ExamLeaf, what the five reference videos actually show, which parts ExamLeaf keeps and which it changes, the default tool stack, the one rule that protects scientific accuracy, the governing rules every job must follow, and a map of every file in the section with a reading order for each role.

**Evidence conventions (same as the research report).**
- [V1]–[V5]: the five reference videos (auto-caption transcripts, so wording is approximate). [V4-MP]: the verbatim paper-collage master prompt from the [V4] description, saved at `12_advanced_animations_with_claude/00_reference_videos/master_prompt_paper_collage.md`.
- [N1]–[N81]: verified web claims, quoted in `12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md`. "(contested)" means one of two verifiers did not confirm the claim.
- [Recommendation] = design judgement by this section. [Hypothesis] = plausible but untested. "verify" = a fact this section could not confirm. Nothing in this section has been installed or run.
- Edge cases are cited by their master number **#1–#65** from §8 of `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`.
- Existing project rules are cited by path and, where one exists, by runbook decision number (RD-xx in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). Section decisions are AD-xx in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`.

---

## 1. What "advanced animations with Claude" means

### 1.1 The core idea in four sentences

1. Claude does not make video. Opus 5.5 "outputs text only" [N71]. Asking it for an MP4 gets nothing (#14).
2. Claude writes **scene code**: HTML/CSS/JavaScript, Canvas 2D, SVG, three.js, React (Remotion) or Python (Manim, NumPy audio).
3. A separate **seek-based renderer** turns that code into frames. It never "plays" the scene. It sets a time `t`, captures the frame, and repeats for every frame. The evidence for this pattern:
   - opus-js-animations: "headless Chrome renders frame i as seek(i / fps) across parallel workers" [N18];
   - HyperFrames: "The renderer never calls play()" [N68] (contested);
   - a HuggingFace tutorial's contract: the scene "must set `window.DURATION` and expose `async window.seek(t)`" [N72].
4. Because the renderer jumps to arbitrary times, every scene must be a **pure function of time**: the same `t` always gives the same picture [N61] (contested). Randomness must be seeded (#17), loops must be finite (#18), and nothing may read the wall clock (#15).

The full contract is in `12_advanced_animations_with_claude/02_documentation/04_HARNESS_CONTRACT_and_DETERMINISM.md` and `12_advanced_animations_with_claude/04_harness_contract/contract.md`.

### 1.2 What it is good at, and what it is not

| Good fit | Poor fit | Evidence |
|---|---|---|
| Designed motion, kinetic typography, diagrams, procedural 2D (doodle, collage), stylised 3D (voxel, orbitals) | Photoreal humans and real-world physics footage | Opus 5.5 "does not natively behave like a cinematic text-to-video model" [N62] (#52) |
| Anything whose state can be computed from validated data at time `t` | Anything that needs the model to "hear" audio or "see" a reference video without help | The model is text-only; give it an analysis JSON (#13) [N71] |
| Scenes that must re-render identically for QA and approvals | Real-time interactive play, wall-clock effects | Seek-only rendering [N68] (#15) |

### 1.3 "Claude Motion" is a community term

No verified source names a product or feature called "Claude Motion". [V1]'s description says "Opus 5.5 Motion Graphics", and a third-party tutorial dates Opus 5.5 to 22 Sep 2026 without a link [N59] (#59). Inside ExamLeaf, "Claude Motion" may be used only as an informal name for this code-to-video layer (AD-10). Asking Anthropic whether an official feature exists is open question Q1 in doc 14.

---

## 2. The three levels of quality ([V2])

[V2] describes three levels. ExamLeaf adopts Level 2 as the minimum for production and Level 3 only through ExamLeaf's own adapters.

| Level | What [V2] shows | Result in [V2] | ExamLeaf stance |
|---|---|---|---|
| **L1** One-line prompt | "Use JavaScript to animate a black hole." Opus uses JS and internal tools. | "Essentially random": sometimes great, sometimes "ridiculous" | **Exploration only.** Never in production (#7). Useful for trying a new style in a sandbox. |
| **L2** Structured prompt + references | A reference style and an actual reference video; strict pacing instructions; creative direction "to keep viewers watching"; Python-composed sound and music; optionally HyperFrames or Remotion for render control. Effort high or xhigh ("extra"); model contained in one workspace. | Convincing doodle story with good music; critique "flat and cartoonish", "strictly 2D" fixed by iteration | **Production default.** The ExamLeaf brief (doc 02) is a stricter L2: reference analysis numbers, brand tokens, harness contract, cue sheet, fixtures, forbidden list, iteration cap. |
| **L3** Orchestrated production | Human supplies three things the model "is still not fully capable of handling": the plan/idea, the reference video, the pacing research. Opus writes JS, uses MCP servers (clips/B-roll, studio narration, a "music studio MCP") and a harness. Demo prompt included "don't stop working until the animation matches the exact quality of the reference video". | Per-scene raw-JS animation, voices and music placed on a HyperFrames timeline | **Allowed with changes.** The three human inputs map to ExamLeaf artefacts (lesson plan + storyboard route; house style guide; pacing controller). MCP calls go through `examleaf-mcp-orchestrator` with a credit ledger. "Don't stop until it matches" is replaced by an iteration cap and a QA rubric (#60). |

Details, ingredients and worked briefs: `12_advanced_animations_with_claude/02_documentation/02_PROMPTING_the_structured_brief.md`.

---

## 3. The four workflows the videos show, and what ExamLeaf keeps or changes

### 3.1 Workflow A: effort sweep on a music video ([V1])

**What happens.** Devarf ran the same "make a music video" prompt through Opus 5.5 at low, medium, high, xhigh and max, plus one ultracode run, in Claude Code 2.1.287 in the terminal, on a 79-second song clip. Each run had its own folder with "some information and tools": a tools folder with three.js, Canvas 2D, SVG and frame-conversion tools, and no guides or examples. Because "the AI cannot hear the song", he first ran a custom audio-analysis tool (beats, notes, instruments, dynamics, lyrics, a plain note on meaning) at high effort.

**Measured results** (one creator, single runs, estimated at API prices; he paid by subscription):

| Run | Visual | Wall time | Tokens | Est. API price |
|---|---|---|---|---|
| Low | 2D | ~42 min | ~78K | ~$3 |
| Medium–xhigh | 3D | between low and max (not stated per level) | — | — |
| Max | 3D | ~3 h | ~625K | ~$49 |
| Max + ultracode | 2D character on a 3D card stage | did not finish | ≥2.5M | ≥$348 |

| Keep | Change |
|---|---|
| Headless terminal sessions, one folder per run (#9) | No "work on its own… not to stop and ask": every job has a storyboard gate and an iteration cap (#47, #60) |
| A tools folder with renderers and frame converters (the ExamLeaf harness) | No ultracode in any production or unattended run (#3, #4) |
| An analysis JSON so the model can "hear" timing (#13): ExamLeaf uses word timestamps from alignment plus a beat grid | Effort set explicitly per task, because Opus 5.5 silently defaults to medium (#1) [N22] |
| Effort tiers as a cost lever | Budgets per scene, logged by `examleaf-effort-governor` |

### 3.2 Workflow B: JavaScript 2D animation, L2 and L3 ([V2])

**What happens.** L2: a doodle-style reference video, a ~20 s story outline, "compose original background music using Python", Opus at high/xhigh, contained in a workspace. L3: the paper-collage reference, a story, "make it funny", "use the MCP servers I have connected", HyperFrames opened as a side panel with a scene timeline, Higgsfield MCP for voices.

| Keep | Change |
|---|---|
| Reference style + reference video + pacing instructions | Reference videos are analysed into numbers first (`examleaf-reference-analyzer`); copyrighted references are for analysis only, never asset reuse |
| Python-composed music and SFX | Music is off under teaching in lessons; Python beds for hooks, transitions, outros and Reels only (AD-15) |
| HyperFrames as the timeline and render harness | HyperFrames is the master timeline; Remotion is benchmarked (AD-01) |
| Ask for depth explicitly (parallax, foreground strips, shadows): [V2]'s first pass was "flat" | "Don't stop until it matches" is banned (#60); MCP voice is replaced by ExamLeaf's TTS adapter |

### 3.3 Workflow C: motion graphics with Remotion ([V3])

**What happens.** Claude is asked to "download and set up the latest version of Remotion directly in the project folder" and research its current docs; Remotion Studio opens with a composition list. A "massive, detailed prompt" plus a reference video for pacing; "study the reference video's layout structure and its exact typography treatment"; brand hex codes; "do not inspect any of my older projects or folders". Audio must be requested ("generate the sound effects and background music using Python"). An orchestrated Vox-style sun-vs-planets demo used all connected MCPs "without errors", but its AI-written script was the weak point.

| Keep | Change |
|---|---|
| Long structured brief; layout and typography study; brand hex codes | Brand tokens come from `02_learning_psychology/palette_and_typography_tokens.json` and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`, never improvised |
| "Do not inspect other folders" (#9) | Enforced by workspace layout and permissions, not only by the prompt (doc 01 §8) |
| Ask explicitly for audio (#10) | Audio stems are produced by `examleaf-audio-compose`, mixed by the existing `examleaf-audio-production-engineer` |
| Remotion skills as a benchmark candidate | Remotion is benchmarked, not adopted, until its licence is confirmed (open question Q3) |
| — | **The script never comes from the animation agent** (#11). [V3]'s model "did its own proper research"; in ExamLeaf any on-screen fact comes only from validated fixtures (#12) |
| — | "Full permission to use all the MCPs" is never granted; MCP tools are enabled per job (doc 05 §8) |

### 3.4 Workflow D: style-guide master prompt with a storyboard gate ([V4], [V4-MP])

**What happens.** One master prompt replaces the reference video with a written style guide. Steps: study the style guide → write a 60 s script (140–160 words) → 3×3 storyboard grid via Higgsfield MCP (GPT Image 2.5) → "⛔ Review checkpoint… wait for my approval" → voiceover via Higgsfield (ElevenLabs v3, preset "Arthur") → image assets → JavaScript animation synced to the voice → music and SFX. [V4] says the style is "on the expensive side regarding credits". The video is sponsored by Higgsfield.

| Keep (the structure) | Change (the content) |
|---|---|
| Style guide → storyboard grid → **hard human gate** → voice → assets → animate → audio → compile (#47) | Script from the Super Teacher system with science review and academic approval (GA), not the agent (#11) |
| The written style guide as the reference | The style guide is re-laid out for 1080×1920 (#49); see doc 03 |
| Seeded randomness, finite repeats, a timeline "that can jump to any frame" | Voice from `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter` (Indian English, Hinglish, Hindi), not "Arthur" |
| Text, tape, doodles and UI built in code | Labelled science visuals come from SVG/Manim fixtures; image models never draw text or formulas (#54) |
| The reveal-on-the-word sync rule | Storyboard thumbnails are code-rendered first; Higgsfield only when look-dev needs it, under a credit ledger (#41, #42) |

### 3.5 The Fable 5.5 signal ([V5])

[V5] reports a leak-based claim that a newer model ("Fable 5.5") produced style-morphing animation, physics Rube Goldberg machines and a voxel island "50–60% better" than Opus 5.5. None of it is verified. [N26] confirms only that a "Fable" model family exists in Claude Code. ExamLeaf does not plan on it (#57): the harness stays model-agnostic, and any model switch re-runs the determinism and science QA first (AD-03).

---

## 4. The recommended default stack

[Recommendation] The stack below is the report's §0 item 10 and §2.6, aligned with the existing compositor decision RD-07 (native SVG = reference renderer; HyperFrames first candidate; Remotion measured alternative; select exactly one).

| Layer | Default | Role | Evidence | Status |
|---|---|---|---|---|
| Authoring agent | Claude Code, Opus 5.5 at explicit **high** effort (xhigh for complex 3D/physics; medium for planning text; never ultracode) | Writes scene code, prompts, small tools | [V1], [V2], [N22]–[N26] | AD-02 |
| Master timeline and renderer | **HyperFrames** (Node 22+, FFmpeg; Apache-2.0, no per-render fee) | Composes the 1080×1920 lesson/Reel; imports every clip | [N8], [N9], [N14], [N68]–[N70] | AD-01; benchmark in `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md` |
| Benchmark challenger | **Remotion** (skills via `npx skills add remotion-dev/skills`) | Same three test lessons; licence must be confirmed first | [N1]–[N7], [N63]–[N67] | Benchmark only |
| Data-bound diagrams | Existing **SVG proof renderer** and **Manim CE** (`examleaf-svg-scenes`, `examleaf-manim-scenes`) | Axes, values, equations, structures | `04_video_engine/`; [N44]–[N49] | Existing; Manim CE only (#28) |
| Light 3D | **three.js** via a raw seek pipeline (`examleaf-threejs-scenes`) | Orbitals, lattices, field lines, voxel recaps | [N18], [V1] | New; render-box policy (#65) |
| Hero 3D (rare) | **Blender**, scripted and seeded, headless (`examleaf-blender-scenes`) | Spatial hero assets only | [V3]; `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §6 | Existing skill; Blender MCP is an authoring aid only |
| Music and SFX | **Python** (NumPy synthesis, seeded, bar-aligned stems) via `examleaf-audio-compose` | Beds for hooks/transitions/Reels; SFX one-shots | [V2], [V3], [V4-MP] | New; library versions to verify in pilot |
| Beat and onset analysis | **librosa** via `examleaf-audio-analysis` | Beat grid for Reels, onsets/energy for SFX placement | [N36]–[N43], [N81] | New; traps #31–#38 |
| Narration and timing | Existing TTS adapter + forced alignment (`examleaf-voice-synthesis`, `examleaf-tts-provider-adapter`, `examleaf-alignment-localize`, `examleaf-speech-animation-synchronizer`) | Word timestamps into the cue sheet | `05_narration_system/` | Existing; only voice path |
| Raster assets (optional) | **Higgsfield** (GPT Image 2.5) for storyboard grids and collage cutouts only, under a hard credit budget | Look-dev and cutouts; never science, never text, no premium video models | [V4-MP], [N29]–[N35], [N75]–[N80] | AD-08; ledger in doc 05 |

Not adopted: Motion Canvas (no verified evidence; AD-27); premium video generators (default generated video = 0 s, RD-39); style-morph montages ([V5], unverified, rarely useful for teaching).

---

## 5. The accuracy invariant

[Recommendation, report §9] **Any glyph that encodes science must be traceable to a fixture field.** That covers numbers, units, chemical formulae, labels, arrow directions, angles, ratios and graph shapes.

How it is enforced across the section:

1. **Routing.** `examleaf-storyboard-route` tags every scene. Only `illustrative/narrative` and `typographic` scenes go to free-form Claude scene code. `data-bound` scenes go to the existing SVG, Manim, molecule and biology skills (or to three.js scenes fed from fixtures); `spatial-hero` goes to Blender.
2. **Read-only props.** Scene code receives fixtures as read-only data staged into the job folder with their hashes (doc 01 §8). Claude never types a scientific value into code.
3. **Mixed scenes.** An illustrative scene that shows a science element (a refracted ray in a doodle hook, a planet-size ratio in an editorial scene) treats that element as data-bound: its geometry comes from the fixture, and decoration may not change an angle, a ratio or a direction the lesson teaches (report §7.13). Wobble, boil, push-ins and shakes are switched off on that element and during its reveal (#64).
4. **No image-model science.** Image models never draw text, formulas or labelled diagrams (#54). Text is always built in code.
5. **QA diff.** `examleaf-anim-qa` compares rendered text (DOM text dump or OCR) against fixture fields; a mismatch is a critical defect that blocks release regardless of visual score (existing rule in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`).
6. **Human approval.** Academic approval (GA) of the script bundle and full final-video review (GF/GS) remain the only release authority. Agents never approve.

---

## 6. Governing rules

Every animation job follows these rules. Each one names the edge cases it prevents and where it is specified.

| # | Rule | Prevents | Specified in |
|---|---|---|---|
| G1 | **Set effort explicitly** for every run and log the effective model and level. Defaults: scene code high; complex 3D/physics xhigh; planning text medium; max only with a written justification. | #1, #2, #5 | doc 01 §7; skill `examleaf-effort-governor` |
| G2 | **Never ultracode** in production or unattended runs. It can only be started with `claude --effort ultracode` [N24] and cannot be persisted [N25]; audit launch scripts for the flag. | #3, #4 | doc 01 §7; AD-02 |
| G3 | **Pin full model IDs**; aliases resolve differently on other providers [N28]. Keep the harness model-agnostic; a model switch re-runs QA. | #6, #57, #62 | doc 01 §7; AD-03 |
| G4 | **Iteration cap: 3 fix loops per scene** against the rubric during authoring; after an automated QA or render failure, the existing VE rule applies (at most two repair attempts, then human escalation). Never "don't stop until perfect". | #60 | AD-11; doc 02 §3.16 |
| G5 | **One isolated workspace per job.** The agent reads only its job folder; sibling folders and old projects are denied by permissions as well as by the prompt. | #9 | doc 01 §8 |
| G6 | **Secrets outside the repo**: environment or user config only ([N19] pattern); provider calls run in the provider worker, not in the scene workspace. | #40 | doc 01 §6, doc 05 §8 |
| G7 | **Storyboard gate before any paid asset or scene code**: 3×3 grid, beats.json, estimate.json, human approval bound to hashes. | #41, #42, #47 | doc 05 |
| G8 | **Vertical only**: 1080×1920 at 30 fps, safe-zone tokens, 16:9 references re-laid out, never cropped. | #49, #51 | doc 03 §3; AD-07 |
| G9 | **The script never comes from the animation agent**; the agent may not write, edit or "improve" approved text. | #11 | doc 02 §3.13 |
| G10 | **On-screen facts only from fixtures**; the agent may not research facts. | #12 | §5 above |
| G11 | **Image models never draw text, formulas or labels.** | #54 | doc 05 §10 |
| G12 | **Scenes are pure functions of time**: `window.DURATION`, `async window.seek(t)`, seeded stateless randomness, finite repeats, no wall clock, no rAF polling, single worker for video-heavy scenes. | #15–#20 | doc 04 |
| G13 | **Credits and tokens are capped by the pipeline**, not by the prompt: estimate before call, hard stop, human overrun approval, idempotent job IDs. | #41–#45 | doc 05 §7 |
| G14 | **Audio is mandatory and mastered**: the brief requests audio; loudness is normalised and re-measured after mux. | #10, #39 | doc 14 AD-04 |
| G15 | **No photosensitive flashes**; [V4-MP]'s "white flash or bloom for explosions" is replaced by a non-flashing transition. | #56 | doc 03 §6 |
| G16 | **Renders are offline and reproducible**: staged local assets and fonts only; one pinned render box; double-render frame-hash test. | #17, #55, #65 | doc 04 §6–§10 |

These rules sit on top of the project-wide principles in `README.md` (verified data decides what components display; one Skill owns each output; two human approvals bound to hashes; untrusted content stays data; failures never silently change the lesson).

---

## 7. How the layer plugs into the existing pipeline

[Recommendation, report §9] The advanced-animation layer adds skills at five points in the existing stage map (`06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md`). It removes nothing.

| Existing stage (stage map #) | New or extended skill | What it adds | Doc |
|---|---|---|---|
| 9 Storyboard route | `examleaf-anim-storyboard-gate` (extends storyboard-route), `examleaf-anim-brief`, `examleaf-reference-analyzer`, `examleaf-style-guides`, `examleaf-effort-governor` | Route tags for illustrative/typographic scenes; 3×3 grid; estimate; brief | docs 02, 03, 05 |
| 10 Scene rendering | `examleaf-motion-harness` (extends web-composition), `examleaf-procedural-2d`, `examleaf-kinetic-typography`, `examleaf-threejs-scenes`, `examleaf-vertical-adapt` | Seek contract, linter, primitives, three.js scenes, vertical layouts | docs 03, 04 |
| 14 Alignment | `examleaf-cue-sheet` (extends speech-animation-synchronizer and alignment-localize) | One cue sheet per scene from word timings, beats and SFX | doc 04 §4 |
| 15 Audio | `examleaf-audio-compose`, `examleaf-audio-analysis` | Seeded Python beds and SFX; librosa beat grid | report §5 |
| 16 Visual QA, 15 Audio QA | `examleaf-anim-qa` (extends visual-qa and audio-caption-qa) | Safe zones, hold times, flash check, determinism hash, fixture-vs-text diff, LUFS | doc 04 §7 |
| 21 Observability/cost, 25 Selective generation | `examleaf-mcp-orchestrator`, `examleaf-effort-governor` (extends observability-cost) | Credit ledger, per-job MCP permissions, effort and token logging | doc 05 |
| 22 Skills security | (existing) `examleaf-skills-security` | Admits remotion-dev/skills, heygen-com/hyperframes, klsoen/opus-js-animations, manim_skill (CE) | doc 01 §5 |

**Order inside one lesson or Reel** [Recommendation]:

```text
GA academic approval of script bundle (existing)
  → storyboard-route tags scenes (existing, extended)
  → reference analysis + style guide selection
  → ⛔ storyboard gate: grid + beats.json + estimate.json → human approval bound to hashes
  → narration synthesis + alignment (existing) → cue sheet per scene
  → optional raster assets via mcp-orchestrator (ledger)
  → brief per scene → Claude Code writes scene code in an isolated job folder (≤ 3 fix loops)
  → lint + double-render determinism test
  → HyperFrames master timeline imports clips (Manim / SVG / three.js / Blender)
  → audio bed + SFX + narration mix → loudness normalisation
  → anim-qa + existing visual/audio QA → ⛔ GF / GS full review → export
```

**Development vs production.** The runbook warns that production must not turn "every lesson" into "an expensive, unpredictable coding project" (`07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §3). [Recommendation] Bespoke Claude scene code is therefore limited to illustrative scenes (hooks, analogies, recaps). Once a bespoke scene is approved, its reusable parts are promoted into `examleaf-procedural-2d` / `examleaf-kinetic-typography` templates so the next lesson configures rather than re-codes (AD-23).

---

## 8. Map of the section

Paths are ROOT-relative (ROOT = `ExamLeaf_Video_EdTech_Pipeline/`).

### 8.1 Inputs (read-only)

| Path | Content |
|---|---|
| `12_advanced_animations_with_claude/00_reference_videos/INDEX.md` | The five videos: id, title, channel, date, duration |
| `12_advanced_animations_with_claude/00_reference_videos/<id>/` | `metadata.json`, `description.md`, `transcript_plain.txt`, `transcript_timed.txt` for 3S4vuHxGh7c [V1], MPDhk385gSg [V2], OIAWkkSO4WY [V3], WXu4O9oIdIE [V4], BbsoRYprICI [V5] |
| `12_advanced_animations_with_claude/00_reference_videos/master_prompt_paper_collage.md` | [V4-MP] verbatim |
| `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md` | The cited report: harnesses, effort, styles, audio, MCP, craft rules, **65 edge cases (§8)**, integration (§9), **15 skills (§10)**, open questions (§11) |
| `12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md` | Every [N#] with quote, URL, status |
| `12_advanced_animations_with_claude/01_research/README.md` | How the research was produced |

### 8.2 Documentation (`12_advanced_animations_with_claude/02_documentation/`)

| File | Content |
|---|---|
| `12_advanced_animations_with_claude/02_documentation/00_OVERVIEW_and_PRINCIPLES.md` | This document |
| `12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` | Empty machine → ready: prerequisites, HyperFrames, Remotion, opus-js-animations, Manim CE, skill admission, Claude Code configuration, workspace layout, preflight, verification checklist |
| `12_advanced_animations_with_claude/02_documentation/02_PROMPTING_the_structured_brief.md` | L1/L2/L3 ingredients, the ExamLeaf brief structure, describing references from analyzer JSON, three worked briefs, anti-patterns |
| `12_advanced_animations_with_claude/02_documentation/03_STYLE_GUIDES_vertical.md` | The five house styles, 16:9→9:16 rules, fonts incl. Indic, palette, motion vocabulary |
| `12_advanced_animations_with_claude/02_documentation/04_HARNESS_CONTRACT_and_DETERMINISM.md` | Time-in/pixels-out contract, PRNG, cue-sheet loader, fonts, lint rules, determinism test, harness decision table, clip import, render box, export |
| `12_advanced_animations_with_claude/02_documentation/05_STORYBOARD_GATE_and_MCP_budgets.md` | 3×3 gate, beats.json, estimate.json, approval record; Higgsfield; credit ledger; MCP permissions |
| `12_advanced_animations_with_claude/02_documentation/06_AUDIO_compose_analyze_sync.md` | Python music/SFX, librosa analysis, cue sheet, voice path, mix and loudness |
| `12_advanced_animations_with_claude/02_documentation/07_THREEJS_MANIM_BLENDER_3D_and_math.md` | three.js, Manim CE and Blender: determinism, fixtures, clip import |
| `12_advanced_animations_with_claude/02_documentation/08_KINETIC_TYPOGRAPHY_and_INDIC_text.md` | Word-timed type, Hindi and Assamese text, captions |
| `12_advanced_animations_with_claude/02_documentation/09_EFFORT_COST_GOVERNANCE.md` | Model/effort/iteration choice, ultracode ban, caching, ledger fields, alerts |
| `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` | Automated checks, human gates, rubric, release blockers for animated scenes |
| `12_advanced_animations_with_claude/02_documentation/11_INTEGRATION_with_ExamLeaf_pipeline.md` | Routing tags, flow, owners, proposed runbook amendments |
| `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md` | All 65 master edge cases plus new ones |
| `12_advanced_animations_with_claude/02_documentation/13_END_TO_END_WALKTHROUGH.md` | Two fully worked examples: a 30 s doodle-style Reel ("Which line has the larger resistance? Check the axes.") and a data-bound Ohm's-law I–V graph lesson scene, with brief, cue sheet, scene code outline, audio, QA and export at every step |
| `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md` | Section decisions AD-01…, conflicts with existing docs, every open question with owner |

### 8.3 Skills (`12_advanced_animations_with_claude/03_skills/`)

Each skill folder contains `SKILL.md`, `references/`, `templates/`, `evals/cases.json` and `scripts/`.

| Skill | New / extends | Purpose | Edge cases owned |
|---|---|---|---|
| `examleaf-anim-brief` | new | Assemble the L2/L3 brief and constraints block | #7–#9, #11, #12, #50, #60 |
| `examleaf-reference-analyzer` | new | Reference video → pacing/style JSON | variable fps, letterbox, analysis-only use |
| `examleaf-style-guides` | new library | Versioned vertical house styles | #49, #54, #55, #56 |
| `examleaf-anim-storyboard-gate` | extends storyboard-route | 3×3 grid, beats, estimate, approval stop | #41, #42, #45, #47, #48 |
| `examleaf-motion-harness` | extends web-composition | Seek contract, linter, determinism test | #14–#24, #26, #65 |
| `examleaf-procedural-2d` | new | Doodle/collage primitives | #17, #18, #64 |
| `examleaf-kinetic-typography` | new | Word/grapheme-timed type, Indic-safe | #50, #55, #63 |
| `examleaf-threejs-scenes` | new | Seek-pure three.js from fixtures | #15, #17, #65 |
| `examleaf-audio-compose` | new | Seeded Python beds and SFX | #10, #39 |
| `examleaf-audio-analysis` | new | librosa beat grid, onsets, energy | #31–#38 |
| `examleaf-cue-sheet` | extends synchronizer + alignment | Canonical cue sheet; re-time on TTS change | #33, #35, #63 |
| `examleaf-mcp-orchestrator` | new | Per-job MCP permissions, credit ledger, reconciliation | #40–#46 |
| `examleaf-effort-governor` | extends observability-cost | Model/effort/iteration choice; refuse ultracode | #1–#6, #58, #60, #61 |
| `examleaf-anim-qa` | extends visual-qa + audio-caption-qa | Safe zones, holds, flashes, hashes, fixture diff, LUFS | #12, #17, #39, #50, #51, #56 |
| `examleaf-vertical-adapt` | new | 16:9→9:16 re-layout rules and sub-range Reels | #49, #51 |

### 8.4 Harness contract (`12_advanced_animations_with_claude/04_harness_contract/`)

`contract.md` (normative contract), `scene_template.html` (reference scene), `lint_seek_contract.js` (static linter), `determinism_hash_check.py` (double-render hash test), `cue_sheet.schema.json` and `cue_sheet.example.json`, `preflight.sh` (machine checks), `vertical_safe_zones.tokens.json`, `reference_analysis.sh` (FFmpeg/ffprobe reference measurement), `README.md`.

### 8.5 Style guides (`12_advanced_animations_with_claude/05_style_guides/`)

`paper-collage-vertical.md`, `doodle-handdrawn.md`, `editorial-vox.md`, `kinetic-type.md`, `voxel-isometric.md`, `style_tokens.json`, `README.md`.

### 8.6 Prompts and templates (`12_advanced_animations_with_claude/06_prompts_and_templates/`)

`brief_template.md`, `master_prompt_paper_collage_VERTICAL.md`, `storyboard_request.md`, `review_checkpoint.md`, per-style prompt templates, `negative_tests.md`, `README.md`.

### 8.7 Benchmark and pilot (`12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/`)

`BENCHMARK_hyperframes_vs_remotion.md`, `PILOT_three_test_lessons.md`, `record_sheets.md`.

---

## 9. Reading order by role

| Role | Read first | Then | Reference when needed |
|---|---|---|---|
| **Founder / operations** | This doc §1–§6 | doc 14 (decisions, conflicts, open questions); doc 05 §6–§7 (credits, ledger) | `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/PILOT_three_test_lessons.md`; `07_end_to_end_pipeline_instructions/08_COST_TRACKING_and_BUDGETS.md` |
| **Academic / subject reviewer** | This doc §5 (accuracy invariant) | doc 02 §5 worked brief (b); doc 05 §2–§5 (what you approve at the storyboard gate) | `12_advanced_animations_with_claude/06_prompts_and_templates/review_checkpoint.md`; `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` |
| **Engineer (harness / render box)** | doc 01 | doc 04; `12_advanced_animations_with_claude/04_harness_contract/contract.md` and `README.md` | `12_advanced_animations_with_claude/03_skills/examleaf-motion-harness/`; `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md` |
| **Animation author / prompt engineer** (the person driving Claude Code) | doc 02 | doc 03; doc 04 §2–§3; the chosen file in `12_advanced_animations_with_claude/05_style_guides/` | `12_advanced_animations_with_claude/06_prompts_and_templates/brief_template.md`; `12_advanced_animations_with_claude/06_prompts_and_templates/negative_tests.md`; `12_advanced_animations_with_claude/03_skills/examleaf-anim-brief/` |
| **Visual / motion designer** | doc 03 | `12_advanced_animations_with_claude/05_style_guides/*`; doc 02 §4 (reference analysis) | `12_advanced_animations_with_claude/03_skills/examleaf-procedural-2d/`, `12_advanced_animations_with_claude/03_skills/examleaf-kinetic-typography/`, `12_advanced_animations_with_claude/03_skills/examleaf-vertical-adapt/` |
| **Audio / narration lead** | This doc §4 (stack) and doc 14 AD-04, AD-15 | doc 04 §4 (cue sheet) | `12_advanced_animations_with_claude/03_skills/examleaf-audio-compose/`, `12_advanced_animations_with_claude/03_skills/examleaf-audio-analysis/`, `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/`; `05_narration_system/INSTRUCTIONS_narration_pipeline.md` |
| **Production QA reviewer** | doc 04 §7–§8 (what the machine checks) | doc 03 §3 and §6 (safe zones, holds, flashes) | `12_advanced_animations_with_claude/03_skills/examleaf-anim-qa/`; `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` |
| **Storyboard approver** (founder or academic lead) | doc 05 §2–§5 | doc 03 (style summary table) | `12_advanced_animations_with_claude/06_prompts_and_templates/review_checkpoint.md` |
| **Security / skill admission** | doc 01 §5 | doc 05 §8 | `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` |

---

## 10. Where this section disagrees with existing project documents

The full table with resolutions is in doc 14 §2. The main tensions are:

1. **Master format.** The runbook treats the long-form lesson as a 16:9 master with 9:16 recomposed Shorts (RD-16; `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` scope line). Section 11's playbook and this section treat everything as vertical 9:16. This section produces vertical only (AD-07) and proposes a runbook decision; it does not edit section 07. *Resolved 15 Oct 2026: the runbook recorded the vertical-only decision (RD-16 SUPERSEDED in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`); all output is 1080×1920 @ 30 fps.*
2. **Loudness.** House standard −16 LUFS integrated / ≤ −1 dBTP (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md`, `05_narration_system/`) vs [V4-MP] about −14 LUFS / peaks below −1.5 dBFS (AD-04).
3. **Music.** Learning-psychology tokens set `background_music_in_core_explanation: false`, and section 11 keeps music off under teaching; [V4-MP] and [V2] use continuous music beds (AD-15).
4. **Decorative motion.** The QA gates say "No decorative motion"; [V4-MP] says "Never frozen: everything on screen gets a gentle idle sway" (AD-16).
5. **Fonts.** RD-23 sets Inter + Noto Sans + KaTeX; [N51] says avoid Inter for distinctive design (AD-14).
6. **Dark backgrounds.** RD-27 says light theme only at launch; the collage style uses night-navy and charcoal sheets (AD-17).
7. **Repair attempts.** VE skills allow at most two failed repair attempts; this section's cap is three authoring fix loops per scene (AD-11).
8. **Model routing.** RD-04 uses the strong model for review and escalation only; this section uses Opus 5.5 at high for illustrative scene code (AD-24, with an Opus-vs-Sonnet A/B).
9. **Remotion licence.** `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5 records a conditional commercial licence with per-render figures from the earlier ChatGPT research; the section 12 evidence set has no verified licence terms. Both say "confirm before use" (open question Q3).

---

## 11. What is verified and what is not

| Verified (cited) | Not verified (treat as open) |
|---|---|
| Seek-based rendering pattern [N18], [N72]; rAF trap [N69]; single worker for video-heavy renders [N70] | HyperFrames `window.__hf` API shape [N68] (contested) |
| HyperFrames requirements, scaffold, plugin, licence [N8]–[N14] | HyperFrames' bundled tween library, worker flags, 9:16 presets, Indic shaping |
| Remotion skills install paths [N1], [N63]–[N67] | Remotion commercial licence, Node version, symlink behaviour on Windows or with an existing folder [N67] |
| Claude Code effort defaults and ultracode mechanics [N22]–[N26] | Caching across ultracode sub-agents; official cost per effort level |
| Higgsfield credit facts from its help centre [N33]–[N35] | Higgsfield plan prices (competitor-authored [N75]–[N77]), per-model credit costs, generated-asset licence terms |
| librosa beat-tracking behaviour [N36]–[N43], [N81] | Python music library versions; quality of synthesised music for long lessons |
| Manim skill install and CE/GL split [N44]–[N49] | Manim 9:16 frame configuration [Hypothesis] |
| [V1] measured effort runs (single creator) | Per-level values for medium/high/xhigh; how ExamLeaf template-based scenes compare (measure in pilot) |
| — | Platform safe-zone insets for Reels/Shorts; Indic conjunct shaping in headless Chrome; headless WebGL determinism across machines |

Everything in the right-hand column is listed with an owner and a resolution path in doc 14 §3.
