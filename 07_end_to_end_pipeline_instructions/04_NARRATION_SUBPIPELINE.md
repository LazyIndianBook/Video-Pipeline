# 04 · Narration sub-pipeline: the complete audio procedure

> **27 Oct 2026 (RD-55, PD-29): the voice system is decided.** Voice-over is local VoxCPM2 through MLX Audio, cloned from the founder's own voice, and transcription and alignment use local Whisper small.en. ElevenLabs and the other cloud providers below are research history, not candidates. Operating steps: `../05_narration_system/local_voice_voxcpm2/SETUP.md`. The rest of this procedure (rights, pronunciation, segmenting, QA, approvals) still applies.

**Scope.** Stage S10–S11 of [`03_PER_LESSON_PRODUCTION_PROCEDURE.md`](03_PER_LESSON_PRODUCTION_PROCEDURE.md) in full: casting and rights, the performance reference corpus, the pronunciation dictionary, the structured narration plan, per-provider request compilation, generation, independent transcription, alignment, protected pauses, captions, mastering, QA, approvals, fallback, golden set, benchmark studies, Assamese/Hindi gates and cost pointers.

**Status (verbatim from the sources).** "**Status: offline-tested sidecar, not a finished production speech service.**" 57 local tests passed on NOT-SPEECH signal fixtures. *[15 Oct 2026: the suite is now 60 cases: 58 pass + 2 FFmpeg-environment failures on a machine without FFmpeg, 60 with FFmpeg; see 01 §3.2 N4.]* Request compilation "sends **zero network requests**". Authenticated synthesis transport, ASR/alignment execution and authenticated approval are **[NOT DONE]**. The only real voice outputs are two Eleven v3 auditions and one Multilingual v2 probe through a connected Runway account (27 workspace credits in total), never downloaded, listened to, aligned or ranked; "they are demonstrations — not a controlled A/B experiment". No voice has been cast; the example plan's rights status is `audition-only`. The 40-term lexicon is `editorially_checked` but **not acoustically approved**, and has no Hindi or Assamese entries.

**Sources:** [`05_narration_system/INSTRUCTIONS_narration_pipeline.md`](../05_narration_system/INSTRUCTIONS_narration_pipeline.md), [`05_narration_system/FULL_narration_system.md`](../05_narration_system/FULL_narration_system.md), [`05_narration_system/VOICE_IDENTITY_and_DELIVERY_GUIDE.md`](../05_narration_system/VOICE_IDENTITY_and_DELIVERY_GUIDE.md), [`05_narration_system/TTS_PROVIDER_COMPARISON.md`](../05_narration_system/TTS_PROVIDER_COMPARISON.md), [`05_narration_system/narration_system_v1/docs/`](../05_narration_system/narration_system_v1/docs/Architecture.md) (Architecture, Audition_and_Evaluation, Provider_Lifecycle, Reusable_Prompts, Implementation_Roadmap), `src/examleaf_narration/*.py`.

All commands run from `narration/` in the canonical repository (01 §4) with the venv active.

---

## 1. Interfaces with the engine

| Direction | Artefact | Rule |
|---|---|---|
| In | GA-approved script bundle; `NarrationPlan` draft (`script/narration_plan.json`) referencing approved claim IDs | "Approved source-linked claims → teacher draft → … → academic script approval" precedes any synthesis |
| In | Lesson `academic_edition`, locale, `source_claim_manifest` path | Plan-level fields |
| Out | Accepted segment WAVs, `alignment.json`, `timeline.json` (events with cue, element, action, global sample, output frame; clips; pauses; captions) | "Pass accepted `timeline.events` to scene adapters"; "Replace estimated scene lengths with measured clip/hold intervals" |
| Out | `narration_plan_uri`, `narration_manifest_sha256` added to the lesson manifest | Any audio change → new hash → GF invalid |
| Out | Mastered master + measurements; audio approval evidence | Release requires audio-specific approval evidence, "rather than trusting the narration agent's own conclusion" |
| Never | Changes to scientific renderers | "Leave existing Python scientific verification and renderer adapters unchanged." |

Skill ownership (authoritative delegation map; see 01 §6.2): VE voice-direction → NA **voice-acting-director**, **pacing-controller**, **stem-pronunciation**; VE voice-synthesis → NA **tts-provider-adapter**; VE alignment-localize → NA **speech-animation-synchronizer**, **multilingual-director**; VE audio-caption-qa → NA **audio-production-engineer**, **narration-quality-reviewer**; VE observability-cost → NA **cost-regeneration-optimizer**. "Fifteen capabilities — not fifteen mandatory LLM calls for every segment."

---

## 2. N1 · Voice casting, rights records and the performance reference corpus (once per locale; narration week 1)

