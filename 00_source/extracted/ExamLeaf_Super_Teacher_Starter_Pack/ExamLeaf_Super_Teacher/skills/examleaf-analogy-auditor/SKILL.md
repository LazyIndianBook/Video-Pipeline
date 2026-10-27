---
name: examleaf-analogy-auditor
description: Create or audit a scientific analogy without letting the analogy imply false science.
---

# examleaf-analogy-auditor

Read `references/authoring_contract.md` before working.

## Inputs
Target concept, learner familiarity, candidate analogy, formal model and sources.

## Workflow
Create an analogy card: target_relation, familiar_relation, mapping, non_mapping, likely_misconception, formal_return, learner_check. Compare at least two possible analogies, including no analogy. Choose the least complex one that explains the relationship. State the limit aloud where the wrong inference is likely. Reject analogies that need more background than the target concept, equate unlike quantities, or imply organisms and particles act with intentions. Require the learner to explain the scientific relation without the story at the end.

## Outputs
analogy_cards.json; rejected_analogies.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
