"""Focused source-only regression tests for #616 audit failure boundaries."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gen9_data_parity_audit as audit


class ParityTests(unittest.TestCase):
    def test_ts_literals_do_not_read_callback_properties(self):
        fields = audit.direct_fields('\t\taccuracy: true,\n\t\tpriority: -6,\n\t\tonHit() {\n\t\t\tpp: 99,\n\t\t},\n')
        self.assertEqual(fields, {"accuracy": True, "priority": -6})

    def test_machine_accent_is_not_a_mismatch(self):
        self.assertEqual(audit.identity("Façade"), audit.identity("MOVE_FACADE".removeprefix("MOVE_")))

    def test_array_count_padding_and_overflow(self):
        order, explicit = audit.move_order("gMoves[2] = { MOVE_POUND };", "gMoves", 2)
        self.assertEqual((order, explicit), (["MOVE_POUND", "MOVE_NONE"], 1))
        with self.assertRaisesRegex(ValueError, "overflow"):
            audit.move_order("gMoves[1] = { MOVE_POUND, MOVE_CUT };", "gMoves", 1)

    def test_missing_array_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Missing order"):
            audit.move_order("", "gMoves", 2)

    def test_machine_order_error_does_not_shift_bits(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "1 - Hail.txt").write_text("TM01: Hail\nBULBASAUR\n")
            pairs, issues, _ = audit.compatibility_files(path, 1, ["MOVE_LOWKICK"], {"SPECIES_BULBASAUR": 1})
            self.assertEqual(pairs, {(1, 0)})
            self.assertEqual(issues[0]["class"], "DATA_MISMATCH")

    def test_invalid_species_row_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "1 - Cut.txt").write_text("TM01: Cut\n1440\n")
            with self.assertRaisesRegex(ValueError, "outside bitset"):
                audit.compatibility_files(path, 1, ["MOVE_CUT"], {})

    def test_missing_compatibility_file_is_not_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, issues, _ = audit.compatibility_files(Path(tmp), 1, ["MOVE_CUT"], {})
            self.assertEqual(issues[0]["reason"], "missing/duplicate compatibility file")

    def test_acquisition_methods_are_separate_and_inherited(self):
        learnsets = {"base": {"pound": ["9M", "8T", "9L1", "9E"]}, "child": {"cut": ["8M"]}}
        metadata = {"child": {"prevo": "Base"}}
        self.assertEqual(dict(audit.acquisition_evidence("child", learnsets, metadata, "T")), {"cut": set(), "pound": {"8T"}})
        self.assertEqual(audit.acquisition_evidence("child", learnsets, metadata, "M")["pound"], {"9M"})

    def test_inheritance_cycle_rejected(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            audit.acquisition_evidence("a", {}, {"a": {"prevo": "b"}, "b": {"prevo": "a"}}, "M")

    def test_evolution_parser_retains_malformed_designator_evidence(self):
        parsed = audit.evolution_rows("[SPECIES_STANTLER] {{EVO_MOVE, MOVE_PSYSHIELDBASH, SPECIES_WYRDEER, 0}},\n};")
        self.assertEqual(parsed["SPECIES_STANTLER"][0][2], "SPECIES_WYRDEER")
        parsed = audit.evolution_rows("[SPECIES_ROCKRUFF] = {{EVO_LEVEL_SPECIFIC_TIME_RANGE, 25, SPECIES_LYCANROC_DUSK, TIME_RANGE(17, 20)}},\n};")
        self.assertEqual(len(parsed["SPECIES_ROCKRUFF"][0]), 4)
        self.assertEqual(parsed["SPECIES_ROCKRUFF"][0][3], "TIME_RANGE(17, 20)")

    def test_reference_revision_rejected_before_source_reads(self):
        with patch.object(audit.closure, "git", return_value="wrong"):
            with self.assertRaisesRegex(ValueError, "Showdown revision"):
                audit.verify(Path("unused"))

    def test_reference_file_hash_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            reference = audit.json.loads(audit.closure.REFERENCE.read_text())
            for name in reference["sha256"]:
                (path / name).write_text("altered source")
            with patch.object(audit.closure, "git", return_value=reference["revision"]):
                with self.assertRaisesRegex(ValueError, "file hashes"):
                    audit.verify(path)

    def test_last_move_row_without_comma_is_not_missing(self):
        rows = audit.c_rows("[MOVE_PSYCHICNOISE] =\n{\n.power = 90,\n}\n#endif\n};", "MOVE_")
        self.assertEqual(audit.c_fields(rows["MOVE_PSYCHICNOISE"])["power"], "90")


if __name__ == "__main__":
    unittest.main()
