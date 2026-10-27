# Templates

Fill-in templates. Each must validate against its schema in `schemas/` (Content Request, Format Spec, Level Profile, Subject Validation Profile, Locale Profile, Curriculum Framework, Learning Signal; the last two added 15 Oct 2026). The Locale Profile validates against schemas/locale_profile.schema.json (added 15 Oct 2026). Replace `<…>` placeholders. Tagged numbers in Level Profiles (and in Locale Profile pacing) are multiples of 0.5 (schema, 15 Oct 2026). Delete optional lines you do not use; never add fields that are not in the schema (additionalProperties is false everywhere). No commercial fields.

## 1. Format Spec (`content/registry/format/<id>.yaml`)

```yaml
format_id: format/<snake_case_id>
version: 1.0.0
title: <Human title>
purpose: <one sentence: what this artefact does>
learner_outcome: <what the learner can do afterwards>
kind: <primary | derived | composition>
select:
  root: <objective_set | assessment_item | misconception | worked_item | claim | claim_pair | activity | story | text_passage | member_artefacts>
  include:
    - <selector, e.g. CLM[key=true]>
    - <selector, e.g. MIS[priority<=2]>
node_requirements_by_level:            # optional; level-conditional requirements
  - levels: [<level/l6_8>, <level/l9_10>]
    requirements:
      - {node_type: <WRK>, per: <objective>, min: <1>}
  - levels: [<level/l1_2>, <level/l3_5>]
    requirements:
      - {node_type: <ACT>, per: objective, min: 1, any_of: [ACT, STY]}
grammar:                               # registered slot types only
  - {slot: <hook.realworld>}
  - {slot: <explain.ladder_step>, repeat: <per_objective>}
  - {slot: <check.interpolated>}
level_variants:                        # optional
  - variant_id: <gentle>
    levels: [<level/l1_2>, <level/l3_5>]
    grammar:
      - {slot: <hook.surprise>}
    duration_s: {min: <n>, max: <n>, tag: Hypothesis, source: <pilot ref>}
    notes: <why this variant>
format_variants:                       # optional (15 Oct 2026); content variants with their own root, e.g. short.misconception
  - variant_id: <format.variant>
    select: {root: <misconception>, include: [<selector>]}
    grammar:
      - {slot: <misconception.elicit>}
    duration_s: {min: <n>, max: <n>, tag: <...>}   # optional
duration_s: {min: <n>, max: <n>, tag: <Hypothesis|Recommendation|Evidence|Inherited>, source: <ref>}   # omit for kind: composition
max_segment_s: <≤360>
aspect: <9x16 | 16x9>                  # 16x9 only for level/ug, level/pg, level/adult_prof; omit for kind: composition
resolution: <1080x1920 | 1920x1080>   # omit for kind: composition
voice_path_default: <A | B>            # R1 may force A
render_targets: [video]                # add audio_only only if every visual-essential scene is narrated
interaction:
  interpolated_checks: <required | optional | forbidden>
  check_answer_hidden: true
  think_window_protected: true
levels_allowed: [<level/...>]
families_allowed: [<family/...>]
overlays_allowed: [<overlay/...>]      # optional
styles_allowed: [<style/...>]
style_defaults:                        # required (15 Oct 2026): one default style per level; levels disjoint, union = levels_allowed (VISUAL_STYLE §4.1 step 7, §4.2)
  - {levels: [<level/...>], style: <style/...>}
gates: [GA_DELTA, H_SB, A_SUITE, <GF | GS>, DISCLOSURE, RELEASE_CHECK, VOICE]   # primary adds GA_GRAPH
qa_checks: [<q-closure>, <q-fix>, <...>]
derivation:
  may_introduce_node_types: []          # must be empty for derived
  parent_formats: [<format/...>]        # optional
composition:                            # only for kind: composition
  member_formats: [<format/...>]
  ordering: <curriculum | difficulty | paper_order | explicit>
  single_file: <true | false>
  members_must_be_approved: true
evidence:
  - {claim: <statement>, tag: <Evidence|Hypothesis|Recommendation>, source: <N# or section ref>}
```

