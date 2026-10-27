#!/usr/bin/env python3
"""Fixture for chem-balance-ci-01. Parses formulas, counts atoms per side, asserts every number the script speaks.
Plain Python 3, stdlib only. Run from anywhere: writes fixture.json next to this file and prints it."""
import json, pathlib, re
from collections import Counter

ELEMENTS = {"H": "hydrogen", "O": "oxygen"}


def parse(formula):
    """'H2O' -> [('H', 2), ('O', 1)]. Simple formulas only (no brackets, no charges)."""
    parts = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    assert "".join(e + n for e, n in parts) == formula, f"cannot parse {formula}"
    return [(e, int(n) if n else 1) for e, n in parts]


def count(side):
    """side: [(coefficient, formula)] -> Counter of atoms."""
    c = Counter()
    for k, f in side:
        for e, n in parse(f):
            c[e] += k * n
    return c


def tally(lhs, rhs):
    L, R = count(lhs), count(rhs)
    els = sorted(set(L) | set(R), key=list(ELEMENTS).index)
    return {"left": {e: L[e] for e in els}, "right": {e: R[e] for e in els},
            "match": {e: L[e] == R[e] for e in els}, "balanced": L == R,
            "coefficients": {f: k for k, f in lhs + rhs}}


EQS = {  # the three states the video shows, in order
    "unbalanced": ([(1, "H2"), (1, "O2")], [(1, "H2O")]),
    "step1":      ([(1, "H2"), (1, "O2")], [(2, "H2O")]),   # "put a two in front of water"
    "balanced":   ([(2, "H2"), (1, "O2")], [(2, "H2O")]),   # "put a two in front of hydrogen"
}
SPECIES = {"H2": "hydrogen", "O2": "oxygen", "H2O": "water", "H2O2": "hydrogen peroxide"}

results = {k: tally(*v) for k, v in EQS.items()}
results["peroxide_atoms"] = dict(count([(1, "H2O2")]))

# Asserts: every number the script speaks or the screen shows.
u, s1, b = results["unbalanced"], results["step1"], results["balanced"]
assert u["left"] == {"H": 2, "O": 2} and u["right"] == {"H": 2, "O": 1}       # "left, two oxygen ... right, only one"
assert u["match"] == {"H": True, "O": False} and not u["balanced"]             # oxygen mismatch
assert s1["right"] == {"H": 4, "O": 2} and s1["left"]["O"] == s1["right"]["O"]  # "oxygen: two and two", "hydrogen is four on the right"
assert not s1["balanced"]
assert b["left"] == {"H": 4, "O": 2} and b["right"] == {"H": 4, "O": 2} and b["balanced"]   # "four and four"
assert b["coefficients"] == {"H2": 2, "O2": 1, "H2O": 2}                         # "put a two in front"
assert results["peroxide_atoms"] == {"H": 2, "O": 2}                             # "H two O two"
assert parse("H2") == [("H", 2)] and parse("O2") == [("O", 2)] and parse("H2O") == [("H", 2), ("O", 1)]

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
display = {
    "ops": {"plus": "+", "arrow": "→", "eq": "=", "neq": "≠"},
    "elements": {e: {"symbol": e, "name": n} for e, n in ELEMENTS.items()},
    # parts: one entry per element in the formula; 'sub' is the subscript string, "" when the count is 1.
    "species": {f: {"unicode": f.translate(SUB), "name": n,
                    "parts": [{"symbol": e, "sub": str(k) if k > 1 else ""} for e, k in parse(f)]}
                for f, n in SPECIES.items()},
    "coefficients": {k: {f: (str(c) if c > 1 else "") for f, c in v["coefficients"].items()} for k, v in results.items() if "coefficients" in v},
    "counts": {k: {side: {e: str(n) for e, n in v[side].items()} for side in ("left", "right")} for k, v in results.items() if "left" in v},
    "ui": {"think_prompt": "Pause. Predict."},   # contract §4 think-window treatment; not science
}
parameters = {"species": {f: dict(parse(f)) for f in SPECIES}, "equations": {k: {"lhs": [[c, f] for c, f in v[0]], "rhs": [[c, f] for c, f in v[1]]} for k, v in EQS.items()}}

fixture = {"fixture_id": "FIX-chem-balance-water", "video_id": "chem-balance-ci-01", "compute": "fixtures/compute.py",
           "display": display, "parameters": parameters, "results": results}
out = json.dumps(fixture, ensure_ascii=False, indent=1)
(pathlib.Path(__file__).resolve().parent / "fixture.json").write_text(out + "\n", encoding="utf-8")
print(out)
