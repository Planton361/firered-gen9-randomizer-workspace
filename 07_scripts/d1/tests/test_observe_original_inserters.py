"""Synthetic RAM I/O only. Never launch a sandbox, tool, component or build."""
import copy
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
o = importlib.import_module('observe_original_inserters')
v = o.v


def make_store(files=None):
    root = Path('/synthetic-component')
    files = {'BPRE0.gba': b'abcdefghijklmnop', 'build/output.bin': b'CODE',
             'config.h': b'#define SYNTHETIC 1\n'} if files is None else files
    def reader(path):
        key = path.relative_to(root).as_posix()
        if key not in files:
            raise FileNotFoundError()
        return files[key]
    stream = io.BytesIO()
    store = o.RamStore(root, reader, o.Journal(stream))
    return store, stream, files


def replay(store, stream, files, actual=None):
    snapshots = {key: files[key] for key in store.snapshots}
    verifier = v.JournalVerifier(snapshots)
    stream.seek(0)
    for row in o.journal_rows(stream):
        verifier.consume(row)
    verifier.finish(bytes(store.data['test.gba']) if actual is None else actual,
                    store.write_count, store.binding.hexdigest())
    return verifier


def policy():
    doc = {'allocations': [], 'owners': [], 'overrides': [], 'config': o.sha(b'synthetic')}
    for c, start in (('dpe', v.DPE_START), ('cfru', v.CFRU_START)):
        doc['allocations'].append({'id': c, 'component': c, 'kind': 'payload',
                                   'start': start, 'end': start + 0x40000,
                                   'basis': 'independent_reservation'})
    cursors = {'dpe': v.DPE_START, 'cfru': v.CFRU_START}
    for role, length in v.REQUIRED_ROLES.items():
        c = 'dpe' if role.startswith('native_') or role == 'evolution_rows' else 'cfru'
        start = (cursors[c] + 3) // 4 * 4
        end = start + (length or 32)
        cursors[c] = end
        doc['owners'].append({'id': role, 'component': c, 'roles': [role],
                              'start': start, 'end': end, 'allocation': c,
                              'basis': 'independent_link_and_input_map'})
    return doc


def write(start, data=b'ABCD', phase='bytepatch', kind='data'):
    return {'op': 'write', 'key': 'test.gba', 'handle': 0, 'phase': phase, 'kind': kind,
            'source_line': 1, 'source_function': 'synthetic', 'start': start,
            'length': len(data), 'data': data.hex(), 'before': o.sha(b'old!')}