**Do.**
1. **Fix the voice brief.** "A highly competent teacher who is warm toward the learner, precise about the science, and occasionally amused by the problem." Performance brief: clear Indian English for the English edition, authentic Hindi or Assamese for dedicated editions, moderate warmth, attentive rhythm, confident sentence endings, no shouting, exaggerated breathiness or constant excitement. **One stable lead voice per course/locale**; no permanent second character; never impersonate Professor Dave, Sal Khan, a celebrity or a local teacher. "Neither gender nor a specific pitch is an established learning optimum." Cast by intelligibility and student listening effort, not stereotype.
2. **Build the casting corpus:** the 40 written STEM term mappings (`configs/pronunciation.json`) + **12 connected passages, three per subject**, covering negation, a decimal, an exponent, a formula condition, Hindi/English switches, native Assamese text, a question, a correction, a restrained joke and a quiet calculation; numbers, units, Indian names.
3. **Audition 3 viable voices per needed locale**, 2 repeat generations of difficult passages, identical content, **normalized playback level**, blinded provider names, rotated order, low-cost phone speaker and ordinary earphones, quiet and moderate noise; evaluate **10-minute continuity** after short-listing (study A, §15).
4. **Record rights.** Production compile requires `rights_status` ∈ `licensed-stock` or `consented-custom`. Store the licence or the written consent (adult performer; allowed uses, territory, duration, payment, model permissions, revocation/future use, deletion) in `private_voice_references/` with access control. "Never convert a local audition-only flag into fictional consent." A Runway preset name is not a direct vendor voice ID.
5. **Commission a performance reference corpus** from a performer: "a calm explanation, prediction, difficult formula, understated joke, supportive correction, and confident recap." It gives directors and reviewers a standard; it "does not necessarily need to become a cloned voice". **Performance reference** (rhythm and intention) ≠ **identity reference** (creating or conditioning a voice like that speaker), which needs specific permission and the provider's verification process (ElevenLabs professional cloning has explicit verification requirements). Consent to record a lesson is not consent to an indefinitely reusable synthetic identity. **Never use student recordings.**

- **Owner:** NA **voice-acting-director** (direction records, audition list) under VE voice-direction; humans decide.
- **Output:** `VoiceIdentity` record (`identity_id`, `version`, `brief`, `locale` ∈ en-IN / hi-IN / as-IN, `rights_status`, `rights_record`, `reference_audio_sha256`); audition results; `ledgers/model_lifecycle.md` entry.
- **Gate (narration week 1):** "Approved primary voice per required locale." Teachers and native reviewers "must reject meaning-changing pronunciations regardless of acting preference."

## 3. N2 · Localized text first (only for hi-IN / as-IN editions)

- **Owner:** NA **multilingual-director** (localized script, back-check, native-review issues); runs **before** voice direction for each locale. ST language-editor rules apply as a lens: no demographic language assumptions; code-switch only at meaningful boundaries; translate the *function* of humour; keep exam terminology; `terminology.csv`. "Do not substitute Bengali for Assamese."
- **Rules:** "Translate meaning and exam terminology; do not merely dub the English timeline." Each locale has **independent voice, lexicon, audio and timing objects**; "Do not time-stretch the translation into English durations." Do not transfer English word-rate targets to other languages.
- **Gate:** native-language subject editor approves the localized script before synthesis (part of GA for that locale).

## 4. N3 · The structured narration plan

"Keep directing instructions out of canonical spoken text. The provider adapter decides what can safely become a model-specific control." Formal schema: `configs/narration.schema.json` (generated from `contracts.NarrationPlan`).

