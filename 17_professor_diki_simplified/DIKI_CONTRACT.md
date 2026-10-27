# Professor Diki Simplified: builder contract v2 for shorts (format `concept_short_60`, 16 Oct 2026)

Status: binding for every builder of a Professor Diki Simplified short. It **replaces `16_pilot_builds_2026-10-16/PILOT_CONTRACT.md` for format `concept_short_60`**. PILOT_CONTRACT still governs `concept_intro` (60–70 s) builds. Decisions cited: `DECISIONS_PD.md` PD-01 … PD-13. Paths are relative to the project root `ExamLeaf_Video_EdTech_Pipeline/`.

## 0. What you build

One 60-second vertical short (1080 × 1920) that teaches one idea, so the learner ends thinking "I can solve this one myself". You write the lesson graph, fixture, `script.json` (v2), one scene and build notes; the lead narrates, renders and runs QA. A failed blocking check (§8) comes back to you with its id; no judge sees a failing build.

```
<video>/lesson_graph.json  fixtures/compute.py  fixtures/fixture.json  script.json  storyboard.md
<video>/s01.src.html  →  tools/build_scene.py  →  scenes/s01.html      (ONE scene per short)
<video>/build_notes.md
```

## 1. One persistent scene (PD-03)

- `script.scenes` has exactly one entry, and every beat lives in it. One cue sheet carries every beat.
- The board (hero) is placed once, visible from t = 0, and afterwards only transforms (ChangeValue, SwapPart, TracePath, CompareStates). Register it with `Diki.hero(el)` + `Diki.PreserveObject(el)` (or `data-role="hero"`) so QA can measure it.
- Nothing tears down; a part leaves only for a named reason (a resistor swapped for a lamp). The end card is the scene's final state. A headline appears whole on its cue and stays until replaced.

## 2. The look: the design system only (PD-08)

- Start from `design_system/diki_scene_base.html` (with `tokens.json`, `diki_runtime.js`, the subject components); build with `design_system/tools/build_scene.py` (inlines, brand and decoration gates, seek lint).
- Lanes from `tokens.json` `lanes.default` (diagram y 452–1316, result 1324–1470); a caption lane only in `captioned`.
- Colour by meaning, one role per hue across subjects; ink is the default. One sans family plus the math fallback; true subscripts.
- Motion only through `tokens.motion.verbs` (reveal 180–300 ms, emphasis 180–350 ms, transform 400–900 ms), driven from `seek(t)`; no back/elastic/bounce/spring. The 12/05 style guides are not used for shorts.

## 3. Script v2

Field reference: `format/script_v2_fields.md` (until it lands: the `pilotlib.py` docstring and `format/sample_v2_script.json`). Required:

- `"schema_version": "script/v2"`, `"format": "concept_short_60"`, `target_duration_s: 60`, `duration_tolerance_s: 1.0`.
- **Slots.** These anchor slots must all occur, with their first occurrences in this order: `hook.question_reveal` → `check.predict` → `reveal.answer` → `check.transfer` → `feedback.transfer` → `close.next_step` → `outro.brand`. Between the anchors you may add `explain.intuition`, `explain.givens`, `explain.prerequisite`, `explain.mechanism`, `worked.step`, `worked.faded`, `explain.formal`, `exam.language` and `misconception.confront` (at most one bounded exception).
- **`pauses: [{purpose, after_s?}]`** after each beat. Purposes and lengths are in §4.
- **`energy`** per beat: `low | mid | high | peak`. Use at least three distinct marks. Put the peak on `reveal.answer`, `check.transfer` or `feedback.transfer`.
- **`insight_beat: true`** on exactly one beat: the first usable idea (givens plus first result), starting ≤ 10 s; the reveal is **`payoff_beat`** (PD-16).
- **`visual_op`** per beat: the motion verb(s) the beat performs on the board. Every spoken clause anchors a meaningful change.
- **`check`** on predict and transfer beats: `{task_kind, asks, answerable_from: [fixture paths]}`.
- **Length.** 120–135 spoken words at 140–160 wpm active rate, and 125–165 wpm in every beat.

## 4. Pause policy (PD-01)

