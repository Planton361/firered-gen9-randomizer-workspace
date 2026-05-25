# CFRU/DPE Tracker Layout Overrides

Status: documentation-only source analysis. No ROMs, builds, saves, emulator states, raw logs, hashes, private paths, `offsets.ini` data or real runtime addresses were used.

## Executive summary

Several Tracker override values are safe as source-derived layout candidates, especially CFRU `BattleMove`, `BattlePokemon`, `BaseStats`, `Trainer` header fields, and simple trainer-party row variants. These are struct sizes and offsets, not ROM or RAM addresses.

The unsafe area is live party Pokemon. CFRU `struct Pokemon` is no longer the vanilla encrypted Gen 3 party layout that Ironmon Tracker's `Program.readNewPokemon` decodes. A simple `sizeofPokemonStruct`/`offsetPokemonSubstruct` override is unlikely to be enough for correct party reads unless the extension also changes the reader or uses a CFRU metadata table.

The committed `tracker-overrides.example.json` should remain example-only. It can list safe candidates and validation notes, but real `game-addresses.json` / `tracker-overrides.json` values for a local ROM must stay ignored/local until a public source-symbol or metadata path exists.

## Tracker override model

| Tracker source | Relevant behavior | CFRU/DPE impact |
| --- | --- | --- |
| `02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua` | `importTrackerOverridesFromJson` reads JSON sections named `Program`, `PokemonData`, `MoveData`, `AbilityData`, and `BattleDetailsScreen`. | The extension can use Tracker override JSON as a starting point, but must validate that loaded keys actually affect the nested tables consumed by read paths. |
| `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua` | `TrackerAPI.loadTrackerOverridesFromJson(filepath)` forwards to `GameSettings.importTrackerOverridesFromJson`. | This is the public API surface for a future extension smoke. |
| `02_external/Ironmon-Tracker/ironmon_tracker/Program.lua` | Read paths consume `Program.Addresses.*` for party, battle, trainer and struct sizes. | CFRU/DPE overrides must ultimately update `Program.Addresses`, not just document candidates. |
| `PokemonData.lua` | Base stats use `PokemonData.Addresses.*` plus `Program.Addresses.sizeofBaseStatsPokemon`. | CFRU/DPE base stat offsets are mostly source-derived, including hidden ability as a CFRU extension field. |
| `MoveData.lua` | Move reads use `Program.Addresses.offsetBattleMoves`, `Program.Addresses.offsetBattleMoveFlags`, `Program.Addresses.sizeofBattleMove`, then bit offsets in `MoveData.Addresses.*`. | CFRU `struct BattleMove` is byte-oriented and larger than the vanilla 4-byte bitfield read model; the read model must be validated with CFRU offsets. |

Important loader caveat: the inspected `importTrackerOverridesFromJson` loop decodes entries under `globalInfo.Addresses`, but assigns them to `globalObj[k]`. The consumers inspected in `Program.lua`, `PokemonData.lua`, and `MoveData.lua` read nested `*.Addresses.*` tables. A future implementation must smoke-test the effective override path or set nested fields explicitly in the extension.

## Source-derived layout candidates

