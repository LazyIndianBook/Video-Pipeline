# Pilot build contract (16 Oct 2026): three vertical concept-intro videos, strong tier vs cheap tier

This file is the single brief for every builder agent in this experiment, whatever model runs it. Read it fully before touching anything. Paths are relative to the project root `ExamLeaf_Video_EdTech_Pipeline/` unless absolute.

## 0. What is being tested

Three 60–70 s vertical videos (Physics, Chemistry, Biology; Class 10 NCERT level; English; format `concept_intro`), each built twice: once by a strong model (Opus 5.5, "reference" tier) and once by a cheap model (Haiku 5.5, "kit" tier) using only the project's own skills, guides and this contract. The lead (Fable) narrates, renders, runs QA and judges both. Where the cheap tier falls short, the gap is fixed in the guides and the cheap tier runs again. Nothing here is a release: Path B narration with a stock English voice, no human approvals, no platform export.

## 1. Folder layout (per subject, per tier)

```
16_pilot_builds_2026-10-16/<subject>/brief.md                  ← read first (topic, level, scope, style, voice)
16_pilot_builds_2026-10-16/<subject>/<tier>/                    ← tier = opus | haiku ; you write ONLY inside your tier folder
    lesson_graph.json        truth: claims, objectives, misconception, simplification, worked item, assessment item, fixture spec, sources
    fixtures/compute.py      executable science: prints fixture.json; every number on screen comes from here
    fixtures/fixture.json    output of compute.py (commit it)
    script.json              the beats (schema in §3)
    storyboard.md            one row per scene: what is on screen, which beat(s), which cues, style notes, safe-zone use
    scenes/sNN.html          one self-contained seek-deterministic scene per script scene (contract in §4)
    scenes/_preview/*.png    produced by tooling/preview_scene.py (see §6); keep the final set
    build_notes.md           Opus: the Kit card (see §7). Haiku: every place a guide was unclear, missing or wrong, and what you did instead
```

The lead adds later: `narration/` (beat audio, timeline), `cues/` (per-scene cue sheets), `render/` (MP4, manifest, contact sheet), `qa/` (reports).

## 2. Reading list (in this order; stop reading when you know the rule you need)

1. `<subject>/brief.md`
2. `12_advanced_animations_with_claude/04_harness_contract/contract.md` (sections 2, 4, 5, 6, 8, 9) and `scene_template.html` (copy its structure; it is the exemplar)
3. `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` (zone shares, side margin, insets) and `cue_sheet.schema.json`
4. The style guide named in the brief, under `12_advanced_animations_with_claude/05_style_guides/`
5. `03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md` (delivery modes, pacing 130–155 wpm, protected pauses) and `02_learning_psychology/INSTRUCTIONS_production_rules.md` (prediction before reveal, retrieval, no hype)
6. `15_content_engine_v2/subsystems/SCRIPTING_REGISTRY.md` §14 (sentence-to-node closure) and §15 (script quality checks)
7. Skills under `12_advanced_animations_with_claude/03_skills/`: `examleaf-anim-brief`, `examleaf-anim-storyboard-gate`, `examleaf-procedural-2d`, `examleaf-kinetic-typography`, `examleaf-vertical-adapt`, `examleaf-anim-qa` (read each `SKILL.md`; use their scripts where they fit)
8. `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md` (skim for your scene types)

## 3. `script.json` (pilot schema, exact)

```json
{
  "video_id": "phy-ohm-ci-01",
  "subject": "physics", "topic": "Ohm's law: does twice the voltage mean twice the current?",
  "level": "l9_10", "locale": "en-IN", "language": "en",
  "format": "concept_intro", "target_duration_s": 65, "style": "doodle-handdrawn",
  "voice": {"path": "B", "provider": "elevenlabs", "model_id": "eleven_v4", "voice_id": "JBFqnCBsd6RMkjVDRZzb", "persona": "persona/super-teacher#core"},
  "scenes": [ {"id": "s01", "file": "scenes/s01.html", "beats": ["b01", "b02"], "title": "Hook"} ],
  "beats": [
    {"id": "b01", "scene": "s01", "slot": "hook.question_reveal", "mode": "curious", "tag": "[curious]",
     "text": "Here's a ten-ohm resistor with two volts across it. Now we make it four volts. Does twice the voltage always mean twice the current?",
     "node_ids": ["CLM-ohm-proportional", "CLM-ohm-condition"],
     "pause_after_s": 0.6, "think_window_s": 0,
     "on_screen": {"headline": "twice the voltage?", "fx_refs": ["parameters.resistance_ohm", "parameters.v1", "parameters.v2"]},
     "cues": [ {"id": "c01", "kind": "reveal", "element_id": "resistor", "anchor_word": "resistor", "occurrence": 1, "lead_s": 0.05},
               {"id": "c02", "kind": "emphasis", "element_id": "v_label", "anchor_word": "four", "occurrence": 1, "lead_s": 0.05} ]}
  ]
}
```

