# Judge rubric for the pilot builds (16 Oct 2026)

Each judge receives, for ONE subject, two anonymised builds (A and B; the tier is hidden) with: `script.json`, `lesson_graph.json`, `fixtures/fixture.json`, `storyboard.md`, `build_notes.md`, the render contact sheet and three full frames per scene, the QA report, the narration timeline (word timings) and, where it exists, the MP4 path. Judges score 1–5 on each dimension, cite evidence (file, frame time, beat id), then rank A vs B and say what the weaker build would have needed from the guides to match the stronger one.

| # | Dimension | 5 looks like | 1 looks like |
|---|---|---|---|
| D1 | Science traceability | Every spoken number and every on-screen glyph traces to a fixture value or a graph claim with a named NCERT section; no claim without a node | Numbers typed by hand, claims the graph lacks, a wrong or over-stated fact |
| D2 | Pedagogy (02 rules, Super Teacher) | Real hook question, a genuine prediction pause before the reveal, the misconception named and confronted with evidence, one-idea recap, no hype | Reveals the answer before the pause, lectures without a question, countdown or exam-pressure language |
| D3 | Script craft (SCRIPTING_REGISTRY §15) | Short sentences, concrete nouns, the condition stated, emphasis placed where the fixture value changes, 130–155 wpm, register fits l9_10 | Abstract phrasing, run-on sentences, jargon unexplained, pace off |
| D4 | Visual craft (style guide, tokens) | The named style is recognisable; layout uses all three zones; sizes at or above token minimums; nothing clipped or overlapping; motion has purpose and holds ≥ 1.2 s; the middle visual actually explains | Generic look, content crammed in the top third, static frames, illegible labels, decorative motion that encodes nothing |
| D5 | Sync and timing | Reveals land on their words; emphasis on the key word; the think window reads as a calm pause; the scene never runs ahead of or behind the voice | Elements appear seconds off, everything shown at once, empty seconds |
| D6 | Technical conformance | QA report A1–A9 pass; deterministic; sources injected; no error-channel entries | Lint or cue-sheet failures, fallbacks, errors |
| D7 | Learner outcome (holistic) | A Class 10 student would understand the one idea, remember the condition or rule, and keep watching | Confusing, dull, or wrong |

**Verdict fields:** scores per dimension for A and B; three strongest evidence lines each; `winner` (A, B or tie) with a one-sentence reason; `gap_for_weaker`: the specific rule, template or example that the guides should add so the weaker build reaches the stronger one (file and section to change); `blocking_defects`: anything that must be fixed before a human would approve either build.
