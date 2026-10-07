#!/usr/bin/env python3
"""Source-only and synthetic byte fixtures; never opens game/local manifests."""
import copy
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

import generate_cfru_dpe_source_data as g

ROOT = Path(__file__).resolve().parents[2]


class MemorySources:
    def __init__(self, data, provenance):
        self.data = copy.deepcopy(data)
        self.provenance = copy.deepcopy(provenance)

    def read(self, component, path):
        return self.data[component][path]


class ParserTests(unittest.TestCase):
    def test_defines_enums_forward_aliases(self):
        symbols, expressions = g.parse_header("""
#define MOVE_ALIAS MOVE_FIRST
#define MOVE_FIRST 4
// commented values must not enter the map
/* #define MOVE_WRONG 99 */
enum
{
MOVE_NEXT = MOVE_FIRST + 1,
MOVE_LAST,
};
#define MOVES_COUNT (MOVE_LAST + 1)
""")
        self.assertEqual(symbols, {"MOVE_FIRST": 4, "MOVE_NEXT": 5, "MOVE_LAST": 6,
                                   "MOVES_COUNT": 7, "MOVE_ALIAS": 4})
        self.assertEqual(expressions["MOVE_ALIAS"], "MOVE_FIRST")

    def test_missing_invalid_duplicate_cyclic_definitions(self):
        for source in ("#define X MISSING", "#define X 1\n#define X 1", "#define X 1 * 2",
                       "#define X Y\n#define Y X", "enum\n{\nX = MISSING,\nY,\n};",
                       "enum\n{\nX = 1,", "#if 1\n#define X 1\n#endif"):
            with self.subTest(source=source), self.assertRaises(g.ProfileError):
                g.parse_header(source)

    def test_inactive_unbound_branch_excluded(self):
        symbols, _ = g.parse_header("#define ITEM_A 1\n#ifdef UNBOUND\n#define ITEM_A 99\n#endif", {"UNBOUND": False})
        self.assertEqual(symbols, {"ITEM_A": 1})
        with self.assertRaises(g.ProfileError):
            g.parse_header("#ifdef NEW_CONFIG\n#define X 1\n#endif")

    def test_alias_resolution_not_first_definition(self):
        names = [{"name": "none"}, {"name": "actual source name"}]
        symbols, exprs = g.parse_header("#define ABILITY_ALIAS ABILITY_REAL\n#define ABILITY_REAL 1\n#define ABILITY_NONE 0")
        rows = g.mapping(symbols, exprs, "ABILITY_", 2, names, sentinels=("ABILITY_NONE",))
        self.assertEqual(rows[1]["constant"], "ABILITY_REAL")
        self.assertEqual(rows[1]["aliases"][0]["constant"], "ABILITY_ALIAS")
        self.assertEqual(rows[0]["state"], "sentinel")

    def test_ambiguous_literal_duplicate_rejected(self):
        with self.assertRaisesRegex(g.ProfileError, "Ambiguous duplicate"):
            g.mapping({"MOVE_A": 0, "MOVE_B": 0}, {"MOVE_A": "0", "MOVE_B": "0"},
                      "MOVE_", 1, [{"name": "x"}])

    def test_missing_count_names_out_of_range_and_hole(self):
        for count, symbols, names in ((None, {"MOVE_A": 0}, []),
                                      (1, {"MOVE_A": 0}, []),
                                      (1, {"MOVE_A": 2}, [{"name": "x"}])):
            with self.subTest(count=count), self.assertRaises(g.ProfileError):
                g.mapping(symbols, {"MOVE_A": "0"}, "MOVE_", count, names)
        rows = g.mapping({"MOVE_A": 0}, {"MOVE_A": "0"}, "MOVE_", 2, [{"name": "x"}, {"name": "-"}])
        self.assertEqual(rows[1]["state"], "hole")
        self.assertIsNone(rows[1]["constant"])

    def test_string_escapes_labels_and_truncation(self):
        rows, stride = g.parse_strings("MAX_LENGTH=3\nFILL_FF=True\n#org @gNames\n#org @NAME_A'S\nA\\e[B6]A\n",
                                       "gNames", "BB=A\n1B=é\n1B=\\e\nB6=♀\n")
        self.assertEqual(stride, 4)
        self.assertEqual(rows[0]["name"], "Aé♀")
        self.assertTrue(rows[0]["truncated"])
        self.assertEqual(rows[0]["labels"], ["gNames", "NAME_A'S"])

    def test_unknown_character_duplicate_label_and_missing_width(self):
        for text in ("MAX_LENGTH=2\nFILL_FF=True\n#org @gNames\n[BUFFER]\n",
                     "MAX_LENGTH=2\nFILL_FF=True\n#org @gNames\nA\n#org @gNames\nA\n",
                     "#org @gNames\nA\n"):
            with self.subTest(text=text), self.assertRaises(g.ProfileError):
                g.parse_strings(text, "gNames", "BB=A")


class LockedProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        locked = g.LockedSources(ROOT)
        cls.source = {component: {path: locked.read(component, path) for path in paths}
                      for component, paths in g.INPUTS.items()}
        cls.provenance = locked.provenance
        cls.profile = g.make_profile(MemorySources(cls.source, cls.provenance))

    def reader(self):
        return MemorySources(self.source, self.provenance)

    def mutate_source(self, component, path, before, after):
        reader = self.reader()
        self.assertIn(before, reader.data[component][path])
        reader.data[component][path] = reader.data[component][path].replace(before, after, 1)
        return reader

    def test_locked_revision_trees_and_source_hashes(self):
        p = self.profile["metadata"]
        self.assertEqual(p["productWorkspace"]["commit"], g.PRODUCT)
        self.assertEqual(p["contractWorkspace"]["tree"], g.CONTRACT_TREE)
        self.assertNotEqual(p["productWorkspace"]["commit"], p["contractWorkspace"]["commit"])
        self.assertEqual(p["revisions"], {k: pin for k, (_, pin) in g.PINS.items()})
        self.assertEqual(len(p["inputs"]), sum(map(len, g.INPUTS.values())))

    def test_wrong_checked_out_revision_rejected(self):
        real_git = g.git

        def wrong_revision(root, *args):
            if args == ("rev-parse", "HEAD"):
                return "0" * 40
            return real_git(root, *args)
        with patch.object(g, "git", wrong_revision), self.assertRaisesRegex(g.ProfileError, "revision mismatch"):
            g.LockedSources(ROOT)

    def test_non_allowlisted_input_rejected_before_read(self):
        reader = g.LockedSources(ROOT)
        with self.assertRaisesRegex(g.ProfileError, "allowlisted"):
            reader.read("CFRU", "not-an-authorized-source.txt")

    def test_gen1_mid_gen8_gen9_regional_ids_and_table_names(self):
        for value, constant, name in ((1, "SPECIES_BULBASAUR", "Bulbasaur"),
                                      (501, "SPECIES_LUCARIO", "Lucario"),
                                      (1102, "SPECIES_GROOKEY", "Grookey"),
                                      (1294, "SPECIES_SPRIGATITO", "Sprigatito"),
                                      (1439, "SPECIES_PECHARUNT", "Pecharunt"),
                                      (1022, "SPECIES_RAICHU_A", "Raichu")):
            with self.subTest(value=value):
                row = self.profile["species"][value]
                self.assertEqual((row["constant"], row["name"]), (constant, name))
        self.assertEqual(self.profile["species"][29]["name"], "Nidoran♀")
        self.assertEqual(self.profile["species"][777]["name"], "Flabébé")

    def test_expanded_moves_abilities_items_types(self):
        for section, value, name in (("moves", 733, "Wicked Blow"), ("moves", 991, "PsychicNoise"),
                                     ("abilities", 77, "Lingering Aroma"), ("abilities", 254, "Pastel Veil"),
                                     ("items", 743, "Boost Energy"), ("items", 774, "Tera Orb"),
                                     ("types", 23, "Fairy"), ("types", 24, "Stellr")):
            with self.subTest(section=section, value=value):
                self.assertEqual(self.profile[section][value]["name"], name)
        self.assertEqual(self.profile["moves"][539]["name"], "Land's Wrath")

    def test_item_coverage_and_reserved_rows(self):
        self.assertEqual(self.profile["counts"]["items"]["value"], 779)
        self.assertEqual(self.profile["counts"]["items"]["dpeSlots"], 799)
        self.assertEqual([r["id"] for r in self.profile["itemExclusions"]], list(range(779, 799)))
        self.assertTrue(all(r["state"] == "reserved" for r in self.profile["items"][776:779]))
        # Inactive UNBOUND symbols must not masquerade as aliases of active items.
        names = {r["constant"] for r in self.profile["items"]}
        self.assertNotIn("ITEM_TM01_FOCUS_PUNCH", names)
        self.assertEqual(self.profile["items"][289]["constant"], "ITEM_TM01")

    def test_species_holes_missing_initializers_and_sentinels(self):
        self.assertEqual(self.profile["counts"]["species"]["holes"], list(range(252, 277)))
        for value in (706, 835, 836):
            self.assertEqual(self.profile["species"][value]["baselineData"], "UNAVAILABLE")
        self.assertEqual(self.profile["species"][412]["state"], "sentinel")
        for section in ("species", "moves", "items", "abilities"):
            self.assertEqual(self.profile[section][0]["state"], "sentinel")
        self.assertEqual(self.profile["counts"]["types"]["holes"], [18, 21, 22])

    def test_cross_component_aliases_and_dynamic_names(self):
        aliases = self.profile["abilities"][179]["aliases"]
        self.assertEqual(len(aliases), 4)  # Ruin aliases use STALL's numeric slot.
        self.assertEqual(self.profile["abilities"][179]["name"], "Stall")
        self.assertEqual(self.profile["species"][1426]["aliases"][0]["constant"], "SPECIES_OGERPON_TERASTAL")
        overrides = self.profile["abilityNameOverrides"]
        self.assertEqual(overrides["resolution"], "UNRESOLVED")
        self.assertIn("Good As Gold", {r["name"] for r in overrides["names"]})
        self.assertEqual(overrides["tableTerminator"]["id"], 255)

    def test_layout_target_pointer_padding_and_bitfields(self):
        layout = self.profile["layouts"]
        self.assertEqual(layout["target"], "thumbv4t-none-eabi")
        self.assertEqual(layout["pointerBytes"], 4)
        records = layout["records"]
        for name, size in (("Pokemon", 100), ("BattlePokemon", 88), ("BaseStats", 28),
                           ("BattleMove", 12), ("Trainer", 40), ("TrainerMonItemCustomMoves", 32), ("Item", 44)):
            self.assertEqual(records[name]["size"], size)
        self.assertEqual(records["Pokemon"]["fields"]["hiddenAbility"],
                         {"offset": 75, "type": "u32", "bitOffset": 7, "bitWidth": 1})
        self.assertEqual(records["Trainer"]["fields"]["party"]["offset"], 36)
        self.assertEqual(records["BattleMove"]["fields"]["split"]["offset"], 10)

    def test_synthetic_party_rows_multiple_slots_and_generations(self):
        # Fixture bytes are independent fixed GBA offsets, not generated by the profile.
        data = bytearray(600)
        species = [1, 501, 1102, 1294, 1022, 1439]
        for slot, value in enumerate(species):
            start = slot * 100
            struct.pack_into("<HH", data, start + 32, value, 743)
            struct.pack_into("<4H", data, start + 44, 33, 733, 991, 0)
            data[start + 75] = 0x80
            data[start + 84] = 50
            struct.pack_into("<HH", data, start + 86, 73, 120)
        layout = self.profile["layouts"]["records"]["Pokemon"]
        offsets = layout["fields"]
        for slot, value in enumerate(species):
            start = slot * layout["size"]
            species_id = struct.unpack_from("<H", data, start + offsets["species"]["offset"])[0]
            self.assertEqual(species_id, value)
            self.assertEqual(self.profile["species"][species_id]["state"], "mapped")
            self.assertEqual(struct.unpack_from("<4H", data, start + offsets["moves"]["offset"]), (33, 733, 991, 0))
            self.assertEqual(struct.unpack_from("<H", data, start + offsets["hp"]["offset"])[0], 73)
            bit = offsets["hiddenAbility"]
            self.assertEqual((data[start + bit["offset"]] >> bit["bitOffset"]) & 1, 1)

    def test_synthetic_battle_and_move_category_bytes(self):
        data = bytearray(88)
        struct.pack_into("<H", data, 0, 1294)
        data[32] = 254
        data[33:35] = bytes([23, 24])
        struct.pack_into("<HH", data, 44, 120, 743)
        fields = self.profile["layouts"]["records"]["BattlePokemon"]["fields"]
        self.assertEqual(data[fields["ability"]["offset"]], 254)
        self.assertEqual(data[fields["type1"]["offset"]], 23)
        self.assertEqual(struct.unpack_from("<H", data, fields["item"]["offset"])[0], 743)
        move = bytes([0, 80, 23, 100, 10, 0, 0, 0, 255, 0, 2, 0])
        split = self.profile["layouts"]["records"]["BattleMove"]["fields"]["split"]["offset"]
        self.assertEqual(move[split], 2)  # Not category bits in flags at byte 8.

    def test_pointer_slot_anchor_and_runtime_not_conflated(self):
        addresses = self.profile["addresses"]
        self.assertEqual(addresses["gBaseStats"]["kind"], "repoint-anchor")
        self.assertIsNone(addresses["gBaseStats"]["indirection"])
        self.assertEqual(addresses["gBaseStatsPointerSlot"]["kind"], "pointer-slot")
        self.assertEqual(addresses["gBaseStatsPointerSlot"]["indirection"], 1)
        self.assertEqual(addresses["gBattlerPartyIndexes"]["widthBytes"], 2)
        self.assertTrue(all(a["runtimeAddress"] == "UNRESOLVED" for a in addresses.values()))
        self.assertTrue(all(c["confidence"] == "UNKNOWN" and c["sampleEpoch"] is None
                            for c in self.profile["capabilities"].values()))

    def test_missing_source_names_counts_and_table_rows_fail(self):
        changes = [("CFRU", "include/constants/moves.h", "#define MOVES_COUNT", "// removed MOVES_COUNT"),
                   ("CFRU", "strings/attack_name_table.string", "#org @NAME_POUND\nPound", ""),
                   ("DPE", "src/Base_Stats.c", "[SPECIES_BULBASAUR]", "[SPECIES_MISSING]"),
                   ("DPE", "src/Base_Stats.c", "[SPECIES_NONE] = {0},", "[SPECIES_NONE] = {0}, [1440] = {0},"),
                   ("CFRU", "src/Tables/item_tables.c", ".itemId = ITEM_MASTER_BALL,", ".itemId = ITEM_NONE,"),
                   ("CFRU", "strings/ability_name_table.string", "NAME_LAST_ABILITY", "NAME_UNKNOWN"),
                   ("CFRU", "src/config.h", "#define EXPANDED_NEW_ITEMS", "// #define EXPANDED_NEW_ITEMS")]
        for change in changes:
            with self.subTest(change=change[:2]), self.assertRaises(g.ProfileError):
                g.make_profile(self.mutate_source(*change))

    def test_layout_and_address_source_mutations_fail(self):
        changes = [("CFRU", "include/pokemon.h", "u8 split;", "u16 split;"),
                   ("CFRU", "include/pokemon.h", "typedef struct Pokemon\n{\n\tu32 personality;",
                    "typedef struct Pokemon\n{\n\tu16 personality;"),
                   ("CFRU", "include/battle.h", "u8 \tivSpread[6];", "u8 \tivSpread[7];"),
                   ("CFRU", "include/battle.h", "extern u16 gBattlerPartyIndexes", "extern u8 gBattlerPartyIndexes"),
                   ("CFRU", "include/new/rom_locs.h", "0x80001BC", "0x80001BD"),
                   ("CFRU", "BPRE.ld", "gBattleMons = 0x2023BE4;", "gBattleMons = 0x8023BE4;")]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(g.ProfileError):
                g.make_profile(self.mutate_source(*change))

    def test_schema_pin_missing_unknown_key_mapping_layout_rejected(self):
        mutations = [lambda p: p["metadata"].update(schemaVersion=1),
                     lambda p: p["metadata"].update(schemaVersion=True),
                     lambda p: p["metadata"]["revisions"].update(CFRU="0" * 40),
                     lambda p: p.pop("moves"), lambda p: p.update(unreviewed=True),
                     lambda p: p["species"][1].update(id=2),
                     lambda p: p["moves"][991].update(name="guessed"),
                     lambda p: p["layouts"]["records"]["Pokemon"].update(size=80),
                     lambda p: p["addresses"]["gBaseStats"].update(kind="pointer-slot"),
                     lambda p: p["addresses"]["gBaseStats"].update(sourceAddress="080001BC")]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index), self.assertRaises(g.ProfileError):
                p = copy.deepcopy(self.profile)
                mutate(p)
                p["metadata"].pop("profileId")
                p["metadata"]["profileId"] = "sha256:" + g.digest(g.serialized(p))
                g.validate_profile(p, self.profile)

    def test_byte_identical_regeneration_and_committed_manifest(self):
        regenerated = g.make_profile(self.reader())
        self.assertEqual(g.serialized(regenerated), g.serialized(self.profile))
        self.assertEqual((ROOT / g.OUTPUT).read_bytes(), g.serialized(regenerated))
        g.validate_profile(json.loads(g.serialized(regenerated)), self.profile)


if __name__ == "__main__":
    unittest.main()
