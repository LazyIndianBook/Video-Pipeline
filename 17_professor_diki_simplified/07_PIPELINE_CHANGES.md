# 07 · Pipeline changes: QA A11–A21, render audio extras, contract v2, regression suite (16 Oct 2026)

Status (16 Oct 2026):
- Built and run. The regression suite passes 12 of 12 tests (`tests/run_all.sh`), plus the brand and motif self-tests.
- A11–A21 were run on all five pilot renders; the before-table is in §2.
- Nothing here has been checked by a human viewer.
- Sources: A4 §3 (proposed controls), A2/A3 findings, PD-01 … PD-13.

The A4 audit numbered its proposals differently. **The ids below are binding**, and the scorecard (`09_SCORECARD.md`) uses them.

## 1. Every change

### 1.1 `16_pilot_builds_2026-10-16/tooling/qa.py`

A1–A10 moved into `legacy_checks()` unchanged except A8: for a script with `pauses[]` (v2) its "think window ≥ 4 s" clause no longer applies, because A13 judges pauses by purpose. Each new check is a pure function that returns `{status, reasons[], evidence}`. `run_new_checks()` gathers the inputs. Reason strings are stable, because the regression tests assert them.

| check | function | enforces | threshold |
|---|---|---|---|
| A11 | `a11_duration` | muxed length (FFmpeg) | `concept_short_60`: 60.0 ± 1.0 s, else fail. Other formats: script target ± 1 s, warn |
| A12 | `a12_brand` | brand hygiene | calls `brand/brand_check.py` by subprocess and reads its JSON (spoken text, scene source text, fixture strings, metadata, end-card items). Adds what it cannot see: visible DOM text sampled every 2 s and 0.3 s before each scene end, `captions.vtt`, and the STT transcript. Any forbidden hit or missing end-card item fails. Without `brand_check.py`, it falls back to a built-in list |
| A13 | `a13_pauses` | PD-01 pause policy | see the rules below |
| A14 | `a14_first_idea` | time to the first usable idea | `insight_beat` (givens + first result; the reveal is `payoff_beat`, PD-16) start ≤ 10 s; diagram lane not empty at 1.5 s |
| A15 | `a15_change_density` | visual change while speaking | 2 fps frames; a change is a novel-edge fraction ≥ 0.0015 between samples in the diagram + result lanes. A static run > 3.0 s during speech fails; < 3.3 changes per 10 s warns |
| A16 | `a16_diagram_fill` | no empty board; hero size | empty = edge density < max(0.02, 0.5 × median during speech); an empty run ≥ 1.0 s while speaking fails. The hero bbox height (`Diki.hero`-registered elements or `[data-role=hero]`, from the DOM at 25/50/75 % of runtime) must be ≥ 0.70 × the diagram lane (tokens `fill.hero_min_of_diagram`) |
| A17 | `a17_persistence` | one scene, no teardown | more than one scene file fails; similarity between diagram-lane edge masks 1 s apart (3×3 dilation) < 0.60 before the end card (the last 2.5 s) fails. Reports the minimum and its time |
| A18 | `a18_teaching_order` | PD-06 sequence | see the rules below |
| A19 | `a19_pace` | rate per beat | active wpm (first word to last word) within 125–165 for every beat of ≥ 4 words |
| A20 | `a20_silence_share` | dead time | silence ≥ 0.3 s below −40 dB (room tone at −60 dBFS counts) ≤ 15 % of runtime, on the plan's definition: the 0.3 s lead-in (PD-16) and the end-card tail after the last word are excluded (A13 polices both) |
| A21 | `a21_energy` | energy curve | ≥ 3 distinct `energy` marks; peak on `reveal.answer`, `check.transfer`, `feedback.transfer`, the `payoff_beat` or the insight beat (low/mid/high/peak = 2/3/4/5) |

