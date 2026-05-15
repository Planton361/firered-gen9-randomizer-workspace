# 115 - CFRU/DPE Pickup Items Scope Diagnostics

Datum: 2026-05-15

## Ziel

Dieser Block dokumentiert eine sanitisiert ausgefuehrte read-only Pickup-only Kandidatendiagnose fuer den CFRU/DPE Gen9-BPRE-Stand. Es wurde kein Codefix umgesetzt, kein Randomizer-Write ausgefuehrt, kein Build gestartet und keine Output-ROM erzeugt oder dokumentiert.

Scope bleibt ausschliesslich `FVX-ITEM-010 Pickup Items Random / Ban Bad Items`. Field Items, Shops, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser-Arbeit bleiben ausserhalb.

## Voraussetzungen / Ausgangsstand

- Workspace PR #159 (`docs: plan pickup items diagnostics scope`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Workspace-Submodule `02_external/upr-fvx` bleibt auf `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Ein lokaler CFRU/DPE Gen9-BPRE-Kandidat war fuer diesen read-only Pickup-only Diagnoseblock freigegeben.
- Lokale Harness-/Diagnoseartefakte blieben ignored unter `05_builds/**`.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/114_pickup_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

Optionaler Field-Items-Kontext aus den Diagnosen 098 bis 113 wurde nur zur Abgrenzung beruecksichtigt.

## Sanitizing

Dokumentiert werden ausschliesslich aggregierte Zaehler und boolesche Ergebnisse. Nicht dokumentiert werden private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Logs, Output-ROM-Pfade oder lokale Artefaktwerte.

## Diagnose-Ergebnis

```text
candidateFilesChecked=97
candidateLoaded=true
pickupScanSuccessful=true
pickupLocatorSuccessful=true
pickupItemsTotal=16
pickupExpectedCount=16
pickupEntrySize=4
pickupProbabilitySlots=10
pickupProbabilityModelStable=true
pickupUniqueItems=16
pickupDuplicateItems=0
pickupAllowedItems=15
pickupDisallowedItems=1
pickupBadItems=7
pickupTmItems=1
pickupNonTmItems=15
pickupModernItemIds=0
pickupInvalidItemIds=0
pickupUnloadedItemIds=0
pickupFallbackItems=0
pickupPlaceholderItems=0
pickupCommonSlots=7
pickupRareSlots=5
pickupCommonRareModelDetected=false
pickupTableLengthMismatch=0
pickupPoolAllowedSize=536
pickupPoolNonBadSize=485
pickupTmPoolPolicy=tms allowed
canTMsBeHeld=true
isTMsReusable=false
pickupItemIdMax=337
pickupInternalMappingFailures=0
pickupProbabilitySlotMismatches=0
pickupEntrySizeDetected=4
pickupLocatorCandidateCount=1
pickupBadItemPoolCandidates=51
pickupBadItemPoolExcluded=51
pickupPolicyWarnings=0
exceptionClass=none
stacktrace=none
```

## Bewertung

- Pickup-Locator ist erfolgreich: `pickupLocatorSuccessful=true` und `pickupLocatorCandidateCount=1`.
- Pickup-Count und Tabellenlaenge sind plausibel: `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupTableLengthMismatch=0`.
- Entry-Size und Modell passen zum aktuellen Gen3-/FRLG-Pfad: `pickupEntrySize=4`, `pickupEntrySizeDetected=4`, `pickupProbabilitySlots=10`.
- Probability-Modell ist stabil: `pickupProbabilityModelStable=true`, `pickupProbabilitySlotMismatches=0`.
- Es gibt keinen Hinweis auf ein Emerald-/Common-Rare-29er-Modell: `pickupCommonRareModelDetected=false`.
- Alle aktuell gelesenen Pickup-Item-IDs sind valide und geladen: `pickupInvalidItemIds=0`, `pickupUnloadedItemIds=0`, `pickupInternalMappingFailures=0`.
- Keine Fallback-/Placeholder-Items wurden im aktuellen Pickup-Scope gefunden: `pickupFallbackItems=0`, `pickupPlaceholderItems=0`.
- Aktuelle Pickup-Tabelle enthaelt Bad-Item- und TM-Risikoindikatoren: `pickupBadItems=7`, `pickupTmItems=1`.
- Poolseitig ist Ban Bad relevant: `pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`, `pickupPoolAllowedSize=536`, `pickupPoolNonBadSize=485`.
- TMs sind fuer diesen Pickup-Pfad aktuell erlaubt: `pickupTmPoolPolicy=tms allowed`, `canTMsBeHeld=true`, `isTMsReusable=false`.

## Pickup-Scope-Bewertung

Ein Pickup Random Write-/Reload-Smoke ohne Ban Bad ist als naechster enger Schritt sinnvoll, weil Locator, Count, Entry-Size, Probability-Modell und Item-ID-Mapping read-only stabil sind.

Ban Bad muss danach separat bleiben, weil der Poolfilter eine messbare eigene Wirkung hat (`pickupBadItemPoolCandidates=51`, `pickupBadItemPoolExcluded=51`). Ein kombinierter erster Smoke wuerde Random-Write-Stabilitaet und Bad-Item-Poolfilter vermischen.

Kein UPR-FVX-Codefix ist aus dieser Diagnose direkt belegt. `FVX-ITEM-010` bleibt bis zu einem eigenen Pickup Random Write-/Reload-Smoke `Write modelliert`.

## Preserve-/Skip-Folgen

Fuer spaetere Pickup-only Smokes gilt:

- nur die eindeutig lokalisierte Pickup-Tabelle schreiben.
- Tabellenlaenge `16`, Slotreihenfolge, Entry-Size `4` und Probability-Slots `10` erhalten.
- keine unbekannte Common/Rare- oder externe Probability-Struktur annehmen.
- invalid, unloaded, fallback und placeholder Items nie als Random-Picks verwenden.
- Ban Bad nur im eigenen Ban-Bad-Smoke aktivieren.
- TM-Policy fuer Pickup aus `canTMsBeHeld=true` und `isTMsReusable=false` ableiten; keine Field-TM- oder globale TM-Allow-Policy uebernehmen.
- keine Field Items, Shops oder Held Items beruehren.

## Naechste Smoke-/Fix-Empfehlung

Naechster minimaler Smoke:

- `test/upr-fvx-cfru-dpe-pickup-items-random-reload-smoke`

Scope:

- nur `FVX-ITEM-010 Pickup Items Random`.
- `PickupItemsMod.RANDOM`.
- `banBadRandomPickupItems=false`.
- kein Codefix, kein Submodule-Pin-Wechsel.
- keine Shops, Field Items oder Held Items.

Erwartete Kernkriterien:

```text
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
pickupLocatorSuccessful=true
pickupItemsTotalBefore=16
pickupItemsTotalAfter=16
pickupItemsTotalReload=16
pickupItemReloadMismatches=0
pickupTableLengthMismatches=0
pickupProbabilityMismatches=0
pickupCommonRarePolicyViolations=0
invalidPickupItemWrites=0
unloadedPickupItemWrites=0
fallbackPickupItemWrites=0
placeholderPickupItemWrites=0
pickupTmPolicyViolations=0
fieldItemScopeChanged=false
shopItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

Danach separat:

- `test/upr-fvx-cfru-dpe-pickup-items-random-ban-bad-reload-smoke`
- nur wenn Random ohne Ban Bad stabil reloadet.
