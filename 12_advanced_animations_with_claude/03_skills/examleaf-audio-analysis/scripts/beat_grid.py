#!/usr/bin/env python3
"""beat_grid.py - beat grid, onsets and energy envelope for music beds and Reels -> analysis.json.

Usage:
  python3 beat_grid.py --bed-meta jobs/<id>/audio/bed/bed_meta.json --out analysis.json        # own bed: no librosa needed
  python3 beat_grid.py --audio licensed_bed.wav --out analysis.json [--start-bpm 100 | --prior-norm 100 10]
                       [--bpm-curve bpm.json] [--words alignment.json] [--hop 512]
  python3 beat_grid.py --selftest      # stdlib only: exercises every guard on a synthetic onset envelope

librosa (and numpy, scipy for --prior-norm) are imported lazily, only for --audio. This script never installs them.
Exit codes: 0 ok, 1 validation failed (blocker JSON on stdout), 2 usage/IO/dependency error.
Guards (report 8 / librosa 0.11 docs):
  #31 stereo + sparse=True unsupported -> downmix to mono first [N37][N43]
  #32 tempo is an ndarray even for mono -> tempo_scalar() [N38]
  #33 beats default to frames -> units='time' always, plus a beats<=duration check [N39]
  #34 silent/beatless -> 0 BPM and empty beats -> fallback to narration grid [N41]
  #35 librosa.load resamples to 22050 Hz by default -> sr=None, one sr everywhere [N81]
  #36 ParameterError on missing y/onset_envelope or bad units -> validate first, catch, report [N40]
  #37 start_bpm is ignored when a prior is given -> refuse both [N36]
  #38 time-varying bpm must match onset_envelope shape [N42]
"""
import argparse, hashlib, json, math, random, statistics, sys
from pathlib import Path

VALID_UNITS = ("frames", "samples", "time")
PHRASE_GAP_S = 0.12  # [Recommendation] a word that follows a pause >= this starts a narration-grid "beat"


class GuardError(ValueError):
    def __init__(self, edge, msg):
        super().__init__(f"{edge}: {msg}")
        self.edge = edge


def tempo_scalar(tempo):
    """#32 [N38]: librosa returns tempo as an ndarray even for mono input. Returns (bpm, varies)."""
    if hasattr(tempo, "ravel"):
        tempo = tempo.ravel().tolist()
    if isinstance(tempo, (list, tuple)):
        vals = [float(v) for v in tempo]
        if not vals:
            return 0.0, False
        return (statistics.median(vals), len(set(vals)) > 1) if len(vals) > 1 else (vals[0], False)
    return float(tempo), False


def check_call_args(y_present, onset_present, units, start_bpm, prior_present):
    """#36 [N40] and #37 [N36]: fail before librosa does."""
    if not y_present and not onset_present:
        raise GuardError("#36", "neither y nor onset_envelope supplied (librosa would raise ParameterError)")
    if units not in VALID_UNITS:
        raise GuardError("#36", f"units={units!r} is not one of {VALID_UNITS}")
    if units != "time":
        raise GuardError("#33", "ExamLeaf requires units='time' (librosa defaults to frames)")
    if start_bpm is not None and prior_present:
        raise GuardError("#37", "start_bpm is ignored when a prior is given; pass one or the other")


def check_bpm_shape(bpm_len, onset_len):
    """#38 [N42]."""
    if bpm_len is not None and bpm_len not in (1, onset_len):
        raise GuardError("#38", f"bpm curve has {bpm_len} values but onset_envelope has {onset_len}")


def check_channels(channels, sparse):
    """#31 [N37]: multi-channel only with sparse=False; ExamLeaf downmixes instead (keeps a sparse beat list)."""
    if channels > 1 and sparse:
        raise GuardError("#31", "multi-channel input with sparse=True; downmix to mono first")


def check_sr(load_sr, analysis_sr):
    """#35 [N81]: every frame->time conversion must use the sr the audio was loaded at."""
    if load_sr != analysis_sr:
        raise GuardError("#35", f"audio loaded at {load_sr} Hz but converted with {analysis_sr} Hz: cues will drift")


def check_beats(beats, duration):
    """#33: beats returned in frames look like values far beyond the clip length."""
    bad = [b for b in beats if b < 0 or b > duration + 1e-3]
    if bad:
        raise GuardError("#33", f"{len(bad)} beat(s) outside [0, {duration:.3f}] s: units are not seconds")
    if any(b2 <= b1 for b1, b2 in zip(beats, beats[1:])):
        raise GuardError("#33", "beats are not strictly increasing")


def narration_grid(words):
    """#34 fallback: phrase onsets from aligned words ({text,start,end}); first word always included."""
    grid, prev_end = [], None
    for w in words:
        if prev_end is None or w["start"] - prev_end >= PHRASE_GAP_S:
            grid.append(round(float(w["start"]), 4))
        prev_end = w["end"]
    return grid


