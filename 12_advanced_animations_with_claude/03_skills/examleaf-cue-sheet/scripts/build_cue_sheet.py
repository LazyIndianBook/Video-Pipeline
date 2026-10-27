#!/usr/bin/env python3
"""build_cue_sheet.py - merge word timings + beats + SFX + reveal cues into the canonical per-scene cue sheet.

Usage:
  python3 build_cue_sheet.py --spec jobs/<scene_id>/cue_spec.json --out jobs/<scene_id>/cue_sheet.json
                             [--previous old_cue_sheet.json]      # #63 re-time report after TTS regeneration
                             [--window START END]                 # Reel sub-range: crop and shift to t=0
                             [--production]                       # release: hashes + real alignment required
  python3 build_cue_sheet.py --selftest

Output: cue_sheet.json in the harness shape (04_harness_contract/cue_sheet.schema.json, schema_version 1.0):
{schema_version, scene_id, fps, duration, language, alignment_source, narration_audio_sha256, script_sha256,
words[{w,t0,t1}], beats[], cues[{id,at,kind,element_id?,word_index?,until?}], sfx[{file,at,gain_db}], meta}, plus
<out>.provenance.json (input hashes, anchor resolution, contains_fixture) and, with --previous, <out>.retime.json.
Every sheet is checked by the ONE harness validator, 04_harness_contract/validate_cue_sheet.py (imported by path;
override the folder with EXAMLEAF_HARNESS_DIR). 15 Oct 2026 (audit M7): the skill-local validator copy was deleted.
Spec kinds are mapped to the schema enum (doc 06 section 5.2): show->reveal, highlight->emphasis,
transform/hide->transition, reveal-answer->reveal (protection recorded in meta.answer_protection).
Paths inside the spec resolve relative to the spec file. Output is byte-deterministic.
Exit codes: 0 ok, 1 blocked (blocker JSON on stdout), 2 usage/IO error.
Rules: reveal at or ~0.05 s before its word [V4-MP 8]; duration derives from narration; frames = DURATION x fps,
snapped UP to a whole frame [N72]; repeated words use a 1-based occurrence index (same semantics as the narration Cue);
optional spec "snap": {"kinds": ["transition"], "tol_s": 0.1} moves decorative cues to the nearest beat (Reels),
never reveal/highlight/show/reveal-answer.
Edge cases: #16, #33, #35, #63. Owns the merged cue sheet only: word timing is examleaf-alignment-localize's,
narration cue frames/captions are examleaf-speech-animation-synchronizer's.
"""
import argparse, hashlib, importlib.util, json, math, os, subprocess, sys, tempfile, unicodedata, wave
from pathlib import Path

# 15 Oct 2026 (audit M7): one validator only, the harness copy. Resolved by path (symlinks resolved), or from
# EXAMLEAF_HARNESS_DIR when the skill is installed away from the repo. Missing harness = hard error, never a skip.
HARNESS = Path(os.environ.get("EXAMLEAF_HARNESS_DIR") or Path(__file__).resolve().parents[3] / "04_harness_contract")
HARNESS_VALIDATOR = HARNESS / "validate_cue_sheet.py"


def _harness():
    spec = importlib.util.spec_from_file_location("examleaf_harness_validate_cue_sheet", HARNESS_VALIDATOR)
    if spec is None or not HARNESS_VALIDATOR.is_file():
        raise OSError(f"harness validator not found at {HARNESS_VALIDATOR} (set EXAMLEAF_HARNESS_DIR)")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, json.loads((HARNESS / "cue_sheet.schema.json").read_text(encoding="utf-8"))


