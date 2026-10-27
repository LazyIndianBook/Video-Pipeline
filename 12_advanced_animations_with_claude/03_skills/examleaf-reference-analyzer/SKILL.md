---
name: examleaf-reference-analyzer
description: "Use when an ExamLeaf style or pacing decision needs measured numbers from a reference video (mp4/mov) instead of adjectives. Runs ffprobe and standard FFmpeg filters (scene-change select + showinfo, cropdetect, freezedetect) through a stdlib Python helper and writes one JSON: fps and variable-fps flag, duration, orientation, letterbox crop, shot lengths, cut rhythm, static-hold estimates, palette swatches and quarantined stills. References are analysed only and never reused as assets or image-model references. Does not choose styles, re-lay out 16:9 material, or write briefs."
---

# examleaf-reference-analyzer

## Status and boundary

- **Status:** proposed agent workflow; authored, not agent-evaluated. `scripts/analyze_reference.py --selftest` passes offline using synthetic FFmpeg logs. The FFmpeg command lines are standard FFmpeg usage and must be verified on the render box's build (`ffmpeg -version`); they were not executed in this environment because FFmpeg was not installed.
- **Owns:** `reference_analysis.json` per reference and the quarantined stills folder.
- **Does not own:** style selection (`examleaf-style-guides`), vertical re-layout (`examleaf-vertical-adapt`), the brief (`examleaf-anim-brief`), asset rights (`examleaf-asset-library`), audio beat analysis (`examleaf-audio-analysis`).
- **Why it exists:** [V2] and [V3] show that a reference video for pacing beats adjectives; [V3] says to study "layout structure and its exact typography treatment". Report §7.10 [Recommendation] turns that into measurement: duration and fps with ffprobe, cuts with the scene-change select filter plus `showinfo`, one still per shot, and the measured numbers fed into the brief. Report §10.2 specifies this skill.

## Invocation

**Trigger when:**
- A new house style is being drafted or revised and the style owner supplies a reference clip.
- A brief needs pacing numbers (median shot length, cut rhythm, hold estimates) for a scene or reel.
- A reviewer asks "how fast does the reference actually cut?" or "what palette does it use?".

**Do not trigger for:**
- Music or narration analysis (beats, onsets, energy) → `examleaf-audio-analysis`.
- Re-laying out a 16:9 reference into 9:16 → `examleaf-vertical-adapt` (this skill only reports the letterbox and orientation).
- Extracting frames to use as cutouts, backgrounds or image-model references. Forbidden: references are analysis-only.
- QA of ExamLeaf's own renders (flash, holds, safe zones) → `examleaf-anim-qa`.
- Downloading a reference from a platform. This skill reads a local file supplied by the user; acquisition and its rights are the user's responsibility.

## Inputs

| Field | Type | Rule |
|---|---|---|
| `input` | local path to mp4/mov/webm | must exist; never a URL |
| `rights_note` | string | who supplied it and why; recorded in the request, not in the JSON output |
| `scene_threshold` | float, default 0.30 | starting value for `select='gt(scene,T)'`; tune per reference (lower for soft cuts) |
| `freeze_min` | float seconds, default 0.5 | minimum static interval counted as a hold |
| `max_stills` | int, default 12 | stills at shot midpoints |
| `stills_dir` | path | quarantine folder inside the job workspace |

Example request:

```json
{"input":"jobs/style-collage-v2/refs/reference_a.mp4",
 "rights_note":"supplied by style owner for pacing study only",
 "scene_threshold":0.30,"freeze_min":0.5,"max_stills":12,
 "stills_dir":"jobs/style-collage-v2/refs/quarantine_stills"}
```

## Outputs and contracts

`reference_analysis.json` (schema `1.0`, full example in `templates/reference_analysis.example.json`):

| Key | Content |
|---|---|
| `source` | `{path, sha256, rights:"analysis_only"}` |
| `probe` | `{width, height, duration_s, codec, r_frame_rate, avg_frame_rate, fps, vfr_suspected, orientation}` |
| `letterbox` | `{letterboxed, crop:"w:h:x:y", active_aspect, container_aspect}` |
| `shots` | `{count, cut_times_s[], shot_lengths_s[], median_s, mean_s, p10_s, p90_s, min_s, max_s, cv, cuts_per_minute, histogram}` |
| `holds` | `{method, intervals[], count, median_s}` (freezedetect proxy) |
| `palette` | `{per_shot:[{t_s, swatches:[{hex, share}]}], overall:[{hex, share}]}` |
| `stills`, `stills_policy` | quarantined paths; "never assets" |
| `commands`, `ffmpeg_version` | exact command lines run and the FFmpeg version line |
| `warnings` | VFR, letterbox, landscape, no-cuts |

