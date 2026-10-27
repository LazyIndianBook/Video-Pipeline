# Brief: Physics concept intro (Class 10)

- **video_id:** `phy-ohm-ci-01`
- **Topic:** Ohm's law. Hook: "Does twice the voltage always mean twice the current?" Teach: for an ohmic conductor at constant temperature, current is proportional to the potential difference; resistance is the constant of proportionality; the one condition that makes the rule work; a filament bulb heats up and is not ohmic, so the rule fails there.
- **Fixture (compute in code):** R = 10 Ω; V1 = 2 V → I1 = 0.2 A; V2 = 4 V → I2 = 0.4 A; ratio I2/I1 = 2; V/I constant = 10 Ω at both points. Assert each. Display labels: "R =", "Ω", "V =", "V", "I =", "A".
- **Level:** `l9_10` (Class 10 NCERT Science, chapter "Electricity", section "Ohm's law"). Register: Super Teacher core variant; voltage equals current multiplied by resistance (not "V equals I R" shorthand at this level); no calculus, no microscopic model.
- **Misconception to confront:** "Ohm's law is universal; doubling voltage always doubles current." Why wrong: resistance of many components changes with temperature (filament lamp), so the proportionality holds only while R stays constant.
- **Format:** `concept_intro`, 60–70 s, one `check.predict` with a 5 s think window ("Predict the current at four volts, and decide whether 'always' is safe"), one `misconception.confront`, a `recap.statement`, the `outro.disclosure` beat.
- **Style:** `doodle-handdrawn` (hand-drawn circuit: cell, resistor, ammeter; marker-stroke lines; paper texture must be decorative only).
- **Scenes:** 4–5 (hook circuit; predict pause; the ratio reveal with both readings from the fixture; the filament exception; recap + disclosure).
- **Voice:** Path B, ElevenLabs `eleven_v4`, premade voice George (`JBFqnCBsd6RMkjVDRZzb`), English. The lead narrates per beat.
- **Character budget:** 1,000 characters of spoken text in total.
- **Tooling python:** `/private/tmp/claude-501/-Users-chinmoybhuyan-Desktop-Personal-Book-Videos/e7dd322a-a174-4149-805e-5961efcb1de7/scratchpad/narr_venv/bin/python`
