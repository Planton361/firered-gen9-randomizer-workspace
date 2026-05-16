# 028 - Trainer Writer/Reload/Text Field Review

## Scope

Read-only review for later Trainer ROM-/Reload-/Text-Encoding evidence.

No ROM, save, emulator state, output ROM, build artifact, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented. No UPR-FVX code change, writer fix, reload implementation, smoke run, build or P1 promotion was performed.

## Reviewed Code Paths

Primary Trainer data interfaces:

- `RomHandler.getTrainers()`, `loadTrainers()` and `saveTrainers()` define the Trainer data surface.
- `GameRandomizer.maybeRandomizeTrainerNames()` calls `TrainerNameRandomizer.randomizeTrainerClassNames()` and `randomizeTrainerNames()` only when `romHandler.canChangeTrainerText()` is true.
- `TrainerNameRandomizer` uses `getTrainerNames()`, `setTrainerNames(...)`, `getTrainerClassNames()`, `setTrainerClassNames(...)`, `trainerNameMode()`, `maxTrainerNameLength()`, `maxSumOfTrainerNameLengths()`, `getTCNameLengthsByTrainer()`, `fixedTrainerClassNamesLength()`, `maxTrainerClassNameLength()`, `getDoublesTrainerClasses()` and `internalStringLength(...)`.
- `AbstractRomHandler.getTrainerNames()` / `setTrainerNames(...)` map Trainer names through loaded `Trainer` objects by default.
- `Gen3RomHandler` overrides Gen3 Trainer class-name read/write and Gen3 string encoding/length behavior.

## Trainer Writer/Reload Fields

Gen3 `loadTrainers()` reads each Trainer entry from `TrainerData` using `TrainerCount` and `TrainerEntrySize`. The relevant reload fields are:

| Field | Read path | Write path | Evidence target |
|---|---|---|---|
| Trainer index/order | loop index and `Trainer.index` | implicit same order in `saveTrainers()` iterator | `trainerCountBefore/After/Reload`, index-stable compare |
| Team flags / poketype | entry byte `pokeDataType` | `writeByte(trOffset, tr.getPoketype())` | custom-moves and held-item structure width preserved |
| Trainer class byte | entry byte at `trOffset + 1` as lookup for class text | no current `saveTrainers()` write observed | preserve-only unless a later scope explicitly changes classes as data |
| Encounter gender high bit / stored class marker | `trOffset + 2` high bit into `Trainer.trainerclass` | no current write observed except battle style byte elsewhere | preserve/unchanged check if relevant |
| Trainer name text | `readVariableLengthString(trOffset + 4)` | `writeFixedLengthString(tr.getName(), trOffset + 4, TrainerNameLength)` | encoded fixed-length text reload compare |
| Battle style / battle mode byte | `trOffset + entryLen - 16` | conditional write when `isForcedDoubleBattle()` | battle-style evidence must compare this byte/semantic state |
| Team size | `trOffset + entryLen - 8` | `writeByte(..., tr.getPokemon().size())` | party count before/after/reload |
| Pokemon data pointer | `readPointer(trOffset + entryLen - 4)` | `DataRewriter` through pointer offset | pointer/repoint reload stability |
| Trainer Pokemon IV/strength | first word or byte-derived IV | `Math.min(255, 1 + IV * 255 / 31)` | IV/strength compare if included |
| Trainer Pokemon level | per-slot level word | per-slot level word | level compare for level modifier/evolution rules |
| Trainer Pokemon species | internal species word | `getTrainerPokemonInternalSpeciesId(...)` | internal `SpeciesSet` identity compare |
| Trainer Pokemon held item | optional item word | internal item word or `0` | held-item compare and preserve counters |
| Trainer Pokemon moves | optional four move words | existing moves or reset-level moves | move compare, invalid/unknown move counters |
| Mossdeep Steven special team | fixed 20-byte entries | species, IV, level and moves via custom writer | separate preserve/compare if Emerald scope is ever included |

`Trainer` also carries non-ROM or classification state such as `tag`, `fullDisplayName`, `multiBattleStatus`, `forceStarterPosition`, `requiresUniqueHeldItems` and `currBattleStyle`. Later evidence should distinguish these from bytes that are actually written.

