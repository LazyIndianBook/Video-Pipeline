"""Structural checker regression tests. No Claude/Codex evaluations are run."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("examleaf_linter", ROOT / "tools/lint_script.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
BASE = json.loads((ROOT / "examples/sample_lesson.json").read_text(encoding="utf-8"))

class TestLinter(unittest.TestCase):
    def codes(self, value):
        return {i["code"] for i in module.validate_lesson(value)}
    def changed(self):
        return copy.deepcopy(BASE)
    def test_sample_is_structurally_valid(self):
        self.assertEqual(module.validate_lesson(BASE), [])
    def test_wrong_root(self):
        self.assertIn("root_type", self.codes([]))
    def test_gap_is_caught(self):
        d=self.changed(); d["beats"][1]["start_s"] += 1
        self.assertIn("noncontiguous", self.codes(d))
    def test_duplicate_is_caught(self):
        d=self.changed(); d["beats"][1]["id"] = d["beats"][0]["id"]
        self.assertIn("duplicate_id", self.codes(d))
    def test_hold_cannot_fill_entire_beat(self):
        d=self.changed(); d["beats"][0]["hold_s"] = 30
        self.assertIn("beat_timing", self.codes(d))
    def test_stage_direction_is_not_spoken(self):
        d=self.changed(); d["beats"][0]["spoken_text"] += " [THINK: 6]"
        self.assertIn("spoken_stage_tag", self.codes(d))
    def test_active_task_needs_answer_key(self):
        d=self.changed(); d["beats"][0]["interaction"]["expected_answer"] = ""
        self.assertIn("interaction_answer", self.codes(d))
    def test_fake_sensing_is_flagged(self):
        d=self.changed(); d["beats"][0]["spoken_text"] += " I heard you say the answer."
        self.assertIn("fake_contingency", self.codes(d))
    def test_runtime_mismatch(self):
        d=self.changed(); d["target_runtime_s"] = 601
        self.assertIn("final_runtime", self.codes(d))
    def test_nonfinite_time(self):
        d=self.changed(); d["beats"][0]["end_s"] = float("nan")
        self.assertIn("beat_timing", self.codes(d))
    def test_boolean_time_rejected(self):
        d=self.changed(); d["beats"][0]["start_s"] = False
        self.assertIn("beat_timing", self.codes(d))
    def test_checker_does_not_modify_lesson(self):
        d=self.changed(); before=copy.deepcopy(d)
        module.validate_lesson(d); self.assertEqual(d, before)

if __name__ == "__main__":
    unittest.main()