def resolve_beats(bpm, beats, duration, words):
    """#34 [N41]: 0 BPM / empty list -> narration grid (if words) else none. Returns (beats, fallback, warnings)."""
    if bpm > 0 and beats:
        check_beats(beats, duration)
        return [round(b, 4) for b in beats], None, []
    warn = [f"#34 beat tracker returned {bpm:g} BPM and {len(beats)} beats (silent or beatless audio) [N41]"]
    if words:
        return narration_grid(words), "narration_grid", warn
    return [], "none", warn + ["no alignment supplied: cue sheet gets an empty beats list"]


def toy_beat_track(onset_env, hop_s, lo_bpm=60, hi_bpm=180):
    """TEST-ONLY stand-in for librosa.beat.beat_track on an onset envelope (autocorrelation + best phase).
    Used by --selftest so the guard logic runs without librosa. Never used for production analysis."""
    n = len(onset_env)
    if n == 0 or max(onset_env) <= 0:
        return [0.0], []
    best_lag, best = None, -1.0
    for lag in range(max(1, int(60 / hi_bpm / hop_s)), int(60 / lo_bpm / hop_s) + 1):
        s = sum(onset_env[i] * onset_env[i + lag] for i in range(n - lag))
        if s > best:
            best, best_lag = s, lag
    phase = max(range(best_lag), key=lambda p: sum(onset_env[p::best_lag]))
    return [60.0 / (best_lag * hop_s)], [round(i * hop_s, 4) for i in range(phase, n, best_lag)]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def from_bed_meta(meta_path, words):
    meta = json.loads(Path(meta_path).read_text(encoding="utf-8"))
    beats = [float(b) for b in meta["beat_times_s"]]
    check_beats(beats, meta["duration_s"])
    return {"schema_version": "1.0", "engine": {"name": "bed_metadata", "version": meta.get("generator")},
            "source": {"path": str(meta_path), "sha256": sha256_file(meta_path), "sr_native": meta["sample_rate"],
                       "sr_used": meta["sample_rate"], "channels": meta["channels"], "duration_s": meta["duration_s"]},
            "params": {"units": "time", "note": "grid taken from compose_bed.py metadata; no detection needed"},
            "tempo_bpm": float(meta["bpm"]), "tempo_varies": False, "beats_s": beats,
            "downbeats_s": [float(b) for b in meta["bar_times_s"]], "onsets_s": None, "energy": None,
            "fallback": None, "warnings": []}


def analyse_audio(path, hop, start_bpm, prior_norm, bpm_curve, words):
    try:  # lazy heavy imports (#guard: clear message, no install)
        import numpy as np
        import librosa
    except ImportError as e:
        raise RuntimeError(f"librosa/numpy not importable ({e}). Use the approved audio environment; "
                           "this skill does not install packages. For ExamLeaf-composed beds pass --bed-meta instead.")
    warnings = []
    y, sr = librosa.load(path, sr=None, mono=False)  # #35 keep native rate [N81]
    channels = 1 if y.ndim == 1 else int(y.shape[0])
    if channels > 1:
        y = librosa.to_mono(y)  # #31 [N37]
        warnings.append(f"#31 downmixed {channels} channels to mono before beat tracking")
    check_channels(1, sparse=True)
    duration = float(y.shape[-1]) / sr
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop)
    prior = None
    if prior_norm:
        from scipy import stats  # librosa expects a scipy.stats distribution for prior (verify on pinned version)
        prior = stats.norm(loc=prior_norm[0], scale=prior_norm[1])
    check_call_args(True, True, "time", start_bpm, prior is not None)
    bpm_arr = None
    if bpm_curve is not None:
        bpm_arr = np.asarray(bpm_curve, dtype=float)
        check_bpm_shape(bpm_arr.size, onset_env.shape[-1])
        if bpm_arr.size != 1:
            bpm_arr = bpm_arr.reshape(onset_env.shape)
    kwargs = {"onset_envelope": onset_env, "sr": sr, "hop_length": hop, "units": "time"}
    if start_bpm is not None:
        kwargs["start_bpm"] = start_bpm
    if prior is not None:
        kwargs["prior"] = prior
    if bpm_arr is not None:
        kwargs["bpm"] = bpm_arr
    try:
        tempo, beats = librosa.beat.beat_track(**kwargs)
    except librosa.util.exceptions.ParameterError as e:  # #36 [N40]
        raise GuardError("#36", f"librosa ParameterError: {e}")
    bpm, varies = tempo_scalar(tempo)
    beats_s, fallback, w = resolve_beats(bpm, [float(b) for b in beats], duration, words)
    warnings += w
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr, hop_length=hop, units="time")
    rms = librosa.feature.rms(y=y, hop_length=hop)[0]
    check_sr(sr, sr)
    return {"schema_version": "1.0", "engine": {"name": "librosa", "version": getattr(librosa, "__version__", None)},
            "source": {"path": str(path), "sha256": sha256_file(path), "sr_native": int(sr), "sr_used": int(sr),
                       "channels": channels, "duration_s": round(duration, 6)},
            "params": {"units": "time", "hop_length": hop, "start_bpm": start_bpm,
                       "prior": None if prior_norm is None else {"dist": "norm", "loc": prior_norm[0], "scale": prior_norm[1]},
                       "bpm_curve": bpm_curve is not None, "sparse": True},
            "tempo_bpm": round(bpm, 3), "tempo_varies": varies, "beats_s": beats_s, "downbeats_s": None,
            "onsets_s": [round(float(t), 4) for t in onsets],
            "energy": {"hop_s": hop / sr, "rms": [round(float(v), 5) for v in rms]},
            "fallback": fallback, "warnings": warnings}


