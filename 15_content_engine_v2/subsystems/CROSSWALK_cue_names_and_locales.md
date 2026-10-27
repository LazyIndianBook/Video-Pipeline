# Crosswalk: cue names and locale gaps (Content Engine v2 subsystem)

Status: specification, 15 Oct 2026. Nothing here has run. This document maps two vocabularies that were designed separately and records the locale and pacing gaps found while mapping them. It changes no code. Every code change is a P1 build item (section 5).

**Sources read.**

- 05 = `05_narration_system/INSTRUCTIONS_narration_pipeline.md` §7.1 to §7.2 (the `NarrationPlan` cue `action` enum, `target_wpm`, `VoiceIdentity.locale`), with `narration_system_v1/src/examleaf_narration/contracts.py` and `compiler.py` for the code facts.
- 12 = `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json` and `validate_cue_sheet.py` (the cue `kind` enum and its timing rules).
- 12 cue builder = `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/SKILL.md`, which already maps 05 actions to 12 kinds in its input table.
- v2 = `SCRIPTING_REGISTRY.md` §13 (beat direction tag grammar and cue grammar), `VOICE_and_PERSONA_REGISTRY.md` §2.5 and §6, and `../ARCHITECTURE_content_engine_v2.md` §8 and `../TEMPLATES.md` (Locale Profile `bcp47`).

**Tags.** **[Recommendation]** is a design choice. "verify" means not established in the project documents.

---

## 1. Why two names exist

The Script Spec compiles to the 05 `NarrationPlan`. Inside a segment, `cues[].action` names what the *narration* wants to happen at a spoken phrase: `show`, `highlight`, `transform`, `hide`, `reveal-answer`. The 12 cue sheet is the animation harness's timing file. Its `cues[].kind` names how the *scene code* treats a moment: `reveal`, `emphasis`, `transition`, `hold`, `marker`. The two enums have different sizes and different meanings, so the translation is many-to-one in one direction and partly empty in the other. The 12 cue builder does the translation today; the table below makes it the specification.

## 2. Mapping table (05 action to 12 kind)

| 05 `cues[].action` | 12 `cues[].kind` | What else is written | Timing rule | May a beat snap move it? |
|---|---|---|---|---|
| `show` | `reveal` | `element_id` copied; `word_index` set when `edge` is `start` | `at` = the phrase's first word `t0` plus `offset_s` (default −0.05 s). The 12 validator errors if `at` is after the keyed word's `t0` (never late) and warns if `at` is more than 0.10 s before it (the rule is on, or about 0.05 s before, the word) | No |
| `highlight` | `emphasis` | As `show` | As `show` | No |
| `transform` | `transition` | `element_id` copied; no `word_index`. **The original action is lost** (see 3.1) | `at` from the phrase `t0` (`edge: start`) or last-word `t1` (`edge: end`) plus `offset_s`. No lead check applies to `transition` | Yes, only on Reels, within `tol_s` (default 0.1 s), and only for decorative cues |
| `hide` | `transition` | As `transform`. **The original action is lost** | As `transform` | As `transform` |
| `reveal-answer` | `reveal` | The cue id is also written to `meta.answer_protection[]`; no `word_index` | `offset_s` is 0 and never negative. It must fall after the protected window of the question named by `answers_after` ends (05 §7.2; `compose` raises "Premature answer") | Never (blocked) |

**Reverse direction (12 kind to 05 action).**

| 12 `kind` | Comes from 05 | Comes from elsewhere |
|---|---|---|
| `reveal` | `show`, `reveal-answer` | Scene-authored element entrances keyed to a spoken word |
| `emphasis` | `highlight` | Style-token emphasis beats (a Format Plan `emphasis` word) |
| `transition` | `transform`, `hide` | Decorative transitions the builder or the style adds between scene sheets |
| `hold` | nothing | The builder, from hold rules: a headline hold of at least 1.2 s (longer for Indic text) and an equation hold until narration ends plus 0.5 s (style tokens, 12 A-checks). The cue carries `until`, and only `hold` may carry `until` |
| `marker` | nothing | Free scene markers (chapter or section marks, debugging); no 05 equivalent and no narration meaning |

Window music roles are not cues; the cue builder derives them per MUSIC §2.2 into `meta.music_roles` (15 Oct 2026).

