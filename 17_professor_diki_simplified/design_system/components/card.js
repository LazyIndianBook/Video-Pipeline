/* components/card.js - structured elements on the card sheet (design system v2.0.0, PD-18).
 * ONE card lane (layout 'carded') = a taped paper sheet; one card visible at a time (D.Card windows). Kinds:
 *   definition: { term: fxPath, text: fxPath, at?, role? }               a term (on a chip) and its one-line meaning
 *   points:     [{ fx, at?, role? }]                                     numbered points, each on its word
 *   table:      { head: [fxPath...], rows: [{ cells: [fxPath | {fx, dec?, role?, at?}], at? }] }   a small data table;
 *               a cell with `at` appears WHOLE on that reference (verb Card on the cell) inside a ruled empty slot,
 *               e.g. V and I from frame 0 and the V ÷ I cell only at the ratio beat
 * mount(container, fixture, opts) -> { el, rows: [{el, at}], set({opacity}) }
 *   opts: { id, kind, definition | points | table }   (opts.border is accepted for v1 scenes and ignored: the sheet
 *   is the frame)
 * Every string is a fixture value (data-fx, PD-13). A row with `at` appears whole on that reference (verb Card);
 * rows without `at` appear with the card. Taller than the lane: W_CARD_OVERFLOW; more than type.card.max_rows rows:
 * W_CARD_ROWS. Opacity only; nothing moves. The sheet (D.backdrop('card')) shows only while some card is visible.
 */
(function () {
'use strict';
const D = window.Diki;

const lanes = new Map();                       // container -> its cards

function mount(container, fixture, opts) {
  const T = D.T, K = opts.kind || 'definition';
  if (!lanes.has(container)) {
    lanes.set(container, []);
    const sheet = D.backdrop('card');
    D.track(t => { let m = 0; for (const c of lanes.get(container)) m = Math.max(m, parseFloat(c.style.opacity) || 0); if (sheet) sheet.style.opacity = D.op(m); }, 2);
  }
  const el = D.div('card card-' + K, container); if (opts.id) el.id = opts.id;   // .card-table: ruled row slots, so a table filling up is never an empty box
  lanes.get(container).push(el);
  const rows = [];
  const cell = (parent, spec, cls, cellAt) => {          // cellAt: only TABLE cells may carry their own `at`
    const s0 = typeof spec === 'string' ? { fx: spec } : spec, s = cellAt ? s0 : Object.assign({}, s0, { at: null });
    const c = D.div(cls || 'card-cell', s.at != null ? null : parent, 'span');
    if (s.role) c.style.color = D.color(s.role);
    D.text(c, s.fx, s.dec);
    if (s.at != null) {                                       // cell-level reveal: a ruled empty slot until its reference
      const slot = D.div('card-slot', parent, 'span'); slot.appendChild(c); D.Card(c, s.at); return c;
    }
    return c;
  };
  const row = (at, cls) => { const r = D.div('card-row ' + cls, el); rows.push({ el: r, at: at == null ? null : at }); return r; };
  if (K === 'definition') {
    const d = opts.definition, r = row(d.at, 'card-def');
    const term = D.chip(r, { fx: d.term, role: d.role || 'result', kind: 'lbl', rot: -2 }); term.classList.add('card-term');
    D.div('', r); cell(r, { fx: d.text }, 'card-text');
  } else if (K === 'points') opts.points.forEach((p, i) => { const r = row(p.at, 'card-point'); D.div('card-num', r, 'span').textContent = String(i + 1); cell(r, p, 'card-text'); });
  else if (K === 'table') { const tb = opts.table; if (tb.head) { const h = row(null, 'card-head'); tb.head.forEach(x => cell(h, x)); } tb.rows.forEach(rw => { const r = row(rw.at, 'card-tr'); rw.cells.forEach(x => cell(r, x, null, true)); }); }
  else throw D.fail('E_READY', 'card kind ' + K);
  rows.forEach(r => { if (r.at == null) r.el.style.opacity = 1; else D.Card(r.el, r.at); });
  if (rows.length > T.type.card.max_rows) D._warn('W_CARD_ROWS', 'card ' + (opts.id || K) + ' has ' + rows.length + ' rows > ' + T.type.card.max_rows);
  if (el.scrollHeight > container.clientHeight - 28 + 1) D._warn('W_CARD_OVERFLOW', 'card ' + (opts.id || K) + ' exceeds the card lane');
  const set = s => { if (s.opacity != null) el.style.opacity = s.opacity; };
  return { el, rows, set };
}

D.Components.card = { mount };
})();
