# 060 - P1 GUI-Suboptions-Regressionsmatrix fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll ordnet konkrete FVX-GUI-Hauptoptionen und Suboptionen gegen den aktuellen CFRU/DPE-P1-Supportstand ein. Es konsolidiert die Kompatibilitaetsmatrix 047 und die Grenzen aus 055-059.

Scope:

- Nur bestehende Protokolle und read-only `rg`-/Quellbefunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Grenzen:

- Diagnose 055 bleibt die Grenze fuer Log-Hygiene, Unknown-/Fallback-Marker und Placeholder-/Null-Species-Einordnung.
- Diagnose 056 bleibt die Grenze fuer Move-Data-Write.
- Diagnose 057 bleibt die Grenze fuer Field Items, Shops, Pickup und allgemeine Item-Randomization.
- Diagnose 058 bleibt die Grenze fuer echte Palette-Randomization und Graphics/Sprites.
- Diagnose 059 bleibt die Grenze fuer Type-Chart und Type-Effectiveness.
- Ein stabiler Hauptpfad stuft keine Suboption automatisch auf `P1-supported` hoch.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `055_type_log_placeholder_hygiene.md`
- `056_p1_move_data_write_model.md`
- `057_p1_field_items_shops_pickup_model.md`
- `058_p1_palette_randomization_model.md`
- `059_p1_type_chart_model.md`

Read-only `rg`- und Codebefunde:

- `Settings.java`: Settings-Enums und Flags fuer Limit Pokemon, Base Stats, Types, Abilities, Evolutions, Starters, Trainers, Wild, Movesets, TM/HM, Tutor, MoveData, Field Items, Shops, Pickup, TypeEffectiveness und PokemonPalettes.
- `RandomizerGUI.java`: GUI-Checkboxen/Radiobuttons werden auf Settings-Flags gemappt.
- `GameRandomizer.java`: Ausfuehrungsreihenfolge und getrennte Randomizer-Komponenten.
- `Bundle.properties`: GUI-Labels und Tooltips, darunter Generation Limits, Follow Evolutions, Similar Strength, Same Type, Level Modifier, Force Change, Change Impossible Evolutions, Type Effectiveness und Pokemon Palettes.

Wichtige Codegrenzen:

- `maybeRandomizeMoveData()` ist ein eigener MoveData-Pfad und bleibt durch 056 begrenzt.
- `maybeRandomizeTypeEffectiveness()` ist ein eigener TypeChart-Pfad und bleibt durch 059 begrenzt.
- `maybeRandomizeFieldItems()`, `maybeRandomizeShops()` und `maybeRandomizePickupItems()` bleiben durch 057 begrenzt.
- `maybeRandomizePokemonPalettes()` ruft echte Palette-Randomization nur bei `PokemonPalettesMod.RANDOM` auf und bleibt durch 058 begrenzt.
- Level-Modifier fuer Trainer, Wild, Static und Totem/Ally sind eigene Level-Write-/Range-Effekte, nicht nur Species-Pool-Filter.

## Statusklassen

| Status | Bedeutung |
|---|---|
| `P1-supported` | Der Datenpfad ist im bestehenden P1-Stand direkt durch Save/Log/Output/Reload und passende Mismatch-Kriterien belegt. |
| `wahrscheinlich supported, aber nicht einzeln getestet` | Die Suboption nutzt wahrscheinlich einen bereits stabilen Writer oder reine Pool-/Filterlogik, wurde aber nicht als eigene GUI-Kombination belegt. |
| `modelliert, Fix offen` | Ein read-only Modell existiert und klassifiziert Risiken, aber ein Writer-/Reload-Fix ist offen. |
| `open-not-diagnosed` | Keine ausreichende CFRU/DPE-P1-Diagnose fuer diese Suboption oder diesen Writer. |
| `out of scope` | Nicht Teil des aktuellen P1-Datenpfads oder explizit einem spaeteren P2/Text/Graphics/Misc-Thema zugeordnet. |

## Leitplanken fuer die Einordnung

