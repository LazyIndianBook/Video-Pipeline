# 06 · Audio: compose, analyse and sync

**Purpose.** How the advanced-animation layer makes music and sound effects in Python, how it analyses audio for timing, how every animation is driven by one canonical cue sheet, which voice path is allowed, and how the final mix is levelled and checked. It turns report §5 into an operating procedure that fits the existing narration sub-pipeline.

**Status.** [PROPOSED]. Nothing here has been run on real narration. Libraries named below (NumPy, SciPy, soundfile, librosa, a SoundFont synthesiser) are **not in the verified evidence set** except the librosa behaviours cited as [N36]–[N43] and [N81]. Pin versions in the pilot and verify every call against the pinned docs.

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V1]–[V5] reference videos (auto-captions, wording approximate), [V4-MP] the paper-collage master prompt (`12_advanced_animations_with_claude/00_reference_videos/master_prompt_paper_collage.md`), [N#] verified web evidence (`12_advanced_animations_with_claude/01_research/SOURCES_and_claims.md`). Project documents are cited by ROOT-relative path. Design judgement is labelled [Recommendation] or [Hypothesis]. Edge cases use the master numbers #1–#65 from report §8; additions are NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

**Owning skills.** `12_advanced_animations_with_claude/03_skills/examleaf-audio-compose/` (beds and SFX), `12_advanced_animations_with_claude/03_skills/examleaf-audio-analysis/` (beat grid, onsets, energy), `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/` (canonical cue sheet). Existing owners that are **not** replaced: `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter` (voice), `examleaf-speech-animation-synchronizer` (timeline, captions), `examleaf-audio-production-engineer` (master), `examleaf-audio-caption-qa` (QA) — see `06_skills_library/SKILLS_PIPELINE_STAGE_MAP.md` rows 13–15.

---

## 0. The ten rules (read this if nothing else)

1. **Narration is the clock.** Scene duration derives from the accepted narration, never the reverse (report §5.5). `DURATION × fps` sets the frame count [N72].
2. **Animations never hard-code times.** They read `cues[].at` from the cue sheet. A reveal lands on, or up to about 0.05 s before, its word ([V4-MP] sync rule).
3. **The cue sheet is a projection of `audio/timeline.json`, not a second source of truth.** If they disagree, the narration timeline wins (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12) [Recommendation].
4. **Regenerated TTS means re-align, rebuild the cue sheet, re-render. Scene code does not change** (#63).
5. **One voice path:** the ExamLeaf TTS adapter with pronunciation and multilingual direction. MCP voice only for exploratory storyboards, never released (report §5.3).
6. **No music under the core explanation** (`02_learning_psychology/palette_and_typography_tokens.json` `background_music_in_core_explanation: false`; `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13). Beds live in hooks, transitions, recaps and CTAs only (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §6.3).
7. **House loudness wins for lessons:** −16 LUFS ± 1 integrated, true peak ≤ −1 dBTP (pass at ≤ −0.9), 48 kHz (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1). [V4-MP]'s −14 LUFS / −1.5 dBFS is not adopted; for Reels it is only tested against −16 LUFS in a controlled A/B (AD-04 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`).
8. **Loudness normalisation is mandatory, never assumed** (#39). Some toolchains do "no normalising, EQ or fades unless you ask" [N20].
9. **Everything is 48 kHz from end to end.** librosa resamples to 22,050 Hz by default; load with `sr=None` [N81] (#35).
10. **Every generated sound is seeded, bar-aligned, hashed and logged** with its licence status.

---

## 1. Reference practice versus ExamLeaf house rules

The reference videos are marketing and entertainment demos. ExamLeaf already has stricter audio rules. Where they differ, the house rule governs.

| Topic | Reference practice | ExamLeaf house rule | Source of the house rule |
|---|---|---|---|
| Who makes music | Opus composes music "using Python code" [V2]; ask explicitly for Python SFX and music [V3] | Python beds allowed for SFX, Reel hook beds, prototypes and fallback; **brand bed and sonic logo composed by a contracted human** (the owned, commissioned sonic logo; same policy in AD-15 addendum, 15 Oct 2026) | `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §7.1 item 7, §6.4 |
| Music under teaching | Bed under the whole piece ([V4-MP] §11) | **Off** during definitions, derivations, numericals, "watch this step" beats | `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13; `02_learning_psychology/INSTRUCTIONS_production_rules.md` G5 |
| Bed level under voice | 15–20 dB under the voice [V4-MP] | Lesson ≈ 20–24 dB under dialogue; Reel ≈ 18–22 dB [Hypothesis, unsourced, test]. *15 Oct 2026: one level, 20–24 dB, for every allowed placement (hooks, transitions, recaps, outros), lessons and Reels (AD-15 addendum)* | `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §5 |
| Final loudness | ≈ −14 LUFS, peaks < −1.5 dBFS [V4-MP] | −16 LUFS ± 1, TP ≤ −1 dBTP, re-measured after mux; Reels: A/B −14 vs −16 before any change (AD-04) | `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1; doc 14 AD-04 |
| Voice | Higgsfield → ElevenLabs v3 "Arthur" [V4-MP]; MCP voice [V2][V3] | ExamLeaf TTS adapter, approved `VoiceIdentity`, lexicon, native review | `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §1–§9 |
| Stings and gags | Boing, pop, tear, thud, chime ([V4-MP] §11) | At most 1–2 stings per lesson, 0–1 per Reel; no laugh effects, no unrelated stings | `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §5; `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13 |
| Licensing | Library song in [V1] ("Mirror Mirror", YouTube Audio Library) | Owned or commissioned only; never platform-library songs in brand content | `11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §6.4 |
| Archive format | Not stated | 48 kHz, 24-bit WAV; voice/music/SFX stems kept separate | `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13; playbook §5 |

**Consequence** [Recommendation]: in a ~10-minute lesson the Python-composed layer is mostly **SFX and short transition beds**. In Reels it can carry the hook (0–3 s) and the CTA. Under the explanation it is muted or absent unless an A/B test (`02_learning_psychology/AB_EXPERIMENTS_and_EVALUATION.md`) shows no comprehension or listening-effort cost.

---

## 2. Why compose in Python at all

**Evidence.**
- [V2]: the music in the demo "was also composed by Opus 5.5 using Python code"; the model "can compose original music and create sound effects".
- [V3]: the harness "might not automatically include audio", so you must "explicitly tell the model to generate the sound effects and background music using Python". [V3] also says that routing to a dedicated music generator is "a massive upgrade because then Opus doesn't have to rely purely on basic Python scripts" — an admission of the ceiling.
- [V1]: the sound effects in all six videos were AI-made.

**What it buys ExamLeaf** [Recommendation]:
1. **Zero marginal cost and no credits.** No MCP call, no ledger reservation (contrast #41–#42).
2. **Determinism.** A seeded generator gives byte-identical WAVs on the same render box, so audio can join the cache key and the double-render hash (#17).
3. **Exact bar alignment.** The beat grid is known analytically, so no beat tracking is needed for our own beds (§4.2).
4. **Ownership.** The output is produced by ExamLeaf code. Whether that is enough for brand use is a legal question; record it as `licence: "examleaf-generated (legal review pending)"` until counsel confirms [Recommendation].

**Limits** [Hypothesis]: synthesised music "can sound chiptune without careful voicing" (report §5.1). Keep a curated, licensed fallback bed for long lessons, or a commissioned composer bed (playbook §6.4), or an evaluated music model behind `12_advanced_animations_with_claude/03_skills/examleaf-mcp-orchestrator/`.

---

## 3. Composition recipe (`examleaf-audio-compose`)

### 3.1 Fixed parameters

| Parameter | Value | Basis |
|---|---|---|
| Sample rate | 48,000 Hz | House master; narration timeline is sample-based at 48 kHz (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12) |
| Bit depth (archive) | 24-bit PCM | Same, §13 |
| Channels | Mono by default [Recommendation] | Voice master is mono; stereo stems only if `examleaf-audio-production-engineer` delivers a stereo mix (verify) |
| Tempo | ≈ 100 BPM for the storybook/doodle styles | [V4-MP] §11 |
| Meter | 4/4 [Recommendation] | Simplest bar maths |
| Video frame rate | 30 fps | Vertical-only decision of 15 Oct 2026 (RD-16 superseded) in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` |

**Choose tempos whose beat is a whole number of frames at 30 fps** [Recommendation]. Frames per beat = 1800 / BPM. Checked locally with exact fractions:

| BPM | Frames per beat | Frames per 4/4 bar | Samples per bar at 48 kHz | Use |
|---:|---:|---:|---:|---|
| 72 | 25 | 100 | 160,000 | Calm recap |
| 75 | 24 | 96 | 153,600 | Calm recap |
| 90 | 20 | 80 | 128,000 | Editorial |
| **100** | **18** | **72** | **115,200** | **Default** ([V4-MP]) |
| 120 | 15 | 60 | 96,000 | Energetic Reel hook |

With these tempos every beat and bar boundary falls exactly on a frame and a sample. No rounding drift accumulates over a 10-minute timeline.

### 3.2 Building blocks

All are standard DSP. They are design choices, not sourced recipes [Recommendation].

| Block | Purpose | Minimal form |
|---|---|---|
| Oscillators | Tones | sine; triangle; band-limited saw/square by additive partials (avoid naive saw aliasing) |
| ADSR envelope | Shape each note | attack, decay, sustain level, release in seconds |
| One-pole low-pass | Mood control, softening | `y += k·(x − y)`, `k = 1 − e^(−2π·fc/sr)` |
| Noise + envelope | Percussion, paper swish, tear | seeded white noise, band-limited by the filter |
| Plucked string (Karplus–Strong) | Ukulele/pizzicato-like plucks | delay line + averaging filter |
| Mixer and limiter | Sum stems safely | sum, then soft clip or peak normalise below 0 dBFS before mastering |

**Richer timbres option.** Write MIDI and render it with a SoundFont synthesiser (report §5.1). The SoundFont is a third-party asset: record its licence in the asset ledger (`examleaf-asset-library`) and pin its hash. The synthesiser and its command line are **not verified** here; verify in the pilot.

### 3.3 Reference sketch (stdlib only, run locally on 14 Oct 2026)

The sketch below uses only the Python standard library (`wave`, `math`, `random`, `struct`, `hashlib`). It was executed twice on the build machine (with a one-pole low-pass added for the somber variant): identical SHA-256 both times, and 2 bars at 100 BPM = 230,400 samples as expected. It is a **teaching sketch** for the skill, not production code; production may use NumPy for speed [Recommendation].

```python
"""Seeded, bar-aligned pluck bed: stdlib only (wave, math, random, hashlib)."""
import math, random, struct, wave

SR, BPM, BEATS_PER_BAR = 48_000, 100, 4
BEAT_S = 60 / BPM                                   # 0.6 s
BAR_SAMPLES = round(SR * BEAT_S * BEATS_PER_BAR)    # 115,200

def adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    env = []
    for i in range(n):
        if i < a: env.append(i / max(a, 1))
        elif i < a + d: env.append(1 - (1 - s) * (i - a) / max(d, 1))
        elif i < n - r: env.append(s)
        else: env.append(s * max(n - i, 0) / max(r, 1))
    return env

def note(freq, dur_s, amp=0.2):
    n = int(dur_s * SR)
    env = adsr(n, 0.005, 0.08, 0.3, 0.12)
    return [amp * env[i] * math.sin(2 * math.pi * freq * i / SR) for i in range(n)]

def bed(bars, seed, scale=(261.63, 293.66, 329.63, 392.00, 440.00)):
    rng = random.Random(seed)                       # never the global RNG
    buf = [0.0] * (bars * BAR_SAMPLES)
    for beat in range(bars * BEATS_PER_BAR):
        start = round(beat * BEAT_S * SR)
        for i, v in enumerate(note(rng.choice(scale), BEAT_S * 0.9)):
            if start + i < len(buf): buf[start + i] += v
    return buf

def write_wav(path, x):                             # 24-bit mono PCM
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(3); w.setframerate(SR)
        frames = bytearray()
        for v in x:
            frames += struct.pack("<i", int(max(-1.0, min(1.0, v)) * 8_388_607))[:3]
        w.writeframes(bytes(frames))

if __name__ == "__main__":
    a, b = bed(2, seed=7), bed(2, seed=7)
    assert a == b and len(a) == 2 * BAR_SAMPLES == 230_400   # seeded + bar-exact
    assert bed(2, seed=8) != a
    write_wav("bed_test.wav", a)
```

### 3.4 Procedure for one bed

1. **Read the brief.** From the scene brief (`12_advanced_animations_with_claude/03_skills/examleaf-anim-brief/`) take: style ID, mood segments, the scenes that allow music (hook, transition, recap, CTA), and the total duration from the cue sheet.
2. **Pick tempo and key** from the style tokens (`12_advanced_animations_with_claude/05_style_guides/style_tokens.json`). Default 100 BPM, 4/4.
3. **Compute bars:** `bars = ceil(duration_s / bar_s) + 1` (one extra bar for tails). Render stems at whole-bar length.
4. **Render stems separately:** pad, plucks, bass, light percussion. Each stem is loopable at bar boundaries and seeded with the seed from examleaf-audio-compose Execution step 3, recorded in bed_meta.json (15 Oct 2026; replaces the earlier `seed = hash(scene_id, stem, bed_version)`, which differed from the skill).
5. **Apply mood automation** from the cue sheet's `mood` segments (§5.2): low-pass and −6 to −10 dB for somber beats; a gentle swell on the end card ([V4-MP] §11). The dB values are a [Hypothesis] to tune by ear.
6. **Cut on bar lines only.** Where a scene ends mid-bar, fade over the last beat rather than truncating a note [Recommendation].
7. **Write 48 kHz/24-bit mono WAV stems** and a `bed.json` (§3.6). Hash every file.
8. **Do not master the bed.** Mastering happens once, on the final mix, in `examleaf-audio-production-engineer` (§7).

### 3.5 SFX palette

Short one-shots placed by the cue sheet's `sfx[]` array. Each is seeded and rendered to its own WAV.

| SFX | Use | Recipe [Recommendation] | Source of the idea |
|---|---|---|---|
| Paper swish | Sheet transition | band-passed noise, 150–300 ms, fast attack, falling filter sweep | [V4-MP] §11 |
| Tap | Ransom letter landing | 10–20 ms click + short damped sine | [V4-MP] §11 |
| Cartoon pop | Cutout appears | sine with fast downward pitch sweep, 60–120 ms | [V4-MP] §11 |
| Boing | Hop | sine with vibrato-like pitch wobble, 300–500 ms | [V4-MP] §11 |
| Paper tear | Tear gag | noise bursts with random gaps (seeded), 300–600 ms | [V4-MP] §11 |
| Thud | Drop | low sine + noise, steep decay | [V4-MP] §11 |
| Sparkle chime | Magic moment / correct answer | 2–3 high partials, long release | [V4-MP] §11; playbook §6.3 ("correct-answer sting allowed" in Reel body) |
| Pencil scratch | Doodle draw-on | high-passed noise modulated at stroke speed | [V2] doodle style [Recommendation] |
| Electric hum | Circuits | 50 Hz-family partials, very low level | Report §5.1 STEM one-shots |
| Bubbling | Reactions | short seeded noise blips with rising pitch | Report §5.1 |
| Click-snap | Bond forming | 2 clicks 30 ms apart | Report §5.1 |

**SFX rules.**
- Subtle by default ([V4-MP] §11: "kept subtle"); bigger booms "only for real drama".
- **No SFX in the voice track** (playbook Step 5: "no sound-effect tags in the voice track, because SFX belong in the edit").
- **A sound must not imply wrong science** [Recommendation]: no "spark" on a safe low-voltage circuit; no "explosion" for an ordinary reaction; no hum that suggests mains AC when the lesson uses a DC cell. Science review signs off SFX on data-bound scenes.
- Respect the sting budget: 1–2 per lesson, 0–1 per Reel (playbook §5).

### 3.6 `bed.json` metadata (minimum)

```json
{
  "bed_id": "reel-iv-graph-hook-v1",
  "generator": "examleaf-audio-compose",
  "generator_version": "<pin>",
  "bpm": 100, "meter": "4/4", "bars": 3, "beat_offset_s": 0.0,
  "sample_rate": 48000, "bit_depth": 24, "channels": 1,
  "seed": 7,
  "stems": [{"name": "pluck", "path": "audio/beds/pluck.wav", "sha256": "<64 hex>"}],
  "mood_segments": [{"from_s": 0.0, "to_s": 4.8, "mood": "curious"}],
  "licence": "examleaf-generated (legal review pending)",
  "contains_samples": false
}
```

If any third-party sample or SoundFont is used, `contains_samples: true` and each sample gets an `examleaf-asset-library` record with licence and attribution (`07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §3.8 `AssetManifest`).

### 3.7 Fallback bed

When a generated bed sounds cheap or a lesson needs more than a few seconds of music:
1. Use the commissioned ExamLeaf bed (playbook §6.4 deliverables: 48 kHz/24-bit WAV, stems, loudness-matched versions, written buyout or exclusive licence).
2. Otherwise a curated licensed bed, logged with the playbook §6.5 fields (`asset_id | title | composer | licence type | territory | term | platforms | paid-ads allowed | contract file | date | stems location | used in`).
3. A music model via MCP only through `12_advanced_animations_with_claude/03_skills/examleaf-mcp-orchestrator/` with an estimate, a ledger reservation and a hard cap (#41, #42). No verified music-MCP install or pricing exists (report §6.3, §11 item 6).

---

## 4. Audio analysis for sync (`examleaf-audio-analysis`)

### 4.1 What ExamLeaf actually needs

[V1] built a custom analyser (beats, notes, instruments, dynamics, lyrics, song meaning) because "the AI cannot hear the song". It used about 5 GB RAM with a 6 GB VRAM GPU [V1]. ExamLeaf's lessons are narration-led, so it needs far less (report §5.2):

| Need | Source | Analysis required? |
|---|---|---|
| (a) **Beat grid** for Reels with a music bed | Own Python bed: analytic (`bpm`, `beat_offset_s`) | **No** for own beds; librosa only for licensed or external beds |
| (b) **Word timestamps** | TTS provider timestamps or forced alignment → `audio/alignment.json` → `audio/timeline.json` (`examleaf-alignment-localize`, `examleaf-speech-animation-synchronizer`) | Already in the narration pipeline |
| (c) **Onset and energy envelopes** | Narration master and beds | Simple RMS per video frame; onset strength only for external music |

A [V1]-style full analyser is relevant only for a music-video-style Reel built around an external track, which is outside the current Reel formats (`01_business_model/REEL_BACKLOG_36.md`).

### 4.2 Beat grid from our own bed (no analysis)

```
beat_time[k] = beat_offset_s + k * 60 / bpm        k = 0, 1, 2, ...
beat_frame[k] = round_half_up(beat_time[k] * fps)  exact when 1800/bpm is an integer (§3.1)
```

Write it straight into the cue sheet's `beats[]`. This avoids every librosa trap below.

### 4.3 librosa for external audio: the traps and their fixes

Only for licensed or external tracks. Behaviours verified against librosa 0.11.0 docs [N36]–[N43], [N81]; pin the version and re-verify before use.

| # | Trap | Symptom | Fix | Source |
|---|---|---|---|---|
| #35 | `librosa.load` mixes to mono and resamples to 22,050 Hz by default | Cue times computed at one rate drift against 48 kHz video | `librosa.load(path, sr=None)`; carry the returned `sr` everywhere; never mix rates | [N81] |
| #31 | Stereo input with `sparse=True` | Error | Downmix first, or pass `sparse=False` | [N37] |
| #31 (cont.) | `sparse=False` output | Dense boolean per-frame array, not beat indices | Convert explicitly; prefer mono + default sparse | [N43] |
| #32 | Tempo returned as an ndarray even for mono input | Type errors downstream | `tempo = float(np.atleast_1d(tempo)[0])` | [N38] |
| #33 | Beats in frames by default | Sync off by a large factor | `units='time'` | [N39] |
| #34 | Silent or beatless audio | 0 BPM, empty beat list | Guard; fall back to a narration-derived grid (§4.5) | [N41] |
| #36 | Neither `y` nor `onset_envelope`, or invalid `units` | `ParameterError` | Validate inputs before the call | [N40] |
| #37 | `start_bpm` with a prior | `start_bpm` ignored | Use one or the other; log which | [N36] |
| #38 | Time-varying `bpm` array | Shape error | `bpm` shape must match `onset_envelope` | [N42] |

**Guarded call (parameter names from [N36]–[N43], [N81]; verify against the pinned version):**

```python
import librosa, numpy as np

y, sr = librosa.load(path, sr=None)                 # keep native rate (#35)
if y.size == 0 or not np.any(np.abs(y) > 1e-4):     # silence guard (#34)
    beats = []
else:
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units="time")  # (#33)
    tempo = float(np.atleast_1d(tempo)[0])          # (#32)
    beats = [float(b) for b in np.atleast_1d(beats)]
if len(beats) < 2:
    beats = narration_grid()                        # fallback (§4.5)
```

The silence threshold `1e-4` is a [Hypothesis]; tune it on real beds.

### 4.4 Onset and energy without extra libraries

For ducking, SFX placement and QA, an RMS value per video frame is enough [Recommendation]:

```
samples_per_frame = 48000 / 30 = 1600
rms[f] = sqrt(mean(x[f*1600 : (f+1)*1600] ** 2))
```

This needs no librosa and is frame-exact. Use librosa onset strength only for external music; its API is not in the verified set (verify).

### 4.5 Fallback grid when there are no beats

If an external bed is beatless (#34) or a Reel has no bed, build a **narration grid**: sentence starts from `timeline.json` clips, plus phrase boundaries where pauses ≥ 0.3 s (the lower bound of the ordinary phrase pause, `02_learning_psychology/INSTRUCTIONS_production_rules.md` G3). Decorative motion can snap to this grid.

### 4.6 Output: `analysis.json`

`source_path`, `source_sha256`, `sr` (as loaded), `method` (`analytic-bed` · `librosa-beat-track` · `narration-grid`), `library_version`, `tempo_bpm` (float or null), `beats_s[]`, `rms_per_frame[]` (fps stated), `warnings[]` (empty-beat fallback, resample, downmix).

---

## 5. The canonical cue sheet (`examleaf-cue-sheet`)

### 5.1 Canonical example (report §5.5, verbatim)

```json
{"scene_id":"phy-10-03-s04","fps":30,"duration":7.4,
 "words":[{"w":"refraction","t0":1.12,"t1":1.71}],
 "beats":[0.0,0.6,1.2],
 "cues":[{"id":"label_n1","at":1.07,"kind":"reveal"}],
 "sfx":[{"file":"pop.wav","at":1.07,"gain_db":-12}]}
```

Note that the reveal (`1.07`) lands 0.05 s before the word (`1.12`), and the beats are 0.6 s apart (100 BPM).

**The schema governs.** The machine contract is `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`, with a full example in `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.example.json` and the loader rules in `12_advanced_animations_with_claude/04_harness_contract/contract.md`. If this document and the schema disagree, the schema wins and this document is corrected. The report's example is the *minimum*; the schema (version 1.0) additionally **requires** `schema_version`, `language`, `narration_audio_sha256` and `script_sha256`, allows `alignment_source` and `meta`, and rejects unknown top-level fields. Validate every sheet with `python3 12_advanced_animations_with_claude/04_harness_contract/validate_cue_sheet.py SHEET.json --production` (stdlib-only; exit 0 valid, 1 invalid). Two schema-valid worked sheets are in `12_advanced_animations_with_claude/02_documentation/13_END_TO_END_WALKTHROUGH.md` §A.7 and §B.5.

### 5.2 Field semantics (schema 1.0)

| Field | Meaning | Rule |
|---|---|---|
| `schema_version` | Cue-sheet format version | `"1.0"` |
| `scene_id` | Scene identifier | Schema pattern `^[a-z0-9][a-z0-9_-]{2,63}$`; use the same ID as the `SceneSpec` (whose pattern is `^[a-z][a-z0-9_-]{2,70}$`), so pick IDs that satisfy both |
| `fps` | Intended render fps | 30 (vertical-only decision of 15 Oct 2026, RD-16 superseded); if the renderer's fps differs, the renderer wins and cue times are never rescaled (contract §7) |
| `duration` | Scene length in seconds | Becomes `window.DURATION`; frame count `N = round(duration × fps)`; the builder makes `duration × fps` an integer (§5.3 step 2; `SceneSpec` whole-frame rule) |
| `language` | Primary narration language | BCP-47 style (`en-IN`, `hi-IN`, `as-IN`); code-switched words carry their own `lang` |
| `alignment_source` | How word times were made | `forced_alignment` · `tts_provider` · `manual` (production); `synthetic_even_spacing` · `example` are rejected by `--production` |
| `narration_audio_sha256`, `script_sha256` | Hashes of the aligned audio and the approved script | Staleness detection (#63); `null` only before narration exists |
| `words[]` | `{w, t0, t1, occurrence?, lang?}` | From the accepted alignment, scene-local seconds; spoken order; non-overlapping |
| `beats[]` | Beat times in seconds | Strictly increasing; may be empty (silent or beatless audio, or no bed) [N41] |
| `cues[]` | `{id, at, kind, element_id?, occurrence?, word_index?, until?}` | `kind` ∈ `reveal` · `emphasis` · `transition` · `hold` · `marker`; `word_index` keys the reveal-lead check; `until` ends a `hold` (e.g. equation: narration end + 0.5 s) |
| `sfx[]` | `{file, at, gain_db}` | Relative path to a 48 kHz WAV/FLAC; `gain_db` between −60 and 0 (no positive gain) |
| `meta` | Free-form provenance | Not read by scene code; carries mood segments, answer-protection notes, warnings |

**Mapping from the narration timeline.** Alignment `method` → `alignment_source`: `provider-timestamps` → `tts_provider`; `forced-aligner` → `forced_alignment`; `human` → `manual`; `synthetic-fixture` → never production. Narration cue `action` → cue `kind` [Recommendation]: `show` → `reveal`; `highlight` → `emphasis`; `transform` → `transition`; `hide` → `transition` (or `marker`); `reveal-answer` → `reveal` or `emphasis`, with the protection recorded in `meta` (§5.3 step 6).

### 5.3 Building the cue sheet (numbered procedure)

Inputs: `audio/timeline.json` (narration; sample-exact events, clips, pauses), `audio/alignment.json`, the narration `Cue` list (phrase, occurrence, edge, action, element ID; `07_end_to_end_pipeline_instructions/12_GLOSSARY_and_DATA_CONTRACTS.md` §4.3), `analysis.json` or `bed.json`, and the brief's SFX plan.

1. **Find the scene window** in the lesson timeline: `scene_start_sample`, `scene_end_sample` (from the `SceneSpec` cue span after re-timing to measured audio, `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S11).
2. **Compute duration** = `(scene_end_sample − scene_start_sample) / 48000`, then round **up** to a whole frame: `frames = ceil(duration × fps)`, `duration = frames / fps`. Never round down; that would cut the last word.
3. **Copy words** that fall in the window, converting to scene-local seconds: `t = (sample − scene_start_sample) / 48000`.
4. **Resolve each semantic cue** from the narration events (`events[]` already carry `sample` and `frame`, computed once with `frame = round_half_up(sample × fps_num / (48,000 × fps_den))`, `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12). Use that frame; do not recompute from floats.
5. **Apply the lead** ([V4-MP]: "on, or about 0.05 s before"): `at = word.t0 − 0.05`, the template default (`12_advanced_animations_with_claude/04_harness_contract/contract.md` §8). Any `at` in `[t0 − 0.05, t0]` is valid; the validator rejects `at > t0` and warns when a reveal is more than 0.10 s early. Times stay continuous seconds — do not snap them to frames; the harness captures frame `i` at `i / fps` (contract §7).
6. **Protect answers.** The schema has no answer kind, so the builder takes every narration event with action `reveal-answer`, finds the cues whose `element_id` matches it, and checks that each `at` is after the question's protected pause ends. Answer reveals use offset 0 — never a negative lead — as `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/` specifies. The narration composer already raises "Premature answer"; the builder repeats the check because a lead could otherwise move a reveal into the protected window. Record the pair in `meta` (e.g. `meta.answer_protection`).
7. **Add beats** from §4 (scene-local).
8. **Place decorative cues** (idle sways, doodle boils, paper-sheet transitions). These may snap to the nearest beat within ±0.1 s [Hypothesis]; semantic cues never move off their word.
9. **Place SFX** at their cue's `at`; transition swishes start with the sheet. Paper sheets start about 0.3 s after the previous line's last word ([V4-MP] §9).
10. **Validate** (§5.6) and write `anim/<scene_id>/cue_sheet.json` with the source hashes.

### 5.4 Relationship to existing timing artefacts

| Artefact | Owner | Role |
|---|---|---|
| `audio/alignment.json` | NA `speech-animation-synchronizer` via `alignment-localize` | Word timings per segment |
| `audio/timeline.json` | NA `speech-animation-synchronizer` | Lesson-wide, sample-exact events, pauses, captions — **source of truth** |
| `scenes/scene-spec.json` cues | VE `storyboard-route`, re-timed at S11 | Caption-level cue roles (`explain`, `question`, …) |
| `anim/<scene_id>/cue_sheet.json` | New `examleaf-cue-sheet` | **Per-scene projection** for animation code; adds beats, SFX, decorative cues |

`examleaf-cue-sheet` extends `examleaf-speech-animation-synchronizer` and `examleaf-alignment-localize` (report §10 item 11). It must not re-author captions or alignment (caption ownership, `06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 9).

### 5.5 Re-align on TTS regeneration (#63)

When any narration segment is regenerated (pronunciation fix, wording change, voice change):
1. The narration pipeline re-runs ASR, alignment and the timeline for the affected segments (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S15 table: "Spoken text of one segment → that segment's audio, ASR, alignment, timeline, captions, re-timed scenes, render").
2. `examleaf-cue-sheet` detects staleness: the sheet's `narration_audio_sha256` (or `script_sha256`) no longer matches the accepted audio (or approved script).
3. Rebuild the cue sheets of every scene whose window overlaps a changed segment.
4. Re-render those scenes. **Scene code is unchanged**, because it only reads `cues[].at`.
5. Re-run the determinism hash, hold-time and sync checks (`12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md`).
6. GF is invalidated by any audio time change (S15 table); re-approve on the new hash.

A scene that hard-codes a time fails `12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js` before it can be rendered [Recommendation for the linter].

### 5.6 Validation checks

`validate_cue_sheet.py --production` enforces the schema plus the semantic rules JSON Schema cannot express (monotonic, non-overlapping words; cues within duration; reveal lead). The builder adds:
1. `duration × fps` is an integer [N72].
2. Every semantic cue keyed by `word_index` lies in `[t0 − 0.05, t0]` of its word [V4-MP].
3. No answer reveal inside a protected pause (§5.3 step 6).
4. `beats[]` non-empty where a bed plays, or `meta` records the fallback (#34).
5. Every `sfx[].file` exists, is 48 kHz, and its hash is in the asset ledger.
6. `narration_audio_sha256` and `script_sha256` match the current accepted audio and approved script (#63).
7. `alignment_source` is a production value.

---

## 6. Voice path

| Allowed | Not allowed in production |
|---|---|
| `examleaf-voice-synthesis` → `examleaf-tts-provider-adapter` with an approved `VoiceIdentity` and rights record | Higgsfield "Arthur" or any MCP voice ([V4-MP] step 4) |
| `examleaf-stem-pronunciation` lexicon; `examleaf-voice-acting-director`; `examleaf-pacing-controller` | Voice chosen by the animation agent ([V3] lets the model pick a voice) |
| `examleaf-multilingual-director` before voice direction for each locale; native-language review | Raw machine translation for Hindi/Hinglish (playbook §7.1 item 3) |
| Keys only in the environment or a user config outside the repo ([N19] pattern) | Keys in prompts or the project (#40) |

**Why** (report §5.3): one place keeps persona, pronunciation, Hinglish/Hindi direction and cost logging. MCP voice is acceptable **only** for exploratory storyboards, and such audio must be tagged `exploratory_not_for_release` and never enter `audio/accepted/`.

**Script drift guard** [Hypothesis → check]: diff the text sent to TTS against the GA-approved script (report §6.4). A mismatch is a blocker. The narration compiler already expands `{{tokens}}` from the lexicon; compare the expanded canonical spoken text, not the template.

**Language gates.** Launch locale is en-IN only (RD-26). Assamese and Hindi need a successful model-specific API request plus native review before any production (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §18). Never substitute Bengali pronunciation for Assamese.

---

## 7. Mixing and loudness

### 7.1 Targets

| Quantity | Target | Basis |
|---|---|---|
| Integrated loudness | −16 LUFS ± 1 | House (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §2.1) |
| True peak | ≤ −1 dBTP (pass at ≤ −0.9) | Same |
| Archive | 48 kHz, 24-bit WAV, stems kept | `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13; playbook §5 |
| Bed under voice (lesson segments that allow it) | ≈ 20–24 dB below dialogue | Playbook §5 [Hypothesis] |
| Bed under voice (Reel hook/CTA) | ~~≈ 18–22 dB~~ ≈ 20–24 dB below dialogue (unified 15 Oct 2026, AD-15 addendum) | Playbook §5 [Hypothesis] |
| Reference-video values, **not adopted** | −14 LUFS, peaks < −1.5 dBFS; music 15–20 dB under voice | [V4-MP] §11. `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (`audio.loudness_conflict`, `audio.music_under_voice_db: [15, 20]`) and `import_clip_notes.md` §6.3 still list these as unresolved; this document resolves them per AD-04 and the playbook, and the tokens file should be updated to match. **Done 15 Oct 2026:** tokens now use `audio.loudness` (−1.5 dBFS recorded as sample peak) and `audio.music_policy` (20–24 dB); §6.3 points to them |

Platform normalisation targets for YouTube, Shorts and Reels are unverified (playbook Step 11). Keep −16 LUFS until measured.

### 7.2 Where music may play

Use the playbook usage map (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` §6.3): bed under the lesson cold open's first line (ducked), 2–4 s swells at chapter transitions, recap/outro, Reel hook, Reel end. **Muted** during teaching beats. The cue sheet's `mood[]` marks these segments; `examleaf-audio-compose` refuses to render music into a segment tagged `core_explanation` [Recommendation].

### 7.3 Ducking, deterministically

The playbook proposes sidechain ducking with fast attack, a release of a few hundred ms and 8–12 dB gain reduction [Hypothesis]. A signal-driven compressor adds variance. Because speech intervals are known exactly from `timeline.json` clips, apply ducking as **gain automation computed from the timeline** [Recommendation]:

1. For each clip `[start_sample, end_sample]`, set bed gain to `−duck_db` from `start − attack` to `end + release`.
2. Use linear ramps of `attack` (≈ 10 ms) and `release` (≈ 300 ms) [Hypothesis].
3. Between phrases the bed may rise to about 12 dB below dialogue (playbook §1 item 3) [Hypothesis].
4. The result is reproducible and hashable.

### 7.4 Mix and master order

1. Voice master from the narration pipeline (`audio/master.wav`, already −16 LUFS, mono, 48 kHz).
2. Music stems with automation (§7.3).
3. SFX bus with per-cue `gain_db`.
4. Sum to the programme mix (`examleaf-audio-production-engineer` owns this step).
5. **Normalise the programme mix** (#39). The narration CLI's two-pass `loudnorm=I=-16:TP=-1:LRA=7` with `linear=true`, `-ar 48000 -ac 1 -c:a pcm_s24le` is the tested pattern for the voice master (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13). Applying the same settings to the full mix is a [Recommendation]; the exact final-mix command must be confirmed by the audio owner (verify).
6. **Mux, then re-measure** the delivered file: "the final encoded delivery should be measured again" (same §13). `mux_supplied_audio(..., tolerance_s=0.05)` refuses mismatches ("Conform the timeline; do not silently stretch speech", `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S12).

### 7.5 Sample-rate hygiene

- Providers may return 24 or 44.1 kHz; the narration pipeline resamples polyphase to 48 kHz ("Resampling does not recreate missing high-frequency detail", `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §12).
- Generated beds and SFX are born at 48 kHz.
- Licensed beds delivered at 44.1 kHz are resampled **once**, on import, and the resampled file is hashed (NEW-4 in doc 12). A 44.1 kHz file declared as 48 kHz plays about 8.8 % fast and drifts against every cue [arithmetic: 48,000 / 44,100 ≈ 1.088].
- librosa analysis loads with `sr=None` (#35).

### 7.6 Verification with `examleaf-audio-caption-qa`

Run on the final muxed file (details in `12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` A9–A10):
1. Streams and duration (audio stream present; duration within tolerance).
2. Integrated loudness and true peak (§7.1).
3. Clipping, DC offset, unexpected silence with **protected intervals supplied** (the CLI `qa` cannot pass them; use `qa.signal_report(path, protected_intervals=…)`, `07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §13).
4. Music absent in `core_explanation` segments (RMS of the music stem below a floor in those windows) [Recommendation].
5. Caption timing against the timeline; reveals on or ≤ 0.05 s before their words.
6. Full listen by a human (production QA), including on a phone speaker (playbook QC devices).

---

## 8. Edge cases this document owns

#10 (missing audio, §2), #13 (model can't hear audio, §4), #31–#38 (librosa traps, §4.3), #39 (unnormalised audio, §7.4), #40 (keys, §6), #63 (TTS regenerated, §5.5), and NEW-4 (44.1 vs 48 kHz, §7.5), NEW-9 (music under core explanation, §7.2), NEW-10 (ducking variance, §7.3), NEW-11 (SFX implying wrong science, §3.5). Full rows: `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

---

## 9. Hand-offs and files

Lesson-folder paths: cue sheets `anim/<scene_id>/cue_sheet.json`; beds `audio/beds/<bed_id>/` + `bed.json`; SFX `audio/sfx/`; analysis `audio/analysis/`; mix `audio/mix/programme.wav` + `mix_qa.json` (owned by `examleaf-audio-production-engineer`); cost lines in `costs.json`. The full hand-off table is in `12_advanced_animations_with_claude/02_documentation/11_INTEGRATION_with_ExamLeaf_pipeline.md` §3; a worked bed and cue sheet in `12_advanced_animations_with_claude/02_documentation/13_END_TO_END_WALKTHROUGH.md` §A.7–§A.9.

---

## 10. Open questions (verify before relying on them)

1. Library versions: NumPy, SciPy/soundfile, librosa (0.11.0 docs were verified, not a pinned install), any SoundFont synthesiser — pin and test in the pilot.
2. Whether Python-generated music satisfies the playbook's "composed by a person ExamLeaf contracts" rule for brand use — product owner decision; until then Python beds are for SFX, Reel hooks and prototypes.
3. Final-mix normalisation command and whether the delivery mix stays mono — confirm with the audio owner.
4. Bed levels and ducking values — run the A/B test in `02_learning_psychology/AB_EXPERIMENTS_and_EVALUATION.md` style before adopting.
5. Platform loudness normalisation for Reels and Shorts — measure an upload.
6. Legal status of generated audio for brand and paid-ads use — counsel.
