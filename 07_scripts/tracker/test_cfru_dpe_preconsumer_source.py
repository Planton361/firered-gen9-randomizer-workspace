#!/usr/bin/env python3
"""#709 source provenance, five-file boundary and synthetic execution isolation."""
import hashlib
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import run_cfru_dpe_preconsumer_mock_tests as guard
import run_cfru_dpe_host_consumer_mock_tests as stock
from test_cfru_dpe_host_consumer_source import REVIEWED

ALLOWED = {
    guard.EXT + 'source_preconsumer_guard.lua',
    '07_scripts/tracker/run_cfru_dpe_preconsumer_mock_tests.py',
    guard.HARNESS,
    '07_scripts/tracker/test_cfru_dpe_preconsumer_source.py',
    'docs/tracker/T5_PRECONSUMER_GUARD_PHASE_A.md',
}


class PreconsumerSourceTests(unittest.TestCase):
    def test_exact_five_new_paths_existing_files_and_ten_clean_gitlinks(self):
        rows = stock.git('diff', '--name-status', guard.BASE).decode().splitlines()
        paths = {row.split('\t')[-1] for row in rows}
        self.assertTrue(paths <= ALLOWED, rows)
        self.assertTrue(all(row.startswith('A\t') for row in rows), rows)
        if stock.git('rev-parse', 'HEAD').decode().strip() != guard.BASE:
            self.assertEqual(paths, ALLOWED)
        for path in ALLOWED:
            self.assertTrue((guard.ROOT / path).is_file())
            missing = subprocess.run(['git', 'cat-file', '-e', guard.BASE + ':' + path],
                                     cwd=guard.ROOT, capture_output=True)
            self.assertNotEqual(missing.returncode, 0, path)
        def links(ref):
            return [r for r in stock.git('ls-tree', '-r', ref).splitlines() if r.startswith(b'160000 ')]
        self.assertEqual(len(links('HEAD')), 10)
        self.assertEqual(links('HEAD'), links(guard.BASE))
        self.assertEqual(links('HEAD'), links('3bdfe9919afc0b7bea55c79f37285e832be495c3'))
        for row in links('HEAD'):
            checkout = guard.ROOT / row.split(b'\t')[1].decode()
            self.assertEqual(stock.git('rev-parse', 'HEAD', cwd=checkout).strip(), row.split()[2])
            self.assertEqual(stock.git('status', '--porcelain', '--untracked-files=no', cwd=checkout), b'')

    def test_all_original_definitions_keep_independent_hashes_and_boundaries(self):
        selected, proof = stock.definitions()
        self.assertEqual(set(selected), set(REVIEWED))
        for name, (first, last, digest) in REVIEWED.items():
            self.assertEqual((proof[name]['first'], proof[name]['last'], proof[name]['sha256']),
                             (first, last, digest), name)
        module = (guard.ROOT / guard.EXT / 'source_preconsumer_guard.lua').read_text()
        for name in ('Program.readNewPokemon', 'Program.updatePokemonTeams',
                     'Battle.updateViewSlots', 'Battle.beginNewBattle'):
            self.assertIn(REVIEWED[name][2], module)

    def test_early_save_state_precedes_the_actual_late_hook(self):
        selected, _ = stock.definitions()
        begin = selected['Battle.beginNewBattle']
        self.assertLess(begin.index('GameOverScreen.createTempSaveState()'),
                        begin.index('CustomCode.afterBattleBegins()'))
        self.assertIn('Utils.bit_xor', selected['Program.readNewPokemon'])
        self.assertIn('Memory.readbyte(GameSettings.gBattlerPartyIndexes)', selected['Battle.updateViewSlots'])
        self.assertIn('move.pp = tonumber(MoveData.Moves[move.id].pp)', selected['Program.updatePokemonTeams'])

    def test_production_and_all_accepted_dependencies_byte_identical(self):
        paths = [guard.EXT + name for name in (
            'CFRUDPEExtension.lua', 'source_party_decoder.lua', 'source_battle_decoder.lua',
            'source_ui_projection.lua', 'profile_sha256.lua', 'data/source-data.json')]
        paths += [guard.STOCK_HARNESS, '07_scripts/tracker/generate_cfru_dpe_source_data.py',
                  '07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py']
        for path in paths:
            self.assertEqual((guard.ROOT / path).read_bytes(), stock.git('show', guard.BASE + ':' + path), path)
        production = (guard.ROOT / guard.EXT / 'CFRUDPEExtension.lua').read_text()
        self.assertNotIn('source_preconsumer_guard', production)

    def test_public_profile_and_bootstrap_drift_rejected_before_execution(self):
        original = Path.read_bytes
        def drift(path):
            raw = original(path)
            return raw + b'\n--synthetic drift' if str(path).endswith(guard.STOCK_HARNESS) else raw
        with patch.object(Path, 'read_bytes', drift):
            with self.assertRaisesRegex(ValueError, 'bootstrap/controls drift'):
                guard.inputs()
        original_text = Path.read_text
        def profile_drift(path, *args, **kwargs):
            text = original_text(path, *args, **kwargs)
            return text + '\n' if path.name == 'source-data.json' else text
        with patch.object(Path, 'read_text', profile_drift):
            with self.assertRaisesRegex(ValueError, 'public profile drift'):
                guard.inputs()

    def test_original_source_drift_rejected_before_execution(self):
        original = stock.definitions
        def drift():
            bodies, proof = original()
            proof['Battle.beginNewBattle']['sha256'] = '0' * 64
            return bodies, proof
        with patch.object(stock, 'definitions', drift):
            with self.assertRaisesRegex(ValueError, 'Unreviewed original body'):
                guard.inputs()

    def test_guard_has_only_reviewed_dependencies_and_no_stock_delegation(self):
        module = (guard.ROOT / guard.EXT / 'source_preconsumer_guard.lua').read_text()
        self.assertNotRegex(module, r'\b(?:Memory|memory|emu|gui|forms|Tracker|TrackerAPI|GameSettings|FileManager)\s*[.:]')
        self.assertNotRegex(module, r'\b(?:io\.open|os\.execute|require|loadstring|load|loadfile)\s*\(')
        self.assertNotIn('_G', module)
        self.assertNotRegex(module, r'\b(?:original|start)\s*\(')
        self.assertEqual(module.count('dofile('), 3)
        for name in ('source_party_decoder.lua', 'source_battle_decoder.lua', 'profile_sha256.lua'):
            self.assertIn('dofile(ROOT .. "/' + name + '")', module)

    def test_payload_is_bounded_and_retains_all_63_stock_controls(self):
        selected, _, _, _, _, controls = guard.inputs()
        accepted = stock.git('show', guard.BASE + ':' + guard.STOCK_HARNESS).decode()
        self.assertEqual(hashlib.sha256(accepted.encode()).hexdigest(), guard.STOCK_SHA)
        self.assertNotIn(guard.FOOTER, controls)
        self.assertIn("trustedLoad(body,'@PIN/'..name,'t',env)", controls)
        self.assertNotIn('dump=string.dump', controls)
        self.assertIn('("x").dump(function() end)', controls)
        self.assertEqual(set(selected), set(REVIEWED))
        harness = (guard.ROOT / guard.HARNESS).read_text()
        self.assertNotRegex(harness, r'\b(?:dofile|require|loadfile)\s*\(')
        self.assertIn('eq(stockCount,0)', harness)
        self.assertIn('eq(#s.readLog,0); eq(#s.violations,0)', harness)
        runner = (guard.ROOT / '07_scripts/tracker/run_cfru_dpe_preconsumer_mock_tests.py').read_text()
        self.assertNotRegex(runner, r'\b(?:glob|rglob|walk)\(')


if __name__ == '__main__':
    unittest.main()
