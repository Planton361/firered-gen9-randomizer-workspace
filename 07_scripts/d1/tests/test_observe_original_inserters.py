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
    def test_path_open_write_target_and_copy_denials_keep_fixed_reasons(self):
        cases = (
            ('PATH_POLICY', lambda s: s.key(7)),
            ('PATH_POLICY', lambda s: s.open('../PRIVATE', 'r')),
            ('PATH_POLICY', lambda s: s.open('/PRIVATE', 'r')),
            ('PATH_POLICY', lambda s: s.copy('BPRE0.gba', '../PRIVATE')),
            ('OPEN_MODE', lambda s: s.open('PRIVATE', 'invalid')),
            ('OPEN_MODE', lambda s: s.open('PRIVATE', opener='PRIVATE')),
            ('WRITE_TARGET', lambda s: s.open('PRIVATE', 'w')),
            ('COPY_CONTRACT', lambda s: s.copy('PRIVATE', 'test.gba')),
            ('COPY_CONTRACT', lambda s: s.copy('BPRE0.gba', 'PRIVATE')),
            ('COPY_CONTRACT', lambda s: s.copy('BPRE0.gba', 'test.gba', follow_symlinks=False)),
        )
        for reason, operation in cases:
            with self.subTest(reason=reason):
                store, stream, _ = make_store()
                with self.assertRaises(o.Stop) as stopped:
                    operation(store)
                self.assertTrue(store.denied)
                self.assertEqual('UNSUPPORTED_IO', stopped.exception.category)
                self.assertEqual('UNSUPPORTED_IO', store.journal.stop_category)
                self.assertEqual(reason, store.journal.io_stop_reason)
                self.assertEqual(b'', stream.getvalue())
                self.assertEqual((), stopped.exception.args)
        store, _, _ = make_store()
        with patch.object(Path, 'is_symlink', return_value=True), self.assertRaises(o.Stop):
            store.key('PRIVATE')
        self.assertEqual('PATH_POLICY', store.journal.io_stop_reason)

    def test_ram_file_denials_keep_method_specific_reasons(self):
        cases = (
            ('seek', (-1,), False, 'SEEK_RULE'),
            ('seek', ('PRIVATE',), False, 'SEEK_RULE'),
            ('seek', (0, 3), False, 'SEEK_RULE'),
            ('seek', (0,), True, 'SEEK_RULE'),
            ('read', (-2,), False, 'READ_RULE'),
            ('read', ('PRIVATE',), False, 'READ_RULE'),
            ('read', (), True, 'READ_RULE'),
            ('write', (b'PRIVATE',), False, 'WRITE_RULE'),
            ('write', (b'PRIVATE',), True, 'WRITE_RULE'),
            ('truncate', (0,), False, 'TRUNCATE_RULE'),
            ('truncate', (0,), True, 'TRUNCATE_RULE'),
            ('fileno', (), False, 'FILENO_RULE'),
        )
        for method, args, closed, reason in cases:
            with self.subTest(method=method, closed=closed, args=args):
                store, _, _ = make_store()
                with store.open('BPRE0.gba', 'rb') as file:
                    if closed:
                        file.close()
                    with self.assertRaises(o.Stop):
                        getattr(file, method)(*args)
                self.assertTrue(store.denied)
                self.assertEqual('UNSUPPORTED_IO', store.journal.stop_category)
                self.assertEqual(reason, store.journal.io_stop_reason)
        for size in (-1, 'PRIVATE'):
            store, _, _ = make_store()
            with store.open('generatedrepoints', 'wb') as file:
                with self.assertRaises(o.Stop):
                    file.truncate(size)
            self.assertEqual('TRUNCATE_RULE', store.journal.io_stop_reason)
        store, _, _ = make_store()
        store.copy('BPRE0.gba', 'test.gba')
        with store.open('test.gba', 'rb+') as file:
            with self.assertRaises(o.Stop): file.truncate(0)
        self.assertEqual('TRUNCATE_RULE', store.journal.io_stop_reason)

    def test_first_stop_category_and_io_reason_are_latched_together(self):
        for first_category, first_reason, expected in (
                ('UNSUPPORTED_IO', 'PATH_POLICY', 'PATH_POLICY'),
                ('UNSUPPORTED_IO', 'UNKNOWN', 'UNKNOWN'),
                ('RESOURCE_LIMIT', 'PATH_POLICY', 'UNKNOWN')):
            with self.subTest(category=first_category, reason=first_reason):
                store, _, _ = make_store()
                for category, reason in ((first_category, first_reason),
                                         ('UNSUPPORTED_IO', 'OPEN_MODE'), ('MEMORY_ERROR', 'UNKNOWN')):
                    with self.assertRaises(o.Stop): store.deny(category, reason)
                self.assertEqual(first_category, store.journal.stop_category)
                self.assertEqual(expected, store.journal.io_stop_reason)

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
        self.assertEqual('RESOURCE_LIMIT', j.stop_category)
        j = o.Journal(io.BytesIO(), max_bytes=1)
        with self.assertRaises(o.Stop): j.emit('copy', src='a', dst='b')
        self.assertEqual('RESOURCE_LIMIT', j.stop_category)
        with self.assertRaises(v.Missing): v.JournalVerifier({'large': b'123'}, limit=2)
        store, _, _ = make_store()
        with patch.object(o, 'MEMORY_LIMIT', 1):
            with self.assertRaises(o.Stop): store.open('BPRE0.gba', 'rb')
        self.assertEqual('RESOURCE_LIMIT', store.journal.stop_category)

    def test_ram_seek_write_and_truncate_budgets_are_resource_stops(self):
        for operation in ('seek', 'write', 'truncate'):
            with self.subTest(operation=operation):
                store, _, _ = make_store()
                with store.open('generatedrepoints', 'wb') as cache:
                    with patch.object(o, 'MEMORY_LIMIT', 4), self.assertRaises(o.Stop):
                        if operation == 'seek': cache.seek(5)
                        elif operation == 'truncate': cache.truncate(5)
                        else: cache.write(b'12345')
                self.assertTrue(store.denied)
                self.assertEqual('RESOURCE_LIMIT', store.journal.stop_category)

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
""", 'UNKNOWN', 'UNSUPPORTED_SUBPROCESS')

    def test_unsupported_io_is_reported_even_when_caught(self):
        self.exercise("""try:
    open('config.h', 'w')
