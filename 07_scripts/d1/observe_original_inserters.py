#!/usr/bin/env python3
"""USER-ONLY: exact original inserters in a read-only Linux sandbox and RAM.

Codex must run only synthetic tests. No build, production insertion or receipt
trust mode. All private evidence remains in ignored scratch in this Workspace.
"""
import bisect
import builtins
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import secrets
import shutil
import subprocess
import sys
import tempfile

import validate_owner_write_sets as v

SOURCE_HASHES = {
    'dpe': '1f2b1548921033a6912fbc3b4b4d851f98110ae0225cc48ba3d343b3d5b9c6f6',
    'cfru': 'd794824b6b4185de437ed3b987f7a66a0da7360f1559f411a240291a2b59ce51',
}
COMPONENTS = {'dpe': '02_external/Dynamic-Pokemon-Expansion-Gen-9',
              'cfru': '02_external/CFRU-expansion',
              'upr': '02_external/upr-fvx'}
# Only valid for the exact public source hashes above. Helpers inherit their
# caller's phase, rather than misclassifying writes by helper source line.
PHASE_LINES = {
    'dpe': {290: 'copy', 291: 'expand', 304: 'payload', 316: 'bytepatch',
            342: 'special', 382: 'hooks', 405: 'repoints', 439: 'generated_repoints',
            461: 'repoint_all', 496: 'routine_pointers', 519: 'function_rewrites', 541: 'offsets'},
    'cfru': {2324: 'copy', 2337: 'payload', 2350: 'generated_repoints', 2374: 'repoint_all',
             2411: 'special', 2452: 'free_bytepatch', 2486: 'bytepatch', 2513: 'hooks',
             2538: 'repoints', 2575: 'routine_pointers', 2598: 'function_rewrites',
             2623: 'events', 2802: 'overlays', 2805: 'songs', 2840: 'offsets'},
}
GATES = ('D1_SANDBOX', 'D1_PUBLIC_SOURCE_IDENTITY', 'D1_ORIGINAL_EXECUTION',
         'D1_IO_RECOMPUTATION', 'D1_CAPACITY', 'D1_DECLARED_OWNER_CHECKS',
         'D1_REVIEWED_OVERRIDES', 'D1_LINK_IMAGE', 'D1_OAK_LINK_SHAPE',
         'D1_INPUT_CHAIN', 'D1_OUTPUT_REPRODUCTION', 'D1_CACHE_FRESHNESS',
         'D1_SOURCE_CONFIG_BUILD_PROVENANCE', 'D1_FULL_NATIVE_OWNERSHIP',
         'D1_ABI_RELOCATION_SEMANTICS', 'D1_DPE_REPRODUCIBILITY', 'D1_ALL')
DISCOVERY_GATES = ('D1_DISCOVERY', 'D1_CANDIDATE_PLAN', 'D1_RESERVATION_REVIEW',
                   'D1_ASSET_OWNER_CENSUS', 'D1_LEARNSET_OWNER_CENSUS')
GATES += DISCOVERY_GATES
# Diagnostics are separate from acceptance gates; UNKNOWN also covers no stop report.
STOP_STATUSES = ('D1_DPE_STOP_CATEGORY', 'D1_CFRU_STOP_CATEGORY')
STOP_CATEGORIES = ('UNSUPPORTED_IO', 'UNSUPPORTED_SUBPROCESS', 'SUBPROCESS_FAILURE',
                   'RESOURCE_LIMIT', 'MEMORY_ERROR', 'UNEXPECTED_EXCEPTION', 'UNKNOWN')
IO_STOP_STATUSES = ('D1_DPE_IO_STOP_REASON', 'D1_CFRU_IO_STOP_REASON')
IO_STOP_REASONS = ('PATH_POLICY', 'OPEN_MODE', 'WRITE_TARGET', 'COPY_CONTRACT',
                   'SEEK_RULE', 'READ_RULE', 'WRITE_RULE', 'TRUNCATE_RULE', 'FILENO_RULE', 'UNKNOWN')
