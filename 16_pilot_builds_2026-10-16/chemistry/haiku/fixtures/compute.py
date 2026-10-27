#!/usr/bin/env python3
"""compute.py: fixture for chem-balance-ci-01 (balancing H2 + O2 -> H2O).

Parses every formula in code, counts atoms per element on each side, searches the
smallest whole-number coefficients that balance the equation, asserts every result the
scenes show, prints the fixture JSON to stdout and writes fixtures/fixture.json.
Plain Python 3, standard library only.
"""
import itertools
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "fixture.json"
SUBSCRIPT = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
TERM_RE = re.compile(r"^\s*(\d*)\s*([A-Z][A-Za-z0-9]*)\s*$")
ATOM_RE = re.compile(r"([A-Z][a-z]?)(\d*)")


def parse_term(term):
    """'2H2O' -> (2, 'H2O', {'H': 2, 'O': 1}). Refuses anything it cannot read in full."""
    m = TERM_RE.match(term)
    if not m:
        raise ValueError("cannot parse term %r" % term)
    coef = int(m.group(1)) if m.group(1) else 1
    formula = m.group(2)
    counts = {}
    rebuilt = ""
    for sym, n in ATOM_RE.findall(formula):
        counts[sym] = counts.get(sym, 0) + (int(n) if n else 1)
        rebuilt += sym + n
    if rebuilt != formula:
        raise ValueError("formula %r not fully parsed" % formula)
    return coef, formula, counts


def side(terms, coefs):
    """Atom totals for one side, using the coefficients given for each term."""
    total = {}
    for term, coef in zip(terms, coefs):
        _, _, counts = parse_term(term)
        for sym, n in counts.items():
            total[sym] = total.get(sym, 0) + coef * n
    return total


def formulas_of(terms):
    return {parse_term(t)[1] for t in terms}


def show(formula):
    return formula.translate(SUBSCRIPT)


LEFT, RIGHT = ["H2", "O2"], ["H2O"]
MIS_RIGHT = ["H2O2"]

# Unbalanced, balanced (searched, not typed) and the tempting wrong fix.
unbal_left, unbal_right = side(LEFT, [1, 1]), side(RIGHT, [1])
unbal_left_check = {"H": 2, "O": 2}
unbal_right_check = {"H": 2, "O": 1}
assert unbal_left == unbal_left_check, unbal_left
assert unbal_right == unbal_right_check, unbal_right
assert unbal_left != unbal_right, "the unbalanced equation must mismatch"

# Smallest whole-number coefficients (1 to 4) that balance H2 + O2 -> H2O.
best = None
for a, b, c in itertools.product(range(1, 5), repeat=3):
    if side(LEFT, [a, b]) == side(RIGHT, [c]):
        if best is None or a + b + c < sum(best):
            best = (a, b, c)
assert best == (2, 1, 2), best
coef_h2, coef_o2, coef_h2o = best
bal_left, bal_right = side(LEFT, [coef_h2, coef_o2]), side(RIGHT, [coef_h2o])
assert bal_left == {"H": 4, "O": 2}, bal_left
assert bal_right == {"H": 4, "O": 2}, bal_right
assert bal_left == bal_right, "balanced equation must be equal on both sides"
assert formulas_of(LEFT + RIGHT) == {"H2", "O2", "H2O"}, "only coefficients may change"

mis_left, mis_right = side(LEFT, [1, 1]), side(MIS_RIGHT, [1])
assert mis_left == {"H": 2, "O": 2} and mis_right == {"H": 2, "O": 2}, (mis_left, mis_right)
assert mis_left == mis_right, "the wrong fix matches the counts"
assert "H2O2" != "H2O", "the wrong fix names a different substance"

fixture = {
    "fixture_id": "FIX-chem-balance-ci-01",
    "compute": "fixtures/compute.py",
    "display": {
        "formula_h2": show("H2"),
        "formula_o2": show("O2"),
        "formula_h2o": show("H2O"),
        "formula_h2o2": show("H2O2"),
        "plus": "+",
        "arrow": "→",
        "equals": "=",
        "sym_h": "H",
        "sym_o": "O",
        "side_left": "Left side",
        "side_right": "Right side",
        "name_h2o": "water",
        "name_h2o2": "hydrogen peroxide",
        "note_different": "a different compound",
        "word_equation": "hydrogen + oxygen \u2192 water",
        "ui": {"think_prompt": "Pause. Predict."},
    },
    "parameters": {"coef_h2": coef_h2, "coef_o2": coef_o2, "coef_h2o": coef_h2o},
    "results": {
        "unbalanced": {"left": unbal_left, "right": unbal_right},
        "balanced": {"left": bal_left, "right": bal_right},
        "misconception": {"left": mis_left, "right": mis_right},
    },
    "asserts": [
        "unbalanced H2 + O2 -> H2O: left H2 O2, right H2 O1 (oxygen mismatch)",
        "balanced 2H2 + O2 -> 2H2O: left H4 O2, right H4 O2 (equal)",
        "misconception H2 + O2 -> H2O2: counts match but H2O2 is hydrogen peroxide, not water",
        "only coefficients change: formulas H2, O2, H2O appear unchanged",
    ],
}

text = json.dumps(fixture, ensure_ascii=False, indent=2) + "\n"
OUT.write_text(text, encoding="utf-8")
print(text, end="")
