# Persona template (`content/registry/persona/<id>.yaml`)

Validates against `../schemas/persona.schema.json` (draft-07, `additionalProperties: false`). Replace `<…>`. Delete optional lines you do not use; never add fields. No commercial fields, no wpm numbers (pacing lives in the Level Profile: CE-16, R8). A released persona is immutable; a change is a new version through GR (pedagogical change class, Architecture §3.6).

```yaml
persona_id: persona/<lowercase-id>            # super-teacher | super-teacher-junior | lecturer | exam-coach | skills-instructor
version: 1.0.0
title: <Human title>
status: draft                                 # draft | released | superseded | revoked
kind: <root | derived | register_overlay>     # root only for persona/super-teacher
inherits: persona/super-teacher@<x.y.z>       # required unless kind: root
identity: >
  <One paragraph: who this teacher is for this audience, in observable behaviour.>
voice_brief: >
  <Casting/performance brief: clarity, warmth, amusement ceiling, what never to do with the voice.>
core_rules:                                   # all fifteen are required (schema); they can only be added to, never removed
  - no_fake_sensing
  - no_invented_biography
  - no_impersonation
  - no_unconditional_praise
  - no_ease_or_marks_guarantees
  - no_ridicule_or_sarcasm_at_learner
  - no_fake_disfluency_or_laughter
  - no_intention_as_cause
  - no_pressure_fear_or_urgency
  - no_data_solicitation
  - no_claims_outside_closure
  - no_stage_tags_in_spoken_text
  - no_speeding_science_to_fit_time
  - humour_ceiling_not_quota
  - answer_hidden_until_window_ends
overlays: [overlay/<id>]                      # register_overlay only
excluded_safety_classes: [safety/ac0]         # register_overlay only (must contain ac0)
variants:
  - variant_id: <lowercase-id>
    architecture_name: <name used in Architecture §6, e.g. Super Teacher Coach>
    levels: [level/<id>]
    safety_classes: [safety/<ac0|ac1|ac2>]    # an ac0 variant lists ac0 alone
    register:
      summary: <one line>
      sentence_style: <e.g. one idea per sentence; concrete nouns>
      vocabulary: <controlled_list | board_terms_with_glossary | discipline_register | research_register | trade_register | professional_register>
      humour: <none | play_safe | concept_linked | dry_rare>   # ac0 ⇒ none or play_safe
      sarcasm_allowed: false                  # constant
      rigour_markers: [<e.g. "under the assumption that">]
      required_moves: [<e.g. state the condition before the formula>]
    modes_allowed: [<curious | steady | deliberate | light | reassuring | focused>]   # ac0 ⇒ never focused (schema)
    direction_map:                            # all nine beats required
      - {beat: hook,          mode: <mode>, intent: <what the voice does>, notes: <optional>}
      - {beat: prerequisite,  mode: <mode>, intent: <…>}
      - {beat: core,          mode: <mode>, intent: <…>}
      - {beat: worked,        mode: <mode>, intent: <…>}
      - {beat: guided,        mode: <mode>, intent: <…>}
      - {beat: independent,   mode: <mode>, intent: <…>}
      - {beat: misconception, mode: <mode>, intent: <…>}
      - {beat: recap,         mode: <mode>, intent: <…>}
      - {beat: cta,           mode: <mode>, intent: <learning next step only; no platform call to action>}
    additional_never: [<persona-specific prohibitions>]
    retired_expressions: [<phrases the persona linter flags>]
    capture_brief: <Path A: the learner the performer speaks to, e.g. "one Class 10 student in Jorhat who got this wrong three times">
    pacing_notes: <mode ordering or level-band reference; never a new number>
pacing:
  owner: level_profile                        # constant
  mode_order_slow_to_fast: [deliberate, reassuring, steady, focused, curious, light]
  locale_rule: no_cross_language_rate_transfer  # constant
persona_lint:
  blocking: false                             # report-only until the persona pilot passes (CE-35)
  rules_ref: <persona-lint rule file id>
owner: <academic lead or delegate>
evidence:
  - {field: identity, tag: Inherited, source: "03 INSTRUCTIONS Step 1"}
  - {field: <field>, tag: Hypothesis, source: <ref>, owner: <name>, pilot_ref: <pilot id>}
```

Checklist before GR: persona linter fixtures pass (positive and negative scripts); every level that names this persona resolves to exactly one variant; the direction map was read aloud by a Path A performer; the child-development reviewer signed any ac0 variant.