SCHEMA_VERSION = "1.0"
JOINERS = {"\u200c", "\u200d"}          # ZWNJ/ZWJ: transparent, as in the narration comparator
SYMBOL_TOKENS = set("+\u2212=^<>-")      # maths symbols are single tokens, as in the narration comparator
# Spec kind -> schema enum kind (02_documentation/06 section 5.2 mapping)
KIND_MAP = {"reveal": "reveal", "show": "reveal", "reveal-answer": "reveal", "emphasis": "emphasis",
            "highlight": "emphasis", "transition": "transition", "transform": "transition", "hide": "transition",
            "hold": "hold", "marker": "marker"}
NARRATION_LOCKED = {"reveal", "highlight", "show", "reveal-answer", "emphasis"}
ALIGNMENT_SOURCE = {"forced-aligner": "forced_alignment", "provider-timestamps": "tts_provider", "human": "manual",
                    "synthetic-fixture": "synthetic_even_spacing"}


class Blocked(ValueError):
    pass


def _wordch(ch):
    return unicodedata.category(ch)[0] in "LMN"


def tokens(text):
    """Same rules as the narration comparator normalized_words() (05_narration_system pronunciation.py, 15 Oct
    2026): NFC + casefold; a word is a run of letters, marks and digits (Devanagari/Bengali-Assamese conjuncts stay
    whole); ZWJ/ZWNJ inside a word are dropped, never split the word; inner apostrophes kept; maths symbols are
    single tokens."""
    text = unicodedata.normalize("NFC", text).casefold()
    out, buf = [], ""
    for i, ch in enumerate(text):
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if _wordch(ch):
            buf += ch
        elif buf and ch in JOINERS and _wordch(nxt):
            continue
        elif buf and ch in "'\u2019" and _wordch(nxt):
            buf += ch
        else:
            if buf:
                out.append(buf)
                buf = ""
            if ch in SYMBOL_TOKENS:
                out.append(ch)
    if buf:
        out.append(buf)
    return out


def resolve_anchor(words, anchor):
    """Return (time_s, first_word_index) for {phrase, occurrence (1-based), edge start|end}."""
    phrase = tokens(anchor["phrase"])
    if not phrase:
        raise Blocked(f"anchor phrase {anchor['phrase']!r} has no word tokens")
    flat, owner = [], []
    for i, w in enumerate(words):
        for t in tokens(w["text"]):
            flat.append(t)
            owner.append(i)
    hits = [k for k in range(len(flat) - len(phrase) + 1) if flat[k:k + len(phrase)] == phrase]
    occ = int(anchor.get("occurrence", 1))
    if occ < 1 or len(hits) < occ:
        raise Blocked(f"missing occurrence {occ} of {anchor['phrase']!r} (found {len(hits)}): "
                      "the script or the alignment changed; fix the spec, never guess")
    k = hits[occ - 1]
    i, j = owner[k], owner[k + len(phrase) - 1]
    edge = anchor.get("edge", "start")
    if edge not in ("start", "end"):
        raise Blocked(f"edge must be start or end, got {edge!r}")
    return (words[i]["start"] if edge == "start" else words[j]["end"]), i


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def wav_duration(p):
    with wave.open(str(p), "rb") as w:
        return w.getnframes() / w.getframerate()


def load(base, rel):
    p = (base / rel) if not Path(rel).is_absolute() else Path(rel)
    return p, json.loads(p.read_text(encoding="utf-8"))