class IoTests(unittest.TestCase):
    def test_original_fixture_writes_are_captured_in_actual_order(self):
        store, stream, files = make_store()
        # Execute a synthetic original, rather than simulate its resulting diff.
        source = """def main():
    copy('BPRE0.gba', 'test.gba')
    with open('test.gba', 'rb+') as rom:
        rom.seek(2)
        rom.write(b'XY')
        rom.seek(2)
        rom.write(b'XY')  # unchanged writes still count
        rom.seek(0)
        assert rom.read(4) == b'abXY'
"""
        namespace = {'copy': store.copy, 'open': store.open}
        exec(compile(source, '<synthetic original>', 'exec'), namespace)
        store.phase = 'bytepatch'
        namespace['main']()
        self.assertEqual(2, store.write_count)
        verifier = replay(store, stream, files)
        self.assertEqual(b'abXYefghijklmnop', bytes(verifier.files['test.gba']))
        self.assertEqual(b'abcdefghijklmnop', files['BPRE0.gba'])

    def test_every_original_rom_write_phase_and_source_class(self):
        for c in ('dpe', 'cfru'):
            store, stream, files = make_store()
            store.copy('BPRE0.gba', 'test.gba')
            with store.open('test.gba', 'rb+') as rom:
                for phase in v.PHASES[c]:
                    if phase in v.NO_ROM_WRITES:
                        continue
                    store.phase = phase
                    rom.seek(0)
                    rom.write(phase.encode())
            replay(store, stream, files)
            rows = list(o.journal_rows(io.BytesIO(stream.getvalue())))
            self.assertEqual([p for p in v.PHASES[c] if p not in v.NO_ROM_WRITES],
                             [e['phase'] for e in rows if e['op'] == 'write'])
            self.assertEqual(set(v.PHASES[c]), set(o.PHASE_LINES[c].values()))

    def test_append_expand_seek_and_text_cache_truncate(self):
        store, stream, files = make_store()
        store.copy('BPRE0.gba', 'test.gba')
        with store.open('test.gba', 'rb+') as rom:
            self.assertEqual(16, rom.seek(0, 2))
            rom.write(b'\xff' * 32)
            rom.seek(-2, 1)
            self.assertEqual(b'\xff\xff', rom.read())
        with store.open('generatedrepoints', 'w') as cache:
            cache.write('synthetic 123\n')
        with store.open('generatedrepoints', 'a') as cache:
            cache.write('another 456\n')
        with store.open('offsets.ini', 'w') as offsets:
            offsets.write('remove me')
        with store.open('offsets.ini', 'r+') as offsets:
            offsets.truncate(0)
            offsets.write('fresh')
        replay(store, stream, files)

    def test_missing_and_double_recorded_unchanged_writes_are_detected(self):
        store, stream, files = make_store()
        store.copy('BPRE0.gba', 'test.gba')
        with store.open('test.gba', 'rb+') as rom:
            rom.write(b'abcd')  # no final diff
        rows = list(o.journal_rows(io.BytesIO(stream.getvalue())))
        event = next(e for e in rows if e['op'] == 'write')
        for changed in ([e for e in rows if e is not event], rows[:-1] + [event] + rows[-1:]):
            with self.subTest(events=len(changed)):
                verifier = v.JournalVerifier({k: files[k] for k in store.snapshots})
                with self.assertRaises(v.Invalid):
                    for row in changed:
                        verifier.consume(row)
                    verifier.finish(bytes(store.data['test.gba']), store.write_count, store.binding.hexdigest())

    def test_output_preimage_reader_seek_and_file_alias_mismatch(self):
        store, stream, files = make_store()
        store.copy('BPRE0.gba', 'test.gba')
        with store.open('test.gba', 'rb+') as rom:
            rom.seek(2)
            rom.read(4)
            rom.seek(2)
            rom.write(b'NEW')
        with self.assertRaises(v.Invalid):
            replay(store, stream, files, actual=b'wrong output')
        rows = list(o.journal_rows(io.BytesIO(stream.getvalue())))
        for op, field, value in (('read', 'sha256', o.sha(b'wrong')),
                                 ('seek', 'position', 9), ('write', 'before', o.sha(b'wrong')),
                                 ('write', 'key', 'config.h')):
            altered = copy.deepcopy(rows)
            next(e for e in altered if e['op'] == op)[field] = value
            verifier = v.JournalVerifier({k: files[k] for k in store.snapshots})
            with self.assertRaises(v.Invalid):
                for event in altered:
                    verifier.consume(event)

    def test_rejected_paths_writers_fileno_seek_and_rom_truncate(self):
        for path, mode in (('../outside', 'r'), ('/outside', 'r'), ('build/output.bin', 'w'),
                           ('config.h', 'rb+'), ('config.h', 'invalid')):
            store, _, _ = make_store()
            with self.assertRaises(o.Stop):
                store.open(path, mode)
            self.assertTrue(store.denied)
        for operation in ('seek', 'truncate', 'fileno', 'read_only_write'):
            store, _, _ = make_store()
            store.copy('BPRE0.gba', 'test.gba')
            with store.open('test.gba', 'rb' if operation == 'read_only_write' else 'rb+') as rom:
                with self.assertRaises(o.Stop):
                    if operation == 'seek': rom.seek(-1)
                    elif operation == 'truncate': rom.truncate(0)
                    elif operation == 'fileno': rom.fileno()
                    else: rom.write(b'bad')

    def test_journal_and_memory_limits_stop_without_sampling(self):
        j = o.Journal(io.BytesIO(), max_events=1, max_bytes=1000)
        j.emit('copy', src='a', dst='b')
        with self.assertRaises(o.Stop): j.emit('copy', src='a', dst='b')
        self.assertTrue(j.stopped)
        j = o.Journal(io.BytesIO(), max_bytes=1)
        with self.assertRaises(o.Stop): j.emit('copy', src='a', dst='b')
        with self.assertRaises(v.Missing): v.JournalVerifier({'large': b'123'}, limit=2)
        store, _, _ = make_store()
        with patch.object(o, 'MEMORY_LIMIT', 1):
            with self.assertRaises(o.Stop): store.open('BPRE0.gba', 'rb')

    def test_unrecognized_effect_and_failed_subprocess_are_rejected(self):
        verifier = v.JournalVerifier({})
        for event in ({'op': 'os_write'}, {'op': 'subprocess', 'returncode': 1}):
            with self.assertRaises(v.Invalid): verifier.consume(event)
        for command in (['sh', '-c', 'touch x'], ['git', 'diff', '--output=x'],
                        ['arm-none-eabi-nm', 'different.o'], 'shell string'):
            with self.assertRaises(o.Stop): o.command_kind(command, Path('/synthetic'))

    def test_sandbox_is_read_only_and_stdout_flags_latch_failures(self):
        cmd = o.sandbox_command('/usr/bin/bwrap', Path('/synthetic'), Path('/ignored/evidence'), Path('/ignored/cfg'))
        self.assertIn('--unshare-all', cmd)
        self.assertEqual(['/', '/'], cmd[cmd.index('--ro-bind') + 1:cmd.index('--ro-bind') + 3])
        self.assertEqual(['/ignored/evidence', '/ignored/evidence'], cmd[cmd.index('--bind') + 1:cmd.index('--bind') + 3])
        sink = o.OutputSink()
        sink.write('Symbol missing: PRIVATE_SYMBOL')
        self.assertTrue(sink.failed)


