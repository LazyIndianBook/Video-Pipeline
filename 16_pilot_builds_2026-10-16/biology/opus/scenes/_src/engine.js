(function () {
'use strict';
/* ExamLeaf paper-collage scene engine (seek contract 1.0.0). Structure follows 04_harness_contract/scene_template.html:
   [5] config, [6] error channel, [7] seeded PRNG, [8] easing, [9] loaders, [10] state, [11] render, [12] ready + seek.
   Inlined verbatim into every scene by build_scenes.py; the per-scene part is #scene-config plus the markup. */
const Q = new URLSearchParams(location.search);
const num = (k, d) => { const v = parseFloat(Q.get(k)); return isFinite(v) ? v : d; };
const FPS = num('fps', 30), SEED = num('seed', 20261016), EPS = 1e-6;
const W = 1080, H = 1920;
const LEAD = 0.05;                                    // reveal on, or 0.05 s before, its word [V4-MP]
const HOLD_MIN = 1.2;                                 // tokens hold_times_s.headline_min [N60]
const INSETS = { top: 250, bottom: 450, left: 60, right: 120 };   // tokens platform_insets_px.generic_conservative (PLACEHOLDER)
const SHARES = [0.22, 0.54, 0.24];                    // tokens zones.*.share (owner: vertical_safe_zones.tokens.json)
const SIDE_MIN = 96;                                  // tokens zones.side_margin_min_px
const LEFT = Math.max(INSETS.left, SIDE_MIN), RIGHT = Math.max(INSETS.right, SIDE_MIN);
const MIN_PX = { tile: 59, label: 50, eq: 63 };      // tokens typography_px_at_1080.minimums_px
const BOIL_FPS = 8;                                   // brief: boil at 8 fps, decorative only (style guide §8.4 says 10; brief wins here)
const VIS_W = 864, VIS_H = 659;                       // art box authored at the placeholder middle_visual zone size
const FONT_SPECS = [
  { family: 'Noto Sans', weight: 700, text: 'Aa 0123 CO₂ H₂O C₆H₁₂O₆ →' },
  { family: 'Noto Sans', weight: 600, text: 'sunlight chlorophyll %' }];
const SCENE = JSON.parse(document.getElementById('scene-config').textContent);

/* [6] ERROR CHANNEL */
window.__errors = [];
const report = (code, severity, message, t) => window.__errors.push({ code, severity, message, t: t == null ? null : t });
const fail = (code, message, t) => { report(code, 'error', message, t); const e = new Error(code + ': ' + message); e.code = code; return e; };

/* [7] SEEDED RANDOMNESS: stateless only inside render (rngAt keyed by scene:element and step). */
function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const rngAt = (seed, i) => mulberry32((seed ^ Math.imul(i + 1, 0x9E3779B1)) >>> 0)();
function fnv1a(s) { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); } return h >>> 0; }
const KEY = s => (fnv1a(SCENE.id + ':' + s) ^ SEED) >>> 0;

/* [8] EASING (pure) */
const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x, lerp = (a, b, u) => a + (b - a) * u;
const ease = {
  cubicOut: u => 1 - Math.pow(1 - u, 3),
  sineInOut: u => 0.5 - 0.5 * Math.cos(Math.PI * u),
  backOut: u => { const s = 2.2, c = s + 1, v = u - 1; return 1 + c * v * v * v + s * v * v; }   // back.out(2.2): collage pop
};
// Finite damped pulse for 'emphasis' cues: n periods then stop (edge case 18).
const pulse = (t, at, n = 2, period = 0.5, amp = 0.07) => { const d = t - at; return d < 0 || d > n * period ? 1 : 1 + amp * Math.sin(2 * Math.PI * d / period) * (1 - d / (n * period)); };