except BaseException:
    pass
""", 'UNKNOWN', 'UNSUPPORTED_IO', io_reason='WRITE_TARGET')

    def test_worker_reports_each_io_reason_without_private_arguments(self):
        operations = {
            'PATH_POLICY': "open('../PRIVATE', 'r')",
            'OPEN_MODE': "open('PRIVATE', 'invalid')",
            'WRITE_TARGET': "open('PRIVATE', 'w')",
            'COPY_CONTRACT': "import shutil\nshutil.copyfile('PRIVATE', 'PRIVATE')",
            'SEEK_RULE': "with open('generatedrepoints', 'wb') as f:\n    f.seek(-1)",
            'READ_RULE': "with open('generatedrepoints', 'wb') as f:\n    f.read(-2)",
            'WRITE_RULE': "f = open('generatedrepoints', 'wb')\nf.close()\nf.write(b'PRIVATE')",
            'TRUNCATE_RULE': "with open('generatedrepoints', 'wb') as f:\n    f.truncate(-1)",
            'FILENO_RULE': "with open('generatedrepoints', 'wb') as f:\n    f.fileno()",
        }
        for reason, source in operations.items():
            with self.subTest(reason=reason):
                self.exercise(source + '\n', 'UNKNOWN', 'UNSUPPORTED_IO', io_reason=reason)

    def test_worker_probes_use_path_policy_without_calling_foreign_fallback(self):
        for probe in ('isfile', 'exists', 'getsize'):
            with self.subTest(probe=probe):
                self.exercise("import os\nos.path." + probe + "('../PRIVATE')\n",
                              'UNKNOWN', 'UNSUPPORTED_IO', io_reason='PATH_POLICY')

    def test_caught_io_denial_keeps_first_reason_after_later_denials(self):
        self.exercise("""try:
    open('../PRIVATE', 'r')
except BaseException:
    pass
try:
    open('PRIVATE', 'invalid')
except BaseException:
    pass
raise RuntimeError('PRIVATE')
""", 'UNKNOWN', 'UNSUPPORTED_IO', io_reason='PATH_POLICY')

    def test_subprocess_options_are_rejected_before_launch(self):
        self.exercise("import subprocess\nsubprocess.run(['git', 'diff'], shell=True)\n",
                      'UNKNOWN', 'UNSUPPORTED_SUBPROCESS')

    def test_subprocess_nonzero_launch_failure_and_timeout_are_distinguished(self):
        for returncode, error, category in (
                (1, None, 'SUBPROCESS_FAILURE'),
                (None, FileNotFoundError('PRIVATE_PATH'), 'SUBPROCESS_FAILURE'),
                (None, o.subprocess.CalledProcessError(1, ['PRIVATE']), 'SUBPROCESS_FAILURE'),
                (None, o.subprocess.TimeoutExpired(['PRIVATE'], 1), 'RESOURCE_LIMIT'),
                (None, MemoryError('PRIVATE'), 'MEMORY_ERROR'),
                (None, RuntimeError('PRIVATE'), 'UNEXPECTED_EXCEPTION')):
            with self.subTest(category=category, error=type(error)):
                self.exercise("""import subprocess
try:
    subprocess.check_output(['git', 'diff'])
except BaseException:
    pass
""", 'UNKNOWN', category, returncode=returncode, process_error=error)

    def test_memory_error_and_unexpected_exception_keep_original_outcomes(self):
        self.exercise("raise MemoryError('PRIVATE_PATH HASH OFFSET')\n", 'UNKNOWN', 'MEMORY_ERROR')
        self.exercise("raise RuntimeError('PRIVATE_PATH HASH OFFSET')\n", 'FAIL', 'UNEXPECTED_EXCEPTION')
        self.exercise("from observe_original_inserters import Stop\nraise Stop()\n", 'UNKNOWN')

    def test_journal_limit_remains_latched_when_caught(self):
        with patch.object(o, 'MAX_LINE', 1):
            self.exercise("""try:
    open('generatedrepoints', 'w')
