"""Synthetic source fixtures only. No ROM, save, generated build or network."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import showdown_pokemon_data_sync as sync
import showdown_pinned_closure as closure
import showdown_coherent_forms as coherent


class ClosureTests(unittest.TestCase):
    values = {"MOVE_TACKLE": 1, "MOVE_GROWL": 2, "MOVE_NONE": 0}
    good = ((1, "MOVE_TACKLE"), (4, "MOVE_GROWL"))

    def record(self, expected=None, source="a", **kw):
        return {"source": source, "local": source, "expected": expected,
                "form_blocker": None, "move_blockers": [], **kw}

    def classify(self, current, records, uncovered=()):
        return closure.classify_table(current, records, uncovered, self.values)[0]

    def test_identical_shared_expectations_are_coalesced(self):
        records = [self.record(self.good), self.record(self.good, "b")]
        self.assertEqual("SAFE_DATA_DIFF", self.classify((), records))
        self.assertEqual("NO_DIFF", self.classify(self.good, records))

    def test_conflict_cannot_be_hidden_by_last_form_or_input_order(self):
        records = [self.record(self.good), self.record(((1, "MOVE_GROWL"),), "b")]
        for ordered in (records, records[::-1]):
            self.assertEqual("SHARED_TABLE_CONFLICT", self.classify((), ordered))

    def test_empty_literal_form_is_conflict_not_permission_to_clear(self):
        self.assertEqual("SHARED_TABLE_CONFLICT", self.classify((), [
            self.record(self.good), self.record((), "b", form_blocker="no level sources")]))

    def test_missing_form_is_not_inherited_without_evidence(self):
        self.assertEqual("FORM_MAPPING_BLOCK", self.classify((), [
            self.record(self.good), self.record(None, "b", form_blocker="missing")]))
        self.assertEqual("FORM_MAPPING_BLOCK", self.classify((), [self.record(self.good)], ["b"]))

    def test_blocked_move_consumer_blocks_shared_update(self):
        self.assertEqual("MOVE_BEHAVIOR_BLOCK", self.classify((), [
            self.record(self.good), self.record(None, "b", move_blockers=["allyswitch"])]))

    def test_order_only_changes_are_not_assumed_harmless(self):
        a = ((1, "MOVE_TACKLE"), (1, "MOVE_GROWL"))
        self.assertEqual("MOVE_BEHAVIOR_BLOCK", self.classify(a, [self.record(a[::-1])]))

    def test_l1_and_bounds_validation(self):
        for pairs in ((), ((27, "MOVE_TACKLE"),), ((101, "MOVE_TACKLE"),),
                      ((-1, "MOVE_TACKLE"),), ((1, "MOVE_NONE"),), ((1, "MOVE_UNKNOWN"),),
                      ((1, "MOVE_TACKLE"),) * 51, ((2, "MOVE_TACKLE"), (1, "MOVE_GROWL"))):
            with self.subTest(pairs=pairs):
                self.assertEqual("FAIL_LOW_LEVEL_PATH", closure.move_invariant(pairs, self.values)["status"])
        self.assertEqual("PASS_L1_STRUCTURAL", closure.move_invariant(self.good, self.values)["status"])
        self.assertEqual("PASS_L1_STRUCTURAL", closure.move_invariant(((0, "MOVE_TACKLE"),), self.values)["status"])

    def test_one_generation_never_retains_older_only_moves(self):
        selected, _ = sync.latest_level_moves({"tackle": ["8L1", "9L4"], "growl": ["7L1"], "other": ["9M"]})
        self.assertEqual([(4, "tackle")], selected)
        with self.assertRaises(ValueError):
            sync.latest_level_moves({"tackle": ["10L1"]})

    def test_newest_complete_literal_not_per_move_fallback(self):
        self.assertEqual((8, [(1, "tackle"), (7, "growl")]), sync.coherent_level_moves(
            {"tackle": ["7L1", "8L1", "9M"], "growl": ["8L7"], "old": ["6L1"]}))
        for source in ("9L1x", "9L", "0L1", "10L1"):
            with self.assertRaises(ValueError):
                sync.coherent_level_moves({"tackle": [source]})

    def test_own_older_form_dataset_wins_over_newer_parent(self):
        datasets = {"base": {"tackle": ["9L1"]}, "form": {"growl": ["6L1"]}}
        forms = {"base": {}, "form": {"forme": "Cosplay", "changesFrom": "Base"}}
        result = coherent.select("form", datasets, forms)
        self.assertEqual((6, [(1, "growl")], "form"), (result["generation"], result["moves"], result["dataset"]))

    def test_restricted_moves_are_not_level_up_moves(self):
        result = coherent.select("form", {"base": {"tackle": ["9L1"]}, "form": {"special": ["9R"]}},
            {"base": {}, "form": {"changesFrom": "Base"}})
        self.assertEqual([(1, "tackle")], result["moves"])
        self.assertEqual("explicit-changesFrom-or-battleOnly", result["policy"])

    def test_missing_literal_form_requires_source_structure(self):
        datasets = {"base": {"tackle": ["9L1"]}}
        forms = {"base": {}, "form": {"forme": "Origin", "baseSpecies": "Base"}}
        self.assertEqual(9, coherent.select("form", datasets, forms)["generation"])
        # Own non-level literal without an explicit switch relation cannot be
        # assumed to inherit (e.g. an event-only or independently defined form).
        with self.assertRaises(ValueError):
            coherent.select("form", {**datasets, "form": {"special": ["9S0"]}}, forms)
        with self.assertRaises(ValueError):
            coherent.select("guessedprefixform", datasets, forms)

    def test_all_explicit_battle_parents_must_agree(self):
        forms = {"a": {}, "b": {}, "form": {"battleOnly": ["A", "B"]}}
        datasets = {"a": {"tackle": ["9L1"]}, "b": {"tackle": ["9L1"]}}
        self.assertEqual(2, len(coherent.select("form", datasets, forms)["parents"]))
        for differing in ({"growl": ["9L1"]}, {"tackle": ["8L1"]}):
            with self.assertRaises(ValueError):
                coherent.select("form", {**datasets, "b": differing}, forms)

    def test_cyclic_inheritance_and_prevo_fallback_fail_closed(self):
        with self.assertRaises(ValueError):
            coherent.select("a", {}, {"a": {"changesFrom": "B"}, "b": {"changesFrom": "A"}})
        with self.assertRaises(ValueError):
            coherent.select("a", {"b": {"tackle": ["9L1"]}}, {"a": {"prevo": "B"}, "b": {}})

    def test_no_fabricated_l1_from_an_older_generation(self):
        result = coherent.select("a", {"a": {"tackle": ["8L1", "9L5"]}}, {"a": {}})
        self.assertEqual([(5, "tackle")], result["moves"])

    def test_tie_order_preserved_but_removed_moves_cannot_survive(self):
        original = ((1, "MOVE_GROWL"), (1, "MOVE_TACKLE"), (1, "MOVE_OLD"))
        desired = [(1, "MOVE_TACKLE"), (1, "MOVE_NEW"), (1, "MOVE_GROWL")]
        self.assertEqual(((1, "MOVE_GROWL"), (1, "MOVE_TACKLE"), (1, "MOVE_NEW")),
                         coherent.preserve_ties(desired, original))

    def fixture(self, directory):
        path = Path(directory) / "synthetic.c"
        path.write_text("// [SPECIES_COMMENT] = sGhostLevelUpLearnset\n"
            "static const struct LevelUpMove sSharedLevelUpLearnset[] = {\n"
            "\tLEVEL_UP_MOVE(1, MOVE_TACKLE),\n\tLEVEL_UP_END};\n\n"
            "static const struct LevelUpMove sOtherLevelUpLearnset[] = {\n"
            "\tLEVEL_UP_MOVE(1, MOVE_GROWL),\n\tLEVEL_UP_END,\n};\n"
            "[SPECIES_A] = sSharedLevelUpLearnset,\n"
            "[SPECIES_B] = sSharedLevelUpLearnset,\n"
            "[SPECIES_C] = sOtherLevelUpLearnset,\n")
        return path

    def test_exact_split_and_new_existing_id_binding_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            original = path.read_text().replace("[SPECIES_A]", "const struct LevelUpMove* const gLevelUpLearnsets[] =\n{\n[SPECIES_A]", 1) + "};\n"
            target = ((1, "MOVE_GROWL"),)
            after = coherent.render(original, {"sSplitLevelUpLearnset": target},
                {"b": "sSplitLevelUpLearnset", "d": "sSharedLevelUpLearnset"},
                {"b": "SPECIES_B", "d": "SPECIES_D"})
            pointers, tables = closure.read_tables(coherent.TextSource(after))
            self.assertEqual("sSharedLevelUpLearnset", pointers["a"])
            self.assertEqual("sSharedLevelUpLearnset", pointers["d"])
            self.assertEqual("sSplitLevelUpLearnset", pointers["b"])
            self.assertEqual(target, tables["sSplitLevelUpLearnset"])
            self.assertEqual(original, path.read_text().replace("[SPECIES_A]", "const struct LevelUpMove* const gLevelUpLearnsets[] =\n{\n[SPECIES_A]", 1) + "};\n")
            for invalid in ((), ((8, "MOVE_GROWL"),), ((1, "MOVE_NONE"),), target * 51):
                with self.assertRaises(ValueError):
                    coherent.render(original, {"sSplitLevelUpLearnset": invalid}, {}, {})

    def test_source_form_metadata_parser_handles_parent_arrays(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pokedex.ts"
            path.write_text('export const Pokedex = {\n form: {\n name: "Form",\n baseSpecies: "Base",\n forme: "Ultra",\n battleOnly: ["A", "B"],\n },\n};\n')
            self.assertEqual(["A", "B"], coherent.metadata(path)["form"]["battleOnly"])

    def test_inline_end_comments_and_pointer_key_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            pointers, tables = closure.read_tables(path)
            self.assertEqual(3, len(pointers))
            self.assertEqual(((1, "MOVE_TACKLE"),), tables["sSharedLevelUpLearnset"])
            original = path.read_text()
            changed = sync.update_learnsets_file(path, {"SPECIES_A": list(self.good), "b": list(self.good)},
                True, approved_tables={"sSharedLevelUpLearnset"})
            self.assertEqual(1, changed)
            result = path.read_text()
            self.assertIn("\tLEVEL_UP_END};\n", result)
            self.assertEqual(original[original.index("static const struct LevelUpMove sOther"):],
                             result[result.index("static const struct LevelUpMove sOther"):])
            self.assertEqual(self.good, closure.read_tables(path)[1]["sSharedLevelUpLearnset"])
            self.assertEqual(0, sync.update_learnsets_file(path, {"a": list(self.good)}, True,
                             approved_tables={"sSharedLevelUpLearnset"}))

    def test_writer_prevalidates_all_targets_before_touching_any_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            original = path.read_bytes()
            for updates in ({"a": list(self.good), "b": [(1, "MOVE_GROWL")]},
                            {"a": list(self.good), "unknown": list(self.good)}, {"a": []},
                            {"a": [(27, "MOVE_TACKLE")]}, {"a": [(1, "MOVE_NONE")]}):
                with self.assertRaises(ValueError):
                    sync.update_learnsets_file(path, updates, True, approved_tables={"sSharedLevelUpLearnset"})
                self.assertEqual(original, path.read_bytes())
            with self.assertRaises(ValueError):
                sync.update_learnsets_file(path, {"a": list(self.good)}, True)

    def test_duplicate_or_missing_local_tables_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            original = path.read_text()
            for suffix in ("[SPECIES_A] = sOtherLevelUpLearnset,\n", "[SPECIES_D] = sMissing,\n",
                           "static const struct LevelUpMove sSharedLevelUpLearnset[] = {\nLEVEL_UP_END};\n"):
                path.write_text(original + suffix)
                with self.assertRaises(ValueError):
                    sync.parse_learnset_blocks(path)

    def test_malformed_or_nonterminal_end_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.fixture(tmp)
            path.write_text(path.read_text().replace("LEVEL_UP_END};", "LEVEL_UP_END, LEVEL_UP_MOVE(1, MOVE_TACKLE)};"))
            with self.assertRaises(ValueError):
                closure.read_tables(path)

    def test_pattern_ignore_beats_direct_move(self):
        index = {"moves:*": [{"showdown_pattern": "hiddenpowerfire", "status": "ignore"}]}
        direct = {"hiddenpowerfire": "MOVE_HIDDENPOWER"}
        self.assertEqual((None, "move-ignore"), sync.resolve_move("hiddenpowerfire", direct, direct, index))

    def test_unsupported_ability_never_emits_assignment(self):
        index = {"abilities:commander": [{"status": "open-risk", "generator_policy": "blocked"}]}
        for constants in ({}, {"commander": "ABILITY_TORRENT"}):
            fields, blocked = sync.target_fields({"abilities": {"0": "commander"}}, constants, index)
            self.assertNotIn("ability1", fields)
            self.assertEqual(1, len(blocked))
        self.assertEqual((None, "ability-unmapped"), sync.resolve_ability("invented", {}, {}))

    def test_ambiguous_aliases_are_not_first_match_wins(self):
        entries = [{"status": "alias", "local_keys": ["a", "b"]}]
        constants = {"a": "MOVE_TACKLE", "b": "MOVE_GROWL"}
        self.assertEqual((None, "move-ambiguous"), sync.resolve_move("x", constants, constants, {"moves:x": entries}))
        self.assertEqual((None, "ability-ambiguous"), sync.resolve_ability("x", constants, {"abilities:x": entries}))
        self.assertEqual("species-ambiguous", sync.resolve_species("x", {"num": 1}, constants, constants,
                         {"species:x": entries})[1])

    def test_reference_commit_content_and_alias_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "pokedex.ts").write_text("synthetic reference")
            reference = {"revision": "pinned", "sha256": {"pokedex.ts": closure.digest(path / "pokedex.ts")},
                         "aliases_sha256": closure.digest(sync.ALIAS_FILE)}
            with patch.object(closure, "git", return_value="pinned"):
                closure.verify_reference(path, reference)
                with self.assertRaises(ValueError):
                    closure.verify_reference(path, {**reference, "aliases_sha256": "wrong"})
                (path / "pokedex.ts").write_text("modified")
                with self.assertRaises(ValueError):
                    closure.verify_reference(path, reference)
            with patch.object(closure, "git", return_value="other"):
                with self.assertRaises(ValueError):
                    closure.verify_reference(path, reference)

    def test_deterministic_inventory_serialization(self):
        inventory = {"summary": {}, "inventories": {c: [] for c in closure.CATEGORIES},
                     "low_level_invariants": [], "focused_families": {}}
        self.assertEqual(closure.serialize_inventory(inventory, True),
                         closure.serialize_inventory(dict(reversed(list(inventory.items()))), True))


if __name__ == "__main__":
    unittest.main()
