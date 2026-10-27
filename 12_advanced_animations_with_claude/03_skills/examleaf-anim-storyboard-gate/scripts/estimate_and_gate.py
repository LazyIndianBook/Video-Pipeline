#!/usr/bin/env python3
"""estimate_and_gate.py - storyboard-gate estimate, beats, approval stub and approval check (stdlib only).

Usage:
  python3 estimate_and_gate.py --scenes segment_scenes.json --out-dir jobs/<segment>/storyboard [--grid grid.png]
  python3 estimate_and_gate.py --verify-approval jobs/<segment>/storyboard/approval_record.json \
          --out-dir jobs/<segment>/storyboard [--grid grid.png] --style-file STYLE.md --fixtures-dir FIXTURES/ \
          [--hero hero.png]
  python3 estimate_and_gate.py --selftest

Writes estimate.json, beats.json and approval_record.json (every approver approved=false). Nothing downstream may run
until --verify-approval exits 0: BOTH roles approved (founder = cost, academic_lead = science fit; two different
identities) AND every bound hash (estimate, beats, grid, script, fixtures, style, hero) still matches the files.
15 Oct 2026 (audit M10, RD-46): this check runs in the RUNNER, not the agent. It proves roles and hashes only; the
runner must also confirm each approver identity and the signature with the authenticated RD-17 approval service
(storyboard/** is Edit-denied to the agent, so a forged local record is a policy breach, not a pass).
No prices are built in: credits_per_image must come from the operator's verified provider config.
Edge cases: #41 estimate before every call, #42 pipeline-enforced cap, #45 no premium video / plan balance,
#47 mandatory gate, #48 hero reference image. Exit: 0 ok/approved, 1 blocked/over cap/not approved, 2 IO error.
"""
import argparse, hashlib, json, math, os, re, sys, tempfile

