#!/usr/bin/env python3
"""make_motif.py - Professor Diki Simplified audio identity v1.0.0 (stdlib only, seeded, owned).

Writes, next to this file:
  diki_end_motif_v1.wav  three-note end motif, 0.70 s  (E5 -> G5 -> C5: "question -> answer")
  confirm_tick_v1.wav    correct-reveal accent, 0.10 s (the motif's answer pitch C, one octave up)
  mismatch_v1.wav        muted "not equal" accent, 0.14 s (E4 + F4 a semitone apart, low-passed)
  motif_meta.json        notes, timings, peaks, sha256 (+ FFmpeg measurements with --measure)

Conventions are those of examleaf-audio-compose (helpers imported from compose_bed.py and sfx_palette.py):
48 kHz, 16-bit, mono, peak -6 dBFS, seeded per sound so re-renders are byte-identical.

Usage:
  python3 make_motif.py [--seed 2026] [--measure /path/to/ffmpeg]
  python3 make_motif.py --selftest
Exit codes: 0 ok, 1 validation failed, 2 usage/IO error.
"""
import argparse, json, math, random, re, subprocess, sys, tempfile, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.dont_write_bytecode = True                       # never leave __pycache__ in the shared skill folder
sys.path.insert(0, str(ROOT / "12_advanced_animations_with_claude/03_skills/examleaf-audio-compose/scripts"))
from compose_bed import SR, adsr, onepole_lp, mix_into, normalize, write_wav, sha256_file, peak_dbfs  # noqa: E402
from sfx_palette import fade  # noqa: E402

VERSION = "1.0.0"
PEAK_DBFS = -6.0
DEFAULT_SEED = 2026


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


# (name, midi, onset_s, gain, decay_s). Short-short-long: two pickup notes ask, the held third note answers.
MOTIF_NOTES = [("E5", 76, 0.000, 0.80, 0.10), ("G5", 79, 0.110, 0.85, 0.10), ("C5", 72, 0.240, 1.00, 0.20)]
MOTIF_LEN_S = 0.70


def mallet(f, n, rng, decay, attack=0.012):
    """Soft mallet tone: fundamental + 2nd and 3rd partials that die faster; seeded phase and tiny detune."""
    det = 1 + (rng.random() - 0.5) * 0.002          # +-0.1 % detune (about +-1.7 cents)
    ph = [rng.random() for _ in range(3)]
    parts = [(1.0, 1.0, decay), (2.0, 0.28, decay * 0.45), (3.0, 0.10, decay * 0.25)]
    na = int(attack * SR)
    out = []
    for i in range(n):
        t = i / SR
        a = 0.5 - 0.5 * math.cos(math.pi * min(1.0, i / max(na, 1)))   # raised-cosine attack: soft, no click
        out.append(a * sum(g * math.sin(2 * math.pi * (f * det * r * t + p)) * math.exp(-t / d)
                           for (r, g, d), p in zip(parts, ph)))
    return out


def room(x, wet=0.14):
    """Small, dry room: three feedback combs (prime-length delays, 23-37 ms) and one allpass."""
    out = [0.0] * len(x)
    for ms, fb in ((23.3, 0.42), (29.7, 0.38), (37.1, 0.34)):
        d, buf = int(ms * SR / 1000), [0.0] * len(x)
        for i, v in enumerate(x):
            buf[i] = v + (fb * buf[i - d] if i >= d else 0.0)
        mix_into(out, buf, 0, 1 / 3)
    out = onepole_lp(out, 4500)                      # darken the tail so it reads as a room, not a metal plate
    d, g, ap = int(0.005 * SR), 0.5, [0.0] * len(out)
    for i, v in enumerate(out):
        xd = out[i - d] if i >= d else 0.0
        yd = ap[i - d] if i >= d else 0.0
        ap[i] = -g * v + xd + g * yd
    return [a + wet * b for a, b in zip(x, ap)]


def end_motif(seed):
    rng = random.Random(f"{seed}:end_motif")
    n = int(MOTIF_LEN_S * SR)
    dry = [0.0] * n
    timings = []
    for name, midi, onset, gain, decay in MOTIF_NOTES:
        jitter = (rng.random() - 0.5) * 0.004         # seeded +-2 ms humanisation
        start = max(0, int((onset + jitter) * SR))
        g = gain * 10 ** (((rng.random() - 0.5) * 0.6) / 20)   # +-0.3 dB velocity
        mix_into(dry, mallet(hz(midi), n - start, rng, decay), start, g)
        timings.append({"note": name, "midi": midi, "hz": round(hz(midi), 2), "onset_s": round(start / SR, 4)})
    x = room(dry)
    tail = int(0.08 * SR)                            # 80 ms cosine release so the file ends in silence
    x = [v * (0.5 + 0.5 * math.cos(math.pi * max(0, i - (n - tail)) / tail)) if i >= n - tail else v
         for i, v in enumerate(x)]
    return x, timings


def confirm_tick(seed):
    rng = random.Random(f"{seed}:confirm_tick")
    n = int(0.100 * SR)
    x = [a + 0.35 * b for a, b in zip(mallet(hz(84), n, rng, 0.025, attack=0.003),
                                     mallet(hz(91), n, rng, 0.012, attack=0.003))]   # C6 + G6 glint
    return fade(x, 0.002, 0.015)


def mismatch(seed):
    rng = random.Random(f"{seed}:mismatch")
    n = int(0.140 * SR)
    env = adsr(n, 0.010, 0.05, 0.5, 0.06)
    x = [e * (a + b) for e, a, b in zip(env, mallet(hz(64), n, rng, 0.08, attack=0.008),
                                         mallet(hz(65), n, rng, 0.08, attack=0.008))]   # E4 vs F4: they beat
    return fade(onepole_lp(onepole_lp(x, 1100), 1100), 0.002, 0.02)


