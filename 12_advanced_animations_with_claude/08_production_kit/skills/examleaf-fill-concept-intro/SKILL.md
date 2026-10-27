---
name: examleaf-fill-concept-intro
description: Fill the scenes of a 60-70 s vertical concept_intro lesson (hook, predict, reveal-and-compare, confront, recap, disclosure) from an approved script and fixture. Use when the routed format is concept_intro and the science is one relationship, equation or count with one misconception.
---

# Fill concept_intro (Kit v0.1.0, 16 Oct 2026, status PROPOSED)

Evidence base: six pilot builds and four blind verdicts in `16_pilot_builds_2026-10-16/` (paths below are relative to the project root). `A1`-`A10` are checks in `16_pilot_builds_2026-10-16/tooling/qa.py`. `PK-Dnn` are proposed detectors defined in §4.1; until each is built, you run its check by hand from §5. Rule ids `R-0nn` are in `../../RESTRICTIONS.md`.

## 1. When to use / when not

- Use when: `script.json.format == "concept_intro"`, 1080×1920, 5 scenes, beats in the slot order `hook.question_reveal → check.predict → explain.ladder_step (1-2) → worked.step and/or misconception.confront → recap.statement → close.next_step (optional) → outro.brand`, and a `fixtures/fixture.json` exists with every number the script speaks.
- Do not use when:
  - no fixture, or a spoken number has no fixture field → `ESCALATE: MISSING_FIXTURE`
  - the science is a plotted graph, a derivation of more than 3 steps, a formula with brackets or charges, or more than 3 states → `ESCALATE: UNKNOWN_ARCHETYPE`
  - the headline language is not Latin script → `ESCALATE: INDIC_UNVERIFIED`
  - the style is not `doodle-handdrawn`, `editorial-vox` or `paper-collage-vertical` → `ESCALATE: STYLE_NOT_IN_KIT`

## 2. Default path + escape hatch

**Default (exactly one).** Copy `../../templates/concept_intro_scene_skeleton.md` zone by zone into `scenes/s01.html` built on `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`. Keep the runtime, tokens block and the style's L0/L1/L2/L4 layers identical in all five scenes; per scene change only (a) the headline word list, (b) the L3 hero markup with its `data-fx` bindings, (c) the reveal map `{element_id: cue_id}` and (d) the state map `{cue_id: state_key}`. Fill the slot table (§3) for each scene before writing markup.

**Escape hatch (exactly one).** If a scene needs a behaviour the skeleton does not have (a new state kind, a new glyph type), add one named field to that scene's spec handled by the shared runtime, and copy the runtime change to every scene. Never hard-code a time literal. If that would take more than one new field, stop and write `"escalate": "SKELETON_GAP:<what>"` in `build_notes.md`.

## 3. Slot table (one archetype per scene)