- `Similar Strength` haengt an Species-Pool, BST, Special-/Placeholder-Filtern und ggf. Forme-/Alt-Species-Policy.
- `Relative` / `Follow Evolutions` haengt an Evolutionsgraph, Formes und interner Species-Identitaet.
- `Level Modifier` ist ein eigener Trainer-/Wild-/Static-/Totem-Level-Write-/Range-Effekt.
- `Force Change`, `Change Impossible Evolutions` und `Make Evolutions Easier` koennen Evolution-Methoden, ExtraInfos, Items, Moves oder Locations beruehren.
- `Same Type` / `Prefer Same Type` nutzt Type-Felder aus 051, beweist aber keinen TypeChart-Support aus 059.
- Unknown-/Fallback-Marker aus 055 bleiben Log-Hygiene, solange Save/Log/Output/Reload stabil bleiben und Mismatches `0` sind.
- MoveData-, Item-, Palette- und TypeChart-Writer werden nicht durch stabile Pokemon-, Trainer-, Wild- oder Moveset-Hauptpfade freigegeben.

## Global

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| `Limit Pokemon` aus | `P1-supported` | Species-Pool ohne Generationseinschraenkung | 047; P1-Pfade Starters, Static/Gift, Trainer, Evolutions, Wild | Gen1-Gen9-Pools sind fuer die belegten Species-Pfade nutzbar. |
| `Limit Pokemon` an | `wahrscheinlich supported, aber nicht einzeln getestet` | `Settings.limitPokemon`, `GenRestrictions` | 047; `RandomizerGUI` / `Settings` | Poolfilter, aber keine einzelne GUI-Suboptionsmatrix mit allen P1-Writern. |
| Generation Limits | `wahrscheinlich supported, aber nicht einzeln getestet` | `GenRestrictions.limitToGen(...)` | `Bundle.properties` warnt fuer ROM-Hacks mit geaenderten/ergaenzten Pokemon | Bei CFRU/DPE konservativ als Poolfilter, nicht als Writer-Nachweis. |
| related Pokemon | `wahrscheinlich supported, aber nicht einzeln getestet` | verwandte Species aus eingeschraenkten Generationen | `GenerationLimitDialog.relatedPokemonHeader` | Haengt an Evolutionsgraph, Formes und Species-Identitaet. |
| Irregular / premature evolutions bans | `wahrscheinlich supported, aber nicht einzeln getestet` | Poolfilter | 047 + `Settings` | Keine eigene Writer-Oberflaeche, aber kann Poolverfuegbarkeit aendern. |

## Pokemon

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Base Stats random/shuffle | `P1-supported` | `gBaseStats` | 051 | BaseStats-Read/Write reload-stabil. |
| Base Stats Follow Evolutions | `wahrscheinlich supported, aber nicht einzeln getestet` | `baseStatsFollowEvolutions` im BaseStats-Randomizer | 051 als Writer; GUI-Suboption nicht separat belegt | Haengt an Evolutionsgraph und BST-Propagation. |
| Randomize Added Stats on Evolution | `wahrscheinlich supported, aber nicht einzeln getestet` | BaseStats-Evolutionsverteilung | 051 als Writer; `Bundle.properties` | Nur Suboptionslogik, keine eigene Reload-Diagnose. |
| Update Base Stats to Generation | `open-not-diagnosed` | BaseStats-Update-Logik | nicht durch 051 belegt | Kann generationales Datenmodell statt nur Random-Write betreffen. |
| Pokemon Types random/follow evolutions | `P1-supported` fuer Type-Bytes; Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | `SpeciesTypeRandomizer`, `gBaseStats` Type-Felder | 051; 059-Grenze | Type-Felder sind supported, TypeChart nicht. |
| Force Dual Types | `wahrscheinlich supported, aber nicht einzeln getestet` | Type-Randomization-Suboption | 051; 059 | Nutzt Species-Type-Felder; Stellar/unsupported bleibt skip/preserve. |
| Abilities randomize | `P1-supported` | Ability1/2 + Hidden Ability in `gBaseStats` | 055 verweist auf 052; 047 war aelter | Ability-Writer ist belegt, Namen/Fallbacks bleiben Log-Hygiene. |
| Abilities Follow Evolutions | `wahrscheinlich supported, aber nicht einzeln getestet` | Ability-Propagation entlang Evolutionsgraph | 052-Stand ueber 055; keine eigene GUI-Kombination | Haengt an Evolutionsgraph, Formes und all-zero Ability-Species-Filtern. |
| Ability-Bans / Ensure Two Abilities | `wahrscheinlich supported, aber nicht einzeln getestet` | Ability-Poolfilter | 052-Stand ueber 055 | Kein eigener Writer, aber Poollogik und Fallback-Namen bleiben konservativ. |

