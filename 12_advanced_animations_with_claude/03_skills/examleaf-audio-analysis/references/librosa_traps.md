# librosa traps and their guards

Every claim below is quoted from the librosa 0.11 documentation, as recorded in `12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md`:
- `beat_track`: https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html, [N36]–[N43];
- tutorial: https://librosa.org/doc/0.11.0/tutorial.html, [N81].

The guard functions live in `scripts/beat_grid.py`. Pin the librosa version in the audio environment and re-read these pages when it changes.

## #31 Stereo input with `sparse=True` [N37], [N43]

- **Doc:** "multi-channel input is only supported when `sparse=False`." With `sparse=False`, "detections are encoded as a dense boolean array" [N43].
- **Symptom:** an error on stereo files, or, if someone flips `sparse=False` to silence it, a per-frame boolean array where downstream code expects a short list of beat times.
- **Guard:** load with `mono=False` so the channel count is visible and recorded, then `librosa.to_mono(y)` before any analysis. `check_channels(channels, sparse)` refuses multi-channel input with sparse output. The cue sheet only accepts a sparse list of seconds.

## #32 Tempo is an ndarray [N38]

- **Doc:** "By default, the tempo is returned as an ndarray even for mono input."
- **Symptom:** `TypeError` in JSON serialisation, string formatting, or comparisons such as `if tempo > 0:` on arrays.
- **Guard:** `tempo_scalar(tempo)` flattens anything with `.ravel()`. An empty array gives 0.0; one value gives `float(v)`; several values give the median, with `tempo_varies: true` recorded. Do not call `float()` on an ndarray with more than zero dimensions: newer NumPy versions deprecate converting a non-0-d array to a scalar.

## #33 Beats in frames by default [N39]

- **Doc:** "By default, 'frames' are used."
- **Symptom:** sync off "by a large factor" (report §8). At 48 kHz with hop 512, frame 94 is about 1.0 s, but a scene would read it as 94 s.
- **Guard:** always pass `units='time'`. `check_call_args()` refuses any other unit, and `check_beats(beats, duration)` refuses beats beyond the clip or out of order. The cue-sheet builder independently refuses `params.units != "time"` and beats past `source.duration_s`.

## #34 Silent or beatless audio gives 0 BPM and an empty list [N41]

- **Doc:** "beat_tracker estimates 0 BPM and returns an empty list."
- **Symptom:** an empty `beats[]`, divide-by-zero in "bars = duration × bpm / 240", or animation that never fires its beat cues.
- **Guard:** `resolve_beats()` returns `fallback: "narration_grid"` built from aligned words: the first word, plus every word that follows a pause ≥ 0.12 s ([Recommendation] `PHRASE_GAP_S`). Without words it returns `fallback: "none"` and an empty list, with a warning. Scene code must handle an empty beats list; the brief says so explicitly.

## #35 Resampling drift [N81]

- **Doc:** "By default, all audio is mixed to mono and resampled to 22050 Hz at load time."
- **Symptom:** cues slip progressively. The usual cause is frames computed at one rate and converted with another (for example, loaded at 22050 Hz and converted with 48000 Hz). Times in seconds computed consistently are fine, but mixed rates are not.
- **Guard:** `librosa.load(path, sr=None, mono=False)` keeps the native rate. One `sr` variable is passed to every librosa call. `check_sr(load_sr, analysis_sr)` refuses a mismatch. `analysis.json` records `sr_native` and `sr_used`, and the cue sheet warns when they differ in a foreign file.

## #36 ParameterError [N40]

- **Doc:** raises "if neither `y` nor `onset_envelope` are provided, or if `units` is not one of" the allowed values.
- **Symptom:** an uncaught exception with a stack trace.
- **Guard:** `check_call_args(y_present, onset_present, units, …)` runs before the call. The call itself is wrapped in `except librosa.util.exceptions.ParameterError`, which becomes a structured blocker (exit 1, `edge_case: "#36"`).

## #37 `start_bpm` versus `prior` [N36]

- **Doc:** `start_bpm` defaults to 120, and "If provided, `start_bpm` will be ignored" when a prior is given.
- **Symptom:** a hint that silently does nothing, which leaves people confused when the grid comes out wrong.
- **Guard:** `check_call_args()` refuses both together. Pass one or the other: a hint for known tempos, a prior for uncertain ones. `--prior-norm MEAN STD` builds `scipy.stats.norm(loc=MEAN, scale=STD)`. That librosa accepts a frozen scipy distribution as `prior` should be confirmed on the pinned version.

## #38 Time-varying `bpm` shape [N42]

- **Doc:** "the shape of `bpm` should match that of `onset_envelope`."
- **Symptom:** a shape or broadcast error, or a mis-aligned tempo curve.
- **Guard:** `check_bpm_shape(len(curve), len(onset_env))` accepts a single value or an exact-length curve, and refuses anything else before librosa is called.

## Practical defaults

| Parameter | Value | Why |
|---|---|---|
| `sr` | `None` (native) | #35 |
| `mono` on load | `False`, then explicit `to_mono` | #31 visibility |
| `hop_length` | 512 | librosa's default hop; same hop for onsets, beats and RMS |
| `units` | `'time'` | #33 |
| `sparse` | `True` (default) | Sparse beat list; downmix instead of dense output |
| `trim`, `tightness` | librosa defaults | No evidence to change them |

## What the selftest covers without librosa

`toy_beat_track()` is a test-only autocorrelation tracker over an onset envelope. It exists so the guard logic runs offline: synthetic 100 BPM impulses must give 100 ± 0.5 BPM and an exact 0.6 s grid, and a silent envelope must give `[0.0]` tempo and no beats, which takes the #34 path. It is **never** used for production analysis, and the CLI exposes no flag to select it.
