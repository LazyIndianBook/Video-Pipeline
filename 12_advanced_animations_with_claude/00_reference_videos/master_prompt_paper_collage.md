# Master prompt: paper-collage educational animation (from RandomAI video WXu4O9oIdIE description link)

Source: https://docs.google.com/document/d/12f1-nob7t0-wf809BX8WdLaGgWeU9UXxIhRXKXYWMYs (fetched 14 Oct 2026, verbatim export)

```text
﻿Create a ~1-minute animated explainer about how an asteroid wiped out the dinosaurs. Match the writing style and animation style described in the Style Guide at the end of this prompt. There is no reference video; the Style Guide replaces it.
Step 1: Study the Style Guide
* Writing style: Read how the narration is written, including tone, sentence length, pacing, hooks, and how facts are delivered.
* Animation style: Read the visual style. The video must be built entirely with JavaScript animations, so note the visual approach, motion style, transitions, typography, and color palette.
Step 2: Write the script
* Topic: A brief history of how the asteroid impact led to the extinction of the dinosaurs.
* Length: About 60 seconds of narration (roughly 140–160 words).
* Style: Closely match the writing style in the Style Guide.
Step 3: Create the storyboard
* Tool: Higgsfield MCP, using the GPT Image 2.5 image model (model ID: gpt_image_2_5).
* Output: One 3x3 grid image with 9 panels covering the main beats of the script in order.
* Style: Match the art style in the Style Guide.
⛔ Review checkpoint
Stop after Steps 2 and 3. Show me the script and the storyboard grid, then wait for my approval before continuing.
Step 4: Generate the voiceover (after approval)
* Tool: Higgsfield MCP
* Voice: Arthur (preset voice, voice_id 30fc8796-ceb6-4a66-b3a7-4a145ef7f346)
* Model: ElevenLabs v3 (Higgsfield text2speech_v2, variant elevenlabs)
* Input: The approved script
Step 5: Build the animation (after approval)
* Build the video in JavaScript, replicating the Style Guide's animation style as closely as possible.
* Follow the approved storyboard for scene order and content.
* Sync the animation to the voiceover timing.
________________


STYLE GUIDE: "Paper-Cutout Storybook Collage"
1. The look in one sentence
A hand-made paper collage in a children's-storybook style. Every character and prop is a watercolor and colored-pencil illustration cut out of paper, with a thin white die-cut border and a soft drop shadow. The cutouts are layered flat on textured paper backgrounds: cream watercolor paper, kraft cardboard, watercolor washes and torn-paper strips. Motion is snappy and playful, like stop-motion, with ransom-note typography, hand-lettered captions and pencil doodles.
2. Materials and surfaces
* Cutouts:
   * Each character or prop is a separate watercolor and colored-pencil painting. It shows paper grain, soft pigment blooms and loose pencil outlines.
   * Every cutout has a clean white paper border (about 6–12 px at 1080p) following its silhouette, like a die-cut sticker.
   * Underneath is a soft, warm drop shadow: roughly 0 9px 7px rgba(74,48,22,0.30) layered with a tight 0 2px 1.5px rgba(0,0,0,0.20).
* Full-frame backgrounds (rotate between these):
   * Cream cold-press watercolor paper with faint fibers, a soft warm vignette, and a few faint pencil sparkle doodles in the corners.
   * Brown kraft cardboard or handmade fibrous paper with flecks, used like a pinboard for taped "photos" and paper tags.
   * Watercolor skies:
      * pale blue and cream with loose painted clouds;
      * deep navy night with white splatter-paint stars;
      * gloomy charcoal soot for somber moments;
      * warm amber for dramatic moments.
   * Landscapes built from layered torn-paper strips (hills, ground, sea), each with ragged white torn-fiber edges and a slight shadow between layers.
* Craft-table props:
   * washi-tape strips (pink, mustard or teal, semi-transparent) holding photos and tags;
   * cream paper tags and labels;
   * polaroid-style photo cards with thick bottom borders;
   * paper confetti squares and torn paper scraps.
* Everything is flat and seen head-on, like a paper diorama photographed straight on. Avoid 3D rendering, glossy gradients, photorealism, and heavy blur or glow.
3. Color palette
* Tomato red #d9483b
* Mustard #e0a73a
* Teal #2f7f7a
* Ultramarine #2f4fa8
* Olive #7c8a3c
* Sage #9dbb8e
* Blush pink #f1a9a0
* Cream #f3ecdf
* Paper white #fbf7ee
* Kraft #b98f5e
* Ink #2b2622
* Pencil #3a332c
* Night navy #1b2a4a
The overall feel is warm and muted, like gouache or watercolor on paper. Saturation is gentle; the brightest accents are tomato red and mustard.
4. Character design
* Cute, round, chunky proportions with big heads.
* Small solid black dot eyes, simple curved smiles, and rosy blush circles on the cheeks.
* Soft watercolor fills with darker pencil outlines.
* Animals and creatures follow the same rules. They are friendly and slightly comic, never scary, even in dramatic moments. For example, a panicked T. rex yells with little sweat drops, and a sad dinosaur shivers with an icicle on its nose.
* Objects can have faces when it's funny: a mischievous asteroid, a surprised wave, a sleepy sun, a worried bullet.
* Use one recurring hero character with a signature outfit, such as a small kid in a red beanie and yellow raincoat, or a curly-haired kid in a blue knitted sweater.
   * Keep them identical across shots by using an earlier image of them as a reference.
   * Make pose variants of the same character: pointing, crying, cheering, waving.
5. Typography (only three kinds of text)
1. Ransom-note titles:
   * Each letter sits on its own small paper square, and each square has a different color and font.
   * Tiles get a slight random rotation (about ±6°), some vertical jitter and a small drop shadow; some letters are lowercase.
   * Tile styles:
      * black with cream or mustard letters;
      * cream with red or black letters;
      * red with cream letters;
      * ultramarine with mustard letters;
      * mustard with black letters;
      * pink with dark red or blue letters;
      * a red polka-dot tile;
      * a blue grid-paper tile;
      * teal with cream letters.
   * Mixed display fonts: Alfa Slab One, Abril Fatface, Bowlby One, Special Elite, Bungee, Titan One, Ultra, Lilita One, Bebas Neue, Playfair Display Black, Rubik Mono One.
   * Letters slap on one at a time (about 0.04–0.05 s apart), synced to the spoken words.
2. Hand-lettered brush captions:
   * Set in "Caveat Brush" in dark ink #2b2622.
   * Revealed letter by letter like handwriting.
   * Often followed by a red pencil double underline that draws itself on in two slightly wobbly strokes.
3. Small labels:
   * Set in "Patrick Hand" on cream paper tags held by a strip of washi tape.
   * Sometimes a red pencil check mark or circle draws on next to them.
On-screen text stays short: a title, a number or a punchline word, never full narration sentences. Keep text about 90 px from the frame edges.
6. Pencil doodles
* Drawn in ink #3a332c, 3–5 px wide, with round caps.
* Types:
   * sparkle crosses in corners;
   * "?" and "!" above characters;
   * speed lines, impact ticks and motion arcs;
   * dashed travel trails;
   * "z z z" and shiver marks.
* They draw themselves on as strokes, or pop in and wobble.
7. Composition
* 16:9 at 1920×1080, 30 fps.
* Flat, straight-on camera, generous negative space, one clear idea per frame.
* Build depth by layering: background → torn-paper middle layers → props → characters → a foreground strip (hills or ferns) that characters can pop up from behind.
* A subtle warm vignette over everything.
* Recurring layouts:
   * a character bottom-left looking up at a ransom-note title;
   * photos taped to a kraft board;
   * a row of objects appearing one per word;
   * a big central prop with small tags around it.
8. Motion language (JavaScript / GSAP)
* Pop-in with overshoot: from scale 0 and about ±12° rotation up to full size with back.out(2–3), pivoting at the bottom (the feet).
* Drop-in from above with a bounce, slide-in from off-frame, and hops with squash and stretch from the feet.
* Never frozen: everything on screen gets a gentle idle sway or bob (±1.5–4° rotation, a few pixels), with a finite number of repeats.
* Stop-motion boil: stepped random jitter at 8–10 fps for shivering, nerves, crying, fire flicker and shaking ground.
* Signature gags:
   * crowds or objects multiply (1 → 2 → 4 → 8 …);
   * things tear in half along matching jagged edges, and the halves fall away with scraps;
   * a paper-flip swap turns one thing into another: scaleX 1 → 0, swap the image, 0 → 1, with a puff of paper confetti;
   * things shrink in squashy steps;
   * photos get taped onto a board.
* Camera:
   * slow push-ins (scale 1 → about 1.03–1.04 over a scene);
   * stepped shakes on impacts;
   * occasional pans between stacked layers.
* Sync rule:
   * Every reveal lands on, or about 0.05 s before, the exact spoken word it illustrates.
   * One sentence equals one visual beat.
   * Never put everything on screen at once; reveal it across the scene.
* Snappy and playful: anticipation → action → follow-through. Never floaty, never corporate, no linear motion.
* For reliable rendering, use only seeded randomness, only finite repeats, and a timeline that can jump to any frame.
9. Scene transitions
* Default: a new full-frame paper sheet slides over the previous scene from one side.
   * It takes 0.5–0.7 s with power3.out and settles from a slight rotation.
   * Its torn leading edge shows white paper fibers, with a drop shadow.
   * Vary the direction each scene: right, left, top, bottom.
* Variations:
   * a heavy dark sheet dropping from the top for somber beats (power2.inOut, about 0.9 s, small settle bounce);
   * a fast whip (about 0.4 s, expo.out) for urgency;
   * a white flash or bloom for explosions.
* Start each incoming sheet about 0.3 s after the previous line's last word so the punchline lands.
* No exit animations: the next sheet is the exit.
10. Writing style of the narration
* Tone: a warm, wry, gentle storybook narrator. Dry understatement, never snarky or mean. Speaks inclusively ("we", "you").
* Hook: open with a big question, which also appears on screen as the ransom-note title.
* Sentences:
   * Short (about 5–9 words) and lots of fragments.
   * Lots of periods, with pauses after punchlines.
   * Conversational asides ("for, well, forever").
* Rule of three with a deflating third beat: two straight items, then a deadpan comic one. Example: "Philosophers wrote enormous books. The stars kept quiet. And the cat said: 'Nap.'"
* Facts:
   * Deliver them as concrete images and comparisons, not a pile of statistics.
   * Use at most one number per sentence ("a rock the size of Mount Everest").
   * Use lists of short sensory fragments.
* Ending: a turn near the end ("Turns out…" or "But…"), then a warm, witty closing line or instruction that ties back to the opening question.
* Every sentence must work as one visual gag.
* Pacing: the original style is slow, about 110 words per minute of video. If the script is 140–160 words, shorten the long pauses after recording so the video stays near 60 seconds.
11. Sound
* Music:
   * A whimsical storybook track: pizzicato strings, ukulele, glockenspiel, soft clarinet and light brushed percussion, about 100 BPM, instrumental.
   * It sits about 15–20 dB under the voice.
   * Turn it down or muffle it (low-pass) for somber moments; let it swell slightly on the end card.
* Paper-craft sound effects, kept subtle:
   * soft paper swishes for sheet transitions;
   * light taps for ransom letters;
   * cartoon pops when cutouts appear;
   * a boing for hops;
   * a paper-tear sound when things tear;
   * a thud for drops;
   * a sparkle chime for magic moments.
* Bigger booms and rumbles only for real drama.
* Final loudness: about −14 LUFS, with peaks below −1.5 dBFS.
12. Generating the image elements (Higgsfield, GPT Image 2.5)
* Cutouts (transparent background, 2K, high quality). Prompt template:
"Paper-cutout sticker asset for a stop-motion collage animation, on a FULLY TRANSPARENT background. Hand-painted watercolor + colored-pencil children's-storybook illustration, cut out of watercolor paper with a thin clean white paper border following the whole silhouette (die-cut sticker edge). Single isolated object, centered, whole object visible with generous margin, flat straight-on view, no cast shadow, no ground, no scenery, no text. Palette: tomato red, mustard yellow, teal, ultramarine, olive, sage green, blush pink, cream. Cute round design, small black dot eyes, rosy blush cheeks. Match the character designs and art style of the attached storyboard sheet. SUBJECT: …"
   * Attach the approved storyboard grid, or an earlier character cutout, as an image reference for consistency.
   * Trim the transparent margins before use.
   * Backgrounds (opaque, 16:9):
   * blank textured cream watercolor paper;
   * blank kraft cardboard;
   * watercolor skies with layered torn-paper hills (no characters);
   * navy starry night with white splatter stars;
   * sooty charcoal sky with a torn-paper ground strip.
   * Storyboard grid: one 16:9 image with 3×3 panels, thin cream gutters, and a small number tag on each panel. Describe each panel in order, all in the style above.
   * Built in code, not generated as images (HTML/CSS/SVG):
   * ransom letters, captions and tags;
   * washi tape, confetti and doodles;
   * underlines;
   * screens and simple interface elements.```
