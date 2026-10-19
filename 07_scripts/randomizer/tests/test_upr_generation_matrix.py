"""#727 tests: exact public source + synthetic temp artifacts + mocked subprocesses.

Never launches Java/Gradle/UPR or opens a real ROM, jar, build, save or state.
"""
import base64
import contextlib
import importlib.util
import io
import itertools
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import zlib
from unittest.mock import patch
from urllib.request import urlopen


SCRIPT = Path(__file__).resolve().parents[1] / "upr_generation_matrix.py"
SPEC = importlib.util.spec_from_file_location("upr_generation_matrix", SCRIPT)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)
# Immutable public GitHub text, verified against the exact commit's blob IDs.
# Never inspect the user's local component worktrees or binary artifacts.
SETTINGS_SOURCE = m.read_public_source(m.SETTINGS_SOURCE)
GENERATOR_SOURCE = m.read_public_source()
OVERLAYS, UNSUPPORTED, PROFILES = m.source_model(GENERATOR_SOURCE)


def public_fixture(path, blob):
    with urlopen(m.PUBLIC_SOURCE_URL + path, timeout=30) as response:
        data = response.read()
    if m.public_blob_id(data) != blob:
        raise AssertionError("Exact public fixture mismatch")
    return data.decode("utf-8")


def result(code=0, text="", err=""):
    return subprocess.CompletedProcess([], code, text, err)


def synthetic_payload(data):
    # Only a fixture for mocked API output, never a production serializer.
    return "422" + base64.b64encode(data + bytes(33)).decode()


def decoded_fields(data):
    """Independent field decoder derived from pinned public read API source.

    All serialized booleans/enums are checked, not just the selected ON bits.
    Production does not use this test decoder or construct serialized settings.
    """
    fields = {}
    for name, index, bit in re.findall(r'settings\.set(\w+)\(restoreState\(data\[(\d+)\],\s*(\d+)\)\)', SETTINGS_SOURCE):
        fields[name] = bool(data[int(index)] & (1 << int(bit)))
    for name, enum, index, bits in re.findall(r'settings\.set(\w+)\(restoreEnum\((\w+)\.class,\s*data\[(\d+)\],(.*?)\)\);', SETTINGS_SOURCE, re.S):
        bits = re.sub(r'//[^\n]*', '', bits)
        bits = [int(n) for n in re.findall(r'\d+', bits)]
        declaration = re.search(r'public enum ' + enum + r'\s*\{([^}]+)\}', SETTINGS_SOURCE)[1]
        values = re.findall(r'\b[A-Z][A-Z0-9_]*\b', declaration)
        enabled = [value for value, bit in zip(values, bits) if data[int(index)] & (1 << bit)]
        if len(enabled) != 1:
            raise AssertionError((name, enabled))
        fields[name] = enabled[0]
    fields["RandomizeWildPokemon"] = not bool(data[15] & 1)
    fields["GuaranteedMoveCount"] = ((data[11] & 0xC0) >> 6) + 2
    fields["TrainersLevelModifier"] = int.from_bytes(data[38:39], "big", signed=True) + 28
    fields["CurrentRestrictions"] = int.from_bytes(data[30:34], "little")
    fields["CurrentMiscTweaks"] = int.from_bytes(data[34:38], "big")
    return fields


class MatrixStructureTest(unittest.TestCase):
    def setUp(self):
        self.cases = m.build_matrix(OVERLAYS, UNSUPPORTED, PROFILES)

    def test_inventory_at_exact_pin(self):
        self.assertEqual(159, len(OVERLAYS))
        self.assertEqual({"FVX-SST-001", "FVX-MOVE-006", "FVX-GFX-005", "FVX-GFX-006"}, UNSUPPORTED)
        self.assertEqual(9, len(m.EXCLUDED))
        required = set(OVERLAYS) - UNSUPPORTED - m.EXCLUDED
        self.assertEqual(146, len(required))
        self.assertEqual(required, {c.id for c in self.cases if c.layer == "STRESS"})

    def test_deterministic_order_and_identity(self):
        self.assertEqual(self.cases, m.build_matrix(OVERLAYS, UNSUPPORTED, PROFILES))
        self.assertEqual(303, len(self.cases))
        self.assertEqual(len(self.cases), len({c.id for c in self.cases}))
        self.assertEqual(list(m.SELECTED), [c.id for c in self.cases[:3]])
        self.assertEqual(56, sum(c.layer == "MODE" for c in self.cases))

    def test_all_66_pairs_once(self):
        pairs = [c.families for c in self.cases if c.layer == "PAIR"]
        self.assertEqual(66, len(pairs))
        self.assertEqual(66, len(set(pairs)))
        self.assertEqual(set(itertools.combinations(m.FAMILIES, 2)), set(pairs))

    def test_high_risk_and_maximum(self):
        self.assertEqual(set(m.TRIPLES), {c.families for c in self.cases if c.layer == "TRIPLE"})
        self.assertEqual(12, len(m.TRIPLES))
        self.assertTrue(set(m.MAXIMUM) <= {c.id for c in self.cases})
        secondary = {m.selected_name(c) for c in self.cases if c.secondary}
        self.assertEqual(set(m.MAXIMUM + m.SELECTED[1:]) | m.RISK_IDS, secondary)
        self.assertEqual((0, 1, 677, 20261005658), m.SECONDARY)
        self.assertEqual(20261005658, m.PRIMARY)

    def test_control_approved_safe_derivation_everywhere(self):
        self.assertEqual(m.ITEMS_SAFE, PROFILES["07_ITEMS_SAFE"])
        self.assertNotIn("FVX-ITEM-010", PROFILES["07_ITEMS_SAFE"])
        self.assertEqual(PROFILES["07_ITEMS_FULL"][:-1], m.ITEMS_SAFE)
        for case in self.cases:
            if case.classification != "DIAGNOSTIC":
                self.assertNotEqual("07_ITEMS_FULL", case.id)
                self.assertFalse(set(case.overlays) & m.EXCLUDED)
                state = m.effective(case, OVERLAYS)
                if case.id not in m.PICKUP_APPROVED_IDS:
                    self.assertNotIn("PickupItemsMod", state)  # safe families stay unchanged
                if "ITEMS_SHOPS" in case.families:
                    self.assertTrue(set(m.ITEMS_SAFE) <= set(case.overlays))
        source = m.bridge_source(self.cases, OVERLAYS)
        self.assertIn("s.getPickupItemsMod() != Settings.PickupItemsMod.UNCHANGED", source)
        self.assertNotIn('"07_ITEMS_FULL"', source)
        self.assertIn("s.setPickupItemsMod(Settings.PickupItemsMod.RANDOM)", source)
        self.assertIn(".contains(id)", source)

    def test_exact_target_exclusion_reasons(self):
        self.assertEqual({
            "FVX-TRAIT-025": "OWNERSHIP_WITNESS_V1_REQUIRED",
            "FVX-MISC-011": "REDUNDANT_CFRU_NATIVE_REUSABLE_TMS",
        }, m.TARGET_EXCLUSIONS)
        self.assertEqual({"SOURCE_OVERLAY_IDS": 159, "GENERATOR_UNSUPPORTED": 4,
                          "TARGET_EXCLUDED": 9, "REQUIRED_OVERLAY_CASES": 146},
                         m.inventory_counts(OVERLAYS, UNSUPPORTED))

    def test_safe_bundles_exact_source_semantics(self):
        self.assertEqual(tuple(f"FVX-TRAIT-{n:03}" for n in (1, 6, 8, 13, 14, 15, 16, 22)),
                         PROFILES["01_TRAITS_SAFE"])
        state = m.effective(m.Intent("TRAITS_SAFE", "FULL", PROFILES["01_TRAITS_SAFE"]), OVERLAYS)
        self.assertEqual({
            "BaseStatisticsMod": "Settings.BaseStatisticsMod.RANDOM",
            "SpeciesTypesMod": "Settings.SpeciesTypesMod.COMPLETELY_RANDOM",
            "AbilitiesMod": "Settings.AbilitiesMod.RANDOMIZE",
            "BanTrappingAbilities": "true", "BanNegativeAbilities": "true",
            "BanBadAbilities": "true", "EvolutionsMod": "Settings.EvolutionsMod.RANDOM",
            "EvosForceChange": "true",
        }, state)
        self.assertEqual(("FVX-GFX-001", "FVX-GFX-003"), PROFILES["09_GRAPHICS_PALETTES_SAFE"])
        state = m.effective(m.Intent("GRAPHICS_SAFE", "FULL", PROFILES["09_GRAPHICS_PALETTES_SAFE"]), OVERLAYS)
        self.assertEqual({"PokemonPalettesMod": "Settings.PokemonPalettesMod.RANDOM",
                          "PokemonPalettesFollowEvolutions": "true"}, state)
        self.assertEqual(tuple(f"FVX-MISC-{n:03}" for n in (1, 3, 5, 6, 7, 8, 9)),
                         PROFILES["10_MISC_SAFE"])
        state = m.effective(m.Intent("MISC_SAFE", "FULL", PROFILES["10_MISC_SAFE"]), OVERLAYS)
        self.assertEqual({"MiscTweak": " | ".join(sorted("MiscTweak." + name for name in (
            "FASTEST_TEXT", "RANDOMIZE_PC_POTION", "FAST_EGG_HATCHING", "LOWER_CASE_POKEMON_NAMES",
            "RANDOMIZE_CATCHING_TUTORIAL", "BAN_LUCKY_EGG", "BALANCE_STATIC_LEVELS")))}, state)

    def test_full_pair_triple_max_transitive_safety_and_single_coverage(self):
        originals = {"01_TRAITS_FULL", "09_GRAPHICS_PALETTES", "10_MISC_TWEAKS"}
        self.assertFalse(originals & {c.id for c in self.cases})
        for case in self.cases:
            if case.layer in {"FULL", "PAIR", "TRIPLE", "MAX"}:
                self.assertFalse(set(case.overlays) & (m.EXCLUDED | UNSUPPORTED), case.id)
                state = m.effective(case, OVERLAYS)
                for key in ("MakeEvolutionsEasier", "RemoveTimeBasedEvolutions",
                            "PokemonPalettesFollowTypes", "PokemonPalettesShinyFromNormal"):
                    self.assertNotEqual("true", state.get(key), case.id)
                self.assertNotIn("MiscTweak.REUSABLE_TMS", state.get("MiscTweak", ""), case.id)
                for family, profile in (("TRAITS", "01_TRAITS_SAFE"),
                                        ("GRAPHICS_PALETTES", "09_GRAPHICS_PALETTES_SAFE"),
                                        ("MISC", "10_MISC_SAFE")):
                    if family in case.families:
                        self.assertTrue(set(PROFILES[profile]) <= set(case.overlays), case.id)
        # Supported suboptions omitted from family stress still run individually.
        leaves = {c.id for c in self.cases if c.layer == "STRESS"}
        for original in originals:
            self.assertTrue((set(PROFILES[original]) - m.EXCLUDED - UNSUPPORTED) <= leaves)
        for name in ("FVX-MISC-002", "FVX-MISC-004", "FVX-MISC-010", "FVX-MISC-012"):
            self.assertIn(name, leaves)
            self.assertNotIn(name, PROFILES["10_MISC_SAFE"])

    def test_transitive_exclusion_injected_into_each_family_fails_closed(self):
        for profile in m.FULL:
            for excluded in m.EXCLUDED | UNSUPPORTED:
                altered = dict(PROFILES, **{profile: PROFILES[profile] + (excluded,)})
                with self.subTest(profile=profile, excluded=excluded), self.assertRaises(m.MatrixError):
                    m.build_matrix(OVERLAYS, UNSUPPORTED, altered)

    def test_max_safe_composition_and_world_unchanged(self):
        by_id = {c.id: c for c in self.cases}
        # Exact original MAX_SAFE_WORLD source sequence, including unchanged Items SAFE.
        expected_world = tuple(
            [f"FVX-SST-{n:03}" for n in (2, 6, 7, 8, 11, 13, 14, 15)]
            + [f"FVX-FOE-{n:03}" for n in (1, 2, 3, 4, 13, 14)]
            + [f"FVX-WILD-{n:03}" for n in range(1, 13)]
            + [f"FVX-TM-{n:03}" for n in range(1, 16)]
            + [f"FVX-ITEM-{n:03}" for n in (2, 4, 6, 7, 8, 9)])
        self.assertEqual(expected_world, by_id["MAX_SAFE_WORLD"].overlays)
        gen = ("MODE-GEN-LIMIT-1-9-NO-RELATIVES", "MODE-ALLOW-REGIONAL-FORMS",
               "MODE-GEN-LIMIT-1-9-NO-MEGAS", "MODE-GEN-LIMIT-1-9-NO-GMAX")
        expected_data = tuple(dict.fromkeys(gen + PROFILES["01_TRAITS_SAFE"]
                                           + PROFILES["03_MOVES_MOVESETS_FULL"]
                                           + ("FVX-TRAIT-016", "FVX-TRAIT-022")))
        self.assertEqual(expected_data, by_id["MAX_SAFE_DATA"].overlays)
        expected_combined = tuple(dict.fromkeys(expected_data + expected_world
                                  + PROFILES["09_GRAPHICS_PALETTES_SAFE"]
                                  + PROFILES["10_MISC_SAFE"] + PROFILES["11_SPECIAL_WILD"]))
        self.assertEqual(expected_combined, by_id["MAX_SAFE_COMBINED"].overlays)

    def test_derived_structure_counts(self):
        counts = {layer: sum(c.layer == layer for c in self.cases)
                  for layer in ("ACCEPTANCE", "STRESS", "MODE", "FULL", "PAIR", "TRIPLE", "MAX", "RISK", "DIAGNOSTIC")}
        self.assertEqual(dict(zip(counts, (3, 146, 56, 12, 66, 12, 5, 2, 1))), counts)
        self.assertEqual(sum(counts.values()), len(self.cases))

    def test_source_drift_fails_closed(self):
        source = GENERATOR_SOURCE
        with self.assertRaises(m.MatrixError):
            m.source_model(source.replace('"FVX-ITEM-008", "FVX-ITEM-009", "FVX-ITEM-010"', '"FVX-ITEM-009", "FVX-ITEM-010"'))

    def test_source_inventory_cardinality_drift_fails_closed(self):
        source = GENERATOR_SOURCE
        for altered in (source.replace('"FVX-GEN-003"', '"FVX-GEN-002"'),
                        source.replace('return Collections.unmodifiableMap(overlays);',
                                       'overlays.put("NEW-UNREVIEWED", s -> s.setRaceMode(true));\n'
                                       'return Collections.unmodifiableMap(overlays);')):
            with self.assertRaises(m.MatrixError):
                m.source_model(altered)

    def test_no_mutually_exclusive_intent_modes(self):
        for case in self.cases:
            m.effective(case, OVERLAYS)
        conflicting = m.Intent("CONFLICT", "MODE", ("MODE-FOE-RANDOM", "MODE-FOE-TYPE-THEMED"))
        with self.assertRaises(m.MatrixError):
            m.effective(conflicting, OVERLAYS)
        for owner in ("TrainersMod", "StaticPokemonMod", "StartersMod", "WildPokemonZoneMod", "TypeEffectivenessMod"):
            for case in self.cases:
                state = m.effective(case, OVERLAYS)
                if owner in state:
                    self.assertEqual(1, state[owner].count("Settings."))

    def test_settings_api_calls_exist_in_pinned_source(self):
        source = m.bridge_source(self.cases, OVERLAYS)
        setters = set(re.findall(r's\.set(\w+)\(', source))
        public_setters = set(re.findall(r'public (?:void|Settings) set(\w+)\(', SETTINGS_SOURCE))
        self.assertFalse(setters - public_setters)
        self.assertIn("SettingsProfileGenerator.invoke", source)
        self.assertIn("Settings.fromString", source)
        self.assertIn("Settings.readFromFileFormat", source)
        self.assertIn("restored.toString()", source)
        # Split methods avoid the JVM 64KiB single-method limit.
        self.assertEqual(len(self.cases), source.count("static void case"))


