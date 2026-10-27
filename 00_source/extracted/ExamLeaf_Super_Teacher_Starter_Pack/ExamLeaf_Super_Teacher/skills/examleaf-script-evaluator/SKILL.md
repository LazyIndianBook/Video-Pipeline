---
name: examleaf-script-evaluator
description: Evaluate an ExamLeaf script for regressions, naturalness, accessibility and actual learning opportunities.
---

# examleaf-script-evaluator

Read `references/authoring_contract.md` before working.

## Inputs
Current script, approved prior scripts, test corpus, source reviews and any learner-study results.

## Workflow
Run structural checks, then perform a qualitative read-aloud review. Track repeated opening forms, analogy families, jokes and closures across the recent catalogue; do not replace accurate technical terms merely for novelty. Check that timing includes pauses and that prompt answers are hidden. Report separately: science blockers, learner-action failures, naturalness observations and research hypotheses. Compare the voice-only, visual-only and combined experience. Design content-matched or time-matched learner tests explicitly, with immediate and delayed unprompted outcomes and confidence calibration. Small usability tests do not establish causal effectiveness. Never claim model evaluation proves teenagers will enjoy a joke.

## Outputs
release_review.md; regression_report.json; experiment_plan.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
