#!/usr/bin/env python3
"""preview_scene.py <script.json> <scene_id> [--fixture path] [--times 0.1,0.5,0.9]
Builds a synthetic cue sheet for the scene, renders it in headless Chrome (installed Google Chrome) and writes
scenes/_preview/<scene>_<t>.png plus <scene>.report.json. Exit 2 if the scene reports an error or a fallback source.
Also shoots the middle of every labelled pause (think plates, end card) and records meta.pauses / meta.energy in the
report. Script v2 (pilotlib.is_v2) previews use the per-slot speaking rates, so the synthetic times match the plan."""
import argparse, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("scene"); ap.add_argument("--fixture"); ap.add_argument("--times", default="0.1,0.5,0.9")
    a = ap.parse_args()
    s = L.load_script(a.script); d = pathlib.Path(s["_dir"])
    fx_path = pathlib.Path(a.fixture) if a.fixture else d / "fixtures" / "fixture.json"
    fixture = json.loads(fx_path.read_text(encoding="utf-8")) if fx_path.exists() else {}
    sheet, _, _ = L.build_scene_sheet(s, a.scene)
    scene_file = d / next(sc["file"] for sc in s["scenes"] if sc["id"] == a.scene)
    out = d / "scenes" / "_preview"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{a.scene}.synthetic_cues.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=1), encoding="utf-8")
    times = sorted({round(float(x) * sheet["duration"], 2) for x in a.times.split(",")} | {min(sheet["duration"], round(c["at"] + 0.3, 2)) for c in sheet["cues"]}
                   | {round((pz["start"] + pz["end"]) / 2, 2) for pz in sheet["meta"]["pauses"]})
    report = {"scene": a.scene, "duration_synthetic": sheet["duration"], "times": times, "pauses": sheet["meta"]["pauses"], "energy": sheet["meta"]["energy"]}
    with sync_playwright() as p:
        b, page = L.open_scene(p, scene_file, sheet, fixture)
        report["DURATION"] = page.evaluate("window.DURATION"); report["cueSource"] = page.evaluate("window.__cueSource"); report["fixtureSource"] = page.evaluate("window.__fixtureSource")
        for t in times:
            page.evaluate(f"window.seek({t})")
            page.screenshot(path=str(out / f"{a.scene}_{t:06.2f}.png"), type="png")
        report["errors"] = page.evaluate("window.__errors || []")
        b.close()
    (out / f"{a.scene}.report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    bad = [e for e in report["errors"] if e.get("severity") == "error" or "FALLBACK" in str(e.get("code"))]
    print(json.dumps({k: report[k] for k in ("DURATION", "cueSource", "fixtureSource", "times")}), "| errors:", len(report["errors"]), "| blocking:", len(bad))
    for e in report["errors"]:
        print(" ", e)
    if bad or report["cueSource"] != "injected" or report["fixtureSource"] != "injected":
        sys.exit(2)


if __name__ == "__main__":
    main()
