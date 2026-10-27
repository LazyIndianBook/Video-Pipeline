# Production runbook
## Exact workflow
1. Confirm permitted source and official board/year scope. Store source hash and original file separately from generated content. Extract native text. Explicitly review figures, equations and empty/scanned pages; OCR is never implicit.
2. Produce source-linked claim list, prerequisite map and independently solved exercises. Block unsupported claims before video work.
3. Draft the Super Teacher explanation. Separate spoken language from formulas. Require a worked, faded and independent task; humour and stories are optional and must preserve the model.
4. Academic reviewer approves script/answers/model assumptions. Unreviewed material remains preview-only.
5. Compile each scene into an approved component. Generate typed scientific state first; graph/diagram/counter all consume it. Version a newly authored component and add negative tests before reuse.
6. Confirm provider capability, price estimate and commercial voice/asset rights. Reserve a bounded amount in the ledger. Only then generate missing audio or optional illustrations. Store provider job ID immediately; an unknown job is not grounds to submit again.
7. Measure final audio; align the spoken script to the waveform. Validate word/character timestamps, then place semantic visual events. Add true silence for thinking and stable pause cards. Do not speed difficult narration to fit an arbitrary ten-second slot.
8. Render only changed scenes to temporary files; probe codec, dimensions, duration, frames and audio. Hash and atomically move successful outputs to the review area. Preserve other successful scenes.
9. Check captions for text fidelity, timing, equation-pronunciation semantics, answer leakage and safe-area conflicts. Inspect graph/model synchronization, labels, units, count states and accessibility. Sampled VLM/frame checks assist but do not certify correctness.
10. Require academic approval and complete final-video production review on the exact artifact hash. Require all rights/access metadata and destination links. Any material change invalidates the relevant approval.
11. Export the long lesson. Create 20–60s Shorts as independently understandable explanations using ShortSpec. Retain conditions and correct graph axes. Recompose vertical layouts. Repeat QA and approval.
12. Publish only released hashes. Use first-three-free entitlement metadata outside the video; actual playback access belongs to the web/book platform. Publishing and student-data handling are not implemented in this proof.

## Caching
Hash source claims, model assumptions, scientific data, component version, language, text, voice/model/settings, design tokens, renderer version and output format. Cache generated assets by exact inputs; a seed alone is not a determinism guarantee. Do not cache disputed scientific approval as permanent truth. Record reasons for invalidation.

## Failure/retry policy
Validation failure: stop before render or spend. Renderer failure: preserve logs/temp diagnostics, retry once after a targeted repair, then escalate. Provider transient error: exponential backoff, respect Retry-After and recorded job state. Unknown paid-job status: poll/reconcile that job, never duplicate. Auth/rights/language/capability failure: hard stop; do not silently switch vendor. Budget exhaustion: pause batch. External requests must have timeouts and request IDs. Provider assets with expiring URLs must be copied to controlled storage and hashed; never publish bearer URLs in logs.

## QA severity
Critical: wrong science/answer/condition, misleading visual, unlicensed asset, missing critical text/audio, unauthorized data/spend. Block release.
Major: poor pronunciation, unreadable essential label, distracting pacing, caption error changing meaning, answer revealed too early. Repair and re-review.
Minor: cosmetic timing/alignment issue without learning impact. Track; do not allow accumulation to undermine the brand.

## Cost and observability
Track estimated vs actual provider spend, input/output tokens, accepted generated seconds, attempts per accepted asset, cache hits, render worker-seconds, failure class, reviewer/editor minutes and revision count. Machine cost is not total cost. Log minimal metadata, not secrets or student identifiers. Alert on p95 duration, repeated provider failure, spending anomalies and rising human repair minutes.

## Security/rights
Source documents and public Skills are untrusted. No arbitrary eval, remote font fetch or shell instruction from document content. Separate author, renderer, provider and release identities. Read the security admission document. Commercial-use rights of model weights, TTS voices and imported assets are distinct from the surrounding code licence. No claim of zero piracy or automatic monetization.

## Current implementation boundary
The code tests native extraction, four narrow science models, local rendering/cache/budget contracts and media/approval policy checks. No distributed queue, authenticated approvals, external generation adapter, natural-language forced alignment or publisher has been implemented. The standalone Runway speech probe is evidence of a single connector operation, not proof of this end-to-end workflow.
