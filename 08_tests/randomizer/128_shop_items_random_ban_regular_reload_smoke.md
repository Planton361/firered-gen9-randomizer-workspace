# Diagnose 128: Shop Items Random + Ban Regular Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-regular-reload-smoke`
Scope: Shop-only `FVX-ITEM-007` Subscope fuer `ShopItemsMod.RANDOM` mit `banRegularShopItems=true`

## Ziel

Dieser Block prueft ausschliesslich den Shop-Random-Pfad mit aktivierter Regular-Shop-Item-Ban-Option.

In Scope:
- `Settings.ShopItemsMod = RANDOM`
- `banBadRandomShopItems=false`
- `banRegularShopItems=true`
- `banOPShopItems=false`
- Shop-only Write/Reload-Smoke auf der lokal freigegebenen CFRU/DPE Gen9-BPRE-Kandidatenquelle

Out of Scope:
- Ban Bad und OP-Ban
- Ban-Kombinationen
- Guarantee Evolution Items und Guarantee X Items
- `balanceShopPrices` und `addCheapRareCandiesToShops`
- Field Items, Pickup Items und Held Items
- Codeaenderungen, Builds, Submodule-Pin-Aenderungen und Upstream-Kontakte

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten wurden nicht dokumentiert.
Lokale Output-ROM-, Log- und Harness-Artefakte blieben ignoriert.

## Vorbedingung

`getRegularShopItems()` wurde read-only im temporaren Harness geprueft und war eindeutig nutzbar:

- `regularShopSetClassifiable=true`
- `regularShopItemPoolCandidates=16`
- `regularShopItemPoolExcluded=16`

Damit war der Smoke ausfuehrbar; kein Blocked-/Preflight-Abbruch war noetig.

## Baseline

- `FVX-ITEM-005` ist im getesteten Shop-only Shuffle-Scope GUI-kompatibel.
- `FVX-ITEM-006` ist im getesteten Shop-only Random-Scope GUI-kompatibel.
- `FVX-ITEM-007` Ban Bad ist im getesteten `Shop Random + Ban Bad`-Scope reloadstabil.
- Diagnose 126 bestaetigt: `banRegularShopItems` entfernt `getRegularShopItems()` aus dem Shop-Random-Pool.
- Der Regular-Ban-Smoke laeuft bewusst ohne Ban Bad; Bad Items im Ergebnis sind deshalb kein Fehler dieses Subscopes.

## Smoke-Ergebnis

Bestanden fuer den getesteten Subscope `Shop Random + Ban Regular`.

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
- `regularShopItemBannedWrites=0` fuer den randomisierten Special-Shop-Schreibbereich.

Damit ist `FVX-ITEM-007` fuer den getesteten Subscope `ShopItemsMod.RANDOM + banRegularShopItems=true` als GUI-kompatibel belegt.
Ban Bad bleibt aus Diagnose 127 dokumentiert; OP-Ban bleibt separat offen.

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
| `badShopItems` | 36 | 38 | 38 |
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

## Ban-Regular-/Pool-Befund

- `regularShopSetClassifiable=true`
- `regularShopItemPoolCandidates=16`
- `regularShopItemPoolExcluded=16`
- `regularShopItemBannedWrites=0`
- `invalidShopItemWrites=0`
- `unloadedShopItemWrites=0`
- `fallbackShopItemWrites=0`
- `placeholderShopItemWrites=0`

Der Regular-Ban-Subscope entfernt die klassifizierbaren Regular-Shop-Items aus dem Shop-Random-Pool und schreibt im randomisierten Special-Shop-Bereich keine Regular-Shop-Items.
`badShopItemsAfter/Reload=38` ist fuer diesen Smoke kein Fehler, weil `banBadRandomShopItems=false` gesetzt war.

## Fremdscope- und Preisbefund

- `priceTableTouched=false`
- `priceReloadMismatches=0`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`

## Risiken / Blocker

Keine Blocker fuer den getesteten `Shop Random + Ban Regular`-Subscope.

Verbleibende Risiken:
- `banOPShopItems` ist nicht getestet.
- Ban-Kombinationen sind nicht getestet.
- `FVX-ITEM-008` Guarantee Evolution/X Items ist nicht getestet.
- `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies ist nicht getestet.

## Metriken

```text
candidateFilesChecked=5
candidateLoaded=true
regularShopSetClassifiable=true
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
regularShopItemPoolCandidates=16
regularShopItemPoolExcluded=16
regularShopItemBannedWrites=0
badShopItemsBefore=36
badShopItemsAfter=38
badShopItemsReload=38
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

- `FVX-ITEM-007` ist fuer `Shop Random + Ban Regular` im getesteten Shop-only Scope GUI-kompatibel.
- `FVX-ITEM-007` ist damit fuer Ban Bad und Ban Regular einzeln belegt.
- `FVX-ITEM-007` wird nicht pauschal fuer OP-Ban oder Ban-Kombinationen hochgestuft.
- `FVX-ITEM-008` und `FVX-ITEM-009` bleiben ausstehend.

## Naechster minimaler Schritt

Shop Random + Ban OP separat planen oder smoken, nur wenn der OP-Shop-Item-Pool eindeutig klassifizierbar bleibt.
