# ExamLeaf Narration Pipeline — Step-by-step Instructions

**Section:** `05_narration_system` · **Code described:** `narration_system_v1/` (the unzipped `ExamLeaf_Narration_System` starter, 123 files, package `examleaf-narration` 0.1.0, compiler version 0.1.1) · **Sources:** message 12 §9–§15 (`FULL_narration_system.md`); `narration_system_v1/README.md`, `AGENTS.md`, `CLAUDE.md`, `LICENSING_AND_SECURITY.md`, `pyproject.toml`; `docs/Architecture.md`, `docs/Audition_and_Evaluation.md`, `docs/Implementation_Roadmap.md`, `docs/Provider_Lifecycle.md`; every module in `src/examleaf_narration/`; `scripts/build_examples.py`, `scripts/build_docs.py`; `tests/test_narration.py`; `outputs/*`. All code was **read, not executed**, while organising this section.

> **What this pipeline is today (verbatim status):** "**Status: offline-tested sidecar, not a finished production speech service.**" It "Integrates with the prior ExamLeaf Video Engine through manifests, not by changing its scientific renderers." Local tests: **57 passed** (`outputs/tests.txt`: "57 passed in 3.17s", Python 3.13.5 on Linux). "Complete production service — Not yet: authenticated synthesis transport, actual ASR/alignment execution, and authenticated approval remain to be integrated." "Production HTTP transport, billing ledger and authentication are not implemented. Do not blindly execute request JSON." "Local signal fixtures demonstrate engineering timing only. No new voice clone was created."
>
> **15 Oct 2026 update:** after the Indic tokenization fix (`narration_system_v1/CHANGES.md`) the suite is 52 test functions = 60 cases: **58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg**. Two files now differ from `DELIVERY_MANIFEST.json` on purpose (`src/examleaf_narration/pronunciation.py`, `tests/test_narration.py`); every other manifest entry still matches. The loudness/mastering tests are verified only where FFmpeg is installed.

Cross-references: the video engine whose scene adapters consume `timeline.events` → `04_video_engine`; the end-to-end production run-book that this sidecar slots into → `07_end_to_end_pipeline_instructions`; Skills that drive each stage → `SKILLS_INDEX_narration_15.md` (this section) and `06_skills_library`; persona/voice rules → `VOICE_IDENTITY_and_DELIVERY_GUIDE.md` and `03_super_teacher_framework`; providers and costs → `TTS_PROVIDER_COMPARISON.md` and `08_cost_models`; listening pilots → `10_pilots_and_examples`.

---

## 1. Prerequisites

| Requirement | Detail (from `README.md` / `pyproject.toml` / `outputs/environment.json`) |
|---|---|
| Python | **3.11+** (`requires-python = ">=3.11"`). Built and tested on Python 3.13.5, Linux-6.18.44-x86_64-with-glibc2.41. |
| FFmpeg | "a **reviewed FFmpeg build on PATH**". Needed by `qa` and `master` CLI commands, by `scripts/build_examples.py` (mastering step), and by 2 tests (`test_silent_loudness_rejected`, `test_two_pass_master_real_signal_file`). FFmpeg licence is "LGPL/GPL depending build/codecs". |
| Runtime deps | `pydantic>=2.10,<3`, `numpy>=2,<3`, `scipy>=1.14,<2`, `soundfile>=0.12,<1` (recorded versions: pydantic 2.13.5, numpy 2.3.5, scipy 1.17.0, soundfile 0.13.1) |
| Test deps | `pytest>=8,<10` (extra `[test]`) |
| Build | `setuptools>=68`; package found under `src/`; console script **`examleaf-voice`** = `examleaf_narration.cli:main` |
| Reproducibility caveat | "Dependency ranges in pyproject are not a fully hashed reproducible lock. Pin target deployment wheels/container before production." |
| Network / credentials | **None needed.** "No network execution or paid synthesis occurs from the offline CLI." Provider IDs and `ENV:` markers are templates, not credentials. |

## 2. Set up (step by step)

1. **Work on a copy, not on the archived starter.** `scripts/build_examples.py` overwrites `configs/pronunciation.json`, the five `configs/<profile>.json`, `configs/narration.schema.json`, `examples/teacher.json|textbook.json|claims.json` and most of `outputs/`; `pip install -e` writes build metadata into `src/`. Keep `05_narration_system/narration_system_v1/` pristine (its 122 files are hash-listed in `DELIVERY_MANIFEST.json`, all verified at delivery; *15 Oct 2026: `src/examleaf_narration/pronunciation.py` and `tests/test_narration.py` intentionally differ, see `CHANGES.md`*):
   ```bash
   cp -R /path/to/05_narration_system/narration_system_v1 ~/work/examleaf_narration
   cd ~/work/examleaf_narration          # every command below runs from the repo root (relative paths)
   ```
2. **Create and activate a virtual environment.**
   ```bash
   python -m venv .venv
   # Activate the environment for your operating system:
   source .venv/bin/activate             # macOS / Linux
   # .venv\Scripts\activate              # Windows
   ```
3. **Install the package with test extras.**
   ```bash
   python -m pip install -e '.[test]'
   ```
4. **Confirm FFmpeg:** `ffmpeg -version` (use a build you have reviewed).

## 3. Every CLI command, in the order to run them

All commands are exactly as in `README.md` / message 12 §15. `PYTHONPATH=src` lets them run even without the editable install.

| # | Command | What it does | Writes | Expected result |
|---:|---|---|---|---|
| 1 | `PYTHONPATH=src python scripts/build_examples.py` | Rebuilds the 40-term lexicon, the teacher/textbook plans and claims ledger, the 5 provider profiles and their compiled requests, the JSON schema, five **NOT-SPEECH** tone fixtures (24 kHz, 16-bit, carrier 170 + 25·i Hz + 430 Hz, duration 0.4 + 0.18 s × word count), synthetic word timings (`method: synthetic-fixture`, 0.18 s per word), the composed 48 kHz timeline + WAV, captions, signal QA, two-pass master (FFmpeg), release blockers and environment record | `configs/pronunciation.json`, `configs/{eleven_v4,eleven_v3,cartesia_snapshot,gemini_38,openai_snapshot}.json`, `configs/narration.schema.json`, `examples/{teacher,textbook,claims}.json`, `outputs/<profile>_requests.json`, `outputs/fixtures/*_signal_NOT_SPEECH.wav`, `outputs/fixture_alignment.json`, `outputs/timing_fixture_NOT_SPEECH.wav`, `outputs/timeline.json`, `outputs/fixture_captions.vtt`, `outputs/signal_qa.json`, `outputs/mastering_qa.json`, `outputs/master_fixture_NOT_SPEECH.wav`, `outputs/release_blockers.json`, `outputs/environment.json` | prints `Built 40 explicit term mappings, 5 request recipes; fixture duration 34.940s`. Note: it rewrites `environment.json` without the `pydantic`/`scipy` keys the shipped copy has. |
| 2 | `PYTHONPATH=src pytest -q` | Runs `tests/test_narration.py` (49 test functions, 57 cases with parametrisation at delivery; *15 Oct 2026: 52 functions, 60 cases*) | pytest temp dirs only | `57 passed` at delivery; *15 Oct 2026: 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg* |
| 3 | `PYTHONPATH=src python -m examleaf_narration.cli validate examples/teacher.json` | Validates a plan against the Pydantic contracts (fields, ranges, ids, answer dependencies, no stage tags in spoken text) | nothing | `Valid contract: water_coefficient_demo; not academic/audio approval` |
| 4 | `PYTHONPATH=src python -m examleaf_narration.cli compile examples/teacher.json --lexicon configs/pronunciation.json --profile configs/gemini_38.json --out outputs/request_preview.json` | Expands `{{tokens}}`, checks locale/model admission and lexicon version, builds one provider request per segment. **Sends zero network requests.** Swap `--profile` for any of the five `configs/*.json` profiles (Cartesia fails until `api_version` is a real value) | `--out` JSON (atomic write) | `Compiled 5 payloads; sent 0 requests` |
| 5 | `PYTHONPATH=src python -m examleaf_narration.cli qa outputs/timing_fixture_NOT_SPEECH.wav --out outputs/local_qa.json` | Signal report (duration, rate, channels, sample peak, RMS, clipped samples, DC offset, silences ≥ 0.6 s) + FFmpeg loudness measurement | `outputs/local_qa.json` | JSON with `signal` and `loudness`. The CLI does not pass the timeline's pause intervals, so every silence is reported `planned: false` here (`build_examples.py` passes them and gets `planned: true`). |
| 6 | `PYTHONPATH=src python -m examleaf_narration.cli master <in.wav> --out <out.wav>` | Two-pass FFmpeg `loudnorm` (I = −16, TP = −1, LRA = 7, linear) → 48 kHz mono 24-bit PCM WAV, then re-measures. Refuses to overwrite the source. *(Present in `cli.py`; not listed in the README.)* | `<out.wav>` | prints `{before, after, target, within_target}` |
| 7 | `PYTHONPATH=src python -m examleaf_narration.cli release-check outputs/timeline.json` | Builds the release report with **empty** checks and evidence and then **always exits with status 2** | nothing | prints the blocker list (same as `outputs/release_blockers.json`), exit code 2 |

