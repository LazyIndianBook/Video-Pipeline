#!/usr/bin/env python3
"""Regression tests for the Professor Diki QA checks A11–A21 (16_pilot_builds_2026-10-16/tooling/qa.py) and the audio
extras in render.py. Plain Python; run with the project venv python (it has imageio_ffmpeg + playwright, which qa.py and
render.py import):  $PY tests/test_regressions.py   (pytest also collects the test_* functions).
Negative fixtures: the three frozen Opus pilot builds (they must keep failing A11/A12/A13/A17 for the audited reasons).
Positive fixture: tests/fixtures/good (script v2 fields; timeline synthesised from the script; `--write-fixtures` rewrites
tests/fixtures/good/narration/timeline.json)."""
import re as _re
import copy, hashlib, json, pathlib, shutil, sys, tempfile, wave

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PILOT = ROOT / "16_pilot_builds_2026-10-16"
sys.path.insert(0, str(PILOT / "tooling"))
import qa, render, imageio_ffmpeg   # noqa: E402

GOOD = HERE / "fixtures/good"
FF = imageio_ffmpeg.get_ffmpeg_exe()
WORD_S, WORD_LEN, LEAD_IN, TAIL = 0.40, 0.32, 0.30, 0.80
XFAIL = {}   # test name -> reason, for any case that cannot pass yet


def synth_timeline(script):
    """Word timings at 150 wpm, each beat followed by the sum of its pauses[].after_s, a 0.3 s lead-in (PD-16) and 0.8 s tail."""
    t = LEAD_IN; beats = []
    for b in script["beats"]:
        ws = []
        for w in qa.L.words_of(b["text"]):
            ws.append({"w": w, "t0": round(t, 3), "t1": round(t + WORD_LEN, 3)}); t += WORD_S
        t = t - WORD_S + WORD_LEN
        beats.append({"id": b["id"], "scene": b["scene"], "slot": b["slot"], "start": ws[0]["t0"], "end": round(t, 3), "words": ws})
        t += sum(qa._pause_len(p) for p in qa.end_pauses(b)) or 0.08
    total = round(beats[-1]["end"] + TAIL, 3)
    return {"video_id": script["video_id"], "fps": 30, "lead_in_s": LEAD_IN, "beats": beats,
            "scenes": [{"id": "s01", "start": 0.0, "end": total, "duration": total}], "total_duration_s": total}


def load_good():
    s = json.loads((GOOD / "script.json").read_text(encoding="utf-8"))
    tl = json.loads((GOOD / "narration/timeline.json").read_text(encoding="utf-8"))
    fx = json.loads((GOOD / "fixtures/fixture.json").read_text(encoding="utf-8"))
    return s, tl, fx


def shift_after(tl, beat_id, delta):
    """Lengthen the pause after beat_id by delta seconds (moves every later word)."""
    tl = copy.deepcopy(tl); on = False
    for b in tl["beats"]:
        if on:
            b["start"] += delta; b["end"] += delta
            for w in b["words"]: w["t0"] = round(w["t0"] + delta, 3); w["t1"] = round(w["t1"] + delta, 3)
        on = on or b["id"] == beat_id
    tl["total_duration_s"] = round(tl["total_duration_s"] + delta, 3)
    return tl


# ---------------------------------------------------------------- negative: the frozen Opus pilots
OPUS_EXPECT = {
    "physics": {"A11": ["duration 71.93 s outside 60.0 ± 1.0 s"],
                "A12": ["forbidden 'ExamLeaf' (F01) in spoken script.json#b07", "forbidden 'ExamLeaf' (F01) in captions narration/captions.vtt",
                        "missing end-card item end_card.brand_line"],
                "A13": ["script has no pauses[] with purpose labels (legacy pause_after_s/think_window_s)",
                        "unscripted silence 17.00–22.50 s (5.51 s) > 0.6 s", "tail silence 69.75–71.94 s (2.19 s) > 1.0 s end-card hold"],
                "A17": ["5 scene files (PD-03: one persistent scene)", "diagram similarity 0.50 at 22.5 s < 0.60 (teardown)", "diagram similarity 0.43 at 46.5 s < 0.60 (teardown)",
                        "diagram similarity 0.57 at 57.5 s < 0.60 (teardown)"],
                "A14": ["no insight_beat declared; first explain beat b03 starts at 22.6 s"],
                "A16": ["diagram lane empty for 3.0 s from 1.0 s while speaking"],
                "A18": ["missing slot check.transfer"], "A19": ["b07 75 wpm beyond ±30 % of 125–165"],
                "A21": ["no energy marks in script (beats[].energy absent)"]},
    "chemistry": {"A11": ["duration 73.20 s outside 60.0 ± 1.0 s"],
                  "A12": ["forbidden 'ExamLeaf' (F01) in spoken script.json#b07"],
                  "A13": ["unscripted silence 16.08–21.64 s (5.56 s) > 0.6 s"],
                  "A17": ["diagram similarity 0.00 at 49.0 s < 0.60 (teardown)"],
                  "A15": ["no visual change for 7.5 s from 29.5 s during speech (> 3 s)"]},
    "biology": {"A11": ["duration 67.10 s outside 60.0 ± 1.0 s"],
                "A12": ["forbidden 'ExamLeaf' (F01) in spoken script.json#b07"],
                "A13": ["unscripted silence 13.62–18.87 s (5.25 s) > 0.6 s"],
                "A17": ["diagram similarity 0.00 at 40.0 s < 0.60 (teardown)", "diagram similarity 0.07 at 52.5 s < 0.60 (teardown)"],
                "A16": ["diagram lane empty for 7.0 s from 40.5 s while speaking"], "A19": ["b07 77 wpm beyond ±30 % of 125–165"]},
}


