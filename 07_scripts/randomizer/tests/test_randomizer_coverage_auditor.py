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
            self.assertNotIn("ITEM_USE_PARTY_MENU", items)
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

    def test_species_alias_normalization_maps_common_log_labels_to_expected(self):
        aliases = {
            "Flabébé": "flabebe",
            "Farfetch’d": "farfetchd",
            "Sirfetch’d": "sirfetchd",
            "Nidoran♀": "nidoran_f",
            "Nidoran♂": "nidoran_m",
            "Unown !": "unown_exclamation",
            "Unown ?": "unown_question",
            "Squawkbily": "squawkabilly",
            "Baculegion": "basculegion",
            "Dudunsprce": "dudunsparce",
            "Corvknight": "corviknight",
            "Corvsquire": "corvisquire",
            "Fletchindr": "fletchinder",
            "Meowscrada": "meowscarada",
            "Baraskewda": "barraskewda",
            "Polchgeist": "poltchageist",
            "Poltegeist": "polteageist",
            "IronThorns": "iron_thorns",
            "Iron_Valiant": "iron_valiant",
            "RoaringMoon": "roaring_moon",
            "WalkingWake": "walking_wake",
            "GreatTusk": "great_tusk",
            "ScreamTail": "scream_tail",
        }

        for observed, expected_key in aliases.items():
            with self.subTest(observed=observed):
                self.assertEqual(expected_key, auditor.canonical_key_for_observed(observed, "species"))

    def test_item_alias_normalization_maps_common_log_labels_to_expected(self):
        aliases = {
            "TinyMushroom": "tiny_mushroom",
            "BrightPowder": "bright_powder",
            "DeepSeaScale": "deep_sea_scale",
            "DeepSeaTooth": "deep_sea_tooth",
            "Nevermeltice": "never_melt_ice",
            "ThunderStone": "thunder_stone",
            "PrisonBottle": "prison_bottle",
            "Reins Unity": "reins_of_unity",
            "A-Patch": "ability_patch",
            "A-Potion": "ability_potion",
            "Blk Augurite": "black_augurite",
            "BlackGlasses": "black_glasses",
            "TwistedSpoon": "twisted_spoon",
            "SilverPowder": "silver_powder",
            "Unr. Teacup": "unremarkable_teacup",
            "Protec Pads": "protective_pads",
            "Ut. Umbrella": "utility_umbrella",
            "Blunder Pol.": "blunder_policy",
            "Weakness Pol.": "weakness_policy",
            "Terrain Ext.": "terrain_extender",
            "Punch Glove": "punching_glove",
            "Elect. Seed": "electric_seed",
            "X Sp. Atk": "x_special",
            "Fire Mem.": "fire_memory",
            "Electr Mem.": "electric_memory",
            "Fight Mem.": "fighting_memory",
            "Blk Apricorn": "black_apricorn",
            "Blu Apricorn": "blue_apricorn",
            "Grn Apricorn": "green_apricorn",
            "Pnk Apricorn": "pink_apricorn",
            "Wht Apricorn": "white_apricorn",
            "Ylw Apricorn": "yellow_apricorn",
        }

        for observed, expected_key in aliases.items():
            with self.subTest(observed=observed):
                self.assertEqual(expected_key, auditor.canonical_key_for_observed(observed, "item"))

    def test_alias_normalization_reduces_observed_not_expected_fixture_rows(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(
                """
( Wild Pokemon {WDPK} )
Flabébé Lv4
Squawkbily Lv4
Baculegion Lv4
Dudunsprce Lv4
IronThorns Lv4

( Field Items {FIIT} )
1 => TinyMushroom
2 => BrightPowder
3 => DeepSeaScale
4 => Unr. Teacup
5 => Electr Mem.
6 => Blk Apricorn
""",
                encoding="utf-8",
            )

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            auditor.compare_all(out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_coverage.tsv")}
            items = {row["canonical_key"]: row for row in read_tsv(out / "items_coverage.tsv")}
            suspicious_keys = {row["canonical_key"] for row in read_tsv(out / "suspicious_or_missing.tsv")}
            for key in {"flabebe", "squawkabilly", "basculegion", "dudunsparce", "iron_thorns"}:
                self.assertEqual("EXPECTED_AND_OBSERVED", species[key]["coverage_status"])
                self.assertNotIn(key, suspicious_keys)
            for key in {"tiny_mushroom", "bright_powder", "deep_sea_scale", "unremarkable_teacup",
                        "electric_memory", "black_apricorn"}:
                self.assertEqual("EXPECTED_AND_OBSERVED", items[key]["coverage_status"])
                self.assertNotIn(key, suspicious_keys)

    def test_black_belt_trainerclass_line_is_not_held_item_but_explicit_item_is(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            temp_dir = Path(temp_name)
            logs = temp_dir / ".local" / "coverage" / "raw-logs"
            out = temp_dir / ".local" / "coverage"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(
                """
( Trainer Pokemon {TRPK} )
Black Belt Koichi - Machop Lv10
#1 (Black Belt) - Machop@Black Belt Lv10
""",
                encoding="utf-8",
            )

            auditor.parse_logs(logs, out)

            items = {row["canonical_key"]: row for row in read_tsv(out / "items_observed.tsv")}
            self.assertEqual("1", items["black_belt"]["observed_count_total"])
            self.assertEqual("trainer_held_item", items["black_belt"]["observed_sections"])

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
            tms = {row["canonical_key"]: row for row in read_tsv(out / "tm_hm_coverage.tsv")}
            self.assertEqual("EXPECTED_NOT_OBSERVED", tms["tm52"]["coverage_status"])
            suspicious = read_tsv(out / "suspicious_or_missing.tsv")
            suspicious_keys = {row["canonical_key"] for row in suspicious}
            self.assertNotIn("tm52", suspicious_keys)

    def test_loaded_manifest_marks_expected_not_loaded_as_hard_failure(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            write_loaded_manifest(out, species_keys=["bulbasaur"], item_keys=["tm51"], tm_hm_keys=["tm51"])
            auditor.compare_all(out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_coverage.tsv")}
            coverage_rows = (
                read_tsv(out / "species_coverage.tsv")
                + read_tsv(out / "items_coverage.tsv")
                + read_tsv(out / "tm_hm_coverage.tsv")
            )
            hard_failure_count = sum(1 for row in coverage_rows if row["coverage_status"] == "EXPECTED_NOT_LOADED")
            summary = (out / "coverage_summary.md").read_text(encoding="utf-8")
            self.assertEqual("EXPECTED_NOT_LOADED", species["charmander"]["coverage_status"])
            self.assertIn(f"Hard failure candidates (`EXPECTED_NOT_LOADED`): {hard_failure_count}", summary)
            self.assertNotIn("/home/anton/private", summary)

    def test_loaded_species_aliases_and_ids_prevent_false_expected_not_loaded(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text("", encoding="utf-8")

            auditor.build_expected(out, root)
            write_tsv_rows(out / "species_observed.tsv", [], auditor.OBSERVED_FIELDS)
            write_loaded_manifest(out, species_keys=[], item_keys=[], tm_hm_keys=[])
            (out / "species_loaded.tsv").write_text(
                "canonical_key\tdisplay_name\tsource_internal_id\tform_family\tis_loaded\n"
                "nidoran\tNidoran♀\t29\t\tyes\n"
                "unown\tUnown !\t1024\tUnown\tyes\n"
                "rotom\tRotom\t714\tRotom\tyes\n",
                encoding="utf-8",
            )

            auditor.compare_all(out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_coverage.tsv")}
            self.assertEqual("LOADED_NOT_OBSERVED", species["nidoran_f"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", species["unown_exclamation"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", species["rotom_heat"]["coverage_status"])

    def test_loaded_item_aliases_prevent_false_expected_not_loaded(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text("", encoding="utf-8")

            auditor.build_expected(out, root)
            write_tsv_rows(out / "items_observed.tsv", [], auditor.OBSERVED_FIELDS)
            write_tsv_rows(out / "tms_hms_observed.tsv", [], auditor.OBSERVED_FIELDS)
            write_loaded_manifest(out, species_keys=[], item_keys=[], tm_hm_keys=[])
            (out / "items_loaded.tsv").write_text(
                "canonical_key\tdisplay_name\tsource_internal_id\titem_family\tis_loaded\tis_tm\tis_hm\n"
                "thunderstone\tThunderStone\t0\t\tyes\tno\tno\n"
                "fight_mem\tFight Mem.\t0\tMemory\tyes\tno\tno\n"
                "apatch\tA-Patch\t0\t\tyes\tno\tno\n"
                "blkaugurite\tBlk Augurite\t0\t\tyes\tno\tno\n",
                encoding="utf-8",
            )
            (out / "tms_hms_loaded.tsv").write_text(
                "canonical_key\tdisplay_name\tsource_internal_id\titem_family\tis_loaded\tis_tm\tis_hm\n"
                "hm06\tHM06\t0\tHM\tyes\tno\tyes\n",
                encoding="utf-8",
            )

            auditor.compare_all(out)

            items = {row["canonical_key"]: row for row in read_tsv(out / "items_coverage.tsv")}
            tms = {row["canonical_key"]: row for row in read_tsv(out / "tm_hm_coverage.tsv")}
            self.assertEqual("LOADED_NOT_OBSERVED", items["thunder_stone"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", items["fighting_memory"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", items["ability_patch"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", items["black_augurite"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", tms["hm06"]["coverage_status"])

    def test_loaded_manifest_marks_loaded_not_observed_as_non_hard_status(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            write_loaded_manifest(
                out,
                species_keys=["bulbasaur", "charmander"],
                item_keys=["tm51", "potion"],
                tm_hm_keys=["tm51", "tm52"],
            )
            auditor.compare_all(out)

            species = {row["canonical_key"]: row for row in read_tsv(out / "species_coverage.tsv")}
            tms = {row["canonical_key"]: row for row in read_tsv(out / "tm_hm_coverage.tsv")}
            summary = (out / "coverage_summary.md").read_text(encoding="utf-8")
            self.assertEqual("LOADED_NOT_OBSERVED", species["charmander"]["coverage_status"])
            self.assertEqual("LOADED_NOT_OBSERVED", tms["tm52"]["coverage_status"])
            self.assertIn("`LOADED_NOT_OBSERVED` is not a hard failure", summary)
            self.assertIn("Hard failure candidates (`EXPECTED_NOT_LOADED`):", summary)

    def test_compare_ignores_private_path_columns_in_loaded_manifest(self):
        with tempfile.TemporaryDirectory(dir=local_test_root()) as temp_name:
            root = Path(temp_name)
            write_source_fixture(root)
            out = root / ".local" / "coverage"
            logs = out / "raw-logs"
            logs.mkdir(parents=True)
            (logs / "run_0001.log").write_text(SAMPLE_LOG, encoding="utf-8")

            auditor.build_expected(out, root)
            auditor.parse_logs(logs, out)
            write_loaded_manifest(
                out,
                species_keys=["bulbasaur", "charmander"],
                item_keys=["tm51"],
                tm_hm_keys=["tm51"],
                include_private_column=True,
            )
            auditor.compare_all(out)

            for filename in ["species_coverage.tsv", "items_coverage.tsv", "tm_hm_coverage.tsv",
                             "coverage_summary.md", "suspicious_or_missing.tsv"]:
                self.assertNotIn("/home/anton/private", (out / filename).read_text(encoding="utf-8"))

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
            "#define SPECIES_NIDORAN_F 0x1D",
            "#define SPECIES_NIDORAN_M 0x20",
            "#define SPECIES_FARFETCHD 0x53",
            "#define SPECIES_UNOWN_EXCLAMATION 0x400",
            "#define SPECIES_UNOWN_QUESTION 0x401",
            "#define SPECIES_FLABEBE 0x29D",
            "#define SPECIES_VIVILLON 0x306",
            "#define SPECIES_SQUAWKABILLY 0x3AB",
            "#define SPECIES_BASCULEGION 0x386",
            "#define SPECIES_DUDUNSPARCE 0x3D4",
            "#define SPECIES_IRON_THORNS 0x3E3",
            "#define SPECIES_ALCREMIE_BERRY 0x4AC",
            "#define SPECIES_ROTOM_HEAT 0x2CA",
            "#define SPECIES_ROTOM_WASH 0x2CA",
            "#define SPECIES_COUNT 0x999",
        ]),
        encoding="utf-8",
    )
    (dpe / "items.h").write_text(
        "\n".join([
            "#define ITEM_NONE 0x0",
            "#define ITEM_POTION 0xD",
            "#define ITEM_TINY_MUSHROOM 0x56",
            "#define ITEM_BRIGHT_POWDER 0xB3",
            "#define ITEM_DEEP_SEA_SCALE 0xC4",
            "#define ITEM_BLACK_BELT 0xCF",
            "#define ITEM_ORAN_BERRY 0x8B",
            "#define ITEM_THUNDER_STONE 0x55",
            "#define ITEM_FIGHTING_MEMORY 0x205",
            "#define ITEM_ABILITY_PATCH 0x2C1",
            "#define ITEM_ABILITY_POTION 0x2C2",
            "#define ITEM_BLACK_AUGURITE 0x2C3",
            "#define ITEM_FIRE_GEM 0x250",
            "#define ITEM_ELECTRIC_MEMORY 0x206",
            "#define ITEM_UNREMARKABLE_TEACUP 0x2B0",
            "#define ITEM_BLACK_APRICORN 0x266",
            "#define ITEM_TM51 376",
            "#define ITEM_TM52 377",
            "#define ITEM_HM01_CUT 0x153",
            "#define ITEM_HM06_ROCK_SMASH 0x158",
            "#define ITEM_USE_PARTY_MENU 0x9990",
            "#define ITEMS_COUNT 0x999",
        ]),
        encoding="utf-8",
    )
    (cfru / "species.h").write_text("", encoding="utf-8")
    (cfru / "items.h").write_text("", encoding="utf-8")


def read_tsv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_loaded_manifest(out, species_keys, item_keys, tm_hm_keys, include_private_column=False):
    extra = "\tprivate_path" if include_private_column else ""
    private_value = "\t/home/anton/private/input.gba" if include_private_column else ""
    (out / "species_loaded.tsv").write_text(
        "canonical_key\tdisplay_name\tsource_internal_id\tform_family\tis_loaded\tallowed\tbanned\tmechanic_gated"
        + extra + "\n"
        + "".join(f"{key}\t{key}\t1\t\tyes\tyes\tno\tno{private_value}\n" for key in species_keys),
        encoding="utf-8",
    )
    (out / "items_loaded.tsv").write_text(
        "canonical_key\tdisplay_name\tsource_internal_id\titem_family\tis_loaded\tallowed\tbanned\tmechanic_gated\tis_tm\tis_hm"
        + extra + "\n"
        + "".join(f"{key}\t{key}\t1\t\tyes\tyes\tno\tno\tno\tno{private_value}\n" for key in item_keys),
        encoding="utf-8",
    )
    (out / "tms_hms_loaded.tsv").write_text(
        "canonical_key\tdisplay_name\tsource_internal_id\titem_family\tis_loaded\tallowed\tbanned\tmechanic_gated\tis_tm\tis_hm"
        + extra + "\n"
        + "".join(f"{key}\t{key}\t1\tTM\tyes\tyes\tno\tno\tyes\tno{private_value}\n" for key in tm_hm_keys),
        encoding="utf-8",
    )


def write_tsv_rows(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def local_test_root():
    root = Path(".local/test-randomizer-coverage-auditor")
    root.mkdir(parents=True, exist_ok=True)
    return root


if __name__ == "__main__":
    unittest.main()
