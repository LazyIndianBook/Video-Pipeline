#!/usr/bin/env python3
"""compile_verdicts.py: unblind and tabulate judging/<subject>/verdict_*.json into judging/SUMMARY.md and SUMMARY.json."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]; J = ROOT / "judging"
mapping = json.loads((J / "mapping.json").read_text(encoding="utf-8"))
rows = []; out = {"subjects": {}}
for subj_dir in sorted(p for p in J.iterdir() if p.is_dir() and not p.name.startswith("_")):
    subj = subj_dir.name; labels = mapping.get(subj) or {}
    inv = {label: tier for label, tier in labels.items()}
    for vf in sorted(subj_dir.glob("verdict_*.json")):
        v = json.loads(vf.read_text(encoding="utf-8")); lens = v["lens"]
        rec = {"lens": lens, "winner_label": v["winner"], "winner_tier": inv.get(v["winner"], v["winner"]), "reason": v["reason"], "scores": {}, "gaps": v.get("gap_for_weaker", []), "blocking": {}, "empty_seconds": {}}
        for label, sc in v["scores"].items():
            tier = inv.get(label, label); rec["scores"][tier] = {"dims": sc, "total": sum(sc.values())}
            rec["blocking"][tier] = v.get("blocking_defects", {}).get(label, [])
            if "empty_seconds" in v: rec["empty_seconds"][tier] = v["empty_seconds"].get(label)
        out["subjects"].setdefault(subj, []).append(rec)
        rows.append((subj, lens, rec))
md = ["# Judging summary (unblinded)", "", "| Subject | Lens | Totals by tier | Winner | Dimensions by tier | Empty middle-zone seconds |", "|---|---|---|---|---|---|"]
for subj, lens, rec in rows:
    tot = "; ".join(f"{t} {v['total']}" for t, v in rec["scores"].items()); dims = "; ".join(f"{t} {v['dims']}" for t, v in rec["scores"].items())
    emp = "; ".join(f"{t} {v}" for t, v in rec["empty_seconds"].items()) or "-"
    md.append(f"| {subj} | {lens} | {tot} | {rec['winner_tier']} | {dims} | {emp} |")
md += ["", "## Gap rules proposed by the judges (for the weaker build)", ""]
for subj, lens, rec in rows:
    for g in rec["gaps"]:
        md.append(f"- **{subj}/{lens}:** {g['rule']} _({g['where']})_" if isinstance(g, dict) else f"- **{subj}/{lens}:** {g}")   # PD rubric gates are plain strings
md += ["", "## Blocking defects", ""]
for subj, lens, rec in rows:
    for tier, items in rec["blocking"].items():
        for it in items:
            md.append(f"- **{subj}/{lens}/{tier}:** {it}")
(J / "SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8"); (J / "SUMMARY.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print("\n".join(md[:4 + len(rows)]))
