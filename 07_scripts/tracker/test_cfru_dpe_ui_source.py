#!/usr/bin/env python3
"""#694 Phase A isolation and unchanged accepted boundaries; tracked text only."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
EXT = Path("03_tools/tracker-extensions/CFRUDPEExtension")
BASE = "ed38910a7931855e1fad6aa871e1931a26fed659"


class UIProjectionSourceTests(unittest.TestCase):
    def test_production_decoders_profile_generator_and_gitlinks_unchanged(self):
        for path in (EXT / "CFRUDPEExtension.lua", EXT / "source_party_decoder.lua",
                     EXT / "source_battle_decoder.lua", EXT / "profile_sha256.lua",
                     EXT / "data/source-data.json",
                     Path("07_scripts/tracker/generate_cfru_dpe_source_data.py")):
            expected = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
            self.assertEqual((ROOT / path).read_bytes(), expected, str(path))
        def gitlinks(ref):
            rows = subprocess.check_output(["git", "ls-tree", "-r", ref], cwd=ROOT).splitlines()
            return [row for row in rows if row.startswith(b"160000 ")]
        self.assertEqual(gitlinks("HEAD"), gitlinks(BASE))

    def test_projection_has_no_host_sink_or_private_io(self):
        module = (ROOT / EXT / "source_ui_projection.lua").read_text()
        self.assertNotRegex(module, r"\b(?:Memory|memory|emu|GameSettings|Program|Tracker|TrackerAPI|FileManager|gui|forms)\s*[.:]")
        self.assertNotRegex(module, r"\b(?:io\.open|os\.execute|require|loadstring|load|loadfile)\s*\(")
        self.assertNotIn("_G", module)
        self.assertEqual(re.findall(r'dofile\(ROOT .. "(/[^\"]+)"\)', module),
                         ["/source_party_decoder.lua", "/source_battle_decoder.lua"])
        self.assertEqual(module.count("dofile("), 2)
        self.assertNotIn(".local.json", module)
        self.assertNotIn("offsets.ini", module)
        self.assertNotIn("source_ui_projection", (ROOT / EXT / "CFRUDPEExtension.lua").read_text())

    def test_runner_only_reuses_allowlisted_committed_sources(self):
        runner = (ROOT / "07_scripts/tracker/run_cfru_dpe_ui_mock_tests.py").read_text()
        self.assertIn("ROOT, PUBLIC_SOURCES", runner)
        self.assertIn('reader.read("CFRU", "include/new/multi.h")', runner)
        self.assertIn("source.LockedSources(ROOT)", runner)
        self.assertNotRegex(runner, r"(?:glob|rglob|os\.walk|open)\(")
        self.assertNotIn(".local.json", runner)
        self.assertNotIn("offsets.ini", runner)
        self.assertEqual(re.findall(r'\.read_text\(\)', runner), [".read_text()"])


if __name__ == "__main__":
    unittest.main()
