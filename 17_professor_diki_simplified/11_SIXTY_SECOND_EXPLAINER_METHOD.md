# 11 · The 60-second explainer method (the "100 Seconds" profile for Professor Diki Simplified)

**Status (17 Oct 2026).** Founder decision PD-26: Fireship's "100 Seconds" series is the editorial reference for every 60-second short. This document is the full writing method; the skill `skills/professor-diki-script/` applies it, `check_script.py` and `check_pd_script.py` enforce the measurable parts, and `tooling/JUDGE_RUBRIC_PD.md` judges the rest. Inputs: the founder's steer of 17 Oct 2026 and the external editorial profile PDS-60-Editorial-1.0 (`Professor_Diki_Simplified_Production_Kit.zip`, 17 Oct 2026), adapted to our audience and to decisions PD-24 (no pause questions in shorts) and PD-25 (story first). The reference was inspected as structure, not imitated in wording, voice or branding.

**The promise the writing must pass:** *One minute. One idea you can use.* A viewer leaves able to do one thing they could not do sixty seconds earlier, with the condition that makes it true. The line is an editorial test, never a spoken slogan.

## 1. What we take from the reference, and what we do not

| We take | Why it fits a Class 10 learner on a phone |
|---|---|
| **The explanation starts in the first sentence.** Topic named, purpose given, no greeting, no ident beat. | The scroller decides in three seconds; our opening ident is on screen, not spoken. |
| **One developing example carries the whole short.** The same circuit, reaction or specimen is changed, measured and explained from first frame to end card. | It is our one-persistent-board rule (PD-03) with a reason attached: every definition serves something the viewer is already trying to do. |
| **Definitions arrive at the point of use.** The instrument explains the quantity it measures; the part explains its property; the two terminals explain where the voltage applies. | A glossary before the lesson is where weak learners leave. |
| **Compact language.** One claim per sentence, concrete nouns, decisive verbs, the words that carry meaning, conditions and causality kept, everything else cut. | Our voice runs at 117–142 words per minute; every filler word costs a second of teaching. |
| **Movement with progress.** Each beat has a visible explanatory action: locate, label, apply, compare, substitute, transform, verify. | A2 and A15: a still board during speech is the fastest way to lose the feed. |
| **Personality that comes from the subject.** Dry, confident, warm; a relevant aside when the material offers one. | A6: forced jokes and meme templates read as fake; a true observation reads as a person. |
| **A finish that pays the opening and offers one next gain.** | PD-10/PD-14: the free lesson is the next step; the promise is paid inside the short. |

