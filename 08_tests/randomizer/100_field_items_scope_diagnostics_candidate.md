# 100 - CFRU/DPE Field Items Scope Diagnostics Candidate

Datum: 2026-05-14
Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`
UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

## Ziel

Dieser Block dokumentiert einen sanitisierten read-only Field-Items-only Diagnose-Lauf fuer einen explizit freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten.

Der Lauf prueft nur Field Items:

- sichtbare Itemballs
- Hidden Items / Signposts
- TM-Slots
- Non-TM-Slots
- Required Field TMs
- required/progression-sensitive Items
- Key-/System-/Placeholder-/Fallback-/Bad-Items
- moderne Item-IDs
- invalid oder nicht geladene Item-IDs
- Script-/Map-Erkennungsrisiken

Nicht ausgefuehrt und nicht beruehrt:

- kein Fix
- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Build
- kein Randomizer-Write/Save
- keine Output-ROM
- keine committed Logs
- keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs oder Tool-Binaries committed
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Secrets, Tokens oder `.env`-Inhalte dokumentiert
- keine Original-Upstream-Kontakte

## Voraussetzung / GitHub-Stand

- Workspace PR #144 `docs: record field items diagnostics` wurde als gemerged geprueft.
- Der Diagnosebranch wurde danach von `origin/main` erstellt.
- Ein lokaler CFRU/DPE Gen9-BPRE-Kandidat war fuer diesen read-only Field-Items-Diagnoseblock explizit freigegeben.

## Durchfuehrung

- Es wurde ein temporerer lokaler Diagnose-Harness unter ignored `05_builds/**` verwendet.
- Der Harness lief read-only gegen den lokal freigegebenen Kandidaten.
- Es wurde kein Randomizer-Write/Save ausgefuehrt.
- Es wurde keine Output-ROM erzeugt.
- Es wurden nur aggregierte Zaehler und boolesche Ergebnisse in dieses Protokoll uebernommen.
- Loader-interne Raw-Diagnoseausgaben mit Offsets/Interna wurden nicht dokumentiert und nicht committed.

## Diagnose-Ergebnis

Pflichtmetriken:

- `candidateFilesChecked=94`
- `candidateLoaded=true`
- `fieldItemScanSuccessful=true`
- `mapBanksScanned=43`
- `mapsScanned=425`
- `fieldItemsTotal=339`
- `visibleFieldItemSlots=168`
- `hiddenFieldItemSlots=171`
- `allowedFieldItemSlots=280`
- `disallowedFieldItemSlots=59`
- `tmFieldItemSlots=28`
- `nonTmFieldItemSlots=311`
- `requiredFieldTMsTotal=24`
- `requiredFieldTMPresent=24`
- `requiredFieldTMMissing=0`
- `progressionSensitiveFieldItems=59`
- `keyOrSystemFieldItems=3`
- `placeholderFieldItems=0`
- `fallbackFieldItems=0`
- `badFieldItems=75`
- `modernFieldItemIds=0`
- `invalidFieldItemIds=0`
- `unloadedFieldItemIds=0`
- `scriptPatternUnmatchedItemBalls=10`
- `hiddenItemSignpostSlots=183`
- `coinOrNullHiddenItemSlots=12`
- `exceptionClass=none`
- `stacktrace=none`

Optionale Metriken:

- `fieldItemUniqueItems=119`
- `fieldItemDuplicateItems=220`
- `tmFieldItemUniqueItems=28`
- `nonTmFieldItemUniqueItems=91`
- `requiredProgressionItemsPreservedByCurrentPolicy=83`
- `badItemBanCandidates=75`
- `badItemBanRemovalsNeeded=75`
- `modernItemIdsAllowed=0`
- `modernItemIdsRejected=0`
- `fieldItemScanWarnings=0`

## Field-Items-Scope-Bewertung

Der Field-Items-only Scope ist fuer einen spaeteren engen Fix-/Smoke-Block belastbar genug inventarisiert.

Wichtige Befunde:

- Der Kandidat laedt und der Field-Item-Scan ist erfolgreich.
- Der erkannte Scope umfasst `339` Field-Item-Slots.
- Sichtbare Itemballs und Hidden Items sind beide relevant: `168` sichtbare Slots und `171` Hidden-Slots.
- Der bestehende Gen3-Handler filtert `280` erlaubte Field-Item-Slots; `59` Slots sind disallowed/preserve-relevant.
- TM-/Non-TM-Trennung ist notwendig: `28` TM-Slots und `311` Non-TM-Slots.
- Required Field TMs sind vollstaendig praesent: `requiredFieldTMPresent=24`, `requiredFieldTMMissing=0`.
- Es gibt keine invaliden, ungeladenen, fallback- oder modernen Field-Item-IDs im erkannten Scope.
- `scriptPatternUnmatchedItemBalls=10` bestaetigt, dass ein spaeterer Fix die aktuelle Script-Erkennung nicht blind erweitern darf.

## Preserve-/Skip-Folgen

Policy fuer einen spaeteren Fix-/Smoke-Block:

- Nur die `allowedFieldItemSlots=280` duerfen als Write-Kandidaten gelten.
- `disallowedFieldItemSlots=59` bleiben preserve-only.
- Required Field TMs muessen nach jedem Write weiterhin vollstaendig abgedeckt bleiben.
- TM-Slots duerfen nur durch TMs ersetzt werden.
- Non-TM-Slots duerfen nicht durch TMs ersetzt werden.
- `badFieldItems=75` muessen bei aktivem Ban-Bad-Field-Items-Mode aus dem Random-Pool ausgeschlossen werden; vorhandene Slots bleiben ohne Fix-Smoke preserve-only zu bewerten.
- `keyOrSystemFieldItems=3` und alle progression-sensitive Slots bleiben preserve-only, bis eine explizite Required-/Progression-Policy existiert.
- `scriptPatternUnmatchedItemBalls=10` bleibt Diagnose-/Skip-Signal; kein Scriptparser-Ausbau im ersten Fix.
- Hidden Coin-/Null-Faelle bleiben ausserhalb normaler Field-Item-Randomization.
- Shops, Pickup und Held-Item-Pfade bleiben separate Scopes.

## Naechste Fix-/Smoke-Empfehlung

Ein enger Fix-/Smoke-Block ist jetzt sinnvoll, aber nur fuer Field Items:

- Scope: `FVX-ITEM-001` Field Items Shuffle und/oder ein minimaler Random-Mode-Carrier.
- Write-Kandidaten: nur erlaubte Field-Item-Slots.
- Required TMs: weiterhin `requiredFieldTMMissing=0` nach Reload.
- TM-/Non-TM-Slot-Typen: unveraendert.
- Disallowed, progression-sensitive, key/system, invalid/unloaded und pattern-unmatched Slots: preserve/skip.

Empfohlener Folgebranch:

`compat/upr-fvx-cfru-dpe-field-items-allowed-slot-write-guard`

## Reload-/Review-Kriterien fuer den Folgeblock

Ein spaeterer Write-/Reload-Smoke soll mindestens berichten:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `fieldItemsTotalReload=339`
- `fieldItemReloadMismatches=0`
- `visibleFieldItemReloadMismatches=0`
- `hiddenFieldItemReloadMismatches=0`
- `tmFieldItemSlotMismatches=0`
- `nonTmFieldItemSlotMismatches=0`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `exceptionClass=none`
- `stacktrace=none`
