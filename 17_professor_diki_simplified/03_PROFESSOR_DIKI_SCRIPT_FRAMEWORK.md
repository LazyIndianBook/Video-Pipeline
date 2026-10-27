# 03 · Professor Diki Simplified: scriptwriting framework v1.0.0

**Status (16 Oct 2026):** v1.0.0; skill `skills/professor-diki-script/`. Both exemplars pass `check_script.py` v2 and `check_pd_script.py`. Binding: PD-01 to PD-21 and the founder steer ("not exciting and motivating enough"). A6 (creative benchmarks) is integrated in §4.1.

## 0. The flow: a creator's process with a teacher's skeleton

**17 Oct 2026 (PD-26).** For 60-second shorts the writing method is `11_SIXTY_SECOND_EXPLAINER_METHOD.md` (the "100 Seconds" profile: purpose in the first sentence, one developing example, definitions at the point of use, explicit links, movement with progress, the promise paid before the invitation). This framework's voice (§1, §1b), obligations (§2), artefacts (§3), humour rules (§4) and simplification ladder (§5) still apply underneath it; §6 (the question plan) now serves the quiz format only.

Write like a creator: why stop scrolling? Then engineer every second. The seven obligations (§2) sit underneath, never dropped. One claim plus its condition per short (PD-14). No hype, invented numbers, fear or marks promises.

1. **Scroll test.** Write one sentence: why would a 16-year-old on Instagram stop for *this* idea in the first second? If you have no answer, change the angle, not the wording.
2. **Find the surprise.** Look for one of these:
   - a counter-intuitive fact;
   - a number that feels wrong;
   - a visible contradiction;
   - a classic exam slip (call it a slip; never attach a percentage);
   - an everyday Indian object that hides the idea: a phone charger, the bulb at home, a pressure cooker, Diwali lights, a rocket launch on the news.
3. **Five hooks, one winner.** Write five hooks of different kinds: pattern interrupt, bold claim, challenge, visible puzzle, stakes. Stakes are allowed only if true and sourced. Score each hook 1–5 on the scroll test. Then apply the honesty test: is every word true, and does the payoff keep the hook's promise? Choose the best honest hook. Its complete picture is on screen by 1 s and its question by 3 s.
4. **Open a loop.** Promise the payoff without giving it away ("Watch the meter.").
5. **Take the shortest path on ONE picture.** Keep one persistent board. Re-hook every 8–12 s with a new question, a reversal or the exception. Plan retention in a table (§6); do not leave it to chance.
6. **Effort beat.** Ask one answerable prediction. Every given it needs is already on screen. Size the window by PD-01.
7. **Name the payoff.** The answer lands with a visible confirmation, then gets a name: one true, quotable line a student would send to a friend ("Twice the push, twice the flow.").
8. **Transfer win.** Pose a new case on the same board that the learner solves. Follow it with a conditional confidence line.
9. **Close (PD-14).** An optional light tease for the next short, which may invite a follow ("Next: why hot bulbs give less than double. Follow for it."). Then exactly two sentences: "Try the free lesson on <topic>." and "Professor Diki Simplified." The end card shows the text "Free lesson: <topic>", the brand and the disclosure.

## 1. The Professor Diki voice

**Who speaks, to whom.** A brilliant Indian teacher who enjoys the subject, speaks plainly, anticipates the mistake and makes the student think, talking to one Class 9–10 learner with weak foundations who could swipe away at any second.

**Excitement register:**
- direct address ("you", "your turn");
- present tense;
- contrast ("more, not less"; "never… only");
- concrete nouns (meter, cell, molecule);
- verbs of change (doubles, swings, vanishes);
- punchy lines, with one longer explanatory line per beat;
- Indian everyday examples by default;
- no generic AI phrasing.

**Sentence rules:**
- One idea per sentence: typically ≤ 14 words, never more than 18.
- Never speak a term before it is visible. Give its plain meaning by the next beat.
- Reveal the decision ("Only the voltage changed, so…"); never just announce a result.
- Every explain beat has a consequence or contrast word tied to something visible.
- Never use a standalone naming sentence ("That is the law of…").
- At least one sentence per beat speaks to the learner or says "we".

