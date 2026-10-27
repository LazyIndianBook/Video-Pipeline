#!/usr/bin/env python3
"""prepare_judging.py [subjects...]: build blind A/B folders for the judges under judging/<subject>/{A,B} with
tier-neutral copies (script, graph, fixture, storyboard, contact sheet, three full frames per scene, timeline words,
sanitised QA summary). The tier→label mapping is written to judging/mapping.json (judges never read it)."""
import hashlib, json, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
args = [a for a in sys.argv[1:] if not a.startswith("--")]; opts = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
SUBJECTS = args or ["physics", "chemistry", "biology"]
TIERS = opts.get("tiers", "opus,haiku").split(",")          # e.g. --tiers=opus,haiku_v2
NAME_SUFFIX = opts.get("suffix", "")                         # e.g. --suffix=_v2 → judging/physics_v2/
mapping = {}
for subj in SUBJECTS:
    key = subj + NAME_SUFFIX
    # deterministic but opaque assignment: hash of the judging name decides which tier is A
    a_first = int(hashlib.sha256(key.encode()).hexdigest(), 16) % 2 == 0
    pairs = [("A", TIERS[0] if a_first else TIERS[1]), ("B", TIERS[1] if a_first else TIERS[0])]
    mapping[key] = {label: tier for label, tier in pairs}
    for label, tier in pairs:
        src = ROOT / subj / tier; dst = ROOT / "judging" / key / label
        if dst.exists(): shutil.rmtree(dst)
        (dst / "frames").mkdir(parents=True)
        for f in ("script.json", "lesson_graph.json", "storyboard.md"):
            if (src / f).exists(): shutil.copy(src / f, dst / f)
        shutil.copy(src / "fixtures" / "fixture.json", dst / "fixture.json")
        if (src / "render" / "contact_sheet.png").exists(): shutil.copy(src / "render" / "contact_sheet.png", dst / "contact_sheet.png")
        for fr in sorted((src / "render" / "frames").glob("s*_[0-9][0-9][0-9][0-9][0-9].png")):
            shutil.copy(fr, dst / "frames" / fr.name)
        for fr in sorted((src / "render" / "frames").glob("s*_t*.png")):
            shutil.copy(fr, dst / "frames" / fr.name)
        tl = json.loads((src / "narration" / "timeline.json").read_text(encoding="utf-8"))
        (dst / "timeline_words.json").write_text(json.dumps({"total_duration_s": tl["total_duration_s"], "scenes": tl["scenes"], "beats": [{"id": b["id"], "slot": b["slot"], "start": b["start"], "end": b["end"], "words": [(w["w"], w["t0"]) for w in b["words"]]} for b in tl["beats"]]}, ensure_ascii=False, indent=1), encoding="utf-8")
        qa = json.loads((src / "qa" / "report.json").read_text(encoding="utf-8"))
        sanitised = [{"id": c["id"], "name": c["name"], "status": c["status"], "detail": json.loads(json.dumps(c["detail"]).replace(tier, "<tier>").replace("opus", "<tier>").replace("haiku", "<tier>"))} for c in qa["checks"]]
        (dst / "qa_summary.json").write_text(json.dumps({"summary": qa["summary"], "checks": sanitised}, ensure_ascii=False, indent=1), encoding="utf-8")
        # strip tier words from text files that might leak the label
        for f in ("storyboard.md",):
            p = dst / f
            if p.exists():
                t = p.read_text(encoding="utf-8"); p.write_text(t.replace("Opus", "the builder").replace("opus", "the builder").replace("Haiku", "the builder").replace("haiku", "the builder"), encoding="utf-8")
        for f in ("script.json", "lesson_graph.json"):
            p = dst / f; t = p.read_text(encoding="utf-8")
            if "opus" in t.lower() or "haiku" in t.lower():
                p.write_text(t.replace("opus", "tier").replace("Opus", "tier").replace("haiku", "tier").replace("Haiku", "tier"), encoding="utf-8")
        vid = json.loads((src / "script.json").read_text(encoding="utf-8"))["video_id"]
        mp4 = src / "render" / f"{vid}.mp4"                    # the muxed final, never video_silent.mp4
        if mp4.exists(): shutil.copy(mp4, dst / "video.mp4")   # never expose the tier path
        for q in dst.rglob("*"):                            # scrub tier names from every text file
            if q.suffix in (".json", ".md", ".txt"):
                t = q.read_text(encoding="utf-8")
                for w in ("haiku_v2", "Haiku_v2", "opus", "Opus", "haiku", "Haiku"): t = t.replace(w, "tier")
                q.write_text(t, encoding="utf-8")
mp = ROOT / "judging" / "mapping.json"; prev = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
prev.update(mapping); mp.write_text(json.dumps(prev, indent=1), encoding="utf-8")   # merge: never drop other subjects
print(json.dumps(mapping))
