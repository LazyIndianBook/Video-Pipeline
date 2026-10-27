# 05 — Narration System (AI narration, voice acting and teaching-voice production)

## 1. What this section is and where it came from

This section holds everything the ExamLeaf research project produced about **narration**: how the "Super Teacher" voice should sound and behave, which speech technologies to use, how narration is written, directed, pronounced, generated, checked, aligned to animation and mastered, what it costs for 1 / 100 / 1,000 ten-minute videos, and a working offline Python starter with 15 custom Claude/Codex Skills.

The narration system is a **sidecar to the ExamLeaf Video Engine** (`04_video_engine`): it integrates through manifests and a sample-accurate timeline (`narration_plan_uri`, `narration_manifest_sha256`, `timeline.events`), not by changing the engine's scientific renderers.

**Provenance (all copied, nothing under `00_source/` modified):**

| Placed here | Came from | Verification |
|---|---|---|
| `prompt/11_USER_prompt_narration_system.md` | `00_source/chatgpt_transcript/messages/11_USER_prompt_narration_system.md` (the user's brief, 8,893 chars) | `cmp` identical |
| `FULL_narration_system.md` | cleaned full text of `00_source/chatgpt_transcript/messages/12_ASSISTANT_narration_system.md` (ChatGPT's answer, 45,047 chars, research checked 13 Oct 2026) | word-level diff vs raw: only the provenance comment, 26 removed citation tokens (listed in its Appendix A), 5 re-pointed sandbox links and the scraper footer (moved to Appendix B) differ |
| `narration_system_v1/` | `cp -R` of `00_source/extracted/ExamLeaf_Narration_System/ExamLeaf_Narration_System/` (the unzipped `ExamLeaf_Narration_System.zip`) | 123 files; `diff -rq` identical; all 122 files listed in its `DELIVERY_MANIFEST.json` match their SHA-256 *(15 Oct 2026: true at delivery; two files now differ from the manifest on purpose, `src/examleaf_narration/pronunciation.py` and `tests/test_narration.py`, see `narration_system_v1/CHANGES.md`; the pristine copy is `00_source/extracted/`)* |
| — | `00_source/downloads/ExamLeaf_Narration_System/{docs/Voice_Identity_Guide.md, research/Public_Narration_Directory.md, examples/Before_After.md}` | each `cmp`-identical to the zip copy, so not duplicated here |
| — | Narration workbook sheets as CSV: `00_source/spreadsheets_as_csv/ExamLeaf_Narration_Cost_Model__{Inputs,Methods,Provider_Tariffs,Skills,Sources,Summary}__{values,formulas}.csv` | used for the cost tables in `TTS_PROVIDER_COMPARISON.md`; the `.xlsx` itself is in `narration_system_v1/` |

## 2. Contents

```text
05_narration_system/
├── README.md                                  this file
├── FULL_narration_system.md                   cleaned full text of message 12 (all 15 sections, tables, formulas, YAML)
├── prompt/
│   └── 11_USER_prompt_narration_system.md     the original request (verbatim)
├── INSTRUCTIONS_narration_pipeline.md         how to run the starter + the full production pipeline spec
├── VOICE_IDENTITY_and_DELIVERY_GUIDE.md       Super Teacher voice, modes, emotions, pacing, interaction, worked example, templates
├── TTS_PROVIDER_COMPARISON.md                 ElevenLabs / Gemini / Cartesia / OpenAI / open-source, languages, tariffs, cost tables
├── SKILLS_INDEX_narration_15.md               the 15 custom Skills + existing-engine mapping + public Skills directory (28)
├── ELEVENLABS_SETUP_2026-10-16.md             live ElevenLabs check (retired for narration 27 Oct 2026, RD-55)
├── local_voice_voxcpm2/                       the voice system in use since 27 Oct 2026 (PD-29, RD-55)
│   ├── SETUP.md                               what is installed where, founder steps, commands, measurements
│   ├── SOURCE_Local_Voice_and_Animated_EdTech_Production_on_M1_Pro.md   the founder's plan (verbatim)
│   └── studio/                                the studio's own files: narrate.py (audition) and the designed test voices
└── narration_system_v1/                       the complete offline starter repo (123 files)
```

| Item | What it is |
|---|---|
| `README.md` | Section overview, provenance, status, how to use, cross-references, gaps |
| `FULL_narration_system.md` | Message 12 in full: launch stack; ElevenLabs v4 / Cartesia Sonic / Gemini 3.8 TTS / OpenAI deprecation; language table; open-source table + self-hosting verdict; public Skills reuse + installation policy; 15 custom Skills table + integration; voice identity + emotional delivery; pacing + Dora structure + improved phrases; textbook-vs-teaching script; structured YAML segment + provider translation; STEM pronunciation system; synchronization, ASR vs alignment, sample timing, QA layers, mastering; human performance / STS / consistency; costs; benchmark studies A/B/C; repo structure, run commands, 6-week roadmap; final recommendation; the ChatGPT conversation summary. Formatting-only cleanup |
| `prompt/11_USER_prompt_narration_system.md` | The user's 8-part brief and the 10 required deliverables |
| `INSTRUCTIONS_narration_pipeline.md` | Prerequisites; setup; every CLI command (incl. why `release-check` exits 2); what each `src` module does; the test suite (57 at delivery; 15 Oct 2026: 60 cases, 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg); the 11-step production sequence with per-step status; narration data format spec; per-provider translation incl. human recording sheet; pronunciation dictionary spec + all 40 lexicon entries; ASR vs alignment; sample timing; QA layers; mastering; music; human performance/consent/golden set/fallback; benchmark studies A/B/C; 6-week roadmap; next engineering steps; safety; `outputs/` reference |
| `VOICE_IDENTITY_and_DELIVERY_GUIDE.md` | Defining brief; personality rules + example lines; six delivery modes (with the exact provider style text); emotion-by-situation table; pacing table; Dora-style structure; improved-phrases table; humour/analogy/language rules; human performance; evidence limits; full textbook-vs-ExamLeaf example (both renderings + `teacher.json` table + fixture timing); reusable prompts and templates |
| `TTS_PROVIDER_COMPARISON.md` | Launch stack; each commercial provider with all caveats; what the compiler actually sends per provider; language-support and locale-admission tables; open-source table + licences + self-hosting verdict; ASR/alignment tools; tariff table; worked cost calculations; five-method 1/100/1,000-video costs with formula breakdown; admission checklist |
| `SKILLS_INDEX_narration_15.md` | Master table (#, name, input→output, safeguard, folder, owner, files); per-Skill purpose, steps, gates, cost/fallback, eval case, handoff template, implementing code; shared boilerplate; `existing_engine_skill_mapping.json` as a table; install/use steps; public Skills reuse + policy; full 28-entry public directory |
| `narration_system_v1/` | The starter itself — see §2.1 |

### 2.1 `narration_system_v1/` — per-directory description (123 files)

| Path | Files | What it contains |
|---|---:|---|
| *(root files)* | 8 | `README.md` (status, run commands, next steps), `AGENTS.md` (agent rules: sidecar, no network, no fixture→release, run pytest), `CLAUDE.md` (role separation), `LICENSING_AND_SECURITY.md` (rights/secrets/consent boundaries), `DELIVERY_MANIFEST.json` (date 2026-10-13, "57 passed", `neural_tts_local: false`, `human_voice_approval: false`, bytes + SHA-256 of the other 122 files), `pyproject.toml` (package `examleaf-narration` 0.1.0, Python ≥ 3.11, CLI `examleaf-voice`), `.gitignore`, `ExamLeaf_Narration_Cost_Model.xlsx` (sheets Summary, Inputs, Methods, Provider_Tariffs, Skills, Sources) |
| `configs/` | 8 | 5 provider profiles — `eleven_v4.json`, `eleven_v3.json`, `cartesia_snapshot.json` (Sonic 3.5 snapshot), `gemini_38.json` (voice Kore), `openai_snapshot.json` (legacy migration fixture); `pronunciation.json` (40 en-IN STEM mappings, not acoustically approved); `narration.schema.json` (JSON Schema of the NarrationPlan); `existing_engine_skill_mapping.json` (8 existing engine Skills → 15 narration Skills) |
| `docs/` | 7 | `Architecture.md` (production graph, what is/isn't implemented, engine hookup, segments, independent checks, worker design, audio release, safety), `Audition_and_Evaluation.md` (3 experiments, casting corpus, rating roles, Runway evidence), `Costs_and_Methods.md` (five-method costs and assumptions), `Implementation_Roadmap.md` (weeks 1–6), `Provider_Lifecycle.md` (OpenAI/ElevenLabs/Cartesia/Gemini lifecycle + admission checklist), `Reusable_Prompts.md` (teacher, naturalizer, voice-direction, QA prompts), `Voice_Identity_Guide.md` (Super Teacher voice) |
| `examples/` | 4 | `teacher.json` (5-segment interactive plan), `textbook.json` (1-segment textbook plan), `claims.json` (3 OpenStax-sourced claims), `Before_After.md` (the two scripts with directions) |
| `outputs/` | 22 | 17 files + `fixtures/` (5): compiled requests for each of the 5 profiles + `request_preview.json`; `fixture_alignment.json`; `timeline.json`; `fixture_captions.vtt`; `signal_qa.json`; `mastering_qa.json`; `release_blockers.json`; `cost_summary.json`; `environment.json`; `tests.txt`; `timing_fixture_NOT_SPEECH.wav`, `master_fixture_NOT_SPEECH.wav`, and `fixtures/{question,answer,repair,retry,check}_signal_NOT_SPEECH.wav` — **tone signals, not speech** |
| `research/` | 3 | `Public_Narration_Directory.md` (28 public Skills/APIs/models/tools + install protocol + documentation drift), `public_directory.csv` (same, tabular), `custom_skills.csv` (source rows for the 15 Skills) |
| `scripts/` | 2 | `build_examples.py` (regenerates lexicon, examples, profiles, requests, schema, fixtures, timeline, QA, master, release report), `build_docs.py` (regenerates research files, Skills, mapping, AGENTS/CLAUDE, 4 docs and an older README variant) |
| `skills/` | 60 | 15 Skill folders × 4 files (`SKILL.md`, `evals/cases.json`, `references/README.md`, `templates/handoff.json`) — see `SKILLS_INDEX_narration_15.md` |
| `src/examleaf_narration/` | 8 | `__init__.py`, `contracts.py` (Pydantic contracts), `pronunciation.py` (`{{token}}` expansion, normalisation), `compiler.py` (offline provider requests, cache keys), `cache.py` (hashes, atomic JSON, job-state decisions), `timeline.py` (sample-index composition, cues, frames, VTT), `qa.py` (transcript/signal/loudness/master/release), `cli.py` |
| `tests/` | 1 | `test_narration.py` — 49 test functions = 57 cases at delivery; *15 Oct 2026: 52 functions = 60 cases (58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg)* |

## 3. How to use this section (step by step)

1. **Read the brief and the answer:** `prompt/11_USER_prompt_narration_system.md`, then `FULL_narration_system.md` (start with "What was actually implemented and tested" — reproduced in §4 below).
2. **Fix the voice before anything else:** read `VOICE_IDENTITY_and_DELIVERY_GUIDE.md` together with the persona in `03_super_teacher_framework`. Use its templates (§12) when writing or directing scripts.
3. **Choose providers to audition:** `TTS_PROVIDER_COMPARISON.md` §1–§4 (Eleven v4 first, Gemini 3.8 Flash TTS as main alternative, Cartesia Sonic as challenger; OpenAI legacy TTS is migration-only; self-host only when one of the four triggers is demonstrated).
4. **Budget:** `TTS_PROVIDER_COMPARISON.md` §5–§6 for narration-only costs; do not double-count review time with the full-video budget in `08_cost_models`.
5. **Run the starter offline:** follow `INSTRUCTIONS_narration_pipeline.md` §1–§3 on a *copy* of `narration_system_v1/` (venv → `pip install -e '.[test]'` → `build_examples.py` → `pytest -q` (57 passed at delivery; *15 Oct 2026: 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg*) → `validate` → `compile` → `qa` → `release-check`, which deliberately exits 2).
6. **Install only the Skills a task needs** into `.claude/skills/` or `.agents/skills/`: `SKILLS_INDEX_narration_15.md` §6. The existing engine Skills they plug into are in `06_skills_library`.
7. **Author lessons in the narration format** (`INSTRUCTIONS_narration_pipeline.md` §7) with STEM terms as `{{lexicon_key}}` (§9); validate with `cli validate`.
8. **Run the six-week integration** (`INSTRUCTIONS_narration_pipeline.md` §17): cast and approve voices → one live transport → independent ASR + real alignment → hook `timeline.events` into the engine's scene adapters (`04_video_engine`) and run four subject pilots → 20–30-lesson batch. The overall production run-book is in `07_end_to_end_pipeline_instructions`; pilot/listening-test designs in `10_pilots_and_examples`.
9. **Benchmark before branding the voice:** studies A/B/C (`INSTRUCTIONS_narration_pipeline.md` §16); evidence background in `02_learning_psychology` and `09_research_and_evidence`.

## 4. Verified vs proposed / untested (exactly as the sources state)

### 4.1 Message 12 — "What was actually implemented and tested"

| Item | Status |
|---|---|
| Structured narration contracts and provider-request compiler | Implemented locally |
| Fifteen dedicated ExamLeaf narration Skills | Written, with evaluation cases; **not agent-evaluated** |
| Forty explicit English STEM pronunciation mappings | Included; **not acoustically approved** |
| Sample-accurate timeline, protected thinking pauses, and animation markers | Implemented and tested |
| Cache invalidation, transcript comparison, signal analysis, and two-pass mastering | Implemented within the starter |
| Local tests | **57 passed** (at delivery). *15 Oct 2026: 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg* |
| Actual voice demonstrations | **Two speech auditions generated through your connected Runway account**, using 18 workspace credits |
| Local processing of those generated voices | Not completed; the audio assets were not transferred into this runtime |
| Local speech-quality or pronunciation benchmark | **Not performed** |
| Local audio fixtures | Real WAV test files, explicitly labelled **NOT SPEECH** |
| Complete production service | Not yet: authenticated synthesis transport, actual ASR/alignment execution, and authenticated approval remain to be integrated |

"The two generated auditions compare textbook-style wording with a more interactive teaching rendition using the same requested voice, model, and speed. **They differ in wording, length, and expressive instructions, so they are demonstrations—not a controlled A/B experiment.**" "Research was checked on **13 October 2026**. Pricing, model lifecycle, documented capabilities, original design recommendations, and local test results are distinguished below."

### 4.2 Further status statements in the sources

- **Proposed, not validated:** the launch stack ("a ranked implementation recommendation, not a claim that I have listened to and benchmarked all three commercial models"); the emotional-delivery table ("proposed performance directions, not universal psychological prescriptions"); pace/pause numbers ("ExamLeaf starting specifications to test"); mastering target ("an internal production target, not a universal platform requirement"); all cost inputs ("editable planning assumptions, not quotations or measured TTS benchmarks"); Eleven v4 price (not known — v2/v3 reference used).
- **Research-read, not live-tested:** every entry in the 28-item public directory; Gemini 3.8 ("Neither has been live-synthesized here"); Cartesia Sonic 3.6 (recipe is the 3.5 snapshot); OpenAI `gpt-realtime-2.1-mini` (not implemented); Gemini Assamese transcription; WhisperX / faster-whisper / MFA / Silero / librosa ("Not installed here").
- **Implemented but offline only:** request compilation ("sends zero network requests"); FFmpeg two-pass mastering ("executed on synthetic signal fixtures here. No speech-quality claim").
- **Not implemented** (`docs/Architecture.md`): authenticated provider REST transport, provider-side forced-alignment execution, independent ASR inference, locale-specific Indic ASR normalization, distributed queue, identity-authenticated reviewer service, fully mastered approved narration lesson or student outcome tests. Also: human recording-sheet export, voice-consistency checks, Hindi/Assamese lexicon entries.
- **Release:** always blocked by design (`release-check` exits 2).
- **This organising pass:** code and tests were read, not executed; the "57 passed" figure is the sources' own record (`outputs/tests.txt`) and matches a static count of the test file (49 functions, 57 parametrised cases). *15 Oct 2026: the suite was executed on this Mac after the Indic fix: 52 functions = 60 cases, 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg (the two failures, `test_silent_loudness_rejected` and `test_two_pass_master_real_signal_file`, shell out to `ffmpeg`, which is not installed here). The loudness/mastering gate is verified only where FFmpeg is installed.*

## 5. Cross-references

| Section | Relationship |
|---|---|
| `01_business_model` | Narration cost per video feeds unit economics |
| `02_learning_psychology` | Retrieval practice, enthusiasm and cognitive-load evidence behind the pacing/interaction rules |
| `03_super_teacher_framework` | The Super Teacher persona this voice performs; its balancing-equations sample script matches the worked example here |
| `04_video_engine` | The engine/renderer that consumes `timeline.events` and the narration manifest fields |
| `06_skills_library` | Existing engine Skills (`examleaf-super-teacher`, `examleaf-voice-direction`, `examleaf-voice-synthesis`, `examleaf-alignment-localize`, `examleaf-audio-caption-qa`, …) that delegate to the 15 narration Skills |
| `07_end_to_end_pipeline_instructions` | Where the narration sidecar sits in the full production run |
| `08_cost_models` | Whole-project workbooks; avoid double-counting review costs |
| `09_research_and_evidence` | Sources and evidence boundaries |
| `10_pilots_and_examples` | Four subject pilots, listening panels, learning evaluation |

## 6. Gaps and inconsistencies noticed (recorded, not resolved)

1. The Runway auditions themselves are not in the project (never transferred; signed URLs deliberately not kept). Only task IDs and credit usage are recorded.
2. The working example's spoken text in `teacher.json` expands `{{water_formula}}` to "H two O", while message 12 and `Before_After.md` say "Changing **water** into hydrogen peroxide"; message 12 also splits "Keep the given formulas fixed…" into its own FOCUSED beat, while the files keep it in the LIGHT segment.
3. Message 12's pronunciation examples differ slightly in wording from the shipped lexicon (e.g. "ten to the power minus three" vs "ten to the power of negative three"); the lexicon lacks the subject / allowed-variants / model-override / accepted-audio fields message 12 says it must record, and has no Hindi or Assamese entries.
4. `scripts/build_docs.py` would overwrite `README.md` with an older variant; `scripts/build_examples.py` rewrites `outputs/environment.json` without the `pydantic`/`scipy` keys present in the shipped copy.
5. The CLI `qa` command cannot pass protected pause intervals, so it reports every silence as unplanned.
6. The source repo's own prose has missing spaces ("Created13October2026", "exits2"); the copies in `narration_system_v1/` are kept verbatim, and the consolidated docs here respace them.


## Local change log (after delivery)

- **2026-10-15:** Indic tokenization fixed in `narration_system_v1/src/examleaf_narration/pronunciation.py` (`normalized_words`); 3 regression tests added; suite 58 passed, 2 FFmpeg-only environmental failures. Details in `narration_system_v1/CHANGES.md`. The delivered copy under `00_source/` is unchanged.
- **15 Oct 2026 (audit addendum, `14_end_to_end_audit/AUDIT_REPORT_2026-10-15.md` minor "Stale test counts and integrity claims"):** test counts in this README updated to 58 passed + 2 FFmpeg-environment failures here; 60 with FFmpeg. Two files intentionally differ from `DELIVERY_MANIFEST.json`: `src/examleaf_narration/pronunciation.py` and `tests/test_narration.py` (reason and diff summary in `narration_system_v1/CHANGES.md`); the manifest itself was not regenerated and still records the delivered state ("57 passed"). The transcript comparator `normalized_words()` is no longer English-only: it is a category-based scanner (Unicode letters/marks/numbers; ZWJ/ZWNJ transparent) and is Indic-safe for Devanagari and Bengali–Assamese script. It is still a surface comparator, not a linguistic tokenizer; native review is still required.

*16 Oct 2026:* `ELEVENLABS_SETUP_2026-10-16.md` records the live check of Eleven v4, the dialogue-route limits, the hosted MCP registration and the founder steps that remain (onboarding, API key, OAuth, plan).

*27 Oct 2026:* the founder replaced ElevenLabs with a local voice system: VoxCPM2 through MLX Audio, cloned from the founder's own voice (PD-29, RD-55). `local_voice_voxcpm2/` holds the founder's plan (verbatim) and `SETUP.md`. The provider comparison (§3 step 3 above, `TTS_PROVIDER_COMPARISON.md`) is kept as research history.
