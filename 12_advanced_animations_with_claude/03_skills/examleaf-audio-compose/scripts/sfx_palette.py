#!/usr/bin/env python3
"""sfx_palette.py - seeded SFX one-shots per house style (stdlib only; reuses compose_bed.py helpers).

Usage:
  python3 sfx_palette.py --style paper-collage-vertical --seed 11 --out-dir jobs/<scene_id>/audio/sfx
  python3 sfx_palette.py --style kinetic-type --only tap,pop --seed 11 --out-dir ...
  python3 sfx_palette.py --list [--style S]
  python3 sfx_palette.py --selftest

Writes <name>.wav (48 kHz, 16-bit, mono, peak -6 dBFS, 2 ms fade-in / 5 ms fade-out) and sfx_palette.json.
Cue placement and gain_db belong to the cue sheet (examleaf-cue-sheet), not to this script.
Exit codes: 0 ok, 1 validation failed (blocker JSON on stdout), 2 usage/IO error.
Sources: paper-craft list (swish, tap, pop, boing, tear, thud, chime; booms/rumbles only for real drama) [V4-MP 11];
STEM sounds (electric hum, bubbling, click-snap) are report 5.1 [Recommendation].
"""
import argparse, json, math, random, sys, tempfile, wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compose_bed import SR, adsr, onepole_lp, normalize, write_wav, sha256_file, peak_dbfs  # noqa: E402

PEAK_DBFS = -6.0  # [Recommendation] one-shot peak; per-cue gain_db in the cue sheet sets the mix level


def _n(sec):
    return int(sec * SR)


def _noise(rng, n):
    return [rng.random() * 2 - 1 for _ in range(n)]


def _sweep_sine(f0, f1, sec, decay):
    out, ph, n = [], 0.0, _n(sec)
    for i in range(n):
        f = f0 + (f1 - f0) * i / n
        ph += f / SR
        out.append(math.sin(2 * math.pi * ph) * math.exp(-i / (decay * SR)))
    return out


def _hp(x, cutoff):
    return [a - b for a, b in zip(x, onepole_lp(x, cutoff))]


def paper_swish(rng):
    n = _n(0.35)
    x, env, out, y = _noise(rng, n), adsr(n, 0.12, 0.1, 0.5, 0.13), [], 0.0
    for i, v in enumerate(x):  # time-varying one-pole low-pass sweep 800 -> 6000 Hz
        fc = 800 + 5200 * i / n
        a = 1 - math.exp(-2 * math.pi * fc / SR)
        y += a * (v - y)
        out.append(y * env[i])
    return out


def whip(rng):
    return paper_swish(rng)[::2] + [0.0] * 10  # same material, twice as fast, for the ~0.4 s urgency whip [V4-MP 9]


def tap(rng):
    n = _n(0.04)
    click = [v * math.exp(-i / (0.004 * SR)) for i, v in enumerate(_noise(rng, n))]
    tone = _sweep_sine(2000, 1800, 0.04, 0.008)
    return [a * 0.6 + b * 0.5 for a, b in zip(click, tone)]


def pop(rng):
    return _sweep_sine(900, 300, 0.09, 0.03)


def boing(rng):
    out, ph, n = [], 0.0, _n(0.5)
    for i in range(n):
        t = i / SR
        f = 220 * (1 + 0.25 * math.exp(-t / 0.15) * math.sin(2 * math.pi * 12 * t))
        ph += f / SR
        out.append(math.sin(2 * math.pi * ph) * math.exp(-t / 0.18))
    return out


def tear(rng):
    n, out = _n(0.45), []
    gate = 0.0
    for i, v in enumerate(_noise(rng, n)):
        if i % 240 == 0:
            gate = 1.0 if rng.random() < 0.55 else 0.15  # seeded fibre crackle
        out.append(v * gate * (1 - i / n))
    return _hp(out, 1500)


def thud(rng):
    body = [a + 0.6 * b for a, b in zip(_sweep_sine(80, 60, 0.3, 0.08), _sweep_sine(45, 40, 0.3, 0.1))]
    hit = onepole_lp([v * math.exp(-i / (0.01 * SR)) for i, v in enumerate(_noise(rng, len(body)))], 400)
    return [a + 0.5 * b for a, b in zip(body, hit)]


def chime(rng):
    n, out = _n(1.2), []
    partials = [(1.0, 1.0, 0.6), (2.76, 0.5, 0.35), (5.4, 0.25, 0.2)]  # inharmonic bell partials
    for i in range(n):
        t = i / SR
        out.append(sum(g * math.sin(2 * math.pi * 880 * r * t) * math.exp(-t / d) for r, g, d in partials))
    return out


def rumble(rng):
    n = _n(1.2)
    x = onepole_lp(onepole_lp(_noise(rng, n), 120), 120)
    env = adsr(n, 0.15, 0.3, 0.7, 0.6)
    return [a * e for a, e in zip(x, env)]


def pencil(rng):
    n, out = _n(0.4), []
    x = _hp(_noise(rng, n), 3000)
    amp = 1.0
    for i, v in enumerate(x):
        if i % 480 == 0:
            amp = 0.4 + 0.6 * rng.random()  # seeded stroke pressure
        out.append(v * amp * math.sin(math.pi * i / n))
    return out


def electric_hum(rng):
    n = _n(0.8)
    env = adsr(n, 0.1, 0.0, 1.0, 0.2)
    return [env[i] * (math.sin(2 * math.pi * 100 * i / SR) + 0.5 * math.sin(2 * math.pi * 200 * i / SR)
                      + 0.25 * math.sin(2 * math.pi * 300 * i / SR) + 0.02 * (rng.random() * 2 - 1)) for i in range(n)]