Checklist before GR: linter green on golden graphs for every allowed level; level `formats_allowed` updated to match; one golden render; owner named.

## 2. Level Profile (`content/registry/level/<id>.yaml`)

```yaml
level_id: level/<id>
version: 1.0.0
title: <Classes x–y / band name>
band: {grades: "<x-y>", stage_ref: <foundational|preparatory|middle|secondary|higher_secondary|undergraduate|postgraduate|adult|vocational>, stage_source: <N# or framework id>}
safety_class: safety/<ac0|ac1|ac2>   # fixed by level_id (schema, 15 Oct 2026): l1_2, l3_5 → ac0; l6_8, l9_10, l11_12, ug, voc → ac1; pg, adult_prof, educator → ac2
persona: persona/<id>#<variant>   # e.g. persona/super-teacher-junior#coach (CE-64; pin form persona/<id>@x.y.z#<variant>)
accessibility: a11y/base
voice_path_floor: <A | either>         # ac0 ⇒ A (schema)
attention:
  max_segment_s: {value: <n|null>, unit: s, tag: <...>, source: <...>, owner: <if Hypothesis>, pilot_ref: <if Hypothesis>}
  max_new_ideas_per_segment: {value: <n|null>, tag: <...>, owner: <...>, pilot_ref: <...>}
  max_artefact_s: {value: <n|null>, unit: s, tag: <...>, source: <...>}   # optional (15 Oct 2026); omit = no level ceiling (R5)
pacing:
  wpm_ordinary: {min: <n|null>, max: <n|null>, unit: wpm, tag: <...>, source: <...>, owner: <...>, pilot_ref: <...>}
  wpm_dense: {min: <...>, max: <...>, tag: <...>}
  wpm_recap: {min: <n|null>, max: <n|null>, unit: wpm, tag: <...>, source: <...>, owner: <...>, pilot_ref: <...>}   # required (15 Oct 2026); Cal levels: min/max null, tag Hypothesis, owner and pilot_ref
  think_window_s: {min: <≥4>, max: <...>, tag: <...>}    # min ≥ 4 s (schema); 4 s only for a binary choice
language:
  lexicon_ref: <lex/level-locale>
  max_sentence_words: {value: <...>, tag: <...>}
  max_new_terms_per_scene: {value: <...>, tag: <...>}
  on_screen_text: <icons_and_single_words|short_phrases|sentences|dense_notation>
  notation: <none|basic|standard|advanced>
  single_language_per_lesson: <true|false>
interaction:
  cadence_s: {min: <...>, max: <...>, tag: <...>}
  allowed_types: [<call_response>, <predict>, <...>]
  response_modes: [<think|say_aloud|point|move|draw|write|sing|solve|critique>]
on_screen:
  max_text_elements: {value: <...>, tag: <...>}
  min_type_px: {value: <...>, tag: Inherited, source: "02 tokens"}
  caption_policy: <access_only|standard|short_lines>
  hold_level_multiplier: {value: <n|null>, tag: <Recommendation|Hypothesis|Inherited|Evidence>, owner: <if Hypothesis>, pilot_ref: <if Hypothesis>}   # m_level for A5 holds; Hypothesis for l1_2–l6_8 (CE-62); added 15 Oct 2026
motion:
  flash_policy: <wcag_2_3_1 | ac0_zero_flash>   # ac0 ⇒ ac0_zero_flash (schema)
  reduced_motion_variant: true
  max_visual_change_rate: {value: <...>, tag: <...>}      # optional
assessment_orientation: <play_and_talk|recall_and_reasoning|reasoning|exam_reasoning|critique>
required_reviewers: [<academic_subject>, <family_qualified>, <child_development if ac0>]
formats_allowed: [<format/...>]
exam_overlays_allowed: [<overlay/...>]
evidence:
  - {field: <path>, tag: <...>, source: <N#|section|pilot>}
```

