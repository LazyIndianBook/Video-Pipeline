#!/usr/bin/env python3
"""Fixture for phy-ohm-pd-04 (Professor Diki Simplified, explainer_60, PD-26 method, PD-27 plain speech, PD-28 fast and
packed): one ohmic resistor, its meter unknown until I = V / R gives 0.20 A at 2 V; 4 V -> 0.40 A; the resistance case
20 ohm at 2 V -> 0.10 A; the V-I graph points (0, 0), (0.20, 2), (0.40, 4), (0.60, 6); the NCERT 12.3 statement and the
unit meanings as display strings; the qualitative filament flag. Every number and every on-screen string comes from here.
Run: python3 fixtures/compute.py   (writes fixture.json next to this file; fails on any broken assertion)"""
import json, pathlib, re
from fractions import Fraction as F           # exact arithmetic: no float noise in 0.2 / 0.4 / 0.6

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE.parent
BRAND = json.loads((BUILD.parents[1] / "brand" / "strings.json").read_text(encoding="utf-8"))

R = F(10)                         # ohm (ohmic resistor, constant temperature)
R2 = F(20)                        # ohm: the resistance case (double R at 2 V)
V1, V2, V3 = F(2), F(4), F(6)     # volt: the calculation, the change (doubled), the free lesson's next meter
I1, I2, I3 = V1 / R, V2 / R, V3 / R   # I = V / R
I_R2 = V1 / R2                    # 2 V / 20 ohm
J_PER_C_1 = V1                    # 1 V = 1 J/C (DEF-potential-difference): 2 V across the ends = 2 J per coulomb
num = lambda q: int(q) if q.denominator == 1 else float(q)

# every spoken or shown number
assert num(I1) == 0.2 and num(I2) == 0.4 and num(I3) == 0.6, "2/10, 4/10, 6/10"
assert V2 / V1 == 2 and I2 / I1 == 2, "doubling V doubles I for constant R"
assert V1 / I1 == V2 / I2 == V3 / I3 == R == 10, "V / I is 10 ohm throughout"
assert J_PER_C_1 == 2, "two volts = two joules per coulomb"
assert num(I_R2) == 0.1 and R2 / R == 2 and I1 / I_R2 == 2, "2/20 = 0.10: double R at the same V halves I"
assert V1 == I1 * R and I1 == V1 / R and R == V1 / I1, "V = I R and both rearrangements"
GRAPH = [(F(0), F(0)), (I1, V1), (I2, V2), (I3, V3)]   # NCERT plots V against I: a straight line through the origin
assert all(v == R * i for i, v in GRAPH), "every graph point lies on V = R I: slope R, through the origin"
LAMP_CURRENT_DOUBLES = False      # CLM-filament: qualitative and reviewed flag only; never a lamp current value (PD-16)

# display strings (PD-13: literal fixture strings, bound by data-fx; nothing assembled at runtime)
sym = {"V": "V", "I": "I", "R": "R"}
ops = {"eq": "=", "div": "÷", "times": "×", "over": "/", "sep": "·"}   # over/sep: the NCERT-page formula line "V = I R · I = V / R · R = V / I"
words = {"current": "current", "voltage": "voltage", "resistance": "resistance"}   # the calculation in words first
condition = "same temperature"   # NCERT 12.3: "provided its temperature remains the same"; spoken "stays the same"
units = {"ampere": "1 A = 1 C/s", "volt": "1 V = 1 J/C", "ohm": "1 Ω = 1 V/A"}   # unit meanings (DEF-units)
ncert = {"tag": "NCERT §12.3 Ohm's law",
         "statement": "“The potential difference, V, across the ends of a given metallic wire in an electric circuit is directly proportional to the current flowing through it, provided its temperature remains the same.”",
         "source": "NCERT Class 10 Science, Chapter 12 Electricity, §12.3"}
ncert["p1"], ncert["p2"] = ("“The potential difference, V, across the ends of a given metallic wire in an electric circuit",
                            "is directly proportional to the current flowing through it, provided its temperature remains the same.”")
