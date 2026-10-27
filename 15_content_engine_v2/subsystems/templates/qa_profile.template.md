# QA Profile template (`content/qa_profiles/QAP-<request_id>.json`)

A QA Profile is **generated** by `profile-resolver` as `qa_resolve(EPP, qa/catalogue@<version>)`. Nobody writes one by hand. This template does two jobs:

- it documents the shape, for reviewers reading a profile;
- it is the starting point for CI fixtures (positive and negative).

**Rules.**
- The profile must validate against `../schemas/qa_profile.schema.json` (draft-07). `additionalProperties` is false everywhere.
- Replace `<…>` placeholders and delete optional lines you do not use.
- No commercial fields. No field name contains "tier".
- Check IDs come from `../QA_PROFILES_REGISTRY.md` §2 exactly. Lowercase IDs such as `q-closure` fail.

```json
{
  "qa_profile_id": "QAP-<request_id>",
  "version": "1.0.0",
  "catalogue_pin": "qa/catalogue@<x.y.z>",
  "request_id": "CR-<id>",
  "epp_hash": "<64 hex>",
  "format_plan_sha256": "<64 hex>",
  "axes": {
    "format": "format/<id>",
    "format_variant": "<e.g. short.misconception>",
    "level": "level/<l1_2|l3_5|l6_8|l9_10|l11_12|ug|pg|adult_prof|voc|educator>",
    "family": "family/<stem_fixture|quant_social|humanities_citation|languages_literature|arts_skills|vocational|exam_strategy|health_medicine|law|evs_foundational>",
    "locale": "locale/<en-in|hinglish|hi-in|…>",
    "safety_class": "safety/<ac0|ac1|ac2>",
    "voice_path": "<A|B; absent for print>",
    "render_target": "<video|audio_only|print (level-3+, CE-119, 15 Oct 2026)>",
    "aspect": "<9x16|16x9; absent for print>",
    "resolution": "<1080x1920|1920x1080>",
    "overlay": "overlay/<id>",
    "style": "style/<id>"
  },
  "voice_path_reasons": ["<format_default_a|series_first|flagship|demo_real|safety_ac0|level_floor_a|a11y_isl|no_gl_voice_tts|path_b_default>"],
  "checks": [
    {
      "check_id": "<Q-…|Q-….sub|A1…A17|A<n>.sub, e.g. A9.package>",
      "stage": "<S1…S14|GR>",
      "mode": "<auto|human|hybrid>",
      "implementation": {"skill": "<skill name>", "script": "<script path>", "status": "<exists|extend|to_build>"},
      "owner": "<owning skill, or founder-engineer (CI); registry §2.12>",
      "human_roles": ["<role>"],
      "severity": "<critical|major|minor>",
      "severity_provenance": [{"source": "<registry id or catalogue>", "severity": "<…>"}],
      "enforcement": "<blocking|report_only>",
      "report_only_until": "<trigger, e.g. level/l9_10 pilot; O-2 signed>",
      "precondition_open_items": ["O-<n>"],
      "waivable": false,
      "waiver_roles": ["<role holding the gate; never the author>"],
      "params": {"<name>": "<value with provenance>"},
      "applies_because": ["<format/…|family/…|safety/…|a11y/base|locale/…|voice path|render target>"],
      "pass_criteria": "<one line, copied from the catalogue with resolved parameters>",
      "defect_scope": ["<science|instruction_answer|readability|sync|audio|accessibility_flash|craft|tone|composition|rights|disclosure|metadata|determinism|child_safety|claims_sources|schema_hash>"],
      "review_minutes_estimate": {"minutes": 0, "basis": "<rd41_baseline|o14_timed|pilot_timed>"},
      "evidence": {"path": "jobs/<artefact_id>/qa/<check_id>.json", "bound_to_artefact_sha256": true}
    }
  ],
  "gates": [
    {
      "gate": "<H_CG|GV_CLAIMS|GA_GRAPH|GA_DELTA|H_SB|VOICE|A_SUITE|GF|GS|COPY|DISCLOSURE|G_COUNSEL|GL_GLOSSARY|GL_VOICE|RELEASE_CHECK>",
      "roles": [{"role": "<role>", "count": 1, "co_sign": false}],
      "automated": false,
      "bound_to": ["<the gate's bound object, registry §4.1; GA_DELTA: script_content_sha256, interaction_spec_content_sha256, format_plan_sha256, graph_subtree_sha256>"],
      "sampling": "never",
      "distinct_identities": true,
      "author_may_approve": false,
      "reopen_on": ["<byte change|subtree change|voice change|…>"],
      "defect_scope": ["<scope from registry §2.12>"],
      "review_minutes_estimate": {"minutes": 0, "basis": "<rd41_baseline|o14_timed|pilot_timed>"}
    },
    {"gate": "A_SUITE", "roles": [], "automated": true, "bound_to": ["artefact_sha256"], "sampling": "never", "distinct_identities": true, "author_may_approve": false, "defect_scope": ["determinism", "readability", "accessibility_flash", "science", "sync", "audio", "composition", "craft", "rights", "metadata"]},
    {"gate": "RELEASE_CHECK", "roles": [], "automated": true, "bound_to": ["closure_hash"], "sampling": "never", "distinct_identities": true, "author_may_approve": false, "defect_scope": ["schema_hash", "metadata"]}
  ],
  "preconditions": {
    "g_counsel_record_ref": "<counsel record for the safety class and export schema version>",
    "gl_voice_record_ref": "<required when voice_path = B>",
    "gl_glossary_record_ref": "<first artefact of a family × locale pair>",
    "open_items": [{"id": "O-<n>"}],
    "reviewers_available": [{"role": "<role>", "primary": "reviewer/<id>", "backup": "reviewer/<id>"}]
  },
  "judge_policy": {
    "judge_model_ref": "model/<id>@<x.y.z>",
    "calibration_record_ref": "<ledger ref of the calibration run for this cell>",
    "admitted_questions": ["<binary question admitted for this cell>"],
    "may": ["reorder_queue", "add_flag", "prefill_evidence", "recommend_escalation", "block_pending_human"],
    "may_approve": false, "may_waive": false, "may_pass_check": false, "counts_as_approval": false
  },
  "reqa_policy": {
    "automated_coverage": "all_affected",
    "order": "canary_first",
    "audit_share_per_mille": 50,
    "human_gates_on_changed_bytes": "never_sampled",
    "auto_reaffirm_requires_identical_bytes": true
  },
  "human_minutes_total": 0,
  "self_approval_allowed": false,
  "provenance": {
    "resolver_version": "<x.y.z>",
    "created_at": "<ISO 8601 date-time>",
    "source_entries": ["format/<id>@<v>", "level/<id>@<v>", "family/<id>@<v>", "safety/<ac#>@<v>", "a11y/base@<v>", "locale/<id>@<v>", "qa/catalogue@<v>"]
  },
  "qa_profile_sha256": "<64 hex: sha256(JCS(NFC(profile minus qa_profile_sha256 minus provenance.created_at)))>"
}
```

