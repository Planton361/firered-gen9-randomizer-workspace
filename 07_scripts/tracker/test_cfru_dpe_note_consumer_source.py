"""#713 source-locked oracle, exact boundary and restricted-sandbox checks."""
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

import run_cfru_dpe_note_consumer_mock_tests as note
import run_cfru_dpe_host_consumer_mock_tests as stock

ALLOWED = {note.MODULE, note.HARNESS,
           '07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py',
           '07_scripts/tracker/test_cfru_dpe_note_consumer_source.py',
           'docs/tracker/T5_NOTE_CONSUMER_QUARANTINE_PHASE_A.md'}


class NoteConsumerSourceTests(unittest.TestCase):
    def test_exact_five_new_files_existing_bytes_and_ten_clean_gitlinks(self):
        rows = stock.git('diff', '--name-status', note.BASE).decode().splitlines()
        self.assertEqual({r.split('\t')[-1] for r in rows}, ALLOWED)
        self.assertTrue(all(r.startswith('A\t') for r in rows), rows)
        self.assertEqual(stock.git('branch', '--show-current').decode().strip(),
                         'feature/tracker-note-consumer-quarantine-mock')
        for path in ALLOWED:
            self.assertTrue((note.ROOT / path).is_file())
            self.assertNotEqual(subprocess.run(['git', 'cat-file', '-e', note.BASE + ':' + path],
                               cwd=note.ROOT, capture_output=True).returncode, 0)
        def links(ref):
            return [r for r in stock.git('ls-tree', '-r', ref).splitlines() if r.startswith(b'160000 ')]
        baseline = links(note.BASE)
        self.assertEqual(len(baseline), 10)
        self.assertEqual(links('HEAD'), baseline)
        self.assertEqual(baseline, links('3bdfe9919afc0b7bea55c79f37285e832be495c3'))
        for row in baseline:
            checkout = note.ROOT / row.split(b'\t')[1].decode()
            self.assertEqual(stock.git('rev-parse', 'HEAD', cwd=checkout).strip(), row.split()[2])
            self.assertEqual(stock.git('status', '--porcelain', '--untracked-files=no', cwd=checkout), b'')
        self.assertEqual(stock.git('diff', '--check', note.BASE), b'')

    def test_four_getters_match_independent_frozen_ranges_and_digests(self):
        bodies, provenance = note.note_definitions()
        self.assertEqual(set(bodies), set(note.REVIEWED))
        for name, (first, last, digest) in note.REVIEWED.items():
            self.assertEqual((provenance[name]['first'], provenance[name]['last'], provenance[name]['sha256']),
                             (first, last, digest))
        self.assertIn('pokemonID * 1000 + level', bodies['Tracker.getMoves'])
        self.assertIn('trackedPokemon.abilities or', bodies['Tracker.getAbilities'])
        self.assertIn('trackedPokemon.note or ""', bodies['Tracker.getNote'])
        self.assertIn('return trackedPokemon.eL', bodies['Tracker.getLastLevelSeen'])

    def test_original_digest_drift_fails_before_lua(self):
        real = stock.extract
        def changed(text, name):
            body, first, last = real(text, name)
            return body + '\n', first, last
        with patch.object(stock, 'extract', changed):
            with self.assertRaisesRegex(ValueError, 'Unreviewed original note getter'):
                note.note_definitions()

    def test_existing_bridge_and_bootstrap_dependencies_are_immutable(self):
        note.payload()
        original = Path.read_bytes
        for filename in ('source_host_field_bridge.lua', 'source_preconsumer_guard.lua'):
            def drift(path):
                value = original(path)
                return value + b'\n-- drift' if path.name == filename else value
            with patch.object(Path, 'read_bytes', drift):
                with self.assertRaisesRegex(ValueError, 'Accepted dependency drift'):
                    note.payload()

    def test_internal_bridge_only_no_runtime_channels_or_retained_history(self):
        module = (note.ROOT / note.MODULE).read_text()
        self.assertEqual(module.count('dofile('), 1)
        self.assertIn('dofile(ROOT.."/source_host_field_bridge.lua")', module)
        self.assertIn('bridgeModule.newMock(host,expected,bodies,raw,sources,multi)', module)
        for method in ('installMock', 'transitionMock', 'submitMock', 'contextMock', 'selectMock', 'teardownMock'):
            self.assertIn('bridge.' + method + '(', module)
        self.assertEqual(module.count('_historical'), 1)
        self.assertNotRegex(module, r'\b(?:Tracker|TrackerAPI|Memory|memory|emu|gui|FileManager|DataHelper|TrackerScreen|BattleDetailsScreen)\s*[.:]')
        self.assertNotRegex(module, r'\b(?:require|load|loadfile|loadstring|io\.open|os\.execute)\s*\(')
        self.assertNotIn('_G', module)
        production = (note.ROOT / note.EXT / 'CFRUDPEExtension.lua').read_text()
        self.assertNotIn('source_note_consumer_quarantine', production)

    def test_original_and_gate_environments_have_executable_traps(self):
        chunk, _ = note.payload()
        self.assertIn('trustedLoad(GATE_SOURCE,"@"..GATE_PATH,"t",gateEnv)', chunk)
        self.assertIn('eq(gateForbidden,0)', chunk)
        self.assertIn('state.fixtureFrozen=frozen', chunk)
        self.assertIn("trustedLoad(body,'@PIN/'..name,'t',env)", chunk)
        self.assertIn('NOTE_ORIGINAL_EXECUTIONS', chunk)
        self.assertIn('NOTE_ORACLE_STUB_EXECUTIONS', chunk)
        self.assertIn('zero(s)', chunk)
        harness = (note.ROOT / note.HARNESS).read_text()
        self.assertNotRegex(harness, r'\b(?:dofile|loadfile|require)\s*\(')
        for name in ('recordBattleMoveByPokemonLevel', 'saveData', 'loadData', 'loadFromFile',
                     'saveToFile', 'buildTrackerScreenDisplay'):
            self.assertIn('trap("Tracker.' + name + '")' if name not in ('buildTrackerScreenDisplay', 'loadFromFile', 'saveToFile')
                          else ('trap("DataHelper.buildTrackerScreenDisplay")' if name == 'buildTrackerScreenDisplay'
                                else 'trap("Tracker.AutoSave.' + name + '")'), harness)

    def test_no_private_discovery_or_compilation_artifacts(self):
        for path in ('07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py',
                     '07_scripts/tracker/test_cfru_dpe_note_consumer_source.py'):
            text = (note.ROOT / path).read_text()
            self.assertNotRegex(text, r'\b(?:glob|rglob|walk)\(')
            compile(text, path, 'exec')
        text = (note.ROOT / '07_scripts/tracker/run_cfru_dpe_note_consumer_mock_tests.py').read_text()
        self.assertIn("if {t.id() for t in tests} & exclusions != exclusions:", text)
        self.assertIn('Historical suite drift', text)


if __name__ == '__main__':
    unittest.main()