## 3. Subject Validation Profile (`content/registry/family/<id>.yaml`)

```yaml
family_id: family/<id>
version: 1.0.0
title: <Family name>
subjects: [<subject_id>, <...>]          # each subject in exactly one family
levels_allowed: [<level/...>]            # required (15 Oct 2026); R3 refuses other levels
subject_locales: {<subject_id>: <locale/...>}   # required for family/languages_literature (R9a)
risk_class: <standard | high>             # high ⇒ ≥2 sources routine + disclaimers (schema)
validation_mode: <fixture | claim_ledger | executable | hybrid>
validators: [<fixture_exec|claim_flagger|span_hash|source_policy|...>]
claim_types_allowed: [<definition|quantitative|historical_event|...>]
source_policy:
  min_sources_routine: <1|2>
  min_sources_exceptional: <≥2>
  min_sources_sensitive: <≥2>
  reliability_classes_allowed: [<board_textbook>, <peer_reviewed>, <...>]
  primary_authority: <e.g. board textbook at school levels>
  wiki_citable: false
  self_published_about_living: false
  reject_for_cost_of_access: false
reviewer_roles:
  - {role: <family_qualified>, qualification: <e.g. PG in history>, count: <1>, applies_to: <all>}
  - {role: <sensitivity>, qualification: <...>, count: 1, applies_to: sensitive}
contested_policy:
  statuses_allowed: [settled, attributed, contested, board_vs_scholarship]
  contested_min_reviewers: 2
  short_must_attribute: true
  perspectives_required_at_levels: [<level/...>]   # may be empty; replaces perspectives_format_required (15 Oct 2026)
time_bound_policy:
  claim_types: [<legal_rule|rate_or_threshold|...>]
  default_review_interval_days: <n>        # optional; Hypothesis until piloted
  tag: <Hypothesis|Recommendation>
sensitivity_checks: [<religion>, <caste>, <...>]   # optional
disclaimers: [<"not medical advice">]              # required if risk_class high
executable_policy:                                  # required if executable mode or sandbox validator
  sandbox: no_network_readonly_fs_cpu_mem_time_capped
  runtime_pins: [<python@3.12.x>, <...>]
activation:
  activated: <false until named reviewers exist>
  named_reviewer_ids: [<reviewer/...>]              # ≥1 required when activated
```

## 4. Content Request (`content/requests/CR-<id>.json`)

```json
{
  "request_id": "CR-<id>",
  "competency_guids": ["<guid>"],
  "objective_ids": ["OBJ-<id>"],
  "format": "format/<id>",
  "variant": "<format.variant>",
  "root_node_ids": ["<MIS|CLM|WRK|ASM|ACT|STY|TXT>-<id>"],
  "level": "level/<id>",
  "taught_level": "level/<id>",
  "subject": "<subject_id>",
  "locale": "locale/<id>",
  "exam_overlay": "overlay/<id>",
  "style": "style/<id>",
  "packaging_profiles": ["packaging/<id>"],
  "series": {"series_id": "SER-<id>", "series_position": "<first|subsequent|standalone>"},
  "flagship": {"value": false},
  "demo_kind": "<real|virtual|none>",
  "render_target": "<video|audio_only|print>",
  "requested_by": "<reviewer or founder id>",
  "created_at": "<ISO 8601 date-time>"
}
```

Notes: omit `exam_overlay`, `style`, `objective_ids`, `render_target`, `packaging_profiles` (the format defaults apply, R14), `variant` and `root_node_ids` (required only where R4 says so) when unused; include `taught_level` only, and always, with `level/educator`; omit `series_id` only for standalone. `flagship.value: true` requires `set_by` (academic lead) and `reason`. Never include a subject family: the Resolver derives it (R3). ~~Versions may be pinned with `@x.y.z`; otherwise the latest released version is pinned in the EPP.~~ Versions may be pinned with `@x.y.z` only to reproduce a past build; release always uses the current version (Architecture §3.6 Re-resolution; corrected 15 Oct 2026).

