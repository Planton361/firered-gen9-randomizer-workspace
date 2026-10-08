#!/usr/bin/env python3
"""#713 immutable source oracle and restricted consumer gate; no host activation."""
import argparse
import hashlib
import shutil
import subprocess
import sys
import unittest

import run_cfru_dpe_host_field_bridge_mock_tests as accepted
import run_cfru_dpe_host_consumer_mock_tests as stock
from run_cfru_dpe_extension_mock_tests import lua_literal

ROOT = stock.ROOT
BASE = '17e1351c079863cb9797f520f2dc4cb4530deb2a'
EXT = accepted.EXT
MODULE = EXT + 'source_note_consumer_quarantine.lua'
HARNESS = '07_scripts/tracker/tests/cfru_dpe_note_consumer_mock.lua'
REVIEWED = {
    'Tracker.getMoves': (387, 397, '8aa1972accd4379dc26dd3a4d29ebdae97304efc2cb43e0b921a03280e8947ec'),
    'Tracker.getAbilities': (402, 408, 'ad7f0f3adee3aef83c35ac6716720da635a82323d35925fda842879f5d73f060'),
    'Tracker.getNote': (488, 494, '8e641e5effb5267cc836b9cd572851e6b812aabb824fc1ec3ad9fff2e0cf4cd3'),
    'Tracker.getLastLevelSeen': (520, 523, '8ef4ef42c0bd1db2d707af6f167b60576f45eb9f912472c1ebfe82235d2dcb98'),
}
DEPENDENCIES = (*accepted.DEPENDENCIES, accepted.MODULE, accepted.HARNESS,
                '07_scripts/tracker/run_cfru_dpe_host_field_bridge_mock_tests.py',
                '07_scripts/tracker/test_cfru_dpe_host_field_bridge_source.py',
                '07_scripts/tracker/test_cfru_dpe_host_consumer_source.py')


def note_definitions():
    text = stock.public_sources()['Tracker.lua']
    selected, provenance = {}, {}
    blob = stock.git('rev-parse', stock.PIN + ':ironmon_tracker/Tracker.lua', cwd=stock.TRACKER).decode().strip()
    for name, oracle in REVIEWED.items():
        body, first, last = stock.extract(text, name)
        digest = hashlib.sha256(body.encode()).hexdigest()
        if (first, last, digest) != oracle:
            raise ValueError('Unreviewed original note getter: ' + name)
        selected[name] = body
        provenance[name] = dict(path='Tracker.lua', blob=blob, first=first, last=last, sha256=digest)
    return selected, provenance


def payload():
    for path in DEPENDENCIES:
        if (ROOT / path).read_bytes() != stock.git('show', BASE + ':' + path):
            raise ValueError('Accepted dependency drift: ' + path)
    selected, provenance, raw, texts, multi, controls = accepted.accepted.inputs()
    notes, note_provenance = note_definitions()
    provenance.update(note_provenance)
    # Trusted harness-only construction capabilities: frozen fixtures and exact
    # reviewed definition installation. Neither capability is visible in env.
    needle = '    state.originals={}\n'
    if controls.count(needle) != 1:
        raise ValueError('Unreviewed fixture construction seam')
    controls = controls.replace(needle, '''    state.fixtureFrozen=frozen
    function state.fixtureDefinition(name,body)
        local ns,key=name:match("^(%w+)%.(%w+)$")
        locked=false
        assert(trustedLoad(body,'@PIN/'..name,'t',env))()
        locked=true
        return stores[ns][key]
    end
''' + needle)
    # Reuse only immutable #711 byte-fixture declarations, no bridge test cases.
    fixture = (ROOT / accepted.HARNESS).read_text()
    marker = 'for _,id in ipairs({1,1102,1294,1022}) do'
    if fixture.count(marker) != 1:
        raise ValueError('Ambiguous accepted fixture boundary')
    fixture = fixture.split(marker)[0]
    prelude = 'local SOURCES=' + stock.literal(selected)
    prelude += '\nlocal NOTE_SOURCES=' + stock.literal(notes)
    prelude += '\nlocal MOCK_SOURCE=' + lua_literal(raw)
    prelude += '\nlocal MOCK_PUBLIC_SOURCES=' + lua_literal(texts)
    prelude += '\nlocal MOCK_MULTI=' + lua_literal(multi)
    prelude += '\nlocal GATE_SOURCE=' + lua_literal((ROOT / MODULE).read_text())
    prelude += '\nlocal GATE_PATH=' + lua_literal(MODULE)
    prelude += '\nlocal acceptedBridge=dofile(' + lua_literal(accepted.MODULE) + ')\n'
    # Warm accepted dependency source validation outside per-case instruction cap.
    prelude += '''local warm={Program={},Battle={},Lifecycle={startTracker=function() end}}
local expected={}
for _,name in ipairs({"Program.updatePokemonTeams","Program.readNewPokemon","Battle.updateViewSlots","Battle.beginNewBattle"}) do
 local ns,key=name:match("^(%w+)%.(%w+)$")
 warm[ns][key]=function() error("warm stock must never execute") end
 expected[name]=warm[ns][key]
end
assert(acceptedBridge.newMock(warm,expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI))
'''
    # Only the four new unchanged getter bodies execute in the note oracle.
    # #707's 63 controls keep their existing SOURCES and stock fixture stubs.
    harness = (ROOT / HARNESS).read_text()
    if harness.count('-- ACCEPTED_FIXTURE_DECLARATIONS') != 1:
        raise ValueError('Ambiguous note fixture seam')
    return prelude + controls + '\n' + harness.replace('-- ACCEPTED_FIXTURE_DECLARATIONS', fixture), provenance


