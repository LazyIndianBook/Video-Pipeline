# 10_pilots_and_examples - four pilot lessons, rendered previews, sample scripts and narration fixtures

## 1. What this section is and where it came from

This section gathers everything ChatGPT produced (and that was downloaded) about **pilots and worked examples** for the ExamLeaf Video Engine: the **four pilot-lesson plans** (Physics RC charging, Chemistry atom balancing, Mathematics chain rule, Biology monohybrid cross), the **eight rendered 30-second preview MP4s** (two per subject: 16:9 and 9:16) with their contact sheets, sampled frames, manifests, captions and QA files, the **complete sample/blueprint scripts** (a full 10-minute balancing-equations script and the 41-beat Ohm's-law blueprint), the **textbook-versus-teacher narration example**, and the **narration pack's offline fixtures and outputs**. Nothing was dropped: every file in the source folders listed below was copied (`cp -R`) and re-verified byte-for-byte.

Sources (all read-only under `../00_source/`; nothing there was modified):

| Source | Used for |
|---|---|
| `extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine/` : `docs/Four_Pilots.md`, `examples/` (8 JSON), `outputs/` (103 files), `preview.html` | `pilots/`, `rendered_previews/` (ChatGPT message 10 deliverable: `ExamLeaf_Video_Engine_Implementation.zip`) |
| `downloads/ExamLeaf_Engine_Implementation/outputs/` (6 files) | `rendered_previews/_downloaded_copies/` (the separately downloaded files; `cmp`-checked against the zip) |
| `extracted/ExamLeaf_Super_Teacher_Starter_Pack/ExamLeaf_Super_Teacher/examples/` (2 files) | `sample_scripts/super_teacher_examples/` (message 08 deliverable) |
| `extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/examples/` (4 files) and `outputs/` (22 files) | `sample_scripts/narration_examples/`, `narration_outputs/` (message 12 deliverable) |
| `chatgpt_transcript/messages/` : 04 (section 11), 08 (sections 12 and 13), 12 (sections 8 and 14), 10 (sections 8.1 and 9), 02 (section 14) | `sample_scripts/*.md` (verbatim) and `INSTRUCTIONS_running_the_four_pilots.md` |

ChatGPT conversation: share `6acf03ec-b480-83ee-a000-3701059934d9`; research and local tests dated 13 October 2026.

## 2. Verified vs proposed (stated exactly as the sources state it)

**Verified (ChatGPT sandbox, with local tests):** four bounded scientific models and visual templates; **eight real 30-second silent MP4s** (30 s, 720 frames, 24 fps, 1280x720 or 720x1280); **56 tests passed** (`rendered_previews/tests.txt`); local caching, media hashes, atomic rendering and a budget ledger; render wall times 27.338-29.375 s (two jobs concurrently); one live Runway speech operation returned a 32.18 s audio asset (9 workspace credits). For the narration pack: **57 tests passed**; fixtures are real WAV files explicitly labelled **NOT SPEECH**. Message 10's own words: "The previews are therefore **technical proofs, not finished ExamLeaf lessons or evidence of production readiness**."

**Re-verified by this organiser:** every copied file is byte-identical to its source; the 8 MP4s' duration/frames/fps/resolution/codec re-measured independently (`PREVIEW_BENCHMARKS.md`); the 6 downloaded files are byte-identical to the zip copies (`cmp`).

**Not done / not verified (do not treat as established):** the four complete narrated 10-minute lessons (the `*_600s_plan.json` files are `blueprint_only` beat plans); narration imported into or synchronised with any video (the live audio was never downloaded); teacher/academic approval; student learning evaluation; browser playback of `preview.html` (blocked by administrator policy in ChatGPT's sandbox, not bypassed); HyperFrames/Remotion/Manim/Blender execution (researched, not installed or benchmarked); agent evaluation of the custom Skills; small-phone readability (layout QA is canvas-bounds only); Assam-board syllabus mapping (`pending`); the Ohm's-law blueprint and the balancing-equations script (planned, unrecorded, unvalidated; "exact second boundaries remain hypotheses"). **Proposed only:** the HyperFrames-vs-Remotion protocol, the eight-lesson phase D, the drift-velocity and biology-process first pilots, the A/B studies and the 8-16 hour budget per initial lesson.

## 3. Contents (counts are from the filesystem at time of writing)

Total files in this section: **156** = **147 copied unchanged from `00_source`** + **9 written/derived by the organiser** (marked "ADDED").

| Path | Files | What it is |
|---|---:|---|
| `README.md` (ADDED) | 1 | this file |
| `INSTRUCTIONS_running_the_four_pilots.md` (ADDED) | 1 | step-by-step guide: pilot table, per-pilot record list, HyperFrames vs Remotion protocol, release rule, v1 suggestions, Super Teacher comparisons, narration studies A/B/C, outcome measures + 2x2 calibration, opening `preview.html` |
| `PREVIEW_BENCHMARKS.md` (ADDED) | 1 | render timings (message 10 section 8.1), measured MP4/JPG/PNG properties, `cmp` results, `tests.txt` summary, probe findings |
| `pilots/` | 10 | 4 scene JSONs + 4 `*_600s_plan.json` + `Four_Pilots.md` (copied, 9) + `PILOT_PLANS_SUMMARY.md` (ADDED, every beat of each plan) |
| `rendered_previews/` | 112 | engine `outputs/` (103) + `preview.html` (copied) + `preview_local.html` (ADDED, path-fixed copy) at top level (105); plus `_downloaded_copies/` (7) |
| `sample_scripts/` | 9 | 3 ADDED verbatim extracts from the chat answers + `super_teacher_examples/` (2) + `narration_examples/` (4) |
| `narration_outputs/` | 22 | narration pack `outputs/`: 17 top-level files + `fixtures/` (5 NOT-SPEECH WAVs) |

### 3.1 `pilots/` (10 files)

| File | Notes |
|---|---|
| `Four_Pilots.md` | engine doc: actual technical run table, full pilot objectives, compositor comparison, acceptance gates, work/time planning (copied from `docs/`) |
| `physics_rc.json`, `chemistry_balance.json`, `mathematics_chain.json`, `biology_genetics.json` | 30 s scene fixtures: title, objective, class context, parameters, assumptions, OpenStax source, draft claim, 5 timed cues |
| `physics_rc_600s_plan.json`, `chemistry_balance_600s_plan.json`, `mathematics_chain_600s_plan.json`, `biology_genetics_600s_plan.json` | 600 s beat plans, `status: blueprint_only`, 11 beats each (sum 600 s) |
| `PILOT_PLANS_SUMMARY.md` (ADDED) | every beat (start/duration/end/purpose/task/script_status), prerequisites, reviews and success measures per plan, plus each scene's cues; generated from the JSON. The four beat arrays are identical (checked) |

### 3.2 `rendered_previews/` (112 files)

The 103 engine output files are placed flat (as in the zip's `outputs/`) with these stems: `physics_rc`, `chemistry_balance`, `mathematics_chain`, `biology_genetics`, each in `_16x9` and `_9x16`.

| Group | Count | Names |
|---|---:|---|
| MP4 previews | 8 | `<stem>_<aspect>.mp4`, aspect = `16x9` or `9x16` (30 s, 720 frames, 24 fps, H.264 silent) |
| Verification manifests | 8 | `<stem>_<aspect>.manifest.json` |
| Captions (WebVTT, 5 cues each) | 8 | `<stem>_<aspect>.vtt` |
| ffmpeg logs (all 0 bytes) | 8 | `<stem>_<aspect>.ffmpeg.log` |
| Sampled frames, PNG | 32 | `<stem>_<aspect>_<state>.png`, state = `opening`, `question`, `answer` or `recap` |
| Sampled frames, SVG | 32 | `<stem>_<aspect>_<state>.svg`, same four states |
| Contact sheets | 2 | `technical_previews_contact_sheet.jpg` (1280x840, landscape), `vertical_review.jpg` (1080x680, vertical) |
| Run records | 5 | `benchmark.json`, `delivery_status.json`, `live_speech_probe.json`, `browser_smoke.json`, `tests.txt` |
| **Subtotal (engine outputs)** | **103** | |
| `preview.html` | 1 | engine review page (expects an `outputs/` sub-path; see INSTRUCTIONS section 11) |
| `preview_local.html` (ADDED) | 1 | same page, `outputs/` prefix removed from 32 references so it works from this folder |
| `_downloaded_copies/` | 7 | `physics_rc_16x9.mp4`, `chemistry_balance_16x9.mp4`, `mathematics_chain_16x9.mp4`, `biology_genetics_16x9.mp4`, `technical_previews_contact_sheet.jpg`, `vertical_review.jpg` (copied, 6) + `CMP_RESULTS.md` (ADDED). All six are byte-identical (`cmp`) to the zip entries, the extracted copies and the top-level copies |

### 3.3 `sample_scripts/` (9 files)

| File | Notes |
|---|---|
| `SAMPLE_balancing_chemical_equations_full_script.md` (ADDED) | message 08 section 12 **verbatim**: 16 timed sections 00:00-10:00, italic directions, spoken text; about 1,225 spoken words, 63 s of explicit holds; planned, no audio generated |
| `BLUEPRINT_ohms_law_600_seconds.md` (ADDED) | message 04 section 11 **verbatim**: 41 instructional beats in three tables (00:00-03:30, 03:30-07:20, 07:20-10:00), 4 predictions, 3 major learner-controlled pauses; script lines are excerpts, not complete narration |
| `EXAMPLE_textbook_vs_teacher_narration.md` (ADDED) | message 12 section 8 **verbatim** (textbook vs ExamLeaf version with CURIOUS/DELIBERATE/LIGHT/FOCUSED/REASSURING modes) + the narration pack's `Before_After.md` verbatim |
| `super_teacher_examples/Complete_Sample_Script.md`, `sample_lesson.json` | Super Teacher pack examples (copied): the same balancing script as a pack file; JSON = 16 beats, 600 s, 1,225 words, status `UNRENDERED_DRAFT`, `academic_review: PENDING_HUMAN_REVIEW`, `timing_status: PLANNED_NOT_AUDIO_MEASURED` |
| `narration_examples/Before_After.md`, `claims.json`, `teacher.json`, `textbook.json` | Narration pack examples (copied): the two scripts, their source-claim ledger and the structured-narration (voice, segments, pauses, cues) JSON |

The two chat-answer files carry invisible private-use characters around `cite...turn...` markers (ChatGPT citation placeholders); they were left in so the text is byte-identical to the transcript. The same two pack files also exist in `00_source/downloads/` (`Complete_Sample_Script.md`, `Before_After.md`) and are byte-identical to the extracted ones (`cmp`).

### 3.4 `narration_outputs/` (22 files)

17 top-level files + 5 in `fixtures/` (the brief's "17" counts the top-level files; `fixtures/` adds 5):

| File(s) | Notes |
|---|---|
| `tests.txt`, `environment.json` | 57 tests passed in 3.17 s; offline signal tests, no speech model run |
| `timeline.json`, `fixture_alignment.json`, `fixture_captions.vtt` | sample-accurate timeline (48 kHz, 30 fps, 34.94 s, 5 clips, pauses, events) of the synthetic fixture; `contains_fixture: true` |
| `timing_fixture_NOT_SPEECH.wav`, `master_fixture_NOT_SPEECH.wav` | 34.94 s mono 48 kHz WAVs (24-bit); not speech |
| `fixtures/<segment>_signal_NOT_SPEECH.wav` (5; segment = `question`, `answer`, `repair`, `retry`, `check`) | per-segment 24 kHz 16-bit fixtures, 3.10-5.62 s; not speech |
| `signal_qa.json`, `mastering_qa.json`, `release_blockers.json` | signal analysis, two-pass loudness mastering (before/after vs -16 LUFS, <= -1 dBTP target), release blockers (`release_allowed: false`). There is **no `local_qa.json`** in this pack; these three are the QA records |
| `eleven_v3_requests.json`, `eleven_v4_requests.json`, `cartesia_snapshot_requests.json`, `openai_snapshot_requests.json`, `gemini_38_requests.json`, `request_preview.json` | offline compiled provider requests (no network operations). `request_preview.json` is **byte-identical** to `gemini_38_requests.json` (same MD5) |
| `cost_summary.json` | narration subsystem cost scenarios for 1/100/1,000 videos |

## 4. How to use this section (step by step)

1. **Know the status first.** Read section 2 above and `PREVIEW_BENCHMARKS.md` (top table). Everything rendered is a silent 30 s technical proof; no pilot lesson exists yet.
2. **See the proofs.** Open any MP4 in `rendered_previews/` (e.g. `physics_rc_16x9.mp4`), the two contact sheets, or run the review page: `cd rendered_previews && python3 -m http.server 8000 --bind 127.0.0.1`, then open `http://127.0.0.1:8000/preview_local.html` (details and caveats: `INSTRUCTIONS_running_the_four_pilots.md` section 11). Browser playback of the original page was never validated in the source.
3. **Read the pilot plans.** Start with `pilots/PILOT_PLANS_SUMMARY.md` (every beat), then `pilots/Four_Pilots.md`, then the JSON files.
4. **Study the exemplars before authoring.** Read `sample_scripts/SAMPLE_balancing_chemical_equations_full_script.md` and `BLUEPRINT_ohms_law_600_seconds.md` for the target density of interaction, then `EXAMPLE_textbook_vs_teacher_narration.md` for the direction style. The machine-readable counterparts are `super_teacher_examples/sample_lesson.json` and `narration_examples/teacher.json`.
5. **Inspect the narration pipeline outputs.** `narration_outputs/timeline.json` shows how pauses, cues and frames are expressed in samples; the `*_requests.json` files show provider-specific payloads; `release_blockers.json` shows what stops a release. Remember the WAVs are not speech.
6. **Check the numbers.** `PREVIEW_BENCHMARKS.md` has the render timing table, measured media properties and test/probe findings, with the gaps listed.
7. **Run the four pilots.** Follow `INSTRUCTIONS_running_the_four_pilots.md` (12-step procedure, per-pilot record sheet, compositor comparison, release rule, learning measures).
8. **Re-verify integrity at any time** (from the project root; prints nothing if everything matches):

```sh
S=00_source; R=10_pilots_and_examples
VE=$S/extracted/ExamLeaf_Video_Engine_Implementation/ExamLeaf_Video_Engine
(cd $VE/outputs && find . -type f) | while read f; do cmp -s "$VE/outputs/$f" "$R/rendered_previews/$f" || echo "DIFF $f"; done
for f in $VE/examples/*.json $VE/docs/Four_Pilots.md; do cmp -s "$f" "$R/pilots/$(basename $f)" || echo "DIFF $f"; done
cmp -s $VE/preview.html $R/rendered_previews/preview.html || echo "DIFF preview.html"
NS=$S/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System
(cd $NS/outputs && find . -type f) | while read f; do cmp -s "$NS/outputs/$f" "$R/narration_outputs/$f" || echo "DIFF $f"; done
for f in $S/downloads/ExamLeaf_Engine_Implementation/outputs/*; do cmp -s "$f" "$R/rendered_previews/_downloaded_copies/$(basename $f)" || echo "DIFF $f"; done
```

## 5. Cross-references to other sections

| Section | Relationship |
|---|---|
| `../02_learning_psychology/` | pedagogy behind the beats; source of the Ohm's-law 600 s blueprint and the A/B-experiment and confidence-calibration designs (that section also holds its own copy of the blueprint) |
| `../03_super_teacher_framework/` | the teaching personality, interaction loop and the balancing-equations sample script; pilot comparisons (message 08 section 13) |
| `../04_video_engine/` | the engine that produced these previews: architecture, schemas, 32 Skill drafts, runbook, HyperFrames/Remotion decision, how to run `examleaf.cli` |
| `../05_narration_system/` | voice identity, provider comparison, pronunciation lexicon, alignment/mastering - the system that `narration_outputs/` demonstrates |
| `../07_end_to_end_pipeline_instructions/` | the full production procedure the four pilots must run through |

## 6. Known gaps and discrepancies

- **No complete 10-minute pilot exists** for any subject; only plans (`blueprint_only`) and one full chemistry script (unrendered draft).
- **No audio in any MP4**; `ffmpeg.log` files are empty; browser playback unvalidated; tests not re-run here (no installs allowed); `ffprobe` is not installed on this machine, so media properties were re-measured with a stdlib MP4 parser plus `file`/`mdls`/`sips`/`md5`/`shasum` (see `PREVIEW_BENCHMARKS.md`).
- The task brief mentioned `local_qa.json` and 17 narration outputs "incl. fixtures/": the pack actually has 17 top-level files plus 5 in `fixtures/` (22) and no `local_qa.json`.
- `preview.html` as shipped cannot find its media when placed beside them (it expects `outputs/`); `preview_local.html` was added rather than editing the original.
- The message-04 and message-08 extracts contain ChatGPT citation placeholders; message 12 section 8 itself notes that its citation concerns the tool project, not the chemistry claim.

## 7. Complete file manifest (relative to this folder; bytes)

```text
INSTRUCTIONS_running_the_four_pilots.md  36417
PREVIEW_BENCHMARKS.md  20882
README.md  (this file)
narration_outputs/cartesia_snapshot_requests.json  9478
narration_outputs/cost_summary.json  1131
narration_outputs/eleven_v3_requests.json  7597
narration_outputs/eleven_v4_requests.json  8032
narration_outputs/environment.json  252
narration_outputs/fixture_alignment.json  12990
narration_outputs/fixture_captions.vtt  1444
narration_outputs/fixtures/answer_signal_NOT_SPEECH.wav  261164
narration_outputs/fixtures/check_signal_NOT_SPEECH.wav  235244
narration_outputs/fixtures/question_signal_NOT_SPEECH.wav  148844
narration_outputs/fixtures/repair_signal_NOT_SPEECH.wav  269804
narration_outputs/fixtures/retry_signal_NOT_SPEECH.wav  200684
narration_outputs/gemini_38_requests.json  11675
narration_outputs/master_fixture_NOT_SPEECH.wav  5031462
narration_outputs/mastering_qa.json  711
narration_outputs/openai_snapshot_requests.json  9545
narration_outputs/release_blockers.json  435
narration_outputs/request_preview.json  11675
narration_outputs/signal_qa.json  530
narration_outputs/tests.txt  99
narration_outputs/timeline.json  5600
narration_outputs/timing_fixture_NOT_SPEECH.wav  5031404
pilots/Four_Pilots.md  4240
pilots/PILOT_PLANS_SUMMARY.md  19574
pilots/biology_genetics.json  2659
pilots/biology_genetics_600s_plan.json  3656
pilots/chemistry_balance.json  2691
pilots/chemistry_balance_600s_plan.json  3641
pilots/mathematics_chain.json  2335
pilots/mathematics_chain_600s_plan.json  3553
pilots/physics_rc.json  2588
pilots/physics_rc_600s_plan.json  3606
rendered_previews/_downloaded_copies/CMP_RESULTS.md  1421
rendered_previews/_downloaded_copies/biology_genetics_16x9.mp4  203333
rendered_previews/_downloaded_copies/chemistry_balance_16x9.mp4  212515
rendered_previews/_downloaded_copies/mathematics_chain_16x9.mp4  225773
rendered_previews/_downloaded_copies/physics_rc_16x9.mp4  347653
rendered_previews/_downloaded_copies/technical_previews_contact_sheet.jpg  105919
rendered_previews/_downloaded_copies/vertical_review.jpg  63830
rendered_previews/benchmark.json  22333
rendered_previews/biology_genetics_16x9.ffmpeg.log  0
rendered_previews/biology_genetics_16x9.manifest.json  2663
rendered_previews/biology_genetics_16x9.mp4  203333
rendered_previews/biology_genetics_16x9.vtt  496
rendered_previews/biology_genetics_16x9_answer.png  54615
rendered_previews/biology_genetics_16x9_answer.svg  3640
rendered_previews/biology_genetics_16x9_opening.png  47774
rendered_previews/biology_genetics_16x9_opening.svg  2981
rendered_previews/biology_genetics_16x9_question.png  52004
rendered_previews/biology_genetics_16x9_question.svg  3513
rendered_previews/biology_genetics_16x9_recap.png  56735
rendered_previews/biology_genetics_16x9_recap.svg  3640
rendered_previews/biology_genetics_9x16.ffmpeg.log  0
rendered_previews/biology_genetics_9x16.manifest.json  2663
rendered_previews/biology_genetics_9x16.mp4  202027
rendered_previews/biology_genetics_9x16.vtt  496
rendered_previews/biology_genetics_9x16_answer.png  61322
rendered_previews/biology_genetics_9x16_answer.svg  3742
rendered_previews/biology_genetics_9x16_opening.png  54840
rendered_previews/biology_genetics_9x16_opening.svg  3086
rendered_previews/biology_genetics_9x16_question.png  60287
rendered_previews/biology_genetics_9x16_question.svg  3615
rendered_previews/biology_genetics_9x16_recap.png  63124
rendered_previews/biology_genetics_9x16_recap.svg  3741
rendered_previews/browser_smoke.json  367
rendered_previews/chemistry_balance_16x9.ffmpeg.log  0
rendered_previews/chemistry_balance_16x9.manifest.json  2491
rendered_previews/chemistry_balance_16x9.mp4  212515
rendered_previews/chemistry_balance_16x9.vtt  472
rendered_previews/chemistry_balance_16x9_answer.png  57649
rendered_previews/chemistry_balance_16x9_answer.svg  6423
rendered_previews/chemistry_balance_16x9_opening.png  53655
rendered_previews/chemistry_balance_16x9_opening.svg  5144
rendered_previews/chemistry_balance_16x9_question.png  58770
rendered_previews/chemistry_balance_16x9_question.svg  5943
rendered_previews/chemistry_balance_16x9_recap.png  56752
rendered_previews/chemistry_balance_16x9_recap.svg  6421
rendered_previews/chemistry_balance_9x16.ffmpeg.log  0
rendered_previews/chemistry_balance_9x16.manifest.json  2492
rendered_previews/chemistry_balance_9x16.mp4  212760
rendered_previews/chemistry_balance_9x16.vtt  472
rendered_previews/chemistry_balance_9x16_answer.png  64152
rendered_previews/chemistry_balance_9x16_answer.svg  6635
rendered_previews/chemistry_balance_9x16_opening.png  60899
rendered_previews/chemistry_balance_9x16_opening.svg  5316
rendered_previews/chemistry_balance_9x16_question.png  66073
rendered_previews/chemistry_balance_9x16_question.svg  6155
rendered_previews/chemistry_balance_9x16_recap.png  63941
rendered_previews/chemistry_balance_9x16_recap.svg  6632
rendered_previews/delivery_status.json  642
rendered_previews/live_speech_probe.json  735
rendered_previews/mathematics_chain_16x9.ffmpeg.log  0
rendered_previews/mathematics_chain_16x9.manifest.json  2640
rendered_previews/mathematics_chain_16x9.mp4  225773
rendered_previews/mathematics_chain_16x9.vtt  423
rendered_previews/mathematics_chain_16x9_answer.png  62562
rendered_previews/mathematics_chain_16x9_answer.svg  6808
rendered_previews/mathematics_chain_16x9_opening.png  57373
rendered_previews/mathematics_chain_16x9_opening.svg  6565
rendered_previews/mathematics_chain_16x9_question.png  61127
rendered_previews/mathematics_chain_16x9_question.svg  6677
rendered_previews/mathematics_chain_16x9_recap.png  64069
rendered_previews/mathematics_chain_16x9_recap.svg  6927
rendered_previews/mathematics_chain_9x16.ffmpeg.log  0
rendered_previews/mathematics_chain_9x16.manifest.json  2640
rendered_previews/mathematics_chain_9x16.mp4  222870
rendered_previews/mathematics_chain_9x16.vtt  423
rendered_previews/mathematics_chain_9x16_answer.png  62810
rendered_previews/mathematics_chain_9x16_answer.svg  6788
rendered_previews/mathematics_chain_9x16_opening.png  59718
rendered_previews/mathematics_chain_9x16_opening.svg  6670
rendered_previews/mathematics_chain_9x16_question.png  64791
rendered_previews/mathematics_chain_9x16_question.svg  6780
rendered_previews/mathematics_chain_9x16_recap.png  67944
rendered_previews/mathematics_chain_9x16_recap.svg  7067
rendered_previews/physics_rc_16x9.ffmpeg.log  0
rendered_previews/physics_rc_16x9.manifest.json  2667
rendered_previews/physics_rc_16x9.mp4  347653
rendered_previews/physics_rc_16x9.vtt  477
rendered_previews/physics_rc_16x9_answer.png  61917
rendered_previews/physics_rc_16x9_answer.svg  4109
rendered_previews/physics_rc_16x9_opening.png  56258
rendered_previews/physics_rc_16x9_opening.svg  3901
rendered_previews/physics_rc_16x9_question.png  60626
rendered_previews/physics_rc_16x9_question.svg  4115
rendered_previews/physics_rc_16x9_recap.png  63100
rendered_previews/physics_rc_16x9_recap.svg  4905
rendered_previews/physics_rc_9x16.ffmpeg.log  0
rendered_previews/physics_rc_9x16.manifest.json  2667
rendered_previews/physics_rc_9x16.mp4  340225
rendered_previews/physics_rc_9x16.vtt  477
rendered_previews/physics_rc_9x16_answer.png  68664
rendered_previews/physics_rc_9x16_answer.svg  4214
rendered_previews/physics_rc_9x16_opening.png  63864
rendered_previews/physics_rc_9x16_opening.svg  4004
rendered_previews/physics_rc_9x16_question.png  67703
rendered_previews/physics_rc_9x16_question.svg  4220
rendered_previews/physics_rc_9x16_recap.png  69818
rendered_previews/physics_rc_9x16_recap.svg  5016
rendered_previews/preview.html  4730
rendered_previews/preview_local.html  4410
rendered_previews/technical_previews_contact_sheet.jpg  105919
rendered_previews/tests.txt  99
rendered_previews/vertical_review.jpg  63830
sample_scripts/BLUEPRINT_ohms_law_600_seconds.md  9086
sample_scripts/EXAMPLE_textbook_vs_teacher_narration.md  5855
sample_scripts/SAMPLE_balancing_chemical_equations_full_script.md  11441
sample_scripts/narration_examples/Before_After.md  2391
sample_scripts/narration_examples/claims.json  836
sample_scripts/narration_examples/teacher.json  5095
sample_scripts/narration_examples/textbook.json  1371
sample_scripts/super_teacher_examples/Complete_Sample_Script.md  14406
sample_scripts/super_teacher_examples/sample_lesson.json  18655
```

156 files listed .
