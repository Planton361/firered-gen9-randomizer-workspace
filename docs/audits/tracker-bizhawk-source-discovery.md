# Post-freeze Ironmon Tracker / BizHawk design

Date: 2026-09-15. **Design and compile-only source checks; no live support claim.**
No ROM/save/state, local address manifest, build symbol file, emulator, tool
binary download or private artifact was accessed. No Tracker-core, extension
runtime or engine implementation is changed. Existing diagnostics are not an
exact-revision profile and must not be promoted to live support as-is.

## Source identity and current-source reconciliation

| Source | Workspace pin | Public current ref inspected |
|---|---|---|
| Workspace extension | `7437cd551545ab5e4dcd57a2ff5dbf9672193d74` | `origin/main` same revision |
| CFRU pilot | `827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec` | Pilot compatibility head unchanged. Default Experiments is `0cf50941320975e5754e3a545dff0ee3a54d98ac`, NOT the pilot. Candidate #46 `94404bcebd92f3817da0d03963cc536d7b7f44c3` has unchanged struct headers. |
| DPE pilot | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | Pilot compatibility head unchanged. Default master is `0528450c7a95bd517df7ebc9e0f2bb00a06f0162`, NOT substituted for pilot. |
| Ironmon Tracker | `c450ecaee2d8131a2789bb656e3be792a93712fb` | Fetched `main`: `41e671124fbc1e944480adfe62fc62dac26fd5b8` |
| NatDexExtension | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | Configured `dev_new`: `c5c3f1f25c7d8e9876c613988dd90d384a8b3d8a`; default `main`: `46c0e12c50010c614af93d8674462495cc364b61` |
| BizHawk | Not pinned by workspace | Public HEAD `44417b1adbd5376cf0622e07ba8ba9841680f07e`; inspected Lua memory API and mGBA memory-domain implementation, not a downloaded emulator. |

Tracker's relevant Memory/GameSettings/TrackerAPI/PokemonData/MoveData files
are unchanged between workspace pin and current main. Program's relevant diff
only switches trainer IV reads from u16 to the low byte, with explanation; it
does not add CFRU custom-row support. NatDex main/dev_new extension source is
identical; compared with the pinned extension it updates version 1.2.0→1.2.1,
minimum advertised Tracker v8.5.0→v9.3.0 and some display names, not CFRU layouts.
Exact source comparisons therefore supersede historical compatibility notes.

## Compatibility gap matrix

Classifications are per sub-capability, not a blanket feature PASS. Every
enabled live read eventually also needs NEEDS_RUNTIME_VALIDATION on an exact
frozen revision and emulator/core. Numeric values below are source layout
offsets/counts, not discovered private addresses.

