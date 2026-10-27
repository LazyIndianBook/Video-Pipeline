#!/usr/bin/env python3
"""Fixture for bio-photosyn-ci-01. Counts atoms of 6CO2 + 6H2O -> C6H12O6 + 6O2 from the formulas in code,
asserts the balance, and computes the carbon mass fraction of glucose from integer atomic masses.
Prints the fixture JSON and writes fixtures/fixture.json next to this file. Stdlib only."""
import json, pathlib, re
from fractions import Fraction

ATOMIC_MASS = {"C": 12, "H": 1, "O": 16}          # integer atomic masses (brief; NCERT-level rounding)
REACTANTS = [(6, "CO2"), (6, "H2O")]
PRODUCTS = [(1, "C6H12O6"), (6, "O2")]


def atoms(formula):
    out = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        out[el] = out.get(el, 0) + (int(n) if n else 1)
    return out


def side(terms):
    tot = {}
    for coef, f in terms:
        for el, n in atoms(f).items():
            tot[el] = tot.get(el, 0) + coef * n
    return tot


def molar_mass(formula):
    return sum(ATOMIC_MASS[el] * n for el, n in atoms(formula).items())


left, right = side(REACTANTS), side(PRODUCTS)
glucose = atoms("C6H12O6")
c_mass = ATOMIC_MASS["C"] * glucose["C"]
g_mass = molar_mass("C6H12O6")
frac = Fraction(c_mass, g_mass)
carbon_in_reactants_by_formula = {f: atoms(f).get("C", 0) for _, f in REACTANTS}

# Every number the script speaks or the scenes show is asserted here.
assert left == right, (left, right)                                   # equation balances
assert left == {"C": 6, "O": 18, "H": 12}                             # C 6/6, H 12/12, O 18/18 (brief said O 24/24: wrong, 12 + 6 = 18)
assert (left["C"], right["C"]) == (6, 6)                              # "six atoms on each side"
assert carbon_in_reactants_by_formula == {"CO2": 1, "H2O": 0}         # water carries no carbon: all reactant carbon is in CO2
assert 6 * carbon_in_reactants_by_formula["CO2"] == left["C"]         # "every one arrived as carbon dioxide"
assert (c_mass, g_mass) == (72, 180)
assert frac == Fraction(2, 5)                                         # 72/180 = 0.4
assert round(float(frac) * 100) == 40                                 # "about forty percent"
assert [c for c, _ in REACTANTS] + [PRODUCTS[1][0]] == [6, 6, 6]      # coefficients shown and spoken as "six"

fixture = {
    "fixture_id": "FIX-photosyn-balance",
    "compute": "fixtures/compute.py",
    "display": {
        "co2": "CO₂", "h2o": "H₂O", "glucose": "C₆H₁₂O₆", "o2": "O₂",
        "plus": "+", "arrow": "→", "equals": "=", "slash": "/",
        "sunlight": "sunlight", "chlorophyll": "chlorophyll",
        "carbon_symbol": "C", "percent": "%",
    },
    "parameters": {
        "coef_co2": REACTANTS[0][0], "coef_h2o": REACTANTS[1][0], "coef_glucose": PRODUCTS[0][0], "coef_o2": PRODUCTS[1][0],
        "atomic_mass": ATOMIC_MASS,
    },
    "results": {
        "atoms_left": left, "atoms_right": right, "balanced": left == right,
        "carbon_left": left["C"], "carbon_right": right["C"],
        "carbon_atoms_in_co2_per_molecule": carbon_in_reactants_by_formula["CO2"],
        "carbon_atoms_in_h2o_per_molecule": carbon_in_reactants_by_formula["H2O"],
        "glucose_carbon_mass": c_mass, "glucose_molar_mass": g_mass,
        "carbon_mass_fraction": float(frac), "carbon_percent": round(float(frac) * 100),
    },
}

text = json.dumps(fixture, ensure_ascii=False, indent=1)
(pathlib.Path(__file__).resolve().parent / "fixture.json").write_text(text + "\n", encoding="utf-8")
print(text)
