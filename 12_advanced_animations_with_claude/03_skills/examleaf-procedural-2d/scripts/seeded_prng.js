#!/usr/bin/env node
'use strict';
/*
 * seeded_prng.js - deterministic randomness for seek-pure 2D scenes (no dependencies; browser or Node).
 *
 *   Node:    const P = require('./seeded_prng.js');      Browser: <script src="seeded_prng.js"></script> -> window.ExamLeafPRNG
 *   Selftest: node seeded_prng.js --selftest             (offline; exit 0 pass, 1 fail)
 *
 * mulberry32 and rngAt are byte-for-byte the formulas in
 * 12_advanced_animations_with_claude/04_harness_contract/scene_template.html section [7], so the same seed gives the
 * same values in template code and in these primitives.
 *   - mulberry32(seed): STATEFUL stream. Use only while building data once (in window.ready), in a fixed order.
 *   - rngAt(seed, i):   STATELESS. Safe inside render(t): same (seed, i) -> same value, in any seek order.
 * Edge case #17 (unseeded randomness) [N61]; boil helpers serve the 8-10 fps stop-motion boil ([V4-MP]).
 * ponytail: value noise (not Perlin/simplex); smooth enough for wobble and grain, upgrade only if a style needs it.
 */
(function (root) {
  const EPS = 1e-6;

  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const rngAt = (seed, i) => mulberry32((seed ^ Math.imul(i + 1, 0x9E3779B1)) >>> 0)();

  // FNV-1a 32-bit: stable seed from a name such as "phy-10-03-s04:straw:wobble".
  function hashSeed(str) {
    let h = 0x811C9DC5;
    for (const b of new TextEncoder().encode(String(str))) { h ^= b; h = Math.imul(h, 0x01000193) >>> 0; }
    return h >>> 0;
  }

  const range = (seed, i, lo, hi) => lo + (hi - lo) * rngAt(seed, i);
  const signed = (seed, i) => rngAt(seed, i) * 2 - 1;
  const pick = (seed, i, arr) => arr[Math.floor(rngAt(seed, i) * arr.length) % arr.length];

  // 1D value noise in [0,1): lattice values from rngAt, smoothstep blend. Pure function of (seed, x).
  function noise1D(seed, x) {
    const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
    const a = rngAt(seed, i), b = rngAt(seed, i + 1);
    return a + (b - a) * u;
  }

  // Stop-motion boil: index of the boil step at time t (constant for 1/fps seconds).
  const boilStep = (t, fps) => Math.floor(t * fps + EPS);

  // Wobble offset for point k of a stroke: re-seeded once per boil step, so it "boils" at 8-10 fps.
  function wobble(seed, k, t, boilFps, amp) {
    const s = boilStep(t, boilFps);
    const base = (k * 7919 + s * 104729) | 0;
    return [signed(seed, base) * amp, signed(seed, base + 1) * amp];
  }

  // Deterministic shuffle using a fresh stream (build-time only).
  function shuffled(seed, arr) {
    const r = mulberry32(seed), a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; }
    return a;
  }

  const API = { mulberry32, rngAt, hashSeed, range, signed, pick, noise1D, boilStep, wobble, shuffled, EPS };

  function selftest() {
    let fails = 0;
    const ok = (name, cond, extra) => { console.log('  ' + (cond ? 'PASS' : 'FAIL') + ' ' + name + (cond || !extra ? '' : ' - ' + extra)); if (!cond) fails++; };
    console.log('seeded_prng.js --selftest');
    const s1 = mulberry32(20261014), s2 = mulberry32(20261014);
    const a = [s1(), s1(), s1()], b = [s2(), s2(), s2()];
    ok('mulberry32 is reproducible for the same seed', a.every((v, i) => v === b[i]));
    ok('mulberry32 known answer (seed 1)', mulberry32(1)() === 0.6270739405881613, String(mulberry32(1)()));
    ok('mulberry32 values in [0,1)', a.every(v => v >= 0 && v < 1));
    const seq = [], idx = [...Array(200).keys()];
    for (const i of idx) seq[i] = rngAt(42, i);
    const shuffledIdx = shuffled(7, idx);
    ok('rngAt is order-independent (any seek order)', shuffledIdx.every(i => rngAt(42, i) === seq[i]));
    ok('rngAt differs across seeds', rngAt(1, 0) !== rngAt(2, 0));
    let sum = 0; for (let i = 0; i < 20000; i++) sum += rngAt(99, i);
    ok('rngAt mean near 0.5 (sanity, 20000 draws)', Math.abs(sum / 20000 - 0.5) < 0.02, String(sum / 20000));
    ok('hashSeed FNV-1a known answer ("abc" = 0x1a47e90b)', hashSeed('abc') === 0x1a47e90b, hashSeed('abc').toString(16));
    ok('hashSeed handles Devanagari names deterministically', hashSeed('प्रकाश') === hashSeed('प्रकाश') && hashSeed('प्रकाश') !== hashSeed('प्रकाष'));
    ok('range stays in bounds', idx.every(i => { const v = range(5, i, -6, 6); return v >= -6 && v < 6; }));
    const n0 = noise1D(3, 2.5), n1 = noise1D(3, 2.5 + 1e-4);
    ok('noise1D is continuous', Math.abs(n0 - n1) < 1e-3);
    ok('noise1D equals lattice value at integers', noise1D(3, 4) === rngAt(3, 4));
    ok('boilStep constant within a step at 8 fps', boilStep(1.0, 8) === boilStep(1.124, 8) && boilStep(1.125, 8) === 9);
    const w1 = wobble(11, 3, 2.00, 10, 4), w2 = wobble(11, 3, 2.09, 10, 4), w3 = wobble(11, 3, 2.10, 10, 4);
    ok('wobble holds within one boil step and changes at the next', w1[0] === w2[0] && w1[1] === w2[1] && (w3[0] !== w1[0] || w3[1] !== w1[1]));
    ok('wobble amplitude bounded', Math.abs(w1[0]) <= 4 && Math.abs(w1[1]) <= 4);
    ok('shuffled is a deterministic permutation', JSON.stringify(shuffled(7, idx)) === JSON.stringify(shuffledIdx) && [...shuffledIdx].sort((x, y) => x - y).every((v, i) => v === i));
    console.log('selftest: ' + (fails ? 'FAILED (' + fails + ' failed)' : 'OK (0 failed)'));
    return fails ? 1 : 0;
  }
  API.selftest = selftest;

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
    if (require.main === module) {
      if (process.argv.includes('--selftest')) process.exitCode = selftest();
      else { console.error('usage: node seeded_prng.js --selftest   (or require() it)'); process.exitCode = 2; }
    }
  } else {
    root.ExamLeafPRNG = API;
  }
})(typeof window !== 'undefined' ? window : globalThis);
