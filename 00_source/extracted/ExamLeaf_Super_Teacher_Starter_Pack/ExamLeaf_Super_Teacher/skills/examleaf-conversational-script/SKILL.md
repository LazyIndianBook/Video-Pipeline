---
name: examleaf-conversational-script
description: Draft or rewrite source-grounded educational narration into the original ExamLeaf teacher voice.
---

# examleaf-conversational-script

Read `references/authoring_contract.md` before working.

## Inputs
Approved lesson brief, claim ledger, answer keys, analogy cards and recent script ledger.

## Workflow
Write for a single teenage viewer, not for a textbook or an auditorium. Keep the scientific relationships fixed while rewriting their explanation. State why each step is chosen. Prefer concrete verbs, short clauses, natural contractions and purposeful question-answer turns. Include exact exam terminology after the plain-language explanation. Write every spoken word; do not replace difficult teaching with placeholders. Separate narration from stage directions. Do not fabricate memories, an audible student, spontaneous errors or named-teacher impersonation. Return meaningful alternative openings, choose one, and explain the choice briefly. Keep humour optional and secondary.

## Outputs
script.md; beat_plan.json; change_log.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
