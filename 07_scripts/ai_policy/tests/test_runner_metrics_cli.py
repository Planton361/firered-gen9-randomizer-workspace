import json
import math
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy.metrics import summarize
from ai_policy.policies import choose_action
from ai_policy.runner import replay_matches, run_all, run_fixture, twin_mismatches
from ai_policy.schema import load_fixtures
from ai_policy.trace import canonical_trace_line


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_fixtures.json"
CLI = Path(__file__).resolve().parents[1] / "cli.py"


class RunnerMetricsCliTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(FIXTURES)
        cls.by_id = {item["fixture_id"]: item for item in cls.fixtures}

    def test_canonical_replay_is_byte_identical_for_every_fixture(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertTrue(replay_matches(fixture))

    def test_trace_has_required_stable_fields(self):
        trace = run_fixture(self.by_id["equal_two"]).trace
        required = {
            "fixture_id", "schema_version", "policy_config_id", "policy_id",
            "observation_hash", "profile", "information_mode", "legal_action_ids",
            "excluded_action_ids", "hard_floor_reasons", "candidate_contract",
            "selected_action_id", "policy_rng", "coverage_tags",
        }
        self.assertLessEqual(required, trace.keys())
        self.assertEqual(1, trace["policy_rng"]["draw_count"])
        self.assertEqual(canonical_trace_line(trace), canonical_trace_line(dict(reversed(list(trace.items())))))

    def test_trace_rejects_paths_pointers_and_protected_suffixes(self):
        for value in ("/private/place", "0xDEADBEEF", "sample.gba", "save.sav"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                canonical_trace_line({"safe": value})

    def test_uniform_legal_two_way_entropy_and_balance(self):
        fixture = self.by_id["equal_two"]
        counts = Counter(run_fixture(fixture, replicate=index).trace["selected_action_id"]
                         for index in range(1024))
        probabilities = [counts[action] / 1024 for action in ("equal_a", "equal_b")]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.5) <= 0.05 for p in probabilities))

    def test_uniform_legal_four_way_entropy_and_balance(self):
        fixture = self.by_id["equal_four"]
        ids = ("equal_a", "equal_b", "equal_c", "equal_d")
        counts = Counter(run_fixture(fixture, replicate=index).trace["selected_action_id"]
                         for index in range(1024))
        probabilities = [counts[action] / 1024 for action in ids]
        entropy = -sum(p * math.log2(p) for p in probabilities) / 2
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.25) <= 0.05 for p in probabilities))

    def test_ko_first_baseline_chooses_robust_ko_without_rng(self):
        result = run_fixture(self.by_id["ko_vs_accuracy"], policy_id="ko_first_no_switch")
        self.assertEqual("ko_move", result.trace["selected_action_id"])
        self.assertEqual(0, result.trace["policy_rng"]["draw_count"])

    def test_first_legal_baseline_is_deterministic(self):
        result = run_fixture(self.by_id["equal_four"], policy_id="first_legal")
        self.assertEqual("equal_a", result.trace["selected_action_id"])
        self.assertEqual(0, result.trace["policy_rng"]["draw_count"])

    def test_unknown_baseline_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown baseline"):
            run_fixture(self.by_id["equal_two"], policy_id="current_cfru")

    def test_synthetic_metric_summary_has_expected_zero_error_rates(self):
        results = run_all(self.fixtures)
        metrics = summarize(results)
        self.assertEqual(29, metrics["decision_count"])
        self.assertEqual(0, metrics["illegal_action"]["count"])
        self.assertEqual(0, metrics["invalid_no_effect"]["count"])
        self.assertEqual(0, metrics["missed_robust_ko"]["count"])
        self.assertEqual(0, metrics["redundant_status"]["count"])
        self.assertEqual(0, metrics["harmful_repeated_status"]["count"])
        self.assertEqual(1, metrics["harmful_repeated_status"]["opportunities"])
        self.assertEqual(1, metrics["switch_loop_detection_count"])
        self.assertEqual(0, metrics["hidden_information_twin_mismatch_count"])
        self.assertEqual(0, metrics["submitted_action_twin_mismatch_count"])
        self.assertEqual(0, metrics["deterministic_replay_mismatch_count"])

    def test_hidden_twin_comparison_uses_same_policy_seed(self):
        results = run_all(self.fixtures)
        self.assertEqual([], twin_mismatches(results))

    def test_cli_validate_replay_and_summarize(self):
        commands = (
            ["validate"],
            ["replay", "--fixture-id", "equal_two", "--replicate", "7"],
            ["summarize"],
        )
        for arguments in commands:
            with self.subTest(arguments=arguments):
                completed = subprocess.run(
                    [sys.executable, str(CLI), "--fixtures", str(FIXTURES), *arguments],
                    cwd=ROOT, check=True, text=True, capture_output=True,
                )
                self.assertIsInstance(json.loads(completed.stdout), dict)
                self.assertEqual("", completed.stderr)

    def test_cli_run_emits_one_canonical_line_per_fixture(self):
        completed = subprocess.run(
            [sys.executable, str(CLI), "--fixtures", str(FIXTURES), "run",
             "--policy", "first_legal"],
            cwd=ROOT, check=True, capture_output=True,
        )
        lines = completed.stdout.splitlines()
        self.assertEqual(29, len(lines))
        self.assertTrue(all(isinstance(json.loads(line), dict) for line in lines))


if __name__ == "__main__":
    unittest.main()