**Emphasis.** Stress only the changed quantity, a negation or a condition. Stress one word per sentence at most, and never the last word of a falling sentence.

**Warmth without speeches.** Confidence comes from structure: a task the learner can do, then a success they can see. Praise is conditional only: "If you got 0.6, the rule is yours."

**Banned phrases.** The full regex list is `references/banned_phrases.txt`.

| Banned | Replace with |
|---|---|
| "Pause and predict" | State the task: "More current, less, or the same?" |
| "Many think…" | Pose the shortcut instead: "Write H two O two?" |
| "Let's dive in", "Welcome back", "In this video" | Open on the object: "Rockets burn this." |
| "Mind blown", "Amazing", "It's that simple", "Super easy" | Name what changed: "Twice the push, twice the flow." |
| "always is not safe" (a quoted word used as a noun) | Ask it: "Always? Only at constant temperature." |
| Any disclosure, spoken or on screen (PD-20); "ExamLeaf"; "linked below" | Say only `cta_line` and then "Professor Diki Simplified." |

### 1b. Story first (PD-25, 17 Oct 2026)

The founder's rule after the first explainer draft: "be a better storyteller, not just a boring teacher." Every short is told, not taught: open on a scene the learner recognises with the quantities in action; give the quantities roles inside one sustained metaphor (voltage pushes, current flows, resistance holds back) and never mix metaphors; narrate the board as action in the present tense ("watch the meter climb"); make the condition the twist (voice the doubt, show the bend, resolve it); land the example as the pay-off scene; close on the moral, the claim line. Lecture openers are banned phrases ("states that", "is defined as", "we can see that"). The definition card can be formal while the voice tells the story: the card carries the proper wording, the voice carries the meaning.

## 2. The seven obligations: decisions, failures, momentum

| Obligation | Decision | Reject when | Momentum role |
|---|---|---|---|
| **Diagnose** | Which wrong idea or missing prerequisite blocks the learner, and which hook exposes it. | The hook is abstract, has no object, or gives the predict away (A1-08, A1-12). | Hook question by 3 s, at high energy. |
| **Make concrete** | The picture, then the givens and the first result by 10 s (`insight_beat`: "Two volts, ten ohms: point two amperes."). | A term arrives before its picture, or the board is empty at frame 0. | **First insight by 10 s.** |
| **Invite an answerable prediction** | One question, with every given already shown. `task_kind` sets the window. | The learner would need the rule being taught (A1-01), the prompt asks two tasks, or the window does not fit the task. | The effort beat, at 10–15 s. |
| **Show the mechanism by changing one thing** | What changes, what stays the same, and which instrument shows it. | The answer is announced instead of read off the board, or the board resets (A1-03). | Payoff (`payoff_beat`) within 3 s of the window, at **peak**, with the claim line on screen. |
| **Name and formalise** | The term, the condition, the unit, and the exam form ("In the exam…"). | The term first appears in the recap, the noun switches, or the condition is missing (A1-06, A1-33). | The deliberate low point; a re-hook ("Always?") keeps the pull. |
| **Transfer** | A new case on the same board, with one changed parameter, solvable with the rule just taught. | There is no transfer (A1-27), or it needs a new rule. | Answer lands at 70–90 % of runtime, as the second peak. |
| **Close** | The tease, `cta_line`, then the identity line. | It ends on a legal line, a restated recap, hype or a sales pitch (A1-28, A1-M7). | Ends warm, at mid energy, never at its lowest point. |

