#!/usr/bin/env python3
"""test_v2.py: regression for script v2 (16 Oct 2026). The sample passes check_script; each broken copy fails for the
named reason; the v1 Opus scripts still pass; v1 synthetic cue sheets keep their think windows. Run: python3 test_v2.py"""
import copy, json, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); import pilotlib as L
SAMPLE = HERE.parents[1] / "17_professor_diki_simplified/format/sample_v2_script.json"


def run(path):
    r = subprocess.run([sys.executable, str(HERE / "check_script.py"), str(path)], capture_output=True, text=True)
    return r.returncode, r.stdout


def broken(mutate, expect):
    s = json.loads(SAMPLE.read_text()); mutate(s)
    p = SAMPLE.parent / "_test_broken.json"          # same folder: lesson_graph.json and fixtures/ resolve
    try:
        p.write_text(json.dumps(s)); code, out = run(p)
    finally:
        p.unlink()
    assert code == 1 and expect in out, (expect, out[-800:])


def beat(s, slot):
    return next(b for b in s["beats"] if b["slot"] == slot)


assert run(SAMPLE)[0] == 0, run(SAMPLE)[1]
broken(lambda s: beat(s, "check.predict").update(text="What does the meter read at eight volts?"), "prediction not answerable")
broken(lambda s: s["beats"].remove(beat(s, "check.transfer")), "missing slot check.transfer")
broken(lambda s: beat(s, "close.next_step").update(text="Try ExamLeaf books."), "ExamLeaf")
broken(lambda s: beat(s, "outro.brand").update(text="AI-generated narration."), "disclosure is spoken")
broken(lambda s: beat(s, "check.predict")["pauses"][0].update(after_s=5), "outside PD-01")
broken(lambda s: beat(s, "explain.mechanism").update(pauses=[]), "every gap carries a purpose")
broken(lambda s: s["beats"][2].pop("insight_beat"), "exactly one insight_beat")
broken(lambda s: s["beats"].insert(1, copy.deepcopy(beat(s, "explain.formal")) | {"id": "bx"}), "outside 120-135")
broken(lambda s: beat(s, "outro.brand").update(text="AI-generated narration; script by ExamLeaf. Professor Diki Simplified."), "disclosure is spoken")
broken(lambda s: s["beats"][-2].update(text="Follow for more."), "must be cta_line")
broken(lambda s: beat(s, "outro.brand").update(text="Professor Diki Simplified. Bye."), "last spoken sentence")


def one_beat_close(s):   # PD-14 close as one outro beat of two sentences
    cta = s["beats"].pop(-2); s["scenes"][0]["beats"].remove(cta["id"])
    beat(s, "outro.brand")["text"] = cta["text"] + " Professor Diki Simplified."


p = SAMPLE.parent / "_test_ok.json"; s1 = json.loads(SAMPLE.read_text()); one_beat_close(s1)
try:
    p.write_text(json.dumps(s1)); code, out = run(p)
finally:
    p.unlink()
assert code == 0, out
for subj in ("physics", "chemistry", "biology"):
    code, out = run(HERE.parent / subj / "opus/script.json")
    assert code == 0, out
    v1 = L.load_script(HERE.parent / subj / "opus/script.json")
    sh, _, _ = L.build_scene_sheet(v1, "s02")
    assert sh["meta"]["think_windows"][0]["seconds"] == 5.0 and sh["meta"]["pauses"][-1]["purpose"] == "think_calc"
s2 = L.load_script(SAMPLE); sh, _, _ = L.build_scene_sheet(s2, "s01")
assert [p["purpose"] for p in sh["meta"]["think_windows"]] == ["think_calc", "think_calc"]
assert len(sh["meta"]["energy"]) == len(s2["beats"]) and "disclosure" not in sh["meta"]["beats_text"][-1]   # PD-20: no disclosure in the lesson
assert sh["meta"]["beats_text"][-1]["text"].strip() == "Professor Diki Simplified."
print("test_v2: all checks passed")
