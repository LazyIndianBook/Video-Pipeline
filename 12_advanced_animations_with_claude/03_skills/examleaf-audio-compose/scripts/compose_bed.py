#!/usr/bin/env python3
"""compose_bed.py - seeded, bar-aligned music-bed stems (stdlib only: wave, math, random, array).

Usage:
  python3 compose_bed.py --style paper-collage-vertical --bars 8 --seed 7 --mood neutral --out-dir jobs/<scene_id>/audio/bed
  python3 compose_bed.py --style doodle-handdrawn --seconds 21.5 --bpm 100 --seed 3 --mood endcard --out-dir ...
  python3 compose_bed.py --selftest

Writes pad.wav, pluck.wav, perc.wav (48 kHz, 16-bit PCM, mono) and bed_meta.json (BPM, bars, seed,
bar/beat grid, stem hashes and levels). Stems are NOT mastered: loudness belongs to
examleaf-audio-production-engineer (-16 LUFS / <= -1 dBTP house target, 07_end_to_end_pipeline_instructions/06).
Exit codes: 0 ok, 1 validation failed (blocker JSON on stdout), 2 usage/IO error.
Edge cases: #10 missing audio, #13 the model cannot hear audio (grid in metadata), #39 levels left to mastering.
Sources: tempo ~100 BPM, low-pass for somber beats, swell on end card [V4-MP 11]; seeded randomness [N61].
"""
import argparse, array, hashlib, json, math, os, random, sys, tempfile, wave
from pathlib import Path

SR = 48000
BEATS_PER_BAR = 4
HEADROOM_DBFS = -12.0          # [Recommendation] stem peak before mixing; the mixer sets the final bed gain
MOODS = {"neutral": (1800.0, 0.0), "somber": (600.0, -6.0), "endcard": (2400.0, 0.0)}  # (pad/bed low-pass Hz, gain dB)
# Chord progressions as semitone offsets from the root. Only the storybook tempo (~100 BPM) is sourced [V4-MP];
# the other styles reuse it as a [Recommendation] default.
STYLES = {
    "paper-collage-vertical": {"root_hz": 261.63, "prog": [[0, 4, 7], [7, 11, 14], [9, 12, 16], [5, 9, 12]], "perc": "brush"},
    "doodle-handdrawn":       {"root_hz": 293.66, "prog": [[0, 4, 7], [5, 9, 12], [7, 11, 14], [0, 4, 7]], "perc": "brush"},
    "editorial-vox":          {"root_hz": 220.00, "prog": [[0, 3, 7], [8, 12, 15], [3, 7, 10], [10, 14, 17]], "perc": "kick"},
    "kinetic-type":           {"root_hz": 246.94, "prog": [[0, 4, 7], [9, 12, 16], [5, 9, 12], [7, 11, 14]], "perc": "kick"},
    "voxel-isometric":        {"root_hz": 329.63, "prog": [[0, 4, 7], [2, 7, 9], [4, 7, 11], [0, 5, 9]], "perc": "brush"},
}


def blocker(msg, **extra):
    print(json.dumps({"status": "blocked", "skill": "examleaf-audio-compose", "error": msg, **extra}, indent=2))
    return 1


def db_to_gain(db):
    return 10.0 ** (db / 20.0)


def peak_dbfs(x):
    p = max((abs(v) for v in x), default=0.0)
    return round(20 * math.log10(p), 2) if p > 0 else None


def rms_dbfs(x):
    if not x:
        return None
    r = math.sqrt(sum(v * v for v in x) / len(x))
    return round(20 * math.log10(r), 2) if r > 0 else None


def adsr(n_total, a, d, s, r, sr=SR):
    """Linear ADSR envelope of n_total samples; a/d/r in seconds, s = sustain level 0..1."""
    na, nd, nr = int(a * sr), int(d * sr), int(r * sr)
    env = []
    for i in range(n_total):
        if i < na:
            e = i / max(na, 1)
        elif i < na + nd:
            e = 1.0 - (1.0 - s) * (i - na) / max(nd, 1)
        else:
            e = s
        tail = n_total - i
        if tail < nr:
            e *= tail / max(nr, 1)
        env.append(e)
    return env


def osc(kind, freq, n, sr=SR, phase=0.0):
    out, ph, inc = [], phase, freq / sr
    for _ in range(n):
        if kind == "sine":
            out.append(math.sin(2 * math.pi * ph))
        else:  # naive saw; aliasing is softened by the low-pass that always follows it
            out.append(2.0 * (ph - math.floor(ph + 0.5)))
        ph += inc
    return out


