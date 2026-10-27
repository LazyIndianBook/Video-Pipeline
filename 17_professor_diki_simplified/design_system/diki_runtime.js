/* diki_runtime.js - Professor Diki Simplified scene runtime, design system v2.0.0 (seek contract 1.0.0).
 *
 * The paper cut-out collage house style for every subject (PD-19): a full-bleed torn-paper world per subject,
 * sticker objects with cream outlines, ransom-note word chips, taped paper sheets, paper grain.
 * Loaded by diki_scene_base.html after tokens.js. Everything here is a pure function of t once ready() has
 * built the state: verbs register "tracks" (render functions); render(t) runs every track in order.
 * No clock, no rAF, no unseeded randomness, no CSS animation; opacity, transform and SVG attributes are written
 * from seek(t) only. The world is generated ONCE in init from fixed token seeds (it never changes per frame).
 *
 * Phases: phase 1 tracks set state (component set(), values, opacity, transform). Phase 2 tracks MEASURE the DOM
 * (halos, link lines, strike lines, focus rings, tape) and therefore run after every phase-1 write.
 * One owner per property: two verbs must never write the same property of the same element; drive shared
 * objects through one StateTable or one Equation track instead.
 *
 * Time references (never hard-coded seconds):  'cue:c04'  'beat:b03.start'  'beat:b03.end'
 *   'think:b02.start'  'think:b02.end'  'end'   plus an optional offset: 'cue:c04+0.7'.
 */
