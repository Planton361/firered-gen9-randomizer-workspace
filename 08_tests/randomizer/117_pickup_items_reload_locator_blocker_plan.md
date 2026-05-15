# 117 - CFRU/DPE Pickup Items Reload Locator Blocker Plan

Datum: 2026-05-15
Branch: `analysis/upr-fvx-cfru-dpe-pickup-items-reload-locator-blocker-plan`
UPR-FVX-Pin: `328e4441c2981d37aba9e2707a6f27f779b026e2`

## Ziel

Dieser Block plant read-only, wie der Pickup-Reload-Locator-Blocker nach `PickupItemsMod.RANDOM` behoben werden kann. Es wurde kein Code geaendert, kein Build gestartet, kein Randomizer-Lauf ausgefuehrt und kein ROM-/Output-Artefakt dokumentiert.

Scope bleibt ausschliesslich `FVX-ITEM-010 Pickup Items Random`. Pickup Ban Bad, Field Items, Shops, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser-Arbeit bleiben ausserhalb.

## Voraussetzungen / Ausgangsstand

- Workspace PR #161 (`docs: record pickup items random smoke`) wurde vor Branch-Erstellung als gemerged verifiziert.
- Branch wurde von aktuellem `origin/main` erstellt.
- Workspace-Submodule `02_external/upr-fvx` steht auf `328e4441c2981d37aba9e2707a6f27f779b026e2`.
- Diagnose 115 bestaetigte read-only den Pickup-Table-Locator vor einem Write: `pickupLocatorSuccessful=true`, `pickupItemsTotal=16`, `pickupEntrySize=4`, `pickupProbabilitySlots=10`, `pickupProbabilityModelStable=true`.
- Diagnose 116 bestaetigte Save/Log/Output/Reopen nach Pickup Random, blockierte aber beim frischen Pickup-Reload: `pickupLocatorSuccessful=false`, `pickupItemsTotalReload=0`, `pickupItemReloadMismatches=16`, `pickupTableLengthMismatches=1`, `pickupProbabilityMismatches=16`.

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/097_field_items_shops_pickup_scope_plan.md`
- `08_tests/randomizer/114_pickup_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/115_pickup_items_scope_diagnostics.md`
- `08_tests/randomizer/116_pickup_items_random_reload_smoke.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`

## Betroffene UPR-FVX-Codepfade

### Orchestrierung und Randomizer

- `GameRandomizer.maybeRandomizePickupItems()` ruft `ItemRandomizer.randomizePickupItems()` nur bei `Settings.PickupItemsMod.RANDOM` auf.
- `ItemRandomizer.randomizePickupItems()` baut den Pickup-Pool aus `romHandler.getAllowedItems()` oder bei aktivem Ban Bad aus `romHandler.getNonBadItems()`.
- TMs werden nur entfernt, wenn `!romHandler.canTMsBeHeld()` oder `romHandler.isTMsReusable()`.
- Der Randomizer liest aktuelle Slots via `romHandler.getPickupItems()`, kopiert die modellierten `PickupItem.PROBABILITY_SLOTS` und schreibt die neuen Items via `romHandler.setPickupItems(newItems)`.

### Gen3RomHandler Pickup-Pfad

`Gen3RomHandler.getPickupItems()`:

- liest `PickupItemCount` aus der ROM-Entry-Konfiguration.
- setzt die Entry-Groesse auf `2` fuer Emerald, sonst `4`.
- sucht den Tabellenstart nur dann, wenn `pickupItemsTableOffset == 0`.
- nutzt `PickupTableStartLocator` als Inhalts-Pattern via `find(...)`.
- cached den gefundenen Offset nur in der aktuellen Handler-Instanz.
- liest pro Eintrag ein `u16` Item-Feld und mappt es mit `Gen3Constants.itemIDToStandard(...)`.
- modelliert danach die 10 Probability-Slots aus dem Rom-Typ; fuer FRLG sind es 16 Eintraege mit fester Wahrscheinlichkeitsverteilung.

`Gen3RomHandler.setPickupItems(...)`:

- nutzt denselben `pickupItemsTableOffset` der aktuellen Handler-Instanz.
- schreibt pro Eintrag nur das `u16` Item-Feld ueber `Gen3Constants.itemIDToInternal(...)`.
- schreibt keine Probability-Felder separat.
- fuehrt keine neue Lokalisierung aus, wenn der Offset bereits in derselben Handler-Instanz gecached ist.

### ROM-Entry-Konfiguration

Fuer den FRLG/BPRE-Pfad ist der relevante ROM-Entry klassisch inhaltsbasiert:

- `PickupTableStartLocator=8B000F00850019008600230087002D`
- `PickupItemCount=16`

Es wurde kein stabiler separater Pickup-Tabellen-Offset oder Pointer im gelesenen Konfigurationspfad identifiziert, der bereits statt des Inhalts-Locators verwendet wird.

## Blocker-Einschaetzung

Der aktive Blocker ist sehr wahrscheinlich kein Write-Fehler im eigentlichen Pickup-Item-ID-Write, sondern ein Reload-Locator-Problem.

Begruendung:

- Diagnose 116 zeigt in derselben Handler-Instanz nach dem Write weiterhin `pickupItemsTotalAfter=16`.
- Das ist plausibel, weil `pickupItemsTableOffset` in dieser Handler-Instanz bereits vor dem Write gefunden und gecached wurde.
- `setPickupItems(...)` veraendert die Item-ID-Woerter, die Teil des `PickupTableStartLocator`-Patterns sind.
- Ein frischer Reload hat keinen gecachten `pickupItemsTableOffset` und sucht erneut nach dem urspruenglichen Inhalts-Pattern.
- Nach Randomization stimmt dieses Pattern nicht mehr; daher liefert der frische Handler `pickupItemsTotalReload=0` und `pickupLocatorSuccessful=false`.

Die Wahrscheinlichkeit ist hoch, dass `PickupTableStartLocator` aktuell eine konkrete Anfangssequenz der Vanilla-/FRLG-Pickup-Items sucht und deshalb nicht reloadstabil ist, sobald die Pickup-Items randomisiert wurden.

## Mögliche Fix-Optionen

### Option A: Stabilen Tabellen-Offset im ROM-Entry nutzen

- Einen festen, ROM-entry-basierten Pickup-Tabellenstart fuer den CFRU/DPE Gen9-BPRE-/FRLG-Pfad einfuehren oder nutzen, falls er eindeutig belegbar ist.
- `getPickupItems()` wuerde im sicheren Gate zuerst diesen stabilen Offset verwenden und nur als Fallback den bestehenden Locator nutzen.
- Vorteil: frischer Reload ist unabhaengig vom Inhalt der randomisierten Pickup-Tabelle.
- Risiko: der feste Offset darf nicht aus privaten Artefakten dokumentiert werden und muss reviewbar im UPR-FVX-Konfigurations-/Gate-Kontext stehen.

### Option B: Pointer-/Referenz-basierte Lokalisierung

- Statt des Pickup-Inhalts-Patterns eine stabile Pointer- oder Code-Referenz zur Pickup-Tabelle suchen.
- Vorteil: reloadstabil, solange Pointer/Routine unveraendert bleiben.
- Risiko: breiter als Option A, weil Pointer-/Code-Referenzen fuer CFRU/DPE sauber modelliert werden muessen.

### Option C: Inhalts-Locator breiter machen

- Locator nicht auf konkrete Item-ID-Werte stuetzen, sondern auf erhaltene Entry-Struktur, Count, Entry-Size oder Probability-/Levelbereich-Kontext.
- Risiko: Struktur allein kann zu viele Kandidaten liefern; False Positives waeren gefaehrlicher als der aktuelle Blocker.

### Option D: Nur Handler-internen Cache verwenden

- Das passiert faktisch bereits und erklaert `pickupItemsTotalAfter=16`.
- Als alleiniger Fix ungeeignet, weil ein frischer Reload eine neue Handler-Instanz ohne Cache ist.

## Empfohlener enger Fix-Scope

Empfohlen wird ein enger UPR-FVX-Fix in `Gen3RomHandler.getPickupItems()` / `setPickupItems(...)` oder einem kleinen privaten Pickup-Table-Helper:

1. Im sicheren CFRU/DPE Gen9-BPRE-/FRLG-Gate eine reloadstabile Pickup-Table-Lokalisierung einfuehren.
2. Bevorzugt einen ROM-Entry-Wert oder eine stabile, nicht item-inhaltsabhaengige Referenz verwenden.
3. Den bestehenden `PickupTableStartLocator` als Fallback fuer klassische unveraenderte ROMs erhalten.
4. `PickupItemCount=16`, Entry-Size `4` und Probability-Modell unveraendert lassen, solange kein separater Befund eine andere CFRU/DPE-Struktur belegt.
5. `setPickupItems(...)` weiterhin nur die Item-ID-Felder schreiben lassen.
6. Keine Ban-Bad-Pickup-Logik, keine Field-Items-, Shop-, Held-Item- oder TM/HM/Tutor/Learnset-Ausweitung einbauen.

Falls keine stabile Adresse oder Pointer-/Referenzquelle reviewbar belegt werden kann, sollte vor einem Fix ein weiterer read-only Locator-Diagnoseblock geplant werden.

## Preserve-/Skip-Policy

- Nur die eindeutig lokalisierte Pickup-Tabelle schreiben.
- Tabellenlaenge `16`, Slotreihenfolge, Entry-Size `4` und Probability-Slots `10` erhalten.
- `setPickupItems(...)` schreibt nur Item-ID-Felder.
- Invalid, unloaded, fallback und placeholder Items nie als Picks verwenden.
- Ban Bad bleibt inaktiv, bis Random ohne Ban Bad reloadstabil ist.
- TMs entsprechend `canTMsBeHeld=true` und `isTMsReusable=false` behandeln; keine globale TM-Policy ableiten.
- Keine Field Items, Shops, Encounter Held Items, Trainer Held Items oder Starter Held Items beruehren.

## Spaetere Fix-/Smoke-Kriterien

Ein spaeterer enger Fix-Smoke fuer `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false` sollte mindestens berichten:

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
pickupExpectedCount=16
pickupEntrySize=4
pickupProbabilitySlots=10
pickupProbabilityModelStable=true
pickupItemReloadMismatches=0
pickupTableLengthMismatches=0
pickupProbabilityMismatches=0
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

Zusaetzlich sinnvoll fuer den Fix:

```text
pickupLocatorMode=stable-offset oder stable-reference
pickupContentLocatorUsed=false nach randomisiertem Reload, falls Fallback nicht noetig ist
pickupLocatorCandidateCount=1
pickupLocatorStableAfterWrite=true
pickupReloadLocatorRegression=false
```

Keine Raw Pointer, Offsets, ROM-Namen, lokale Pfade, Hashes, Raw-Bytes, Logs oder Output-Pfade dokumentieren.

## Pickup Ban Bad Status

Pickup Ban Bad bleibt blockiert, bis `PickupItemsMod.RANDOM` mit `banBadRandomPickupItems=false` reloadstabil ist.

Begruendung:

- Ban Bad ist ein Poolfilter auf demselben Pickup-Writer.
- Der aktuelle Blocker liegt unterhalb der Poolfilter-Ebene in der frischen Tabellenlokalisierung.
- Ein Ban-Bad-Smoke wuerde denselben Reload-Locator-Fehler erben und keine zusaetzliche fachliche Aussage liefern.

## Empfehlung

Naechster minimaler Schritt:

- `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`

Ziel:

- Minimalen UPR-FVX-Fix fuer eine reloadstabile Pickup-Table-Lokalisierung vorbereiten.
- Danach denselben Pickup-only Random-Smoke aus Diagnose 116 wiederholen.
- Keine Ban-Bad-Pickup-Arbeit vor erfolgreichem Random-ohne-Ban-Smoke.