**A13 rules.** Silences come from FFmpeg `silencedetect` (−40 dB, ≥ 0.3 s) on the shipped MP4 and are matched to the gap after a beat. Fail: measured silence outside its purpose band ±25 %; scripted `after_s` outside its band ±10 %; unknown purpose; no `pauses[]`; unscripted silence > 0.6 s; tail > 1.0 s. Warn: a scripted pause ≥ 0.45 s missing from the audio.

**A18 rules.** All script v2 anchors present, first occurrences in order (hook → `check.predict` → `reveal.answer` → `check.transfer` → `feedback.transfer` → `close.next_step` → `outro.brand`); the transfer has a think pause; each predict given (`check.answerable_from`, else `givens`, else `parameters.*` fx_refs) is in fx_refs by the question and, if numeric, spoken by then; `check_script.py`'s own answerability lines are added as reasons.

**Shared inputs.** `lanes()` reads tokens `lanes.default` (diagram y 452–1316, result 1324–1470; fallback height × 0.54 centred); `frame_series()` decodes 2 fps greyscale 216 × 384 frames (→ `qa/frame_series.json`); `detect_silences()` / `silences_from_timeline()` (synthetic fixtures).

**CLI.** `--format` selects thresholds (`concept_short_60` enforced; other formats turn A11–A21 fails into warn); `--only new` (or ids) re-runs those checks and keeps the rest of `qa/report.json` (this kept the paid A7 results); `--no-dom` skips Playwright. Results go into the existing `report.json`/`report.md` with reasons.

**Calibration** (five pilot renders): board boil 0.0001–0.0003 novel-edge vs reveals ≥ 0.0015; documented resets 0.00–0.57 similarity vs persistent reveals ≥ 0.76; documented blanks below half the median edge density.

### 1.2 `16_pilot_builds_2026-10-16/tooling/render.py`

- `audio_events()`: the **end motif** (if `brand/motif/diki_end_motif_v1.wav` exists and the outro beat has `motif_at`, seconds before the end, default 1.4, or script v2 `outro.motif` is set with `motif_starts: "after_last_word"`), at `motif_gain_db` default −3 dB (−6 → −9 dBFS peak), clamped to start ≥ 0.1 s after the last word (manifest records `moved_from`, `truncated`); plus every cue-sheet **`sfx[]`** `{file, at (scene-local), gain_db (default −6)}`, files resolved against the build folder then `brand/motif/`.
- `mix_extras()`: one fixed FFmpeg graph (`adelay` + `volume` + `amix normalize=0`, bit-exact flags) → `narration/mix_final.wav`, then muxed. No events: the old path, byte for byte. Manifest gains `audio_events`, `audio_final_sha256`.
- Determinism verified: two `--mux-only` runs on a copy of physics/opus with motif and tick gave the same MP4 sha256; the regression test checks identical WAV bytes, onset within 20 ms, peak −9 dBFS. No `--end-card-hold`: the scene holds the end card.

### 1.3 New files

- `17_professor_diki_simplified/DIKI_CONTRACT.md`: the v2 builder contract for `concept_short_60`. It supersedes PILOT_CONTRACT for shorts and covers PD-01…PD-13 and A1–A21.
- `tests/test_regressions.py`, `tests/run_all.sh` and `tests/fixtures/good/` (script v2, timeline synthesised at 150 wpm, fixture with `display.ui.*` end-card strings, a minimal scene).
- `12_advanced_animations_with_claude/08_production_kit/RESTRICTIONS.md` § v0.2.0 (R-027…R-038) and the same rows in `restrictions.json`.

### 1.4 Side effects on the pilot folders

In the five evaluated build folders only `qa/` changed: `report.json`/`report.md` now hold A1–A21 (A1–A10 kept), and `frame_series.json` was added.

## 2. Before-table (regression baseline, `--format concept_short_60`)

