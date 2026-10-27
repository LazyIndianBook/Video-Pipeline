# Narration system architecture

## Production graph
Approved source-linked claims → teacher draft → naturalizer/story/interaction review → academic script approval → Direction and context-aware pronunciation mappings → provider request compilation → rights/model/budget admission → one synthesis job per coherent segment → persist job ID and raw audio → independent ASR → script diff and critical-word review → forced alignment against exact accepted speech → semantic visual anchors → sample-index composition with protected pauses → captions → whole-track mastering → final encode/re-measure → native/academic/full-viewing approval bound to hashes.

## Status of this implementation
Local implementation: typed contracts, explicit lexicon expansion, five provider request recipe profiles, four provider branches, cache keys/file integrity, retry-decision logic, normalized word comparison, validated alignment import, global sample→frame mapping, PCM assembly with protected pauses, prototype VTT export, signal/silence QA, two-pass FFmpeg mastering and fail-closed release report.

Not implemented: authenticated provider REST transport, provider-side forced-alignment execution, independent ASR inference, locale-specific Indic ASR normalization, distributed queue, identity-authenticated reviewer service, fully mastered approved narration lesson or student outcome tests. Synthetic alignment timestamps are test data, never claimed as acoustic alignment.

## Connect to the existing engine
Leave existing Python scientific verification and renderer adapters unchanged. Add `narration_plan_uri` and `narration_manifest_sha256` to the lesson manifest. Pass accepted `timeline.events` to scene adapters; each includes the cue, element, action, global sample and output frame. Replace estimated scene lengths with measured clip/hold intervals. Rendering may be repeated freely without resynthesizing speech. Export science visual and spoken-caption alternatives separately; a symbol-focused caption view must not erase accessible spoken meaning.

Each locale has independent voice/lexicon/audio/timing objects. Do not time-stretch the translation into English durations. Hash actual provider/model/voice and pronunciation versions. Where vendor voices expire or change, preserve lawfully retained approved output; alert and audition replacement rather than silently switching.

## Segments
Typical target: coherent one-to-three-sentence or roughly15–35-second units. Not a fixed rule. Do not synthesize every sentence separately: unnecessary boundaries harm continuity and create overhead. Split questions from answer reveals; insert exact think time locally. For long formulas, spoken semantic phrases need matching visual groups. Use sample-rate48k for final master; providers may natively return24k/44.1k. Resampling does not recreate missing high-frequency detail.

## Independent checks
Alignment validates where accepted words are placed; independent ASR asks what might actually have been spoken. Even zero ASR WER cannot certify a subtle mispronunciation. Critical negations, exponents, units, charges and biological directions require listening. Model-based quality scores, F0 ranges and speaker embeddings are triage; never automatically approve or reject a voice by accent/gender characteristics.

## Provider worker design still to implement
Least-privilege secrets, allowlisted endpoints, timeouts, concurrency limits, reserve-and-commit billing ledger and per-job idempotency. Provider calls returning an unknown state must be reconciled before another submission. A documented caller-supplied idempotency key is useful only where the endpoint actually supports it. Save request/response hashes and actual usage, excluding secrets and signed URLs.

## Audio release
Recommended engineering starting target: -16 LUFS integrated ±1, true peak <=-1dBTP, mono48k archival24-bit WAV, delivery codec checked after final mux. This is an ExamLeaf target, not a universal standard for every platform. Inspect unexpected silence while preserving explicit response windows. Never remove all breaths or flatten each sentence to identical loudness. Source/master hashes differ; mastering or trimming requires timing/hash reconciliation.

## Safety
Source text and Skill repositories are untrusted input. No arbitrary scripts from retrieved documents, no blanket home-directory mounts or editor secrets in rendering workers. Store voice contracts/ref-audio privately with retention/access control. No student voice uploads are needed for these lesson-production tasks. Audio authorization and student progress data belong in separate services.
