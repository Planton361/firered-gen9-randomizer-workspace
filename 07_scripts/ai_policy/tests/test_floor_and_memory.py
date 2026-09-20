import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy.floor import apply_common_floor
from ai_policy.memory import consecutive_successes, detects_aba_switch_loop, voluntary_switch_edges
from ai_policy.observation import project_observation
from ai_policy.runner import run_fixture
from ai_policy.schema import load_fixtures


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_fixtures.json"


class FloorAndMemoryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(FIXTURES)
        cls.by_id = {item["fixture_id"]: item for item in cls.fixtures}

    def test_every_fixture_selects_an_allowed_action_and_no_forbidden_action(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                result = run_fixture(fixture)
                self.assertIn(result.trace["selected_action_id"], fixture["expected"]["allowed_best_set"])
                self.assertNotIn(result.trace["selected_action_id"], fixture["expected"]["forbidden_actions"])

    def test_required_floor_reasons_are_emitted(self):
        for fixture in self.fixtures:
            with self.subTest(fixture=fixture["fixture_id"]):
                reasons = set(run_fixture(fixture).trace["hard_floor_reasons"])
                self.assertLessEqual(set(fixture["expected"]["required_reasons"]), reasons)

    def test_robust_ko_dominates_accuracy_utility(self):
        result = run_fixture(self.by_id["ko_vs_accuracy"])
        self.assertEqual("ko_move", result.trace["selected_action_id"])
        self.assertEqual(["sand_attack", "smokescreen"], result.trace["excluded_action_ids"])

    def test_capped_accuracy_and_setup_are_nonproductive(self):
        for fixture_id in ("accuracy_capped", "capped_setup"):
            result = run_fixture(self.by_id[fixture_id])
            self.assertIn("CAPPED_STAT_CHANGE", result.trace["hard_floor_reasons"])

    def test_redundant_status_and_full_hp_recovery_lose_to_damage(self):
        redundant = run_fixture(self.by_id["redundant_status"])
        recovery = run_fixture(self.by_id["full_hp_recovery"])
        self.assertEqual("damage", redundant.trace["selected_action_id"])
        self.assertIn("REDUNDANT_STATUS", redundant.trace["hard_floor_reasons"])
        self.assertEqual("damage", recovery.trace["selected_action_id"])
        self.assertIn("NO_MARGINAL_VALUE", recovery.trace["hard_floor_reasons"])

    def test_known_no_effect_loses_to_productive_attack(self):
        result = run_fixture(self.by_id["known_immunity"])
        self.assertEqual("neutral_hit", result.trace["selected_action_id"])
        self.assertIn("KNOWN_NO_EFFECT", result.trace["hard_floor_reasons"])

    def test_forced_action_is_tagged_and_selected(self):
        result = run_fixture(self.by_id["forced_choice"])
        self.assertEqual("forced_locked_move", result.trace["selected_action_id"])
        self.assertIn("FORCED_ACTION", result.trace["hard_floor_reasons"])

    def test_all_futile_uses_deterministic_least_cost_fallback(self):
        fixture = self.by_id["all_futile"]
        for replicate in range(20):
            result = run_fixture(fixture, replicate=replicate)
            self.assertEqual("least_cost_futile", result.trace["selected_action_id"])
            self.assertIn("NO_PRODUCTIVE_ACTION", result.trace["hard_floor_reasons"])
            self.assertEqual(0, result.trace["policy_rng"]["draw_count"])

    def test_string_shot_contract_distinguishes_order_flip(self):
        self.assertEqual("string_shot", run_fixture(self.by_id["string_shot_flip"]).trace["selected_action_id"])
        self.assertEqual("damage", run_fixture(self.by_id["string_shot_no_benefit"]).trace["selected_action_id"])

    def test_sand_attack_and_smokescreen_share_repeat_family(self):
        fixture = self.by_id["accuracy_alternating_repeat"]
        self.assertEqual(2, consecutive_successes(fixture["policy_memory"]["decisions"], "sand_attack"))
        result = run_fixture(fixture)
        self.assertIn("HARMFUL_REPEAT", result.trace["hard_floor_reasons"])
        self.assertEqual("damage", result.trace["selected_action_id"])

    def test_forced_replacement_does_not_consume_voluntary_loop_budget(self):
        decisions = self.by_id["switch_loop"]["policy_memory"]["decisions"]
        self.assertEqual([("A", "B"), ("B", "A")], voluntary_switch_edges(decisions))
        self.assertTrue(detects_aba_switch_loop(decisions))

    def test_good_emergency_switch_beats_entry_ko_switch(self):
        result = run_fixture(self.by_id["emergency_switch"])
        self.assertEqual("good_switch", result.trace["selected_action_id"])
        self.assertIn("ENTRY_KO", result.trace["hard_floor_reasons"])

    def test_filtering_does_not_consume_rng(self):
        fixture = self.by_id["equal_four"]
        observation = project_observation(fixture)
        floor = apply_common_floor(observation, fixture["policy_memory"])
        self.assertEqual(("equal_a", "equal_b", "equal_c", "equal_d"), floor.eligible_ids)
        self.assertEqual(1, run_fixture(fixture).trace["policy_rng"]["draw_count"])


if __name__ == "__main__":
    unittest.main()