except BaseException:
    pass
""", 'UNKNOWN', 'RESOURCE_LIMIT')

    def test_ram_budget_is_reported_without_real_memory_exhaustion(self):
        with patch.object(o, 'MEMORY_LIMIT', 1024):
            self.exercise("with open('generatedrepoints', 'w') as f:\n    f.write('x' * 1025)\n",
                          'UNKNOWN', 'RESOURCE_LIMIT')

    def test_first_concrete_cause_survives_cleanup_and_later_exception(self):
        self.exercise("""import subprocess
try:
    open('config.h', 'w')
except BaseException:
    pass
try:
    subprocess.run(['sh', '-c', 'NEVER_EXECUTED'])
except BaseException:
    pass
raise MemoryError('PRIVATE')
""", 'UNKNOWN', 'UNSUPPORTED_IO', io_reason='WRITE_TARGET')
        # A failing subprocess precedes a journal-budget failure recording it.
        with patch.object(o, 'MAX_LINE', 1):
            self.exercise("import subprocess\nsubprocess.run(['git', 'diff'])\n",
                          'UNKNOWN', 'SUBPROCESS_FAILURE', returncode=1)

    def test_unknown_cause_can_be_replaced_only_by_first_concrete_category(self):
        journal = o.Journal(io.BytesIO())
        for value in ('PRIVATE\nPATH', None, [], 'UNKNOWN'):
            journal.note_stop(value)
            self.assertEqual('UNKNOWN', journal.stop_category)
        journal.note_stop('RESOURCE_LIMIT')
        journal.note_stop('UNSUPPORTED_IO')
        self.assertEqual('RESOURCE_LIMIT', journal.stop_category)
        self.assertEqual((), o.Stop('PRIVATE').args)
        self.assertEqual('UNKNOWN', o.Stop('PRIVATE').category)

    def exercise(self, source, outcome, category='UNKNOWN', returncode=None, process_error=None,
                 io_reason='UNKNOWN'):
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
                 patch.object(o.subprocess, 'run', side_effect=process_error,
                              return_value=o.subprocess.CompletedProcess(['synthetic'], returncode, stdout=b'')) as process:
                code = o.worker(str(cfg))
            if returncode is None and process_error is None:
                process.assert_not_called()
            else:
                process.assert_called_once()
            report = json.loads((scratch / 'report.json').read_text())
            self.assertEqual(outcome, report['outcome'])
            self.assertEqual(category, report['stop_category'])
            self.assertEqual(io_reason, report['io_stop_reason'])
            self.assertEqual(outcome == 'PASS', report['completed'])
            self.assertNotIn('PRIVATE', json.dumps(report))
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


class DiscoveryTests(unittest.TestCase):
    def test_actual_noops_and_zero_writes_keep_ids_and_exact_conflicts(self):
        store, stream, files = make_store()
        store.copy('BPRE0.gba', 'test.gba')
        store.phase = 'repoint_all'
        with store.open('test.gba', 'rb+') as rom:
            for _ in range(2):
                rom.seek(0)
                rom.write(b'abcd')
            rom.write(b'')
        census_stream = io.BytesIO()
        census = o.Discovery(census_stream, '.local/synthetic')
        verifier = v.JournalVerifier({k: files[k] for k in store.snapshots})
        for row in o.journal_rows(io.BytesIO(stream.getvalue())):
            verifier.consume(row)
            census.consume('dpe', row)
        verifier.finish(bytes(store.data['test.gba']), store.write_count, store.binding.hexdigest())
        later = write(1, b'bcde', 'generated_repoints', 'pointer')
        census.consume('cfru', later)
        rows = list(o.journal_rows(io.BytesIO(census_stream.getvalue())))
        writes = [r for r in rows if r['op'] == 'write_candidate']
        self.assertEqual(['dpe_0', 'dpe_1', 'dpe_2', 'cfru_0'], [r['id'] for r in writes])
        self.assertTrue(all(r['unchanged'] for r in writes[:3]))
        conflicts = [r for r in rows if r['op'] == 'intersection_candidate']
        self.assertEqual([('dpe_0', 'dpe_1'), ('dpe_0', 'cfru_0'), ('dpe_1', 'cfru_0')],
                         [(r['earlier'], r['later']) for r in conflicts])
        self.assertEqual(v.write_binding(later, 'cfru'), conflicts[-1]['later_write'])
        self.assertTrue(all(r['basis'] is None for r in conflicts))
        self.assertEqual([], census.plan['ownership']['overrides'])
        with self.assertRaises(v.Missing): o.OwnerChecks(census.plan['ownership'])

    def test_large_allocation_is_fact_without_reservation_or_owner_grant(self):
        stream = io.BytesIO()
        census = o.Discovery(stream, '.local/synthetic')
        request = {'op': 'allocate', 'start': 0x900000, 'length': 3_778_560}
        census.consume('cfru', request)
        rows = list(o.journal_rows(io.BytesIO(stream.getvalue())))
        self.assertEqual(request['start'] + request['length'], rows[-1]['end'])
        self.assertIsNone(rows[-1]['basis'])
        self.assertEqual([], census.plan['ownership']['allocations'])
        self.assertEqual([], census.plan['ownership']['owners'])
        for bad in (dict(request, start=0x900001), dict(request, length=v.ROM_LIMIT)):
            with self.assertRaises(v.Invalid): census.consume('cfru', bad)

    def test_worker_scanner_result_precedes_actual_write_in_verified_census(self):
        source = """import shutil
