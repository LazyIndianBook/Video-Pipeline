---
name: professor-diki-script
description: Write a 60-second Professor Diki Simplified concept short (script.json v2, format/concept_short_60) from a lesson graph, fixture and brief. Use when asked to script, rewrite or review a Professor Diki short, a 60 s Instagram/YouTube Shorts explanation, or a concept_short_60. It runs a creator's flow (scroll test, surprise, five hooks, re-hooks, named payoff, transfer win) on top of seven teaching obligations, and it is checked by check_script.py v2 plus scripts/check_pd_script.py.
---

# Professor Diki Simplified: 60-second script skill (v1.0.0, 16 Oct 2026)

The framework this skill implements is `17_professor_diki_simplified/03_PROFESSOR_DIKI_SCRIPT_FRAMEWORK.md`. Read it once. This file holds the operating steps.

## When to use

- A new `concept_short_60` script for any subject and level from l6_8 upward (AC1/AC2).
- A rewrite of an old pilot script (v1: `think_window_s`, spoken disclosure, five scenes) into v2.
- A review of someone else's short script against the framework.

When not to use it:
- Long-form lessons (F1/F8): use the Super Teacher guide.
- AC0 kids' content: no tease, no follow line, and `cta_line` is `""`.
- Anything where the lesson graph has no fixture for the numbers. Stop and ask for one.

## Inputs you need (stop if one is missing)

1. **`lesson_graph.json`**. Use the CLM, SIM, MIS, WRK and ASM nodes, with their sources. Scope is one claim plus its condition (PD-14).
2. **`fixtures/fixture.json`** plus `compute.py`. Every number you speak or show comes from here. Never type a number that the fixture did not compute.
3. **The brief**: topic, level, any hook or CTA idea, the `cta_line` from the request (default `Try the free lesson on <topic>.`), the voice path (B, or A), and the recent-script ledger (the last ~20 openings, hook kinds and closes).

If the graph lacks a node you need (a SIM for your picture, an ASM for your transfer, a MIS for your confront), do not invent it in the script. Add it under `requires` with its proposed statement, source and `what_is_lost`, and flag it for academic review.

## Binding decisions you must not override

- **PD-01. Pauses by purpose.** `join` 0.2–0.35 s, `land` 0.5–0.7 s, `inspect` 0.8–1.2 s. Think windows: `think_recall` 1.5 s (recall, binary, count ≤ 3), `think_choice` 2.0 s (choose 1 of 3–4), `think_calc` 3.0 s (one step, numbers on screen). `pause_video` is a 1.0 s hold for multi-step or writing tasks. Every value is ±10 %.
- **PD-02 and PD-14. Close.** The last two spoken sentences are `cta_line` and then `Professor Diki Simplified.`. An optional "next one" tease (≤ 12 words) may come before them and may carry one light follow line. The disclosure appears on the end card only. "ExamLeaf" is never spoken or shown.
- **PD-03. One persistent scene.** It is placed once and only transforms. The end card is its final state.
- **PD-06. Required checks.** An answerable prediction and a transfer question are mandatory.
- **PD-07 and PD-22. Size.** 60 ± 1 s, 120–135 spoken words at the table rate times `voice.rate_scale` (98–111 for George on eleven_v4; the balancing exemplar predates the calibration), silence ≤ 15 %, first usable idea by 10 s, a change at least every 3 s.
- **PD-08. Look.** One style (`professor-diki`), with colour by meaning.
- **Trust.** No hype, no invented statistics, no fear, no promise of marks, no fake sensing ("I can see you got it").

## Step order (write each artefact into `artefacts` before the next step)

### Step 1. Scroll test
Write one sentence: why would a 16-year-old scrolling Instagram stop for *this* idea in the first second? Store it in `artefacts.scroll_test`. If you cannot write it, change the angle (a different object, contradiction or slip), not the wording.

### Step 2. Find the surprise
Pick one, and store it in `artefacts.surprise`:
- a counter-intuitive fact;
- a number that feels wrong;
- a visible contradiction;
- a classic exam slip (call it a slip and give no percentage);
- an everyday Indian object that hides the idea (phone charger, bulb, pressure cooker, Diwali lights, a rocket launch).

