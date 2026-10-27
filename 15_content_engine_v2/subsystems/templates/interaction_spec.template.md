# Template: Interaction Spec (`content/scripts/<artefact_id>/IS-<id>.json`)

Validates against `subsystems/schemas/interaction_spec.schema.json` (draft-07, `additionalProperties: false` everywhere). Rules: `subsystems/INTERACTION_and_ASSESSMENT_REGISTRY.md`. Replace `<…>` placeholders; delete optional lines you do not use; never add fields that are not in the schema; no commercial fields (CE-L1). One Interaction Spec per Script Spec. `sha256` is required (NFC → JCS → SHA-256 with the `sha256` field excluded). GA-Δ binds the content hashes `script_content_sha256` (of the Script Spec) and `interaction_spec_content_sha256` (this spec with `sha256`, `interaction_spec_content_sha256`, `interaction_spec_id`, `version`, `epp_hash`, `format_plan_sha256`, `script_content_sha256`, `qa_results` and `provenance` removed), so any content change to either stales GA-Δ and a pin-only release does not (15 Oct 2026, resolver-07). The level → safety class mapping is checked against the EPP (Q-SCHEMA), not by this schema.

```json
{
  "interaction_spec_id": "IS-<id>",
  "version": "1.0.0",
  "hash_canon": "JCS-RFC8785+NFC",
  "sha256": "<sha256 of this spec, sha256 field excluded>",
  "script_spec_id": "SS-<id>",
  "interaction_spec_content_sha256": "<sha256>",
  "script_content_sha256": "<sha256>",
  "epp_hash": "<sha256>",
  "format_plan_sha256": "<sha256>",
  "format": "format/<id>",
  "level": "level/<id>",
  "safety_class": "safety/<ac0 | ac1 | ac2, matching the level>",
  "family": "family/<id>",
  "locale": "locale/<registered locale id, e.g. en-in | hinglish | hi-in | as-in>",
  "render_target": "<video | audio_only>",
  "interactions": [
    {
      "interaction_id": "II-<id>",
      "beat_id": "<Script Spec beat id>",
      "slot": "<registered slot hosting the prompt>",
      "itype": "<predict | retrieve_definition | record_formula | reconstruct | draw | complete_missing_step | solve_independently | explain_error | verify | classify | plan_time | read_along | call_response | point_and_say | sing_along | move_along | do_along | discussion_prompt | viva_prompt | critique>",
      "prompt_sentence_ids": ["<sentence ids of the prompt>"],
      "response_modes": ["<think | say_aloud | point | move | draw | write | sing | solve | critique>"],
      "asm_id": "ASM-<id> (or use wrk_step_ref)",
      "wrk_step_ref": "WRK-<id>#<n>",
      "asm_item_kind": "<mcq | short | long | numeric | oral | practical | match | fill_blank | diagram_label | ordering>",
      "mis_ids": ["MIS-<id>"],
      "evaluative": <true | false>,
      "item_presentation": "<mcq | numeric | short_answer | long_answer | diagram_label | ordering | match | fill_blank | oral | practical | none>",
      "window": {
        "kind": "<think | pause-video | call_response>",
        "seconds": {"value": <think: 4–8, default 6 (RD-11); 4 only with `binary_choice: true`; call_response: ≥ 6; pause-video: media hold; null only if Hypothesis>, "tag": "<Inherited | Hypothesis | Recommendation | Evidence>", "source": "<e.g. RD-11>", "owner": "<if Hypothesis>", "pilot_ref": "<if Hypothesis>"},
        "protected": true,
        "prompt_stays_visible": true,
        "narration_stops": true
      },
      "reveal": {
        "trigger": "<window_end (think) | learner_continue (pause-video) | no_single_answer (discussion, critique, sing/move/read/do-along; pause-video allowed)>",
        "reveal_beat_id": "<beat that answers; required unless no_single_answer>",
        "answer_hidden_until_reveal": true,
        "hidden_channels": ["narration", "display", "captions", "overlays", "audio_description", "thumbnail", "preview", "transcript_order"]
      },
      "feedback": {
        "structure": "correct_change_next",
        "conditional": true,
        "sentence_ids": ["<feedback sentence ids>"],
        "branches": [{"error_kind": "<arithmetic | representation | strategy | terminology | prerequisite | misconception>", "mis_id": "MIS-<id, required for misconception>", "sentence_id": "<branch sentence id>"}]
      },
      "accessibility_alternatives": ["<typing | oral | partial_template | choose_from_options | describe_aloud | think_only | larger_view | audio_described | captioned_prompt | seated | point>"],
      "option_labels": [{"option_id": "<ASM option_id, match/diagram_label left item or ordering element>", "screen_reader_label": "<option text and position only; never marks the key>", "keyboard_key": "<1-9 | A-Z, unique in this interaction>"}],
      "binary_choice": <true only for a two-option prediction; omit otherwise>,
      "grown_up_cue_sentence_id": "<AC0 pause-video: the grown-up cue sentence id>",
      "timer_display": "none",
      "item_label": "<past_paper | examleaf_practice_question | diagnostic | none>",
      "marks_display": {"shown": <true only for past_paper with a registered key>, "marks": <n, multiple of 0.5>, "marks_source": "<source_paper | official_key>", "source_id": "SRC-<id>"},
      "exam_source_display": {"board_or_exam": "<board or exam>", "year": <yyyy>, "source_id": "SRC-<id>"},
      "pre_post": {"role": "<pre | post>", "pair_id": "PP-<id>"}
    }
  ],
  "confidence_checkpoints": [
    {"checkpoint_id": "CC-<id>", "beat_id": "<beat>", "kinds": ["followed", "completed_with_support", "solved_without_support"], "prompt_sentence_ids": ["<ids>"], "route_sentence_ids": ["<ids of the specific next actions>"], "self_report_captured_by": "platform"}
  ],
  "spacing": {
    "schedule_ref": "<02 §I4 or the level's calibrated schedule>",
    "tag": "<Inherited | Hypothesis>",
    "owner": "<if Hypothesis>",
    "pilot_ref": "<if Hypothesis>",
    "platform_reminders": <false for AC0>,
    "occasions": [
      {"occasion": "end_of_lesson", "asm_ids": ["ASM-<id>"], "cue_change": "none_same_session", "delivered_by": "video"},
      {"occasion": "<next_day | about_3_days | about_1_week | exam_timed>", "asm_ids": ["ASM-<twin or variant>"], "cue_change": "<new_wording | new_representation | new_values_and_wording | mixed_method_selection>", "delivered_by": "platform"}
    ]
  },
  "platform_boundary": {"adaptive_feedback_in_video": false, "response_capture_in_video": false, "interaction_sidecar_exported": true},
  "safety_constraints": {"no_competition_or_comparison": true, "no_streaks_or_variable_rewards": true, "no_threatening_countdowns": true, "no_data_solicitation": true, "no_links_in_prompts": true},
  "qa_results": [{"check_id": "IQ-01", "result": "<pass | fail | report_only_flag | not_applicable>", "detail": "<optional>"}],
  "provenance": {"author_kind": "<human | model | import>", "author_id": "<id>", "created_at": "<ISO 8601>", "model_id": "<if model>", "effort": "<if model>", "kit_version": "<if model>"}
}
```

