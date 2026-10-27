#!/usr/bin/env python3
"""effort_policy.py - map an animation task to model + explicit effort + caps; refuse ultracode; log the run.

Usage:
  python3 effort_policy.py plan --task scene_code_2d --job J --scene S --round 1 --pins model_pins.json \
        --caps budget_caps.json --mode production [--est-prompt-tokens N] [--est-output-tokens N] \
        [--lesson-tokens-used N] [--effort max --justification "..."] [--out run_config.json] [--log runs.jsonl]
  python3 effort_policy.py record --run-id R --log runs.jsonl --caps budget_caps.json --task T \
        --tokens-in N --tokens-out N [--cache-read N] [--cache-write N] --effective-effort high --status ok \
        [--lesson-tokens-used N]
  python3 effort_policy.py --selftest

Exit codes: 0 ok, 1 refused (blocker JSON on stdout), 2 usage/IO error.
Policy source: report 3.4 table [Recommendation]. Facts: Opus/Sonnet/Haiku 5.5 default to medium [N22]; unsupported
levels fall back to the highest supported level at or below [N23]; ultracode only via `claude --effort ultracode`
[N24] and never via effortLevel / CLAUDE_CODE_EFFORT_LEVEL [N25]; thinking cannot be disabled on 5.5 or Fable [N26];
aliases resolve differently off the Anthropic API, and Haiku 5.5 prompts >100K tokens cost more [N28];
1M context / 128K output "as of" the tutorial, recheck [N73]. Edge cases: #1-#6, #58, #60, #61.

Task families (15 Oct 2026, audit "Effort and ultracode conflicts"; AD-41 in 02_documentation/14; section 13 D-16 and
section 5.8): "strong" = the tasks below governed by AD-02/AD-11/AD-24 (explicit high, 3 authoring loops). "kit_cascade" =
cheap-model slot-fill through the production Kit, with its own caps (tier 1 Haiku 1+2 repairs, k<=3; tier 1b Haiku
xhigh 1; tier 2 Sonnet medium 2; tier 3 Opus medium/high 2; lesson circuit breaker at 20% escalated). Haiku may author
scene code ONLY in kit_cascade. ultracode is refused in every family and mode; there is deliberately NO attended,
probe or founder exception in this code (the section 13 S5 "Ultra" probe is not a policy exception here).
"""
import argparse, hashlib, json, sys, tempfile
from pathlib import Path

LEVELS = ["low", "medium", "high", "xhigh", "max"]
POLICY = {  # task -> (model alias, effort, report 3.4 row)
    "brief_text":         ("sonnet", "medium", "Brief and storyboard text, prompt assembly"),
    "storyboard_text":    ("sonnet", "medium", "Brief and storyboard text, prompt assembly"),
    "prompt_assembly":    ("sonnet", "medium", "Brief and storyboard text, prompt assembly"),
    "scene_code_2d":      ("opus", "high", "Scene code: 2D motion, kinetic type, collage"),
    "scene_code_complex": ("opus", "xhigh", "Complex three.js, physics replay, intricate choreography"),
    "render_debug":       ("opus", "high", "Debugging a render failure (give logs + failing frame time)"),
    "batch_clerical":     ("haiku", "low", "Batch re-renders, captions, file ops (Sonnet/Haiku low-medium)"),
    # kit_cascade family (13 STRATEGY section 5.8 / D-16): slot-fill into Kit archetype templates, verifiers decide
    "kit_route":          ("haiku", "low", "Kit: route beat -> archetype (strict enum, token-only)"),
    "kit_fill":           ("haiku", "medium", "Kit tier 1: Haiku slot-fill + repairs"),
    "kit_fill_xhigh":     ("haiku", "xhigh", "Kit tier 1b: Haiku per-message xhigh"),
    "kit_escalate_sonnet": ("sonnet", "medium", "Kit tier 2: Sonnet escalation"),
    "kit_escalate_opus":  ("opus", "medium", "Kit tier 3: Opus escalation (medium, then high)"),
}
# kit_cascade caps: max attempts per scene per tier (round cap), max k (best-of), USD ceiling per scene [Recommendation]
KIT = {"kit_route": (1, 1, None), "kit_fill": (3, 3, 0.02), "kit_fill_xhigh": (1, 1, 0.02),
       "kit_escalate_sonnet": (2, 1, 0.25), "kit_escalate_opus": (2, 1, 0.60)}
