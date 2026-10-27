# Master prompt: paper-collage educational animation, ExamLeaf vertical (1080×1920)

**Rewrite of:** [V4-MP], the RandomAI "Paper-Cutout Storybook Collage" master prompt for a 16:9 explainer (verbatim local copy: `12_advanced_animations_with_claude/00_reference_videos/master_prompt_paper_collage.md`; source in `01_research/RESEARCH_REPORT_advanced_animations_with_claude.md` §1.3).
**Style guide it uses:** `12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md` (version 1.0.0) and `style_tokens.json`.
**Version:** 1.0.0 | **Date:** 15 Oct 2026 | **Status:** draft for the pilot. Nothing here has been run.

**Evidence labels:** [V#]/[N#] are cited from the research report; [Recommendation] = design judgement; [Hypothesis] = untested; edge cases are #1-#65 (report §8); project decisions are RD-xx (`07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md`).

## How to read and use this file

- The structure of [V4-MP] is kept visible: each step is shown as an **ORIGINAL →** line (a short paraphrase of what [V4-MP] says, never a quotation) followed by an **EXAMLEAF →** block (the text that replaces it). The EXAMLEAF blocks are what a session receives.
- Fields in angle brackets, such as `<scene_id>`, are filled by the pipeline from the job's brief. This file is not processed by the brief helper (that is `brief_template.md`). In production the brief assembler produces the brief and the session prompt together from the job's approved inputs; this file is the reference wording for the paper-collage workflow.
- Use it only for `illustrative` or `narrative` scenes tagged by `examleaf-storyboard-route`. A `data-bound` scene never goes through this prompt (it is built from fixtures by the SVG, Manim, molecule or biology skills).
- Run settings: Claude Code, a pinned full model ID, effort **high** set explicitly (xhigh only with a written reason), **never ultracode** (#1, #3, #4; report §3.4). One isolated workspace per job (#9).
- Iteration cap: at most 3 fix rounds; no "don't stop until it matches" (#60).

## Summary of what changed from [V4-MP]

| Aspect | ORIGINAL → | EXAMLEAF → |
|---|---|---|
| Frame | 16:9, 1920×1080, 30 fps | 9:16, 1080×1920, 30 fps, stacked zones in the platform-safe box |
| Script | The model writes about 140-160 words | The model never writes it; it uses the approved script (hash-checked) |
| Voice | Higgsfield, preset voice "Arthur", ElevenLabs v3 | ExamLeaf TTS adapter and alignment; the cue sheet drives timing |
| Storyboard | Higgsfield GPT Image grid | Code thumbnails first (free); Higgsfield only if approved with a credit estimate |
| Checkpoint | Stop after script and storyboard | Stop after storyboard; approval bound to the script hash and credit cap |
| Build | JavaScript replicating the style | Seek-pure scene code under the harness contract, fixtures read-only |
| Sound | Inside the style guide only | Separate step: `examleaf-audio-compose`; -16 LUFS / -1 dBTP |
| QA | None | Separate step: `examleaf-anim-qa` |
| Science on screen | Free | Fixtures only; image models never draw text, numbers or formulae |

---

## Opening

**ORIGINAL →** Ask for a roughly one-minute animated explainer about a single story (an asteroid and the dinosaurs). Match the writing and animation style of the Style Guide at the end of the prompt. There is no reference video; the Style Guide replaces it.

**EXAMLEAF →**

```text
You are building the illustrative layer of ExamLeaf scene <scene_id> (lesson <lesson_id>,
language <language>, route <route_tag>) as seek-pure scene code. The look is the
"Paper-Cutout Storybook Collage" adapted to 1080x1920 at 30 fps. There is no reference
video: the style guide at 12_advanced_animations_with_claude/05_style_guides/
paper-collage-vertical.md replaces it. Your workspace is <workspace>; read only the
paths named in your brief.

You never write, edit, shorten or "improve" narration. You never research facts. You
never ask an image model to draw text, numbers, symbols or formulae. Every number, unit,
formula, label, arrow direction and graph shape on screen comes from a fixture field in
your brief. The scene duration is <cue_sheet.duration>, taken from the cue sheet.

This scene is <duration> s long and has <n_beats> beats. Creative direction from the
approved storyboard: <creative_direction>.
```

## Step 1: Study the style guide

**ORIGINAL →** Read the Style Guide: the writing style (tone, sentence length, pacing, hooks, how facts are delivered) and the animation style (built entirely in JavaScript: visual approach, motion, transitions, typography, palette).

**EXAMLEAF →**

```text
Step 1. Study the style guide.
Read paper-collage-vertical.md completely (the digest first, then the body) and
style_tokens.json (styles["paper-collage-vertical"] and common.*). Every rule is tagged
KEPT (unchanged from the 16:9 original), ADAPTED (changed for ExamLeaf; the "was" value
is given) or ADDED. Note:
 - Writing style: the guide's section 10 tells you which sentences are hooks, recaps or
   explanation, and which are candidates for one visual gag. You do NOT imitate it in new
   text; you only use it to choose visuals for the approved sentences.
 - Animation style: stacked zones, die-cut borders, two-layer shadows, the 13-colour
   palette, three kinds of text, motion vocabulary, transitions, determinism block,
   forbidden list.
Write style_readback.md (at most 200 words): the zone shares, the safe-box source file,
the border and shadow values, the boil rate, the font allow and ban lists, the hold
times, and the forbidden list, in your own words. It is a cheap check that you loaded
the constraints, not a deliverable for learners.
```

## Step 2: The script

**ORIGINAL →** Write a script of about 60 seconds (roughly 140-160 words) on the given topic, closely matching the writing style in the Style Guide.

**EXAMLEAF →**

```text
Step 2. USE the approved script. Never write one.
The approved script is <script_path>, SHA-256 <script_sha256>. Compute the SHA-256 of
the file bytes; if it differs, stop and write blockers.json (SCRIPT_HASH_MISMATCH).
The script came from the Super Teacher system (scriptwriter, science review, academic
approval). You may not add, remove, reorder, shorten, paraphrase or reword a single
word of narration or approved on-screen text.
Duration comes from the narration: DURATION = cue_sheet.duration. There is no word target.
Do these read-only checks and report them in beats.json, without changing anything:
 - map each sentence to a beat id and mark it "illustrative" or "data-bound";
 - words per minute = words / (speech seconds / 60) for each sentence group, against
   130-155 (ordinary), 145-165 (recap) and 105-125 (dense symbolic) from the production
   rules; flag, never fix, anything outside the band;
 - flag any sentence that cannot be one visual beat (for example, 20+ words) as a
   timing note for the script owner, without proposing replacement wording.
```

## Step 3: The storyboard

**ORIGINAL →** Using the Higgsfield MCP and the GPT Image 2.5 model, make one 3×3 grid image with nine panels covering the main beats of the script in order, in the Style Guide's art style.

**EXAMLEAF →**

```text
Step 3. Storyboard 3x3 (code thumbnails first).
Build one 3x3 grid, nine panels in beat order, each panel 9:16 (so the whole grid is
9:16), thin cream gutters, number tags added in code after rendering.
 Default (zero credits): code-rendered thumbnails using the style's own primitives
 (paper shapes, tape, doodles, placeholder cards).
 Optional (credits): Higgsfield GPT Image grid, ONLY if the human has approved it in
 writing AND a credit estimate exists in estimate.json. All Higgsfield calls go through
 examleaf-mcp-orchestrator with a per-job cap and ledger; you never call it directly.
Panels are science-free: a data-bound beat is a blank placeholder card that says, in
code, "science fixture goes here". No labels, numbers, symbols or formulae are drawn
by an image model.
Outputs: storyboard/grid.png, storyboard/beats.json, storyboard/estimate.json.
The exact request text is in 06_prompts_and_templates/storyboard_request.md.
```

## ⛔ Review checkpoint

**ORIGINAL →** Stop after the script and storyboard steps. Show the script and the storyboard grid, then wait for approval before continuing.

**EXAMLEAF →**

```text
⛔ REVIEW CHECKPOINT. STOP after Step 3.
Show: (1) the approved script's hash, unchanged; (2) the storyboard grid; (3) beats.json;
(4) estimate.json with the credit and token estimate; (5) a one-paragraph style-match
note; (6) confirmation that every panel is science-free.
Then WAIT. Do not generate voice, assets or scene code until
<workspace>storyboard/approval_record.json exists, is approved, and its script_sha256
equals <script_sha256>. Silence, or a reply that is not the approval line, is not
approval. See 06_prompts_and_templates/review_checkpoint.md for the exact wording.
```

## Step 4: The voiceover

**ORIGINAL →** After approval, generate the voiceover through the Higgsfield MCP with a preset voice named Arthur (ElevenLabs v3 through the Higgsfield text-to-speech tool) from the approved script.

**EXAMLEAF →**

```text
Step 4. Voice via the ExamLeaf TTS adapter (after approval; a pipeline step, not yours).
Voice is generated only through examleaf-voice-synthesis / examleaf-tts-provider-adapter,
with examleaf-stem-pronunciation and examleaf-multilingual-director, in the Super Teacher
delivery modes (curious, steady, deliberate, light, reassuring; focused for exam
strategy). No MCP voice, no preset "Arthur", no voice cloning, no imitation of a real
teacher. The text sent to the adapter must equal the approved script (diff it).
Think pauses and learner-controlled pauses are inserted on the timeline, never by TTS.
examleaf-alignment-localize and examleaf-cue-sheet then produce cue_sheet.json
(words with t0/t1, cues, sfx). If you are the scene agent you only CONSUME the cue sheet;
if it is missing or stale (hash mismatch), stop (CUE_SHEET_MISSING) and do not estimate.
```

## Step 5: Build the animation

**ORIGINAL →** After approval, build the video in JavaScript, replicating the Style Guide's animation as closely as possible, following the approved storyboard's scene order and content, and syncing the animation to the voiceover timing.

**EXAMLEAF →**

```text
Step 5. Build per the harness contract and sync to the cue sheet.
 - Start from 04_harness_contract/scene_template.html. Canvas 1080x1920 in fixed pixels, 30 fps.
   window.DURATION = cue_sheet.duration; async window.seek(t).
   The scene is a pure function of t: seeded stateless PRNG, finite repeats, no wall
   clock, no requestAnimationFrame, no CSS wall-clock animation. Lint with
   lint_seek_contract.js at level 2 (zero errors). Two renders must give identical frame hashes.
 - Follow the approved storyboard: same beat order, same layouts, same style.
 - Layout: stacked zones inside the safe box from vertical_safe_zones.tokens.json; side
   margin at least 96 px; captions only in the bottom zone.
 - Timing: every reveal cue's at lies in [t0 - 0.05, t0] of its word (the cue-sheet validator
   rejects later); times come from cues[].at and words[]; one sentence is one visual beat;
   nothing hard-coded.
 - Assets: tier A (code-made paper shapes) by default; tier B own/licensed art; tier C
   Higgsfield cutouts only if approved with an estimate. Every asset has a manifest
   entry (tier, licence or job ID, prompt, SHA-256). Border 6-12 px; the two-layer shadow.
 - Science: fixture strings only, in ExamLeaf tokens on an #F7F9FC tag, each element marked
   data-fx="path.to.field"; no wobble, boil, drift or camera effect on them.
 - Provide a reduced-motion variant (a flag that changes only motion).
 - At most 3 fix rounds, then stop with blockers.json.
```

## Step 6: Music and SFX (new)

**ORIGINAL →** There is no separate step; sound is described only inside the Style Guide (a whimsical track about 100 BPM, 15-20 dB under the voice, subtle paper-craft SFX, about -14 LUFS).

**EXAMLEAF →**

```text
Step 6. Music and SFX via examleaf-audio-compose (a pipeline step; your scene emits no audio).
 - Core explanation has no background music by default; the bed is allowed only in the
   hook, sheet transitions, the recap outro and Reel beds. No music under reasoning,
   derivations, predictions or think holds.
 - SFX one-shots are placed from the cue sheet sfx[] (file, at, gain_db); none during
   think, pause-video, equation reading or inspection. Your scene must have a visual
   event within one frame of every sfx[] entry; list any mismatch in scene_notes.md.
 - Music (when used): seeded Python synthesis, about 100 BPM (one bar = 2.4 s), bar-aligned
   stems, about 20 dB under the voice during narration with ducking, low-passed for
   somber beats.
 - Mix and master with examleaf-audio-production-engineer: -16 LUFS integrated (+/-1),
   true peak at most -1 dBTP, two-pass loudnorm, re-measured after the final mux (#39).
   The original -14 LUFS / -1.5 dBFS is replaced by the house target.
```

## Step 7: QA (new)

**ORIGINAL →** There is no QA step.

**EXAMLEAF →**

```text
Step 7. QA via examleaf-anim-qa (a pipeline step; you only prepare for it).
Checks: safe-zone overlay; contrast on rendered stills at cue times; hold times; flash
and luminance check; double-render frame-hash determinism; rendered text equals fixture
fields and approved script tokens (DOM text dump or OCR); border and shadow values;
caption zone clear; reduced-motion variant renders; audio LUFS and peak; caption sync.
A missing axis, label or condition, or a text/fixture mismatch, is a critical defect and
blocks release regardless of visual quality. Agents never approve; examleaf-release-review
and the human gates GA/GF/GS decide.
```

## The style guide

**ORIGINAL →** The whole Style Guide ("Paper-Cutout Storybook Collage") is appended at the end of the prompt, with twelve sections: the look; materials and surfaces; colour palette; character design; typography; pencil doodles; composition; motion language; scene transitions; writing style; sound; generating the image elements.

**EXAMLEAF →** The guide stays in its own file so that its version and hash can be recorded. The session prompt carries the reference and the digest (below, verbatim from the guide). The full guide is staged read-only in the workspace and governs on any difference.

```text
## Style: paper-collage-vertical@1.0.0
Guide (read-only): 12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md  sha256 <style_guide_sha256>
Tokens (read-only): 12_advanced_animations_with_claude/05_style_guides/style_tokens.json  sha256 <style_tokens_sha256>
Digest:
1. 1080×1920, 30 fps, flat head-on paper diorama. No 3D, gloss, photoreal, heavy blur or glow.
2. Stacked zones inside the platform-safe box: title (top), visual (middle), accessible caption (bottom). Insets come from `04_harness_contract/vertical_safe_zones.tokens.json`; never invent them. Side margin at least 96 px.
3. Cutouts: watercolour + coloured-pencil look, white die-cut border 6-12 px, two-layer shadow `0 9px 7px rgba(74,48,22,0.30)` + `0 2px 1.5px rgba(0,0,0,0.20)`.
4. 13-colour storybook palette for artwork. Science-bearing text uses ExamLeaf tokens on an `#F7F9FC` tag, never storybook colours on cream.
5. Three kinds of text only: ransom-note titles (Latin letters per tile; Indic per word), Caveat Brush punchlines (Indic: wipe per word), small labels on washi-taped tags. Short text only.
6. Motion: back.out(2-3) pops pivoting at the feet, power3.out sheets, expo.out whips, boil at 10 fps, finite repeats, seeded PRNG, seek-driven timeline. Reveals land on, or 0.05 s before, the spoken word, times read from the cue sheet.
7. Narration is the Super Teacher's (130-155 wpm, five modes), not a storybook narrator. Storybook warmth only in hooks and recaps.
8. House loudness -16 LUFS integrated, true peak at most -1 dBTP. No music under reasoning.
9. Image models never draw text, numbers, formulas or labels (#54). Number tags on storyboard grids are added in code.
10. Forbidden: infinite repeats, Math.random/Date.now, full-frame flashes, camera effects during label reveals, per-code-point Indic animation, unlicensed or scraped images, stereotypes.
Fonts allow: <fonts_allow>
Fonts ban: <fonts_ban>
```

Section map of the guide (twelve original sections, plus ExamLeaf additions): 1 look; 2 materials; 3 palette; 4 characters; 5 typography; 6 doodles; 7 composition and stacked zones; 8 motion; 9 transitions; 10 writing; 11 sound; 12 image assets; 13 Hindi/Hinglish/Assamese rules; 14 Indian setting cues and the no-stereotype rule; 15 determinism; 16 forbidden; 17 QA.

## FORBIDDEN (applies to every step)

1. Writing, editing, shortening, paraphrasing or adding narration or approved on-screen words (#11).
2. Researching, estimating or recalling facts; any science glyph without a fixture field (#12).
3. Image-model text, numbers, symbols, formulae or labelled diagrams (#54); number tags on the grid are added in code.
4. Infinite repeats (#18), wall-clock time (#15), `Math.random` or unseeded randomness (#17), `requestAnimationFrame` polling (#19).
5. Reading other folders (#9); "don't stop until it is perfect" (#60); more than 3 fix rounds.
6. Skipping or shortcutting the storyboard checkpoint (#47); calling Higgsfield without an approved estimate and ledger (#41, #42).
7. A 16:9 composition cropped into 9:16 (#49); text outside the safe box (#51).
8. Full-frame flashes (#56); camera effects during label reveals (#64).
9. Per-code-point animation of Indic text (#55).
10. Music under reasoning; unlicensed or trending audio; voice cloning.
11. Unlicensed or scraped images; a reference creator's artwork.
12. Stereotypes; shaming; fake enthusiasm; identity-based praise.
13. Ultracode; unattended high-effort loops; secrets in prompts or logs (#3, #40).

## Iteration cap and stop rules

- Storyboard: at most 2 revision rounds before the human decides [Recommendation].
- Build: at most 3 fix rounds; then write `blockers.json` (`{ "code", "message", "evidence", "needs_human": true }`) and stop.
- Cost: credits and tokens are capped by the pipeline; on a budget-exceeded signal, stop.
- Late Higgsfield results (up to about 60 s [N35]): wait, then reconcile by job ID; never retry blindly, which can double spend.

## Output manifest

`manifest.json` lists the SHA-256 of the script, cue sheet, fixtures, tokens and style files as read; every file written; assets with tier and provenance; loops used; seeds used. `scene_notes.md` lists which cue drives each reveal and which fixture field drives each on-screen value.

## Edge cases covered

#1-#4 (run settings), #7 (structured prompt), #9 (isolation), #10 (Step 6), #11 (Step 2), #12 (opening, Step 5), #15-#19 (Step 5), #39 (Step 6), #41/#42/#47 (Step 3 and checkpoint), #48 (style guide §4), #49 (Step 5), #51 (Step 5), #54 (Step 3), #55 (guide §13), #56 (guide §9), #60 (iteration cap), #63 (Step 4), #64 (Step 5).
