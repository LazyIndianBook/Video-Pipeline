/* components/chemistry_species.js - reaction formula + atom group + atom ledger from ONE state (v2.0.0, collage:
 * the formula and the ledger sit on taped paper sheets, every atom is a cut-out sticker with a cream outline).
 *
 * mount(container, fixture, opts) -> { svg, hero, el: { formula, coef: {id: el}, atoms: {id: el}, ledger }, set(state) }
 *   fixture[opts.reaction || 'reaction'] = {
 *     species: [ { id: 'h2', side: 'L'|'R', formula: [ ['H', 2] ] }, ... ],   // element symbol, subscript
 *     stages:  { unbalanced: { h2: 1, o2: 1, h2o: 1 }, balanced: { h2: 2, ... } },  // coefficients
 *     counts?: { balanced: { L: { H: 4, O: 2 }, R: { H: 4, O: 2 } } } }              // optional cross-check
 *   fixture.display: elements { H: 'H', ... }, plus '+', arrow '→', marks { eq: '=', ne: '≠' }
 * set(state): coef_<speciesId> number (StateTable tweens it; molecules fade in/out one by one and the column
 *   re-centres, so EXISTING atoms keep their identity and slide), atoms 0..1, ledger 0..1, fx { coef_<id>: path }.
 * Invariants: true subscripts (tspan at type.subscript.scale, >= 40 px), coefficients full size; coefficient 1
 * is not drawn; the ledger counts are DERIVED from the same coefficients as the atoms (never typed) and are
 * checked against fixture counts at mount (E_FIXTURE_MISMATCH); '≠' is the only red glyph.
 */
