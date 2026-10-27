#!/usr/bin/env python3
"""validate_trajectory_fixture.py - check a precomputed trajectory fixture before a three.js replay (stdlib only).

Usage:
  python3 validate_trajectory_fixture.py FIXTURE.json [--duration S] [--fps 30] [--tol 1e-6] [--allow-draft] [--json]
  python3 validate_trajectory_fixture.py --selftest

A seek-pure 3D scene never steps physics in real time; it interpolates fixed-step samples computed and checked
upstream by the science skills. This validator checks: provenance (claim IDs, status), units for every field,
finite numbers, strictly monotonic time, fixed step dt, start at t=0, coverage of the scene duration, and
sampling density vs the render fps. Edge cases #12 (facts only from fixtures), #15 (no wall-clock physics).
Exit: 0 valid (warnings allowed), 1 invalid, 2 usage/IO error.
"""
import argparse, json, math, sys

STATUSES_OK = {"machine_checked", "expert_approved"}


def rows(fx):
    fields = fx.get("fields")
    s = fx.get("samples") or []
    if s and isinstance(s[0], dict):
        fields = fields or list(s[0].keys())
        return fields, [[r.get(f) for f in fields] for r in s]
    return fields, s


def validate(fx, duration=None, fps=None, tol=1e-6, allow_draft=False):
    E, W = [], []
    for k in ("fixture_id", "units", "samples"):
        if k not in fx:
            E.append(f"missing {k}")
    if E:
        return E, W, {}
    if not fx.get("source_claim_ids"):
        E.append("source_claim_ids empty: on-screen motion must trace to approved claims (#12)")
    st = fx.get("status")
    if st not in STATUSES_OK and not (allow_draft and st == "draft"):
        E.append(f"status '{st}' not usable; need machine_checked or expert_approved")
    if st == "machine_checked":
        W.append("status machine_checked: expert approval still required before release")
    fields, data = rows(fx)
    if not fields or "t" not in fields:
        E.append("fields must include 't'")
        return E, W, {}
    units = fx["units"]
    for f in fields:
        u = units.get(f)
        if not isinstance(u, str) or not u.strip():
            E.append(f"unit missing for field '{f}'")
    if units.get("t") != "s":
        E.append("time unit must be 's' (cue sheet and seek(t) use seconds)")
    if len(data) < 2:
        E.append("need at least 2 samples")
        return E, W, {}
    ti = fields.index("t")
    bad = 0
    for i, r in enumerate(data):
        if not isinstance(r, list) or len(r) != len(fields):
            E.append(f"sample {i}: expected {len(fields)} values")
            bad += 1
        elif not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in r):
            E.append(f"sample {i}: non-numeric or non-finite value")
            bad += 1
        if bad >= 5:
            E.append("too many bad samples; stopping")
            return E, W, {}
    if E:
        return E, W, {}
    ts = [r[ti] for r in data]
    dt = fx.get("dt", fx.get("dt_s"))
    if not isinstance(dt, (int, float)) or dt <= 0:
        E.append("dt (fixed sample step, seconds) must be a positive number")
        return E, W, {}
    if abs(ts[0]) > tol:
        E.append(f"first sample t={ts[0]} must be 0 (scene-relative time)")
    worst = 0.0
    for i in range(1, len(ts)):
        d = ts[i] - ts[i - 1]
        if d <= 0:
            E.append(f"time not strictly increasing at sample {i} ({ts[i - 1]} -> {ts[i]})")
            break
        worst = max(worst, abs(d - dt))
    if worst > tol * max(1.0, dt) + 1e-12 and not any("strictly" in e for e in E):
        E.append(f"variable step: max |dt_i - dt| = {worst:.3g} s > tol; resample to a fixed step upstream")
    span = ts[-1]
    if duration is not None and span + tol < duration:
        E.append(f"samples end at {span} s < scene duration {duration} s; replay would extrapolate")
    if fps:
        if dt > 1.0 / fps + 1e-12:
            W.append(f"dt {dt} s coarser than one frame (1/{fps} s); interpolation may hide motion detail")
    integ = fx.get("integrator") or {}
    if not integ.get("method"):
        W.append("integrator.method not recorded (analytic, RK4, ...); provenance incomplete")
    info = {"samples": len(ts), "dt": dt, "span_s": span, "fields": fields}
    return E, W, info


def selftest():
    g, v0, ang = 9.8, 10.0, math.radians(30)
    dt = 1 / 120
    samples = [[round(i * dt, 9), round(v0 * math.cos(ang) * i * dt, 9),
                round(v0 * math.sin(ang) * i * dt - 0.5 * g * (i * dt) ** 2, 9), 0.0] for i in range(122)]
    good = {"schema_version": "1.0", "fixture_id": "phy-11-05-projectile-01", "kind": "trajectory",
            "source_claim_ids": ["claim-projectile-eq"], "status": "expert_approved",
            "integrator": {"method": "analytic"}, "dt": dt, "fields": ["t", "x", "y", "z"],
            "units": {"t": "s", "x": "m", "y": "m", "z": "m"}, "samples": samples}
    e, w, info = validate(good, duration=1.0, fps=30)
    assert not e and not w and info["samples"] == 122, (e, w)
    objs = dict(good, samples=[dict(zip(good["fields"], r)) for r in samples], fields=None)
    assert not validate(objs, duration=1.0)[0], "object-form samples"
    def bad(mut, *a, **k):
        d = json.loads(json.dumps(good)); mut(d); return validate(d, *a, **k)[0]
    assert bad(lambda d: d["samples"].__setitem__(5, [d["samples"][3][0]] + d["samples"][5][1:]))       # non-monotonic
    assert bad(lambda d: d["samples"].__setitem__(5, [d["samples"][5][0] + 0.002] + d["samples"][5][1:]))  # variable step
    assert bad(lambda d: d["units"].pop("y"))
    assert bad(lambda d: d["units"].update(t="ms"))
    assert bad(lambda d: d["samples"][7].__setitem__(2, "NaN"))
    assert bad(lambda d: d.update(source_claim_ids=[]))
    assert bad(lambda d: d.update(status="draft"))
    assert not bad(lambda d: d.update(status="draft"), allow_draft=True)
    assert bad(lambda d: None, duration=2.0)                                                     # coverage
    assert bad(lambda d: d["samples"].__setitem__(0, [0.5] + d["samples"][0][1:]))
    coarse = dict(good, dt=0.1, samples=[[round(i * 0.1, 9), 0.0, 0.0, 0.0] for i in range(11)])
    assert any("coarser" in x for x in validate(coarse, duration=1.0, fps=30)[1])
    print(json.dumps({"selftest": "pass", "script": "validate_trajectory_fixture.py"}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate a fixed-step trajectory fixture")
    ap.add_argument("fixture", nargs="?")
    ap.add_argument("--duration", type=float); ap.add_argument("--fps", type=float)
    ap.add_argument("--tol", type=float, default=1e-6); ap.add_argument("--allow-draft", action="store_true")
    ap.add_argument("--json", action="store_true"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.fixture:
        ap.error("FIXTURE.json required")
    try:
        fx = json.load(open(a.fixture, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        print(json.dumps({"status": "error", "error": str(ex)}))
        return 2
    e, w, info = validate(fx, a.duration, a.fps, a.tol, a.allow_draft)
    print(json.dumps({"valid": not e, "errors": e, "warnings": w, "info": info}, indent=2))
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main())
