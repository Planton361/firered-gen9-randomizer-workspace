#!/usr/bin/env python3
"""#709: immutable #707 controls plus detached guard, ROM-free Lua 5.4 only."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

import generate_cfru_dpe_source_data as source
import run_cfru_dpe_host_consumer_mock_tests as stock
from run_cfru_dpe_party_mock_tests import PUBLIC_SOURCES
from run_cfru_dpe_extension_mock_tests import lua_literal
from test_cfru_dpe_host_consumer_source import REVIEWED

ROOT = stock.ROOT
BASE = 'e7485c591c46e4e0ca06b236fc7339bbe0453731'
EXT = '03_tools/tracker-extensions/CFRUDPEExtension/'
HARNESS = '07_scripts/tracker/tests/cfru_dpe_preconsumer_mock.lua'
STOCK_HARNESS = '07_scripts/tracker/tests/cfru_dpe_host_consumer_mock.lua'
STOCK_SHA = '2bd09683acd3b6b95012c35cfda85aa7b84dc569518c0d42e9489556b4dfe48c'
FOOTER = 'local failed, hazards, totals=0,0,{}'


def inputs():
    selected, provenance = stock.definitions()
    for name, (first, last, digest) in REVIEWED.items():
        p = provenance[name]
        if (p['first'], p['last'], p['sha256']) != (first, last, digest):
            raise ValueError('Unreviewed original body: ' + name)
    reader = source.LockedSources(ROOT)
    texts = {f'{component}:{path}': reader.read(component, path)
             for component, paths in PUBLIC_SOURCES.items() for path in paths}
    multi = reader.read('CFRU', 'include/new/multi.h')
    raw = (ROOT / source.OUTPUT).read_text()
    profile = json.loads(raw)
    if hashlib.sha256(raw.encode()).hexdigest() != '8f49fd4156fcd87fefa01a329b7257e61afa0cd997e504d3660bc286c2e87981':
        raise ValueError('Accepted public profile drift')
    for locator, text in {**texts, 'CFRU:include/new/multi.h': multi}.items():
        if source.digest(text.encode()) != profile['metadata']['inputs'][locator]['sha256']:
            raise ValueError('Accepted public input drift: ' + locator)
    old = (ROOT / STOCK_HARNESS).read_bytes()
    if hashlib.sha256(old).hexdigest() != STOCK_SHA or old != stock.git('show', BASE + ':' + STOCK_HARNESS):
        raise ValueError('Accepted #707 bootstrap/controls drift')
    old = old.decode()
    if old.count(FOOTER) != 1:
        raise ValueError('Ambiguous control/driver boundary')
    controls, _ = old.split(FOOTER)
    # Add pure string methods required by the accepted T3/T4 parsers. dump, loaders,
    # host/global namespace access remain denied. Original bodies stay unchanged.
    needle = 'sub=string.sub}'
    if controls.count(needle) != 1:
        raise ValueError('Unreviewed intrinsic string-method seam')
    controls = controls.replace(needle, 'sub=string.sub,byte=string.byte,gsub=string.gsub,gmatch=string.gmatch}')
    needle = '    state.originals={}\n'
    if controls.count(needle) != 1:
        raise ValueError('Unreviewed trusted fixture seam')
    controls = controls.replace(needle, '''    function state.fixtureNamespace(name, values)
        backing[name]=namespace(name,values)
    end
''' + needle)
    return selected, provenance, raw, texts, multi, controls


def payload():
    selected, provenance, raw, texts, multi, controls = inputs()
    prelude = 'local SOURCES=' + stock.literal(selected)
    prelude += '\nlocal MOCK_SOURCE=' + lua_literal(raw)
    prelude += '\nlocal MOCK_PUBLIC_SOURCES=' + lua_literal(texts)
    prelude += '\nlocal MOCK_MULTI=' + lua_literal(multi)
    prelude += '\nlocal guardModule=dofile(' + lua_literal(EXT + 'source_preconsumer_guard.lua') + ')\n'
    # Warm exact immutable-string validation before the per-case instruction budget.
    prelude += '''local warm={Program={},Battle={},Lifecycle={startTracker=function() end}}
local expected={}
for name in pairs(SOURCES) do
 local ns,key=name:match("^(%w+)%.(%w+)$")
 if (ns=="Program" and (key=="updatePokemonTeams" or key=="readNewPokemon"))
 or (ns=="Battle" and (key=="updateViewSlots" or key=="beginNewBattle")) then
  warm[ns][key]=function() error("warm originals must never execute") end
  expected[name]=warm[ns][key]
 end
end
local warmed,why=guardModule.newMock(warm,expected,SOURCES,MOCK_SOURCE,MOCK_PUBLIC_SOURCES,MOCK_MULTI)
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
    result = subprocess.run([executable, '-'], input=chunk, text=True, cwd=ROOT,
                            capture_output=capture, timeout=120)
    return result if capture else result.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lua', default='lua5.4')
    args = parser.parse_args()
    try:
        sys.exit(run(args.lua))
    except (ValueError, subprocess.SubprocessError) as error:
        print('FAIL:', error)
        sys.exit(1)