/* [9] LOADERS: injected window.__CUE_SHEET__ / __FIXTURE__, then ?cues= / ?fixture=, then inline (template precedence). */
const deepFreeze = o => { Object.values(o).forEach(v => { if (v && typeof v === 'object') deepFreeze(v); }); return Object.freeze(o); };
async function loadJson(inject, param, inlineId, what) {
  if (inject) return { data: inject, source: 'injected' };
  const path = Q.get(param);
  if (path) {
    try { const r = await fetch(path); if (!r.ok) throw new Error('HTTP ' + r.status); return { data: await r.json(), source: 'path' }; }
    catch (e) {
      if (Q.get('strict') === '1') throw fail('E_' + what + '_LOAD', 'cannot load ' + path + ': ' + e.message);
      report('W_' + what + '_FALLBACK', 'warning', 'cannot load ' + path + ' (' + e.message + '); inline fallback used. Not valid for production.');
      return { data: JSON.parse(document.getElementById(inlineId).textContent), source: 'inline-fallback' };
    }
  }
  return { data: JSON.parse(document.getElementById(inlineId).textContent), source: 'inline' };
}
function checkSheet(s) {
  if (!s || !(s.duration > 0) || !isFinite(s.duration) || !Array.isArray(s.words) || !Array.isArray(s.cues)) throw fail('E_CUES_INVALID', 'cue sheet needs finite duration>0, words[], cues[]');
  s.words.forEach((w, i) => { if (i && w.t0 < s.words[i - 1].t0) throw fail('E_CUES_INVALID', 'words[' + i + '] not monotonic'); });
}

