# Voice asset template (`content/registry/voice/<id>.yaml`)

Validates against `../schemas/voice_asset.schema.json`. One entry = one voice × one locale × one version. Personal data never lives in this file: names, contracts, consent forms and reference audio stay in the private store (`private://…`, gitignored, access-controlled; 07/07 §7). Never student recordings. Admission (`status: admitted`) needs licence or consent evidence (Maturity Roadmap step 6), a passed native review and, for provider voices, a verified live contract and a passed golden set; a TTS voice also needs a GL-voice pass.

```yaml
voice_id: voice/<lowercase-id>                # e.g. voice/st-brand-en-in, voice/performer-p001-as-in
version: 1.0.0
title: <Human title>
status: draft                                 # draft | admitted | suspended | revoked | superseded
asset_kind: <human_performer | sts_target_voice | tts_voice>
path_role: <A_direct_release | A_performance_source | A_conversion_target | B_tts>
target_origin: <designed_synthetic | performer_clone | provider_stock>   # tts_voice and sts_target_voice: required; performer_clone ⇒ performer + consented-custom + uses [identity_reference, voice_clone] + counsel + provider verification
superseded_by: voice/<id>@<x.y.z>             # required when status: superseded; later series members pin it
personas: [persona/<id>]
locale: locale/<id>                           # as-in ⇒ human_performer + A_direct_release only (RD-42)

performer:                                    # human_performer only
  performer_ref: performer/<pseudonymous-id>
  adult: true                                 # constant
  is_student: false                           # constant
  credit_ref: private://<path>                # the "Performed by" credit text
  on_camera_release_ref: private://<path>     # only if talking-head inserts use the performer's image
  native_speaker_of_locale: <true|false>     # as-in ⇒ true (schema)

provider:                                     # tts_voice and sts_target_voice only
  provider: <provider name as in 05 TTS_PROVIDER_COMPARISON>
  model_id: <exact model id>
  provider_voice_ref: <provider voice id; never a placeholder containing REPLACE>
  api_version: <if the provider requires one>
  live_contract_verified: <true|false>
  admission_record_ref: <07/07 §4 admission record>
  controls_permitted: [<only controls proven by a live request>]
  lifecycle: {deprecation_notice_date: "<YYYY-MM-DD>", shutdown_date: "<YYYY-MM-DD>", custom_voice_storage_expiry: "<YYYY-MM-DD>"}

rights:
  rights_status: <audition-only | licensed-stock | consented-custom | unverified>   # 05 VoiceIdentity enum
  rights_record_ref: private://<path>
  consent:                                    # human_performer, performer_clone and consented-custom STS/TTS: required
    consent_record_ref: private://<path>
    uses: [recording, performance_reference, identity_reference, speech_to_speech_conversion, voice_clone, on_camera_insert]   # only what was consented
    languages: [locale/<id>]
    territories: [<…>]
    platforms: [<…>]
    term_start: "<YYYY-MM-DD>"
    term_end: "<YYYY-MM-DD>"
    named_processors: [<every third-party processor that receives recordings; must have passed 07/07 admission>]
    promotional_use_allowed: <true|false>
    compensation_recorded_in_contract: true   # constant; amounts never stored here
    revocation_terms_ref: private://<path>
    revocation_effect: <withdraw_published | future_only>   # default withdraw_published unless counsel approves future_only
    deletion_terms_ref: private://<path>
    models_permitted: [<exact provider model ids>]   # required when uses include speech_to_speech_conversion, voice_clone or identity_reference; target model must be listed (XF-5)
    raw_audio_retention_until: "<YYYY-MM-DD>"   # raw takes, reference audio, golden-set recordings
    removal_sla_days: <integer ≥ 1>
    only_seen_content: true                   # constant
  counsel_review_ref: <consent template sign-off, O-6>
  provider_verification_ref: <provider cloning/identity verification, where required>

verification: {status: <unverified | contract_verified | live_request_verified | golden_set_passed>, live_request_record_ref: <ref>, date: "<YYYY-MM-DD>"}
gl_voice:                                     # tts_voice: required
  status: <not_applicable | not_run | pending | passed | failed | lapsed>
  record_ref: <ledger row>
  reviewer_ids: [reviewer/<id>]
  tested_model_id: <model id>
  families_covered: [family/<id>]
  date: "<YYYY-MM-DD>"
native_review: {status: <not_run | pending | passed | failed>, reviewer_ids: [reviewer/<id>], record_ref: <ref>}
golden_set:                                   # tts_voice and sts_target_voice: required
  golden_set_ref: gs/<locale>-<family>@<x.y.z>
  golden_set_sha256: <64 hex>
  accepted_audio_manifest_sha256: <64 hex>    # required when admitted
  last_run_date: "<YYYY-MM-DD>"                 # required when result is pass or fail
  result: <not_run | pass | fail>
  tested_model_id: <model id>                 # required when result is pass or fail; = provider.model_id when admitted (XF-1)
  tested_provider_voice_ref: <voice id>       # required when result is pass or fail; = provider.provider_voice_ref when admitted (XF-1)
  reviewer_ids: [reviewer/<id>]               # at least one when admitted
lexicon_refs: [lex/<family>.<locale>@<x.y.z>]

allowed:
  formats: [format/<id>]
  levels: [level/<id>]
  safety_classes: [safety/<id>]               # B_tts may never list safety/ac0
  families: [family/<id>]
disclosure:
  variant: <path_a_converted | path_a_direct | path_b_tts>   # must match path_role
  text_ref: <locale disclosure text id>
expiry: {expires_on: "<YYYY-MM-DD>", renewal_due_by: "<YYYY-MM-DD>", renewal_owner: <name>}
voice_identity:                               # compiled to the 05 VoiceIdentity contract
  identity_id: <lowercase id>
  brief: <provider style brief from the persona voice_brief>
  reference_audio_sha256: <64 hex, optional>
revocation:                                   # required when status: revoked
  reason: <…>
  effective_date: "<YYYY-MM-DD>"
  scope_note: <…>
  processor_deletion_confirmation_refs: [private://<path>]   # required for consent_withdrawn under withdraw_published
  replay_store_purged: true                   # same condition; CE-38 stored audio purged, hashes kept as records
owner: <founder or delegate>
evidence:
  - {field: <field>, tag: <Evidence|Inherited|Recommendation|Hypothesis>, source: <ref>}
```

Checklist before GR: the consent scope covers every use, locale, platform and processor this entry allows; the performer is not a GF approver of their own performance; the golden set was re-run on the exact `model_id` and provider voice id (XF-1); `expires_on` is no later than the provider shutdown, custom-voice storage expiry and consent term end (XF-4); the Locale Profile `voices[]` row is updated in the same pull request.