| check | physics/opus | chemistry/opus | biology/opus | physics/haiku (v1) | physics/haiku_v2 |
|---|---|---|---|---|---|
| A1–A10 | 10 pass | 10 pass | 10 pass | 10 pass | 10 pass |
| A11 | fail (71.9 s) | fail (73.2 s) | fail (67.1 s) | fail (73.9 s) | fail (73.5 s) |
| A12 | fail | fail | fail | fail | fail |
| A13 | fail (11 reasons) | fail (9) | fail (9) | fail (9) | fail (9) |
| A14 | fail | fail | fail | fail | fail |
| A15 | fail (4.0 s static) | fail (8.0 s) | **pass** (2.5 s) | fail (8.0 s) | fail (4.5 s) |
| A16 | fail (4.5 s empty) | fail (5.5 s) | fail (12.5 s) | fail (13.5 s) | fail (3.0 s) |
| A17 | fail (min 0.43 @ 47.0 s) | fail (0.00 @ 49.0 s) | fail (0.00 @ 40.0 s) | fail (0.00 @ 20.5 s) | fail (0.11 @ 45.0 s) |
| A18 | fail | fail | fail | fail | fail |
| A19 | fail (1 beat) | fail (1) | fail (3) | fail (3) | fail (3) |
| A20 | fail (22.5 %) | fail (25.0 %) | fail (22.0 %) | fail (23.0 %) | fail (23.2 %) |
| A21 | fail | fail | fail | fail | fail |

The Opus failures match the audit: **A11** 7–13 s over (A3-01). **A12** "ExamLeaf" spoken (b07), in timeline, captions, transcript and on screen in s05 (physics @ 69.4 s); no lockup/brand/disclosure/free-lesson line; last line not the outro (A3-02, A2-15). **A13** "script has no pauses[] with purpose labels", the fixed think silence (physics "unscripted silence 17.00–22.50 s (5.51 s) > 0.6 s"), 0.70 s lead-ins, 0.6–1.1 s inter-beat gaps, 2.2 s tails (A3-03/05/06/07). **A14** no `insight_beat`, first explain at 18.9–22.6 s (A3-M2); physics and chemistry empty at 1.5 s (A2-04). **A15** chemistry 8.0 s static from 29.0 s while the law is spoken (A3-M3). **A16** empty lanes at physics 1.0 and 58.0 s, chemistry 1.0 and 49.5 s, biology 7.0, 19.0, 40.5 s (A2-02); no hero registered (A2-07). **A17** five scene files; teardowns at physics 22.5/46.5/57.5 s, chemistry 21.5/49.0/60.0 s, biology 7.0/18.5/40.0/52.5 s (A2-01). **A18** no `reveal.answer`, `check.transfer`, `feedback.transfer`, `close.next_step`, `outro.brand`; chemistry/biology predicts declare no givens (A1-01/02). **A19** disclosure beats 74–77 wpm, biology hook 204 wpm (A3-08). **A20** 22.0–25.0 % silence after excluding lead-in and tail (25.7–28.5 % raw, A3-01). **A21** no energy marks (A3-09).

**Known false pass.** Biology A15 passes because the collage's ambient motion (sun rays, sparkles) registers as change. The audit counted biology static gaps of 4.3 s and 3.1 s from the cues. PD-08 removes ambient decoration from shorts; until then a judge must watch for it.

**Haiku comparison.** The same eleven checks fail on both Haiku builds. Haiku v1 has more empty-lane time (13.5 s) and the longest static run (8.0 s). Haiku_v2 (with the Kit) is closest to passing A16 (3.0 s empty) and A15 (4.5 s), but it still tears down at every cut.

## 3. The review loop

1. **Render** deterministically (`narrate.py`, `render.py`); audio extras come from script and cue sheets, never by hand.
2. **Auto-checks:** `qa.py --format concept_short_60` (A1–A21) + `brand_check.py`, `build_scene.py`, `check_script.py`. A failed blocking check returns to the builder with its id and reason; no judge sees a failing build.
3. **Judge rubric:** the absolute scorecard (`09_SCORECARD.md`, with **D8 Momentum and motivation**) on the full MP4 with audio, plus a cross-video panel; `tooling/scorecard.py` combines QA and verdicts; hard gates include A11, A12, A17, A18, A20.
4. **Fix** at the lowest rung that holds (template default → schema → validator → exemplar → prose); record the rung in RESTRICTIONS.
5. **Regression:** each judge finding becomes a frozen negative case in `tests/test_regressions.py` plus a check (or a written reason it cannot be checked); `tests/run_all.sh` runs on every change to qa.py, render.py, tokens, contract or brand strings.

