#!/usr/bin/env python3
"""qa.py <script.json> [--no-stt] [--format concept_short_60] [--only new|A11,A12,...] [--no-dom]
Runs the pilot QA suite on a narrated, rendered tier folder and writes <tier>/qa/report.json + report.md:
  A1 seek-contract lint (node, level 1) per scene            A2 cue sheets validate (--production)
  A3 on-screen science text == fixture (DOM [data-fx] vs fixture values)   A4 safe zones (DOM boxes vs tokens)
  A5 flash test (per-frame luminance deltas from the MP4 via FFmpeg signalstats → flash_check.py)
  A6 loudness (ebur128 integrated / true peak)              A7 transcript check (local Whisper on the mix vs script words)
  A8 durations, wpm, think windows present                  A9 render manifest: errors, sources, determinism
  A10 video length = timeline. A11–A21: Professor Diki short-form checks (see the A11–A21 section; thresholds in its
  constants; --format concept_short_60 enforces them, --only new runs just A11–A21 and keeps A1–A10 from report.json)."""
import argparse, json, os, pathlib, re, statistics, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pilotlib as L
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
ANIM = ROOT / "12_advanced_animations_with_claude"
LINT = ANIM / "04_harness_contract/lint_seek_contract.js"; VALID = ANIM / "04_harness_contract/validate_cue_sheet.py"
TOKENS = ANIM / "04_harness_contract/vertical_safe_zones.tokens.json"
SAFE = ANIM / "03_skills/examleaf-anim-qa/scripts/safe_zone_check.py"; FLASH = ANIM / "03_skills/examleaf-anim-qa/scripts/flash_check.py"
NODE = "/Users/chinmoybhuyan/.nvm/versions/node/v24.6.0/bin/node"


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw); return r.returncode, (r.stdout + r.stderr)


