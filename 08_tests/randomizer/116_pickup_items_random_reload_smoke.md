# 116 - CFRU/DPE Pickup Items Random Reload-Smoke

Datum: 2026-05-15

## Ziel

Dieser Block dokumentiert einen sanitisierten Pickup-only Write-/Reload-Smoke fuer `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false` im CFRU/DPE Gen9-BPRE-Stand.

Es wurde kein Codefix umgesetzt, kein Submodule-Pin geaendert und kein anderer Itempfad in den Scope aufgenommen. Lokaler Harness, Output-ROM und Log blieben ignored unter `05_builds/**` und werden nicht dokumentiert oder committed.

## Voraussetzungen / Ausgangsstand

- Workspace PR #160 (`docs: record pickup items diagnostics`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Workspace-Submodule `02_external/upr-fvx` bleibt auf `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Ein lokaler CFRU/DPE Gen9-BPRE-Kandidat war fuer diesen Pickup-only Write-/Reload-Smoke explizit freigegeben.
- Diagnose 115 hatte den read-only Pickup-Scope mit `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupExpectedCount=16`, `pickupEntrySize=4` und `pickupProbabilityModelStable=true` vorbereitet.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/114_pickup_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/115_pickup_items_scope_diagnostics.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Scope

- Nur Pickup Items.
- `Settings.PickupItemsMod.RANDOM`.
- `banBadRandomPickupItems=false`.
- Kein Ban-Bad-Pickup-Smoke.
- Keine Field Items, Shops oder Held Items.
- Keine TM/HM/Tutor/Learnset-, Palette/Graphics-, MoveData/MoveNames-, TypeChart/TypeEffectiveness-, Trainer/Wild/Evolution-, Text/Menu- oder Scriptparser-Arbeit.

## Sanitizing

Dokumentiert werden ausschliesslich aggregierte Zaehler und boolesche Ergebnisse. Nicht dokumentiert werden private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Logs, Output-ROM-Pfade oder lokale Artefaktwerte.

## Smoke-/Reload-Ergebnis

```text
candidateFilesChecked=97
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
pickupLocatorSuccessful=false
pickupItemsTotalBefore=16
pickupItemsTotalAfter=16
pickupItemsTotalReload=0
pickupExpectedCount=16
pickupEntrySize=4
pickupProbabilitySlots=10
pickupProbabilityModelStable=false
pickupItemReloadMismatches=16
pickupTableLengthMismatches=1
pickupProbabilityMismatches=16
pickupCommonRarePolicyViolations=0
invalidPickupItemWrites=0
unloadedPickupItemWrites=0
fallbackPickupItemWrites=0
placeholderPickupItemWrites=0
badPickupItemWrites=not evaluated
pickupTmPolicyViolations=0
pickupPoolAllowedSize=536
pickupTmPoolPolicy=tms allowed
canTMsBeHeld=true
isTMsReusable=false
fieldItemScopeChanged=false
shopItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Bewertung

Der Smoke ist fachlich blockiert.

Positive Teilergebnisse:

- Candidate wurde geladen: `candidateLoaded=true`.
- Randomizer-Write lief durch: `smokeExecuted=true`, `saveSuccessful=true`.
- Log und Output wurden erzeugt: `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- Output-ROM konnte wieder geoeffnet werden: `reloadSuccessful=true`.
- Vor und direkt nach dem Write bleibt der aktive Handler bei `pickupItemsTotalBefore=16` und `pickupItemsTotalAfter=16`.
- Item-Safety im Write-Scope blieb sauber: `invalidPickupItemWrites=0`, `unloadedPickupItemWrites=0`, `fallbackPickupItemWrites=0`, `placeholderPickupItemWrites=0`.
- Keine anderen Itempfade wurden veraendert: `fieldItemScopeChanged=false`, `shopItemScopeChanged=false`, `heldItemScopeChanged=false`.

Blocker:

- Der frische Reload findet die Pickup-Tabelle nicht mehr: `pickupLocatorSuccessful=false`.
- Dadurch ist `pickupItemsTotalReload=0` statt `16`.
- Reload-Vergleich scheitert: `pickupItemReloadMismatches=16`, `pickupTableLengthMismatches=1`, `pickupProbabilityMismatches=16`.

Interpretation:

- Der aktuelle Gen3-Pickup-Pfad verwendet `PickupTableStartLocator`, der offenbar auf den urspruenglichen Tabelleninhalt passt.
- `PickupItemsMod.RANDOM` schreibt die Item-ID-Felder der lokalisierten Tabelle. Danach kann ein frischer Handler dieselbe Tabelle nicht mehr ueber den alten Inhalts-Locator finden.
- Das ist kein Output-/Save-Abbruch und keine Field-/Shop-/Held-Item-Ausweitung, sondern ein enger Pickup-Reload-Locator-Blocker.

## Pickup-Statusentscheidung

- `FVX-ITEM-010 Pickup Items Random`: bleibt `Write modelliert` / blockiert fuer Reload.
- Keine Hochstufung auf `Getestet` oder `GUI-kompatibel`.
- Pickup Ban Bad bleibt ungetestet und darf nicht hochgestuft werden.
- Field Items bleiben in ihrem bereits getesteten Scope unveraendert.
- Shops und Held Items bleiben getrennt und ohne Hochstufung.

## Preserve-/Skip-Folgen

Bis zum Locator-Fix gilt:

- Pickup Random Write nicht als reloadstabil freigeben.
- Ban Bad nicht testen, bevor Random ohne Ban Bad reloadstabil ist.
- Tabellenlaenge `16`, Entry-Size `4` und Probability-Slots `10` bleiben die erwartete Preserve-Basis.
- Spaeterer Fix muss den Tabellenstand nach Write fuer einen frischen Reload wieder auffindbar machen, ohne Field Items, Shops oder Held Items zu beruehren.
- Invalid/unloaded/fallback/placeholder Picks bleiben weiterhin verboten.

## Naechste Empfehlung

Naechster minimaler Block:

- `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`

Ziel:

- Read-only klaeren, wie der Gen3/CFRU-DPE Pickup-Reload-Locator nach einem Random-Write stabilisiert werden kann.
- Pruefen, ob der spaetere Fix eng in `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)` oder in einem kleinen privaten Pickup-Table-Helper bleiben kann.
- Keine Ban-Bad-, Field-Items-, Shop-, Held-Item-, TM/HM/Tutor/Learnset-, Palette/Graphics-, MoveData/MoveNames-, TypeChart-, Trainer/Wild/Evolution- oder Text/Menu-Arbeit.