## Evolutions

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Evolutions Random | `P1-supported` | Evolution-Species-Write | 047 | Evolution-Scope und interne Species-Identitaet sind belegt. |
| Random Every Level | `wahrscheinlich supported, aber nicht einzeln getestet` | Evolution-Randomizer mit Level-Policy | 047 als Evolution-Writer | Suboption aendert Evolution-Policy staerker als Standard-Random. |
| Similar Strength | `wahrscheinlich supported, aber nicht einzeln getestet` | Species-Pool + BST-Filter | 047, 051 | Haengt an BST, Placeholder-/Special-Species-Filtern und Formes. |
| Same Typing | `wahrscheinlich supported, aber nicht einzeln getestet` | Species-Type-Filter | 051, 059 | Nutzt Type-Felder, nicht TypeChart. |
| Limit to Three Stages | `wahrscheinlich supported, aber nicht einzeln getestet` | Evolutionsgraph-Constraint | 047 | Graphconstraint, keine eigene Writerdiagnose. |
| Force Change | `wahrscheinlich supported, aber nicht einzeln getestet` | Evolutionsziel muss sich aendern | 047 | Kann bei engen Pools blockieren; keine eigene GUI-Kombination. |
| Force Growth | `wahrscheinlich supported, aber nicht einzeln getestet` | BST-Wachstumsconstraint | 051 + Evolution-Writer | Haengt an BST und Evolutionsgraph. |
| No Convergence / related graph constraints | `wahrscheinlich supported, aber nicht einzeln getestet` | Evolutionsgraph-Constraint | `Settings.evosNoConvergence` | Pool-Engpassrisiko bei CFRU/DPE-Formen. |
| Change Impossible Evolutions | `open-not-diagnosed` | `removeImpossibleEvolutions(...)` | `GameRandomizer.maybeApplyEvolutionImprovements()` | Kann Methoden, ExtraInfos, Moves, Items oder Locations beruehren. |
| Make Evolutions Easier | `open-not-diagnosed` | `condenseLevelEvolutions(...)`, `makeEvolutionsEasier(...)` | `GameRandomizer` | Eigene Level-/Methodenlogik, nicht durch Evolution-Random-Write belegt. |
| Remove Time-Based Evolutions | `open-not-diagnosed` | `removeTimeBasedEvolutions()` | `GameRandomizer` | Eigener Evolution-Methodenpfad. |

## Starters

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Starters Completely Random | `P1-supported` | Starter-Species-Write | 047 | Interne Species-Identitaet fuer Starter ist belegt. |
| Random basic / two evolutions | `wahrscheinlich supported, aber nicht einzeln getestet` | Starter-Poolfilter | 047 | Haengt an Evolutionsgraph und related Species. |
| Type Restrictions / Single Type / Triangle | `wahrscheinlich supported, aber nicht einzeln getestet` | Starter-Type-Filter | 051, 059 | Nutzt Type-Felder, nicht TypeChart; Pool kann zu klein werden. |
| No Dual Types | `wahrscheinlich supported, aber nicht einzeln getestet` | Starter-Type-Filter | 051 | Keine eigene Writerdiagnose. |
| BST limits | `wahrscheinlich supported, aber nicht einzeln getestet` | Starter-BST-Filter | 051 | Haengt an BaseStats/BST und Placeholder-Filtern. |
| No Legendaries / Allow Alt Formes | `wahrscheinlich supported, aber nicht einzeln getestet` | Starter-Poolfilter | 047 | Alt-Formes bleiben konservativ zu behandeln. |
| Randomize Starter Held Items | `open-not-diagnosed` | Starter-Held-Item-Write | nicht durch 054/057 belegt | Encounter Held Items und Trainer Held Items beweisen Starter-Held-Items nicht. |
| Ban Bad Starter Held Items | `open-not-diagnosed` | Starter-Item-Poolfilter | 053/057 als Itemmodellgrenze | Item-Pool muss pfadspezifisch bewertet werden. |

