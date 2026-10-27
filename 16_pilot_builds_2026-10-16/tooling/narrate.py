#!/usr/bin/env python3
"""narrate.py <script.json> [--dry-run] [--force]
Per-beat Path B narration through ElevenLabs eleven_v4 (text-to-dialogue with timestamps), cached by content hash so a
re-run never re-bills an unchanged beat. 27 Oct 2026 (PD-29): ElevenLabs is retired for voice-over; the release voice is
local VoxCPM2 (narrate_voxcpm.py fills this cache first), and this script then only builds from the cache, with no key
and no network. Writes <tier>/narration/{beats/*.mp3,*.wav,*.align.json, timeline.json, mix.wav,
mix_norm.wav, captions.vtt} and <tier>/cues/<scene>.cues.json (validated with the harness validator, --production).
Key comes from ELEVENLABS_API_KEY (never written anywhere).

--dry-run never synthesises: it prints the planned timeline (beats, labelled pauses, planned duration and silence share)
and the characters to synthesise; the quota is read only when the key is set.
Gaps are room tone, not digital silence (16 Oct 2026, A3-04): a seeded pink-noise bed at ROOM_TONE_DBFS runs under the
whole mix and each beat clip gets 10 ms edge fades; the master is two-pass linear loudnorm (A3-14) so the bed is not
pumped up in the gaps. v2 scripts (pilotlib.is_v2) are placed by word edges: each clip is trimmed to its first/last
aligned word (+ CLIP_HEAD_S / CLIP_TAIL_S), the next beat's first word starts exactly the pause seconds (PD-01 purpose
default or after_s) after the last word, the last beat has no pause, and the tail is pilotlib.tail_s (0.8 s motif).
v1 scripts keep their placement (clip end + pause_after_s + think_window_s, 1.6 s tail). Lead-in 0.6 s in both; the
first scene starts at video time 0. timeline.json keeps pause_after_s/think_window_s per beat (qa.py reads them) and
adds pause {purpose, seconds}, energy and a video-time pauses[] list."""
import argparse, base64, difflib, json, os, pathlib, random, subprocess, sys, urllib.request, wave
from array import array
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L

API = "https://api.elevenlabs.io"
LEAD_IN_S = L.LEAD_IN_S  # silence before the first word of the video
TAIL_S = L.TAIL_S_V1     # v1 hold after the last word
SR = 48000
ROOM_TONE_DBFS = -66.0   # RMS of the pink-noise bed (pre-master); the master lifts it ~10 dB, and its peaks must stay under the −40 dB silence detector (16 Oct 2026: −60 tripped it)
ROOM_TONE_SEED = 20261016
FADE_S = 0.010
CLIP_HEAD_S, CLIP_TAIL_S = 0.03, 0.08   # v2 clip pads around the aligned words (A3-15: ends can run ~0.08 s late)
ROOT = pathlib.Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py"


def key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ELEVENLABS_API_KEY missing in the environment")
    return k


def api(path, body=None, q=None):
    url = API + path + (("?" + q) if q else "")
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None,
                                 headers={"xi-api-key": key(), "Content-Type": "application/json"}, method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r), {k.lower(): v for k, v in r.headers.items()}


def remaining_quota():
    s, _ = api("/v1/user/subscription")
    return int(s.get("character_limit", 0)) - int(s.get("character_count", 0)), s.get("tier")


def mp3_to_wav(ff, mp3, wav):
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(mp3), "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(wav)], check=True)
    with wave.open(str(wav)) as w:
        return w.getnframes() / w.getframerate()


