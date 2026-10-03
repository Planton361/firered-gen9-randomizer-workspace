# DPE integration and evolution parity re-audit — 2026-10-03

Contract: [Workspace #619](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/619), integrating [DPE PR #6](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/pull/6). Branch: `integration/619-dpe-evolution-parity`; target: `main`; no agent merge.

**Verdict: `DPE_EVOLUTION_PARITY_REPAIRED_WITH_TM07_UNKNOWN`.** The former 15 evolution-level `DATA_MISMATCH` records are now **0**. No new evolution mismatch is introduced. The genuine mismatch ledger changes only by these 15 records: **67 − 15 = 52** (51 CFRU move records + one unresolved TM07 identity contract). This is source evidence, not full Gen-9 parity or runtime acceptance.

Evidence classification: **CONFIRMED CURRENT STATE** for exact Git history, source continuity and deterministic evolution comparisons; **CONFIRMED USER DECISION** for the bounded integration authorization; **UNKNOWN** for retained uncertified mechanics and acquisition policies. The accepted [#616 report](gen9-data-parity-2026-10-03.md) and its helper remain unchanged historical evidence. This additive report supersedes only its old-pin evolution-level findings.

## Exact integration basis

| Role | Before | After |
| --- | --- | --- |
| Workspace basis | `7538acd9660fdda651e7dc72d22e32ae11453883` | This report's containing integration commit, identified by the PR head |
| CFRU | `237e1dfaa785af332ddad72af906b3bba5beaab9` | unchanged |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | `73b3d00859b8d602699775eb41f301901b707b91` |
| UPR-FVX | `7bf79ee1e7c46c972f7a9c84942970a950be0723` | unchanged |
| Showdown | `b1156ff19204e48089e2384eb2c9c1a8004f57ce` | unchanged |

The after-Workspace revision is unambiguously the commit that adds this report and updates the sole authorized Gitlink; `git log -1 --format=%H -- docs/audits/gen9-data-parity-dpe-integration-2026-10-03.md` resolves it without a self-referential hash. The exact commit is also recorded in the delivery/PR. All other Gitlinks remain identical to the basis. Older canonical-document pin paragraphs are historical relative to this Issue's explicit exact basis.

## DPE merge proof and all repaired rows

Both old pin `22ffa27...` and accepted candidate `ceb5fa5f030971712d36ca2a649a769cbf89ceb2` are ancestors of merged target `73b3d008...`. Candidate-to-merge tree diff is empty. Old-to-merge diff changes only `src/Evolution Table.c`.

All 785 parsed local evolution/form-transition rows retain parent identity, row order and count. Exactly 15 rows change exactly field 1 (the level parameter); method, target and auxiliary field are identical. Replacing those 15 tokens reconstructs the entire target file byte-for-byte, proving no unrelated textual/source change.

| Parent | Target | Method | Old level | New/reference level | After classification |
| --- | --- | --- | --- | --- | --- |
| SPECIES_BINACLE | SPECIES_BARBARACLE | EVO_LEVEL | 36 | 39 | REFERENCE_MATCH |
| SPECIES_RUFFLET | SPECIES_BRAVIARY | EVO_LEVEL | 50 | 54 | REFERENCE_MATCH |
| SPECIES_RUFFLET | SPECIES_BRAVIARY_H | EVO_LEVEL_HOLD_ITEM | 50 | 54 | ENGINE_TRIGGER_REVIEW |
| SPECIES_DARTRIX | SPECIES_DECIDUEYE_H | EVO_LEVEL_HOLD_ITEM | 34 | 36 | ENGINE_TRIGGER_REVIEW |
| SPECIES_SNORUNT | SPECIES_GLALIE | EVO_LEVEL | 30 | 42 | REFERENCE_MATCH |
| SPECIES_KLINK | SPECIES_KLANG | EVO_LEVEL | 35 | 38 | REFERENCE_MATCH |
| SPECIES_KLANG | SPECIES_KLINKLANG | EVO_LEVEL | 45 | 49 | REFERENCE_MATCH |
| SPECIES_SLUGMA | SPECIES_MAGCARGO | EVO_LEVEL | 30 | 38 | REFERENCE_MATCH |
| SPECIES_VULLABY | SPECIES_MANDIBUZZ | EVO_LEVEL | 50 | 54 | REFERENCE_MATCH |
| SPECIES_MIENFOO | SPECIES_MIENSHAO | EVO_LEVEL | 46 | 50 | REFERENCE_MATCH |
| SPECIES_GLAMEOW | SPECIES_PURUGLY | EVO_LEVEL | 34 | 38 | REFERENCE_MATCH |
| SPECIES_DUCKLETT | SPECIES_SWANNA | EVO_LEVEL | 30 | 35 | REFERENCE_MATCH |
| SPECIES_PUPITAR | SPECIES_TYRANITAR | EVO_LEVEL | 48 | 55 | REFERENCE_MATCH |
| SPECIES_VANILLITE | SPECIES_VANILLISH | EVO_LEVEL | 24 | 35 | REFERENCE_MATCH |
| SPECIES_VANILLISH | SPECIES_VANILLUXE | EVO_LEVEL | 42 | 47 | REFERENCE_MATCH |

The two Hisui held-item rows now match the selected level, while retaining `ENGINE_TRIGGER_REVIEW` for their Hisui Rock route. No engine-support claim follows from repairing their levels.

## Full evolution-domain comparison

The unchanged #616 `species_audit`, `evolution_rows` and `evolution_audit` functions are imported read-only. The same aliases and reviewed species ownership are used. The old table is obtained from its exact Git blob and supplied through an external temporary directory; the new table is read at the merged DPE pin. No hard-coded pin check in the historical helper is edited or bypassed to run its full audit: the temporary comparator performs its own explicit current-pin, ancestry, reference and policy checks, then calls only the existing evolution-domain functions.

All **523 mapped source evolution metadata records** are regenerated against the same pinned `pokedex.ts` and comparison policy. The comparison covers relationships, supplied level/item/move/method metadata, alternate local parents, missing handlers, and battle transitions. It does not infer omitted trigger thresholds, probabilities, regional/version rules or complete mechanics.

| Classification | Before | After |
| --- | --- | --- |
| DATA_MISMATCH | 15 | **0** |
| REFERENCE_MATCH | 459 | 472 |
| ENGINE_TRIGGER_REVIEW | 41 | 43 |
| MAPPING_BLOCK | 2 | 2 |
| PROJECT_POLICY | 5 | 5 |
| UNVERIFIABLE_FROM_SELECTED_REFERENCE | 1 | 1 |
| Total | 523 | 523 |

All 508 records outside the 15 repaired targets are exactly equal, including their classifications and metadata. No target is added or removed. Every repaired target becomes a reference match or, for the two Hisui routes, a level-correct trigger-review record. The complete missing-CFRU-case inventory, battle-transition inventory and Stantler GNU-style disposition are exactly equal. All remaining trigger, parent-mapping and event/form uncertainties from #616 Appendix F are retained. **New DPE evolution mismatches: 0.**

## Unchanged source domains and retained findings

The exhaustive old-to-new DPE file diff proves byte-identical `src/Base_Stats.c` and all type/gender/egg-group/Ability-assignment inputs, constants, Ability representations, egg sources, TM/tutor sources and configuration. CFRU and UPR-FVX are unchanged exact pins with clean tracked source. CFRU `EXPAND_MOVESETS` remains active; DPE `EXPAND_LEARNSETS` remains commented out. The active CFRU level-up table is unaffected. This is continuity evidence; no unrelated full-domain re-audit or reclassification is claimed.

- **51 CFRU move-data mismatches remain pending separate repair**, with the exact identities and field evidence in #616 §13 unchanged.
- Ability boundaries remain unchanged: 310 relevant identities; 1 `ALIAS_APPROXIMATION`, 30 `ALIAS_PLUS_HOOK`, 7 `MISSING_LOCAL`, 9 `NAME_ONLY_OR_BEHAVIOR_BLOCKED`, 263 `UNKNOWN`; zero independently certified native behavior owners. Missing Commander/Hospitality/Embody Aspect and partial Palafin/Terapagos remain unchanged.
- UPR evolution-preservation risks remain: 272 source rows with methods beyond loader IDs 1..15 risk deletion; one recognized Froslass auxiliary gender condition risks zeroing. The two repaired Hisui held-item rows still belong to the same unsupported-loader method domain; corrected levels do not repair preservation. Generated-move exposure (156 counterexample IDs), species/form eligibility and species-gated Ability alias risks remain unchanged. Actual frozen randomized-output manifestation is **UNKNOWN**.
- Egg, tutor and aggregate acquisition-policy uncertainties remain unchanged. No negative compatibility oracle or new generation/inheritance policy is selected.
- TM07 is explicitly **UNKNOWN / unresolved**: `gTMHMMoves[6] = MOVE_LOWKICK`, while the compatibility owner remains `src/tm_compatibility/7 - Hail.txt` with header `TM07: Hail`. Its numeric filename supplies membership to that slot. The identity conflict remains one genuine mismatch; exact intended Low Kick TM membership policy remains **UNKNOWN**. No membership repair or slot reordering occurs.

The residual ledger is exactly **52 affected records/contracts**, not a species count or proof of complete effects. Subtracting only the 15 repaired level records does not waive TM07 or any unrelated #616 finding.

## Locked inputs and deterministic evidence

Only the four previously allowed sparse Showdown data files are read; no fifth sim file is verified and no raw reference is vendored. The reference lock's historical `dex_species_sha256` remains inherited policy evidence, not a newly verified input.

| Input | SHA-256 |
| --- | --- |
| abilities.ts | `818edd100c8eb5bdf4d4ded8dd1b1ce9d394f87f40f7d9d53a5414276e84f82b` |
| learnsets.ts | `26969c5e9ca7310b701612da8c9cea217b7d43efb8cd22a7e46783a6ca9b386e` |
| moves.ts | `cd14e386b4c105a30c09dd0866d1378619f493984d68a782472672cefbcfe186` |
| pokedex.ts | `73048386b864be5aff093e9393acf32e8016299e9d7b76078bf5120b769e2fe0` |
| showdown_aliases.json | `10585f6b5863ec847264a02e45adf5da190c2783a8fe58ca5f19ca9ea48414ba` |
| showdown_learnset_ownership.json | `b513f4802874ef81e19b54d61da9e6e67e4398d67a220cfc398652e7c41968d1` |
| showdown_pilot_reference.json | `5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd` |
| helper | `d8882af5629f23f8f0b42b1b79f0686560823f45b3e67ece80bc22ae05e4fb75` |
| new_evolution | `9b57b40f6eb81083c60a63cce18b662644d639c5422e1163ec4d820b0ae707d6` |
| old_evolution | `04c839474c547813afd7164fe7cee159ded80d5a5acd6ee82272a6c6d35ad3bb` |
| script | `2c4ce040c90bd6fcc9cfc1e285d7e035854cf7f157a3ea60769849d9bd10dd8e` |
| deterministic comparison JSON | `e7c2a433f790aa324177da99d91f6c17fe64eb68af3fffdfb633ea3a9b013fb3` |

Python 3.12.14 was used. Two fresh runs produce byte-identical JSON. The JSON includes all before/after evolution records and local edges, the exact 15 changes and input hashes; it stays outside Git. The complete temporary comparator is reproduced below for durable replay. Extract the Python block to `/tmp/619-evolution-reaudit.py` without changing its contents, then run from the Workspace root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/619-evolution-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/619-evolution-reaudit.json
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/619-evolution-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/619-evolution-reaudit-repeat.json
cmp /tmp/619-evolution-reaudit.json /tmp/619-evolution-reaudit-repeat.json
```

`SHOWDOWN_DATA_DIR` must identify the four-file `data` directory inside a checkout at the exact pinned Showdown commit. The script fails on reference/policy drift, dirty tracked component source, unexpected ancestry, extra component changes, incorrect repair fields, changed unaffected records or any remaining/new mismatch.

```python
import hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / '07_scripts/data_audit'))
import gen9_data_parity_audit as audit
s, c = audit.sync, audit.closure
old = '22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc'
new = '73b3d00859b8d602699775eb41f301901b707b91'
basis = '7538acd9660fdda651e7dc72d22e32ae11453883'
candidate = 'ceb5fa5f030971712d36ca2a649a769cbf89ceb2'
data = Path(sys.argv[1])
reference = json.loads(c.REFERENCE.read_text())
assert c.git(data, 'rev-parse', 'HEAD') == reference['revision']
hashes = {name: c.digest(data / name) for name in reference['sha256']}
assert hashes == reference['sha256']
for name, field in [('showdown_aliases.json','aliases_sha256'), ('showdown_learnset_ownership.json','ownership_sha256')]:
    assert c.digest(s.SCRIPT_DIR / name) == reference[field]
