# Diagnose 133 - Shop Prices / Cheap Rare Candies Scope Plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-shop-prices-cheap-rare-candies-scope-plan`
Scope: Read-only plan for `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`

## Ziel

Dieser Block plant `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies` als separaten Shop-only Subscope nach den einzeln reloadstabilen Shop Items-, Ban- und Guarantee-Smokes.

Der Block ist read-only:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Lauf
- kein ROM-/Artefaktzugriff
- kein Shop Write/Save

## Scope

Nur `FVX-ITEM-009` wird geplant.

Getrennt betrachtet:

- Balance Shop Prices
- Cheap Rare Candies / `addCheapRareCandiesToShops`

Ausserhalb des Scopes:

- Evolution+X-Kombination fuer `FVX-ITEM-008`; optionaler spaeterer Follow-up, aber kein Test in diesem Block
- Ban-Kombinationen fuer `FVX-ITEM-007`
- Field Items
- Pickup
- Held Items
- ROMs, Saves, Emulator States, Builds, Logs, Output-ROMs und Tool-Binaries

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten wurden nicht dokumentiert.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/123_shop_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/125_shop_items_random_reload_smoke.md`
- `08_tests/randomizer/130_shop_guarantee_items_scope_plan.md`
- `08_tests/randomizer/131_shop_guarantee_evolution_items_reload_smoke.md`
- `08_tests/randomizer/132_shop_guarantee_x_items_reload_smoke.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Read-only Suche

Verwendet wurden `rg`, `rg --files` und gezielte Dateiauszuege. Es gab keinen Build, keinen Randomizer-Lauf und keinen ROM-/Artefaktzugriff.

Suchbegriffe:

- `balanceShopPrices`
- `addCheapRareCandiesToShops`
- `getShopPrices`
- `setShopPrices`
- `ShopItemsMod`
- `Settings`
- `GameRandomizer`
- `maybeRandomizeShops`
- `ItemRandomizer`
- `setupNewItems`
- `placeNewItems`
- `getShops`
- `setShops`
- `Shop`
- `Gen3RomHandler`
- `RomHandler`
- `Rare Candy`
- `RandomizerGUI`
- `Bundle.properties`

## FVX-ITEM-009-Scope-Einschaetzung

`FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies` ist ein eigener Shop-only Preis-/Rare-Candy-Subscope.

Begruendung:

- Diagnose 124 belegt `FVX-ITEM-005 Shop Items Shuffle`.
- Diagnose 125 belegt `FVX-ITEM-006 Shop Items Random` ohne Preis- oder Rare-Candy-Optionen.
- Diagnose 127, 128 und 129 belegen `FVX-ITEM-007` fuer Ban Bad, Ban Regular und Ban OP jeweils einzeln, nicht fuer Ban-Kombinationen.
- Diagnose 131 und 132 belegen `FVX-ITEM-008` fuer Guarantee Evolution Items und Guarantee X Items jeweils einzeln, nicht fuer die Evolution+X-Kombination.
- Balance Shop Prices schreibt keine Shoplisten, sondern Item-Preisfelder.
- Cheap Rare Candies schreibt Shoplisten und setzt den Rare-Candy-Preis; damit vermischt es Shoplisten-Repointing und Preiswriter und braucht einen separaten Smoke.

`FVX-ITEM-009` bleibt bis zu eigenen Shop-only Write/Reload-Smokes `Write modelliert`.

## Relevante Codepfade

