#!/usr/bin/env python3
"""#707: execute only reviewed definitions from immutable public Tracker Lua blobs."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = 'c16db3221ca772701c0a38dd0a181f4721ed528e'
PIN = 'c450ecaee2d8131a2789bb656e3be792a93712fb'
TRACKER = ROOT / '02_external/Ironmon-Tracker'
SELECTION = {
    'Program.lua': ['Program.readNewPokemon', 'Program.updatePokemonTeams', 'Program.validPokemonData'],
    'Battle.lua': ['Battle.inActiveBattle', 'Battle.getViewedPokemon', 'Battle.updateViewSlots', 'Battle.beginNewBattle'],
    'TrackerAPI.lua': ['TrackerAPI.getPlayerPokemon', 'TrackerAPI.getEnemyPokemon', 'TrackerAPI.getActiveBattlePokemon'],
    'Tracker.lua': ['Tracker.getPokemon', 'Tracker.saveData', 'Tracker.loadData', 'Tracker.verifyDataForPlayer'],
    'data/DataHelper.lua': ['DataHelper.buildTrackerScreenDisplay'],
}
WITNESSES = ('screens/TrackerScreen.lua', 'screens/BattleDetailsScreen.lua', 'data/MiscData.lua')
# Lua lexical tokens: comments and quoted/long strings never contribute block keywords.
TOKEN = re.compile(r'--\[(=*)\[.*?\]\1\]|--[^\n]*|\[(=*)\[.*?\]\2\]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z_0-9]*|[^\s]', re.S)


def tokens(source):
    end = 0
    for match in TOKEN.finditer(source):
        if source[end:match.start()].strip():
            raise ValueError('Unrecognized lexical gap')
        end = match.end()
        token = match.group()
        if token.startswith(('--', '"', "'", '[')) and (token != '['):
            continue
        yield token, match.start(), match.end()
    if source[end:].strip():
        raise ValueError('Unrecognized lexical tail')


def extract(source, name):
    """Balance Lua blocks after a unique named definition, retaining exact bytes.

    for/while own their do; standalone do owns a block; repeat owns until.
    elseif/else share the original if block. Nested anonymous functions count.
    This intentionally supports reviewed stock syntax, not arbitrary Lua parsing.
    """
    stream = list(tokens(source))
    wanted = ['function'] + re.findall(r'[A-Za-z_][A-Za-z_0-9]*|[.:]', name) + ['(']
    hits = [i for i in range(len(stream)) if [t[0] for t in stream[i:i+len(wanted)]] == wanted]
    if len(hits) != 1:
        raise ValueError('Definition missing or ambiguous: ' + name)
    start = hits[0]
    stack = []
    for token, _, stop in stream[start:]:
        if token in ('function', 'if', 'repeat'):
            stack.append(token)
        elif token in ('for', 'while'):
            stack.append('pending-do')
        elif token == 'do':
            if stack and stack[-1] == 'pending-do':
                stack[-1] = 'do'
            else:
                stack.append('do')
        elif token in ('end', 'until'):
            if not stack or (token == 'until') != (stack[-1] == 'repeat'):
                raise ValueError('Unbalanced block: ' + name)
            stack.pop()
            if not stack:
                begin = stream[start][1]
                return source[begin:stop], source.count('\n', 0, begin)+1, source.count('\n', 0, stop)+1
    raise ValueError('Unterminated definition: ' + name)


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', *args], cwd=cwd)


def public_sources():
    if git('rev-parse', 'HEAD', cwd=TRACKER).decode().strip() != PIN:
        raise ValueError('Tracker checkout is not the approved pin')
    links = git('ls-tree', 'HEAD', '--', '02_external/Ironmon-Tracker').decode()
    if PIN not in links or not links.startswith('160000 '):
        raise ValueError('Workspace Tracker Gitlink changed')
    sources = {}
    for path in (*SELECTION, *WITNESSES):
        locator = 'ironmon_tracker/' + path
        committed = git('show', PIN + ':' + locator, cwd=TRACKER)
        actual = (TRACKER / locator).read_bytes()
        if actual != committed:
            raise ValueError('Public Lua source differs from pinned blob: ' + path)
        sources[path] = actual.decode('utf-8')
    return sources


def definitions():
    sources = public_sources()
    selected, provenance = {}, {}
    for path, names in SELECTION.items():
        blob = git('rev-parse', PIN + ':ironmon_tracker/' + path, cwd=TRACKER).decode().strip()
        for name in names:
            body, first, last = extract(sources[path], name)
            selected[name] = body
            provenance[name] = {'path': path, 'blob': blob, 'first': first, 'last': last,
                                'sha256': hashlib.sha256(body.encode()).hexdigest()}
    return selected, provenance


def literal(value):
    if isinstance(value, str):
        return '"' + ''.join('\\%03d' % b for b in value.encode('utf-8')) + '"'
    return '{' + ','.join('[' + literal(k) + ']=' + literal(v) for k,v in value.items()) + '}'


def run(runtime='lua5.4', capture=False):
    executable = shutil.which(runtime)
    if not executable:
        print('NOT_RUN: existing Lua 5.4 unavailable')
        return 2
    probe = subprocess.run([executable, '-e', 'io.write(_VERSION)'], capture_output=True, text=True, timeout=10)
    if probe.returncode or probe.stdout != 'Lua 5.4':
        print('NOT_RUN: requires existing Lua 5.4')
        return 2
    selected, provenance = definitions()
    for name, record in provenance.items():
        print('SOURCE', name, record, flush=True)
    # Trusted bootstrap itself is the only local harness read; no runtime modules.
    harness = (ROOT / '07_scripts/tracker/tests/cfru_dpe_host_consumer_mock.lua').read_text()
    payload = 'local SOURCES=' + literal(selected) + '\n' + harness
    result = subprocess.run([executable, '-'], input=payload, text=True, cwd=ROOT,
                            capture_output=capture, timeout=30)
    if capture:
        return result
    return result.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lua', default='lua5.4')
    args = parser.parse_args()
    try:
        sys.exit(run(args.lua))
    except (ValueError, subprocess.SubprocessError) as error:
        print('FAIL:', error)
        sys.exit(1)
