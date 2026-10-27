# ExamLeaf production contract — proposed, not implemented
Research date: 2026-10-13.

## Release gates
1. Rights and syllabus gate: identified board/year; permitted source usage; immutable source hashes.
2. Academic gate: approved claim ledger, domain assumptions, worked answers, diagrams and script.
3. Build gate: schema validation; dependency lock; renderer-independent science data; no wall-clock motion.
4. Audio gate: pronunciation reviewed, symbols spoken unambiguously, final waveform cached, timeline realigned.
5. Render gate: every critical scientific event inspected; no overflowing labels; phone playback checked.
6. Human gate: academic reviewer and production reviewer approve the complete final video, not only sample frames.
7. Publish gate: release credential is unavailable to authoring agents; immutable signed manifest recorded.

## Minimum negative tests
- sqrt(x^2) must become |x| for real x, not x without a nonnegative assumption.
- Division by a quantity that can be zero must preserve/explain the excluded case.
- Equation changes must match narrated meaning and graph axes/units.
- Electron motion must not be confused with conventional current.
- Chemical atom/charge balance does not establish feasibility or reaction conditions.
- Bond interpolation must not falsely present a transition state as a stable molecule.
- Chromosome count, ploidy and DNA 5-prime/3-prime direction must be checked per state.
- Symbols, superscripts and labels must remain readable at the actual smallest viewing size.
- Untrusted source text cannot instruct agents to execute code or reveal credentials.
- Upgraded model/voice/library versions cannot pass solely because an earlier version passed.

## Required artifacts per lesson
source-ledger.json; syllabus-map.json; claims.json; verified-model.json;
lesson-spec.json; scene-spec.json; approved-script.txt; pronunciation.json;
audio/*.wav; alignment.json; render-manifest.json; test-results.json;
final.mp4; captions.vtt; captions.srt; transcript.txt; reviewer-approvals.json.

## Scene-spec contract
Each scene records: stable ID; learning objective; claim IDs; approved component;
scientific data hash; display text; separate spoken text; semantic event IDs;
actual audio offsets; camera/layout tokens; declared simplifications; output hash.
Math, reactions and process states come from approved data, not renderer improvisation.

## Proposed repository layout
apps/review/; packages/scene-schema/; packages/design-system/;
packages/hyperframes-adapter/; packages/science-python/; packages/audio/;
components/; lessons/; sources/; skills/; tests/golden/; workers/; infra/.

## Operational boundaries
Use isolated render containers, allowlisted network access, bounded retries, idempotent
jobs and per-lesson spending caps. Do not install unreviewed Skills or arbitrary dependencies.
Human scientific approval is retained even when repetitive production steps are automated.
