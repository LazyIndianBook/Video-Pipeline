# Re-timing on TTS regeneration (#63) and Reel sub-ranges

## 1. Why this exists

Edge case #63: "TTS regenerated → reveals out of sync → timings changed → **cue-sheet driven code; re-align**" ([V4-MP], [Recommendation]). The [V4-MP] master prompt syncs animation "to the voiceover timing". In ExamLeaf, narration is regenerated for many reasons:
- a pronunciation repair (`examleaf-stem-pronunciation`);
- a wording change after academic review;
- a provider retake;
- a new locale.

If scene code holds times, every regeneration becomes a code edit, which means re-review of code and a risk of drift. With the cue sheet, a regeneration is **data-only**.

## 2. The procedure

```text
1. Narration regenerated (voice-synthesis / tts-provider-adapter)      → new segment WAV (new audio_sha256)
2. Re-align (examleaf-alignment-localize)                             → new Alignment JSON
3. Re-compose timeline (examleaf-speech-animation-synchronizer)       → new timeline.json (events, captions, pauses)
4. Archive the old sheet:  cp cue_sheet.json cue_sheet.v<N>.json
5. Rebuild (this skill), SAME cue_spec.json:
     python3 scripts/build_cue_sheet.py --spec cue_spec.json --out cue_sheet.json --previous cue_sheet.v<N>.json
6. Read cue_sheet.retime.json: per-cue delta_s, duration/frames old→new, added/removed cues
7. If the bed length changed by ≥ 1 bar → examleaf-audio-compose re-renders the bed (same seed), then audio-analysis
8. Re-render the scene (examleaf-render-batch): the scene CODE is unchanged, its INPUT hash changed
9. Re-run examleaf-anim-qa (reveal-on-word, holds, safe zones) and the determinism hash test
10. Approvals: any changed critical artefact invalidates approval (examleaf-release-review)
```

What **must not** change in that procedure:
- scene source code;
- `cue_spec.json`, unless the *wording* changed. In that case an anchor phrase may no longer exist, the build blocks with "missing occurrence", and the author updates the spec against the newly approved script;
- the music seed;
- any fixture value.

## 3. Reading the re-time report

```json
{"scene_id": "phy-10-03-s04", "duration_old": 3.3, "duration_new": 3.5,
 "frames_old": 99, "frames_new": 105,
 "cues": [{"id": "arrow_2", "old_at": 1.25, "new_at": 1.45, "delta_s": 0.2},
          {"id": "title", "old_at": 0.0, "new_at": 0.0, "delta_s": 0.0}],
 "added": [], "removed": [],
 "action": "scene code unchanged; re-render the scene and re-run QA (hash changes)"}
```

| Pattern in the report | Likely cause | Action |
|---|---|---|
| All anchored cues shift by the same delta | Leading silence or padding changed | Fine; re-render |
| Deltas grow through the scene | Different speaking rate | Re-check headline holds (#50) and equation holds in anim-qa |
| One cue jumps a lot | The anchor matched a different occurrence | Check `anchors[].word_index` in provenance; fix `occurrence` |
| `removed` is non-empty | The spec changed, or a window dropped cues | Confirm intentional |
| Frames changed | Duration changed | Composition timeline (`examleaf-web-composition`) must take the new length; the bed may need a bar more or less |
| Build blocked: missing occurrence | The wording changed | Not a re-time: script change → narration pipeline → academic approval → update the spec |

## 4. Repeated words: the most common silent failure

When the regenerated script reorders a sentence, "current" may move from occurrence 2 to occurrence 3. The builder cannot know which one the illustration meant. Two things protect you:
- it resolves strictly by occurrence and records `word_index`;
- `examleaf-anim-qa` checks that the reveal lands on the intended word in the render.

A human confirms any anchor flagged in the handoff.

## 5. Reel sub-ranges (`--window START END`)

Scenes are pure functions of time [N61] (contested), so a Reel can reuse a lesson scene's time range without new code (report §9 item 10; `examleaf-vertical-adapt` `references/reel_subrange_recipe.md`).

```sh
python3 scripts/build_cue_sheet.py --spec jobs/phy-10-03-s04/cue_spec.json \
    --out jobs/reel-phy-10-03-a/cue_sheet.json --window 1.25 9.80
```

- Words, beats, cues and SFX inside the window shift by −START. The duration is snapped up to whole frames.
- A window boundary inside a word is **blocked**: "window cuts through the word …; move the window to a word gap". Reels reuse accepted narration segments whole where they stand alone (`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md`).
- Cues outside the window appear in `provenance.dropped_cues`. If a dropped cue revealed something the remaining narration refers to, the Reel is not standalone. `examleaf-reel-repurpose` rejects it ("Produce fewer useful Shorts rather than cutting arbitrary segments").
- The scene renders with its local time mapped as `t_scene = START + t_reel`. That mapping belongs to the composition (`examleaf-motion-harness` / `examleaf-web-composition`); the cue sheet carries Reel-local times.
- **Beat re-time for Reels:** a decorative transition may move to the nearest beat within a tolerance (`examleaf-vertical-adapt`). A narration-locked reveal never moves off its word.

## 6. Determinism check after a re-time

Because outputs are byte-deterministic, rebuilding the same spec with the same inputs must give the same `cue_sheet.json` bytes. If it does not, an input changed without a hash change (an untracked file), and that is a blocker. The selftest asserts this.