**Why `release-check` exits 2 (by design):** "The release check intentionally exits 2. It requires true speech and an authenticated approval service; local self-asserted booleans cannot approve a production lesson." `release_report()` always returns `release_allowed: false` and always appends "Authenticated approval service not implemented; local booleans are not trusted approvals" — even when every evidence flag is `true` and hashes match (`test_no_fabricated_local_human_approval`). For the shipped fixture timeline it also lists: "Synthetic fixture is not speech and cannot be released"; "Missing academic_listening"; "Missing voice_rights"; "Missing native_language_review"; "Missing caption_review"; "Missing sync_review"; "Approval/audio hash mismatch"; "Audio mastering not passed". **"Do not bypass that result with fabricated reviewer identities."** `AGENTS.md`: "Do not turn a fixture into a release by changing a boolean."

**Not part of the run sequence:** `scripts/build_docs.py` regenerates `research/*.csv`, `research/Public_Narration_Directory.md`, all 15 `skills/*`, `configs/existing_engine_skill_mapping.json`, `AGENTS.md`, `CLAUDE.md`, `docs/Architecture.md`, `docs/Voice_Identity_Guide.md`, `docs/Audition_and_Evaluation.md`, `docs/Reusable_Prompts.md` and `README.md`. Static comparison shows its output equals the shipped files **except `README.md`**: the generated README is an older variant that omits the pointers to `docs/Provider_Lifecycle.md` and `docs/Implementation_Roadmap.md`. Do not run it over the curated copy. (`docs/Costs_and_Methods.md`, `docs/Provider_Lifecycle.md`, `docs/Implementation_Roadmap.md`, `outputs/cost_summary.json`, `outputs/tests.txt`, the `.xlsx` and `DELIVERY_MANIFEST.json` are produced by neither script.)

After any modification: `AGENTS.md` — "Run `PYTHONPATH=src pytest -q` after modifications."

## 4. What each `src/examleaf_narration` module does (read from the code)

| Module | Responsibility | Key functions / classes and enforced rules |
|---|---|---|
| `__init__.py` | Package marker | Docstring "Offline-tested narration sidecar. No implicit provider requests."; `__version__ = "0.1.0"` |
| `contracts.py` | Typed data contracts (Pydantic v2, `extra="forbid"`, `validate_assignment=True`) | `VoiceIdentity`, `Direction`, `Cue`, `Pause`, `Segment`, `NarrationPlan`, `ProviderProfile`, `AlignedWord`, `Alignment` — full field spec in §7. Rejects unknown fields (e.g. an injected `"execute": "rm -rf data"`), duplicate segment/cue ids, forward or window-less answers, pauses without task prompts, stage tags in spoken text, non-positive or overlapping word intervals |
| `pronunciation.py` | Explicit symbolic speech choices ("never infer ambiguous mathematics silently") | `TOKEN = \{\{([a-z][a-z0-9_]*)\}\}`; `expand(template, lexicon, locale, form="spoken"\|"display"\|"caption")` → fails on unknown token ("Unresolved STEM token: …"), on a locale without an `editorially_checked` mapping ("No editorially checked {locale} mapping for {key}"), on leftover braces ("Malformed/unresolved speech token"); returns NFC text. Acoustic approval is deliberately *not* checked here. `digest()` = SHA-256 of canonical JSON. `normalized_words()` — NFC + casefold tokeniser keeping `+ − = ^ < > -` ("Only an English/surface comparator. Native Indic tokenization requires separate review." — delivered docstring). *15 Oct 2026: no longer English-only. Replaced by a category-based scanner: a word is a run of Unicode letters, marks and numbers (category L/M/N), inner apostrophes kept, ZWJ/ZWNJ transparent, maths symbols single tokens; Indic-safe (Devanagari and Bengali–Assamese vowel signs, virama and nukta no longer split words). Still a surface comparator; native review still required. See `CHANGES.md`.*. `critical_counts()` — occurrences of each critical phrase |
| `compiler.py` | Offline provider-request compiler ("Does not send HTTP or consume provider credits") | `compile_plan(plan, profile, lexicon, production=False)`: admission via `LANGUAGES`; production gates (deprecated model, voice rights, `live_contract_verified`, placeholder voice id); lexicon-version match; 1,800-character segment cap; per-provider body (§8); per-segment `audio_cache_key` = digest of {compiler version, expanded spoken text, profile, voice, direction, digest of only the lexicon entries this segment uses} — **visuals and holds are excluded** ("no paid resynthesis for an editorial timing change"). Output `{status: "offline-request-compilation-not-live-integration", lesson_id, requests[], network_operations: 0}`; each request has `segment_id, method, url, headers_template, body, canonical_spoken, caption_text, audio_cache_key, editorial_style, warnings` |
| `cache.py` | Integrity and regeneration control | `file_hash()` (SHA-256, 1 MiB blocks); `atomic_json()` (temp file + fsync + `os.replace`, `allow_nan=False`); `cache_record()` / `cache_valid()` (key + audio hash must both match); `decide_submission(state)`: `submitted`/`running`/`unknown` → `reconcile-existing-job-never-blindly-resubmit`; `succeeded` → `validate-and-cache-existing-output`; `not-submitted` → `reserve-budget-then-submit-once`; `failed` → `review-failure-and-authorize-bounded-retry`; anything else → error |
| `timeline.py` | Sample-accurate assembly and animation events | `frame_at(sample, sr, fps_num=30, fps_den=1)` — exact rational, round-half-up; `validate_alignment()` — audio hash, transcript digest, identical normalized word sequence, non-empty, last word ≤ duration + 1 ms; `cue_time()` — phrase match on one-token-per-word alignment, chosen `occurrence`, `edge` start/end ("Missing cue occurrence: …"); `compose(plan, lexicon, audio_paths, alignments, output, sample_rate=48000, fps_num=30, fps_den=1)` — mono only ("explicitly review/downmix first"), polyphase resampling to 48 kHz, clips placed back-to-back, cue events at `clip_start + round(t × 48000)`, captions every 6 aligned words, **exact zero samples** for each pause, "Premature answer" if an answer clip starts before its question's pause ends, writes 24-bit WAV, returns `{lesson_id, sample_rate, fps_num, fps_den, total_samples, duration_seconds, audio_sha256, clips, pauses, events, captions, contains_fixture}`; `write_vtt()` — WebVTT from sample positions |
| `qa.py` | Transcript, signal, loudness, mastering, release gate | `transcript_check(expected, observed, critical_phrases)` — word-level edit distance → `surface_word_error_rate`, `edit_count`, `critical_mismatches`, `needs_human_check`, `limitation` ("ASR can normalize mispronunciation into the intended word; zero WER does not approve pronunciation."); `signal_report(path, protected_intervals=(), silence_seconds=0.6)` — 20 ms frames, quiet < −50 dBFS, clipped = \|x\| ≥ 0.9999, silence `planned` if inside a protected interval ± 0.05 s, `not_measured: naturalness, accent authenticity, STEM pronunciation, true-peak until FFmpeg measurement`; `loudness_measure()` — FFmpeg `loudnorm=I=-16:TP=-1:LRA=7:print_format=json`, rejects unmeasurable (silent) audio; `master()` — second pass with measured values, `linear=true`, `-ar 48000 -ac 1 -c:a pcm_s24le`, re-measure, `within_target` = \|I + 16\| ≤ 1 and TP ≤ −0.9; `release_report()` — fail-closed blocker list (always `release_allowed: false`) |
| `cli.py` | Command line (`argparse`, "Offline-first narration tools: compile never calls providers.") | sub-commands `validate`, `compile`, `qa`, `master`, `release-check` (§3) |