**Evidence rule.** Every confrontation of a misconception shows its evidence on the board. Evidence is either a fixture counter-value (the meter's 0.4 beside a struck 40) or a sourced observation (the "hydrogen peroxide" label from the fixture). An exception without a fixture value stays qualitative and bounded, and it can become the next short's tease (the hot bulb: "less than double", from the flag `lamp.current_doubles: false`).

**Energy curve.**

| Beat | Hook | Givens | Predict | Payoff | Mechanism | Formal | Confront | Transfer | Win | Close |
|---|---|---|---|---|---|---|---|---|---|---|
| Energy | high | mid | high | **peak** | mid | low | mid | high | **peak** | mid |

The `energy` field takes `low`, `mid`, `high` or `peak`. The tooling also accepts the numbers 2–5.

## 3. The writer's intermediate artefacts

Stored under `artefacts` in the script, in this order:

1. **Scroll-test sentence and surprise** (flow steps 1–2).
2. **One-sentence outcome:** "After 60 s the learner can ___ using ___."
3. **Prerequisite bridge:** the one gap most likely to block understanding, repaired in at most one sentence ("H two: two hydrogens stuck together.").
4. **Source-backed fact sheet:** each fact paired with its lesson-graph node, plus every number from the fixture. Nothing reaches the script unless it is on this sheet.
5. **Four-line causal chain:** system → change → consequence → rule. If the chain needs more than four lines, the scope is wrong (PD-14).
6. **A visual operation beside every line:** one `visual_op`, and a cue anchored on a spoken word. Something meaningful changes every ≤ 3 s.
7. **Five hooks, scored.** Selection rule: the highest scroll score that also passes the honesty test, shows the picture at frame 0, asks by 3 s, does not answer the predict, and is a different kind from the last two openings in the ledger.
8. **"Remove the adjectives" test.** Delete every adjective and adverb. Still teaches? Keep the shorter line. Says nothing? Rebuild it around a concrete noun.
9. **Conversational repair pass** (Super Teacher Step 13): read it aloud to one learner; fix written-sounding lines, hidden decisions, early answers and jokes needing outside knowledge; log original → replacement → reason → science check; run both checkers.

## 4. Humour, analogy, story and meme rules

*Enriched from A6: see §4.1.*

**Humour.** A joke must expose a wrong idea or make a consequence memorable, and the concept must survive it. Zero jokes is fine. Never joke inside a think window. Read the line straight.

**Memes:** only culturally exact and optional, our own graphics as a split-screen contrast, never a licensed reaction clip.

**Analogies** state what corresponds, what does not, and where the science returns; reject one that needs more explaining than the concept. **Stories:** system → change → consequence → explanation, no invented characters.

| # | Usable pattern | Example |
|---|---|---|
| 1 | Tempting shortcut exposed | "H two O two is hydrogen peroxide. Neat trick, wrong chemical." |
| 2 | Absurd consequence of the wrong method | "Multiply instead? Forty amperes? The meter said point four." |
| 3 | Visible contradiction | "Rockets burn this. What's impossible here?" |
| 4 | Indifferent instrument | "The meter doesn't care how confident you are." |
| 5 | Everyday Indian object | "Your phone charger runs on this one rule." |
| 6 | True scale shock (sourced numbers only) | "Five years, about seventy kilos of willow; the soil lost under sixty grams." |
| 7 | Quotable callback | "Twice the push, twice the flow" comes back at the transfer. |
| 8 | Harmless exam friction | "Bigger numbers don't earn bonus marks for looking busy." |

| # | Anti-pattern | Never |
|---|---|---|
| 1 | Joking at the learner | "Only a genius would miss this." |
| 2 | Personification that teaches false science | "Electrons are lazy, so they take the easy path." |
| 3 | Hype | "Mind blown! Physics is crazy!" |
| 4 | A punchline inside the window | A gag spoken during the 2 s think pause. |
| 5 | A meme that needs explaining | A film-star reaction clip over the coefficient rule. |
| 6 | Token code-switching | "Bhai, current toh double hoga!" with no native review. |
| 7 | An invented statistic as the surprise | "90 % of students get this wrong!" |
| 8 | Fear stakes, or a motivational speech | "Miss this and you lose marks." / "Believe in yourself." |

**Quotable-line rule.** Every short has exactly one claim line. It is ≤ 9 words, true, spoken verbatim at the payoff, and shown for ≥ 1.5 s (`on_screen.claim_line`).

### 4.1 Pin, Turn, Release (the Professor Diki signature, from A6)

This stays fixed, I change one thing, watch what answers, see where it stops. **Pin** (first 8 s): name, colour, mark each held quantity. **Turn**: move one quantity; one persistent readout answers. **Release**: once, the pin slips and the rule returns with its condition. **Mark**: close on the ticked answer sheet.

Physics: pin R and constant temperature; turn V, read I; release: the heating filament. Chemistry: pin the subscripts; turn a coefficient, read the tally; release: edit a subscript, water becomes peroxide. Biology: pin carbon; turn its form; release: the one exception the graph licenses.

**Verified patterns** (`A6_sources.json`). Hooks: tempting answer first [S01, S09]; commit before reveal [S05–S07]; one surprise, one gap, closed last [S29, S44]; "Doubt:" card [S46]. Humour: one line, ≤ 4 s, carrying the concept [S21, S30–S32]: dry aside at the shortcut, analogy with its break point [S26], rationed self-deprecation [S31, S63].

**Meme rule.** No trend templates, trending audio or film stills; none verified current and safe for Assam Class 10–12. "6-7" was mocked by March 2026 [S51]; Cockroach Janta Party, the largest 2026 youth meme movement found, is exam-irregularity satire [S52, S53].

## 5. Simplification ladder for weak foundations

Climb down until a Class 8 student could hold the picture. Then climb back up, one rung per beat:

**claim → plain relationship → picture → one operation on the picture → term → exam form**

| Topic | Claim | Picture a Class 8 student holds | Operation | Exam form |
|---|---|---|---|---|
| Ohm's law | I ∝ V at constant temperature | A cell pushes, a resistor holds back, and dots flow past a meter | Double the push and keep the resistor: the dots double and the meter goes from 0.2 to 0.4 | "Current is directly proportional to potential difference, at constant temperature." |
| Balancing | Atoms are conserved, so change only coefficients | Coloured atom balls stuck in pairs; the small 2 means "two stuck together" | Add a whole molecule (never glue on a single atom), then recount the balls | "2H₂ + O₂ → 2H₂O, balanced by changing coefficients only." |
| Photosynthesis | The plant's carbon comes from CO₂ in the air | A tree as a pile of carbon atoms, each tagged with where it came from | Trace one carbon atom from the air, through a leaf pore, into sugar, then into wood | "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂ in sunlight and chlorophyll." |

Every simplification spoken on the way down needs a `SIM` node with its `what_is_lost` (for example, SIM-push-flow).

## 6. The 60-second beat plan (120–135 words at the table rate; times `voice.rate_scale`, PD-22: 98–111 words for George on eleven_v4)

| # | t (s) | Slot (flow step) | Words | Pause | Energy | visual_op | Picture cue |
|---|---|---|---|---|---|---|---|
| 1 | 0.3–3 | hook.question_reveal (3) | 6–8 | join | high | PreserveObject | The whole object at frame 0; highlight what will change |
| 2 | 3–7 | explain.givens (4) | 9–11 | join | mid | MapSymbol | Each label lands on its part, on its word |
| 3 | 7–10 | explain.givens, `insight_beat` | 8–10 | land | mid | ChangeValue | The instrument reads the baseline |
| 4 | 10–15 | check.predict (6) | 9–11 | think 1.5 / 2.0 / 3.0 | high | PauseForPrediction | Options, or "?" on the instrument; answer hidden |
| 5 | 16–20 | reveal.answer, `payoff_beat` (7) | 6–9 | land | **peak** | ChangeValue / RevealMismatch | The instrument confirms; the claim line appears |
| 6 | 21–25 | explain.mechanism (5) | 8–13 | join | mid | CompareStates | Before and after side by side; the unchanged part ticked |
| 7 | 25–35 | explain.formal + exam.language | 18–24 | inspect | low | EquationTransform / Badge | Words morph into symbols; condition badge; exam line |
| 8 | 36–40 | misconception.confront (5) | 9–12 | land | mid | StrikeThrough | The wrong result, struck through, beside the evidence |
| 9 | 40–44 | check.transfer (8) | 9–13 | think_calc 3.0 | high | ChangeValue | One parameter changes on the same board |
| 10 | 47–51 | feedback.transfer | 10–12 | land | **peak** | Badge | Confirmation and a tick |
| 11 | 51–58 | close.next_step × 2 (9) | 7–10 + `cta_line` | join | mid | Badge | Tease card, then the end card |
| 12 | 58–60 | outro.brand | 3 | 0.8 s motif tail | mid | Badge | Wordmark; the motif follows the last word |

Silence (lead-in plus gaps ≥ 0.3 s) ≤ 15 %.

**Retention plan (physics exemplar, planned seconds):** 0.3 question · 2.8 promise ("Watch the meter.") · 6.7 first result (0.2 A) · 9.8 task · 16.2 turn (meter reads 0.4; claim line) · 20.2 "Why?" · 28.1 exception ("Always?") · 35.1 reversal (40 A struck) · 39.6 task (6 V) · 46.2 win (0.6 A) · 50.9 next loop (hot bulbs).

## 7. Before and after (Opus scripts → exemplars)

| Original (video time) | Rewrite | Rule that fixed it |
|---|---|---|
| Physics 00:11 "Pause and predict the current at four volts. Then decide whether always is safe." | "Two volts, ten ohms: point two amperes." … "Now four volts, same resistor. More current, less, or the same?" | Prediction answerable from the baseline shown (SQ-25); one question; B10; a 2.0 s window, not 5.5 s |
| Physics 00:33 "That constant is the resistance: voltage equals current multiplied by resistance." | "Why? Only the voltage changed, so current kept pace. That's Ohm's law: current equals voltage divided by resistance." | Change one thing; reveal the decision; re-hook; a single equation form; no standalone naming |
| Physics 00:46 "But always is not safe. A filament bulb gets hot…" | "Always? Only at constant temperature." The bulb becomes the tease: "Next: why hot bulbs give less than double." | B27; the exception stays bounded and qualitative (fixture flag `lamp.current_doubles: false`, no invented lamp current) |
| Physics 01:06 "AI-generated narration; script by ExamLeaf." | "Try the free lesson on Ohm's law." / "Professor Diki Simplified." Disclosure goes on the end card. | PD-02, PD-14 |
| Chemistry 00:00 "Hydrogen burns in oxygen to make water. Write it down: H two plus O two gives H two O." | "Rockets burn this. What's impossible here?" | Flow step 3: picture at frame 0, question ends at 2.9 s; W04 |
| Chemistry 00:30 "That is the law of conservation of mass." | "Just one. Real atoms never vanish. Bad equations do." | A named payoff that is also the claim line (SQ-42); B29 |
| Chemistry 00:36 "Put a two in front of water. Oxygen: two and two. Hydrogen is four on the right, so put a two in front of hydrogen." | "Mass is conserved, so fix the equation: add a whole water molecule. Two oxygens now, but four hydrogens. Same fix?" | Reveal the decision (A1-15); the whole molecule appears on the board; re-hook within 12 s |
| Chemistry 00:49 "That is hydrogen peroxide, a different substance." | "Why? H two O two is hydrogen peroxide. Neat trick, wrong chemical." | §4 pattern 1; evidence label (SQ-23) |
| Biology 00:40 "Many think a plant is built from soil… About forty percent of glucose, by mass, is carbon." | "The air. Your tree is built mostly from air." Then the sourced willow evidence. | B11; payoff ≤ 8 words with no new number after it (SQ-33); evidence rule |

## 8. Script QA list

**C** = `check_script.py` v2; **P** = `check_pd_script.py`; **J** = an independent reviewer (separate session, Super Teacher review prompt).

| ID | Check | How |
|---|---|---|
| SQ-01, 02 | Closure: every spoken or shown number equals a fixture output | Structural (closure-check, Q-FIX) |
| SQ-04, 25 | Prediction answerable from shown givens; one question; pause fits `task_kind`; answer hidden, then shown in the next beat | Structural (P); number heuristic (C) |
| SQ-05 | Conditional feedback only; no fake sensing | Regex (P) |
| SQ-09, 30 | Forbidden and stock phrases (`banned_phrases.txt`) | Regex (P) |
| SQ-10, 11, 20, 22 | Analogy non-mapping; SIM `what_is_lost`; conditions spoken or shown with each claim | Structural |
| SQ-17 | Emphasis words appear verbatim | Regex (P); placement (J) |
| SQ-23 | Every confrontation shows evidence (`evidence`) | Structural (P); picture fit (J) |
| SQ-26 | Terms shown at first use; plain meaning by the next beat | Structural (P, `terms`) |
| SQ-27 | Transfer present; `feedback.transfer` lands at 70–90 % | Structural (C, P) |
| SQ-28 | Energy curve: hook ≥ high; peak on the payoff; second peak on the win; nothing low after the transfer; ≥ 3 marks | Structural (C, P) |
| SQ-29 | Silence ≤ 15 %; every gap labelled with a PD-01 purpose | Structural (C) |
| SQ-31, 37 | Brand: exactly `cta_line`, then "Professor Diki Simplified."; tease ≤ 12 words; end card "Free lesson: <topic>"; no disclosure on screen or spoken (PD-20); no ExamLeaf | Regex and structural (C, P, brand_check) |
| SQ-32, 34 | One persistent scene; a verb on every beat; a cue on every line; a change every ≤ 3 s | Structural (C) |
| SQ-33 | Exactly one `payoff_beat` on `reveal.answer`, directly after the predict; first sentence ≤ 8 words | Structural (P) |
| SQ-35 | Re-hook (a `rehook` tag, an anchor slot or a question) every ≤ 12 s until the transfer answer | Structural (P fails; C warns) |
| SQ-36 | First insight ≤ 10 s; 120–135 words; 60 ± 1 s; PD-14 scope (one claim plus its condition) | Structural (C) |
| SQ-38 | Sentences ≤ 18 words, and ≥ 80 % of them ≤ 14 words | Structural (P) |
| SQ-39, 40 | Scroll-test sentence present; five hooks of different kinds, one chosen, honest | Structural (P); honesty judgement (J) |
| SQ-41 | Hook picture at frame 0; the hook's question ends ≤ 3.0 s | Structural (P); re-measured after TTS (qa) |
| SQ-42 | Exactly one claim line: ≤ 9 words, spoken, on screen ≥ 1.5 s | Structural (P fails; C warns) |
| SQ-43 | The tease and follow line are optional; "follow" appears only in the tease, claim-free, never a sales line | Regex (P) |
| SQ-18, 44 | Ledger: hook kind, opening, joke premise and close all differ from the previous two in the batch | Ledger diff (J) |
| J-voice | Sounds like a teacher talking to one learner; excitement without hype; every joke keeps the concept intact (D8, PD-09) | J |

## 6b. The explainer beat plan (`explainer_60`, PD-24, 17 Oct 2026)

The founder's call after the first before-vs-after: feed shorts are complete explainers, not question-answer videos. The question devices (prediction window, transfer question, spoken "pause") move to the free lessons and to a later quiz format. What an explainer keeps from this framework: the scroll test, the five-hook draft, a complete first frame with the question in the title ("What is Ohm's law?"), the first usable idea by 10 s, one turn (the "when it breaks" moment), the quotable claim line, structured cards, the PD-14 close.

| # | Slot | Seconds | Job | Writer's test |
|---|---|---|---|---|
| 1 | `hook.question_reveal` | 0–3 | "What is <law>?" plus what it decides | a stranger knows the topic and the promise by 3 s |
| 2 | `explain.definition` | 3–12 | the definition in plain words, tied to the proper one (`insight_beat`) | a weak learner can repeat it |
| 3 | `explain.mechanism` | 12–24 | the board proves it: change one thing, read the answer (`payoff_beat`) | the number on the board is the evidence |
| 4 | `explain.formal` | 24–33 | the formula and what each symbol means, back to the definition | every symbol points at a thing on the board |
| 5 | `explain.condition` | 33–43 | "When does it hold?": the condition and what breaks it | the exception is shown, not asserted |
| 6 | `worked.step` | 43–51 | one example shown, not asked | the learner sees the computation land |
| 7 | `recap.statement` | 51–56 | the rule in one line (`claim_line`) + three points | shareable |
| 8 | `close.next_step` → `outro.brand` | 56–60 | `cta_line`, then "Professor Diki Simplified." | — |

Pauses: join, land, one inspect at most; no `think_*`. Dead time ≤ 10 %. Words 120–135 at the table rate times `voice.rate_scale` (98–111 for George). Spec: `format/explainer_60.md`.
