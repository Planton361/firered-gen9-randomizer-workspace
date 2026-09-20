import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ai_policy import SCHEMA_VERSION
from ai_policy.schema import FixtureError, load_fixtures, validate_fixture


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "synthetic_fixtures.json"


class SchemaContractTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = load_fixtures(FIXTURES)

    def write_document(self, document, directory):
        path = Path(directory) / "fixtures.json"
        path.write_text(json.dumps(document), encoding="utf-8")
        return path

    def test_corpus_is_versioned_and_complete(self):
        self.assertEqual(29, len(self.fixtures))
        self.assertTrue(all(item["schema_version"] == SCHEMA_VERSION for item in self.fixtures))

    def test_mandatory_inventory_tags_are_present(self):
        tags = {tag for fixture in self.fixtures for tag in fixture["expected"]["coverage_tags"]}
        required = {
            "guaranteed_ko_vs_accuracy", "accuracy_neutral", "accuracy_lowered",
            "accuracy_capped", "string_shot_order_flip", "string_shot_no_order_benefit",
            "redundant_major_status", "useful_setup", "capped_setup", "full_hp_recovery",
            "known_immunity", "forced_choice_encore", "emergency_good_vs_entry_ko_switch",
            "aba_switch_loop", "two_equal_actions", "four_equal_actions",
            "hidden_move_twin", "hidden_item_twin", "hidden_ability_twin",
            "hidden_bench_twin", "submitted_action_twin", "all_futile_fallback",
        }
        self.assertEqual(set(), required - tags)

    def test_duplicate_fixture_id_is_rejected(self):
        document = json.loads(FIXTURES.read_text(encoding="utf-8"))
        document["fixtures"].append(copy.deepcopy(document["fixtures"][0]))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FixtureError, "duplicate fixture ID"):
                load_fixtures(self.write_document(document, directory))

    def test_unknown_schema_is_rejected(self):
        document = json.loads(FIXTURES.read_text(encoding="utf-8"))
        document["schema_version"] = "future"
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FixtureError, "unknown schema"):
                load_fixtures(self.write_document(document, directory))

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaisesRegex(FixtureError, "cannot load"):
                load_fixtures(path)

    def test_incomplete_fixture_is_rejected(self):
        fixture = copy.deepcopy(self.fixtures[0])
        del fixture["expected"]
        with self.assertRaisesRegex(FixtureError, "missing"):
            validate_fixture(fixture)

    def test_contradictory_expected_sets_are_rejected(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["expected"]["forbidden_actions"].append("ko_move")
        with self.assertRaisesRegex(FixtureError, "allowed/forbidden contradiction"):
            validate_fixture(fixture)

    def test_contradictory_action_facts_are_rejected(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["truth_state"]["actions"][0]["legal"] = False
        with self.assertRaisesRegex(FixtureError, "illegal action claims"):
            validate_fixture(fixture)

    def test_seed_mismatch_is_rejected(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["seeds"]["decision"] ^= 1
        with self.assertRaisesRegex(FixtureError, "seed fields"):
            validate_fixture(fixture)

    def test_unknown_public_history_field_is_rejected(self):
        fixture = copy.deepcopy(self.fixtures[0])
        fixture["public_history"].append({"submitted_action": "secret"})
        with self.assertRaisesRegex(FixtureError, "unknown fields"):
            validate_fixture(fixture)

    def test_short_compact_action_is_rejected(self):
        document = json.loads(FIXTURES.read_text(encoding="utf-8"))
        document["fixtures"][0]["truth_state"]["actions"][0].pop()
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(FixtureError, "compact action"):
                load_fixtures(self.write_document(document, directory))


if __name__ == "__main__":
    unittest.main()
