# Build notes (Haiku, kit tier): chem-balance-ci-01

## Steps: guide used; what was unclear or missing
1. **Reading.** PILOT_CONTRACT §0-8; brief; harness contract §2, 4-9, 11-13; scene_template; tokens; cue schema; editorial-vox; production rules D-I; Super Teacher §9-10; SCRIPTING_REGISTRY §14-15; six named skills.
2. **lesson_graph.json.** Contract §5. Unclear: fixture `outputs` form, source ids. NCERT cited by section, not checked against the book.
3. **compute.py.** PILOT §5. Unclear whether `results` may nest (I nested counts). Asserts pass.
4. **script.json.** PILOT §3, SCRIPTING_REGISTRY §15, production G2-G3, Super Teacher §10. Conflict: dense notation paces at 105-125 wpm, but 60-70 s with 1,000 characters needs 130-155. Kept 130-155 (estimate 70 s).
5. **storyboard.md.** PILOT §1. Storyboard-gate and anim-brief skills assume paid generation and approvals; not applicable, not run.
6. **Scenes.** scene_template; contract §2, 4-9, 12; editorial-vox §3-8; kinetic-typography; vertical-adapt; procedural-2d; anim-qa.
7. **Checks.** Lint, check_script, preview, DOM audit, determinism (forward, shuffled, reverse, separate processes).

## Guide problems
- **Harness template (critical).** scene_template section [11] animates `transform` on `.w` spans. On Chrome 155 here, the unmodified template renders different pixels at 10 of 11 times when seeked in reverse; removing the transform fixes it. Contract §2 evidence covers DOM and canvas, not pixels.
- editorial-vox says "not for equations", yet the brief needs one. No equation archetype.
- Fonts: Noto Serif is not installed; the template stack includes system-ui, which the guide bans as display. Fallback order unspecified.
- Contract §8 requires inline fallbacks; I dropped them, since a silent fallback hides a changed cue sheet.
- Production D7 requires captions; contract §3-4 forbids other on-screen text. No captions drawn.
- Template reads headlines from `words[]`; contract §4 says `meta.beats_text`.

## Rules not met
- Narration captions (above). Push-in omitted (editorial-vox §8).
- Layout uses getComputedTextLength() in ready(): deterministic on one machine only.
- Not run: layout_zones, safe_zone_check, text_fixture_diff, flash_check (outside §4).
- Reduced-motion (`?reduced=1`): error-checked only.

## Iterations after previews
1. Hook: a card multiplied with the highlight into a heavy block; removed it, equation to 81 px, added the word equation.
2. Georgia's old-style figures sat low; switched to lining figures; content centred.
3. Compact tallies read as "H2O2"; spaced them.
4. Headline hold 1.07 s, below 1.2 s: pause after b03 raised to 1.0 s; three pauses cut to 0.4 s.
5. Determinism failed on headline transforms; fixed, rechecked.