class ClosureTest(unittest.TestCase):
    def test_owner_rules_for_each_child_overlay(self):
        requirements = {
            "FVX-TRAIT-002": ("BaseStatisticsMod", "RANDOM"),
            "FVX-TRAIT-003": ("BaseStatsFollowEvolutions", "true"),
            "FVX-TRAIT-007": ("SpeciesTypesMod", "COMPLETELY_RANDOM"),
            "FVX-TRAIT-013": ("AbilitiesMod", "RANDOMIZE"),
            "FVX-TRAIT-018": ("EvolutionsMod", "RANDOM"),
            "FVX-TRAIT-026": ("ChangeImpossibleEvolutions", "true"),
            "FVX-TRAIT-028": ("StandardizeEXPCurves", "true"),
            "FVX-SST-005": ("StartersMod", "COMPLETELY_RANDOM"),
            "FVX-SST-008": ("RandomizeStartersHeldItems", "true"),
            "FVX-SST-013": ("StaticPokemonMod", "COMPLETELY_RANDOM"),
            "FVX-SST-015": ("InGameTradesMod", "RANDOMIZE_GIVEN_AND_REQUESTED"),
            "FVX-MOVE-010": ("MovesetsMod", "COMPLETELY_RANDOM"),
            "FVX-FOE-002": ("TrainersMod", "RANDOM"),
            "FVX-FOE-005": ("TrainersMod", "RANDOM"),
            "FVX-FOE-008": ("TrainersMod", "RANDOM"),
            "FVX-FOE-009": ("TrainersMod", "TYPE_THEMED"),
            "FVX-FOE-012": ("StartersMod", "COMPLETELY_RANDOM"),
            "MODE-TRAINER-CLASS-SPRITE-SYNC": ("RandomizeTrainerClassNames", "true"),
            "FVX-WILD-009": ("RandomizeWildPokemonHeldItems", "true"),
            "FVX-WILD-004": ("RandomizeWildPokemon", "true"),
            "FVX-TM-003": ("TmsMod", "RANDOM"),
            "FVX-TM-007": ("TmsHmsCompatibilityMod", "COMPLETELY_RANDOM"),
            "FVX-TM-011": ("MoveTutorMovesMod", "RANDOM"),
            "FVX-TM-015": ("MoveTutorsCompatibilityMod", "COMPLETELY_RANDOM"),
            "FVX-ITEM-004": ("FieldItemsMod", "RANDOM"),
            "FVX-ITEM-008": ("ShopItemsMod", "RANDOM"),
            "FVX-GFX-004": ("PokemonPalettesMod", "RANDOM"),
            "FVX-TYPE-002": ("TypeEffectivenessMod", "INVERSE"),
            "MODE-ALLOW-REGIONAL-FORMS": ("CurrentRestrictions", "new GenRestrictions(0x3FE)"),
            "FVX-SPECIAL-WILD-001": ("RandomizeWildPokemon", "true"),
        }
        for overlay, (key, value) in requirements.items():
            with self.subTest(overlay=overlay):
                actual = m.effective(m.Intent(overlay, "STRESS", (overlay,)), OVERLAYS)[key]
                self.assertTrue(actual == value or actual.endswith("." + value), actual)

    def test_preserve_explicit_owner_and_idempotence(self):
        state = {"TrainersMod": "Settings.TrainersMod.TYPE_THEMED", "BetterBossTrainerMovesets": "true"}
        self.assertEqual(state, m.closure(state))
        for overlay in set(OVERLAYS) - UNSUPPORTED - m.EXCLUDED:
            s = m.effective(m.Intent(overlay, "STRESS", (overlay,)), OVERLAYS)
            self.assertEqual(s, m.closure(s))

    def test_misc_bits_union_not_last_writer(self):
        case = m.Intent("MISC", "FULL", tuple(n for n in PROFILES["10_MISC_TWEAKS"] if n not in m.EXCLUDED))
        bits = m.effective(case, OVERLAYS)["MiscTweak"].split(" | ")
        self.assertEqual(11, len(bits))
        self.assertIn("MiscTweak.FASTEST_TEXT", bits)


class IdentityAndDedupTest(unittest.TestCase):
    def test_mocked_settings_adapter_and_normalizer(self):
        cases = [m.Intent("IRONMON_NATDEX", "ACCEPTANCE"), m.Intent("CASUAL_NATDEX", "ACCEPTANCE")]
        payloads = [m.IRONMON, synthetic_payload(m.CASUAL_BYTES)]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)

            def execute(args, cwd, timeout=600):
                self.assertEqual(temp, cwd)
                self.assertEqual(["java", "--class-path", "synthetic.jar"], args[:3])
                for i, payload in enumerate(payloads):
                    (temp / f"{i}.settings").write_text(payload)
                    (temp / f"{i}.rnqs").write_text("synthetic settings")
                    (temp / f"{i}.normalization").write_text("NONE")
                return result()

            with patch.object(m, "command", side_effect=execute) as command:
                self.assertEqual(payloads, m.generate_settings(cases, OVERLAYS, Path("synthetic.jar"), temp))
                self.assertEqual((payloads, {}, {}), m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, payloads, OVERLAYS))
                self.assertEqual(2, command.call_count)
            self.assertTrue((temp / "MatrixSettings.java").is_file())
            self.assertIn("s.tweakForRom", (temp / "MatrixNormalize.java").read_text())
            self.assertIn("usesCfruDpeRandomPoolPolicy", m.NORMALIZER)

    def test_adapter_failures_and_normalization_identity_drift_stop(self):
        cases = [m.Intent("IRONMON_NATDEX", "ACCEPTANCE")]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            with patch.object(m, "command", return_value=result(1, "/fictional/private path")):
                with self.assertRaises(m.MatrixError):
                    m.generate_settings(cases, OVERLAYS, Path("synthetic.jar"), temp)
                with self.assertRaises(m.MatrixError):
                    m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, [m.IRONMON], OVERLAYS)
            (temp / "0.settings").write_text(synthetic_payload(bytes(67)))
            (temp / "0.normalization").write_text("NONE")
            with patch.object(m, "command", return_value=result()):
                with self.assertRaises(m.MatrixError):
                    m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, [m.IRONMON], OVERLAYS)

    def test_exact_casual_all_serialized_boolean_and_enum_fields(self):
        fields = decoded_fields(m.CASUAL_BYTES)
        # All flags default OFF. All modes default UNCHANGED or NONE, with
        # LEGENDARIES/ENCOUNTER_SET as explicit inactive selector defaults.
        for key, actual in fields.items():
            if key in m.CASUAL and key != "CurrentRestrictions":
                expected = m.CASUAL[key]
                expected = expected == "true" if isinstance(actual, bool) else expected.split(".")[-1] if isinstance(actual, str) else int(expected)
            elif isinstance(actual, bool):
                expected = False
            elif isinstance(actual, str):
                expected = "LEGENDARIES" if key == "ExpCurveMod" else "NONE" if key in {"StartersTypeMod", "WildPokemonTypeMod", "WildPokemonEvolutionMod"} else "UNCHANGED"
            else:
                expected = {"GuaranteedMoveCount": 2, "TrainersLevelModifier": 0,
                            "CurrentRestrictions": 0x3FE, "CurrentMiscTweaks": 8}[key]
            self.assertEqual(expected, actual, key)

    def test_accepted_ironmon_identity_and_selected_deltas(self):
        fields = decoded_fields(m.settings_data(m.IRONMON))
        self.assertEqual("RANDOM", fields["BaseStatisticsMod"])
        self.assertEqual("RANDOMIZE", fields["AbilitiesMod"])
        self.assertEqual("COMPLETELY_RANDOM", fields["MovesetsMod"])
        self.assertEqual(4, fields["GuaranteedMoveCount"])
        self.assertEqual(50, fields["TrainersLevelModifier"])
        self.assertTrue(fields["TrainersLevelModified"])
        self.assertTrue(fields["RaceMode"])
        self.assertTrue(fields["BlockWildLegendaries"])
        self.assertTrue(fields["BlockBrokenMovesetMoves"])
        for key in ("BanTrappingAbilities", "BanNegativeAbilities", "BanBadAbilities"):
            self.assertTrue(fields[key])
        for key in ("AllowWonderGuard", "BaseStatsFollowEvolutions", "AbilitiesFollowEvolutions", "EvolutionMovesForAll", "RandomizeIntroMon", "BanIrregularAltFormes"):
            self.assertFalse(fields[key])
        self.assertEqual("UNCHANGED", fields["PickupItemsMod"])
        self.assertEqual("UNCHANGED", fields["SpeciesTypesMod"])
        self.assertEqual(0x3FE, fields["CurrentRestrictions"])
        self.assertEqual(8, fields["CurrentMiscTweaks"])

    def test_identity_mismatch_clear_stop(self):
        cases = [m.Intent("IRONMON_NATDEX", "ACCEPTANCE"), m.Intent("CASUAL_NATDEX", "ACCEPTANCE")]
        m.verify_selected_payloads(cases, [m.IRONMON, synthetic_payload(m.CASUAL_BYTES)])
        for i in (0, 1):
            payloads = [m.IRONMON, synthetic_payload(m.CASUAL_BYTES)]
            payloads[i] = synthetic_payload(bytes(67))
            with self.assertRaises(m.MatrixError):
                m.verify_selected_payloads(cases, payloads)

    def test_dedup_uses_exact_payload_preserves_all_aliases(self):
        cases = [m.Intent("A", "STRESS"), m.Intent("B", "MODE"), m.Intent("C", "MAX", replay=True)]
        with tempfile.TemporaryDirectory() as directory:
            groups = m.deduplicate(cases, ["same", "same", "different"], Path(directory))
            self.assertEqual(2, len(groups))
            self.assertEqual(["A", "B"], [c.id for c in groups[0].aliases])
            self.assertEqual(["C"], [c.id for c in groups[1].aliases])


