#!/usr/bin/env python3
"""flash_check.py - per-frame luminance-delta flash test (stdlib only).

Usage:
  python3 flash_check.py --frames-dir renders/<scene>/frames --fps 30 [--grid 4] [--out flash_report.json]
  python3 flash_check.py --csv luma.csv --fps 30 [--encoding linear|srgb8]
  python3 flash_check.py --selftest

Inputs: a directory of binary/ASCII PGM or PPM frames (P2/P3/P5/P6, sorted by name), or a CSV `frame,luminance`
(linear relative luminance 0-1, or 8-bit gamma-encoded values with --encoding srgb8, which is an approximation).
Method (see references/flash_test_method.md): per tile, a "transition" is a luminance swing >= --delta (default 0.10)
from the last extreme in the opposite direction, where the darker side is < --dark-limit (default 0.80); a flash is
a pair of opposing transitions; count flashes in every sliding 1 s window.
Defaults follow the WCAG 2.x SC 2.3.1 "general flash" definition as recalled: VERIFY THE EXACT THRESHOLDS against the
current W3C text before relying on them. Red-flash and the area/visual-angle condition are NOT implemented: a
tile-only finding goes to a human. Severity: critical = >3 flashes/s on the whole frame OR any whole-frame flash
(house ban, section rule G15; raised from major on 15 Oct 2026, audit science-safety-6: never waivable); major =
>3 flashes/s in a tile (area condition not implemented, so a human judges it); pass otherwise.
Exit codes: 0 pass/minor, 1 major or critical (report JSON on stdout), 2 usage/IO error. Edge case: #56.
"""
import argparse, csv, json, sys, tempfile
from pathlib import Path


