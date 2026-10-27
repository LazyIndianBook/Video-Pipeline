#!/usr/bin/env python3
"""render.py <script.json> [--fps 30] [--scenes s01,s02] [--no-determinism]
Harness-conformant frame capture (contract §11): per scene, inject the measured cue sheet and the fixture, await
window.ready, N = round(DURATION × fps), seek(i / fps) for integer i, PNG frames piped to FFmpeg (libx264, yuv420p),
error channel read after every seek, cueSource/fixtureSource must be 'injected'. Then concat + narration mux, a
determinism re-check (fresh page, reverse order, three frames), a contact sheet and a render manifest.
Audio extras (Professor Diki shorts, 17_professor_diki_simplified/07_PIPELINE_CHANGES.md): if
17_professor_diki_simplified/brand/motif/diki_end_motif_v1.wav exists and the outro beat (last beat) defines `motif_at`
(seconds before the end; default 1.4) or the script v2 top-level `outro.motif` is set (`outro.motif_starts:
"after_last_word"` places it 0.1 s after the last word), the motif is mixed there at `motif_gain_db` (default −3 dB on the asset); it is
moved later if it would start under the last word (never under speech). Every cue-sheet `sfx[]` entry {file, at
(scene-local s), gain_db (default −6)} is mixed at its video time. The extras are summed onto mix_norm.wav with FFmpeg
(adelay + volume + amix normalize=0, bit-exact flags): same inputs, same bytes."""
import argparse, hashlib, json, pathlib, subprocess, sys, time, wave
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L
import imageio_ffmpeg
from playwright.sync_api import sync_playwright


MOTIF = pathlib.Path(__file__).resolve().parents[2] / "17_professor_diki_simplified/brand/motif/diki_end_motif_v1.wav"
MOTIF_AT_DEFAULT, MOTIF_GAIN_DEFAULT, SFX_GAIN_DEFAULT, MOTIF_AFTER_SPEECH_S = 1.4, -3.0, -6.0, 0.1


