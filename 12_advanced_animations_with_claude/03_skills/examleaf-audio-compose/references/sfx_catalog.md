# SFX catalog and per-style palettes

**Scope.** Every one-shot that `scripts/sfx_palette.py` can render: how it is synthesised, what it is for, where it comes from, and which style palettes include it.
- Source for the paper-craft set: [V4-MP] §11, which lists paper swishes for sheet transitions, light taps for ransom letters, pops for cutouts, a boing for hops, a tear, a thud for drops and a sparkle chime, with booms and rumbles kept for real drama.
- Source for the STEM set: report §5.1 [Recommendation] ("electric hum, bubbling, click-snap for bonds").
- Everything else is a [Recommendation].

## 1. Format

- 48 kHz, 16-bit PCM, mono.
- Peak-normalised to −6 dBFS, with a 2 ms fade-in and a 5 ms fade-out so cuts never click. [N20] notes some toolchains cut "on zero crossings, with no normalising, EQ or fades unless you ask"; ExamLeaf asks.
- The level in the mix comes from `gain_db` on each cue-sheet `sfx[]` entry (report §5.5 example: `-12`). The validator warns on positive gain.

## 2. Catalog

| Name | Recipe (stdlib) | Duration | Use | Source |
|---|---|---|---|---|
| `paper_swish` | Seeded noise through a time-varying one-pole low-pass swept 800→6000 Hz, rise-fall envelope | 0.35 s | Sheet transition (0.5–0.7 s power3.out slide) | [V4-MP] |
| `whip` | `paper_swish` at double speed | ~0.18 s | Urgency whip (~0.4 s expo.out) | [V4-MP] §9 + §11 |
| `tap` | 4 ms noise click + 2 kHz sine blip | 0.04 s | Ransom-letter tile landing, per letter 0.04–0.05 s apart | [V4-MP] |
| `pop` | Sine swept 900→300 Hz, 30 ms decay | 0.09 s | Cutout or label pop-in (back.out) | [V4-MP] |
| `boing` | 220 Hz sine with decaying 12 Hz vibrato | 0.5 s | Hop with squash and stretch | [V4-MP] |
| `tear` | Seeded gated noise ("fibre crackle"), high-passed at 1.5 kHz, linear fade | 0.45 s | Tear-in-half gag | [V4-MP] |
| `thud` | 80→60 Hz and 45→40 Hz sines + low-passed noise hit | 0.3 s | Drop-in landing | [V4-MP] |
| `chime` | Inharmonic partials 1, 2.76, 5.4 × 880 Hz with staggered decays | 1.2 s | Sparkle / magic / "aha" moment | [V4-MP] |
| `rumble` | Double low-passed noise (120 Hz), slow envelope | 1.2 s | **Real drama only**; needs a storyboard justification | [V4-MP] |
| `pencil` | High-passed noise (3 kHz) with seeded stroke pressure | 0.4 s | Doodle stroke draws on | [Recommendation] |
| `electric_hum` | 100/200/300 Hz harmonics + faint noise | 0.8 s | Circuit closes, current flows (STEM) | report §5.1 |
| `bubble` | Six seeded rising sine blips | 0.6 s | Reaction, gas evolution (STEM) | report §5.1 |
| `snap` | 2 ms click + 3 kHz blip | 0.03 s | Bond forms, click-snap (STEM) | report §5.1 |

## 3. Palettes

| Style | Palette (plus the STEM extras on every style) |
|---|---|
| `paper-collage-vertical` | paper_swish, whip, tap, pop, boing, tear, thud, chime, rumble |
| `doodle-handdrawn` | pencil, pop, boing, whip, chime, tap |
| `editorial-vox` | whip, tap, thud, pop, chime, pencil |
| `kinetic-type` | tap, pop, whip, snap |
| `voxel-isometric` | pop, snap, thud, chime, whip |

STEM extras on every style: `electric_hum`, `bubble`, `snap`.

`python3 scripts/sfx_palette.py --list --style <style>` prints the palette with its uses. Asking for an effect outside the palette is refused. To add one: write a generator, add it to `GENERATORS`, `USE` and the palette, extend the selftest, and record the new script hash in asset-library.

## 4. Usage rules

1. **Subtle by default.** [V4-MP] says "kept subtle".
   - A sheet-transition swish sits around −18 dB in the cue sheet. A letter tap sits lower still, because a 9-letter ransom title fires 9 taps in under half a second.
   - These gains are [Recommendation] starting values; the mixer confirms them.
2. **One sound per visual beat.** Do not stack pop + chime + swish on one cue.
3. **No SFX under the core explanation** unless the storyboard names it and it passed the comprehension and listening-effort comparison. No laugh effects and no unrelated stings (`04_NARRATION_SUBPIPELINE.md` §13).
4. **STEM sounds never assert science.** A hum can accompany a circuit closing that the fixture shows closing. It must never imply current where the diagram shows none (report §7.13: decoration must not contradict the science).
5. **Placement** is the cue sheet's job (`sfx[{file, at, gain_db}]`, usually tied to a cue with `offset_s`). Scene code reads the cue sheet and never hard-codes SFX times.
6. **Photosensitivity pairing.** [V4-MP] pairs explosions with "a white flash or bloom"; house rule G15 replaces the flash. The `rumble` can carry the drama alone.

## 5. Licensing

All effects are synthesised from seeded code, so `contains_samples: false` and there are no third-party rights. A recorded or downloaded effect may be used only after `examleaf-asset-library` records its licence and attribution. Until then it is quarantined. Never mix an effect whose source is unknown.
