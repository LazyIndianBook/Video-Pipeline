#!/usr/bin/env python3
"""Validate an ExamLeaf lesson's structure, not its science or learning efficacy.

Python 3.10+. No third-party packages. Warnings are editorial flags for review;
passing is never academic or publication approval. Times describe a planned cut.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any

REQUIRED_TEXT = ("spoken_text", "visual_direction", "sync_note", "title", "tone")
ACTIVE_TYPES = {"prediction", "guided_pause", "independent_pause", "retrieval_pause"}
ALL_TYPES = ACTIVE_TYPES | {"none", "feedback"}
STAGE_TAG = re.compile(r"\[(?:BEAT|THINK|PAUSE_VIDEO|VOICE|TONE|EMPHASIS|REVEAL|SMILE|LAUGH|SIGH)\b[^\]]*\]", re.I)
FAKE_CONTINGENCY = re.compile(r"\b(?:I heard you (?:say|answer)|I can see (?:that )?you (?:got|wrote)|you have definitely mastered)\b", re.I)


def finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w]+(?:['’][\w]+)?\b", text))


def validate_lesson(data: Any) -> list[dict[str, str]]:
    """Return machine-readable error/warning records; never modify input."""
    issues: list[dict[str, str]] = []

    def add(level: str, code: str, location: str, message: str) -> None:
        issues.append({"level": level, "code": code, "location": location, "message": message})

    if not isinstance(data, dict):
        add("error", "root_type", "root", "Expected a JSON object.")
        return issues
    target = data.get("target_runtime_s")
    if not finite_number(target) or target <= 0:
        add("error", "runtime", "root", "target_runtime_s must be finite and positive.")
    for field in ("title", "audience", "scope", "status", "academic_review", "timing_status"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            add("error", "metadata", field, "Required non-empty text is missing.")
    if not isinstance(data.get("sources"), list) or not data["sources"]:
        add("warning", "sources", "root", "No source records; add approved evidence before review.")
    beats = data.get("beats")
    if not isinstance(beats, list) or not beats:
        add("error", "beats", "root", "Expected at least one beat.")
        return issues
    seen: set[str] = set()
    previous_end = 0.0
    timeline_valid = True
    for index, beat in enumerate(beats):
        loc = f"beats[{index}]"
        if not isinstance(beat, dict):
            add("error", "beat_type", loc, "Expected an object.")
            timeline_valid = False
            continue
        ident = beat.get("id")
        if not isinstance(ident, str) or not ident.strip():
            add("error", "beat_id", loc, "A non-empty ID is required.")
        elif ident in seen:
            add("error", "duplicate_id", loc, f"Duplicate ID: {ident}")
        else:
            seen.add(ident)
        for field in REQUIRED_TEXT:
            if not isinstance(beat.get(field), str) or not beat[field].strip():
                add("error", "beat_text", f"{loc}.{field}", "Required non-empty text is missing.")
        start, end, hold = (beat.get(k) for k in ("start_s", "end_s", "hold_s"))
        valid_times = all(finite_number(v) for v in (start, end, hold))
        if not valid_times or start < 0 or end <= start or hold < 0 or hold >= end - start:
            add("error", "beat_timing", loc, "Require 0 <= start < end and 0 <= hold < duration; all finite.")
            timeline_valid = False
        else:
            if not math.isclose(start, previous_end, abs_tol=1e-6):
                add("error", "noncontiguous", loc, f"Start {start} does not match previous end {previous_end}.")
            previous_end = float(end)
        text = beat.get("spoken_text", "")
        if isinstance(text, str):
            if STAGE_TAG.search(text):
                add("error", "spoken_stage_tag", loc, "Editorial stage direction appears in clean spoken text.")
            if FAKE_CONTINGENCY.search(text):
                add("warning", "fake_contingency", loc, "Potential fabricated awareness of the learner; inspect context.")
            if valid_times and end > start and 0 <= hold < end - start:
                rate = 60 * word_count(text) / (end - start - hold)
                if rate > 170:
                    add("warning", "high_planned_rate", loc, f"Planned active rate {rate:.1f} wpm; audition, do not auto-speed up.")
        interaction = beat.get("interaction")
        if not isinstance(interaction, dict):
            add("error", "interaction", loc, "An interaction object is required, even for type none.")
            continue
        kind = interaction.get("type")
        if kind not in ALL_TYPES:
            add("error", "interaction_type", loc, "Unknown interaction type.")
        if kind in ACTIVE_TYPES:
            for field in ("prompt", "expected_answer"):
                if not isinstance(interaction.get(field), str) or not interaction[field].strip():
                    add("error", "interaction_answer", f"{loc}.interaction.{field}", "Active task requires prompt and expected answer.")
            if finite_number(hold) and hold < 3:
                add("warning", "short_attempt", loc, "Less than three seconds planned; verify external pause/control.")
    if timeline_valid and finite_number(target) and not math.isclose(previous_end, target, abs_tol=1e-6):
        add("error", "final_runtime", "root", f"Last end {previous_end} differs from target {target}.")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", type=Path)
    parser.add_argument("--json-output", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.lesson.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.exit(2, f"Could not read valid UTF-8 JSON: {exc}\n")
    issues = validate_lesson(data)
    errors = sum(i["level"] == "error" for i in issues)
    warnings = sum(i["level"] == "warning" for i in issues)
    report = {
        "check": "STRUCTURE_ONLY", "errors": errors, "warnings": warnings,
        "issues": issues, "academic_approval": False, "audio_timing_measured": False,
    }
    if args.json_output:
        print(json.dumps(report, indent=2))
    else:
        print(f"Structural check: {errors} errors; {warnings} warnings.")
        for issue in issues:
            print(f"{issue['level'].upper()} {issue['code']} {issue['location']}: {issue['message']}")
        print("This is not scientific approval, measured audio timing, or evidence of learning efficacy.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
