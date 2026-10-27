#!/usr/bin/env python3
"""credit_ledger.py - hard credit ledger for MCP generation jobs (stdlib only; JSON file, atomic writes).

Usage:
  python3 credit_ledger.py --ledger L.json init --cap 120 [--unit credits] [--provider higgsfield]
  python3 credit_ledger.py --ledger L.json reserve --job JOBKEY --estimate 4 --estimate-source "model page 2026-10-14"
                                                   [--tool image] [--approval-ref gate/approval.json#sha256]
  python3 credit_ledger.py --ledger L.json submit  --job JOBKEY --provider-job-id ID [--now ISO]
  python3 credit_ledger.py --ledger L.json mark-unknown --job JOBKEY            # result missing after the window
  python3 credit_ledger.py --ledger L.json commit  --job JOBKEY --actual 4 --outcome succeeded|failed
  python3 credit_ledger.py --ledger L.json release --job JOBKEY --reason "gate rejected"   # never-submitted only
  python3 credit_ledger.py --ledger L.json due [--now ISO] [--window-s 60]      # jobs to reconcile, never resubmit
  python3 credit_ledger.py --ledger L.json unfreeze --approver NAME --note TEXT # human only; not authentication
  python3 credit_ledger.py --ledger L.json status
  python3 credit_ledger.py --selftest

States: reserved -> submitted -> (unknown) -> committed | released (reserved only). Open jobs (reserved, submitted,
unknown) count at their estimate; committed jobs at their actual. Exit codes: 0 ok, 1 refused/blocked (JSON on
stdout), 2 usage/IO error, 3 cap would be exceeded, 4 overrun recorded and ledger frozen.
Facts: agent generations always deduct credits [N33]; no native credit cap [N34]; results usually within 60 s of
completion, else check Manage Account -> Usage [N35]. Semantics mirror src/examleaf/budget.py (idempotent reserve,
honest overrun record, then block). Edge cases: #41, #42, #43, #45.
"""
import argparse, json, os, sys, tempfile
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import fcntl  # POSIX advisory lock; absent on Windows
except ImportError:  # pragma: no cover
    fcntl = None

OPEN = ("reserved", "submitted", "unknown")


class Refused(Exception):
    code = 1


class CapExceeded(Refused):
    code = 3


class Overrun(Refused):
    code = 4


def now_iso(s=None):
    return s or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@contextmanager
def locked(path):
    lock = Path(str(path) + ".lock")
    with open(lock, "a") as fh:
        if fcntl:
            fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if fcntl:
                fcntl.flock(fh, fcntl.LOCK_UN)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, data):
    path = Path(path)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=path.name, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)  # atomic on the same filesystem


def exposure(led, exclude=None):
    total = 0.0
    for k, j in led["jobs"].items():
        if k == exclude or j["state"] == "released":
            continue
        total += j["actual"] if j["state"] == "committed" else j["estimate"]
    return round(total, 6)


def _event(job, what, at, **kw):
    job["history"].append({"event": what, "at": at, **kw})


def op_init(path, cap, unit, provider):
    if Path(path).exists():
        raise Refused("ledger exists; refusing to overwrite spend history")
    if cap <= 0:
        raise Refused("cap must be positive: no cap means no generation [N34]")
    write(path, {"schema_version": "1.0", "unit": unit, "provider": provider, "cap": cap,
                 "frozen": False, "freeze_reason": None, "approvals": [], "jobs": {}})
    return {"status": "ok", "cap": cap, "unit": unit}


def op_reserve(led, job, estimate, source, tool, approval_ref, at):
    if not job or len(job) < 8:
        raise Refused("job key must be >= 8 characters (idempotency key)")
    if estimate is None or estimate <= 0 or not source:
        raise Refused("estimate-before-call: a positive estimate and its source are required; "
                      "if the provider cannot estimate, get a separately approved bound - never invent a price")
    if job in led["jobs"]:
        j = led["jobs"][job]
        if j["estimate"] != estimate:
            raise Refused("idempotency key reused with a different estimate")
        return {"status": "noop", "job": job, "state": j["state"]}
    if led["frozen"]:
        raise Refused(f"ledger frozen: {led['freeze_reason']}; a human must unfreeze")
    if exposure(led) + estimate > led["cap"]:
        raise CapExceeded(f"cap {led['cap']} {led['unit']} would be exceeded "
                          f"(exposure {exposure(led)} + estimate {estimate}); ask a human for an overrun approval")
    led["jobs"][job] = {"state": "reserved", "estimate": estimate, "actual": None, "estimate_source": source,
                        "tool": tool, "approval_ref": approval_ref, "provider_job_id": None,
                        "submitted_at": None, "outcome": None, "history": []}
    _event(led["jobs"][job], "reserve", at, estimate=estimate)
    return {"status": "ok", "job": job, "exposure": exposure(led), "cap": led["cap"]}


def _get(led, job):
    if job not in led["jobs"]:
        raise Refused(f"unknown job {job!r}: reserve first")
    return led["jobs"][job]


