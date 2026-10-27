# Cue-sheet contract

## 1. Shape

Report §5.5 [Recommendation] defines one canonical cue sheet per scene:

```json
{"scene_id":"phy-10-03-s04","fps":30,"duration":7.4,
 "words":[{"w":"refraction","t0":1.12,"t1":1.71}],
 "beats":[0.0,0.6,1.2],
 "cues":[{"id":"label_n1","at":1.07,"kind":"reveal"}],
 "sfx":[{"file":"pop.wav","at":1.07,"gain_db":-12}]}
```

- The harness copy of the schema is `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`, with `cue_sheet.example.json` beside it. Both are owned by the harness author (`examleaf-motion-harness`). If the harness schema and this document ever disagree, the harness schema wins for field names and this skill is updated.
- This skill emits **only** the fields above, so even a strict schema (`additionalProperties: false`) passes. Provenance lives in sidecars.

## 2. Timing rules

| Rule | Source | Implementation |
|---|---|---|
| Every reveal lands on, or about 0.05 s before, the spoken word it illustrates | [V4-MP] §8 | `at = word_time + offset_s`, default offset −0.05; validator range [−0.10, 0] for reveal, highlight and show |
| One sentence = one visual beat; never everything on screen at once | [V4-MP] §8 | Authoring rule for the spec (one reveal per idea); `examleaf-anim-qa` checks render density |
| Each new sheet starts about 0.3 s after the previous line's last word | [V4-MP] §9 | Transition cue: `anchor.edge = "end"`, `offset_s = +0.3` |
| Duration derives from the narration | Report §5.5 | WAV length (or synchronizer clip) + `tail_s` |
| Frame count = DURATION × fps | [N72] | `frames = ceil((narration_end + tail_s) × fps − 1e-9)`; `duration = frames / fps` |
| Animations read `cues[].at` and never hard-code times | Report §5.5 | Lint concern of `examleaf-motion-harness`; this skill provides the times |
| Answers never appear before their response window ends | `04_NARRATION_SUBPIPELINE.md` §12 ("Premature answer") | `reveal-answer` offset ≥ 0, default 0 |

## 3. Anchors and occurrence

- An anchor is `{phrase, occurrence, edge}`, the same semantics as the narration `Cue` (`cue_id`, `phrase`, `occurrence` ≥ 1, `edge` ∈ start/end).
- `occurrence` is 1-based. "Highlight when the word 'current' is spoken" is ambiguous when it appears four times; "A missing occurrence fails loudly" (`04_NARRATION_SUBPIPELINE.md` §12).
- Edge `start` uses the first matched word's `start`; edge `end` uses the last matched word's `end`.
- **Tokenizer.** NFC, casefold, then runs of Unicode letters (L*), digits (N*) and combining marks (M*), plus ZWJ/ZWNJ and inner apostrophes. Punctuation separates tokens and is dropped. Python's `\w` does not match Indic vowel signs or viramas. Checked on Python 3.14 (15 Oct 2026): `re.findall(r'[^\W_]+', 'विद्युत्')` returns `['व', 'द', 'य', 'त']`, and `'বিদ্যুৎ'` splits into four pieces. The narration comparator `normalized_words` uses that regex, and notes it is "Only an English/surface comparator. Native Indic tokenization requires separate review." Its `cue_time` requires one normalized token per word, so it cannot anchor most Hindi or Assamese words. This skill's tokenizer keeps them whole, and difficult Indic anchors still get a native reviewer's check. **Update (15 Oct 2026):** the narration comparator was fixed at the root (category-based tokenizer in `05_narration_system/narration_system_v1/src/examleaf_narration/pronunciation.py`; `'विद्युत्'` is now one token and `cue_time` anchors Hindi words); this skill's own tokenizer is kept for independence, and both must agree on the Hindi/Assamese test strings in `05_narration_system/narration_system_v1/tests/test_narration.py`. **Update 2 (15 Oct 2026, audit "Two cue-sheet validators"):** the builder's rules now match the comparator exactly: ZWJ/ZWNJ (U+200D/U+200C) are **dropped** inside a word and never split it (earlier they were kept inside the token, so `क्\u200dष` did not equal the comparator's `क्ष`); inner apostrophes are kept only when a letter follows; maths symbols `+ − = ^ < > -` are single tokens. The selftest asserts `tokens('क्\u200dष') == ['क्ष']`.

