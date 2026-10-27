/* components/badge.js - condition / assumption / mismatch / result / scale badges as label CHIPS (design system v2.0.0).
 *
 * mount(container, fixture, opts) -> { el, set(state), box }
 *   container: an SVG element (the chip is placed in that SVG's user space = its HTML host's px) or an HTML element
 *   opts: { fx: 'display.condition', style: 'condition'|'assumption'|'mismatch'|'result'|'scale', x, y (centre), id }
 *   set({ opacity: 0..1, dim: 0..1 })  dim > 0.5: the chip turns to muted grid paper (a condition that no longer
 *   holds; pair it with StrikeThrough for the shape cue).
 * The label text is a fixture value (data-fx). Chip colour = meaning (tokens.chips.roles via tokens.badge).
 */
(function () {
'use strict';
const D = window.Diki;

function mount(container, fixture, opts) {
  const T = D.T, role = T.badge[opts.style || 'condition'] || 'label';
  const host = D.hostOf(container);
  const style = T.chips.roles[role], mutedStyle = T.chips.roles.muted;
  const el = D.chip(null, { fx: opts.fx, role, kind: 'lbl', id: opts.id, rot: opts.rot == null ? -1.5 : opts.rot });
  D.place(el, host, opts.x, opts.y, opts.anchor || 'middle');
  const base = el.className.replace('chip-' + style, '').replace(/\s+/g, ' ').trim(), fg = T.chips.styles.find(x => x.name === style).fg;
  function set(s) {                                   // writes the whole class and colour every time: same DOM for the same t
    if (s.opacity != null) el.style.opacity = D.op(s.opacity);
    const d = (s.dim || 0) > 0.5;
    el.className = base + ' chip-' + (d ? mutedStyle : style);
    el.style.color = d ? D.color('muted') : fg;
  }
  const r = el.getBoundingClientRect();
  return { el, set, box: { x: opts.x - r.width / 2, y: opts.y - r.height / 2, w: r.width, h: r.height } };
}

D.Components.badge = { mount };
})();
