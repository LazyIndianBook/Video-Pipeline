---
name: examleaf-interaction-designer
description: Create genuine prediction, retrieval and practice moments for prerecorded or interactive lessons.
---

# examleaf-interaction-designer

Read `references/authoring_contract.md` before working.

## Inputs
Lesson objectives, script, answer keys, player type and timing budget.

## Workflow
Distinguish rhetorical questions from learner-response prompts. Each learner prompt needs expected_answer, acceptable_variations, available_hint, reveal_trigger, estimated_task_time, feedback and retry. Use a few meaningful checkpoints, not questions on every sentence. Reserve learner-controlled pauses for writing, drawing and multi-step work. During such tasks stop new narration. Keep answers hidden across diagram, captions and overlays. Prerecorded feedback is conditional; actual answer-dependent branches require recorded input and a verified rule. Do not count copying as retrieval. Select tasks appropriate to the subject, rather than forcing all activity types into every lesson.

## Outputs
interactions.json; timing_changes.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