def build(spec, base):
    warns, prov_inputs, anchors = [], {}, {}
    fps = spec["fps"]
    if not spec.get("language"):
        raise Blocked("spec.language is required (BCP-47, e.g. en-IN, hi-IN): the harness schema requires it")
    nar = spec["narration"]
    apath, alignment = load(base, nar["alignment"])
    prov_inputs["alignment"] = sha256_file(apath)
    words = alignment["words"]
    contains_fixture = alignment.get("method") == "synthetic-fixture"
    if contains_fixture:
        warns.append("alignment method is synthetic-fixture: this cue sheet can never pass release")
    # --- narration duration (duration derives from narration, never the reverse) ---
    sync_events, clip, sr = {}, None, None
    if spec.get("synchronizer"):
        tpath, tl = load(base, spec["synchronizer"]["timeline"])
        prov_inputs["timeline"] = sha256_file(tpath)
        seg = spec["synchronizer"]["segment_id"]
        clip = next((c for c in tl["clips"] if c["segment_id"] == seg), None)
        if clip is None:
            raise Blocked(f"segment {seg!r} not in synchronizer timeline")
        sr = tl["sample_rate"]
        sync_events = {e["cue_id"]: e for e in tl["events"] if e.get("segment_id") == seg}
    audio_sha = nar.get("audio_sha256") or alignment.get("audio_sha256")
    if nar.get("wav"):
        wpath = (base / nar["wav"])
        prov_inputs["narration_wav"] = sha256_file(wpath)
        if audio_sha and audio_sha != prov_inputs["narration_wav"]:
            raise Blocked("narration WAV hash differs from the alignment/spec audio_sha256: stale inputs")
        audio_sha = prov_inputs["narration_wav"]
        narration_end, dsrc = wav_duration(wpath), "wav"
    elif clip is not None:
        narration_end, dsrc = (clip["end_sample"] - clip["start_sample"]) / sr, "synchronizer_clip"
    elif nar.get("duration_s"):
        narration_end, dsrc = float(nar["duration_s"]), "spec"
    else:
        narration_end, dsrc = words[-1]["end"], "last_word_end"
        warns.append("duration taken from the last word end; pass the narration WAV for an exact length")
    if words and words[-1]["end"] > narration_end + 1e-3:
        raise Blocked("alignment ends after the narration audio: alignment and audio do not belong together")
    frames = math.ceil((narration_end + float(spec.get("tail_s", 0.0))) * fps - 1e-9)
    duration = frames / fps
    # --- beats ---
    beats = []
    if spec.get("beats"):
        bpath, an = load(base, spec["beats"]["analysis"])
        prov_inputs["analysis"] = sha256_file(bpath)
        if an.get("params", {}).get("units") != "time":
            raise Blocked("#33 analysis beats are not in seconds (units must be 'time') [N39]")
        src = an.get("source", {})
        if src.get("sr_used") and src.get("sr_native") and src["sr_used"] != src["sr_native"]:
            warns.append("#35 analysis ran on resampled audio; valid only if times used the same sr [N81]")
        if any(b > src.get("duration_s", math.inf) + 1e-3 for b in an["beats_s"]):
            raise Blocked("#33 beats exceed the analysed audio length: frames mistaken for seconds")
        if an.get("fallback") == "none":
            warns.append("#34 no beats and no narration grid: beats list is empty")
        off = float(spec["beats"].get("offset_s", 0.0))
        beats = [round(b + off, 4) for b in an["beats_s"] if 0 <= b + off < duration]
    # --- cues ---
    default_off = float(spec.get("default_offset_s", -0.05))
    cues, at_by_id = [], {}
    for req in spec.get("cues", []):
        cid, kind = req["id"], req["kind"]
        if kind not in KIND_MAP:
            raise Blocked(f"cue {cid!r}: unknown kind {kind!r} (allowed: {sorted(KIND_MAP)})")
        widx = None
        if "at" in req:
            at, src = float(req["at"]), "absolute"
        else:
            t, widx = resolve_anchor(words, req["anchor"])
            src = "alignment"
            if cid in sync_events:  # the synchronizer owns narration cue frames; cross-check, then use its time
                ev = sync_events[cid]
                ts = (ev["sample"] - clip["start_sample"]) / sr
                if abs(ts - t) > 1.0 / fps:
                    raise Blocked(f"cue {cid!r}: synchronizer {ts:.3f}s vs alignment {t:.3f}s differ by >1 frame (stale input)")
                t, src = ts, "synchronizer"
            off = float(req.get("offset_s", 0.0 if kind == "reveal-answer" else default_off))
            if kind == "reveal-answer" and off < 0:
                raise Blocked(f"cue {cid!r}: reveal-answer never leads its word (a lead falls inside the protected "
                              "response window; the synchronizer's 'Premature answer' rule)")
            at = max(0.0, t + off)
            anchors[cid] = {"phrase": req["anchor"]["phrase"], "occurrence": req["anchor"].get("occurrence", 1),
                            "edge": req["anchor"].get("edge", "start"), "word_index": widx, "word_time": t, "source": src}
        at = round(at, 4)
        c = {"id": cid, "at": at, "kind": kind}
        for k in ("element_id", "occurrence", "until"):
            if k in req:
                c[k] = req[k]
        # word_index keys the harness late-reveal check; only for start-edge reveal/emphasis (answers: never-early rule)
        if widx is not None and req["anchor"].get("edge", "start") == "start" and kind != "reveal-answer" \
                and KIND_MAP[kind] in ("reveal", "emphasis"):
            c["word_index"] = widx
        cues.append(c)
        at_by_id[cid] = at
    snapped = []
    snap = spec.get("snap")
    if snap:  # Reel beat re-time: only decorative kinds may move to a beat; reveals stay on their words [V4-MP 8]
        kinds, tol = set(snap.get("kinds", [])), float(snap.get("tol_s", 0.1))
        if kinds & NARRATION_LOCKED:
            raise Blocked(f"narration-locked cue kinds {sorted(kinds & NARRATION_LOCKED)} never snap to beats")
        for c in cues:
            if c["kind"] in kinds and beats:
                b = min(beats, key=lambda x: abs(x - c["at"]))
                if abs(b - c["at"]) <= tol + 1e-9 and b != c["at"]:
                    snapped.append({"id": c["id"], "from": c["at"], "to": b})
                    c["at"] = at_by_id[c["id"]] = b
    cues.sort(key=lambda c: (c["at"], c["id"]))
    spec_kinds, answers = {}, []
    for c in cues:
        if c["kind"] == "reveal-answer":
            answers.append({"cue_id": c["id"], "at": c["at"], "word_time": anchors.get(c["id"], {}).get("word_time"),
                            "rule": "offset >= 0: never leads its word (synchronizer 'Premature answer')"})
        if KIND_MAP[c["kind"]] != c["kind"]:
            spec_kinds[c["id"]] = c["kind"]
            c["kind"] = KIND_MAP[c["kind"]]
    # --- sfx ---
    palette = None
    if spec.get("sfx_manifest"):
        mpath, man = load(base, spec["sfx_manifest"])
        prov_inputs["sfx_manifest"] = sha256_file(mpath)
        palette = {i["file"] for i in man["items"]}
    sfx = []
    for s in spec.get("sfx", []):
        if "gain_db" not in s:
            raise Blocked(f"sfx {s.get('file')!r}: gain_db is required (mix level is an explicit decision)")
        if "cue" in s:
            if s["cue"] not in at_by_id:
                raise Blocked(f"sfx {s['file']!r} references unknown cue {s['cue']!r}")
            at = at_by_id[s["cue"]] + float(s.get("offset_s", 0.0))
        else:
            at = float(s["at"])
        if palette is not None and s["file"] not in palette:
            warns.append(f"sfx file {s['file']!r} is not in the style palette manifest")
        sfx.append({"file": s["file"], "at": round(at, 4), "gain_db": s["gain_db"]})
    sfx.sort(key=lambda x: (x["at"], x["file"]))
    script_sha = spec.get("script_sha256")
    if spec.get("script"):
        script_sha = prov_inputs["script"] = sha256_file(base / spec["script"])
    src = ALIGNMENT_SOURCE.get(alignment.get("method"))
    meta = {"generator": "examleaf-cue-sheet/build_cue_sheet.py"}
    if spec_kinds:
        meta["spec_kinds"] = spec_kinds
    if answers:
        meta["answer_protection"] = answers
    sheet = {"schema_version": SCHEMA_VERSION, "scene_id": spec["scene_id"], "fps": fps, "duration": duration,
             "language": spec["language"], **({"alignment_source": src} if src else {}),
             "narration_audio_sha256": audio_sha, "script_sha256": script_sha,
             "words": [{"w": unicodedata.normalize("NFC", w["text"]), "t0": w["start"], "t1": w["end"]} for w in words],
             "beats": beats, "cues": cues, "sfx": sfx, "meta": meta}
    prov = {"generator": "examleaf-cue-sheet/build_cue_sheet.py", "scene_id": spec["scene_id"],
            "inputs_sha256": prov_inputs, "alignment_method": alignment.get("method"),
            "contains_fixture": contains_fixture, "narration_end_s": narration_end, "duration_source": dsrc,
            "frames": frames, "anchors": anchors, "snapped": snapped, "window": None, "dropped_cues": [], "warnings": warns}
    return sheet, prov


