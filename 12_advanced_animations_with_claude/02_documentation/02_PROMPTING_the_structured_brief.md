# 02 · Prompting: the structured brief

**Purpose.** How to instruct Claude Code so that animation quality is repeatable rather than random: the three levels from [V2] with the exact ingredients the videos use, the ExamLeaf brief structure field by field, how to describe a reference video with measured numbers, three complete worked briefs, the prompt anti-patterns, and how the brief is produced by the `examleaf-anim-brief` skill.

**Read with.** `12_advanced_animations_with_claude/06_prompts_and_templates/brief_template.md` (the fill-in template), `12_advanced_animations_with_claude/06_prompts_and_templates/negative_tests.md`, `12_advanced_animations_with_claude/03_skills/examleaf-anim-brief/SKILL.md`, doc 03 (styles) and doc 04 (contract).

**Conventions.** As in doc 00. Edge cases #1–#65 from report §8.

---

## 1. Why the brief matters more than the effort level

Three independent observations point the same way:

1. [V1]: effort changes cost steeply (about 78K tokens at low to about 625K at max for one 79 s piece) but the author still called low "still good"; the visible gains from medium to max were 3D models and movement.
2. [V2]: an L1 one-liner gives "essentially random" results; the same model with a structured prompt and a reference video gives convincing, consistent style.
3. [V3]: "If you just give it a lazy generic prompt" the result is dull; a "massive and detailed prompt" plus a reference video for pacing works.

