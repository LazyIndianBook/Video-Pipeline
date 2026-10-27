# Public narration and audio directory

Checked 13 October 2026. Research-read is not live-tested. Service charges, voice rights, model weights and source-code licences are separate. No third-party repositories were blindly installed.

## 1. ElevenLabs official Skills
**Type:** Skill repository. **Source:** https://github.com/elevenlabs/skills

**Licence:** MIT Skill code; hosted services/voices separate

**Use:** Reuse selected TTS/STT/voice-changer/cleanup/dubbing guidance

**Boundary:** Ten Skills in inspected README. Python elevenlabs; JS @elevenlabs/elevenlabs-js. No need live conversational agent Skills for prerecorded lessons.

## 2. ElevenLabs MCP
**Type:** Official MCP server. **Source:** https://github.com/elevenlabs/elevenlabs-mcp

**Licence:** MIT bridge; account charges apply

**Use:** Supervised audition/asset operations

**Boundary:** MCP is tool access, not TTS quality or permission sandbox. Prefer SDK worker for bulk production.

## 3. Eleven v4
**Type:** Hosted TTS API. **Source:** https://elevenlabs.io/docs/changelog/2026/9/28

**Licence:** Commercial API/account and voice terms

**Use:** Primary expressive candidate; audition first

**Boundary:** Released 28 Sep 2026. v4 and turbo differ. v4 no SSML or legacy speed/style sliders. Text-to-dialogue documented; endpoint feature parity must be tested.

## 4. Eleven pronunciation
**Type:** Provider dictionary/API. **Source:** https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries

**Licence:** Provider terms

**Use:** Audited model-specific dictionary, aliases as portable base

**Boundary:** Dictionary phonemes are not universal SSML support. Newer API docs and Studio guides differ; pin exact endpoint/model/dictionary version.

## 5. Eleven forced alignment
**Type:** Hosted alignment API. **Source:** https://elevenlabs.io/docs/api-reference/forced-alignment/create

**Licence:** Usage fee/account terms

**Use:** Baseline timeline alignment candidate

**Boundary:** Aligns supplied text and audio; not an independent scientific/pronunciation test.

## 6. Cartesia official Skills
**Type:** Skill repository. **Source:** https://github.com/cartesia-ai/skills

**Licence:** MIT Skill code

**Use:** cartesia-api; not line-voice-agent for recorded lessons

**Boundary:** Use selected instructions only. Installation does not create a licensed voice or guarantee provider contract compatibility.

## 7. Cartesia MCP
**Type:** Official MCP server. **Source:** https://github.com/cartesia-ai/cartesia-mcp

**Licence:** Check pinned repository licence and service terms

**Use:** Supervised audition, optional

**Boundary:** Do not add production orchestration merely to wrap a REST request.

## 8. Cartesia Sonic
**Type:** Hosted TTS API. **Source:** https://docs.cartesia.ai/build-with-cartesia/tts-models/latest

**Licence:** Commercial service

**Use:** English/Hindi cost-quality challenger

**Boundary:** Sonic3.6 appears on current product pages; checked API documentation snapshot was 3.5. Scaffold pins 3.5-2026-05-04, not a claim that 3.5 is latest. Assamese not established by this audit.

## 9. Gemini TTS
**Type:** Hosted API, not a Skill. **Source:** https://ai.google.dev/gemini-api/docs/speech-generation

**Licence:** Commercial API terms; free/paid data policies differ

**Use:** 3.8 Flash expressive challenger; Flash-Lite high-throughput comparison

**Boundary:** Latest indexed guide: structured speech_metadata, verbatim text, angle-bracket event tags, unary WAV. Old cached guide still showed3.1. Assamese documented in current language list; native audition mandatory.

## 10. OpenAI speech
**Type:** Hosted API. **Source:** https://developers.openai.com/api/docs/guides/text-to-speech

**Licence:** Commercial API; licensed/custom voice controls

**Use:** Evaluate realtime2.1-mini migration; do not launch on legacy TTS

