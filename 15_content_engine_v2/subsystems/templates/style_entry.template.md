# Style entry template (`content/registry/style/<id>.yaml`)

Validates against `../schemas/style_entry.schema.json`. A style says how an artefact looks and moves, never what it asserts. Every selectable entry extends `style/base@1.0.0` and binds the 02 and 12 token files by pointer and SHA-256 (the file hashes are fields of the style entry, so they enter the closure through the style pin inside `epp_hash`, not as separate closure keys; corrected 15 Oct 2026, Architecture §3.7). A style may only tighten limits: fields marked `"x-kind": "limit"` take the most restrictive value, and other scalars follow safety class > a11y profile > level > overlay > format > locale > style > persona (R8 as corrected 15 Oct 2026). Full rules: `../VISUAL_STYLE_and_ANIMATION_REGISTRY.md`. Dated 15 Oct 2026.

Three rules to remember before you fill it in:

- **No commercial or "tier" field names.** CI rejects, case-insensitively, any match of `(price|pricing|paid|is_free|free_|premium|entitle|subscri|sku|paywall|unlock|monetis|monetiz|revenue|discount|coupon|tier|destination_resource|cta_destination|funnel|purchase_|checkout_|product_id|offer_|trial_|utm_|campaign_|affiliate_|activation_code|storefront)` applied to every object key at every depth, every `required` entry, pattern key and enum or const value; `series_position`, `flagship` and `demo_kind` are exempt (CE-26, CE-70; widened 15 Oct 2026). Asset provenance classes are `asset_sources_allowed`.
- **Owned audio only.** `sonic.music_sources` is `commissioned` and/or `code_composed`. `licensed` is not admissible (CE-66). `sonic_logo_ref` is a pin to an admitted `music/` entry, never free text.
- **Never put a number you cannot source.** Every tunable number is a tagged value (`value`, `tag`, and for a Hypothesis an `owner` and a `pilot_ref`). A null value must be a Hypothesis.

## Fill-in skeleton

