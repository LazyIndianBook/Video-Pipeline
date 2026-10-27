---
name: examleaf-voice-director
description: Prepare clean narration and provider-neutral performance cues for ExamLeaf voice production.
---

# examleaf-voice-director

Read `references/authoring_contract.md` before working.

## Inputs
Approved script, pronunciation lexicon, chosen provider/model capabilities and shot/scene IDs.

## Workflow
Separate spoken_text, display_text, tone, emphasis, pause and visual_event fields. Use one stable narrator voice with local energy changes at conceptual turns. Spell out ambiguous formulas, units and chemical coefficients; preserve academic notation on screen. Avoid laughter over instructions, fake gasps and every-line emotion tags. Write a short performance brief and a native language pronunciation audition. Map only documented controls to the selected voice engine. Unknown controls must fail validation, not be spoken accidentally. Exact waits and reveals belong to the renderer. Measure generated audio; edit scope or wording instead of blindly speeding it up.

## Outputs
narration.txt; performance.json; pronunciation_review.md

## Acceptance and escalation
Every new scientific claim must have source support or be explicitly marked for review. Maintain immutable IDs for unchanged claims and scenes. Never silently change the model to improve comedy, fluency or timing. Stop release on a critical scientific, accessibility or deceptive-personalization issue. This Skill gives instructions; it is not a permission or publication boundary.

## Evaluation
See `evals/evals.json` for a negative test. Model runs have not been executed in this starter pack. Human read-aloud and student validation are still required.
