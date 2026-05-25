# CFRU Runtime Custom Move Construction

Date: 2026-05-26

## Executive summary

The UPR-FVX write/reload audit can be clean while the emulator-side `gBattleMons`
snapshot still shows rows like `moves[-/Flamecharge/Cosmicpower/Block]` because
the audit and CFRU runtime do not necessarily interpret trainer move data through
the same path.

Source-backed findings:

- CFRU `BattlePokemon` layout supports the current Tracker move reader:
  `moves[4]` starts at offset `0x0C`, PP starts at `0x24`, and row size is
  `0x58` in `02_external/CFRU-expansion/include/pokemon.h`.
- CFRU custom trainer moves are 0-based and exact-copied by
  `SET_MOVES(structure)` in `include/new/build_pokemon_2.h`; CFRU does not
  compact `MOVE_NONE` out of slot 0 in that macro.
- CFRU `CreateNPCTrainerParty` disables custom trainer moves when
  `FLAG_POKEMON_RANDOMIZER` is active, unless Battle Facility or the temporary
  disable-randomizer flag applies. In that mode, Better-Movesets custom rows may
  be ignored at runtime and generated/default moves are used instead.
- UPR-FVX currently writes classic Gen3 custom-move trainer rows as 16 bytes for
  both no-item and held-item custom-move trainers. CFRU's
  `TrainerMonItemCustomMoves` layout is expanded and expects held-item
  custom-move rows to contain ability/nature/IV/EV fields, held item, moves, and
  tera type. That is not the same layout as UPR-FVX's current item+custom writer.

Most likely cause candidates, in priority order:

1. If the affected trainer has `partyFlags == PARTY_FLAG_CUSTOM_MOVES |
   PARTY_FLAG_HAS_ITEM`, UPR-FVX and CFRU disagree on row size and move offsets.
   The UPR-FVX audit can pass against the classic 16-byte layout while CFRU reads
   a different 32-byte expanded layout at runtime.
2. If `FLAG_POKEMON_RANDOMIZER` is active during the battle, CFRU intentionally
   skips trainer custom moves. Then the observed `gBattleMons` moves come from
   CFRU's generated move path, not from the audited UPR-FVX custom-move row.
3. The Tracker move offsets are less likely to be the root cause for the leading
   empty slot because HP, PP, species, level, and move slots align with
   `struct BattlePokemon`; however, local battle context should still include
   trainer id, party slot, and party flags before classifying a row.

## Relevant CFRU code paths

| File | Function / block | Source-backed behavior | Impact for `[-/Move/Move/Move]` |
| --- | --- | --- | --- |
| `02_external/CFRU-expansion/include/pokemon.h` | `struct BattlePokemon` | `moves[4]` is at offset `0x0C`; PP is at `0x24`; row size is `0x58`. | Supports the CFRUDPEExtension `gBattleMons` move-slot offsets. |
| `02_external/CFRU-expansion/include/battle.h` | `struct TrainerMonNoItemCustomMoves` | Layout is `iv`, `lvl`, `species`, `moves[4]`, filler; 16 bytes. | Matches classic no-item custom-move trainer rows. |
| `02_external/CFRU-expansion/include/battle.h` | `struct TrainerMonItemCustomMoves` | Layout is `iv`, `lvl`, `species`, `ability`, `nature`, `ivSpread[6]`, `evSpread[6]`, `heldItem`, `moves[4]`, `teraType`; expanded row. | Does not match a classic 16-byte held-item custom-move row. |
| `02_external/CFRU-expansion/include/battle.h` | `PARTY_FLAG_CUSTOM_MOVES`, `PARTY_FLAG_HAS_ITEM` | Party flag `1` means custom moves; flag `2` means held item; flag `3` means both. | Flag `3` is the high-risk layout case. |
| `02_external/CFRU-expansion/include/new/build_pokemon_2.h` | `SET_MOVES(structure)` | Copies `structure[i].moves[j]` directly into `party[i].moves[j]` for `j = 0..3`; PP is computed per same index. | CFRU does not compact a leading `MOVE_NONE`; if slot 0 is zero in the runtime structure, it stays zero. |
| `02_external/CFRU-expansion/src/build_pokemon.c` | `CreateNPCTrainerParty` / `setCustomMoves` | With `FLAG_POKEMON_RANDOMIZER`, custom moves are applied only in Battle Facility, when species randomizer is off, or when temp-disable-randomizer is set. | Under normal randomized trainer battles, Better-Movesets custom rows may be ignored by CFRU runtime. |
| `02_external/CFRU-expansion/src/build_pokemon.c` | `CreateNPCTrainerParty` / party flag switch | `PARTY_FLAG_CUSTOM_MOVES` uses `NoItemCustomMoves`; flag `3` uses `ItemCustomMoves`. `SET_MOVES` is conditional on `setCustomMoves`. | Runtime behavior depends on both party flags and randomizer flags. |

## UPR-FVX vs CFRU trainer layout comparison

