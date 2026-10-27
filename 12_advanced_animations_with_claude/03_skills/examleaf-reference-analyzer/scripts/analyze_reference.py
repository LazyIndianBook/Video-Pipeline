#!/usr/bin/env python3
"""analyze_reference.py - turn a reference video into pacing/style numbers (stdlib + external ffmpeg/ffprobe).

Usage:
  python3 analyze_reference.py --input ref.mp4 --out analysis.json [--stills-dir DIR] [--scene-threshold 0.30]
                               [--max-stills 12] [--freeze-min 0.5]
  python3 analyze_reference.py --selftest      (offline; uses synthetic FFmpeg logs, needs no ffmpeg)

The FFmpeg/ffprobe invocations below are standard FFmpeg usage; verify them on your build (`ffmpeg -version`).
Rights: references are analysed only. Stills go to a quarantine folder for internal study and are never assets.
Exit codes: 0 ok, 1 analysis failed, 2 blocker (missing ffmpeg/ffprobe or unreadable input).
"""
import argparse, hashlib, json, os, re, shutil, statistics, subprocess, sys
from fractions import Fraction

SCHEMA = "1.0"


# ---------- pure parsers (unit-tested by --selftest) ----------
def parse_rate(s):
    try:
        f = Fraction(str(s))
        return float(f) if f > 0 else None
    except (ValueError, ZeroDivisionError):
        return None


def parse_probe(probe_json):
    d = json.loads(probe_json) if isinstance(probe_json, str) else probe_json
    st = (d.get("streams") or [{}])[0]
    fmt = d.get("format") or {}
    r, a = parse_rate(st.get("r_frame_rate")), parse_rate(st.get("avg_frame_rate"))
    vfr = bool(r and a and abs(r - a) / r > 0.01)
    dur = float(fmt.get("duration") or st.get("duration") or 0) or None
    w, h = st.get("width"), st.get("height")
    return {"width": w, "height": h, "duration_s": dur, "codec": st.get("codec_name"),
            "r_frame_rate": st.get("r_frame_rate"), "avg_frame_rate": st.get("avg_frame_rate"),
            "fps": round(a or r, 3) if (a or r) else None, "vfr_suspected": vfr,
            "orientation": None if not (w and h) else ("portrait" if h > w else "landscape" if w > h else "square")}


def parse_showinfo_times(log):
    """pts_time values from `select=...,showinfo` stderr; each selected frame is a cut."""
    return sorted({float(m) for m in re.findall(r"pts_time:\s*([0-9]+(?:\.[0-9]+)?)", log)})


def parse_cropdetect(log):
    crops = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", log)
    if not crops:
        return None
    w, h, x, y = (int(v) for v in max(set(crops), key=crops.count))  # most frequent suggestion
    return {"w": w, "h": h, "x": x, "y": y}


def parse_freezes(log):
    starts = [float(v) for v in re.findall(r"freeze_start:\s*([0-9.]+)", log)]
    durs = [float(v) for v in re.findall(r"freeze_duration:\s*([0-9.]+)", log)]
    return [{"start_s": s, "duration_s": d} for s, d in zip(starts, durs)]


def shot_stats(cuts, duration, min_gap):
    pts = [0.0]
    for c in cuts:
        if c - pts[-1] >= min_gap and (duration is None or c < duration - min_gap):
            pts.append(c)
    if duration:
        pts.append(duration)
    lengths = [round(b - a, 4) for a, b in zip(pts, pts[1:])]
    if not lengths:
        return {"count": 0, "cut_times_s": [], "shot_lengths_s": []}
    q = statistics.quantiles(lengths, n=10) if len(lengths) >= 2 else [lengths[0]] * 9
    buckets = {"<0.5": 0, "0.5-1": 0, "1-2": 0, "2-4": 0, ">=4": 0}
    for L in lengths:
        k = "<0.5" if L < 0.5 else "0.5-1" if L < 1 else "1-2" if L < 2 else "2-4" if L < 4 else ">=4"
        buckets[k] += 1
    mean = statistics.fmean(lengths)
    return {"count": len(lengths), "cut_times_s": pts[1:-1] if duration else pts[1:],
            "shot_lengths_s": lengths, "median_s": round(statistics.median(lengths), 3),
            "mean_s": round(mean, 3), "p10_s": round(q[0], 3), "p90_s": round(q[-1], 3),
            "min_s": min(lengths), "max_s": max(lengths),
            "cv": round(statistics.pstdev(lengths) / mean, 3) if mean else None,
            "cuts_per_minute": round((len(lengths) - 1) / (duration / 60), 2) if duration else None,
            "histogram": buckets}


