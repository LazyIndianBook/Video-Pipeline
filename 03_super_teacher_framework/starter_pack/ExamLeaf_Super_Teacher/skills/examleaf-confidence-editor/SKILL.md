---
name: examleaf-confidence-editor
description: Replace empty praise and anxiety-inducing wording with evidence-specific, respectful teaching feedback.
---

# examleaf-confidence-editor

Read `references/authoring_contract.md` before working.

## Inputs
Script, anticipated student errors, answer rubric and evidence level.

## Workflow
Inspect every claim about the learner, every success message and every correction. Rewrite feedback as observed/conditional success, specific issue and actionable next step. Use “your choice of relationship is correct” only when actual input supports it, or phrase it conditionally in video. Separate arithmetic, representation, strategy, terminology and prerequisite errors. Remove “easy”, “obvious”, score promises and intelligence judgments where they shame or overclaim. Preserve warmth without fabricated intimacy. End with a self-check and a fresh task, not a declaration that viewing equals mastery. Keep persistent anxiety outside the scope of a teaching-video cure.

## Outputs
feedback_edits.md; confidence_checks.json

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
