/* components/physics_circuit.js - persistent series loop as cut-out STICKERS on the workbench (v2.0.0):
 * battery, resistor <-> filament lamp, ammeter; ink wires; every label on a chip.
 *
 * mount(container, fixture, opts) -> { svg, hero, el: {...}, set(state) }
 *   container: the diagram lane div (any size; the loop fills the lane height, text never scales)
 *   opts.fx: override any fixture path below (defaults match the Ohm example fixture)
 * set(state), all keys optional after the first call (StateTable passes the full state every frame):
 *   v, i       number (tweened by StateTable) or null -> shows display.ui.unknown ("?"), decimals from the fixture
 *   load       0 = resistor, 1 = filament lamp, between = cross-fade IN PLACE (SwapPart; the wires never move)
 *   heat       0..1 heat rays around the lamp + the glass glows (heat changes the condition)
 *   badge      0..1 condition chip opacity;  badgeDim 0..1 condition no longer holds (pair with StrikeThrough)
 *   fx         { v: path, i: path } fixture path of the value at rest, written to data-fx for the text diff
 * Layout (lane-relative; fits the 584 px 'carded' lane and the 864 px default lane), three rows inside the loop that
 * never touch: label chip above the top wire | condition chip under the load | I chip beside the ammeter; the V chip
 * sits left of the battery above the bottom wire. Colour by meaning: battery + V chip royal (voltage), ammeter + I chip
 * teal (current), resistor / lamp + R and condition chips mustard (resistance / condition). Labels >= 52 px.
 */
