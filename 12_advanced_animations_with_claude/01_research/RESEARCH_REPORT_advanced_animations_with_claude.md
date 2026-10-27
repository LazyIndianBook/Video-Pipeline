# Advanced Animations with Claude: research report (14 Oct 2026)

**Scope.** This report covers an end-to-end capability for advanced animation made with Claude Code (Opus 5.5 / Sonnet 5.5) for ExamLeaf. ExamLeaf makes vertical 9:16 STEM revision lessons (about 10 minutes) and Reels/Shorts (20–60 s) for ASSEB Class 10–12, narrated by the Super Teacher persona.

**Citation conventions**
- Reference videos are cited as [V1]–[V5]. Their transcripts are auto-captions, so wording is approximate.
- Verified web evidence is cited as [N#]. Claims flagged in the evidence set are marked "(contested)".
- The paper-collage master prompt from the [V4] description is cited as [V4-MP].
- Design judgement is labelled [Recommendation] or [Hypothesis].
- Where nothing verified exists, the report says so. No commands, prices or limits have been invented.

---

## 0. Executive summary

1. **Claude writes animation code; a separate renderer produces the video.** Opus 5.5 "outputs text only" [N71]. Every working workflow has Claude write scene code (HTML/JS, Canvas, SVG, three.js, React/Remotion, Python/Manim). A deterministic renderer then seeks each frame by time and encodes it [N18][N68][N72]. The scene must be a pure function of time [N61] (contested).
2. **[V1] measured the effect of effort directly.** Devarf gave the same "make a music video" prompt to Opus 5.5 at low, medium, high, xhigh and max, plus one ultracode run, using Claude Code 2.1.287 in the terminal on a 79-second song clip.
   - Wall time rose from about 42 minutes (low) to almost 3 hours (max).
   - Tokens rose from about 78K to about 625K.
   - Estimated API-price cost rose from about $3 to about $49. He paid nothing extra because he is on a subscription.
   - Low produced 2D. Medium to max produced 3D. The ultracode run mixed 2D and 3D.
3. **Ultracode caused a cost blow-up in [V1].**
   - The run was max effort plus ultracode, set by mistake.
   - It wrote at least 2.5 million tokens, at least four times the max run. The estimate at API prices is at least $348.
   - It used almost three 5-hour usage windows on a Max plan and never finished; the author stopped it while it was trying to fix the video.
   - Each sub-agent built its own cache in its own session. When the limit hit, unfinished agents restarted fresh.
   - The author's advice is "Don't use Ultra Code". Ultracode is multi-agent work, not a higher effort level [V1]. It starts at xhigh when launched with `claude --effort ultracode` [N24], and it cannot be set as a persisted default [N25].
4. **The default effort is a trap.** Opus 5.5 and Sonnet 5.5 default to **medium** effort, while most other models default to high [N22]. [V2] recommends high or xhigh ("extra") for JavaScript animation, and max only for very complex scenes. Set the effort level explicitly.
5. **[V2] defines three levels of quality.**
   - L1: a one-line prompt. Results are random and inconsistent.
   - L2: a structured prompt with a reference style, a reference video, pacing instructions, creative direction, Python-composed music and optionally HyperFrames or Remotion.
   - L3: L2 plus MCP orchestration (clips and B-roll, studio narration, music models) and a rendering harness. The human still supplies the plan, the reference video and the pacing research.
6. **[V3] covers motion graphics with Remotion.**
   - Claude installs Remotion and researches its current docs, then the Remotion Studio opens in the browser.
   - A long, detailed prompt plus a reference video for pacing beats a "make it stunning" prompt.
   - Brand hex codes go in the prompt.
   - Tell Claude **not to inspect old project folders**.
   - Audio is not added automatically, so ask for Python-made SFX and music.
   - In the orchestrated demo (sun vs planets, Vox editorial style), the visuals were strong but the AI-written script was weak.
7. **[V4] is the closest template for ExamLeaf.** A style-guide master prompt replaces the reference video. The flow is:
   1. Study the style guide.
   2. Write the script (60 s, 140–160 words).
   3. Make a 3×3 storyboard via Higgsfield MCP (GPT Image 2.5).
   4. **Stop for human approval.**
   5. Generate the voiceover (Higgsfield → ElevenLabs v3 "Arthur").
   6. Generate the image assets.
   7. Build the JavaScript animation synced to the voice.
   8. Compose music and SFX.

   [V4] says this style is credit-expensive. The video is sponsored by Higgsfield.
8. **[V5] (Fable 5.5) is an unverified signal only.** The claims rest on a routing "leak" and third-party demos (style-morphing animation, physics Rube Goldberg, voxel island, described as "50–60% better" than Opus 5.5). Do not plan on it. The Fable model family itself exists: Claude Code docs say thinking cannot be turned off on "the Fable models" [N26].
9. **"Claude Motion" is not verified as a product name.** No verified source names a product or feature called "Claude Motion". [V1]'s description says "Opus 5.5 Motion Graphics". [N59] (a third-party tutorial) dates Opus 5.5 to 22 Sep 2026 but cites no link. Treat "Claude Motion" as a community term for this code-to-video practice.
10. **Recommended default stack for ExamLeaf** [Recommendation]:
    - Claude Code on Opus 5.5 at explicit **high** effort (xhigh for hard scenes).
    - **HyperFrames** as the default composition and render harness (Node 22+, FFmpeg, Apache-2.0, no per-render fees [N8][N14]), with Remotion benchmarked in parallel. Remotion skills install with `npx skills add remotion-dev/skills` [N1].
    - Existing **SVG and Manim CE** scenes for every data-bound diagram.
    - three.js for light 3D, and Blender only selectively.
    - Python for music and SFX, librosa for beat sync, and the existing TTS and alignment for narration timing.
    - Higgsfield only for storyboards and optional raster assets, under a hard credit budget.
11. **Science accuracy needs a hard split** [Recommendation]. Decorative and narrative layers (hooks, analogies, collage characters) can be freeform Claude code. Any axis, value, equation, label, structure or graph must come from validated fixtures in the existing pipeline. Image models must not draw text or formulas.
12. **Everything must be vertical.** The [V4-MP] style guide is written for 16:9 1920×1080 at 30 fps with text about 90 px from the edges. It needs a deliberate 9:16 adaptation, not a crop.
13. **Credits have no native cap.** Every Higgsfield generation through an agent deducts credits whatever the plan [N33]. "There's no native credit cap", and prompt-level limits are not hard limits [N34]. Budgets must be enforced in the pipeline.
14. **Quality comes mostly from the brief, not the effort level** ([V1], [V2], [V3]). The brief that pays off is: reference video or style guide, brand tokens, distinctive fonts [N51], one orchestrated staggered entrance [N53], a minimum hold of about 1.2 s for headlines [N60], and seeded, stateless animation [N61].
15. **Top 10 edge cases** (full table in §8):
    1. Silent medium-effort default [N22].
    2. Ultracode runaway cost [V1].
    3. Wall-clock or rAF animation that breaks seek-rendering [N68][N69].
    4. Unseeded randomness [N61].
    5. Multiple videos decoding in parallel exhausts decoders [N70].
    6. librosa stereo/sparse and tempo-ndarray traps, beats in frames instead of seconds, and resampling drift [N37][N38][N39][N81].
    7. Silent audio returns an empty beat list [N41].
    8. Higgsfield has no credit cap [N34].
    9. Manim CE and ManimGL are incompatible [N48].
    10. Missing Chrome or Node/FFmpeg on the render box [N8][N17].

---

## 1. The method the videos converge on

### 1.1 The three levels ([V2])

**Level 1: idea → one-line prompt → JavaScript.**
- Example: "Use JavaScript to animate a black hole."
- Opus uses JS and internal tools to produce a video. The presenter calls the results random: sometimes great, sometimes "ridiculous".
- Takeaway: never use L1 in production. It is good only for exploring styles.

**Level 2: a structured prompt plus references.**
The ingredients are:
- a reference style to match, plus an actual reference video;
- strict pacing instructions;
- creative direction "to keep viewers watching";
- the instruction to compose sound and music with Python;
- optionally, a harness (HyperFrames or Remotion) for more render control.

Setup notes from [V2]:
- Select Opus 5.5 with effort at xhigh ("extra") or high. Max only "if… incredibly complex"; "99% of the time you won't need anything more than extra."
- Keep the model contained inside one workspace folder.

Demo:
- The prompt asked for a ~20 s animated story in the reference doodle style (a Sonnet 5.5-made video), written in JavaScript, with original pleasant background music in Python and a full story outline (baby deer, tiger chase, butterfly guide, reunion).
- Result: convincing hand-drawn look and good music.
- Critique: "flat and cartoonish", "strictly 2D… no depth". These were fixed by iterating with the model.

[V2] also says Sonnet 5.5 can do this, but Opus 5.5 gives "more polished results". It shows a soothing music video whose music was composed by Opus in Python. A third-party example used Gemini Flash 3.8 TTS for the voice (third-party claim, not verified).

**Level 3: orchestrated production.**
- The human still provides three things the model "is still not fully capable of handling": **the plan/idea, the reference video, and the pacing research** (how the video is structured).
- Opus writes the JavaScript animation and uses MCP servers for:
  - clips and B-roll, or local video files;
  - studio narration;
  - a "music studio MCP" for model-generated tracks.
- Everything runs through a harness (HyperFrames or Remotion). The model can install these itself because they are free.
- The demo used the **Higgsfield MCP**, and HyperFrames opened in a side panel with a scene timeline for extending or editing scenes.
- The prompt included a story, a style reference (a paper-collage piece by creator "Kevin No Again"), "make it funny", "follow our usual workflow", "use the MCP servers I have connected", and "don't stop working until the animation matches the exact quality of the reference video".
- Output: per-scene raw-JS animation, Higgsfield voices, and audio placed on the timeline with background music.

**ExamLeaf reading** [Recommendation]:
- The three human-owned inputs map onto ExamLeaf's existing artefacts:
  - plan/idea → lesson plan and storyboard route;
  - reference → house style guide;
  - pacing research → pacing controller.
- The "don't stop until it matches" instruction is a **cost hazard** (see §3 and §8). Replace it with a bounded number of iteration rounds and a QA rubric.

### 1.2 The structured prompt, reference video and pacing brief ([V3])

[V3] gives this procedure for motion graphics with Remotion:

1. Ask Claude to "download and set up the latest version of Remotion directly in the project folder" and to "research Remotion's current official documentation and tools". The verified install path for the agent skills is `npx skills add remotion-dev/skills` [N1], or `npx remotion skills add` [N64].
2. Remotion Studio opens in the browser and lists compositions.
3. Give a **massive, detailed prompt** plus a **reference video** "so the AI understands exactly how the pacing and timing should feel". Lazy prompts ("make a stunning premium video") produce "dumb boring" results.
4. The prompt should specify:
   - replicate the reference's animation style;
   - duration (20 s);
   - the subject (Sonnet 5.5 vs Opus 5.5 benchmarks);
   - "study the reference video's layout structure and its exact typography treatment";
   - brand palette (your own hex codes);
   - "**do not inspect any of my older projects or folders**".
5. Ask explicitly for SFX and music generated with Python, because "it might not automatically include audio".
6. For "level two motion graphics", connect MCPs (image generator, voice generator, music generator, Blender) and grant permission to use them.

In the sun-vs-planets demo (15 s, Vox editorial style), the model selected a fitting voice and orchestrated every MCP "without errors". The weak point was the AI-written script; the presenter's fix is to write the script yourself.

[V3] also reports a SaaS promo "done in just 15 minutes" and a 15-second "showreel" from a one-line prompt with timed SFX and music. 3D motion graphics came via a **Blender MCP** (Kevin NGO example).

**ExamLeaf reading**:
- [V3]'s two biggest lessons fit ExamLeaf directly: **scripts come from ExamLeaf's narration system, never from the animation agent**, and **reference-driven layout and typography beat adjectives**.
- [V3]'s model "did its own proper research on the benchmarks". In ExamLeaf that is forbidden for any on-screen fact. Facts flow only from validated data (§9).

### 1.3 The style-guide master prompt ([V4], [V4-MP])

[V4] runs the full pipeline from a single master prompt (the verbatim export is in `00_reference_videos/master_prompt_paper_collage.md`).

**Steps**
1. **Study the style guide.** Writing style (tone, sentence length, hooks, how facts are delivered) and animation style (JS-only build, motion, transitions, typography, palette).
2. **Write the script.** About 60 s, 140–160 words.
3. **Storyboard.** Higgsfield MCP, GPT Image 2.5 (`gpt_image_2_5`), one 3×3 grid of 9 panels in beat order.
4. **⛔ Review checkpoint.** "Stop after Steps 2 and 3… wait for my approval."
5. **Voiceover.** Higgsfield MCP, preset voice "Arthur" (a specific voice_id), ElevenLabs v3 via Higgsfield `text2speech_v2`, variant elevenlabs.
6. **Build the animation.** JavaScript, following the approved storyboard, synced to the voiceover timing.

**Style guide ("Paper-Cutout Storybook Collage")**
- **Look:** watercolour and coloured-pencil cutouts with a 6–12 px white die-cut border and a two-layer warm drop shadow (`0 9px 7px rgba(74,48,22,0.30)` plus `0 2px 1.5px rgba(0,0,0,0.20)`).
- **Backgrounds:** textured paper (cream watercolour, kraft board, watercolour skies, torn-paper strips). Flat head-on view; no 3D, gloss or heavy blur.
- **Palette:** 13 named hexes (tomato #d9483b, mustard #e0a73a, teal #2f7f7a, ultramarine #2f4fa8, … ink #2b2622, night navy #1b2a4a).
- **Characters:** round, big heads, dot eyes, blush; never scary. One recurring hero kept identical by passing an earlier image as a reference.
- **Typography, only three kinds:**
  - ransom-note tiles with mixed display fonts, ±6° rotation, each letter landing 0.04–0.05 s apart in sync with speech;
  - Caveat Brush handwriting with a red double underline;
  - Patrick Hand labels on washi-taped tags.
- **On-screen text:** short only (title, number or punchline), about 90 px from the edges.
- **Doodles:** 3–5 px pencil strokes that draw on.
- **Composition:** 16:9 1920×1080 at 30 fps, layered depth, subtle vignette, slow push-in to about 1.03–1.04 scale.
- **Motion (GSAP vocabulary):**
  - pop-in with back.out(2–3), pivoting at the feet;
  - idle sway with **finite repeats**;
  - stop-motion "boil" at 8–10 fps;
  - gags: multiply, tear, paper-flip swap, squashy shrink.
- **Sync rule:** every reveal lands on, or about 0.05 s before, its spoken word; one sentence = one visual beat.
- **Determinism:** "use only seeded randomness, only finite repeats, and a timeline that can jump to any frame."
- **Transitions:**
  - default: a paper sheet slides over the previous scene in 0.5–0.7 s, power3.out, varying direction;
  - somber beats: a dark sheet drops in about 0.9 s;
  - urgency: a whip in about 0.4 s;
  - each new sheet starts about 0.3 s after the previous line's last word; no exit animations.
- **Writing:** warm, wry storybook narrator; 5–9-word sentences; rule of three with a deadpan third beat; at most one number per sentence; about 110 wpm natural pace.
- **Sound:** whimsical track at about 100 BPM, sitting 15–20 dB under the voice and low-passed for somber beats, with subtle paper SFX. Final loudness about **−14 LUFS, peaks < −1.5 dBFS**.
- **Asset rules:**
  - cutouts generated on transparent backgrounds at 2K, with a long template prompt; transparent margins trimmed before use;
  - the storyboard or an earlier cutout attached as a reference for consistency;
  - **text, tape, confetti, doodles and simple UI are built in code, not generated as images.**

**Setup and cost notes**
- Connection in [V4]: on the Higgsfield site, "install Higgsfield MCP" → "connect to Higgsfield" → continue (pre-filled). Verified official paths are in §6.
- [V4] admits the style is "on the expensive side regarding credits" because it needs many individual assets.

**ExamLeaf reading** [Recommendation]:
- Adopt the **structure** wholesale: style guide → script → storyboard grid → hard gate → voice → assets → animate → audio → compile.
- Change the content:
  - The **script comes from the Super Teacher system** with science review and academic approval, not the animation agent.
  - The voice comes from ExamLeaf's TTS adapter (Indian English, Hinglish or Hindi), not "Arthur".
  - The aspect ratio becomes 1080×1920 (§7).
  - Labelled science visuals come from the SVG and Manim fixtures.
  - The collage style becomes one of several house styles, used mainly for hooks, analogies and recap stories.

### 1.4 Effort and ultracode economics ([V1])

**Setup**
- Claude Code 2.1.287, Opus 5.5, terminal (not the app, to avoid "fill[ing] up my chat list").
- A folder per run containing "some information and tools":
  - a tools folder with three.js, Canvas 2D, SVG and frame-conversion tools;
  - **no guides or examples**.
- Claude "cannot hear the song", so a custom audio-analysis tool was built and run with Opus at high effort. It extracted beats, notes, instruments, dynamics, lyrics and a plain-language note on the song's meaning or story. It used about 5 GB RAM with a 6 GB VRAM GPU. The author suggests asking Claude to build one sized to your hardware.

**Prompt**
- "A full music video, like a real official one, with a lot of dance or some story, motion graphics only."
- 2D, 3D or both allowed.
- "Creative and unique."
- "Work on its own from start to finish and not to stop and ask."

**Results**

| Run | Visual | Time | Tokens | Est. API price |
|---|---|---|---|---|
| Low | 2D | ~42 min | ~78K | ~$3 |
| Medium–xhigh | 3D | between low and max (per-run values not stated) | — | — |
| Max | 3D | ~3 h | ~625K | ~$49 |
| Max + ultracode | 2D character on a 3D playing-card stage | did not finish | ≥2.5M (some agent logs missing counts) | ≥$348 |

- All six runs delivered the full 79 s with the original audio matched.
- The ultracode run cost "almost three 5-hour limits" on the Max plan. It "kept reviewing the video with multiple agents"; each agent built its own cache; unfinished agents restarted fresh after the limit.
- The author: improvements from medium to max were visible (3D models, movement), but low was "still good". His advice: don't use ultracode; if you must, try it at low effort in the terminal (untested by him).

**Implications** [Recommendation]:
- The effort-to-cost curve is steep: about 8× tokens from low to max for one 79-second piece.
- ExamLeaf's unit is a scene, not a whole video. Use **high** for most scene code, **xhigh** for complex 3D or physics, and medium for planning-text tasks. Never use ultracode in unattended pipelines.
- Effort has to be set explicitly because medium is the silent default on Opus 5.5 [N22].
- Verified mechanics: `claude --effort ultracode` starts at xhigh with ultracode on [N24]. The persisted `effortLevel` setting and `CLAUDE_CODE_EFFORT_LEVEL` do not accept ultracode [N25], which is good for safety: it cannot become a default by accident. Thinking cannot be switched off on Opus/Sonnet/Haiku 5.5 or Fable models [N26], so some thinking cost is always there.

### 1.5 Fable 5.5 signals ([V5]) — unverified

- **Claimed leak mechanism:** web users selecting "Fable 5.1" were silently routed to a newer model. The evidence offered is a knowledge-cutoff test about a recent meme that the API version of Fable 5.1 answered wrongly.
- **Demos shown:**
  - a desk scene whose art style changes almost every second, with music and SFX, made in 15 minutes;
  - a Superman painting-style morph with camera moves;
  - a pure-JS roster of heroes in one shot;
  - "an animation of a dot";
  - a 3D Rube Goldberg machine with natural-looking physics and SFX;
  - a motion-design reel described as "50–60% better";
  - a voxel island compared with an Opus 5.5 island.
- **Status:** none of this is verified. The claims are third-party, the release date is "as early as next Tuesday", and the comparisons are unquantified. [N26] confirms only that a "Fable" model family exists in Claude Code.

[Recommendation] Treat Fable 5.5 as a future upgrade to the model slot, not a design input. Keep the harness model-agnostic. When it ships, re-run the §8 determinism and science-accuracy QA before switching.

---

## 2. Rendering harnesses

### 2.1 The common contract: time in, pixels out

Every verified harness works the same way. Headless Chrome (or a Python renderer) sets time `t` and captures a frame; nothing is played in real time.

- opus-js-animations: "headless Chrome renders frame i as seek(i / fps) across parallel workers" [N18].
- HyperFrames: compositions expose `window.__hf` with duration and seek, and "the renderer never calls play()" [N68] (contested).
- A HuggingFace tutorial uses a contract where each scene must set `window.DURATION` and expose `async window.seek(t)`; frame count = DURATION × fps [N72].

The consequences:
- Animations must be **pure functions of time** with seeded randomness [N61] (contested).
- No `setInterval`, no real-time physics stepping without a fixed-step replay, and no `Date.now()`.
- Polling that relies on requestAnimationFrame **hangs** in BeginFrame mode ("rAF doesn't fire") [N69]. Poll with `page.evaluate` plus a `setTimeout` loop and a deadline.

### 2.2 Remotion

**Install and skills**
- Install with `npx skills add remotion-dev/skills` [N1], or via the CLI family `npx remotion skills <subcommand>` [N63], which has `add` [N64] and `update` [N65].
- Skills are offered at project creation [N2] (contested).
- Target agents: Claude Code, Codex, Kimi Code, Cursor [N3].
- Skills install into `.agents/skills`. Claude Code compatibility comes from a symlink `.claude/skills → .agents/skills` [N66][N67]. Whether the CLI creates it, and what happens on Windows or with an existing `.claude/skills` folder, is not documented [N67].
- Named skills in the evidence:
  - `/remotion-best-practices`, the umbrella that "encompasses all other skills" [N4];
  - `/remotion-render`, for a video or still render [N5];
  - `/remotion-maps` (Mapbox, MapLibre, MapTiler, GeoJSON, CesiumJS flyovers) [N6];
  - `/remotion-upgrade`, which upgrades Remotion, Mediabunny packages and installed skills together [N7].
- Run upgrade before benchmarking to avoid version drift [N7].

**Workflow ([V3])**
Claude installs Remotion, researches the docs, and Studio opens in the browser with a composition list. Audio must be explicitly requested.

**Not verified**
- Remotion's licence terms for commercial use, captions APIs, the audio API surface and error catalogue were **not in the verified evidence set**.
- [Recommendation] Have the benchmarking team read the current licence and docs (via `/remotion-best-practices`) before any commercial decision, and record findings in the benchmark report.

**Fit for ExamLeaf** [Hypothesis]:
- React components map well onto data-driven science scenes, because props come from validated JSON.
- Studio is a good human-review surface.
- Composition sizes can be set to 1080×1920 (to be confirmed in benchmark).

### 2.3 HyperFrames

**Requirements and install**
- Node.js 22+ and FFmpeg [N8].
- Scaffold with `npx hyperframes init my-video` [N9].
- Claude Code plugin: `claude plugin install hyperframes@hyperframes` after adding the marketplace [N10].
- Agent skills via `npx skills add heygen-com/hyperframes` [N58] (tutorial source). The repo "ships 21 skills agents load on demand" [N11].
- Clone with `GIT_LFS_SKIP_SMUDGE=1` to skip LFS payloads [N13].
- A Codex archive build fails above Codex's 100 MB upload limit [N12].

**Licence:** Apache 2.0, "no per-render fees or commercial-use thresholds" [N14].

**Rendering model** (HeyGen research blog):
- seek-only via `window.__hf.seek(t)` [N68] (contested);
- rAF-based polling hangs [N69];
- **video-heavy compositions should use a single worker** because Chrome cannot seek several video elements at once without running out of decoders [N70].

**Studio and timeline:** [V2] shows HyperFrames opening as a panel with scenes on a timeline, where audio and music are placed.

**GSAP:** [V4-MP] specifies motion in GSAP vocabulary (back.out, power3.out, expo.out). Whether HyperFrames bundles or prefers GSAP was not verified. [Recommendation] Any tween library works if its timeline is driven by `seek(t)` rather than playing.

**Fit:** this is ExamLeaf's existing first-choice harness. It is plain HTML/CSS/JS (closest to what Opus writes natively in [V2] and [V4]), Apache-licensed and seek-deterministic.

### 2.4 Raw Canvas/SVG/three.js frame pipelines

**opus-js-animations** (klsoen, MIT [N21]):
- Install as a Claude Code plugin with `/plugin marketplace add klsoen/opus-js-animations` [N15], or manually with `cp -r opus-js-animations/skills/opus-js-animations ~/.claude/skills/` [N16].
- Parallel seek rendering [N18]. Set `CHROME=/path` if Chrome isn't found [N17].
- Voiceover keys are read from the environment or `~/.config/opus-js-animations/keys.env`, "never written into your project" [N19].
- Audio is cut on zero crossings "with no normalising, EQ or fades unless you ask" [N20].
- Claims of working with models other than Opus 5.5 are untested [N21].

[V1] used a homemade tools folder of exactly this kind: three.js, Canvas 2D, SVG and frame converters.

**ExamLeaf's existing Python SVG→FFmpeg proof renderer** is the same pattern for 2D science.

[Recommendation] Use raw pipelines for:
- three.js 3D scenes (orbitals, lattices, field lines) that are awkward inside a composition framework;
- procedural doodle and collage drawing;
- anything exported as an image sequence and then placed as a clip in HyperFrames or Remotion.

### 2.5 Manim and Motion Canvas

**Manim skills:** `npx skills add adithya-s-k/manim_skill` installs both skills [N44]. Install only the CE skill by path with `npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices` [N45].

**Install traps:**
- Manim CE installs via `pip install manim`; verify with `manim --version` [N46].
- ManimGL on ARM macOS needs `arch -arm64 brew install pkg-config cairo` first [N47].
- **CE and ManimGL are separate, incompatible frameworks** [N48]. Pick CE, which matches the existing `examleaf-manim-scenes`.
- Many parallel test workers cause out-of-memory errors; use 4–6 workers [N49].

**Motion Canvas:** no verified evidence was collected. [Recommendation] Do not add it; Remotion, HyperFrames and Manim already cover the space.

### 2.6 Decision table for ExamLeaf

| Criterion | HyperFrames | Remotion | Raw Canvas/SVG/three.js | Manim CE | Blender (MCP/scripted) |
|---|---|---|---|---|---|
| 9:16 vertical | Yes (HTML viewport you set) [Hypothesis] | Yes (composition size) [Hypothesis] | Yes (canvas size) | Yes (config frame size) [Hypothesis] | Yes (render resolution) |
| Deterministic | Seek-only renderer [N68] | Frame-based React [Hypothesis] | Seek per frame [N18][N72] | Scripted, deterministic [Hypothesis] | Deterministic if scripted and seeded [Hypothesis] |
| Science accuracy (data-bound) | Good when fed validated JSON | Good (typed props) | Good for custom diagrams | **Best for equations and graphs** | Selective spatial assets only |
| Agent skill support | 21 skills [N11] plus a plugin [N10] | Umbrella plus render/maps/upgrade [N4]–[N7] | opus-js-animations [N15] | manim_skill [N44] | Unverified MCP |
| Licence/cost | Apache-2.0, no per-render fee [N14] | **Verify** (not in evidence) | MIT [N21] | Open source [Hypothesis] | Open source [Hypothesis] |
| Requirements | Node 22+, FFmpeg [N8] | Node (version not in evidence) | Chrome/Chromium [N17] | Python, cairo on ARM for GL [N47] | Blender install |
| Video-in-video | Single worker [N70] | Benchmark | Avoid | n/a | n/a |
| Role | **Default lesson/reel composer** | Benchmark challenger | 3D and procedural inserts | Equation/graph inserts | Rare hero 3D |

[Recommendation] **HyperFrames is the master timeline.** Manim, SVG, three.js and Blender render to clips or PNG sequences that are imported into it. The benchmark against Remotion runs on the same three test lessons (one physics, one chemistry, one biology). It measures render time, determinism (identical frame hashes across two renders), agent token cost per scene, fix-loop count and reviewer edit time.

---

## 3. "Claude Motion" and Claude Code settings

### 3.1 What "Claude Motion" is

- No verified source documents a feature named "Claude Motion".
- The verified facts are: Opus 5.5 is text-only [N71]; it writes animation code that external renderers execute [N71][N72]; it "does not natively behave like a cinematic text-to-video model" [N62] and suits designed motion, typography, diagrams and procedural scenes. Photoreal humans and real-world physics should go to dedicated video generators [N62].
- Opus 5.5 has a 1M-token context and up to 128K output tokens, as of the tutorial's date; recheck [N73].
- [N59] (third-party, no link) dates Opus 5.5 to 22 Sep 2026.

[Recommendation] Use "Claude Motion" internally only as the name of ExamLeaf's code-to-video layer. Ask Anthropic whether an official feature exists (§11).

### 3.2 Effort levels

- Levels seen in [V1]: low, medium, high, xhigh, max, plus ultracode, which is a separate multi-agent mode that sits after max on the app slider.
- Defaults: high on most models, but **medium on Opus 5.5, Sonnet 5.5 and Haiku 5.5** [N22].
- If you request a level a model doesn't support, Claude Code falls back to the highest supported level at or below it. Example: xhigh runs as high on Opus 4.6 [N23].
- Ultracode is launched with `claude --effort ultracode` (starts at xhigh) [N24]. It is not accepted by `effortLevel` or `CLAUDE_CODE_EFFORT_LEVEL` [N25].
- Thinking cannot be disabled on Opus/Sonnet/Haiku 5.5 or Fable models [N26].
- On 4.6 models, `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` reverts to a fixed budget set by `MAX_THINKING_TOKENS` [N27] (contested, and not applicable to 5.5).
- The `opus`, `sonnet` and `haiku` aliases resolve to the newest version only on the Anthropic API; some other providers get earlier versions [N28]. Pin full model IDs.
- Haiku 5.5 prompts over 100K tokens cost more per token [N28].

### 3.3 Caching, usage limits and cost

**Caching**
- [V1] observed that ultracode sub-agents each build their own cache in their own sessions, and that they restart fresh after a limit. Multi-agent work multiplies cache-creation cost.
- [Recommendation] Run one main session per scene batch. Keep stable context (style guide, brand tokens, harness contract) at the start of the prompt and unchanged between scenes to maximise cache reuse. Precise caching mechanics and prices were not in the verified set; confirm with the `claude-api` docs before modelling.

**Usage limits**
- Max plans start "From $100" per month [N74]. [V1] burned almost three 5-hour windows with one ultracode run.

**Cost formula** [Recommendation]:
- Track tokens per scene and scene count per lesson.
- Use [V1] as an upper-bound reference: about 78K tokens at low to about 625K at max for one 79 s piece, built from scratch with no guides.
- [Hypothesis] ExamLeaf scenes built from templates and skills should land far below these figures, because the harness, style and data are pre-supplied. Measure this in the pilot.

### 3.4 Recommended settings per task [Recommendation]

| Task | Model | Effort | Notes |
|---|---|---|---|
| Brief and storyboard text, prompt assembly | Sonnet 5.5 | medium (default) | Cheap; structure matters more than depth |
| Scene code: 2D motion, kinetic type, collage | Opus 5.5 | **high** (set explicitly) | Matches [V2]'s guidance |
| Complex three.js, physics replay, intricate choreography | Opus 5.5 | xhigh | Max only with a written justification |
| Debugging a render failure | Opus 5.5 | high | Give the logs plus the failing frame time |
| Batch re-renders, captions, file ops | Sonnet/Haiku 5.5 | low–medium | No creative judgement needed |
| Anything | — | **never ultracode** in unattended or production runs | [V1], [N24]; separate sandbox and budget only |

Operational rules:
- Run headless in the terminal, one workspace per job ([V1], [V2]).
- Tell the agent not to read sibling project folders ([V3]).
- Cap iteration rounds, for example 3 fix loops per scene.
- Never use "don't stop until perfect" without a budget.
- Log tokens per run to `examleaf-observability-cost`.

---

## 4. Drawing styles in code

For each style below: how it is produced, what reference material it needs, and its limits.

### 4.1 Paper-collage storybook ([V4-MP], [V2] L3 demo)

**How it is produced**
- Raster cutouts (Higgsfield, GPT Image 2.5, transparent, 2K), trimmed.
- Placed as DOM or canvas layers with CSS shadows and white borders.
- Paper textures as backgrounds.
- Text, tape, doodles and UI built in code.
- GSAP-style tweens driven by seek. Stop-motion boil uses stepped seeded jitter at 8–10 fps.

**Reference material:** the full style guide plus the approved storyboard grid and one canonical hero image for character consistency.

**Limits**
- Credit-heavy because of many assets ([V4]).
- Character drift between generations.
- Image models must not render labels or formulas [Recommendation].
- The guide is 16:9 and needs 9:16 re-layout.

**ExamLeaf use:** hooks, analogies, history-of-science stories, recap endings.

### 4.2 Doodle and hand-drawn (pure code) ([V2])

**How it is produced**
- Canvas 2D or SVG paths with wobble: seeded noise on control points, re-seeded at a "boil" rate.
- Stroke-dash draw-on, a pencil texture overlay, flat fills.
- No image model needed. The [V2] deer story was entirely code.

**Reference material:** a short reference clip or 3–5 stills in the target style, plus a palette.

**Limits:** [V2] found the result "flat"; ask for parallax layers and depth cues explicitly.

[Recommendation] This is the **cheapest house style** (no credits). Make it ExamLeaf's default illustrative style for Reels.

### 4.3 Vox-style editorial ([V3])

**How it is produced**
- Textured backgrounds, cut-out photos or illustrations, highlighter strokes.
- Bold serif and sans headline mix, map and number callouts, push-ins.
- Built in Remotion or HyperFrames, with MCP-generated assets and voice.

**Reference material:** a reference video for pacing, typography treatment and layout.

**Limits:** the AI-written script was weak in [V3]; supply the script.

**ExamLeaf use:** comparisons and scale stories (planet sizes, orders of magnitude), driven by validated numbers.

### 4.4 Kinetic typography and SaaS-style motion graphics ([V3], [N50]–[N55], [N60])

**How it is produced**
- Per-word or per-letter timeline keyed to TTS word timestamps.
- Masks, slides and scale pops.
- One orchestrated staggered entrance rather than scattered micro-animations [N53].
- Dominant colour with sharp accents [N52].
- Distinctive fonts instead of Arial or Inter [N51]. Note that repeated generations still converge on common choices such as Space Grotesk [N55], so ban or rotate fonts explicitly.
- For HTML, prefer CSS-only motion; use the Motion library for React [N54].
- Hold primary headlines fully readable for at least 1.2 s before the next major transition [N60]. This is an example figure; lengthen it for Hindi and longer copy.

**Limits:**
- Indic scripts need fonts with full Devanagari and Bengali-Assamese coverage [Hypothesis].
- Per-letter animation can break conjuncts and ligatures in Devanagari [Hypothesis]. Animate per word or per grapheme cluster, never per code point.

### 4.5 Voxel and isometric 3D ([V5] island demo, [V1] 3D runs)

**How it is produced:** three.js with instanced boxes, an orthographic camera, baked or simple lighting, and seeded procedural layout. Camera paths are written as functions of t.

**Limits:** GPU and headless WebGL availability on the render box [Hypothesis]; frame-time variance; anti-aliasing differences between machines.

**ExamLeaf use:** crystal lattices, cell organelles, a stylised "island of concepts" recap.

### 4.6 three.js scientific 3D and Blender

**three.js:** for orbitals, field lines, molecular geometry and wave surfaces driven by validated parametric data.

**Blender:**
- For hero spatial assets via the existing `examleaf-blender-scenes` skill.
- [V3] shows Blender MCP–driven 3D motion graphics, but **no verified install or command evidence for a Blender MCP was collected**.
- [Recommendation] Keep Blender scripted (Python, seeded) and rendered offline. Treat a Blender MCP as an optional authoring aid behind permission gates (§6).

### 4.7 Style-morph, multi-style montage ([V5])

Unverified Fable 5.5 demos only. [Hypothesis] Feasible with Opus by switching render functions per time segment, but rarely useful for teaching. Skip it.

---

## 5. Audio

### 5.1 Python-composed music and SFX

**Evidence of capability**
- [V2]: music "composed by Opus 5.5 using Python code"; the model "can compose original music and create sound effects".
- [V3]: when using Remotion, you must ask for Python SFX and music explicitly.
- [V1]: SFX in all six videos were AI-made.

**Recipe** [Recommendation; libraries not in the verified set, confirm versions in the pilot]:
- Music: synthesise with NumPy (oscillators, ADSR envelopes, simple filters) and write WAV with a standard writer such as `scipy.io.wavfile` or `soundfile`. For richer timbres, write MIDI and render with a SoundFont synth.
- Fix the tempo first. [V4-MP] uses about 100 BPM for the storybook style. Generate bar-aligned stems (pad, plucks, percussion) so the music can be cut to any scene length.
- Seed every random call so re-renders are identical.
- SFX library: paper swish, tap, pop, boing, tear, thud, chime ([V4-MP]), plus STEM-specific sounds (electric hum, bubbling, click-snap for bonds). Make them short one-shots placed by a cue sheet.
- Mood control: low-pass the music for somber beats; swell it on the end card ([V4-MP]).

**Limits** [Hypothesis]: synthesised music can sound "chiptune" without careful voicing. Keep a curated, licensed fallback bed, or use an MCP music model (§6), for long lessons.

### 5.2 Audio analysis for sync

**librosa `beat_track`**
- Returns tempo **as an ndarray even for mono input**, so index it or `float()` it [N38].
- Beat output is in **frames by default**; pass `units='time'` for seconds [N39].
- `start_bpm` defaults to 120 and is ignored if a prior is given [N36].
- Multi-channel input works only with `sparse=False` [N37], which returns a dense boolean per-frame array [N43].
- Raises `ParameterError` if neither `y` nor `onset_envelope` is supplied or `units` is invalid [N40].
- Silent or beatless audio gives 0 BPM and an empty beat list [N41].
- A time-varying `bpm` array must match the `onset_envelope` shape [N42].

**librosa `load`**
- Mixes to mono and resamples to 22050 Hz by default; pass `sr=None` to keep the native rate [N81].
- Timestamps computed with a different `sr` than the one loaded drift against the video [N81].

**[V1] approach:** a custom analyser (beats, notes, instruments, dynamics, lyrics, song meaning), because "the AI cannot hear the song", about 5 GB RAM.

[Recommendation] ExamLeaf rarely needs full music analysis. It needs:
- (a) a **beat grid** for Reels with music beds;
- (b) **word timestamps** for narration sync, from the TTS provider's alignment or the existing `examleaf-alignment-localize` forced alignment;
- (c) **onset and energy envelopes** for SFX placement and ducking.

### 5.3 Voice via MCP/TTS

[V4] uses Higgsfield → ElevenLabs v3 (preset "Arthur"). [V2] and [V3] use MCP voice generation. [N19] keeps voiceover keys outside the project.

[Recommendation] Keep ExamLeaf's `examleaf-voice-synthesis` and `examleaf-tts-provider-adapter` as the only voice path, so that persona, pronunciation (`examleaf-stem-pronunciation`) and Hinglish/Hindi direction are preserved. MCP voice is acceptable only for exploratory storyboards. ElevenLabs MCP install details were not verified (§11).

### 5.4 Mixing and loudness

- **Targets** [Recommendation, from [V4-MP]]: integrated about −14 LUFS, true peaks below −1.5 dBFS, music 15–20 dB under the voice, sidechain-style ducking on speech.
- [N20] warns that some toolchains do **no normalisation unless asked**. Make loudness a mandatory final step: FFmpeg's `loudnorm` filter, or the existing `examleaf-audio-production-engineer`.
- Verify with `examleaf-audio-caption-qa`.

### 5.5 Passing timing to the animation [Recommendation]

Use one canonical **cue sheet JSON** per scene:

```json
{"scene_id":"phy-10-03-s04","fps":30,"duration":7.4,
 "words":[{"w":"refraction","t0":1.12,"t1":1.71}],
 "beats":[0.0,0.6,1.2],
 "cues":[{"id":"label_n1","at":1.07,"kind":"reveal"}],
 "sfx":[{"file":"pop.wav","at":1.07,"gain_db":-12}]}
```

- Animations read `cues[].at` and never hard-code times. This applies the [V4-MP] sync rule: a reveal lands on, or about 0.05 s before, its word.
- If narration is regenerated, re-align it, rebuild the cue sheet and re-render. Scene code does not change.
- Duration derives from the narration, not the other way round. Remember that `DURATION × fps` determines the frame count [N72].

---

## 6. MCP orchestration

### 6.1 Higgsfield

**Connect**
- claude.ai custom connector URL `https://mcp.higgsfield.ai/mcp`, added under Settings → Connectors [N29] (contested).
- ChatGPT uses the Higgsfield Plugin with no URL [N30] (contested).
- CLI agents such as Claude Code: `npm i -g @higgsfield/cli`, then `higgsfield auth login` [N31].
- [V4] shows a web "install / connect" button flow.

**Capabilities seen**
- Image generation with a selectable model (GPT Image 2.5 in [V4-MP]).
- text2speech_v2 with an ElevenLabs variant and preset voices ([V4-MP]).
- Video models (15+ aggregated) [N78].
- Audio generation and the Website Building skill are unavailable in ChatGPT [N32]. Use claude.ai, Cursor or a CLI agent for audio.

**Credits**
- Every agent generation deducts credits regardless of plan; unlimited and free generations don't apply via MCP [N33].
- **No native credit cap**; prompt limits are not hard limits [N34].
- Results usually appear within 60 s of job completion; otherwise check Manage Account → Usage [N35].
- Plan prices (competitor-authored, unverified): Starter $15/month for 200 credits, Plus $34/month for 1,000 credits [N75].
- Premium video models use 40–70 credits per generation [N76]. Starter can be exhausted in 3–5 days of premium use [N77].
- Unlimited covers lower-tier models only [N79] and may be throttled at peak [N80].

[Recommendation] Use Higgsfield for:
- (1) 3×3 storyboard grids at the review gate;
- (2) optional collage cutouts and backgrounds.

Never use it for labelled science, and avoid premium video models entirely: ExamLeaf's visuals are code. Wrap every call in a budget ledger with:
- a per-job credit estimate before the call;
- a hard stop when the ledger hits the job cap;
- a human approval for overruns;
- logging of each job ID, so missing results can be reconciled after the 60 s window [N35].

### 6.2 Blender MCP

[V3] shows Blender-MCP 3D motion graphics. No verified install, permission or tool list was collected.

[Recommendation] Use it only as an optional authoring assistant. Production 3D should be versioned Python scripts run by `examleaf-blender-scenes` headlessly, so renders are reproducible and reviewable.

### 6.3 ElevenLabs, music and image MCPs

- [V2] and [V3] describe "music studio" MCPs and image and voice MCPs generically. [V4] reaches ElevenLabs v3 through Higgsfield.
- No verified details were collected for a direct ElevenLabs MCP or for specific music MCPs (§11).

[Recommendation] Route through ExamLeaf's provider adapters instead. That keeps one place for keys, voices, pronunciation dictionaries and cost logging.

### 6.4 Permissions, budgets and failure modes

**Permissions**
- Grant MCP tools per job, not globally.
- Keep API keys in the environment or a user config outside the repo, following the [N19] pattern, and never in the project or prompts.
- [V3] grants "full permission to use all the MCPs" for demos. Do not do this in production [Recommendation].

**Budgets**
- Pipeline-enforced caps for credits [N34] and tokens ([V1]).
- An approval gate before the asset phase. [V4]'s review checkpoint exists precisely to avoid wasting credits.

**Failure modes**
- Results delayed or missing [N35].
- Throttling stalls batch jobs [N80].
- A plan's free tiers don't apply via MCP [N33].
- The agent retries a failed generation and silently doubles spend [Hypothesis].
- Character inconsistency across asset calls ([V4-MP] mitigation: pass the reference image).
- An MCP-generated script or voice drifts from the approved script [Hypothesis]. Diff the text sent to TTS against the approved script.

---

## 7. Motion-design craft rules (avoiding "AI slop")

1. **Steer away from defaults.** Claude "defaults to safe choices unless explicitly encouraged otherwise" [N50]. Name fonts, palette and motion vocabulary, and ban overused fonts [N51][N55].
2. **Use dominant colours with sharp accents** rather than even palettes [N52]. Encode the ExamLeaf brand as tokens: background, ink, two accents, and subject colours for Physics, Chemistry, Maths and Biology.
3. **Choreograph one staggered entrance** rather than many micro-interactions [N53].
4. **Easing:** anticipation → action → follow-through. Never linear. Use back.out for pops, power3.out for slides, expo.out for whips ([V4-MP]).
5. **Hold times:** headlines readable at least 1.2 s [N60], longer for Hindi. Equations stay on screen until the narration has finished reading them, plus 0.5 s [Recommendation].
6. **One idea per frame,** with reveals across the scene, never everything at once ([V4-MP]).
7. **Sync:** each reveal lands on, or about 0.05 s before, its word; one sentence = one beat ([V4-MP]).
8. **Never frozen, never infinite.** Idle motion with finite repeats ([V4-MP]); a seeded RNG [N61].
9. **9:16 safe zones** [Recommendation]:
   - Canvas 1080×1920.
   - Keep text and critical diagram parts inside a central safe area that avoids the top status/title strip and the bottom caption, CTA and UI overlays used by Reels and Shorts.
   - Measure exact insets per platform against current app screenshots and store them as tokens. Exact pixel values were not in the verified evidence.
   - Adapt the [V4-MP] "90 px from edges" rule to larger top and bottom margins.
10. **Reference analysis with FFmpeg** [Recommendation; standard FFmpeg/ffprobe usage, verify on your build]:
    - Get duration and fps with ffprobe.
    - Detect cuts with FFmpeg's scene-change select filter plus `showinfo` to compute the shot-length distribution.
    - Extract one still per shot for palette and typography study.
    - Feed the measured numbers (median shot length, cut rhythm, text hold) into the brief. [V3] stresses studying "layout structure and its exact typography treatment".
11. **Photosensitivity:** [V1] warns its videos have "bright, fast flashes". For students, ban full-frame flashes and limit rapid luminance changes; check them in visual QA [Recommendation].
12. **Depth:** ask for parallax layers, foreground strips and shadows. [V2]'s first pass was flat.
13. **Do not let decoration contradict the science.** A stylised arrow or wobble must not change an angle, a ratio or a direction that the lesson teaches [Recommendation].

---

## 8. Edge cases and failure modes

| # | Edge case | Symptom | Cause | Prevention / fix | Source |
|---|---|---|---|---|---|
| 1 | Silent medium effort | Mediocre, generic scenes | Opus/Sonnet 5.5 default to medium | Pass effort explicitly per run | [N22] |
| 2 | Requested level unsupported | xhigh behaves like high | Silent fallback | Log the effective model and level; pin model IDs | [N23] |
| 3 | Ultracode runaway | Millions of tokens, limit windows exhausted, unfinished | Multi-agent reviews, separate caches, fresh restarts | Ban in production; sandbox only, low effort, budget | [V1], [N24] |
| 4 | Ultracode set as default | Can't be | Not accepted by settings or env | Use the launch flag only; audit the scripts | [N25] |
| 5 | Can't zero the thinking cost | Higher token use than expected | Thinking can't be disabled on 5.5 or Fable | Budget for it; lower effort for clerical tasks | [N26] |
| 6 | Alias drift | Different output across providers | Alias resolves to an older model elsewhere | Pin full model IDs | [N28] |
| 7 | One-line prompt | Random quality | L1 prompting | Structured brief plus reference | [V2] |
| 8 | Generic look | Same fonts and palettes everywhere | Safe defaults; convergence | Name or ban fonts; brand tokens | [N50][N51][N55] |
| 9 | Context contamination | Copies old projects | Agent reads sibling folders | "Do not inspect other folders"; one isolated workspace per job | [V3], [V2] |
| 10 | Missing audio | Silent render | Harness doesn't add audio by default | Require music and SFX in the brief | [V3] |
| 11 | Weak script | Dull narration | Agent-written script | Script from the narration system only | [V3] |
| 12 | Hallucinated facts on screen | Wrong numbers or labels | Agent "researches" itself | On-screen facts only from validated fixtures; science review | [V3], [Recommendation] |
| 13 | Model can't hear audio | Animation ignores the music | Text-only model | Provide an analysis JSON (beats, energy, words) | [V1], [N71] |
| 14 | Expecting an MP4 from the model | No video | Text-only output | A renderer executes the code | [N71] |
| 15 | Wall-clock animation | Frozen or garbled frames | Renderer seeks; never plays | Pure function of t | [N68][N18] |
| 16 | Missing seek contract | Render fails or wrong length | No DURATION or seek | Contract lint before render | [N72] |
| 17 | Unseeded randomness | Frames differ between renders | Math.random | Seeded PRNG; double-render hash test | [N61] |
| 18 | Infinite repeats | Seeking yields inconsistent states | Unbounded tweens | Finite repeats; seekable timeline | [V4-MP] |
| 19 | rAF polling | Render hangs | rAF doesn't fire in BeginFrame | setTimeout polling with a deadline | [N69] |
| 20 | Multiple video elements | Decoder errors, black frames | Parallel seeking exhausts decoders | workers = 1 for video-heavy scenes | [N70] |
| 21 | Chrome not found | Renderer won't start | Autodetect failed | Set `CHROME=/path` | [N17] |
| 22 | Old Node / no FFmpeg | HyperFrames fails | Requirements unmet | Preflight: Node 22+, FFmpeg | [N8] |
| 23 | Heavy clone | Slow or failing checkout | LFS payloads | `GIT_LFS_SKIP_SMUDGE=1` | [N13] |
| 24 | Archive too big | Codex build fails | Over 100 MB upload limit | Trim assets | [N12] |
| 25 | Skill/package version drift | Agent uses stale APIs | Unsynced upgrades | `/remotion-upgrade` before the benchmark | [N7] |
| 26 | Skills invisible to Claude | Skills not loaded | Missing `.claude/skills` symlink or existing folder | Check the symlink after install; handle Windows | [N66][N67] |
| 27 | Update without add | Undefined behaviour | Not documented | Always `add` first | [N65] |
| 28 | Manim framework mix | Import errors | CE vs GL incompatible | Standardise on CE | [N48] |
| 29 | ManimGL on ARM Mac | Install failure | Missing cairo/pkg-config | `arch -arm64 brew install pkg-config cairo` | [N47] |
| 30 | Manim parallel tests | OOM | Too many workers | 4–6 workers | [N49] |
| 31 | Stereo with sparse=True | librosa error | Multi-channel unsupported | Downmix or `sparse=False` | [N37] |
| 32 | Tempo is an array | Type errors downstream | ndarray return | `float(tempo[0])` | [N38] |
| 33 | Beats in frames | Sync off by a large factor | Default units | `units='time'` | [N39] |
| 34 | Silent or beatless audio | Empty beat list, 0 BPM | No onsets | Guard; fall back to a narration grid | [N41] |
| 35 | Resample drift | Cues slip over time | 22050 Hz default | `sr=None`; consistent sr | [N81] |
| 36 | Bad librosa args | ParameterError | Missing y/onset or bad units | Validate inputs | [N40] |
| 37 | Prior given | start_bpm ignored | API behaviour | Use one or the other | [N36] |
| 38 | Variable tempo | Shape error | bpm shape ≠ onset envelope | Match shapes | [N42] |
| 39 | Unnormalised audio | Loudness jumps between scenes | No processing by default | Final loudnorm to −14 LUFS | [N20], [V4-MP] |
| 40 | Keys leaked into the repo | Secret exposure | Keys in the project | Env or user config only | [N19] |
| 41 | MCP credits on any plan | Unexpected spend | Agent generations always billed | Ledger and estimate before each call | [N33] |
| 42 | No credit cap | Runaway generation | Prompt limits aren't hard | Pipeline-enforced cap | [N34] |
| 43 | Late results | Agent thinks a job failed and retries | Delivery up to about 60 s | Wait, then check usage; idempotent job IDs | [N35] |
| 44 | Throttling | Batch stalls | Peak-time limits | Off-peak batches; retries with backoff | [N80] |
| 45 | Starter exhausted | Pipeline halts mid-lesson | 200 credits; premium models | Avoid premium video; size the plan | [N76][N77] |
| 46 | Audio missing in ChatGPT | No Higgsfield audio | Platform limitation | Use the CLI agent or claude.ai | [N32] |
| 47 | Skipped review gate | Credits wasted on rejected visuals | No checkpoint | Mandatory storyboard approval | [V4] |
| 48 | Character drift | Hero looks different per shot | Independent generations | Pass the reference image; pose variants | [V4-MP] |
| 49 | 16:9 guide in a 9:16 pipeline | Cramped or cropped compositions | Style guide aspect | Vertical re-layout rules | [V4-MP], [Recommendation] |
| 50 | Short headline hold | Unreadable text | Fast transitions | ≥1.2 s, longer for Hindi | [N60] |
| 51 | Platform UI overlap | Captions hidden by app chrome | Unsafe placement | Safe-zone tokens, QA overlay | [Recommendation] |
| 52 | Photoreal request | Uncanny or failed output | Not a text-to-video model | Route to video generators or redesign | [N62] |
| 53 | Parser expects a fenced html block | Helper error | Strict format | Enforce the output format | [N56] (contested) |
| 54 | Image model draws text or formulas | Misspelled labels, wrong equations | Raster generation | Build text in code only | [V4-MP], [Recommendation] |
| 55 | Indic glyph gaps | Tofu boxes, broken conjuncts | Font lacks the script; per-code-point animation | Noto-class fonts; per-word animation | [Hypothesis] |
| 56 | Photosensitive flashes | Viewer discomfort | Rapid luminance changes | Flash ban in QA | [V1], [Recommendation] |
| 57 | Fable 5.5 assumptions | Plans built on an unreleased model | Leak hype | Model-agnostic harness | [V5] |
| 58 | Context/output limits change | Truncated long scene files | Limits as of article | Recheck the catalog; split files | [N73] |
| 59 | Release-date claims | Wrong compatibility assumptions | Unsourced article | Verify with Anthropic | [N59] |
| 60 | "Don't stop until perfect" | Endless loops, cost | Unbounded instruction | Max N rounds plus a rubric | [V2], [V1] |
| 61 | Haiku long prompts | Higher per-token cost | >100K-token prompts | Keep Haiku prompts short | [N28] |
| 62 | Plugin with another model | Unknown behaviour | Untested claim | Test before switching models | [N21] |
| 63 | TTS regenerated | Reveals out of sync | Timings changed | Cue-sheet driven code; re-align | [V4-MP], [Recommendation] |
| 64 | Composition-wide time fx (shake, push-in) | Diagrams misread | Camera moves distort geometry | No camera fx during measurement or label reveals | [Recommendation] |
| 65 | Headless WebGL variance | 3D frames differ by machine | GPU/driver differences | Fixed render box; software GL fallback test | [Hypothesis] |

---

## 9. Integration with the ExamLeaf pipeline

[Recommendation] This is the proposed flow, from the existing stages to the new layer. Arrows are hand-offs; ⛔ marks a mandatory gate.

1. **Lesson plan and curriculum** (`examleaf-curriculum-map`, `examleaf-lesson-plan`) → **science claims** (`examleaf-claim-research`, `examleaf-science-physics/chemistry/math/biology`) → validated data fixtures (JSON: values, units, geometry, labels).
2. **Script.** `examleaf-super-teacher-scriptwriter` with `examleaf-science-reviewer` and `examleaf-confidence-editor` → ⛔ **human academic approval**. The animation agent never writes or edits approved text.
3. **Storyboard routing.** `examleaf-storyboard-route` tags each scene:
   - `data-bound` (axes, values, structures, equations) → `examleaf-svg-scenes`, `examleaf-manim-scenes`, `examleaf-molecule-scenes`, `examleaf-biology-scenes`, or new three.js scenes fed from fixtures;
   - `spatial-hero` → `examleaf-blender-scenes`;
   - `illustrative/narrative` (hook, analogy, story, recap) → the **advanced animation layer** (doodle, collage, kinetic type, editorial);
   - `typographic` → the kinetic typography skill.
4. **Storyboard gate.** A 3×3 grid per lesson segment, built either from code-rendered thumbnails (free) or Higgsfield GPT Image (credits) → ⛔ **human approval of visuals and credit estimate** ([V4]).
5. **Narration.** `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter`, with `examleaf-stem-pronunciation` and `examleaf-multilingual-director`. Then `examleaf-alignment-localize` produces word timings, which go into the cue sheet (§5.5), along with `examleaf-speech-animation-synchronizer`.
6. **Scene authoring.** Claude Code (Opus 5.5, high) writes scene code against the harness contract, reading only the cue sheet, brand tokens, style guide and fixtures.
7. **Composition.** `examleaf-web-composition` (HyperFrames default; Remotion benchmark) assembles the 1080×1920 timeline and imports clips from Manim, SVG, three.js and Blender.
8. **Audio.** Python music/SFX bed plus narration, mixed by `examleaf-audio-production-engineer`, then loudness normalisation.
9. **QA gates:**
   - `examleaf-visual-qa`: safe zones, contrast, flash check, label legibility, a frame-hash determinism test;
   - `examleaf-audio-caption-qa`: LUFS and peaks, caption sync;
   - a science re-check comparing on-screen numbers and labels against fixtures by OCR or DOM text dump [Recommendation];
   - `examleaf-release-review` → ⛔ final human sign-off.
10. **Reels.** `examleaf-reel-repurpose` re-cuts lesson scenes to 20–60 s. Because scenes are time-pure, a reel can re-seek sub-ranges, re-time them to a beat grid (librosa) and add a hook card. Then `examleaf-thumbnail-package`.
11. **Ops.** `examleaf-observability-cost` logs tokens, effort, model ID, credits, render minutes and fix loops per scene. `examleaf-render-batch` runs renders on a preflighted box (Node 22+, FFmpeg, Chrome, fonts). `examleaf-skills-security` reviews third-party skills ([N15], [N44], [N1], [N58]) before install.

**Accuracy invariant** [Recommendation]: any glyph that encodes science must be traceable to a fixture field. This covers numbers, units, chemical formulae, labels, arrows' directions and graph shapes. Scene code receives fixtures as read-only props, and QA diffs rendered text against fixtures.

---

## 10. Proposed skill set for the "advanced animation" layer

These are for the build team. Each skill lists its purpose, inputs → outputs, dependencies, and the edge cases it must handle. "Extends" means amend an existing skill rather than create a duplicate (see `06_skills_library/OVERLAP_and_DEDUPLICATION.md`).

1. **`examleaf-anim-brief`** (new)
   - **Purpose:** assemble the L2/L3 structured prompt.
   - **Inputs → outputs:** approved script, scene route, style ID, cue sheet, brand tokens, reference analysis → brief.md plus a constraints block (harness contract, determinism, safe zones, fonts allow/ban list, hold times, iteration cap, "do not read other folders").
   - **Dependencies:** storyboard-route, pacing-controller.
   - **Edge cases:** #7–9, 11, 12, 50, 60.

2. **`examleaf-reference-analyzer`** (new)
   - **Purpose:** turn a reference video into measurable pacing and style specs.
   - **Inputs → outputs:** reference mp4 → JSON (fps, duration, shot lengths, cut rhythm, palette swatches, text-hold estimates, stills).
   - **Dependencies:** FFmpeg/ffprobe.
   - **Edge cases:** variable-fps input, letterboxed 16:9 references, copyrighted references used for analysis only (never asset reuse).

3. **`examleaf-style-guides`** (new library)
   - **Purpose:** versioned house style guides for 9:16: paper-collage-vertical (adapted from [V4-MP]), doodle-handdrawn, editorial-vox, kinetic-type, voxel-isometric. Each holds the palette, fonts (with Indic coverage), motion vocabulary, SFX list, writing hooks and do/don't lists.
   - **Edge cases:** #49, 54, 55, 56.

4. **`examleaf-anim-storyboard-gate`** (extends storyboard-route)
   - **Purpose:** produce a 3×3 grid per segment (code thumbnails or Higgsfield), a credit and token estimate, then stop for approval.
   - **Outputs:** grid image, beats.json, estimate.json, approval record.
   - **Edge cases:** #41, 42, 45, 47, 48.

5. **`examleaf-motion-harness`** (extends web-composition)
   - **Purpose:** a single contract for HyperFrames, Remotion and raw pipelines (`DURATION`, `seek(t)`, seeded PRNG, cue-sheet loader, 1080×1920 canvas, font preload) plus a linter and a double-render frame-hash determinism test.
   - **Edge cases:** #14–24, 26, 65.

6. **`examleaf-procedural-2d`** (new)
   - **Purpose:** Canvas/SVG primitives for doodle and collage: wobble strokes, draw-on, boil, paper textures, die-cut borders, shadows, tear and paper-flip gags, depth layers.
   - **Edge cases:** #17, 18, 64.

7. **`examleaf-kinetic-typography`** (new)
   - **Purpose:** word- and grapheme-cluster-timed type animation from the cue sheet, ransom/handwriting/label modes, Hindi/Assamese-safe.
   - **Edge cases:** #50, 55, 63.

8. **`examleaf-threejs-scenes`** (new)
   - **Purpose:** seek-pure three.js scenes (fixed-step physics replay, seeded layouts, orthographic voxel mode) fed by fixtures, exported as clips.
   - **Edge cases:** #15, 17, 65; WebGL context loss in headless mode.

9. **`examleaf-audio-compose`** (new)
   - **Purpose:** seeded Python music beds and an SFX palette per style, bar-aligned stems, mood variants.
   - **Outputs:** WAV stems plus metadata (BPM, bars).
   - **Edge cases:** #10, 39; licensing of any samples used.

10. **`examleaf-audio-analysis`** (new)
    - **Purpose:** librosa beat grid, onsets and energy for beds and reels.
    - **Edge cases:** #31–38 (stereo/sparse, ndarray tempo, units, sr, empty beats, priors, shapes).

11. **`examleaf-cue-sheet`** (extends speech-animation-synchronizer and alignment-localize)
    - **Purpose:** merge word timings, beats and SFX into the canonical cue sheet; re-time on TTS regeneration.
    - **Edge cases:** #33, 35, 63.

12. **`examleaf-mcp-orchestrator`** (new)
    - **Purpose:** wrap Higgsfield (and future Blender, music or voice MCPs) with per-job permissions, an estimate-before-call, a hard credit ledger, idempotent job IDs, 60 s result reconciliation, retry with backoff, and secrets kept outside the repo.
    - **Edge cases:** #40–46.

13. **`examleaf-effort-governor`** (extends observability-cost)
    - **Purpose:** choose model, effort and iteration cap per task (§3.4); refuse ultracode; log the effective level, tokens and cost; alert on budget overrun.
    - **Edge cases:** #1–6, 58, 60, 61.

14. **`examleaf-anim-qa`** (extends visual-qa and audio-caption-qa)
    - **Purpose:** safe-zone overlay check, hold-time check, flash and luminance check, a determinism hash, fixture-vs-rendered text diff, LUFS and peak check.
    - **Edge cases:** #12, 17, 39, 50, 51, 56.

15. **`examleaf-vertical-adapt`** (new)
    - **Purpose:** rules and helpers for re-laying out 16:9 references and guides into 9:16 (stacked layouts, top title / middle visual / bottom caption zones), and for sub-range reels.
    - **Edge cases:** #49, 51.

**Third-party skills to evaluate (security review first):** `remotion-dev/skills` [N1], `heygen-com/hyperframes` [N58]/plugin [N10], `klsoen/opus-js-animations` [N15], `adithya-s-k/manim_skill` (CE only) [N45].

---

## 11. Open questions, unverified claims and vendor questions

1. **Anthropic:** Is there an official "Claude Motion" feature? What is the confirmed Opus 5.5 release date [N59] and the current context and output limits [N73]? How does prompt caching behave across ultracode sub-agents ([V1])? Is there an official cost per effort level?
2. **Fable 5.5 ([V5]):** release status, effort defaults, pricing, and whether its animation quality claims hold up. All unverified.
3. **Remotion:** commercial licence terms for a company of ExamLeaf's size; captions and audio APIs; required Node version; whether `skills add` creates the `.claude/skills` symlink and how it treats an existing folder [N67]; the `skills update`-before-`add` behaviour [N65]; whether project-creation skill install is still offered [N2] (contested).
4. **HyperFrames:** confirm the seek-only `window.__hf` API [N68] (contested); bundled tween library (GSAP?); worker settings; 9:16 presets; font and Indic shaping in its Chrome build; the list of its 21 skills [N11].
5. **Higgsfield:** confirm the MCP URL path [N29] (contested) vs CLI [N31]; per-model credit costs for image and TTS; actual plan prices (the [N75] figures are competitor-authored); API-level spend caps; data retention of uploaded storyboards; licence and ownership of generated assets for commercial education; Indian-English and Hindi voice quality via the ElevenLabs variant.
6. **Blender MCP / ElevenLabs MCP / music MCPs:** no verified install, permission or pricing evidence; evaluate before use.
7. **[V1] figures** are one creator's single runs on a subscription, estimated at API prices. Per-level values for medium, high and xhigh were not stated in the transcript, and the ultracode token count is a lower bound.
8. **Opus vs Sonnet 5.5 for scene code:** [V2] says Sonnet works but is less polished. ExamLeaf should run an A/B on its own templates.
9. **9:16 safe-zone insets** per platform (Instagram Reels, YouTube Shorts) need measurement. No verified pixel values.
10. **Indic typography:** test conjunct shaping and per-grapheme animation in headless Chrome for Devanagari and Bengali-Assamese scripts.
11. **Headless WebGL determinism** across machines: decide on a single render box or a software-GL policy.
12. **[N56]** (fenced-html parser) and **[N61]** (pure-function determinism) are flagged contested in the evidence set. Treat them as strong guidance, not guarantees.

---

## Sources

**Reference videos**
- [V1] Devarf, "I Had Opus 5.5 Make the Same Music Video at Every Effort" — https://www.youtube.com/watch?v=3S4vuHxGh7c
- [V2] RandomAI, "Claude Opus 5.5 + JavaScript = INSANE 2D Animations (Full Tutorial)" — https://www.youtube.com/watch?v=MPDhk385gSg
- [V3] RandomAI, "Claude Opus 5.5 Is INSANE at Motion Graphics" — https://www.youtube.com/watch?v=OIAWkkSO4WY
- [V4] RandomAI, "Claude Opus 5.5 Makes INSANE Educational Animations (Full Tutorial)" — https://www.youtube.com/watch?v=WXu4O9oIdIE (sponsored by Higgsfield). [V4-MP] master prompt: https://docs.google.com/document/d/12f1-nob7t0-wf809BX8WdLaGgWeU9UXxIhRXKXYWMYs (local copy: 00_reference_videos/master_prompt_paper_collage.md)
- [V5] RandomAI, "Claude Fable 5.5 Just Got Leaked and It's INSANE" — https://www.youtube.com/watch?v=BbsoRYprICI (unverified capability signal)

**Web evidence**
- [N1]–[N7] https://www.remotion.dev/docs/ai/skills
- [N8]–[N14] https://github.com/heygen-com/hyperframes
- [N15]–[N21] https://github.com/klsoen/opus-js-animations
- [N22]–[N28] https://code.claude.com/docs/en/model-config
- [N29]–[N35] https://higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent
- [N36]–[N43] https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html
- [N44]–[N49] https://github.com/adithya-s-k/manim_skill
- [N50]–[N56] https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics
- [N57]–[N62] https://aiidelist.com/blog/opus-5-5-motion-design
- [N63]–[N67] https://www.remotion.dev/docs/cli/skills
- [N68]–[N70] https://www.heygen.com/research/html-to-video
- [N71]–[N73] https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5
- [N74] https://claude.com/pricing
- [N75]–[N80] https://creatify.ai/blog/what-is-higgsfield-mcp-what-it-does-what-it-costs-and-how-to-use-it
- [N81] https://librosa.org/doc/0.11.0/tutorial.html