## 4. How a builder runs it

```sh
PY=~/Movies/DikiStudio/.venv/bin/python                     # 27 Oct 2026 (PD-29): the pipeline venv, with mlx-audio
T=16_pilot_builds_2026-10-16/tooling; V=<video folder>
$PY $T/check_script.py $V/script.json                       # plan: slots, pauses, 60 s, givens, energy
$PY 17_professor_diki_simplified/design_system/tools/build_scene.py $V/s01.src.html $V/scenes/s01.html \
    --fixture $V/fixtures/fixture.json --script $V/script.json --scene s01
$PY $T/preview_scene.py $V/script.json s01                  # look at every PNG
# lead: narrate (local voice, PD-29) + render
$PY $T/narrate_voxcpm.py $V/script.json                     # per-beat takes + word times; listen to any LISTEN beat, --redo it
$PY $T/narrate.py $V/script.json && $PY $T/render.py $V/script.json
$PY $T/qa.py $V/script.json --format concept_short_60       # A1–A21 → $V/qa/report.{json,md}
$PY $T/qa.py $V/script.json --format concept_short_60 --only new   # re-run A11–A21 after a fix, keep A1–A10
sh 17_professor_diki_simplified/tests/run_all.sh            # regression suite (must stay green)
```

The venv lives in the founder's studio folder (`05_narration_system/local_voice_voxcpm2/SETUP.md`). The earlier scratchpad `narr_venv` was partly removed by macOS's /tmp cleanup and no longer runs. Set `PY` to the project venv on another machine.

## 5. What remains proposed or unresolved

- **Hero fill threshold.** The brief said "≥ 45 % of frame height"; the tokens make the diagram lane exactly 45 % and the hero ≥ 70 % of it. A16 follows the tokens (≥ 605 px; ohm demo hero 793 px) and uses 45 % only without tokens. Lead to confirm.
- **A15 ambient motion** can pass A15 (§2). A cue-sheet cross-check (change must coincide with a cue or `visual_op`) is proposed.
- **`pauses[].after_s`** is read as the gap after the beat (pilotlib v2); mid-beat pauses (`at` ≠ "end") are not matched.
- **A18 is a heuristic:** a given that is shown and spoken may still lack its tool (physics passes the givens part although A1-01 calls it unanswerable). PK-D09 (answer hidden) is still proposed.
- **Provider timing:** the positive fixture is synthetic; the first narrated v2 short (demo/physics_v2) is the real positive test for A13's ±25 % bands.
- **Kit:** `restrictions.json` lacks R-020…R-026 (Kit 0.1.1), not back-filled; PK-D02–D04, D06, D07, D10–D12, D14, D15, D18, D19 remain proposed (advisory under 0.2.0); `restrictions_lint.py` (A4 §3.5) is not built.

## Later the same day (16 Oct 2026, evening): changes after the founder's four later steers

