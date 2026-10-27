# Provider lifecycle and capability admission — 13 October 2026

## OpenAI: important migration, not a new-production default
The official deprecation notice dated 1 October 2026 schedules tts-1, tts-1-hd, gpt-4o-mini-tts-2025-03-20 and gpt-4o-mini-tts-2025-12-15 for shutdown on 6 January 2027. It names gpt-realtime-2.1-mini as replacement. Old guides and Skills still contain older model examples. The lifecycle notice takes precedence over those cached examples.

The bundled openai_snapshot.json is an offline migration fixture. compile_plan(..., production=True) rejects it even if local voice-rights and endpoint booleans are supplied. This project does not implement the realtime replacement or claim exact-script compliance on it. Its documented model rates are $0.60/M text input tokens and $20/M audio output tokens; do not transplant another vendor's audio token-per-second convention.

Sources: https://developers.openai.com/api/docs/deprecations ; https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini

## ElevenLabs
Eleven v4 is the current expressive audition candidate. The compiler uses its documented text-to-dialogue route, separate from earlier text-to-speech examples. It does not copy older speed/style or SSML controls into v4. v4/v3 language documentation lists Assamese, but model-level availability is not a successful native-language audition. Stock-voice IDs are provider-specific; a Runway voice preset name is not a direct ElevenLabs API voice ID.

Sources: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 ; https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support

## Cartesia
Sonic3.6 is the current marketed model. This package's request recipe uses a documented Sonic3.5 snapshot, explicitly labelled as such. Select the actual live model identifier, API version, voice and language contract in a new tested adapter. Do not rename a snapshot and pretend it was tested. Hindi/code-switching suitability must be auditioned; Assamese is not admitted by this scaffold.

Sources: https://docs.cartesia.ai/build-with-cartesia/tts-models/latest ; https://cartesia.ai/pricing

## Gemini
Current3.8 TTS uses the Interactions schema in the primary recipe, with exact spoken text separate from speech_metadata.style. The legacy Generate Content route has a DIFFERENT schema. Unary3.8 audio is WAV, while streaming commonly uses headerless PCM. Do not prepend a second header or concatenate complete WAV containers as raw samples. Custom voice storage/expiry limits matter for a stable brand voice; record expiry and renewal obligations.

Both3.8 Flash and Flash-Lite list Assamese/Hindi. Neither has been live-synthesized here. Current Flash pricing is $0.50/M input and $9/M output tokens; the announced2027-01-01 prices are $1/$18 respectively. Pricing specifies25 audio tokens/second. Account terms, caps and actual usage govern invoices.

Sources: https://ai.google.dev/gemini-api/docs/speech-generation ; https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-lite-tts ; https://ai.google.dev/gemini-api/docs/pricing

## Admission checklist
Record provider, API version, exact model ID, lifecycle dates, voice rights, voice ID, locale, permitted controls, audio format, rate/concurrency limits, estimate/actual usage, sample hashes and reviewer approvals. Only a successful request plus content and listening checks can promote a recipe into a production integration.
