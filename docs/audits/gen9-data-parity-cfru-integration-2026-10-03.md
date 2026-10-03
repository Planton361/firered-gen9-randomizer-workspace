# CFRU integration and move parity re-audit — 2026-10-03

Contract: [Workspace #622](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/622), integrating accepted [CFRU PR #73](https://github.com/Planton361/CFRU-expansion/pull/73) / [Workspace #621](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/621). Branch: `integration/622-cfru-move-parity`; target: `main`; no agent merge.

**Verdict: `CFRU_MOVE_DATA_PARITY_INTEGRATED_WITH_TM07_UNKNOWN`.** All 51 former move-data mismatch records / 67 comparable fields are repaired at the integrated pin: **785 DATA_MATCH / 0 DATA_MISMATCH**. Evolution-level mismatches remain **0**. The genuine comparable/source-structure mismatch ledger is **67 − 15 − 51 = 1**, solely the unresolved TM07 identity contract. Source-data reduction does not certify runtime behavior, full Move/Ability effects or comprehensive Gen-9 mechanics.

Evidence classification: **CONFIRMED USER DECISION** for bounded integration and CONTROL's explained leftover-checkout authorization; **CONFIRMED CURRENT STATE** for exact Git history, source continuity and deterministic re-audit; **UNKNOWN** for TM07 policy and retained mechanics/acquisition/preservation limitations. The accepted [#616 audit](gen9-data-parity-2026-10-03.md), [DPE integration audit](gen9-data-parity-dpe-integration-2026-10-03.md) and historical helper remain unchanged. This additive report supersedes only the old-pin move-data mismatch findings, and reconfirms the integrated evolution result.

## Exact basis and merge proof

| Role | Before | After |
| --- | --- | --- |
| Workspace | `bbd1607cbbc7d25dbcddbb58ecb7afb7b5776aff` | This report's containing integration commit / PR head |
| CFRU Gitlink | `237e1dfaa785af332ddad72af906b3bba5beaab9` | `fe61d5473c015db71f5f4c5a3335a4a67f943254` |
| DPE | `73b3d00859b8d602699775eb41f301901b707b91` | unchanged |
| UPR-FVX | `7bf79ee1e7c46c972f7a9c84942970a950be0723` | unchanged |
| Showdown | `b1156ff19204e48089e2384eb2c9c1a8004f57ce` | unchanged |

The after-Workspace commit is resolved without a self-referential hash by `git log -1 --format=%H -- docs/audits/gen9-data-parity-cfru-integration-2026-10-03.md`; its full SHA is recorded in the PR/delivery. All other Gitlinks are exactly equal to the basis, including nested reference Gitlinks. Older canonical pin paragraphs remain historical relative to this Issue's explicit basis.

The starting Workspace was detached at the exact basis with only CFRU advanced to accepted candidate `ece9b9fc6d349f5d0c3d18285b349bbaa7e2c20f`. Work stopped initially under AGENTS.md. CONTROL explicitly classified that checkout as an explained leftover in #622. After mandatory reading, renewed safety/status checks and exact-basis verification, the bounded branch was created from that basis. Only CFRU was moved directly from candidate to merge; no intermediate candidate Gitlink was staged or committed. Status immediately afterward contained only the expected CFRU delta.

Old pin and accepted candidate are ancestors of merge `fe61d547...`; the candidate's sole parent is the old pin. Candidate and merge share tree `7fbd24158cf3763f4c2bdb1fdc9f55825d5d369f`; candidate → merge file diff is empty. Old pin → merge changes exactly `src/Tables/battle_moves.c`, matching the accepted #621 repair (133 insertions / 45 deletions). No other component source changes are introduced by the merge. No component source was edited in this Workspace task.

## Complete move-domain re-audit

The external temporary comparator imports the unchanged #616 domain functions, checks its own exact current pins/reference/policies, and never calls the historical full-audit entry point with overridden pins. The old table comes from the exact old Git blob. Config and defines are unchanged; current flag ownership is independently checked across tracked C/headers. The accepted fail-closed presence-conditional preprocessor rejects unsupported directives, unmatched branches and duplicate active fields. No compiler/product build is invoked.

All **833 ordinary mapped records** are regenerated against pinned `moves.ts`. The complete inventory contains **935 records**, including generated and mapping-boundary records. Type, category, ordinary power, accuracy, PP, signed priority and the defensible target subset use the same accepted comparison/normalization policy.

| Classification | Old pin | Integrated pin |
| --- | ---: | ---: |
| DATA_MATCH | 734 | **785** |
| DATA_MISMATCH | 51 | **0** |
| ENGINE_BEHAVIOR_UNVERIFIED | 6 | 6 |
| INTENTIONAL_ENGINE_DIFFERENCE | 129 | 129 |
| MAPPING_BLOCK | 14 | 14 |
| MISSING_LOCAL_MOVE | 1 | 1 |
| Total | 935 | 935 |

Every former mismatch identity and field set is independently checked against #616 §13. All 51 become DATA_MATCH. **All 734 formerly matching records and all 884 non-ledger inventory records are exactly equal**, including classification, metadata and differences; no added/removed identity or changed uncompared-local inventory occurs. New move mismatches: **0**.

Exactly 67 direct C field values change on the 51 ledger moves. Every other field/row, all non-row source text, effects, flags, secondary chances and splits remain identical. The complete 51-row disposition follows; each listed field equals its selected reference in the active configuration.

| Move | Direct fields: old → active reference | Disposition | After |
| --- | --- | --- | --- |
| absorb | power: 25 → 20 | SAFE_TABLE_REPAIR | DATA_MATCH |
| alluringvoice | target: MOVE_TARGET_ALL → MOVE_TARGET_SELECTED | SAFE_TABLE_REPAIR | DATA_MATCH |
| barbbarrage | power: 75 → 60; pp: 15 → 10 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| bittermalice | power: 60 → 75; pp: 15 → 10 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| bleakwindstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| ceaselessedge | power: 80 → 65 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| corrosivegas | target: MOVE_TARGET_SELECTED → MOVE_TARGET_ALL | SAFE_TABLE_REPAIR | DATA_MATCH |
| direclaw | power: 60 → 80 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| doodle | pp: 15 → 10 | SAFE_TABLE_REPAIR | DATA_MATCH |
| eeriespell | accuracy: 90 → 100; pp: 15 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| esperwing | accuracy: 90 → 100; power: 75 → 80; priority: 1 → 0 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| expandingforce | pp: 20 → 10 | SAFE_TABLE_REPAIR | DATA_MATCH |
| flowertrick | accuracy: 100 → 0 | SAFE_TABLE_REPAIR | DATA_MATCH |
| glaciallance | power: 130 → 120 | SAFE_TABLE_REPAIR | DATA_MATCH |
| grassyglide | power: 70 → 55 | SAFE_TABLE_REPAIR | DATA_MATCH |
| infernalparade | power: 75 → 60 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| lunarblessing | pp: 10 → 5 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| lusterpurge | power: 70 → 95 | SAFE_TABLE_REPAIR | DATA_MATCH |
| makeitrain | target: MOVE_TARGET_OPPONENTS_FIELD → MOVE_TARGET_BOTH | SAFE_TABLE_REPAIR | DATA_MATCH |
| malignantchain | pp: 20 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| matchagotcha | target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | SAFE_TABLE_REPAIR | DATA_MATCH |
| mightycleave | pp: 10 → 5; priority: 3 → 0 | SAFE_TABLE_REPAIR | DATA_MATCH |
| milkdrink | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| mistball | power: 70 → 95 | SAFE_TABLE_REPAIR | DATA_MATCH |
| mortalspin | target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | SAFE_TABLE_REPAIR | DATA_MATCH |
| mountaingale | power: 110 → 100; pp: 5 → 10 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| psychicnoise | power: 90 → 75 | SAFE_TABLE_REPAIR | DATA_MATCH |
| ragingfury | accuracy: 85 → 100 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| recover | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| rest | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| revivalblessing | pp: 5 → 1 | SAFE_TABLE_REPAIR | DATA_MATCH |
| roost | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| sandsearstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| scaleshot | pp: 25 → 20 | SAFE_TABLE_REPAIR | DATA_MATCH |
| shelter | pp: 20 → 10 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| shoreup | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| slackoff | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| softboiled | pp: 10 → 5 | SAFE_TABLE_REPAIR | DATA_MATCH |
| spicyextract | accuracy: 100 → 0 | SAFE_TABLE_REPAIR | DATA_MATCH |
| springtidestorm | power: 105 → 100; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| steameruption | power: 120 → 110 | SAFE_TABLE_REPAIR | DATA_MATCH |
| stoneaxe | power: 80 → 65 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| supercellslam | accuracy: 100 → 95 | SAFE_TABLE_REPAIR | DATA_MATCH |
| syrupbomb | pp: 15 → 10 | SAFE_TABLE_REPAIR | DATA_MATCH |
| tachyoncutter | type: TYPE_DRAGON → TYPE_STEEL | SAFE_TABLE_REPAIR | DATA_MATCH |
| takeheart | pp: 20 → 15 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| triplearrows | power: 60 → 90; pp: 15 → 10 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| wavecrash | power: 75 → 120; priority: 1 → 0 | CONFIG_PRESERVING_REPAIR | DATA_MATCH |
| wickedblow | power: 80 → 75 | SAFE_TABLE_REPAIR | DATA_MATCH |
| wickedtorque | power: 100 → 80 | SAFE_TABLE_REPAIR | DATA_MATCH |
| wildboltstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH | CONFIG_PRESERVING_REPAIR | DATA_MATCH |

## Macro witnesses, PLA preservation and derived fields

The active state is freshly derived from merged source/config; the active config include chain and config-only macro ownership are checked, not assumed.

| Presence macro | Active |
| --- | --- |
| ACTUAL_PLA_MOVE_POWERS | false |
| BUFFED_LEECH_LIFE | true |
| DARK_VOID_ACC_NERF | true |
| DYNAMAX_FEATURE | true |
| FROSTBITE | true |
| GEN_6_POWER_NERFS | true |
| GEN_7_POWER_NERFS | true |
| UNBOUND | false |

| Preprocessor regression | Integrated value |
| --- | --- |
| Blizzard power | 110 |
| Aura Sphere power | 80 |
| Leech Life power / PP | 80 / 10 |
| Dark Void accuracy | 50 |
| Sucker Punch power | 70 |
| Feint power | 30 |

All six witnesses PASS. All **256 combinations** of the eight table presence macros are preprocessed fail-closed, with equal row/field inventories and no out-of-ledger field changes. Whenever `ACTUAL_PLA_MOVE_POWERS=true` (128 combinations), every one of the **18 configuration-preserving repair rows is completely identical to its old-pin preprocessed row**, including power, accuracy, PP, target, priority, flags, effects and Z fields. These are Dire Claw, Stone Axe, Raging Fury, Wave Crash, Mountain Gale, Barb Barrage, Esper Wing, Bitter Malice, Shelter, Triple Arrows, Infernal Parade, Ceaseless Edge, Bleakwind Storm, Wildbolt Storm, Sandsear Storm, Springtide Storm, Lunar Blessing and Take Heart. The other 33 repairs retain their contracted data changes; the entire alternate table is not claimed byte-identical. Whenever PLA is false, all represented contracted fields equal their selected reference across the other presence-macro states.

**Z/Max derived values remain unchanged and uncertified policy.** Every Z field is equal in active and alternate states. The entire raw `gDynamaxMovePowers` initializer remains byte-identical, as does its preprocessed form whenever DYNAMAX is active. Existing per-move values are retained; no universal ordinary-power conversion formula or new derived-value policy is adopted. The 129 intentional engine differences still include 87 generated records and 42 ordinary dynamic/typeless encodings. Generated moves, six delegated targets, exact targets outside the compared subset, missing Ally Switch and 14 mapping blocks remain in their prior classes.

## Evolution re-audit and residual ledger

DPE remains pinned exactly to the already integrated #6 merge. The complete **523 mapped evolution metadata records** are freshly regenerated using the unchanged #616 species/evolution functions, aliases and pinned `pokedex.ts`. The original pre-DPE table is separately replayed from its exact Git blob through an external temporary directory. The same 15 formerly mismatching records become level-correct REFERENCE_MATCH or ENGINE_TRIGGER_REVIEW; all other 508 records are exactly equal. Missing-handler, battle-transition and GNU-style dispositions remain equal. CFRU `src/evolution.c` is byte-identical across this pin change. No new evolution mismatch occurs.

| Evolution classification | Integrated result |
| --- | ---: |
| DATA_MISMATCH | **0** |
| REFERENCE_MATCH | 472 |
| ENGINE_TRIGGER_REVIEW | 43 |
| MAPPING_BLOCK | 2 |
| PROJECT_POLICY | 5 |
| UNVERIFIABLE_FROM_SELECTED_REFERENCE | 1 |
| Total | 523 |

The exact DPE evolution-file hash is rechecked against #619. The two Hisui held-item routes remain ENGINE_TRIGGER_REVIEW despite their repaired levels; complete triggers/form behavior are not certified. CFRU EXPAND_MOVESETS remains active; DPE EXPAND_LEARNSETS remains disabled.

The genuine ledger is regenerated from fresh move/evolution records plus source-layout issues from all 128 machine files and 152 tutor files. Base-field zero mismatches are carried by exact unchanged source continuity and the accepted prior audit; no new unrelated base/acquisition-domain audit is claimed. The unchanged #616 ledger function verifies unique domain/identity keys.

| Stage | Move records | Evolution-level records | TM07 contract | Total |
| --- | ---: | ---: | ---: | ---: |
| Original #616 | 51 | 15 | 1 | 67 |
| After integrated DPE #6 | 51 | 0 | 1 | 52 |
| After integrated CFRU #73 | **0** | **0** | **1** | **1** |

Complete residual ledger: `machines / slot-7`, DATA_MISMATCH, `7 - Hail.txt`, `MOVE_LOWKICK`, reason `header/order identity differs`. Tutor source-layout issues remain zero.

**TM07 is explicitly UNKNOWN / unresolved.** `gTMHMMoves[6]` remains `MOVE_LOWKICK`; compatibility owner remains `src/tm_compatibility/7 - Hail.txt` with header `TM07: Hail`. The numeric filename supplies membership to slot 7. The complete intended Low Kick TM membership policy remains UNKNOWN. No slot reorder, membership repair or policy invention occurred. This is one identity-contract mismatch, not a complete negative compatibility oracle or a species count.

## Retained classifications and UNKNOWN

Only the move-data findings above are superseded. Exact old → merge single-file isolation, unchanged DPE/UPR pins and unchanged source/config inputs carry the unrelated findings without reclassification:

- Ability behavior: 310 relevant identities; 1 ALIAS_APPROXIMATION, 30 ALIAS_PLUS_HOOK, 7 MISSING_LOCAL, 9 NAME_ONLY_OR_BEHAVIOR_BLOCKED and **263 UNKNOWN** behavior-owner identities; zero independently certified native behavior owners. Missing Commander/Hospitality/Embody Aspect and partial Palafin/Terapagos remain unchanged. Ability assignment/name identity does not certify effects or transferable species-gated hooks.
- UPR preservation: 272 source evolution rows beyond loader method IDs 1..15 risk deletion; one recognized Froslass auxiliary gender condition risks zeroing. Level repairs do not fix those writer/loader gaps. Actual frozen randomized-output manifestation remains UNKNOWN.
- Generated-move exposure remains the prior 156 numeric counterexample IDs; eligibility/settings-dependent species/form and Ability-alias risks remain unchanged. No new UPR policy or runtime manifestation is established.
- Egg, tutor, aggregate machine/acquisition-generation/inheritance policy and negative compatibility uncertainties remain unchanged. No absence-as-prohibition inference or new policy is selected.
- Missing Ally Switch, mapping limitations, full Move/Ability effect semantics, Springtide form effects, Bitter Malice freeze/frostbite behavior, transformation mechanics, omitted evolution triggers and broader support remain uncertified. Matching scalar fields does not certify these mechanics.

## Locked inputs and deterministic replay

Only the four authorized Showdown data files are read; no fifth sim file is acquired/verified and no raw Showdown source is vendored. The historical dex-species hash in the reference lock remains inherited policy evidence.

| Input / evidence | SHA-256 |
| --- | --- |
| abilities.ts | `818edd100c8eb5bdf4d4ded8dd1b1ce9d394f87f40f7d9d53a5414276e84f82b` |
| learnsets.ts | `26969c5e9ca7310b701612da8c9cea217b7d43efb8cd22a7e46783a6ca9b386e` |
| moves.ts | `cd14e386b4c105a30c09dd0866d1378619f493984d68a782472672cefbcfe186` |
| pokedex.ts | `73048386b864be5aff093e9393acf32e8016299e9d7b76078bf5120b769e2fe0` |
| showdown_aliases.json | `10585f6b5863ec847264a02e45adf5da190c2783a8fe58ca5f19ca9ea48414ba` |
| showdown_learnset_ownership.json | `b513f4802874ef81e19b54d61da9e6e67e4398d67a220cfc398652e7c41968d1` |
| showdown_pilot_reference.json | `5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd` |
| Historical #616 helper | `d8882af5629f23f8f0b42b1b79f0686560823f45b3e67ece80bc22ae05e4fb75` |
| Old raw battle_moves.c | `0f9e024e3e40cfa265ffddf663de72e0cabfd7a41e54edf6f9c0e28b56541047` |
| Merged raw battle_moves.c | `d6a8ba9aa8defa395129d8a648484356cb3a9ec45e647d80846a574d897a69cb` |
| Integrated DPE Evolution Table.c | `9b57b40f6eb81083c60a63cce18b662644d639c5422e1163ec4d820b0ae707d6` |
| Temporary comparator | `e454e89377706fc4885c5fae1d12a9eddb39388a93d906cbfd17aaa880e67800` |
| active_source_sha256 | `3a19ff4e0e5356d6482a30a383ae4ec7a15a4decfb74e00d90068b131f7e611e` |
| config_sha256 | `32ec0b81ed8cb872d010ba181962986c9a6beca684a156e64a9cf68251de5f67` |
| defines_sha256 | `96b717303e2fd4594d22c2719535334ca6359a946225450dfd0a2c3b27f43a39` |
| Deterministic JSON | `f45475cb06b1dc003f3fc46557ae26104c3468f1a05b29e77db61c90572bc4e0` |

Python 3.12.14 was used (system python3 is 3.9.6). Two fresh complete comparator processes produce byte-identical JSON. It includes all before/after move and evolution records, direct changes, source layouts, hashes, regressions and residual ledger, without timestamps/private paths. Temporary scripts/JSON remain outside Git.

The unchanged historical 20-test suite was also run: 19 PASS, one fails its explicit old-pin assertion (`237e1df...` versus the authorized `fe61d547...`) before checking move branches. This is an obsolete pin gate for this integration, not a field/preprocessor regression; it is recorded rather than rewritten or monkeypatched. The 19 pin-independent tests pass when run separately, including unsupported-conditional rejection. The temporary comparator independently passes all six current-source branch witnesses at the new exact pin. No new repository helper/tests are added.

Extract the complete Python block below unchanged to `/tmp/622-cfru-reaudit.py`. From this Workspace branch, `SHOWDOWN_DATA_DIR` must point to the four-file data directory inside the exact pinned Showdown checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/622-cfru-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/622-cfru-reaudit.json
PYTHONDONTWRITEBYTECODE=1 python3.12 /tmp/622-cfru-reaudit.py "$SHOWDOWN_DATA_DIR" > /tmp/622-cfru-reaudit-repeat.json
cmp /tmp/622-cfru-reaudit.json /tmp/622-cfru-reaudit-repeat.json
```

The comparator fails on wrong pins, ancestry/tree/source scope, helper/reference/policy drift, dirty component sources, incorrect counts, changed non-ledger records, any out-of-ledger fields, PLA regression, derived-field change, failed witnesses, evolution regression or a different residual source-layout ledger. It does not amend the historical audit's hard-coded pin checks.

```python
import sys,json,re,hashlib,itertools,subprocess
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path.cwd()/'07_scripts/data_audit'))
import gen9_data_parity_audit as a
s,c=a.sync,a.closure
root=Path.cwd();component=s.CFRU_ROOT; data=Path(sys.argv[1])
base='237e1dfaa785af332ddad72af906b3bba5beaab9'
basis='bbd1607cbbc7d25dbcddbb58ecb7afb7b5776aff'
merge='fe61d5473c015db71f5f4c5a3335a4a67f943254'
candidate='ece9b9fc6d349f5d0c3d18285b349bbaa7e2c20f'
assert c.git(root,'branch','--show-current')=='integration/622-cfru-move-parity'
assert c.git(root,'merge-base','HEAD',basis)==basis
assert c.git(component,'rev-parse','HEAD')==merge
for pin in [base,candidate]: assert c.git(component,'merge-base',pin,merge)==pin
assert c.git(component,'rev-parse',candidate+'^{tree}')==c.git(component,'rev-parse',merge+'^{tree}')
assert not c.git(component,'diff',candidate,merge)
assert c.git(component,'diff','--name-only',base,merge)=='src/Tables/battle_moves.c'
assert c.git(component,'rev-parse',candidate+'^')==base
for path,pin in [(component,merge),(s.DPE_ROOT,'73b3d00859b8d602699775eb41f301901b707b91'),(a.UPR,a.PINS['UPR'])]:
    assert c.git(path,'rev-parse','HEAD')==pin
    assert not c.git(path,'status','--porcelain')
    expected=base if path==component else pin
    assert c.git(root,'rev-parse',basis+':'+path.relative_to(root).as_posix())==expected