## What the schema enforces

- **Mandatory gates.** Every profile has GV_CLAIMS, GA_DELTA, H_SB, A_SUITE, VOICE (except print, below), COPY (added 15 Oct 2026; the GF/GS reviewer pair on copy_sha256), DISCLOSURE, RELEASE_CHECK and GF or GS. Human gates are `sampling: never`, `distinct_identities: true` and `author_may_approve: false`. A_SUITE and RELEASE_CHECK are automated, with no human roles; every other gate names at least one role. Every gate names its `defect_scope`. *(15 Oct 2026.)*
- **Critical checks.** A critical check has `waivable: false`. It is blocking, unless `precondition_open_items` names the open items its cell's release waits on (for example Q-FLASH.ac0_zero before O-2 is signed).
- **Waivers and report-only checks.** A waivable check names `waiver_roles` (copied from registry §2.12). A report-only check names `report_only_until`.
- **Owner, scope and minutes** *(15 Oct 2026)*. Every check names an `owner` and a `defect_scope` from the registry §7 vocabulary. Human and hybrid checks carry `review_minutes_estimate`; the profile carries `human_minutes_total` (registry §3 rule 10).
- **Universal checks.** Every profile carries Q-SCHEMA, Q-COMM, Q-HASH, Q-CLOSURE, Q-META, Q-META.hash_bind, Q-DISC.script, Q-LEDGER.citation, Q-A11Y.transcript and Q-DET. *(15 Oct 2026: Q-META.hash_bind added; Q-A11Y.captions moved to video, because audio_only delivers a transcript.)*
  - Video adds Q-FLASH.full_frame, A3, A11, Q-A11Y.captions and Q-A11Y.reduced_motion.
  - audio_only adds Q-A11Y.visual_essential.
  - print (level-3+, CE-119, 15 Oct 2026) adds Q-A11Y.visual_essential and Q-A11Y.print_structure. A print profile has no narration, so `axes.voice_path`, `axes.aspect`, `axes.resolution`, `voice_path_reasons` and the VOICE gate are absent; every other profile must carry them.
  - `family/stem_fixture`, `family/quant_social`, `family/health_medicine` and `family/evs_foundational` add Q-FIX (registry §3.1).
- **Aspect.** 16:9 only at 1920×1080 for `level/ug`, `level/pg` and `level/adult_prof`. Otherwise 1080×1920.
- **Level and safety.** `level/ug` always uses `safety/ac1`. `safety/ac0` forces Path A.
- **ac0 extras.** ac0 adds:
  - the Q-SAFE rows (no_solicitation, no_external_prompts, no_timers, startle, language, sensitive) and Q-FLASH.ac0_zero;
  - a child-development co-sign on GA_DELTA, H_SB and GF/GS;
  - a child-development reviewer with a named backup;
  - O-1, O-2 and O-22 listed in `open_items` (by id only).
- **Path B** requires a `gl_voice_record_ref`.
- **Check ids** *(15 Oct 2026)*. The `check_id` pattern accepts the new parent `Q-LOC` (Q-LOC.meaning, CE-118). The corpus check Q-REPR (CE-121) is never in a profile, so the pattern rejects it.
- **Judges** can never approve, waive, pass a check or count as an approval.

## Checklist before a profile is accepted

1. `profile-resolver` produced it, and two runs give the same `qa_profile_sha256`.
2. The `catalogue_pin` matches the pin in the EPP.
3. Every check's severity is ≥ its catalogue base (no lowering). `severity_provenance` lists each contributor.
4. Every applicable check has an evidence path. A missing file means incomplete, which blocks.
5. Gate roles resolve to active entries in `reviewer/` with no conflict of interest.
6. RELEASE-CHECK finds every listed open item closed, with a closure record, in the Architecture §12 register. *(15 Oct 2026: open-item state is no longer stored in the profile, so it does not change `qa_profile_sha256`.)*