| Area | Candidate | Source basis | Tracker use | Confidence |
| --- | --- | --- | --- | --- |
| `BattleMove` size | `0x0C` | CFRU `include/pokemon.h` defines 12 one-byte fields: effect, power, type, accuracy, PP, chance, target, priority, flags, z-move power, split, z-move effect. | `Program.Addresses.sizeofBattleMove`. | High as a source layout candidate. |
| `BattleMove` data dword | `offsetBattleMoves = 0x01` | In CFRU `struct BattleMove`, power/type/accuracy/PP are bytes at `0x01..0x04`. Tracker reads one dword starting at this offset. | `MoveData.readMoveInfoFromMemory`. | High for power/type/accuracy/PP extraction. |
| `BattleMove` flags byte | `offsetBattleMoveFlags = 0x08` | CFRU `flags` field is byte `0x08`. | Physical/special category support. | Medium; CFRU also has explicit `split` at `0x0A`. |
| `MoveData` bit offsets | power `0`, type `8`, accuracy `16`, PP `24` | Tracker extracts each byte from the dword read at `offsetBattleMoves`. | `MoveData.Addresses.*`. | High if `offsetBattleMoves = 0x01` is used. |
| Move category | `offsetMoveFlagsCategory = 0x0A` candidate for CFRU split byte | CFRU `struct BattleMove.split` is byte `0x0A`; stock Tracker category reads bits from a flags byte. | Move category display. | Medium; may need a custom read because Tracker currently reads one flags byte at `offsetBattleMoveFlags`. |
| `BattlePokemon` size | `0x58` | CFRU source comments fields from species `0x00` through `otId` at `0x54`; natural end is `0x58`. | `Program.Addresses.sizeofBattlePokemon`. | High as a source-commented candidate, still metadata-validation recommended. |
| `BattlePokemon` stat stages | `0x19` | CFRU `statStages` starts at `0x19`. | Battle detail/stat-stage reads. | High. |
| `BattlePokemon` types | `0x21` | CFRU `type1`/`type2` at `0x21`/`0x22`. | `Program.getPokemonTypes`. | High. |
| `BaseStats` size | `0x1C` candidate | CFRU and DPE `struct BaseStats` comments run through hidden ability at `0x1A`; alignment likely pads to `0x1C`. | `Program.Addresses.sizeofBaseStatsPokemon`. | Medium-high; bitfields/alignment should be validated. |
| `BaseStats` core offsets | base stats `0x00`, types `0x06`, catch `0x08`, exp `0x09`, friendship `0x12`, abilities `0x16` | CFRU `pokemon.h` and DPE `base_stats.h` match. | `PokemonData.readPokemonInfoFromMemory`. | High for the named byte offsets. |
| Hidden ability | `0x1A` | CFRU/DPE add `hiddenAbility` after body color/noFlip bitfield. | Extension-side ability display. | Medium; stock Tracker only reads two abilities unless extended. |
| `Trainer` header size | `0x28` | CFRU `struct Trainer` comments through party pointer at `0x24`; 32-bit pointer makes natural end `0x28`. | `Program.readTrainerGameData`. | High under GBA 32-bit ABI. |
| `Trainer` header offsets | class `0x01`, gender/music `0x02`, pic `0x03`, name `0x04`, items `0x10`, double `0x18`, AI `0x1C`, party size `0x20`, party ptr `0x24` | CFRU `battle.h` comments. | Static trainer identity/context. | High for header fields. |
| Simple TrainerMon rows | no-item/default `0x08`, item/default `0x08`, no-item/custom `0x10` | CFRU `battle.h` struct definitions. | Stock-style static trainer-party reads. | Medium; static party is not final runtime truth. |
| Expanded item/custom TrainerMon row | `0x1C` candidate | CFRU adds ability, nature, IV spread, EV spread, held item, moves and Tera type. | Static trainer-party context only. | Medium; stock Tracker's `sizeofTrainerMonWithCustomMoves = 0x10` is insufficient. |
| Bag item slot | `0x04` candidate | CFRU `struct ItemSlot` is `u16 itemId; u16 quantity;`. | Later bag support. | High for slot size, but address path remains unsafe. |
| Bag pocket counts | items `42`, key items `30`, balls `13`, TM/HM `58`, berries `43` | CFRU `global.h` constants. | Later bag manifest. | High for counts, not for SaveBlock base address. |

## Unsafe or validation-required areas