| Area | Classification | Current source and precise work needed |
|---|---|---|
| Basic extension API / 8-,16-,32-bit little-endian reads | SUPPORTED_AS_IS | Tracker exposes hooks, file loaders and emulator-neutral read primitives. Reuse the read-only subset; availability is not profile correctness. [TrackerAPI][TAPI], [Memory][TM] |
| Revision detection | NEEDS_PROFILE | Stock GameSettings selects vanilla header/software-version addresses; BPRE is not CFRU revision identity. NatDex only tests its own count 1258 before loading its metadata header; target count is 1440 and target has no equivalent verified NatDex header. Never force NatDex detection true. [GameSettings][TGS], [NatDex][N] |
| Layout override import | NEEDS_DECODER_CHANGE | `importTrackerOverridesFromJson` iterates `globalInfo.Addresses` / `.Values` but assigns `globalObj[k]`; consumers read `globalObj.Addresses[k]` / `.Values[k]`. It can return true after xpcall error. A successful loader log does not prove applied offsets. Correct nested/transactional import needs its own test/PR. [GameSettings][TGS] |
| ROM bank/domain mapping | NEEDS_DECODER_CHANGE | `splitDomainAndAddress` maps high-byte 8 only to ROM; addresses in high-byte 9 fall through with nil domain. Expanded source insertion/UPR windows can be beyond 16 MiB. Handle the approved cartridge range as domain-relative offset with explicit range/size checks, never nil/default domain. [Memory][TM] |
| Species/forms identity | NEEDS_PROFILE | Target IDs 0..1439 differ from NatDex's 1258-entry ID space. Map internal ID→National Dex→form separately, preserve holes/egg/placeholders and encounter-safe vs transition-only forms. Do not blindly reuse NatDex icon filenames or linked-ability groups. [DPE species][DS], [NatDex][N] |
| Species names/types/icons | NEEDS_PROFILE | Source-derived macro fallback names are not authoritative display strings or a complete icon pack. Use target text/name tables and explicitly mapped legal assets; unknown icon falls back to a labeled placeholder. Tracker Fairy is 0x12, CFRU Fairy 0x17; Stellar 0x18 and pseudo-types require explicit display policy. [PokemonData][TP], [CFRU structs][CP] |
| Moves and category | NEEDS_DECODER_CHANGE | Count 992, 12-byte rows. CFRU split byte is +10 with 0/1/2 physical/special/status. Stock reads flags at +8, bits6..7 and maps 1/2/3. Changing an offset alone does not fix category indexing. Supply explicit decoder and target names/effect caveats; no new move effects. [MoveData][TMD], [CFRU structs][CP] |
| Ability tables / names | NEEDS_PROFILE | IDs 0..254, 33 aliases; target name rows 16+terminator with species-context overrides. A global name/description by ID is insufficient. Do not import NatDex's >255 ability numbering or modern effects. [CFRU naming][CN] |
| Hidden ability and selected party ability | NEEDS_DECODER_CHANGE | Base row normal slots at 0x16/0x17, hidden at 0x1A. Stock reads two slots and treats misc bit31 as normal alternate ability. CFRU uses that bit as hidden; otherwise personality parity selects ability1/2, with ability2 NONE fallback. Decode target's exact `GetMonAbility`; distinguish party ability from temporary battle ability. [PokemonData][TP], [build_pokemon][CB] |
| Expanded Pokemon struct / player party | NEEDS_STRUCT_LAYOUT_CHANGE | Size remains 0x64 (not a bigger stride), but fields/semantics differ: direct ordered growth/attacks/etc; backupSpecies/tera fields; no vanilla XOR/permutation. `bytereplacement` active Decryption block and direct C access establish intended source behavior; final insertion still needs runtime verification. Stock Program always XORs and permutes. New dedicated decoder, not just size override. [Program][TG], [CFRU patches][CX], [CFRU structs][CP] |
| Enemy party / active battle rows | NEEDS_STRUCT_LAYOUT_CHANGE | Enemy party uses same Pokemon decoder. BattlePokemon remains 0x58, but +0x18 is type3 and statStages begin +0x19 (stock begins +0x18). Ability +0x20, types +0x21/+0x22, item +0x2E, status +0x4C/+0x50. Separate battle and party layouts. [CFRU structs][CP], [Battle][TB] |
| Battle identity / event timing / trainers | NEEDS_PROFILE | gBattlersCount, gBattleMons, gBattlerPartyIndexes (u16), gBattleTypeFlags, opponent A/B, callbacks/script addresses and changed ABI must be exact profile symbols. Stock battle/ability tracking compares script pointers; replacing table addresses alone is insufficient. Party indexes 0..5 and battler banks 0..3 validated; do not infer active battle from plausible leftover rows. [Battle][TB] |
| Base Stats | NEEDS_PROFILE | Six stats/typing within 28-byte row structurally agree; addresses/counts/randomized values need exact profile. Add third ability; source metadata only fallback when actual runtime data unknown. [CFRU structs][CP], [DPE stats][DB] |
| Trainer header | SUPPORTED_AS_IS | 40-byte header layout and party pointer +0x24 agree structurally; target table identity and trainer IDs still NEEDS_PROFILE. Do not confuse header agreement with party-row agreement. [CFRU trainer][CT], [Program][TG] |
| Trainer party rows | NEEDS_STRUCT_LAYOUT_CHANGE | Flags0/2: 8 bytes; flag1:16; flag3:32 with ability6, nature7, six IVs8..13, six EVs14..19, item20, moves22..29, tera30. Stock shares one 16-byte custom stride for flags1/3 and item6/moves8. Need flag-specific layouts and richer fields, not a global custom stride=32. [CFRU trainer][CT], [Program][TG] |
| Level-up learnsets | NEEDS_DECODER_CHANGE | Pointer table entries remain4 bytes; records are move u16 LE + level u8, stride3, END 00 00 FF. Stock `Memory.getReadFunc(3)` returns readword (2 bytes); setting stride3/bit widths still loses level/END. Explicit byte+word decoder, bounded scan and fail-closed missing terminator required. [PokemonData][TP], [Memory][TM] |
| Items / bag | NEEDS_PROFILE | DPE source count799 vs CFRU constants779 is an explicit current conflict, not license to read max(counts). `struct Item`44 bytes, inline name14, itemId14, price16, pocket26. Resolve active table/capacity ownership per frozen profile and unknown high IDs safely. Bag pointer/pocket/counter/encryption policy is a separate read gate; do not assume Pokemon decryption patches disable bag encryption. [Item][CI], [source data][WS] |
| Map/location state | NEEDS_PROFILE | Tracker keys routes by gMapHeader.mapLayoutId (+0x12), not National Dex-style map-group/number. CFRU same header offset; use exact map/header identity and explicit layoutId↔group/number/region mapping. Pallet/Parcel/Bill overlays change state, not necessarily layout IDs. Trainer defeated flags and renewal groups require target mapping. [RouteData][TR], [Program][TG] |
| Live profile activation, menus/warp/battle/party transitions | NEEDS_RUNTIME_VALIDATION | User-run, exact revision/core, no extension writes, bounded frame snapshots, stale-cache clearing; no result claimed this session. |
| Missing Gen9 battle mechanics / transform correctness / damage predictor completeness | OUT_OF_SCOPE | Preserve CFRU/DPE baseline and M-010 limits. Display does not imply implementing modern battle mechanics or full predictive support. |
| ROM/save/state parsing, emulator installation/automation, quickload/poke/patch features | OUT_OF_SCOPE | No access or implementation in this task. Do not auto-enable stock memory-write features through the new profile. |

