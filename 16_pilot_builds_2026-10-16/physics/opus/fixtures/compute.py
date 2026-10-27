#!/usr/bin/env python3
"""Fixture for phy-ohm-ci-01: Ohm's law with one ohmic resistor at two voltages.
Every number and science label on screen comes from here. Run: python3 fixtures/compute.py"""
import json, pathlib
from fractions import Fraction as F   # exact arithmetic: no float noise in 0.2 / 0.4

R = F(10)            # ohm, the resistor (constant: ohmic conductor at constant temperature)
V1, V2 = F(2), F(4)  # volt, the two settings

I1, I2 = V1 / R, V2 / R          # Ohm's law: I = V / R
ratio_v, ratio_i = V2 / V1, I2 / I1
vi1, vi2 = V1 / I1, V2 / I2

num = lambda q: int(q) if q.denominator == 1 else float(q)

# Every result the script speaks or shows
assert I1 == F(1, 5) and num(I1) == 0.2, "I1 must be 0.2 A"
assert I2 == F(2, 5) and num(I2) == 0.4, "I2 must be 0.4 A"
assert ratio_v == 2 and ratio_i == 2, "doubling V doubles I for constant R"
assert vi1 == R and vi2 == R and num(vi1) == 10, "V/I is 10 ohm at both points"
assert V2 == 2 * V1, "four volts is twice two volts"

fixture = {
    "fixture_id": "FIX-ohm-two-points",
    "compute": "fixtures/compute.py",
    "parameters": {"resistance_ohm": num(R), "v1": num(V1), "v2": num(V2)},
    "results": {"i1": num(I1), "i2": num(I2), "ratio_v": num(ratio_v), "ratio_i": num(ratio_i),
                "v_over_i_1": num(vi1), "v_over_i_2": num(vi2)},
    "display": {"r_label": "R =", "r_unit": "Ω", "v_label": "V =", "v_unit": "V", "i_label": "I =", "i_unit": "A",
                "ammeter_symbol": "A", "vi_label": "V / I =", "times": "×",
                "equation": "V = I × R", "condition": "constant temperature",
                "lamp_label": "filament lamp", "r_symbol": "R", "rises": "↑"},
}
out = pathlib.Path(__file__).resolve().parent / "fixture.json"
out.write_text(json.dumps(fixture, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(fixture, ensure_ascii=False))
