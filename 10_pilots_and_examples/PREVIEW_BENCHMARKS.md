# PREVIEW_BENCHMARKS - render timings, measured media properties, tests and probes

Scope: the eight 30-second silent technical-preview MP4s (two per subject: 16:9 and 9:16), their contact sheets, sampled frames and QA files, all under `rendered_previews/`.

> **Read this first - what these numbers are.** The previews are **technical proofs, not finished ExamLeaf lessons and not evidence of production readiness** (message 10, section 'What was actually tested'). Every manifest says `release_status: blocked_pending_audio_and_expert_review` and `audio_status: intentionally_silent_technical_preview`. There is no narration, no teacher approval and no student-learning evaluation. The timings are **not** a forecast for a narrated ten-minute lesson, complex 3D, or a browser compositor (HyperFrames/Remotion were researched but not installed or benchmarked).

## Verified vs proposed (exactly as stated in the sources)

| Claim | Status | Basis |
|---|---|---|
| Four scientific models + visual templates; 8 real 30 s MP4s; 56 tests pass; local cache/hashes/atomic render/budget ledger | **Verified by ChatGPT in its sandbox** (implemented and tested); this folder re-verifies the media files only | message 10 table; `tests.txt`; `benchmark.json`. Tests were NOT re-run here (no package installs allowed). |
| MP4 properties (duration, frames, fps, resolution, codec) | **Re-verified here** by an independent parse of the copied files (section 3) | Python stdlib MP4 box parser + `file` + `mdls` + `stat` + `md5`/`shasum`; `ffprobe` is not installed on this machine. |
| Frame readability on small phones, layout overlaps | **Not verified** | `layout_qa` checks canvas bounds only on 10 sampled frames; contact sheets were inspected by eye only. |
| Browser playback of `preview.html` | **Not verified by ChatGPT** (`browser_smoke.json`: blocked by administrator policy). This folder only checks that every file the page references exists (via `preview_local.html`). | `browser_smoke.json` |
| Narration imported/synchronised into the videos | **Not completed** | `delivery_status.json` `voice_import_and_alignment: not_validated` |
| Four complete narrated ten-minute lessons | **Not completed** - four beat plans only (`blueprint_only`) | `delivery_status.json` `full_600s_narrated_lessons_completed: 0` |
| HyperFrames / Remotion / Manim / Blender execution | **Researched, not installed or benchmarked** | message 10 |
| Custom Skills evaluated through Claude Code/Codex | **Drafted, not agent-evaluated** | `agent_skill_evaluations_performed: 0` |
| Teacher approval / student learning evaluation | **Not performed** | `academic_approval: pending`, `student_learning_study: not_performed` |
| Production cost per video, human minutes, peak memory, accepted-asset attempts | **Not measured**; planning assumptions only (see `INSTRUCTIONS_running_the_four_pilots.md`) | `Four_Pilots.md`: 'Work/time planning, not measured' |

## 1. Render timing table (message 10, section 8.1) cross-checked against `benchmark.json`

Conditions stated in message 10 / `Four_Pilots.md`: each file is **30 seconds, 720 frames, 24 fps**, rendered at **1280x720** (16:9) or **720x1280** (9:16); **two jobs ran concurrently** (two workers), so the 'local job seconds' are wall times per job under concurrency, **not isolated single-worker performance**. Source fixtures are original examples based on cited OpenStax sections, not a conversion of ExamLeaf PDFs. Research/pricing checked 13 October 2026.

| Subject | Preview and checked model (message 10) | Landscape 16:9 render time (s) | Vertical 9:16 render time (s) | `benchmark.json` 16:9 | `benchmark.json` 9:16 | Match |
|---|---|---:|---:|---:|---:|---|
| Physics | RC charging: initial condition, one time constant, KVL, numerical/analytical agreement | **27.338** | **28.102** | 27.338 | 28.102 | yes |
| Chemistry | Atom balancing: specified molecular identities and atom counts | **28.670** | **29.375** | 28.670 | 29.375 | yes |
| Mathematics | Chain rule: symbolic and finite-difference check for (3x+1)^2 | **27.372** | **27.576** | 27.372 | 27.576 | yes |
| Biology | Monohybrid cross: probabilities and complete-dominance assumption | **27.425** | **27.951** | 27.425 | 27.951 | yes |

Derived arithmetic (not in the sources): min 27.338 s, max 29.375 s, mean 27.976 s per 30 s / 720-frame job under two-worker concurrency; every vertical render was slower than its landscape twin. `cache_hit` is `false` for all eight (first builds).

