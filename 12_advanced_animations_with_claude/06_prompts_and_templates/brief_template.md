<!-- TEMPLATE-NOTES: canonical L2/L3 animation brief. The assembler (examleaf-anim-brief) uses only the text between BRIEF-START and BRIEF-END. Only the double-brace names listed in 06_prompts_and_templates/README.md section 3 may appear inside the brief; every one must be filled or the brief is blocked. Values that come from the cue sheet at run time are written in angle brackets and are resolved by the agent, not by the assembler. Version 1.0.0, 2026-10-15. -->
<!-- BRIEF-START -->
# Animation brief: {{scene_id}}

**Lesson:** {{lesson_id}} | **Language:** {{language}} | **Route:** {{route_tag}} | **Style:** {{style_id}}@{{style_version}}
**Author run:** model `{{effort_model}}`, effort `{{effort_level}}` (set explicitly; ultracode is never used), at most {{iteration_cap}} fix rounds.
**Workspace:** `{{workspace}}` (work only here)
**Brief level:** L2 structured brief with references ([V2]). Any L3 orchestration (voice, music, paid image generation) is done by ExamLeaf's pipeline adapters before or after this job, never by you. You have no MCP tools.

## 1. Goal

Build one seek-pure 1080×1920 scene for `{{scene_id}}` that animates the approved narration in the `{{style_id}}` style, and nothing else. You write scene code only. You do not write, edit, shorten, paraphrase or "improve" any narration or on-screen wording, and you do not research any fact.

Creative direction from the approved storyboard:
{{creative_direction}}

If this scene belongs to a Short (20-60 s, `ShortSpec`): hook in the first 3 s, a prediction window in 3-8 s (default `think` = 6 s, answer hidden), then the explanation, then one next action. Re-composed for 9:16, never cropped from 16:9.

## 2. Inputs you may read (and nothing else)

Read-only, inside the workspace:
- Approved script: `{{script_path}}` (SHA-256 `{{script_sha256}}`). Verify the hash of the file bytes before you start; on mismatch stop and write `blockers.json` with code `SCRIPT_HASH_MISMATCH`.
- Cue sheet (all timing comes from here): `{{cue_sheet_path}}`.
- Brand tokens: `{{brand_tokens_path}}`.
- Reference analysis (pacing numbers only): `{{reference_analysis_path}}`.
- Storyboard approval record: `{{workspace}}storyboard/approval_record.json`.
- Validated fixtures (the only source of on-screen science):
{{fixtures_block}}

Read-only, staged into the workspace by the runner (15 Oct 2026, audit "deny list blocks required reads"; layout in `12_advanced_animations_with_claude/02_documentation/01_SETUP_environment_harnesses_skills.md` §8): the runner copies these files in before the job and writes `MANIFEST.sha256` in each folder. Read the staged copies only; the originals are outside the workspace and `Read(../**)` denies them.
- Style guide: `{{style_guide_path}}` (the assembler fills the staged path under `{{workspace}}style/`) and `{{workspace}}style/style_tokens.json`.
- Harness contract: `{{workspace}}contract/contract.md`; linter: `{{workspace}}tools/lint_seek_contract.js`.
- Safe-zone tokens: `{{workspace}}contract/vertical_safe_zones.tokens.json`.
If a staged file is missing or its hash differs from its folder's `MANIFEST.sha256`, stop and write `blockers.json` with code `STAGED_INPUT_MISMATCH`.