```yaml
style_id: style/<lowercase-id>                  # e.g. style/storybook-junior
version: 1.0.0
title: <Human title>
purpose: <one sentence: what this style is for and where it is the default>
status: draft                                   # draft | released | deprecated | revoked   (released needs measured-or-approved safe zones)
legacy_style_id: <key in 12 style_tokens.json, optional>
extends: [style/base@1.0.0, <other style/<id>@x.y.z if layered>]   # style/base must be present unless this IS style/base
layer: <science | expressive | hybrid>          # root only for style/base
selectable: true                                # false only for style/base
route_tags_allowed: [<data-bound | illustrative | narrative | typographic | spatial-hero | hook | recap | comparison | scale-story | insert | lattice | organelle-schematic | concept-island | label | next-step | slide | sheet | map | timeline | text-passage | equation | story | activity | card>]
route_tags_forbidden: [<same enum>]
safety_classes_allowed: [safety/<ac0 | ac1 | ac2>]
levels_allowed: [level/<l1_2 | l3_5 | l6_8 | l9_10 | l11_12 | ug | pg | adult_prof | voc | educator>]
formats_allowed: [format/<id>]
aspects_supported:                              # at least one
  - aspect: <9x16 | 16x9>
    resolution: <1080x1920 for 9x16 | 1920x1080 for 16x9>
    formats_limited_to: [format/<id>]           # required for 16x9
    safe_zone_tokens: {role: safe_zones_<9x16|16x9>, path: <token file>, json_pointer: <ptr>, sha256: <64 hex>}   # required unless token_status is missing
    token_status: <approved | placeholder_insets | missing>   # 16x9 may only be released with approved (O-19)
token_bindings:                                 # at least one; each {role, path, json_pointer, sha256, file_version?}
  - {role: <base_palette_typography | style_common | style_block | safe_zones_9x16 | safe_zones_16x9 | music_policy | holds | fonts_registry>, path: <file>, json_pointer: "<ptr or empty>", sha256: <64 hex>}
palette:
  artwork_palette: <base_light | base_light_tints | storybook_13>
  science_text_on: <base_tokens | base_tokens_tag>
  dark_surfaces: <forbidden | mood_only_pending_ad17>   # ac0 ⇒ forbidden
  colour_alone_never_differentiates: true       # constant
  one_highlight_at_a_time: true                 # constant
  max_accents: <int, optional>
  display_only_pairs: [<fg/bg pairs below 4.5:1, never essential text>]
typography:
  science_fonts: [<font ids, at least one>]
  display_fonts: [<optional>]
  indic_fonts: {devanagari: [<…>], bengali_assamese: [<…>]}
  indic_animation_unit: <word | word_or_grapheme_cluster_after_test_card>
  per_codepoint_animation: forbidden            # constant
  fonts_vendored_hashed_licensed: true          # constant (no CDN, RD-23)
  max_title_words: <int, optional>
  max_words_on_screen: <int, optional>
motion:
  vocabulary: [<motion verbs, at least one>]     # science layer may not list boil, idle, shake, whip, push_in, pan, parallax_drift, orbit, paper_burst, wiggle
  element_transition_ms: [<min>, <max>]
  highlight_ms: [<min>, <max>]
  scene_transition_ms: [<min>, <max>]           # optional
  boil_fps_allowed: [<int 1-30>]                # optional
  camera_off_during: [<hold | think | label_reveal | measurement | data_bound_reveal>]
  repeats: finite_only                          # constant
  by_safety_class:                              # a style may only tighten
    safety/<acN>:
      flash_policy: <ac0_zero_flash for ac0 | wcag_2_3_1 for ac1, ac2>
      verbs_forbidden: [<verbs>]                # ac0 must forbid shake, whip, push_in, parallax_drift, orbit, boil (until O-2), count_up and paper_burst, with pop_overshoot_max ≤ 1.4 and idle_rotation_deg_max ≤ 1.5; also fixture_rotate (15 Oct 2026)
      dark_surfaces: <forbidden | mood_only_pending_ad17>   # ac0 ⇒ forbidden
      pop_overshoot_max: <n>                    # required at ac0, ≤ 1.4
      idle_rotation_deg_max: {value: <n|null>, tag: <Recommendation|Hypothesis|Inherited|Evidence>, owner: <if Hypothesis>, pilot_ref: <if Hypothesis>}   # required at ac0, value ≤ 1.5
      boil_fps_max: {value: <n|null>, tag: <…>}  # optional; ≤ 8 at ac0
      hold_extra_multiplier: {value: <n ≥ 1.0 | null>, tag: <…>}   # optional style tightening on top of the Level Profile on_screen.hold_level_multiplier (m_level); renamed 15 Oct 2026
  reduced_motion:
    verbs_disabled: [<verbs>]                   # must include boil, idle, wiggle, parallax_drift, push_in, pan, zoom, orbit, shake, whip, paper_burst, somber_drop, count_up, sheet_slide (registry §2.2; 15 Oct 2026)
    reveal_replacement: <fade_150_300_ms | cross_dissolve_150_300_ms | none_needed>
    variant_rendered: true                      # constant: the variant is always rendered
holds:
  tokens: {role: holds, path: <file>, json_pointer: <ptr>, sha256: <64 hex>}
  formula: "m_script * m_level * max(headline_min_s, per_word_floor_s * word_count)"   # constant
  script_multipliers:                           # latn, deva, beng required; hinglish_latn optional
    latn: {value: <n>, tag: <…>}
    deva: {value: <n|null>, tag: Hypothesis, owner: <native editor>, pilot_ref: <…>}
    beng: {value: <n|null>, tag: Hypothesis, owner: <native editor>, pilot_ref: <…>}
  question_visible_through_think_window: true   # constant
flash:
  full_frame_flash: forbidden                   # constant
  policy_by_class: {safety/ac0: ac0_zero_flash, safety/ac1: wcag_2_3_1, safety/ac2: wcag_2_3_1}   # list the classes you allow; safety/ac0 is required when ac0 is allowed
slot_types_implemented: [<slot ids from the closed vocabulary; at least one>]
science_layer:
  data_bound_scenes_resolve_to: style/<science style, normally style/whiteboard-science>
  data_attribute: data-fx                       # constant
  data_path_kinds: [<fixture | node>]
  decorative_motion_on_science: forbidden       # constant
  text_in_generated_rasters: forbidden          # constant
asset_sources_allowed: [<code_only | owned_or_licensed | generated_gated>]   # ac0 styles may not list generated_gated
cost: {cost_class: <zero_credit_code | zero_credit_render_box | zero_credit_studio_minutes | gated_generation_estimate_at_h_sb>, credits_default: 0, estimate_gate: H_SB, ledger_rows: [<cost | capacity | provenance | licence>]}
references: [{kind: <style_guide | token_file | prompt_template | master_prompt | reference_clip | stills | hero_sheet | storyboard_grid | fixture | format_spec | doc>, path: <path>, sha256: <optional>}]
sonic:                                          # optional block; if present, music_policy and music_sources are required
  sonic_logo_ref: music/<id>@<x.y.z>            # pin to an admitted sonic_logo entry (ac0 ⇒ music/logo-junior)
  child_variant_required: <true | false>
  music_policy: {role: music_policy, path: <file>, json_pointer: <ptr>, sha256: <64 hex>}
  music_sources: [<commissioned | code_composed>]     # owned audio only (CE-66)
  sfx: [<music/sfx-<name> ids from the style palette>]
determinism:
  contract_path: <path to the harness contract>
  contract_version: <x.y.z>
  canvas_from_epp_resolution: true              # constant: the canvas comes from the EPP, never hard-coded
  render_box_pinned: <true | false>
qa:
  a_suite: "A1-A17 all"                         # constant
  parameters: {<A-check or Q-check id>: "<style-specific parameter note>"}
forbidden: [<free-text list of things this style must never do>]
edge_cases: ["#<n>" | "NEW-<n>"]
evidence: [{claim: <…>, tag: <…>, source: <N# or doc>, owner: <if Hypothesis>, pilot_ref: <if Hypothesis>}]
changelog: [{version: <x.y.z>, date: "<YYYY-MM-DD>", semver_class: <patch|minor|major>, change_class: <Presentational|Safety|Structural|Render toolchain|Revocation>, summary: <…>}]
```

