# SCENE PEDAGOGY SCHEMA and release review (blueprint section 13, in full)

> **Provenance.** Verbatim extract of section 13 of `FULL_learning_psychology_blueprint.md` (ChatGPT message 04). Only cleaning: citation tokens removed. Nothing shortened.
> **Evidence label:** this is a production requirement derived from the research ("Convert the psychology into production requirements"); it is a proposed standard, not a validated one. The source also states automated checks "cannot determine scientific validity or genuine student learning from visual polish alone."
> Where the schema is implemented: `04_video_engine` (scene model) and `07_end_to_end_pipeline_instructions`; the Skills that should enforce it live in `06_skills_library`.

---

# 13. Convert the psychology into production requirements

The ExamLeaf Video Engine should store pedagogical intent alongside its visual and audio instructions.

| Scene field | What it records |
|---|---|
| Learning objective | The capability this scene supports |
| Prerequisite | What the student must already know |
| Scientific relationship | The verified claim or model being explained |
| Attention target | The object or relationship that should dominate |
| Representation | Diagram, equation, graph, process state, or example |
| Learner action | Observe, predict, explain, write, draw, solve, or retrieve |
| Available support | Full example, partial hint, or independent task |
| Answer visibility | Whether the answer must remain hidden |
| Pause mode | Brief built-in silence or learner-controlled pause |
| Feedback | What a correct or incorrect attempt should lead to |
| Misconception | The specific incorrect interpretation being addressed |
| Delayed assessment | How this capability will later be tested |

### Release review should answer four questions

**Scientific:** Is every claim, diagram, transformation, condition, and answer correct?

**Instructional:** Does the learner get an opportunity to perform the target task without the explanation doing it for them?

**Perceptual:** Can the essential content be read and followed on the intended devices, with captions and audio working together?

**Emotional:** Are the challenges fair, feedback specific, and confidence statements honest?

Automated checks can flag contrast, text size, clipping, answer-reveal timing, missing units, absent captions, or suspiciously dense scenes. They cannot determine scientific validity or genuine student learning from visual polish alone.

## The recommended ExamLeaf standard

Build each lesson around:

> **One clear purpose, a small number of connected ideas, a stable visual model, explicit reasoning, meaningful student attempts, useful feedback, and a later opportunity to retrieve the learning.**

The strongest brand promise is not that ExamLeaf makes every topic feel effortless.

It is that **students can see what they understand, discover what still needs work, and become progressively more capable of answering without ExamLeaf beside them.**

---

## Organiser addendum (NOT in the source): how to use the 12 fields

### 1. Illustrative scene record
One beat of the Ohm's-law blueprint (03:00-03:12, Major pause 1) expressed with the twelve source fields. The field names are the source's "Scene field" column in snake_case; the *values* are taken from the blueprint; the JSON syntax is only an illustration (the canonical scene schema belongs to `04_video_engine`).

```json
{
  "learning_objective": "State V=IR / I=V/R and the condition under which it is used, from memory",
  "prerequisite": "Current, potential difference and their units (reactivated at 00:30-00:45)",
  "scientific_relationship": "For an ohmic resistor under constant relevant physical conditions, I = V/R",
  "attention_target": "The blank note area where the learner writes the relationship and its condition",
  "representation": "equation",
  "learner_action": "write",
  "available_support": "independent task (completed formula hidden)",
  "answer_visibility": "hidden until after the learner-controlled pause",
  "pause_mode": "learner-controlled pause (Major pause 1)",
  "feedback": "Reveal a model response highlighting relationship, unit information and condition (03:12-03:30); learner compares and repairs the note",
  "misconception": "That the rule applies universally, regardless of conditions",
  "delayed_assessment": "Next-day recall of the law with its condition; 7-day unprompted assessment item on an unfamiliar application"
}
```

### 2. Field-to-rule trace (which rules in `INSTRUCTIONS_production_rules.md` each field enforces)
| Scene field | Enforces |
|---|---|
| Learning objective, Prerequisite | B3 (establish symbols, changing/constant quantities, target), J (weak prior knowledge) |
| Scientific relationship | Release review "Scientific"; E5 (subject-specific visual rules) |
| Attention target | B2 (one dominant explanatory focus), D4 (one dominant highlight) |
| Representation | E1 (animation decision table) |
| Learner action, Available support | C3 (worked-example progression), F2-F3 (interaction pattern and menu) |
| Answer visibility, Pause mode | F1 (pause specification), F7 (learner-controlled "Continue to explanation"), G3 (pause lengths) |
| Feedback | H3 (feedback scripts, conditional wording) |
| Misconception | I3 (misconception-correction sequence) |
| Delayed assessment | I4 (spacing schedule), AB_EXPERIMENTS_and_EVALUATION.md (primary outcome) |

### 3. Automated vs human review (from the source's last paragraph of section 13)
- **Automatable flags:** contrast, text size, clipping, answer-reveal timing, missing units, absent captions, suspiciously dense scenes.
- **Human only:** scientific validity (Scientific question), whether the learner really gets to perform the task (Instructional), fairness of challenge, specificity of feedback and honesty of confidence statements (Emotional). Subject reviewers must also check the subject-specific visual rules (E5), "not inferred from whether the animation looks convincing."
