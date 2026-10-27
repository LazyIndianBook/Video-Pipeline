# Format Spec: `format/concept_short_60` (F8s, derived; sibling of F8 concept_intro)

Registry index row (for `15_content_engine_v2/FORMAT_REGISTRY.md`, added at the end of the cycle per PD-07):

| # | format_id | Kind | Default voice | Aspect | Levels allowed | Families allowed | Overlays allowed |
|---|---|---|---|---|---|---|---|
| F8s | concept_short_60 | derived | B | 9:16 | l6_8, l9_10, l11_12 (others after a pilot) | stem_fixture first; all ten after the four-subject component proof | any except jnvst |

## F8s Concept Short 60 (`format/concept_short_60`, derived)

- **Purpose.** A 60 s Professor Diki Simplified entry point to one exact free lesson. It carries one complete, correct insight and one learner success (PD-06, PD-07). The design is in `04_SIXTY_SECOND_FORMAT.md`.
- **Learner outcome.** The learner predicts once with a tool given in the first 10 s, then answers a new case on the same board with the rule just taught. They hear that they got it right.
- **Length.** 60.0 ± 1.0 s. This is a hard gate (`target_duration_s` 60, `duration_tolerance_s` 1.0). The bounds are [Hypothesis, A3-derived]; pilots tune them through registry versions.
- **Beats** (script v2 slots; `explain.*` and paired beats may repeat; one sentence per beat):
  1. `hook.question_reveal` (≤ 3.0 s);
  2. `explain.givens` / `explain.intuition` / `explain.prerequisite`, with one `insight_beat` starting ≤ 10 s;
  3. `check.predict` (think window 1.5 / 2.0 / 3.0 s by task);
  4. `reveal.answer` (≤ 3 s after the window, with a confirmation);
  5. `explain.mechanism` (change one thing; `claim_line`);
  6. `explain.formal` / `exam.language`;
  7. `misconception.confront` (the bounded exception, with `evidence`);
  8. `check.transfer` (its own window);
  9. `feedback.transfer` ("If you got that, you can …");
  10. `close.next_step` (open next question, then the request's `cta_line`, default "Try the free lesson on <topic>.");
  11. `outro.brand`, spoken exactly "Professor Diki Simplified." (PD-14 also accepts the CTA and the brand line as one two-sentence outro beat).
- **Format fields (per request).** `cta_line`: the spoken pointer, supplied by the business layer so the pipeline stays commercially agnostic (PD-14, RD-49); empty or null means no CTA (AC0). The end card text "Free lesson: <topic>" is a literal fixture display string (PD-13).
- **Graph inputs.**
  - Scope is one claim plus its condition (PD-14): one key CLM and its condition CLM.
  - One WRK with its fixture.
  - Two ASM nodes: the prediction and the transfer, each with an answer and a likely-wrong feedback.
  - The MIS and the confronting CLM for the exception.
  - At most one SIM (with `what_is_lost`) and one ANL (with `non_mapping`) permitted at the level.
- **Families and overlays.** stem_fixture first (physics, chemistry, biology quantitative claims). Other families follow after the four-subject component proof (roadmap). Overlays: any except jnvst.
- **Derivation rules.**
  - Recompose, never crop.
  - Every spoken or shown number comes from the fixture.
  - The prediction is answerable: every given is spoken and shown before the question (check_script heuristic plus `check.answerable_from`).
  - The answer is hidden until its window ends.
  - The transfer changes one parameter on the same board.
  - No claim beyond the root claim, its condition and the exception.
- **Narration.**
  - Path B. Eleven v4, with tags per `NARRATION_DIRECTION_SHEET.md`.
  - Speaking rate 150–160 wpm; formula and exception 125–140.
  - Pauses by purpose (PD-01), rendered as room tone.
  - No disclosure on screen or spoken (PD-20); the declaration is made at upload.
  - Lead-in 0.6 s; tail 0.8 s carrying the end motif.
- **Visual.**
  - One persistent scene (PD-03). The complete board is visible at frame 0.
  - Layout: opening ident (≤ 2.5 s), board, result sheet, card lane or caption lane; no persistent header (PD-21).
  - At least 1 meaningful change every 3 s during the explanation; no static frame over 2 s during speech.
  - Motion verbs from `design_system/tokens.json`.
  - The end card is the final state of the same scene, on screen ≥ 1.5 s, carrying:
    - "Professor Diki Simplified";
    - "AI-generated narration" (Path B), or "Performed by <name> · voice converted with AI" (Path A, PD-12);
    - "Free lesson: <topic>".
- **Interaction.**
  - Two windows: the prediction and the transfer.
  - Each window has a purpose-labelled plate (`pauses[].prompt`), no countdown, and the answer hidden.
  - A multi-step task is out of format. It becomes `pause_video` (a 1.0 s hold) or the free lesson.
- **Retention and share** (founder steer, 16 Oct 2026):
  - a re-hook (question, reveal, turn, transfer) every ≤ 12 s;
  - one `claim_line` (the quotable aha) on screen for ≥ 1.5 s;
  - the close is a truthful "next one" tease or open question, then `cta_line`, then the identity line;
  - no engagement or purchase prompts, no claims.
  - Platform metrics (3 s hold, 50 % and 100 % watch-through, shares, saves and follows per 1,000 views) are [Hypothesis] targets measured against our own baseline (`04_SIXTY_SECOND_FORMAT.md` §8).
- **QA extra.**
  - check_script v2: words 120–135 × `voice.rate_scale` (PD-22); planned duration; silence ≤ 15 %; insight ≤ 10 s; pause ranges; answerable prediction; transfer present; outro text; on-screen disclosure; no "ExamLeaf"; energy curve; re-hook gaps; claim line.
  - check_pd_script (framework §8).
  - QA, measured: A11 duration, A13 pause compliance, A14 first insight and board by 1.5 s, A15 change density, A17 persistence, A20 silence share, A21 energy curve.
  - brand_check.
  - GS full watch.
- **Level variants.**
  - l6_8: think windows at the upper bound; transfer only as think_recall or think_choice.
  - l9_10 and l11_12: as specified.
  - AC0 contexts: no CTA line; the close is the open question and the outro only.
- **Example.** Physics C01 (`format/sample_v2_script.json`). "Double the voltage: double the current?" → 2 V reads 0.2 A, current = volts ÷ ohms → predict at 4 V → "Zero point four, exactly double" → same resistor, twice the push → V = I × R → but a bulb heats up → "Your turn: six volts" → "Zero point six: if you got that, you can use this rule" → "Why does a bulb's graph curve?" → "Try the free lesson on Ohm's law." → "Professor Diki Simplified." 59.97 s planned, 122 words, 13.8 % silence.
