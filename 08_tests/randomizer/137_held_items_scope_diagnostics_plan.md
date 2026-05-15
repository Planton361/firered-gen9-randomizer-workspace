# Diagnose 137 - Held Items Scope Diagnostics Plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-held-items-scope-diagnostics-plan`
Scope: Read-only plan for CFRU/DPE Gen9-BPRE Held Items diagnostics

## Ziel

Dieser Block plant Held Items als neuen separaten Randomizer-Scope nach dem abgeschlossenen Shop Items Scope.

Der Block ist read-only:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Lauf
- kein ROM-/Artefaktzugriff
- keine Smoke-Ausfuehrung
- keine Feature-Hochstufung

## Scope

Held Items werden als eigener Feature-/Paket-Scope bestaetigt und strikt von Field Items, Pickup und Shops getrennt.

Getrennte Subscopes:

1. Wild/Encounter Held Items.
2. Trainer Held Items.
3. Starter Held Items, weil UPR-FVX einen eigenen Starter-Held-Item-Pfad besitzt.
4. Ban-Bad-/Pool-Optionen separat, falls sie fuer den jeweiligen Subscope vorhanden sind.

Ausserhalb dieses Blocks:

- Field Items
- Pickup
- Shops
- Preise, Rare Candies, Shop Guarantees und Shop Bans
- Trainer-Randomization ausser Held-Items-Analyse
- Wild-Randomization ausser Held-Items-Analyse
- Evolution, Learnset, TM/HM/Tutor, Move, Ability, TypeChart, Palette, Graphics und Text/Menu
- ROMs, Saves, Emulator States, Builds, Logs, Output-ROMs, Randomizer-JARs und Tool-Binaries

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens und `.env`-Inhalte wurden nicht dokumentiert.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/136_shop_balance_prices_cheap_rare_candies_reload_smoke.md`

## Read-only Suche

Verwendet wurden `rg`, `rg --files` und gezielte Dateiauszuege. Es gab keinen Build, keinen Randomizer-Lauf und keinen ROM-/Artefaktzugriff.

Suchbegriffe:

- `Held`
- `heldItem`
- `heldItems`
- `randomizeHeldItems`
- `randomizeWildHeldItems`
- `randomizeTrainerHeldItems`
- `randomizeStarterHeldItems`
- `Pokemon`
- `PokemonSpecies`
- `Species`
- `TrainerPokemon`
- `Trainer`
- `Encounter`
- `EncounterSet`
- `WildPokemon`
- `Starter`
- `getPokemon`
- `setPokemon`
- `getTrainers`
- `setTrainers`
- `getEncounters`
- `setEncounters`
- `getStarters`
- `setStarters`
- `ItemList`
- `getAllowedItems`
- `getNonBadItems`
- `canTMsBeHeld`
- `isBad`
- `isAllowed`
- `isTM`
- `Settings`
- `GameRandomizer`
- `RandomizerGUI`
- `Bundle.properties`
- `Gen3RomHandler`
- `RomHandler`

## Held-Items-Scope-Einschaetzung

Held Items sind ein eigener Scope und duerfen nicht mit Field Items, Pickup oder Shops vermischt werden.

Begruendung:

- Shop Items sind durch Diagnose 136 im getesteten CFRU/DPE Gen9-BPRE Scope abgeschlossen.
- Field Items schreiben Map-/Script-/Signpost-Itemdaten.
- Pickup schreibt Pickup-Tabellen.
- Shops schreiben Shoplisten und Preisfelder.
- Held Items schreiben andere Zielstrukturen: Species-Basisdaten fuer Wild/Encounter-Held-Items, Trainer-Teamdaten fuer Trainer-Held-Items und Starter-Held-Item-Felder fuer Starter-Held-Items.

Keine Held-Item-Option wird durch diesen Plan hochgestuft. Der naechste Block muss zuerst eine read-only Kandidatendiagnose liefern.

## Relevante Codepfade

### Gemeinsamer Ablauf

- `GameRandomizer.applyRandomizers()` ruft Held-Item-Pfade getrennt von Pickup und Shops auf.
- `GameRandomizer.maybeRandomizeWildHeldItems()` ruft `EncounterHeldItemRandomizer.randomizeWildHeldItems()` bei `Settings.isRandomizeWildPokemonHeldItems()`.
- `GameRandomizer.maybeRandomizeStarters()` ruft `StarterRandomizer.randomizeStarterHeldItems()` bei `Settings.isRandomizeStartersHeldItems()`.
- `GameRandomizer.maybeRandomizeTrainerHeldItems()` ruft `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` bei Boss-/Important-/Regular-Trainer-Held-Item-Flags.

### Wild/Encounter Held Items

- `Settings.randomizeWildPokemonHeldItems` aktiviert Wild-Held-Items.
- `Settings.banBadRandomWildPokemonHeldItems` schaltet den Pool von `getAllowedItems()` auf `getNonBadItems()`.
- `EncounterHeldItemRandomizer.randomizeWildHeldItems()` iteriert ueber `romHandler.getSpeciesSetInclFormes()`.
- Der Pfad schreibt auf `Species`-Felder: `guaranteedHeldItem`, `commonHeldItem`, `rareHeldItem` und optional `darkGrassHeldItem`.
- Der Pfad ueberschreibt nur Species, die bereits irgendeinen Held-Item-Slot besitzen; vollstaendig leere Held-Item-Species werden uebersprungen.
- Unsichere Items werden gefiltert, wenn Item oder Name fehlt oder der Name als Platzhalter `item #...` erscheint.
- `Gen3RomHandler` liest und schreibt Wild/Encounter-Held-Items ueber BaseStats Common-/Rare-Held-Item-Felder; gleiche Common/Rare-Werte bedeuten Guaranteed Item.

