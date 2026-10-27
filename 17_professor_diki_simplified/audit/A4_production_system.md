# A4 · Production-system root causes (Opus concept_intro pilots, 16 Oct 2026)

Inspected the system behind `16_pilot_builds_2026-10-16/*/opus/`; measurements from `narration/timeline.json`, `cues/*.cues.json` and `audit/measurements.json`. Rungs: **R1** template default, **R2** schema, **R3** validator, **R4** exemplar, **R5** prose.

## 0. Headline finding

The Opus builders mostly did what the system told them to do. Nearly every recurring deficiency traces to a written rule, a constant or a missing check. On all three videos, **QA A1–A10 passed 10/10** (`opus/qa/report.json`), and the Kit then named these builds "Golden candidates" (`08_production_kit/skills/examleaf-fill-concept-intro/SKILL.md` §9). QA checks whether a render is *correct*. Nothing checks *learning sequence, persistence, time use, identity or brand*. The rules that touch those (Kit R-001, R-017, R-023; SQ-22–24) are R5 prose with "proposed" detectors. No PK-D01…D19 exists in any `.py` or `.js` file.

## 1. Deficiency → cause

**1.1 Over-length (67.1 / 71.9 / 73.2 s): system.**
- `PILOT_CONTRACT.md` §0 and §3 say "60–70 s", with example `target_duration_s: 65`. Every brief repeats "60–70 s", and all three scripts set 65.
- `tooling/check_script.py` L82–84 estimates `words/2.4 + pauses + think`. It omits `narrate.py` `LEAD_IN_S = 0.6` and `TAIL_S = 1.6`, and it only prints, never fails. Physics was estimated at 68 s and passed.
- `qa.py` A8 accepts 55–80 s, as a warning only.
- About 11 s of fixed overhead: lead-in 0.6, think 5.0 (measured 5.51), pauses about 4.0, spoken disclosure about 4.4, tail 1.6 (measured 2.19).
- The 1,000-character budget is a quota cap, not a duration control: 1,000 characters is about 75 s of speech at 144 wpm.

