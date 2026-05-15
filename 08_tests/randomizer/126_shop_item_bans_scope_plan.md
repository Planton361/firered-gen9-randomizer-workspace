# Diagnose 126 - Shop Item Bans scope plan

Datum: 2026-05-15

## Ziel

Dieser Block plant `FVX-ITEM-007 Shop Item Bans` als separaten Shop-only Subscope nach dem erfolgreichen Shop Random Smoke aus Diagnose 125.

Der Block ist read-only:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Lauf
- kein ROM-/Artefaktzugriff
- kein Shop Write/Save

## Scope

Nur `FVX-ITEM-007 Shop Item Bans` wird geplant.

Getrennt betrachtet:

- `banBadRandomShopItems`
- `banRegularShopItems`
- `banOPShopItems`

Ausserhalb des Scopes:

- `FVX-ITEM-008 Guarantee Evolution/X Items`
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`
- Field Items
- Pickup
- Held Items
- TM/HM/Tutor/Learnset
- Encounter, Trainer, Starter, Wild, Evolution
- Text/Menu
- Palette/Graphics
- MoveData/MoveNames
- TypeChart/TypeEffectiveness

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/124_shop_items_shuffle_reload_smoke.md`
- `08_tests/randomizer/125_shop_items_random_reload_smoke.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Read-only Suche

Verwendet wurden nur `rg`, `rg --files` und kurze gezielte Dateiauszuege.

Suchbegriffe:

- `banBadRandomShopItems`
- `banRegularShopItems`
- `banOPShopItems`
- `randomizeShopItems`
- `shuffleShopItems`
- `ShopItemsMod`
- `Settings`
- `GameRandomizer`
- `maybeRandomizeShops`
- `ItemRandomizer`
- `ItemList`
- `getAllowedItems`
- `getNonBadItems`
- `isBad`
- `isAllowed`
- `isTM`
- `getShops`
- `setShops`
- `Shop`
- `Gen3RomHandler`
- `RomHandler`
- `Bundle.properties`
- `RandomizerGUI`

## Ban-Scope-Einschaetzung

`FVX-ITEM-007 Shop Item Bans` ist ein eigener Shop-only Subscope.

Begruendung:

- Diagnose 124 belegt nur `FVX-ITEM-005 Shop Items Shuffle`.
- Diagnose 125 belegt nur `FVX-ITEM-006 Shop Items Random` ohne aktive Ban-/Guarantee-/Preisoptionen.
- Die Ban-Flags veraendern nicht den Shoplisten-Writer selbst, sondern den Kandidatenpool fuer `randomizeShopItems()`.
- Ban Bad, Ban Regular und Ban OP haben unterschiedliche Poolquellen und sollten deshalb nicht gemeinsam als erstes getestet werden.
- Field Items, Pickup und Held Items sind nicht betroffen und werden nicht aus dem Shop-Ban-Scope hochgestuft.

`FVX-ITEM-007` bleibt bis zu einem eigenen Shop-only Write/Reload-Smoke `Write modelliert`.

## Relevante Codepfade

- `Settings.ShopItemsMod`: `UNCHANGED`, `SHUFFLE`, `RANDOM`.
- `Settings.banBadRandomShopItems`: Settings-Flag fuer Ban Bad im Shop-Random-Pool.
- `Settings.banRegularShopItems`: Settings-Flag fuer Regular-Shop-Item-Ausschluss.
- `Settings.banOPShopItems`: Settings-Flag fuer OP-Shop-Item-Ausschluss.
- `RandomizerGUI`: liest und schreibt die Shop-Radio-Buttons und Checkboxes:
  - `shRandomRadioButton`
  - `shShuffleRadioButton`
  - `shUnchangedRadioButton`
  - `shBanBadItemsCheckBox`
  - `shBanRegularShopItemsCheckBox`
  - `shBanOverpoweredShopItemsCheckBox`
- `Bundle.properties`: beschreibt die drei Shop-Ban-Checkboxen als Shop-Item-Pool-Filter.
- `GameRandomizer.maybeRandomizeShops()`: ruft bei `ShopItemsMod.SHUFFLE` nur `shuffleShopItems()` auf; bei `ShopItemsMod.RANDOM` ruft es `randomizeShopItems()` auf.
- `ItemRandomizer.randomizeShopItems()`: kopiert Shops, baut den Pool ueber `setupPossible()`, platziert neue Items und schreibt ueber `romHandler.setShops(...)`.
- `ItemRandomizer.setupPossible()`:
  - startet mit `romHandler.getNonBadItems()` wenn `banBadRandomShopItems=true`
  - sonst mit `romHandler.getAllowedItems()`
  - entfernt danach TMs per `possible.removeIf(Item::isTM)`
  - entfernt bei `banRegularShopItems=true` `romHandler.getRegularShopItems()`
  - entfernt bei `banOPShopItems=true` `romHandler.getOPShopItems()`
- `AbstractRomHandler.getAllowedItems()`: alle geladenen erlaubten Items.
- `AbstractRomHandler.getNonBadItems()`: erlaubte Items ohne `Item.isBad()`.
- `AbstractRomHandler.getRegularShopItems()`: globale Regular-Shop-Item-Klasse.
- `Gen3RomHandler.getOPShopItems()`: Gen3-spezifische OP-Shop-Item-Klasse.
- `Gen3RomHandler.getShops()` / `setShops(...)`: Shoplisten-Reader/-Writer mit `DataRewriter<Shop>`-Repointing-Risiko.

## Wirkung der Ban-Flags

Die Ban-Flags wirken im untersuchten Codepfad nur fuer `ShopItemsMod.RANDOM`.

Einordnung:

- `ShopItemsMod.UNCHANGED`: `GameRandomizer.maybeRandomizeShops()` ruft keinen Shop-Item-Randomizer auf; Ban-Flags haben keine Shoplisten-Wirkung.
- `ShopItemsMod.SHUFFLE`: `maybeRandomizeShops()` ruft `shuffleShopItems()` auf; `shuffleShopItems()` nutzt die Ban-Flags nicht.
- `ShopItemsMod.RANDOM`: `maybeRandomizeShops()` ruft `randomizeShopItems()` auf; dort wirkt `setupPossible()` mit den drei Ban-Flags.

Folge fuer Tests:

- Ban-Smokes muessen als `ShopItemsMod.RANDOM` laufen.
- Ein Shop Shuffle + Ban Smoke waere nicht aussagekraeftig fuer `FVX-ITEM-007`.
- Preis-/Rare-Candy-Optionen bleiben deaktiviert, weil sie eigene Pfade nach dem Random-/Shuffle-Block ausloesen.

## Pool-/Flag-Befund

Baseline aus Diagnose 125:

- `allowedShopItemPoolSize=536`
- `nonBadShopItemPoolSize=485`
- Differenz fuer Ban Bad: `51` potenzielle Bad-Pool-Kandidaten werden gegenueber dem no-ban Pool ausgeschlossen.
- `badShopItemsBefore=36`, `badShopItemsAfter=36`, `badShopItemsReload=36` sind Bestand im Shop-Set aus dem no-ban Random-Smoke, kein Ban-Ergebnis.
- `tmShopItemsBefore=6`, `tmShopItemsAfter=6`, `tmShopItemsReload=6` sind Bestand; der Random-Pool entfernt TMs vor der Platzierung.

Weitere Poolklassen:

- `banRegularShopItems` entfernt `getRegularShopItems()` aus dem bereits TM-bereinigten Pool.
- `banOPShopItems` entfernt `getOPShopItems()` aus dem bereits TM-bereinigten Pool.
- Die konkreten Regular-/OP-Write-Metriken sollten im Smoke ueber klassifizierbare Set-Zugehoerigkeit gemessen werden.

## Empfohlene Ban-Testreihenfolge

1. Shop Random + Ban Bad Smoke.
2. Shop Random + Ban Regular Smoke, falls Regular-Shop-Item-Klassifikation im Harness klar messbar ist.
3. Shop Random + Ban OP Smoke, falls OP-Shop-Item-Klassifikation im Harness klar messbar ist.
4. Kombinationen erst nach erfolgreichen Einzel-Smokes.

Erster Smoke:

- `Settings.ShopItemsMod=RANDOM`
- `banBadRandomShopItems=true`
- `banRegularShopItems=false`
- `banOPShopItems=false`
- `guaranteeEvolutionItems=false`
- `guaranteeXItems=false`
- `balanceShopPrices=false`
- `addCheapRareCandiesToShops=false`

Warum Ban Bad zuerst:

- Diagnose 125 liefert bereits `allowedShopItemPoolSize=536` und `nonBadShopItemPoolSize=485`.
- Ban Bad ist direkt als Wechsel von `getAllowedItems()` zu `getNonBadItems()` modelliert.
- Erwartete Kandidatendifferenz ist klar: `banBadShopItemPoolCandidates=51`, `banBadShopItemPoolExcluded=51`.
- Bad-Item-Write-Metriken sind ueber `Item.isBad()` direkt klassifizierbar.

## Spaetere Smoke-Metriken

Pflichtmetriken fuer Shop Random + Ban Bad:

```text
candidateFilesChecked
candidateLoaded
smokeExecuted
saveSuccessful
logSuccessful
outputRomExists
logNonEmpty
reloadSuccessful
shopCountBefore
shopCountAfter
shopCountReload
shopItemsTotalBefore
shopItemsTotalAfter
shopItemsTotalReload
minShopLengthBefore
minShopLengthAfter
minShopLengthReload
maxShopLengthBefore
maxShopLengthAfter
maxShopLengthReload
terminatorModelStableAfter
terminatorModelStableReload
shopLengthMismatchesAfter
shopLengthMismatchesReload
shopItemReloadMismatches
skippedShopItemMismatchesAfter
skippedShopItemMismatchesReload
specialShopPolicyMismatches
invalidShopItemWrites
unloadedShopItemWrites
fallbackShopItemWrites
placeholderShopItemWrites
badShopItemWrites
regularShopItemBannedWrites
opShopItemBannedWrites
allowedShopItemPoolSize
nonBadShopItemPoolSize
banBadShopItemPoolCandidates
banBadShopItemPoolExcluded
priceTableTouched=false
priceReloadMismatches=0
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
exceptionClass
stacktrace
```

Zusatzmetriken fuer spaetere Regular-/OP-Smokes:

```text
regularShopItemPoolCandidates
regularShopItemPoolExcluded
regularShopItemBannedWrites
opShopItemPoolCandidates
opShopItemPoolExcluded
opShopItemBannedWrites
```

## Risiken / Blocker

- Ban Regular und Ban OP brauchen eine klare, harnessseitig messbare Set-Klassifikation gegen `getRegularShopItems()` und `getOPShopItems()`.
- Kombinationen koennen Poolgroessen stark reduzieren und sollten erst nach Einzel-Smokes laufen.
- `DataRewriter<Shop>` / Repointing bleibt ein Reload-Kriterium, obwohl Ban-Flags nur den Pool veraendern.
- Skipped Shops muessen preserve-only bleiben.
- Preisfelder duerfen bei Ban-Smokes unveraendert bleiben.
- Existing bad Shop inventory aus Diagnose 123/125 darf nicht als Ban-Fehler missverstanden werden; massgeblich sind neue Writes in randomisierten Special Shops.

## Feature-Status

- `FVX-ITEM-005 Shop Items Shuffle`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope aus Diagnose 124.
- `FVX-ITEM-006 Shop Items Random`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope aus Diagnose 125.
- `FVX-ITEM-007 Shop Item Bans`: bleibt `Write modelliert`; dieser Block plant nur den Smoke-Scope.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: unveraendert `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: unveraendert `Write modelliert`.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`: Shop-only Write/Reload-Smoke fuer `ShopItemsMod.RANDOM` mit nur `banBadRandomShopItems=true`.