(function () {
'use strict';
const T = window.DIKI_TOKENS;
const D = window.Diki = { T, version: '2.0.1', Components: {} };
const EPS = 1e-6, SVGNS = 'http://www.w3.org/2000/svg';
const MV = T.motion.verbs, LEAD = T.motion.lead;

/* ---------- context ---------- */
let SHEET, FX, report, fail, STAGE, LAYOUT, BEATS = [], THINK = [];
const tracks = [[], []];            // [phase1, phase2]
const intervals = [];               // verb activity windows, for the think-window stillness check
const warned = new Set();
const warnOnce = (code, msg, t) => { if (warned.has(code + msg)) return; warned.add(code + msg); report(code, 'warning', msg, t); };
D._warn = (code, msg) => warnOnce(code, msg);

D.init = function (ctx) {
  SHEET = ctx.sheet; FX = ctx.fx; report = ctx.report; fail = ctx.fail; STAGE = ctx.stage; D.fail = fail;
  D.layoutName = ctx.layout || (ctx.captions ? 'captioned' : 'default'); LAYOUT = T.lanes[D.layoutName];
  if (!LAYOUT) throw fail('E_READY', 'unknown layout ' + D.layoutName + ' (tokens.lanes)');
  D.subject = ctx.subject || 'physics';
  if (!T.world.subjects[D.subject]) throw fail('E_READY', 'unknown subject ' + D.subject + ' (tokens.world.subjects)');
  STAGE.classList.add('subject-' + D.subject);
  const meta = SHEET.meta || {};
  BEATS = Array.isArray(meta.beats_text) ? meta.beats_text : [];
  THINK = Array.isArray(meta.think_windows) ? meta.think_windows : [];
  if (!BEATS.length) report('W_NO_BEATS_TEXT', 'warning', 'cue sheet has no meta.beats_text: no headlines, no end card');
  D.sheet = SHEET; D.beats = BEATS; D.think = THINK; D.lanes = LAYOUT;
  D.underlay = document.getElementById('underlay'); D.overlay = document.getElementById('overlay');
  placeLanes(); buildDefs(); buildWorld(); buildSheets();
};

/* ---------- small helpers ---------- */
const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
const lerp = (a, b, u) => a + (b - a) * u;
D.clamp01 = clamp01; D.lerp = lerp; D.EPS = EPS;
const EASE = {
  linear: u => u,
  out: u => 1 - Math.pow(1 - u, 3),                                          // cubic out: reveals, pops, slides
  standard: u => u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2,  // cubic in-out: transforms, no overshoot
  pulse: u => Math.sin(Math.PI * u)                                          // 0 -> 1 -> 0, one finite bump
};
D.prog = (t, t0, dur, ease) => {
  if (t < t0 - EPS) return 0;
  const u = dur > 0 ? clamp01((t - t0) / dur) : 1;
  return (EASE[ease || 'standard'])(u);
};
const s0 = x => (x < 1e-4 ? 0 : x > 0.9999 ? 1 : x).toFixed(4);
D.op = s0;
D.svg = (tag, attrs, parent) => {
  const e = document.createElementNS(SVGNS, tag);
  for (const k in attrs || {}) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
};
D.div = (cls, parent, tag) => { const e = document.createElement(tag || 'div'); if (cls) e.className = cls; if (parent) parent.appendChild(e); return e; };
/* stateless seeded randomness: same (seed, i) -> same value in any order. Chips use D.rngAt (seeded by ?seed=);
 * the world uses the fixed per-band token seeds so it never depends on the render seed. */
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const rng = (seed, i) => mulberry32((seed ^ Math.imul(i + 1, 0x9E3779B1)) >>> 0)();
const SUBJECT_ROLES = ['page', 'paper', 'surface', 'rule'];
D.color = role => {                                       // semantic role -> hex; unknown roles are a bug, not a default
  let v;
  if (SUBJECT_ROLES.includes(role)) v = role === 'rule' ? T.world.subjects[D.subject].rule : role === 'page' ? T.color.hue.cream : T.color.hue.paper;
  else v = typeof T.color[role] === 'string' ? T.color[role] : role && role.split('.').reduce((o, k) => o && o[k], T.color);
  if (typeof v !== 'string') throw fail('E_READY', 'unknown colour role ' + role);
  return v;
};

/* ---------- fixture access (contract section 9) ---------- */
D.fx = path => {
  const v = String(path).split('.').reduce((o, k) => o == null ? o : o[k], FX);
  if (v === undefined) throw fail('E_FIXTURE_MISSING', 'fixture has no ' + path);
  return v;
};
D.dec = d => d == null ? null : (typeof d === 'string' ? D.fx(d) : d);
D.fmt = (v, dec) => dec == null ? String(v) : Number(v).toFixed(dec);
D.text = (el, path, dec) => {
  el.setAttribute('data-fx', path);
  if (dec != null) el.setAttribute('data-fx-dec', typeof dec === 'string' ? dec : String(dec));
  el.textContent = D.fmt(D.fx(path), D.dec(dec));
  return el;
};
D.bindFx = root => root.querySelectorAll('[data-fx]').forEach(el => {
  if (!el.textContent) el.textContent = D.fmt(D.fx(el.dataset.fx), D.dec(el.dataset.fxDec));
});

/* true-subscript formula into an SVG <text>: formula = [['C', 6], ['H', 12], ...]; symbols from display.elements.<El>,
 * subscripts from <fxPrefix>.<i>.1, at type.subscript.scale x size, dropped by drop_em x size. Never Unicode subscripts. */
D.formula = (textEl, formula, fxPrefix, size) => {
  const SUB = T.type.subscript, drop = (SUB.drop_em * size).toFixed(1);
  if (SUB.scale * size < SUB.floor - EPS) warnOnce('W_SUBSCRIPT_SMALL', 'subscript ' + (SUB.scale * size).toFixed(1) + ' px < ' + SUB.floor + ' px');
  formula.forEach(([e, n], i) => {
    D.text(D.svg('tspan', i && formula[i - 1][1] > 1 ? { dy: '-' + drop } : {}, textEl), 'display.elements.' + e);
    if (n > 1) D.text(D.svg('tspan', { 'font-size': (SUB.scale * size).toFixed(1), dy: drop }, textEl), fxPrefix + '.' + i + '.1');
  });
  return textEl;
};

/* ---------- time references ---------- */
D.when = ref => {
  if (typeof ref === 'number') return ref;
  const m = /^([a-z]+)(?::([^+\-]+))?([+\-]\d*\.?\d+)?$/.exec(String(ref));
  if (!m) throw fail('E_READY', 'bad time reference ' + ref);
  const off = m[3] ? parseFloat(m[3]) : 0, arg = m[2] || '';
  const [id, edge] = arg.split('.');
  let base;
  if (m[1] === 'cue') {
    const c = SHEET.cues.find(c => c.id === arg);
    if (!c) throw fail('E_CUE_MISSING', 'cue sheet has no cue ' + arg);
    base = c.at;
  } else if (m[1] === 'beat') {
    const b = BEATS.find(b => b.id === id);
    if (!b) throw fail('E_CUE_MISSING', 'cue sheet has no beat ' + id);
    base = b[edge || 'start'];
  } else if (m[1] === 'think') {
    const w = THINK.find(w => w.beat === id);
    if (!w) throw fail('E_CUE_MISSING', 'cue sheet has no think window for ' + id);
    base = w[edge || 'start'];
  } else if (m[1] === 'end') base = window.DURATION;
  else throw fail('E_READY', 'bad time reference ' + ref);
  return base + off;
};

/* ---------- verb bookkeeping ---------- */
function verbDur(verb, override) {
  const spec = MV[verb]; const d = override == null ? spec.dur : override;
  const [lo, hi] = T.motion.range[spec.class];
  if (d < lo - EPS || d > hi + EPS) warnOnce('W_VERB_DURATION', verb + ' duration ' + d + ' s outside ' + spec.class + ' range ' + lo + '-' + hi + ' s');
  return d;
}
/* hidden overlay shapes go back to a canonical geometry, so the DOM (not only the pixels) is the same for the same t
 * whatever the seek history (contract section 2.2) */
const CANON = { rect: ['x', 'y', 'width', 'height'], line: ['x1', 'y1', 'x2', 'y2'], path: [] };
const hide = (...els) => els.forEach(e => {
  if (e.namespaceURI !== SVGNS) { e.style.opacity = 0; e.style.left = '0px'; e.style.top = '0px'; return; }
  e.setAttribute('opacity', 0); (CANON[e.tagName] || []).forEach(a => e.setAttribute(a, 0)); if (e.tagName === 'path') e.setAttribute('d', 'M0,0');
});
const note = (verb, t0, dur, still) => intervals.push({ verb, t0, t1: t0 + dur, still: !!still });
D.hide = hide;
D.track = (fn, phase) => { tracks[phase === 2 ? 1 : 0].push(fn); };

const stageRect = () => STAGE.getBoundingClientRect();
D.box = el => {
  const r = el.getBoundingClientRect(), s = stageRect();
  return { x: r.left - s.left, y: r.top - s.top, w: r.width, h: r.height };
};
function effOpacity(el) {
  let o = 1;
  for (let e = el; e && e !== STAGE; e = e.parentNode) { const v = e.style && e.style.opacity; if (v !== '' && v != null) o *= parseFloat(v); }
  return o;
}
D.effOpacity = effOpacity;
/* visibility window helper: 1 inside [a, u), eased in/out over dur; a window that starts at 0 is up at frame 0 */
const win = (t, a, u, dur) => (a <= EPS ? 1 : D.prog(t, a, dur, 'out')) * (u == null ? 1 : 1 - D.prog(t, u, dur, 'out'));

/* =========================== MOTION VERBS ===========================
 * Each verb takes resolved elements and time references, registers its track and returns a handle.
 * Durations are fixed per verb (tokens.motion.verbs); an override outside the class range warns.
 */

/* Reveal: opacity 0 -> 1 (no movement, no scale). Optional until: fades out again. */
D.Reveal = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur('Reveal', o.dur), u = o.until != null ? D.when(o.until) : null;
  note('Reveal', a, dur); if (u != null) note('Reveal', u, dur);
  D.track(t => { el.style.opacity = s0(win(t, a, u, dur)); });
  return { at: a };
};

/* transform owner for Pop / Slide / Chips / Tape: base rotation (data-rot, deg) + the verb's scale or travel.
 * SVG elements scale about their own box centre. */
const prepXf = el => { if (el.namespaceURI === SVGNS) { el.style.transformBox = 'fill-box'; el.style.transformOrigin = '50% 50%'; } return parseFloat(el.dataset.rot || 0); };
const xf = (rot, sc, dx, dy) => (dx || dy ? 'translate(' + dx.toFixed(2) + 'px,' + dy.toFixed(2) + 'px) ' : '') + 'rotate(' + rot.toFixed(2) + 'deg) scale(' + sc.toFixed(4) + ')';

/* Pop: opacity + scale 0.94 -> 1 over 0.26 s, ease out (no overshoot). Leaving (until) reverses it. Stickers,
 * chips, sheets. at <= 0 means visible at frame 0. */
D.Pop = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur(o.verb || 'Pop', o.dur), u = o.until != null ? D.when(o.until) : null, S0 = T.motion.pop_scale0;
  note(o.verb || 'Pop', a, dur); if (u != null) note(o.verb || 'Pop', u, dur);
  const rot = prepXf(el);
  D.track(t => { const v = win(t, a, u, dur); el.style.opacity = s0(v); el.style.transform = xf(rot, S0 + (1 - S0) * v, 0, 0); });
  return { at: a };
};

/* Slide: opacity + 24 px travel (from 'up' | 'down' | 'left' | 'right', default 'up' = arrives moving up). */
D.Slide = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur('Slide', o.dur), u = o.until != null ? D.when(o.until) : null, px = T.motion.slide_px;
  note('Slide', a, dur); if (u != null) note('Slide', u, dur);
  const dir = { up: [0, 1], down: [0, -1], left: [1, 0], right: [-1, 0] }[o.from || 'up'], rot = prepXf(el);
  D.track(t => { const v = win(t, a, u, dur), k = (1 - v) * px; el.style.opacity = s0(v); el.style.transform = xf(rot, 1, dir[0] * k, dir[1] * k); });
  return { at: a };
};