(function () {
'use strict';
const D = window.Diki;

function mount(container, fixture, opts = {}) {
  const T = D.T, RX = opts.reaction || 'reaction', R = D.fx(RX), C = r => D.color(r);
  const W = container.clientWidth, H = container.clientHeight;
  const sheets = D.div('', container); sheets.style.cssText = 'position:absolute;inset:0';   // paper sheets behind the SVG
  const svg = D.svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}` }, container);
  svg.style.overflow = 'visible'; svg.style.position = 'absolute'; svg.style.left = '0'; svg.style.top = '0';
  const g = D.svg('g', { id: opts.id || 'reaction' }, svg);
  const EQ = T.type.equation.size;
  const text = (attrs, parent) => { const e = D.svg('text', Object.assign({ 'font-weight': T.type.equation.weight, fill: C('ink') }, attrs), parent || g); e.style.fontFamily = 'var(--font-math)'; return e; };
  const elFill = el => (T.color.chem[el] || { fill: '#FFFFFF', stroke: T.color.ink, text: T.color.ink });

  // --- counts derived from coefficients x subscripts; cross-check the fixture
  const sp = R.species;
  const countsFor = coefs => { const c = { L: {}, R: {} }; sp.forEach(s => s.formula.forEach(([e, n]) => { c[s.side][e] = (c[s.side][e] || 0) + n * coefs[s.id]; })); return c; };
  for (const stage in (R.counts || {})) {
    const got = countsFor(R.stages[stage]);
    for (const side of ['L', 'R']) for (const e in R.counts[stage][side]) if (got[side][e] !== R.counts[stage][side][e])
      throw D.fail('E_FIXTURE_MISMATCH', stage + ' ' + side + ' ' + e + ' derived ' + got[side][e] + ' != fixture ' + R.counts[stage][side][e]);
  }
  const elements = []; sp.forEach(s => s.formula.forEach(([e]) => { if (!elements.includes(e)) elements.push(e); }));
  const maxCoef = {}; sp.forEach(s => { maxCoef[s.id] = Math.max(...Object.values(R.stages).map(st => st[s.id])); });

  // --- formula row: [coef slot][species]  +  ...  →  ...   (one text per species; true subscripts)
  const formula = D.svg('g', { id: 'formula' }, g), yF = EQ * 1.15;
  const probe = text({ 'font-size': EQ }, formula); probe.textContent = '8'; const slot = probe.getComputedTextLength() + 6; probe.remove();
  const coefEl = {}, items = [];
  sp.forEach((s, si) => {
    if (si && sp[si - 1].side === s.side) items.push({ glyph: 'display.plus' });
    if (si && sp[si - 1].side !== s.side) items.push({ glyph: 'display.arrow' });
    items.push({ species: s, si });
  });
  let x = 0; const gap = 0.32 * EQ;
  items.forEach(it => {
    if (it.glyph) { const e = D.text(text({ 'font-size': EQ, x, y: yF, fill: C('muted') }, formula), it.glyph); it.el = e; it.w = e.getComputedTextLength(); x += it.w + gap; return; }
    const s = it.species, ce = text({ id: 'coef_' + s.id, 'font-size': EQ, x: x + slot - 6, y: yF, 'text-anchor': 'end', fill: C('chem.coefficient') }, formula);
    coefEl[s.id] = ce; x += slot;
    const t = text({ id: 'formula_' + s.id, 'font-size': EQ, x, y: yF }, formula);
    D.formula(t, s.formula, RX + '.species.' + it.si + '.formula', EQ);
    it.el = t; x += t.getComputedTextLength() + gap;
  });
  const fw = x - gap, fx0 = (W - fw) / 2;
  if (fw > W + 1) D._warn('W_FORMULA_OVERFLOW', 'formula ' + Math.round(fw) + ' px > lane ' + W);
  formula.querySelectorAll('text').forEach(e => e.setAttribute('x', (parseFloat(e.getAttribute('x')) + fx0).toFixed(1)));
  D.sheetEl(sheets, { x: Math.round(Math.max(0, fx0 - 34)), y: 0, w: Math.round(Math.min(W, fw + 68)), h: Math.round(yF + 0.42 * EQ + 18) }, [['teal', 0.15], ['pink', 0.85]]);

  // --- atom group: one molecule per coefficient unit; atoms keep ids across coefficient changes
  const rowP = 86, ly0 = H - rowP * elements.length - 10;              // ledger rows sit at the bottom of the lane
  const ar = 46, step = ar * 1.55, pitch = ar * 2.5, cy = (yF + 40 + ly0) / 2;   // atom group centred between formula and ledger
  const atomsG = D.svg('g', { id: 'atoms' }, g), atomEl = {}, mols = [];
  ['L', 'R'].forEach(side => {
    const list = sp.filter(s => s.side === side), x0 = side === 'L' ? 0 : W / 2 + 50, x1 = side === 'L' ? W / 2 - 50 : W;
    list.forEach((s, ci) => {
      const colX = x0 + (x1 - x0) * (ci + 0.5) / list.length;
      const order = []; s.formula.forEach(([e, n]) => { for (let j = 0; j < n; j++) order.push(e); });
      if (order.length === 3) { const single = s.formula.find(([, n]) => n === 1); if (single) { const i = order.indexOf(single[0]); order.splice(i, 1); order.splice(1, 0, single[0]); } }
      for (let k = 0; k < maxCoef[s.id]; k++) {
        const mg = D.svg('g', { id: 'mol_' + s.id + '_' + k, filter: 'url(#cut-sm)' }, atomsG), atoms = [];
        order.forEach((e, j) => {
          const a = D.svg('g', { id: `atom_${s.id}_${k}_${e}${j}`, 'data-identity': `${s.id}#${k}:${e}${j}` }, mg), f = elFill(e);
          const c = D.svg('circle', { r: ar, fill: f.fill, stroke: f.stroke, 'stroke-width': T.stroke.detail }, a);
          const l = D.text(text({ 'text-anchor': 'middle', 'font-size': T.type.atom_letter.size, 'font-weight': T.type.atom_letter.weight, fill: f.text }, a), 'display.elements.' + e);
          atoms.push({ c, l, dx: (j - (order.length - 1) / 2) * step }); atomEl[a.id] = a;
        });
        mols.push({ s, k, g: mg, atoms, colX });
      }
    });
  });
  const arrowMid = D.text(text({ 'font-size': EQ, x: W / 2, y: cy + EQ * 0.36, 'text-anchor': 'middle', fill: C('muted') }), 'display.arrow');

  // --- ledger: element | left count | mark | right count (derived)
  const ledger = D.svg('g', { id: 'ledger' }, g), LB = T.type.label.size, rows = {};
  const ledgerSheet = D.sheetEl(sheets, { x: Math.round(W / 2 - 270), y: Math.round(ly0 - 14), w: 540, h: Math.round(rowP * elements.length + 20) }, [['mustard', 0.5]]);
  elements.forEach((e, n) => {
    const y = ly0 + n * rowP + rowP / 2, f = elFill(e);
    D.svg('rect', { x: W / 2 - 230, y: y - 36, width: 72, height: 72, rx: 14, fill: f.fill, filter: 'url(#cut-sm)' }, ledger);
    D.text(text({ x: W / 2 - 194, y: y + LB * 0.36, 'text-anchor': 'middle', 'font-size': LB, fill: f.text }, ledger), 'display.elements.' + e);
    const mk = (xx, anchor) => text({ x: xx, y: y + LB * 0.36, 'text-anchor': anchor, 'font-size': LB }, ledger);
    rows[e] = { L: mk(W / 2 - 40, 'end'), M: mk(W / 2 + 20, 'middle'), R: mk(W / 2 + 80, 'start') };
  });
  const marks = { eq: D.fx('display.marks.eq'), ne: D.fx('display.marks.ne') };

  const op = v => (v < 1e-4 ? 0 : v > 0.9999 ? 1 : v).toFixed(4);
  const shown = c => Math.ceil(c - 1e-9);                       // a coefficient mid-tween shows its target integer
  function set(s) {
    const fx = s.fx || {}, coefs = {};
    sp.forEach(x => {
      const c = s['coef_' + x.id]; coefs[x.id] = shown(c);
      const e = coefEl[x.id]; e.textContent = String(coefs[x.id]); e.style.opacity = op(D.clamp01(c - 1));
      if (fx['coef_' + x.id]) e.setAttribute('data-fx', fx['coef_' + x.id]);
    });
    mols.forEach(m => {
      const c = s['coef_' + m.s.id], y = cy + (m.k - (c - 1) / 2) * pitch;
      m.g.style.opacity = op(D.clamp01(c - m.k) * (s.atoms == null ? 1 : s.atoms));
      m.atoms.forEach(a => { const ax = (m.colX + a.dx).toFixed(2); a.c.setAttribute('cx', ax); a.c.setAttribute('cy', y.toFixed(2)); a.l.setAttribute('x', ax); a.l.setAttribute('y', (y + T.type.atom_letter.size * 0.36).toFixed(2)); });
    });
    const cnt = countsFor(coefs);
    elements.forEach(e => {
      const r = rows[e], l = cnt.L[e] || 0, rr = cnt.R[e] || 0, ok = l === rr;
      r.L.textContent = l; r.R.textContent = rr; r.M.textContent = ok ? marks.eq : marks.ne;
      r.M.setAttribute('fill', ok ? C('ink') : C('mismatch'));
      r.L.setAttribute('data-derived', 'count:L:' + e); r.R.setAttribute('data-derived', 'count:R:' + e);
    });
    ledger.style.opacity = op(s.ledger == null ? 1 : s.ledger); ledgerSheet.style.opacity = ledger.style.opacity;
  }
  const init = {}; sp.forEach(x => { init['coef_' + x.id] = R.stages[Object.keys(R.stages)[0]][x.id]; });
  set(init);
  return { svg, hero: g, set, el: { formula, coef: coefEl, atoms: atomEl, ledger, arrow: arrowMid, rows } };
}

D.Components.chemistrySpecies = { mount };
})();