| We do not take | Why |
|---|---|
| The developer-level density. | Our learner needs the foundations taught inside the same minute; we compress scope and filler, never conditions, units or reading time. |
| The sign-off wording, catchphrases, voice or visual gags. | Original voice; the brand is the opening ident and the end card (PD-21). |
| A pause for the viewer to think (the external profile's 2.5-second gap). | The reference never pauses, and PD-24 moved prediction windows to the free lessons. The student's one action is posed and answered in the flow; a viewer who wants to think pauses the video. The question format `concept_short_60` keeps the window for quiz shorts. |

## 2. The shape of a minute (functions, not fixed sections)

| Function | Seconds (plan) | What the writing does | What the viewer sees |
|---|---|---|---|
| **Purpose** | 0–5 | Name the topic and give the task: what the viewer will be able to read, calculate, predict or explain. A question is optional. | The complete board from frame 0 with the target concealed or unknown; the opening ident. |
| **Example starts, definitions ride on it** | 5–28 | Introduce each necessary quantity beside its object, in the order the example needs them. Each definition is a sentence of plain words plus the proper term and unit. | Locate, label, apply: the instrument, the part, the terminals, the given values. |
| **Visible reasoning** | 28–38 | The calculation or relation, built on screen: words, meanings, values with units, operation, answer, interpretation. | The equation assembles; the readout appears with the completed step. |
| **The change** | 38–46 | Change one thing, keep the rest, state the consequence and its cause ("same resistance, so …"). This is the student's one action, posed and answered in the flow. | ChangeValue, the comparison kept side by side, the table row. |
| **The rule and its scope** | 46–53 | Name the rule the example obeyed and the condition that made it true; say where it stops. | The rule on the sheet; the condition chip; the exception shown, not argued. |
| **Pay-off and next gain** | 53–60 | Resolve the opening task in one line (the claim line), then one concrete next learning gain, then the brand. | The answer sheet (points card), the end card with "Free lesson: <topic>". |

Order follows the subject's needs, not the table; a definition, an example and a demonstration may share one action. What never moves: the purpose is first, the pay-off precedes the invitation, the brand is last.

## 3. Rules (M01–M12)

- **M01 Finish line.** One observable outcome in the brief (`outcome`): identify, explain, calculate or predict something. The title promises that outcome and nothing larger.
- **M02 Start now.** The first sentence names the topic and the viewer's purpose (`promise_line`). No greeting, no "in this video", no standalone brand beat.
- **M03 One developing example.** One object or process is the backbone; every action changes or explains it; a second scene must resolve a teaching need the first cannot.
- **M04 Definitions at use.** A necessary term is introduced beside its object or representation before anything depends on it. A topic word may appear in the title before its definition; a calculation may not use an undefined symbol.
- **M05 Explicit links.** Transitions carry the logic: because, so, across these two points, keep this fixed, change this, watch. The reviewer flags any place the viewer must invent the connection.
- **M06 Words for meaning.** Cut duplicate summaries, repeated directions, history, promotion. Keep referents, units, conditions, arithmetic steps and feedback. Sentences of one claim, under 20 words.
- **M07 Movement with progress.** Every beat has a visible explanatory action; highlights may change inside a stable shot; no cut quota, no claim at every change.
- **M08 A human teacher.** Natural connected speech, warmth, decisive verbs. Humour optional and only when the subject offers it; never a quota, never at the student's expense.
- **M09 The student's one action, in the flow.** One prediction or recall posed with every given visible and already taught, answered in the next sentence with its reason (PD-24: no hold in shorts).
- **M10 Close the promise.** The opening task is resolved before the invitation; the condition stays attached to the rule in the recap.
- **M11 Continue the learning.** One concrete next gain that continues the task ("two more meters in the free lesson"); the route must exist (business layer verifies).
- **M12 Prove the fit.** Words 120–135 at the table rate times `voice.rate_scale` (PD-22); measure the generated voice; if clarity does not fit, narrow the outcome or split the short. Never trim a unit, a condition or a reading hold to make time.

## 4. Language

Open with the thing, not with the law's name followed by "states that". Prefer "the meter counts the charge passing each second" to "current is defined as the rate of flow of charge", then attach the proper term and unit. Verbs of action: apply, double, hold, keep, watch, read, swap. Links in every transition (M05). Numbers spoken the way the fixture shows them. Banned: lecture openers, "let us understand", "in this video", empty intensifiers, any sentence a textbook would print unchanged. The one metaphor of the short is chosen once and kept (PD-25).

**Register (PD-27, 17 Oct 2026).** Write as a teacher talking to a small child, in full flowing sentences: "When electricity passes through a wire, something pushes it along. That push is called voltage, and we measure it in volts." Never caption fragments ("Resistance, ten ohms."), never colon lists spoken aloud, never a noun phrase standing alone as a sentence. Join ideas with when, then, so, because, and. Plain words first (push, flow, holds back, wire, bulb), the technical word second, the unit third, each in a full sentence. The NCERT definition is spoken once in simplified form and shown on the card in NCERT's words, with the chapter and section named. A reader should not be able to tell where one line ends and the next begins: it is one person talking.

**Density and pace (PD-28).** The reference runs 190–230 words per minute. Our shorts target 175–205 effective words per minute with plain words: 150–205 spoken words in the minute (`pace: fast`), pauses only joins and short lands, dead time ≤ 8 %, something changing on the board at least every 2.5 s. Pack the minute: the NCERT definition, the formula and its rearrangements, two or more numeric cases on the same board, the representation NCERT uses (the V–I line), the units, and at least one edge case with its condition. Speed never removes a definition, a unit or a condition; the transcript check must still match every word.

## 5. The writer's five passes

1. **Specification.** The outcome, the prerequisite boundary (what the viewer must already know), the dependency map (which meaning must precede which step), the ledgers: terms, quantities with units, claims with sources, the likely misconception, the controlled example with its held variables.
2. **Three openings.** Three first sentences that make the same promise; score each on topic clarity, interesting uncertainty and whether the short can pay it off; choose one with a reason (the scroll test of framework §0 still applies).
3. **Narration and visuals together.** One beat table: for each beat the new meaning or action, the dominant visual focus, the visible change, the transition word that connects it to the previous beat. Build the example while teaching its quantities; no glossary slide.
4. **Compression.** Cut redundancy and scope, never units, conditions, steps, feedback or reading time. Check every sentence for one claim, under 20 words, a verb of action.
5. **Measurement.** `check_script.py` for the plan at the calibrated rate; narrate; re-time from the measured words (pauses at the low end of their bands, tempo within 0.95–1.05); never speed the voice to meet the clock.

## 6. Review standard (evidence, not adjectives)

The teaching reviewer and the blind judges answer these with a quoted line and a beat id:

1. What exact promise does the opening make, and which beat resolves it?
2. What is the viewer trying to do while the definitions are introduced?
3. Which visible action grounds each essential term, quantity and condition?
4. For each transition, why does the next idea follow? Cite the line.
5. Does each beat add meaning, reasoning, application, feedback or necessary reading time?
6. Could the learner answer the in-flow prediction from the audience-facing content alone?
7. Is the energy made by progress, or by passing over meaning too quickly?
8. Does the ending complete the short and offer a real next learning gain?

Reject: a promise not paid inside the short; a definition that exists only in production notes; a calculation with an undefined symbol; misleading motion; rushing a technical phrase to fit. Hold: measured timing, source support or the promised destination unknown. Machine coverage: A14 (first usable idea), A15 (movement), A18 explainer spine (purpose first, pay-off before the invitation, required functions present), A20 (dead time ≤ 10 %), A21 (energy peak on the reasoning or the change); `check_pd_script.py` warns when the opening lacks the topic or a task verb, when transitions lack link words, when `outcome` or `promise_line` is missing.

## 7. Worked example: Ohm's law in 60 seconds (`demo/physics_v4_method/`)

Outcome: the viewer can read the current meter's unit, calculate one current from voltage and resistance, and predict the reading when the voltage doubles, knowing why unchanged resistance matters. Promise line: "Ohm's law lets you calculate electric current. Let's read this meter." The example is one circuit whose meter is unknown until the calculation; the definitions of current (at the meter), resistance (at the resistor, temperature steady) and voltage (across the resistor's ends, energy per coulomb) ride on it; the change is 2 V → 4 V answered in the flow; the rule is named with its scope and the bulb shows where it bends; the claim line "Twice the push, twice the flow" pays the opening; the next gain is "two more meters in the free lesson". The full script, storyboard and checks live in the demo folder; narration waits for the ElevenLabs quota reset (15 Nov 2026) or the paid plan.