assert c.git(ROOT, 'merge-base', 'HEAD', basis) == basis
for path, pin in [(s.CFRU_ROOT, audit.PINS['CFRU']), (audit.UPR, audit.PINS['UPR']), (s.DPE_ROOT, new)]:
    assert c.git(path, 'rev-parse', 'HEAD') == pin
    assert not c.git(path, 'status', '--porcelain', '--untracked-files=no')
    expected = old if path == s.DPE_ROOT else pin
    assert c.git(ROOT, 'rev-parse', basis + ':' + path.relative_to(ROOT).as_posix()) == expected
for pin in [old, candidate]:
    assert c.git(s.DPE_ROOT, 'merge-base', pin, new) == pin
assert c.git(s.DPE_ROOT, 'diff', '--name-only', old, new) == 'src/Evolution Table.c'
assert not c.git(s.DPE_ROOT, 'diff', candidate, new)
old_text = subprocess.check_output(['git','-C',str(s.DPE_ROOT),'show',old + ':src/Evolution Table.c']).decode()
new_text = subprocess.check_output(['git','-C',str(s.DPE_ROOT),'show',new + ':src/Evolution Table.c']).decode()
expected = {'SPECIES_MAGCARGO':(30,38),'SPECIES_TYRANITAR':(48,55),'SPECIES_GLALIE':(30,42),'SPECIES_PURUGLY':(34,38),'SPECIES_SWANNA':(30,35),'SPECIES_VANILLISH':(24,35),'SPECIES_VANILLUXE':(42,47),'SPECIES_KLANG':(35,38),'SPECIES_KLINKLANG':(45,49),'SPECIES_MIENSHAO':(46,50),'SPECIES_BRAVIARY':(50,54),'SPECIES_BRAVIARY_H':(50,54),'SPECIES_MANDIBUZZ':(50,54),'SPECIES_BARBARACLE':(36,39),'SPECIES_DECIDUEYE_H':(34,36)}
a, b = audit.evolution_rows(old_text), audit.evolution_rows(new_text)
assert a.keys() == b.keys()
changes = []
for parent in a:
    assert len(a[parent]) == len(b[parent])
    for index, (before, after) in enumerate(zip(a[parent], b[parent], strict=True)):
        if before != after:
            assert len(before) == len(after) == 4
            assert [i for i in range(4) if before[i] != after[i]] == [1]
            assert before[0] in ('EVO_LEVEL','EVO_LEVEL_HOLD_ITEM')
            assert (int(before[1]), int(after[1])) == expected[before[2]]
            changes.append({'parent':parent,'index':index,'before':before,'after':after})