## Trainers

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Trainer Pokemon random/distributed/main playthrough | `P1-supported` | Trainer-Species-Write | 047 | Trainer-Scope und interne Species-Identitaet belegt. |
| Similar Strength | `wahrscheinlich supported, aber nicht einzeln getestet` | Trainer-Species-Pool + BST | 047, 051 | Haengt an BST, Pool und Special-Species-Filtern. |
| Type themes / Keep Themed / Keep Theme or Primary | `wahrscheinlich supported, aber nicht einzeln getestet` | Trainer-Type-Poolfilter | 051, 059 | Nutzt Species-Type-Felder, nicht TypeChart. |
| Type diversity | `wahrscheinlich supported, aber nicht einzeln getestet` | Trainer-Team-Type-Constraint | 051 | Kein eigener Reload-Nachweis. |
| Use Local Pokemon | `open-not-diagnosed` | Wild-Encounter-abhaengiger Trainer-Pool | 047 + Wild-Grenzen | Haengt an Wilddaten, Evolutionsverwandtschaft und Poolableitung. |
| Rival carries starter | `wahrscheinlich supported, aber nicht einzeln getestet` | Trainer + Starter-Kopplung | 047 | Kopplung zweier stabiler Writer, aber nicht einzeln belegt. |
| Trainer Level Modifier | `open-not-diagnosed` | `applyTrainerLevelModifier()` | `GameRandomizer` | Eigener Level-Write-/Range-Effekt. |
| Trainers evolve Pokemon / Evolution Level Modifier | `open-not-diagnosed` | Trainer-Level/Evolution-Policy | `Settings`, `GameRandomizer` | Eigenes Level-/Evolution-Constraint. |
| Additional Pokemon | `open-not-diagnosed` | `addTrainerPokemon()` | `GameRandomizer` | Aendert Party-Groessen und Battle-Kontexte. |
| Battle Style | `open-not-diagnosed` | `modifyBattleStyle()` | GUI-Tooltip nennt bekannte Softlock-Risiken | Nicht durch Trainer-Species-P1 belegt. |
| Trainer Held Items normal/sensible/consumable | `P1-supported` fuer belegte Trainer-Held-Item-Pfade; Subflags `wahrscheinlich supported, aber nicht einzeln getestet` | Trainer-Held-Item-Write | 047, 028, 032 | Boss/Important/Regular-Subflags und Highest-Level-only nicht alle einzeln belegt. |
| Better Movesets | `wahrscheinlich supported, aber nicht einzeln getestet` | TrainerMovesetRandomizer | 049-Stand ueber 047 | Haengt an Move-/Learnset-/TM/Tutor/Egg-Pools; MoveData-Write bleibt 056. |
| Trainer names / class names | `out of scope` | Text-Writer | `GameRandomizer.maybeRandomizeTrainerNames()` | Text/UI nicht Teil der P1-Datenmatrix. |

## Wild

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Wild Pokemon Randomize | `P1-supported` fuer Standard/Fallback-Wild | Wild-Encounter-Species-Write | 047 | Custom Day/Night bleibt separat. |
| Zone modes: game/location/map/encounter set/none | `wahrscheinlich supported, aber nicht einzeln getestet` | Wild-Zone-Gruppierung | 047 | Zone-Gruppen sind Pool-/Scope-Logik, nicht einzeln smoked. |
| Split by encounter types | `wahrscheinlich supported, aber nicht einzeln getestet` | Wild-Zone-Gruppierung | `Settings.splitWildZoneByEncounterTypes` | Keine eigene GUI-Kombination. |
| Similar Strength | `wahrscheinlich supported, aber nicht einzeln getestet` | Wild-Pool + BST | 047, 051 | Haengt an BST und Placeholder-/Special-Species-Filtern. |
| Type themes / Keep Primary | `wahrscheinlich supported, aber nicht einzeln getestet` | Wild-Type-Poolfilter | 051, 059 | TypeChart nicht beteiligt. |
| Evolution-stage filters / keep families | `wahrscheinlich supported, aber nicht einzeln getestet` | Wild-Evolution-Poolfilter | 047 | Haengt an Evolutionsgraph und Species-Identitaet. |
| Catch Em All / time-based encounters | `open-not-diagnosed` | Wild-Encounter-Sonderlogik | 047-Grenze | Day/Night/Time-basierte CFRU/DPE-Wilddaten sind separat. |
| Minimum catch rate | `open-not-diagnosed` | Species-Catch-Rate-Write | `GameRandomizer.maybeRandomizeWildPokemon()` | Eigenes BaseStats-/catch-rate-Feld, nicht 051-Teilziel. |
| Wild Level Modifier | `open-not-diagnosed` | Wild-Level-Write | `GameRandomizer.maybeRandomizeWildPokemon()` | Eigener Level-Write-/Range-Effekt. |
| Wild held items | `P1-supported` | Encounter Held Items in `gBaseStats` | 054; 055 | Nur Encounter Held Items, nicht Field/Shops/Pickup. |
| Balance Shaking Grass / alternate encounter systems | `out of scope` | nicht-FRLG/CFRU-Sonderpfad | GUI/Settings | Nicht Teil des getesteten BPRE-P1-Fallback-Wildpfads. |

