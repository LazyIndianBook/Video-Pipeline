# EXAMPLE - Textbook reading versus ExamLeaf teaching narration

This file has two parts: Part A is the chat answer's section 8 (verbatim); Part B is the narration pack's `examples/Before_After.md` (verbatim, also copied byte-for-byte to `narration_examples/Before_After.md`).

## Part A - message 12 section 8 (chat answer)

> Provenance note: the body below is copied verbatim from the ChatGPT transcript (`12_ASSISTANT_narration_system.md`, lines 346-400). The invisible private-use characters around `cite...turn...` markers are ChatGPT citation placeholders and are left in place so the text stays byte-identical to the source. Nothing here has been re-verified by a human teacher.

---

# 8. Script example: textbook reading versus teaching

The scientific target is the distinction between a coefficient and a subscript in a chemical equation. Changing coefficients adjusts quantities; changing the specified formula changes the chemical representation. citeturn676449view5

*The citation above concerns the tool project rather than chemistry and should not be used to establish the chemistry claim; the complete example’s scientific source is recorded in the downloadable script.*

## Textbook version

> “A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms.”

This is clear factual narration. It is not necessarily badly voiced. Its weakness is that it provides little help in constructing or testing the learner’s understanding.

## ExamLeaf version

**CURIOUS**

> “Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.”

*Show two intact water molecules. Keep totals hidden. Insert six seconds of actual silence after the question audio ends.*

**DELIBERATE**

> “Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules—not what a molecule is.”

*Reveal the hydrogen count when it is spoken. Highlight the coefficient when it is named.*

**LIGHT**

> “Changing water into hydrogen peroxide would be a very efficient way to answer a different question.”

*Show the rejected change separately and clearly label it.*

**FOCUSED**

> “Keep the given formulas fixed. Use coefficients to change the counts.”

**REASSURING**

> “Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.”

*Allow a learner-controlled pause. Do not treat the short media hold as a deadline.*

**FOCUSED**

> “Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.”

[**Read the full before-and-after example and directions**](sandbox:/mnt/data/ExamLeaf_Narration_System/examples/Before_After.md)

### Why this version is more useful

The proposed script separates counts, creates a genuine attempt, explains the error, and checks a new case. The humour reinforces the identity-versus-quantity distinction.

Its value should be measured through the next independent question—not simply whether students preferred the voice.

---

---

## Part B - narration pack `examples/Before_After.md` (verbatim)

# One scientific explanation, two narration styles

These are original scripts about coefficients and molecular composition. They are not a complete lesson. Exact seconds below are director targets until final audio is measured. The generated Runway auditions demonstrate the contrast but differ in length and wording; they are not a controlled provider or learning benchmark.

## Textbook version
A balanced chemical equation contains equal numbers of atoms of each element on the reactant and product sides. Balancing is performed by changing coefficients, not the subscripts in the specified chemical formulas. Two water molecules contain four hydrogen atoms and two oxygen atoms. Verification requires counting each element on both sides.

Direction: neutral, clear. Visual: equation and counts. No deliberately degraded pronunciation or robotic effect.

## ExamLeaf version
CURIOUS — Two water molecules. How many hydrogen atoms altogether? Count each complete molecule before you answer.

[Keep two intact water molecules visible. Hide totals. After the question audio ends, insert six seconds of genuine silence.]

DELIBERATE — Four hydrogen atoms. Each water molecule contains two, and we have two complete copies. That is what the coefficient changes: how many molecules, not what a molecule is.

[Reveal four hydrogen atoms when the phrase begins. Highlight the coefficient only when it is named.]

LIGHT — Changing water into hydrogen peroxide would be a very efficient way to answer a different question. Keep the given formulas fixed. Use coefficients to change the counts.

[Show a rejected proposed formula separately and clearly label it. Restore water. No laughing sound effect.]

REASSURING — Your turn again: three water molecules. How many hydrogen atoms, and how many oxygen atoms? Pause here and write both counts.

[Five-second default media hold, plus explicit student-controlled pause. This is not a five-second deadline.]

FOCUSED — Six hydrogen atoms and three oxygen atoms. If those match, check the method too: the number of copies multiplies every atom count in the formula.

The machine-readable version is teacher.json. Actual live audition B was one provider take with expressive tags, not the sample-exact classroom hold implementation.

Scientific basis: https://openstax.org/books/chemistry-2e/pages/4-1-writing-and-balancing-chemical-equations