assert c.digest(s.SCRIPT_DIR/'gen9_data_parity_audit.py')=='d8882af5629f23f8f0b42b1b79f0686560823f45b3e67ece80bc22ae05e4fb75'
assert c.digest(c.REFERENCE)=='5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd'
reference=json.loads(c.REFERENCE.read_text())
assert c.git(data,'rev-parse','HEAD')==reference['revision']
hashes={n:c.digest(data/n) for n in reference['sha256']}
assert hashes==reference['sha256']
for file,field in [('showdown_aliases.json','aliases_sha256'),('showdown_learnset_ownership.json','ownership_sha256')]:
    assert c.digest(s.SCRIPT_DIR/file)==reference[field]
old=subprocess.check_output(['git','-C',str(component),'show',base+':src/Tables/battle_moves.c']).decode()
new=(component/'src/Tables/battle_moves.c').read_text()
# Rebuild before-domain evidence through the existing read-only comparator.
# Only the active table input is supplied from the exact base Git blob;
# current config/flag ownership was independently verified first.
_,config=a.preprocess((component/'src/config.h').read_text())
oldactive,_=a.preprocess(old,config)
_,pp=a.active_move_source()
oldpp=dict(pp,active_source_sha256=hashlib.sha256(oldactive.encode()).hexdigest())
assert oldpp['active_source_sha256']=='0aa98143f5cd06b043428465522da0500a48c07b97495be552428fc378e868e7'
aliases,_=s.alias_indexes()
current_reader=a.active_move_source
a.active_move_source=lambda:(oldactive,oldpp)
try: before=a.move_audit(data,aliases)
finally: a.active_move_source=current_reader
after=a.move_audit(data,aliases)
pla={'direclaw','stoneaxe','ragingfury','wavecrash','mountaingale','barbbarrage','esperwing','bittermalice','shelter','triplearrows','infernalparade','ceaselessedge','bleakwindstorm','wildboltstorm','sandsearstorm','springtidestorm','lunarblessing','takeheart'}
ofields={k:a.c_fields(v) for k,v in a.c_rows(oldactive,'MOVE_').items()}
maxs=dict(re.findall(r'\[(MOVE_\w+)\]\s*=\s*(\d+)',oldactive.split('const u8 gDynamaxMovePowers',1)[1]))
ledger=[]
for row in before['rows']:
    if row['class']=='DATA_MISMATCH':
        row=dict(row)
        row['disposition']='CONFIG_PRESERVING_REPAIR' if row['source'] in pla else 'SAFE_TABLE_REPAIR'
        row['derived_before']={'z':ofields[row['local']].get('z_move_power'),'max':maxs.get(row['local'])} if 'power' in row['differences'] else None
        ledger.append(row)