## Worked example

A draft AC0 style: `style/storybook-junior`. The hashes are placeholders and every figure marked Hypothesis names an owner and a pilot. This block validates against the schema.

```json
{
  "style_id": "style/storybook-junior",
  "version": "1.0.0",
  "title": "Storybook Junior",
  "purpose": "AC0 story, song, activity and picture-card visuals.",
  "status": "draft",
  "extends": ["style/base@1.0.0", "style/paper-collage@1.0.0"],
  "layer": "expressive",
  "selectable": true,
  "route_tags_allowed": ["illustrative", "narrative", "story", "activity", "card", "hook", "recap"],
  "route_tags_forbidden": ["data-bound", "spatial-hero"],
  "safety_classes_allowed": ["safety/ac0"],
  "levels_allowed": ["level/l1_2", "level/l3_5"],
  "formats_allowed": ["format/detailed", "format/short", "format/story_history"],
  "aspects_supported": [
    {"aspect": "9x16", "resolution": "1080x1920", "token_status": "placeholder_insets",
     "safe_zone_tokens": {"role": "safe_zones_9x16", "path": "12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json", "json_pointer": "", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"}}
  ],
  "token_bindings": [
    {"role": "base_palette_typography", "path": "02_learning_psychology/palette_and_typography_tokens.json", "json_pointer": "", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"},
    {"role": "style_common", "path": "12_advanced_animations_with_claude/05_style_guides/style_tokens.json", "json_pointer": "/common", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"}
  ],
  "palette": {"artwork_palette": "storybook_13", "science_text_on": "base_tokens_tag", "dark_surfaces": "forbidden", "colour_alone_never_differentiates": true, "one_highlight_at_a_time": true},
  "typography": {"science_fonts": ["inter", "noto_sans", "katex_fonts"], "indic_animation_unit": "word", "per_codepoint_animation": "forbidden", "fonts_vendored_hashed_licensed": true},
  "motion": {
    "vocabulary": ["appear", "fade", "pop", "sheet_slide", "cross_dissolve", "idle", "highlight"],
    "element_transition_ms": [150, 300],
    "highlight_ms": [300, 600],
    "repeats": "finite_only",
    "by_safety_class": {
      "safety/ac0": {
        "flash_policy": "ac0_zero_flash",
        "verbs_forbidden": ["boil", "shake", "whip", "push_in", "parallax_drift", "orbit", "fixture_rotate", "count_up", "paper_burst", "somber_drop"],
        "idle_rotation_deg_max": {"value": 1.5, "tag": "Hypothesis", "owner": "child-development reviewer", "pilot_ref": "PILOT-ac0-motion"},
        "pop_overshoot_max": 1.4,
        "hold_extra_multiplier": {"value": null, "tag": "Hypothesis", "owner": "child-development reviewer", "pilot_ref": "PILOT-ac0-holds"},
        "dark_surfaces": "forbidden"
      }
    },
    "reduced_motion": {"verbs_disabled": ["boil", "idle", "wiggle", "parallax_drift", "push_in", "pan", "zoom", "orbit", "shake", "whip", "paper_burst", "somber_drop", "count_up", "sheet_slide", "pop"], "reveal_replacement": "cross_dissolve_150_300_ms", "variant_rendered": true}
  },
  "holds": {
    "tokens": {"role": "holds", "path": "12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json", "json_pointer": "/hold_times_s", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"},
    "formula": "m_script * m_level * max(headline_min_s, per_word_floor_s * word_count)",
    "script_multipliers": {
      "latn": {"value": 1.0, "tag": "Inherited"},
      "deva": {"value": 1.5, "tag": "Hypothesis", "owner": "native editor", "pilot_ref": "PILOT-indic-holds"},
      "beng": {"value": 1.5, "tag": "Hypothesis", "owner": "native editor", "pilot_ref": "PILOT-indic-holds"}
    },
    "question_visible_through_think_window": true
  },
  "flash": {"full_frame_flash": "forbidden", "policy_by_class": {"safety/ac0": "ac0_zero_flash"}},
  "slot_types_implemented": ["story.beat", "story.song_chant", "activity.setup", "activity.do", "activity.observe", "activity.safety_cue", "hook.surprise", "hook.realworld", "hook.question_reveal", "explain.ladder_step", "explain.definition", "explain.analogy", "check.retrieval", "check.predict", "misconception.elicit", "card.front", "card.back", "recap.retrieval", "recap.statement", "source.read", "chapter.title", "close.next_step", "bridge.return_link"],
  "science_layer": {"data_bound_scenes_resolve_to": "style/whiteboard-science", "data_attribute": "data-fx", "data_path_kinds": ["fixture", "node"], "decorative_motion_on_science": "forbidden", "text_in_generated_rasters": "forbidden"},
  "asset_sources_allowed": ["code_only", "owned_or_licensed"],
  "cost": {"cost_class": "zero_credit_code", "credits_default": 0, "estimate_gate": "H_SB", "ledger_rows": ["capacity"]},
  "references": [{"kind": "style_guide", "path": "12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md"}],
  "sonic": {
    "sonic_logo_ref": "music/logo-junior@1.0.0",
    "child_variant_required": true,
    "music_policy": {"role": "music_policy", "path": "12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json", "json_pointer": "/audio/music_policy", "sha256": "0000000000000000000000000000000000000000000000000000000000000001"},
    "music_sources": ["commissioned", "code_composed"]
  },
  "determinism": {"contract_path": "12_advanced_animations_with_claude/04_harness_contract/contract.md", "contract_version": "1.0.0", "canvas_from_epp_resolution": true},
  "qa": {"a_suite": "A1-A17 all", "parameters": {"A6": "ac0 tile analyser", "Q-FLASH.ac0_zero": "blocking after O-2"}},
  "edge_cases": ["#48", "#54", "#55", "#56"],
  "evidence": [{"claim": "Play-way and multimodal methods suit Classes 3-5", "tag": "Evidence", "source": "[N9][N10]"}]
}
```