Blocker (exit 2): `{"status":"blocked","skill":"examleaf-reference-analyzer","error":…,"action":…}`.

`templates/handoff.json` follows the library schema; `output_ids` carries the analysis SHA-256.

## Dependencies

- Python 3 standard library (`subprocess`, `json`, `statistics`, `fractions`, `hashlib`).
- **FFmpeg and ffprobe** on PATH: version not pinned in the evidence (verify; record `ffmpeg_version` in every output). The render-box preflight (`12_advanced_animations_with_claude/04_harness_contract/preflight.sh`) checks for FFmpeg because HyperFrames needs it too [N8].
- Related: `12_advanced_animations_with_claude/04_harness_contract/reference_analysis.sh` (agreed path, owned by the harness-contract folder): a shell wrapper with the same probe and scene-change steps, a smaller `analysis.json`, and exit code 3 when FFmpeg is missing. Use one tool per job. This helper adds VFR, letterbox, static-hold and palette fields and exits 2 when FFmpeg is missing; downstream skills read this helper's JSON shape.
- No network. No installs.

## Execution

1. **Place the reference** in `jobs/<job>/refs/`. Record `rights_note` in the request file. Never fetch from a URL inside this skill.
2. **Preflight:** `command -v ffmpeg ffprobe`. If missing, stop with the blocker (exit 2); do not attempt an install.
3. **Run the helper:**
   ```sh
   python3 12_advanced_animations_with_claude/03_skills/examleaf-reference-analyzer/scripts/analyze_reference.py \
     --input jobs/style-collage-v2/refs/reference_a.mp4 \
     --out jobs/style-collage-v2/refs/reference_a.analysis.json \
     --stills-dir jobs/style-collage-v2/refs/quarantine_stills --scene-threshold 0.30
   ```
   It runs, in order (standard FFmpeg usage, verify on your build):
   - `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,codec_name,duration:format=duration -of json IN`
   - `ffmpeg -hide_banner -nostats -i IN -vf fps=2,cropdetect -an -f null -`
   - `ffmpeg -hide_banner -nostats -i IN -vf "select='gt(scene,0.30)',showinfo" -an -f null -`
   - `ffmpeg -hide_banner -nostats -i IN -vf freezedetect=n=-60dB:d=0.5 -an -f null -`
   - per shot midpoint: a 48×48 `rgb24` raw frame for palette quantisation (cropped to the active area when letterboxed) and, if requested, one PNG still.
4. **Sanity-check cuts.** Open three stills and compare with `cut_times_s`. If `shots.count` ≤ 1 or many cuts sit inside one obvious shot, re-run with a different threshold (lower for dissolves and paper-slide transitions, higher for flashy material). Record the final threshold.
5. **Interpret** with `references/interpreting_metrics.md`: median and p90 shot length set beat spacing; `cuts_per_minute` sets transition budget; `holds.median_s` is an upper-bound proxy for text holds and never lowers the 1.2 s floor [N60]; palette `overall` informs, but never replaces, the style tokens' dominant + accents rule [N52].
6. **Hand off** the JSON to `examleaf-anim-brief` (as `reference_analysis`, rights `analysis_only`) and, for style work, to `examleaf-style-guides`. Send letterboxed or landscape references' layout questions to `examleaf-vertical-adapt`.

## Decision rules