allowed={r['local']:set(r['differences']) for r in ledger}
assert len(allowed)==51
assert before['counts']=={'DATA_MATCH':734,'DATA_MISMATCH':51,'ENGINE_BEHAVIOR_UNVERIFIED':6,'INTENTIONAL_ENGINE_DIFFERENCE':129,'MAPPING_BLOCK':14,'MISSING_LOCAL_MOVE':1}
accepted=(root/'docs/audits/gen9-data-parity-2026-10-03.md').read_text().split('## 13. Complete genuine data-mismatch ledger',1)[1].split('| Evolution target',1)[0]
expected={}
for key,cell in re.findall(r'^\| (\w+) \| ([^\n]+) \|$',accepted,re.M):
    if ' → ' in cell and ': ' in cell:
        expected[key]={}
        for part in cell.split('; '):
            field,values=part.split(': ');oldvalue,newvalue=values.split(' → ')
            expected[key][field]={'local':oldvalue,'reference':newvalue}
assert expected=={r['source']:r['differences'] for r in ledger}
assert after==a.move_audit(data,aliases)
assert before['normal_mapping_count']==after['normal_mapping_count']==833
oldrows={r['source']:r for r in before['rows']};newrows={r['source']:r for r in after['rows']}
assert oldrows.keys()==newrows.keys()
assert {r['source'] for r in ledger}=={k for k,v in oldrows.items() if v['class']=='DATA_MISMATCH'}
assert after['counts']=={'DATA_MATCH':785,'ENGINE_BEHAVIOR_UNVERIFIED':6,'INTENTIONAL_ENGINE_DIFFERENCE':129,'MAPPING_BLOCK':14,'MISSING_LOCAL_MOVE':1}
for key,row in oldrows.items():
    if row['class']=='DATA_MISMATCH': assert newrows[key]['class']=='DATA_MATCH'
    else: assert row==newrows[key],key