def apply_window(sheet, prov, a, b):
    fps = sheet["fps"]
    if not (0 <= a < b <= sheet["duration"] + 1e-9):
        raise Blocked(f"window [{a}, {b}] outside the scene [0, {sheet['duration']}]")
    for w in sheet["words"]:
        if w["t0"] < a < w["t1"] or w["t0"] < b < w["t1"]:
            raise Blocked(f"window cuts through the word {w['w']!r}; move the window to a word gap")
    frames = math.ceil((b - a) * fps - 1e-9)
    dur = frames / fps
    sh = lambda t: round(t - a, 4)  # noqa: E731
    kept = [i for i, w in enumerate(sheet["words"]) if a <= w["t0"] and w["t1"] <= b]
    newidx = {old: new for new, old in enumerate(kept)}

    def recue(c):
        c = dict(c, at=sh(c["at"]))
        if "word_index" in c:
            if c["word_index"] in newidx:
                c["word_index"] = newidx[c["word_index"]]
            else:
                del c["word_index"]
        return c
    out = dict(sheet, duration=dur,
               words=[dict(sheet["words"][i], t0=sh(sheet["words"][i]["t0"]), t1=sh(sheet["words"][i]["t1"])) for i in kept],
               beats=[sh(x) for x in sheet["beats"] if a <= x < b],
               cues=[recue(c) for c in sheet["cues"] if a <= c["at"] <= b],
               sfx=[dict(s, at=sh(s["at"])) for s in sheet["sfx"] if a <= s["at"] < b])
    prov = dict(prov, frames=frames, window=[a, b],
                dropped_cues=[c["id"] for c in sheet["cues"] if not (a <= c["at"] <= b)])
    return out, prov


