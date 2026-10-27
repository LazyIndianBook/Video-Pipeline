<!-- Paste into the scene brief (examleaf-anim-brief) for an illustrative segment. Fill every {{field}}. -->
## Audio (mandatory line, edge case #10)

- Segment role: {{segment_role}} (reel_hook / reel_cta / prototype; any other role: none (policy); 15 Oct 2026).
- Music bed: {{"yes: style " + style + ", " + bpm + " BPM, seed " + seed | "none (policy)"}}.
- The bed and SFX are produced by `examleaf-audio-compose`. **Do not write audio code in the scene.** Do not fetch or embed any music or sound file.
- Read beat and bar times only from the cue sheet (`beats[]`). Never hard-code times (report §5.5).
- SFX are placed by the cue sheet (`sfx[]`). The scene must not play audio itself; the compositor mixes.
- Somber beats: cue `{{somber_cue_id}}` switches to the low-passed bed on the next bar line.
- End card: the swell starts at cue `{{endcard_cue_id}}`.
- Loudness is mastered later to −16 LUFS / ≤ −1 dBTP by `examleaf-audio-production-engineer`. Do not normalise in the scene.
