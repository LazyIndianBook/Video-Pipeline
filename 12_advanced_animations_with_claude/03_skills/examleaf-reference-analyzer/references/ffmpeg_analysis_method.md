# FFmpeg analysis method

All commands are **standard FFmpeg/ffprobe usage; verify on your build** (report §7.10). The research evidence set contains no FFmpeg documentation page, so this file describes the filters by their common, long-standing behaviour and the helper parses their logs defensively. Record `ffmpeg -version` with every run.

## 1. Probe: duration, fps, size

```sh
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,codec_name,duration:format=duration \
  -of json IN.mp4
```

- `r_frame_rate` is the stream's base (tick) rate; `avg_frame_rate` is frames divided by duration. Both are rational strings such as `30000/1001`; the helper converts them with `fractions.Fraction`.
- **VFR heuristic:** if they differ by more than 1 %, the file is probably variable-frame-rate (screen recordings and phone captures often are). Consequences: frame counts and frame indices are unreliable, so the helper reports everything in seconds from `pts_time`.
- `nb_frames` is often missing for some containers; the helper does not depend on it.
- `format.duration` is preferred over `stream.duration`.

## 2. Letterbox: cropdetect

```sh
ffmpeg -hide_banner -nostats -i IN.mp4 -vf fps=2,cropdetect -an -f null -
```

- Typical log line: `[Parsed_cropdetect_1 @ 0x…] x1:0 x2:1079 y1:656 y2:1263 w:1080 h:608 x:0 y:656 … crop=1080:608:0:656`.
- `fps=2` samples two frames per second to save time; cropdetect's default thresholds are kept.
- The helper takes the **most frequent** `crop=` suggestion (not the last), because fades and dark scenes produce outliers.
- Letterboxed if the active area is under 95 % of the container in either axis. A 16:9 picture inside a 1080×1920 container gives `active_aspect ≈ 1.776`.
- Limits: very dark shots, vignettes and paper textures with dark edges can fool cropdetect. Confirm with a still.

## 3. Cuts: scene-change select + showinfo

```sh
ffmpeg -hide_banner -nostats -i IN.mp4 -vf "select='gt(scene,0.30)',showinfo" -an -f null -
```

- The `scene` value is a per-frame difference score between 0 and 1; `select` passes only frames scoring above the threshold, and `showinfo` logs each passed frame.
- Typical log line: `[Parsed_showinfo_1 @ 0x…] n:   3 pts: 270270 pts_time:9.009 duration: 1001 …`. The helper extracts every `pts_time:` value.
- **Threshold tuning:** 0.30 is a starting value, not a verified constant. Paper-slide transitions in the collage style ([V4-MP] 0.5–0.7 s sheet slides) and dissolves change the picture gradually, so per-frame scores stay low; lower the threshold (for example 0.2) and verify on stills. Flash-heavy music videos ([V1] warns of "bright, fast flashes") produce false cuts; raise the threshold.
- **Duplicate detections:** a cut sometimes scores high on two adjacent frames. The helper merges cuts closer than one frame period.
- **Shot list:** boundaries are `[0, cuts…, duration]`; shot lengths are the differences. Cuts within one frame of the end are dropped.

## 4. Static holds: freezedetect

```sh
ffmpeg -hide_banner -nostats -i IN.mp4 -vf freezedetect=n=-60dB:d=0.5 -an -f null -
```

- Typical log lines: `lavfi.freezedetect.freeze_start: 3.2`, `lavfi.freezedetect.freeze_duration: 1.6`, `lavfi.freezedetect.freeze_end: 4.8`.
- `n` is the noise tolerance and `d` the minimum duration. A stricter `n` misses holds with idle sway ([V4-MP] "never frozen" styles); a looser one merges slow motion into holds.
- **Use:** an upper-bound proxy for how long text sits still. In ExamLeaf styles text is often on a gently swaying layer, so freezedetect will under-report holds there. It never overrides the 1.2 s floor [N60].

## 5. Palette and stills

Palette (per shot midpoint, active area only when letterboxed):

```sh
ffmpeg -hide_banner -v error -ss T -i IN.mp4 -frames:v 1 -vf [crop=W:H:X:Y,]scale=48:48 -f rawvideo -pix_fmt rgb24 -
```

- The helper reads the raw bytes from stdout, quantises each pixel to 3 bits per channel (512 buckets), and returns the six largest buckets with their mean colour and pixel share.
- Aspect distortion from `scale=48:48` does not matter for colour counts.
- Limits: anti-aliased edges and gradients spread across buckets; the result is a mood palette, not exact brand hexes.

Stills (quarantine):

```sh
ffmpeg -hide_banner -v error -y -ss T -i IN.mp4 -frames:v 1 OUT.png
```

- Placing `-ss` before `-i` seeks fast on keyframes; precision is adequate for study stills.

## 6. What the helper does not do

- No OCR. Text-hold estimates come from freezedetect and human review of stills.
- No audio analysis (owned by `examleaf-audio-analysis`; librosa traps #31–38 live there).
- No downloads, no installs, no network.
- No asset export.

## 7. Failure signatures

| Symptom | Likely cause | Action |
|---|---|---|
| `shots.count` = 1 on an obviously edited video | Threshold too high, or gradual transitions | Lower threshold; verify with stills |
| Hundreds of cuts per minute | Flashing, particles, film grain | Raise threshold; flag #56 for the style owner |
| `letterboxed: true` on a dark full-frame video | cropdetect fooled by dark content | Check a still; override in the request notes |
| `fps: null` | Odd container or stream metadata | Report; use seconds-based stats only |
| Exit 2 | ffmpeg/ffprobe missing or input missing | Run the preflight; supply the file |
