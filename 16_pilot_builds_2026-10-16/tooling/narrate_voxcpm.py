#!/usr/bin/env python3
"""narrate_voxcpm.py <script.json> [--redo b03,b07] [--reference <wav>]
Release voice (PD-29, 27 Oct 2026): the founder's own voice cloned locally by VoxCPM2-4bit through MLX Audio, offline
and free. Until the founder's voice/reference.wav exists, it clones the designed test voice voice/default_reference.wav
(PD-29a) and marks the voice block test_voice. Fills the narration cache that narrate.py reads (per-beat mp3 + align.json under the cache key narrate.py
computes), so `narrate.py <script.json>` then builds the timeline, mix, captions and cue sheets with no network call.
Word times are local Whisper small.en word timestamps matched to the script words (narrate.align_words), recorded as
alignment_source forced_alignment. The same pass compares what Whisper heard with the script and prints LISTEN for a
beat whose take dropped, added or changed words: listen, then `--redo <beat>` for a new take (the next seed).
Cached beats are skipped, so a re-run voices only changed text. Run it with the DikiStudio python
(pilotlib.STUDIO/.venv/bin/python; models/ and voice/reference.wav live there too). voice.voice_id hashes the reference
audio, the delivery instruction and the settings, so changing any of them re-voices every beat. Direction tags are
stripped before speaking: VoxCPM2 takes its delivery from `instruct`. The raw float take stays as <beat>.take.wav."""
import argparse, difflib, json, os, pathlib, subprocess, sys, time
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L
import narrate as N