## Verified layouts, not guessed sizeof values

`07_scripts/tracker/check_pilot_struct_layouts.c` contains compile-time assertions
against real target headers. Run with an existing ARM toolchain and an isolated
exact CFRU source checkout:

```sh
arm-none-eabi-gcc -mthumb -mcpu=arm7tdmi -march=armv4t -std=c11 -Wall -Wextra -fsyntax-only -I /path/to/cfru 07_scripts/tracker/check_pilot_struct_layouts.c
```

PASS against candidate `94404bcebd92f3817da0d03963cc536d7b7f44c3`; relevant headers
are unchanged from pilot pin. No link, output binary or memory input. Assertions
cover Pokemon100/Box80/Battle88/BaseStats28/Move12/Trainer40, all four trainer
row variants, packed learnset3, Item44 and MapHeader28/+0x12. Bitfield semantics
still need synthetic decode tests and live verification; sizeof alone does not
prove hidden-ability selection or inserted decryption patches.

Party direct offsets verified: species0x20, item0x22, experience0x24, moves0x2C,
PP0x34, EVs0x38, status0x50, level0x54, HP0x56, maxHP0x58. Expanded PC storage
also has `CompressedPokemon` paths; a future all-boxes reader must not assume
14×30 vanilla BoxPokemon rows. PC enumeration is deferred from first party-only
profile until the active compression/storage mode is source-verified.

## BizHawk integration boundary

The current Lua API accepts explicit memory domains for little-endian reads.
Its byte-array APIs have different indexing conventions (array 1-based versus
dictionary/domain-relative); adapters must normalize before decoding. Reuse
existing Tracker wrappers where correct; avoid changing a global selected domain.
[MemoryLuaLibrary][BM]

