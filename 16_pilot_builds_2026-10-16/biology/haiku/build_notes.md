# build_notes (haiku tier, bio-photosyn-ci-01)

Nothing under opus/ was opened.

## Step 1: reading
- Used: pilot contract; harness contract §§2, 4-9, 11-13; template; tokens; cue schema; paper-collage digest, §§0-10, 15-17; procedural-2d; kinetic-typography; anim-qa; vertical-adapt; Super Teacher 2, 7, 10; production rules B1, E1, E5, F1, I1, I3, I5; SCRIPTING_REGISTRY §§2, 3, 13-15.
- Unclear: no precedence order. storyboard-gate hard-stops for human approval; the pilot waives it. I followed the pilot and made no beats.json, estimate.json or approval_record.json.

## Step 2: lesson graph and fixture
- Used: contract §5; pilot §5; SCRIPTING_REGISTRY §14.
- Wrong in brief: oxygen count "24/24". The balanced count is 18 per side; compute.py asserts 18.
- Unsupported in brief: "most of a plant's dry mass is carbon" (about half). Script says "about forty percent of glucose" and "a large share" (flagged).
- Not satisfiable: "fifty elephants". No fixture value or node supports it; §14 makes every model sentence assertive. Dropped.
- For subject review: CLM-carbon-to-structure, CLM-wood-carbon-from-air, CLM-dry-mass-carbon.

## Step 3: script
- Used: pilot §3; check_script; Super Teacher 7, 10; production rules B1, F1, I3, I5.
- Removed "Not mainly from the soil" from the hook: it gives part of the predict answer (pilot §3; SQ-04).
- Missing: a mode-to-tag map. Used steady to [calm], deliberate to [thoughtful], light to [warm].

## Step 4: storyboard and scenes
- Used: paper-collage §§3, 5.4, 7.2, 8.4, 15; tokens; template; procedural-2d; kinetic-typography; contract §§4, 8, 9.
- Conflict: boil rate. Brief and procedural-2d say 8 fps; style §8.4, §15.4 and digest item 6 say 10 fps. Used 8, decorative sparkles only, frozen in think windows.
- Not built: ransom and brush typography (no fonts, no network); caption track (pilot allows no other text); paper textures; paper-sheet transitions (no spec for who draws them); reduced motion.
- Approximate: die-cut border and shadow via SVG filters, not compared to a style test sheet.
- Template gaps: its headline builder shows the first six sheet words, so per-beat headlines are never shown. Its inline fallbacks are demo data; removed.

## Step 5: checks
- Lint level 1: 0 errors, 0 warnings per scene.
- check_script: OK. preview_scene: exit 0 per scene, sources injected.
- Own checks: double render in two browser sessions, 15 frames identical; rendered text against fixture, 38 bindings, 0 mismatches.
- Tool gap: preview_scene --times takes fractions of DURATION; the docstring does not say so.
