# Judge rubric for Professor Diki Simplified shorts (v1.0, 16 Oct 2026)

Extends `16_pilot_builds_2026-10-16/tooling/JUDGE_RUBRIC.md` (D1–D7 unchanged) with the dimension the founder asked for and the gates the scorecard enforces. Judges receive two anonymised builds (A and B) with script, graph, fixture, storyboard, contact sheet, 1-fps frames, word timings, the sanitised QA summary and the MP4 path. Scores 1–5 with evidence (file, time, beat id); rank A vs B; name what the weaker build needed.

| # | Dimension | 5 looks like | 1 looks like |
|---|---|---|---|
| D1 | Science traceability | every number and glyph from the fixture; every claim from a sourced node; condition stated with the rule | hand-typed numbers; claims without nodes; a wrong or over-stated fact |
| D2 | Pedagogy | intuition before the term; prediction answerable from shown givens; misconception confronted with evidence on the same board; transfer solved; one idea | prediction before its givens; assertion instead of evidence; no transfer; several ideas |
| D3 | Script craft and voice | short contrastive sentences, a teacher talking to one student, no stock AI phrases, terms shown before named, one quotable line | textbook register, jargon first, filler, repeated skeleton |
| D4 | Visual explanation | the collage house style (PD-19) with one persistent board, every change causal, science colour by meaning, legible on a phone, at least one structured element (table, definition card or points) tied to the picture (PD-18), nothing empty | tear-downs, empty time, small content, three looks, props that encode nothing, flat panels on a blank page |
| D5 | Sync and timing | reveals on their words; pauses by purpose; no dead time | early or late reveals; 5 s holds for simple prompts |
| D6 | Technical conformance | all machine checks pass; deterministic | failures or fallbacks |
| D7 | Learner outcome | "I get it and I can solve the next one" | confused, bored, or wrong |
| **D8** | **Momentum, motivation and pull** | first frame complete and the question by 3 s; first usable idea ≤ 10 s; a turn every 8–12 s; the payoff lands and is named; the learner succeeds at a transfer; the close makes you want the next one; you would share the aha line or follow | empty opening, long setup, flat energy, payoff late or missing, close that just stops, nothing to share |

**Hard gates (fail = not releasable regardless of score):** any science error; "ExamLeaf" or a forbidden string on screen or spoken; an AI-disclosure line on screen or spoken (PD-20); a persistent brand header in the lesson frames (PD-21); prediction not answerable from shown givens; no transfer question; silence > 15 % of runtime; the board torn down inside the lesson; duration outside 60 ± 1 s for `concept_short_60`.

**Verdict JSON fields:** `scores{A,B}{D1…D8}`, `evidence{A,B}[3]`, `empty_seconds{A,B}`, `time_to_first_insight_s{A,B}`, `turns_count{A,B}` (re-hooks or reversals counted), `shareable_line{A,B}` (quote or none), `gates{A,B}` (list of failed gates), `winner`, `reason`, `gap_for_weaker[]`, `blocking_defects{A,B}`, `notes`.
