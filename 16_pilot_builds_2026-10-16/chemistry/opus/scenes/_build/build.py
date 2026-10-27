#!/usr/bin/env python3
"""Assembles self-contained scenes/sNN.html from core.html + sNN.part.html (sections: <!--CSS--> <!--BODY--> <!--JS-->).
Inline fallbacks = the synthetic cue sheet for that scene + fixtures/fixture.json. Re-run after editing script or fixture."""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent; OPUS = HERE.parent.parent
sys.path.insert(0, str(OPUS.parent.parent / "tooling"))
import pilotlib as L

script = L.load_script(OPUS / "script.json"); fixture = (OPUS / "fixtures" / "fixture.json").read_text(encoding="utf-8")
core = (HERE / "core.html").read_text(encoding="utf-8")
for sc in script["scenes"]:
    part = (HERE / f"{sc['id']}.part.html").read_text(encoding="utf-8")
    sec = dict(re.findall(r"<!--(CSS|BODY|JS)-->\n(.*?)(?=<!--(?:CSS|BODY|JS)-->|\Z)", part, re.S))
    sheet, _, _ = L.build_scene_sheet(script, sc["id"])
    out = core
    for k, v in {"TITLE": f"{script['video_id']} {sc['id']}: {sc['title']}", "CSS": sec.get("CSS", ""), "BODY": sec.get("BODY", ""),
                 "SCENE_JS": sec["JS"], "CUES_INLINE": json.dumps(sheet, ensure_ascii=False), "FIXTURE_INLINE": fixture.strip()}.items():
        out = out.replace("{{" + k + "}}", v)
    (OPUS / sc["file"]).write_text(out, encoding="utf-8"); print("wrote", sc["file"], len(out))