assert len(changes) == 15 and {x['before'][2] for x in changes} == expected.keys()
# Replacing just the 15 tokens reconstructs the entire target file.
reconstructed = old_text
for change in changes:
    before, after = change['before'], change['after']
    pattern = r'(\{' + before[0] + r',\s*)' + before[1] + r'(?=,\s*' + before[2] + r',)'
    reconstructed, n = re.subn(pattern, lambda m: m[1] + after[1], reconstructed)
    assert n == 1
assert reconstructed == new_text
aliases, _ = s.alias_indexes()
mapped, species = audit.species_audit(s.parse_pokedex(data/'pokedex.ts'), aliases, s.constants_by_kind('species'))
dpe = s.DPE_ROOT
with tempfile.TemporaryDirectory(prefix='619-old-evolution-') as tmp:
    root = Path(tmp); (root/'src').mkdir()
    (root/'src/Evolution Table.c').write_text(old_text)
    s.DPE_ROOT = root
    before = audit.evolution_audit(data, mapped)
s.DPE_ROOT = dpe
after = audit.evolution_audit(data, mapped)
old_rows = {r['source']:r for r in before['rows']}
new_rows = {r['source']:r for r in after['rows']}
assert old_rows.keys() == new_rows.keys() and len(old_rows) == 523
repaired = [key for key in old_rows if old_rows[key]['class'] == 'DATA_MISMATCH']
assert len(repaired) == 15 and after['counts'].get('DATA_MISMATCH',0) == 0
assert all(old_rows[key] == new_rows[key] for key in old_rows if key not in repaired)
assert all(new_rows[key]['class'] in ('REFERENCE_MATCH','ENGINE_TRIGGER_REVIEW') for key in repaired)
for field in ['methods_without_cfru_case','battle_transitions','gnu_obsolete_designators','designator_disposition']:
    assert before[field] == after[field]