FAMILY = {t: ("kit_cascade" if t in KIT else "strong") for t in POLICY}
AUTHORING = {"scene_code_2d", "scene_code_complex", "render_debug", "kit_fill", "kit_fill_xhigh",
             "kit_escalate_sonnet", "kit_escalate_opus"}
KIT_ESCALATION_BREAKER = 0.20   # 13 section 5.8: >20% of a lesson's scenes past tier 1 -> stop, Opus-low via the Kit
KIT_TOKEN_GUARD = 60_000        # 13 section 2.1 step 5: prompt < 60K; never > 100K on Haiku
AUTHORING_LOOPS = 3      # report 3.4 "for example 3 fix loops per scene"; section AD-11
REPAIR_ATTEMPTS = 2      # VE library rule: at most two repair attempts after an automated failure
HAIKU_LONG_PROMPT = 100_000          # [N28]
V1_LOW_TOKENS, V1_MAX_TOKENS = 78_000, 625_000   # [V1] whole 79 s video from scratch, low vs max
OUTPUT_LIMIT_ASSUMED = 128_000       # [N73] recheck the model catalog


class Refused(Exception):
    pass


def run_id(job, scene, task, rnd):
    return hashlib.sha256(f"{job}|{scene}|{task}|{rnd}".encode()).hexdigest()[:16]


def effective_level(requested, supported):
    """[N23]: highest supported level at or below the requested one; None when support is unknown."""
    if not supported:
        return None
    ok = [lv for lv in LEVELS[:LEVELS.index(requested) + 1] if lv in supported]
    return ok[-1] if ok else None