The think and pause-video windows are **not** cues in either vocabulary. In 05 they are `pause_after` on a segment; in 12 they exist only as a gap in the narration timeline (`words[]`) plus, for answers, `meta.answer_protection`. Do not model a protected window as a `hold`.

## 3. Field-level map

| Concept | 05 `Cue` | 12 cue | Note |
|---|---|---|---|
| Identifier | `cue_id` (`^[a-z][a-z0-9_-]*$`) | `id` (`^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$`) | 05's pattern is a subset of 12's, so every 05 id is a valid 12 id |
| What happens | `action` (5 values) | `kind` (5 values) | Section 2 |
| Where in speech | `phrase`, `occurrence` (≥ 1), `edge` (`start` default, `end`) | `at` (seconds), optional `word_index` into `words[]`, optional `occurrence` | The builder resolves `phrase` and `occurrence` against the alignment into `at` and `word_index`. 12's `occurrence` means "this id fires more than once", which is a different thing from 05's phrase occurrence |
| Target | `element_id` | `element_id` | Same name and meaning |
| Offset | none in 05 | `offset_s` is a builder input; the sheet stores only the result in `at` | Default −0.05 s |
| Answer protection | `answers_after` on the *segment* | `meta.answer_protection[{cue_id}]` | The 12 schema has no "answer" kind, so protection is metadata, and `safe_zone_check.py --cues` in the anim-qa skill reads it |
| Language of a word | none | `words[].lang` for code-switched words | 05 locale is plan-level only |

### 3.1 Information lost by the mapping **[Recommendation]**

`transform` and `hide` both become `transition`, so scene code cannot tell an element that changes from one that leaves. The 05 action should survive in `meta` (for example `meta.cue_actions[cue_id] = "hide"`) so that QA, the scene author and a future 12 schema revision can use it. The sheet is hash-bound and `meta` is not read by scene code, so this costs nothing at render time. P1 item P1-CW-1.

### 3.2 What the v2 Script Spec does

`script_spec.schema.json` keeps the **05 vocabulary** on purpose (`show | highlight | transform | hide | reveal-answer`), because the Script Spec compiles to the 05 `NarrationPlan` and the 05 enum is what the narration validator enforces. The v2 Script Spec never names a 12 kind. The 05-to-12 step stays in the cue builder. If the vocabularies are ever merged, the 12 side moves, because it has the fewer constraints on meaning.

### 3.3 Two occurrence rules (16 Oct 2026, pilot gap L-04)

Phrase occurrences are counted two ways. The **05 narration comparator** matches words after Unicode NFC normalisation and casefolding, so "Four" and "four" are the same word and share one count. The **12 cue-sheet validator** checks `words[].occurrence` on the exact surface form: identical spellings (case and marks included) are numbered 1..n in spoken order, and "Four" and "four" are separate sequences. The cue-sheet builder therefore numbers occurrences **per exact surface form** when it writes `words[]`; a phrase anchor resolved with the comparator's rule must be re-indexed to the surface-form count before it is written to the sheet. The pilot hit this as a validator error on "four"/"Four" (`16_pilot_builds_2026-10-16/COMPARISON_and_GAPS.md` §1 L-04).

## 4. Locale gaps

### 4.1 Hinglish is missing from 05's locale list

- 05 `VoiceIdentity.locale` is `Literal["en-IN", "hi-IN", "as-IN"]` (`contracts.py` line 13), and `compiler.LANGUAGES` lists the same three per provider-model pair. A plan for Hinglish therefore cannot be built, although Hinglish is a launch locale (CE-L5) and its own registry entry (`locale/hinglish`, RD-42).
- The v2 locale registry has four ids. A mapping is needed between them and the BCP-47 tags the cue sheet and 05 use.

| v2 `locale/` id | BCP-47 tag | In 05 `VoiceIdentity.locale` today | In 12 `language` pattern |
|---|---|---|---|
| `locale/en-in` | `en-IN` | Yes | Yes |
| `locale/hi-in` | `hi-IN` | Yes | Yes |
| `locale/hinglish` | `hi-Latn-IN` (the tag already in `TEMPLATES.md` for the Locale Profile) | **No** | Yes (`^[a-z]{2,3}(-[A-Za-z0-9]{2,8})*$` accepts it) |
| `locale/as-in` | `as-IN` | Yes (human voice only, RD-42, no TTS or STS) | Yes |