assert not re.search(r'^\s*#define\s+EXPAND_LEARNSETS\b', c.uncomment((dpe/'src/defines.h').read_text()), re.M)
assert re.search(r'^\s*#define\s+EXPAND_MOVESETS\b', c.uncomment((s.CFRU_ROOT/'src/config.h').read_text()), re.M)
result = {'basis':basis,'DPE_before':old,'DPE_after':new,'reference_revision':reference['revision'],'reference_hashes':hashes,'policy_hashes':{name:c.digest(s.SCRIPT_DIR/name) for name in ('showdown_pilot_reference.json','showdown_aliases.json','showdown_learnset_ownership.json')},'changes':changes,'before':before,'after':after,'repaired_targets':repaired,'source_hashes':{'old_evolution':hashlib.sha256(old_text.encode()).hexdigest(),'new_evolution':c.digest(dpe/'src/Evolution Table.c'),'helper':c.digest(s.SCRIPT_DIR/'gen9_data_parity_audit.py'),'script':c.digest(Path(__file__))},'ordinary_source_rows':sum(len(v) for v in a.values()),'all_other_reference_records_identical':True,'new_mismatches':0,'genuine_ledger':{'before':67,'removed':15,'after':52,'moves':51,'TM07':1}}
print(json.dumps(result, sort_keys=True, indent=2))
```

## Checks, scope and CONTROL handoff

PASS: Git safety check before changes and handoff; clean starting Workspace; exact basis/ancestry; accepted candidate containment and candidate/merge tree equality; exhaustive DPE component diff and 15-field reconstruction; reference/policy hashes; deterministic full evolution comparison and repeat equality; active learnset ownership; `git diff --check`; status/stat/submodule-log review; exact `git ls-tree` Gitlinks; all other Gitlinks unchanged; exact two-path Workspace allowlist. The old #616 report/helper are unchanged.

**No product build, runtime, emulator or Randomizer execution was performed.** No component source edits, ROM/save/state/build/tool-binary/private-path/secret access, upstream contribution or merge occurred. `UPSTREAM_CONTRIBUTION = DEFERRED`. New-pin runtime behavior and general support remain uncertified; prior runtime evidence is not promoted to this revision.

CONTROL: review the Workspace PR and exact commit/pin evidence. After **user merge**, close #619, keep #498 Phase R1 on hold, and route the next eligible bounded repair contract, expected to be CFRU move-parameter Gen-9 parity. No next Issue/component implementation is opened or executed here. Acceptance/freeze and product-runtime gates remain separate.
