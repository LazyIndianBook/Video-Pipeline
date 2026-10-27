# Synthesis recipes for seeded music beds

**Scope.** How `scripts/compose_bed.py` builds a bed, why each choice was made, and how to change it without breaking determinism. Sources: report §5.1 ([V2], [V3], [V4-MP] §11, [Recommendation]); [N61] (pure function of time, contested). Library versions for NumPy or SoundFont routes are **not verified**; confirm them in the pilot before use.

## 1. What the evidence says

- [V2]: Opus 5.5 "can compose original music and create sound effects" with Python, and a soothing music video used Opus-composed Python music.
- [V3]: when building in Remotion, you must ask for SFX and music generated with Python, because audio "might not automatically" be included (#10).
- [V1]: the SFX in all six music videos were AI-made.
- [V4-MP] §11 gives the target sound:
  - a whimsical storybook track (pizzicato strings, ukulele, glockenspiel, soft clarinet, light brushed percussion) at **about 100 BPM**, instrumental;
  - about 15–20 dB under the voice ([V4-MP] reference; ExamLeaf uses 20–24 dB and only in hooks/transitions/recaps/outros, AD-15 addendum 15 Oct 2026);
  - **low-passed or turned down for somber moments**, with a slight swell on the end card.
- Report §5.1 recipe [Recommendation]:
  - oscillators, ADSR envelopes and simple filters;
  - **fix the tempo first**;
  - generate **bar-aligned stems** (pad, plucks, percussion) so music can be cut to any scene length;
  - **seed every random call**.

Nothing in the evidence gives voicing, chord or mix-level numbers beyond the above. Every concrete number below is a [Recommendation] starting point unless it is cited.

## 2. Building blocks (all stdlib)

| Block | Implementation | Notes |
|---|---|---|
| Sine oscillator | `sin(2π·phase)`, phase += f/sr | Plucks, kick body, bell partials |
| Saw oscillator | `2·(phase − floor(phase + 0.5))` (naive) | Pad. It aliases, so it is always followed by a low-pass |
| ADSR | Linear attack/decay to a sustain level, linear release inside the note length | Pad 0.3/0.2/0.8/0.4 s; pluck 0.005/0.25/0/0.05 s |
| One-pole low-pass | `y += a·(x − y)`, `a = 1 − exp(−2π·fc/sr)` | 6 dB/octave. Gentle, which suits "muffle" |
| One-pole high-pass | `x − lowpass(x)` | Brush noise, tear, pencil |
| Seeded noise | `random.Random(seed).random()·2 − 1` | Never `random.random()` at module level |
| Writer | `wave` module, mono, 16-bit, 48 kHz, clamped to [−1, 1] | Byte-swapped on big-endian hosts |

At 48 kHz every bar at 100 BPM is exactly 115,200 samples (2.4 s). Bars are computed as `round(4 × 60/bpm × sr)` samples, so the grid in `bed_meta.json` matches the files to the sample.

## 3. The three stems

1. **Pad.** Each bar plays one chord (three notes) as low-passed saws, an octave below the style root. The cutoff depends on mood: 1800 Hz neutral, 600 Hz somber, 2400 Hz end card. Each note's start phase is drawn from the seeded RNG, so the result is reproducible and not phase-aligned.
2. **Pluck.** Eighth-note arpeggio: chord tones chosen by the RNG, with a 15% seeded rest probability and velocity in 0.8–1.0. This stands in for pizzicato/ukulele/glockenspiel.
3. **Perc.** Brush styles get high-passed noise ticks on beats 2 and 4. Kick styles (`editorial-vox`, `kinetic-type`) also get a pitch-swept sine kick (120→50 Hz) on beats 1 and 3. Velocity jitter is seeded.

Each stem is peak-normalised to −12 dBFS. Then the mood gain is applied (somber −6 dB) and the end-card ramp (−6 → 0 dB over the last two bars). The mixer receives three stems at a known headroom and decides the level.

## 4. Progressions per style ([Recommendation])

| Style | Root | Progression (semitones from root) | Feel |
|---|---|---|---|
| paper-collage-vertical | C4 261.63 Hz | I–V–vi–IV | Warm storybook |
| doodle-handdrawn | D4 293.66 Hz | I–IV–V–I | Simple, bright |
| editorial-vox | A3 220 Hz | i–VI–III–VII | Serious, documentary |
| kinetic-type | B3 246.94 Hz | I–vi–IV–V | Pop, energetic |
| voxel-isometric | E4 329.63 Hz | I–ii(sus)–iii–IV(sus) | Game-like, light |

To change a progression, edit `STYLES` in `compose_bed.py`. That changes every bed of that style, so bump the seed salt (`…|bed|v2`) and record the change in `examleaf-asset-library`.

## 5. Determinism rules

- One `random.Random(seed)` per bed, consumed in a fixed order: bar → pad notes → plucks → percussion. Never draw a random number inside a branch that depends on wall-clock time, file-system order or a dictionary that is not ordered.
- No `time`, no `datetime`, no environment reads inside synthesis.
- The same `(style, bpm, bars, seed, mood)` gives byte-identical WAVs, and the selftest proves it. A changed generator script is a new asset version: record its sha256.
- SFX use `random.Random(f"{seed}:{name}")`. Python's string seeding is stable across processes and is not affected by `PYTHONHASHSEED`.

## 6. Cutting to length

- Beds are rendered in whole bars, so cut points sit on `bar_times_s`. For a scene of D seconds, render `ceil(D / bar_s)` bars and let the mixer fade over the last bar.
- **Never stretch or speed narration to fit the bed.** Re-time visuals or re-cut the bed instead (`examleaf-pacing-controller`: "Prefer re-timing visuals to paid resynthesis"; never auto-speed).
- Mood changes happen on a bar line. The cue sheet decides which bar.

## 7. The chiptune risk and repairs

Report §5.1 [Hypothesis]: synthesised music "can sound 'chiptune' without careful voicing". The levers, in order of cost:

1. **Darken the pad**: lower the neutral cutoff from 1800 to 1200 Hz, or lower the pad gain.
2. **Thin the plucks**: raise the rest probability, or limit plucks to the first and third beats.
3. **Swap the pluck timbre**: replace the sine with a sine plus a quiet second harmonic and a shorter decay, for a softer "glock".
4. **Change preset**: a different progression or root for the scene.
5. **Licensed fallback bed** from `examleaf-asset-library`, with its licence attached.
6. **No bed.** Zero music is always valid, and under explanations it is the default.

Steps 1–4 count against the **two repair attempts** limit. Steps 5–6 are fallbacks, not repairs.

## 8. Richer routes (not default)

- **NumPy synthesis** gives the same recipe faster and allows band-limited oscillators (polyBLEP). Use it only from the approved audio environment, write with `scipy.io.wavfile` or `soundfile`, and keep seeds identical.
- **MIDI + SoundFont** gives better timbres. It needs a SoundFont whose licence is recorded in asset-library, and a pinned synth version. Neither is in the verified evidence.
- **Music MCP models** ([V2] "music studio MCP"): no verified install, permission or pricing evidence (report §6.3). Use them only through `examleaf-mcp-orchestrator` after `examleaf-skills-security` admits the server.
