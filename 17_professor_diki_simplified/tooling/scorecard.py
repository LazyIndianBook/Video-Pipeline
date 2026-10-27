#!/usr/bin/env python3
"""scorecard.py <build_dir> [--verdicts dir] [--label A|B] : compute the Professor Diki Simplified scorecard (09_SCORECARD.md)
from <build_dir>/qa/report.json (checks A1…A21) and, optionally, judge verdict JSONs (verdict_*.json with scores[label][Dn]).
Prints the gate status, per-dimension scores and the 0–100 total; writes <build_dir>/qa/scorecard.json."""
import argparse, json, pathlib, statistics

WEIGHTS = {"D1": 20, "D2": 20, "D3": 10, "D4": 15, "D5": 8, "D6": 5, "D7": 10, "D8": 12}
MACHINE = {"D1": ["A3", "A7"], "D2": ["A18"], "D3": ["A19"], "D4": ["A14", "A15", "A16", "A17"], "D5": ["A10", "A13"],
           "D6": ["A1", "A2", "A4", "A5", "A6", "A8", "A9"], "D7": [], "D8": ["A14", "A15", "A20", "A21"]}
GATES = {"science": ["A3", "A7"], "brand": ["A12"], "prediction_transfer": ["A18"], "persistence": ["A17"],
         "silence_length": ["A20", "A11"], "technical": ["A1", "A2", "A4", "A5", "A6", "A9", "A10"]}
POINTS = {"pass": 5.0, "warn": 3.0, "fail": 0.0}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("build"); ap.add_argument("--verdicts"); ap.add_argument("--label", default="A"); a = ap.parse_args()
    n_verdicts = len(list(pathlib.Path(a.verdicts).glob("verdict_*.json"))) if a.verdicts else 0   # releasable needs judges (16 Oct 2026 plan finding)
    b = pathlib.Path(a.build); rep = json.loads((b / "qa" / "report.json").read_text(encoding="utf-8"))
    status = {c["id"]: c["status"] for c in rep["checks"]}
    judge = {}
    if a.verdicts:
        for vf in sorted(pathlib.Path(a.verdicts).glob("verdict_*.json")):
            v = json.loads(vf.read_text(encoding="utf-8")); sc = (v.get("scores") or {}).get(a.label) or {}
            for d, s in sc.items(): judge.setdefault(d, []).append(float(s))
    gates = {}
    for g, ids in GATES.items():
        present = [i for i in ids if i in status]
        gates[g] = "fail" if any(status[i] == "fail" for i in present) else ("missing" if not present else "pass")
    dims = {}
    for d, w in WEIGHTS.items():
        m = [POINTS.get(status[i], 0.0) for i in MACHINE[d] if i in status]
        ms = statistics.mean(m) if m else None; js = statistics.mean(judge[d]) if judge.get(d) else None
        if ms is not None and js is not None: score = 0.5 * ms + 0.5 * js
        elif js is not None: score = js
        elif ms is not None: score = ms
        else: score = None
        dims[d] = {"weight": w, "machine": ms, "judge": js, "score_0_5": round(score, 2) if score is not None else None,
                   "checks": {i: status.get(i, "absent") for i in MACHINE[d]}}
    scored = [(d, v) for d, v in dims.items() if v["score_0_5"] is not None]
    total = round(sum(v["score_0_5"] / 5 * v["weight"] for d, v in scored) / sum(v["weight"] for d, v in scored) * 100, 1) if scored else None
    out = {"build": str(b), "gates": gates, "any_gate_failed": any(g == "fail" for g in gates.values()), "dimensions": dims, "total_0_100": total,
           "releasable": (n_verdicts > 0 and total is not None and total >= 85 and not any(g == "fail" for g in gates.values()) and "missing" not in gates.values()), "judge_verdicts": n_verdicts,
           "note": "weights are house policy v1.0; judge scores averaged over the panel; dimensions without any evidence are excluded from the total"}
    (b / "qa" / "scorecard.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"gates: {gates}"); [print(f"  {d}: machine {v['machine']} judge {v['judge']} → {v['score_0_5']} (w {v['weight']})") for d, v in dims.items()]
    print(f"TOTAL {total} / 100 | releasable: {out['releasable']}")


if __name__ == "__main__":
    main()