class OwnershipTests(unittest.TestCase):
    def test_overlay_one_byte_boundary_and_wrong_order(self):
        p = policy()
        p['allocations'].append({'id': 'tail', 'component': 'cfru', 'kind': 'overlay',
                                 'start': v.DPE_START - 32, 'end': v.DPE_START,
                                 'basis': 'independent_reservation'})
        p['owners'].append({'id': 'overlay', 'component': 'cfru', 'roles': ['overlay'],
                            'start': v.DPE_START - 32, 'end': v.DPE_START, 'allocation': 'tail',
                            'basis': 'independent_link_and_input_map'})
        c = o.OwnerChecks(p)
        c.check('cfru', write(v.DPE_START - 32, b'x' * 32, 'overlays'))
        with self.assertRaises(v.Missing):
            o.OwnerChecks(p).check('cfru', write(v.DPE_START - 32, b'x' * 33, 'overlays'))
        with self.assertRaises(v.Invalid):
            c.check('cfru', write(v.CFRU_START, b'bad', 'bytepatch'))

    def test_large_dynamic_reservation_and_foreign_owner(self):
        p = policy()
        start, length = 0x900000, 3_778_560
        p['allocations'].append({'id': 'large', 'component': 'cfru', 'kind': 'dynamic',
                                 'start': start, 'end': start + length,
                                 'basis': 'independent_reservation'})
        p['owners'].append({'id': 'large_owner', 'component': 'cfru', 'roles': ['dynamic'],
                            'start': start, 'end': start + length, 'allocation': 'large',
                            'basis': 'independent_link_and_input_map'})
        o.OwnerChecks(p).allocation({'op': 'allocate', 'start': start, 'length': length})
        with self.assertRaises(v.Invalid):
            o.OwnerChecks(p).allocation({'op': 'allocate', 'start': start, 'length': length + 1})
        p['owners'][-1]['allocation'] = None
        with self.assertRaises(v.Invalid): o.OwnerChecks(p)

    def test_missing_owner_and_pointer_target_are_rejected(self):
        c = o.OwnerChecks(policy())
        with self.assertRaises(v.Missing): c.check('dpe', write(0x1234))
        start = c.owners['oak_record']['start']
        with self.assertRaises(v.Invalid):
            c.check('cfru', write(start, b'\0' * 4, 'repoints', 'pointer'))

    def test_observed_reviewed_cross_override_and_unknown_alias(self):
        p = policy()
        p['owners'].append({'id': 'shared', 'component': 'dpe', 'roles': ['reviewed_shared_patch'],
                            'start': 0x1000, 'end': 0x1004, 'allocation': None,
                            'basis': 'independent_link_and_input_map'})
        a, b = write(0x1000), write(0x1000, b'WXYZ')
        b['before'] = o.sha(bytes.fromhex(a['data']))
        edge = {'earlier': 'dpe_0', 'later': 'cfru_0', 'start': 0x1000, 'end': 0x1004,
                'basis': 'reviewed_dpe_to_cfru_patch', 'review': {
                    'reference': 'SYNTHETIC_ONLY', 'decision_sha256': o.sha(b'synthetic decision'),
                    'owner': 'shared', 'config': p['config'],
                    'sources': {c: v.SOURCES[c] for c in ('dpe', 'cfru')},
                    'earlier_write': v.write_binding(a, 'dpe'), 'later_write': v.write_binding(b, 'cfru')}}
        p['overrides'] = [edge]
        c = o.OwnerChecks(p)
        c.check('dpe', a); c.check('cfru', b)
        self.assertEqual(set(c.overrides), c.seen_overrides)
        for basis in ('reviewed_source_order', 'unreviewed'):
            edge['basis'] = basis
            c = o.OwnerChecks(p); c.check('dpe', a)
            with self.assertRaises(v.Invalid): c.check('cfru', b)
        p['owners'][-1]['roles'] = ['protected']
        c = o.OwnerChecks(p); c.check('dpe', a)
        with self.assertRaises(v.Invalid): c.check('cfru', b)