assert before['local_uncompared']==after['local_uncompared']
assert before['preprocessor']['condition_macros']==after['preprocessor']['condition_macros']
for field in ['config_sha256','defines_sha256']:assert before['preprocessor'][field]==after['preprocessor'][field]
_,config=a.preprocess((component/'src/config.h').read_text())
active,_=a.active_move_source()
fields=lambda text:{k:a.c_fields(v) for k,v in a.c_rows(text,'MOVE_').items()}
oldactive,_=a.preprocess(old,config);of,nf=fields(oldactive),fields(active)
changes=[]
for name in of:
    assert of[name].keys()==nf[name].keys()
    for field in of[name]:
        if of[name][field]!=nf[name][field]:
            assert name in allowed and field in allowed[name]
            changes.append({'move':name,'field':field,'before':of[name][field],'after':nf[name][field]})
assert len(changes)==sum(len(x) for x in allowed.values())
for r in ledger:
    for field,values in r['differences'].items():assert nf[r['local']][field].strip()==values['reference']
assert {name for name in of if of[name]!=nf[name]}==set(allowed)
# Source isolation: every other textual row and all non-row text unchanged.
oldraw=a.c_rows(old,'MOVE_');newraw=a.c_rows(new,'MOVE_')
assert oldraw.keys()==newraw.keys()
assert all(oldraw[k]==newraw[k] for k in oldraw.keys()-allowed.keys())
rowpat=r'\[(MOVE_\w+)\]\s*=\s*\{.*?\n[ \t]*\},?'
assert re.sub(rowpat,'ROW',old,flags=re.S)==re.sub(rowpat,'ROW',new,flags=re.S)
assert old.split('const u8 gDynamaxMovePowers',1)[1]==new.split('const u8 gDynamaxMovePowers',1)[1]
for name in of:assert of[name].get('z_move_power')==nf[name].get('z_move_power')
# All 256 presence-macro combinations: fail-closed parser, no new/removed rows,
# no out-of-ledger field difference, complete PLA row identity preservation.
macronames=list(after['preprocessor']['condition_macros'])
configrows={r['local'] for r in ledger if r['disposition']=='CONFIG_PRESERVING_REPAIR'}
for bits in itertools.product([False,True],repeat=len(macronames)):
    macros={k for k,v in zip(macronames,bits,strict=True) if v}
    oa,_=a.preprocess(old,macros);na,_=a.preprocess(new,macros)
    x,y=fields(oa),fields(na);assert x.keys()==y.keys()
    for name in x:
        assert x[name].keys()==y[name].keys()
        for field in x[name]:
            if x[name][field]!=y[name][field]:assert name in allowed and field in allowed[name]
    if 'ACTUAL_PLA_MOVE_POWERS' in macros:
        for name in configrows:assert x[name]==y[name],name
    else:
        for r in ledger:
            if r['local'] in y:
                for field,values in r['differences'].items():assert y[r['local']][field].strip()==values['reference']
    if 'DYNAMAX_FEATURE' in macros:
        assert oa.split('const u8 gDynamaxMovePowers',1)[1]==na.split('const u8 gDynamaxMovePowers',1)[1]
