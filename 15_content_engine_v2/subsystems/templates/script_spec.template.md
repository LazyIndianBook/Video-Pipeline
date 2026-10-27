# Template: Script Spec (`content/scripts/<artefact_id>/SS-<id>.json`)

Validates against `subsystems/schemas/script_spec.schema.json` (draft-07, `additionalProperties: false` everywhere). Rules: `subsystems/SCRIPTING_REGISTRY.md`. Replace `<…>` placeholders; delete optional lines you do not use; never add fields that are not in the schema; no commercial fields of any kind (CE-L1). The compiler fills most identity, pin and budget fields from the EPP and Format Plan; authors and Kit fills write `beats[].sentences[]` and the direction fields.

```json
{
  "script_spec_id": "SS-<id>",
  "version": "1.0.0",
  "hash_canon": "JCS-RFC8785+NFC",
  "script_content_sha256": "<content hash bound by GA-Δ; exclusions in Scripting Registry §1>",
  "status": "<draft | machine_checked | submitted | superseded | revoked>",
  "timing_status": "PLANNED_NOT_AUDIO_MEASURED",
  "request_id": "CR-<id>",
  "epp_hash": "<sha256 of the EPP>",
  "format_plan_sha256": "<sha256>",
  "graph_subtree_sha256": "<sha256>",
  "pins": {"format/<id>@<x.y.z>": "<sha256>", "level/<id>@<x.y.z>": "<sha256>", "persona/<id>@<x.y.z>#<variant>": "<sha256>", "locale/<id>@<x.y.z>": "<sha256>"},
  "format": "format/<id>",
  "variant_id": "<level or format variant, e.g. gentle | short.misconception>",
  "level": "level/<id>",
  "safety_class": "safety/<ac0 | ac1 | ac2>",
  "persona": "persona/<id pinned in the EPP, e.g. super-teacher-junior | super-teacher | lecturer | skills-instructor>",
  "persona_variant": "<variant pinned in the EPP, e.g. junior | coach | core | mentor | lecturer | seminar-lead | colleague | instructor>",
  "register_overlay": "persona/exam-coach",
  "exam_overlay": "overlay/<id>",
  "family": "family/<id>",
  "locale": "locale/<id pinned in the EPP, e.g. en-in | hinglish | hi-in | as-in>",
  "language_pair": {"medium": "locale/<id>", "target": "locale/<id>"},
  "voice_path": "<A | B | mixed>",
  "voice_path_by_chapter": {"1": "<A | B>", "2": "<A | B>"},
  "render_target": "<video | audio_only>",
  "interaction_spec_id": "IS-<id>",
  "beat_map_of": {"script_spec_id": "SS-<master id>", "sha256": "<master sha256>"},
  "duration_budget_s": {"min": <n>, "max": <n>},
  "word_budget": {"min": <n | null>, "max": <n | null>, "tag": "<Inherited | Hypothesis | Recommendation | Evidence>", "source": "<e.g. 02 §G2 bands × planned speech seconds>", "owner": "<if Hypothesis>", "pilot_ref": "<if Hypothesis>"},
  "beats": [
    {
      "beat_id": "b01",
      "chapter": 1,
      "slot": "<registered slot, e.g. hook.realworld>",
      "objective_ids": ["OBJ-<id>"],
      "hook_kind": "<realworld | question_reveal | surprise | contradiction | unfinished_task | none>",
      "close_kind": "<delayed_practice | capability_check | next_artefact_pointer | open_loop | retest | calm_end | none>",
      "direction": {"mode": "<curious | steady | deliberate | light | reassuring | focused>", "wpm_band": "<ordinary | dense | recap | teacher_set>", "target_wpm": <resolved from EPP, or null for teacher_set>, "emphasis": ["<phrase that occurs verbatim>"], "notes": "<optional>"},
      "pause_after": {"kind": "<none | beat | think | pause-video>", "seconds": <0 for none; ≤4 for beat; ≥4 and a multiple of 0.5 for think and pause-video>, "prompt": "<required for think and pause-video>", "interaction_id": "II-<id, required for think and pause-video>"},
      "cues": [{"cue_id": "<id>", "phrase": "<spoken phrase>", "occurrence": 1, "edge": "start", "action": "<show | highlight | transform | hide | reveal-answer>", "element_id": "<scene element>"}],
      "answers_after": "<earlier beat id with a think or pause-video window>",
      "interaction_id": "II-<id>",
      "visual_essential": <true | false>,
      "sting": false,
      "planned_ms": <integer milliseconds>,
      "word_budget": {"min": <n | null>, "max": <n | null>, "tag": "<…>"},
      "sentences": [
        {
          "sentence_id": "b01-s1",
          "role": "<assertive | exam_language | citation | analogy | misconception_statement | question_prompt | feedback | humour | story_frame | instruction | transition | rhetorical | call_response | disclosure>",
          "spoken_text": "<clean spoken words; no [ ] < >; numbers and units in spoken form>",
          "display_text": "<on-screen form, e.g. I = V/R>",
          "lang": "<BCP-47, only when the whole sentence differs from the locale>",
          "spans": [{"text": "<span, in order>", "lang": "<BCP-47>"}],
          "node_ids": ["<CLM-… | SIM-… | WRK-…#n | ASM-… | MIS-… | ANL-… | STY-…#n>"],
          "fixture_refs": ["<fixture id and case>"],
          "tokens": [{"text": "<0.4 A>", "kind": "<number | date | name | unit | symbol | term>", "fixture_ref": "<fixture case>"}],
          "assertive": <true, or false only for Kit template output>,
          "non_assertive_template_id": "<NAT-… Kit template id, only when assertive is false>",
          "is_new_wording": <true | false>
        }
      ]
    }
  ],
  "closure": {"status": "<pass | fail | not_run>", "checker_version": "<x.y.z>", "assertive_sentences": <n>, "mapped_sentences": <n>, "unmapped_sentence_ids": [], "unmatched_tokens": [], "unconfronted_mis_ids": [], "checked_at": "<ISO 8601>"},
  "derived_surface": {"sim_ids": ["SIM-<id>"], "anl_ids": ["ANL-<id>"], "new_wording_sentence_ids": ["<sentence ids>"], "interaction_ids": ["II-<id>"]},
  "disclosure": {"template": "<path_a | path_a_direct | path_b | mixed, matching voice_path and locale>", "variant": "<standard | child (AC0)>", "text_ref": "voice/<id>@<x.y.z>#<path_a | path_b | child>", "locale": "locale/<id>"},
  "fills": [
    {"beat_id": "b01", "cascade_rung": "<kit_template | haiku | sonnet | opus | human>", "role": "<author | review | repair>", "model_profile_ref": "model/<id>@<x.y.z>, for model rungs", "effort": "<low | medium | high | xhigh | max>", "max_justification_ref": "LEDGER-<id>, only for effort max", "kit_version": "<x.y.z>", "prompt_template_id": "<kit template id>", "output_sha256": "<sha256>", "attempt": 1, "result": "<accepted | rejected | escalated>"}
  ],
  "qa_results": [{"check_id": "SQ-01", "result": "<pass | fail | report_only_flag | not_applicable>", "detail": "<optional>"}],
  "recent_script_ledger": {"window": 20, "repeated_sentence_ids": []},
  "rehearsal": {"measured_s": <n>, "beat_seconds": {"b01": <n>}, "reader_role": "<path_a_performer | author>", "take_sha256": "<sha256>", "measured_at": "<ISO 8601>"},
  "provenance": {"author_kind": "<human | model | import>", "author_id": "<id>", "created_at": "<ISO 8601>", "model_profile_ref": "<model/id@x.y.z, if model>", "effort": "<if model>", "kit_version": "<if model>"}
}
```