def selftest():
    hop_s = 0.01
    rng = random.Random(7)
    env = [0.05 * rng.random() for _ in range(1000)]  # 10 s synthetic onset envelope
    for i in range(0, 1000, 60):                         # an onset every 0.6 s = 100 BPM
        env[i] = 1.0
    t, beats = toy_beat_track(env, hop_s)
    bpm, varies = tempo_scalar(t)
    assert abs(bpm - 100.0) < 0.5 and not varies, bpm
    assert all(abs((b2 - b1) - 0.6) < 1e-6 for b1, b2 in zip(beats, beats[1:])), "grid spacing"
    out, fb, _ = resolve_beats(bpm, beats, 10.0, None)
    assert fb is None and out[0] == 0.0
    # #32 tempo shapes
    assert tempo_scalar([120.0]) == (120.0, False) and tempo_scalar(99) == (99.0, False)
    assert tempo_scalar((90.0, 110.0)) == (100.0, True) and tempo_scalar([]) == (0.0, False)
    # #34 silent envelope -> 0 BPM / empty -> narration grid
    t0, b0 = toy_beat_track([0.0] * 500, hop_s)
    words = [{"text": "light", "start": 0.10, "end": 0.40}, {"text": "bends", "start": 0.42, "end": 0.70},
             {"text": "here", "start": 1.10, "end": 1.40}]
    grid, fb, warn = resolve_beats(tempo_scalar(t0)[0], b0, 5.0, words)
    assert fb == "narration_grid" and grid == [0.1, 1.1] and warn
    assert resolve_beats(0.0, [], 5.0, None)[1] == "none"

    def raises(edge, fn, *a):
        try:
            fn(*a)
        except GuardError as e:
            assert e.edge == edge, (e.edge, edge)
            return
        raise AssertionError(f"{edge} guard did not fire")
    raises("#31", check_channels, 2, True)
    raises("#33", check_beats, [0.5, 1.0, 400.0], 10.0)      # frames, not seconds
    raises("#33", check_call_args, True, False, "frames", None, False)
    raises("#35", check_sr, 48000, 22050)
    raises("#36", check_call_args, False, False, "time", None, False)
    raises("#36", check_call_args, True, False, "beats", None, False)
    raises("#37", check_call_args, True, True, "time", 100.0, True)
    raises("#38", check_bpm_shape, 7, 1000)
    check_bpm_shape(1000, 1000)
    check_bpm_shape(None, 1000)
    try:
        import librosa  # noqa: F401
        print("note: librosa importable; --selftest still uses only the stdlib guard path")
    except ImportError:
        print("note: librosa not installed; --audio mode would exit 2 with a clear message (expected offline)")
    print("beat_grid selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--audio")
    src.add_argument("--bed-meta")
    ap.add_argument("--out")
    ap.add_argument("--hop", type=int, default=512)
    ap.add_argument("--start-bpm", type=float)
    ap.add_argument("--prior-norm", type=float, nargs=2, metavar=("MEAN", "STD"))
    ap.add_argument("--bpm-curve", help="JSON list: one bpm per onset frame, or a single value")
    ap.add_argument("--words", help="alignment JSON with words[{text,start,end}] for the #34 fallback")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.out or not (a.audio or a.bed_meta):
        ap.print_usage(sys.stderr)
        return 2
    try:
        words = json.loads(Path(a.words).read_text(encoding="utf-8"))["words"] if a.words else None
        if a.bed_meta:
            result = from_bed_meta(a.bed_meta, words)
        else:
            curve = json.loads(Path(a.bpm_curve).read_text(encoding="utf-8")) if a.bpm_curve else None
            result = analyse_audio(a.audio, a.hop, a.start_bpm, a.prior_norm, curve, words)
    except GuardError as e:
        print(json.dumps({"status": "blocked", "skill": "examleaf-audio-analysis", "edge_case": e.edge, "error": str(e)}, indent=2))
        return 1
    except (RuntimeError, OSError, KeyError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    Path(a.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"status": "ok", "tempo_bpm": result["tempo_bpm"], "beats": len(result["beats_s"]),
                      "fallback": result["fallback"], "out": a.out}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
