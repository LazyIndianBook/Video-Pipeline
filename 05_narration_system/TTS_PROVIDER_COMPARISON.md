# TTS Provider Comparison — commercial, open-source, languages, tariffs and costs

**Section:** `05_narration_system` · **Research date in the sources:** 13 October 2026 · **Sources consolidated:** message 12 §1–§3, §12.2 and §13 (`FULL_narration_system.md`); `narration_system_v1/docs/Provider_Lifecycle.md`; `narration_system_v1/docs/Costs_and_Methods.md`; `narration_system_v1/research/Public_Narration_Directory.md` / `public_directory.csv`; `narration_system_v1/src/examleaf_narration/compiler.py`; `narration_system_v1/configs/*.json`; `narration_system_v1/outputs/cost_summary.json`; the workbook `narration_system_v1/ExamLeaf_Narration_Cost_Model.xlsx` (sheets exported as CSV in `00_source/spreadsheets_as_csv/ExamLeaf_Narration_Cost_Model__*.csv`).

> **Read this first — what is and is not verified (verbatim from the sources)**
>
> - "**This is a ranked implementation recommendation, not a claim that I have listened to and benchmarked all three commercial models.**"
> - "The documentation supports the language coverage, **not the comparative naturalness ranking**."
> - Local speech-quality or pronunciation benchmark: "**Not performed**". No neural TTS model was run locally ("The supplied package does **not** include pretrained weights or claim that a neural TTS model was run locally.").
> - The only real voice output: "**Two speech auditions generated through your connected Runway account**, using 18 workspace credits" — both on **Eleven v3** (voice "Arjun", speed 0.95, en). They "differ in wording, length, and expressive instructions, so they are demonstrations—not a controlled A/B experiment", and were never transferred, listened to, measured or mastered locally.
> - All provider "recipes" in `configs/` compile to **non-executing request JSON**; "The compile command creates request JSON and sends **zero network requests**."
> - Prices: "Personnel rates, processing times, retry rate, and GPU figures are **editable planning assumptions, not quotations or measured TTS benchmarks**."

Cross-references: overall video-engine stack and renderer → `04_video_engine`; the complete cost workbooks for the whole project → `08_cost_models`; research sources and evidence → `09_research_and_evidence`; Skill-level reuse of provider Skills → `SKILLS_INDEX_narration_15.md` §7–§8; pilot listening studies → `10_pilots_and_examples`.

---

## 1. Recommended launch stack (message 12 §1)

| Layer | Recommended choice | Why |
|---|---|---|
| Script and teaching direction | Custom ExamLeaf Skills through Claude Code/Codex | Your personality, scientific constraints, and teaching progression should remain provider-independent |
| Primary expressive TTS candidate | **Eleven v4** | Strong candidate for directed, expressive narration and a consistent voice identity |
| Main alternative to audition | **Gemini 3.8 Flash TTS** | Explicit separation of spoken text and performance metadata; broad language coverage and attractive published pricing |
| Additional challenger | **Cartesia Sonic 3.6** | Particularly worth testing for conversational Indian English/Hindi and production efficiency |
| Human-performance path | Consented human recording, optionally converted to a licensed target voice | Preserves a deliberately performed rhythm where text prompting is insufficient |
| Independent transcription | A separately evaluated ASR model/provider | Helps detect omissions, additions, wrong numbers, and substituted terms |
| Alignment | ElevenLabs alignment initially; WhisperX/MFA where language resources are suitable | Align accepted speech with the approved transcript |
| Audio processing | FFmpeg + SoundFile + NumPy/SciPy | Reproducible audio assembly, measurement, mastering, and export |
| Playback timing | Sample-index narration timeline passed to existing scene adapters | Animations follow actual speech instead of forcing speech into rigid scenes |
| Release | Academic/native-language listening plus full-video review | Automated checks cannot certify teacher quality or every pronunciation |

**This is a ranked implementation recommendation, not a claim that I have listened to and benchmarked all three commercial models.** The choice of final voice should follow a controlled audition. A marginally cheaper API is not a saving when it produces substantially more pronunciation repairs or reviewer work.

Message 12 opening recommendation: **one consistent lead voice per language**, premium commercial speech generation initially, and **selective human-performed reference passages** for difficult humour, emotional transitions, or particularly important explanations. Do not make every lesson a two-character conversation.

---

## 2. Commercial providers

### 2.1 ElevenLabs — first production candidate, with model-specific controls

**Message 12 §2.1.** Eleven v4 is the current expressive candidate. Current documentation also lists Assamese and Hindi coverage in the relevant newer model families. That resolves an important uncertainty from earlier generic language-support discussions, but **documented support is not proof of native-quality pronunciation for your curriculum**.

For ExamLeaf:

- **Use TTS** for most approved script segments.
- **Use speech-to-speech** when a performer can deliver a passage more effectively than a text instruction can.
- **Use voice isolation** only when a recording genuinely needs cleanup.
- **Use dubbing cautiously** for exploratory localization. Final Hindi or Assamese lessons should retain explicit control over scientific wording, conditions, notation, and timing.