| Scene | Archetype | Beat slot(s) | Fixed (copy across briefs) | Varies (from brief and fixture) | Required element ids | Cues |
|---|---|---|---|---|---|---|
| s01 | **Hook circuit / equation card** | `hook.question_reveal` | headline + drawn "?" + underline in top_title; hero setup on L3; no answer anywhere | the setup (circuit parts, unbalanced equation from `display.species.*.parts`, cutout prop); scale values from fixture | `hl_*` words, `qmark`, `setup` (container), one id per setup part (`resistor`, `f_H2`, …), value chips (`v1_chip`, …) | one reveal per part on the word that names it; first cue on the beat's first content word |
| s02 | **Predict pause plate** | `check.predict` | s01 end state carried over; `think_plate` (`data-fx="display.ui.think_prompt"`) in bottom_caption; boil and drift frozen in the window | the unknown marker (`I = ?`, halo on the short element, option cards with pictures only) | `query` (the "?" marker), `think_plate` | `think_plate` hold from `meta.think_windows[0].start` to `.end`; no reveal of any answer token |
| s03 | **Reveal-and-compare panel** | `explain.ladder_step` (+ `worked.step`) | two matched cards or tally rows; relation marks `×2` / `=` (teal) / `≠` (amber) in a gap ≥ 150 px; condition chip in amber; boxed relationship | rows and values from fixture states; which state each cue switches to | `col1_*`/`col2_*` or `row_<El>`, `rel_*`, `cond_chip`, `equation`, `coef_<species>`, `tick` | one value per cue on its spoken number; each coefficient cue also switches the tally state (R-004, R-005) |
| s04 | **Confront panel with change glyph** | `misconception.confront` | same setup as s01/s03 (same ids, one part swapped); change glyph (`R ↑`, highlighted changed subscript) on the causal word; struck shortcut (`×2` struck, wrong formula struck); no red cross | the swapped part, the name of the wrong result, the evidence glyphs | `setup` (reused), `swap_*`, `chg_*` (change glyph), `strike_*`, `name_*` | first sentence answers the predict prompt's open half; `chg_*` on the causal verb ("rises", "changes"); `strike_*` on the shortcut word ("doubles", "write") |
| s05 | **Recap checklist with ticks** | `recap.statement` | checklist rows, one per idea; every relationship and condition from s03 repeated (R-002); tick per row | rows (condition, relationship, rule) | `row1..rowN`, `tick1..tickN`, `cond_chip`, `equation` | tick on the word that completes each idea |
| s05 (tail) | **End-card outro** | `close.next_step` (optional) → `outro.brand` | the end card from two fixture display strings bound with `data-fx` (`display.ui.endcard_line1/2`, PD-13): "Professor Diki Simplified" and "Free lesson: <topic>"; recap visual stays in middle_visual; no disclosure line (PD-20) and nothing else promotional (no URL, QR code, handle or price) | none | the two `data-fx` end-card lines | reveal on the first word of `outro.brand` |

Per-scene spec fields (types): `headline: [[word, occurrence_in_beat, isClaim]]` · `reveals: {element_id: cue_id}` · `states: {cue_id: state_key}` (state keys from the fixture state table) · `holds: {element_id: cue_id}` · `layers: "L0".."L4"` (fixed per style).

## 4. Rules (14; each links a detector)

1. MUST keep the middle_visual zone carrying explanatory ink at every sample inside a beat; a gap over 0.5 s, or any gap while science is spoken, fails. Carry the previous panel over. — PK-D01 (R-001)
2. NEVER show a container before its first content element; hide `setup`, cards and plates until their first child reveals. — PK-D11 (R-017)
3. MUST show every relationship, equation and condition on its anchor word as a fixture display string (e.g. `display.conditions.constant_temperature`), and again in the s05 recap rows. — PK-D02, SQ-22 (R-002)
4. MUST build s04 in s03's setup: reuse its ids, swap one part, reveal `chg_*` on the causal word and `strike_*` on the shortcut word. An isolated prop fails. — PK-D05, SQ-23 (R-003)
5. MUST change one coefficient or quantity per `worked.step` cue and switch the tally to that cue's fixture state (`unbalanced → step1 → balanced`) on the same cue; the narration recounts aloud ("Oxygen: two and two"). — PK-D06, SQ-24 (R-004)
6. NEVER let any state-bearing element lag the equation shown: numerals, circles, `=`/`≠`, the "short" highlight and the headline all read the same `data-state`. — PK-D03 (R-005, R-015)
7. MUST build formulas from `display.species.<key>.parts[]` spans with a lowered `sub` (60-70 % size, ≥ 0.25 em drop, lining figures) and coefficients from `display.coefficients.<state>.<key>` at full size in the accent colour; NEVER type `₂`. — PK-D04 (R-006)
8. NEVER let s01 or s02 show or say the predict answer before `think_windows[].end`; the window shows the unknown marker and `think_plate` only. — SQ-04, PK-D09, A8 (R-007, R-016)
9. MUST set each beat's headline to ≤ 6 of that beat's spoken words, looked up as (beat, word, occurrence in beat) from the cue sheet, at ≥ 59 px in the style's display face. — check_script, PK-D07 (R-008)
10. MUST build the style's mandatory layers in every scene (skeleton §3) and NEVER use Inter, Helvetica or system-ui for the headline. — PK-D08 (R-009)
11. MUST bind every science glyph and UI string with `data-fx`; nothing typed. — A3 (R-014)
12. MUST reveal with opacity only; NEVER animate transform/scale/translate on text or fixture elements, never CSS transitions; reveal `at` sits in `[t0 − 0.05, t0]`. — A1, A2, A9, PK-D10 (R-012)
13. NEVER let an equation or ratio wrap; keep ≥ 24 px between any chip and a board edge, outline or neighbour. — A4, PK-D12 (R-018)
14. MUST check every spoken number against a `compute.py` assert before narration; a brief number that disagrees with the fixture is reported, not used. — SQ-02, compute asserts (R-019)