`Four_Pilots.md` records the same eight jobs with result `Passed; release blocked`.

Environment recorded in every manifest (ChatGPT's Linux sandbox, not this Mac): Python 3.13.5; Linux-6.18.44-x86_64-with-glibc2.41; ffmpeg version 7.1.5-0+deb13u1 Copyright (c) 2000-2026 the FFmpeg developers; packages numpy 2.3.5, scipy 1.17.0, sympy 1.14.0, pydantic 2.13.5, CairoSVG 2.8.2, Pillow 12.3.0, rdkit 2025.9.4; font sha256 `57f73e11f51999432bf7ab22ce55b6f945d5eca1bf824404cfa9ec2e3718c84e`. `invoice_cost_usd` = 0.0 for all eight: No external generation APIs invoked. Local execution was not separately invoiced or cloud-priced.

## 2. Per-file science checks, media QA and layout QA recorded in each manifest

| Scene | Science checks recorded (all `passed: true`) | Boundary stated |
|---|---|---|
| physics_rc | `initial_condition` (V_C(0)=0 for an initially uncharged capacitor); `one_time_constant` (V_C(tau)/V_s=1-exp(-1)); `numerical_ode_crosscheck` (max absolute voltage error 1.9e-10 V); `voltage_law` (V_s=IR+V_C); `monotonic_charge` (Charging is monotonic for the ideal model) | Checks cover the specified model only; they do not establish curriculum fit or expert approval. |
| chemistry_balance | `element_conservation` (reactants={'H': 4, 'O': 2}; products={'O': 2, 'H': 4}); `smallest_whole_numbers` (coefficients have greatest common divisor 1); `approved_formulas` (RDKit explicit-H atom count verifies H2O composition) | Checks cover the specified model only; they do not establish curriculum fit or expert approval. |
| mathematics_chain | `template_parameter_contract` (This visual template is the reviewed (3x+1)^2 fixture; build a new template for another expression); `symbolic_derivative` (18*x + 6); `finite_difference_crosscheck` (max finite-difference error 1.24e-10); `real_domain` (Polynomial and derivative valid for all real x) | Checks cover the specified model only; they do not establish curriculum fit or expert approval. |
| biology_genetics | `probability_normalization` ({'AA': Fraction(1, 4), 'Aa': Fraction(1, 2), 'aa': Fraction(1, 4)}); `genotype_ratio` (Expected 1:2:1 for Aa x Aa); `complete_dominance_phenotype` (3/4 dominant phenotype under complete dominance assumption); `no_small_sample_guarantee` (Probabilities are not guaranteed counts in four offspring) | Checks cover the specified model only; they do not establish curriculum fit or expert approval. |

Identical across all 8 manifests: `media_qa.passed = true` (checks: dimensions, duration, frame_count, codec, pixel_format; `audio_present = false`); `layout_qa.passed = true`, `sampled_frames = 10`, `issues = []`, with the stated boundary **'Canvas bounds only. Does not prove absence of all overlaps or mobile readability.'**; warnings: Not a full ten-minute pilot.; Academic correctness not signed off by a teacher.; Voice quality and alignment untested.; No student-learning study performed.

## 3. Media properties measured on the copies in this folder

**Method.** `ffprobe`/`ffmpeg` are not installed on this machine (`which ffprobe ffmpeg` returned nothing). Properties were therefore read with read-only tools that already exist: a small Python 3 standard-library ISO-BMFF (MP4) box parser (duration from `mvhd`/`mdhd`, frame count from `stts` and `stsz`, fps = media timescale / sample delta, resolution from `tkhd` and the `avc1` sample entry, profile/level from `avcC`, chroma format and bit depth from the SPS), plus `file`, `mdls` (Spotlight), `stat`, `md5` and `shasum -a 256`. Nothing was decoded or modified. Raw parser JSON is not kept in the project; the table below is the record.

| File | Bytes | Duration (s) | Frames (stts / stsz) | fps | Resolution (tkhd = avc1) | Codec | Profile / level | Chroma / bit depth | Tracks | Sync (key) frames | Avg video kbit/s (derived) | MD5 |
|---|---:|---:|---|---:|---|---|---|---|---|---:|---:|---|
| `physics_rc_16x9.mp4` | 347653 | 30.000 | 720 / 720 | 24 | 1280x720 = 1280x720 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 92.7 | `7b2fd6f7a11dceec8a454273d537608b` |
| `physics_rc_9x16.mp4` | 340225 | 30.000 | 720 / 720 | 24 | 720x1280 = 720x1280 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 90.7 | `4c86198d8e91046446cb79de4ae73052` |
| `chemistry_balance_16x9.mp4` | 212515 | 30.000 | 720 / 720 | 24 | 1280x720 = 1280x720 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 56.7 | `1924fa1ea73e9bdc10df7190164e3130` |
| `chemistry_balance_9x16.mp4` | 212760 | 30.000 | 720 / 720 | 24 | 720x1280 = 720x1280 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 56.7 | `dac03d782674ec4696b8b41dc50b33b4` |
| `mathematics_chain_16x9.mp4` | 225773 | 30.000 | 720 / 720 | 24 | 1280x720 = 1280x720 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 60.2 | `34989e90f8d6ba0f6e952a66da1a5ab8` |
| `mathematics_chain_9x16.mp4` | 222870 | 30.000 | 720 / 720 | 24 | 720x1280 = 720x1280 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 59.4 | `d73cba038680e248d4f548ae571aef32` |
| `biology_genetics_16x9.mp4` | 203333 | 30.000 | 720 / 720 | 24 | 1280x720 = 1280x720 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 54.2 | `8fef84fa05b649b4fd64d6db1ba0b632` |
| `biology_genetics_9x16.mp4` | 202027 | 30.000 | 720 / 720 | 24 | 720x1280 = 720x1280 | H.264 (`avc1`) | High (idc 100) / level 3.1 | chroma_format_idc 1 (4:2:0), 8-bit => yuv420p | 1 (`vide` only; no audio) | 3 | 53.9 | `fefef87df200cb5d2343efd336ac56ad` |

Container: `ftyp` brand `isom`; box order `ftyp, moov, free, mdat` (`moov` before `mdat`; `free` box present). `file` identifies every MP4 as: `ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]`. All 8 MP4s have `ctts` and the same box order; each has `ctts` (composition offsets, i.e. B-frames) and a 12288 Hz media timescale (24 fps = sample delta 512).

**Cross-checks.** (a) SHA-256 of every copied MP4 equals the `sha256` recorded in its manifest: all 8 equal. (b) `mdls` (independent tool): duration 30 s, H.264, and width x height matching the table for all 8 (`kMDItemTotalBitRate` values 51-90 as reported by Spotlight, roughly consistent with the derived averages above, which are file bytes x 8 / 30 s and include container overhead). (c) Everything matches the 'Each file is 30 seconds, 720 frames, 24 fps, rendered at 1280x720 or 720x1280' statement in message 10 and each manifest's `media_qa`.

`mdls` rows:

| File | mdls duration (s) | mdls width x height | mdls codec | mdls `TotalBitRate` (as reported) |
|---|---:|---|---|---:|
| `physics_rc_16x9.mp4` | 30 | 1280x720 | H.264 | 90 |
| `physics_rc_9x16.mp4` | 30 | 720x1280 | H.264 | 88 |
| `chemistry_balance_16x9.mp4` | 30 | 1280x720 | H.264 | 54 |
| `chemistry_balance_9x16.mp4` | 30 | 720x1280 | H.264 | 54 |
| `mathematics_chain_16x9.mp4` | 30 | 1280x720 | H.264 | 57 |
| `mathematics_chain_9x16.mp4` | 30 | 720x1280 | H.264 | 56 |
| `biology_genetics_16x9.mp4` | 30 | 1280x720 | H.264 | 51 |
| `biology_genetics_9x16.mp4` | 30 | 720x1280 | H.264 | 51 |

### 3.1 Contact sheets (JPG)

| File | Bytes | Dimensions (`file` / `sips`) | Format | MD5 | What it shows (viewed by eye) |
|---|---:|---|---|---|---|
| `technical_previews_contact_sheet.jpg` | 105919 | 1280x840 | baseline JPEG, 8-bit, 3 components, RGB (per `sips`), no alpha | `85506b4559c0d7e44f7aac7870e2c755` | 2x2 grid of the four landscape previews, one answer-state frame each: physics_rc, chemistry_balance, mathematics_chain, biology_genetics; each tile shows the ExamLeaf header, title, diagram, key numbers and caption, with the 'TECHNICAL PREVIEW - NO AUDIO - REVIEW PENDING' footer. |
| `vertical_review.jpg` | 63830 | 1080x680 | baseline JPEG, 8-bit, 3 components, RGB (per `sips`), no alpha | `fd4a0eca1b3fadeb5e5607803c7ca6c9` | Four vertical (9:16) previews side by side in the same subject order, stacked layout: title, diagram, concept card, caption; the lower part of the sheet (about 25%) is blank white. |

### 3.2 Sampled frames (PNG + SVG)

32 PNG + 32 SVG: four sampled states per video (`opening`, `question`, `answer`, `recap`) for each of the 8 videos. PNG dimensions measured with `sips`: 16 files at 1280x720, 16 files at 720x1280; every PNG matches its filename's aspect: yes. All PNGs are 8-bit RGB (`file`), non-interlaced. The SVGs are the vector sources of the same frames.

### 3.3 Captions (WebVTT) and logs

- 8 `.vtt` files, one per video, each with **5 cues** (0-6, 6-11, 11-16.5, 16.5-24, 24-30 s) whose start/end times and text were checked programmatically and equal the `cues[]` of the matching scene JSON in `../pilots/` (8 of 8 files match). (Both aspect ratios of a scene have identical captions.)
- 8 `*.ffmpeg.log` files: **all 0 bytes** (empty) in the delivered package, so they carry no encoder evidence.
- 8 `*.manifest.json`: verification manifest per video (sha256, cache_key, render_wall_seconds, science, media_qa, layout_qa, environment, warnings).

## 4. The six separately downloaded files vs the zip copies (`cmp`)

The ChatGPT transcript exposed `ExamLeaf_Engine_Implementation/outputs/` as a separate download with six files (four 16:9 MP4s, `technical_previews_contact_sheet.jpg`, `vertical_review.jpg`). Each was compared byte-for-byte (`cmp -s`) against (i) the same file read straight out of `downloads/ExamLeaf_Video_Engine_Implementation.zip` with `unzip -p`, (ii) the extracted copy under `00_source/extracted/`, and (iii) the copy placed in `rendered_previews/`.

| File | Bytes | MD5 | vs zip entry | vs extracted copy | vs `rendered_previews/` copy |
|---|---:|---|---|---|---|
| `physics_rc_16x9.mp4` | 347653 | `7b2fd6f7a11dceec8a454273d537608b` | IDENTICAL | IDENTICAL | IDENTICAL |
| `chemistry_balance_16x9.mp4` | 212515 | `1924fa1ea73e9bdc10df7190164e3130` | IDENTICAL | IDENTICAL | IDENTICAL |
| `mathematics_chain_16x9.mp4` | 225773 | `34989e90f8d6ba0f6e952a66da1a5ab8` | IDENTICAL | IDENTICAL | IDENTICAL |
| `biology_genetics_16x9.mp4` | 203333 | `8fef84fa05b649b4fd64d6db1ba0b632` | IDENTICAL | IDENTICAL | IDENTICAL |
| `technical_previews_contact_sheet.jpg` | 105919 | `85506b4559c0d7e44f7aac7870e2c755` | IDENTICAL | IDENTICAL | IDENTICAL |
| `vertical_review.jpg` | 63830 | `fd4a0eca1b3fadeb5e5607803c7ca6c9` | IDENTICAL | IDENTICAL | IDENTICAL |

Result: **all six identical to all three references.** The separate download adds no new content; the four vertical MP4s exist only in the zip/extracted outputs (the download offered landscape MP4s plus the two contact sheets).

## 5. Test results (`tests.txt`)

```text
........................................................                 [100%]
56 passed in 3.51s
```

**56 passed in 3.51 s** (ChatGPT's sandbox). Recorded in `delivery_status.json` as `unit_contract_media_tests_passed: 56`. The tests live in the implementation's `tests/` folder (not part of this section): `test_engine.py` (30 test functions), `test_interfaces.py` (4), `test_media_integration.py` (5) = 39 functions, which expand to 56 collected tests because `test_science` is parametrised over 4 subjects, `test_layout` over 4 subjects x 2 aspects and `test_actual_mp4` over 4 subjects x 2 aspects (39 + 3 + 7 + 7 = 56; this arithmetic is our reconciliation, not something the file states). Tests named in the files include `test_actual_mp4`, `test_real_cache_hit`, `test_actual_release_blocked`, `test_audio_mux_and_mismatch`, `test_voice_fail_closed`, `test_no_audio_no_release`, `test_plans_total_600` (the four 600 s plans must sum to 600 s), `test_vertical_not_crop`, `test_untrusted_molecule_rejected`. **We did not re-run them** (no package installs permitted; the reference environment is Linux).

The narration pack has its own `tests.txt` (`../narration_outputs/tests.txt`): **57 passed in 3.17 s**.

## 6. `live_speech_probe.json` findings

| Field | Value |
|---|---|
| `status` | provider_returned_audio |
| `provider_surface` | connected Runway tool |
| `task_id` | 2cf16161-f661-430f-a80d-a70908c1b972 |
| `model` | eleven_multilingual_v2 |
| `voice` | Arjun |
| `language` | en |
| `speed` | 0.95 |
| `credits_debited` | 9 |
| `provider_reported_duration_s` | 32.182857 |
| `local_audio_download` | blocked by container DNS/network; no audio file included |
| `integrated_into_video` | False |
| `listened_and_academically_approved` | False |
| `financial_boundary` | 9 workspace credits were debited; no conversion to USD asserted; separate from local-render invoice fields |
| `packaged_provider_adapter` | not implemented |
| `signed_asset_url` | omitted to avoid redistributing a temporary bearer URL |

Reading: one Runway speech operation (model `eleven_multilingual_v2`, voice 'Arjun', speed 0.95) **returned a 32.18-second audio asset and debited 9 workspace credits** (message 10). The audio was **never downloaded** (container DNS/network blocked), **never integrated into a video**, **never listened to or academically approved**, and no provider adapter was packaged. Credits are not converted to USD. The temporary signed asset URL was deliberately omitted from the file.

## 7. `browser_smoke.json` findings

| Field | Value |
|---|---|
| `status` | blocked_by_environment |
| `error` | Playwright Page.goto: net::ERR_BLOCKED_BY_ADMINISTRATOR for local HTTP preview |
| `network_policy_bypassed` | False |
| `passed_browser_tests` | 0 |
| `fallback` | MP4/ffprobe integration tests passed; generated PNG contact sheets manually inspected. Preview HTML is supplied but browser playback was not validated. |

Reading: the Playwright browser smoke test of the local `preview.html` page was **blocked by administrator policy** (`net::ERR_BLOCKED_BY_ADMINISTRATOR`); ChatGPT did not bypass the restriction. **0 browser tests passed.** The fallback was the MP4/ffprobe integration tests plus manual inspection of the generated PNG contact sheets. Browser playback of `preview.html` is therefore **unvalidated** in the source; to try it yourself see `INSTRUCTIONS_running_the_four_pilots.md` section 11 (note the `outputs/` path caveat and `preview_local.html`).

## 8. `delivery_status.json` (ChatGPT's own summary of what was delivered)

| Field | Value |
|---|---|
| `date` | 2026-10-13 |
| `unit_contract_media_tests_passed` | 56 |
| `browser_smoke` | blocked_by_administrator_policy |
| `rendered_outputs` | 8 |
| `subject_fixtures` | 4 |
| `seconds_per_output` | 30 |
| `full_600s_narrated_lessons_completed` | 0 |
| `custom_skill_drafts` | 32 |
| `agent_skill_evaluations_performed` | 0 |
| `public_directory_entries` | 21 |
| `external_video_generation_jobs` | 0 |
| `external_speech_jobs_completed` | 1 |
| `runway_credits_debited` | 9 |
| `voice_output_provider_duration_seconds` | 32.182857 |
| `voice_import_and_alignment` | not_validated |
| `academic_approval` | pending |
| `student_learning_study` | not_performed |

## 9. Gaps in the measurements (do not read more into the numbers than they carry)

- Render time is wall time with two concurrent workers on ChatGPT's Linux sandbox; isolated single-worker, cold-vs-cached and peak-memory (RSS) figures were not recorded.
- No HyperFrames, Remotion, Manim or Blender run exists; do not extrapolate the simple native-SVG timings to a browser engine (`Four_Pilots.md`).
- No audio exists in any MP4; sync, captions-vs-voice alignment and loudness are untested for the video previews (narration fixtures in `../narration_outputs/` are explicitly NOT SPEECH).
- Layout QA is canvas-bounds only on 10 sampled frames per video; overlap-freedom and small-phone readability are not proven.
- Science checks cover the specified model only; they do not establish curriculum fit (Assam board mapping is `pending`) or expert approval.
- `ffmpeg.log` files are empty; the media properties above rest on the MP4 headers, not on an encoder log.
- `ffprobe` was unavailable here, so the independent re-measurement used a stdlib box parser plus macOS `mdls`/`file`; an `ffprobe -show_streams` run is still worth doing on a machine that has FFmpeg.
