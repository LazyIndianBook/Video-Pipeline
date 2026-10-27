#!/usr/bin/env python3
"""Fixture for phy-ohm-pd-02 (Professor Diki Simplified, concept_short_60): one ohmic resistor at three voltages, plus
the qualitative filament flag. Every number and every on-screen string comes from here.
Run: python3 fixtures/compute.py   (writes fixture.json next to this file; fails on any broken assertion)"""
import json, pathlib, re
from fractions import Fraction as F           # exact arithmetic: no float noise in 0.2 / 0.4 / 0.6

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE.parent
BRAND = json.loads((BUILD.parents[1] / "brand" / "strings.json").read_text(encoding="utf-8"))

R = F(10)                         # ohm (ohmic resistor, constant temperature)
V1, V2, V3 = F(2), F(4), F(6)     # volt: baseline, prediction, transfer
I1, I2, I3 = V1 / R, V2 / R, V3 / R   # I = V / R
num = lambda q: int(q) if q.denominator == 1 else float(q)

# every spoken or shown number
assert num(I1) == 0.2 and num(I2) == 0.4 and num(I3) == 0.6, "2/10, 4/10, 6/10"
assert V2 / V1 == 2 and I2 / I1 == 2, "doubling V doubles I for constant R"
assert V1 / I1 == V2 / I2 == V3 / I3 == R == 10, "V / I is 10 ohm at all three points"
LAMP_CURRENT_DOUBLES = False      # CLM-filament: qualitative and reviewed flag only; never a lamp current value (PD-16)

# display strings (PD-13: literal fixture strings, bound by data-fx; nothing assembled at runtime)
sym = {"V": "V", "I": "I", "R": "R"}
ops = {"eq": "=", "div": "÷", "times": "×"}
condition = "constant temperature"
topic = "Ohm's law"
ui = {                            # PD-20/21: no header, no disclosure line; end card = brand line + free-lesson line
    "think_prompt": "More, less or same?",
    "transfer_prompt": f"Your turn: {sym['I']} {ops['eq']} ?",
    "unknown": "?",
    "check": "✓",
    "options": {"more": "more", "less": "less", "same": "same"},   # the three-way prediction (A6: commit before reveal)
    "endcard_line1": BRAND["end_card"]["brand_line"],
    "endcard_line2": BRAND["end_card"]["free_lesson_line"].replace("{{TOPIC}}", topic),
}
fmt_i = lambda q: f"{float(q):.2f}"
card = {                          # PD-18 card strings; each traces to a lesson-graph node (comment)
    "head": {"v": sym["V"], "i": sym["I"], "ratio": f"{sym['V']} {ops['div']} {sym['I']}"},
    "def": {"term": topic,                                                         # CLM-resistance-constant
            "text": f"{sym['V']} {ops['eq']} {sym['I']} {ops['times']} {sym['R']}, at {condition}."},   # + CLM-ohm-proportional
    "points": {"p1": f"Double {sym['V']}, double {sym['I']}.",                     # CLM-ohm-proportional, WRK-ohm-two-points
               "p2": f"{num(V3)} V {ops['div']} {num(R)} Ω {ops['eq']} {fmt_i(I3)} A.",  # ASM-transfer-six-volts
               "p3": f"Only at {condition}."},                                     # CLM-ohm-proportional (condition), CLM-filament
}
assert list(ui["options"].values()) == ["more", "less", "same"]
assert ui["endcard_line1"] == "Professor Diki Simplified"
assert ui["endcard_line2"] == "Free lesson: Ohm's law"
assert card["points"]["p2"] == "6 V ÷ 10 Ω = 0.60 A." and V3 / R == I3
assert card["def"]["text"] == "V = I × R, at constant temperature."
assert card["head"]["ratio"] == "V ÷ I" and V1 / I1 == V2 / I2 == V3 / I3 == R
strings = [v for v in ui.values() if isinstance(v, str)] + list(ui["options"].values()) + [v for d in card.values() for v in d.values()]
assert not any(re.search(r"ai[- ]generated|script by|\{\{|exam\s*leaf|PROFESSOR DIKI SIMPLIFIED ·", v, re.I) for v in strings), "PD-20/21"
assert all(len(v) <= 32 for v in card["points"].values()), "points fit one card row"

fixture = {
    "fixture_id": "FIX-ohm-pd-02",
    "compute": "fixtures/compute.py",
    "parameters": {"resistance_ohm": num(R), "v1": num(V1), "v2": num(V2), "v3": num(V3)},
    "results": {"i1": num(I1), "i2": num(I2), "i3": num(I3), "ratio_v": num(V2 / V1), "ratio_i": num(I2 / I1),
                "v_over_i_1": num(V1 / I1), "v_over_i_2": num(V2 / I2), "v_over_i_3": num(V3 / I3),
                "lamp": {"current_doubles": LAMP_CURRENT_DOUBLES}},
    "display": {"r_label": "R =", "r_unit": "Ω", "v_label": "V =", "v_unit": "V", "i_label": "I =", "i_unit": "A",
                "ammeter_symbol": "A", "condition": condition, "lamp_label": "filament lamp", "r_symbol": "R", "rises": "↑",
                "sym": sym, "ops": ops, "times": ops["times"], "decimals": {"v": 0, "i": 2}, "ui": ui, "card": card},
}
assert "lamp" not in json.dumps(fixture["parameters"]) and set(fixture["results"]["lamp"]) == {"current_doubles"}, "no lamp number"

# closure: every number phrase the script speaks matches a fixture value
script = json.loads((BUILD / "script.json").read_text(encoding="utf-8")) if (BUILD / "script.json").exists() else None
if script:
    spoken = " ".join(b["text"] for b in script["beats"]).lower()
    said = {"two volts": V1, "four volts": V2, "six volts": V3, "ten ohms": R, "point two": I1, "point four": I2, "point six": I3}
    for phrase, q in said.items():
        assert phrase in spoken, f"script no longer says '{phrase}'"
    assert not re.search(r"\b(three|five|seven|eight|nine|forty|hundred)\b|\d", spoken), "an unfixtured number is spoken"
    claim = next(b["on_screen"]["claim_line"] for b in script["beats"] if (b.get("on_screen") or {}).get("claim_line"))
    assert len(claim.split()) <= 9 and claim in " ".join(b["text"] for b in script["beats"]), "claim line spoken verbatim"

(HERE / "fixture.json").write_text(json.dumps(fixture, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("fixture OK" + (" (script closure checked)" if script else " (no script yet)"))
