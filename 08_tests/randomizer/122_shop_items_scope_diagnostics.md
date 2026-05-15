# 122 - CFRU/DPE Shop Items Scope Diagnostics

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-shop-items-scope-diagnostics`
UPR-FVX-Pin: `a2373888ad17145f270ebf6ff17303af41aa86eb`

## Scope

Dieser Block ist eine read-only Shop-Kandidatendiagnose fuer den CFRU/DPE Gen9-BPRE Shop-Items-Scope.

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Write oder Save
- kein Output-ROM
- keine Logs oder Builds als Artefakte
- keine Shop Writes
- keine Field Items
- kein Pickup
- keine Held Items
- keine Preisveraenderungen
- keine Guarantee-, Ban-, Shuffle- oder Random-Smokes
- keine ROMs, Saves, Emulator States, Tool-Binaries oder private Artefakte dokumentieren
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentieren

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/121_shop_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Read-only Codepfad-Suche

Verwendet wurden nur `rg`-Suchen in UPR-FVX-Quelltexten. Es gab keinen Build, keinen Randomizer-Lauf, keinen ROM-Zugriff und keine private Kandidatensuche.

Suchbegriffe:

- `getShops`
- `setShops`
- `ShopPointerOffsets`
- `MainGameShops`
- `SkipShops`
- `Shop`
- `DataRewriter`
- `getShopPrices`
- `setShopPrices`
- `ItemRandomizer`
- `randomizeShopItems`
- `shuffleShopItems`
- `addCheapRareCandiesToShops`
- `guaranteeEvolutionItems`
- `guaranteeXItems`
- `banBadRandomShopItems`
- `banRegularShopItems`
- `banOPShopItems`
- `Settings.ShopItemsMod`
- `GameRandomizer.maybeRandomizeShops`
- `Gen3RomHandler`
- `RomHandler`
- `ItemList`

## Kandidatenstatus

Fuer diesen Block wurde keine explizit freigegebene lokale CFRU/DPE Gen9-BPRE-Kandidatenquelle angegeben. Deshalb wurde keine private Suche ausgeweitet und kein ROM beruehrt.

Die Diagnose ist damit ein blocked/preflight-Protokoll: Der Shop-Reader-/Strukturpfad ist dokumentiert, aber keine fachliche Shop-Struktur eines Kandidaten wurde gescannt.

## Diagnose-Ergebnis

```text
candidateFilesChecked=0
candidateLoaded=false
shopScanSuccessful=false
shopCount=not_available
mainGameShopCount=not_available
skippedShopCount=not_available
specialShopCount=not_available
emptyShopCount=not_available
shopItemsTotal=not_available
minShopLength=not_available
maxShopLength=not_available
terminatorModelStable=not_available
shopLengthMismatch=not_available
invalidShopItemIds=not_available
unloadedShopItemIds=not_available
fallbackShopItems=not_available
placeholderShopItems=not_available
badShopItems=not_available
tmShopItems=not_available
shopPointerModelObserved=true
dataRewriterOrRepointingRisk=true
skipShopsPreserved=not_available
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
priceTableTouched=false
exceptionClass=none
stacktrace=none
```

## Shop-Struktur aus Codepfad

- `RomHandler.getShops()` / `setShops(...)` definieren die gemeinsame Shop-API.
- `RomHandler.getShopPrices()` / `setShopPrices(...)` definieren die getrennte Preis-API.
- `Gen3RomHandler.getShops()` liest Gen3/BPRE-Shops aus `ShopPointerOffsets`.
- `MainGameShops` markiert Main-Game-Shops fuer spaetere Guarantee-Placement-Policy.
- `SkipShops` markiert Shops, die nicht randomisiert werden sollen.
- `Shop` transportiert `items`, `name`, `isMainGame` und `isSpecialShop`.
- Gen3-Shoplisten sind terminierte Itemlisten; der Terminator ist nicht Teil von `Shop.items`.
- `Gen3RomHandler.setShops(...)` nutzt `DataRewriter<Shop>` und ist deshalb ein potenzieller Repointing-Pfad.
- `Gen3RomHandler.getShopPrices()` und `setShopPrices(...)` laufen ueber Itempreisfelder und sind getrennt vom Shoplisten-Writer zu behandeln.

## Risiken / Blocker

Aktiver Blocker fuer einen Shop Shuffle Smoke:

- Es gibt noch keinen fachlichen read-only Kandidatenscan fuer die aktive CFRU/DPE Gen9-BPRE-Shopstruktur.
- Ohne Kandidatenscan sind `shopCount`, Shoplaengen, Terminatorstabilitaet, Skip-/Special-/MainGame-Verteilung und Item-Safety nicht belegt.

Weiterhin relevante Risiken:

- Terminatoren koennen bei falscher Laengenbehandlung Shops abschneiden oder zusammenlaufen lassen.
- `DataRewriter<Shop>` kann repointen; spaetere Smokes muessen Pointer-/Reload-Stabilitaet explizit nachweisen.
- `SkipShops` und Special-Shop-Policy duerfen nicht versehentlich invertiert werden.
- `MainGameShops` ist relevant fuer Guarantee Evolution/X Items und darf nicht mit Random/Shuffle gleichgesetzt werden.
- Preislogik bleibt separat; `priceTableTouched=false` fuer diesen Block.
- Bad-/Regular-/OP-Bans sind nicht getestet und bleiben Shop-only spaeter zu pruefen.

## Preserve-/Skip-Befund

- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`
- `priceTableTouched=false`
- `skipShopsPreserved=not_available`, weil kein Kandidatenscan lief.
- Keine Field-Items-, Pickup-, Held-Items-, Preis- oder Shop-Write-Pfade wurden ausgefuehrt.

## Feature-Status

- `FVX-ITEM-005 Shop Items Shuffle`: bleibt `Write modelliert` / blocked bis ein Kandidatenscan Shopstruktur und Terminatoren bestaetigt.
- `FVX-ITEM-006 Shop Items Random`: bleibt `Write modelliert`.
- `FVX-ITEM-007 Shop Item Bans`: bleibt `Write modelliert`.
- `FVX-ITEM-008 Guarantee Evolution/X Items`: bleibt `Write modelliert`.
- `FVX-ITEM-009 Balance Shop Prices / Cheap Rare Candies`: bleibt `Write modelliert`.
- Field Items, Pickup und Held Items werden nicht geaendert oder hochgestuft.

## Naechster minimaler Schritt

Eine explizit freigegebene lokale CFRU/DPE Gen9-BPRE-Kandidatenquelle fuer eine read-only Shop-Strukturdiagnose bereitstellen. Danach denselben Scope erneut ausfuehren und nur aggregierte Shop-, Terminator-, Laengen-, Policy-, Item-Safety- und Preislese-Metriken dokumentieren. Kein Shop Shuffle Smoke vor erfolgreichem read-only Kandidatenscan.
