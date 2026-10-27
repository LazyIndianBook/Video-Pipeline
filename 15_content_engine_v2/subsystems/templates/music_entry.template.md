# Music and sound entry template (`content/registry/music/<id>.yaml`)

Validates against `../schemas/music_entry.schema.json`. v1 admits owned audio only: `code_composed` (seeded, `examleaf-audio-compose`) or `commissioned` (contracted composer with assignment, full buyout or exclusive perpetual licence). No third-party samples, no platform-library songs. Music is never placed in a teaching window.

```yaml
music_id: music/<lowercase-id>                # e.g. music/logo-core-short, music/bed-reel-hook-paper-neutral
version: 1.0.0
title: <Human title>
status: draft                                 # draft | admitted | suspended | revoked | superseded
kind: <sonic_logo | sting | bed | sfx | ambience | song_backing>
variant: <core_full | core_short | core_extended | junior | lecture | correct_answer | transition | loop_30s | loop_60s | mood_neutral | mood_somber | mood_endcard | one_shot>   # core_*/lecture ⇒ ac1/ac2 only; sonic_logo junior ⇒ ac0 only
motif_ref: music/<motif-id>@<x.y.z>           # required for sonic_logo; recommended for every logo-derived asset
origin: <code_composed | commissioned>        # sonic_logo ⇒ commissioned
composed_by_human: <false for code_composed | true for commissioned>
contains_samples: false                       # constant in v1
release_eligible: <true|false>                # prototype-only entries ⇒ false

generator:                                    # code_composed only
  skill: examleaf-audio-compose
  script_path: <path>
  script_sha256: <64 hex>
  generator_version: <pin>
  seed: <seed of the reference render; per-scene seeds follow MUSIC §5.1 step 3>
  request_sha256: <64 hex>
  determinism_verified: <true after a second render matched>   # admitted ⇒ true

commission:                                   # commissioned only
  composer_ref: composer/<pseudonymous-id>
  contract_ref: private://<path>
  contract_sha256: <64 hex of the signed agreement in the private store>
  originality_warranty: true                  # constant: no samples or pre-existing third-party material
  licence_type: <copyright_assignment | full_buyout | exclusive_perpetual_licence>
  territory: worldwide                        # constant
  term: <…>
  platforms: [all_current_and_future, <…>]    # must contain all_current_and_future
  promotional_use_allowed: true               # constant
  stems_location_ref: private://<path>
  counsel_review_ref: <O-7 sign-off>
  contract_date: "<YYYY-MM-DD>"

licence_ledger_ref: <CE-49 ledger row of type licence>
files:
  - {role: <stem|mix|one_shot|loudness_matched|stems_package>, name: <name>, path: <path>, sha256: <64 hex>, sample_rate: 48000, bit_depth: <16|24>, channels: <1|2>, duration_s: "<n.nn> s", peak_dbfs: "-<n.n> dBFS"}
musical: {bpm: <60-180>, beats_per_bar: 4, bars: <n>, mood: <neutral|somber|endcard|curious|calm>}

placement:
  allowed_segment_roles: [<cold_open | hook | chapter_transition | outro | end_card | reel_hook | reel_cta | reel_end | wordless_visual | story_interlude | song_chant | cue_sfx | prototype>]   # never a teaching role; sfx and sting must include cue_sfx; song_backing: song_chant (or prototype); ac0: no reel_hook or reel_cta
  forbidden_segment_roles: [core_explanation, worked_example, derivation, think_window, pause_video, spoken_recap, safety_cue, equation_reading, inspection]   # bed, sonic_logo, ambience, song_backing: all nine; sfx, sting: think_window, pause_video, equation_reading, inspection, safety_cue
  storyboard_named_only: <true>               # sfx and sting: required
mix:
  under_speech_db: {min: <n|null>, max: <n|null>, unit: dB, tag: Hypothesis, source: <ref>, owner: <audio lead>, pilot_ref: <T2>}   # beds, logos, ambience; ac0 beds and ambience: min ≥ 20
  cue_gain_db: {min: <n>, max: <n>, unit: dB, tag: Recommendation, source: <ref>}                                                   # sfx and sting
  duck_reduction_db: {min: <n>, max: <n>, unit: dB, tag: Hypothesis, source: <ref>, owner: <…>, pilot_ref: <…>}
  rise_between_phrases_allowed: <true|false>  # ac0 ⇒ false, and required for ac0 beds, ambience, song backings and logos
  end_card_swell_db_max: <0-6>                # ac0 ⇒ ≤ 3, required as above
allowed:
  formats: [format/<id>]
  levels: [level/<id>]
  safety_classes: [safety/<id>]               # listing ac0 forces startle_class none and child-development sign-off
  styles: [style/<id>]
startle:
  startle_class: <none | low | dramatic>      # dramatic ⇒ justification_required true, never ac0
  ac0_safe: <true|false>
  flash_pairing_forbidden: true               # constant
  justification_required: <true|false>
  notes: <onset, low-frequency content, why it is safe>
science_binding: <none | decorative | data_bound>   # data_bound ⇒ science review signs the cue
qa:
  human_listen: <pending | ok | chiptune | too_busy | masks_speech | wrong_mood | startling>   # admitted ⇒ ok
  listener_id: reviewer/<id>
  child_development_signoff_ref: <required when ac0 is allowed>
  phone_speaker_checked: <true|false>         # admitted ⇒ true
expiry: {expires_on: <"YYYY-MM-DD" | null>, renewal_owner: <name>}
revocation: {reason: <…>, effective_date: "<YYYY-MM-DD>"}   # required when status: revoked
owner: <audio lead>
evidence:
  - {field: <field>, tag: <…>, source: <ref>}
```

Checklist before GR: the human listen was done on a phone speaker together with narration; the determinism re-render matched (code_composed); the licence ledger row exists; the style entry that references this asset (`sonic logo`) is bumped in the same pull request.
