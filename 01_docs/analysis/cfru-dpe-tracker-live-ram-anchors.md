# CFRU/DPE Tracker Live RAM Anchors

## Executive summary

The current Tracker smoke result is expected: `source-data`, `game-addresses.local`, and `tracker-overrides.local` can load successfully while Player, Enemy, and Wild data still remain unreadable.

The primary blocker is live RAM anchoring. Ironmon Tracker's stock read path needs `pstats`, `estats`, `gBattleMons`, and several battle-state addresses to point at the running CFRU/DPE game. The current local address generator can load table/name symbols from local `offsets.ini`, but previous generator warnings showed the important live symbols `gPlayerParty`, `gEnemyParty`, and `gBattleMons` missing from that local symbol input. A loaded local manifest is therefore not proof that the required runtime anchors exist.

The secondary blocker is layout decoding. Ironmon Tracker's `Program.readNewPokemon` decodes vanilla Gen III encrypted/reordered party substructures. CFRU's `struct Pokemon` in `include/pokemon.h` is an expanded direct struct with fields such as `species`, `item`, `moves`, `pp`, `level`, `teraType`, `gigantamax`, and hidden-ability state exposed in source layout. Supplying only `pstats` / `estats` is unlikely to make the stock reader correct.

## Current smoke interpretation

| Smoke signal | What it proves | What it does not prove |
| --- | --- | --- |
| `source-data=loaded species=1440 moves=992 abilities=255 items=799` | The extension found committed source-derived ID/count data. | No live RAM, party, battle, or enemy data correctness. |
| `game-addresses.local=true` | `TrackerAPI.loadGameSettingsFromJson` returned true for the local file. | The file may still lack `pstats`, `estats`, `gBattleMons`, or battle-state anchors. |
| `tracker-overrides.local=true` | `TrackerAPI.loadTrackerOverridesFromJson` returned true for the local file. | The effective nested fields consumed by read paths still need local validation. |
| Player/Starter not recognized | Stock player-party read path is not producing valid Tracker Pokemon. | It does not distinguish missing address anchors from wrong CFRU Pokemon decoding by itself. |
| Wild battle not recognized | Battle status never reaches a usable active-battle state. | It does not prove wild generation failed; it can fail at Tracker address, party, or battle-status reads. |

## Tracker read paths

| Tracker file/function | Required anchors/layout | Source-backed behavior | Failure mode for CFRU/DPE |
| --- | --- | --- | --- |
| `Program.updatePokemonTeams` in `02_external/Ironmon-Tracker/ironmon_tracker/Program.lua` | `GameSettings.pstats`, `GameSettings.estats`, `Program.Addresses.sizeofPokemonStruct` | Iterates six slots, reads personality/OT ID, then calls `Program.readNewPokemon` for player and enemy teams. | Missing or wrong `pstats` / `estats` leaves teams empty or invalid. |
| `Program.readNewPokemon` in `Program.lua` | Vanilla Gen III party layout, `offsetPokemonSubstruct`, encrypted/reordered substructures | XORs substructure words with personality/OT key and extracts species, moves, EVs, ability number, stats, and other fields. | CFRU direct expanded `struct Pokemon` is not the same model, so correct addresses can still decode garbage. |
| `Battle.updateBattleStatus` in `02_external/Ironmon-Tracker/ironmon_tracker/Battle.lua` | `gBattlersCount`, `gBattleMons`, `gBattleOutcome`, `gBattleMainFunc`, enemy lead from `Tracker.getPokemon(1, false)` | Rejects fake battles when battler count is zero or first battle species is invalid; requires an opposing Pokemon and battle-main state before `dataReady`. | Missing `gBattleMons` / state anchors or an empty enemy team prevents active-battle detection. |
| `Program.getPokemonTypes` in `Program.lua` | `gBattleMons`, `sizeofBattlePokemon`, `offsetBattlePokemonTypes`, doubles partner offset | Reads active battle types directly from `gBattleMons`. | This can become useful once `gBattleMons` and layout offsets are trusted. |
| `TrackerAPI.getPlayerPokemon` / `getEnemyPokemon` / `getActiveBattlePokemon` in `TrackerAPI.lua` | Populated `Program.GameData.PlayerTeam` / `EnemyTeam`; active battle state for default active slots | API wrappers return Tracker party objects, and active battle API returns empty when `Battle.inActiveBattle()` is false. | Extension API calls remain empty until the stock or replacement readers populate teams and battle state. |

## CFRU/DPE live data sources

| CFRU source | Relevant symbols or structs | Why it matters |
| --- | --- | --- |
| `02_external/CFRU-expansion/include/pokemon.h` | `struct BoxPokemon`, `struct Pokemon`, `struct BattlePokemon`, extern `gPlayerParty`, extern `gEnemyParty` | Confirms party and battle layouts are source-declared and expanded beyond vanilla assumptions. |
| `02_external/CFRU-expansion/include/battle.h` | extern `gBattleMons`, `struct BattleMove` | Confirms live active battle data and battle move layout are source-visible. |
| `02_external/CFRU-expansion/include/global.h` | `struct SaveBlock1`, `playerParty`, `ItemSlot`, SaveBlock pointers | Bag/save support needs pointer-aware handling; it is not solved by table/name manifests. |
| `02_external/CFRU-expansion/src/wild_encounter.c` | Writes wild Pokemon into `gEnemyParty` and initializes battle flags. | Wild enemy truth is runtime party/battle RAM, not static table data. |
| `02_external/CFRU-expansion/src/build_pokemon.c` | Builds trainer parties into `gEnemyParty`. | Trainer enemy truth can be affected by CFRU runtime construction and randomizer behavior. |
| `02_external/CFRU-expansion/BPRE.ld` | Declares RAM symbols including party, battle, battle-state, and SaveBlock anchors. | It is a useful source-backed symbol reference, but docs must not copy real local/private address values. |