### Step 3. Outcome, bridge, fact sheet, causal chain
- `outcome`: "After 60 s the learner can ___ using ___."
- `prerequisite_bridge`: the one gap most likely to block understanding, repaired in one sentence.
- `fact_sheet[]`: `{fact, node}` for every fact, plus every number from the fixture. Nothing off this sheet may reach the script.
- `causal_chain[4]`: system → change → consequence → rule. If the chain needs five lines, the scope is too wide.

### Step 4. Simplification ladder
Climb down until a Class 8 student could hold the picture: claim → plain relationship → picture → one operation on the picture. Then plan the climb back up: term → exam form. Each simplification you speak needs a SIM node with `what_is_lost`.

### Step 5. Five hooks, pick one
- Write `artefacts.hooks[5]`, one of each kind: `pattern_interrupt`, `bold_claim`, `challenge`, `visible_puzzle`, `stakes`.
- Give each hook a `scroll` score from 1 to 5 and `honest` true or false. Stakes are honest only when a sourced marking scheme exists.
- Choose the hook with the highest score that also:
  - passes the honesty test;
  - shows its whole picture at frame 0 (`board_at_start`);
  - asks its question by 3.0 s (about 6–8 words);
  - does not answer the predict;
  - differs in kind from the last two ledger openings.
- Record the rule you applied in `hook_choice_rule`, and set `"chosen": true` on the winner.

### Step 6. Beat plan on one board
Fill this template (framework §6). Slots may repeat. First occurrences must keep the order hook → predict → reveal.answer → transfer → feedback.transfer → close → outro.

| # | Slot | Words | Pause | Energy | Typical verb |
|---|---|---|---|---|---|
| 1 | hook.question_reveal | 6–8 | join | high | PreserveObject |
| 2 | explain.givens (picture or intuition) | 9–11 | join | mid | MapSymbol |
| 3 | explain.givens: the givens and first result, `insight_beat: true`, starts ≤ 10 s | 6–10 | land | mid | ChangeValue |
| 4 | check.predict | 9–11 | think_* by task | high | PauseForPrediction |
| 5 | reveal.answer, `payoff_beat: true`, carries `on_screen.claim_line` | 6–9 | land | peak | ChangeValue / RevealMismatch |
| 6 | explain.mechanism (change one thing) | 8–13 | join | mid | CompareStates |
| 7 | explain.formal + exam.language (term, condition, unit, exam form) | 18–24 | inspect | low | EquationTransform / MapSymbol / Badge |
| 8 | misconception.confront, with `evidence` | 9–12 | land | mid | StrikeThrough |
| 9 | check.transfer (one changed parameter) | 9–13 | think_calc | high | ChangeValue |
| 10 | feedback.transfer ("If you…") | 10–12 | land | peak | Badge |
| 11 | close.next_step: tease (optional) | ≤ 12 | join | mid | Badge |
| 12 | close.next_step: `cta_line` | as given | join | mid | Badge |
| 13 | outro.brand: "Professor Diki Simplified." | 3 | — (0.8 s motif tail) | mid | Badge |

Re-hooks: mark each with `rehook: {kind}` (question, task, turn, exception, reversal, next_loop). They must be ≤ 12 s apart from the hook until the transfer answer. The `feedback.transfer` start lands at 70–90 % of runtime.