## 5. The test suite (`tests/test_narration.py`, 57 cases at delivery; 60 cases as of 15 Oct 2026)

Contracts: `test_contract`, `test_extra_field`, `test_duplicate_segment`, `test_forward_answer`, `test_no_response_window`, `test_pause_needs_task`, `test_pause_none_no_time`, `test_direction_not_spoken`×3 (`[excited]`, `<short pause>`, `[REVEAL answer]`). Pronunciation: `test_alias_water`, `test_display_separate`, `test_missing_term`, `test_malformed_term`, `test_no_unreviewed_language`, `test_distinct_scientific_readings`×5 (inverse vs reciprocal sine, milli- vs mega-ampere, mol/L vs mol/kg, 5′ vs 3′, mitosis vs meiosis). Compiler: `test_unknown_provider_model`, `test_block_unverified_production`, `test_lexicon_version`, `test_v4_no_legacy_knobs`, `test_gemini_metadata`, `test_openai_metadata`, `test_cartesia_version_required`, `test_multilingual_v2_reject_assamese`, `test_deprecated_model_blocked_even_with_approval`. Cache: `test_cache_ignores_visual_edit`, `test_cache_changes_voice`, `test_cache_changes_speech`, `test_corrupt_cache`, `test_atomic_manifest`, `test_never_duplicate_unknown_paid_job`×3, `test_unused_lexicon_entry_does_not_regenerate`, `test_used_lexicon_entry_does_regenerate`. Alignment/timeline: `test_invalid_aligned_interval`, `test_overlapping_single_voice_alignment`, `test_second_occurrence_anchor`, `test_missing_anchor_fails`, `test_frame_mapping` (48,000 samples → frame 30; 600 s at 30000/1001 fps → frame 17,982), `test_fixture_timing_and_answer_protection`, `test_alignment_wrong_waveform`. QA/release: `test_negation_loss`, `test_wrong_atom_count`, `test_zero_wer_not_pronunciation_approval`, `test_reject_empty_transcript`, `test_signal_clipping`, `test_silence_is_planned`, `test_silent_loudness_rejected`, `test_two_pass_master_real_signal_file`, `test_master_source_protected`, `test_release_fail_closed`, `test_no_fabricated_local_human_approval`.

*15 Oct 2026: three Indic regression tests added: `test_indic_words_stay_whole`, `test_cue_time_anchors_hindi_words`, `test_transcript_check_hindi_critical_phrase`. Result on this Mac: 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg (the two FFmpeg-dependent tests are `test_silent_loudness_rejected` and `test_two_pass_master_real_signal_file`).*

---

## 6. The correct production sequence

### 6.1 Overall approach (message 12, opening)

> **Approved academic explanation → conversational teaching script → performance direction → context-aware pronunciation → segmented speech generation → independent transcription and listening checks → alignment → animation timing → mastering → final approval.**

The user's requested pipeline (message 11 §7): Academic Content → Human-Like Script → Teaching Psychology Review → Humour & Storytelling → Emotional Voice Direction → Pronunciation Validation → TTS Generation → Speech Alignment → Audio QA → Animation Synchronization → Final Mastering.

Full production graph (`docs/Architecture.md`): Approved source-linked claims → teacher draft → naturalizer/story/interaction review → academic script approval → Direction and context-aware pronunciation mappings → provider request compilation → rights/model/budget admission → one synthesis job per coherent segment → persist job ID and raw audio → independent ASR → script diff and critical-word review → forced alignment against exact accepted speech → semantic visual anchors → sample-index composition with protected pauses → captions → whole-track mastering → final encode/re-measure → native/academic/full-viewing approval bound to hashes.

### 6.2 The audio sequence, step by step (message 12 §11.1 diagram + final approval gate)

```text
Accepted narration text
        ↓
Generate coherent sentence groups
        ↓
Save raw audio and provider usage
        ↓
Independent ASR and critical-term review
        ↓
Accept or repair the take
        ↓
Forced alignment to accepted speech
        ↓
Resolve semantic animation markers
        ↓
Insert protected thinking/writing pauses
        ↓
Compose captions and visual events
        ↓
Master, encode, re-measure and review
```

"Do not begin by estimating that every sentence needs eight seconds." The source diagram has ten boxes; step 11 below is the "final approval" gate named in the overall approach and in `docs/Architecture.md`.