**Boundary:** Official deprecation notice dated2026-10-01 schedules the old TTS snapshots for shutdown2027-01-06. Replacement is gpt-realtime-2.1-mini. Old recipe is an OFFLINE MIGRATION FIXTURE blocked for production. Realtime replacement requires a new live-tested adapter; it is not assumed a drop-in endpoint. Assamese not admitted by scaffold.

## 11. OpenAI curated speech Skill
**Type:** Official Skill. **Source:** https://github.com/openai/skills/tree/main/skills/.curated/speech

**Licence:** Review exact repo/files licence

**Use:** Adapt script and CLI patterns

**Boundary:** Not proof current commands/model defaults are ideal for ExamLeaf. Model/endpoint contracts override old Skill snippets.

## 12. Remotion Skills
**Type:** Official renderer Skills. **Source:** https://github.com/remotion-dev/skills

**Licence:** Skills and renderer/service licensing are separate

**Use:** remotion-captions, remotion-render, remotion-multimedia

**Boundary:** Remotion composes media; it is not a voice model. Drive <Sequence> and <Audio> from measured global timeline. No Remotion runtime tested in this package.

## 13. Anthropic Skills
**Type:** Official Skill examples. **Source:** https://github.com/anthropics/skills

**Licence:** Many Apache2; document Skills source-available separately

**Use:** skill-creator for evaluations; webapp-testing for reviewer UI

**Boundary:** No inherited assertion that a Skill is production-safe. Review scripts and allowed tools.

## 14. Manim Voiceover
**Type:** Community Manim extension. **Source:** https://github.com/ManimCommunity/manim-voiceover

**Licence:** Review pinned extension/dependency licence

**Use:** Optional Manim clip synchronization

**Boundary:** Use preapproved clips and bookmarks. Do not synthesize again inside every render. Not needed for the native timing proof.

## 15. Chatterbox
**Type:** Open-weight model and library. **Source:** https://github.com/resemble-ai/chatterbox

**Licence:** MIT as published; reference voice rights separate

**Use:** First self-hosted English/Hindi challenger

**Boundary:** Multilingual model documents Hindi. Turbo/Nano language coverage differs; not all variants multilingual. Assamese not established. No local inference benchmark.

## 16. Kokoro82M
**Type:** Open-weight model. **Source:** https://huggingface.co/hexgrad/Kokoro-82M

**Licence:** Apache2 weights; review voices/dependencies

**Use:** Economical English drafts and listening challenger

**Boundary:** Small82M model. Do not assume same expressive controls as premium systems. No Assamese support established. Voice/language table required before non-English production.

## 17. Fish Speech S2
**Type:** Research-licensed model/code. **Source:** https://github.com/fishaudio/fish-speech

**Licence:** FISH AUDIO RESEARCH LICENSE for code and weights

**Use:** Research candidate; not default commercial self-hosting

**Boundary:** Open repository is not an unrestricted commercial licence. Obtain suitable commercial authorization or provider contract.

## 18. F5-TTS
**Type:** Open code / restricted default weights. **Source:** https://github.com/SWivid/F5-TTS

**Licence:** MIT code; default pretrained weights CC-BY-NC

**Use:** Research only with default weights for this commercial project

**Boundary:** Do not infer commercial permission from code licence. Replacement checkpoints need their own provenance/terms.

## 19. CosyVoice
**Type:** Open model/library. **Source:** https://github.com/QwenAudio/CosyVoice

**Licence:** Apache2 code; check exact weights/assets

**Use:** Secondary English research candidate

**Boundary:** FunAudioLLM URL redirects. Current listed9 languages omit Hindi/Assamese. Do not label it Indic-ready from general multilingual claims.

## 20. Qwen3-TTS
**Type:** Open model/library. **Source:** https://github.com/QwenLM/Qwen3-TTS

**Licence:** Apache2 code/weights as published; voice rights separate

**Use:** Secondary expressive English candidate

**Boundary:** Documented language list does not establish Hindi/Assamese. No target-hardware or STEM audition performed.

## 21. Indic Parler TTS
**Type:** Indic open-weight TTS. **Source:** https://huggingface.co/ai4bharat/indic-parler-tts