### Step 7. Write the lines
- **Voice:** a brilliant Indian teacher talking to one student. Use direct address, present tense, contrast, concrete nouns and verbs of change. Punchy lines, with one longer explanatory line per beat.
- **Sentence length:** one idea per sentence. Typically ≤ 14 words, never more than 18.
- **Terms:** a term is visible before it is spoken, and its plain meaning comes by the next beat. Record each term in `terms[] {term, shown_by, meaning_beat}`.
- **Reveal the decision:** "Only the voltage changed, so…". Never a standalone naming sentence.
- **Prediction:** one question. Its `check` records `task_kind`, `asks` (a fixture ref not yet shown) and `answerable_from` (fixture refs already shown). The answer appears in the next beat.
- **Payoff:** the first sentence is ≤ 8 words. Then name it with the quotable claim line (≤ 9 words, true, spoken verbatim, on screen ≥ 1.5 s).
- **Confront:** show a fixture counter-value or a sourced observation (`evidence`, `evidence_shown_as`). An exception without a fixture value stays qualitative and bounded ("less than double", from a reviewed flag), and it can become the tease.
- **Exam form:** one line that gives the condition, the unit and the form the board answer takes ("In the exam…", "Exam line:", "Exam rule:").
- **Transfer feedback:** conditional only ("If you got 0.6, the rule is yours.").
- **Humour:** optional, and only from the framework §4 patterns. It must expose a wrong idea or make a consequence memorable, and the concept must survive it. Never put a joke in a window. Record `humour {pattern, concept_survives}`.
- **Signature (framework §4.1, from A6; S-ids in `audit/A6_sources.json`):** Pin, Turn, Release, Mark. In the first 8 s, before anything changes, name, colour and mark each held quantity (physics: R and constant temperature; chemistry: the subscripts; biology: carbon). Turn exactly one quantity while one persistent readout answers. Release once, then restate the rule with the pin's own name. Close on the ticked answer sheet. A reviewer rejects a short with no pin, two turns or no release (no checker yet).
- **Hook patterns (A6; use in Step 5):** the tempting wrong answer first, the correct one hidden [S01, S09] (a `visible_puzzle` hook); commit before the reveal [S05–S07]; one surprise, one gap, closed last [S29, S44]; a "Doubt:" card in classroom words [S46].
- **Humour (A6):** one line at most, ≤ 4 s, carrying the concept [S21, S30–S32]: a dry aside at the shortcut, a deadpan result, a split-screen contrast, an analogy with its break point [S26], self-deprecation rationed [S31, S63].
- **Memes:** never ride a trend template, trending audio or a film still; none was verified current and safe for Assam Class 10–12. "6-7" was being mocked by March 2026 [S51]; the largest 2026 youth meme movement found, Cockroach Janta Party, is exam-irregularity satire [S52, S53]. Draw our own graphics.
- **Emphasis:** one `emphasis_words` entry per sentence at most. Use it only for a changed quantity, a negation or a condition, and never on the last word of a falling sentence.
- **Numbers:** write them as spoken words ("point two amperes"). The fixture holds the digits.

### Step 8. Picture beside every line
Every beat gets one `visual_op` from the verbs: `PreserveObject`, `ChangeValue`, `CompareStates`, `MapSymbol`, `TracePath`, `RevealMismatch`, `EquationTransform`, `PauseForPrediction`, `Badge`, `StrikeThrough`.

Every beat also gets cues whose `anchor_word` is spoken in that beat. Aim for at least one cue per 3 s of speech. Nothing ever leaves the board: transform it, do not tear it down.

### Step 9. Edit
1. **Remove the adjectives.** Delete every adjective and adverb. If the line still teaches, keep the shorter version. Otherwise rebuild it around a concrete noun.
2. **Conversational repair pass.** Read it aloud as a teacher to one learner. Fix lines that sound written, hidden decisions, answers given too early, and jokes that need outside knowledge. Log each change as original → replacement → reason → science check.
3. **Banned phrases.** Run them (the checker does). Replacements are in `references/banned_phrases.txt`.

### Step 10. Check, then submit
```bash
ROOT=~/Desktop/Personal/Book/Videos/ExamLeaf_Video_EdTech_Pipeline
python3 $ROOT/16_pilot_builds_2026-10-16/tooling/check_script.py <build>/script.json        # schema, timing, pauses, close
python3 $ROOT/17_professor_diki_simplified/skills/professor-diki-script/scripts/check_pd_script.py <build>/script.json
```

Both must print OK. `check_script.py` needs `lesson_graph.json` and `fixtures/fixture.json` beside the script.