def onepole_lp(x, cutoff_hz, sr=SR):
    a = 1.0 - math.exp(-2.0 * math.pi * cutoff_hz / sr)
    y, out = 0.0, []
    for v in x:
        y += a * (v - y)
        out.append(y)
    return out


def mix_into(dst, src, start, gain=1.0):
    for i, v in enumerate(src):
        j = start + i
        if j >= len(dst):
            break
        dst[j] += v * gain


def normalize(x, target_dbfs):
    p = max((abs(v) for v in x), default=0.0)
    if p == 0:
        return x
    g = db_to_gain(target_dbfs) / p
    return [v * g for v in x]


def write_wav(path, samples, sr=SR):
    """Write mono 16-bit PCM WAV; clamps to [-1, 1]."""
    data = array.array("h", (int(max(-1.0, min(1.0, v)) * 32767) for v in samples))
    if sys.byteorder == "big":
        data.byteswap()
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(data.tobytes())


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def render(style, bpm, bars, seed, mood):
    st = STYLES[style]
    rng = random.Random(seed)
    beat_s = 60.0 / bpm
    bar_n = int(round(BEATS_PER_BAR * beat_s * SR))
    total = bar_n * bars
    pad, pluck, perc = [0.0] * total, [0.0] * total, [0.0] * total
    root = st["root_hz"]
    for b in range(bars):
        chord = st["prog"][b % len(st["prog"])]
        start = b * bar_n
        env = adsr(bar_n, 0.3, 0.2, 0.8, 0.4)
        for semi in chord:  # pad: three detuned-free saws through the mood low-pass
            f = root / 2 * 2 ** (semi / 12)
            tone = osc("saw", f, bar_n, phase=rng.random())
            mix_into(pad, [t * e for t, e in zip(tone, env)], start, 0.25)
        eighth = bar_n // (BEATS_PER_BAR * 2)
        for k in range(BEATS_PER_BAR * 2):  # pluck: seeded arpeggio on eighth notes
            if rng.random() < 0.15:
                continue  # seeded rests keep it from sounding mechanical
            f = root * 2 ** (rng.choice(chord) / 12)
            n = int(0.35 * SR)
            note = [t * e for t, e in zip(osc("sine", f, n), adsr(n, 0.005, 0.25, 0.0, 0.05))]
            mix_into(pluck, note, start + k * eighth, 0.5 * (0.8 + 0.2 * rng.random()))
        beat_n = bar_n // BEATS_PER_BAR
        for k in range(BEATS_PER_BAR):  # perc: soft kick on 1/3, brush or tick on 2/4
            pos = start + k * beat_n
            if k % 2 == 0 and st["perc"] == "kick":
                n = int(0.15 * SR)
                kick, ph = [], 0.0
                for i in range(n):
                    f = 50 + 70 * math.exp(-i / (0.03 * SR))
                    ph += f / SR
                    kick.append(math.sin(2 * math.pi * ph) * math.exp(-i / (0.05 * SR)))
                mix_into(perc, kick, pos, 0.9)
            elif k % 2 == 1:
                n = int(0.08 * SR)
                noise = [(rng.random() * 2 - 1) * math.exp(-i / (0.02 * SR)) for i in range(n)]
                lp = onepole_lp(noise, 2500)
                mix_into(perc, [a - b2 for a, b2 in zip(noise, lp)], pos, 0.6 * (0.85 + 0.15 * rng.random()))
    cutoff, gain_db = MOODS[mood]
    pad = onepole_lp(pad, cutoff)
    if mood == "somber":  # [V4-MP 11] "muffle it (low-pass) for somber moments"
        pluck, perc = onepole_lp(pluck, cutoff), onepole_lp(perc, cutoff)
    stems = {"pad": pad, "pluck": pluck, "perc": perc}
    g = db_to_gain(gain_db)
    swell_n = min(2, bars) * bar_n
    for name in stems:
        x = normalize(stems[name], HEADROOM_DBFS)
        if mood == "endcard":  # [V4-MP 11] "let it swell slightly on the end card": -6 dB -> 0 dB over the last bars
            lo = db_to_gain(-6.0)
            x = [v * (lo if i < total - swell_n else lo + (1 - lo) * (i - (total - swell_n)) / swell_n) for i, v in enumerate(x)]
        stems[name] = [v * g for v in x]
    return stems, bar_n, total


