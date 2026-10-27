# Reel sub-range recipe: re-seek and beat re-time

**Basis:** report §9 item 10 [Recommendation]: "Because scenes are time-pure, a reel can re-seek sub-ranges, re-time them to a beat grid (librosa) and add a hook card." Scenes are pure functions of time [N61] (contested) and are rendered by seeking [N18][N72]. The procedure: `07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` and `examleaf-reel-repurpose`.

## 1. What a Reel may and may not reuse

| May reuse | Must not |
|---|---|
| Accepted narration segments that stand alone (traceable hashes) | New or changed spoken wording without the narration pipeline and academic approval (hook line, shortened payoff, CTA line = new script) |
| Lesson scene code, re-seeked over a time window | Cropping a 16:9 render (ShortSpec rejects crop strategy) |
| Fixtures, assets, style | A window whose dropped cues leave the Reel non-standalone ("Produce fewer useful Shorts rather than cutting arbitrary segments") |
| A music bed; it is optional in Reels, licensed or in-house only | Time-stretching narration to hit beats (pacing-controller: never auto-speed) |

## 2. Re-seek mapping

- The Reel window is `[START, END)` in scene time. The Reel's local time is `t_reel ∈ [0, END − START)`.
- The scene is driven with `seek(START + t_reel)`. The composition (`examleaf-web-composition` / `examleaf-motion-harness`) owns this offset: the Reel's clip sets the scene's time origin, and the scene code is unchanged. Use the chosen harness's clip time-offset mechanism as documented in `04_harness_contract/contract.md`. If the contract has none, record a harness gap for `examleaf-motion-harness`; never hack `window.DURATION` inside the scene.
- The Reel cue sheet carries **Reel-local** times (step 3), so overlays added at Reel level (hook card, CTA) use the same clock.

## 3. Window the cue sheet

```sh
python3 12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/scripts/build_cue_sheet.py \
    --spec jobs/phy-10-03-s04/cue_spec.json --out jobs/reel-phy-10-03-a/cue_sheet.json --window 1.25 9.80
```

- Words, beats, cues and SFX inside the window are shifted by −START. The duration is snapped up to whole frames [N72].
- A boundary inside a word is **blocked**. Move the window to a word gap; the alignment shows the gaps.
- `cue_sheet.provenance.json` → `dropped_cues` lists what fell outside. Review it with reel-repurpose for standalone sense.

## 4. Beat re-time (decorative cuts only)

If the Reel has a bed:
1. **Get its grid.** For an in-house bed, `beat_grid.py --bed-meta`. For a licensed bed, `beat_grid.py --audio` with the guarded librosa path (`examleaf-audio-analysis`).
2. **Place the bed** in the Reel spec. Set `beats.offset_s` so the bed's t = 0 sits at Reel t = 0. When building from the lesson spec with `--window`, that is `offset_s = START`, because beats are filtered in scene time and then shifted.
3. **Snap decorative cues** by adding to the spec:
   ```json
   "snap": {"kinds": ["transition"], "tol_s": 0.1}
   ```
   Each `transition` cue moves to the nearest beat within ±0.1 s ([Recommendation], 3 frames at 30 fps). SFX tied to it move with it. Each move is recorded in `provenance.snapped`.
4. **Never snap** `reveal`, `highlight`, `show` or `reveal-answer`. The builder blocks it: "narration-locked cue kinds … never snap to beats". The [V4-MP] sync rule (reveal on, or about 0.05 s before, the word) beats the music.
5. If no beat is within tolerance, the transition stays where the narration put it (about 0.3 s after the previous line's last word, [V4-MP] §9). Music sync is a bonus, never a constraint.
6. **No beats** (silent or speech-only Reel): the analysis falls back to the narration phrase grid (#34). Transitions then already sit on phrase starts.

## 5. Audio for the Reel

- **Narration:** the accepted segment audio for `[START, END)`. Cut only at word gaps (the same gaps the window used). Re-master the whole Reel mix to −16 LUFS ±1, ≤ −1 dBTP (`examleaf-audio-production-engineer`) and re-measure after mux (anim-qa Q15).
- **Bed:** from `examleaf-audio-compose` (cut on bar lines, end-card swell) or a licensed bed. It sits 20–24 dB under the voice (AD-15 addendum, 15 Oct 2026; [V4-MP] said 15–20 dB), and is "optional and never necessary to make the explanation work" (Shorts procedure).

## 6. Layout for the Reel

Usually unchanged, because lesson scenes are already vertical (AD-07). Recompute `zones.json` only if the Reel targets a single platform (`--platform <name>`). The hook card and CTA use the TITLE and CAPTION zones; text comes from the approved Reel script.

## 7. QA and approval

Re-run on the Reel:
- the anim-qa checks (determinism of the Reel render, safe zone, holds, which are critical after windowing because headlines can get truncated, reveal sync, flash, which matters across scene joins, text diff, loudness);
- visual-qa and audio-caption-qa;
- the Reel's own GS approval (stage map #19: "stages 15–18 again for the Short").

## 8. Worked example

Lesson scene `phy-10-03-s04` (7.4 s). The Reel takes 1.25–6.95 s (5.7 s → 171 frames):
- the cue `label_n1` at 1.07 is **dropped**, because it is before the window. Its label is not shown in the Reel, so check that the remaining narration does not refer to "this label";
- the cue `ray_bend` at 2.31 becomes **1.06** Reel-local;
- the cue `sheet_next` at 5.62 becomes 4.37 and **snaps** to the bed beat at 4.40 (Δ = 0.03 s ≤ 0.1);
- the headline that was visible 0.0–2.1 s in the lesson is now visible 0.0–0.85 s in the Reel. That is below 1.2 s, a **major** finding: start the window earlier or drop the headline.

All numbers are illustrative.