MODEL = "models/VoxCPM2-4bit"
INSTRUCT = "Brisk, energetic English teaching. Clear pronunciation, natural emphasis, and short natural pauses."
STEPS, CFG, SEED = 10, 2.0, 20261016   # source plan §4: keep 10 steps and CFG 2.0 for the first pilot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--redo", default="", help="comma list of beat ids to re-voice with the next seed")
    ap.add_argument("--reference", help="reference WAV (default: the founder's voice/reference.wav; until it exists, the designed test voice voice/default_reference.wav)")
    a = ap.parse_args()
    own = L.STUDIO / "voice/reference.wav"
    ref = pathlib.Path(a.reference).expanduser() if a.reference else own if own.exists() else L.STUDIO / "voice/default_reference.wav"
    if not ref.exists():
        sys.exit(f"voice reference missing: {ref} (15-20 s of clean speech, mono WAV: 05_narration_system/local_voice_voxcpm2/SETUP.md §3)")
    test = not ref.name.startswith("reference")   # PD-29a: anything but the founder's own reference is a test voice
    if test:
        print(f"TEST voice {ref.name} (designed, not the founder's): record {own} before release")
    import mlx.core as mx, numpy as np, soundfile as sf, imageio_ffmpeg
    mx.set_cache_limit(0)   # free buffers at once: peak ~5 GB instead of ~10 GB on the 16 GB M1 Pro, same speed (27 Oct 2026: the default cache swapped a beat from 30 s to 5 min)
    from mlx_audio.tts.utils import load as load_tts
    from mlx_audio.stt.utils import load as load_stt
    p = pathlib.Path(a.script); s = json.loads(p.read_text(encoding="utf-8")); d = p.parent
    v = s.setdefault("voice", {}); v.pop("preview", None)
    v.update(provider="local", model_id="voxcpm2-4bit", voice_id="ref-" + L.sha256_bytes(ref.read_bytes() + f"|{INSTRUCT}|{STEPS}|{CFG}".encode())[:12],
             reference=f"{ref.name} sha256 {L.sha256_file(ref)[:16]}", instruct=INSTRUCT, inference_timesteps=STEPS, cfg_value=CFG, test_voice=test,
             note=("TEST voice designed with VoxCPM2 (PD-29a), not for release" if test else "local VoxCPM2 clone of the founder's voice (PD-29)")
             + "; re-measure rate_scale on the first narration (PD-22)")
    p.write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    bd = d / "narration" / "beats"; bd.mkdir(parents=True, exist_ok=True)
    redo = {x for x in a.redo.split(",") if x}; todo = []
    if redo - {b["id"] for b in s["beats"]}:
        sys.exit(f"--redo names unknown beats: {sorted(redo - {b['id'] for b in s['beats']})}")
    for b in s["beats"]:
        spoken = (b.get("tag", "") + " " + b["text"]).strip()
        ck = L.sha256_bytes(f"{v['model_id']}|{v['voice_id']}|{s['language']}|{spoken}|seed20261016".encode())[:16]
        mp = bd / f"{b['id']}.align.json"; old = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {}
        if old.get("cache_key") == ck and (bd / f"{b['id']}.mp3").exists() and b["id"] not in redo:
            print(f"  {b['id']}: cached (take {old.get('take', 1)})"); continue
        todo.append((b, spoken, ck, old.get("take", 0) + 1 if old.get("cache_key") == ck else 1))
    if not todo:
        print("all beats cached; now run narrate.py on the same script"); return
    ff = imageio_ffmpeg.get_ffmpeg_exe(); tts = load_tts(str(L.STUDIO / MODEL)); takes = []
    for b, spoken, ck, take in todo:   # pass 1: voice every beat (the TTS model alone in memory)
        (bd / f"{b['id']}.align.json").unlink(missing_ok=True)       # a crash before pass 2 leaves the beat uncached, never stale
        mx.random.seed(SEED + take - 1); t0 = time.perf_counter()
        r = next(tts.generate(text=L.TAG_RE.sub(" ", b["text"]).strip(), ref_audio=str(ref), instruct=INSTRUCT, inference_timesteps=STEPS, cfg_value=CFG))
        audio = np.asarray(r.audio.astype(mx.float32)); gen_s = time.perf_counter() - t0
        if audio.ndim != 1 or audio.size == 0 or not np.isfinite(audio).all():
            sys.exit(f"{b['id']}: invalid generated audio")
        wav = bd / f"{b['id']}.take.wav"; sf.write(str(wav), audio, int(r.sample_rate), subtype="FLOAT")
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(wav), "-ar", "48000", "-ac", "1", "-codec:a", "libmp3lame", "-b:a", "320k", str(bd / f"{b['id']}.mp3")], check=True)
        takes.append((b, spoken, ck, take, wav, gen_s))
        print(f"  {b['id']}: take {take} | {audio.size / r.sample_rate:.2f} s of audio in {gen_s:.1f} s", flush=True)
    del tts; mx.clear_cache()
    stt = load_stt(str(L.STUDIO / L.STT_MODEL)); listen = []
    for b, spoken, ck, take, wav, gen_s in takes:   # pass 2: word times and the heard-vs-script check
        heard = L.stt_words(wav, stt); chars, t0s, t1s = [], [], []
        for w, x0, x1 in heard:                     # whisper words as the character alignment align_words expects
            chars += list(w) + [" "]; t0s += [x0] * len(w) + [x1]; t1s += [x1] * (len(w) + 1)
        words, unmatched = N.align_words(chars, t0s, t1s, L.words_of(b["text"]))
        exp = L.canon([L.norm_word(w) for w in L.words_of(b["text"])]); got = L.canon(L.heard_tokens([w for w, _, _ in heard]))
        sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
        diffs = [(" ".join(exp[i1:i2]), " ".join(got[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
        span = words[-1]["t1"] - words[0]["t0"] if words else 0
        meta = {"cache_key": ck, "beat": b["id"], "chars": len(spoken), "request_id": f"voxcpm2-4bit-{v['voice_id']}-seed{SEED + take - 1}",
                "model_id": v["model_id"], "voice_id": v["voice_id"], "take": take, "seed": SEED + take - 1, "generation_s": round(gen_s, 1),
                "unmatched_words": unmatched, "words": words, "provider_alignment": None, "alignment_source": "forced_alignment",
                "stt": {"model": L.STT_MODEL, "heard": " ".join(w for w, _, _ in heard), "match_ratio": round(sm.ratio(), 3), "diffs": diffs}}
        (bd / f"{b['id']}.align.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {b['id']}: {len(words)} words | {len(words) / span * 60 if span > 0 else 0:.0f} wpm | heard {sm.ratio():.2f}" + (f" | LISTEN {diffs}" if diffs else ""))
        if diffs: listen.append(b["id"])
    print(("LISTEN to " + ",".join(listen) + "; if a word is really wrong, re-run with --redo " + ",".join(listen) + ". " if listen else "")
          + "Then run narrate.py on the same script.")


if __name__ == "__main__":
    main()