- `Settings.balanceShopPrices`: GUI-/Settings-Flag fuer Balance Shop Item Prices.
- `Settings.addCheapRareCandiesToShops`: GUI-/Settings-Flag fuer Add Cheap Rare Candies.
- `RandomizerGUI`: liest und schreibt `shBalanceShopItemPricesCheckBox` und `shAddRareCandyCheckBox` in `Settings`.
- `Bundle.properties`: beschreibt `Balance Shop Item Prices` und `Add Cheap Rare Candies` als Shop-Suboptionen.
- `GameRandomizer.maybeRandomizeShops()`: fuehrt zuerst je nach `ShopItemsMod` Shuffle oder Random aus; danach laufen `romHandler.setBalancedShopPrices()` und `itemRandomizer.addCheapRareCandiesToShops()` separat, falls ihre Flags aktiv sind.
- `AbstractRomHandler.setBalancedShopPrices()`: liest `getShopPrices()`, ersetzt Eintraege aus `getBalancedShopPrices()` und schreibt `setShopPrices(...)`.
- `Gen3RomHandler.getShopPrices()`: liest Preise aus ItemData-Preisfeldern in eine Liste mit Item-Standard-IDs.
- `Gen3RomHandler.setShopPrices(...)`: schreibt Preiswerte zurueck in ItemData-Preisfelder; die Listengroesse muss zur Itemliste passen.
- `ItemRandomizer.addCheapRareCandiesToShops()`: ruft `addRareCandiesToShops()`, danach `makeRareCandiesCheap()` und setzt `shopChangesMade=true`.
- `ItemRandomizer.addRareCandiesToShops()`: fuegt jedem Shop ein Rare Candy hinzu und schreibt die Shops ueber `romHandler.setShops(...)`.
- `ItemRandomizer.makeRareCandiesCheap()`: setzt den Rare-Candy-Preis auf einen niedrigen Wert und schreibt ueber `setShopPrices(...)`.
- `RomHandler.canChangeShopSizes()`: erlaubt bei unterstuetzten Handlern das Entfernen beliebiger Items und das Hinzufuegen von bis zu einem Item pro Shop; die GUI zeigt/aktiviert Cheap Rare Candies daran gekoppelt.
- `Gen3RomHandler.canChangeShopSizes()`: gibt fuer Gen3 `true` zurueck.
- `Gen3RomHandler.setShops(...)`: schreibt terminierte Shoplisten ueber `DataRewriter<Shop>` und kann repointen.

## Preis-/Rare-Candy-Policy-Befund

### Balance Shop Prices

- Balance Shop Prices wirkt unabhaengig von `ShopItemsMod`, weil `maybeRandomizeShops()` die Preisoption nach dem `ShopItemsMod`-Switch prueft.
- Die Option kann also auch bei `ShopItemsMod.UNCHANGED` Preisfelder schreiben.
- Der Pfad schreibt ueber `getShopPrices()` / `setShopPrices(...)` und ist getrennt von Shoplisten, Terminatoren und `DataRewriter<Shop>`.
- Fuer den ersten Smoke sollte `ShopItemsMod.UNCHANGED` gesetzt werden, damit nur Preisfelder getestet werden.

### Cheap Rare Candies

- Cheap Rare Candies wirkt ebenfalls als eigene Option nach dem `ShopItemsMod`-Switch.
- Der Pfad veraendert Shoplisten: jedem Shop wird ein Rare Candy angehaengt.
- Danach wird der Rare-Candy-Preis ueber `getShopPrices()` / `setShopPrices(...)` gesetzt.
- Dieser Smoke muss daher Shoplisten-Laengenwachstum, Terminatoren, `DataRewriter`/Repointing und Preis-Reload gemeinsam messen.
- Der GUI-Pfad ist an `romHandler.canChangeShopSizes()` gekoppelt; Gen3 meldet `true`.
- SkipShops sind bei Cheap Rare Candies nicht automatisch preserve-only, weil `addRareCandiesToShops()` ueber alle Shops iteriert. Der Smoke muss deshalb nicht dieselbe Skip-Preserve-Erwartung wie Random/Shuffle/Ban/Guarantee verwenden, sondern gezielt pruefen, ob die dokumentierte Option bewusst alle Shops erweitert.

## Risiken / Blocker

