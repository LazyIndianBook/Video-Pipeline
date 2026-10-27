---
name: examleaf-science-reviewer
description: Independently verify the scientific claims, examples and implications in a finished ExamLeaf script.
---

# examleaf-science-reviewer

Read `references/authoring_contract.md` before working.

## Inputs
Script, claim ledger, source packet, equations, visual specification and answer keys.

## Workflow
Re-solve the examples without relying on the author answer. Check conditions, signs, units, domains, atom and charge counts, diagram directions, biological compartments and declared simplifications as applicable. Review what humour and analogy imply literally. Check intermediate states, not only the final answer. Distinguish balanced equations from plausible reactions, schematic motion from mechanism and authored exam wording from official rubrics. Return critical/major/minor findings with scene IDs, source support and a minimal repair. Do not use an aggregate score to pass a critical error. Human approval remains separate from this agent review.

## Outputs
science_review.json; independently_solved_answers.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
