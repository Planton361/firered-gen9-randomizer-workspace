#!/usr/bin/env python3
"""#692 isolation/safety checks; public source and tracked Git objects only."""
import hashlib
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
EXT = Path("03_tools/tracker-extensions/CFRUDPEExtension")
BASE = "35576d3c8e6a219ee1da3e72197f46d31ac89c49"


class PartySourceTests(unittest.TestCase):
    def test_accepted_guard_generator_profile_and_gitlinks_unchanged(self):
        for path in (EXT / "CFRUDPEExtension.lua", EXT / "profile_sha256.lua",
                     EXT / "data/source-data.json",
                     Path("07_scripts/tracker/generate_cfru_dpe_source_data.py")):
            expected = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes(), expected, str(path))
        def gitlinks(ref):
            rows = subprocess.check_output(["git", "ls-tree", "-r", ref], cwd=ROOT).splitlines()
            return [row for row in rows if row.startswith(b"160000 ")]
        self.assertEqual(gitlinks("HEAD"), gitlinks(BASE))

    def test_detached_module_only_loads_existing_public_hash_helper(self):
        module = (ROOT / EXT / "source_party_decoder.lua").read_text()
        self.assertNotRegex(module, r"\b(?:Memory|memory|emu|GameSettings|Program|PokemonData)\s*[.:]")
        self.assertNotRegex(module, r"\b(?:io\.open|os\.execute|require|loadstring|load|loadfile)\s*\(")
        self.assertEqual(module.count("dofile("), 1)
        self.assertIn('dofile(ROOT .. "/profile_sha256.lua")', module)
        self.assertNotIn(".local.json", module)
        self.assertNotIn("offsets.ini", module)
        extension = (ROOT / EXT / "CFRUDPEExtension.lua").read_text()
        self.assertNotIn("source_party_decoder", extension)

    def test_full_canonical_lock_and_explicit_test_only_live_unknown(self):
        raw = (ROOT / EXT / "data/source-data.json").read_bytes()
        module = (ROOT / EXT / "source_party_decoder.lua").read_text()
        self.assertIn(hashlib.sha256(raw).hexdigest(), module)
        self.assertIn('evidence="TEST_ONLY", liveConfidence="UNKNOWN"', module)
        self.assertIn('field("UNKNOWN", nil, reason)', module)
        self.assertIn('field("UNAVAILABLE", nil, reason)', module)
        self.assertIn('sha256(sources[locator]) == input.sha256', module)


if __name__ == "__main__":
    unittest.main()