def op_submit(led, job, pjid, at):
    j = _get(led, job)
    if not pjid:
        raise Refused("provider job id is required: persist it before anything else")
    if j["state"] in ("submitted", "unknown"):
        if j["provider_job_id"] == pjid:
            return {"status": "noop", "job": job}
        raise Refused("job already submitted with a different provider job id: possible duplicate paid call; reconcile")
    if j["state"] != "reserved":
        raise Refused(f"cannot submit from state {j['state']}")
    j.update(state="submitted", provider_job_id=pjid, submitted_at=at)
    _event(j, "submit", at, provider_job_id=pjid)
    return {"status": "ok", "job": job}


def op_mark_unknown(led, job, at):
    j = _get(led, job)
    if j["state"] != "submitted":
        raise Refused(f"only submitted jobs can become unknown (state {j['state']})")
    j["state"] = "unknown"
    _event(j, "unknown", at, note="result missing after window; check Manage Account -> Usage [N35]; do not resubmit")
    return {"status": "ok", "job": job, "next": "reconcile via usage page; never resubmit an unknown job"}


def op_commit(led, job, actual, outcome, at):
    j = _get(led, job)
    if j["state"] not in ("submitted", "unknown"):
        raise Refused(f"commit needs a submitted/unknown job (state {j['state']})")
    if actual is None or actual < 0 or outcome not in ("succeeded", "failed"):
        raise Refused("commit needs --actual >= 0 and --outcome succeeded|failed (failed jobs may still be billed [N33])")
    j.update(state="committed", actual=actual, outcome=outcome)
    _event(j, "commit", at, actual=actual, outcome=outcome)
    res = {"status": "ok", "job": job, "exposure": exposure(led)}
    if actual > j["estimate"]:
        j["estimate_exceeded"] = True
        res["warning"] = f"actual {actual} > estimate {j['estimate']}: re-check the estimate source"
    if exposure(led) > led["cap"]:
        led["frozen"], led["freeze_reason"] = True, f"overrun recorded at {at}: exposure {exposure(led)} > cap {led['cap']}"
        raise Overrun(led["freeze_reason"] + "; production must pause")
    return res


def op_release(led, job, reason, at):
    j = _get(led, job)
    if j["state"] != "reserved":
        raise Refused(f"only never-submitted reservations can be released (state {j['state']}); reconcile instead")
    j["state"] = "released"
    _event(j, "release", at, reason=reason)
    return {"status": "ok", "job": job, "exposure": exposure(led)}