- Preisfelder falsch geschrieben: `setShopPrices(...)` schreibt ItemData-Preisfelder nach Item-Standard-ID-Mapping; falsche IDs oder Listenlaengen koennen falsche Preise setzen.
- Preis-Reload-Mismatches: Preise muessen nach Reload exakt wieder lesbar sein.
- Shoplisten-Laengenaenderung durch Rare Candies: jedes hinzugefuegte Rare Candy verlaengert Shoplisten und erzwingt Terminator-/Laengen-/Reload-Pruefung.
- Terminatoren: Rare-Candy-Anhaenge koennen terminierte `u16`-Shopstreams verschieben; fehlende oder falsch gesetzte Terminatoren koennen Shops zusammenlaufen lassen.
- `DataRewriter` / Repointing: `setShops(...)` kann Shoplisten repointen; Reload muss gueltige Struktur nachweisen.
- SkipShops: fuer Balance Prices muessen Shoplisten unveraendert bleiben; fuer Cheap Rare Candies muss bewusst dokumentiert werden, ob SkipShops ebenfalls ein Rare Candy erhalten.
- Field/Pickup/Held: alle Fremdscopes muessen unveraendert bleiben.
- Kombinationen: Balance Prices + Cheap Rare Candies erst nach stabilen Einzel-Smokes; Ban-Kombinationen und Evolution+X bleiben getrennte Follow-ups.

## Empfohlene Testreihenfolge

1. Balance Shop Prices Smoke.
2. Cheap Rare Candies Smoke.
3. Kombination Balance Shop Prices + Cheap Rare Candies nur nach stabilen Einzel-Smokes.

Empfohlener erster Smoke:

- `ShopItemsMod=UNCHANGED`
- `balanceShopPrices=true`
- `addCheapRareCandiesToShops=false`
- alle Ban- und Guarantee-Flags `false`
- Field Items, Pickup und Held Items unveraendert

Empfohlener zweiter Smoke:

- `ShopItemsMod=UNCHANGED`
- `balanceShopPrices=false`
- `addCheapRareCandiesToShops=true`
- alle Ban- und Guarantee-Flags `false`
- Field Items, Pickup und Held Items unveraendert

## Spaetere Smoke-Metriken

Pflichtmetriken fuer FVX-ITEM-009-Smokes:

```text
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
terminatorModelStableAfter
terminatorModelStableReload
shopLengthMismatchesAfter
shopLengthMismatchesReload
shopItemReloadMismatches
priceTableReadable
priceTableTouched
priceEntriesBefore
priceEntriesAfter
priceEntriesReload
priceReloadMismatches
balancedPriceWrites
cheapRareCandyWrites
cheapRareCandyReloadPresent
skippedShopItemMismatchesAfter
skippedShopItemMismatchesReload
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
exceptionClass
stacktrace
```

Zusatzmetriken empfohlen:

```text
rareCandyPriceBefore
rareCandyPriceAfter
rareCandyPriceReload
shopsWithRareCandyBefore
shopsWithRareCandyAfter
shopsWithRareCandyReload
rareCandyAdditionsAfter
rareCandyAdditionsReload
skipShopRareCandyAdditionsAfter
skipShopRareCandyAdditionsReload
priceOnlyShopItemsChanged=false fuer Balance-Only
shopLengthGrowthExpected=true fuer Cheap-Rare-Candy-Smoke
```

## Feature-Status

- `FVX-ITEM-005 Shop Items Shuffle`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope.
- `FVX-ITEM-006 Shop Items Random`: bleibt `GUI-kompatibel` im getesteten Shop-only Scope.
- `FVX-ITEM-007 Shop Item Bans`: Ban Bad, Ban Regular und Ban OP sind jeweils einzeln `GUI-kompatibel`; Ban-Kombinationen bleiben optional separat.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: Guarantee Evolution Items und Guarantee X Items sind jeweils einzeln `GUI-kompatibel`; die Evolution+X-Kombination bleibt optional separat.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: bleibt bis Smoke `Write modelliert`.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-shop-balance-prices-reload-smoke`: Shop-only Write/Reload-Smoke fuer `ShopItemsMod.UNCHANGED` mit nur `balanceShopPrices=true`.
