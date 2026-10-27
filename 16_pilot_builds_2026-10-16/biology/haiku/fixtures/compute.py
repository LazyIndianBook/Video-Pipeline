#!/usr/bin/env python3
"""compute.py: fixture for bio-photosyn-ci-01 (photosynthesis atom balance and glucose carbon mass fraction).

Plain Python 3, standard library only. Prints the fixture JSON to stdout and writes fixtures/fixture.json next to
this file. Every number the script speaks is asserted here before it is written.
"""
import json
import pathlib
from collections import Counter

# Integer atomic masses, as the brief specifies (C = 12, H = 1, O = 16).
ATOMIC_MASS = {"C": 12, "H": 1, "O": 16}

# Molecular formulas as element counts per molecule.
CO2 = {"C": 1, "O": 2}
H2O = {"H": 2, "O": 1}
GLUCOSE = {"C": 6, "H": 12, "O": 6}
O2 = {"O": 2}

# Coefficients of 6CO2 + 6H2O -> C6H12O6 + 6O2.
COEF_CO2, COEF_H2O, COEF_GLUCOSE, COEF_O2 = 6, 6, 1, 6


def count_atoms(terms):
    """terms: list of (coefficient, {element: count}); returns Counter of atoms."""
    total = Counter()
    for coef, comp in terms:
        for el, n in comp.items():
            total[el] += coef * n
    return total


def main():
    left = count_atoms([(COEF_CO2, CO2), (COEF_H2O, H2O)])
    right = count_atoms([(COEF_GLUCOSE, GLUCOSE), (COEF_O2, O2)])

    # Atom balance: every element must have the same count on both sides.
    for el in ("C", "H", "O"):
        assert left[el] == right[el], f"atom balance fails for {el}: {left[el]} vs {right[el]}"
    assert left["C"] == 6 and right["C"] == 6
    assert left["H"] == 12 and right["H"] == 12
    # Oxygen: 12 (from 6 CO2) + 6 (from 6 H2O) = 18 on the left; 6 (in glucose) + 12 (in 6 O2) = 18 on the right.
    # The brief's earlier figure of 24 is wrong; the balanced count is 18.
    assert left["O"] == 18 and right["O"] == 18

    glucose_molar_mass = sum(ATOMIC_MASS[el] * n for el, n in GLUCOSE.items())
    carbon_mass_glucose = ATOMIC_MASS["C"] * GLUCOSE["C"]
    assert glucose_molar_mass == 180
    assert carbon_mass_glucose == 72
    fraction = carbon_mass_glucose / glucose_molar_mass
    assert abs(fraction - 0.4) < 1e-12
    carbon_percent = round(fraction * 100)   # exact integer here (72/180 = 0.4), stored as an int so display text matches
    assert carbon_percent == 40 and isinstance(carbon_percent, int)

    fixture = {
        "_note": "Computed by fixtures/compute.py for bio-photosyn-ci-01. Do not edit by hand; re-run the script.",
        "display": {
            "co2": "CO₂",
            "h2o": "H₂O",
            "glucose": "C₆H₁₂O₆",
            "o2": "O₂",
            "plus": "+",
            "arrow": "→",
            "sunlight": "sunlight",
            "chlorophyll": "chlorophyll",
            "elem_C": "C",
            "elem_H": "H",
            "elem_O": "O",
            "carbon_word": "carbon",
            "soil": "soil",
            "water": "water",
            "air": "air",
            "equals": "=",
            "percent_sign": "%",
            "ui": {
                "think_prompt": "Pause. Predict."
            }
        },
        "parameters": {
            "coef_co2": COEF_CO2,
            "coef_h2o": COEF_H2O,
            "coef_glucose": COEF_GLUCOSE,
            "coef_o2": COEF_O2,
            "atomic_mass_C": ATOMIC_MASS["C"],
            "atomic_mass_H": ATOMIC_MASS["H"],
            "atomic_mass_O": ATOMIC_MASS["O"]
        },
        "results": {
            "atoms_left_C": left["C"],
            "atoms_right_C": right["C"],
            "atoms_left_H": left["H"],
            "atoms_right_H": right["H"],
            "atoms_left_O": left["O"],
            "atoms_right_O": right["O"],
            "glucose_molar_mass": glucose_molar_mass,
            "carbon_mass_glucose": carbon_mass_glucose,
            "carbon_mass_percent_glucose": carbon_percent
        }
    }

    out = pathlib.Path(__file__).resolve().parent / "fixture.json"
    text = json.dumps(fixture, ensure_ascii=False, indent=2) + "\n"
    out.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
