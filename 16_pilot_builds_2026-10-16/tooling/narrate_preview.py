#!/usr/bin/env python3
"""narrate_preview.py <script.json> [--voice Rishi] [--rate 185]
Local PREVIEW voice through macOS `say` (offline, free): fills the narration cache that narrate.py reads (per-beat
mp3 + align.json with the cache key narrate.py computes), so `narrate.py <script.json>` then builds the timeline, the
mix and the cue sheets without any ElevenLabs call. Word timings are proportional to word length inside each clip's
voiced span (no forced aligner): good enough for a timing preview, never for release (17 Oct 2026, PD-28 preview path).
Sets script.json voice.model_id = "macos-say" and voice.voice_id = <voice> so the cache keys match; direction tags
are stripped before speaking (say would read them aloud)."""
import argparse, json, pathlib, re, subprocess, sys, wave, array, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L
import imageio_ffmpeg


def voiced_span(wav_path, dbfs=-45.0, win_s=0.01):
    with wave.open(str(wav_path), "rb") as w:
        sr, ch, sw, n = w.getframerate(), w.getnchannels(), w.getsampwidth(), w.getnframes()
        a = array.array({1: "b", 2: "h", 4: "i"}[sw], w.readframes(n))
    if ch > 1: a = a[::ch]
    full = float(2 ** (8 * sw - 1)); per = max(1, int(win_s * sr)); first = last = None
    for i in range(0, len(a) - per + 1, per):
        seg = a[i:i + per]; r = math.sqrt(sum(x * x for x in seg) / len(seg)) / full
        if 20 * math.log10(max(r, 1e-9)) > dbfs:
            if first is None: first = i / sr
            last = (i + per) / sr
    return first or 0.0, last or (len(a) / sr)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--voice", default="Rishi"); ap.add_argument("--rate", type=int, default=185)
    a = ap.parse_args()
    p = pathlib.Path(a.script); s = json.loads(p.read_text(encoding="utf-8")); d = p.parent
    s.setdefault("voice", {}); s["voice"]["model_id"] = "macos-say"; s["voice"]["voice_id"] = a.voice; s["voice"]["preview"] = f"macOS say -r {a.rate} (not for release)"
    p.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ff = imageio_ffmpeg.get_ffmpeg_exe(); bd = d / "narration" / "beats"; bd.mkdir(parents=True, exist_ok=True)
    for b in s["beats"]:
        spoken = (b.get("tag", "") + " " + b["text"]).strip()
        ck = L.sha256_bytes(f"{s['voice']['model_id']}|{s['voice']['voice_id']}|{s['language']}|{spoken}|seed20261016".encode())[:16]
        text = re.sub(r"\[[^\]]*\]", "", b["text"]).strip()
        aiff = bd / f"{b['id']}.aiff"; mp3 = bd / f"{b['id']}.mp3"; wav = bd / f"{b['id']}.raw.wav"
        subprocess.run(["say", "-v", a.voice, "-r", str(a.rate), "-o", str(aiff), text], check=True)
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(aiff), "-ar", "48000", "-ac", "1", str(wav)], check=True)
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(wav), "-codec:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
        on, off = voiced_span(wav); words = L.words_of(b["text"]); total = sum(len(w) + 1 for w in words)
        t = on; out = []
        for w in words:
            dur = (off - on) * (len(w) + 1) / total; out.append({"w": w, "t0": round(t, 3), "t1": round(t + dur * 0.92, 3)}); t += dur
        meta = {"cache_key": ck, "beat": b["id"], "chars": len(spoken), "request_id": f"macos-say-{a.voice}-{a.rate}", "model_id": "macos-say", "voice_id": a.voice,
                "unmatched_words": 0, "words": out, "provider_alignment": None, "preview": True}
        (bd / f"{b['id']}.align.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        aiff.unlink(); wav.unlink()
        print(f"  {b['id']}: {len(words)} words | voiced {on:.2f}-{off:.2f} s | {len(words) / max(off - on, 0.01) * 60:.0f} wpm")
    print("preview cache written; now run narrate.py on the same script (all beats cached, no API synthesis)")


if __name__ == "__main__":
    main()
