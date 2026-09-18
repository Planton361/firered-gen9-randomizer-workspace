# Coherent current learnsets — final core-data pass

**HISTORICAL / SUPERSEDED INTEGRATION STATUS (2026-09-19):** This report
records the pre-integration CFRU #48 candidate and its old `827fa1e…` baseline.
CFRU #48 was later merged and is included in the current CFRU pin
`8bc8c38210ddba0b05c933dbda06cb4539254c7a`. The source findings remain valid
supporting evidence; the old “draft/no merge” wording below is historical.
Current runtime evidence is recorded separately in
[Runtime Gate 1](../testing/runtime-gate-1-2026-09-19.md), with tested revision
binding still UNKNOWN.

## Disposition

New draft [CFRU #48](https://github.com/Planton361/CFRU-expansion/pull/48):
**`c483410d44c1b592e8039e631556cadab2352b3a`**, branch
`data/coherent-current-learnsets`, directly based on canonical CFRU
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`.

Old #47 `d6b0e8eb14cc66e7dc75c1738fbe16b99623f843` is **SUPERSEDED**,
not accepted integration evidence. Its branch, commit and checkout are preserved.
#46 remains superseded for modern-data closure; neither #46 nor #47 was used
as this candidate's baseline. No merge, component pin update, DPE modification,
new feature or battle-engine implementation occurred.

NEW reproducible Showdown reference:
**`b1156ff19204e48089e2384eb2c9c1a8004f57ce`**.
The exact historical sync source revision remains **UNKNOWN**.

The corrected candidate replaces 820 existing table bodies, adds two form
tables, rebinds seven existing IDs and fills one existing-ID null pointer.
All other learnset-file bytes and engine/layout/constants/configuration source
remain canonical. Source-only metadata, tests and the narrow M-009 preflight
extension account for the rest of the six-file CFRU change.

## Policy correction and source basis

For each exact species/form, select its literal Gen-9 level-up dataset if
present; otherwise select its newest earlier coherent level-up dataset. Never
select a generation separately for each move. Never pad a current dataset with
older-only moves, event moves, restricted-form moves, pre-evolution moves,
machines or tutors. A selected dataset with no safe L1 path or an unsupported
move fails closed rather than receiving invented fallback moves.

Own older-generation form datasets win over newer base-form datasets. Missing
literal form datasets may follow explicit source `changesFrom` / `battleOnly`
relationships or the missing-literal `forme` / `baseSpecies` rule. The pinned
[learnset inheritance implementation](https://github.com/smogon/pokemon-showdown/blob/b1156ff19204e48089e2384eb2c9c1a8004f57ce/sim/dex-species.ts)
establishes these paths. All explicit possible battle parents must agree in
generation and level/move pairs. No pre-evolution inheritance or new form
transformation logic is implemented.

The [learnset literals](https://github.com/smogon/pokemon-showdown/blob/b1156ff19204e48089e2384eb2c9c1a8004f57ce/data/learnsets.ts)
encode generation and level, not ordering within a level. Retain canonical
relative order of surviving exact level/move pairs and append newly introduced
same-level pairs in source property order. This preserves reviewed initial-move
ordering where possible without retaining an older-only move. It is an explicit
local representation policy, not a claim that Showdown supplies in-game tie order.

The 89 tables in old #47 are materially superseded: only 13 remain exactly
identical to the corrected candidate. Of the other 76, 73 differ in same-level
order; three differ in content: Raichu loses older-only Slam, Sandshrew loses
older-only Magnitude and its old level-23 Sand Tomb entry, and Marshadow loses
older-only Pursuit/Rolling Kick/Jump Kick. Across the whole pilot, 807 existing
tables differ between #47 and #48, plus the two new split tables and bindings.
The earlier union's zero-safe-diff result is not evidence under this policy.

## Fresh inventory

| Class | Canonical source | Corrected candidate | Counting unit |
| --- | ---: | ---: | --- |
| SAFE_DATA_DIFF | 830 | 0 | 822 table plans (820 replacements + 2 new), 8 pointer plans; zero DPE diffs |
| NO_DIFF | 1559 | 2381 | 1293 comparable approved base rows + 266 → 1088 table rows |
| SHARED_TABLE_CONFLICT | 0 | 0 | After the two explicitly approved split plans; no unresolved conflict |
| FORM_MAPPING_BLOCK | 88 | 88 | 87 general source mappings + one local Shadow Warrior table |
| MOVE_BEHAVIOR_BLOCK | 18 | 18 | Table-level unsupported Ally Switch mappings, unchanged |
| ABILITY_BEHAVIOR_BLOCK | 44 | 44 | Blocked ability assignment slots, unchanged |
| NO_L1_PATH | 9 | 0 | Actual non-sentinel targets; planned new tables excluded before creation |
| UNBOUND_POINTER | 1 | 0 | Numeric source pointer holes; repaired ID 1209 |

These are typed rows, not interchangeable Pokemon counts. DPE's 1,293
comparable approved Base Stats rows match; blocked ability slots are excluded
explicitly. DPE receives **NO CODE/DATA CHANGE**. Ability names/assignments retain
the reviewed existing engine semantics and alias policy; missing abilities are
not renamed into existence.

The candidate has 1,107 active tables, including one intentional sentinel, and
1,440 bound pointer slots. All 1,106 non-sentinel tables have a structural usable
L1 path. Fully reconciled source legality covers 1,087 tables; 18 move-blocked
tables and Shadow Warrior retain legacy source and are not current-data certified.
The sentinel has 27 NONE/EGG/reserved consumers, explicitly not encounter species.
No unbound pointer remains anywhere in the current 1,440-slot array.

All 1,412 non-sentinel/non-Shadow-Warrior consumers have a recorded selected
reference generation: Gen9 996, Gen8 317, Gen7 92, Gen6 6, Gen4 1. These include
blocked-move reference selections: recording a generation is not a claim that a
blocked table was imported. Unsupported Shadow Warrior has UNKNOWN generation;
reserved sentinel generations are explicitly NOT_APPLICABLE.

- [Full canonical inventory](coherent-learnsets-baseline-2026-09-15.jsonl)
- [Full final inventory](coherent-learnsets-candidate-2026-09-15.jsonl)
- [Reference and policy lock](../../07_scripts/data_audit/showdown_pilot_reference.json)
- [Explicit learnset-only form ownership/splits](../../07_scripts/data_audit/showdown_learnset_ownership.json)
- [Pinned CFRU manifest](https://github.com/Planton361/CFRU-expansion/blob/c483410d44c1b592e8039e631556cadab2352b3a/docs/coherent-learnsets-provenance.json)
- [Every CFRU consumer's provenance](https://github.com/Planton361/CFRU-expansion/blob/c483410d44c1b592e8039e631556cadab2352b3a/docs/coherent-learnset-consumers.jsonl)

## Eight conflict dispositions

| Family | Source-backed finding | Exact disposition |
| --- | --- | --- |
| Pikachu | **B/E:** base/caps Gen9; exact Cosplay dataset Gen6; costume forms explicitly change from Cosplay | Keep `sPikachuLevelUpLearnset` for Gen9; add `sPikachuCosplayLevelUpLearnset` and rebind COSPLAY/LIBRE/POP_STAR/ROCK_STAR/BELLE/PHD, preserving all IDs |
| Pichu | **B:** exact Spiky-eared dataset is Gen4, unlike base Gen9 | Add `sPichuSpikyLevelUpLearnset`; rebind existing PICHU_SPIKY only |
| Rotom | **E/A:** appliances explicitly change from Rotom; their own restricted `R` entries are not level-up rows | Shared coherent Gen9, 13 rows; no special-form move mechanics added |
| Zygarde | **E:** no Gen9 L dataset; coherent Gen8 exists; 10% changes from base, Complete's possible parents agree | Shared Gen8, 18 rows; Cell/Core retain reviewed pointer ownership but are excluded noncombat placeholders |
| Necrozma | **E/A:** Dusk/Dawn explicit parent paths; Ultra's two parents agree; restricted signature entries are not L rows | Shared Gen9, 16 rows; no fusion/transformation mechanic change |
| Magearna | **A:** normal and Original exact Gen9 datasets are identical | Keep shared Gen9, 17 rows |
| Zacian | **E/A:** Crowned has restricted-only literal entries and an explicit battle parent | Keep shared Gen9, 14 rows; no signature-move substitution implemented |
| Zamazenta | **E/A:** same explicit source relation; exact selected Gen9 differs from older union | Keep shared Gen9, 13 rows |

No unresolved conflict remains. Every split has exact pointer assertions, source
hashes, generation checks, whole-file replay and negative re-sharing tests.

## Low-level gaps and Zarude-Dada

All nine canonical non-sentinel gaps are resolved from selected source start
moves, not fallback inventions. The five empty historical-restoration families
(Pikachu, Rotom, Necrozma, Zacian, Zamazenta) use coherent Gen9 data. Dialga uses
Gen9 with Metal Claw/Scary Face at L1; Origin has explicit source inheritance.
Zygarde uses its Gen8 start rows (including Core Enforcer/Thousand Arrows/
Thousand Waves). Sandshrew's Gen9 start rows are Defense Curl/Scratch; Litleo's
are Leer/Tackle. Their former first levels 27, 5, 50 and 80 were not a reason to
fabricate a move: the selected source already supplies legal early entries.

The exact Cosplay Gen6 and Spiky-eared Gen4 split datasets also have L1 moves:
Tail Whip/Thunder Shock and Charm/Thunder Shock respectively. No selected,
otherwise-unblocked authoritative dataset was found to genuinely lack an early
move. Every non-sentinel path was executed at all low levels, not merely parsed.

Zarude-Dada's own exact Gen9 level-up dataset equals Zarude (17 rows). Pinned
[DPE Learnsets.c](https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Learnsets.c)
already explicitly binds the same existing ID to `sZarudeLevelUpLearnset`.
The CFRU candidate adds that binding and asserts pointer identity plus all-level
execution. This resolves the null-learnset path; it does not certify every other
expanded-form consumer or randomizer profile.

## Remaining supported-profile dispositions

Each of the 87 blocked general source mappings includes its exact reviewed alias
entries and a disposition in the inventory: either **learnset-only reviewed local
ownership** (general Base Stats/ability mapping still blocked), or
**exclude from the supported source-form profile**. The local Shadow Warrior
table stays source-identical and explicitly unsupported/UNKNOWN; no invented
Showdown mapping is supplied.

Enumerated cosmetic/gender/size representations are permitted only by reviewed,
locked existing CFRU/DPE pointer ownership. Distinct source variants must
independently compare equal. Four custom pre-evolution markers have no active
dormant-DPE pointer; that absence is explicitly locked, with CFRU-only shared
ownership and an excluded-custom-form disposition. Surfing/Flying Pikachu and
Zygarde Cell/Core are likewise not certified mainline combat forms. No general
prefix inheritance or new form system was added.

The 18 Ally Switch-blocked tables are Alakazam, Armarouge, Azelf, Ceruledge,
Cresselia, Duosion, Hoopa, Hoopa-Unbound, Iron Leaves, Kadabra, Latios, Mesprit,
Mr. Mime-Galar, Mr. Rime, Orbeetle, Reuniclus, Solosis and Uxie. All shared
consumers are listed. These retain legacy data, not a silently truncated current
dataset. They need an explicit supported-profile exception/exclusion; runtime
smoke cannot make the missing move mapping a PASS. No new exclusion code or
missing move behavior was introduced in this data-only pass.

Similarly, the 44 blocked ability slots are existing semantics limitations, not
new assignments. Source-only data closure does not implement Commander,
Hospitality, Embody Aspect, Terastal or other missing battle behavior. The scoped
safe candidate is reviewable, but unrestricted whole-pilot current-data or
Gen1–9 random-selection certification is **not declared**.

## Reproduce without an unrecorded HEAD

Use isolated component worktrees with the canonical pins and an isolated public
Showdown source checkout at the exact reference above. Only the four `data/*.ts`
files named in the lock plus `sim/dex-species.ts` are reference inputs. The helper
rejects a different commit, file contents, alias/ownership policy, or canonical
component inputs. No protected fixture is needed.

From the workspace root, set `SHOWDOWN_DATA` to that public checkout's `data`
directory; do not point it at an unrecorded external HEAD:

```sh
python3 07_scripts/bootstrap/check_git_safety.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s 07_scripts/data_audit -p 'test_showdown_pinned_closure.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/data_audit/showdown_pokemon_data_sync.py --showdown-data-dir "$SHOWDOWN_DATA" --canonical-baseline --inventory /tmp/coherent-baseline.jsonl
PYTHONDONTWRITEBYTECODE=1 python3 07_scripts/data_audit/showdown_pokemon_data_sync.py --showdown-data-dir "$SHOWDOWN_DATA" --verify-candidate --inventory /tmp/coherent-candidate.jsonl
cmp docs/audits/coherent-learnsets-candidate-2026-09-15.jsonl /tmp/coherent-candidate.jsonl
```

For a new canonical CFRU candidate only, `--write` is allowed on a clean isolated
non-main branch whose HEAD is exactly the canonical pin. It writes CFRU only,
then requires zero remaining safe diffs. Never combine with `--generation`,
`--canonical-baseline` or an alternate input. `--verify-candidate` independently
replays canonical source into disposable text and compares every byte.
`export_coherent_provenance.py --showdown-data-dir "$SHOWDOWN_DATA"` deterministically
exports CFRU source manifests only after that exact replay passes.

## Completed checks and outstanding gates

PASS: 27 hardened synthetic helper tests; exact replay and repeated inventory
byte comparison; ARM syntax with repository flags; exact source ownership and
five negative mutations; actual `GiveBoxMonInitialMoveset` for 144,000 cases
(all 1,440 IDs at levels 1–100) under address/undefined/bounds sanitizers; M-009
source/frame preflight, compiled scanner and eight negative cases; diff checks.
This covers start/low-level and every level boundary in 1–100. Engine source,
IDs, layout, constants and configuration remain canonical.

Full clean/source-link build is **BLOCKED on unavailable native `wav2agb` and
`mid2agb`**, not passed. Source/configuration inspection and executable-name
lookup confirm the already documented environment blocker. No converter was
downloaded, installed, copied or patched around; no existing build, ROM, save,
state, tool binary or secret artifact was inspected. See the CFRU candidate's
`docs/coherent-learnsets-closure.md` for exact user-side PATH preflight and
`python3 scripts/build.py` instructions for a fresh complete source checkout.

| Remaining acceptance | PASS criterion / STOP condition |
| --- | --- |
| Approved full source build | Clean compile/link succeeds at exact candidate; stop on any error before insertion/runtime |
| Fresh starters/encounters L1–5 | Non-sentinel species have usable listed legal moves; stop on empty moves, invalid IDs or crash |
| Eight resolved families + Dialga/Origin, Sandshrew, Litleo, Zarude/Dada | Exact selected-generation moves and pointer/form identity; no unexpected inherited restricted move; stop on mismatch |
| Level boundaries / Move Reminder | At listed levels, expected coherent rows appear; removed older-only entries do not return; no overflow or UI corruption |
| Save/reload and form display sanity | Stable species/moves/name display; stop on corruption, crash or unsupported-form selection |
| Randomized output smoke | Profile exclusions/limitations explicitly enforced or accepted; expanded form and low-level paths safe; no blanket Gen1–9 selection claim from this source audit |
| M-001–M-009 integration | Retain prior behavior, including M-009 field/frame transitions, menus, warps, battle return and sparkles |

Record only sanitized text: exact component SHAs, test ID, level/species/form,
expected/actual move names or IDs, PASS/FAIL/BLOCKED and severity. A crash, null
pointer, invalid move/write, or state corruption is STOP/S1. Do not attach or
request protected ROM/save/state/build artifacts.

## Pins, integration and next action

| Component | Preserved canonical pin |
| --- | --- |
| CFRU | `827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `1a597a667129b50284dd88afb231372b5bd01d7f` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |

Review #48 and this Workspace #493 follow-up; do not integrate #46 or old #47.
Supply the already-approved toolchain locally, complete the source build, then
the sanitized manual acceptance matrix. Resolve/explicitly scope the remaining
profile limitations before calling current learnset data complete. #45 is an
independent canonical-baseline candidate; any later combination must preserve
both preflight guards and receive a fresh integrated build/runtime pass. No
merge is performed or implied by these source results.