| Area | Why unsafe | Recommended handling |
| --- | --- | --- |
| Live `struct Pokemon` party reads | CFRU `typedef struct Pokemon` exposes direct growth/attack/condition/misc fields, `backupSpecies`, `teraType`, `gigantamax`, `hiddenAbility`, and trailing battle stats. Tracker `Program.readNewPokemon` assumes vanilla encrypted/reordered substructs and XOR decoding. | Do not claim stock party reads are fixed by offsets alone. Use a CFRU-specific reader or metadata table before public v1. |
| `BoxPokemon` | CFRU box layout includes `teraType` before unencrypted substructs and bitfields. | Delay box/storage support. |
| Bitfields and compiler padding | `PokemonSubstruct3`, `BaseStats`, `Trainer.encounterMusic/gender` and IV fields depend on GBA ABI assumptions. Source comments help but should be validated. | Generate or validate offsets via compiler metadata, static assertions, or a public metadata table. |
| Move category | CFRU has both flags and a separate `split` byte, while Tracker's stock physical/special model extracts category bits from a flags byte. | Prefer an extension-side move reader or explicit validation before relying on category display. |
| Static trainer party | CFRU/randomizer can build or alter real enemy Pokemon at runtime; expanded TrainerMon rows exceed stock custom-row assumptions. | Use static trainer data for names/classes/context only. Treat live `gEnemyParty`/`gBattleMons` as battle truth. |
| SaveBlock/bag addresses | `SaveBlock1` comments give internal offsets and bag counts, but `gSaveBlock1` is a runtime pointer. | Keep local addresses in ignored JSON until metadata/symbol support exists. |
| Override loader semantics | The inspected JSON import writes decoded `Addresses` keys to the global object root while read paths consume nested `.Addresses` tables. | Local smoke must verify that `TrackerAPI.loadTrackerOverridesFromJson` actually changes effective read fields, or the extension must assign nested tables explicitly. |

## v1 Tracker fields

For a useful first extension smoke, prioritize these fields:

| Goal | Fields needed | Status |
| --- | --- | --- |
| Move display from `gBattleMoves` | `sizeofBattleMove`, `offsetBattleMoves`, `offsetBattleMoveFlags`, move power/type/accuracy/PP bit offsets; category handling caveat. | Source-derived candidates exist; category needs validation. |
| Base stat/type/ability display | `sizeofBaseStatsPokemon`, base stat/type/catch/exp/friendship/ability offsets, species/move/ability ID mappings. | Source-derived candidates exist; hidden ability needs extension support. |
| Active battle type/stat reads | `sizeofBattlePokemon`, `offsetBattlePokemonTypes`, `offsetBattlePokemonStatStages`, real `gBattleMons` address from safe metadata/local override. | Layout candidates exist; address does not. |
| Player/enemy party display | real `gPlayerParty`/`gEnemyParty` addresses plus a CFRU-aware party reader. | Not safe through stock layout overrides alone. |
| Trainer identity | `sizeofTrainer`, trainer header offsets, trainer class name address, trainer table address. | Header layout candidates exist; addresses remain metadata/local override. |
| Static trainer party | TrainerMon row sizes and offsets. | Context-only; not v1 battle truth. |
| Bag/items | `ItemSlot` size, bag pocket counts, SaveBlock pointer model. | Later target; address path unresolved. |

## Manifest recommendation

Keep committed examples split by confidence:

- `sourceDerivedCandidates`: source-backed offsets/sizes that are useful generator inputs.
- `needsValidation`: candidates that depend on ABI, Tracker loader behavior, or CFRU-specific reader support.
- `notAddressData`: explicit reminder that these values are not ROM/RAM target addresses.
- real `Program.Addresses`, `PokemonData.Addresses`, and `MoveData.Addresses` fields should remain `TODO_SOURCE_DERIVED` in examples until a local ignored smoke proves both loader behavior and CFRU read correctness.

Long-term, the cleanest public path is a CFRU/DPE metadata table or source-symbol generator that emits:

- safe target addresses or pointer slots;
- struct sizes and offsets from the exact compiled profile;
- source-derived counts and ID/name mappings;
- a schema version that the Tracker extension can reject when incompatible.

## Open questions

- Whether the Tracker override API should be used as-is, or the extension should bypass it and patch nested `*.Addresses` tables directly.
- Whether CFRU move category should come from `BattleMove.split` at `0x0A` rather than the stock flags-category bit extraction path.
- Exact compiler-derived size for CFRU `struct Pokemon` and whether any stock `readNewPokemon` path can be reused safely.
- How hidden ability, Tera type and Gigantamax should be surfaced in Tracker without misreporting stock ability semantics.
- Which source-public metadata path should provide final `gPlayerParty`, `gEnemyParty`, `gBattleMons`, `gBattleMoves`, `gBaseStats`, `gTrainers`, name tables and SaveBlock pointers.