/* [10] STATE built once in ready(); render(t) only reads it. */
let SHEET, FX, ZONES = [], visScale = 1, freezeAt = Infinity;
const heads = [], recs = new Map(), boils = [];
const fx = path => { const v = path.split('.').reduce((o, k) => o == null ? o : o[k], FX); if (v === undefined) throw fail('E_FIXTURE_MISSING', 'fixture has no ' + path); return v; };
const norm = w => String(w).normalize('NFC').toLowerCase().replace(/[^\p{L}\p{M}\p{N}'’]/gu, '');
const surface = w => String(w).replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}'’]+$/gu, '');      // strip edge punctuation an aligner may keep
const findWord = (target, from) => { for (let i = from; i < SHEET.words.length; i++) if (norm(SHEET.words[i].w) === target) return i; return -1; };
const TILE_STYLES = [                                 // style guide §5.1 tile pairs; display pairs need >= 72 px glyphs
  { bg: '#2b2622', fg: '#f3ecdf', ff: 'var(--font)' },
  { bg: '#e0a73a', fg: '#2b2622', ff: 'Georgia, serif' },
  { bg: '#f3ecdf', fg: '#2b2622', ff: '"Courier New", monospace', grid: true },
  { bg: '#d9483b', fg: '#fbf7ee', ff: 'var(--font)' },
  { bg: '#2f7f7a', fg: '#fbf7ee', ff: 'Georgia, serif' },
  { bg: '#fbf7ee', fg: '#2f4fa8', ff: 'var(--font)', grid: true }];

function buildZones() {
  const y0 = INSETS.top, band = H - INSETS.top - INSETS.bottom; let y = y0;
  ZONES = SHARES.map(s => { const z = { y0: Math.round(y), y1: Math.round(y + s * band) }; y += s * band; return z; });
  const names = ['top_title', 'middle_visual', 'bottom_caption'], stage = document.getElementById('stage');
  ZONES.forEach((z, i) => { const d = document.createElement('div'); d.className = 'zone'; d.style.top = z.y0 + 'px'; d.style.height = (z.y1 - z.y0) + 'px'; d.style.left = LEFT + 'px'; d.style.width = (W - LEFT - RIGHT) + 'px'; d.textContent = names[i] + '  PLACEHOLDER insets'; stage.appendChild(d); });
  document.querySelectorAll('.box').forEach(b => { const z = ZONES[+b.dataset.zone]; b.style.top = z.y0 + 'px'; b.style.height = (z.y1 - z.y0) + 'px'; b.style.left = LEFT + 'px'; b.style.width = (W - LEFT - RIGHT) + 'px'; });
  const z = ZONES[1], zw = W - LEFT - RIGHT, zh = z.y1 - z.y0, vis = document.getElementById('vis');
  visScale = Math.min(zw / VIS_W, zh / VIS_H);
  if (Math.abs(visScale - 1) > 0.01) report('W_VIS_SCALED', 'warning', 'middle_visual is ' + zw + 'x' + zh + '; art scaled by ' + visScale.toFixed(3) + ' (text sizes scale too: re-check minimums)');
  vis.style.left = ((zw - VIS_W * visScale) / 2) + 'px'; vis.style.top = ((zh - VIS_H * visScale) / 2) + 'px';
}

function buildGeom() {                                  // data-bound geometry (not decoration): drawn from fixture values only
  document.querySelectorAll('[data-geom="pie"]').forEach(p => {
    const f = fx(p.dataset.fxGeom), cx = +p.dataset.cx, cy = +p.dataset.cy, r = +p.dataset.r;
    if (!(f > 0 && f < 1)) throw fail('E_FIXTURE_RANGE', p.dataset.fxGeom + ' must be in (0,1), got ' + f);
    const a0 = -Math.PI / 2, a1 = a0 + f * 2 * Math.PI, P = a => (cx + r * Math.cos(a)).toFixed(2) + ' ' + (cy + r * Math.sin(a)).toFixed(2);
    p.setAttribute('d', 'M' + cx + ' ' + cy + ' L' + P(a0) + ' A' + r + ' ' + r + ' 0 ' + (f > 0.5 ? 1 : 0) + ' 1 ' + P(a1) + ' Z');
    const anchor = p.dataset.anchor && document.getElementById(p.dataset.anchor);
    if (anchor) {                                       // centre the value tag on the wedge's mid-angle (placement follows the data)
      const am = a0 + f * Math.PI, k = +p.dataset.anchorK || 0.62;
      anchor.style.left = Math.round(cx + k * r * Math.cos(am) - anchor.offsetWidth / 2) + 'px'; anchor.style.top = Math.round(cy + k * r * Math.sin(am) - anchor.offsetHeight / 2) + 'px';   // whole pixels: subpixel offsets made frames depend on seek history
    }
  });
}

function buildHeadlines() {                             // headline = in-order subsequence of this scene's spoken words (script on_screen.headline)
  const box = document.getElementById('title'); box.lang = SHEET.language; let cursor = 0, ti = 0;
  (SCENE.headlines || []).forEach(h => {
    const g = { el: document.createElement('div'), tiles: [], start: Infinity, end: Infinity };
    g.el.className = 'hl'; box.appendChild(g.el);
    h.words.forEach((word, wi) => {
      const idx = findWord(norm(word), cursor);
      if (idx < 0) { report('W_HEADLINE_WORD_MISSING', 'warning', 'headline word "' + word + '" not found in cue sheet words after index ' + cursor); return; }
      cursor = idx + 1;
      const w = SHEET.words[idx], st = TILE_STYLES[(ti * 5 + 1) % TILE_STYLES.length], sp = document.createElement('span');
      sp.className = 'tile' + (st.grid ? ' grid' : ''); sp.textContent = surface(w.w) + (h.q && wi === h.words.length - 1 ? '?' : '');
      if (w.lang) sp.lang = w.lang;
      sp.style.backgroundColor = st.bg; sp.style.color = st.fg; sp.style.fontFamily = st.ff;
      g.el.appendChild(sp);
      g.tiles.push({ el: sp, at: Math.max(0, w.t0 - LEAD), rot: (rngAt(KEY('tile'), ti) - 0.5) * 12, dy: (rngAt(KEY('tile'), ti + 500) - 0.5) * 10 });
      ti++;
    });
    if (g.tiles.length) g.start = g.tiles[0].at;
    heads.push(g);
  });
  heads.forEach((g, k) => {
    g.end = k + 1 < heads.length ? heads[k + 1].start : Infinity;
    if (!g.tiles.length) return;
    const hold = Math.min(g.end, window.DURATION) - g.tiles[g.tiles.length - 1].at;
    if (hold < HOLD_MIN) report('W_HOLD_SHORT', 'warning', 'headline ' + k + ' hold ' + hold.toFixed(2) + ' s < ' + HOLD_MIN + ' s [N60]');
  });
}

const recOf = el => { if (!recs.has(el)) recs.set(el, { el, anim: el.dataset.anim || 'pop', reveal: null, hold: null, pulses: [], rot0: el.dataset.rot != null ? +el.dataset.rot : (rngAt(KEY(el.id), 7) - 0.5) * 24, draws: Array.from(el.querySelectorAll('.ink')) }); return recs.get(el); };
function buildCues() {                                  // cues drive elements by element_id; times are never hard-coded here
  SHEET.cues.forEach(c => {
    if (!c.element_id) return;
    const el = document.getElementById(c.element_id);
    if (!el) { report('W_CUE_NO_ELEMENT', 'warning', 'cue ' + c.id + ' targets missing element ' + c.element_id); return; }
    const r = recOf(el);
    if (c.kind === 'reveal') r.reveal = r.reveal == null ? c.at : Math.min(r.reveal, c.at);
    else if (c.kind === 'hold') r.hold = { at: c.at, until: isFinite(c.until) ? c.until : window.DURATION };
    else if (c.kind === 'emphasis') r.pulses.push(c.at);
  });
  document.querySelectorAll('[data-follow]').forEach(el => {   // a container that appears with its first cued child (no own cue)
    const lead = document.getElementById(el.dataset.follow), lr = lead && recs.get(lead), r = recOf(el);
    if (lr && lr.reveal != null) r.reveal = lr.reveal; else report('W_FOLLOW_NO_CUE', 'warning', el.id + ' follows ' + el.dataset.follow + ', which has no reveal cue');
  });
  document.querySelectorAll('[data-reveal]').forEach(el => { const r = recOf(el); if (r.reveal == null && !r.hold) report('W_ELEMENT_NO_CUE', 'warning', 'element ' + el.id + ' has no reveal/hold cue in this sheet; it stays hidden'); });
  recs.forEach(r => r.draws.forEach(p => { p.setAttribute('pathLength', '1'); p.style.strokeDasharray = '1 1'; }));
  if (SCENE.freezeOn) { const el = document.getElementById(SCENE.freezeOn), r = el && recs.get(el); if (r && r.hold) freezeAt = r.hold.at; else report('W_THINK_UNMARKED', 'warning', 'think-window element ' + SCENE.freezeOn + ' has no hold cue; boil is not frozen'); }
}

function buildApprovedText() {                          // text shown verbatim from the approved script, verified against the spoken words
  (SCENE.approvedText || []).forEach(a => {
    const el = document.getElementById(a.element_id); if (!el) { report('W_TEXT_NO_ELEMENT', 'warning', 'no element ' + a.element_id); return; }
    let cur = 0; const missing = a.words.filter(w => { const i = findWord(norm(w), cur); if (i < 0) return true; cur = i + 1; return false; });
    if (missing.length) report('E_TEXT_NOT_SPOKEN', 'error', a.element_id + ': words not in the cue sheet: ' + missing.join(', '));
    if (a.breakAfter && a.text.includes(a.breakAfter)) {   // line break for layout only; textContent stays the approved string
      const i = a.text.indexOf(a.breakAfter) + a.breakAfter.length; el.textContent = '';
      [a.text.slice(0, i + 1), a.text.slice(i + 1)].forEach(part => { const sp = document.createElement('span'); sp.style.display = 'block'; sp.textContent = part; el.appendChild(sp); });
    } else el.textContent = a.text;
  });
}

function buildBoil() { document.querySelectorAll('[data-boil]').forEach(el => boils.push({ el, key: KEY('boil:' + (el.dataset.boil || el.id)), amp: +(el.dataset.amp || 1) })); }

/* [11] RENDER: synchronous, pure function of t (plus immutable state). */
function stateOf(r, t) {
  let o = 1, s = 1, rot = 0, draw = 1;
  if (r.el.hasAttribute('data-reveal')) {
    const a = r.reveal != null ? r.reveal : r.hold ? r.hold.at : Infinity, d = t - a;
    if (d < -EPS) { o = 0; s = r.anim === 'pop' ? 0.001 : 0.9; draw = 0; }
    else if (r.anim === 'pop') { const u = clamp01(d / 0.4); o = clamp01(d / 0.08); s = Math.max(0.001, ease.backOut(u)); rot = (1 - ease.cubicOut(u)) * r.rot0; }
    else if (r.anim === 'draw') { draw = ease.cubicOut(clamp01(d / 0.6)); }
    else { o = ease.cubicOut(clamp01(d / 0.25)); }     // 'fade': 250 ms opacity-only (science tags: no scale, so raster never depends on seek history)
    if (r.hold && r.hold.until < window.DURATION - EPS) o *= 1 - clamp01((t - r.hold.until) / 0.3);
  }
  r.pulses.forEach(at => { s *= pulse(t, at); });
  return { o, s, rot, draw };
}
function render(t) {
  heads.forEach(g => {
    const out = g.end === Infinity ? 1 : clamp01((g.end - 0.05 - t) / 0.2);          // gone by the next headline's first word
    g.tiles.forEach(x => {
      const d = t - x.at, u = clamp01(d / 0.35);
      x.el.style.opacity = d < -EPS ? 0 : clamp01(d / 0.06) * out;
      x.el.style.transform = 'translateY(' + (x.dy + (1 - ease.cubicOut(u)) * -30).toFixed(2) + 'px) rotate(' + (x.rot + (1 - ease.cubicOut(u)) * 9).toFixed(2) + 'deg) scale(' + (d < 0 ? 1.25 : lerp(1.25, 1, ease.backOut(u))).toFixed(4) + ')';
    });
  });
  recs.forEach(r => {
    const st = stateOf(r, t);
    r.el.style.opacity = st.o;
    r.el.style.transform = 'rotate(' + st.rot.toFixed(2) + 'deg) scale(' + st.s.toFixed(4) + ')';
    r.draws.forEach(p => { p.style.strokeDashoffset = (1 - st.draw).toFixed(4); });
  });
  const k = Math.floor(Math.min(t, freezeAt) * BOIL_FPS + EPS);                      // boil step: stateless jitter, frozen in think windows
  boils.forEach(b => {
    const jx = (rngAt(b.key, k) - 0.5) * 3 * b.amp, jy = (rngAt(b.key, k + 100003) - 0.5) * 3 * b.amp, jr = (rngAt(b.key, k + 200003) - 0.5) * 1.4 * b.amp;
    b.el.style.transform = 'translate(' + jx.toFixed(2) + 'px,' + jy.toFixed(2) + 'px) rotate(' + jr.toFixed(2) + 'deg)';
  });
  const push = SCENE.pushIn ? 1 + SCENE.pushIn * ease.sineInOut(clamp01(t / window.DURATION)) : 1;   // hook only: no labels in that scene (#64)
  document.getElementById('vis').style.transform = 'scale(' + (visScale * push).toFixed(5) + ')';
}

/* Layout self-check: every visible text element inside its zone and the side margins, at or above the size floor,
   and no two text boxes overlapping. Runs on frames the scene computes itself; never changes state. */
function layoutCheck() {
  const sr = document.getElementById('stage').getBoundingClientRect(), times = [window.DURATION];
  heads.forEach(g => { if (isFinite(g.end)) times.push(Math.max(0, g.end - 0.3)); });
  times.forEach(t => {
    render(t);
    const effOp = el => { let o = 1; for (let e = el; e && e.id !== 'stage'; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
    const items = Array.from(document.querySelectorAll('.tile,.tag,[data-text-role]')).filter(el => effOp(el) > 0.02);
    const boxes = items.map(el => {
      const b = el.getBoundingClientRect(), zoneEl = el.closest('.box'), z = zoneEl ? ZONES[+zoneEl.dataset.zone] : null;
      const rect = { el, x0: b.left - sr.left, y0: b.top - sr.top, x1: b.right - sr.left, y1: b.bottom - sr.top };
      if (z && (rect.y0 < z.y0 - 1 || rect.y1 > z.y1 + 1 || rect.x0 < LEFT - 1 || rect.x1 > W - RIGHT + 1))
        report('W_TEXT_OUTSIDE_ZONE', 'warning', (el.id || el.textContent) + ' box ' + [rect.x0, rect.y0, rect.x1, rect.y1].map(Math.round).join(',') + ' leaves its zone', t);
      const role = el.classList.contains('tile') ? 'tile' : el.classList.contains('lbl') ? 'label' : el.closest('.eq') ? 'eq' : 'label';
      el.querySelectorAll('[data-fx]').forEach(f => { if (f.closest('.tile,.tag,[data-text-role]') !== el) return; const px = parseFloat(getComputedStyle(f).fontSize) * visScale; if (px < MIN_PX[role] - 0.5 && !f.closest('.sub-ok')) report('W_TEXT_TOO_SMALL', 'warning', f.dataset.fx + ' ' + px.toFixed(0) + ' px < ' + MIN_PX[role], t); });
      if (role === 'tile' && parseFloat(getComputedStyle(el).fontSize) < MIN_PX.tile) report('W_TEXT_TOO_SMALL', 'warning', 'headline tile ' + el.textContent, t);
      return rect;
    });
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      if (a.x0 < b.x1 - 2 && b.x0 < a.x1 - 2 && a.y0 < b.y1 - 2 && b.y0 < a.y1 - 2) report('W_TEXT_OVERLAP', 'warning', (a.el.id || a.el.textContent) + ' overlaps ' + (b.el.id || b.el.textContent), t);
    }
  });
  render(0);
}

/* [12] READY + SEEK (template). seek never waits on requestAnimationFrame [N69]. */
window.FPS = FPS;
window.DURATION = 4.0;                                  // synchronous default; final value is the cue sheet duration, set in ready()
window.SCENE_META = { contract: '1.0.0', videoCount: 0, notes: 'paper-collage-vertical; ' + SCENE.id };
window.ready = (async () => {
  const s = await loadJson(window.__CUE_SHEET__, 'cues', 'cue-sheet-inline', 'CUES'); SHEET = s.data; window.__cueSource = s.source; checkSheet(SHEET);
  const f = await loadJson(window.__FIXTURE__, 'fixture', 'fixture-inline', 'FIXTURE'); FX = deepFreeze(f.data); window.__fixtureSource = f.source;
  window.DURATION = SHEET.duration;
  window.FRAME_COUNT = Math.round(window.DURATION * FPS);
  if (SHEET.fps !== FPS) report('W_FPS_MISMATCH', 'warning', 'cue sheet fps ' + SHEET.fps + ' != render fps ' + FPS + '; times stay in seconds');
  await Promise.all(FONT_SPECS.map(f => document.fonts.load(f.weight + ' 40px "' + f.family + '"', f.text).catch(e => report('E_FONT_LOAD', 'error', f.family + ': ' + e.message))));
  document.querySelectorAll('[data-fx]').forEach(el => { el.textContent = String(fx(el.dataset.fx)); });   // read-only, unformatted
  buildZones(); buildApprovedText(); buildHeadlines(); buildCues(); buildBoil();
  await document.fonts.ready;
  buildGeom(); layoutCheck();
  if (Q.get('safe') === '1') document.getElementById('stage').classList.add('safe');
  addEventListener('keydown', e => { if (e.key === 's' || e.key === 'S') document.getElementById('stage').classList.toggle('safe'); });
})().catch(e => { if (!e.code) report('E_READY', 'error', e.message); throw e; });

let chain = Promise.resolve();
window.seek = async function seek(t) {
  const prev = chain; let done; chain = new Promise(r => { done = r; });
  try {
    await prev; await window.ready;
    if (typeof t !== 'number' || !isFinite(t)) throw fail('E_BAD_T', 'seek(t) needs a finite number of seconds, got ' + t);
    const tc = Math.min(Math.max(t, 0), window.DURATION);
    render(tc);
    await document.fonts.ready;
    await Promise.all(Array.from(document.images).map(i => i.decode().catch(e => report('E_ASSET_LOAD', 'error', i.src + ': ' + e.message, tc))));
    return { t: tc, frame: Math.round(tc * FPS) };
  } finally { done(); }
};
window.__hf = window.__hf || { get duration() { return window.DURATION; }, seek: t => window.seek(t) };
if (Q.get('preview') === '1') window.ready.then(() => { const r = document.createElement('input'); r.type = 'range'; r.id = 'scrub'; r.min = 0; r.max = window.DURATION; r.step = 1 / FPS; r.value = 0; r.oninput = () => window.seek(parseFloat(r.value)); document.body.appendChild(r); });
if (Q.has('t')) window.ready.then(() => window.seek(num('t', 0)));
})();
