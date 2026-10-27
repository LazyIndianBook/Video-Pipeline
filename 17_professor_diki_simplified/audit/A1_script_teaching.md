# A1 audit: script and teaching (three Opus videos)

Auditor A1, 16 Oct 2026. Sources: the Opus folders under `16_pilot_builds_2026-10-16/` (script, lesson graph, storyboard, build notes, timelines), the briefs, `measurements.json` and the 1-fps frames (tNNN ≈ second NNN−1). Full records (effect, fix, control) are in `A1_findings.json`: 41 findings: 33 teaching (A1-01…33) and 8 motivation (A1-M1…M8); 4 critical, 30 major, 7 minor.

## 1. Per-video findings

### Physics (phy-ohm-ci-01, 71.9 s)

| ID | t | Exact words / what is seen | Problem | Root cause | Sev |
|---|---|---|---|---|---|
| 01 | 00:11–00:22 | "Pause and predict the current at four volts." Screen: R = 10 Ω, V = 4 V, I = ? only | You cannot answer this without I = V/R, which the video has not taught yet. The 0.2 A baseline (it is in the ASM stem) is never given. The 5.5 s window is dead time | script; contract has no "predict is answerable" rule | **critical** |
| 02 | 00:14, 00:46 | "Then decide whether always is safe." / "But always is not safe." (also the headline) | Two tasks in one window. It uses "always" as a noun, which sounds translated | brief wording; §3 headline-subset rule locks the phrase on screen | major |
| 03 | 00:22–00:32 | "At two volts, the current is zero point two amperes." | Numbers are announced, not read from a meter or derived. The circuit disappears at t023 | script + storyboard | major |
| 04 | 00:05, 00:33–00:45 | "a resistor of ten ohms" … "voltage divided by current stays ten ohms… That constant is the resistance" | The Aha is circular: the resistor is labelled 10 Ω before any reading. Three forms of one law arrive in 12 s | script | major |
| 05 | 00:00–00:45 | numbers → ratio → equation | No intuition (push / narrow part / flow) comes before the formal law | §3 slot grammar lacks an intuition/analogy slot | major |
| 06 | 00:58–01:05 | "So, for a **conductor**… current is **proportional** to voltage" | First use of both terms comes in the recap, and the noun switches from resistor to conductor. "Potential difference" and "ohmic" (named in the brief, needed for the exam statement) are never said | no term-first-use rule; SQ-07 report-only | major |
| 07 | 00:46–00:57 | "A filament bulb gets hot… the current no longer doubles." Screen: "R ↑", struck "×2", no reading | The misconception is confronted by assertion, with no counter-value | brief fixture has no bulb data; SQ-23 asks only for a glyph | major |
| 08 | 00:00–00:05 | "Does twice the voltage always mean twice the current?" over an empty board (t001–t004) | Abstract textbook question with no object and no stakes | brief C01 / 02 §I1 example copied | major |
| 09 | 00:33 | "For **this resistor**…" while only two cards are visible | Narration points at something no longer on screen | storyboard s03 | major |
| 10 | 00:57–01:05 | empty board t058–t060; the recap omits the bulb boundary | Restates instead of retrieving | recap.statement-only grammar | minor |

### Chemistry (chem-balance-ci-01, 73.2 s)