def align_words(chars, t0s, t1s, expected):
    """Provider character alignment → words matched to the script's spoken words (surface form from the script)."""
    toks = []; cur = None
    for ch, a, b in zip(chars, t0s, t1s):
        if ch.isspace():
            if cur: toks.append(cur); cur = None
        else:
            if cur is None: cur = {"text": "", "t0": a, "t1": b}
            cur["text"] += ch; cur["t1"] = b
    if cur: toks.append(cur)
    toks = [t for t in toks if L.norm_word(t["text"]) and not L.TAG_RE.fullmatch(t["text"])]
    got = [L.norm_word(t["text"]) for t in toks]; exp = [L.norm_word(w) for w in expected]
    out = [None] * len(expected)
    sm = difflib.SequenceMatcher(a=exp, b=got, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                out[i1 + k] = (toks[j1 + k]["t0"], toks[j1 + k]["t1"])
        elif tag == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                out[i1 + k] = (toks[j1 + k]["t0"], toks[j1 + k]["t1"])
    unmatched = [i for i, v in enumerate(out) if v is None]
    # interpolate any unmatched word between its timed neighbours (or the beat edges)
    total_end = toks[-1]["t1"] if toks else 0.0
    for i in unmatched:
        prev_t = next((out[j][1] for j in range(i - 1, -1, -1) if out[j]), 0.0)
        nxt_t = next((out[j][0] for j in range(i + 1, len(out)) if out[j]), total_end)
        span = max(nxt_t - prev_t, 0.12); n_gap = 1 + sum(1 for j in range(i + 1, len(out)) if out[j] is None and j < next((k for k in range(i + 1, len(out)) if out[k]), len(out)))
        out[i] = (round(prev_t + 0.02, 3), round(prev_t + span / n_gap - 0.02, 3))
    words = [{"w": w, "t0": round(float(a), 3), "t1": round(float(b), 3)} for w, (a, b) in zip(expected, out)]
    return words, len(unmatched)


def room_tone(n, seed=ROOM_TONE_SEED, dbfs=ROOM_TONE_DBFS):
    """n samples (int16 array) of seeded pink noise at `dbfs` RMS: a 4 s Kellet-filtered buffer, tiled."""
    rng = random.Random(seed); m = 4 * SR; b0 = b1 = b2 = 0.0; buf = []
    for _ in range(m):
        w = rng.uniform(-1, 1)
        b0 = 0.99765 * b0 + w * 0.0990460; b1 = 0.96300 * b1 + w * 0.2965164; b2 = 0.57000 * b2 + w * 1.0526913
        buf.append(b0 + b1 + b2 + w * 0.1848)
    rms = (sum(x * x for x in buf) / m) ** 0.5; g = 32767 * 10 ** (dbfs / 20) / rms
    loop = array("h", (int(round(x * g)) for x in buf))
    return array("h", (loop[i % m] for i in range(n)))


VOICE_EDGE_DBFS = -45.0   # a 10 ms window above this is voice; used to trim alignment edges (16 Oct 2026: v4 alignment
                          # reported the first word at 0.00 s and the last word at the clip end, stretching every gap by 0.1-0.3 s)


def voice_edges(wav_path, dbfs=VOICE_EDGE_DBFS, win_s=0.01):
    """(onset_s, offset_s) of the voiced part of a wav by RMS per window, or (None, None) when nothing is voiced."""
    import wave, array, math
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
    return first, last


def mix(clips, total_s, out_path):
    """clips: [(video_start_s, wav_path, clip_a_s, clip_b_s)] summed onto the room-tone bed with 10 ms edge fades."""
    n = int(round(total_s * SR)); out = room_tone(n); f = int(FADE_S * SR)
    for start_s, wav_path, a, b in clips:
        with wave.open(str(wav_path)) as w:
            w.setpos(int(a * SR)); data = array("h", w.readframes(max(0, int(b * SR) - int(a * SR))))
        pos = int(round(start_s * SR)); k = len(data)
        for i in range(min(k, n - pos)):
            g = min(1.0, (i + 1) / f, (k - i) / f)
            out[pos + i] = max(-32768, min(32767, out[pos + i] + int(data[i] * g)))
    with wave.open(str(out_path), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes(out.tobytes())


def master(ff, src, dst, I=-16.0, TP=-1.5, LRA=11.0):
    """Two-pass linear loudnorm (A3-14); ffmpeg falls back to dynamic itself if linear cannot reach the target."""
    r = subprocess.run([ff, "-hide_banner", "-i", str(src), "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    try:
        m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    except ValueError:   # measurement unreadable: the v1 single-pass master
        print("  master: loudnorm measurement unreadable; single-pass dynamic")
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(src), "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}", "-ar", str(SR), str(dst)], check=True)
        return
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(src), "-af", af, "-ar", str(SR), str(dst)], check=True)


