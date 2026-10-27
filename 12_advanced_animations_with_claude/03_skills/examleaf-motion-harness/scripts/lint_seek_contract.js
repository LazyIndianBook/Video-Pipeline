#!/usr/bin/env node
'use strict';
/*
 * lint_seek_contract.js - static check of a scene file against the ExamLeaf seek contract
 * (contract.md). Node >= 18, no dependencies, offline.
 *
 * Usage:
 *   node lint_seek_contract.js [--level 0|1|2] [--hf] [--strict] FILE...   (.html or .js)
 *   node lint_seek_contract.js --selftest
 *
 * stdout: one JSON report. stderr: one human line per violation.
 * Exit codes (contract.md section 12): 0 no errors, 1 violations (or selftest failed), 2 usage/IO error.
 *
 * Severity: "error" fails the run; "warning" fails only with --strict.
 * Silence one finding by putting `lint-allow: RULEID[,RULEID]` in a comment on the same line.
 * ponytail: regex/heuristic scanner, not a JS parser. It misses dynamically built calls
 * (window['Math']['random']) and can flag string contents. The double-render hash test
 * (determinism_hash_check.py) is the real proof; this is the cheap early filter.
 */
const fs = require('fs');

const CONTRACT_VERSION = '1.0.0';

// ---- rule table. edge = research report section 8 row number; src = report citation.
const RULES = [
  { id: 'F01', sev: 'error', scope: 'js', re: /\bDate\s*\.\s*now\b/g, edge: 15, src: '[N68][N18]', msg: 'Date.now() reads the wall clock; scene state must be a pure function of t.' },
  { id: 'F02', sev: 'error', scope: 'js', re: /\bnew\s+Date\s*\(\s*\)|(?<![\w.$])Date\s*\(\s*\)/g, edge: 15, src: '[N68][N18]', msg: 'Date() with no argument reads the wall clock.' },
  { id: 'F03', sev: 'error', scope: 'js', re: /\bperformance\s*\.\s*now\b/g, edge: 15, src: '[N68][N18]', msg: 'performance.now() reads a real-time clock; use the t passed to seek(t).' },
  { id: 'F04', sev: 'error', scope: 'js', re: /\bMath\s*\.\s*random\b/g, edge: 17, src: '[N61]', msg: 'Math.random() is unseeded; use the seeded PRNG (mulberry32) created at load.' },
  { id: 'F05', sev: 'error', scope: 'js', re: /\bcrypto\s*\.\s*(?:getRandomValues|randomUUID)\b/g, edge: 17, src: '[N61]', msg: 'crypto random values are not reproducible; use the seeded PRNG.' },
  { id: 'F06', sev: 'error', scope: 'js', re: /\bsetInterval\s*\(/g, edge: 19, src: '[N69]', msg: 'setInterval drives state in real time; the renderer seeks, it never plays.' },
  { id: 'F07', sev: 'error', scope: 'js', re: /\b(?:requestAnimationFrame|cancelAnimationFrame)\b/g, edge: 19, src: '[N69]', msg: 'rAF does not fire in BeginFrame mode and hangs the render; poll with setTimeout and a deadline if you must wait.' },
  { id: 'F08', sev: 'error', scope: 'js', re: /\.\s*play\s*\(/g, edge: 15, src: '[N68]', msg: '.play() starts real-time playback; the renderer never calls play(). Seek instead (video.currentTime, timeline.time(t)).' },
  { id: 'F09', sev: 'error', scope: 'html', re: /\bautoplay\b/gi, edge: 15, src: '[N68]', msg: 'autoplay starts real-time playback.' },
  { id: 'F10', sev: 'error', scope: 'js', re: /\brepeat\s*:\s*(?:-1|Infinity)\b|\.\s*repeat\s*\(\s*(?:-1|Infinity)\s*\)|\biterations\s*:\s*Infinity\b/g, edge: 18, src: '[V4-MP]', msg: 'Infinite repeat; use a finite repeat count.' },
  { id: 'F10', sev: 'error', scope: 'css', re: /animation-iteration-count\s*:\s*infinite\b|(?<![\w-])animation\s*:[^;}]*\binfinite\b/gi, edge: 18, src: '[V4-MP]', msg: 'Infinite CSS animation; use a finite count.' },
  { id: 'F12', sev: 'error', scope: 'html', re: /\b(?:src|href)\s*=\s*["']?\s*(?:https?:)?\/\//gi, edge: null, src: 'contract section 5', msg: 'Remote resource. Scenes must render offline with no CDN.' },
  { id: 'F12', sev: 'error', scope: 'js', re: /\b(?:fetch|import|importScripts)\s*\(\s*["'`]\s*(?:https?:)?\/\/|\bfrom\s+["']\s*(?:https?:)?\/\//g, edge: null, src: 'contract section 5', msg: 'Remote resource. Scenes must render offline with no CDN.' },
  { id: 'F12', sev: 'error', scope: 'css', re: /url\(\s*["']?\s*(?:https?:)?\/\/|@import\s+(?:url\(\s*)?["']?\s*(?:https?:)?\/\//gi, edge: null, src: 'contract section 5', msg: 'Remote resource. Scenes must render offline with no CDN.' },
  { id: 'W01', sev: 'warning', scope: 'js', re: /\bsetTimeout\s*\(/g, edge: 19, src: '[N69]', msg: 'setTimeout: allowed only for deadline-bounded polling that never changes visual state. Add `lint-allow: W01` to confirm.' },
  { id: 'W02', sev: 'warning', scope: 'js', re: /\brequestIdleCallback\b/g, edge: 19, src: '[N69]', msg: 'requestIdleCallback is wall-clock scheduled; avoid.' },
  // W03 is a warning at --level 0 and becomes error F14 at --level 1+ (16 Oct 2026, pilot gap L-14).
  { id: 'W03', sev: 'warning', l1: 'F14', scope: 'css', re: /@keyframes\b|(?<![\w-])animation(?:-name|-duration)?\s*:|(?<![\w-])transition(?:-property|-duration)?\s*:/gi, edge: 15, src: '[Hypothesis]', msg: 'CSS animations/transitions run on the document timeline, not on seek(t), so frames depend on wall-clock time. Set every property from seek(t) instead (error F14 at level 1+).' },
  { id: 'W03', sev: 'warning', l1: 'F14', scope: 'html', re: /\bstyle\s*=\s*"[^"]*(?:animation|transition)\s*:/gi, edge: 15, src: '[Hypothesis]', msg: 'Inline CSS animation/transition is not seek-driven; frames depend on wall-clock time (error F14 at level 1+).' },
];

// ---- requirements by conformance level (contract.md section 13)
const REQUIRED = [
  { id: 'R01', key: 'DURATION', level: 0, sev: 'error', test: s => /window\s*\.\s*DURATION\s*=(?!=)|window\s*\[\s*["']DURATION["']\s*\]\s*=(?!=)|defineProperty\(\s*window\s*,\s*["']DURATION["']/.test(s), msg: 'window.DURATION is not set (seconds).' },
  { id: 'R02', key: 'seek', level: 0, sev: 'error', test: s => /window\s*\.\s*seek\s*=(?!=)|window\s*\[\s*["']seek["']\s*\]\s*=(?!=)|defineProperty\(\s*window\s*,\s*["']seek["']/.test(s), msg: 'window.seek(t) is not exported.' },
  { id: 'R03', key: 'seek_async', level: 0, sev: 'warning', test: s => /\basync\b[^;{]{0,80}\bseek\w*|\bseek\w*\s*=\s*async\b/.test(s), msg: 'Could not confirm that seek is async. It must return a Promise that resolves when frame t is fully painted.' },
  { id: 'R04', key: 'ready', level: 1, sev: 'error', test: s => /window\s*\.\s*ready\s*=(?!=)/.test(s), msg: 'window.ready (Promise) is not exported; cue sheet, fixture and fonts must be ready before the first seek.' },
  { id: 'R05', key: 'fonts', level: 1, sev: 'error', test: s => /document\s*\.\s*fonts\s*\.\s*(?:load|ready)\b/.test(s), msg: 'Fonts are not preloaded (document.fonts.load / ready) before the first seek. Edge case 55.' },
  { id: 'R06', key: 'cue_loader', level: 1, sev: 'warning', test: s => /URLSearchParams/.test(s) && /["']cues["']/.test(s), msg: 'No cue-sheet loader from a ?cues= path found.' },
  { id: 'R07', key: 'frozen_fixture', level: 1, sev: 'warning', test: s => /Object\s*\.\s*freeze/.test(s), msg: 'Fixture props are not frozen (Object.freeze). Fixtures are read-only.' },
  { id: 'R08', key: 'errors_channel', level: 1, sev: 'error', test: s => /__errors/.test(s), msg: 'window.__errors channel is missing; errors must be reported, never swallowed.' },
  { id: 'R09', key: 'scene_meta', level: 2, sev: 'error', test: s => /SCENE_META/.test(s) && /\bcontract\s*:/.test(s), msg: 'window.SCENE_META with a contract version is missing.' },
  { id: 'R10', key: 'hf_adapter', level: 99, sev: 'error', test: s => /__hf/.test(s), msg: 'window.__hf adapter missing (required by --hf). Shape is contested [N68]; verify.' },
];

// ---- source preparation -------------------------------------------------------------
const mask = s => s.replace(/[^\n\r]/g, ' ');

// Blank out JS comments (keeping newlines so line numbers survive). Strings are kept.
function stripJsComments(src) {
  let out = '', i = 0, state = 'code', prevSig = '';
  const n = src.length;
  while (i < n) {
    const c = src[i], d = src[i + 1];
    if (state === 'code') {
      if (c === '/' && d === '/') { state = 'line'; out += '  '; i += 2; continue; }
      if (c === '/' && d === '*') { state = 'block'; out += '  '; i += 2; continue; }
      if (c === '"' || c === "'" || c === '`') { state = c; out += c; i++; continue; }
      if (c === '/' && (prevSig === '' || '(,=:[!&|?{};+-*%<>~^'.includes(prevSig))) { // regex literal
        let j = i + 1, cls = false;
        while (j < n) {
          const e = src[j];
          if (e === '\\') { j += 2; continue; }
          if (e === '\n') break;
          if (e === '[') cls = true; else if (e === ']') cls = false; else if (e === '/' && !cls) break;
          j++;
        }
        out += src.slice(i, j + 1); i = j + 1; prevSig = ')'; continue;
      }
      out += c; if (!/\s/.test(c)) prevSig = c; i++; continue;
    }
    if (state === 'line') { if (c === '\n') { state = 'code'; out += c; } else out += (c === '\r' ? c : ' '); i++; continue; }
    if (state === 'block') { if (c === '*' && d === '/') { state = 'code'; out += '  '; i += 2; continue; } out += (c === '\n' || c === '\r') ? c : ' '; i++; continue; }
    if (c === '\\') { out += c + (d === undefined ? '' : d); i += 2; continue; }
    if (c === state) { state = 'code'; prevSig = ')'; } else if (c === '\n' && state !== '`') { state = 'code'; }
    out += c; i++;
  }
  return out;
}

// Split an HTML file into three same-length views: executable JS, CSS, and markup.
function splitHtml(src) {
  const segs = [];
  const re = /<!--[\s\S]*?-->|<script\b([^>]*)>([\s\S]*?)<\/script\s*>|<style\b[^>]*>([\s\S]*?)<\/style\s*>/gi;
  let m;
  while ((m = re.exec(src))) {
    const innerStart = m.index + m[0].indexOf('>') + 1;
    if (m[0].startsWith('<!--')) segs.push({ s: m.index, e: m.index + m[0].length, k: 'comment' });
    else if (/^<script/i.test(m[0])) {
      const t = /type\s*=\s*["']?([^"'\s>]+)/i.exec(m[1] || '');
      segs.push({ s: innerStart, e: innerStart + m[2].length, k: (!t || /javascript|ecmascript|module/i.test(t[1])) ? 'js' : 'data' });
    } else segs.push({ s: innerStart, e: innerStart + m[3].length, k: 'css' });
  }
  let js = '', css = '', html = '', pos = 0;
  const add = (txt, k) => { const x = mask(txt); js += k === 'js' ? txt : x; css += k === 'css' ? txt : x; html += k === 'html' ? txt : x; };
  for (const g of segs) { if (g.s > pos) add(src.slice(pos, g.s), 'html'); add(src.slice(g.s, g.e), g.k); pos = g.e; }
  if (pos < src.length) add(src.slice(pos), 'html');
  return { js: stripJsComments(js), css: css.replace(/\/\*[\s\S]*?\*\//g, mask), html };
}

function views(file, src) {
  if (/\.html?$/i.test(file)) return splitHtml(src);
  return { js: stripJsComments(src), css: '', html: '' };
}

// ---- the linter ---------------------------------------------------------------------
function lintSource(file, src, opts) {
  const v = views(file, src);
  const lines = src.split('\n');
  const starts = [0];
  for (let i = 0; i < src.length; i++) if (src[i] === '\n') starts.push(i + 1);
  const where = idx => { let lo = 0, hi = starts.length - 1; while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (starts[mid] <= idx) lo = mid; else hi = mid - 1; } return { line: lo + 1, col: idx - starts[lo] + 1 }; };
  const allowed = (line, id) => { const m = /lint-allow:\s*([A-Za-z0-9_, ]+)/.exec(lines[line - 1] || ''); return !!m && m[1].split(/[ ,]+/).includes(id); };
  const out = [];
  const push = (rule, idx, text) => {
    const w = where(idx);
    if (!allowed(w.line, rule.id)) out.push({ rule: rule.id, severity: rule.sev, line: w.line, col: w.col, match: String(text).slice(0, 60), message: rule.msg, edge_case: rule.edge === undefined ? null : rule.edge, source: rule.src || null });
  };

  for (const r0 of RULES) {
    const r = r0.l1 && opts.level >= 1 ? { ...r0, id: r0.l1, sev: 'error' } : r0;
    const text = v[r.scope];
    if (!text) continue;
    r.re.lastIndex = 0;
    let m;
    while ((m = r.re.exec(text))) { push(r, m.index, m[0]); if (m[0] === '') r.re.lastIndex++; }
  }

  // F11: setTimeout re-scheduling its own enclosing function (a hand-rolled animation loop).
  const reT = /\bsetTimeout\s*\(\s*([A-Za-z_$][\w$]*)\s*[,)]/g;
  let m;
  while ((m = reT.exec(v.js))) {
    const name = m[1];
    const def = new RegExp('function\\s+' + name + '\\b|(?:const|let|var)\\s+' + name + '\\s*=|\\b' + name + '\\s*=\\s*(?:async\\s*)?(?:function|\\([^)]*\\)\\s*=>|[\\w$]+\\s*=>)').exec(v.js);
    if (!def) continue;
    let i = v.js.indexOf('{', def.index), depth = 0, end = -1;
    for (let j = i; i >= 0 && j < v.js.length; j++) { if (v.js[j] === '{') depth++; else if (v.js[j] === '}' && --depth === 0) { end = j; break; } }
    if (i >= 0 && end > 0 && m.index > i && m.index < end) push({ id: 'F11', sev: 'error', edge: 19, src: '[N69]', msg: 'setTimeout re-schedules its own function: a real-time animation loop.' }, m.index, m[0]);
  }

  // F13: several <video> elements need a declared single worker.
  const vids = [];
  const reV = /<video\b/gi, reC = /createElement\(\s*["']video["']\s*\)/g;
  while ((m = reV.exec(v.html))) vids.push(m.index);
  while ((m = reC.exec(v.js))) vids.push(m.index);
  vids.sort((a, b) => a - b);
  if (vids.length >= 2 && !/workersMax/.test(v.js)) push({ id: 'F13', sev: 'error', edge: 20, src: '[N70]', msg: 'Two or more <video> elements: declare window.SCENE_META.workersMax = 1 (Chrome cannot seek several videos in parallel).' }, vids[0], '<video>');
  else if (vids.length === 1 && !/workersMax/.test(v.js)) push({ id: 'W05', sev: 'warning', edge: 20, src: '[N70]', msg: 'A <video> element is present: declare window.SCENE_META.workersMax = 1 if the scene is video-heavy.' }, vids[0], '<video>');

  // requirements
  const required = {};
  for (const q of REQUIRED) {
    const ok = q.test(v.js);
    required[q.key] = ok;
    const active = q.level === 99 ? opts.hf : q.level <= opts.level;
    if (!ok && active) out.push({ rule: q.id, severity: q.sev, line: 1, col: 1, match: '', message: q.msg, edge_case: q.key === 'fonts' ? 55 : (q.key === 'DURATION' || q.key === 'seek') ? 16 : null, source: '[N72]' });
  }
  out.sort((a, b) => a.line - b.line || a.col - b.col);
  const errors = out.filter(x => x.severity === 'error').length;
  const warnings = out.filter(x => x.severity === 'warning').length;
  return { file, ok: errors === 0 && !(opts.strict && warnings), errors, warnings, required, violations: out };
}

function lintFiles(files, opts) {
  const reports = files.map(f => lintSource(f, fs.readFileSync(f, 'utf8'), opts));
  const errors = reports.reduce((a, r) => a + r.errors, 0), warnings = reports.reduce((a, r) => a + r.warnings, 0);
  return { tool: 'lint_seek_contract.js', contract_version: CONTRACT_VERSION, level: opts.level, hf: opts.hf, strict: opts.strict, reports, summary: { files: reports.length, errors, warnings, ok: reports.every(r => r.ok) } };
}

// ---- selftest -----------------------------------------------------------------------
const GOOD = `<!doctype html><html><head><meta charset="utf-8"><title>good</title>
<style>/* animation: none; this CSS comment mentions animation: */ .a{color:#123}</style></head>
<body><video id="v" muted></video>
<script type="application/json" id="data">{"note":"Math.random Date.now setInterval are only text here"}</script>
<script>
// Math.random(), Date.now(), setInterval(), requestAnimationFrame() and .play() are named in comments only.
/* performance.now() in a block comment */
(function () {
  var P = new URLSearchParams(location.search), cues = P.get('cues'), seed = 7;
  function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  var rand = mulberry32(seed), fx = Object.freeze({ a: 1 }), thing = { replay: function () {}, randomized: 1 };
  thing.replay();
  window.__errors = []; window.SCENE_META = { contract: '1.0.0', workersMax: 1 };
  window.DURATION = 7.4;
  var wait = function () { setTimeout(function () {}, 50); }; // lint-allow: W01
  window.ready = document.fonts.load('40px serif', 'x').then(function () {});
  window.seek = async function (t) { await window.ready; return t; };
  window.__hf = { duration: 7.4, seek: function (t) { return window.seek(t); } };
})();
</script></body></html>`;

const BAD = `<!doctype html><html><head>
<script src="https://cdn.example.com/lib.js"></script>
<style>.x{animation: spin 2s infinite} @keyframes spin{to{opacity:0}}</style></head>
<body><video autoplay></video><video></video>
<script>
var a = Date.now(), b = new Date(), c = performance.now(), d = Math.random();
var e = crypto.getRandomValues(new Uint8Array(1));
setInterval(function () {}, 16);
requestAnimationFrame(function () {});
document.querySelector('video').play();
gsap.to(x, { repeat: -1 });
function tick() { draw(); setTimeout(tick, 16); }
tick();
</script></body></html>`;

function selftest() {
  let fails = 0;
  const ok = (name, cond, detail) => { console.log('  ' + (cond ? 'PASS' : 'FAIL') + ' ' + name + (!cond && detail ? ' - ' + detail : '')); if (!cond) fails++; };
  console.log('lint_seek_contract.js --selftest');
  const good = lintSource('good.html', GOOD, { level: 2, hf: true, strict: true });
  ok('good sample: 0 errors, 0 warnings (strict, level 2, --hf)', good.errors === 0 && good.warnings === 0, JSON.stringify(good.violations));
  ok('good sample: comments, JSON data block, .replay(), "randomized", lint-allow ignored/handled', good.violations.length === 0);
  const bad = lintSource('bad.html', BAD, { level: 2, hf: true, strict: false });
  const ids = new Set(bad.violations.map(x => x.rule));
  const expect = ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13', 'W01', 'W03', 'R01', 'R02', 'R04', 'R05', 'R08', 'R09', 'R10'];
  for (const id of expect) ok('bad sample reports ' + id, ids.has(id) || (id === 'W03' && ids.has('F14')));
  ok('level 1+: CSS animation/transition is error F14, not warning W03', ids.has('F14') && !ids.has('W03') && bad.violations.filter(x => x.rule === 'F14').every(x => x.severity === 'error'));
  const css0 = lintSource('t.html', '<style>.a{transition: opacity 1s}</style><script>window.DURATION = 1; window.seek = async (t) => t;</script>', { level: 0, hf: false, strict: false });
  ok('level 0: CSS transition stays warning W03', css0.errors === 0 && css0.violations.some(x => x.rule === 'W03' && x.severity === 'warning'), JSON.stringify(css0.violations));
  ok('bad sample fails (ok=false)', bad.ok === false && bad.errors > 10);
  const lvl0 = lintSource('only.js', 'window.DURATION = 3; window.seek = async (t) => t;', { level: 0, hf: false, strict: true });
  ok('level 0: minimal DURATION + async seek passes', lvl0.errors === 0 && lvl0.warnings === 0, JSON.stringify(lvl0.violations));
  const lvl1 = lintSource('only.js', 'window.DURATION = 3; window.seek = async (t) => t;', { level: 1, hf: false, strict: false });
  ok('level 1: same file fails (no ready / fonts / __errors)', lvl1.errors >= 3);
  const lines = bad.violations.filter(x => x.rule === 'F04');
  ok('line numbers are reported (Math.random on line 6)', lines.length === 1 && lines[0].line === 6, JSON.stringify(lines));
  console.log('selftest: ' + (fails ? 'FAILED (' + fails + ' failed)' : 'OK (0 failed)'));
  return fails ? 1 : 0;
}

// ---- main ---------------------------------------------------------------------------
function main(argv) {
  const opts = { level: 0, hf: false, strict: false };
  const files = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--selftest') return selftest();
    else if (a === '--level') { opts.level = parseInt(argv[++i], 10); if (![0, 1, 2].includes(opts.level)) { console.error('error: --level must be 0, 1 or 2'); return 2; } }
    else if (a === '--hf') opts.hf = true;
    else if (a === '--strict') opts.strict = true;
    else if (a.startsWith('--')) { console.error('error: unknown option ' + a); return 2; }
    else files.push(a);
  }
  if (!files.length) { console.error('usage: node lint_seek_contract.js [--level 0|1|2] [--hf] [--strict] FILE...\n       node lint_seek_contract.js --selftest'); return 2; }
  let report;
  try { report = lintFiles(files, opts); } catch (e) { console.error('error: ' + e.message); return 2; }
  console.log(JSON.stringify(report, null, 2));
  for (const r of report.reports) for (const x of r.violations) console.error(`${r.file}:${x.line}:${x.col} ${x.severity.toUpperCase()} ${x.rule} ${x.message}${x.source ? ' ' + x.source : ''}`);
  return report.summary.ok ? 0 : 1;
}

process.exitCode = main(process.argv.slice(2));
