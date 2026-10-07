#!/usr/bin/env python3
"""Phase A boundaries and public lock checks; no runtime/game inputs."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
EXT = ROOT / "03_tools/tracker-extensions/CFRUDPEExtension"


class ExtensionSourceTests(unittest.TestCase):
    def test_source_lock_binds_entire_unchanged_t1_serialization(self):
        raw = (EXT / "data/source-data.json").read_bytes()
        lua = (EXT / "CFRUDPEExtension.lua").read_text()
        expected = re.search(r'local SOURCE_SHA256 = "([0-9a-f]{64})"', lua)[1]
        self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)
        profile = json.loads(raw)
        self.assertEqual(profile["metadata"]["schemaVersion"], 2)
        self.assertIn(profile["metadata"]["profileId"], lua)
        self.assertIn(profile["metadata"]["revisions"]["Tracker"], lua)
        self.assertEqual(len(raw), 1092720)
        for descriptor in profile["addresses"].values():
            self.assertEqual(descriptor["runtimeAddress"], "UNRESOLVED")
        for capability in profile["capabilities"].values():
            self.assertEqual(capability["confidence"], "UNKNOWN")
            self.assertIsNone(capability["sampleEpoch"])

    def test_extension_has_no_filesystem_import_or_memory_mutation_calls(self):
        for filename in ("CFRUDPEExtension.lua", "profile_sha256.lua"):
            source = (EXT / filename).read_text()
            self.assertNotRegex(source, r'\b(?:Memory|memory|emu)\s*[.:]\s*write\w*\s*\(')
            self.assertNotRegex(source, r'\b(?:io\.open|decodeJsonFile|loadGameSettingsFromJson|loadTrackerOverridesFromJson)\s*\(')
            self.assertNotRegex(source, r'\b(?:os\.execute|loadstring|require)\s*\(')
        source = (EXT / "CFRUDPEExtension.lua").read_text()
        self.assertNotIn(".local.json", source)
        self.assertNotIn("offsets.ini", source)

    def test_pinned_early_stop_and_persistent_restart_seams(self):
        main = (ROOT / "02_external/Ironmon-Tracker/ironmon_tracker/Main.lua").read_text()
        self.assertLess(main.index("CustomCode.beforeGameDataLoad()"), main.index("GameSettings.initialize()"))
        self.assertLess(main.index('GameSettings.gamename == "Unsupported Game"'),
                        main.index('FileManager.executeEachFile("initialize"'))
        self.assertIn("return IronmonTracker.startTracker()", main)
        entry = (ROOT / "02_external/Ironmon-Tracker/Ironmon-Tracker.lua").read_text()
        self.assertIn("if IronmonTracker == nil then", entry)
        self.assertNotIn("IronmonTracker = {}", entry)
        settings = (ROOT / "02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua").read_text().splitlines()
        self.assertEqual(settings[283], "function GameSettings.initialize()")

    def test_mock_dependencies_and_allowlist_target_existing_nested_consumers(self):
        profile = json.loads((EXT / "data/source-data.json").read_text())
        required = set()
        for capability in ("playerParty", "enemyParty"):
            for dep in profile["capabilities"][capability]["dependencies"]:
                self.assertTrue(dep in profile or dep in profile["layouts"]["records"] or dep in profile["addresses"])
                if dep in profile["addresses"]:
                    required.add(dep)
        self.assertEqual(required, {"gPlayerParty", "gPlayerPartyCount", "gEnemyParty"})
        for symbol in required:
            self.assertEqual(profile["addresses"][symbol]["kind"], "fixed-symbol")
        program = (ROOT / "02_external/Ironmon-Tracker/ironmon_tracker/Program.lua").read_text()
        for field in ("sizeofPokemonStruct", "sizeofBaseStatsPokemon", "sizeofBattleMove", "sizeofBattlePokemon"):
            consumers = program + (ROOT / "02_external/Ironmon-Tracker/ironmon_tracker/data/MoveData.lua").read_text()
            self.assertTrue("Program.Addresses." + field in consumers, field + " consumer missing")
        pokemon = (ROOT / "02_external/Ironmon-Tracker/ironmon_tracker/data/PokemonData.lua").read_text()
        for field in ("offsetTypes", "offsetAbilities"):
            self.assertTrue("PokemonData.Addresses." + field in pokemon, field + " consumer missing")


if __name__ == "__main__":
    unittest.main()
