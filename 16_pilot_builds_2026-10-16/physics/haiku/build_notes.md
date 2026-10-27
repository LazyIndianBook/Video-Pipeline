# Build notes (kit tier, Haiku 5.5): phy-ohm-ci-01

**1. Reading.** Used: contract §0-§9, §11-§13; brief; scene_template.html; tokens; cue schema; doodle-handdrawn §1-§14; Super Teacher Steps 7, 10; production rules F, G, I; registry §3, §14, §15, §18; six skill SKILL.md files; edge rows 15-19, 50-64. Never opened `opus/`.
Unclear: contract §4 says headline words come from `meta.beats_text`, but the template reads `words[]`. No rule maps headline words to word indices; I matched them in order inside each beat's `word_range`.

**2. Graph and fixtures.** Used: contract §5; registry §14, §18. Missing: no NCERT text in the project, so claims come from the brief, cited by chapter and section name only, and are not checked against the book. Added: whole-number results are stored as integers so DOM text equals fixture text.

**3. Script.** Used: contract §3; registry §3, §15 (SQ-04, SQ-20); production rules G2, G3; Super Teacher §9.3. Unclear: the `tag` vocabulary against delivery `mode`; I set both. Estimate 69 s at 144 wpm.

**4. Storyboard.** Used: contract §1 row format. storyboard-gate covers paid grids and approvals, which this pilot does not use, so none were produced.

**5. Scenes.** Used: scene_template.html; contract §2, §4-§9; tokens; doodle-handdrawn §2-§7; procedural-2d; kinetic-typography.
Deviations and gaps:
- Doodle §2.1 wobble is per vertex. No helper exists, so I used an SVG displacement filter seeded by the boil step.
- Boil rate: doodle §2.1 says 10 fps, procedural-2d says 8. I used 10.
- Kalam (doodle §5) is not vendored; the system stack is used, as contract §4 allows.
- Depth (doodle §3) is only partly met: three layers, one hatch shadow, no camera drift, no off-register fills.
- The template ignores `hold` cues. Mine keeps an element until `until`. Unused here.
- vertical-adapt gives default zones 18/57/25; the tokens give 22/54/24. I used the tokens.

**6. Checks.** lint `--level 1`: 0 errors, 0 warnings on all five. check_script: OK. preview_scene: exit 0, errors [], injected sources on all five. Scratch DOM check: every `data-fx` text equals its fixture field; static text is headline or disclosure only.
Double render: two separate processes, five scenes, 38 preview frames, all byte-identical (SHA-256). Not run: anim-qa safe-zone, text-diff and flash checks (L2); determinism_hash_check.py needs a harness frame dump.