assert ncert["p1"] + " " + ncert["p2"] == ncert["statement"], "the two sheet pages are the verbatim statement, split once"
topic = "Ohm's law"
ui = {                            # PD-20/21/24: no header, no disclosure, no prompts; end card = brand line + free-lesson line
    "unknown": "?",
    "ellipsis": "…",              # page-turn mark between the two halves of the NCERT sentence (chrome, not quoted text)
    "endcard_line1": BRAND["end_card"]["brand_line"],
    "endcard_line2": BRAND["end_card"]["free_lesson_line"].replace("{{TOPIC}}", topic),
}
FLOW_PX_PER_A = 300               # animation scale: dash speed px/s = 300 x the current (SIM-flow-speed); not a physical speed
flow = {"px_per_a": FLOW_PX_PER_A, "lamp_factor": 0.7}   # lamp: dashes slow to 0.7 x the 4 V resistor speed; QUALITATIVE, never a number
fmt_i = lambda q: f"{float(q):.2f}"
card = {                          # PD-18 card strings; each traces to a lesson-graph node (comment)
    "head": {"v": sym["V"], "i": sym["I"], "ratio": f"{sym['V']} {ops['div']} {sym['I']}"},
    "head3": {"v": sym["V"], "r": sym["R"], "i": sym["I"]},
    "def": {                                                                       # definitions at the point of use (M04), each with its unit meaning
        "voltage": {"term": "Voltage", "text": f"potential difference: energy per unit charge. {units['volt']}"},           # DEF-potential-difference, DEF-units
        "current": {"term": "Current", "text": f"the charge flowing each second. {units['ampere']}"},            # DEF-current, DEF-units
        "resistance": {"term": "Resistance", "text": f"how much it holds the flow back. {units['ohm']}"},       # DEF-resistance, DEF-units
    },
    "ncert": ncert,                                                                # CLM-ncert-ohm (verbatim, NCERT 12.3)
    "graph": {"title": "V–I graph (NCERT §12.3)", "x": f"{sym['I']} (A)", "y": f"{sym['V']} (V)",     # REP-vi-graph
              "slope": f"slope = {sym['V']} {ops['div']} {sym['I']}", "slope_r": f"= {sym['R']} = {num(R)} Ω"},
    "points": {"p1": f"{sym['V']} = {sym['I']} × {sym['R']}, {sym['I']} = {sym['V']} ÷ {sym['R']}, {sym['R']} = {sym['V']} ÷ {sym['I']}",  # CLM-resistance-constant
               "p2": f"2× {sym['V']} → 2× {sym['I']}, 2× {sym['R']} → ½ {sym['I']}",               # WRK-ohm-two-points, WRK-ohm-double-r
               "p3": f"Same temperature only."},                                                # CLM-ncert-ohm, CLM-filament
}
assert ui["endcard_line1"] == "Professor Diki Simplified"
assert ui["endcard_line2"] == "Free lesson: Ohm's law"
assert units == {"ampere": "1 A = 1 C/s", "volt": "1 V = 1 J/C", "ohm": "1 Ω = 1 V/A"}, "unit meanings (NCERT 12.1, 12.2, 12.3)"
assert ncert["statement"].strip("“”") == ("The potential difference, V, across the ends of a given metallic wire in an electric circuit is directly "
    "proportional to the current flowing through it, provided its temperature remains the same."), "NCERT 12.3 verbatim"
assert card["graph"]["slope"] + " " + card["graph"]["slope_r"] == "slope = V ÷ I = R = 10 Ω" and all(v == R * i for i, v in GRAPH[1:])
assert I2 == 2 * I1 and I_R2 == I1 / 2, "points p2: 2x V -> 2x I, 2x R -> half I"
assert 0 < flow["lamp_factor"] < 1 and FLOW_PX_PER_A * I1 * 2 == FLOW_PX_PER_A * I2, "dash speed tracks the meter; the lamp only slows (qualitative)"
assert card["head"]["ratio"] == "V ÷ I"
strings = [v for v in ui.values() if isinstance(v, str)] + [v for v in card["head"].values()] + list(card["points"].values()) \
    + [x for d in card["def"].values() for x in d.values()] + list(words.values()) + list(units.values()) + list(ncert.values()) + list(card["graph"].values())
assert not any(re.search(r"ai[- ]generated|script by|\{\{|exam\s*leaf|PROFESSOR DIKI SIMPLIFIED ·", v, re.I) for v in strings), "PD-20/21"
assert all(len(v) <= 32 for v in card["points"].values()), "points fit one card row"
assert all(len(d["text"]) <= 64 for d in card["def"].values()), "a definition fits two card lines"

fixture = {
    "fixture_id": "FIX-ohm-pd-04",
    "compute": "fixtures/compute.py",
    "parameters": {"resistance_ohm": num(R), "r2": num(R2), "v1": num(V1), "v2": num(V2), "v3": num(V3)},
    "results": {"i1": num(I1), "i2": num(I2), "i3": num(I3), "ratio_v": num(V2 / V1), "ratio_i": num(I2 / I1),
                "v_over_i_1": num(V1 / I1), "v_over_i_2": num(V2 / I2), "v_over_i_3": num(V3 / I3), "j_per_c_1": num(J_PER_C_1),
                "i_r2": num(I_R2), "ratio_r": num(R2 / R), "graph": [[num(i), num(v)] for i, v in GRAPH],
                "lamp": {"current_doubles": LAMP_CURRENT_DOUBLES}},
    "display": {"r_label": "R =", "r_unit": "Ω", "v_label": "V =", "v_unit": "V", "i_label": "I =", "i_unit": "A",
                "ammeter_symbol": "A", "condition": condition, "lamp_label": "filament lamp", "r_symbol": "R", "rises": "↑",
                "sym": sym, "ops": ops, "words": words, "units": units, "times": ops["times"], "decimals": {"v": 0, "i": 2}, "ui": ui,
                "card": card, "flow": flow},
}
assert "lamp" not in json.dumps(fixture["parameters"]) and set(fixture["results"]["lamp"]) == {"current_doubles"}, "no lamp number"

# closure: every number phrase the script speaks matches a fixture value, and nothing else is spoken as a number
script = json.loads((BUILD / "script.json").read_text(encoding="utf-8")) if (BUILD / "script.json").exists() else None
if script:
    spoken = " ".join(b["text"] for b in script["beats"]).lower()
    said = {"two volts": V1, "four volts": V2, "ten ohms": R, "twenty ohms": R2, "point two": I1, "point four": I2,
            "point one": I_R2}
    for phrase, q in said.items():
        assert phrase in spoken, f"script no longer says '{phrase}'"
    assert not re.search(r"\b(three|five|six|seven|eight|nine|forty|hundred)\b|\d", spoken), "an unfixtured number is spoken"
    claim = next(b["on_screen"]["claim_line"] for b in script["beats"] if (b.get("on_screen") or {}).get("claim_line"))
    assert len(claim.split()) <= 9 and claim in " ".join(b["text"] for b in script["beats"]), "claim line spoken verbatim"
    assert script["beats"][0]["text"].startswith(script["promise_line"]), "promise_line is the hook's first sentence (M02)"

(HERE / "fixture.json").write_text(json.dumps(fixture, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("fixture OK" + (" (script closure checked)" if script else " (no script yet)"))