## Checklist before GR (registry change review)

1. The entry validates, the commercial-term lint (widened regex, every key, enum and const value) is clean, and the word `tier` appears in no field name. Dates in the YAML are quoted strings (YAML 1.2 core; Architecture §3.1 Registry entry hash).
2. It extends `style/base@1.0.0`, and a science style (`layer: science`) lists none of the banned expressive verbs.
3. An AC0 style: ac0 must forbid shake, whip, push_in, parallax_drift, orbit, boil (until O-2), count_up and paper_burst, with pop_overshoot_max ≤ 1.4 and idle_rotation_deg_max ≤ 1.5. It also forbids `fixture_rotate`, lists `safety/ac0` in `flash.policy_by_class`, forbids dark surfaces, lists no `generated_gated` asset source and carries the child-development sign-off (updated 15 Oct 2026; the schema enforces all but the sign-off).
4. A 16:9 aspect lists `formats_limited_to`, is only `released` with approved tokens, and the style allows a level that may use 16:9 (UG, PG or adult professional).
5. `sonic.music_sources` lists owned sources only, and `sonic_logo_ref` points at an admitted `music/` entry. The music registry is bumped in the same pull request if the logo changed.
6. Every Hypothesis has an owner and a pilot, and a null value is a Hypothesis.
7. `motion.reduced_motion.verbs_disabled` lists the registry §2.2 reduced-motion set (15 Oct 2026).
8. Run the impact preview. A Presentational change re-renders and re-runs the A-suite, flash and a11y checks for every artefact that pins this style, and reopens GF/GS only where bytes change.
