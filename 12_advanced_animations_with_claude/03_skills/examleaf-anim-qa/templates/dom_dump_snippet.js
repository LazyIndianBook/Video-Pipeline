// dom_dump_snippet.js - evaluate in the scene page AFTER `await window.seek(t)` (harness contract [N72]).
// Returns one sample: element boxes (canvas px), text, animated parts, and a camera sample.
// Uses only standard DOM APIs. The harness runner collects samples at every cue boundary + first/last frame
// and merges them into elements.json / dom_text.json (visible intervals = consecutive samples where visible).
// Tag scene elements with data-qa-id, data-qa-role (headline|text|caption|label|equation|critical|decor),
// optional data-qa-cue, data-qa-lang, data-qa-zone; animated sub-spans with data-qa-part.
(function sample(t) {
  const root = document.querySelector('[data-qa-root]') || document.body;
  const rootBox = root.getBoundingClientRect();
  const out = { t: t, elements: [], camera: null };
  document.querySelectorAll('[data-qa-id]').forEach(function (el) {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const visible = cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.01 && r.width > 0 && r.height > 0;
    const parts = Array.prototype.map.call(el.querySelectorAll('[data-qa-part]'), function (p) { return p.textContent; });
    out.elements.push({
      id: el.dataset.qaId, role: el.dataset.qaRole || 'decor', cue_id: el.dataset.qaCue || null,
      lang: el.dataset.qaLang || null, zone: el.dataset.qaZone || null,
      x: r.left - rootBox.left, y: r.top - rootBox.top, w: r.width, h: r.height,
      visible: visible, text: (el.textContent || '').trim(), parts: parts
    });
  });
  const cam = document.querySelector('[data-qa-camera]');
  if (cam) {
    const m = new DOMMatrixReadOnly(getComputedStyle(cam).transform === 'none' ? undefined : getComputedStyle(cam).transform);
    out.camera = { t: t, scale: Math.hypot(m.a, m.b), tx: m.e, ty: m.f };
  }
  return out;
})(window.__qa_t);
