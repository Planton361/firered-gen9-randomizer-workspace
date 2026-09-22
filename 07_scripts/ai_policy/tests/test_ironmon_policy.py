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

from ai_policy import IRONMON_SCHEMA_VERSION
from ai_policy.ironmon import ironmon_utility, response_distribution
from ai_policy.metrics import summarize
from ai_policy.observation import project_observation
from ai_policy.runner import RunResult, replay_matches, run_all, run_fixture, twin_mismatches
from ai_policy.schema import FixtureError, load_fixtures, validate_ironmon_fixture
from ai_policy.standard import INT32_MIN


ROOT = Path(__file__).resolve().parents[3]
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures"
V1_FIXTURES = FIXTURE_DIR / "synthetic_fixtures.json"
V2_FIXTURES = FIXTURE_DIR / "standard_fixtures.json"
IRONMON_FIXTURES = FIXTURE_DIR / "ironmon_fixtures.json"
CLI = Path(__file__).resolve().parents[1] / "cli.py"


MANDATORY_TAGS = {
    "immediate_robust_ko_vs_tactical", "supported_2hko", "high_roll_false_ko",
    "two_speed_drops", "two_speed_drops_no_survival", "already_faster",
    "priority_trick_room_counterexample", "setup_3hko_to_2hko",
    "setup_no_matching_attack", "accuracy_repeat_residual_exception",
    "speed_repeat_no_exception", "toxic_residual_line",
    "seed_yawn_duplicate_rejection", "recovery_residual_survival_race",
    "futile_recovery", "choice_encore_safe_switch", "trapped_lock_no_switch",
    "emergency_switch", "switch_advantage_11", "switch_advantage_12",
    "switch_advantage_19", "switch_advantage_20",
    "deterministic_switch_admission", "entry_ko_switch_rejection",
    "revealed_absorber_hidden_twin", "forced_revenge_replacement",
    "voluntary_revenge_takes_hit", "preserve_vs_sacrifice",
    "aba_loop_prohibition", "changed_public_threat_exception",
    "consecutive_switch_guard", "productive_regenerator_exception",
    "pointless_regenerator_loop", "revealed_one_plus_unknown",
    "unknown_response_100", "all_revealed_no_unknown",
    "frequency_add_one_smoothing", "zero_speculative_switch_prior",
    "submitted_action_twin", "hidden_state_twin", "hidden_move_twin",
    "hidden_item_twin", "hidden_ability_twin", "hidden_stats_twin",
    "hidden_bench_twin", "future_rng_twin",
    "public_reveal_transition", "epsilon_4_boundaries", "equal_action_entropy",
    "all_futile_fallback", "unsupported_tactical_unknown",
    "supported_field_protect_pivot", "no_useful_bench", "entry_hazard_cost",
    "residual_combinations", "singleton_zero_draw", "stable_action_id_order",
    "switch_candidate_min_advantage",
}


class IronmonPolicyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(IRONMON_FIXTURES)
        cls.by_id = {item["fixture_id"]: item for item in cls.fixtures}

    def result(self, fixture_id, replicate=0):
        return run_fixture(self.by_id[fixture_id], "ironmon_smart", replicate)

    def diagnostic(self, fixture_id, action_id, replicate=0):
        return next(
            row for row in self.result(fixture_id, replicate).trace[
                "ironmon_policy"]["candidate_diagnostics"]
            if row["action_id"] == action_id
        )

    def write_document(self, document, directory):
        path = Path(directory) / "fixtures.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def test_v3_corpus_and_machine_checked_mandatory_inventory(self):
        self.assertEqual(63, len(self.fixtures))
        self.assertTrue(all(fixture["schema_version"] == IRONMON_SCHEMA_VERSION
                            for fixture in self.fixtures))
        tags = {
            tag for fixture in self.fixtures for tag in fixture["expected"]["coverage_tags"]
        }
        self.assertEqual(58, len(tags))
        self.assertEqual(set(), MANDATORY_TAGS - tags)

    def test_every_fixture_obeys_allowed_forbidden_and_reason_oracles(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                result = run_fixture(fixture, "ironmon_smart")
                selected = result.trace["selected_action_id"]
                self.assertIn(selected, fixture["expected"]["allowed_best_set"])
                self.assertNotIn(selected, fixture["expected"]["forbidden_actions"])
                self.assertLessEqual(
                    set(fixture["expected"]["required_reasons"]),
                    set(result.trace["hard_floor_reasons"]),
                )

    def test_response_distribution_unknown_uniform_and_frequency_weights(self):
        expected = {
            "ironmon_response_none_known": [("UNKNOWN", 1)],
            "ironmon_response_one_known": [("TACKLE", 3), ("UNKNOWN", 1)],
            "ironmon_response_all_revealed": [("GROWL", 1), ("TACKLE", 1)],
            "ironmon_response_frequency": [("GROWL", 3), ("TACKLE", 9), ("UNKNOWN", 4)],
        }
        for fixture_id, rows in expected.items():
            with self.subTest(fixture=fixture_id):
                distribution = response_distribution(
                    project_observation(self.by_id[fixture_id]))
                self.assertEqual(rows, [
                    (row["response_id"], row["weight"]) for row in distribution
                ])
                self.assertFalse(any(row["response_id"].startswith("SWITCH")
                                     for row in distribution))

    def test_frequency_weighting_uncertainty_and_future_discount_are_exact(self):
        frequency = self.diagnostic("ironmon_response_frequency", "weighted_line")
        self.assertEqual(56, frequency["expected_before_uncertainty"])
        self.assertEqual(100, frequency["branch_range"])
        self.assertEqual(25, frequency["uncertainty_cost"])
        self.assertEqual(31, frequency["utility_total"])
        speed = self.diagnostic("ironmon_second_speed_drop", "second_speed_drop")
        branch = speed["branch_utilities"][0]
        self.assertEqual(80, branch["future_gain_undiscounted"])
        self.assertEqual(40, branch["discounted_future_gain"])
        self.assertEqual(8, speed["repeat_cost"])

    def test_signed_toward_zero_and_final_int32_saturation(self):
        fixture = copy.deepcopy(self.by_id["ironmon_response_none_known"])
        action = fixture["candidates"][0]
        action["responses"][0].update({
            "net_faints": -1,
            "opponent_hp_fraction_lost": 0,
            "own_hp_fraction_lost": 256,
            "future_gain_undiscounted": -1,
            "entry_cost": 2**31 - 1,
        })
        score = ironmon_utility(
            action, response_distribution(project_observation(fixture)),
            fixture["policy_memory"])
        self.assertEqual(INT32_MIN, score.total)
        self.assertTrue(score.saturated)
        self.assertEqual(0, score.branches[0]["discounted_future_gain"])

    def test_floor_and_supported_tactical_witnesses(self):
        expected = {
            "ironmon_robust_ko": "robust_ko",
            "ironmon_clean_2hko": "clean_2hko",
            "ironmon_high_roll_false_ko": "reliable_damage",
            "ironmon_second_speed_drop": "second_speed_drop",
            "ironmon_speed_plan_no_survival": "damage",
            "ironmon_already_faster": "damage",
            "ironmon_priority_trick_room": "priority_damage",
            "ironmon_setup_3hko_to_2hko": "threshold_setup",
            "ironmon_setup_no_matching_attack": "damage",
            "ironmon_toxic_residual": "toxic_line",
            "ironmon_recovery_residual_race": "recover_and_survive",
            "ironmon_futile_recovery": "damage",
            "ironmon_supported_field_protect_pivot": "supported_protect",
            "ironmon_residual_combination": "burn_seed_line",
        }
        for fixture_id, action_id in expected.items():
            with self.subTest(fixture=fixture_id):
                self.assertEqual(action_id, self.result(fixture_id).trace["selected_action_id"])

    def test_repeat_cost_exception_margin_and_normalized_families(self):
        accepted = self.diagnostic(
            "ironmon_accuracy_repeat_residual", "residual_win_drop")
        self.assertEqual(2, accepted["repeat_count"])
        self.assertEqual(16, accepted["repeat_cost"])
        self.assertEqual("residual_win_line", accepted["repeat_exception_reason"])
        self.assertTrue(accepted["repeat_exception_admitted"])
        self.assertGreaterEqual(accepted["repeat_exception_margin"], 8)
        self.assertTrue(accepted["ironmon_eligible"])
        rejected = self.diagnostic(
            "ironmon_speed_repeat_no_threshold", "repeat_speed_drop")
        self.assertEqual(2, rejected["repeat_count"])
        self.assertEqual(16, rejected["repeat_cost"])
        self.assertIn("HARMFUL_REPEAT", rejected["admission_reasons"])
        self.assertFalse(rejected["ironmon_eligible"])

        insufficient = copy.deepcopy(self.by_id["ironmon_accuracy_repeat_residual"])
        insufficient["candidates"][0]["responses"][0]["future_gain_undiscounted"] = 0
        result = run_fixture(insufficient, "ironmon_smart")
        self.assertEqual("productive_damage", result.trace["selected_action_id"])
        repeat = next(
            row for row in result.trace["ironmon_policy"]["candidate_diagnostics"]
            if row["action_id"] == "residual_win_drop"
        )
        self.assertFalse(repeat["repeat_exception_admitted"])
        self.assertIn("IRONMON_REPEAT_EXCEPTION_REJECTED",
                      repeat["admission_reasons"])

    def test_switch_boundaries_emergency_entry_and_locks(self):
        cases = {
            "ironmon_choice_encore_escape": ("safe_escape", "emergency"),
            "ironmon_trapped_lock": ("locked_attack", "no_eligible_switch"),
            "ironmon_emergency_switch": ("emergency_switch", "emergency"),
            "ironmon_switch_advantage_11": ("stay", "below_12"),
            "ironmon_switch_advantage_20": ("switch_20", "at_least_20"),
            "ironmon_entry_ko_switch": ("stay", "no_eligible_switch"),
            "ironmon_entry_hazard_cost": ("stay", "below_12"),
            "ironmon_no_useful_bench": ("stay", "no_eligible_switch"),
        }
        for fixture_id, (selected, threshold) in cases.items():
            with self.subTest(fixture=fixture_id):
                trace = self.result(fixture_id).trace
                self.assertEqual(selected, trace["selected_action_id"])
                self.assertEqual(
                    threshold,
                    trace["ironmon_policy"]["switch_arbitration"]["threshold_class"],
                )
        for fixture_id, advantage in (
                ("ironmon_switch_advantage_12", 12),
                ("ironmon_switch_advantage_19", 19)):
            arbitration = self.result(fixture_id).trace[
                "ironmon_policy"]["switch_arbitration"]
            self.assertEqual(advantage, arbitration["advantage"])
            self.assertEqual("random_12_19", arbitration["threshold_class"])
            self.assertEqual(1, arbitration["admission_rng"]["draw_count"])

    def test_switch_admission_is_deterministic_balanced_and_exactly_one_draw(self):
        fixture = self.by_id["ironmon_switch_advantage_12"]
        results = [run_fixture(fixture, "ironmon_smart", index) for index in range(1024)]
        admissions = [
            result.trace["ironmon_policy"]["switch_arbitration"]["admission_rng"]
            for result in results
        ]
        counts = Counter(row["admitted"] for row in admissions)
        probabilities = [counts[value] / 1024 for value in (False, True)]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.5) <= 0.05 for p in probabilities))
        self.assertTrue(all(row["draw_count"] == 1 for row in admissions))
        self.assertTrue(all(replay_matches(fixture, "ironmon_smart", index)
                            for index in range(1024)))

    def test_each_switch_candidate_clears_its_own_admission_threshold(self):
        random_cases = {
            "ironmon_switch_candidates_12_8": {
                "switch_12": (12, True), "switch_8": (8, False)},
            "ironmon_switch_candidates_13_9": {
                "switch_13": (13, True), "switch_9": (9, False)},
        }
        for fixture_id, expected in random_cases.items():
            with self.subTest(fixture=fixture_id):
                results = [self.result(fixture_id, index) for index in range(8)]
                admitted = next(
                    result for result in results
                    if result.trace["ironmon_policy"]["switch_arbitration"][
                        "admission_rng"]["admitted"]
                )
                arbitration = admitted.trace["ironmon_policy"]["switch_arbitration"]
                candidates = {
                    row["action_id"]: (row["advantage"], row["threshold_eligible"])
                    for row in arbitration["switch_candidates"]
                }
                self.assertEqual(expected, candidates)
                self.assertEqual("random_12_19", arbitration["threshold_class"])
                self.assertEqual(1, arbitration["admission_rng"]["draw_count"])
                self.assertEqual(
                    [next(action_id for action_id, facts in expected.items() if facts[1])],
                    arbitration["admitted_replacement_pool"],
                )
                self.assertNotIn(
                    next(action_id for action_id, facts in expected.items() if not facts[1]),
                    admitted.trace["ironmon_policy"]["near_best_action_ids"],
                )

        deterministic = self.result("ironmon_switch_candidates_20_16")
        arbitration = deterministic.trace["ironmon_policy"]["switch_arbitration"]
        self.assertEqual("at_least_20", arbitration["threshold_class"])
        self.assertEqual(0, arbitration["admission_rng"]["draw_count"])
        self.assertEqual(
            ["switch_16", "switch_20"], arbitration["admitted_replacement_pool"])
        self.assertEqual(
            ["switch_16", "switch_20"],
            deterministic.trace["ironmon_policy"]["near_best_action_ids"],
        )
        self.assertEqual(
            {"switch_16": (16, True), "switch_20": (20, True)},
            {
                row["action_id"]: (row["advantage"], row["threshold_eligible"])
                for row in arbitration["switch_candidates"]
            },
        )

        emergency = self.result("ironmon_emergency_candidates_dominance")
        arbitration = emergency.trace["ironmon_policy"]["switch_arbitration"]
        self.assertEqual("emergency", arbitration["threshold_class"])
        self.assertEqual(["emergency_dominating"],
                         arbitration["admitted_replacement_pool"])
        self.assertEqual(["emergency_dominating"],
                         emergency.trace["ironmon_policy"]["near_best_action_ids"])
        self.assertEqual("emergency_dominating", emergency.trace["selected_action_id"])
        self.assertEqual(
            {
                "emergency_dominating": (4, True),
                "emergency_nondominating": (0, False),
            },
            {
                row["action_id"]: (row["advantage"], row["threshold_eligible"])
                for row in arbitration["switch_candidates"]
            },
        )

    def test_multi_switch_admission_1024_seed_replay_and_rng_order(self):
        fixture = self.by_id["ironmon_switch_candidates_12_8"]
        results = [run_fixture(fixture, "ironmon_smart", index) for index in range(1024)]
        admissions = [
            result.trace["ironmon_policy"]["switch_arbitration"]["admission_rng"]
            for result in results
        ]
        counts = Counter(row["admitted"] for row in admissions)
        probabilities = [counts[value] / 1024 for value in (False, True)]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        selected = Counter(result.trace["selected_action_id"] for result in results)
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.5) <= 0.05 for p in probabilities))
        self.assertTrue(all(row["draw_count"] == 1 for row in admissions))
        self.assertTrue(all(result.trace["policy_rng"]["draw_count"] == 1
                            for result in results))
        self.assertEqual(0, selected["switch_8"])
        self.assertEqual({"stay", "switch_12"}, set(selected))
        self.assertTrue(all(replay_matches(fixture, "ironmon_smart", index)
                            for index in range(1024)))

    def test_switch_threshold_metric_detects_selected_candidate_own_advantage(self):
        fixture = self.by_id["ironmon_switch_candidates_12_8"]
        results = [run_fixture(fixture, "ironmon_smart", index) for index in range(16)]
        result = next(
            candidate for candidate in results
            if candidate.trace[
                "ironmon_policy"]["switch_arbitration"]["admission_rng"]["admitted"]
        )
        trace = copy.deepcopy(result.trace)
        trace["selected_action_id"] = "switch_8"
        tampered = RunResult(
            result.fixture, result.observation, trace, result.line, result.replicate)
        metric = summarize([tampered])["ironmon_switch_threshold_violation"]
        self.assertEqual(1, metric["count"])
        self.assertEqual(1, metric["below_threshold_selected_count"])
        self.assertEqual(8, metric["below_threshold_selections"][0]["advantage"])

    def test_switch_loop_and_progress_guards(self):
        aba = self.diagnostic("ironmon_aba_prohibited", "return_to_a")
        self.assertEqual(16, aba["loop_cost"])
        self.assertIn("IRONMON_ABA_LOOP_GUARD", aba["admission_reasons"])
        self.assertEqual(
            "return_after_change",
            self.result("ironmon_aba_changed_threat").trace["selected_action_id"],
        )
        consecutive = self.diagnostic("ironmon_consecutive_switch_guard", "third_switch")
        self.assertIn("IRONMON_CONSECUTIVE_SWITCH_GUARD",
                      consecutive["admission_reasons"])
        self.assertEqual(
            "productive_switch",
            self.result("ironmon_productive_regenerator_exception").trace[
                "selected_action_id"],
        )
        pointless = self.diagnostic("ironmon_pointless_regenerator_loop", "regenerator_only")
        self.assertIn("IRONMON_CONSECUTIVE_SWITCH_GUARD", pointless["admission_reasons"])

    def test_forced_switches_do_not_consume_loop_budget_and_aba_spans_three_decisions(self):
        forced_memory = copy.deepcopy(self.by_id["ironmon_consecutive_switch_guard"])
        for decision in forced_memory["policy_memory"]["decisions"]:
            decision["forced"] = True
        result = run_fixture(forced_memory, "ironmon_smart")
        self.assertEqual("third_switch", result.trace["selected_action_id"])
        diagnostic = next(
            row for row in result.trace["ironmon_policy"]["candidate_diagnostics"]
            if row["action_id"] == "third_switch"
        )
        self.assertNotIn("IRONMON_CONSECUTIVE_SWITCH_GUARD",
                         diagnostic["admission_reasons"])

        spaced_aba = copy.deepcopy(self.by_id["ironmon_aba_prohibited"])
        spaced_aba["policy_memory"]["decisions"].append({
            "action_id": "intervening_move", "kind": "move", "effect_family": "damage",
            "success": True, "public_result": "damage", "switch_from": None,
            "switch_to": None, "forced": False,
        })
        spaced = run_fixture(spaced_aba, "ironmon_smart")
        return_row = next(
            row for row in spaced.trace["ironmon_policy"]["candidate_diagnostics"]
            if row["action_id"] == "return_to_a"
        )
        self.assertEqual(16, return_row["loop_cost"])
        self.assertIn("IRONMON_ABA_LOOP_GUARD", return_row["admission_reasons"])

    def test_epsilon_boundary_singleton_and_stable_id_order(self):
        epsilon = self.result("ironmon_epsilon_4").trace
        self.assertEqual(
            ["best", "exact_boundary", "inside"],
            epsilon["ironmon_policy"]["near_best_action_ids"],
        )
        self.assertNotIn("outside", epsilon["ironmon_policy"]["near_best_action_ids"])
        singleton = self.result("ironmon_robust_ko").trace
        self.assertEqual(0, singleton["policy_rng"]["draw_count"])
        equal = self.result("ironmon_equal_four").trace
        self.assertEqual(
            ["equal_a", "equal_b", "equal_c", "equal_d"],
            equal["ironmon_policy"]["near_best_action_ids"],
        )

    def test_equal_action_entropy_balance_and_no_invalid_sampling(self):
        fixture = self.by_id["ironmon_equal_four"]
        ids = ("equal_a", "equal_b", "equal_c", "equal_d")
        counts = Counter(
            run_fixture(fixture, "ironmon_smart", index).trace["selected_action_id"]
            for index in range(1024)
        )
        probabilities = [counts[action_id] / 1024 for action_id in ids]
        entropy = -sum(p * math.log2(p) for p in probabilities) / 2
        self.assertGreaterEqual(entropy, 0.95)
        self.assertTrue(all(abs(p - 0.25) <= 0.05 for p in probabilities))
        self.assertEqual(set(ids), set(counts))

    def test_hidden_submitted_and_future_rng_twins_are_identical(self):
        results = run_all(self.fixtures, "ironmon_smart")
        self.assertEqual([], twin_mismatches(results))
        metrics = summarize(results)
        self.assertEqual(0, metrics["hidden_information_twin_mismatch_count"])
        self.assertEqual(0, metrics["submitted_action_twin_mismatch_count"])
        self.assertEqual(0, metrics["future_rng_twin_mismatch_count"])

    def test_public_reveal_changes_only_publicly_derived_response_and_action(self):
        before = self.result("ironmon_before_reveal").trace
        after = self.result("ironmon_after_reveal").trace
        self.assertNotEqual(before["observation_hash"], after["observation_hash"])
        self.assertNotEqual(
            before["ironmon_policy"]["response_weights"],
            after["ironmon_policy"]["response_weights"],
        )
        self.assertEqual("fallback", before["selected_action_id"])
        self.assertEqual("revealed_plan", after["selected_action_id"])
        self.assertIn("REVEALED_MOVE:TACKLE", after["observation_reasons"])

    def test_all_futile_and_unsupported_effects_are_conservative(self):
        futile = self.result("ironmon_all_futile").trace
        self.assertEqual("least_cost", futile["selected_action_id"])
        self.assertIn("NO_PRODUCTIVE_ACTION", futile["hard_floor_reasons"])
        unsupported = self.result("ironmon_unsupported_tactical").trace
        self.assertEqual("damage", unsupported["selected_action_id"])
        diagnostic = self.diagnostic("ironmon_unsupported_tactical", "unsupported_effect")
        self.assertFalse(diagnostic["ironmon_eligible"])
        self.assertIn("NO_MARGINAL_VALUE", diagnostic["admission_reasons"])

    def test_canonical_replay_and_trace_fields(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                self.assertTrue(replay_matches(fixture, "ironmon_smart", 37))
        trace = self.result("ironmon_switch_advantage_12", 37).trace
        self.assertLessEqual({
            "response_model", "response_weights", "candidate_diagnostics", "switch_arbitration",
            "near_best_action_ids", "epsilon", "best_score",
        }, trace["ironmon_policy"].keys())
        self.assertLessEqual({
            "best_stay", "best_switch", "advantage", "threshold_class",
            "admission_rng", "admitted_tactical_class", "admitted_replacement_pool",
            "selected_candidate_advantage", "switch_candidates",
        }, trace["ironmon_policy"]["switch_arbitration"].keys())

    def test_summary_meets_acceptance_gates(self):
        metrics = summarize(run_all(self.fixtures, "ironmon_smart"))
        self.assertEqual(63, metrics["decision_count"])
        for key in (
                "illegal_action", "invalid_no_effect", "missed_robust_ko",
                "redundant_status", "harmful_repeated_status",
                "ironmon_switch_threshold_violation",
                "ironmon_switch_loop_guard_violation"):
            self.assertEqual(0, metrics[key]["count"], key)
        self.assertEqual(1.0, metrics["allowed_best_compliance"]["rate"])
        self.assertEqual(1.0, metrics["near_best_compliance"]["rate"])
        self.assertLessEqual(metrics["utility_regret"]["maximum"], 4)
        self.assertEqual(19, metrics["fixture_allowed_utility_regret"]["maximum"])
        self.assertEqual(0, metrics["ironmon_response_model"][
            "speculative_switch_weight_sum"])
        self.assertEqual(0, metrics["deterministic_replay_mismatch_count"])

    def test_v1_and_v2_canonical_digests_remain_unchanged(self):
        v1 = b"".join(result.line for result in run_all(load_fixtures(V1_FIXTURES)))
        v2 = b"".join(
            result.line for result in run_all(load_fixtures(V2_FIXTURES), "standard"))
        self.assertEqual(
            "71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7",
            hashlib.sha256(v1).hexdigest(),
        )
        self.assertEqual(
            "227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85",
            hashlib.sha256(v2).hexdigest(),
        )

    def test_v3_canonical_digest_is_frozen(self):
        stream = b"".join(
            result.line for result in run_all(self.fixtures, "ironmon_smart"))
        self.assertEqual(
            "0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7",
            hashlib.sha256(stream).hexdigest(),
        )

    def test_v3_unknown_malformed_float_and_switch_prior_fail_closed(self):
        base = json.loads(IRONMON_FIXTURES.read_text(encoding="utf-8"))
        mutations = []
        unknown = copy.deepcopy(base)
        unknown["fixtures"][0]["unknown"] = True
        mutations.append((unknown, "unknown"))
        floating = copy.deepcopy(base)
        floating["fixtures"][0]["candidates"][0]["entry_cost"] = 1.5
        mutations.append((floating, "floating-point"))
        switch_prior = copy.deepcopy(base)
        switch_prior["defaults"]["public_state"]["response_model"][
            "opponent_switch_weight"] = 1
        mutations.append((switch_prior, "switch weight"))
        short_branch = copy.deepcopy(base)
        short_branch["fixtures"][0]["candidates"][0]["responses"][0].pop()
        mutations.append((short_branch, "compact Ironmon response"))
        for document, message in mutations:
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                with self.assertRaisesRegex(FixtureError, message):
                    load_fixtures(self.write_document(document, directory))

    def test_direct_loaded_fixture_validation_rejects_private_float(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["private_state"]["hidden_opponent"]["exact_stats"] = 1.25
        with self.assertRaisesRegex(FixtureError, "floating-point"):
            validate_ironmon_fixture(fixture)

    def test_baselines_and_standard_are_deterministic_on_v3(self):
        for policy_id in (
                "uniform_legal", "ko_first_no_switch", "first_legal", "standard"):
            with self.subTest(policy=policy_id):
                left = b"".join(
                    result.line for result in run_all(self.fixtures, policy_id))
                right = b"".join(
                    result.line for result in run_all(self.fixtures, policy_id))
                self.assertEqual(left, right)
                metrics = summarize(run_all(self.fixtures, policy_id))
                self.assertEqual(0, metrics["illegal_action"]["count"])
                self.assertEqual(0, metrics["deterministic_replay_mismatch_count"])
                self.assertEqual(63, metrics["chosen_utility"]["count"])

    def test_cli_supports_v3_validate_run_replay_and_summarize(self):
        commands = (
            ["validate"],
            ["run", "--policy", "ironmon_smart", "--replicate", "0"],
            ["replay", "--fixture-id", "ironmon_equal_four", "--policy",
             "ironmon_smart", "--replicate", "37"],
            ["summarize", "--policy", "ironmon_smart", "--replicate", "0"],
        )
        for arguments in commands:
            with self.subTest(arguments=arguments):
                completed = subprocess.run(
                    [sys.executable, str(CLI), *arguments], cwd=ROOT,
                    check=True, text=True, capture_output=True,
                )
                self.assertEqual("", completed.stderr)
                lines = completed.stdout.splitlines()
                expected_lines = 63 if arguments[0] == "run" else 1
                self.assertEqual(expected_lines, len(lines))
                self.assertTrue(all(isinstance(json.loads(line), dict) for line in lines))


if __name__ == "__main__":
    unittest.main()
