#!/usr/bin/env python3
"""Fixture for phy-ohm-ci-01 (Ohm's law). Plain Python 3, no third-party imports.

Computes the two readings of one resistor, the ratios, and asserts every value the script speaks.
Prints the fixture JSON to stdout and writes fixtures/fixture.json (same folder as this file).
"""
import json
import pathlib

OHM = "Ω"  # Greek capital omega, the unit sign used in the brief

parameters = {"resistance_ohm": 10, "v1": 2, "v2": 4}
R = parameters["resistance_ohm"]
V1 = parameters["v1"]
V2 = parameters["v2"]

I1 = V1 / R   # 0.2 A
I2 = V2 / R   # 0.4 A

results = {
    "i1_a": round(I1, 6),
    "i2_a": round(I2, 6),
    "ratio_i2_over_i1": round(I2 / I1, 6),
    "v1_over_i1_ohm": round(V1 / I1, 6),
    "v2_over_i2_ohm": round(V2 / I2, 6),
}

# Whole-number results are stored as integers so the on-screen text matches the fixture text exactly (10, not 10.0).
results = {k: (int(v) if float(v).is_integer() else v) for k, v in results.items()}

# Every value the script speaks, checked here (spoken: 0.2 A, 0.4 A, twice, ten ohms).
assert results["i1_a"] == 0.2, results
assert results["i2_a"] == 0.4, results
assert results["ratio_i2_over_i1"] == 2.0, results
assert results["v1_over_i1_ohm"] == 10.0, results
assert results["v2_over_i2_ohm"] == 10.0, results
assert V2 / V1 == results["ratio_i2_over_i1"], "doubling the voltage must double the current here"

display = {
    "r_label": "R =",
    "r_unit": OHM,
    "v_label": "V =",
    "v_unit": "V",
    "i_label": "I =",
    "i_unit": "A",
    "ratio_label": "V / I =",
    "ui": {"think_prompt": "Pause. Predict."},
}

fixture = {
    "fixture_id": "FIX-ohm-readings",
    "display": display,
    "parameters": parameters,
    "results": results,
}

text = json.dumps(fixture, ensure_ascii=False, indent=2)
(pathlib.Path(__file__).resolve().parent / "fixture.json").write_text(text + "\n", encoding="utf-8")
print(text)
