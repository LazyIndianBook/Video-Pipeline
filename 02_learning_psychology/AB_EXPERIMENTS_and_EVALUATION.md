# A/B EXPERIMENTS and EVALUATION (blueprint section 12, in full)

> **Provenance.** Verbatim extract of section 12 of `FULL_learning_psychology_blueprint.md` (ChatGPT message 04). Only cleaning: citation tokens removed. Nothing shortened.
> **Evidence label (source's words):** the 7-day delay is "a study-design choice, not the only valid measure of retention"; sample sizes are "approximate planning calculations, not a power analysis for a finished study".

---

# 12. A/B experiments that can establish what works for ExamLeaf

## 12.1 Choose learning outcomes before choosing variants

The recommended primary outcome is:

> **Performance on a delayed, unprompted assessment containing unfamiliar but curriculum-aligned applications.**

A practical initial delay is seven days; that interval is a study-design choice, not the only valid measure of retention.

Secondary outcomes should include immediate understanding, task completion without hints, confidence calibration, total study time, listening effort, and voluntary return to useful practice.

Watch time should remain a diagnostic measure.

## 12.2 Prioritized experiments

| Priority | Comparison | Main question |
|---|---|---|
| **1** | Explanation-only versus explanation plus retrieval and feedback | Does the active version improve delayed performance enough to justify additional study time? |
| **2** | Full worked examples throughout versus gradually faded support | Does fading improve independent method selection? |
| **3** | Fewer substantial checkpoints versus more frequent brief checkpoints | Which pattern benefits learning without excessive interruption? |
| **4** | Clear static sequence versus semantically equivalent animation | Does motion improve understanding of this particular relationship? |
| **5** | Approximately 130 versus 150 wpm with the same substantive explanation | Who benefits from each pace, and what happens to study time and comprehension? |
| **6** | Specific task feedback versus generic but respectful feedback | Does specificity improve error correction and calibration? |
| **7** | Learner-controlled pause versus automatic answer reveal | Do students actually attempt the task, and does delayed learning improve? |
| **8** | Copying a compact reference versus reconstruction followed by checking | Which produces better later retrieval for the time invested? |
| **9** | Two accessible, aesthetically coherent palettes | Are there meaningful differences in reading accuracy and comfort? |

Do not test an unreadable palette against a readable one and label the result “colour psychology.”

## 12.3 Design the comparisons carefully

Randomly assign learners or classes as appropriate. Record prior knowledge, class level, language proficiency, and device conditions before interpreting group differences.

Keep scientific content and assessment difficulty equivalent. Decide whether the experiment is **content-matched** or **time-matched**: adding practice usually adds study time, while increasing speech rate changes runtime unless another element is adjusted.

Use parallel test items rather than showing the identical question repeatedly. Have written responses scored with a predefined rubric, preferably without the marker knowing which version the student watched.

Predefine the main outcome and analysis. Report attrition, confidence intervals, and all planned comparisons rather than selecting whichever metric looks favourable.

For experiments involving minors, use age-appropriate informed participation, necessary permissions, minimal data collection, and no intrusive emotion or attention surveillance.

## 12.4 Sample size: distinguish usability from efficacy

A small group can reveal that a graph label is unreadable. It cannot reliably establish a modest learning advantage.

As an illustrative calculation, a conventional two-group comparison targeting a standardized difference of **0.30**, with 80% power and a two-sided 5% significance level, requires approximately **175 independent learners per group** before allowing for attrition. A difference of **0.20** requires roughly **400 per group**.

These are approximate planning calculations, not a power analysis for a finished study. Classroom clustering, repeated observations, baseline adjustment, measurement reliability, and missing data change the requirement.

Begin with a small, diverse usability study; then run a properly powered learning study on the most consequential design decision.

## 12.5 Measure confidence calibration—not merely confidence increases

At selected checkpoints, ask students to estimate whether their answer is correct before seeing feedback.

Then distinguish:

**Accurate confidence**, **high-confidence errors**, and **correct answers accompanied by excessive uncertainty**.

A variant that makes students feel highly confident while increasing errors should lose—even when they prefer it.

Conversely, a useful variant should not unnecessarily leave successful students believing they are incapable.


---

## Organiser notes (NOT in the source; added for implementers)

1. **Sample-size arithmetic re-checked.** Using n per group = 2 x (1.96 + 0.8416)^2 / d^2 (two-sided alpha = 0.05, power = 80%): d = 0.30 gives 174.4 (source: "approximately 175"); d = 0.20 gives 392.4 (source: "roughly 400"). The source figures are consistent with the standard formula. Cluster/classroom effects, baseline adjustment, attrition and measurement reliability (which the source says change the requirement) are not modelled.
2. **Where each experiment plugs into the pipeline.** Experiments 1, 3, 7 and 8 change interaction design (`02_learning_psychology/INSTRUCTIONS_production_rules.md` section F); 2 changes the worked-example progression (section C); 4 changes the animation decision (section E); 5 changes narration pace (section G); 6 changes the feedback scripts (section H); 9 changes the palette (section D). Experiment 9 must compare two *accessible* palettes (see palette in `palette_and_typography_tokens.json`); the source says not to compare an unreadable palette with a readable one.
3. **Order of work (from the source's own priority column):** start with a small diverse usability study (legibility, clipping, caption fit on phones), then run one properly powered learning study on the most consequential design decision (priority 1: explanation-only vs explanation plus retrieval and feedback).
4. **Primary outcome reminder:** delayed (initially 7 days), unprompted assessment with unfamiliar but curriculum-aligned applications; watch time stays a diagnostic measure only.
5. See `10_pilots_and_examples` for pilot lessons that can host these comparisons and `09_research_and_evidence` for the evidence ledger.
