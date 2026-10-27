# 12 · Edge cases: master table

**Purpose.** One table of every known failure mode of the advanced-animation layer: all 65 edge cases from report §8 (master numbers #1–#65, unchanged) plus further cases justified from the project documents and sources (NEW-1 onward). Each row gives the symptom, cause, prevention or fix, the detection test, the owning skill and the source.

**Status.** [PROPOSED] prevention and detection. Sources as in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md` (§8 is the origin of #1–#65); [Recommendation]/[Hypothesis] mark design judgement. Check IDs (A1–A17, H-SB, H-RV, GF, GS) refer to `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`.

**Skill paths.** New skills live in `12_advanced_animations_with_claude/03_skills/<name>/`; existing ones in `06_skills_library/custom_skills/video_engine/<name>/` or `06_skills_library/custom_skills/narration/<name>/`. The `examleaf-` prefix is kept in the table. Harness files: `12_advanced_animations_with_claude/04_harness_contract/`.

**How to use.** Search by number from any document. When a new failure is found in the pilot, add a NEW-# row here first, then reference it elsewhere.

---

## Part 1 · The 65 master edge cases, grouped by phase

### 1.1 Model, effort and cost governance

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 1 | Silent medium effort | Mediocre, generic scenes | Opus/Sonnet/Haiku 5.5 default to medium | Pass effort explicitly per run (doc 09 §4) | A17a governor audit: `effort_requested` present | examleaf-effort-governor | [N22] |
| 2 | Requested level unsupported | xhigh behaves like high | Silent fallback to the highest supported level | Log effective model and level; pin model IDs | A17a: `effort_effective` ≠ requested → block | examleaf-effort-governor | [N23] |
| 3 | Ultracode runaway | Millions of tokens, usage windows exhausted, job unfinished | Multi-agent reviews, separate caches, fresh restarts | Banned in production and unattended runs; the only exception is the single attended, founder-approved, provider-capped $50 ceiling probe (13 D-9 / RD-48); never a default; AD-02/AD-11/AD-24 scoped to the strong-model phase (updated 15 Oct 2026) | Job-script grep for `ultracode`; ledger `ultracode: true` blocks | examleaf-effort-governor | [V1], [N24] |
| 4 | Ultracode set as default | Cannot happen via settings | Not accepted by `effortLevel` or `CLAUDE_CODE_EFFORT_LEVEL` | Launch flag is the only path; audit job scripts | Same grep before each batch | examleaf-effort-governor | [N25] |
| 5 | Thinking cost cannot be zeroed | Higher token use than expected | Thinking cannot be disabled on 5.5 or Fable models | Budget for it; lower effort and cheaper models for clerical tasks | Ledger tokens vs estimate | examleaf-effort-governor | [N26] |
| 6 | Alias drift | Different output across providers | Alias resolves to an older model elsewhere | Pin full model IDs | Job-script grep for bare aliases; ledger `alias_used` | examleaf-effort-governor | [N28] |
| 57 | Fable 5.5 assumptions | Plans built on an unreleased model | Leak hype | Model-agnostic harness; re-run QA before any model switch | Change-control review | examleaf-effort-governor | [V5] |
| 58 | Context/output limits change | Truncated long scene files | Limits quoted as of an article date | Recheck the catalogue; split scene files | Lint: file size; incomplete-file check (contract lint fails) | examleaf-effort-governor | [N73] |
| 59 | Release-date claims | Wrong compatibility assumptions | Unsourced article | Verify with Anthropic | Vendor-question log (report §11) | examleaf-effort-governor | [N59] |
| 60 | "Don't stop until perfect" | Endless loops and cost | Unbounded instruction | Max 3 creative rounds + 2 failed repairs; rubric stop | Ledger `round` > cap → stop | examleaf-effort-governor, examleaf-anim-brief | [V2], [V1] |
| 61 | Haiku long prompts | Higher per-token cost | Prompts > 100K tokens | Keep Haiku prompts short | Ledger `tokens_input` > 100K on Haiku → alert | examleaf-effort-governor | [N28] |
| 62 | Plugin with another model | Unknown behaviour | Untested claim of multi-model support | Test before switching models | Pilot re-run on the new model | examleaf-skills-security, examleaf-effort-governor (the governor lists #62 since 15 Oct 2026) | [N21] |

### 1.2 Brief, script and content

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 7 | One-line prompt | Random quality | L1 prompting | Structured brief plus reference or style guide | Brief completeness check (required fields) | examleaf-anim-brief | [V2] |
| 8 | Generic look | Same fonts and palettes everywhere | Safe defaults; convergence | Name or ban fonts; brand and style tokens | H-RV rubric R7; font-usage report across scenes | examleaf-anim-brief, examleaf-style-guides | [N50][N51][N55] |
| 9 | Context contamination | Copies old projects | Agent reads sibling folders | "Do not inspect other folders"; one isolated workspace per job | Session file-access log review | examleaf-anim-brief | [V3], [V2] |
| 11 | Weak script | Dull narration | Agent-written script | Script only from the narration system (GA-approved) | Diff script used vs approved script | examleaf-anim-brief | [V3] |
| 12 | Hallucinated facts on screen | Wrong numbers or labels | Agent "researches" itself | On-screen facts only from validated fixtures; science review | A7 text diff; A12 science-frame QA | examleaf-anim-brief, examleaf-anim-qa | [V3], [Recommendation] |
| 52 | Photoreal request | Uncanny or failed output | Opus is not a cinematic text-to-video model | Route to video generators or redesign as designed motion | Route review at H-SB | examleaf-storyboard-route | [N62] |
| 53 | Parser expects a fenced html block | Helper error | Strict output format in a helper | Enforce the output format in the brief | Harness intake validation | examleaf-anim-brief, examleaf-motion-harness (both list #53 in their edge-case tables since 15 Oct 2026) | [N56] (contested) |

### 1.3 Storyboard, MCP and credits

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 40 | Keys leaked into the repo | Secret exposure | Keys in the project or prompts | Environment or user config outside the repo only | Secret scan before commit/batch | examleaf-mcp-orchestrator | [N19] |
| 41 | MCP credits on any plan | Unexpected spend | Agent generations always billed | Ledger reservation and estimate before each call | Unreserved job → block | examleaf-mcp-orchestrator, examleaf-anim-storyboard-gate | [N33] |
| 42 | No credit cap | Runaway generation | Prompt limits aren't hard limits | Pipeline-enforced cap (`BudgetLedger`) | Ledger refuses over-cap reservation | examleaf-mcp-orchestrator, examleaf-anim-storyboard-gate | [N34] |
| 43 | Late results | Agent thinks a job failed and retries | Delivery up to about 60 s | Wait, then check usage; idempotent job IDs; never resubmit an unknown job | `ProviderJob` state `unknown` must be reconciled | examleaf-mcp-orchestrator | [N35] |
| 44 | Throttling | Batch stalls | Peak-time limits | Off-peak batches; retry with backoff | Job latency alert | examleaf-mcp-orchestrator | [N80] |
| 45 | Starter plan exhausted | Pipeline halts mid-lesson | 200 credits; premium models 40–70 credits each | Avoid premium video; size the plan | Credits remaining vs estimate | examleaf-mcp-orchestrator, examleaf-anim-storyboard-gate | [N76][N77] |
| 46 | Audio missing in ChatGPT | No Higgsfield audio | Platform limitation | Use the CLI agent or claude.ai | n/a (not ExamLeaf's voice path) | examleaf-mcp-orchestrator | [N32] |
| 47 | Skipped review gate | Credits wasted on rejected visuals | No checkpoint | Mandatory storyboard approval H-SB | Asset jobs require an H-SB approval ID | examleaf-anim-storyboard-gate | [V4] |
| 48 | Character drift | Hero looks different per shot | Independent generations | Pass the reference image; pose variants | H-RV visual review | examleaf-anim-storyboard-gate | [V4-MP] |
| 54 | Image model draws text or formulas | Misspelled labels, wrong equations | Raster generation | Build all text in code | A7 OCR on generated assets must return no text | examleaf-style-guides, examleaf-anim-qa | [V4-MP], [Recommendation] |

### 1.4 Harness, rendering and environment

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 14 | Expecting an MP4 from the model | No video | Text-only model output | A renderer executes the code | Pipeline design | examleaf-motion-harness | [N71] |
| 15 | Wall-clock animation | Frozen or garbled frames | Renderer seeks; never plays | Pure function of `t` | A1 lint (`Date.now`, timers) | examleaf-motion-harness, examleaf-threejs-scenes | [N68][N18] |
| 16 | Missing seek contract | Render fails or wrong length | No `DURATION` or `seek` | Contract lint before render | A1 lint; A11 frame count | examleaf-motion-harness | [N72] |
| 17 | Unseeded randomness | Frames differ between renders | `Math.random` | Seeded PRNG; double-render hash | A1 lint; A3 hash | examleaf-motion-harness, examleaf-procedural-2d, examleaf-threejs-scenes, examleaf-anim-qa | [N61] |
| 18 | Infinite repeats | Seeking yields inconsistent states | Unbounded tweens | Finite repeats; seekable timeline | A1 lint (`repeat: -1`) | examleaf-motion-harness, examleaf-procedural-2d | [V4-MP] |
| 19 | rAF polling | Render hangs | rAF doesn't fire in BeginFrame mode | `setTimeout` polling with a deadline | A1 lint; render watchdog | examleaf-motion-harness | [N69] |
| 20 | Multiple video elements | Decoder errors, black frames | Parallel seeking exhausts decoders | One worker for video-heavy scenes | A15 empty frames; worker config check | examleaf-motion-harness, examleaf-web-composition | [N70] |
| 21 | Chrome not found | Renderer won't start | Autodetect failed | Set `CHROME=/path` | A2 preflight | examleaf-motion-harness | [N17] |
| 22 | Old Node / no FFmpeg | HyperFrames fails | Requirements unmet | Preflight: Node 22+, FFmpeg | A2 preflight | examleaf-motion-harness | [N8] |
| 23 | Heavy clone | Slow or failing checkout | LFS payloads | `GIT_LFS_SKIP_SMUDGE=1` | Setup log | examleaf-motion-harness | [N13] |
| 24 | Archive too big | Codex build fails | Over 100 MB upload limit | Trim assets | Archive size check | examleaf-motion-harness | [N12] |
| 64 | Composition-wide time fx (shake, push-in) | Diagrams misread | Camera moves distort geometry | No camera fx during measurement or label reveals | A14 camera-fx guard | examleaf-procedural-2d, examleaf-threejs-scenes | [Recommendation] |
| 65 | Headless WebGL variance | 3D frames differ by machine | GPU/driver differences | Fixed render box; software-GL fallback test | A3 cross-box tolerance compare | examleaf-motion-harness, examleaf-threejs-scenes | [Hypothesis] |

### 1.5 Packages and skills

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 25 | Skill/package version drift | Agent uses stale APIs | Unsynced upgrades | `/remotion-upgrade` before the benchmark; pin versions | Version manifest diff | examleaf-motion-harness, examleaf-skills-security | [N7] |
| 26 | Skills invisible to Claude | Skills not loaded | Missing `.claude/skills` symlink or existing folder | Check the symlink after install; handle Windows | Post-install listing check | examleaf-motion-harness, examleaf-skills-security | [N66][N67] |
| 27 | Update without add | Undefined behaviour | Not documented | Always `add` first | Install runbook check | examleaf-skills-security | [N65] |
| 28 | Manim framework mix | Import errors | CE and GL incompatible | Standardise on CE | Import lint; `manim --version` | examleaf-manim-scenes | [N48] |
| 29 | ManimGL on ARM Mac | Install failure | Missing cairo/pkg-config | `arch -arm64 brew install pkg-config cairo` (GL only; CE preferred) | Install log | examleaf-manim-scenes | [N47] |
| 30 | Manim parallel tests | Out of memory | Too many workers | 4–6 workers | Worker config check; memory monitor | examleaf-manim-scenes | [N49] |

### 1.6 Audio and sync

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 10 | Missing audio | Silent render | Harness doesn't add audio by default | Require music/SFX plan in the brief; mux narration | A11 `audio_present`; A9 | examleaf-audio-compose | [V3] |
| 13 | Model can't hear audio | Animation ignores the music | Text-only model | Provide analysis JSON and cue sheet (beats, energy, words) | Cue sheet present before authoring | examleaf-audio-analysis, examleaf-cue-sheet | [V1], [N71] |
| 31 | Stereo with `sparse=True` | librosa error | Multi-channel unsupported in sparse mode | Downmix or `sparse=False` | Unit test on stereo input | examleaf-audio-analysis | [N37] |
| 32 | Tempo is an array | Type errors downstream | ndarray return | `float(tempo[0])` | Type assertion | examleaf-audio-analysis | [N38] |
| 33 | Beats in frames | Sync off by a large factor | Default units are frames | `units='time'` | Beat interval sanity (≈ 60/BPM s) | examleaf-audio-analysis, examleaf-cue-sheet | [N39] |
| 34 | Silent or beatless audio | Empty beat list, 0 BPM | No onsets | Guard; fall back to a narration grid | Cue-sheet validator: empty `beats` needs a warning | examleaf-audio-analysis | [N41] |
| 35 | Resample drift | Cues slip over time | 22,050 Hz default in `librosa.load` | `sr=None`; one consistent rate | Analysis JSON records `sr`; drift test on a long file | examleaf-audio-analysis, examleaf-cue-sheet | [N81] |
| 36 | Bad librosa arguments | `ParameterError` | Missing `y`/onset or invalid `units` | Validate inputs | Unit tests | examleaf-audio-analysis | [N40] |
| 37 | Prior given | `start_bpm` ignored | API behaviour | Use one or the other | Log parameters used | examleaf-audio-analysis | [N36] |
| 38 | Variable tempo | Shape error | `bpm` shape ≠ onset envelope | Match shapes | Unit test | examleaf-audio-analysis | [N42] |
| 39 | Unnormalised audio | Loudness jumps between scenes | No processing by default | Final loudnorm to the house target (−16 LUFS, −1 dBTP; Reels per the AD-04 test) | A9 on final mux | examleaf-audio-compose, examleaf-anim-qa, examleaf-audio-production-engineer | [N20], [V4-MP] |
| 63 | TTS regenerated | Reveals out of sync | Timings changed | Cue-sheet-driven code; re-align and rebuild | A10 staleness hash; A1 no hard-coded times | examleaf-cue-sheet, examleaf-kinetic-typography | [V4-MP], [Recommendation] |

### 1.7 Layout, typography and accessibility

| # | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source |
|---|---|---|---|---|---|---|---|
| 49 | 16:9 guide in a 9:16 pipeline | Cramped or cropped compositions | Style-guide aspect | Vertical re-layout rules | A4; H-RV R10 | examleaf-vertical-adapt, examleaf-style-guides | [V4-MP], [Recommendation] |
| 50 | Short headline hold | Unreadable text | Fast transitions | ≥ 1.2 s, longer for Hindi; equation and transform holds | A5 hold-time | examleaf-kinetic-typography, examleaf-anim-qa, examleaf-anim-brief | [N60] |
| 51 | Platform UI overlap | Captions or text hidden by app chrome | Unsafe placement | Safe-zone tokens; QA overlay | A4 safe-zone | examleaf-vertical-adapt, examleaf-anim-qa | [Recommendation] |
| 55 | Indic glyph gaps | Tofu boxes, broken conjuncts | Font lacks the script; per-code-point animation | Noto-class fonts; per-word animation | A8a coverage; A8b shaping test card | examleaf-kinetic-typography, examleaf-style-guides | [Hypothesis] |
| 56 | Photosensitive flashes | Viewer discomfort | Rapid luminance changes | Flash ban in QA | A6 luminance series | examleaf-anim-qa, examleaf-style-guides | [V1], [Recommendation] |

**Coverage check:** 12 + 7 + 10 + 13 + 6 + 12 + 5 = 65 rows; every master number #1–#65 appears exactly once.

---

## Part 2 · Additional edge cases (NEW-#)

Each is justified from a source or project document, or labelled [Hypothesis].

### 2.1 Layout, typography and text

| ID | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source / justification |
|---|---|---|---|---|---|---|---|
| NEW-1 | Caption burn-in collision | Burned-in captions overlap kinetic text, diagram parts or platform UI | Captions placed without the reserve; expressive text drifts into the caption band | Captions only inside the protected reserve; kinetic text never enters it; same text as sidecar | A4 overlay including caption boxes | examleaf-vertical-adapt, examleaf-kinetic-typography | Protected caption area (`02_learning_psychology/INSTRUCTIONS_production_rules.md` D7; 03 S8 tokens ≈ 190 px reserve) |
| NEW-2 | Font licence missing or unsuitable | Brand cannot use the video commercially; takedown risk | Font downloaded "free" without checking licence terms for embedding/video | Licence recorded per font in the asset ledger; vendor only cleared fonts | A16 provenance | examleaf-style-guides, examleaf-asset-library | RD-23: "licence recorded"; "Licences are tracked by component" (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14) |
| NEW-3 | Emoji and pictographic glyphs | Missing or differently drawn symbols on the render box | Colour-emoji font absent or platform-specific | Use drawn SVG icons; ban emoji in scene text | A8a coverage (flags emoji code points) | examleaf-kinetic-typography | [Hypothesis]; same mechanism as #55 |
| NEW-16 | System or network font fallback | Different glyph widths, broken layout, non-deterministic frames | Font not loaded before first seek; remote font fails | Vendor fonts; wait for font load; fail render on load error | A2 preflight; A3 hash; A1 no network fetch | examleaf-motion-harness, examleaf-kinetic-typography | "No uncontrolled network fonts" (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14) |
| NEW-17 | Text drawn into canvas/WebGL or rasters | DOM text-dump QA cannot see it | Labels baked into textures or clips | Labels in SVG/DOM overlay; symbol manifests for Manim; OCR/human fallback | A7 reports elements with no DOM text but text-like pixels | examleaf-threejs-scenes, examleaf-manim-scenes, examleaf-anim-qa | Accuracy invariant (report §9) |
| NEW-18 | Grapheme segmentation differs by Chrome/ICU version | Indic cluster animation breaks after a browser update | Segmentation rules and data change across Unicode versions | Whole-word mask by default; re-run the test card on every Chrome update | A8b test card | examleaf-kinetic-typography | [Hypothesis]; report §11 item 10 |
| NEW-19 | Equation typography mismatch across layers | KaTeX equations in the composition look different from Manim equations | Different math fonts | One math typeface per lesson; visual check | H-RV R7 | examleaf-manim-scenes, examleaf-web-composition | RD-23 (KaTeX fonts); `examleaf-manim-scenes` "LaTeX as needed" |
| NEW-27 | Safe-zone tokens unmeasured or stale | Text hidden by Reels/Shorts UI after an app update | Platform insets not verified; UI changes | Measure per platform; store `measured_on`; re-measure periodically | A4 warns on missing/stale date | examleaf-vertical-adapt | Report §7.9, §11 item 9; playbook marks safe-zone specs unverified |
| NEW-30 | Numeral system inconsistent | Mixed Devanagari and Western digits; decimal convention differs from the textbook | Localisation without a rule | Fixture records the edition's numeral convention | A7 text diff against fixture | examleaf-kinetic-typography, examleaf-alignment-localize | [Recommendation]; textbook-edition binding in 03 S0–S2 |
| NEW-31 | Style palette fails contrast | Collage or doodle text unreadable | Style palettes not validated against WCAG thresholds | Validate every style token pair on real frames | A13 | examleaf-style-guides | WCAG thresholds (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §3); RD-27 pattern (unvalidated accents not used) |

### 2.2 Audio

| ID | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source / justification |
|---|---|---|---|---|---|---|---|
| NEW-4 | Sample-rate mismatch (44.1 vs 48 kHz) | Audio runs ≈ 8.8 % fast or slow, or drifts against cues | A 44.1 kHz file treated as 48 kHz, or mixed rates | Resample once on import; everything 48 kHz; record `sr` | Probe sample rate of every input; A10 drift check | examleaf-audio-compose, examleaf-audio-production-engineer | Providers return 24/44.1 kHz; polyphase to 48 kHz (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12) |
| NEW-9 | Music under core explanation | Listening effort rises; violates house rule | Bed rendered across the whole scene | `core_explanation` segments block music | A9 music-stem RMS in those windows | examleaf-audio-compose | `background_music_in_core_explanation: false` (`02_learning_psychology/palette_and_typography_tokens.json`) |
| NEW-10 | Ducking pumping or non-deterministic sidechain | Audible pumping; mix differs between renders | Signal-driven compressor | Gain automation from timeline clip intervals | A3-style hash of the mix; listening | examleaf-audio-compose | [Recommendation]; playbook ducking values [Hypothesis] |
| NEW-11 | SFX implies wrong science | A "spark" on a safe low-voltage circuit; mains hum in a DC lesson | Decorative sound chosen for effect | Science review of SFX on data-bound scenes | H-RV R1; GA of planned visuals | examleaf-audio-compose | Report §7.13 (decoration must not contradict science) |
| NEW-14 | Encoder priming delay offsets audio | Audio starts slightly late versus video | Lossy audio encoder delay in the delivery file [Hypothesis] | Measure offset after mux; correct in mux step | A10 A/V offset measurement | examleaf-audio-caption-qa | [Hypothesis]; "measured again" after mux (04 §13) |

### 2.3 Rendering, colour and files

| ID | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source / justification |
|---|---|---|---|---|---|---|---|
| NEW-5 | Colour space or range mismatch | Washed-out or over-dark palette; contrast changes after encode | RGB frames encoded with an inconsistent matrix or range, or converted to YUV more than once | Clips and stills sRGB 8-bit; convert RGB→YUV once at the final encode, tagged BT.709 with the correct range (options: verify) | A13 on decoded delivery frames vs source PNGs | examleaf-motion-harness, examleaf-render-batch | `12_advanced_animations_with_claude/04_harness_contract/import_clip_notes.md` §6.1; delivery h264/yuv420p (06 §2.2) |
| NEW-6 | Long-render parallelism exhausts memory | Crashes, killed workers, partial outputs | Too many browser or Manim workers; large instanced scenes | Bounded workers; memory-aware scheduling; record peak memory | Render manifest peak memory; A2 resource check | examleaf-render-batch, examleaf-motion-harness | [N49] (Manim OOM); [N70]; `costs.json` peak memory field (08 §3) |
| NEW-8 | Output file too large | Upload rejected or slow; storage cost | Uncontrolled bitrate; lossless intermediates shipped | Bitrate targets per platform (verify limits); intermediates never delivered | Size check against configured limit | examleaf-render-batch | [Hypothesis]; platform limits unverified (playbook "bitrate unverified") |
| NEW-12 | Encoder non-determinism changes the MP4 hash | Approval invalidated or cache miss although frames are identical | Container metadata or encoder threading varies | Hash PNG frames before encoding for determinism; bind approval to the delivered file hash | A3 on PNG frames (`determinism_hash_check.py`) | examleaf-motion-harness | Approvals bind to hashes (06 §5); [Recommendation] |
| NEW-13 | Frame-count rounding | Last word cut off or one extra frame; `duration × fps` not an integer | Duration taken from float audio length | Round duration up to a whole frame; validator | A11 exact frame count; cue-sheet validator | examleaf-cue-sheet, examleaf-motion-harness | [N72]; `SceneSpec` whole-frame rule (12 §3.4) |
| NEW-15 | Alpha lost in H.264 clip | Black box behind an overlay clip | H.264 yuv420p has no alpha | PNG sequence or alpha-capable intermediate for overlays | Composite check; A15 | examleaf-threejs-scenes, examleaf-manim-scenes | [Recommendation]; `examleaf-manim-scenes` "transparent or opaque insert" |
| NEW-20 | LaTeX toolchain missing for Manim | Equation objects fail to render | TeX distribution or package absent | Preflight checks TeX for routed Manim inserts | A2 | examleaf-manim-scenes | `examleaf-manim-scenes` dependency "LaTeX as needed" |
| NEW-21 | WebGL context loss | Black frames mid-render | GPU memory pressure or driver reset | Listen for context loss; fail loudly; bound GPU memory | A15; render log | examleaf-threejs-scenes | Report §10 item 8 ("WebGL context loss in headless mode") |
| NEW-22 | WebGL canvas captured blank | Empty frames although the scene renders on screen | Drawing buffer cleared before capture in some capture paths [Hypothesis] | Test `preserveDrawingBuffer`; capture right after render | A15 non-empty frames | examleaf-threejs-scenes | [Hypothesis] |
| NEW-23 | Sub-range seek depends on earlier state | A Reel cut from a lesson scene starts in the wrong state | Accumulated or lazily initialised state | Strict pure function of `t`; test random-order seeks | A1 runtime probe (seek order independence) | examleaf-motion-harness, examleaf-vertical-adapt | [N61] (contested); doc 11 §6 |
| NEW-33 | Frame pixels depend on seek-and-capture history (16 Oct 2026, pilot L-01, L-02) | Reverse-order or sampled re-render differs by a few LSBs (PSNR ≈ 45 dB) although DOM state is identical; concurrent renders mismatch on a few frames | Chrome 155/macOS raster-scale cache on CSS-`transform` layers; two renders sharing one machine | Define determinism as the identical in-order procedure (fresh page, every frame seeked and captured in order) and compare every frame hash; reveal headline/word text with `opacity` (and SVG/canvas positions) instead of `transform` scale; one render per machine at a time | A3 re-run of the identical procedure, every frame (`determinism_hash_check.py`); pilot MP4 SHA-256 matched across runs | examleaf-motion-harness | `16_pilot_builds_2026-10-16/COMPARISON_and_GAPS.md` §1 L-01, L-02; contract §2.2, §11 |
| NEW-28 | Decorative wobble on data-bound strokes | Slopes, angles or ratios visibly altered | Doodle boil applied to every stroke | Zero wobble amplitude on data-bound layers | A12 geometry check | examleaf-procedural-2d | Report §7.13; #64 family |

### 2.4 Assets, licensing and references

| ID | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source / justification |
|---|---|---|---|---|---|---|---|
| NEW-7 | Unlicensed asset (SFX sample, SoundFont, texture, mesh, HDRI) | Release blocked; legal exposure | Asset pulled without a licence record | Every asset in `AssetManifest` with licence and hash; quarantine unconfirmed rights | A16 | examleaf-asset-library | "Unlicensed asset" is Critical (06 §4); 03 S9 quarantine rule |
| NEW-24 | Variable-frame-rate or letterboxed reference | Wrong shot lengths and pacing numbers | Reference not normalised before analysis | Detect VFR and letterbox; normalise first | Reference-analyzer warnings | examleaf-reference-analyzer | Report §10 item 2 |
| NEW-25 | Copyrighted reference reused as an asset | Rights violation | Frames or audio from a reference copied into a video | References are analysis inputs only | A16; H-RV | examleaf-reference-analyzer, examleaf-asset-library | Report §10 item 2 |

### 2.5 Pacing and governance

| ID | Edge case | Symptom | Cause | Prevention / fix | Detection test | Owning skill | Source / justification |
|---|---|---|---|---|---|---|---|
| NEW-26 | Sub-agent logs missing token counts | Ledger under-reports cost | Agents end without final counts | Require counts from every run; mark missing as defect | A17b | examleaf-effort-governor | [V1] ("some agent logs are missing their final counts") |
| NEW-29 | Re-timing a Reel speeds narration | Rushed, unnatural speech; approval invalid | Narration stretched to fit a beat grid | Re-time only holds and decorative motion | A10 audio hash unchanged for reused segments | examleaf-vertical-adapt, examleaf-cue-sheet | Forbidden repair: "speeding audio to fit a slot" (03 S16) |
| NEW-32 | Mid-session model or effort change | Cache invalidated; cost jump | Switching model/effort inside one session | Separate sessions per model/effort | Ledger: one model and effort per session | examleaf-effort-governor | [CAPI] in doc 09 §1 (cache breakers on the API) |

---

## Part 3 · Index by owning skill

| Skill | Edge cases |
|---|---|
| examleaf-effort-governor | #1–#6, #57–#62, NEW-26, NEW-32 |
| examleaf-anim-brief | #7–#9, #11, #12, #50, #53, #60 |
| examleaf-style-guides | #8, #49, #54, #55, #56, NEW-2, NEW-31 |
| examleaf-anim-storyboard-gate | #41, #42, #45, #47, #48 |
| examleaf-mcp-orchestrator | #40–#46 |
| examleaf-motion-harness | #14–#26, #53, #65, NEW-5, NEW-6, NEW-12, NEW-13, NEW-16, NEW-23, NEW-33 |
| examleaf-procedural-2d | #17, #18, #64, NEW-28 |
| examleaf-kinetic-typography | #50, #55, #63, NEW-1, NEW-3, NEW-16, NEW-18, NEW-30 |
| examleaf-threejs-scenes | #15, #17, #64, #65, NEW-15, NEW-17, NEW-21, NEW-22 |
| examleaf-audio-compose | #10, #39, NEW-4, NEW-9, NEW-10, NEW-11 |
| examleaf-audio-analysis | #13, #31–#38 |
| examleaf-cue-sheet | #13, #33, #35, #63, NEW-13, NEW-29 |
| examleaf-anim-qa | #12, #17, #39, #50, #51, #54, #56, NEW-17 |
| examleaf-vertical-adapt | #49, #51, NEW-1, NEW-23, NEW-27, NEW-29 |
| examleaf-reference-analyzer | NEW-24, NEW-25 |
| Existing: examleaf-manim-scenes | #28–#30, NEW-15, NEW-17, NEW-19, NEW-20 |
| Existing: examleaf-skills-security | #25–#27, #62 |
| Existing: examleaf-storyboard-route | #52 |
| Existing: examleaf-asset-library | NEW-2, NEW-7, NEW-25 |
| Existing: examleaf-render-batch / examleaf-web-composition | #20, NEW-5, NEW-6, NEW-8, NEW-19 |
| Existing: examleaf-audio-production-engineer / examleaf-audio-caption-qa | #39, NEW-4, NEW-14 |
