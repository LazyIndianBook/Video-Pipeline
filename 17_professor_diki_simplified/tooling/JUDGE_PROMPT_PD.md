# Blind judge brief (Professor Diki Simplified, physics A vs B)

You are one of three independent judges. You receive two anonymised builds, A and B, of the same 60-second physics short (Ohm's law, Class 10) in `judging/physics_pd/A/` and `judging/physics_pd/B/`. Each folder holds the script, the lesson graph, the fixture, the storyboard, a contact sheet, full frames, the narration word timings, a sanitised QA summary and the path of the MP4. You do not know which build is older or how either was made, and you must not guess from style; judge what a Class 10 learner on a phone would experience.

Rubric: `17_professor_diki_simplified/tooling/JUDGE_RUBRIC_PD.md` (D1–D8, the hard gates, the verdict JSON fields). Score every dimension 1–5 for both builds with evidence (file, time, beat id); count empty seconds, the time to the first usable idea and the number of turns; quote the shareable line if there is one; list any failed gate; pick the winner and say what the weaker build needed. Base every claim on the files; if something cannot be verified from them, say so instead of guessing.

Lenses (one per judge): `teaching` (D1, D2, D7 first), `craft` (D3, D4, D5, D6 first), `pull` (D8 first: momentum, motivation, whether you would share or follow). Score all eight regardless of lens.

Output: write `judging/physics_pd/verdict_<lens>.json` with the fields in the rubric (`lens`, `scores{A,B}{D1…D8}`, `evidence{A,B}[3]`, `empty_seconds{A,B}`, `time_to_first_insight_s{A,B}`, `turns_count{A,B}`, `shareable_line{A,B}`, `gates{A,B}`, `winner`, `reason`, `gap_for_weaker[]`, `blocking_defects{A,B}`, `notes`). Reply with a 120-word summary.