**Plan level:** `schema_version` "1.0"; `lesson_id`; `academic_edition`; `source_claim_manifest`; `voice` (`VoiceIdentity`); `lexicon_version` (must equal the lexicon's `version` at compile time); `segments` (≥ 1, unique IDs, cue IDs unique across the plan).

**Segment:** `segment_id`; `objective_id`; `claim_ids` (≥ 1); `text_template` (1–6,000 chars, spoken words only, **no `[…]` or `<…>`**, STEM terms as `{{lexicon_key}}`); `direction` (`mode`, `target_wpm` 80–185 default 140, `emphasis`, `notes`); `pause_after` (`kind` ∈ `none` | `beat` | `think` | `pause-video`, `seconds` 0–30, `prompt`; `none` must be 0 s; `think`/`pause-video` require a prompt); `cues` (`cue_id`, `phrase`, `occurrence` ≥ 1, `edge` start/end, `action` ∈ show / highlight / transform / hide / reveal-answer, `element_id`); `expected_visuals`; `critical_phrases`; `answers_after` (ID of an **earlier** question segment).

**Pause kinds.** `none` (no added time), `beat` (short editorial pause), `think` (protected silent window for a mental attempt, answer hidden), `pause-video` (learner-controlled working time with a task prompt).

**`answers_after` rule.** "The answer segment declares `answers_after: question`. Its answer-reveal events cannot precede the protected response window." Enforced at validation (earlier segment; it must end with `think`/`pause-video` > 0 s: "Question needs an explicit protected response window") and at assembly ("Premature answer").

**Segmenting.** "Coherent one-to-three-sentence or roughly 15–35-second units. Not a fixed rule. Do not synthesize every sentence separately." Split questions from answer reveals; long formulas need spoken semantic phrases matched to visual groups. Character caps [RD-28]: ≤ 700 characters per ElevenLabs request (`providers.example.json`), ≤ 1,800 characters per segment absolute (compiler: "Split at a sentence boundary").

**Example segment (message 12 §9, from the implemented schema):**

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

Full five-segment example (question → answer → repair → retry → check): `narration_system_v1/examples/teacher.json`, tabulated in [`05_narration_system/VOICE_IDENTITY_and_DELIVERY_GUIDE.md`](../05_narration_system/VOICE_IDENTITY_and_DELIVERY_GUIDE.md) §11.4.

- **Check:** `PYTHONPATH=src python -m examleaf_narration.cli validate <plan.json>` → "Valid contract: <lesson_id>; not academic/audio approval".

## 5. N4 · Voice direction and pacing estimate

- **Owners:** NA **voice-acting-director** (direction records, emphasis, pronunciation audition list); NA **pacing-controller** (estimate now, measure after synthesis).
- **Six modes** (narration schema) [RD-12]: `curious` (real question, modest anticipation), `steady` (default; causal words carry emphasis), `deliberate` (units, signs, conditions, formulas), `light` (one dry concept-linked observation, no laugh), `reassuring` (specific correction, no pity), `focused` (exam strategy and final checks, "credibility before motivation"). **One dominant intention per segment**; vary because the teaching task changes.
- **Emphasis** only on words that carry logical/quantitative meaning ("because", "provided that", "when the temperature stays constant").
- **Pace** [RD-10]: ordinary 130–155 active wpm; familiar recap ≈ 145–165; new symbolic relationship ≈ 105–125 plus inspection time; brief beat 0.2–0.6 s; important contrast 0.8–1.5 s; completed formula/diagram inspection 2–4 s; simple prediction 4–8 s (runbook default 5–8 s, think = 6 s [RD-11]); writing/drawing/multi-step = learner-controlled pause. Distinguish **active speaking rate** from total lesson rate.
- **Forbidden:** deliberate errors, artificial ums, identity imitation, shouting, forced laughter; "automatic speeding of equations to force ten minutes". Pacing controller order: "Estimate first; generate actual voice; measure active rate and pauses; shorten redundant language before accelerating; lengthen animation; split a chapter if necessary."
- **Prompt:** "Voice direction prompt" in `docs/Reusable_Prompts.md` ("Do not output provider syntax until the adapter selects a capability-tested model").

## 6. N5 · The STEM pronunciation dictionary

**Principle: do not send raw formulas and hope.** Four representations: **scientific meaning → displayed notation → intended spoken form → accepted audio realization.** Examples (contextual authoring, not one universal dictionary): `I = neA·v_d` → "Current magnitude equals number density times elementary charge times cross-sectional area times drift-speed magnitude"; `mA` "milliamperes" vs `MA` "megaamperes"; `10⁻³` "ten to the power minus three"; `sin⁻¹x` "inverse sine of x" vs `1/sin x` "one divided by sine x"; `Na⁺`; `5′→3′` "five-prime to three-prime"; `ΔG` "delta G" with meaning introduced separately.

**Identifier approach.** STEM terms are written as explicit `{{identifier}}` tokens (for example `{{water_formula}}`), never by replacing every occurrence of a short symbol in arbitrary text. `expand()` fails on an unknown token ("Unresolved STEM token"), on a locale without an editorially checked mapping, and on leftover braces. Display, spoken and caption forms come from the same entry.

**Required fields per entry** (message 12 §10.2): **subject, meaning, display form, locale, spoken form, allowed variants, model-specific phoneme/alias override, reviewer status, accepted audio reference.** Current shipped shape: `{display, meaning, locales: {en-IN: {spoken, caption, editorially_checked, acoustic_approved}}}` — **gap**: add `subject`, `allowed_variants`, `model_overrides`, `accepted_audio_sha256` before production (build item, phase 2).

**Critical distinctions** to test in every voice: molarity vs molality; milli vs mega; minus signs, charges, exponents, reciprocals; "increase" vs "decrease"; "not", "only", "provided that" and other conditions; biological directions and counts; similar-sounding scientific names (mitosis vs meiosis). Tested distinctions today: inverse vs reciprocal sine, mA vs MA, mol/L vs mol/kg, 5′ vs 3′, mitosis vs meiosis.

**Overrides are model-specific.** "An IPA string, phoneme dictionary, alias dictionary, and SSML tag are not interchangeable mechanisms." **An explicit spoken alias is the portable baseline**; use provider phoneme features **only after a successful acoustic test**. Eleven v4/v3 do not support SSML break tags; Google SSML support is model-specific. Store dictionaries by **language, subject, provider, model and voice** (message 02 §10).

**Hindi/Assamese.** "Do not automatically use English phonetic spelling as the final Assamese or Hindi representation." Native editors draft and approve those mappings; "this package does not fabricate approved Assamese pronunciations."

**Procedure to add a term:** add the entry; bump `version` **and** the plan's `lexicon_version` together (mismatch blocks compile); reference it as `{{key}}`; only segments using the changed entry get a new `audio_cache_key`.

- **Owner:** NA **stem-pronunciation** (versioned spoken/display/caption mappings + test corpus). It rejects "inverse sine interpreted as reciprocal sine, mA/MA confusion, molarity/molality merging and unreviewed IPA".
- **Output:** `configs/pronunciation.json` (new version) + `audio/pronunciation.json` copy in the lesson folder recording the version used.

## 7. N6 · Compile provider requests (offline), per provider

**Command [TESTED offline]:**

```sh
PYTHONPATH=src python -m examleaf_narration.cli compile ../lessons/<…>/script/narration_plan.json \
  --lexicon configs/pronunciation.json --profile configs/<profile>.json \
  --out ../lessons/<…>/audio/requests/<profile>_requests.json
# prints: Compiled N payloads; sent 0 requests
```

Each compiled request carries `segment_id`, `method`, `url`, `headers_template` (`ENV:` placeholders, not credentials), `body`, `canonical_spoken`, `caption_text`, `audio_cache_key`, **`editorial_style`** (the full direction the provider could not take) and **`warnings`**. **Rule: report unsupported direction, never discard it** — whatever a model cannot accept is kept in `editorial_style` for the human reviewer and the recording sheet (message 12: "Preserve unsupported detailed direction for the reviewer").

| Provider (profile) | Role (launch stack) | What the compiler emits | Caveats |
|---|---|---|---|
| **ElevenLabs Eleven v4** (`eleven_v4.json`) | **Primary expressive candidate; audition first** | `POST /v1/text-to-dialogue`, `{"model_id","inputs":[{"text": <tag>+text,"voice_id"}],"language_code"}`; tags `[curious]`, `[calm]` (deliberate/reassuring); no speed/style/SSML | Released 28 Sep 2026; **no verified tariff (TBD)** [RD-03]; do not copy v2 settings into v4; "WPM and detailed acting cues are editorial targets, not exact API controls"; Assamese and Hindi listed in documentation = **not** a native audition |
| ElevenLabs v3 (`eleven_v3.json`) | Reference | `POST /v1/text-to-speech/{voice_id}`, `{"model_id","text","language_code"}` | v2/v3 reference tariff $0.10/1,000 chars; no SSML breaks |
| **Gemini 3.8 Flash TTS** (`gemini_38.json`, voice Kore) | **Main alternative** | `POST …/v1beta/interactions`; exact text in `content[0].text`, style (brief + mode + wpm + emphasis + notes) in `annotations[{type: speech_metadata, style}]`; `response_format: audio` | "Unary 3.8 output is WAV: do not prepend another header. Streaming differs" (headerless PCM); legacy Generate Content route has a different schema; record custom-voice expiry; $0.50 / $9 per M tokens through 31 Dec 2026, **$1 / $18 from 1 Jan 2027** |
| **Cartesia Sonic** (`cartesia_snapshot.json`) | Additional challenger (English/Hindi) | `POST https://api.cartesia.ai/tts/bytes`, `Cartesia-Version` header required, `generation_config.speed = clamp(wpm/145, 0.6, 1.5)` (a heuristic), beta emotion disabled | Recipe pins the documented **Sonic 3.5 snapshot** (`3.5-2026-05-04`), not 3.6; compile **fails until `api_version` is a real value**; **Assamese not admitted** |
| OpenAI (`openai_snapshot.json`) | **Migration fixture only** | `POST /v1/audio/speech` + "LEGACY MIGRATION FIXTURE ONLY" warning | `tts-1`, `tts-1-hd`, listed `gpt-4o-mini-tts` snapshots shut down **6 Jan 2027**; `production=True` rejects it; the realtime replacement (`gpt-realtime-2.1-mini`) needs a new, separately auditioned adapter |
| **Human performance** | Selective: difficult humour, emotional transitions, important explanations | Not implemented in code: export a **recording sheet** from the same plan | Template below; performer consent per N1 |

**Human recording sheet** (one row per segment, from the plan fields): `segment_id` · exact text (spoken form after `{{token}}` expansion) · mode · target wpm · emphasis · notes · pause after (kind / seconds / task — inserted in the edit, **not performed**) · critical phrases · take # / accepted?

**Production gates coded in `compile_plan(…, production=True)`** (in order): deprecated model → "Deprecated model: new production blocked; migrate before 2027-01-06"; rights not `licensed-stock`/`consented-custom` → "Production voice rights not cleared"; `live_contract_verified` false → "Live endpoint contract not approved"; voice ID containing `REPLACE` → "Replace placeholder voice ID". Always: lexicon version match; 1,800-character cap.

- **Owner:** NA **tts-provider-adapter** ("Reject unsupported SSML, plaintext secrets, unverified voices and unknown-status resubmission").

## 8. N7 · Admission and budget reservation before any paid call

1. **Provider admission checklist** (`docs/Provider_Lifecycle.md`): record provider, API version, exact model ID, lifecycle dates, voice rights, voice ID, locale, permitted controls, audio format, rate/concurrency limits, estimate/actual usage, sample hashes and reviewer approvals. "Only a successful request plus content and listening checks can promote a recipe into a production integration."
2. **Reserve** the estimated cost in the budget ledger under an idempotency key (`BudgetLedger.reserve(key, cents)`; same key + same cents = no-op; same key + different cents = error; over the limit = refused). Create a `ProviderJob` (`idempotency_key` ≥ 8 chars, `provider`, `model`, `estimated_cents`, `input_sha256`, `state: reserved`).
3. Synthesis runs **only in the provider worker** (its scoped key, approved outbound domain, cost reservation, timeouts, concurrency limits). "Keep synthesis out of the agent's direct shell." **Bulk narration uses SDK/API workers with explicit budgets and persistent job records; MCP only for supervised development and auditions** ("MCP is not a permission sandbox or durable production queue").

## 9. N8 · Generate in coherent sentence groups; persist job IDs immediately

- **Do:** one synthesis job per coherent segment; **persist the provider job ID the moment it is returned** (a `ProviderJob` in `submitted`/`running`/`succeeded`/`unknown` state must carry `provider_job_id`); save raw audio, request/response hashes and actual usage, "excluding secrets and signed URLs"; copy provider assets with expiring URLs to controlled storage and hash them.
- **Job-state decisions** (`cache.decide_submission`, [TESTED]): `submitted` / `running` / `unknown` → **reconcile the existing job, never blindly resubmit**; `succeeded` → validate and cache the existing output; `not-submitted` → reserve budget then submit once; `failed` → review the failure and authorize a bounded retry.
- **Retry policy:** transient errors → exponential backoff, respect `Retry-After`; unknown paid-job status → poll/reconcile, never duplicate; auth/rights/language/capability failure → **hard stop, no silent vendor switch**; budget exhaustion → pause. "A second unknown or repeated failure requires review, not blind regeneration." Settle actual cost (`settle(key, actual_cents)` records an overrun honestly, then blocks further spend).
- **Cache:** `audio_cache_key` excludes visuals and holds (no paid resynthesis for a timing edit); a cache hit requires key **and** audio hash to match.
- **Owners:** VE voice-synthesis (audio assets + job/cost manifest) → NA tts-provider-adapter; NA **cost-regeneration-optimizer** (usage ledger, scoped invalidation, retry decision: "Reject repeated submission after timeout and unlimited attempts to chase a vibe").
- **Output:** `audio/raw/*.wav`, `audio/provider_jobs.json`.

## 10. N9 · Independent ASR and critical-term review; accept or repair the take

- **Do:** transcribe each take with a **separately evaluated** ASR using **audio-only decoding** ("do not supply expected answer text that biases away defects"); compare with the canonical spoken text; check every critical phrase, number, unit, negation, direction and condition; **listen** to every critical term.
- **Tool [TESTED comparator only]:** `qa.transcript_check(expected, observed, critical_phrases)` → `surface_word_error_rate`, `edit_count`, `critical_mismatches`, `needs_human_check`; limitation: "ASR can normalize mispronunciation into the intended word; **zero WER does not approve pronunciation**." Tested on a dropped "not" and "Four" → "Two". English-only surface comparator; native Indic normalization needs separate review.
- **ASR candidates [RESEARCHED]:** faster-whisper (independent baseline); Gemini transcription (lists Assamese and word-level timestamps; "a relevant candidate, not an integration tested"). ASR inference is **not integrated** (narration week 3).
- **Accept/repair:** regenerate **only** the affected segment; edit wording rather than speeding audio; a fallback voice/model must be pre-approved or the job waits.
- **Owner:** NA **narration-quality-reviewer** ("Reject WER0 or neural MOS as proof of scientific pronunciation and teaching success"). QA prompt: `docs/Reusable_Prompts.md` "QA prompt".
- **Output:** `audio/asr_diff.json`, `audio/accepted/*.wav`.

## 11. N10 · Forced alignment to the accepted speech

- **ASR asks** "What does another system think was spoken?"; **forced alignment asks** "Where does the supplied text fit in this audio?" "Zero word error rate and a successful alignment do not prove correct STEM pronunciation."
- **Tools [RESEARCHED]:** ElevenLabs forced-alignment endpoint initially (not integrated); WhisperX (numbers/currency tokens can lack times; language-specific aligner needed) and Montreal Forced Aligner (needs matching dictionary and acoustic model incl. STEM entries; "not a pronunciation oracle") where language resources suit. **Reject unavailable language resources rather than inventing word timing.** Verify against a **manually annotated sample**.
- **Import [TESTED]:** `Alignment` (`segment_id`, `audio_sha256`, `transcript_sha256`, `method` ∈ provider-timestamps / forced-aligner / human / synthetic-fixture, `engine_version`, `words[{text, start, end}]`); `timeline.validate_alignment` checks audio hash, transcript digest, identical normalized word sequence, monotonic intervals (1 ms tolerance), last word ≤ duration. `synthetic-fixture` alignment sets `contains_fixture: true`, which blocks release. "Synthetic alignment timestamps are test data, never claimed as acoustic alignment."
- **Output:** `audio/alignment.json`.

## 12. N11 · Protected pauses, semantic events and captions (the timeline)

- **Sample-based timing.** "At 48 kHz, 6 seconds = 288,000 samples." The composer inserts **exact zero samples** for every pause; it never asks the TTS engine to "pause for exactly six seconds". Store events against accepted-audio sample positions, then convert **once** to frames: `frame = round_half_up(sample × fps_num / (48,000 × fps_den))` (30 fps default; 30000/1001 supported). Avoid repeated floating-point rounding or independent sentence-duration estimates.
- **Occurrence index.** "Highlight when the word 'current' is spoken" is ambiguous when it appears four times; every `Cue` carries `occurrence` (1-based) and `edge`. A missing occurrence fails loudly.
- **Answer protection.** An answer clip or `reveal-answer` cue that starts before the question's pause ends raises "Premature answer".
- **Mono only** ("explicitly review/downmix first"); polyphase resampling to 48 kHz; providers may return 24/44.1 kHz ("Resampling does not recreate missing high-frequency detail").
- **Captions:** prototype WebVTT every 6 aligned words; caption readability checks are **[NOT DONE]**; captions must never reveal an answer during a response window; captions are an accessibility requirement, not optional.
- **Owner:** NA **speech-animation-synchronizer** ("Reject guessed uniform word timing for production; synthetic fixture cannot pass release").
- **Command/function:** `timeline.compose(plan, lexicon, audio_paths, alignments, output, sample_rate=48000, fps_num=30, fps_den=1)` + `write_vtt()` (a CLI wrapper is a phase-2 build item).
- **Output:** `audio/timeline.json`, timeline WAV, `captions.vtt` → engine S11.

## 13. N12 · Mastering

- **Target** (an internal ExamLeaf starting target, "not a universal platform requirement"): **48 kHz mono, 24-bit archival WAV; ≈ −16 LUFS integrated (±1); true peak ≤ −1 dBTP**; delivery codec checked **after the final mux** ("the final encoded delivery should be measured again").
- **Command [TESTED on signal fixtures]:** `PYTHONPATH=src python -m examleaf_narration.cli master <in.wav> --out <out.wav>` → two-pass `loudnorm=I=-16:TP=-1:LRA=7` with `linear=true`, `-ar 48000 -ac 1 -c:a pcm_s24le`, re-measure; pass = |I + 16| ≤ 1 and TP ≤ −0.9; refuses to overwrite its source.
- **Do not** treat clean synthetic speech like a noisy location recording; excessive denoising damages consonants; never remove all breaths or flatten every sentence to identical loudness; never let silence removal cross protected thinking windows (Silero VAD: "Never remove protected think/write pauses automatically"). Mastering or trimming changes hashes → reconcile timing and hashes.
- **Music:** **off during the main explanation by default**; add music or effects only when they survive a comprehension and listening-effort comparison; no laugh effects, no unrelated stings; licensed audio only.
- **Owner:** NA **audio-production-engineer** ("Reject unnecessary denoise/reverb/music and silenceremove applied across thinking windows").
- **Output:** `audio/master.wav`, `audio/mastering_qa.json`, `audio/signal_qa.json` (run `qa` **with** the protected intervals; the CLI `qa` command cannot pass them and will flag deliberate pauses as unplanned silence — add an intervals option as a build item or use `qa.signal_report(path, protected_intervals=…)` directly).

## 14. QA layers (message 12 §11.4)

| Layer | Automated checks | Human responsibility | Implemented today |
|---|---|---|---|
| Text | Missing conditions, unresolved terms, forbidden metadata in dialogue | Scientific meaning and natural teaching | Unresolved/malformed `{{tokens}}`; stage tags rejected [TESTED] |
| Transcript | Added/omitted words, critical numbers and phrases | Ambiguous pronunciation and ASR mistakes | `transcript_check` [TESTED]; ASR inference [NOT DONE] |
| Signal | Clipping, DC offset, duration, unexpected silence | Audible distortion, joins, fatigue | `signal_report` [TESTED] |
| Voice consistency | Flag unusual rate, level, or speaker changes | Judge acceptable performance variation | [NOT DONE] |
| Alignment | Word order, monotonic timestamps, audio/transcript hashes | Inspect difficult anchors | `validate_alignment` [TESTED] |
| Interaction | Answer hidden until response window ends | Confirm the task is fair and meaningful | `answers_after` + "Premature answer" [TESTED] |
| Captions | Timing and text checks | Readability and accurate meaning | Prototype VTT; readability [NOT DONE] |
| Final video | Automated defect report | Listen/watch the whole result | [NOT DONE] |

"Pitch tracks or model-generated 'naturalness scores' may help triage. They should not automatically reject a voice because of accent or approve a lesson because it scores highly." The user's requested automatic checks (missing words, inaccurate scientific pronunciation, awkward phrasing, inconsistent delivery, clipped audio, excessive silence, unnatural intonation, incorrect synchronization) map onto these rows; pronunciation, phrasing, delivery and intonation remain human judgements.

## 15. Audio approvals and the narration release check

Release evidence the narration side must supply for GF (`qa.release_report` keys): **academic_listening**, **voice_rights**, **native_language_review** (localized editions), **caption_review**, **sync_review**, approval/audio **hash match**, **mastering passed**, and the absence of fixtures. Approvals come from the authenticated approval service bound to the audio and video hashes. `PYTHONPATH=src python -m examleaf_narration.cli release-check <timeline.json>` **always exits 2 in the starter** ("It requires true speech and an authenticated approval service; local self-asserted booleans cannot approve a production lesson"); production replaces it with a check against the approval service [RD-32]. Never fabricate reviewer identities or flip booleans.

## 16. Fallback, consistency and the golden set

- **Fallback rule:** "Do not silently replace a voice when a provider fails. **A fallback must be an approved voice/model combination, or the job should wait.**" Where vendor voices expire or change, "preserve lawfully retained approved output; alert and audition replacement rather than silently switching."
- **Consistency:** version the voice profile, pronunciation dictionary, reference passages, model, settings and accepted samples. "Consistency is not identical pitch and rhythm on every sentence."
- **Golden set:** keep a set of difficult passages (from the casting corpus: negation, decimals, exponents, conditions, code-switches, the critical distinctions) with accepted audio hashes; **re-run it before any model, voice or provider upgrade** and before adopting a new model generation. An upgrade "cannot pass solely because an earlier version passed".
- **Lifecycle dates to watch** (checked 13 Oct 2026): OpenAI legacy TTS shutdown 6 Jan 2027; Gemini 3.8 price change 1 Jan 2027; Eleven v4 tariff unknown; Cartesia allowance above 8 M credits needs a quote. Keep them in `ledgers/model_lifecycle.md`.
- **When speech-to-speech is worthwhile:** passages where the performer's delivery matters (dry joke, difficult multilingual transition, careful contrast, subtle reassurance); it "does not automatically fix wrong science, missing words, or an incorrect pronunciation in the input". Reference price $0.12 per generated minute (before performer and review).

## 17. Benchmark the voice before making it the brand: studies A, B, C

"Separate three experiments: (1) provider/voice selection with identical content and normalized playback level; (2) script-style comparison with matched science/time; (3) actual learning efficacy."

| Study | Design | Raters / measures | Not allowed |
|---|---|---|---|
| **A · Voice/provider audition** | Identical passages; normalized level; blinded provider names; rotated order; connected explanations, not only impressive sentences; corpus per N1; 3 voices/locale; 2 repeats of difficult passages; 10-minute continuity after short-listing | Teacher: meaning-changing pronunciation defects (**release blocker**), terms and conditions. Native editor: accent, intelligibility, naturalness without imposing a stereotype. Students: listening effort, clarity, warmth, dignity, preference. Production reviewer: joins, loudness, silence, captions, reveal timing | Weighted scoring that lets delightful acting compensate for wrong science; intrusive attention/emotion surveillance |
| **B · Script-style comparison** | Same science and study opportunity; straightforward explanation vs Super Teacher version | Comprehension, listening effort | Treating the two Runway auditions as evidence (several variables changed together) |
| **C · Learning evaluation** | Independent question immediately and a fresh question later; short listening panels first, then a properly designed study | Delayed performance; calibration | Preference, voice similarity, completion rate or apparent confidence as the primary outcome; claiming a modest exam advantage from a small panel |

## 18. Assamese and Hindi gates

- **Gate for any non-English locale:** (1) a **successful model-specific API request** in that locale; (2) **native-language review** of script, lexicon and audio (mandatory); (3) separate transcript-normalization tests; (4) new performance, QA and timeline verification ("A second language requires new performance, QA and timeline verification"). "Model language support is a hard gate verified through a real request and native review, not a generic marketing language count."
- **Provider status for Assamese** (13 Oct 2026; *research record only — since 15 Oct 2026 there is **no Assamese TTS commitment**, RD-42*): ElevenLabs v4/v3 and Gemini 3.8 Flash/Flash-Lite list Assamese (documented, not auditioned); **Cartesia: not admitted**; OpenAI replacement: not admitted; **Sarvam Bulbul v3: marketing mentions Assamese but the model-specific API language list omits it — "sufficient to block an Assamese production commitment until an actual API request succeeds and native reviewers approve"**; open-source: Indic Parler TTS documents Assamese (gated download, needs native review); Chatterbox, Kokoro, CosyVoice, Qwen3-TTS not established. **Never substitute Bengali pronunciation or infer support from script similarity.**
- **Hindi/Hinglish:** documented for Eleven v4, Gemini 3.8; worth testing for Cartesia (code-switching must be auditioned); Chatterbox multilingual documents Hindi. "Do not assume Hindi is universally comfortable for an Assam audience."
- Launch decision *(revised 15 Oct 2026; RD-42 supersedes RD-26)*: **en-IN, Hinglish and hi-IN** at launch, each released only after it passes the gate above (Hinglish is audited as its own code-switching locale; it does not inherit en-IN or hi-IN approval). **as-IN is deferred** and, when started, uses a **human voice** (recorded performer under a consent and rights record); no TTS or speech-to-speech route is committed for Assamese. (Previous text: ~~"**en-IN only** until the business medium decision (W3) requires otherwise [RD-26]"~~.)

## 19. Self-hosting and open-source licence traps

"Do not self-host first solely to save the TTS API fee." Start only when one of these is **demonstrated**: a tested model gives a better required language/voice; privacy/offline needs justify it; real usage exceeds full hosting + maintenance + QA cost; vendor independence is worth the engineering. Code, weights, voice references and commercial permissions are checked separately: **F5-TTS** code MIT but default weights **CC BY-NC** ("a self-hosting licence trap"); **Fish Speech S2** under the **FISH AUDIO RESEARCH LICENSE** (code and weights; not a default commercial self-host); Kokoro Apache-2.0 weights (English drafts/previews; no Assamese); Indic Parler gated download. No local neural TTS has been run.

## 20. Cost per lesson (pointers; planning estimates)

| Item | Value | Source |
|---|---|---|
| Premium TTS synthesis (v2/v3 reference) | 7,800 chars × 1.2 × $0.10/1k = **$0.936** | narration workbook [RD-03] |
| Gemini 3.8 Flash synthesis | $0.1392 now; $0.2784 from 1 Jan 2027 | same |
| Speech-to-speech | 8.5 min × 1.2 × $0.12 = $1.224 | same |
| Self-hosted GPU (illustrative) | $0.272 (RTF 2, $0.80/GPU-h, unbenchmarked) | same |
| Premium commercial TTS method, variable per lesson | **$12.50** ($1.666 machine incl. $0.60 LLM direction, $0.08 ASR/QA, $0.05 storage + $10.83 human: 25 min review + 10 min editing) | message 12 §13.3 |
| Other methods | self-hosted $14.75; human recorded $42.40; performance + STS $34.87; hybrid 80/20 $17.06 | same |
| Human hours at 1,000 lessons (premium) | ≈ 583 h — "the dominant cost" *(15 Oct 2026, RD-41: review cash is $0, so this is capacity, not cash)* | same |
| Narration set-up reserve | $4,000 (separate) | same |

Do **not** add the narration review minutes on top of the engine's review without deciding the overlap: [`08_COST_TRACKING_and_BUDGETS.md`](08_COST_TRACKING_and_BUDGETS.md) §6.

## 21. Known gotchas (narration pack)

1. `scripts/build_examples.py` overwrites `configs/`, `examples/` and most of `outputs/`; run only on a copy.
2. `scripts/build_docs.py` overwrites `README.md` with an older variant and regenerates Skills/docs; do not run it on the curated copy.
3. CLI `qa` flags deliberate pauses as unplanned silence (no protected-interval option).
4. CLI `release-check` always exits 2 until real speech and an authenticated approval service exist.
5. The example `teacher.json` spoken text expands `{{water_formula}}` to "H two O" where message 12 says "water"; shipped lexicon wording differs slightly from message 12's examples (the lexicon, not the prose, is what the compiler uses).
6. The NOT-SPEECH WAVs must never be played or marketed as voice demonstrations.