## 8. Fields and pipeline mapping

| Field (script v2) | Meaning | Checked by |
|---|---|---|
| `format` | `explainer_60` | spine, dead time, peak slots |
| `profile` | `pds-60-method-1.0` (this document) | recorded in the cue sheet meta |
| `outcome` | the one observable outcome (M01) | check_pd_script warns if absent |
| `promise_line` | the first sentence (M02) | must equal the hook beat's first sentence |
| `claim_line`, `cta_line` | the pay-off line and the next gain (M10, M11) | existing checks |
| slots | `hook.question_reveal` first; `explain.*`, `worked.step` in the order the example needs; `recap.statement`, `close.next_step`, `outro.brand` last | `pilotlib.spine_problems` |

## 9. Delivery rate and the fast profile (PD-28)

| Item | Value | Source |
|---|---|---|
| Reference, Docker in 100 Seconds | 449 words / 1:58 ≈ 228 wpm | transcript mirror, 17 Oct 2026 |
| Reference, Python in 100 Seconds | 457 words / 2:22 ≈ 193 wpm | transcript mirror, 17 Oct 2026 |
| Our story voice (George, eleven_v4, story tags) | 138–142 wpm measured | `demo/physics_v3_explainer/narration/timeline.json` |
| Reference, four more videos (Git, Docker, Linux, SQL; founder's kit, 17 Oct) | 195–235 wpm, about 214 average; about 208 over the first 59 s | transcript mirrors, kit v2.1 |
| Target for Class 10, second-language listeners | 175–205 effective wpm; 150–205 words per 60 s (`pace: fast`); the first fast narration decides | PD-28 |
| Means | a quick natural read (direction tags; a faster voice when the paid plan allows an audition), then `narrate.py --tempo` up to 1.3 (pitch kept) if the natural read is slower; A7 transcript must still pass | PD-22, PD-28 |
| Plan | `pace: fast` sets the word band to 150–205 and the per-beat band to 150–215 wpm; `voice.rate_scale` is re-measured on the first fast narration | check_script, qa A19 |

The reference audience is adult developers in their own language; ours is younger and often listening in a second language, so the target sits just under the reference and the words are plain. Both ends of the band are tested with learners before either becomes the rule.
