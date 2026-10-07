# Tracker / BizHawk architecture

**TRACKER_ARCHITECTURE_REBASELINED — T0, source/documentation evidence only.**
Contract: [#688](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/688),
under [#499](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/499)
and successor [#500](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/500).
Reviewed on 2026-10-07 on macOS without ROMs, emulator execution, saves, states,
builds, tool binaries or local address manifests. Implementation and runtime
acceptance remain **INTENDED FUTURE STATE**. This marker does not close #499/#500.

## Locked basis and authority

**CONFIRMED CURRENT STATE:** the inspected Workspace HEAD/tree and checked-out
Gitlinks match the Issue's locked pilot. These are the analysis base, not a
claim that the later documentation commit was runtime-tested.

| Component | Exact revision |
| --- | --- |
| Workspace base | `3bdfe9919afc0b7bea55c79f37285e832be495c3` |
| Workspace base tree | `f6bc65355811d7de153a91091b223fec9b50991e` |
| CFRU | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| DPE | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR-FVX | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` — v9.3.1 |
| NatDexExtension reference | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` — source declares v1.2.0 |

The current #499/#500/#688 contracts and their 2026-10-07 CONTROL clarifications
establish this lock and the Mac preparation exception. Older component pins,
M-014-pending statements and linear runtime-first scheduling in the general
canonical documents describe earlier evidence; they are not the Tracker lock.
This bounded task does not rewrite those files or historical status records.
Reference branch labels such as `main`/`dev_new` are not version selectors.

## Target architecture

**CONFIRMED USER DECISION:** use normal Ironmon Tracker with the separate,
workspace-owned [CFRUDPEExtension](../../03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua).
The extension reads emulator memory only. It owns profile validation, CFRU/DPE
decoding, data/resource adaptation and field confidence. No component changes,
Gitlink updates, NatDex dependency, engine metadata insertion or Tracker fork
are authorized by T0. A demonstrated extension limitation requires a separate
CONTROL decision before any core fork.

The flow is: pinned public source -> deterministic source profile -> validated
local runtime binding -> extension readers -> field confidence -> standard
Tracker presentation. [PROFILE_CONTRACT.md](PROFILE_CONTRACT.md) defines the
identity, manifest and fail-closed rules. Source data supplies identifiers and
baseline semantics; the selected randomized output and live RAM supply mutable
values. Source base stats or ability assignments must not overwrite randomized
values under the label of live game data.

## Tracker and BizHawk reference expectations

These facts are bound to the Tracker pin, not to the latest upstream release.
[Main.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/Main.lua)
(`Main.Version`, `GetBizhawkVersion`, `Run`, `SetupEmulatorInfo`) and the pinned
[README](../../02_external/Ironmon-Tracker/README.md) establish v9.3.1 and a
BizHawk minimum of 2.8. The version classifier distinguishes 2.8, 2.9 and
2.10+/future releases; accepting a version string is not compatibility evidence.
The README identifies Lua 5.1 for 2.8 and Lua 5.4 for 2.9, and requires extension
syntax compatible with both. No exact Linux BizHawk patch version, GBA core or
Lua engine setting has yet been accepted for this pilot: **UNKNOWN**, to record
in B1. No source-backed requirement for a particular NLua/LuaInterface switch
was established in this review; do not invent one.

[Memory.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/Memory.lua)
maps `read8/read16/read32` (also `readbyte/readword/readdword`) to BizHawk
`memory.read_u8/read_u16_le/read_u32_le(address, domain)`. It splits absolute
GBA addresses into BIOS/EWRAM/IWRAM/ROM domains for high bytes 0/2/3/8.
Unrecognized domains fall through; the extension must reject them before reads.
Little-endian width, bounds, alignment and pointer indirection are profile facts.

The host must provide `client.getversion`, `emu.frameadvance`, console/script
loading, `event.onexit/onconsoleclose`, and the Tracker's normal `client`,
`gui`, `forms`, input/joypad services. See `Main.Run`,
[Program.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/Program.lua)
and [Drawing.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/Drawing.lua).
B1 establishes host reads/frame operation; later T2/T5/T6 prove extension
lifecycle and presentation. Standalone mGBA's text-only Tracker path is not
substitute BizHawk acceptance and is not run on Mac for this task.

The host itself has optional memory-writing behavior:
`Program.changeGameSettingForLR` calls `Memory.writebyte` when
`Options["Override Button Mode to LR"]` is enabled. The accepted read-only
integration must disable that option and exclude other memory-mutating helpers;
T2/T6 must verify no write path is invoked. The presence of write functions in
the host API does not authorize the extension to use them.

## API and lifecycle seams

**CONFIRMED CURRENT STATE:** `Main.Run` initializes Memory, loads extensions,
calls `beforeGameDataLoad`, then `GameSettings.initialize`, then the remaining
module initializers, and only then extension startups. Thus `startup` alone is
too late to protect initial table reads. The following is the selected future
integration contract, using
[CustomCode.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/CustomCode.lua)
and [TrackerAPI.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua).

| Seam | Intended responsibility / limitation |
| --- | --- |
| `beforeGameDataLoad` | Install one reversible `GameSettings.initialize` guard, restricted to profile/address initialization. Validate before any dependent stock data initialization. |
| `TrackerAPI.loadGameSettingsFromJson` | Import an already validated address manifest; check effective GameSettings values, including `pstats`/`estats` aliases for the parties. |
| `TrackerAPI.loadTrackerOverridesFromJson` | Transport only; its return value does not establish effective nested overrides or schema validity. Use an extension-owned allowlisted adapter as described below. |
| `startup` | Confirm early activation, populate explicit source ID/resource tables and rebuild only validated data readers. Enabling mid-session requires clean restart through the early guard. |
| `afterProgramDataUpdate` | Publish a validated player-party snapshot; documented cadence is 30 frames, with forced updates also possible. |
| `afterBattleDataUpdate` | Publish current battle fields only after the extension's own context/layout gate; host battle state alone is insufficient. |
| `afterBattleBegins/afterBattleEnds` | Invalidate previous battle rows/context; begin a new sampling epoch or clear on exit. |
| `afterEachFrame/afterRedraw` | Lightweight invalidation/presentation only; no repeated parsing or table reconstruction. |
| `unload` | Restore owned wrappers/settings, clear snapshots and request `Main.forceRestart` when shared tables were mutated. Never resume stock interpretation of an unverified CFRU/DPE session. |

Lookup APIs `getPlayerPokemon`, `getEnemyPokemon`, `getActiveBattlePokemon`,
`getPokemonInfo`, `getMoveInfo`, `getAbilityInfo`, `getItemName` are presentation
and inspection seams, not independent proof. `getActiveBattlePokemon` returns
Tracker party objects through `Battle.Combatants`; it is not a `gBattleMons`
reader. Trainer APIs delegate to static `Program.readTrainerGameData`.

**Confirmed adapter hazards:**
[GameSettings.lua](../../02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua)
imports both JSON `Addresses` and `Values` with `globalObj[k] = value`, while
consumers use `Program.Addresses`, `PokemonData.Addresses`, `MoveData.Addresses`
and nested values. Imports can also return `true` after caught internal errors,
and partial imports can leave old keys intact. T2 must validate transactionally,
snapshot affected globals, apply only allowlisted nested fields locally and
assert read-back at the actual consumer path. Do not fix Tracker core or rely
on the historical override generator's successful import message.

T3 needs an extension-owned party decoder at `Program.readNewPokemon` and a
guarded team-update adapter: stock `updatePokemonTeams` can retain old rows on
invalid reads and substitutes maximum enemy PP outside battle. T4 must adapt
the battle consumers; post-read hooks alone cannot prevent an earlier incorrect
stock read. T5 must gate all affected views and derived calculations. Exact
wrapper coverage is to be proved with mocked consumers in T2–T5; API sufficiency
for complete UI coverage remains **UNKNOWN**, not justification for a fork now.

## NatDex patterns to reuse and reject

At the pinned [NatDexExtension.lua](../../02_external/NatDexExtension/NatDexExtension.lua),
`beforeGameDataLoad`, `overrideGameSettingsInitialize`, `startup`,
`addUpdateNewData`, `overrideCoreTrackerFunctions` and `unload` demonstrate:
capturing/restoring function references, early GameSettings adaptation,
extension-local paths, explicit data/resource insertion, forced data rebuilds,
and restart after unloading global modifications. Reuse these patterns with
idempotence, ownership checks and rollback.

Do not copy `Memory.read32(0x08000170) == 1258`, the CyanSMP64 fixed metadata
slots, NatDex struct sizes, append-at-stock-end ID mappings, sprites, settings
paths or linked-species rules as CFRU/DPE truth. NatDex's original-initialize-first
wrapper and return-on-detection-failure are also insufficient for fail-closed
CFRU/DPE activation. Any coincidentally shared pointer slot requires independent
CFRU/DPE source provenance.

## Source findings and data ownership

| Surface | Rechecked locked source and consequence |
| --- | --- |
| IDs and types | DPE `include/{species,moves,abilities,items}.h`, CFRU `include/constants/*.h`, CFRU `include/pokemon.h` and DPE `include/base_stats.h`: species upper bound 1440, moves 992, abilities 255; bounds are not counts of supported unique forms. Preserve holes, zero sentinels and aliases. Fairy is `0x17`, Stellar `0x18`; no stock type-index assumption. |
| Names and baseline data | DPE `strings/Pokemon_Name_Table.string`, `src/Base_Stats.c`; CFRU `strings/{attack_name_table,ability_name_table,type_names}.string`, `src/Tables/{battle_moves,item_tables}.c`: public source inputs. Parse string encoding/ID association explicitly; macro-derived labels are not verified display names. Ability aliases do not prove modern battle mechanics. |
| Items | DPE defines 799 slots including shiny placeholders; CFRU constants define 779. `gItemData` is source-owned in CFRU `item_tables.c`. T1 must reconcile effective per-table coverage/configuration; neither number alone validates every held-item ID. |
| Player party | CFRU `include/pokemon.h`, `src/build_pokemon.c::GetMonAbility`, `src/util.c::GetAbility1/GetAbility2/GetHiddenAbility`: direct fields, hidden-ability bit, personality-based ordinary selector and `TryRandomizeAbility`. Stock `Program.readNewPokemon` uses XOR and shuffled substructures and a different selector. Equal row size cannot prove decoding compatibility. |
| Active battle | CFRU `include/pokemon.h::BattlePokemon` comments support row `0x58`, species `0x00`, moves `0x0C`, PP `0x24`, HP `0x28`, level `0x2A`, maxHP `0x2C`, item `0x2E`, ability `0x20`, types `0x21/0x22`, status `0x4C/0x50`. These are source layout facts, not runtime address acceptance. |
| Party/battler relation | CFRU `include/battle.h`: `gBattlerPartyIndexes` is `u16[]`, `gBattleTypeFlags` is `u32`, `gBattlersCount` is `u8`. `src/multi.c::MultiInitPokemonOrder` makes multi/partner slot interpretation context-dependent. No universal battler-index-to-party-slot equality. |
| Trainer/wild truth | CFRU `src/build_pokemon.c::BuildTrainerPartySetup/CreateNPCTrainerParty`, `src/wild_encounter.c::CreateWildMon`: enemies are constructed into `gEnemyParty`; flags/configuration can affect moves, levels and abilities. `gBattleMons` owns current active battle values. `gTrainers` supplies validated identity/context only, never final randomized team predictions. |
| Move category | CFRU `BattleMove` is 12 bytes with explicit `split` byte at `0x0A`. Tracker `MoveData.readMoveInfoFromMemory` extracts category bits from a selected byte. Use a validated CFRU adapter; a byte offset cannot be passed as a bit offset. |
| Base stats / trainer layout | `BaseStats.hiddenAbility` is at `0x1A`; `0x1C` row size needs explicit target ABI evidence. `Trainer` comments place the party pointer at `0x24`. Current expanded `TrainerMonItemCustomMoves` fields sum to `0x20` bytes under the GBA ABI, superseding the historical `0x1C` candidate; do not use native macOS pointer/bitfield layout to certify GBA structs. |
| Address provenance | CFRU/DPE `BPRE.ld`, `repointall`, CFRU `repoints`, `include/new/rom_locs.h`: distinguish public fixed symbols, pointer slots, repoint anchors and resolved targets. A source pointer slot is not the table it points to. |

## Existing workspace code disposition

No implementation is changed by T0. Module below means a responsibility within
the current single Lua file or its data/helper files.

| Existing module | Disposition for successors |
| --- | --- |
| Metadata, path helpers, hook shell | **Keep/repair (T2):** preserve workspace ownership and explicit `.local.json` paths; bind schema, pins and activation to the contract. Examples remain inert. |
| `loadSourceData`, ID/type/status lookup | **Repair (T1/T3):** today only table/count presence is required; no exact source identity validation. Preserve aliases and source provenance, replace fallback names/types as production truth. |
| `loadConfiguredManifests`, early hook, `startup` | **Supersede activation logic (T2):** today either import succeeding sets `manifestsLoaded`; early hook merely prepares paths. Require the complete capability dependency set before initial reads. |
| `safeRead`, `readBattlerPartySlot` | **Keep/repair (T4):** protected calls and `u16` stride are useful; add domain/range/layout/epoch checks. `pcall` success is not validity. |
| `readBattleMon`, `readActiveBattleMons`, context | **Repair (T4):** retain diagnostic baseline only. Today it reads two fixed left rows, optionally checks battler count and accepts species/level/maxHP plausibility; it can consume inherited GameSettings without manifest readiness and attach trainer A without a trainer-battle gate. |
| Diagnostic snapshots / `getActiveBattleMons` | **Keep diagnostic role; add gated UI adapter (T5):** current state does not feed normal Tracker teams/screens and has no field-level trust. |
| `unload` | **Repair (T2):** clears extension state today but does not undo GameSettings/override mutations. Restore ownership and restart shared tables. |
| `data/source-data.json`, source generator | **Supersede schema, retain parser evidence (T1):** existing metadata lacks exact revision binding, uses normalized macro names and count fallbacks, omits types/layouts; warnings alone are insufficient for required facts. |
| Example manifests and local generator helpers | **Retain as historical prototypes; repair separately under T1/T2.** Do not execute local address/build-input helpers in Mac ROM-free preparation. No existing local manifest is examined by T0. |

## Historical evidence reconciliation

The [extension design](../../01_docs/analysis/cfru-dpe-tracker-extension-design.md),
[memory/API map](../../01_docs/analysis/tracker-memory-api-map.md),
[source reference map](../../01_docs/analysis/tracker-source-reference-map.md),
[Lua inventory](../../01_docs/analysis/tracker-lua-source-inventory.md),
[manifest source map](../../01_docs/analysis/cfru-dpe-tracker-manifest-source-map.md)
and [runtime trainer analysis](../../01_docs/analysis/cfru-runtime-trainer-vs-tracker-slot.md)
remain supporting evidence. Their source references were rechecked above.

**LEGACY / OBSOLETE as current acceptance:** manual selection as sufficient
detection, optional detection hardening, successful imports as readiness,
stock fallback for seemingly compatible fields, macro labels as accurate names,
and the old expanded trainer-row `0x1C` candidate. The inventory's claim that no
simple species-name source was identified is superseded by the DPE string source.
The [layout analysis](../../01_docs/analysis/cfru-dpe-tracker-layout-overrides.md)
also conflates a move byte offset with a category bit offset; T3 must not reuse it.

The [historical battle smoke](../../08_tests/randomizer/cfru-dpe-gbattlemons-reader-smoke-results.md)
is `PASS_TARGETED_LOCAL_SMOKE_WITH_CAVEATS`, not locked-pilot/BizHawk/UI fidelity
evidence. Its statement that the reader lacks party-index/context reads predates
the current `u16`/context helpers. Its unproven fields, doubles and transition
coverage remain unproven. Historical Route-22 diagnostic hypotheses do not
reopen accepted ROM/randomizer work. Historical suggestions to add engine
metadata are deferred scope, not a T0–T6 dependency.

## Dependency and acceptance sequence

This is a dependency contract, not a duplicate daily queue. Operational status
stays in the Project/Issues. All successors below remain future work.

| Contract | Entry and exit evidence |
| --- | --- |
| [B1 #689](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/689) | After T0; **PENDING_LINUX_HOST / NOT_RUN**, not FAIL. User-owned boot/new game/input/save-reload/wild/trainer/Lua/read/frame smoke, exact BizHawk/core/settings. `BIZHAWK_LOCKED_PILOT_READY`; closes #499 only with accepted T0 and B1. No Tracker data correctness claim. |
| [T1 #690](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/690) | After T0 review/merge: Mac public-source generator and synthetic fixtures explicitly permitted before B1. Deterministic identity/mappings/layout manifest, missing required facts fail generation. `CFRUDPE_TRACKER_PROFILE_READY` is source-only. |
| [T2 #691](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/691) | T1 plus #499 acceptance for integration activation; any further Mac-only work needs explicit CONTROL disposition. Mocked lifecycle/identity/failure tests and later Linux load/unload smoke. `CFRUDPE_EXTENSION_PROFILE_ACTIVE`. |
| [T3 #692](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/692) | T2; species/move/ability/item/type and multi-slot player-party fidelity, Gen1/8/9/regional controls. `CFRUDPE_TRACKER_DATA_FIDELITY_READY`. No enemy/trainer acceptance yet. |
| [T4 #693](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/693) | T3; live parties/battle/context, transition clearing, supported doubles/multi mapping; owns future `docs/tracker/RUNTIME_CONTRACT.md`. `CFRUDPE_TRACKER_BATTLE_FIDELITY_READY`. |
| [T5 #694](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/694) | T4; normal Tracker views and derived values honor field trust, no stock/stale fallback. `IRONMON_TRACKER_CFRUDPE_UI_READY`. |
| [T6 #695](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/695) | T5 and #499 PASS; user-owned Control/Casual NatDex/IronMON NatDex E2E including randomized values, trainer +50%, forms, items, status, save/reload and battle transitions. Owns future `docs/tracker/ACCEPTANCE.md`. `IRONMON_TRACKER_LOCKED_PILOT_READY` closes #500 and makes #501 eligible; does not itself declare freeze. |

T0 validation is source inspection, pin/status/safety checks, document/link/scope
review and `git diff --check`. No runtime check is requested before the user
reports Linux access. Open runtime identity, ABI and UI questions are recorded
in the profile contract, not converted into implicit PASS.