**Licence:** Apache2 model metadata; gated download consent

**Use:** Assamese/Hindi self-hosted comparison

**Boundary:** Explicit Assamese and emotion-prompt documentation. Native review required. Newer Indic-Speak mention does not carry old model licence forward.

## 22. WhisperX
**Type:** ASR + forced alignment library. **Source:** https://github.com/m-bain/whisperX

**Licence:** BSD2 code; alignment/diarization weights separate

**Use:** English alignment candidate with validated locale models

**Boundary:** Number/currency tokens can lack times; language-specific aligner needed; overlapping speech weak. Do not run diarization for a single narrator by default.

## 23. faster-whisper
**Type:** ASR runtime. **Source:** https://github.com/SYSTRAN/faster-whisper

**Licence:** MIT runtime; model files separately reviewed

**Use:** Independent baseline transcript comparison

**Boundary:** Use audio-only decoding; do not supply expected answer text that biases away defects. Not installed here.

## 24. Montreal Forced Aligner
**Type:** Forced alignment toolkit. **Source:** https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner

**Licence:** MIT code; acoustic/lexicon model licences separate

**Use:** Offline phoneme alignment for supported language resources

**Boundary:** Need matching phoneme dictionary and acoustic model, including STEM entries. Not a pronunciation oracle.

## 25. Silero VAD
**Type:** Voice activity model/tool. **Source:** https://github.com/snakers4/silero-vad

**Licence:** MIT as published; verify pinned assets

**Use:** Optional speech/non-speech segmentation

**Boundary:** Never remove protected think/write pauses automatically. Not installed here.

## 26. FFmpeg
**Type:** Audio/media executable. **Source:** https://ffmpeg.org/ffmpeg-filters.html

**Licence:** LGPL/GPL depending build/codecs

**Use:** Required decode, loudnorm, mux and final remeasurement

**Boundary:** Two-pass loudness and sample-rate output executed on synthetic signal fixtures here. No speech-quality claim.

## 27. SoundFile + SciPy
**Type:** Audio IO and DSP libraries. **Source:** https://python-soundfile.readthedocs.io/

**Licence:** BSD-style code; libsndfile separate

**Use:** Local waveform timing/resampling/PCM QA

**Boundary:** Installed environment used. Local normalized timeline and exact zeros demonstrated. No implicit denoising.

## 28. librosa
**Type:** Audio analysis library. **Source:** https://librosa.org/doc/latest/index.html

**Licence:** ISC code; dependencies separate

**Use:** Optional pitch/duration feature extraction

**Boundary:** Pitch statistics and neural MOS are diagnostics, not grades for teaching/naturalness. Not installed for this package.

## Install and update protocol
Read the repository and selected SKILL.md, scripts, package manifests, network endpoints and credential access first. Pin a real commit and dependency lock; do not mistake a file blob SHA for a commit. Copy only approved Skills into a project-local path. The public convenience commands `npx skills add elevenlabs/skills`, `npx skills add cartesia-ai/skills`, and `npx skills add remotion-dev/skills` are discovery/install routes, not audit procedures. This package did not execute them.

Claude Code: project `.claude/skills/<skill>/SKILL.md`. Codex: project `.agents/skills/<skill>/SKILL.md`; check client-specific current behavior. Use one canonical source folder and controlled sync, not diverging copies.

MCP adds tool access inside authoring clients. SDK/REST workers own unattended synthesis, job IDs, secret handling, spending limits and retry state. A Skill is neither a TTS model nor a runtime permission sandbox.

## Documentation drift
Some directly opened pages were cached months earlier while current indexed official pages described newer models. Keep a dated capability manifest. Eleven v4 no longer accepts all v2-style settings. Sonic3.6 is marketed but this scaffold compiles a documented3.5 snapshot; do not silently label the recipe3.6. Gemini3.8 differs from legacy3.1 prompt and audio-output handling. OpenAI deprecated its older TTS models on2026-10-01; shutdown is2027-01-06. Its older guide remains indexed, but the lifecycle notice controls new deployment decisions. Admission means a successful live contract test plus listening evaluation, not reading a launch post.
