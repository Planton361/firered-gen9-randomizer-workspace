# Diagnose 127: Shop Items Random + Ban Bad Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-shop-items-random-ban-bad-reload-smoke`
Scope: Shop-only `FVX-ITEM-007` Subscope fuer `ShopItemsMod.RANDOM` mit `banBadRandomShopItems=true`

## Ziel

Dieser Block prueft ausschliesslich den Shop-Random-Pfad mit aktivierter Bad-Item-Ban-Option.

In Scope:
- `Settings.ShopItemsMod = RANDOM`
- `banBadRandomShopItems=true`
- `banRegularShopItems=false`
- `banOPShopItems=false`
- Shop-only Write/Reload-Smoke auf der lokal freigegebenen CFRU/DPE Gen9-BPRE-Kandidatenquelle

Out of Scope:
- Shop Regular-Ban und OP-Ban
- Guarantee Evolution Items und Guarantee X Items
- `balanceShopPrices` und `addCheapRareCandiesToShops`
- Field Items, Pickup Items und Held Items
- Codeaenderungen, Builds, Submodule-Pin-Aenderungen und Upstream-Kontakte

Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten wurden nicht dokumentiert.
Lokale Output-ROM-, Log- und Harness-Artefakte blieben ignoriert.

## Baseline

- `FVX-ITEM-005` ist im getesteten Shop-only Shuffle-Scope GUI-kompatibel.
- `FVX-ITEM-006` ist im getesteten Shop-only Random-Scope GUI-kompatibel.
- Diagnose 126 bestaetigt: `banBadRandomShopItems` wirkt im Shop-Random-Pfad, indem der Shop-Pool von `getAllowedItems()` auf `getNonBadItems()` wechselt; TMs werden danach aus dem Shop-Random-Pool entfernt.
- `badShopItemsBefore/After/Reload=36` aus Diagnose 125 war Bestand ohne Ban-Bad-Aussage, kein Ban-Ergebnis.

## Smoke-Ergebnis

Bestanden fuer den getesteten Subscope `Shop Random + Ban Bad`.

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
- `badShopItemWrites=0` fuer den randomisierten Special-Shop-Schreibbereich.

Damit ist `FVX-ITEM-007` nur fuer den getesteten Subscope `ShopItemsMod.RANDOM + banBadRandomShopItems=true` als GUI-kompatibel belegt.
`banRegularShopItems` und `banOPShopItems` bleiben separat und werden nicht durch diesen Smoke hochgestuft.

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
| `badShopItems` | 36 | 35 | 35 |
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

## Ban-Bad-/Pool-Befund

- `allowedShopItemPoolSize=536`
- `nonBadShopItemPoolSize=485`
- `banBadShopItemPoolCandidates=51`
- `banBadShopItemPoolExcluded=51`
- `badShopItemWrites=0`
- `invalidShopItemWrites=0`
- `unloadedShopItemWrites=0`
- `fallbackShopItemWrites=0`
- `placeholderShopItemWrites=0`

Der Ban-Bad-Subscope nutzt den nicht-schlechten Shop-Random-Pool und schreibt im randomisierten Special-Shop-Bereich keine Bad Items.
Die weiterhin vorhandenen `badShopItemsAfter/Reload=35` sind erhaltener Bestand ausserhalb des randomisierten Special-Shop-Schreibbereichs und kein Ban-Bad-Verstoss.

## Fremdscope- und Preisbefund

- `priceTableTouched=false`
- `priceReloadMismatches=0`
- `fieldItemScopeChanged=false`
- `pickupScopeChanged=false`
- `heldItemScopeChanged=false`

## Risiken / Blocker

Keine Blocker fuer den getesteten `Shop Random + Ban Bad`-Subscope.

Verbleibende Risiken:
- `banRegularShopItems` ist nicht getestet.
- `banOPShopItems` ist nicht getestet.
- Ban-Kombinationen sind nicht getestet.
- `FVX-ITEM-008` Guarantee Evolution/X Items ist nicht getestet.
- `FVX-ITEM-009` Balance Shop Prices / Cheap Rare Candies ist nicht getestet.

## Metriken

```text
candidateFilesChecked=5
candidateLoaded=true
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
badShopItemsBefore=36
badShopItemsAfter=35
badShopItemsReload=35
badShopItemWrites=0
allowedShopItemPoolSize=536
nonBadShopItemPoolSize=485
banBadShopItemPoolCandidates=51
banBadShopItemPoolExcluded=51
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

- `FVX-ITEM-007` ist fuer `Shop Random + Ban Bad` im getesteten Shop-only Scope GUI-kompatibel.
- `FVX-ITEM-007` wird nicht pauschal fuer Regular-/OP-Bans hochgestuft.
- `FVX-ITEM-008` und `FVX-ITEM-009` bleiben ausstehend.

## Naechster minimaler Schritt

Shop Random + Ban Regular separat planen oder smoken, nur wenn der Regular-Shop-Item-Pool eindeutig klassifizierbar bleibt.