def print_plan(s):
    rows, total = L.plan(s)
    print(f"plan ({'v2 word-edge' if L.is_v2(s) else 'v1 clip'} placement): {total:.2f} s planned | silence {L.silence_share(s):.1%} | tail {L.tail_s(s)} s")
    for r in rows:
        print(f"  {r['start']:6.2f}-{r['end']:6.2f} {r['id']:<4} {r['slot']:<24} + {r['pause_s']:.2f} {r['purpose']}")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--tempo", type=float, default=1.0, help="speech tempo on every clip (FFmpeg atempo, pitch kept), 0.9-1.25; pauses stay exact; word times scale")
    a = ap.parse_args()
    s = L.load_script(a.script); d = pathlib.Path(s["_dir"]); v2 = L.is_v2(s)
    nd = d / "narration"; bd = nd / "beats"
    if not a.dry_run:
        bd.mkdir(parents=True, exist_ok=True); (d / "cues").mkdir(exist_ok=True)
    cd = d / "cues"
    v = s["voice"]; beats = s["beats"]
    todo = []
    for b in beats:
        spoken = (b.get("tag", "") + " " + b["text"]).strip()
        ck = L.sha256_bytes(f"{v['model_id']}|{v['voice_id']}|{s['language']}|{spoken}|seed20261016".encode())[:16]
        meta = bd / f"{b['id']}.align.json"
        cached = meta.exists() and json.loads(meta.read_text()).get("cache_key") == ck and (bd / f"{b['id']}.mp3").exists()
        todo.append((b, spoken, ck, cached))
    need = sum(len(sp) for _, sp, _, c in todo if not c)
    if a.dry_run:
        q = "quota not read (no ELEVENLABS_API_KEY)" if not os.environ.get("ELEVENLABS_API_KEY") else "quota remaining %s (%s)" % remaining_quota()
        print(f"DRY RUN, nothing synthesised | beats {len(beats)} | to synthesise {sum(1 for t in todo if not t[3])} | characters needed {need} | {q}")
        print_plan(s)
        return
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"beats {len(beats)} | to synthesise {sum(1 for t in todo if not t[3])} | characters needed {need}")
    if need and not v["model_id"].startswith("eleven"):   # PD-29: local voices fill the cache themselves; no ElevenLabs call
        sys.exit(f"{v['model_id']} beats not in the cache: run narrate_voxcpm.py (or narrate_preview.py for a preview) on this script first")
    if need:
        rem, tier = remaining_quota(); print(f"quota remaining {rem} ({tier})")
        if need > rem and not a.force:
            sys.exit("not enough quota; use --force to try anyway")
    prev_ids = []
    for b, spoken, ck, cached in todo:
        if cached:
            print(f"  {b['id']}: cached"); continue
        body = {"model_id": v["model_id"], "inputs": [{"text": spoken, "voice_id": v["voice_id"]}], "language_code": s["language"], "seed": 20261016}
        if prev_ids:
            body["previous_request_ids"] = prev_ids[-3:]
        j, h = api("/v1/text-to-dialogue/with-timestamps", body, "output_format=mp3_44100_128")
        (bd / f"{b['id']}.mp3").write_bytes(base64.b64decode(j["audio_base64"]))
        al = j.get("alignment") or j.get("normalized_alignment")
        words, unmatched = align_words(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"], L.words_of(b["text"]))
        rid = h.get("request-id")
        if rid: prev_ids.append(rid)
        meta = {"cache_key": ck, "beat": b["id"], "chars": len(spoken), "request_id": rid, "model_id": v["model_id"], "voice_id": v["voice_id"],
                "unmatched_words": unmatched, "words": words, "provider_alignment": al, "voice_segments": j.get("voice_segments")}
        (bd / f"{b['id']}.align.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {b['id']}: {len(spoken)} chars | request {rid} | unmatched words {unmatched}")
    # timeline in video time
    t = LEAD_IN_S; timeline = {"video_id": s["video_id"], "voice": v, "fps": L.FPS, "lead_in_s": LEAD_IN_S, "script_v2": v2,
                               "room_tone_dbfs": ROOM_TONE_DBFS, "tempo": a.tempo, "beats": [], "scenes": [], "pauses": []}
    timing = {}; clips = []; srcs = set()
    for i, b in enumerate(beats):
        meta = json.loads((bd / f"{b['id']}.align.json").read_text(encoding="utf-8"))
        srcs.add(meta.get("alignment_source", "tts_provider"))
        dur = mp3_to_wav(ff, bd / f"{b['id']}.mp3", bd / f"{b['id']}.wav"); wavp = bd / f"{b['id']}.wav"
        if abs(a.tempo - 1.0) > 1e-6:                                   # re-timing knob: speech only, never the pauses
            if not 0.9 <= a.tempo <= 1.35: sys.exit("--tempo must be within 0.9..1.35 (PD-22 0.95-1.05; PD-28 fast profile up to 1.3)")
            wavp = bd / f"{b['id']}.tempo.wav"
            subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(bd / f"{b['id']}.wav"), "-af", f"atempo={a.tempo:.4f}", str(wavp)], check=True)
            dur = dur / a.tempo
            meta = dict(meta, words=[dict(w, t0=w["t0"] / a.tempo, t1=w["t1"] / a.tempo) for w in meta["words"]])
        on, offv = voice_edges(wavp)                                   # trim alignment edges to the audible voice
        ws_ = meta["words"]
        if ws_ and on is not None:
            if ws_[0]["t0"] < on - 0.05: ws_[0]["t0"] = round(min(on, ws_[0]["t1"] - 0.02), 3)
            if ws_[-1]["t1"] > offv + 0.05: ws_[-1]["t1"] = round(max(offv, ws_[-1]["t0"] + 0.02), 3)
        purpose, sec = L.beat_pause(b)
        if v2:   # t is where this beat's first word starts; the clip is trimmed to its words
            if i == len(beats) - 1:
                sec = 0.0
            w0, w1 = meta["words"][0]["t0"], min(meta["words"][-1]["t1"], dur)
            off = t - w0; ca, cb = max(0.0, w0 - CLIP_HEAD_S), min(dur, w1 + CLIP_TAIL_S)
        else:    # t is where this beat's clip starts
            off = t; ca, cb = 0.0, dur
        words = [{"w": w["w"], "t0": round(off + w["t0"], 3), "t1": round(off + w["t1"], 3)} for w in meta["words"]]
        start = round(off + ca, 3); end = round(off + cb, 3); clips.append((off + ca, wavp, ca, cb))
        think = sec if purpose.startswith("think_") else 0.0
        rec = {"id": b["id"], "scene": b["scene"], "slot": b["slot"], "start": start, "end": end, "audio_s": round(dur, 3),
               "pause_after_s": (sec - think) if v2 else float(b.get("pause_after_s", 0)),
               "think_window_s": think if v2 else float(b.get("think_window_s", 0)),
               "pause": {"purpose": purpose, "seconds": sec}, "chars": meta["chars"],
               "request_id": meta["request_id"], "sha256": L.sha256_file(bd / f"{b['id']}.mp3"), "words": words}
        if "energy" in b:
            rec["energy"] = b["energy"]
        timeline["beats"].append(rec)
        timing[b["id"]] = {"start": start, "end": end, "words": words}
        gap_from = (off + w1) if v2 else end
        if sec > 0:
            timeline["pauses"].append({"beat": b["id"], "purpose": purpose, "seconds": sec, "start": round(gap_from, 3), "end": round(gap_from + sec, 3)})
        t = gap_from + sec
    import math
    total = math.ceil((t + L.tail_s(s)) * L.FPS) / L.FPS          # whole frames [N72]
    # scenes tile the video on the frame grid: a scene starts on the frame containing its first word
    by = L.beats_by_scene(s); starts = []
    for k, sc in enumerate(s["scenes"]):
        first = by[sc["id"]][0]["id"]
        # the first scene starts at video time 0 and carries the lead-in silence (judge finding 16 Oct 2026: starting it at
        # the first word made every video run LEAD_IN_S ahead of the narration)
        starts.append((sc["id"], 0.0 if k == 0 else math.floor(timing[first]["start"] * L.FPS + 1e-6) / L.FPS))
    for i, (sid, st) in enumerate(starts):
        en = starts[i + 1][1] if i + 1 < len(starts) else total
        timeline["scenes"].append({"id": sid, "start": round(st, 4), "end": round(en, 4), "duration": round(en - st, 4)})
    # scene-local word times are measured from the snapped scene start
    for sc in timeline["scenes"]:
        for b in by[sc["id"]]:
            timing[b["id"]]["scene_start"] = sc["start"]
    timeline["total_duration_s"] = total; timeline["chars_total"] = sum(x["chars"] for x in timeline["beats"])
    # mix: beats at offsets on a room-tone bed, 48 kHz mono; two-pass linear master
    mix(clips, total, nd / "mix.wav")
    master(ff, nd / "mix.wav", nd / "mix_norm.wav")
    audio_sha = L.sha256_file(nd / "mix_norm.wav"); timeline["narration_audio_sha256"] = audio_sha; timeline["script_sha256"] = s["_sha256"]
    (nd / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=1), encoding="utf-8")
    # captions
    def ts(x):
        h, r = divmod(x, 3600); m, sec = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}"
    vtt = ["WEBVTT", ""]
    for x in timeline["beats"]:
        vtt += [f"{ts(x['start'])} --> {ts(x['end'])}", next(b["text"] for b in beats if b["id"] == x["id"]), ""]
    (nd / "captions.vtt").write_text("\n".join(vtt), encoding="utf-8")
    # per-scene cue sheets with measured timings
    ok = True
    for sc in timeline["scenes"]:
        sheet, _, _ = L.build_scene_sheet(s, sc["id"], timing=timing, audio_sha=audio_sha, alignment_source=next(iter(srcs)) if len(srcs) == 1 else "tts_provider", duration_override=sc["duration"])
        p = cd / f"{sc['id']}.cues.json"; p.write_text(json.dumps(sheet, ensure_ascii=False, indent=1), encoding="utf-8")
        r = subprocess.run([sys.executable, str(VALIDATOR), "--production", str(p)], capture_output=True, text=True)
        line = (r.stdout.strip().splitlines() or r.stderr.strip().splitlines() or ["?"])[-1]
        print(f"  cue sheet {sc['id']}: duration {sc['duration']} s | words {len(sheet['words'])} | cues {len(sheet['cues'])} | validator exit {r.returncode}: {line[:120]}")
        ok &= r.returncode == 0
    print(f"total {total} s | spoken chars {timeline['chars_total']} | mix_norm sha256 {audio_sha[:16]} | cue sheets {'valid' if ok else 'INVALID'}")
    if not ok:
        sys.exit(3)


if __name__ == "__main__":
    main()