## Movesets, TM, Tutor, Egg

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Pokemon Movesets random completely | `P1-supported` | Learnset-/Egg-Move-Flow | 047, 049 | GUI-Flow-Safety ist belegt. |
| Random preferring same type | `wahrscheinlich supported, aber nicht einzeln getestet` | Move-Pool + Species-/Move-Type-Filter | 049, 051, 056/059-Grenzen | Same Type nutzt Type-Felder, nicht TypeChart; MoveData-Write bleibt offen. |
| Force Good Damaging | `P1-supported` fuer getestete GUI-Flow-Kombinationen; Suboption sonst `wahrscheinlich supported, aber nicht einzeln getestet` | Move-Poolfilter | 049 | Haengt an Move-Data-Read und Move-Pool, nicht MoveData-Write. |
| Reorder Damaging Moves | `P1-supported` | Learnset-Write/Repointing-Flow | 049 | MoveData-Read nutzt 992 Moves; kein MoveData-Write. |
| Evolution Moves for All Pokemon | `P1-supported` fuer gekoppelte Flow-Safety; Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | Learnset-/Evolution-Move-Write | 049 | Keine neue Diagnose in 060. |
| TM moves random | `P1-supported` | 128-Slot TM/HM-Move-Write | 047 | 128 TM/HM-Slot-Support belegt. |
| TM Force Good Damaging / no game-breaking | `wahrscheinlich supported, aber nicht einzeln getestet` | TM-Move-Poolfilter | 047, 049 | Poolfilter; hohe Move-IDs durch Reader abgedeckt, MoveData-Write nicht. |
| TM compatibility random completely / prefer same type | `P1-supported` fuer Compatibility; Same-Type-Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | 128-Bit TM/HM-Compatibility | 047, 051 | Same Type nutzt Type-Felder, nicht TypeChart. |
| TM Follow Evolutions / level-up sanity | `P1-supported` fuer getestete Sanity-Flow-Kombinationen; Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | TM/HM-Compatibility + Learnsets | 049 | Haengt an Evolutionsgraph und Learnset-Reader/Writer. |
| Tutor moves random | `P1-supported` | normale Tutor-Tabelle | 047 | Special Tutors bleiben separat. |
| Tutor compatibility random / prefer same type | `P1-supported` fuer Compatibility; Same-Type-Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | Tutor-Compatibility | 047, 051 | Same Type nutzt Type-Felder, nicht TypeChart. |
| Tutor Follow Evolutions / level-up sanity | `P1-supported` fuer getestete Sanity-Flow-Kombinationen; Suboption `wahrscheinlich supported, aber nicht einzeln getestet` | Tutor-Compatibility + Learnsets | 049 | Evolutionsgraph-Abhaengigkeit. |
| Direct Egg Moves | `P1-supported` | `gEggMoves` Stream | 047 | Gekoppelte Movesets/Egg-Flow-Safety ueber 049. |
| Special Tutors / Tutor text/menu | `out of scope` | Special-Tutor-/Textpfade | 047 | Separates P2/Text/Menu-Thema. |

