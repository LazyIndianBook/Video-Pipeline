# Sources and Claims Register: New Evidence (N1–N76)

**Research date:** 14 Oct 2026.

**Status meanings**
- **Unanimous:** every verifier confirmed it.
- **Contested:** not every verifier confirmed it. Re-check it before you rely on it.

**Earlier claims** [P-S1]–[P-S39] (Sarvam capabilities, the listener-perception study, microdrama market facts, YouTube auto-labelling, Zee v. Nykaa music licensing) are in `/Users/chinmoybhuyan/Desktop/Personal/Book/Videos/ExamLeaf_Video_EdTech_Pipeline/11_human_feel_voice_audio_research/SOURCES_and_claims.md`.

| ID | Claim | Quote | URL | Kind | Status |
|---|---|---|---|---|---|
| N1 | SSML break tags give pauses up to 3 s on supported models | "Use `<break time="x.xs" />` for natural pauses up to 3 seconds." | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N2 | Eleven v4 and v3 do not support SSML break tags | "Eleven v4 and Eleven v3 do not support SSML break tags." | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N3 | Speed minimum 0.7 | "Values below 1.0 will slow the voice down, to a minimum of 0.7." | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N4 | Speed maximum 1.2 | "Values above 1.0 will speed up the voice, to a maximum of 1.2." | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N5 | Default speed 1.0 | "The default value is 1.0, which means that the speed is not adjusted." | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N6 | Phoneme tags only with eleven_flash_v2 | "Phoneme tags are only compatible with the `eleven_flash_v2` model" | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N7 | Text normalization on by default | "Normalization is enabled by default for all TTS models" | https://elevenlabs.io/docs/best-practices/prompting | official-doc | Unanimous |
| N8 | Bulbul v3: 11 languages, 30+ voices | "`bulbul:v3` speaks 11 languages (10 Indian + English) with 30+ voices" | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N9 | TTS codecs include mulaw/alaw plus mp3/wav/opus | "`output_audio_codec` supports `mulaw` and `alaw` alongside `mp3`, `wav`, `opus`, etc." | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N10 | REST STT up to 30 s; Batch API for longer | "The REST endpoint handles clips up to 30 seconds, for longer audio use the Batch API" | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N11 | Streaming STT accepts only WAV and raw PCM | "Streaming STT accepts WAV and raw PCM (`pcm_s16le`, `pcm_l16`, `pcm_raw`) only." | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N12 | 8 kHz streaming needs sample_rate=8000 on connection and chunks | "set `sample_rate=8000` both when opening the streaming connection and when sending each audio chunk" | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N13 | Sarvam Vision: 23 languages | "23 languages (22 Indian + English)" | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N14 | Doc translation: up to 12 targets per job | "pick up to 12 target languages per job" | https://docs.sarvam.ai/api/getting-started/building-for-india | official-doc | Unanimous |
| N15 | Voice Changer input under 50 MB | "The audio file must be less than 50mb in size" | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N16 | Input capped at 5 minutes | "cannot exceed 5 minutes in length" | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N17 | Cost 1,000 characters per minute | "The cost for a voice changer generation is solely duration-based at 1000 characters per minute." | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N18 | Recording consumes no credits | "you will not be charged this quota for recording anything" | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N19 | Multilingual v2: 29 languages | "Our multilingual v2 models support 29 languages" | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N20 | eleven_english_sts_v2 English only | "The eleven_english_sts_v2 model only supports English." | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N21 | Inputs: MP3, M4A, FLAC, OGA, OGG, WAV | "MP3, M4A, FLAC, OGA, OGG, WAV" | https://elevenlabs.io/docs/product-guides/playground/voice-changer | official-doc | Unanimous |
| N22 | High-pass AI vocals 80–100 Hz | "High-pass filtering (80-100 Hz)" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N23 | Presence 2–5 kHz | "Presence enhancement (2-5 kHz)" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N24 | Subtle 1–2 dB shelf boosts | "Apply subtle shelf boosts of 1-2 dB" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N25 | Attack 10–30 ms | "Slower attack times (10-30 milliseconds)" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N26 | Ratio 3:1–4:1 | "Moderate compression ratios (3:1 to 4:1)" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N27 | Release 100–300 ms | "Optimal release times (100-300 milliseconds)" | https://www.sonarworks.com/blog/learn/mastering-ai-vocals-eq-and-compression-tips | blog | Unanimous |
| N28 | Microdrama episodes ~100 M views | "most episodes gaining 100 million views per episode" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Contested |
| N29 | 60-episode series sound design in 2–3 weeks | "A 60-episode vertical drama series may require complete sound design within two or three weeks" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N30 | Absence of ambience / isolated sound sharpens the next beat | "a sudden absence of ambience, an isolated breath, or a subtle Foley detail" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N31 | Low frequencies lose impact on phone speakers | "Since low frequencies can lose their impact on mobile speakers" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N32 | Test on monitors, headphones, phones | "continuously testing mixes across studio monitors, headphones, and mobile devices" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N33 | Attention-grabbing sounds for irreversible turns | "Attention-grabbing sounds mark irreversible story turns" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N34 | Sound expands the world beyond the 9:16 frame | "The restricted frame reveals less surrounding environment, so sound expands the world beyond the image" | https://www.music-news.com/news/Underground/190732/Minjia-Du-talks-subtle-sound-design-for-booming-vertical-drama-industry | news | Unanimous |
| N35 | Ipsos: audio assets 3.44x more effective than visual | "audio assets were, on average, 3.44 times more effective than visual assets" | https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539 | research | Contested |
| N36 | Sonic identities ~5% perceived value lift | "brands that have recognizable sonic identities can see an average 5% increase in their perceived value" | https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539 | research | Unanimous |
| N37 | YouGov: 20% of young adults more inclined to buy | "20% of young adults were more inclined to buy a product from a brand with a sonic identity" | https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539 | research | Unanimous |
| N38 | Case: +38% recall, +70% appeal | "38% increase in brand recall, a 13% increase in brand score, and a 70% increase in overall appeal" | https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539 | research | Unanimous |
| N39 | Retail background music: 7.7% lower perceived value | "there was actually a 7.7% reduction in perceived value." | https://ora.ox.ac.uk/objects/uuid:a3db49b9-75e6-41c9-b31e-586b4f76b605/files/rt148fj539 | research | Unanimous |
| N40 | YouTube requires disclosure of realistic altered/synthetic content | "we require creators to disclose when they use AI to meaningfully alter or generate photorealistic content." | https://support.google.com/youtube/answer/14328491 | official-doc | Contested |
| N41 | Making a real person appear to say/do something is disclosable | "Makes a real person appear to say or do something they didn't do." | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N42 | Non-realistic AI content needs no disclosure | "Creators don't need to disclose non-realistic content that's made with AI" | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N43 | Own-voice cloning for voice-overs is exempt | "Cloning one's own voice to create voice overs or dubs" | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N44 | Non-photoreal/animated may get description label | "Labels may appear in the expanded description for AI content that is non-photorealistic or animated." | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N45 | YouTube may auto-apply AI labels (incl. C2PA) | "YouTube may automatically apply an AI label on the video player or in the expanded description" | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N46 | Non-disclosure can lead to labels, removal, YPP suspension | "may be subject to manual application of a label, or penalties from YouTube, including removal of content" | https://support.google.com/youtube/answer/14328491 | official-doc | Unanimous |
| N47 | ElevenLabs skills install via npx | "npx skills add elevenlabs/skills" | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Unanimous |
| N48 | Skills follow the Agent Skills spec | "They follow the Agent Skills specification and can be used with compatible coding assistants." | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Unanimous |
| N49 | STT skill returns speaker IDs + paragraph timestamps | "Return a transcript that contains speaker IDs and timestamps at the start of each paragraph." | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Contested |
| N50 | Realtime skill uses scribe_v2_realtime with word timestamps | "scribe_v2_realtime" | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Contested |
| N51 | Voice changer skill preserves delivery (eleven_multilingual_sts_v2) | "Transform a recording into a different target voice while preserving the original delivery." | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Contested |
| N52 | Speech Engine skill adds voice to a chat agent | "Speech Engine skill" | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Contested |
| N53 | Hosted MCP with OAuth, no local install | "It uses OAuth sign-in with your ElevenLabs account and requires no local installation." | https://elevenlabs.io/docs/eleven-api/resources/agent-tooling | official-doc | Unanimous |
| N54 | Eleven v4 inline audio tags | "using inline tags like [laughs], [said angrily in French accent], [light rain], or [phone buzzing]." | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N55 | v4 / v4 Turbo: 90+ languages (Hindi not named) | "Both Eleven v4 and Eleven v4 Turbo support more than 90 languages." | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N56 | IVC from ~10 s of audio | "Instant Voice Clones can now capture voices with high fidelity using just 10 seconds of audio." | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N57 | ~75% blind preference for v4 (vendor claim) | "preferred by ~75% of listeners in blind head-to-head tests over competing models" | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N58 | v4 supports Professional Voice Clones | "Eleven v4 also adds support for Professional Voice Clones (PVC), for the highest-fidelity cloning use cases." | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N59 | Availability in ElevenAgents/Creative/API; no pricing on page | "Both models are available now in ElevenAgents, ElevenCreative, and via ElevenAPI." | https://elevenlabs.io/blog/eleven-v4 | official-doc | Unanimous |
| N60 | Only the matching language_code block applies | "When `language_code` is `hi-IN`, only the `hi-IN` block applies." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N61 | Dictionary cap 100 words | "you have 100 words to work with." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N62 | One dict_id per request | "One dictionary per request." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N63 | Plain JSON, no phoneme markup | "Save this as a `.json` file. That's it, no XML, no special phoneme notation, no markup." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N64 | cURL upload needs ;type=application/json | "The `;type=application/json` suffix is required." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N65 | Updating keeps the same dict_id | "The `dict_id` stays the same, so your TTS integrations keep working." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N66 | dict_id works across REST, HTTP Stream, WebSocket | "The `dict_id` parameter works across REST, HTTP Stream, and WebSocket." | https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary | official-doc | Unanimous |
| N67 | Segmind voice changer ~$0.00375/s (~$0.225/min); $0.0037 quoted elsewhere | "$0.00375 per second of output duration" | https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/ | blog | Unanimous |
| N68 | eleven_english_sts_v2 English-only; multilingual exists | "eleven_english_sts_v2 is optimized for English only." | https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/ | blog | Contested |
| N69 | Optional noise isolation before conversion | "applies ElevenLabs noise isolation to the input before conversion." | https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/ | blog | Unanimous |
| N70 | Segmind latency under 7 s (author observation) | "the bus-to-bus latency on Segmind is consistently under 7 seconds." | https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/ | blog | Unanimous |
| N71 | Trailing silence billed as output | "any trailing silence in the input becomes paid silence in the output." | https://blog.segmind.com/elevenlabs-voice-changer-how-to-convert-voices-in-2026/ | blog | Unanimous |
| N72 | Gentle 2:1–3:1 compression on AI vocals | "Gentle ratio settings (2:1 to 3:1)" | https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals | blog | Unanimous |
| N73 | Ratios above 4:1 make AI vocals lifeless | "Ratios above 4:1 quickly transform AI vocals into lifeless, flat elements" | https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals | blog | Unanimous |
| N74 | Attack 15–30 ms preserves transients | "Attack times between 15–30 ms allow initial transients through" | https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals | blog | Unanimous |
| N75 | Release 100–300 ms matched to rhythm | "release times of 100–300 ms match track tempo and rhythm" | https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals | blog | Unanimous |
| N76 | Parallel compression at 6:1+ blended low | "Mix heavily compressed AI vocals (6:1 ratio or higher) at low levels with unprocessed signals" | https://www.sonarworks.com/blog/learn/compression-strategies-for-ai-generated-backing-vocals | blog | Unanimous |