def plan(task, job, scene, rnd, pins, caps, mode, effort=None, justification=None,
         est_prompt=None, est_output=None, lesson_used=0, k=1, escalated_fraction=None):
    warns = []
    if task not in POLICY:
        raise Refused(f"unknown task {task!r}; known: {sorted(POLICY)}")
    if effort == "ultracode":   # every family, every mode, any justification: no exception path exists
        raise Refused("#3/#4 ultracode is refused for every ExamLeaf run (multi-agent, separate caches, [V1] >=2.5M tokens "
                      "unfinished); it exists only as `claude --effort ultracode` [N24] and is never a default [N25]")
    alias, level, row = POLICY[task]
    family = FAMILY[task]
    if alias == "haiku" and task in AUTHORING and family != "kit_cascade":
        raise Refused(f"Haiku may author scene code only in the kit_cascade family, not {task!r} (AD-41)")
    if family == "kit_cascade":
        attempts, k_max, _usd = KIT[task]
        if rnd > attempts:
            raise Refused(f"kit_cascade cap: {task} attempt {rnd} > {attempts}; escalate to the next tier (13 section 5.8)")
        if k > k_max:
            raise Refused(f"kit_cascade cap: k={k} > {k_max} for {task}")
        if escalated_fraction is not None and escalated_fraction > KIT_ESCALATION_BREAKER and task != "kit_escalate_opus":
            raise Refused(f"kit circuit breaker: {escalated_fraction:.0%} of the lesson's scenes escalated past tier 1 "
                          f"(> {KIT_ESCALATION_BREAKER:.0%}); run the rest as kit_escalate_opus at low and open a Kit defect")
        if alias == "haiku" and (est_prompt or 0) > KIT_TOKEN_GUARD:
            raise Refused(f"kit token guard: prompt {est_prompt} > {KIT_TOKEN_GUARD} tokens; never send >100K to Haiku [N28]")
        if task == "kit_escalate_opus" and effort == "high" and rnd >= 2 and not justification:
            justification = "tier 3 second attempt (medium, then high)"
    elif k != 1:
        raise Refused("best-of-k sampling is a kit_cascade feature only")
    if effort and effort != level:
        if effort not in LEVELS:
            raise Refused(f"unknown effort {effort!r}; levels {LEVELS}")
        if effort == "max" and (task != "scene_code_complex" or not justification):
            raise Refused("max only for scene_code_complex with a written --justification (report 3.4)")
        if LEVELS.index(effort) > LEVELS.index(level) and effort != "max" and not justification:
            raise Refused(f"raising {task} above {level} needs a written --justification")
        warns.append(f"override: {level} -> {effort} ({justification or 'lowered'})")
        level = effort
    if alias == "haiku" and (est_prompt or 0) > HAIKU_LONG_PROMPT:
        alias = "sonnet"
        warns.append("#61 Haiku 5.5 prompts >100K tokens cost more [N28]: routed to sonnet; prefer splitting the input")
    if family == "strong" and rnd > AUTHORING_LOOPS:
        raise Refused(f"#60 iteration cap: round {rnd} > {AUTHORING_LOOPS} authoring loops; escalate to a human with the rubric")
    pin = (pins or {}).get(alias, {})
    model_id = pin.get("model_id")
    if not model_id or model_id.startswith("<"):
        if mode == "production":
            raise Refused(f"#6 no pinned full model ID for {alias!r} in model_pins.json [N28]; aliases drift across providers")
        warns.append(f"#6 sandbox run on unpinned alias {alias!r}; results are not comparable across providers [N28]")
        model_id = None
    eff = effective_level(level, pin.get("supported_efforts"))
    if eff is None:
        warns.append("#2 effective effort unknown for this model: read it from the session and complete the log [N23]")
    elif eff != level:
        warns.append(f"#2 requested {level} will run as {eff} on this model [N23]")
    cap = (caps or {}).get("per_run_tokens", {}).get(task)
    lesson_cap = (caps or {}).get("per_lesson_tokens")
    alert = float((caps or {}).get("alert_fraction", 0.8))
    if mode == "production" and (cap is None or lesson_cap is None):
        raise Refused("no token cap set for this task or lesson in budget_caps.json: no cap, no run (#42 analogue for tokens)")
    if cap and cap > V1_MAX_TOKENS:
        warns.append(f"per-run cap {cap} exceeds [V1]'s whole-video max run (~{V1_MAX_TOKENS}); is that intended?")
    if lesson_cap and lesson_used + (cap or 0) > lesson_cap:
        raise Refused(f"lesson token budget: used {lesson_used} + run cap {cap} > {lesson_cap}; ask for an approved increase")
    if lesson_cap and lesson_used + (cap or 0) >= alert * lesson_cap:
        warns.append(f"budget alert: this run can take the lesson to >= {int(alert * 100)}% of its token cap")
    if est_output and est_output > OUTPUT_LIMIT_ASSUMED // 2:
        warns.append(f"#58 expected output {est_output} tokens is over half the assumed {OUTPUT_LIMIT_ASSUMED} limit [N73]: split the scene file")
    rid = run_id(job, scene, task, rnd)
    cfg = {"run_id": rid, "job_id": job, "scene_id": scene, "task": task, "family": family, "policy_row": row,
           "model_alias": alias, "model_id": model_id, "effort": level, "effort_effective_expected": eff,
           "ultracode": False,
           "env": {"CLAUDE_CODE_EFFORT_LEVEL": level},   # [N25] env accepts levels, never ultracode
           "cli_args": ["--effort", level],               # flag form shown in [N24]
           "thinking": "always on for 5.5/Fable models; budget includes it [N26]",
           "caps": {"authoring_loops": AUTHORING_LOOPS if family == "strong" else KIT[task][0],
                    "repair_attempts": REPAIR_ATTEMPTS, "round": rnd, "k": k,
                    "usd_ceiling_per_scene": KIT[task][2] if family == "kit_cascade" else None,
                    "per_run_tokens": cap, "per_lesson_tokens": lesson_cap, "alert_fraction": alert},
           "cache_plan": {"stable_prefix_order": ["harness contract", "style guide", "brand tokens", "fixtures (read-only)"],
                          "rule": "one main session per scene batch; keep the prefix byte-identical; no sub-agent fan-out ([V1] caches per agent)"},
           "workspace_rule": "one isolated job folder; do not read sibling folders (#9)",
           "warnings": warns}
    log = {"event": "planned", "run_id": rid, "job_id": job, "scene_id": scene, "task": task, "family": family, "model_alias": alias,
           "model_id": model_id, "effort_requested": level, "effort_effective": eff, "ultracode": False,
           "round": rnd, "per_run_cap": cap, "warnings": warns}
    return cfg, log


def record(rid, task, caps, tokens_in, tokens_out, cache_read, cache_write, effective, status, lesson_used=0):
    if effective == "ultracode":
        raise Refused("#3 a run reported ultracode: stop the batch and audit the launch script")
    total = tokens_in + tokens_out  # tokens_out includes thinking on 5.5 models [N26]
    cap = (caps or {}).get("per_run_tokens", {}).get(task)
    lesson_cap = (caps or {}).get("per_lesson_tokens")
    alert = float((caps or {}).get("alert_fraction", 0.8))
    alerts = []
    if cap and total > cap:
        alerts.append(f"run exceeded its cap: {total} > {cap} tokens; freeze further runs for this scene")
    if lesson_cap and lesson_used + total > lesson_cap:
        alerts.append(f"lesson budget exceeded: {lesson_used + total} > {lesson_cap}")
    elif lesson_cap and lesson_used + total >= alert * lesson_cap:
        alerts.append(f"lesson budget at {round(100 * (lesson_used + total) / lesson_cap)}%")
    if total > V1_LOW_TOKENS:
        alerts.append(f"one run used more than [V1]'s whole low-effort video (~{V1_LOW_TOKENS} tokens): review the brief")
    return {"event": "completed", "run_id": rid, "task": task, "tokens_in": tokens_in, "tokens_out": tokens_out,
            "cache_read": cache_read, "cache_write": cache_write, "tokens_total": total,
            "effort_effective": effective, "status": status, "alerts": alerts}