### 4.1 Proposed detectors (to implement in `examleaf-anim-qa`; thresholds are [Hypothesis] until calibrated on the pilot frames)

| id | Property | Input | Fails when |
|---|---|---|---|
| PK-D01 | middle zone not empty | MP4 at 2 fps, ink density in the `middle_visual` band from the tokens (≈ y 518-1177 at current insets) | a run > 0.5 s below the decoration-only density inside a beat, or any run overlapping a science word |
| PK-D02 | condition/relationship glyph present | script nodes (`CLM.assumptions`, relationships), cue sheet, DOM at anchor t0 + 0.3 s and in the recap scene | the bound `data-fx` element is absent or invisible at either time |
| PK-D03 | state agreement | DOM samples every 0.25 s; `data-state` on state-bearing elements | two visible state-bearing elements carry different states |
| PK-D04 | subscript glyph test | render of H₂O, 2H₂O, H₂O₂ at 1080 width; DOM boxes | sub bottom ≥ baseline, or sub size outside 60-70 %, or a U+2080-2089 char in formula text |
| PK-D05 | confront evidence | s04 DOM vs s03 ids; cues | fewer than 50 % of s03 setup ids reused, or no `chg_*` reveal on a causal word, or no `strike_*` |
| PK-D06 | worked recount | cues and `states` map | a coefficient reveal cue has no state switch in the same beat |
| PK-D07 | headline limits | DOM | > 6 words, or computed font-size < 59 px |
| PK-D08 | style layers and face | DOM `data-layer` attributes; computed headline font-family | a mandatory layer missing, or face in `fonts_ban` |
| PK-D09 | answer hidden | ASM answer tokens and the predict reveal values; DOM text before `think_windows[].end` | any answer token visible |
| PK-D10 | no early reveal | MP4 frames at each cue's word t0 − 0.2 s | the cued element is already visible (catches a shifted mux that A10's length check could miss) |
| PK-D11 | no empty container | DOM per sample | a visible container with no visible content child |
| PK-D12 | no wrap, clearance | DOM boxes | `.eq`/`.ratio` line count > 1, or clearance < 24 px |

## 5. Pre-submit checklist (yes/no)

- [ ] Every scene's middle zone has visible ink at t = 0.3 s and at every cue + 0.3 s preview frame (opened and looked at)?
- [ ] Every condition and relationship in the script is a `data-fx` element revealed on its word and repeated in s05?
- [ ] s04 reuses s03's setup ids and has a `chg_*` and a `strike_*`?
- [ ] Each coefficient cue switches the tally state, and no frame shows a balanced equation over an unbalanced tally?
- [ ] Formulas use `parts[].sub` spans; no `₂` anywhere in scene text?
- [ ] No answer token visible before the think window ends; the plate is `display.ui.think_prompt`?
- [ ] Every headline ≤ 6 spoken words at ≥ 59 px in the style's face; style layers present in every scene?
- [ ] Reveals are opacity-only; no `transform` in any animated property; no `transition`?
- [ ] `lint_seek_contract.js --level 1` ok ×5, `check_script.py` OK, `preview_scene.py` exit 0 with both sources `injected`?
- [ ] `compute.py` runs and asserts every spoken number?

## 6. Reading validator errors