def flatten(o, prefix=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items(): out.update(flatten(v, f"{prefix}{k}."))
    elif isinstance(o, list):
        for i, v in enumerate(o): out.update(flatten(v, f"{prefix}{i}."))
    else:
        out[prefix[:-1]] = o
    return out


NUM, canon = L.NUM, L.canon   # shared with narrate_voxcpm.py (27 Oct 2026)


# ============================================================================================================
# A11–A21: Professor Diki Simplified short-form checks (17_professor_diki_simplified/07_PIPELINE_CHANGES.md).
# Each check is a pure function over parsed inputs and returns {"status", "reasons", "evidence"}; main() gathers the
# inputs (MP4 duration, silencedetect, 2 fps frame series, DOM samples) so tests/test_regressions.py can feed
# synthetic ones. Thresholds live in the constants below; --format selects the row of FORMATS.
# ============================================================================================================

DIKI = ROOT / "17_professor_diki_simplified"
BRAND_CHECK = DIKI / "brand/brand_check.py"; BRAND_STRINGS = DIKI / "brand/strings.json"; DS_TOKENS = DIKI / "design_system/tokens.json"
FALLBACK_FORBIDDEN = [("F01", r"exam[\s_.\-]*leaf", "ExamLeaf"), ("F02", r"\bguarantee(s|d)?\b", "guarantee"),
                      ("F03", r"\bfull[\s-]+marks\b", "full marks"), ("F06", r"\bmind[\s-]*blown\b", "mind blown")]

# Formats with enforced thresholds. Any other format: A11 is judged at the script's own target and every A11–A21
# failure is reported as warn (the checks are written for Professor Diki shorts).
FORMATS = {"concept_short_60": {"target_s": 60.0, "tol_s": 1.0}, "explainer_60": {"target_s": 60.0, "tol_s": 1.0}}   # both short formats are enforced

# PD-01 pause policy: purpose -> (lo, hi) seconds (purpose names as pilotlib script v2). Scripted values may sit ±10 %
# outside the band; measured silences ±25 % (the QA tolerance). A pause without after_s gets the PD-01 default.
PAUSE_BANDS = {"join": (0.20, 0.35), "land": (0.50, 0.70), "inspect": (0.80, 1.20), "think_recall": (1.50, 1.50),
               "think_choice": (2.00, 2.00), "think_calc": (3.00, 3.00), "pause_video": (1.00, 1.00)}
PAUSE_DEFAULT = {"join": 0.25, "land": 0.6, "inspect": 1.0, "think_recall": 1.5, "think_choice": 2.0, "think_calc": 3.0, "pause_video": 1.0}
PAUSE_ALIASES = {"breath": "join", "land_result": "land", "inspect_formula": "inspect", "inspect_condition": "inspect",
                 "recall": "think_recall", "think_binary": "think_recall", "think_count": "think_recall",
                 "choose": "think_choice", "think_choose": "think_choice", "compute": "think_calc", "think_compute": "think_calc",
                 "think_one_step": "think_calc", "multi_step": "pause_video", "pause_the_video": "pause_video"}
SCRIPTED_TOL, MEASURED_TOL, MEASURED_ABS_S = 0.10, 0.25, 0.15   # measured: ±25 % or ±0.15 s, whichever is larger
SILENCE_DB, SILENCE_MIN_S = -40, 0.30       # silencedetect noise floor and minimum length (A13)
A20_MIN_S = 0.45                            # A20 counts pauses >= 0.45 s (PD-23: PD-01 joins of 0.2-0.35 s are designed, not dead time)
UNSCRIPTED_MAX_S = 0.60                     # A13: longest silence allowed with no scripted pause
UNSCRIPTED_SENTENCE_MAX_S = 0.80            # A13: ... unless it follows a sentence end inside a beat (the voice's own sentence break)
TAIL_HOLD_MAX_S = 1.00                      # A13: silent end-card hold allowed after the motif / last word
SILENCE_SHARE_MAX = 0.15                    # A20 (PD-07)
LEAD_IN_S = 0.3                             # A20: PD-16 lead-in, not counted as silence
INSIGHT_MAX_S, BOARD_BY_S = 10.0, 1.5       # A14 (PD-07)
FRAME_FPS, FRAME_W, FRAME_H = 2, 216, 384   # frame series: 2 fps, 0.2 scale, greyscale
EDGE_THR = 40                               # |dx|+|dy| grey levels for an "ink" (edge) pixel
EMPTY_ABS, EMPTY_REL = 0.02, 0.5            # empty = edge density < max(EMPTY_ABS, EMPTY_REL × median during speech)
CHANGE_MIN = 0.0015                         # A15: novel-edge fraction between 0.5 s samples that counts as a visual change
MOTION_THR, MOTION_MIN = 96, 0.0012         # A15: coherent motion (flowing dashes, a travelling marker) also counts: fraction of lane pixels whose grey value moves by > MOTION_THR between 0.5 s samples. Calibrated 17 Oct 2026: dashes >= 0.0030, the pilots' boil texture <= 0.0005 (boil must NOT count)
MAX_STATIC_S, MIN_CHANGES_PER_10S = 3.0, 3.3  # A15 (PD-07: change event every ≤ 3 s)
EMPTY_RUN_MAX_S = 1.0                       # A16: longest empty-diagram run allowed while speaking (2 samples at 2 fps)
FILL_HERO_OF_LANE, FILL_FRAME_FALLBACK = 0.70, 0.45  # A16: tokens fill.hero_min_of_diagram, else 45 % of frame height
SIM_MIN = 0.60                              # A17: consecutive-second diagram similarity floor
END_CARD_S = 2.5                            # A17: the last 2.5 s (or the last beat, whichever is shorter) is the end card
WPM_BAND, WPM_MIN_WORDS = (125, 165), 4     # A19
ENERGY_MIN_MARKS = 3                        # A21
ENERGY_WORDS = {"low": 2, "mid": 3, "high": 4, "peak": 5}      # script_v2_fields.md: low/mid/high/peak = 2/3/4/5; integers 1-5 as given
ENERGY_PEAK_SLOTS = ("reveal.answer", "check.transfer", "feedback.transfer", "explain.mechanism", "worked.step")   # question and explainer formats
# script v2 anchor slots: each must occur, first occurrences in this order (pilotlib.V2_ANCHORS when present)
ANCHORS = getattr(L, "V2_ANCHORS", ["hook.question_reveal", "check.predict", "reveal.answer", "check.transfer", "feedback.transfer",
                                    "close.next_step", "outro.brand"])


def res(status, reasons=None, **evidence):
    return {"status": status, "reasons": reasons or [], "evidence": evidence}


def verdict(fails, warns=(), **evidence):
    return res("fail" if fails else ("warn" if warns else "pass"), list(fails) + [f"(warn) {w}" for w in warns], **evidence)


def lanes():
    """Diagram and result lanes in frame pixels: design_system/tokens.json lanes.default if present, else the old middle zone
    (frame height × 0.54 centred) with a result lane under it."""
    try:
        t = json.loads(DS_TOKENS.read_text(encoding="utf-8")); L_ = t["lanes"]["default"]; f = t.get("fill", {})
        return {"diagram": (L_["diagram"]["y0"], L_["diagram"]["y1"]), "result": (L_["result"]["y0"], L_["result"]["y1"]),
                "hero_of_lane": f.get("hero_min_of_diagram", FILL_HERO_OF_LANE), "source": "design_system/tokens.json"}
    except Exception:
        return {"diagram": (round(1920 * 0.23), round(1920 * 0.77)), "result": (round(1920 * 0.77), round(1920 * 0.85)),
                "hero_of_lane": None, "source": "fallback 0.54 × height centred"}


# ---------------------------------------------------------------- input gathering (FFmpeg, frames, timeline)
def media_duration(ff, media):
    rc, out = run([ff, "-hide_banner", "-i", str(media)])
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else None


def detect_silences(ff, media, noise_db=SILENCE_DB, min_s=SILENCE_MIN_S):
    rc, out = run([ff, "-hide_banner", "-i", str(media), "-vn", "-af", f"silencedetect=noise={noise_db}dB:d={min_s}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", out)]; ends = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", out)]
    dur = media_duration(ff, media)
    return [(round(max(0.0, s0), 3), round(ends[i] if i < len(ends) else dur, 3)) for i, s0 in enumerate(starts)]


def silences_from_timeline(timeline, min_s=SILENCE_MIN_S):
    """Silences implied by word timings (used when there is no audio, e.g. synthetic fixtures)."""
    ws = [w for b in timeline["beats"] for w in b["words"]]; out = []; prev = 0.0
    for w in ws:
        if w["t0"] - prev >= min_s - 1e-6: out.append((round(prev, 3), round(w["t0"], 3)))
        prev = max(prev, w["t1"])
    if timeline["total_duration_s"] - prev >= min_s - 1e-6: out.append((round(prev, 3), round(timeline["total_duration_s"], 3)))
    return out


def speech_spans(timeline):
    return [(b["words"][0]["t0"], b["words"][-1]["t1"]) for b in timeline["beats"] if b.get("words")]


def in_speech(t, spans):
    return any(a <= t <= b for a, b in spans)


def frame_series(ff, mp4, ln=None, fps=FRAME_FPS):
    """Greyscale frames at 2 fps, 216×384. Per sample: edge density in the diagram lane, novel-edge fraction against the
    previous sample over diagram+result lanes (3×3 dilation absorbs 1 px boil), and similarity to the sample 1 s earlier."""
    import subprocess as sp
    ln = ln or lanes(); W = FRAME_W; n = W * FRAME_H
    raw = sp.run([ff, "-loglevel", "error", "-i", str(mp4), "-vf", f"fps={fps},scale={W}:{FRAME_H}:flags=area,format=gray", "-f", "rawvideo", "-"],
                 capture_output=True, check=True).stdout
    frames = [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]; k = FRAME_H / 1920
    d0, d1 = int(ln["diagram"][0] * k), int(ln["diagram"][1] * k); r1 = int(ln["result"][1] * k)

    def edges(f, y0, y1):
        s = set()
        for y in range(y0, y1 - 1):
            r = y * W
            for x in range(W - 1):
                p = f[r + x]
                if abs(p - f[r + x + 1]) + abs(p - f[r + W + x]) > EDGE_THR: s.add(r + x)
        return s

    def dil(m):
        o = set()
        for i in m: o.update((i - W - 1, i - W, i - W + 1, i - 1, i, i + 1, i + W - 1, i + W, i + W + 1))
        return o
    dg = [edges(f, d0, d1) for f in frames]; full = [edges(f, d0, r1) for f in frames]
    dgd = [dil(m) for m in dg]; fud = [dil(m) for m in full]; area_d = (d1 - d0) * W; area_f = (r1 - d0) * W
    out = []
    lane_lo, lane_hi = d0 * W, r1 * W
    for i in range(len(frames)):
        nov = (len(full[i] - fud[i - 1]) + len(full[i - 1] - fud[i])) / area_f if i else 0.0
        if i:
            a, b = frames[i][lane_lo:lane_hi], frames[i - 1][lane_lo:lane_hi]
            motion = sum(1 for x, y in zip(a, b) if (x - y if x > y else y - x) > MOTION_THR) / area_f
        else: motion = 0.0
        j = i - fps; sim = None
        if j >= 0 and (dg[j] or dg[i]):
            sim = (len(dgd[j] & dg[i]) + len(dgd[i] & dg[j])) / (len(dg[i]) + len(dg[j]))
        out.append({"t": round(i / fps, 2), "edge": round(len(dg[i]) / area_d, 5), "novelty": round(nov, 5), "motion": round(motion, 5), "sim": None if sim is None else round(sim, 3)})
    return out


def empty_floor(series, spans):
    sp_ = [x["edge"] for x in series if in_speech(x["t"], spans)] or [x["edge"] for x in series] or [0]
    return max(EMPTY_ABS, EMPTY_REL * statistics.median(sp_))


def runs(flags, step):
    """[(t_start, length_s)] of consecutive True samples; flags = [(t, bool)]."""
    out = []; cur = None
    for t, f in flags:
        if f:
            cur = cur or [t, 0.0]; cur[1] += step
        elif cur:
            out.append(tuple(cur)); cur = None
    if cur: out.append(tuple(cur))
    return out


def beat_start(timeline, beat_id):
    for b in timeline["beats"]:
        if b["id"] == beat_id: return b["words"][0]["t0"] if b.get("words") else b["start"]
    return None


def insight_beat_id(script):
    ib = script.get("insight_beat")
    if isinstance(ib, dict): ib = ib.get("beat") or ib.get("id")
    if isinstance(ib, str): return ib
    return next((b["id"] for b in script["beats"] if b.get("insight_beat") is True or b.get("insight") is True), None)


# ---------------------------------------------------------------- the checks
def a11_duration(duration, fmt, script):
    """A11: muxed length 60 ± 1 s for concept_short_60; other formats warn at their own target ± 1 s."""
    f = FORMATS.get(fmt)
    target, tol = (f["target_s"], f["tol_s"]) if f else (float(script.get("target_duration_s") or 0), 1.0)
    if duration is None: return res("fail", ["no MP4 duration"])
    ok = abs(duration - target) <= tol
    return res("pass" if ok else ("fail" if f else "warn"), [] if ok else [f"duration {duration:.2f} s outside {target:.1f} ± {tol:.1f} s"],
               duration_s=round(duration, 3), target_s=target, tolerance_s=tol, format=fmt)


def forbidden_patterns():
    try:
        return [(f["id"], re.compile(f["pattern"], re.I), f["label"]) for f in json.loads(BRAND_STRINGS.read_text(encoding="utf-8"))["forbidden"]]
    except Exception:
        return [(i, re.compile(p, re.I), lab) for i, p, lab in FALLBACK_FORBIDDEN]


def a12_brand(build_dir, dom_texts=None, captions=None, transcript=None):
    """A12: brand_check.py (spoken text, scene source text, fixture strings, metadata, end-card items) plus what it cannot
    see: on-screen DOM text at sampled times [(where, text)], burnt/sidecar captions and the STT transcript."""
    fails = []; ev = {}
    if BRAND_CHECK.exists():
        rc, out = run([sys.executable, str(BRAND_CHECK), str(build_dir)])
        try:
            rep = json.loads(out[out.index("{"):])
        except Exception:
            rep = {"status": "error", "raw": out[-300:]}
        ev["brand_check"] = {"status": rep.get("status"), "violations": len(rep.get("violations", [])), "scanned": rep.get("scanned")}
        for v in rep.get("violations", []):
            fails.append(f"forbidden '{v['label']}' ({v['id']}) in {v['scope']} {v['where']}")
        for r in rep.get("required", []):
            if not r["ok"]: fails.append(f"missing end-card item {r['item']}")
        if rep.get("status") == "error": fails.append(f"brand_check.py error: {rep.get('error') or rep.get('raw')}")
    else:
        ev["brand_check"] = "absent: built-in forbidden list only"
        s = json.loads((pathlib.Path(build_dir) / "script.json").read_text(encoding="utf-8"))
        dom_texts = list(dom_texts or []) + [(f"spoken script.json#{b['id']}", b.get("text", "")) for b in s.get("beats", [])]
    pats = forbidden_patterns(); extra = list(dom_texts or [])
    if captions: extra.append(("captions narration/captions.vtt", captions))
    if transcript: extra.append(("transcript qa/transcript.json", transcript))
    seen = set()
    for where, text in extra:
        for fid, rx, label in pats:
            m = rx.search(text or "")
            if m and (fid, where.split(" @")[0]) not in seen:
                seen.add((fid, where.split(" @")[0])); fails.append(f"forbidden '{label}' ({fid}) in {where}")
    ev["extra_sources_scanned"] = len(extra)
    return verdict(fails, **ev)


def _purpose(p):
    pur = str(p.get("purpose", "")).strip().lower().replace(" ", "_").replace("-", "_")
    if pur == "think" and p.get("difficulty"): pur = "think_" + str(p["difficulty"]).lower()
    return PAUSE_ALIASES.get(pur, pur)


def _pause_len(p):
    for k in ("after_s", "s", "seconds", "duration_s"):
        if k in p: return float(p[k])
    return PAUSE_DEFAULT.get(_purpose(p))


def end_pauses(b):
    """Pauses placed after the beat's last word (`at` omitted or "end"), as narrate.py places them."""
    p = b.get("pauses"); p = [p] if isinstance(p, dict) else (p or [])
    return [x for x in p if x.get("at", "end") == "end"]


def _at_sentence_end(timeline, t, script=None):
    """True when the last word spoken before time t ends a sentence (. ? !) in the SCRIPT text (timeline words carry no
    punctuation), i.e. the silence is the voice's own sentence break inside a beat."""
    raw = {}
    for b in (script or {}).get("beats", []):
        toks = [x for x in str(b.get("text", "")).split() if any(ch.isalnum() for ch in x)]
        raw[b["id"]] = toks
    last = None
    for b in timeline["beats"]:
        toks = raw.get(b["id"], [])
        for i, w in enumerate(b.get("words") or []):
            if w["t0"] <= t + 0.08 and (last is None or w["t0"] > last[0]):     # the word that started last before the silence
                tok = toks[i] if i < len(toks) else str(w["w"])                 # (alignment word ends often swallow the pause itself)
                last = (w["t0"], tok)
    return bool(last) and str(last[1]).rstrip('"\')').endswith((".", "?", "!", ":", ";"))   # clause ends too: the voice pauses at a colon


def a13_pauses(script, timeline, silences, duration):
    """A13 (PD-01): every silence ≥ 0.3 s sits in a scripted pause whose purpose band (±25 %) contains it; no unscripted
    silence > 0.6 s; the end-card hold after the last word ≤ 1.0 s. `pauses[].after_s` is read as the pause length after
    the beat (script v2; PD-01 default when omitted); scripted lengths must be inside their band ±10 %."""
    fails, warns = [], []
    sb = {b["id"]: b for b in script["beats"]}; tb = timeline["beats"]
    if not any(b.get("pauses") for b in script["beats"]):
        fails.append("script has no pauses[] with purpose labels (legacy pause_after_s/think_window_s)")
    gaps = []   # (beat_id, gap_start, gap_end, purposes, scripted_s, band)
    for i, b in enumerate(tb):
        ps = end_pauses(sb.get(b["id"], {}))
        if not b.get("words"): continue
        g0 = b["words"][-1]["t1"]; g1 = next((x["words"][0]["t0"] for x in tb[i + 1:] if x.get("words")), duration)
        purs, lo, hi, tot = [], 0.0, 0.0, 0.0
        for p in ps:
            pur = _purpose(p); L_ = _pause_len(p); purs.append(pur)
            if pur not in PAUSE_BANDS: fails.append(f"{b['id']}: pause purpose '{p.get('purpose')}' not in the PD-01 table"); continue
            blo, bhi = PAUSE_BANDS[pur]; lo += blo; hi += bhi; tot += L_ or 0
            if L_ is None: fails.append(f"{b['id']}: pause '{pur}' has no after_s")
            elif not (blo * (1 - SCRIPTED_TOL) - 1e-9 <= L_ <= bhi * (1 + SCRIPTED_TOL) + 1e-9):
                fails.append(f"{b['id']}: scripted {pur} pause {L_:.2f} s outside {blo:.2f}–{bhi:.2f} s ±10 %")
        gaps.append((b["id"], g0, g1, purs, tot, (lo, hi) if purs and all(x in PAUSE_BANDS for x in purs) else None))
    matched = set(); checked = []
    for s0, s1 in silences:
        L_ = s1 - s0
        if L_ < SILENCE_MIN_S - 1e-6: continue
        best = max(gaps, key=lambda g: min(s1, g[2]) - max(s0, g[1]), default=None)
        ov = (min(s1, best[2]) - max(s0, best[1])) if best else 0
        if best and ov > 0.05 and best[5]:
            lo, hi = best[5]; matched.add(best[0]); checked.append((best[0], round(L_, 2), "+".join(best[3])))
            if not (min(lo * (1 - MEASURED_TOL), lo - MEASURED_ABS_S) <= L_ <= max(hi * (1 + MEASURED_TOL), hi + MEASURED_ABS_S)):
                fails.append(f"silence {s0:.2f}–{s1:.2f} s ({L_:.2f} s) after {best[0]} outside {'+'.join(best[3])} {lo:.2f}–{hi:.2f} s ±25 % / ±{MEASURED_ABS_S:.2f} s")
        elif s1 >= duration - 0.05 and s0 > 0.05:
            if L_ > TAIL_HOLD_MAX_S + 1e-6: fails.append(f"tail silence {s0:.2f}–{s1:.2f} s ({L_:.2f} s) > {TAIL_HOLD_MAX_S:.1f} s end-card hold")
        elif L_ > (UNSCRIPTED_SENTENCE_MAX_S if _at_sentence_end(timeline, s0, script) else UNSCRIPTED_MAX_S) + 1e-6:
            fails.append(f"unscripted silence {s0:.2f}–{s1:.2f} s ({L_:.2f} s) > {UNSCRIPTED_MAX_S:.1f} s")
    for bid, g0, g1, purs, tot, band in gaps:
        if band and tot >= 0.45 and bid not in matched:   # shorter scripted pauses may legitimately measure < 0.3 s
            warns.append(f"scripted {'+'.join(purs)} pause after {bid} ({tot:.2f} s) not found in the audio")
    return verdict(fails, warns, silences_ge_0_3=len([x for x in silences if x[1] - x[0] >= SILENCE_MIN_S]), matched=checked[:20], failures_total=len(fails))


def a14_first_idea(script, timeline, series=None, spans=None):
    """A14 (PD-07, PD-16): the insight beat (the first usable idea: givens plus first result; the reveal is payoff_beat) starts ≤ 10 s; the diagram lane is not empty at 1.5 s (edge density ≥ the empty floor)."""
    fails = []; ev = {}
    ib = insight_beat_id(script)
    if ib is None:
        first_exp = next((b for b in timeline["beats"] if b.get("slot", "").startswith(("explain", "worked", "name"))), None)
        fails.append("no insight_beat declared" + (f"; first explain beat {first_exp['id']} starts at {first_exp['words'][0]['t0']:.1f} s" if first_exp and first_exp.get("words") else ""))
    else:
        t = beat_start(timeline, ib); ev["insight_beat"] = ib; ev["insight_start_s"] = t
        if t is None: fails.append(f"insight_beat {ib} not in timeline")
        elif t > INSIGHT_MAX_S: fails.append(f"insight beat {ib} starts at {t:.1f} s > {INSIGHT_MAX_S:.0f} s")
    if series:
        fl = empty_floor(series, spans or speech_spans(timeline)); at = min(series, key=lambda x: abs(x["t"] - BOARD_BY_S))
        ev.update(board_edge_at_1_5s=at["edge"], empty_floor=round(fl, 4))
        if at["edge"] < fl: fails.append(f"diagram lane empty at {BOARD_BY_S} s (edge density {at['edge']:.3f} < {fl:.3f})")
    else:
        ev["board"] = "no frames: board-visible part not checked"
    return verdict(fails, **ev)


def a15_change_density(timeline, series):
    """A15 (PD-07): during speech no static run > 3.0 s in the diagram+result lanes (novel-edge fraction ≥ CHANGE_MIN between
    0.5 s samples counts as a change); report changes per 10 s of speech (warn below 3.3)."""
    if not series: return res("skipped", ["no frames"])
    spans = speech_spans(timeline); step = 1 / FRAME_FPS; run_s = 0.0; run_t = None; worst = (0.0, None); n_ch = 0; sp_s = 0.0
    for x in series:
        ch = x["novelty"] >= CHANGE_MIN or x.get("motion", 0.0) >= MOTION_MIN; sp = in_speech(x["t"], spans)
        if sp: sp_s += step; n_ch += ch
        if ch: run_s, run_t = 0.0, None
        elif sp:
            run_t = run_t if run_t is not None else x["t"]; run_s += step
            if run_s > worst[0]: worst = (run_s, run_t)
    rate = n_ch / sp_s * 10 if sp_s else 0
    fails = [f"no visual change for {worst[0]:.1f} s from {worst[1]:.1f} s during speech (> {MAX_STATIC_S:.0f} s)"] if worst[0] > MAX_STATIC_S + 1e-6 else []
    warns = [f"{rate:.1f} changes per 10 s of speech < {MIN_CHANGES_PER_10S}"] if rate < MIN_CHANGES_PER_10S else []
    return verdict(fails, warns, longest_static_s=worst[0], longest_static_from_s=worst[1], changes=n_ch, changes_per_10s=round(rate, 2), change_threshold=CHANGE_MIN)


def a16_diagram_fill(timeline, series, hero=None, ln=None):
    """A16: no empty diagram lane while speaking (run ≥ 1.0 s below the empty floor fails), and the hero bounding box
    (Diki.hero-registered elements or [data-role=hero], from the DOM at 25/50/75 % of runtime) fills ≥ tokens fill.hero_min_of_diagram of the diagram lane
    (fallback without tokens: ≥ 45 % of frame height). hero = [(t, height_px or None)]."""
    fails, ev = [], {}
    ln = ln or lanes()
    if series:
        spans = speech_spans(timeline); fl = empty_floor(series, spans)
        empt = runs([(x["t"], x["edge"] < fl and in_speech(x["t"], spans)) for x in series], 1 / FRAME_FPS)
        ev.update(empty_floor=round(fl, 4), empty_speech_s=round(sum(r[1] for r in empt), 1), empty_runs=[(t, L_) for t, L_ in empt][:10])
        for t, L_ in empt:
            if L_ >= EMPTY_RUN_MAX_S - 1e-6: fails.append(f"diagram lane empty for {L_:.1f} s from {t:.1f} s while speaking")
    if hero is not None:
        lane_h = ln["diagram"][1] - ln["diagram"][0]; need = ln["hero_of_lane"] * lane_h if ln["hero_of_lane"] else FILL_FRAME_FALLBACK * 1920
        ev["hero_height_px"] = hero; ev["hero_min_px"] = round(need)
        for row in hero:
            t, h = row[0], row[1]; lane_meas = row[2] if len(row) > 2 else None     # the lane the scene actually uses (carded layouts are shorter)
            need_t = ln["hero_of_lane"] * lane_meas if (ln["hero_of_lane"] and lane_meas) else need
            if lane_meas: ev["hero_min_px"] = round(need_t); ev["diagram_lane_px"] = round(lane_meas)
            if h is None: fails.append(f"no visible hero (Diki.hero / [data-role=hero]) at {t:.1f} s")
            elif h < need_t: fails.append(f"hero height {h:.0f} px at {t:.1f} s < {need_t:.0f} px ({h / 1920:.0%} of frame)")
    return verdict(fails, **ev) if (series or hero is not None) else res("skipped", ["no frames, no DOM"])


def a17_persistence(timeline, series, duration, script=None):
    """A17 (PD-03): one scene file; diagram-lane similarity between samples 1 s apart never drops below SIM_MIN outside the
    end card; samples whose earlier frame is empty are skipped (building from nothing is A14/A16's business)."""
    pre = [f"{len(script['scenes'])} scene files (PD-03: one persistent scene)"] if script and len(script.get("scenes", [])) > 1 else []
    if not series: return verdict(pre) if pre else res("skipped", ["no frames"])
    last = timeline["beats"][-1]; end_from = max(duration - END_CARD_S, last["words"][0]["t0"] if last.get("words") else last["start"])
    fl = empty_floor(series, speech_spans(timeline)); by_t = {x["t"]: x for x in series}; worst = (1.0, None); drops = []
    for x in series:
        prev = by_t.get(round(x["t"] - 1.0, 2))
        if x["sim"] is None or x["t"] >= end_from or prev is None or prev["edge"] < fl: continue
        if x["sim"] < worst[0]: worst = (x["sim"], x["t"])
        if x["sim"] < SIM_MIN and not (drops and x["t"] - drops[-1][1] <= 1.0): drops.append((x["sim"], x["t"]))
    fails = pre + [f"diagram similarity {s:.2f} at {t:.1f} s < {SIM_MIN:.2f} (teardown)" for s, t in drops]
    return verdict(fails, min_similarity=worst[0], min_similarity_t=worst[1], end_card_from_s=round(end_from, 2), threshold=SIM_MIN)


def _spoken_forms(v):
    """Digit and word forms of a fixture number as a script may speak it."""
    if isinstance(v, bool) or not isinstance(v, (int, float)): return {str(v).lower()}
    inv = {d: w for w, d in NUM.items()}; s = f"{v:g}"; forms = {s}
    if s in inv: forms.add(inv[s])
    if "." in s:
        ip, fp = s.split(".", 1); fd = " ".join(fp); fw = " ".join(inv.get(c, c) for c in fp)
        forms |= {f"{ip} point {fd}", f"point {fd}", f"{inv.get(ip, ip)} point {fw}", f"point {fw}", " ".join(inv.get(ch, ch) if ch != "." else "point" for ch in s)}
    return forms


def _fx(fixture, path):
    v = fixture
    for k in path.split("."):
        if not isinstance(v, dict) or k not in v: return None
        v = v[k]
    return v


def a18_teaching_order(script, fixture=None, check_script_problems=None):
    """A18 (PD-06): hook first; the script v2 anchor slots all present with first occurrences in order (hook → predict →
    reveal.answer → check.transfer → feedback.transfer → close.next_step → outro.brand); check.transfer has a think pause;
    the predict beat's givens (`check.answerable_from`, else `givens`, else its parameters.* fx_refs) are on screen
    (fx_refs) at or before the question, and numeric givens are spoken by then. check_script_problems: the
    prediction lines check_script.py printed (its own answerable heuristic), added as reasons."""
    fails = []; beats = script["beats"]; slots = [b["slot"] for b in beats]
    anchors = getattr(L, "anchors_for", lambda sc: ANCHORS)(script)        # explainer_60 has no questions (PD-24)
    if script.get("format") == "explainer_60" and hasattr(L, "spine_problems"):
        fails += L.spine_problems(script); anchors = []                   # PD-26: purpose first, pay-off before the invitation
    elif not slots or slots[0] != anchors[0]: fails.append(f"first beat is not {anchors[0]}")
    for a in anchors:
        if a not in slots: fails.append(f"missing slot {a}")
    firsts = [(slots.index(a), a) for a in anchors if a in slots]
    for (i1, a1), (i2, a2) in zip(firsts, firsts[1:]):
        if i2 < i1: fails.append(f"slot order: {a2} ({beats[i2]['id']}) before {a1} ({beats[i1]['id']})")
    ti = slots.index("check.transfer") if "check.transfer" in slots else None
    if ti is not None and not any(_purpose(p).startswith(("think", "pause_video")) for p in end_pauses(beats[ti])):
        fails.append(f"check.transfer {beats[ti]['id']} has no think pause")
    pi = slots.index("check.predict") if "check.predict" in slots else None; givens_ev = None
    if pi is not None:
        p = beats[pi]
        givens = (p.get("check") or {}).get("answerable_from") or p.get("givens") or [x for x in (p.get("on_screen") or {}).get("fx_refs", []) if x.startswith("parameters.")]
        shown = {x for b in beats[:pi + 1] for x in (b.get("on_screen") or {}).get("fx_refs", [])}
        said = " " + " ".join(canon([L.norm_word(w) for b in beats[:pi + 1] for w in L.words_of(b["text"])])) + " "
        givens_ev = givens
        if not givens: fails.append(f"check.predict {p['id']} declares no givens")
        for g in givens:
            later = next((b["id"] for b in beats[pi + 1:] if g in (b.get("on_screen") or {}).get("fx_refs", [])), None)
            v = _fx(fixture, g) if fixture is not None else None
            if g not in shown:
                fails.append(f"check.predict {p['id']} asks before its given {g} is shown" + (f" (first shown in {later})" if later else ""))
            elif isinstance(v, (int, float)) and not isinstance(v, bool) and not any(f" {f} " in said for f in _spoken_forms(v)):
                fails.append(f"check.predict {p['id']}: given {g} = {v} is not spoken by then")
    for x in check_script_problems or []:
        fails.append(f"check_script: {x}")
    return verdict(fails, slots=slots, givens=givens_ev)


def a19_pace(timeline, band=WPM_BAND, script=None):
    """A19: active wpm per beat (words / first-to-last-word span) inside 125–165 scaled by the script's voice.rate_scale
    (PD-22); beats under 4 words are not rated. Outside the scaled band warns (delivery varies by beat); beyond ±30 % of
    the band edges fails (a rushed or dragging beat)."""
    rs = float(((script or {}).get("voice") or {}).get("rate_scale") or 1.0); lo, hi = band[0] * rs, band[1] * rs
    if (script or {}).get("pace") == "fast": lo, hi = 150.0, 215.0                                   # PD-28 fast profile
    fails, warns, rows = [], [], []
    for b in timeline["beats"]:
        ws = b.get("words") or []
        if len(ws) < WPM_MIN_WORDS: rows.append((b["id"], len(ws), None)); continue
        span = ws[-1]["t1"] - ws[0]["t0"]; wpm = len(ws) / span * 60 if span > 0 else 0; rows.append((b["id"], len(ws), round(wpm)))
        if wpm < lo * 0.7 or wpm > hi * 1.3: fails.append(f"{b['id']} {wpm:.0f} wpm beyond ±30 % of {lo:.0f}–{hi:.0f}")
        elif not lo <= wpm <= hi: warns.append(f"{b['id']} {wpm:.0f} wpm outside {lo:.0f}–{hi:.0f}")
    return verdict(fails, warns, per_beat=rows, band=[round(lo), round(hi)], rate_scale=rs)


def a20_silence_share(silences, duration, timeline=None, fmt=None, script=None):
    """A20 (PD-07, PD-23): silence (pauses ≥ 0.45 s below −40 dB; the room-tone bed counts as silence) ≤ 15 % of runtime. Same
    definition as the plan (pilotlib.silence_share): the first LEAD_IN_S of the video and the end-card tail after the last
    word are not counted (A13 polices both)."""
    last = max((b["words"][-1]["t1"] for b in (timeline or {}).get("beats", []) if b.get("words")), default=duration)
    gap_starts = [b["words"][-1]["t1"] for b in (timeline or {}).get("beats", []) if b.get("words")]   # scripted gaps start at beat ends
    tot = 0.0
    for s0, s1 in silences:
        s0, s1 = max(s0, LEAD_IN_S if s0 <= 0.05 else s0), min(s1, last)
        L_ = s1 - s0
        if L_ < A20_MIN_S - 1e-6: continue
        scripted = any(abs(s0 - g) < 0.25 for g in gap_starts)
        if not scripted and timeline is not None and L_ <= UNSCRIPTED_SENTENCE_MAX_S and _at_sentence_end(timeline, s0, script):
            continue                                                 # the voice's own sentence break inside a beat (PD-23), not dead time
        tot += L_
    share = tot / duration if duration else 1
    share_max = getattr(L, "SILENCE_MAX_BY_FORMAT", {}).get(fmt, SILENCE_SHARE_MAX)
    if (script or {}).get("pace") == "fast": share_max = min(share_max, 0.08)                      # PD-28
    return verdict([f"silence {share:.1%} of runtime > {share_max:.0%}"] if share > share_max else [],
                   silence_s=round(tot, 2), duration_s=round(duration, 2), share=round(share, 3))


def _energy(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool): return float(v)
    if isinstance(v, dict): v = v.get("level", v.get("mark"))
    if isinstance(v, (int, float)): return float(v)
    return ENERGY_WORDS.get(str(v).lower()) if v is not None else None


def a21_energy(script):
    """A21 (digest §6): beats carry `energy` marks (low|mid|high|peak or 1-5); ≥ 3 distinct marks; the highest mark falls on
    reveal.answer, check.transfer or feedback.transfer (or the payoff_beat / insight beat)."""
    marks = [(b["id"], b["slot"], _energy(b.get("energy"))) for b in script["beats"]]
    have = [m for m in marks if m[2] is not None]
    if not have: return res("fail", ["no energy marks in script (beats[].energy absent)"], tags=[(b["id"], b.get("tag")) for b in script["beats"]])
    fails = []; distinct = sorted({m[2] for m in have}); top = max(distinct); ib = insight_beat_id(script)
    if len(distinct) < ENERGY_MIN_MARKS: fails.append(f"{len(distinct)} distinct energy marks < {ENERGY_MIN_MARKS}")
    peaks = [m for m in have if m[2] == top]
    payoff = {b["id"] for b in script["beats"] if b.get("payoff_beat") is True} | ({script["payoff_beat"]} if isinstance(script.get("payoff_beat"), str) else set())
    ok = any(bid == ib or bid in payoff or sl in ENERGY_PEAK_SLOTS or (not sl.startswith("hook") and "reveal" in sl) for bid, sl, _ in peaks)
    if not ok: fails.append(f"energy peak {top:g} on {', '.join(p[0] for p in peaks)}, not on the reveal or the transfer")
    unmarked = [m[0] for m in marks if m[2] is None]
    return verdict(fails, [f"beats without energy: {', '.join(unmarked)}"] if unmarked else [], curve=[(m[0], m[2]) for m in marks], peak=top)


NEW_CHECKS = {"A11": ("duration 60 ± 1 s (concept_short_60)", "critical"), "A12": ("brand: no forbidden string anywhere; end card", "critical"),
              "A13": ("pause policy by purpose (PD-01)", "major"), "A14": ("first usable idea ≤ 10 s; board by 1.5 s", "major"),
              "A15": ("change events: none > 3 s static during speech", "major"), "A16": ("diagram never empty while speaking; hero fill", "major"),
              "A17": ("persistence: no teardown before the end card", "critical"), "A18": ("teaching order: predict with givens, transfer", "critical"),
              "A19": ("pace per beat 125–165 wpm", "major"), "A20": ("silence ≤ 15 % of runtime", "critical"), "A21": ("energy curve: ≥ 3 marks, peak at reveal/transfer", "major")}


def _text_matches(text, exp, dec):
    """On-screen text equals the fixture value: exactly, or formatted with the element's data-fx-dec decimals, or numerically."""
    if text == exp: return True
    if "".join(str(text).split()) == "".join(str(exp).split()): return True   # chips split a label into words; textContent drops the spaces
    try:
        if abs(float(text) - float(exp)) < 1e-9: return True        # "0.20" shows 0.2 with the fixture's decimals
    except (TypeError, ValueError):
        pass
    try:
        return dec not in (None, "") and text == f"{float(exp):.{int(dec)}f}"
    except (TypeError, ValueError):
        return False                                                 # dec may be a fixture path; numeric equality above covers it


def dom_samples(d, s, fixture, timeline, hero_times):
    """Playwright: visible text in every scene every 2 s (and 0.3 s before its end), and the [data-role=hero] height at the
    given video times. Returns ([(where, text)], [(t, height_px or None)])."""
    JS_TEXT = """() => { const out = []; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
      while ((n = w.nextNode())) { const t = n.textContent.trim(); const e = n.parentElement; if (!t || !e || ['SCRIPT','STYLE','TITLE'].includes(e.tagName)) continue;
        let op = 1, vis = true; for (let x = e; x && x.nodeType === 1; x = x.parentElement) { const cs = getComputedStyle(x); op *= parseFloat(cs.opacity || '1'); if (cs.display === 'none') { vis = false; break; } }
        const r = e.getBoundingClientRect(); if (vis && getComputedStyle(e).visibility !== 'hidden' && op > 0.05 && r.width > 0 && r.height > 0) out.push(t); }
      return out.join(' '); }"""
    # hero = elements registered with the design-system runtime (Diki.hero -> window.__diki_qa.hero_fill ids) or marked
    # data-role="hero"; the union of the visible ones is measured at the sample time
    JS_HERO = """() => { const ids = ((window.__diki_qa || {}).hero_fill || []).map(h => h.id).filter(Boolean);
      const els = [...ids.map(i => document.getElementById(i)), ...document.querySelectorAll('[data-role="hero"]')].filter(Boolean);
      let y0 = Infinity, y1 = -Infinity;
      for (const h of els) { const r = h.getBoundingClientRect(); const cs = getComputedStyle(h);
        if (r.height > 0 && cs.opacity !== '0' && cs.visibility !== 'hidden' && cs.display !== 'none') { y0 = Math.min(y0, r.top); y1 = Math.max(y1, r.bottom); } }
      const ld = document.getElementById('lane-diagram'); const lane = ld ? ld.getBoundingClientRect().height : null;
      return {h: y1 > y0 ? y1 - y0 : null, lane}; }"""
    texts, hero = [], []; scenes = {x["id"]: x for x in timeline["scenes"]}
    with sync_playwright() as p:
        for sc in s["scenes"]:
            sheet = json.loads((d / "cues" / f"{sc['id']}.cues.json").read_text(encoding="utf-8")); st = scenes[sc["id"]]
            b, page = L.open_scene(p, d / sc["file"], sheet, fixture); dur = sheet["duration"]
            for t in sorted({round(x * 2.0, 2) for x in range(int(dur // 2) + 1)} | {max(0.0, round(dur - 0.3, 2))}):
                page.evaluate(f"window.seek({t})"); texts.append((f"on screen {sc['id']} @ {st['start'] + t:.1f} s", page.evaluate(JS_TEXT)))
            for T in hero_times:
                if st["start"] <= T < st["end"] or (T >= st["end"] and sc is s["scenes"][-1]):
                    page.evaluate(f"window.seek({min(dur, T - st['start'])})"); hr = page.evaluate(JS_HERO); hero.append((round(T, 1), hr["h"], hr["lane"]))
            b.close()
    return texts, hero


def run_new_checks(s, d, fmt, ff, dom=True):
    """Gather inputs from a narrated, rendered build folder and run A11–A21. Returns [(id, result)]."""
    timeline = json.loads((d / "narration/timeline.json").read_text(encoding="utf-8"))
    fixture = json.loads((d / "fixtures/fixture.json").read_text(encoding="utf-8"))
    final = d / "render" / f"{s['video_id']}.mp4"; duration = media_duration(ff, final)
    silences = detect_silences(ff, final); ln = lanes(); series = frame_series(ff, final, ln); spans = speech_spans(timeline)
    texts, hero = dom_samples(d, s, fixture, timeline, [duration * f for f in (0.25, 0.5, 0.75)]) if dom else ([], None)
    cap = (d / "narration/captions.vtt").read_text(encoding="utf-8") if (d / "narration/captions.vtt").exists() else None
    tr = json.loads((d / "qa/transcript.json").read_text(encoding="utf-8")).get("text") if (d / "qa/transcript.json").exists() else None
    rc, cs_out = run([sys.executable, str(pathlib.Path(__file__).resolve().parent / "check_script.py"), str(d / "script.json")])
    prior = [ln.strip(" -") for ln in cs_out.splitlines() if "prediction not answerable" in ln or "answerable_from" in ln]
    (d / "qa").mkdir(exist_ok=True)
    (d / "qa/frame_series.json").write_text(json.dumps({"lanes": ln, "series": series, "silences": silences}, ensure_ascii=False), encoding="utf-8")
    out = [("A11", a11_duration(duration, fmt, s)), ("A12", a12_brand(d, texts, cap, tr)), ("A13", a13_pauses(s, timeline, silences, duration)),
           ("A14", a14_first_idea(s, timeline, series, spans)), ("A15", a15_change_density(timeline, series)),
           ("A16", a16_diagram_fill(timeline, series, hero, ln)), ("A17", a17_persistence(timeline, series, duration, s)),
           ("A18", a18_teaching_order(s, fixture, prior)), ("A19", a19_pace(timeline, script=s)), ("A20", a20_silence_share(silences, duration, timeline, fmt, s)), ("A21", a21_energy(s))]
    if fmt not in FORMATS:   # advisory outside Professor Diki shorts (A11 already warns at the script's own target)
        for cid, r in out:
            if r["status"] == "fail": r["status"] = "warn"; r["reasons"].append(f"(advisory: format {fmt} is not enforced)")
    return out



def legacy_checks(a, s, d, ff, qd, fixture, fx_flat, timeline, manifest, add):
    """A1–A10, unchanged."""
    # A1 lint
    bad = []
    for sc in s["scenes"]:
        rc, out = run([NODE, str(LINT), "--level", "1", str(d / sc["file"])])
        if '"ok": true' not in out: bad.append((sc["id"], out[-300:]))
    add("A1", "seek-contract lint level 1", "pass" if not bad else "fail", bad or f"{len(s['scenes'])} scenes ok")
    # A2 cue sheets
    bad = []
    for sc in s["scenes"]:
        rc, out = run([sys.executable, str(VALID), "--production", str(d / "cues" / f"{sc['id']}.cues.json")])
        if rc: bad.append((sc["id"], out[-200:]))
    add("A2", "cue sheets valid (production)", "pass" if not bad else "fail", bad or "all valid")
    # A3 + A4 via DOM at several times per scene
    text_bad = []; zone_items = []; tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        for sc in s["scenes"]:
            sheet = json.loads((d / "cues" / f"{sc['id']}.cues.json").read_text(encoding="utf-8"))
            b, page = L.open_scene(p, d / sc["file"], sheet, fixture)
            times = sorted({0.5, sheet["duration"] / 2, max(0.0, sheet["duration"] - 0.5)} | {min(sheet["duration"], c["at"] + 0.6) for c in sheet["cues"]})
            boxes = {}
            for t in times:
                page.evaluate(f"window.seek({t})")
                items = page.evaluate("""() => Array.from(document.querySelectorAll('[data-fx]')).map(e => ({path: e.dataset.fx, dec: e.dataset.fxDec == null ? null : e.dataset.fxDec, text: e.textContent.trim(), visible: !!(e.offsetWidth || e.offsetHeight || e.getClientRects().length) && getComputedStyle(e).opacity !== '0'}))""")
                for it in items:
                    if "->" in str(it["path"]): continue               # a ChangeValue mid-tween (from->to): no value is at rest
                    exp = fx_flat.get(it["path"])
                    if exp is None: text_bad.append((sc["id"], it["path"], "no such fixture field"))
                    elif not _text_matches(it["text"], exp, it.get("dec")): text_bad.append((sc["id"], it["path"], f"screen '{it['text']}' != fixture '{exp}'"))
                els = page.evaluate("""() => Array.from(document.querySelectorAll('#stage [id]')).filter(e => e.id !== 'stage' && e.id !== 'cv').map(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); const vis = r.width > 0 && r.height > 0 && cs.opacity !== '0' && cs.visibility !== 'hidden' && cs.display !== 'none' && (e.textContent||'').trim().length > 0; return {id: e.id, x: r.left, y: r.top, w: r.width, h: r.height, vis, text: (e.textContent||'').trim().slice(0,40)}; })""")
                for e in els:
                    if e["vis"]:
                        boxes.setdefault(e["id"], {"id": e["id"], "role": "text", "x": round(e["x"]), "y": round(e["y"]), "w": round(e["w"]), "h": round(e["h"]), "visible": []})["visible"].append([round(t, 2), round(t + 0.1, 2)])
            b.close()
            zone_items.append({"scene": sc["id"], "elements": list(boxes.values())})
    add("A3", "on-screen science text equals fixture", "pass" if not text_bad else "fail", text_bad[:20] or "every [data-fx] element matches")
    safe_bad = []
    for z in zone_items:
        el = {"canvas": {"width": 1080, "height": 1920}, "elements": z["elements"]}
        pth = qd / f"elements_{z['scene']}.json"; pth.write_text(json.dumps(el), encoding="utf-8")
        rc, out = run([sys.executable, str(SAFE), "--tokens", str(TOKENS), "--boxes", str(pth), "--out", str(qd / f"safe_{z['scene']}.json")])
        try:
            rep = json.loads((qd / f"safe_{z['scene']}.json").read_text()); fails = [f for f in rep.get("findings", rep.get("issues", [])) if str(f.get("severity", f.get("level", ""))).lower() in ("critical", "major", "fail", "error")]
            if fails: safe_bad.append((z["scene"], fails[:5]))
        except Exception as e:
            safe_bad.append((z["scene"], f"checker output unreadable: {out[-200:]}"))
    add("A4", "safe zones (text inside zones, side margin)", "pass" if not safe_bad else "fail", safe_bad or "no critical or major finding", "major")
    # A5 flash: luminance per frame from the final MP4
    final = d / "render" / f"{s['video_id']}.mp4"
    rc, out = run([ff, "-loglevel", "info", "-i", str(final), "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"])
    yav = [float(m.group(1)) for m in re.finditer(r"YAVG=([0-9.]+)", out)]
    csv = qd / "luma.csv"; csv.write_text("frame,luminance\n" + "".join(f"{i},{y}\n" for i, y in enumerate(yav)), encoding="utf-8")
    rc, out = run([sys.executable, str(FLASH), "--csv", str(csv), "--fps", str(manifest["fps"]), "--encoding", "srgb8", "--out", str(qd / "flash.json")])
    try:
        fl = json.loads((qd / "flash.json").read_text()); verdict = fl.get("verdict") or fl.get("result") or ("fail" if fl.get("violations") else "pass")
    except Exception:
        fl = {"raw": out[-300:]}; verdict = "unknown"
    add("A5", "flash test (luminance deltas, 3 Hz rule)", "pass" if str(verdict).lower().startswith("pass") or verdict == "ok" else ("warn" if verdict == "unknown" else "fail"), {"frames": len(yav), "verdict": verdict, "summary": {k: v for k, v in fl.items() if k in ("violations", "max_transitions_per_s", "worst_tile", "transitions")}})
    # A6 loudness
    rc, out = run([ff, "-loglevel", "info", "-i", str(final), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"])
    I = re.findall(r"I:\s+(-?[0-9.]+) LUFS", out); TP = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", out)
    I = float(I[-1]) if I else None; TP = float(TP[-1]) if TP else None
    add("A6", "loudness −16 LUFS ±1, true peak ≤ −1 dBTP", "pass" if I is not None and abs(I + 16) <= 1 and TP is not None and TP <= -1.0 else "fail", {"integrated_lufs": I, "true_peak_dbtp": TP}, "major")
    # A7 transcript check: local Whisper small.en on the mastered mix (PD-29, 27 Oct 2026; was ElevenLabs Scribe v2)
    if not a.no_stt:
        try:
            ws = L.stt_words(d / "narration/mix_norm.wav")
            heard = canon(L.heard_tokens([w for w, _, _ in ws]))
            expected = canon([L.norm_word(w) for b in s["beats"] for w in L.words_of(b["text"])])
            import difflib
            sm = difflib.SequenceMatcher(a=expected, b=heard, autojunk=False); ratio = sm.ratio()
            diffs = [(tag, expected[i1:i2], heard[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
            (qd / "transcript.json").write_text(json.dumps({"text": " ".join(w for w, _, _ in ws), "diffs": diffs, "ratio": ratio}, ensure_ascii=False, indent=1), encoding="utf-8")
            add("A7", "transcript matches script (local Whisper)", "pass" if ratio >= 0.97 and not any(t == "replace" and any(ch.isdigit() for ch in "".join(e)) for t, e, h in diffs) else ("warn" if ratio >= 0.93 else "fail"), {"match_ratio": round(ratio, 3), "diffs": diffs[:12]})
        except Exception as e:
            add("A7", "transcript matches script (local Whisper)", "warn", f"STT failed: {e}")
    else:
        add("A7", "transcript matches script (local Whisper)", "skipped", "--no-stt")
    # A8 durations and pacing
    spoken_s = sum(b["audio_s"] for b in timeline["beats"]); words = sum(len(b["words"]) for b in timeline["beats"]); wpm = words / spoken_s * 60 if spoken_s else 0
    think = [b for b in timeline["beats"] if b.get("think_window_s", 0) >= 4]
    v2 = any(b.get("pauses") for b in s["beats"])   # script v2: pauses are judged by purpose in A13, not by a ≥ 4 s window
    add("A8", "pacing 130–155 wpm, total 55–80 s, think window ≥ 4 s present" + (" (v2: think window judged by A13)" if v2 else ""), "pass" if 125 <= wpm <= 160 and 55 <= timeline["total_duration_s"] <= 80 and (think or v2) else "warn", {"wpm": round(wpm), "total_s": timeline["total_duration_s"], "spoken_s": round(spoken_s, 1), "think_windows": [(b["id"], b["think_window_s"]) for b in think]}, "major")
    # A9 manifest
    det = all(x.get("deterministic_rerender", x.get("deterministic_reverse_order", False)) for x in manifest["scenes"]); srcs = all(x["cue_source"] == "injected" and x["fixture_source"] == "injected" for x in manifest["scenes"])
    add("A9", "render: no scene errors, injected sources, re-render determinism", "pass" if manifest["total_errors"] == 0 and srcs and det else ("warn" if manifest["total_errors"] == 0 and srcs else "fail"), {"errors": manifest["total_errors"], "sources_injected": srcs, "deterministic": det, "warnings": sum(len(x["warnings"]) for x in manifest["scenes"])})
    # A10 audio/video alignment: video length must equal the timeline total within one frame (a dropped lead-in shifts every reveal)
    vid_s = len(yav) / manifest["fps"] if yav else None
    add("A10", "video length equals narration timeline (±1 frame)", "pass" if vid_s is not None and abs(vid_s - timeline["total_duration_s"]) <= 1.0 / manifest["fps"] + 1e-6 else "fail", {"video_s": round(vid_s, 3) if vid_s else None, "timeline_s": timeline["total_duration_s"], "first_scene_start": timeline["scenes"][0]["start"]})


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("script"); ap.add_argument("--no-stt", action="store_true")
    ap.add_argument("--format", help="threshold set for A11–A21 (default: the script's format); concept_short_60 is enforced")
    ap.add_argument("--only", help="comma list of check ids, or 'new' for A11–A21; other checks are kept from the existing report.json")
    ap.add_argument("--no-dom", action="store_true", help="skip the Playwright DOM samples of A12/A16")
    a = ap.parse_args()
    s = L.load_script(a.script); d = pathlib.Path(s["_dir"]); ff = imageio_ffmpeg.get_ffmpeg_exe(); qd = d / "qa"; qd.mkdir(exist_ok=True)
    fixture = json.loads((d / "fixtures/fixture.json").read_text(encoding="utf-8")); fx_flat = {k: str(v) for k, v in flatten(fixture).items()}
    timeline = json.loads((d / "narration/timeline.json").read_text(encoding="utf-8")); manifest = json.loads((d / "render/render_manifest.json").read_text(encoding="utf-8"))
    fmt = a.format or s.get("format"); only = None
    if a.only:
        only = set(NEW_CHECKS) if a.only == "new" else set(a.only.split(","))
    R = {"video_id": s["video_id"], "checks": []}
    if only and (qd / "report.json").exists():
        R["checks"] = [c for c in json.loads((qd / "report.json").read_text(encoding="utf-8"))["checks"] if c["id"] not in only]
    def add(cid, name, status, detail, severity="critical"):
        R["checks"].append({"id": cid, "name": name, "status": status, "severity": severity, "detail": detail})
    if not only or only & {f"A{i}" for i in range(1, 11)}:
        n0 = len(R["checks"]); legacy_checks(a, s, d, ff, qd, fixture, fx_flat, timeline, manifest, add)
        R["checks"] = R["checks"][:n0] + [c for c in R["checks"][n0:] if not only or c["id"] in only]
    if not only or only & set(NEW_CHECKS):
        for cid, r in run_new_checks(s, d, fmt, ff, dom=not a.no_dom):
            if only and cid not in only: continue
            add(cid, NEW_CHECKS[cid][0], r["status"], {"reasons": r["reasons"], **r["evidence"]}, NEW_CHECKS[cid][1])
    R["checks"].sort(key=lambda c: int(c["id"][1:])); R["format"] = fmt
    R["summary"] = {k: sum(1 for c in R["checks"] if c["status"] == k) for k in ("pass", "warn", "fail", "skipped")}
    (qd / "report.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# QA report: {s['video_id']} ({d.name} tier, format {fmt})", "", "| Check | Status | Detail |", "|---|---|---|"]
    for c in R["checks"]:
        det = c["detail"]
        if isinstance(det, dict) and det.get("reasons"):
            det_s = "; ".join(det["reasons"][:6]) + (f" (+{len(det['reasons']) - 6} more)" if len(det["reasons"]) > 6 else "")
        else:
            det_s = json.dumps(det, ensure_ascii=False)[:300]
        md.append(f"| {c['id']} {c['name']} | **{c['status']}** | {det_s.replace('|', chr(92) + '|')} |")
    (qd / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(R["summary"])); [print(f"  {c['id']} {c['status']:7s} {c['name']}") for c in R["checks"]]


if __name__ == "__main__":
    main()