**1.2 The same 5 s hold for every prompt: system, four layers.**
- The briefs ask for "a 5 s think window"; contract §3 says 4–6; `check_script.py` L49 rejects anything under 4 s (so the audit's 1.4 s cannot pass); `qa.py` A8 requires ≥ 4 s.
- The source is `03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md` L437 ("Simple mental predictions might receive 4–8 seconds"). That guide was written for 10-minute lessons, and nobody scaled it for a Short.
- `pause_after_s` (0.3–0.8 s) has no purpose label; each video has 15–19 unlabelled silences of 0.3–1.0 s.

**1.3 "ExamLeaf" footer, spoken and shown: system.**
- `tooling/pilotlib.py` L13: `DISCLOSURE = "AI-generated narration; script by ExamLeaf."`.
- `check_script.py` L47 enforces it exactly; contract §3 makes it the last spoken beat and §4 puts it on screen.
- `qa.py` A7 then verifies it was *spoken correctly*. QA certifies the defect.

**1.4 Resets (physics 00:57; biology's six representations): system.**
- Each brief prescribes a scene list (physics: "hook circuit; predict pause; ratio reveal; filament exception; recap + disclosure").
- Contract §4 requires one HTML file per scene, with scene time starting at 0.
- `narrate.py` L131–141 tiles scenes at first words; `render.py` L72–74 joins them with `ffmpeg concat -c copy`: a hard cut into a fresh DOM.
- Nothing carries one scene's end state into the next; "carry the previous panel over" (R-001) is prose. The Kit fixes one archetype per scene; physics s05 is a new checklist board ("s05 opened on an empty board").

**1.5 Diagrams become useful late: template default plus the anchoring rule.**
- `scene_template.html` starts every cued element at `opacity:0` and reveals it at `t0 − 0.05` of the word that names it.
- `validate_cue_sheet.py` warns on reveals > 0.10 s early.
- The Kit adds "one reveal per part on the word that names it" (§3 s01). The diagram is therefore only complete once the narration has named every part: in physics s01 the first reveal lands at 2.23 s and the last at 9.67 s of an 11.2 s scene.
- Longest stretches with no visual change: chemistry s03 8.96 s (from 25.6 s), chemistry s05 8.35 s, and s02 in every video 6.5–7.6 s.
- `hold_times_s.headline_min 1.2` is only a floor. There is no maximum-static rule.

**1.6 Slow headlines and elastic pops: template default.**
- `buildText` reveals one span per word on its `t0`, so a headline is complete only when its last word is spoken.
- `buildCues` gives every reveal `scale 0.6→1 backOut`, an elastic overshoot. Physics also put `translateY/scale backOut` on words and fades each headline out at beat end (`t >= h.end`), which adds a per-beat reset.
- Kit R-012 (opacity only) came after these builds, and the template still ships `backOut`.

**1.7 Small explanatory content: tokens.**
- `vertical_safe_zones.tokens.json` uses placeholder insets (top 250, bottom 450) and zone shares 0.22/0.54/0.24. That leaves `middle_visual` 659 px tall, 34 % of the frame.
- The 24 % caption zone holds no captions, only the think plate and disclosure.
- R-023 (hero fill ≥ 0.7 of the middle zone) is still "proposed". The real cause is over-constraint with reserved space left empty, not an "unconstrained" layout.

**1.8 Identity varies across videos: system.**
- The three briefs assign three styles; `05_style_guides/README.md` §2 picks a style per scene job ("one illustrative style per lesson"). Nothing sets an identity across the series.
- Contract §4 says "system stack" while every style bans `system-ui`, and fonts are not vendored (COMPARISON L-09). Each builder picked a face: Chalkboard SE, Georgia, or the collage's.

**1.9 Textbook register: mostly system, partly builder judgement.**
- Contract §3 says a sentence may not assert anything its nodes do not say. The nodes are NCERT "short statements", and the briefs' "Teach:" lines are NCERT sentences. The narration restates them ("That is the law of conservation of mass").
- The pilot graph schema (§5) has no analogy node, and SCRIPTING_REGISTRY SQ-10 requires an ANL node first. Analogy and story are blocked by construction.
- Four tags only (curious, calm, warm, thoughtful); SQ-05/06/07 are report-only and absent from `check_script.py`.
- `JUDGE_RUBRIC.md` D3 rewards "register fits l9_10".

**1.10 Content defects seeded by the briefs: system (no brief gate).**
- Biology: the brief asks about "the carbon in the wood" and claims "most of dry mass is carbon", but the fixture computes carbon *in glucose*, and the brief invites "about forty percent". The Opus notes record the fix-up.
- Physics: the brief's "decide whether 'always' is safe" became "But always is not safe".
- Chemistry: the brief's own hook leaked the answer (L-13). The "Did an atom just vanish?" half-answer is builder judgement, and SQ-04 has no automated check.

**1.11 No transfer, no learning check: system.**
- `pilotlib.SLOTS` has no transfer slot, and `check.retrieval` is optional.
- The `assessment_item` is never required to be spoken.
- SCRIPTING_REGISTRY §4 F8 says close with `next_artefact_pointer`. The pilot replaced that with the disclosure, so brief C01's closing question and "Try the free lesson" are both missing.

**1.12 QA checks rendering, not teaching: system.**
- A1–A10 cannot see learning sequence, persistence, hero size, empty or static time, brand, per-beat pacing, think-window fit, or cross-video identity.
- A4 samples only elements with an id and text, so SVG heroes are never measured.
- `examleaf-anim-qa/references/qa_rubric.md` L55 puts teaching quality and pacing out of scope and leaves them to ST/NA reviewers. The pilot had no human approvals (contract §0).

## 2. Review loop audit

| Stage | Caught | Missed |
|---|---|---|
| Builder self-check (lint, `check_script`, preview PNGs) | layout bugs (V at t = 0, ×2 crowding, empty card 4 s, art under panels) | length, holds, resets: not in the contract |
| `qa.py` A1–A10 | loudness, determinism; the 0.6 s A/V offset only after judges found it | everything in 1.12 |
| Blind Opus judges (two lenses, A vs B) | empty-zone seconds, empty-board hook, crowded chip, ransom cap, chlorophyll tag | 60 s target, think-length fit, brand, cross-video identity (one subject per judge), "slow/boring" |
| Kit synthesis | Haiku gaps | Opus's own defects. Opus became the exemplar (R4), and eval bars are anchored to its scores ("pedagogy ≥ 18, visual ≥ 14") |

**Structural flaw.** The rubric is comparative (`winner`, `gap_for_weaker`). Every loop moved Haiku toward Opus, and none moved Opus toward the founder's target. The judges saw contact sheets and three frames per scene. The rubric has no absolute threshold, no hard gate, and no criterion for duration or brand.

## 3. Permanent controls

### 3.1 Rule changes (exact wording)

1. **Contract §0/§3 (R2 + R3).** Replace "60–70 s" with: "**Hard maximum 60.0 s of muxed video; plan 52–58 s.** `target_duration_s` ≤ 58. The estimate counts lead-in, tail, every pause, every think window and the outro."
2. **Think window (R2).** Replace "`think_window_s` 4–6" with: "`think_kind` ∈ {`recall` 1.2–2.0 s, `predict_one_step` 1.4–3.0 s, `compute` 3.0–5.0 s}; `think_window_s` lies in its kind's band; a window over 2.0 s shows what to produce." Every `pause_after_s` > 0.4 s carries a `pause_kind`: `breath` 0.2–0.4, `after_causal` 0.6–1.0, `inspect_transform` 1.0–2.0.
3. **Outro (R1/R2).** Delete the exact-disclosure sentence. Replace with: "**No beat speaks a brand or disclosure.** The final 1.5 s shows `brand.end_card` ('Professor Diki Simplified') and `brand.ai_label`. 'ExamLeaf' never appears in spoken text, captions or visible pixels." `pilotlib.DISCLOSURE` becomes fixture-bound `brand.*`. *Founder or legal decision needed:* whether an on-screen AI label alone satisfies SQ-12.
4. **Scenes (R1).** Add: "A video is one **persistent stage**. A scene boundary changes annotations, not the board. The hero (`data-rep`) survives every boundary unless `scenes[].reset_reason` is set. At most two representation switches per video." Remove the scene lists from the briefs.
5. **Slots (R2).**
   - New order: `hook` → `concrete` → `check.predict` → `explain.mechanism` → `name.formal` → `misconception.confront` (optional) → `check.transfer` (**required**: new fixture numbers, answer after its window) → `close`.
   - `explain.mechanism` cites a SIM or ANL node before `name.formal`.
   - The graph schema gains an **ANL** type with `maps`, `breaks_at` and `formal_return`.
6. **Brief gate (R3).**
   - A brief declares `question_target`. The hook, the predict answer and the confront answer must all name it.
   - Every spoken fixture value is `on_chain: true`; off-chain values, such as 40 % of glucose, are rejected.
7. **Style (R2).** `script.style` becomes the enum `professor-diki@1.0`: one headline face, one math face, paper `#F5F2EA`, ink `#16263A`, and subject accents only.

### 3.2 Template and token defaults (R1)
- **`scene_template.html`:**
  - The hero (`data-role="hero"`) is visible from t = 0, and cues annotate it.
  - The headline appears whole on its first word (one 200 ms fade) and stays until replaced.
  - Delete the `backOut` scale; reveals become `cubicOut` opacity over 180–300 ms.
  - Add `meta.carry_in`, the previous scene's end state, injected by `narrate.py`.
- **Tokens 2.0:** shares 0.16/0.66/0.18 while no captions are burned in; `zones.middle_visual.min_fill 0.7`; `motion.max_static_s 3.0`; `equation_transform_ms [400, 900]`.
- **`render.py`:** allow one long scene per video, so boundaries become state changes instead of file cuts.

### 3.3 New QA checks (R3, in `qa.py`, all blocking)

| ID | Name | Measures | Threshold | Reads |
|---|---|---|---|---|
| A11 | duration_hard | muxed length; full `check_script` estimate | ≤ 60.0 s; estimate ≤ 58 s | ffprobe, `timeline.json`, `script.json` |
| A12 | brand_hygiene | `/examleaf/i` in beat texts, VTT, STT transcript and visible DOM text at every sample; end card present | 0 hits; card shows "Professor Diki Simplified" | `script.json`, `captions.vtt`, `qa/transcript.json`, DOM |
| A13 | think_fit | window inside its `think_kind` band; measured −40 dB silence | ≤ band max + 0.4 s | `script.json`, mix |
| A14 | time_to_useful | share of hero ink visible | ≥ 80 % by 1.5 s (hook) / 0.5 s after each scene start | DOM `[data-role=hero] *` |
| A15 | max_static | longest gap with no cue or state change inside teaching beats (think windows excluded) | ≤ 3.0 s | cue sheets, timeline |
| A16 | empty_middle (PK-D01) | ink density at 2 fps in the `middle_visual` band | no run > 0.5 s below the calibrated floor | MP4 |
| A17 | persistence | `data-rep` equal across each boundary unless `reset_reason`; hero bbox IoU at the boundary | IoU ≥ 0.6; ≤ 2 switches | DOM ± 1 frame |
| A18 | hero_size | hero bbox height relative to the middle zone | ≥ 0.70 | DOM |
| A19 | identity | headline and label font-family, background and palette against `professor-diki@1.0`; one chrome hash per batch | exact | DOM, tokens |
| A20 | learning_sequence | slot order concrete → predict → mechanism → name → transfer → close; answer hidden until the window ends (PK-D09); transfer uses fixture values not shown earlier | all true | script, graph, cues, DOM |
| A21 | beat_pacing | wpm per beat against its band (130–155 / 105–125 / 145–165) | ±5 % | `timeline.json` |
| F15 | lint | `backOut`/`scale`/`translate` on `[data-fx]` or headline spans | error at L1 | `lint_seek_contract.js` |

### 3.4 Regression tests
Freeze the current Opus builds as negative fixtures in `17_professor_diki_simplified/regression/neg/`:

| Input | Expected failure |
|---|---|
| physics/opus | A11 (71.93 s); A13 (5 s for `predict_one_step`); A12 (b07); A17 at the 57.4 s boundary; A14 in s01 (complete at 9.67 s) |
| chemistry/opus | A15 (8.96 s at 25.6 s; 8.35 s at 64.8 s); A19 (editorial serif) |
| biology/opus | A17 (5 switches); A20 (40 % off-chain; "wood" asked, "carbon" answered); A16 (s04 empty sky, 2.2 s) |
| all scripts | `check_script.py` rejects the `DISCLOSURE` text, and rejects 5 s for `recall` |

The repaired physics pilot is the positive fixture and must pass A1–A21. `tooling/regress.py` runs both sets before any judge sees a build.

### 3.5 Exemplar (R4) and prose (R5)
- Re-card the Opus pilots as **negative** examples N-A11…A20, and delete "Golden candidates".
- The repaired physics build becomes golden only after it passes A1–A21 and scores ≥ 85 on the absolute scorecard.
- New `restrictions_lint.py` fails the Kit build when a restriction marked `block` names a "proposed" verifier. This stops rules from sitting as prose while the defects come back.

## 4. The improvement loop

1. **Render:** deterministic and hashed, as today.
2. **Auto-checks:** A1–A21 plus `regress.py`. A failure goes back to the owning file with its check id, and no judge sees a failing build.
3. **Judge rubric:** an *absolute* scorecard using the external weights, threshold 85, with A11, A12 and A20 as hard gates. Judges get the full MP4 with audio. A separate cross-video panel sees all three subjects together for identity and repetition. The question is the founder's target ("I can solve these myself"), not A vs B.
4. **Fix at the lowest rung that holds:** template default, then schema, then validator, then exemplar, then prose. Record the rung in the restrictions file.
5. **Regression:** every judge finding becomes a frozen negative case plus a check (or a written reason it cannot be checked); a finding seen twice with no check is a process failure; the suite re-runs on every contract, template or token change.

## 5. Preserve

- **Fixture-bound glyphs** (`data-fx`, A3, `compute.py` asserts): caught biology's O 24 → 18 and refute "numbers detached".
- **Seek-deterministic rendering:** the identical in-order procedure, `--disable-gpu`, serial renders, and A9.
- **Provider word timings:** v4 `with-timestamps`, plus A10 for A/V length.
- **Hash binding:** `script_sha256` and `narration_audio_sha256` in every cue sheet; content-hash caching never re-bills an unchanged beat (about 2,285 characters of quota left).
- **`meta.beats_text` and `think_windows`:** they make timed annotation possible on a persistent stage.
- **SQ-04, SQ-20 and the same-setup confront:** the filament lamp in the same loop, with R ↑ and the struck ×2, is the seed of the persistent board.