| Step | What to do | Tool / module / Skill | Status in the starter |
|---:|---|---|---|
| 1. Accepted narration text | Approved claims → teacher draft → naturalizer/story/interaction review → academic script approval; STEM terms written as `{{tokens}}`; plan validated | Skills #1–#9; `cli validate`; existing scientific reviewer remains the authority (see `06_skills_library`) | Contracts implemented and tested; Skills authored, not agent-evaluated |
| 2. Generate coherent sentence groups | Split into coherent one-to-three-sentence or roughly 15–35-second units ("Not a fixed rule. Do not synthesize every sentence separately"). Split questions from answer reveals. Compile model-specific requests; pass rights/model/budget admission; **one synthesis job per coherent segment** | Skill #11; `compiler.compile_plan` (1,800-char cap) | Request compilation implemented offline; **live transport not implemented** |
| 3. Save raw audio and provider usage | Persist job ID, raw audio, request/response hashes and actual usage, excluding secrets and signed URLs; never resubmit an unknown-state job | Skill #15; `cache.decide_submission`, `cache_record`, `atomic_json` | Local hashing/decision logic only; billing ledger and queue not implemented |
| 4. Independent ASR and critical-term review | Transcribe with a **separately evaluated** ASR (audio-only decoding, no expected-text bias); compare with canonical text; check every critical phrase, number, unit, negation, direction | Skill #14; `qa.transcript_check`; candidates faster-whisper, Gemini transcription (Assamese) | Comparator implemented; **no ASR inference integrated** |
| 5. Accept or repair the take | Human listening of hard terms; regenerate **only** the affected segment (cache key unchanged for visual-only edits) | Skills #14, #15; reviewers | Human step |
| 6. Forced alignment to accepted speech | Align the exact accepted transcript to the accepted audio; import as `Alignment` (method `provider-timestamps`/`forced-aligner`/`human`); verify against a manually annotated sample | Skill #12; ElevenLabs alignment initially, WhisperX/MFA where language resources suit; `timeline.validate_alignment` | Import/validation implemented; **no aligner executed** (fixture timings are synthetic) |
| 7. Resolve semantic animation markers | Resolve each `Cue` (phrase + occurrence + edge) to a word time | `timeline.cue_time` | Implemented and tested |
| 8. Insert protected thinking/writing pauses | Insert exact zero samples (e.g. 6 s = 288,000 samples at 48 kHz); answers cannot start before the window ends | `timeline.compose` | Implemented and tested |
| 9. Compose captions and visual events | Global sample → output frame once; WebVTT captions; pass `timeline.events` to the existing scene adapters | `timeline.compose`, `write_vtt`; existing renderer (`04_video_engine`) | Prototype captions; renderer hookup pending |
| 10. Master, encode, re-measure and review | Two-pass loudness to −16 LUFS / ≤ −1 dBTP, 48 kHz mono 24-bit archive; encode; **re-measure the final encoded delivery**; listen | Skill #13; `qa.master`, `qa.loudness_measure`, `qa.signal_report` | Implemented; tested on signal fixtures only |
| 11. Final approval | Native-language, academic and full-viewing approval **bound to hashes**; release gate | Skill #14; `qa.release_report` / `cli release-check` | Fail-closed by design; **authenticated approval service not implemented** |

### 6.3 Connect to the existing engine (`docs/Architecture.md`)

Leave existing Python scientific verification and renderer adapters unchanged. Add `narration_plan_uri` and `narration_manifest_sha256` to the lesson manifest. Pass accepted `timeline.events` to scene adapters; each includes the cue, element, action, global sample and output frame. Replace estimated scene lengths with measured clip/hold intervals. Rendering may be repeated freely without resynthesizing speech. Export science visual and spoken-caption alternatives separately; a symbol-focused caption view must not erase accessible spoken meaning. Each locale has independent voice/lexicon/audio/timing objects. Do not time-stretch the translation into English durations. Hash actual provider/model/voice and pronunciation versions. Where vendor voices expire or change, preserve lawfully retained approved output; alert and audition replacement rather than silently switching. Re-align or remap after any audio trim/time change (README step 4). The engine side is documented in `04_video_engine`.

**Segments (`docs/Architecture.md`):** Typical target: coherent one-to-three-sentence or roughly 15–35-second units. Not a fixed rule. Do not synthesize every sentence separately: unnecessary boundaries harm continuity and create overhead. Split questions from answer reveals; insert exact think time locally. For long formulas, spoken semantic phrases need matching visual groups. Use sample-rate 48k for final master; providers may natively return 24k/44.1k. Resampling does not recreate missing high-frequency detail.

**Provider worker design still to implement:** Least-privilege secrets, allowlisted endpoints, timeouts, concurrency limits, reserve-and-commit billing ledger and per-job idempotency. Provider calls returning an unknown state must be reconciled before another submission. A documented caller-supplied idempotency key is useful only where the endpoint actually supports it. Save request/response hashes and actual usage, excluding secrets and signed URLs.

---

## 7. Structured narration format (spec)

"Keep directing instructions out of canonical spoken text. The provider adapter decides what can safely become a model-specific control." "The included plan contains a voice identity, version, locale, rights record, source-claim manifest, lexicon version, and an ordered set of segments." (message 12 §9) Formal schema: `configs/narration.schema.json` (generated from `contracts.NarrationPlan`).

### 7.1 Plan-level fields (`NarrationPlan`)

| Field | Type / rule | Example (`examples/teacher.json`) |
|---|---|---|
| `schema_version` | const `"1.0"` (default) | `1.0` |
| `lesson_id` | `^[a-z][a-z0-9_-]*$` | `water_coefficient_demo` |
| `academic_edition` | string | "Demonstration only; board alignment not certified" |
| `source_claim_manifest` | string (path/URI of the claim ledger) | `examples/claims.json` |
| `voice` | `VoiceIdentity` (below) | — |
| `lexicon_version` | string; **must equal** the lexicon's `version` at compile time | `en-reviewed-example-1` |
| `segments` | ≥ 1 `Segment`; ids unique; cue ids unique across the plan | 5 segments |

`VoiceIdentity`: `identity_id`, `version`, `brief` (all non-empty); `locale` ∈ `en-IN | hi-IN | as-IN`; `rights_status` ∈ `audition-only | licensed-stock | consented-custom | unverified`; `rights_record` (non-empty); `reference_audio_sha256` (optional). Production compile requires `licensed-stock` or `consented-custom`.

### 7.2 Segment fields

| Field | Type / rule |
|---|---|
| `segment_id` | `^[a-z][a-z0-9_-]*$` |
| `objective_id` | non-empty (educational objective) |
| `claim_ids` | ≥ 1 approved claim id |
| `text_template` | 1–6,000 chars; spoken words only; **no `[…]` or `<…>`**; STEM terms as `{{lexicon_key}}` |
| `direction` | `mode` ∈ curious, steady (default), deliberate, light, reassuring, focused; `target_wpm` 80–185 (default 140); `emphasis` list; `notes` |
| `pause_after` | `kind` ∈ none (default), beat, think, pause-video; `seconds` 0–30; `prompt`. `none` must have 0 s; `think`/`pause-video` require a `prompt` |
| `cues` | list of `Cue`: `cue_id` (`^[a-z][a-z0-9_-]*$`), `phrase`, `occurrence` ≥ 1 (default 1), `edge` start (default)/end, `action` ∈ show, highlight, transform, hide, reveal-answer, `element_id` |
| `expected_visuals` | list of strings |
| `critical_phrases` | list of strings (verified in transcript checks) |
| `answers_after` | optional id of an **earlier** question segment |