### Trainer Held Items

- `Settings.randomizeHeldItemsForBossTrainerPokemon` aktiviert Boss-Trainer-Held-Items.
- `Settings.randomizeHeldItemsForImportantTrainerPokemon` aktiviert Important-Trainer-Held-Items.
- `Settings.randomizeHeldItemsForRegularTrainerPokemon` aktiviert Regular-Trainer-Held-Items.
- `TrainerPokemonRandomizer.randomizeTrainerHeldItems()` iteriert ueber `romHandler.getTrainers()` und deren `TrainerPokemon`.
- Trainer mit `shouldNotGetBuffs()` werden uebersprungen.
- Boss/Important/Regular-Filter begrenzen, welche Trainerteams Items erhalten.
- `highestLevelGetsItemsForTrainers` kann den Write auf ein hoechstleveliges Teammitglied begrenzen.
- `sensibleItemsOnlyForTrainers` nutzt `romHandler.getSensibleHeldItemsFor(...)` und optional Moveset-Kontext.
- `consumableItemsOnlyForTrainers` nutzt `romHandler.getAllConsumableHeldItems()`.
- Sonst nutzt der Pfad `romHandler.getAllHeldItems()`.
- Z-Crystals und Mega Stones koennen preserve-only bleiben, wenn entsprechende Bedingungen greifen.
- `Gen3RomHandler` liest/schreibt Trainer-Held-Items in `TrainerPokemon.heldItem`; Teamdaten nutzen Trainer-Teamflags und 8-/16-Byte Team-Pokemon-Strukturen.

### Starter Held Items

- `Settings.randomizeStartersHeldItems` aktiviert Starter-Held-Items.
- `Settings.banBadRandomStarterHeldItems` schaltet den Pool von `getAllowedItems()` auf `getNonBadItems()`.
- `RomHandler.supportsStarterHeldItems()` gate-t die GUI-/Settings-Option.
- `StarterRandomizer.randomizeStarterHeldItems()` liest `romHandler.getStarterHeldItems()`, erzeugt eine gleich lange neue Itemliste und schreibt `romHandler.setStarterHeldItems(...)`.
- `Gen3RomHandler.supportsStarterHeldItems()` gibt `true` zurueck.
- Fuer Gen3/FRLG wird laut GUI-Hinweis ein gemeinsames Starter-Held-Item modelliert; `Gen3RomHandler.setStarterHeldItems(...)` akzeptiert nur eine Itemliste der Laenge 1.

### GUI-/Settings-Pfade

- `RandomizerGUI` schreibt Wild-Held-Items aus `wpRandomizeHeldItemsCheckBox` und `wpBanBadItemsCheckBox` in Settings.
- `RandomizerGUI` schreibt Starter-Held-Items aus `spRandomizeStarterHeldItemsCheckBox` und `spBanBadItemsCheckBox` in Settings.
- `RandomizerGUI` schreibt Trainer-Held-Items aus `tpBossTrainersItemsCheckBox`, `tpImportantTrainersItemsCheckBox`, `tpRegularTrainersItemsCheckBox` sowie Consumable/Sensible/Highest-Level-Optionen.
- `Bundle.properties` beschreibt die sichtbaren GUI-Texte fuer Wild, Starter und Trainer Held Items.
- `Settings.tweakForRom(...)` deaktiviert nicht unterstuetzte Held-Item-Optionen ueber `supportsStarterHeldItems()` und `canAddHeldItemsTo...Trainers()`.

## Erwartete Datenstruktur

### Wild/Encounter Held Items