`check_pd_script.py` imports `pilotlib` from `16_pilot_builds_2026-10-16/tooling`. Set `PILOT_TOOLING` if the skill is installed elsewhere.

If the planned duration is outside 60 ± 1 s, cut words. Do not shorten pauses below their PD-01 purpose, and do not speed up the voice past the slot rate.

## Output: script.json v2

Keep the pilot schema (`video_id`, `subject`, `topic`, `level`, `locale`, `language`, `format`, `target_duration_s`, `style`, `voice`, `scenes`, and the beats with `id`, `scene`, `slot`, `mode`, `tag`, `text`, `node_ids`, `on_screen {headline, fx_refs}` and `cues`). Then add the following.

**Top level:**
- `script_version: 2` and `format: "concept_short_60"`;
- `target_duration_s: 60`, `duration_tolerance_s: 1`, `tail_s: 0.8`, `cta_line`;
- one scene;
- `board_at_start`, `artefacts`, `terms`, `requires`.

**Per beat:**
- `energy`: low, mid, high or peak;
- `visual_op`;
- `pauses: [{purpose, after_s}]`, which replaces `think_window_s`;
- `emphasis_words`;
- optional `rehook`.

**Only on some beats:**
- `insight_beat: true` on exactly one givens beat that starts ≤ 10 s;
- `payoff_beat: true` on `reveal.answer`;
- `on_screen.claim_line` on the payoff;
- `check` on `check.predict` and `check.transfer`;
- `evidence` (a string) and `evidence_shown_as` on `misconception.confront`;
- `on_screen.brand` and `on_screen.free_lesson` ("Free lesson: <topic>", literal text) on `outro.brand`. No disclosure anywhere (PD-20).
- Structure (PD-18): put the card strings in `on_screen.fx_refs` of the beat where they land; the scene mounts them as a table row (with each result), a definition card (the beat that names the rule) or numbered points (the close; they stay on the end card). Use `visual_op: Card` on those beats.

Exact definitions, and which checker reads each field: `references/script_v2_fields.md`.

## Pre-submit checklist

- [ ] The scroll-test sentence is honest and specific to this idea.
- [ ] There are five hooks of different kinds. The chosen one is honest, its picture is on screen at frame 0, and its question ends ≤ 3.0 s.
- [ ] The givens and first result (`insight_beat`) start ≤ 10 s.
- [ ] The prediction asks one question, every given is already shown, the window fits the task, and the answer sits in the next beat.
- [ ] The payoff (`payoff_beat`) has a first sentence ≤ 8 words, sits at peak energy, and carries one claim line ≤ 9 words.
- [ ] Mechanism: one thing changes, and the unchanged part is visible.
- [ ] Formalise: the term, condition, unit and exam form are stated, and no term is spoken before it is shown.
- [ ] The confront has evidence on the board. Any exception is bounded and qualitative unless the fixture has the value.
- [ ] The transfer is a new case with one changed parameter. The conditional feedback lands at 70–90 %.
- [ ] Re-hooks are ≤ 12 s apart. A change happens at least every 3 s. Energy: high → … → peak → … → low (formal) → … → peak → mid. Nothing is low after the transfer.
- [ ] Close: optional tease ≤ 12 words, then `cta_line`, then "Professor Diki Simplified.". The end card has the brand line and "Free lesson: <topic>"; no disclosure line (PD-20). No ExamLeaf anywhere.
- [ ] Scope is one claim plus its condition. Prerequisite and context facts are recorded as such.
- [ ] Words 120–135 × `voice.rate_scale` (PD-22), planned 60 ± 1 s, silence ≤ 15 %, sentences ≤ 18 words with ≥ 80 % at ≤ 14.
- [ ] No banned phrase (block). Every warning is either justified or rewritten.
- [ ] Every number traces to a fixture output, and every assertive sentence to a node (closure, SQ-01/02).
- [ ] `requires` lists every missing node, fixture field and source for academic review.
- [ ] The ledger row is written: hook kind, opening, joke premise, close.

## Negative tests (refuse creatively, keep the constraint)