## 4. Synchronizer precedence

`examleaf-speech-animation-synchronizer` already turns NarrationPlan cues into events at accepted-audio sample positions, converted once to frames:

```text
frame = round_half_up(sample × fps_num / (48,000 × fps_den))
```

(`timeline.frame_at`; `04_NARRATION_SUBPIPELINE.md` §12.)

When a cue ID in the spec also exists as a synchronizer event for the same segment:
1. scene time = `(event.sample − clip.start_sample) / sample_rate`;
2. it is cross-checked against the alignment-derived time; a difference greater than 1/fps means the inputs are stale, and the build blocks;
3. the synchronizer time is used, and `offset_s` is then applied.

Animation-only cues, such as a doodle sparkle on "suddenly", resolve from the alignment directly.

## 5. Beats and SFX

- **Beats** come from `analysis.json` (`examleaf-audio-analysis`):
  - `params.units` must be `"time"` (#33);
  - beats must not exceed `source.duration_s`;
  - `beats.offset_s` places the bed's t = 0 inside the scene;
  - only beats in `[0, duration)` are kept;
  - a `fallback: "narration_grid"` analysis is accepted, because those beats are phrase onsets; `"none"` gives `[]` plus a warning.
- **SFX** come from the spec. They are tied to a cue (`at = cue.at + offset_s`) or absolute, and `gain_db` is required. If `sfx_manifest` is given, files missing from the palette produce a warning. Placement inside `[0, duration)` is validated.

## 5a. Beat snap (Reels)

`"snap": {"kinds": ["transition"], "tol_s": 0.1}` in the spec moves each cue of a listed kind to the nearest beat within the tolerance. SFX tied to that cue move with it, because SFX resolve after snapping. Moves are recorded in `provenance.snapped` (`id`, `from`, `to`).

Kinds `reveal`, `highlight`, `show` and `reveal-answer` are narration-locked: listing them blocks the build, because the sync rule (on, or about 0.05 s before, the word) beats the music. Snapping happens in scene time, before any `--window`, so the alignment survives the shift.

## 6. Provenance sidecar

`cue_sheet.provenance.json` makes the sheet auditable and re-buildable:
- `inputs_sha256`: every input file;
- `alignment_method` and `contains_fixture` (release blocks on true);
- `narration_end_s`, `duration_source` and `frames`;
- `anchors`: per cue, the phrase, occurrence, edge, matched word index, raw word time, and source (`alignment` or `synchronizer`);
- `window` and `dropped_cues` (Reels);
- `warnings`.

Compare `inputs_sha256` with the previous build to decide whether a rebuild, and therefore a re-render, is needed at all.

## 7. Validation

*15 Oct 2026 (audit M7): rewritten.* The only validator is `12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py` (positional sheet path, `--production`, `--json`, tolerance 1e-6). It interprets every keyword the schema uses (including `$ref`, `pattern`, `const`, `maximum`) and refuses to run on a schema keyword it does not implement. The builder imports it by path and runs it on every sheet; the earlier skill-local subset validator (`--sheet`, 1e-3 tolerance, no `pattern`/`$ref`, accepted `alignment_source: "example"`) was deleted.

## 8. Example resolution (from the selftest)

| Word | t0 | t1 |
|---|---|---|
| The | 0.10 | 0.25 |
| current | 0.30 | 0.70 |
| splits; | 0.75 | 1.10 |
| current | 1.30 | 1.70 |
| rejoins | 1.75 | 2.20 |
| विद्युत् | 2.30 | 2.80 |

Each cue resolves as follows:
- `{"phrase": "current", "occurrence": 2}` → 1.30 − 0.05 = **1.25**;
- `{"phrase": "rejoins", "edge": "end"}` with +0.3 → 2.20 + 0.3 = **2.50**;
- `{"phrase": "विद्युत्"}` → 2.30 − 0.05 = **2.25**.

A 3.0 s WAV with `tail_s` 0.3 gives 3.3 s × 30 = **99 frames** (duration 3.3).
