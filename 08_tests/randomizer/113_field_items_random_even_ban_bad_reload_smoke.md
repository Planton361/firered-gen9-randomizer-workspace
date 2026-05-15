# 113 - CFRU/DPE Field Items Random Even Ban Bad Reload Smoke

Datum: 2026-05-15

## Scope

- Repo: `Planton361/firered-gen9-randomizer-workspace`
- Branch: `test/upr-fvx-cfru-dpe-field-items-random-even-ban-bad-reload-smoke`
- UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`
- Feature: `FVX-ITEM-003 Field Items Random even distribution` mit `banBadRandomFieldItems=true`
- Bewerteter Ban-Bad-Teil: `FVX-ITEM-004 Field Items Ban Bad Items` fuer `FieldItemsMod.RANDOM_EVEN`

Dieser Smoke prueft nur den Field-Items-only Write-/Reload-Pfad fuer `Settings.FieldItemsMod.RANDOM_EVEN` mit aktivem Ban-Bad-Filter. Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser bleiben ausserhalb des Scopes.

## Sicherheits- und Sanitizing-Grenzen

- Dokumentiert werden nur aggregierte Zaehler und boolesche Ergebnisse.
- Keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes oder Logauszuege werden dokumentiert.
- Lokaler Harness, Output-ROM und Logs bleiben ignored unter `05_builds/**`.
- Keine Codeaenderung, keine Aenderung an `02_external/**`, kein Submodule-Pin-Wechsel und kein Build.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/098_field_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/099_field_items_scope_diagnostics.md`
- `08_tests/randomizer/100_field_items_scope_diagnostics_candidate.md`
- `08_tests/randomizer/101_field_items_allowed_slot_write_guard.md`
- `08_tests/randomizer/102_field_items_allowed_slot_reload_smoke.md`
- `08_tests/randomizer/103_field_items_random_reload_smoke.md`
- `08_tests/randomizer/104_field_items_random_tm_pool_blocker_plan.md`
- `08_tests/randomizer/105_field_items_random_tm_pool_fix.md`
- `08_tests/randomizer/106_field_items_random_tm_pool_reload_smoke.md`
- `08_tests/randomizer/107_field_items_random_api_tm_slot_scope_plan.md`
- `08_tests/randomizer/108_field_items_api_tm_slot_scope_fix.md`
- `08_tests/randomizer/109_field_items_api_tm_slot_reload_smoke.md`
- `08_tests/randomizer/110_field_items_random_even_reload_smoke.md`
- `08_tests/randomizer/111_field_items_ban_bad_scope_plan.md`
- `08_tests/randomizer/112_field_items_random_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Ergebnis

```text
candidateFilesChecked=9
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
fieldItemsTotalBefore=339
fieldItemsTotalAfter=339
fieldItemsTotalReload=339
fieldItemReloadMismatches=0
visibleFieldItemReloadMismatches=0
hiddenFieldItemReloadMismatches=0
tmFieldItemSlotMismatches=0
nonTmFieldItemSlotMismatches=0
requiredFieldTMMissingAfter=0
requiredItemPolicyViolations=0
progressionItemPolicyViolations=0
invalidFieldItemWrites=0
unloadedFieldItemWrites=0
fallbackFieldItemWrites=0
placeholderFieldItemWrites=0
disallowedFieldItemWrites=0
apiTmFieldSlotWrites=27
scriptPatternExpansion=0
badFieldItemWrites=0
badFieldItemPoolCandidates=47
badFieldItemPoolExcluded=47
nonBadFieldItemPoolSize=485
randomTmNeededSlots=28
randomTmCurrentSlots=28
randomTmRequiredTotal=24
randomTmRequiredPresent=24
randomTmRequiredMissingBefore=0
randomTmRequiredMissingAfter=0
randomTmLoadedPoolSize=50
randomTmAllowedPoolSize=0
randomTmUniquePoolSize=50
randomTmFillerNeeded=4
randomTmFillerAvailable=26
randomTmDuplicateSelections=0
randomTmPoolDeficit=0
randomTmResultSize=28
randomTmResultUniqueSize=28
apiFieldItemsTotal=308
apiTmFieldItemSlots=28
apiNonTmFieldItemSlots=280
rawTmFieldItemSlots=28
rawApiTmSlotAlignmentMismatches=0
tmGloballyAllowedChanged=false
shopItemScopeChanged=false
pickupItemScopeChanged=false
heldItemScopeChanged=false
randomEvenQueueUsed=true
randomEvenTmDistributionStable=true
randomEvenNonTmDistributionStable=true
nonBadFieldItemQueueRefills=0
exceptionClass=none
stacktrace=none
```

## Bewertung

Der Write-/Reload-Smoke ist fachlich stabil:

- Save, Log, Output und Reload waren erfolgreich.
- Field-Items-Anzahl bleibt stabil bei `339`.
- Reload-Mismatches bleiben `0` fuer Gesamt-, sichtbare und Hidden-Field-Items.
- TM-/Non-TM-Slottypen bleiben stabil.
- Required Field TMs bleiben vollstaendig.
- Keine invaliden, unloaded, fallback, placeholder oder disallowed Non-TM-Field-Item-Writes wurden beobachtet.
- Ban Bad erzeugt keine Bad-Item-Writes: `badFieldItemWrites=0`.
- Random-Even-Queue-/Verteilungsstabilitaet ist fuer diesen Smoke belegt: `randomEvenQueueUsed=true`, `randomEvenTmDistributionStable=true`, `randomEvenNonTmDistributionStable=true`, `nonBadFieldItemQueueRefills=0`.
- Der TM-Pool bleibt stabil: `randomTmNeededSlots=28`, `randomTmRequiredTotal=24`, `randomTmFillerNeeded=4`, `randomTmPoolDeficit=0`, `randomTmResultUniqueSize=28`.
- TMs wurden nicht global allowed gesetzt, und Shop-, Pickup- sowie Held-Item-Scope blieben unveraendert.

Konservative Einordnung der Bad-Item-Pool-Zaehler:

- Wie Diagnose 112 findet dieser Smoke `badFieldItemPoolCandidates=47` und `badFieldItemPoolExcluded=47` im geladenen fachlichen Kandidaten.
- Die fruehere 75er-Baseline aus Diagnose 111 wird nicht als fixer Zielwert erzwungen.
- Entscheidend fuer diesen Smoke ist, dass `badFieldItemWrites=0` und alle Preserve-/Reload-Zielwerte erreicht sind.

## Preserve-/Skip-Policy

- Write nur ueber den Field-Items-API-Scope.
- CFRU/DPE Field-TM-Slots bleiben eng sichtbar.
- TMs werden nicht global allowed gesetzt.
- TM-Slots bleiben TM-Slots.
- Non-TM-Slots bleiben Non-TM-Slots.
- Required Field TMs bleiben vollstaendig.
- Ban Bad veraendert nur die Auswahl aus dem Non-TM-Random-Even-Pool.
- Preserve-only bleiben:
  - disallowed non-TM Field-Item-Slots
  - progression/key/system Slots
  - invalid/unloaded/fallback/placeholder Slots
  - `scriptPatternUnmatchedItemBalls=10`
  - nicht erkannte Script-/Map-Strukturen
- Shops, Pickup und Held Items bleiben ausserhalb dieses Scopes.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle` bleibt `GUI-kompatibel` im getesteten allowed-slot Scope.
- `FVX-ITEM-002 Field Items Random` bleibt `GUI-kompatibel` im engen Field-Items-Random-Scope; Diagnose 112 bestaetigt zusaetzlich `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003 Field Items Random even distribution` bleibt `GUI-kompatibel` im engen Field-Items-Random-Even-Scope; dieser Lauf bestaetigt zusaetzlich `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM_EVEN`.
- `FVX-ITEM-004 Field Items Ban Bad Items` wird fuer Field Items Random und Random Even als `GUI-kompatibel` bewertet.
- Shops, Pickup und Held Items werden nicht hochgestuft.

## Risiken / Annahmen

- Die Bewertung gilt fuer den explizit freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten und den engen Field-Items-only Scope.
- Der lokale Harness und seine Artefakte bleiben ignored und wurden nicht committed.
- Die Bad-Item-Pool-Baseline ist kandidaten-/API-scope-abhaengig; dokumentiert wird der aggregierte Laufwert, nicht ein privater Artefaktbefund.
- Shops, Pickup, Held Items und TM/HM/Tutor/Learnset bleiben eigene Scopes.

## Naechster minimaler Schritt

`analysis/upr-fvx-cfru-dpe-pickup-items-scope-diagnostics-plan`: Pickup als naechsten getrennten Item-Writer-Scope read-only planen. Field Items `FVX-ITEM-001..004` sind im getesteten engen Field-Items-only Scope abgeschlossen; Shops und Pickup bleiben getrennt.