def _opus(subject):
    d = PILOT / subject / "opus"; s = qa.L.load_script(d / "script.json")
    return dict(qa.run_new_checks(s, d, "concept_short_60", FF, dom=False))


def _check_opus(subject):
    got = _opus(subject)
    for cid, want in OPUS_EXPECT[subject].items():
        r = got[cid]
        assert r["status"] == "fail", (subject, cid, r)
        for reason in want:
            if reason.startswith("diagram similarity"):      # the similarity value is a measurement; compare it to the nearest 0.05 (frame sampling jitter)
                key = lambda x: _re.sub(r"similarity (\d\.\d\d)", lambda m: "similarity %.2f" % (round(float(m.group(1)) / 0.05) * 0.05), x)
                assert any(key(x) == key(reason) for x in r["reasons"]), (subject, cid, reason, r["reasons"])
            else:
                assert reason in r["reasons"], (subject, cid, reason, r["reasons"])


def test_opus_physics_fails(): _check_opus("physics")
def test_opus_chemistry_fails(): _check_opus("chemistry")
def test_opus_biology_fails(): _check_opus("biology")


# ---------------------------------------------------------------- positive: the synthetic good build
def test_good_passes():
    s, tl, fx = load_good(); sil = qa.silences_from_timeline(tl); dur = tl["total_duration_s"]
    out = {"A11": qa.a11_duration(dur, "concept_short_60", s), "A12": qa.a12_brand(GOOD), "A13": qa.a13_pauses(s, tl, sil, dur),
           "A14": qa.a14_first_idea(s, tl), "A18": qa.a18_teaching_order(s, fx), "A19": qa.a19_pace(tl),
           "A20": qa.a20_silence_share(sil, dur, tl), "A21": qa.a21_energy(s)}
    for cid, r in out.items():
        assert r["status"] == "pass", (cid, r)


def test_five_second_think_fails_a13():
    s, tl, fx = load_good(); s = copy.deepcopy(s)
    s["beats"][5]["pauses"] = [{"after_s": 5.0, "purpose": "think_calc"}]      # b06 transfer, the old fixed 5 s window
    tl = shift_after(tl, "b06", 2.0); sil = qa.silences_from_timeline(tl)
    r = qa.a13_pauses(s, tl, sil, tl["total_duration_s"])
    assert r["status"] == "fail", r
    assert "b06: scripted think_calc pause 5.00 s outside 3.00–3.00 s ±10 %" in r["reasons"], r["reasons"]
    assert any(x.startswith("silence ") and "after b06 outside think_calc" in x for x in r["reasons"]), r["reasons"]


def test_examleaf_fails_a12():
    with tempfile.TemporaryDirectory() as t:
        d = pathlib.Path(t) / "b"; shutil.copytree(GOOD, d)
        s = json.loads((d / "script.json").read_text(encoding="utf-8"))
        s["beats"][6]["text"] += " Script by ExamLeaf."
        (d / "script.json").write_text(json.dumps(s), encoding="utf-8")
        r = qa.a12_brand(d)
    assert r["status"] == "fail", r
    assert "forbidden 'ExamLeaf' (F01) in spoken script.json#b07" in r["reasons"], r["reasons"]


def test_examleaf_in_captions_fails_a12():
    r = qa.a12_brand(GOOD, captions="WEBVTT\n\n00:00:58.000 --> 00:00:59.000\nAI-generated narration; script by ExamLeaf.\n")
    assert r["status"] == "fail" and "forbidden 'ExamLeaf' (F01) in captions narration/captions.vtt" in r["reasons"], r


