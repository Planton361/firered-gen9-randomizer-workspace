"""#681 tests: public source + synthetic temp artifacts + mocked subprocesses only.

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


SCRIPT = Path(__file__).resolve().parents[1] / "upr_generation_matrix.py"
SPEC = importlib.util.spec_from_file_location("upr_generation_matrix", SCRIPT)
m = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = m
SPEC.loader.exec_module(m)
PUBLIC = m.ROOT / m.PINS["UPR-FVX"][0]
SETTINGS_SOURCE = (PUBLIC / "random/src/main/java/com/uprfvx/random/Settings.java").read_text()
OVERLAYS, UNSUPPORTED, PROFILES = m.source_model((PUBLIC / m.SOURCE).read_text())


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
        self.assertEqual(13, len(m.EXCLUDED))
        required = set(OVERLAYS) - UNSUPPORTED - m.EXCLUDED
        self.assertEqual(142, len(required))
        self.assertEqual(required, {c.id for c in self.cases if c.layer == "STRESS"})

    def test_deterministic_order_and_identity(self):
        self.assertEqual(self.cases, m.build_matrix(OVERLAYS, UNSUPPORTED, PROFILES))
        self.assertEqual(297, len(self.cases))
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
        self.assertEqual(set(m.MAXIMUM + m.SELECTED[1:]), secondary)
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
                self.assertNotIn("PickupItemsMod", state)  # baseline UNCHANGED
                if "ITEMS_SHOPS" in case.families:
                    self.assertTrue(set(m.ITEMS_SAFE) <= set(case.overlays))
        source = m.bridge_source(self.cases, OVERLAYS)
        self.assertIn("s.getPickupItemsMod() != Settings.PickupItemsMod.UNCHANGED", source)
        self.assertNotIn('"07_ITEMS_FULL"', source)
        self.assertNotIn('"FVX-ITEM-010"', source)

    def test_exact_target_exclusion_reasons(self):
        self.assertEqual({
            "FVX-TRAIT-025": "UNSAFE_CFRU_DPE_EVOLUTION_IMPROVEMENT_RAW_ROW",
            "FVX-TRAIT-027": "UNSAFE_CFRU_DPE_EVOLUTION_IMPROVEMENT_RAW_ROW",
            "FVX-GFX-002": "UNSAFE_CFRU_DPE_OPTIONAL_PALETTE_SUBOPTION",
            "FVX-GFX-004": "UNSAFE_CFRU_DPE_OPTIONAL_PALETTE_SUBOPTION",
            "FVX-MISC-011": "REDUNDANT_CFRU_NATIVE_REUSABLE_TMS",
        }, m.TARGET_EXCLUSIONS)
        self.assertEqual({"SOURCE_OVERLAY_IDS": 159, "GENERATOR_UNSUPPORTED": 4,
                          "TARGET_EXCLUDED": 13, "REQUIRED_OVERLAY_CASES": 142},
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
                  for layer in ("ACCEPTANCE", "STRESS", "MODE", "FULL", "PAIR", "TRIPLE", "MAX", "DIAGNOSTIC")}
        self.assertEqual(dict(zip(counts, (3, 142, 56, 12, 66, 12, 5, 1))), counts)
        self.assertEqual(sum(counts.values()), len(self.cases))

    def test_source_drift_fails_closed(self):
        source = (PUBLIC / m.SOURCE).read_text()
        with self.assertRaises(m.MatrixError):
            m.source_model(source.replace('"FVX-ITEM-008", "FVX-ITEM-009", "FVX-ITEM-010"', '"FVX-ITEM-009", "FVX-ITEM-010"'))

    def test_source_inventory_cardinality_drift_fails_closed(self):
        source = (PUBLIC / m.SOURCE).read_text()
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
        case = m.Intent("MISC", "FULL", PROFILES["10_MISC_TWEAKS"])
        bits = m.effective(case, OVERLAYS)["MiscTweak"].split(" | ")
        self.assertEqual(12, len(bits))
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
                self.assertEqual((payloads, {}), m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, payloads))
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
                    m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, [m.IRONMON])
            (temp / "0.settings").write_text(synthetic_payload(bytes(67)))
            (temp / "0.normalization").write_text("NONE")
            with patch.object(m, "command", return_value=result()):
                with self.assertRaises(m.MatrixError):
                    m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/input.gba", temp, [m.IRONMON])

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
                    return result(text="/fictional/private/Secret.gba DD88761C")
                with patch.object(m, "command", side_effect=execute):
                    if witness == self.witness():
                        after, events = m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/Private.gba", directory, before)
                        self.assertEqual({0: 1022}, events)
                        self.assertEqual([self.adapted(before[0])], after)
                    else:
                        with self.assertRaises(m.MatrixError) as caught:
                            m.normalize_settings(cases, Path("synthetic.jar"), "/fictional/Private.gba", directory, before)
                        self.assertNotIn("Secret.gba", str(caught.exception))
                        self.assertNotIn("DD88761C", str(caught.exception))
            self.assertFalse(directory.exists())  # adapter, witness, settings all removed


class ExecutionTest(unittest.TestCase):
    def setUp(self):
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
        gen3 = (PUBLIC / "romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java").read_text()
        opener = (PUBLIC / "romio/src/main/java/com/uprfvx/romio/romio/RomOpener.java").read_text()
        self.assertIn("public boolean usesCfruDpeRandomPoolPolicy()", gen3)
        self.assertIn("public Results openRomFile(File", opener)
        self.assertIn("public boolean wasOpeningSuccessful()", opener)
        self.assertIn("public RomHandler getRomHandler()", opener)

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
            second = m.Outcome("PASS", "PASS") if second_pass else m.Outcome("FAIL", error_class="GenerationFailure")
            with patch.object(m, "attempt", side_effect=[first, second]) as attempt, contextlib.redirect_stdout(io.StringIO()):
                out = m.run_case(self.group, m.PRIMARY, self.rom, self.jar, self.directory)
            self.assertEqual(2, attempt.call_count)
            self.assertEqual(attempt.call_args_list[0], attempt.call_args_list[1])
            self.assertEqual("FAIL" if second_pass else "PASS", out.reproduced)
            self.assertFalse(out.passed)

    def test_no_retry_on_pass(self):
        with patch.object(m, "attempt", return_value=m.Outcome("PASS", "PASS", "PASS")) as attempt:
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
        self.assertEqual("GENERATION_PASS_WITH_KNOWN_SEMANTIC_LIMITATION", m.diagnostic_status(m.Outcome("PASS", "PASS")))

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
    def test_dry_run_no_rom_java_build_or_output_access(self):
        with patch.object(m, "verify_pins"), patch.object(m, "prepare_tool") as tool, patch.object(m, "attempt") as attempt, patch("builtins.input") as prompt, contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, m.main(["--dry-run", "--rom", "/fictional/never-read.gba"]))
        tool.assert_not_called()
        attempt.assert_not_called()
        prompt.assert_not_called()
        self.assertIn("PRIVATE_ROM_MATRIX = NOT_RUN", output.getvalue())

    def entry_run(self, argv, fail=False):
        cases = [m.Intent("CONTROL_UNCHANGED", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("CASUAL_NATDEX", "ACCEPTANCE", classification="ACCEPTANCE", secondary=True)]
        payloads = ["control", "casual"]
        calls = []

        def run(group, seed, rom, jar, temp):
            self.assertTrue(Path(temp).is_dir())
            calls.append((group.aliases[0].id, seed, rom, Path(temp)))
            return m.Outcome("FAIL") if fail else m.Outcome("PASS", "PASS")

        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=payloads), patch.object(m, "normalize_settings", return_value=(payloads, {})), patch.object(m, "run_case", side_effect=run), patch("builtins.input", return_value="/fictional/private.gba") as prompt, contextlib.redirect_stdout(io.StringIO()) as output:
            code = m.main(argv)
        return code, calls, prompt, output.getvalue()

    def test_diagnostics_nonblocking_success_and_failure(self):
        cases = [m.Intent("CONTROL_UNCHANGED", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("OPTIONAL_DIAGNOSTIC", "DIAGNOSTIC", classification="DIAGNOSTIC")]
        for diagnostic in (m.Outcome("PASS", "PASS"),
                           m.Outcome("FAIL", error_class="RomIOException"),
                           m.Outcome("PASS", "FAIL", error_class="ProcessFailure")):
            with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=["control", "diagnostic"]), patch.object(m, "normalize_settings", return_value=(["control", "diagnostic"], {})), patch.object(m, "run_case", side_effect=[m.Outcome("PASS", "PASS"), diagnostic]), contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(0, m.main(["--rom", "/fictional/input.gba", "--stop-on-fail"]))
            text = output.getvalue()
            self.assertIn("PASS: 1\nFAIL: 0", text)
            self.assertIn("Diagnostic OPTIONAL_DIAGNOSTIC: " + m.diagnostic_status(diagnostic), text)
            self.assertIn("CASUAL_NATDEX: NOT_RUN", text)
            self.assertIn("Result: R2_RANDOMIZER_GENERATION_MATRIX_PASS", text)

    def test_diagnostic_never_masks_required_failure(self):
        cases = [m.Intent("CASUAL_NATDEX", "ACCEPTANCE", classification="ACCEPTANCE"),
                 m.Intent("OPTIONAL_DIAGNOSTIC", "DIAGNOSTIC", classification="DIAGNOSTIC")]
        with patch.object(m, "verify_pins"), patch.object(m, "build_matrix", return_value=cases), patch.object(m, "prepare_tool", return_value=Path("synthetic.jar")), patch.object(m, "generate_settings", return_value=["casual", "diagnostic"]), patch.object(m, "normalize_settings", return_value=(["casual", "diagnostic"], {})), patch.object(m, "run_case", side_effect=[m.Outcome("FAIL"), m.Outcome("FAIL", error_class="RomIOException")]), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(1, m.main(["--rom", "/fictional/input.gba"]))
        self.assertIn("CASUAL_NATDEX: FAIL", output.getvalue())
        self.assertIn("PASS: 0\nFAIL: 1", output.getvalue())

    def test_inventory_report_and_dry_run_exclusions(self):
        with patch.object(m, "verify_pins"), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(0, m.main(["--dry-run"]))
        text = output.getvalue()
        for line in ("SOURCE_OVERLAY_IDS: 159", "GENERATOR_UNSUPPORTED: 4",
                     "TARGET_EXCLUDED: 13", "REQUIRED_OVERLAY_CASES: 142", "CASE_INTENTS: 297"):
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
        self.assertIn("SKIP / excluded: 4 / 17", text)

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
            with patch.object(m, "command", return_value=response) as command:
                with self.assertRaises(m.MatrixError):
                    m.prepare_tool(m.ROOT, Path("/synthetic/temp"))
            self.assertEqual(1, command.call_count)

    def test_build_failure_or_missing_jar_before_rom_use(self):
        for build, jar_exists in ((result(1), False), (result(), False)):
            with patch.object(m, "command", side_effect=[result(err='openjdk version "25"'), build]), patch.object(Path, "is_file", return_value=jar_exists), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(m.MatrixError):
                    m.prepare_tool(m.ROOT, Path("/synthetic/temp"))

    def test_build_exact_pin_then_reverify(self):
        with patch.object(m, "command", side_effect=[result(err='openjdk version "25"'), result()]) as command, patch.object(Path, "is_file", return_value=True), patch.object(m, "verify_pins") as verify, contextlib.redirect_stdout(io.StringIO()):
            jar = m.prepare_tool(m.ROOT, Path("/synthetic/temp"))
        self.assertEqual(PUBLIC / "random/build/libs/UPR-FVX.jar", jar)
        self.assertIn("--rerun-tasks", command.call_args_list[1].args[0])
        self.assertIn(":random:jar", command.call_args_list[1].args[0])
        verify.assert_called_once_with(m.ROOT)

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
        if args[0] == "merge-base":
            return ""
        if args[0] == "diff" or args[0] == "status":
            return ""
        if args[0] == "ls-remote":
            return m.PINS["UPR-FVX"][1] + "\trefs/heads/compat/firered-cfru-dpe"
        if args[0] == "ls-tree":
            pin = next(pin for relative, pin in m.PINS.values() if relative == args[-1])
            return "160000 commit " + pin + "\t" + args[-1]
        if args[0] == "rev-parse":
            if args[-1].endswith("^{tree}"):
                return m.TREE
            return next(pin for relative, pin in m.PINS.values() if Path(root) == m.ROOT / relative)
        self.fail(args)

    def test_pins_allow_only_runner_descendant(self):
        with patch.object(m, "git", side_effect=self.public_git):
            m.verify_pins(m.ROOT)

    def test_every_pin_and_dirty_boundary_fail_closed(self):
        for broken in ("tree", "checkout", "gitlink", "target", "dirty", "scope"):
            def git(root, *args):
                if broken == "tree" and args[0] == "rev-parse" and args[-1].endswith("^{tree}"):
                    return "wrong"
                if broken == "checkout" and args == ("rev-parse", "HEAD"):
                    return "wrong"
                if broken == "gitlink" and args[0] == "ls-tree":
                    return "160000 commit wrong"
                if broken == "target" and args[0] == "ls-remote":
                    return "wrong"
                if broken == "dirty" and args[0] == "status":
                    return "modified synthetic source"
                if broken == "scope" and args[0] == "diff":
                    return "docs/outside_scope.md"
                return self.public_git(root, *args)
            with self.subTest(broken=broken), patch.object(m, "git", side_effect=git):
                with self.assertRaises(m.MatrixError):
                    m.verify_pins(m.ROOT)


if __name__ == "__main__":
    unittest.main()