class WorkerFixtureTests(unittest.TestCase):
    def test_actual_worker_entry_executes_only_synthetic_original(self):
        self.exercise("""import shutil
shutil.copyfile('BPRE0.gba', 'test.gba')
with open('test.gba', 'rb+') as f:
    f.seek(1)
    f.write(b'NEW')
""", 'PASS')

    def test_missing_symbol_output_is_latched_failure(self):
        self.exercise("print('Symbol missing: SYNTHETIC')\n", 'FAIL')

    def test_caught_unsupported_effect_cannot_clear_stop(self):
        self.exercise("""import subprocess
try:
    subprocess.run(['sh', '-c', 'NEVER_EXECUTED'])
except BaseException:
    pass
""", 'UNKNOWN')

    def exercise(self, source, outcome):
        real_open = open
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            scratch = root / 'evidence'; scratch.mkdir()
            (root / 'scripts/insert.py').write_text(source)
            cfg = root / 'worker.json'
            cfg.write_text(json.dumps({'root': str(root), 'scratch': str(scratch),
                                       'component': 'dpe', 'nonce': 'synthetic'}))
            def synthetic_open(path, mode='r', *args, **kwargs):
                if Path(path) == root / 'BPRE0.gba':
                    return io.BytesIO(b'abcdefgh')  # No ROM file exists on disk.
                return real_open(path, mode, *args, **kwargs)
            with patch('builtins.open', side_effect=synthetic_open), \
                 patch.object(o, 'SOURCE_HASHES', {'dpe': o.sha(source.encode())}), \
                 patch.object(sys, 'path', list(sys.path)), patch.object(sys, 'argv', []), \
                 patch.object(o.subprocess, 'run') as process:
                code = o.worker(str(cfg))
            process.assert_not_called()
            report = json.loads((scratch / 'report.json').read_text())
            self.assertEqual(outcome, report['outcome'])
            self.assertEqual(0 if outcome == 'PASS' else 2, code)
            self.assertFalse((root / 'test.gba').exists())
            self.assertFalse((root / 'BPRE0.gba').exists())
            if outcome == 'PASS':
                self.assertEqual(b'aNEWefgh', (scratch / 'ram-output.bin').read_bytes())
                snapshots = {'BPRE0.gba': b'abcdefgh'}
                verifier = v.JournalVerifier(snapshots)
                with (scratch / 'operations.jsonl').open('rb') as stream:
                    for event in o.journal_rows(stream):
                        verifier.consume(event)
                verifier.finish(b'aNEWefgh', report['write_count'], report['write_binding'])


