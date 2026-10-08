#!/usr/bin/env python3
"""#711 ROM-free bridge oracle, reusing unchanged #707 extraction/sandbox."""
import argparse
import hashlib
import shutil
import subprocess
import sys
import unittest

import run_cfru_dpe_preconsumer_mock_tests as accepted
import run_cfru_dpe_host_consumer_mock_tests as stock
from run_cfru_dpe_extension_mock_tests import lua_literal

ROOT = stock.ROOT
BASE = '17c859785015d9c48544558969bade7f0212ba0b'
EXT = accepted.EXT
HARNESS = '07_scripts/tracker/tests/cfru_dpe_host_field_bridge_mock.lua'
MODULE = EXT + 'source_host_field_bridge.lua'
DEPENDENCIES = (
    EXT + 'source_preconsumer_guard.lua', EXT + 'source_party_decoder.lua',
    EXT + 'source_battle_decoder.lua', EXT + 'profile_sha256.lua',
    '07_scripts/tracker/run_cfru_dpe_preconsumer_mock_tests.py',
    '07_scripts/tracker/run_cfru_dpe_host_consumer_mock_tests.py',
    accepted.STOCK_HARNESS,
)


def payload():
    for path in DEPENDENCIES:
        if (ROOT / path).read_bytes() != stock.git('show', BASE + ':' + path):
            raise ValueError('Accepted dependency drift: ' + path)
    selected, provenance, raw, texts, multi, controls = accepted.inputs()
    prelude = 'local SOURCES=' + stock.literal(selected)
    prelude += '\nlocal MOCK_SOURCE=' + lua_literal(raw)
    prelude += '\nlocal MOCK_PUBLIC_SOURCES=' + lua_literal(texts)
    prelude += '\nlocal MOCK_MULTI=' + lua_literal(multi)
    prelude += '\nlocal bridgeModule=dofile(' + lua_literal(MODULE) + ')\n'
    prelude += '''local warm={Program={},Battle={},Lifecycle={startTracker=function() end}}
local expected={}
for _,name in ipairs({"Program.updatePokemonTeams","Program.readNewPokemon","Battle.updateViewSlots","Battle.beginNewBattle"}) do
 local ns,key=name:match("^(%w+)%.(%w+)$")
 warm[ns][key]=function() error("warm stock must never execute") end
 expected[name]=warm[ns][key]
end
local warmed,why=bridgeModule.newMock(warm,expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
assert(warmed,why and why.reason)
'''
    return prelude + controls + '\n' + (ROOT / HARNESS).read_text(), provenance


def run(runtime='lua5.4', capture=False):
    executable = shutil.which(runtime)
    if not executable:
        print('NOT_RUN: existing Lua 5.4 unavailable')
        return 2
    probe = subprocess.run([executable, '-e', 'io.write(_VERSION)'], text=True,
                           capture_output=True, timeout=10)
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
    names = [
        'test_cfru_dpe_extension_source', 'test_cfru_dpe_party_source',
        'test_cfru_dpe_battle_source', 'test_cfru_dpe_ui_source',
        'test_cfru_dpe_host_consumer_source', 'test_cfru_dpe_preconsumer_source',
        'test_cfru_dpe_host_field_bridge_source',
        'test_generate_cfru_dpe_source_data.ParserTests',
    ]
    exclusions = {
        'test_cfru_dpe_host_consumer_source.HostConsumerSourceTests.test_exact_four_new_paths_all_gitlinks_and_component_status',
        'test_cfru_dpe_preconsumer_source.PreconsumerSourceTests.test_exact_five_new_paths_existing_files_and_ten_clean_gitlinks',
    }
    def flatten(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item
    tests = list(flatten(unittest.defaultTestLoader.loadTestsFromNames(names)))
    found = {t.id() for t in tests} & exclusions
    if found != exclusions:
        raise ValueError('Historical allowlist exclusion no longer matches exact tests')
    for name in sorted(exclusions):
        print('NOT_RUN', name, '— superseded by #711 exact five-file verifier', flush=True)
    print('NOT_RUN 21 LockedProfileTests and generator --check: Clang required', flush=True)
    selected = unittest.TestSuite(t for t in tests if t.id() not in exclusions)
    result = unittest.TextTestRunner(verbosity=2).run(selected)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lua', default='lua5.4')
    parser.add_argument('--python-source', action='store_true', help='Run all applicable safe Python regressions')
    args = parser.parse_args()
    try:
        sys.exit(run_python_sources() if args.python_source else run(args.lua))
    except (ValueError, subprocess.SubprocessError) as error:
        print('FAIL:', error)
        sys.exit(1)