- Zielstruktur: `Species` / BaseStats, nicht Encounter-Listen.
- Geaenderte Felder: Common Held Item, Rare Held Item, Guaranteed Held Item und optional Dark-Grass-Held-Item.
- In Gen3 schreibt `saveBasicPokeStats(...)` Common/Rare-Item-IDs zurueck in BaseStats-Felder.
- Reload muss per Species-/Forme-Identitaet vergleichen, nicht per Encounter-Slot.

### Trainer Held Items

- Zielstruktur: `Trainer` und `TrainerPokemon`.
- Geaendertes Feld: `TrainerPokemon.heldItem`.
- In Gen3 haengt die Schreibposition davon ab, ob Trainer-Teamflags Held Items und/oder Custom Moves nutzen.
- Reload muss Trainerklassifizierung, Teamgroessen, Teamflags, Species-/Forme-Zuordnung und Held-Item-ID pro TrainerPokemon erhalten.

### Starter Held Items

- Zielstruktur: eigener Starter-Held-Item-Pfad ueber `RomHandler.getStarterHeldItems()` / `setStarterHeldItems(...)`.
- In Gen3/FRLG ist ein gemeinsames Starter-Held-Item zu erwarten.
- Starter-Species selbst sind nicht Teil dieses Scopes; `getStarters()` / `setStarters(...)` bleiben unveraendert.

## Item-Pools und TM-Policy

- Wild Held Items und Starter Held Items nutzen `getAllowedItems()` oder bei Ban Bad `getNonBadItems()`.
- Wild Held Items filtern zusaetzlich null-/namenlose Placeholder-Items und `item #...`-Fallbacks.
- Trainer Held Items nutzen nicht denselben Allowed-/NonBad-Pool, sondern Held-Item-spezifische Pools: `getAllHeldItems()`, `getAllConsumableHeldItems()` oder `getSensibleHeldItemsFor(...)`.
- Eine explizite `canTMsBeHeld`-Policy wurde in den relevanten Pfaden nicht als Gate beobachtet; spaetere Diagnosen muessen TM-Held-Item-Zahlen trotzdem messen.
- Ban-Bad-Optionen existieren fuer Wild und Starter Held Items. Fuer Trainer Held Items sind die sichtbaren Poolfilter Consumable Only, Sensible Items und Highest Level Only; kein gleichnamiges Ban-Bad-Flag wurde als Trainer-Held-Items-Flag beobachtet.

## Preserve-/Skip-Policy

Wild/Encounter:

- Null-, invalid- und BaseStats-leere Species muessen preserve-only bleiben.
- Species ohne vorhandenen Held-Item-Slot werden durch den beobachteten Wild-Held-Item-Pfad uebersprungen.
- Forme-/Gen9-Species-Identitaet muss erhalten bleiben.
- Field Items, Pickup und Shops muessen unveraendert bleiben.

Trainer:

- Trainer mit `shouldNotGetBuffs()` bleiben preserve-only.
- Nicht aktivierte Trainerklassen bleiben preserve-only, wenn nur Boss, nur Important oder nur Regular getestet wird.
- Z-Crystals und Mega Stones koennen preserve-only sein und muessen als solche gemessen werden.
- Teamgroessen, Teamflags, Moves und Species duerfen im Held-Items-only Smoke nicht unbeabsichtigt veraendert werden.

Starter:

- Starter-Species bleiben preserve-only.
- Nur Starter-Held-Item-Felder werden gemessen.
- Falls der Kandidat keinen stabilen Starter-Held-Item-Pfad bietet, muss der Starter-Subscope blockiert bleiben.

## Risiken / Blocker

- Falsche Zielstruktur: Wild-Held-Items schreiben BaseStats/Species, nicht Encounter-Slots; ein falscher Vergleich koennte echte Writes uebersehen.
- Trainer-Teamflags: Held-Item-Writes koennen Team-Pokemon-Strukturbreite oder Itemflag-Verhalten beruehren.
- Forme-/Gen9-Species-Mapping: SpeciesSet- und Forme-Identitaet muss stabil bleiben, besonders bei CFRU/DPE Gen9-Pools.
- Invalid/unloaded/fallback/placeholder Item IDs koennen bei modernen Itemlisten falsche Writes erzeugen.
- Bad-Item-Pool: Wild/Starter Ban-Bad-Pfade muessen separat getestet werden; Trainer nutzt andere Poolfilter.
- TM-Held-Policy: TMs muessen gemessen werden, auch wenn kein eigener `canTMsBeHeld`-Gate beobachtet wurde.
- Reload-Mismatches: BaseStats-, Trainer- und Starter-Held-Item-Writes brauchen getrennte Reload-Vergleiche.
- Fremdscope-Veraenderungen: Field Items, Pickup und Shops muessen in Held-Items-Smokes unveraendert bleiben.
- Moveset-Kontext: Trainer sensible-item mode kann Moveset-Lesen ausloesen; erster Smoke sollte diesen Filter nicht aktivieren.