(function () {
'use strict';
const D = window.Diki;
const DEF = {
  r_label: 'display.r_label', r_value: 'parameters.resistance_ohm', r_unit: 'display.r_unit',
  v_label: 'display.v_label', v_unit: 'display.v_unit', i_label: 'display.i_label', i_unit: 'display.i_unit',
  ammeter: 'display.ammeter_symbol', condition: 'display.condition', lamp_label: 'display.lamp_label',
  unknown: 'display.ui.unknown', dec_v: 'display.decimals.v', dec_i: 'display.decimals.i'
};

function mount(container, fixture, opts = {}) {
  const T = D.T, P = Object.assign({}, DEF, opts.fx || {}), H = T.color.hue;
  const W = container.clientWidth, Hh = container.clientHeight;
  const svg = D.svg('svg', { width: W, height: Hh, viewBox: `0 0 ${W} ${Hh}` }, container);
  svg.style.overflow = 'visible'; svg.style.position = 'absolute'; svg.style.left = '0'; svg.style.top = '0';
  const g = D.svg('g', { id: opts.id || 'circuit' }, svg);

  // geometry: label row | top wire + load | condition row | ammeter + I row | V row | bottom wire + battery
  const xc = W / 2, xL = 40, xR = W - 40, aR = 56, half = 150;
  const yLabel = 46, yTop = 166, yBadge = yTop + 110, yBot = Hh - 66;
  const yA = Math.max(yBadge + 94, Math.round((yBadge + yBot) / 2) - 10), yV = yBot - 76;
  const wire = { fill: 'none', stroke: D.color('line.ink'), 'stroke-width': T.stroke.wire, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };

  // ink wires: one closed loop with gaps only where a part sits. Never redrawn.
  D.svg('path', Object.assign({ d: `M${xc - half},${yTop} L${xL},${yTop} L${xL},${yBot} L${xc - 78},${yBot} M${xc + 86},${yBot} L${xR},${yBot} L${xR},${yTop} L${xc + half},${yTop}` }, wire), g);
  // the load slot keeps its leads in both states (the loop is closed in every state)
  D.svg('path', Object.assign({}, wire, { d: `M${xc - half},${yTop} L${xc - 112},${yTop} M${xc + 112},${yTop} L${xc + half},${yTop}` }), g);

  // battery sticker on the bottom wire: royal body, navy end, cream + and - marks (shapes, not text), terminal nub
  const cell = D.sticker(g, { id: 'cell' });
  D.svg('rect', { x: xc - 78, y: yBot - 36, width: 150, height: 72, rx: 14, fill: H.royal }, cell);
  D.svg('rect', { x: xc - 78, y: yBot - 36, width: 40, height: 72, rx: 14, fill: H.navy }, cell);
  D.svg('rect', { x: xc + 72, y: yBot - 14, width: 14, height: 28, rx: 4, fill: H.ink }, cell);
  D.svg('path', { d: `M${xc + 40},${yBot - 14} v28 M${xc + 26},${yBot} h28 M${xc - 68},${yBot} h20`, stroke: H.paper, 'stroke-width': 6, 'stroke-linecap': 'round' }, cell);

  // load 1: resistor sticker (mustard capsule, colour bands, ink leads)
  const res = D.sticker(g, { id: 'resistor' });
  D.svg('path', { d: `M${xc - 112},${yTop} L${xc - 96},${yTop} M${xc + 96},${yTop} L${xc + 112},${yTop}`, stroke: H.ink, 'stroke-width': T.stroke.wire, 'stroke-linecap': 'round' }, res);
  D.svg('rect', { x: xc - 100, y: yTop - 34, width: 200, height: 68, rx: 30, fill: H.mustard }, res);
  [[-52, H.soil_dark], [-22, H.black], [8, H.black], [52, H.leaf_light]].forEach(([dx, c]) => D.svg('rect', { x: xc + dx - 8, y: yTop - 34, width: 16, height: 68, fill: c }, res));
  D.svg('path', { d: `M${xc - 80},${yTop - 18} C${xc - 40},${yTop - 26} ${xc + 30},${yTop - 26} ${xc + 76},${yTop - 18}`, stroke: H.paper, 'stroke-width': 5, 'stroke-linecap': 'round', fill: 'none', opacity: 0.55 }, res);

  // load 2: filament lamp sticker in the same slot: glass bulb on the wire, ink filament, screw cap; glow + rays = heat
  const lamp = D.svg('g', { id: 'lamp' }, g);
  const glow = D.svg('circle', { cx: xc, cy: yTop, r: 92, fill: T.color.highlight, opacity: 0 }, lamp);
  const lampS = D.sticker(lamp, {});
  D.svg('path', { d: `M${xc - 112},${yTop} L${xc - 62},${yTop} M${xc + 62},${yTop} L${xc + 112},${yTop}`, stroke: H.ink, 'stroke-width': T.stroke.wire, 'stroke-linecap': 'round' }, lampS);
  const glass = D.svg('circle', { cx: xc, cy: yTop, r: 60, fill: H.paper, stroke: H.mustard, 'stroke-width': 10 }, lampS);
  D.svg('path', { d: `M${xc - 44},${yTop} L${xc - 26},${yTop} L${xc - 16},${yTop - 16} L${xc - 4},${yTop + 14} L${xc + 8},${yTop - 16} L${xc + 18},${yTop + 14} L${xc + 26},${yTop} L${xc + 44},${yTop}`, stroke: H.ink, 'stroke-width': 6, fill: 'none', 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, lampS);
  const heat = D.sticker(g, { id: 'heat' }, 'sm');
  [[-0.5, -0.866], [0.5, -0.866], [-0.9, -0.42], [0.9, -0.42]].forEach(([dx, dy], k) =>
    D.svg('line', { x1: xc + dx * 74, y1: yTop + dy * 74, x2: xc + dx * 90, y2: yTop + dy * 90, stroke: k < 2 ? H.brick : H.mustard, 'stroke-width': 9, 'stroke-linecap': 'round' }, heat));

  // ammeter sticker on the right wire: teal ring, cream face hides the wire, the A symbol from the fixture
  const amm = D.sticker(g, { id: 'ammeter' });
  D.svg('circle', { cx: xR, cy: yA, r: aR, fill: H.outline, stroke: H.teal, 'stroke-width': 12 }, amm);
  const aTxt = D.svg('text', { x: xR, y: yA + 20, 'text-anchor': 'middle', 'font-size': 56, 'font-weight': 800, fill: D.color('current') }, amm);
  aTxt.style.fontFamily = 'var(--font-sans)'; D.text(aTxt, P.ammeter);

  // labels on chips (HTML over the SVG, same px), colour by meaning
  const host = container;
  const chipOf = (id, role, parts, kind) => {
    const c = D.chip(null, { role, kind: kind || 'lbl', id, rot: 0 }); const spans = [];
    parts.forEach((p, n) => { if (n) c.appendChild(document.createTextNode(' ')); const s = D.div('', c, 'span'); if (p) D.text(s, p); spans.push(s); });
    return { c, spans };
  };
  const R = chipOf('r_label', 'resistance', [P.r_label, P.r_value, P.r_unit]); D.place(R.c, host, xc, yLabel, 'middle'); R.c.dataset.rot = '-2';
  const LL = chipOf('lamp_label', 'resistance', [P.lamp_label]); D.place(LL.c, host, xc, yLabel, 'middle'); LL.c.dataset.rot = '-2';
  const V = chipOf('v_label', 'voltage', [P.v_label, null, P.v_unit], 'readout'); D.place(V.c, host, xc - 100, yV, 'end'); V.c.dataset.rot = '1.5';
  const I = chipOf('i_readout', 'current', [P.i_label, null, P.i_unit], 'readout'); D.place(I.c, host, xR - aR - 22, yA, 'end'); I.c.dataset.rot = '-1.5';
  [R, LL, V, I].forEach(x => { x.c.style.transform = 'rotate(' + x.c.dataset.rot + 'deg)'; });

  const badge = D.Components.badge.mount(svg, fixture, { id: 'cond_badge', fx: P.condition, style: 'condition', x: xc, y: yBadge });

  const decV = D.dec(P.dec_v), decI = D.dec(P.dec_i), unknown = D.fx(P.unknown);
  const op = D.op;
  const val = (span, v, dec, path) => {
    if (v == null) { span.textContent = unknown; span.setAttribute('data-fx', P.unknown); span.removeAttribute('data-fx-dec'); return; }
    span.textContent = D.fmt(v, dec);
    if (path) span.setAttribute('data-fx', path);
    span.setAttribute('data-fx-dec', String(dec));
  };
  function set(s) {
    const fx = s.fx || {};
    val(V.spans[1], s.v, decV, fx.v); val(I.spans[1], s.i, decI, fx.i);
    const load = s.load || 0, h = s.heat || 0;
    res.style.opacity = op(1 - load); R.c.style.opacity = op(1 - load);
    lamp.style.opacity = op(load); LL.c.style.opacity = op(load);
    heat.style.opacity = op(h * load); glow.setAttribute('opacity', (0.85 * h * load).toFixed(4));
    glass.setAttribute('fill', h * load > 0.5 ? T.color.highlight : H.paper);
    badge.set({ opacity: s.badge == null ? 0 : s.badge, dim: s.badgeDim || 0 });
  }
  set({ v: null, i: null, load: 0, heat: 0, badge: 0 });
  return { svg, hero: g, set, el: { circuit: g, cell, resistor: res, lamp, heat, ammeter: amm, r_label: R.c, lamp_label: LL.c, v_label: V.c, v_value: V.spans[1], i_readout: I.c, i_value: I.spans[1], badge: badge.el } };
}

D.Components.physicsCircuit = { mount };
})();