The inspected mGBA core exposes EWRAM (256 KiB), IWRAM (32 KiB), ROM and System
Bus as distinct domains. A full CPU address is not a ROM-domain offset. Validate
the actual core's domain names/sizes at activation and every span read; reject
unsupported cores instead of assuming another core's mapping. Keep all profile
operations read-only, including error/teardown paths. [mGBA domains][BD]

No decision to install/run BizHawk on this Mac is made. The tracker project's
documented platform support and core/API availability are a separate user setup
gate; a current source API is not a tested emulator version. [Tracker README][TRE]

## Existing workspace extension is diagnostics only

[CFRUDPEExtension][WE] loads source counts and optional ignored local manifests.
Its gBattleMons helper reads only left player/opponent rows and uses plausible
field checks; battler-count gating is optional. `manifestsLoaded` means either
loader succeeded, not all prerequisites. It neither verifies an exact revision
nor replaces stock team decoding. `beforeGameDataLoad` only prepares paths;
`startup` does the imports, which is too weak a contract for an atomic verified
profile. Existing helpers can supply reusable formatting, not activation proof.

Do not run the local offsets/symbol generators, read .local.json files or
invent missing addresses. Historical loader/battle diagnostic smoke does not
prove current party, trainers, full battle events, map state or final data names.

## Fail-closed revision profile design

Each immutable public profile describes: schema version; profile ID; exact
workspace/CFRU/DPE/UPR data-contract SHAs; Tracker API/version range; emulator/core
domain contract; feature capabilities; table counts/strides/name encodings;
decoder names; source-symbol names; permitted source/config variations; explicit
disabled functions; and expected source-owned revision evidence. Private address
manifests stay user-owned/ignored and are never requested or published here.

State progression: DISABLED → CANDIDATE_METADATA → VERIFIED_REVISION →
VERIFIED_LAYOUT → ACTIVE_READ_ONLY. Any error, reset/reload, profile switch,
unexpected schema or contradictory signature returns to DISABLED and clears
all derived party/battle/location/UI caches and override state.

- Loading a file, selecting a profile, seeing BPRE, or reading count1440 is not
  revision verification. A frozen source identity plus explicitly approved
  revision-specific public evidence is required. No such complete profile is
  established here; automatic live activation remains disabled.
- Future source-owned identification metadata would need its own authorization
  and reviewed source contract; this design does not add an engine marker or
  inspect a private ROM to discover one. If exact identity cannot be proved,
  only source-only metadata browsing is permitted, not live speculative reads.
- Separate layout identity from randomized content: a supported UPR run may
  alter species/moves/tables and pointers within approved ranges. Do not use
  randomized data values as a fixed build signature. Verify permitted writer
  contract and table spans; unknown UPR/source/config combination fails closed.
- Preflight all required symbols, domain ranges, alignments, bounds and schema
  without applying partial global overrides. Commit an all-or-nothing profile;
  compare effective nested reader settings after application. Roll back fully
  on any failure; errors cannot be transformed into loader success.
- Read counts/pointers with capability-specific limits before following them.
  Reject negative/non-integer/overflowed/truncated spans, invalid species/move/
  ability/item IDs, impossible party/battler sizes and absent learnset END.
  Unknown/placeholder identifiers display as unknown only where explicitly
  allowed, never silently as a different valid species.
- Battle activation requires verified battle state plus consistent bank/party
  indices, not plausible old gBattleMons memory. Sample coherently per frame,
  discard transition mismatches and prevent stale enemy data after battle.
- Treat data visibility separately from availability: opponent hidden ability,
  unrevealed moves and trainer parties must respect tracker challenge/spoiler
  settings. Do not expose all decoded information merely because readable.
- No memory writes, auto-downloads, ROM patching, quickload or external requests
  in the initial profile. Extension unload/reset restores previous in-process
  overrides and clears caches; it does not mutate game memory.

## Bounded implementation roadmap

One milestone/branch/PR per row; no engine mechanics; never merge automatically.