## Notes

- Omit `variant_id`, `register_overlay`, `exam_overlay`, `language_pair`, `beat_map_of`, `hook_kind`, `close_kind`, `answers_after`, `interaction_id`, `display_text`, `lang`, `fixture_refs`, `tokens`, `slot_params`, `recent_script_ledger`, `non_assertive_template_id`, `spans`, `voice_path_by_chapter`, `rehearsal` and `max_justification_ref` when unused. `spans` is required for `locale/hinglish` and with a `language_pair`; `rehearsal` is required before GA-Δ when any beat is `teacher_set` (Scripting Registry §2). Registry ids are patterns; Q-SCHEMA checks each against the EPP pins (15 Oct 2026). `register_overlay` requires `exam_overlay` and is never allowed at AC0.
- Level fixes safety class, persona and variant. ~~(schema; ids from `VOICE_and_PERSONA_REGISTRY.md` §2.2)~~ The Level Profile and the voice registry own the mapping; Q-SCHEMA checks that the Script Spec carries the EPP's values (corrected 15 Oct 2026). Current mapping: l1_2/l3_5 → ac0, super-teacher-junior#junior; l6_8 → super-teacher-junior#coach; l9_10 → super-teacher#core; l11_12 → super-teacher#mentor; ug and adult_prof → lecturer#lecturer; pg → lecturer#seminar-lead; educator → lecturer#colleague; voc → skills-instructor#instructor.
- AC0 forces `voice_path: A`, the child disclosure variant and no `next_artefact_pointer` close (CE-19). Path A converted uses `path_a`, Path A direct (as-IN) uses `path_a_direct`, Path B uses `path_b`, a single-file F16 uses `mixed` with `voice_path_by_chapter`; never Path A wording on Path B audio (RD-45; corrected 15 Oct 2026).
- Hashes: `sha256` excludes lifecycle and check fields; GA-Δ binds `script_content_sha256` (Scripting Registry §1).
- Never type a WPM number by hand: `target_wpm` is resolved from the EPP band (CE-16). For `teacher_set` it is null.
- Every sentence with role `assertive`, `exam_language`, `citation`, `analogy`, `misconception_statement`, `question_prompt`, `feedback` or `humour` needs at least one node ID, of the type its role requires (Scripting Registry §14). A model-authored sentence is assertive whatever its role; only Kit template output may be `assertive: false`. Fixture cases go in `fixture_refs`, never `node_ids`.
- The beat header form for reviews and recording sheets is defined in the Scripting Registry §13; it is a rendering of these fields, not a separate source.

## Checklist before GA-Δ

- [ ] `closure.status = pass` (required for `submitted`): no unmapped sentence, no unmatched token, every elicited MIS confronted, every cited claim's conditions present (SQ-20).
- [ ] Any `teacher_set` beat: `rehearsal` recorded and within `duration_budget_s`.
- [ ] Every SIM and ANL used is in `derived_surface` (with `what_is_lost` and `non_mapping` visible to the reviewer).
- [ ] Every think and pause-video beat has an `interaction_id` present in the Interaction Spec; every reveal has `answers_after`.
- [ ] No tags or markup in `spoken_text`; emphasis phrases occur verbatim.
- [ ] Persona, register and forbidden-phrase lints run (SQ-05 to SQ-09); AC0 rules pass.
- [ ] Contested and time-bound phrasing per family (Scripting Registry §7.2); marks only from the source paper or official key.
- [ ] Disclosure record matches the voice path, locale and safety class.
- [ ] `fills[]` records `model_profile_ref`, effort and Kit version for every model fill (ledger justification for max); timing stays `PLANNED_NOT_AUDIO_MEASURED` until narration is measured.
- [ ] Locale edition: same beat map as the master (`beat_map_of`), native subject editor assigned.
