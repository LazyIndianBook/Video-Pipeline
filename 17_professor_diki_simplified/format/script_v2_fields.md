# script.json v2 fields (`"schema_version": "script/v2"`, 16 Oct 2026)

The v2 fields extend PILOT_CONTRACT §3; every v1 field keeps its meaning. A script is v2 when either `schema_version` is `"script/v2"` or `script_version` is 2 or higher. Support:

- **Read by:** `16_pilot_builds_2026-10-16/tooling/pilotlib.py` (`is_v2`, `beat_pause`, `plan`, `silence_share`).
- **Validated by:** `check_script.py` (v2 branch) and `skills/professor-diki-script/scripts/check_pd_script.py` (framework rules).
- **Placed by:** `narrate.py`.
- **Example:** `format/sample_v2_script.json`.
- **Regression:** `tooling/test_v2.py`.

## Top level

| Field | Value | Notes |
|---|---|---|
| `schema_version` | `"script/v2"` | `script_version: 2` is accepted too |
| `format` | `"concept_short_60"` | turns on the 120–135 word gate |
| `target_duration_s` | `60` | required for concept_short_60 |
| `duration_tolerance_s` | `1.0` | the default is 1.0, with a warning when missing |
| `scenes` | exactly one | PD-03 |
| `cta_line` | the spoken CTA sentence, supplied per request (PD-14), e.g. `"Try the free lesson on Ohm's law."` | It must be the sentence right before "Professor Diki Simplified.", either as the last `close.next_step` beat or as the first sentence of the outro beat. Empty or null means no CTA (AC0). Without the field, check_script warns and checks the default "Try the free lesson on <topic>." shape. |
| `tail_s` | seconds after the last word (default 0.8) | `outro.tail_s` is read too |
| `outro` | `{beat, spoken, end_card: {brand_line, free_lesson_line, min_on_screen_s}, motif, motif_starts, tail_s}` | `end_card` is copied into the cue sheet as `meta.end_card` |

## Per beat

| Field | Value | Default and checks |
|---|---|---|
| `format` | `concept_short_60` (question format) or `explainer_60` (PD-24, no questions) | Selects the slot spine, the energy peak slots and the dead-time ceiling (15 % / 10 %) |
| `outcome` | one observable outcome (M01, explainer_60) | check_pd_script warns if absent |
| `promise_line` | the first sentence of the hook beat (M02) | check_pd_script warns if it differs from the hook's first sentence |
| `pace` | `fast` (PD-28) or absent | fast: word band 150–185, per-beat band 150–200 wpm, dead time ≤ 8 % |
| `profile` | `pds-60-method-1.0` for the 60-second method | recorded in the cue sheet meta |
| `slot` | one of `pilotlib.RATE_WPM` keys | The first occurrences of hook → `check.predict` → `reveal.answer` → `check.transfer` → `feedback.transfer` → `close.next_step` → `outro.brand` must come in that order |
| `pauses` | `[{"purpose", "after_s"?, "prompt"?, "at"?: "end"}]` | One entry, the gap after the beat's last word. `s` is an alias of `after_s`. When `after_s` is omitted, the PD-01 default applies: join 0.25, land 0.6, inspect 1.0, think_recall 1.5, think_choice 2.0 (`think_choose` is accepted), think_calc 3.0, pause_video 1.0. Values must lie in the PD-01 ranges (±10 %). Required on every beat except the last. |
| `think_window_s` | v1 field | Still read: in v2 it maps to `think_calc` with a warning |
| `energy` | integer 1–5 | `low`/`mid`/`high`/`peak` are accepted as 2/3/4/5. The curve needs ≥ 3 distinct marks, with the peak on a reveal or the transfer |
| `visual_op` | a motion verb, or a list of them | `design_system/tokens.json` `motion.verbs` plus `PreserveObject`; includes `Card` (PD-18: a table row, definition card or points list appearing on its words) and, from design system v2, the collage verbs `Chips`, `Pop`, `Slide`, `Tape` |
| `insight_beat` | `true` on exactly one beat | The first usable idea; planned start ≤ 10 s |
| `target_wpm` | number, optional | Overrides the slot rate in the estimate |
| `check` | `{task_kind, asks, answerable_from[], likely_wrong?}` on `check.predict` / `check.transfer` | `task_kind` must match the pause purpose. Every `answerable_from` fx path must be on screen by the question. |
| `emphasis_words` | list | Copied to `meta.beats_text` |
| `evidence` | node id or fixture path on `misconception.confront` | check_pd_script requires it |
| `on_screen.claim_line` | the quotable aha | One per short, on screen ≥ 1.5 s; its words must be spoken in that beat |
| `on_screen.disclosure` | retired (PD-20): check_script fails any on-screen disclosure; the AI declaration is made at upload | It may instead come from `outro.end_card.disclosure_line` or from fixture `display.ui.disclosure` (in `fx_refs`). It must match the Path A or B pattern in `brand/strings.json`. |
| `text` of `outro.brand` | ends with exactly `Professor Diki Simplified.`, optionally preceded by the `cta_line` | No disclosure anywhere, spoken or on screen (PD-20); no "ExamLeaf" anywhere |

## Cue sheet additions (both versions)

| Field | Content |
|---|---|
| `meta.pauses[]` | `{beat, purpose, seconds, start, end, prompt?}` in scene time. v1 beats report `unlabelled` and `think_calc`. |
| `meta.energy[]` | `{beat, energy (1–5), start, end}` |
| `meta.think_windows[]` | Unchanged for v1. In v2 it holds every `think_*` pause, so old scenes keep working. |
| `meta.beats_text[]` | Also carries `energy`, `visual_op`, `insight_beat`, `emphasis_words`, `claim_line`, `pause` and `think_window`. |

`narration/timeline.json` (v2) keeps `pause_after_s` and `think_window_s` per beat for qa.py, and adds `pause`, `energy` and a video-time `pauses[]` list.
