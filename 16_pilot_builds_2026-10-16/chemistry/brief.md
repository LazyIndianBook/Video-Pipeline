# Brief: Chemistry concept intro (Class 10)

- **video_id:** `chem-balance-ci-01`
- **Topic:** Balancing a chemical equation. Hook (ask, do not reveal; the predict beat asks which side is short): "Hydrogen burns in oxygen to make water. Write it down and count the atoms on each side. Something does not add up. Can you spot it?" Teach: atoms are never created or destroyed in a reaction (law of conservation of mass), so the equation must have the same count of each element on both sides; we balance by changing coefficients in front of formulas, never the subscripts inside a formula; H2 + O2 → H2O becomes 2H2 + O2 → 2H2O.
- **Fixture (compute in code):** parse formulas and count atoms: unbalanced left H=2, O=2; right H=2, O=1 (O mismatch). Balanced 2H2 + O2 → 2H2O: left H=4, O=2; right H=4, O=2. Assert both. Display strings for the formulas with subscripts (use Unicode subscript digits ₂ in `display`, or mark the subscript element with `data-fx`), coefficients "2", arrows "→".
- **Level:** `l9_10` (NCERT Class 10 Science, chapter "Chemical Reactions and Equations", section on balanced chemical equations). Register: Super Teacher core variant.
- **Misconception to confront:** "Fix the count by writing H2O2 or changing the subscript." Why wrong: changing a subscript changes the substance (H2O2 is hydrogen peroxide, a different compound); only coefficients may change.
- **Format:** `concept_intro`, 60–70 s, one `check.predict` with a 5 s think window ("Count the oxygen atoms on each side. Which side is short?"), one `misconception.confront`, a `recap.statement`, the `outro.disclosure` beat.
- **Style:** `editorial-vox` (clean editorial layout, strong type, calm colour, atom counters as tally marks and circles; no flashes).
- **Scenes:** 4–5 (hook with the unbalanced equation; predict pause; atom-count tally from the fixture; the subscript trap; recap + disclosure).
- **Voice:** Path B, ElevenLabs `eleven_v4`, premade voice George (`JBFqnCBsd6RMkjVDRZzb`), English. The lead narrates per beat.
- **Character budget:** 1,000 characters of spoken text in total.
- **Tooling python:** `/private/tmp/claude-501/-Users-chinmoybhuyan-Desktop-Personal-Book-Videos/e7dd322a-a174-4149-805e-5961efcb1de7/scratchpad/narr_venv/bin/python`