## Notes

- Answer-bearing types (predict, retrieve_definition, record_formula, reconstruct, draw, complete_missing_step, solve_independently, explain_error, verify, classify, plan_time, viva_prompt, call_response, point_and_say) need `asm_id` or `wrk_step_ref`; `asm_id` needs `asm_item_kind`.
- `diagram_label` and `ordering` are stored as ASM `diagram_label` and `ordering` (enum extended 15 Oct 2026, CE-67).
- `item_label: past_paper` needs `exam_source_display`; `examleaf_practice_question` can never show marks (CE-31).
- AC0: no `plan_time`, `discussion_prompt`, `viva_prompt`, `critique`, `record_formula` or `explain_error`; `timer_display: none`; no marks; `platform_reminders: false`; only an end_of_lesson occasion delivered_by video; a `move` response lists `seated`; a pause-video window needs `grown_up_cue_sentence_id` (15 Oct 2026).
- Pause matching (schema, 15 Oct 2026): solve_independently, record_formula, reconstruct, draw, plan_time, discussion_prompt, critique and do_along, and any `write` or `draw` response mode, use pause-video. discussion_prompt and critique with `no_single_answer` need at least one `feedback.sentence_ids` entry (the labelled model response).
- `audio_only`: no `diagram_label` or `ordering` presentation and no `point` response mode.
- `option_labels` (level-3+, CE-120, 15 Oct 2026): required when `item_presentation` is `mcq`, `match`, `ordering` or `diagram_label`; one entry per ASM option with a `screen_reader_label` (option text and position only, never marking the key) and a unique `keyboard_key` (`1`–`9` or `A`–`Z`). The exporter copies it into `export/interactions.json` (IQ-15, Q-A11Y.asm_labels).
- `interactions` may be empty only for `format/series` (members carry their own).
- Omit `wrk_step_ref`, `mis_ids`, `binary_choice`, `grown_up_cue_sentence_id`, `marks_display`, `exam_source_display`, `pre_post`, `confidence_checkpoints` and `qa_results` when unused.

## Checklist before GA-Δ

- [ ] Every think and pause-video beat in the Script Spec has a matching interaction here, and every `reveal_beat_id` equals the Script Spec `answers_after` link.
- [ ] Window kind matches the task: simple prediction or binary choice → think (5–8 s, default 6; 4 s only with `binary_choice: true`); writing, drawing, multi-step → pause-video (03 Step 7).
- [ ] Hindi and Hinglish windows are not shorter than the en-IN master for the same `interaction_id` (IQ-14); any extension is tagged Hypothesis with owner and pilot.
- [ ] Feedback branches are conditional and each maps to an ASM or MIS node; no "I heard you", no identity praise.
- [ ] Answer keys verified by the family method (fixture, solver, official scheme or reviewer key) and independently re-solved.
- [ ] Accessibility alternatives listed for every interaction; captions show only the prompt during the window.
- [ ] Every option-bearing interaction has `option_labels` with a key and a screen-reader label per option, and no label gives away the answer (15 Oct 2026).
- [ ] Spacing occasions after the lesson change cues and are delivered by the platform.
- [ ] AC0 and AC1 safety rules hold: no comparison, streaks, countdowns, data requests or links.