The craft evidence explains why: Claude "defaults to safe choices unless explicitly encouraged otherwise" [N50], so unnamed fonts, palettes and motion converge on common choices [N55] (#8). The brief's job is to remove every default that matters and to fence off every action that is dangerous (facts, script, cost, other folders).

[Recommendation] Fix the brief first, then the effort. Effort for scene code is **high** by default and **xhigh** for complex 3D or physics (doc 01 §7.2); never raise effort to compensate for a vague brief.

---

## 2. The three levels in depth

### 2.1 Level 1: one-line prompt ([V2])

| Ingredient | [V2] example | ExamLeaf use |
|---|---|---|
| Idea | "Use JavaScript to animate a black hole." | Style exploration in a sandbox only |
| Constraints | none | — |
| Result | "inconsistent or frankly dumb results"; "essentially random" | Never in production (#7) |

### 2.2 Level 2: structured prompt plus references

**Ingredients named in [V2]:**

| # | Ingredient | [V2] wording (approximate, auto-captions) |
|---|---|---|
| 1 | Reference styles to match | "specific reference styles to match" |
| 2 | An actual reference video | "alongside an actual reference video" |
| 3 | Strict pacing instructions | "strict instructions on how it should handle the pacing" |
| 4 | Creative direction | "the creative direction it needs to take to keep viewers watching" |
| 5 | A highly structured prompt | "a proper, highly structured prompt" |
| 6 | Python sound and music | "create the sound and music on its own… using Python" |
| 7 | Optional harness | "hook it up to frameworks like HyperFrames or Remotion" |
| 8 | Model and effort | Opus 5.5; "extra or high"; max only if "incredibly complex" |
| 9 | Containment | "keep the model contained inside a workspace" |

**The [V2] L2 demo prompt** asked for: a short animated video "about 20 seconds long"; "use the provided video as a reference style"; "write the animation in JavaScript, matching the visual style of the reference video as closely as you can"; "compose original background music using Python. It should be pleasant"; plus a full story outline (baby deer, tiger chase, separation, butterfly guide, reunion). The critique after the first pass: "a bit flat and cartoonish", "strictly 2D… no depth"; fixed by iterating.

**Ingredients named in [V3]** (motion graphics with Remotion):

| # | Ingredient | [V3] wording (approximate) |
|---|---|---|
| 1 | Setup instruction | "download and set up the latest version of Remotion directly in the project folder" |
| 2 | Documentation research | "research Remotion's current official documentation and tools" |
| 3 | Long, detailed prompt | "a pretty massive and detailed prompt… this level of detail is crucial" |
| 4 | Reference video for pacing | "so the AI understands exactly how the pacing and timing should feel" |
| 5 | Duration and subject | 20 s; a benchmark comparison |
| 6 | Layout and typography study | "study the reference video's layout structure and its exact typography treatment" |
| 7 | Brand palette | "your own custom hex codes and branding guidelines" |
| 8 | Isolation | "not to inspect any of my older projects or folders" |
| 9 | Audio | "explicitly tell the model to generate the sound effects and background music using Python" |

### 2.3 Level 3: orchestrated production

**[V2] L3 ingredients:** the human supplies "the plan, the idea, and the reference video" and "the pacing research"; Opus writes JavaScript and uses MCP servers for clips/B-roll, studio narration and a "music studio MCP"; a harness (HyperFrames or Remotion); the demo prompt said "make it funny and engaging", "follow our usual workflow", "use the MCP servers I have connected", and "not to stop working until the animation matches the exact quality of the reference video".

**[V3] L3 ingredients:** connected MCPs (image, voice, music, Blender) and "full permission to use all the MCPs"; a 15 s educational comparison in a Vox editorial style. The visuals were strong; the AI-written script was weak.

**[V4] / [V4-MP] ingredients (the closest template for ExamLeaf):**

| # | Ingredient | [V4-MP] content |
|---|---|---|
| 1 | Topic and length | "~1-minute animated explainer"; script "About 60 seconds of narration (roughly 140–160 words)" |
| 2 | Style guide replaces reference video | "There is no reference video; the Style Guide replaces it." |
| 3 | Study step | Writing style (tone, sentence length, pacing, hooks, how facts are delivered) and animation style (visual approach, motion, transitions, typography, palette) |
| 4 | Storyboard | Higgsfield MCP, `gpt_image_2_5`, "One 3x3 grid image with 9 panels covering the main beats of the script in order" |
| 5 | Hard gate | "⛔ Review checkpoint… Stop after Steps 2 and 3… wait for my approval" |
| 6 | Voice | Higgsfield `text2speech_v2`, ElevenLabs v3 variant, preset voice "Arthur" |
| 7 | Build | "Build the video in JavaScript"; "Follow the approved storyboard"; "Sync the animation to the voiceover timing" |
| 8 | Style guide body | Look, materials, 13-colour palette, characters, three kinds of text, doodles, composition, GSAP motion vocabulary, sync rule, transitions, writing, sound, asset generation rules |
| 9 | Determinism line | "use only seeded randomness, only finite repeats, and a timeline that can jump to any frame" |

### 2.4 What ExamLeaf takes from each level

| Element | Source | ExamLeaf version |
|---|---|---|
| Reference style | [V2], [V3] | A versioned house style from `12_advanced_animations_with_claude/05_style_guides/` (doc 03) |
| Reference video | [V2], [V3] | Measured by `examleaf-reference-analyzer` into numbers (§4); video used for analysis only |
| Pacing research | [V2] L3 | `examleaf-pacing-controller` hold schedule + the cue sheet from real narration timings |
| Plan/idea | [V2] L3 | Approved lesson plan, storyboard route and beats.json (doc 05) |
| Script | [V4] step 2, [V3] | **Never the agent.** Approved script from the Super Teacher system after GA (#11) |
| Facts | [V3] "did its own proper research" | **Never the agent.** Fixtures only (#12) |
| Voice | [V4] "Arthur", [V2]/[V3] MCP voice | `examleaf-voice-synthesis` / `examleaf-tts-provider-adapter` |
| Music/SFX | [V2], [V3], [V4-MP] | `examleaf-audio-compose` stems; music rules in AD-15 |
| Storyboard gate | [V4] | Mandatory; code thumbnails first (doc 05) (#47) |
| "Don't stop until it matches" | [V2] L3 | Replaced by a 3-loop cap and a rubric (#60) |
| "Full permission to all MCPs" | [V3] | Replaced by per-job permissions (doc 05 §8) |
| Harness | [V2], [V3] | HyperFrames master timeline; contract in doc 04 |

---

## 3. The ExamLeaf brief, section by section

The brief is a Markdown file `brief.md` in the job folder (doc 01 §8). It is generated by `examleaf-anim-brief` from approved artefacts, hashed, and read-only for the job. Sections appear in this order because stable content first (style, tokens, contract) and job-specific content later maximises prompt-cache reuse across scenes (report §3.3 [Recommendation]).

### 3.1 Header and provenance

`job_id`, `lesson_id`, `scene_ids`, `route` per scene (illustrative / typographic / data-bound element inside an illustrative scene), brief version, and the SHA-256 of every input: approved script bundle, cue sheets, fixtures, style guide version, reference analysis, storyboard approval record. If any hash differs from the approval record, the job must not start (doc 05 §5).

### 3.2 Goal

One paragraph: what the viewer should understand or feel by the end of the scene, and the scene's pedagogical role (hook, analogy, recap, transition). Taken from the scene's pedagogy fields in `scenes/scene-spec.json` (`02_learning_psychology/SCENE_PEDAGOGY_SCHEMA.md`). Never adjectives alone ("stunning", "premium") [V3].

### 3.3 Audience

Class (10, 11 or 12), board (ASSEB), subject, language of narration and of on-screen text (Indian English, Hinglish in Latin script, or Hindi in Devanagari), viewing context (phone, vertical, often sound-on but captions required).

### 3.4 Duration from narration

Duration is **derived from the narration**, never chosen by the animation: `DURATION = cue_sheet.duration` and frame count = `DURATION × fps` [N72]. Reels are capped at 20–60 s (RD-19). If the scene needs more time than the narration gives (for an inspection hold), the extra time is a **protected pause** inserted by the narration timeline, not a stretch of the animation.

### 3.5 Style ID

One style from doc 03 (`paper-collage-vertical`, `doodle-handdrawn`, `editorial-vox`, `kinetic-type`, `voxel-isometric`) plus its version, or `base-science` for data-bound scenes (doc 03 §1.2). The style file is copied into `style/`; the brief quotes only the parts the scene needs (palette subset, fonts, motion verbs, transitions) to keep the prompt focused.

### 3.6 Reference analysis numbers

Measured numbers from `reference/reference_analysis.json` (§4): median shot length, cut rhythm, text-hold estimates, palette swatches, title placement. Numbers, not adjectives. If the style guide replaces a reference video (as in [V4-MP]), say so explicitly.

### 3.7 Brand tokens

Exact hex codes and roles from `02_learning_psychology/palette_and_typography_tokens.json` (base) and `12_advanced_animations_with_claude/05_style_guides/style_tokens.json` (style layer). Dominant colour plus sharp accents [N52]; one dominant highlight at a time; a quantity keeps its colour across scenes (`02_learning_psychology/palette_and_typography_tokens.json` colour rules).

### 3.8 Fonts: allow and ban

An explicit allow list with file paths in `assets/fonts/`, and an explicit ban list [N51][N55] (#8). Science text uses Inter / Noto Sans / KaTeX (RD-23). Indic text is animated per word or per grapheme cluster, never per code point (#55). Details in doc 03 §4.

### 3.9 Harness contract block

Pasted verbatim from `12_advanced_animations_with_claude/04_harness_contract/contract.md` (summary form):

```text
HARNESS CONTRACT (mandatory)
- Canvas 1080x1920, 30 fps, devicePixelRatio 1.
- Set window.DURATION (seconds) = cue sheet duration.
- Expose async window.seek(t): render the exact state at time t, resolve when drawn.
- Never call play(); never rely on requestAnimationFrame, setInterval, setTimeout,
  Date.now(), performance.now() or CSS animations/transitions for timing.
- Read all timings from cues/<scene_id>.json; never hard-code a time.
- Read all science values from fixtures/; never type a scientific value into code.
- Load fonts only from assets/fonts/ and await them before the first seek resolves.
- No network access of any kind (no CDN, no remote fonts, no fetch to http/https).
- At most one <video> element per scene; prefer PNG sequences for imported clips.
```

### 3.10 Determinism block

```text
DETERMINISM (mandatory)
- The scene is a pure function of t: seek(t) twice, or in any order, gives identical pixels.
- Randomness: only the provided stateless hash RNG rand(seed, key, step). No Math.random.
- Repeats are finite. Idle sway, boil and loops are computed from t, not accumulated.
- Physics: fixed-step replay from t=0 computed deterministically, or precomputed tables.
- The scene must pass tools/lint_seek_contract.js and tools/determinism_hash_check.py.
```

Source: [V4-MP] "use only seeded randomness, only finite repeats, and a timeline that can jump to any frame"; [N61] (contested); edge cases #15–#19.

### 3.11 Safe zones

The token names from `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` and the rule: essential text and essential diagram parts stay inside the central safe area, clear of the top status/title strip and the bottom caption/CTA/UI band (#51). Exact pixel insets come from the token file, which must be filled from measured platform screenshots (open question Q9); do not invent them in the brief.

### 3.12 Hold times

- Headlines fully readable for at least **1.2 s** before the next major transition [N60] (#50); longer for Hindi and for longer copy.
- After an important transformation or a completed diagram: **2–4 s, longer when necessary** (RD-02).
- Equations stay until narration has finished reading them, plus 0.5 s [Recommendation, report §7.5].
- Answers stay hidden until the response window ends (existing QA rule in `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §3).

### 3.13 Approved narration, sync rule and cue-sheet path (read-only)

- The approved narration text is included **for reference only**, marked read-only. The agent must not write, shorten, translate, "punch up" or re-order it (#11).
- Cue sheet path: `cues/<scene_id>.json` (schema in `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`).
- Sync rule ([V4-MP]): every reveal lands on, or about 0.05 s before, its spoken word; one sentence = one visual beat; never everything at once. At 30 fps, 0.05 s is 1.5 frames, so in practice a reveal's first visible frame is one or two frames before the word's `t0`.
- Transitions start about 0.3 s after the previous line's last word ([V4-MP]); no exit animations in the collage style (the next sheet is the exit).
- If narration is regenerated, timings change; code that reads `cues[].at` re-syncs without edits (#63).

### 3.14 Fixture paths

List every fixture file and the exact fields the scene may display, with units. Example: `fixtures/ohm_iv_10ohm.json → points[].v_volt, points[].i_amp, axis.v_max, axis.i_max, labels.*`. State which visual elements are bound to which fields. Any element not listed is decorative and must not display a number, unit, formula, label or direction that teaches science (accuracy invariant, doc 00 §5).

### 3.15 FORBIDDEN

```text
FORBIDDEN (any violation fails the job)
1. Writing, editing, shortening, translating or re-ordering narration or on-screen script text. (#11)
2. Researching, inferring or "correcting" facts; using any number, unit, label, formula or
   direction not present in fixtures/. (#12)
3. Asking an image model (or any MCP) to draw text, numbers, formulas or labelled diagrams. (#54)
4. Infinite repeats, wall-clock timing, requestAnimationFrame polling, Math.random. (#15, #17, #18, #19)
5. Reading, listing or searching any folder outside this job folder; inspecting other projects. (#9)
6. Network access, installing packages, calling MCP tools or providers. (#40–#42)
7. Full-frame flashes or rapid luminance flicker. (#56)
8. Camera shake, push-in or wobble on a science element or during its reveal. (#64)
9. Continuing beyond the fix-loop cap; "keep going until perfect". (#60)
10. Editing brief.md, fixtures/, cues/, style/, contract/, reference/ or storyboard/.
```

*15 Oct 2026 (audit M10 and science-safety-10).* Item 10 now names `contract/` and `storyboard/`. The job settings deny `Edit(./storyboard/**)` (the approval record comes only from the RD-17 approval service and is verified by the runner, RD-46), and the style guide, `style_tokens.json`, `contract.md` and the safe-zone tokens are **staged as hashed read-only copies** into `style/` and `contract/` (doc 01 §7.4 and §8.1), so the brief never asks the agent to read outside the job folder, which `Read(../**)` denies.

### 3.16 Iteration cap and stop conditions

- **3 fix loops per scene** (AD-11). One loop = edit → render preview frames at the cue times → lint → determinism check → self-review against the rubric → notes in `logs/fix_notes.md`.
- Stop and report (do not continue) when: the cap is reached; the rubric cannot be met without breaking a FORBIDDEN rule; a fixture or cue appears wrong (report it; never patch it); the token budget in the brief header is reached.
- After automated QA or render failure in the pipeline, the existing VE rule applies: at most two repair attempts, then human escalation (`07_end_to_end_pipeline_instructions/09_ROLES_humans_and_agents.md` §2.2).

**Rubric (machine items fail the loop; human items are noted for the reviewer):**

| Item | Pass condition | Checked by |
|---|---|---|
| Contract lint | 0 errors | `lint_seek_contract.js` |
| Determinism | identical hashes for forward, repeat and reverse-order renders | `determinism_hash_check.py` |
| Sync | every `reveal` cue's first visible frame within [t0 − 0.1 s, t0] | cue-frame check in anim-qa |
| Holds | §3.12 satisfied for every headline, equation and completed diagram | anim-qa |
| Safe zones | no essential element outside the safe area | anim-qa overlay |
| Fixture text | every displayed number/label equals its fixture field | DOM text dump diff |
| Flashes | no full-frame luminance flash | anim-qa flash check |
| Style adherence | palette, fonts, motion verbs as briefed | human reviewer |
| Depth | at least background / middle / subject / foreground layers where the style asks for depth ([V2] "flat" critique) | human reviewer |

### 3.17 Output format expectations

- One HTML file (or folder) per scene in `scenes/<scene_id>/`, entry `index.html`, conforming to the contract.
- No other files written outside `scenes/`, `renders/` and `logs/`.
- A `logs/scene_report.md` per scene: which fixture fields are bound to which elements; which cues drive which reveals; open issues.
- If a helper tool expects a specific output format (for example a fenced `html` block parsed by a script), the brief states it exactly; [N56] (contested) shows a parser that "depends on this format" (#53). ExamLeaf's harness reads files, not chat output, which avoids this failure.

---

## 4. Describing a reference video from the analyzer JSON

### 4.1 Why numbers

[V3] stresses studying "layout structure and its exact typography treatment"; the model cannot watch a video natively, and adjectives drift. `examleaf-reference-analyzer` turns a reference into numbers with FFmpeg/ffprobe (report §7.10, standard usage, verify on your build) and the brief quotes the numbers.

### 4.2 Measurements (standard FFmpeg usage; the script is `12_advanced_animations_with_claude/04_harness_contract/reference_analysis.sh`)

```sh
# Duration, frame rate, size
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate:format=duration \
  -of json reference.mp4

# Shot changes: scene-change score above a threshold, with timestamps from showinfo
ffmpeg -i reference.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2> scenes.log

# One still per detected shot for palette and typography study (timestamps from scenes.log)
ffmpeg -ss <t> -i reference.mp4 -frames:v 1 stills/shot_<n>.png
```

Notes: the 0.3 threshold is a starting value [Hypothesis]; tune per style (collage cuts are hard; doodle boil can trigger false cuts). Variable-frame-rate references report different `r_frame_rate` and `avg_frame_rate`: record both. Letterboxed 16:9 references inside a 9:16 frame (or the reverse) must be detected and cropped for palette analysis only.

### 4.3 Example analyzer output (illustrative numbers, not a measurement)

```json
{
  "reference_id": "ref-doodle-001",
  "usage": "analysis_only",
  "source_aspect": "16:9",
  "letterbox_detected": false,
  "fps": {"r_frame_rate": "30/1", "avg_frame_rate": "30/1", "variable": false},
  "duration_s": 21.4,
  "shots": {"count": 9, "median_s": 2.3, "p10_s": 1.1, "p90_s": 3.6},
  "cuts_per_10s": 4.2,
  "text_holds_s": {"median": 1.6, "min": 0.9},
  "title_position": "upper third",
  "palette": [
    {"hex": "#F3ECDF", "share": 0.46},
    {"hex": "#2B2622", "share": 0.12},
    {"hex": "#D9483B", "share": 0.05}
  ],
  "stills": ["stills/shot_01.png", "stills/shot_02.png"]
}
```

### 4.4 Turning the JSON into brief prose

| JSON field | Brief sentence pattern | Caveat |
|---|---|---|
| `shots.median_s`, `p10/p90` | "Hold each visual idea about 2.3 s (range 1.1–3.6 s); never cut faster than the narration's sentence rhythm." | Narration timing wins; cuts follow sentences, not the reference |
| `cuts_per_10s` | "About four visual changes per 10 s in the hook; fewer in explanation." | Learning-psychology motion budget (25–35% of runtime) still applies to lessons |
| `text_holds_s.min` | "Our minimum is 1.2 s [N60], above the reference's 0.9 s." | Never copy a hold below the house minimum (#50) |
| `title_position` | "Title in the upper third, inside the safe area token `title_band`." | Re-laid out for 9:16 (#49) |
| `palette` | "Dominant cream paper, ink outlines, tomato accent used sparingly." | Use house tokens; the reference palette only guides proportions |
| `source_aspect: 16:9` | "Recompose for 1080×1920 using the vertical layout rules; never crop." | doc 03 §3 |

**Copyright.** A reference video is analysed, never copied: no frames, cutouts, music or characters from it enter an ExamLeaf asset (report §10 skill 2).

---

## 5. Worked briefs

The three briefs below show the full structure. Values in fixtures are shown only to illustrate what the agent receives; the real values come from the validated fixture files. Narration excerpts are **placeholders**: the real text comes from `examleaf-super-teacher-scriptwriter` after academic approval.

### 5.1 Worked brief (a): 30 s doodle-style refraction hook Reel

```markdown
# BRIEF · job phy10-refraction-reel-01 · v1
## 3.1 Header
lesson_id: asseb-c10-phy-light-refraction · scenes: s01 hook, s02 question, s03 ray, s04 payoff, s05 cta
routes: s01 illustrative · s02 typographic · s03 illustrative WITH data-bound element (ray geometry)
        · s04 typographic · s05 typographic
inputs (sha256): script_bundle=<…> cues/*=<…> fixtures/refraction_air_water.json=<…>
                 style/doodle-handdrawn.md v1=<…> reference_analysis=<…> storyboard_approval=<…>
model: <pinned Opus 5.5 ID> · effort: high · fix-loop cap: 3 · token budget: <from estimate.json>

## 3.2 Goal
Hook: a pencil in a glass of water looks broken. Viewer wonders why, then sees that light
changes direction at the air–water boundary and bends toward the normal. Complete payoff
inside the Reel, then one CTA to the free refraction lesson.

## 3.3 Audience
ASSEB Class 10 Physics; phone, vertical; Hinglish narration (Latin-script on-screen text).

## 3.4 Duration
DURATION = cues/reel.json duration (≈30 s). Reel cap 20–60 s (RD-19). Do not stretch.

## 3.5 Style
doodle-handdrawn v1: seeded wobble strokes, stroke-dash draw-on, boil at 9 fps, flat fills,
pencil texture overlay; parallax layers (paper bg / table / glass / pencil / foreground doodles).

## 3.6 Reference numbers
Style guide replaces a reference video for look; pacing from reference_analysis.json:
median shot 2.3 s, ~4 visual changes per 10 s in the hook, title upper third.

## 3.7 Tokens
Base: background #F7F9FC, ink #14213D, blue #185ABD (light ray — the SAME blue in every
scene), amber #9A5B00 (normal line). Style layer per style_tokens.json "doodle". One dominant
highlight at a time.

## 3.8 Fonts
Allow: Patrick Hand (doodle labels), Caveat Brush (one hand-lettered question),
Inter Semibold (science labels i, r, "normal"). Ban: Arial, Space Grotesk, Inter as display.

## 3.9–3.10 Contract + determinism blocks (verbatim, see contract.md)

## 3.11 Safe zones
Use tokens title_band, content_safe, caption_band from vertical_safe_zones.tokens.json.
Ray diagram fully inside content_safe; captions never cover the glass–water boundary.

## 3.12 Holds
Question title ≥1.2 s. Completed ray diagram (s03) held 2–4 s before s04.

## 3.13 Narration (READ-ONLY) and sync
Placeholder excerpt (real text from the approved script):
  s01 "Pencil seedha hai… phir yeh toota kyun dikh raha hai?"
  s03 "Light hawa se paani mein jaati hai — aur mud jaati hai, normal ki taraf."
Cue sheet: cues/s01.json … cues/s05.json. Each reveal lands on, or ≤0.05 s before, its word.
Doodle strokes for the ray start drawing at cue ray_incident.at and finish by ray_refracted.at.

## 3.14 Fixtures
fixtures/refraction_air_water.json:
  n1 (air), n2 (water), theta_i_deg, theta_r_deg (computed by the science validator),
  boundary_y_frac (where the water surface sits in the glass drawing)
Bound elements: incident ray angle = theta_i_deg from the normal; refracted ray angle =
theta_r_deg; normal is perpendicular to the boundary; labels "i", "r", "normal".
Example of what you will receive (illustrative): {"n1":1.00,"n2":1.33,"theta_i_deg":45.0,
"theta_r_deg":32.1}. Do NOT compute or round angles yourself; read them.

## 3.15 FORBIDDEN (verbatim list) + scene-specific:
- No wobble, boil, shake or push-in on the rays, the normal or the boundary, ever (#64).
- The apparent "break" of the pencil is illustrative; the rays are science.

## 3.16 Cap: 3 fix loops; rubric as in brief template.

## 3.17 Output
scenes/s01…s05/index.html; logs/scene_report.md mapping each fixture field to its element.
Audio: none in scene code. The audio bed (Reel: allowed under hook and CTA only) and SFX
(pencil scratch, soft pop on labels) are produced by examleaf-audio-compose and placed by
the cue sheet.
```

**Why this brief is shaped this way.**
- The hook is illustrative, but the ray is science; the brief splits them explicitly (doc 00 §5). The direction "toward the normal when entering water" is exactly the kind of fact decoration must not contradict (report §7.13).
- The blue used for the light ray is fixed across all scenes because a quantity keeps its colour (`02_learning_psychology/palette_and_typography_tokens.json`).
- The Reel music rule follows section 11's playbook table (bed allowed under hook and CTA for Reels).
- Edge cases covered: #7, #8, #11, #12, #15–#18, #49–#51, #54, #60, #63, #64.

### 5.2 Worked brief (b): data-bound Ohm's-law graph scene

Context: the 600-second Ohm's-law blueprint (`02_learning_psychology/BLUEPRINT_600_second_ohms_law_lesson.md`) uses the same 10 Ω resistor; 2 V → 0.2 A; 4 V → 0.4 A revealed after silence; plotted points give slope 0.1 A/V = 1/R; a second, steeper line for a smaller resistance whose value the script must choose; axes and scale stay fixed.

**Routing note.** Data-bound scenes normally go to `examleaf-svg-scenes` or `examleaf-manim-scenes`. This brief shows the case where the graph is built in the HyperFrames timeline by `examleaf-motion-harness`; the rules are identical either way.

```markdown
# BRIEF · job phy10-ohm-graph-01 · v1
## 3.1 Header
lesson_id: asseb-c10-phy-ohms-law · scene: s07 iv-graph · route: data-bound (whole scene)
inputs (sha256): fixtures/ohm_iv.json=<…> cues/s07.json=<…> interactions.json=<…>
model: <pinned Opus 5.5 ID> · effort: high · cap: 3

## 3.2 Goal
Students see that plotting (V, I) pairs for the same resistor gives a straight line through
the origin whose slope is 1/R, then predict before the answer appears.

## 3.3 Audience
ASSEB Class 10 Physics; Indian English narration; phone, vertical.

## 3.4 Duration
DURATION = cues/s07.json duration, INCLUDING the protected prediction pause already in the
timeline. Never shorten the pause.

## 3.5 Style
base-science (doc 03 §1.2): light theme, no illustrative decoration, no idle motion,
no camera moves. Motion only for semantic changes (point appears, line draws, highlight).

## 3.7 Tokens
background #F7F9FC, ink #14213D, blue #185ABD = current I (same blue as earlier scenes),
teal #087986 = second resistor line, amber #9A5B00 = the "constant temperature" condition tag.
Lines distinguished by label AND dash pattern, not colour alone.

## 3.8 Fonts
Inter (labels, units), KaTeX fonts (I = V/R). Essential labels ≥ ~50 px source on the
1080-wide master (RD-18 derivation). Check I/l/1 and O/0 legibility.

## 3.11 Safe zones
Graph inside content_safe; axis titles and units never in caption_band.

## 3.12 Holds
After the line is complete: 2–4 s (RD-02). Equation stays until narration finishes it + 0.5 s.

## 3.13 Narration (READ-ONLY) and sync
Cues used: pt_2V (reveal point 1), pt_4V_question (show 4 V tick and "?"),
answer_04A (reveal 0.4 A — MUST NOT appear before this cue; interactions.json answers_after),
line_draw, slope_label, second_line.

## 3.14 Fixtures
fixtures/ohm_iv.json:
  resistor_a.r_ohm, resistor_a.points[] {v_volt, i_amp}
  resistor_b.r_ohm, resistor_b.points[]  (value chosen in the approved script)
  axis.v_min, axis.v_max, axis.v_step, axis.i_min, axis.i_max, axis.i_step, axis.units
  labels.v_axis, labels.i_axis, labels.condition
Every tick, number, unit, point, line endpoint, slope label and condition tag comes from
these fields. Axes and scale do not change during the scene.

## 3.15 FORBIDDEN (verbatim) + scene-specific:
- No push-in, shake, wobble, parallax or idle sway anywhere in this scene (#64).
- Do not extrapolate the line beyond the fixture's points unless axis/line_extent says so.
- Do not draw the non-ohmic curve here (separate approved scene).

## 3.17 Output
scenes/s07/index.html; logs/scene_report.md listing each displayed string and its fixture
field (used by anim-qa's DOM-text diff).
```

**Why.** Everything a student could copy into an exam answer is fixture-bound. The answer-hiding cue enforces the existing QA rule "Answer hidden until the window ends". The ban on camera effects implements #64. Colour is never the only cue (existing visual QA rule). Edge cases covered: #12, #15–#18, #50, #51, #63, #64.

### 5.3 Worked brief (c): paper-collage history-of-science recap

Topic: a 40 s recap segment at the end of a Class 11 "structure of atom" lesson: the gold-foil experiment and what it showed. Facts on screen (years, "most alpha particles passed straight through", "a few bounced back") must exist as approved claims.

```markdown
# BRIEF · job chem11-atom-recap-collage-01 · v1
## 3.1 Header
lesson_id: asseb-c11-chem-structure-of-atom · scenes: r01–r05 · route: illustrative
inputs (sha256): script_bundle=<…> fixtures/rutherford_recap.json=<…> cues/r0*.json=<…>
                 assets/asset_manifest.json=<…> (cutouts approved at the storyboard gate)
                 style/paper-collage-vertical.md v1=<…> hero/hero_canonical.png=<…>
model: <pinned Opus 5.5 ID> · effort: high · cap: 3

## 3.2 Goal
A warm, wry storybook recap that leaves one picture in memory: tiny particles fired at thin
gold foil; almost all pass through; a few bounce back; so the atom's mass sits in a tiny
nucleus. Ends on the lesson's opening question.

## 3.3 Audience
ASSEB Class 11 Chemistry; Hinglish narration; on-screen text in Latin script.
A Hindi version will reuse the scene with Devanagari tiles (per-word, not per-letter).

## 3.4 Duration
≈40 s from cues; one sentence = one visual beat.

## 3.5 Style
paper-collage-vertical v1 (adapted from [V4-MP]): cutouts with 6–12 px white die-cut border
(scale to the 1080-wide canvas per style file), two-layer warm shadow, cream watercolour and
kraft backgrounds ONLY (no night-navy or charcoal sheets in this lesson: light theme, RD-27),
torn-paper strips, washi tape, doodles 3–5 px. Paper-sheet transitions slide in from bottom
or top (vertical), 0.5–0.7 s power3.out. NO white flash.

## 3.6 Reference numbers
Style guide replaces the reference video. Pacing: one beat per sentence; ransom letters
0.04–0.05 s apart (1–2 frames at 30 fps).

## 3.7 Tokens
Collage palette from style_tokens.json "paper_collage" (tomato, mustard, teal, ultramarine,
olive, sage, blush, cream, paper white, kraft, ink, pencil). Gold foil = mustard family;
alpha particles = tomato. Contrast of any text tile ≥ 4.5:1.

## 3.8 Fonts
Ransom tiles: rotate among the allowed display list in the style file (Latin only);
captions: Caveat Brush; tags: Patrick Hand. Science words on tags ("nucleus", "α particle"):
Noto Sans/Inter for the Greek letter. Ban: Arial, Space Grotesk.

## 3.9–3.10 Contract + determinism (verbatim). Boil at 8–10 fps via rand(seed,id,floor(t*9)).

## 3.11 Safe zones
Ransom title in title_band; hero character bottom-left INSIDE content_safe (not in
caption_band); taped "photos" stacked vertically in the middle band.

## 3.13 Narration (READ-ONLY) and sync
Placeholder excerpt: r02 "Thin gold foil. Tiny particles. Fire!" — each noun's cutout pops on
its word (back.out(2–3), pivot at the base). Transitions begin ≈0.3 s after the previous
line's last word.

## 3.14 Fixtures
fixtures/rutherford_recap.json: claims[] {claim_id, display_text, year?} approved at GA.
Every on-screen fact string (any year, any "most/few" statement) = claims[].display_text,
verbatim. The scientist is shown as a generic paper character with a code-built name tag
taken from the fixture; no likeness portrait.

## 3.15 FORBIDDEN (verbatim) + scene-specific:
- No text inside any raster asset; all titles, tags and numbers are DOM/SVG text.
- Do not invent extra particle-path statistics; the "few bounce back" count is shown as a
  small handful of particles, not as a number, unless the fixture provides one.
- Idle sway and boil allowed on characters and props, never on claim tags while being read.

## 3.17 Output
scenes/r01…r05/index.html; logs/scene_report.md. Audio: no music under the recap narration
(lesson rule); subtle paper SFX on pops and tears via the cue sheet; music swell only on the
end card.
```

**Why.** The collage look comes from approved raster cutouts, but every word on screen is code text tied to an approved claim (#54, #12). Dark sheets are excluded because the project is light-theme-only at launch (RD-27). Ransom tiles are per word for Hindi (#55). Credit cost was approved at the storyboard gate before any cutout was generated (#41, #47). Character consistency uses the canonical hero image as a reference (#48). Edge cases covered: #11, #12, #17, #18, #41, #47–#49, #54–#56, #63.

---

## 6. Prompt anti-patterns

| Anti-pattern | What goes wrong | Do instead | Edge case |
|---|---|---|---|
| "Make it stunning / premium" with no specifics | Generic, safe defaults [N50] | Style ID, tokens, measured reference numbers | #7, #8 |
| One-line prompt in production | Random quality | Full brief | #7 |
| No font named | Inter/Arial/Space Grotesk convergence [N51][N55] | Allow + ban list | #8 |
| "Write a script about…" to the animation agent | Weak, unapproved text ([V3]) | Approved script, read-only | #11 |
| "Research the facts" / "check the latest numbers" | Hallucinated or unapproved on-screen facts | Fixtures only | #12 |
| "Don't stop until it matches the reference" | Endless loops and cost ([V2] demo; [V1] ultracode) | 3-loop cap + rubric | #60 |
| "Use all connected MCPs" | Unbudgeted credits; no cap [N34] | Per-job permissions; ledger | #41, #42 |
| Hard-coded times ("at 3.2 s show…") | Desync after TTS regeneration | Cue IDs from the cue sheet | #63 |
| "Animate letter by letter" for Hindi or Assamese | Broken conjuncts | Per word or grapheme cluster | #55 |
| "Loop forever", "repeat: -1" | Seek states inconsistent | Finite repeats from t | #18 |
| "Add random sparkles" without a seed | Frames differ between renders | Stateless seeded RNG | #17 |
| "Make the logo spin using requestAnimationFrame" | Render hangs or freezes | Pure function of t | #15, #19 |
| "Generate a labelled diagram of the eye" (image model) | Misspelled labels, wrong anatomy | Code-built labels on an approved diagram | #54 |
| "Look at my other projects for inspiration" | Context contamination ([V3]) | Isolated job folder | #9 |
| "Use the music from the reference" | Copyright; [V1]'s song was a library track | Owned/generated audio only | — |
| "Shake the screen when the graph appears" | Misread geometry | No camera fx on science | #64 |
| "Flash white on the explosion" ([V4-MP] variation) | Photosensitivity risk | Non-flash transition | #56 |
| "Make it photoreal" | Not a text-to-video model [N62] | Redesign in a code style | #52 |
| "Output the HTML in chat" when a parser expects a fence | Helper error [N56] | File output in `scenes/` | #53 |
| Effort left unset | Medium default on 5.5 [N22] | Explicit effort | #1 |

---

## 7. How the brief feeds `examleaf-anim-brief`

### 7.1 Inputs → outputs

| Input | From | Used for brief section |
|---|---|---|
| Approved script bundle hash and per-scene text | GA approval; `lessons/<…>/script/approved-script.txt` | 3.1, 3.13 |
| Scene spec + pedagogy fields + route | `lessons/<…>/scenes/scene-spec.json` | 3.1, 3.2 |
| Cue sheets | `examleaf-cue-sheet` | 3.4, 3.13 |
| Fixtures (validated) | `lessons/<…>/science/verified-model.json` → staged copies | 3.14 |
| Style guide + tokens | `12_advanced_animations_with_claude/05_style_guides/` | 3.5, 3.7, 3.8 |
| Reference analysis | `examleaf-reference-analyzer` | 3.6 |
| Safe-zone tokens | `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` | 3.11 |
| Hold schedule | `examleaf-pacing-controller` | 3.12 |
| Model/effort/cap/budget | `examleaf-effort-governor` and `estimate.json` | 3.1, 3.16 |
| Storyboard approval record | `examleaf-anim-storyboard-gate` | 3.1 |

**Outputs:** `brief.md`, `brief.sha256`, the job's `CLAUDE.md` (rules subset), and the staged job folder (doc 01 §8).

### 7.2 Procedure

1. Refuse to build a brief if the script bundle lacks GA approval or the storyboard approval is missing or its hashes differ.
2. Fill sections 3.1–3.17 from the inputs above; paste the contract and determinism blocks verbatim from `12_advanced_animations_with_claude/04_harness_contract/contract.md`.
3. Run the brief linter (in the skill's `scripts/`): every FORBIDDEN item present; no adjective-only goal; at least one fixture field per data-bound element; fonts allow and ban lists non-empty; effort explicit and not `ultracode`; fix-loop cap present; no absolute time literals in the narrative sections; no secrets.
4. Hash and lock the brief; write it to the job folder.
5. Log the brief hash in `estimate.json` and in the job's `logs/run.json`.

### 7.3 Changes after approval

- A change to style, assets, scene count or fixtures is **material**: it produces a new brief hash and invalidates the storyboard approval (doc 05 §5).
- Fix-loop notes never edit the brief; they go to `logs/fix_notes.md`.
- A narration regeneration changes cue sheets: rebuild cues, re-hash, re-render; scene code does not change (#63). If the new duration changes beat structure, return to the storyboard gate.

---

## 8. Checklist before launching a job

- [ ] GA-approved script bundle hash matches the brief header.
- [ ] Storyboard approval record present and hashes match (doc 05 §5): both roles (founder, academic lead) approved, fixture/style/hero hashes bound, verified by the runner against the RD-17 service (15 Oct 2026).
- [ ] Style ID and version set; tokens and fonts copied into the job folder.
- [ ] Fixture fields listed for every science element; fixtures read-only.
- [ ] Cue sheets present, units in seconds, durations match narration (#33, #35).
- [ ] Contract and determinism blocks pasted verbatim.
- [ ] FORBIDDEN list complete; fix-loop cap 3; token budget set.
- [ ] Model ID pinned; effort high (or xhigh with reason); never ultracode (#1, #3, #6).
- [ ] Job folder permissions tested (denied read outside the folder) (#9); `Edit(./storyboard/**)` denied; style and contract files staged with `MANIFEST.sha256` (15 Oct 2026).
- [ ] No provider keys in the session environment (#40).