Every silence is a scripted pause with a purpose. Lengths are in seconds; the script may be off by ±10 %, and the measured audio by ±25 %. Use room tone, never digital zero.

| purpose | seconds | use |
|---|---|---|
| `join` | 0.20–0.35 | between clauses of one thought |
| `land` | 0.50–0.70 | after a result lands |
| `inspect` | 0.80–1.20 | to look at a formula or a condition |
| `think_recall` | 1.5 | recall, binary choice, count ≤ 3 |
| `think_choice` | 2.0 | choose 1 of 3–4 |
| `think_calc` | 3.0 | one-step calculation with the numbers on screen |
| `pause_video` | 1.0 hold | multi-step or writing: say "pause the video" |

No unscripted silence over 0.6 s; lead-in 0.3 s (PD-16); room tone at −60 dBFS, never digital zero, counts as silence; tail ≤ 0.8 s carrying the end motif (a silent hold over 1.0 s fails). A window over 2 s shows what to produce (`I = ? A`).

## 5. Prediction and transfer (PD-06)

- Ask `check.predict` only after every given it needs is **on screen** (listed in `on_screen.fx_refs` in the predict beat or earlier) and **spoken**. The givens are in `check.answerable_from`. The hook never states or shows the answer.
- `reveal.answer` lands ≤ 3 s after the window, confirms the learner ("If you said zero point four, you're right"), then gives the why.
- `check.transfer` is a new case on the same board, with new fixture numbers. The learner solves it with the rule just taught. It carries a think pause from §4.
- `feedback.transfer` gives the answer plus conditional confidence ("If you got that, you can use this rule").
- `close.next_step` names the next step in one line: the script's `cta_line`, shaped "Try the free lesson on <topic>." (PD-14), spoken right before "Professor Diki Simplified."; `cta_line` empty means no CTA.

## 6. Brand and disclosure (PD-02, PD-04, PD-12, PD-13, PD-14, PD-20, PD-21)

- The audience-facing name is exactly **Professor Diki Simplified**. "ExamLeaf" never appears in spoken text, on screen, in captions, in fixture display strings, in filenames or in titles; it is publisher metadata only. The other strings in `brand/strings.json` `forbidden` are banned too ("guarantee", "full marks", "100%" in claim text, stock AI phrases). Fixture science values are exempt from "100%" (PD-12).
- The last spoken beat is `outro.brand` with the exact text `Professor Diki Simplified.` **Nothing speaks a disclosure.**
- Brand marks (PD-21): an opening ident, the "Professor Diki Simplified" sticker over the complete board from frame 0 and gone by 2.5 s, and the end-card wordmark. No persistent header in lesson frames; the lesson code is metadata only. There is no logo animation.
- End card (≥ 1.5 s): `Professor Diki Simplified`; `AI-generated narration` (Path B) or `Performed by <name> · voice converted with AI` (Path A); `Free lesson: <topic>` (no URL).
- **End-card text is literal fixture display strings** (`display.ui.endcard_line1` brand line, `display.ui.endcard_line2` "Free lesson: <topic>"; no disclosure line, PD-20), bound with `data-fx`. They are never assembled at runtime (PD-13).
- Audio: one end motif (`brand/motif/diki_end_motif_v1.wav`, 0.70 s) at most 0.1 s after the last word. Set `outro.motif` / `motif_starts: "after_last_word"` (or `motif_at` on the outro beat); `render.py` mixes it at −3 dB and never under speech.
- Optional event accents (`confirm_tick_v1.wav` after a correct reveal, `mismatch_v1.wav` on `RevealMismatch`) go in cue-sheet `sfx[]` entries `{file, at, gain_db}`. Use at most 3, never within ±250 ms of a spoken number, and no music bed under science.

## 7. The 60-second target (PD-07)

Muxed MP4 60.0 ± 1.0 s; silence (≥ 0.3 s below −40 dB) ≤ 15 % of runtime; first usable idea by 10 s; board visible by 1.5 s; a meaningful visual change at least every 3 s of speech. `check_script.py` plans the timeline and fails a plan off target: plan for it, do not discover it at render.

## 8. Checks and thresholds

`qa.py <script.json> --format concept_short_60` runs A1–A21. A11–A21 block a `concept_short_60` build. For other formats they are advisory (reported as warn).