| ID | t | Exact words / what is seen | Problem | Root cause | Sev |
|---|---|---|---|---|---|
| 11 | 00:00–00:05 | "Hydrogen burns in oxygen… Write it down:" (next phrase starts 0.9 s later) | An instruction nobody can obey in that time. No flame is shown | script | minor |
| 12 | 00:08–00:22 | Hook "Count the atoms. Did an atom just vanish?" then predict "Count the oxygen atoms… Which side is short?" | The hook sets the same task and hints at the answer. The 2-vs-1 count is visible on screen, so the 5.56 s window is longer than the task | script + fixed 5 s window | major |
| 13 | 00:04–00:08 | "H two plus O two gives H two O." | Assumes the learner can read subscripts (the prerequisite Super Teacher Step 3 names for this exact topic) | ST guide's 30–60 s repair cannot fit 60 s | major |
| 14 | 00:30, 00:55–00:59 | "law of conservation of mass"; "Change the coefficients in front, never the subscripts inside." | Exam terms are first used inside a prohibition and never labelled on screen. "Mass" is never explained | no explain.definition slot in §3 | major |
| 15 | 00:36–00:48 | "Put a two in front of water… Hydrogen is four on the right…" | The recount is good, but the decisions are hidden: why water, why two, why four (2 × 2) | SQ-24 requires the recount but not the reason | major |
| 16 | 00:49–00:59 | "That is hydrogen peroxide, a different substance." | Strong contrast left abstract. The natural line (the first-aid antiseptic) is unused | no light-line/analogy slot | minor |
| 17 | 00:22–00:48 | the molecules leave at t023; "Put a two in front of water" adds no molecule | The script talks about molecules while the picture shows a ledger | storyboard s03 | minor |

### Biology (bio-photosyn-ci-01, 67.1 s)