def op_due(led, at, window_s):
    t = datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    due = []
    for k, j in sorted(led["jobs"].items()):
        if j["state"] == "unknown":
            due.append({"job": k, "state": "unknown", "provider_job_id": j["provider_job_id"]})
        elif j["state"] == "submitted":
            sub = datetime.strptime(j["submitted_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if t - sub > timedelta(seconds=window_s):
                due.append({"job": k, "state": "submitted", "provider_job_id": j["provider_job_id"],
                            "waited_s": int((t - sub).total_seconds())})
    return {"status": "ok", "due": due, "rule": "reconcile by provider job id; do not resubmit [N35]"}


def op_unfreeze(led, approver, note, at):
    if not approver or not note:
        raise Refused("unfreeze needs --approver and --note (a recorded human decision)")
    led["approvals"].append({"event": "unfreeze", "approver": approver, "note": note, "at": at,
                             "exposure": exposure(led), "cap": led["cap"],
                             "caveat": "local JSON is not authentication; production uses the review service identity"})
    led["frozen"], led["freeze_reason"] = False, None
    return {"status": "ok", "exposure": exposure(led), "cap": led["cap"]}


def op_status(led):
    by = {}
    for j in led["jobs"].values():
        by[j["state"]] = by.get(j["state"], 0) + 1
    return {"status": "ok", "cap": led["cap"], "unit": led["unit"], "exposure": exposure(led),
            "remaining": round(led["cap"] - exposure(led), 6), "frozen": led["frozen"], "jobs_by_state": by}


def dispatch(a):
    if a.cmd == "init":
        return op_init(a.ledger, a.cap, a.unit, a.provider)
    with locked(a.ledger):
        led = read(a.ledger)
        at = now_iso(getattr(a, "now", None))
        try:
            if a.cmd == "reserve":
                res = op_reserve(led, a.job, a.estimate, a.estimate_source, a.tool, a.approval_ref, at)
            elif a.cmd == "submit":
                res = op_submit(led, a.job, a.provider_job_id, at)
            elif a.cmd == "mark-unknown":
                res = op_mark_unknown(led, a.job, at)
            elif a.cmd == "commit":
                res = op_commit(led, a.job, a.actual, a.outcome, at)
            elif a.cmd == "release":
                res = op_release(led, a.job, a.reason, at)
            elif a.cmd == "unfreeze":
                res = op_unfreeze(led, a.approver, a.note, at)
            elif a.cmd == "due":
                return op_due(led, at, a.window_s)
            else:
                return op_status(led)
        except Overrun:
            write(a.ledger, led)  # record the overrun honestly before refusing further work
            raise
        write(a.ledger, led)
        return res


def parser():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--ledger")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("init")
    p.add_argument("--cap", type=float, required=True)
    p.add_argument("--unit", default="credits")
    p.add_argument("--provider", default="higgsfield")
    p = sub.add_parser("reserve")
    p.add_argument("--job", required=True)
    p.add_argument("--estimate", type=float, required=True)
    p.add_argument("--estimate-source", required=True)
    p.add_argument("--tool")
    p.add_argument("--approval-ref")
    p.add_argument("--now")
    p = sub.add_parser("submit")
    p.add_argument("--job", required=True)
    p.add_argument("--provider-job-id", required=True)
    p.add_argument("--now")
    p = sub.add_parser("mark-unknown")
    p.add_argument("--job", required=True)
    p.add_argument("--now")
    p = sub.add_parser("commit")
    p.add_argument("--job", required=True)
    p.add_argument("--actual", type=float, required=True)
    p.add_argument("--outcome", required=True)
    p.add_argument("--now")
    p = sub.add_parser("release")
    p.add_argument("--job", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--now")
    p = sub.add_parser("due")
    p.add_argument("--now")
    p.add_argument("--window-s", type=int, default=60)
    p = sub.add_parser("unfreeze")
    p.add_argument("--approver", required=True)
    p.add_argument("--note", required=True)
    p.add_argument("--now")
    sub.add_parser("status")
    return ap


def run(argv):
    a = parser().parse_args(argv)
    return dispatch(a)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        L = str(Path(d) / "ledger.json")
        T = "2026-10-14T10:00:00Z"

        def ok(*args):
            return run(["--ledger", L, *args])

        def refused(cls, *args):
            try:
                ok(*args)
            except cls as e:
                return str(e)
            raise AssertionError(f"expected {cls.__name__} for {args}")
        ok("init", "--cap", "10")
        refused(Refused, "init", "--cap", "10")                                   # never overwrite history
        assert ok("reserve", "--job", "job-aaaa-01", "--estimate", "4", "--estimate-source", "s")["status"] == "ok"
        assert ok("reserve", "--job", "job-aaaa-01", "--estimate", "4", "--estimate-source", "s")["status"] == "noop"
        refused(Refused, "reserve", "--job", "job-aaaa-01", "--estimate", "5", "--estimate-source", "s")
        refused(Refused, "reserve", "--job", "short", "--estimate", "1", "--estimate-source", "s")
        refused(Refused, "reserve", "--job", "job-zero-01", "--estimate", "0", "--estimate-source", "s")
        refused(CapExceeded, "reserve", "--job", "job-bbbb-01", "--estimate", "7", "--estimate-source", "s")
        ok("submit", "--job", "job-aaaa-01", "--provider-job-id", "hf-123", "--now", T)
        assert ok("submit", "--job", "job-aaaa-01", "--provider-job-id", "hf-123", "--now", T)["status"] == "noop"
        refused(Refused, "submit", "--job", "job-aaaa-01", "--provider-job-id", "hf-999")   # duplicate paid call
        refused(Refused, "release", "--job", "job-aaaa-01", "--reason", "x")              # submitted: reconcile, not release
        assert ok("due", "--now", "2026-10-14T10:00:30Z")["due"] == []
        assert ok("due", "--now", "2026-10-14T10:01:05Z")["due"][0]["job"] == "job-aaaa-01"
        ok("mark-unknown", "--job", "job-aaaa-01", "--now", "2026-10-14T10:01:10Z")
        ok("commit", "--job", "job-aaaa-01", "--actual", "4", "--outcome", "succeeded")
        ok("reserve", "--job", "job-cccc-01", "--estimate", "6", "--estimate-source", "s")   # 4 + 6 = 10 <= cap
        ok("release", "--job", "job-cccc-01", "--reason", "storyboard gate rejected")
        ok("reserve", "--job", "job-dddd-01", "--estimate", "6", "--estimate-source", "s")
        ok("submit", "--job", "job-dddd-01", "--provider-job-id", "hf-456", "--now", T)
        refused(Overrun, "commit", "--job", "job-dddd-01", "--actual", "8", "--outcome", "failed")  # 12 > 10
        st = ok("status")
        assert st["frozen"] and st["exposure"] == 12.0, st
        refused(Refused, "reserve", "--job", "job-eeee-01", "--estimate", "1", "--estimate-source", "s")  # frozen
        ok("unfreeze", "--approver", "founder", "--note", "accept overrun; raise cap next lesson")
        refused(CapExceeded, "reserve", "--job", "job-eeee-01", "--estimate", "1", "--estimate-source", "s")
        led = read(L)
        assert led["jobs"]["job-dddd-01"]["estimate_exceeded"] and led["approvals"][0]["approver"] == "founder"
    print("credit_ledger selftest OK")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()
    ap = parser()
    a = ap.parse_args(argv)
    if not a.ledger or not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        res = dispatch(a)
    except Refused as e:
        print(json.dumps({"status": "refused", "skill": "examleaf-mcp-orchestrator", "error": str(e)}, indent=2))
        return e.code
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
