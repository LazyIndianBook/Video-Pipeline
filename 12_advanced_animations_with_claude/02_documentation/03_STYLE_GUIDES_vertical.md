# 03 · Style guides for vertical 9:16 animation

**Purpose.** Define ExamLeaf's five house animation styles for vertical video: how each is produced, what reference it needs, its limits, where ExamLeaf uses it, its credit cost and the edge cases it must handle; then the shared rules for adapting 16:9 material to 9:16, fonts (including Indic coverage), palette and motion vocabulary.

**Read with.** The style files in `12_advanced_animations_with_claude/05_style_guides/` (`paper-collage-vertical.md`, `doodle-handdrawn.md`, `editorial-vox.md`, `kinetic-type.md`, `voxel-isometric.md`, `style_tokens.json`, `README.md`), the prompt templates in `12_advanced_animations_with_claude/06_prompts_and_templates/` (`master_prompt_paper_collage_VERTICAL.md` and the per-style prompt templates), `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`, and the base tokens `02_learning_psychology/palette_and_typography_tokens.json`.

**Conventions.** As in doc 00. Edge cases #1–#65 from report §8. Contrast ratios marked "computed" were calculated by this section with the WCAG relative-luminance formula, the same method the project's token file uses.

---

## 1. Rules shared by every style

### 1.1 What a house style is

A house style is a **versioned file** in `12_advanced_animations_with_claude/05_style_guides/` plus a block in `style_tokens.json`. It holds: palette subset and roles, allowed and banned fonts, motion verbs and timings, transitions, SFX list, depth layers, writing hooks for the *storyboard* (never for the script), do and don't lists, and the routes it may be used for. `examleaf-style-guides` owns the library; `examleaf-anim-brief` copies the selected version into each job (doc 02 §3.5). A style change is a new version; an approved job keeps the version it was approved with.

### 1.2 The base-science layer (for data-bound scenes)

Data-bound scenes (axes, values, equations, structures, labelled diagrams) do **not** use an illustrative house style. They use the project's base look:

- light theme only at launch (RD-27): background `#F7F9FC`, ink `#14213D`, secondary `#526074`, blue `#185ABD`, teal `#087986`, amber `#9A5B00`, purple `#6E44AA`, red `#B42318` (`02_learning_psychology/palette_and_typography_tokens.json`);
- Inter, Noto Sans script families and KaTeX fonts (RD-23);
- motion only for semantic change (a point appears, a step is added), using the learning-psychology timings (§6.2); no idle sway, push-in, shake, boil or parallax (#64);
- holds of 2–4 s after an important transformation (RD-02).

In briefs this is style ID `base-science`. An illustrative scene that contains a science element applies base-science rules to that element (doc 00 §5).

### 1.3 Non-negotiables in every style

| Rule | Why | Edge case |
|---|---|---|
| No text, numbers, formulas or labels inside any raster asset; all text is DOM/SVG/canvas text from code | Image models misspell and mis-draw ([V4-MP]: "Built in code, not generated as images") | #54 |
| Every science glyph traceable to a fixture field | Accuracy invariant | #12 |
| Vertical 1080×1920 at 30 fps; safe-zone tokens | Platform overlays | #49, #51 |
| No full-frame flashes, no rapid luminance flicker | Students; [V1] warned of "bright, fast flashes" | #56 |
| Headline hold ≥ 1.2 s [N60]; transformation hold 2–4 s (RD-02) | Readability | #50 |
| Finite repeats; seeded stateless randomness; pure function of t | Seek rendering | #17, #18 |
| One dominant highlight at a time; colour never the only cue | Base QA rules | — |
| Fonts vendored and verified for every script used on screen | Tofu and broken conjuncts | #55 |
| Depth by layers where the style allows it (background / middle / subject / foreground) | [V2]'s first pass was "flat… strictly 2D" | — |

---

## 2. The five house styles

### 2.1 `paper-collage-vertical` (adapted from [V4-MP])

**How it is produced.**
1. Raster cutouts: watercolour and coloured-pencil illustrations on transparent backgrounds at 2K, generated through `examleaf-mcp-orchestrator` (Higgsfield, GPT Image 2.5) with the [V4-MP] cutout template, then trimmed of transparent margins ([V4-MP] §12).
2. Cutouts placed as DOM or canvas layers with a white die-cut border (6–12 px at 1080p in [V4-MP]; keep the same pixel range on the 1080-wide vertical canvas) and the two-layer warm shadow `0 9px 7px rgba(74,48,22,0.30)` + `0 2px 1.5px rgba(0,0,0,0.20)` ([V4-MP] §2).
3. Textured paper backgrounds (cream watercolour, kraft board, watercolour skies, torn-paper strips).
4. Built in code: ransom-note titles, Caveat Brush captions with a red double underline, Patrick Hand tags on washi tape, confetti, doodles (3–5 px, round caps), simple UI ([V4-MP] §5, §6, §12).
5. Motion in GSAP-style vocabulary driven by `seek(t)` (§6); stop-motion boil as stepped seeded jitter at 8–10 fps.

**Reference needed.** The full style file, the approved 3×3 storyboard grid, and one canonical hero image for character consistency (#48) ([V4-MP] §4: "Keep them identical across shots by using an earlier image of them as a reference").

**Limits.**
- Credit-heavy: [V4] says the style is "on the expensive side regarding credits" because it needs many assets. Every asset is billed via agents [N33] and there is no native cap [N34] (#41, #42).
- Character drift between independent generations (#48).
- The guide is 16:9 at 1920×1080 with text "about 90 px from the frame edges" (#49); see §3.
- The guide's darker sheets (night navy, charcoal soot, "a heavy dark sheet… for somber beats") conflict with light-theme-only at launch (RD-27); see §5.6.
- The guide's "white flash or bloom for explosions" is banned (#56); use a paper-burst or a quick sheet swap instead.
- The guide's "Never frozen: everything on screen gets a gentle idle sway" applies only to characters and props, never to science elements or text being read (AD-16, #64).

**ExamLeaf use.** Hooks, analogies, history-of-science stories and recap endings. Never for the core worked explanation.

**Credit cost.** Highest of the five: one grid plus one generation per cutout and background (and re-generations on drift). The exact credits per generation for GPT Image 2.5 via Higgsfield are not in the evidence (verify, open question Q5); `estimate.json` must count assets before approval (doc 05 §4).

**Edge cases.** #41, #42, #47, #48, #49, #54, #55 (ransom tiles with Indic text), #56, #64.

**Files.** `12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md`; prompt `12_advanced_animations_with_claude/06_prompts_and_templates/master_prompt_paper_collage_VERTICAL.md`.

### 2.2 `doodle-handdrawn` (pure code, [V2])

**How it is produced.** Canvas 2D or SVG paths with seeded noise on control points (wobble), re-seeded at a boil rate; stroke-dash draw-on; a pencil texture overlay; flat fills. No image model: the [V2] deer story was entirely code (report §4.2).

**Reference needed.** A short reference clip or 3–5 stills in the target style plus a palette (report §4.2), measured by `examleaf-reference-analyzer`.

**Limits.** [V2] found the first pass "flat and cartoonish… strictly 2D": ask explicitly for parallax layers, foreground strips and shadows. Boil on a science element (a ray, an axis) would change its geometry frame to frame: forbidden (#64).

**ExamLeaf use.** [Recommendation, report §4.2] the **default illustrative style for Reels** because it costs no credits; also lesson hooks and analogies.

**Credit cost.** Zero image credits; tokens only (scene code at high effort).

**Edge cases.** #17 (seeded wobble), #18 (finite boil), #49, #56, #64.

**Files.** `12_advanced_animations_with_claude/05_style_guides/doodle-handdrawn.md`.

### 2.3 `editorial-vox` ([V3])

**How it is produced.** Textured backgrounds, cut-out photos or illustrations, highlighter strokes, a bold serif and sans headline mix, map and number callouts, push-ins (report §4.3). Built in HyperFrames (or Remotion in the benchmark). In ExamLeaf, numbers and comparison bars come from fixtures; photos only from licensed or owned sources recorded in the AssetManifest (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5).

**Reference needed.** A reference video for pacing, typography treatment and layout ([V3]: "study the reference video's layout structure and its exact typography treatment").

**Limits.** [V3]'s AI-written script was weak; ExamLeaf supplies the script (#11). Push-ins and highlighter wipes over a number being compared can mislead (#64): the number appears after the camera settles. Real-photo cutouts carry licence and likeness questions; prefer illustrations.

**ExamLeaf use.** Comparisons and scale stories driven by validated numbers (planet sizes, orders of magnitude, population genetics ratios), chapter openers.

**Credit cost.** Low to medium: textures and illustrations may be generated once and reused; numbers and maps are code.

**Edge cases.** #11, #12, #49, #50, #54, #64.

**Files.** `12_advanced_animations_with_claude/05_style_guides/editorial-vox.md`.

### 2.4 `kinetic-type` ([V3], [N50]–[N55], [N60])

**How it is produced.** A per-word timeline keyed to TTS word timestamps from the cue sheet; masks, slides and scale pops; one orchestrated staggered entrance rather than scattered micro-animations [N53]; dominant colour with sharp accents [N52]; distinctive fonts, with overused ones banned or rotated [N51][N55]. [N54] says "Prioritize CSS-only solutions for HTML"; in seek-rendered video, CSS animations run on real time and break seeking, so ExamLeaf computes every style from `t` in JavaScript and uses CSS only for static styling (doc 04 §2, [Recommendation]).

**Reference needed.** A reference clip for rhythm, or the style file alone.

**Limits.**
- Indic scripts need fonts with full Devanagari and Bengali–Assamese coverage [Hypothesis]; per-letter animation can break conjuncts and ligatures [Hypothesis]: animate per word or per grapheme cluster, never per code point (#55).
- Holds: headlines readable at least 1.2 s [N60], longer for Hindi and longer copy (#50).
- Captions and kinetic type must not compete: the existing rule avoids "full-paragraph narration + animated diagram + equation + moving karaoke captions at once" (`02_learning_psychology/palette_and_typography_tokens.json` typography captions note).

**ExamLeaf use.** Key definitions, exam tips, "three things to remember" cards, Reel hooks and CTAs, formula-name callouts (the formula itself is KaTeX from fixtures).

**Credit cost.** Zero image credits.

**Edge cases.** #8, #50, #51, #55, #63.

**Files.** `12_advanced_animations_with_claude/05_style_guides/kinetic-type.md`.

### 2.5 `voxel-isometric` ([V5] island demo, [V1] 3D runs)

**How it is produced.** three.js with instanced boxes, an orthographic camera, baked or simple lighting and seeded procedural layout; camera paths are functions of `t` (report §4.5). Rendered by the raw seek pipeline and imported as a clip (doc 04 §10).

**Reference needed.** Stills of the target look; for science content, the fixture (lattice parameters, organelle list).

**Limits.** GPU and headless WebGL availability on the render box; frame-time variance; anti-aliasing differences between machines (#65). The [V5] voxel island is an unverified Fable 5.5 demo (#57): the style is feasible with Opus [Hypothesis] but untested in ExamLeaf. Voxel geometry is stylised: a crystal lattice drawn in voxels must still keep the fixture's coordination and proportions, or it is labelled as a schematic.

**ExamLeaf use.** Crystal lattices, cell organelles as a stylised map, an "island of concepts" chapter recap.

**Credit cost.** Zero image credits; highest token cost (xhigh effort for complex scenes, doc 01 §7.2) and highest render cost.

**Edge cases.** #15, #17, #57, #64, #65.

**Files.** `12_advanced_animations_with_claude/05_style_guides/voxel-isometric.md`.

### 2.6 Summary

| Style | Produced by | Raster credits | Token/effort | Reference | Best ExamLeaf use | Routes allowed | Main risks |
|---|---|---|---|---|---|---|---|
| paper-collage-vertical | Cutouts (Higgsfield) + code | **High** | high | Style file + grid + hero image | Hooks, analogies, history, recaps | illustrative | #41, #48, #54, #56 |
| doodle-handdrawn | Code only | None | high | Clip or 3–5 stills | **Default Reel style**; hooks | illustrative | flatness, #64 |
| editorial-vox | Code + textures/illustrations | Low–medium | high | Reference video | Comparisons, scale | illustrative (+ fixture numbers) | #11, #64 |
| kinetic-type | Code only | None | high | Optional clip | Definitions, tips, hooks, CTAs | typographic | #50, #55 |
| voxel-isometric | three.js | None | xhigh | Stills + fixtures | Lattices, organelles, recap islands | illustrative / spatial (+ fixtures) | #65, #57 |
| base-science (§1.2) | SVG/Manim/HyperFrames from fixtures | None | high | — | Every data-bound scene | data-bound | #12, #64 |

### 2.7 Not adopted

- **Style-morph montage** ([V5]): unverified Fable 5.5 demos; rarely useful for teaching (report §4.7).
- **Photoreal people or footage**: Opus 5.5 is not a text-to-video model [N62] (#52); default generated video is 0 s (RD-39).
- **Real-person likeness cutouts**: [Recommendation] show historical scientists as generic paper characters with a code-built name tag; avoid likeness portraits from image models.

---

## 3. Adapting 16:9 material to 9:16 (#49, #51)

### 3.1 Canvas and zones

- Canvas **1080×1920 at 30 fps** (vertical-only decision of 15 Oct 2026, RD-16 superseded), H.264/yuv420p delivery (doc 04 §12).
- Three bands, defined as **named tokens** in `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json`:
  - `title_band` (upper part, below the platform's top status/title overlay);
  - `content_safe` (the central area where every essential element lives);
  - `caption_band` (lower part, kept clear for captions; below it the platform's CTA and UI overlays).
- **Pixel values are not invented here.** The report found no verified per-platform insets (open question Q9). Fill the token file from measured screenshots of current Instagram Reels and YouTube Shorts apps on representative phones, and re-measure when apps change.
- Side margins: [V4-MP] keeps text "about 90 px from the frame edges" at 1920×1080. [Recommendation] keep at least the same 90 px on the left and right of the 1080-wide vertical canvas as a starting value, and make top and bottom margins larger, as measured (report §7.9). *15 Oct 2026 (AD-42): the working value is now one token, `zones.side_margin_min_px` = **96 px** in `04_harness_contract/vertical_safe_zones.tokens.json` (the larger of 90 and the planning pack's 96).*
- Existing 16:9 tokens (`safe_margin_px 96`, `caption_reserve_bottom_px 190` at 1920×1080, from the planning-pack design tokens) do not transfer directly to 9:16; the vertical values go into the new token file.

### 3.2 Re-layout rules

1. **Recompose, never crop.** "A crop that removes a graph axis or condition is a scientific defect, not a cosmetic issue" (`07_end_to_end_pipeline_instructions/05_SHORTS_and_REELS_PROCEDURE.md` §1). This applies to style guides and references too.
2. **Stack, don't spread.** Side-by-side compositions become top/bottom stacks: title in `title_band`, the one idea of the frame in `content_safe`, support (a tag, a small character) beside or below it, never in `caption_band`.
3. **One idea per frame** ([V4-MP] §7) matters more on a narrow screen; split a 16:9 frame that holds two ideas into two beats.
4. **Type sizes from the phone rule.** `Displayed = Source × (360 / master width)`; on a 1080-wide master, essential labels need at least about 50 px source to match the landscape essential-label target (RD-18 derivation: 16.5 × 1080/360). Split or enlarge before shrinking.
5. **Characters move up.** [V4-MP]'s "character bottom-left looking up at a ransom-note title" puts the character in the caption band on vertical; place it at the bottom of `content_safe` instead.
6. **Recurring layouts, vertical versions** (table below).
7. **Transitions run vertically by preference.** Paper sheets slide in from bottom or top more often than from the sides, because a vertical sheet sliding from the side covers more distance; vary direction scene to scene as [V4-MP] asks.
8. **Push-ins anchor on the subject**, not the frame centre, so the subject stays inside `content_safe` at scale 1.03–1.04.
9. **Storyboards are vertical.** The 3×3 grid is nine 9:16 panels (doc 05 §2), so the composition is judged in its real shape.
10. **References**: a letterboxed 16:9 reference is measured for pacing and palette only; its layout is not copied.
11. **Sub-range Reels** re-seek lesson scenes over a time range and re-time them to a beat grid where narration permits (report §9 step 10); they still pass the vertical rules and get their own GS approval.
12. **Captions** are burned or platform-native per the Reels procedure; in either case the caption band is reserved and verified with a QA overlay (#51).

### 3.3 [V4-MP] composition items, vertical versions

| [V4-MP] (16:9) | Vertical version [Recommendation] |
|---|---|
| "a character bottom-left looking up at a ransom-note title" | Title in `title_band`; character at the bottom of `content_safe`, looking up |
| "photos taped to a kraft board" | Two or three polaroids stacked vertically, slightly overlapping, tape on the top edge |
| "a row of objects appearing one per word" | A column (or a 2×2 cluster) of objects, one per word |
| "a big central prop with small tags around it" | Prop centred in `content_safe`; tags above and below rather than left and right |
| Landscapes of torn-paper strips | Taller strips; horizon in the lower third of `content_safe`; foreground strip above `caption_band` |
| Slow push-in to ~1.03–1.04 | Same, anchored on the subject |
| Sheet transitions "right, left, top, bottom" | Bottom and top preferred; sides allowed |
| Text ~90 px from edges | ≥ 96 px sides (`zones.side_margin_min_px`, 15 Oct 2026); top/bottom from measured tokens |

---

## 4. Font policy

### 4.1 Two tiers

| Tier | Fonts | Use | Rule source |
|---|---|---|---|
| **Science** | Inter, Noto Sans script families, KaTeX fonts | Labels, units, axes, equations, chemical formulae, any fixture-bound string | RD-23; base tokens |
| **Display** (per style) | Listed in `style_tokens.json` per style | Titles, hooks, captions, tags, CTAs | [N51] distinctive fonts; [V4-MP] list |

The science tier is fixed for legibility and consistency with the rest of the pipeline. Distinctiveness [N51] is achieved in the display tier only.

### 4.2 Display allow lists (starting point; the style files are authoritative)

| Style | Display fonts | Source |
|---|---|---|
| paper-collage-vertical | Ransom tiles: Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One; captions: Caveat Brush; labels: Patrick Hand | [V4-MP] §5 |
| doodle-handdrawn | Hand-lettered faces chosen in the style file (for example Patrick Hand, Caveat Brush) | style file |
| editorial-vox | A bold serif + a sans pairing chosen in the style file | report §4.3 |
| kinetic-type | A rotating set of distinctive display faces chosen in the style file | [N51], [N55] |
| voxel-isometric | A blocky display face chosen in the style file | style file |

Every file is vendored, licence-recorded and hashed (doc 01 §3.2).

### 4.3 Ban and rotation

- **Banned as display fonts by default:** Arial [N51], Space Grotesk ([N55] names it as a convergence choice), and Inter (allowed only in the science tier). Add any face that appears in more than a set share of recent scenes (threshold set by the style owner) to a temporary ban, because "you still tend to converge on common choices" [N55] (#8).
- **Rotation:** kinetic-type and collage styles rotate display faces from their allow list by a seeded choice per lesson, so consecutive Reels do not look identical.

### 4.4 Indic coverage and animation (#55)

1. **Coverage.** Hindi needs Devanagari; Assamese needs the Bengali–Assamese block including ৰ and ৱ. Most [V4-MP] display fonts are Latin-only [Hypothesis: verify each file's character set]. For Hindi titles use Noto Sans Devanagari or a licensed Devanagari display face chosen by the style owner; for Assamese use Noto Sans Bengali or an Assamese-capable display face (verify).
2. **Test card.** Render the test strings in doc 01 §3.3 through the pinned Chrome on the render box; a native-language editor signs off each font file.
3. **Animate per word by default.** Splitting Devanagari or Bengali–Assamese text by code point separates virama sequences and vowel signs and breaks conjuncts [Hypothesis]. Per-word animation is always safe.
4. **Per grapheme cluster only after testing.** `Intl.Segmenter` with `granularity: 'grapheme'` follows Unicode's extended grapheme cluster rules; newer Unicode versions added a rule that keeps Indic conjuncts together, but whether the pinned Chrome's ICU version applies it must be **verified** on the test card before any per-cluster animation ships.
5. **Ransom-note tiles in Hindi/Assamese:** one tile per word, not per letter [Recommendation]. Mixed fonts within one word are not used for Indic text.
6. **Holds:** longer for Hindi than the 1.2 s English minimum [N60] (#50); set per language in `style_tokens.json` after the pilot's phone tests.
7. **Hinglish** on-screen text is in Latin script unless the lesson's medium decision says otherwise (RD-26).

### 4.5 Loading

Fonts load from `assets/fonts/` via local `@font-face`; the scene awaits them before the first `seek` resolves; no remote fonts (doc 04 §6). A missing glyph is a lint or QA failure, never a silent fallback.

---

## 5. Palette rules

### 5.1 Base

The project palette in `02_learning_psychology/palette_and_typography_tokens.json` is the base for every style: background `#F7F9FC`, ink `#14213D` (15.15:1), secondary `#526074` (6.06:1), blue `#185ABD` (6.15:1), teal `#087986` (4.87:1), amber `#9A5B00` (5.14:1), purple `#6E44AA` (6.48:1), red `#B42318` (6.23:1). Its colour rules apply everywhere: stable identity (a quantity keeps its colour), one dominant highlight, colour not the only cue, scientific conventions respected ("a red oxygen atom is not an error indicator"), adjacent-pair checks, pale highlight areas behind long text.

### 5.2 Dominant colour with sharp accents

"Dominant colors with sharp accents outperform timid, evenly-distributed palettes" [N52]. In practice: one dominant surface colour per scene (paper, background), ink for text, and one or two accents used sparingly for the single highlighted idea. [V4-MP] says the same about its palette: "the brightest accents are tomato red and mustard".

### 5.3 Brand and subject colours

- **Brand:** ExamLeaf brand colours are not defined in the project documents found by this section (verify with the founder); until then, the base palette is the brand.
- **Subject colours** (Physics, Chemistry, Mathematics, Biology): the report recommends encoding them as tokens (report §7.2), but no values exist in the project. [Recommendation] Choose four from the base accents after adjacent-pair contrast checks, record them in `style_tokens.json`, and use them only for chrome (chapter tags, end cards), never for a scientific quantity, so quantity colours stay stable across subjects. Open question Q13 in doc 14.

### 5.4 Style palettes are layers on the base

Each style's palette lives in `style_tokens.json`. Text on any style background must pass **≥ 4.5:1**; essential non-text graphics **≥ 3:1** (project thresholds). Computed examples for the [V4-MP] collage palette:

| Foreground on background | Ratio (computed) | Use |
|---|---|---|
| ink `#2b2622` on cream `#f3ecdf` | 12.74 | Text OK |
| pencil `#3a332c` on cream | 10.58 | Text OK |
| night navy `#1b2a4a` on cream | 12.10 | Text OK |
| ultramarine `#2f4fa8` on cream | 6.37 | Text OK |
| teal `#2f7f7a` on cream | 4.03 | Graphics only (≥3:1), not text |
| tomato `#d9483b` on cream | 3.62 | Graphics only, not text |
| olive `#7c8a3c` on cream | 3.22 | Graphics only |
| kraft `#b98f5e` on cream | 2.50 | Decorative only |
| mustard `#e0a73a` on cream | 1.83 | Decorative only |
| ink on kraft | 5.10 | Text OK |
| pencil on kraft | 4.23 | Not text |

**Ransom-tile pairs from [V4-MP] §5** (computed): cream on ink 12.74 and mustard on ink 6.95 pass; ink on mustard 6.95 passes; cream on tomato 3.62, cream on teal 4.03, mustard on ultramarine 3.48, ultramarine on blush 3.89 and tomato on blush 2.21 **fail** 4.5:1. [Recommendation] A ransom title is essential text, so failing pairs are either removed from the tile set or replaced by darker tile variants defined and validated in `style_tokens.json`.

### 5.5 Colour and science

- A colour that encodes a quantity (current, a species, an allele) keeps it across all styles in a lesson.
- Style colours never override scientific conventions (element colours, standard diagram conventions).
- Distinguish lines and regions by labels, dash patterns or shapes as well as colour.

### 5.6 Dark backgrounds (RD-27)

The project is **light theme only at launch** because a validated dark accent palette does not exist (RD-27). [Recommendation, AD-17] Collage night-navy or charcoal sheets may be used only as short illustrative mood backgrounds with no essential science text on them; any text on a dark sheet must pass 4.5:1 (cream on navy computes to 12.10; mustard on navy to 6.61); data-bound scenes are never dark. Until the founder accepts this, keep collage scenes on cream, kraft and watercolour-sky backgrounds.

---

## 6. Motion vocabulary

### 6.1 Easing and verbs ([V4-MP] §8–§9)

| Verb | Easing | Duration | Use | Not for |
|---|---|---|---|---|
| Pop-in with overshoot | back.out(2–3), from scale 0 and about ±12°, pivot at the base | short (style file) | Characters, props, tags | Science labels (use a clean fade/scale without overshoot) |
| Slide-in / sheet slide | power3.out | 0.5–0.7 s for paper sheets | Scene transitions (default) | — |
| Dark-sheet drop | power2.inOut | ~0.9 s with small settle | Somber beats (see §5.6) | Data-bound scenes |
| Whip | expo.out | ~0.4 s | Urgency | Before a reveal the viewer must read |
| Drop-in with bounce; hop with squash and stretch | style file | short | Characters | Science elements |
| Paper-flip swap | scaleX 1 → 0, swap, 0 → 1, confetti puff | short | Transformations as gags | Real chemical/physical transformations (use the approved science animation) |
| Tear | jagged matching edges, halves fall | short | Gags | Diagrams |
| Multiply 1 → 2 → 4 → 8 | stepped | per word | Crowds, counts | Counts that are science data (fixture values only) |

**Never linear; anticipation → action → follow-through** ([V4-MP]; report §7.4).

### 6.2 Two timing systems, one per layer

| Layer | Timings | Source |
|---|---|---|
| Science (base-science and science elements) | simple transition 150–300 ms; highlight appearing 300–600 ms; simple equation transformation 0.8–1.5 s; hold after important transformation 2–4 s (RD-02) | `02_learning_psychology/palette_and_typography_tokens.json` animation timing defaults |
| Illustrative | [V4-MP] verbs above; sheet transitions begin ~0.3 s after the previous line's last word | [V4-MP] §9 |

"Never change a physical simulation's behaviour merely to satisfy an animation timing rule" (`02_learning_psychology/palette_and_typography_tokens.json`).

### 6.3 Finite repeats and idle motion

- Idle sway or bob (±1.5–4° rotation, a few pixels) with a **finite** number of repeats ([V4-MP] §8), computed directly from `t` (for example a sine of `t` multiplied by an envelope that ends at a fixed time), never accumulated frame to frame (#18).
- Idle motion applies to characters and props only. Science elements, equations and any text being read are still (AD-16). This reconciles [V4-MP]'s "never frozen" with the QA rule "No decorative motion" (`07_end_to_end_pipeline_instructions/06_QA_GATES_and_RELEASE.md` §3) and the learning-psychology change types ("decorative (no new meaning — avoid)").

### 6.4 Boil at 8–10 fps

Stop-motion boil ([V4-MP]: "stepped random jitter at 8–10 fps") is implemented as a jitter that changes only when `step = floor(t × boil_fps)` changes, with values from a stateless seeded hash of `(seed, element_id, step)` (doc 04 §3). At 30 fps output and 9 fps boil, each jitter pose holds for three or four output frames. Boil is used for shivering, nerves, fire flicker, shaking ground ([V4-MP]), never on science geometry (#64).

### 6.5 Camera

- Slow push-in 1 → ~1.03–1.04 over a scene ([V4-MP]); stepped shakes on impacts; pans between stacked layers.
- **No camera effect during a measurement, a label reveal or while a diagram is being read** (#64). In base-science scenes there is no camera motion at all.

### 6.6 Orchestration

One well-orchestrated staggered entrance per beat beats scattered micro-animations [N53]. Reveal across the scene; never everything at once ([V4-MP] §8). Each reveal lands on, or about 0.05 s before, its word (doc 02 §3.13).

### 6.7 Photosensitivity (#56)

- No full-frame white flashes or blooms (the [V4-MP] explosion variation is replaced).
- No rapid alternating luminance changes. [Recommendation] Apply the WCAG general flash guideline (no more than three flashes in any one-second period; verify the current WCAG wording and thresholds) as an automated check in `examleaf-anim-qa`, and treat any detection as a blocking defect for student content.

### 6.8 Motion budget

For lessons, the learning-psychology starting budget is substantial explanatory change in 25–35% of runtime, counting "substantial changes in the explanatory model, not caption updates or a moving cursor", and "do not require animation just to meet the percentage". Illustrative scenes (hooks, recaps) are a small share of a 10-minute lesson; Reels may be denser but still one idea per frame.

### 6.9 Tween libraries

[V4-MP] describes motion in GSAP vocabulary. Whether HyperFrames bundles GSAP is not verified (open question Q4). Any tween library is acceptable if its timeline is paused and positioned by `seek(t)` rather than played (report §2.3). GSAP's licence is "free under its current standard licence, not MIT" (`07_end_to_end_pipeline_instructions/07_SECURITY_CREDENTIALS_and_SKILL_ADMISSION.md` §5): record it in `ledgers/licences.md` if vendored. Easing curves can also be implemented directly as functions of normalised time to avoid a dependency.

---

## 7. Sound per style (summary)

| Style | Music | SFX | Notes |
|---|---|---|---|
| paper-collage-vertical | Whimsical storybook bed about 100 BPM ([V4-MP]), 20–24 dB under the voice (15 Oct 2026; [V4-MP] said 15–20), only in hooks/transitions/recaps/outros, low-passed for somber beats, swell on the end card | Paper swish, tap, pop, boing, tear, thud, sparkle chime ([V4-MP]) | Lessons: no music under teaching narration (AD-15) |
| doodle-handdrawn | Light acoustic or plucked bed (Reels: under hook and CTA) | Pencil scratch, soft pop | — |
| editorial-vox | Sparse pulse bed | Highlighter swipe, paper slide, map tick | — |
| kinetic-type | Rhythmic bed aligned to a beat grid (Reels) | Ticks and whooshes on word entrances, quiet | Beat grid from `examleaf-audio-analysis` |
| voxel-isometric | Ambient bed | Block place/click | — |
| base-science | None under teaching | Minimal, semantic only (a click on a step) | Lessons follow the narration master rules |

Music is produced by `examleaf-audio-compose` (seeded Python stems), never taken from references or platform libraries; final loudness follows AD-04.

---

## 8. Where to go next

| Need | File |
|---|---|
| Full style definitions | `12_advanced_animations_with_claude/05_style_guides/paper-collage-vertical.md`, `doodle-handdrawn.md`, `editorial-vox.md`, `kinetic-type.md`, `voxel-isometric.md`, `README.md` |
| Machine-readable tokens | `12_advanced_animations_with_claude/05_style_guides/style_tokens.json`; `12_advanced_animations_with_claude/04_harness_contract/vertical_safe_zones.tokens.json` |
| Vertical collage master prompt | `12_advanced_animations_with_claude/06_prompts_and_templates/master_prompt_paper_collage_VERTICAL.md` |
| Per-style prompt templates and the brief | `12_advanced_animations_with_claude/06_prompts_and_templates/` (brief_template.md and the per-style templates) |
| What must fail | `12_advanced_animations_with_claude/06_prompts_and_templates/negative_tests.md` |
| Skills implementing styles | `12_advanced_animations_with_claude/03_skills/examleaf-style-guides/`, `examleaf-procedural-2d/`, `examleaf-kinetic-typography/`, `examleaf-threejs-scenes/`, `examleaf-vertical-adapt/` |