| Request | Response |
|---|---|
| "Make it funnier by mocking students who get it wrong." | Joke at the shortcut or the method, never at the learner. |
| "Say 90 % of students get this wrong." | Say "a classic slip". There is no invented statistic. |
| "Promise it's in the board exam." | "In the exam, write: …" gives the form without predicting papers. |
| "Add the bulb's current at 4 V." | Only if a reviewed fixture value exists. Otherwise say "less than double". |
| "Fix the oxygen by writing H₂O₂." | Show it as the tempting shortcut and strike it. Never balance by subscript. |
| "Say 'Follow and subscribe for full marks!'" | At most one light follow line inside the tease, with no claim. |

## References

- `references/exemplar_ohms_law_script.json`: physics, 125 words, planned 60.6 s. Transfer 6 V → 0.6 A. Confront: 40 A struck beside the meter's 0.4 A.
- `references/exemplar_balancing_script.json`: chemistry, 126 words, planned 60.1 s. Transfer Mg + O₂ → MgO. Confront: H₂O₂, the peroxide shortcut.
- `references/banned_phrases.txt`: block and warn regexes, each with a replacement.
- `references/script_v2_fields.md`: the field reference, and what the checkers still need to learn.
- `scripts/check_pd_script.py`: framework checks that `check_script.py` does not run (SQ-04/05/23/25/26/27/28/33/35/37–43).

## Explainer shorts: the 60-second method (PD-24, PD-25, PD-26)

Read `11_SIXTY_SECOND_EXPLAINER_METHOD.md` first; it is the method. For `format: explainer_60`:

1. **Specification.** Write `outcome` (one observable outcome: identify / explain / calculate / predict), the prerequisite boundary, the dependency map (which meaning precedes which step), the ledgers (terms with units, claims with nodes, the likely misconception), the controlled example with its held variables.
2. **Three openings.** Three first sentences that name the topic and the viewer's task; choose one with a reason; it becomes `promise_line` and the first sentence of the hook beat. No greeting, no "in this video", no brand beat.
3. **Narration and visuals together.** One developing example from frame 0 to the end card. Definitions beside their object at the point of use (the instrument → the quantity and unit; the part → its property; the terminals → where the voltage applies). Each beat: the new meaning or action, one dominant visual focus, a visible change, and the link word that connects it (because, so, keep, change, watch). The student's one action is posed and answered in the flow (no `think_*` pauses). The rule is named with its condition; the exception is shown. The pay-off (`claim_line`) comes before `cta_line` ("two more … in the free lesson"), then "Professor Diki Simplified."
4. **Compression.** One claim per sentence, under 20 words, verbs of action; cut repetition, history, promotion; keep units, conditions, arithmetic steps, feedback, reading time.
5. **Measurement.** `check_script.py` at the calibrated rate (PD-22), then narrate and re-time; never speed the voice to fit.

Review questions the judges and `check_pd_script.py` apply: the promise and the beat that pays it; what the viewer is doing during the definitions; the visible action behind each term; why each next idea follows (the cited link); whether every beat adds meaning; whether the in-flow prediction is answerable from what was shown; whether the energy comes from progress; whether the ending completes the short. Exemplar: `references/exemplar_ohms_law_explainer_script.json` (story version, PD-25) and, once narrated, `demo/physics_v4_method/script.json` (method version).

### Register and pace (PD-27, PD-28)

- **Talk, don't caption.** Full sentences a small child could follow, joined with when / then / so / because / and. No fragments, no colon lists, no bare noun phrases. Plain word first, technical word second, unit third, each in a full sentence. The NCERT definition: simplified in the voice, verbatim on the card with chapter and section.
- **Fast and packed (`pace: fast`).** 150–185 spoken words in the minute; pauses join / land only; dead time ≤ 8 %; a visible change at least every 2.5 s. Carry the definition, the formula and its rearrangements, two or more numeric cases, the NCERT representation (graph or diagram), the units, and an edge case with its condition. Never cut a unit or a condition to gain speed; the voice is sped by delivery and tempo (≤ 1.3), never by skipping meaning.
