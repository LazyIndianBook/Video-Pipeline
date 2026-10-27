# Subsystems: the eight registries of Content Engine v2

Dated 15 Oct 2026. This folder holds the subsystem specifications that sit under `../ARCHITECTURE_content_engine_v2.md`. They are specifications, not builds: nothing here has run, no platform figure has been measured, and every number is either inherited from sections 02 to 13, tagged **[Hypothesis]** with an owner and a pilot, or marked "calibrate". Tags used throughout: **[Recommendation]** (a design choice), **[Hypothesis]** (needs a pilot), "verify" (not in the verified evidence).

## 1. What each registry is

| Registry document | What it specifies | Registry kind or record | Stage | Machine contract | Template |
|---|---|---|---|---|---|
| `SCRIPTING_REGISTRY.md` | The Script Spec: sentence-level, hashed script per artefact; slot sources, word budgets, level and persona register rules, locale and family phrasing, beat direction tags, sentence-to-node closure, scripting cascade (Kit, Haiku, Sonnet, Opus, human) | Per-artefact record (`content/scripts/`) | S6, checked S7, GA-Δ | `script_spec.schema.json` | `script_spec.template.md` |
| `INTERACTION_and_ASSESSMENT_REGISTRY.md` | The Interaction Spec: interaction types, think windows, feedback forms, item kinds and per-family answer keys, AC0 rules, neutral sidecar for the platform | Per-artefact record | S5 to S7, S14 | `interaction_spec.schema.json` | `interaction_spec.template.md` |
| `VOICE_and_PERSONA_REGISTRY.md` | Personas (five ids with variants), voices (Path A and B, speech-to-speech rules, consent, providers), pronunciation lexicons, the native-speaker gate, disclosure variants | `persona/`, `voice/`, `lex/`, `gs/` | S5 (voice selection, R13) to S9, GL-voice, DISCLOSURE | `persona.schema.json`, `voice_asset.schema.json`, `lex_entry.schema.json`, `golden_set.schema.json` (last two added 15 Oct 2026) | `persona.template.md`, `voice_asset.template.md` |
| `MUSIC_and_SOUND_REGISTRY.md` | Sonic logo, stings, beds, SFX and song backings; owned audio only; placement by format; mix and ducking; licensing ledger; AC0 audio | `music/` | Selection S5 (EPP pins); placement S10 (cue sheet) | `music_entry.schema.json` | `music_entry.template.md` |
| `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` | Style entries: tokens, motion, holds, flash policy, safe zones, science layer (Rule 0), AC0 limits, 16:9 gating | `style/` | R4, S5, S10 | `style_entry.schema.json` | `style_entry.template.md` |
| `PACKAGING_and_DISTRIBUTION_REGISTRY.md` | Render targets, platform profiles, titles, covers, descriptions, captions and transcripts, the neutral metadata sidecar, disclosure placements, kids' and series packaging, export QA | `packaging/` | S14, after RELEASE-CHECK | `packaging_profile.schema.json` (sidecar is `#/definitions/metadata_sidecar`) | `packaging_profile.template.md` |
| `QA_PROFILES_REGISTRY.md` | The check catalogue and the QA Profile computed from the EPP: severity, enforcement, owners, applicability per format, level, family, locale, safety class and voice path | `qa/` | S7, S11 to S13 | `qa_profile.schema.json` | `qa_profile.template.md` |
| `SKILLS_and_KIT_MAP_v2.md` + `skills_map_v2.csv` | Every skill (72 existing, 19 new) mapped to status (reuse, extend, dormant, retire, new), stage and registry owner; Kit cells, archetypes, cascade and ownership | Map, not a kind | all | none | none |
| `CROSSWALK_cue_names_and_locales.md` | The mapping between 05 narration cue actions and 12 cue-sheet kinds, and the locale and pacing gaps | Mapping | S6 to S10 | none | none |

## 2. How they resolve into the Effective Production Profile

The Resolver is a pure function, `resolve(request, registry_snapshot, graph) → EPP`, with the rules R1 to R12 of Architecture §3.4 (plus R9a, R13 voice entry and R14 packaging, added 15 Oct 2026; evaluation order R2, R3, R1, R4 … R12, R13, R14). The EPP pins every registry entry as `entry@version: sha256`, and `epp_hash = sha256(JCS(NFC(EPP)))`. Every approval binds to that hash. What each registry contributes, in the order the Resolver applies it:

1. **Safety class (R2), taken from the Level Profile only.** `safety/ac0`, `ac1`, `ac2`. Nothing else can change it, and every subsystem treats it as the strongest constraint.
2. **Subject family (R3), derived from the subject.** Selects validators, reviewers and the family phrasing and answer-key rules in the Scripting and Interaction registries.
3. **Voice path (R1).** Path A or B. Voice selection (VOICE §1) then picks an admitted `voice/` entry for the locale and persona. No candidate is a compile error, never a substitute. Selection runs inside profile-resolver at S5, so the voice pin is in the EPP before epp_hash is computed.
4. **Compatibility (R4).** The style must support the format's aspect and the safety class; the format and level must list each other.
5. **Duration (R5).** The intersection of the format duration and the level ceiling; an empty intersection is a compile error. Word budgets in the Scripting registry derive from it.
6. **Validators (R6) and gates (R7).** Unions. The QA registry expands them into the QA Profile with `qa_resolve(EPP, qa/catalogue@x.y.z)`. A gate is never removed.
7. ~~**Scalar precedence (R8): safety class > level > overlay > format > style > persona.**~~ **R8 Scalar resolution. (a) A limit is any field its schema marks `"x-kind": "limit"` (maxima such as max_segment_s, flash, motion, bed level and duration ceilings; minima such as hold times, contrast and think windows). A limit takes the most restrictive value across safety class, a11y profile, level, overlay, format, locale and style. A lower entry may tighten a limit but never loosen it. (b) Every other scalar takes the value of the highest entry in the order safety class > a11y profile > level > overlay > format > locale > style > persona. (c) Locale sets only surface fields (R9); persona sets no number (CE-16). Provenance records which entry set or tightened each value.** (Corrected 15 Oct 2026, word for word with Architecture §3.4 and CE-09.)
8. **Locale (R9) changes surface only:** lexicon (`lex/`), script, register, voice. It never changes node selection or claims.
9. **Persona (R11)** comes from the level as `persona/<id>#<variant>`; an overlay may add the register overlay `persona/exam-coach#strategist`, never at `safety/ac0`. Persona has the lowest scalar precedence and owns no number.
10. ~~**After the EPP and the narration timeline exist:** music is resolved deterministically (logo variant by safety class, level and format; beds by the allowed roles of the format; SFX by the style palette filtered by level), so the result is part of the closure hash.~~ **Music (S5 selection, S10 placement).** Music entries are pinned in the EPP by the Resolver at S5 (logo variant by safety class, level and format; candidate beds by the format's allowed roles; SFX by the style palette filtered by level). After the narration timeline exists, placement and timing are written at S10 to the cue sheet and `bed_meta.json` with file hashes; these are closure inputs, never EPP fields. (Corrected 15 Oct 2026.)
11. **Packaging** is written at S14 only after RELEASE-CHECK (content) recomputes the closure; ~~DISCLOSURE and RELEASE-CHECK (publish) follow the export~~ COPY and DISCLOSURE are approved at S12 and checked by RELEASE-CHECK at S13, and the publisher records platform flags per channel in a publish receipt after S14 (Architecture §4; corrected 15 Oct 2026). Bytes fields (encode, burned captions) are pinned in the EPP by R14 (15 Oct 2026); distribution fields (copy, sidecar, chapters, disclosure placements) are pinned in the Distribution Package record.

**Who wins when two documents disagree (single source per fact).**

| Fact | Owner |
|---|---|
| Persona ids, variants, disclosure template text | `VOICE_and_PERSONA_REGISTRY.md` and the `voice/` entry |
| Pacing numbers, think windows, reading level | The Level Profile (`../LEVEL_PROFILES.md`); personas and scripts name bands, never numbers (CE-16) |
| Music policy, loudness, logo variants, beds | `MUSIC_and_SOUND_REGISTRY.md` (policy 1 to 7 cannot be weakened by an entry) |
| Check ids, severities, waiver rules | `QA_PROFILES_REGISTRY.md` |
| Look, motion, holds, safe zones, flash policy | `VISUAL_STYLE_and_ANIMATION_REGISTRY.md`, bounded by the safety class |
| Cue vocabulary mapping and locale tags | `CROSSWALK_cue_names_and_locales.md` |
| Beat grammar per format | `../FORMAT_REGISTRY.md` |
| Titles, covers, sidecar fields, platform placements | `PACKAGING_and_DISTRIBUTION_REGISTRY.md`; it can never change what an artefact says |
| Registry kinds and change classes | Architecture §3.1 and §3.6, with the 15 Oct 2026 addendum (CE-63) |
| Anything commercial | Outside the pipeline (CE-L1, RD-49): no price, tier, entitlement, free or paid field exists in any schema |

## 3. File index (word counts, whitespace-separated)

| File | Words |
|---|---|
| `SCRIPTING_REGISTRY.md` | 8,505 |
| `INTERACTION_and_ASSESSMENT_REGISTRY.md` | 6,204 |
| `VOICE_and_PERSONA_REGISTRY.md` | 9,064 |
| `MUSIC_and_SOUND_REGISTRY.md` | 6,613 |
| `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` | 9,421 |
| `PACKAGING_and_DISTRIBUTION_REGISTRY.md` | 8,568 |
| `QA_PROFILES_REGISTRY.md` | 14,397 |
| `SKILLS_and_KIT_MAP_v2.md` | 9,156 |
| `skills_map_v2.csv` | 831 |
| `CROSSWALK_cue_names_and_locales.md` | 1,855 |
| `README.md` (this file) | 5,663 |
| `templates/interaction_spec.template.md` | 1,105 |
| `templates/music_entry.template.md` | 621 |
| `templates/packaging_profile.template.md` | 1,841 |
| `templates/persona.template.md` | 510 |
| `templates/qa_profile.template.md` | 926 |
| `templates/script_spec.template.md` | 1,226 |
| `templates/style_entry.template.md` | 1,705 |
| `templates/voice_asset.template.md` | 702 |
| `schemas/golden_set.schema.json` | 250 |
| `schemas/interaction_spec.schema.json` | 2,844 |
| `schemas/lex_entry.schema.json` | 383 |
| `schemas/music_entry.schema.json` | 2,425 |
| `schemas/packaging_profile.schema.json` | 5,610 |
| `schemas/persona.schema.json` | 1,203 |
| `schemas/qa_profile.schema.json` | 2,850 |
| `schemas/script_spec.schema.json` | 3,629 |
| `schemas/style_entry.schema.json` | 2,856 |
| `schemas/voice_asset.schema.json` | 2,455 |

Documents, CSV, templates and schemas together (excluding this README): 107,657 words in 28 files. `skills_map_v2.csv` has 91 data rows. With this README the folder holds 29 files. (Recounted with `wc -w` by the critic-pass verifier, 15 Oct 2026.)

## 4. Schemas and validation status

All checks were run on 15 Oct 2026 with `jsonschema` `Draft7Validator.check_schema` for meta-validation, the commercial-term regex ~~`(price|pricing|paid|is_free|free_|premium|entitle|subscri|sku|paywall|unlock|monetis|monetiz|revenue|discount|coupon|tier)`~~ (case-insensitive, widened 15 Oct 2026 to Architecture §1.2 P1) `(price|pricing|paid|is_free|free_|premium|entitle|subscri|sku|paywall|unlock|monetis|monetiz|revenue|discount|coupon|tier|destination_resource|cta_destination|funnel|purchase_|checkout_|product_id|offer_|trial_|utm_|campaign_|affiliate_|activation_code|storefront)` over every object key at every depth, every `required` entry, pattern key and enum or const value in every `*.json` under `15_content_engine_v2/` (re-run 15 Oct 2026 with the widened regex: 0 hits), and positive and negative instance checks where an instance exists. The embedded JSON examples in the documents and templates were extracted and validated against their schemas.

| Schema | Meta-valid | Commercial lint | Instance checks this pass |
|---|---|---|---|
| `subsystems/schemas/script_spec.schema.json` | Yes | 0 hits (the `tier` property is now `cascade_rung`) | Example valid after the rename; the old `tier` key is rejected; `family/evs_foundational` accepted |
| `subsystems/schemas/interaction_spec.schema.json` | Yes | 0 hits | Document example and example file valid; `diagram_label`, `ordering` and `family/evs_foundational` accepted; 15 Oct 2026 stitch: `interaction_spec_content_sha256` and `script_content_sha256` required, a 6.3 s window and a dotted locale rejected |
| `subsystems/schemas/persona.schema.json` | Yes | 0 hits | Positive and negative suite passed (variant suffix accepted) |
| `subsystems/schemas/voice_asset.schema.json` | Yes | 0 hits | Positive and negative suite passed |
| `subsystems/schemas/music_entry.schema.json` | Yes | 0 hits | Positive and negative suite passed |
| `subsystems/schemas/style_entry.schema.json` | Yes | 0 hits | Template example valid; `licensed` and undefined `in_house` music rejected; free-text logo ref rejected; `premium_palette` and `asset_tier` rejected; AC0 `generated_gated` rejected |
| `subsystems/schemas/packaging_profile.schema.json` | Yes | 0 hits | Template example valid; both worked sidecars valid (re-validated after the stitch added every required pin kind); an interaction sidecar validates and one without `reveal_start` is rejected; ac0 `next_step` description block rejected; `gs/`, `reviewer/` and bare `packaging/` pin keys rejected; `access_tier` and `destination_resource_id` rejected; old audio-source constant rejected; invented bitrate and unmeasured release rejected |
| `subsystems/schemas/qa_profile.schema.json` | Yes | 0 hits | Positive and negative suite passed; 15 Oct 2026 stitch: `audit_share_per_mille` accepted and the float `audit_share_per_cell` rejected; `COPY` gate accepted; ug at ac1 no longer schema-checked (level_profile owns it) |
| `subsystems/schemas/lex_entry.schema.json` (new, 15 Oct 2026) | Yes | 0 hits | A `lex/core.hi-in` lexicon validates; a `price` key is rejected |
| `subsystems/schemas/golden_set.schema.json` (new, 15 Oct 2026) | Yes | 0 hits | A `gs/hi-in-stem_fixture` set validates; an unknown passage feature is rejected |
| `schemas/content_request.schema.json` | Yes | 0 hits | 15 Oct 2026: `variant`, `root_node_ids`, `taught_level` (required for and only for educator) and `packaging_profiles` accepted; per-kind id patterns reject `format/short.x`; `access_tier` rejected |
| `schemas/format_spec.schema.json` | Yes | 0 hits | 15 Oct 2026: a composition validates at all levels without aspect, resolution or duration and is rejected if it declares them; a derived spec without aspect is rejected; 16:9 at l9_10 rejected; `format_variants` accepted |
| `schemas/lesson_graph.schema.json` | Yes | 0 hits | `item_kind` enum now includes `diagram_label` and `ordering`; 15 Oct 2026 stitch: mcq without `options`, an original distractor without `distractor_source`, a unitless numeric answer, short without `rubric`, a past-paper item without `stem_form` and a `marking_scheme` without `marks` are rejected |
| `schemas/level_profile.schema.json` | Yes | 0 hits | `persona` pattern accepts `persona/<id>[@x.y.z][#variant]` and rejects an empty or malformed variant; 15 Oct 2026: `wpm_recap` required (null Hypothesis accepted for Cal levels), think window min below 4 rejected, optional `max_artefact_s` |
| `schemas/subject_profile.schema.json` | Yes | 0 hits | An inactive `family/evs_foundational` instance validates; 15 Oct 2026: `levels_allowed` required, the old boolean `perspectives_format_required` rejected, hybrid without `claim_flagger` rejected, languages_literature without `subject_locales` rejected |
| `schemas/epp.schema.json` (new, 15 Oct 2026) | Yes | 0 hits | A CR-2 EPP validates; a missing `qa/catalogue` pin, a `reviewer/` pin, a video EPP without a style pin, named reviewers in `resolved` and an unpinned requested overlay are rejected |
| `schemas/approval_record.schema.json` (new) | Yes | 0 hits | GS approval validates; VOICE without `narration_audio_sha256` and the old `reviewer_registry_version` are rejected; 15 Oct 2026 stitch: GA_DELTA binds `script_content_sha256` (old `script_bundle_sha256` rejected), DISCLOSURE binds the delivered file, voice pin and `disclosure_text_sha256`, GF/GS production_qa without `full_video_watched` rejected |
| `schemas/format_plan.schema.json` (new) | Yes | 0 hits | Plan validates; an unregistered slot is rejected |
| `schemas/locale_profile.schema.json` (new) | Yes | 0 hits | hi-IN validates; `tts_admitted: true` without a GL-voice-passed Path B voice, `locale/as-in` with `tts_admitted: true` and the typo `tts_admited` are rejected |

Enum and `const` values were also scanned for the same words: 0 hits. Registry ids used across these documents (format, level, family, locale, persona, style, safety) were checked against the Format Registry, Level Profiles, Subject Validation Profiles and the Architecture: all resolve. The 26 formats, 10 levels, 4 locales, 5 persona ids, 3 safety classes and 10 families match. The ten style ids were not in any decision and are now introduced by CE-72. The scanner's only other hits, `format/level` and `level/format`, are prose in two documents and not ids.

## 5. Inconsistency log

Status: **fixed** (changed in the files), **recorded** (the difference is noted in a dated note or decision and the fix is a P1 build item or a lead decision).

| ID | Inconsistency | Status | Where and how |
|---|---|---|---|
| A | `tier` in Script Spec fills against the commercial-term lint (CE-26) | Fixed | `script_spec.schema.json` `fills[].cascade_rung`, `SCRIPTING_REGISTRY.md` §16, `script_spec.template.md`; also the skills-map column (`exec_mode` in `skills_map_v2.csv`, "Exec mode" in `SKILLS_and_KIT_MAP_v2.md`) and "tier 3" cascade mentions. CE-70 |
| B | Style schema allowed `licensed` music; policy is owned or commissioned audio only | Fixed | `style_entry.schema.json` `sonic.music_sources` allows only `commissioned` and `code_composed`, `sonic_logo_ref` takes a `music/<id>@x.y.z` pin; `packaging_profile.schema.json` `audio_sources` is `owned_audio_only`; packaging, visual-style, FORMAT_REGISTRY text and CE-54 note. CE-66. The `lesson_graph` `music_source` enum keeps two reserved values (P1-05); and QA_PROFILES_REGISTRY.md Q-SAFE.audio_source and Q-RIGHTS (15 Oct 2026) |
| C | Persona ids against the nine Architecture §6 names | Fixed | `LEVEL_PROFILES.md` §3.11, Architecture §6 note, `TEMPLATES.md`; the `#variant` suffix accepted by the level, persona, voice and packaging schemas. CE-64 |
| D | Registry kinds `qa/`, `music/`, `lex/`, `gs/` (and `packaging/`) missing from Architecture §3.1 | Fixed | Architecture §3.1 addendum with change classes. CE-63 |
| E | Classes 1 to 5 EVS belongs to no family | Recorded as a [Recommendation] | `SUBJECT_VALIDATION_PROFILES.md` §13 and matrix row, Architecture §7 note, family enums in the script and interaction schemas. CE-65, P1-10 |
| F | `ShortSpec.access_tier` and `destination_resource_id` in the pipeline contract | Recorded (04 code deliberately not edited) | Dated notes in 07/05 and Architecture §10; CE-68; P1-01 |
| G | Animation media check A11 rejects 1920×1080; anim-qa severities contradict 07/06 | Fixed in the documents, code is P1 | `10_QA_GATES_anim.md` A11 and gate table, `examleaf-anim-qa/SKILL.md` (flash and untraceable science text critical), `references/flash_test_method.md`. CE-69, P1-03 |
| H | 05 cue actions against 12 cue kinds; Hinglish and `target_wpm` gaps | Crosswalk written; code is P1 | `CROSSWALK_cue_names_and_locales.md`. CE-71, P1-02 |
| I | ASM `item_kind` lacks `diagram_label` and `ordering`; "competitive" is an overlay, not a level | Fixed | `lesson_graph.schema.json`, `interaction_spec.schema.json`, interaction template and registry; `LEVEL_PROFILES.md` §3.12, Scripting and Interaction table rows, root README row. CE-67 |
| J | Music policy conflicts (bed level, spoken recaps, code-composed scope, logo length) | Fixed | `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` (summary, AC0, hook example, inconsistency 11) and `PACKAGING_and_DISTRIBUTION_REGISTRY.md` now follow `MUSIC_and_SOUND_REGISTRY.md`; its §12 items 6, 7 and 10 are marked; QA_PROFILES Q-SAFE.audio_source and Q-RIGHTS aligned (15 Oct 2026); bed level aligned to 20–24 dB in MUSIC §6 (15 Oct 2026; the 11 PLAYBOOK lines are outside the stitch scope and stay a recorded follow-up) |
| K | Packaging worked example used `persona/super_teacher@1.0.0`, which is not a registered id | Fixed | Now `persona/super-teacher@1.0.0#core`; packaging schema pattern accepts hyphen ids and the variant |
| L | QA registry cited `style/paper-collage-vertical` (a legacy key) as an id | Fixed | `style/paper-collage` with the legacy key noted |
| M | Four new style ids (whiteboard-science, lecture-slides, storybook-junior, exam-sheet) had no decision | Fixed | CE-72 |
| N | `access_tier` and `destination_resource_id` also appear in 07/12 (glossary), 07/00 (hand-off row), 12/13 (walkthrough), 07/11 (S14/SH2 checklist) and 07/03 (S14 export record) | Recorded; 07/11, 07/03 and 07/06 §7 got dated retirement notes on 15 Oct 2026 | P1-01 |
| O | `reviewer_roles` enums in the level and subject schemas lack `production_qa` and `publisher`; Format Spec `qa_checks` is a free string list | Recorded | P1-06 (the QA schema already adds the roles) |
| P | The Level Profile and Locale Profile both use `lexicon_ref` for different things | Recorded | P1-09 |
| Q | SFX token names in `style_tokens.json` differ from generator names | Recorded | P1-07 |
| R | 12/04 C11, doc 04 §5 and the token `canvas` stay vertical-only | Recorded | P1-03, waits on O-19 |
| S | The 05 `target_wpm` default of 140 would apply an adult English rate to Class 1 to 5, vocational and Indic content | Recorded | CROSSWALK §4.2; P1-02 |
| T | Architecture §7 says "nine families" | Fixed | Architecture §7 dated note; QA_PROFILES_REGISTRY.md §2 notation |
| U | Model-authored sentences could be cleared as non-assertive and escape the closure check | Fixed (15 Oct 2026) | Only deterministic Kit template output (`non_assertive_template_id`) may be `assertive: false`; a submitted Script Spec requires `closure.status: pass` (SCRIPTING §14; `script_spec.schema.json`). CE-74 |
| V | VOICE §3.9 disclosure wording (11 PB Step 14) differed from 07/06 §6.4, the packaging schema pattern and Q-DISC.script | Fixed | VOICE §3.9; RD-45's row text is the decision, 07/06 §6.4 the enforced template; PACKAGING §15 item 3 note |
| W | 12/10 A3 step 2 says never compare MP4 bytes; QA Q-DET compares MP4 SHA-256 | Fixed | QA_PROFILES_REGISTRY §2.1 Q-DET (same `harness/` pin, CE-38 bitexact, precondition O-16); dated note in 12/10 A3 |
| X | PACKAGING §15 item 3: the en-IN disclosure wording differs between RD-45, 07/06 §6.4 and VOICE §3.9 | Recorded (15 Oct 2026) | Needs a lead ruling; the sidecar schema no longer fixes the wording (text owned by the `voice/` entry, checked by Q-DISC.script) |
| Y | Scripting group (scripting-01 to -15): record and content hashes, non-assertive rule, node-type closure rules, condition preservation (SQ-20), F1 independent attempt, fixtures and K templates, locale pacing, spans, disclosure variants, rehearsal, model-profile fills (SQ-21) | Fixed | SCRIPTING_REGISTRY §1–§18; `script_spec.schema.json` and template; stitched notes in QA §2.2 (Q-CLOSURE.conditions), SKILLS row 44, FORMAT_REGISTRY F1, Architecture §8 (`pacing_by_level`, also added to `schemas/locale_profile.schema.json`). CE-73, CE-74 |
| Z | Schemas group (schemas-01 to -15): level→safety copies, registry enums, planned_ms and 0.5 s multiples, pin-key patterns, reviewer ids, YAML hash canon, set order, per-kind id patterns, new EPP, approval, Format Plan and Locale schemas | Fixed | `schemas/` and `subsystems/schemas/` (level→safety rules now only in `level_profile`; patterns per Architecture §3.1; `audit_share_per_mille`; multipleOf 0.5 on level, style, music and interaction numbers); QA §2.1 Q-SCHEMA, Q-HASH; Architecture §3.1, §3.5. CE-75, CE-76, CE-93 |
| AA | Safety group (safety-01 to -15): gate-requirement release rule, REN literals, AC0 style and close rules, voice-path agreement, rights scope, consented-custom voices, style loosening class, widened commercial lint | Fixed | Architecture §3.6, §3.7; QA §2.2 (Q-CLOSURE.ren_equivalence), §2.7 (Q-RIGHTS.scope), §2.9, §4.1, N-23, N-24; PACKAGING §11; packaging, voice and music schemas; FORMAT_REGISTRY F2, F8, F18. CE-89, CE-103 |
| AB | Resolver group (resolver-01 to -15): closure manifest M, content-hash binding, R8 limits, effect-based `qa/` class, re-resolution, R13 voice entry, R14 packaging, EPP and sidecar pin keys, gs/ not pinned, toolchain versions | Fixed | Architecture §3.1–§3.7; QA §1, §4.1; VISUAL §4.1 step 9; MUSIC §2.1; PACKAGING §1, §14; `interaction_spec`, `qa_profile`, `packaging_profile`, `epp` schemas. CE-73, CE-77 to CE-80 |
| AC | Walkthrough group (walkthrough-01 to -14): M1 scope and preconditions, distinct identities, drills, variants and roots, stage order, per-gate binding, style defaults, packaging profiles | Fixed; DISCLOSURE stage recorded in row AM | Roadmap §4; Architecture §3.4, §3.7, §4; QA §8.1; README §2. CE-82, CE-83 |
| AD | Coverage group (coverage-01 to -15): ca_cs on ug, family levels and overlays, single-language levels, language pair (R9a), taught_level, calibration nulls, voc interaction types, adult_prof F2/F18 | Fixed | LEVEL_PROFILES §2, §3, §5, §6; FORMAT_REGISTRY index and F14; INTERACTION §10; SCRIPTING §3, §5, §7.1; VISUAL §3.9; VOICE §3.2; `subject_profile`, `content_request` schemas. CE-81, CE-84, CE-87, CE-88 |
| AE | Sceptic group (sceptic-01 to -15): disclosure text ref, packaging catalogue ids, enum-free family registration, locale profile pointer, roadmap claims, P1 levels, test counts, schema paths, beat-grammar ownership | Fixed (sceptic-01 wording Recorded, row X) | SUBJECT_VALIDATION §13; QA §2.1, §2.7; PACKAGING §11; SCRIPTING §4 (beat-grammar column removed); Roadmap §1, §7. CE-90 |
| AF | Interaction group (interaction-01 to -15): interaction sidecar, structured ASM keys, numeric form, rubrics and rubric_entailment, step marking schemes, verbatim past-paper stems, response windows, binary choice, AC0 alternatives and spacing | Fixed | `lesson_graph.schema.json` node_ASM; `packaging_profile.schema.json#/definitions/interaction_sidecar`; INTERACTION §8–§15; QA §2.2 (Q-CLOSURE.asm_key, Q-CLOSURE.marking_scheme), §2.3 Q-RIGHTS, §2.6, §2.7; SUBJECT_VALIDATION §4, §5; QA §3.1 map gains `rubric_entailment`. CE-91, CE-92, CE-94 |
| AG | Voice group (voice-01 to -15): performer clones, as-IN native speaker, golden-set fields, A_direct disclosure, series continuity, successors, consent retention and withdrawal, STS golden sets, lexicon and golden-set contracts | Fixed | VOICE §1, §3, §4; `voice_asset`, `persona` schemas; new `lex_entry.schema.json` and `golden_set.schema.json`; 07/06 §6.4 A-direct row; PACKAGING §7; QA Q-DISC.placement; Roadmap P1-04. CE-95 to CE-97 |
| AH | Music group (music-01 to -15): derived window roles, non-teaching roles, AC0 bed limits, S5 selection and S10 placement, admission units, logo rules, bed level, licences, AC0 engagement audio, AD mix | Fixed; 12 skill-template JSON (music-10) and 11 PLAYBOOK lines (music-09) are outside the stitch's markdown scope and stay follow-ups | MUSIC §2–§12; `music_entry.schema.json`; CROSSWALK §2; 12/06 seed line; 12 audio-compose SKILL.md. CE-98, CE-99 |
| AI | Visual group (visual-01 to -15): AC0 verb bans, aspect filtering, storybook-junior slots, 16:9 releases, render determinism, typed data-fx, fixture motion, data-motion declarations, spatial flash patterns, reduced motion, style defaults, m_level ownership | Fixed | VISUAL §0–§14; `style_entry.schema.json`; `format_spec.schema.json` `style_defaults`; `level_profile.schema.json` `hold_level_multiplier`; QA A5, A14, Q-FLASH.pattern; SKILLS flash-analyser; Roadmap P1-12. CE-100 to CE-104 |
| AJ | Packaging group (packaging-01 to -15): ac0 publication, sidecar agreement rules, COPY approval, #render pins, publish receipts, reduced-motion delivery, copy phrase patterns, end-card line, house loudness, hashtags, corrections, child likeness | Fixed | PACKAGING §1–§15; `packaging_profile.schema.json`; QA §2.7, §4.1 (COPY, DISCLOSURE); Architecture §3.1, §4; `approval_record` and `qa_profile` gate enums. CE-105, CE-106 |
| AK | QA group (qa-01 to -15): hash_bind, catalogue rows for sibling checks, automated gates, O-22, id-only open items, validator map, sensitive topics, A13 severity, waivers, canary halts, ASR, review minutes, defect scopes, V-ladder | Fixed | QA §1–§11; `qa_profile.schema.json`; Architecture §3.7 (`full_video_watched`, `waivers[]`, also in `approval_record.schema.json`), §12 O-22; MUSIC §6.1, §7, §9; LEVEL_PROFILES §2; 12/10 A3 note; Roadmap P1-13. CE-107 |
| AL | Skills group (skills-01 to -15): v1-import drafts, cascade rungs per slot, registry validators, stage crosswalk, REN drafts, programme mix, single slot owners, retired lenses, packaging-export and kit-verify, ASM authorship, accessibility producers | Fixed | SKILLS_and_KIT_MAP_v2 and `skills_map_v2.csv` (89 rows); Architecture §5.2, §10, §10.1; INTERACTION §8; PACKAGING §7, §10, §11; QA §2.8, §2.12; MUSIC §5.1; Roadmap §1; 13 §2.4 addendum. CE-108 to CE-110 |
| AM | Conflicts between fix-pass notes, resolved at the 15 Oct 2026 stitch | Recorded | (1) DISCLOSURE stage: walkthrough-06 (S14, bound to the PKG hash) against packaging-05/resolver-10 (S12, bound to the delivered file); S12 adopted (CE-105), CE-86 struck. (2) GA-Δ input hashes: interaction-02 and walkthrough-07 (record `sha256`, `script_bundle_sha256`) against resolver-07 (content hashes); content hashes adopted (CE-73, CE-91). (3) Locale and persona id character sets: schemas-07 and sceptic-05 (dots allowed) against schemas-14 and Architecture §3.1 (no dots); §3.1 adopted. (4) Sidecar pin kinds: resolver-13 listed `gs/`; dropped per resolver-08 (gs/ not pinned). (5) Script Spec pin kinds: schemas-02 listed `reviewer/`; dropped per resolver-14. (6) voice-05 `A_direct` as a `voice_path` value and an English wording pattern: not applied; `disclosure_variant: path_a_direct` (schemas-01) already carries it, and a new voice_path value would break the ac0 and series Path A rules. (7) music-11 requires `all_current_and_future` in `commission.platforms`; safety-11's enum keeps it in place of `all`. (8) F14 visual line: visual-11 and coverage-13 merged |
| AN | MUSIC §2.1 item 1 (logo rules) still quoted the old five-element precedence chain "safety > level > overlay > format > style" as R8 (REVIEW_opus_pass leftover 1, check 9) | Fixed (15 Oct 2026, critic pass) | `MUSIC_and_SOUND_REGISTRY.md` §2.1 item 1 now refers to R8 as worded in Architecture §3.4, CE-09, §2 item 7 of this README and VISUAL §4.1 step 9 (limits take the most restrictive value; other scalars follow safety class > a11y profile > level > overlay > format > locale > style > persona) |
| AO | The `style_entry.schema.json` top-level description carried the old six-element chain and said the token-file hashes "enter the EPP pins and the approval closure hash", which predates resolver-03 (REVIEW_opus_pass leftover 1) | Fixed (15 Oct 2026, critic pass) | `schemas/style_entry.schema.json` description: R8 chain as in CE-09 and token hashes bound as resolver-03 states |
| AP | Q-RIGHTS checked `rights_status` but nothing said who may set `licensed` or `public_domain` for NCERT, board, CBSE or NTA material, and `quotation_within_policy` named no policy (completeness critic item 2, level-1) | Fixed in the documents; code is P1-17; legal position open (O-23, owner Counsel) | `QA_PROFILES_REGISTRY.md` Q-RIGHTS row: fails when the SRC `rights_basis` {policy_ref `rights/<publisher>@x.y.z`, decided_by, decided_on} is missing where rights_status ≠ `consulted_only`, or the policy has expired; registry kind `rights/`; `lesson_graph.schema.json` SRC. CE-112 |
| AQ | Renderings were checked only for literals (Q-CLOSURE.ren_equivalence), so an adapted analogy, story or context could enter as a REN and prose meaning drift had no check (completeness critic item 8, level-3+) | Fixed in the documents (report-only check) | New `Q-LOC.meaning` in `QA_PROFILES_REGISTRY.md`: back-translation of each REN diffed against its source node, flags routed to a bilingual subject reviewer at GA-Δ; report-only until the level-4 pilot measures precision. Architecture §8 rule "a REN changes wording only"; `adapted_from` and `locale_scope[]` on ANL, STY, WRK. CE-118 |
| AR | No corpus-level representation check: skew in names, genders, regions, settings, disability and language is invisible per artefact (completeness critic item 11, level-3+) | Fixed in the documents (report-only, quarterly) | New corpus check `Q-REPR` in `QA_PROFILES_REGISTRY.md` over the optional `depicted_attributes` tags on WRK contexts, STY characters, ASM stems and MED people (generated or drawn only); never blocks an artefact; quarterly report in Roadmap §6. CE-121 |
| AS | Q-A11Y covered only `a11y/base`; no checks for low vision, cognitive, dyslexia or ISL profiles, or for print output (completeness critic items 9 and 10, level-3+) | Fixed in the documents; profile values for `a11y/dyslexia` stay [Hypothesis]; sources open (O-24) | `QA_PROFILES_REGISTRY.md` Q-A11Y additions for `a11y/low_vision`, `a11y/cognitive`, `a11y/dyslexia`, `a11y/isl` and the print target (reading order, PDF tags); O-18 trigger reworded; O-24 registers the RPwD Act 2016 and the 2021 Ministry of Education e-content guidelines as sources to verify. CE-119, CE-120 |
| AT | Packaging had no text or print profile and no withdrawal path for offline copies (completeness critic items 5 and 9) | Fixed in the documents; file-size limit marked verify | `PACKAGING_and_DISTRIBUTION_REGISTRY.md`: new profile `packaging/print-pdf` (PDF/UA plus HTML from the same Format Plan via the pinned Chrome print path); `export/withdrawals.jsonl` {artefact_sha256, reason_class, replacement_sha256?, erratum_text} read by the platform and by offline clients on reconnect (`packaging/offline-download`). CE-115 (level-2), CE-119 (level-3+) |
| AU | The interaction sidecar did not require keyboard and screen-reader labels for ASM options (completeness critic item 10, level-3+) | Fixed in the documents | `INTERACTION_and_ASSESSMENT_REGISTRY.md` and the `interaction_sidecar` definition in `packaging_profile.schema.json`: every ASM option carries a keyboard and screen-reader label. CE-120 |
| AV | The skills map had no owner for curriculum framework ingestion, and learning-evaluation had no input from aggregate learning signals (completeness critic items 1 and 7) | Fixed in the documents | `SKILLS_and_KIT_MAP_v2.md` and `skills_map_v2.csv`: new skill `examleaf-curriculum-ingest` (syllabus PDF → candidate framework items with spans → H-CG; validates against `curriculum_framework.schema.json`); learning-evaluation reads `learning_signal` records and opens `signal_proposal` rows, never graph edits. CE-111, CE-117 |
| AW | Eleven leftovers from the critic-pass verifier that were lead calls or one-line edits: crypto-shredding granularity, signature scope, `a11y_isl` as an R1 reason, print in the Script Spec, Interaction Spec and sidecar print form, the §3.1 character-set sentence, `FW-assam` examples, overlay `exam_windows`, reviewer schema split, ledger-row schemas, the root README format count, the SKILLS §9 item 8 note and a stray `__pycache__` | Fixed (CE-123, CE-124; P1-18, P1-19) | Architecture §3.1, §3.4 R1, §3.7, §9.5; `approval_record`, `epp`, `qa_profile`, `script_spec` schemas; VOICE §3.10; PACKAGING §14 examples; MATURITY §7; root README; `SKILLS_and_KIT_MAP_v2.md` §9 |

Open items that are lead decisions, not build items, remain in the individual documents: for example the CE-14 ruling on whether variants and renditions each need GF or GS, the O-5 spoken disclosure line, O-7 song licensing, O-19 16:9 safe zones, O-23 the counsel rights position for official sources and O-24 the disability-access sources (both added 15 Oct 2026), and every platform figure marked "verify".

## 6. P1 build items (level per Roadmap §7)

Full table with locations and the level of each item in `../MATURITY_MODEL_and_ROADMAP.md` §7 (retitled 15 Oct 2026: not every item is level 1).

| ID | Item |
|---|---|
| P1-01 | Remove `access_tier` and `destination_resource_id` from the 04 `ShortSpec` code, schema and tests (and the 07/12, 07/00, 12/13, 07/11 and 07/03 mentions) |
| P1-02 | Cue-crosswalk code items: `meta.cue_actions`, Hinglish in 05, unset-able `target_wpm`, educator pacing, action-to-kind test |
| P1-03 | `media_check()` reads the resolution from the EPP; vertical-only 12/04 items accept a 16:9 token set after O-19 |
| P1-04 | CI: compile every schema under `schemas/` and `subsystems/schemas/` (21 on 15 Oct 2026, with `lex_entry` and `golden_set`, then `curriculum_framework` and `learning_signal` from the completeness critic), run the commercial lint over all JSON including embedded examples, add instance tests (including the pin-key positives and negatives of Roadmap §7) and the copy lint, and the voice/ cross-field checks XF-1 to XF-5 (VOICE §4.1; 15 Oct 2026) |
| P1-05 | Narrow the `lesson_graph` `music_source` enum when O-7 is decided; implement the Q-RIGHTS gate M6 |
| P1-06 | Align `reviewer_roles` enums; make Format Spec `qa_checks` accept only catalogue ids |
| P1-07 | Map SFX token names to generator names |
| P1-08 | Seed the five new registry kinds and the ten style ids; wire them into the Resolver pin map (except gs/, which is recorded on the voice entry and is not pinned) |
| P1-09 | Rename one of the two `lexicon_ref` fields |
| P1-10 | Register `family/evs_foundational` through GR when the lead activates it |
| P1-11 | Schemas for `overlay/`, `safety/`, `a11y/`, `reviewer/`, `slot/`, `model/`, `kit/`, `harness/`, then `budget/` (15 Oct 2026; `lex/` and `gs/` schemas added the same day) Lead ruling 15 Oct 2026 (CE-124): the `overlay/` schema carries `exam_windows[]` (CE-122), and the `reviewer/` schema takes over the `reviewer_entry` and `signing_key` definitions that sit inside `approval_record.schema.json` until then. |
| P1-12 | 12/04 harness contract 1.1.0: typed data-fx (`fixture:<FX-id>#<path>`, `node:<id>#<field>`) at Level 2, `fx()` prefix handling with E_FIXTURE_MISSING, and the A1 data-motion lint rule (15 Oct 2026; level 2) |
| P1-13 | Admit an ASR provider (07/07) and wire `transcript_check` to it, so Q-NARR.asr_diff can move from R to M (15 Oct 2026; level 4) |
| P1-14 | curriculum_framework schema, fixtures and negative tests in CI before M1 step 1, with the UUIDv5 GUID-minting function and a re-ingest idempotence test (CE-111; 15 Oct 2026; level 1) |
| P1-15 | content-addressed blob store (`content/blobs/sha256/<aa>/<hash>`), daily cross-region backup with `backup` ledger rows, `retention_class` with per-class crypto-shredding, restore drill (CE-114; 15 Oct 2026; level 2, M1 exit gate) |
| P1-16 | signed approvals and the agent-identity CI rule: `signing_keys[]` on `reviewer/`, `signature` on approval records, `ssh-keygen -Y verify` in RELEASE-CHECK, CI rejection of agent commits to `content/approvals/` (CE-113; 15 Oct 2026; level 2, M1 exit gate) |
| P1-17 | rights_basis field and Q-RIGHTS expiry check: SRC `rights_basis`, registry kind `rights/`, Q-RIGHTS fails on a missing basis or expired policy (CE-112, O-23; 15 Oct 2026; level 2) |
| P1-18 | Schemas for the blob manifest, the ledger row types `backup`, `incident` and `signal_proposal`, and `export/withdrawals.jsonl`, so CI validates every record that Architecture §9.5–§9.7 writes; `backup` rows are level 1 (the M1 restore drill reads them), `incident` and `signal_proposal` rows level 2 (lead ruling 15 Oct 2026, CE-124) |
| P1-19 | Print support inside the per-artefact schemas: relax the voice-path, beat-timing and duration rules of `script_spec.schema.json` for `render_target: print`; the Interaction Spec stays video and audio only (print has no timed interactions; answer keys are separate files); the sidecar print form and print disclosure wording are decided at level 3 before `packaging/print-pdf` leaves draft (CE-119; lead ruling 15 Oct 2026, CE-124; level-3+) |

## 7. Reading order

1. `../README.md` and `../ARCHITECTURE_content_engine_v2.md` §3 and §6 (resolver, levels).
2. `SCRIPTING_REGISTRY.md` and `INTERACTION_and_ASSESSMENT_REGISTRY.md` (what is said and asked).
3. `VOICE_and_PERSONA_REGISTRY.md`, `MUSIC_and_SOUND_REGISTRY.md`, `VISUAL_STYLE_and_ANIMATION_REGISTRY.md` (how it sounds and looks).
4. `QA_PROFILES_REGISTRY.md` and `PACKAGING_and_DISTRIBUTION_REGISTRY.md` (how it is checked and shipped).
5. `SKILLS_and_KIT_MAP_v2.md` (who does it) and `CROSSWALK_cue_names_and_locales.md` (the seams with sections 05 and 12).