## Text Encoder/Decoder Length Checks

Gen3 text review findings:

- `Gen3RomHandler.translateString(...)` encodes visible text and escape/control forms into bytes.
- `Gen3RomHandler.internalStringLength(...)` returns `translateString(string).length`; this is the relevant encoded/internal length check.
- `writeFixedLengthString(...)` copies at most the fixed field length, writes a terminator when space remains, then pads to the fixed field length.
- Gen3 Trainer names use `TrainerNameLength`; `maxTrainerNameLength()` returns `TrainerNameLength - 1`.
- Gen3 Trainer class names use `TrainerClassNames`, `TrainerClassCount` and `TrainerClassNameLength`; `maxTrainerClassNameLength()` returns `TrainerClassNameLength - 1`.
- `fixedTrainerClassNamesLength()` returns false for Gen3, so class names are bounded by maximum encoded length rather than same-length replacement.

Trainer name selection mostly uses `internalStringLength(...)` for pool filtering, replacement length and total-length accounting.

Trainer class-name selection builds length buckets with `internalStringLength(...)`, but the max-length rejection loop currently checks `changeTo.length() > maxLength`. That is an open risk because Java character count can differ from encoded/internal byte length.

The current Non-ROM `TrainerNameRandomizerTest` explicitly says it does not prove Gen3 writer, reload or text-encoding safety. Its fake `internalStringLength(...)` returns Java string length, so it cannot prove encoded-byte safety.

## Later Evidence Checks To Measure

For Trainer Pokemon / battle-style / special-rule evidence:

- Save/Log/Output/Reload true.
- `trainerCountBefore/After/Reload` and `trainerPokemonCountBefore/After/Reload`.
- `writeReloadTrainerPokemonMismatches=0` or narrower equivalent counters for species, level, moves and held items.
- `trainerTeamFlagMismatches=0`, party-size mismatches `0`, battle-style byte/semantic mismatches `0` when in scope.
- Preserve counters for non-target Boss/Important/Regular/`shouldNotGetBuffs` groups where applicable.
- `Bad Egg=false`, `<unknown>=false`, invalid move/item/species counters `0`, and `stacktrace=none`.

For Trainer Names/Class Names evidence:

- `trainerNamesBefore/After/Reload`, `trainerClassNamesBefore/After/Reload`.
- Encoded byte lengths for every changed name/class before write and after reload.
- No changed encoded name exceeds the fixed field payload length before terminator/padding.
- Reloaded decoded text matches the expected text for every changed slot.
- Padding/terminator behavior remains valid for shortened names.
- Repeated-name translations remain reload-stable.
- Doubles trainer names/classes use the expected pools and reload to the expected decoded strings.
- `changeTo.length()` must not be accepted as the proof metric; use `internalStringLength(...)` or raw encoded byte length.

## Open Risks

- Trainer class-name max filtering still has a Java-length check in the selection loop; later evidence must prove encoded length is safe or keep the scope blocked.
- `writeFixedLengthString(...)` truncates translated bytes to the fixed field length; evidence must detect truncation instead of treating a successful save as sufficient.
- `readVariableLengthString(...)` is used for fixed Trainer name/class slots in the reviewed code path; evidence must confirm terminator and padding do not hide trailing-byte corruption.
- Trainer class byte and some Trainer entry metadata are read or used for display/classification but are not generally rewritten in `saveTrainers()`; promotion criteria must separate data-preserve checks from actual writer claims.
- Mossdeep Steven uses a special fixed team writer and should not be folded into generic Trainer evidence unless explicitly scoped.

## Decision

This review identifies the fields and checks needed for later evidence. It does not change current status: recent Trainer follow-ups remain `tested-non-rom`, not P1-supported.

## Next Minimal Step

If authorized later, create a separate evidence plan or harness design for one narrow Trainer scope. Start with Trainer Names/Class Names only if the evidence can measure encoded/internal byte length, fixed-field write/reload, terminator/padding validity and decoded reload equality without relying on Java `String.length()`.
