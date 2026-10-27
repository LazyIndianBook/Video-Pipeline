/* components/biology_tracer.js - compartments, material vs energy arrows, carbon tracer (design system v2.0.0,
 * the reference collage look: each compartment is a tinted taped paper sheet (sky, grass, paper...) with its name on a
 * chip, arrows are two-tone (cream outline under the stroke), the carbon token is the charcoal C sticker).
 *
 * mount(container, fixture, opts) -> { svg, hero, el: { compartments, stations, material: [paths], energy, token, scale }, set(state) }
 *   fixture[opts.tracer || 'tracer'] = {
 *     compartments: [ { id: 'air', label: 'display.bio.air' }, ... ]            // stacked top -> bottom
 *     stations: [ { id: 'co2', compartment: 'air', formula?: [['C',1],['O',2]], name?: 'display.bio.sugar' }, ... ]
 *     energy: { label: 'display.bio.light', into: 'leaf' },  scale_note: 'display.bio.scale_note' }
 * set(state): tracer 0..n-1 (station index; fractional = travelling along the material arrow), stations 0..n
 *   (station k visible when stations > k), material 0..1, energy 0..1, scale 0..1.
 * Invariants: material arrows are solid (bio.material), the energy arrow is a dashed wave (bio.energy) that ENDS
 * in its compartment (energy does not become wood); the tracer token is ONE object (one carbon) for the whole
 * scene; the scale disclosure badge says the picture is schematic. Formulae use true subscripts (D.formula).
 */
