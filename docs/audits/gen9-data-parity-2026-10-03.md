# Gen-9 data parity — comprehensive source audit, 2026-10-03

Contract: [Workspace #616](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/616). Nonblocking side audit; #498 Phase R1 is unchanged. Branch: `audit/616-gen9-data-parity`; target: `main`; never merge.

**Verdict: `DATA_MISMATCH_FOUND`. The pilot is not comprehensively Gen-9-current even within its documented engine boundary.** The accepted base-field and coherent-level-up closure still holds. This wider audit finds 77 move records with comparable field differences, 15 evolution-level differences, one TM order/compatibility identity conflict, and one malformed evolution source designator. Missing/partial mechanics and unselected aggregate acquisition policies remain separate from those data findings. Source evidence does not change or pause acceptance, repair the frozen pilot, or certify runtime behavior.

Evidence: **CONFIRMED CURRENT STATE** for inspected pinned source and deterministic comparisons; **CONFIRMED USER DECISION** for scope and reviewed policies; **UNKNOWN** for the uncertified semantics/policies below; **CONFLICT** for source defects versus any broad claim that all data domains are already current. Historical union-generation learnset policy is **LEGACY / OBSOLETE**.

## 1. Exact revisions and reference hashes

| Role | Revision |
| --- | --- |
| CFRU | `237e1dfaa785af332ddad72af906b3bba5beaab9` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR | `7bf79ee1e7c46c972f7a9c84942970a950be0723` |
| Workspace | `3d464cebf3544dfd3e23127889e88acd8ca517aa` |
| product_source | `1a3e73871730783f7fe2108b335e3d86f69adbe8` |
| smogon/pokemon-showdown | `b1156ff19204e48089e2384eb2c9c1a8004f57ce` |

The Workspace branch descends from the exact requested main commit. Both Workspace basis commits have the same three inspected Gitlinks. Component HEADs and tracked source are clean and match those Gitlinks. The older `docs/REPRODUCIBILITY.md` pin paragraph is historical relative to this task; #616 and the current-pin R0 report supply the exact current basis. No Gitlink is changed.

| Locked input | SHA-256 |
| --- | --- |
| abilities.ts | `818edd100c8eb5bdf4d4ded8dd1b1ce9d394f87f40f7d9d53a5414276e84f82b` |
| learnsets.ts | `26969c5e9ca7310b701612da8c9cea217b7d43efb8cd22a7e46783a6ca9b386e` |
| moves.ts | `cd14e386b4c105a30c09dd0866d1378619f493984d68a782472672cefbcfe186` |
| pokedex.ts | `73048386b864be5aff093e9393acf32e8016299e9d7b76078bf5120b769e2fe0` |
| showdown_aliases.json | `10585f6b5863ec847264a02e45adf5da190c2783a8fe58ca5f19ca9ea48414ba` |
| showdown_learnset_ownership.json | `b513f4802874ef81e19b54d61da9e6e67e4398d67a220cfc398652e7c41968d1` |
| showdown_pilot_reference.json | `5155f67814a4887433f15996299904ad6229ad9311a763c7fe7b5fd1ae36a4bd` |

Only the four Showdown data files were acquired/read from the sparse source checkout. No Showdown data is vendored. The lock also records historical `dex_species_sha256=5f47308e655371968c3b4ddc6680cf0da1c92022c330625ca5cce71e3f0e43ce`; that sim file is intentionally not acquired or re-read under #616’s four-file restriction. Its already-reviewed form inheritance rule is reused through `showdown_coherent_forms.py`; the ownership file and reference lock hashes above are verified. This distinction avoids claiming a fifth reference-file verification.

## 2. Methodology and reproducibility

Read the canonical entry point and all requested existing data evidence/helpers before normalization. The new read-only wrapper composes existing parsers, reviewed aliases, selected-generation form ownership and `build_inventory`. It never calls table-writing functions. Existing CFRU/DPE species/move/Ability constants, DPE base/learnset inputs and CFRU learn-move owners are byte-identical to the historical normalization baseline. The old whole-file `config.h` check rejects later approved QoL changes; the wrapper instead verifies current source pins plus `EXPAND_MOVESETS`, disabled DPE `EXPAND_LEARNSETS`, and unchanged actual normalization/runtime dependencies. It does not modify or override the old helper.

TS literals are read only at top-level property indentation; callback values are not interpreted as data fields. C table rows are parsed without comments, including the final Psychic Noise row without a trailing comma. Signed priority bytes are normalized as `s8` (e.g. 250 → −6); `MOVE_TARGET_ALL` and `MOVE_TARGET_FOES_AND_ALLY` both encode 0x20. Dynamic-power/damage sentinels and typeless Struggle are engine encodings, not raw-field errors. Effect IDs, hook names and displayed strings never prove complete modern effect semantics.

TM/Tutor comparisons retain the local move order. Their evidence oracle uses literal M/T sources, explicit missing-form parents and pre-evolution inheritance, with generations preserved in the external JSON. TM positives in the selected coherent species/form generation are reference matches; older same-method and cross-method positives are project aggregate-policy candidates. Tutors use the best available historical same-method evidence because the local aggregate is not an SV tutor contract. Absence is not treated as a definitive compatibility prohibition. No new species/form alias or acquisition policy is silently approved. Egg evidence is literal E-source union only; no inferred breeding/inheritance policy is invented.

Replay from the Workspace root, with Python ≥3.10 (this session used Python 3.12.14; the system `python3` is 3.9.6 and cannot run the existing strict-zip parser):

```sh
PYTHONDONTWRITEBYTECODE=1 python3.12 07_scripts/data_audit/gen9_data_parity_audit.py --showdown-data-dir "$SHOWDOWN_DATA_DIR" > /tmp/gen9-parity-audit.json
PYTHONDONTWRITEBYTECODE=1 python3.12 07_scripts/data_audit/gen9_data_parity_audit.py --showdown-data-dir "$SHOWDOWN_DATA_DIR" > /tmp/gen9-parity-audit-repeat.json
cmp /tmp/gen9-parity-audit.json /tmp/gen9-parity-audit-repeat.json
PYTHONDONTWRITEBYTECODE=1 python3.12 -m unittest discover -s 07_scripts/data_audit -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 02_external/CFRU-expansion/scripts/check_coherent_learnsets.py
python3 07_scripts/bootstrap/check_git_safety.py
git diff --check
```

Deterministic JSON output SHA-256: `7f8895af4c9ccc6f292b12b298e4117a8af20e3df6ff201ebb30377745f4b949`. Output has no timestamps or absolute/private paths. It contains complete derived domain records, all input hashes and exception sets, stays outside Git, and can be regenerated from the pins. The Markdown tables below retain all genuine mismatches and all exception sets; unchanged raw Showdown records are not committed.

## 3. Species and form coverage

| Unit | Classification counts |
| --- | --- |
| 1,380 pinned NatDex 1–1025 source records | {"EXCLUDED_FORM":87,"INTENTIONAL_ALIAS":125,"MATCH":1168} |
| 1,415 local named constants | {"EXCLUDED_FORM":11,"INTENTIONAL_ALIAS":236,"MATCH":1168} |
| Runtime pointer ID domain | 1,440 slots; 27 NONE/EGG/reserved sentinel bindings |

Source coverage is 1,168 exact identities, 125 intentional aliases, and 87 excluded/blocked source forms; missing mappings and mapping conflicts are zero **within the existing reviewed source policy**, not universal form parity. The pinned reference includes Future Mega forms on existing NatDex numbers; these stay in the excluded source inventory, not the pilot’s represented Gen-9 battle-form claim. Local representation classifies 1,168 matches, 236 intentional aliases/ownership representations, 11 excluded forms, zero unresolved local-only constants. Learnset-only ownership does not waive blocked base/Ability mapping. Complete source/local exceptions are in Appendix A.

Form representation is separate from activation, transformation, reversion and battle safety. Custom Alolan/Galar pre-evolution markers, Surfing/Flying Pikachu and Zygarde Cell/Core are excluded from the supported-form profile. NONE, EGG, reserved slots and Shadow Warrior are not certified encounter forms. Structural pointers alone do not authorize selection.

## 4. Base Stats, types and assignments

Classification: `CURRENT_DATA_MATCH_WITH_DOCUMENTED_ENGINE_LIMITS`. **1,293 comparable local rows; 1,293 matches on approved comparable fields; 18,058 comparable field values; zero genuine mismatches.** All six stats, both normalized type slots, gender ratio and both egg-group slots match. Of 3,879 Ability slots, 3,835 compare under accepted identity policy and 44 are blocked (44 distinct source records). Thirty-eight accepted assignment slots use an older Ability effect alias; they are identity-policy matches, not exact Gen-9 behavior matches. Base import exclusions: 87 source forms. Fully unblocked 14-field rows: 1,249; 44 rows have a blocked Ability slot. Appendix B lists all blocked slots and the 38 accepted alias assignments.

Single-type and single-egg-group sources are duplicated into the second local slot per existing policy; missing second/hidden Ability uses NONE. Numeric older-effect aliases are not newly modernized by this audit. Catch/EXP/EV and other nonreference fields are outside this match count.

## 5. Exact level-up moves and learning levels

Classification: `CURRENT_DATA_MATCH_WITH_DOCUMENTED_ENGINE_LIMITS` for the accepted subset. Active owner is CFRU `src/Tables/level_up_learnsets.c`; DPE `EXPAND_LEARNSETS` remains disabled.

| Unit / result | Count |
| --- | --- |
| Unique active non-sentinel tables | 1106 |
| Exact ordered coherent-reference targets | 1087 |
| Structural-only safe, move-behavior blocked legacy tables | 18 |
| Structural-only safe, form-mapping blocked legacy table | 1 |
| Sentinel target | 1 |
| Pointer slots with NO_DIFF disposition | 1391 |
| Move-blocked pointer consumers | 21 |
| Unresolved-form pointer consumer | 1 |
| Excluded sentinel pointer consumers | 27 |
| Safe data/pointer diffs, shared conflicts, unbound pointers, non-sentinel L1 gaps | 0 each |

Eight of the 1,391 NO_DIFF pointer consumers are explicitly excluded custom/noncombat forms; the other 1,383 match their selected source representation. Selection counts over all pointers with provenance: Gen9 996, Gen8 317, Gen7 92, Gen6 6, Gen4 1; 28 have no selected dataset (27 sentinels + Shadow Warrior). These are pointer counts, not unique species or unique table counts. Blocked tables retain legacy data and cannot be called current-reference matches.

Every approved table agrees on exact ordered `(level, move)` pairs, exact learning levels and exact selected generation/form source. One generation per exact form is chosen: literal Gen9 L sources when present, otherwise the newest coherent earlier literal dataset; reviewed explicit form inheritance applies only when justified. No per-move generation union, pre-evolution/event/R/machine/tutor padding or older-only survivor is accepted. Own older form data takes precedence over newer base data. Showdown does not specify same-level order; the locked canonical surviving-pair order followed by new source-property order is the approved project rule, not a mainline-order oracle.

Level 0 is retained as an evolution/start entry and is eligible at initial level 1 alongside level-1 moves. Engine prefix scanning and duplicate/last-four behavior are covered by the existing actual `GiveBoxMonInitialMoveset` host regression at all levels 1–100 and every ID: **144,000 cases PASS**. This includes low levels and both sides of all in-range learning boundaries. Source bounds remain sorted 0..100, ≤50 rows and valid nonzero u16 move IDs. All 1,440 pointers are bound. This proves the host initial-move contract, not game/runtime/form support. Appendix C lists every blocked target and excluded consumer.

## 6. Move data

Classification: `DATA_MISMATCH_FOUND`. `DATA_MATCH` 708; `DATA_MISMATCH` 77; `ENGINE_BEHAVIOR_UNVERIFIED` 6; `INTENTIONAL_ENGINE_DIFFERENCE` 129; `MAPPING_BLOCK` 14; `MISSING_LOCAL_MOVE` 1.

833 ordinary mapped records are compared. The 935-record classification inventory also includes 87 generated Z/Max/GMax source records (excluded from ordinary acquisition), 13 blocked LGPE partner moves, Ally Switch, and ignored Future Nihil Light. Of 129 intentional engine-difference records, 87 are generated moves and 42 use explicit dynamic-power/typeless encodings. 708 records match all compared literal fields; this does not mean their effects or every target class are Gen-9-correct. Six delegated-target records remain behavior-unverified. Type/category/power/accuracy/PP/priority are checked; only normal, self, all adjacent foes and all adjacent battlers have an exact target mapping. Other target classes remain explicitly uncertified. No move effect is certified by its Effect ID.

Ally Switch has no approved local move mapping and blocks 18 learnset tables / 21 consumers. It is an engine/mapping limitation, not a silently fixed data row. Local project Leech Fang/Steely Hit, split constants, sentinel/helpers and reference typed Hidden Power variants stay outside normal learnset imports. Move name identity follows reviewed constant mapping; 94 full reference display names are not found literally in the local short-name table. The 12-character local ABI/abbreviations are a name-format boundary, not automatically 94 identity mismatches. The complete list is retained in Appendix D; no new name alias is approved.

## 7. Ability assignment, identity/name and behavior

Assignment results are in §4. Behavior/representation classification across **310 Ability identities relevant to the 1,293 mapped source records**: `ALIAS_APPROXIMATION` 1; `ALIAS_PLUS_HOOK` 30; `MISSING_LOCAL` 7; `NAME_ONLY_OR_BEHAVIOR_BLOCKED` 9; `NATIVE_BEHAVIOR_SUPPORTED` 263.

`NATIVE_BEHAVIOR_SUPPORTED` means the existing local Ability constant has native source-handler evidence; it is not a proof of every Gen-9 trigger, nerf, suppression, interaction or random assignment. Complete effect semantics are not certified. `ALIAS_PLUS_HOOK` means an older numeric effect plus species-gated code/name plumbing exists; hooks may be partial, disabled or identity-only, and none are counted as exact Gen-9 behavior. `ALIAS_APPROXIMATION` is Opportunist → Dancer without a matched dedicated hook. The 32 Gen-9 alias defines are all explicitly listed below, including the Tablets of Ruin spelling alias. Protosynthesis aliases Quark Drive, which itself repurposes older Tangling Hair ID 0xAF; it is not an older-generation Ability identity simply because its numeric slot is reused. Accepted alias assignments and blocked slots remain disjoint ledgers.

| Gen-9 named constant | Local aliased effect / ID |
| --- | --- |
| ABILITY_ANGERSHELL | ABILITY_WEAKARMOR |
| ABILITY_ARMORTAIL | ABILITY_DAZZLING |
| ABILITY_BEADSOFRUIN | ABILITY_STALL |
| ABILITY_COSTAR | ABILITY_CURIOUSMEDICINE |
| ABILITY_CUDCHEW | ABILITY_HARVEST |
| ABILITY_EARTHEATER | ABILITY_VOLTABSORB |
| ABILITY_ELECTROMORPHOSIS | ABILITY_COLORCHANGE |
| ABILITY_GOODASGOLD | ABILITY_CLEARBODY |
| ABILITY_GUARDDOG | ABILITY_INNERFOCUS |
| ABILITY_HADRONENGINE | ABILITY_ELECTRICSURGE |
| ABILITY_MINDSEYE | ABILITY_SCRAPPY |
| ABILITY_MYCELIUMMIGHT | ABILITY_MOLDBREAKER |
| ABILITY_OPPORTUNIST | ABILITY_DANCER |
| ABILITY_ORICHALCUMPULSE | ABILITY_DROUGHT |
| ABILITY_POISONPUPPETEER | ABILITY_PLUS |
| ABILITY_PROTOSYNTHESIS | ABILITY_QUARKDRIVE |
| ABILITY_PURIFYINGSALT | ABILITY_IMMUNITY |
| ABILITY_ROCKYPAYLOAD | ABILITY_STEELWORKER |
| ABILITY_SEEDSOWER | ABILITY_GRASSYSURGE |
| ABILITY_SHARPNESS | ABILITY_STRONGJAW |
| ABILITY_SUPERSWEETSYRUP | ABILITY_INTIMIDATE |
| ABILITY_SUPREMEOVERLORD | ABILITY_HUGEPOWER |
| ABILITY_SWORDOFRUIN | ABILITY_STALL |
| ABILITY_TABLETOFRUIN | ABILITY_STALL |
| ABILITY_THERMALEXCHANGE | ABILITY_STEAMENGINE |
| ABILITY_TOXICCHAIN | ABILITY_POISONTOUCH |
| ABILITY_TOXICDEBRIS | ABILITY_POISONPOINT |
| ABILITY_VESSELOFRUIN | ABILITY_STALL |
| ABILITY_WELLBAKEDBODY | ABILITY_STEAMENGINE |
| ABILITY_WINDPOWER | ABILITY_BERSERK |
| ABILITY_WINDRIDER | ABILITY_ANGERPOINT |
| ABILITY_ZEROTOHERO | ABILITY_TORRENT |

Commander, Hospitality and the four Embody Aspect identities have no native local implementation and no approved assignment import. Zero to Hero aliases Torrent: Palafin name/description and activation-message hooks exist, but the inspected owners do not establish the actual exit/re-entry Hero transition; classification is `NAME_ONLY_OR_BEHAVIOR_BLOCKED`, not full support. Terapagos uses Ice Face/form-change plumbing; `SpeciesHasTeraShift` and `SpeciesHasTeraShell` test the undefined `SPECIES_TERAPAGOS_TERA` spelling (the header defines `SPECIES_TERAPAGOS_TERASTAL`), so those utility predicates fall through to FALSE. A separate Ice Face switch-in branch can change base Terapagos to Terastal. Tera Shell’s damage hook does not establish support when its predicate is false; Teraform Zero/Stellar activation and Terastal mechanics remain missing/partial. No implementation is performed.

Chilling Neigh is represented via Moxie and a species name override, not a missing display/effect merely because DPE lacks its own named constant. Lingering Aroma has DPE UNUSED versus CFRU LINGERINGAROMA at 0x4D; As One names, Libero, Full Metal Body and Tablets of Ruin retain reviewed identity/behavior blocks. Name presence is recorded separately from effective assignment and behavior; species-specific name override helpers are not universally transferable random Ability IDs. Appendix E lists every relevant Ability classification, local representation, name evidence and hook.

## 8. Evolutions and form changes

Classification: `DATA_MISMATCH_FOUND` plus `UNVERIFIABLE_FROM_SELECTED_REFERENCE` for incomplete trigger metadata. `DATA_MISMATCH` 15; `ENGINE_TRIGGER_REVIEW` 41; `MAPPING_BLOCK` 2; `PROJECT_POLICY` 5; `REFERENCE_MATCH` 459; `UNVERIFIABLE_FROM_SELECTED_REFERENCE` 1.

623 mapped source evolution metadata records are accounted for. The 459 reference matches compare the supplied relationship/level/item/move/method subset; omitted regional, version, friendship threshold or form probability metadata is not inferred. The 15 level mismatches are complete in §13. There is no remaining definitive missing/wrong target after examining alternate local parent ownership, but two parent mappings are blocked (Basculegion-F and Lycanroc-Dusk), five relationships use alternate local parents, and Vivillon-Fancy has unresolved event/form-versus-ordinary-evolution semantics. The complete remaining 41 trigger/form exception records and all local evolution edges are preserved in Appendix F.

DPE EvolutionMethods extends CFRU’s enum with `EVO_COINS`, `EVO_MAUSHOLD_THREE`, `EVO_MAUSHOLD_FOUR`; CFRU `src/evolution.c` has no corresponding cases. Gimmighoul and Roaming Gimmighoul use EVO_COINS parameter 2999 instead of the reference’s 999 item-coin condition; Tandemaus uses the two Maushold methods. This is an engine/data-contract limitation, not a certified inexpressible trigger made correct by names. DPE also contains `[SPECIES_STANTLER] {{...}}` without `=`. The parser retains that malformed row as evidence and reports the syntax defect; it does not repair it. A future clean DPE source build implication is unresolved under this source-only contract. Earlier CFRU insertion/native-build evidence cannot waive this DPE textual defect or prove that the frozen artifact realizes every evolution row.

Move-use counts/style (Annihilape, Overqwil, Wyrdeer), Let’s Go steps (Pawmot, Rabsca, Brambleghast), leader battles (Kingambit), inverted console (Malamar), regional map/damage gates (Runerigus), full-moon condition (Ursaluna), Tower progression (Urshifu), fog extension (Goodra), Hisui Rock gating, day/night/version shortcuts, and friendship-versus-affection replacements are separately listed mechanics/project substitutions. Brambleghast’s friendship parameter 1000 is ignored by the inspected CFRU friendship handler, which checks friendship ≥220. Palafin’s reference evoLevel 38 alone does not certify Union Circle semantics, which this selected metadata does not encode. Gender/nature/personality and Shedinja special methods with matching levels remain metadata/engine-review entries where this reference cannot prove every omitted form condition. Mega/Gigantamax/Primal/Ultra-style DPE entries are battle transition metadata, not ordinary evolutionary relationships; they are listed separately. No transformation is claimed implemented by an evolution row.

## 9. Egg moves

Classification: `UNVERIFIABLE_FROM_SELECTED_REFERENCE`. `EXACT_LITERAL_E_UNION` 124; `MAPPING_BLOCK` 18; `UNVERIFIABLE_FROM_SELECTED_REFERENCE` 296. Local DPE has 437 species entries; 438 mapped source records have literal E evidence and/or local entries. Of the 420 unblocked observable set comparisons, 124 exactly match the literal historical E-source union and 296 differ or lack an unambiguous literal basis. Eighteen are move-mapping blocked. These 124 set agreements are not 124 certified current-Gen9 breeding contracts. Missing/extra literal entries, source generations and local-entry absence are exhaustively listed in Appendix G; no difference is automatically called genuine data error without a selected egg-generation/inheritance policy.

Showdown E notation supplies acquisition provenance, not a complete project-local inheritance/breeding procedure. Evolution/form inheritance, Mirror Herb and removed historical egg sources cannot be guessed into the intended local set. The source has its terminator; egg markers use the existing 20000 offset / 0xFFFF terminator. UPR’s reader handles that layout; source comparison does not establish actual breeding behavior.

## 10. TM/HM compatibility

Classification: `DATA_MISMATCH_FOUND` for TM07’s identity contract; compatibility policy is partly `UNVERIFIABLE_FROM_SELECTED_REFERENCE`. Exact local order is 128 moves = 120 TMs + 8 HMs, frozen in Appendix H; 16 bytes × 1,440 rows, little-endian bit order, one file per slot, source-only encode/decode replay PASS. No generated assembly/build artifact is opened. `MAPPING_BLOCK` 1,293; `PROJECT_POLICY` 14,133; `REFERENCE_MATCH` 27,841; `UNVERIFIABLE_FROM_SELECTED_REFERENCE` 122,237.

The comparison accounts for all **165,504 mapped source/slot pairs**. There are 27,841 comparable positive selected-generation machine agreements; 14,133 policy candidates (13,777 older same-method positives + 356 cross-method positives); 1,293 mapping blocks (the project Leech Fang slot); 122,237 unverifiable pairs, including absent/absent pairs and acquisition disagreements. Local positives: 47,660; reference same-method positives: 46,673. A true-negative certificate count is zero: an absent method string is not a complete prohibitory oracle for this aggregate contract. A full current-Gen9 binary mismatch count is **UNKNOWN**, not zero. Every positive disagreement and mapping block is listed by exact local species-ID set in Appendix H.

TM07 `gTMHMMoves[6]` is Low Kick, but compatibility file `7 - Hail.txt` is labeled Hail and supplies its species list to that bit position. The filename/header/order conflict is a concrete data-contract mismatch; its exact affected source membership and source-reconstructed bitset are frozen by the helper. It is not a Scarlet/Violet TM-list comparison. Façade’s cedilla is normalized and produces no false identity mismatch. No slot is reordered or repaired.

## 11. Tutor compatibility

Classification: `PROJECT_POLICY_DIFFERENCE` / `UNVERIFIABLE_FROM_SELECTED_REFERENCE`. **152 explicit moves**, 152 compatibility files, **19 bytes per species**, 1,440 rows; one-to-one slot/name order and source encode/decode replay PASS. Stale inline comments had suggested 151; parsing the initializer proves 152, with Confuse Ray at slot 147 and Tera Blast at 152. Zero structural slot/name mismatch. `PROJECT_POLICY` 12,047; `REFERENCE_MATCH` 10,408; `UNVERIFIABLE_FROM_SELECTED_REFERENCE` 174,081.

All **196,536 mapped source/slot pairs** are accounted for. Positive same-method reference agreements: 10,408; cross-method aggregate-policy candidates: 12,047; unverifiable pairs: 174,081; mapping blocks: zero. Local positives: 25,191; same-method reference positives: 11,501. Of the 10,408 same-method positive tutor matches, 783 have evidence in the selected coherent species/form generation and 9,625 rely on earlier tutor evidence; they are not 10,408 literal Gen9 tutor matches. Of the 10,408 same-method positive tutor matches, 783 have evidence in the selected coherent species/form generation and 9,625 rely on earlier tutor evidence; they are not 10,408 literal Gen9 tutor matches. Full binary current-Gen9 compatibility mismatches remain UNKNOWN until a selected project aggregation policy is supplied; no Scarlet/Violet-specific tutor system is imposed. The exact local order, bitset hashes and complete observable disagreements are in Appendix I.

## 12. UPR-FVX source implications

Read-only source review confirms the Gen3 CFRU/DPE profile’s species count 1,440, 992 move slots, three byte-sized Ability slots up to 0xFE, 128/16-byte TM and 152/19-byte tutor contracts, 20000/0xFFFF egg layout and 16 evolution slots × 8-byte rows. Runtime learnset readers/writers use CFRU’s 3-byte entries, bounded 50-row lists, pointer/range validation and bounded allocation; preservation does not modernize their contents. TM/tutor read/write routines retain the numeric order/bit positions and thus can preserve or rewrite the discovered TM07 mismatch. Move writers and ordinary unchanged settings retain move field mismatches; they do not correct them from Showdown.

`Gen3RomHandler.getCfruDpeRandomPoolSpeciesAssetIssues` rejects NONE/EGG/out-of-range/null species, empty usable learnsets and invalid front-sprite/palette pointers. Wild, trainer and loaded-manifest paths apply the asset filter; trainer paths also reject zero-BST/all-NONE-Abilities. However those guards are not a coherent-reference/Ability-mechanics exclusion registry. `getAltFormes`, `getIrregularFormes` and functional-form support are empty/false for Gen3, while represented local forms may be ordinary numeric species. The asset-safe but audit-excluded custom markers/typed Pikachu/Zygarde placeholders, legacy move-blocked consumers, and partial Palafin/Terapagos/Ability hooks can therefore remain candidate risks if their loaded assets and settings permit selection. Exact frozen-artifact eligibility for each is UNKNOWN; this audit neither runs the Randomizer nor alters a profile.

Ability randomization chooses numeric IDs through 0xFE and standard option-dependent bans. It cannot create nonexistent independent Commander/Hospitality/Embody Aspect IDs, but can assign older alias IDs on species that lack the species-gated modern hook, or leave those old effects on their original species. Generic bans and species-name overrides do not guarantee the reviewed unsupported-Ability policy. Pickup randomization remains explicitly rejected for this profile; stale National-Dex-at-start requests remain guarded. Those existing guards do not address this audit’s data/mechanics differences.

**Generated move exposure:** source-level replay finds 156 local generated Z/Max/GMax constants not removed by the standard numeric Z-Move/bannedRandomMoves filters. Example: local Breakneck Blitz-P is 767; UPR `MoveIDs.breakneckBlitzPhysical` is 622. Local Max Strike-P is 821, outside the standard bans. Gen3 inherits empty `getIllegalMoves` / `getMovesBannedFromLevelup`; ordinary moveset selection iterates loaded moves after those filters. All 156 counterexample IDs are in Appendix J. This flags capability conditional on loading/settings, not observed randomized output. No automatic policy change follows.

Evolution preservation has a concrete source-level gap: `Gen3Constants.evolutionMethodCount=15`; `loadEvolutions` ignores later methods, Mega/Gigantamax entries and other unmapped records. `AbstractRomHandler.prepareSaveRom` calls `saveSpeciesStats`, which calls `writeEvolutions` even without an evolution-randomization choice. The writer emits only imported relationships, writes auxiliary u16 fields as zero, and zeroes remaining slots. Thus 272 DPE source rows have methods outside the import domain and are at risk of deletion when present in loaded species; Froslass’s recognized Dawn Stone row loses its nonzero female gate (MON_FEMALE=0xFE → 0). Gallade’s male gate is already zero and is not counted as a lost value. Appendix J lists the exact 272 rows and the one nonzero auxiliary-field case. These are source capability findings, not observed artifact output; frozen table realization and loaded membership remain UNKNOWN. No preservation guarantee is asserted. The exact rows without CFRU cases and the syntax defect are explicitly retained. Starter/static paths are distinct from the wild/trainer asset guard; universal selection exclusion is not inferred.

## 13. Complete genuine data-mismatch ledger

This ledger contains every confirmed comparable-field or source-structure defect found by the pipeline. Differences below are not waived as intentional merely because values resemble an older generation. No reviewed policy supplied by this contract authorizes those altered values. Target-field differences are based only on defensible exact target encodings, not Effect IDs.

| Move | Local → selected reference |
| --- | --- |
| absorb | power: 25 → 20 |
| alluringvoice | target: MOVE_TARGET_ALL → MOVE_TARGET_SELECTED |
| aurasphere | power: 90 → 80 |
| barbbarrage | power: 75 → 60; pp: 15 → 10 |
| bittermalice | power: 60 → 75; pp: 15 → 10 |
| bleakwindstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |
| blizzard | power: 120 → 110 |
| burnup | power: 140 → 130 |
| ceaselessedge | power: 80 → 65 |
| clangingscales | power: 120 → 110 |
| corrosivegas | target: MOVE_TARGET_SELECTED → MOVE_TARGET_ALL |
| darkvoid | accuracy: 80 → 50 |
| direclaw | power: 60 → 80 |
| doodle | pp: 15 → 10 |
| dracometeor | power: 140 → 130 |
| dragonpulse | power: 90 → 85 |
| eeriespell | accuracy: 90 → 100; pp: 15 → 5 |
| esperwing | accuracy: 90 → 100; power: 75 → 80; priority: 1 → 0 |
| expandingforce | pp: 20 → 10 |
| feint | power: 50 → 30 |
| fireblast | power: 120 → 110 |
| flamethrower | power: 95 → 90 |
| fleurcannon | power: 140 → 130 |
| flowertrick | accuracy: 100 → 0 |
| glaciallance | power: 130 → 120 |
| grassyglide | power: 70 → 55 |
| heatwave | power: 100 → 95 |
| hurricane | power: 120 → 110 |
| hydropump | power: 120 → 110 |
| icebeam | power: 95 → 90 |
| infernalparade | power: 75 → 60 |
| leafstorm | power: 140 → 130 |
| leechlife | power: 20 → 80; pp: 15 → 10 |
| lunarblessing | pp: 10 → 5 |
| lusterpurge | power: 70 → 95 |
| magmastorm | power: 120 → 100 |
| makeitrain | target: MOVE_TARGET_OPPONENTS_FIELD → MOVE_TARGET_BOTH |
| malignantchain | pp: 20 → 5 |
| matchagotcha | target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |
| meteormash | power: 100 → 90 |
| mightycleave | pp: 10 → 5; priority: 3 → 0 |
| milkdrink | pp: 10 → 5 |
| mistball | power: 70 → 95 |
| mortalspin | target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |
| mountaingale | power: 110 → 100; pp: 5 → 10 |
| muddywater | power: 95 → 90 |
| originpulse | power: 120 → 110 |
| overheat | power: 140 → 130 |
| psychicnoise | power: 90 → 75 |
| ragingfury | accuracy: 85 → 100 |
| recover | pp: 10 → 5 |
| rest | pp: 10 → 5 |
| revivalblessing | pp: 5 → 1 |
| roost | pp: 10 → 5 |
| sandsearstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |
| scaleshot | pp: 25 → 20 |
| shelter | pp: 20 → 10 |
| shoreup | pp: 10 → 5 |
| slackoff | pp: 10 → 5 |
| softboiled | pp: 10 → 5 |
| spicyextract | accuracy: 100 → 0 |
| springtidestorm | power: 105 → 100; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |
| steameruption | power: 120 → 110 |
| stoneaxe | power: 80 → 65 |
| suckerpunch | power: 80 → 70 |
| supercellslam | accuracy: 100 → 95 |
| surf | power: 95 → 90 |
| syrupbomb | pp: 15 → 10 |
| tachyoncutter | type: TYPE_DRAGON → TYPE_STEEL |
| takeheart | pp: 20 → 15 |
| thunder | power: 120 → 110 |
| thunderbolt | power: 95 → 90 |
| triplearrows | power: 60 → 90; pp: 15 → 10 |
| wavecrash | power: 75 → 120; priority: 1 → 0 |
| wickedblow | power: 80 → 75 |
| wickedtorque | power: 100 → 80 |
| wildboltstorm | power: 105 → 100; pp: 5 → 10; target: MOVE_TARGET_SELECTED → MOVE_TARGET_BOTH |

| Evolution target | Local level → reference level | Local method |
| --- | --- | --- |
| barbaracle | 36 → 39 | EVO_LEVEL |
| braviary | 50 → 54 | EVO_LEVEL |
| braviaryhisui | 50 → 54 | EVO_LEVEL_HOLD_ITEM |
| decidueyehisui | 34 → 36 | EVO_LEVEL_HOLD_ITEM |
| glalie | 30 → 42 | EVO_LEVEL |
| klang | 35 → 38 | EVO_LEVEL |
| klinklang | 45 → 49 | EVO_LEVEL |
| magcargo | 30 → 38 | EVO_LEVEL |
| mandibuzz | 50 → 54 | EVO_LEVEL |
| mienshao | 46 → 50 | EVO_LEVEL |
| purugly | 34 → 38 | EVO_LEVEL |
| swanna | 30 → 35 | EVO_LEVEL |
| tyranitar | 48 → 55 | EVO_LEVEL |
| vanillish | 24 → 35 | EVO_LEVEL |
| vanilluxe | 42 → 47 | EVO_LEVEL |

| Other defect | Evidence / consequence |
| --- | --- |
| TM07 identity conflict | Low Kick move slot; Hail-labeled compatibility file at the same bit index. |
| DPE Stantler malformed designator | Missing = before {{EVO_MOVE, MOVE_PSYSHIELDBASH, SPECIES_WYRDEER, 0}}. Source defect; frozen-artifact manifestation UNKNOWN. |

Total: **94 affected records/contracts** = 77 move records + 15 evolution-level records + TM07 + Stantler source syntax. This is not 94 species and not an exhaustive effect-semantics error count. No genuine base-field or accepted coherent-learnset mismatch was found. Egg/compatibility disagreements and unsupported triggers are separately classified, not hidden in this total.

## 14. Complete engine/mechanics-limit ledger

All limits established or left unverified by this audit are retained in the appendices: every blocked Ability slot (B), move-behavior/form target (C), generated/delegated/unsupported move identity (D), older Ability alias/native-handler-only identity (E), trigger/form transition and missing CFRU method (F), inheritance/source limitations (G–I), and UPR selection/writer exposures (J). The domain boundaries are: unsupported Commander/Hospitality/Embody Aspect; partial Palafin and Terapagos; all 32 Gen9 alias defines / reused numeric Ability slots; no universal transfer of species-gated hooks; missing Ally Switch and LGPE partner moves; generated moves not normal acquisition; no complete Move/Ability effects or transformations proof; incomplete evolution methods/conditions; source-only initial-move proof; reference-incomplete breeding and aggregate compatibility; asset checks that do not enforce mechanics policy. No alias is exact Gen9 mechanics parity.

## 15. Complete project-policy-difference ledger

Established policy: coherent newest-one-generation L selection with explicit older-form priority; locked surviving same-level local tie order; duplicate second type/egg-group representation and NONE Ability slots; enumerated species/form aliases and learnset-only ownership; eight explicit custom/noncombat excluded consumers; local Leech Fang/Steely Hit; generated split move representation; dynamic power and Struggle encodings; 120+8 local machines and 152 aggregate tutors. Full mappings, engine encodings and orders are in A–I.

Observable substitutions needing policy disposition: five alternative evolution parents; Hisui Rock routes; day/night/version and regional substitutes; movement/battle-counter/story-trigger shortcuts; fog and friendship/affection extensions; alternative trade/item and battle transition routes (all local edges in F); 13,777 older machine positives, 13,777 older machine positives, 356 machine and 12,047 tutor cross-method positive pairs (H/I); historical E unions and all acquisition disagreements (G–I). `PROJECT_POLICY` identifies a project-local observable representation, **not proof that CONTROL reviewed every individual deviation**. Their intentional approval is UNKNOWN where no existing rule covers the row. No repair or new policy is adopted.

## 16. NOT CERTIFIED BY SELECTED REFERENCE

Catch rate; Base EXP yield; EV yield; growth rate; egg cycles; base friendship; held-item rates; body color; encounter availability; complete Move effects; complete Ability effects; transformation/battle-form mechanics. Also uncertified: same-level mainline order, omitted evolution trigger thresholds/version/form probabilities, complete breeding inheritance, and the project’s negative TM/tutor aggregation policy. The reference may expose incidental values in some records; this pipeline does not promote them into an approved automatic comparison contract.

## 17. Proposed follow-up Issues — no implementation

| Proposed bounded contract | Evidence to resolve |
| --- | --- |
| Move parameter parity decision/repair | Review the complete 77-record field ledger, selected-generation parameter policy and target mappings; preserve mechanics exclusions. |
| Evolution data and source-owner repair | Review 15 wrong levels and malformed Stantler source; reconcile DPE/CFRU enum/handler boundary, alternate parents and frozen-artifact lineage. |
| TM07 identity and compatibility policy | Choose intended Low Kick/Hail identity; review exact compatibility memberships; define a reproducible aggregate machine oracle. |
| Egg/Tutor aggregate reference policy | Select generation/form/inheritance/transfer rules; then recalculate the complete exception sets without treating absence as prohibition. |
| UPR mechanics/generation exclusion contract | Audit generated numeric move pools, species-only aliases, supported-form exclusions, and each selection/writer path; preserve current #498 work until CONTROL explicitly authorizes changes. |
| Post-pilot mechanics validation, only if requested | Full Gen9 effect/transform behavior remains outside the pilot; no implementation Issue is automatically opened. |

These are proposals only; no Issue is created, no component change is made, and #498’s state/scope is not edited.

## 18. Verification, UNKNOWN / CONFLICT and final verdict

Exact Workspace basis/Gitlinks/component HEADs and clean tracked component sources PASS; exact Showdown commit and four source SHA-256s PASS; alias/reference/ownership locks PASS; core dependency continuity and runtime learnset owner checks PASS. Existing 27 synthetic coherent regressions PASS. New focused tests: 13 PASS; combined existing/new helper suite: 40 PASS (including TS property scope, Unicode identity, array overflow/implicit slot handling, missing/order-invalid files, bounds, inheritance separation/cycles, malformed evolution evidence, and pin rejection). Existing source ownership/negative mutations and 144,000 host initial-move cases PASS. Two full audit outputs compare byte-identical. No raw Showdown files are staged. Changed-file allowlist, no Gitlink/component diff, diff whitespace check, safety, and post-commit clean status are verified for the PR handoff.

UNKNOWN: full native Move/Ability behavior and runtime consequences; frozen-artifact realization of Stantler/modern evolution methods; unsupported-form asset eligibility and every Randomizer setting/path; intended egg/M/T aggregation and deliberate approval of each acquisition/evolution substitution; omitted reference evolution conditions. CONFLICT: an unqualified comprehensive Gen9-current claim is contradicted by the 94-record defect ledger. No change to the earlier bounded core-data closure or #498 acceptance disposition is inferred. No unreviewed product conflict is silently resolved.

**Final answer:** the accepted Base Stats/types/gender/egg-group/assignment subset and coherent learnsets are current against the selected reference within their reviewed exclusions. The pilot’s Pokémon data as a whole is **not comprehensively Gen9-current within the CFRU/DPE boundary**: comparable move/evolution data and the TM07 contract differ, while Ability mechanics and acquisition policies are only partially represented/certifiable. `GEN9_DATA_PARITY_AUDIT_READY` denotes a reviewable completed source audit, not product parity or runtime acceptance.

No implementation, component/config/Gitlink write, game runtime, Randomizer execution, emulator, ROM/save/state/product-build/tool-binary/private-artifact or secret access; no upstream PR; no merge. `UPSTREAM_CONTRIBUTION = DEFERRED`. Only the authorized report, read-only helper and focused tests are changed.

## Appendix A — complete representation exceptions

| Source form | Class | Local identity / blocker |
| --- | --- | --- |
| absolmegaz | EXCLUDED_FORM | species-ignore |
| alcremie | EXCLUDED_FORM | species-open-risk |
| alcremiegmax | INTENTIONAL_ALIAS | alcremiegiga |
| appletungmax | INTENTIONAL_ALIAS | appletungiga |
| araquanidtotem | EXCLUDED_FORM | species-ignore |
| arcaninehisui | INTENTIONAL_ALIAS | arcanineh |
| arceusfighting | INTENTIONAL_ALIAS | arceusfight |
| articunogalar | INTENTIONAL_ALIAS | articunog |
| avalugghisui | INTENTIONAL_ALIAS | avaluggh |
| barbaraclemega | EXCLUDED_FORM | species-ignore |
| basculegion | EXCLUDED_FORM | species-open-risk |
| basculin | EXCLUDED_FORM | species-open-risk |
| basculinbluestriped | EXCLUDED_FORM | species-open-risk |
| basculinwhitestriped | EXCLUDED_FORM | species-open-risk |
| baxcaliburmega | EXCLUDED_FORM | species-ignore |
| blastoisegmax | INTENTIONAL_ALIAS | blastoisegiga |
| braviaryhisui | INTENTIONAL_ALIAS | braviaryh |
| butterfreegmax | INTENTIONAL_ALIAS | butterfreegiga |
| calyrexice | INTENTIONAL_ALIAS | calyrexicerider |
| calyrexshadow | INTENTIONAL_ALIAS | calyrexshadowrider |
| castformrainy | EXCLUDED_FORM | species-ignore |
| castformsnowy | EXCLUDED_FORM | species-ignore |
| castformsunny | EXCLUDED_FORM | species-ignore |
| centiskorchgmax | INTENTIONAL_ALIAS | centiskorchgiga |
| chandeluremega | EXCLUDED_FORM | species-ignore |
| charizardgmax | INTENTIONAL_ALIAS | charizardgiga |
| cherrimsunshine | INTENTIONAL_ALIAS | cherrimsun |
| chesnaughtmega | EXCLUDED_FORM | species-ignore |
| chimechomega | EXCLUDED_FORM | species-ignore |
| cinderacegmax | INTENTIONAL_ALIAS | cinderacegiga |
| clefablemega | EXCLUDED_FORM | species-ignore |
| coalossalgmax | INTENTIONAL_ALIAS | coalossalgiga |
| copperajahgmax | INTENTIONAL_ALIAS | copperajahgiga |
| corsolagalar | INTENTIONAL_ALIAS | corsolag |
| corviknightgmax | INTENTIONAL_ALIAS | corviknightgiga |
| crabominablemega | EXCLUDED_FORM | species-ignore |
| darkraimega | EXCLUDED_FORM | species-ignore |
| darmanitangalar | INTENTIONAL_ALIAS | darmanitang |
| darmanitangalarzen | INTENTIONAL_ALIAS | darmanitangzen |
| darumakagalar | INTENTIONAL_ALIAS | darumakag |
| decidueyehisui | INTENTIONAL_ALIAS | decidueyeh |
| delphoxmega | EXCLUDED_FORM | species-ignore |
| diglettalola | INTENTIONAL_ALIAS | digletta |
| dragalgemega | EXCLUDED_FORM | species-ignore |
| dragonitemega | EXCLUDED_FORM | species-ignore |
| drampamega | EXCLUDED_FORM | species-ignore |
| drednawgmax | INTENTIONAL_ALIAS | drednawgiga |
| dudunsparcethreesegment | INTENTIONAL_ALIAS | dudunsparcethree |
| dugtrioalola | INTENTIONAL_ALIAS | dugtrioa |
| duraludongmax | INTENTIONAL_ALIAS | duraludongiga |
| eelektrossmega | EXCLUDED_FORM | species-ignore |
| eeveegmax | INTENTIONAL_ALIAS | eeveegiga |
| eeveestarter | EXCLUDED_FORM | species-ignore |
| electrodehisui | INTENTIONAL_ALIAS | electrodeh |
| emboarmega | EXCLUDED_FORM | species-ignore |
| excadrillmega | EXCLUDED_FORM | species-ignore |
| exeggutoralola | INTENTIONAL_ALIAS | exeggutora |
| falinksmega | EXCLUDED_FORM | species-ignore |
| farfetchdgalar | INTENTIONAL_ALIAS | farfetchdg |
| feraligatrmega | EXCLUDED_FORM | species-ignore |
| flapplegmax | INTENTIONAL_ALIAS | flapplegiga |
| floettemega | EXCLUDED_FORM | species-ignore |
| froslassmega | EXCLUDED_FORM | species-ignore |
| garbodorgmax | INTENTIONAL_ALIAS | garbodorgiga |
| garchompmegaz | EXCLUDED_FORM | species-ignore |
| gengargmax | INTENTIONAL_ALIAS | gengargiga |
| geodudealola | INTENTIONAL_ALIAS | geodudea |
| glimmoramega | EXCLUDED_FORM | species-ignore |
| golemalola | INTENTIONAL_ALIAS | golema |
| golisopodmega | EXCLUDED_FORM | species-ignore |
| golurkmega | EXCLUDED_FORM | species-ignore |
| goodrahisui | INTENTIONAL_ALIAS | goodrah |
| gourgeistlarge | EXCLUDED_FORM | species-open-risk |
| gourgeistsmall | EXCLUDED_FORM | species-open-risk |
| gourgeistsuper | EXCLUDED_FORM | species-open-risk |
| graveleralola | INTENTIONAL_ALIAS | gravelera |
| greninjaash | INTENTIONAL_ALIAS | ashgreninja |
| greninjabond | EXCLUDED_FORM | species-open-risk |
| greninjamega | EXCLUDED_FORM | species-ignore |
| grimeralola | INTENTIONAL_ALIAS | grimera |
| grimmsnarlgmax | INTENTIONAL_ALIAS | grimmsnarlgiga |
| growlithehisui | INTENTIONAL_ALIAS | growlitheh |
| gumshoostotem | EXCLUDED_FORM | species-ignore |
| hatterenegmax | INTENTIONAL_ALIAS | hatterenegiga |
| hawluchamega | EXCLUDED_FORM | species-ignore |
| heatranmega | EXCLUDED_FORM | species-ignore |
| indeedeef | INTENTIONAL_ALIAS | indeedeefemale |
| inteleongmax | INTENTIONAL_ALIAS | inteleongiga |
| kinglergmax | INTENTIONAL_ALIAS | kinglergiga |
| kommoototem | EXCLUDED_FORM | species-ignore |
| laprasgmax | INTENTIONAL_ALIAS | laprasgiga |
| lilliganthisui | INTENTIONAL_ALIAS | lilliganth |
| linoonegalar | INTENTIONAL_ALIAS | linooneg |
| lucariomegaz | EXCLUDED_FORM | species-ignore |
| lurantistotem | EXCLUDED_FORM | species-ignore |
| lycanrocmidnight | INTENTIONAL_ALIAS | lycanrocn |
| machampgmax | INTENTIONAL_ALIAS | machampgiga |
| magearnamega | EXCLUDED_FORM | species-ignore |
| magearnaoriginal | INTENTIONAL_ALIAS | magearnap |
| magearnaoriginalmega | EXCLUDED_FORM | species-ignore |
| malamarmega | EXCLUDED_FORM | species-ignore |
| marowakalola | INTENTIONAL_ALIAS | marowaka |
| marowakalolatotem | EXCLUDED_FORM | species-ignore |
| meganiummega | EXCLUDED_FORM | species-ignore |
| melmetalgmax | INTENTIONAL_ALIAS | melmetalgiga |
| meowsticf | INTENTIONAL_ALIAS | meowsticfemale |
| meowsticfmega | EXCLUDED_FORM | species-ignore |
| meowsticmmega | EXCLUDED_FORM | species-ignore |
| meowthalola | INTENTIONAL_ALIAS | meowtha |
| meowthgalar | INTENTIONAL_ALIAS | meowthg |
| meowthgmax | INTENTIONAL_ALIAS | meowthgiga |
| mimikyubustedtotem | EXCLUDED_FORM | species-ignore |
| mimikyutotem | EXCLUDED_FORM | species-ignore |
| minior | INTENTIONAL_ALIAS | miniorred |
| miniormeteor | INTENTIONAL_ALIAS | miniorshield |
| moltresgalar | INTENTIONAL_ALIAS | moltresg |
| mrmimegalar | INTENTIONAL_ALIAS | mrmimeg |
| mukalola | INTENTIONAL_ALIAS | muka |
| ninetalesalola | INTENTIONAL_ALIAS | ninetalesa |
| ogerponcornerstone | EXCLUDED_FORM | species-open-risk |
| ogerponcornerstonetera | INTENTIONAL_ALIAS | ogerponcornerstoneterastal |
| ogerponhearthflame | EXCLUDED_FORM | species-open-risk |
| ogerponhearthflametera | INTENTIONAL_ALIAS | ogerponhearthflameterastal |
| ogerpontealtera | INTENTIONAL_ALIAS | ogerponterastal |
| ogerponwellspring | EXCLUDED_FORM | species-open-risk |
| ogerponwellspringtera | INTENTIONAL_ALIAS | ogerponwellspringterastal |
| oinkolognef | INTENTIONAL_ALIAS | oinkolognefemale |
| orbeetlegmax | INTENTIONAL_ALIAS | orbeetlegiga |
| oricoriopau | INTENTIONAL_ALIAS | oricoriop |
| oricoriopompom | INTENTIONAL_ALIAS | oricorioy |
| oricoriosensu | INTENTIONAL_ALIAS | oricorios |
| persianalola | INTENTIONAL_ALIAS | persiana |
| pichuspikyeared | INTENTIONAL_ALIAS | pichuspiky |
| pikachualola | INTENTIONAL_ALIAS | pikachucapalola |
| pikachugmax | INTENTIONAL_ALIAS | pikachugiga |
| pikachuhoenn | INTENTIONAL_ALIAS | pikachucaphoenn |
| pikachukalos | INTENTIONAL_ALIAS | pikachucapkalos |
| pikachuoriginal | INTENTIONAL_ALIAS | pikachucaporiginal |
| pikachupartner | INTENTIONAL_ALIAS | pikachucappartner |
| pikachusinnoh | INTENTIONAL_ALIAS | pikachucapsinnoh |
| pikachustarter | EXCLUDED_FORM | species-ignore |
| pikachuunova | INTENTIONAL_ALIAS | pikachucapunova |
| pikachuworld | EXCLUDED_FORM | species-ignore |
| polteageistantique | EXCLUDED_FORM | species-open-risk |
| ponytagalar | INTENTIONAL_ALIAS | ponytag |
| pumpkaboolarge | EXCLUDED_FORM | species-open-risk |
| pumpkaboosmall | EXCLUDED_FORM | species-open-risk |
| pumpkaboosuper | EXCLUDED_FORM | species-open-risk |
| pyroarmega | EXCLUDED_FORM | species-ignore |
| qwilfishhisui | INTENTIONAL_ALIAS | qwilfishh |
| raichualola | INTENTIONAL_ALIAS | raichua |
| raichumegax | EXCLUDED_FORM | species-ignore |
| raichumegay | EXCLUDED_FORM | species-ignore |
| rapidashgalar | INTENTIONAL_ALIAS | rapidashg |
| raticatealola | INTENTIONAL_ALIAS | raticatea |
| raticatealolatotem | EXCLUDED_FORM | species-ignore |
| rattataalola | INTENTIONAL_ALIAS | rattataa |
| ribombeetotem | EXCLUDED_FORM | species-ignore |
| rillaboomgmax | INTENTIONAL_ALIAS | rillaboomgiga |
| rockruffdusk | EXCLUDED_FORM | species-open-risk |
| salazzletotem | EXCLUDED_FORM | species-ignore |
| samurotthisui | INTENTIONAL_ALIAS | samurotth |
| sandacondagmax | INTENTIONAL_ALIAS | sandacondagiga |
| sandshrewalola | INTENTIONAL_ALIAS | sandshrewa |
| sandslashalola | INTENTIONAL_ALIAS | sandslasha |
| scolipedemega | EXCLUDED_FORM | species-ignore |
| scovillainmega | EXCLUDED_FORM | species-ignore |
| scraftymega | EXCLUDED_FORM | species-ignore |
| silvallyfighting | INTENTIONAL_ALIAS | silvallyfight |
| sinisteaantique | EXCLUDED_FORM | species-open-risk |
| skarmorymega | EXCLUDED_FORM | species-ignore |
| sliggoohisui | INTENTIONAL_ALIAS | sliggooh |
| slowbrogalar | INTENTIONAL_ALIAS | slowbrog |
| slowkinggalar | INTENTIONAL_ALIAS | slowkingg |
| slowpokegalar | INTENTIONAL_ALIAS | slowpokeg |
| sneaselhisui | INTENTIONAL_ALIAS | sneaselh |
| snorlaxgmax | INTENTIONAL_ALIAS | snorlaxgiga |
| staraptormega | EXCLUDED_FORM | species-ignore |
| starmiemega | EXCLUDED_FORM | species-ignore |
| stunfiskgalar | INTENTIONAL_ALIAS | stunfiskg |
| tatsugiricurlymega | EXCLUDED_FORM | species-ignore |
| tatsugiridroopy | EXCLUDED_FORM | species-open-risk |
| tatsugiridroopymega | EXCLUDED_FORM | species-ignore |
| tatsugiristretchy | EXCLUDED_FORM | species-open-risk |
| tatsugiristretchymega | EXCLUDED_FORM | species-ignore |
| taurospaldeaaqua | INTENTIONAL_ALIAS | taurosaquap |
| taurospaldeablaze | INTENTIONAL_ALIAS | taurosblazep |
| taurospaldeacombat | INTENTIONAL_ALIAS | taurosp |
| togedemarutotem | EXCLUDED_FORM | species-ignore |
| toxtricitygmax | INTENTIONAL_ALIAS | toxtricitygiga |
| toxtricitylowkeygmax | INTENTIONAL_ALIAS | toxtricitylowkeygiga |
| typhlosionhisui | INTENTIONAL_ALIAS | typhlosionh |
| urshifu | INTENTIONAL_ALIAS | urshifusingle |
| urshifugmax | INTENTIONAL_ALIAS | urshifusinglegiga |
| urshifurapidstrike | INTENTIONAL_ALIAS | urshifurapid |
| urshifurapidstrikegmax | INTENTIONAL_ALIAS | urshifurapidgiga |
| venusaurgmax | INTENTIONAL_ALIAS | venusaurgiga |
| victreebelmega | EXCLUDED_FORM | species-ignore |
| vikavolttotem | EXCLUDED_FORM | species-ignore |
| voltorbhisui | INTENTIONAL_ALIAS | voltorbh |
| vulpixalola | INTENTIONAL_ALIAS | vulpixa |
| weezinggalar | INTENTIONAL_ALIAS | weezingg |
| wishiwashischool | INTENTIONAL_ALIAS | wishiwashis |
| wooperpaldea | INTENTIONAL_ALIAS | wooperp |
| xerneasneutral | INTENTIONAL_ALIAS | xerneasnatural |
| yamaskgalar | INTENTIONAL_ALIAS | yamaskg |
| zapdosgalar | INTENTIONAL_ALIAS | zapdosg |
| zeraoramega | EXCLUDED_FORM | species-ignore |
| zigzagoongalar | INTENTIONAL_ALIAS | zigzagoong |
| zoroarkhisui | INTENTIONAL_ALIAS | zoroarkh |
| zoruahisui | INTENTIONAL_ALIAS | zoruah |
| zygardemega | EXCLUDED_FORM | species-ignore |

| Local species ID / constant | Class | Mapped source or reviewed learnset-only owner |
| --- | --- | --- |
| 1196 / SPECIES_ALCREMIE_BERRY | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1197 / SPECIES_ALCREMIE_CLOVER | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1198 / SPECIES_ALCREMIE_FLOWER | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1289 / SPECIES_ALCREMIE_GIGA | INTENTIONAL_ALIAS | alcremiegmax |
| 1199 / SPECIES_ALCREMIE_LOVE | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1200 / SPECIES_ALCREMIE_RIBBON | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1201 / SPECIES_ALCREMIE_STAR | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1161 / SPECIES_ALCREMIE_STRAWBERRY | INTENTIONAL_ALIAS | alcremie [learnset only] |
| 1282 / SPECIES_APPLETUN_GIGA | INTENTIONAL_ALIAS | appletungmax |
| 1235 / SPECIES_ARCANINE_H | INTENTIONAL_ALIAS | arcaninehisui |
| 720 / SPECIES_ARCEUS_FIGHT | INTENTIONAL_ALIAS | arceusfighting |
| 1221 / SPECIES_ARTICUNO_G | INTENTIONAL_ALIAS | articunogalar |
| 839 / SPECIES_ASHGRENINJA | INTENTIONAL_ALIAS | greninjaash |
| 1249 / SPECIES_AVALUGG_H | INTENTIONAL_ALIAS | avalugghisui |
| 1254 / SPECIES_BASCULEGION_M | INTENTIONAL_ALIAS | basculegion [learnset only] |
| 736 / SPECIES_BASCULIN_BLUE | INTENTIONAL_ALIAS | basculin [learnset only] |
| 1243 / SPECIES_BASCULIN_H | INTENTIONAL_ALIAS | basculinwhitestriped [learnset only] |
| 603 / SPECIES_BASCULIN_RED | INTENTIONAL_ALIAS | basculin [learnset only] |
| 1262 / SPECIES_BLASTOISE_GIGA | INTENTIONAL_ALIAS | blastoisegmax |
| 1246 / SPECIES_BRAVIARY_H | INTENTIONAL_ALIAS | braviaryhisui |
| 707 / SPECIES_BURMY_SANDY | INTENTIONAL_ALIAS | burmy [learnset only] |
| 708 / SPECIES_BURMY_TRASH | INTENTIONAL_ALIAS | burmy [learnset only] |
| 1263 / SPECIES_BUTTERFREE_GIGA | INTENTIONAL_ALIAS | butterfreegmax |
| 1210 / SPECIES_CALYREX_ICE_RIDER | INTENTIONAL_ALIAS | calyrexice |
| 1211 / SPECIES_CALYREX_SHADOW_RIDER | INTENTIONAL_ALIAS | calyrexshadow |
| 1286 / SPECIES_CENTISKORCH_GIGA | INTENTIONAL_ALIAS | centiskorchgmax |
| 1261 / SPECIES_CHARIZARD_GIGA | INTENTIONAL_ALIAS | charizardgmax |
| 751 / SPECIES_CHERRIM_SUN | INTENTIONAL_ALIAS | cherrimsunshine |
| 1275 / SPECIES_CINDERACE_GIGA | INTENTIONAL_ALIAS | cinderacegmax |
| 1280 / SPECIES_COALOSSAL_GIGA | INTENTIONAL_ALIAS | coalossalgmax |
| 1290 / SPECIES_COPPERAJAH_GIGA | INTENTIONAL_ALIAS | copperajahgmax |
| 1225 / SPECIES_CORSOLA_G | INTENTIONAL_ALIAS | corsolagalar |
| 1277 / SPECIES_CORVIKNIGHT_GIGA | INTENTIONAL_ALIAS | corviknightgmax |
| 1038 / SPECIES_CUBONE_A | EXCLUDED_FORM | cubone [learnset only] |
| 1230 / SPECIES_DARMANITAN_G | INTENTIONAL_ALIAS | darmanitangalar |
| 1231 / SPECIES_DARMANITAN_G_ZEN | INTENTIONAL_ALIAS | darmanitangalarzen |
| 1229 / SPECIES_DARUMAKA_G | INTENTIONAL_ALIAS | darumakagalar |
| 1250 / SPECIES_DECIDUEYE_H | INTENTIONAL_ALIAS | decidueyehisui |
| 739 / SPECIES_DEERLING_AUTUMN | INTENTIONAL_ALIAS | deerling [learnset only] |
| 738 / SPECIES_DEERLING_SUMMER | INTENTIONAL_ALIAS | deerling [learnset only] |
| 740 / SPECIES_DEERLING_WINTER | INTENTIONAL_ALIAS | deerling [learnset only] |
| 1027 / SPECIES_DIGLETT_A | INTENTIONAL_ALIAS | diglettalola |
| 1279 / SPECIES_DREDNAW_GIGA | INTENTIONAL_ALIAS | drednawgmax |
| 1379 / SPECIES_DUDUNSPARCE_THREE | INTENTIONAL_ALIAS | dudunsparcethreesegment |
| 1028 / SPECIES_DUGTRIO_A | INTENTIONAL_ALIAS | dugtrioalola |
| 1291 / SPECIES_DURALUDON_GIGA | INTENTIONAL_ALIAS | duraludongmax |
| 1270 / SPECIES_EEVEE_GIGA | INTENTIONAL_ALIAS | eeveegmax |
| 412 / SPECIES_EGG | EXCLUDED_FORM | explicit excluded local extra |
| 1237 / SPECIES_ELECTRODE_H | INTENTIONAL_ALIAS | electrodehisui |
| 1036 / SPECIES_EXEGGCUTE_A | EXCLUDED_FORM | exeggcute [learnset only] |
| 1037 / SPECIES_EXEGGUTOR_A | INTENTIONAL_ALIAS | exeggutoralola |
| 1217 / SPECIES_FARFETCHD_G | INTENTIONAL_ALIAS | farfetchdgalar |
| 840 / SPECIES_FLABEBE_BLUE | INTENTIONAL_ALIAS | flabebe [learnset only] |
| 841 / SPECIES_FLABEBE_ORANGE | INTENTIONAL_ALIAS | flabebe [learnset only] |
| 843 / SPECIES_FLABEBE_WHITE | INTENTIONAL_ALIAS | flabebe [learnset only] |
| 842 / SPECIES_FLABEBE_YELLOW | INTENTIONAL_ALIAS | flabebe [learnset only] |
| 1281 / SPECIES_FLAPPLE_GIGA | INTENTIONAL_ALIAS | flapplegmax |
| 844 / SPECIES_FLOETTE_BLUE | INTENTIONAL_ALIAS | floette [learnset only] |
| 845 / SPECIES_FLOETTE_ORANGE | INTENTIONAL_ALIAS | floette [learnset only] |
| 847 / SPECIES_FLOETTE_WHITE | INTENTIONAL_ALIAS | floette [learnset only] |
| 846 / SPECIES_FLOETTE_YELLOW | INTENTIONAL_ALIAS | floette [learnset only] |
| 849 / SPECIES_FLORGES_BLUE | INTENTIONAL_ALIAS | florges [learnset only] |
| 850 / SPECIES_FLORGES_ORANGE | INTENTIONAL_ALIAS | florges [learnset only] |
| 852 / SPECIES_FLORGES_WHITE | INTENTIONAL_ALIAS | florges [learnset only] |
| 851 / SPECIES_FLORGES_YELLOW | INTENTIONAL_ALIAS | florges [learnset only] |
| 704 / SPECIES_FRILLISH_F | INTENTIONAL_ALIAS | frillish [learnset only] |
| 866 / SPECIES_FURFROU_DANDY | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 867 / SPECIES_FURFROU_DEBUTANTE | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 860 / SPECIES_FURFROU_DIAMOND | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 859 / SPECIES_FURFROU_HEART | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 863 / SPECIES_FURFROU_KABUKI | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 864 / SPECIES_FURFROU_LA_REINE | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 865 / SPECIES_FURFROU_MATRON | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 862 / SPECIES_FURFROU_PHAROAH | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 861 / SPECIES_FURFROU_STAR | INTENTIONAL_ALIAS | furfrou [learnset only] |
| 1272 / SPECIES_GARBODOR_GIGA | INTENTIONAL_ALIAS | garbodorgmax |
| 712 / SPECIES_GASTRODON_EAST | INTENTIONAL_ALIAS | gastrodon [learnset only] |
| 1267 / SPECIES_GENGAR_GIGA | INTENTIONAL_ALIAS | gengargmax |
| 1031 / SPECIES_GEODUDE_A | INTENTIONAL_ALIAS | geodudealola |
| 1033 / SPECIES_GOLEM_A | INTENTIONAL_ALIAS | golemalola |
| 1248 / SPECIES_GOODRA_H | INTENTIONAL_ALIAS | goodrahisui |
| 857 / SPECIES_GOURGEIST_L | INTENTIONAL_ALIAS | gourgeist [learnset only] |
| 858 / SPECIES_GOURGEIST_M | INTENTIONAL_ALIAS | gourgeist [learnset only] |
| 856 / SPECIES_GOURGEIST_XL | INTENTIONAL_ALIAS | gourgeist [learnset only] |
| 1032 / SPECIES_GRAVELER_A | INTENTIONAL_ALIAS | graveleralola |
| 1034 / SPECIES_GRIMER_A | INTENTIONAL_ALIAS | grimeralola |
| 1288 / SPECIES_GRIMMSNARL_GIGA | INTENTIONAL_ALIAS | grimmsnarlgmax |
| 1234 / SPECIES_GROWLITHE_H | INTENTIONAL_ALIAS | growlithehisui |
| 1287 / SPECIES_HATTERENE_GIGA | INTENTIONAL_ALIAS | hatterenegmax |
| 744 / SPECIES_HIPPOPOTAS_F | INTENTIONAL_ALIAS | hippopotas [learnset only] |
| 745 / SPECIES_HIPPOWDON_F | INTENTIONAL_ALIAS | hippowdon [learnset only] |
| 1203 / SPECIES_INDEEDEE_FEMALE | INTENTIONAL_ALIAS | indeedeef |
| 1276 / SPECIES_INTELEON_GIGA | INTENTIONAL_ALIAS | inteleongmax |
| 705 / SPECIES_JELLICENT_F | INTENTIONAL_ALIAS | jellicent [learnset only] |
| 1268 / SPECIES_KINGLER_GIGA | INTENTIONAL_ALIAS | kinglergmax |
| 1218 / SPECIES_KOFFING_G | EXCLUDED_FORM | koffing [learnset only] |
| 1269 / SPECIES_LAPRAS_GIGA | INTENTIONAL_ALIAS | laprasgmax |
| 1242 / SPECIES_LILLIGANT_H | INTENTIONAL_ALIAS | lilliganthisui |
| 1227 / SPECIES_LINOONE_G | INTENTIONAL_ALIAS | linoonegalar |
| 1046 / SPECIES_LYCANROC_N | INTENTIONAL_ALIAS | lycanrocmidnight |
| 1266 / SPECIES_MACHAMP_GIGA | INTENTIONAL_ALIAS | machampgmax |
| 1073 / SPECIES_MAGEARNA_P | INTENTIONAL_ALIAS | magearnaoriginal |
| 1039 / SPECIES_MAROWAK_A | INTENTIONAL_ALIAS | marowakalola |
| 1273 / SPECIES_MELMETAL_GIGA | INTENTIONAL_ALIAS | melmetalgmax |
| 832 / SPECIES_MEOWSTIC_FEMALE | INTENTIONAL_ALIAS | meowsticf |
| 1029 / SPECIES_MEOWTH_A | INTENTIONAL_ALIAS | meowthalola |
| 1212 / SPECIES_MEOWTH_G | INTENTIONAL_ALIAS | meowthgalar |
| 1265 / SPECIES_MEOWTH_GIGA | INTENTIONAL_ALIAS | meowthgmax |
| 1228 / SPECIES_MIME_JR_G | EXCLUDED_FORM | mimejr [learnset only] |
| 1066 / SPECIES_MINIOR_BLUE | INTENTIONAL_ALIAS | minior [learnset only] |
| 1070 / SPECIES_MINIOR_GREEN | INTENTIONAL_ALIAS | minior [learnset only] |
| 1069 / SPECIES_MINIOR_INDIGO | INTENTIONAL_ALIAS | minior [learnset only] |
| 1067 / SPECIES_MINIOR_ORANGE | INTENTIONAL_ALIAS | minior [learnset only] |
| 1065 / SPECIES_MINIOR_RED | INTENTIONAL_ALIAS | minior |
| 991 / SPECIES_MINIOR_SHIELD | INTENTIONAL_ALIAS | miniormeteor |
| 1071 / SPECIES_MINIOR_VIOLET | INTENTIONAL_ALIAS | minior [learnset only] |
| 1068 / SPECIES_MINIOR_YELLOW | INTENTIONAL_ALIAS | minior [learnset only] |
| 1223 / SPECIES_MOLTRES_G | INTENTIONAL_ALIAS | moltresgalar |
| 1220 / SPECIES_MR_MIME_G | INTENTIONAL_ALIAS | mrmimegalar |
| 1035 / SPECIES_MUK_A | INTENTIONAL_ALIAS | mukalola |
| 1026 / SPECIES_NINETALES_A | INTENTIONAL_ALIAS | ninetalesalola |
| 0 / SPECIES_NONE | EXCLUDED_FORM | explicit excluded local extra |
| 1425 / SPECIES_OGERPON_CORNERSTONE_MASK | INTENTIONAL_ALIAS | ogerpon [learnset only] |
| 1429 / SPECIES_OGERPON_CORNERSTONE_TERASTAL | INTENTIONAL_ALIAS | ogerponcornerstonetera |
| 1424 / SPECIES_OGERPON_HEARTHFLAME_MASK | INTENTIONAL_ALIAS | ogerpon [learnset only] |
| 1428 / SPECIES_OGERPON_HEARTHFLAME_TERASTAL | INTENTIONAL_ALIAS | ogerponhearthflametera |
| 1426 / SPECIES_OGERPON_TERASTAL | INTENTIONAL_ALIAS | ogerpontealtera |
| 1423 / SPECIES_OGERPON_WELLSPRING_MASK | INTENTIONAL_ALIAS | ogerpon [learnset only] |
| 1427 / SPECIES_OGERPON_WELLSPRING_TERASTAL | INTENTIONAL_ALIAS | ogerponwellspringtera |
| 1305 / SPECIES_OINKOLOGNE_FEMALE | INTENTIONAL_ALIAS | oinkolognef |
| 1278 / SPECIES_ORBEETLE_GIGA | INTENTIONAL_ALIAS | orbeetlegmax |
| 1044 / SPECIES_ORICORIO_P | INTENTIONAL_ALIAS | oricoriopau |
| 1045 / SPECIES_ORICORIO_S | INTENTIONAL_ALIAS | oricoriosensu |
| 1043 / SPECIES_ORICORIO_Y | INTENTIONAL_ALIAS | oricoriopompom |
| 1030 / SPECIES_PERSIAN_A | INTENTIONAL_ALIAS | persianalola |
| 1100 / SPECIES_PICHU_SPIKY | INTENTIONAL_ALIAS | pichuspikyeared |
| 1098 / SPECIES_PIKACHU_CAP_ALOLA | INTENTIONAL_ALIAS | pikachualola |
| 1094 / SPECIES_PIKACHU_CAP_HOENN | INTENTIONAL_ALIAS | pikachuhoenn |
| 1097 / SPECIES_PIKACHU_CAP_KALOS | INTENTIONAL_ALIAS | pikachukalos |
| 1093 / SPECIES_PIKACHU_CAP_ORIGINAL | INTENTIONAL_ALIAS | pikachuoriginal |
| 1099 / SPECIES_PIKACHU_CAP_PARTNER | INTENTIONAL_ALIAS | pikachupartner |
| 1095 / SPECIES_PIKACHU_CAP_SINNOH | INTENTIONAL_ALIAS | pikachusinnoh |
| 1096 / SPECIES_PIKACHU_CAP_UNOVA | INTENTIONAL_ALIAS | pikachuunova |
| 1086 / SPECIES_PIKACHU_FLYING | EXCLUDED_FORM | pikachu [learnset only] |
| 1264 / SPECIES_PIKACHU_GIGA | INTENTIONAL_ALIAS | pikachugmax |
| 1085 / SPECIES_PIKACHU_SURFING | EXCLUDED_FORM | pikachu [learnset only] |
| 1195 / SPECIES_POLTEAGEIST_CHIPPED | INTENTIONAL_ALIAS | polteageistantique [learnset only] |
| 1213 / SPECIES_PONYTA_G | INTENTIONAL_ALIAS | ponytagalar |
| 854 / SPECIES_PUMPKABOO_L | INTENTIONAL_ALIAS | pumpkaboo [learnset only] |
| 855 / SPECIES_PUMPKABOO_M | INTENTIONAL_ALIAS | pumpkaboo [learnset only] |
| 853 / SPECIES_PUMPKABOO_XL | INTENTIONAL_ALIAS | pumpkaboo [learnset only] |
| 831 / SPECIES_PYROAR_FEMALE | INTENTIONAL_ALIAS | pyroar [learnset only] |
| 1239 / SPECIES_QWILFISH_H | INTENTIONAL_ALIAS | qwilfishhisui |
| 1022 / SPECIES_RAICHU_A | INTENTIONAL_ALIAS | raichualola |
| 1214 / SPECIES_RAPIDASH_G | INTENTIONAL_ALIAS | rapidashgalar |
| 1021 / SPECIES_RATICATE_A | INTENTIONAL_ALIAS | raticatealola |
| 1020 / SPECIES_RATTATA_A | INTENTIONAL_ALIAS | rattataalola |
| 1274 / SPECIES_RILLABOOM_GIGA | INTENTIONAL_ALIAS | rillaboomgmax |
| 1241 / SPECIES_SAMUROTT_H | INTENTIONAL_ALIAS | samurotthisui |
| 1283 / SPECIES_SANDACONDA_GIGA | INTENTIONAL_ALIAS | sandacondagmax |
| 1023 / SPECIES_SANDSHREW_A | INTENTIONAL_ALIAS | sandshrewalola |
| 1024 / SPECIES_SANDSLASH_A | INTENTIONAL_ALIAS | sandslashalola |
| 742 / SPECIES_SAWSBUCK_AUTUMN | INTENTIONAL_ALIAS | sawsbuck [learnset only] |
| 741 / SPECIES_SAWSBUCK_SUMMER | INTENTIONAL_ALIAS | sawsbuck [learnset only] |
| 743 / SPECIES_SAWSBUCK_WINTER | INTENTIONAL_ALIAS | sawsbuck [learnset only] |
| 706 / SPECIES_SHADOW_WARRIOR | EXCLUDED_FORM | explicit excluded local extra |
| 711 / SPECIES_SHELLOS_EAST | INTENTIONAL_ALIAS | shellos [learnset only] |
| 1048 / SPECIES_SILVALLY_FIGHT | INTENTIONAL_ALIAS | silvallyfighting |
| 1194 / SPECIES_SINISTEA_CHIPPED | INTENTIONAL_ALIAS | sinisteaantique [learnset only] |
| 1247 / SPECIES_SLIGGOO_H | INTENTIONAL_ALIAS | sliggoohisui |
| 1216 / SPECIES_SLOWBRO_G | INTENTIONAL_ALIAS | slowbrogalar |
| 1224 / SPECIES_SLOWKING_G | INTENTIONAL_ALIAS | slowkinggalar |
| 1215 / SPECIES_SLOWPOKE_G | INTENTIONAL_ALIAS | slowpokegalar |
| 1240 / SPECIES_SNEASEL_H | INTENTIONAL_ALIAS | sneaselhisui |
| 1271 / SPECIES_SNORLAX_GIGA | INTENTIONAL_ALIAS | snorlaxgmax |
| 1233 / SPECIES_STUNFISK_G | INTENTIONAL_ALIAS | stunfiskgalar |
| 1373 / SPECIES_TATSUGIRI_RED | INTENTIONAL_ALIAS | tatsugiri [learnset only] |
| 1374 / SPECIES_TATSUGIRI_YELLOW | INTENTIONAL_ALIAS | tatsugiri [learnset only] |
| 1411 / SPECIES_TAUROS_AQUA_P | INTENTIONAL_ALIAS | taurospaldeaaqua |
| 1410 / SPECIES_TAUROS_BLAZE_P | INTENTIONAL_ALIAS | taurospaldeablaze |
| 1409 / SPECIES_TAUROS_P | INTENTIONAL_ALIAS | taurospaldeacombat |
| 1284 / SPECIES_TOXTRICITY_GIGA | INTENTIONAL_ALIAS | toxtricitygmax |
| 1285 / SPECIES_TOXTRICITY_LOW_KEY_GIGA | INTENTIONAL_ALIAS | toxtricitylowkeygmax |
| 1238 / SPECIES_TYPHLOSION_H | INTENTIONAL_ALIAS | typhlosionhisui |
| 703 / SPECIES_UNFEZANT_F | INTENTIONAL_ALIAS | unfezant [learnset only] |
| 413 / SPECIES_UNOWN_B | INTENTIONAL_ALIAS | unown [learnset only] |
| 414 / SPECIES_UNOWN_C | INTENTIONAL_ALIAS | unown [learnset only] |
| 415 / SPECIES_UNOWN_D | INTENTIONAL_ALIAS | unown [learnset only] |
| 416 / SPECIES_UNOWN_E | INTENTIONAL_ALIAS | unown [learnset only] |
| 438 / SPECIES_UNOWN_EXCLAMATION | INTENTIONAL_ALIAS | unown [learnset only] |
| 417 / SPECIES_UNOWN_F | INTENTIONAL_ALIAS | unown [learnset only] |
| 418 / SPECIES_UNOWN_G | INTENTIONAL_ALIAS | unown [learnset only] |
| 419 / SPECIES_UNOWN_H | INTENTIONAL_ALIAS | unown [learnset only] |
| 420 / SPECIES_UNOWN_I | INTENTIONAL_ALIAS | unown [learnset only] |
| 421 / SPECIES_UNOWN_J | INTENTIONAL_ALIAS | unown [learnset only] |
| 422 / SPECIES_UNOWN_K | INTENTIONAL_ALIAS | unown [learnset only] |
| 423 / SPECIES_UNOWN_L | INTENTIONAL_ALIAS | unown [learnset only] |
| 424 / SPECIES_UNOWN_M | INTENTIONAL_ALIAS | unown [learnset only] |
| 425 / SPECIES_UNOWN_N | INTENTIONAL_ALIAS | unown [learnset only] |
| 426 / SPECIES_UNOWN_O | INTENTIONAL_ALIAS | unown [learnset only] |
| 427 / SPECIES_UNOWN_P | INTENTIONAL_ALIAS | unown [learnset only] |
| 428 / SPECIES_UNOWN_Q | INTENTIONAL_ALIAS | unown [learnset only] |
| 439 / SPECIES_UNOWN_QUESTION | INTENTIONAL_ALIAS | unown [learnset only] |
| 429 / SPECIES_UNOWN_R | INTENTIONAL_ALIAS | unown [learnset only] |
| 430 / SPECIES_UNOWN_S | INTENTIONAL_ALIAS | unown [learnset only] |
| 431 / SPECIES_UNOWN_T | INTENTIONAL_ALIAS | unown [learnset only] |
| 432 / SPECIES_UNOWN_U | INTENTIONAL_ALIAS | unown [learnset only] |
| 433 / SPECIES_UNOWN_V | INTENTIONAL_ALIAS | unown [learnset only] |
| 434 / SPECIES_UNOWN_W | INTENTIONAL_ALIAS | unown [learnset only] |
| 435 / SPECIES_UNOWN_X | INTENTIONAL_ALIAS | unown [learnset only] |
| 436 / SPECIES_UNOWN_Y | INTENTIONAL_ALIAS | unown [learnset only] |
| 437 / SPECIES_UNOWN_Z | INTENTIONAL_ALIAS | unown [learnset only] |
| 1208 / SPECIES_URSHIFU_RAPID | INTENTIONAL_ALIAS | urshifurapidstrike |
| 1293 / SPECIES_URSHIFU_RAPID_GIGA | INTENTIONAL_ALIAS | urshifurapidstrikegmax |
| 1184 / SPECIES_URSHIFU_SINGLE | INTENTIONAL_ALIAS | urshifu |
| 1292 / SPECIES_URSHIFU_SINGLE_GIGA | INTENTIONAL_ALIAS | urshifugmax |
| 1260 / SPECIES_VENUSAUR_GIGA | INTENTIONAL_ALIAS | venusaurgmax |
| 921 / SPECIES_VIVILLON_ARCHIPELAGO | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 922 / SPECIES_VIVILLON_CONTINENTAL | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 923 / SPECIES_VIVILLON_ELEGANT | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 924 / SPECIES_VIVILLON_GARDEN | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 925 / SPECIES_VIVILLON_HIGH_PLAINS | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 926 / SPECIES_VIVILLON_ICY_SNOW | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 927 / SPECIES_VIVILLON_JUNGLE | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 928 / SPECIES_VIVILLON_MARINE | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 929 / SPECIES_VIVILLON_MODERN | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 930 / SPECIES_VIVILLON_MONSOON | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 931 / SPECIES_VIVILLON_OCEAN | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 933 / SPECIES_VIVILLON_POLAR | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 934 / SPECIES_VIVILLON_RIVER | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 935 / SPECIES_VIVILLON_SANDSTORM | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 936 / SPECIES_VIVILLON_SAVANNA | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 937 / SPECIES_VIVILLON_SUN | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 938 / SPECIES_VIVILLON_TUNDRA | INTENTIONAL_ALIAS | vivillon [learnset only] |
| 1236 / SPECIES_VOLTORB_H | INTENTIONAL_ALIAS | voltorbhisui |
| 1025 / SPECIES_VULPIX_A | INTENTIONAL_ALIAS | vulpixalola |
| 1219 / SPECIES_WEEZING_G | INTENTIONAL_ALIAS | weezinggalar |
| 1047 / SPECIES_WISHIWASHI_S | INTENTIONAL_ALIAS | wishiwashischool |
| 1412 / SPECIES_WOOPER_P | INTENTIONAL_ALIAS | wooperpaldea |
| 1101 / SPECIES_XERNEAS_NATURAL | INTENTIONAL_ALIAS | xerneasneutral |
| 1232 / SPECIES_YAMASK_G | INTENTIONAL_ALIAS | yamaskgalar |
| 1222 / SPECIES_ZAPDOS_G | INTENTIONAL_ALIAS | zapdosgalar |
| 1226 / SPECIES_ZIGZAGOON_G | INTENTIONAL_ALIAS | zigzagoongalar |
| 1245 / SPECIES_ZOROARK_H | INTENTIONAL_ALIAS | zoroarkhisui |
| 1244 / SPECIES_ZORUA_H | INTENTIONAL_ALIAS | zoruahisui |
| 835 / SPECIES_ZYGARDE_CELL | EXCLUDED_FORM | zygarde [learnset only] |
| 836 / SPECIES_ZYGARDE_CORE | EXCLUDED_FORM | zygarde [learnset only] |

## Appendix B — complete blocked and aliased assignments

| Source | Slot | Intended Ability | Current local value | Block |
| --- | --- | --- | --- | --- |
| calyrexice | ability1 | asoneglastrier | ABILITY_ASONE_CHILLING | ability-blocked-alias |
| calyrexshadow | ability1 | asonespectrier | ABILITY_ASONE_GRIM | ability-blocked-alias |
| chiyu | ability1 | beadsofruin | ABILITY_STALL | ability-blocked-alias |
| glastrier | ability1 | chillingneigh | ABILITY_MOXIE | ability-blocked-alias |
| tatsugiri | ability1 | commander | ABILITY_GUTS | ability-blocked-alias |
| ogerponcornerstonetera | ability1 | embodyaspectcornerstone | ABILITY_STURDY | ability-blocked-alias |
| ogerponhearthflametera | ability1 | embodyaspecthearthflame | ABILITY_MOLDBREAKER | ability-blocked-alias |
| ogerpontealtera | ability1 | embodyaspectteal | ABILITY_DEFIANT | ability-blocked-alias |
| ogerponwellspringtera | ability1 | embodyaspectwellspring | ABILITY_WATERABSORB | ability-blocked-alias |
| solgaleo | ability1 | fullmetalbody | ABILITY_CLEARBODY | ability-blocked-alias |
| gholdengo | ability1 | goodasgold | ABILITY_GOODASGOLD | ability-blocked-alias |
| miraidon | ability1 | hadronengine | ABILITY_HADRONENGINE | ability-blocked-alias |
| poltchageist | ability1 | hospitality | ABILITY_WEAKARMOR | ability-blocked-alias |
| poltchageistartisan | ability1 | hospitality | ABILITY_WEAKARMOR | ability-blocked-alias |
| sinistcha | ability1 | hospitality | ABILITY_WEAKARMOR | ability-blocked-alias |
| sinistchamasterpiece | ability1 | hospitality | ABILITY_WEAKARMOR | ability-blocked-alias |
| cinderacegmax | hiddenAbility | libero | ABILITY_NONE | ability-blocked-alias |
| cinderace | hiddenAbility | libero | ABILITY_PROTEAN | ability-blocked-alias |
| raboot | hiddenAbility | libero | ABILITY_PROTEAN | ability-blocked-alias |
| scorbunny | hiddenAbility | libero | ABILITY_PROTEAN | ability-blocked-alias |
| oinkologne | ability1 | lingeringaroma | ABILITY_AROMAVEIL | ability-unmapped |
| koraidon | ability1 | orichalcumpulse | ABILITY_ORICHALCUMPULSE | ability-blocked-alias |
| pecharunt | ability1 | poisonpuppeteer | ABILITY_POISONPUPPETEER | ability-blocked-alias |
| bombirdier | hiddenAbility | rockypayload | ABILITY_ROCKYPAYLOAD | ability-blocked-alias |
| arboliva | ability1 | seedsower | ABILITY_SEEDSOWER | ability-blocked-alias |
| veluza | hiddenAbility | sharpness | ABILITY_INTIMIDATE | ability-blocked-alias |
| gallade | ability2 | sharpness | ABILITY_STRONGJAW | ability-blocked-alias |
| kleavor | hiddenAbility | sharpness | ABILITY_STRONGJAW | ability-blocked-alias |
| samurotthisui | hiddenAbility | sharpness | ABILITY_STRONGJAW | ability-blocked-alias |
| chienpao | ability1 | swordofruin | ABILITY_STALL | ability-blocked-alias |
| wochien | ability1 | tabletsofruin | ABILITY_STALL | ability-blocked-alias |
| terapagosstellar | ability1 | teraformzero | ABILITY_COLORCHANGE | ability-blocked-alias |
| terapagosterastal | ability1 | terashell | ABILITY_COLORCHANGE | ability-blocked-alias |
| terapagos | ability1 | terashift | ABILITY_ICEFACE | ability-blocked-alias |
| glimmet | ability1 | toxicdebris | ABILITY_TOXICDEBRIS | ability-blocked-alias |
| glimmora | ability1 | toxicdebris | ABILITY_TOXICDEBRIS | ability-blocked-alias |
| tinglu | ability1 | vesselofruin | ABILITY_STALL | ability-blocked-alias |
| kilowattrel | ability1 | windpower | ABILITY_WINDPOWER | ability-blocked-alias |
| wattrel | ability1 | windpower | ABILITY_WINDPOWER | ability-blocked-alias |
| brambleghast | ability1 | windrider | ABILITY_WINDRIDER | ability-blocked-alias |
| bramblin | ability1 | windrider | ABILITY_WINDRIDER | ability-blocked-alias |
| shiftry | ability2 | windrider | ABILITY_WINDRIDER | ability-blocked-alias |
| palafin | ability1 | zerotohero | ABILITY_ZEROTOHERO | ability-blocked-alias |
| palafinhero | ability1 | zerotohero | ABILITY_ZEROTOHERO | ability-blocked-alias |

| Source | Slot | Accepted identity | Older effect |
| --- | --- | --- | --- |
| arctibax | 0 | thermalexchange | ABILITY_STEAMENGINE |
| baxcalibur | 0 | thermalexchange | ABILITY_STEAMENGINE |
| bellibolt | 0 | electromorphosis | ABILITY_COLORCHANGE |
| brutebonnet | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| dachsbun | 0 | wellbakedbody | ABILITY_STEAMENGINE |
| dipplin | 0 | supersweetsyrup | ABILITY_INTIMIDATE |
| espathra | 0 | opportunist | ABILITY_DANCER |
| farigiraf | 0 | cudchew | ABILITY_HARVEST |
| farigiraf | 1 | armortail | ABILITY_DAZZLING |
| fezandipiti | 0 | toxicchain | ABILITY_POISONTOUCH |
| flamigo | H | costar | ABILITY_CURIOUSMEDICINE |
| fluttermane | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| frigibax | 0 | thermalexchange | ABILITY_STEAMENGINE |
| garganacl | 0 | purifyingsalt | ABILITY_IMMUNITY |
| gougingfire | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| greattusk | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| hydrapple | 0 | supersweetsyrup | ABILITY_INTIMIDATE |
| kingambit | 1 | supremeoverlord | ABILITY_HUGEPOWER |
| klawf | 0 | angershell | ABILITY_WEAKARMOR |
| mabosstiff | 1 | guarddog | ABILITY_INNERFOCUS |
| munkidori | 0 | toxicchain | ABILITY_POISONTOUCH |
| nacli | 0 | purifyingsalt | ABILITY_IMMUNITY |
| naclstack | 0 | purifyingsalt | ABILITY_IMMUNITY |
| okidogi | 0 | toxicchain | ABILITY_POISONTOUCH |
| okidogi | H | guarddog | ABILITY_INNERFOCUS |
| orthworm | 0 | eartheater | ABILITY_VOLTABSORB |
| ragingbolt | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| roaringmoon | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| sandyshocks | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| screamtail | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| slitherwing | 0 | protosynthesis | ABILITY_QUARKDRIVE |
| taurospaldeaaqua | H | cudchew | ABILITY_HARVEST |
| taurospaldeablaze | H | cudchew | ABILITY_HARVEST |
| taurospaldeacombat | H | cudchew | ABILITY_HARVEST |
| toedscool | 0 | myceliummight | ABILITY_MOLDBREAKER |
| toedscruel | 0 | myceliummight | ABILITY_MOLDBREAKER |
| ursalunabloodmoon | 0 | mindseye | ABILITY_SCRAPPY |
| walkingwake | 0 | protosynthesis | ABILITY_QUARKDRIVE |

## Appendix C — blocked learnsets and excluded consumers

| Target | Class | Consumers | Block |
| --- | --- | --- | --- |
| sAlakazamLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | alakazam, alakazammega | allyswitch:move-open-risk |
| sArmarougeLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | armarouge | allyswitch:move-open-risk |
| sAzelfLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | azelf | allyswitch:move-open-risk |
| sCeruledgeLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | ceruledge | allyswitch:move-open-risk |
| sCresseliaLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | cresselia | allyswitch:move-open-risk |
| sDuosionLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | duosion | allyswitch:move-open-risk |
| sHoopaLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | hoopa | allyswitch:move-open-risk |
| sHoopaUnboundLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | hoopaunbound | allyswitch:move-open-risk |
| sIronLeavesLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | ironleaves | allyswitch:move-open-risk |
| sKadabraLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | kadabra | allyswitch:move-open-risk |
| sLatiosLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | latios, latiosmega | allyswitch:move-open-risk |
| sMespritLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | mesprit | allyswitch:move-open-risk |
| sMrMimeGLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | mrmimeg | allyswitch:move-open-risk |
| sMrRimeLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | mrrime | allyswitch:move-open-risk |
| sOrbeetleLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | orbeetle, orbeetlegiga | allyswitch:move-open-risk |
| sReuniclusLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | reuniclus | allyswitch:move-open-risk |
| sSolosisLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | solosis | allyswitch:move-open-risk |
| sUxieLevelUpLearnset | MOVE_BEHAVIOR_BLOCK | uxie | allyswitch:move-open-risk |
| sShadowWarriorLevelUpLearnset | FORM_MAPPING_BLOCK | shadowwarrior | unmapped consumer or no justified coherent dataset |

| Consumer | Disposition | Target / profile |
| --- | --- | --- |
| 252 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 253 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 254 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 255 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 256 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 257 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 258 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 259 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 260 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 261 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 262 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 263 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 264 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 265 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 266 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 267 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 268 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 269 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 270 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 271 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 272 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 273 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 274 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 275 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| 276 | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| alakazam | MOVE_BEHAVIOR_BLOCK | sAlakazamLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| alakazammega | MOVE_BEHAVIOR_BLOCK | sAlakazamLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| armarouge | MOVE_BEHAVIOR_BLOCK | sArmarougeLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| azelf | MOVE_BEHAVIOR_BLOCK | sAzelfLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| ceruledge | MOVE_BEHAVIOR_BLOCK | sCeruledgeLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| cresselia | MOVE_BEHAVIOR_BLOCK | sCresseliaLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| cubonea | NO_DIFF | sCuboneLevelUpLearnset; EXCLUDE_CUSTOM_PRE_EVOLUTION_MARKER |
| duosion | MOVE_BEHAVIOR_BLOCK | sDuosionLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| egg | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| exeggcutea | NO_DIFF | sExeggcuteLevelUpLearnset; EXCLUDE_CUSTOM_PRE_EVOLUTION_MARKER |
| hoopa | MOVE_BEHAVIOR_BLOCK | sHoopaLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| hoopaunbound | MOVE_BEHAVIOR_BLOCK | sHoopaUnboundLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| ironleaves | MOVE_BEHAVIOR_BLOCK | sIronLeavesLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| kadabra | MOVE_BEHAVIOR_BLOCK | sKadabraLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| koffingg | NO_DIFF | sKoffingLevelUpLearnset; EXCLUDE_CUSTOM_PRE_EVOLUTION_MARKER |
| latios | MOVE_BEHAVIOR_BLOCK | sLatiosLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| latiosmega | MOVE_BEHAVIOR_BLOCK | sLatiosLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| mesprit | MOVE_BEHAVIOR_BLOCK | sMespritLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| mimejrg | NO_DIFF | sMimeJrLevelUpLearnset; EXCLUDE_CUSTOM_PRE_EVOLUTION_MARKER |
| mrmimeg | MOVE_BEHAVIOR_BLOCK | sMrMimeGLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| mrrime | MOVE_BEHAVIOR_BLOCK | sMrRimeLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| none | EXCLUDE_RESERVED_SENTINEL | sEmptyMoveset;  |
| orbeetle | MOVE_BEHAVIOR_BLOCK | sOrbeetleLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| orbeetlegiga | MOVE_BEHAVIOR_BLOCK | sOrbeetleLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| pikachuflying | NO_DIFF | sPikachuLevelUpLearnset; EXCLUDE_CUSTOM_TYPED_FORM; existing base learnset ownership only, no invented Fly/Surf |
| pikachusurfing | NO_DIFF | sPikachuLevelUpLearnset; EXCLUDE_CUSTOM_TYPED_FORM; existing base learnset ownership only, no invented Fly/Surf |
| reuniclus | MOVE_BEHAVIOR_BLOCK | sReuniclusLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| shadowwarrior | EXCLUDE_UNRESOLVED_FORM | sShadowWarriorLevelUpLearnset;  |
| solosis | MOVE_BEHAVIOR_BLOCK | sSolosisLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| uxie | MOVE_BEHAVIOR_BLOCK | sUxieLevelUpLearnset; LEARNSET_DATA_ONLY; battle/form mechanics not certified |
| zygardecell | NO_DIFF | sZygardeLevelUpLearnset; EXCLUDE_NONCOMBAT_PLACEHOLDER; existing pointer ownership only, no battle-form claim |
| zygardecore | NO_DIFF | sZygardeLevelUpLearnset; EXCLUDE_NONCOMBAT_PLACEHOLDER; existing pointer ownership only, no battle-form claim |

## Appendix D — complete move boundaries

| Move | Class | Reason / engine encoding |
| --- | --- | --- |
| 10000000voltthunderbolt | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| aciddownpour | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| alloutpummeling | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| allyswitch | MISSING_LOCAL_MOVE | move-open-risk |
| assist | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| baddybad | MAPPING_BLOCK | move-open-risk |
| beatup | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| bide | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| blackholeeclipse | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| bloomdoom | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| bouncybubble | MAPPING_BLOCK | move-open-risk |
| breakneckblitz | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| buzzybuzz | MAPPING_BLOCK | move-open-risk |
| catastropika | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| clangoroussoulblaze | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| comeuppance | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| continentalcrush | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| copycat | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| corkscrewcrash | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| counter | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| crushgrip | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| devastatingdrake | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| dragonrage | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| electroball | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| endeavor | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| extremeevoboost | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| finalgambit | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| fissure | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| flail | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| fling | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| floatyfall | MAPPING_BLOCK | move-open-risk |
| freezyfrost | MAPPING_BLOCK | move-open-risk |
| frustration | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| genesissupernova | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gigavolthavoc | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| glitzyglow | MAPPING_BLOCK | move-open-risk |
| gmaxbefuddle | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxcannonade | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxcentiferno | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxchistrike | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxcuddle | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxdepletion | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxdrumsolo | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxfinale | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxfireball | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxfoamburst | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxgoldrush | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxgravitas | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxhydrosnipe | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxmalodor | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxmeltdown | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxoneblow | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxrapidflow | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxreplenish | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxresonance | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxsandblast | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxsmite | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxsnooze | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxsteelsurge | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxstonesurge | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxstunshock | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxsweetness | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxtartness | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxterror | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxvinelash | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxvolcalith | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxvoltcrash | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxwildfire | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| gmaxwindrage | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| grassknot | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| guardianofalola | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| guillotine | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| gyroball | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| hardpress | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| heatcrash | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| heavyslam | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| horndrill | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| hydrovortex | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| infernooverdrive | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| letssnuggleforever | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| lightthatburnsthesky | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| lowkick | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| magiccoat | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| magnitude | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| maliciousmoonsault | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxairstream | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxdarkness | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxflare | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxflutterby | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxgeyser | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxguard | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxhailstorm | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxknuckle | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxlightning | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxmindstorm | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxooze | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxovergrowth | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxphantasm | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxquake | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxrockfall | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxstarfall | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxsteelspike | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxstrike | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| maxwyrmwind | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| menacingmoonrazemaelstrom | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| metalburst | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| metronome | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| mirrorcoat | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| naturalgift | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| naturesmadness | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| neverendingnightmare | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| nightshade | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| nihillight | MAPPING_BLOCK | move-ignore |
| oceanicoperetta | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| painsplit | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| pikapapow | MAPPING_BLOCK | move-open-risk |
| present | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| psywave | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| pulverizingpancake | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| punishment | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 60 |
| return | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| reversal | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| ruination | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| sappyseed | MAPPING_BLOCK | move-open-risk |
| savagespinout | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| searingsunrazesmash | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| seismictoss | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| shatteredpsyche | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| sheercold | INTENTIONAL_ENGINE_DIFFERENCE | handler-computed damage/power: Showdown 0 / CFRU 1 |
| sinisterarrowraid | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| sizzlyslide | MAPPING_BLOCK | move-open-risk |
| sleeptalk | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| snatch | ENGINE_BEHAVIOR_UNVERIFIED | target handler requires review: MOVE_TARGET_DEPENDS / MOVE_TARGET_USER |
| sonicboom | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| soulstealing7starstrike | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| sparklyswirl | MAPPING_BLOCK | move-open-risk |
| spitup | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| splinteredstormshards | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| splishysplash | MAPPING_BLOCK | move-open-risk |
| stokedsparksurfer | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| struggle | INTENTIONAL_ENGINE_DIFFERENCE | Struggle typeless engine encoding; damage_calc explicitly handles MOVE_STRUGGLE |
| subzeroslammer | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| superfang | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| supersonicskystrike | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| tectonicrage | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| trumpcard | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| twinkletackle | INTENTIONAL_ENGINE_DIFFERENCE | generated Z/Max/GMax; excluded from ordinary learnset domain |
| veeveevolley | MAPPING_BLOCK | move-open-risk |
| wringout | INTENTIONAL_ENGINE_DIFFERENCE | dynamic-power: Showdown 0 / CFRU 1 |
| zippyzap | MAPPING_BLOCK | move-open-risk |

Mapped full names not literally present in short name table: alluringvoice, aromaticmist, astralbarrage, babydolleyes, banefulbunker, behemothbash, behemothblade, blazingtorque, bleakwindstorm, breakingswipe, burningbulwark, burningjealousy, ceaselessedge, chillingwater, chillyreception, clangingscales, clangoroussoul, collisioncourse, coreenforcer, corrosivegas, craftyshield, darkestlariat, dazzlinggleam, disarmingvoice, doubleironbash, dragonhammer, drainingkiss, dynamaxcannon, electricterrain, expandingforce, falsesurrender, firstimpression, floralhealing, flowershield, forestscurse, freezingglare, gigatonhammer, grassyterrain, highhorsepower, highjumpkick, hyperspacefury, hyperspacehole, infernalparade, junglehealing, kowtowcleave, lightofruin, lunarblessing, magicaltorque, magneticflux, malignantchain, meteorassault, mightycleave, mistyexplosion, mistyterrain, moongeistbeam, mysticalfire, mysticalpower, naturesmadness, noxioustorque, paraboliccharge, petalblizzard, populationbomb, poweruppunch, precipiceblades, prismaticlaser, psychicfangs, psychicterrain, psyshieldbash, revelationdance, revivalblessing, risingvoltage, sandsearstorm, scorchingsands, smellingsalts, sparklingaria, spectralthief, spiritshackle, springtidestorm, steameruption, stompingtantrum, strangesteam, sunsteelstrike, supercellslam, surgingstrikes, tachyoncutter, tearfullook, terastarstorm, thousandarrows, thousandwaves, thunderouskick, trickortreat, watershuriken, wildboltstorm.

Mapped records with no exact target-class certificate: acrobatics:any, acupressure:adjacentAllyOrSelf, aerialace:any, aeroblast:any, airslash:any, aromatherapy:allyTeam, aromaticmist:adjacentAlly, aurasphere:any, auroraveil:allySide, bounce:any, bravebird:any, chatter:any, chillyreception:all, coaching:adjacentAlly, comeuppance:scripted, counter:scripted, courtchange:all, craftyshield:allySide, darkpulse:any, doodle:adjacentFoe, dragonascent:any, dragoncheer:adjacentAlly, dragonpulse:any, drillpeck:any, electricterrain:all, fairylock:all, flowershield:all, fly:any, flyingpress:any, gearup:allySide, grassyterrain:all, gravity:all, gust:any, hail:all, happyhour:allySide, haze:all, healbell:allyTeam, healpulse:any, helpinghand:adjacentAlly, holdhands:adjacentAlly, howl:allies, hurricane:any, iondeluge:all, junglehealing:allies, lifedew:allies, lightscreen:allySide, luckychant:allySide, lunarblessing:allies, magicroom:all, magneticflux:allySide, matblock:allySide, mefirst:adjacentFoe, metalburst:scripted, mirrorcoat:scripted, mist:allySide, mistyterrain:all, mudsport:all, oblivionwing:any, outrage:randomNormal, peck:any, perishsong:all, petaldance:randomNormal, pluck:any, psychicterrain:all, quickguard:allySide, ragingfury:randomNormal, raindance:all, reflect:allySide, rototiller:all, safeguard:allySide, sandstorm:all, skyattack:any, skydrop:any, snowscape:all, spikes:foeSide, stealthrock:foeSide, stickyweb:foeSide, struggle:randomNormal, sunnyday:all, tailwind:allySide, teatime:all, thrash:randomNormal, toxicspikes:foeSide, trickroom:all, uproar:randomNormal, waterpulse:any, watersport:all, wideguard:allySide, wingattack:any, wonderroom:all.

Uncompared local battle constants (generated/project/helper scope): MOVE_10000000_VOLT_THUNDERBOLT, MOVE_ACID_DOWNPOUR_P, MOVE_ACID_DOWNPOUR_S, MOVE_ALL_OUT_PUMMELING_P, MOVE_ALL_OUT_PUMMELING_S, MOVE_BLACK_HOLE_ECLIPSE_P, MOVE_BLACK_HOLE_ECLIPSE_S, MOVE_BLOOM_DOOM_P, MOVE_BLOOM_DOOM_S, MOVE_BREAKNECK_BLITZ_P, MOVE_BREAKNECK_BLITZ_S, MOVE_CATASTROPIKA, MOVE_CLANGOROUS_SOULBLAZE, MOVE_CONTINENTAL_CRUSH_P, MOVE_CONTINENTAL_CRUSH_S, MOVE_CORKSCREW_CRASH_P, MOVE_CORKSCREW_CRASH_S, MOVE_DEVASTATING_DRAKE_P, MOVE_DEVASTATING_DRAKE_S, MOVE_EXTREME_EVOBOOST, MOVE_GENESIS_SUPERNOVA, MOVE_GIGAVOLT_HAVOC_P, MOVE_GIGAVOLT_HAVOC_S, MOVE_GUARDIAN_OF_ALOLA, MOVE_G_MAX_BEFUDDLE_P, MOVE_G_MAX_BEFUDDLE_S, MOVE_G_MAX_CANNONADE_P, MOVE_G_MAX_CANNONADE_S, MOVE_G_MAX_CENTIFERNO_P, MOVE_G_MAX_CENTIFERNO_S, MOVE_G_MAX_CHI_STRIKE_P, MOVE_G_MAX_CHI_STRIKE_S, MOVE_G_MAX_CUDDLE_P, MOVE_G_MAX_CUDDLE_S, MOVE_G_MAX_DEPLETION_P, MOVE_G_MAX_DEPLETION_S, MOVE_G_MAX_DRUM_SOLO_P, MOVE_G_MAX_DRUM_SOLO_S, MOVE_G_MAX_FINALE_P, MOVE_G_MAX_FINALE_S, MOVE_G_MAX_FIREBALL_P, MOVE_G_MAX_FIREBALL_S, MOVE_G_MAX_FOAM_BURST_P, MOVE_G_MAX_FOAM_BURST_S, MOVE_G_MAX_GOLD_RUSH_P, MOVE_G_MAX_GOLD_RUSH_S, MOVE_G_MAX_GRAVITAS_P, MOVE_G_MAX_GRAVITAS_S, MOVE_G_MAX_HYDROSNIPE_P, MOVE_G_MAX_HYDROSNIPE_S, MOVE_G_MAX_MALODOR_P, MOVE_G_MAX_MALODOR_S, MOVE_G_MAX_MELTDOWN_P, MOVE_G_MAX_MELTDOWN_S, MOVE_G_MAX_ONE_BLOW_P, MOVE_G_MAX_ONE_BLOW_S, MOVE_G_MAX_RAPID_FLOW_P, MOVE_G_MAX_RAPID_FLOW_S, MOVE_G_MAX_REPLENISH_P, MOVE_G_MAX_REPLENISH_S, MOVE_G_MAX_RESONANCE_P, MOVE_G_MAX_RESONANCE_S, MOVE_G_MAX_SANDBLAST_P, MOVE_G_MAX_SANDBLAST_S, MOVE_G_MAX_SMITE_P, MOVE_G_MAX_SMITE_S, MOVE_G_MAX_SNOOZE_P, MOVE_G_MAX_SNOOZE_S, MOVE_G_MAX_STEELSURGE_P, MOVE_G_MAX_STEELSURGE_S, MOVE_G_MAX_STONESURGE_P, MOVE_G_MAX_STONESURGE_S, MOVE_G_MAX_STUN_SHOCK_P, MOVE_G_MAX_STUN_SHOCK_S, MOVE_G_MAX_SWEETNESS_P, MOVE_G_MAX_SWEETNESS_S, MOVE_G_MAX_TARTNESS_P, MOVE_G_MAX_TARTNESS_S, MOVE_G_MAX_TERROR_P, MOVE_G_MAX_TERROR_S, MOVE_G_MAX_VINE_LASH_P, MOVE_G_MAX_VINE_LASH_S, MOVE_G_MAX_VOLCALITH_P, MOVE_G_MAX_VOLCALITH_S, MOVE_G_MAX_VOLT_CRASH_P, MOVE_G_MAX_VOLT_CRASH_S, MOVE_G_MAX_WILDFIRE_P, MOVE_G_MAX_WILDFIRE_S, MOVE_G_MAX_WIND_RAGE_P, MOVE_G_MAX_WIND_RAGE_S, MOVE_HYDRO_VORTEX_P, MOVE_HYDRO_VORTEX_S, MOVE_INFERNO_OVERDRIVE_P, MOVE_INFERNO_OVERDRIVE_S, MOVE_LEECHFANG, MOVE_LETS_SNUGGLE_FOREVER, MOVE_LIGHT_THAT_BURNS_THE_SKY, MOVE_MALICIOUS_MOONSAULT, MOVE_MAX_AIRSTREAM_P, MOVE_MAX_AIRSTREAM_S, MOVE_MAX_DARKNESS_P, MOVE_MAX_DARKNESS_S, MOVE_MAX_FLARE_P, MOVE_MAX_FLARE_S, MOVE_MAX_FLUTTERBY_P, MOVE_MAX_FLUTTERBY_S, MOVE_MAX_GEYSER_P, MOVE_MAX_GEYSER_S, MOVE_MAX_GUARD, MOVE_MAX_HAILSTORM_P, MOVE_MAX_HAILSTORM_S, MOVE_MAX_KNUCKLE_P, MOVE_MAX_KNUCKLE_S, MOVE_MAX_LIGHTNING_P, MOVE_MAX_LIGHTNING_S, MOVE_MAX_MINDSTORM_P, MOVE_MAX_MINDSTORM_S, MOVE_MAX_OOZE_P, MOVE_MAX_OOZE_S, MOVE_MAX_OVERGROWTH_P, MOVE_MAX_OVERGROWTH_S, MOVE_MAX_PHANTASM_P, MOVE_MAX_PHANTASM_S, MOVE_MAX_QUAKE_P, MOVE_MAX_QUAKE_S, MOVE_MAX_ROCKFALL_P, MOVE_MAX_ROCKFALL_S, MOVE_MAX_STARFALL_P, MOVE_MAX_STARFALL_S, MOVE_MAX_STEELSPIKE_P, MOVE_MAX_STEELSPIKE_S, MOVE_MAX_STRIKE_P, MOVE_MAX_STRIKE_S, MOVE_MAX_WYRMWIND_P, MOVE_MAX_WYRMWIND_S, MOVE_MENACING_MOONRAZE_MAELSTROM, MOVE_NEVER_ENDING_NIGHTMARE_P, MOVE_NEVER_ENDING_NIGHTMARE_S, MOVE_OCEANIC_OPERETTA, MOVE_PULVERIZING_PANCAKE, MOVE_SAVAGE_SPIN_OUT_P, MOVE_SAVAGE_SPIN_OUT_S, MOVE_SEARING_SUNRAZE_SMASH, MOVE_SHATTERED_PSYCHE_P, MOVE_SHATTERED_PSYCHE_S, MOVE_SINISTER_ARROW_RAID, MOVE_SOUL_STEALING_7_STAR_STRIKE, MOVE_SPLINTERED_STORMSHARDS, MOVE_STEELYHIT, MOVE_STOKED_SPARKSURFER, MOVE_SUBZERO_SLAMMER_P, MOVE_SUBZERO_SLAMMER_S, MOVE_SUPERSONIC_SKYSTRIKE_P, MOVE_SUPERSONIC_SKYSTRIKE_S, MOVE_TECTONIC_RAGE_P, MOVE_TECTONIC_RAGE_S, MOVE_TWINKLE_TACKLE_P, MOVE_TWINKLE_TACKLE_S.

## Appendix E — every relevant Ability

| Identity | Class | Local representation | Name string evidence | Hook |
| --- | --- | --- | --- | --- |
| adaptability | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ADAPTABILITY / 0x58 | True | none |
| aerilate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_AERILATE / 0x89 | True | none |
| aftermath | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_AFTERMATH / 0x77 | True | none |
| airlock | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CLOUDNINE / 0xD | True | none |
| analytic | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ANALYTIC / 0x7D | True | none |
| angerpoint | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ANGERPOINT / 0xBB | True | none |
| angershell | ALIAS_PLUS_HOOK | ABILITY_ANGERSHELL / ABILITY_WEAKARMOR | True | SpeciesHasAngerShell |
| anticipation | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ANTICIPATION / 0xBC | True | none |
| arenatrap | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ARENATRAP / 0x47 | True | none |
| armortail | ALIAS_PLUS_HOOK | ABILITY_ARMORTAIL / ABILITY_DAZZLING | True | SpeciesHasArmorTail |
| aromaveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_AROMAVEIL / 0xC9 | True | none |
| asoneglastrier | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_ASONE_CHILLING / 0x9A | False | none |
| asonespectrier | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_ASONE_GRIM / 0x99 | False | none |
| aurabreak | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_AURABREAK / 0x86 | True | none |
| baddreams | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BADDREAMS / 0xCE | True | none |
| ballfetch | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BALLFETCH / 0xF0 | True | none |
| battery | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BATTERY / 0xE9 | True | none |
| battlearmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BATTLEARMOR / 0x4 | True | none |
| battlebond | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BATTLEBOND / 0x9C | True | none |
| beadsofruin | ALIAS_PLUS_HOOK | ABILITY_BEADSOFRUIN / ABILITY_STALL | True | SpeciesHasBeadsofRuin |
| beastboost | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BEASTBOOST / 0x9D | True | none |
| berserk | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BERSERK / 0xD8 | True | none |
| bigpecks | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BIGPECKS / 0x59 | True | none |
| blaze | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BLAZE / 0x42 | True | none |
| bulletproof | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_BULLETPROOF / 0x74 | True | none |
| cheekpouch | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CHEEKPOUCH / 0xE4 | True | none |
| chillingneigh | ALIAS_PLUS_HOOK | ABILITY_MOXIE / ABILITY_MOXIE (species name override) | True | none |
| chlorophyll | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CHLOROPHYLL / 0x22 | True | none |
| clearbody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CLEARBODY / 0x1D | True | none |
| cloudnine | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CLOUDNINE / 0xD | True | none |
| colorchange | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_COLORCHANGE / 0x10 | True | none |
| comatose | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_COMATOSE / 0xE7 | True | none |
| commander | MISSING_LOCAL | none / none | False | none |
| competitive | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_COMPETITIVE / 0x8F | True | none |
| compoundeyes | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_COMPOUNDEYES / 0xE | True | none |
| contrary | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CONTRARY / 0xBF | True | none |
| corrosion | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CORROSION / 0x9E | True | none |
| costar | ALIAS_PLUS_HOOK | ABILITY_COSTAR / ABILITY_CURIOUSMEDICINE | True | SpeciesHasCostar |
| cottondown | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_COTTONDOWN / 0xF1 | True | none |
| cudchew | ALIAS_PLUS_HOOK | ABILITY_CUDCHEW / ABILITY_HARVEST | True | SpeciesHasCudChew |
| curiousmedicine | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CURIOUSMEDICINE / 0xEB | True | none |
| cursedbody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CURSEDBODY / 0x78 | True | none |
| cutecharm | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CUTECHARM / 0x38 | True | none |
| damp | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DAMP / 0x6 | True | none |
| dancer | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DANCER / 0xE8 | True | none |
| darkaura | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DARKAURA / 0x84 | True | none |
| dauntlessshield | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DAUNTLESSSHIELD / 0xEF | True | none |
| dazzling | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DAZZLING / 0xDD | True | none |
| defeatist | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DEFEATIST / 0x90 | True | none |
| defiant | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DEFIANT / 0x8E | True | none |
| deltastream | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DELTASTREAM / 0xD6 | True | none |
| desolateland | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DESOLATELAND / 0xD5 | True | none |
| disguise | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DISGUISE / 0x9F | True | none |
| download | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DOWNLOAD / 0x67 | True | none |
| dragonsmaw | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DRAGONSMAW / 0x49 | True | none |
| drizzle | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DRIZZLE / 0x2 | True | none |
| drought | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DROUGHT / 0x46 | True | none |
| dryskin | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DRYSKIN / 0x62 | True | none |
| earlybird | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_EARLYBIRD / 0x30 | True | none |
| eartheater | ALIAS_PLUS_HOOK | ABILITY_EARTHEATER / ABILITY_VOLTABSORB | True | SpeciesHasEarthEater |
| effectspore | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_EFFECTSPORE / 0x1B | True | none |
| electricsurge | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ELECTRICSURGE / 0xB5 | True | none |
| electromorphosis | ALIAS_PLUS_HOOK | ABILITY_ELECTROMORPHOSIS / ABILITY_COLORCHANGE | True | SpeciesHasElectromorphosis |
| embodyaspectcornerstone | MISSING_LOCAL | none / none | False | none |
| embodyaspecthearthflame | MISSING_LOCAL | none / none | False | none |
| embodyaspectteal | MISSING_LOCAL | none / none | False | none |
| embodyaspectwellspring | MISSING_LOCAL | none / none | False | none |
| emergencyexit | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_EMERGENCYEXIT / 0xA0 | True | none |
| fairyaura | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FAIRYAURA / 0x85 | True | none |
| filter | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FILTER / 0x65 | True | none |
| flamebody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLAMEBODY / 0x31 | True | none |
| flareboost | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLAREBOOST / 0x93 | True | none |
| flashfire | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLASHFIRE / 0x12 | True | none |
| flowergift | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLOWERGIFT / 0xCD | True | none |
| flowerveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLOWERVEIL / 0xCA | True | none |
| fluffy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FLUFFY / 0xA1 | True | none |
| forecast | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FORECAST / 0x3B | True | none |
| forewarn | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FOREWARN / 0xBD | True | none |
| friendguard | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FRIENDGUARD / 0xE0 | True | none |
| frisk | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FRISK / 0xBE | True | none |
| fullmetalbody | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_CLEARBODY / 0x1D | True | none |
| furcoat | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FURCOAT / 0x94 | True | none |
| galewings | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GALEWINGS / 0x75 | True | none |
| galvanize | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GALVANIZE / 0xED | True | none |
| gluttony | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GLUTTONY / 0xDE | True | none |
| goodasgold | ALIAS_PLUS_HOOK | ABILITY_GOODASGOLD / ABILITY_CLEARBODY | True | SpeciesHasGoodAsGold |
| gooey | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GOOEY / 0x79 | True | none |
| gorillatactics | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GORILLATACTICS / 0xD7 | True | none |
| grasspelt | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GRASSPELT / 0xBA | True | none |
| grassysurge | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GRASSYSURGE / 0xB6 | True | none |
| grimneigh | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GRIMNEIGH / 0x7B | True | none |
| guarddog | ALIAS_PLUS_HOOK | ABILITY_GUARDDOG / ABILITY_INNERFOCUS | True | SpeciesHasGuardDog |
| gulpmissile | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GULPMISSILE / 0xF3 | True | none |
| guts | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GUTS / 0x3E | True | none |
| hadronengine | ALIAS_PLUS_HOOK | ABILITY_HADRONENGINE / ABILITY_ELECTRICSURGE | True | SpeciesHasHadronEngine |
| harvest | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HARVEST / 0xE1 | True | none |
| healer | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HEALER / 0x6C | True | none |
| heatproof | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HEATPROOF / 0x61 | True | none |
| heavymetal | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HEAVYMETAL / 0xC2 | True | none |
| honeygather | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HONEYGATHER / 0xDF | True | none |
| hospitality | MISSING_LOCAL | none / none | False | none |
| hugepower | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HUGEPOWER / 0x25 | True | none |
| hungerswitch | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HUNGERSWITCH / 0x4C | True | none |
| hustle | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HUSTLE / 0x37 | True | none |
| hydration | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HYDRATION / 0x6B | True | none |
| hypercutter | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HYPERCUTTER / 0x34 | True | none |
| icebody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ICEBODY / 0x69 | True | none |
| iceface | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ICEFACE / 0xFA | True | none |
| icescales | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ICESCALES / 0xF8 | True | none |
| illuminate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ILLUMINATE / 0x23 | True | none |
| illusion | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ILLUSION / 0xE3 | True | none |
| immunity | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_IMMUNITY / 0x11 | True | none |
| imposter | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_IMPOSTER / 0xC5 | True | none |
| infiltrator | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INFILTRATOR / 0x66 | True | none |
| innardsout | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INNARDSOUT / 0xDC | True | none |
| innerfocus | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INNERFOCUS / 0x27 | True | none |
| insomnia | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INSOMNIA / 0xF | True | none |
| intimidate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INTIMIDATE / 0x16 | True | none |
| intrepidsword | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INTREPIDSWORD / 0xEE | True | none |
| ironbarbs | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ROUGHSKIN / 0x18 | True | none |
| ironfist | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_IRONFIST / 0x5D | True | none |
| justified | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_JUSTIFIED / 0xC6 | True | none |
| keeneye | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_KEENEYE / 0x33 | True | none |
| klutz | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_KLUTZ / 0xCC | True | none |
| leafguard | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LEAFGUARD / 0xCB | True | none |
| levitate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LEVITATE / 0x1A | True | none |
| libero | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_PROTEAN / 0x96 | True | none |
| lightmetal | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LIGHTMETAL / 0xC3 | True | none |
| lightningrod | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LIGHTNINGROD / 0x1F | True | none |
| limber | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LIMBER / 0x7 | True | none |
| lingeringaroma | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_UNUSED / 0x4D; CFRU ABILITY_LINGERINGAROMA | True | none |
| liquidooze | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LIQUIDOOZE / 0x40 | True | none |
| liquidvoice | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LIQUIDVOICE / 0xDA | True | none |
| longreach | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_LONGREACH / 0xD9 | True | none |
| magicbounce | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MAGICBOUNCE / 0x5A | True | none |
| magicguard | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MAGICGUARD / 0x73 | True | none |
| magician | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MAGICIAN / 0xD2 | True | none |
| magmaarmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MAGMAARMOR / 0x28 | True | none |
| magnetpull | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MAGNETPULL / 0x2A | True | none |
| marvelscale | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MARVELSCALE / 0x3F | True | none |
| megalauncher | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MEGALAUNCHER / 0x7F | True | none |
| merciless | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MERCILESS / 0xC8 | True | none |
| mimicry | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MIMICRY / 0xFC | True | none |
| mindseye | ALIAS_PLUS_HOOK | ABILITY_MINDSEYE / ABILITY_SCRAPPY | True | SpeciesHasMindsEye |
| minus | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MINUS / 0x3A | True | none |
| mirrorarmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MIRRORARMOR / 0xF2 | True | none |
| mistysurge | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MISTYSURGE / 0xB7 | True | none |
| moldbreaker | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOLDBREAKER / 0x98 | True | none |
| moody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOODY / 0x6A | True | none |
| motordrive | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOTORDRIVE / 0x50 | True | none |
| moxie | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOXIE / 0x76 | True | none |
| multiscale | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MULTISCALE / 0x51 | True | none |
| multitype | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MULTITYPE / 0xB4 | True | none |
| mummy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MUMMY / 0x7A | True | none |
| myceliummight | ALIAS_PLUS_HOOK | ABILITY_MYCELIUMMIGHT / ABILITY_MOLDBREAKER | True | SpeciesHasMyceliumMight |
| naturalcure | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_NATURALCURE / 0x1E | True | none |
| neuroforce | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_NEUROFORCE / 0xEC | True | none |
| neutralizinggas | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_NEUTRALIZINGGAS / 0x4A | False | none |
| noguard | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_NOGUARD / 0x7E | True | none |
| normalize | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_NORMALIZE / 0x8A | True | none |
| oblivious | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_OBLIVIOUS / 0xC | True | none |
| opportunist | ALIAS_APPROXIMATION | ABILITY_OPPORTUNIST / ABILITY_DANCER | True | none |
| orichalcumpulse | ALIAS_PLUS_HOOK | ABILITY_ORICHALCUMPULSE / ABILITY_DROUGHT | True | SpeciesHasOrichalcumPulse |
| overcoat | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_OVERCOAT / 0x72 | True | none |
| overgrow | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_OVERGROW / 0x41 | True | none |
| owntempo | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_OWNTEMPO / 0x14 | True | none |
| parentalbond | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PARENTALBOND / 0x97 | True | none |
| pastelveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PASTELVEIL / 0xFE | True | none |
| perishbody | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PERISHBODY / 0xA3 | True | none |
| pickpocket | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PICKPOCKET / 0xCF | True | none |
| pickup | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PICKUP / 0x35 | True | none |
| pixilate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PIXILATE / 0x88 | True | none |
| plus | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PLUS / 0x39 | True | none |
| poisonheal | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_POISONHEAL / 0x68 | True | none |
| poisonpoint | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_POISONPOINT / 0x26 | True | none |
| poisonpuppeteer | ALIAS_PLUS_HOOK | ABILITY_POISONPUPPETEER / ABILITY_PLUS | True | SpeciesHasPoisonPuppeteer |
| poisontouch | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_POISONTOUCH / 0xD1 | True | none |
| powerconstruct | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_POWERCONSTRUCT / 0xA5 | True | none |
| powerofalchemy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RECEIVER / 0xEA | True | none |
| powerspot | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_POWERSPOT / 0xFB | True | none |
| prankster | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PRANKSTER / 0x57 | True | none |
| pressure | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PRESSURE / 0x2E | True | none |
| primordialsea | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PRIMORDIALSEA / 0xD4 | True | none |
| prismarmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PRISMARMOR / 0xA6 | True | none |
| propellertail | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STALWART / 0xF4 | True | none |
| protean | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PROTEAN / 0x96 | True | none |
| protosynthesis | ALIAS_PLUS_HOOK | ABILITY_PROTOSYNTHESIS / ABILITY_QUARKDRIVE | True | SpeciesHasProtosynthesis |
| psychicsurge | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PSYCHICSURGE / 0xB8 | True | none |
| punkrock | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_PUNKROCK / 0xF6 | True | none |
| purepower | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_HUGEPOWER / 0x25 | True | none |
| purifyingsalt | ALIAS_PLUS_HOOK | ABILITY_PURIFYINGSALT / ABILITY_IMMUNITY | True | SpeciesHasPurifyingSalt |
| quarkdrive | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_QUARKDRIVE / 0xAF | True | none |
| queenlymajesty | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_DAZZLING / 0xDD | True | none |
| quickdraw | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_QUICKDRAW / 0xDB | True | none |
| quickfeet | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_QUICKFEET / 0x70 | True | none |
| raindish | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RAINDISH / 0x2C | True | none |
| rattled | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RATTLED / 0xC7 | True | none |
| receiver | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RECEIVER / 0xEA | True | none |
| reckless | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RECKLESS / 0x5B | True | none |
| refrigerate | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_REFRIGERATE / 0x87 | True | none |
| regenerator | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_REGENERATOR / 0x56 | True | none |
| ripen | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RIPEN / 0xF9 | True | none |
| rivalry | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RIVALRY / 0x5E | True | none |
| rkssystem | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RKS_SYSTEM / 0xA7 | True | none |
| rockhead | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ROCKHEAD / 0x45 | True | none |
| rockypayload | ALIAS_PLUS_HOOK | ABILITY_ROCKYPAYLOAD / ABILITY_STEELWORKER | True | SpeciesHasRockyPayload |
| roughskin | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ROUGHSKIN / 0x18 | True | none |
| runaway | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_RUNAWAY / 0x32 | True | none |
| sandforce | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SANDFORCE / 0x5F | True | none |
| sandrush | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SANDRUSH / 0x7C | True | none |
| sandspit | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SANDSPIT / 0xF7 | True | none |
| sandstream | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SANDSTREAM / 0x2D | True | none |
| sandveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SANDVEIL / 0x8 | True | none |
| sapsipper | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SAPSIPPER / 0x71 | True | none |
| schooling | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SCHOOLING / 0xA8 | True | none |
| scrappy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SCRAPPY / 0x53 | True | none |
| screencleaner | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SCREENCLEANER / 0xFD | True | none |
| seedsower | ALIAS_PLUS_HOOK | ABILITY_SEEDSOWER / ABILITY_GRASSYSURGE | True | SpeciesHasSeedSower |
| serenegrace | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SERENEGRACE / 0x20 | True | none |
| shadowshield | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHADOWSHIELD / 0xA9 | True | none |
| shadowtag | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHADOWTAG / 0x17 | True | none |
| sharpness | ALIAS_PLUS_HOOK | ABILITY_SHARPNESS / ABILITY_STRONGJAW | True | SpeciesHasSharpness |
| shedskin | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHEDSKIN / 0x3D | True | none |
| sheerforce | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHEERFORCE / 0x5C | True | none |
| shellarmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHELLARMOR / 0x4B | True | none |
| shielddust | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHIELDDUST / 0x13 | True | none |
| shieldsdown | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SHIELDSDOWN / 0xAA | True | none |
| simple | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SIMPLE / 0x8C | True | none |
| skilllink | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SKILLLINK / 0x4F | True | none |
| slowstart | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SLOWSTART / 0x91 | True | none |
| slushrush | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SLUSHRUSH / 0xAB | True | none |
| sniper | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SNIPER / 0x55 | True | none |
| snowcloak | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SNOWCLOAK / 0x6D | True | none |
| snowwarning | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SNOWWARNING / 0x6F | True | none |
| solarpower | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SOLARPOWER / 0x60 | True | none |
| solidrock | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_FILTER / 0x65 | True | none |
| soulheart | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SOULHEART / 0xAC | True | none |
| soundproof | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SOUNDPROOF / 0x2B | True | none |
| speedboost | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SPEEDBOOST / 0x3 | True | none |
| stakeout | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STAKEOUT / 0xE6 | True | none |
| stall | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STALL / 0xB3 | True | none |
| stalwart | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STALWART / 0xF4 | True | none |
| stamina | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STAMINA / 0xAD | True | none |
| stancechange | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STANCECHANGE / 0xD3 | True | none |
| static | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STATIC / 0x9 | True | none |
| steadfast | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STEADFAST / 0xC4 | True | none |
| steamengine | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STEAMENGINE / 0xF5 | True | none |
| steelworker | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STEELWORKER / 0xAE | True | none |
| steelyspirit | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STEELYSPIRIT / 0xA2 | True | none |
| stench | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STENCH / 0x1 | True | none |
| stickyhold | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STICKYHOLD / 0x3C | True | none |
| stormdrain | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STORMDRAIN / 0x83 | True | none |
| strongjaw | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STRONGJAW / 0x81 | True | none |
| sturdy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_STURDY / 0x5 | True | none |
| suctioncups | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SUCTIONCUPS / 0x15 | True | none |
| superluck | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SUPERLUCK / 0x54 | True | none |
| supersweetsyrup | ALIAS_PLUS_HOOK | ABILITY_SUPERSWEETSYRUP / ABILITY_INTIMIDATE | True | SpeciesHasSuperSweetSyrup |
| supremeoverlord | ALIAS_PLUS_HOOK | ABILITY_SUPREMEOVERLORD / ABILITY_HUGEPOWER | True | SpeciesHasSupremeOverlord |
| surgesurfer | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SURGESURFER / 0xB9 | True | none |
| swarm | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SWARM / 0x44 | True | none |
| sweetveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SWEETVEIL / 0x4E | True | none |
| swiftswim | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SWIFTSWIM / 0x21 | True | none |
| swordofruin | ALIAS_PLUS_HOOK | ABILITY_SWORDOFRUIN / ABILITY_STALL | True | SpeciesHasSwordofRuin |
| symbiosis | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SYMBIOSIS / 0xE5 | True | none |
| synchronize | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_SYNCHRONIZE / 0x1C | True | none |
| tabletsofruin | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_TABLETOFRUIN / ABILITY_STALL | True | SpeciesHasTabletsofRuin |
| tangledfeet | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TANGLEDFEET / 0x6E | True | none |
| tanglinghair | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_GOOEY / 0x79 | True | none |
| technician | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TECHNICIAN / 0x52 | True | none |
| telepathy | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TELEPATHY / 0xE2 | True | none |
| teraformzero | MISSING_LOCAL | none / none | False | none |
| terashell | NAME_ONLY_OR_BEHAVIOR_BLOCKED | none / none | True | SpeciesHasTeraShell |
| terashift | NAME_ONLY_OR_BEHAVIOR_BLOCKED | none / none | True | SpeciesHasTeraShift |
| teravolt | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOLDBREAKER / 0x98 | True | SpeciesHasTeravolt |
| thermalexchange | ALIAS_PLUS_HOOK | ABILITY_THERMALEXCHANGE / ABILITY_STEAMENGINE | True | SpeciesHasThermalExchange |
| thickfat | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_THICKFAT / 0x2F | True | none |
| tintedlens | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TINTEDLENS / 0x63 | True | none |
| torrent | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TORRENT / 0x43 | True | none |
| toughclaws | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TOUGHCLAWS / 0x80 | True | none |
| toxicboost | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TOXICBOOST / 0x92 | True | none |
| toxicchain | ALIAS_PLUS_HOOK | ABILITY_TOXICCHAIN / ABILITY_POISONTOUCH | True | SpeciesHasToxicChain |
| toxicdebris | ALIAS_PLUS_HOOK | ABILITY_TOXICDEBRIS / ABILITY_POISONPOINT | True | SpeciesHasToxicDebris |
| trace | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TRACE / 0x24 | True | none |
| transistor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TRANSISTOR / 0x48 | True | none |
| triage | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TRIAGE / 0xB0 | True | none |
| truant | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_TRUANT / 0x36 | True | none |
| turboblaze | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_MOLDBREAKER / 0x98 | True | SpeciesHasTurboblaze |
| unaware | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_UNAWARE / 0x8D | True | none |
| unburden | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_UNBURDEN / 0x8B | True | none |
| unnerve | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_UNNERVE / 0xC0 | True | none |
| unseenfist | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_UNSEENFIST / 0x64 | True | none |
| vesselofruin | ALIAS_PLUS_HOOK | ABILITY_VESSELOFRUIN / ABILITY_STALL | True | SpeciesHasVesselofRuin |
| victorystar | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_VICTORYSTAR / 0x82 | True | none |
| vitalspirit | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_INSOMNIA / 0xF | True | none |
| voltabsorb | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_VOLTABSORB / 0xA | True | none |
| wanderingspirit | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WANDERINGSPIRIT / 0xA4 | True | none |
| waterabsorb | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WATERABSORB / 0xB | True | none |
| waterbubble | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WATERBUBBLE / 0xB1 | True | none |
| watercompaction | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WATERCOMPACTION / 0xB2 | True | none |
| waterveil | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WATERVEIL / 0x29 | True | none |
| weakarmor | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WEAKARMOR / 0xC1 | True | none |
| wellbakedbody | ALIAS_PLUS_HOOK | ABILITY_WELLBAKEDBODY / ABILITY_STEAMENGINE | True | SpeciesHasWellBakedBody |
| whitesmoke | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_CLEARBODY / 0x1D | True | none |
| wimpout | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_EMERGENCYEXIT / 0xA0 | True | none |
| windpower | ALIAS_PLUS_HOOK | ABILITY_WINDPOWER / ABILITY_BERSERK | True | SpeciesHasWindPower |
| windrider | ALIAS_PLUS_HOOK | ABILITY_WINDRIDER / ABILITY_ANGERPOINT | True | SpeciesHasWindRider |
| wonderguard | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WONDERGUARD / 0x19 | True | none |
| wonderskin | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_WONDERSKIN / 0x95 | True | none |
| zenmode | NATIVE_BEHAVIOR_SUPPORTED | ABILITY_ZENMODE / 0x9B | True | none |
| zerotohero | NAME_ONLY_OR_BEHAVIOR_BLOCKED | ABILITY_ZEROTOHERO / ABILITY_TORRENT | True | SpeciesHasZerotoHero |

## Appendix F — complete evolution/form exceptions and local edges

| Source target | Class | Reference metadata / source limitation | Local rows / alternative parents |
| --- | --- | --- | --- |
| annihilape | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Use Rage Fist 20 times and level-up","evoType":"other"}; Primeape | [["EVO_MOVE","MOVE_RAGEFIST","SPECIES_ANNIHILAPE","0"]] |
| avalugghisui | ENGINE_TRIGGER_REVIEW | {"evoLevel":37}; Bergmite | [["EVO_LEVEL_HOLD_ITEM","37","SPECIES_AVALUGG_H","ITEM_HISUI_ROCK"]] |
| barbaracle | DATA_MISMATCH | {"evoLevel":39}; level/method differs | [["EVO_LEVEL","36","SPECIES_BARBARACLE","0"]] |
| basculegionf | MAPPING_BLOCK | {}; Basculin-White-Striped | [] |
| brambleghast | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Walk 1000 steps in Let's Go","evoType":"other"}; Bramblin | [["EVO_FRIENDSHIP","1000","SPECIES_BRAMBLEGHAST","0"]] |
| braviary | DATA_MISMATCH | {"evoLevel":54}; level/method differs | [["EVO_LEVEL","50","SPECIES_BRAVIARY","0"]] |
| braviaryhisui | DATA_MISMATCH | {"evoLevel":54}; level/method differs | [["EVO_LEVEL_HOLD_ITEM","50","SPECIES_BRAVIARY_H","ITEM_HISUI_ROCK"]] |
| cascoon | ENGINE_TRIGGER_REVIEW | {"evoLevel":7}; Wurmple | [["EVO_LEVEL_CASCOON","7","SPECIES_CASCOON","0"]] |
| decidueyehisui | DATA_MISMATCH | {"evoLevel":36}; level/method differs | [["EVO_LEVEL_HOLD_ITEM","34","SPECIES_DECIDUEYE_H","ITEM_HISUI_ROCK"]] |
| exeggutoralola | PROJECT_POLICY | {"evoItem":"Leaf Stone","evoRegion":"Alola","evoType":"useItem"}; relationship represented through alternate local parent | {"SPECIES_EXEGGCUTE_A":[["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_EXEGGUTOR_A","0"]]} |
| gholdengo | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Level up with 999 Coins in the bag","evoType":"other"}; Gimmighoul | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| glalie | DATA_MISMATCH | {"evoLevel":42}; level/method differs | [["EVO_LEVEL","30","SPECIES_GLALIE","0"]] |
| goodra | ENGINE_TRIGGER_REVIEW | {"evoCondition":"during rain","evoLevel":50}; Sliggoo | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA","0"]] |
| goodrahisui | ENGINE_TRIGGER_REVIEW | {"evoCondition":"during rain","evoLevel":50}; Sliggoo-Hisui | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA_H","0"]] |
| kingambit | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Defeat 3 Bisharp leading Pawniard and level-up","evoType":"other"}; Bisharp | [["EVO_ITEM","ITEM_LEADERS_CREST","SPECIES_KINGAMBIT","0"]] |
| klang | DATA_MISMATCH | {"evoLevel":38}; level/method differs | [["EVO_LEVEL","35","SPECIES_KLANG","0"]] |
| klinklang | DATA_MISMATCH | {"evoLevel":49}; level/method differs | [["EVO_LEVEL","45","SPECIES_KLINKLANG","0"]] |
| lunala | ENGINE_TRIGGER_REVIEW | {"evoLevel":53}; Cosmoem | [["EVO_LEVEL_NIGHT","53","SPECIES_LUNALA","0"]] |
| lycanrocdusk | MAPPING_BLOCK | {}; Rockruff-Dusk | [] |
| magcargo | DATA_MISMATCH | {"evoLevel":38}; level/method differs | [["EVO_LEVEL","30","SPECIES_MAGCARGO","0"]] |
| malamar | ENGINE_TRIGGER_REVIEW | {"evoCondition":"with the console turned upside-down","evoLevel":30}; Inkay | [["EVO_LEVEL","30","SPECIES_MALAMAR","0"]] |
| mandibuzz | DATA_MISMATCH | {"evoLevel":54}; level/method differs | [["EVO_LEVEL","50","SPECIES_MANDIBUZZ","0"]] |
| marowak | ENGINE_TRIGGER_REVIEW | {"evoLevel":28}; Cubone | [["EVO_LEVEL_DAY","28","SPECIES_MAROWAK","0"]] |
| maushold | ENGINE_TRIGGER_REVIEW | {"evoLevel":25}; Tandemaus | [["EVO_MAUSHOLD_THREE","25","SPECIES_MAUSHOLD","0"]] |
| mausholdfour | ENGINE_TRIGGER_REVIEW | {"evoLevel":25}; Tandemaus | [["EVO_MAUSHOLD_FOUR","25","SPECIES_MAUSHOLD_FOUR","0"]] |
| meowstic | ENGINE_TRIGGER_REVIEW | {"evoLevel":25}; Espurr | [["EVO_MALE_LEVEL","25","SPECIES_MEOWSTIC","0"]] |
| meowsticf | ENGINE_TRIGGER_REVIEW | {"evoLevel":25}; Espurr | [["EVO_FEMALE_LEVEL","25","SPECIES_MEOWSTIC_FEMALE","0"]] |
| mienshao | DATA_MISMATCH | {"evoLevel":50}; level/method differs | [["EVO_LEVEL","46","SPECIES_MIENSHAO","0"]] |
| mothim | ENGINE_TRIGGER_REVIEW | {"evoLevel":20}; Burmy | [["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| mrmimegalar | PROJECT_POLICY | {"evoMove":"Mimic","evoRegion":"Galar","evoType":"levelMove"}; relationship represented through alternate local parent | {"SPECIES_MIME_JR_G":[["EVO_MOVE","MOVE_MIMIC","SPECIES_MR_MIME_G","0"]]} |
| ninjask | ENGINE_TRIGGER_REVIEW | {"evoLevel":20}; Nincada | [["EVO_LEVEL_NINJASK","20","SPECIES_NINJASK","0"]] |
| oinkologne | ENGINE_TRIGGER_REVIEW | {"evoLevel":18}; Lechonk | [["EVO_MALE_LEVEL","18","SPECIES_OINKOLOGNE","0"]] |
| oinkolognef | ENGINE_TRIGGER_REVIEW | {"evoLevel":18}; Lechonk | [["EVO_FEMALE_LEVEL","18","SPECIES_OINKOLOGNE_FEMALE","0"]] |
| overqwil | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Use Strong style Barb Barrage 20 times","evoType":"other"}; Qwilfish-Hisui | [["EVO_MOVE","MOVE_BARBBARRAGE","SPECIES_OVERQWIL","0"]] |
| pawmot | ENGINE_TRIGGER_REVIEW | {"evoCondition":"walk 1000 steps in Let's Go","evoType":"other"}; Pawmo | [["EVO_FRIENDSHIP","0","SPECIES_PAWMOT","0"]] |
| probopass | ENGINE_TRIGGER_REVIEW | {"evoCondition":"near a special magnetic field","evoType":"levelExtra"}; Nosepass | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_PROBOPASS","0"],["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_PROBOPASS","0"]] |
| purugly | DATA_MISMATCH | {"evoLevel":38}; level/method differs | [["EVO_LEVEL","34","SPECIES_PURUGLY","0"]] |
| rabsca | ENGINE_TRIGGER_REVIEW | {"evoCondition":"walk 1000 steps in Let's Go","evoType":"other"}; Rellor | [["EVO_FRIENDSHIP","0","SPECIES_RABSCA","0"]] |
| runerigus | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Have 49+ HP lost and walk under stone sculpture in Dusty Bowl","evoType":"other"}; Yamask-Galar | [["EVO_LEVEL","35","SPECIES_RUNERIGUS","0"]] |
| salazzle | ENGINE_TRIGGER_REVIEW | {"evoLevel":33}; Salandit | [["EVO_FEMALE_LEVEL","33","SPECIES_SALAZZLE","0"]] |
| samurotthisui | ENGINE_TRIGGER_REVIEW | {"evoLevel":36}; Dewott | [["EVO_LEVEL_HOLD_ITEM","36","SPECIES_SAMUROTT_H","ITEM_HISUI_ROCK"]] |
| shedinja | ENGINE_TRIGGER_REVIEW | {"evoLevel":20}; Nincada | [["EVO_LEVEL_SHEDINJA","20","SPECIES_SHEDINJA","0"]] |
| silcoon | ENGINE_TRIGGER_REVIEW | {"evoLevel":7}; Wurmple | [["EVO_LEVEL_SILCOON","7","SPECIES_SILCOON","0"]] |
| sirfetchd | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Land 3 critical hits in 1 battle","evoType":"other"}; Farfetch’d-Galar | [["EVO_CRITICAL_HIT","0","SPECIES_SIRFETCHD","0"]] |
| sliggoohisui | ENGINE_TRIGGER_REVIEW | {"evoLevel":40}; Goomy | [["EVO_LEVEL_HOLD_ITEM","40","SPECIES_SLIGGOO_H","ITEM_HISUI_ROCK"]] |
| solgaleo | ENGINE_TRIGGER_REVIEW | {"evoLevel":53}; Cosmoem | [["EVO_LEVEL_DAY","53","SPECIES_SOLGALEO","0"]] |
| swanna | DATA_MISMATCH | {"evoLevel":35}; level/method differs | [["EVO_LEVEL","30","SPECIES_SWANNA","0"]] |
| sylveon | ENGINE_TRIGGER_REVIEW | {"evoCondition":"with a Fairy-type move and two levels of Affection","evoType":"levelExtra"}; Eevee | [["EVO_MOVE_TYPE","TYPE_FAIRY","SPECIES_SYLVEON","TRUE"]] |
| toxtricity | ENGINE_TRIGGER_REVIEW | {"evoLevel":30}; Toxel | [["EVO_NATURE_HIGH","30","SPECIES_TOXTRICITY","0"]] |
| toxtricitylowkey | ENGINE_TRIGGER_REVIEW | {"evoLevel":30}; Toxel | [["EVO_NATURE_LOW","30","SPECIES_TOXTRICITY_LOW_KEY","0"]] |
| typhlosionhisui | ENGINE_TRIGGER_REVIEW | {"evoLevel":36}; Quilava | [["EVO_LEVEL_HOLD_ITEM","36","SPECIES_TYPHLOSION_H","ITEM_HISUI_ROCK"]] |
| tyranitar | DATA_MISMATCH | {"evoLevel":55}; level/method differs | [["EVO_LEVEL","48","SPECIES_TYRANITAR","0"]] |
| ursaluna | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Peat Block when there's a full moon","evoType":"other"}; Ursaring | [["EVO_ITEM_NIGHT","ITEM_PEAT_BLOCK","SPECIES_URSALUNA","0"]] |
| urshifu | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Defeat the Single Strike Tower","evoType":"other"}; Kubfu | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_URSHIFU_SINGLE","0"]] |
| urshifurapidstrike | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Defeat the Rapid Strike Tower","evoType":"other"}; Kubfu | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_URSHIFU_RAPID","0"]] |
| vanillish | DATA_MISMATCH | {"evoLevel":35}; level/method differs | [["EVO_LEVEL","24","SPECIES_VANILLISH","0"]] |
| vanilluxe | DATA_MISMATCH | {"evoLevel":47}; level/method differs | [["EVO_LEVEL","42","SPECIES_VANILLUXE","0"]] |
| vespiquen | ENGINE_TRIGGER_REVIEW | {"evoLevel":21}; Combee | [["EVO_FEMALE_LEVEL","21","SPECIES_VESPIQUEN","0"]] |
| vivillonfancy | UNVERIFIABLE_FROM_SELECTED_REFERENCE | {"evoLevel":12}; form/event vs ordinary evolution ownership; no reviewed evolution-form policy | [] |
| weezinggalar | PROJECT_POLICY | {"evoLevel":35,"evoRegion":"Galar"}; relationship represented through alternate local parent | {"SPECIES_KOFFING_G":[["EVO_LEVEL","35","SPECIES_WEEZING_G","0"]]} |
| wormadam | ENGINE_TRIGGER_REVIEW | {"evoLevel":20}; Burmy | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM","0"]] |
| wormadamsandy | PROJECT_POLICY | {"evoLevel":20}; relationship represented through alternate local parent | {"SPECIES_BURMY_SANDY":[["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_SANDY","0"]]} |
| wormadamtrash | PROJECT_POLICY | {"evoLevel":20}; relationship represented through alternate local parent | {"SPECIES_BURMY_TRASH":[["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_TRASH","0"]]} |
| wyrdeer | ENGINE_TRIGGER_REVIEW | {"evoCondition":"Use Agile style Psyshield Bash 20 times","evoType":"other"}; Stantler | [["EVO_MOVE","MOVE_PSYSHIELDBASH","SPECIES_WYRDEER","0"]] |

Local methods with no CFRU evolution case:

| Parent | Rows |
| --- | --- |
| SPECIES_GIMMIGHOUL | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_GIMMIGHOUL_ROAMING | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_TANDEMAUS | [["EVO_MAUSHOLD_THREE","25","SPECIES_MAUSHOLD","0"],["EVO_MAUSHOLD_FOUR","25","SPECIES_MAUSHOLD_FOUR","0"]] |

All ordinary local source edges are listed to expose additional project substitutions beyond the selected-reference direction. Rows are method, parameter, target and auxiliary field; these are sanitized local source evidence, not artifact readback.

| Local parent | Nonbattle rows |
| --- | --- |
| SPECIES_ABRA | [["EVO_LEVEL","16","SPECIES_KADABRA","0"]] |
| SPECIES_AIPOM | [["EVO_MOVE","MOVE_DOUBLEHIT","SPECIES_AMBIPOM","0"]] |
| SPECIES_AMAURA | [["EVO_LEVEL_NIGHT","39","SPECIES_AURORUS","0"]] |
| SPECIES_ANORITH | [["EVO_LEVEL","40","SPECIES_ARMALDO","0"]] |
| SPECIES_APPLIN | [["EVO_ITEM","ITEM_TART_APPLE","SPECIES_FLAPPLE","0"],["EVO_ITEM","ITEM_SWEET_APPLE","SPECIES_APPLETUN","0"],["EVO_ITEM","ITEM_SYRUPY_APPLE","SPECIES_DIPPLIN","0"]] |
| SPECIES_ARCHEN | [["EVO_LEVEL","37","SPECIES_ARCHEOPS","0"]] |
| SPECIES_ARCTIBAX | [["EVO_LEVEL","54","SPECIES_BAXCALIBUR","0"]] |
| SPECIES_ARON | [["EVO_LEVEL","32","SPECIES_LAIRON","0"]] |
| SPECIES_ARROKUDA | [["EVO_LEVEL","26","SPECIES_BARRASKEWDA","0"]] |
| SPECIES_AXEW | [["EVO_LEVEL","38","SPECIES_FRAXURE","0"]] |
| SPECIES_AZURILL | [["EVO_FRIENDSHIP","0","SPECIES_MARILL","0"]] |
| SPECIES_BAGON | [["EVO_LEVEL","30","SPECIES_SHELGON","0"]] |
| SPECIES_BALTOY | [["EVO_LEVEL","36","SPECIES_CLAYDOL","0"]] |
| SPECIES_BARBOACH | [["EVO_LEVEL","30","SPECIES_WHISCASH","0"]] |
| SPECIES_BASCULIN_H | [["EVO_MOVE_MALE","MOVE_WAVECRASH","SPECIES_BASCULEGION_M","0"],["EVO_MOVE_FEMALE","MOVE_WAVECRASH","SPECIES_BASCULEGION_F","0"]] |
| SPECIES_BAYLEEF | [["EVO_LEVEL","32","SPECIES_MEGANIUM","0"]] |
| SPECIES_BELDUM | [["EVO_LEVEL","20","SPECIES_METANG","0"]] |
| SPECIES_BELLSPROUT | [["EVO_LEVEL","21","SPECIES_WEEPINBELL","0"]] |
| SPECIES_BERGMITE | [["EVO_LEVEL","37","SPECIES_AVALUGG","0"],["EVO_LEVEL_HOLD_ITEM","37","SPECIES_AVALUGG_H","ITEM_HISUI_ROCK"]] |
| SPECIES_BIDOOF | [["EVO_LEVEL","15","SPECIES_BIBAREL","0"]] |
| SPECIES_BINACLE | [["EVO_LEVEL","36","SPECIES_BARBARACLE","0"]] |
| SPECIES_BISHARP | [["EVO_ITEM","ITEM_LEADERS_CREST","SPECIES_KINGAMBIT","0"]] |
| SPECIES_BLIPBUG | [["EVO_LEVEL","10","SPECIES_DOTTLER","0"]] |
| SPECIES_BLITZLE | [["EVO_LEVEL","27","SPECIES_ZEBSTRIKA","0"]] |
| SPECIES_BOLDORE | [["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GIGALITH","0"],["EVO_TRADE","0","SPECIES_GIGALITH","0"]] |
| SPECIES_BONSLY | [["EVO_MOVE","MOVE_MIMIC","SPECIES_SUDOWOODO","0"]] |
| SPECIES_BOUNSWEET | [["EVO_LEVEL","18","SPECIES_STEENEE","0"]] |
| SPECIES_BRAIXEN | [["EVO_LEVEL","36","SPECIES_DELPHOX","0"]] |
| SPECIES_BRAMBLIN | [["EVO_FRIENDSHIP","1000","SPECIES_BRAMBLEGHAST","0"]] |
| SPECIES_BRIONNE | [["EVO_LEVEL","34","SPECIES_PRIMARINA","0"]] |
| SPECIES_BRONZOR | [["EVO_LEVEL","33","SPECIES_BRONZONG","0"]] |
| SPECIES_BUDEW | [["EVO_FRIENDSHIP_DAY","0","SPECIES_ROSELIA","0"]] |
| SPECIES_BUIZEL | [["EVO_LEVEL","26","SPECIES_FLOATZEL","0"]] |
| SPECIES_BULBASAUR | [["EVO_LEVEL","16","SPECIES_IVYSAUR","0"]] |
| SPECIES_BUNEARY | [["EVO_FRIENDSHIP","0","SPECIES_LOPUNNY","0"]] |
| SPECIES_BUNNELBY | [["EVO_LEVEL","20","SPECIES_DIGGERSBY","0"]] |
| SPECIES_BURMY | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_BURMY_SANDY | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_SANDY","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_BURMY_TRASH | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_TRASH","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_CACNEA | [["EVO_LEVEL","32","SPECIES_CACTURNE","0"]] |
| SPECIES_CAPSAKID | [["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_SCOVILLAIN","0"]] |
| SPECIES_CARKOL | [["EVO_LEVEL","34","SPECIES_COALOSSAL","0"]] |
| SPECIES_CARVANHA | [["EVO_LEVEL","30","SPECIES_SHARPEDO","0"]] |
| SPECIES_CASCOON | [["EVO_LEVEL","10","SPECIES_DUSTOX","0"]] |
| SPECIES_CATERPIE | [["EVO_LEVEL","7","SPECIES_METAPOD","0"]] |
| SPECIES_CETODDLE | [["EVO_ITEM","ITEM_ICE_STONE","SPECIES_CETITAN","0"]] |
| SPECIES_CHANSEY | [["EVO_FRIENDSHIP","0","SPECIES_BLISSEY","0"]] |
| SPECIES_CHARCADET | [["EVO_ITEM","ITEM_AUSPICIOUS_ARMOR","SPECIES_ARMAROUGE","0"],["EVO_ITEM","ITEM_MALICIOUS_ARMOR","SPECIES_CERULEDGE","0"]] |
| SPECIES_CHARJABUG | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_VIKAVOLT","0"],["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_VIKAVOLT","0"]] |
| SPECIES_CHARMANDER | [["EVO_LEVEL","16","SPECIES_CHARMELEON","0"]] |
| SPECIES_CHARMELEON | [["EVO_LEVEL","36","SPECIES_CHARIZARD","0"]] |
| SPECIES_CHERUBI | [["EVO_LEVEL","25","SPECIES_CHERRIM","0"]] |
| SPECIES_CHESPIN | [["EVO_LEVEL","16","SPECIES_QUILLADIN","0"]] |
| SPECIES_CHEWTLE | [["EVO_LEVEL","22","SPECIES_DREDNAW","0"]] |
| SPECIES_CHIKORITA | [["EVO_LEVEL","16","SPECIES_BAYLEEF","0"]] |
| SPECIES_CHIMCHAR | [["EVO_LEVEL","14","SPECIES_MONFERNO","0"]] |
| SPECIES_CHINCHOU | [["EVO_LEVEL","27","SPECIES_LANTURN","0"]] |
| SPECIES_CHINGLING | [["EVO_FRIENDSHIP_NIGHT","0","SPECIES_CHIMECHO","0"]] |
| SPECIES_CLAMPERL | [["EVO_ITEM","ITEM_DEEP_SEA_TOOTH","SPECIES_HUNTAIL","0"],["EVO_ITEM","ITEM_DEEP_SEA_SCALE","SPECIES_GOREBYSS","0"],["EVO_TRADE_ITEM","ITEM_DEEP_SEA_TOOTH","SPECIES_HUNTAIL","0"],["EVO_TRADE_ITEM","ITEM_DEEP_SEA_SCALE","SPECIES_GOREBYSS","0"]] |
| SPECIES_CLAUNCHER | [["EVO_LEVEL","37","SPECIES_CLAWITZER","0"]] |
| SPECIES_CLEFAIRY | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_CLEFABLE","0"]] |
| SPECIES_CLEFFA | [["EVO_FRIENDSHIP","0","SPECIES_CLEFAIRY","0"]] |
| SPECIES_CLOBBOPUS | [["EVO_MOVE","MOVE_TAUNT","SPECIES_GRAPPLOCT","0"]] |
| SPECIES_COMBEE | [["EVO_FEMALE_LEVEL","21","SPECIES_VESPIQUEN","0"]] |
| SPECIES_COMBUSKEN | [["EVO_LEVEL","36","SPECIES_BLAZIKEN","0"]] |
| SPECIES_CORPHISH | [["EVO_LEVEL","30","SPECIES_CRAWDAUNT","0"]] |
| SPECIES_CORSOLA_G | [["EVO_LEVEL","38","SPECIES_CURSOLA","0"]] |
| SPECIES_CORVISQUIRE | [["EVO_LEVEL","38","SPECIES_CORVIKNIGHT","0"]] |
| SPECIES_COSMOEM | [["EVO_LEVEL_DAY","53","SPECIES_SOLGALEO","0"],["EVO_LEVEL_NIGHT","53","SPECIES_LUNALA","0"]] |
| SPECIES_COSMOG | [["EVO_LEVEL","43","SPECIES_COSMOEM","0"]] |
| SPECIES_COTTONEE | [["EVO_ITEM","ITEM_SUN_STONE","SPECIES_WHIMSICOTT","0"]] |
| SPECIES_CRABRAWLER | [["EVO_ITEM","ITEM_ICE_STONE","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_FROST_MOUNTAIN","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_ROUTE_8","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_BLIZZARD_CITY","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_FROZEN_FOREST","SPECIES_CRABOMINABLE","0"]] |
| SPECIES_CRANIDOS | [["EVO_LEVEL","30","SPECIES_RAMPARDOS","0"]] |
| SPECIES_CROAGUNK | [["EVO_LEVEL","37","SPECIES_TOXICROAK","0"]] |
| SPECIES_CROCALOR | [["EVO_LEVEL","36","SPECIES_SKELEDIRGE","0"]] |
| SPECIES_CROCONAW | [["EVO_LEVEL","30","SPECIES_FERALIGATR","0"]] |
| SPECIES_CUBCHOO | [["EVO_LEVEL","37","SPECIES_BEARTIC","0"]] |
| SPECIES_CUBONE | [["EVO_LEVEL_DAY","28","SPECIES_MAROWAK","0"],["EVO_LEVEL_NIGHT","28","SPECIES_MAROWAK_A","0"]] |
| SPECIES_CUBONE_A | [["EVO_LEVEL_NIGHT","28","SPECIES_MAROWAK_A","0"]] |
| SPECIES_CUFANT | [["EVO_LEVEL","34","SPECIES_COPPERAJAH","0"]] |
| SPECIES_CUTIEFLY | [["EVO_LEVEL","25","SPECIES_RIBOMBEE","0"]] |
| SPECIES_CYNDAQUIL | [["EVO_LEVEL","14","SPECIES_QUILAVA","0"]] |
| SPECIES_DARTRIX | [["EVO_LEVEL","34","SPECIES_DECIDUEYE","0"],["EVO_LEVEL_HOLD_ITEM","34","SPECIES_DECIDUEYE_H","ITEM_HISUI_ROCK"]] |
| SPECIES_DARUMAKA | [["EVO_LEVEL","35","SPECIES_DARMANITAN","0"]] |
| SPECIES_DARUMAKA_G | [["EVO_ITEM","ITEM_ICE_STONE","SPECIES_DARMANITAN_G","0"]] |
| SPECIES_DEERLING | [["EVO_LEVEL","34","SPECIES_SAWSBUCK","0"]] |
| SPECIES_DEERLING_AUTUMN | [["EVO_LEVEL","34","SPECIES_SAWSBUCK_AUTUMN","0"]] |
| SPECIES_DEERLING_SUMMER | [["EVO_LEVEL","34","SPECIES_SAWSBUCK_SUMMER","0"]] |
| SPECIES_DEERLING_WINTER | [["EVO_LEVEL","34","SPECIES_SAWSBUCK_WINTER","0"]] |
| SPECIES_DEINO | [["EVO_LEVEL","50","SPECIES_ZWEILOUS","0"]] |
| SPECIES_DEWOTT | [["EVO_LEVEL","36","SPECIES_SAMUROTT","0"],["EVO_LEVEL_HOLD_ITEM","36","SPECIES_SAMUROTT_H","ITEM_HISUI_ROCK"]] |
| SPECIES_DEWPIDER | [["EVO_LEVEL","22","SPECIES_ARAQUANID","0"]] |
| SPECIES_DIGLETT | [["EVO_LEVEL","26","SPECIES_DUGTRIO","0"]] |
| SPECIES_DIGLETT_A | [["EVO_LEVEL","26","SPECIES_DUGTRIO_A","0"]] |
| SPECIES_DIPPLIN | [["EVO_MOVE","MOVE_DRAGONCHEER","SPECIES_HYDRAPPLE","0"]] |
| SPECIES_DODUO | [["EVO_LEVEL","31","SPECIES_DODRIO","0"]] |
| SPECIES_DOLLIV | [["EVO_LEVEL","35","SPECIES_ARBOLIVA","0"]] |
| SPECIES_DOTTLER | [["EVO_LEVEL","30","SPECIES_ORBEETLE","0"]] |
| SPECIES_DOUBLADE | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_AEGISLASH","0"]] |
| SPECIES_DRAGONAIR | [["EVO_LEVEL","55","SPECIES_DRAGONITE","0"]] |
| SPECIES_DRAKLOAK | [["EVO_LEVEL","60","SPECIES_DRAGAPULT","0"]] |
| SPECIES_DRATINI | [["EVO_LEVEL","30","SPECIES_DRAGONAIR","0"]] |
| SPECIES_DREEPY | [["EVO_LEVEL","50","SPECIES_DRAKLOAK","0"]] |
| SPECIES_DRIFLOON | [["EVO_LEVEL","28","SPECIES_DRIFBLIM","0"]] |
| SPECIES_DRILBUR | [["EVO_LEVEL","31","SPECIES_EXCADRILL","0"]] |
| SPECIES_DRIZZILE | [["EVO_LEVEL","35","SPECIES_INTELEON","0"]] |
| SPECIES_DROWZEE | [["EVO_LEVEL","26","SPECIES_HYPNO","0"]] |
| SPECIES_DUCKLETT | [["EVO_LEVEL","30","SPECIES_SWANNA","0"]] |
| SPECIES_DUNSPARCE | [["EVO_MOVE","MOVE_HYPERDRILL","SPECIES_DUDUNSPARCE","0"],["EVO_MOVE","MOVE_HYPERDRILL","SPECIES_DUDUNSPARCE_THREE","100"]] |
| SPECIES_DUOSION | [["EVO_LEVEL","41","SPECIES_REUNICLUS","0"]] |
| SPECIES_DURALUDON | [["EVO_ITEM","ITEM_METAL_ALLOY","SPECIES_ARCHALUDON","0"]] |
| SPECIES_DUSCLOPS | [["EVO_ITEM","ITEM_REAPER_CLOTH","SPECIES_DUSKNOIR","0"],["EVO_TRADE_ITEM","ITEM_REAPER_CLOTH","SPECIES_DUSKNOIR","0"]] |
| SPECIES_DUSKULL | [["EVO_LEVEL","37","SPECIES_DUSCLOPS","0"]] |
| SPECIES_DWEBBLE | [["EVO_LEVEL","34","SPECIES_CRUSTLE","0"]] |
| SPECIES_EELEKTRIK | [["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_EELEKTROSS","0"]] |
| SPECIES_EEVEE | [["EVO_FRIENDSHIP_DAY","0","SPECIES_ESPEON","0"],["EVO_FRIENDSHIP_NIGHT","0","SPECIES_UMBREON","0"],["EVO_MOVE_TYPE","TYPE_FAIRY","SPECIES_SYLVEON","TRUE"],["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_FLAREON","0"],["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_JOLTEON","0"],["EVO_ITEM","ITEM_WATER_STONE","SPECIES_VAPOREON","0"],["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_LEAFEON","0"],["EVO_ITEM","ITEM_ICE_STONE","SPECIES_GLACEON","0"]] |
| SPECIES_EKANS | [["EVO_LEVEL","22","SPECIES_ARBOK","0"]] |
| SPECIES_ELECTABUZZ | [["EVO_ITEM","ITEM_ELECTIRIZER","SPECIES_ELECTIVIRE","0"],["EVO_TRADE_ITEM","ITEM_ELECTIRIZER","SPECIES_ELECTIVIRE","0"]] |
| SPECIES_ELECTRIKE | [["EVO_LEVEL","26","SPECIES_MANECTRIC","0"]] |
| SPECIES_ELEKID | [["EVO_LEVEL","30","SPECIES_ELECTABUZZ","0"]] |
| SPECIES_ELGYEM | [["EVO_LEVEL","42","SPECIES_BEHEEYEM","0"]] |
| SPECIES_ESPURR | [["EVO_MALE_LEVEL","25","SPECIES_MEOWSTIC","0"],["EVO_FEMALE_LEVEL","25","SPECIES_MEOWSTIC_FEMALE","0"]] |
| SPECIES_EXEGGCUTE | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_EXEGGUTOR","0"]] |
| SPECIES_EXEGGCUTE_A | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_EXEGGUTOR_A","0"]] |
| SPECIES_FARFETCHD_G | [["EVO_CRITICAL_HIT","0","SPECIES_SIRFETCHD","0"]] |
| SPECIES_FEEBAS | [["EVO_ITEM","ITEM_PRISM_SCALE","SPECIES_MILOTIC","0"],["EVO_TRADE_ITEM","ITEM_PRISM_SCALE","SPECIES_MILOTIC","0"]] |
| SPECIES_FENNEKIN | [["EVO_LEVEL","16","SPECIES_BRAIXEN","0"]] |
| SPECIES_FERROSEED | [["EVO_LEVEL","40","SPECIES_FERROTHORN","0"]] |
| SPECIES_FIDOUGH | [["EVO_LEVEL","26","SPECIES_DACHSBUN","0"]] |
| SPECIES_FINIZEN | [["EVO_LEVEL","38","SPECIES_PALAFIN","0"]] |
| SPECIES_FINNEON | [["EVO_LEVEL","31","SPECIES_LUMINEON","0"]] |
| SPECIES_FLAAFFY | [["EVO_LEVEL","30","SPECIES_AMPHAROS","0"]] |
| SPECIES_FLABEBE | [["EVO_LEVEL","19","SPECIES_FLOETTE","0"]] |
| SPECIES_FLABEBE_BLUE | [["EVO_LEVEL","19","SPECIES_FLOETTE_BLUE","0"]] |
| SPECIES_FLABEBE_ORANGE | [["EVO_LEVEL","19","SPECIES_FLOETTE_ORANGE","0"]] |
| SPECIES_FLABEBE_WHITE | [["EVO_LEVEL","19","SPECIES_FLOETTE_WHITE","0"]] |
| SPECIES_FLABEBE_YELLOW | [["EVO_LEVEL","19","SPECIES_FLOETTE_YELLOW","0"]] |
| SPECIES_FLETCHINDER | [["EVO_LEVEL","35","SPECIES_TALONFLAME","0"]] |
| SPECIES_FLETCHLING | [["EVO_LEVEL","17","SPECIES_FLETCHINDER","0"]] |
| SPECIES_FLITTLE | [["EVO_LEVEL","35","SPECIES_ESPATHRA","0"]] |
| SPECIES_FLOETTE | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_FLORGES","0"]] |
| SPECIES_FLOETTE_BLUE | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_FLORGES_BLUE","0"]] |
| SPECIES_FLOETTE_ORANGE | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_FLORGES_ORANGE","0"]] |
| SPECIES_FLOETTE_WHITE | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_FLORGES_WHITE","0"]] |
| SPECIES_FLOETTE_YELLOW | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_FLORGES_YELLOW","0"]] |
| SPECIES_FLORAGATO | [["EVO_LEVEL","36","SPECIES_MEOWSCARADA","0"]] |
| SPECIES_FOMANTIS | [["EVO_LEVEL_DAY","34","SPECIES_LURANTIS","0"]] |
| SPECIES_FOONGUS | [["EVO_LEVEL","39","SPECIES_AMOONGUSS","0"]] |
| SPECIES_FRAXURE | [["EVO_LEVEL","48","SPECIES_HAXORUS","0"]] |
| SPECIES_FRIGIBAX | [["EVO_LEVEL","35","SPECIES_ARCTIBAX","0"]] |
| SPECIES_FRILLISH | [["EVO_LEVEL","40","SPECIES_JELLICENT","0"]] |
| SPECIES_FRILLISH_F | [["EVO_LEVEL","40","SPECIES_JELLICENT_F","0"]] |
| SPECIES_FROAKIE | [["EVO_LEVEL","16","SPECIES_FROGADIER","0"]] |
| SPECIES_FROGADIER | [["EVO_LEVEL","36","SPECIES_GRENINJA","0"]] |
| SPECIES_FUECOCO | [["EVO_LEVEL","16","SPECIES_CROCALOR","0"]] |
| SPECIES_GABITE | [["EVO_LEVEL","48","SPECIES_GARCHOMP","0"]] |
| SPECIES_GASTLY | [["EVO_LEVEL","25","SPECIES_HAUNTER","0"]] |
| SPECIES_GEODUDE | [["EVO_LEVEL","25","SPECIES_GRAVELER","0"]] |
| SPECIES_GEODUDE_A | [["EVO_LEVEL","25","SPECIES_GRAVELER_A","0"]] |
| SPECIES_GIBLE | [["EVO_LEVEL","24","SPECIES_GABITE","0"]] |
| SPECIES_GIMMIGHOUL | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_GIMMIGHOUL_ROAMING | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_GIRAFARIG | [["EVO_MOVE","MOVE_TWINBEAM","SPECIES_FARIGIRAF","0"]] |
| SPECIES_GLAMEOW | [["EVO_LEVEL","34","SPECIES_PURUGLY","0"]] |
| SPECIES_GLIGAR | [["EVO_HOLD_ITEM_NIGHT","ITEM_RAZOR_FANG","SPECIES_GLISCOR","0"]] |
| SPECIES_GLIMMET | [["EVO_LEVEL","35","SPECIES_GLIMMORA","0"]] |
| SPECIES_GLOOM | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_VILEPLUME","0"],["EVO_ITEM","ITEM_SUN_STONE","SPECIES_BELLOSSOM","0"]] |
| SPECIES_GOLBAT | [["EVO_FRIENDSHIP","0","SPECIES_CROBAT","0"]] |
| SPECIES_GOLDEEN | [["EVO_LEVEL","33","SPECIES_SEAKING","0"]] |
| SPECIES_GOLETT | [["EVO_LEVEL","43","SPECIES_GOLURK","0"]] |
| SPECIES_GOOMY | [["EVO_LEVEL","40","SPECIES_SLIGGOO","0"],["EVO_LEVEL_HOLD_ITEM","40","SPECIES_SLIGGOO_H","ITEM_HISUI_ROCK"]] |
| SPECIES_GOSSIFLEUR | [["EVO_LEVEL","20","SPECIES_ELDEGOSS","0"]] |
| SPECIES_GOTHITA | [["EVO_LEVEL","32","SPECIES_GOTHORITA","0"]] |
| SPECIES_GOTHORITA | [["EVO_LEVEL","41","SPECIES_GOTHITELLE","0"]] |
| SPECIES_GRAVELER | [["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOLEM","0"],["EVO_TRADE","0","SPECIES_GOLEM","0"]] |
| SPECIES_GRAVELER_A | [["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOLEM_A","0"],["EVO_TRADE","0","SPECIES_GOLEM_A","0"]] |
| SPECIES_GREAVARD | [["EVO_LEVEL_NIGHT","30","SPECIES_HOUNDSTONE","0"]] |
| SPECIES_GRIMER | [["EVO_LEVEL","38","SPECIES_MUK","0"]] |
| SPECIES_GRIMER_A | [["EVO_LEVEL","38","SPECIES_MUK_A","0"]] |
| SPECIES_GROOKEY | [["EVO_LEVEL","16","SPECIES_THWACKEY","0"]] |
| SPECIES_GROTLE | [["EVO_LEVEL","32","SPECIES_TORTERRA","0"]] |
| SPECIES_GROVYLE | [["EVO_LEVEL","36","SPECIES_SCEPTILE","0"]] |
| SPECIES_GROWLITHE | [["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_ARCANINE","0"]] |
| SPECIES_GROWLITHE_H | [["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_ARCANINE_H","0"]] |
| SPECIES_GRUBBIN | [["EVO_LEVEL","20","SPECIES_CHARJABUG","0"]] |
| SPECIES_GULPIN | [["EVO_LEVEL","26","SPECIES_SWALOT","0"]] |
| SPECIES_GURDURR | [["EVO_TRADE","0","SPECIES_CONKELDURR","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_CONKELDURR","0"]] |
| SPECIES_HAKAMO_O | [["EVO_LEVEL","45","SPECIES_KOMMO_O","0"]] |
| SPECIES_HAPPINY | [["EVO_HOLD_ITEM_DAY","ITEM_OVAL_STONE","SPECIES_CHANSEY","0"]] |
| SPECIES_HATENNA | [["EVO_LEVEL","32","SPECIES_HATTREM","0"]] |
| SPECIES_HATTREM | [["EVO_LEVEL","42","SPECIES_HATTERENE","0"]] |
| SPECIES_HAUNTER | [["EVO_TRADE","0","SPECIES_GENGAR","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GENGAR","0"]] |
| SPECIES_HELIOPTILE | [["EVO_ITEM","ITEM_SUN_STONE","SPECIES_HELIOLISK","0"]] |
| SPECIES_HERDIER | [["EVO_LEVEL","32","SPECIES_STOUTLAND","0"]] |
| SPECIES_HIPPOPOTAS | [["EVO_LEVEL","34","SPECIES_HIPPOWDON","0"]] |
| SPECIES_HIPPOPOTAS_F | [["EVO_LEVEL","34","SPECIES_HIPPOWDON_F","0"]] |
| SPECIES_HONEDGE | [["EVO_LEVEL","35","SPECIES_DOUBLADE","0"]] |
| SPECIES_HOOTHOOT | [["EVO_LEVEL","20","SPECIES_NOCTOWL","0"]] |
| SPECIES_HOPPIP | [["EVO_LEVEL","18","SPECIES_SKIPLOOM","0"]] |
| SPECIES_HORSEA | [["EVO_LEVEL","32","SPECIES_SEADRA","0"]] |
| SPECIES_HOUNDOUR | [["EVO_LEVEL","24","SPECIES_HOUNDOOM","0"]] |
| SPECIES_IGGLYBUFF | [["EVO_FRIENDSHIP","0","SPECIES_JIGGLYPUFF","0"]] |
| SPECIES_IMPIDIMP | [["EVO_LEVEL","32","SPECIES_MORGREM","0"]] |
| SPECIES_INKAY | [["EVO_LEVEL","30","SPECIES_MALAMAR","0"]] |
| SPECIES_IVYSAUR | [["EVO_LEVEL","32","SPECIES_VENUSAUR","0"]] |
| SPECIES_JANGMO_O | [["EVO_LEVEL","35","SPECIES_HAKAMO_O","0"]] |
| SPECIES_JIGGLYPUFF | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_WIGGLYTUFF","0"]] |
| SPECIES_JOLTIK | [["EVO_LEVEL","36","SPECIES_GALVANTULA","0"]] |
| SPECIES_KABUTO | [["EVO_LEVEL","40","SPECIES_KABUTOPS","0"]] |
| SPECIES_KADABRA | [["EVO_TRADE","0","SPECIES_ALAKAZAM","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_ALAKAZAM","0"]] |
| SPECIES_KAKUNA | [["EVO_LEVEL","10","SPECIES_BEEDRILL","0"]] |
| SPECIES_KARRABLAST | [["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_ESCAVALIER","0"],["EVO_TRADE","0","SPECIES_ESCAVALIER","0"]] |
| SPECIES_KIRLIA | [["EVO_LEVEL","30","SPECIES_GARDEVOIR","0"],["EVO_ITEM","ITEM_DAWN_STONE","SPECIES_GALLADE","MON_MALE"]] |
| SPECIES_KLANG | [["EVO_LEVEL","45","SPECIES_KLINKLANG","0"]] |
| SPECIES_KLINK | [["EVO_LEVEL","35","SPECIES_KLANG","0"]] |
| SPECIES_KOFFING | [["EVO_LEVEL","35","SPECIES_WEEZING","0"]] |
| SPECIES_KOFFING_G | [["EVO_LEVEL","35","SPECIES_WEEZING_G","0"]] |
| SPECIES_KRABBY | [["EVO_LEVEL","28","SPECIES_KINGLER","0"]] |
| SPECIES_KRICKETOT | [["EVO_LEVEL","10","SPECIES_KRICKETUNE","0"]] |
| SPECIES_KROKOROK | [["EVO_LEVEL","40","SPECIES_KROOKODILE","0"]] |
| SPECIES_KUBFU | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_URSHIFU_SINGLE","0"],["EVO_ITEM","ITEM_WATER_STONE","SPECIES_URSHIFU_RAPID","0"]] |
| SPECIES_LAIRON | [["EVO_LEVEL","42","SPECIES_AGGRON","0"]] |
| SPECIES_LAMPENT | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_CHANDELURE","0"]] |
| SPECIES_LARVESTA | [["EVO_LEVEL","59","SPECIES_VOLCARONA","0"]] |
| SPECIES_LARVITAR | [["EVO_LEVEL","30","SPECIES_PUPITAR","0"]] |
| SPECIES_LECHONK | [["EVO_MALE_LEVEL","18","SPECIES_OINKOLOGNE","0"],["EVO_FEMALE_LEVEL","18","SPECIES_OINKOLOGNE_FEMALE","0"]] |
| SPECIES_LEDYBA | [["EVO_LEVEL","18","SPECIES_LEDIAN","0"]] |
| SPECIES_LICKITUNG | [["EVO_MOVE","MOVE_ROLLOUT","SPECIES_LICKILICKY","0"]] |
| SPECIES_LILEEP | [["EVO_LEVEL","40","SPECIES_CRADILY","0"]] |
| SPECIES_LILLIPUP | [["EVO_LEVEL","16","SPECIES_HERDIER","0"]] |
| SPECIES_LINOONE_G | [["EVO_LEVEL_NIGHT","35","SPECIES_OBSTAGOON","0"]] |
| SPECIES_LITLEO | [["EVO_LEVEL","35","SPECIES_PYROAR","0"]] |
| SPECIES_LITTEN | [["EVO_LEVEL","17","SPECIES_TORRACAT","0"]] |
| SPECIES_LITWICK | [["EVO_LEVEL","41","SPECIES_LAMPENT","0"]] |
| SPECIES_LOMBRE | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_LUDICOLO","0"]] |
| SPECIES_LOTAD | [["EVO_LEVEL","14","SPECIES_LOMBRE","0"]] |
| SPECIES_LOUDRED | [["EVO_LEVEL","40","SPECIES_EXPLOUD","0"]] |
| SPECIES_LUXIO | [["EVO_LEVEL","30","SPECIES_LUXRAY","0"]] |
| SPECIES_MACHOKE | [["EVO_TRADE","0","SPECIES_MACHAMP","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_MACHAMP","0"]] |
| SPECIES_MACHOP | [["EVO_LEVEL","28","SPECIES_MACHOKE","0"]] |
| SPECIES_MAGBY | [["EVO_LEVEL","30","SPECIES_MAGMAR","0"]] |
| SPECIES_MAGIKARP | [["EVO_LEVEL","20","SPECIES_GYARADOS","0"]] |
| SPECIES_MAGMAR | [["EVO_TRADE_ITEM","ITEM_MAGMARIZER","SPECIES_MAGMORTAR","0"],["EVO_ITEM","ITEM_MAGMARIZER","SPECIES_MAGMORTAR","0"]] |
| SPECIES_MAGNEMITE | [["EVO_LEVEL","30","SPECIES_MAGNETON","0"]] |
| SPECIES_MAGNETON | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_MAGNEZONE","0"],["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_MAGNEZONE","0"]] |
| SPECIES_MAKUHITA | [["EVO_LEVEL","24","SPECIES_HARIYAMA","0"]] |
| SPECIES_MANKEY | [["EVO_LEVEL","28","SPECIES_PRIMEAPE","0"]] |
| SPECIES_MANTYKE | [["EVO_OTHER_PARTY_MON","SPECIES_REMORAID","SPECIES_MANTINE","0"]] |
| SPECIES_MAREANIE | [["EVO_LEVEL","38","SPECIES_TOXAPEX","0"]] |
| SPECIES_MAREEP | [["EVO_LEVEL","15","SPECIES_FLAAFFY","0"]] |
| SPECIES_MARILL | [["EVO_LEVEL","18","SPECIES_AZUMARILL","0"]] |
| SPECIES_MARSHTOMP | [["EVO_LEVEL","36","SPECIES_SWAMPERT","0"]] |
| SPECIES_MASCHIFF | [["EVO_LEVEL","30","SPECIES_MABOSSTIFF","0"]] |
| SPECIES_MEDITITE | [["EVO_LEVEL","37","SPECIES_MEDICHAM","0"]] |
| SPECIES_MELTAN | [["EVO_ITEM","ITEM_METAL_COAT","SPECIES_MELMETAL","0"],["EVO_ITEM","ITEM_METAL_POWDER","SPECIES_MELMETAL","0"]] |
| SPECIES_MEOWTH | [["EVO_LEVEL","28","SPECIES_PERSIAN","0"]] |
| SPECIES_MEOWTH_A | [["EVO_FRIENDSHIP","0","SPECIES_PERSIAN_A","0"]] |
| SPECIES_MEOWTH_G | [["EVO_LEVEL","28","SPECIES_PERRSERKER","0"]] |
| SPECIES_METANG | [["EVO_LEVEL","45","SPECIES_METAGROSS","0"]] |
| SPECIES_METAPOD | [["EVO_LEVEL","10","SPECIES_BUTTERFREE","0"]] |
| SPECIES_MIENFOO | [["EVO_LEVEL","46","SPECIES_MIENSHAO","0"]] |
| SPECIES_MILCERY | [["EVO_ITEM","ITEM_STRAWBERRY_SWEET","SPECIES_ALCREMIE_STRAWBERRY","0"],["EVO_ITEM","ITEM_BERRY_SWEET","SPECIES_ALCREMIE_BERRY","0"],["EVO_ITEM","ITEM_LOVE_SWEET","SPECIES_ALCREMIE_LOVE","0"],["EVO_ITEM","ITEM_CLOVER_SWEET","SPECIES_ALCREMIE_CLOVER","0"],["EVO_ITEM","ITEM_FLOWER_SWEET","SPECIES_ALCREMIE_FLOWER","0"],["EVO_ITEM","ITEM_RIBBON_SWEET","SPECIES_ALCREMIE_RIBBON","0"],["EVO_ITEM","ITEM_STAR_SWEET","SPECIES_ALCREMIE_STAR","0"]] |
| SPECIES_MIME_JR | [["EVO_MOVE","MOVE_MIMIC","SPECIES_MR_MIME","0"]] |
| SPECIES_MIME_JR_G | [["EVO_MOVE","MOVE_MIMIC","SPECIES_MR_MIME_G","0"]] |
| SPECIES_MINCCINO | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_CINCCINO","0"]] |
| SPECIES_MISDREAVUS | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_MISMAGIUS","0"]] |
| SPECIES_MONFERNO | [["EVO_LEVEL","36","SPECIES_INFERNAPE","0"]] |
| SPECIES_MORELULL | [["EVO_LEVEL","24","SPECIES_SHIINOTIC","0"]] |
| SPECIES_MORGREM | [["EVO_LEVEL","42","SPECIES_GRIMMSNARL","0"]] |
| SPECIES_MR_MIME_G | [["EVO_LEVEL","42","SPECIES_MR_RIME","0"]] |
| SPECIES_MUDBRAY | [["EVO_LEVEL","30","SPECIES_MUDSDALE","0"]] |
| SPECIES_MUDKIP | [["EVO_LEVEL","16","SPECIES_MARSHTOMP","0"]] |
| SPECIES_MUNCHLAX | [["EVO_FRIENDSHIP","0","SPECIES_SNORLAX","0"]] |
| SPECIES_MUNNA | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_MUSHARNA","0"]] |
| SPECIES_MURKROW | [["EVO_ITEM","ITEM_DUSK_STONE","SPECIES_HONCHKROW","0"]] |
| SPECIES_NACLI | [["EVO_LEVEL","24","SPECIES_NACLSTACK","0"]] |
| SPECIES_NACLSTACK | [["EVO_LEVEL","38","SPECIES_GARGANACL","0"]] |
| SPECIES_NATU | [["EVO_LEVEL","25","SPECIES_XATU","0"]] |
| SPECIES_NICKIT | [["EVO_LEVEL","18","SPECIES_THIEVUL","0"]] |
| SPECIES_NIDORAN_F | [["EVO_LEVEL","16","SPECIES_NIDORINA","0"]] |
| SPECIES_NIDORAN_M | [["EVO_LEVEL","16","SPECIES_NIDORINO","0"]] |
| SPECIES_NIDORINA | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_NIDOQUEEN","0"]] |
| SPECIES_NIDORINO | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_NIDOKING","0"]] |
| SPECIES_NINCADA | [["EVO_LEVEL_NINJASK","20","SPECIES_NINJASK","0"],["EVO_LEVEL_SHEDINJA","20","SPECIES_SHEDINJA","0"]] |
| SPECIES_NOIBAT | [["EVO_LEVEL","48","SPECIES_NOIVERN","0"]] |
| SPECIES_NOSEPASS | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_PROBOPASS","0"],["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_PROBOPASS","0"]] |
| SPECIES_NUMEL | [["EVO_LEVEL","33","SPECIES_CAMERUPT","0"]] |
| SPECIES_NUZLEAF | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_SHIFTRY","0"]] |
| SPECIES_NYMBLE | [["EVO_LEVEL","24","SPECIES_LOKIX","0"]] |
| SPECIES_ODDISH | [["EVO_LEVEL","21","SPECIES_GLOOM","0"]] |
| SPECIES_OMANYTE | [["EVO_LEVEL","40","SPECIES_OMASTAR","0"]] |
| SPECIES_ONIX | [["EVO_TRADE_ITEM","ITEM_METAL_COAT","SPECIES_STEELIX","0"],["EVO_ITEM","ITEM_METAL_COAT","SPECIES_STEELIX","0"]] |
| SPECIES_OSHAWOTT | [["EVO_LEVEL","17","SPECIES_DEWOTT","0"]] |
| SPECIES_PALPITOAD | [["EVO_LEVEL","36","SPECIES_SEISMITOAD","0"]] |
| SPECIES_PANCHAM | [["EVO_TYPE_IN_PARTY","32","SPECIES_PANGORO","TYPE_DARK"]] |
| SPECIES_PANPOUR | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_SIMIPOUR","0"]] |
| SPECIES_PANSAGE | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_SIMISAGE","0"]] |
| SPECIES_PANSEAR | [["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_SIMISEAR","0"]] |
| SPECIES_PARAS | [["EVO_LEVEL","24","SPECIES_PARASECT","0"]] |
| SPECIES_PATRAT | [["EVO_LEVEL","20","SPECIES_WATCHOG","0"]] |
| SPECIES_PAWMI | [["EVO_LEVEL","18","SPECIES_PAWMO","0"]] |
| SPECIES_PAWMO | [["EVO_FRIENDSHIP","0","SPECIES_PAWMOT","0"]] |
| SPECIES_PAWNIARD | [["EVO_LEVEL","52","SPECIES_BISHARP","0"]] |
| SPECIES_PETILIL | [["EVO_ITEM","ITEM_SUN_STONE","SPECIES_LILLIGANT","0"],["EVO_ITEM_HOLD_ITEM","ITEM_SUN_STONE","SPECIES_LILLIGANT_H","ITEM_HISUI_ROCK"]] |
| SPECIES_PHANPY | [["EVO_LEVEL","25","SPECIES_DONPHAN","0"]] |
| SPECIES_PHANTUMP | [["EVO_TRADE","0","SPECIES_TREVENANT","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_TREVENANT","0"]] |
| SPECIES_PICHU | [["EVO_FRIENDSHIP","0","SPECIES_PIKACHU","0"]] |
| SPECIES_PIDGEOTTO | [["EVO_LEVEL","36","SPECIES_PIDGEOT","0"]] |
| SPECIES_PIDGEY | [["EVO_LEVEL","18","SPECIES_PIDGEOTTO","0"]] |
| SPECIES_PIDOVE | [["EVO_LEVEL","21","SPECIES_TRANQUILL","0"]] |
| SPECIES_PIGNITE | [["EVO_LEVEL","36","SPECIES_EMBOAR","0"]] |
| SPECIES_PIKACHU | [["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_RAICHU","0"],["EVO_ITEM_LOCATION","ITEM_THUNDER_STONE","SPECIES_RAICHU_A","MB_SHALLOW_WATER"]] |
| SPECIES_PIKIPEK | [["EVO_LEVEL","14","SPECIES_TRUMBEAK","0"]] |
| SPECIES_PILOSWINE | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_MAMOSWINE","0"]] |
| SPECIES_PINECO | [["EVO_LEVEL","31","SPECIES_FORRETRESS","0"]] |
| SPECIES_PIPLUP | [["EVO_LEVEL","16","SPECIES_PRINPLUP","0"]] |
| SPECIES_POIPOLE | [["EVO_MOVE","MOVE_DRAGONPULSE","SPECIES_NAGANADEL","0"]] |
| SPECIES_POLIWAG | [["EVO_LEVEL","25","SPECIES_POLIWHIRL","0"]] |
| SPECIES_POLIWHIRL | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_POLIWRATH","0"],["EVO_TRADE_ITEM","ITEM_KINGS_ROCK","SPECIES_POLITOED","0"],["EVO_ITEM","ITEM_KINGS_ROCK","SPECIES_POLITOED","0"]] |
| SPECIES_POLTCHAGEIST | [["EVO_ITEM","ITEM_UNREMARKABLE_TEACUP","SPECIES_SINISTCHA","0"]] |
| SPECIES_POLTCHAGEIST_ARTISAN | [["EVO_ITEM","ITEM_MASTERPIECE_TEACUP","SPECIES_SINISTCHA_MASTERPIECE","0"]] |
| SPECIES_PONYTA | [["EVO_LEVEL","40","SPECIES_RAPIDASH","0"]] |
| SPECIES_PONYTA_G | [["EVO_LEVEL","40","SPECIES_RAPIDASH_G","0"]] |
| SPECIES_POOCHYENA | [["EVO_LEVEL","18","SPECIES_MIGHTYENA","0"]] |
| SPECIES_POPPLIO | [["EVO_LEVEL","17","SPECIES_BRIONNE","0"]] |
| SPECIES_PORYGON | [["EVO_ITEM","ITEM_UP_GRADE","SPECIES_PORYGON2","0"],["EVO_TRADE_ITEM","ITEM_UP_GRADE","SPECIES_PORYGON2","0"]] |
| SPECIES_PORYGON2 | [["EVO_TRADE_ITEM","ITEM_DUBIOUS_DISC","SPECIES_PORYGON_Z","0"],["EVO_ITEM","ITEM_DUBIOUS_DISC","SPECIES_PORYGON_Z","0"]] |
| SPECIES_PRIMEAPE | [["EVO_MOVE","MOVE_RAGEFIST","SPECIES_ANNIHILAPE","0"]] |
| SPECIES_PRINPLUP | [["EVO_LEVEL","36","SPECIES_EMPOLEON","0"]] |
| SPECIES_PSYDUCK | [["EVO_LEVEL","33","SPECIES_GOLDUCK","0"]] |
| SPECIES_PUMPKABOO | [["EVO_TRADE","0","SPECIES_GOURGEIST","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOURGEIST","0"]] |
| SPECIES_PUMPKABOO_L | [["EVO_TRADE","0","SPECIES_GOURGEIST_L","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOURGEIST_L","0"]] |
| SPECIES_PUMPKABOO_M | [["EVO_TRADE","0","SPECIES_GOURGEIST_M","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOURGEIST_M","0"]] |
| SPECIES_PUMPKABOO_XL | [["EVO_TRADE","0","SPECIES_GOURGEIST_XL","0"],["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_GOURGEIST_XL","0"]] |
| SPECIES_PUPITAR | [["EVO_LEVEL","48","SPECIES_TYRANITAR","0"]] |
| SPECIES_PURRLOIN | [["EVO_LEVEL","20","SPECIES_LIEPARD","0"]] |
| SPECIES_QUAXLY | [["EVO_LEVEL","16","SPECIES_QUAXWELL","0"]] |
| SPECIES_QUAXWELL | [["EVO_LEVEL","36","SPECIES_QUAQUAVAL","0"]] |
| SPECIES_QUILAVA | [["EVO_LEVEL","36","SPECIES_TYPHLOSION","0"],["EVO_LEVEL_HOLD_ITEM","36","SPECIES_TYPHLOSION_H","ITEM_HISUI_ROCK"]] |
| SPECIES_QUILLADIN | [["EVO_LEVEL","36","SPECIES_CHESNAUGHT","0"]] |
| SPECIES_QWILFISH_H | [["EVO_MOVE","MOVE_BARBBARRAGE","SPECIES_OVERQWIL","0"]] |
| SPECIES_RABOOT | [["EVO_LEVEL","35","SPECIES_CINDERACE","0"]] |
| SPECIES_RALTS | [["EVO_LEVEL","20","SPECIES_KIRLIA","0"]] |
| SPECIES_RATTATA | [["EVO_LEVEL","20","SPECIES_RATICATE","0"]] |
| SPECIES_RATTATA_A | [["EVO_LEVEL_NIGHT","20","SPECIES_RATICATE_A","0"]] |
| SPECIES_RELLOR | [["EVO_FRIENDSHIP","0","SPECIES_RABSCA","0"]] |
| SPECIES_REMORAID | [["EVO_LEVEL","25","SPECIES_OCTILLERY","0"]] |
| SPECIES_RHYDON | [["EVO_ITEM","ITEM_PROTECTOR","SPECIES_RHYPERIOR","0"],["EVO_TRADE_ITEM","ITEM_PROTECTOR","SPECIES_RHYPERIOR","0"]] |
| SPECIES_RHYHORN | [["EVO_LEVEL","42","SPECIES_RHYDON","0"]] |
| SPECIES_RIOLU | [["EVO_FRIENDSHIP_DAY","0","SPECIES_LUCARIO","0"]] |
| SPECIES_ROCKRUFF | [["EVO_LEVEL_DAY","25","SPECIES_LYCANROC","0"],["EVO_LEVEL_NIGHT","25","SPECIES_LYCANROC_N","0"],["EVO_LEVEL_SPECIFIC_TIME_RANGE","25","SPECIES_LYCANROC_DUSK","TIME_RANGE(17, 20)"]] |
| SPECIES_ROGGENROLA | [["EVO_LEVEL","25","SPECIES_BOLDORE","0"]] |
| SPECIES_ROLYCOLY | [["EVO_LEVEL","18","SPECIES_CARKOL","0"]] |
| SPECIES_ROOKIDEE | [["EVO_LEVEL","18","SPECIES_CORVISQUIRE","0"]] |
| SPECIES_ROSELIA | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_ROSERADE","0"]] |
| SPECIES_ROWLET | [["EVO_LEVEL","17","SPECIES_DARTRIX","0"]] |
| SPECIES_RUFFLET | [["EVO_LEVEL","50","SPECIES_BRAVIARY","0"],["EVO_LEVEL_HOLD_ITEM","50","SPECIES_BRAVIARY_H","ITEM_HISUI_ROCK"]] |
| SPECIES_SALANDIT | [["EVO_FEMALE_LEVEL","33","SPECIES_SALAZZLE","0"]] |
| SPECIES_SANDILE | [["EVO_LEVEL","29","SPECIES_KROKOROK","0"]] |
| SPECIES_SANDSHREW | [["EVO_LEVEL","22","SPECIES_SANDSLASH","0"]] |
| SPECIES_SANDSHREW_A | [["EVO_ITEM","ITEM_ICE_STONE","SPECIES_SANDSLASH_A","0"]] |
| SPECIES_SANDYGAST | [["EVO_LEVEL","42","SPECIES_PALOSSAND","0"]] |
| SPECIES_SCATTERBUG | [["EVO_LEVEL","9","SPECIES_SPEWPA","0"]] |
| SPECIES_SCORBUNNY | [["EVO_LEVEL","16","SPECIES_RABOOT","0"]] |
| SPECIES_SCRAGGY | [["EVO_LEVEL","39","SPECIES_SCRAFTY","0"]] |
| SPECIES_SCYTHER | [["EVO_TRADE_ITEM","ITEM_METAL_COAT","SPECIES_SCIZOR","0"],["EVO_ITEM","ITEM_METAL_COAT","SPECIES_SCIZOR","0"],["EVO_TRADE_ITEM","ITEM_BLACK_AUGURITE","SPECIES_KLEAVOR","0"],["EVO_ITEM","ITEM_BLACK_AUGURITE","SPECIES_KLEAVOR","0"]] |
| SPECIES_SEADRA | [["EVO_TRADE_ITEM","ITEM_DRAGON_SCALE","SPECIES_KINGDRA","0"],["EVO_ITEM","ITEM_DRAGON_SCALE","SPECIES_KINGDRA","0"]] |
| SPECIES_SEALEO | [["EVO_LEVEL","44","SPECIES_WALREIN","0"]] |
| SPECIES_SEEDOT | [["EVO_LEVEL","14","SPECIES_NUZLEAF","0"]] |
| SPECIES_SEEL | [["EVO_LEVEL","34","SPECIES_DEWGONG","0"]] |
| SPECIES_SENTRET | [["EVO_LEVEL","15","SPECIES_FURRET","0"]] |
| SPECIES_SERVINE | [["EVO_LEVEL","36","SPECIES_SERPERIOR","0"]] |
| SPECIES_SEWADDLE | [["EVO_LEVEL","20","SPECIES_SWADLOON","0"]] |
| SPECIES_SHELGON | [["EVO_LEVEL","50","SPECIES_SALAMENCE","0"]] |
| SPECIES_SHELLDER | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_CLOYSTER","0"]] |
| SPECIES_SHELLOS | [["EVO_LEVEL","30","SPECIES_GASTRODON","0"]] |
| SPECIES_SHELLOS_EAST | [["EVO_LEVEL","30","SPECIES_GASTRODON_EAST","0"]] |
| SPECIES_SHELMET | [["EVO_ITEM","ITEM_LINK_CABLE","SPECIES_ACCELGOR","0"],["EVO_TRADE","0","SPECIES_ACCELGOR","0"]] |
| SPECIES_SHIELDON | [["EVO_LEVEL","30","SPECIES_BASTIODON","0"]] |
| SPECIES_SHINX | [["EVO_LEVEL","15","SPECIES_LUXIO","0"]] |
| SPECIES_SHROODLE | [["EVO_LEVEL","28","SPECIES_GRAFAIAI","0"]] |
| SPECIES_SHROOMISH | [["EVO_LEVEL","23","SPECIES_BRELOOM","0"]] |
| SPECIES_SHUPPET | [["EVO_LEVEL","37","SPECIES_BANETTE","0"]] |
| SPECIES_SILCOON | [["EVO_LEVEL","10","SPECIES_BEAUTIFLY","0"]] |
| SPECIES_SILICOBRA | [["EVO_LEVEL","36","SPECIES_SANDACONDA","0"]] |
| SPECIES_SINISTEA | [["EVO_ITEM","ITEM_CRACKED_POT","SPECIES_POLTEAGEIST","0"]] |
| SPECIES_SINISTEA_CHIPPED | [["EVO_ITEM","ITEM_CHIPPED_POT","SPECIES_POLTEAGEIST_CHIPPED","0"]] |
| SPECIES_SIZZLIPEDE | [["EVO_LEVEL","28","SPECIES_CENTISKORCH","0"]] |
| SPECIES_SKIDDO | [["EVO_LEVEL","32","SPECIES_GOGOAT","0"]] |
| SPECIES_SKIPLOOM | [["EVO_LEVEL","27","SPECIES_JUMPLUFF","0"]] |
| SPECIES_SKITTY | [["EVO_ITEM","ITEM_MOON_STONE","SPECIES_DELCATTY","0"]] |
| SPECIES_SKORUPI | [["EVO_LEVEL","40","SPECIES_DRAPION","0"]] |
| SPECIES_SKRELP | [["EVO_LEVEL","48","SPECIES_DRAGALGE","0"]] |
| SPECIES_SKWOVET | [["EVO_LEVEL","24","SPECIES_GREEDENT","0"]] |
| SPECIES_SLAKOTH | [["EVO_LEVEL","18","SPECIES_VIGOROTH","0"]] |
| SPECIES_SLIGGOO | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA","0"]] |
| SPECIES_SLIGGOO_H | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA_H","0"]] |
| SPECIES_SLOWPOKE | [["EVO_LEVEL","37","SPECIES_SLOWBRO","0"],["EVO_TRADE_ITEM","ITEM_KINGS_ROCK","SPECIES_SLOWKING","0"],["EVO_ITEM","ITEM_KINGS_ROCK","SPECIES_SLOWKING","0"]] |
| SPECIES_SLOWPOKE_G | [["EVO_ITEM","ITEM_GALARICA_CUFF","SPECIES_SLOWBRO_G","0"],["EVO_ITEM","ITEM_GALARICA_WREATH","SPECIES_SLOWKING_G","0"]] |
| SPECIES_SLUGMA | [["EVO_LEVEL","30","SPECIES_MAGCARGO","0"]] |
| SPECIES_SMOLIV | [["EVO_LEVEL","25","SPECIES_DOLLIV","0"]] |
| SPECIES_SMOOCHUM | [["EVO_LEVEL","30","SPECIES_JYNX","0"]] |
| SPECIES_SNEASEL | [["EVO_HOLD_ITEM_NIGHT","ITEM_RAZOR_CLAW","SPECIES_WEAVILE","0"]] |
| SPECIES_SNEASEL_H | [["EVO_HOLD_ITEM_DAY","ITEM_RAZOR_CLAW","SPECIES_SNEASLER","0"]] |
| SPECIES_SNIVY | [["EVO_LEVEL","17","SPECIES_SERVINE","0"]] |
| SPECIES_SNOM | [["EVO_FRIENDSHIP_NIGHT","0","SPECIES_FROSMOTH","0"]] |
| SPECIES_SNORUNT | [["EVO_LEVEL","30","SPECIES_GLALIE","0"],["EVO_ITEM","ITEM_DAWN_STONE","SPECIES_FROSLASS","MON_FEMALE"]] |
| SPECIES_SNOVER | [["EVO_LEVEL","40","SPECIES_ABOMASNOW","0"]] |
| SPECIES_SNUBBULL | [["EVO_LEVEL","23","SPECIES_GRANBULL","0"]] |
| SPECIES_SOBBLE | [["EVO_LEVEL","16","SPECIES_DRIZZILE","0"]] |
| SPECIES_SOLOSIS | [["EVO_LEVEL","32","SPECIES_DUOSION","0"]] |
| SPECIES_SPEAROW | [["EVO_LEVEL","20","SPECIES_FEAROW","0"]] |
| SPECIES_SPEWPA | [["EVO_LEVEL","12","SPECIES_VIVILLON","0"]] |
| SPECIES_SPHEAL | [["EVO_LEVEL","32","SPECIES_SEALEO","0"]] |
| SPECIES_SPINARAK | [["EVO_LEVEL","22","SPECIES_ARIADOS","0"]] |
| SPECIES_SPOINK | [["EVO_LEVEL","32","SPECIES_GRUMPIG","0"]] |
| SPECIES_SPRIGATITO | [["EVO_LEVEL","16","SPECIES_FLORAGATO","0"]] |
| SPECIES_SPRITZEE | [["EVO_ITEM","ITEM_SACHET","SPECIES_AROMATISSE","0"],["EVO_TRADE_ITEM","ITEM_SACHET","SPECIES_AROMATISSE","0"]] |
| SPECIES_SQUIRTLE | [["EVO_LEVEL","16","SPECIES_WARTORTLE","0"]] |
| SPECIES_STANTLER | [["EVO_MOVE","MOVE_PSYSHIELDBASH","SPECIES_WYRDEER","0"]] |
| SPECIES_STARAVIA | [["EVO_LEVEL","34","SPECIES_STARAPTOR","0"]] |
| SPECIES_STARLY | [["EVO_LEVEL","14","SPECIES_STARAVIA","0"]] |
| SPECIES_STARYU | [["EVO_ITEM","ITEM_WATER_STONE","SPECIES_STARMIE","0"]] |
| SPECIES_STEENEE | [["EVO_MOVE","MOVE_STOMP","SPECIES_TSAREENA","0"]] |
| SPECIES_STUFFUL | [["EVO_LEVEL","27","SPECIES_BEWEAR","0"]] |
| SPECIES_STUNKY | [["EVO_LEVEL","34","SPECIES_SKUNTANK","0"]] |
| SPECIES_SUNKERN | [["EVO_ITEM","ITEM_SUN_STONE","SPECIES_SUNFLORA","0"]] |
| SPECIES_SURSKIT | [["EVO_LEVEL","22","SPECIES_MASQUERAIN","0"]] |
| SPECIES_SWABLU | [["EVO_LEVEL","35","SPECIES_ALTARIA","0"]] |
| SPECIES_SWADLOON | [["EVO_FRIENDSHIP","0","SPECIES_LEAVANNY","0"]] |
| SPECIES_SWINUB | [["EVO_LEVEL","33","SPECIES_PILOSWINE","0"]] |
| SPECIES_SWIRLIX | [["EVO_ITEM","ITEM_WHIPPED_DREAM","SPECIES_SLURPUFF","0"],["EVO_TRADE_ITEM","ITEM_WHIPPED_DREAM","SPECIES_SLURPUFF","0"]] |
| SPECIES_TADBULB | [["EVO_ITEM","ITEM_THUNDER_STONE","SPECIES_BELLIBOLT","0"]] |
| SPECIES_TAILLOW | [["EVO_LEVEL","22","SPECIES_SWELLOW","0"]] |
| SPECIES_TANDEMAUS | [["EVO_MAUSHOLD_THREE","25","SPECIES_MAUSHOLD","0"],["EVO_MAUSHOLD_FOUR","25","SPECIES_MAUSHOLD_FOUR","0"]] |
| SPECIES_TANGELA | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_TANGROWTH","0"]] |
| SPECIES_TAROUNTULA | [["EVO_LEVEL","15","SPECIES_SPIDOPS","0"]] |
| SPECIES_TEDDIURSA | [["EVO_LEVEL","30","SPECIES_URSARING","0"]] |
| SPECIES_TENTACOOL | [["EVO_LEVEL","30","SPECIES_TENTACRUEL","0"]] |
| SPECIES_TEPIG | [["EVO_LEVEL","17","SPECIES_PIGNITE","0"]] |
| SPECIES_THWACKEY | [["EVO_LEVEL","35","SPECIES_RILLABOOM","0"]] |
| SPECIES_TIMBURR | [["EVO_LEVEL","25","SPECIES_GURDURR","0"]] |
| SPECIES_TINKATINK | [["EVO_LEVEL","24","SPECIES_TINKATUFF","0"]] |
| SPECIES_TINKATUFF | [["EVO_LEVEL","38","SPECIES_TINKATON","0"]] |
| SPECIES_TIRTOUGA | [["EVO_LEVEL","37","SPECIES_CARRACOSTA","0"]] |
| SPECIES_TOEDSCOOL | [["EVO_LEVEL","30","SPECIES_TOEDSCRUEL","0"]] |
| SPECIES_TOGEPI | [["EVO_FRIENDSHIP","0","SPECIES_TOGETIC","0"]] |
| SPECIES_TOGETIC | [["EVO_ITEM","ITEM_SHINY_STONE","SPECIES_TOGEKISS","0"]] |
| SPECIES_TORCHIC | [["EVO_LEVEL","16","SPECIES_COMBUSKEN","0"]] |
| SPECIES_TORRACAT | [["EVO_LEVEL","34","SPECIES_INCINEROAR","0"]] |
| SPECIES_TOTODILE | [["EVO_LEVEL","18","SPECIES_CROCONAW","0"]] |
| SPECIES_TOXEL | [["EVO_NATURE_HIGH","30","SPECIES_TOXTRICITY","0"],["EVO_NATURE_LOW","30","SPECIES_TOXTRICITY_LOW_KEY","0"]] |
| SPECIES_TRANQUILL | [["EVO_LEVEL","32","SPECIES_UNFEZANT","0"]] |
| SPECIES_TRAPINCH | [["EVO_LEVEL","35","SPECIES_VIBRAVA","0"]] |
| SPECIES_TREECKO | [["EVO_LEVEL","16","SPECIES_GROVYLE","0"]] |
| SPECIES_TRUBBISH | [["EVO_LEVEL","36","SPECIES_GARBODOR","0"]] |
| SPECIES_TRUMBEAK | [["EVO_LEVEL","28","SPECIES_TOUCANNON","0"]] |
| SPECIES_TURTWIG | [["EVO_LEVEL","18","SPECIES_GROTLE","0"]] |
| SPECIES_TYMPOLE | [["EVO_LEVEL","25","SPECIES_PALPITOAD","0"]] |
| SPECIES_TYNAMO | [["EVO_LEVEL","39","SPECIES_EELEKTRIK","0"]] |
| SPECIES_TYPE_NULL | [["EVO_FRIENDSHIP","0","SPECIES_SILVALLY","0"]] |
| SPECIES_TYROGUE | [["EVO_LEVEL_ATK_GT_DEF","20","SPECIES_HITMONLEE","0"],["EVO_LEVEL_ATK_EQ_DEF","20","SPECIES_HITMONTOP","0"],["EVO_LEVEL_ATK_LT_DEF","20","SPECIES_HITMONCHAN","0"]] |
| SPECIES_TYRUNT | [["EVO_LEVEL_DAY","39","SPECIES_TYRANTRUM","0"]] |
| SPECIES_URSARING | [["EVO_ITEM_NIGHT","ITEM_PEAT_BLOCK","SPECIES_URSALUNA","0"]] |
| SPECIES_VANILLISH | [["EVO_LEVEL","42","SPECIES_VANILLUXE","0"]] |
| SPECIES_VANILLITE | [["EVO_LEVEL","24","SPECIES_VANILLISH","0"]] |
| SPECIES_VAROOM | [["EVO_LEVEL","40","SPECIES_REVAVROOM","0"]] |
| SPECIES_VENIPEDE | [["EVO_LEVEL","22","SPECIES_WHIRLIPEDE","0"]] |
| SPECIES_VENONAT | [["EVO_LEVEL","31","SPECIES_VENOMOTH","0"]] |
| SPECIES_VIBRAVA | [["EVO_LEVEL","45","SPECIES_FLYGON","0"]] |
| SPECIES_VIGOROTH | [["EVO_LEVEL","36","SPECIES_SLAKING","0"]] |
| SPECIES_VOLTORB | [["EVO_LEVEL","30","SPECIES_ELECTRODE","0"]] |
| SPECIES_VOLTORB_H | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_ELECTRODE_H","0"]] |
| SPECIES_VULLABY | [["EVO_LEVEL","50","SPECIES_MANDIBUZZ","0"]] |
| SPECIES_VULPIX | [["EVO_ITEM","ITEM_FIRE_STONE","SPECIES_NINETALES","0"]] |
| SPECIES_VULPIX_A | [["EVO_ITEM","ITEM_ICE_STONE","SPECIES_NINETALES_A","0"]] |
| SPECIES_WAILMER | [["EVO_LEVEL","40","SPECIES_WAILORD","0"]] |
| SPECIES_WARTORTLE | [["EVO_LEVEL","36","SPECIES_BLASTOISE","0"]] |
| SPECIES_WATTREL | [["EVO_LEVEL","25","SPECIES_KILOWATTREL","0"]] |
| SPECIES_WEEDLE | [["EVO_LEVEL","7","SPECIES_KAKUNA","0"]] |
| SPECIES_WEEPINBELL | [["EVO_ITEM","ITEM_LEAF_STONE","SPECIES_VICTREEBEL","0"]] |
| SPECIES_WHIRLIPEDE | [["EVO_LEVEL","30","SPECIES_SCOLIPEDE","0"]] |
| SPECIES_WHISMUR | [["EVO_LEVEL","20","SPECIES_LOUDRED","0"]] |
| SPECIES_WIGLETT | [["EVO_LEVEL","26","SPECIES_WUGTRIO","0"]] |
| SPECIES_WIMPOD | [["EVO_LEVEL","30","SPECIES_GOLISOPOD","0"]] |
| SPECIES_WINGULL | [["EVO_LEVEL","25","SPECIES_PELIPPER","0"]] |
| SPECIES_WOOBAT | [["EVO_FRIENDSHIP","0","SPECIES_SWOOBAT","0"]] |
| SPECIES_WOOLOO | [["EVO_LEVEL","24","SPECIES_DUBWOOL","0"]] |
| SPECIES_WOOPER | [["EVO_LEVEL","20","SPECIES_QUAGSIRE","0"]] |
| SPECIES_WOOPER_P | [["EVO_LEVEL","20","SPECIES_CLODSIRE","0"]] |
| SPECIES_WURMPLE | [["EVO_LEVEL_SILCOON","7","SPECIES_SILCOON","0"],["EVO_LEVEL_CASCOON","7","SPECIES_CASCOON","0"]] |
| SPECIES_WYNAUT | [["EVO_LEVEL","15","SPECIES_WOBBUFFET","0"]] |
| SPECIES_YAMASK | [["EVO_LEVEL","34","SPECIES_COFAGRIGUS","0"]] |
| SPECIES_YAMASK_G | [["EVO_LEVEL","35","SPECIES_RUNERIGUS","0"]] |
| SPECIES_YAMPER | [["EVO_LEVEL","25","SPECIES_BOLTUND","0"]] |
| SPECIES_YANMA | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_YANMEGA","0"]] |
| SPECIES_YUNGOOS | [["EVO_LEVEL_DAY","20","SPECIES_GUMSHOOS","0"]] |
| SPECIES_ZIGZAGOON | [["EVO_LEVEL","20","SPECIES_LINOONE","0"]] |
| SPECIES_ZIGZAGOON_G | [["EVO_LEVEL","20","SPECIES_LINOONE_G","0"]] |
| SPECIES_ZORUA | [["EVO_LEVEL","30","SPECIES_ZOROARK","0"]] |
| SPECIES_ZORUA_H | [["EVO_LEVEL","30","SPECIES_ZOROARK_H","0"]] |
| SPECIES_ZUBAT | [["EVO_LEVEL","22","SPECIES_GOLBAT","0"]] |
| SPECIES_ZWEILOUS | [["EVO_LEVEL","64","SPECIES_HYDREIGON","0"]] |

Battle-transition metadata, separately accounted:

| Parent | Rows |
| --- | --- |
| SPECIES_ABOMASNOW | [["EVO_MEGA","ITEM_ABOMASITE","SPECIES_ABOMASNOW_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABOMASNOW_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ABOMASNOW","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABSOL | [["EVO_MEGA","ITEM_ABSOLITE","SPECIES_ABSOL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABSOL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ABSOL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AERODACTYL | [["EVO_MEGA","ITEM_AERODACTYLITE","SPECIES_AERODACTYL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AERODACTYL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AERODACTYL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AGGRON | [["EVO_MEGA","ITEM_AGGRONITE","SPECIES_AGGRON_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AGGRON_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AGGRON","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALAKAZAM | [["EVO_MEGA","ITEM_ALAKAZITE","SPECIES_ALAKAZAM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALAKAZAM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ALAKAZAM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALCREMIE_BERRY | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_CLOVER | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_FLOWER | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_ALCREMIE_STRAWBERRY","0"]] |
| SPECIES_ALCREMIE_LOVE | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_RIBBON | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_STRAWBERRY | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALTARIA | [["EVO_MEGA","ITEM_ALTARIANITE","SPECIES_ALTARIA_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALTARIA_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ALTARIA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AMPHAROS | [["EVO_MEGA","ITEM_AMPHAROSITE","SPECIES_AMPHAROS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AMPHAROS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AMPHAROS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_APPLETUN | [["EVO_GIGANTAMAX","TRUE","SPECIES_APPLETUN_GIGA","0"]] |
| SPECIES_APPLETUN_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_APPLETUN","0"]] |
| SPECIES_AUDINO | [["EVO_MEGA","ITEM_AUDINITE","SPECIES_AUDINO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AUDINO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AUDINO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BANETTE | [["EVO_MEGA","ITEM_BANETTITE","SPECIES_BANETTE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BANETTE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BANETTE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BEEDRILL | [["EVO_MEGA","ITEM_BEEDRILLITE","SPECIES_BEEDRILL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BEEDRILL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BEEDRILL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BLASTOISE | [["EVO_MEGA","ITEM_BLASTOISINITE","SPECIES_BLASTOISE_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_BLASTOISE_GIGA","0"]] |
| SPECIES_BLASTOISE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_BLASTOISE","0"]] |
| SPECIES_BLASTOISE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BLASTOISE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BLAZIKEN | [["EVO_MEGA","ITEM_BLAZIKENITE","SPECIES_BLAZIKEN_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BLAZIKEN_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BLAZIKEN","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BUTTERFREE | [["EVO_GIGANTAMAX","TRUE","SPECIES_BUTTERFREE_GIGA","0"]] |
| SPECIES_BUTTERFREE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_BUTTERFREE","0"]] |
| SPECIES_CAMERUPT | [["EVO_MEGA","ITEM_CAMERUPTITE","SPECIES_CAMERUPT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CAMERUPT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_CAMERUPT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CENTISKORCH | [["EVO_GIGANTAMAX","TRUE","SPECIES_CENTISKORCH_GIGA","0"]] |
| SPECIES_CENTISKORCH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CENTISKORCH","0"]] |
| SPECIES_CHARIZARD | [["EVO_MEGA","ITEM_CHARIZARDITE_X","SPECIES_CHARIZARD_MEGA_X","MEGA_VARIANT_STANDARD"],["EVO_MEGA","ITEM_CHARIZARDITE_Y","SPECIES_CHARIZARD_MEGA_Y","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_CHARIZARD_GIGA","0"]] |
| SPECIES_CHARIZARD_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CHARIZARD","0"]] |
| SPECIES_CHARIZARD_MEGA_X | [["EVO_MEGA","ITEM_NONE","SPECIES_CHARIZARD","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CHARIZARD_MEGA_Y | [["EVO_MEGA","ITEM_NONE","SPECIES_CHARIZARD","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CINDERACE | [["EVO_GIGANTAMAX","TRUE","SPECIES_CINDERACE_GIGA","0"]] |
| SPECIES_CINDERACE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CINDERACE","0"]] |
| SPECIES_COALOSSAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_COALOSSAL_GIGA","0"]] |
| SPECIES_COALOSSAL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_COALOSSAL","0"]] |
| SPECIES_COPPERAJAH | [["EVO_GIGANTAMAX","TRUE","SPECIES_COPPERAJAH_GIGA","0"]] |
| SPECIES_COPPERAJAH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_COPPERAJAH","0"]] |
| SPECIES_CORVIKNIGHT | [["EVO_GIGANTAMAX","TRUE","SPECIES_CORVIKNIGHT_GIGA","0"]] |
| SPECIES_CORVIKNIGHT_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CORVIKNIGHT","0"]] |
| SPECIES_DIANCIE | [["EVO_MEGA","ITEM_DIANCITE","SPECIES_DIANCIE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_DIANCIE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_DIANCIE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_DREDNAW | [["EVO_GIGANTAMAX","TRUE","SPECIES_DREDNAW_GIGA","0"]] |
| SPECIES_DREDNAW_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_DREDNAW","0"]] |
| SPECIES_DURALUDON | [["EVO_GIGANTAMAX","TRUE","SPECIES_DURALUDON_GIGA","0"]] |
| SPECIES_DURALUDON_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_DURALUDON","0"]] |
| SPECIES_EEVEE | [["EVO_GIGANTAMAX","TRUE","SPECIES_EEVEE_GIGA","0"]] |
| SPECIES_EEVEE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_EEVEE","0"]] |
| SPECIES_FLAPPLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_FLAPPLE_GIGA","0"]] |
| SPECIES_FLAPPLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_FLAPPLE","0"]] |
| SPECIES_GALLADE | [["EVO_MEGA","ITEM_GALLADITE","SPECIES_GALLADE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GALLADE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GALLADE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARBODOR | [["EVO_GIGANTAMAX","TRUE","SPECIES_GARBODOR_GIGA","0"]] |
| SPECIES_GARBODOR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GARBODOR","0"]] |
| SPECIES_GARCHOMP | [["EVO_MEGA","ITEM_GARCHOMPITE","SPECIES_GARCHOMP_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARCHOMP_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GARCHOMP","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARDEVOIR | [["EVO_MEGA","ITEM_GARDEVOIRITE","SPECIES_GARDEVOIR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARDEVOIR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GARDEVOIR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GENGAR | [["EVO_MEGA","ITEM_GENGARITE","SPECIES_GENGAR_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_GENGAR_GIGA","0"]] |
| SPECIES_GENGAR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GENGAR","0"]] |
| SPECIES_GENGAR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GENGAR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GLALIE | [["EVO_MEGA","ITEM_GLALITITE","SPECIES_GLALIE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GLALIE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GLALIE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GRIMMSNARL | [["EVO_GIGANTAMAX","TRUE","SPECIES_GRIMMSNARL_GIGA","0"]] |
| SPECIES_GRIMMSNARL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GRIMMSNARL","0"]] |
| SPECIES_GROUDON | [["EVO_MEGA","ITEM_RED_ORB","SPECIES_GROUDON_PRIMAL","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_GROUDON_PRIMAL | [["EVO_MEGA","ITEM_NONE","SPECIES_GROUDON","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_GYARADOS | [["EVO_MEGA","ITEM_GYARADOSITE","SPECIES_GYARADOS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GYARADOS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GYARADOS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HATTERENE | [["EVO_GIGANTAMAX","TRUE","SPECIES_HATTERENE_GIGA","0"]] |
| SPECIES_HATTERENE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_HATTERENE","0"]] |
| SPECIES_HERACROSS | [["EVO_MEGA","ITEM_HERACRONITE","SPECIES_HERACROSS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HERACROSS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_HERACROSS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HOUNDOOM | [["EVO_MEGA","ITEM_HOUNDOOMINITE","SPECIES_HOUNDOOM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HOUNDOOM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_HOUNDOOM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_INTELEON | [["EVO_GIGANTAMAX","TRUE","SPECIES_INTELEON_GIGA","0"]] |
| SPECIES_INTELEON_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_INTELEON","0"]] |
| SPECIES_KANGASKHAN | [["EVO_MEGA","ITEM_KANGASKHANITE","SPECIES_KANGASKHAN_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_KANGASKHAN_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_KANGASKHAN","MEGA_VARIANT_STANDARD"]] |
| SPECIES_KINGLER | [["EVO_GIGANTAMAX","TRUE","SPECIES_KINGLER_GIGA","0"]] |
| SPECIES_KINGLER_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_KINGLER","0"]] |
| SPECIES_KYOGRE | [["EVO_MEGA","ITEM_BLUE_ORB","SPECIES_KYOGRE_PRIMAL","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_KYOGRE_PRIMAL | [["EVO_MEGA","ITEM_NONE","SPECIES_KYOGRE","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_LAPRAS | [["EVO_GIGANTAMAX","TRUE","SPECIES_LAPRAS_GIGA","0"]] |
| SPECIES_LAPRAS_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_LAPRAS","0"]] |
| SPECIES_LATIAS | [["EVO_MEGA","ITEM_LATIASITE","SPECIES_LATIAS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIAS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LATIAS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIOS | [["EVO_MEGA","ITEM_LATIOSITE","SPECIES_LATIOS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIOS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LATIOS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LOPUNNY | [["EVO_MEGA","ITEM_LOPUNNITE","SPECIES_LOPUNNY_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LOPUNNY_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LOPUNNY","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LUCARIO | [["EVO_MEGA","ITEM_LUCARIONITE","SPECIES_LUCARIO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LUCARIO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LUCARIO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MACHAMP | [["EVO_GIGANTAMAX","TRUE","SPECIES_MACHAMP_GIGA","0"]] |
| SPECIES_MACHAMP_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MACHAMP","0"]] |
| SPECIES_MANECTRIC | [["EVO_MEGA","ITEM_MANECTITE","SPECIES_MANECTRIC_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MANECTRIC_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MANECTRIC","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MAWILE | [["EVO_MEGA","ITEM_MAWILITE","SPECIES_MAWILE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MAWILE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MAWILE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEDICHAM | [["EVO_MEGA","ITEM_MEDICHAMITE","SPECIES_MEDICHAM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEDICHAM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MEDICHAM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MELMETAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_MELMETAL_GIGA","0"]] |
| SPECIES_MELMETAL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MELMETAL","0"]] |
| SPECIES_MEOWTH | [["EVO_GIGANTAMAX","TRUE","SPECIES_MEOWTH_GIGA","0"]] |
| SPECIES_MEOWTH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MEOWTH","0"]] |
| SPECIES_METAGROSS | [["EVO_MEGA","ITEM_METAGROSSITE","SPECIES_METAGROSS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_METAGROSS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_METAGROSS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO | [["EVO_MEGA","ITEM_MEWTWONITE_X","SPECIES_MEWTWO_MEGA_X","MEGA_VARIANT_STANDARD"],["EVO_MEGA","ITEM_MEWTWONITE_Y","SPECIES_MEWTWO_MEGA_Y","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO_MEGA_X | [["EVO_MEGA","ITEM_NONE","SPECIES_MEWTWO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO_MEGA_Y | [["EVO_MEGA","ITEM_NONE","SPECIES_MEWTWO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_NECROZMA_DAWN_WINGS | [["EVO_MEGA","ITEM_ULTRANECROZIUM_Z","SPECIES_NECROZMA_ULTRA","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_NECROZMA_DUSK_MANE | [["EVO_MEGA","ITEM_ULTRANECROZIUM_Z","SPECIES_NECROZMA_ULTRA","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_NECROZMA_ULTRA | [["EVO_MEGA","ITEM_NONE","SPECIES_NECROZMA_DUSK_MANE","MEGA_VARIANT_ULTRA_BURST"],["EVO_MEGA","ITEM_NONE","SPECIES_NECROZMA_DAWN_WINGS","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_ORBEETLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_ORBEETLE_GIGA","0"]] |
| SPECIES_ORBEETLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_ORBEETLE","0"]] |
| SPECIES_PIDGEOT | [["EVO_MEGA","ITEM_PIDGEOTITE","SPECIES_PIDGEOT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PIDGEOT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_PIDGEOT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PIKACHU | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_BELLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_ALOLA | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_HOENN | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_KALOS | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_ORIGINAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_PARTNER | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_SINNOH | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_UNOVA | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_COSPLAY | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_FLYING | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_PIKACHU","0"]] |
| SPECIES_PIKACHU_LIBRE | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_PHD | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_POP_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_ROCK_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_SURFING | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PINSIR | [["EVO_MEGA","ITEM_PINSIRITE","SPECIES_PINSIR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PINSIR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_PINSIR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_RAYQUAZA | [["EVO_MEGA","MOVE_DRAGONASCENT","SPECIES_RAYQUAZA_MEGA","MEGA_VARIANT_WISH"]] |
| SPECIES_RAYQUAZA_MEGA | [["EVO_MEGA","MOVE_NONE","SPECIES_RAYQUAZA","MEGA_VARIANT_WISH"]] |
| SPECIES_RILLABOOM | [["EVO_GIGANTAMAX","TRUE","SPECIES_RILLABOOM_GIGA","0"]] |
| SPECIES_RILLABOOM_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_RILLABOOM","0"]] |
| SPECIES_SABLEYE | [["EVO_MEGA","ITEM_SABLENITE","SPECIES_SABLEYE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SABLEYE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SABLEYE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SALAMENCE | [["EVO_MEGA","ITEM_SALAMENCITE","SPECIES_SALAMENCE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SALAMENCE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SALAMENCE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SANDACONDA | [["EVO_GIGANTAMAX","TRUE","SPECIES_SANDACONDA_GIGA","0"]] |
| SPECIES_SANDACONDA_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_SANDACONDA","0"]] |
| SPECIES_SCEPTILE | [["EVO_MEGA","ITEM_SCEPTILITE","SPECIES_SCEPTILE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCEPTILE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SCEPTILE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCIZOR | [["EVO_MEGA","ITEM_SCIZORITE","SPECIES_SCIZOR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCIZOR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SCIZOR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SHARPEDO | [["EVO_MEGA","ITEM_SHARPEDONITE","SPECIES_SHARPEDO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SHARPEDO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SHARPEDO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SLOWBRO | [["EVO_MEGA","ITEM_SLOWBRONITE","SPECIES_SLOWBRO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SLOWBRO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SLOWBRO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SNORLAX | [["EVO_GIGANTAMAX","TRUE","SPECIES_SNORLAX_GIGA","0"]] |
| SPECIES_SNORLAX_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_SNORLAX","0"]] |
| SPECIES_STEELIX | [["EVO_MEGA","ITEM_STEELIXITE","SPECIES_STEELIX_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_STEELIX_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_STEELIX","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SWAMPERT | [["EVO_MEGA","ITEM_SWAMPERTITE","SPECIES_SWAMPERT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SWAMPERT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SWAMPERT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_TOXTRICITY | [["EVO_GIGANTAMAX","TRUE","SPECIES_TOXTRICITY_GIGA","0"]] |
| SPECIES_TOXTRICITY_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_TOXTRICITY","0"]] |
| SPECIES_TOXTRICITY_LOW_KEY | [["EVO_GIGANTAMAX","TRUE","SPECIES_TOXTRICITY_LOW_KEY_GIGA","0"]] |
| SPECIES_TOXTRICITY_LOW_KEY_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_TOXTRICITY_LOW_KEY","0"]] |
| SPECIES_TYRANITAR | [["EVO_MEGA","ITEM_TYRANITARITE","SPECIES_TYRANITAR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_TYRANITAR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_TYRANITAR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_URSHIFU_RAPID | [["EVO_GIGANTAMAX","TRUE","SPECIES_URSHIFU_RAPID_GIGA","0"]] |
| SPECIES_URSHIFU_RAPID_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_URSHIFU_RAPID","0"]] |
| SPECIES_URSHIFU_SINGLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_URSHIFU_SINGLE_GIGA","0"]] |
| SPECIES_URSHIFU_SINGLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_URSHIFU_SINGLE","0"]] |
| SPECIES_VENUSAUR | [["EVO_MEGA","ITEM_VENUSAURITE","SPECIES_VENUSAUR_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_VENUSAUR_GIGA","0"]] |
| SPECIES_VENUSAUR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_VENUSAUR","0"]] |
| SPECIES_VENUSAUR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_VENUSAUR","MEGA_VARIANT_STANDARD"]] |

## Appendix G — complete Egg Move differences / blocks

| Source / local | Class | Generations | Local entry | Missing literal-E union | Extra local | Move blocks |
| --- | --- | --- | --- | --- | --- | --- |
| abra / abra | MAPPING_BLOCK | 3,4,5,6,7,8 | True | MOVE_CONFUSION | MOVE_COUNTER | allyswitch:move-open-risk |
| absol / absol | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_ASSURANCE, MOVE_FEINT, MOVE_MEFIRST, MOVE_PERISHSONG, MOVE_SUBSTITUTE, MOVE_SUCKERPUNCH | MOVE_RAZORWIND, MOVE_WISH |  |
| aerodactyl / aerodactyl | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True |  | MOVE_DUALWINGBEAT |  |
| aipom / aipom | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_AGILITY, MOVE_IRONTAIL, MOVE_SCREECH | MOVE_MUDBOMB, MOVE_QUICKATTACK |  |
| alomomola / alomomola | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_BOUNCE |  |  |
| amaura / amaura | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True | MOVE_AURORAVEIL, MOVE_ROCKTHROW | MOVE_REFLECTTYPE |  |
| anorith / anorith | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_ROCKSLIDE, MOVE_SWORDSDANCE | MOVE_ACCELEROCK |  |
| archen / archen | MAPPING_BLOCK | 5,6,7,8 | True | MOVE_DOUBLETEAM |  | allyswitch:move-open-risk |
| aron / aron | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_IRONHEAD, MOVE_MUDSLAP |  |  |
| axew / axew | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_AQUATAIL, MOVE_DRAGONPULSE, MOVE_ENDURE | MOVE_BITE |  |
| azurill / azurill | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_SLAM, MOVE_WATERSPORT |  |  |
| bagon / bagon | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ENDURE, MOVE_SHADOWCLAW | MOVE_HEALBELL, MOVE_WISH |  |
| barboach / barboach | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_MUDDYWATER |  |  |
| basculegionf / basculegionf | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_ENDEAVOR, MOVE_LASTRESPECTS |  |  |
| bellsprout / bellsprout | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ACIDSPRAY, MOVE_LEECHLIFE, MOVE_REFLECT, MOVE_SUCKERPUNCH, MOVE_SWORDSDANCE | MOVE_LEECHFANG, MOVE_MORNINGSUN, MOVE_TEETERDANCE |  |
| bergmite / bergmite | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True | MOVE_RECOVER | MOVE_ICESHARD |  |
| bidoof / bidoof | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7 | True | MOVE_DEFENSECURL, MOVE_ROCKCLIMB, MOVE_ROLLOUT | MOVE_BITE, MOVE_NORETREAT |  |
| binacle / binacle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True | MOVE_NIGHTSLASH, MOVE_SANDATTACK |  |  |
| blitzle / blitzle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_SHOCKWAVE |  |  |
| bouffalant / bouffalant | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_ROCKCLIMB |  |  |
| bronzor / bronzor | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_GRAVITY, MOVE_RECYCLE |  |  |
| bruxish / bruxish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_SUPERFANG |  |  |
| buizel / buizel | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True | MOVE_AQUATAIL, MOVE_TAILSLAP | MOVE_MUDSHOT, MOVE_PURSUIT, MOVE_WHIRLPOOL |  |
| bulbasaur / bulbasaur | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_LIGHTSCREEN, MOVE_SAFEGUARD | MOVE_CELEBRATE |  |
| buneary / buneary | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8 | True | MOVE_ATTRACT | MOVE_TRIPLEAXEL |  |
| bunnelby / bunnelby | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True |  | MOVE_STUFFCHEEKS |  |
| cacnea / cacnea | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True |  | MOVE_POWERTRIP |  |
| carnivine / carnivine | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7 | True |  | MOVE_BIND |  |
| castform / castform | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_PSYCHUP |  |  |
| cetoddle / cetoddle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_FLAIL |  |
| chansey / chansey | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_HELPINGHAND, MOVE_NATURALGIFT, MOVE_SUBSTITUTE | MOVE_BESTOW, MOVE_SWEETKISS, MOVE_TRIATTACK, MOVE_WISH |  |
| charmander / charmander | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FLAREBLITZ, MOVE_IRONTAIL, MOVE_ROCKSLIDE, MOVE_SWORDSDANCE | MOVE_CELEBRATE |  |
| chatot / chatot | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7 | True | MOVE_BOOMBURST | MOVE_PARTINGSHOT |  |
| cherubi / cherubi | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8 | True |  | MOVE_SLEEPPOWDER, MOVE_STUNSPORE |  |
| chespin / chespin | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True | MOVE_ROLLOUT, MOVE_SUPERFANG, MOVE_WIDEGUARD |  |  |
| chewtle / chewtle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True | MOVE_SHELLSMASH |  |  |
| chikorita / chikorita | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_AROMATHERAPY, MOVE_BODYSLAM, MOVE_LEAFSTORM |  |  |
| chimchar / chimchar | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True | MOVE_POWERUPPUNCH |  |  |
| chimecho / chimecho | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_DREAMEATER |  |  |
| chinchou / chinchou | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FLAIL, MOVE_SUCKERPUNCH |  |  |
| chingling / chingling | MAPPING_BLOCK | 4,5,6,7,9 | True | MOVE_DREAMEATER, MOVE_RECYCLE |  | allyswitch:move-open-risk |
| clauncher / clauncher | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True | MOVE_AQUAJET, MOVE_BUBBLEBEAM, MOVE_CRABHAMMER |  |  |
| cleffa / cleffa | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_SPLASH, MOVE_SUBSTITUTE | MOVE_COSMICPOWER, MOVE_SOFTBOILED, MOVE_TELEPORT |  |
| clobbopus / clobbopus | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | True |  | MOVE_AQUAJET |  |
| corphish / corphish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ENDEAVOR, MOVE_KNOCKOFF |  |  |
| corsola / corsola | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_AQUARING, MOVE_ROCKSLIDE | MOVE_MUDSPORT |  |
| crabrawler / crabrawler | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_FOCUSPUNCH |  |  |
| cramorant / cramorant | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True | MOVE_AQUACUTTER |  |  |
| cranidos / cranidos | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True | MOVE_LEER | MOVE_BITE |  |
| croagunk / croagunk | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_CROSSCHOP | MOVE_FLATTER |  |
| cryogonal / cryogonal | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_AURORAVEIL, MOVE_EXPLOSION, MOVE_FROSTBREATH |  |  |
| cubone / cubone | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_LEER, MOVE_ROCKSLIDE, MOVE_SWORDSDANCE | MOVE_THRASH |  |
| cyndaquil / cyndaquil | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_CURSE, MOVE_DOUBLEEDGE, MOVE_QUICKATTACK |  |  |
| darumaka / darumaka | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True |  | MOVE_RAGE |  |
| deerling / deerling | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True |  | MOVE_TROPKICK |  |
| deino / deino | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_ASSURANCE | MOVE_SLAM |  |
| delibird / delibird | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_AURORABEAM, MOVE_BESTOW, MOVE_DESTINYBOND, MOVE_FAKEOUT, MOVE_FREEZEDRY, MOVE_ICEPUNCH, MOVE_ICYWIND, MOVE_SPIKES |  |  |
| diglett / diglett | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ASTONISH, MOVE_MUDBOMB, MOVE_ROCKSLIDE |  |  |
| doduo / doduo | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_BRAVEBIRD, MOVE_ENDEAVOR, MOVE_QUICKATTACK, MOVE_SKYATTACK, MOVE_WHIRLWIND | MOVE_DOUBLEEDGE, MOVE_LUNGE, MOVE_UPROAR |  |
| dratini / dratini | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_DRAGONDANCE, MOVE_DRAGONRUSH, MOVE_LIGHTSCREEN |  |  |
| drifloon / drifloon | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_DESTINYBOND, MOVE_TAILWIND |  |  |
| drilbur / drilbur | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_CRUSHCLAW, MOVE_RAPIDSPIN, MOVE_ROCKCLIMB, MOVE_SLASH |  |  |
| drowzee / drowzee | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_NASTYPLOT | MOVE_MINDREADER, MOVE_TELEPORT, MOVE_WISH |  |
| druddigon / druddigon | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_CRUSHCLAW, MOVE_METALCLAW | MOVE_CHIPAWAY |  |
| ducklett / ducklett | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_AIRCUTTER, MOVE_BRINE, MOVE_DIVE, MOVE_ENDEAVOR | MOVE_BUBBLEBEAM, MOVE_WINGATTACK |  |
| dunsparce / dunsparce | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ANCIENTPOWER, MOVE_ROCKSLIDE | MOVE_NORETREAT |  |
| durant / durant | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_ROCKCLIMB |  |  |
| dwebble / dwebble | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True |  | MOVE_FIRSTIMPRESSION |  |
| eevee / eevee | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_CHARM, MOVE_COVET | MOVE_CELEBRATE, MOVE_MIMIC |  |
| eiscue / eiscue | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True | MOVE_ICICLECRASH |  |  |
| ekans / ekans | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_POISONFANG | MOVE_TOXICSPIKES |  |
| electrike / electrike | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_DISCHARGE, MOVE_SHOCKWAVE, MOVE_SPARK, MOVE_THUNDERFANG |  |  |
| elgyem / elgyem | MAPPING_BLOCK | 5,6,7,8 | True | MOVE_PSYCHUP, MOVE_TELEPORT |  | allyswitch:move-open-risk |
| espurr / espurr | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True |  | MOVE_PSYCHICTERRAIN |  |
| exeggcute / exeggcute | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_GIGADRAIN, MOVE_NATURALGIFT, MOVE_PSYCHUP, MOVE_REFLECT, MOVE_SYNTHESIS | MOVE_BESTOW, MOVE_TELEPORT, MOVE_WISH |  |
| farfetchd / farfetchd | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_FEINT, MOVE_LEAFBLADE, MOVE_NIGHTSLASH | MOVE_AIRSLASH, MOVE_WISH, MOVE_YAWN |  |
| feebas / feebas | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_LIGHTSCREEN |  |  |
| fennekin / fennekin | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True | MOVE_COPYCAT, MOVE_MAGICROOM |  |  |
| ferroseed / ferroseed | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_ROCKCLIMB |  |  |
| fidough / fidough | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_LASTRESORT |  |
| flabebe / flabebe | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True | MOVE_ENDEAVOR | MOVE_DAZZLINGGLEAM, MOVE_SOLARBEAM |  |
| fletchling / fletchling | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True | MOVE_TAILWIND | MOVE_RAZORWIND |  |
| flittle / flittle | MAPPING_BLOCK | 9 | True |  |  | allyswitch:move-open-risk |
| fomantis / fomantis | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True | MOVE_SUPERPOWER |  |  |
| foongus / foongus | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_GROWTH, MOVE_STUNSPORE |  |  |
| frillish / frillish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_BUBBLEBEAM, MOVE_RECOVER |  |  |
| froakie / froakie | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True | MOVE_COUNTER, MOVE_RETALIATE, MOVE_SPIKES, MOVE_SWITCHEROO | MOVE_HAPPYHOUR |  |
| gastly / gastly | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_EXPLOSION, MOVE_SMOG, MOVE_TOXIC, MOVE_WILLOWISP |  |  |
| geodude / geodude | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_DYNAMICPUNCH, MOVE_ROCKCLIMB, MOVE_ROCKSLIDE | MOVE_SUCKERPUNCH |  |
| geodudealola / geodudea | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_ROCKCLIMB, MOVE_ZAPCANNON | MOVE_SUCKERPUNCH |  |
| gible / gible | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_METALCLAW, MOVE_MUDSHOT, MOVE_OUTRAGE, MOVE_ROCKCLIMB, MOVE_SANDTOMB |  |  |
| girafarig / girafarig | MAPPING_BLOCK | 3,4,5,6,7,9 | True | MOVE_PSYCHUP, MOVE_UPROAR | MOVE_PSYWAVE, MOVE_RETALIATE | allyswitch:move-open-risk |
| glameow / glameow | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7 | True | MOVE_LASTRESORT, MOVE_WAKEUPSLAP | MOVE_METALCLAW, MOVE_NIGHTSLASH |  |
| gligar / gligar | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ROCKCLIMB | MOVE_CRABHAMMER |  |
| goomy / goomy | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True |  | MOVE_FLAIL |  |
| gothita / gothita | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True |  | MOVE_MAGICPOWDER |  |
| greavard / greavard | MAPPING_BLOCK | 9 | True |  |  | allyswitch:move-open-risk |
| grimer / grimer | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_EXPLOSION |  |  |
| grimeralola / grimera | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_RECYCLE |  |  |
| grookey / grookey | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True | MOVE_STRENGTH |  |  |
| growlithe / growlithe | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_CRUNCH, MOVE_FLAREBLITZ, MOVE_HEATWAVE, MOVE_HOWL, MOVE_SAFEGUARD | MOVE_FLAMEBURST, MOVE_TELEPORT |  |
| growlithehisui / growlitheh | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True | MOVE_HEADSMASH | MOVE_BODYSLAM, MOVE_BURNUP, MOVE_CLOSECOMBAT, MOVE_FIRESPIN, MOVE_FLAMEBURST, MOVE_TELEPORT |  |
| gulpin / gulpin | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_CLEARSMOG, MOVE_DREAMEATER, MOVE_GUNKSHOT, MOVE_STUFFCHEEKS |  |  |
| happiny / happiny | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_LASTRESORT, MOVE_SUBSTITUTE | MOVE_BESTOW |  |
| hatenna / hatenna | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True | MOVE_MYSTICALFIRE |  |  |
| hawlucha / hawlucha | MAPPING_BLOCK | 6,7,8,9 | True |  |  | allyswitch:move-open-risk |
| heatmor / heatmor | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_BODYSLAM | MOVE_BIND |  |
| heracross / heracross | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FALSESWIPE, MOVE_MEGAHORN, MOVE_TAKEDOWN | MOVE_BULLETSEED |  |
| hippopotas / hippopotas | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_SANDTOMB, MOVE_SLACKOFF |  |  |
| honedge / honedge | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True | MOVE_METALSOUND, MOVE_SHADOWSNEAK |  |  |
| hoothoot / hoothoot | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_HURRICANE | MOVE_SYNCHRONOISE, MOVE_ZENHEADBUTT |  |
| hoppip / hoppip | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_PSYCHUP, MOVE_RAGEPOWDER, MOVE_REFLECT, MOVE_SWITCHEROO, MOVE_WORRYSEED |  |  |
| horsea / horsea | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_DRAGONBREATH |  |  |
| houndour / houndour | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_FIREFANG, MOVE_NASTYPLOT, MOVE_PUNISHMENT, MOVE_PURSUIT, MOVE_WILLOWISP | MOVE_EMBARGO, MOVE_FEINTATTACK, MOVE_ODORSLEUTH |  |
| igglybuff / igglybuff | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_LASTRESORT, MOVE_ROLLOUT | MOVE_TELEPORT, MOVE_TRIATTACK |  |
| illumise / illumise | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ATTRACT, MOVE_BUGBUZZ, MOVE_ENCORE, MOVE_ROOST | MOVE_PLAYROUGH, MOVE_TAILGLOW |  |
| impidimp / impidimp | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_PARTINGSHOT |  |  |
| joltik / joltik | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_ROCKCLIMB, MOVE_STRUGGLEBUG | MOVE_BUGBITE, MOVE_FURYCUTTER |  |
| kabuto / kabuto | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_DIG, MOVE_MUDSHOT | MOVE_WRINGOUT |  |
| kangaskhan / kangaskhan | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_FOCUSENERGY, MOVE_SAFEGUARD, MOVE_STOMP, MOVE_SUBSTITUTE | MOVE_HEADBUTT, MOVE_LEER, MOVE_WISH, MOVE_YAWN |  |
| karrablast / karrablast | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_MEGAHORN | MOVE_ACIDSPRAY, MOVE_BUGBUZZ |  |
| kecleon / kecleon | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_CAMOUFLAGE |  |  |
| koffing / koffing | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_DESTINYBOND, MOVE_WILLOWISP |  |  |
| komala / komala | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_SUPERPOWER |  |  |
| krabby / krabby | MAPPING_BLOCK | 3,4,5,6,7,8 | True | MOVE_DIG, MOVE_FLAIL, MOVE_SLAM, MOVE_SWORDSDANCE |  | allyswitch:move-open-risk |
| lapras / lapras | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_SUBSTITUTE |  |  |
| larvesta / larvesta | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_ABSORB, MOVE_STRINGSHOT, MOVE_THRASH |  |  |
| ledyba / ledyba | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_BUGBUZZ, MOVE_SILVERWIND | MOVE_AGILITY |  |
| lickitung / lickitung | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_BELLYDRUM, MOVE_BODYSLAM, MOVE_SUBSTITUTE | MOVE_CHIPAWAY, MOVE_HEALBELL, MOVE_ICEBALL, MOVE_MEFIRST, MOVE_SLAM, MOVE_WISH |  |
| lileep / lileep | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_BIND, MOVE_MEGADRAIN, MOVE_ROCKSLIDE |  |  |
| litleo / litleo | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True |  | MOVE_EXTREMESPEED, MOVE_HEADBUTT |  |
| lotad / lotad | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FLAIL, MOVE_GIGADRAIN | MOVE_NATURALGIFT |  |
| luvdisc / luvdisc | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_AQUARING, MOVE_CAPTIVATE |  |  |
| machop / machop | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_CLOSECOMBAT, MOVE_KNOCKOFF, MOVE_LIGHTSCREEN, MOVE_ROCKSLIDE, MOVE_SUBMISSION | MOVE_MACHPUNCH, MOVE_VITALTHROW |  |
| magby / magby | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FOCUSPUNCH | MOVE_FIRESPIN |  |
| magnemite / magnemite | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_ELECTROWEB, MOVE_EXPLOSION |  |  |
| makuhita / makuhita | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_REVENGE, MOVE_WIDEGUARD | MOVE_STORMTHROW |  |
| mankey / mankey | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_CLOSECOMBAT, MOVE_CURSE, MOVE_ROCKSLIDE, MOVE_SPITE | MOVE_RETALIATE, MOVE_SKULLBASH, MOVE_THUNDEROUSKICK |  |
| mantine / mantine | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_CONFUSERAY, MOVE_HYDROPUMP, MOVE_ROCKSLIDE, MOVE_WIDEGUARD |  |  |
| mantyke / mantyke | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8 | True | MOVE_CONFUSERAY, MOVE_HYDROPUMP, MOVE_ROCKSLIDE, MOVE_WIDEGUARD |  |  |
| maractus / maractus | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_LEECHSEED | MOVE_TAILGLOW |  |
| mareep / mareep | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_CHARGE, MOVE_ELECTROWEB, MOVE_REFLECT, MOVE_SAFEGUARD, MOVE_TAKEDOWN |  |  |
| marill / marill | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_LIGHTSCREEN, MOVE_SUBSTITUTE, MOVE_SUPERPOWER, MOVE_WATERSPORT |  |  |
| mawile / mawile | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_FALSESWIPE, MOVE_PSYCHUP, MOVE_SUCKERPUNCH, MOVE_SWORDSDANCE | MOVE_FEINTATTACK, MOVE_SING |  |
| meditite / meditite | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_DRAINPUNCH |  |  |
| meowth / meowth | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_LASTRESORT, MOVE_PSYCHUP | MOVE_ASSURANCE, MOVE_CAPTIVATE |  |
| meowthalola / meowtha | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True |  | MOVE_ASSURANCE, MOVE_CAPTIVATE, MOVE_NIGHTDAZE |  |
| mienfoo / mienfoo | MAPPING_BLOCK | 5,6,7,8,9 | True | MOVE_ENDURE | MOVE_FURYSWIPES | allyswitch:move-open-risk |
| miltank / miltank | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_DOUBLEEDGE, MOVE_PSYCHUP |  |  |
| mimejr / mimejr | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8 | True | MOVE_MIMIC, MOVE_PSYCHUP, MOVE_TEETERDANCE, MOVE_TICKLE, MOVE_TRICK | MOVE_MEDITATE, MOVE_ROLEPLAY |  |
| minccino / minccino | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True |  | MOVE_BONERUSH |  |
| minun / minun | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_DISCHARGE, MOVE_FAKETEARS, MOVE_SUBSTITUTE |  |  |
| misdreavus / misdreavus | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_PSYCHUP, MOVE_SPITE | MOVE_HYPNOSIS |  |
| mrmime / mrmime | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_MIMIC, MOVE_PSYCHUP, MOVE_TEETERDANCE, MOVE_TICKLE, MOVE_TRICK | MOVE_CHARM, MOVE_FOLLOWME, MOVE_HEALINGWISH, MOVE_MEDITATE, MOVE_MISTYTERRAIN, MOVE_ROLEPLAY, MOVE_TELEPORT |  |
| mrmimegalar / mrmimeg | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | True | MOVE_TICKLE | MOVE_CHARM, MOVE_FUTURESIGHT, MOVE_HEALINGWISH, MOVE_MAGICROOM, MOVE_MEDITATE, MOVE_NASTYPLOT, MOVE_PSYCHICTERRAIN, MOVE_ROLEPLAY, MOVE_WAKEUPSLAP |  |
| mudbray / mudbray | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True | MOVE_ENDEAVOR | MOVE_BIDE |  |
| mudkip / mudkip | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True |  | MOVE_BIDE, MOVE_FORESIGHT, MOVE_MUDSPORT |  |
| munchlax / munchlax | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_LICK, MOVE_SUBSTITUTE |  |  |
| munna / munna | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_MAGICCOAT | MOVE_PSYWAVE, MOVE_SYNCHRONOISE |  |
| murkrow / murkrow | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ASSURANCE, MOVE_FEINTATTACK, MOVE_WINGATTACK | MOVE_AIRCUTTER, MOVE_NIGHTSLASH, MOVE_PUNISHMENT |  |
| natu / natu | MAPPING_BLOCK | 3,4,5,6,7,8 | True | MOVE_PSYCHUP |  | allyswitch:move-open-risk |
| nidoranf / nidoranf | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_POISONFANG | MOVE_SUCKERPUNCH |  |
| nidoranm / nidoranm | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_HORNDRILL, MOVE_POISONTAIL, MOVE_THRASH |  |  |
| noibat / noibat | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8,9 | True | MOVE_TAILWIND |  |  |
| nosepass / nosepass | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_BLOCK, MOVE_EXPLOSION, MOVE_HEADSMASH | MOVE_POWERSHIFT |  |
| numel / numel | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_YAWN | MOVE_FLAMEWHEEL |  |
| oddish / oddish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_STRENGTHSAP, MOVE_SWORDSDANCE | MOVE_LUCKYCHANT |  |
| omanyte / omanyte | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_ROCKSLIDE |  |  |
| onix / onix | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_EXPLOSION, MOVE_ROCKCLIMB, MOVE_ROCKSLIDE, MOVE_STEALTHROCK | MOVE_POWERSHIFT, MOVE_RAGE, MOVE_ROCKTHROW |  |
| oricorio / oricorio | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_ATTRACT, MOVE_CAPTIVATE, MOVE_DEFOG |  |  |
| oricoriopau / oricoriop | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_PLUCK, MOVE_SAFEGUARD, MOVE_TAILWIND |  |
| oricoriopompom / oricorioy | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_PLUCK, MOVE_SAFEGUARD, MOVE_TAILWIND |  |
| oricoriosensu / oricorios | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_PLUCK, MOVE_SAFEGUARD, MOVE_TAILWIND |  |
| oshawott / oshawott | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_AQUACUTTER, MOVE_KNOCKOFF | MOVE_SECRETSWORD |  |
| pachirisu / pachirisu | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True |  | MOVE_EERIEIMPULSE |  |
| pancham / pancham | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True |  | MOVE_KARATECHOP, MOVE_VITALTHROW |  |
| paras / paras | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_FALSESWIPE, MOVE_LIGHTSCREEN, MOVE_METALCLAW |  |  |
| passimian / passimian | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True |  | MOVE_BESTOW, MOVE_COURTCHANGE |  |
| patrat / patrat | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7 | True |  | MOVE_BIDE |  |
| pawmi / pawmi | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_EERIEIMPULSE |  |
| pawniard / pawniard | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_PURSUIT, MOVE_REVENGE | MOVE_EMBARGO, MOVE_FEINTATTACK |  |
| petilil / petilil | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True |  | MOVE_RECOVER |  |
| phantump / phantump | MAPPING_BLOCK | 6,7,8,9 | True |  |  | allyswitch:move-open-risk |
| pichu / pichu | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_VOLTTACKLE | MOVE_CELEBRATE, MOVE_EXTREMESPEED |  |
| pidgey / pidgey | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_AIRSLASH, MOVE_BRAVEBIRD, MOVE_STEELWING |  |  |
| pikachualola / pikachucapalola | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachuhoenn / pikachucaphoenn | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachukalos / pikachucapkalos | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachuoriginal / pikachucaporiginal | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachupartner / pikachucappartner | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachusinnoh / pikachucapsinnoh | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikachuunova / pikachucapunova | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | False | MOVE_CHARGE, MOVE_DISARMINGVOICE, MOVE_FAKEOUT, MOVE_FLAIL, MOVE_PRESENT, MOVE_TICKLE, MOVE_WISH |  |  |
| pikipek / pikipek | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_BRAVEBIRD, MOVE_GUNKSHOT, MOVE_SKYATTACK |  |  |
| pineco / pineco | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_DOUBLEEDGE, MOVE_REFLECT |  |  |
| pinsir / pinsir | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_BUGBITE, MOVE_FALSESWIPE, MOVE_SUPERPOWER, MOVE_THRASH | MOVE_REVENGE |  |
| piplup / piplup | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True | MOVE_BIDE, MOVE_HYDROPUMP, MOVE_ROOST | MOVE_HAZE |  |
| plusle / plusle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_CHARM, MOVE_DISCHARGE, MOVE_SUBSTITUTE |  |  |
| poliwag / poliwag | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_BUBBLEBEAM, MOVE_MUDDYWATER, MOVE_MUDSHOT, MOVE_WATERSPORT |  |  |
| ponyta / ponyta | MAPPING_BLOCK | 3,4,5,6,7,8 | True | MOVE_FLAMEWHEEL |  | allyswitch:move-open-risk |
| ponytagalar / ponytag | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | True |  | MOVE_HEALINGWISH |  |
| poochyena / poochyena | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_PLAYROUGH, MOVE_SUCKERPUNCH, MOVE_YAWN |  |  |
| psyduck / psyduck | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_LIGHTSCREEN, MOVE_PSYCHIC | MOVE_MUDSPORT, MOVE_TRIATTACK |  |
| purrloin / purrloin | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_SLASH | MOVE_NIGHTDAZE |  |
| qwilfish / qwilfish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_BRINE, MOVE_POISONJAB, MOVE_WATERPULSE | MOVE_ANCHORSHOT, MOVE_ROLLOUT, MOVE_TAKEDOWN |  |
| qwilfishhisui / qwilfishh | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True | MOVE_WATERPULSE | MOVE_ICEBALL, MOVE_ROLLOUT, MOVE_SIGNALBEAM, MOVE_TAKEDOWN |  |
| ralts / ralts | MAPPING_BLOCK | 3,4,5,6,7,8,9 | True | MOVE_MYSTICALFIRE, MOVE_WILLOWISP | MOVE_FUTURESIGHT | allyswitch:move-open-risk |
| rattata / rattata | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_BITE, MOVE_LASTRESORT, MOVE_SWAGGER | MOVE_TAKEDOWN |  |
| relicanth / relicanth | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_AQUATAIL, MOVE_ROCKSLIDE |  |  |
| remoraid / remoraid | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_AURORABEAM, MOVE_THUNDERWAVE, MOVE_WATERPULSE |  |  |
| rhyhorn / rhyhorn | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ROCKCLIMB, MOVE_ROCKSLIDE, MOVE_SWORDSDANCE | MOVE_HEADSMASH |  |
| riolu / riolu | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True |  | MOVE_MACHPUNCH |  |
| roselia / roselia | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_GIGADRAIN, MOVE_GRASSWHISTLE, MOVE_SYNTHESIS | MOVE_SWEETKISS |  |
| rowlet / rowlet | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True | MOVE_DOUBLETEAM, MOVE_OMINOUSWIND, MOVE_ROOST |  |  |
| rufflet / rufflet | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_ROCKSMASH, MOVE_ROOST |  |  |
| sableye / sableye | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_MEANLOOK, MOVE_PSYCHUP | MOVE_NIGHTMARE |  |
| sandile / sandile | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_POWERTRIP, MOVE_ROCKCLIMB | MOVE_ASSURANCE, MOVE_MUDSLAP |  |
| sandshrew / sandshrew | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_RAPIDSPIN, MOVE_ROCKCLIMB, MOVE_ROCKSLIDE, MOVE_SAFEGUARD, MOVE_SWORDSDANCE |  |  |
| sandshrewalola / sandshrewa | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True | MOVE_ICESHARD, MOVE_METALCLAW, MOVE_MIRRORCOAT |  |  |
| sandygast / sandygast | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True |  | MOVE_STRENGTHSAP |  |
| scatterbug / scatterbug | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | False | MOVE_POISONPOWDER, MOVE_RAGEPOWDER, MOVE_STUNSPORE |  |  |
| scraggy / scraggy | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_FAKEOUT, MOVE_POWERUPPUNCH | MOVE_BEATUP, MOVE_CHIPAWAY, MOVE_FOCUSPUNCH |  |
| scyther / scyther | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FEINT, MOVE_LIGHTSCREEN, MOVE_NIGHTSLASH, MOVE_SAFEGUARD | MOVE_DUALWINGBEAT, MOVE_PURSUIT, MOVE_VACUUMWAVE |  |
| seedot / seedot | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FALSESWIPE |  |  |
| seel / seel | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ENCORE |  |  |
| sentret / sentret | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_COVET, MOVE_LASTRESORT, MOVE_SUBSTITUTE |  |  |
| seviper / seviper | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_ASSURANCE, MOVE_NIGHTSLASH, MOVE_WRINGOUT | MOVE_SUCKERPUNCH |  |
| sewaddle / sewaddle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_SNORE, MOVE_SWITCHEROO, MOVE_SYNTHESIS, MOVE_WORRYSEED |  |  |
| shellos / shellos | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_BRINE, MOVE_MEMENTO |  |  |
| shinx / shinx | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_BABYDOLLEYES, MOVE_THUNDERFANG | MOVE_DISCHARGE |  |
| shroomish / shroomish | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_FALSESWIPE, MOVE_SEEDBOMB, MOVE_SWAGGER, MOVE_WORRYSEED |  |  |
| shuppet / shuppet | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_PAYBACK, MOVE_PHANTOMFORCE, MOVE_SHADOWSNEAK | MOVE_COTTONGUARD |  |
| sigilyph / sigilyph | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_SKILLSWAP | MOVE_MIRRORMOVE |  |
| sinistea / sinistea | MAPPING_BLOCK | 9 | False |  |  | allyswitch:move-open-risk |
| sizzlipede / sizzlipede | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8 | True |  | MOVE_BURNUP |  |
| skarmory / skarmory | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_BRAVEBIRD, MOVE_DRILLPECK, MOVE_NIGHTSLASH | MOVE_AIRSLASH, MOVE_COUNTER, MOVE_SWIFT |  |
| skiddo / skiddo | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,9 | True | MOVE_MILKDRINK |  |  |
| skitty / skitty | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_CAPTIVATE, MOVE_FAKEOUT, MOVE_LASTRESORT, MOVE_PSYCHUP, MOVE_SUBSTITUTE | MOVE_PAYDAY, MOVE_SWEETKISS |  |
| skorupi / skorupi | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8 | True | MOVE_NIGHTSLASH, MOVE_PURSUIT |  |  |
| slakoth / slakoth | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True |  | MOVE_RETALIATE, MOVE_SUCKERPUNCH |  |
| slowpoke / slowpoke | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_SAFEGUARD, MOVE_ZENHEADBUTT | MOVE_TELEPORT |  |
| slowpokegalar / slowpokeg | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 8,9 | True |  | MOVE_FUTURESIGHT, MOVE_TELEPORT |  |
| slugma / slugma | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_EARTHPOWER |  |  |
| smoochum / smoochum | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_ICEPUNCH, MOVE_PSYCHUP, MOVE_ROLEPLAY |  |  |
| sneasel / sneasel | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_AVALANCHE, MOVE_ICEPUNCH, MOVE_ICESHARD, MOVE_PUNISHMENT, MOVE_REFLECT |  |  |
| sneaselhisui / sneaselh | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True | MOVE_NIGHTSLASH, MOVE_QUICKGUARD, MOVE_SWITCHEROO | MOVE_ASSIST, MOVE_CRUSHCLAW, MOVE_FOCUSENERGY, MOVE_PURSUIT, MOVE_SPITE, MOVE_SWIFT, MOVE_THROATCHOP |  |
| snivy / snivy | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,9 | True | MOVE_SYNTHESIS |  |  |
| snorlax / snorlax | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_BELCH, MOVE_LICK, MOVE_SUBSTITUTE | MOVE_ICEBALL |  |
| snorunt / snorunt | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_FAKETEARS | MOVE_DOUBLEEDGE, MOVE_POWDERSNOW |  |
| snover / snover | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_MIST |  |  |
| snubbull / snubbull | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_COUNTER, MOVE_CRUNCH, MOVE_FIREFANG, MOVE_ICEFANG, MOVE_REFLECT, MOVE_RETALIATE, MOVE_THUNDERFANG |  |  |
| spearow / spearow | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_FALSESWIPE |  |  |
| spheal / spheal | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_ROCKSLIDE, MOVE_ROLLOUT | MOVE_CHILLINGWATER |  |
| spinarak / spinarak | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_MEGAHORN, MOVE_POISONJAB | MOVE_FIRSTIMPRESSION |  |
| spinda / spinda | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_ROCKSLIDE |  |  |
| spiritomb / spiritomb | MAPPING_BLOCK | 4,5,6,7,8,9 | True | MOVE_SHADOWSNEAK |  | allyswitch:move-open-risk |
| spoink / spoink | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_SUBSTITUTE, MOVE_ZENHEADBUTT | MOVE_PAYBACK, MOVE_RECOVER |  |
| sprigatito / sprigatito | MAPPING_BLOCK | 9 | True |  |  | allyswitch:move-open-risk |
| spritzee / spritzee | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True |  | MOVE_DISARMINGVOICE |  |
| squawkabillyblue / squawkabillyblue | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_DOUBLEEDGE, MOVE_FINALGAMBIT, MOVE_FLATTER, MOVE_PARTINGSHOT |  |
| squawkabillywhite / squawkabillywhite | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_DOUBLEEDGE, MOVE_FINALGAMBIT, MOVE_FLATTER, MOVE_PARTINGSHOT |  |
| squawkabillyyellow / squawkabillyyellow | UNVERIFIABLE_FROM_SELECTED_REFERENCE |  | True |  | MOVE_DOUBLEEDGE, MOVE_FINALGAMBIT, MOVE_FLATTER, MOVE_PARTINGSHOT |  |
| squirtle / squirtle | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True |  | MOVE_CELEBRATE, MOVE_FOLLOWME |  |
| stantler / stantler | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_DOUBLEKICK, MOVE_MEGAHORN, MOVE_PSYCHUP, MOVE_SWAGGER, MOVE_ZENHEADBUTT | MOVE_CAPTIVATE, MOVE_ENTRAINMENT, MOVE_IMPRISON |  |
| stufful / stufful | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8 | True | MOVE_ENDURE |  |  |
| stunfisk / stunfisk | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_EARTHPOWER, MOVE_SHOCKWAVE | MOVE_SHOREUP |  |
| stunky / stunky | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,8,9 | True | MOVE_SLASH | MOVE_MEMENTO |  |
| sunkern / sunkern | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_GRASSWHISTLE, MOVE_INGRAIN, MOVE_LEECHSEED, MOVE_NATURALGIFT |  |  |
| surskit / surskit | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_AQUAJET | MOVE_MUDSPORT, MOVE_SOAK |  |
| swablu / swablu | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ASTONISH, MOVE_DEFOG, MOVE_HYPERVOICE, MOVE_TAILWIND |  |  |
| swinub / swinub | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ROCKSLIDE, MOVE_TAKEDOWN |  |  |
| tadbulb / tadbulb | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_EERIEIMPULSE |  |
| taillow / taillow | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_BRAVEBIRD, MOVE_STEELWING | MOVE_FEATHERDANCE |  |
| tangela / tangela | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_GIGADRAIN, MOVE_MEGADRAIN, MOVE_NATURALGIFT, MOVE_REFLECT | MOVE_ACIDSPRAY, MOVE_DOUBLEHIT, MOVE_MORNINGSUN |  |
| tauros / tauros | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_CURSE, MOVE_ENDEAVOR |  |  |
| teddiursa / teddiursa | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_FAKETEARS, MOVE_FURYCUTTER, MOVE_PLAYROUGH |  |  |
| tentacool / tentacool | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_SAFEGUARD | MOVE_BARRIER |  |
| timburr / timburr | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True |  | MOVE_SLAM |  |
| tinkatink / tinkatink | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_SLAM |  |
| tirtouga / tirtouga | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_IRONDEFENSE |  |  |
| togedemaru / togedemaru | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8 | True |  | MOVE_EERIEIMPULSE |  |
| togepi / togepi | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_AERIALACE, MOVE_PSYCHUP, MOVE_SUBSTITUTE | MOVE_BESTOW, MOVE_SOFTBOILED |  |
| torchic / torchic | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ENDURE, MOVE_FEATHERDANCE, MOVE_LASTRESORT, MOVE_PECK, MOVE_REVERSAL, MOVE_ROCKSLIDE, MOVE_SWAGGER | MOVE_FIRESPIN, MOVE_SANDATTACK |  |
| torkoal / torkoal | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_CLEARSMOG, MOVE_EARTHQUAKE, MOVE_ERUPTION, MOVE_FLAIL |  |  |
| totodile / totodile | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_AQUAJET, MOVE_COUNTER, MOVE_CRUNCH, MOVE_DRAGONCLAW, MOVE_HYDROPUMP, MOVE_ROCKSLIDE, MOVE_THRASH |  |  |
| trapinch / trapinch | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_EARTHPOWER, MOVE_FEINT |  |  |
| treecko / treecko | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_ENDEAVOR, MOVE_LEAFSTORM, MOVE_NIGHTSLASH, MOVE_SLASH | MOVE_AGILITY, MOVE_PURSUIT |  |
| tropius / tropius | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_LEAFSTORM, MOVE_NATURALGIFT, MOVE_SYNTHESIS |  |  |
| turtwig / turtwig | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 4,5,6,7,9 | True | MOVE_SHELLSMASH | MOVE_LEAFBLADE, MOVE_SLEEPPOWDER |  |
| tympole / tympole | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_EARTHPOWER |  |  |
| tyrogue / tyrogue | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_HELPINGHAND |  |  |
| tyrunt / tyrunt | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 6,7,8 | True | MOVE_ROCKTHROW |  |  |
| venipede / venipede | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8 | True | MOVE_ROCKCLIMB, MOVE_TAKEDOWN |  |  |
| venonat / venonat | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_BUGBITE, MOVE_VENOSHOCK |  |  |
| volbeat / volbeat | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_COUNTER, MOVE_LUNGE, MOVE_ROOST, MOVE_SWAGGER |  |  |
| voltorb / voltorb | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_METALSOUND, MOVE_RECYCLE |  |  |
| voltorbhisui / voltorbh | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | False | MOVE_LEECHSEED, MOVE_RECYCLE, MOVE_WORRYSEED |  |  |
| vullaby / vullaby | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True | MOVE_FOULPLAY | MOVE_FEINTATTACK |  |
| vulpix / vulpix | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_DISABLE, MOVE_ENERGYBALL, MOVE_EXTRASENSORY, MOVE_HEX, MOVE_PSYCHUP, MOVE_SPITE |  |  |
| vulpixalola / vulpixa | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8,9 | True | MOVE_DISABLE, MOVE_EXTRASENSORY, MOVE_SPITE | MOVE_FEINTATTACK, MOVE_QUICKATTACK |  |
| wailmer / wailmer | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_BODYSLAM, MOVE_ROLLOUT, MOVE_SWAGGER |  |  |
| wattrel / wattrel | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_EERIEIMPULSE |  |
| whismur / whismur | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_SWAGGER | MOVE_TEETERDANCE |  |
| wingull / wingull | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_AERIALACE, MOVE_AGILITY, MOVE_AIRCUTTER, MOVE_KNOCKOFF, MOVE_MIST, MOVE_ROOST | MOVE_FLING |  |
| wishiwashi / wishiwashi | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,8 | True | MOVE_TAKEDOWN |  |  |
| wooper / wooper | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8,9 | True | MOVE_MUDSPORT, MOVE_SAFEGUARD |  |  |
| wooperpaldea / wooperp | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_BODYSLAM, MOVE_EERIEIMPULSE, MOVE_GUARDSWAP |  |
| yamask / yamask | MAPPING_BLOCK | 5,6,7,8 | True | MOVE_CRAFTYSHIELD, MOVE_DISABLE | MOVE_OMINOUSWIND | allyswitch:move-open-risk |
| yanma / yanma | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,9 | True | MOVE_LEECHLIFE, MOVE_PURSUIT, MOVE_SILVERWIND | MOVE_GUST, MOVE_LEECHFANG, MOVE_STRINGSHOT |  |
| yungoos / yungoos | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 7,9 | True | MOVE_ENDEAVOR, MOVE_LASTRESORT |  |  |
| zangoose / zangoose | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7 | True | MOVE_FURYSWIPES, MOVE_NIGHTSLASH, MOVE_ROAR |  |  |
| zigzagoon / zigzagoon | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_EXTREMESPEED, MOVE_ROCKCLIMB, MOVE_SUBSTITUTE | MOVE_BESTOW |  |
| zorua / zorua | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 5,6,7,8,9 | True |  | MOVE_EMBARGO, MOVE_FEINTATTACK |  |
| zoruahisui / zoruah | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 9 | True |  | MOVE_HAPPYHOUR |  |
| zubat / zubat | UNVERIFIABLE_FROM_SELECTED_REFERENCE | 3,4,5,6,7,8 | True | MOVE_WINGATTACK |  |  |

Local egg entries without safe general species mapping: basculinblue, basculinh, basculinred, deerlingautumn, deerlingsummer, deerlingwinter, flabebeblue, flabebeorange, flabebewhite, flabebeyellow, pumpkabool, pumpkaboom, pumpkabooxl, shelloseast, species, tatsugirired, tatsugiriyellow.

## Appendix H — exact TM/HM order and complete positive disagreement sets

Ordered move-list SHA-256: `1b10d4dcda17781fbeea3d904a70c6d0dbbdf13b997735d4c32b265921633998`. Source-reconstructed bitset SHA-256: `104a1f03d198ea5376c12243e0b2b1c3a3504c3b1e1b4c240e99ec25af054d9a`. These hashes cover source normalization, not a ROM or build artifact.

| 1-based slot | Move |
| --- | --- |
| 1 | MOVE_FOCUSPUNCH |
| 2 | MOVE_DRAGONCLAW |
| 3 | MOVE_WATERPULSE |
| 4 | MOVE_CALMMIND |
| 5 | MOVE_ROAR |
| 6 | MOVE_TOXIC |
| 7 | MOVE_LOWKICK |
| 8 | MOVE_BULKUP |
| 9 | MOVE_BULLETSEED |
| 10 | MOVE_HIDDENPOWER |
| 11 | MOVE_SUNNYDAY |
| 12 | MOVE_TAUNT |
| 13 | MOVE_ICEBEAM |
| 14 | MOVE_BLIZZARD |
| 15 | MOVE_HYPERBEAM |
| 16 | MOVE_LIGHTSCREEN |
| 17 | MOVE_PROTECT |
| 18 | MOVE_RAINDANCE |
| 19 | MOVE_GIGADRAIN |
| 20 | MOVE_SAFEGUARD |
| 21 | MOVE_FRUSTRATION |
| 22 | MOVE_SOLARBEAM |
| 23 | MOVE_IRONTAIL |
| 24 | MOVE_THUNDERBOLT |
| 25 | MOVE_THUNDER |
| 26 | MOVE_EARTHQUAKE |
| 27 | MOVE_RETURN |
| 28 | MOVE_DIG |
| 29 | MOVE_PSYCHIC |
| 30 | MOVE_SHADOWBALL |
| 31 | MOVE_BRICKBREAK |
| 32 | MOVE_DOUBLETEAM |
| 33 | MOVE_REFLECT |
| 34 | MOVE_SHOCKWAVE |
| 35 | MOVE_FLAMETHROWER |
| 36 | MOVE_SLUDGEBOMB |
| 37 | MOVE_SANDSTORM |
| 38 | MOVE_FIREBLAST |
| 39 | MOVE_ROCKTOMB |
| 40 | MOVE_AERIALACE |
| 41 | MOVE_TORMENT |
| 42 | MOVE_FACADE |
| 43 | MOVE_SECRETPOWER |
| 44 | MOVE_REST |
| 45 | MOVE_ATTRACT |
| 46 | MOVE_THIEF |
| 47 | MOVE_STEELWING |
| 48 | MOVE_SKILLSWAP |
| 49 | MOVE_LEECHFANG |
| 50 | MOVE_OVERHEAT |
| 51 | MOVE_ROOST |
| 52 | MOVE_FOCUSBLAST |
| 53 | MOVE_ENERGYBALL |
| 54 | MOVE_FALSESWIPE |
| 55 | MOVE_BRINE |
| 56 | MOVE_HONECLAWS |
| 57 | MOVE_CHARGEBEAM |
| 58 | MOVE_ENDURE |
| 59 | MOVE_DRAGONPULSE |
| 60 | MOVE_DRAINPUNCH |
| 61 | MOVE_WILLOWISP |
| 62 | MOVE_SILVERWIND |
| 63 | MOVE_VENOSHOCK |
| 64 | MOVE_EXPLOSION |
| 65 | MOVE_SHADOWCLAW |
| 66 | MOVE_PAYBACK |
| 67 | MOVE_RECYCLE |
| 68 | MOVE_GIGAIMPACT |
| 69 | MOVE_ROCKPOLISH |
| 70 | MOVE_FLASH |
| 71 | MOVE_STONEEDGE |
| 72 | MOVE_AVALANCHE |
| 73 | MOVE_THUNDERWAVE |
| 74 | MOVE_GYROBALL |
| 75 | MOVE_SWORDSDANCE |
| 76 | MOVE_STEALTHROCK |
| 77 | MOVE_FLAMECHARGE |
| 78 | MOVE_LOWSWEEP |
| 79 | MOVE_DARKPULSE |
| 80 | MOVE_ROCKSLIDE |
| 81 | MOVE_XSCISSOR |
| 82 | MOVE_SLEEPTALK |
| 83 | MOVE_SCALD |
| 84 | MOVE_POISONJAB |
| 85 | MOVE_DREAMEATER |
| 86 | MOVE_GRASSKNOT |
| 87 | MOVE_SWAGGER |
| 88 | MOVE_PLUCK |
| 89 | MOVE_UTURN |
| 90 | MOVE_SUBSTITUTE |
| 91 | MOVE_FLASHCANNON |
| 92 | MOVE_VOLTSWITCH |
| 93 | MOVE_DRAGONTAIL |
| 94 | MOVE_INCINERATE |
| 95 | MOVE_STRUGGLEBUG |
| 96 | MOVE_BULLDOZE |
| 97 | MOVE_FROSTBREATH |
| 98 | MOVE_WORKUP |
| 99 | MOVE_WILDCHARGE |
| 100 | MOVE_INFESTATION |
| 101 | MOVE_POWERUPPUNCH |
| 102 | MOVE_DAZZLINGGLEAM |
| 103 | MOVE_SLUDGEWAVE |
| 104 | MOVE_PSYSHOCK |
| 105 | MOVE_BRUTALSWING |
| 106 | MOVE_SMARTSTRIKE |
| 107 | MOVE_ACROBATICS |
| 108 | MOVE_SNARL |
| 109 | MOVE_DEFOG |
| 110 | MOVE_DRAININGKISS |
| 111 | MOVE_SMACKDOWN |
| 112 | MOVE_ROUND |
| 113 | MOVE_ECHOEDVOICE |
| 114 | MOVE_NATURALGIFT |
| 115 | MOVE_QUASH |
| 116 | MOVE_TRICKROOM |
| 117 | MOVE_FLING |
| 118 | MOVE_AURORAVEIL |
| 119 | MOVE_SKYDROP |
| 120 | MOVE_NATUREPOWER |
| 121 | MOVE_CUT |
| 122 | MOVE_FLY |
| 123 | MOVE_SURF |
| 124 | MOVE_STRENGTH |
| 125 | MOVE_DIVE |
| 126 | MOVE_ROCKSMASH |
| 127 | MOVE_WATERFALL |
| 128 | MOVE_ROCKCLIMB |

Exception sets use **decimal local DPE species IDs**, inclusive ranges. Resolve against pinned `include/species.h` and Appendix A; the helper JSON gives every source key. Every set is complete. Unverifiable absent/absent pairs are counted but are not disagreements. LOCAL_POSITIVE project-policy rows contain older same-method or cross-method evidence; REF-positive/local-negative remains unverifiable without the aggregate contract. The selected-generation match count is 27,841, with 13,777 historical same-method and 356 cross-method positive policy candidates.

| Slot / move | Classification and direction | Records | Complete local species-ID set |
| --- | --- | --- | --- |
| 1 / MOVE_FOCUSPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 68 | 31, 34, 63–68, 104–106, 108, 113, 115, 122, 124, 127, 156, 165–166, 176, 241, 277, 306, 308, 317, 355, 384, 410, 453, 480–481, 492, 516, 521, 537, 558, 564–569, 584, 589–592, 607–608, 684, 768, 782–783, 920, 976–977, 1004, 1011, 1019, 1039–1042, 1078, 1087, 1158, 1220 |
| 1 / MOVE_FOCUSPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 1084, 1088–1092, 1144–1145, 1154, 1229–1230 |
| 1 / MOVE_FOCUSPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 45 | 60, 284, 399–400, 697, 746, 870–872, 875–879, 882–884, 887, 889–892, 894–897, 906, 909, 912, 914–916, 999–1000, 1261–1262, 1264, 1266–1267, 1271, 1274, 1288, 1292–1293, 1358 |
| 2 / MOVE_DRAGONCLAW | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 333, 462, 870–871, 881, 889–890, 896, 901, 905, 907–909, 911, 913, 1261, 1291, 1430, 1432 |
| 3 / MOVE_WATERPULSE | PROJECT_POLICY:LOCAL_POSITIVE | 113 | 29–34, 52–53, 98–99, 108, 115, 118–121, 124, 128, 138–141, 143, 150, 174–176, 206, 222–224, 226, 238, 241, 248, 251, 288–289, 308, 313–317, 322, 330–331, 341–343, 350, 364–366, 370–376, 380–385, 390–391, 406, 453, 480–481, 484–485, 493, 495, 499, 502–503, 511, 516, 521, 568–569, 588–590, 617–618, 635–637, 645–646, 671, 796–797, 806–807, 820–822, 963, 985, 997, 1001, 1005, 1029–1030, 1249, 1378–1379 |
| 3 / MOVE_WATERPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 403, 1144–1145, 1156, 1174–1175, 1225 |
| 3 / MOVE_WATERPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 35 | 839, 872, 876, 878, 880, 882–883, 889, 892, 894, 896, 899, 903–904, 907–908, 910–912, 914–915, 1191–1192, 1202, 1262, 1265, 1268–1269, 1271, 1276, 1279, 1358, 1436–1438 |
| 4 / MOVE_CALMMIND | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 593–594, 774, 868, 932 |
| 4 / MOVE_CALMMIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 175–176, 1079–1080 |
| 4 / MOVE_CALMMIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 30 | 746, 875–876, 882–883, 893–894, 897, 902–903, 907–908, 910, 914, 916–918, 991, 1037, 1101, 1270, 1278, 1287, 1289, 1413, 1433, 1435–1438 |
| 5 / MOVE_ROAR | PROJECT_POLICY:LOCAL_POSITIVE | 75 | 31, 34, 95, 115, 131, 142, 145, 208, 216–217, 249–250, 289, 313–314, 331, 337–338, 342–343, 370–372, 382–384, 496–498, 500, 505, 538, 559–561, 607–608, 619–620, 657, 674, 782–783, 804–807, 821, 824, 976–977, 989–990, 993, 997, 1002, 1004, 1009, 1048–1064 |
| 5 / MOVE_ROAR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 16 | 403, 820, 1078, 1120, 1127–1128, 1154, 1172–1175, 1226–1227, 1229–1230, 1249 |
| 5 / MOVE_ROAR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 53 | 2, 126, 283–284, 520, 576, 696–697, 699, 737, 752–753, 869–872, 878, 880–881, 884–885, 888–892, 896, 898–901, 905, 907–911, 913–914, 1101, 1260–1262, 1269–1270, 1291–1292, 1430, 1432–1433, 1436–1438 |
| 6 / MOVE_TOXIC | PROJECT_POLICY:LOCAL_POSITIVE | 780 | 4–9, 12, 25–42, 50–68, 74–87, 90–91, 95, 98–108, 111–128, 130–131, 133–150, 152–164, 169–181, 183–193, 196, 198–200, 203–205, 208–210, 212–227, 230–234, 236–251, 277–289, 295–303, 309–314, 318–359, 361–366, 369–372, 376–378, 380–384, 386–397, 399–411, 440–451, 455–464, 470–483, 486, 489–493, 496–505, 509–524, 526–556, 559–563, 570–602, 604–623, 625–642, 645–654, 656–681, 684–702, 718–735, 747–750, 752–771, 774–783, 785–797, 800–812, 815–816, 818–830, 832, 834, 848, 868, 919–920, 932, 939–963, 966–973, 976–990, 992–1005, 1008–1017, 1019, 1022–1033, 1037, 1039–1046, 1048–1065, 1074–1078, 1082–1084, 1093–1099, 1158, 1220, 1238, 1241–1242, 1246–1253, 1375, 1377, 1380 |
| 6 / MOVE_TOXIC | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 231 | 713–717, 837, 1079–1080, 1088–1092, 1102–1115, 1117–1131, 1133–1140, 1142–1157, 1159–1160, 1162–1181, 1183–1190, 1203, 1208–1215, 1217, 1221–1223, 1225–1227, 1229–1230, 1232–1237, 1244–1245, 1255, 1258–1259, 1294–1331, 1333–1336, 1339–1340, 1343–1357, 1361–1362, 1365–1372, 1381–1390, 1392–1411, 1413–1418, 1422 |
| 6 / MOVE_TOXIC | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 81 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1207, 1260–1273, 1284–1285, 1436–1439 |
| 7 / MOVE_LOWKICK | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 568–569 |
| 7 / MOVE_LOWKICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 201 | 7–9, 72–73, 79–80, 86–87, 90–91, 98–99, 113, 116–121, 124, 130–131, 134, 138–140, 144–148, 170–171, 183–184, 194–195, 199, 211, 220–222, 225–226, 230, 238, 242, 245, 249, 295–297, 309–310, 313–314, 323–331, 341–343, 346–348, 350, 373–376, 381, 385, 402, 404, 446–448, 475–476, 493, 509–512, 524, 526, 531, 537, 542–543, 546, 554–556, 588–589, 633–637, 645–647, 668, 699, 720–735, 752–753, 798–799, 806–807, 811, 814, 820–821, 824, 827, 834, 920, 945–947, 957, 963–965, 984–985, 988–990, 1025–1026, 1048–1064, 1156, 1158, 1165, 1167, 1175, 1188, 1210, 1215–1216, 1220, 1224–1225, 1239, 1241, 1248–1249, 1255, 1257, 1368–1370, 1382, 1388, 1393–1395, 1400 |
| 7 / MOVE_LOWKICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 221 | 27–28, 56–57, 66–68, 77–78, 84–85, 96–97, 103–107, 125–126, 157, 180–181, 185, 190, 203, 209–210, 214, 216–217, 236–237, 239–240, 248, 277–282, 299–300, 307, 322, 335–336, 344–345, 352, 356–357, 365–366, 371–372, 380, 384, 391, 410, 443–445, 477, 480–481, 491, 500–501, 506–507, 519–520, 528, 552–553, 575–576, 584–587, 591–592, 595, 605–606, 612–613, 618, 624, 664–665, 672–673, 675–678, 684, 701, 746, 758–760, 762–763, 765–766, 768, 782–783, 797, 803, 809, 839, 878, 882–884, 887, 889–892, 894, 896–897, 912, 914–917, 941, 944, 966–967, 977, 980, 983, 992, 999–1001, 1012, 1019, 1037, 1039–1042, 1078, 1102–1107, 1151–1154, 1166, 1172, 1174, 1183–1185, 1208–1209, 1213–1214, 1222, 1238, 1240, 1242, 1245, 1250, 1253, 1256, 1266, 1274–1275, 1288, 1292–1293, 1295–1296, 1300–1302, 1307, 1309, 1311–1315, 1338, 1349, 1367, 1375–1377, 1380, 1385, 1389, 1392, 1398, 1404–1405, 1407, 1412–1413, 1419, 1422, 1426–1429 |
| 8 / MOVE_BULKUP | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 758 |
| 8 / MOVE_BULKUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 1413 |
| 8 / MOVE_BULKUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 125, 519, 552, 737, 879, 882–883, 887, 891–892, 894, 897, 909, 911, 914, 916, 1072, 1231, 1266, 1274–1275, 1277, 1288, 1292–1293, 1358 |
| 9 / MOVE_BULLETSEED | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 46–47, 466, 508 |
| 9 / MOVE_BULLETSEED | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 557–558, 564–565, 709–710 |
| 9 / MOVE_BULLETSEED | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 21 | 548–550, 595, 625, 693, 751, 869, 887, 890, 915, 1204, 1260, 1274, 1281–1282, 1426–1429, 1431 |
| 10 / MOVE_HIDDENPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 845 | 1–9, 12, 23–45, 48–128, 130–131, 133–164, 167–200, 203–234, 236–251, 277–289, 295–303, 306–307, 309–314, 318–359, 361–372, 376–384, 386–397, 399–411, 440–451, 455–464, 469–483, 486–493, 495–507, 509–556, 559–563, 570–602, 604–654, 656–702, 718–735, 747–750, 752–771, 774–783, 785–830, 832, 834, 848, 868, 919–920, 932, 939–987, 989–990, 992–1005, 1008–1019, 1022–1035, 1037, 1039–1046, 1048–1065, 1074–1078, 1082, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 10 / MOVE_HIDDENPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 259 | 713–717, 773, 837, 1073, 1079–1080, 1083–1084, 1088–1092, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 10 / MOVE_HIDDENPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 74 | 465, 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 11 / MOVE_SUNNYDAY | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 245, 1023–1024 |
| 11 / MOVE_SUNNYDAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 713–717, 837 |
| 11 / MOVE_SUNNYDAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 94 | 575–576, 582–583, 630–632, 675–676, 691, 697, 737, 746, 751, 833, 838, 869–871, 873–891, 893–897, 900–903, 905–909, 911–914, 916–918, 1000–1001, 1017, 1072, 1101, 1207, 1231, 1260–1261, 1263, 1265–1267, 1270–1272, 1274–1275, 1277, 1280–1282, 1284–1286, 1426–1429, 1431–1433, 1436–1438 |
| 12 / MOVE_TAUNT | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 758 |
| 12 / MOVE_TAUNT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 1255 |
| 12 / MOVE_TAUNT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 52 | 62, 106–107, 125–126, 239, 300, 386, 576, 737, 839, 875, 877, 880–883, 885, 888–889, 893–897, 899, 902–904, 916, 1072, 1204, 1231, 1265, 1267, 1274–1277, 1284–1285, 1288, 1290, 1292–1293, 1358, 1426–1429, 1433–1434 |
| 13 / MOVE_ICEBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 40 | 839, 872, 876, 878, 880, 882–883, 889, 892, 895–896, 899, 901, 903–904, 907–908, 910–912, 915, 917, 1023–1024, 1047, 1191–1192, 1202, 1231, 1262, 1268–1269, 1271, 1273, 1276, 1279, 1358, 1436–1438 |
| 14 / MOVE_BLIZZARD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 839, 872, 876, 878, 880, 882–883, 889, 892, 896, 899, 903–904, 910–912, 915, 917, 1191–1192, 1202, 1231, 1262, 1268–1269, 1271, 1276, 1279, 1358 |
| 15 / MOVE_HYPERBEAM | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 299 |
| 15 / MOVE_HYPERBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 837, 1079–1080, 1315 |
| 15 / MOVE_HYPERBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 106 | 227, 737, 746, 751, 833, 838–839, 869–918, 950, 969, 991, 1072, 1101, 1191–1192, 1202, 1207, 1231, 1260–1263, 1266–1269, 1271–1291, 1358, 1430–1438 |
| 16 / MOVE_LIGHTSCREEN | PROJECT_POLICY:LOCAL_POSITIVE | 10 | 1–3, 220–221, 512–513, 526, 593, 965 |
| 16 / MOVE_LIGHTSCREEN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 848, 1079–1080, 1088–1092 |
| 16 / MOVE_LIGHTSCREEN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 36 | 746, 869, 875–876, 882–884, 886, 893–894, 897–898, 904, 906–908, 915–918, 991, 1072, 1101, 1207, 1260, 1264, 1266, 1276–1278, 1282, 1287–1289, 1291, 1430 |
| 17 / MOVE_PROTECT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 837, 1079–1080, 1088–1092 |
| 17 / MOVE_PROTECT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 115 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1439 |
| 18 / MOVE_RAINDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 713–717, 1088–1092 |
| 18 / MOVE_RAINDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 92 | 84–85, 298–300, 593–595, 691, 746, 816–817, 833, 839, 872, 874–884, 886–889, 892–908, 910–918, 1001, 1009, 1047, 1072, 1101, 1191–1192, 1202, 1207, 1262–1272, 1276–1277, 1279, 1282, 1284–1285, 1293, 1358, 1426–1429, 1431, 1436–1438 |
| 19 / MOVE_GIGADRAIN | PROJECT_POLICY:LOCAL_POSITIVE | 13 | 15, 46–47, 165–166, 292, 294, 380, 466–467, 508, 564–565 |
| 19 / MOVE_GIGADRAIN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 709–710 |
| 19 / MOVE_GIGADRAIN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 751, 869, 873, 877, 890, 894, 915, 1072, 1260, 1263, 1267, 1272, 1274, 1278, 1281–1282, 1287, 1289, 1426–1429, 1431 |
| 20 / MOVE_SAFEGUARD | PROJECT_POLICY:LOCAL_POSITIVE | 240 | 1–3, 26–28, 35–40, 45, 58–59, 72–73, 79–80, 86–87, 96–97, 113, 123, 131, 146–154, 173–174, 179–182, 191–192, 194–195, 199, 212, 242, 249–250, 277–279, 306–307, 325, 329, 346–347, 358–359, 369, 392–394, 401–405, 407–411, 440–442, 486, 489–490, 493, 509–510, 512–513, 528, 531, 533–537, 539–543, 545–546, 548–550, 593–595, 599–602, 625–632, 638–639, 647, 660–662, 675–676, 689–693, 696–697, 699–701, 718–735, 752–753, 757, 761–763, 774, 777–779, 785–786, 808, 811, 815–817, 820–821, 827–829, 832, 834, 848, 868, 919–920, 932, 939–941, 958–960, 964–965, 969–971, 978–982, 995–996, 999–1001, 1008–1009, 1022–1026, 1040–1045, 1065, 1108–1110, 1134, 1148–1150, 1165–1166, 1181, 1190, 1203, 1210–1211, 1215–1216, 1223–1224, 1242, 1249–1250, 1252 |
| 20 / MOVE_SAFEGUARD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 48 | 837, 1234–1235, 1310–1320, 1328–1330, 1341–1342, 1344–1345, 1347–1354, 1356–1357, 1371–1372, 1376, 1382, 1385, 1391, 1404, 1408, 1412, 1414–1418, 1420–1422 |
| 20 / MOVE_SAFEGUARD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 33 | 746, 751, 838, 869, 875–876, 878, 882–884, 886, 890, 893, 901, 904, 907–910, 915–918, 991, 1072, 1260, 1263, 1269, 1276, 1278, 1282, 1287, 1289 |
| 21 / MOVE_FRUSTRATION | PROJECT_POLICY:LOCAL_POSITIVE | 845 | 1–9, 12, 23–45, 48–128, 130–131, 133–164, 167–200, 203–234, 236–251, 277–289, 295–303, 306–307, 309–314, 318–359, 361–372, 376–384, 386–397, 399–411, 440–451, 455–464, 469–483, 486–493, 495–507, 509–556, 559–563, 570–602, 604–654, 656–702, 718–735, 747–750, 752–771, 774–783, 785–830, 832, 834, 848, 868, 919–920, 932, 939–987, 989–990, 992–1005, 1008–1019, 1022–1035, 1037, 1039–1046, 1048–1065, 1074–1078, 1082, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 21 / MOVE_FRUSTRATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 258 | 713–717, 837, 1073, 1079–1080, 1083–1084, 1088–1092, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 21 / MOVE_FRUSTRATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 73 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 22 / MOVE_SOLARBEAM | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 332, 1026 |
| 22 / MOVE_SOLARBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 131, 709–710, 1079–1080 |
| 22 / MOVE_SOLARBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 54 | 282, 737, 751, 869–871, 873, 878, 882–883, 888, 890–891, 895–896, 900–901, 907–909, 911–912, 915, 917, 991, 1207, 1220, 1229–1231, 1260–1261, 1263, 1271–1274, 1278, 1280–1282, 1286, 1289, 1291, 1426–1431, 1433, 1436–1438 |
| 23 / MOVE_IRONTAIL | PROJECT_POLICY:LOCAL_POSITIVE | 297 | 4–9, 19–20, 23–28, 35–38, 52–59, 79–80, 86–87, 111–113, 125–126, 128, 130–131, 133–137, 147–154, 158–162, 172–173, 179–181, 183–184, 190, 194–197, 199, 203, 206–207, 210, 215, 228–229, 231–234, 240, 242–249, 277–279, 283–287, 307, 315–317, 321, 328–329, 334, 350–354, 359, 379–380, 397, 405–406, 440–445, 452–453, 456–458, 461–464, 470–472, 477, 484–485, 487–488, 496–498, 500–503, 512–514, 517, 519–520, 523–525, 527, 533–536, 540, 546, 548–558, 564–569, 604–606, 612–613, 625–626, 656–657, 663–665, 688, 694–695, 698, 718, 720–735, 754–756, 758–763, 775–776, 780–781, 784–786, 798–801, 808, 810, 812–814, 822–823, 832, 834, 919, 945–947, 951–952, 961–962, 974–975, 983, 996, 999–1001, 1008, 1020–1026, 1029–1030, 1037, 1046, 1082, 1087, 1093–1099, 1111–1112, 1126, 1155, 1180–1181, 1185, 1209, 1212, 1215–1216, 1224, 1241, 1247–1248, 1251, 1375, 1377–1379 |
| 23 / MOVE_IRONTAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 55 | 837, 1088–1092, 1234–1235, 1240, 1256, 1258–1259, 1297–1299, 1304–1305, 1310–1312, 1316–1317, 1335–1336, 1338, 1356–1357, 1361–1362, 1365–1366, 1368–1372, 1376, 1381, 1385, 1387, 1390, 1392, 1394–1395, 1400, 1403, 1405–1407, 1409–1412, 1419, 1421 |
| 23 / MOVE_IRONTAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 37 | 838, 870–872, 875–876, 878, 880–885, 888–890, 892, 896, 898, 901, 903, 905, 909, 911–915, 917, 1047, 1261–1262, 1264–1265, 1269–1270, 1279 |
| 24 / MOVE_THUNDERBOLT | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 386, 544 |
| 24 / MOVE_THUNDERBOLT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 12 | 713–717, 1020–1021, 1088–1092 |
| 24 / MOVE_THUNDERBOLT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 39 | 746, 877–878, 880, 882–884, 889, 893, 896, 898, 902–903, 907–912, 916–917, 1072, 1101, 1204, 1264–1265, 1267, 1269, 1271–1273, 1284–1285, 1291, 1430, 1433, 1436–1438 |
| 25 / MOVE_THUNDER | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 56 |
| 25 / MOVE_THUNDER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 12 | 713–717, 1020–1021, 1088–1092 |
| 25 / MOVE_THUNDER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 39 | 161, 648, 746, 877–878, 880, 882–884, 889, 896, 898, 902–903, 907–912, 917, 954, 1072, 1101, 1204, 1264–1265, 1267, 1269, 1271, 1273, 1284–1285, 1291, 1430, 1433, 1436–1438 |
| 26 / MOVE_EARTHQUAKE | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 204, 236, 362, 951 |
| 26 / MOVE_EARTHQUAKE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 26 / MOVE_EARTHQUAKE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 63 | 103, 131, 218, 709, 737, 838, 869–872, 876, 878–883, 885, 887, 889–892, 896, 899–901, 904–911, 913–916, 991, 1047, 1231, 1260–1262, 1266, 1269, 1271, 1273–1274, 1279–1280, 1282–1283, 1290, 1430–1434, 1436–1438 |
| 27 / MOVE_RETURN | PROJECT_POLICY:LOCAL_POSITIVE | 845 | 1–9, 12, 23–45, 48–128, 130–131, 133–164, 167–200, 203–234, 236–251, 277–289, 295–303, 306–307, 309–314, 318–359, 361–372, 376–384, 386–397, 399–411, 440–451, 455–464, 469–483, 486–493, 495–507, 509–556, 559–563, 570–602, 604–654, 656–702, 718–735, 747–750, 752–771, 774–783, 785–830, 832, 834, 848, 868, 919–920, 932, 939–987, 989–990, 992–1005, 1008–1019, 1022–1035, 1037, 1039–1046, 1048–1065, 1074–1078, 1082, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 27 / MOVE_RETURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 258 | 713–717, 837, 1073, 1079–1080, 1083–1084, 1088–1092, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 27 / MOVE_RETURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 73 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 28 / MOVE_DIG | PROJECT_POLICY:LOCAL_POSITIVE | 31 | 19–20, 46–47, 165–166, 207, 243, 245, 308, 315–317, 446–448, 452–453, 484–485, 525, 557–558, 564–569, 709, 784 |
| 28 / MOVE_DIG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 466, 710, 837, 1020–1021, 1088–1092 |
| 28 / MOVE_DIG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 44 | 143, 499, 551–553, 737, 838–839, 870–872, 876, 878–879, 884–885, 887, 889–892, 894, 896, 900, 909, 912–914, 917, 1231, 1261–1262, 1264–1266, 1268, 1270–1271, 1279–1280, 1283, 1290, 1292–1293 |
| 29 / MOVE_PSYCHIC | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 143, 499 |
| 29 / MOVE_PSYCHIC | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 1079–1080, 1255 |
| 29 / MOVE_PSYCHIC | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 32 | 737, 746, 875–877, 882–883, 893–894, 897, 902, 906–908, 914, 916–918, 991, 1072, 1101, 1231, 1263, 1267, 1269, 1271–1272, 1278, 1287, 1289, 1434–1435 |
| 30 / MOVE_SHADOWBALL | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 512–513 |
| 30 / MOVE_SHADOWBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 102–103, 713–717, 1037 |
| 30 / MOVE_SHADOWBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 37 | 746, 785, 833, 875–878, 882–883, 888, 893–895, 897, 902–904, 906–908, 912, 914–917, 1072, 1207, 1263, 1265, 1267, 1270–1271, 1275–1276, 1278, 1287, 1439 |
| 31 / MOVE_BRICKBREAK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 837, 1079–1080, 1088–1092 |
| 31 / MOVE_BRICKBREAK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 61 | 697, 737, 746, 833, 838–839, 870–873, 876–879, 882–884, 886–887, 889–892, 894–897, 905–906, 909–911, 913–916, 1204, 1231, 1261–1262, 1264, 1266–1268, 1271, 1273–1274, 1284–1285, 1288, 1290–1293, 1426–1430, 1434–1435 |
| 32 / MOVE_DOUBLETEAM | PROJECT_POLICY:LOCAL_POSITIVE | 843 | 1–9, 12, 23–45, 48–128, 130–131, 133–164, 167–200, 203–234, 236–251, 277–289, 295–303, 306–307, 309–314, 318–359, 361–372, 376–384, 386–397, 399–411, 440–451, 455–464, 469–483, 486–493, 495–507, 509–556, 559–563, 570–602, 604–654, 656–702, 718–735, 747–750, 752–771, 774–783, 785–830, 832, 834, 848, 868, 919–920, 932, 939–990, 992–1003, 1005, 1008–1019, 1022–1035, 1037, 1039–1046, 1048–1065, 1075, 1077–1078, 1082, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 32 / MOVE_DOUBLETEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 258 | 713–717, 837, 1004, 1073, 1079–1080, 1083–1084, 1088–1092, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1295, 1297–1357, 1359–1372, 1376, 1381–1422 |
| 32 / MOVE_DOUBLETEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 73 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 33 / MOVE_REFLECT | PROJECT_POLICY:LOCAL_POSITIVE | 10 | 209–210, 215, 220–221, 244–245, 514, 672–673 |
| 33 / MOVE_REFLECT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 16 | 386–387, 713–717, 1079–1080, 1087–1092, 1100 |
| 33 / MOVE_REFLECT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 36 | 131, 464, 519, 675–676, 833, 875, 882–884, 893–894, 897, 906–908, 916–918, 991, 1010, 1101, 1202, 1207, 1264, 1269, 1276–1278, 1280, 1282, 1287–1288, 1291, 1430–1431 |
| 34 / MOVE_SHOCKWAVE | PROJECT_POLICY:LOCAL_POSITIVE | 312 | 19–20, 25–26, 29–36, 39–40, 52–53, 63–65, 81–82, 88–89, 100–101, 108–115, 122, 125, 128, 131, 135, 137, 143, 145, 147–151, 161–162, 170–176, 179–181, 190, 200, 203, 206, 209–211, 233–234, 239, 241–243, 248–251, 288–289, 308–310, 315–317, 320, 322, 337–338, 351–354, 364–368, 370–372, 376–378, 380, 382–387, 392–394, 401–411, 452–453, 456–458, 461–464, 470, 477–482, 484–486, 492–493, 495, 499, 515–519, 521, 527–529, 531–537, 539–540, 544, 546–547, 557–561, 570–571, 575–576, 580–581, 614–616, 625–632, 640, 645–646, 648–649, 652–654, 656–665, 671, 674–676, 686–688, 695, 697, 701–702, 718, 720–735, 747–750, 755, 762–763, 785–789, 798–799, 802–803, 810, 812–814, 826, 828–829, 832, 834, 919–920, 951–955, 983, 993–994, 997, 1001–1002, 1008–1009, 1012–1014, 1016–1018, 1020–1022, 1029–1030, 1032–1035, 1040–1042, 1075, 1078, 1087, 1093–1099, 1158, 1219–1220, 1247–1248, 1251, 1377–1379 |
| 34 / MOVE_SHOCKWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 65 | 713–717, 837, 1073, 1079–1080, 1088–1092, 1117–1118, 1123–1124, 1127–1128, 1140–1141, 1148–1156, 1159, 1163, 1168, 1172–1173, 1179, 1186, 1193, 1203, 1212, 1222, 1225–1227, 1232–1233, 1236–1237, 1239, 1257, 1310–1312, 1331–1334, 1382, 1384, 1386, 1389, 1392, 1404, 1406 |
| 34 / MOVE_SHOCKWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 875, 878, 882–884, 889, 893–894, 896, 898, 902–903, 907–912, 916, 1264–1265, 1269, 1271 |
| 35 / MOVE_FLAMETHROWER | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 493 |
| 35 / MOVE_FLAMETHROWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 35 | 737, 870–871, 876, 878, 880–883, 888–889, 891, 895–896, 898, 900–901, 903, 905, 909, 911, 913, 917, 1207, 1231, 1261, 1266, 1271, 1275, 1280, 1286, 1432, 1436–1438 |
| 36 / MOVE_SLUDGEBOMB | PROJECT_POLICY:LOCAL_POSITIVE | 7 | 191, 582–583, 758–760, 800 |
| 36 / MOVE_SLUDGEBOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 19–20 |
| 36 / MOVE_SLUDGEBOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 13 | 869, 873, 877, 888, 895, 906, 1207, 1260, 1267, 1272, 1284–1285, 1439 |
| 37 / MOVE_SANDSTORM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 837 |
| 37 / MOVE_SANDSTORM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 39 | 675–676, 683, 709, 838, 870–871, 878, 880–883, 885–886, 889, 895–896, 900, 903, 906–909, 911, 913, 918, 991, 1017, 1261, 1271, 1279–1280, 1283, 1290, 1426–1429, 1434 |
| 38 / MOVE_FIREBLAST | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 493 |
| 38 / MOVE_FIREBLAST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 31 | 737, 870–871, 876, 878, 880–883, 888–889, 891, 895–896, 900–901, 903, 905, 909, 911, 913, 917, 1207, 1231, 1261, 1266, 1271, 1275, 1280, 1286, 1432 |
| 39 / MOVE_ROCKTOMB | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 7–8, 362 |
| 39 / MOVE_ROCKTOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 39 / MOVE_ROCKTOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 55 | 709, 737, 839, 870–872, 878–879, 881–883, 885, 887, 889–892, 894–897, 899–900, 903, 905–906, 909–911, 913–916, 918, 991, 1231, 1261–1262, 1266, 1268, 1271, 1273, 1279–1280, 1283, 1290–1293, 1426–1430, 1434 |
| 40 / MOVE_AERIALACE | PROJECT_POLICY:LOCAL_POSITIVE | 170 | 4–5, 12, 29–31, 41–42, 49–51, 54–58, 80, 83, 104–105, 115, 122, 137, 140–142, 150, 169, 176–178, 200, 226, 233, 251, 301–303, 326–327, 376, 382–384, 390–391, 395–396, 403, 409, 443–444, 482, 496, 504–505, 511, 518, 521, 527, 536, 539–540, 544, 546, 559–563, 572–574, 580–581, 595, 609–611, 614, 619–620, 623, 640–642, 651, 674, 679, 682, 684–685, 690, 694, 702, 718, 720–735, 747–750, 754, 774, 782–783, 787–789, 796–797, 804–805, 810, 825, 834, 868, 919, 932, 959–960, 971, 976–977, 983, 985, 989–990, 996, 998–999, 1002, 1015, 1027–1028, 1039, 1048–1064, 1075, 1078, 1375 |
| 40 / MOVE_AERIALACE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 545, 719, 1079–1080, 1118–1120, 1128, 1158, 1172, 1220, 1244, 1413 |
| 40 / MOVE_AERIALACE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 45 | 333, 699, 752–753, 833, 839, 870–871, 873–874, 876, 878, 881–883, 886–887, 889–891, 894, 896–897, 901, 903, 905–909, 911, 913–914, 916, 944, 1191–1192, 1261, 1263, 1265, 1277, 1281, 1292–1293, 1434 |
| 41 / MOVE_TORMENT | PROJECT_POLICY:LOCAL_POSITIVE | 181 | 23–24, 31, 34, 41–42, 52–53, 63–65, 85, 88–89, 91–97, 100–101, 109–110, 122, 124, 130, 142, 150–151, 169, 185, 197–198, 200, 207–210, 215–217, 227–229, 246–248, 286–287, 299–300, 320, 322, 330–331, 347, 351–352, 355, 361–362, 371–372, 376–378, 392–394, 410–411, 443–445, 463–464, 472, 482–483, 486–488, 492, 495, 504–507, 514, 519–520, 525, 528–531, 535, 538, 544, 548–550, 562–563, 570–571, 580–581, 604–606, 608, 612–613, 619–620, 623–624, 627–629, 674, 677–678, 682–683, 686–688, 694–695, 754–755, 767–768, 782–783, 785–786, 790–791, 794–797, 809, 815, 822–823, 825, 828–829, 832, 942–944, 951–952, 974–975, 996, 1002–1005, 1012, 1029–1030, 1034–1035, 1040–1042, 1077, 1158, 1219–1220, 1253, 1380 |
| 41 / MOVE_TORMENT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 63 | 1108–1110, 1113–1115, 1119–1120, 1138–1139, 1141, 1148–1155, 1169, 1184–1185, 1188, 1193, 1209–1210, 1212, 1226–1227, 1230, 1236–1237, 1239, 1244–1245, 1257, 1294–1296, 1309, 1321–1324, 1330, 1335–1338, 1355, 1384, 1390, 1392, 1399–1404, 1413, 1419–1421 |
| 41 / MOVE_TORMENT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 20 | 737, 875, 877, 880–883, 885, 888–889, 893–895, 899, 902–904, 916, 1265, 1267 |
| 42 / MOVE_FACADE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 837, 1079–1080, 1088–1092 |
| 42 / MOVE_FACADE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 120 | 737, 746, 751, 833, 838–839, 869–918, 948–950, 972–973, 991, 1047, 1072, 1083, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1438 |
| 43 / MOVE_SECRETPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 762 | 1–9, 12, 15–128, 130–131, 133–200, 203–234, 236–251, 277–289, 292, 294–359, 361–397, 399–411, 440–453, 455–464, 466–467, 469–602, 604–654, 656–702, 709–710, 718–735, 747–750, 752–771, 774–830, 832, 834, 848, 868, 919–920, 932, 1022, 1037, 1039–1042, 1158, 1219–1220, 1238, 1241–1242, 1246–1249, 1251–1253, 1375, 1377–1380 |
| 43 / MOVE_SECRETPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 386 | 713–717, 837, 939–987, 989–990, 992–1005, 1008–1021, 1023–1035, 1043–1046, 1048–1065, 1073–1080, 1082–1084, 1088–1099, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1250, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 43 / MOVE_SECRETPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 69 | 737, 746, 751, 833, 838, 869–918, 1101, 1260–1272 |
| 44 / MOVE_REST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 837, 1079–1080, 1088–1092 |
| 44 / MOVE_REST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 115 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1439 |
| 45 / MOVE_ATTRACT | PROJECT_POLICY:LOCAL_POSITIVE | 582 | 1–9, 23–28, 35–40, 43–45, 48–62, 69–76, 79–80, 84–94, 96–97, 102–103, 106–107, 109–113, 116–117, 123, 125–126, 128, 130–131, 133–136, 143, 147–149, 151–164, 167–168, 170–174, 179–200, 203–207, 209–212, 214–221, 225, 227–232, 234, 236–237, 239–240, 242, 246–248, 277–287, 295–300, 302, 306–307, 309–312, 320–329, 332–336, 339–340, 344–347, 350–354, 356–359, 361–362, 364–369, 377–380, 386–387, 392–397, 407–408, 411, 440–451, 455–458, 461–464, 469–472, 475–479, 482–483, 486–488, 491, 493, 495–503, 506–507, 509–510, 512–514, 517, 519–520, 522–526, 528–531, 538, 541, 548–556, 575–576, 582–583, 585–587, 593–595, 599–602, 604–606, 612–613, 623–634, 638–639, 643–644, 647–649, 656–657, 660–668, 672–673, 677–678, 680–683, 686–690, 694–695, 698, 754–756, 758–766, 769–771, 774–781, 785–786, 794–795, 798–801, 808–810, 812–817, 820–823, 832, 848, 868, 932, 939–962, 964–971, 974–975, 978–983, 986–987, 992, 995–996, 998–1001, 1022–1035, 1037, 1043–1046, 1065, 1082, 1093–1099, 1102–1115, 1125–1126, 1129–1141, 1148–1153, 1155, 1160, 1163–1171, 1176–1179, 1183–1184, 1193, 1203, 1208, 1212, 1215–1216, 1219, 1224, 1238, 1241–1242, 1246–1253, 1375, 1377–1380, 1414 |
| 45 / MOVE_ATTRACT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 307 | 10–11, 13–14, 81–82, 100–101, 120–121, 129, 132, 137, 144–146, 150, 201–202, 233, 235, 243–245, 249–251, 290–291, 293, 301, 303, 318–319, 348–349, 360, 398–406, 409–410, 454, 465, 468, 489–490, 515, 527, 532–537, 539–540, 542–547, 652–655, 675–676, 691–693, 696–697, 699–702, 713–735, 747–750, 752–753, 757, 772–773, 811, 824–830, 834, 837, 919–920, 989–990, 1002–1019, 1040–1042, 1048–1064, 1073–1080, 1083–1084, 1088–1092, 1116, 1146–1147, 1162, 1172–1175, 1180–1182, 1185–1190, 1209–1211, 1221–1223, 1234–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1312, 1316–1357, 1359–1372, 1376, 1393–1395, 1409–1413, 1419–1422 |
| 45 / MOVE_ATTRACT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 90 | 737, 751, 833, 839, 869–881, 884–905, 907–908, 912–917, 991, 1047, 1072, 1191–1192, 1202, 1204, 1231, 1260–1272, 1274–1293, 1430–1431 |
| 46 / MOVE_THIEF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 455, 713–717, 1079–1080, 1087–1092 |
| 46 / MOVE_THIEF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 56 | 35–36, 158–160, 277–279, 281–282, 326–327, 585–587, 737, 839, 873–875, 877–879, 881, 886–888, 890–891, 893–894, 897–899, 901–903, 916, 944, 1072, 1191–1192, 1204, 1231, 1263–1268, 1272, 1274, 1277, 1284–1285, 1288 |
| 47 / MOVE_STEELWING | PROJECT_POLICY:LOCAL_POSITIVE | 77 | 6, 84–85, 123, 144–146, 149, 151, 163–164, 193, 198, 207, 212, 225, 227, 249–250, 309–310, 333–334, 358–359, 369, 397, 407–408, 448–451, 483, 522, 525, 540, 595, 633–634, 680–683, 688, 696–697, 699, 718, 752–753, 769–771, 809, 822–823, 939–941, 948–950, 958, 1043–1045, 1115, 1137, 1178–1179, 1221–1223, 1246, 1250, 1252 |
| 47 / MOVE_STEELWING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 23 | 1300–1302, 1320–1324, 1333–1334, 1349, 1355, 1367, 1378–1379, 1385, 1388, 1390–1391, 1394–1395, 1403, 1421 |
| 47 / MOVE_STEELWING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 13 | 870–871, 874, 881, 886, 901, 905, 907–908, 1191–1192, 1261, 1277 |
| 48 / MOVE_SKILLSWAP | PROJECT_POLICY:LOCAL_POSITIVE | 6 | 308, 317, 466–467, 709–710 |
| 48 / MOVE_SKILLSWAP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 848 |
| 48 / MOVE_SKILLSWAP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 35–36, 163–164, 746, 794–795, 875–877, 882–883, 893–894, 897, 902, 916–918, 1263, 1267, 1278, 1287 |
| 49 / MOVE_LEECHFANG | MAPPING_BLOCK:LOCAL_POSITIVE | 77 | 27–28, 41–42, 46–49, 71, 140–141, 151, 167–169, 292, 294, 301–303, 311–312, 361–362, 455, 505, 508, 522, 530, 648–649, 669–670, 689–690, 702, 747–750, 822–823, 942–944, 959–960, 968–971, 974–975, 984–985, 995, 1011, 1023–1024, 1075, 1117–1118, 1142–1143, 1151–1153, 1156, 1165, 1174, 1306–1309, 1346–1347, 1385 |
| 49 / MOVE_LEECHFANG | MAPPING_BLOCK:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 1216 | 1–26, 29–40, 43–45, 50–70, 72–139, 142–150, 152–166, 170–251, 277–291, 293, 295–300, 304–310, 313–360, 363–411, 440–454, 456–504, 506–507, 509–521, 523–529, 531–602, 604–647, 650–668, 671–688, 691–701, 709–710, 713–735, 737, 746, 751–821, 824–830, 832–834, 837–839, 848, 868–920, 932, 939–941, 945–958, 961–967, 972–973, 976–983, 986–994, 996–1010, 1012–1022, 1025–1035, 1037, 1039–1065, 1072–1074, 1076–1084, 1087–1116, 1119–1141, 1144–1150, 1154–1155, 1157–1160, 1162–1164, 1166–1173, 1175–1193, 1202–1217, 1219–1227, 1229–1242, 1244–1253, 1255–1305, 1310–1345, 1348–1372, 1375–1384, 1386–1422, 1426–1439 |
| 50 / MOVE_OVERHEAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 15 | 737, 870–871, 888, 891, 898, 900, 909, 911, 1231, 1261, 1275, 1280, 1286, 1432 |
| 51 / MOVE_ROOST | PROJECT_POLICY:LOCAL_POSITIVE | 107 | 6, 12, 41–42, 49, 83–85, 123, 142, 144–146, 149, 151, 163–164, 169, 176–178, 193, 198, 206–207, 212, 226–227, 249–250, 302, 309–310, 312, 333–334, 358–359, 369, 386–387, 397, 407–408, 449–451, 469, 483, 521–522, 525, 572–574, 580–581, 614, 619–620, 633–634, 640, 680–683, 688, 690, 696–697, 699, 752–753, 769–771, 774, 809, 822–823, 825, 868, 932, 939–941, 948–950, 955, 958–960, 997, 1002, 1009, 1011–1012, 1043–1045, 1246, 1250, 1252, 1378–1379 |
| 51 / MOVE_ROOST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 37 | 446–448, 509–511, 1113–1115, 1118, 1133, 1137, 1157, 1165, 1179, 1217, 1221–1223, 1300–1302, 1321–1324, 1333–1334, 1348–1349, 1355, 1367, 1385, 1390–1391, 1403, 1421 |
| 51 / MOVE_ROOST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 870–871, 873–874, 881, 886, 901, 905, 907–908, 1261, 1263 |
| 52 / MOVE_FOCUSBLAST | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 217, 1253 |
| 52 / MOVE_FOCUSBLAST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 837 |
| 52 / MOVE_FOCUSBLAST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 47 | 75, 239, 737, 746, 838, 870–872, 875–879, 882–884, 887, 889–893, 895–897, 909, 911–912, 914–916, 1032, 1101, 1231, 1261–1262, 1266–1267, 1271–1272, 1274–1275, 1288, 1292–1293, 1358, 1435 |
| 53 / MOVE_ENERGYBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 709–710, 1025–1026 |
| 53 / MOVE_ENERGYBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 33 | 486, 746, 751, 869, 875, 877, 882–883, 890, 893–894, 897, 907–908, 911, 915–916, 1260, 1263, 1267, 1274, 1278, 1281–1282, 1289, 1426–1429, 1431, 1436–1438 |
| 54 / MOVE_FALSESWIPE | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 7–9, 358–359 |
| 54 / MOVE_FALSESWIPE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 32 | 27–28, 833, 839, 869–873, 879, 886–887, 890, 895, 901, 903, 913, 916, 1024, 1260–1262, 1265, 1268, 1274, 1279, 1292–1293, 1426–1429 |
| 55 / MOVE_BRINE | PROJECT_POLICY:LOCAL_POSITIVE | 84 | 7–9, 54–55, 72–73, 79–80, 86–87, 90–91, 116–117, 130–131, 134, 151, 170–171, 199, 211, 230, 245, 249, 309–310, 325, 328–329, 336, 373–375, 404, 446–448, 471–472, 475–476, 509–510, 537, 542–543, 546, 666–667, 720–735, 834, 920, 945–947, 964–965, 986–987, 1163, 1167, 1178–1179, 1208, 1215–1216, 1224 |
| 55 / MOVE_BRINE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 23 | 554–556, 568–569, 633–634, 647, 1239, 1241, 1255, 1257, 1301–1302, 1353–1354, 1356–1357, 1370–1372, 1388, 1407 |
| 55 / MOVE_BRINE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 872, 876, 880, 899, 910, 1047, 1202, 1262, 1268–1269, 1293 |
| 56 / MOVE_HONECLAWS | PROJECT_POLICY:LOCAL_POSITIVE | 185 | 4–6, 27–34, 46–47, 50–57, 98–99, 140–142, 149, 151, 158–162, 167–168, 190, 207, 215–217, 248, 279–282, 288–289, 296–297, 301–303, 317, 322, 326–327, 334, 359, 364–366, 376, 380, 382–384, 390–391, 395–397, 399–400, 403, 405–408, 443–445, 447–448, 455, 469, 477, 484–485, 487–488, 496–498, 501, 504–505, 514, 525, 536–537, 540, 546, 562–569, 582–583, 595, 604–606, 610–611, 619–620, 623–624, 650–651, 657, 663–667, 674, 677–678, 680–681, 684–685, 691, 696–697, 699, 701–702, 718, 720–735, 747–750, 752–753, 759–760, 771, 783, 796–797, 804–805, 809, 817, 823, 825, 834, 919–920, 1246, 1253, 1375, 1380 |
| 56 / MOVE_HONECLAWS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 88 | 800–801, 942–944, 951–952, 970–971, 974–975, 985, 989–990, 992, 995, 1008, 1017, 1023–1024, 1027–1030, 1048–1064, 1078–1080, 1113–1115, 1119–1120, 1127–1128, 1133, 1151–1155, 1176, 1179, 1185, 1209, 1212, 1226–1227, 1240, 1244–1245, 1256, 1296, 1316–1317, 1330, 1335–1336, 1343, 1355, 1361, 1365–1366, 1392–1395, 1403, 1405–1407, 1413 |
| 56 / MOVE_HONECLAWS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 746, 870–871, 881, 889–891, 894, 896, 901, 903, 905–909, 911, 913–914, 1261, 1265, 1268 |
| 57 / MOVE_CHARGEBEAM | PROJECT_POLICY:LOCAL_POSITIVE | 77 | 39–40, 63–65, 113, 122, 135, 145, 150, 172, 206, 223–224, 242, 251, 288–289, 318–319, 337–338, 348–349, 355, 376, 478–481, 492, 540, 547, 570–571, 580–581, 584, 614, 627–629, 640, 652–654, 658–659, 674, 688, 701–702, 718, 747–750, 790–791, 802–803, 806–807, 818–819, 828–829, 973, 993–995, 1003, 1010, 1013, 1158, 1378–1379 |
| 57 / MOVE_CHARGEBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 45 | 713–717, 1079–1080, 1088–1092, 1111–1112, 1117–1118, 1123–1124, 1127–1128, 1140, 1147–1154, 1156, 1168, 1172–1173, 1176, 1178–1179, 1189–1190, 1203, 1211, 1214, 1222, 1225–1227 |
| 57 / MOVE_CHARGEBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 746, 875, 882–884, 893, 895, 898, 902–903, 907–908, 912, 916–917, 991, 1072, 1204, 1220, 1264, 1284–1285, 1433 |
| 58 / MOVE_ENDURE | PROJECT_POLICY:LOCAL_POSITIVE | 34 | 15–22, 46–47, 165–166, 292, 294, 304–305, 308, 315–317, 373–375, 385, 452–453, 466–467, 484–485, 494, 508, 709–710 |
| 58 / MOVE_ENDURE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 25 | 557–558, 564–569, 713–717, 784, 837, 1020–1021, 1079–1080, 1087–1092 |
| 58 / MOVE_ENDURE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 116 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1164, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1439 |
| 59 / MOVE_DRAGONPULSE | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 7–8, 160 |
| 59 / MOVE_DRAGONPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 59 / MOVE_DRAGONPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 33 | 838, 870–872, 880–881, 884–885, 889–890, 896, 901, 905, 907–909, 911, 913–914, 1207, 1261–1262, 1269, 1281–1282, 1291, 1430–1433, 1436–1438 |
| 60 / MOVE_DRAINPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 7 | 44–45, 165–166, 308, 317, 493 |
| 60 / MOVE_DRAINPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 68, 1413 |
| 60 / MOVE_DRAINPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 27 | 552–553, 746, 875–878, 882–883, 890, 894, 897, 912, 914, 916–917, 1072, 1267, 1272, 1274, 1284–1285, 1288–1289, 1292–1293, 1358 |
| 61 / MOVE_WILLOWISP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 713–717, 1142 |
| 61 / MOVE_WILLOWISP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 25 | 300, 737, 769, 870–871, 877, 882–883, 888, 891, 893–894, 900–903, 909, 916, 1072, 1231, 1261, 1267, 1275, 1280, 1286 |
| 62 / MOVE_SILVERWIND | PROJECT_POLICY:LOCAL_POSITIVE | 59 | 12, 15, 49, 123, 151, 163–166, 176–178, 187–189, 193, 212, 251, 292, 294, 300, 302, 312, 333–334, 369, 386–387, 455, 467, 469, 478–479, 495, 509–510, 521–522, 540, 546, 718, 720–735, 834, 1252 |
| 62 / MOVE_SILVERWIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 55 | 301, 303, 466, 593–598, 641, 643–644, 648–649, 670–671, 690, 702, 709–710, 747–750, 772–774, 826, 837, 868, 932, 955, 959–960, 972–973, 981, 1012, 1014, 1075, 1118, 1122, 1165, 1306–1309, 1346–1349, 1383, 1385, 1391, 1421 |
| 62 / MOVE_SILVERWIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 873, 886, 1263 |
| 63 / MOVE_VENOSHOCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 16 | 212, 214, 869, 873, 877, 886–887, 1207, 1260, 1263, 1267, 1272, 1284–1286, 1439 |
| 64 / MOVE_EXPLOSION | PROJECT_POLICY:LOCAL_POSITIVE | 112 | 74–76, 81–82, 88–95, 100–103, 109–110, 151, 185, 204–205, 208, 211, 219, 222, 298–300, 318–321, 340, 347–349, 367–368, 399–403, 478–479, 487–488, 490–491, 515–516, 529, 535, 538, 577–579, 621–622, 630–632, 635–637, 650–651, 668, 698, 702, 747–750, 756, 811, 818–819, 827, 830, 990, 993, 1014, 1018, 1031–1035, 1037, 1048–1065, 1077, 1219 |
| 64 / MOVE_EXPLOSION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 29 | 1073, 1084, 1129–1131, 1146–1147, 1156, 1166, 1176, 1186–1187, 1225, 1236–1237, 1239, 1257, 1325–1327, 1359–1360, 1363–1364, 1386, 1415–1418 |
| 64 / MOVE_EXPLOSION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 877, 885, 900, 904, 906, 918, 991, 1267, 1272 |
| 65 / MOVE_SHADOWCLAW | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 65 / MOVE_SHADOWCLAW | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 31 | 400, 746, 833, 870–871, 877–878, 887, 889, 891, 894, 896, 902–903, 905–909, 911, 913–914, 916, 1020–1021, 1072, 1261, 1265, 1267, 1287–1288 |
| 66 / MOVE_PAYBACK | PROJECT_POLICY:LOCAL_POSITIVE | 232 | 23–24, 37–38, 52–53, 56–57, 62, 72–73, 85, 88–94, 109–112, 128, 130, 151, 186, 190, 197–198, 200, 204–205, 207, 209–211, 215–217, 227–229, 246–248, 286–287, 298–300, 310, 322, 326–327, 336, 344–345, 347, 351–352, 361–362, 377–380, 461–462, 472, 477–479, 482–483, 487–490, 500–501, 506–507, 509–510, 514, 517, 525, 530–531, 535, 538–540, 544, 546, 585–587, 593–595, 604–606, 612–613, 623–624, 627–629, 643–644, 660–665, 672–673, 677–678, 682–683, 688, 694–699, 701, 718, 720–735, 752–756, 758–760, 775–776, 780–781, 785–786, 794–795, 809, 832, 834, 951–952, 956–957, 964–967, 970–971, 974–975, 979–980, 982–983, 992, 995–996, 999–1001, 1025–1026, 1029–1030, 1034–1035, 1046, 1111–1115, 1125–1126, 1134, 1141, 1146–1147, 1155, 1162–1163, 1169, 1171, 1181–1182, 1184–1185, 1188–1189, 1193, 1209–1212, 1219, 1222–1223, 1253, 1375, 1380 |
| 66 / MOVE_PAYBACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 49 | 837, 1239–1240, 1244–1245, 1256–1259, 1295–1296, 1309, 1311–1312, 1328–1330, 1335–1336, 1339–1340, 1355, 1365–1367, 1383–1384, 1389–1390, 1392, 1399–1403, 1405, 1409–1411, 1413–1422 |
| 66 / MOVE_PAYBACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 36 | 495, 737, 746, 838, 873, 877, 880–881, 885, 888–889, 894–896, 899, 902–904, 912, 914, 1072, 1204, 1207, 1231, 1265–1267, 1272, 1277–1279, 1282, 1284–1285, 1290, 1292 |
| 67 / MOVE_RECYCLE | PROJECT_POLICY:LOCAL_POSITIVE | 131 | 35–36, 39–40, 63–65, 79–82, 96–97, 113, 120–122, 124, 137, 143, 150–151, 163–164, 173–174, 199, 203, 225, 233, 238, 242, 308, 317–319, 348–349, 351–352, 356–357, 392–394, 409–411, 478–479, 486, 489–490, 492–493, 499, 515, 527–528, 533–535, 541, 546, 564–569, 621–622, 627–629, 652–654, 658–659, 684, 701–702, 720–735, 747–750, 762–763, 767–768, 785–786, 810, 815, 828–829, 832, 834, 972–973, 986–988, 1017, 1022, 1035, 1040–1042, 1076–1077, 1158, 1220, 1377 |
| 67 / MOVE_RECYCLE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 38 | 1079–1080, 1111–1112, 1121–1122, 1132–1134, 1148–1150, 1160, 1168–1169, 1190, 1203, 1210–1211, 1215–1216, 1224, 1303–1305, 1329, 1347–1349, 1370, 1382, 1386, 1388–1389, 1404, 1408, 1414, 1420 |
| 67 / MOVE_RECYCLE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 8 | 875–876, 882–883, 893, 897, 916, 1271 |
| 68 / MOVE_GIGAIMPACT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 111, 837, 1079–1080, 1315 |
| 68 / MOVE_GIGAIMPACT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 118 | 82, 106–107, 227, 237, 333, 399, 737, 746, 751, 833, 838–839, 869–918, 950, 969, 991, 1072, 1101, 1191–1192, 1202, 1207, 1231, 1260–1263, 1266–1269, 1271–1293, 1358, 1426–1438 |
| 69 / MOVE_ROCKPOLISH | PROJECT_POLICY:LOCAL_POSITIVE | 110 | 74–76, 95, 111–112, 138–142, 151, 185, 205, 207–208, 213, 219, 222, 232, 246–248, 318–320, 340, 348–349, 381–384, 388–391, 399–403, 405, 442, 461–464, 489–491, 517, 525, 529, 539, 577–579, 610–611, 617–620, 622, 650–654, 675–678, 691–692, 698, 702, 747–750, 756, 796–797, 804–807, 811, 820–821, 827, 961–962, 986–987, 1001, 1017, 1031–1035, 1046, 1065, 1076, 1082, 1249, 1380 |
| 69 / MOVE_ROCKPOLISH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 22 | 1079–1080, 1126, 1129–1131, 1136, 1166, 1176, 1234–1235, 1252, 1325–1327, 1343, 1362–1364, 1381, 1387, 1392 |
| 69 / MOVE_ROCKPOLISH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 685, 881, 885, 889, 896, 900, 906, 909, 918, 991, 1272 |
| 70 / MOVE_FLASH | PROJECT_POLICY:LOCAL_POSITIVE | 341 | 1–3, 12, 15, 25–26, 35–36, 39–40, 43–49, 52–55, 63–65, 69–71, 79–82, 96–97, 100–103, 109–110, 113–114, 120–122, 124–125, 135, 137, 145, 150–154, 163–168, 170–182, 187–189, 191–197, 199–200, 203, 213, 227, 233–234, 238–239, 242–244, 249–251, 277–279, 292, 294–303, 306–308, 311–312, 315–319, 322, 337–338, 344–349, 351–354, 356–357, 361–363, 369, 376–378, 385–389, 392–394, 399–400, 407–411, 440–442, 455–460, 466–467, 469–470, 473–474, 476, 478–479, 482, 484–486, 489–490, 492–493, 495, 504–505, 508–510, 512–513, 515, 518–519, 521–523, 527–528, 530–536, 541, 543–550, 558, 564–565, 570–571, 575–576, 580–581, 584, 593–595, 599–602, 614–616, 627–632, 638–640, 643–646, 648–651, 656–662, 671, 675–676, 693, 697, 701–702, 709–710, 719–735, 747–750, 758–760, 774, 777–779, 784–786, 790–795, 802–803, 806–808, 810–811, 818–821, 824, 827–829, 832, 834, 848, 868, 919, 932, 1022, 1037, 1040–1042, 1158, 1219–1220, 1242, 1249, 1251, 1377 |
| 70 / MOVE_FLASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 120 | 398, 713–717, 947, 954–955, 959–960, 968–973, 994, 996, 1009–1010, 1013, 1017–1018, 1025–1026, 1029–1030, 1065, 1073, 1078–1080, 1088–1099, 1117–1118, 1127–1128, 1140–1141, 1148–1153, 1155, 1159–1160, 1163, 1165, 1168–1169, 1172–1173, 1181, 1186, 1190, 1193, 1203, 1210–1216, 1221–1222, 1224, 1232–1233, 1236–1237, 1246, 1297–1299, 1310–1312, 1316–1317, 1331–1334, 1341–1342, 1347–1349, 1363–1364, 1376, 1382–1384, 1386, 1389, 1391–1392, 1398, 1404, 1406, 1408, 1412, 1420–1421 |
| 70 / MOVE_FLASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 746, 751, 869, 873, 875–876, 882–884, 890, 893–894, 897–898, 902–904, 906–908, 915–918, 1101, 1260, 1263–1265 |
| 71 / MOVE_STONEEDGE | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 758, 956–957 |
| 71 / MOVE_STONEEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 71 / MOVE_STONEEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 47 | 27, 218, 220, 332–333, 400, 737, 746, 838, 879–883, 885, 887, 889, 891–892, 895–896, 900, 903, 905–906, 909, 911, 913–914, 916, 918, 991, 1231, 1266, 1279–1280, 1283, 1290–1293, 1430, 1432, 1434, 1436–1438 |
| 72 / MOVE_AVALANCHE | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 385, 410, 1040–1042 |
| 72 / MOVE_AVALANCHE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 86, 699, 752–753, 872, 876, 878, 880, 882–883, 889, 892, 896, 899, 904, 910–911, 915, 1202, 1231, 1262, 1269 |
| 73 / MOVE_THUNDERWAVE | PROJECT_POLICY:LOCAL_POSITIVE | 8 | 206, 249–250, 1008–1009, 1017, 1378–1379 |
| 73 / MOVE_THUNDERWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 713–717, 1020–1021, 1079–1080, 1088–1092 |
| 73 / MOVE_THUNDERWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 40 | 746, 875–877, 880, 882–884, 889, 893–894, 896, 898, 902–903, 907–912, 916–917, 1031–1033, 1072, 1101, 1204, 1264–1265, 1267, 1273, 1284–1285, 1287–1288, 1291, 1430, 1433 |
| 74 / MOVE_GYROBALL | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 758 |
| 74 / MOVE_GYROBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 74 / MOVE_GYROBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 710, 737, 833, 872, 885, 894, 904, 906, 911, 918, 991, 1231, 1262, 1273, 1280, 1282, 1291, 1430–1431, 1436–1438 |
| 75 / MOVE_SWORDSDANCE | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 191, 298, 306, 758–759 |
| 75 / MOVE_SWORDSDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 1079–1080, 1244 |
| 75 / MOVE_SWORDSDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 44 | 106–107, 613, 746, 751, 833, 839, 869–871, 873, 879, 886–887, 890–891, 895, 902–903, 909, 911, 913–916, 1072, 1260–1261, 1268, 1274–1276, 1279, 1287, 1291–1293, 1426–1430, 1434–1435 |
| 76 / MOVE_STEALTHROCK | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 317, 446–447, 452–453 |
| 76 / MOVE_STEALTHROCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 76 / MOVE_STEALTHROCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 218, 332–334, 697, 710, 879, 881, 885, 889, 892, 895–896, 900, 906, 909, 911, 913, 918, 991, 1279–1280, 1283, 1290–1291, 1430, 1436–1438 |
| 77 / MOVE_FLAMECHARGE | PROJECT_POLICY:LOCAL_POSITIVE | 35 | 77–78, 547, 607–608, 702, 747–750, 818–819, 989–990, 993, 1014, 1039, 1048–1064, 1077 |
| 77 / MOVE_FLAMECHARGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 1127–1128, 1142–1143, 1229–1230 |
| 77 / MOVE_FLAMECHARGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 10 | 737, 870–871, 888, 891, 900, 1261, 1275, 1280, 1432 |
| 78 / MOVE_LOWSWEEP | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 758 |
| 78 / MOVE_LOWSWEEP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 24 | 61, 186, 210, 746, 839, 882–883, 890–891, 894, 897, 912, 914, 916, 1266, 1274–1275, 1288, 1292–1293, 1426–1429 |
| 79 / MOVE_DARKPULSE | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 506, 765, 775 |
| 79 / MOVE_DARKPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 713–717, 1079–1080 |
| 79 / MOVE_DARKPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 32 | 839, 872, 877, 880, 882–883, 885, 888–889, 894–896, 899, 902–904, 914, 1072, 1204, 1262, 1265, 1267, 1272, 1276, 1287–1288, 1291–1292, 1430, 1436–1438 |
| 80 / MOVE_ROCKSLIDE | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 362, 672–673 |
| 80 / MOVE_ROCKSLIDE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 80 / MOVE_ROCKSLIDE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 53 | 737, 833, 838–839, 870–872, 878–879, 881–883, 885, 887, 889–892, 895–897, 900, 903, 905–906, 909–911, 913–916, 918, 991, 1101, 1231, 1261–1262, 1266, 1268, 1271, 1273, 1279–1280, 1283, 1290–1293, 1430, 1436–1438 |
| 81 / MOVE_XSCISSOR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 81 / MOVE_XSCISSOR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 873, 879, 886, 890, 894, 903, 916, 1072, 1268, 1286, 1434–1435 |
| 82 / MOVE_SLEEPTALK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 837, 1079–1080, 1088–1092 |
| 82 / MOVE_SLEEPTALK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 115 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1439 |
| 83 / MOVE_SCALD | PROJECT_POLICY:LOCAL_POSITIVE | 83 | 7–9, 54–55, 60–62, 72–73, 79, 116–117, 158–160, 183–184, 186, 194–195, 211, 283–285, 295–297, 309–312, 323–328, 350, 404, 446–448, 471–472, 475–476, 509–510, 554–556, 633–634, 700, 757, 764–766, 798, 800–801, 945–947, 956–957, 964–965, 968–969, 996, 1126, 1137–1139, 1178–1179, 1208, 1215–1216, 1224, 1241 |
| 83 / MOVE_SCALD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 1255, 1411–1412 |
| 83 / MOVE_SCALD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 17 | 839, 872, 876, 880, 892, 899, 910, 1047, 1191–1192, 1262, 1268, 1276, 1279–1280, 1286, 1293 |
| 84 / MOVE_POISONJAB | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 970, 1138 |
| 84 / MOVE_POISONJAB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 459 |
| 84 / MOVE_POISONJAB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 3, 107, 126, 240, 285, 520, 869, 873, 877, 882–883, 891–892, 894, 897, 899, 913–914, 916, 1207, 1260, 1266–1267, 1279, 1284–1285, 1292–1293, 1434 |
| 85 / MOVE_DREAMEATER | PROJECT_POLICY:LOCAL_POSITIVE | 206 | 12, 35–36, 38–40, 52–53, 63–65, 79–80, 92–94, 96–97, 102–103, 108, 113, 121–122, 124, 131, 137, 150–151, 163–164, 173–178, 190, 193, 196–200, 203, 206, 215, 228–229, 233–234, 238, 242, 249–251, 303, 318–319, 322, 348–349, 351–352, 356–359, 361–362, 367–368, 376–378, 392–394, 407–411, 477–479, 482–483, 486, 489–490, 492–493, 495, 514, 516, 521–522, 527–528, 530–535, 540–541, 544, 546, 562–563, 570–571, 580–581, 584, 593–595, 599–602, 614–616, 627–632, 645–646, 658–662, 701, 718, 720–735, 761–763, 774, 785–786, 790–793, 806–807, 816–819, 822–823, 825, 828–829, 832, 834, 868, 932, 959–960, 972–973, 982, 995–996, 1009, 1026, 1029–1030, 1037, 1039–1042, 1158, 1220, 1242, 1251, 1377–1379 |
| 85 / MOVE_DREAMEATER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 39 | 713–717, 1117–1118, 1146–1150, 1156, 1159–1160, 1168, 1179, 1189–1190, 1203, 1210–1211, 1221, 1225, 1232, 1329, 1347–1349, 1370, 1382, 1398, 1402, 1404, 1415–1418, 1420 |
| 85 / MOVE_DREAMEATER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 746, 875–877, 882–883, 888, 893–894, 897, 901–903, 907–908, 916–917, 1072, 1263, 1265, 1267, 1269 |
| 86 / MOVE_GRASSKNOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 709–710, 837, 1088–1092 |
| 86 / MOVE_GRASSKNOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 36 | 737, 746, 751, 838–839, 869, 875–876, 882–883, 890, 893, 895, 897, 906–908, 912, 915–917, 959–960, 1101, 1231, 1260, 1264, 1274, 1281–1282, 1358, 1426–1429, 1431 |
| 87 / MOVE_SWAGGER | PROJECT_POLICY:LOCAL_POSITIVE | 840 | 1–9, 12, 23–45, 48–128, 130–131, 133–164, 167–200, 203–234, 236–251, 277–289, 295–303, 306–307, 309–314, 318–359, 361–372, 376–384, 386–397, 399–411, 440–451, 455–464, 469–483, 486–493, 495–507, 509–556, 559–563, 570–602, 604–654, 656–702, 718–735, 747–750, 752–771, 774–783, 785–830, 832, 834, 848, 868, 919–920, 932, 939–990, 992–996, 998–1005, 1008–1015, 1017–1019, 1022–1035, 1037, 1039–1046, 1048–1065, 1077, 1082, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 87 / MOVE_SWAGGER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 259 | 713–717, 837, 1073, 1079–1080, 1083–1084, 1088–1092, 1102–1115, 1117–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 87 / MOVE_SWAGGER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 73 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 88 / MOVE_PLUCK | PROJECT_POLICY:LOCAL_POSITIVE | 56 | 16–22, 41–42, 83–85, 144–146, 151, 163–164, 169, 177–178, 198, 225, 227, 250, 304–305, 309–310, 359, 446–453, 483, 494, 521, 572–574, 580–581, 614, 619–620, 633–634, 680–683, 1246 |
| 88 / MOVE_PLUCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 54 | 769–771, 794–795, 939–941, 948–952, 958, 996, 1020–1021, 1043–1045, 1111–1115, 1125–1126, 1133, 1137, 1157, 1167, 1172–1173, 1217, 1221–1223, 1250, 1300–1302, 1321–1324, 1333–1334, 1348–1349, 1355, 1367, 1370, 1388, 1421 |
| 88 / MOVE_PLUCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 358, 874, 901 |
| 89 / MOVE_UTURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 737, 746, 839, 873–874, 886, 891, 911–912, 991, 1047, 1231, 1263, 1265, 1274–1278, 1281, 1292–1293, 1426–1429 |
| 90 / MOVE_SUBSTITUTE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 837, 1079–1080, 1088–1092 |
| 90 / MOVE_SUBSTITUTE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 115 | 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1358, 1426–1439 |
| 91 / MOVE_FLASHCANNON | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 820 |
| 91 / MOVE_FLASHCANNON | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 91 / MOVE_FLASHCANNON | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 710, 833, 872, 885–886, 895–896, 900, 906, 914, 918, 1023–1024, 1101, 1207, 1249, 1262, 1273, 1277, 1290–1291, 1430, 1435–1438 |
| 92 / MOVE_VOLTSWITCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 713–717, 1088–1092, 1100 |
| 92 / MOVE_VOLTSWITCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 8 | 884, 898, 1204, 1264, 1284–1285, 1433, 1435 |
| 93 / MOVE_DRAGONTAIL | PROJECT_POLICY:LOCAL_POSITIVE | 26 | 9, 31, 34, 95, 108, 112, 199, 208, 379, 384, 405, 516, 556, 620, 674, 802–807, 826, 993, 997, 1016, 1075 |
| 93 / MOVE_DRAGONTAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 837, 1172, 1174, 1379 |
| 93 / MOVE_DRAGONTAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 28 | 277–279, 333, 838, 870–872, 880, 884–885, 889–890, 896, 905, 909, 911, 913, 1207, 1261–1262, 1279, 1282, 1291, 1430–1433 |
| 94 / MOVE_INCINERATE | PROJECT_POLICY:LOCAL_POSITIVE | 193 | 4–6, 31, 34–40, 58–59, 66–68, 74–80, 88–89, 104–105, 108–113, 115, 126, 128, 130, 136, 142–143, 146–151, 155–157, 173–176, 199, 206, 209–210, 218–219, 223–224, 228–229, 240, 242, 244, 248, 250, 280–282, 286–287, 317, 321–322, 334, 339–340, 349, 355, 359, 364–366, 370–372, 376, 380, 384–385, 395–397, 405–406, 443–445, 461–464, 483, 487–488, 493, 496–499, 516–517, 520–521, 535–538, 544, 546–547, 551–553, 566–567, 584, 604–608, 612–613, 623–624, 660–665, 674, 682–684, 686–690, 694–696, 720–735, 754–755, 761–763, 770–771, 775–776, 814, 818–819, 830, 834, 919–920, 1039, 1219, 1238, 1378–1379 |
| 94 / MOVE_INCINERATE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 73 | 942–944, 974–975, 990, 993, 997, 1000–1001, 1008, 1014, 1016, 1031–1035, 1048–1064, 1075, 1077, 1105–1107, 1129–1131, 1142–1143, 1179, 1182, 1215–1216, 1223–1224, 1229–1230, 1234–1235, 1244–1245, 1248, 1297–1299, 1328–1330, 1345, 1382, 1390–1392, 1402–1403, 1405, 1410 |
| 94 / MOVE_INCINERATE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 737, 870–871, 876, 878, 880–883, 888–889, 891, 894–896, 900–901, 903, 905, 909, 911, 913, 917, 1261, 1266, 1271 |
| 95 / MOVE_STRUGGLEBUG | PROJECT_POLICY:LOCAL_POSITIVE | 36 | 12, 15, 46–47, 127, 165–166, 213, 292, 294, 301–303, 390–391, 466–467, 504–505, 596–598, 610–611, 641–642, 669–670, 685, 702, 709–710, 747–750 |
| 95 / MOVE_STRUGGLEBUG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 12 | 465, 968–969, 984–985, 1011–1012, 1116–1118, 1142–1143 |
| 95 / MOVE_STRUGGLEBUG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 193, 873, 879, 886–887, 1263 |
| 96 / MOVE_BULLDOZE | PROJECT_POLICY:LOCAL_POSITIVE | 8 | 9, 23, 243, 245, 249–250, 362, 530 |
| 96 / MOVE_BULLDOZE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 96 / MOVE_BULLDOZE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 59 | 218, 576, 709, 737, 838, 869–872, 876, 878–885, 887, 889–892, 896, 899–901, 904–911, 913–916, 918, 955, 991, 1047, 1231, 1260–1262, 1266, 1269, 1271, 1274, 1279–1280, 1282–1283, 1290, 1432, 1434–1435 |
| 97 / MOVE_FROSTBREATH | PROJECT_POLICY:LOCAL_POSITIVE | 41 | 87, 91, 124, 131, 144, 151, 225, 238, 341–343, 346–347, 402, 512–513, 524, 531, 635–637, 666–668, 806–807, 820–821, 956–957, 964–965, 968–969, 985, 996, 1023–1026, 1249 |
| 97 / MOVE_FROSTBREATH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 16 | 1158, 1165, 1167, 1173, 1175, 1188, 1210, 1220, 1229–1230, 1368–1369, 1388, 1393–1395 |
| 97 / MOVE_FROSTBREATH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 904, 915, 1269 |
| 98 / MOVE_WORKUP | PROJECT_POLICY:LOCAL_POSITIVE | 240 | 1–9, 27–28, 35–36, 39–40, 50–53, 56–57, 62, 84–85, 106–107, 113, 128, 133–136, 143, 151–164, 173–174, 183–184, 190, 196–197, 203, 209–210, 214, 216–217, 234, 236–237, 242, 277–285, 307, 335–336, 350, 356–357, 364–366, 380, 440–451, 477, 493, 499–501, 506–507, 523–524, 528, 546, 548–556, 585–587, 612–613, 625–626, 638–639, 672–673, 680–681, 686–688, 691–693, 700–701, 720–735, 757–766, 769–771, 775–776, 780–781, 785–786, 808–809, 832, 834, 939–952, 956–958, 982–983, 992, 995, 999–1001, 1008–1009, 1023–1024, 1027–1030, 1043–1045, 1082, 1102–1110, 1113–1115, 1155, 1170–1171, 1180–1181, 1183–1184, 1208, 1212, 1238, 1241, 1246, 1250–1251, 1253, 1375, 1377 |
| 98 / MOVE_WORKUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 50 | 1294–1296, 1300–1305, 1310–1317, 1321–1324, 1328–1330, 1332–1334, 1344–1345, 1349, 1353–1354, 1356–1357, 1361, 1367–1369, 1382, 1389–1390, 1404–1406, 1408–1411, 1413, 1419 |
| 98 / MOVE_WORKUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 34 | 737, 746, 839, 869–872, 874, 878, 887, 890–892, 897, 912, 914, 916–917, 1072, 1231, 1260–1262, 1265–1266, 1270–1271, 1274–1277, 1290, 1292–1293 |
| 99 / MOVE_WILDCHARGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 461–462, 1088–1092, 1100 |
| 99 / MOVE_WILDCHARGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 16 | 884, 898, 911, 917, 1031–1032, 1204, 1264, 1271, 1284–1285, 1433–1434, 1436–1438 |
| 100 / MOVE_INFESTATION | PROJECT_POLICY:LOCAL_POSITIVE | 110 | 12, 23–24, 43–45, 48–49, 69–73, 88–89, 92–94, 102–103, 109–110, 114, 122, 151, 167–168, 182, 187–189, 194–195, 213, 218–219, 311–312, 361–362, 367–368, 378–379, 386–389, 455, 469, 475–476, 492, 495, 504–505, 518, 530, 588–590, 596–598, 615–616, 621–622, 630–632, 641–642, 648–649, 669–671, 702, 747–750, 774, 783, 796–797, 812–814, 868, 932, 959–960, 964–965, 968–969, 986–987, 995, 1034–1035, 1037, 1076, 1158, 1219–1220, 1247–1248 |
| 100 / MOVE_INFESTATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 35 | 1116–1118, 1121–1122, 1142–1143, 1159, 1163–1165, 1177–1179, 1232–1233, 1306–1309, 1339–1342, 1346–1347, 1376, 1385, 1391, 1396–1399, 1412, 1414 |
| 100 / MOVE_INFESTATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 7 | 873, 877, 902, 1072, 1263, 1267, 1272 |
| 101 / MOVE_POWERUPPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 209 | 4–9, 31, 34–36, 39–40, 54–57, 61–62, 66–68, 74–76, 88–89, 94, 96–97, 104–108, 112–113, 115, 122, 124–126, 143, 149–151, 157–162, 165–166, 180–181, 183–186, 190, 195, 199, 209–210, 215–217, 225, 239–242, 246–248, 277–279, 281–282, 284–285, 296–297, 299–300, 307–308, 317, 322, 334–336, 344–345, 352, 355–357, 362, 364–368, 371–372, 380, 384, 386–387, 399–403, 405, 409–410, 443–445, 455, 461–462, 471–472, 477, 480–481, 499–501, 506–507, 514, 516–517, 519–520, 528, 530, 533–535, 539, 544, 547, 552–553, 558, 565, 567, 569, 584–587, 590–592, 605–608, 612–613, 629, 632, 657, 666–667, 672–678, 684, 701, 758–768, 782–783, 786, 796–797, 809, 817, 828–829, 832, 1039–1042, 1253, 1375, 1380 |
| 101 / MOVE_POWERUPPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 69 | 816, 944, 956–957, 976–977, 983, 995, 1000–1001, 1004, 1011, 1016, 1019, 1031–1035, 1046, 1078, 1084, 1102–1107, 1131, 1140–1141, 1144–1145, 1151–1154, 1158, 1183–1185, 1193, 1208–1209, 1216, 1220, 1224, 1229–1230, 1238, 1240, 1242, 1256, 1295–1296, 1311–1312, 1327, 1357, 1369, 1382, 1388–1389, 1392, 1398, 1404–1405, 1413, 1419 |
| 101 / MOVE_POWERUPPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 737, 746, 870–872, 877–878, 882–884, 889–892, 894–897, 906, 909, 912, 914, 916–917, 1261–1262, 1266–1267, 1271 |
| 102 / MOVE_DAZZLINGGLEAM | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 43–44 |
| 102 / MOVE_DAZZLINGGLEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 173, 746, 751, 875, 877, 884, 893–894, 901–902, 916–918, 991, 1072, 1101, 1267, 1287–1289, 1436–1438 |
| 103 / MOVE_SLUDGEWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 837, 1239, 1258–1259, 1421 |
| 103 / MOVE_SLUDGEWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 49, 69–71, 167–168, 487–488, 766, 838–839, 877, 892, 1207, 1267, 1272, 1284–1285, 1439 |
| 104 / MOVE_PSYSHOCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 104 / MOVE_PSYSHOCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 21 | 102, 746, 794, 875–876, 882–883, 893, 897, 906–908, 916–918, 1101, 1278, 1287, 1289, 1434–1435 |
| 105 / MOVE_BRUTALSWING | PROJECT_POLICY:LOCAL_POSITIVE | 103 | 6, 23–24, 26, 72–73, 112, 123, 130, 147–151, 161–162, 181, 183–184, 212, 214, 225, 232, 237, 248, 279, 300, 329, 334, 350, 369, 379, 397, 400, 405–406, 410, 478–479, 498, 517, 525, 540, 550, 583, 585–587, 605–606, 665, 673, 688, 694–699, 718, 752–756, 766, 795, 814, 817, 944, 956–957, 982–983, 1000–1001, 1017, 1031–1035, 1037, 1040–1042, 1104, 1111–1112, 1135–1136, 1149–1150, 1166, 1170–1171, 1180, 1182, 1185, 1209, 1216, 1219, 1252 |
| 105 / MOVE_BRUTALSWING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 44 | 74–76, 88–89, 160, 190, 477, 1079–1080, 1248, 1258–1259, 1295–1296, 1307, 1309, 1311–1312, 1320, 1330, 1341–1342, 1345, 1350–1354, 1356–1357, 1361, 1368–1369, 1371, 1381, 1387–1388, 1390, 1392, 1403, 1405, 1419, 1422 |
| 105 / MOVE_BRUTALSWING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 34 | 833, 839, 870–871, 873, 879–887, 889–890, 895–896, 903, 905–906, 909, 911–913, 1207, 1261, 1268, 1273–1274, 1283, 1286–1287, 1290 |
| 106 / MOVE_SMARTSTRIKE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 106 / MOVE_SMARTSTRIKE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 575–576, 887, 896, 1101, 1269, 1279, 1432, 1435 |
| 107 / MOVE_ACROBATICS | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 4–5, 953–954 |
| 107 / MOVE_ACROBATICS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 33 | 84–85, 163–164, 249, 634, 683, 746, 839, 870–871, 873, 886, 890–891, 901, 912, 948–950, 991, 1137, 1191–1192, 1261, 1263, 1274–1276, 1281, 1292–1293, 1358 |
| 108 / MOVE_SNARL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 494 |
| 108 / MOVE_SNARL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 25 | 23–24, 37–38, 160, 411, 888–889, 894, 898–899, 903, 1204, 1265, 1274–1275, 1284–1285, 1290–1292, 1413, 1430, 1432–1433 |
| 109 / MOVE_DEFOG | PROJECT_POLICY:LOCAL_POSITIVE | 188 | 6, 12, 15–18, 21–22, 41–42, 49, 83, 123, 142, 144–146, 149, 151, 163–164, 166, 169, 176, 178, 193, 198, 207, 212, 225–227, 249–250, 280–282, 292, 294, 298–300, 302, 304–305, 309–310, 312, 333–334, 358–359, 369, 385–387, 397, 406–408, 411, 446–451, 467, 469, 478–479, 483, 487–488, 494, 508–510, 521–522, 525, 532, 540, 546, 548–550, 572–574, 580–581, 599–600, 614, 619–620, 633–634, 640, 668, 680–683, 688, 690, 694–698, 718, 720–735, 754–756, 769–771, 774, 779, 809, 815, 822–825, 830, 834, 868, 932, 939–941, 948–950, 958–960, 970–971, 981, 990, 997, 1002, 1005, 1009, 1015, 1043–1045, 1048–1064, 1246, 1250, 1252 |
| 109 / MOVE_DEFOG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 34 | 713–717, 1113–1115, 1133, 1137, 1157, 1165, 1178–1179, 1217, 1221–1223, 1258–1259, 1321–1324, 1333–1334, 1349, 1355, 1367, 1388, 1390–1391, 1403, 1421 |
| 109 / MOVE_DEFOG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 870–871, 873–874, 881, 886, 905, 907–908, 1261, 1263 |
| 110 / MOVE_DRAININGKISS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 122, 375, 480–481, 848, 1087–1092 |
| 110 / MOVE_DRAININGKISS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 329, 387, 407, 411, 751, 893, 895, 907, 916–918, 1072, 1101, 1263–1264, 1287–1289, 1358 |
| 111 / MOVE_SMACKDOWN | PROJECT_POLICY:LOCAL_POSITIVE | 56 | 31, 34, 56, 66–68, 95, 104–105, 127, 138–142, 208, 213, 223–224, 318–319, 348–349, 371–372, 381, 384, 388–391, 577–579, 608, 610–611, 614, 617–620, 622, 674, 767–768, 796–797, 993, 1011, 1014, 1016, 1019, 1039, 1076–1077 |
| 111 / MOVE_SMACKDOWN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 1145, 1154, 1159, 1230, 1232 |
| 111 / MOVE_SMACKDOWN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 35 | 27–28, 190, 218, 220–221, 285, 477, 526, 675–676, 737, 758–759, 839, 872, 879, 881, 885, 887, 889, 892, 896, 900, 909, 918, 1262, 1266, 1271–1272, 1275–1276, 1280, 1290, 1430 |
| 112 / MOVE_ROUND | PROJECT_POLICY:LOCAL_POSITIVE | 685 | 1–9, 23–28, 35–40, 43–45, 48–62, 69–76, 79–82, 84–94, 96–97, 100–103, 106–107, 109–113, 116–117, 123, 125–126, 128, 130–131, 133–137, 143–164, 167–168, 170–174, 179–200, 203–207, 209–212, 214–221, 225, 227–234, 236–237, 239–240, 242–250, 277–287, 295–300, 306–307, 309–312, 320–329, 332–336, 339–340, 344–347, 350–354, 356–359, 361–362, 364–369, 377–380, 386–387, 392–397, 399–411, 440–451, 455–458, 461–464, 469–472, 475–479, 482–483, 486–491, 493, 495–503, 506–507, 509–510, 512–515, 517, 519–520, 522–546, 548–556, 575–576, 582–583, 585–587, 593–595, 599–602, 604–606, 612–613, 623–634, 638–639, 643–644, 647–649, 656–657, 660–668, 672–673, 675–678, 680–683, 686–701, 718–735, 752–766, 769–771, 774–781, 785–786, 794–795, 798–801, 808–817, 820–823, 827–830, 832, 834, 848, 868, 919–920, 932, 939–962, 964–971, 974–975, 978–983, 986–987, 992, 995–996, 999–1001, 1008–1009, 1017–1018, 1022–1035, 1037, 1040–1046, 1065, 1073, 1082, 1093–1099, 1102–1115, 1125–1126, 1129–1131, 1133–1141, 1146–1153, 1155, 1160, 1162–1171, 1176–1190, 1193, 1203, 1208–1212, 1215–1216, 1219, 1221–1224, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 112 / MOVE_ROUND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 148 | 713–717, 837, 1079–1080, 1088–1092, 1100, 1234–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 112 / MOVE_ROUND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 103 | 737, 746, 751, 787–788, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1191–1192, 1202, 1204, 1207, 1231, 1260–1293, 1430 |
| 113 / MOVE_ECHOEDVOICE | PROJECT_POLICY:LOCAL_POSITIVE | 242 | 1–6, 25–26, 29–36, 39–40, 50–53, 77–80, 84–87, 104–105, 113, 124, 131, 133–136, 151–154, 161–164, 172–176, 179–181, 186, 196–197, 199–200, 203, 231–232, 238, 241–242, 249–251, 280–285, 288–289, 295–297, 309–310, 313–314, 339–343, 353–354, 358–359, 370–372, 376, 392–394, 406, 411, 446–451, 455, 470–472, 482, 486, 493, 521, 523–524, 528, 536–537, 540, 546, 551–553, 562–563, 572–574, 584, 588–590, 625–626, 638–639, 658–659, 666–667, 688, 696–697, 699, 701, 718, 720–735, 752–753, 761–766, 775–779, 782–783, 785–786, 790–791, 806–808, 822–824, 832, 834, 848, 919–920, 939–941, 945–952, 961–962, 981, 997, 999–1005, 1010, 1012, 1018–1019, 1022, 1027–1030, 1033, 1039, 1046, 1074–1075, 1078, 1082, 1093–1099, 1250, 1377 |
| 113 / MOVE_ECHOEDVOICE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 87 | 1073, 1083–1084, 1088–1092, 1100, 1102–1104, 1137, 1140–1141, 1153–1155, 1158, 1162, 1171–1173, 1178–1182, 1188–1190, 1193, 1210–1216, 1220, 1223–1224, 1226–1227, 1297–1299, 1303–1305, 1310–1317, 1321–1324, 1331–1334, 1343, 1348–1349, 1353–1354, 1368–1369, 1376, 1381–1382, 1384, 1387, 1390, 1393–1395, 1403–1406, 1419 |
| 113 / MOVE_ECHOEDVOICE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 23 | 746, 839, 869–871, 876, 884, 891–893, 900–901, 903, 911, 916–917, 1101, 1260–1261, 1264–1265, 1269–1270 |
| 114 / MOVE_NATURALGIFT | PROJECT_POLICY:LOCAL_POSITIVE | 517 | 1–9, 12, 15–128, 130–131, 133–200, 203–234, 236–251, 277–289, 292, 294–359, 361–397, 399–411, 440–453, 455–464, 466–467, 469–546, 709–710, 718–735, 808, 834, 919–920, 1022, 1037, 1039–1042, 1158, 1219–1220, 1238, 1251–1253, 1375, 1377–1379 |
| 114 / MOVE_NATURALGIFT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 632 | 547–602, 604–654, 656–702, 713–717, 747–750, 752–771, 774–807, 809–830, 832, 837, 848, 868, 932, 939–987, 989–990, 992–1005, 1008–1021, 1023–1035, 1043–1046, 1048–1065, 1073–1080, 1082–1084, 1087–1099, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1242, 1244–1250, 1255–1259, 1294–1357, 1359–1372, 1376, 1380–1422 |
| 114 / MOVE_NATURALGIFT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 61 | 751, 869–916, 1260–1271 |
| 115 / MOVE_QUASH | PROJECT_POLICY:LOCAL_POSITIVE | 53 | 31, 34, 99, 151, 198–199, 230, 243–245, 322, 366, 446–448, 469, 483, 495, 546, 720–735, 783, 828–829, 834, 944, 958, 982, 987–988, 992, 1029–1030, 1034–1035, 1043–1045, 1077 |
| 115 / MOVE_QUASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 30 | 1110, 1115, 1119–1120, 1144–1145, 1148–1154, 1169, 1185, 1189–1190, 1209–1211, 1223, 1226–1227, 1296, 1355, 1399–1402, 1408 |
| 115 / MOVE_QUASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 2 | 894, 1268 |
| 116 / MOVE_TRICKROOM | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 102 |
| 116 / MOVE_TRICKROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 116 / MOVE_TRICKROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 16 | 746, 875–877, 882–883, 893, 897, 902, 916–918, 1072, 1267, 1278, 1287 |
| 117 / MOVE_FLING | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 44, 999, 1160 |
| 117 / MOVE_FLING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 1079–1080, 1088–1092 |
| 117 / MOVE_FLING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 61 | 737, 746, 839, 870–872, 875–879, 882–884, 886–887, 889–897, 902, 909, 911–917, 996, 1072, 1204, 1231, 1261–1262, 1264, 1266–1268, 1271–1272, 1274–1276, 1284–1285, 1288–1290, 1292–1293, 1358, 1426–1429 |
| 118 / MOVE_AURORAVEIL | PROJECT_POLICY:LOCAL_POSITIVE | 13 | 124, 144, 151, 225, 238, 402, 524, 531, 668, 1023–1026 |
| 118 / MOVE_AURORAVEIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 27 | 513, 635–637, 806–807, 820–821, 1158, 1165, 1167, 1173, 1175, 1188, 1210, 1220–1221, 1229–1230, 1249, 1368–1369, 1388, 1393–1395, 1400 |
| 119 / MOVE_SKYDROP | PROJECT_POLICY:LOCAL_POSITIVE | 25 | 6, 142, 144–146, 149, 151, 227, 249–250, 310, 406, 680–681, 694–695, 754–755, 809, 825, 955, 1002, 1009, 1075, 1246 |
| 119 / MOVE_SKYDROP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 1115, 1179, 1182, 1221, 1223, 1355 |
| 119 / MOVE_SKYDROP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 870–871, 881, 911, 1261 |
| 120 / MOVE_NATUREPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 136 | 1–3, 43–45, 69–71, 74–76, 95, 102–103, 114, 141, 151–157, 182, 185, 191–192, 208, 218–219, 222, 251, 277–279, 295–300, 321, 327, 339–340, 344–345, 363, 369, 440–442, 459–460, 473–474, 491, 509, 518, 523, 538–539, 545, 548–550, 577–579, 593–595, 599–602, 609–611, 638–639, 643–644, 650–651, 693, 719, 758–760, 767–768, 777–781, 796–797, 806–807, 811, 816–819, 824, 827, 848, 939–941, 960, 970–973, 978–982, 997, 1002–1005, 1013, 1031–1033, 1037, 1238, 1242, 1250 |
| 120 / MOVE_NATUREPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 52 | 1102–1104, 1121–1122, 1126, 1133–1136, 1148–1153, 1156, 1163, 1165, 1168, 1172–1175, 1182, 1185, 1190, 1203, 1209–1211, 1225, 1294–1296, 1318–1320, 1339–1342, 1344–1345, 1383, 1399, 1408, 1415–1418, 1422 |
| 120 / MOVE_NATUREPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 510, 751, 869, 885, 890, 900, 918, 1101, 1260 |
| 121 / MOVE_CUT | PROJECT_POLICY:LOCAL_POSITIVE | 291 | 1–6, 15, 19–20, 27–34, 43–47, 50–53, 69–73, 83, 98–99, 108, 112, 114–115, 123, 127, 141, 149, 151–162, 182, 190–192, 196–197, 207–208, 212, 214–217, 227, 243–245, 248, 251, 277–282, 288–289, 299–303, 307, 317, 322, 326–327, 344–345, 363–366, 369, 376, 382–384, 390–391, 395–397, 399–400, 405, 407–408, 410, 440–448, 452–453, 455, 459–460, 462, 469–470, 477–481, 484–485, 487–488, 496–498, 504–505, 507–508, 514, 516–518, 525, 528, 536–537, 540, 544, 546, 548–550, 554–558, 562–569, 582–583, 593–595, 598, 601–602, 604–606, 610–611, 619–620, 623–624, 639–642, 648–649, 651, 657, 663–667, 674, 677–685, 691–693, 696–697, 699–700, 718, 720–735, 752–753, 757–768, 782–783, 785–789, 794–797, 800–803, 808–810, 815–817, 822–825, 830, 832, 834, 919–920, 1040–1042, 1238, 1241–1242, 1246, 1252–1253, 1380 |
| 121 / MOVE_CUT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 124 | 942–944, 951–952, 961–962, 970–971, 973–975, 979–980, 985, 989–990, 992–993, 995, 999–1001, 1008, 1015–1017, 1020–1021, 1023–1024, 1027–1030, 1046, 1048–1064, 1074–1075, 1078–1080, 1082, 1102–1104, 1111–1112, 1119–1120, 1125–1126, 1140–1143, 1151–1155, 1157, 1169, 1172–1173, 1176–1180, 1183–1185, 1193, 1208–1209, 1212, 1217, 1226–1227, 1233, 1240, 1244–1245, 1255–1256, 1294–1296, 1310–1312, 1330, 1337–1338, 1361, 1370, 1392–1395, 1400, 1403–1405, 1407–1408, 1413 |
| 121 / MOVE_CUT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 29 | 833, 869–871, 873, 878–879, 885–887, 889–891, 894, 896, 903, 905–909, 912–913, 916, 1101, 1260–1261, 1265, 1268 |
| 122 / MOVE_FLY | PROJECT_POLICY:LOCAL_POSITIVE | 1 | 84 |
| 122 / MOVE_FLY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 400, 498, 522 |
| 122 / MOVE_FLY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 15 | 870–871, 874, 881, 901, 905, 907–908, 911, 1191–1192, 1207, 1261, 1277, 1281 |
| 123 / MOVE_SURF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 1087–1092, 1100 |
| 123 / MOVE_SURF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 32 | 820, 839, 872, 876, 878, 880, 889, 892, 896, 899, 907–908, 910–911, 913, 917, 1047, 1191–1192, 1202, 1249, 1262, 1264, 1268–1269, 1271, 1276, 1279, 1358, 1436–1438 |
| 124 / MOVE_STRENGTH | PROJECT_POLICY:LOCAL_POSITIVE | 379 | 1–9, 20, 23–36, 39–40, 54–59, 61–62, 66–68, 74–80, 88–89, 94–95, 98–99, 102–108, 111–113, 115, 125–128, 130–131, 134–136, 142–143, 149–151, 153–154, 156–157, 159–160, 162, 166, 180–181, 183–186, 190, 195, 199, 203–210, 212–217, 219–222, 229, 231–232, 236–237, 241–244, 248–250, 277–285, 287, 289, 296–297, 299–300, 307–308, 313–314, 316–317, 319–321, 324, 326–327, 331–343, 345, 355–357, 362, 364–369, 371–372, 376, 379–380, 382–384, 389, 391, 395–397, 399–406, 410, 440–445, 447–448, 453, 455–458, 461–464, 471–472, 476–477, 481, 488, 490, 496–507, 513–514, 516–520, 523–526, 528–530, 536–540, 544, 546, 550–553, 556, 558, 560–561, 577–579, 582–583, 585–587, 590–592, 598, 605–608, 610–613, 617–618, 632, 651, 657, 663–667, 672–676, 679–681, 685–688, 691–701, 718, 720–735, 752–760, 764–768, 775–776, 780–783, 796–797, 804–805, 809, 814, 816–817, 820–821, 826, 830, 834, 919–920, 1022, 1037, 1039–1042, 1238, 1246, 1249, 1253, 1375, 1377–1379 |
| 124 / MOVE_STRENGTH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 170 | 86–87, 837, 944, 952, 956–957, 961–962, 966–967, 976–977, 983, 985, 992–993, 1000–1002, 1004, 1008, 1011–1012, 1014, 1016–1017, 1019, 1021, 1023–1024, 1031–1035, 1046, 1076, 1078–1080, 1082, 1084, 1088–1099, 1102–1107, 1111–1112, 1120, 1123–1124, 1126, 1128, 1130–1131, 1134, 1136, 1141, 1143–1145, 1153–1155, 1157, 1159, 1162, 1166, 1168, 1170–1174, 1176, 1181, 1183–1185, 1188, 1193, 1203, 1208–1210, 1212–1217, 1222, 1224, 1226–1227, 1229–1230, 1234–1235, 1240–1241, 1248, 1250, 1252, 1256, 1295–1296, 1298–1299, 1301–1305, 1307, 1309, 1311–1312, 1317, 1326–1327, 1336, 1343, 1351–1352, 1361, 1366, 1368–1369, 1371, 1376, 1380–1382, 1385, 1387, 1389–1390, 1392, 1394–1395, 1399–1401, 1403–1411, 1413, 1419 |
| 124 / MOVE_STRENGTH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 50 | 737, 746, 838, 869–872, 876–892, 895–900, 903, 905–906, 909–916, 1260–1262, 1264, 1266–1269, 1271 |
| 125 / MOVE_DIVE | PROJECT_POLICY:LOCAL_POSITIVE | 125 | 7–9, 54–55, 60–62, 72–73, 79–80, 86–87, 90–91, 116–117, 130–131, 134, 149–151, 158–160, 170–171, 183–184, 186, 194–195, 199, 211, 230, 245, 249, 283–285, 296–297, 323–325, 327–329, 373–375, 404, 406–408, 446–448, 453, 471–472, 475–476, 509–510, 537, 542–543, 546, 554–556, 568–569, 633–634, 647, 667, 720–735, 764–766, 798–801, 834, 920, 945–947, 969, 1108–1110, 1125–1126, 1137–1139, 1167, 1178–1179, 1208, 1215–1216, 1224, 1241 |
| 125 / MOVE_DIVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 15 | 1239, 1255, 1257, 1300–1302, 1353–1354, 1356–1357, 1371–1372, 1376, 1407, 1412 |
| 125 / MOVE_DIVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 21 | 872, 876, 880, 882–883, 892, 899, 907–908, 910–911, 1047, 1191–1192, 1202, 1262, 1268–1269, 1276, 1279, 1293 |
| 126 / MOVE_ROCKSMASH | PROJECT_POLICY:LOCAL_POSITIVE | 435 | 1–9, 15, 19–20, 25–36, 46–47, 50–51, 54–59, 61–62, 66–68, 74–76, 80, 89, 94–95, 98–99, 104–108, 111–115, 123, 125–128, 130–131, 134–136, 138–146, 149–151, 153–154, 156–157, 159–160, 162, 166, 175–176, 180–181, 183–186, 190, 194–195, 199, 203–210, 212–222, 227–229, 231–232, 236–237, 239–246, 248–250, 277–289, 296–300, 307–308, 313–314, 316–317, 319–322, 324, 326–327, 331–336, 339–343, 355–357, 359, 362, 364–369, 371–372, 376, 379–384, 389–391, 395–397, 399–406, 410, 440–445, 447–448, 452–453, 455, 461–464, 471–472, 476–477, 480–481, 487–488, 490, 496–507, 513–514, 516–521, 523–526, 528–530, 536–540, 544, 546–547, 550–556, 558–561, 563–569, 576–579, 582, 585–587, 589–592, 596–598, 605–608, 612–613, 617–620, 624, 632, 639, 642, 650–654, 657, 663–667, 672–688, 691–701, 718, 720–735, 752–760, 764–768, 775–776, 780–784, 787–789, 796–797, 804–807, 809, 814, 816–821, 826, 830, 834, 919–920, 1022, 1039–1042, 1238, 1241, 1246, 1249, 1252–1253, 1375, 1377–1380 |
| 126 / MOVE_ROCKSMASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 136 | 837, 948–950, 956–957, 966–967, 983, 985, 1084, 1088–1099, 1102–1107, 1111–1115, 1119–1120, 1123–1126, 1130–1131, 1134–1136, 1138–1139, 1141, 1144–1145, 1152–1154, 1157–1159, 1162, 1166, 1170–1176, 1179–1185, 1188, 1190, 1193, 1208–1210, 1216–1217, 1220, 1222, 1224, 1226–1227, 1229–1230, 1232–1235, 1240, 1242, 1245, 1248, 1250, 1256, 1258–1259, 1295–1296, 1301–1302, 1307, 1309, 1311–1312, 1327, 1330, 1343, 1350–1352, 1367, 1376, 1381, 1385, 1387, 1389–1390, 1392, 1394–1395, 1400, 1403–1405, 1407–1413, 1419, 1422 |
| 126 / MOVE_ROCKSMASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 57 | 247, 583, 610–611, 737, 746, 833, 838, 869–873, 876–892, 894–897, 899–901, 903, 905–906, 909–916, 1260–1262, 1264, 1266–1269, 1271 |
| 127 / MOVE_WATERFALL | PROJECT_POLICY:LOCAL_POSITIVE | 5 | 7–9, 72–73 |
| 127 / MOVE_WATERFALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 634 |
| 127 / MOVE_WATERFALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 839, 872, 876, 880, 892, 899, 907–908, 910–911, 1047, 1202, 1262, 1269, 1276, 1279, 1293, 1358 |
| 128 / MOVE_ROCKCLIMB | PROJECT_POLICY:LOCAL_POSITIVE | 113 | 3, 9, 27–28, 31, 34, 55–57, 59, 62, 66–68, 74–76, 95, 104–108, 111–113, 115, 125–128, 139, 141, 143, 150–151, 154, 157, 160, 181, 208, 210, 217, 242–245, 248, 279, 282, 285, 297, 335–336, 365–366, 372, 380, 384, 401–403, 405, 440–445, 448, 453, 461–462, 496–499, 501, 505–507, 513, 516–517, 519–520, 526, 538–540, 544, 546, 718, 720–735, 834, 1039, 1253, 1375 |
| 128 / MOVE_ROCKCLIMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 147 | 207, 288–289, 400, 452, 525, 552–553, 558, 560–561, 578–579, 582–583, 585–587, 590–592, 596–598, 604–606, 612–613, 618, 648–651, 672–676, 679, 685, 691–693, 700, 757, 768, 782–783, 797, 809, 826, 837, 944, 952, 956–957, 961–962, 967, 977, 983, 990, 992, 1000–1001, 1011–1012, 1016, 1023–1024, 1031–1033, 1046, 1048–1064, 1082, 1084, 1104, 1107, 1124, 1126, 1131, 1134, 1136, 1141, 1145, 1153–1154, 1162, 1166, 1171, 1176, 1183–1185, 1188, 1193, 1208–1210, 1226–1227, 1230, 1235, 1238, 1240, 1256, 1296, 1299, 1302, 1311–1312, 1326–1327, 1338, 1355, 1361, 1389, 1392, 1394–1395, 1405–1411, 1413, 1419 |
| 128 / MOVE_ROCKCLIMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 21 | 869, 872, 878–879, 882–885, 889–892, 896, 909, 913–915, 1260, 1262, 1266, 1271 |

## Appendix I — exact Tutor order and complete positive disagreement sets

Ordered move-list SHA-256: `0ce90e03cab093e2362ad5977e13708ae2aeb1ed2e6706fd1cf4e866a04bdb46`. Source-reconstructed bitset SHA-256: `e0e893b8e166460e072cd55c3d331e045e1983af50d11cdb1469554dedb28a3b`. These hashes cover source text normalization, not a ROM or build artifact.

| 1-based slot | Move |
| --- | --- |
| 1 | MOVE_FIREPUNCH |
| 2 | MOVE_ICEPUNCH |
| 3 | MOVE_THUNDERPUNCH |
| 4 | MOVE_SNORE |
| 5 | MOVE_HEALBELL |
| 6 | MOVE_ELECTROWEB |
| 7 | MOVE_LOWKICK |
| 8 | MOVE_UPROAR |
| 9 | MOVE_BIND |
| 10 | MOVE_HELPINGHAND |
| 11 | MOVE_BLOCK |
| 12 | MOVE_WORRYSEED |
| 13 | MOVE_COVET |
| 14 | MOVE_BUGBITE |
| 15 | MOVE_SNATCH |
| 16 | MOVE_SPITE |
| 17 | MOVE_AFTERYOU |
| 18 | MOVE_SYNTHESIS |
| 19 | MOVE_SIGNALBEAM |
| 20 | MOVE_GRAVITY |
| 21 | MOVE_IRONDEFENSE |
| 22 | MOVE_TELEKINESIS |
| 23 | MOVE_MAGNETRISE |
| 24 | MOVE_BOUNCE |
| 25 | MOVE_ROLEPLAY |
| 26 | MOVE_IRONHEAD |
| 27 | MOVE_AQUATAIL |
| 28 | MOVE_PAINSPLIT |
| 29 | MOVE_TAILWIND |
| 30 | MOVE_ENDEAVOR |
| 31 | MOVE_ICYWIND |
| 32 | MOVE_ZENHEADBUTT |
| 33 | MOVE_SEEDBOMB |
| 34 | MOVE_LASERFOCUS |
| 35 | MOVE_TRICK |
| 36 | MOVE_DRILLRUN |
| 37 | MOVE_MAGICCOAT |
| 38 | MOVE_MAGICROOM |
| 39 | MOVE_WONDERROOM |
| 40 | MOVE_LIQUIDATION |
| 41 | MOVE_GASTROACID |
| 42 | MOVE_FOULPLAY |
| 43 | MOVE_SUPERFANG |
| 44 | MOVE_OUTRAGE |
| 45 | MOVE_SKYATTACK |
| 46 | MOVE_THROATCHOP |
| 47 | MOVE_STOMPINGTANTRUM |
| 48 | MOVE_EARTHPOWER |
| 49 | MOVE_GUNKSHOT |
| 50 | MOVE_DUALCHOP |
| 51 | MOVE_HEATWAVE |
| 52 | MOVE_HYPERVOICE |
| 53 | MOVE_SUPERPOWER |
| 54 | MOVE_KNOCKOFF |
| 55 | MOVE_PSYCHUP |
| 56 | MOVE_VACUUMWAVE |
| 57 | MOVE_LASTRESORT |
| 58 | MOVE_CONFIDE |
| 59 | MOVE_GRASSPLEDGE |
| 60 | MOVE_FIREPLEDGE |
| 61 | MOVE_WATERPLEDGE |
| 62 | MOVE_FRENZYPLANT |
| 63 | MOVE_BLASTBURN |
| 64 | MOVE_HYDROCANNON |
| 65 | MOVE_FOCUSENERGY |
| 66 | MOVE_COSMICPOWER |
| 67 | MOVE_BATONPASS |
| 68 | MOVE_ENCORE |
| 69 | MOVE_SCREECH |
| 70 | MOVE_FAKETEARS |
| 71 | MOVE_SCARYFACE |
| 72 | MOVE_VENOMDRENCH |
| 73 | MOVE_SPIKES |
| 74 | MOVE_TOXICSPIKES |
| 75 | MOVE_DRAGONDANCE |
| 76 | MOVE_AGILITY |
| 77 | MOVE_NASTYPLOT |
| 78 | MOVE_GRASSYTERRAIN |
| 79 | MOVE_MISTYTERRAIN |
| 80 | MOVE_ELECTRICTERRAIN |
| 81 | MOVE_PSYCHICTERRAIN |
| 82 | MOVE_WHIRLPOOL |
| 83 | MOVE_FIRESPIN |
| 84 | MOVE_SANDTOMB |
| 85 | MOVE_PINMISSILE |
| 86 | MOVE_ICICLESPEAR |
| 87 | MOVE_TAILSLAP |
| 88 | MOVE_ROCKBLAST |
| 89 | MOVE_THUNDERFANG |
| 90 | MOVE_ICEFANG |
| 91 | MOVE_FIREFANG |
| 92 | MOVE_BODYSLAM |
| 93 | MOVE_BODYPRESS |
| 94 | MOVE_HEATCRASH |
| 95 | MOVE_HEAVYSLAM |
| 96 | MOVE_REVERSAL |
| 97 | MOVE_ELECTROBALL |
| 98 | MOVE_STOREDPOWER |
| 99 | MOVE_BREAKINGSWIPE |
| 100 | MOVE_RAZORSHELL |
| 101 | MOVE_HEX |
| 102 | MOVE_WEATHERBALL |
| 103 | MOVE_AIRSLASH |
| 104 | MOVE_AURASPHERE |
| 105 | MOVE_BLAZEKICK |
| 106 | MOVE_BUGBUZZ |
| 107 | MOVE_CROSSPOISON |
| 108 | MOVE_CRUNCH |
| 109 | MOVE_DARKESTLARIAT |
| 110 | MOVE_HIGHHORSEPOWER |
| 111 | MOVE_LEAFBLADE |
| 112 | MOVE_MUDDYWATER |
| 113 | MOVE_MYSTICALFIRE |
| 114 | MOVE_PHANTOMFORCE |
| 115 | MOVE_PLAYROUGH |
| 116 | MOVE_POLLENPUFF |
| 117 | MOVE_POWERGEM |
| 118 | MOVE_PSYCHICFANGS |
| 119 | MOVE_PSYCHOCUT |
| 120 | MOVE_BRAVEBIRD |
| 121 | MOVE_CLOSECOMBAT |
| 122 | MOVE_FLAREBLITZ |
| 123 | MOVE_HURRICANE |
| 124 | MOVE_HYDROPUMP |
| 125 | MOVE_LEAFSTORM |
| 126 | MOVE_MEGAHORN |
| 127 | MOVE_POWERWHIP |
| 128 | MOVE_SOLARBLADE |
| 129 | MOVE_EXPANDINGFORCE |
| 130 | MOVE_STEELROLLER |
| 131 | MOVE_SCALESHOT |
| 132 | MOVE_METEORBEAM |
| 133 | MOVE_MISTYEXPLOSION |
| 134 | MOVE_GRASSYGLIDE |
| 135 | MOVE_RISINGVOLTAGE |
| 136 | MOVE_TERRAINPULSE |
| 137 | MOVE_SKITTERSMACK |
| 138 | MOVE_BURNINGJEALOUSY |
| 139 | MOVE_LASHOUT |
| 140 | MOVE_POLTERGEIST |
| 141 | MOVE_CORROSIVEGAS |
| 142 | MOVE_COACHING |
| 143 | MOVE_FLIPTURN |
| 144 | MOVE_TRIPLEAXEL |
| 145 | MOVE_DUALWINGBEAT |
| 146 | MOVE_SCORCHINGSANDS |
| 147 | MOVE_CONFUSERAY |
| 148 | MOVE_CHILLINGWATER |
| 149 | MOVE_POUNCE |
| 150 | MOVE_TRAILBLAZE |
| 151 | MOVE_ICESPINNER |
| 152 | MOVE_TERABLAST |

Exception sets use **decimal local DPE species IDs**, inclusive ranges. Resolve them against the pinned `include/species.h` and Appendix A; the helper’s JSON gives every corresponding source key. Each displayed set is complete, not a sample. Mapping blocks are shown even for absent bits. Unverifiable absent/absent pairs are not disagreements and are included only in the aggregate count. A REFERENCE_POSITIVE_LOCAL_NEGATIVE entry is missing observable acquisition evidence locally; LOCAL_POSITIVE means extra/cross-method/unmapped local compatibility. Neither is silently declared an approved policy or a genuine binary mismatch.

| Slot / move | Classification and direction | Records | Complete local species-ID set |
| --- | --- | --- | --- |
| 1 / MOVE_FIREPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 25 | 199, 1077, 1107, 1131, 1141, 1153–1154, 1183–1184, 1193, 1208, 1224, 1229–1230, 1238, 1248, 1256, 1312, 1327, 1382, 1389, 1392, 1404, 1413, 1419 |
| 1 / MOVE_FIREPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 761 |
| 1 / MOVE_FIREPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 24 | 737, 746, 870–871, 875, 877–878, 882–884, 889, 891, 893–894, 896–897, 909, 912, 916–917, 1261, 1266–1267, 1271 |
| 2 / MOVE_ICEPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 27 | 180–181, 1084, 1144–1145, 1153–1154, 1158, 1167, 1183–1184, 1208, 1216, 1220, 1229–1230, 1312, 1327, 1357, 1369, 1382, 1388–1389, 1392, 1404, 1413, 1419 |
| 2 / MOVE_ICEPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 74–76, 1031–1033 |
| 2 / MOVE_ICEPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 746, 839, 872, 875–878, 882–883, 889, 892–897, 906, 912, 914–917, 1262, 1266–1267, 1271 |
| 3 / MOVE_THUNDERPUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 27 | 199, 1084, 1141, 1153–1154, 1169, 1172–1173, 1183–1184, 1193, 1208, 1224, 1238, 1248, 1295–1296, 1311–1312, 1327, 1382, 1389, 1392, 1398, 1404, 1413, 1419 |
| 3 / MOVE_THUNDERPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 1088–1092, 1100 |
| 3 / MOVE_THUNDERPUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 28 | 746, 870–871, 875, 877–878, 882–884, 889–891, 893–897, 906, 909, 912, 914, 916–917, 1261, 1264, 1266–1267, 1271 |
| 4 / MOVE_SNORE | PROJECT_POLICY:LOCAL_POSITIVE | 113 | 818–819, 1073, 1083–1084, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1233 |
| 4 / MOVE_SNORE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 147 | 713–717, 837, 1079–1080, 1088–1092, 1234–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 4 / MOVE_SNORE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 80 | 10–11, 290–291, 293, 454, 465, 737, 746, 751, 833, 838–839, 869–918, 991, 1047, 1072, 1101, 1260–1272 |
| 5 / MOVE_HEALBELL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 108, 144, 149, 286–287, 490, 1073, 1221, 1384, 1404 |
| 5 / MOVE_HEALBELL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 746, 884, 893, 901, 912, 917–918, 1269–1270 |
| 6 / MOVE_ELECTROWEB | PROJECT_POLICY:LOCAL_POSITIVE | 13 | 1018, 1073, 1169, 1186, 1307, 1310–1312, 1331–1334, 1386 |
| 6 / MOVE_ELECTROWEB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 713–717, 1088–1092, 1100, 1306, 1406 |
| 6 / MOVE_ELECTROWEB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 873, 884, 1263–1264 |
| 7 / MOVE_LOWKICK | PROJECT_POLICY:LOCAL_POSITIVE | 69 | 54, 149, 180–181, 203, 216, 307, 352, 471, 513, 941, 983, 992, 1102–1107, 1151–1154, 1166, 1172–1174, 1183–1185, 1208–1209, 1213–1214, 1222, 1238, 1240, 1242, 1245, 1250, 1256, 1295–1296, 1300–1302, 1307, 1309, 1311–1315, 1338, 1349, 1367, 1376–1377, 1385, 1389, 1392, 1398, 1404–1405, 1407, 1412–1413, 1419, 1422 |
| 7 / MOVE_LOWKICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 746, 839, 878, 882–883, 887, 889–892, 894, 896–897, 912, 914, 916–917, 1266 |
| 8 / MOVE_UPROAR | PROJECT_POLICY:LOCAL_POSITIVE | 76 | 186, 206, 216, 324, 351–352, 448, 469, 796–797, 809, 963, 1027–1028, 1093–1099, 1102–1104, 1111–1112, 1127–1128, 1137, 1141, 1151–1153, 1155, 1162, 1169, 1188–1189, 1193, 1210–1212, 1229–1230, 1233, 1255, 1258–1259, 1303–1305, 1321–1324, 1333–1334, 1348–1349, 1359–1361, 1365–1366, 1378–1379, 1382, 1405, 1413, 1415–1421 |
| 8 / MOVE_UPROAR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 713–717, 1087–1092, 1409–1411 |
| 8 / MOVE_UPROAR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 737, 746, 874, 877–878, 880, 888–889, 892, 896, 898–899, 901, 909–912, 917, 1264–1265, 1267, 1271 |
| 9 / MOVE_BIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 19 | 837, 1108–1110, 1135–1136, 1142–1145, 1182, 1185, 1209, 1233, 1341–1342, 1353–1354, 1362 |
| 9 / MOVE_BIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 838, 869, 879, 885, 911, 1260 |
| 10 / MOVE_HELPINGHAND | PROJECT_POLICY:LOCAL_POSITIVE | 331 | 1–9, 50–55, 79–82, 86–91, 96–97, 100–101, 108, 112, 123, 127, 130–131, 144–150, 157, 175–176, 179–182, 194–195, 199–200, 203–206, 209–210, 212, 215–217, 223–225, 228–229, 231–232, 234, 243–250, 309–312, 320–324, 329, 339–340, 344–347, 351–352, 355, 358–359, 361–362, 364–369, 377–380, 395–397, 404–406, 446–451, 455, 469, 475–476, 478–479, 482–483, 487–490, 495–498, 502–503, 509–510, 512–517, 521, 529–532, 604–606, 623–624, 638–639, 675–676, 680–681, 685, 687–688, 696–697, 699, 752–753, 761–766, 780–781, 939–941, 951–952, 956–957, 961–962, 1008–1009, 1027–1030, 1034–1035, 1046, 1073, 1078, 1082, 1105–1107, 1117–1118, 1121–1122, 1127–1128, 1134, 1141, 1148–1150, 1154–1155, 1157, 1160, 1162, 1165, 1168, 1177–1181, 1183–1185, 1190, 1193, 1203, 1208–1212, 1215–1217, 1221–1224, 1226–1227, 1234–1235, 1245–1246, 1250–1253, 1294–1305, 1310–1330, 1335–1338, 1343–1345, 1348–1354, 1356–1357, 1362, 1365–1366, 1368–1369, 1372, 1376–1379, 1382, 1384, 1388, 1391, 1393–1395, 1404–1406, 1408, 1412–1413, 1420, 1422 |
| 10 / MOVE_HELPINGHAND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 713–717, 1088–1092 |
| 10 / MOVE_HELPINGHAND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 746, 751, 878, 887, 891, 893, 897, 907–908, 912, 914, 916–918, 1047, 1264, 1266, 1270 |
| 11 / MOVE_BLOCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 27 | 1, 4, 7, 837, 1129–1131, 1158–1159, 1166, 1176, 1215–1216, 1224, 1232, 1241, 1249, 1306–1307, 1327, 1339–1340, 1381, 1387, 1392, 1408, 1419 |
| 11 / MOVE_BLOCK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 16 | 833, 838, 869, 876, 885, 889, 896, 904, 906, 909–910, 915, 1101, 1260, 1269, 1271 |
| 12 / MOVE_WORRYSEED | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 37 | 709–710, 1102–1104, 1121–1122, 1133–1134, 1185, 1190, 1209–1211, 1236–1237, 1294–1296, 1318–1320, 1339–1342, 1344–1345, 1383, 1399, 1408, 1414–1418, 1422 |
| 12 / MOVE_WORRYSEED | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 751, 869, 890, 915, 1260 |
| 13 / MOVE_COVET | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 46 | 1088–1092, 1100, 1111–1112, 1119–1120, 1123–1124, 1148–1155, 1157, 1168–1169, 1185, 1203, 1209, 1212, 1217, 1226–1227, 1234–1235, 1245, 1303–1305, 1316–1317, 1350–1352, 1382, 1413, 1419–1421 |
| 13 / MOVE_COVET | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 13 | 746, 878, 907, 912, 917–918, 1047, 1072, 1075, 1264–1265, 1270–1271 |
| 14 / MOVE_BUGBITE | PROJECT_POLICY:LOCAL_POSITIVE | 10 | 1164–1165, 1306–1309, 1346–1347, 1385, 1414 |
| 14 / MOVE_BUGBITE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 1117–1118, 1142–1143 |
| 14 / MOVE_BUGBITE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 873, 879, 886–887, 1263 |
| 15 / MOVE_SNATCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 50 | 713–717, 1119–1120, 1151–1155, 1159, 1169, 1179, 1184–1185, 1190, 1209–1212, 1226–1227, 1229–1230, 1232, 1240, 1244–1245, 1256, 1296, 1307, 1309, 1328–1330, 1338, 1348–1349, 1355, 1361, 1382, 1384, 1400, 1402, 1404, 1419–1421 |
| 15 / MOVE_SNATCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 737, 746, 839, 875, 877, 882–883, 888, 893–895, 902–903, 916–917, 1072, 1265, 1267, 1271 |
| 16 / MOVE_SPITE | PROJECT_POLICY:LOCAL_POSITIVE | 42 | 89, 150, 211, 369, 469, 798–799, 1113–1115, 1146–1147, 1155, 1212, 1223, 1238–1240, 1244–1245, 1255–1257, 1309, 1328–1330, 1336, 1339–1340, 1384, 1399–1402, 1415–1421 |
| 16 / MOVE_SPITE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 713–717, 837, 1156, 1159, 1232–1233 |
| 16 / MOVE_SPITE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 833, 838–839, 877–878, 880, 888–889, 894, 896, 899, 902–904, 1072, 1265, 1267, 1272 |
| 17 / MOVE_AFTERYOU | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 20 | 1073, 1118, 1148–1150, 1158–1159, 1168, 1203, 1215–1216, 1223–1224, 1232, 1313–1315, 1376, 1383, 1412 |
| 17 / MOVE_AFTERYOU | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 833, 876, 884, 900, 912, 917–918, 1072, 1271 |
| 18 / MOVE_SYNTHESIS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 35 | 709–710, 1102–1104, 1121–1122, 1133–1134, 1185, 1190, 1209–1211, 1236–1237, 1294–1296, 1318–1320, 1339–1340, 1344–1345, 1383, 1399, 1408, 1414–1418, 1422 |
| 18 / MOVE_SYNTHESIS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 751, 869, 890, 915, 1260 |
| 19 / MOVE_SIGNALBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 67 | 713–717, 1073, 1079–1080, 1088–1092, 1117–1118, 1127–1128, 1141–1143, 1148–1150, 1165, 1168–1169, 1172–1173, 1186, 1190, 1193, 1203, 1210–1211, 1213–1216, 1221–1222, 1224, 1236–1237, 1239, 1257, 1306–1312, 1346–1349, 1370, 1385–1386, 1388, 1390–1391, 1404, 1406–1408, 1420 |
| 19 / MOVE_SIGNALBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 20 | 746, 872, 875–876, 882–884, 893–894, 897–898, 904, 906, 910, 916–917, 1262–1264, 1269 |
| 20 / MOVE_GRAVITY | PROJECT_POLICY:LOCAL_POSITIVE | 16 | 196, 394, 524, 1018, 1073, 1150, 1166, 1168, 1182, 1190, 1210–1211, 1327, 1347, 1386, 1408 |
| 20 / MOVE_GRAVITY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 1079–1080, 1118 |
| 20 / MOVE_GRAVITY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 746, 875, 882–883, 894, 897, 906, 917–918, 991, 1101 |
| 21 / MOVE_IRONDEFENSE | PROJECT_POLICY:LOCAL_POSITIVE | 75 | 112, 185, 208, 213, 319, 395, 442, 505, 517, 608, 932, 1073, 1083–1084, 1115, 1117–1118, 1126, 1129–1131, 1133–1134, 1136, 1154–1159, 1162, 1166–1167, 1170–1171, 1175–1176, 1180–1181, 1184, 1188, 1208, 1210, 1212, 1216, 1220, 1224–1225, 1230, 1232–1233, 1258–1259, 1325–1327, 1329–1330, 1343, 1346–1347, 1359–1360, 1362–1364, 1386–1387, 1389, 1392, 1408, 1415–1418 |
| 21 / MOVE_IRONDEFENSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 21 / MOVE_IRONDEFENSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 710, 833, 872–873, 876, 879, 886–887, 889, 895–896, 905–906, 914, 918, 1262–1263, 1268 |
| 22 / MOVE_TELEKINESIS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 43 | 713–717, 1079–1080, 1118, 1148–1150, 1159, 1168, 1190, 1203, 1210–1211, 1213–1216, 1221, 1224, 1232, 1237, 1246, 1299, 1329–1330, 1339–1340, 1347–1349, 1370, 1382, 1384, 1396–1398, 1404, 1408, 1420 |
| 22 / MOVE_TELEKINESIS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 746, 875–877, 882–883, 893–894, 897, 902, 906–908, 916–918, 991, 1072, 1267 |
| 23 / MOVE_MAGNETRISE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 43 | 1073, 1079–1080, 1088–1092, 1127–1128, 1141, 1148–1150, 1163, 1169, 1172–1173, 1186, 1193, 1233, 1236–1237, 1310–1312, 1331–1332, 1350–1352, 1359–1360, 1362, 1386–1392, 1398, 1406 |
| 23 / MOVE_MAGNETRISE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 710, 833, 884–885, 895–896, 898, 906, 914, 918, 991, 1264 |
| 24 / MOVE_BOUNCE | PROJECT_POLICY:LOCAL_POSITIVE | 14 | 1105–1110, 1124, 1138–1139, 1186, 1213–1214, 1222, 1233 |
| 24 / MOVE_BOUNCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 1239, 1244–1245, 1255, 1257, 1309, 1356–1357, 1367–1370, 1381–1382, 1387, 1402, 1405, 1408 |
| 24 / MOVE_BOUNCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 839, 880, 891, 899, 903, 912 |
| 25 / MOVE_ROLEPLAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 25 | 1118, 1146–1147, 1159, 1168, 1190, 1203, 1210–1211, 1232, 1242, 1258–1259, 1328–1330, 1347–1349, 1382, 1389, 1409–1411, 1420 |
| 25 / MOVE_ROLEPLAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 18 | 746, 839, 875, 877, 882–883, 888, 891, 894, 897, 902–903, 907, 914–915, 917, 1266–1267 |
| 26 / MOVE_IRONHEAD | PROJECT_POLICY:LOCAL_POSITIVE | 82 | 81–82, 147–148, 155–157, 205, 231–232, 379, 395–397, 440–441, 489, 608, 663–665, 681, 811, 1073, 1084, 1107, 1115, 1129–1131, 1134, 1136, 1155, 1162, 1167, 1170–1171, 1174–1176, 1180–1181, 1183–1184, 1208, 1212, 1230, 1235, 1238, 1247–1249, 1258–1259, 1303–1305, 1325–1327, 1330, 1357, 1359–1362, 1376–1377, 1381, 1387, 1389–1390, 1392, 1394–1395, 1398, 1403, 1405, 1409–1411, 1419 |
| 26 / MOVE_IRONHEAD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 26 / MOVE_IRONHEAD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 710, 833, 880–881, 885–886, 889, 895–896, 900, 904, 906, 909–911, 913, 991, 1269, 1271 |
| 27 / MOVE_AQUATAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 28 | 350, 1138–1139, 1175, 1179, 1215–1216, 1224, 1233, 1239, 1248, 1255, 1257, 1356–1357, 1361, 1370–1371, 1376, 1390, 1392–1395, 1403, 1412, 1419, 1421 |
| 27 / MOVE_AQUATAIL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 19 | 183, 872, 876, 878, 880–883, 885, 889, 892, 896, 905, 910–911, 913, 1047, 1262, 1269 |
| 28 / MOVE_PAINSPLIT | PROJECT_POLICY:LOCAL_POSITIVE | 14 | 1073, 1147, 1189, 1211, 1239, 1255, 1257, 1339–1340, 1384, 1415–1418 |
| 28 / MOVE_PAINSPLIT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 16 | 713–717, 837, 1144–1146, 1156, 1159, 1225, 1232–1233, 1382, 1404 |
| 28 / MOVE_PAINSPLIT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 838, 877, 893–895, 897, 902, 916–917, 1072, 1267, 1272 |
| 29 / MOVE_TAILWIND | PROJECT_POLICY:LOCAL_POSITIVE | 28 | 187–189, 225, 940, 1113–1115, 1137, 1165, 1221–1223, 1250, 1258–1259, 1321–1324, 1333–1334, 1355, 1367, 1378, 1390, 1403, 1421 |
| 29 / MOVE_TAILWIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 1157, 1217, 1379 |
| 29 / MOVE_TAILWIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 14 | 245, 870–871, 873–874, 881, 886, 901, 905, 907–908, 911, 1261, 1263 |
| 30 / MOVE_ENDEAVOR | PROJECT_POLICY:LOCAL_POSITIVE | 26 | 25, 1093–1099, 1102–1104, 1112, 1255, 1303–1305, 1333–1336, 1343, 1381, 1387, 1409–1411 |
| 30 / MOVE_ENDEAVOR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 21 | 172, 1087–1092, 1100, 1115, 1123–1124, 1154, 1168, 1176, 1184, 1203, 1208, 1229–1230, 1233, 1382 |
| 30 / MOVE_ENDEAVOR | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 737, 873, 878, 890, 892, 896, 912, 918, 991, 1047, 1101 |
| 31 / MOVE_ICYWIND | PROJECT_POLICY:LOCAL_POSITIVE | 43 | 248, 537, 920, 996, 1110, 1137, 1154, 1156, 1164–1165, 1167, 1173, 1175, 1188, 1210, 1215–1216, 1224–1227, 1239, 1244–1246, 1255, 1257, 1302, 1355–1357, 1368–1370, 1372, 1384, 1388, 1393–1395, 1400, 1404, 1421 |
| 31 / MOVE_ICYWIND | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 33 | 839, 872, 876–878, 880, 882–883, 892–896, 899, 902–904, 906–908, 910–911, 915–917, 1023–1024, 1262, 1265, 1267–1269, 1271 |
| 32 / MOVE_ZENHEADBUTT | PROJECT_POLICY:LOCAL_POSITIVE | 122 | 39–40, 88–89, 155–157, 306–307, 321, 323, 335–336, 339–340, 345, 364–366, 368–369, 379–380, 405, 440–445, 489, 542–543, 638–639, 647, 657, 680, 695, 755, 951, 1034–1035, 1073, 1077, 1107, 1117–1118, 1124, 1134, 1136, 1158–1159, 1162, 1167–1168, 1170–1171, 1174–1175, 1183–1184, 1188, 1190, 1203, 1208, 1210–1211, 1213–1216, 1220, 1224, 1229–1230, 1232, 1238, 1246, 1255, 1258–1259, 1297–1299, 1303–1305, 1325–1327, 1344–1345, 1347–1349, 1356–1357, 1359–1360, 1370–1371, 1376, 1380–1383, 1385, 1387, 1390, 1395, 1399, 1401–1406, 1409–1411, 1422 |
| 32 / MOVE_ZENHEADBUTT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 95, 208, 492, 837 |
| 32 / MOVE_ZENHEADBUTT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 26 | 737, 746, 838, 872, 875–876, 882–883, 893–894, 897, 899, 903, 905–908, 914, 916–917, 991, 1076, 1101, 1262, 1269, 1271 |
| 33 / MOVE_SEEDBOMB | PROJECT_POLICY:LOCAL_POSITIVE | 62 | 204–205, 352, 364–366, 379–380, 810, 951–952, 992, 1102–1104, 1111–1112, 1122, 1133–1134, 1154–1155, 1169, 1185, 1190, 1209–1212, 1226–1227, 1236–1237, 1294–1299, 1303–1305, 1312–1315, 1318–1320, 1339–1342, 1344–1345, 1348–1349, 1383, 1399, 1413–1414, 1422 |
| 33 / MOVE_SEEDBOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 317, 709–710 |
| 33 / MOVE_SEEDBOMB | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 8 | 751, 869, 890, 915, 1260, 1265, 1271–1272 |
| 34 / MOVE_LASERFOCUS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 37 | 19–20, 1020–1021, 1087–1092, 1138–1139, 1157, 1176, 1180–1181, 1187, 1217, 1221–1224, 1230, 1235, 1238, 1240, 1245–1246, 1248, 1250, 1256, 1384, 1403–1404, 1407–1408, 1413 |
| 34 / MOVE_LASERFOCUS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 35 | 737, 746, 751, 833, 873–875, 877, 881–884, 886, 888, 890–891, 893, 895, 897–898, 903–908, 912–914, 916–917, 1101, 1264, 1267, 1270 |
| 35 / MOVE_TRICK | PROJECT_POLICY:LOCAL_POSITIVE | 51 | 234, 242, 536–537, 608, 676, 761, 778–779, 919–920, 1018, 1073, 1117–1118, 1146–1154, 1159, 1168, 1190, 1203, 1210–1211, 1215–1216, 1221, 1224, 1226–1227, 1232, 1244–1245, 1251, 1296, 1329, 1347–1349, 1365–1366, 1382, 1398, 1404, 1420 |
| 35 / MOVE_TRICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 713–717, 848 |
| 35 / MOVE_TRICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 16 | 746, 875–877, 882–883, 893–894, 897, 902, 906–908, 916, 1072, 1267 |
| 36 / MOVE_DRILLRUN | PROJECT_POLICY:LOCAL_POSITIVE | 17 | 28, 91, 95, 208, 225, 556, 1135–1136, 1138–1139, 1214, 1241, 1355, 1370, 1409–1411 |
| 36 / MOVE_DRILLRUN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 2 | 873, 1269 |
| 37 / MOVE_MAGICCOAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 22 | 1118, 1156, 1159, 1215–1216, 1224–1225, 1232, 1236–1237, 1246, 1329, 1347–1349, 1370, 1382, 1384, 1386, 1404, 1408, 1420 |
| 37 / MOVE_MAGICCOAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 15 | 746, 875–876, 882–883, 893–894, 897, 902–903, 907–908, 912, 916–917 |
| 38 / MOVE_MAGICROOM | PROJECT_POLICY:LOCAL_POSITIVE | 8 | 1117–1118, 1150, 1168, 1190, 1210–1211, 1214 |
| 38 / MOVE_MAGICROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 1203, 1296, 1329, 1347–1349, 1377, 1382, 1384, 1404, 1420 |
| 38 / MOVE_MAGICROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 746, 875, 882–883, 893, 902, 907, 916, 1072 |
| 39 / MOVE_WONDERROOM | PROJECT_POLICY:LOCAL_POSITIVE | 18 | 1117–1118, 1146–1147, 1150, 1153, 1159, 1166, 1168, 1190, 1210–1211, 1214–1216, 1219, 1224, 1232 |
| 39 / MOVE_WONDERROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 1296, 1329, 1347–1349, 1377, 1382, 1384, 1404, 1420 |
| 39 / MOVE_WONDERROOM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 14 | 746, 875–877, 882–883, 893–894, 901, 908, 916, 918, 1101, 1267 |
| 40 / MOVE_LIQUIDATION | PROJECT_POLICY:LOCAL_POSITIVE | 88 | 54, 62, 79–80, 116–117, 131, 134, 139–140, 183, 186, 194–195, 199, 224, 230, 245, 285, 323–324, 343, 381, 446–447, 471, 475–476, 498, 554–555, 590, 657, 666–667, 764–766, 794–795, 798–800, 956–957, 963, 998, 1108–1110, 1125–1126, 1137–1139, 1144–1145, 1156, 1163, 1167, 1174–1175, 1208, 1215–1216, 1224–1225, 1239, 1241, 1255, 1257, 1300–1302, 1353–1354, 1356–1357, 1367–1371, 1376, 1404, 1407, 1411–1412 |
| 40 / MOVE_LIQUIDATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 341–342 |
| 40 / MOVE_LIQUIDATION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 872, 899, 910, 1262, 1268 |
| 41 / MOVE_GASTROACID | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 1108–1110, 1125–1126, 1133–1134, 1141, 1193, 1215–1216, 1224, 1306–1307, 1337–1338, 1376, 1383 |
| 42 / MOVE_FOULPLAY | PROJECT_POLICY:LOCAL_POSITIVE | 74 | 50–51, 79, 225, 312, 344, 347, 546, 720–735, 834, 1027–1028, 1119–1120, 1146–1147, 1151–1153, 1155, 1158, 1169, 1176, 1184, 1189, 1211–1212, 1215–1216, 1220, 1223–1224, 1233, 1236–1237, 1244–1245, 1296, 1321–1324, 1337–1338, 1341–1342, 1348–1355, 1399, 1415–1418 |
| 42 / MOVE_FOULPLAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 713–717 |
| 42 / MOVE_FOULPLAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 13 | 875–877, 882–883, 888–889, 894–895, 902–903, 1265, 1267 |
| 43 / MOVE_SUPERFANG | PROJECT_POLICY:LOCAL_POSITIVE | 23 | 488, 992, 996, 1105–1107, 1111–1112, 1126, 1169, 1303–1305, 1310–1315, 1337–1338, 1344–1345 |
| 43 / MOVE_SUPERFANG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 1154, 1174–1175, 1226–1227 |
| 43 / MOVE_SUPERFANG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 888, 895, 899, 904 |
| 44 / MOVE_OUTRAGE | PROJECT_POLICY:LOCAL_POSITIVE | 46 | 323–324, 365–366, 1133–1134, 1136, 1169, 1171–1172, 1174, 1176, 1178–1179, 1182, 1187–1188, 1210, 1234–1235, 1255, 1258–1259, 1297–1299, 1336, 1357, 1361, 1371–1372, 1378, 1383, 1390, 1393–1395, 1403, 1405–1407, 1409–1411, 1414, 1419 |
| 44 / MOVE_OUTRAGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 15, 837, 1079–1080, 1379 |
| 44 / MOVE_OUTRAGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 25 | 838, 869–872, 878, 880, 884, 889–890, 892, 896, 901, 905, 907–908, 911, 913, 915, 1101, 1260–1262, 1269, 1271 |
| 45 / MOVE_SKYATTACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 19 | 1113–1115, 1137, 1157, 1217, 1221–1223, 1246, 1321–1324, 1333–1334, 1355, 1367, 1421 |
| 45 / MOVE_SKYATTACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 84, 874, 881, 901 |
| 46 / MOVE_THROATCHOP | PROJECT_POLICY:LOCAL_POSITIVE | 52 | 27–28, 106, 128, 679, 1126, 1137–1139, 1141, 1152–1157, 1162–1163, 1184–1185, 1188, 1193, 1209–1210, 1212, 1214, 1217, 1222, 1225, 1227, 1239–1241, 1245, 1256–1257, 1296, 1307, 1309, 1312, 1330, 1353–1354, 1367, 1390, 1400–1401, 1403–1404, 1409, 1419, 1422 |
| 46 / MOVE_THROATCHOP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 1238, 1242, 1252, 1295, 1301–1302, 1311, 1389, 1394–1395, 1405, 1410–1411, 1413 |
| 46 / MOVE_THROATCHOP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 485, 873, 879, 887–888, 890, 902–903, 916–917, 1265–1266 |
| 47 / MOVE_STOMPINGTANTRUM | PROJECT_POLICY:LOCAL_POSITIVE | 118 | 149–150, 181, 231, 246–247, 323, 335, 339, 352, 365, 489–490, 546, 604–605, 657, 663, 675, 685, 687–688, 698, 720–735, 756, 780, 834, 956–957, 1104, 1112, 1125–1126, 1134, 1145, 1153–1154, 1156, 1158, 1166, 1169–1174, 1176, 1185, 1188–1189, 1209–1211, 1220, 1222, 1224–1225, 1227, 1233, 1238, 1248–1249, 1297–1299, 1304–1305, 1316–1317, 1325–1327, 1343–1345, 1353–1354, 1362, 1365–1366, 1368–1369, 1371, 1376, 1381–1383, 1385–1387, 1389, 1392, 1395, 1401, 1403, 1405, 1409–1413, 1419, 1422 |
| 47 / MOVE_STOMPINGTANTRUM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 837 |
| 47 / MOVE_STOMPINGTANTRUM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 17 | 838, 869, 885, 889, 892, 896, 900, 906, 909, 913, 915, 917, 1260, 1266, 1268, 1271–1272 |
| 48 / MOVE_EARTHPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 60 | 3, 60–62, 150, 186, 205–206, 234, 352, 513, 1104, 1126, 1131, 1135–1136, 1156, 1159, 1166, 1170–1172, 1174, 1187, 1225, 1232–1233, 1251, 1253, 1258–1259, 1299, 1304–1305, 1318–1320, 1325–1327, 1341–1343, 1347, 1353–1354, 1362, 1364, 1376, 1378–1379, 1381, 1383, 1386–1387, 1390, 1392, 1401, 1412–1413 |
| 48 / MOVE_EARTHPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 154, 508, 837, 1079–1080 |
| 48 / MOVE_EARTHPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 709, 838, 881, 885, 889, 892, 896, 900, 909, 911, 913, 918 |
| 49 / MOVE_GUNKSHOT | PROJECT_POLICY:LOCAL_POSITIVE | 63 | 92–94, 211, 306–307, 379–380, 487–488, 546, 606, 720–735, 834, 956–957, 992, 1105–1107, 1141, 1154–1155, 1182, 1193, 1212, 1216, 1224, 1226–1227, 1239–1240, 1256–1257, 1337–1338, 1346–1347, 1359–1360, 1363–1364, 1376, 1412–1413, 1419–1421 |
| 49 / MOVE_GUNKSHOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 710, 839, 902, 1265, 1271–1272 |
| 50 / MOVE_DUALCHOP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 17 | 1141, 1145, 1153–1154, 1176, 1179, 1184, 1193, 1208, 1252, 1311–1312, 1330, 1394–1395, 1404–1405 |
| 50 / MOVE_DUALCHOP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 7 | 746, 890–891, 913–914, 916, 1266 |
| 51 / MOVE_HEATWAVE | PROJECT_POLICY:LOCAL_POSITIVE | 33 | 110, 300, 405, 1105–1107, 1130–1131, 1142–1143, 1219, 1229–1230, 1234–1235, 1297–1299, 1321–1324, 1328–1330, 1355, 1385, 1390–1391, 1402–1403, 1405, 1421 |
| 51 / MOVE_HEATWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 51 / MOVE_HEATWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 11 | 737, 870–871, 874, 881, 888, 891, 900–901, 905, 1261 |
| 52 / MOVE_HYPERVOICE | PROJECT_POLICY:LOCAL_POSITIVE | 71 | 59, 206, 338, 352, 365–366, 442, 503, 532, 635–637, 763, 975, 982, 1104, 1111–1112, 1121–1122, 1128, 1141, 1154–1155, 1168, 1173, 1180–1181, 1185, 1193, 1203, 1209, 1212, 1221, 1223, 1226–1227, 1235, 1245–1246, 1297–1299, 1303–1305, 1313–1315, 1320–1324, 1331–1332, 1336, 1349, 1355, 1357, 1361, 1368–1369, 1378–1379, 1382, 1384, 1390, 1403–1404, 1413 |
| 52 / MOVE_HYPERVOICE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 9 | 347, 713–717, 837, 1079–1080 |
| 52 / MOVE_HYPERVOICE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 15 | 746, 838, 888, 893, 901, 905, 911–912, 916–917, 1101, 1265, 1269–1271 |
| 53 / MOVE_SUPERPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 26 | 62, 1084, 1104, 1112, 1126, 1134, 1137, 1144–1145, 1153, 1157, 1162, 1166, 1170–1171, 1183–1185, 1188, 1208–1210, 1217, 1222, 1229–1230 |
| 53 / MOVE_SUPERPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 29 | 308, 837, 1241–1242, 1248–1249, 1252, 1255, 1258–1259, 1312, 1357, 1367, 1375, 1381, 1385, 1387, 1389–1390, 1392, 1404–1405, 1408–1411, 1413, 1419, 1422 |
| 53 / MOVE_SUPERPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 737, 838, 879, 886, 889, 891–892, 896, 903, 1266, 1268, 1271 |
| 54 / MOVE_KNOCKOFF | PROJECT_POLICY:LOCAL_POSITIVE | 75 | 54–55, 89, 96–97, 150, 248, 345, 365–366, 368, 392–394, 443–445, 487–488, 554–555, 655, 760, 814, 939–941, 952, 956–957, 1046, 1102–1104, 1112, 1155, 1162, 1171, 1185, 1209, 1212, 1222, 1241, 1244–1245, 1248, 1250, 1296, 1302, 1306–1307, 1309, 1311–1312, 1337–1338, 1341–1343, 1350–1352, 1355, 1361, 1368–1369, 1381, 1387, 1390, 1399, 1403–1404, 1407, 1419, 1422 |
| 54 / MOVE_KNOCKOFF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 20 | 88, 1079–1080, 1088–1092, 1119–1120, 1142–1145, 1154, 1157, 1159, 1176, 1217, 1232 |
| 54 / MOVE_KNOCKOFF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 22 | 746, 869, 873, 875, 877, 879, 886–887, 891, 894–895, 902–903, 916–917, 1252, 1260, 1264–1268 |
| 55 / MOVE_PSYCHUP | PROJECT_POLICY:LOCAL_POSITIVE | 176 | 12, 37–38, 81–82, 163–164, 187–189, 375, 459, 466–467, 478–479, 484–486, 489–493, 495, 509–510, 515, 522, 531–537, 539–547, 558, 562–563, 570–571, 574, 580–581, 584, 614–616, 623–624, 627–632, 645–647, 658–662, 672–673, 682–683, 686–688, 691–693, 700–701, 709–710, 718–735, 757, 761–763, 774, 785–786, 790–795, 802–803, 806–808, 811, 815, 824, 827–829, 832, 834, 868, 919–920, 932, 947, 959–960, 981–982, 985, 988, 992, 995, 997, 1002–1005, 1008–1009, 1019, 1025–1026, 1029–1030, 1065, 1158, 1168, 1190, 1203, 1210–1211, 1215–1216, 1220, 1224, 1244–1245, 1329–1330, 1347, 1349, 1382, 1404, 1420 |
| 55 / MOVE_PSYCHUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 20 | 713–717, 1157, 1159, 1212, 1217, 1232, 1240, 1256, 1328, 1348, 1370, 1384, 1386, 1390, 1407–1408 |
| 55 / MOVE_PSYCHUP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 30 | 286–287, 370–372, 388–389, 875–877, 882–883, 885, 893–895, 897, 901–903, 906–911, 916, 1265, 1267, 1271 |
| 56 / MOVE_VACUUMWAVE | PROJECT_POLICY:LOCAL_POSITIVE | 18 | 54–55, 123, 212, 394, 448, 555–556, 983, 1110, 1240–1242, 1246, 1252, 1256, 1330, 1404 |
| 56 / MOVE_VACUUMWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 1015 |
| 56 / MOVE_VACUUMWAVE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 887, 891, 897, 914, 916, 1266 |
| 57 / MOVE_LASTRESORT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 23 | 1073, 1124, 1154–1155, 1157, 1160, 1168, 1178–1179, 1212, 1217, 1226–1227, 1300–1302, 1316–1317, 1349, 1381–1382, 1387, 1413 |
| 57 / MOVE_LASTRESORT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 13 | 746, 891, 895, 907–908, 912, 917–918, 991, 1072, 1265, 1270–1271 |
| 58 / MOVE_CONFIDE | PROJECT_POLICY:LOCAL_POSITIVE | 890 | 1–9, 12, 15–128, 130–131, 133–200, 203–234, 236–251, 277–289, 292, 294–359, 361–397, 399–411, 440–453, 455–464, 466–467, 469–602, 604–654, 656–702, 709–710, 718–735, 747–750, 752–771, 774–830, 832, 834, 848, 868, 919–920, 932, 939–990, 992–1005, 1008–1015, 1017–1035, 1037, 1039–1046, 1048–1065, 1074–1075, 1077–1078, 1082, 1087, 1093–1099, 1158, 1219–1220, 1238, 1241–1242, 1246–1253, 1375, 1377–1380 |
| 58 / MOVE_CONFIDE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 259 | 713–717, 837, 1073, 1079–1080, 1083–1084, 1088–1092, 1100, 1102–1115, 1117–1131, 1133–1157, 1159–1160, 1162–1190, 1193, 1203, 1208–1217, 1221–1227, 1229–1230, 1232–1237, 1239–1240, 1244–1245, 1255–1259, 1294–1357, 1359–1372, 1376, 1381–1422 |
| 59 / MOVE_GRASSPLEDGE | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 151, 1294–1296 |
| 59 / MOVE_GRASSPLEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 869, 890, 1260, 1274 |
| 60 / MOVE_FIREPLEDGE | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 151, 1297–1299 |
| 60 / MOVE_FIREPLEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 990, 1048–1064 |
| 60 / MOVE_FIREPLEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 870–871, 891, 1261, 1275 |
| 61 / MOVE_WATERPLEDGE | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 151, 1300–1302 |
| 61 / MOVE_WATERPLEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 990, 1048–1064 |
| 61 / MOVE_WATERPLEDGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 839, 872, 892, 1262, 1276 |
| 62 / MOVE_FRENZYPLANT | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 151, 1250, 1296 |
| 62 / MOVE_FRENZYPLANT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 869, 890, 1260, 1274 |
| 63 / MOVE_BLASTBURN | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 151, 1238, 1299 |
| 63 / MOVE_BLASTBURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 546, 720–735, 834 |
| 63 / MOVE_BLASTBURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 870–871, 891, 1261, 1275 |
| 64 / MOVE_HYDROCANNON | PROJECT_POLICY:LOCAL_POSITIVE | 3 | 151, 1241, 1302 |
| 64 / MOVE_HYDROCANNON | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 18 | 546, 720–735, 834 |
| 64 / MOVE_HYDROCANNON | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 839, 872, 892, 1262, 1276 |
| 65 / MOVE_FOCUSENERGY | PROJECT_POLICY:LOCAL_POSITIVE | 115 | 29–34, 66–68, 83, 104–107, 115–117, 123, 126–127, 133–136, 151, 196–197, 212, 223–224, 230, 236–237, 240, 246–248, 280–282, 330–334, 395–397, 478–479, 487–488, 501, 520, 523–524, 547, 572–574, 585–587, 591–592, 604–608, 663–665, 672–673, 679, 686–688, 783, 808, 830, 983, 1011, 1039, 1082, 1102–1107, 1110, 1113–1115, 1128, 1133, 1138–1139, 1153–1154, 1157, 1162, 1180–1181, 1183–1184, 1187, 1208, 1217, 1222, 1229–1230, 1252 |
| 65 / MOVE_FOCUSENERGY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 66 | 15, 19–22, 56–57, 130, 161–162, 168, 216–217, 231–232, 304–305, 335–336, 339–340, 365–366, 443–445, 451, 455, 461–464, 500, 528, 554–558, 1020–1021, 1240–1241, 1253, 1256, 1300–1302, 1356–1357, 1367, 1370, 1375, 1381, 1387, 1389–1390, 1392–1395, 1403–1404, 1413, 1419, 1422 |
| 66 / MOVE_COSMICPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 26 | 35–36, 120–121, 151, 177–178, 318–319, 348–349, 399–400, 406, 409, 480–481, 614, 629, 658–659, 1007–1009, 1017, 1182 |
| 66 / MOVE_COSMICPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 36 | 315–316, 385, 410–411, 486, 541, 546, 720–735, 834, 1014, 1040–1042, 1065, 1079–1080, 1346–1349 |
| 67 / MOVE_BATONPASS | PROJECT_POLICY:LOCAL_POSITIVE | 172 | 12, 35–36, 39–40, 48–49, 78, 83, 85, 97, 122–123, 133–136, 145, 151, 161–162, 167–168, 175–178, 182, 187–190, 196–197, 203, 206–207, 212, 225, 251, 280–282, 302, 311–312, 348–349, 353–357, 376, 380, 386–387, 407–409, 455, 471–472, 477–481, 492, 506–507, 514, 521, 523–525, 533–535, 542–543, 545, 547, 562–563, 580–581, 593–595, 598, 638–640, 647, 669–670, 672–673, 685, 701, 719, 777–779, 794–795, 808–809, 827, 939–941, 958–960, 983, 988, 1018, 1043–1045, 1073, 1105–1110, 1118–1120, 1124, 1146–1150, 1155, 1158, 1177–1179, 1190, 1203, 1210–1211, 1214, 1220, 1250, 1252, 1300–1302, 1310–1317, 1337–1338, 1348–1349, 1372, 1377–1379, 1382, 1420 |
| 67 / MOVE_BATONPASS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 15 | 15, 21–22, 165–166, 304–305, 308, 315–316, 374–375, 557–558, 848 |
| 68 / MOVE_ENCORE | PROJECT_POLICY:LOCAL_POSITIVE | 194 | 25–26, 35–40, 54–57, 60–71, 86–87, 93–94, 96–97, 122, 124, 143, 149, 151, 172–176, 183–184, 186–189, 191–192, 194–195, 202, 213, 231–232, 238, 296–297, 322, 341–345, 350–354, 360, 364–368, 377–378, 386–387, 392–394, 409, 443–445, 470, 480–481, 492, 499, 506–507, 510, 521, 528, 533–535, 547, 554–556, 562–563, 584, 599–602, 607–608, 623–626, 630–632, 640–642, 666–667, 669–670, 761–763, 790–791, 806–807, 809, 827, 945–947, 975, 981–982, 994, 1018, 1022, 1025–1026, 1073, 1077, 1093–1099, 1140–1141, 1158, 1168, 1185, 1190, 1193, 1209–1211, 1220, 1229–1230, 1241–1242, 1297–1302, 1310–1315, 1320, 1337–1338, 1350–1352, 1356–1357, 1375, 1382, 1388, 1404, 1422 |
| 68 / MOVE_ENCORE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 165–166, 190, 308, 477, 494, 1087–1092, 1100 |
| 69 / MOVE_SCREECH | PROJECT_POLICY:LOCAL_POSITIVE | 162 | 39–40, 42, 50–55, 72–73, 81–82, 90–91, 95, 104–105, 108–110, 125–126, 140–141, 143, 151, 163–164, 169–171, 174, 186, 197, 206, 208, 215, 222–224, 239–240, 246–248, 277–279, 300, 302, 330–331, 333–334, 370–372, 382–384, 390–391, 469, 487–488, 499–501, 504–507, 514–516, 519, 562–563, 588–590, 596–598, 609, 622, 641–642, 648–649, 652–654, 658–659, 677–678, 685–688, 702, 747–750, 787–789, 796–797, 822–823, 953–955, 984–985, 988, 995, 999–1002, 1015, 1027–1030, 1039, 1102–1104, 1115, 1119–1120, 1135–1136, 1141, 1154–1156, 1158, 1162, 1170–1171, 1176, 1182, 1186, 1193, 1212, 1219–1220, 1222, 1225–1227, 1233, 1378–1380 |
| 69 / MOVE_SCREECH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 85 | 15, 19–20, 23–24, 46–49, 56–57, 88–89, 100–101, 158–160, 165–168, 179–181, 190, 193, 198, 200, 207, 317, 374, 377–379, 455, 461–464, 477, 482–483, 522, 525, 554–558, 575–576, 593–595, 948–950, 996, 1020–1021, 1031–1035, 1236–1237, 1240–1241, 1256, 1308–1309, 1341–1342, 1359–1360, 1375, 1382, 1384, 1386, 1390–1392, 1405 |
| 70 / MOVE_FAKETEARS | PROJECT_POLICY:LOCAL_POSITIVE | 145 | 25–26, 35–36, 38–40, 52–53, 124, 133–136, 151, 158–160, 173–174, 183–185, 196–197, 200, 209–210, 215–217, 238, 306–307, 346–347, 350, 353–355, 370–372, 387, 409, 443–445, 456–458, 470, 480–482, 491, 514, 523–524, 531, 543, 562–563, 580–581, 599–600, 612–613, 615–616, 623–629, 638–639, 682–683, 701, 785–786, 790–795, 808, 827, 832, 959–960, 975, 1022, 1026, 1029–1030, 1093–1099, 1113–1115, 1119–1120, 1151–1155, 1158–1159, 1169, 1212, 1226–1227, 1232, 1244–1245, 1253, 1294–1296, 1313–1315, 1321–1324, 1335–1336, 1350–1352, 1382, 1384 |
| 70 / MOVE_FAKETEARS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 190, 315–316, 386, 477, 484–485, 1087–1092, 1413 |
| 71 / MOVE_SCARYFACE | PROJECT_POLICY:LOCAL_POSITIVE | 366 | 4–6, 23–24, 56–59, 66–68, 88–89, 91–95, 97, 101, 111–112, 123, 128, 130, 136, 142, 149–151, 158–160, 167–168, 197–198, 200, 206, 208–212, 215, 217, 220–221, 228–229, 232, 234, 246–248, 286–287, 312, 324, 330–331, 336, 338–340, 344–345, 347, 365–366, 377–379, 384, 395–397, 399–400, 404–406, 442, 445, 448, 456–458, 461–464, 469, 472, 482–483, 487–488, 495–498, 501, 504–507, 513–514, 517, 525–526, 531, 536–538, 540–541, 544, 546, 556, 585–587, 591–592, 604–606, 612–613, 616, 619–620, 623–624, 641–642, 644, 656–657, 663–665, 667–668, 674, 677–683, 686–688, 691–692, 694–695, 698–699, 718, 720–735, 752–756, 760, 783, 795, 798–799, 801, 804–805, 818–819, 821, 823, 828–830, 834, 919–920, 942–944, 951–952, 957, 961–962, 965, 967, 971, 974–975, 982–983, 986–987, 989–990, 996, 999–1001, 1004, 1008–1009, 1017, 1027–1028, 1034–1035, 1046, 1048–1064, 1078, 1082, 1103–1104, 1113–1115, 1125–1126, 1133, 1135–1136, 1139, 1141, 1145, 1151–1154, 1159, 1169, 1171, 1176, 1180–1185, 1188–1190, 1193, 1208–1211, 1216, 1221–1224, 1226–1227, 1234–1235, 1237, 1239, 1241, 1245–1246, 1248–1253, 1255, 1257–1259, 1299, 1307, 1309, 1317, 1321–1324, 1334–1336, 1338–1343, 1345, 1355, 1359–1360, 1365–1366, 1371, 1375, 1378–1383, 1387, 1389–1390, 1392, 1394–1395, 1399–1403, 1405–1411, 1413, 1419, 1422 |
| 71 / MOVE_SCARYFACE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 20–22, 374, 1021, 1079–1080 |
| 72 / MOVE_VENOMDRENCH | PROJECT_POLICY:LOCAL_POSITIVE | 47 | 29–34, 41–42, 73, 109–110, 151, 169, 211, 460, 487–488, 505–507, 580–581, 588–590, 596–598, 621–622, 670, 798–799, 816–817, 964–965, 974–975, 988, 1010, 1074–1075, 1163, 1182, 1219, 1224 |
| 72 / MOVE_VENOMDRENCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 23 | 24, 48–49, 89, 168, 294, 367–368, 379, 1035, 1239, 1257, 1337–1338, 1359–1360, 1363–1364, 1376, 1391, 1419–1421 |
| 73 / MOVE_SPIKES | PROJECT_POLICY:LOCAL_POSITIVE | 85 | 28, 90–91, 138–139, 151, 185, 194–195, 204–205, 211, 214, 225, 227, 324, 344–347, 363, 405, 410, 459–460, 469, 476, 491, 498, 525, 531, 596–598, 609–611, 621–622, 650–651, 669–670, 758–760, 764–768, 811, 815, 827, 984–985, 1018, 1024, 1040–1042, 1073, 1075, 1129–1131, 1163, 1239, 1257, 1296, 1306–1307, 1339–1342, 1362–1364, 1376, 1386, 1392, 1401, 1412, 1422 |
| 74 / MOVE_TOXICSPIKES | PROJECT_POLICY:LOCAL_POSITIVE | 84 | 23–24, 29–34, 48–49, 72–73, 89–91, 93–94, 109–110, 138–139, 151, 167–168, 195, 204–205, 211, 344–345, 363, 367–368, 460, 469, 487–488, 504–505, 596–598, 615–616, 621–622, 669–670, 764–766, 798–799, 964–965, 974–975, 1010, 1074–1075, 1141, 1159, 1163, 1182, 1193, 1219, 1224, 1232, 1239–1240, 1256–1257, 1296, 1306–1307, 1341–1342, 1359–1360, 1363–1364, 1376, 1391, 1412 |
| 74 / MOVE_TOXICSPIKES | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 15, 410, 1040–1042 |
| 75 / MOVE_DRAGONDANCE | PROJECT_POLICY:LOCAL_POSITIVE | 85 | 4–6, 95, 116–117, 130–131, 142, 147–149, 151, 158–160, 208, 230, 246–248, 279, 323–324, 326–327, 329, 334, 359, 369, 395–397, 406–408, 546, 612–613, 663–665, 688, 696–697, 699, 720–735, 752–753, 804–805, 823, 834, 975, 997, 999–1001, 1017, 1075, 1133, 1178–1179, 1182, 1187, 1372, 1392, 1395, 1403, 1407 |
| 75 / MOVE_DRAGONDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 837, 1079–1080 |
| 75 / MOVE_DRAGONDANCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 1 | 838 |
| 76 / MOVE_AGILITY | PROJECT_POLICY:LOCAL_POSITIVE | 312 | 25–26, 28, 37–38, 41–42, 48–53, 58–59, 77–78, 83–85, 98–101, 107, 116–119, 121, 123, 135, 137, 142, 144–151, 160, 162–164, 167–171, 179–181, 190, 203, 206–207, 211–212, 215, 225–227, 230, 233–234, 237, 243–245, 277–282, 302–303, 309–312, 325, 330–331, 337–338, 353–354, 358–359, 380, 399–400, 407–408, 410, 443–451, 458, 469–472, 477, 480–481, 500–501, 504–505, 509–511, 514, 525, 527–528, 546, 572–576, 595–598, 619–620, 623–624, 638–640, 642, 648–649, 658–659, 670, 672–673, 680–681, 685, 694–695, 720–735, 754–755, 761–763, 767–771, 802–803, 809–810, 822–823, 834, 955, 958, 962, 974–975, 994, 996, 1002, 1008–1009, 1012, 1018–1019, 1022, 1024–1030, 1040–1045, 1073, 1078, 1093–1099, 1105–1107, 1110, 1113–1115, 1118–1120, 1123–1124, 1128, 1137–1139, 1150, 1162, 1167, 1169, 1178–1182, 1186, 1189–1190, 1210–1211, 1213–1214, 1221–1223, 1234–1237, 1239–1240, 1244–1246, 1251–1252, 1255–1259, 1294–1296, 1302, 1308–1317, 1333–1334, 1348–1349, 1353–1354, 1356–1357, 1361, 1367, 1370, 1377–1379, 1388, 1391, 1404–1408, 1421 |
| 76 / MOVE_AGILITY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 25 | 15–18, 21–22, 46–47, 165–166, 193, 304–305, 375, 386, 494, 522, 593–594, 1087–1092 |
| 77 / MOVE_NASTYPLOT | PROJECT_POLICY:LOCAL_POSITIVE | 186 | 25–26, 37–42, 52–55, 65, 80, 92–94, 96–97, 122, 124, 150–151, 163–164, 169, 172, 175–176, 190, 198–200, 203, 215, 228–229, 238, 251, 286–287, 298–300, 319, 322, 327, 344–345, 348, 352–354, 377–378, 410, 443–445, 477, 482–483, 487–488, 492, 495, 500–501, 506–507, 514, 521, 527, 532–535, 544, 562–563, 580–581, 615–616, 623–624, 627–629, 658–659, 682–683, 686–688, 694–695, 698, 754–756, 763, 785–786, 790–791, 794–795, 819, 828–829, 832, 939–944, 974–975, 982, 1022, 1025–1026, 1029–1030, 1040–1042, 1074–1075, 1093–1099, 1113–1115, 1119–1120, 1146–1147, 1151–1153, 1155, 1158–1159, 1169, 1185, 1189, 1209, 1211–1212, 1216, 1220, 1223–1224, 1232, 1240, 1244–1245, 1250, 1256, 1294–1296, 1337–1338, 1355, 1372, 1377, 1396–1398, 1402, 1415–1418, 1420–1421 |
| 77 / MOVE_NASTYPLOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 28 | 315–317, 484–485, 494, 557–558, 564–569, 633–634, 713–717, 1087–1092, 1100 |
| 78 / MOVE_GRASSYTERRAIN | PROJECT_POLICY:LOCAL_POSITIVE | 133 | 1–3, 43–45, 71, 102–103, 114, 151–154, 182, 187–189, 191–192, 251, 277–279, 298–300, 306–307, 344–345, 369, 389, 440–442, 460, 473–474, 518, 545–546, 548–550, 593–595, 599–600, 602, 609, 638–639, 643–644, 719–735, 758–760, 777–781, 834, 848, 939–941, 970–971, 978–981, 1004, 1037, 1102–1104, 1121–1122, 1133–1134, 1185, 1190, 1209–1211, 1236–1237, 1242, 1250, 1258–1259, 1294–1296, 1318–1320, 1339–1342, 1344–1345, 1383, 1399, 1408, 1414–1418, 1422 |
| 78 / MOVE_GRASSYTERRAIN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 46–47 |
| 79 / MOVE_MISTYTERRAIN | PROJECT_POLICY:LOCAL_POSITIVE | 81 | 35–36, 39–40, 122, 151, 173–174, 183–184, 355, 392–394, 492, 528, 546, 584, 599–600, 647, 720–735, 777–779, 786, 790–791, 808, 810–811, 815, 824, 830, 834, 848, 945–947, 995, 1005, 1018, 1026, 1073, 1148–1153, 1158, 1160, 1180, 1214, 1219–1220, 1258–1259, 1300–1302, 1316–1317, 1382, 1384, 1404 |
| 80 / MOVE_ELECTRICTERRAIN | PROJECT_POLICY:LOCAL_POSITIVE | 91 | 25–26, 81–82, 100–101, 113, 135, 145, 151, 172, 179–181, 242–243, 338, 456–458, 470, 515, 519, 532, 546, 654, 656–657, 671, 695, 720–735, 755, 802–803, 810, 834, 994, 1002, 1013, 1022, 1032–1033, 1078, 1084, 1093–1099, 1128, 1141, 1163, 1169, 1186, 1193, 1236–1237, 1310–1312, 1331–1334, 1386–1392, 1404, 1406, 1408 |
| 80 / MOVE_ELECTRICTERRAIN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 12 | 713–717, 1087–1092, 1100 |
| 81 / MOVE_PSYCHICTERRAIN | PROJECT_POLICY:LOCAL_POSITIVE | 95 | 63–65, 79–80, 96–97, 122, 124, 150–151, 196, 199, 203, 251, 318–319, 348–349, 351–352, 356–357, 392–394, 489–490, 492, 528, 541, 546, 571, 627–632, 659, 720–735, 761–763, 786, 828–829, 832, 834, 982, 996, 1003, 1022, 1117–1118, 1148–1150, 1158, 1168, 1190, 1203, 1210–1211, 1214–1216, 1220, 1224, 1246, 1329, 1347–1349, 1370, 1377, 1382, 1404, 1408, 1420 |
| 82 / MOVE_WHIRLPOOL | PROJECT_POLICY:LOCAL_POSITIVE | 185 | 7–9, 31, 34, 54–55, 60–62, 72–73, 79–80, 86–87, 90–91, 98–99, 108, 112, 115–121, 128, 130–131, 134, 138–141, 143, 147–149, 151, 158–162, 170–171, 183–184, 186, 194–195, 199, 211, 215, 222–224, 226, 230, 241, 245, 248–249, 283–285, 288–289, 295–297, 310, 313–314, 323–331, 335–336, 341–343, 350, 372–375, 381, 384, 404, 406–408, 446–448, 453, 462, 471–472, 475–476, 498–499, 509–511, 514, 516–517, 537, 542–543, 546, 617–618, 645–647, 720–735, 797, 834, 920, 945–947, 963, 998, 1005, 1108–1110, 1125–1126, 1137–1139, 1145, 1154, 1156, 1167, 1174–1175, 1208, 1215–1216, 1224–1227, 1255, 1300–1302, 1353–1354, 1357, 1372, 1388, 1407, 1411 |
| 82 / MOVE_WHIRLPOOL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 7 | 1239, 1257, 1356, 1370–1371, 1376, 1412 |
| 83 / MOVE_FIRESPIN | PROJECT_POLICY:LOCAL_POSITIVE | 94 | 4–6, 37–38, 58–59, 77–78, 126, 136, 146–149, 151, 155–157, 218–219, 228–229, 240, 244, 250, 280–282, 321, 334, 339–340, 349, 359, 395–397, 443–445, 488, 520, 538, 547, 607–608, 660–662, 684, 688–690, 761–763, 770–771, 775–776, 830, 942–944, 993, 1008, 1039, 1077, 1105–1107, 1130–1131, 1142–1143, 1172, 1182, 1229–1230, 1234–1235, 1238, 1297–1299, 1328–1330, 1391, 1402–1403, 1405, 1410 |
| 83 / MOVE_FIRESPIN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 566–567 |
| 84 / MOVE_SANDTOMB | PROJECT_POLICY:LOCAL_POSITIVE | 88 | 27–28, 31, 34, 50–51, 95, 151, 185, 204–205, 207–208, 212–213, 220–221, 227, 231–232, 246–248, 284–285, 318–320, 324, 332–334, 348–349, 383–384, 401, 403, 405, 440–442, 476, 491, 496–498, 502–503, 505, 525–526, 529, 577–579, 582–583, 604–606, 610–611, 698, 756, 768, 811, 827, 966–967, 986–987, 1027–1028, 1126, 1129–1131, 1135–1136, 1159, 1166, 1362–1364, 1386, 1392, 1401 |
| 85 / MOVE_PINMISSILE | PROJECT_POLICY:LOCAL_POSITIVE | 35 | 28, 91, 135, 139, 151, 211, 214, 288–289, 363, 459–460, 469, 504–505, 596–598, 609, 648–651, 964–965, 985, 994, 1024, 1074–1075, 1154, 1156, 1163, 1226–1227 |
| 85 / MOVE_PINMISSILE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 15 | 15, 167–168, 204–205, 207, 344–345, 525, 758–760, 1239, 1257, 1392 |
| 86 / MOVE_ICICLESPEAR | PROJECT_POLICY:LOCAL_POSITIVE | 54 | 86–87, 90–91, 124, 144, 151, 215, 220–222, 225, 342–343, 346–347, 402, 512–514, 524, 526, 531, 635–637, 666–668, 699, 752–753, 807, 820–821, 1024, 1110, 1156, 1158, 1164–1165, 1167, 1173, 1175, 1188, 1210, 1220, 1225, 1249, 1368–1369, 1393–1395 |
| 87 / MOVE_TAILSLAP | PROJECT_POLICY:LOCAL_POSITIVE | 21 | 37–38, 151, 288–289, 487–488, 625–626, 786, 832, 962, 1025–1026, 1082, 1111–1112, 1119–1120, 1180–1181 |
| 87 / MOVE_TAILSLAP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 161–162, 190, 315–316, 453, 471–472, 477, 1421 |
| 88 / MOVE_ROCKBLAST | PROJECT_POLICY:LOCAL_POSITIVE | 118 | 31, 34, 50–51, 68, 74–76, 90–91, 95, 111–112, 138–142, 151, 185, 204–205, 208, 213–214, 219, 222–224, 226, 246–248, 320, 348–349, 381, 383–384, 388–391, 401, 405, 442, 463–464, 476, 489–491, 517, 526, 529, 538, 577–579, 583, 587, 610–611, 617–622, 626, 692, 796–797, 804–807, 811, 949–950, 962, 1017, 1027–1028, 1031–1033, 1046, 1077, 1082, 1126, 1129–1131, 1135–1136, 1156, 1159, 1166, 1170–1175, 1216, 1225, 1234–1235, 1249, 1252, 1327, 1343, 1355, 1362–1364, 1392 |
| 88 / MOVE_ROCKBLAST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 105, 1079–1080 |
| 89 / MOVE_THUNDERFANG | PROJECT_POLICY:LOCAL_POSITIVE | 118 | 24, 58–59, 111–112, 135, 142, 151, 208–210, 228–229, 232, 243, 248, 286–287, 337–338, 355, 372, 379, 395–397, 456–458, 470, 496–498, 502–503, 505, 517, 525, 559–561, 604–606, 656–657, 674, 685–688, 697, 775–776, 804–805, 830, 951–952, 961–962, 990, 1046, 1048–1064, 1082, 1112, 1120, 1127–1128, 1136, 1141, 1143, 1169, 1172–1173, 1180–1181, 1187, 1193, 1234–1235, 1297–1299, 1310–1312, 1316–1317, 1335–1336, 1361, 1365–1366, 1381–1382, 1387, 1392, 1395, 1403, 1405, 1419 |
| 89 / MOVE_THUNDERFANG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 19–20 |
| 90 / MOVE_ICEFANG | PROJECT_POLICY:LOCAL_POSITIVE | 113 | 24, 111–112, 130, 142, 151, 158–160, 208–210, 221, 232, 245, 248, 286–287, 330–331, 337–338, 343, 346–347, 355, 372, 379, 456–458, 471–472, 502–503, 505, 517, 524–526, 531, 559–561, 666–667, 686–688, 804–805, 820–821, 951–952, 990, 996, 1048–1064, 1112, 1120, 1125–1126, 1138–1139, 1169, 1173–1175, 1180–1181, 1187, 1216, 1229–1230, 1233, 1249, 1255, 1316–1317, 1335–1336, 1365–1366, 1368–1371, 1381–1382, 1387, 1392–1395, 1400, 1405, 1419 |
| 90 / MOVE_ICEFANG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 19–20, 374, 453 |
| 91 / MOVE_FIREFANG | PROJECT_POLICY:LOCAL_POSITIVE | 130 | 4–6, 24, 58–59, 111–112, 136, 142, 151, 155–157, 208–210, 228–229, 232, 244, 248, 286–287, 337–338, 355, 372, 379, 395–397, 405, 456–458, 496–498, 502–503, 505, 517, 525, 538, 559–561, 604–608, 674, 686–688, 696, 775–776, 804–805, 830, 942–944, 951–952, 961–962, 974–975, 990, 1046, 1048–1064, 1082, 1105–1107, 1112, 1120, 1127–1128, 1136, 1143, 1169, 1172, 1180–1181, 1187, 1229–1230, 1234–1235, 1238, 1297–1299, 1316–1317, 1335–1336, 1345, 1361, 1365–1366, 1381–1382, 1390, 1392, 1403, 1405, 1407, 1419 |
| 91 / MOVE_FIREFANG | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 19–20 |
| 92 / MOVE_BODYSLAM | PROJECT_POLICY:LOCAL_POSITIVE | 309 | 91, 118–119, 310, 324, 440–442, 445, 448, 458, 463–464, 472, 475–476, 478–479, 487–491, 495–499, 501–503, 512–513, 515, 536–541, 546, 551–553, 556, 584, 591, 604–606, 608, 617–618, 622, 624, 629, 638–639, 643–644, 647, 656–657, 665–670, 674, 676, 679–681, 684, 686–690, 694–695, 698, 718, 720–735, 754–756, 758–760, 768, 775–776, 780–783, 801, 804–807, 809, 811–814, 820–821, 823–827, 830, 834, 919–920, 942–944, 952, 956–957, 961–962, 965–967, 975, 977, 982–983, 987, 992–993, 1010–1011, 1014, 1016, 1018, 1023–1035, 1046, 1073, 1076, 1082, 1084, 1093–1099, 1102–1104, 1111–1112, 1115, 1124–1126, 1129–1131, 1134–1136, 1144–1145, 1153–1158, 1162–1163, 1166–1168, 1170–1176, 1179–1189, 1203, 1208–1217, 1220, 1224–1227, 1230, 1234–1235, 1241, 1245–1249, 1258–1259, 1297–1299, 1303–1307, 1316–1317, 1325–1327, 1335–1336, 1343, 1349, 1356–1357, 1359–1362, 1368–1371, 1376, 1381–1383, 1385–1390, 1392–1395, 1399, 1401, 1403, 1405–1407, 1409–1414, 1419 |
| 92 / MOVE_BODYSLAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 485, 837, 1020–1021, 1087–1092, 1100 |
| 92 / MOVE_BODYSLAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 50 | 869–872, 875–880, 882–885, 887–898, 900–911, 916, 1260–1262, 1264–1271 |
| 93 / MOVE_BODYPRESS | PROJECT_POLICY:LOCAL_POSITIVE | 175 | 9, 31, 34, 39–40, 80, 95, 97, 108, 112, 131, 143, 149, 151, 185, 195, 205, 208, 226–227, 232, 241, 248, 285, 313–314, 319–321, 335–336, 339–340, 343, 352, 366, 368–369, 381–384, 400–401, 403, 405, 442, 490, 502–503, 513, 515–517, 526, 529, 536–539, 546, 577–579, 608, 611, 616, 622, 651, 657, 666–667, 676, 696–697, 699, 720–735, 752–753, 760, 809, 811, 814, 821, 827, 830, 834, 919–920, 957, 967, 977, 993, 998, 1001, 1016, 1076, 1084, 1104, 1112, 1115, 1117–1118, 1124, 1126, 1130–1131, 1134, 1136, 1153–1154, 1159, 1162, 1166, 1170–1171, 1176, 1181, 1184, 1188, 1190, 1208, 1210, 1216, 1227, 1230, 1248–1249, 1253, 1304–1305, 1312, 1317, 1326–1327, 1362, 1366, 1368–1369, 1371, 1376, 1378, 1381, 1383, 1385–1387, 1389, 1392, 1395, 1399, 1401, 1403, 1405, 1409–1413, 1419 |
| 93 / MOVE_BODYPRESS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 1379 |
| 94 / MOVE_HEATCRASH | PROJECT_POLICY:LOCAL_POSITIVE | 36 | 6, 59, 112, 143, 151, 219, 282, 321, 339–340, 405, 517, 538–539, 551–553, 676, 696, 830, 944, 993, 1008, 1016, 1076, 1129–1131, 1142–1143, 1166, 1171, 1235, 1299, 1385, 1405 |
| 95 / MOVE_HEAVYSLAM | PROJECT_POLICY:LOCAL_POSITIVE | 137 | 66–68, 76, 81–82, 95, 112, 143, 151, 205, 208, 231–232, 241, 248, 313–314, 320–321, 335–336, 339–340, 343, 366, 382–384, 401–405, 440–442, 463–464, 489–490, 503, 515, 517, 526, 529, 536–539, 546, 551–553, 577–579, 611, 651, 657, 666–667, 675–676, 720–735, 811, 821, 830, 834, 919–920, 966–967, 993, 998, 1008, 1014, 1016, 1018, 1033, 1073, 1076, 1084, 1115, 1130–1131, 1133–1134, 1155, 1166, 1170–1171, 1176, 1181, 1188, 1210, 1247–1249, 1253, 1325–1327, 1352, 1360, 1362, 1368–1369, 1371, 1376, 1378, 1381, 1385–1387, 1389, 1392, 1398, 1401, 1405–1406, 1413 |
| 95 / MOVE_HEAVYSLAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 1379 |
| 96 / MOVE_REVERSAL | PROJECT_POLICY:LOCAL_POSITIVE | 210 | 25–26, 50–51, 56–59, 62, 66–68, 106, 111–112, 115, 123, 127–128, 150–151, 155–157, 161–162, 172, 193, 204–205, 211–215, 225, 228–229, 241, 280–282, 307, 335–336, 356–357, 365–366, 379–380, 382–384, 444–445, 469, 481, 500–501, 506–507, 514, 517, 522, 528, 547, 559–561, 585–587, 591–592, 608, 642, 663–665, 667, 670, 672–673, 678–679, 681, 691–694, 700–701, 754, 757, 760, 783, 787–789, 795, 809, 826, 944, 951–952, 956–958, 977, 983, 990, 992, 994, 999–1001, 1011, 1019, 1022, 1027–1028, 1043–1046, 1048–1064, 1078, 1082, 1093–1099, 1105–1107, 1113–1115, 1123–1124, 1137, 1144–1145, 1154, 1162–1163, 1167, 1180–1181, 1183–1184, 1187, 1208, 1222, 1230, 1234–1235, 1238–1240, 1246, 1250, 1252, 1256–1257, 1302, 1307, 1309, 1321–1324, 1335–1336, 1343, 1357, 1367, 1375, 1380–1381, 1385, 1389, 1404–1405, 1408–1411, 1419, 1422 |
| 96 / MOVE_REVERSAL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 15 | 19–20, 304–305, 837, 1020–1021, 1087–1092, 1100, 1255 |
| 97 / MOVE_ELECTROBALL | PROJECT_POLICY:LOCAL_POSITIVE | 85 | 25–26, 81–82, 100–101, 125, 135, 145, 150–151, 170–172, 179–181, 239, 337–338, 353–354, 456–458, 470, 515, 519, 532, 640, 648–649, 656–657, 695, 697, 755, 802–803, 810, 954–955, 994, 1002, 1013, 1018, 1022, 1073, 1078, 1093–1099, 1105–1107, 1123–1124, 1127–1128, 1141, 1163, 1169, 1172–1173, 1186, 1193, 1236–1237, 1310–1312, 1331–1334, 1347, 1386–1387, 1392, 1398, 1406 |
| 97 / MOVE_ELECTROBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 12 | 713–717, 1087–1092, 1100 |
| 98 / MOVE_STOREDPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 163 | 35–36, 38–40, 65, 79–80, 96–97, 113, 122, 124, 133–136, 150–151, 163–164, 173, 175–178, 196–197, 199–200, 203, 206, 234, 238, 242, 319, 348–349, 351–352, 356–357, 392–394, 407–409, 411, 478–479, 482, 486, 489–490, 492–493, 495, 521, 523–524, 528, 532–535, 541, 543, 546–547, 570–571, 580–581, 614, 627–632, 658–659, 720–735, 761–763, 777–779, 794–795, 808, 815, 827, 832, 834, 947, 981–982, 1002–1005, 1017–1018, 1022, 1026, 1073, 1077, 1117–1118, 1141, 1146–1150, 1158, 1160, 1168, 1190, 1193, 1203, 1210–1211, 1213–1216, 1220–1221, 1224, 1246, 1251, 1329–1330, 1347–1349, 1370, 1377–1379, 1382, 1384, 1404, 1420 |
| 98 / MOVE_STOREDPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 713–717, 848, 1079–1080 |
| 99 / MOVE_BREAKINGSWIPE | PROJECT_POLICY:LOCAL_POSITIVE | 59 | 6, 95, 112, 147–149, 151, 160, 208, 230, 248, 279, 329, 334, 359, 397, 406–408, 498, 517, 536–537, 540, 663–665, 688, 696–697, 699, 718, 752–753, 803, 805, 814, 826, 919–920, 975, 997, 1001, 1017, 1037, 1075, 1110, 1172, 1176, 1178–1179, 1187, 1248, 1361, 1392, 1395, 1403, 1405, 1407 |
| 99 / MOVE_BREAKINGSWIPE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 837, 1079–1080, 1369, 1390, 1394 |
| 100 / MOVE_RAZORSHELL | PROJECT_POLICY:LOCAL_POSITIVE | 18 | 80, 90–91, 98–99, 141, 151, 199, 326–327, 618, 642, 796–797, 985, 1126, 1216, 1224 |
| 100 / MOVE_RAZORSHELL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 554–556, 1241 |
| 101 / MOVE_HEX | PROJECT_POLICY:LOCAL_POSITIVE | 147 | 31, 34, 37–38, 72–73, 88–89, 92–94, 97, 150–151, 169, 198, 200, 206, 211, 303, 318–319, 322, 346–347, 361–362, 376–378, 469, 478–479, 482–483, 487–490, 495, 528, 530–532, 540, 544, 546, 596–598, 615–616, 623–624, 644–646, 657, 660–662, 718, 720–735, 763, 816–819, 834, 941, 965, 986–987, 995, 998, 1009–1010, 1019, 1025–1026, 1034–1035, 1039, 1075, 1141, 1146–1147, 1156, 1159, 1163, 1178–1179, 1189, 1193, 1211, 1223–1225, 1232, 1238–1239, 1244–1245, 1255, 1257, 1299, 1330, 1339–1342, 1349, 1365–1366, 1378–1379, 1383–1384, 1396–1402, 1404, 1415–1418, 1420–1421 |
| 101 / MOVE_HEX | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 385, 713–717 |
| 102 / MOVE_WEATHERBALL | PROJECT_POLICY:LOCAL_POSITIVE | 139 | 1–9, 37–38, 69–71, 79–80, 91, 131, 133–136, 144–146, 148–151, 186, 191–192, 196–197, 199, 225, 243–245, 249–251, 297, 310, 312–314, 321, 324, 329, 346–349, 359, 363, 446–448, 459–460, 473–474, 476, 478–479, 490, 502–503, 512–513, 519–520, 523–524, 531, 542–543, 579, 588–590, 602, 609, 637, 694–699, 752–756, 766, 774, 800–801, 803, 806–808, 814, 830, 947, 970–971, 973, 1025–1026, 1106–1110, 1122, 1137, 1165, 1167, 1215–1216, 1224, 1242, 1248, 1258–1259, 1318–1320, 1329, 1331–1334, 1346–1347, 1407 |
| 102 / MOVE_WEATHERBALL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 385, 868, 932 |
| 103 / MOVE_AIRSLASH | PROJECT_POLICY:LOCAL_POSITIVE | 174 | 6, 12, 41–42, 49, 83, 123, 144, 146, 149, 151, 163–164, 169, 177–178, 193, 198, 206, 212, 225–227, 245, 249–250, 300, 302, 309–310, 312, 333–334, 369, 376, 397, 406–408, 448–451, 469, 479, 483, 510–511, 521–522, 528, 545–546, 554–556, 572–574, 580–581, 595, 614, 620, 633–634, 640, 677–678, 680–683, 690–694, 700, 719–735, 754, 757, 769–771, 774, 789, 822–823, 825, 834, 868, 932, 939–941, 955, 958, 989–990, 1009, 1014–1015, 1043–1045, 1048–1064, 1075, 1110, 1113–1115, 1133, 1137, 1165, 1180, 1221, 1223, 1241–1242, 1246, 1250, 1252, 1300–1302, 1321–1324, 1333–1334, 1355, 1367, 1378–1380, 1390–1391, 1403, 1408, 1421 |
| 103 / MOVE_AIRSLASH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 16–18, 165–166, 176, 292, 304–305, 467, 494, 593–594 |
| 104 / MOVE_AURASPHERE | PROJECT_POLICY:LOCAL_POSITIVE | 63 | 7–9, 106–107, 150–151, 243, 251, 282, 357, 380, 394, 407–409, 445, 481, 501, 521, 528, 536–537, 540, 546, 672–673, 700, 718, 720–735, 757, 800–801, 834, 919–920, 1001, 1018–1019, 1073, 1078, 1184, 1208, 1250, 1296, 1329, 1357, 1404 |
| 105 / MOVE_BLAZEKICK | PROJECT_POLICY:LOCAL_POSITIVE | 21 | 6, 106, 151, 281–282, 500–501, 547, 673, 702, 747–750, 944, 1019, 1078, 1105–1107, 1222 |
| 105 / MOVE_BLAZEKICK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 357, 443–445 |
| 106 / MOVE_BUGBUZZ | PROJECT_POLICY:LOCAL_POSITIVE | 87 | 12, 48–49, 123, 151, 167–168, 193, 204–205, 212, 214, 301–303, 311–312, 333–334, 386–387, 455, 468–469, 504–505, 522, 546, 593–595, 641–642, 648–649, 669–670, 689–690, 702, 720–735, 747–750, 774, 834, 868, 932, 955, 959–960, 968–969, 984–985, 1012, 1117–1118, 1142–1143, 1164–1165, 1252, 1306–1309, 1346–1347, 1385, 1391 |
| 106 / MOVE_BUGBUZZ | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 165–166, 292, 294, 466–467, 709–710 |
| 107 / MOVE_CROSSPOISON | PROJECT_POLICY:LOCAL_POSITIVE | 27 | 68, 72–73, 123, 141, 151, 169, 212, 279, 390–391, 469, 504–505, 507, 598, 622, 648–649, 965, 971, 975, 1010, 1075, 1154, 1182, 1252 |
| 107 / MOVE_CROSSPOISON | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 15, 41–42, 46–47, 167–168, 207, 525, 1240, 1256, 1337–1338, 1421 |
| 108 / MOVE_CRUNCH | PROJECT_POLICY:LOCAL_POSITIVE | 238 | 4–6, 9, 24, 29–31, 41–42, 58–59, 111–112, 115, 130, 142–143, 151, 158–160, 169, 197, 203, 208–211, 216–217, 228–229, 243, 246–248, 277–279, 286–287, 326–327, 330–334, 337–338, 343, 346–347, 355, 372, 379, 384, 395–397, 405–406, 440–442, 456–458, 461–462, 471–472, 487–488, 497–498, 500–505, 517, 531, 538, 559–561, 604–606, 612–613, 617–620, 624, 656–657, 663–667, 674, 685–688, 694–698, 754–756, 760, 775–776, 782–783, 804–805, 820–821, 826, 942–944, 951–955, 961–962, 968–969, 990, 996, 1008, 1016, 1034–1035, 1046, 1048–1064, 1082, 1111–1112, 1120, 1125–1128, 1138–1139, 1142–1143, 1153, 1155, 1169, 1174–1175, 1180–1181, 1184–1185, 1187–1189, 1209–1212, 1233–1235, 1239, 1245, 1249, 1253, 1255, 1257, 1297–1299, 1310–1317, 1335–1336, 1344–1345, 1361, 1365–1366, 1370–1371, 1377, 1382–1383, 1390, 1392–1395, 1400, 1402–1403, 1405–1407, 1413, 1419 |
| 108 / MOVE_CRUNCH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 17 | 19–20, 374, 452–453, 508, 557–558, 564–569, 837, 1020–1021 |
| 109 / MOVE_DARKESTLARIAT | PROJECT_POLICY:LOCAL_POSITIVE | 21 | 62, 68, 143, 151, 285, 519, 530, 539, 606, 676, 783, 944, 977, 1004, 1011, 1084, 1104, 1153, 1184–1185, 1209 |
| 109 / MOVE_DARKESTLARIAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1405, 1419 |
| 110 / MOVE_HIGHHORSEPOWER | PROJECT_POLICY:LOCAL_POSITIVE | 106 | 31, 34, 51, 62, 68, 75–78, 95, 99, 111–112, 127–128, 143, 151, 185, 195, 203, 208, 214, 217, 220–221, 231–232, 241, 247–248, 285, 323–324, 339–340, 366, 384, 405, 442, 502–503, 517, 526, 539, 582–583, 586–587, 606, 639, 676, 679, 760, 768, 781, 805, 821, 826, 966–967, 977, 1004, 1011, 1016, 1028, 1076, 1084, 1104, 1112, 1126, 1130–1131, 1134, 1136, 1162, 1166, 1170–1172, 1188, 1210, 1213–1214, 1249, 1251, 1253, 1304–1305, 1343, 1360, 1362, 1368–1369, 1376–1377, 1381, 1385–1387, 1392, 1395, 1409–1411, 1413, 1419 |
| 110 / MOVE_HIGHHORSEPOWER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 461–462, 499, 784, 837 |
| 111 / MOVE_LEAFBLADE | PROJECT_POLICY:LOCAL_POSITIVE | 21 | 83, 151, 182, 251, 278–279, 299–300, 523, 528, 602, 693, 939–941, 970–971, 1015, 1157, 1217, 1250 |
| 111 / MOVE_LEAFBLADE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 14 | 71, 192, 369, 548–550, 595, 780–781, 1185, 1209, 1242, 1404, 1408 |
| 112 / MOVE_MUDDYWATER | PROJECT_POLICY:LOCAL_POSITIVE | 89 | 7–9, 55, 60–62, 72–73, 80, 108, 116–119, 130, 134, 138–139, 151, 160, 183–184, 186, 194–195, 199, 230, 246–248, 284–285, 296–297, 323–324, 326–329, 350, 381, 404, 475–476, 502–503, 516, 588–590, 617–618, 646, 671, 700, 757, 797, 800–801, 812–814, 963–965, 985, 998, 1005, 1108–1110, 1126, 1144–1145, 1163, 1216, 1224, 1233, 1247–1248, 1255, 1331–1332, 1353–1354, 1372, 1376 |
| 112 / MOVE_MUDDYWATER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 373–375, 1174–1175, 1184, 1300–1302, 1412 |
| 113 / MOVE_MYSTICALFIRE | PROJECT_POLICY:LOCAL_POSITIVE | 41 | 6, 35–38, 77–78, 122, 136, 146, 151, 175–176, 250, 394, 407–408, 520–521, 547, 608, 660–662, 690, 696, 808, 818–819, 827, 1008, 1077, 1143, 1148–1150, 1168, 1182, 1203, 1213–1214 |
| 113 / MOVE_MYSTICALFIRE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 33 | 157, 478–479, 482, 546, 720–735, 763, 834, 1238, 1246, 1258–1259, 1299, 1329, 1382, 1384, 1391, 1404 |
| 114 / MOVE_PHANTOMFORCE | PROJECT_POLICY:LOCAL_POSITIVE | 67 | 93–94, 151, 200, 303, 322, 377–378, 478–479, 482, 495, 540, 546, 616, 675–676, 718, 720–735, 816–817, 819, 825, 828–829, 834, 941, 995, 998, 1009, 1019, 1146–1147, 1159, 1178–1179, 1189, 1211, 1244–1245, 1255, 1330, 1339–1340, 1365–1366, 1375, 1384, 1415–1418 |
| 114 / MOVE_PHANTOMFORCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 1 | 544 |
| 115 / MOVE_PLAYROUGH | PROJECT_POLICY:LOCAL_POSITIVE | 175 | 25–26, 35–36, 39–40, 52–53, 58–59, 77–78, 151, 155–157, 172–176, 182–184, 209–210, 216–217, 231–232, 241, 286–287, 289, 355, 358–359, 364–366, 376, 386–387, 409, 456–458, 470, 474, 480–481, 487–488, 521, 533–535, 545, 559–563, 600, 625–626, 638–639, 647, 666–667, 701, 719, 780–781, 785–786, 792–793, 798–799, 804–805, 808, 810, 815, 824, 827, 832, 945–947, 959–962, 978–981, 992, 995, 997, 1003, 1005, 1018, 1022, 1029–1030, 1046, 1073, 1078, 1082, 1093–1099, 1119–1120, 1127–1128, 1148–1153, 1155, 1165, 1168, 1170–1171, 1180–1181, 1203, 1212–1214, 1219, 1238, 1253, 1258–1259, 1294–1296, 1303–1305, 1310–1317, 1335–1336, 1350–1352, 1365–1366, 1368–1369, 1381–1382, 1388–1389, 1421–1422 |
| 115 / MOVE_PLAYROUGH | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 13 | 315–316, 484–485, 494, 1087–1092, 1100, 1413 |
| 116 / MOVE_POLLENPUFF | PROJECT_POLICY:LOCAL_POSITIVE | 36 | 12, 45, 151, 187–189, 251, 469, 473–474, 601–602, 643–644, 774, 777–779, 868, 932, 960, 971–973, 981, 1121–1122, 1190, 1210–1211, 1242, 1296, 1320, 1383, 1399, 1414 |
| 116 / MOVE_POLLENPUFF | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 152–154, 387, 848 |
| 117 / MOVE_POWERGEM | PROJECT_POLICY:LOCAL_POSITIVE | 92 | 52–53, 55, 120–121, 150–151, 179–181, 185, 196, 199–200, 219, 222, 248, 320, 322, 348, 351–352, 469, 482, 489–491, 497–498, 529, 536–538, 541, 546, 578–579, 652–654, 720–735, 811, 827, 834, 919–920, 1010, 1017, 1029–1030, 1065, 1129–1131, 1156, 1166, 1216, 1224–1225, 1234–1235, 1296, 1325–1327, 1343, 1347, 1355, 1363–1364, 1384, 1386, 1392, 1396–1398, 1406 |
| 117 / MOVE_POWERGEM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1079–1080 |
| 118 / MOVE_PSYCHICFANGS | PROJECT_POLICY:LOCAL_POSITIVE | 84 | 58–59, 142, 151, 160, 196, 203, 208, 210, 228–229, 286–287, 330–331, 337–338, 355, 379, 397, 456–458, 525, 559–561, 581, 775–776, 804–805, 951–952, 961–962, 990, 996, 1008, 1017, 1046, 1048–1064, 1082, 1112, 1128, 1138–1139, 1169, 1174–1175, 1178–1181, 1234–1235, 1255, 1316–1317, 1335–1336, 1365–1366, 1370, 1377, 1382, 1400, 1419 |
| 118 / MOVE_PSYCHICFANGS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 20, 1021, 1079–1080 |
| 119 / MOVE_PSYCHOCUT | PROJECT_POLICY:LOCAL_POSITIVE | 50 | 64–65, 103, 121, 123–124, 141, 150–151, 212, 215, 251, 376, 399–400, 407–408, 514, 528, 533–535, 541, 563, 580–581, 614, 665, 677–678, 787–789, 794–795, 941, 971, 1003, 1009, 1015, 1017, 1118, 1150, 1180, 1189, 1211, 1214, 1221, 1252, 1380 |
| 119 / MOVE_PSYCHOCUT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 15 | 96–97, 308, 356–357, 939–940, 1079–1080, 1241, 1246, 1250, 1330, 1370, 1404 |
| 120 / MOVE_BRAVEBIRD | PROJECT_POLICY:LOCAL_POSITIVE | 65 | 41–42, 83–85, 144–146, 151, 169, 198, 225, 227, 250, 282, 309–310, 358–359, 449–451, 483, 574, 633–634, 680–683, 769–771, 809, 939–941, 948–950, 1002, 1113–1115, 1137, 1157, 1217, 1221–1223, 1246, 1250, 1300–1302, 1321–1324, 1333–1334, 1349, 1355, 1367, 1421 |
| 120 / MOVE_BRAVEBIRD | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 16–18, 22, 304–305 |
| 121 / MOVE_CLOSECOMBAT | PROJECT_POLICY:LOCAL_POSITIVE | 134 | 56–59, 62, 66–68, 83, 106–107, 123, 127–128, 151, 209–210, 212, 214, 216–217, 237, 282, 307, 327, 331, 335–336, 356–357, 376, 380, 444–445, 451, 481, 500–501, 507, 528, 586–587, 592, 606, 613, 642, 657, 665, 667, 672–673, 676, 679–681, 691–693, 700–701, 757, 760, 783, 787–789, 804–805, 809, 824, 944, 956–957, 962, 966–967, 977, 983, 985, 1000–1001, 1004, 1008, 1011–1012, 1019, 1046, 1078, 1082, 1138–1139, 1144–1145, 1154–1155, 1157, 1162, 1180–1181, 1183–1185, 1188, 1208–1210, 1217, 1222, 1234–1235, 1240, 1242, 1246, 1250, 1252–1253, 1256, 1302, 1312, 1330, 1357, 1367, 1375, 1381, 1383, 1385, 1389, 1404–1405, 1408–1411, 1419 |
| 121 / MOVE_CLOSECOMBAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 20, 166, 1002, 1021, 1413 |
| 122 / MOVE_FLAREBLITZ | PROJECT_POLICY:LOCAL_POSITIVE | 98 | 4–6, 37–38, 58–59, 77–78, 126, 136, 146, 151, 155–157, 228–229, 240, 244, 250, 281–282, 321, 339–340, 349, 443–445, 520, 538, 546–547, 551–553, 607–608, 684, 689–690, 696, 720–735, 761–763, 769–771, 775–776, 830, 834, 942–944, 974–975, 1008, 1039, 1105–1107, 1130–1131, 1143, 1229–1230, 1234–1235, 1238, 1297–1299, 1328–1330, 1385, 1391, 1402, 1405, 1410 |
| 122 / MOVE_FLAREBLITZ | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 3 | 566–567, 576 |
| 123 / MOVE_HURRICANE | PROJECT_POLICY:LOCAL_POSITIVE | 99 | 6, 12, 130, 142, 144–146, 149–151, 163–164, 169, 198, 226, 230, 249, 300, 309–310, 312, 358–359, 369, 397, 406, 449–451, 469, 483, 546, 574, 600, 633–634, 680–681, 690, 694, 720–735, 754, 769–771, 774, 822–823, 825, 834, 868, 932, 941, 958, 997, 1043–1045, 1114–1115, 1136–1137, 1165, 1221–1223, 1242, 1246, 1302, 1321–1324, 1333–1334, 1355, 1367, 1378, 1385, 1390–1391, 1403, 1407, 1421 |
| 123 / MOVE_HURRICANE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 10 | 16–18, 292, 304–305, 385, 467, 494, 1379 |
| 124 / MOVE_HYDROPUMP | PROJECT_POLICY:LOCAL_POSITIVE | 199 | 7–9, 54–55, 60–62, 72–73, 79–80, 87, 90–91, 99, 108, 112, 115–121, 129–131, 134, 138–141, 143, 147–149, 151, 158–160, 170–171, 183–184, 186, 194–195, 199, 211, 222–224, 226, 230, 245, 248–249, 283–285, 296–297, 309–314, 323–327, 329–331, 343, 372, 381, 384, 395–397, 404, 406, 446–448, 471–472, 475–476, 499, 509–511, 516–517, 537, 542–543, 546, 554–556, 588–590, 617–618, 645–647, 688, 700, 720–735, 757, 764–766, 798–801, 814, 821, 830, 834, 920, 945–947, 963–965, 969, 996–998, 1005, 1108–1110, 1125–1126, 1137–1139, 1145, 1156, 1163, 1167, 1173–1175, 1178–1179, 1215–1216, 1224–1225, 1239, 1241, 1248, 1255, 1257, 1300–1302, 1353–1354, 1356–1357, 1370–1372, 1376, 1388, 1390, 1403, 1407, 1411–1412 |
| 124 / MOVE_HYDROPUMP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 374–375, 385, 568–569 |
| 125 / MOVE_LEAFSTORM | PROJECT_POLICY:LOCAL_POSITIVE | 103 | 1–3, 71, 102–103, 114, 151–154, 182, 187–189, 191–192, 251, 277–279, 297, 300, 307, 344–345, 363, 369, 440–442, 459–460, 512–513, 518, 523, 545, 548–550, 595, 601–602, 609, 638–639, 643–644, 693, 719, 758–760, 780–781, 817, 939–941, 970–971, 978–980, 1037, 1102–1104, 1121–1122, 1133–1134, 1185, 1190, 1209–1211, 1236–1237, 1242, 1250, 1294–1296, 1318–1320, 1339–1342, 1344–1345, 1383, 1399, 1408, 1414–1418, 1422 |
| 125 / MOVE_LEAFSTORM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 466, 564–565, 709–710 |
| 126 / MOVE_MEGAHORN | PROJECT_POLICY:LOCAL_POSITIVE | 29 | 34, 78, 111–112, 118–119, 128, 131, 151, 214, 376, 517, 598, 641–642, 679, 691–693, 700, 757, 824, 1004, 1014, 1126, 1162, 1188, 1210, 1214 |
| 126 / MOVE_MEGAHORN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 11 | 167–168, 234, 556, 639, 1241, 1251, 1376, 1381, 1387, 1408 |
| 127 / MOVE_POWERWHIP | PROJECT_POLICY:LOCAL_POSITIVE | 29 | 1–3, 108, 114, 130, 151, 363, 389, 460, 516, 518, 589–590, 651, 814, 819, 980, 998, 1013, 1037, 1142–1143, 1150, 1153, 1170–1171, 1185, 1209 |
| 127 / MOVE_POWERWHIP | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 21 | 69–71, 207, 232, 379, 508, 525, 1190, 1210–1211, 1248, 1339–1342, 1361, 1381, 1387, 1399, 1422 |
| 128 / MOVE_SOLARBLADE | PROJECT_POLICY:LOCAL_POSITIVE | 47 | 77–78, 83, 151–154, 251, 278–279, 299–300, 369, 474, 518, 523, 528, 602, 611, 693, 787–789, 941, 971, 980, 998, 1015, 1102–1104, 1157, 1180, 1185, 1190, 1209–1211, 1217, 1242, 1318–1320, 1330, 1399, 1408, 1422 |
| 128 / MOVE_SOLARBLADE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 70–71 |
| 129 / MOVE_EXPANDINGFORCE | PROJECT_POLICY:LOCAL_POSITIVE | 23 | 96–97, 203, 351–352, 356–357, 410–411, 763, 828–829, 996, 1040–1042, 1246, 1329, 1347, 1349, 1370, 1377, 1382 |
| 129 / MOVE_EXPANDINGFORCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 486, 701, 1079–1080, 1348, 1408 |
| 129 / MOVE_EXPANDINGFORCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 10 | 737, 875–876, 882–883, 893, 906, 916, 1278, 1287 |
| 130 / MOVE_STEELROLLER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 30 | 74–76, 100–101, 205, 232, 463–464, 529, 760, 1031–1033, 1065, 1236–1237, 1239, 1247–1248, 1257, 1332, 1350–1352, 1359–1360, 1362, 1382, 1387 |
| 130 / MOVE_STEELROLLER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 885, 896, 904, 906, 1271, 1273, 1290–1291, 1430 |
| 131 / MOVE_SCALESHOT | PROJECT_POLICY:LOCAL_POSITIVE | 15 | 23–24, 160, 325, 550, 605, 647, 1239, 1255, 1257, 1361, 1370, 1395, 1403, 1405 |
| 131 / MOVE_SCALESHOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 317, 374–375, 379, 509–510, 837, 996 |
| 131 / MOVE_SCALESHOT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 15 | 838, 870–871, 880, 890, 899, 907–908, 911, 913, 1047, 1261, 1276, 1279, 1283 |
| 132 / MOVE_METEORBEAM | PROJECT_POLICY:LOCAL_POSITIVE | 12 | 320, 410, 464, 529, 1033, 1040–1042, 1065, 1327, 1363–1364 |
| 132 / MOVE_METEORBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 6 | 76, 461–463, 1079–1080 |
| 132 / MOVE_METEORBEAM | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 881, 885, 896, 906, 911, 918, 1207, 1279–1280 |
| 133 / MOVE_MISTYEXPLOSION | PROJECT_POLICY:LOCAL_POSITIVE | 4 | 779, 1258–1259, 1382 |
| 133 / MOVE_MISTYEXPLOSION | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 893, 918, 1101, 1287, 1289 |
| 134 / MOVE_GRASSYGLIDE | PROJECT_POLICY:LOCAL_POSITIVE | 39 | 69–71, 152–154, 192, 344–345, 440–442, 545, 548–550, 593–595, 638–639, 719, 758–760, 780–781, 1236–1237, 1294–1296, 1339–1342, 1344–1345, 1422 |
| 134 / MOVE_GRASSYGLIDE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 46–47, 466, 508, 564–565, 709–710 |
| 134 / MOVE_GRASSYGLIDE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 751, 869, 890, 915, 1260, 1274, 1281–1282, 1431 |
| 135 / MOVE_RISINGVOLTAGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 40 | 100–101, 179–181, 353–354, 470, 575–576, 655–657, 713–717, 1031–1033, 1087–1092, 1236–1237, 1310–1312, 1331–1334, 1386, 1389, 1392, 1406 |
| 135 / MOVE_RISINGVOLTAGE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 898, 1204, 1264, 1284–1285 |
| 136 / MOVE_TERRAINPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 27 | 546, 720–735, 834, 1387–1392, 1404, 1406, 1408 |
| 136 / MOVE_TERRAINPULSE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 869, 872, 878, 914, 918, 1101, 1260, 1262, 1271 |
| 137 / MOVE_SKITTERSMACK | PROJECT_POLICY:LOCAL_POSITIVE | 23 | 23–24, 167–168, 377–379, 593–595, 774, 1244–1245, 1306–1309, 1346–1347, 1350–1352, 1385 |
| 137 / MOVE_SKITTERSMACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 24 | 46–47, 88–89, 200, 218–219, 292, 294, 367–368, 440–442, 482, 766, 837, 868, 932, 1034–1035, 1250, 1384, 1391 |
| 137 / MOVE_SKITTERSMACK | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 6 | 838, 877, 1267, 1279, 1283, 1286 |
| 138 / MOVE_BURNINGJEALOUSY | PROJECT_POLICY:LOCAL_POSITIVE | 26 | 155–157, 200, 219, 228–229, 378, 443–445, 482, 761–763, 776, 974–975, 1105–1107, 1238, 1244–1245, 1345, 1402 |
| 138 / MOVE_BURNINGJEALOUSY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 218, 287, 566–567, 1021 |
| 138 / MOVE_BURNINGJEALOUSY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 4 | 737, 1072, 1231, 1288 |
| 139 / MOVE_LASHOUT | PROJECT_POLICY:LOCAL_POSITIVE | 66 | 56–57, 89, 150, 198, 228–229, 247, 286–287, 336, 339–340, 345, 365–366, 377–379, 444–445, 448, 482–483, 544, 687–688, 828–829, 1035, 1239–1241, 1244–1245, 1248, 1256–1257, 1296, 1304–1305, 1309, 1321–1324, 1335–1336, 1345, 1355, 1360, 1375, 1383, 1390, 1399–1403, 1409–1411, 1419–1422 |
| 139 / MOVE_LASHOUT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 2 | 1020–1021 |
| 139 / MOVE_LASHOUT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 9 | 737, 880, 889, 894, 1204, 1231, 1265, 1288, 1292 |
| 140 / MOVE_POLTERGEIST | PROJECT_POLICY:LOCAL_POSITIVE | 21 | 200, 377–378, 482, 1189, 1238, 1245, 1299, 1330, 1339–1340, 1347, 1365–1366, 1384, 1398, 1415–1418, 1420 |
| 140 / MOVE_POLTERGEIST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 713–717 |
| 140 / MOVE_POLTERGEIST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 877, 894, 1267 |
| 141 / MOVE_CORROSIVEGAS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 367–368, 1359–1360 |
| 141 / MOVE_CORROSIVEGAS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 877, 1267, 1272 |
| 142 / MOVE_COACHING | PROJECT_POLICY:LOCAL_POSITIVE | 15 | 335–336, 445, 552–553, 701, 760, 956–957, 1240, 1256, 1311–1312, 1375, 1404 |
| 142 / MOVE_COACHING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 57, 307, 356–357, 444, 1367, 1389, 1405 |
| 142 / MOVE_COACHING | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 8 | 887, 891, 914, 916, 1266, 1275, 1292–1293 |
| 143 / MOVE_FLIPTURN | PROJECT_POLICY:LOCAL_POSITIVE | 30 | 54, 86–87, 211, 325, 446–448, 471–472, 509–510, 542–543, 554–556, 647, 996, 1110, 1138, 1167, 1241, 1255, 1301–1302, 1357, 1370, 1388, 1407 |
| 143 / MOVE_FLIPTURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 4 | 374–375, 568–569 |
| 143 / MOVE_FLIPTURN | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 5 | 872, 892, 899, 1047, 1262 |
| 144 / MOVE_TRIPLEAXEL | PROJECT_POLICY:LOCAL_POSITIVE | 2 | 87, 701 |
| 144 / MOVE_TRIPLEAXEL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 8 | 510, 634, 1388, 1393–1395, 1400, 1404 |
| 144 / MOVE_TRIPLEAXEL | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 3 | 893, 912, 916 |
| 145 / MOVE_DUALWINGBEAT | PROJECT_POLICY:LOCAL_POSITIVE | 29 | 198, 207, 312, 448–451, 483, 522, 525, 948–950, 958, 1043–1045, 1321–1324, 1333–1334, 1355, 1367, 1385, 1390, 1405, 1421 |
| 145 / MOVE_DUALWINGBEAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 22 | 15–18, 21–22, 165–166, 193, 292, 294, 304–305, 386–387, 466–467, 494, 633–634, 709–710 |
| 145 / MOVE_DUALWINGBEAT | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 14 | 870–871, 881, 886, 901, 905, 907–908, 1191–1192, 1261, 1263, 1277, 1281 |
| 146 / MOVE_SCORCHINGSANDS | PROJECT_POLICY:LOCAL_POSITIVE | 8 | 157, 219, 339–340, 445, 763, 1235, 1386 |
| 146 / MOVE_SCORCHINGSANDS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 20 | 74–76, 218, 229, 231–232, 553, 567, 776, 837, 1031–1033, 1238, 1253, 1381, 1387, 1401, 1413 |
| 146 / MOVE_SCORCHINGSANDS | UNVERIFIABLE_FROM_SELECTED_REFERENCE:REFERENCE_POSITIVE_LOCAL_NEGATIVE | 12 | 838, 870–871, 885, 891, 909, 913, 1261, 1275, 1280, 1283, 1286 |
| 147 / MOVE_CONFUSERAY | PROJECT_POLICY:LOCAL_POSITIVE | 153 | 37–38, 48–49, 54–55, 81–82, 88–89, 92–94, 97, 126, 131, 150–151, 170–171, 179–181, 196–198, 200, 203, 234, 240, 322, 351–352, 361–362, 377–378, 386, 392–394, 409, 456–458, 469, 482–483, 489–490, 495, 509–510, 515, 520, 528, 530–534, 539–541, 544, 546, 623–624, 657, 660–662, 668, 718, 720–735, 763, 774, 816–817, 834, 868, 932, 939–941, 986–987, 995, 1009, 1018, 1025–1026, 1029–1030, 1065, 1073, 1146–1147, 1177–1179, 1182, 1189, 1211, 1238, 1244–1246, 1250–1251, 1255, 1328–1332, 1339–1342, 1347–1349, 1363–1366, 1377, 1383–1384, 1391, 1396–1398, 1402, 1404, 1406, 1420 |
| 147 / MOVE_CONFUSERAY | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 25 | 41–42, 120–121, 141, 169, 177–178, 226, 303, 388–389, 511, 558, 713–717, 818–819, 972–973, 1077, 1118 |
| 148 / MOVE_CHILLINGWATER | PROJECT_POLICY:LOCAL_POSITIVE | 210 | 7–9, 39–40, 52–55, 60–62, 72–73, 79–80, 86–87, 90–91, 113, 116–117, 130–131, 134, 147–151, 158–162, 170–171, 183–184, 186, 194–195, 199, 206, 211, 225, 230, 242, 249, 283–285, 295–297, 309–312, 323–324, 326–329, 335–336, 346–347, 351–352, 364–366, 404, 446–448, 471–472, 475–476, 483, 506–507, 509–510, 512–514, 524, 531, 537, 542–543, 546, 554–556, 633–634, 647, 666–668, 694, 720–735, 754, 764–766, 777–779, 798–801, 812–814, 820–821, 834, 920, 945–947, 951–952, 956–957, 964–965, 968–969, 982–983, 986–987, 996, 1029–1030, 1108–1110, 1125–1126, 1138–1139, 1151–1153, 1155, 1163, 1167, 1208, 1215–1216, 1224, 1239, 1241, 1247–1249, 1255, 1257, 1296, 1300–1305, 1314, 1331–1332, 1353–1354, 1356–1357, 1367–1372, 1376, 1378–1379, 1388, 1407, 1411–1412 |
| 148 / MOVE_CHILLINGWATER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 84 | 98–99, 108, 118–121, 124, 138–141, 222–224, 226, 238, 288–289, 313–317, 330–331, 341–343, 370–375, 381, 385, 402, 452–453, 516, 568–569, 617–618, 635–637, 645–646, 796–797, 806–807, 848, 963, 985, 990, 997, 1005, 1048–1064, 1154, 1156, 1175, 1225–1227, 1315 |
| 149 / MOVE_POUNCE | PROJECT_POLICY:LOCAL_POSITIVE | 66 | 48–49, 123, 151, 204–206, 212, 214, 306–307, 311–312, 366, 377–379, 455, 469, 538, 689–690, 772–774, 800–801, 868, 932, 964–965, 968–969, 995, 1132–1134, 1164–1165, 1178–1179, 1252, 1306–1309, 1321–1324, 1337–1340, 1346–1352, 1367, 1378–1379, 1391, 1414 |
| 149 / MOVE_POUNCE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 5 | 467, 1011–1012, 1142–1143 |
| 150 / MOVE_TRAILBLAZE | PROJECT_POLICY:LOCAL_POSITIVE | 274 | 1–3, 25–26, 39–40, 43–45, 52–55, 69–71, 96–97, 113, 123, 128, 133–136, 150–154, 172, 174, 179–185, 187–189, 191–192, 194–197, 203, 212, 214–217, 225, 228–229, 231–232, 234, 242, 277–279, 295–300, 339–340, 344–347, 351–352, 356–359, 365–366, 369, 378–379, 440–442, 455–458, 470, 487–488, 491, 500–501, 512–514, 523–524, 531, 545–546, 548–550, 593–595, 601–602, 638–639, 663–667, 689–690, 693, 719–735, 758–760, 764–766, 775–781, 808–810, 816–817, 834, 939–941, 951–952, 958, 961–962, 970–971, 974–975, 978–983, 992, 995, 1022, 1029–1030, 1037, 1043–1046, 1082, 1093–1099, 1102–1107, 1111–1112, 1133–1134, 1141, 1151–1153, 1155, 1162, 1180–1181, 1184–1185, 1188, 1193, 1208–1210, 1212, 1222, 1240, 1242, 1250–1253, 1256, 1294–1296, 1303–1309, 1314, 1316–1320, 1335–1345, 1361, 1376–1377, 1383, 1385, 1399, 1408–1413, 1420, 1422 |
| 150 / MOVE_TRAILBLAZE | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 34 | 46–47, 102–103, 114, 251, 363, 459–460, 473–474, 508, 518, 564–565, 599–600, 609, 818–819, 848, 998, 1087–1092, 1100, 1121–1124, 1315 |
| 151 / MOVE_ICESPINNER | PROJECT_POLICY:LOCAL_POSITIVE | 56 | 39–40, 90–91, 144, 149, 151, 183–184, 204–206, 225, 232, 346–347, 446–448, 471–472, 489–490, 512–514, 531, 668, 820–821, 957, 964–965, 992, 1018, 1023–1024, 1073, 1126, 1165, 1167, 1208, 1242, 1247–1249, 1302, 1361, 1368–1369, 1378–1379, 1381, 1387–1388, 1400 |
| 151 / MOVE_ICESPINNER | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 9 | 120–121, 138–139, 399–400, 516, 1229–1230 |
| 152 / MOVE_TERABLAST | PROJECT_POLICY:LOCAL_POSITIVE | 824 | 1–9, 23–28, 35–40, 43–45, 48–62, 69–76, 79–82, 84–94, 96–97, 100–103, 106–107, 109–113, 116–117, 123, 125–126, 128, 130–131, 133–137, 143–164, 167–168, 170–174, 179–200, 203–207, 209–212, 214–221, 225, 227–234, 236–237, 239–240, 242–250, 277–287, 295–300, 306–307, 309–312, 320–329, 332–336, 339–340, 344–347, 350–354, 356–359, 361–362, 364–369, 377–380, 386–387, 392–397, 399–411, 440–451, 454–458, 461–464, 468–472, 475–479, 482–483, 486–491, 493, 495–503, 506–507, 509–510, 512–515, 517, 519–520, 522–546, 548–556, 575–576, 582–583, 585–587, 593–595, 599–602, 604–606, 612–613, 623–634, 638–639, 643–644, 647–649, 655–657, 660–668, 672–673, 675–678, 680–683, 686–701, 718–735, 752–766, 769–781, 785–786, 794–795, 798–801, 808–817, 820–823, 827–830, 832, 834, 868, 919–920, 932, 939–962, 964–971, 974–975, 978–983, 986–987, 992, 995–996, 999–1001, 1008–1009, 1017–1018, 1022–1035, 1037, 1040–1046, 1065, 1073, 1082, 1093–1099, 1102–1115, 1125–1126, 1129–1141, 1146–1153, 1155, 1160, 1162–1171, 1176–1190, 1193, 1203, 1208–1212, 1215–1216, 1219, 1221–1224, 1234–1242, 1244–1253, 1255–1259, 1294–1357, 1359–1372, 1375–1422 |
| 152 / MOVE_TERABLAST | UNVERIFIABLE_FROM_SELECTED_REFERENCE:LOCAL_POSITIVE | 333 | 12, 15–22, 29–34, 41–42, 46–47, 63–68, 77–78, 83, 95, 98–99, 104–105, 108, 114–115, 118–122, 124, 127, 138–142, 165–166, 169, 175–178, 201, 208, 213, 222–224, 226, 238, 241, 251, 288–289, 292, 294, 301–305, 308, 313–319, 330–331, 337–338, 341–343, 348–349, 355, 363, 370–376, 381–385, 388–391, 452–453, 459–460, 466–467, 473–474, 480–481, 484–485, 492, 494, 504–505, 508, 511, 516, 518, 521, 547, 557–574, 577–581, 584, 588–592, 596–598, 607–611, 614–622, 635–637, 640–642, 645–646, 650–654, 658–659, 669–671, 674, 679, 684–685, 702, 709–710, 713–717, 747–750, 767–768, 782–784, 787–793, 796–797, 802–807, 818–819, 824–826, 837, 848, 963, 972–973, 976–977, 984–985, 989–990, 993–994, 997–998, 1002–1005, 1010–1016, 1019–1021, 1039, 1048–1064, 1074–1080, 1083–1084, 1087–1092, 1100, 1117–1124, 1127–1128, 1142–1145, 1154, 1156–1159, 1172–1175, 1213–1214, 1217, 1220, 1225–1227, 1229–1230, 1232–1233 |

## Appendix J — complete UPR generated-move numeric counterexamples

| Local generated constant | Local move ID |
| --- | --- |
| MOVE_10000000_VOLT_THUNDERBOLT | 804 |
| MOVE_ACID_DOWNPOUR_P | 773 |
| MOVE_ACID_DOWNPOUR_S | 774 |
| MOVE_ALL_OUT_PUMMELING_P | 769 |
| MOVE_ALL_OUT_PUMMELING_S | 770 |
| MOVE_BLACK_HOLE_ECLIPSE_P | 799 |
| MOVE_BLACK_HOLE_ECLIPSE_S | 800 |
| MOVE_BLOOM_DOOM_P | 789 |
| MOVE_BLOOM_DOOM_S | 790 |
| MOVE_BREAKNECK_BLITZ_P | 767 |
| MOVE_BREAKNECK_BLITZ_S | 768 |
| MOVE_CATASTROPIKA | 803 |
| MOVE_CLANGOROUS_SOULBLAZE | 814 |
| MOVE_CONTINENTAL_CRUSH_P | 777 |
| MOVE_CONTINENTAL_CRUSH_S | 778 |
| MOVE_CORKSCREW_CRASH_P | 783 |
| MOVE_CORKSCREW_CRASH_S | 784 |
| MOVE_DEVASTATING_DRAKE_P | 797 |
| MOVE_DEVASTATING_DRAKE_S | 798 |
| MOVE_EXTREME_EVOBOOST | 806 |
| MOVE_GENESIS_SUPERNOVA | 808 |
| MOVE_GIGAVOLT_HAVOC_P | 791 |
| MOVE_GIGAVOLT_HAVOC_S | 792 |
| MOVE_GUARDIAN_OF_ALOLA | 815 |
| MOVE_G_MAX_BEFUDDLE_P | 863 |
| MOVE_G_MAX_BEFUDDLE_S | 864 |
| MOVE_G_MAX_CANNONADE_P | 861 |
| MOVE_G_MAX_CANNONADE_S | 862 |
| MOVE_G_MAX_CENTIFERNO_P | 907 |
| MOVE_G_MAX_CENTIFERNO_S | 908 |
| MOVE_G_MAX_CHI_STRIKE_P | 869 |
| MOVE_G_MAX_CHI_STRIKE_S | 870 |
| MOVE_G_MAX_CUDDLE_P | 877 |
| MOVE_G_MAX_CUDDLE_S | 878 |
| MOVE_G_MAX_DEPLETION_P | 917 |
| MOVE_G_MAX_DEPLETION_S | 918 |
| MOVE_G_MAX_DRUM_SOLO_P | 885 |
| MOVE_G_MAX_DRUM_SOLO_S | 886 |
| MOVE_G_MAX_FINALE_P | 913 |
| MOVE_G_MAX_FINALE_S | 914 |
| MOVE_G_MAX_FIREBALL_P | 887 |
| MOVE_G_MAX_FIREBALL_S | 888 |
| MOVE_G_MAX_FOAM_BURST_P | 873 |
| MOVE_G_MAX_FOAM_BURST_S | 874 |
| MOVE_G_MAX_GOLD_RUSH_P | 867 |
| MOVE_G_MAX_GOLD_RUSH_S | 868 |
| MOVE_G_MAX_GRAVITAS_P | 893 |
| MOVE_G_MAX_GRAVITAS_S | 894 |
| MOVE_G_MAX_HYDROSNIPE_P | 889 |
| MOVE_G_MAX_HYDROSNIPE_S | 890 |
| MOVE_G_MAX_MALODOR_P | 881 |
| MOVE_G_MAX_MALODOR_S | 882 |
| MOVE_G_MAX_MELTDOWN_P | 883 |
| MOVE_G_MAX_MELTDOWN_S | 884 |
| MOVE_G_MAX_ONE_BLOW_P | 919 |
| MOVE_G_MAX_ONE_BLOW_S | 920 |
| MOVE_G_MAX_RAPID_FLOW_P | 921 |
| MOVE_G_MAX_RAPID_FLOW_S | 922 |
| MOVE_G_MAX_REPLENISH_P | 879 |
| MOVE_G_MAX_REPLENISH_S | 880 |
| MOVE_G_MAX_RESONANCE_P | 875 |
| MOVE_G_MAX_RESONANCE_S | 876 |
| MOVE_G_MAX_SANDBLAST_P | 903 |
| MOVE_G_MAX_SANDBLAST_S | 904 |
| MOVE_G_MAX_SMITE_P | 909 |
| MOVE_G_MAX_SMITE_S | 910 |
| MOVE_G_MAX_SNOOZE_P | 911 |
| MOVE_G_MAX_SNOOZE_S | 912 |
| MOVE_G_MAX_STEELSURGE_P | 915 |
| MOVE_G_MAX_STEELSURGE_S | 916 |
| MOVE_G_MAX_STONESURGE_P | 895 |
| MOVE_G_MAX_STONESURGE_S | 896 |
| MOVE_G_MAX_STUN_SHOCK_P | 905 |
| MOVE_G_MAX_STUN_SHOCK_S | 906 |
| MOVE_G_MAX_SWEETNESS_P | 901 |
| MOVE_G_MAX_SWEETNESS_S | 902 |
| MOVE_G_MAX_TARTNESS_P | 899 |
| MOVE_G_MAX_TARTNESS_S | 900 |
| MOVE_G_MAX_TERROR_P | 871 |
| MOVE_G_MAX_TERROR_S | 872 |
| MOVE_G_MAX_VINE_LASH_P | 857 |
| MOVE_G_MAX_VINE_LASH_S | 858 |
| MOVE_G_MAX_VOLCALITH_P | 897 |
| MOVE_G_MAX_VOLCALITH_S | 898 |
| MOVE_G_MAX_VOLT_CRASH_P | 865 |
| MOVE_G_MAX_VOLT_CRASH_S | 866 |
| MOVE_G_MAX_WILDFIRE_P | 859 |
| MOVE_G_MAX_WILDFIRE_S | 860 |
| MOVE_G_MAX_WIND_RAGE_P | 891 |
| MOVE_G_MAX_WIND_RAGE_S | 892 |
| MOVE_HYDRO_VORTEX_P | 787 |
| MOVE_HYDRO_VORTEX_S | 788 |
| MOVE_INFERNO_OVERDRIVE_P | 785 |
| MOVE_INFERNO_OVERDRIVE_S | 786 |
| MOVE_LETS_SNUGGLE_FOREVER | 813 |
| MOVE_LIGHT_THAT_BURNS_THE_SKY | 818 |
| MOVE_MALICIOUS_MOONSAULT | 810 |
| MOVE_MAX_AIRSTREAM_P | 825 |
| MOVE_MAX_AIRSTREAM_S | 826 |
| MOVE_MAX_DARKNESS_P | 853 |
| MOVE_MAX_DARKNESS_S | 854 |
| MOVE_MAX_FLARE_P | 839 |
| MOVE_MAX_FLARE_S | 840 |
| MOVE_MAX_FLUTTERBY_P | 833 |
| MOVE_MAX_FLUTTERBY_S | 834 |
| MOVE_MAX_GEYSER_P | 841 |
| MOVE_MAX_GEYSER_S | 842 |
| MOVE_MAX_GUARD | 820 |
| MOVE_MAX_HAILSTORM_P | 849 |
| MOVE_MAX_HAILSTORM_S | 850 |
| MOVE_MAX_KNUCKLE_P | 823 |
| MOVE_MAX_KNUCKLE_S | 824 |
| MOVE_MAX_LIGHTNING_P | 845 |
| MOVE_MAX_LIGHTNING_S | 846 |
| MOVE_MAX_MINDSTORM_P | 847 |
| MOVE_MAX_MINDSTORM_S | 848 |
| MOVE_MAX_OOZE_P | 827 |
| MOVE_MAX_OOZE_S | 828 |
| MOVE_MAX_OVERGROWTH_P | 843 |
| MOVE_MAX_OVERGROWTH_S | 844 |
| MOVE_MAX_PHANTASM_P | 835 |
| MOVE_MAX_PHANTASM_S | 836 |
| MOVE_MAX_QUAKE_P | 829 |
| MOVE_MAX_QUAKE_S | 830 |
| MOVE_MAX_ROCKFALL_P | 831 |
| MOVE_MAX_ROCKFALL_S | 832 |
| MOVE_MAX_STARFALL_P | 855 |
| MOVE_MAX_STARFALL_S | 856 |
| MOVE_MAX_STEELSPIKE_P | 837 |
| MOVE_MAX_STEELSPIKE_S | 838 |
| MOVE_MAX_STRIKE_P | 821 |
| MOVE_MAX_STRIKE_S | 822 |
| MOVE_MAX_WYRMWIND_P | 851 |
| MOVE_MAX_WYRMWIND_S | 852 |
| MOVE_MENACING_MOONRAZE_MAELSTROM | 817 |
| MOVE_NEVER_ENDING_NIGHTMARE_P | 781 |
| MOVE_NEVER_ENDING_NIGHTMARE_S | 782 |
| MOVE_OCEANIC_OPERETTA | 811 |
| MOVE_PULVERIZING_PANCAKE | 807 |
| MOVE_SAVAGE_SPIN_OUT_P | 779 |
| MOVE_SAVAGE_SPIN_OUT_S | 780 |
| MOVE_SEARING_SUNRAZE_SMASH | 816 |
| MOVE_SHATTERED_PSYCHE_P | 793 |
| MOVE_SHATTERED_PSYCHE_S | 794 |
| MOVE_SINISTER_ARROW_RAID | 809 |
| MOVE_SOUL_STEALING_7_STAR_STRIKE | 819 |
| MOVE_SPLINTERED_STORMSHARDS | 812 |
| MOVE_STOKED_SPARKSURFER | 805 |
| MOVE_SUBZERO_SLAMMER_P | 795 |
| MOVE_SUBZERO_SLAMMER_S | 796 |
| MOVE_SUPERSONIC_SKYSTRIKE_P | 771 |
| MOVE_SUPERSONIC_SKYSTRIKE_S | 772 |
| MOVE_TECTONIC_RAGE_P | 775 |
| MOVE_TECTONIC_RAGE_S | 776 |
| MOVE_TWINKLE_TACKLE_P | 801 |
| MOVE_TWINKLE_TACKLE_S | 802 |

Relevant source anchors: UPR `Gen3RomHandler.java` profile constants 175–207, pool asset guard 925–965, ability load/write 1914ff, wild exclusions 4368ff, moveset owner 5290ff, TM 6440ff, tutors 6685–6765, highest Ability index 7594, Pickup 7350ff; random `WildEncounterRandomizer`, `TrainerPokemonRandomizer`, `StarterRandomizer`, `SpeciesAbilityRandomizer`, `SpeciesMovesetRandomizer`; `GlobalConstants.zMoves` and `MoveIDs`; CFRU `ability_util.c`, `ability_battle_effects.c`, `damage_calc.c`, `accuracy_calc.c`, `evolution.c`, `include/pokemon.h`, `include/battle.h`; DPE source/constant tables identified above. All anchors refer to the exact pinned revisions in §1.

### UPR evolution rows outside methods 1–15

| Local parent | Exact ignored rows |
| --- | --- |
| SPECIES_ABOMASNOW | [["EVO_MEGA","ITEM_ABOMASITE","SPECIES_ABOMASNOW_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABOMASNOW_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ABOMASNOW","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABSOL | [["EVO_MEGA","ITEM_ABSOLITE","SPECIES_ABSOL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ABSOL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ABSOL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AERODACTYL | [["EVO_MEGA","ITEM_AERODACTYLITE","SPECIES_AERODACTYL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AERODACTYL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AERODACTYL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AGGRON | [["EVO_MEGA","ITEM_AGGRONITE","SPECIES_AGGRON_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AGGRON_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AGGRON","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AIPOM | [["EVO_MOVE","MOVE_DOUBLEHIT","SPECIES_AMBIPOM","0"]] |
| SPECIES_ALAKAZAM | [["EVO_MEGA","ITEM_ALAKAZITE","SPECIES_ALAKAZAM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALAKAZAM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ALAKAZAM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALCREMIE_BERRY | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_CLOVER | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_FLOWER | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_ALCREMIE_STRAWBERRY","0"]] |
| SPECIES_ALCREMIE_LOVE | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_RIBBON | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALCREMIE_STRAWBERRY | [["EVO_GIGANTAMAX","TRUE","SPECIES_ALCREMIE_GIGA","0"]] |
| SPECIES_ALTARIA | [["EVO_MEGA","ITEM_ALTARIANITE","SPECIES_ALTARIA_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_ALTARIA_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_ALTARIA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AMAURA | [["EVO_LEVEL_NIGHT","39","SPECIES_AURORUS","0"]] |
| SPECIES_AMPHAROS | [["EVO_MEGA","ITEM_AMPHAROSITE","SPECIES_AMPHAROS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AMPHAROS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AMPHAROS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_APPLETUN | [["EVO_GIGANTAMAX","TRUE","SPECIES_APPLETUN_GIGA","0"]] |
| SPECIES_APPLETUN_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_APPLETUN","0"]] |
| SPECIES_AUDINO | [["EVO_MEGA","ITEM_AUDINITE","SPECIES_AUDINO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_AUDINO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_AUDINO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BANETTE | [["EVO_MEGA","ITEM_BANETTITE","SPECIES_BANETTE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BANETTE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BANETTE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BASCULIN_H | [["EVO_MOVE_MALE","MOVE_WAVECRASH","SPECIES_BASCULEGION_M","0"],["EVO_MOVE_FEMALE","MOVE_WAVECRASH","SPECIES_BASCULEGION_F","0"]] |
| SPECIES_BEEDRILL | [["EVO_MEGA","ITEM_BEEDRILLITE","SPECIES_BEEDRILL_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BEEDRILL_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BEEDRILL","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BERGMITE | [["EVO_LEVEL_HOLD_ITEM","37","SPECIES_AVALUGG_H","ITEM_HISUI_ROCK"]] |
| SPECIES_BLASTOISE | [["EVO_MEGA","ITEM_BLASTOISINITE","SPECIES_BLASTOISE_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_BLASTOISE_GIGA","0"]] |
| SPECIES_BLASTOISE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_BLASTOISE","0"]] |
| SPECIES_BLASTOISE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BLASTOISE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BLAZIKEN | [["EVO_MEGA","ITEM_BLAZIKENITE","SPECIES_BLAZIKEN_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BLAZIKEN_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_BLAZIKEN","MEGA_VARIANT_STANDARD"]] |
| SPECIES_BONSLY | [["EVO_MOVE","MOVE_MIMIC","SPECIES_SUDOWOODO","0"]] |
| SPECIES_BURMY | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_BURMY_SANDY | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_SANDY","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_BURMY_TRASH | [["EVO_FEMALE_LEVEL","20","SPECIES_WORMADAM_TRASH","0"],["EVO_MALE_LEVEL","20","SPECIES_MOTHIM","0"]] |
| SPECIES_BUTTERFREE | [["EVO_GIGANTAMAX","TRUE","SPECIES_BUTTERFREE_GIGA","0"]] |
| SPECIES_BUTTERFREE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_BUTTERFREE","0"]] |
| SPECIES_CAMERUPT | [["EVO_MEGA","ITEM_CAMERUPTITE","SPECIES_CAMERUPT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CAMERUPT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_CAMERUPT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CENTISKORCH | [["EVO_GIGANTAMAX","TRUE","SPECIES_CENTISKORCH_GIGA","0"]] |
| SPECIES_CENTISKORCH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CENTISKORCH","0"]] |
| SPECIES_CHARIZARD | [["EVO_MEGA","ITEM_CHARIZARDITE_X","SPECIES_CHARIZARD_MEGA_X","MEGA_VARIANT_STANDARD"],["EVO_MEGA","ITEM_CHARIZARDITE_Y","SPECIES_CHARIZARD_MEGA_Y","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_CHARIZARD_GIGA","0"]] |
| SPECIES_CHARIZARD_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CHARIZARD","0"]] |
| SPECIES_CHARIZARD_MEGA_X | [["EVO_MEGA","ITEM_NONE","SPECIES_CHARIZARD","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CHARIZARD_MEGA_Y | [["EVO_MEGA","ITEM_NONE","SPECIES_CHARIZARD","MEGA_VARIANT_STANDARD"]] |
| SPECIES_CHARJABUG | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_VIKAVOLT","0"]] |
| SPECIES_CINDERACE | [["EVO_GIGANTAMAX","TRUE","SPECIES_CINDERACE_GIGA","0"]] |
| SPECIES_CINDERACE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CINDERACE","0"]] |
| SPECIES_CLOBBOPUS | [["EVO_MOVE","MOVE_TAUNT","SPECIES_GRAPPLOCT","0"]] |
| SPECIES_COALOSSAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_COALOSSAL_GIGA","0"]] |
| SPECIES_COALOSSAL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_COALOSSAL","0"]] |
| SPECIES_COMBEE | [["EVO_FEMALE_LEVEL","21","SPECIES_VESPIQUEN","0"]] |
| SPECIES_COPPERAJAH | [["EVO_GIGANTAMAX","TRUE","SPECIES_COPPERAJAH_GIGA","0"]] |
| SPECIES_COPPERAJAH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_COPPERAJAH","0"]] |
| SPECIES_CORVIKNIGHT | [["EVO_GIGANTAMAX","TRUE","SPECIES_CORVIKNIGHT_GIGA","0"]] |
| SPECIES_CORVIKNIGHT_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_CORVIKNIGHT","0"]] |
| SPECIES_COSMOEM | [["EVO_LEVEL_DAY","53","SPECIES_SOLGALEO","0"],["EVO_LEVEL_NIGHT","53","SPECIES_LUNALA","0"]] |
| SPECIES_CRABRAWLER | [["EVO_MAP","MAPSEC_FROST_MOUNTAIN","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_ROUTE_8","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_BLIZZARD_CITY","SPECIES_CRABOMINABLE","0"],["EVO_MAP","MAPSEC_FROZEN_FOREST","SPECIES_CRABOMINABLE","0"]] |
| SPECIES_CUBONE | [["EVO_LEVEL_DAY","28","SPECIES_MAROWAK","0"],["EVO_LEVEL_NIGHT","28","SPECIES_MAROWAK_A","0"]] |
| SPECIES_CUBONE_A | [["EVO_LEVEL_NIGHT","28","SPECIES_MAROWAK_A","0"]] |
| SPECIES_DARTRIX | [["EVO_LEVEL_HOLD_ITEM","34","SPECIES_DECIDUEYE_H","ITEM_HISUI_ROCK"]] |
| SPECIES_DEWOTT | [["EVO_LEVEL_HOLD_ITEM","36","SPECIES_SAMUROTT_H","ITEM_HISUI_ROCK"]] |
| SPECIES_DIANCIE | [["EVO_MEGA","ITEM_DIANCITE","SPECIES_DIANCIE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_DIANCIE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_DIANCIE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_DIPPLIN | [["EVO_MOVE","MOVE_DRAGONCHEER","SPECIES_HYDRAPPLE","0"]] |
| SPECIES_DREDNAW | [["EVO_GIGANTAMAX","TRUE","SPECIES_DREDNAW_GIGA","0"]] |
| SPECIES_DREDNAW_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_DREDNAW","0"]] |
| SPECIES_DUNSPARCE | [["EVO_MOVE","MOVE_HYPERDRILL","SPECIES_DUDUNSPARCE","0"],["EVO_MOVE","MOVE_HYPERDRILL","SPECIES_DUDUNSPARCE_THREE","100"]] |
| SPECIES_DURALUDON | [["EVO_GIGANTAMAX","TRUE","SPECIES_DURALUDON_GIGA","0"]] |
| SPECIES_DURALUDON_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_DURALUDON","0"]] |
| SPECIES_EEVEE | [["EVO_MOVE_TYPE","TYPE_FAIRY","SPECIES_SYLVEON","TRUE"],["EVO_GIGANTAMAX","TRUE","SPECIES_EEVEE_GIGA","0"]] |
| SPECIES_EEVEE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_EEVEE","0"]] |
| SPECIES_ESPURR | [["EVO_MALE_LEVEL","25","SPECIES_MEOWSTIC","0"],["EVO_FEMALE_LEVEL","25","SPECIES_MEOWSTIC_FEMALE","0"]] |
| SPECIES_FARFETCHD_G | [["EVO_CRITICAL_HIT","0","SPECIES_SIRFETCHD","0"]] |
| SPECIES_FLAPPLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_FLAPPLE_GIGA","0"]] |
| SPECIES_FLAPPLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_FLAPPLE","0"]] |
| SPECIES_FOMANTIS | [["EVO_LEVEL_DAY","34","SPECIES_LURANTIS","0"]] |
| SPECIES_GALLADE | [["EVO_MEGA","ITEM_GALLADITE","SPECIES_GALLADE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GALLADE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GALLADE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARBODOR | [["EVO_GIGANTAMAX","TRUE","SPECIES_GARBODOR_GIGA","0"]] |
| SPECIES_GARBODOR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GARBODOR","0"]] |
| SPECIES_GARCHOMP | [["EVO_MEGA","ITEM_GARCHOMPITE","SPECIES_GARCHOMP_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARCHOMP_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GARCHOMP","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARDEVOIR | [["EVO_MEGA","ITEM_GARDEVOIRITE","SPECIES_GARDEVOIR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GARDEVOIR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GARDEVOIR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GENGAR | [["EVO_MEGA","ITEM_GENGARITE","SPECIES_GENGAR_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_GENGAR_GIGA","0"]] |
| SPECIES_GENGAR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GENGAR","0"]] |
| SPECIES_GENGAR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GENGAR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GIMMIGHOUL | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_GIMMIGHOUL_ROAMING | [["EVO_COINS","2999","SPECIES_GHOLDENGO","0"]] |
| SPECIES_GIRAFARIG | [["EVO_MOVE","MOVE_TWINBEAM","SPECIES_FARIGIRAF","0"]] |
| SPECIES_GLALIE | [["EVO_MEGA","ITEM_GLALITITE","SPECIES_GLALIE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GLALIE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GLALIE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GLIGAR | [["EVO_HOLD_ITEM_NIGHT","ITEM_RAZOR_FANG","SPECIES_GLISCOR","0"]] |
| SPECIES_GOOMY | [["EVO_LEVEL_HOLD_ITEM","40","SPECIES_SLIGGOO_H","ITEM_HISUI_ROCK"]] |
| SPECIES_GREAVARD | [["EVO_LEVEL_NIGHT","30","SPECIES_HOUNDSTONE","0"]] |
| SPECIES_GRIMMSNARL | [["EVO_GIGANTAMAX","TRUE","SPECIES_GRIMMSNARL_GIGA","0"]] |
| SPECIES_GRIMMSNARL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_GRIMMSNARL","0"]] |
| SPECIES_GROUDON | [["EVO_MEGA","ITEM_RED_ORB","SPECIES_GROUDON_PRIMAL","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_GROUDON_PRIMAL | [["EVO_MEGA","ITEM_NONE","SPECIES_GROUDON","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_GYARADOS | [["EVO_MEGA","ITEM_GYARADOSITE","SPECIES_GYARADOS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_GYARADOS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_GYARADOS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HAPPINY | [["EVO_HOLD_ITEM_DAY","ITEM_OVAL_STONE","SPECIES_CHANSEY","0"]] |
| SPECIES_HATTERENE | [["EVO_GIGANTAMAX","TRUE","SPECIES_HATTERENE_GIGA","0"]] |
| SPECIES_HATTERENE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_HATTERENE","0"]] |
| SPECIES_HERACROSS | [["EVO_MEGA","ITEM_HERACRONITE","SPECIES_HERACROSS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HERACROSS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_HERACROSS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HOUNDOOM | [["EVO_MEGA","ITEM_HOUNDOOMINITE","SPECIES_HOUNDOOM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_HOUNDOOM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_HOUNDOOM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_INTELEON | [["EVO_GIGANTAMAX","TRUE","SPECIES_INTELEON_GIGA","0"]] |
| SPECIES_INTELEON_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_INTELEON","0"]] |
| SPECIES_KANGASKHAN | [["EVO_MEGA","ITEM_KANGASKHANITE","SPECIES_KANGASKHAN_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_KANGASKHAN_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_KANGASKHAN","MEGA_VARIANT_STANDARD"]] |
| SPECIES_KINGLER | [["EVO_GIGANTAMAX","TRUE","SPECIES_KINGLER_GIGA","0"]] |
| SPECIES_KINGLER_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_KINGLER","0"]] |
| SPECIES_KYOGRE | [["EVO_MEGA","ITEM_BLUE_ORB","SPECIES_KYOGRE_PRIMAL","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_KYOGRE_PRIMAL | [["EVO_MEGA","ITEM_NONE","SPECIES_KYOGRE","MEGA_VARIANT_PRIMAL"]] |
| SPECIES_LAPRAS | [["EVO_GIGANTAMAX","TRUE","SPECIES_LAPRAS_GIGA","0"]] |
| SPECIES_LAPRAS_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_LAPRAS","0"]] |
| SPECIES_LATIAS | [["EVO_MEGA","ITEM_LATIASITE","SPECIES_LATIAS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIAS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LATIAS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIOS | [["EVO_MEGA","ITEM_LATIOSITE","SPECIES_LATIOS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LATIOS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LATIOS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LECHONK | [["EVO_MALE_LEVEL","18","SPECIES_OINKOLOGNE","0"],["EVO_FEMALE_LEVEL","18","SPECIES_OINKOLOGNE_FEMALE","0"]] |
| SPECIES_LICKITUNG | [["EVO_MOVE","MOVE_ROLLOUT","SPECIES_LICKILICKY","0"]] |
| SPECIES_LINOONE_G | [["EVO_LEVEL_NIGHT","35","SPECIES_OBSTAGOON","0"]] |
| SPECIES_LOPUNNY | [["EVO_MEGA","ITEM_LOPUNNITE","SPECIES_LOPUNNY_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LOPUNNY_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LOPUNNY","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LUCARIO | [["EVO_MEGA","ITEM_LUCARIONITE","SPECIES_LUCARIO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_LUCARIO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_LUCARIO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MACHAMP | [["EVO_GIGANTAMAX","TRUE","SPECIES_MACHAMP_GIGA","0"]] |
| SPECIES_MACHAMP_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MACHAMP","0"]] |
| SPECIES_MAGNETON | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_MAGNEZONE","0"]] |
| SPECIES_MANECTRIC | [["EVO_MEGA","ITEM_MANECTITE","SPECIES_MANECTRIC_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MANECTRIC_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MANECTRIC","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MANTYKE | [["EVO_OTHER_PARTY_MON","SPECIES_REMORAID","SPECIES_MANTINE","0"]] |
| SPECIES_MAWILE | [["EVO_MEGA","ITEM_MAWILITE","SPECIES_MAWILE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MAWILE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MAWILE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEDICHAM | [["EVO_MEGA","ITEM_MEDICHAMITE","SPECIES_MEDICHAM_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEDICHAM_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_MEDICHAM","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MELMETAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_MELMETAL_GIGA","0"]] |
| SPECIES_MELMETAL_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MELMETAL","0"]] |
| SPECIES_MEOWTH | [["EVO_GIGANTAMAX","TRUE","SPECIES_MEOWTH_GIGA","0"]] |
| SPECIES_MEOWTH_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_MEOWTH","0"]] |
| SPECIES_METAGROSS | [["EVO_MEGA","ITEM_METAGROSSITE","SPECIES_METAGROSS_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_METAGROSS_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_METAGROSS","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO | [["EVO_MEGA","ITEM_MEWTWONITE_X","SPECIES_MEWTWO_MEGA_X","MEGA_VARIANT_STANDARD"],["EVO_MEGA","ITEM_MEWTWONITE_Y","SPECIES_MEWTWO_MEGA_Y","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO_MEGA_X | [["EVO_MEGA","ITEM_NONE","SPECIES_MEWTWO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MEWTWO_MEGA_Y | [["EVO_MEGA","ITEM_NONE","SPECIES_MEWTWO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_MIME_JR | [["EVO_MOVE","MOVE_MIMIC","SPECIES_MR_MIME","0"]] |
| SPECIES_MIME_JR_G | [["EVO_MOVE","MOVE_MIMIC","SPECIES_MR_MIME_G","0"]] |
| SPECIES_NECROZMA_DAWN_WINGS | [["EVO_MEGA","ITEM_ULTRANECROZIUM_Z","SPECIES_NECROZMA_ULTRA","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_NECROZMA_DUSK_MANE | [["EVO_MEGA","ITEM_ULTRANECROZIUM_Z","SPECIES_NECROZMA_ULTRA","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_NECROZMA_ULTRA | [["EVO_MEGA","ITEM_NONE","SPECIES_NECROZMA_DUSK_MANE","MEGA_VARIANT_ULTRA_BURST"],["EVO_MEGA","ITEM_NONE","SPECIES_NECROZMA_DAWN_WINGS","MEGA_VARIANT_ULTRA_BURST"]] |
| SPECIES_NOSEPASS | [["EVO_MAP","MAPSEC_THUNDERCAP_MOUNTAIN","SPECIES_PROBOPASS","0"]] |
| SPECIES_ORBEETLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_ORBEETLE_GIGA","0"]] |
| SPECIES_ORBEETLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_ORBEETLE","0"]] |
| SPECIES_PANCHAM | [["EVO_TYPE_IN_PARTY","32","SPECIES_PANGORO","TYPE_DARK"]] |
| SPECIES_PETILIL | [["EVO_ITEM_HOLD_ITEM","ITEM_SUN_STONE","SPECIES_LILLIGANT_H","ITEM_HISUI_ROCK"]] |
| SPECIES_PIDGEOT | [["EVO_MEGA","ITEM_PIDGEOTITE","SPECIES_PIDGEOT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PIDGEOT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_PIDGEOT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PIKACHU | [["EVO_ITEM_LOCATION","ITEM_THUNDER_STONE","SPECIES_RAICHU_A","MB_SHALLOW_WATER"],["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_BELLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_ALOLA | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_HOENN | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_KALOS | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_ORIGINAL | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_PARTNER | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_SINNOH | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_CAP_UNOVA | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_COSPLAY | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_FLYING | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_PIKACHU","0"]] |
| SPECIES_PIKACHU_LIBRE | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_PHD | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_POP_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_ROCK_STAR | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PIKACHU_SURFING | [["EVO_GIGANTAMAX","TRUE","SPECIES_PIKACHU_GIGA","0"]] |
| SPECIES_PILOSWINE | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_MAMOSWINE","0"]] |
| SPECIES_PINSIR | [["EVO_MEGA","ITEM_PINSIRITE","SPECIES_PINSIR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_PINSIR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_PINSIR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_POIPOLE | [["EVO_MOVE","MOVE_DRAGONPULSE","SPECIES_NAGANADEL","0"]] |
| SPECIES_PRIMEAPE | [["EVO_MOVE","MOVE_RAGEFIST","SPECIES_ANNIHILAPE","0"]] |
| SPECIES_QUILAVA | [["EVO_LEVEL_HOLD_ITEM","36","SPECIES_TYPHLOSION_H","ITEM_HISUI_ROCK"]] |
| SPECIES_QWILFISH_H | [["EVO_MOVE","MOVE_BARBBARRAGE","SPECIES_OVERQWIL","0"]] |
| SPECIES_RATTATA_A | [["EVO_LEVEL_NIGHT","20","SPECIES_RATICATE_A","0"]] |
| SPECIES_RAYQUAZA | [["EVO_MEGA","MOVE_DRAGONASCENT","SPECIES_RAYQUAZA_MEGA","MEGA_VARIANT_WISH"]] |
| SPECIES_RAYQUAZA_MEGA | [["EVO_MEGA","MOVE_NONE","SPECIES_RAYQUAZA","MEGA_VARIANT_WISH"]] |
| SPECIES_RILLABOOM | [["EVO_GIGANTAMAX","TRUE","SPECIES_RILLABOOM_GIGA","0"]] |
| SPECIES_RILLABOOM_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_RILLABOOM","0"]] |
| SPECIES_ROCKRUFF | [["EVO_LEVEL_DAY","25","SPECIES_LYCANROC","0"],["EVO_LEVEL_NIGHT","25","SPECIES_LYCANROC_N","0"],["EVO_LEVEL_SPECIFIC_TIME_RANGE","25","SPECIES_LYCANROC_DUSK","TIME_RANGE(17, 20)"]] |
| SPECIES_RUFFLET | [["EVO_LEVEL_HOLD_ITEM","50","SPECIES_BRAVIARY_H","ITEM_HISUI_ROCK"]] |
| SPECIES_SABLEYE | [["EVO_MEGA","ITEM_SABLENITE","SPECIES_SABLEYE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SABLEYE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SABLEYE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SALAMENCE | [["EVO_MEGA","ITEM_SALAMENCITE","SPECIES_SALAMENCE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SALAMENCE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SALAMENCE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SALANDIT | [["EVO_FEMALE_LEVEL","33","SPECIES_SALAZZLE","0"]] |
| SPECIES_SANDACONDA | [["EVO_GIGANTAMAX","TRUE","SPECIES_SANDACONDA_GIGA","0"]] |
| SPECIES_SANDACONDA_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_SANDACONDA","0"]] |
| SPECIES_SCEPTILE | [["EVO_MEGA","ITEM_SCEPTILITE","SPECIES_SCEPTILE_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCEPTILE_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SCEPTILE","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCIZOR | [["EVO_MEGA","ITEM_SCIZORITE","SPECIES_SCIZOR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SCIZOR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SCIZOR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SHARPEDO | [["EVO_MEGA","ITEM_SHARPEDONITE","SPECIES_SHARPEDO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SHARPEDO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SHARPEDO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SLIGGOO | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA","0"]] |
| SPECIES_SLIGGOO_H | [["EVO_RAINY_FOGGY_OW","50","SPECIES_GOODRA_H","0"]] |
| SPECIES_SLOWBRO | [["EVO_MEGA","ITEM_SLOWBRONITE","SPECIES_SLOWBRO_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SLOWBRO_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SLOWBRO","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SNEASEL | [["EVO_HOLD_ITEM_NIGHT","ITEM_RAZOR_CLAW","SPECIES_WEAVILE","0"]] |
| SPECIES_SNEASEL_H | [["EVO_HOLD_ITEM_DAY","ITEM_RAZOR_CLAW","SPECIES_SNEASLER","0"]] |
| SPECIES_SNORLAX | [["EVO_GIGANTAMAX","TRUE","SPECIES_SNORLAX_GIGA","0"]] |
| SPECIES_SNORLAX_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_SNORLAX","0"]] |
| SPECIES_STANTLER | [["EVO_MOVE","MOVE_PSYSHIELDBASH","SPECIES_WYRDEER","0"]] |
| SPECIES_STEELIX | [["EVO_MEGA","ITEM_STEELIXITE","SPECIES_STEELIX_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_STEELIX_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_STEELIX","MEGA_VARIANT_STANDARD"]] |
| SPECIES_STEENEE | [["EVO_MOVE","MOVE_STOMP","SPECIES_TSAREENA","0"]] |
| SPECIES_SWAMPERT | [["EVO_MEGA","ITEM_SWAMPERTITE","SPECIES_SWAMPERT_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_SWAMPERT_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_SWAMPERT","MEGA_VARIANT_STANDARD"]] |
| SPECIES_TANDEMAUS | [["EVO_MAUSHOLD_THREE","25","SPECIES_MAUSHOLD","0"],["EVO_MAUSHOLD_FOUR","25","SPECIES_MAUSHOLD_FOUR","0"]] |
| SPECIES_TANGELA | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_TANGROWTH","0"]] |
| SPECIES_TOXEL | [["EVO_NATURE_HIGH","30","SPECIES_TOXTRICITY","0"],["EVO_NATURE_LOW","30","SPECIES_TOXTRICITY_LOW_KEY","0"]] |
| SPECIES_TOXTRICITY | [["EVO_GIGANTAMAX","TRUE","SPECIES_TOXTRICITY_GIGA","0"]] |
| SPECIES_TOXTRICITY_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_TOXTRICITY","0"]] |
| SPECIES_TOXTRICITY_LOW_KEY | [["EVO_GIGANTAMAX","TRUE","SPECIES_TOXTRICITY_LOW_KEY_GIGA","0"]] |
| SPECIES_TOXTRICITY_LOW_KEY_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_TOXTRICITY_LOW_KEY","0"]] |
| SPECIES_TYRANITAR | [["EVO_MEGA","ITEM_TYRANITARITE","SPECIES_TYRANITAR_MEGA","MEGA_VARIANT_STANDARD"]] |
| SPECIES_TYRANITAR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_TYRANITAR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_TYRUNT | [["EVO_LEVEL_DAY","39","SPECIES_TYRANTRUM","0"]] |
| SPECIES_URSARING | [["EVO_ITEM_NIGHT","ITEM_PEAT_BLOCK","SPECIES_URSALUNA","0"]] |
| SPECIES_URSHIFU_RAPID | [["EVO_GIGANTAMAX","TRUE","SPECIES_URSHIFU_RAPID_GIGA","0"]] |
| SPECIES_URSHIFU_RAPID_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_URSHIFU_RAPID","0"]] |
| SPECIES_URSHIFU_SINGLE | [["EVO_GIGANTAMAX","TRUE","SPECIES_URSHIFU_SINGLE_GIGA","0"]] |
| SPECIES_URSHIFU_SINGLE_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_URSHIFU_SINGLE","0"]] |
| SPECIES_VENUSAUR | [["EVO_MEGA","ITEM_VENUSAURITE","SPECIES_VENUSAUR_MEGA","MEGA_VARIANT_STANDARD"],["EVO_GIGANTAMAX","TRUE","SPECIES_VENUSAUR_GIGA","0"]] |
| SPECIES_VENUSAUR_GIGA | [["EVO_GIGANTAMAX","FALSE","SPECIES_VENUSAUR","0"]] |
| SPECIES_VENUSAUR_MEGA | [["EVO_MEGA","ITEM_NONE","SPECIES_VENUSAUR","MEGA_VARIANT_STANDARD"]] |
| SPECIES_YANMA | [["EVO_MOVE","MOVE_ANCIENTPOWER","SPECIES_YANMEGA","0"]] |
| SPECIES_YUNGOOS | [["EVO_LEVEL_DAY","20","SPECIES_GUMSHOOS","0"]] |

Recognized rows whose nonzero auxiliary field is zeroed:

| Local parent | Row |
| --- | --- |
| SPECIES_SNORUNT | [["EVO_ITEM","ITEM_DAWN_STONE","SPECIES_FROSLASS","MON_FEMALE"]] |

Core audited source SHA-256s:

| Source owner | SHA-256 |
| --- | --- |
| 02_external/CFRU-expansion/src/Tables/battle_moves.c | 0f9e024e3e40cfa265ffddf663de72e0cabfd7a41e54edf6f9c0e28b56541047 |
| 02_external/CFRU-expansion/src/Tables/level_up_learnsets.c | fe6f670a6ff2abcdf4059c72500909bab4b5ce6c08c7186372f22c870a07545f |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/include/abilities.h | 9d866db85216091b8018cda7af544d92dcc5624fc5192fbf4fe5238ed7281953 |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/include/evolution.h | c40ab5de94d26a0fe2c54dc1ef16f01e0b374850afad481d7aa61e76a989f159 |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c | 79b6fcb057b719c28246b92d1bff088ab5293c69df8067afe2a5f386d2784026 |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Egg_Moves.c | dce5b82b0f3590494a182a2d5a50dd7f591a1bbf384ee85b4fb6c939d787a889 |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Evolution Table.c | 04c839474c547813afd7164fe7cee159ded80d5a5acd6ee82272a6c6d35ad3bb |
| 02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c | 86176d7df43e684f11f9506e73a4216a96af79c910c878fe6d9bf2924054d47a |
