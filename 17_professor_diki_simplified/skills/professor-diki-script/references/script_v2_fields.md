# script.json v2 fields (Professor Diki Simplified, `format/concept_short_60`)

v1.0.0, 16 Oct 2026. These are the fields the skill writes. The pilot schema (PILOT_CONTRACT §3) stays the same unless a row below changes it. **C** = `16_pilot_builds_2026-10-16/tooling/check_script.py` (v2 branch, `pilotlib.py`); **P** = `scripts/check_pd_script.py` (this skill). Both exemplars pass C and P as of 16 Oct 2026, 19:15 (planned 60.6 s and 60.1 s). C reports two warnings: the scene file is not built yet, and the PD-14 claim-scope count. The format builder's own reference is `17_professor_diki_simplified/format/script_v2_fields.md`. If the two disagree, the code in `pilotlib.py` wins, and this file gets updated.

## Top level

| Field | Type / values | Rule | Read by |
|---|---|---|---|
| `script_version` | `2` | Selects the v2 checks. Absent means v1. | C, P |
| `format` | `"concept_short_60"` | — | C |
| `target_duration_s`, `duration_tolerance_s` | `60`, `1` | Planned duration (pilotlib.plan) is 60 ± 1 s (PD-07). | C |
| `tail_s` | `0.8` | The end-motif tail after the last word. It is not counted as silence. | C |
| `cta_line` | string, or `""` for none (AC0) | Supplied per request by the business layer (PD-14). Default: `"Try the free lesson on <topic>."`. It is spoken as the last `close.next_step` beat, directly before the outro. | C, P |
| `style` | `"professor-diki"` | One style for every subject (PD-08). | — |
| `scenes` | exactly one | One persistent scene. It holds every beat, and the end card is its final state (PD-03). | C |
| `board_at_start` | element ids | What is visible at frame 0. The hook's complete picture lives here (SQ-41). | P |
| `artefacts` | object | `scroll_test` (one sentence), `surprise`, `outcome`, `prerequisite_bridge`, `fact_sheet[] {fact, node}`, `causal_chain[4]`, `hooks[5] {kind, text, scroll 1-5, honest, chosen?, why_rejected?}`, `hook_choice_rule`. These are writer's evidence and are never spoken. | P (scroll_test, hooks) |
| `terms` | `[{term, shown_by, meaning_beat}]` | Every technical term is visible (`shown_by` is cued at or before its first spoken use, or sits in `board_at_start`). Its plain meaning is spoken no later than the next beat (SQ-26). | P |
| `requires` | object | Fixture fields, lesson-graph nodes and sources that the script needs and that do not exist yet. Physics: `results.i_if_multiplied`, and the reviewed flag `results.lamp.current_doubles: false` (never a lamp current value). Chemistry: the Mg fixture and `SRC-h2o2-name` for the peroxide line. Each item goes to academic review, and the build fails until it exists. | builder |

## Per beat (fields added to the pilot beat)