class NormalizationAccountingTest(unittest.TestCase):
    """CONTROL-disposed C/I delta; only synthetic API witness/payload fixtures."""

    def setUp(self):
        mock = patch.object(m, "input_digest", return_value=b"synthetic input")
        mock.start()
        self.addCleanup(mock.stop)

    def selected(self, name):
        before = m.IRONMON if name == "IRONMON_NATDEX" else synthetic_payload(m.CASUAL_BYTES)
        return [m.Intent(name, "ACCEPTANCE")], [before]

    def adapted(self, payload, extra=None):
        data = bytearray(m.settings_data(payload))
        data[30:34] = b"\xff" * 4
        data[65] &= ~8
        if extra is not None:
            index, bit = extra
            data[index] ^= bit
        data[-8:-4] = zlib.crc32(data[:-8]).to_bytes(4, "big")
        return "422" + base64.b64encode(data).decode()

    def witness(self, **changes):
        fields = [m.GEN_NORMALIZATION, "true", "true", "false", "true", "1022", "false", "-1"]
        for index, value in changes.items():
            fields[int(index)] = value
        return "\t".join(fields)

    def verify(self, name, marker=True, extra=None):
        cases, before = self.selected(name)
        events = {0: m.parse_normalization_witness(self.witness())} if marker else {}
        m.verify_selected_normalized_payloads(cases, before, [self.adapted(before[0], extra)], events)

    def test_pre_rom_casual_exact_identity(self):
        m.verify_selected_payloads(*self.selected("CASUAL_NATDEX"))

    def test_pre_rom_ironmon_exact_identity(self):
        m.verify_selected_payloads(*self.selected("IRONMON_NATDEX"))

    def test_pre_rom_drift_still_stops_even_with_marker(self):
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            cases, before = self.selected(name)
            data = bytearray(m.settings_data(before[0]))
            data[0] ^= 1
            before[0] = "422" + base64.b64encode(data).decode()
            with self.assertRaises(m.MatrixError):
                m.verify_selected_normalized_payloads(cases, before, [self.adapted(before[0])], {0: 1022})

    def test_post_rom_casual_exact_delta_with_witness(self):
        self.verify("CASUAL_NATDEX")

    def test_post_rom_ironmon_exact_delta_with_witness(self):
        self.verify("IRONMON_NATDEX")

    def test_identical_delta_without_marker_stops(self):
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            with self.subTest(name=name), self.assertRaises(m.MatrixError):
                self.verify(name, marker=False)

    def test_non_cfru_policy_marker_rejected(self):
        with self.assertRaises(m.MatrixError):
            m.parse_normalization_witness(self.witness(**{"2": "false"}))

    def test_valid_rom_marker_rejected(self):
        with self.assertRaises(m.MatrixError):
            m.parse_normalization_witness(self.witness(**{"3": "true"}))

    def test_wrong_handler_marker_rejected(self):
        with self.assertRaises(m.MatrixError):
            m.parse_normalization_witness(self.witness(**{"1": "false"}))

    def test_every_other_serialized_profile_field_drift_stops(self):
        # Exhaust every bit in all 67 settings bytes (starter/trainer/wild,
        # items, misc, inactive flags, mechanics, etc.), beyond the two deltas.
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            for index in range(67):
                if 30 <= index < 34:
                    continue
                for bit in (1, 2, 4, 8, 16, 32, 64, 128):
                    if index == 65 and bit == 8:
                        continue
                    with self.subTest(name=name, index=index, bit=bit), self.assertRaises(m.MatrixError):
                        self.verify(name, extra=(index, bit))

    def test_misc_fastest_text_removal_stops(self):
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            with self.assertRaises(m.MatrixError):
                self.verify(name, extra=(37, 8))  # big-endian CurrentMiscTweaks=8

    def test_pickup_change_stops(self):
        # Derive the Pickup field offset from the pinned public decoder.
        match = re.search(r'settings.setPickupItemsMod\(restoreEnum\([^;]+data\[(\d+)\]', SETTINGS_SOURCE)
        self.assertIsNotNone(match)
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            with self.assertRaises(m.MatrixError):
                self.verify(name, extra=(int(match[1]), 1))

    def test_extra_restriction_or_limit_delta_stops(self):
        for mutation in ((30, 1), (65, 8)):
            with self.assertRaises(m.MatrixError):
                self.verify("CASUAL_NATDEX", extra=mutation)

    def test_post_normalization_metadata_and_checksum_drift_stop(self):
        cases, before = self.selected("IRONMON_NATDEX")
        after = self.adapted(before[0])
        for index in (67, 68, -8, -4):
            data = bytearray(m.settings_data(after))
            data[index] ^= 1
            changed = "422" + base64.b64encode(data).decode()
            with self.subTest(index=index), self.assertRaises(m.MatrixError):
                m.verify_selected_normalized_payloads(cases, before, [changed], {0: 1022})

    def test_incomplete_accounting_stops(self):
        cases, before = self.selected("CASUAL_NATDEX")
        with self.assertRaises(m.MatrixError):
            m.verify_selected_normalized_payloads(cases, before, [], {})

    def test_normalization_stop_cleans_runtime_workspace(self):
        cases, before = self.selected("CASUAL_NATDEX")
        directories = []
        def execute(args, cwd, timeout=600):
            directories.append(cwd)
            (cwd / "0.settings").write_text(self.adapted(before[0], (37, 8)))
            (cwd / "0.normalization").write_text(self.witness())
            return result(text="Private.gba /fictional/private DD88761C")
        output = io.StringIO()
        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=before), patch.object(m, "command", side_effect=execute), patch.object(m, "run_case") as run, patch("builtins.input", return_value="/fictional/private/Private.gba"), contextlib.redirect_stdout(output):
            self.assertEqual(1, m.main([]))
        run.assert_not_called()
        self.assertTrue(directories)
        self.assertTrue(all(not d.exists() for d in directories))
        for private in ("Private.gba", "/fictional", "DD88761C"):
            self.assertNotIn(private, output.getvalue())

    def test_unchanged_post_rom_selected_payloads_pass(self):
        for name in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            cases, before = self.selected(name)
            m.verify_selected_normalized_payloads(cases, before, before, {})

    def test_marker_without_actual_transition_stops(self):
        cases, before = self.selected("CASUAL_NATDEX")
        with self.assertRaises(m.MatrixError):
            m.verify_selected_normalized_payloads(cases, before, before, {0: 1022})

    def test_report_public_marker_and_count_only(self):
        report = io.StringIO()
        with contextlib.redirect_stdout(report):
            m.print_report([], [], [], m.inventory_counts(OVERLAYS, UNSUPPORTED), "NOT_RUN", adaptations={0: 1022, 1: 1023})
        text = report.getvalue()
        self.assertIn("UPR target-normalized adaptations: " + m.GEN_NORMALIZATION, text)
        self.assertIn("Gen-limit intents normalized by target: 2", text)
        self.assertIn("effective Gen-limit execution not claimed", text)
        for private in ("1022", "1023", "DD88761C", ".gba", "/fictional", "CRC", "hash"):
            self.assertNotIn(private, text)

    def test_gen_limit_alias_survives_effective_deduplication(self):
        cases, before = self.selected("CASUAL_NATDEX")
        cases.append(m.Intent("GEN_LIMIT_RELATIVES", "MODE"))
        relatives = bytearray(m.settings_data(before[0]))
        relatives[30:34] = (0x3FF).to_bytes(4, "little")
        before.append("422" + base64.b64encode(relatives).decode())
        after = [self.adapted(p) for p in before]
        m.verify_selected_normalized_payloads(cases, before, after, {0: 1022, 1: 1023})
        with tempfile.TemporaryDirectory() as directory:
            groups = m.deduplicate(cases, after, Path(directory))
            self.assertEqual(1, len(groups))
            self.assertEqual([c.id for c in cases], [c.id for c in groups[0].aliases])

    def test_runtime_adapter_api_guards_and_marker(self):
        for source in ("instanceof Gen3RomHandler", "usesCfruDpeRandomPoolPolicy()",
                       "handler.isRomValid(null)", "s.isLimitPokemon()", "s.getCurrentRestrictions().toInt()",
                       "policy && !valid && beforeLimit && beforeRestrictions >= 0",
                       "!afterLimit && s.getCurrentRestrictions() == null && afterRestrictions == -1", m.GEN_NORMALIZATION):
            self.assertIn(source, m.NORMALIZER)
        self.assertLess(m.NORMALIZER.index("boolean beforeLimit"), m.NORMALIZER.index("s.tweakForRom(handler)"))
        self.assertLess(m.NORMALIZER.index("s.tweakForRom(handler)"), m.NORMALIZER.index("boolean afterLimit"))
        # Java's actual tab escape must reach the generated source.
        self.assertIn('"\\ttrue\\t"', m.NORMALIZER)

    def test_mocked_adapter_witness_and_cleanup_after_stop(self):
        cases, before = self.selected("CASUAL_NATDEX")
        for witness in (self.witness(), self.witness(**{"2": "false"}), "NONE",
                        "/fictional/private/Secret.gba DD88761C"):
            directory = None
            with tempfile.TemporaryDirectory() as name:
                directory = Path(name)
                def execute(args, cwd, timeout=600):
                    (cwd / "0.settings").write_text(self.adapted(before[0]))
                    (cwd / "0.rnqs").write_text("synthetic")
                    (cwd / "0.normalization").write_text(witness)
                    # The instrumented adapter suppresses library output on success.
                    return result()
                with patch.object(m, "command", side_effect=execute):
                    if witness == self.witness():
                        after, events, blocked = m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/Private.gba", directory, before, OVERLAYS)
                        self.assertEqual({0: 1022}, events)
                        self.assertEqual([self.adapted(before[0])], after)
                    else:
                        with self.assertRaises(m.MatrixError) as caught:
                            m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/Private.gba", directory, before, OVERLAYS)
                        self.assertNotIn("Secret.gba", str(caught.exception))
                        self.assertNotIn("DD88761C", str(caught.exception))
            self.assertFalse(directory.exists())  # adapter, witness, settings all removed