def test_prediction_before_givens_fails_a18():
    s, tl, fx = load_good(); s = copy.deepcopy(s)
    for b in s["beats"][:3]:
        b["on_screen"]["fx_refs"] = [x for x in b["on_screen"]["fx_refs"] if x != "parameters.v2"]
    r = qa.a18_teaching_order(s, fx)
    assert r["status"] == "fail", r
    assert "check.predict b03 asks before its given parameters.v2 is shown (first shown in b04)" in r["reasons"], r["reasons"]


def test_missing_transfer_fails_a18():
    s, tl, fx = load_good(); s = copy.deepcopy(s); s["beats"] = [b for b in s["beats"] if b["slot"] != "check.transfer"]
    r = qa.a18_teaching_order(s, fx)
    assert r["status"] == "fail" and "missing slot check.transfer" in r["reasons"], r


def test_flat_energy_fails_a21():
    s, tl, fx = load_good(); s = copy.deepcopy(s)
    for b in s["beats"]: b["energy"] = 2
    r = qa.a21_energy(s)
    assert r["status"] == "fail" and "1 distinct energy marks < 3" in r["reasons"], r


def test_render_motif_mix_deterministic():
    """The end motif lands at its time, at −3 dB, and two mixes of the same inputs are byte-identical."""
    with tempfile.TemporaryDirectory() as t:
        t = pathlib.Path(t); base = t / "base.wav"
        with wave.open(str(base), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000); w.writeframes(b"\x00\x00" * 48000 * 3)
        ev = [{"file": str(render.MOTIF), "at": 1.6, "gain_db": -3.0}]
        a = render.mix_extras(FF, base, ev, t / "a.wav"); b = render.mix_extras(FF, base, ev, t / "b.wav")
        ha, hb = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (a, b))
        assert ha == hb, "mix not deterministic"
        with wave.open(str(a)) as w:
            n = w.getnframes(); data = w.readframes(n)
        import array
        x = array.array("h", data); first = next(i for i, v in enumerate(x) if abs(v) > 30)
        peak = max(abs(v) for v in x)
        assert n == 48000 * 3, n
        assert abs(first / 48000 - 1.6) < 0.02, first / 48000
        assert abs(20 * __import__("math").log10(peak / 32768) - (-9.0)) < 0.6, peak   # asset peak −6 dBFS, −3 dB gain


def test_render_motif_never_under_speech():
    s, tl, fx = load_good(); s = copy.deepcopy(s); s["beats"][-1]["motif_at"] = 3.0   # would start under the outro words
    ev = render.audio_events(s, GOOD, tl, tl["total_duration_s"])
    m = ev[0]; last_t1 = tl["beats"][-1]["words"][-1]["t1"]
    assert m["kind"] == "end_motif" and m["at"] >= last_t1 + 0.1 - 1e-9 and "moved_from" in m, m


def test_local_transcript_numbers_match_spoken_script():
    """PD-29 (A7, narrate_voxcpm LISTEN): local Whisper writes digits and may split "0.2" into "0" + ".2"; the script speaks words."""
    said = qa.canon([qa.L.norm_word(w) for w in qa.L.words_of("Two volts over ten ohms gives point two amperes, or one point five.")])
    heard = ["2", "volts", "over", "10", "ohms", "gives", "0", ".2", "amperes,", "or", "1.5."]
    assert qa.canon(qa.L.heard_tokens(heard)) == said, (qa.canon(qa.L.heard_tokens(heard)), said)
    assert qa.canon(qa.L.heard_tokens(heard[:6] + ["0.3"] + heard[8:])) != said   # a changed number still shows


def main():
    if "--write-fixtures" in sys.argv:
        s = json.loads((GOOD / "script.json").read_text(encoding="utf-8")); tl = synth_timeline(s)
        (GOOD / "narration").mkdir(exist_ok=True)
        (GOOD / "narration/timeline.json").write_text(json.dumps(tl, indent=1), encoding="utf-8")
        words = sum(len(b["words"]) for b in tl["beats"])
        print(f"wrote timeline: {tl['total_duration_s']} s, {words} words"); return 0
    tests = [(k, v) for k, v in globals().items() if k.startswith("test_") and callable(v)]; bad = 0
    for name, fn in tests:
        try:
            fn(); print(f"PASS  {name}")
        except Exception as e:   # noqa: BLE001
            if name in XFAIL: print(f"XFAIL {name}: {XFAIL[name]}")
            else: bad += 1; print(f"FAIL  {name}: {type(e).__name__}: {str(e)[:600]}")
    print(f"{len(tests) - bad}/{len(tests)} passed"); return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