## MoveData

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Randomize Move Power | `modelliert, Fix offen` | `saveMoves()` klassisches Feld `+1` | 056 | Writer muss 992-Move-Scope und Preserve-Policy absichern. |
| Randomize Move Accuracy | `modelliert, Fix offen` | `saveMoves()` klassisches Feld `+3` | 056 | Kein Reload-Fix belegt. |
| Randomize Move PP | `modelliert, Fix offen` | `saveMoves()` klassisches Feld `+4` | 056 | Kein Reload-Fix belegt. |
| Randomize Move Types | `modelliert, Fix offen` | `saveMoves()` klassisches Feld `+2` | 056, 059 | Move-Type-Byte ist nicht Pokemon-TypeChart. |
| Randomize Move Category | `modelliert, Fix offen` | CFRU/DPE `BattleMove.split` bei `+10` | 056 | Aktueller Gen3-Writer schreibt `split` nicht. |
| Randomize Move Names | `open-not-diagnosed` | Move-Name-/Text-Write | 056-Grenze | Text/Menu/Description bleiben getrennt. |
| Update Moves to Generation | `modelliert, Fix offen` | MoveData-Update-Logik | 056 | Darf Zusatzfelder nicht verlieren. |

## Items

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Field Items shuffle/random/random even | `modelliert, Fix offen` | `ItemRandomizer.randomizeFieldItems()` | 057 | Script-/Map-/required-TM- und Item-Pool-Risiken. |
| Ban Bad Field Items | `modelliert, Fix offen` | Field-Item-Poolfilter | 057 | Bad-/Banned-Policy muss pfadspezifisch sein. |
| Shops shuffle/random | `modelliert, Fix offen` | `randomizeShopItems()`, `shuffleShopItems()` | 057 | Shopgroessen, Terminatoren, Preise, Special Shops. |
| Guaranteed Evolution Items / X Items | `modelliert, Fix offen` | Shop-Pool-/Placement-Policy | 057 | Progression und moderne Item-Bans. |
| Balance Shop Prices / Add Cheap Rare Candies | `modelliert, Fix offen` | Shop-Preis-/Inventar-Write | 057 | Preis-/Groessen-Reload separat. |
| Pickup random | `modelliert, Fix offen` | `randomizePickupItems()` | 057 | Common/Rare, Probability-Slots, moderne Item-Pools. |
| Ban Bad Pickup Items | `modelliert, Fix offen` | Pickup-Poolfilter | 057 | Nicht automatisch durch Encounter Held Items belegt. |

## Palettes

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Pokemon Palettes Unchanged | `P1-supported` | Palette-Safety / Skip-Unchanged-Save | 047, 058 | Safety-Pfad, keine echte geaenderte Palette-Randomization. |
| Pokemon Palettes Random | `modelliert, Fix offen` | `Gen3to5PaletteRandomizer`, `savePokemonPalettes()` | 058 | Compressed data, shared pointers, repointing. |
| Follow Types | `modelliert, Fix offen` | Palette-Type-Following | 058, 059 | Type-Following-Paletten sind kein TypeChart-Support. |
| Follow Evolutions | `modelliert, Fix offen` | Palette-Evolution-Following | 058 | Evolution-Following ist kein Evolution-Write-Nachweis. |
| Shiny From Normal | `modelliert, Fix offen` | Normal-/Shiny-Palette-Write | 058 | Shared/missing shiny pointers brauchen eigene Policy. |

## Type Effectiveness

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Type Effectiveness Unchanged | `P1-supported` als Nicht-Write | kein TypeChart-Write | 059 | Keine neue TypeChart-Unterstuetzung wird daraus abgeleitet. |
| Random | `modelliert, Fix offen` | `TypeEffectivenessRandomizer.randomizeTypeEffectiveness(false)` | 059 | TypeTable-Write, Fairy, Stellar/unsupported, Terminatoren. |
| Random Balanced | `modelliert, Fix offen` | `randomizeTypeEffectiveness(true)` | 059 | Zusaetzliche Balancing-Constraints. |
| Keep Type Identities | `modelliert, Fix offen` | TypeTable-Identity-Swaps | 059 | Kein Species-Type-Write. |
| Inverse | `modelliert, Fix offen` | `invertTypeEffectiveness(...)` | 059 | Kein P1-Reload-Nachweis fuer CFRU/DPE. |
| Add Random Immunities | `modelliert, Fix offen` | Inverse-Suboption | 059 | Darf keine unsupported/Stellar-Eintraege verlieren. |
| Update Type Effectiveness | `modelliert, Fix offen` | TypeEffectivenessUpdater / TypeTable | 059 | Gen6-Update beweist keine CFRU/DPE-Gen9-TypeChart-Sicherheit. |

## Misc, Tweaks, Text, Graphics

