import csv
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "randomizer_coverage_auditor.py"
SPEC = importlib.util.spec_from_file_location("randomizer_coverage_auditor", SCRIPT_PATH)
auditor = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = auditor
SPEC.loader.exec_module(auditor)


SAMPLE_LOG = """
( Starter Pokemon {SRPK} )
Mode: Random (completely)
Set starter 1 to Bulbasaur, holding Potion
Set starter 2 to Vivillon Fancy
Set starter 3 to Rotom-Wash

==========================================================

( Static Pokemon {STPK} )
Snorlax Lv30 => Deoxys Attack Lv30

==========================================================

( Wild Pokemon {WDPK} )
Area #1 - Route 1 (rate=25)
Alcremie Berry Lv4
Minior Core Lvs5-7

==========================================================

( Trainer Pokemon {TRPK} )
#1 (Bug Catcher) - Silvally Fire@Leftovers Lv7, Unown ! Lv8

==========================================================

( Shop Items {SHMS} )
--Special Shops:--

Celadon Department 4F
- TM51
- Oran Berry

==========================================================

( Pickup Items {PUMS} )
Level 1-10
10%: Fire Gem, Potion

==========================================================

( TM Moves {TMMV} )
TM01: Tackle
HM01 Cut => Surf
"""


class RandomizerCoverageAuditorTest(unittest.TestCase):

    def test_expected_parsers_extract_species_items_and_tms(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"

            result = auditor.build_expected(out, root)

            species = {row["source_constant"]: row for row in result["species_expected.tsv"]}
            items = {row["source_constant"]: row for row in result["items_expected.tsv"]}
            tms = {row["source_constant"]: row for row in result["tms_hms_expected.tsv"]}
            self.assertEqual("Bulbasaur", species["SPECIES_BULBASAUR"]["display_name_guess"])
            self.assertEqual("Vivillon", species["SPECIES_VIVILLON"]["form_family"])
            self.assertEqual("TM51", items["ITEM_TM51"]["display_name_guess"])
            self.assertEqual("yes", items["ITEM_TM51"]["is_tm"])
            self.assertEqual("yes", items["ITEM_HM01_CUT"]["is_hm"])
            self.assertIn("ITEM_TM51", tms)
            self.assertIn("ITEM_HM01_CUT", tms)

    def test_parse_logs_reuses_shop_pickup_and_reads_species_sections(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            temp_dir = Path(temp_name)
            logs = temp_dir / ".local" / "coverage" / "raw-logs"
            out = temp_dir / ".local" / "coverage"
            logs.mkdir(parents=True)
            raw_log = logs / "run_0001.log"
            raw_log.write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.parse_logs(logs, out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_observed.tsv")}
            items = {row["canonical_key"]: row for row in read_tsv(out / "items_observed.tsv")}
            tms = {row["canonical_key"]: row for row in read_tsv(out / "tms_hms_observed.tsv")}
            self.assertIn("bulbasaur", species)
            self.assertIn("deoxys_attack", species)
            self.assertIn("silvally_fire", species)
            self.assertIn("oran_berry", items)
            self.assertIn("fire_gem", items)
            self.assertIn("tm51", tms)
            self.assertIn("hm01", tms)

    def test_compare_marks_expected_not_observed_as_non_loaded_failure_boundary(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            auditor.compare_all(out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_coverage.tsv")}
            items = {row["canonical_key"]: row for row in read_tsv(out / "items_coverage.tsv")}
            self.assertEqual("EXPECTED_AND_OBSERVED", species["bulbasaur"]["coverage_status"])
            self.assertEqual("EXPECTED_NOT_OBSERVED", species["charmander"]["coverage_status"])
            self.assertIn("do not prove", species["charmander"]["reason"])
            self.assertEqual("OBSERVED_NOT_EXPECTED", species["deoxys_attack"]["coverage_status"])
            self.assertEqual("EXPECTED_AND_OBSERVED", items["tm51"]["coverage_status"])

    def test_parse_logs_can_delete_raw_logs_only_after_success(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            temp_dir = Path(temp_name)
            logs = temp_dir / ".local" / "coverage" / "raw-logs"
            out = temp_dir / ".local" / "coverage"
            logs.mkdir(parents=True)
            raw_log = logs / "run_0001.log"
            raw_log.write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.parse_logs(logs, out, delete_raw=True)

            self.assertFalse(raw_log.exists())
            self.assertTrue((out / "species_observed.tsv").exists())

    def test_cleanup_refuses_outside_workspace_paths(self):
        with tempfile.TemporaryDirectory() as temp_name:
            outside = Path(temp_name) / "run.log"
            outside.write_text(SAMPLE_LOG, encoding="utf-8")

            with self.assertRaises(ValueError):
                auditor.cleanup_files([outside], outside.parent, {".log"})

            self.assertTrue(outside.exists())

    def test_sanitize_path_removes_private_path(self):
        sanitized = auditor.sanitize_path_for_error(Path("/home/anton/private/input.gba"))

        self.assertEqual("<path>", sanitized)

    def test_expected_not_observed_is_not_written_to_suspicious_by_default(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            auditor.compare_all(out)

            suspicious = read_tsv(out / "suspicious_or_missing.tsv")
            self.assertNotIn("charmander", {row["canonical_key"] for row in suspicious})
            self.assertIn("deoxys_attack", {row["canonical_key"] for row in suspicious})

    def test_help_command_is_available(self):
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as context:
                auditor.build_parser().parse_args(["--help"])

        self.assertEqual(0, context.exception.code)


def write_source_fixture(root):
    dpe = root / "02_external" / "Dynamic-Pokemon-Expansion-Gen-9" / "include"
    cfru = root / "02_external" / "CFRU-expansion" / "include" / "constants"
    dpe.mkdir(parents=True)
    cfru.mkdir(parents=True)
    (dpe / "species.h").write_text(
        "\n".join([
            "#define SPECIES_NONE 0x0",
            "#define SPECIES_BULBASAUR 0x1",
            "#define SPECIES_CHARMANDER 0x4",
            "#define SPECIES_VIVILLON 0x306",
            "#define SPECIES_ALCREMIE_BERRY 0x4AC",
            "#define SPECIES_ROTOM_WASH 0x2CA",
            "#define SPECIES_COUNT 0x999",
        ]),
        encoding="utf-8",
    )
    (dpe / "items.h").write_text(
        "\n".join([
            "#define ITEM_NONE 0x0",
            "#define ITEM_POTION 0xD",
            "#define ITEM_ORAN_BERRY 0x8B",
            "#define ITEM_FIRE_GEM 0x250",
            "#define ITEM_TM51 376",
            "#define ITEM_HM01_CUT 0x153",
            "#define ITEMS_COUNT 0x999",
        ]),
        encoding="utf-8",
    )
    (cfru / "species.h").write_text("", encoding="utf-8")
    (cfru / "items.h").write_text("", encoding="utf-8")


def read_tsv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def local_test_root():
    root = Path(".local/test-randomizer-coverage-auditor")
    root.mkdir(parents=True, exist_ok=True)
    return root


if __name__ == "__main__":
    unittest.main()