def append(log_path, entry):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def selftest():
    pins = {"opus": {"model_id": "TEST-PIN-opus", "supported_efforts": LEVELS},
            "sonnet": {"model_id": "TEST-PIN-sonnet", "supported_efforts": ["low", "medium", "high"]},
            "haiku": {"model_id": "<fill from model catalog>"}}
    caps = {"per_run_tokens": {t: 60_000 for t in POLICY}, "per_lesson_tokens": 400_000, "alert_fraction": 0.8}
    cfg, log = plan("scene_code_2d", "job1", "s04", 1, pins, caps, "production")
    assert (cfg["model_id"], cfg["effort"], cfg["env"]["CLAUDE_CODE_EFFORT_LEVEL"]) == ("TEST-PIN-opus", "high", "high")
    assert log["effort_effective"] == "high" and cfg["run_id"] == run_id("job1", "s04", "scene_code_2d", 1)

    def refused(fn, *a, **k):
        try:
            fn(*a, **k)
        except Refused as e:
            return str(e)
        raise AssertionError("expected refusal")
    assert "ultracode" in refused(plan, "scene_code_complex", "j", "s", 1, pins, caps, "sandbox", effort="ultracode")
    assert "max only" in refused(plan, "scene_code_2d", "j", "s", 1, pins, caps, "production", effort="max", justification="x")
    assert "max only" in refused(plan, "scene_code_complex", "j", "s", 1, pins, caps, "production", effort="max")
    cfg, _ = plan("scene_code_complex", "j", "s", 1, pins, caps, "production", effort="max", justification="12-body replay")
    assert cfg["effort"] == "max"
    assert "#60" in refused(plan, "scene_code_2d", "j", "s", 4, pins, caps, "production")
    assert "#6" in refused(plan, "batch_clerical", "j", "s", 1, pins, caps, "production")       # haiku unpinned
    cfg, _ = plan("batch_clerical", "j", "s", 1, pins, caps, "production", est_prompt=150_000)
    assert cfg["model_alias"] == "sonnet" and any("#61" in w for w in cfg["warnings"])
    cfg, _ = plan("brief_text", "j", "s", 1, pins, caps, "production", effort="xhigh", justification="dense brief")
    assert any("will run as high" in w for w in cfg["warnings"]), cfg["warnings"]          # [N23] fallback
    assert "no cap" in refused(plan, "scene_code_2d", "j", "s", 1, pins, {}, "production")
    assert "lesson token budget" in refused(plan, "scene_code_2d", "j", "s", 1, pins, caps, "production", lesson_used=390_000)
    cfg, _ = plan("scene_code_2d", "j", "s", 1, pins, caps, "production", lesson_used=280_000, est_output=90_000)
    assert any("budget alert" in w for w in cfg["warnings"]) and any("#58" in w for w in cfg["warnings"])
    rec = record("r1", "scene_code_2d", caps, 50_000, 30_000, 40_000, 5_000, "high", "ok", lesson_used=100_000)
    assert any("exceeded its cap" in a for a in rec["alerts"]) and any("[V1]" in a for a in rec["alerts"])
    assert "#3" in refused(record, "r1", "scene_code_2d", caps, 1, 1, 0, 0, "ultracode", "ok")
    # kit_cascade family (15 Oct 2026)
    pins_k = dict(pins, haiku={"model_id": "TEST-PIN-haiku", "supported_efforts": LEVELS})
    cfg, _ = plan("kit_fill", "j", "s", 3, pins_k, caps, "production", k=3)
    assert (cfg["family"], cfg["model_alias"], cfg["effort"], cfg["caps"]["authoring_loops"]) == ("kit_cascade", "haiku", "medium", 3)
    assert "kit_cascade cap" in refused(plan, "kit_fill", "j", "s", 4, pins_k, caps, "production")
    assert "kit_cascade cap" in refused(plan, "kit_fill", "j", "s", 1, pins_k, caps, "production", k=4)
    assert "kit_cascade cap" in refused(plan, "kit_escalate_sonnet", "j", "s", 3, pins_k, caps, "production")
    assert "best-of-k" in refused(plan, "scene_code_2d", "j", "s", 1, pins_k, caps, "production", k=3)
    assert "token guard" in refused(plan, "kit_fill", "j", "s", 1, pins_k, caps, "production", est_prompt=70_000)
    assert "circuit breaker" in refused(plan, "kit_fill", "j", "s", 1, pins_k, caps, "production", escalated_fraction=0.25)
    cfg, _ = plan("kit_escalate_opus", "j", "s", 1, pins_k, caps, "production", effort="low", escalated_fraction=0.25)
    assert cfg["model_alias"] == "opus" and cfg["effort"] == "low"
    cfg, _ = plan("kit_escalate_opus", "j", "s", 2, pins_k, caps, "production", effort="high")
    assert cfg["effort"] == "high"                                    # tier 3: medium, then high
    for t in KIT:                                                     # ultracode: no exception, any family or mode
        for m in ("production", "sandbox"):
            assert "ultracode" in refused(plan, t, "j", "s", 1, pins_k, caps, m, effort="ultracode", justification="attended S5 probe")
    assert all(POLICY[t][0] != "haiku" for t in AUTHORING if FAMILY[t] == "strong")   # Haiku authors only in the Kit
    POLICY["tmp_haiku_author"] = ("haiku", "high", "test"); FAMILY["tmp_haiku_author"] = "strong"; AUTHORING.add("tmp_haiku_author")
    try:
        assert "only in the kit_cascade" in refused(plan, "tmp_haiku_author", "j", "s", 1, pins_k, caps, "sandbox")
    finally:
        POLICY.pop("tmp_haiku_author"); FAMILY.pop("tmp_haiku_author"); AUTHORING.discard("tmp_haiku_author")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "runs.jsonl"
        append(p, log)
        append(p, rec)
        assert len(p.read_text().splitlines()) == 2
    print("effort_policy selftest OK")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("plan")
    p.add_argument("--task", required=True)
    p.add_argument("--job", required=True)
    p.add_argument("--scene", required=True)
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--pins")
    p.add_argument("--caps")
    p.add_argument("--mode", choices=["production", "sandbox"], default="production")
    p.add_argument("--effort")
    p.add_argument("--justification")
    p.add_argument("--est-prompt-tokens", type=int)
    p.add_argument("--est-output-tokens", type=int)
    p.add_argument("--lesson-tokens-used", type=int, default=0)
    p.add_argument("--k", type=int, default=1, help="best-of-k (kit_cascade only)")
    p.add_argument("--escalated-fraction", type=float, help="share of the lesson's scenes past Kit tier 1")
    p.add_argument("--out")
    p.add_argument("--log")
    r = sub.add_parser("record")
    r.add_argument("--run-id", required=True)
    r.add_argument("--task", required=True)
    r.add_argument("--caps")
    r.add_argument("--tokens-in", type=int, required=True)
    r.add_argument("--tokens-out", type=int, required=True)
    r.add_argument("--cache-read", type=int)
    r.add_argument("--cache-write", type=int)
    r.add_argument("--effective-effort", required=True)
    r.add_argument("--status", required=True)
    r.add_argument("--lesson-tokens-used", type=int, default=0)
    r.add_argument("--log", required=True)
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_usage(sys.stderr)
        return 2
    try:
        rd = lambda x: json.loads(Path(x).read_text(encoding="utf-8")) if x else None  # noqa: E731
        if a.cmd == "plan":
            cfg, log = plan(a.task, a.job, a.scene, a.round, rd(a.pins), rd(a.caps), a.mode, a.effort, a.justification,
                            a.est_prompt_tokens, a.est_output_tokens, a.lesson_tokens_used, a.k, a.escalated_fraction)
            if a.out:
                Path(a.out).write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            if a.log:
                append(a.log, log)
            print(json.dumps(cfg, indent=2))
        else:
            rec = record(a.run_id, a.task, rd(a.caps), a.tokens_in, a.tokens_out, a.cache_read, a.cache_write,
                         a.effective_effort, a.status, a.lesson_tokens_used)
            append(a.log, rec)
            print(json.dumps(rec, indent=2))
            if rec["alerts"]:
                return 1 if any("exceeded" in x for x in rec["alerts"]) else 0
    except Refused as e:
        print(json.dumps({"status": "refused", "skill": "examleaf-effort-governor", "error": str(e)}, indent=2))
        return 1
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