**render_target print (level-3+, CE-119, 15 Oct 2026).** `print` yields a tagged PDF/UA plus HTML from the same Format Plan via the pinned Chrome print path. Use it only with a print configuration (F-W Worksheet on `format/practice_set`, F-TN Teacher Notes on `format/teacher_explainer`, F-GN Guardian Note (AC0) on `format/recap`, Revision Sheet print on `format/revision_sheet`) and with `packaging/print-pdf`. Omit `style` if the format default applies; no voice path, duration, aspect or resolution is resolved for print (EPP schema, 15 Oct 2026). Example that validates against `schemas/content_request.schema.json`:

```json
{
  "request_id": "CR-print-0001",
  "competency_guids": ["719e5255-6dd6-5dcc-8d39-8556e73afa31"],
  "format": "format/practice_set",
  "level": "level/l9_10",
  "subject": "science",
  "locale": "locale/en-in",
  "packaging_profiles": ["packaging/print-pdf"],
  "series": {"series_position": "standalone"},
  "flagship": {"value": false},
  "demo_kind": "none",
  "render_target": "print",
  "requested_by": "reviewer/academic-lead",
  "created_at": "2026-10-15T10:00:00+05:30"
}
```

## 5. Locale Profile (`content/registry/locale/<id>.yaml`)

```yaml
locale_id: locale/<id>                   # lowercase, e.g. locale/hi-in, locale/hinglish, locale/as-in
version: 1.0.0
bcp47: <hi-IN | hi-Latn-IN | as-IN | ur-IN>
script: <Latn | Deva | Beng | Arab>
text_direction: <ltr | rtl>
font_stack: [<Noto Sans Devanagari>, <...>]        # vendored in the container
shaping_engine: {name: harfbuzz, version_ref: harness/<id>@<ver>}
numerals: <latn | deva | beng | arab>
spoken_math_policy: <ref to policy file: how symbols, units and notation are spoken; display/spoken split per RD-29>
transliteration_table: <ref, versioned; reference standard ISO 15919 once registered>
code_mix_policy:                          # per level (15 Oct 2026)
  <level/id>: {pattern: <none | pattern id>, terms_kept_ref: <optional>, approved_by: <reviewer/...; required when the level has single_language_per_lesson: true and pattern ≠ none>}
caption_line_rules: {max_chars_per_line: <n|calibrate>, max_lines: <n>}
pacing_by_level:                          # optional (15 Oct 2026; CE-40); absent = Script Specs use teacher_set for every beat
  <level/id>: {ordinary: {min: <n|null>, max: <n|null>, unit: wpm, tag: <...>}, dense: {...}, recap: {...}, owner: <reviewer/native subject editor>}
readability_method: <controlled_vocabulary_lists>   # not ported English formulas
lexicon_ref: <lex/core.<locale>>                  # pronunciation lexicon in the lex/ registry (05)
glossaries:
  <family/stem_fixture>: {ref: <glossary id>, gl_glossary_passed: <true|false>, approved_by: <reviewer id>}
voices:
  - {voice_ref: voice/<id>, path: <A|B>, gl_voice_passed: <true|false>, gl_voice_record: <ledger ref>}
locale_gate_status: <passed | pending>             # 07/04 §18
tts_admitted: <true only if ≥1 Path B voice has gl_voice_passed>
native_reviewer_ids: [<reviewer/...>]
disclosure_text_ref: <per locale and voice; RD-45>
```

Rules: `tts_admitted: false` makes R1 force Path A for every artefact in this locale. An RTL locale requires an rtl layout test in Q-LOCALE before first use. Changing the lexicon or glossary is a locale/narration-class change; changing fonts, direction or shaping is presentational.