regressions={'MOVE_BLIZZARD':{'power':'110'},'MOVE_AURASPHERE':{'power':'80'},'MOVE_LEECHLIFE':{'power':'80','pp':'10'},'MOVE_DARKVOID':{'accuracy':'50'},'MOVE_SUCKERPUNCH':{'power':'70'},'MOVE_FEINT':{'power':'30'}}
for name,expected in regressions.items():
    for field,value in expected.items():assert nf[name][field].strip()==value
# No syntax beyond authorized scalar replacements/conditional branches was introduced.
maxvalues=dict(re.findall(r'\[(MOVE_\w+)\]\s*=\s*(\d+)',active.split('const u8 gDynamaxMovePowers',1)[1]))
for r in ledger:
    if 'power' in r['differences']:
        assert nf[r['local']]['z_move_power']==r['derived_before']['z']
        assert maxvalues[r['local']]==r['derived_before']['max']
# Working diff before commit, or commit diff after commit, exactly one source file.
assert c.git(component,'diff','--name-only',base)=='src/Tables/battle_moves.c'
assert c.git(component,'diff','--check',base)==''
result={'result':'CFRU_GEN9_MOVE_DATA_PARITY_REPAIRED','workspace_basis':basis,'base':base,'head':c.git(component,'rev-parse','HEAD'),'reference_revision':reference['revision'],'reference_hashes':hashes,'before_counts':before['counts'],'after_counts':after['counts'],'normal_mapping_count':833,'changed_direct_fields':changes,'dispositions':ledger,'preprocessor':after['preprocessor'],'macro_combinations_checked':256,'unchanged_nonledger_records':len(oldrows)-51,'original_matching_rows_preserved':734,'blocks':[],'derived_changes':[],'derived_policy':'Literal per-move table values retained: no deterministic general power-to-Z/Max rule in current CFRU source. Runtime getters use tables directly.','regressions':regressions,'old_source_sha256':hashlib.sha256(old.encode()).hexdigest(),'new_source_sha256':hashlib.sha256(new.encode()).hexdigest(),'verifier_sha256':c.digest(Path(__file__))}
# Fresh complete evolution comparison, using old DPE blob only in /tmp.
import tempfile
mapped,_=a.species_audit(s.parse_pokedex(data/'pokedex.ts'),aliases,s.constants_by_kind('species'))
dpe=s.DPE_ROOT
evolution=a.evolution_audit(data,mapped)
assert evolution['counts']=={'REFERENCE_MATCH':472,'ENGINE_TRIGGER_REVIEW':43,'MAPPING_BLOCK':2,'PROJECT_POLICY':5,'UNVERIFIABLE_FROM_SELECTED_REFERENCE':1}
old_evo=c.git(dpe,'show',a.PINS['DPE']+':src/Evolution Table.c')
with tempfile.TemporaryDirectory(prefix='622-old-evolution-') as tmp:
    temp=Path(tmp);(temp/'src').mkdir();(temp/'src/Evolution Table.c').write_text(old_evo)
    s.DPE_ROOT=temp
    try: old_evolution=a.evolution_audit(data,mapped)
    finally: s.DPE_ROOT=dpe
