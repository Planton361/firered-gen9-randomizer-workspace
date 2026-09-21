import copy
import hashlib
import json
import math
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy import STANDARD_SCHEMA_VERSION
from ai_policy.metrics import summarize
from ai_policy.runner import replay_matches, run_all, run_fixture, twin_mismatches
from ai_policy.schema import FixtureError, load_fixtures, validate_standard_fixture
from ai_policy.standard import INT32_MIN, utility


ROOT = Path(__file__).resolve().parents[3]
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures"
V1_FIXTURES = FIXTURE_DIR / "synthetic_fixtures.json"
STANDARD_FIXTURES = FIXTURE_DIR / "standard_fixtures.json"
CLI = Path(__file__).resolve().parents[1] / "cli.py"


class StandardPolicyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(STANDARD_FIXTURES)
        cls.by_id = {item["fixture_id"]: item for item in cls.fixtures}

    def diagnostic(self, fixture_id, action_id, replicate=0):
        result = run_fixture(self.by_id[fixture_id], "standard", replicate)
        return next(
            item for item in result.trace["standard_policy"]["candidate_diagnostics"]
            if item["action_id"] == action_id
        )

    def test_standard_corpus_is_explicit_v2_and_has_mandatory_inventory(self):
        self.assertEqual(30, len(self.fixtures))
        self.assertTrue(all(item["schema_version"] == STANDARD_SCHEMA_VERSION
                            for item in self.fixtures))
        tags = {tag for fixture in self.fixtures for tag in fixture["expected"]["coverage_tags"]}
        required = {
            "robust_ko_vs_strong_utility", "damage_vs_low_marginal_accuracy",
            "useful_first_accuracy_drop", "diminishing_accuracy_drop",
            "repeated_accuracy_family_guard", "useful_string_shot_order_flip",
            "useless_string_shot", "useful_setup_immediate_followup", "useless_setup",
            "useful_recovery", "futile_recovery", "useful_major_status",
            "redundant_major_status", "emergency_switch",
            "non_emergency_tactical_switch_rejected", "entry_ko_switch_rejected",
            "switch_loop_memory", "unique_best", "near_best_inside_epsilon",
            "near_best_exact_epsilon", "near_best_outside_epsilon",
            "standard_two_equal_actions", "standard_four_equal_actions",
            "standard_hidden_information_twin", "standard_submitted_action_twin",
            "all_futile_standard_fallback", "extreme_utility_saturation",
            "forced_replacement_separate",
        }
        self.assertEqual(set(), required - tags)

    def test_every_standard_fixture_obeys_allowed_and_forbidden_oracles(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                result = run_fixture(fixture, "standard")
                selected = result.trace["selected_action_id"]
                self.assertIn(selected, fixture["expected"]["allowed_best_set"])
                self.assertNotIn(selected, fixture["expected"]["forbidden_actions"])
                reasons = set(result.trace["hard_floor_reasons"])
                self.assertLessEqual(set(fixture["expected"]["required_reasons"]), reasons)

    def test_fixed_point_utility_terms_are_exact_integers(self):
        damage = self.diagnostic("standard_damage_vs_low_accuracy", "meaningful_damage")
        self.assertEqual(37, damage["utility_total"])
        self.assertEqual(37, damage["utility_terms"]["hp_delta_term"])
        recovery = self.diagnostic("standard_recovery_useful", "recover")
        self.assertEqual(45, recovery["utility_total"])
        self.assertEqual(50, recovery["utility_terms"]["hp_delta_term"])
        for fixture in self.fixtures:
            for action in fixture["candidates"]:
                for field in (
                        "net_faints", "opponent_hp_fraction_lost", "own_hp_fraction_lost",
                        "immediate_future_gain", "entry_cost", "repeat_cost",
                        "uncertainty_cost"):
                    self.assertIs(type(action[field]), int)

    def test_extreme_utility_saturates_and_out_of_bounds_fail_closed(self):
        extreme = self.diagnostic("standard_extreme_saturation", "extreme_cost")
        self.assertEqual(INT32_MIN, extreme["utility_total"])
        self.assertTrue(extreme["utility_terms"]["saturated"])
        for field, value in (("immediate_future_gain", 41), ("entry_cost", 2**31)):
            fixture = copy.deepcopy(self.by_id["standard_extreme_saturation"])
            fixture["candidates"][0][field] = value
            with self.subTest(field=field), self.assertRaises(FixtureError):
                validate_standard_fixture(fixture)
        action = copy.deepcopy(
            self.by_id["standard_extreme_saturation"]["candidates"][0])
        action["opponent_hp_fraction_lost"] = 1.0
        with self.assertRaisesRegex(ValueError, "must be an integer"):
            utility(action)

    def test_robust_ko_and_floor_exclusions_cannot_be_restored(self):
        result = run_fixture(self.by_id["standard_robust_ko_vs_utility"], "standard")
        self.assertEqual("ko_move", result.trace["selected_action_id"])
        status = self.diagnostic("standard_robust_ko_vs_utility", "strong_accuracy_drop")
        self.assertFalse(status["standard_eligible"])
        self.assertFalse(status["near_best"])
        self.assertIn("ROBUST_KO_DOMINATES", status["admission_reasons"])

    def test_status_setup_and_recovery_use_only_certified_marginal_value(self):
        expected = {
            "standard_accuracy_first_useful": "sand_attack",
            "standard_accuracy_diminishing": "damage",
            "standard_accuracy_repeat_guard": "damage",
            "standard_string_shot_flip": "string_shot",
            "standard_string_shot_useless": "damage",
            "standard_setup_useful": "setup",
            "standard_setup_useless": "damage",
            "standard_recovery_useful": "recover",
            "standard_recovery_futile": "damage",
            "standard_major_status_useful": "useful_status",
            "standard_major_status_redundant": "damage",
        }
        for fixture_id, action_id in expected.items():
            with self.subTest(fixture=fixture_id):
                self.assertEqual(
                    action_id,
                    run_fixture(self.by_id[fixture_id], "standard").trace["selected_action_id"],
                )

    def test_standard_switch_admission_is_emergency_only_and_loop_guarded(self):
        emergency = run_fixture(self.by_id["standard_switch_emergency"], "standard")
        tactical = run_fixture(self.by_id["standard_switch_tactical_rejected"], "standard")
        entry_ko = run_fixture(self.by_id["standard_switch_entry_ko"], "standard")
        loop = run_fixture(self.by_id["standard_switch_loop_guard"], "standard")
        forced = run_fixture(self.by_id["standard_forced_replacement"], "standard")
        self.assertEqual("safe_switch", emergency.trace["selected_action_id"])
        self.assertEqual("damage", tactical.trace["selected_action_id"])
        self.assertEqual("damage", entry_ko.trace["selected_action_id"])
        self.assertEqual("damage", loop.trace["selected_action_id"])
        self.assertEqual("forced_switch", forced.trace["selected_action_id"])
        self.assertIn(
            "STANDARD_NON_EMERGENCY_SWITCH",
            self.diagnostic("standard_switch_tactical_rejected", "tactical_switch")[
                "admission_reasons"],
        )
        self.assertIn(
            "STANDARD_SWITCH_LOOP_GUARD",
            self.diagnostic("standard_switch_loop_guard", "return_switch")[
                "admission_reasons"],
        )
        self.assertIn(
            "STANDARD_FORCED_REPLACEMENT_ADMITTED",
            self.diagnostic("standard_forced_replacement", "forced_switch")[
                "admission_reasons"],
        )

    def test_near_best_boundary_and_rng_draw_contract(self):
        cases = {
            "standard_unique_best": (["best"], 0),
            "standard_near_best_inside": (["best", "inside"], 1),
            "standard_near_best_exact": (["best", "exact_boundary"], 1),
            "standard_near_best_outside": (["best"], 0),
        }
        for fixture_id, (near_best, draws) in cases.items():
            with self.subTest(fixture=fixture_id):
                trace = run_fixture(self.by_id[fixture_id], "standard").trace
                self.assertEqual(near_best, trace["standard_policy"]["near_best_action_ids"])
                self.assertEqual(draws, trace["policy_rng"]["draw_count"])

    def test_standard_two_way_entropy_and_balance(self):
        fixture = self.by_id["standard_equal_two"]
        counts = Counter(run_fixture(fixture, "standard", index).trace["selected_action_id"]
                         for index in range(1024))
        probabilities = [counts[action] / 1024 for action in ("equal_a", "equal_b")]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.5) <= 0.05 for p in probabilities))

    def test_standard_four_way_entropy_and_balance(self):
        fixture = self.by_id["standard_equal_four"]
        ids = ("equal_a", "equal_b", "equal_c", "equal_d")
        counts = Counter(run_fixture(fixture, "standard", index).trace["selected_action_id"]
                         for index in range(1024))
        probabilities = [counts[action] / 1024 for action in ids]
        entropy = -sum(p * math.log2(p) for p in probabilities) / 2
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.25) <= 0.05 for p in probabilities))

    def test_hidden_and_submitted_twins_match_scores_draws_and_actions(self):
        results = run_all(self.fixtures, "standard")
        self.assertEqual([], twin_mismatches(results))
        metrics = summarize(results)
        self.assertEqual(0, metrics["hidden_information_twin_mismatch_count"])
        self.assertEqual(0, metrics["submitted_action_twin_mismatch_count"])

    def test_all_futile_fallback_is_deterministic_and_draw_free(self):
        fixture = self.by_id["standard_all_futile"]
        for replicate in range(20):
            result = run_fixture(fixture, "standard", replicate)
            self.assertEqual("least_cost_futile", result.trace["selected_action_id"])
            self.assertEqual(0, result.trace["policy_rng"]["draw_count"])
            self.assertIn("NO_PRODUCTIVE_ACTION", result.trace["hard_floor_reasons"])

    def test_standard_trace_has_complete_deterministic_diagnostics(self):
        fixture = self.by_id["standard_near_best_exact"]
        result = run_fixture(fixture, "standard", replicate=17)
        self.assertTrue(replay_matches(fixture, "standard", replicate=17))
        standard = result.trace["standard_policy"]
        self.assertEqual(8, standard["epsilon"])
        self.assertEqual(2, len(standard["candidate_diagnostics"]))
        for diagnostic in standard["candidate_diagnostics"]:
            self.assertLessEqual({
                "utility_total", "utility_terms", "admission_reasons", "near_best",
                "selected", "standard_eligible",
            }, diagnostic.keys())
        self.assertEqual(1, result.trace["policy_rng"]["draw_count"])
        self.assertNotEqual(
            result.trace["policy_rng"]["pre_state"],
            result.trace["policy_rng"]["post_state"],
        )

    def test_standard_summary_meets_acceptance_gates(self):
        metrics = summarize(run_all(self.fixtures, "standard"))
        self.assertEqual(30, metrics["decision_count"])
        for key in (
                "illegal_action", "invalid_no_effect", "missed_robust_ko",
                "redundant_status", "harmful_repeated_status",
                "standard_non_emergency_voluntary_switch"):
            self.assertEqual(0, metrics[key]["count"], key)
        self.assertEqual(1.0, metrics["oracle_agreement"]["rate"])
        self.assertEqual(1.0, metrics["near_best_compliance"]["rate"])
        self.assertEqual(0, metrics["utility_regret"]["maximum"])
        self.assertEqual(0, metrics["deterministic_replay_mismatch_count"])
        self.assertEqual(0, metrics["hidden_information_twin_mismatch_count"])
        self.assertEqual(0, metrics["submitted_action_twin_mismatch_count"])

    def test_baselines_are_deterministic_on_standard_corpus(self):
        for policy_id in ("uniform_legal", "ko_first_no_switch", "first_legal"):
            with self.subTest(policy=policy_id):
                left = b"".join(result.line for result in run_all(self.fixtures, policy_id))
                right = b"".join(result.line for result in run_all(self.fixtures, policy_id))
                self.assertEqual(left, right)
                metrics = summarize(run_all(self.fixtures, policy_id))
                self.assertEqual(0, metrics["illegal_action"]["count"])
                self.assertEqual(0, metrics["deterministic_replay_mismatch_count"])

    def test_v1_uniform_baseline_trace_digest_is_unchanged(self):
        stream = b"".join(result.line for result in run_all(load_fixtures(V1_FIXTURES)))
        self.assertEqual(
            "71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7",
            hashlib.sha256(stream).hexdigest(),
        )

    def test_v2_unknown_fields_and_short_actions_fail_closed(self):
        document = json.loads(STANDARD_FIXTURES.read_text(encoding="utf-8"))
        document["fixtures"][0]["unknown"] = True
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(FixtureError, "unknown"):
                load_fixtures(path)
        document = json.loads(STANDARD_FIXTURES.read_text(encoding="utf-8"))
        document["fixtures"][0]["candidates"][0].pop()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(FixtureError, "compact Standard action"):
                load_fixtures(path)

    def test_cli_supports_standard_run_replay_and_summarize(self):
        commands = (
            ["run", "--policy", "standard", "--replicate", "0"],
            ["replay", "--fixture-id", "standard_equal_four", "--policy", "standard",
             "--replicate", "37"],
            ["summarize", "--policy", "standard", "--replicate", "0"],
        )
        for arguments in commands:
            with self.subTest(arguments=arguments):
                completed = subprocess.run(
                    [sys.executable, str(CLI), *arguments],
                    cwd=ROOT, check=True, text=True, capture_output=True,
                )
                self.assertEqual("", completed.stderr)
                lines = completed.stdout.splitlines()
                self.assertEqual(30 if arguments[0] == "run" else 1, len(lines))
                self.assertTrue(all(isinstance(json.loads(line), dict) for line in lines))


if __name__ == "__main__":
    unittest.main()