**[Recommendation]** Add `hi-Latn-IN` to the 05 `VoiceIdentity.locale` enum and to every `compiler.LANGUAGES` set whose provider documents Hindi, only after the provider's Hinglish behaviour has a recorded GL-voice pass (CE-41); until then a Hinglish request resolves to Path A (R1). The provider matrix in `VOICE_and_PERSONA_REGISTRY.md` §3.5 is the place to record which pairs are admitted. P1 item P1-CW-2.

### 4.2 `target_wpm` is required but undefined for some levels and locales

05 `Segment.direction.target_wpm` is an integer 80 to 185 with **default 140** (`contracts.py` line 20). The v2 Script Spec requires `target_wpm` too, but it can be `null` when the band is `teacher_set`. The Level Profile and Voice registry give a number for only some cells:

| Cell | Level Profile value | Result in the Script Spec | Risk when compiled to 05 |
|---|---|---|---|
| l1_2, l3_5 | calibrate (child-development reviewer; no adult WPM imported) | `wpm_band: teacher_set`, `target_wpm: null` | 05 has no null. If the field is omitted, 05 **silently applies 140 wpm**, an adult English rate, to child content |
| voc | calibrate (trade instructor) | As above | As above |
| educator | not set in the Level Profile | No band defined | A gap in the Level Profile, not only in 05 |
| hi-IN, Hinglish, as-IN (any level) | No wpm values: rates are not transferred across languages | Band needs a locale measurement | The 05 default 140 is an English figure applied to another language |

**[Recommendation]** Make the 05 field explicitly unset-able (`target_wpm: null` or a `teacher_set` marker accepted by the schema and the compiler, with no default), and make the compiler refuse to fall back to 140. Where the band is `teacher_set`, the Path A performer's pace is the pace, and an overrun against the format's length budget is a compile error (R5), never a speed-up. The Level Profile for educator needs a value or an explicit `teacher_set`. Locale bands are measured by the native-language editor in the first GL-voice run or Path A pilot [Hypothesis, owner native-language editor]. P1 items P1-CW-3 and P1-CW-4.

## 5. P1 build items from this crosswalk (levels per Roadmap §7)

| ID | Item | Where |
|---|---|---|
| P1-CW-1 | Preserve the 05 cue `action` in the 12 sheet (`meta.cue_actions`) so `transform` and `hide` stay distinguishable; add a test to the cue builder selftest | `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/scripts/build_cue_sheet.py` |
| P1-CW-2 | Add `hi-Latn-IN` to `VoiceIdentity.locale` and `compiler.LANGUAGES` (gated by GL-voice per provider and model); keep Assamese on the human route | `05_narration_system/narration_system_v1/src/examleaf_narration/contracts.py`, `compiler.py`, `configs/narration.schema.json` |
| P1-CW-3 | Allow an unset `target_wpm` (`teacher_set`) in the 05 contract; remove the 140 default; a plan with neither a number nor `teacher_set` fails validation | same `contracts.py` and schema |
| P1-CW-4 | Give `level/educator` a pacing value or an explicit `teacher_set`; record locale bands for hi-IN, Hinglish and as-IN after the first native measurement | `../LEVEL_PROFILES.md`, Locale Profiles |
| P1-CW-5 | Add a registry test that every action in the Script Spec `cues[].action` enum maps to one 12 kind through this table, and that no 12 kind other than `hold` and `marker` is unreachable | `ci/` schema step (Roadmap level 1) |

## 6. Negative tests

| # | Input | Expected result |
|---|---|---|
| CW-N1 | Script cue with `action: pulse` | Script Spec schema rejects it (not in the 05 enum) |
| CW-N2 | A `reveal-answer` cue placed inside its question's `think` window | Narration validator and cue builder block it (Premature answer) |
| CW-N3 | `hide` cue built to a sheet and then read back as a `reveal` | The test in P1-CW-5 fails; `hide` maps to `transition` |
| CW-N4 | A Hinglish `NarrationPlan` with `locale: hi-Latn-IN` before P1-CW-2 | Rejected by the 05 `Literal`; documented gap, not a pass |
| CW-N5 | l3_5 segment with `target_wpm` omitted | Today: accepted with 140 (the defect). After P1-CW-3: rejected |
| CW-N6 | A `hold` cue with no `until` | The 12 validator warns; the builder must always set `until` |