## Muss zuerst eine read-only Kandidatendiagnose laufen?

Ja.

Vor jedem Write-/Reload-Smoke muss eine read-only Held-Items-Kandidatendiagnose fuer denselben CFRU/DPE Gen9-BPRE-Kandidaten laufen. Sie muss ohne ROM-Write, Save, Build, Output-ROM und private Artefaktdokumentation klaeren:

- ob Wild/Encounter-Held-Items ueber Species/BaseStats sichtbar sind
- wie viele Species/Formes vorhandene Held-Item-Slots besitzen
- ob Trainer-Held-Item-Strukturen lesbar sind
- ob Boss/Important/Regular-Trainerklassifizierung fuer den Kandidaten stabil ist
- ob Starter-Held-Items unter Gen3/FRLG sichtbar und schreibmodelliert sind
- welche invalid/unloaded/fallback/placeholder/bad/TM-Item-Zaehler im Bestand existieren
- ob Field/Pickup/Shop-Fingerprints read-only stabil bleiben

## Spaetere Diagnose-/Smoke-Metriken

Pflichtmetriken fuer die read-only Diagnose:

```text
candidateFilesChecked
candidateLoaded
heldItemScanSuccessful
wildHeldItemsTotal
wildHeldSpeciesWithAnyHeldItem
wildHeldGuaranteedCount
wildHeldCommonCount
wildHeldRareCount
wildHeldDarkGrassCount
trainerHeldItemsTotal
trainerPokemonTotal
trainerBossPokemonTotal
trainerImportantPokemonTotal
trainerRegularPokemonTotal
starterHeldItemsTotal
starterHeldItemsSupported
invalidHeldItemIds
unloadedHeldItemIds
fallbackHeldItems
placeholderHeldItems
badHeldItems
tmHeldItems
heldItemPoolAllowedSize
heldItemPoolNonBadSize
trainerAllHeldItemPoolSize
trainerConsumableHeldItemPoolSize
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass
stacktrace
```

Pflichtmetriken fuer spaetere Write-/Reload-Smokes:

```text
candidateLoaded
smokeExecuted
saveSuccessful
logSuccessful
outputRomExists
logNonEmpty
reloadSuccessful
wildHeldItemsBefore/After/Reload
trainerHeldItemsBefore/After/Reload
starterHeldItemsBefore/After/Reload
heldItemReloadMismatches
wildHeldItemReloadMismatches
trainerHeldItemReloadMismatches
starterHeldItemReloadMismatches
invalidHeldItemWrites
unloadedHeldItemWrites
fallbackHeldItemWrites
placeholderHeldItemWrites
badHeldItemWrites
tmHeldItemWrites
preservedSpeciesHeldItemMismatches
preservedTrainerHeldItemMismatches
preservedStarterSpeciesMismatches
trainerTeamCountBefore/After/Reload
trainerPokemonCountBefore/After/Reload
trainerTeamFlagMismatches
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass
stacktrace
```

Pool-spezifische Zusatzmetriken:

```text
banBadWildHeldItemPoolCandidates
banBadWildHeldItemPoolExcluded
banBadStarterHeldItemPoolCandidates
banBadStarterHeldItemPoolExcluded
trainerSensibleItemPoolClassifiable
trainerConsumableOnlyPoolClassifiable
highestLevelOnlyTargets
zCrystalPreservedCount
megaStonePreservedCount
```

## Empfohlene Diagnose-/Smoke-Reihenfolge

1. Held Items read-only Kandidatendiagnose.
2. Wild/Encounter Held Items Smoke ohne Ban Bad.
3. Wild/Encounter Held Items + Ban Bad Smoke, falls der erste Smoke reloadstabil ist.
4. Trainer Held Items Smoke mit einem engen ersten Scope, empfohlen Boss Trainers only, ohne Consumable/Sensible/Highest-Level-Filter.
5. Trainer Held Items weitere Trainerklassen und Poolfilter separat.
6. Starter Held Items Smoke, nur falls die read-only Diagnose einen stabilen eigenen Starter-Held-Item-Pfad bestaetigt.
7. Starter Held Items + Ban Bad separat, falls Starter-Basis reloadstabil ist.

## Feature-Status

- Shop Items Scope: abgeschlossen im getesteten CFRU/DPE Gen9-BPRE Scope nach Diagnose 136.
- Held Items Scope: Plan erstellt; keine Held-Item-Feature-Hochstufung in diesem Block.
- Field Items, Pickup und Shops bleiben unveraendert.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-held-items-scope-diagnostics`: read-only Held-Items-Kandidatendiagnose fuer Wild/Encounter-, Trainer- und Starter-Held-Item-Strukturen.