def run(runtime='lua5.4', capture=False):
    executable = shutil.which(runtime)
    if not executable:
        print('NOT_RUN: existing Lua 5.4 unavailable')
        return 2
    probe = subprocess.run([executable, '-e', 'io.write(_VERSION)'], text=True, capture_output=True, timeout=10)
    if probe.returncode or probe.stdout != 'Lua 5.4':
        print('NOT_RUN: requires existing Lua 5.4')
        return 2
    chunk, provenance = payload()
    for name, record in provenance.items():
        print('SOURCE', name, record, flush=True)
    print('HARNESS_SHA256', hashlib.sha256((ROOT / HARNESS).read_bytes()).hexdigest(), flush=True)
    result = subprocess.run([executable, '-'], input=chunk, text=True, cwd=ROOT,
                            capture_output=capture, timeout=120)
    return result if capture else result.returncode


def run_python_sources():
    names = ['test_cfru_dpe_extension_source', 'test_cfru_dpe_party_source',
             'test_cfru_dpe_battle_source', 'test_cfru_dpe_ui_source',
             'test_cfru_dpe_host_consumer_source', 'test_cfru_dpe_preconsumer_source',
             'test_cfru_dpe_host_field_bridge_source', 'test_cfru_dpe_note_consumer_source',
             'test_generate_cfru_dpe_source_data.ParserTests']
    exclusions = {
        'test_cfru_dpe_host_consumer_source.HostConsumerSourceTests.test_exact_four_new_paths_all_gitlinks_and_component_status',
        'test_cfru_dpe_preconsumer_source.PreconsumerSourceTests.test_exact_five_new_paths_existing_files_and_ten_clean_gitlinks',
        'test_cfru_dpe_host_field_bridge_source.HostFieldBridgeSourceTests.test_exact_five_added_paths_all_existing_bytes_and_ten_gitlinks',
    }
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item
    # Lock every historical test/runner used, without editing any of them.
    for module in names[:-2] + ['test_generate_cfru_dpe_source_data']:
        path = '07_scripts/tracker/' + module + '.py'
        if (ROOT / path).read_bytes() != stock.git('show', BASE + ':' + path):
            raise ValueError('Historical suite drift: ' + path)
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(names)))
    if {t.id() for t in tests} & exclusions != exclusions:
        raise ValueError('Historical exclusions no longer match exact tests')
    for name in sorted(exclusions):
        print('NOT_RUN', name, "— superseded by #713's exact-five-new-file verifier", flush=True)
    print('NOT_RUN 21 LockedProfileTests and generator --check: Clang prohibited', flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(t for t in tests if t.id() not in exclusions))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lua', default='lua5.4')
    parser.add_argument('--python-source', action='store_true')
    args = parser.parse_args()
    try:
        sys.exit(run_python_sources() if args.python_source else run(args.lua))
    except (ValueError, subprocess.SubprocessError) as error:
        print('FAIL:', error)
        sys.exit(1)