def srgb_to_linear(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


LUT8 = [srgb_to_linear(i / 255) for i in range(256)]


def read_pnm(path):
    """Return (width, height, channels, maxval, flat list of samples). Supports P2, P3, P5, P6."""
    data = Path(path).read_bytes()
    fields, pos = [], 0
    while len(fields) < 4:  # magic, width, height, maxval (comments allowed)
        while pos < len(data) and data[pos:pos + 1].isspace():
            pos += 1
        if data[pos:pos + 1] == b"#":
            while pos < len(data) and data[pos:pos + 1] not in (b"\n", b"\r"):
                pos += 1
            continue
        start = pos
        while pos < len(data) and not data[pos:pos + 1].isspace():
            pos += 1
        fields.append(data[start:pos])
    magic, w, h, maxval = fields[0].decode(), int(fields[1]), int(fields[2]), int(fields[3])
    ch = 3 if magic in ("P3", "P6") else 1
    n = w * h * ch
    if magic in ("P5", "P6"):
        raw = data[pos + 1:]
        if maxval < 256:
            vals = list(raw[:n])
        else:
            vals = [int.from_bytes(raw[i:i + 2], "big") for i in range(0, 2 * n, 2)]
    elif magic in ("P2", "P3"):
        vals = [int(x) for x in data[pos:].split()[:n]]
    else:
        raise ValueError(f"{path}: unsupported PNM magic {magic}")
    if len(vals) != n:
        raise ValueError(f"{path}: truncated image data")
    return w, h, ch, maxval, vals


def tile_luminance(path, grid):
    """Mean relative luminance per tile (row-major grid x grid)."""
    w, h, ch, maxval, vals = read_pnm(path)
    lin = (lambda v: LUT8[v]) if maxval == 255 else (lambda v: srgb_to_linear(v / maxval))
    sums, counts = [0.0] * (grid * grid), [0] * (grid * grid)
    for y in range(h):
        ty = min(grid - 1, y * grid // h)
        row = y * w * ch
        for x in range(w):
            i = row + x * ch
            if ch == 3:
                yv = 0.2126 * lin(vals[i]) + 0.7152 * lin(vals[i + 1]) + 0.0722 * lin(vals[i + 2])
            else:
                yv = lin(vals[i])
            t = ty * grid + min(grid - 1, x * grid // w)
            sums[t] += yv
            counts[t] += 1
    return [s / c for s, c in zip(sums, counts)]


def transitions(series, delta, dark_limit):
    """Frames where a swing >= delta completes, measured from the running extreme since the last transition
    (hysteresis), alternating rise/fall. Only swings whose darker side is < dark_limit are returned."""
    out = []
    if not series:
        return out
    lo = hi = series[0]
    direction = 0
    for i, v in enumerate(series):
        hi, lo = max(hi, v), min(lo, v)
        if direction <= 0 and v - lo >= delta:          # rise completed
            if lo < dark_limit:
                out.append({"frame": i, "delta": round(v - lo, 4), "darker": round(lo, 4)})
            direction, hi, lo = 1, v, v
        elif direction >= 0 and hi - v >= delta:        # fall completed
            if v < dark_limit:
                out.append({"frame": i, "delta": round(v - hi, 4), "darker": round(v, 4)})
            direction, hi, lo = -1, v, v
    return out


def max_flashes_per_window(trans, fps):
    """Max number of flashes (pairs of opposing transitions) inside any 1 s window."""
    frames = [t["frame"] for t in trans]
    best, start_f, j = 0, None, 0
    for i, f in enumerate(frames):
        while frames[j] <= f - fps:
            j += 1
        flashes = (i - j + 1) // 2
        if flashes > best:
            best, start_f = flashes, frames[j]
    return best, (None if start_f is None else round(start_f / fps, 3))


def analyse(tiles_per_frame, fps, delta=0.10, dark_limit=0.80, full=None):
    """tiles_per_frame: list of per-frame tile lists. full: optional whole-frame series (else mean of tiles)."""
    n_tiles = len(tiles_per_frame[0]) if tiles_per_frame else 0
    full = full or [sum(f) / len(f) for f in tiles_per_frame]
    ft = transitions(full, delta, dark_limit)
    full_rate, full_at = max_flashes_per_window(ft, fps)
    any_full_flash = len(ft) >= 2 and any(b["frame"] - a["frame"] <= fps for a, b in zip(ft, ft[1:]))
    tile_hits = []
    for t in range(n_tiles if n_tiles > 1 else 0):
        tr = transitions([f[t] for f in tiles_per_frame], delta, dark_limit)
        rate, at = max_flashes_per_window(tr, fps)
        if rate > 3:
            tile_hits.append({"tile": t, "max_flashes_per_s": rate, "window_start_s": at})
    if full_rate > 3 or any_full_flash:
        sev = "critical"
    elif tile_hits:
        sev = "major"
    else:
        sev = "pass"
    return {"fps": fps, "frames": len(full), "delta": delta, "dark_limit": dark_limit,
            "full_frame": {"max_flashes_per_s": full_rate, "window_start_s": full_at, "transitions": ft[:50]},
            "tiles_over_3_per_s": tile_hits, "severity": sev,
            "notes": ["thresholds from the WCAG 2.x general-flash definition as recalled - verify against the current W3C text",
                      "red-flash rule and area condition not implemented; tile findings need human review",
                      "any whole-frame flash is banned by house rule G15 even below the WCAG count"]}


def selftest():
    fps = 30
    steady = [[0.2 + 0.5 * i / 90] for i in range(90)]
    assert analyse(steady, fps)["severity"] == "pass"
    strobe = [[0.9 if (i // 3) % 2 else 0.1] for i in range(90)]           # 5 Hz square wave
    r = analyse(strobe, fps)
    assert r["severity"] == "critical" and r["full_frame"]["max_flashes_per_s"] == 5, r["full_frame"]
    bloom = [[0.2]] * 30 + [[0.95]] * 4 + [[0.2]] * 30                      # one white "bloom" transition [V4-MP 9]
    assert analyse(bloom, fps)["severity"] == "critical"                   # any whole-frame flash (15 Oct 2026)
    flicker = [[0.5 + (0.03 if i % 2 else -0.03)] for i in range(60)]       # below the delta
    assert analyse(flicker, fps)["severity"] == "pass"
    bright = [[0.95 if i % 4 < 2 else 0.85] for i in range(60)]             # both sides >= 0.80: not a flash
    assert analyse(bright, fps)["severity"] == "pass"
    with tempfile.TemporaryDirectory() as d:                                # PGM/PPM round trip, one flashing tile
        for i in range(30):
            px = []
            for y in range(4):
                for x in range(4):
                    px.append(230 if (x < 2 and y < 2 and (i // 2) % 2) else 40)
            Path(d, f"f{i:04d}.pgm").write_bytes(b"P5\n# t\n4 4\n255\n" + bytes(px))
        Path(d, "c.ppm").write_bytes(b"P3 1 1 255 255 255 255")
        assert abs(tile_luminance(Path(d, "c.ppm"), 1)[0] - 1.0) < 1e-9
        frames = [tile_luminance(p, 2) for p in sorted(Path(d).glob("*.pgm"))]
        r = analyse(frames, fps)
        assert r["tiles_over_3_per_s"] and r["tiles_over_3_per_s"][0]["tile"] == 0, r
        assert r["severity"] in ("major", "critical")
    print("flash_check selftest OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--frames-dir")
    ap.add_argument("--csv")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--grid", type=int, default=1)
    ap.add_argument("--encoding", choices=["linear", "srgb8"], default="linear")
    ap.add_argument("--delta", type=float, default=0.10)
    ap.add_argument("--dark-limit", type=float, default=0.80)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.fps or not (a.frames_dir or a.csv):
        ap.print_usage(sys.stderr)
        return 2
    try:
        if a.csv:
            with open(a.csv, newline="", encoding="utf-8") as f:
                rows = sorted(((int(r["frame"]), float(r["luminance"])) for r in csv.DictReader(f)))
            vals = [v for _, v in rows]
            if a.encoding == "srgb8":
                vals = [srgb_to_linear(v / 255) for v in vals]
            tiles = [[v] for v in vals]
        else:
            paths = sorted(p for p in Path(a.frames_dir).iterdir() if p.suffix.lower() in (".pgm", ".ppm", ".pnm"))
            if not paths:
                raise ValueError("no PGM/PPM frames found")
            tiles = [tile_luminance(p, max(1, a.grid)) for p in paths]
    except (OSError, ValueError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    rep = analyse(tiles, int(round(a.fps)), a.delta, a.dark_limit)
    rep["input"] = a.csv or a.frames_dir
    if a.encoding == "srgb8":
        rep["notes"].append("CSV was gamma-encoded 8-bit means: linearised per frame mean, an approximation")
    if a.out:
        Path(a.out).write_text(json.dumps(rep, indent=2), encoding="utf-8")
    print(json.dumps(rep, indent=2))
    return 0 if rep["severity"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