def validate(style, bpm, bars, seed, mood):
    errs = []
    if style not in STYLES:
        errs.append(f"unknown style {style!r}; expected one of {sorted(STYLES)}")
    if not (60 <= bpm <= 180):
        errs.append("bpm outside the guard range 60-180 (fixed tempo per bed)")
    if not (1 <= bars <= 512):
        errs.append("bars must be 1-512")
    if mood not in MOODS:
        errs.append(f"unknown mood {mood!r}; expected one of {sorted(MOODS)}")
    if not isinstance(seed, int):
        errs.append("seed must be an integer (unseeded randomness is forbidden, #17/[N61])")
    return errs


def compose(style, bpm, bars, seed, mood, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stems, bar_n, total = render(style, bpm, bars, seed, mood)
    meta_stems = []
    for name, x in stems.items():
        p = out / f"{name}.wav"
        write_wav(p, x)
        meta_stems.append({"name": name, "file": p.name, "sha256": sha256_file(p),
                           "peak_dbfs": peak_dbfs(x), "rms_dbfs": rms_dbfs(x)})
    beat_s = bar_n / BEATS_PER_BAR / SR
    meta = {
        "schema_version": "1.0", "generator": "examleaf-audio-compose/compose_bed.py",
        "style": style, "bpm": bpm, "beats_per_bar": BEATS_PER_BAR, "bars": bars, "seed": seed, "mood": mood,
        "sample_rate": SR, "bit_depth": 16, "channels": 1,
        "samples": total, "duration_s": round(total / SR, 6),
        "bar_times_s": [round(b * bar_n / SR, 6) for b in range(bars)],
        "beat_times_s": [round(k * beat_s, 6) for k in range(bars * BEATS_PER_BAR)],
        "stems": meta_stems,
        "contains_samples": False,
        "licence": "Generated in-house by deterministic code from a seed; no third-party samples.",
        "mastering": "Not mastered. examleaf-audio-production-engineer owns loudness; place the bed 20-24 dB under voice, only in hooks/transitions/recaps/outros (AD-15, 15 Oct 2026).",
    }
    (out / "bed_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def selftest():
    with tempfile.TemporaryDirectory() as d:
        # 120 BPM, 1 bar = exactly 2.0 s
        m1 = compose("paper-collage-vertical", 120, 1, 1, "neutral", Path(d) / "a")
        for s in m1["stems"]:
            with wave.open(str(Path(d) / "a" / s["file"]), "rb") as w:
                assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, SR), "header"
                assert w.getnframes() == 2 * SR, f"length {w.getnframes()}"
        assert m1["duration_s"] == 2.0 and m1["beat_times_s"] == [0.0, 0.5, 1.0, 1.5]
        m2 = compose("paper-collage-vertical", 120, 1, 1, "neutral", Path(d) / "b")
        assert [s["sha256"] for s in m1["stems"]] == [s["sha256"] for s in m2["stems"]], "same seed must be byte-identical"
        m3 = compose("paper-collage-vertical", 120, 1, 2, "neutral", Path(d) / "c")
        assert m1["stems"][1]["sha256"] != m3["stems"][1]["sha256"], "different seed must change the pluck stem"
        som = compose("paper-collage-vertical", 120, 1, 1, "somber", Path(d) / "s")
        assert som["stems"][0]["peak_dbfs"] < m1["stems"][0]["peak_dbfs"], "somber must be quieter"
        stems, bar_n, total = render("editorial-vox", 120, 2, 5, "endcard")
        first = rms_dbfs(stems["pad"][:bar_n // 2])
        last = rms_dbfs(stems["pad"][-bar_n // 2:])
        assert last > first, "endcard swell must rise"
        assert all(peak_dbfs(x) <= HEADROOM_DBFS + 0.01 for x in stems.values()), "headroom"
        assert validate("nope", 300, 0, None, "x") and not validate("kinetic-type", 100, 4, 0, "neutral")
    print("compose_bed selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--style", default="paper-collage-vertical")
    ap.add_argument("--bpm", type=float, default=100.0)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--bars", type=int)
    g.add_argument("--seconds", type=float, help="rounded UP to whole bars")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--mood", default="neutral")
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out_dir or (a.bars is None and a.seconds is None):
        ap.print_usage(sys.stderr)
        return 2
    bars = a.bars if a.bars is not None else math.ceil(a.seconds / (BEATS_PER_BAR * 60.0 / a.bpm) - 1e-9)
    errs = validate(a.style, a.bpm, bars, a.seed, a.mood)
    if errs:
        return blocker("invalid bed request", details=errs)
    try:
        meta = compose(a.style, a.bpm, bars, a.seed, a.mood, a.out_dir)
    except OSError as e:
        print(f"IO error: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "ok", "bars": meta["bars"], "duration_s": meta["duration_s"],
                      "meta": str(Path(a.out_dir) / "bed_meta.json")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
