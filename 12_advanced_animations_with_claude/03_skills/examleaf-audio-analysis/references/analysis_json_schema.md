# `analysis.json` schema (v1.0)

Written by `scripts/beat_grid.py`. Read by `examleaf-cue-sheet` (`spec.beats.analysis`) and by Reel re-timing in `examleaf-vertical-adapt`. JSON, UTF-8. Every time is in seconds, relative to the start of the analysed file.

## Fields

| Field | Type | Required | Meaning / invariant |
|---|---|---|---|
| `schema_version` | `"1.0"` | yes | Bump on any breaking change |
| `engine.name` | `"librosa"` or `"bed_metadata"` | yes | `bed_metadata` = grid copied from `examleaf-audio-compose` |
| `engine.version` | string or null | yes | librosa `__version__`, or the generator name |
| `source.path` | string | yes | Path as given (job-relative preferred) |
| `source.sha256` | hex string | yes | Hash of the analysed file (the audio, or `bed_meta.json`) |
| `source.sr_native` | int | yes | Rate in the file |
| `source.sr_used` | int | yes | Rate used for every call; **must equal** `sr_native` (#35) |
| `source.channels` | int | yes | Channels in the file before any downmix (#31) |
| `source.duration_s` | number | yes | Length of the analysed audio |
| `params.units` | `"time"` | yes | Anything else is invalid (#33) |
| `params.hop_length` | int | librosa only | Same hop for onsets, beats and RMS |
| `params.start_bpm` | number or null | librosa only | Never set together with `params.prior` (#37) |
| `params.prior` | object or null | librosa only | `{"dist": "norm", "loc", "scale"}` |
| `params.bpm_curve` | bool | librosa only | True means a time-varying bpm was supplied (#38) |
| `params.sparse` | `true` | librosa only | Sparse beat list |
| `tempo_bpm` | number | yes | Plain float (#32); 0 means no tempo found |
| `tempo_varies` | bool | yes | True when librosa returned more than one tempo value; `tempo_bpm` is then their median |
| `beats_s` | number[] | yes | Strictly increasing, all in `[0, source.duration_s]`; may be empty |
| `downbeats_s` | number[] or null | yes | Exact bar starts from `bed_meta.json`; `null` for librosa (not detected) |
| `onsets_s` | number[] or null | yes | Onset times (librosa); `null` for `bed_metadata` |
| `energy.hop_s` | number | librosa only | Seconds per RMS value (`hop_length / sr_used`) |
| `energy.rms` | number[] | librosa only | Linear RMS per hop |
| `fallback` | `null`, `"narration_grid"` or `"none"` | yes | See below (#34) |
| `warnings` | string[] | yes | Each prefixed with its edge-case number where one applies |

## Fallback semantics (#34)

- `null`: `beats_s` are music beats (detected, or exact from metadata).
- `"narration_grid"`: no beats were found, and `beats_s` holds phrase onsets from the narration alignment (the first word, plus every word after a pause ≥ 0.12 s). Downstream treats them as soft beats: Reel cuts may land on them, but nothing claims musical sync.
- `"none"`: no beats and no alignment. `beats_s` is `[]`. Scene code must tolerate it.

## Example: in-house bed (no detection)

```json
{"schema_version": "1.0",
 "engine": {"name": "bed_metadata", "version": "examleaf-audio-compose/compose_bed.py"},
 "source": {"path": "audio/bed/neutral/bed_meta.json", "sha256": "…", "sr_native": 48000, "sr_used": 48000,
            "channels": 1, "duration_s": 7.2},
 "params": {"units": "time", "note": "grid taken from compose_bed.py metadata; no detection needed"},
 "tempo_bpm": 100.0, "tempo_varies": false,
 "beats_s": [0.0, 0.6, 1.2, 1.8, 2.4, 3.0, 3.6, 4.2, 4.8, 5.4, 6.0, 6.6],
 "downbeats_s": [0.0, 2.4, 4.8], "onsets_s": null, "energy": null,
 "fallback": null, "warnings": []}
```

## Example: licensed stereo bed

```json
{"schema_version": "1.0", "engine": {"name": "librosa", "version": "0.11.0"},
 "source": {"path": "assets/licensed/bed_upbeat_01.wav", "sha256": "…", "sr_native": 44100, "sr_used": 44100,
            "channels": 2, "duration_s": 31.2},
 "params": {"units": "time", "hop_length": 512, "start_bpm": 100.0, "prior": null, "bpm_curve": false, "sparse": true},
 "tempo_bpm": 99.384, "tempo_varies": false, "beats_s": [0.511, 1.115, 1.718],
 "downbeats_s": null, "onsets_s": [0.499, 0.766], "energy": {"hop_s": 0.01161, "rms": [0.01214, 0.01533]},
 "fallback": null, "warnings": ["#31 downmixed 2 channels to mono before beat tracking"]}
```

The numbers in this example are illustrative, not measured.

## Example: silent clip with alignment

```json
{"tempo_bpm": 0.0, "beats_s": [0.1, 1.1], "fallback": "narration_grid",
 "warnings": ["#34 beat tracker returned 0 BPM and 0 beats (silent or beatless audio) [N41]"]}
```

(The other fields are as above.)

## Consumer rules

1. `examleaf-cue-sheet` adds `spec.beats.offset_s` (where the bed starts in scene time) and keeps beats in `[0, scene duration)`.
2. The consumer never rescales beats by a sample rate: they are already seconds.
3. A changed `source.sha256` invalidates every cue sheet built from this analysis. Rebuild and re-render.
