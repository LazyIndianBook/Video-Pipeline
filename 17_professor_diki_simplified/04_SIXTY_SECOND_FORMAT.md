# 04 · The 60-second Professor Diki Simplified short (`format/concept_short_60`)

Status (16 Oct 2026): designed and enforced by `16_pilot_builds_2026-10-16/tooling/` (`check_script.py` v2, `narrate.py`, `pilotlib.py`). Format Spec `format/concept_short_60.md`; fields `format/script_v2_fields.md`; passing sample `format/sample_v2_script.json`. Binding: PD-01, PD-02, PD-03, PD-06, PD-07, PD-14. Timings from A3; every platform number in §8 is a hypothesis.

**PD-24 (17 Oct 2026).** The feed short is now the explainer format `format/explainer_60.md` (no prediction window, no transfer question; definition-led spine; dead time ≤ 10 %). The question-based plan below is kept for the later quiz short format.

## 1. The job of the short

A short is the entry point to one exact free lesson. In 60 seconds it delivers **one complete, correct insight** (one claim plus its condition, PD-14) and **one learner success**: the viewer answers a new question with the rule they just saw, and the voice confirms it. The rest of the topic (the bulb's curved graph, three-element equations) is held back as the reason to open the free lesson.

It fails if it shows only the narrator being clever, teaches two ideas, or ends on a legal line.

The old Opus shorts failed in three measured ways (A3):
- The first usable idea arrived at 21–35 s.
- 26–29 % of the runtime was silence.
- None of them asked a transfer question.

## 2. Segments, timings and budgets (60.0 s)

Rates are active wpm, first word to last word of a beat. A beat is one sentence; each gap between beats is a labelled pause. Energy uses marks 1–5. Boundaries may shift ±1 s if §6 still holds.

| # | Segment | Time | Words | Rate (wpm) | Energy | Pause after (PD-01) | Visual job |
|---|---|---|---|---|---|---|---|
| 1 | **Hook**: the complete board is visible from frame 0; the question is spoken by 3.0 s | 0.0–3.0 (lead-in 0.3) | 5–8 | 160–165 | 4 | join 0.25 | PreserveObject, Emphasize the two quantities; opening ident on screen 0–2.5 s (PD-21) |
| 2 | **Givens and first result**: the numbers the prediction needs, then one usable tool (`insight_beat`) | 3.0–10.0 | 15–20 | 155–160 | 3 | join, then land 0.5–0.6 | ChangeValue, MapSymbol; table row 1 (the givens) lands with the first result (PD-18) |
| 3 | **Answerable prediction**: one question; every given already spoken and shown | 10.0–16.0 | 6–9 + window | 150 | 4 | think window 1.5 / 2.0 / 3.0 by task | ChangeValue, PauseForPrediction |
| 4 | **Reveal**: the answer within 0.1 s of the window, then the confirmation "If you said …, you're right." | 16.0–20.5 | 8–12 | 160 | **5** | land 0.5 | ChangeValue, CompareStates; table row 2 lands with the reveal |
| 5 | **Mechanism by changing one thing**: same object, one changed quantity, the quotable claim line | 20.5–25.0 | 10–16 | 155–160 | 3 | join | TracePath, CompareStates |
| 6 | **Name and formalise**: the term goes on the thing; one equation form | 25.0–32.0 | 10–15 | 125–135 | 2 | inspect 0.8–1.0 | MapSymbol, EquationTransform; definition card (term + one-line meaning) while the rule is named (PD-18) |
| 7 | **Exception, bounded**: one counter-case on the same board, then the condition | 32.0–40.0 | 12–18 | 130–140 | 4 → 3 | join, join | SwapPart, RevealMismatch, Badge |
| 8 | **Transfer question**: a new case on the same board, solvable with the rule just taught | 40.0–47.0 | 10–13 + window | 150 | 4 | its own window 1.5–3.0 | SwapPart, ChangeValue, PauseForPrediction |
| 9 | **Independent result**: the answer plus "If you got that, you can …" | 47.0–52.0 | 10–13 | 160 | **5** | land 0.5 | ChangeValue, Badge; table row 3 lands with the transfer result |
| 10 | **Close**: an open question the free lesson answers, then `cta_line` | 52.0–57.8 | 10–14 | 150 | 3 | join, join | CompareStates (teaser), Badge; numbered points appear and stay on the end card as the answer sheet (PD-18) |
| 11 | **End card** (the final state of the same scene, ≥ 1.5 s on screen): brand line spoken, motif in the 0.8 s tail; wordmark + "Free lesson: <topic>", no disclosure line (PD-20) | 57.8–60.0 | 3 | 140 | 3 | none; tail 0.8 | EndMotif |

**Total: 120–135 words at the table rate, times `voice.rate_scale`** (PD-07, PD-22: 98–111 for George on eleven_v4; check_script fails a script outside the scaled range).

**How the end card works.** The end card starts on the first word of the outro. It holds the brand line, "AI-generated narration" (Path B) and "Free lesson: <topic>". The 0.6–0.75 s end motif plays after the last word. This meets the 1.5 s on-screen minimum without adding 1.5 s of dead air (A3-07 measured a 2.2 s silent tail).

## 3. The energy curve

Marks by segment, 1 to 11: **4 · 3 · 4 · 5 · 3 · 2 · 4→3 · 4 · 5 · 3 · 3**.

The curve has two peaks:
- the reveal, which confirms the learner's prediction;
- the independent result, the learner's own success.

There is one turn, the exception. The formula is the deliberate trough. Nothing after the transfer drops below 3. The rules:
- at least three distinct marks;
- the maximum sits on a reveal or the transfer (scorecard A21);
- no run longer than 20 s stays within one mark (A3-M1).

## 4. Change events and the retention design

**What counts as a change.** A change is a state change of a science element that the narration is pointing at:
- a value changes;
- a label maps onto a part;
- a path is traced;
- two states are compared;
- a part is swapped;
- a badge or condition appears;
- an equation transforms.

Headline word builds, decoration and camera drift do not count.

**Density target during the explanation** (from the end of the hook to the close):
- at least one change per 3.0 s;
- no gap longer than 3.0 s during speech;
- every spoken clause anchors at least one cue.

During a think window the board deliberately holds still and only the prompt plate is lit. (the purpose of the pause; ≤ 3.0 s).

**Re-hook every 8–12 s** (founder steer). A scrolling viewer decides again every few seconds whether to stay, so each segment either opens a question or pays one off:

| Time (s) | Re-hook | What it does for the scroller |
|---|---|---|
| 0–3 | the question on a complete picture | there is something to look at and something to decide |
| ~10 | the prediction | the viewer commits to an answer, so leaving costs them the result |
| ~16 | the reveal and confirmation | the first payoff: "I called it" |
| ~21 | "Why …?" (the mechanism question) | a new open loop exactly where formal content tends to lose people |
| ~32 | the turn ("But a bulb?") | a reversal: the rule has a boundary |
| ~40 | the transfer | a second commitment |
| ~47 | the independent result | the learner's own success |
| ~52 | the open next question | a reason to follow and open the lesson |

`check_script.py` warns when two re-hooks sit more than 12 s apart. A re-hook is a question, a reveal, the turn or the transfer.

**Share trigger.** The mechanism or reveal beat names one quotable aha line, `on_screen.claim_line`, for example "Same resistor, twice the push, twice the flow". It sits in the result lane as a claim line for at least 1.5 s. Its words are spoken in that beat; it states the rule, not a slogan. One per short: the frame people screenshot.

**Follow and next-step close**, in this order:
1. The open next question ("Why does a bulb's graph curve?"). Use a "next one" tease only when that short is actually scheduled.
2. The CTA, spoken as `cta_line` (PD-14: "Try the free lesson on <topic>.", supplied per request; empty means no CTA). The end card carries the literal fixture text "Free lesson: <topic>".
3. The identity line "Professor Diki Simplified."

There are no engagement prompts (subscribe, like, share, follow), no marks or exam claims and no purchase prompt. In an AC0 child context there is no CTA at all.

## 5. Silence budget and what is forbidden

**Silence** (lead-in plus every gap of 0.3 s or more) is at most 15 % of runtime, which is 9.0 s. The motif tail is excluded because it carries the motif under the end card. A typical budget:

| Item | Seconds |
|---|---|
| Lead-in | 0.3 |
| Prediction window | 1.5–3.0 |
| Transfer window | 1.5–3.0 |
| Three lands at 0.5–0.6 | 1.5–1.8 |
| One inspect | 0.8–1.0 |
| **Total** | **≤ 9.0** |

Joins of 0.2–0.35 s are breaths and are not counted. When both windows are `think_calc` (3.0 s, or 2.7 s at −10 %), keep the lands at 0.5 and make one boundary a join. Every pause carries a purpose: join, land, inspect, think_recall, think_choice, think_calc or pause_video. A pause with no purpose is a defect.

**The voice adds silence between sentences inside a beat.** George measured 0.4–0.66 s at each full stop. So write one sentence per beat; v2 placement then turns each sentence boundary into a planned 0.25 s join.

**Forbidden:** intro bumper or title card; logo animation; spoken disclosure; recap of the recap; countdowns; static frames > 2 s during speech; scene cuts or teardown (PD-03); stroke-by-stroke drawing or word-by-word headlines; spoken "Pause and predict" filler; an answer visible before its window ends; "ExamLeaf".

## 6. Acceptance numbers

| Criterion | Target | Gate |
|---|---|---|
| Duration | 60.0 ± 1.0 s (`target_duration_s` 60, `duration_tolerance_s` 1.0) | check_script (planned); QA A11 (measured) |
| Spoken words | 120–135 × `voice.rate_scale` (PD-22) | check_script |
| First usable idea (`insight_beat` start) | ≤ 10.0 s | check_script; A14 |
| Hook question complete | ≤ 3.0 s target, ≤ 3.5 s accepted | check_script warns |
| Pause policy | every gap labelled, within PD-01 ±10 %; measured silences match the script within ±25 % | check_script; A13 |
| Silence share | ≤ 15 % | check_script (planned); A20 (measured) |
| Prediction answerable | every number in the question was spoken or shown earlier; `check.answerable_from` is on screen | check_script |
| Transfer present | `check.transfer` with its own think window, followed by `feedback.transfer` | check_script |
| Change density | ≥ 1 per 3 s; no gap > 3 s during speech | check_script warns (planned); A15 |
| Outro and disclosure | spoken outro exactly "Professor Diki Simplified."; disclosure on screen | check_script; brand_check |
| D8 momentum proxies | insight ≤ 10 s; payoff ≤ 3 s after the window; energy curve per §3; transfer answer at 70–90 % of runtime; re-hook gap ≤ 12 s; the close is a next step | check_script, check_pd_script, judge D8 |

## 7. Worked timelines

These are planned by `pilotlib.plan` with the default rates. The physics row is the passing sample. Energy uses marks 1–5. In the Pause column, think = think window and conf. = confirmation.

**Physics, brief C01** (sample: 122 words, 59.97 s, silence 13.8 %, insight at 7.5 s, transfer answer at 79 %):

| Time (s) | Words | Spoken | Pause | E | Visual verb |
|---|---|---|---|---|---|
| 0.0–0.6 | – | (complete circuit on screen) | lead-in | – | PreserveObject |
| 0.6–2.9 | 6 | Double the voltage: double the current? | join | 4 | Emphasize |
| 3.1–7.2 | 11 | Two volts, ten ohms: the meter reads zero point two amps. | join | 3 | ChangeValue |
| 7.5–9.7 | 6 | Current is volts divided by ohms. *(insight)* | land 0.5 | 3 | MapSymbol |
| 10.2–13.4 | 8 | Now four volts: what does the meter read? | think_calc 2.7 | 4 | ChangeValue, PauseForPrediction |
| 16.1–20.3 | 11 | Zero point four, exactly double. If you said that, you're right. | land 0.5 | 5 | ChangeValue, CompareStates |
| 20.8–24.5 | 10 | Why double? Same resistor, twice the push, twice the flow. *(claim line)* | join | 3 | TracePath, CompareStates |
| 24.8–31.7 | 15 | Four by zero point four is still ten, the resistance: voltage equals current times resistance. | inspect 0.8 | 2 | MapSymbol, EquationTransform; definition card (term + one-line meaning) while the rule is named (PD-18) |
| 32.5–36.9 | 10 | But a bulb? It heats up, so its resistance rises. | join | 4 | SwapPart, RevealMismatch |
| 37.2–39.8 | 6 | So the rule needs constant temperature. | join | 3 | Badge |
| 40.1–44.5 | 11 | Your turn: six volts, same resistor, what does the meter read? | think_calc 2.7 | 4 | SwapPart, ChangeValue, PauseForPrediction |
| 47.2–51.7 | 12 | Zero point six: if you got that, you can use this rule. | land 0.5 | 5 | ChangeValue, Badge |
| 52.2–54.6 | 6 | Why does a bulb's graph curve? | join | 3 | CompareStates |
| 54.8–57.6 | 7 | Try the free lesson on Ohm's law. | join | 3 | Badge |
| 57.9–60.0 | 3 | Professor Diki Simplified. | tail 0.8 (motif) | 3 | EndMotif |

**Chemistry, balancing H₂ + O₂ → H₂O** (122 words, 59.76 s, silence 14.4 %, insight at 3.5 s):

| Time (s) | Words | Spoken | Pause | E | Visual verb |
|---|---|---|---|---|---|
| 0.0–0.6 | – | (equation and molecule balls on screen) | lead-in | – | PreserveObject |
| 0.6–3.2 | 7 | Is an atom missing from this equation? | join | 4 | Emphasize |
| 3.5–7.2 | 10 | The small two counts atoms: H two is two hydrogens. *(insight)* | join | 3 | MapSymbol |
| 7.5–9.0 | 4 | Left side: two oxygens. | land 0.5 | 3 | Badge (count) |
| 9.5–11.9 | 6 | How many oxygens on the right? | think_recall 1.5 | 4 | PauseForPrediction |
| 13.4–16.4 | 8 | Just one. If you said one, you're right. | land 0.6 | 5 | RevealMismatch |
| 17.0–21.1 | 11 | Atoms can't vanish, so make a second water: two oxygens now. | join | 3 | PreserveObject, ChangeValue (duplicate) |
| 21.4–24.4 | 8 | Now hydrogen is short: two H twos. Balanced. | land 0.5 | 4 | ChangeValue, Badge |
| 24.9–29.9 | 11 | That big two is a coefficient: it copies the whole molecule. | inspect 0.9 | 2 | MapSymbol |
| 30.8–33.9 | 7 | Why not write H two O two? | join | 4 | SwapPart |
| 34.2–39.1 | 11 | That's hydrogen peroxide, a different substance: never change the small two. | land 0.5 | 3 | RevealMismatch, StrikeThrough |
| 39.6–44.8 | 13 | Your turn: magnesium plus O two makes magnesium oxide, what goes in front? | think_calc 3.0 | 4 | ChangeValue, PauseForPrediction |
| 47.8–52.3 | 12 | Two, then two magnesiums: if you got that, you can balance these. | land 0.5 | 5 | ChangeValue, Badge |
| 52.8–54.4 | 4 | Three elements at once? | join | 3 | CompareStates |
| 54.6–57.4 | 7 | Try the free lesson on balancing equations. | join | 3 | Badge |
| 57.7–59.8 | 3 | Professor Diki Simplified. | tail 0.8 (motif) | 3 | EndMotif |

The transfer stays on the same board: the hydrogen and oxygen molecules give way to Mg and O₂ in the same slots. The peroxide line needs a sourced CLM (A1-16).

## 8. Platform metrics the format is built for (all targets are hypotheses)

These are Instagram and YouTube Shorts aggregate insights only: no per-viewer tracking, no child profiling. Every number below is a **[H] starting guess to replace with our own baseline after the first 10 posts**. None is a claim or a benchmark.

| Metric | [H] starting target | On-video lever |
|---|---|---|
| Hook rate (3 s hold) | ≥ 60 % | complete picture at frame 0; question by 3 s; no bumper; first word at 0.6 s |
| 50 % watch-through | ≥ 45 % | prediction at ~10 s and its reveal at ~16 s; re-hook every ≤ 12 s; no static frame |
| 100 % watch-through | ≥ 25 % | the transfer answer at 79 % of runtime; the end card is 2 s, not a tail |
| Shares per 1,000 views | ≥ 5 | the claim line (screenshot-able, correct, quotable) |
| Saves per 1,000 views | ≥ 10 | the formal line plus the condition badge, legible together in one frame |
| Follows per 1,000 views | ≥ 2 | the learner's own success, then a real next question and the free lesson |

Test one lever per A/B pair; claim nothing until measured.