/* Chips: a whole phrase of chips appears TOGETHER (stagger 30 ms by index, <= 40 ms; never word-by-word). */
D.Chips = (row, at, o = {}) => {
  const chips = Array.from(row.querySelectorAll('.chip')), st = Math.min(T.motion.chip_stagger_s, T.motion.chip_stagger_max_s);
  const a = D.when(at);
  chips.forEach((c, i) => D.Pop(c, a <= EPS ? 0 : a + i * st, { verb: 'Chips', until: o.until }));
  return { at: a, chips };
};

/* Tape: a washi strip appears on the top edge of el (opacity + scale 0.94 -> 1). color: pink | mustard | teal;
 * pos: 0..1 along the top edge. The strip follows el (measured in phase 2). */
D.Tape = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur('Tape', o.dur), S0 = T.motion.pop_scale0, TP = T.tape;
  note('Tape', a, dur);
  const strip = D.div('tape tape-' + (o.color || 'pink'), D.overlayHtml());
  const rot = o.rot == null ? TP.rot_deg : o.rot;
  D.track(t => {
    const v = a <= EPS ? 1 : D.prog(t, a, dur, 'out');
    if (v <= 0) { strip.style.opacity = 0; strip.style.left = '0px'; strip.style.top = '0px'; strip.style.transform = xf(rot, S0, 0, 0); return; }
    const b = D.box(el);
    strip.style.left = Math.round(b.x + b.w * (o.pos == null ? 0.5 : o.pos)) + 'px'; strip.style.top = Math.round(b.y - TP.h / 2) + 'px';
    strip.style.opacity = s0(v); strip.style.transform = xf(rot, S0 + (1 - S0) * v, 0, 0);
  }, 2);
  return { at: a, el: strip };
};
let overlayHtml = null;
D.overlayHtml = () => { if (!overlayHtml) { overlayHtml = D.div('', STAGE); overlayHtml.id = 'overlay-html'; overlayHtml.style.cssText = 'position:absolute;inset:0;z-index:4;pointer-events:none'; } return overlayHtml; };

/* Card: a structured element (components/card.js) or one of its rows appears WHOLE on its word (PD-18). Several
 * visibility windows: D.Card(el, null, { windows: [[at, until], ...] }); a window starting at 0 is up at frame 0. */
D.Card = (el, at, o = {}) => {
  const wins = (o.windows || [[at, o.until]]).map(([a, u]) => [D.when(a), u == null ? null : D.when(u)]), dur = verbDur('Card', o.dur);
  wins.forEach(([a, u]) => { note('Card', a, dur); if (u != null) note('Card', u, dur); });
  D.track(t => { let m = 0; for (const [a, u] of wins) m = Math.max(m, win(t, a, u, dur)); el.style.opacity = s0(m); });
  return { at: wins[0][0] };
};

/* PreserveObject: el is the same object for the rest of the scene. QA: once visible it must stay visible
 * (effective opacity >= 0.99) to the end, end card included; otherwise W_PERSIST_BROKEN. */
const preserved = [];
D.PreserveObject = (el, o = {}) => { preserved.push({ el, from: o.from != null ? D.when(o.from) : 0, name: o.name || el.id }); return el; };
D.track(t => {
  for (const p of preserved) if (t >= p.from + MV.Reveal.dur - EPS && effOpacity(p.el) < 0.99) warnOnce('W_PERSIST_BROKEN', 'preserved object ' + p.name + ' hidden at t=' + t.toFixed(2), t);
}, 2);

/* ChangeValue: a number tweens between two fixture values with fixed decimals (from the fixture). */
D.ChangeValue = (el, from, to, at, o = {}) => {
  const a = D.when(at), dur = verbDur('ChangeValue', o.dur), dec = D.dec(o.dec);
  const v0 = D.fx(from), v1 = D.fx(to);
  if (typeof v0 !== 'number' || typeof v1 !== 'number') throw fail('E_READY', 'ChangeValue needs numeric fixture values: ' + from + ', ' + to);
  note('ChangeValue', a, dur);
  if (o.dec != null) el.setAttribute('data-fx-dec', String(o.dec));
  D.track(t => {
    const p = D.prog(t, a, dur, 'standard');
    el.textContent = D.fmt(lerp(v0, v1, p), dec);
    el.setAttribute('data-fx', p <= 0 ? from : p >= 1 ? to : from + '->' + to);
  });
};

/* Emphasize: one finite halo bump BEHIND the element (underlay). Never scales, never wobbles. */
D.Emphasize = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur('Emphasize', o.dur), pad = o.pad == null ? 12 : o.pad;
  note('Emphasize', a, dur);
  const r = D.svg('rect', { rx: T.radius.focus, fill: D.color(o.color || 'highlight'), opacity: 0 }, D.underlay);
  D.track(t => {
    const p = D.prog(t, a, dur, 'pulse');
    if (p <= 1e-3) { hide(r); return; }
    const b = D.box(el);
    r.setAttribute('x', (b.x - pad).toFixed(1)); r.setAttribute('y', (b.y - pad).toFixed(1)); r.setAttribute('width', (b.w + 2 * pad).toFixed(1)); r.setAttribute('height', (b.h + 2 * pad).toFixed(1));
    r.setAttribute('opacity', (T.color.halo_alpha * p).toFixed(4));
  }, 2);
};

/* TracePath: draws an SVG path along its length. ONLY when the drawing is the mechanism (a flow, a route). */
D.TracePath = (pathEl, at, o = {}) => {
  const a = D.when(at), dur = verbDur('TracePath', o.dur); let len = null;
  note('TracePath', a, dur);
  D.track(t => {
    if (len == null) { len = pathEl.getTotalLength(); pathEl.setAttribute('stroke-dasharray', len + ' ' + len); }
    pathEl.setAttribute('stroke-dashoffset', (len * (1 - D.prog(t, a, dur, 'standard'))).toFixed(2));
  });
};