class ExecutionTest(unittest.TestCase):
    def setUp(self):
        self.digest_mock = patch.object(m, "input_digest", return_value=b"synthetic input")
        self.digest_mock.start()
        self.addCleanup(self.digest_mock.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.settings = self.directory / "synthetic.rnqs"
        self.settings.write_text("synthetic")
        self.group = m.Group("synthetic", self.settings, [m.Intent("CASE", "STRESS", replay=True)])
        # Fictional path strings only; never stat/open these inputs or jar.
        self.rom = "/fictional/private/Personal Name.gba"
        self.jar = Path("/fictional/tool/UPR.jar")

    def executor(self, generate=None, reopen=None, mismatch=False, identity_states=None, identity_result=None):
        calls = []
        states = iter(identity_states or [(True, True, True), (True, True, True)])

        def execute(args, cwd, timeout=600):
            calls.append((args, Path(cwd)))
            self.assertTrue(Path(cwd).is_relative_to(self.directory))
            self.assertEqual("java", args[0])
            if args[1] == "--class-path":
                adapter = Path(args[3])
                self.assertEqual(Path(cwd) / "MatrixReopen.java", adapter)
                self.assertEqual(m.REOPEN_IDENTITY, adapter.read_text())
                output = Path(args[4])
                self.assertTrue(output.is_relative_to(Path(cwd)))
                self.assertTrue(output.is_file())
                if identity_result is not None:
                    return identity_result
                opened, gen3_handler, cfru_dpe_policy = next(states)
                return result(text="Supported CFRU/DPE output identity verified.") if opened and gen3_handler and cfru_dpe_policy else result(1)
            if args[3] == "cli":
                output = Path(args[args.index("-o") + 1])
                self.assertTrue(output.is_relative_to(Path(cwd)))
                output.write_bytes(b"second" if mismatch and output.name == "replay.gba" else b"synthetic bytes")
                # Ensure raw sidecars are also removed by the enclosing finally.
                output.with_suffix(".log").write_text("private raw log")
                return generate or result(text="Randomized successfully!")
            if args[3] == "loaded-manifest":
                output = Path(args[args.index("-o") + 1])
                self.assertTrue(output.is_relative_to(Path(cwd)))
                output.mkdir()
                (output / "synthetic.tsv").write_text("synthetic manifest")
                return reopen or result(text="Wrote sanitized loaded manifests.")
            self.fail("Unexpected subprocess")
        return calls, execute

    def assert_clean(self):
        self.assertEqual([self.settings], list(self.directory.iterdir()))

    def test_generate_reopen_replay_match_and_cleanup(self):
        calls, execute = self.executor()
        with patch.object(m, "command", side_effect=execute):
            out = m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, True)
        self.assertTrue(out.passed)
        self.assertEqual("PASS", out.replay)
        self.assertEqual(6, len(calls))
        self.assertEqual(["cli", "identity", "loaded-manifest"] * 2,
                         ["identity" if a[1] == "--class-path" else a[3] for a, _ in calls])
        self.assertEqual([m.PRIMARY, m.PRIMARY], [int(a[a.index("-z") + 1]) for a, _ in calls if a[3] == "cli"])
        self.assert_clean()

    def test_generation_failure_partial_success_rejected_and_cleanup(self):
        failures = [result(1, "Randomized successfully!"), result(text="no success marker"),
                    result(text="Randomized successfully!\nERROR: failure"),
                    result(text="Randomized successfully!\nRandomizationException: private details")]
        for failure in failures:
            calls, execute = self.executor(generate=failure)
            with patch.object(m, "command", side_effect=execute):
                out = m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, True)
            self.assertFalse(out.passed)
            self.assertEqual("FAIL", out.generate)
            self.assertEqual(1, len(calls))
            self.assert_clean()

    def test_missing_or_empty_output_fails(self):
        for empty in (False, True):
            def execute(args, cwd, timeout=600):
                if empty:
                    Path(args[args.index("-o") + 1]).touch()
                return result(text="Randomized successfully!")
            with patch.object(m, "command", side_effect=execute):
                out = m.attempt(self.group, 0, self.rom, self.jar, self.directory, False)
            self.assertEqual("FAIL", out.generate)
            self.assert_clean()

    def test_reopen_failure_and_missing_success(self):
        for failure in (result(1, "ERROR: cannot load"), result(text="not reopened")):
            calls, execute = self.executor(reopen=failure)
            with patch.object(m, "command", side_effect=execute):
                out = m.attempt(self.group, 1, self.rom, self.jar, self.directory, True)
            self.assertEqual("PASS", out.generate)
            self.assertEqual("FAIL", out.reopen)
            self.assertEqual("NOT_APPLICABLE", out.replay)
            self.assertEqual(3, len(calls))
            self.assert_clean()

    def test_cfru_dpe_identity_pass_then_manifest_pass(self):
        calls, execute = self.executor(identity_states=[(True, True, True)])
        with patch.object(m, "command", side_effect=execute):
            out = m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, False)
        self.assertTrue(out.passed)
        self.assertEqual("PASS", out.reopen)
        self.assertEqual(["cli", "identity", "loaded-manifest"],
                         ["identity" if a[1] == "--class-path" else a[3] for a, _ in calls])
        self.assert_clean()

    def test_openable_generic_gen3_identity_fails_closed(self):
        calls, execute = self.executor(identity_states=[(True, True, False)])
        with patch.object(m, "command", side_effect=execute):
            out = m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, True)
        self.assertEqual("PASS", out.generate)
        self.assertEqual("FAIL", out.reopen)
        self.assertEqual("ReopenIdentityFailure", out.error_class)
        self.assertEqual("Output was not recognized as the supported CFRU/DPE profile.", out.message)
        self.assertFalse(out.passed)
        self.assertEqual(2, len(calls))  # no manifest/replay after failed identity
        self.assert_clean()

    def test_identity_open_failure_and_wrong_handler(self):
        for state in ((False, False, False), (True, False, False)):
            with self.subTest(state=state):
                calls, execute = self.executor(identity_states=[state])
                with patch.object(m, "command", side_effect=execute):
                    out = m.attempt(self.group, 1, self.rom, self.jar, self.directory, False)
                self.assertEqual("PASS", out.generate)
                self.assertEqual("FAIL", out.reopen)
                self.assertEqual("ReopenIdentityFailure", out.error_class)
                self.assertEqual(2, len(calls))
                self.assert_clean()

    def test_identity_nonzero_and_private_java_details_are_discarded(self):
        private = 'Private Filename.gba /fictional/private/Secret.gba ' + self.rom
        calls, execute = self.executor(identity_result=result(1, private, "IllegalStateException: " + private))
        with patch.object(m, "command", side_effect=execute):
            out = m.attempt(self.group, 1, self.rom, self.jar, self.directory, False)
        self.assertEqual("PASS", out.generate)
        self.assertEqual("FAIL", out.reopen)
        self.assertEqual("ReopenIdentityFailure", out.error_class)
        report = io.StringIO()
        with contextlib.redirect_stdout(report):
            m.print_report(self.group.aliases, [self.group], [(self.group, 1, out)], m.inventory_counts(OVERLAYS, UNSUPPORTED), "FAIL")
        for marker in (private, "Private Filename", "/fictional", "Secret.gba", "IllegalStateException"):
            self.assertNotIn(marker, str(out))
            self.assertNotIn(marker, report.getvalue())
        self.assertEqual(2, len(calls))
        self.assert_clean()

    def test_identity_missing_marker_or_partial_success_rejected(self):
        for response in (result(), result(text="Supported CFRU/DPE output identity verified.\nERROR: failure"),
                         result(1, "Supported CFRU/DPE output identity verified.")):
            _, execute = self.executor(identity_result=response)
            with patch.object(m, "command", side_effect=execute):
                out = m.attempt(self.group, 1, self.rom, self.jar, self.directory, False)
            self.assertEqual("FAIL", out.reopen)
            self.assertEqual("ReopenIdentityFailure", out.error_class)
            self.assert_clean()

    def test_replay_identity_failure_before_manifest_or_byte_comparison(self):
        calls, execute = self.executor(identity_states=[(True, True, True), (True, True, False)])
        with patch.object(m, "command", side_effect=execute), patch.object(m, "same_bytes") as compare:
            out = m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, True)
        self.assertEqual("PASS", out.generate)
        self.assertEqual("FAIL", out.reopen)
        self.assertEqual("FAIL", out.replay)
        self.assertEqual("ReopenIdentityFailure", out.error_class)
        self.assertFalse(out.passed)
        compare.assert_not_called()  # even byte-identical synthetic ROMs cannot pass
        self.assertEqual(["cli", "identity", "loaded-manifest", "cli", "identity"],
                         ["identity" if a[1] == "--class-path" else a[3] for a, _ in calls])
        # Includes removal of first manifest, both ROMs/logs and Java adapter.
        self.assert_clean()

    def test_identity_adapter_checks_exact_pinned_public_api_without_raw_errors(self):
        source = m.REOPEN_IDENTITY
        self.assertIn("RomOpener.Results loaded = new RomOpener().openRomFile(new File(args[0]))", source)
        self.assertIn("!loaded.wasOpeningSuccessful()", source)
        self.assertIn("!(loaded.getRomHandler() instanceof Gen3RomHandler)", source)
        self.assertIn("!((Gen3RomHandler) loaded.getRomHandler()).usesCfruDpeRandomPoolPolicy()", source)
        self.assertIn("System.exit(1)", source)
        self.assertIn("catch (Exception ignored)", source)
        self.assertNotIn("printStackTrace", source)
        self.assertNotIn("System.err", source)
        gen3 = public_fixture("romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java",
                              "7206af0126ccf61aea4a2ebe22772928f63ad4c5")
        opener = public_fixture("romio/src/main/java/com/uprfvx/romio/romio/RomOpener.java",
                                "ce0003feef079c764db6f3c3d3904e5a38e9274b")
        self.assertIn("public boolean usesCfruDpeRandomPoolPolicy()", gen3)
        self.assertIn("public Results openRomFile(File", opener)
        self.assertIn("public boolean wasOpeningSuccessful()", opener)
        self.assertIn("public RomHandler getRomHandler()", opener)

    def test_input_mutation_after_cli_stops_before_reopen_or_replay(self):
        calls, execute = self.executor()
        with patch.object(m, "input_digest", side_effect=[b"original", b"original", b"modified", b"modified"]), patch.object(m, "command", side_effect=execute), self.assertRaises(m.MatrixError):
            m.attempt(self.group, m.PRIMARY, self.rom, self.jar, self.directory, True)
        self.assertEqual(1, len(calls))
        self.assertEqual("cli", calls[0][0][3])
        self.assert_clean()

    def test_replay_mismatch(self):
        _, execute = self.executor(mismatch=True)
        with patch.object(m, "command", side_effect=execute):
            out = m.attempt(self.group, 677, self.rom, self.jar, self.directory, True)
        self.assertEqual("FAIL", out.replay)
        self.assertEqual("ReplayMismatch", out.error_class)
        self.assert_clean()

    def test_retry_once_identical_settings_and_seed(self):
        for second_pass in (False, True):
            first = m.Outcome("FAIL", error_class="GenerationFailure")
            second = m.Outcome("PASS", "PASS", input_unchanged="PASS") if second_pass else m.Outcome("FAIL", error_class="GenerationFailure")
            with patch.object(m, "attempt", side_effect=[first, second]) as attempt, contextlib.redirect_stdout(io.StringIO()):
                out = m.run_case(self.group, m.PRIMARY, self.rom, self.jar, self.directory)
            self.assertEqual(2, attempt.call_count)
            self.assertEqual(attempt.call_args_list[0], attempt.call_args_list[1])
            self.assertEqual("FAIL" if second_pass else "PASS", out.reproduced)
            self.assertFalse(out.passed)

    def test_no_retry_on_pass(self):
        with patch.object(m, "attempt", return_value=m.Outcome("PASS", "PASS", "PASS", input_unchanged="PASS")) as attempt:
            self.assertTrue(m.run_case(self.group, 1, self.rom, self.jar, self.directory).passed)
        self.assertEqual(1, attempt.call_count)

    def test_different_retry_failure_is_not_called_reproduced(self):
        with patch.object(m, "attempt", side_effect=[m.Outcome("FAIL"), m.Outcome("PASS", "FAIL")]):
            out = m.run_case(self.group, m.PRIMARY, self.rom, self.jar, self.directory)
        self.assertEqual("DIFFERENT_FAILURE", out.reproduced)
        self.assertEqual("FAIL", out.retry)

    def test_replay_generation_and_reopen_failure(self):
        for fail_step in (4, 6):
            _, execute = self.executor()
            count = 0

            def failing(args, cwd, timeout=600):
                nonlocal count
                count += 1
                if count == fail_step:
                    return result(1, "ERROR: replay failed")
                return execute(args, cwd, timeout)

            with patch.object(m, "command", side_effect=failing):
                out = m.attempt(self.group, 1, self.rom, self.jar, self.directory, True)
            self.assertEqual("FAIL", out.replay)
            self.assertFalse(out.passed)
            self.assert_clean()

    def test_diagnostic_expectation_does_not_mask_infrastructure_failure(self):
        self.assertEqual("EXPECTED_FAIL", m.diagnostic_status(m.Outcome("FAIL", error_class="RomIOException")))
        self.assertEqual("DIAGNOSTIC_FAIL", m.diagnostic_status(m.Outcome("FAIL", error_class="ProcessFailure")))
        self.assertEqual("GENERATION_PASS_WITH_KNOWN_SEMANTIC_LIMITATION", m.diagnostic_status(m.Outcome("PASS", "PASS", input_unchanged="PASS")))

    def test_exception_timeout_and_interrupt_cleanup(self):
        for error in (OSError(self.rom), subprocess.TimeoutExpired(self.rom, 1), KeyboardInterrupt(), InterruptedError()):
            def execute(args, cwd, timeout=600):
                (Path(cwd) / "synthetic.gba").write_bytes(b"synthetic")
                raise error
            with patch.object(m, "command", side_effect=execute):
                if isinstance(error, (KeyboardInterrupt, InterruptedError)):
                    with self.assertRaises(type(error)):
                        m.attempt(self.group, 0, self.rom, self.jar, self.directory, True)
                else:
                    out = m.attempt(self.group, 0, self.rom, self.jar, self.directory, True)
                    self.assertFalse(out.passed)
                    self.assertNotIn(self.rom, out.message)
            self.assert_clean()

    def test_sanitization_allowlist(self):
        private = '/unknown/root/My ROM.gba relative-private.gba C:\\Secret\\Private.gba abc123 ' + 'f' * 64
        for cls in m.ERROR_CLASSES:
            name, message = m.safe_error(cls + ": " + private, "Failure")
            self.assertEqual(cls, name)
            for marker in ("My ROM", "relative-private", "Secret", "abc123", "f" * 64):
                self.assertNotIn(marker, message)
        self.assertEqual(("Failure", "UPR step failed; raw details discarded."), m.safe_error(private, "Failure"))

    def test_sanitized_report_and_alias_coverage(self):
        self.group.aliases += [m.Intent("CASUAL_NATDEX", "ACCEPTANCE", classification="ACCEPTANCE")]
        out = m.Outcome("FAIL", message="UPR step failed; raw details discarded.")
        text = io.StringIO()
        with contextlib.redirect_stdout(text):
            m.print_report(self.group.aliases, [self.group], [(self.group, m.PRIMARY, out)], m.inventory_counts(OVERLAYS, UNSUPPORTED), "FAIL")
        report = text.getvalue()
        self.assertIn("CASE_INTENTS: 2", report)
        self.assertIn("UNIQUE_EFFECTIVE_CASES: 1", report)
        self.assertIn("Classification: ACCEPTANCE", report)
        self.assertIn("CASUAL_NATDEX: FAIL", report)
        self.assertIn("CASE + CASUAL_NATDEX", report)
        self.assertNotIn(self.rom, report)
        self.assertNotIn(str(self.directory), report)
        self.assertNotIn("synthetic bytes", report)


class EntryPointTest(unittest.TestCase):
    def setUp(self):
        for name, value in (("read_public_source", GENERATOR_SOURCE), ("input_digest", b"synthetic input")):
            mock = patch.object(m, name, return_value=value)
            mock.start()
            self.addCleanup(mock.stop)

    def test_dry_run_no_rom_java_build_or_output_access(self):
        with patch.object(m, "verify_pins"), patch.object(m, "prepare_tool") as tool, patch.object(m, "attempt") as attempt, patch("builtins.input") as prompt, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, m.main(["--dry-run", "--rom", "/fictional/never-read.gba"]))
        tool.assert_not_called()
        attempt.assert_not_called()
        prompt.assert_not_called()
        self.assertIn("PRIVATE_ROM_MATRIX = NOT_RUN", output.getvalue())
        for line in (
            "Workspace: 9411c39f472d1d08555be988d2f7ab9482902580",
            "Tree: e56df52bb79f3239fa4e9534cd252525d6229685",
            "UPR-FVX: f979c3c6ec4d32a92ecf632a3d9d38151d5cb19c",
            "CASE_INTENTS: 303", "SOURCE_OVERLAY_IDS: 159",
            "GENERATOR_UNSUPPORTED: 4", "TARGET_EXCLUDED: 9",
            "REQUIRED_OVERLAY_CASES: 146",
        ):
            self.assertIn(line, output.getvalue())

    def entry_run(self, argv, fail=False):
        cases = [m.Intent("CONTROL_UNCHANGED", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("CASUAL_NATDEX", "ACCEPTANCE", classification="ACCEPTANCE", secondary=True)]
        payloads = ["control", "casual"]
        calls = []

        def run(group, seed, rom, jar, temp):
            self.assertTrue(Path(temp).is_dir())
            calls.append((group.aliases[0].id, seed, rom, Path(temp)))
            return m.Outcome("FAIL") if fail else m.Outcome("PASS", "PASS", input_unchanged="PASS")

        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=payloads), patch.object(m, "normalize_settings", return_value=(payloads, {}, {})), patch.object(m, "run_case", side_effect=run), patch("builtins.input", return_value="/fictional/private.gba") as prompt, contextlib.redirect_stdout(io.StringIO()) as output:
            code = m.main(argv)
        return code, calls, prompt, output.getvalue()

    def test_diagnostics_nonblocking_success_and_failure(self):
        cases = [m.Intent("CONTROL_UNCHANGED", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("OPTIONAL_DIAGNOSTIC", "DIAGNOSTIC", classification="DIAGNOSTIC")]
        for diagnostic in (m.Outcome("PASS", "PASS", input_unchanged="PASS"),
                           m.Outcome("FAIL", error_class="RomIOException"),
                           m.Outcome("PASS", "FAIL", error_class="ProcessFailure")):
            with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=["control", "diagnostic"]), patch.object(m, "normalize_settings", return_value=(["control", "diagnostic"], {}, {})), patch.object(m, "run_case", side_effect=[m.Outcome("PASS", "PASS", input_unchanged="PASS"), diagnostic]), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(0, m.main(["--rom", "/fictional/input.gba", "--stop-on-fail"]))
            text = output.getvalue()
            self.assertIn("PASS: 1\nFAIL: 0", text)
            self.assertIn("Diagnostic OPTIONAL_DIAGNOSTIC: " + m.diagnostic_status(diagnostic), text)
            self.assertIn("CASUAL_NATDEX: NOT_RUN", text)
            self.assertIn("Result: R2_RANDOMIZER_GENERATION_MATRIX_PASS", text)

    def test_diagnostic_never_masks_required_failure(self):
        cases = [m.Intent("CASUAL_NATDEX", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("OPTIONAL_DIAGNOSTIC", "DIAGNOSTIC", classification="DIAGNOSTIC")]
        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=["casual", "diagnostic"]), patch.object(m, "normalize_settings", return_value=(["casual", "diagnostic"], {}, {})), patch.object(m, "run_case", side_effect=[m.Outcome("FAIL"), m.Outcome("FAIL", error_class="RomIOException")]), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, m.main(["--rom", "/fictional/input.gba"]))
        self.assertIn("CASUAL_NATDEX: FAIL", output.getvalue())
        self.assertIn("PASS: 0\nFAIL: 1", output.getvalue())

    def test_inventory_report_and_dry_run_exclusions(self):
        with patch.object(m, "verify_pins"), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, m.main(["--dry-run"]))
        text = output.getvalue()
        for line in ("SOURCE_OVERLAY_IDS: 159", "GENERATOR_UNSUPPORTED: 4",
                     "TARGET_EXCLUDED: 9", "REQUIRED_OVERLAY_CASES: 146", "CASE_INTENTS: 303"):
            self.assertIn(line, text)
        for overlay, reason in m.TARGET_EXCLUSIONS.items():
            self.assertIn(overlay + ": " + reason, text)
            self.assertNotIn("STRESS " + overlay, text)

    def test_interactive_once_then_automatic_seed_sweep(self):
        code, calls, prompt, text = self.entry_run([])
        self.assertEqual(0, code)
        prompt.assert_called_once_with("Private ROM: ")
        self.assertEqual([m.PRIMARY, m.PRIMARY, 0, 1, 677], [call[1] for call in calls])
        self.assertFalse(calls[0][3].exists())
        self.assertNotIn("/fictional/private.gba", text)

    def test_optional_rom_no_prompt(self):
        code, calls, prompt, _ = self.entry_run(["--rom", "/fictional/argument.gba"])
        self.assertEqual(0, code)
        prompt.assert_not_called()
        self.assertTrue(all(c[2] == "/fictional/argument.gba" for c in calls))

    def test_stop_on_fail_skips_rest_and_sweep(self):
        code, calls, _, text = self.entry_run(["--stop-on-fail"], fail=True)
        self.assertEqual(1, code)
        self.assertEqual(1, len(calls))
        self.assertIn("CASUAL_NATDEX: NOT_RUN", text)
        self.assertIn("SKIP / excluded: 4 / 13", text)

    def test_normalization_after_single_prompt_and_before_any_case(self):
        order = []
        cases = [m.Intent("CONTROL_UNCHANGED", "ACCEPTANCE", classification="ACCEPTANCE")]

        def prompt(text):
            order.append("prompt")
            return "/fictional/private.gba"

        def normalize(*args):
            order.append("normalize")
            raise m.MatrixError("Recognition failed")

        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=["synthetic"]), patch.object(m, "normalize_settings", side_effect=normalize), patch.object(m, "run_case") as run, patch("builtins.input", side_effect=prompt), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(1, m.main([]))
        self.assertEqual(["prompt", "normalize"], order)
        run.assert_not_called()

    def test_no_secondary_if_primary_fails(self):
        code, calls, _, _ = self.entry_run([], fail=True)
        self.assertEqual(1, code)
        self.assertEqual([m.PRIMARY, m.PRIMARY], [call[1] for call in calls])

    def test_fail_fast_before_prompt_or_rom_use(self):
        for step in ("verify_pins", "prepare_tool", "generate_settings"):
            with patch.object(m, "verify_pins"), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=[]), patch.object(m, step, side_effect=m.MatrixError("Prerequisite failed")), patch.object(m, "attempt") as attempt, patch("builtins.input") as prompt, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(1, m.main(["--rom", "/fictional/never-read.gba"]))
                self.assertEqual(1, m.main([]))
            attempt.assert_not_called()
            prompt.assert_not_called()

    def test_java_missing_or_wrong_version(self):
        for response in (result(1), result(err='openjdk version "21"')):
            with patch.object(m, "command", return_value=response) as command, patch.object(Path, "is_file", return_value=True):
                with self.assertRaises(m.MatrixError):
                    m.prepare_tool(m.ROOT, Path("/synthetic/temp"), Path("/synthetic/candidate.jar"),
                                   m.CANDIDATES["UPR-FVX"], GENERATOR_SOURCE)
            self.assertEqual(1, command.call_count)

    def test_invalid_cli_argument_does_not_echo_private_value(self):
        with contextlib.redirect_stderr(io.StringIO()) as output:
            with self.assertRaises(SystemExit):
                m.main(["--private-invalid", "/fictional/Secret Name.gba"])
        self.assertNotIn("Secret", output.getvalue())

    def test_shell_entry_finds_root_independent_of_cwd(self):
        # Read only this public source script; don't launch the actual matrix.
        source = SCRIPT.with_name("run_upr_generation_matrix.sh").read_text()
        self.assertIn('dirname -- "$0"', source)
        self.assertIn('exec python3 "$script_dir/upr_generation_matrix.py" "$@"', source)


