"""#711 exact five-file boundary, immutable provenance and isolation checks."""
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import run_cfru_dpe_host_field_bridge_mock_tests as bridge
import run_cfru_dpe_host_consumer_mock_tests as stock

ALLOWED = {
    bridge.MODULE, bridge.HARNESS,
    '07_scripts/tracker/run_cfru_dpe_host_field_bridge_mock_tests.py',
    '07_scripts/tracker/test_cfru_dpe_host_field_bridge_source.py',
    'docs/tracker/T5_HOST_FIELD_BRIDGE_PHASE_A.md',
}


class HostFieldBridgeSourceTests(unittest.TestCase):
    def test_exact_five_added_paths_all_existing_bytes_and_ten_gitlinks(self):
        rows = stock.git('diff', '--name-status', bridge.BASE).decode().splitlines()
        self.assertEqual({r.split('\t')[-1] for r in rows}, ALLOWED)
        self.assertTrue(all(r.startswith('A\t') for r in rows), rows)
        self.assertEqual(stock.git('branch', '--show-current').decode().strip(),
                         'feature/tracker-host-field-bridge-mock')
        for path in ALLOWED:
            self.assertTrue((bridge.ROOT / path).is_file())
            missing = subprocess.run(['git', 'cat-file', '-e', bridge.BASE + ':' + path],
                                     cwd=bridge.ROOT, capture_output=True)
            self.assertNotEqual(missing.returncode, 0, path)
        def links(ref):
            return [r for r in stock.git('ls-tree', '-r', ref).splitlines() if r.startswith(b'160000 ')]
        baseline = links(bridge.BASE)
        self.assertEqual(len(baseline), 10)
        self.assertEqual(links('HEAD'), baseline)
        self.assertEqual(baseline, links('3bdfe9919afc0b7bea55c79f37285e832be495c3'))
        for row in baseline:
            checkout = bridge.ROOT / row.split(b'\t')[1].decode()
            self.assertEqual(stock.git('rev-parse', 'HEAD', cwd=checkout).strip(), row.split()[2])
            self.assertEqual(stock.git('status', '--porcelain', '--untracked-files=no', cwd=checkout), b'')

    def test_internal_guard_is_only_snapshot_source(self):
        module = (bridge.ROOT / bridge.MODULE).read_text()
        self.assertEqual(module.count('dofile('), 1)
        self.assertIn('dofile(ROOT .. "/source_preconsumer_guard.lua")', module)
        self.assertIn('guardModule.newMock(host,expected,bodies,raw,sources,multi)', module)
        for method in ('installMock', 'transitionMock', 'submitMock', 'readMock', 'teardownMock'):
            self.assertIn('guard.' + method + '(', module)
        self.assertNotRegex(module, r'\b(?:Memory|memory|emu|gui|Tracker|TrackerAPI|FileManager|GameSettings)\s*[.:]')
        self.assertNotRegex(module, r'\b(?:require|load|loadfile|loadstring|io\.open|os\.execute)\s*\(')
        self.assertNotIn('_G', module)
        self.assertNotIn('source_party_decoder.lua', module)
        self.assertNotIn('source_battle_decoder.lua', module)
        production = (bridge.ROOT / bridge.EXT / 'CFRUDPEExtension.lua').read_text()
        self.assertNotIn('source_host_field_bridge', production)

    def test_accepted_dependencies_are_immutable_and_drift_blocks_execution(self):
        bridge.payload()
        original = Path.read_bytes
        def drift(path):
            data = original(path)
            return data + b'\n--drift' if path.name == 'source_preconsumer_guard.lua' else data
        with patch.object(Path, 'read_bytes', drift):
            with self.assertRaisesRegex(ValueError, 'Accepted dependency drift'):
                bridge.payload()

    def test_original_accessor_bodies_are_selection_only(self):
        selected, _ = stock.definitions()
        for name in ('TrackerAPI.getPlayerPokemon', 'TrackerAPI.getEnemyPokemon',
                     'TrackerAPI.getActiveBattlePokemon', 'Battle.getViewedPokemon'):
            self.assertNotIn('Memory.', selected[name])
        self.assertIn('Tracker.getPokemon', selected['Battle.getViewedPokemon'])
        self.assertIn('Battle.numBattlers > 2', selected['TrackerAPI.getActiveBattlePokemon'])
        chunk, _ = bridge.payload()
        self.assertIn("trustedLoad(body,'@PIN/'..name,'t',env)", chunk)
        self.assertIn('eq(#s.readLog,0); eq(#s.violations,0)', chunk)
        self.assertIn('BRIDGE_ORIGINAL_EXECUTIONS', chunk)
        harness = (bridge.ROOT / bridge.HARNESS).read_text()
        self.assertNotRegex(harness, r'\b(?:dofile|loadfile|require)\s*\(')
        self.assertIn('ORACLE_SYNTHETIC_STUB', harness)
        self.assertIn('EXPECTED_STOCK_HAZARD', chunk)

    def test_no_private_discovery_and_python_compiles_in_memory(self):
        for path in ('07_scripts/tracker/run_cfru_dpe_host_field_bridge_mock_tests.py',
                     '07_scripts/tracker/test_cfru_dpe_host_field_bridge_source.py'):
            text = (bridge.ROOT / path).read_text()
            self.assertNotRegex(text, r'\b(?:glob|rglob|walk)\(')
            compile(text, path, 'exec')


if __name__ == '__main__':
    unittest.main()