| Field | Type / values | Rule | Read by |
|---|---|---|---|
| `slot` | `hook.question_reveal`, `explain.intuition`, `explain.givens`, `explain.prerequisite`, `check.predict`, `reveal.answer`, `explain.mechanism`, `worked.step`, `worked.faded`, `explain.formal`, `exam.language`, `misconception.confront`, `check.transfer`, `feedback.transfer`, `close.next_step`, `outro.brand` | Slots may repeat. The first occurrences of hook → predict → reveal.answer → transfer → feedback.transfer → close → outro must keep that order. The confront is expected; C warns if it is missing. | C, P |
| `pauses` | `[{"purpose", "after_s"}]`, one entry | This is the gap after the beat's last word, and it replaces `think_window_s` (retired). Purposes and PD-01 seconds: `join` 0.2–0.35, `land` 0.5–0.7, `inspect` 0.8–1.2, `think_recall` 1.5, `think_choice` 2.0, `think_calc` 3.0, `pause_video` 1.0 hold, each ±10 %. The last beat has `[]`. The alias `think_choose` → `think_choice` is accepted. | C |
| `energy` | `low` / `mid` / `high` / `peak` (C also accepts 1–5; low=2, mid=3, high=4, peak=5) | The hook is ≥ high. The `reveal.answer` carries the peak. `feedback.transfer` is a second peak. Nothing after the transfer is low. At least 3 distinct marks (SQ-28). | C, P |
| `visual_op` | one verb: `PreserveObject`, `ChangeValue`, `CompareStates`, `MapSymbol`, `TracePath`, `RevealMismatch`, `EquationTransform`, `PauseForPrediction`, `Badge`, `StrikeThrough` | The main operation on the persistent board during this beat. C also accepts the design system's extra verbs (`Reveal`, `Emphasize`, `SwapPart`, `EndMotif`, `Headline`). Scripts written with this skill use the ten listed here. | C |
| `insight_beat` | `true` on exactly one beat | The first usable idea: the givens-and-first-result beat ("Two volts, ten ohms: point two amperes."). Planned start ≤ 10 s (A3-M2). | C |
| `payoff_beat` | `true` on the `reveal.answer` beat | The answer to the prediction, at peak energy, carrying the claim line. It is a different beat from `insight_beat`. | P |
| `rehook` | `{"kind": question / task / turn / exception / reversal / next_loop}`, optional | The retention plan. A re-hook event is a `rehook` tag, an anchor slot (hook, predict, reveal.answer, confront, transfer, feedback.transfer, close) or a spoken `?`. From the hook to the transfer's answer, events are ≤ 12 s apart (SQ-35). | P (fail), C (warn) |
| `check` | on `check.predict` and `check.transfer`: `{task_kind: recall/binary/count/choose/calc/multi, asks: fx_ref, answerable_from: [fx_refs], changed_parameter?, likely_wrong?}` | `task_kind` fixes the pause purpose. Every `answerable_from` ref is in this beat's or an earlier beat's `fx_refs`. `asks` is not shown before the window, and it is shown in the next beat (SQ-25, SQ-04). | P (C has a number-token heuristic) |
| `evidence`, `evidence_shown_as` | on `misconception.confront`: a string (a fixture ref such as `results.i2`, or a node id), plus a prose description | A counter-value from the fixture or a sourced observation, visible on the board (SQ-23). It must be a string: C puts it in a set. | C, P |
| `humour` | optional `{pattern, concept_survives}` | Names the §4 pattern used and the science that the line keeps true. | judge |
| `on_screen.claim_line` | string, on one beat | The quotable line. It is ≤ 9 words, spoken verbatim in that beat, and stays on screen ≥ 1.5 s (SQ-42). | C (warn), P (fail) |
| `on_screen.disclosure`, `.brand`, `.free_lesson` | on `outro.brand` | `"AI-generated narration"` (Path B), or the Path A string from `brand/strings.json`. Brand is exactly "Professor Diki Simplified". | C |
| `emphasis_words` | strings | Each occurs verbatim in `text` (SQ-17). Emphasise only a changed quantity, a negation or a condition, at most one per sentence, and never the last word of a falling sentence. | P (judge for placement) |
| `mode`, `tag` | as v1 | Tags: `[curious]`, `[calm]`, `[warm]`, `[thoughtful]`. Candidates (`[excited]`, `[confident]`, `[surprised]`) only warn until the voice audition admits them. | C |

**Close (PD-14).** The last two spoken sentences are `cta_line` (the final `close.next_step` beat) and then `Professor Diki Simplified.` (the `outro.brand` beat).

- An optional tease beat may come before them. It is a `close.next_step` of ≤ 12 words containing "next", and it may carry one light follow line ("Next one: why hot bulbs break this. Follow for it.").
- The end card shows the literal text `Free lesson: <topic>` (`on_screen.free_lesson`, a fixture display string per PD-13), the brand and the disclosure.
- No spoken disclosure, and no "ExamLeaf" anywhere.

**Scope (PD-14).** One claim plus its condition. C warns when more than two CLM nodes are cited outside the confront evidence.

## What the checkers still have to learn

1. **C**: fail, not warn, on a missing `claim_line` and on a re-hook gap > 12 s once the format lead confirms. Today P fails on both.
2. **C**: measure the hook's question end inside the beat (P does this). C warns only on the whole hook row (`end > 3.5 s`).
3. **C**: read `check.answerable_from` and `check.asks`. The number heuristic cannot see an intuition predict ("more, less, or the same?") or a distractor value.
4. **C / qa.py**: after TTS, re-measure on `narration/timeline.json` the hook question end, the re-hook gaps, the transfer-answer position (70–90 %) and `claim_line` on-screen time. Both checkers plan from wpm estimates only.
5. **brand/strings.json**: `cta_options` still say "linked below" (pre-PD-14), and `cta_rule` forbids engagement prompts. Following PD-14 and the founder steer, the only spoken CTA is `cta_line`, and one light follow tease is allowed before it. The brand owner must amend both.
6. **C scope warning**: it counts prerequisite and context claims (chemistry: CLM-subscript-meaning, CLM-rocket-hydrogen) as extra ideas. A `role: prerequisite|context` mark on the node would let it count only the taught claim and its condition.