Each error has `code`, `path`, `expected`, `got`, `fix`. Apply only the `fix`; change nothing else. Common ones from the pilot:
- `E_WORD_MISSING` / `E_TEXT_WORD_MISSING`: a headline word or occurrence is not in that beat; pick a word the beat speaks.
- `W_REVEAL_MISSING`: an element has `data-reveal` but no cue; add the cue to `script.json` or remove the attribute.
- `W_ELEMENT_NO_CUE` / `W_CUE_NO_ELEMENT`: id mismatch between script and DOM; rename the DOM id to the script's.
- `W_TEXT_OVERLAP`: raise the row gap; never shrink below the token sizes.
- A3 mismatch: the DOM text differs from the fixture; fix the binding path, never the fixture.

## 7. Verification

You are not done until lint, `check_script.py` and `preview_scene.py` return 0 errors for all five scenes and every §5 item is "yes". Do not state that the video is complete; write what you ran and its output in `build_notes.md`. The lead runs `qa.py` (A1-A10) after narration and render.

## 8. Escalate when

- 3 failed attempts on the same validator error (the controller counts);
- `UNKNOWN_ARCHETYPE`, `MISSING_FIXTURE`, `STYLE_NOT_IN_KIT`, `INDIC_UNVERIFIED`, `SKELETON_GAP:<what>`;
- a brief number or claim disagrees with the fixture or lesson graph (report it, do not "fix" the science);
- a rule here conflicts with the contract or tokens (tokens and contract win; report the conflict);
- refusal.

## 9. References

- Golden (candidates, not yet carded): physics/opus (`16_pilot_builds_2026-10-16/physics/opus/`), chemistry/opus (`…/chemistry/opus/`). Biology is unjudged.
- Negative (to card from the real failing builds): N-R001-01 physics/haiku s04-s05 empty zone; N-R005-01 chemistry/haiku s03 stale tally; N-R006-01 chemistry/haiku Unicode subscripts.
- Skeleton: `../../templates/concept_intro_scene_skeleton.md` · Restrictions: `../../RESTRICTIONS.md` · Edge cases: `../../EDGE_CASES_pilot.md`.

## 10. Evals

Input packages are the pilot briefs, frozen as of 16 Oct 2026 (biology with the corrected oxygen count). Scores are the pilot rubric (`16_pilot_builds_2026-10-16/tooling/JUDGE_RUBRIC.md`): pedagogy = D1+D2+D3+D7, visual = D4+D5+D6+D7, each out of 20.

| Eval ID | Input package | Expected | Pass rule |
|---|---|---|---|
| EV-CI-01 | `16_pilot_builds_2026-10-16/physics/brief.md` (Ohm's law, doodle-handdrawn) | condition chip on "temperature" and in recap; ×2 marks; filament lamp in the same loop with `R ↑` and struck `×2`; V = I × R boxed and in recap | A1-A10 pass; PK-D01/D02/D05/D08 pass; blind judge vs physics/opus: pedagogy ≥ 18 and visual ≥ 14 (opus scored 19 and 15), no blocking defect; in ≥ 4 of 5 samples |
| EV-CI-02 | `16_pilot_builds_2026-10-16/chemistry/brief.md` (balancing H₂ + O₂, editorial-vox) | lowered subscripts; teal full-size coefficients; tally re-derives on each coefficient (`unbalanced → step1 → balanced`); H₂O₂ vs 2H₂O side by side with counts | A1-A10 pass; PK-D03/D04/D06/D09 pass; judge vs chemistry/opus: pedagogy ≥ 18, visual ≥ 14 (opus 19 and 15), no blocking defect; ≥ 4 of 5 samples |
| EV-CI-03 | `16_pilot_builds_2026-10-16/biology/brief.md` (photosynthesis, paper-collage-vertical) | O 18/18 from the fixture (not the brief's original 24); no "fifty elephants" number on screen; hook does not say "not from the soil"; soil-vs-air confront in the same tree setup with the carbon fraction glyph | A1-A10 pass; PK-D01/D02/D05/D09 pass; compute asserts pass; no blocking defect from either judge lens (no opus score yet; set the bar after biology is judged); ≥ 4 of 5 samples |