def bubble(rng):
    out = [0.0] * _n(0.6)
    for _ in range(6):
        start = int(rng.random() * (len(out) - _n(0.06)))
        f0 = 300 + 500 * rng.random()
        for i, v in enumerate(_sweep_sine(f0, f0 * 2.2, 0.06, 0.02)):
            out[start + i] += v
    return out


def snap(rng):
    n = _n(0.03)
    click = [v * math.exp(-i / (0.002 * SR)) for i, v in enumerate(_noise(rng, n))]
    return [a + 0.7 * b for a, b in zip(click, _sweep_sine(3000, 2600, 0.03, 0.006))]


GENERATORS = {f.__name__: f for f in (paper_swish, whip, tap, pop, boing, tear, thud, chime, rumble,
                                      pencil, electric_hum, bubble, snap)}
STEM_EXTRAS = ["electric_hum", "bubble", "snap"]
PALETTES = {  # paper-collage list is [V4-MP 11]; the others are [Recommendation] starting palettes
    "paper-collage-vertical": ["paper_swish", "whip", "tap", "pop", "boing", "tear", "thud", "chime", "rumble"],
    "doodle-handdrawn": ["pencil", "pop", "boing", "whip", "chime", "tap"],
    "editorial-vox": ["whip", "tap", "thud", "pop", "chime", "pencil"],
    "kinetic-type": ["tap", "pop", "whip", "snap"],
    "voxel-isometric": ["pop", "snap", "thud", "chime", "whip"],
}
USE = {"paper_swish": "sheet transition", "whip": "urgency whip transition", "tap": "ransom letter / tile land",
       "pop": "cutout or label pop-in", "boing": "hop", "tear": "paper tear gag", "thud": "drop",
       "chime": "sparkle / magic moment", "rumble": "real drama only", "pencil": "doodle draw-on",
       "electric_hum": "circuit / current (STEM)", "bubble": "reaction / bubbling (STEM)", "snap": "bond click-snap (STEM)"}


def fade(x, fin=0.002, fout=0.005):
    a, b = _n(fin), _n(fout)
    return [v * min(1.0, i / max(a, 1), (len(x) - i) / max(b, 1)) for i, v in enumerate(x)]


def build(style, seed, out_dir, only=None):
    names = PALETTES[style] + STEM_EXTRAS
    if only:
        bad = [n for n in only if n not in names]
        if bad:
            raise ValueError(f"not in the {style} palette: {bad}")
        names = only
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    items = []
    for k, name in enumerate(names):
        rng = random.Random(f"{seed}:{name}")  # per-effect stream: adding one SFX never changes another
        x = fade(normalize(GENERATORS[name](rng), PEAK_DBFS))
        p = out / f"{name}.wav"
        write_wav(p, x)
        items.append({"name": name, "file": p.name, "duration_s": round(len(x) / SR, 4),
                      "peak_dbfs": peak_dbfs(x), "sha256": sha256_file(p), "use": USE[name],
                      "source": "[V4-MP 11]" if name in PALETTES["paper-collage-vertical"] else "[Recommendation]"})
    manifest = {"schema_version": "1.0", "generator": "examleaf-audio-compose/sfx_palette.py", "style": style,
                "seed": seed, "sample_rate": SR, "bit_depth": 16, "channels": 1, "contains_samples": False,
                "licence": "Generated in-house by deterministic code; no third-party samples.", "items": items}
    (out / "sfx_palette.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def selftest():
    with tempfile.TemporaryDirectory() as d:
        for style in PALETTES:
            assert all(n in GENERATORS for n in PALETTES[style]), style
        m1 = build("paper-collage-vertical", 11, Path(d) / "a")
        m2 = build("paper-collage-vertical", 11, Path(d) / "b")
        assert [i["sha256"] for i in m1["items"]] == [i["sha256"] for i in m2["items"]], "determinism"
        for it in m1["items"]:
            with wave.open(str(Path(d) / "a" / it["file"]), "rb") as w:
                assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (1, 2, SR)
                assert 0.01 <= w.getnframes() / SR <= 2.0, it["name"]
            assert it["peak_dbfs"] <= PEAK_DBFS + 0.01
        m3 = build("paper-collage-vertical", 12, Path(d) / "c", only=["tear"])
        assert m3["items"][0]["sha256"] != next(i for i in m1["items"] if i["name"] == "tear")["sha256"], "seed"
        m4 = build("paper-collage-vertical", 11, Path(d) / "e", only=["tear"])
        assert m4["items"][0]["sha256"] == next(i for i in m1["items"] if i["name"] == "tear")["sha256"], "subset stable"
        try:
            build("kinetic-type", 1, Path(d) / "f", only=["rumble"])
            raise AssertionError("rumble is not in the kinetic-type palette")
        except ValueError:
            pass
    print("sfx_palette selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--style", default="paper-collage-vertical")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--only", help="comma-separated subset of the style palette")
    ap.add_argument("--out-dir")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.style not in PALETTES:
        print(json.dumps({"status": "blocked", "error": f"unknown style {a.style!r}", "styles": sorted(PALETTES)}))
        return 1
    if a.list:
        print(json.dumps({n: USE[n] for n in PALETTES[a.style] + STEM_EXTRAS}, indent=2))
        return 0
    if a.seed is None or not a.out_dir:
        ap.print_usage(sys.stderr)
        return 2
    try:
        m = build(a.style, a.seed, a.out_dir, a.only.split(",") if a.only else None)
    except ValueError as e:
        print(json.dumps({"status": "blocked", "error": str(e)}))
        return 1
    except OSError as e:
        print(f"IO error: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "ok", "count": len(m["items"]), "manifest": str(Path(a.out_dir) / "sfx_palette.json")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