GRID = 9  # 3x3 panels per grid ([V4-MP])
ROLES = {"founder": "cost (estimate, caps, credits)", "academic_lead": "science fit with the approved script and fixtures"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
NO_HERO = "not_applicable"
SERVICE_NOTE = ("NOT checked here: the runner must verify each approver identity and the signature against the "
                "authenticated RD-17 approval service; a local JSON record alone never authorises a paid step")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def bundle_hash(hashes):
    return hashlib.sha256("\n".join(f"{k}:{v}" for k, v in sorted(hashes.items())).encode()).hexdigest()


def estimate(req):
    blockers, warns, rows = [], [], []
    caps = req.get("caps") or {}
    price = (req.get("pricing") or {}).get("credits_per_image")
    repairs = int(req.get("max_repair_attempts", 2))
    if repairs > 2:
        blockers.append("max_repair_attempts > 2 is not allowed (library rule: at most two repair attempts)")
    tok_defaults = req.get("token_defaults_by_effort") or {}
    gen_total = 0
    hig_any = False
    for sc in req.get("scenes") or []:
        sid = sc.get("scene_id", "?")
        if sc.get("video_generation"):
            blockers.append(f"{sid}: video-model generation requested; avoid premium video models (#45, report 6.1)")
        if sc.get("effort") == "ultracode":
            blockers.append(f"{sid}: ultracode is banned in production ([V1], [N24])")
        tokens = sc.get("est_tokens")
        if tokens is None:
            tokens = tok_defaults.get(sc.get("effort"))
            if tokens is None:
                blockers.append(f"{sid}: no token basis (give est_tokens from examleaf-observability-cost history "
                                f"or token_defaults_by_effort); estimates are never invented")
                tokens = 0
            else:
                warns.append(f"{sid}: token estimate from defaults for effort '{sc.get('effort')}'")
        src = sc.get("thumbnail_source", "code")
        gens = int(sc.get("new_cutouts", 0))
        if src == "higgsfield":
            hig_any = True
            if sc.get("has_character") and not sc.get("hero_ref"):
                blockers.append(f"{sid}: character panels need hero_ref (pass the reference image, #48)")
        elif src != "code":
            blockers.append(f"{sid}: thumbnail_source must be 'code' or 'higgsfield'")
        if gens and sc.get("has_character") and not sc.get("hero_ref"):
            blockers.append(f"{sid}: cutouts with a character need hero_ref (#48)")
        gen_total += gens
        rows.append({"scene_id": sid, "thumbnail_source": src, "beats": int(sc.get("beats", 1)),
                     "tokens_expected": int(tokens), "image_generations_expected": gens})
    beats_total = sum(r["beats"] for r in rows)
    grids = max(1, math.ceil(beats_total / GRID))
    if hig_any:
        gen_total += grids                      # one generated grid image per 3x3 grid
    credits_needed = gen_total > 0
    if credits_needed and not isinstance(price, (int, float)):
        blockers.append("credits_per_image unknown: fill pricing from the verified provider config "
                        "(examleaf-mcp-orchestrator); otherwise use code thumbnails only (#41)")
        price = 0
    price = price or 0
    tok = sum(r["tokens_expected"] for r in rows)
    totals = {"beats": beats_total, "grids": grids, "tokens_expected": tok,
              "tokens_worst_case": tok * (1 + repairs),
              "image_generations_expected": gen_total,
              "credits_expected": round(gen_total * price, 2),
              "credits_worst_case": round(gen_total * price * (1 + repairs), 2),
              "worst_case_basis": f"each unit may be repaired up to {repairs} times at full cost"}
    over = []
    if caps.get("tokens") is not None and totals["tokens_worst_case"] > caps["tokens"]:
        over.append(f"tokens worst case {totals['tokens_worst_case']} > cap {caps['tokens']}")
    if credits_needed:
        if caps.get("credits") is None:
            blockers.append("no credit cap set; Higgsfield has no native cap, the pipeline must set one (#42, [N34])")
        elif totals["credits_worst_case"] > caps["credits"]:
            over.append(f"credits worst case {totals['credits_worst_case']} > job cap {caps['credits']}")
        bal = caps.get("credits_remaining_on_plan")
        if bal is not None and totals["credits_worst_case"] > bal:
            over.append(f"credits worst case {totals['credits_worst_case']} > plan balance {bal} (#45)")
    status = "blocked" if blockers else "over_cap" if over else "awaiting_approval"
    return {"schema_version": "1.0", "skill": "examleaf-anim-storyboard-gate",
            "segment_id": req.get("segment_id"), "lesson_id": req.get("lesson_id"), "style": req.get("style"),
            "pricing_source": (req.get("pricing") or {}).get("source"), "caps": caps, "scenes": rows,
            "totals": totals, "over_cap": over, "blockers": blockers, "warnings": warns, "status": status}


def beats_doc(req):
    panels, n = [], 0
    for sc in req.get("scenes") or []:
        for i in range(int(sc.get("beats", 1))):
            panels.append({"grid": n // GRID + 1, "panel": n % GRID + 1, "scene_id": sc.get("scene_id"),
                           "beat_index": i + 1, "description": (sc.get("beat_descriptions") or [""] * 99)[i],
                           "cue_id": (sc.get("beat_cue_ids") or [None] * 99)[i],
                           "source": sc.get("thumbnail_source", "code"), "hero_ref": sc.get("hero_ref")})
            n += 1
    return {"schema_version": "1.0", "segment_id": req.get("segment_id"), "panels_per_grid": GRID,
            "panel_aspect": "9:16", "panels": panels}


def _hash_inputs(req, base):
    """Fixture, style and hero hashes for the approval record (02_documentation/05 section 5.1). Paths are relative
    to the request file's folder; missing files leave a null that verify() rejects."""
    def h(rel):
        p = os.path.join(base, rel) if rel else None
        return sha256_file(p) if p and os.path.isfile(p) else None
    fixtures = {os.path.basename(f): h(f) for f in req.get("fixtures") or []}
    hero_refs = sorted({sc["hero_ref"] for sc in req.get("scenes") or [] if sc.get("hero_ref")})
    hero = h(hero_refs[0]) if len(hero_refs) == 1 else (NO_HERO if not hero_refs else None)
    return fixtures, h(req.get("style_file")), hero


def write_all(req, out_dir, grid=None, base="."):
    os.makedirs(out_dir, exist_ok=True)
    est, beats = estimate(req), beats_doc(req)
    ep, bp = os.path.join(out_dir, "estimate.json"), os.path.join(out_dir, "beats.json")
    json.dump(est, open(ep, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(beats, open(bp, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    bound = {"estimate.json": sha256_file(ep), "beats.json": sha256_file(bp)}
    if grid:
        bound["grid"] = sha256_file(grid)
    if req.get("script_sha256"):
        bound["script"] = req["script_sha256"]
    fixtures, style_hash, hero_hash = _hash_inputs(req, base)
    bound.update(fixtures=bundle_hash(fixtures) if fixtures and all(fixtures.values()) else None,
                 style=style_hash, hero=hero_hash)
    rec = {"schema_version": "1.1", "approval_id": None, "gate": "storyboard",
           "segment_id": req.get("segment_id"), "style": req.get("style"),
           "gate_status": est["status"], "script_sha256": req.get("script_sha256"),
           "approvers": [{"role": r, "scope": s, "reviewer_id": None, "approved": False, "reviewed_at": None}
                         for r, s in ROLES.items()],
           "decision_notes": "", "override_reason": None,
           "fixture_hashes": fixtures, "style_hash": style_hash, "hero_hash": hero_hash,
           "bound_sha256": bound, "artifact_sha256": bundle_hash(bound), "signature": None,
           "authentication": "local JSON is not authentication; each approver identity and the signature are verified "
                             "by the runner against the RD-17 approval service, never by the agent"}
    json.dump(rec, open(os.path.join(out_dir, "approval_record.json"), "w", encoding="utf-8"), indent=2)
    return est, rec


def verify(rec_path, out_dir, grid=None, style_file=None, hero_file=None, fixtures_dir=None):
    """Runner-side check of roles and hashes. Identity/signature checks belong to the RD-17 service (SERVICE_NOTE)."""
    rec = json.load(open(rec_path, encoding="utf-8"))
    problems = []
    approvers = {a.get("role"): a for a in rec.get("approvers") or [] if isinstance(a, dict)}
    for role in ROLES:
        a = approvers.get(role)
        if a is None:
            problems.append(f"missing approver role {role!r} (two roles required, RD-46)")
            continue
        if a.get("approved") is not True:
            problems.append(f"{role}: not approved (#47 hard stop)")
        if not a.get("reviewer_id") or len(str(a["reviewer_id"])) < 3:
            problems.append(f"{role}: missing reviewer_id")
        if not a.get("reviewed_at"):
            problems.append(f"{role}: missing reviewed_at")
    ids = [str(approvers[r].get("reviewer_id")) for r in ROLES if r in approvers and approvers[r].get("reviewer_id")]
    if len(ids) == len(ROLES) and len(set(ids)) != len(ids):
        problems.append("founder and academic_lead must be two different identities")
    if rec.get("gate_status") == "over_cap" and not rec.get("override_reason"):
        problems.append("over-cap estimate approved without override_reason")
    if rec.get("gate_status") == "blocked":
        problems.append("estimate was blocked; a blocked estimate cannot be approved")
    bound = rec.get("bound_sha256") or {}
    for name in ("estimate.json", "beats.json"):
        p = os.path.join(out_dir, name)
        if not os.path.isfile(p) or sha256_file(p) != bound.get(name):
            problems.append(f"{name} changed or missing since approval")
    if "grid" in bound and (not grid or sha256_file(grid) != bound["grid"]):
        problems.append("grid image changed or not supplied")
    if rec.get("script_sha256") != bound.get("script") or not HEX64.match(str(bound.get("script"))):
        problems.append("script_sha256 missing or does not match the bound script hash")
    # fixtures, style and hero (02_documentation/05 section 5.1): present, bound, and re-hashed from the files now
    fx = rec.get("fixture_hashes") or {}
    if not fx or not all(HEX64.match(str(v)) for v in fx.values()):
        problems.append("fixture_hashes missing or not sha256")
    elif bound.get("fixtures") != bundle_hash(fx):
        problems.append("fixture_hashes do not match the bound fixtures hash")
    elif not fixtures_dir:
        problems.append("fixtures not supplied for re-hash (--fixtures-dir)")
    else:
        for name, want in sorted(fx.items()):
            p = os.path.join(fixtures_dir, name)
            if not os.path.isfile(p) or sha256_file(p) != want:
                problems.append(f"fixture {name} changed or missing since approval")
    sh = rec.get("style_hash")
    if not HEX64.match(str(sh)) or bound.get("style") != sh:
        problems.append("style_hash missing or not bound")
    elif not style_file or sha256_file(style_file) != sh:
        problems.append("style file changed or not supplied (--style-file)")
    hh = rec.get("hero_hash")
    beats_p = os.path.join(out_dir, "beats.json")
    heroes = os.path.isfile(beats_p) and any(p.get("hero_ref") for p in json.load(open(beats_p, encoding="utf-8")).get("panels", []))
    if bound.get("hero") != hh:
        problems.append("hero_hash not bound")
    elif hh == NO_HERO:
        if heroes:
            problems.append("hero_hash is not_applicable but beats.json has hero_ref panels")
    elif not HEX64.match(str(hh)):
        problems.append("hero_hash missing or not sha256")
    elif not hero_file or sha256_file(hero_file) != hh:
        problems.append("hero reference changed or not supplied (--hero)")
    if bundle_hash(bound) != rec.get("artifact_sha256"):
        problems.append("artifact_sha256 does not match bound hashes")
    return {"approved_and_bound": not problems, "problems": problems, "segment_id": rec.get("segment_id"),
            "roles_checked": sorted(ROLES), "authentication": SERVICE_NOTE}


def selftest():
    base = {"segment_id": "phy-10-03-seg2", "lesson_id": "phy-10-03", "style": "doodle-handdrawn@1.0.0",
            "script_sha256": "a" * 64, "caps": {"tokens": 1_000_000, "credits": 50, "credits_remaining_on_plan": 120},
            "pricing": {"credits_per_image": None, "source": None}, "max_repair_attempts": 2,
            "scenes": [{"scene_id": "s1", "beats": 4, "thumbnail_source": "code", "effort": "high", "est_tokens": 60000},
                       {"scene_id": "s2", "beats": 5, "thumbnail_source": "code", "effort": "high", "est_tokens": 80000}]}
    e = estimate(base)
    assert e["status"] == "awaiting_approval" and e["totals"]["credits_expected"] == 0, e
    assert e["totals"]["tokens_worst_case"] == 420000 and e["totals"]["grids"] == 1
    def mut(fn):
        r = json.loads(json.dumps(base)); fn(r); return estimate(r)
    hig = lambda r: r["scenes"][0].update(thumbnail_source="higgsfield", new_cutouts=3)
    assert mut(hig)["status"] == "blocked"                                   # unknown price
    priced = lambda r: (hig(r), r["pricing"].update(credits_per_image=5, source="operator config v1"))
    e2 = mut(priced)                       # 3 cutouts + 1 grid = 4 images x 5 credits; worst case x3 = 60 > cap 50
    assert e2["status"] == "over_cap" and e2["totals"]["credits_worst_case"] == 60, e2
    assert e2["totals"]["image_generations_expected"] == 4 and e2["totals"]["credits_expected"] == 20
    assert mut(lambda r: (priced(r), r["caps"].update(credits=60)))["status"] == "awaiting_approval"
    assert mut(lambda r: (priced(r), r["caps"].update(credits=30)))["status"] == "over_cap"
    assert mut(lambda r: (priced(r), r["caps"].update(credits=None)))["status"] == "blocked"     # #42
    assert mut(lambda r: (priced(r), r["caps"].update(credits_remaining_on_plan=10)))["status"] == "over_cap"  # #45
    assert mut(lambda r: r["scenes"][0].update(video_generation=True))["status"] == "blocked"
    assert mut(lambda r: (priced(r), r["scenes"][0].update(has_character=True)))["status"] == "blocked"   # #48
    assert mut(lambda r: r["scenes"][0].pop("est_tokens"))["status"] == "blocked"
    assert mut(lambda r: r["scenes"][0].update(effort="ultracode"))["status"] == "blocked"
    big = json.loads(json.dumps(base)); big["scenes"][1]["beats"] = 14
    b = beats_doc(big)
    assert len(b["panels"]) == 18 and b["panels"][9]["grid"] == 2 and b["panels"][9]["panel"] == 1
    with tempfile.TemporaryDirectory() as td:
        grid = os.path.join(td, "grid.png"); open(grid, "wb").write(b"\x89PNG fake grid")
        fxd = os.path.join(td, "fixtures"); os.makedirs(fxd)
        open(os.path.join(fxd, "ohm_iv.json"), "w").write('{"R_ohm": 10}')
        open(os.path.join(td, "style.md"), "w").write("doodle-handdrawn 1.0.0")
        req = dict(base, fixtures=["fixtures/ohm_iv.json"], style_file="style.md")
        out = os.path.join(td, "sb")
        _, rec = write_all(req, out, grid, base=td)
        assert rec["hero_hash"] == "not_applicable" and len(rec["approvers"]) == 2 and rec["style_hash"]
        rp = os.path.join(out, "approval_record.json")
        kw = dict(style_file=os.path.join(td, "style.md"), fixtures_dir=fxd)
        res = verify(rp, out, grid, **kw)
        assert not res["approved_and_bound"] and "RD-17" in res["authentication"]   # stub is not approved (#47)
        def approve(r, role, who):
            next(a for a in r["approvers"] if a["role"] == role).update(
                approved=True, reviewer_id=who, reviewed_at="2026-10-15T18:00:00+05:30")
        approve(rec, "founder", "rev-founder")
        json.dump(rec, open(rp, "w"), indent=2)
        res = verify(rp, out, grid, **kw)                                       # one role is not enough (M10)
        assert not res["approved_and_bound"] and any("academic_lead" in p for p in res["problems"]), res
        approve(rec, "academic_lead", "rev-founder")
        json.dump(rec, open(rp, "w"), indent=2)
        assert any("two different" in p for p in verify(rp, out, grid, **kw)["problems"])   # same person twice
        approve(rec, "academic_lead", "rev-acad-lead")
        json.dump(rec, open(rp, "w"), indent=2)
        assert verify(rp, out, grid, **kw)["approved_and_bound"], verify(rp, out, grid, **kw)
        assert not verify(rp, out, grid)["approved_and_bound"]                 # style/fixtures not re-hashed
        open(os.path.join(fxd, "ohm_iv.json"), "w").write('{"R_ohm": 12}')    # fixture edited after approval
        assert any("fixture ohm_iv.json" in p for p in verify(rp, out, grid, **kw)["problems"])
        open(os.path.join(fxd, "ohm_iv.json"), "w").write('{"R_ohm": 10}')
        legacy = dict(rec); legacy.pop("approvers"); legacy.update(role="production", reviewer_id="x-agent", approved=True)
        json.dump(legacy, open(rp, "w"), indent=2)                            # old single-role record is refused
        assert not verify(rp, out, grid, **kw)["approved_and_bound"]
        json.dump(rec, open(rp, "w"), indent=2)
        open(os.path.join(out, "beats.json"), "a").write(" ")                 # tamper after approval
        assert not verify(rp, out, grid, **kw)["approved_and_bound"]
    print(json.dumps({"selftest": "pass", "script": "estimate_and_gate.py"}))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Storyboard gate: estimate + beats + approval")
    ap.add_argument("--scenes"); ap.add_argument("--out-dir"); ap.add_argument("--grid")
    ap.add_argument("--verify-approval"); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--style-file"); ap.add_argument("--hero"); ap.add_argument("--fixtures-dir")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.verify_approval:
            if not a.out_dir:
                ap.error("--out-dir required with --verify-approval")
            res = verify(a.verify_approval, a.out_dir, a.grid, a.style_file, a.hero, a.fixtures_dir)
            print(json.dumps(res, indent=2))
            return 0 if res["approved_and_bound"] else 1
        if not a.scenes or not a.out_dir:
            ap.error("--scenes and --out-dir are required")
        req = json.load(open(a.scenes, encoding="utf-8"))
        est, _ = write_all(req, a.out_dir, a.grid, base=os.path.dirname(os.path.abspath(a.scenes)))
    except (OSError, ValueError) as ex:
        print(json.dumps({"status": "error", "error": str(ex)}))
        return 2
    print(json.dumps({"status": est["status"], "totals": est["totals"], "over_cap": est["over_cap"],
                      "blockers": est["blockers"], "next": "STOP: human approval required before any paid call, "
                      "voice or asset step (#47)"}, indent=2))
    return 0 if est["status"] == "awaiting_approval" else 1


if __name__ == "__main__":
    sys.exit(main())