| ID | t | Exact words / what is seen | Problem | Root cause | Sev |
|---|---|---|---|---|---|
| 18 | 00:00–00:07 | "…weigh more than a **herd** of elephants" at 204 wpm. **One** small elephant is drawn | Spoken and drawn scale disagree. Fastest beat of all three videos. "hook_colour" is an off-schema node type | §8 fixture rule turned "fifty" into "herd" | major |
| 19 | 00:04–00:13 | "where did all that wood come from?" → "Where did the **carbon** in that wood come from" | Jumps from wood to carbon with no bridge | script | major |
| 20 | 00:19–00:47 | after the window: "Green plants make their own food." The explicit answer comes at 00:47 | The prediction is answered 28 s late; the interaction loop breaks | §3: the next beat need not answer | major |
| 21 | 00:23–00:40 | "stomata", "chlorophyll", "glucose"; "Count the carbon: six atoms on each side" | Three undefined terms. The formula count has no scaffold (no C tracer from CO₂ into glucose) | no term rule; storyboard | major |
| 22 | 00:40–00:52 | "Many think a plant is built from soil… About forty percent of glucose, by mass, is carbon." Empty sky at t041–t042 | Confront by assertion, ending on a mass-percent detour. The obvious evidence (van Helmont's willow) is missing | brief suggested the 40 % line; SQ-23 report-only | major |
| 23 | 00:47–01:00 | "So a tree's carbon came from the air." | The sugar → cellulose → wood chain is never said (it sits in the CLM reasoning field) | script | major |
| 24 | 00:52–01:00 | word equation spoken for the third time | Restatement instead of retrieval | recap.statement-only | minor |

## 2. Cross-video findings

| ID | Finding | Root cause | Sev |
|---|---|---|---|
| 25 | Same skeleton in all three: hook → predict (5 s) → explain → confront → recap → spoken disclosure. Five scenes each; beat 3 always opens with the answer | PILOT_CONTRACT §3 fixed order (enforced by check_script) + one brief template | major |
| 26 | Stock phrases: "Pause and predict" (physics 00:11, biology 00:12), "Many think". Biology build_notes: *Speak "Pause and predict" so the chip is legal* | §3 rule that on-screen text must be a subset of the narration, plus the §4 plate | minor |
| 27 | **No transfer question in any video.** The learner never applies the idea to a new case | §3 grammar has no transfer slot; SR §4 F8's close was replaced by the disclosure | **critical** |
| 28 | Spoken outro "AI-generated narration; script by ExamLeaf." (75–77 wpm, then 2.2 s of silence) breaks the brand rule and ends on a legal line instead of learning | §3 exact outro text; SQ-12 | **critical** |
| 29 | Think window 5.51 / 5.56 / 5.25 s for three different tasks (an unanswerable calculation, a visible count, an intuition guess). It suits biology only. The plate never says what to produce (02 §F1) | contract `think_window_s` 4–6; briefs "5 s"; ST Step 7 / 02 §G3 give 4–8 s | major |
| 30 | No conditional feedback for the likely wrong answer ("If you said soil…") | ST Step 7 loop not carried into the §3 schema | major |
| 31 | Textbook register. "Green plants make their own food" is CLM-autotroph read out word for word. "You/we" counts: 1 / 0 / 0. Sentence length is *not* the problem (means 9.7 / 7.0 / 10.5 words) | closure rule pushes builders to paraphrase CLM statements; the ST conversational repair pass (Step 13) is missing from the contract's reading list | major |
| 32 | No analogies, light moments or stories in 211 s of narration, although natural ones exist (push/pipe, recipe copies, peroxide antiseptic, the willow) | no analogy/story slot; SR §5 pro-rata humour cap | major |
| 33 | No exam-form sentence anywhere | SR §4 F8 "Exam-language conversion: None" | minor |

**Prediction and think window verdict.** Physics: not earned, because the question cannot be answered (01, 02). Chemistry: not earned, because the hook gives away the task and the count is visible; 2–3 s would do (12). Biology: earned. It is a genuine, tempting three-way intuition question with a fair 5.25 s, but the answer arrives 28 s late (20).

Script-vs-picture mismatches are in 03, 09, 11, 17, 18, 21 and 22.

## 2b. Motivation and confidence in the script (founder addendum, digest §6)

**Measures from the timelines.** Time to first insight (the first sentence that answers the hook): physics 00:31.8 (the full answer comes at 00:46), chemistry 00:25.6, biology 00:23 (implied) and 00:47 (explicit). Last learner action: 00:22, 00:22, 00:19, so nothing for the learner to do in the final two thirds. Payoff tag: calm or thoughtful in all three. Close type: legal disclosure in all three (target: next_step).

**Emotional arc, beat by beat (tag, wpm → learner state).**

| Beat | Physics | Chemistry | Biology |
|---|---|---|---|
| b01 hook | curious 162 → mild, abstract curiosity | curious 151 → real puzzle ("vanish?") | curious 204 → wonder, rushed |
| b02 predict | curious 142 → effort blocked, confusion | thoughtful 153 → trivial effort | curious 164 → genuine guess |
| b03 | calm 150 → told the answer | calm 142 → early payoff, then naming a law | calm 158 → no answer, textbook |
| b04 | thoughtful 128 → load peak, circular | calm 146 → the *narrator* succeeds ("Balanced.") | thoughtful 125 → dense count |
| b05 | thoughtful 146 → twist asserted | thoughtful 139 → good tempting shortcut | thoughtful 161 → payoff buried, detour |
| b06 recap | warm 136 → restatement | warm 134 → rule | warm 146 → third repeat |
| b07 outro | calm 75 → deflation | calm 75 → deflation | calm 77 → deflation |

All three share one arc: energy peaks in the first 10 s and falls to 75 wpm on a legal line. The learner never succeeds at anything themselves.

| ID | Finding | Permanent fix (framework rule) | Sev |
|---|---|---|---|
| M1 | No small success before the end in any video | **Payoff rule:** a transfer at 70–90 % of runtime, answerable with only the taught rule, 2–4 s window, then the answer and a conditional confidence line ("If you said 0.6 A, you just used Ohm's law on a new circuit") | **critical** |
| M2 | The energy curve falls; payoff beats get no lift; the video ends at its lowest point | **Energy rule:** energy rises to the payoff (a bright tag plus emphasis on the payoff word); nothing after the payoff runs > 15 wpm below the explain band; the last beat is the close | major |
| M3 | Physics: "always?" curiosity, but the effort is blocked; the twist "But always is not safe." is announced, not revealed | A doable predict; the payoff lands on the meter; the bulb becomes a second prediction answered by its reading | major |
| M4 | Chemistry: the effort is trivial and the success belongs to the narrator ("Four and four. Balanced.") | **Faded-step rule:** the learner makes the last change ("What goes in front of H₂?", 3 s) | major |
| M5 | Biology: the biggest Aha ("the carbon in wood comes from the air") is buried after a semicolon and followed by "About forty percent of glucose, by mass, is carbon." | **Payoff-sentence rule:** the answer gets its own sentence of ≤ 8 words, within 3 s of the window or as the confront's climax, then a pause of ≥ 0.8 s and no new number | major |
| M6 | Flat sentences: "That constant is the resistance: voltage equals current multiplied by resistance."; "That is the law of conservation of mass."; "Green plants make their own food." (more in the JSON) | **Sentence rules:** every explain beat has a consequence or contrast word tied to the visual; ≥ 1 sentence per beat addresses the learner or "we"; no standalone naming sentences; the recap is one sentence a learner could say aloud | major |
| M7 | No close leaves the learner more capable or curious about the free lesson (the brief's "Try the free lesson" was dropped) | **Close rule:** ≤ 15 words, a next capability posed as a question the free lesson answers, then the end motif; no hype, no promise of marks | major |
| M8 | Once the hook closes (chemistry 00:25, biology 00:23), nothing pulls the learner forward | **Open-loop rule:** open a smaller second question within 3 s of the first payoff; no stretch > 15 s without an open question or a task | major |

Each rule's control (energy curve, payoff position, open-question timeline) is in the JSON.

## 3. Permanent fixes by file

- **PILOT_CONTRACT §3:** add `check.transfer`, `explain.intuition` and `close.next_step` slots; derive `think_window_s` from `task_kind`; one question per predict; the answer comes first after the window; exempt `display.ui.*` from the subset rule; offer archetype orders.
- **SCRIPTING_REGISTRY §15:** new SQ-25 and SQ-26; tighten SQ-18, SQ-23 and SQ-24.
- **Super Teacher guide:** add a short-format annex.
- **check_script.py:** each rule becomes a hard check.
- **Lesson graphs:** add the new nodes, under academic review.

## 4. What the scripts do well (verified)

- Sentences are short (means 7.0–10.5 words, maximum 18), and the overall pace of 139–150 wpm is inside the 130–155 band.
- Every spoken and shown number matches its fixture (0.2/0.4 A, 2 = 2 and 4 = 4, C 6 = 6).
- Answers stay hidden during every window, with no counts and no answer leaks. The biology builder removed the brief's leak ("not mainly from the soil").
- Physics states its condition with the law ("constant temperature", revealed on its anchor word) and bounds the exception ("The rule needs constant resistance") in the same loop.
- Chemistry recounts after each change ("Oxygen: two and two… Four and four. Balanced.") and stages the strongest contrast of the set: H₂O₂ vs. 2H₂O.
- The biology hook is concrete and culturally apt (banyan, elephants), and its three-way predict is a genuine misconception probe.
- No hype, fake praise, fake listening, countdowns or marks talk. Misconceptions are corrected by explanation, never with a red cross.

## 5. The three changes with the largest effect (150 words)

1. **End on a transfer.** Make `check.transfer` mandatory: a new case, a short window and conditional feedback (6 V → 0.6 A; Mg + O₂ → MgO; "the plant gained 2 kg: did the soil lose 2 kg?"). Pay for it by dropping the spoken ExamLeaf disclosure (4.4 s) and the over-long windows, then close with one learning step under "Professor Diki Simplified".
2. **Make every prediction answerable and intuition-first.** Show the givens before the window. Ask one question. Size the window to the task. Answer in the next sentence, with a repair for the likely wrong guess. Put an intuition or analogy rung, and each term's plain meaning, before the formal word.
3. **Confront with evidence, in a teacher's voice.** Every confront shows a counter-value or a sourced observation (bulb meter reading, van Helmont's willow, peroxide). Every script then goes through the conversational repair pass, which makes it reveal the reason behind each step.
