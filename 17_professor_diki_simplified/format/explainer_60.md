# Format Spec: `format/explainer_60` (F8e, derived; the feed short, PD-24)

**Learner outcome.** In 60 seconds a Class 10 learner can state the law in plain words, say what each symbol in its formula means, name the condition under which it holds, and has seen one example computed on the board.

**Spine (slots in this order; first occurrences must keep the order).**

| # | Slot | Time (planned, s) | Job | Visual |
|---|---|---|---|---|
| 1 | `hook.question_reveal` | 0–3 | "What is <law>?" plus a one-line promise (what it decides) | complete board from frame 0; opening ident 0–2.5 s |
| 2 | `explain.definition` | 3–12 | the definition in plain words, tied to the proper definition; `insight_beat` | definition card appears with its first word; the quantities pointed at on the board |
| 3 | `explain.mechanism` | 12–24 | the board proves it: one quantity changes, the readout answers; `payoff_beat` | ChangeValue, CompareStates, table rows landing, flow animation scaled to the quantity |
| 4 | `explain.formal` | 24–33 | the formula and what each symbol means, back to the definition | EquationTransform, MapSymbol from symbols to parts |
| 5 | `explain.condition` | 33–43 | "When does it hold?": the condition, and what happens when it breaks (the turn) | SwapPart, heat, StrikeThrough of the condition chip, back |
| 6 | `worked.step` | 43–51 | one example shown, not asked | ChangeValue to the new case, the table's last row, the result sheet with a tick |
| 7 | `recap.statement` | 51–56 | the rule in one line (`claim_line`) and the three points | points card (stays on the end card) |
| 8 | `close.next_step` | 56–58.5 | `cta_line` | — |
| 9 | `outro.brand` | 58.5–60 | "Professor Diki Simplified." | end card, motif in the tail |

**Rules.** 60.0 ± 1 s; words 120–135 at the table rate times `voice.rate_scale` (PD-22); pauses: join, land, at most one inspect; no `think_*` or `pause_video` purposes; dead time (pauses ≥ 0.45 s) ≤ 10 %; a visual change at least every 3 s during speech; first usable idea ≤ 10 s; energy peak on the mechanism result or the worked example; one `claim_line`; a re-hook (new question or turn) at least every 12 s; one persistent scene; every number from the fixture; PD-04/PD-20/PD-21 brand rules; PD-14 close. `check_script.py` and `qa.py` enforce these when `format` is `explainer_60`.

**What is deliberately absent.** Prediction windows, transfer questions and spoken prompts to pause: they belong to the free lesson and to the later quiz short format (`concept_short_60`).
