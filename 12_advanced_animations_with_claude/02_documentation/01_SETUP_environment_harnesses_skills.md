# 01 · Setup: from an empty machine to a ready animation workstation and render box

**Purpose.** Step-by-step setup for the advanced-animation layer: prerequisites, fonts, GPU policy, the HyperFrames and Remotion harnesses, opus-js-animations, Manim CE, Python audio tools, third-party skill admission, Claude Code configuration (models, effort, ultracode, permissions), the per-job workspace, the preflight script and a verification checklist with expected outputs.

**Read with.** `07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` (the existing engine and narration setup; do that first), `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` (admission procedure), `12_advanced_animations_with_claude/04_harness_contract/preflight.sh` and `12_advanced_animations_with_claude/04_harness_contract/README.md`.

**Conventions.** [N#], [V#], [V4-MP], [Recommendation], [Hypothesis] and "verify" as in doc 00. Edge cases are #1–#65 from report §8. **Nothing below has been installed or run by this section.** Every command is either quoted from the evidence (with its [N#]) or is standard tool usage marked as such; flags that were not in the evidence are marked "verify".

---

## 1. Two machines, two jobs

| Machine | Purpose | OS | Holds secrets? | Internet |
|---|---|---|---|---|
| **Authoring workstation** | Runs Claude Code headless in the terminal, one job folder at a time; previews scenes; runs lint and quick renders | macOS or Linux (authoring and review may be macOS, RD-24) | Only the Claude Code login. Provider keys live in the provider worker (§6) | Yes, for Claude and for admitted installs |
| **Render box** | Final renders, determinism hashes, encodes, loudness measurement | **Linux** (container or WSL2), pinned image (RD-24) | **None** | **None after assets are staged** (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2) |
| Provider worker (logical role; may be a container on the workstation) | The only place that calls Higgsfield or a TTS provider | Linux container | Its own scoped key only | Its approved domain only |

Why split: the render cache key in the existing engine includes OS, Python, FFmpeg and font hashes, so one reference environment avoids cross-platform churn (`07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` §1); and headless WebGL output can differ by machine (#65).

---

## 2. Prerequisites

### 2.1 Table of prerequisites

| # | Component | Required version / form | Why | Evidence | Edge case |
|---|---|---|---|---|---|
| P1 | **Node.js** | **22 or newer** | HyperFrames requirement | "Requirements: Node.js 22+, FFmpeg" [N8] | #22 |
| P2 | **FFmpeg and ffprobe** | Reviewed build on `PATH` (Homebrew's `ffmpeg` provides `ffprobe`) | HyperFrames requirement; encoding; reference analysis; loudness | [N8]; existing setup §2 | #22 |
| P3 | **Chrome or Chromium** | Pinned build on the render box | Headless seek rendering for raw pipelines; set `CHROME=/path` if autodetect fails | "set `CHROME=/path` if it isn't found" [N17] | #21 |
| P4 | **Python** | ≥ 3.11; 3.13 is the reference (RD-33) | Manim CE, NumPy audio, librosa, determinism hash script | existing packs `>=3.11` | — |
| P5 | **Fonts** | Vendored files, licence recorded, hashed (RD-23) | Science text (Inter, Noto Sans, KaTeX), Indic scripts, style display fonts | RD-23; [V4-MP] font list | #8, #55 |
| P6 | **git** | Any current | Pinned commits for admitted skills | `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4 | #23 |
| P7 | **Claude Code** | Version recorded per job ([V1] used 2.1.287) | Authoring agent | [V1] | #1–#6 |
| P8 | **GPU or software-GL decision** | One policy per render box | three.js and voxel scenes | [Hypothesis] | #65 |

### 2.2 Install on macOS (authoring workstation)

The existing project already documents the macOS path for the engine (`07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` §2.3): `brew install python@3.13 ffmpeg cairo`. For this layer, add Node 22+ from a reviewed channel (Homebrew, the official installer or a version manager; choose one and record it) and a Chrome or Chromium build.

**Observed on this Mac (read-only check by this section, 14 Oct 2026):**

| Item | Found | Verdict |
|---|---|---|
| Node.js | v20.19.4 (via nvm) | **Below the Node 22+ requirement** [N8] (#22): install Node 22+ before HyperFrames |
| ffmpeg / ffprobe | not on `PATH` | **Missing** (#22); matches the existing setup note |
| Python | 3.14.2 (Homebrew) | ≥ 3.11, but not the 3.13 reference (RD-33); Manim CE and librosa support for 3.14 is unverified, so use a 3.13 virtual environment |
| Manim | not installed | Install CE only (§4.4) |
| Google Chrome | present in `/Applications` | Record its version; set `CHROME` if a renderer cannot find it (#21) |

**Addendum, 15 Oct 2026 (audit "Setup executability", executability-4/-5/-7).** Re-checked on this Mac:

| Item | Found | What to do |
|---|---|---|
| `python` | **no `python` binary**; only `python3` (Homebrew 3.14.2) and a Python 3.11 | Always type `python3`. Run every selftest as `python3 -B -I <script> --selftest` (no bytecode, isolated mode). |
| Virtual environment | none | Pin the interpreter, never "whatever `python3` is": `python3.13 -m venv .venv` after `brew install python@3.13` (RD-33 reference), or `python3.11 -m venv .venv` with the 3.11 already here. Do not build the Manim/librosa venv on 3.14 (support unverified). Check with `.venv/bin/python --version`. |
| Node.js | default shell is **v20.19.4**; **v24.6.0 is already installed under nvm** | `nvm use 24` (or `nvm alias default 24`) before any HyperFrames or `lint_seek_contract.js` work; `node --version` must print v24.x. No new install is needed. |
| ffmpeg **and** ffprobe | **both missing** from `PATH` (not only ffprobe) | `brew install ffmpeg` (provides both). Until then the loudness gate, `reference_analysis.sh`, `analyze_reference.py` and every encode are blocked (exit 2), and `preflight.sh` reports two FAIL rows. |

### 2.3 Install on Linux (render box)

The existing Debian path: `sudo apt-get install -y python3 python3-venv python3-pip ffmpeg libcairo2 fonts-dejavu-core git` (`07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` §2.2). Add Node 22+ from a reviewed source (distribution packages may lag behind 22; check before relying on them) and a pinned Chromium. Pin the container image by digest and record the FFmpeg build string and Chrome version in `ledgers/environment.md`.

### 2.4 Version checks (standard usage)

```sh
node --version          # must print v22.x or higher [N8]
ffmpeg -version | head -1
ffprobe -version | head -1
python3 --version       # >= 3.11; 3.13 on the reference box (RD-33). There is no `python` binary on this Mac (15 Oct 2026)
.venv/bin/python --version   # the pinned venv (3.13 or 3.11), never 3.14
"$CHROME" --version     # only if CHROME is set [N17]
git --version
claude --version        # record in the job log
```

### 2.5 Chrome discovery (#21)

1. Install Chrome or Chromium from a reviewed channel.
2. If a renderer reports that Chrome was not found, export the path: `export CHROME=/absolute/path/to/chrome` [N17].
3. Put the same path in the render box's environment file (not in the repo).
4. Record the Chrome version with the job's environment hash; a Chrome upgrade invalidates the determinism baseline (doc 04 §7).

### 2.6 GPU and software-GL policy (#65)

[Hypothesis] Headless WebGL output can vary with GPU, driver and anti-aliasing. Policy [Recommendation]:

1. Designate **one render box** for any scene that uses WebGL (three.js, voxel).
2. Record GPU model, driver version and Chrome version in `ledgers/environment.md`.
3. Run the double-render determinism test (doc 04 §7) on that box. Store the baseline frame hashes per box.
4. Run the same scene once with a software-GL backend and compare. The Chrome switch that forces software GL differs between Chrome versions: **verify** against the Chromium documentation for your pinned build before scripting it.
5. If software GL is deterministic and fast enough for the pilot scenes, prefer it for portability; otherwise keep WebGL scenes on the designated GPU box only. Record the decision (open question Q11 in doc 14).
6. Never compare frame hashes across boxes for WebGL scenes; compare per box.

---

## 3. Fonts

### 3.1 What to install

| Role | Fonts | Source of the rule | Notes |
|---|---|---|---|
| Science text (labels, equations, units, axes) | **Inter**, **Noto Sans** script families, **KaTeX** fonts | RD-23; `02_learning_psychology/palette_and_typography_tokens.json` | Medium or semibold for essential labels |
| Hindi (Devanagari) | Noto Sans Devanagari (plus a licensed Devanagari display face for titles, to be chosen) | [Hypothesis] coverage; RD-23 "script coverage tests" | Test conjuncts (§3.3) |
| Assamese (Bengali–Assamese script) | Noto Sans Bengali (covers the Bengali–Assamese block) | [Hypothesis]; verify that the chosen file contains ৰ and ৱ | Assamese voice comes later (section 11), but on-screen terms may appear earlier |
| Paper-collage style display | Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One; **Caveat Brush**; **Patrick Hand** | [V4-MP] §5 | Latin display faces; Devanagari/Assamese coverage must be **verified per file** before use with Hindi or Assamese text |
| Other house styles | Per `12_advanced_animations_with_claude/05_style_guides/style_tokens.json` | doc 03 §4 | Allow/ban list in doc 03 |

### 3.2 Rules

1. **Vendor every font file** into the repository's font directory with its licence; record name, version, licence, SHA-256 and where used in `ledgers/licences.md` (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5). Display fonts named in [V4-MP] are commonly distributed under the SIL Open Font License, but **verify each file's licence** before vendoring.
2. **No network fonts in renders.** "No uncontrolled network fonts or remote media dependencies during final rendering" (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2). Scene code uses `@font-face` with local URLs only; the linter rejects remote font URLs (doc 04 §8).
3. **Hash fonts into the environment record**, as the existing engine does with its font hash (`07_end_to_end_pipeline_instructions/01_SETUP_new_machine_and_repository.md` §0).
4. **Ban by default** [N51][N55]: Arial and Space Grotesk as display fonts; Inter as a *display* font in illustrative styles (it stays the science font). Details and rotation in doc 03 §4.

### 3.3 Glyph-coverage checks (#55)

Standard fontconfig usage on Linux (verify the language tags on your fontconfig build):

```sh
fc-list :lang=hi family file     # fonts claiming Hindi (Devanagari) coverage
fc-list :lang=as family file     # fonts claiming Assamese coverage (verify tag support)
```

A language claim is not proof. Also render a test card through the harness (doc 04 §6) containing at least:

| Script | Test strings | What to look for |
|---|---|---|
| Devanagari | क्ष, त्र, ज्ञ, श्र, द्ध, र्क, कि, की, विद्युत, प्रतिरोध | Conjuncts formed, reph placed, matras attached; no dotted circles, no tofu boxes |
| Bengali–Assamese | ক্ষ, ৰ, ৱ, বিদ্যুৎ, প্ৰতিৰোধ | ৰ and ৱ present (Assamese-specific letters); conjuncts and vowel signs correct |
| Latin + science | I l 1, O 0, −, ., x², H₂O, Ω, λ, θ, μ | Confusable glyphs from `02_learning_psychology/palette_and_typography_tokens.json` `glyphs_to_test` |

The Hindi and Assamese words above are test strings only; correct terminology comes from the native-language editor and `examleaf-stem-pronunciation`. A native-language editor signs off the test card per font file.

---

## 4. Harnesses and tools

### 4.1 HyperFrames (default master timeline)

**Facts.** Requires Node.js 22+ and FFmpeg [N8]. Scaffold with `npx hyperframes init my-video` [N9]. Claude Code plugin: `claude plugin install hyperframes@hyperframes` after adding the marketplace [N10]. Agent skills via `npx skills add heygen-com/hyperframes` [N58] (tutorial source). The repo "ships 21 skills agents load on demand" [N11]. Clone without LFS payloads using `GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` [N13]. Licence: Apache 2.0, "no per-render fees or commercial-use thresholds" [N14]. A Codex archive build fails above Codex's 100 MB upload limit [N12].

**Steps** [Recommendation, following `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4]:

1. **Admit first.** Run the admission procedure (§5) on `heygen-com/hyperframes` before any install. Record the reviewed commit SHA (not a blob SHA) and the npm package version.
2. **Inspect without LFS** (#23): `GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/heygen-com/hyperframes.git` [N13], then `git -C hyperframes checkout --detach <APPROVED_COMMIT>`.
3. **Scaffold in a scratch folder**, never in a lesson folder: `npx hyperframes init my-video` [N9]. Pin the exact `hyperframes` package version in `package.json` and commit the lockfile. Running `npx` without a pinned version fetches whatever is current; pin it (version: verify at admission).
4. **Disable on-demand auto-install.** The runbook requires "disable its on-demand workflow auto-install" (`07_end_to_end_pipeline_instructions/02_PHASED_BUILD_ROADMAP.md` P1) and "HyperFrames' router can auto-install workflows — disable unaudited auto-expansion" (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4). The exact switch is not in the evidence: **verify** in the admitted commit's docs.
5. **Skills, selectively.** `npx skills add heygen-com/hyperframes` [N58] installs the bundle; the runbook treats `npx skills add` as "a discovery/install route, not an audit procedure". Prefer copying only the reviewed skill folders you need into the package's `.claude/skills/` (RD-25). The list of the 21 skills is open question Q4.
6. **Plugin (optional).** `claude plugin install hyperframes@hyperframes` [N10] after adding the marketplace. The marketplace-add command for HyperFrames is not in the evidence: **verify**. A plugin "can bundle Skills, MCP servers and hooks" (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4), so review what it bundles before enabling it.
7. **Codex users** (#24): keep the archive under 100 MB [N12] by excluding renders, frames and large media.
8. **Video-heavy compositions** (#20): configure a single render worker [N70]. The worker flag name is not in the evidence: **verify**.
9. **Smoke test:** render the reference scene `12_advanced_animations_with_claude/04_harness_contract/scene_template.html` at 1080×1920, 30 fps, twice, and run `12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py` on the two outputs (doc 04 §7).

**Contested point.** HyperFrames compositions expose `window.__hf` with duration and seek [N68] (contested). The ExamLeaf contract uses `window.DURATION` + `async window.seek(t)` [N72] and a thin adapter for `window.__hf` (doc 04 §2). Confirm the real API at admission (open question Q4).

### 4.2 Remotion (benchmark challenger only)

**Facts.**
- One-command skill install: `npx skills add remotion-dev/skills` [N1].
- CLI family `npx remotion skills <subcommand>` [N63] with `add` ("Install skills from `remotion-dev/skills`") [N64] and `update` [N65]. "Only add and update documented" [N63].
- Skills install into `.agents/skills` [N66]; Claude Code compatibility comes from "symlinking `.claude/skills` to `.agents/skills`" [N67]. Whether the CLI creates the symlink, and what happens on Windows or with an existing `.claude/skills` folder, is not documented [N67] (#26).
- Skills may be offered at project creation [N2] (contested).
- Named skills: `/remotion-best-practices` ("encompasses all other skills") [N4], `/remotion-render` (video or still) [N5], `/remotion-maps` (Mapbox, MapLibre, MapTiler, GeoJSON, CesiumJS) [N6], `/remotion-upgrade` (Remotion, related packages, Mediabunny and installed skills together) [N7].
- Target agents: Claude Code, Codex, Kimi Code, Cursor [N3].

**Steps** [Recommendation]:

1. **Licence before anything commercial.** The section 12 evidence set has no verified Remotion licence terms (report §2.2). The existing runbook records a conditional commercial licence with per-render figures from the earlier ChatGPT research and says to confirm what a billable render is (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5; RD-07 "only after licence eligibility is confirmed"). Treat both as unverified until the benchmark team reads the current licence (open question Q3).
2. **Admit** `remotion-dev/skills` through §5; pin the commit.
3. **Install skills in a benchmark-only package**, never alongside the HyperFrames package: `npx skills add remotion-dev/skills` [N1] or `npx remotion skills add` [N64].
4. **Always `add` before `update`** (#27): behaviour of `update` when nothing was added is undocumented [N65].
5. **Check the symlink** (#26). Standard shell usage:
   ```sh
   ls -la .agents/skills
   ls -la .claude/skills       # should be a symlink to ../.agents/skills [N67]
   ```
   If `.claude/skills` is missing, create the link yourself from the package root: `ln -s ../.agents/skills .claude/skills`. If a real `.claude/skills` folder already exists, do **not** overwrite it: move its reviewed contents into `.agents/skills` first, then link, and re-run the skill listing in Claude Code to confirm both sets are visible. On Windows, symlinks need extra privileges; behaviour is undocumented [N67]: verify, or use the reference Linux box.
6. **Upgrade before benchmarking** (#25): run `/remotion-upgrade` [N7] once at the start of the benchmark, record the resulting versions, then freeze them for all benchmark runs.
7. **Composition size** 1080×1920 at 30 fps [Hypothesis: confirm in benchmark].
8. **Node version** for Remotion is not in the evidence: verify.
9. Benchmark protocol: `12_advanced_animations_with_claude/07_benchmark_and_pilot_plan/BENCHMARK_hyperframes_vs_remotion.md`.

### 4.3 opus-js-animations (raw Canvas/SVG/three.js pipeline, optional)

**Facts.** Plugin install `/plugin marketplace add klsoen/opus-js-animations` [N15]; manual install `cp -r opus-js-animations/skills/opus-js-animations ~/.claude/skills/` [N16]; parallel seek rendering in headless Chrome [N18]; `CHROME=/path` override [N17]; voiceover keys "read from the environment or `~/.config/opus-js-animations/keys.env`, never written into your project" [N19]; audio "cut on zero crossings, with no normalising, EQ or fades unless you ask" [N20]; MIT licence, other-model support untested [N21].

**Steps** [Recommendation]:

1. Admit through §5 and pin the commit.
2. Install **per package**, not user-global. [N16] copies into `~/.claude/skills/`, but the runbook keeps "activated copies only in the package's `.claude/skills/` or `.agents/skills/`" (RD-25). Copy the reviewed folder into the animation package's `.claude/skills/` instead.
3. Do **not** give it TTS keys. ExamLeaf narration comes only from `examleaf-tts-provider-adapter`; leave `~/.config/opus-js-animations/keys.env` absent on the workstation.
4. Treat its audio output as un-normalised (#39) [N20]: every mix goes through loudness normalisation and re-measurement (`05_narration_system/INSTRUCTIONS_narration_pipeline.md` step 10).
5. Test it with the pinned model before relying on it (#62) [N21].
6. Use it as a pattern source for `examleaf-threejs-scenes` and `examleaf-procedural-2d`; exported image sequences are imported into HyperFrames as clips (doc 04 §10).

### 4.4 Manim Community Edition only

**Facts.** `pip install manim`; verify with `manim --version` [N46]. Skills: `npx skills add adithya-s-k/manim_skill` installs both CE and GL skills [N44]; install only CE by path with `npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices` [N45]. CE and ManimGL "are separate, incompatible frameworks" [N48]. ManimGL on ARM macOS needs `arch -arm64 brew install pkg-config cairo` first [N47]. "Parallel testing with many workers can cause out-of-memory errors" [N49].

**Steps** [Recommendation]:

1. Create a dedicated virtual environment (standard usage): `python3 -m venv .venv-manim && . .venv-manim/bin/activate`.
2. `pip install manim` [N46], then pin the resolved version in a lock file (version: verify).
3. `manim --version` [N46]; record the output.
4. Install **only** the CE skill by path [N45] after admission. Never install the GL skill (#28).
5. On ARM macOS you do not need the GL prerequisites [N47] because GL is not used (#29); Cairo is already installed by the existing setup (`brew install … cairo`).
6. Limit parallel test or render workers to **4–6** [N49] (#30).
7. The existing `examleaf-manim-scenes` skill remains the owner of Manim scenes; this layer only imports its output (doc 04 §10).
8. 9:16 frame configuration for Manim is a [Hypothesis]; confirm the config keys in the pinned version's docs.

### 4.5 three.js and raw seek pipelines

1. three.js is MIT (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5). Vendor a pinned build file into the package; never load it from a CDN at render time (offline render rule).
2. Scenes follow the contract in doc 04 and render through either opus-js-animations [N18] or the HyperFrames clip path.
3. WebGL scenes obey the GPU policy in §2.6 (#65).

### 4.6 Python audio tools

1. A separate virtual environment for audio: NumPy, SciPy or soundfile for WAV writing, and librosa for analysis. The evidence cites the **librosa 0.11.0** documentation [N36]–[N43], [N81]; pin a 0.11.x release to match it (verify availability), and pin NumPy/SciPy/soundfile versions in a lock file (versions: verify in the pilot, report §5.1).
2. Seed every random call so re-renders are identical (report §5.1).
3. Known librosa traps the skill must guard (#31–#38): multi-channel only with `sparse=False` [N37]; tempo returned as an ndarray [N38]; beats in frames unless `units='time'` [N39]; `ParameterError` on missing input [N40]; empty beats on silence [N41]; bpm shape must match the onset envelope [N42]; `librosa.load` mixes to mono at 22050 Hz unless `sr=None` [N81].

---

## 5. Third-party skill, plugin and MCP admission

Every public skill, plugin, CLI or MCP server used by this layer goes through `examleaf-skills-security` and the procedure in `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4. Summary of that procedure:

1. Resolve the official repository; fetch a commit and read metadata, licence, manifests, install hooks, skill scripts and MCP entrypoints **without executing them**.
2. Record an exact **commit SHA** (not a blob SHA), distribution checksum and dependency lock.
3. Inspect filesystem scope, outbound domains, telemetry, subprocesses, code execution and credential loading.
4. Evaluate in a disposable user or container without production credentials, Docker socket or student data; package scripts disabled by default.
5. Install only selected reviewed folders; block on-demand auto-install and auto-update in production.
6. Run positive, negative, timeout, cost-cap and exfiltration tests; re-audit upgrades in a pull request.
7. Record the admission in `ledgers/skill_activations.md`.

**Candidates for this layer** (report §10, "security review first"):

| Source | Install route in the evidence | Licence | Admission notes |
|---|---|---|---|
| `heygen-com/hyperframes` | `npx hyperframes init` [N9]; plugin [N10]; `npx skills add heygen-com/hyperframes` [N58] | Apache-2.0 [N14] | Disable on-demand workflow auto-install; review plugin bundle |
| `remotion-dev/skills` | `npx skills add remotion-dev/skills` [N1]; `npx remotion skills add` [N64] | Skill licence separate from Remotion's (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5); verify | Benchmark package only; licence confirmation first (Q3) |
| `klsoen/opus-js-animations` | `/plugin marketplace add klsoen/opus-js-animations` [N15]; manual copy [N16] | MIT [N21] | Per-package copy; no TTS keys; untested with other models (#62) |
| `adithya-s-k/manim_skill` (CE skill only) | `npx skills add adithya-s-k/manim_skill/skills/manimce-best-practices` [N45] | MIT (per project directory) | Never the GL skill (#28) |
| Higgsfield CLI / MCP | `npm i -g @higgsfield/cli`, `higgsfield auth login` [N31]; connector URL [N29] (contested) | Provider terms | Provider worker only; doc 05 §6 |

**Hard rules** (existing, `07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §4): no `curl | sh`; never install every discovered skill; directories and marketplaces are discovery, not audits; install counts are not audits.

---

## 6. Secrets and keys (#40)

1. **No key in any project folder, prompt, brief, log or commit.** The pattern to copy is [N19]: keys "read from the environment or `~/.config/…/keys.env`, never written into your project".
2. Provider keys (Higgsfield, TTS) live **only** in the provider worker's secret store (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §2: "Keep model/provider keys only in an allowlisted worker secret store").
3. The authoring workstation's Claude Code session has **no** provider keys in its environment. Scene jobs never call providers; they read staged assets.
4. The render box holds no secrets at all.
5. Add a pre-commit or preflight check that refuses to proceed if files under the job folder match common key patterns (the preflight script's secret scan, §9).
6. If a key appears anywhere in a job folder or log: stop, rotate the key at the provider, purge the artefact, and record the incident.

---

## 7. Claude Code configuration

### 7.1 Facts that drive the configuration

| Fact | Evidence | Edge case | Consequence |
|---|---|---|---|
| Effort defaults to **high** on most models but **medium on Opus 5.5, Sonnet 5.5 and Haiku 5.5** | [N22] | #1 | Always set effort explicitly |
| Unsupported levels fall back silently to "the highest supported level at or below the one you set" | [N23] | #2 | Log the effective model and level per run |
| `claude --effort ultracode` starts at xhigh with ultracode on | [N24] | #3 | The only way to start ultracode; audit launch scripts for it |
| `effortLevel` (settings) and `CLAUDE_CODE_EFFORT_LEVEL` (env) do **not** accept `ultracode` | [N25] | #4 | Ultracode can never become a persisted default |
| Thinking cannot be turned off on Opus/Sonnet/Haiku 5.5 or Fable models | [N26] | #5 | Budget for thinking tokens; use lower effort for clerical tasks |
| Aliases (`opus`, `sonnet`, `haiku`) resolve to the newest version only on the Anthropic API | [N28] | #6 | Pin full model IDs |
| Haiku 5.5 prompts over 100K tokens cost more per token | [N28] | #61 | Keep Haiku prompts short |
| 1M-token context, up to 128K output tokens (as of the tutorial; recheck) | [N73] | #58 | Split long scene files; recheck limits |
| Ultracode in [V1]: ≥2.5M tokens, ~3 usage windows, never finished; sub-agents each built their own cache and restarted fresh | [V1] | #3 | Never in production |

### 7.2 Effort and model per task [Recommendation, report §3.4]

| Task | Model | Effort | Max fix loops |
|---|---|---|---|
| Brief and storyboard text, prompt assembly | Sonnet 5.5 | medium (set explicitly) | 2 |
| Scene code: 2D motion, kinetic type, collage, doodle | Opus 5.5 | **high** | 3 (AD-11) |
| Complex three.js, physics replay, intricate choreography | Opus 5.5 | **xhigh** | 3 |
| Debugging a render failure | Opus 5.5 | high | existing VE rule: ≤ 2 repair attempts, then human |
| Batch re-renders, captions, file operations | Sonnet or Haiku 5.5 | low–medium | 1 |
| max | Opus 5.5 | only with a written justification in the job log | 3 |
| **ultracode** | — | **never** in production or unattended runs; sandbox experiments only, with their own budget | — |

### 7.3 How to set it

- **Per run (preferred for scene jobs).** Launch headless from the job folder with an explicit model and effort. The `--effort` flag is documented for ultracode [N24]; use the same flag with `high` or `xhigh`, and confirm the accepted values with `claude --help` on your version (verify). Pass the pinned model ID with the model flag (verify the flag name and the full ID for your provider).
- **Per package (default).** Set `effortLevel` in the package's Claude Code settings [N25] so a forgotten flag never falls back to medium. `effortLevel` cannot hold `ultracode` [N25], which is the safety property we want.
- **Per environment.** `CLAUDE_CODE_EFFORT_LEVEL` [N25] may be set in the job runner; it also refuses `ultracode`.
- **Audit.** `examleaf-effort-governor` greps launch scripts and job logs for `ultracode` and fails the job if found (#3, #4).

### 7.4 Example package settings [Recommendation; key names other than `effortLevel` must be verified against current Claude Code documentation]

```json
{
  "model": "<pinned full Opus 5.5 model ID — verify for your provider>",
  "effortLevel": "high",
  "permissions": {
    "allow": [
      "Read(./**)",
      "Edit(./scenes/**)",
      "Edit(./tools/**)",
      "Edit(./logs/**)",
      "Bash(node ./tools/lint_seek_contract.js:*)",
      "Bash(python3 ./tools/determinism_hash_check.py:*)",
      "Bash(ffprobe:*)"
    ],
    "deny": [
      "Read(../**)",
      "Read(~/**)",
      "Edit(./fixtures/**)",
      "Edit(./cues/**)",
      "Edit(./style/**)",
      "Edit(./contract/**)",
      "Edit(./storyboard/**)",
      "Edit(./brief.md)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Bash(npm install:*)",
      "Bash(npx:*)",
      "Bash(pip install:*)",
      "WebFetch",
      "WebSearch"
    ]
  }
}
```

Why each deny exists: `Read(../**)` and `Read(~/**)` enforce "do not inspect other folders" (#9, [V3]). *15 Oct 2026 (audit science-safety-10):* because of that deny, the brief's required reads (style guide, `style_tokens.json`, `contract.md`, safe-zone tokens, linter) are **never** read from their original paths: the runner stages hashed copies into `style/`, `contract/` and `tools/` inside the job folder (§8.1, §8.2 rule 1) and the brief points at those copies. `Edit(./storyboard/**)` (audit M10) keeps the storyboard approval record out of the agent's reach: it is written only by the RD-17 approval service and verified by the runner (RD-46); `Edit(./style/**)` and `Edit(./contract/**)` keep the staged copies read-only. Claude Code applies `Edit(...)` rules to its file-writing tools; Bash writes are separately limited by the Bash allow list (verify both on the installed version, V12); `Edit(./fixtures/**)` and `Edit(./cues/**)` make fixtures and timings read-only (accuracy invariant, #12, #63); `Edit(./brief.md)` keeps the brief immutable during the job; network and install denials keep the agent from researching facts (#12) or pulling unreviewed packages (§5). The permission-rule syntax shown is the common Claude Code pattern; **verify** it against your installed version, and test that a denied read is actually refused before the first real job.

### 7.5 Logging per run

Record in `logs/run.json` for every Claude Code invocation: Claude Code version, pinned model ID, requested effort, **effective** effort (#2), start/end time, tokens in/out (from the session's usage reporting or headless JSON output; field names: verify), fix-loop count, exit status. `examleaf-effort-governor` forwards this to `examleaf-observability-cost`.

---

## 8. Workspace layout and isolation

### 8.1 One folder per job

[Recommendation, from [V1] "a folder for each run" and [V2] "keep the model contained inside a workspace"]

```text
anim_jobs/<lesson_id>/<job_id>/            ← Claude Code is launched HERE and nowhere else
├── brief.md                 immutable for the job; hash recorded (doc 02)
├── brief.sha256
├── .claude/settings.json    model, effortLevel, permissions (§7.4)
├── CLAUDE.md                job rules: read only this folder; never write narration text; never research facts;
│                            stop after N fix loops; output format (doc 02 §3.17)
├── fixtures/                READ-ONLY copies of validated data staged from
│                            lessons/<…>/science/verified-model.json (+ SHA-256 manifest)
├── cues/                    READ-ONLY cue_sheet.json per scene (doc 04 §4) built from lessons/<…>/audio/alignment.json
├── style/                   READ-ONLY copy of the selected 05_style_guides/<style>.md + style_tokens.json (+ MANIFEST.sha256)
├── contract/                READ-ONLY copies of 04_harness_contract/contract.md + vertical_safe_zones.tokens.json
│                            (+ MANIFEST.sha256); added 15 Oct 2026 so the brief's reads stay inside the folder
├── storyboard/              approval_record.json from the RD-17 service; agent may read, never edit (Edit-denied)
├── reference/               reference_analysis.json + stills (never the reference video itself unless licensed)
├── assets/                  approved raster assets (cutouts, textures) with AssetManifest entries; fonts/
├── tools/                   pinned harness: scene_template.html, lint_seek_contract.js,
│                            determinism_hash_check.py, frame converters, vendored three.js/GSAP builds
├── scenes/                  the ONLY place scene code is written (one file or folder per scene_id)
├── renders/                 preview and candidate renders, frames, hashes
└── logs/                    run.json per invocation, lint output, determinism reports, fix-loop notes
```

### 8.2 Rules

1. **Stage, then lock.** A job runner copies fixtures, cues, style files, assets and tools into the job folder, writes SHA-256 manifests, and makes `fixtures/`, `cues/`, `style/`, `reference/` and `brief.md` read-only at the filesystem level as well as in permissions.
2. **Launch from the job folder.** Claude Code's working directory is the job folder. Do not use `--add-dir`-style options to widen access (verify option names; the point is: grant no extra directories).
3. **Prompt rule as well as permission rule.** The brief and `CLAUDE.md` both state "Do not read, list or search any folder outside this job folder" ([V3]: "do not inspect any of my older projects or folders"). Permissions are the enforcement; the prompt reduces wasted attempts.
4. **No sibling jobs in view.** Keep `anim_jobs/` outside the engine and narration package roots so a job never sees other lessons or the skills library.
5. **Headless terminal.** Run jobs in the terminal (not the desktop app) so job logs are files and chat history does not fill up ([V1]).
6. **Results flow back by copy.** Approved scene code, renders and logs are copied back into `lessons/<…>/scenes/` and `lessons/<…>/render/` by the job runner, with hashes, never by the agent.
7. **Concurrency.** Start with two to four concurrent jobs, isolated, with clear file ownership (`07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §3). Never let two agents edit the same harness contract.

---

## 9. The preflight script

`12_advanced_animations_with_claude/04_harness_contract/preflight.sh` checks a machine before any job. Run it on the authoring workstation and on the render box as `bash preflight.sh --dir <frames dir> --workspace <job folder>`; save its output in `logs/preflight.txt` and in `ledgers/environment.md` for the render box. The script file is authoritative.

*Relabelled 15 Oct 2026 (audit M11): the table now says which checks the script actually performs ("implemented") and which are still only proposed. Earlier text credited preflight with all of them.*

| Check | Pass condition | Edge case | Status |
|---|---|---|---|
| Node version | major ≥ 22 | #22 [N8] | **implemented** |
| npx | present (WARN if not) | — | **implemented** |
| FFmpeg and ffprobe present | both print a version | #22 [N8] | **implemented** |
| Chrome/Chromium | found on PATH or via `CHROME` (executable) | #21 [N17] | **implemented** (version not printed) |
| Python | `python3` ≥ 3.11 | — | **implemented** (does not check the venv pin) |
| Fonts | at least one installed face covers U+0915, U+0995 and U+09F0 (`fc-list`) | #55 | **implemented** (coverage only); font-ledger hashes and the test card are **proposed** |
| Disk space | free space at `--dir` | — | **implemented** |
| Skills visibility | if `.agents/skills` exists, `.claude/skills` exists and is a symlink | #26 [N67] | **implemented** |
| Secrets | no `sk-ant-…`, `AKIA…`, `BEGIN … PRIVATE KEY`, `api_key=…` strings in the job folder (file names reported, never the match) | #40 [N19] | **implemented 15 Oct 2026** (needs `--workspace`); provider-key environment variables: **proposed** |
| Effort configuration | no ultracode effort in a flag, `EFFORT_LEVEL=` variable or `"effortLevel"` setting in the job folder | #3, #4 | **implemented 15 Oct 2026** (needs `--workspace`); "`effortLevel` set and not empty": **proposed** (the governor sets it per run) |
| Model pinning | no unversioned `claude-opus`/`claude-sonnet`/`claude-haiku`, no bare `"model": "opus"` or `--model opus` in the job folder | #6 [N28] | **implemented 15 Oct 2026** (needs `--workspace`) |
| Manim variant | `manim --version` reports Community Edition; no `manimgl` importable in the same environment | #28 [N48] | **proposed** |
| Repository weight | warn if the package exceeds 100 MB when a Codex archive is planned | #24 [N12] | **proposed** |
| Render box only | no outbound network after staging (operator-confirmed); GPU/driver or software-GL policy recorded | #65 | **proposed** (operator checklist) |

---

## 10. Verification checklist (expected outputs)

Tick each item and paste the output into the setup log.

| # | Step | Expected output | If it fails |
|---|---|---|---|
| V1 | `node --version` | `v22.…` or higher | Install Node 22+ (#22) |
| V2 | `ffmpeg -version` and `ffprobe -version` | One version line each | Install FFmpeg; Homebrew's includes ffprobe |
| V3 | `"$CHROME" --version` (or autodetect) | A Chrome/Chromium version line | Set `CHROME=/path` [N17] (#21) |
| V4 | `python3 --version` | `Python 3.11+` (3.13 on the render box) | Install per existing setup |
| V5 | `manim --version` [N46] | A Manim Community version line | Wrong package or GL installed (#28) |
| V6 | `ls -la .claude/skills` in each package | Lists only admitted skills; in the Remotion benchmark package it is a symlink to `.agents/skills` | Fix the link (§4.2 step 5) (#26) |
| V7 | Claude Code skill listing in the package | Admitted skills visible; nothing unreviewed | Remove unreviewed folders |
| V8 | `bash 12_advanced_animations_with_claude/04_harness_contract/preflight.sh` | All checks PASS (warnings explained in the log) | Fix each failing line |
| V9 | Font test card render (§3.3) | No tofu, no dotted circles; native editor sign-off | Change font or animate per word (#55) |
| V10 | Reference scene rendered twice at 1080×1920, 30 fps | `determinism_hash_check.py` reports identical frame hashes | See doc 04 §13 (#15–#19). Minimal frame capture for this gate is below the table |
| V11 | Same reference scene rendered with frames in reverse order | Hashes identical to forward render | Hidden state or stateful RNG (#17) |
| V12 | A denied read (`../`) attempted in a test job | Claude Code refuses | Fix permissions (#9) |
| V13 | A test launch script containing an ultracode effort flag, placed in a scratch job folder | `preflight.sh --workspace <scratch job>` FAILs on "ultracode scan" (implemented 15 Oct 2026), and `effort_policy.py plan --effort ultracode` refuses | Fix the audit (#3) |
| V14 | Test job with effort unset at the CLI | Package `effortLevel` applies; log shows the effective level | Set `effortLevel` (#1) |
| V15 | `ledgers/skill_activations.md` and `ledgers/licences.md` | Rows for every admitted skill, harness and font | Complete admission (§5) |

**Minimal frame capture for V10/V11 (added 15 Oct 2026; [verify] — the flags are standard headless-Chrome usage but are not in this project's evidence, and `--screenshot` is not a BeginFrame harness; contract.md §11 item 5).** The template accepts `?t=SECONDS` for one seek. Serve the scene over local HTTP (a `file://` page cannot fetch the cue sheet, contract.md §8), capture each frame by time, then compare:

```sh
# terminal 1, in the scene folder:  python3 -m http.server 8765 --bind 127.0.0.1
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cap() {  # cap OUT_DIR FRAME_INDEX...
  mkdir -p "$1"; d="$1"; shift
  for i in "$@"; do
    t=$(python3 -c "print($i/30)")
    "$CHROME" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1920 \
      --virtual-time-budget=10000 --screenshot="$d/f_$(printf %05d "$i").png" \
      "http://127.0.0.1:8765/scene.html?cues=cue_sheet.json&t=$t"
  done
}
cap frames_A 0 15 30 60 90                 # forward order
cap frames_B 90 60 30 15 0                 # reverse order (V11 / AD-21)
python3 -B -I 12_advanced_animations_with_claude/04_harness_contract/determinism_hash_check.py frames_A frames_B
```

Exit 0 means every captured frame is byte-identical. This proves the scene, not the production harness; HyperFrames' own render remains the gate once installed.

**Gate S-ANIM (proposed):** V1–V15 pass on the authoring workstation; V1–V5, V8–V11 pass on the render box; outputs recorded. This gate sits beside the existing S-GATE in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §1.

---

## 11. Troubleshooting

| Symptom | Likely cause | Fix | Edge case |
|---|---|---|---|
| Scenes look generic and flat | Effort silently medium; L1-style prompt | Set effort; use the full brief | #1, #7 |
| `xhigh` runs look like `high` | Silent fallback on an older model | Check the effective level in the log; pin the model ID | #2, #6 |
| Token use far above estimate | Thinking cannot be disabled; long prompts; ultracode | Lower effort for clerical tasks; split files; check for ultracode | #5, #3, #58 |
| Renderer will not start | Chrome not found | `CHROME=/path` | #21 |
| HyperFrames fails at install or render | Node < 22 or no FFmpeg | Preflight | #22 |
| Clone takes forever | LFS payloads | `GIT_LFS_SKIP_SMUDGE=1` | #23 |
| Codex build fails | Archive over 100 MB | Exclude media | #24 |
| Agent uses old Remotion APIs | Skills and packages out of sync | `/remotion-upgrade` before the benchmark | #25 |
| Remotion skills not visible to Claude | Missing or blocked symlink | §4.2 step 5 | #26 |
| Manim import errors | CE and GL mixed | One environment, CE only | #28 |
| Manim install fails on ARM Mac | Trying to install GL | Do not install GL | #29 |
| Out-of-memory during Manim tests | Too many workers | 4–6 workers | #30 |
| Tofu boxes or broken conjuncts | Font lacks the script; per-code-point animation | Noto-class fonts; per-word animation | #55 |
| Three.js frames differ between machines | GPU/driver variance | Single render box; per-box baseline | #65 |
| Agent copied a style from another project | Context contamination | Permissions + prompt rule | #9 |
| Plugin behaves oddly with another model | Untested combination | Test before switching | #62 |