/* two-tone overlay line: a cream outline under the coloured stroke, so it reads on every band */
const twoTone = (tag, color, w, extra) => {               // every attribute exists from creation: DOM order never depends on seek history
  const g = D.svg('g', { opacity: 0 }, D.overlay), geo = tag === 'line' ? { x1: 0, y1: 0, x2: 0, y2: 0 } : { d: 'M0,0' };
  const under = D.svg(tag, Object.assign({}, geo, { stroke: T.sticker.outline_color, 'stroke-width': w + 8, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', fill: 'none' }, extra && extra.under), g);
  const over = D.svg(tag, Object.assign({}, geo, { stroke: color, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', fill: 'none' }, extra && extra.over), g);
  return { g, parts: [under, over], reset: () => { g.setAttribute('opacity', 0); [under, over].forEach(l => { for (const k in geo) l.setAttribute(k, geo[k]); }); } };
};

/* StrikeThrough: a mismatch (brick) line with a cream outline across the element (overlay). Shape cue for red. */
D.StrikeThrough = (el, at, o = {}) => {
  const a = D.when(at), dur = verbDur('StrikeThrough', o.dur), u = o.until != null ? D.when(o.until) : null;
  note('StrikeThrough', a, dur);
  const L = twoTone('line', D.color('line.' + (o.color || 'mismatch')), T.stroke.strike);
  D.track(t => {
    const p = D.prog(t, a, dur, 'out') * (u == null ? 1 : 1 - D.prog(t, u, dur, 'out'));
    if (p <= 0) { L.reset(); return; }
    L.g.setAttribute('opacity', p.toFixed(4));
    const b = D.box(el);
    L.parts.forEach(l => { l.setAttribute('x1', (b.x - 10).toFixed(1)); l.setAttribute('y1', (b.y + b.h * 0.6).toFixed(1)); l.setAttribute('x2', (b.x + b.w + 10).toFixed(1)); l.setAttribute('y2', (b.y + b.h * 0.4).toFixed(1)); });
  }, 2);
};

/* MapSymbol: links a symbol (usually an equation term) to the object it names: a two-tone dashed connector that
 * leaves the symbol upward, runs through a side gutter (o.side 'left'|'right') and enters the object from below;
 * halos on both ends. Appears by opacity (no draw-on), holds until `until`. */
D.MapSymbol = (symEl, objEl, at, o = {}) => {
  const a = D.when(at), dur = verbDur('MapSymbol', o.dur), u = o.until != null ? D.when(o.until) : null;
  note('MapSymbol', a, dur);
  const L = twoTone('path', D.color('line.' + (o.color || 'resistance')), T.stroke.link, { over: { 'stroke-dasharray': T.stroke.link_dash } });
  const halos = [symEl, objEl].map(() => D.svg('rect', { rx: T.radius.focus, fill: D.color('highlight'), opacity: 0 }, D.underlay));
  D.track(t => {
    const p = D.prog(t, a, dur, 'out') * (u == null ? 1 : 1 - D.prog(t, u, dur, 'out'));
    if (p <= 0) { L.reset(); hide(...halos); return; }
    L.g.setAttribute('opacity', p.toFixed(4)); halos.forEach(h => h.setAttribute('opacity', (0.8 * T.color.halo_alpha * p).toFixed(4)));
    const s = D.box(symEl), b = D.box(objEl), scx = s.x + s.w / 2, bcx = b.x + b.w / 2;
    const left = o.side ? o.side === 'left' : (scx + bcx) / 2 < T.canvas.width / 2;
    const gx = left ? T.lanes.x0 - 40 : T.lanes.x1 + 40, ys = s.y - 22, yb = b.y + b.h + 40;
    const d = `M${scx.toFixed(1)},${(s.y - 4).toFixed(1)} L${scx.toFixed(1)},${ys.toFixed(1)} L${gx},${ys.toFixed(1)} L${gx},${yb.toFixed(1)} L${bcx.toFixed(1)},${yb.toFixed(1)} L${bcx.toFixed(1)},${(b.y + b.h + 4).toFixed(1)}`;
    L.parts.forEach(l => l.setAttribute('d', d));
    [s, b].forEach((r, i) => { const h = halos[i]; h.setAttribute('x', (r.x - 8).toFixed(1)); h.setAttribute('y', (r.y - 8).toFixed(1)); h.setAttribute('width', (r.w + 16).toFixed(1)); h.setAttribute('height', (r.h + 16).toFixed(1)); });
  }, 2);
};

/* PauseForPrediction: during a think window, a dashed ink focus ring marks the answer slot(s). Nothing else moves
 * (QA: W_MOTION_IN_THINK). The think plate (a taped sheet with the prompt) is chrome, driven by meta.think_windows. */
D.PauseForPrediction = (targets, beatId, o = {}) => {
  const s = D.when('think:' + beatId + '.start'), e = D.when('think:' + beatId + '.end'), dur = verbDur('PauseForPrediction', o.dur);
  note('PauseForPrediction', s, e - s, true);
  const rings = targets.map(() => D.svg('rect', { rx: T.radius.focus, fill: 'none', stroke: D.color(o.color || 'ink'), 'stroke-width': T.stroke.focus, 'stroke-dasharray': T.stroke.focus_dash, opacity: 0 }, D.overlay));
  D.track(t => {
    const p = D.prog(t, s - dur, dur, 'out') * (1 - D.prog(t, e, dur, 'out'));
    targets.forEach((el, i) => {
      const r = rings[i]; if (p <= 0) { hide(r); return; }
      r.setAttribute('opacity', p.toFixed(4));
      const b = D.box(el); r.setAttribute('x', (b.x - 14).toFixed(1)); r.setAttribute('y', (b.y - 10).toFixed(1)); r.setAttribute('width', (b.w + 28).toFixed(1)); r.setAttribute('height', (b.h + 20).toFixed(1));
    });
  }, 2);
};

/* Badge: a badge chip pops in whole and gets one emphasis bump; optional until. */
D.Badge = (el, at, o = {}) => {
  const a = D.when(at);
  D.Pop(el, a, { verb: 'Badge', until: o.until });
  if (o.emphasize !== false) D.Emphasize(el, a + MV.Badge.dur, {});
};

/* Equation-lane verbs: they return STEPS for equation.drive(); one equation = one track (one owner). */
D.CompareStates = (state, at) => ({ verb: 'CompareStates', state, at: D.when(at) });
D.EquationTransform = (state, at) => ({ verb: 'EquationTransform', state, at: D.when(at) });
D.RevealMismatch = (state, at, o = {}) => ({ verb: 'RevealMismatch', state, at: D.when(at), emphasize: o.emphasize });
D._stepDur = s => { const d = verbDur(s.verb); note(s.verb, s.at, d); return d; };

/* =========================== STATE TABLE ===========================
 * Binds NAMED states to time references and drives a component's set(state) as a pure function of t.
 *   D.StateTable(component, { states: { base: {...}, four: {...} }, initial: 'base',
 *                             steps: [ { at: 'cue:c04', state: 'four', verb: 'ChangeValue' }, ... ] })
 * Values: numbers, 'fx:path' (resolved from the fixture; the path is kept for QA), strings, booleans, null.
 * States merge onto the previous state. Numbers tween over the step's verb duration with the 'standard' ease
 * (no overshoot); a number after a null tweens from the last number shown; everything else switches at the step.
 */
D.StateTable = (component, spec) => {
  const resolve = st => { const v = {}, fx = {}; for (const k in st) { const x = st[k]; if (typeof x === 'string' && x.startsWith('fx:')) { fx[k] = x.slice(3); v[k] = D.fx(fx[k]); } else v[k] = x; } return { v, fx }; };
  if (!spec.states[spec.initial]) throw fail('E_READY', 'StateTable initial state missing: ' + spec.initial);
  const steps = spec.steps.map(s => {
    if (!spec.states[s.state]) throw fail('E_READY', 'StateTable state missing: ' + s.state);
    const at = D.when(s.at), dur = verbDur(s.verb || 'ChangeValue', s.dur); note(s.verb || 'ChangeValue', at, dur);
    return { at, dur, ...resolve(spec.states[s.state]) };
  }).sort((a, b) => a.at - b.at);
  const init = resolve(spec.states[spec.initial]);
  const at = t => {
    let cur = { ...init.v }, fx = { ...init.fx }; const lastNum = {};
    for (const k in cur) if (typeof cur[k] === 'number') lastNum[k] = cur[k];
    for (const s of steps) {
      if (t < s.at - EPS) break;
      const p = D.prog(t, s.at, s.dur, 'standard');
      for (const k in s.v) {
        const to = s.v[k], from = typeof cur[k] === 'number' ? cur[k] : lastNum[k];
        if (typeof to === 'number' && typeof from === 'number') cur[k] = lerp(from, to, p);
        else cur[k] = to;
        if (typeof to === 'number') lastNum[k] = to;
        if (k in s.fx) fx[k] = p >= 1 ? s.fx[k] : (fx[k] || '') + '->' + s.fx[k]; else if (k in fx) delete fx[k];
      }
    }
    return { ...cur, fx, t };
  };
  D.track(t => component.set(at(t)));
  return { at };
};

/* =========================== CHIPS, LABELS, STICKERS =========================== */
const CHIP = {}; T.chips.styles.forEach(s => { CHIP[s.name] = s; });
let chipIndex = 0;
const chipRng = i => (D.rngAt ? D.rngAt(7919 + i) : rng(20261016, 7919 + i));
/* one chip. o: { text | fx (+dec), style (chip style name) | role (chips.roles), kind: 'head' | 'lbl' | 'readout',
 *   id, rot (deg; default seeded +-rot_max by chip index for 'head'), lang } */
D.chip = (parent, o = {}) => {
  const style = o.style || T.chips.roles[o.role || 'label'];
  if (!CHIP[style]) throw fail('E_READY', 'unknown chip style ' + style);
  const c = D.div('chip chip-' + style + (o.kind && o.kind !== 'head' ? ' ' + o.kind : ''), parent, 'span');
  if (o.id) c.id = o.id;
  if (o.lang) c.lang = o.lang;
  if (o.fx) D.text(c, o.fx, o.dec); else if (o.text != null) c.textContent = o.text;
  const i = chipIndex++;
  const rot = o.rot != null ? o.rot : (chipRng(i) - 0.5) * 2 * T.chips.rot_max_deg * (o.kind && o.kind !== 'head' ? 0.5 : 1);
  const dy = o.kind && o.kind !== 'head' ? 0 : Math.round((chipRng(i + 5000) - 0.5) * 2 * T.chips.dy_max_px);
  c.dataset.rot = rot.toFixed(2);
  c.style.transform = xf(rot, 1, 0, 0);
  if (dy) c.style.marginTop = dy + 'px';
  return c;
};
/* a ransom-note row: one chip per word, headline_styles cycling (index*step+1) mod n (step coprime to n) so neighbours differ; text nodes keep the
 * spaces so row.textContent is the phrase exactly (fixture/brand diff). styles: optional fixed list. */
let styleIndex = 0;
D.chipRow = (parent, phrase, o = {}) => {
  const row = D.div('chiprow', parent); const words = String(phrase).split(/\s+/).filter(Boolean), names = T.chips.headline_styles;
  const gcd = (a, b) => b ? gcd(b, a % b) : a, step = [5, 3, 2, 1].find(k => k < names.length && gcd(k, names.length) === 1) || 1;   // coprime step: neighbours differ
  words.forEach((w, k) => {
    if (k) row.appendChild(document.createTextNode(' '));
    const style = o.styles ? o.styles[k % o.styles.length] : names[(styleIndex * step + 1) % names.length];
    if (!o.styles) styleIndex++;
    D.chip(row, { text: w, style, kind: 'head', lang: o.lang });
  });
  if (o.size) row.querySelectorAll('.chip').forEach(c => { c.style.fontSize = o.size + 'px'; });
  return row;
};
/* the brand sticker: all words but the last in .bs1, the last in .bs2; text nodes keep row.textContent == text */
D.brandSticker = (parent, text, o = {}) => {
  const s = D.div('brand-sticker' + (o.twoLine ? ' two' : ''), parent), w = String(text).split(/\s+/).filter(Boolean);
  D.div('bs1', s, 'span').textContent = w.slice(0, -1).join(' '); s.appendChild(document.createTextNode(' ')); D.div('bs2', s, 'span').textContent = w[w.length - 1];
  const tp = D.div('tape tape-' + T.brand.sticker.tape, s); tp.style.left = '18%'; tp.style.transform = 'rotate(-6deg)';
  if (o.size) s.style.fontSize = o.size + 'px';
  s.dataset.rot = String(o.rot == null ? -2 : o.rot); s.style.transform = 'rotate(' + s.dataset.rot + 'deg)';
  return s;
};
/* place an element by an anchor point (x, y in the host's px): anchor 'middle' (centre) | 'end' (right edge) | 'start' */
D.place = (el, host, x, y, anchor) => {
  const a = D.div('anchor' + (anchor && anchor !== 'middle' ? ' ' + anchor : ''), host);
  a.style.left = Math.round(x) + 'px'; a.style.top = Math.round(y) + 'px';
  a.appendChild(el); return a;
};
/* HTML host behind an SVG container (components draw in the SVG's user space = the host's px) */
D.hostOf = container => { let h = container; while (h && h.namespaceURI === SVGNS) h = h.parentNode; return h; };
/* sticker group: SVG <g> with the cut-out filter (cream outline + soft double shadow). size 'sm' = thinner outline */
D.sticker = (parent, attrs, size) => D.svg('g', Object.assign({ filter: 'url(#' + (size === 'sm' ? 'cut-sm' : 'cut') + ')' }, attrs || {}), parent);
/* taped paper sheet (HTML), e.g. a formula sheet inside a component. tapes: [[color, pos], ...] */
D.sheetEl = (parent, box, tapes) => {
  const s = D.div('sheet', parent); Object.assign(s.style, { left: box.x + 'px', top: box.y + 'px', width: box.w + 'px', height: box.h + 'px' });
  (tapes || T.sheet.tapes).forEach(([c, pos], k) => { const tp = D.div('tape tape-' + c, s); tp.style.left = (pos * 100) + '%'; tp.style.transform = 'rotate(' + (k % 2 ? 5 : -4) + 'deg)'; });
  return s;
};

/* =========================== WORLD: defs, bands, grain, sparkles =========================== */
function laneY(ref) {
  if (typeof ref === 'number') return ref;
  const m = /^([a-z]+)\.(y0|y1)([+-]\d+)?$/.exec(ref); if (!m) throw fail('E_READY', 'bad band top ' + ref);
  const z = LAYOUT[m[1]]; return z ? z[m[2]] + parseInt(m[3] || '0', 10) : null;
}
function buildDefs() {
  const svg = D.svg('svg', { id: 'diki-defs', width: 0, height: 0, 'aria-hidden': 'true' }, STAGE); svg.style.position = 'absolute';
  const defs = D.svg('defs', {}, svg), ST = T.sticker;
  const cut = (id, r) => {
    const f = D.svg('filter', { id, x: '-20%', y: '-20%', width: '140%', height: '150%', 'color-interpolation-filters': 'sRGB' }, defs);
    D.svg('feMorphology', { in: 'SourceGraphic', operator: 'dilate', radius: r, result: 'd' }, f);
    D.svg('feFlood', { 'flood-color': ST.outline_color }, f); D.svg('feComposite', { in2: 'd', operator: 'in', result: 'border' }, f);
    ST.shadow_svg.forEach((s, k) => {
      D.svg('feGaussianBlur', { in: 'd', stdDeviation: s.blur }, f); D.svg('feOffset', { dy: s.dy, result: 'o' + k }, f);
      D.svg('feFlood', { 'flood-color': s.color, 'flood-opacity': s.opacity }, f); D.svg('feComposite', { in2: 'o' + k, operator: 'in', result: 's' + k }, f);
    });
    const m = D.svg('feMerge', {}, f); ['s0', 's1', 'border', 'SourceGraphic'].forEach(n => D.svg('feMergeNode', { in: n }, m));
  };
  cut('cut', ST.outline); cut('cut-sm', Math.round(ST.outline * 0.65));
  const g = D.svg('filter', { id: 'grain', x: 0, y: 0, width: '100%', height: '100%' }, defs);
  D.svg('feTurbulence', { type: 'fractalNoise', baseFrequency: 0.7, numOctaves: 3, seed: 3 }, g);
  D.svg('feColorMatrix', { type: 'matrix', values: '0 0 0 0 0.42  0 0 0 0 0.33  0 0 0 0 0.22  0.5 0 0 0 -0.18' }, g);
  const w = D.svg('filter', { id: 'wash', x: '-10%', y: '-10%', width: '120%', height: '120%' }, defs);
  D.svg('feTurbulence', { type: 'fractalNoise', baseFrequency: 0.012, numOctaves: 3, seed: 5, result: 'n' }, w);
  D.svg('feDisplacementMap', { in: 'SourceGraphic', in2: 'n', scale: 38 }, w); D.svg('feGaussianBlur', { stdDeviation: 6 }, w);
  const rg = D.svg('radialGradient', { id: 'vig', cx: '50%', cy: '48%', r: '75%' }, defs);
  D.svg('stop', { offset: '62%', 'stop-color': T.color.hue.soil_dark, 'stop-opacity': 0 }, rg);
  D.svg('stop', { offset: '100%', 'stop-color': T.color.hue.soil_dark, 'stop-opacity': T.world.vignette_alpha }, rg);
}
/* torn-paper strip whose ragged top edge sits at y: body, a darker 3 px shadow and a cream fibre edge (seeded once) */
function torn(g, y, fill, seed, k) {
  const amp = 9, step = 24, pts = [];
  for (let x = -40, i = 0; x <= 1120; x += step, i++) pts.push([x, y + (rng(seed, i) - 0.5) * 2 * amp]);
  const edge = off => pts.map(([x, v], i) => 'L' + x + ' ' + (v + off(i)).toFixed(1)).join(' ');
  const body = `M-40 1960 ${edge(() => 0)} L1120 1960 Z`;
  D.svg('path', { d: `M-40 1960 ${edge(i => -7 - rng(seed, i + 900) * 3)} L1120 1960 Z`, fill: T.sticker.outline_color }, g);
  D.svg('path', { d: body, fill: '#000', opacity: 0.1, transform: 'translate(0 -3)' }, g);
  const p = D.svg('path', { d: body, fill, 'data-band': k }, g);
  const cp = D.svg('clipPath', { id: 'band-clip-' + k }, g); D.svg('path', { d: body }, cp);
  return p;
}
function texture(g, kind, y0, seed, k) {
  const t = D.svg('g', { 'clip-path': 'url(#band-clip-' + k + ')' }, g);
  if (kind === 'speckle') for (let i = 0; i < 140; i++) D.svg('circle', { cx: (rng(seed, i) * 1080).toFixed(0), cy: (y0 + rng(seed, i + 300) * (1920 - y0)).toFixed(0), r: (1.5 + rng(seed, i + 600) * 2.5).toFixed(1), fill: T.color.ink, opacity: 0.18 }, t);
  if (kind === 'grain' || kind === 'grain_light') {
    const col = kind === 'grain' ? T.color.hue.soil_dark : T.color.hue.soil, op = kind === 'grain' ? 0.17 : 0.3;
    for (let y = y0 + 30, i = 0; y < 1940; y += 34 + rng(seed, i) * 22, i++) {
      let d = 'M-20 ' + y.toFixed(0); for (let x = 0; x <= 1100; x += 110) d += ' Q' + (x + 55) + ' ' + (y + (rng(seed, i * 20 + x) - 0.5) * 14).toFixed(1) + ' ' + (x + 110) + ' ' + y.toFixed(0);
      D.svg('path', { d, fill: 'none', stroke: col, 'stroke-width': 2 + rng(seed, i + 77) * 2, opacity: op, 'stroke-linecap': 'round' }, t);
    }
    for (let i = 0; i < 6; i++) D.svg('ellipse', { cx: (rng(seed, i + 40) * 1080).toFixed(0), cy: (y0 + 60 + rng(seed, i + 50) * (1900 - y0)).toFixed(0), rx: 22 + rng(seed, i + 60) * 18, ry: 7, fill: 'none', stroke: col, 'stroke-width': 3, opacity: op }, t);
  }
  if (kind === 'blueprint') {                              // light blueprint: cream rules on sky-blue grid paper
    for (let x = 0; x <= 1080; x += 48) D.svg('line', { x1: x, y1: y0 - 20, x2: x, y2: 1920, stroke: T.color.hue.paper, 'stroke-width': x % 192 ? 2 : 4, opacity: 0.55 }, t);
    for (let y = y0 + 24; y <= 1920; y += 48) D.svg('line', { x1: 0, y1: y, x2: 1080, y2: y, stroke: T.color.hue.paper, 'stroke-width': (y - y0 - 24) % 192 ? 2 : 4, opacity: 0.55 }, t);
  }
  if (kind === 'rules') for (let x = 0; x <= 1080; x += 40) { D.svg('line', { x1: x, y1: y0 - 20, x2: x, y2: 1920, stroke: T.color.hue.royal, 'stroke-width': 2, opacity: 0.16 }, t); }
  if (kind === 'rules') for (let y = y0; y <= 1920; y += 40) { D.svg('line', { x1: 0, y1: y, x2: 1080, y2: y, stroke: T.color.hue.royal, 'stroke-width': 2, opacity: 0.16 }, t); }
}
function sparkle(g, x, y, s, col) {
  D.svg('path', { d: `M${x - s} ${y} L${x + s} ${y} M${x} ${y - s} L${x} ${y + s} M${x - s * 0.55} ${y - s * 0.55} L${x + s * 0.55} ${y + s * 0.55} M${x - s * 0.55} ${y + s * 0.55} L${x + s * 0.55} ${y - s * 0.55}`, stroke: col || T.color.ink, 'stroke-width': 4, 'stroke-linecap': 'round', opacity: 0.55 }, g);
}
function buildWorld() {
  const Wt = T.world, S = Wt.subjects[D.subject];
  let svg = document.getElementById('world');
  if (!svg) { svg = D.svg('svg', { id: 'world' }, null); STAGE.insertBefore(svg, STAGE.firstChild); }
  ['width', 'height'].forEach((k, i) => svg.setAttribute(k, [1080, 1920][i])); svg.setAttribute('viewBox', '0 0 1080 1920'); svg.setAttribute('aria-hidden', 'true');
  svg.setAttribute('data-world', D.subject);
  D.svg('rect', { width: 1080, height: 1920, fill: T.color.hue.cream }, svg);
  const sky = D.svg('g', { filter: 'url(#wash)', opacity: 0.9, 'data-sky': '1' }, svg);
  Wt.sky_wash.forEach(e => D.svg('ellipse', { cx: e.cx, cy: e.cy, rx: e.rx, ry: e.ry, fill: e.fill, opacity: e.opacity }, sky));
  D.world = { bands: [] };
  S.bands.forEach((b, k) => {
    const y = laneY(b.top); if (y == null) return;
    const g = D.svg('g', { 'data-band-name': b.name }, svg);
    torn(g, y, b.fill, b.seed, k);
    if (b.texture) texture(g, b.texture, y, b.seed + 100, k);
    D.world.bands.push({ name: b.name, y: Math.round(y), fill: b.fill });
  });
  D.svg('rect', { width: 1080, height: 1920, filter: 'url(#grain)', opacity: Wt.grain_opacity }, svg);
  D.svg('rect', { width: 1080, height: 1920, fill: 'url(#vig)' }, svg);
  const under = y => { let f = T.color.hue.cream; for (const b of D.world.bands) if (b.y <= y) f = b.fill; return f; };
  const dark = h => { const c = [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] < 90; };
  Wt.sparkles.forEach(([x, y, s]) => sparkle(svg, x, y, s, dark(under(y)) ? T.color.hue.paper : T.color.ink));   // cream sparkles on dark bands
}
/* paper backdrops of the result and card lanes (a layer under the halos, so Emphasize shows on a sheet) */
const backdrops = {};
function buildSheets() {
  let host = document.getElementById('sheets'); if (!host) { host = D.div('', STAGE); host.id = 'sheets'; }
  ['result', 'card'].forEach(name => {
    const z = LAYOUT[name]; if (!z) return;
    const s = D.sheetEl(host, { x: T.lanes.x0, y: z.y0, w: T.lanes.x1 - T.lanes.x0, h: z.y1 - z.y0 }, name === 'card' ? [['teal', 0.12], ['mustard', 0.88]] : T.sheet.tapes);
    s.id = 'sheet-' + name; backdrops[name] = s;
  });
}
D.backdrop = name => backdrops[name] || null;

/* =========================== CHROME: lanes, ident, headlines, think plate, end card =========================== */
function placeLanes() {
  const x0 = T.lanes.x0, w = T.lanes.x1 - T.lanes.x0;
  ['title', 'diagram', 'result', 'caption', 'card'].forEach(name => {
    const el = document.getElementById('lane-' + name); if (!el) return;
    const z = LAYOUT[name];
    if (!z) { el.style.display = 'none'; return; }
    el.style.left = x0 + 'px'; el.style.width = w + 'px'; el.style.top = z.y0 + 'px'; el.style.height = (z.y1 - z.y0) + 'px';
  });
  const id = document.getElementById('ident'), iz = T.lanes.ident;
  if (id) { id.style.left = x0 + 'px'; id.style.width = w + 'px'; id.style.top = iz.y0 + 'px'; id.style.height = (iz.y1 - iz.y0) + 'px'; }
  D.lane = name => { const z = LAYOUT[name]; return z ? { x: x0, y: z.y0, w, h: z.y1 - z.y0, el: document.getElementById('lane-' + name) } : null; };
}

const norm = w => String(w).normalize('NFC').toLowerCase().replace(/[^\p{L}\p{M}\p{N}'’]/gu, '');
const isOutro = b => T.brand.endcard_slots.includes(b.slot);

D.buildChrome = function () {
  const titleLane = document.getElementById('lane-title'), B = T.brand;

  // 0. opening ident (PD-21): the brand sticker over the complete board from frame 0, gone by out_end_s
  const ident = document.getElementById('ident');
  if (ident) {
    if (ident.textContent.trim() !== B.wordmark) report('E_BRAND', 'error', 'ident text "' + ident.textContent.trim() + '" != tokens.brand.wordmark');
    ident.textContent = '';
    const st = D.brandSticker(ident, B.wordmark, { size: T.type.ident.size, rot: B.ident.rot_deg });
    D.Pop(st, 0, { until: B.ident.hold_until_s, dur: B.ident.out_dur_s });
    D.identEl = ident;
  }

  // 1. headlines as ransom chips, one per beat with a headline; the whole phrase pops together at its first
  //    headline word as spoken in that beat (the first beat's headline is up at t = 0: frame 0 carries the question)
  const heads = [];
  BEATS.forEach((b, bi) => {
    if (!b.headline || isOutro(b)) return;
    const el = D.chipRow(titleLane, b.headline, { lang: SHEET.language });
    const nWords = b.headline.split(/\s+/).filter(x => norm(x)).length;
    if (nWords > T.type.headline.max_words) report('W_HEADLINE_LONG', 'warning', b.id + ' headline has ' + nWords + ' words > ' + T.type.headline.max_words);
    let at = null;
    if (bi === 0) at = 0;
    else {
      const want = new Set(b.headline.split(/\s+/).map(norm).filter(Boolean));
      const [s, e] = b.word_range || [0, 0];
      for (let i = s; i < e; i++) if (want.has(norm(SHEET.words[i].w))) { at = Math.max(0, SHEET.words[i].t0 - LEAD); break; }
      if (at == null) { at = Math.max(0, b.start - LEAD); report('W_HEADLINE_UNMATCHED', 'warning', b.id + ' headline words not found in its spoken words; shown at beat start'); }
    }
    heads.push({ el, at, id: b.id });
    D.Chips(el, at);
    if (el.scrollHeight > titleLane.clientHeight + 1 || el.scrollWidth > titleLane.clientWidth + 1) report('W_HEADLINE_OVERFLOW', 'warning', b.id + ' headline does not fit the title lane at ' + T.type.headline.size + ' px');
  });
  heads.sort((a, b) => a.at - b.at);

  // 2. think plate: a taped paper sheet with the prompt (display.ui.think_prompt)
  const plate = document.getElementById('think-plate');
  if (plate) { plate.classList.add('sheet', 'plate'); const tp = D.div('tape tape-mustard', plate); tp.style.left = '50%'; tp.style.transform = 'rotate(-4deg)'; }

  // 3. end card = the final STATE of this scene: wordmark chips (display.ui.endcard_line1 == brand) in the title lane
  //    and the "Free lesson: <topic>" chip (display.ui.endcard_line2) on the result sheet. It triggers on the LAST
  //    outro.brand (v2) or outro.disclosure (v1) beat; that beat's text is never shown (PD-20).
  const outro = BEATS.filter(isOutro).pop();
  D.endCardAt = outro ? Math.max(0, outro.start - LEAD) : null;
  const wm = document.getElementById('wordmark'), endWrap = document.getElementById('endline-wrap');
  if (wm) {
    const line1 = String(D.fx(wm.dataset.fx || 'display.ui.endcard_line1'));
    if (line1 !== B.wordmark) report('E_BRAND', 'error', 'end-card line 1 "' + line1 + '" != brand "' + B.wordmark + '"');
    wm.textContent = ''; const st = D.brandSticker(wm, line1, { size: T.type.wordmark.size, twoLine: true, rot: -1.5 });
    if (D.endCardAt != null) D.Pop(st, D.endCardAt);
  }
  const endline = document.getElementById('endline');
  if (endline) {
    D.bindFx(endline.parentNode);
    if (!/^Free lesson: .+/.test(endline.textContent)) report('W_ENDLINE', 'warning', 'end-card line 2 should read "Free lesson: <topic>", got "' + endline.textContent + '"');
    endline.classList.add('chip', 'chip-black'); endline.dataset.rot = '-1.5';
    if (D.endCardAt != null) D.Pop(endline, D.endCardAt + MV.Pop.dur * 0.5); else endline.style.opacity = 0;
  }
  if (!outro) report('W_NO_END_CARD', 'warning', 'no outro.brand / outro.disclosure beat: no end card');
  if (D.endCardAt != null && window.DURATION - D.endCardAt < T.motion.end_card_min_s - EPS) report('W_END_CARD_SHORT', 'warning', 'end card ' + (window.DURATION - D.endCardAt).toFixed(2) + ' s < ' + T.motion.end_card_min_s + ' s');

  // 4. title-lane owner at time t: end card > think plate > latest headline
  const ownerAt = t => {
    if (D.endCardAt != null && t >= D.endCardAt - EPS) return wm;
    for (const w of THINK) if (t >= w.start - EPS && t < w.end - EPS) return plate;
    let h = null; for (const x of heads) if (x.at <= t + EPS) h = x.el;
    return h;
  };
  const times = [0].concat(heads.map(h => h.at), THINK.flatMap(w => [w.start, w.end]), D.endCardAt == null ? [] : [D.endCardAt]).sort((a, b) => a - b);
  const segs = [];
  times.forEach(tt => { const o = ownerAt(tt); if (!segs.length || segs[segs.length - 1].el !== o) segs.push({ el: o, t0: tt }); });
  const owned = [...new Set(heads.map(h => h.el).concat([plate, wm]).filter(Boolean))];
  const dur = MV.Headline.dur;
  const resultMain = document.getElementById('result-main');
  D.track(t => {
    for (const el of owned) {
      let o = 0;
      segs.forEach((s, i) => {
        if (s.el !== el) return;
        const next = segs[i + 1];
        const pin = s.t0 <= EPS ? 1 : D.prog(t, s.t0, dur, 'out');
        o = Math.max(o, pin - (next ? D.prog(t, next.t0, dur, 'out') : 0));
      });
      el.style.opacity = s0(o);
    }
    const e = D.endCardAt == null ? 0 : D.prog(t, D.endCardAt, dur, 'out');
    if (resultMain) resultMain.style.opacity = s0(1 - e);                    // the result gives way to the free-lesson chip
  });
  D.headlines = heads;
};

/* hero registration for the fill check */
const heroes = [];
D.hero = el => { heroes.push(el); return el; };

/* =========================== READY-TIME QA =========================== */
D.finalize = function () {
  const lane = D.lane('diagram'), qa = { layout: D.layoutName, subject: D.subject, diagram_share: +(lane.h / T.canvas.height).toFixed(3) };
  const shareMin = T.fill['diagram_min_share' + ({ captioned: '_captioned', carded: '_carded' }[D.layoutName] || '')];
  if (qa.diagram_share + 1e-9 < shareMin) report('W_DIAGRAM_SHARE', 'warning', 'diagram lane ' + qa.diagram_share + ' of frame < ' + shareMin);
  if (!heroes.length) report('W_NO_HERO', 'warning', 'no persistent hero object registered (Diki.hero)');
  qa.hero_fill = heroes.map(h => { const b = D.box(h); return { id: h.id, fill: +(b.h / lane.h).toFixed(3), top: Math.round(b.y), bottom: Math.round(b.y + b.h) }; });
  qa.hero_fill.forEach(f => { if (f.fill < T.fill.hero_min_of_diagram) report('W_FILL_LOW', 'warning', 'hero ' + f.id + ' fills ' + f.fill + ' of the diagram lane < ' + T.fill.hero_min_of_diagram); });
  qa.motion_in_think = [];
  THINK.forEach(w => intervals.forEach(iv => { if (!iv.still && iv.t0 < w.end - EPS && iv.t1 > w.start + EPS) qa.motion_in_think.push(iv.verb + '@' + iv.t0.toFixed(2)); }));
  if (qa.motion_in_think.length) report('W_MOTION_IN_THINK', 'warning', 'motion during a think window: ' + qa.motion_in_think.join(', '));
  qa.world = { subject: D.subject, bands: (D.world && D.world.bands) || [] };
  if (!document.getElementById('world') || !qa.world.bands.length) report('W_WORLD_MISSING', 'warning', 'no world layer (#world with torn-paper bands)');
  qa.ident = D.identEl ? D.identEl.textContent.trim() : null;
  if (qa.ident !== T.brand.wordmark) report('W_IDENT_MISSING', 'warning', 'opening ident missing or not the brand');
  qa.verbs = intervals.map(iv => iv.verb + '@' + iv.t0.toFixed(2) + '+' + (iv.t1 - iv.t0).toFixed(2));
  qa.end_card_s = D.endCardAt == null ? 0 : +(window.DURATION - D.endCardAt).toFixed(2);
  window.__diki_qa = qa;
};

/* =========================== RENDER =========================== */
D.render = t => { for (const fn of tracks[0]) fn(t); for (const fn of tracks[1]) fn(t); };
})();
