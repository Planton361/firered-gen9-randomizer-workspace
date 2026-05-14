# 099 - CFRU/DPE Field Items Scope Diagnostics

Datum: 2026-05-14
Branch: `test/upr-fvx-cfru-dpe-field-items-scope-diagnostics`
UPR-FVX-Pin: `2697511da9a97df4c29c00dfda8b40e556020489`

## Ziel

Dieser Block sollte einen sanitisierten read-only Diagnose-Lauf fuer den Field-Items-only Scope im CFRU/DPE Gen9-BPRE-Stand dokumentieren.

Der Lauf bleibt auf Field Items begrenzt:

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
- keine Logs committed
- kein Zugriff auf ROMs, Saves, Emulator States, Builds, Randomizer-JARs oder Tool-Binaries
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Secrets, Tokens oder `.env`-Inhalte dokumentiert
- keine Original-Upstream-Kontakte

## Voraussetzung / GitHub-Stand

- Workspace PR #143 `docs: plan field items diagnostics scope` wurde als gemerged geprueft.
- Der Diagnosebranch wurde danach von `origin/main` erstellt.
- `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md` ist auf `main` verfuegbar.

## Kandidaten-/Preflight-Ergebnis

Es wurde kein fachlicher Field-Items-Diagnose-Lauf ausgefuehrt.

Grund: In diesem Arbeitsauftrag wurde kein explizit freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat benannt. Nach den Sicherheitsregeln werden ohne einen solchen freigegebenen Kandidaten keine ROM-Artefakte gesucht, gelesen, kopiert, geoeffnet oder ausgewertet.

Sanitisierte Preflight-Metriken:

- `candidateFilesChecked=0`
- `candidateLoaded=false`
- `fieldItemScanSuccessful=false`
- `exceptionClass=none`
- `stacktrace=none`

## Read-only Diagnosemetriken

Da kein Kandidat geladen wurde, sind alle fachlichen Field-Item-Metriken nicht ausgewertet:

- `mapBanksScanned=not evaluated`
- `mapsScanned=not evaluated`
- `fieldItemsTotal=not evaluated`
- `visibleFieldItemSlots=not evaluated`
- `hiddenFieldItemSlots=not evaluated`
- `allowedFieldItemSlots=not evaluated`
- `disallowedFieldItemSlots=not evaluated`
- `tmFieldItemSlots=not evaluated`
- `nonTmFieldItemSlots=not evaluated`
- `requiredFieldTMsTotal=not evaluated`
- `requiredFieldTMPresent=not evaluated`
- `requiredFieldTMMissing=not evaluated`
- `progressionSensitiveFieldItems=not evaluated`
- `keyOrSystemFieldItems=not evaluated`
- `placeholderFieldItems=not evaluated`
- `fallbackFieldItems=not evaluated`
- `badFieldItems=not evaluated`
- `modernFieldItemIds=not evaluated`
- `invalidFieldItemIds=not evaluated`
- `unloadedFieldItemIds=not evaluated`
- `scriptPatternUnmatchedItemBalls=not evaluated`
- `hiddenItemSignpostSlots=not evaluated`
- `coinOrNullHiddenItemSlots=not evaluated`

Optionale Metriken wurden ebenfalls nicht ausgewertet:

- `fieldItemUniqueItems=not evaluated`
- `fieldItemDuplicateItems=not evaluated`
- `tmFieldItemUniqueItems=not evaluated`
- `nonTmFieldItemUniqueItems=not evaluated`
- `requiredProgressionItemsPreservedByCurrentPolicy=not evaluated`
- `badItemBanCandidates=not evaluated`
- `badItemBanRemovalsNeeded=not evaluated`
- `modernItemIdsAllowed=not evaluated`
- `modernItemIdsRejected=not evaluated`
- `fieldItemScanWarnings=not evaluated`

## Field-Items-Scope-Bewertung

Der Field-Items-only Scope bleibt fachlich sinnvoll und eng, aber weiterhin blockiert bis ein explizit freigegebener CFRU/DPE Gen9-BPRE-Kandidat bereitsteht.

Bestaetigte reine Scope-Grenzen aus 098 bleiben unveraendert:

- Field Items bleiben getrennt von Shops und Pickup.
- Sichtbare Itemballs und Hidden Items/Signposts muessen getrennt gezaehlt werden.
- TM-Slots und Non-TM-Slots muessen getrennt gezaehlt und spaeter positionssicher behandelt werden.
- Required Field TMs und progression-sensitive Items muessen vor jedem Write-Fix klassifiziert werden.
- Invalide, nicht geladene, fallback-, placeholder-, key- oder systemnahe Items duerfen nicht blind in Random-Pools gelangen.

## Preserve-/Skip-Folgen

Bis ein fachlicher Diagnose-Lauf konkrete Zaehler liefert, bleibt die Policy aus 098 konservativ:

- Required/progression-sensitive Field Items: preserve-only.
- Required Field TMs: preserve-only oder nur mit spaeterem Required-TM-Nachweis ersetzbar.
- TM-Slots: nur TM-Ersatz.
- Non-TM-Slots: kein TM-Ersatz.
- Invalid oder nicht geladene Item-IDs: preserve-only und kein Random-Pick.
- Key-/System-/Placeholder-/Fallback-Items: preserve-only oder explizit aus Pools ausschliessen.
- Moderne Item-IDs: erst nach loaded/allowed/reload-stable Nachweis als Pick-Kandidaten zulassen.
- Nicht erkannte Itemball-/Signpost-Strukturen: nicht schreiben.
- Coin-/Null-Hidden-Item-Faelle: ausserhalb normaler Field-Item-Randomization halten.

## Nicht-Ziele dieses Blocks

Nicht bewertet und nicht geaendert:

- Shops
- Pickup
- Encounter Held Items
- Trainer Held Items
- Starter Held Items
- TM/HM/Tutor/Learnset-Writer
- Palette / Graphics
- MoveData / MoveNames
- TypeChart / TypeEffectiveness
- Trainer
- Wild
- Evolution
- Text/Menu
- Field-Item-Fixumsetzung

## Empfehlung

Naechster minimaler Schritt ist ein erneuter Field-Items-only Diagnoseblock, sobald ein explizit freigegebener lokaler CFRU/DPE Gen9-BPRE-Kandidat verfuegbar ist.

Vorgeschlagener Folgebranch:

`test/upr-fvx-cfru-dpe-field-items-scope-diagnostics-candidate`

Der Folgeblock soll erst dann ROM-read-only laufen, wenn der Kandidat im Auftrag explizit freigegeben ist. Bis dahin bleiben `FVX-ITEM-001` bis `FVX-ITEM-004` auf `Write modelliert`.