def FindFreeSpace(rom, length):
    rom.seek(0)
    assert rom.read() == b'abcdefgh'
    return 0x900000
def main():
    shutil.copyfile('BPRE0.gba', 'test.gba')
    with open('test.gba', 'rb+') as rom:
        FindFreeSpace(rom, 3778560)
        rom.seek(2)
        rom.write(b'XY')
main()
"""
        real_open = open
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'scripts/insert.py').write_text(source)
            evidence = root / 'evidence'; evidence.mkdir()
            cfg = root / 'worker.json'
            cfg.write_text(json.dumps({'root': str(root), 'scratch': str(evidence),
                                       'component': 'cfru', 'nonce': 'synthetic'}))
            def synthetic_open(path, mode='r', *args, **kwargs):
                return io.BytesIO(b'abcdefgh') if Path(path) == root / 'BPRE0.gba' else real_open(path, mode, *args, **kwargs)
            with patch('builtins.open', side_effect=synthetic_open), \
                 patch.object(o, 'SOURCE_HASHES', {'cfru': o.sha(source.encode())}), \
                 patch.object(o, 'PHASE_LINES', {'cfru': {1: 'free_bytepatch'}}), \
                 patch.object(sys, 'path', list(sys.path)), patch.object(sys, 'argv', []), \
                 patch.object(o.subprocess, 'run') as process:
                self.assertEqual(0, o.worker(str(cfg)))
            process.assert_not_called()
            report = json.loads((evidence / 'report.json').read_text())
            stream = io.BytesIO()
            census = o.Discovery(stream, '.local/synthetic')
            verifier = v.JournalVerifier({'BPRE0.gba': b'abcdefgh'})
            with (evidence / 'operations.jsonl').open('rb') as journal:
                for event in o.journal_rows(journal):
                    verifier.consume(event)
                    census.consume('cfru', event)
            verifier.finish(b'abXYefgh', report['write_count'], report['write_binding'])
            rows = list(o.journal_rows(io.BytesIO(stream.getvalue())))
            self.assertEqual(['review_required', 'allocation_request', 'write_candidate'], [r['op'] for r in rows])
            self.assertEqual(3_778_560, rows[1]['end'] - rows[1]['start'])
            self.assertEqual('free_bytepatch', rows[2]['phase'])
            self.assertFalse((root / 'BPRE0.gba').exists())
            self.assertFalse((root / 'test.gba').exists())

    def test_phase_order_unknown_class_and_overlay_boundary_fail_closed(self):
        for event in (write(v.DPE_START - 1, b'xx', 'overlays'),
                      write(0, phase='unknown'), write(0, kind='unknown'),
                      write(v.ROM_LIMIT, b'xx'), write(0, phase='copy')):
            with self.subTest(event=event):
                with self.assertRaises(v.Invalid):
                    o.Discovery(io.BytesIO(), '.local/synthetic').consume('cfru', event)
        census = o.Discovery(io.BytesIO(), '.local/synthetic')
        census.consume('cfru', write(v.DPE_START - 4, b'1234', 'overlays'))
        with self.assertRaises(v.Invalid): census.consume('cfru', write(0, phase='bytepatch'))
        with self.assertRaises(v.Invalid): census.consume('dpe', write(0))

    def test_budget_exhaustion_and_incomplete_census_never_emit_plan(self):
        census = o.Discovery(io.BytesIO(), '.local/synthetic')
        census.history_bytes = 128 * 1024 * 1024
        with self.assertRaises(v.Missing): census.consume('dpe', write(0))
        census = o.Discovery(io.BytesIO(), '.local/synthetic')
        census.journal.max_events = 1
        with self.assertRaises(o.Stop): census.consume('dpe', write(0))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'candidate.json'
            with self.assertRaises(v.Invalid): census.finish(path)
            self.assertFalse(path.exists())

    def test_partial_real_elf_candidates_require_review_and_missing_symbols_stay_missing(self):
        from test_validate_owner_write_sets import synthetic_arm_elf
        raw, installed, _ = synthetic_arm_elf()
        census = o.Discovery(io.BytesIO(), '.local/synthetic')
        census.consume('dpe', write(v.DPE_START, b'DPE', 'payload', 'bulk'))
        census.consume('cfru', write(v.CFRU_START, installed[v.CFRU_START:], 'payload', 'bulk'))
        census.linked_candidates('cfru', v.ArmElf(raw), installed)
        owners = census.plan['ownership']['owners']
        self.assertEqual(6, len(owners))  # No invented Pickup/Evolution/asset owners.
        self.assertTrue(all(r['basis'] is None for r in owners))
        with self.assertRaises(v.Missing): o.OwnerChecks(census.plan['ownership'])
        with self.assertRaises(v.Invalid):
            census.linked_candidates('cfru', v.ArmElf(raw), bytes(len(installed)))

    def test_shared_live_path_runs_without_plan_but_never_grants_ownership(self):
        self.exercise()

    def test_bad_journal_nonce_input_output_and_failed_stage_cannot_finish_candidate(self):
        for fault in ('binding', 'nonce', 'input', 'output', 'worker', 'source', 'ignore',
                      'unsupported', 'isolation'):
            with self.subTest(fault=fault): self.exercise(fault)

    def test_worker_stop_categories_return_without_changing_unknown_acceptance(self):
        for category in o.STOP_CATEGORIES:
            with self.subTest(category=category):
                result = self.exercise('worker', worker_category=category)
                self.assertEqual(category, result['D1_DPE_STOP_CATEGORY'])
                self.assertEqual('UNKNOWN', result['D1_CFRU_STOP_CATEGORY'])
                self.assertEqual('UNKNOWN', result['D1_ALL'])
                self.assertEqual('UNKNOWN', result['D1_ORIGINAL_EXECUTION'])

    def test_worker_fail_outcome_is_preserved_with_stop_diagnostic(self):
        result = self.exercise('worker', worker_category='UNEXPECTED_EXCEPTION', report_outcome='FAIL')
        self.assertEqual('UNEXPECTED_EXCEPTION', result['D1_DPE_STOP_CATEGORY'])
        self.assertEqual('FAIL', result['D1_ALL'])
        self.assertEqual('FAIL', result['D1_ORIGINAL_EXECUTION'])

    def test_cfru_stop_diagnostic_is_separate_from_completed_dpe_stage(self):
        result = self.exercise('cfru_worker', worker_category='UNSUPPORTED_IO')
        self.assertEqual('UNKNOWN', result['D1_DPE_STOP_CATEGORY'])
        self.assertEqual('UNSUPPORTED_IO', result['D1_CFRU_STOP_CATEGORY'])
        self.assertEqual('UNKNOWN', result['D1_ALL'])

    def test_untrusted_missing_and_invalid_report_categories_remain_unknown(self):
        for category in ('PRIVATE\nPATH=HASH', None, [], {}, 1):
            with self.subTest(category=category):
                result = self.exercise('worker', worker_category=category)
                self.assertEqual('UNKNOWN', result['D1_DPE_STOP_CATEGORY'])
                self.assertEqual('UNKNOWN', result['D1_ALL'])
        for fault in ('worker_missing', 'worker_bad_nonce', 'worker_bad_component'):
            with self.subTest(fault=fault):
                result = self.exercise(fault, worker_category='UNSUPPORTED_IO')
                self.assertEqual('UNKNOWN', result['D1_DPE_STOP_CATEGORY'])
                self.assertEqual('UNKNOWN', result['D1_ALL'])

    def test_worker_stage_timeout_is_resource_limit_and_still_unknown(self):
        result = self.exercise('worker_timeout')
        self.assertEqual('RESOURCE_LIMIT', result['D1_DPE_STOP_CATEGORY'])
        self.assertEqual('UNKNOWN', result['D1_ALL'])

    def test_worker_io_reasons_return_per_stage_without_promoting_gates(self):
        for reason in o.IO_STOP_REASONS:
            with self.subTest(reason=reason):
                result = self.exercise('worker', worker_category='UNSUPPORTED_IO', worker_io_reason=reason)
                self.assertEqual(reason, result['D1_DPE_IO_STOP_REASON'])
                self.assertEqual('UNSUPPORTED_IO', result['D1_DPE_STOP_CATEGORY'])
                self.assertEqual('UNKNOWN', result['D1_CFRU_IO_STOP_REASON'])
                self.assertEqual('UNKNOWN', result['D1_ALL'])
        result = self.exercise('cfru_worker', worker_category='UNSUPPORTED_IO', worker_io_reason='READ_RULE')
        self.assertEqual('UNKNOWN', result['D1_DPE_IO_STOP_REASON'])
        self.assertEqual('READ_RULE', result['D1_CFRU_IO_STOP_REASON'])

    def test_io_reason_is_unknown_for_invalid_unbound_or_non_io_reports(self):
        for reason in ('PRIVATE\nPATH=OFFSET', None, [], {}, 1):
            with self.subTest(reason=reason):
                result = self.exercise('worker', worker_category='UNSUPPORTED_IO', worker_io_reason=reason)
                self.assertEqual('UNKNOWN', result['D1_DPE_IO_STOP_REASON'])
        for fault in ('worker_missing', 'worker_bad_nonce', 'worker_bad_component', 'worker_legacy'):
            with self.subTest(fault=fault):
                result = self.exercise(fault, worker_category='UNSUPPORTED_IO', worker_io_reason='PATH_POLICY')
                self.assertEqual('UNKNOWN', result['D1_DPE_IO_STOP_REASON'])
        for category in o.STOP_CATEGORIES:
            if category != 'UNSUPPORTED_IO':
                result = self.exercise('worker', worker_category=category, worker_io_reason='PATH_POLICY')
                self.assertEqual('UNKNOWN', result['D1_DPE_IO_STOP_REASON'])
        result = self.exercise(worker_category='UNSUPPORTED_IO', worker_io_reason='PATH_POLICY')
        self.assertEqual('UNKNOWN', result['D1_DPE_IO_STOP_REASON'])

    def test_discovery_finishes_without_selected_cfru_output(self):
        self.exercise(cfru_output='missing')

    def test_discovery_ignores_stale_selected_cfru_output(self):
        self.exercise(cfru_output='stale')

    def test_discovery_dpe_output_mismatch_still_fails(self):
        result = self.exercise('output', cfru_output='missing')
        self.assertEqual('PASS', result['D1_INPUT_CHAIN'])
        self.assertEqual('FAIL', result['D1_OUTPUT_REPRODUCTION'])

    def test_discovery_cfru_elf_mismatch_still_fails(self):
        result = self.exercise('elf', cfru_output='missing')
        self.assertEqual('FAIL', result['D1_LINK_IMAGE'])

    def test_discovery_cfru_journal_mismatch_still_fails(self):
        result = self.exercise('cfru_binding', cfru_output='missing')
        self.assertEqual('FAIL', result['D1_IO_RECOMPUTATION'])

    def test_discovery_cfru_oak_mismatch_still_fails(self):
        result = self.exercise('oak', cfru_output='missing')
        self.assertEqual('FAIL', result['D1_OAK_LINK_SHAPE'])

    def test_plan_retains_missing_stale_and_matching_cfru_output_requirements(self):
        for state, expected in (('missing', 'UNKNOWN'), ('stale', 'FAIL'), ('matching', 'PASS')):
            with self.subTest(state=state):
                result = self.exercise(cfru_output=state, plan_mode=True)
                self.assertEqual(expected, result['D1_OUTPUT_REPRODUCTION'])

    def exercise(self, fault=None, cfru_output='matching', plan_mode=False,
                 worker_category='UNKNOWN', report_outcome='UNKNOWN', worker_io_reason='UNKNOWN'):
        """Original Workspace driver with synthetic RAM I/O, no native/artifact files."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scratch = root / '.local'; scratch.mkdir()
            initial = b'A' * 128
            dpe_output = bytearray(initial + b'\xff' * (1024 - len(initial)))
            dpe_output[512:516] = b'DPE!'
            cfru_ram = bytearray(dpe_output)
            cfru_ram[256:260] = b'CFRU'
            cfru_ram[260:264] = b'MAPS'
            outputs = {'dpe': bytes(dpe_output), 'cfru': bytes(cfru_ram)}
            selected_cfru = (None if cfru_output == 'missing' else
                             b'stale synthetic output' if cfru_output == 'stale' else outputs['cfru'])
            inputs = {'dpe': initial, 'cfru': outputs['dpe']}
            selected_reads = []
            def component(path):
                return next(c for c, relative in o.COMPONENTS.items() if str(path).startswith(str(root / relative)))
            def fake_git(path, *args):
                if args[0] == 'rev-parse':
                    return ((v.SOURCES[component(path)] if fault != 'source' else 'stale') + '\n').encode()
                if args[0] == 'check-ignore' and fault == 'ignore': raise v.Missing()
                return b''
            real_read = o.bounded_read
            def read(path, limit=o.MEMORY_LIMIT):
                if path.name == 'report.json': return real_read(path, limit)
                c = component(path)
                if path.name == 'insert.py': return b'synthetic source'
                if path.name == 'BPRE0.gba': return b'wrong' if fault == 'input' and c == 'cfru' else inputs[c]
                if path.name == 'test.gba':
                    selected_reads.append(c)
                    if c == 'cfru':
                        if selected_cfru is None: raise FileNotFoundError('synthetic output absent')
                        return selected_cfru
                    # Keep the initial DPE -> CFRU input-chain check valid so
                    # this fault exercises the DPE replay/output comparison.
                    return b'wrong' if fault == 'output' and selected_reads.count('dpe') > 1 else outputs[c]
                if path.name == 'ram-output.bin': return outputs[c]  # Handled below via real scratch read.
                if path.name == 'linked.o': return c.encode()
                if path.name == 'output.bin': return b'synthetic payload'
                if path.name == 'oak_intro_contract.s': return b'gOakIntroEligibility:\n.byte 0x00\n.Loak_eligibility_end:'
                raise AssertionError('Unexpected synthetic read')
            def all_reads(path, limit=o.MEMORY_LIMIT):
                return real_read(path, limit) if path.is_relative_to(scratch) else read(path, limit)
            def launch(command, **kwargs):
                self.assertIn('--unshare-all', command)
                self.assertEqual(['/', '/'], command[command.index('--ro-bind') + 1:command.index('--ro-bind') + 3])
                self.assertEqual(o.subprocess.DEVNULL, kwargs['stdout'])
                cfg = json.loads(Path(command[-1]).read_text())
                c, directory = cfg['component'], Path(cfg['scratch'])
                if fault == 'worker_timeout':
                    raise o.subprocess.TimeoutExpired(['PRIVATE'], 7200)
                if fault == 'worker_missing':
                    return o.subprocess.CompletedProcess(command, 2)
                with (directory / 'operations.jsonl').open('wb') as stream:
                    store = o.RamStore(Path(cfg['root']), lambda path: inputs[c], o.Journal(stream))
                    store.copy('BPRE0.gba', 'test.gba')
                    with store.open('test.gba', 'rb+') as rom:
                        if c == 'dpe':
                            store.phase = 'expand'; rom.seek(len(initial)); rom.write(b'\xff' * (1024 - len(initial)))
                        store.phase = 'payload'; rom.seek(512 if c == 'dpe' else 256)
                        rom.write(b'DPE!' if c == 'dpe' else b'CFRU')
                        if c == 'cfru':
                            store.phase = 'overlays'
                            rom.write(b'MAPS'); rom.seek(260); rom.write(b'MAPS')
                    if fault == 'unsupported': store.journal.emit('unobserved_write_class')
                (directory / 'ram-output.bin').write_bytes(store.data['test.gba'])
                report = {'nonce': 'stale' if fault in ('nonce', 'worker_bad_nonce') else cfg['nonce'],
                          'component': 'wrong' if fault == 'worker_bad_component' else c,
                          'outcome': report_outcome, 'stop_category': worker_category,
                          'io_stop_reason': worker_io_reason,
                          'completed': True, 'snapshots': store.snapshots,
                          'write_count': store.write_count, 'event_count': store.journal.count,
                          'write_binding': 'stale' if fault == 'binding' or (fault == 'cfru_binding' and c == 'cfru') else store.binding.hexdigest()}
                if fault == 'worker_legacy': report.pop('io_stop_reason')
                (directory / 'report.json').write_text(json.dumps(report))
                stopped = (fault and fault.startswith('worker')) or (fault == 'cfru_worker' and c == 'cfru')
                return o.subprocess.CompletedProcess(command, 2 if stopped else 0)
            def elf(raw):
                mock = unittest.mock.Mock()
                mock.payload.return_value = 0x08000000 + (512 if raw == b'dpe' else 256)
                if fault == 'elf' and raw == b'cfru': mock.payload.return_value += 4
                mock.symbol.side_effect = v.Missing()
                return mock
            def oak(elf, actual, bitmap):
                self.assertEqual(outputs['cfru'], actual)
                if fault == 'oak': raise v.Invalid()
                return 'UNKNOWN'
            # Isolate the strict output prerequisite; real policy checks have
            # their own unchanged tests. No policy is accepted in discovery.
            checked_policy = unittest.mock.Mock(owners={}, seen_overrides=set(), overrides={})
            with patch.object(o, 'git', side_effect=fake_git), \
                 patch.object(o, 'bounded_read', side_effect=all_reads), \
                 patch.object(o, 'SOURCE_HASHES', dict.fromkeys(('dpe', 'cfru'), o.sha(b'synthetic source'))), \
                 patch.object(o.shutil, 'which', return_value=None if fault == 'isolation' else '/synthetic/bwrap'), \
                 patch.object(o.subprocess, 'run', side_effect=launch) as process, \
                 patch.object(v, 'ROM_LIMIT', 1024), patch.object(v, 'DPE_START', 512), \
                 patch.object(v, 'CFRU_START', 256), patch.object(v, 'ArmElf', side_effect=elf), \
                 patch.object(v, 'verify_oak_link', side_effect=oak), \
                 patch.object(v, 'verify_linked_reservations'), \
                 patch.object(o, 'OwnerChecks', side_effect=None if plan_mode else AssertionError('Discovery must not require a policy'),
                              return_value=checked_policy):
                plan = {'schema': 2, 'scratch': '.local'}
                if plan_mode: plan['ownership'] = {}
                result = o.run_user(plan, root, discovery=not plan_mode)
            candidates = list(scratch.glob('d1-*/candidate-plan.json'))
            if plan_mode:
                self.assertIn('cfru', selected_reads)
                self.assertEqual([], candidates)
                if cfru_output == 'matching': self.assertEqual('PASS', result['D1_IO_RECOMPUTATION'])
                elif cfru_output == 'stale': self.assertEqual('FAIL', result['D1_ALL'])
                else: self.assertEqual('UNKNOWN', result['D1_ALL'])
            elif fault:
                self.assertEqual([], candidates)
                self.assertNotEqual('PASS', result['D1_DISCOVERY'])
                if fault in ('source', 'input', 'ignore', 'isolation'): process.assert_not_called()
            else:
                self.assertEqual(2, process.call_count)
                self.assertEqual('PASS', result['D1_DISCOVERY'])
                self.assertEqual('PASS', result['D1_IO_RECOMPUTATION'])
                self.assertEqual(1, len(candidates))
                candidate = json.loads(candidates[0].read_text())
                self.assertEqual([], candidate['ownership']['overrides'])
                with self.assertRaises(v.Missing): o.OwnerChecks(candidate['ownership'])
            if not plan_mode:
                self.assertNotIn('cfru', selected_reads)
                if fault != 'output': self.assertEqual('UNKNOWN', result['D1_OUTPUT_REPRODUCTION'])
                for gate in ('D1_CAPACITY', 'D1_DECLARED_OWNER_CHECKS', 'D1_REVIEWED_OVERRIDES'):
                    self.assertEqual('UNKNOWN', result[gate])
            for c in ('dpe', 'cfru'):
                self.assertFalse((root / o.COMPONENTS[c] / 'test.gba').exists())
            for gate in ('D1_FULL_NATIVE_OWNERSHIP', 'D1_ABI_RELOCATION_SEMANTICS',
                         'D1_SOURCE_CONFIG_BUILD_PROVENANCE', 'D1_DPE_REPRODUCIBILITY',
                         'D1_RESERVATION_REVIEW', 'D1_ASSET_OWNER_CENSUS', 'D1_LEARNSET_OWNER_CENSUS'):
                self.assertEqual('UNKNOWN', result[gate])
            self.assertNotEqual('PASS', result['D1_ALL'])
            return result

    def test_discovery_rejects_policy_injection_and_nonlocal_scratch(self):
        def fake_git(root, *args):
            if args[0] == 'rev-parse':
                c = next(c for c, name in o.COMPONENTS.items() if str(root).endswith(name))
                return v.SOURCES[c].encode()
            return b''
        for plan in ({'schema': 2, 'scratch': '.local', 'ownership': policy()},
                     *({'schema': 2, 'scratch': path} for path in
                       ('../outside', '/outside', '05_builds', o.COMPONENTS['cfru'] + '/build'))):
            with patch.object(o, 'git', side_effect=fake_git), \
                 patch.object(o, 'bounded_read', return_value=b'synthetic source'), \
                 patch.object(o, 'SOURCE_HASHES', dict.fromkeys(('dpe', 'cfru'), o.sha(b'synthetic source'))), \
                 patch.object(o.subprocess, 'run') as process:
                result = o.run_user(plan, Path('/synthetic'), discovery=True)
            process.assert_not_called()
            self.assertNotEqual('PASS', result['D1_DISCOVERY'])

    def test_discovery_cli_sanitizes_errors_without_reading_a_plan(self):
        out = io.StringIO()
        with patch.object(o, 'run_user', side_effect=PermissionError('SECRET_PATH')), \
             patch.object(o, 'bounded_read') as reader, patch('sys.stdout', out):
            self.assertEqual(2, o.main(['--discover', '.local/SECRET_PATH']))
        reader.assert_not_called()
        self.assertNotIn('SECRET', out.getvalue())
        self.assertEqual(set(o.GATES + o.STOP_STATUSES + o.IO_STOP_STATUSES),
                         {line.split('=')[0] for line in out.getvalue().splitlines()})


