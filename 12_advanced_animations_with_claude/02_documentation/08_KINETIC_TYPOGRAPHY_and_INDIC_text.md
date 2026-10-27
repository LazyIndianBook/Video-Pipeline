# 08 · Kinetic typography and Indic text

**Purpose.** How on-screen words are timed, styled and moved in ExamLeaf animations — including Hindi (Devanagari) and Assamese (Bengali–Assamese script) — without breaking legibility, scientific accuracy, captions or the house rules. Expands report §4.4, §7.1–§7.9 and edge cases #50, #51, #55.

**Status.** [PROPOSED]. Indic shaping and per-cluster animation in headless Chrome are **untested** (report §11 item 10). Every Indic statement here is a [Hypothesis] until the pilot test in §7.6 passes. Font names come from [V4-MP] or project tokens; their licences must be verified one by one.

**Evidence conventions.** As in `12_advanced_animations_with_claude/01_research/RESEARCH_REPORT_advanced_animations_with_claude.md`: [V#], [V4-MP], [N#], ROOT-relative project paths, [Recommendation]/[Hypothesis], master edge cases #1–#65, NEW-# in `12_advanced_animations_with_claude/02_documentation/12_EDGE_CASES_master_table.md`.

**Owning skill.** `12_advanced_animations_with_claude/03_skills/examleaf-kinetic-typography/`. Related: `12_advanced_animations_with_claude/03_skills/examleaf-style-guides/` (fonts and palettes per style), `12_advanced_animations_with_claude/03_skills/examleaf-vertical-adapt/` (layout), `12_advanced_animations_with_claude/03_skills/examleaf-cue-sheet/` (timing), and the existing caption owner `examleaf-speech-animation-synchronizer` (`06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 9). Tokens: `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`, `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`.

---

## 0. Summary

1. **Two text layers, never mixed.** *Science text* (labels, values, units, equations) is fixture-bound, set in the house fonts, and moves little. *Expressive text* (hook questions, titles, punchline words, CTA) may use distinctive fonts and kinetic modes.
2. **Timing comes from the cue sheet's `words[]`.** A word's reveal lands on, or about 0.05 s before, the spoken word ([V4-MP]).
3. **Three expressive modes** from [V4-MP]: ransom-note tiles, handwriting, labels on tags.
4. **One orchestrated staggered entrance** per layout, not scattered micro-animations [N53].
5. **Distinctive fonts with an explicit ban list** [N51][N55]; dominant colour plus sharp accents [N52].
6. **Holds:** headlines ≥ 1.2 s fully readable [N60], longer for Hindi and longer copy (#50); equations until the narration finishes plus 0.5 s; 2–4 s after an important transformation (RD-02).
7. **Indic scripts animate per word or per verified grapheme cluster, never per code point** (#55) [Hypothesis].
8. **Captions are separate**, live in a protected area, and kinetic text never enters it (#51).

---

## 1. House constraints that override reference practice

| Topic | Reference practice | House constraint | Source |
|---|---|---|---|
| Letter-by-letter text | Ransom letters "slap on one at a time (about 0.04–0.05 s apart), synced to the spoken words"; handwriting "revealed letter by letter" ([V4-MP] §5) | "Avoid … syllable-by-syllable karaoke text"; avoid full narration paragraph + animated diagram + equation + moving karaoke captions at once | `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S8 visual rules; `02_learning_psychology/INSTRUCTIONS_production_rules.md` D7 |
| Fonts | Distinctive display fonts; avoid Arial and Inter [N51] | Production: **Inter + Noto Sans + KaTeX**, vendored, licence recorded, hashed into cache key | RD-23 in `07_end_to_end_pipeline_instructions/10_DECISIONS_and_CONFLICT_RESOLUTIONS.md` |
| Text size | ~90 px from edges on 1920×1080 ([V4-MP] §5) | Essential labels on a 1080-wide vertical master ≥ ≈ 50 px source (derived: 16.5 px display × 1080/360) | RD-18 |
| Theme | Warm paper palettes; dark sheets for somber beats ([V4-MP] §3, §9) | Light theme only at launch; text contrast ≥ 4.5:1, essential graphics ≥ 3:1 on actual frames; dark mood sheets only under the narrow exception proposed in AD-17 (no essential science text), pending founder acceptance | RD-27; `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §3; `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md` AD-17 |
| Emphasis | Many simultaneous pops in demos | One dominant highlight at a time | `02_learning_psychology/INSTRUCTIONS_production_rules.md` D4 |
| Motion | GSAP vocabulary; snappy | Transition 150–300 ms; highlight 300–600 ms; equation transform 0.8–1.5 s | `02_learning_psychology/palette_and_typography_tokens.json` `timing_defaults` |

**Resolution** [Recommendation]:
- Per-letter or per-tile staging is allowed **only** for short expressive text: a hook title (≤ 6 words), a single number, a punchline word, a CTA. It is never used for narration sentences, captions, labels or equations. Those appear whole, or per word.
- The [N51] advice "avoid generic fonts like Arial and Inter" applies to the **expressive layer**. The **science layer** keeps Inter + Noto Sans + KaTeX because RD-23 chose them for legibility, licence clarity and script coverage. This is a recorded conflict; see §4.3 and AD-14 / C5 in `12_advanced_animations_with_claude/02_documentation/14_DECISIONS_and_OPEN_QUESTIONS.md`.

---

## 2. The two layers

| | Science text | Expressive text |
|---|---|---|
| Content | Labels, values, units, axis titles, equations, conditions ("same voltage") | Hook question, title, punchline word, CTA, playful tags |
| Source | **Fixture fields only** (accuracy invariant, report §9) | Approved script (GA) and the brief |
| Fonts | Inter, Noto Sans script families, KaTeX (RD-23) | Style-guide display fonts (§4) with Indic pairings |
| Motion | Appear, highlight, transform with symbol correspondence; no wobble, no rotation | Ransom, handwriting, label modes; seeded rotation/jitter |
| Size | Essential ≥ ≈ 50 px on 1080-wide master (RD-18); equations larger | Hook titles large; still checked at 360 px display |
| QA | DOM text diff against fixture (#12) | Spelling vs approved script; hold-time; safe zone |

Never set a scientific value in an expressive mode. "4 V" in a ransom-note tile with a random ±6° tilt is still a scientific value; it belongs to the science layer [Recommendation].

---

## 3. Timing from the cue sheet

### 3.1 Inputs

`words[]` (`{w, t0, t1}`) and `cues[]` from `anim/<scene_id>/cue_sheet.json` (schema: `12_advanced_animations_with_claude/04_harness_contract/cue_sheet.schema.json`; procedure: `12_advanced_animations_with_claude/02_documentation/06_AUDIO_compose_analyze_sync.md` §5). Scene code never hard-codes times (#63).

### 3.2 Word-level reveal

For a text element tied to word `k`:
```
reveal_at = words[k].t0 − 0.05 s      (template default; any value in [t0 − 0.05, t0] is valid)
fully readable by reveal_at + entrance_s
```
Times are continuous seconds; scene code compares them with a small tolerance and never snaps to frames (`12_advanced_animations_with_claude/04_harness_contract/contract.md` §7–§8). `entrance_s` follows the house transition range (150–300 ms). Answer reveals use offset 0 (doc 06 §5.3 step 6).

### 3.3 Staggered sub-units inside a word or title

For ransom tiles or handwriting strokes inside one word:
1. Split the word into **units** (§7: grapheme clusters for Latin; words or verified clusters for Indic).
2. Stagger units by `Δ` = 0.04–0.05 s ([V4-MP] §5; tokens `ransom_letter_stagger_s`). At 30 fps that is 1.2–1.5 frames, so successive tiles appear on alternating 1- and 2-frame gaps once the harness samples at `i / fps`; keep `Δ` in seconds and let sampling decide the frame.
3. **Clamp:** the last unit must land no later than `words[k].t1` (the end of the spoken word). If `n_units × Δ` exceeds the word length, shrink `Δ` to `(t1 − t0) / n_units` with a floor of one frame time (1/30 s); if still too long, reveal per word.
4. For a multi-word title spoken as a phrase, distribute per word first, then per unit inside each word.

### 3.4 Exit and transitions

[V4-MP] §9: "No exit animations: the next sheet is the exit", and each incoming sheet starts about 0.3 s after the previous line's last word. Expressive text therefore leaves with its scene sheet. Science text that must remain for inspection stays until its hold ends (§6).

---

## 4. Modes, fonts and palette

### 4.1 Expressive modes from [V4-MP] §5

| Mode | Look | Motion | Sound | Indic note [Hypothesis] |
|---|---|---|---|---|
| **Ransom-note tiles** | Each letter on its own paper square; tile colour and font vary; ±6° rotation, slight vertical jitter, small shadow; some letters lowercase | Pop-in per tile, back.out(2–3) overshoot; stagger 0.04–0.05 s | Light tap per tile (`12_advanced_animations_with_claude/02_documentation/06_AUDIO_compose_analyze_sync.md` §3.5) | Split per **word** for Devanagari and Bengali–Assamese, one word per tile; per-letter tiles would break conjuncts (§7) |
| **Handwriting** | "Caveat Brush" in ink #2b2622, often with a red pencil double underline drawing on in two wobbly strokes | Mask wipe left→right across the shaped word, like a pen | Pencil scratch | Wipe a shaped word with a mask; never insert characters one at a time |
| **Labels on tags** | "Patrick Hand" on cream paper tags held by washi tape; optional red check mark or circle drawing on | Tag drops in with a small bounce; idle sway with finite repeats | Pop or tap | Label text from the fixture uses the science font if it is a scientific label |

Tile styles ([V4-MP] §5): black with cream or mustard letters; cream with red or black; red with cream; ultramarine with mustard; mustard with black; pink with dark red or blue; red polka-dot; blue grid-paper; teal with cream. Each tile pair must pass the contrast check on the actual frame (NEW-31).

### 4.2 Display fonts named in [V4-MP]

Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One (ransom); Caveat Brush (handwriting); Patrick Hand (labels).

**Rules for using them** [Recommendation]:
1. **Licence check per font** before vendoring (NEW-2). Do not assume a licence because a font is free to download; record licence, source URL, version and file hash in the asset ledger. (The engine docs make the same point about GSAP: free to use does not mean MIT, `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14.)
2. **Vendor locally.** "No uncontrolled network fonts or remote media dependencies during final rendering" (`04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §14). A network font that fails silently falls back to a system font and changes metrics (NEW-16).
3. **Latin-only coverage.** None of these is assumed to contain Devanagari or Bengali–Assamese glyphs. Each style guide pairs every Latin display font with an Indic font for the same role (`12_advanced_animations_with_claude/05_style_guides/`), verified for coverage (§5).
4. **Rotate and ban.** Repeated generations converge on the same choices, e.g. Space Grotesk [N55]. Each style guide keeps an allow list and a ban list; the brief passes both to the scene agent (`12_advanced_animations_with_claude/03_skills/examleaf-anim-brief/`).

### 4.3 Ban list and the Inter conflict

| Font | Expressive layer | Science layer | Basis |
|---|---|---|---|
| Arial | **Banned** | Not used | [N51] |
| Inter | **Banned** | **Required** (RD-23) | [N51] vs RD-23 — recorded conflict, resolved by layer |
| Space Grotesk | **Banned** (convergence example) | Not used | [N55] |
| System default / unspecified | **Banned** | **Banned** | [N50]: Claude "defaults to safe choices unless explicitly encouraged otherwise" |
| Any font without a recorded licence | **Banned** | **Banned** | NEW-2 |

Add further convergent fonts to the ban list when the pilot sees them recur across scenes [Recommendation].

### 4.4 Colour

"Dominant colors with sharp accents outperform timid, evenly-distributed palettes" [N52]. Encode per style in `style_tokens.json`: one dominant background, one ink, two accents, plus the subject colours (report §7.2). In science text, keep a quantity's colour stable across scenes and never encode meaning by colour alone (`02_learning_psychology/INSTRUCTIONS_production_rules.md` D4). The house light palette (`02_learning_psychology/palette_and_typography_tokens.json`) is the default for science text; collage palettes ([V4-MP] §3) apply to the expressive layer and must pass contrast on real frames.

### 4.5 One orchestrated staggered entrance

[N53]: "one well-orchestrated page load with staggered reveals" beats scattered micro-interactions. For each layout:
1. Decide the entrance order from the narration: the elements appear in the order they are spoken.
2. Use one easing family for the entrance (e.g. back.out for pops, power3.out for slides — [V4-MP] §8).
3. After the entrance, only semantic changes move (`02_learning_psychology/INSTRUCTIONS_production_rules.md` E3: classify each change as layout, semantic or decorative; remove decorative change).
4. Idle motion, if any, uses finite repeats and small amplitudes ([V4-MP] §8: ±1.5–4°, a few px) and **never** applies to science text.

---

## 5. Font loading and glyph checks

### 5.1 Preload before the first seek

1. Declare each vendored font with `@font-face` pointing to a local file (`url("fonts/…")`; no CDN, no Google Fonts at render time).
2. Before `window.ready` resolves, **explicitly load** each family and weight with sample text that exercises its glyphs, e.g. `await document.fonts.load('700 40px "Noto Sans Devanagari"', 'प्रकाश क्ष ज्ञ')`. `document.fonts.ready` alone does not trigger loads for faces no element has requested yet (`12_advanced_animations_with_claude/04_harness_contract/contract.md` §6; verify on the pinned Chrome).
3. If a face fails to load, **fail the render** through `window.__errors`. Never let the browser substitute silently (NEW-16).
4. `document.fonts.load()` cannot prove a glyph did not fall back. `preflight.sh` checks system coverage with `fc-list` for U+0915 (Devanagari KA), U+0995 (Bengali KA) and U+09F0 (Assamese RA); the shaping test card (§7.6) checks rendering.

### 5.2 Glyph coverage check (offline, before render) [Recommendation]

1. Collect every string the scene will display: fixture text fields, approved-script words used as expressive text, numbers, symbols.
2. For each string and its assigned font, confirm every code point is in the font's character map. A font-inspection library such as fontTools can read the map (not in the evidence set; verify and admit through `examleaf-skills-security`).
3. Flag emoji and pictographic symbols (NEW-3): colour emoji render differently across systems and may be missing on the Linux render box. Prefer drawn SVG icons to emoji.
4. Output `qa/glyph_coverage.json` with missing code points per font. Any miss is a **Major** defect for expressive text and **Critical** for science text (an inaccessible essential symbol blocks release, `07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §4).

### 5.3 Render-time tofu check

Coverage in the character map does not prove correct shaping. Render a test card per script (§7.6) and compare against reference images reviewed by a native reader. This is the only reliable check for conjunct shaping [Hypothesis].

---

## 6. Hold times

| Text | Minimum fully-readable hold | Source |
|---|---|---|
| Primary headline / hook title | **≥ 1.2 s** before the next major transition | [N60] (example timing, not a tested threshold) |
| Same, in Hindi or Assamese, or longer copy | Longer; start at 1.5 × the English hold and measure reading time in the pilot | [N60] "lengthen it for Hindi and longer copy" (report §4.4); the 1.5 × factor is a [Hypothesis] |
| Equation | Until the narration finishes reading it **+ 0.5 s** | Report §7.5 [Recommendation] |
| After an important transformation or completed diagram | **2–4 s**, longer when necessary | RD-02; `02_learning_psychology/INSTRUCTIONS_production_rules.md` E4 |
| Question or target quantity during a calculation | Visible throughout the step | `07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S8 visual rules |
| Prediction prompt | For the whole think pause (default 6 s; 5–8 s range) | RD-11 |

Machine-readable values live in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` `hold_times_s`: `headline_min` 1.2, `headline_min_devanagari` and `headline_min_bengali_assamese` 1.8 (the 1.5 × [Hypothesis]), `per_word_floor_s` 0.3 with `hold = max(headline_min, 0.3 × word_count)` [Hypothesis], `equation_hold_after_narration_s` 0.5, `important_transformation_hold_s` 2–4. When several rules apply, take the longest. The hold-time check (`12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` A5) measures holds from rendered states, not from intentions.

**Equation hold rule, precisely** [Recommendation]: let `t_end` be the `t1` of the last word that reads the equation aloud (from `words[]`). The equation must stay fully visible and unchanged from its reveal until at least `max(t_end + 0.5 s, transform_end + 2.0 s)`.

---

## 7. Devanagari and Bengali–Assamese text (#55)

### 7.1 Why per-code-point animation breaks Indic text [Hypothesis]

In Devanagari and Bengali–Assamese, one visible syllable (akshara) is often several Unicode code points: a consonant, a virama (halant), another consonant, a vowel sign. The font's shaping engine combines them into a conjunct or reorders a vowel sign (for example, the short-i vowel sign is drawn before the consonant it follows in memory). If an animation inserts characters one code point at a time, intermediate frames show broken forms: a dangling virama, an unattached matra, a conjunct that "pops" into a different shape. This is the failure the report warns about (§4.4: "Animate per word or per grapheme cluster, never per code point").

### 7.2 Units of animation, safest first

1. **Whole word, mask reveal** (default for Indic): the word is shaped once as a single text run; a mask or clip-path wipes it on. Shaping never changes during the animation.
2. **Whole word per tile** (ransom mode for Indic): one tile per word.
3. **Grapheme cluster** (only after the §7.6 test passes): segment with the browser's `Intl.Segmenter` at grapheme granularity (a standard JavaScript API; verify in the harness Chrome version). Note [Hypothesis]: extended grapheme clusters do not always equal aksharas, and segmentation rules have changed across Unicode versions, so results may differ between Chrome/ICU builds (NEW-18). Treat clusters as a candidate unit, confirmed per string by the native reviewer.
4. **Never:** per code point, per byte, or by splitting a word into separate inline elements and revealing them one by one. Separate elements can stop the browser from shaping across element boundaries [Hypothesis]; the safe pattern is one shaped run plus a mask.

### 7.3 Fonts

- Use Noto Sans script families as the house Indic science font (RD-23), with a Devanagari family for Hindi and a Bengali-script family for Assamese. Confirm that the chosen family includes the Assamese-specific letters ৰ (U+09F0) and ৱ (U+09F1) (verify coverage; §5.2). Set `lang` on text containers (`hi`, `as`, `bn`, `en`) and use line-height ≥ 1.4 for marks above and below the line (contract §6).
- Expressive Indic fonts (handwriting or display styles) are **not** identified in the evidence set. Each style guide must name candidates, record licences, and pass the §7.6 test before use.
- Do not substitute a Bengali-language font choice or wording for Assamese on the assumption that the script is shared; language review applies to text as well as voice (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §18: "Never substitute Bengali pronunciation or infer support from script similarity").

### 7.4 Language and medium

- Launch is en-IN only (RD-26). Hindi or Assamese on-screen text appears only after the locale gate passes and the business medium decision requires it.
- Hinglish lines are usually written in Latin script; they follow the Latin rules.
- "Do not assume Hindi is universally comfortable for an Assam audience" (`03_super_teacher_framework/INSTRUCTIONS_super_teacher_authoring.md`). Indic lines are audience-led and reviewed by a native subject editor.
- **Numerals** (NEW-30): use the numeral system and decimal convention of the edition's textbook for that medium, as recorded in the fixture. Never mix Devanagari and Western digits within one scene.
- Localised labels are re-laid out, not shrunk; Indic strings are often wider or taller (conjunct stacking). `examleaf-alignment-localize` owns the localised SceneSpec and label reflow (`06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 7).

### 7.5 Timing for Indic narration

Word timestamps for Hindi or Assamese come from the provider or a language-appropriate forced aligner; "Reject unavailable language resources rather than inventing word timing" (`07_end_to_end_pipeline_instructions/04_NARRATION_SUBPIPELINE.md` §11). If word-level timing is not trustworthy, reveal per phrase at the clip start and lengthen holds.

### 7.6 Pilot test card (required before any Indic kinetic text)

1. Prepare 20 strings per script with conjuncts, reordering vowel signs, nukta forms, Assamese-specific letters, numerals and mixed Latin–Indic text (formulas inside Hindi sentences).
2. Render each string in every assigned font and mode (whole-word mask, per-word tiles, per-cluster) on the production render box.
3. Export the final frame and five intermediate frames per animation.
4. A native reader marks each as correct / broken; any broken intermediate frame disqualifies that mode for that font.
5. Record results in the style guide; re-run when Chrome, the fonts or the harness change.

---

## 8. Captions and safe zones (#51)

### 8.1 Captions are not kinetic typography

- Captions are an accessibility requirement: "accurate selectable captions, an accessible transcript, and a protected caption area" (`02_learning_psychology/INSTRUCTIONS_production_rules.md` D7).
- Caption timing is authored by `examleaf-speech-animation-synchronizer`; corrections by `examleaf-audio-caption-qa`; render and composition only package them (`06_skills_library/OVERLAP_and_DEDUPLICATION.md` cluster 9). The kinetic-typography skill never writes captions.
- On-screen text stays short: "a title, a number or a punchline word, never full narration sentences" ([V4-MP] §5). This also avoids duplicating captions.

### 8.2 Sidecar versus burned-in

| Output | Captions | Use |
|---|---|---|
| Lesson in the ExamLeaf player | **Sidecar** VTT + SRT, selectable; transcript | Default (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S12) |
| Reel / Short | Sidecar where the platform accepts it; optional **burned-in** variant inside the caption reserve [Recommendation] | Platform behaviour unverified (playbook Step 12 marks safe-zone specs unverified) |

Burned-in captions must use the same text as the sidecar (from the narration source), sit inside the caption reserve, and never overlap kinetic text or essential diagram parts (NEW-1).

### 8.3 Safe zones

- Exact Reels/Shorts UI insets are **not** in the verified evidence; measure them per platform against current app screenshots and store them as tokens (report §7.9; NEW-27).
- Tokens live in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`; layout helpers in `12_advanced_animations_with_claude/03_skills/examleaf-vertical-adapt/`. The file partitions the usable band into `top_title` (22 %, headline/hook), `middle_visual` (54 %, all science glyphs) and `bottom_caption` (24 %, protected caption area). Its platform insets (top 250, bottom 450, left 60, right 120 px) are **PLACEHOLDERS** with `measured: false`; QA treats them as provisional (NEW-27). Minimum sizes at 1080 px: essential label 50, equation 63, heading 59 px.
- Adapt the [V4-MP] "about 90 px from the frame edges" rule with larger top and bottom margins for platform chrome and captions (report §7.9).
- The playbook's caption guidance (`11_human_feel_voice_audio_research/PLAYBOOK_human_crafted_vertical_video.md` Step 12, [Recommendation], platform specs unverified): large, high-contrast, 1–2 lines; out of the bottom UI band **and the right-side action rail**; one highlighted keyword per caption; Hindi captions in Devanagari with technical terms in Latin script. Kinetic text follows the same exclusion zones.
- The house reserve for 1920×1080 is a 96 px safe margin and ≈ 190 px protected caption area (`07_end_to_end_pipeline_instructions/03_PER_LESSON_PRODUCTION_PROCEDURE.md` S8 tokens); the vertical equivalent comes from the measured tokens.
- The safe-zone overlay check reads every text element's bounding box from the DOM at each cue boundary (`12_advanced_animations_with_claude/02_documentation/10_QA_GATES_anim.md` A4).

---

## 9. CSS-only, the Motion library and tween libraries

- "Prioritize CSS-only solutions for HTML. Use Motion library for React when available" [N54].
- In a seek-rendered harness, motion must be a function of `t`. CSS animations and transitions run on the browser clock unless they are driven explicitly. Two seekable patterns [Recommendation; verify in the harness]:
  1. **Computed styles:** on `seek(t)`, compute each element's transform and opacity in JavaScript from the cue sheet and set inline styles (simplest, most portable).
  2. **Paused animations:** define CSS keyframes, keep them paused, and set their current time from `t` (for example through the Web Animations API). Verify that the harness's capture sees the updated state.
- For React compositions (if Remotion wins the benchmark), the Motion library is the [N54] choice, driven by the composition frame, not wall time.
- GSAP vocabulary ([V4-MP] §8: back.out, power3.out, expo.out) can be reproduced with pure easing functions. If GSAP itself is used, drive its timeline by `seek(t)` (report §2.3) and record its licence ("free under its current standard licence, but it is not MIT-licensed", `04_video_engine/INSTRUCTIONS_video_engine_setup_and_run.md` §10).
- Infinite repeats are banned (#18): every idle tween has a finite repeat count.

---

## 10. Procedure for a kinetic-typography scene (numbered)

1. **Inputs:** brief (style ID, allowed modes, font allow/ban lists), cue sheet, fixture (science text), approved script (expressive text), safe-zone tokens.
2. **Classify** each text element: science or expressive (§2). Science elements get fixture field IDs.
3. **Choose units** per element (§3.3, §7.2).
4. **Compute timing** from `words[]` with lead, stagger, clamp (§3).
5. **Lay out** in the vertical safe area; check essential size ≥ ≈ 50 px (RD-18).
6. **Preload fonts** and run the glyph coverage check (§5).
7. **Write the scene** against `12_advanced_animations_with_claude/04_harness_contract/scene_template.html`; lint with `lint_seek_contract.js`.
8. **Render twice;** compare frame hashes (#17).
9. **Run QA:** safe zone, hold time, DOM text diff, glyph and shaping checks, contrast (doc 10).
10. **Human review** of the storyboard frames and the final scene; native reader for Indic text.

---

## 11. Edge cases owned here

| # | Edge case | Section |
|---|---|---|
| #8 | Generic look (same fonts everywhere) | §4.2–§4.3 |
| #18 | Infinite repeats | §9 |
| #49 | 16:9 guide in a 9:16 pipeline | §8.3 |
| #50 | Short headline hold | §6 |
| #51 | Platform UI overlap | §8 |
| #54 | Image model draws text | §2: all text built in code ([V4-MP] §12) |
| #55 | Indic glyph gaps, broken conjuncts | §5, §7 |
| #63 | TTS regenerated | §3.1 (timings only from cue sheet) |
| NEW-1, NEW-2, NEW-3, NEW-16, NEW-18, NEW-30, NEW-31 | See doc 12 | §4–§8 |

---

## 12. Open questions (verify)

1. Licences of every [V4-MP] display font and of candidate Indic expressive fonts.
2. Noto family coverage of Assamese-specific letters; shaping quality in the production Chrome build.
3. `Intl.Segmenter` grapheme behaviour for Devanagari and Bengali–Assamese in the pinned Chrome.
4. Platform safe-zone insets for Instagram Reels and YouTube Shorts (measure).
5. Whether burned-in captions measurably help on Reels (A/B test), and the reading-time multiplier for Hindi/Assamese holds.