SOUNDS = [
    ("diki_end_motif_v1.wav", "end_motif", "Once per video, on the end card, after the spoken outro ends; never under speech."),
    ("confirm_tick_v1.wav", "confirm_tick", "On a correct reveal (answer shown after the learner's attempt); never over a spoken number."),
    ("mismatch_v1.wav", "mismatch", "On a RevealMismatch event (two quantities shown not equal); never over a spoken number."),
]
LIMITS = {"end_motif": (0.60, 0.75), "confirm_tick": (0.02, 0.120), "mismatch": (0.02, 0.150)}


def build(out_dir, seed):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    items, timings = [], None
    for fname, kind, rule in SOUNDS:
        if kind == "end_motif":
            x, timings = end_motif(seed)
        else:
            x = {"confirm_tick": confirm_tick, "mismatch": mismatch}[kind](seed)
        x = normalize(x, PEAK_DBFS)
        p = out_dir / fname
        write_wav(p, x)
        items.append({"file": fname, "kind": kind, "duration_s": round(len(x) / SR, 4),
                      "peak_dbfs": peak_dbfs(x), "sha256": sha256_file(p), "placement_rule": rule})
    return {
        "schema_version": "1.0", "asset_version": VERSION, "brand": "Professor Diki Simplified",
        "generator": "17_professor_diki_simplified/brand/motif/make_motif.py",
        "generator_sha256": sha256_file(Path(__file__)), "seed": seed,
        "sample_rate": SR, "bit_depth": 16, "channels": 1, "target_peak_dbfs": PEAK_DBFS,
        "contains_samples": False, "composed_by_human": False,
        "licence": "Generated in-house by deterministic code; owned; no third-party samples. Never describe as human-composed.",
        "motif": {
            "notes": timings,
            "intervals": ["minor third up (E5->G5): the lift of a spoken question",
                          "perfect fifth down (G5->C5): falls onto the tonic, a settled answer"],
            "rhythm": "short-short-long; onsets 0, 110, 240 ms; C5 rings into a small room; 80 ms release",
            "why": "All three notes belong to one C major triad, so the figure is consonant and calm. The rising "
                   "minor third imitates question intonation, the drop of a fifth to the tonic imitates a "
                   "declarative answer: 'question -> answer' in 0.7 s. Fundamentals 523-784 Hz sit in the band "
                   "phone speakers reproduce; no sub-bass, no percussion hit.",
            "length_s": MOTIF_LEN_S},
        "items": items}


def measure(ffmpeg, wav):
    """FFmpeg astats (sample peak, sample count) and ebur128 (true peak, integrated loudness)."""
    r = subprocess.run([ffmpeg, "-hide_banner", "-nostats", "-i", str(wav), "-af",
                        "astats=measure_overall=Peak_level+Number_of_samples:measure_perchannel=none,ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True, check=True)
    err = r.stderr

    def last(pat):
        m = re.findall(pat, err)
        return float(m[-1]) if m else None
    n = last(r"Number of samples:\s*([\d.]+)")
    short = bool(n) and n / SR < 0.4   # below one 400 ms gating block ebur128 reports a floor value, not loudness
    return {"tool": "ffmpeg astats + ebur128=peak=true",
            "sample_peak_dbfs": last(r"Peak level dB:\s*(-?[\d.]+)"),
            "true_peak_dbtp": last(r"Peak:\s*(-?[\d.]+)\s*dBFS"),
            "integrated_lufs": None if short else last(r"I:\s*(-?[\d.]+)\s*LUFS"),
            "samples": int(n) if n else None,
            "duration_s": round(n / SR, 4) if n else None}


def validate(meta):
    problems = []
    for it in meta["items"]:
        lo, hi = LIMITS[it["kind"]]
        if not lo <= it["duration_s"] <= hi:
            problems.append(f"{it['file']}: duration {it['duration_s']} s outside {lo}-{hi}")
        if it["peak_dbfs"] > PEAK_DBFS + 0.01:
            problems.append(f"{it['file']}: peak {it['peak_dbfs']} dBFS above {PEAK_DBFS}")
    return problems


def selftest():
    with tempfile.TemporaryDirectory() as d:
        a, b = build(Path(d) / "a", DEFAULT_SEED), build(Path(d) / "b", DEFAULT_SEED)
        assert [i["sha256"] for i in a["items"]] == [i["sha256"] for i in b["items"]], "determinism"
        c = build(Path(d) / "c", DEFAULT_SEED + 1)
        assert a["items"][0]["sha256"] != c["items"][0]["sha256"], "seed has no effect"
        assert not validate(a), validate(a)
        for it in a["items"]:
            with wave.open(str(Path(d) / "a" / it["file"]), "rb") as w:
                assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, SR), it["file"]
        bad = json.loads(json.dumps(a))
        bad["items"][1]["duration_s"] = 0.2
        assert validate(bad), "validator must reject a 200 ms tick"
    print("make_motif selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument("--measure", metavar="FFMPEG", help="path to an ffmpeg binary; adds measurements to the meta file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    meta = build(HERE, a.seed)
    if a.measure:
        try:
            for it in meta["items"]:
                it["measured"] = measure(a.measure, HERE / it["file"])
        except (OSError, subprocess.CalledProcessError) as e:
            print(f"ffmpeg measurement failed: {e}", file=sys.stderr)
            return 2
    problems = validate(meta)
    (HERE / "motif_meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "blocked" if problems else "ok", "problems": problems,
                      "items": [{k: i[k] for k in ("file", "duration_s", "peak_dbfs")} for i in meta["items"]]}, indent=2))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
