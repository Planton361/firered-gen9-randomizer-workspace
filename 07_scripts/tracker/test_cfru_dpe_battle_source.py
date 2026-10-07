#!/usr/bin/env python3
"""#693 source/ABI binding and protected isolation; public tracked text only."""
import json
from pathlib import Path
import re
import subprocess
import unittest

import generate_cfru_dpe_source_data as source

ROOT = Path(__file__).resolve().parents[2]
EXT = Path("03_tools/tracker-extensions/CFRUDPEExtension")
BASE = "bacec6e5c6719063524aae8a164a73b9ca25e82c"


class BattleSourceTests(unittest.TestCase):
    def test_production_party_profile_generator_and_gitlinks_unchanged(self):
        for path in (EXT / "CFRUDPEExtension.lua", EXT / "source_party_decoder.lua",
                     EXT / "profile_sha256.lua", EXT / "data/source-data.json",
                     Path("07_scripts/tracker/generate_cfru_dpe_source_data.py")):
            expected = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes(), expected, str(path))
        def gitlinks(ref):
            rows = subprocess.check_output(["git", "ls-tree", "-r", ref], cwd=ROOT).splitlines()
            return [row for row in rows if row.startswith(b"160000 ")]
        self.assertEqual(gitlinks("HEAD"), gitlinks(BASE))

    def test_module_is_detached_and_has_no_host_or_private_io(self):
        module = (ROOT / EXT / "source_battle_decoder.lua").read_text()
        self.assertNotRegex(module, r"\b(?:Memory|memory|emu|GameSettings|Program|PokemonData)\s*[.:]")
        self.assertNotRegex(module, r"\b(?:io\.open|os\.execute|require|loadstring|load|loadfile)\s*\(")
        self.assertEqual(module.count("dofile("), 2)
        self.assertIn('dofile(ROOT .. "/source_party_decoder.lua")', module)
        self.assertIn('dofile(ROOT .. "/profile_sha256.lua")', module)
        self.assertNotIn(".local.json", module)
        self.assertNotIn("offsets.ini", module)
        production = (ROOT / EXT / "CFRUDPEExtension.lua").read_text()
        self.assertNotIn("source_battle_decoder", production)

    def test_decoder_widths_offsets_match_accepted_target_abi(self):
        profile = json.loads((ROOT / EXT / "data/source-data.json").read_text())
        record = profile["layouts"]["records"]["BattlePokemon"]
        module = (ROOT / EXT / "source_battle_decoder.lua").read_text()
        self.assertEqual(int(re.search(r"local SIZE = (\d+)", module)[1]), record["size"])
        abi = module.split("local ABI =", 1)[1].split("local function", 1)[0]
        fields = re.findall(r"(\w+)=\{(\d+),(\d+)\}", abi)
        self.assertEqual(len(fields), 13)
        for name, offset, width in fields:
            expected = record["fields"][name]
            self.assertEqual(int(offset), expected["offset"], name)
            self.assertEqual(int(width), {"u8": 1, "u16": 2, "u32": 4,
                                         "u16[4]": 2, "u8[4]": 1}[expected["type"]], name)
        self.assertEqual(profile["limits"]["MAX_BATTLERS_COUNT"]["value"], 4)
        self.assertTrue(profile["metadata"]["configuration"]["FROSTBITE"])

    def test_trainer_b_and_mapping_use_exact_pinned_public_declarations(self):
        profile = json.loads((ROOT / EXT / "data/source-data.json").read_text())
        reader = source.LockedSources(ROOT)
        multi = reader.read("CFRU", "include/new/multi.h")
        entry = profile["metadata"]["inputs"]["CFRU:include/new/multi.h"]
        self.assertEqual(source.digest(multi.encode()), entry["sha256"])
        module = (ROOT / EXT / "source_battle_decoder.lua").read_text()
        self.assertIn(entry["sha256"], module)
        self.assertRegex(multi, r"#define\s+gTrainerBattleOpponent_B\s+ExtensionState.trainerBTrainerId\b")
        battle = reader.read("CFRU", "include/battle.h")
        for declaration in ("extern u16 gBattlerPartyIndexes[MAX_BATTLERS_COUNT];",
                            "extern u8 gBattlerPositions[MAX_BATTLERS_COUNT];",
                            "extern u8 gBattlersCount;", "extern u32 gBattleTypeFlags;"):
            self.assertIn(declaration, battle)
        self.assertIn("GetBattlerPosition(bank) & BIT_SIDE", battle)


if __name__ == "__main__":
    unittest.main()