class PinTest(unittest.TestCase):
    def public_git(self, root, *args):
        self.assertEqual(m.ROOT, root)  # No submodule cwd is ever accessed.
        self.assertNotIn(args[0], ("fetch", "checkout", "reset", "clean", "ls-remote"))
        if args[0] in ("merge-base", "diff", "status"):
            if args[0] == "status":
                self.assertIn("--ignore-submodules=all", args)
                self.assertIn("--untracked-files=no", args)
            return ""
        if args[0] == "ls-tree":
            pin = next(pin for relative, pin in m.BASELINE_GITLINKS.values() if relative == args[-1])
            return "160000 commit " + pin + "\t" + args[-1]
        if args == ("rev-parse", m.WORKSPACE + "^{tree}"):
            return m.TREE
        self.fail(args)

    def test_baseline_and_candidates_are_separate(self):
        self.assertEqual("9411c39f472d1d08555be988d2f7ab9482902580", m.WORKSPACE)
        self.assertEqual("e56df52bb79f3239fa4e9534cd252525d6229685", m.TREE)
        self.assertEqual("4670a5413104ec02bc08c09ff584470a8a6cb7bd", m.BASELINE_GITLINKS["UPR-FVX"][1])
        self.assertEqual("f979c3c6ec4d32a92ecf632a3d9d38151d5cb19c", m.CANDIDATES["UPR-FVX"])
        self.assertEqual("e27e2113e4d59dc76cf5da8d4c43b067addae348", m.CANDIDATES["CFRU"])
        self.assertEqual("d887185de1f6ae6a78e85c4311bbadde17041d00", m.CANDIDATES["DPE"])
        self.assertEqual({
            "07_scripts/randomizer/upr_generation_matrix.py",
            "07_scripts/randomizer/tests/test_upr_generation_matrix.py",
            "08_tests/randomizer/fvx_feature_test_status_matrix.tsv",
            "08_tests/randomizer/195_fvx_feature_test_status_matrix.md",
        }, m.ALLOWED_FILES)

    def test_dirty_component_worktrees_are_never_inspected(self):
        with patch.object(m, "git", side_effect=self.public_git) as git:
            m.verify_pins(m.ROOT)
        self.assertTrue(all(call.args[0] == m.ROOT for call in git.call_args_list))

    def test_allowed_four_file_descendant(self):
        def git(root, *args):
            if args == ("diff", "--name-only", m.WORKSPACE, "HEAD"):
                return "\n".join(sorted(m.ALLOWED_FILES))
            return self.public_git(root, *args)
        with patch.object(m, "git", side_effect=git):
            m.verify_pins(m.ROOT)

    def test_candidate_gitlink_or_mode_mismatch_stops(self):
        for name, (relative, pin) in m.BASELINE_GITLINKS.items():
            for entry in ("", "100644 blob " + pin + "\t" + relative,
                          "160000 commit " + m.CANDIDATES[name] + "\t" + relative,
                          "160000 commit " + "f" * 40 + "\t" + relative):
                if entry == "160000 commit " + pin + "\t" + relative:
                    continue
                def git(root, *args):
                    return entry if args == ("ls-tree", "HEAD", relative) else self.public_git(root, *args)
                with self.subTest(component=name, entry=entry), patch.object(m, "git", side_effect=git), self.assertRaises(m.MatrixError):
                    m.verify_pins(m.ROOT)

    def test_tree_tracked_staged_and_scope_fail_closed(self):
        for broken in ("tree", "tracked", "staged", "scope", "ancestry"):
            def git(root, *args):
                if broken == "tree" and args[0] == "rev-parse":
                    return "f" * 40
                if broken == "tracked" and args[0] == "status":
                    return " M synthetic.py"
                if broken == "staged" and args[:2] == ("diff", "--cached"):
                    return "02_external/upr-fvx"
                if broken == "scope" and args == ("diff", "--name-only", m.WORKSPACE, "HEAD"):
                    return "docs/outside_scope.md"
                if broken == "ancestry" and args[0] == "merge-base":
                    raise m.MatrixError("Public Git prerequisite could not be verified.")
                return self.public_git(root, *args)
            with self.subTest(broken=broken), patch.object(m, "git", side_effect=git), self.assertRaises(m.MatrixError):
                m.verify_pins(m.ROOT)



