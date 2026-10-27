/* components/caption.js - burnt-in caption lane as a paper chip (design system v2.0.0). Used ONLY in the
 * 'captioned' layout (A2: the caption lane exists only when captions are burnt in).
 *
 * mount(container, fixture, opts) -> { set({ t }), chunks }
 *   container: the caption lane div; opts.sheet: the cue sheet (words[] timing + meta.beats_text verbatim text)
 * Text is the approved beat text with punctuation (beats_text), split into chunks of <= type.caption.max_words
 * words, breaking after . ? ! ; and after a comma once a chunk has 3 words. A chunk shows from its first word
 * (minus the reveal lead) until the next chunk, the beat end + 0.4 s, or a think window. Opacity only.
 * Outro beats (outro.brand / outro.disclosure) are never captioned: the end card carries the brand (PD-20).
 */
(function () {
'use strict';
const D = window.Diki;

function mount(container, fixture, opts) {
  const T = D.T, S = opts.sheet, beats = (S.meta && S.meta.beats_text) || [], think = (S.meta && S.meta.think_windows) || [];
  const chunks = [];
  beats.forEach(b => {
    if (T.brand.endcard_slots.includes(b.slot) || !b.word_range) return;
    const toks = b.text.split(/\s+/).filter(x => /[\p{L}\p{N}]/u.test(x));
    let [i] = b.word_range, cur = [];
    const flush = () => { if (cur.length) chunks.push({ toks: cur.map(c => c.tok), t0: S.words[cur[0].i].t0, end: b.end + 0.4 }); cur = []; };
    toks.forEach(tok => {
      cur.push({ tok, i }); i++;
      if (/[.?!;:]$/.test(tok) || cur.length >= T.type.caption.max_words || (/,$/.test(tok) && cur.length >= 3)) flush();
    });
    flush();
  });
  chunks.forEach((c, n) => {
    const nx = chunks[n + 1]; if (nx && nx.t0 - T.motion.lead < c.end) c.end = nx.t0 - T.motion.lead;
    think.forEach(w => { if (w.start >= c.t0 && w.start < c.end) c.end = w.start; });
    const el = D.div('caption', container); el.lang = S.language;
    D.div('', el, 'span').textContent = c.toks.join(' ');
    c.el = el;
    if (el.firstChild.offsetHeight > container.clientHeight + 1) D._warn('W_CAPTION_OVERFLOW', 'caption chunk "' + el.textContent + '" exceeds the caption lane');
  });
  const lead = T.motion.lead, dur = T.motion.verbs.Reveal.dur;
  function set({ t }) {
    chunks.forEach(c => {
      const a = Math.max(0, c.t0 - lead), o = D.prog(t, a, dur, 'out') * (1 - D.prog(t, c.end - dur * 0.75, dur * 0.75, 'out'));
      c.el.style.opacity = D.op(o);
    });
  }
  return { set, chunks };
}

D.Components.caption = { mount };
})();