MEMORY_LIMIT = 512 * 1024 * 1024
MAX_EVENTS = 100_000_000
MAX_JOURNAL = 8 * 1024 * 1024 * 1024
MAX_LINE = 128 * 1024 * 1024
MUTABLE = {'test.gba', 'generatedrepoints', 'offsets.ini'}
LINKED_ROLES = {
    'oak_record': ('gOakIntroContract', False),
    'oak_bitmap': ('gOakIntroEligibility', False),
    'oak_front_bridge': ('CreateOakIntroPokemonSprite', True),
    'oak_cry_bridge': ('Task_OakSpeech_IsInhabitedFarAndWide', True),
    'oak_front_consumer': ('OakIntroSpriteConsumer', True),
    'oak_cry_consumer': ('OakIntroCryConsumer', True),
    'pickup_record': ('gPickupDescriptor', False),
    'pickup_bridge': ('atkE5_pickupitemcalculation', True),
    'pickup_consumer': ('PickupItemCalculation', True),
    'evolution_record': ('gEvolutionFriendshipContract', False),
    'evolution_consumer': ('GetEvolutionTargetSpecies', True),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def stop_category(value):
    return value if type(value) is str and value in STOP_CATEGORIES else 'UNKNOWN'


def io_stop_reason(value):
    return value if type(value) is str and value in IO_STOP_REASONS else 'UNKNOWN'


class Stop(BaseException):
    """Persistent fail-closed latch; cannot be cleared by an inserter catch."""
    def __init__(self, category='UNKNOWN'):
        super().__init__()
        self.category = stop_category(category)


class Journal:
    def __init__(self, stream, max_events=MAX_EVENTS, max_bytes=MAX_JOURNAL):
        self.stream, self.max_events, self.max_bytes = stream, max_events, max_bytes
        self.count = self.size = 0
        self.stopped = False
        self.stop_category = 'UNKNOWN'
        self.io_stop_reason = 'UNKNOWN'

    def note_stop(self, category, io_reason='UNKNOWN'):
        # Later cleanup/errors must not replace the first concrete cause.
        if self.stop_category == 'UNKNOWN':
            self.stop_category = stop_category(category)
            if self.stop_category == 'UNSUPPORTED_IO':
                self.io_stop_reason = io_stop_reason(io_reason)

    def emit(self, op, **fields):
        raw = json.dumps(dict(op=op, **fields), separators=(',', ':')).encode() + b'\n'
        if self.count >= self.max_events or self.size + len(raw) > self.max_bytes or len(raw) > MAX_LINE:
            self.stopped = True
            self.note_stop('RESOURCE_LIMIT')
            raise Stop('RESOURCE_LIMIT')
        self.stream.write(raw)
        self.count += 1
        self.size += len(raw)


def journal_rows(stream):
    count = size = 0
    while True:
        raw = stream.readline(MAX_LINE + 1)
        if not raw:
            return
        count += 1
        size += len(raw)
        if len(raw) > MAX_LINE or count > MAX_EVENTS or size > MAX_JOURNAL:
            raise v.Missing()
        yield json.loads(raw, object_pairs_hook=v.unique_object)


class RamFile(io.RawIOBase):
    def __init__(self, store, key, mode, handle):
        super().__init__()
        self.store, self.key, self.mode, self.handle = store, key, mode, handle
        self.pos = len(store.data[key]) if 'a' in mode else 0

    def readable(self):
        return True

    def writable(self):
        return '+' in self.mode or 'w' in self.mode or 'a' in self.mode

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        if self.closed or type(offset) is not int or whence not in (0, 1, 2):
            self.store.deny(io_reason='SEEK_RULE')
        new = offset + (0 if whence == 0 else self.pos if whence == 1 else len(self.store.data[self.key]))
        if new > MEMORY_LIMIT:
            self.store.deny('RESOURCE_LIMIT')
        if new < 0:
            self.store.deny(io_reason='SEEK_RULE')
        self.pos = new
        self.store.journal.emit('seek', handle=self.handle, offset=offset, whence=whence, position=new)
        return new

    def read(self, size=-1):
        if self.closed or type(size) is not int or size < -1:
            self.store.deny(io_reason='READ_RULE')
        buf = self.store.data[self.key]
        data = bytes(buf[self.pos:] if size == -1 else buf[self.pos:self.pos + size])
        self.pos += len(data)
        self.store.journal.emit('read', handle=self.handle, size=size, length=len(data), sha256=sha(data))
        return data

    def readinto(self, buffer):
        data = self.read(len(buffer))
        buffer[:len(data)] = data
        return len(data)

    def write(self, data):
        if self.closed or not self.writable():
            self.store.deny(io_reason='WRITE_RULE')
        data = bytes(data)
        if 'a' in self.mode:
            self.pos = len(self.store.data[self.key])
        start = self.pos
        before = bytes(self.store.data[self.key][start:start + len(data)])
        # The backend counts/hashes actual writes independently of the journal.
        self.store.backend_write(self.key, start, data)
        self.pos += len(data)
        caller = sys._getframe(1)
        function = caller.f_code.co_name
        kind = ('hook' if function == 'Hook' else 'wrapper' if function == 'FunctionWrap' else
                'pointer' if function in ('Repoint', 'WritePointer') else
                'bulk' if self.store.phase == 'payload' else
                'expand' if self.store.phase == 'expand' else 'data')
        self.store.journal.emit('write', handle=self.handle, key=self.key, phase=self.store.phase,
                                kind=kind, source_line=caller.f_lineno, source_function=function,
                                start=start, length=len(data), before=sha(before), data=data.hex())
        return len(data)

    def truncate(self, size=None):
        if self.closed or not self.writable():
            self.store.deny(io_reason='TRUNCATE_RULE')
        size = self.pos if size is None else size
        if type(size) is not int or size < 0 or self.key == 'test.gba':
            self.store.deny(io_reason='TRUNCATE_RULE')
        if size > MEMORY_LIMIT:
            self.store.deny('RESOURCE_LIMIT')
        buf = self.store.data[self.key]
        if size > len(buf):
            buf.extend(bytes(size - len(buf)))
        else:
            del buf[size:]
        self.store.journal.emit('truncate', handle=self.handle, size=size)
        return size

    def close(self):
        if not self.closed:
            self.store.journal.emit('close', handle=self.handle)
        super().close()

    def fileno(self):
        self.store.deny(io_reason='FILENO_RULE')


class RamStore:
    def __init__(self, root, reader, journal):
        self.root = Path(root).resolve()
        self.reader, self.journal = reader, journal
        self.data, self.snapshots = {}, {}
        self.phase = 'preflight'
        self.denied = False
        self.handles = self.write_count = 0
        self.binding = hashlib.sha256()

    def deny(self, category='UNSUPPORTED_IO', io_reason='UNKNOWN'):
        self.denied = True
        self.journal.note_stop(category, io_reason)
        raise Stop(category)

    def key(self, path):
        if not isinstance(path, (str, os.PathLike)):
            self.deny(io_reason='PATH_POLICY')
        path = Path(path)
        full = path if path.is_absolute() else self.root / path
        # Reject symlink/path aliases; never resolve a write into production.
        if full.is_symlink() or '..' in full.parts:
            self.deny(io_reason='PATH_POLICY')
        resolved = full.resolve()
        if not resolved.is_relative_to(self.root):
            self.deny(io_reason='PATH_POLICY')
        return resolved.relative_to(self.root).as_posix()

    def load(self, key):
        if key not in self.data:
            data = self.reader(self.root / key)
            if sum(map(len, self.data.values())) + len(data) > MEMORY_LIMIT:
                self.deny('RESOURCE_LIMIT')
            self.data[key] = bytearray(data)
            self.snapshots[key] = sha(data)
        return self.data[key]

    def backend_write(self, key, start, data):
        buf = self.data[key]
        end = start + len(data)
        if end > MEMORY_LIMIT or sum(map(len, self.data.values())) + max(0, end - len(buf)) > MEMORY_LIMIT:
            self.deny('RESOURCE_LIMIT')
        if end > len(buf):
            buf.extend(bytes(end - len(buf)))
        buf[start:end] = data
        self.binding.update(v.observation_binding(key, start, data))
        self.write_count += 1

    def open(self, path, mode='r', buffering=-1, encoding=None, errors=None, newline=None, **kwargs):
        if kwargs or mode not in ('rb', 'rb+', 'r', 'r+', 'w', 'a', 'wb', 'wb+'):
            self.deny(io_reason='OPEN_MODE')
        key = self.key(path)
        if ('+' in mode or 'w' in mode or 'a' in mode) and key not in MUTABLE:
            self.deny(io_reason='WRITE_TARGET')
        if 'w' in mode:
            self.data[key] = bytearray()
        else:
            try:
                self.load(key)
            except FileNotFoundError:
                if 'a' not in mode:
                    raise
                self.data[key] = bytearray()
        handle = self.handles
        self.handles += 1
        self.journal.emit('open', handle=handle, key=key, mode=mode)
        raw = RamFile(self, key, mode, handle)
        return raw if 'b' in mode else io.TextIOWrapper(raw, encoding=encoding or 'utf-8',
                                                        errors=errors, newline=newline)

    def copy(self, src, dst, **kwargs):
        if kwargs or self.key(src) != 'BPRE0.gba' or self.key(dst) != 'test.gba':
            self.deny(io_reason='COPY_CONTRACT')
        data = self.load('BPRE0.gba')
        self.data['test.gba'] = bytearray(data)
        self.journal.emit('copy', src='BPRE0.gba', dst='test.gba')
        return dst


class OutputSink:
    def __init__(self):
        self.failed = False

    def write(self, text):
        if any(x in text.lower() for x in ('symbol missing', 'error:', 'error processing', 'could not')):
            self.failed = True
        return len(text)

    def flush(self):
        pass


def command_kind(command, root):
    if not isinstance(command, (list, tuple)) or not command or any(type(x) is not str for x in command):
        raise Stop('UNSUPPORTED_SUBPROCESS')
    name = Path(command[0]).name
    if name in ('arm-none-eabi-nm', 'arm-none-eabi-objdump'):
        if list(command[1:]) in (['build/linked.o'], ['-t', 'build/linked.o']):
            return 'symbols'
    if name == 'git':
        args = list(command[1:])
        if args[:2] == ['-C', str(root)]:
            args = args[2:]
        if args and args[0] in ('show', 'ls-files', 'diff', 'rev-parse', 'merge-base', 'cat-file'):
            # Options such as git diff --output must not create side effects.
            if not any(x.startswith(('--output', '--ext-diff', '--textconv')) for x in args):
                return 'source'
    if command[0] == sys.executable and list(command[1:]) == [
            'scripts/tests/audit_ai_writable_state.py', '--linked-object',
            'build/linked.o', '--output-bin', 'build/output.bin']:
        return 'preflight'
    raise Stop('UNSUPPORTED_SUBPROCESS')


def worker(config_path):
    # Only the parent launches this inside bubblewrap. Never a native build.
    with open(config_path, 'rb') as f:
        cfg = json.load(f)
    root, scratch = Path(cfg['root']), Path(cfg['scratch'])
    component = cfg['component']
    original_open, original_io_open = builtins.open, io.open
    real_run = subprocess.run
    def reader(path):
        with original_open(path, 'rb') as f:
            raw = f.read(MEMORY_LIMIT + 1)
        if len(raw) > MEMORY_LIMIT:
            raise Stop('RESOURCE_LIMIT')
        return raw
    script = root / 'scripts/insert.py'
    if sha(reader(script)) != SOURCE_HASHES[component]:
        return 2
    journal_stream = original_open(scratch / 'operations.jsonl', 'wb')
    store = RamStore(root, reader, Journal(journal_stream))
    sink = OutputSink()
    real_isfile, real_exists, real_size, real_copy = os.path.isfile, os.path.exists, os.path.getsize, shutil.copyfile
    def probe(path, fallback):
        key = store.key(path)
        return (len(store.data[key]) if fallback is real_size else True) if key in store.data else fallback(path)
    def run(command, **kwargs):
        try:
            command_kind(command, root)
            if set(kwargs) - {'check', 'text', 'stdout', 'stderr'}:
                store.deny('UNSUPPORTED_SUBPROCESS')
            # Private child output is captured, never inherited by the terminal.
            result = real_run(command, check=False, text=kwargs.get('text', False),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              stdin=subprocess.DEVNULL, timeout=3600)
            if result.returncode:
                store.journal.note_stop('SUBPROCESS_FAILURE')
            store.journal.emit('subprocess', returncode=result.returncode)
            if result.returncode:
                store.denied = True
                raise Stop('SUBPROCESS_FAILURE')
            return result
        except BaseException as error:
            store.denied = True
            category = (error.category if isinstance(error, Stop) else
                        'MEMORY_ERROR' if isinstance(error, MemoryError) else
                        'RESOURCE_LIMIT' if isinstance(error, subprocess.TimeoutExpired) else
                        'SUBPROCESS_FAILURE' if isinstance(error, (subprocess.SubprocessError, OSError)) else
                        'UNEXPECTED_EXCEPTION')
            store.journal.note_stop(category)
            raise
    def check_output(command, **kwargs):
        return run(command, **kwargs).stdout
    real_check = subprocess.check_output
    def trace(frame, event, arg):
        if frame.f_code.co_filename == str(script):
            if event == 'line' and frame.f_code.co_name == 'main':
                keys = sorted(PHASE_LINES[component])
                at = bisect.bisect_right(keys, frame.f_lineno) - 1
                if at >= 0:
                    store.phase = PHASE_LINES[component][keys[at]]
            elif event == 'return' and frame.f_code.co_name == 'FindFreeSpace':
                if type(arg) is not int:
                    store.deny()
                store.journal.emit('allocate', start=arg, length=frame.f_locals['length'])
        return trace
    completed = False
    outcome = "UNKNOWN"
    try:
        builtins.open = io.open = store.open
        shutil.copyfile = store.copy
        os.path.isfile = lambda path: probe(path, real_isfile)
        os.path.exists = lambda path: probe(path, real_exists)
        os.path.getsize = lambda path: probe(path, real_size)
        subprocess.run, subprocess.check_output = run, check_output
        sys.path.insert(0, str(root / 'scripts'))
        sys.argv = [str(script)]
        sys.settrace(trace)
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            runpy.run_path(str(script), run_name='__main__')
        completed = not store.denied and not store.journal.stopped and not sink.failed
        outcome = "PASS" if completed else "FAIL" if sink.failed else "UNKNOWN"
    except Stop as error:
        store.journal.note_stop(error.category)
        completed = False
    except MemoryError:
        store.journal.note_stop('MEMORY_ERROR')
        completed = False
    except BaseException:
        store.journal.note_stop('UNEXPECTED_EXCEPTION')
        completed = False
        outcome = "UNKNOWN" if store.denied or store.journal.stopped else "FAIL"
    finally:
        sys.settrace(None)
        builtins.open, io.open = original_open, original_io_open
        os.path.isfile, os.path.exists, os.path.getsize, shutil.copyfile = real_isfile, real_exists, real_size, real_copy
        subprocess.run, subprocess.check_output = real_run, real_check
        journal_stream.close()
    if 'test.gba' in store.data:
        with original_open(scratch / 'ram-output.bin', 'wb') as f:
            f.write(store.data['test.gba'])
    report = {'nonce': cfg['nonce'], 'component': component, 'completed': completed, 'outcome': outcome,
              'stop_category': store.journal.stop_category,
              'io_stop_reason': store.journal.io_stop_reason,
              'snapshots': store.snapshots, 'write_count': store.write_count,
              'write_binding': store.binding.hexdigest(), 'event_count': store.journal.count}
    with original_open(scratch / 'report.json', 'w') as f:
        json.dump(report, f)
    return 0 if completed else 2


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if result.returncode:
        raise v.Missing()
    return result.stdout


def bounded_read(path, limit=MEMORY_LIMIT):
    if path.is_symlink() or not path.is_file():
        raise v.Missing()
    with path.open('rb') as f:
        data = f.read(limit + 1)
    if len(data) > limit:
        raise v.Missing()
    return data


def checked_path(root, relative):
    if type(relative) is not str or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise v.Invalid()
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise v.Invalid()
    return path


def sandbox_command(bwrap, root, scratch, cfg):
    # Entire host, including selected originals, is read-only. Only ignored
    # evidence scratch and /tmp are writable; no networking, no production ROM.
    return [bwrap, '--die-with-parent', '--unshare-all', '--new-session',
            '--ro-bind', '/', '/', '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp',
            '--bind', str(scratch), str(scratch), '--chdir', str(root),
            sys.executable, '-B', str(Path(__file__).resolve()), '--internal-worker', str(cfg)]


def verify_live_stage(root, scratch, report, nonce, write_check, event_check=None):
    v.require(report['nonce'] == nonce and report['completed'] is True)
    snapshots = {}
    for name, expected in report['snapshots'].items():
        data = bounded_read(checked_path(root, name))
        v.require(sha(data) == expected)
        snapshots[name] = data
        if sum(map(len, snapshots.values())) > MEMORY_LIMIT:
            raise v.Missing()
    verifier = v.JournalVerifier(snapshots, write_check=write_check)
    count = 0
    with (scratch / 'operations.jsonl').open('rb') as f:
        for event in journal_rows(f):
            verifier.consume(event)
            if event_check is not None:
                event_check(event)
            count += 1
    v.require(count == report['event_count'])
    ram = bounded_read(scratch / 'ram-output.bin')
    verifier.finish(ram, report['write_count'], report['write_binding'])
    return verifier, ram


class OwnerChecks:
    """Stream real writes against declared intervals; never certify map truth."""
    def __init__(self, policy):
        v.fields(policy, ('config', 'allocations', 'owners', 'overrides'))
        # A discovery candidate contains facts to review, never permissions.
        if policy['config'] is None or any(row.get('basis') is None
                                          for key in ('allocations', 'owners') for row in policy[key]):
            raise v.Missing()
        v.digest(policy['config'])
        self.policy = policy
        self.owners = v.owners(policy)
        self.allocs = v.allocations(policy)
        self.history = []
        self.history_pages = {}
        self.owner_order = sorted(self.owners.values(), key=lambda owner: owner['start'])
        self.owner_starts = [owner['start'] for owner in self.owner_order]
        self.seen_overrides = set()
        self.overrides = {}
        self.write_index = {'dpe': 0, 'cfru': 0}
        self.tail = v.CFRU_START
        self.history_bytes = 0
        self.phase_rank = {'dpe': -1, 'cfru': -1}
        self.started_cfru = False
        for e in policy['overrides']:
            pair = (e['earlier'], e['later'])
            v.require(pair not in self.overrides)
            self.overrides[pair] = e

    def check(self, component, event):
        start, end = event['start'], event['start'] + event['length']
        v.integer(start); v.integer(end)
        v.require(start < end)
        phase = event['phase']
        v.require(phase in v.PHASES[component])
        v.require(not (self.started_cfru and component == 'dpe'))
        self.started_cfru |= component == 'cfru'
        rank = v.PHASES[component].index(phase)
        v.require(rank >= self.phase_rank[component])
        self.phase_rank[component] = rank
        index = self.write_index[component]
        self.write_index[component] += 1
        write_id = component + '_' + str(index)
        if phase == 'expand':
            v.require(component == 'dpe' and end == v.ROM_LIMIT)
            return
        if phase == 'payload':
            a = next(a for a in self.allocs.values() if a['component'] == component and a['kind'] == 'payload')
            v.require((start, end) == (a['start'], a['end']))
            if component == 'cfru':
                self.tail = end
            return
        at = bisect.bisect_right(self.owner_starts, start) - 1
        if at < 0 or not start < end <= self.owner_order[at]['end']:
            raise v.Missing()
        owner = self.owner_order[at]
        if phase == 'overlays' and start >= v.CFRU_START:
            v.require(start % 4 == 0 and start >= (self.tail + 3) // 4 * 4 and end <= v.DPE_START)
            self.tail = end
        if component == 'cfru' and start >= v.CFRU_START:
            v.require(end <= v.DPE_START)
        self.history_bytes += len(event['data']) + 1024
        if len(self.history) >= 1_000_000 or self.history_bytes > 128 * 1024 * 1024:
            raise v.Missing()  # Explicit constrained-memory STOP, no sampling.
        ranges = []
        candidates = {index for page in range(start // 4096, (end - 1) // 4096 + 1)
                      for index in self.history_pages.get(page, ())}
        for index in sorted(candidates):
            earlier, previous_component, earlier_id, earlier_owner = self.history[index]
            lo = max(start, earlier['start'])
            hi = min(end, earlier['start'] + earlier['length'])
            if lo >= hi:
                continue
            pair = (earlier_id, write_id)
            v.require(pair in self.overrides)
            edge = self.overrides[pair]
            v.require(edge['start'] == lo and edge['end'] == hi and earlier_owner == owner['id'])
            if previous_component == component:
                v.require(edge['basis'] == 'reviewed_source_order')
            else:
                v.require(previous_component == 'dpe' and component == 'cfru')
                v.require(owner['component'] == 'dpe' and owner['roles'] == ['reviewed_shared_patch']
                          and owner['allocation'] is None)
                v.require(edge['basis'] == 'reviewed_dpe_to_cfru_patch')
                review = edge['review']
                v.token(review['reference']); v.digest(review['decision_sha256'])
                v.require(review['owner'] == owner['id'] and review['config'] == self.policy['config'])
                v.require(review['sources'] == {c: v.SOURCES[c] for c in ('dpe', 'cfru')})
                # Streaming schema-2 operation bindings include actual bytes.
                v.require(review['earlier_write'] == v.write_binding(earlier, previous_component))
                v.require(review['later_write'] == v.write_binding(event, component))
                ranges.append((lo, hi))
            self.seen_overrides.add(pair)
        if owner['component'] != component:
            v.require(owner['component'] == 'dpe' and component == 'cfru')
            cursor = start
            for lo, hi in sorted(ranges):
                v.require(lo <= cursor)
                cursor = max(cursor, hi)
            v.require(cursor == end)
        if event.get('kind') in ('pointer', 'hook', 'wrapper'):
            data = bytes.fromhex(event['data'])
            if event['kind'] == 'pointer':
                v.require(len(data) == 4)
            elif event['kind'] == 'hook':
                v.require(start % 2 == 0 and len(data) == (10 if start % 4 else 8))
            else:
                v.require(start % 2 == 0 and len(data) >= 20)
            target = int.from_bytes(data[-4:], 'little')
            if event['kind'] != 'pointer' or phase == 'routine_pointers':
                v.require(target & 1)
            target = (target & ~1) - 0x08000000
            v.require(any(o['start'] <= target < o['end'] for o in self.owners.values()))
        index = len(self.history)
        self.history.append((event, component, write_id, owner['id']))
        for page in range(start // 4096, (end - 1) // 4096 + 1):
            self.history_pages.setdefault(page, []).append(index)

    def allocation(self, event):
        span = {'start': event['start'], 'end': event['start'] + event['length']}
        v.require(span['start'] % 4 == 0 and span['start'] >= 0x900000)
        matches = [a for a in self.allocs.values() if a['kind'] == 'dynamic' and v.contains(a, span)]
        v.require(len(matches) == 1 and event['length'] >= 256)
        for owner in self.owners.values():
            if v.overlaps(owner, span):
                v.require(owner['allocation'] == matches[0]['id'])


class Discovery:
    """Private census from independently replayed events, without owner grants."""
    def __init__(self, stream, scratch):
        self.journal = Journal(stream)
        self.plan = {'schema': 2, 'scratch': scratch, 'ownership': {
            'config': None, 'allocations': [], 'owners': [], 'overrides': []}}
        self.indices = {'dpe': 0, 'cfru': 0}
        self.ranks = {'dpe': -1, 'cfru': -1}
        self.history, self.pages = [], {}
        self.history_bytes = 0
        self.payloads = {}
        self.started_cfru = False
        self.journal.emit('review_required', sources=v.SOURCES, script_hashes=SOURCE_HASHES,
                          missing_roles=sorted(v.REQUIRED_ROLES))

    def consume(self, component, event):
        if event['op'] == 'allocate':
            start, length = event['start'], event['length']
            v.integer(start); v.integer(length, 1)
            v.require(start % 4 == 0 and start >= 0x900000 and start + length <= v.DPE_START)
            self.journal.emit('allocation_request', component=component, start=start,
                              end=start + length, basis=None)
        elif event['op'] == 'write' and event['key'] == 'test.gba':
            self.write(component, event)

    def write(self, component, event):
        start, length, phase = event['start'], event['length'], event['phase']
        v.integer(start); v.integer(length)
        end = start + length
        v.require(end <= v.ROM_LIMIT and phase in v.PHASES[component]
                  and phase not in v.NO_ROM_WRITES)
        v.require(event['kind'] in ('bulk', 'expand', 'data', 'pointer', 'hook', 'wrapper'))
        v.require(not (self.started_cfru and component == 'dpe'))
        self.started_cfru |= component == 'cfru'
        rank = v.PHASES[component].index(phase)
        v.require(rank >= self.ranks[component])
        self.ranks[component] = rank
        if component == 'cfru' and start >= v.CFRU_START:
            v.require(end <= v.DPE_START)
        if phase == 'payload':
            v.require(component not in self.payloads and length > 0 and start ==
                      (v.DPE_START if component == 'dpe' else v.CFRU_START))
            self.payloads[component] = (start, end)
        write_id = component + '_' + str(self.indices[component])
        self.indices[component] += 1
        row = {'id': write_id, 'component': component, 'phase': phase, 'kind': event['kind'],
               'start': start, 'end': end, 'binding': v.write_binding(event, component),
               'source_line': event['source_line'], 'source_function': event['source_function'],
               'unchanged': event['before'] == sha(bytes.fromhex(event['data']))}
        self.journal.emit('write_candidate', **row)
        # Keep every operation (including no-ops and bulk materialization) and
        # every intersection. An intersection is a review obligation, no edge.
        candidates = {i for page in range(start // 4096, (end + 4095) // 4096) if length
                      for i in self.pages.get(page, ())}
        for i in sorted(candidates):
            earlier = self.history[i]
            lo, hi = max(start, earlier['start']), min(end, earlier['end'])
            if lo < hi:
                self.journal.emit('intersection_candidate', earlier=earlier['id'], later=write_id,
                                  start=lo, end=hi, earlier_write=earlier['binding'],
                                  later_write=row['binding'], basis=None,
                                  materialization=any(r['phase'] in ('expand', 'payload')
                                                      for r in (earlier, row)))
        self.history_bytes += len(json.dumps(row)) + 1024
        if len(self.history) >= 1_000_000 or self.history_bytes > 128 * 1024 * 1024:
            raise v.Missing()
        index = len(self.history)
        self.history.append(row)
        if length:
            for page in range(start // 4096, (end - 1) // 4096 + 1):
                self.pages.setdefault(page, []).append(index)

    def linked_candidates(self, component, elf, installed):
        """Only public named roles with actual sized ELF symbols; no free-byte owners."""
        start, end = self.payloads[component]
        alloc_id = component + '_payload'
        policy = self.plan['ownership']
        policy['allocations'].append({'id': alloc_id, 'component': component, 'kind': 'payload',
                                      'start': start, 'end': end, 'basis': None})
        bindings = LINKED_ROLES if component == 'cfru' else {
            'native_front_table': ('gMonFrontPicTable', False),
            'native_palette_table': ('gMonPaletteTable', False),
            'evolution_rows': ('gEvolutionTable', False)}
        for role, (symbol, thumb) in bindings.items():
            try:
                size = (1440 * 8 if role in ('native_front_table', 'native_palette_table')
                        else v.REQUIRED_ROLES[role])
                value, data = elf.symbol(symbol, size, thumb)
            except v.Missing:
                self.journal.emit('missing_symbol', role=role)
                continue
            at = (value & ~1 if thumb else value) - 0x08000000
            v.require(start <= at < at + len(data) <= end and installed[at:at + len(data)] == data)
            policy['owners'].append({'id': role, 'component': component, 'roles': [role],
                                     'start': at, 'end': at + len(data), 'allocation': alloc_id,
                                     'basis': None})
            self.journal.emit('linked_candidate', role=role, symbol=symbol, source=v.SOURCES[component],
                              start=at, end=at + len(data), basis=None)

    def finish(self, path):
        v.require(set(self.payloads) == {'dpe', 'cfru'})
        present = {r for owner in self.plan['ownership']['owners'] for r in owner['roles']}
        self.journal.emit('census_complete', write_counts=self.indices,
                          missing_roles=sorted(set(v.REQUIRED_ROLES) - present),
                          permissions_reviewed=False)
        with path.open('x') as f:
            json.dump(self.plan, f)


def run_user(plan, workspace, discovery=False):
    result = dict.fromkeys(GATES + STOP_STATUSES + IO_STOP_STATUSES, 'UNKNOWN')
    root = workspace.resolve()
    active_gate = 'D1_ALL'
    try:
        v.fields(plan, ('schema', 'scratch') if discovery else ('schema', 'scratch', 'ownership'))
        v.require(plan['schema'] == 2 and type(plan['schema']) is int)
        active_gate = 'D1_PUBLIC_SOURCE_IDENTITY'
        for c, relative in COMPONENTS.items():
            component = root / relative
            v.require(git(component, 'rev-parse', 'HEAD').decode().strip() == v.SOURCES[c])
            git(component, 'diff', '--quiet', 'HEAD', '--')
        for c in ('dpe', 'cfru'):
            v.require(sha(bounded_read(root / COMPONENTS[c] / 'scripts/insert.py')) == SOURCE_HASHES[c])
        result['D1_PUBLIC_SOURCE_IDENTITY'] = 'PASS'
        scratch_root = checked_path(root, plan['scratch'])
        if discovery:
            # Only the existing ignored local scratch area, never an ignored
            # build/ROM directory or a component checkout.
            v.require(scratch_root.relative_to(root).parts[:1] == ('.local',)
                      and scratch_root.resolve().is_relative_to(root / '.local')
                      and not (root / '.local').is_symlink())
        # Verify ignore coverage with a future file too; no bare top-level workspace.
        git(root, 'check-ignore', '--quiet', str(scratch_root / 'd1-private-evidence'))
        if not scratch_root.is_dir():
            raise v.Missing()
        bwrap = shutil.which('bwrap')
        if bwrap is None or not sys.platform.startswith('linux'):
            raise v.Missing()
        active_gate = 'D1_DECLARED_OWNER_CHECKS'
        checks = None if discovery else OwnerChecks(plan['ownership'])
        dpe, cfru = root / COMPONENTS['dpe'], root / COMPONENTS['cfru']
        active_gate = 'D1_INPUT_CHAIN'
        previous_output, selected_input = bounded_read(dpe / 'test.gba'), bounded_read(cfru / 'BPRE0.gba')
        v.require(previous_output == selected_input and len(selected_input) == v.ROM_LIMIT)
        v.require(0 < len(bounded_read(dpe / 'BPRE0.gba')) <= v.ROM_LIMIT)
        result['D1_INPUT_CHAIN'] = 'PASS'
        existing_caches = any((root / COMPONENTS[c] / 'generatedrepoints').exists() for c in ('dpe', 'cfru'))
        with contextlib.nullcontext(tempfile.mkdtemp(prefix='d1-', dir=scratch_root)) as tmp:
            evidence = Path(tmp)
            census_stream = (evidence / 'candidate-census.jsonl').open('xb') if discovery else None
            # The context closes even after an unsupported/failed native stage.
            with contextlib.ExitStack() as streams:
                if census_stream is not None:
                    streams.enter_context(census_stream)
                census = Discovery(census_stream, plan['scratch']) if discovery else None
                return observe_stages(root, evidence, bwrap, result, checks, census, existing_caches)
    except (v.Invalid, ValueError, TypeError, IndexError):
        result[active_gate] = 'FAIL'
        result['D1_ALL'] = 'FAIL'
    except (Exception, Stop, KeyboardInterrupt):
        pass
    return result


def observe_stages(root, evidence, bwrap, result, checks, census, existing_caches):
    """Shared sandbox path: discovery removes no isolation or integrity checks."""
    active_gate = 'D1_ORIGINAL_EXECUTION'
    cfru = root / COMPONENTS['cfru']
    try:
        # Private evidence stays in this unique ignored directory for USER review.
        for c in ('dpe', 'cfru'):
            directory = evidence / c
            directory.mkdir(mode=0o700)
            nonce = secrets.token_hex(32)
            cfg = directory / 'worker.json'
            cfg.write_text(json.dumps({'root': str(root / COMPONENTS[c]), 'scratch': str(directory),
                                       'component': c, 'nonce': nonce}))
            env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': str(directory),
                   'TMPDIR': str(directory), 'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C',
                   'D1_OBSERVER_SANDBOX_NONCE': nonce}
            active_gate = 'D1_ORIGINAL_EXECUTION'
            stop_status = 'D1_' + c.upper() + '_STOP_CATEGORY'
            try:
                run = subprocess.run(sandbox_command(bwrap, root / COMPONENTS[c], directory, cfg),
                                     env=env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL, timeout=7200)
            except subprocess.TimeoutExpired:
                result[stop_status] = 'RESOURCE_LIMIT'
                raise
            report = json.loads(bounded_read(directory / 'report.json', 16 * 1024 * 1024))
            if run.returncode:
                if report.get('nonce') == nonce and report.get('component') == c:
                    result[stop_status] = stop_category(report.get('stop_category'))
                    if result[stop_status] == 'UNSUPPORTED_IO':
                        result['D1_' + c.upper() + '_IO_STOP_REASON'] = io_stop_reason(report.get('io_stop_reason'))
                if report.get('outcome') == 'FAIL':
                    raise v.Invalid()
                raise v.Missing()
            result['D1_SANDBOX'] = 'PASS'
            active_gate = 'D1_IO_RECOMPUTATION'
            verifier, ram = verify_live_stage(root / COMPONENTS[c], directory, report, nonce,
                                             None if census else lambda e, c=c: checks.check(c, e),
                                             (lambda e, c=c: census.consume(c, e)) if census else None)
            active_gate = 'D1_CAPACITY'
            if checks is not None:
                for alloc in verifier.allocations:
                    checks.allocation(alloc)
            active_gate = 'D1_OUTPUT_REPRODUCTION'
            # Pre-insert discovery has no selected CFRU production output yet.
            # Use the verifier's independently reconstructed bytes for all
            # subsequent link/Oak checks; DPE and --plan retain comparison.
            actual = (bytes(verifier.files['test.gba']) if census is not None and c == 'cfru'
                      else bounded_read(root / COMPONENTS[c] / 'test.gba'))
            v.require(actual == ram and len(ram) == v.ROM_LIMIT)
            active_gate = 'D1_LINK_IMAGE'
            elf = v.ArmElf(bounded_read(root / COMPONENTS[c] / 'build/linked.o'))
            origin = elf.payload(bounded_read(root / COMPONENTS[c] / 'build/output.bin'))
            v.require(origin == 0x08000000 + (v.CFRU_START if c == 'cfru' else v.DPE_START))
            if census is not None:
                census.linked_candidates(c, elf, actual)
            if c == 'cfru':
                active_gate = 'D1_DECLARED_OWNER_CHECKS'
                if checks is not None:
                    v.verify_linked_reservations(elf, checks.owners, LINKED_ROLES)
                asm = bounded_read(cfru / 'assembly/data/oak_intro_contract.s').decode()
                block = asm.split('gOakIntroEligibility:', 1)[1].split('.Loak_eligibility_end:', 1)[0]
                import re
                bitmap = bytes(int(x, 16) for line in block.splitlines() if '.byte ' in line
                               for x in re.findall(r'0x[0-9a-fA-F]+', line.split('@')[0]))
                active_gate = 'D1_OAK_LINK_SHAPE'
                v.verify_oak_link(elf, actual, bitmap)
        active_gate = 'D1_REVIEWED_OVERRIDES'
        if checks is not None:
            v.require(checks.seen_overrides == set(checks.overrides))
        else:
            active_gate = 'D1_CANDIDATE_PLAN'
            census.finish(evidence / 'candidate-plan.json')
            result['D1_CANDIDATE_PLAN'] = result['D1_DISCOVERY'] = 'PASS'
        if not existing_caches:
            result['D1_CACHE_FRESHNESS'] = 'PASS'
        for gate in ('D1_ORIGINAL_EXECUTION', 'D1_IO_RECOMPUTATION', 'D1_LINK_IMAGE',
                     'D1_OAK_LINK_SHAPE'):
            result[gate] = 'PASS'
        if checks is not None:
            for gate in ('D1_CAPACITY', 'D1_DECLARED_OWNER_CHECKS', 'D1_REVIEWED_OVERRIDES',
                         'D1_OUTPUT_REPRODUCTION'):
                result[gate] = 'PASS'
    except (v.Invalid, ValueError, TypeError, IndexError):
        result[active_gate] = 'FAIL'
        result['D1_ALL'] = 'FAIL'
    except (Exception, Stop, KeyboardInterrupt):
        pass
    # Existing artifacts do not prove a fresh native run, complete source-derived
    # owner inventory, C semantics, relocations or #741 reproducibility. Never
    # promote these gates from a plan, a worker report or matching image hashes.
    return result



def sandbox_guard(config_path):
    """Internal entry cannot start native work against writable originals."""
    cfg = json.loads(bounded_read(Path(config_path), 16 * 1024 * 1024))
    workspace = Path(__file__).resolve().parents[2]
    expected = workspace / COMPONENTS[cfg['component']]
    v.require(Path(cfg['root']) == expected)
    v.require(os.environ.get('D1_OBSERVER_SANDBOX_NONCE') == cfg['nonce'])
    v.require(os.statvfs('/').f_flag & os.ST_RDONLY)
    v.require(os.statvfs(expected).f_flag & os.ST_RDONLY)
    v.require(not os.statvfs(cfg['scratch']).f_flag & os.ST_RDONLY)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) == 2 and argv[0] == '--internal-worker':
        try:
            sandbox_guard(argv[1])
            import resource
            resource.setrlimit(resource.RLIMIT_AS, (1536 * 1024 * 1024,) * 2)
            return worker(argv[1])
        except BaseException:
            return 2
    result = dict.fromkeys(GATES + STOP_STATUSES + IO_STOP_STATUSES, 'UNKNOWN')
    try:
        if len(argv) != 2 or argv[0] not in ('--plan', '--discover'):
            raise v.Missing()
        discovery = argv[0] == '--discover'
        if discovery:
            plan = {'schema': 2, 'scratch': argv[1]}
        else:
            raw = bounded_read(Path(argv[1]), 16 * 1024 * 1024)
            plan = json.loads(raw, object_pairs_hook=v.unique_object)
        result = run_user(plan, Path(__file__).resolve().parents[2], discovery=discovery)
    except (v.Invalid, ValueError, TypeError):
        result['D1_ALL'] = 'FAIL'
    except (Exception, Stop, KeyboardInterrupt):
        pass
    for name in GATES:
        print(name + '=' + result[name])
    for name in STOP_STATUSES:
        print(name + '=' + stop_category(result.get(name)))
    for name, category in zip(IO_STOP_STATUSES, STOP_STATUSES):
        reason = io_stop_reason(result.get(name)) if result.get(category) == 'UNSUPPORTED_IO' else 'UNKNOWN'
        print(name + '=' + reason)
    return 1 if result['D1_ALL'] == 'FAIL' else 2


if __name__ == '__main__':
    sys.exit(main())