class SanitizerTests(unittest.TestCase):
    def test_cli_prints_only_allowlisted_stop_categories_and_keeps_exit_code(self):
        for category in (*o.STOP_CATEGORIES, 'PRIVATE\nPATH=HASH', None, []):
            for outcome, code in (('UNKNOWN', 2), ('FAIL', 1)):
                with self.subTest(category=category, outcome=outcome):
                    result = dict.fromkeys(o.GATES, 'UNKNOWN')
                    result.update(D1_ALL=outcome, D1_DPE_STOP_CATEGORY=category,
                                  D1_CFRU_STOP_CATEGORY='PRIVATE\nOFFSET')
                    out = io.StringIO()
                    with patch.object(o, 'run_user', return_value=result), patch('sys.stdout', out):
                        self.assertEqual(code, o.main(['--discover', '.local/synthetic']))
                    lines = out.getvalue().splitlines()
                    self.assertEqual(len(o.GATES + o.STOP_STATUSES + o.IO_STOP_STATUSES), len(lines))
                    self.assertEqual('D1_DPE_STOP_CATEGORY=' + o.stop_category(category), lines[-4])
                    self.assertEqual('D1_CFRU_STOP_CATEGORY=UNKNOWN', lines[-3])
                    self.assertNotIn('PRIVATE', out.getvalue())

    def test_io_reason_cli_and_report_latch_sanitize_all_untrusted_values(self):
        for reason in (*o.IO_STOP_REASONS, 'PRIVATE\nPATH=OFFSET', None, [], {}, 1):
            with self.subTest(reason=reason):
                journal = o.Journal(io.BytesIO())
                journal.note_stop('UNSUPPORTED_IO', reason)
                self.assertEqual(o.io_stop_reason(reason), journal.io_stop_reason)
                result = dict.fromkeys(o.GATES + o.STOP_STATUSES, 'UNKNOWN')
                result.update(D1_DPE_STOP_CATEGORY='UNSUPPORTED_IO', D1_DPE_IO_STOP_REASON=reason,
                              D1_CFRU_IO_STOP_REASON='PATH_POLICY')
                out = io.StringIO()
                with patch.object(o, 'run_user', return_value=result), patch('sys.stdout', out):
                    self.assertEqual(2, o.main(['--discover', '.local/synthetic']))
                lines = out.getvalue().splitlines()
                self.assertEqual(len(o.GATES + o.STOP_STATUSES + o.IO_STOP_STATUSES), len(lines))
                self.assertEqual('D1_DPE_IO_STOP_REASON=' + o.io_stop_reason(reason), lines[-2])
                self.assertEqual('D1_CFRU_IO_STOP_REASON=UNKNOWN', lines[-1])
                self.assertNotIn('PRIVATE', out.getvalue())

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