**`answers_after` rule:** "The answer segment declares `answers_after: question`. Its answer-reveal events cannot precede the protected response window." Enforced twice: at validation (the referenced segment must be earlier and end with a `think`/`pause-video` pause of > 0 s — "Question needs an explicit protected response window"; forward references fail — "An answer must reference an earlier question") and at assembly (`compose` raises "Premature answer" if the answer clip starts before the question's pause ends).

### 7.3 One segment from the implemented schema (message 12 §9, verbatim)

```yaml
segment_id: question
objective_id: count_atoms
claim_ids:
  - water-composition

text_template: >
  Two water molecules. How many hydrogen atoms altogether?
  Count each complete molecule before you answer.

direction:
  mode: curious
  target_wpm: 140
  emphasis:
    - each complete molecule

pause_after:
  kind: think
  seconds: 6
  prompt: Count hydrogen atoms in two separate water molecules.

expected_visuals:
  - Two water molecules; label elements, not totals.

critical_phrases:
  - Two water molecules
  - hydrogen

cues:
  - cue_id: show_molecules
    phrase: Two water molecules
    action: show
    element_id: molecule-pair
```

The complete five-segment plan is tabulated in `VOICE_IDENTITY_and_DELIVERY_GUIDE.md` §11.4.

### 7.4 Alignment records (`Alignment` / `AlignedWord`)

`segment_id`; `audio_sha256` and `transcript_sha256` (64 hex chars; the transcript hash is `digest(expanded spoken text)`); `method` ∈ `provider-timestamps | forced-aligner | human | synthetic-fixture`; `engine_version`; `words` = list of `{text, start ≥ 0, end > start}`, monotonic (overlap tolerance 1 ms). Any `synthetic-fixture` clip sets `contains_fixture: true`, which blocks release. "Synthetic alignment timestamps are test data, never claimed as acoustic alignment."

## 8. Provider translation strategy (message 12 §9 + `compiler.py`)

"This separation allows a voice provider to change without rewriting the lesson's educational structure."

| Provider | Message 12 rule | What the compiler emits |
|---|---|---|
| **ElevenLabs** | Map supported delivery cues into the selected model's actual controls. Preserve unsupported detailed direction for the reviewer. | v4: `POST /v1/text-to-dialogue`, `{"model_id","inputs":[{"text": <tag>+text,"voice_id"}],"language_code"}` — no speed/style/SSML. v3: `POST /v1/text-to-speech/{voice_id}`, `{"model_id","text","language_code"}`. multilingual_v2: no tags, no `as-IN`. Tags: curious → `[curious]`, deliberate/reassuring → `[calm]`. Full style kept in `editorial_style`. Warning: "WPM and detailed acting cues are editorial targets, not exact API controls." |
| **Cartesia** | Use its actual versioned request fields. A speed multiplier is a heuristic, not an exact words-per-minute guarantee. | `POST https://api.cartesia.ai/tts/bytes`, `Cartesia-Version` header required, `{"model_id","transcript","voice":{"mode":"id","id"},"language","output_format":{"container":"wav","encoding":"pcm_s16le","sample_rate":48000},"generation_config":{"speed": clamp(wpm/145, 0.6, 1.5),"volume":1}}`; "beta emotion disabled" |
| **Gemini** | Pass exact dialogue separately from `speech_metadata.style`. | `POST https://generativelanguage.googleapis.com/v1beta/interactions`; text verbatim in `content[0].text`, style (brief + mode + wpm + emphasis + notes) in `annotations[{type: speech_metadata, style}]`; `response_format: audio`; `speech_config[{voice}]`; "Unary 3.8 output is WAV: do not prepend another header. Streaming differs." |
| **OpenAI** | Keep the deprecated request only for migration inspection; implement and test the replacement separately. | `POST https://api.openai.com/v1/audio/speech`, `{"model","voice","input","instructions": style,"response_format":"wav"}` + "LEGACY MIGRATION FIXTURE ONLY…" warning; blocked when `production=True` |
| **Human performance** | Export the same segment text and direction as a recording sheet. | *Not implemented in code.* Produce it from the same plan — one row per segment (template below). |

**Human recording sheet template** (derived from the plan fields; not a source file):

| segment_id | Exact text (spoken form after `{{token}}` expansion) | Mode | Target wpm | Emphasis | Notes | Pause after (kind / s / task) | Critical phrases | Take # / accepted? |
|---|---|---|---|---|---|---|---|---|
| question | Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer. | curious | 140 | each complete molecule | — | think / 6 / Count hydrogen atoms in two separate water molecules. (insert in edit, not performed) | Two water molecules; hydrogen | |

Common to all providers: header values are `ENV:` templates; every request carries "Compiled offline; live behavior and pronunciation require separate approval."; `LICENSING_AND_SECURITY.md`: "All compiled API recipes are non-executing JSON. Replace actual IDs and verify current model contracts before writing a transport. A Runway preset name is not a direct vendor voice ID." Provider details, lifecycle and prices: `TTS_PROVIDER_COMPARISON.md`.

## 9. STEM pronunciation system (message 12 §10 + `configs/pronunciation.json`)

### 9.1 Do not send raw formulas and hope — four representations

**Scientific meaning → displayed notation → intended spoken form → accepted audio realization.**

| Display | Context-dependent spoken form |
|---|---|
| $I=neAv_d$ | "Current magnitude equals number density times elementary charge times cross-sectional area times drift-speed magnitude." |
| $mA$ | "milliamperes" |
| $MA$ | "megaamperes" |
| $10^{-3}$ | "ten to the power minus three" |
| $x^{-2}$ | "x to the power minus two" |
| $\sin^{-1}x$ | "inverse sine of x," where that notation is intended |
| $1/\sin x$ | "one divided by sine x" |
| $Na^+$ | "sodium ion with a positive charge," or the shorter approved form |
| $5'\rightarrow3'$ | "five-prime to three-prime" |
| $\Delta G$ | "delta G," with the meaning introduced separately |

These are **contextual authoring examples**, not one universal pronunciation dictionary. (Plain-text forms: I = neAv_d; mA; MA; 10^−3; x^−2; sin^−1 x; 1/sin x; Na⁺; 5′→3′; ΔG.) Note that several shipped lexicon entries choose slightly different wording for the same notation (e.g. `10⁻³` → "ten to the power of negative three"; `Na⁺` → "sodium ion with one positive charge"; `mA` → "milliampere") — the lexicon, not this table, is what the compiler uses.

**Identifier approach:** "The included library uses explicit identifiers such as `{{water_formula}}` rather than replacing every occurrence of a short symbol in arbitrary text." `expand()` replaces only `{{key}}` tokens; it never searches for raw symbols. Display, spoken and caption forms come from the same entry (`expand(..., form="display")` → `2H₂O`; spoken → "two water molecules").

### 9.2 What the dictionary must record

Each entry should contain: **subject, meaning, display form, locale, spoken form, allowed variants, model-specific phoneme/alias override, reviewer status, and accepted audio reference.**

Current shipped entry shape (`configs/pronunciation.json`): `{display, meaning, locales: {en-IN: {spoken, caption, editorially_checked, acoustic_approved}}}`. **Gap:** `subject`, `allowed variants`, `model-specific override` and `accepted audio reference` fields are specified in message 12 but not yet present in the file.

Critical distinctions include:

- Molarity versus molality.
- Milli versus mega.
- Minus signs, charges, exponents, and reciprocals.
- "Increase" versus "decrease."
- "Not," "only," "provided that," and other conditions.
- Biological directions and counts.
- Similar-sounding scientific names.

Do not automatically use English phonetic spelling as the final Assamese or Hindi representation.

### 9.3 Pronunciation overrides are model-specific

An IPA string, phoneme dictionary, alias dictionary, and SSML tag are not interchangeable mechanisms. ElevenLabs documents different pronunciation options across models; the adapter must verify what the selected endpoint actually accepts. For ExamLeaf, **an explicit spoken alias is the portable baseline**. Use provider phoneme features only after a successful acoustic test. (STEM Pronunciation Skill #9 rejects "inverse sine interpreted as reciprocal sine, mA/MA confusion, molarity/molality merging and unreviewed IPA.")

### 9.4 The shipped 40-entry English lexicon

Lexicon `version: en-reviewed-example-1` — review scope: "Original explicit text mappings checked during this build; no external teacher or acoustic approval." — 40 entries, all `en-IN`, all `editorially_checked: true`, all `acoustic_approved: false`; `caption` = `spoken` for every entry.

| # | Token `{{key}}` | Display | en-IN spoken (= caption) | Meaning / disambiguation note |
|---:|---|---|---|---|
| 1 | `{{water_formula}}` | H₂O | H two O | Water formula; prefer water in explanatory prose. |
| 2 | `{{two_waters}}` | 2H₂O | two water molecules | Coefficient multiplies the whole formula. |
| 3 | `{{hydrogen_peroxide}}` | H₂O₂ | hydrogen peroxide | Do not replace water with this to balance an equation. |
| 4 | `{{hydrogen_molecule}}` | H₂ | a hydrogen molecule | Diatomic identity. |
| 5 | `{{oxygen_molecule}}` | O₂ | an oxygen molecule | Diatomic identity. |
| 6 | `{{sodium_ion}}` | Na⁺ | sodium ion with one positive charge | Not neutral sodium. |
| 7 | `{{sulfate_ion}}` | SO₄²⁻ | sulfate ion with two negative charges | Ion charge is not a stoichiometric coefficient. |
| 8 | `{{iron_three}}` | Fe³⁺ | iron three ion | Formal oxidation state reading; explain positive three charge. |
| 9 | `{{moles_per_litre}}` | mol L⁻¹ | moles per litre | Not moles per kilogram. |
| 10 | `{{moles_per_kilogram}}` | mol kg⁻¹ | moles per kilogram | Specify solvent when describing molality. |
| 11 | `{{three_point_two}}` | 3.2 | three point two | Decimal point required. |
| 12 | `{{negative_power}}` | 10⁻³ | ten to the power of negative three | Do not read as ten minus three. |
| 13 | `{{microfarad}}` | µF | microfarad | µ prefix; context is capacitance, not coefficient of friction. |
| 14 | `{{milliampere}}` | mA | milliampere | Not megaampere. |
| 15 | `{{megaampere}}` | MA | megaampere | Not milliampere. |
| 16 | `{{speed_unit}}` | m s⁻¹ | metres per second | Speed, not acceleration. |
| 17 | `{{acceleration_unit}}` | m s⁻² | metres per second squared | Squared denominator. |
| 18 | `{{ohm_law}}` | V = IR | voltage equals current multiplied by resistance | Application conditions required. |
| 19 | `{{epsilon_zero}}` | ε₀ | epsilon nought | Context: vacuum permittivity. |
| 20 | `{{mu_zero}}` | µ₀ | mu nought | Context: vacuum permeability. |
| 21 | `{{tau}}` | τ | tau | Time constant context, not a generic reading for all symbols. |
| 22 | `{{delta_phi}}` | ΔΦ | change in magnetic flux | Conceptual expansion, not just Greek letter names. |
| 23 | `{{gradient}}` | dy/dx | the derivative of y with respect to x | Do not silently call it a fraction in every context. |
| 24 | `{{inverse_sine}}` | sin⁻¹x | the inverse sine of x | Chosen inverse-function meaning; never guess from syntax alone. |
| 25 | `{{reciprocal_sine}}` | 1/sin x | one divided by sine of x | Not inverse sine. |
| 26 | `{{log_ten}}` | log₁₀x | logarithm of x to base ten | Base explicit. |
| 27 | `{{natural_log}}` | ln x | natural logarithm of x | Base e. |
| 28 | `{{square_root_real}}` | √(x²) = \|x\| | the square root of x squared equals the absolute value of x | Real x; nonnegative principal square root. |
| 29 | `{{integral}}` | ∫₀¹ f(x) dx | the integral from zero to one of f of x, with respect to x | Bounds are ordered. |
| 30 | `{{degrees}}` | 30° | thirty degrees | Not radians. |
| 31 | `{{radians}}` | π/6 rad | pi over six radians | Angle unit explicit. |
| 32 | `{{five_prime}}` | 5′ | five prime | DNA/RNA end label, not five feet. |
| 33 | `{{three_prime}}` | 3′ | three prime | DNA/RNA direction label. |
| 34 | `{{dna}}` | DNA | D N A | Letters separated. |
| 35 | `{{rna}}` | RNA | R N A | Letters separated. |
| 36 | `{{atp}}` | ATP | A T P | Letters separated. |
| 37 | `{{heterozygous}}` | Aa | one uppercase A allele and one lowercase a allele | Explain genotype, do not pronounce aa ambiguously. |
| 38 | `{{diploid}}` | 2n | diploid, two n | Use ploidy in context; not DNA mass. |
| 39 | `{{mitosis}}` | mitosis | mitosis | Native voice pronunciation audition required. |
| 40 | `{{meiosis}}` | meiosis | meiosis | Must stay audibly distinct from mitosis. |

How to add a term: add an entry with `display`, `meaning` and a per-locale `{spoken, caption, editorially_checked, acoustic_approved}`; bump `version` and the plan's `lexicon_version` together (a mismatch blocks compile); reference it as `{{key}}`. Only segments that use the changed entry get a new `audio_cache_key` (`test_used_lexicon_entry_does_regenerate` / `test_unused_lexicon_entry_does_not_regenerate`). Hindi/Assamese mappings must be drafted and approved by native editors — "this package does not fabricate approved Assamese pronunciations."

## 10. ASR versus forced alignment (message 12 §11.2)

**ASR asks:** "What does another system think was spoken?"
**Forced alignment asks:** "Where does the supplied text fit in this audio?"

A forced aligner can attempt to place expected words even when the performance is imperfect. ASR can also normalize a mispronunciation into the intended term. Therefore:

> **Zero word error rate and a successful alignment do not prove correct STEM pronunciation.**

WhisperX documents language-resource requirements and limitations involving some numbers and symbols. Montreal Forced Aligner likewise relies on appropriate dictionaries and acoustic models. For independent Assamese transcription, Gemini's current transcription documentation lists Assamese and word-level timestamps. That is a relevant candidate, not an integration tested in this package.

`docs/Architecture.md` ("Independent checks"): Alignment validates where accepted words are placed; independent ASR asks what might actually have been spoken. Even zero ASR WER cannot certify a subtle mispronunciation. Critical negations, exponents, units, charges and biological directions require listening. Model-based quality scores, F0 ranges and speaker embeddings are triage; never automatically approve or reject a voice by accent/gender characteristics. faster-whisper: "Use audio-only decoding; do not supply expected answer text that biases away defects."

## 11. Sample-based timing and the occurrence-index rule (message 12 §11.3)

At 48 kHz:

$$
6\text{ seconds}=288{,}000\text{ samples}
$$

The starter inserts those samples explicitly. It does not ask the TTS engine to "pause for exactly six seconds." Store animation events against the accepted audio's sample positions, then convert once to output-frame time. Avoid repeated floating-point rounding or independent sentence-duration estimates.

Repeated phrases need an explicit occurrence index. "Highlight when the word 'current' is spoken" is ambiguous when it appears four times. → In the schema: `Cue.occurrence` (1-based) + `Cue.edge` (`start`/`end`). `test_second_occurrence_anchor`: two "two"s at 0.1 s and 0.4 s, `occurrence: 2` → 0.4 s. A missing occurrence fails loudly ("Missing cue occurrence").

Conversion used: `event.sample = clip.start_sample + round(word_time_s × 48000)`; `frame = round_half_up(sample × fps_num / (48000 × fps_den))` (exact fractions; 30 fps default, 30000/1001 supported). Example from `outputs/timeline.json` (NOT-SPEECH fixture): question clip 0–148,800; think pause 148,800–436,800 (= 288,000 samples); answer clip from 436,800; events `show_molecules` sample 7,200 / frame 5, `reveal_hydrogen` 444,000 / frame 278, `highlight_coefficient` 599,520 / frame 375, `reveal_retry` 1,449,120 / frame 906; total 1,677,120 samples = 34.94 s.

## 12. QA layers (message 12 §11.4)

| Layer | Automated checks | Human responsibility |
|---|---|---|
| Text | Missing conditions, unresolved terms, forbidden metadata in dialogue | Scientific meaning and natural teaching |
| Transcript | Added/omitted words, critical numbers and phrases | Ambiguous pronunciation and ASR mistakes |
| Signal | Clipping, DC offset, duration, unexpected silence | Audible distortion, joins, fatigue |
| Voice consistency | Flag unusual rate, level, or speaker changes | Judge acceptable performance variation |
| Alignment | Word order, monotonic timestamps, audio/transcript hashes | Inspect difficult anchors |
| Interaction | Answer hidden until response window ends | Confirm the task is fair and meaningful |
| Captions | Timing and text checks | Readability and accurate meaning |
| Final video | Automated defect report | Listen/watch the whole result |

Pitch tracks or model-generated "naturalness scores" may help triage. They should not automatically reject a voice because of accent or approve a lesson because it scores highly.

**Which automated checks exist in the starter today:** Text — unresolved/malformed `{{tokens}}` and stage tags in spoken text (contracts + `expand`). Transcript — `transcript_check` (surface WER, critical-phrase count mismatches; tested on dropped "not" and "Four"→"Two"). Signal — `signal_report` (clipping, DC offset, duration, silences with planned/unplanned flag). Alignment — `validate_alignment` + `Alignment` validators (hashes, word sequence, monotonic). Interaction — `answers_after` validation + "Premature answer". Captions — `write_vtt` (prototype; 6 aligned words per cue). Release — `release_report`. **Not implemented:** voice-consistency flags (rate/level/speaker change), caption readability checks, final-video defect report, any naturalness/pronunciation scoring. The user's requested automatic checks (message 11 §7) — missing words, inaccurate scientific pronunciation, awkward phrasing, inconsistent delivery, clipped audio, excessive silence, unnatural intonation, incorrect synchronization — map to the rows above; pronunciation, phrasing, delivery and intonation remain human judgements.

## 13. Mastering standard (message 12 §11.5 + `docs/Architecture.md`)

Proposed ExamLeaf starting target: **48 kHz mono, 24-bit archival WAV; approximately −16 LUFS integrated; true peak no higher than −1 dBTP.** This is an **internal production target**, not a universal platform requirement. FFmpeg supports two-pass loudness processing, but the final encoded delivery should be measured again. Architecture adds: "−16 LUFS integrated ±1, true peak <= −1 dBTP, mono 48k archival 24-bit WAV, delivery codec checked after final mux… Inspect unexpected silence while preserving explicit response windows. Never remove all breaths or flatten each sentence to identical loudness. Source/master hashes differ; mastering or trimming requires timing/hash reconciliation."

Avoid processing clean synthetic speech as though it were a noisy location recording. Excessive denoising can damage consonants; removing all breaths can sound unnatural. (Skill #13 rejects "unnecessary denoise/reverb/music and silenceremove applied across thinking windows"; Silero VAD: "Never remove protected think/write pauses automatically.")

Code: `master()` = measure → `loudnorm=I=-16:TP=-1:LRA=7` second pass with measured values and `linear=true` → `-ar 48000 -ac 1 -c:a pcm_s24le` → re-measure; pass = |I + 16| ≤ 1 and TP ≤ −0.9 dBTP. Fixture result (`outputs/mastering_qa.json`, NOT speech): before I −25.52 LUFS / TP −19.17; after I −15.99 LUFS / TP −9.65; `within_target: true`.

## 14. Music default

Keep background music **off during the main explanation initially**. Add music or sound effects only when their contribution survives a comprehension and listening-effort comparison. (`Before_After.md`: "No laughing sound effect." Guide: no "unrelated meme/audio stings".)

## 15. Human performance, consent, speech-to-speech, golden set, fallback (message 12 §12 + `LICENSING_AND_SECURITY.md` + guide)

1. **Performance reference corpus:** commission a performer to record **a calm explanation, prediction, difficult formula, understated joke, supportive correction, and confident recap.** It gives directors and reviewers a concrete standard; it does not necessarily need to become a cloned voice.
2. **Two different uses:** *performance reference* (demonstrates rhythm and intention) vs *identity reference* (creates or conditions a voice resembling that speaker). The latter requires specific permission and the provider's applicable verification process. Consent to record a lesson should not be silently treated as consent to create an indefinitely reusable synthetic identity. ElevenLabs' professional-cloning workflow has explicit verification requirements.
3. **Consent record (guide):** adult performer who knowingly permits the specific synthetic voice/use; document consent, allowed uses, territory, duration, payment, model permissions, revocation/future-use policy and deletion terms. `LICENSING_AND_SECURITY.md`: "Avoid collecting student recordings for voice cloning. Only adult performers who knowingly agree to the exact uses should supply performance or identity references." "Never convert a local audition-only flag into fictional consent." `AGENTS.md`: "Student and performer personal data are not test fixtures. No voice clone without appropriate consent/rights." Message 11: "Use only appropriately licensed or consented voices and voice samples." Store voice contracts/reference audio privately with retention/access control (`.gitignore` excludes `private_voice_references/`).
4. **When speech-to-speech is worthwhile:** passages where the actor's performance makes a material difference — a dry joke, difficult multilingual transition, careful contrast, or unusually subtle reassurance. Less compelling for every ordinary explanatory sentence. It can transfer performance into a target voice, but it does not automatically fix wrong science, missing words, or an incorrect pronunciation in the input.
5. **Consistency:** version the voice profile, pronunciation dictionary, reference passages, model, settings, and accepted samples. Keep a **"golden set"** of difficult passages; re-run it before model upgrades.
6. **Fallback rule:** do not silently replace a voice when a provider fails. **A fallback must be an approved voice/model combination, or the job should wait.** Consistency is not identical pitch and rhythm on every sentence.

## 16. Benchmark the voice before making it the brand — studies A/B/C (message 12 §14 + `docs/Audition_and_Evaluation.md`)

"Separate three experiments: (1) provider/voice selection with identical content and normalized playback level; (2) script-style comparison with matched science/time; (3) actual learning efficacy."

**A. Voice/provider audition.** Use identical passages, normalized playback levels, blinded provider names, and rotated order. Include connected explanations—not only isolated impressive sentences. The corpus should cover numbers, units, negation, scientific conditions, formula reading, Indian names, code-switching, a question, a correction, and a restrained joke. Use native teachers and language editors to identify **meaning-changing defects**, and students to rate clarity, listening effort, warmth, dignity, and preference.

- *Casting corpus (Audition doc):* the **40 written STEM term mappings** in `configs/pronunciation.json`, plus **12 connected passages (three per subject)**, including negation, a decimal, an exponent, a formula condition, Hindi/English switches, native Assamese text, questions, correction, joke and a quiet calculation. Prefer **3 viable voices per desired locale** and **2 repeat generations** of difficult passages. Evaluate **10-minute continuity** after short-listing. Start with a small diverse student/teacher listening panel; power an outcome experiment separately.
- *Rating roles:* Teacher — meaning-changing pronunciation defects (**release blocker**), scientific terms and conditions. Native language editor — accent, intelligibility and naturalness without imposing a stereotype. Students — listening effort, clarity, warmth, dignity and preference. Production reviewer — joins, loudness, silence, captions and reveal timing. Avoid weighted scoring that lets delightful acting compensate for wrong science.
- *Listening conditions:* low-cost phone speaker and ordinary earphones, at normal listening level, in quiet and realistic moderate noise. Randomize/rotate presentation order, blind provider names, give an accessible alternative. No intrusive attention/emotion surveillance.

**B. Script-style comparison.** Hold the science and study opportunity comparable. Compare a straightforward explanation with the Super Teacher version. The two Runway demonstrations produced here are useful for discussion, but **not** sufficient for a causal conclusion because several variables changed together. *Live connector evidence:* A task `f48aa57f-08e4-42b7-aa3a-4058c5fe2519` (textbook); B task `9c51652f-fe83-4d1f-be9e-05234654557c` (teacher-style); both requested Arjun, eleven_v3, speed 0.95, en; workspace credits 116 → 98 (18 credits; "not equivalent to an inferred ElevenAPI dollar price"). Local transfer could not be completed, so no waveform measurement, ASR/alignment, human listening or acoustic ranking is claimed. Signed URLs are deliberately not persisted.

**C. Learning evaluation.** Measure an independent question immediately and a fresh question later. Do not use preference, voice similarity, completion rate, or apparent confidence as the primary learning outcome. Use short listening panels first to find obvious problems, then a properly designed study for claims about learning effectiveness. A small panel is not enough to establish a modest examination-performance advantage. (Pilot designs across the project: `10_pilots_and_examples`.)

"This package's audio WAVs are explicitly labelled signal fixtures, not generated voices. Never play or market them as speech demonstrations."

## 17. Six-week integration roadmap (message 12 §15 + `docs/Implementation_Roadmap.md`)

| Phase | Build | Completion gate |
|---|---|---|
| **Week 1** | Voice casting, language-specific corpus, rights records | Approved primary voice per required locale |
| **Week 2** | One live provider transport, usage records, limits, recovery | Successful controlled synthesis and failure tests |
| **Week 3** | Independent ASR, actual alignment, critical-term checks | Manually verified timing and pronunciation samples |
| **Week 4** | Integrate with existing renderer; complete four subject pilots | Full academic/native-language/listening approval |
| **Weeks 5–6** | Controlled 20–30-lesson batch, dashboard and queue | Predictable accepted-output cost and defect rate |

Detail per phase (`docs/Implementation_Roadmap.md`):

- **Week 1 — casting and reference contracts:** Approve the academic/spoken source pipeline and build 12 connected listening passages plus the 40 written term entries. Audition 3 suitable voices in each needed language using identical content and normalized playback level. Establish actual voice rights and model IDs. Teacher/native reviewers must reject meaning-changing pronunciations regardless of acting preference. Student pilot feedback is usability evidence, not proof of examination gains.
- **Week 2 — one live provider transport:** Implement one approved Eleven v4 or Gemini 3.8 transport after account access is confirmed. Keep synthesis out of the agent's direct shell. Persist actual request/response format, provider ID and billed usage. Add explicit per-run spending limits, concurrency limits, timeout reconciliation, HTTP error classes and no blind paid retries. Do not use the deprecated OpenAI fixture for new production.
- **Week 3 — independent transcription and real alignment:** Add an independent ASR route with verbatim settings where supported. Reject language resources that are unavailable rather than inventing word timing. Import actual forced alignment and verify against a manually annotated sample. English, Hindi and Assamese require separate transcript normalization tests. Manually listen to scientific critical terms and numbers. Test omitted words, repeated phrases, code switching and planned pauses.
- **Week 4 — video integration and full pilots:** Feed timeline events to the existing ExamLeaf scene adapters. Let natural narration determine scene duration. Regenerate only affected segments; update hashes and approvals. Complete four genuinely narrated subject pilots, not padded versions of the timing fixtures. Check caption answer leakage, phone readability, joins and final encoded audio.
- **Weeks 5–6 — controlled batch and operations:** Run 20–30 complete lessons with academic/native-language/final listening approval. Measure accepted audio cost, retake fraction, human minutes and synchronization defects. Add durable queue, authenticated approval service and dashboard only around validated contracts. Expand catalogue when the cost and quality distribution—not just the best demo—are acceptable.
- **Staffing and boundaries:** Assumes dedicated engineering time and available subject/language reviewers, not an unattended guarantee. Original 15 Skills are editorial capabilities/subtasks, not 15 parallel paid LLM passes. Preserve existing science review rather than duplicating or replacing it. Maintain a central content corpus, library, model lifecycle ledger and corrections process.

"The current starter completes portions of the contracts, timing, caching, request compilation, and signal QA. It does not substitute synthetic test timestamps for real alignment or claim that the fifteen Skills have already operated as autonomous agents."

## 18. Next engineering steps (`README.md`, verbatim)

1. Cast native-appropriate licensed voices and approve the corpus.
2. Implement one provider transport, persist actual usage/jobs and test failure/recovery.
3. Import independent ASR and actual forced alignment; validate numbers and language resources.
4. Connect timeline.events to the existing renderer; re-align or remap after any audio trim/time change.
5. Complete four narrated subject pilots with full academic, native-language, caption and listening reviews.
6. Only then expand the batch queue and commercial catalogue.

## 19. Safety and rights boundaries (`AGENTS.md`, `CLAUDE.md`, `LICENSING_AND_SECURITY.md`, `docs/Architecture.md`)

- Sidecar, not a replacement renderer. Keep script authoring, provider access and release roles separate. Public Skills supply package guidance; ExamLeaf contracts own science and pedagogy.
- No network execution or paid synthesis from the offline CLI. "Provider request compilation is not a successful integration." "Verify current exact endpoint contracts before production transport work."
- No third-party source repositories, model weights, font binaries, performer recordings, credentials, or signed temporary artifact URLs are bundled. Confirm each dependency, chosen model weight and voice licence before commercial use.
- Keep model/provider keys only in an allowlisted worker secret store. Research agents and scriptwriters should not have publishing or billing credentials. Do not run unreviewed curl-pipe-shell installers. Skills are untrusted instruction/code packages, not permission boundaries.
- Cache and hash controls here are local demonstrations. Production requires an authenticated reviewer and approval service, encrypted storage and appropriate privacy/retention controls.
- Source text and Skill repositories are untrusted input. No arbitrary scripts from retrieved documents, no blanket home-directory mounts or editor secrets in rendering workers. No student voice uploads are needed for these lesson-production tasks. Audio authorization and student progress data belong in separate services.

## 20. Reference: what is in `outputs/` (all produced offline; WAVs are NOT speech)

| File | Content |
|---|---|
| `eleven_v4_requests.json`, `eleven_v3_requests.json`, `cartesia_snapshot_requests.json`, `gemini_38_requests.json`, `openai_snapshot_requests.json` | Compiled (never sent) requests for the 5-segment teacher plan, one file per profile |
| `request_preview.json` | Output of the README `compile` example (identical to `gemini_38_requests.json`) |
| `fixtures/{question,answer,repair,retry,check}_signal_NOT_SPEECH.wav` | 24 kHz tone fixtures, one per segment |
| `fixture_alignment.json` | Synthetic word timings (`method: synthetic-fixture`, `engine_version: fixture-1-NOT-forced-alignment`) |
| `timing_fixture_NOT_SPEECH.wav` / `timeline.json` / `fixture_captions.vtt` | Composed 48 kHz 24-bit track (34.94 s), timeline with clips/pauses/events/captions (`contains_fixture: true`), 22 WebVTT cues |
| `signal_qa.json` | 34.94 s, 48 kHz, mono, peak −19.17 dBFS, RMS −26.18 dBFS, 0 clipped samples, 2 planned silences |
| `master_fixture_NOT_SPEECH.wav` / `mastering_qa.json` | Two-pass master of the fixture; within target |
| `release_blockers.json` | `release_allowed: false` + 9 blockers |
| `cost_summary.json` | Five-method cost table (USD, one month, narration only) — see `TTS_PROVIDER_COMPARISON.md` §6 |
| `environment.json` | Python 3.13.5, Linux, numpy 2.3.5, soundfile 0.13.1, pydantic 2.13.5, scipy 1.17.0; "Offline signal tests; no speech model downloaded or executed locally." |
| `tests.txt` | `57 passed in 3.17s` (delivered run; not regenerated after the 15 Oct 2026 change) |
