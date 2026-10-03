# TM07 Policy A integration and zero-ledger re-audit — 2026-10-03

Contract: [Workspace #627](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/627), integrating accepted [DPE PR #7](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/pull/7) / [Workspace #626](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/626). Branch: `integration/627-tm07-policy-a`; target: `main`; no agent merge.

**Result: `ROM_DATA_LEDGER_ZERO_AFTER_TM07_POLICY_A`. TM07 = 212/212; machine layout issues = 0; tutor layout issues = 0; Move DATA_MATCH = 785 / DATA_MISMATCH = 0; Evolution DATA_MISMATCH = 0; genuine comparable/source-structure mismatch ledger = 0.**

Evidence classification: **CONFIRMED USER DECISION** for Policy A and the bounded Gitlink integration; **CONFIRMED CURRENT STATE** for exact source/history, manifest equality and deterministic comparisons; **UNKNOWN** for retained Ability/mechanics/UPR/acquisition/runtime limitations. The four accepted reports ([#616](gen9-data-parity-2026-10-03.md), [DPE integration](gen9-data-parity-dpe-integration-2026-10-03.md), [CFRU integration](gen9-data-parity-cfru-integration-2026-10-03.md), [Policy A/B evidence](tm07-low-kick-policy-2026-10-03.md)) remain unchanged. This additive report closes only their residual TM07 contract and reconfirms the previously repaired domains.

`ledger = 0` means **zero known genuine comparable/source-structure mismatches in the audited domains**. It does not mean universal Gen-9 mechanics parity, complete binary acquisition legality, safe form selection, runtime acceptance or Randomizer correctness.

## Exact before/after basis

| Role | Before | After |
| --- | --- | --- |
| Workspace | `0b410db755ed3f00e1dbbb76abd82e700ed2bf12` | Containing integration commit / PR head, resolved below |
| CFRU | `fe61d5473c015db71f5f4c5a3335a4a67f943254` | unchanged |
| DPE | `73b3d00859b8d602699775eb41f301901b707b91` | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR-FVX | `7bf79ee1e7c46c972f7a9c84942970a950be0723` | unchanged |
| Showdown | `b1156ff19204e48089e2384eb2c9c1a8004f57ce` | unchanged |

The exact after-Workspace revision is `git log -1 --format=%H -- docs/audits/tm07-policy-a-integration-2026-10-03.md`; its full SHA is recorded in delivery and the PR. This avoids a self-referential commit hash. All other Workspace Gitlinks, including nested reference Gitlinks, are equal to the exact basis. Historical canonical-document pin paragraphs do not override #627's explicit basis.

The starting Workspace was clean on the previous #624 evidence branch. After complete contract/evidence ingestion, Git safety/status checks and verification that fetched `origin/main` equals the basis, the fresh bounded branch was created directly from that basis. Only DPE was checked out at the authorized merged target; no component source was edited.

## Candidate/merge equality and old-pin scope

Both old pin `73b3d00859b8d602699775eb41f301901b707b91` and accepted candidate `f2276651b6f5b06450ab50c875aa475e88c77c0c` are ancestors of merge `d887185de1f6ae6a78e85c4311bbadde17041d00`. Candidate and merge share exact tree `24b1327baa52d5275a8dbd8c5be2a156f45c49ba`; candidate → merge file diff is empty. GitHub PR #7 is merged at that exact target.

The exhaustive old-pin → merge diff, with rename detection disabled, is exactly:

```text
D src/tm_compatibility/7 - Hail.txt
A src/tm_compatibility/7 - Low Kick.txt
```

No third component path changes. The replacement source is byte-equal to the merge Git blob. `7 - Hail.txt` is absent from both the merged tree and checkout. All other machine sources, every tutor source, `src/TM_Tutor_Tables.c`, `scripts/tm_tutor.py`, `include/species.h`, evolution/base/egg data and configuration remain byte-identical to the old DPE pin.

## Exact TM07 identity, manifest and builder replay

Numeric filename slot **7**, `gTMHMMoves[6] = MOVE_LOWKICK`, path **`src/tm_compatibility/7 - Low Kick.txt`** and header **`TM07: Low Kick`** agree. The body is the lexicographically sorted, exact 212-constant Policy A manifest from the merged #624 report at Workspace basis `0b410db7…`; this is manifest verification, not a new policy derivation.

| Manifest check | Result |
| --- | ---: |
| Body constants / unique constants | 212 / 212 |
| Missing against approved A | 0 |
| Extra against approved A | 0 |
| Included B-only constants | 0 of 42 |
| Builder TM07 positive rows | exactly 212 |

All constants exist, have unique numeric species rows and lie within the 1,440-row domain. The Low Kick tutor list was not used as the TM oracle; it remains unchanged. No slot reorder or Policy-B addition occurs.

The comparator compiles only the exact pinned builder's pure utility functions and row-population AST loop. It excludes freshness/output logic and never calls `DataBuilder`. Sources at both pins are supplied in memory; no generated assembly or product artifact is read or written. The actual `FixEndian` byte encoding is decoded back against every row/slot.

- **1,440 independent rows × 128 bits = 23,040 bytes**, 16 bytes per row.
- TM07 is zero-based byte 0, mask `0x40`; its positives equal exactly the numeric rows of the approved 212 constants.
- **All other 127 machine bits are identical for every row** (182,880 preserved row/bit positions).
- Old Hail membership: 241; retained 26, added 186, removed 215; final 212.
- Old bitset SHA-256: `104a1f03d198ea5376c12243e0b2b1c3a3504c3b1e1b4c240e99ec25af054d9a`.
- Merge bitset SHA-256: `7f7685bd360fdf79c9136e64ba53330a29fa4da6cec48a7d546e9095d2c387da`, exactly matching accepted Policy A and candidate #626 evidence.

All **128 machine** and **152 tutor** source-layout checks are regenerated at both pins using the unchanged #616 order/header/file/species parser. Each initializer has exactly its declared count, every numeric slot has exactly one source file, and every header matches the ordered move identity. All body species references resolve within the row domain.

| Domain | Checks | Old layout issues | Merge layout issues |
| --- | ---: | ---: | ---: |
| TM/HM | 128 | 1: machines / slot-7 | **0** |
| Tutor | 152 | 0 | **0** |

Tutor's existing 152-bit / 19-byte layout and acquisition policy remain unchanged. The structural check does not newly classify tutor legality.

## Fresh Move and Evolution re-audit

The temporary comparator imports unchanged read-only #616 domain functions and independently guards current pins, reference hashes, policies and helper hash. It does not invoke the historical full-audit old-pin entry point or alter its PINS. Current source is compared with exact old Git blobs where needed. The fail-closed presence-conditional move preprocessor independently checks current config macro ownership across tracked C/headers; no compiler is invoked.

**Move:** all 833 ordinary mapped records and the full 935-record inventory are regenerated against pinned `moves.ts`. Current and pre-TM07 domains are exactly equal, including every record, field difference, name evidence, uncomparable inventory and preprocessor evidence. CFRU is at the same exact pin and DPE move/species/Ability dependencies are byte-identical. Counts:

| Move classification | Count |
| --- | ---: |
| DATA_MATCH | **785** |
| DATA_MISMATCH | **0** |
| ENGINE_BEHAVIOR_UNVERIFIED | 6 |
| INTENTIONAL_ENGINE_DIFFERENCE | 129 |
| MAPPING_BLOCK | 14 |
| MISSING_LOCAL_MOVE | 1 |

The original pre-repair CFRU table is independently replayed through the same domain comparator: exactly the former 51 mismatch identities become DATA_MATCH, and all other 884 inventory records remain exactly equal. There is no new move mismatch. Earlier #622 macro/PLA/Z/Max proof remains applicable through the identical CFRU source pin; no new full effect or derived-value policy is claimed.

**Evolution:** all 523 mapped source metadata records are independently regenerated before/after the TM07 pin using the exact old evolution blob in a temporary source-only directory. The two complete domain results are exactly equal, including missing handlers, GNU-style initializer disposition, battle transitions and local edges. There are still 785 parsed local evolution/form-transition rows.

| Evolution classification | Count |
| --- | ---: |
| DATA_MISMATCH | **0** |
| REFERENCE_MATCH | 472 |
| ENGINE_TRIGGER_REVIEW | 43 |
| MAPPING_BLOCK | 2 |
| PROJECT_POLICY | 5 |
| UNVERIFIABLE_FROM_SELECTED_REFERENCE | 1 |
| Total mapped reference records | 523 |

The original DPE evolution table is separately replayed: all former 15 level mismatches become REFERENCE_MATCH or ENGINE_TRIGGER_REVIEW, with all other 508 records exactly equal. Both Hisui held-item routes retain trigger review. Evolution source SHA-256 remains `9b57b40f6eb81083c60a63cce18b662644d639c5422e1163ec4d820b0ae707d6`.

As an additional independent check, the fresh complete move/evolution outputs equal #622's accepted deterministic JSON after its SHA-256 `f45475cb06b1dc003f3fc46557ae26104c3468f1a05b29e77db61c90572bc4e0` is verified. This optional cross-check is not required by the embedded replay and adds no new reference dependency.

## Recomputed complete genuine ledger

The unchanged #616 `mismatch_ledger` function receives freshly generated move/evolution records and all machine/tutor layout issues, verifies unique domain/identity keys, and returns an empty final list. Original tables are replayed to regenerate the intermediate totals, rather than merely subtracting a claimed repair count.

| Stage | Move records | Evolution records | TM07 contract | Total |
| --- | ---: | ---: | ---: | ---: |
| Original #616 | 51 | 15 | 1 | **67** |
| After evolution repair | 51 | 0 | 1 | **52** |
| After CFRU move repair / before TM07 | 0 | 0 | 1 | **1** |
| After TM07 Policy A merge pin | 0 | 0 | 0 | **0** |

Complete previous sole entry: `machines / slot-7`, header/order identity conflict. Complete final ledger: **`[]`**. Base-field and approved coherent-learnset zero findings are carried by accepted evidence and byte-identical source continuity; no unrelated full-domain re-audit is claimed. Stantler's obsolete GNU initializer syntax remains a source-style quirk, not a genuine mismatch. Broader acquisition disagreements do not become defects or matches merely because TM07 is resolved.

## Retained UNKNOWNs and separate limitations

Only the explicitly accepted TM07 identity/membership contract is closed. No other classification changes:

- Ability behavior: 310 relevant identities; 1 ALIAS_APPROXIMATION, 30 ALIAS_PLUS_HOOK, 7 MISSING_LOCAL, 9 NAME_ONLY_OR_BEHAVIOR_BLOCKED and **263 UNKNOWN behavior-owner identities**; zero independently certified native behavior owners. Assignment/name/alias evidence does not certify effects or transferable species-gated hooks. Missing Commander/Hospitality/Embody Aspect and partial Palafin/Terapagos remain unchanged.
- UPR evolution preservation: **272 method>15 rows** remain at risk of deletion; the recognized Froslass auxiliary gender field remains at risk of zeroing. The loader/writer is unchanged. Actual frozen randomized-output manifestation remains UNKNOWN.
- Generated-move exposure remains the previous **156 numeric counterexample IDs**; settings-dependent species/form eligibility and Ability-alias selection risks remain separate and uncertified.
- Egg, tutor and broader machine/acquisition generation, inheritance, negative-compatibility and game/event/transfer-policy uncertainties remain. Approved TM07 Policy A supplies only its bounded closed manifest; absence elsewhere is not a universal prohibition.
- Missing Ally Switch and existing mapping limitations, complete Move/Ability effect semantics, omitted evolution triggers, form/transformation mechanics, battle-form safety, runtime, Randomizer manifestation and broader support remain uncertified. No engine or policy implementation is introduced.

**No product build, ROM, emulator, runtime or Randomizer run or acceptance occurred.** Prior runtime evidence is not promoted to this merge pin. No ROM/save/state/build/tool-binary/private-artifact/secret/.env contents were accessed. No component source edit, other Gitlink change, upstream contribution or merge occurred. `UPSTREAM_CONTRIBUTION = DEFERRED`.

## Locked evidence and durable deterministic replay

Only the four locked Showdown data files are read/hash-verified; the historical dex-species sim hash remains inherited ownership evidence, not a fresh fifth-file check. No raw reference source is vendored. Python **3.12.14** used; system python3 is 3.9.6.

| Input / evidence | SHA-256 |
| --- | --- |
| Showdown abilities.ts | `818edd100c8eb5bdf4d4ded8dd1b1ce9d394f87f40f7d9d53a5414276e84f82b` |
| Showdown learnsets.ts | `26969c5e9ca7310b701612da8c9cea217b7d43efb8cd22a7e46783a6ca9b386e` |
| Showdown moves.ts | `cd14e386b4c105a30c09dd0866d1378619f493984d68a782472672cefbcfe186` |
| Showdown pokedex.ts | `73048386b864be5aff093e9393acf32e8016299e9d7b76078bf5120b769e2fe0` |
| showdown_aliases.json | `10585f6b5863ec847264a02e45adf5da190c2783a8fe58ca5f19ca9ea48414ba` |
| showdown_learnset_ownership.json | `b513f4802874ef81e19b54d61da9e6e67e4398d67a220cfc398652e7c41968d1` |
| showdown_pilot_reference.json | `5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd` |
| DPE include/species.h (unchanged) | `27f503f2c95bc0d03f8d28a60a18c90ccabdf9b988e3602dc8751adc5448228a` |
| DPE scripts/tm_tutor.py (unchanged) | `ff60dca2893055e7adba831c74a375f77f0c2bcaee5432aca1156b50c0a051e6` |
| DPE src/TM_Tutor_Tables.c (unchanged) | `86176d7df43e684f11f9506e73a4216a96af79c910c878fe6d9bf2924054d47a` |
| DPE src/tutor_compatibility/7 - Low Kick.txt (unchanged) | `4e81bf995bd85879757c1a4d562747e4f7cf2bef4c725f9e2165e78ef16af10d` |
| Accepted #624 report | `21428c8ae5bc39f809e3c776ba02a0670f5c13078622a0653df0e55759434ffc` |
| Historical #616 helper | `d8882af5629f23f8f0b42b1b79f0686560823f45b3e67ece80bc22ae05e4fb75` |
| Temporary comparator | `2ef6630c8ce0d18ed94dde5b7cf05669b8842d95ad17579652f22a57577c1866` |
| Deterministic JSON | `ce3a18e14defa90beaa5f5e28d3262e7d8929a283661fbd7e4f652a46bdb828f` |

Two fresh comparator processes produced byte-identical JSON. The JSON contains complete before/after move/evolution domains, original/intermediate ledgers, all layouts and hashes; it remains outside Git. The complete comparator is embedded below for durable replay. Extract it unchanged to `/tmp/627-tm07-reaudit.py`, then run from this Workspace branch with the three declared clean component checkouts. `SHOWDOWN_DATA_DIR` identifies the locked four-file data directory inside the exact pinned checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/627-tm07-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/627-tm07-reaudit.json
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/627-tm07-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/627-tm07-reaudit-repeat.json
cmp /tmp/627-tm07-reaudit.json /tmp/627-tm07-reaudit-repeat.json
```

Historical #616 helpers/tests are not rewritten to accept new pins. Their full-entry-point old-pin assertions are obsolete for this integration and are not used as current acceptance gates. #622 recorded the old-pin test failure; that historical result is preserved, not presented as a fresh test run here. The new temporary comparator guards its own exact pins and imports only the necessary domain functions. It never alters the historical PINS or invokes its full audit. For original-source move replay only, the read-only active table reader is temporarily supplied with the exact historical Git blob and restored immediately; no file or pin assertion is patched.

```python
import ast
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
workspace = Path.cwd()
dpe = workspace / '02_external/Dynamic-Pokemon-Expansion-Gen-9'
data = Path(sys.argv[1])
sys.path.insert(0, str(workspace / '07_scripts/data_audit'))
import gen9_data_parity_audit as a
s, c = a.sync, a.closure
merge = 'd887185de1f6ae6a78e85c4311bbadde17041d00'
candidate = 'f2276651b6f5b06450ab50c875aa475e88c77c0c'
workspace_basis = '0b410db755ed3f00e1dbbb76abd82e700ed2bf12'
base = '73b3d00859b8d602699775eb41f301901b707b91'
old = 'src/tm_compatibility/7 - Hail.txt'
new = 'src/tm_compatibility/7 - Low Kick.txt'
report_path = 'docs/audits/tm07-low-kick-policy-2026-10-03.md'

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])

def basis(path):
    return git(dpe, 'show', base + ':' + path)

def digest(data):
    return hashlib.sha256(data).hexdigest()

report_bytes = git(workspace, 'show', workspace_basis + ':' + report_path)
report = report_bytes.decode()

def manifest(heading):
    matches = re.findall(re.escape(heading) + r'\n\n```text\n(.*?)\n```', report, re.S)
    assert len(matches) == 1
    rows = matches[0].splitlines()
    assert rows == sorted(set(rows))
    assert all(re.fullmatch(r'SPECIES_[A-Z0-9_]+', row) for row in rows)
    return set(rows)

A = manifest('### Policy A — 212 constants')
B = manifest('### Policy B — 254 constants')
B_only = manifest('### B-only — 42')
assert len(A) == 212 and len(B) == 254 and len(B_only) == 42
assert A <= B and B - A == B_only

assert git(workspace, 'merge-base', 'HEAD', workspace_basis).decode().strip() == workspace_basis
assert git(workspace, 'branch', '--show-current').decode().strip() == 'integration/627-tm07-policy-a'
pins = {'02_external/CFRU-expansion': 'fe61d5473c015db71f5f4c5a3335a4a67f943254',
        '02_external/Dynamic-Pokemon-Expansion-Gen-9': merge,
        '02_external/upr-fvx': '7bf79ee1e7c46c972f7a9c84942970a950be0723'}
for path, pin in pins.items():
    assert git(workspace/path, 'rev-parse', 'HEAD').decode().strip() == pin
    assert not git(workspace/path, 'status', '--porcelain')
    assert git(workspace, 'rev-parse', workspace_basis+':'+path).decode().strip() == (base if path == str(dpe.relative_to(workspace)) else pin)
for pin in (base, candidate):
    assert git(dpe, 'merge-base', pin, merge).decode().strip() == pin
assert git(dpe, 'rev-parse', candidate+'^{tree}') == git(dpe, 'rev-parse', merge+'^{tree}')
assert not git(dpe, 'diff', candidate, merge)
assert git(dpe, 'diff', '--name-status', '--no-renames', base, merge).decode().splitlines() == ['D\t'+old, 'A\t'+new]
assert not (dpe/old).exists() and not git(dpe, 'ls-tree', '--name-only', merge, '--', old)
assert git(dpe, 'show', merge+':'+new) == (dpe/new).read_bytes()
lines = (dpe/new).read_text().splitlines()
assert lines[0] == 'TM07: Low Kick'
assert lines[1:] == sorted(A) and len(lines[1:]) == 212
assert not A & B_only and int(Path(new).name.split()[0]) == 7
unchanged = {}
for path in ['include/species.h', 'scripts/tm_tutor.py', 'src/TM_Tutor_Tables.c',
             'src/tutor_compatibility/7 - Low Kick.txt']:
    source_bytes = (dpe / path).read_bytes()
    assert source_bytes == basis(path), path
    unchanged[path] = digest(source_bytes)
order_source = re.sub(r'/\*.*?\*/|//[^\n]*', '', basis('src/TM_Tutor_Tables.c').decode(), flags=re.S)
order = re.search(r'gTMHMMoves\s*\[.*?\]\s*=\s*\{(.*?)\}', order_source, re.S).group(1)
moves = re.findall(r'\bMOVE_[A-Z0-9_]+\b', order)
assert len(moves) == 128 and moves[6] == 'MOVE_LOWKICK'

# Read only tracked TM sources. The baseline comes from exact Git blobs.
paths = git(dpe, 'ls-tree', '-r', '--name-only', base, '--', 'src/tm_compatibility').decode().splitlines()
assert len(paths) == 128 and all(path.endswith('.txt') for path in paths)
before = {path: basis(path).decode() for path in paths}
after = {path: (dpe / path).read_text() for path in paths if path != old}
after[new] = (dpe / new).read_text()
assert set(before) - set(after) == {old} and set(after) - set(before) == {new}
assert all(before[path] == after[path] for path in set(before) & set(after))

# Compile the existing pure utility functions and the exact builder row loop.
# Exclude its output/freshness code: no DataBuilder call or artifact access.
tree = ast.parse(basis('scripts/tm_tutor.py').decode())
functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
namespace = {}
counts = [node for node in tree.body if isinstance(node, ast.Assign)
          and any(isinstance(target, ast.Name) and target.id in {'TM_HM_COUNT', 'SPECIES_COUNT'}
                  for target in node.targets)]
utilities = [functions[name] for name in ['FixEndian', 'ReverseString',
             'PokemonDataListInitializer', 'DefinesDictMaker', 'ReverseDict']]
module = ast.fix_missing_locations(ast.Module(body=counts + utilities, type_ignores=[]))
exec(compile(module, '<tm_tutor pure utilities>', 'exec'), namespace)
assert namespace['TM_HM_COUNT'] == 128 and namespace['SPECIES_COUNT'] == 1440
species_text = basis('include/species.h').decode()
raw_constants = re.findall(r'^#define\s+(SPECIES_\w+)\s+(0x[0-9A-Fa-f]+|[0-9]+)\b', species_text, re.M)
values = {name: int(value, 0) for name, value in raw_constants}
assert len(values) == len(raw_constants)
assert len(set(values.values())) == len(values), 'species-row collision'
assert all(0 <= value < 1440 for value in values.values())
assert A <= values.keys()

species_open = lambda path, mode='r': io.StringIO(species_text) if path == 'include/species.h' and mode == 'r' else fail(path)

def fail(message):
    raise AssertionError(message)

namespace['open'] = species_open
species_dict = namespace['DefinesDictMaker']('include/species.h')
reverse = namespace['ReverseDict'](species_dict)
assert reverse == values
namespace['ReverseSpeciesDict'] = reverse
namespace['sys'] = sys
namespace['print'] = lambda *args, **kwargs: fail(('builder parsing error', args))
loop = next(node for node in functions['DataBuilder'].body
            if isinstance(node, ast.For) and isinstance(node.target, ast.Name) and node.target.id == 'filePath')
loop_module = ast.fix_missing_locations(ast.Module(body=[loop], type_ignores=[]))
loop_code = compile(loop_module, '<exact DataBuilder row loop>', 'exec')

def replay(sources):
    slots = [int(Path(path).name.split()[0]) for path in sources]
    assert sorted(slots) == list(range(1, 129))
    def source_open(path, mode='r'):
        assert mode == 'r' and path in sources
        return io.StringIO(sources[path])
    namespace.update(open=source_open, fileList=sorted(sources), numEntries=128,
                     compatibilityTable=namespace['PokemonDataListInitializer'](128))
    exec(loop_code, namespace)
    rows = namespace['compatibilityTable']
    assert len({id(row) for row in rows}) == 1440
    assert all(len(row) == 128 for row in rows)
    encoded = bytearray()
    for row in rows:
        bits = namespace['FixEndian'](''.join(map(str, row)))
        assert len(bits) == 128
        encoded.extend(int(bits[offset:offset + 8], 2) for offset in range(0, 128, 8))
    assert len(encoded) == 23040
    assert all(((encoded[n * 16 + slot // 8] >> (slot % 8)) & 1) == rows[n][slot]
               for n in range(1440) for slot in range(128))
    return rows, encoded

old_rows, old_bits = replay(before)
new_rows, new_bits = replay(after)
assert {n for n in range(1440) if new_rows[n][6]} == {values[name] for name in A}
assert sum(row[6] for row in new_rows) == 212
assert all(old_rows[n][slot] == new_rows[n][slot]
           for n in range(1440) for slot in range(128) if slot != 6)
assert all(((a ^ b) & (0xBF if offset % 16 == 0 else 0xFF)) == 0
           for offset, (a, b) in enumerate(zip(old_bits, new_bits)))
assert digest(new_bits) == '7f7685bd360fdf79c9136e64ba53330a29fa4da6cec48a7d546e9095d2c387da'
old_tm = {n for n in range(1440) if old_rows[n][6]}
new_tm = {values[name] for name in A}
assert (len(old_tm), len(old_tm & new_tm), len(new_tm - old_tm), len(old_tm - new_tm)) == (241, 26, 186, 215)

# Independent current-pin/reference guards; do not call a.verify/a.run or patch PINS.
assert c.digest(s.SCRIPT_DIR/'gen9_data_parity_audit.py') == 'd8882af5629f23f8f0b42b1b79f0686560823f45b3e67ece80bc22ae05e4fb75'
assert c.digest(c.REFERENCE) == '5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd'
reference = json.loads(c.REFERENCE.read_text())
assert c.git(data, 'rev-parse', 'HEAD') == reference['revision'] == 'b1156ff19204e48089e2384eb2c9c1a8004f57ce'
reference_hashes = {n:c.digest(data/n) for n in reference['sha256']}
assert reference_hashes == reference['sha256']
for n, field in [('showdown_aliases.json','aliases_sha256'),('showdown_learnset_ownership.json','ownership_sha256')]:
    assert c.digest(s.SCRIPT_DIR/n) == reference[field]
aliases, _ = s.alias_indexes()
mapped, coverage = a.species_audit(s.parse_pokedex(data/'pokedex.ts'), aliases, s.constants_by_kind('species'))
assert len(mapped) == 1293
moves_after = a.move_audit(data, aliases)
assert moves_after['counts'] == {'DATA_MATCH':785,'ENGINE_BEHAVIOR_UNVERIFIED':6,'INTENTIONAL_ENGINE_DIFFERENCE':129,'MAPPING_BLOCK':14,'MISSING_LOCAL_MOVE':1}
assert moves_after['normal_mapping_count'] == 833 and len(moves_after['rows']) == 935
# Same exact CFRU pin + identical DPE move dependencies establish the before input.
for path in ['include/species.h','include/moves.h','include/abilities.h','src/defines.h']:
    assert basis(path) == (dpe/path).read_bytes()
moves_before = a.move_audit(data, aliases)
assert moves_before == moves_after
# Recompute old and new evolution domains separately using the exact old Git blob.
import tempfile
with tempfile.TemporaryDirectory(prefix='627-old-source-') as tmp:
    temp = Path(tmp); (temp/'src').mkdir()
    (temp/'src/Evolution Table.c').write_bytes(basis('src/Evolution Table.c'))
    s.DPE_ROOT = temp
    try: evolution_before = a.evolution_audit(data, mapped)
    finally: s.DPE_ROOT = dpe
evolution_after = a.evolution_audit(data, mapped)
assert evolution_before == evolution_after
assert evolution_after['counts'] == {'REFERENCE_MATCH':472,'ENGINE_TRIGGER_REVIEW':43,'MAPPING_BLOCK':2,'PROJECT_POLICY':5,'UNVERIFIABLE_FROM_SELECTED_REFERENCE':1}
assert len(evolution_after['rows']) == 523
assert sum(len(v) for v in a.evolution_rows((dpe/'src/Evolution Table.c').read_text()).values()) == 785
assert c.digest(dpe/'src/Evolution Table.c') == '9b57b40f6eb81083c60a63cce18b662644d639c5422e1163ec4d820b0ae707d6'
# Complete source-layout identity checks at both pins, without acquisition reclassification.
layouts_before, layouts_after = {}, {}
for domain, name, count, directory in [('machines','gTMHMMoves',128,'tm_compatibility'),('tutors','gMoveTutorMoves',152,'tutor_compatibility')]:
    order, explicit = a.move_order((dpe/'src/TM_Tutor_Tables.c').read_text(),name,count)
    assert explicit == count
    pairs, issues, files = a.compatibility_files(dpe/('src/'+directory),count,order,values)
    assert not issues and len(files) == count
    layouts_after[domain] = {'layout_issues':issues,'files':files,'order':order,'checks':count}
    if domain == 'machines':
        assert order[6] == 'MOVE_LOWKICK'
        assert pairs == {(n, slot) for n, row in enumerate(new_rows) for slot, bit in enumerate(row) if bit}
    with tempfile.TemporaryDirectory(prefix='627-old-layout-') as tmp:
        temp = Path(tmp)
        tracked = git(dpe,'ls-tree','-r','--name-only',base,'--','src/'+directory).decode().splitlines()
        assert len(tracked) == count
        for path in tracked: (temp/Path(path).name).write_bytes(basis(path))
        _, old_issues, old_files = a.compatibility_files(temp,count,order,values)
    layouts_before[domain] = {'layout_issues':old_issues,'files':old_files,'order':order,'checks':count}
assert layouts_before['machines']['layout_issues'] == [{'slot':7,'file':'7 - Hail.txt','move':'MOVE_LOWKICK','class':'DATA_MISMATCH','reason':'header/order identity differs'}]
assert not layouts_before['tutors']['layout_issues']
# All untouched domains and all other Workspace Gitlinks are continuity-bound.
for path in ['src/Base_Stats.c','src/Learnsets.c','src/Egg_Moves.c','src/Evolution Table.c','include/evolution.h']:
    assert basis(path) == (dpe/path).read_bytes()
assert not re.search(r'^\s*#define\s+EXPAND_LEARNSETS\b', c.uncomment((dpe/'src/defines.h').read_text()),re.M)
assert re.search(r'^\s*#define\s+EXPAND_MOVESETS\b',c.uncomment((s.CFRU_ROOT/'src/config.h').read_text()),re.M)
ledger_before = a.mismatch_ledger({'moves':moves_before,'evolutions':evolution_before,'base':{'genuine_mismatches':[]},**layouts_before})
ledger_after = a.mismatch_ledger({'moves':moves_after,'evolutions':evolution_after,'base':{'genuine_mismatches':[]},**layouts_after})
assert len(ledger_before) == 1 and ledger_before[0]['identity'] == 'slot-7' and ledger_before[0]['domain'] == 'machines'
assert ledger_after == []
# Original accepted 67 and intermediate 52 are regenerated through unchanged functions.
original_move_text = git(s.CFRU_ROOT,'show',a.PINS['CFRU']+':src/Tables/battle_moves.c').decode()
_, config = a.preprocess((s.CFRU_ROOT/'src/config.h').read_text())
old_active, _ = a.preprocess(original_move_text, config)
_, pp = a.active_move_source()
reader = a.active_move_source
a.active_move_source = lambda:(old_active,dict(pp,active_source_sha256=digest(old_active.encode())))
try: original_moves = a.move_audit(data,aliases)
finally: a.active_move_source = reader
assert original_moves['counts']['DATA_MISMATCH'] == 51
with tempfile.TemporaryDirectory(prefix='627-original-evolution-') as tmp:
    temp = Path(tmp); (temp/'src').mkdir()
    (temp/'src/Evolution Table.c').write_bytes(git(dpe,'show',a.PINS['DPE']+':src/Evolution Table.c'))
    s.DPE_ROOT = temp
    try: original_evolution = a.evolution_audit(data,mapped)
    finally: s.DPE_ROOT = dpe
assert original_evolution['counts']['DATA_MISMATCH'] == 15
original_ledger = a.mismatch_ledger({'moves':original_moves,'evolutions':original_evolution,'base':{'genuine_mismatches':[]},**layouts_before})
intermediate_ledger = a.mismatch_ledger({'moves':original_moves,'evolutions':evolution_before,'base':{'genuine_mismatches':[]},**layouts_before})
assert len(original_ledger) == 67 and len(intermediate_ledger) == 52
expected_original = {r['source'] for r in original_moves['rows'] if r['class']=='DATA_MISMATCH'}
old_m = {r['source']:r for r in original_moves['rows']}; new_m = {r['source']:r for r in moves_after['rows']}
assert old_m.keys() == new_m.keys()
assert all(new_m[k]['class']=='DATA_MATCH' if k in expected_original else new_m[k]==old_m[k] for k in old_m)
old_e = {r['source']:r for r in original_evolution['rows']};new_e = {r['source']:r for r in evolution_after['rows']}
assert old_e.keys() == new_e.keys()
assert all(new_e[k]['class'] in ('REFERENCE_MATCH','ENGINE_TRIGGER_REVIEW') if old_e[k]['class']=='DATA_MISMATCH' else old_e[k]==new_e[k] for k in old_e)
result = {'result':'ROM_DATA_LEDGER_ZERO_AFTER_TM07_POLICY_A','evidence':'SOURCE_STATIC_ONLY',
 'workspace_basis':workspace_basis,'DPE_before':base,'candidate':candidate,'DPE_after':merge,
 'candidate_merge_tree':git(dpe,'rev-parse',merge+'^{tree}').decode().strip(),
 'pins':pins,'reference_revision':reference['revision'],'reference_hashes':reference_hashes,
 'policy_hashes':{n:c.digest(s.SCRIPT_DIR/n) for n in ['showdown_pilot_reference.json','showdown_aliases.json','showdown_learnset_ownership.json']},
 'manifest_report_sha256':digest(report_bytes),'manifest_count':212,'missing':0,'extra':0,'B_only_included':0,
 'TM07_positives':sum(row[6] for row in new_rows),'other_127_bits_preserved':True,
 'bitset_bytes':len(new_bits),'rows':1440,'bits_per_row':128,'old_bitset_sha256':digest(old_bits),'merge_bitset_sha256':digest(new_bits),
 'old_Hail_absent':True,'unchanged_source_sha256':unchanged,'layouts_before':layouts_before,'layouts_after':layouts_after,
 'moves_before':moves_before,'moves_after':moves_after,'evolution_before':evolution_before,'evolution_after':evolution_after,
 'original_ledger':original_ledger,'intermediate_ledger':intermediate_ledger,'ledger_before':ledger_before,'ledger_after':ledger_after,
 'ledger_counts':[67,52,1,0],'helper_sha256':c.digest(s.SCRIPT_DIR/'gen9_data_parity_audit.py'),'comparator_sha256':c.digest(Path(__file__))}
print(json.dumps(result,sort_keys=True,indent=2))
```

## Checks and CONTROL handoff

PASS: safety checks before changes and handoff; clean starting state; exact Workspace/component basis; old/candidate ancestry; candidate/merge tree and file equality; exhaustive two-path DPE scope; exact A manifest/body/header/slot; old Hail absence; pure in-memory builder replay and encode/decode; all other 127 bits preserved; 128 machine + 152 tutor layout checks; complete move/evolution re-audits and original-ledger replay; reference/policy/helper hashes; deterministic repeat equality; whitespace/status/stat/submodule-log review; exact staged/committed two-path Workspace allowlist and all-other-Gitlink equality. Only the authorized DPE Gitlink and this additive report change.

**Handoff to CONTROL:** review the exact Workspace PR/head and DPE `73b3d008… → d887185d…` transition against #627. After **user merge**, CONTROL may close #627 and reconsider #498 Phase R1 using live Project/Issue state. This evidence does not automatically resume #498, open another contract, certify runtime, or declare acceptance/freeze. The retained UNKNOWNs and Randomizer preservation risks remain visible inputs to that routing decision. User merge/acceptance remains separate; Codex performs no merge.
