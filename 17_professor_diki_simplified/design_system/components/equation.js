/* components/equation.js - result/equation lane: term-by-term layouts with identity (design system v2.0.0: terms are text on the result sheet; colour by meaning).
 *
 * mount(container, fixture, opts) -> { svg, el(id), set({from, to, p}), drive(steps, {initial}) }
 *   opts.terms:  { id: { parts: [ {fx: 'path', dec?: 'path'|n} ... ], role: 'voltage'|'current'|'resistance'|'ink'|'muted'|'mismatch',
 *                        italic?: true (quantity symbols) } }
 *   opts.states: { name: { layout: 'line', terms: [ids], size? }
 *                       | { layout: 'grid', rows: [ { l: [ids], m: [ids], r: [ids] } ... ], size? },
 *                  ...  optional per state: roles: { id: role } (e.g. the expected value muted in a mismatch) }
 * Every glyph (operators too) comes from the fixture. A term id that appears in two states is ONE object:
 * EquationTransform moves it (x, y, font-size as SVG attributes); terms only in the old state fade out,
 * terms only in the new state fade in. Positions are SVG attributes, so the DOM is identical for the same t.
 */
(function () {
'use strict';
const D = window.Diki;

function mount(container, fixture, opts) {
  const T = D.T, W = container.clientWidth, H = container.clientHeight;
  const svg = D.svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}`, class: 'eq-svg' }, container);
  svg.style.overflow = 'visible';
  const els = {}, widths = {};                                  // widths at font-size 100
  for (const id in opts.terms) {
    const def = opts.terms[id];
    const tx = D.svg('text', { id: 'eq_' + id, x: 0, y: 0, 'font-size': 100, 'font-weight': T.type.equation.weight, fill: D.color(def.role || 'ink'), opacity: 0 }, svg);
    tx.style.fontFamily = 'var(--font-math)';
    if (def.italic) tx.setAttribute('font-style', 'italic');
    def.parts.forEach((pt, i) => { if (i) tx.appendChild(document.createTextNode('\u00A0')); D.text(D.svg('tspan', {}, tx), pt.fx, pt.dec); });   // NBSP between parts: chrome, not science
    els[id] = tx; widths[id] = tx.getComputedTextLength();
  }
  const wOf = (id, size) => widths[id] * size / 100;
  const layouts = {};
  for (const name in opts.states) {
    const st = opts.states[name], pos = {};
    if (st.layout === 'grid') {
      const size = st.size || T.type.compare.size, gap = 0.28 * size, col = 0.55 * size, pitch = size * 1.22;
      const gw = ids => ids.reduce((s, id) => s + wOf(id, size), 0) + Math.max(0, ids.length - 1) * gap;
      const Lw = Math.max(...st.rows.map(r => gw(r.l || []))), Mw = Math.max(...st.rows.map(r => gw(r.m || []))), Rw = Math.max(...st.rows.map(r => gw(r.r || [])));
      const total = Lw + col + Mw + col + Rw, x0 = (W - total) / 2;
      if (total > W + 1) D._warn('W_EQ_OVERFLOW', 'equation state ' + name + ' is ' + Math.round(total) + ' px > lane ' + W);
      const top = (H - st.rows.length * pitch) / 2;
      st.rows.forEach((r, ri) => {
        const y = top + ri * pitch + 0.82 * size;
        const place = (ids, x) => ids.forEach(id => { pos[id] = { x, y, size }; x += wOf(id, size) + gap; });
        place(r.l || [], x0 + Lw - gw(r.l || []));                      // left column right-aligned
        place(r.m || [], x0 + Lw + col + (Mw - gw(r.m || [])) / 2);   // marks centred
        place(r.r || [], x0 + Lw + col + Mw + col);                   // right column left-aligned
      });
    } else {
      const size = st.size || T.type.equation.size, gap = 0.3 * size;
      const total = st.terms.reduce((s, id) => s + wOf(id, size), 0) + (st.terms.length - 1) * gap;
      if (total > W + 1) D._warn('W_EQ_OVERFLOW', 'equation state ' + name + ' is ' + Math.round(total) + ' px > lane ' + W);
      let x = (W - total) / 2; const y = H / 2 + 0.36 * size;
      st.terms.forEach(id => { pos[id] = { x, y, size }; x += wOf(id, size) + gap; });
    }
    for (const id in pos) if (!els[id]) throw new Error('equation state ' + name + ' uses unknown term ' + id);
    layouts[name] = pos;
  }
  const roleIn = (name, id) => (opts.states[name] && opts.states[name].roles && opts.states[name].roles[id]) || opts.terms[id].role || 'ink';

  /* pure: paints the blend between two named states at progress p (0..1) */
  function set({ from, to, p }) {
    const A = from ? layouts[from] : null, B = to ? layouts[to] : null;
    for (const id in els) {
      const a = A && A[id], b = B && B[id], el = els[id];
      let q, o;
      if (a && b) { q = { x: D.lerp(a.x, b.x, p), y: D.lerp(a.y, b.y, p), size: D.lerp(a.size, b.size, p) }; o = 1; }
      else if (a) { q = a; o = 1 - D.clamp01(p / 0.4); }            // leaving terms are gone by 40 %
      else if (b) { q = b; o = D.clamp01((p - 0.4) / 0.6); }        // arriving terms start at 40 %: no pile-up mid-transform
      else { q = { x: 0, y: 0, size: 100 }; o = 0; }                 // canonical when absent: same DOM for the same t
      el.setAttribute('x', q.x.toFixed(2)); el.setAttribute('y', q.y.toFixed(2)); el.setAttribute('font-size', q.size.toFixed(2));
      el.setAttribute('opacity', (o < 1e-4 ? 0 : o).toFixed(4));
      el.setAttribute('fill', D.color(a || b ? roleIn(p < 0.5 && from ? from : to || from, id) : opts.terms[id].role || 'ink'));
    }
  }

  /* registers ONE track for this equation from verb steps (D.CompareStates / D.EquationTransform / D.RevealMismatch) */
  function drive(steps, o = {}) {
    const S = steps.map(s => ({ ...s, dur: D._stepDur(s) })).sort((a, b) => a.at - b.at);
    S.forEach(s => {
      if (!layouts[s.state]) throw new Error('unknown equation state ' + s.state);
      if (s.verb === 'CompareStates' && opts.states[s.state].layout !== 'grid') D._warn('W_VERB_MISUSE', 'CompareStates to non-grid state ' + s.state);
      if (s.verb === 'RevealMismatch') {
        const mis = Object.keys(layouts[s.state]).filter(id => roleIn(s.state, id) === 'mismatch');
        if (!mis.length) D._warn('W_VERB_MISUSE', 'RevealMismatch state ' + s.state + ' has no mismatch term');
        if (s.emphasize !== false) mis.forEach(id => D.Emphasize(els[id], s.at + s.dur));
      }
    });
    D.track(t => {
      let prev = o.initial || null, cur = null;
      for (const s of S) { if (t < s.at - D.EPS) break; prev = cur ? cur.state : prev; cur = s; }
      if (!cur) set({ from: null, to: o.initial || null, p: 1 });
      else set({ from: prev, to: cur.state, p: D.prog(t, cur.at, cur.dur, 'standard') });
    });
  }
  return { svg, el: id => els[id], set, drive, layouts };
}

D.Components.equation = { mount };
})();