| Case | CFRU runtime layout | UPR-FVX current writer/readback | Compatibility |
| --- | --- | --- | --- |
| No item, default moves (`partyFlags=0`) | 8 bytes: IV, level, species, filler. | 8 bytes. | Compatible. |
| Held item, default moves (`partyFlags=2`) | 8 bytes: IV, level, species, held item. | 8 bytes. | Compatible. |
| No item, custom moves (`partyFlags=1`) | 16 bytes: IV, level, species, moves at offset `+6`, filler at `+14`. | 16 bytes; moves at `+6`; filler at `+14`. | Compatible. |
| Held item, custom moves (`partyFlags=3`) | Expanded CFRU layout: ability/nature/spreads, held item, moves later in the row, tera type. | Classic 16-byte Gen3 layout; item at `+6`, moves at `+8`. | Likely incompatible for CFRU/DPE. |

UPR-FVX source-backed details:

- `Trainer.getPoketype()` builds classic Gen3 flags from
  `pokemonHaveCustomMoves()` plus `pokemonHaveItems()`.
- `Gen3RomHandler.readTrainerDataRowInternal()` reads `pokeDataType == 3` with
  16-byte rows, held item at `+6`, and moves at `+8`.
- `Gen3RomHandler.trainerPokemonToBytes()` writes custom-move trainer data with
  `dataSize = partySize * 16` whenever any custom moves are active. If the
  trainer has items, it writes item at `+6` and moves at `+8`.
- The recent normalization code compacts move slots before write, so a clean
  UPR-FVX audit proves consistency for UPR-FVX's decoded layout, not necessarily
  CFRU's expanded held-item custom layout.

## Why the audit can pass while runtime still differs

The private audit confirms the UPR-FVX output ROM can be reloaded through
UPR-FVX and that raw trainer rows match UPR-FVX's expected runtime-source state.
That rules out the earlier UPR-FVX bugs where rows were written as
`[-/Move/Move/Move]` in the classic custom-move layout.

It does not rule out CFRU runtime interpretation differences:

- For `partyFlags=3`, UPR-FVX's writer and reloader agree with each other on a
  16-byte Gen3 row, but CFRU source defines a different expanded row. CFRU can
  therefore read bytes from different positions than UPR-FVX audited.
- For randomized trainer battles, CFRU can deliberately skip applying custom
  trainer moves via `setCustomMoves == FALSE`. In that case, audited Better
  Movesets are not the final source of `gBattleMons` moves.

## Does CFRU compact or fix leading empty slots?

Not in the normal custom-move copy path. `SET_MOVES(structure)` copies all four
slots as stored in the selected trainer structure. If slot 0 is `MOVE_NONE`,
slot 0 remains empty.

Some unrelated code paths can rewrite moves, for example Frontier spread
creation, Metronome-only handling, randomized move regeneration, or later move
replacement helpers. Those do not change the source-backed conclusion that the
normal trainer custom-move copy path is exact-copy.

## Most likely cause for the current smoke

The strongest source-backed explanation is a combination of:

1. CFRU runtime may not be applying UPR-FVX Better-Movesets custom moves at all
   while `FLAG_POKEMON_RANDOMIZER` is active.
2. Any trainer with both item and custom moves is vulnerable to a layout mismatch
   because CFRU expects expanded `TrainerMonItemCustomMoves` rows while UPR-FVX
   currently writes/reloads classic 16-byte rows.

The exact classification for the sanitized examples
`moves[-/Flamecharge/Cosmicpower/Block]` and
`moves[-/Chargebeam/Substitute/Gravity]` requires the local trainer id, active
party slot, and raw `partyFlags` for those rows. Those values can be documented
as sanitized categories or numeric trainer/slot identifiers, but no ROM path,
address, raw log, hash, screenshot, save, or build artifact should be committed.

## Recommended next fix direction

Do not change CFRU first. The smallest next step is a UPR-FVX diagnostic/fix
branch focused on CFRU/DPE trainer layout compatibility:

1. Extend the private trainer audit to report, for the observed trainer id/slot:
   `partyFlags`, has-item yes/no, custom-moves yes/no, writer row size, writer
   move offset, and whether the row is decoded as classic Gen3 or CFRU expanded
   layout.
2. Add a ROM-free UPR-FVX test for CFRU/DPE `partyFlags=3` trainer rows. The
   expected CFRU layout should be 32 bytes per Pokemon with moves at the CFRU
   `TrainerMonItemCustomMoves.moves` position, not at classic offset `+8`.
3. If confirmed, make UPR-FVX CFRU/DPE mode write and reload held-item
   custom-move trainers using the expanded CFRU layout while preserving the
   already-fixed no-item custom layout.
4. Separately, decide whether Better Movesets should matter when CFRU's
   `FLAG_POKEMON_RANDOMIZER` path disables custom trainer moves. If the intended
   design is runtime-generated moves for randomized trainer species, then the
   next CFRU-side analysis should inspect `GiveBoxMonInitialMoveset` and related
   generated-moves paths for leading `MOVE_NONE` behavior.

## Open questions

- Are the observed rows from trainers with `partyFlags=1` or `partyFlags=3`?
- Was `FLAG_POKEMON_RANDOMIZER` set during the local smoke battle?
- Are the observed active enemies regular trainers, Rival protected slots, or
  randomizable Rival nonstarter slots?
- Does `gEnemyParty` already contain the leading empty slot before battle-copy to
  `gBattleMons`, or is it introduced during battle initialization?