| id | check | threshold (fail) |
|---|---|---|
| A1–A10 | lint L1, cue sheets, screen text = fixture, safe zones, flash, loudness −16 ± 1 LUFS / TP ≤ −1 dBTP, transcript, (A8 legacy, warn; v2 scripts skip its ≥ 4 s think-window clause), manifest + determinism, video = timeline ± 1 frame | unchanged |
| **A11** | duration | outside 60.0 ± 1.0 s |
| **A12** | brand | any forbidden string in spoken text, captions, transcript, scene source, fixture, metadata, or visible DOM text sampled every 2 s; any `brand_check.py` end-card item missing |
| **A13** | pause policy | a pause purpose not in §4; a scripted length outside its band ±10 %; a measured silence outside its purpose band ±25 %; an unscripted silence > 0.6 s; a tail hold > 1.0 s |
| **A14** | first idea, board | `insight_beat` missing or starting > 10 s; diagram lane empty at 1.5 s |
| **A15** | change density | a run > 3.0 s of speech with no visual change in the diagram + result lanes (2 fps; novel-edge fraction ≥ 0.0015); warn below 3.3 changes per 10 s |
| **A16** | diagram fill | diagram lane empty (edge density < max(0.02, 0.5 × median)) for ≥ 1.0 s while speaking; hero height < 0.70 × diagram lane at 25/50/75 % of runtime |
| **A17** | persistence | more than one scene file; diagram similarity between samples 1 s apart < 0.60 before the end card (the last 2.5 s) |
| **A18** | teaching order | anchor slot missing or out of order; transfer without a think pause; a predict given not shown or not spoken by the question |
| **A19** | pace | any beat (≥ 4 words) outside 125–165 wpm |
| **A20** | silence share | > 15 % of runtime (the plan's definition: the 0.3 s lead-in and the end-card tail after the last word are not counted) |
| **A21** | energy curve | fewer than 3 distinct marks; peak not on reveal/transfer |

`brand/brand_check.py`, `design_system/tools/build_scene.py` and `check_script.py` must also exit 0.

## 9. Preview and iterate (your obligations before hand-off)

1. `check_script.py script.json` → OK; answer every warning in the build notes.
2. `build_scene.py s01.src.html scenes/s01.html --fixture fixtures/fixture.json --script script.json --scene s01` → exit 0, no `W_FILL_LOW`, `W_NO_HERO`, `W_MOTION_IN_THINK`.
3. `preview_scene.py script.json s01`; open every PNG (0.3 s, each cue + 0.3 s, each think window, end card); fix empty lanes, crowding, clipping, wraps, anything illegible at phone size.
4. Read the frames as a learner: at 1.5 s is the question's object visible? At each window's end, could a weak learner answer from the screen?
5. After the lead's render, fix each failed A-check at the lowest rung that holds (template default → schema → validator → exemplar → prose). If you think a check is wrong, document the case with frames and numbers; the lead decides.

## 10. Build notes (`build_notes.md`, ≤ 500 words)

Decisions the guides did not make; each pause and its purpose; the energy curve and why the peak sits there; what the board does on every beat; the three things you fixed after preview; the exact commands run and their outputs; anything you could not satisfy, and why.

## 11. Never

- **Never** speak a disclosure or a brand line other than the exact outro `Professor Diki Simplified.`
- **Never** write per-scene files, scene lists, cuts or a teardown. One scene, one board.
- **Never** use bouncy reveals (back/elastic/bounce/spring, scale-pops on values) or animate transform/scale/translate on text or fixture-bound elements.
- **Never** draw stroke by stroke unless the drawing is the mechanism (`TracePath`). Structure appears whole.
- **Never** build a headline word by word in speaking order. A headline is a pre-composed claim of ≤ 5 words shown whole.
- **Never** use a fixed 5 s (or any default) think window. Length follows the task (§4).
- **Never** add decorative props: shelves, pencils, washi tape, halftone bands, ransom tiles, polaroids, boil or wobble, sparkles.
- **Never** show a number, unit, formula, label or UI string that is not a fixture field; never ask a prediction before its givens, or end without a transfer; never call a network service (the lead narrates).
