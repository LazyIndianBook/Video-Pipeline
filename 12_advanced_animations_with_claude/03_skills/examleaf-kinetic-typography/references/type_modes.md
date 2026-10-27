# Type modes

All modes share one pattern: **build spans once in `window.ready`, set styles in `render(t)` from planned times.** Times come from `grapheme_clusters.py --plan` (or the same logic in the page). Easing helpers (`E.backOut`, `E.power3Out`, `prog`, `lerp`) are those in `examleaf-procedural-2d/references/primitives_catalog.md` §1; `rngAt` comes from `seeded_prng.js` (same formula as `scene_template.html`).

## 0. Shared pattern

```js
// ready(): one span per unit; lang per word; Indic font stack first for Indic words.
function buildUnits(box, plan, fontStack) {
  return plan.units.map(u => {
    const sp = document.createElement('span');
    sp.className = 'u'; sp.textContent = u.text; sp.lang = u.lang;
    sp.style.fontFamily = fontStack(u.lang);
    sp.style.display = 'inline-block';                 // needed for transforms; each unit is shaped on its own
    box.appendChild(sp);
    return { el: sp, at: u.at };
  });
}
// render(t): pure function of t.
function renderUnits(units, t, dur = 0.35) {
  for (const { el, at } of units) {
    const p = prog(t, at, dur);
    el.style.opacity = p === 0 ? 0 : 1;
    el.style.transform = 'translateY(' + lerp(30, 0, E.power3Out(p)) + 'px) scale(' + (p === 0 ? 0.8 : E.backOut(p, 2)) + ')';
  }
}
```

`inline-block` units are shaped independently. That is correct for grapheme clusters (each cluster is complete), but the Devanagari and Bengali-Assamese headline bar (shirorekha / matra) is drawn per unit: units must sit with zero letter-spacing and no rotation to keep the bar continuous. Where the bar matters (handwriting, labels, calm headlines), use **word** units or a mask wipe of the whole word.

## 1. Ransom-note tiles ([V4-MP])

- One tile per letter (Latin) or per grapheme cluster (Indic), each tile a different colour pairing and display font, rotation within ±6°, small vertical jitter, small drop shadow; some Latin letters lowercase.
- Tiles slap on 0.04–0.05 s apart, synced to the spoken word (`--stagger 0.045`).
- Tile styles: black/cream or mustard; cream/red or black; red/cream; ultramarine/mustard; mustard/black; pink/dark red or blue; red polka-dot; blue grid-paper; teal/cream ([V4-MP]).

```js
// ready(): seeded tile look per unit (stateless rngAt keeps any seek order identical).
function tileLook(seed, i, styles, fonts) {
  return { rot: (rngAt(seed, 3 * i) * 2 - 1) * 6, dy: (rngAt(seed, 3 * i + 1) * 2 - 1) * 8,
           style: styles[Math.floor(rngAt(seed, 3 * i + 2) * styles.length) % styles.length],
           font: fonts[i % fonts.length] };
}
// render(t): slap-on = fast scale overshoot, then rest at the seeded rotation.
const slap = (t, at) => { const p = prog(t, at, 0.18); return { s: p === 0 ? 0 : E.backOut(p, 3), o: p === 0 ? 0 : 1 }; };
```

Indic tiles use the style's `devanagari` / `bengali_assamese` family for every tile (the [V4-MP] display fonts are Latin-only [Hypothesis; verify]). Keep tile count small: ransom titles are short.

## 2. Handwriting captions ([V4-MP])

- Caveat Brush in ink `#2b2622`, revealed like handwriting, often followed by a red pencil double underline drawn on in two slightly wobbly strokes.
- Latin: reveal per letter with a left-to-right clip.
- Indic: reveal per **word** with a left-to-right mask wipe across the word (keeps conjuncts and the headline bar intact). A handwriting-like Devanagari family (for example Kalam — verify coverage and licence) replaces Caveat Brush for Hindi.

```js
// Mask wipe of a whole word: clip-path inset from the right shrinks to 0.
const wipe = (t, at, dur = 0.5) => 'inset(0 ' + (100 * (1 - E.power3Out(prog(t, at, dur)))).toFixed(2) + '% 0 0)';
// Double underline: two strokes drawn on in sequence (drawOn from procedural-2d), second starts 0.12 s later.
```

## 3. Labels on washi-taped tags ([V4-MP])

- Patrick Hand (Latin) on cream paper tags held by a washi-tape strip; sometimes a red pencil check mark or circle draws on next to them.
- In ExamLeaf, a **science label's text comes from a fixture field** (e.g. `label: fx.labels.normal`), and its pointer geometry from the fixture. The tag animates; the content does not change.
- Indic labels: per word, Indic family, line-height ≥ 1.4.

## 4. Kinetic headline (motion-graphics style, [V3], [N50]–[N55])

- One orchestrated staggered entrance per beat [N53]: the group enters together with a stagger, then holds; no scattered micro-animations.
- Masks, slides, scale pops; dominant colour with one or two sharp accents [N52]; distinctive named display fonts, never Arial or Inter as display [N51] (Inter only for labels, captions and science text per the style tokens); rotate away from convergence fonts such as Space Grotesk [N55].
- For HTML, CSS-only motion is preferred by the cookbook [N54], but in a seek renderer CSS animations do not follow `seek(t)` (lint W03); set styles from `render(t)` or drive the Web Animations API with `currentTime`.

## 5. Equation callouts

- The equation's glyphs come from the fixture renderer (Manim CE, SVG, or a vetted math typesetter chosen by `examleaf-svg-scenes` / `examleaf-manim-scenes`); this mode only reveals and holds the element.
- Reveal the whole equation (fade or mask) on its cue; highlight a term with a finite pulse (≤2 periods) on an `emphasis` cue.
- Hold: until the narration has finished reading the equation, plus 0.5 s [Recommendation]; transformations of an equation hold 2–4 s after completion (tokens).
- Never scramble, retype, per-symbol animate or re-letter an equation; never move the camera during its reveal (#64).

## 6. Quiz prompts and recap lines

- Question text appears with the question cue; any answer stays hidden during the answer-hidden period (engine rule: a question can never have `answer_visible=true`; interaction skills own the timing).
- Recap lines use the kinetic headline mode with the longest hold of the scene.
