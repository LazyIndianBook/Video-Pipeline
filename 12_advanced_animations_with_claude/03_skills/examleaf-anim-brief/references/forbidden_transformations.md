# Forbidden transformations in an animation brief

Each row lists a transformation the scene-authoring agent must never perform, the evidence behind the ban, how `build_brief.py` or review detects it, and the legitimate path that owns the change.

| # | Forbidden | Evidence | Detection | Legitimate owner / path |
|---|---|---|---|---|
| F1 | Altering, paraphrasing, shortening or extending the approved narration or on-screen wording | [V3] AI-written script was the weak point; report §9 step 2 "the animation agent never writes or edits approved text" | Script hash bound in the manifest; regex on "rewrite/edit the script/change the wording"; QA text diff | `examleaf-super-teacher-scriptwriter` → human academic approval |
| F2 | Researching, looking up or inferring any on-screen fact | [V3] model "did its own proper research"; #12 hallucinated facts | Regex on "research/look up/search the web/find facts"; data-bound without fixtures blocks | `examleaf-claim-research`, `examleaf-science-*` → fixtures |
| F3 | Asking an image model to draw text, labels, numbers or formulas | [V4-MP] "text, tape, confetti, doodles and simple UI are built in code"; #54 | Constraint 8; storyboard gate prompts reviewed; anim-qa OCR/DOM diff | Code-built text via `examleaf-kinetic-typography` |
| F4 | Hard-coding times instead of reading the cue sheet | [V4-MP] sync rule; #63 TTS regenerated | Constraint 6; scene notes must name the cue per reveal | `examleaf-cue-sheet` |
| F5 | Wall-clock time, unseeded randomness, infinite repeats, rAF loops, `play()` | [N61][N68][N69][V4-MP]; #15–19 | `lint_seek_contract.js` errors | `examleaf-motion-harness` |
| F6 | Reading folders outside the job workspace | [V3] "do not inspect any of my older projects"; #9 | Workspace must contain the scene ID; inputs copied, not linked | Job runner |
| F7 | Unbounded iteration ("don't stop until it matches") | [V2] L3 demo prompt; [V1] ultracode run never finished; #60 | Regex; `iteration_cap` 1–3 | `examleaf-effort-governor` for exceptions |
| F8 | Using banned or convergent fonts as display faces (Inter only for labels, captions, science text by house policy) | [N51] avoid Arial and Inter; [N55] convergence on Space Grotesk; #8 | Allow/text/ban validation | `examleaf-style-guides` |
| F9 | Shortening holds below the minimum | [N60] 1.2 s; #50 | `headline_min_s` ≥ 1.2; Indic multiplier required | `examleaf-pacing-controller`, `examleaf-kinetic-typography` |
| F10 | Decorative motion that changes a taught quantity (angle, ratio, direction) or a camera effect during a measurement or label reveal | report §7.13; #64 | Constraint 7; scene notes; human review | `examleaf-procedural-2d` rules (no camera fx in measurement windows) |
| F11 | Full-frame flashes or rapid luminance changes | [V1] flash warning; #56 | Constraint 8; anim-qa flash check | `examleaf-anim-qa` |
| F12 | Reusing copyrighted reference frames as assets | Report §10.2: references are analysed only | `reference_analysis.rights == analysis_only` | `examleaf-reference-analyzer` |

## Why a regex scan is only a first line

The free-text scan catches the common hazardous phrasings. It cannot catch paraphrases ("keep polishing it forever"). Two further controls exist:
1. The constraints block is appended verbatim, so even a hazardous creative direction is contradicted by rule 10.
2. The iteration cap is enforced by the job runner and `examleaf-effort-governor`, not by the prompt. Prompt-level limits are not hard limits (compare [N34] for credits).

False positives are acceptable: a creative direction that mentions "the scientist's research lab" will block and must be reworded ("the scientist's lab"). Blocking is cheaper than an unbounded run.

## Required source evidence per brief

- Script: approval record (role `academic`) bound to the script SHA-256, as in the engine's `Approval` model (`04_video_engine/implementation_v2/src/examleaf/contracts.py`).
- Storyboard: approval record from `examleaf-anim-storyboard-gate` bound to the grid, beats and estimate hashes.
- Fixtures: produced and machine-checked by the science skills; IDs referenced, never copied into prose.
- Style: approved version of the style guide (status `approved` in the style tokens).