class SanitizerTests(unittest.TestCase):
    def test_no_arguments_unknown_and_private_errors_never_leak(self):
        for args, error in (([], None), (['--plan', 'SECRET'], PermissionError('SECRET_PATH HASH')),
                            (['--plan', 'SECRET'], ValueError('PRIVATE_SYMBOL'))):
            out = io.StringIO()
            with patch.object(o, 'bounded_read', side_effect=error or RuntimeError('PRIVATE')), patch('sys.stdout', out):
                self.assertIn(o.main(args), (1, 2))
            self.assertNotIn('SECRET', out.getvalue())
            self.assertNotIn('PRIVATE', out.getvalue())
            for line, gate in zip(out.getvalue().splitlines(), o.GATES):
                self.assertRegex(line, '^' + gate + '=(PASS|FAIL|UNKNOWN)$')
            self.assertIn('D1_ALL=UNKNOWN' if error is None or isinstance(error, PermissionError) else 'D1_ALL=FAIL', out.getvalue())

    def test_internal_entry_cannot_bypass_isolation(self):
        with patch.object(o, 'sandbox_guard', side_effect=v.Invalid()), patch.object(o, 'worker') as worker:
            self.assertEqual(2, o.main(['--internal-worker', 'SYNTHETIC_CONFIG']))
        worker.assert_not_called()

    def test_native_claims_in_plan_cannot_promote_gates(self):
        result = o.run_user({'schema': 2, 'scratch': 'ignored', 'ownership': {}, 'native_pass': True}, Path('/synthetic'))
        self.assertEqual('FAIL', result['D1_ALL'])
        for gate in ('D1_FULL_NATIVE_OWNERSHIP', 'D1_ABI_RELOCATION_SEMANTICS',
                     'D1_SOURCE_CONFIG_BUILD_PROVENANCE', 'D1_DPE_REPRODUCIBILITY'):
            self.assertEqual('UNKNOWN', result[gate])

    def test_stale_snapshot_nonce_or_incomplete_report_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'config.txt').write_bytes(b'current config')
            report = {'nonce': 'current', 'completed': True,
                      'snapshots': {'config.txt': o.sha(b'stale config')}}
            with self.assertRaises(v.Invalid):
                o.verify_live_stage(root, root, report, 'current', lambda e: None)
            report['nonce'] = 'stale nonce'
            with self.assertRaises(v.Invalid):
                o.verify_live_stage(root, root, report, 'current', lambda e: None)
            report.update(nonce='current', completed=False)
            with self.assertRaises(v.Invalid):
                o.verify_live_stage(root, root, report, 'current', lambda e: None)

    def test_unavailable_isolation_stops_before_any_inserter(self):
        fake_git = lambda root, *args: ((v.SOURCES['dpe'] if str(root).endswith('Dynamic-Pokemon-Expansion-Gen-9')
                                      else v.SOURCES['cfru'] if str(root).endswith('CFRU-expansion')
                                      else v.SOURCES['upr']) + '\n').encode() if args[:1] == ('rev-parse',) else b''
        with patch.object(o, 'git', side_effect=fake_git), patch.object(o, 'bounded_read', return_value=b'fixture'), \
             patch.object(o, 'SOURCE_HASHES', dict.fromkeys(('dpe', 'cfru'), o.sha(b'fixture'))), \
             patch.object(o.shutil, 'which', return_value=None), patch.object(o.Path, 'is_dir', return_value=True), \
             patch.object(o.subprocess, 'run') as process:
            result = o.run_user({'schema': 2, 'scratch': 'ignored', 'ownership': {}}, Path('/synthetic'))
        process.assert_not_called()
        self.assertEqual('UNKNOWN', result['D1_ALL'])
        self.assertEqual('UNKNOWN', result['D1_ORIGINAL_EXECUTION'])


if __name__ == '__main__':
    unittest.main()