def retime_report(old, new):
    o = {c["id"]: c["at"] for c in old["cues"]}
    n = {c["id"]: c["at"] for c in new["cues"]}
    return {"scene_id": new["scene_id"], "duration_old": old["duration"], "duration_new": new["duration"],
            "frames_old": round(old["duration"] * old["fps"]), "frames_new": round(new["duration"] * new["fps"]),
            "cues": [{"id": k, "old_at": o[k], "new_at": n[k], "delta_s": round(n[k] - o[k], 4)} for k in sorted(o.keys() & n.keys())],
            "added": sorted(n.keys() - o.keys()), "removed": sorted(o.keys() - n.keys()),
            "action": "scene code unchanged; re-render the scene and re-run QA (hash changes)"}


def dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def run(spec_path, out, previous=None, window=None, production=False):
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    sheet, prov = build(spec, spec_path.parent)
    if window:
        sheet, prov = apply_window(sheet, prov, *window)
    hv, schema = _harness()
    errs, warns = hv.validate(sheet, schema, production=production)
    if errs:
        raise Blocked("; ".join(errs))
    prov["warnings"] += warns
    out = Path(out)
    out.write_text(dump(sheet), encoding="utf-8")
    out.with_suffix(".provenance.json").write_text(dump(prov), encoding="utf-8")
    rep = None
    if previous:
        rep = retime_report(json.loads(Path(previous).read_text(encoding="utf-8")), sheet)
        out.with_suffix(".retime.json").write_text(dump(rep), encoding="utf-8")
    return sheet, prov, rep


