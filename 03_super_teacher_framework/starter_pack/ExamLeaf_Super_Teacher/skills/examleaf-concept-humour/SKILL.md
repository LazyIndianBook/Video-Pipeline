---
name: examleaf-concept-humour
description: Generate or review original, teenager-appropriate humour tied to a particular learning point.
---

# examleaf-concept-humour

Read `references/authoring_contract.md` before working.

## Inputs
Approved explanation, exact misconception, audience/language profile and used-joke ledger.

## Workflow
Offer up to three short candidates and a no-joke alternative. For each record concept_anchor, comedic_mechanism, literal_science_risk, translation_risk, narration_seconds and follow-up scientific sentence. Prefer dry observation, a gentle contrast, or a short callback. Do not require a quota. Reject identity-targeted ridicule, teacher imitation, political or relationship bait, sarcasm whose literal reading teaches the wrong answer, unlicensed meme clips and generic motivational rhymes. Put the joke after clarity, or use it to expose the exact wrong turn; never over the first dense derivation. Recheck that the next remembered sentence is the scientific one.

## Outputs
humour_candidates.json; chosen_edits.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