(function () {
'use strict';
const D = window.Diki;

function mount(container, fixture, opts = {}) {
  const T = D.T, PX = opts.tracer || 'tracer', TR = D.fx(PX), C = r => D.color(r);
  const W = container.clientWidth, H = container.clientHeight;
  const sheets = D.div('', container); sheets.style.cssText = 'position:absolute;inset:0';
  const svg = D.svg('svg', { width: W, height: H, viewBox: `0 0 ${W} ${H}` }, container);
  svg.style.overflow = 'visible'; svg.style.position = 'absolute'; svg.style.left = '0'; svg.style.top = '0';
  const tints = T.color.bio.compartment_tints, OUT = T.sticker.outline_color;
  const two = (attrs, parent) => { D.svg('path', Object.assign({}, attrs, { stroke: OUT, 'stroke-width': attrs['stroke-width'] + 8, 'stroke-dasharray': 'none' }), parent); return D.svg('path', attrs, parent); };
  const g = D.svg('g', { id: opts.id || 'tracer' }, svg);
  const LB = T.type.label.size, EQ = T.type.equation.size;
  const text = (attrs, parent, math) => { const e = D.svg('text', Object.assign({ 'font-weight': T.type.label.weight, fill: C('ink') }, attrs), parent || g); e.style.fontFamily = math ? 'var(--font-math)' : 'var(--font-sans)'; return e; };

  // compartments stacked; the bottom strip keeps room for the scale badge
  const n = TR.compartments.length, gap = 20, top = 0, bottom = H - 104, ch = (bottom - top - gap * (n - 1)) / n;
  const comp = {};
  TR.compartments.forEach((c, i) => {
    const y = top + i * (ch + gap), cg = D.svg('g', { id: 'comp_' + c.id }, g);
    const sh = D.sheetEl(sheets, { x: 0, y: Math.round(y), w: W, h: Math.round(ch) }, [[['teal', 'pink', 'mustard'][i % 3], 0.62]]); sh.style.background = tints[i % tints.length];
    const lc = D.chip(null, { fx: c.label, role: 'label', kind: 'lbl', rot: -2 }); D.place(lc, container, 16, y + 44, 'start');
    comp[c.id] = { y, h: ch, g: cg };
  });

  // stations: text centred at sx, tracer anchor on the right-hand track at tx
  const sx = W * 0.62, tx = W - 92, anchors = [], stEl = [];
  TR.stations.forEach((s, i) => {
    const c = comp[s.compartment], sg = D.svg('g', { id: 'station_' + s.id }, g);
    let y = c.y + c.h / 2 + (s.formula && s.name ? -18 : 18);
    if (s.formula) { D.formula(text({ x: sx, y, 'text-anchor': 'middle', 'font-size': EQ, 'font-weight': T.type.equation.weight }, sg, true), s.formula, PX + '.stations.' + i + '.formula', EQ); y += LB + 18; }
    if (s.name) D.text(text({ x: sx, y, 'text-anchor': 'middle', 'font-size': LB, fill: C('ink') }, sg), s.name);
    anchors.push({ x: tx, y: c.y + c.h / 2 }); stEl.push(sg);
  });

  // material arrows between consecutive anchors (solid), arrowhead at the end
  const tokR = 40, mat = D.svg('g', { id: 'material' }, g), matPaths = [];
  for (let i = 0; i + 1 < anchors.length; i++) {
    const a = anchors[i], b = anchors[i + 1], y0 = a.y + tokR + 12, y1 = b.y - tokR - 14;
    matPaths.push(two({ d: `M${a.x},${y0} L${b.x},${y1}`, fill: 'none', stroke: C('bio.material'), 'stroke-width': T.stroke.arrow, 'stroke-linecap': 'round' }, mat));
    two({ d: `M${b.x - 18},${y1 - 22} L${b.x},${y1 + 2} L${b.x + 18},${y1 - 22}`, fill: 'none', stroke: C('bio.material'), 'stroke-width': T.stroke.arrow, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, mat);
  }

  // energy arrow: dashed wave from the top compartment into energy.into, ending there
  const top0 = comp[TR.compartments[0].id].y, en = D.svg('g', { id: 'energy' }, g), into = comp[TR.energy.into], ex = 200, ey0 = top0 + LB + 30, ey1 = into.y + into.h * 0.55;   // clear of the compartment labels (x < 140)
  let d = `M${ex},${ey0}`; for (let y = ey0 + 6; y <= ey1; y += 6) d += ` L${(ex + 14 * Math.sin((y - ey0) / 50 * 2 * Math.PI)).toFixed(1)},${y}`;
  two({ d, fill: 'none', stroke: C('bio.energy'), 'stroke-width': T.stroke.arrow, 'stroke-dasharray': '18 12', 'stroke-linecap': 'round' }, en);
  two({ d: `M${ex - 18},${ey1 - 18} L${ex},${ey1 + 6} L${ex + 18},${ey1 - 18}`, fill: 'none', stroke: C('bio.energy'), 'stroke-width': T.stroke.arrow, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, en);
  const enChip = D.chip(null, { fx: TR.energy.label, role: 'condition', kind: 'lbl', rot: 2 }); D.place(enChip, container, ex + 34, top0 + 44, 'start');   // energy label: mustard chip on the label row

  // the carbon tracer: one token for the whole scene
  const tok = D.svg('g', { id: 'carbon_token', 'data-identity': 'tracer#C', filter: 'url(#cut)' }, g), f = T.color.chem.C;
  const tc = D.svg('circle', { r: tokR, fill: f.fill }, tok);
  const tl = D.text(text({ 'text-anchor': 'middle', 'font-size': T.type.atom_letter.size, 'font-weight': T.type.atom_letter.weight, fill: f.text }, tok, true), 'display.elements.C');

  const scale = D.Components.badge.mount(g, fixture, { id: 'scale_badge', fx: TR.scale_note, style: 'scale', x: W / 2, y: H - 48 });

  const op = v => (v < 1e-4 ? 0 : v > 0.9999 ? 1 : v).toFixed(4);
  function set(s) {
    const k = Math.max(0, Math.min(anchors.length - 1, s.tracer || 0)), i = Math.min(anchors.length - 2, Math.floor(k)), u = k - i;
    const p = anchors.length > 1 ? { x: D.lerp(anchors[i].x, anchors[i + 1].x, u), y: D.lerp(anchors[i].y, anchors[i + 1].y, u) } : anchors[0];
    tc.setAttribute('cx', p.x.toFixed(2)); tc.setAttribute('cy', p.y.toFixed(2));
    tl.setAttribute('x', p.x.toFixed(2)); tl.setAttribute('y', (p.y + T.type.atom_letter.size * 0.36).toFixed(2));
    const st = s.stations == null ? anchors.length : s.stations;
    stEl.forEach((e, j) => { e.style.opacity = op(D.clamp01(st - j)); });
    mat.style.opacity = op(s.material == null ? 1 : s.material);
    en.style.opacity = op(s.energy == null ? 1 : s.energy); enChip.style.opacity = en.style.opacity;
    scale.set({ opacity: s.scale == null ? 1 : s.scale });
  }
  set({ tracer: 0 });
  return { svg, hero: g, set, el: { compartments: comp, stations: stEl, material: matPaths, energy: en, token: tok, scale: scale.el } };
}

D.Components.biologyTracer = { mount };
})();