- **Threshold:** start at 0.30; this is a tunable parameter, not a verified constant. Document any change.
- **Minimum shot gap:** cuts closer than one frame (1/fps) merge, so a single cut detected on two adjacent frames counts once.
- **VFR:** if `r_frame_rate` and `avg_frame_rate` differ by more than 1 %, flag `vfr_suspected`; report times in seconds from `pts_time` (robust), never frame indices; ExamLeaf scenes still render at a fixed fps.
- **Letterbox:** if the most frequent `cropdetect` suggestion is under 95 % of the container in either axis, mark `letterboxed` and analyse palette on the active area only.
- **Landscape references:** pacing numbers transfer; layout does not. Always warn (#49).
- **Holds:** freezedetect finds static intervals, which over-count (static backgrounds) and under-count (text over moving backgrounds). Use only as a sanity bound.
- **Palette:** 3-bit-per-channel quantisation of tiny frames; good for "warm muted cream with tomato accents", not for exact brand hexes.
- **Rights:** if the supplier cannot state why the reference may be studied, stop and ask; never proceed on "found it online".

## Edge cases handled

| Master # / case | Detection | Response |
|---|---|---|
| Variable-fps input (report §10.2) | `r_frame_rate` ≠ `avg_frame_rate` by >1 % | `vfr_suspected: true`, warning, seconds-based stats only |
| Letterboxed 16:9 reference (report §10.2) | `cropdetect` crop < 95 % of container | `letterbox.crop` reported; palette on active area; route layout to `examleaf-vertical-adapt` |
| Missing ffprobe/ffmpeg (report §10.2; #22 analogue) | `shutil.which` returns none | Exit 2 with structured blocker naming the preflight; no install attempt |
| Copyrighted reference reused as an asset (report §10.2) | Any request to export frames for assets or image-model references | Refuse; stills marked quarantine; `rights: analysis_only` in output |
| #49 16:9 guide in a 9:16 pipeline | `orientation: landscape` or letterboxed | Warning; numbers only; vertical re-layout elsewhere |
| #50 Short headline hold | `holds.median_s` < 1.2 s in reference | Report it, but downstream floors stay at 1.2 s [N60] |
| No detectable cuts | `shots.count` ≤ 1 | Warning; re-run with a lower threshold or treat as one continuous shot |
| #56 Photosensitive flashes in the reference | Many sub-0.1 s shots (histogram `<0.5` bucket heavy) | Note in warnings for the style owner; never copy flash rhythm into ExamLeaf |

## Tests and acceptance

- **Helper:** `python3 scripts/analyze_reference.py --selftest` parses a synthetic ffprobe JSON (CFR and VFR), a showinfo log with a duplicate adjacent-frame cut, a cropdetect log (letterboxed 16:9 inside 1080×1920), a freezedetect log and a synthetic two-colour raw frame using [V4-MP] cream and tomato hexes.
- **Eval cases:** `evals/cases.json` (3 positive, 4 negative).
- **Acceptance on a real reference:** stills at three random cut times visibly start new shots; `commands` and `ffmpeg_version` recorded; `source.sha256` matches the file; no still path appears in any AssetManifest.
- A passing selftest is not an evaluation of the Skill's model behaviour.

## Errors, fallback, escalation

- **Missing FFmpeg:** blocker (exit 2). Fallback: a human watches the reference and fills shot lengths manually in the same JSON shape, marked `"method":"manual"`.
- **FFmpeg filter error on an unusual container:** retry once after remuxing is not this skill's job; report the stderr tail and stop. At most two repair attempts (threshold change, `--max-stills` reduction).
- **Very long references:** analyse a representative excerpt the style owner chooses; record the excerpt range.
- **Escalate** when rights are unclear, when the reference contains photosensitive flashing, or when the numbers contradict the style guide (style owner decides).
- **Cost cap:** CPU only, no provider spend.

## Cost/performance

Four decoding passes plus one seek per still; runtime scales with reference length and resolution (not measured here). Run it once per reference and cache the JSON by `source.sha256`. No tokens are spent on video; Claude reads only the JSON, which also keeps context small (Opus 5.5 cannot watch video; it reads analysis JSON, compare #13 and [N71]).

## Security

- The input file is untrusted. It is passed as an argument to FFmpeg, never interpreted by Python. Run on the render box under the renderer role (no secrets, no internet after staging).
- Metadata strings (titles, comments) are not copied into the JSON.
- No uploads; stills never leave the job workspace; nothing is published.
- Copyright: analysis of pacing, palette and layout is the purpose; reproduction of frames, characters or typography as assets is out of scope and refused.

## Handoff

- **To:** `examleaf-anim-brief` (`reference_analysis` input), `examleaf-style-guides` (style drafting), `examleaf-vertical-adapt` (landscape/letterbox layout questions).
- **Files:** `<ref>.analysis.json`, quarantined stills folder, `templates/handoff.json` filled with `input_ids` (reference SHA-256) and `output_ids` (analysis SHA-256), `requires_expert_review: true` (a human confirms the cut threshold).

## References

- `references/ffmpeg_analysis_method.md`: each command, what its log lines look like, how the helper parses them, and known limits.
- `references/interpreting_metrics.md`: how to turn the numbers into brief and style decisions for 9:16 ExamLeaf content.
- `references/contract.md`: handoff and security rules.
- Report §1.2, §7.10, §8 (#49, #50, #56), §10.2, §11.9.