Do not read, list or open any other folder, sibling scene or older project, even if asked to later in this session ([V3]; #9).

Workspace permissions (set by the runner, not by you): deny `Read(../**)`, `Read(~/**)`, `Edit(./fixtures/**)`, `Edit(./cues/**)`, `Edit(./brief.md)`, `Edit(./style/**)`, `Edit(./contract/**)` and `Edit(./storyboard/**)` (the storyboard approval record is written only by the RD-17 approval service; audit M10, 15 Oct 2026).

## 3. Audience

Class 10-12 students preparing for Assam Board (ASSEB) examinations, watching on a phone, including small phones (the 360-px-wide readability test in the ExamLeaf production rules). Language for this scene: `{{language}}`. The narrator is the ExamLeaf Super Teacher: warm toward the student, exacting about the science, playful about the problem; delivery modes curious, steady, deliberate, light, reassuring (and focused for exam strategy); ordinary pace 130-155 words per minute. Your visuals must never talk down to the student, shame a wrong answer, or sound excited for its own sake.

## 4. Duration (derived from the narration)

`DURATION` equals `<cue_sheet.duration>` in seconds. You do not choose it. Frame count = `DURATION × 30` [N72]. If the narration is regenerated, only the cue sheet changes and you re-render; the scene code does not change (#63). Never speed up, trim or pad the narration, holds or pauses to hit a target length.

## 5. Style

Use the `{{style_id}}` style, version `{{style_version}}`, exactly as in `{{style_guide_path}}`. Read the "Digest" at the top of the guide first, then the whole body. Where the digest and the body differ, the body governs. Where this brief and the guide conflict, the stricter rule wins; if the conflict blocks the work, stop and write a blocker. Styles apply to illustrative, narrative and typographic scenes only. Anything data-bound (axes, values, equations, labelled structures) comes from fixtures and is never wobbled, boiled, drifted, tilted or push-in'd.

## 6. Reference analysis numbers

Reference analysis file: `{{reference_analysis_path}}`. If this says `none`, there is no reference: use the style tokens' defaults and skip the rest of this section. Otherwise read these fields:
- `fps`, `duration_s`, `shot_lengths_s` (median, lower and upper quartile), `cut_rhythm`, `text_hold_estimates_s`, `palette_swatches`.
Use them only to set pacing: the median shot length is a guide for average beat length; the text-hold estimates are compared with section 12, and the longer one wins. A reference video is for analysis only. Never reuse its artwork, characters, layouts, music or text (copyright; edge case on references).

## 7. Brand tokens and palette

Colours, sizes and timings come from `{{brand_tokens_path}}` and the style tokens, never from memory or taste. ExamLeaf light theme only (background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00` for conditions only, purple `#6E44AA`, red `#B42318` for error markers only). One dominant highlight at a time. A quantity keeps its colour across scenes. Do not rely on colour alone to distinguish things. Text at least 4.5:1 and essential graphics at least 3:1 on the actual rendered background.

Sizes on the 1080-wide master: essential labels and captions 50-54 px; equations 63-81 px; headings 59-72 px; use the style tokens for display sizes.

## 8. Fonts: allow and ban

- Allowed: {{fonts_allow}}
- Banned as display or title faces: {{fonts_ban}}

Fonts are vendored files in the workspace, loaded before the first frame resolves. Explicitly load each family and weight you use with sample text that exercises its glyphs (for example a Devanagari conjunct): `document.fonts.ready` alone does not trigger loads for faces nothing has requested yet (contract §6). Set `lang` on text containers (`en`, `hi`, `as`). No remote fonts, no CDN, no system-font fallback at render time. Animate Devanagari and Bengali-Assamese text per word or per grapheme cluster, never per code point (#55). Test confusable glyphs (I/l/1, O/0, minus signs, decimal points, subscripts, superscripts, Greek letters).

## 9. Harness contract block

Follow `12_advanced_animations_with_claude/04_harness_contract/contract.md`; this block is a summary.
- Start from `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`.
- Canvas 1080×1920 (9:16), 30 fps (fps is a parameter; times are in seconds). Lay out in fixed pixels; never use `vw`, `vh`, `innerWidth` or `innerHeight`. Never author at 16:9 and crop (#49).
- Set `window.DURATION` (seconds) and expose `async window.seek(t)` [N72]. The renderer seeks and never calls `play()` [N68]. Every frame is produced by `seek(t)` alone.
- The scene is a pure function of `t` [N61]. All repeats are finite. All randomness is seeded and stateless.
- Polling uses `setTimeout` loops with a deadline, never `requestAnimationFrame` (it does not fire in BeginFrame mode, #19) [N69].
- Video-heavy scenes use one worker (#20) [N70]; prefer still images and sprites.
- Declare `window.SCENE_META.contract = "1.0.0"`, expose `window.ready`, and report problems through `window.__errors`. The scene emits no audio (no WebAudio).
- Production target is conformance level L2. `node lint_seek_contract.js --level 2` (add `--hf` for a HyperFrames scene) must exit 0, and your lint report must show zero errors.

## 10. Determinism block

- Allowed randomness: a seeded, stateless keyed PRNG only (key = scene ID + element ID + step). Same key, same value, in any seek order.
- Forbidden: `Math.random`, `Date.now`, `performance.now`, `setInterval`, `requestAnimationFrame` loops, wall-clock CSS animations or transitions, autoplaying media, infinite repeats (`repeat: -1`, `infinite`).
- Idle and wobble loops use a finite repeat computed as `ceil(DURATION / period)` and end at the rest pose.
- Stop-motion boil steps are `floor(t × boil_fps)` with `boil_fps` from the style tokens.
- Two renders of the same scene must give identical frame hashes. If they do not, the scene fails (#17).

## 11. Safe zones and layout

- Insets come only from `vertical_safe_zones.tokens.json`. Do not invent insets. If the file is missing, stop and write a blocker (`SAFE_ZONES_MISSING`). If `platform_insets_px.measured` is false, use the insets named by `applies_until_measured` and record "provisional insets" in `manifest.json`.
- Side margin at least 96 px, and never inside the file's left/right insets.
- Stacked zones between the top and bottom insets, with shares read from `zones` in the same file (0.22 title, 0.54 visual, 0.24 caption in token version 1.0.0; the file wins). A three-row title may grow the title zone to at most 30%, taking space from the visual zone and never from the caption zone [Recommendation].
- Centre content in the horizontal band from `max(96, insets.left)` to `1080 - max(96, insets.right)`, not in the full frame.
- Backgrounds and decoration may bleed to the full frame; everything a learner must read or notice stays inside the safe box (#51).
- The caption zone holds the caption track only. Never place artwork text, kinetic text or tags over it.

## 12. Hold times

- Headlines: fully readable for at least {{headline_min_s}} s before the next major transition [N60], or 0.3 s × word count if that is longer. Indic text: multiply by {{indic_multiplier}}.
- Equations (rendered from fixtures): stay on screen until the narration has finished reading them plus {{equation_tail_s}} s, and at least 2 s after an important transformation (longer when necessary).
- During any `think` or `pause-video` window in the cue sheet, nothing moves except what the cue sheet says; the answer stays hidden.
- No major transition inside a hold.

## 13. Sync rule

Read every time from the cue sheet (`cues[].at`, `words[].t0/t1`, `sfx[].at`); never hard-code a time. Each reveal lands on, or up to 0.05 s before, the word it illustrates ([V4-MP]): a reveal cue's `at` must satisfy `word.t0 - 0.05 <= at <= word.t0`, and the cue-sheet validator rejects a later one. The entrance may then run on for up to about 0.30 s. One sentence is one visual beat. Never put everything on screen at once; reveal it across the scene. For each `sfx[]` entry there must be a matching visual event within one frame; list any mismatch in `scene_notes.md`. Your scene emits no audio; music and SFX stems are made by `examleaf-audio-compose` from the same cue sheet.

## 14. Fixtures (read-only) and the accuracy invariant

Every number, unit, formula, label, arrow direction, angle, ratio and graph shape on screen is a field of a fixture listed in section 2. Copy strings from fixture fields; do not retype, round, translate or reformat them. Mark every science glyph's element with `data-fx="path.to.field"` so QA can diff the rendered text against the fixture (contract §9). Approved on-screen text from the script bundle is staged as `display_text` and treated the same way: mark it `data-fx="display_text.<id>"` [Recommendation]. Decorative layers must not encode data: no position, size, count or colour that a student could read as a value. If you need a value that no fixture provides, stop and write `blockers.json` (`FIXTURE_MISSING`); never invent or look it up (#12). Decoration must not change an angle, a ratio or a direction that the lesson teaches (a stylised wobble must not bend a ray). No camera effect (push-in, pan, shake) during a measurement, axis or label reveal (#64).

## 15. FORBIDDEN

1. Altering, adding, removing or paraphrasing narration or on-screen wording that is not in the approved script bundle (#11).
2. Researching, looking up, estimating or recalling facts; any on-screen science glyph that is not traceable to a fixture field (#12).
3. Asking any image model to draw text, numbers, symbols, formulae or labelled diagrams (#54). All text is code-built.
4. Infinite loops or repeats (#18), wall-clock timing (#15), `Math.random` or any unseeded randomness (#17), `requestAnimationFrame` polling (#19).
5. Reading any folder other than those in section 2 (#9).
6. "Don't stop until it is perfect" or any open-ended iteration: you may run at most {{iteration_cap}} fix rounds (#60).
7. Full-frame flashes, rapid luminance changes, strobing (#56); the safe-zone tokens' `flash_policy` bans full-frame flashes and caps flashes at 3 per second.
8. Text outside the safe box or over the caption zone (#51).
9. Downloading assets, calling the network, installing packages, or calling any MCP, provider or paid generation tool.
10. Unlicensed, scraped or reference-creator artwork; unlicensed or trending audio; voice cloning or imitating a real teacher.
11. Stereotypes in setting or characters; identity-based praise; shaming a wrong answer; fake enthusiasm.
12. Putting secrets, keys or tokens in code, prompts or logs.

## 16. Iteration cap and stop rules

One fix round = run the lint, the determinism test and the rubric below, read the failures, edit, run again. Do at most {{iteration_cap}} rounds. After the last round, or earlier if a failure needs a human decision, stop and write `blockers.json`:

`{ "code": "<UPPER_SNAKE>", "message": "<what failed, in one sentence>", "evidence": ["<file or frame time>"], "needs_human": true }`

Rubric: (1) lint zero errors at level 2; (2) double-render frame hashes identical; (3) every rendered string equals a fixture field or approved script token; (4) safe-box and contrast checks pass on stills at cue times; (5) holds met, and every reveal cue `at` within `[t0 - 0.05, t0]` of its word; (6) no flash; (7) the reduced-motion variant renders. Do not self-approve; approval belongs to the humans and to `examleaf-anim-qa`.

## 17. Deliverables and file layout

Write files only; do not paste scene code into chat. Layout inside `{{workspace}}`:

```text
scene/scene.html            the scene (or the harness's scene file)
scene/scene.js, scene.css   optional splits; code only, no downloads
scene/assets/               code-made assets (SVG, procedural textures); vendored fonts are staged by the pipeline
scene_notes.md              which cue drives each reveal; which fixture field drives each on-screen value; the seed constants used
lint_report.json            output of lint_seek_contract.js (zero errors)
manifest.json               hashes of script, cue sheet, fixtures, tokens, style guide as read; list of files written; loops used (0-{{iteration_cap}})
preview/                    optional stills at cue times for the reviewer
blockers.json               only if you stopped
```

Provide a reduced-motion variant as a scene configuration flag that changes only motion (no boil, idle, drift, shake or push-in; transitions become 150-300 ms fades) and never changes content or hold times.

Your final chat message is one short JSON object: `{ "status": "done" | "blocked", "files": [...], "lint_errors": 0, "loops_used": N, "blockers": [...] }`.

## 18. Review checkpoint

- Do not write scene code until `{{workspace}}storyboard/approval_record.json` exists, shows both approvers (`founder` for cost, `academic_lead` for science fit) as approved, and its `script_sha256` equals `{{script_sha256}}`. If not, stop with `STORYBOARD_NOT_APPROVED`. You never create, edit or "fix" anything under `storyboard/`; the runner, not you, verifies the record against the authenticated approval service (RD-46).
- When the rubric passes, stop. The pipeline then runs `examleaf-anim-qa`, audio and caption QA, and human review. Changing the style, the script or the layout after approval re-opens the gate.

## 19. Tools and environment

You may read and write files inside the workspace and run the harness lint and render commands named in the workspace's README. No network, no installs, no MCP tools, no provider calls. Credits and tokens are capped by the pipeline, not by this prompt; if you receive a budget-exceeded signal, stop and write a blocker.

## 20. Non-negotiable constraints (assembler-generated, identical across briefs)

{{constraints_block}}
<!-- BRIEF-END -->