| Milestone | Deliverable / scope | ROM-free tests and gate |
|---|---|---|
| T01 | Repair nested override importer and failure propagation, no new live profile | Synthetic JSON/global tables; correct Addresses/Values, unknown/malformed keys, zero values, exception rollback, unchanged stock defaults. Independent source-only candidate, intentionally not implemented here. |
| T02 | Explicit safe cartridge-domain adapter + three-byte learnset decoder | Synthetic buffers: both ROM banks and boundary spans; LE move0x03DF/levels0,1,100; 00 00 FF END, truncated/no-END/invalid level/ID. Never set pointer stride to3; it stays4. |
| T03 | Immutable profile schema/atomic activation and source-derived ID/name/form inventory | Unknown revision, same-count wrong source, schema mismatch, one missing manifest, false loader success, changed UPR contract, reset/unload and no-write spies. Gate remains DISABLED without exact frozen identity evidence. |
| T04 | Dedicated CFRU party/ability decoder; read-only player panel first | Synthetic100-byte records at first/last party slots; personality parity, absent ability2, hidden bit/hidden NONE fallback, egg/invalid species, four moves/PP/status, no XOR/permutation; six-member bounds. Runtime player smoke after identity gate. |
| T05 | Flag-specific trainers + moves/types/names and battle decoder | Synthetic mixed flags0/1/2/3 arrays proving second-row alignment; full IV/EV/ability/item/moves; 0-based category; seven stages not type3; u16 party indices; no private symbol discovery. |
| T06 | Exact frozen addresses/event/map profile and gated battle UI | Source/public evidence or separately user-validated ignored metadata, never guessed addresses. Runtime capture/switch/faint/flee/double battle/warp/menu/reload and spoiler-visibility matrix; no stale data. |
| T07 optional | Full box/bag/advanced battle-details support | Separate source layout discovery (compressed PC, pockets/encryption, script triggers), then bounded synthetic and user runtime acceptance. Not prerequisite for first player-party profile. |

Stop at design now: no frozen integration revision or complete exact-revision
evidence exists; automatic activation and real-address changes would broaden
scope. T01/T02 are plausible independent source-only follow-ups, not a claim
that tracker support merely needs an offset file. This session adds only the
layout assertion test and this handoff, in a workspace documentation/test PR.

[TAPI]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/TrackerAPI.lua
[TM]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/Memory.lua
[TGS]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/GameSettings.lua
[TG]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/Program.lua
[TP]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/data/PokemonData.lua
[TMD]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/data/MoveData.lua
[TB]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/Battle.lua
[TR]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/ironmon_tracker/data/RouteData.lua
[TRE]: https://github.com/besteon/Ironmon-Tracker/blob/41e671124fbc1e944480adfe62fc62dac26fd5b8/README.md
[N]: https://github.com/CyanSMP64/NatDexExtension/blob/c5c3f1f25c7d8e9876c613988dd90d384a8b3d8a/NatDexExtension.lua
[CP]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/include/pokemon.h
[CB]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/src/build_pokemon.c
[CT]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/include/battle.h
[CI]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/include/item.h
[CX]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/bytereplacement
[CN]: https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/src/ability_util.c
[DS]: https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/include/species.h
[DB]: https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9/blob/22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc/src/Base_Stats.c
[WE]: ../../03_tools/tracker-extensions/CFRUDPEExtension/CFRUDPEExtension.lua
[WS]: ../../03_tools/tracker-extensions/CFRUDPEExtension/data/source-data.json
[BM]: https://github.com/TASEmulators/BizHawk/blob/44417b1adbd5376cf0622e07ba8ba9841680f07e/src/BizHawk.Client.Common/lua/CommonLibs/MemoryLuaLibrary.cs
[BD]: https://github.com/TASEmulators/BizHawk/blob/44417b1adbd5376cf0622e07ba8ba9841680f07e/src/BizHawk.Emulation.Cores/Consoles/Nintendo/GBA/MGBAHawk.IMemoryDomains.cs