*Important control changes.* Do not copy old ElevenLabs settings into a new model blindly. The inspected v4 guidance differs from older models: **SSML and legacy speed/style controls are not interchangeable across the family**. Dictionary phoneme support likewise does not imply universal SSML support. The starter therefore uses an explicit model-specific request recipe rather than a generic payload containing every setting. **Keep the original teaching direction even when a provider cannot represent it exactly.** The adapter should report that limitation, not silently discard it.

**`docs/Provider_Lifecycle.md` adds:** Eleven v4 is the current expressive audition candidate. The compiler uses its documented text-to-dialogue route, separate from earlier text-to-speech examples. It does not copy older speed/style or SSML controls into v4. v4/v3 language documentation lists Assamese, but model-level availability is not a successful native-language audition. Stock-voice IDs are provider-specific; a Runway voice preset name is not a direct ElevenLabs API voice ID. Sources: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 ; https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support

**Directory entries (research-read, not live-tested):**

| Entry | Boundary (verbatim) |
|---|---|
| Eleven v4 (https://elevenlabs.io/docs/changelog/2026/9/28) | Released 28 Sep 2026. v4 and turbo differ. v4 no SSML or legacy speed/style sliders. Text-to-dialogue documented; endpoint feature parity must be tested. |
| Eleven pronunciation dictionaries | Dictionary phonemes are not universal SSML support. Newer API docs and Studio guides differ; pin exact endpoint/model/dictionary version. |
| Eleven forced alignment | Aligns supplied text and audio; not an independent scientific/pronunciation test. |
| ElevenLabs official Skills (MIT Skill code) | Ten Skills in inspected README. Python `elevenlabs`; JS `@elevenlabs/elevenlabs-js`. No need live conversational agent Skills for prerecorded lessons. |
| ElevenLabs MCP (MIT bridge; account charges apply) | MCP is tool access, not TTS quality or permission sandbox. Prefer SDK worker for bulk production. |

**How the starter compiles ElevenLabs requests (`compiler.py`):**

| Model profile | Endpoint | Body | Mode tag prefix | Locales admitted |
|---|---|---|---|---|
| `eleven_v4` (`configs/eleven_v4.json`) | `POST https://api.elevenlabs.io/v1/text-to-dialogue` | `{"model_id","inputs":[{"text","voice_id"}],"language_code"}` — "Deliberately no v2-style speed/style controls or SSML." | yes | en-IN, hi-IN, as-IN |
| `eleven_v3` (`configs/eleven_v3.json`) | `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` | `{"model_id","text","language_code"}` | yes | en-IN, hi-IN, as-IN |
| `eleven_multilingual_v2` (no shipped profile) | `POST .../text-to-speech/{voice_id}` | `{"model_id","text"}` | **no tags** | en-IN, hi-IN (Assamese rejected — tested) |

Mode→tag mapping (`ELEVEN_TAG`): curious → `[curious] `; deliberate → `[calm] `; reassuring → `[calm] `; steady, light, focused → no tag. Header template `xi-api-key: ENV:ELEVENLABS_API_KEY`. Warning attached to every ElevenLabs request: "WPM and detailed acting cues are editorial targets, not exact API controls."

### 2.2 Cartesia Sonic — strong challenger, not automatically the cheapest accepted audio

**Message 12 §2.2.** Cartesia has an official Skills repository covering its raw APIs, SDKs, and optional MCP tooling. Its `cartesia-api` Skill is relevant here; `line-voice-agent` is primarily aimed at interactive voice-agent applications rather than prerecorded lessons.

Sonic 3.6 is the current marketed generation, including multilingual/code-switching use cases. However, the request contract I could directly inspect in detail used a documented Sonic 3.5 snapshot. **The bundled recipe is labelled accordingly; I did not rename it "3.6" and imply that it was tested.**

Recommended role:

> Audition Sonic against the other shortlisted engines using identical Indian-English and Hindi passages, then compare **accepted output cost**, not advertised latency alone.

Assamese is **not admitted by the Cartesia contract in this starter**. Do not substitute Bengali or assume that a broad multilingual claim covers the intended language.

**`docs/Provider_Lifecycle.md` adds:** Sonic 3.6 is the current marketed model. This package's request recipe uses a documented Sonic 3.5 snapshot, explicitly labelled as such. Select the actual live model identifier, API version, voice and language contract in a new tested adapter. Do not rename a snapshot and pretend it was tested. Hindi/code-switching suitability must be auditioned; Assamese is not admitted by this scaffold. Sources: https://docs.cartesia.ai/build-with-cartesia/tts-models/latest ; https://cartesia.ai/pricing

**Directory boundary:** "Sonic 3.6 appears on current product pages; checked API documentation snapshot was 3.5. Scaffold pins 3.5-2026-05-04, not a claim that 3.5 is latest. Assamese not established by this audit." Cartesia MCP: "Do not add production orchestration merely to wrap a REST request."

**How the starter compiles Cartesia requests:** profile `configs/cartesia_snapshot.json` → model `sonic-3.5-2026-05-04`, `voice_id: REPLACE_WITH_APPROVED_VOICE_ID`, `api_version: REPLACE_WITH_REVIEWED_API_VERSION` (compile **fails** without an `api_version` — "Specify verified Cartesia-Version"). Endpoint `POST https://api.cartesia.ai/tts/bytes`; headers `Authorization: Bearer ENV:CARTESIA_API_KEY`, `Cartesia-Version`; body `{"model_id","transcript","voice":{"mode":"id","id"},"language","output_format":{"container":"wav","encoding":"pcm_s16le","sample_rate":48000},"generation_config":{"speed": clamp(target_wpm/145, 0.6, 1.5) rounded to 3 dp,"volume":1}}` (e.g. 140 wpm → 0.966). Warning: "Speed multiplier is a starting heuristic, not a WPM guarantee; beta emotion disabled." Locales admitted: en-IN, hi-IN only.

### 2.3 Gemini TTS — particularly promising for directed multilingual narration

**Message 12 §2.3.** The current Gemini 3.8 TTS interface separates **verbatim spoken text** from turn-level delivery instructions in `speech_metadata.style`. It also supports point-in-time vocal events. This maps well to an ExamLeaf narration format with separate dialogue and directing metadata.

Both Gemini 3.8 Flash TTS and Flash-Lite list **Assamese and Hindi**. Native review is still mandatory, particularly for scientific names, numbers, borrowed terminology, and code-switch boundaries.

Two implementation details that matter:

- **Audio format:** current unary output is a complete WAV file; streaming output commonly uses raw PCM. Do not prepend a second WAV header or concatenate complete WAV containers as though they were raw samples.
- **Voice lifecycle:** custom voice identifiers have documented storage and expiry limits. A brand voice needs a renewal/version policy, not just a voice ID stored indefinitely.

**Recommended role:** main commercial alternative, especially for multilingual expansion and cost-sensitive bulk production.

**`docs/Provider_Lifecycle.md` adds:** Current 3.8 TTS uses the Interactions schema in the primary recipe, with exact spoken text separate from `speech_metadata.style`. The legacy Generate Content route has a DIFFERENT schema. Unary 3.8 audio is WAV, while streaming commonly uses headerless PCM. Do not prepend a second header or concatenate complete WAV containers as raw samples. Custom voice storage/expiry limits matter for a stable brand voice; record expiry and renewal obligations. Both 3.8 Flash and Flash-Lite list Assamese/Hindi. **Neither has been live-synthesized here.** Current Flash pricing is \$0.50/M input and \$9/M output tokens; the announced 2027-01-01 prices are \$1/\$18 respectively. Pricing specifies 25 audio tokens/second. Account terms, caps and actual usage govern invoices. Sources: https://ai.google.dev/gemini-api/docs/speech-generation ; https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-lite-tts ; https://ai.google.dev/gemini-api/docs/pricing

**Directory boundary:** "Latest indexed guide: structured speech_metadata, verbatim text, angle-bracket event tags, unary WAV. Old cached guide still showed 3.1. Assamese documented in current language list; native audition mandatory." Licence note: "Commercial API terms; free/paid data policies differ." Use: "3.8 Flash expressive challenger; Flash-Lite high-throughput comparison."

**How the starter compiles Gemini requests:** profile `configs/gemini_38.json` → model `gemini-3.8-flash-tts`, voice `Kore` (also admitted: `gemini-3.8-flash-lite-tts`). Endpoint `POST https://generativelanguage.googleapis.com/v1beta/interactions`, header `x-goog-api-key: ENV:GEMINI_API_KEY`. Body: `input[0].content[0] = {"type":"text","text": <exact spoken text>, "annotations":[{"type":"speech_metadata","style": <voice brief + mode style + "Aim for approximately N spoken words per minute; do not add words." + "Emphasize: …" + notes>}]}`, `response_format {"type":"audio"}`, `generation_config.speech_config[{voice}]`. Warning: "Unary 3.8 output is WAV: do not prepend another header. Streaming differs." Locales admitted: en-IN, hi-IN, as-IN. `outputs/request_preview.json` is byte-identical to `outputs/gemini_38_requests.json`.

For independent Assamese transcription, Gemini's current transcription documentation lists Assamese and word-level timestamps. That is a relevant candidate, **not an integration tested in this package** (message 12 §11.2).

### 2.4 OpenAI speech — a migration issue must be handled now

**Message 12 §2.4.** The current official deprecation notice schedules `tts-1`, `tts-1-hd`, and the listed `gpt-4o-mini-tts` snapshots for removal on **6 January 2027**. It names **`gpt-realtime-2.1-mini`** as the recommended replacement. Older guides and public Skills still contain legacy examples. Therefore: **Do not start a new ExamLeaf catalogue on an old TTS snapshot merely because a Skill still uses it.** The replacement is a realtime model with a different integration context. Its documentation lists text and audio pricing, but it should not be treated as a proven drop-in prerecorded-narration replacement without an exact-script audition and endpoint test. The supplied OpenAI recipe is consequently an **offline migration fixture**. The code blocks it for new production.

**`docs/Provider_Lifecycle.md` adds:** The official deprecation notice dated 1 October 2026 schedules `tts-1`, `tts-1-hd`, `gpt-4o-mini-tts-2025-03-20` and `gpt-4o-mini-tts-2025-12-15` for shutdown on 6 January 2027. It names `gpt-realtime-2.1-mini` as replacement. Old guides and Skills still contain older model examples. The lifecycle notice takes precedence over those cached examples. The bundled `openai_snapshot.json` is an offline migration fixture. `compile_plan(..., production=True)` rejects it even if local voice-rights and endpoint booleans are supplied. This project does not implement the realtime replacement or claim exact-script compliance on it. Its documented model rates are **\$0.60/M text input tokens and \$20/M audio output tokens**; do not transplant another vendor's audio token-per-second convention. Sources: https://developers.openai.com/api/docs/deprecations ; https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini

**Directory boundaries:** OpenAI speech — "Official deprecation notice dated 2026-10-01 schedules the old TTS snapshots for shutdown 2027-01-06. Replacement is gpt-realtime-2.1-mini. Old recipe is an OFFLINE MIGRATION FIXTURE blocked for production. Realtime replacement requires a new live-tested adapter; it is not assumed a drop-in endpoint. Assamese not admitted by scaffold." OpenAI curated speech Skill — "Not proof current commands/model defaults are ideal for ExamLeaf. Model/endpoint contracts override old Skill snippets."

**How the starter compiles it:** profile `configs/openai_snapshot.json` → `gpt-4o-mini-tts-2025-12-15`, voice `marin`; endpoint `POST https://api.openai.com/v1/audio/speech`, header `Authorization: Bearer ENV:OPENAI_API_KEY`; body `{"model","voice","input","instructions": <style>,"response_format":"wav"}`; warning "LEGACY MIGRATION FIXTURE ONLY: deprecated 2026-10-01; shutdown 2027-01-06; replacement gpt-realtime-2.1-mini requires a separately tested adapter." Production compile raises "Deprecated model: new production blocked; migrate before 2027-01-06" (tested by `test_deprecated_model_blocked_even_with_approval`). Locales admitted: en-IN, hi-IN.

### 2.5 Human narration, human performance + speech-to-speech

- **Human narration:** English/Indian-English quality "Depends on the actual performer"; Hindi/Hinglish "Native/competent performer available"; Assamese "Native performer offers the clearest control route" (§2.5 table).
- **Speech-to-speech (message 12 §12.2):** Use it for passages where the actor's performance makes a material difference: a dry joke, difficult multilingual transition, careful contrast, or unusually subtle reassurance. It is less compelling for every ordinary explanatory sentence. Speech-to-speech can transfer performance into a target voice, but it does not automatically fix wrong science, missing words, or an incorrect pronunciation in the input. The official ElevenLabs Skill describes it as voice transformation—not an academic correction system.
- **Rights:** consent to record a lesson should not be silently treated as consent to create an indefinitely reusable synthetic identity; ElevenLabs' professional-cloning workflow has explicit verification requirements (§12.1). Full rules: `VOICE_IDENTITY_and_DELIVERY_GUIDE.md` §9 and `INSTRUCTIONS_narration_pipeline.md` §15.

---

## 3. Language support versus voice suitability (message 12 §2.5)

| Candidate | English/Indian-English assessment | Hindi/Hinglish | Assamese |
|---|---|---|---|
| Eleven v4 | Audition the actual voice, not just the model | Documented language support; test code-switching | Documented; native audition required |
| Gemini 3.8 TTS | Explicit style/accent direction available; test outcome | Documented | Documented |
| Cartesia Sonic | Worth auditioning for conversational delivery | Worth testing; model-specific controls matter | Not verified/admitted here |
| OpenAI replacement route | Requires new exact-script benchmark | Requires locale-specific testing | Not admitted by this starter |
| Human narration | Depends on the actual performer | Native/competent performer available | Native performer offers the clearest control route |

The documentation supports the language coverage, **not the comparative naturalness ranking**.

**Locale admission actually enforced by the code (`compiler.LANGUAGES`)** — a request for a locale not in this table raises "Language not admitted by this model contract"; an unknown provider/model raises "Unreviewed provider/model contract":

| Provider | Model | en-IN | hi-IN | as-IN |
|---|---|:-:|:-:|:-:|
| elevenlabs | eleven_v4 | ✓ | ✓ | ✓ |
| elevenlabs | eleven_v3 | ✓ | ✓ | ✓ |
| elevenlabs | eleven_multilingual_v2 | ✓ | ✓ | — |
| cartesia | sonic-3.5-2026-05-04 ("Documented snapshot, not advertised as the latest Sonic.") | ✓ | ✓ | — |
| gemini | gemini-3.8-flash-tts | ✓ | ✓ | ✓ |
| gemini | gemini-3.8-flash-lite-tts | ✓ | ✓ | ✓ |
| openai | gpt-4o-mini-tts-2025-12-15 (legacy fixture) | ✓ | ✓ | — |

Admission ≠ approval: `pronunciation.expand` additionally refuses any locale with no editorially checked mapping — the shipped lexicon has **en-IN only**, so an `as-IN` or `hi-IN` plan that uses `{{tokens}}` fails until native mappings are added (tested by `test_no_unreviewed_language`). Language guidance from `docs/Voice_Identity_Guide.md`: "Do not write Assamese in Bengali just because a provider lists Bengali… A advertised supported locale is not a passed audition."

---

## 4. Open-source and self-hosted options (message 12 §3)

"Open-source TTS" is not one category. Code, pretrained weights, voice references, and commercial permissions must be checked separately.

| Project | Recommended ExamLeaf role | Important boundary |
|---|---|---|
| **Chatterbox** | First self-hosted expressive English/Hindi challenger | MIT project; select the correct multilingual model rather than assuming every variant has identical language support |
| **Indic Parler TTS** | Important self-hosted Assamese/Hindi audition candidate | Model card explicitly covers Indian languages, including Assamese; native quality still needs testing |
| **Kokoro 82M** | Lightweight preview or cost experiment | Apache-2.0 model; do not assume the exact release covers every requested Indian language |
| **CosyVoice** | Secondary research candidate | Inspected language coverage does not make it an automatic Hindi/Assamese solution |
| **Qwen3-TTS** | Additional expressive/voice-control candidate | Verify the exact release's language coverage and weight licence |
| **Fish Speech** | Research or separately licensed commercial candidate | Current repository uses a **FISH AUDIO RESEARCH LICENSE**; do not treat the "open source" label as unrestricted commercial permission |
| **F5-TTS** | Useful research and architecture reference | MIT code and **non-commercial pretrained-weight terms** are separate |

Chatterbox, Indic Parler, and Kokoro are the most relevant first self-hosted investigations for this project. Fish and F5 require particular licensing care. CosyVoice and Qwen3-TTS remain useful alternatives, but should not expand the deployment stack without a demonstrated language or quality advantage.

**Extra detail from the directory (`research/public_directory.csv`)** — licence note / boundary, verbatim except respacing:

| Project | Source | Licence note | Boundary |
|---|---|---|---|
| Chatterbox | https://github.com/resemble-ai/chatterbox | MIT as published; reference voice rights separate | Multilingual model documents Hindi. Turbo/Nano language coverage differs; not all variants multilingual. Assamese not established. No local inference benchmark. |
| Kokoro 82M | https://huggingface.co/hexgrad/Kokoro-82M | Apache 2 weights; review voices/dependencies | Small 82M model. Do not assume same expressive controls as premium systems. No Assamese support established. Voice/language table required before non-English production. |
| Fish Speech S2 | https://github.com/fishaudio/fish-speech | FISH AUDIO RESEARCH LICENSE for code and weights | Open repository is not an unrestricted commercial licence. Obtain suitable commercial authorization or provider contract. |
| F5-TTS | https://github.com/SWivid/F5-TTS | MIT code; default pretrained weights CC-BY-NC | Do not infer commercial permission from code licence. Replacement checkpoints need their own provenance/terms. (Use: "Research only with default weights for this commercial project".) |
| CosyVoice | https://github.com/QwenAudio/CosyVoice | Apache 2 code; check exact weights/assets | FunAudioLLM URL redirects. Current listed 9 languages omit Hindi/Assamese. Do not label it Indic-ready from general multilingual claims. |
| Qwen3-TTS | https://github.com/QwenLM/Qwen3-TTS | Apache 2 code/weights as published; voice rights separate | Documented language list does not establish Hindi/Assamese. No target-hardware or STEM audition performed. |
| Indic Parler TTS | https://huggingface.co/ai4bharat/indic-parler-tts | Apache 2 model metadata; gated download consent | Explicit Assamese and emotion-prompt documentation. Native review required. Newer Indic-Speak mention does not carry old model licence forward. |

### Self-hosting verdict (message 12 §3)

**Do not self-host first solely to save the TTS API fee.** Start self-hosting when one of these is demonstrated:

- A tested model provides a better required language or voice.
- Privacy/offline requirements justify it.
- Real usage exceeds the complete hosting, maintenance, and QA cost.
- Vendor independence is valuable enough to fund the engineering.

The supplied package does **not** include pretrained weights or claim that a neural TTS model was run locally. Final recommendation: "Keep self-hosted models as measured alternatives, not mandatory infrastructure."

### Supporting ASR / alignment / audio tools (directory entries 22–28)

| Tool | Role | Boundary |
|---|---|---|
| WhisperX (BSD 2 code; weights separate) | English alignment candidate with validated locale models | Number/currency tokens can lack times; language-specific aligner needed; overlapping speech weak. Do not run diarization for a single narrator by default. |
| faster-whisper (MIT runtime) | Independent baseline transcript comparison | Use audio-only decoding; do not supply expected answer text that biases away defects. Not installed here. |
| Montreal Forced Aligner (MIT code) | Offline phoneme alignment for supported language resources | Need matching phoneme dictionary and acoustic model, including STEM entries. Not a pronunciation oracle. |
| Silero VAD (MIT) | Optional speech/non-speech segmentation | Never remove protected think/write pauses automatically. Not installed here. |
| FFmpeg (LGPL/GPL by build) | Required decode, loudnorm, mux and final remeasurement | Two-pass loudness and sample-rate output executed on synthetic signal fixtures here. No speech-quality claim. |
| SoundFile + SciPy (BSD-style) | Local waveform timing/resampling/PCM QA | Installed environment used. Local normalized timeline and exact zeros demonstrated. No implicit denoising. |
| librosa (ISC) | Optional pitch/duration feature extraction | Pitch statistics and neural MOS are diagnostics, not grades for teaching/naturalness. Not installed for this package. |

---

## 5. Provider tariffs (as checked 13 October 2026)

### 5.1 Tariff reference table (workbook sheet `Provider_Tariffs`; "Public rates can change. Model, plan, minimum spend and licensing are not interchangeable. Legacy model prices must not drive a new launch.")

| Provider / method | Pricing basis | Example synthesis cost (per 10-min lesson) | Scope | Lifecycle / limit | Source |
|---|---|---|---|---|---|
| ElevenLabs v2/v3 reference | \$0.10 / 1,000 chars | \$0.936 | 9,360 generated characters | Reference budget, not verified v4 tariff | https://elevenlabs.io/pricing/api |
| Eleven v4 | Account/model quote required | TBD | Latest expressive audition candidate | Do not infer from v2/v3 or approximate $/minute marketing | https://elevenlabs.io/pricing/api |
| Gemini 3.8 Flash TTS — now | \$0.50 input / \$9 output per million | \$0.1392 | 612 generated seconds + estimated text | Current through 2026-12-31 per published schedule | https://ai.google.dev/gemini-api/docs/pricing |
| Gemini 3.8 Flash TTS — scheduled | \$1 input / \$18 output per million | \$0.2784 | Same workload | Scheduled from 2027-01-01; recheck | https://ai.google.dev/gemini-api/docs/pricing |
| Cartesia Pro | \$5 / 100,000 credits | Plan, not variable invoice | 1 character = 1 TTS credit | Allowance, concurrency and model constraints apply | https://cartesia.ai/pricing |
| Cartesia Startup | \$49 / 1.25 million credits | \$49 plan fits 936,000 chars | 100 lessons at the modeled length | Does not price 1,000 lessons | https://cartesia.ai/pricing |
| Cartesia Scale | \$299 / 8 million credits | 9.36 million exceeds this allowance | 1,000 modeled lessons | Obtain higher tier / overage quote | https://cartesia.ai/pricing |
| OpenAI realtime 2.1-mini | \$0.60 / M text input; \$20 / M audio output | Usage-dependent | Do not transplant Gemini token/second rate | New adapter and exact-script audition required | https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini |
| OpenAI old TTS models | Legacy migration fixture | Do not use for new production | Model shutdown 2027-01-06 | Official notice 2026-10-01 | https://developers.openai.com/api/docs/deprecations |
| Eleven speech-to-speech | \$0.12 / generated minute | \$1.224 | 10.2 generated minutes with retry allowance | Voice rights + human reference production separate | https://elevenlabs.io/pricing/api |
| Human performance | Illustrative \$30 / recording hour | Not a market quote | Recording time is NOT finished audio time | Buyouts, licensing and retakes must be quoted | Planning assumption |
| Self-hosted inference | Illustrative \$0.80 / GPU hour | \$0.272 | RTF 2, including 20% regeneration | No local neural TTS benchmark performed | Planning assumption |

### 5.2 Message 12 §13.2 text (verbatim)

The reference commercial calculation uses **\$0.10 per 1,000 characters**, a published v2/v3 rate—not an invented Eleven v4 price. With 20% regeneration:

$$
7{,}800\times1.2/1{,}000\times\$0.10=\$0.936
$$

The published speech-to-speech reference is **\$0.12 per generated minute**, before separate performer and review costs.

Gemini 3.8 Flash TTS currently lists **\$0.50/million input tokens and \$9/million audio output tokens**, with scheduled increases to **\$1 and \$18 from 1 January 2027**. Its pricing specifies 25 audio tokens per second. Under the workbook's workload, synthesis is approximately **\$0.139 now** or **\$0.278 at the scheduled rate**, before QA and labour.

Cartesia's plans list **\$5/100,000 credits, \$49/1.25 million, and \$299/8 million**. At 9,360 generated characters per lesson, 100 lessons fit within 1.25 million credits, but 1,000 lessons require 9.36 million—beyond the 8-million allowance. Obtain the actual overage or higher-tier quote rather than extrapolating a false fixed price.

### 5.3 The calculations, worked (formulas from the workbook `Provider_Tariffs` / `Methods` sheets)

| Item | Formula (workbook cell logic) | Result |
|---|---|---:|
| Generated characters / lesson | 7,800 × (1 + 0.20) | 9,360 |
| Premium TTS (v2/v3 reference) | 7,800 × 1.2 / 1,000 × \$0.10 | **\$0.936** |
| Speech-to-speech | 8.5 min × 1.2 × \$0.12 | **\$1.224** (10.2 generated min) |
| Gemini 3.8 Flash now | (8.5 × 60 s × 25 tok/s × \$9 + 2,500 input tok × \$0.50) × 1.2 / 1,000,000 = (114,750 + 1,250) × 1.2 / 10⁶ | **\$0.1392** |
| Gemini 3.8 Flash scheduled | (8.5 × 60 × 25 × \$18 + 2,500 × \$1) × 1.2 / 10⁶ = (229,500 + 2,500) × 1.2 / 10⁶ | **\$0.2784** |
| Gemini generated seconds | 8.5 × 60 × 1.2 | 612 s (15,300 audio tokens) |
| Self-hosted GPU | 8.5 × 60 × 1.2 × RTF 2 / 3,600 × \$0.80 | **\$0.272** |
| Cartesia, 100 lessons | 9,360 × 100 | 936,000 credits → fits the \$49 / 1.25 M plan |
| Cartesia, 1,000 lessons | 9,360 × 1,000 | 9.36 M credits → exceeds the \$299 / 8 M plan; quote needed |

`docs/Costs_and_Methods.md` restates: "Using 25 audio tokens/second, 2,500 input tokens and 20% regeneration, the modeled generation-only costs are \$0.1392 current and \$0.2784 scheduled. This excludes QA and labour." and "One TTS character consumes one credit… Obtain an overage/higher-tier quotation instead of pretending a linear \$299 price covers it." and "OpenAI old TTS models are deprecated; do not underwrite a new catalogue on them. The replacement realtime 2.1-mini has different model/route semantics and must be separately auditioned."

---

## 6. Costs for 1, 100 and 1,000 ten-minute videos (message 12 §13)

### 6.1 Scope

These estimates cover the **narration subsystem**, including script-direction allowance, synthesis, audio QA, editing, and the modeled human work. They do **not** include full academic research, animation production, platform marketing, or audience streaming. Avoid adding the same review cost twice when combining this workbook with the broader Video Engine budget (see `08_cost_models`). All values are **USD before tax**, using one monthly accounting period.

### 6.2 Baseline inputs (message 12 §13.1, extended with the workbook `Inputs` sheet)

| Input | Assumption | Unit | Source / caution (workbook) |
|---|---:|---|---|
| Finished media length | 10 | minutes | Planning assumption — Not all media time is spoken. |
| Active speech | 8.5 | minutes | Narration-only cost basis; response windows are inserted locally. |
| Spoken word budget | 1,200 | words | Pacing varies with complexity and language. *(workbook only)* |
| Transcript length | 7,800 | characters | Count actual final provider input in deployment. |
| Generation/retry allowance | 20% | fraction | Extra generated audio, not a guarantee of acceptance. |
| Premium TTS reference tariff | 0.10 | USD / 1,000 characters | v2/v3 published reference used for budget; NOT a verified Eleven v4 quote. |
| Speech-to-speech tariff | 0.12 | USD / generated minute | Confirm selected account/model; reference usage price. |
| LLM narration editing/direction | \$0.60 | / video | Incremental narration editing/direction only; not whole academic research. |
| ASR/alignment/automatic QA allowance | \$0.08 | / video | Service/compute budget, not a provider price guarantee. |
| Storage/export allowance | \$0.05 | / video | Excludes audience streaming and indefinite storage. |
| Academic audio reviewer | \$20 | / hour | Obtain actual native subject-reviewer quotations. |
| Audio editor | \$15 | / hour | Labour assumption, not a market survey. |
| Performer | \$30 | / recording hour | Illustrative; licensing/buyout fees require a separate agreement. |
| Illustrative GPU cost | \$0.80 | / hour | No GPU benchmark or supplier quote obtained. |
| Self-hosted real-time factor | 2 | compute s / generated s | Unbenchmarked; 2 means slower than real time. |
| Initial subsystem setup | \$4,000 | one-time | Optional separate initial implementation reserve; not in operating totals. |
| Gemini input token estimate | 2,500 | tokens / script | Includes direction; actual billed token count governs. |
| Gemini audio tokens / sec | 25 | tokens / second | Model pricing calculation convention; verify usage records. |
| Gemini 3.8 input (now / from 2027-01-01) | 0.50 / 1 | USD / M input tokens | Before / scheduled rate change; recheck before use. |
| Gemini 3.8 output (now / from 2027-01-01) | 9 / 18 | USD / M audio tokens | Before / scheduled rate change; recheck before use. |

Personnel rates, processing times, retry rate, and GPU figures are **editable planning assumptions, not quotations or measured TTS benchmarks**.

### 6.3 Five production methods (message 12 §13.3 table, verbatim)

| Method | Variable cost/video | Monthly fixed allowance | 1 video | 100 videos | 1,000 videos |
|---|---:|---:|---:|---:|---:|
| **Premium commercial TTS** | **\$12.50** | \$100 | **\$112.50** | **\$1,349.93** | **\$12,599.33** |
| Primarily self-hosted | \$14.75 | \$300 | \$314.75 | \$1,775.20 | \$15,052.00 |
| Human recorded | \$42.40 | \$100 | \$142.40 | \$4,339.67 | \$42,496.67 |
| Human performance + speech-to-speech | \$34.87 | \$125 | \$159.87 | \$3,612.07 | \$34,995.67 |
| Hybrid: 80% TTS, 20% performed/converted | \$17.06 | \$150 | \$167.06 | \$1,855.69 | \$17,206.93 |

The table assumes different review/editing workloads for each method. **It does not prove that self-hosting inherently costs more.** At equal labour requirements, it can be cheaper; actual retakes and maintenance decide the result.

### 6.4 How each variable cost is built (workbook `Methods` sheet)

Machine/video = \$0.73 (LLM 0.60 + QA 0.08 + storage 0.05) + TTS fraction × \$0.936 + STS fraction × \$1.224 + GPU flag × \$0.272.
Human/video = record hours × \$30 + review min/60 × \$20 + edit min/60 × \$15. Total for N videos = N × variable + monthly fixed. Hours at 1,000 = human min/video × 1,000 / 60.

| Method | TTS frac | Record h | STS frac | Review min | Edit min | GPU | Fixed/month | Machine/video | Human/video | Variable/video | Human min/video | Human hours /1,000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Premium commercial TTS | 1 | 0 | 0 | 25 | 10 | 0 | \$100 | \$1.666 | \$10.833 | \$12.499 | 35 | 583.3 |
| Primarily self-hosted | 0 | 0 | 0 | 30 | 15 | 1 | \$300 | \$1.002 | \$13.750 | \$14.752 | 45 | 750.0 |
| Human recorded | 0 | 1 | 0 | 20 | 20 | 0 | \$100 | \$0.730 | \$41.667 | \$42.397 | 100 | 1,666.7 |
| Human performance + STS | 0 | 0.75 | 1 | 20 | 15 | 0 | \$125 | \$1.954 | \$32.917 | \$34.871 | 80 | 1,333.3 |
| Hybrid: 80% TTS / 20% performed | 0.8 | 0.15 | 0.2 | 25 | 10 | 0 | \$150 | \$1.724 | \$15.333 | \$17.057 | 44 | 733.3 |

(`docs/Costs_and_Methods.md` words it as: "Premium review/edit time is 25+10 minutes. Self-hosted 30+15; human recording 60+review 20+editing 20; performance/STS 45+review 20+editing 15; hybrid 9+review 25+editing 10. Hybrid assumes 80% TTS and 20% human-performed/STS." The workbook note: "Operating assumptions for mature workflows. Novel STEM terms, native-language validation and first-use performances can require additional work.")

Workbook `Summary` sensitivity rows: add initial subsystem setup separately **\$4,000**; Premium / 1,000 including initial setup **\$16,599.33**; Premium / 1,000 with review time doubled **\$20,932.67**. Notes: "Assumptions, not vendor quotes, controlled provider benchmarks, or guaranteed quality equivalence." · "Do not add these audio-review costs twice if already included in your full video-production budget." · Excluded: "Tax, voice buyouts, extended licensing, audience streaming, full animation, broad academic research and extra localization." · Scaling: "One locale/version per case. A second language requires new performance, QA and timeline verification." Raw unrounded values: `narration_system_v1/outputs/cost_summary.json`.

### 6.5 The dominant cost (message 12 §13)

The premium case allows **25 minutes of academic audio review and ten minutes of editing per video**. At 1,000 videos, that is approximately **583 human hours**. Reducing generation from roughly one dollar to a few cents matters less than eliminating avoidable pronunciation and synchronization repairs. An illustrative **\$4,000 initial narration-subsystem implementation reserve** is separate. Voice buyouts, broader licences, substantial new localization, and hardware purchases require additional budgeting.

`docs/Costs_and_Methods.md` scope exclusions: "Full academic source research, animation generation/rendering, platform distribution, audience streaming, taxes, large commercial voice buyouts, purchased GPU hardware and additional locales are not silently included. Native-language review and new complex terminology may require more time than this baseline. A low synthesis price is not evidence that the lesson is good."

---

## 7. Provider admission checklist (`docs/Provider_Lifecycle.md`)

Record provider, API version, exact model ID, lifecycle dates, voice rights, voice ID, locale, permitted controls, audio format, rate/concurrency limits, estimate/actual usage, sample hashes and reviewer approvals. **Only a successful request plus content and listening checks can promote a recipe into a production integration.**

Production gates already coded in `compile_plan(..., production=True)` (in this order): deprecated model → "Deprecated model: new production blocked; migrate before 2027-01-06"; `rights_status` not `licensed-stock`/`consented-custom` → "Production voice rights not cleared"; `live_contract_verified` false → "Live endpoint contract not approved"; voice ID containing "REPLACE" → "Replace placeholder voice ID". Additional always-on checks: lexicon version must match the plan; a single segment's spoken text over 1,800 characters → "Split at a sentence boundary; 1800-character scaffold segment cap".

Do not silently replace a voice when a provider fails. A fallback must be an approved voice/model combination, or the job should wait (message 12 §12.3). `docs/Architecture.md`: "Where vendor voices expire or change, preserve lawfully retained approved output; alert and audition replacement rather than silently switching."

## 8. Final recommendation (message 12)

**Launch with commercially generated narration, a carefully cast and licensed voice, explicit pronunciation control, and selective human performance where it genuinely improves the teaching.** Keep self-hosted models as measured alternatives, not mandatory infrastructure. Keep the voice provider replaceable, but the approved teaching language, terminology, timing, and academic standards under ExamLeaf's control.

## Addendum, 16 Oct 2026: live check of Eleven v4 and the ElevenLabs MCP

Read from the live dashboard and docs in the founder's browser; see `ELEVENLABS_SETUP_2026-10-16.md` for the full record. Confirmed: `eleven_v4` exists and is served by `POST /v1/text-to-dialogue` (the compiler's route); v3 is "previous generation". New constraints: keep each dialogue request at or below 2,000 characters across inputs; `model_id` must be sent (the route defaults to v3); PCM/WAV output requires Pro; `seed` is best-effort; up to three pronunciation-dictionary locators per request; `previous_request_ids` gives continuity across beats. `eleven_multilingual_sts_v2` lists Hindi, which settles the Hindi speech-to-speech question at the documentation level. The local `elevenlabs-mcp` package is deprecated; the hosted OAuth MCP (`https://api.us.elevenlabs.io/v1/mcp` for Claude Code) is registered and awaits authorisation. No audio was generated and no key exists yet.