## 6. Curriculum Framework (`content/curriculum/<id>.json`, pinned as `framework/<id>@x.y.z`)

Added 15 Oct 2026 (level-1, CE-111; P1-14). Validates against `schemas/curriculum_framework.schema.json`. Written by `examleaf-curriculum-ingest` (syllabus PDF → candidate items with spans) or hand-authored (M1 step 1), then approved at **H-CG**. `framework_id` and `human_code` are edition-independent: `guid = UUIDv5(UUIDv5(NS_URL, framework_id), human_code)`, so re-ingesting returns the same GUIDs. Never hand-type a GUID; compute it.

```json
{
  "framework_id": "framework/<board>_<stage_or_exam>_<subject>",
  "version": "1.0.0",
  "hash_canon": "JCS-RFC8785+NFC",
  "board": "<board id, lowercase>",
  "edition": "<edition as printed on the syllabus>",
  "stage": "<foundational|preparatory|middle|secondary|higher_secondary|undergraduate|postgraduate|adult|vocational>",
  "subject": "<subject_id>",
  "medium_locale": "locale/<id>",
  "valid_academic_years": ["<YYYY-YY>"],
  "exam_windows": [{"name": "<exam name>", "start": "<YYYY-MM-DD>", "end": "<YYYY-MM-DD>"}],
  "source_refs": [{"source_id": "SRC-<id>", "locator": "<page/section>", "span_sha256": "<sha256>"}],
  "ingestion": {"method": "<examleaf-curriculum-ingest|hand_authored>", "run_ref": "<ingest run id; required for the skill>", "authored_by": "<reviewer/...; required for hand_authored>"},
  "items": [
    {
      "guid": "<UUIDv5 per the rule above>",
      "human_code": "<edition-independent code>",
      "kind": "<competency|learning_outcome|topic>",
      "statement": "<item text>",
      "parent_guid": "<guid; omit at the root>",
      "associations": [{"type": "<prerequisite_of|crosswalk_equivalent|assessed_by_blueprint|non_evaluative>", "target_guid": "<guid>"}],
      "dok": "<only when the framework publishes a depth rubric>",
      "source_span": {"source_id": "SRC-<id>", "locator": "<page/line>", "span_sha256": "<sha256>"}
    }
  ]
}
```

Rules: every SRC in `source_refs` and `source_span` has `reliability_class: official_curriculum`. `exam_windows` (level-3+, CE-122) drive the GR freeze. `valid_academic_years` (level-2, CE-116) keeps artefacts releasable for every edition still inside its window. Change class follows the §3.6 framework diff: removed items and depth changes are Truth-class, text edits Metadata.

Example (illustrative codes, statements, ids and hashes; not a real board record):

