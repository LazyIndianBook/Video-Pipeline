#!/usr/bin/env python3
"""Fixture for phy-ohm-ci-01 (Ohm's law, Class 10). Plain Python 3, no third-party imports.

Writes fixture.json next to this file and prints it. Every value the script speaks is asserted below.
ponytail: single resistor, two readings; no general solver. Ceiling: a 3rd reading would need a loop.
"""
import json
import pathlib

OHM = "Ω"
parameters = {"resistance_ohm": 10, "v1": 2, "v2": 4}
R, V1, V2 = parameters["resistance_ohm"], parameters["v1"], parameters["v2"]

I1 = V1 / R          # 0.2 A
I2 = V2 / R          # 0.4 A
ratio = I2 / I1      # 2.0
vi1 = V1 / I1        # 10 ohm
vi2 = V2 / I2        # 10 ohm

results = {
    "i1_a": round(I1, 6),
    "i2_a": round(I2, 6),
    "ratio_i2_over_i1": round(ratio, 6),
    "v1_over_i1_ohm": round(vi1, 6),
    "v2_over_i2_ohm": round(vi2, 6),
}
results = {k: (int(v) if float(v).is_integer() else v) for k, v in results.items()}

# Asserts: every number the script speaks.
assert results["i1_a"] == 0.2, results                 # "zero point two amperes"
assert results["i2_a"] == 0.4, results                 # "zero point four amperes"
assert results["ratio_i2_over_i1"] == 2, results       # "twice the current"
assert results["v1_over_i1_ohm"] == 10, results        # "ten ohms"
assert results["v2_over_i2_ohm"] == 10, results        # "ten ohms"
assert V2 / V1 == 2, "doubling voltage must be the 2x shown"

display = {
    "r_label": "R =",
    "r_unit": OHM,
    "v_label": "V =",
    "v_unit": "V",
    "i_label": "I =",
    "i_unit": "A",
    "ratio_label": "V / I =",
    "v1_value": "2 V",
    "v2_value": "4 V",
    "i1_value": "0.2 A",
    "i2_value": "0.4 A",
    "r_value": "10 Ω",
    "ratio_value": "10 Ω",
    "times_two": "×2",
    "rise_glyph": "R ↑",
    "condition": "constant temperature",
    "equation": "V = I × R",
    "lamp_name": "filament lamp",
    "relation": "×2 voltage → ×2 current",
    "ui": {"think_prompt": "Pause. Predict."},
}

fixture = {
    "fixture_id": "FIX-ohm-readings",
    "display": display,
    "parameters": parameters,
    "results": results,
}

text = json.dumps(fixture, ensure_ascii=False, indent=2)
pathlib.Path(__file__).resolve().parent.joinpath("fixture.json").write_text(text + "\n", encoding="utf-8")
print(text)
