# Diagnose 129: Shop Items Random + Ban OP Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-op-reload-smoke`
Scope: Shop-only `FVX-ITEM-007` Subscope fuer `ShopItemsMod.RANDOM` mit `banOPShopItems=true`

## Ziel

Dieser Block prueft ausschliesslich den Shop-Random-Pfad mit aktivierter OP-Shop-Item-Ban-Option.

In Scope:
- `Settings.ShopItemsMod = RANDOM`
- `banBadRandomShopItems=false`
- `banRegularShopItems=false`
- `banOPShopItems=true`
- Shop-only Write/Reload-Smoke auf der lokal freigegebenen CFRU/DPE Gen9-BPRE-Kandidatenquelle

Out of Scope:
- Ban Bad und Regular-Ban
- Ban-Kombinationen
- Guarantee Evolution Items und Guarantee X Items
- `balanceShopPrices` und `addCheapRareCandiesToShops`
- Field Items, Pickup Items und Held Items
- Codeaenderungen, Builds, Submodule-Pin-Aenderungen und Upstream-Kontakte

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten wurden nicht dokumentiert.
Lokale Output-ROM-, Log- und Harness-Artefakte blieben ignoriert.

## Vorbedingung

`getOPShopItems()` wurde read-only im temporaeren Harness geprueft und war eindeutig nutzbar:

- `opShopSetClassifiable=true`
- `opShopItemPoolCandidates=9`
- `opShopItemPoolExcluded=9`

Damit war der Smoke ausfuehrbar; kein Blocked-/Preflight-Abbruch war noetig.

## Baseline

- `FVX-ITEM-005` ist im getesteten Shop-only Shuffle-Scope GUI-kompatibel.
- `FVX-ITEM-006` ist im getesteten Shop-only Random-Scope GUI-kompatibel.
- `FVX-ITEM-007` Ban Bad ist im getesteten `Shop Random + Ban Bad`-Scope reloadstabil.
- `FVX-ITEM-007` Ban Regular ist im getesteten `Shop Random + Ban Regular`-Scope reloadstabil.
- Diagnose 126 bestaetigt: `banOPShopItems` entfernt `getOPShopItems()` aus dem Shop-Random-Pool.
- Der OP-Ban-Smoke laeuft bewusst ohne Ban Bad und ohne Regular-Ban; Bad- oder Regular-Item-Befunde waeren deshalb kein Fehler dieses Subscopes.

## Smoke-Ergebnis

Bestanden fuer den getesteten Subscope `Shop Random + Ban OP`.

- Save erfolgreich.
- Log erfolgreich und nicht leer.
- Output-ROM vorhanden, aber nicht committed.
- Reload erfolgreich.
- Shop-Anzahl, MainGame-/Skip-/Special-Zuordnung, Gesamtitemzahl und Shoplaengen blieben stabil.
- Terminator-/Laengenmodell blieb stabil.
- Skip-Shops blieben erhalten.
- Special-Shop-Reload war stabil.
- Preislogik blieb unberuehrt.
- Field Items, Pickup Items und Held Items blieben unveraendert.
- `opShopItemBannedWrites=0` fuer den randomisierten Special-Shop-Schreibbereich.

Damit ist `FVX-ITEM-007` fuer den getesteten Subscope `ShopItemsMod.RANDOM + banOPShopItems=true` als GUI-kompatibel belegt.
Ban Bad und Ban Regular bleiben aus Diagnose 127/128 dokumentiert; Ban-Kombinationen bleiben separat offen.

## Shop-Struktur / Reload-Befund

| Metrik | Before | After | Reload |
| --- | ---: | ---: | ---: |
| `shopCount` | 23 | 23 | 23 |
| `mainGameShopCount` | 3 | 3 | 3 |
| `skippedShopCount` | 20 | 20 | 20 |
| `specialShopCount` | 3 | 3 | 3 |
| `shopItemsTotal` | 157 | 157 | 157 |
| `minShopLength` | 2 | 2 | 2 |
| `maxShopLength` | 9 | 9 | 9 |
| `badShopItems` | 36 | 36 | 36 |
| `tmShopItems` | 6 | 6 | 6 |