def palette_from_rgb(raw, k=6):
    """Quantise rgb24 bytes to 3 bits/channel, return top-k swatches with share."""
    counts, sums = {}, {}
    for i in range(0, len(raw) - 2, 3):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        key = (r >> 5, g >> 5, b >> 5)
        counts[key] = counts.get(key, 0) + 1
        s = sums.setdefault(key, [0, 0, 0])
        s[0] += r; s[1] += g; s[2] += b
    total = sum(counts.values()) or 1
    top = sorted(counts, key=counts.get, reverse=True)[:k]
    return [{"hex": "#%02x%02x%02x" % tuple(round(c / counts[t]) for c in sums[t]),
             "share": round(counts[t] / total, 3)} for t in top]


def letterbox_info(crop, w, h):
    if not crop or not w or not h:
        return {"letterboxed": None, "crop": None, "active_aspect": None}
    boxed = crop["h"] < 0.95 * h or crop["w"] < 0.95 * w
    return {"letterboxed": boxed, "crop": "%d:%d:%d:%d" % (crop["w"], crop["h"], crop["x"], crop["y"]),
            "active_aspect": round(crop["w"] / crop["h"], 3) if crop["h"] else None,
            "container_aspect": round(w / h, 3)}


# ---------- ffmpeg wrappers ----------
def _run(cmd, binary=False):
    p = subprocess.run(cmd, capture_output=True)
    return p.returncode, p.stdout if binary else p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def analyze(path, out, stills_dir, threshold, max_stills, freeze_min):
    ff, fp = shutil.which("ffmpeg"), shutil.which("ffprobe")
    if not ff or not fp:
        return 2, {"status": "blocked", "skill": "examleaf-reference-analyzer",
                   "error": "ffmpeg/ffprobe not found on PATH",
                   "action": "Install FFmpeg on the render box via the approved environment (preflight: "
                             "12_advanced_animations_with_claude/04_harness_contract/preflight.sh). "
                             "This helper does not install anything."}
    if not os.path.isfile(path):
        return 2, {"status": "blocked", "error": f"input not found: {path}"}
    cmds = []
    probe_cmd = [fp, "-v", "error", "-select_streams", "v:0", "-show_entries",
                 "stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,codec_name,duration:format=duration",
                 "-of", "json", path]
    cmds.append(probe_cmd)
    rc, so, se = _run(probe_cmd)
    if rc:
        return 1, {"status": "failed", "stage": "ffprobe", "stderr": se[-2000:]}
    probe = parse_probe(so)
    crop_cmd = [ff, "-hide_banner", "-nostats", "-i", path, "-vf", "fps=2,cropdetect", "-an", "-f", "null", "-"]
    cmds.append(crop_cmd)
    _, _, se = _run(crop_cmd)
    lb = letterbox_info(parse_cropdetect(se), probe["width"], probe["height"])
    scene_cmd = [ff, "-hide_banner", "-nostats", "-i", path, "-vf",
                 f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"]
    cmds.append(scene_cmd)
    _, _, se = _run(scene_cmd)
    fps = probe["fps"] or 30.0
    shots = shot_stats(parse_showinfo_times(se), probe["duration_s"], 1.0 / fps)
    fz_cmd = [ff, "-hide_banner", "-nostats", "-i", path, "-vf", f"freezedetect=n=-60dB:d={freeze_min}",
              "-an", "-f", "null", "-"]
    cmds.append(fz_cmd)
    _, _, se = _run(fz_cmd)
    freezes = parse_freezes(se)
    # stills + palette at shot midpoints (active area only when letterboxed)
    bounds = [0.0] + shots.get("cut_times_s", []) + [probe["duration_s"] or 0.0]
    mids = [round((a + b) / 2, 3) for a, b in zip(bounds, bounds[1:])][:max_stills]
    crop_vf = f"crop={lb['crop']}," if lb.get("letterboxed") else ""
    palettes, stills = [], []
    for i, t in enumerate(mids):
        rc, raw, _ = _run([ff, "-hide_banner", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1",
                           "-vf", crop_vf + "scale=48:48", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], binary=True)
        if rc == 0 and raw:
            palettes.append({"t_s": t, "swatches": palette_from_rgb(raw)})
        if stills_dir:
            os.makedirs(stills_dir, exist_ok=True)
            sp = os.path.join(stills_dir, f"shot_{i:03d}_{t:.2f}s.png")
            if _run([ff, "-hide_banner", "-v", "error", "-y", "-ss", str(t), "-i", path,
                     "-frames:v", "1", sp])[0] == 0:
                stills.append(sp)
    _, ver, _ = _run([ff, "-version"])
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    result = build_result(path, h.hexdigest(), probe, lb, shots, freezes, palettes, stills, threshold,
                          [" ".join(c) for c in cmds], ver.splitlines()[0] if ver else None)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    return 0, {"status": "ok", "out": out, "shots": shots.get("count"), "warnings": result["warnings"]}


def build_result(path, sha, probe, lb, shots, freezes, palettes, stills, threshold, cmds, version):
    warns = []
    if probe["vfr_suspected"]:
        warns.append("variable frame rate suspected (r_frame_rate != avg_frame_rate); cut times use pts_time "
                     "seconds, frame counts are unreliable; author ExamLeaf scenes at a fixed fps")
    if lb.get("letterboxed"):
        warns.append("letterboxed source: analysis restricted to the active area %s (aspect %s); vertical "
                     "re-layout goes to examleaf-vertical-adapt (#49)" % (lb["crop"], lb["active_aspect"]))
    if probe["orientation"] == "landscape":
        warns.append("landscape reference: pacing numbers transfer, layout does not; re-lay out for 1080x1920 (#49)")
    if shots.get("count", 0) <= 1:
        warns.append("no cuts detected at this threshold; lower --scene-threshold or treat as one continuous shot")
    holds = [f["duration_s"] for f in freezes]
    agg = {}
    for p in palettes:
        for s in p["swatches"]:
            agg[s["hex"]] = agg.get(s["hex"], 0) + s["share"]
    overall = sorted(agg.items(), key=lambda kv: kv[1], reverse=True)[:8]
    tot = sum(v for _, v in overall) or 1
    return {"schema_version": SCHEMA, "skill": "examleaf-reference-analyzer",
            "source": {"path": path, "sha256": sha, "rights": "analysis_only"},
            "probe": probe, "letterbox": lb, "scene_threshold": threshold, "shots": shots,
            "holds": {"method": "freezedetect static intervals (upper-bound proxy for text holds; confirm on stills)",
                      "intervals": freezes, "count": len(holds),
                      "median_s": round(statistics.median(holds), 3) if holds else None},
            "palette": {"per_shot": palettes,
                        "overall": [{"hex": k, "share": round(v / tot, 3)} for k, v in overall]},
            "stills": stills, "stills_policy": "quarantine: internal study only; never assets, never image-model references",
            "commands": cmds, "ffmpeg_version": version, "warnings": warns}


# ---------- selftest ----------
def selftest():
    probe = json.dumps({"streams": [{"width": 1080, "height": 1920, "codec_name": "h264",
                                     "r_frame_rate": "30/1", "avg_frame_rate": "2997/100"}],
                        "format": {"duration": "12.0"}})
    p = parse_probe(probe)
    assert p["vfr_suspected"] is False and p["orientation"] == "portrait" and abs(p["fps"] - 29.97) < 1e-6
    p2 = parse_probe({"streams": [{"width": 1920, "height": 1080, "r_frame_rate": "60/1",
                                   "avg_frame_rate": "24000/1001"}], "format": {"duration": "5"}})
    assert p2["vfr_suspected"] is True and p2["orientation"] == "landscape"
    log = ("[Parsed_showinfo_1 @ 0x6000] n:   0 pts:  60060 pts_time:2.002   duration: 1001\n"
           "[Parsed_showinfo_1 @ 0x6000] n:   1 pts: 150150 pts_time:5.005   duration: 1001\n"
           "[Parsed_showinfo_1 @ 0x6000] n:   2 pts: 150180 pts_time:5.006   duration: 1001\n"
           "[Parsed_showinfo_1 @ 0x6000] n:   3 pts: 270270 pts_time:9.009   duration: 1001\n")
    cuts = parse_showinfo_times(log)
    assert cuts == [2.002, 5.005, 5.006, 9.009]
    s = shot_stats(cuts, 12.0, 1 / 30)
    assert s["count"] == 4 and s["shot_lengths_s"] == [2.002, 3.003, 4.004, 2.991], s
    assert s["median_s"] == 2.997 and s["cuts_per_minute"] == 15.0 and s["histogram"]["2-4"] == 3
    crop_log = "[Parsed_cropdetect_1 @ 0x1] x1:0 x2:1079 y1:656 y2:1263 w:1080 h:608 x:0 y:656 crop=1080:608:0:656\n" * 3
    lb = letterbox_info(parse_cropdetect(crop_log), 1080, 1920)
    assert lb["letterboxed"] is True and lb["active_aspect"] == 1.776
    fz = parse_freezes("[freezedetect @ 0x2] lavfi.freezedetect.freeze_start: 3.2\n"
                       "[freezedetect @ 0x2] lavfi.freezedetect.freeze_duration: 1.6\n"
                       "[freezedetect @ 0x2] lavfi.freezedetect.freeze_end: 4.8\n")
    assert fz == [{"start_s": 3.2, "duration_s": 1.6}]
    raw = bytes([243, 236, 223]) * 75 + bytes([217, 72, 59]) * 25        # cream 75 %, tomato 25 % ([V4-MP] hexes)
    pal = palette_from_rgb(raw)
    assert pal[0] == {"hex": "#f3ecdf", "share": 0.75} and pal[1] == {"hex": "#d9483b", "share": 0.25}
    res = build_result("ref.mp4", "0" * 64, p2, lb, s, fz, [{"t_s": 1.0, "swatches": pal}], [], 0.3, [], None)
    assert res["source"]["rights"] == "analysis_only" and len(res["warnings"]) == 3
    assert res["holds"]["median_s"] == 1.6 and res["palette"]["overall"][0]["hex"] == "#f3ecdf"
    print(json.dumps({"selftest": "pass", "script": "analyze_reference.py",
                      "ffmpeg_on_path": bool(shutil.which("ffmpeg"))}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Reference video -> pacing/style JSON (analysis only)")
    ap.add_argument("--input"); ap.add_argument("--out")
    ap.add_argument("--stills-dir"); ap.add_argument("--scene-threshold", type=float, default=0.30,
                                                     help="starting value; tune per reference")
    ap.add_argument("--max-stills", type=int, default=12)
    ap.add_argument("--freeze-min", type=float, default=0.5, help="min static interval (s) counted as a hold")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.input or not a.out:
        ap.error("--input and --out are required")
    rc, info = analyze(a.input, a.out, a.stills_dir, a.scene_threshold, a.max_stills, a.freeze_min)
    print(json.dumps(info, indent=2))
    return rc


if __name__ == "__main__":
    sys.exit(main())