class CandidateSourceTest(unittest.TestCase):
    def response(self, body, url=None):
        response = io.BytesIO(body)
        response.geturl = lambda: url or m.PUBLIC_SOURCE_URL + m.SOURCE
        return response

    def test_exact_public_blob_and_commit_url(self):
        with patch.object(m, "urlopen", return_value=self.response(GENERATOR_SOURCE.encode())) as get, patch.object(Path, "read_bytes", side_effect=AssertionError("No checkout source")), patch.object(m, "git", side_effect=AssertionError("No component Git")):
            self.assertEqual(GENERATOR_SOURCE, m.read_public_source())
        get.assert_called_once_with(m.PUBLIC_SOURCE_URL + m.SOURCE, timeout=30)
        self.assertIn(m.CANDIDATES["UPR-FVX"], get.call_args.args[0])
        self.assertEqual("b679e3e6bea9d908fef804af21456275974484c5",
                         m.public_blob_id(GENERATOR_SOURCE.encode()))

    def test_reject_component_source_before_path_resolution(self):
        with patch.object(Path, "resolve", side_effect=AssertionError("No component metadata")), patch.object(Path, "read_bytes") as read, self.assertRaises(m.MatrixError):
            m.read_public_source(local_file=m.ROOT / "02_external/upr-fvx/SettingsProfileGenerator.java")
        read.assert_not_called()

    def test_stale_missing_redirect_and_unapproved_source_fail_closed(self):
        for body in (b"", GENERATOR_SOURCE.replace("setRemoveTimeBasedEvolutions(true)", "setRemoveTimeBasedEvolutions(false)").encode()):
            with patch.object(m, "urlopen", return_value=self.response(body)), self.assertRaises(m.MatrixError):
                m.read_public_source()
        with patch.object(m, "urlopen", return_value=self.response(b"", "https://example.invalid/private")), self.assertRaises(m.MatrixError):
            m.read_public_source()
        with patch.object(m, "urlopen") as get, self.assertRaises(m.MatrixError):
            m.read_public_source("unapproved.java")
        get.assert_not_called()

    def test_public_source_failure_never_echoes_network_details(self):
        with patch.object(m, "urlopen", side_effect=OSError("/fictional/Secret token")), self.assertRaises(m.MatrixError) as caught:
            m.read_public_source()
        self.assertNotIn("Secret", str(caught.exception))
        self.assertNotIn("token", str(caught.exception))

    def test_local_public_snapshot_has_exact_content(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "SettingsProfileGenerator.java"
            file.write_text(GENERATOR_SOURCE)
            with patch.object(m, "urlopen") as get:
                self.assertEqual(GENERATOR_SOURCE, m.read_public_source(local_file=file))
            get.assert_not_called()
            file.write_text(GENERATOR_SOURCE + "// source drift")
            with self.assertRaises(m.MatrixError):
                m.read_public_source(local_file=file)

    def test_component_or_protected_source_not_opened(self):
        for relative in ("02_external/upr-fvx", "02_external/CFRU-expansion",
                         "04_private_roms", "05_builds", "03_tools/releases"):
            with patch.object(Path, "read_bytes") as read, patch.object(m, "urlopen") as get, self.assertRaises(m.MatrixError):
                m.read_public_source(local_file=m.ROOT / relative / "SettingsProfileGenerator.java")
            read.assert_not_called()
            get.assert_not_called()


class CandidateJarTest(unittest.TestCase):
    def catalogue(self):
        features = "\n".join(name + "\t" + ("unsupported\tpublic reason" if name in UNSUPPORTED else "supported") for name in OVERLAYS)
        profiles = []
        for name, body in re.findall(r'profiles\.put\("([^"]+)",\s*(.*?)\);', GENERATOR_SOURCE, re.S):
            profiles.append(name + "\t" + ",".join(re.findall(r'"([A-Z0-9_-]+)"', body)))
        return features, "\n".join(profiles)

    def prepare(self, feature=None, profile=None):
        features, profiles = self.catalogue()
        with patch.object(Path, "is_file", return_value=True), patch.object(Path, "read_bytes", side_effect=AssertionError("Never inspect a JAR")), patch.object(m, "command", side_effect=[
            result(err='openjdk version "25"'),
            feature or result(text=features),
            profile or result(text=profiles),
        ]) as command, contextlib.redirect_stdout(io.StringIO()):
            jar = m.prepare_tool(m.ROOT, Path("/synthetic/temp"), Path("/synthetic/prebuilt.jar"),
                                 m.CANDIDATES["UPR-FVX"], GENERATOR_SOURCE)
        return jar, command.call_args_list

    def test_supplied_candidate_attestation_and_cli_no_auto_build(self):
        jar, calls = self.prepare()
        self.assertEqual(Path("/synthetic/prebuilt.jar"), jar)
        self.assertEqual(3, len(calls))
        self.assertTrue(all(c.args[0][0] == "java" for c in calls))
        self.assertEqual("--list-features", calls[1].args[0][-1])
        self.assertEqual("--list-profiles", calls[2].args[0][-1])
        self.assertFalse(any("gradlew" in str(c) or "fetch" in str(c) for c in calls))

    def test_filename_version_or_wrong_commit_never_proves_provenance(self):
        for commit in (None, m.BASELINE_GITLINKS["UPR-FVX"][1], "f" * 40):
            with patch.object(Path, "is_file") as exists, patch.object(m, "command") as command, self.assertRaises(m.MatrixError):
                m.prepare_tool(m.ROOT, Path("/synthetic/temp"), Path("/synthetic/PR217-UPR-FVX-v1.5.1.jar"),
                               commit, GENERATOR_SOURCE)
            command.assert_not_called()
            exists.assert_not_called()

    def test_stale_source_rejected_before_jar_access(self):
        for source in (None, GENERATOR_SOURCE + "// not the public blob"):
            with patch.object(Path, "is_file") as exists, patch.object(m, "command") as command, self.assertRaises(m.MatrixError):
                m.prepare_tool(m.ROOT, Path("/synthetic/temp"), Path("/synthetic/candidate.jar"),
                               m.CANDIDATES["UPR-FVX"], source)
            exists.assert_not_called()
            command.assert_not_called()

    def test_old_worktree_jar_and_missing_jar_are_not_built(self):
        with patch.object(Path, "is_file") as exists, patch.object(m, "command") as command, self.assertRaises(m.MatrixError):
            m.prepare_tool(m.ROOT, Path("/synthetic/temp"), m.ROOT / "02_external/upr-fvx/random/build/libs/UPR-FVX.jar",
                           m.CANDIDATES["UPR-FVX"], GENERATOR_SOURCE)
        exists.assert_not_called()
        command.assert_not_called()
        with patch.object(Path, "is_file", return_value=False), patch.object(m, "command") as command, self.assertRaises(m.MatrixError):
            m.prepare_tool(m.ROOT, Path("/synthetic/temp"), Path("/synthetic/unavailable.jar"),
                           m.CANDIDATES["UPR-FVX"], GENERATOR_SOURCE)
        command.assert_not_called()

    def test_source_cli_inventory_profile_and_capability_mismatch(self):
        features, profiles = self.catalogue()
        for feature, profile in (
            (result(1, "/fictional/private.jar Exception"), None),
            (result(text=features.replace("FVX-ITEM-010\tsupported", "FVX-ITEM-010\tunsupported")), None),
            (result(text=features + "\nFVX-ITEM-010\tsupported"), None),
            (None, result(text=profiles + "\nUNREVIEWED\tFVX-ITEM-010")),
            (None, result(1, "/fictional/private details")),
        ):
            with self.subTest(feature=bool(feature), profile=bool(profile)), self.assertRaises(m.MatrixError) as caught:
                self.prepare(feature, profile)
            self.assertNotIn("/fictional", str(caught.exception))


class CandidateRiskTest(unittest.TestCase):
    def setUp(self):
        self.cases = m.build_matrix(OVERLAYS, UNSUPPORTED, PROFILES)
        self.by_id = {c.id: c for c in self.cases}

    @staticmethod
    def observed(**changes):
        # Independent synthetic Settings-getter response, not a serializer.
        fields = {
            "LimitPokemon": "false", "CurrentRestrictions": "1022",
            "EvolutionsMod": "UNCHANGED", "ChangeImpossibleEvolutions": "false",
            "MakeEvolutionsEasier": "false", "EstimateLevelForEvolutionImprovements": "false",
            "RemoveTimeBasedEvolutions": "false", "PickupItemsMod": "UNCHANGED",
            "BanBadRandomPickupItems": "false", "ShopItemsMod": "UNCHANGED",
            "PokemonPalettesMod": "UNCHANGED", "PokemonPalettesFollowTypes": "false",
            "PokemonPalettesFollowEvolutions": "false", "PokemonPalettesShinyFromNormal": "false",
            "UseTimeBasedEncounters": "false",
        }
        fields.update(changes)
        return fields

    def evo_observed(self):
        return self.observed(LimitPokemon="true", CurrentRestrictions="1023", EvolutionsMod="RANDOM",
                             ChangeImpossibleEvolutions="true", EstimateLevelForEvolutionImprovements="true",
                             RemoveTimeBasedEvolutions="true")

    def test_exact_six_new_positive_intents_all_seed_replay(self):
        self.assertEqual(set(m.RISK_SINGLES), {c.id for c in self.cases if c.layer == "STRESS" and c.id in m.RISK_IDS})
        self.assertEqual({m.RISK_EVOLUTION, m.RISK_PICKUP}, {c.id for c in self.cases if c.layer == "RISK"})
        for name in m.RISK_IDS:
            self.assertTrue(self.by_id[name].replay)
            self.assertTrue(self.by_id[name].secondary)
        for case in self.cases:
            if case.layer in ("FULL", "PAIR", "TRIPLE", "MAX"):
                self.assertFalse(set(case.overlays) & set(m.RISK_SINGLES))

    def test_evolution_user_case_relatives_on_and_no_relatives_preserved(self):
        state = m.effective(self.by_id[m.RISK_EVOLUTION], OVERLAYS)
        self.assertEqual("new GenRestrictions(0x3FF)", state["CurrentRestrictions"])
        for flag in ("LimitPokemon", "ChangeImpossibleEvolutions", "EstimateLevelForEvolutionImprovements", "RemoveTimeBasedEvolutions"):
            self.assertEqual("true", state[flag])
        self.assertEqual("Settings.EvolutionsMod.RANDOM", state["EvolutionsMod"])
        self.assertEqual("false", state["MakeEvolutionsEasier"])
        self.assertEqual("new GenRestrictions(0x3FE)",
                         m.effective(self.by_id["MODE-GEN-LIMIT-1-9-NO-RELATIVES"], OVERLAYS)["CurrentRestrictions"])

    def test_pickup_and_shop_exact_supported_owner(self):
        for name in ("FVX-ITEM-010", m.RISK_PICKUP):
            state = m.effective(self.by_id[name], OVERLAYS)
            self.assertEqual("Settings.PickupItemsMod.RANDOM", state["PickupItemsMod"])
            self.assertEqual("true", state["BanBadRandomPickupItems"])
        self.assertEqual("Settings.ShopItemsMod.RANDOM",
                         m.effective(self.by_id[m.RISK_PICKUP], OVERLAYS)["ShopItemsMod"])
        self.assertNotIn("FVX-ITEM-010", PROFILES["07_ITEMS_SAFE"])

    def test_palette_singles_do_not_enable_the_pair(self):
        for name, own, other in (("FVX-GFX-002", "PokemonPalettesFollowTypes", "PokemonPalettesShinyFromNormal"),
                                 ("FVX-GFX-004", "PokemonPalettesShinyFromNormal", "PokemonPalettesFollowTypes")):
            state = m.effective(self.by_id[name], OVERLAYS)
            self.assertEqual("Settings.PokemonPalettesMod.RANDOM", state["PokemonPalettesMod"])
            self.assertEqual("true", state[own])
            self.assertNotEqual("true", state.get(other))

    def test_incompatible_palette_request_rejected_before_override(self):
        for extra in ({}, {"PokemonPalettesShinyFromNormal": "false"}, {"PokemonPalettesMod": "Settings.PokemonPalettesMod.UNCHANGED"}):
            with self.assertRaises(m.MatrixError):
                m.effective(m.Intent("NEGATIVE", "DIAGNOSTIC", ("FVX-GFX-002", "FVX-GFX-004"), extra=extra), OVERLAYS)

    def test_make_easier_is_not_ungated_with_time_or_fake_off_override(self):
        for leaves in (("FVX-TRAIT-025",), ("FVX-TRAIT-025", "FVX-TRAIT-027"),
                       ("FVX-TRAIT-024", "FVX-TRAIT-025", "FVX-TRAIT-027")):
            for extra in ({}, {"MakeEvolutionsEasier": "false"}):
                with self.assertRaisesRegex(m.MatrixError, "OWNERSHIP_WITNESS_V1"):
                    m.effective(m.Intent("NEGATIVE", "STRESS", leaves, extra=extra), OVERLAYS)

    def test_risk_leaf_in_any_safe_family_fails_closed(self):
        for family in m.FULL:
            for leaf in m.RISK_SINGLES:
                altered = dict(PROFILES, **{family: PROFILES[family] + (leaf,)})
                with self.subTest(family=family, leaf=leaf), self.assertRaises(m.MatrixError):
                    m.build_matrix(OVERLAYS, UNSUPPORTED, altered)

    def test_pickup_writer_allowlist_and_negative_guards(self):
        source = m.bridge_source(self.cases, OVERLAYS)
        expected = [str(i) for i, c in enumerate(self.cases) if c.id in ("FVX-ITEM-010", m.RISK_PICKUP)]
        match = re.search(r'Set\.of\(([^)]*)\)\.contains\(id\)', source)
        self.assertEqual(expected, re.findall(r'"([0-9]+)"', match[1]))
        self.assertIn("s.isMakeEvolutionsEasier()", source)
        self.assertIn("s.isPokemonPalettesFollowTypes() && s.isPokemonPalettesShinyFromNormal()", source)
        self.assertIn("MiscTweak.REUSABLE_TMS.getValue()", source)
        self.assertIn("Settings.PickupItemsMod.RANDOM", source)
        self.assertIn("RANDOM_EVERY_LEVEL", source)

    def test_observer_getters_exist_in_exact_public_settings(self):
        getters = set(re.findall(r's\.(\w+)\(', m.OBSERVE_JAVA))
        for method in getters:
            self.assertRegex(SETTINGS_SOURCE, r'public [\w<>]+ ' + method + r'\(')
        self.assertIn("!observe(s).equals(observe(restored))", m.bridge_source(self.cases, OVERLAYS))
        self.assertIn("!observe(s).equals(observe(restored))", m.NORMALIZER)

    def test_risk_source_and_normalized_state_are_observed(self):
        cases = [self.by_id[m.RISK_EVOLUTION]]
        actual = self.evo_observed()
        for stage in ("Settings round-trip", "target normalization"):
            m.verify_requested_states(cases, OVERLAYS, {0: actual}, stage)
            for key in ("LimitPokemon", "CurrentRestrictions", "EvolutionsMod", "ChangeImpossibleEvolutions",
                        "EstimateLevelForEvolutionImprovements", "RemoveTimeBasedEvolutions", "MakeEvolutionsEasier"):
                changed = dict(actual, **{key: "false" if actual[key] == "true" else "true"})
                with self.subTest(stage=stage, key=key):
                    if stage == "Settings round-trip" or key == "MakeEvolutionsEasier":
                        with self.assertRaises(m.MatrixError):
                            m.verify_requested_states(cases, OVERLAYS, {0: changed}, stage)
                    else:
                        self.assertIn(0, m.verify_requested_states(cases, OVERLAYS, {0: changed}, stage))
        with self.assertRaises(m.MatrixError):
            m.verify_requested_states(cases, OVERLAYS, {}, "round-trip")

    def test_normalized_away_user_gen_limit_not_counted_or_substituted(self):
        cases = [self.by_id[m.RISK_EVOLUTION]]
        normalized = dict(self.evo_observed(), LimitPokemon="false", CurrentRestrictions="-1")
        blocked = m.verify_requested_states(cases, OVERLAYS, {0: normalized}, "target normalization")
        self.assertEqual({0: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",)}, blocked)
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN",
                         m.matrix_result(cases, [], [], blocked))
        self.assertIn(m.RISK_EVOLUTION, self.by_id)  # no silently dropped intent
        self.assertEqual("new GenRestrictions(0x3FF)", m.effective(cases[0], OVERLAYS)["CurrentRestrictions"])

    def test_observation_schema_discards_private_content(self):
        text = "\n".join(k + "=" + v for k, v in self.evo_observed().items())
        self.assertEqual(self.evo_observed(), m.parse_observation(text))
        for changed in (text + "\nSecret=/fictional/private.gba", text.replace("RANDOM", "/fictional/private"),
                        text.replace("LimitPokemon=true", "LimitPokemon=true\nLimitPokemon=true")):
            with self.assertRaises(m.MatrixError) as caught:
                m.parse_observation(changed)
            self.assertNotIn("/fictional", str(caught.exception))

    def test_selected_hidden_flags_preserve_guarded_owner_state(self):
        for data in (m.settings_data(m.IRONMON), m.CASUAL_BYTES + bytes(33)):
            fields = decoded_fields(data)
            self.assertFalse(fields["MakeEvolutionsEasier"])
            self.assertFalse(fields["PokemonPalettesFollowTypes"] and fields["PokemonPalettesShinyFromNormal"])
            self.assertEqual("UNCHANGED", fields["PickupItemsMod"])
            for flag in ("AllowMegaForms", "AllowGigantamaxForms", "IncludeMegaItems", "IncludeZCrystalItems", "IncludeDynamaxGmaxItems"):
                self.assertFalse(fields[flag])

    def test_mocked_settings_and_normalizer_gate_observations(self):
        cases = [self.by_id[m.RISK_EVOLUTION]]
        payloads = [synthetic_payload(bytes(67))]
        text = "\n".join(k + "=" + v for k, v in self.evo_observed().items())
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            def execute(args, cwd, timeout=600):
                (cwd / "0.settings").write_text(payloads[0])
                (cwd / "0.rnqs").write_text("synthetic")
                (cwd / "0.normalization").write_text("NONE")
                (cwd / "0.state").write_text(text)
                (cwd / "0.post-state").write_text(text)
                return result()
            with patch.object(m, "command", side_effect=execute):
                self.assertEqual(payloads, m.generate_settings(cases, OVERLAYS, Path("synthetic.jar"), temp))
                self.assertEqual((payloads, {}, {}), m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input", temp, payloads, OVERLAYS))
            (temp / "0.post-state").write_text(text.replace("CurrentRestrictions=1023", "CurrentRestrictions=-1"))
            with patch.object(m, "command", return_value=result()):
                after, events, blocked = m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input", temp, payloads, OVERLAYS)
            self.assertEqual({0: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",)}, blocked)

    def test_two_current_overlays_accounted_without_acceptance(self):
        self.assertIn("FVX-SPECIAL-WILD-001", self.by_id)
        self.assertIn("FVX-FOE-SENSIBLE-HELD-ITEMS", m.EXCLUDED)
        diagnostic = self.by_id["04_FOE_HELD_ITEMS_SENSIBLE_EXPECTED_FAIL"]
        self.assertEqual("DIAGNOSTIC", diagnostic.classification)
        self.assertIn("FVX-FOE-SENSIBLE-HELD-ITEMS", diagnostic.overlays)


class NormalizedCoverageTest(unittest.TestCase):
    """Unavailable options never run as substitutes or inherit a positive alias."""

    def setUp(self):
        self.cases = m.build_matrix(OVERLAYS, UNSUPPORTED, PROFILES)
        self.by_id = {c.id: c for c in self.cases}

    def observations(self, cases):
        observations = {}
        for i in m.observed_indices(cases, OVERLAYS):
            state = CandidateRiskTest.observed()
            for key, value in m.effective(cases[i], OVERLAYS).items():
                if key not in state:
                    continue
                if key == "CurrentRestrictions":
                    value = str(int(re.search(r"0x[0-9A-Fa-f]+", value)[0], 16))
                elif value.startswith("Settings."):
                    value = value.rsplit(".", 1)[1]
                state[key] = value
            observations[i] = state
        return observations

    def test_exact_public_time_encounter_source_normalization(self):
        abstract = public_fixture("romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java",
                                  "43e068b4d10cf2af9f92193738830913881dee81")
        gen3 = public_fixture("romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java",
                              "7206af0126ccf61aea4a2ebe22772928f63ad4c5")
        self.assertRegex(abstract, r"boolean hasTimeBasedEncounters\(\)\s*\{\s*// DEFAULT: no\s*return false;")
        self.assertNotRegex(gen3, r"boolean hasTimeBasedEncounters\(")
        self.assertRegex(SETTINGS_SOURCE, r"if \(!rh.hasTimeBasedEncounters\(\)\) \{\s*this.setUseTimeBasedEncounters\(false\);")
        self.assertEqual("true", m.assignments(OVERLAYS[m.SPECIAL_WILD])["UseTimeBasedEncounters"])

    def test_exact_public_gen_limit_validity_source_gate(self):
        abstract = public_fixture("romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java",
                                  "8e4138d8f72bf29d1c203f435df5d8feb51310f2")
        self.assertIn("return getRomEntry().getExpectedCRC32() == actualCRC32;", abstract)
        self.assertRegex(SETTINGS_SOURCE, r"rh instanceof Gen3RomHandler && !rh.isRomValid\(null\)")
        self.assertIn("this.currentRestrictions = null;", SETTINGS_SOURCE)
        self.assertIn("this.setLimitPokemon(false);", SETTINGS_SOURCE)

    def test_special_wild_on_roundtrip_and_effective_on_are_checked(self):
        cases = [self.by_id[m.SPECIAL_WILD]]
        on = self.observations(cases)
        for stage in ("Settings round-trip", "target normalization"):
            self.assertEqual({}, m.verify_requested_states(cases, OVERLAYS, on, stage))
        off = {0: dict(on[0], UseTimeBasedEncounters="false")}
        with self.assertRaises(m.MatrixError):
            m.verify_requested_states(cases, OVERLAYS, off, "Settings round-trip")

    def test_special_wild_off_blocks_single_full_pairs_and_max(self):
        observed = self.observations(self.cases)
        expected = {i for i, c in enumerate(self.cases)
                    if m.SPECIAL_WILD in c.overlays}
        self.assertTrue(expected)
        for i in expected:
            self.assertIn(i, observed)
            observed[i]["UseTimeBasedEncounters"] = "false"
        blocked = m.verify_requested_states(self.cases, OVERLAYS, observed, "target normalization")
        self.assertEqual(expected, set(blocked))
        self.assertTrue(all(v == ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",) for v in blocked.values()))
        for name in (m.SPECIAL_WILD, "11_SPECIAL_WILD", "MAX_SAFE_COMBINED"):
            self.assertIn(name, {self.cases[i].id for i in blocked})
        self.assertTrue(any(self.cases[i].layer == "PAIR" for i in blocked))

    def test_gen_limit_normalization_isolates_ordinary_and_evolution_requests(self):
        cases = [self.by_id["FVX-ITEM-002"], self.by_id["MODE-GEN-LIMIT-1-9"],
                 self.by_id[m.RISK_EVOLUTION]]
        observed = self.observations(cases)
        for fields in observed.values():
            fields.update(LimitPokemon="false", CurrentRestrictions="-1")
        blocked = m.verify_requested_states(cases, OVERLAYS, observed, "target normalization")
        self.assertEqual({1, 2}, set(blocked))
        self.assertTrue(all(v == ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",) for v in blocked.values()))
        self.assertEqual("new GenRestrictions(0x3FF)", m.effective(cases[2], OVERLAYS)["CurrentRestrictions"])

    def test_lost_relatives_alone_still_blocks_risk(self):
        cases = [self.by_id[m.RISK_EVOLUTION]]
        observed = self.observations(cases)
        observed[0]["CurrentRestrictions"] = "1022"
        self.assertEqual({0: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",)},
                         m.verify_requested_states(cases, OVERLAYS, observed, "target normalization"))

    def test_special_and_gen_limit_reasons_accumulate(self):
        cases = [self.by_id["MAX_SAFE_COMBINED"]]
        observed = self.observations(cases)
        observed[0].update(LimitPokemon="false", CurrentRestrictions="-1", UseTimeBasedEncounters="false")
        self.assertEqual({0: ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF", "GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE")},
                         m.verify_requested_states(cases, OVERLAYS, observed, "target normalization"))

    def test_source_and_schema_failures_are_not_relaxed_to_partial(self):
        cases = [self.by_id[m.SPECIAL_WILD], self.by_id[m.RISK_EVOLUTION]]
        observed = self.observations(cases)
        with self.assertRaises(m.MatrixError):
            m.verify_requested_states(cases, OVERLAYS, {0: observed[0]}, "target normalization")
        observed[0]["UseTimeBasedEncounters"] = "false"
        with self.assertRaises(m.MatrixError):
            m.verify_requested_states(cases, OVERLAYS, observed, "Settings round-trip")
        observed[1]["MakeEvolutionsEasier"] = "true"
        with self.assertRaisesRegex(m.MatrixError, "OWNERSHIP_WITNESS_V1"):
            m.verify_requested_states(cases, OVERLAYS, observed, "target normalization")

    def test_normalized_alias_cannot_inherit_pass_or_wrong_settings_file(self):
        cases = [self.by_id[m.SPECIAL_WILD], self.by_id["FVX-ITEM-002"]]
        blocked = {0: ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",)}
        groups = m.deduplicate(cases, ["same", "same"], Path("/synthetic"), blocked)
        self.assertEqual([cases[1]], groups[0].aliases)
        self.assertEqual(Path("/synthetic/1.rnqs"), groups[0].settings)
        records = [(groups[0], m.PRIMARY, m.Outcome("PASS", "PASS", input_unchanged="PASS"))]
        self.assertEqual("PASS", m.intent_status(cases[1], groups, records))
        self.assertEqual("NOT_RUN", m.intent_status(cases[0], groups, records, {m.SPECIAL_WILD}))
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN",
                         m.matrix_result(cases, groups, records, blocked))

    def test_all_planned_seeds_and_replays_required_for_matrix_pass(self):
        case = self.by_id[m.RISK_PICKUP]
        groups = m.deduplicate([case], ["synthetic"], Path("/synthetic"))
        for seeds, replay in (((m.PRIMARY,), "PASS"), (m.SECONDARY, "NOT_APPLICABLE")):
            records = [(groups[0], seed, m.Outcome("PASS", "PASS", replay, input_unchanged="PASS"))
                       for seed in seeds]
            self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN",
                             m.matrix_result([case], groups, records))
        records = [(groups[0], seed, m.Outcome("PASS", "PASS", "PASS", input_unchanged="PASS"))
                   for seed in m.SECONDARY]
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PASS", m.matrix_result([case], groups, records))
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN", m.matrix_result([case], [], []))

    def test_report_full_max_and_risk_not_run_with_partial_result(self):
        cases = [self.by_id[n] for n in (m.SPECIAL_WILD, "11_SPECIAL_WILD", "MAX_SAFE_COMBINED", m.RISK_EVOLUTION)]
        blocked = {i: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",) if c.id == m.RISK_EVOLUTION
                   else ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",) for i, c in enumerate(cases)}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            m.print_report(cases, [], [], m.inventory_counts(OVERLAYS, UNSUPPORTED),
                           m.matrix_result(cases, [], [], blocked), blocked=blocked)
        text = output.getvalue()
        for name in (m.SPECIAL_WILD, "11_SPECIAL_WILD", "MAX_SAFE_COMBINED"):
            self.assertIn(name + ": NOT_RUN", text)
            self.assertNotIn(name + ": PASS", text)
        self.assertIn(m.RISK_EVOLUTION + ": STOP/NOT_RUN", text)
        self.assertIn("GENERATE=NOT_RUN; REOPEN=NOT_RUN; REPLAY=NOT_RUN", text)
        self.assertIn("NORMALIZATION_BLOCKED_INTENTS: 4", text)
        self.assertNotIn("R2_RANDOMIZER_GENERATION_MATRIX_PASS", text)

    def test_mocked_normalizer_reads_special_state_and_removes_no_flags_itself(self):
        cases = [self.by_id[m.SPECIAL_WILD]]
        observed = self.observations(cases)[0]
        payloads = [synthetic_payload(bytes(67))]
        with tempfile.TemporaryDirectory() as name:
            temp = Path(name)
            def execute(args, cwd, timeout=600):
                observed["UseTimeBasedEncounters"] = "false"
                (cwd / "0.settings").write_text(payloads[0])
                (cwd / "0.normalization").write_text("NONE")
                (cwd / "0.post-state").write_text("\n".join(k + "=" + v for k, v in observed.items()))
                return result()
            with patch.object(m, "command", side_effect=execute):
                after, events, blocked = m.normalize_settings(cases, Path("synthetic.jar"),
                                                               "/fictional/input", temp, payloads, OVERLAYS)
            self.assertEqual(payloads, after)
            self.assertEqual({}, events)
            self.assertEqual({0: ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",)}, blocked)
            self.assertIn("s.tweakForRom(handler)", m.NORMALIZER)
            self.assertNotIn("s.setUseTimeBasedEncounters(true)", m.NORMALIZER)
            self.assertNotIn("s.setLimitPokemon(true)", m.NORMALIZER)

    def test_mocked_roundtrip_special_off_stops_before_rom(self):
        cases = [self.by_id[m.SPECIAL_WILD]]
        observed = CandidateRiskTest.observed()
        with tempfile.TemporaryDirectory() as name:
            temp = Path(name)
            def execute(args, cwd, timeout=600):
                (cwd / "0.settings").write_text(synthetic_payload(bytes(67)))
                (cwd / "0.state").write_text("\n".join(k + "=" + v for k, v in observed.items()))
                return result()
            with patch.object(m, "command", side_effect=execute), self.assertRaises(m.MatrixError):
                m.generate_settings(cases, OVERLAYS, Path("synthetic.jar"), temp)

    def test_main_continues_independent_and_eligible_risks_after_gen_limit_stop(self):
        cases = [self.by_id[n] for n in (m.RISK_EVOLUTION, m.SPECIAL_WILD, "FVX-ITEM-002", m.RISK_PICKUP)]
        # Two unavailable requests normalize to exactly the same strings as
        # eligible cases. Neither may enter a generation call or PASS alias.
        before = ["evolution-on", "time-on", "core", "pickup"]
        after = ["core", "core", "core", "pickup"]
        blocked = {0: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",),
                   1: ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",)}
        calls, temps = [], []
        def execute(group, seed, rom, jar, temp):
            calls.append((tuple(c.id for c in group.aliases), seed))
            temps.append(temp)
            return m.Outcome("PASS", "PASS", "PASS", input_unchanged="PASS")
        with patch.object(m, "read_public_source", return_value=GENERATOR_SOURCE), patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=before), patch.object(m, "normalize_settings", return_value=(after, {0: 1023}, blocked)), patch.object(m, "input_digest", return_value=b"synthetic input"), patch.object(m, "run_case", side_effect=execute), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, m.main(["--rom", "/fictional/input", "--stop-on-fail"]))
        self.assertEqual([(("FVX-ITEM-002",), m.PRIMARY)] +
                         [((m.RISK_PICKUP,), seed) for seed in (m.PRIMARY, 0, 1, 677)], calls)
        self.assertTrue(temps and all(not p.exists() for p in temps))
        text = output.getvalue()
        self.assertIn("EXECUTION_STAGE: INDEPENDENT", text)
        self.assertIn("EXECUTION_STAGE: RISK", text)
        self.assertIn(m.RISK_EVOLUTION + ": STOP/NOT_RUN", text)
        self.assertIn(m.RISK_PICKUP + ": PASS", text)
        self.assertIn("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN", text)
        self.assertNotIn("R2_RANDOMIZER_GENERATION_MATRIX_PASS", text)
        self.assertNotIn("/fictional", text)

    def test_expected_gen_normalization_uses_real_preflight_and_runs_core(self):
        cases = [self.by_id[m.RISK_EVOLUTION], self.by_id["FVX-ITEM-002"]]
        original = bytearray(67)
        original[30:34] = (0x3FF).to_bytes(4, "little")
        original[65] |= 8
        before = [synthetic_payload(original), synthetic_payload(bytes(67))]
        after = [NormalizationAccountingTest().adapted(before[0]), before[1]]
        observed = self.observations(cases)[0]
        observed.update(LimitPokemon="false", CurrentRestrictions="-1")
        dirs = []
        def normalize_java(args, cwd, timeout=600):
            dirs.append(cwd)
            for i, payload in enumerate(after):
                (cwd / f"{i}.settings").write_text(payload)
                (cwd / f"{i}.normalization").write_text(
                    "\t".join((m.GEN_NORMALIZATION, "true", "true", "false", "true", "1023", "false", "-1"))
                    if i == 0 else "NONE")
            (cwd / "0.post-state").write_text("\n".join(k + "=" + v for k, v in observed.items()))
            return result()
        with patch.object(m, "read_public_source", return_value=GENERATOR_SOURCE), patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=before), patch.object(m, "command", side_effect=normalize_java), patch.object(m, "input_digest", return_value=b"synthetic input"), patch.object(m, "run_case", return_value=m.Outcome("PASS", "PASS", input_unchanged="PASS")) as run, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, m.main(["--rom", "/fictional/input"]))
        self.assertEqual(1, run.call_count)
        self.assertEqual(["FVX-ITEM-002"], [c.id for c in run.call_args.args[0].aliases])
        self.assertTrue(dirs and all(not p.exists() for p in dirs))
        self.assertIn("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN", output.getvalue())
        self.assertNotIn("R2_RANDOMIZER_GENERATION_MATRIX_PASS", output.getvalue())

    def test_current_target_normalization_leaves_independent_cases_eligible(self):
        observed = self.observations(self.cases)
        expected = set()
        for i, state in observed.items():
            if state["LimitPokemon"] == "true":
                state.update(LimitPokemon="false", CurrentRestrictions="-1")
                expected.add(i)
            if state["UseTimeBasedEncounters"] == "true":
                state["UseTimeBasedEncounters"] = "false"
                expected.add(i)
        blocked = m.verify_requested_states(self.cases, OVERLAYS, observed, "target normalization")
        self.assertEqual(expected, set(blocked))
        eligible = {c.id for i, c in enumerate(self.cases) if i not in blocked}
        for name in ("CONTROL_UNCHANGED", "CASUAL_NATDEX", "IRONMON_NATDEX", "FVX-ITEM-002",
                     "FVX-TRAIT-027", "FVX-GFX-002", "FVX-GFX-004", m.RISK_PICKUP):
            self.assertIn(name, eligible)
        for name in (m.SPECIAL_WILD, m.RISK_EVOLUTION, "MODE-GEN-LIMIT-1-9", "11_SPECIAL_WILD", "MAX_SAFE_COMBINED"):
            self.assertNotIn(name, eligible)

    def test_other_normalized_risk_loss_is_blocked_before_execution(self):
        cases = [self.by_id["FVX-ITEM-002"], self.by_id[m.RISK_PICKUP]]
        observed = self.observations(cases)
        observed[1]["PickupItemsMod"] = "UNCHANGED"
        blocked = m.verify_requested_states(cases, OVERLAYS, observed, "target normalization")
        self.assertEqual({1: ("RISK_OPTIONS_NOT_EFFECTIVE",)}, blocked)
        groups = m.deduplicate(cases, ["core", "pickup-off"], Path("/synthetic"), blocked)
        self.assertEqual([cases[0]], groups[0].aliases)

    def test_missing_evolution_normalization_witness_stops_before_core(self):
        cases = [self.by_id[m.RISK_EVOLUTION], self.by_id["FVX-ITEM-002"]]
        data = bytearray(67)
        data[30:34] = (0x3FF).to_bytes(4, "little")
        data[65] |= 8
        before = [synthetic_payload(data), synthetic_payload(bytes(67))]
        after = [NormalizationAccountingTest().adapted(before[0]), before[1]]
        with tempfile.TemporaryDirectory() as name:
            temp = Path(name)
            def execute(args, cwd, timeout=600):
                for i, payload in enumerate(after):
                    (cwd / f"{i}.settings").write_text(payload)
                    (cwd / f"{i}.normalization").write_text("NONE")
                return result()
            with patch.object(m, "command", side_effect=execute), self.assertRaisesRegex(m.MatrixError, "Unconfirmed target normalization"):
                m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input", temp, before, OVERLAYS)

    def test_blocked_case_is_not_pass_even_with_fabricated_success_record(self):
        case = self.by_id[m.RISK_EVOLUTION]
        group = m.Group("synthetic", Path("/synthetic"), [case])
        records = [(group, seed, m.Outcome("PASS", "PASS", "PASS", input_unchanged="PASS"))
                   for seed in m.SECONDARY]
        blocked = {0: ("GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE",)}
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN",
                         m.matrix_result([case], [group], records, blocked))

    def test_execution_failure_takes_precedence_over_partial(self):
        cases = [self.by_id[m.SPECIAL_WILD], self.by_id["FVX-ITEM-002"]]
        blocked = {0: ("TIME_BASED_ENCOUNTERS_NORMALIZED_OFF",)}
        groups = m.deduplicate(cases, ["same", "same"], Path("/synthetic"), blocked)
        records = [(groups[0], m.PRIMARY, m.Outcome("FAIL"))]
        self.assertEqual("R2_RANDOMIZER_GENERATION_MATRIX_FAIL", m.matrix_result(cases, groups, records, blocked))

    def test_dedup_incomplete_accounting_fails_closed(self):
        for payloads, blocked in (([], {}), (["x"], {1: ("invalid",)})):
            with self.assertRaises(m.MatrixError):
                m.deduplicate([self.by_id[m.SPECIAL_WILD]], payloads, Path("/synthetic"), blocked)


class InputAtomicityTest(unittest.TestCase):
    def test_private_input_comparison_only_uses_synthetic_bytes_here(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "synthetic.data"
            file.write_bytes(b"public synthetic bytes")
            before = m.input_digest(file)
            self.assertEqual(before, m.input_digest(file))
            file.write_bytes(b"altered synthetic bytes")
            self.assertNotEqual(before, m.input_digest(file))

    def test_failed_input_read_is_sanitized(self):
        with patch.object(Path, "open", side_effect=OSError("/fictional/Private.gba")), self.assertRaises(m.MatrixError) as caught:
            m.input_digest("/fictional/Private.gba")
        self.assertNotIn("Private.gba", str(caught.exception))

    def test_input_change_stops_before_retry(self):
        altered = m.Outcome("FAIL", input_unchanged="FAIL")
        with patch.object(m, "attempt", return_value=altered) as attempt, self.assertRaises(m.MatrixError):
            m.run_case(m.Group("synthetic", Path("synthetic"), []), 1, "/fictional/input", Path("/fictional/jar"), Path("/synthetic"))
        self.assertEqual(1, attempt.call_count)

    def test_input_change_after_retry_stops(self):
        with patch.object(m, "attempt", side_effect=[m.Outcome("FAIL", input_unchanged="PASS"),
                                                    m.Outcome("FAIL", input_unchanged="FAIL")]) as attempt, self.assertRaises(m.MatrixError):
            m.run_case(m.Group("synthetic", Path("synthetic"), []), 1, "/fictional/input", Path("/fictional/jar"), Path("/synthetic"))
        self.assertEqual(2, attempt.call_count)

    def test_normalization_failure_still_checks_input_and_cleans(self):
        created = []
        def normalize(cases, jar, rom, temp, payloads, overlays=None):
            created.append(temp)
            raise m.MatrixError("Synthetic normalization failure")
        with patch.object(m, "verify_pins"), patch.object(m, "read_public_source", return_value=GENERATOR_SOURCE), patch.object(m, "prepare_tool", return_value=Path("/fictional/jar")), patch.object(m, "generate_settings", return_value=[]), patch.object(m, "normalize_settings", side_effect=normalize), patch.object(m, "input_digest", side_effect=[b"before", b"after"]), patch.object(m, "run_case") as run, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, m.main(["--rom", "/fictional/private"]))
        run.assert_not_called()
        self.assertTrue(created and all(not d.exists() for d in created))
        self.assertIn("Input unchanged check failed", output.getvalue())
        self.assertNotIn("/fictional", output.getvalue())

    def test_seed_hash_log_settings_or_gameplay_not_reported_as_evidence(self):
        report = io.StringIO()
        group = m.Group("secret settings", Path("/fictional/private"), [m.Intent("CASE", "STRESS")])
        with contextlib.redirect_stdout(report):
            m.print_report([], [group], [(group, m.PRIMARY, m.Outcome("FAIL"))],
                           m.inventory_counts(OVERLAYS, UNSUPPORTED), "FAIL")
        text = report.getvalue()
        for private in (str(m.PRIMARY), "/fictional/private", "secret settings"):
            self.assertNotIn(private, text)
        for status in ("LOG_CONTENT=NOT_RUN", "MANIFEST_SEMANTICS=NOT_RUN", "GAMEPLAY=NOT_RUN"):
            self.assertIn(status, text)


class NormalizerDiagnosticTest(unittest.TestCase):
    # Independent expected contract, not derived from the production mapping.
    CODES = {
        20: "ADAPTER_COMPILE_OR_LAUNCH", 21: "INPUT_OPEN_REJECTED",
        22: "TARGET_PROFILE_UNRECOGNIZED", 23: "SETTINGS_READ_FAILED",
        24: "SETTINGS_TWEAK_FAILED", 25: "SETTINGS_ROUNDTRIP_FAILED",
        26: "UNKNOWN_ADAPTER_FAILURE",
    }
    PRIVATE = "/fictional/PRIVATE.gba checksum=PRIVATE_HASH seed=PRIVATE_SEED\njava.lang.PrivateException: PRIVATE_SETTINGS\n at private.Stack(trace:1)"

    def wire(self, code):
        return "MATRIX_NORMALIZER_V1\t" + code + "\n"

    def stop(self, response=None, exception=None):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            with patch.object(m, "command", return_value=response, side_effect=exception), patch.object(Path, "read_text", side_effect=AssertionError("No outputs consumed after STOP")), self.assertRaises(m.MatrixError) as caught:
                m.normalize_settings([], Path("/fictional/PRIVATE.jar"),
                                     "/fictional/PRIVATE.gba", temp, [], OVERLAYS)
        return str(caught.exception)

    def test_every_exact_stage_exit_pair_stops_before_output_consumption(self):
        for number, code in self.CODES.items():
            with self.subTest(code=code):
                self.assertEqual("NORMALIZER_STAGE=" + code + "; details discarded.",
                                 self.stop(result(number, self.wire(code))))

    def test_wrong_exit_and_stage_pairs_are_unknown(self):
        for number in (0, 1, -9, 19, 20, 21, 22, 23, 24, 25, 26, 27):
            for expected_number, code in self.CODES.items():
                if number == expected_number:
                    continue
                with self.subTest(exit=number, code=code):
                    self.assertEqual("UNKNOWN_ADAPTER_FAILURE",
                                     m.normalizer_failure(result(number, self.wire(code))))

    def test_malformed_duplicate_injected_or_spoofed_records_are_unknown(self):
        wire = self.wire("INPUT_OPEN_REJECTED")
        for text in ("", "INPUT_OPEN_REJECTED", wire.rstrip(), wire + "\n",
                     " " + wire, wire + wire, wire.lower(),
                     wire.replace("\t", " "), wire.replace("V1", "V2"),
                     wire.replace("\n", "\x00\n"),
                     self.PRIVATE + wire, wire + self.PRIVATE,
                     "MATRIX_NORMALIZER_V1\tPRIVATE_SETTINGS\n"):
            with self.subTest(text=text):
                self.assertEqual("NORMALIZER_STAGE=UNKNOWN_ADAPTER_FAILURE; details discarded.",
                                 self.stop(result(21, text)))

    def test_stderr_is_never_accepted_as_a_status_channel(self):
        for number, code in self.CODES.items():
            for out, err in (("", self.wire(code)), (self.wire(code), self.PRIVATE),
                             (self.wire(code), self.wire(code))):
                with self.subTest(code=code, out=out):
                    self.assertEqual("UNKNOWN_ADAPTER_FAILURE",
                                     m.normalizer_failure(result(number, out, err)))

    def test_compile_error_and_crash_before_stage_are_unknown(self):
        for number in (1, 2, 137, -9):
            for out, err in (("", ""), ("", self.PRIVATE), (self.PRIVATE, "")):
                with self.subTest(exit=number):
                    self.assertEqual("NORMALIZER_STAGE=UNKNOWN_ADAPTER_FAILURE; details discarded.",
                                     self.stop(result(number, out, err)))

    def test_process_launch_oserror_is_classified_without_raw_message(self):
        for exc in (FileNotFoundError(self.PRIVATE), PermissionError(self.PRIVATE)):
            with self.subTest(exception=type(exc).__name__):
                self.assertEqual("NORMALIZER_STAGE=ADAPTER_COMPILE_OR_LAUNCH; details discarded.",
                                 self.stop(exception=exc))

    def test_timeout_and_subprocess_failure_are_unknown_without_raw_output(self):
        for exc in (subprocess.TimeoutExpired([self.PRIVATE], 1, output=self.PRIVATE,
                                            stderr=self.PRIVATE),
                    subprocess.SubprocessError(self.PRIVATE)):
            with self.subTest(exception=type(exc).__name__):
                self.assertEqual("NORMALIZER_STAGE=UNKNOWN_ADAPTER_FAILURE; details discarded.",
                                 self.stop(exception=exc))

    def test_only_silent_exit_zero_is_success(self):
        self.assertIsNone(m.normalizer_failure(result()))
        for out, err in ((self.PRIVATE, ""), ("", self.PRIVATE),
                         (self.wire("SETTINGS_READ_FAILED"), "")):
            self.assertEqual("UNKNOWN_ADAPTER_FAILURE", m.normalizer_failure(result(0, out, err)))

    def test_error_factory_cannot_echo_untrusted_status(self):
        self.assertEqual("NORMALIZER_STAGE=UNKNOWN_ADAPTER_FAILURE; details discarded.",
                         str(m.normalizer_stop(self.PRIVATE)))

    def test_java_template_suppresses_diagnostics_and_emits_only_contract_literals(self):
        java = m.NORMALIZER
        self.assertLess(java.index("System.setOut("), java.index("RootPath.path ="))
        self.assertLess(java.index("System.setErr("), java.index("RootPath.path ="))
        self.assertEqual(2, java.count("OutputStream.nullOutputStream()"))
        records = re.findall(r'case (\d+): status.println\("MATRIX_NORMALIZER_V1\\t([A-Z_]+)"\); break;', java)
        self.assertEqual(self.CODES, {int(n): code for n, code in records})
        self.assertEqual(len(self.CODES), java.count("status.println("))
        self.assertIn("catch (Throwable ignored)", java)
        self.assertIn("System.exit(stage)", java)
        for forbidden in ("getMessage(", "printStackTrace(", "getClass(", "System.out.print", "System.err.print"):
            self.assertNotIn(forbidden, java)

    def test_java_stage_boundaries_keep_loader_profile_and_settings_gates(self):
        java = m.NORMALIZER
        boundaries = (("int stage = 20;", "RootPath.path ="),
                      ("stage = 21;", "new RomOpener().openRomFile"),
                      ("stage = 22;", "instanceof Gen3RomHandler"),
                      ("stage = 26;", "handler.isRomValid(null)"),
                      ("stage = 23;", "Settings.readFromFileFormat(in)"),
                      ("stage = 24;", "s.tweakForRom(handler)"),
                      ("stage = 25;", "s.writeToFileFormat(out)"))
        for marker, operation in boundaries:
            with self.subTest(stage=marker):
                self.assertLess(java.index(marker), java.index(operation))
        self.assertIn("!loaded.wasOpeningSuccessful()", java)
        self.assertIn("!((Gen3RomHandler) loaded.getRomHandler()).usesCfruDpeRandomPoolPolicy()", java)
        self.assertIn("!observe(s).equals(observe(restored))", java)

    def test_each_category_main_returns_nonzero_no_generation_and_cleans(self):
        responses = [result(n, self.wire(code)) for n, code in self.CODES.items()]
        responses += [result(1, self.PRIVATE, self.PRIVATE)]
        for response in responses:
            created = []
            def execute(args, cwd, timeout=600):
                created.append(cwd)
                return response
            with self.subTest(exit=response.returncode), patch.object(m, "verify_pins"), patch.object(m, "read_public_source", return_value=GENERATOR_SOURCE), patch.object(m, "prepare_tool", return_value=Path("/fictional/PRIVATE.jar")), patch.object(m, "generate_settings", return_value=[]), patch.object(m, "command", side_effect=execute), patch.object(m, "input_digest", return_value=b"synthetic input") as digest, patch.object(m, "run_case") as run, contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(1, m.main(["--rom", "/fictional/PRIVATE.gba"]))
            run.assert_not_called()
            self.assertEqual(2, digest.call_count)  # Existing input-unchanged finally gate.
            self.assertTrue(created and all(not p.exists() for p in created))
            code = self.CODES.get(response.returncode, "UNKNOWN_ADAPTER_FAILURE")
            self.assertEqual("Result: STOP\nSanitized message: NORMALIZER_STAGE=" + code
                             + "; details discarded.\n", output.getvalue())


class LedgerTest(unittest.TestCase):
    def test_only_two_rows_added_and_130_original_rows_unchanged(self):
        body = (m.ROOT / "08_tests/randomizer/fvx_feature_test_status_matrix.tsv").read_bytes()
        lines = body.splitlines(keepends=True)
        additions = {b"FVX-SPECIAL-WILD-001", b"FVX-FOE-SENSIBLE-HELD-ITEMS"}
        original = b"".join(l for l in lines if l.split(b"\t", 1)[0] not in additions)
        self.assertEqual("7919b6f73f1ed64b84ec8174028e4eabeb0ad9e9", m.public_blob_id(original))
        rows = [line.decode().rstrip("\n").split("\t") for line in lines[1:]]
        self.assertEqual(132, len(rows))
        self.assertEqual(132, len({r[0] for r in rows}))
        self.assertTrue(all(len(r) == 11 for r in rows))
        self.assertEqual({r[0] for r in rows}, {n for n in OVERLAYS if n.startswith("FVX-")})
        for row in rows:
            if row[0].encode() in additions:
                self.assertEqual(["NOT_STARTED", "NOT_STARTED"], row[5:7])

    def test_existing_matrix_doc_revision_and_method_distinctions(self):
        text = (m.ROOT / "08_tests/randomizer/195_fvx_feature_test_status_matrix.md").read_text()
        for marker in ("132", "Legacy Revisions Only", "NOT_RUN", "USER-only", m.RISK_EVOLUTION,
                       m.RISK_PICKUP, "OWNERSHIP_WITNESS_V1", "GFX-002+GFX-004"):
            self.assertIn(marker, text)



if __name__ == "__main__":
    unittest.main()
