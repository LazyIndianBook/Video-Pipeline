#!/usr/bin/env python3
"""consolidate_findings.py: merge audit/A*_findings.json into 01_VIDEO_AUDIT.md (tables by severity and by video)
and audit/all_findings.json. Keeps every field; orders critical → major → minor; counts per lens, video and layer."""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]; A = ROOT / "audit"
order = {"critical": 0, "major": 1, "minor": 2}
allf = []
for f in sorted(A.glob("A*_findings.json")):
    try:
        items = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print("unreadable", f.name, e); continue
    if isinstance(items, dict): items = items.get("findings", [])
    for it in items:
        it["_lens"] = f.name.split("_")[0]
        sev = str(it.get("severity", "minor")).lower(); it["severity"] = {"high": "major", "medium": "minor", "low": "minor", "blocking": "critical"}.get(sev, sev)   # A3 used high/medium/low
        allf.append(it)
allf.sort(key=lambda x: (order.get(str(x.get("severity", "minor")).lower(), 3), x.get("video", ""), str(x.get("t", ""))))
(A / "all_findings.json").write_text(json.dumps(allf, ensure_ascii=False, indent=1), encoding="utf-8")
by_sev = collections.Counter(str(x.get("severity", "")).lower() for x in allf)
by_video = collections.Counter(x.get("video", "") for x in allf)
by_layer = collections.Counter((x.get("root_cause") or {}).get("layer", "") for x in allf)
by_lens = collections.Counter(x["_lens"] for x in allf)
def cell(s, n=220):
    s = str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n - 1] + "…"
md = ["# 01 · Complete video audit of the Opus builds (consolidated, 16 Oct 2026)", "",
      "Status: consolidated from six audit lenses (A1 script and teaching, A2 visual explanation, A3 pacing/narration/audio, A4 production-system root causes, A5 brand and playbook alignment, A6 creative benchmarks). Each finding carries the video, timestamp, evidence, the root cause located in our own files, the learner effect, severity and the permanent fix. Raw lens reports: `audit/A1…A6_*.md`; machine-readable: `audit/all_findings.json`.", "",
      f"**Counts.** {len(allf)} findings: " + ", ".join(f"{k} {v}" for k, v in sorted(by_sev.items(), key=lambda kv: order.get(kv[0], 3))) + ". By video: " + ", ".join(f"{k or 'unspecified'} {v}" for k, v in by_video.most_common()) + ". By root-cause layer: " + ", ".join(f"{k or 'unspecified'} {v}" for k, v in by_layer.most_common()) + ". By lens: " + ", ".join(f"{k} {v}" for k, v in sorted(by_lens.items())) + ".", ""]
for sev in ("critical", "major", "minor"):
    rows = [x for x in allf if str(x.get("severity", "")).lower() == sev]
    if not rows: continue
    md += [f"## {sev.capitalize()} ({len(rows)})", "", "| ID | Video | Time | What is wrong (evidence) | Root cause (layer · location) | Effect | Permanent fix (what · where · control) |", "|---|---|---|---|---|---|---|"]
    for x in rows:
        rc = x.get("root_cause") or {}; fx = x.get("fix") or {}
        md.append(f"| {x.get('id')} | {x.get('video')} | {cell(x.get('t'), 40)} | {cell(x.get('problem'), 260)} _({cell(x.get('evidence'), 160)})_ | {cell(rc.get('layer'), 30)} · {cell(rc.get('location'), 120)} | {cell(x.get('effect'), 160)} | {cell(fx.get('what'), 200)} · {cell(fx.get('where'), 90)} · {cell(fx.get('control'), 110)} |")
    md.append("")
(ROOT / "01_VIDEO_AUDIT.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(allf)} findings → 01_VIDEO_AUDIT.md; severities {dict(by_sev)}; lenses {dict(by_lens)}")