old_er={r['source']:r for r in old_evolution['rows']};new_er={r['source']:r for r in evolution['rows']}
assert old_er.keys()==new_er.keys() and len(new_er)==523
repaired_evo=[k for k in old_er if old_er[k]['class']=='DATA_MISMATCH']
assert len(repaired_evo)==15
assert all(old_er[k]==new_er[k] for k in old_er if k not in repaired_evo)
assert all(new_er[k]['class'] in ('REFERENCE_MATCH','ENGINE_TRIGGER_REVIEW') for k in repaired_evo)
for key in ['methods_without_cfru_case','battle_transitions','gnu_obsolete_designators','designator_disposition']:
    assert old_evolution[key]==evolution[key]
assert not c.git(component,'diff',base,merge,'--','src/evolution.c')
assert c.digest(dpe/'src/Evolution Table.c')=='9b57b40f6eb81083c60a63cce18b662644d639c5422e1163ec4d820b0ae707d6'
# Recompute actual source-layout issues without choosing any M/T policy.
layouts={}
for domain,name,count,directory in [('machines','gTMHMMoves',128,'tm_compatibility'),('tutors','gMoveTutorMoves',152,'tutor_compatibility')]:
    order,_=a.move_order((dpe/'src/TM_Tutor_Tables.c').read_text(),name,count)
    _,issues,files=a.compatibility_files(dpe/('src/'+directory),count,order,c.constant_values('species','DPE'))
    layouts[domain]={'layout_issues':issues,'order':order,'files':files}