Reload-Details:
- `terminatorModelStableAfter=true`
- `terminatorModelStableReload=true`
- `shopLengthMismatchesAfter=0`
- `shopLengthMismatchesReload=0`
- `shopItemReloadMismatches=0`
- `specialShopPolicyMismatches=0`

## Preserve-/Skip-Befund

- `skippedShopItemMismatchesAfter=0`
- `skippedShopItemMismatchesReload=0`
- `skipShopsPreserved=true`
- Skip-Shops bleiben ausserhalb des Shop-Random-Schreibbereichs.
- Die Special-Shop-Policy ist im Reload stabil.

## Ban-OP-/Pool-Befund

- `opShopSetClassifiable=true`
- `opShopItemPoolCandidates=9`
- `opShopItemPoolExcluded=9`
- `opShopItemBannedWrites=0`
- `invalidShopItemWrites=0`
- `unloadedShopItemWrites=0`
- `fallbackShopItemWrites=0`
- `placeholderShopItemWrites=0`

Der OP-Ban-Subscope entfernt die klassifizierbaren OP-Shop-Items aus dem Shop-Random-Pool und schreibt im randomisierten Special-Shop-Bereich keine OP-Shop-Items.

## Fremdscope- und Preisbefund

- `priceTableTouched=false`
- `priceReloadMismatches=0`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`

## Risiken / Blocker

Keine Blocker fuer den getesteten `Shop Random + Ban OP`-Subscope.

Verbleibende Risiken:
- Ban-Kombinationen sind nicht getestet.
- `FVX-ITEM-008` Guarantee Evolution/X Items ist nicht getestet.
- `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies ist nicht getestet.

## Metriken

```text
candidateFilesChecked=5
candidateLoaded=true
opShopSetClassifiable=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
shopCountBefore=23
shopCountAfter=23
shopCountReload=23
mainGameShopCountBefore=3
mainGameShopCountAfter=3
mainGameShopCountReload=3
skippedShopCountBefore=20
skippedShopCountAfter=20
skippedShopCountReload=20
specialShopCountBefore=3
specialShopCountAfter=3
specialShopCountReload=3
shopItemsTotalBefore=157
shopItemsTotalAfter=157
shopItemsTotalReload=157
minShopLengthBefore=2
minShopLengthAfter=2
minShopLengthReload=2
maxShopLengthBefore=9
maxShopLengthAfter=9
maxShopLengthReload=9
terminatorModelStableAfter=true
terminatorModelStableReload=true
shopLengthMismatchesAfter=0
shopLengthMismatchesReload=0
shopItemReloadMismatches=0
skippedShopItemMismatchesAfter=0
skippedShopItemMismatchesReload=0
specialShopPolicyMismatches=0
invalidShopItemWrites=0
unloadedShopItemWrites=0
fallbackShopItemWrites=0
placeholderShopItemWrites=0
opShopItemPoolCandidates=9
opShopItemPoolExcluded=9
opShopItemBannedWrites=0
badShopItemsBefore=36
badShopItemsAfter=36
badShopItemsReload=36
tmShopItemsBefore=6
tmShopItemsAfter=6
tmShopItemsReload=6
priceTableTouched=false
priceReloadMismatches=0
fieldItemScopeChanged=false
pickupScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Statusentscheidung

- `FVX-ITEM-007` ist fuer `Shop Random + Ban OP` im getesteten Shop-only Scope GUI-kompatibel.
- `FVX-ITEM-007` ist damit fuer Ban Bad, Ban Regular und Ban OP jeweils einzeln belegt.
- `FVX-ITEM-007` wird nicht automatisch fuer Ban-Kombinationen hochgestuft.
- `FVX-ITEM-008` und `FVX-ITEM-009` bleiben ausstehend.

## Naechster minimaler Schritt

Entscheiden, ob `FVX-ITEM-007` zusaetzliche Ban-Kombinationsdeckung braucht oder ob als naechster Shop-Scope `FVX-ITEM-008 Guarantee Evolution/X Items` geplant wird.