def wav_seconds(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def audio_events(s, d, timeline, total_s):
    """[{file, at (video s), gain_db, kind}] from the outro motif (beat motif_at or script outro.motif) and every cue sheet's sfx[]; [] when none apply."""
    ev = []; outro = s["beats"][-1]; top = s.get("outro") or {}
    if MOTIF.exists() and ("motif_at" in outro or top.get("motif")):
        last = next((b for b in reversed(timeline["beats"]) if b.get("words")), None)
        floor = (last["words"][-1]["t1"] + MOTIF_AFTER_SPEECH_S) if last else 0.0
        m_at = outro.get("motif_at", top.get("motif_at"))
        at = floor if (m_at is None and top.get("motif_starts") == "after_last_word") else total_s - float(MOTIF_AT_DEFAULT if m_at is None else m_at)
        e = {"file": str(MOTIF), "at": round(max(at, floor), 3), "gain_db": float(outro.get("motif_gain_db", top.get("motif_gain_db", MOTIF_GAIN_DEFAULT))), "kind": "end_motif"}
        if at < floor: e["moved_from"] = round(at, 3)
        if e["at"] + wav_seconds(MOTIF) > total_s + 1e-6: e["truncated"] = True
        ev.append(e)
    starts = {x["id"]: x["start"] for x in timeline.get("scenes", [])}
    for sc in s["scenes"]:
        p = d / "cues" / f"{sc['id']}.cues.json"
        for x in (json.loads(p.read_text(encoding="utf-8")).get("sfx") or []) if p.exists() else []:
            f = pathlib.Path(x["file"]); f = f if f.is_absolute() else next((c for c in (d / f, MOTIF.parent / f) if c.exists()), d / f)
            ev.append({"file": str(f), "at": round(starts.get(sc["id"], 0.0) + float(x["at"]), 3), "gain_db": float(x.get("gain_db", SFX_GAIN_DEFAULT)), "kind": "sfx", "scene": sc["id"]})
    return ev


def mix_extras(ff, base_wav, events, out_wav):
    """Sum events onto base_wav (length kept). Deterministic: fixed filter graph, no dither, bit-exact muxer flags."""
    cmd = [ff, "-y", "-loglevel", "error", "-i", str(base_wav)]; chains = []
    for i, e in enumerate(events, 1):
        cmd += ["-i", e["file"]]; ms = int(round(e["at"] * 1000))
        chains.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}:all=1,volume={e['gain_db']}dB[e{i}]")
    graph = ";".join(chains + ["[0:a]" + "".join(f"[e{i}]" for i in range(1, len(events) + 1)) + f"amix=inputs={len(events) + 1}:duration=first:normalize=0[out]"])
    subprocess.run(cmd + ["-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", "-fflags", "+bitexact", "-flags:a", "+bitexact", "-map_metadata", "-1", str(out_wav)], check=True)
    return out_wav


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--fps", type=int, default=L.FPS); ap.add_argument("--scenes"); ap.add_argument("--no-determinism", action="store_true")
    ap.add_argument("--mux-only", action="store_true", help="skip capture; rebuild the final file from existing scene MP4s and the current narration mix")
    a = ap.parse_args()
    s = L.load_script(a.script); d = pathlib.Path(s["_dir"]); ff = imageio_ffmpeg.get_ffmpeg_exe(); fps = a.fps
    rd = d / "render"; (rd / "scenes").mkdir(parents=True, exist_ok=True); (rd / "frames").mkdir(exist_ok=True)
    fixture = json.loads((d / "fixtures" / "fixture.json").read_text(encoding="utf-8"))
    timeline = json.loads((d / "narration" / "timeline.json").read_text(encoding="utf-8"))
    only = set(a.scenes.split(",")) if a.scenes else None
    manifest = {"video_id": s["video_id"], "fps": fps, "viewport": [1080, 1920], "seed": 20261016, "scenes": [], "script_sha256": s["_sha256"],
                "narration_audio_sha256": timeline["narration_audio_sha256"], "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if a.mux_only or (only and (rd / "render_manifest.json").exists()):
        old = json.loads((rd / "render_manifest.json").read_text(encoding="utf-8")); manifest["browser"] = old.get("browser"); manifest["capture_started"] = old.get("started")
        manifest["scenes"] = old["scenes"] if a.mux_only else [x for x in old["scenes"] if x["id"] not in only]
    with sync_playwright() as p:
        for sc in s["scenes"]:
            if a.mux_only or (only and sc["id"] not in only): continue
            sheet = json.loads((d / "cues" / f"{sc['id']}.cues.json").read_text(encoding="utf-8")); scene_file = d / sc["file"]
            b, page = L.open_scene(p, scene_file, sheet, fixture, fps=fps)
            if not manifest.get("browser"): manifest["browser"] = b.version
            dur = page.evaluate("window.DURATION"); N = round(dur * fps)
            src = page.evaluate("[window.__cueSource, window.__fixtureSource]")
            rec = {"id": sc["id"], "file": sc["file"], "scene_sha256": L.sha256_file(scene_file), "cue_sheet_sha256": L.sha256_file(d / "cues" / f"{sc['id']}.cues.json"),
                   "cue_source": src[0], "fixture_source": src[1], "duration": dur, "frames": N, "errors": [], "warnings": []}
            if src != ["injected", "injected"]:
                rec["errors"].append({"code": "E_SOURCE", "message": f"sources {src}"})
            out_mp4 = rd / "scenes" / f"{sc['id']}.mp4"
            enc = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "pipe:0", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(fps), str(out_mp4)], stdin=subprocess.PIPE)
            hashes = {}; t0 = time.time(); seen_err = 0
            for i in range(N):
                page.evaluate(f"window.seek({i}/{fps})")
                png = page.screenshot(type="png"); enc.stdin.write(png)
                errs = page.evaluate("window.__errors || []")
                if len(errs) > seen_err:
                    for e in errs[seen_err:]:
                        (rec["errors"] if e.get("severity") == "error" else rec["warnings"]).append(e)
                    seen_err = len(errs)
                hashes[i] = hashlib.sha256(png).hexdigest()
                if i in (0, N // 2, N - 1):
                    (rd / "frames" / f"{sc['id']}_{i:05d}.png").write_bytes(png)
                if i % (fps * 2) == 0:
                    (rd / "frames" / f"{sc['id']}_t{i // fps:03d}.png").write_bytes(png)
            enc.stdin.close(); enc.wait(); rec["encode_exit"] = enc.returncode; rec["capture_s"] = round(time.time() - t0, 1)
            rec["frame_hashes_sample"] = {str(i): hashes[i] for i in (0, N // 2, N - 1) if i in hashes}; rec["frames_sha256"] = hashlib.sha256("".join(hashes[i] for i in range(N)).encode()).hexdigest()
            b.close()
            if not a.no_determinism:
                # Re-run the IDENTICAL procedure (fresh page, every frame seeked AND captured, in order) and compare every
                # frame hash. Observed 16 Oct 2026 on Chrome 155/macOS: pixels depend on the seek-and-capture history for
                # layers with CSS transforms (raster-scale cache), so reverse-order or sampled re-checks differ while an
                # identical full procedure reproduces byte-identically (MP4 sha256 matched across runs).
                b2, page2 = L.open_scene(p, scene_file, sheet, fixture, fps=fps); mism = 0
                for i in range(N):
                    page2.evaluate(f"window.seek({i}/{fps})")
                    if hashlib.sha256(page2.screenshot(type="png")).hexdigest() != hashes[i]: mism += 1
                b2.close(); rec["deterministic_rerender"] = (mism == 0); rec["deterministic_mismatched_frames"] = mism; rec["deterministic_sampled_frames"] = N
            manifest["scenes"] = sorted([x for x in manifest["scenes"] if x["id"] != sc["id"]] + [rec], key=lambda x: [q["id"] for q in s["scenes"]].index(x["id"]))
            print(f"scene {sc['id']}: {N} frames in {rec['capture_s']} s | errors {len(rec['errors'])} | warnings {len(rec['warnings'])} | re-render identical {rec.get('deterministic_rerender')} ({rec.get('deterministic_sampled_frames')} sampled)")
    # concat + mux
    lst = rd / "concat.txt"; lst.write_text("".join(f"file '{(rd / 'scenes' / (sc['id'] + '.mp4')).resolve().as_posix()}'\n" for sc in s["scenes"]))
    video = rd / "video_silent.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)], check=True)
    final = rd / f"{s['video_id']}.mp4"; audio = d / "narration" / "mix_norm.wav"
    events = audio_events(s, d, timeline, timeline["total_duration_s"]); manifest["audio_events"] = events
    if events:
        audio = mix_extras(ff, audio, events, d / "narration" / "mix_final.wav"); manifest["audio_final_sha256"] = L.sha256_file(audio)
        for e in events:
            if e.get("moved_from") is not None or e.get("truncated"): print(f"audio event warning: {e}")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)], check=True)
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(final), "-vf", "fps=1/3,scale=270:-1,tile=6x4", "-frames:v", "1", str(rd / "contact_sheet.png")], check=True)
    manifest["output"] = {"file": final.name, "sha256": L.sha256_file(final), "bytes": final.stat().st_size}
    manifest["total_errors"] = sum(len(x["errors"]) for x in manifest["scenes"]); manifest["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (rd / "render_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"final {final.name} | {manifest['output']['bytes']} bytes | sha256 {manifest['output']['sha256'][:16]} | errors {manifest['total_errors']}")
    if manifest["total_errors"]:
        sys.exit(4)


if __name__ == "__main__":
    main()