| Change | Where | Control |
|---|---|---|
| Design system rebuilt as the paper cut-out collage house style for every subject, v2.0.2 (worlds per subject, chips, stickers, tape, sheets; verbs Pop, Slide, Chips, Tape, Card; light bands only, luminance floor 0.18; headline chips up to 6 words) | `design_system/` (CHANGELOG.md), `05_DESIGN_SYSTEM.md` | `build_tokens.py` contrast and band checks; `build_scene.py` structural gates; `qa_scene.py` purity, W_CARD_*, W_WORLD_MISSING, W_IDENT_MISSING |
| Structured elements: table / definition / points cards in a `carded` layout, rows and table cells appearing on their words | `design_system/components/card.js`, tokens `lanes.carded`, `type.card`, verb `Card` | `qa_scene.py`; `check_script` accepts `visual_op: Card` (verb list now read from the tokens) |
| No "AI-generated" line on screen or spoken (PD-20); brand only as an opening ident and on the end card (PD-21) | `brand/strings.json` 1.1.0, `brand_check.py` (disclosure in the lesson is a violation; brand text required in the first scene), `check_script.py`, `JUDGE_RUBRIC_PD.md` gates, `scorecard.py`, `DIKI_CONTRACT.md` §6, format docs, exemplars, test fixtures | `brand_check.py --selftest`; `tests/run_all.sh` 12/12; `test_v2.py` |
| Brand migration of 56 audience-facing locations in 17 pipeline files to Professor Diki Simplified wording | see `brand/MIGRATION_LOG.md` | `brand_check.py --selftest` |
| Voice calibration (PD-22): `voice.rate_scale` multiplies the planned slot rates and the PD-07 word band; `narrate.py --tempo` (speech only, pauses exact, ≤ 1.05 by policy) | `16_pilot_builds_2026-10-16/tooling/pilotlib.py`, `check_script.py`, `narrate.py` | `check_script` planned duration now matches measured within 1 s for George (61.0 s measured vs 59.65 planned before tempo) |
| Scorecard: `releasable` requires at least one judge verdict | `tooling/scorecard.py` (`judge_verdicts`) | plan finding IP-06 (a) |
| Regression suite tolerant to frame-similarity rounding (±0.025) | `tests/test_regressions.py` | `tests/run_all.sh` |
| A6 creative benchmarks integrated: 8 findings (118 total), framework §4.1 "Pin, Turn, Release" | `audit/A6_*`, `01_VIDEO_AUDIT.md`, framework, skill | `tooling/consolidate_findings.py` |
| Narration clip edges trimmed to the audible voice (alignment stamped the first word at the clip start and the last at its end: 2.6 s of hidden silence over 14 beats); QA A3 compares numbers with their decimals, A13 tolerates ±0.15 s, A16 measures the lane in use, A19 scales with the voice, A20 counts pauses ≥ 0.45 s (PD-23); room tone −66 dBFS | `narrate.py` `voice_edges`, `qa.py` | measured gaps equal planned pauses; `tests/run_all.sh` OK |
| The 60-second method (PD-26, "100 Seconds" profile): `11_SIXTY_SECOND_EXPLAINER_METHOD.md`; the explainer spine is checked as functions (`pilotlib.spine_problems`: purpose first, required functions present, recap → close → brand last) in check_script and qa A18; `check_pd_script.py` warns on M01 (`outcome` missing), M02 (`promise_line` missing or not the hook's first sentence, no task verb in the hook) and M05 (fewer than three beats carrying a link word); script fields `outcome`, `promise_line`, `profile` | `pilotlib.py`, `check_script.py`, `qa.py`, `check_pd_script.py`, `format/script_v2_fields.md`, skill | `tests/run_all.sh` OK; `test_v2.py` OK; the v3 explainer still passes with M-warnings (pre-method) |
| Local preview voice: `narrate_preview.py` voices a script with macOS `say` (offline, free; Rishi for Indian English) and fills the narration cache with the keys `narrate.py` expects, so timeline, mix, cue sheets, render and QA run unchanged without ElevenLabs; word timings are proportional inside each clip's voiced span (preview only). `pace: fast` bands widened to 150–205 words and 150–215 wpm (PD-28a) | `16_pilot_builds_2026-10-16/tooling/narrate_preview.py`, `check_script.py`, `qa.py` | the method short rendered with Rishi at `say -r 170` (175 wpm measured) |
| A15 motion signal (PD-23b): coherent motion in the board and result lanes counts as a change (grey delta > 96/255 on ≥ 0.12 % of lane pixels between samples); calibrated on the preview's current dashes versus the pilots' boil | `qa.py` `frame_series`, `a15_change_density` | preview QA 17 / 3 / 0 / 1; chemistry pilot pin moved from 8.0 s to 7.5 s and still fails |
