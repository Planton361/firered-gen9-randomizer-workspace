import copy
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy.observation import canonical_json, observation_hash, project_observation
from ai_policy.runner import run_all, run_fixture, twin_mismatches
from ai_policy.schema import load_fixtures


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_fixtures.json"


class ObservationBoundaryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(FIXTURES)
        cls.by_id = {item["fixture_id"]: item for item in cls.fixtures}

    def test_fair_mode_filters_hidden_active_data(self):
        observation = project_observation(self.by_id["hidden_move_a"])
        active = observation["opponent_active"]
        self.assertEqual([], active["moves"])
        self.assertIsNone(active["item"])
        self.assertIsNone(active["ability"])
        self.assertNotIn("hidden_stats", active)

    def test_fair_mode_filters_unseen_bench_identity(self):
        observation = project_observation(self.by_id["hidden_bench_a"])
        self.assertEqual([{"unknown": True}], observation["opponent_bench"])

    def test_submitted_action_and_future_rng_are_never_projected(self):
        for fixture in self.fixtures:
            serialized = canonical_json(project_observation(fixture))
            self.assertNotIn("submitted_action", serialized)
            self.assertNotIn("future_rng", serialized)

    def test_active_hidden_stat_changes_do_not_change_fair_observation(self):
        left = copy.deepcopy(self.by_id["hidden_move_a"])
        right = copy.deepcopy(left)
        right["truth_state"]["opponent_active"]["hidden_stats"] = {
            "ivs": 31, "evs": 252, "nature": "different", "speed": 999,
        }
        self.assertEqual(project_observation(left), project_observation(right))
        self.assertEqual(observation_hash(project_observation(left)),
                         observation_hash(project_observation(right)))

    def test_all_fair_hidden_and_submitted_twins_match(self):
        self.assertEqual([], twin_mismatches(run_all(self.fixtures)))

    def test_challenge_exposes_authorized_full_team_fields(self):
        fixture = self.by_id["challenge_boundary"]
        observation = project_observation(fixture)
        active = observation["opponent_active"]
        self.assertEqual("KNOWN_ITEM", active["item"])
        self.assertEqual("KNOWN_ABILITY", active["ability"])
        self.assertEqual([{"id": "KNOWN_MOVE", "pp": 7}], active["moves"])
        self.assertEqual("KNOWN_BENCH", observation["opponent_bench"][0]["species"])
        serialized = canonical_json(observation)
        self.assertNotIn("submitted_action", serialized)
        self.assertNotIn("future_rng", serialized)

    def test_challenge_still_ignores_submitted_action_and_future_rng(self):
        left = copy.deepcopy(self.by_id["challenge_boundary"])
        right = copy.deepcopy(left)
        right["truth_state"]["submitted_action"] = "DIFFERENT_CHOICE"
        right["truth_state"]["future_rng"] = 0
        self.assertEqual(project_observation(left), project_observation(right))

    def test_reveal_changes_observation_and_adds_trace_reason(self):
        hidden = copy.deepcopy(self.by_id["hidden_move_a"])
        revealed = copy.deepcopy(hidden)
        revealed["observation_mask"]["revealed_moves"] = ["HIDDEN_FIRE"]
        revealed["public_history"] = [{"moves_seen": ["HIDDEN_FIRE"]}]
        self.assertNotEqual(project_observation(hidden), project_observation(revealed))
        self.assertIn("REVEALED_MOVE:HIDDEN_FIRE",
                      run_fixture(revealed).trace["observation_reasons"])

    def test_observation_hash_is_canonical_across_mapping_order(self):
        observation = project_observation(self.by_id["equal_two"])
        reversed_mapping = dict(reversed(list(observation.items())))
        self.assertEqual(observation_hash(observation), observation_hash(reversed_mapping))


if __name__ == "__main__":
    unittest.main()