Rules for the script:
- **Budget: the sum of all beat `text` characters is at most 1,000** (the narration account has a small monthly quota). Six to eight beats. Target 60–70 s at 130–155 wpm.
- `text` is exactly what is spoken. No stage directions in it. One optional inline tag per beat in `tag` (only `[curious]`, `[calm]`, `[warm]`, `[thoughtful]`), never inside `text`.
- Slots, in order, for `concept_intro`: `hook.question_reveal` → `check.predict` (a question, then `think_window_s` 4–6 of silence) → `explain.ladder_step` (one or two) → `worked.step` and/or `misconception.confront` (at least one; both allowed, worked first) → `check.retrieval` (optional, short) → `recap.statement` → `close.next_step` (the spoken pointer: the request's `cta_line`, default `Try the free lesson on <topic>.`; omitted when `cta_line` is empty) → `outro.brand` (the last beat; its text must be exactly: `Professor Diki Simplified.`). The disclosure is neither spoken nor shown: it lives in the platform's AI-content label and the description field `ai_voice_disclosure` (PD-20, PD-14). `check_script.py` enforces the order.
- The hook must not state the answer that `check.predict` asks for (SCRIPTING_REGISTRY §15 SQ-04): ask, do not reveal.
- Every beat except the outro maps to at least one `node_ids` entry that exists in `lesson_graph.json`. A sentence may not assert anything its nodes do not say. Numbers spoken must equal fixture values (write the number as words or digits as the Super Teacher guide says; the fixture is the source).
- No hype, no countdown, no "always comes in the exam", no "full marks". No personal data requests. Questions get a real pause.
- `on_screen.headline` words must be a subset of the beat's spoken words (any order, any subset) or fixture fields referenced in `fx_refs`. Nothing else is written on screen anywhere.
- `cues[].anchor_word` must be a word of this beat's `text` (case-insensitive; `occurrence` counts repeats within the beat). `kind` ∈ reveal | emphasis | hold. `element_id` must exist in the scene's DOM.

## 4. Scenes (`scenes/sNN.html`)

- One HTML file per entry in `scenes[]`, built like `scene_template.html`: fixed 1080×1920 stage, tokens block, zones from the tokens file (shares `top_title`/`middle_visual`/`bottom_caption`, side margin), `window.DURATION`, `async window.seek(t)`, `window.ready`, `window.__errors`, `window.__cueSource`, `window.__fixtureSource`, seeded PRNG only, no `Date`, `Math.random`, `requestAnimationFrame`, `setInterval`, `.play()`, infinite repeats, CDN or remote URL. Fonts: the system stack in the template (this machine has no Noto fonts; keep the `document.fonts.load` calls, they resolve to fallbacks and that is acceptable for the pilot).
- The scene receives **its own cue sheet** via `window.__CUE_SHEET__` (the lead injects it; fall back to `?cues=` then an inline block as the template does) and the fixture via `window.__FIXTURE__`. Scene-local time starts at 0 at the first word of the scene's first beat. `DURATION` comes from the cue sheet.
- Every science glyph (numbers, units, formulae, labels, equation text) is a DOM element with `data-fx="path.in.fixture"` whose text is filled from the fixture at ready; never typed by hand. Decorative layers encode no data.
- Reveal and emphasis are driven only by `cues[].at` and `words[].t0` from the cue sheet (element ids match `script.json`). Headline words appear per word on their `t0` (as the template does). A hold cue keeps an element until `until`.
- Think windows (silence) show a calm "Pause. Predict." treatment in the caption zone, no clock, no countdown. **Timing comes from the cue sheet:** `meta.think_windows[]` gives `start` and `end` in scene-local seconds (start = end of the predict beat's last word plus its `pause_after_s`). The two words of the plate are UI chrome, not science: put them in the fixture as `display.ui.think_prompt` and bind them with `data-fx` like any other string.
- **Verbatim text on screen comes from `meta.beats_text[]`** in the cue sheet: each record carries the beat `id`, `slot`, approved `text` (punctuation intact), `headline`, `start`, `end` and `word_range` (indices into `words[]`). Use it for any headline (the end-card lines are fixture display strings, PD-13); `words[]` is for per-word timing and reveals only (punctuation is stripped there). The tokens file's sizes win over the contract's minimums (heading 59 px, label 50 px, equation 63 px).
- Draw everything in SVG or canvas inside the file (paths, shapes, text). No images. Keep the look to the style guide's tokens, motion rules and holds (minimum hold 1.2 s per idea). Full-frame flashes are forbidden; see `examleaf-anim-qa` severities.
- Safe zones: nothing a learner must read inside the platform insets; headline in `top_title`, visual in `middle_visual`, captions/hints in `bottom_caption`; side margin ≥ 96 px.
- The outro scene is the end card, the final state of the scene (PD-03). It shows two literal fixture display strings bound with `data-fx` (`display.ui.endcard_line1/2`, PD-13), worded as in `17_professor_diki_simplified/brand/strings.json`: `Professor Diki Simplified` and `Free lesson: <topic>`. No disclosure line (PD-20) and nothing else promotional (no URL, QR code, handle or price).
- Self-check before you finish: `node 12_advanced_animations_with_claude/04_harness_contract/lint_seek_contract.js --level 1 scenes/sNN.html` must print `"ok": true` for every scene; `python3 tooling/check_script.py <tier>/script.json` must print `OK`; `python3 tooling/preview_scene.py <tier>/script.json sNN` must write preview PNGs with no `error` entries and no `W_*_FALLBACK`; look at the PNGs (open them) and fix layout, overlap, clipping and empty frames.

## 5. Lesson graph and fixtures

- `lesson_graph.json`: `{"graph_id", "subject", "level", "sources":[{"id":"SRC-ncert-...","kind":"textbook","title":"NCERT Class 10 Science","section":"...","reliability_class":"official_curriculum"}], "nodes":[{"id":"CLM-...","type":"claim","statement":"...","source_ids":[...],"fixture_ids":[...]}, {"id":"OBJ-..","type":"objective",...}, {"id":"MIS-..","type":"misconception","statement":"...","why_wrong":"..."}, {"id":"SIM-..","type":"simplification","statement":"...","what_is_lost":"..."}, {"id":"WRK-..","type":"worked_item","prompt":"...","steps":[...],"fixture_ids":[...]}, {"id":"ASM-..","type":"assessment_item","stem":"...","answer":"...","original":true}, {"id":"FIX-..","type":"fixture","compute":"fixtures/compute.py","outputs":[...]}]}`. Short statements; cite the NCERT chapter and section by name (no page quotes).
- `fixtures/compute.py`: plain Python 3, no third-party imports, prints JSON to stdout and writes `fixtures/fixture.json` with a top-level `display` object (labels and units as strings) and `parameters`/`results` objects (numbers). Chemistry fixtures count atoms from formulas in code; physics computes from the law; biology computes atom balance of the photosynthesis equation and the counts the script states. Include an `assert` for every result the script speaks.

## 6. Tooling the lead provides (run with the project venv python at `$PY`, printed in the brief)

- `tooling/check_script.py <script.json>`: schema, budget, node closure, anchors, scene references, on-screen subset.
- `tooling/preview_scene.py <script.json> <scene_id> [--fixture path]`: builds a synthetic evenly-spaced cue sheet for that scene, renders the scene in headless Chrome and writes `scenes/_preview/<scene>_<t>.png` at several times (including 0.3 s after each cue) plus `scenes/_preview/<scene>.report.json` with `__errors`, sources and DURATION.
- The lead's narration and render steps replace the synthetic timings with measured ones; scenes must not depend on the exact numbers.

## 7. Build notes

- **Opus (reference tier):** write `build_notes.md` as a Kit card for a cheap model: the decisions you made that the guides did not make for you, the rules you followed that a cheap model will skip unless told, a slot table for each scene archetype you used (what varies, what is fixed), the three mistakes you caught in your own preview, and the exact checks you ran. Follow `13_strong_to_cheap_model_strategy/DOCUMENTATION_TEMPLATES.md` §1 headings where they fit. Under 600 words.
- **Haiku (kit tier):** write `build_notes.md` listing, for every step, which guide you used, what was unclear or missing, and any rule you could not satisfy and why. Under 400 words. Do not read the `opus/` folder.

## 8. Non-negotiables

Never modify anything outside your tier folder. Never call a network service (the lead narrates). Never put a number, unit, formula or label on screen that is not a fixture field. Never add a claim the graph lacks. Do not exceed the character budget. Report what you could not do instead of pretending.