def _write_silence(p, seconds, sr=48000):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(b"\x00\x00" * int(seconds * sr))


def selftest():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        words = [("The", .10, .25), ("current", .30, .70), ("splits;", .75, 1.10), ("current", 1.30, 1.70),
                 ("rejoins", 1.75, 2.20), ("विद्युत्", 2.30, 2.80)]
        al = {"segment_id": "seg-04", "method": "forced-aligner", "words": [{"text": t, "start": s, "end": e} for t, s, e in words]}
        (d / "al.json").write_text(json.dumps(al))
        _write_silence(d / "seg.wav", 3.0)
        (d / "an.json").write_text(json.dumps({"params": {"units": "time"}, "source": {"sr_native": 48000, "sr_used": 48000, "duration_s": 10.0},
                                               "beats_s": [0.0, 0.6, 1.2, 1.8, 2.4, 3.0, 3.6], "fallback": None}))
        (d / "pal.json").write_text(json.dumps({"items": [{"file": "pop.wav"}, {"file": "paper_swish.wav"}]}))
        (d / "script.txt").write_text("The current splits; current rejoins विद्युत्", encoding="utf-8")
        spec = {"scene_id": "phy-10-03-s04", "fps": 30, "tail_s": 0.3, "default_offset_s": -0.05,
                "language": "en-IN", "script": "script.txt",
                "narration": {"alignment": "al.json", "wav": "seg.wav"},
                "beats": {"analysis": "an.json", "offset_s": 0.0}, "sfx_manifest": "pal.json",
                "cues": [{"id": "arrow_2", "kind": "reveal", "element_id": "arrow_2", "anchor": {"phrase": "current", "occurrence": 2}},
                         {"id": "sheet_in", "kind": "transition", "anchor": {"phrase": "rejoins", "edge": "end"}, "offset_s": 0.3},
                         {"id": "hindi_label", "kind": "reveal", "element_id": "hindi_label", "anchor": {"phrase": "विद्युत्"}},
                         {"id": "title", "kind": "show", "element_id": "title", "at": 0.0}],
                "sfx": [{"file": "pop.wav", "cue": "arrow_2", "gain_db": -12},
                        {"file": "paper_swish.wav", "cue": "sheet_in", "gain_db": -18}]}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False))
        sheet, prov, _ = run(d / "spec.json", d / "cue.json")
        at = {c["id"]: c["at"] for c in sheet["cues"]}
        assert at["arrow_2"] == 1.25, at            # 2nd "current" (1.30) minus 0.05 lead
        assert at["sheet_in"] == 2.5 and at["hindi_label"] == 2.25 and at["title"] == 0.0, at
        assert sheet["duration"] * 30 == 99 and sheet["duration"] == 99 / 30      # ceil((3.0+0.3)*30)
        assert sheet["beats"] == [0.0, 0.6, 1.2, 1.8, 2.4, 3.0] and len(sheet["sfx"]) == 2
        assert not prov["contains_fixture"] and prov["anchors"]["arrow_2"]["occurrence"] == 2
        # 15 Oct 2026 (audit M7): harness shape + the ONE harness validator, including --production
        assert sheet["schema_version"] == "1.0" and sheet["language"] == "en-IN", sheet
        assert sheet["narration_audio_sha256"] == sha256_file(d / "seg.wav") and len(sheet["script_sha256"]) == 64
        assert sheet["alignment_source"] == "forced_alignment" and {c["kind"] for c in sheet["cues"]} <= set(KIND_MAP.values())
        assert sheet["meta"]["spec_kinds"] == {"title": "show"}, sheet["meta"]
        assert next(c for c in sheet["cues"] if c["id"] == "arrow_2")["word_index"] == 3
        hv, schema = _harness()
        assert hv.validate(sheet, schema, production=True) == ([], []), hv.validate(sheet, schema, production=True)
        r = subprocess.run([sys.executable, "-B", "-I", str(HARNESS_VALIDATOR), str(d / "cue.json"), "--production", "--json"],
                           capture_output=True, text=True)
        assert r.returncode == 0 and json.loads(r.stdout)["valid"], (r.returncode, r.stdout, r.stderr)
        run(d / "spec.json", d / "cue_p.json", production=True)
        nos = dict(spec, script=None)
        (d / "nos.json").write_text(json.dumps(nos, ensure_ascii=False))
        try:
            run(d / "nos.json", d / "x.json", production=True)
            raise AssertionError("production without a script hash must block")
        except Blocked as e:
            assert "script_sha256 is null" in str(e)
        (d / "late.json").write_text(json.dumps(dict(spec, cues=[{"id": "late", "kind": "reveal", "anchor": {"phrase": "rejoins"},
                                                                    "offset_s": 0.1}], sfx=[]), ensure_ascii=False))
        try:
            run(d / "late.json", d / "x.json")
            raise AssertionError("a late reveal must fail the harness rule")
        except Blocked as e:
            assert "late reveal" in str(e)
        first = (d / "cue.json").read_bytes()
        run(d / "spec.json", d / "cue2.json")
        assert (d / "cue2.json").read_bytes() == first, "determinism"
        # #63: TTS regenerated -> every word 0.2 s later; spec unchanged, cue sheet re-timed
        al2 = dict(al, words=[{"text": t, "start": s + .2, "end": e + .2} for t, s, e in words])
        (d / "al.json").write_text(json.dumps(al2))
        _, _, rep = run(d / "spec.json", d / "cue3.json", previous=d / "cue.json")
        assert {c["id"]: c["delta_s"] for c in rep["cues"]} == {"arrow_2": 0.2, "hindi_label": 0.2, "sheet_in": 0.2, "title": 0.0}, rep
        # occurrence that does not exist -> blocked, never guessed
        bad = dict(spec, cues=[{"id": "x", "kind": "reveal", "anchor": {"phrase": "current", "occurrence": 3}}], sfx=[])
        (d / "bad.json").write_text(json.dumps(bad))
        try:
            run(d / "bad.json", d / "x.json")
            raise AssertionError("missing occurrence must block")
        except Blocked as e:
            assert "occurrence 3" in str(e)
        # answers never lead into the response window
        ans = dict(spec, cues=[{"id": "ans", "kind": "reveal-answer", "anchor": {"phrase": "rejoins"}, "offset_s": -0.05}], sfx=[])
        (d / "ans.json").write_text(json.dumps(ans))
        try:
            run(d / "ans.json", d / "x.json")
            raise AssertionError("leading reveal-answer must block")
        except Blocked as e:
            assert "reveal-answer" in str(e)
        ans["cues"][0].pop("offset_s")
        (d / "ans.json").write_text(json.dumps(ans))
        sh_a = run(d / "ans.json", d / "x.json")[0]
        assert sh_a["cues"][0]["at"] == 1.95   # default 0 for answers (word at 1.75+0.2)
        assert sh_a["cues"][0]["kind"] == "reveal" and "word_index" not in sh_a["cues"][0]
        assert sh_a["meta"]["answer_protection"][0]["cue_id"] == "ans", sh_a["meta"]
        # #33: analysis in frames
        (d / "an.json").write_text(json.dumps({"params": {"units": "frames"}, "beats_s": [0, 26, 52]}))
        try:
            run(d / "spec.json", d / "y.json")
            raise AssertionError("frames must block")
        except Blocked as e:
            assert "#33" in str(e)
        # window for a Reel: [1.25, 2.25] -> shifted to 0, words straddling refused
        (d / "al.json").write_text(json.dumps(al))
        (d / "an.json").write_text(json.dumps({"params": {"units": "time"}, "source": {"duration_s": 10.0}, "beats_s": [1.2, 1.8, 2.4]}))
        sheet_w, prov_w, _ = run(d / "spec.json", d / "w.json", window=(1.25, 2.29))
        assert sheet_w["words"][0]["w"] == "current" and sheet_w["words"][0]["t0"] == 0.05, sheet_w["words"]
        assert sheet_w["duration"] == 32 / 30 and [c["id"] for c in sheet_w["cues"]] == ["arrow_2", "hindi_label"]
        assert sheet_w["beats"] == [0.55] and "title" in prov_w["dropped_cues"], (sheet_w["beats"], prov_w)
        assert next(c for c in sheet_w["cues"] if c["id"] == "arrow_2")["word_index"] == 0   # re-indexed to the crop
        try:
            run(d / "spec.json", d / "z.json", window=(1.0, 2.0))
            raise AssertionError("window through a word must block")
        except Blocked as e:
            assert "cuts through" in str(e)
        # Reel beat re-time: the transition (2.5) snaps to beat 2.4; the paper swish tied to it follows; reveals never snap
        snap_spec = dict(spec, snap={"kinds": ["transition"], "tol_s": 0.1})
        (d / "snap.json").write_text(json.dumps(snap_spec, ensure_ascii=False))
        sh_s, pr_s, _ = run(d / "snap.json", d / "s.json")
        at_s = {c["id"]: c["at"] for c in sh_s["cues"]}
        assert at_s["sheet_in"] == 2.4 and at_s["arrow_2"] == 1.25 and pr_s["snapped"][0]["from"] == 2.5, (at_s, pr_s["snapped"])
        assert any(x["file"] == "paper_swish.wav" and x["at"] == 2.4 for x in sh_s["sfx"]), sh_s["sfx"]
        (d / "snap.json").write_text(json.dumps(dict(spec, snap={"kinds": ["reveal"]}), ensure_ascii=False))
        try:
            run(d / "snap.json", d / "s2.json")
            raise AssertionError("reveals must never snap")
        except Blocked as e:
            assert "never snap" in str(e)
        # synthetic fixture alignment is flagged
        (d / "al.json").write_text(json.dumps(dict(al, method="synthetic-fixture")))
        sh_f, prov_f, _ = run(d / "spec.json", d / "f.json")
        assert prov_f["contains_fixture"] is True
        try:
            run(d / "spec.json", d / "f2.json", production=True)
            raise AssertionError("synthetic alignment must fail --production")
        except Blocked as e:
            assert "not valid for production" in str(e)
        assert tokens("विद्युत्।") == ["विद्युत्"] and tokens("Ohm's law,") == ["ohm's", "law"]
        # ZWJ/ZWNJ: dropped, word kept whole (narration comparator parity); maths symbols are tokens
        assert tokens("क्\u200dष") == ["क्ष"] and tokens("V = IR") == ["v", "=", "ir"] and tokens("\u200cab") == ["ab"]
    print("build_cue_sheet selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--spec")
    ap.add_argument("--out")
    ap.add_argument("--previous")
    ap.add_argument("--window", type=float, nargs=2, metavar=("START", "END"))
    ap.add_argument("--production", action="store_true", help="harness --production rules: hashes and real alignment")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.spec or not a.out:
        ap.print_usage(sys.stderr)
        return 2
    try:
        sheet, prov, rep = run(a.spec, a.out, a.previous, a.window, a.production)
    except Blocked as e:
        print(json.dumps({"status": "blocked", "skill": "examleaf-cue-sheet", "error": str(e)}, indent=2, ensure_ascii=False))
        return 1
    except (OSError, KeyError, json.JSONDecodeError, wave.Error) as e:
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "ok", "out": a.out, "frames": prov["frames"], "cues": len(sheet["cues"]),
                      "warnings": prov["warnings"], "retime": bool(rep)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
