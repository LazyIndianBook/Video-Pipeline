# Mixing levels, ducking and loudness

**Scope.** What level each artefact leaves this skill at, and what the mixer (`examleaf-audio-production-engineer`) and QA (`examleaf-anim-qa`, `examleaf-audio-caption-qa`) do with it. This skill **never masters**: mastering has one owner (`06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 13: "Master: audio-production-engineer").

## 1. Levels leaving this skill

| Artefact | Level | Why |
|---|---|---|
| Bed stems (pad, pluck, perc) | Peak −12 dBFS each, before the mood gain; somber −6 dB more; end card ramps −6 → 0 dB | Known headroom so the mixer can sum three stems plus voice without clipping. [Recommendation] |
| SFX one-shots | Peak −6 dBFS | The per-cue `gain_db` in the cue sheet sets the mix level. [Recommendation] |
| Sample format | 48 kHz, 16-bit, mono | Matches the mono 48 kHz narration contract (`04_NARRATION_SUBPIPELINE.md` §12) |

Peak and RMS dBFS are written to `bed_meta.json` / `sfx_palette.json`. LUFS is **not** computed here: integrated loudness needs K-weighting and gating, which belong to the mastering tool.

## 2. Music under voice

- [V4-MP] §11: the music "sits about 15–20 dB under the voice", and is turned down or low-passed for somber moments.
- Report §5.4 [Recommendation]: "music 15–20 dB under the voice, sidechain-style ducking on speech".
- *15 Oct 2026 (AD-15 addendum, AD-37): one ExamLeaf policy replaces these reference values: muted under teaching; beds only in hooks, transitions, recaps and outros at 20–24 dB under speech; the numbers live in `04_harness_contract/vertical_safe_zones.tokens.json` `audio.music_policy`.*
- In practice the mixer measures the voice-only master, then sets the bed so it sits 20–24 dB below the voice level during speech (was 15–20 dB, the [V4-MP] figure), using the same meter for both. Between sentences, the bed may come up a few dB on hooks and outros only. Ducking attack and release values are not in the evidence; tune them by ear and record them.

## 3. Loudness target: house standard vs [V4-MP]

| Source | Integrated | Peak | Status |
|---|---|---|---|
| **ExamLeaf house** (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1; `04_NARRATION_SUBPIPELINE.md` §13) | **−16 LUFS ± 1** | **True peak ≤ −1 dBTP** (pass at ≤ −0.9) | **Adopted.** "An internal ExamLeaf starting target, not a universal platform requirement" |
| [V4-MP] §11 | About −14 LUFS | Peaks below −1.5 dBFS (sample peak, not true peak) | Noted, **not adopted** (section decision AD-04); −14 LUFS is only the Reels A/B variant, still under −1 dBTP |

Re-measure after the final mux: "the final encoded delivery should be measured again" (`04_NARRATION_SUBPIPELINE.md` §13). Two reasons:
- [N20] warns that some toolchains do "no normalising, EQ or fades unless you ask";
- edge case #39 is loudness jumping between scenes when nobody normalises.

## 4. Commands (owned by other skills; listed so the handoff is exact)

- **Mastering** (audio-production-engineer, [TESTED on signal fixtures]), from the narration repository root:
  ```sh
  PYTHONPATH=src python -m examleaf_narration.cli master <in.wav> --out <out.wav>
  ```
  This is a two-pass `loudnorm=I=-16:TP=-1:LRA=7` with `linear=true`, output `-ar 48000 -ac 1 -c:a pcm_s24le`, then re-measured. It passes when |I + 16| ≤ 1 and TP ≤ −0.9, and it refuses to overwrite its source.
- **Measurement** (QA), also from the narration repository root:
  ```sh
  PYTHONPATH=src python -m examleaf_narration.cli qa <audio.wav> --out qa.json
  ```
  This runs `signal_report` plus `loudness_measure` (an FFmpeg `loudnorm … print_format=json` pass, from which it reads `input_i` and `input_tp`).
- **Final MP4 audio for re-measurement** (standard FFmpeg usage; verify on your build):
  ```sh
  ffmpeg -i final.mp4 -vn -ac 1 -ar 48000 -c:a pcm_s24le final_audio.wav
  ```

## 5. Mixing checklist for the engineer

1. Voice-only master first, at the house target.
2. Add the bed under it (hooks, transitions, recaps, outros only; never under teaching): 20–24 dB lower during speech (15 Oct 2026), low-passed or down for somber cues, swell only on the end card.
3. Add SFX at their cue-sheet `gain_db`. Nothing may mask a STEM keyword in the narration. If a critical word is masked, lower or move the effect; never raise the voice above the target.
4. Master the full mix to −16 LUFS ±1, ≤ −1 dBTP.
5. Mux, extract, re-measure, then hand the numbers to `examleaf-anim-qa`, which owns the #39 check report for animation scenes. The listen still belongs to the audio lead.

## 6. What this skill must refuse

- "Normalise the bed to −14 LUFS so it pops": loudness is not set here, and the house target is −16.
- "Boost the SFX to +6 dB": positive gain on a one-shot is a mixer decision, and the validator warns on it.
- "Keep the bed running under the derivation for energy": music is off under the core explanation (AD-15).