## Missing live RAM anchors

The address manifest must ultimately provide Tracker-compatible keys, not only CFRU symbol names:

| Needed by Tracker | CFRU/source concept | Status from current analysis |
| --- | --- | --- |
| `pstats` | `gPlayerParty` | Required for stock player-party iteration. Previous local generator warnings showed the symbol missing from local offsets input. |
| `estats` | `gEnemyParty` | Required for stock enemy/wild-party iteration. Previous local generator warnings showed the symbol missing from local offsets input. |
| `gBattleMons` | `gBattleMons` | Required for battle species validity, type reads, and active battle data. Previous local generator warnings showed the symbol missing from local offsets input. |
| `gBattlersCount` | `gBattlersCount` | Required by `Battle.updateBattleStatus` to avoid fake-battle classification. Not currently part of the local address generator's requested symbol set. |
| `gBattleOutcome` | `gBattleOutcome` | Required to decide active vs. ended battle. Included as optional generator target, but still needs local availability. |
| `gBattleMainFunc` and battle-main state pointers | `gBattleMainFunc` plus known battle function markers | Required before `Battle.dataReady` becomes true. Not currently covered by the local address generator. |
| `gBattlerPartyIndexes` | `gBattlerPartyIndexes` | Required for mapping battle slots back to party slots. Not currently covered by the local address generator. |
| `gBattlescriptCurrInstr`, `gBattleScriptingBattler`, `gBattlerTarget` | Battle script state | Used by Tracker battle update paths; future battle detail support needs these too. |
| SaveBlock / bag anchors | `gSaveBlock1`, `gSaveBlock2`, bag fields | Needed later for bag/item support. Current local generator warns when SaveBlock/bag symbols are absent. |

## Stock-reader problems

Even if the missing anchors are supplied, the stock reader still has CFRU-specific risks:

- `Program.readNewPokemon` assumes vanilla encrypted/reordered Gen III Pokemon substructures and an XOR key from personality and OT ID.
- CFRU's `struct Pokemon` is direct and expanded in `include/pokemon.h`, with source-visible fields for species, item, experience, moves, PP, EVs, level, current/max HP, stats, Tera/Gigantamax, and hidden ability.
- `Program.updatePokemonTeams` assumes each party slot can be decoded by that vanilla reader using `Program.Addresses.sizeofPokemonStruct`.
- The current `tracker-overrides.local=true` status does not by itself prove the override file changed the nested `Program.Addresses.*`, `PokemonData.Addresses.*`, or `MoveData.Addresses.*` fields used by readers. `GameSettings.importTrackerOverridesFromJson` returns true after decoding, so local smoke must verify effective assignments.
- Battle detection depends on `Tracker.getPokemon(1, false)` returning a valid enemy object. If `estats` or enemy decoding fails, `Battle.updateBattleStatus` can reject an otherwise real wild battle.

## Strategy comparison

| Option | Description | Assessment |
| --- | --- | --- |
| A. Add only `pstats` / `estats` / `gBattleMons` and keep stock readers | Fill missing live addresses, rely on current Tracker logic. | Useful as a plumbing smoke only. Not sufficient for correctness because CFRU party layout does not match stock `readNewPokemon`. |
| B. Implement a CFRU-aware `readPokemon` in the extension | Decode `struct Pokemon` directly from `gPlayerParty` / `gEnemyParty`. | Needed for reliable party and enemy team display, but requires validated struct offsets and live party anchors. |
| C. Implement active battle reader around `gBattleMons` first | Read species, moves, PP, ability, types, HP, level, item, status, and stat stages from `struct BattlePokemon`. | Recommended first useful v1 step after anchors exist. `BattlePokemon` offsets are source-commented and this bypasses vanilla party encryption assumptions for in-battle display. |
| D. Add a CFRU metadata table or public symbol manifest | Build/export sanitized symbol and layout metadata for Tracker consumption. | Best long-term path. Avoids private address copying and reduces drift when CFRU/DPE changes. |

## Recommended v1 direction

Do not treat the current loaded manifests as a live-data pass. The next minimal implementation should be an extension-side live-data smoke with explicit validation:

1. Extend the local address generator or local metadata input to include battle-state symbols needed by Tracker, especially `gBattlersCount`, `gBattleMainFunc`, `gBattlerPartyIndexes`, and the battle script state symbols.
2. Confirm that `pstats`, `estats`, and `gBattleMons` are present in the ignored local manifest without committing or documenting their values.
3. Prefer a custom active battle reader for `gBattleMons` as the first visible data path. This can prove Wild/Enemy active battle data without depending on vanilla party substructure decoding.
4. Add a CFRU-aware party reader for `gPlayerParty` and `gEnemyParty` after the active-battle reader is validated.
5. Keep SaveBlock/bag support out of v1 unless a safe pointer/source metadata path is available.

## Open questions

- Can the local symbol source reliably expose `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattlersCount`, `gBattleMainFunc`, and `gBattlerPartyIndexes`, or should a public CFRU metadata table be added?
- Should the extension wrap Tracker reader functions, populate Tracker `Program.GameData` directly, or expose a parallel CFRU/DPE data panel first?
- Does `TrackerAPI.loadTrackerOverridesFromJson` update the effective nested address tables in the installed Tracker version, or is extension-side assignment required?
- Which minimal battle-state markers are enough for a robust Wild smoke without depending on all stock `Battle.updateBattleStatus` assumptions?
