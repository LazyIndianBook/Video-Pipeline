# Four pilot blueprints and actual benchmark
## Actual technical run
Eight silent 30-second media outputs, two workers. Local wall time per job is not isolated single-worker performance. Source fixtures are original examples based on the cited OpenStax sections, not a completed conversion of ExamLeaf PDFs. Video quality has been inspected through sampled frames; not teacher-approved or student-tested.

| Fixture | Aspect | Media seconds | Local job seconds | Frames | Result |
|---|---|---:|---:|---:|---|
| biology_genetics | 16:9 | 30 | 27.425 | 720 | Passed; release blocked |
| biology_genetics | 9:16 | 30 | 27.951 | 720 | Passed; release blocked |
| chemistry_balance | 16:9 | 30 | 28.670 | 720 | Passed; release blocked |
| chemistry_balance | 9:16 | 30 | 29.375 | 720 | Passed; release blocked |
| mathematics_chain | 16:9 | 30 | 27.372 | 720 | Passed; release blocked |
| mathematics_chain | 9:16 | 30 | 27.576 | 720 | Passed; release blocked |
| physics_rc | 16:9 | 30 | 27.338 | 720 | Passed; release blocked |
| physics_rc | 9:16 | 30 | 28.102 | 720 | Passed; release blocked |

## Full narrated pilot objectives
| Subject | Proposed full pilot | Tests and traps | Independent outcome |
|---|---|---|---|
| Physics | RC charging as a technical benchmark; confirm Assam syllabus relevance before publishing | Initial condition, dimensions, one tau, KVL, numerical/analytic agreement; graph/counter match; no instant charge | Interpret a changed R/C case and identify the model conditions |
| Chemistry | Balancing equations as Class 10 foundation / Class 12 repair | Fixed formulas, atom ledger, simplest ratios, no claim balance proves feasibility or mechanism | Balance a fresh simple equation and explain coefficient versus subscript |
| Mathematics | Chain rule with nested functions | Assumptions/domains, symbolic and finite-difference check, visible inner derivative | Differentiate a new expression and justify the factors |
| Biology | Monohybrid inheritance under explicit assumptions | Genotype vs phenotype, complete dominance, probability vs guaranteed counts | Explain a new cross and distinguish expected ratio from a small family outcome |

Each *_600s_plan.json is only a beat plan. Complete scripts, teacher-approved answers, narration and event alignment still need producing. Do not stretch a 30-second fixture to ten minutes and call it a pilot.

## Compare the shortlisted browser compositor
Render identical approved scenes in HyperFrames and Remotion: 16:9 + 9:16, same fonts/content/audio/frame count, same hardware and concurrency. Use a warm-up then at least five measured repeats per configuration. Record first-build and cached build separately; measure peak RSS, CPU/GPU usage, wall time, file size, repairs and visual differences. Do not extrapolate the simple native SVG timings as browser-engine benchmarks.

## Acceptance gates
- Zero unresolved critical scientific errors; separate academic and full-video production approval.
- Four actual narrated lessons near the pedagogically appropriate duration; exact ten minutes is not mandatory.
- Correct pronunciation of a versioned STEM test corpus and native review per language.
- Diagram, equations, captions and text readable on representative small phones, with genuine learner-controlled practice pauses.
- Same data drives simultaneous representations; parameter changes invalidate dependent assets.
- Retry/cancel/resume, rate limits, cost caps, expiring assets and duplicate-job prevention tested against real staging APIs.
- At least one original fully solved and one independent transfer item per lesson. Measure delayed learning and confidence calibration separately from retention/watch time.
- Choose the compositor only after cost including human repair is compared. No overall quality score may hide a critical scientific error.

## Work/time planning, not measured
Budget 8–16 academic/editorial hours per initial full lesson plus shared component engineering, then measure reductions with reuse. The mature cost model assumes 85 hybrid human minutes per video; that is not a promise for first-time bespoke lessons. Four full pilots require a separate, explicit reviewer schedule and no publishing deadline should bypass it.
