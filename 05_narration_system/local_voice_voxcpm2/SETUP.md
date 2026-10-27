# Local voice-over: VoxCPM2 through MLX Audio (set up 27 Oct 2026)

**Status (27 Oct 2026).** The founder decided that this voice system replaces ElevenLabs for every voice-over (PD-29 in `17_professor_diki_simplified/DECISIONS_PD.md`, RD-55 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`). It is installed on the founder's MacBook Pro (M1 Pro, 16 GB, macOS 15.6) and tested end to end. Until the founder records the reference (§3), lessons are voiced for testing with a designed default voice (§3a, PD-29a); the test build is `17_professor_diki_simplified/demo/physics_v4_method_testvoice/`. Source plan, verbatim: `SOURCE_Local_Voice_and_Animated_EdTech_Production_on_M1_Pro.md` (software checked by its author on 27 Oct 2026).

## 1. What is installed, and where

| Item | Where | Notes |
|---|---|---|
| Studio folder | `~/Movies/DikiStudio/` (source plan §2) | `voice/`, `models/`, `scripts/`, `audio/`, `exports/`. Outside the project, so the 3 GB of models never sit in the Desktop folder |
| Python environment | `~/Movies/DikiStudio/.venv` | Python 3.11.14 arm64 from the Homebrew `python@3.11` already on the Mac. Installed with pip into the venv only: mlx 0.32.4, mlx-audio 0.6.2, soundfile, imageio-ffmpeg (static FFmpeg), playwright (drives the installed Google Chrome). No brew, nothing system-wide. This is also the pipeline's interpreter now, replacing the old session-scratchpad `narr_venv` |
| Voice model | `models/VoxCPM2-4bit` (`mlx-community/VoxCPM2-4bit`, 2.30 GB) | Model card licence `apache-2.0` (base `openbmb/VoxCPM2`); output 48 kHz. Compare the 8-bit checkpoint (3.23 GB) only if the audition asks for it (source plan §5) |
| Speech-to-text | `models/whisper-small.en-asr-fp16` (485 MB) | Local Whisper small.en through MLX Audio: word times for the cue sheets and the heard-vs-script check. It replaces ElevenLabs' provider timestamps and Scribe (QA A7). This is the source plan's caption model, run inside MLX Audio instead of a brew-installed whisper.cpp |
| Audition script | `~/Movies/DikiStudio/narrate.py` | Source plan §4, verbatim except for one added line, `mx.set_cache_limit(0)`, which halves peak memory (§8). A text file in, a float WAV out, with the WPM reported |
| Pipeline step | `16_pilot_builds_2026-10-16/tooling/narrate_voxcpm.py` | Voices each beat into the narration cache; `narrate.py` then builds the timeline, mix, captions and cue sheets |
| Studio files in git | `studio/` next to this file: `narrate.py` and `voice/designed/` (the three designed voices with `designed_voices.json`) | The repository copy of the studio's own files. On a new Mac: create the venv and download the models (§1), then run `cp -R studio/. ~/Movies/DikiStudio/` and `cp ~/Movies/DikiStudio/voice/designed/male_30s.wav ~/Movies/DikiStudio/voice/default_reference.wav`. The founder's `voice/reference.wav` is never committed |

Disk: 11 GB were free before setup (the drive is 98 % full) and about 8 GB after it. Renders and new takes need room, so free some space before a batch.

## 2. Settings (source plan §4, unchanged for the first pilot)

Reference cloning plus a delivery instruction (not the continuation or "Hi-Fi" mode, which can ignore the instruction). Instruction: "Brisk, energetic English teaching. Clear pronunciation, natural emphasis, and short natural pauses." `inference_timesteps` 10, `cfg_value` 2.0. The seed is 20261016 for a beat's first take and goes up by one per `--redo`, so a take can be reproduced. There is no numeric speed control: pace comes from the script length and the speech-only `narrate.py --tempo` (PD-22; keep changes within about 5–10 %).

## 3. Record the voice reference (founder, once)

1. Use a quiet room with soft furnishings and the microphone you already have. Keep the same distance from the microphone throughout; turn slightly away if plosives pop.
2. Record two or three takes of 45–60 seconds, reading a simple explanation in the delivery you want learners to hear: engaged, clear, conversational, brisk. Use your normal accent. QuickTime Player (File → New Audio Recording) is enough; Audacity is optional.
3. Pick a clean **15–20 second** excerpt: continuous speech, natural sentence variety, no mistakes, no music, no coughs. Do not apply noise removal, reverb or other effects.
4. Save it as a mono WAV, preferably 48 kHz, at **`~/Movies/DikiStudio/voice/reference.wav`**. Keep the full recording, and save a second clean excerpt as `voice/reference_backup.wav`. Or send Claude the recording and the start second, and Claude cuts and converts it with the venv's FFmpeg.
5. Keep using the same reference for the whole series. Changing it changes `voice.voice_id`, which re-voices every beat.

The reference is the founder's own voice, recorded by the founder for this purpose. That is the consent basis, so note the date in the series record. No training and no transcript are needed.

## 3a. Default test voice, until the reference exists (PD-29a)

The founder asked for a proper default voice for testing first, as ElevenLabs' stock voices had been. VoxCPM2's voice design (an instruction with no reference audio) made three voices to the Super Teacher brief: an adult teacher speaking clear Indian English, warm, precise and energetic without shouting. Each speaks the same 52-word passage. Files, descriptions, seeds and metrics are in `~/Movies/DikiStudio/voice/designed/` (`designed_voices.json`).

| Voice | Median pitch | Pace (design) | Whisper | Role |
|---|---|---|---|---|
| `male_30s.wav` | 139 Hz (IQR 122–167) | 178 WPM | 1.00 | **Default**, copied to `voice/default_reference.wav` |
| `female_30s.wav` | 242 Hz (IQR 198–309) | 201 WPM | 1.00 | Alternative |
| `male_40s_calm.wav` | 133 Hz (IQR 119–170) | 177 WPM | 1.00 | Alternative: calmer, deeper |

`narrate_voxcpm.py` clones `voice/default_reference.wav` while `voice/reference.wav` is missing. It prints `TEST voice` and records `voice.test_voice: true`, and such a narration is not released. To switch the test voice, copy another designed file over `voice/default_reference.wav`, or pass `--reference voice/designed/female_30s.wav`; the beats re-voice because the `voice_id` changes. Once the founder's `voice/reference.wav` exists, it is used automatically. A design is regenerated by the same instruction and seed (`mx.random.seed(seed)`, 10 steps, CFG 2.0).

## 4. Audition before building a lesson (source plan §5)

```sh
cd ~/Movies/DikiStudio && source .venv/bin/activate
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
python narrate.py scripts/pilot_01.txt audio/pilot_01_take1.wav   # refuses to overwrite: name each take
```

Write three passages as plain-text files in `scripts/`: a natural explanation of 30–60 words; one with technical terms, an acronym and a number; and a connected 80–100-word explanation generated in groups. A passage passes when the meaning is exact, the voice is consistent and recognisably yours, the terms are pronounced correctly, and the pace is 180–210 WPM. If a passage fails, change one thing at a time: first the reference recording, then the script wording, then the 8-bit checkpoint, then Qwen3-TTS Base with an exact reference transcript, and finally your own direct recording.

## 5. Voice a lesson in the pipeline

```sh
PY=~/Movies/DikiStudio/.venv/bin/python; T=16_pilot_builds_2026-10-16/tooling; V=<video folder>
$PY $T/narrate_voxcpm.py $V/script.json              # one take per beat + word times; prints LISTEN for suspect beats
$PY $T/narrate_voxcpm.py $V/script.json --redo b05   # a new take of a beat that sounded wrong
$PY $T/narrate.py $V/script.json                     # timeline, mix, captions, cue sheets (no key, no network)
$PY $T/render.py $V/script.json
$PY $T/qa.py $V/script.json                          # A1–A21 against the script's own format; A7 is local Whisper
```

`narrate_voxcpm.py` skips unchanged beats, so editing one beat's text re-voices only that beat. The raw float take of each beat stays as `narration/beats/<beat>.take.wav`. The first narration of a new script sets `voice.rate_scale` (PD-22), which is measured active WPM divided by the planned WPM.

## 6. Offline

Installation and the model downloads needed the internet. Generation needs nothing: `narrate_voxcpm.py` and `pilotlib.stt_words` set `HF_HUB_OFFLINE=1` and load both models from `models/`. Both smoke tests below ran with `HF_HUB_OFFLINE=1`.

## 7. What was taken from the source plan, and what was not

Taken: VoxCPM2-4bit through MLX Audio; reference cloning with the delivery instruction; 10 steps and CFG 2.0; 195 WPM as the working target within 180–210, which matches PD-28a in practice (about 180 words in a 60-second short); small pitch-preserving tempo corrections (`narrate.py --tempo`); Whisper small.en; offline mode; keeping every take; recording the reference, model and tempo with each episode (`timeline.json` holds the voice block).

Not taken, because the founder adopted the voice system only: Keynote scenes and DaVinci Resolve finishing (the HTML collage renderer, FFmpeg mux and QA stay); whisper.cpp through brew (the same small.en model runs in MLX Audio, with no system install); brew Python (the existing 3.11 was used).

Changed: the source plan suggests 30–60-word requests. The pipeline voices one beat per request (3–27 words), because it places each beat's words and pauses itself (PD-01). If joins between beats sound choppy, group consecutive beats into one request and split them at the word gaps.

## 8. Measured on this Mac (27 Oct 2026, stand-in reference)

| Test | Result |
|---|---|
| Audition script, 36 words, offline | 12.16 s of audio at **178 WPM**; 48.5 s to generate (about 0.25× real time); 62.5 s including the model load; peak memory footprint 11.1 GB with MLX's default buffer cache |
| Memory | Weights 2.30 GB once loaded. With the default cache the process grew to 10 GB; with swap already 14.7 of 16 GB full (a virtual machine, Chrome and Claude were open), the second beat took 5 minutes instead of about 15 s. With `mx.set_cache_limit(0)`, peak is 4.6–5.0 GB at the same speed (3.5 s of audio in 11–13 s), so both scripts now set it. Close heavy apps (the VM, extra Chrome windows) before a narration run, and never run one alongside a render |
| Whisper small.en word times | Model load 1.5 s; 0.6 s per 6-second clip once warm. The first run on a fresh environment took about 60 s (one-time compile). A spelling hint (`pilotlib.STT_PROMPT`, the brand line) stops Whisper writing "Dickey" for Diki and "iR" for "I R" |
| Pipeline, `demo/physics_v4_method` (copy), 13 beats, 166 words | All beats voiced and timed in 3 min 14 s (both model loads included), peak memory 4.1 GB, about 55 s of audio. Active pace **194 WPM** overall (171–236 per beat): on the source plan's 195 target with no tempo change, but measured with the stand-in voice, so the founder's clone will differ. The heard-vs-script check passed 11 beats on the first pass and flagged b05 and b13, both Whisper spellings; with the hint, `--redo b05,b13` gave take 2 of both at 1.00 |
| Default test voice `male_30s`, `demo/physics_v4_method_testvoice` | 13 beats voiced in about 3 min. **185 WPM active** (inside 180–210), 172 effective over 57.9 s; `narrate.py --tempo 1.03` would bring it to about 190. On the first pass 12 of 13 beats matched under Whisper; b04's "Ohm's" was heard as "ahm's", and `--redo b04` (take 2) matched |
| Render and QA of that build | At tempo 1.0 the short ran 57.9 s, and QA gave 17 pass, 3 warn and 1 fail (A11, length). At `--tempo 0.96` it runs 60.2 s, and QA gives **18 pass, 3 warn, 0 fail**: A7 (local Whisper) passes, and the warnings are A8 (v1 band), A9 (no determinism re-check) and A19 (one 7-word beat at 240 wpm). Rendered with the GPU on and `--no-determinism`, 1,806 frames took 11.6 min; the default software raster ran about half as fast. QA took 23 s |
| Build without ElevenLabs | `narrate.py` with no API key: 53.9 s timeline, room-tone mix, two-pass master, captions, and a cue sheet that passes `validate_cue_sheet.py --production` with `alignment_source` `forced_alignment` |