```json
{
  "framework_id": "framework/seba_hslc_science",
  "version": "1.0.0",
  "hash_canon": "JCS-RFC8785+NFC",
  "board": "seba",
  "edition": "example edition",
  "stage": "secondary",
  "subject": "science",
  "medium_locale": "locale/en-in",
  "valid_academic_years": ["2026-27"],
  "exam_windows": [{"name": "HSLC final examination (example)", "start": "2027-02-15", "end": "2027-03-10"}],
  "source_refs": [{"source_id": "SRC-example-syllabus", "locator": "Unit 3", "span_sha256": "757ef26c02837edcda3a07557bab5c0ccf2cc085a6bc7a5657d91831aab71d8c"}],
  "ingestion": {"method": "hand_authored", "authored_by": "reviewer/academic-lead"},
  "items": [
    {
      "guid": "6caf5343-1f7e-53eb-8268-d166593c8deb",
      "human_code": "SCI10.EL",
      "kind": "topic",
      "statement": "Electricity",
      "source_span": {"source_id": "SRC-example-syllabus", "locator": "Unit 3, heading", "span_sha256": "ec4393cbc1f14db8f89edbd964138a096e3b907c3204b5269734744236d06566"}
    },
    {
      "guid": "719e5255-6dd6-5dcc-8d39-8556e73afa31",
      "human_code": "SCI10.EL.1",
      "kind": "learning_outcome",
      "statement": "Explains electric current as the rate of flow of charge.",
      "parent_guid": "6caf5343-1f7e-53eb-8268-d166593c8deb",
      "associations": [{"type": "prerequisite_of", "target_guid": "6eefa07c-bba5-5bd2-9860-4baf5675af44"}],
      "source_span": {"source_id": "SRC-example-syllabus", "locator": "Unit 3, line 2", "span_sha256": "033ffadc07845a1626956a287f3386c2a7a1912e596080bbbc2939e57eef8bf2"}
    },
    {
      "guid": "6eefa07c-bba5-5bd2-9860-4baf5675af44",
      "human_code": "SCI10.EL.2",
      "kind": "learning_outcome",
      "statement": "Relates potential difference, current and resistance in a simple circuit.",
      "parent_guid": "6caf5343-1f7e-53eb-8268-d166593c8deb",
      "source_span": {"source_id": "SRC-example-syllabus", "locator": "Unit 3, line 3", "span_sha256": "916ab494ff26ae4bbbbc9348f2aa45f3cbec0646ac0cc8f43f76a079cccf5454"}
    }
  ]
}
```

## 7. Learning Signal (platform intake record; aggregate only)

Added 15 Oct 2026 (CE-117: interface level-2, operation level-3+; Architecture §9.7). Validates against `schemas/learning_signal.schema.json`. One record per aggregate cell. **No learner identifiers of any kind**; the schema is closed. Intake rejects a record whose `cohort_size` is below `min_cohort_size`; the minimum is set by counsel under O-3 and is stricter for `safety/ac0` and `safety/ac1`. A signal never edits the graph: it opens a proposal through S4 and GA-Graph and writes a `signal_proposal` ledger row.

```json
{
  "signal_id": "LS-<id>",
  "signal_kind": "<option_selection|misconception_selection|cue_rewatch|doubt_cluster>",
  "artefact_sha256": "<sha256 from the sidecar>",
  "window": {"start": "<YYYY-MM-DD>", "end": "<YYYY-MM-DD>"},
  "cohort_level": "level/<id>",
  "safety_class": "safety/<ac0|ac1|ac2>",
  "cohort_size": <n>,
  "min_cohort_size": <n from the O-3 policy>,
  "min_cohort_policy_ref": "<O-3 policy ref>",
  "asm_id": "ASM-<id>",                       // option_selection, misconception_selection
  "option_id": "<A-H>",                       // option_selection
  "misconception_id": "MIS-<id>",             // misconception_selection
  "attempts": <n>,                            // option_selection, misconception_selection
  "selection_share": "<decimal string 0-1>",  // option_selection, misconception_selection
  "cue_id": "<cue id from the sidecar>",      // cue_rewatch
  "rewatch_share": "<decimal string 0-1>",    // cue_rewatch
  "doubt_cluster_text": "<platform paraphrase, never a quote>"   // doubt_cluster
}
```

Delete the comment markers and the lines that do not apply to `signal_kind`. Shares are decimal strings (hash canon). Example (illustrative values; the cohort minimum shown is a placeholder until O-3 sets it):

```json
{
  "signal_id": "LS-example-0001",
  "signal_kind": "option_selection",
  "artefact_sha256": "2e542184db06ebc18d67b9af610f08067f8bb1de6069bd5d6338c00b05b6a58b",
  "window": {"start": "2026-11-01", "end": "2026-11-30"},
  "cohort_level": "level/l9_10",
  "safety_class": "safety/ac1",
  "cohort_size": 240,
  "min_cohort_size": 100,
  "min_cohort_policy_ref": "O-3 placeholder (to be set by counsel)",
  "asm_id": "ASM-el-current-01",
  "option_id": "B",
  "attempts": 240,
  "selection_share": "0.38"
}
```