| GUI-Option / Suboption | Status | Datenpfad / Komponente | Beleg / Grenze | Risiko / Notiz |
|---|---|---|---|---|
| Intro Pokemon | `open-not-diagnosed` | `IntroPokeRandomizer` | `GameRandomizer.maybeRandomizeIntroPokemon()` | Eigener hardcoded/intro Pfad. |
| In-Game Trades | `open-not-diagnosed` | `TradeRandomizer` | `Settings.InGameTradesMod` | Given/requested Pokemon, Items, IVs, Nicknames/OTs nicht P1-belegt. |
| Static level modifier | `open-not-diagnosed` | Static-Level-Write | `Settings.staticLevelModified` | Static Species ist P1, Levelmodifier nicht. |
| Totem / Ally / Aura | `out of scope` | Gen7+-Sonderpfade | `Settings.TotemPokemonMod` | Nicht BPRE-P1-Scope. |
| Misc Tweaks | `open-not-diagnosed` | `MiscTweakRandomizer` | `GameRandomizer.maybeApplyMiscTweaks()` | Code-/ASM-/Text-/Systempatches getrennt behandeln. |
| PC Potion / catching tutorial | `open-not-diagnosed` | Misc-/Intro-/Item-Sonderpfade | `Bundle.properties` | Kein Field-/Shop-/Pickup-Nachweis aus 057. |
| Lowercase names / custom names / trainer text | `out of scope` | Text-Writer | GUI/Text-Pfade | Text/Menu/Description nicht Teil von 060. |
| Custom Player Graphics | `out of scope` | Graphics pack / sprite data | 058-Grenze | Graphics/Sprites bleiben P2. |
| Pokemon sprites / overworld graphics | `out of scope` | Graphics/Sprite-Repointing | 058-Grenze | Nicht mit Pokemon-Paletten vermischen. |

## Regressionsempfehlungen fuer spaetere Checks

060 fuehrt keine neuen Laeufe aus. Fuer spaetere, separat freigegebene Smoke-/Regression-Checks sollten Suboptionen nach Writer-Oberflaeche gebuendelt werden:

1. Pool-/Filter-Suboptionen ohne neuen Writer: Generation Limits, Similar Strength, Same Type, Follow Evolutions, BST Limits, No Dual Types und related Pokemon.
2. Level-Write-Suboptionen: Trainer, Wild, Static und Totem/Ally Level Modifier getrennt.
3. Evolution-Methoden-Suboptionen: Change Impossible Evolutions, Make Evolutions Easier und Remove Time-Based Evolutions getrennt.
4. Item-Writer: Field Items, Shops, Pickup, Starter Held Items und In-Game-Trade Items nicht mit Encounter Held Items vermischen.
5. MoveData-Writer: Power/Accuracy/PP/Type/Category/Update Moves nach 056 und mit Preserve-Reload pruefen.
6. Palette-Writer: `PokemonPalettesMod.RANDOM` und Follow-Suboptionen nach 058 mit compressed/shared/repointing Kriterien.
7. TypeChart-Writer: Random/Balanced/Keep Identities/Inverse/Update/Add Immunities nach 059.
8. Text/Graphics/Misc: nur als eigene P2- oder Misc-Blocks, nicht als Voraussetzung fuer P1-Datenpfade.

## Ergebnis

Die vorhandenen P1-Fixes tragen viele Hauptpfade, aber nicht jede FVX-GUI-Suboption ist einzeln regressionsgetestet. 060 trennt deshalb drei Ebenen:

- direkt belegte Datenpfade wie Wild/Trainer/Starter/Static/Evolution-Species, Trainer Held Items, Movesets/Learnsets, TM/HM, Tutor, Egg Moves, BaseStats/Types/Abilities und Encounter Held Items;
- wahrscheinlich stabile Suboptionen, die nur Pool-, Filter- oder Follow-Logik ueber bereits belegte Writer nutzen;
- modellierte oder offene Writer fuer MoveData, Field Items/Shops/Pickup, Paletten, TypeChart, Levelmodifier, Evolution-Methoden, Text, Misc und Graphics.

Naechster sinnvoller Block ist ein read-only Regression-Smoke-Plan oder ein priorisierter Fixbranch fuer einen der modellierten offenen Writer. 060 empfiehlt als konservativen Anschluss `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan`, bevor mehrere Suboptionen in einem Fixbranch vermischt werden.
