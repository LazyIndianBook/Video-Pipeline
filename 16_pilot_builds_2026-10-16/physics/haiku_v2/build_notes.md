# Build notes (kit tier, Haiku 5.5, second attempt): phy-ohm-ci-01

**Reading.** Contract, brief, Kit (README, RESTRICTIONS, SKILL, skeleton, EDGE_CASES, LEARNINGS), harness contract and template, tokens, cue schema, doodle guide, SCRIPTING_REGISTRY §14-§16. Not opened: opus/, judging/, COMPARISON_and_GAPS.md.

**Fixture and graph.** compute.py asserts every spoken value and writes the display strings (condition, R ↑, ×2, V = I × R, ui.think_prompt). Graph reused, except CLM-ohm-filament now says resistance "rises" as the lamp heats, which the R ↑ glyph needs.

**Script.** Slot order and budget per check_script; SKILL §3 slot table; SQ-04 (hook asks only); SQ-23 (confront answers the predict and names the evidence); SQ-22 (condition spoken where shown).

**Scenes.** No coded skeleton exists (Kit README), so _build/make.py inlines one runtime into each scene. It differs from scene_template.html: opacity-only reveals (R-012), per-beat headline groups from meta.beats_text (R-008, EC-113), disclosure from beats_text, think plate and boil frozen in the window.

**Rules followed.** R-002: condition, ×2 and V = I × R on their words in s03 and again in the s05 rows. R-003: confront reuses the s01 loop ids, with the resistor swapped for a lamp. R-007/R-016: no answer on screen before or during the predict. R-009: L0-L4 tagged. R-014: every label through data-fx. R-017: containers reveal with their first child.

**Not fully met.** R-001: in s01, s02 and s04 the circuit fills about 45% of the middle zone; the rest is blank for the whole beat. R-004/R-005: the worked step recounts with two ratio rows, not a state switch. R-008: Kalam is not vendored; the rendered face is a fallback I could not identify. R-018: checked by eye at full size, not measured. Board not wobbled; no paper grain.

**Unclear or contradictory.**
- RESTRICTIONS R-008 says headline words "in order"; contract §3 says "any order"; check_script checks neither order nor the 6-word cap.
- Skeleton §1 reserves bottom_caption for lead captions; contract §3-§4 say nothing else on screen; EC-114 open.
- scene_template.html scales cues with CSS transform (against R-012) and reads only the first six headline words (EC-113).
- SKILL §3 says s04 reuses "s01/s03" setup; s03 is a card archetype. I reused the loop ids.
- R-004 and SKILL rule 5 assume state switches; Ohm's law has two readings, so the rule has no clear form here.
- SKILL §2 says escalate SKELETON_GAP when more than one field is new; I wrote a generator and did not escalate.
