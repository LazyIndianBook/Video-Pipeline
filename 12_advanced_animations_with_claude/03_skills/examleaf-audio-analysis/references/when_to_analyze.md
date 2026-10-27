# When to analyse audio, and how much

## 1. What [V1] did, and why ExamLeaf does less

[V1] (Devarf) made six music videos from one 79-second rap clip. Because "the AI cannot hear the song", he first had Opus at high effort build a **custom audio-analysis tool**. It extracted:
- beats;
- notes;
- instruments;
- dynamics;
- lyrics;
- a plain-language note on the song's meaning or story.

It used about 5 GB of RAM with a 6 GB VRAM GPU, and he suggests asking Claude to build one sized to your hardware. The analysis was needed because the video's *whole structure* followed the song: dance on beats, story on lyrics.

ExamLeaf inverts that. **The narration drives the timeline; music is optional and secondary.** Report §5.2 [Recommendation] lists what ExamLeaf actually needs:
- (a) a **beat grid** for Reels with music beds;
- (b) **word timestamps** for narration sync, from the TTS provider's alignment or the existing `examleaf-alignment-localize` forced alignment, not from this skill;
- (c) **onset and energy envelopes** for SFX placement and ducking.

Lyrics, instruments and "meaning" have no use: ExamLeaf beds are instrumental, and they are off under teaching (AD-15).

## 2. Decision tree

```text
Is there music in this segment?
├─ no  → do nothing (the cue sheet gets beats: [] or a narration grid if a Reel needs cut points)
└─ yes → where did the bed come from?
        ├─ examleaf-audio-compose → beat_grid.py --bed-meta (exact grid, no librosa)
        ├─ licensed / asset-library → licence recorded?
        │      ├─ no  → stop: unknown rights stay quarantined
        │      └─ yes → beat_grid.py --audio (guarded librosa) → ear spot-check (Reels)
        └─ MCP music model → only via examleaf-mcp-orchestrator; then treat as licensed audio
```

## 3. Why not just analyse everything?

- **Exactness.** An in-house bed has a mathematically exact grid in `bed_meta.json`. Detecting it again can only add error: half-time, double-time or phase drift.
- **Dependencies.** librosa, numpy and scipy are heavy. Keeping them off the default path means the common case (an in-house bed) runs on the stdlib box.
- **Cost of drift.** Every analysis is a new input hash. Re-running detection on unchanged audio produces cue sheets that differ by milliseconds, which forces re-renders and re-approval for nothing.

## 4. Onsets and energy: when they matter

- **SFX placement on a licensed bed.** Snap a `pop` to the nearest onset within one frame of its cue, only when the cue is decorative. A narration-locked reveal stays on its word ([V4-MP] sync rule beats the music).
- **Ducking hints.** `energy.rms` shows loud bed passages that may mask speech. The mixer decides; this skill only reports.
- **Reel cut points.** `examleaf-vertical-adapt` may move a *transition* (not a reveal) to the nearest beat within its tolerance.

## 5. What "hearing" means for the authoring agent (#13)

The scene-code agent never receives audio. It receives the cue sheet: words, beats, cues and SFX in seconds. The brief tells it to read `beats[]` from the cue sheet and to treat an empty list as "no music sync". That is the whole interface. It replaces [V1]'s "analysis JSON so the model can hear" with a narrower, validated contract.

## 6. Narration-grid fallback in practice (#34)

- **When:** a silent clip, a speech-only Reel, or a beatless ambient bed.
- **What:** phrase onsets: the first word, plus every word that follows a pause ≥ 0.12 s ([Recommendation]; tune per language, since Hindi and Assamese phrasing differs).
- **Use:** Reel transitions land on phrase starts. That respects the [V4-MP] rule "start each incoming sheet about 0.3 s after the previous line's last word", which the cue sheet applies via an `edge: end` anchor with `offset_s: 0.3`.
- **Never:** invent a fixed tempo grid ("assume 120 BPM") when beats are missing. librosa's own default `start_bpm` is 120 [N36]; using it as a fact would be fabrication.