assert layouts['machines']['order'][6]=='MOVE_LOWKICK'
assert layouts['machines']['layout_issues']==[{'slot':7,'file':'7 - Hail.txt','move':'MOVE_LOWKICK','class':'DATA_MISMATCH','reason':'header/order identity differs'}]
assert layouts['tutors']['layout_issues']==[]
assert (dpe/'src/tm_compatibility/7 - Hail.txt').read_text().splitlines()[0]=='TM07: Hail'
# Base-field zero ledger is carried by unchanged exact source; no new base audit claimed.
ledger_result={'moves':after,'evolutions':evolution,'base':{'genuine_mismatches':[]},**layouts}
genuine=a.mismatch_ledger(ledger_result)
assert len(genuine)==1 and genuine[0]['domain']=='machines' and genuine[0]['identity']=='slot-7'
assert not re.search(r'^\s*#define\s+EXPAND_LEARNSETS\b',c.uncomment((dpe/'src/defines.h').read_text()),re.M)
assert re.search(r'^\s*#define\s+EXPAND_MOVESETS\b',c.uncomment((component/'src/config.h').read_text()),re.M)
result.update({'result':'CFRU_MOVE_DATA_PARITY_INTEGRATED_WITH_TM07_UNKNOWN','basis':basis,'candidate':candidate,'merge':merge,'candidate_merge_tree':c.git(component,'rev-parse',merge+'^{tree}'),'before':before,'after':after,'old_evolution':old_evolution,'evolution':evolution,'evolution_repaired_targets':repaired_evo,'layouts':layouts,'genuine_mismatch_ledger':genuine,'ledger_counts':{'old_616':67,'after_DPE':52,'after_CFRU':1},'TM07':'UNKNOWN / unresolved','PLA_preserved_rows':sorted(configrows),'policy_hashes':{n:c.digest(s.SCRIPT_DIR/n) for n in ('showdown_pilot_reference.json','showdown_aliases.json','showdown_learnset_ownership.json')},'helper_sha256':c.digest(s.SCRIPT_DIR/'gen9_data_parity_audit.py'),'evolution_sha256':c.digest(dpe/'src/Evolution Table.c')})
print(json.dumps(result,sort_keys=True,indent=2))
```

## Scope checks and CONTROL handoff

PASS: renewed Git safety/status before the authorized branch/checkout transition; exact basis; old-pin/candidate/merge ancestry and tree/file equality; active macro derivation; full move/evolution comparisons; source-layout ledger; all 256 macro combinations; six witnesses; 18-row PLA preservation; Z/Max preservation; deterministic replay equality; whitespace/status/stat/submodule-log checks; exact staged Gitlinks and all-other-Gitlink equality; exact two-path Workspace allowlist. The two old reports, helper and component tracked sources remain unchanged by this task.

**No product build, Runtime/Emulator/Randomizer run or acceptance occurred.** No ROMs, saves, emulator states, builds, tool binaries, private paths, secrets or .env were accessed. No component-source edits, other Gitlink changes, upstream contribution or merge occurred. `UPSTREAM_CONTRIBUTION = DEFERRED`. Previous runtime evidence is not promoted to the new pin.

CONTROL: review the exact Workspace PR/commit, CFRU Gitlink transition and reproducible evidence. After **user merge**, close #622 and explicitly route the next eligible bounded contract. Keep #498 Phase R1 blocked/on hold; do not resume it automatically because the comparable ledger reaches one. TM07 disposition and Randomizer preservation risks still require explicit routing. Runtime, acceptance/freeze and broader support gates remain separate.
