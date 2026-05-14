# 106 - CFRU/DPE Field Items Random TM-pool Reload-Smoke

Datum: 2026-05-15

Branch: `test/upr-fvx-cfru-dpe-field-items-random-tm-pool-reload-smoke`

UPR-FVX-Pin: `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`

## Ziel

Sanitisierter Field-Items-only Write-/Reload-Smoke fuer `FVX-ITEM-002 Field Items Random` mit `banBadRandomFieldItems=false` nach dem UPR-FVX-Fix aus PR #36.

Nicht im Scope:

- Field Items Shuffle
- Random Even Distribution
- Ban Bad Items
- Shops
- Pickup
- Encounter/Trainer/Starter Held Items
- TM/HM/Tutor/Learnset-Writer
- Palette/Graphics
- MoveData/MoveNames
- TypeChart/TypeEffectiveness
- Trainer/Wild/Evolution/Text/Menu
- Scriptparser-Erweiterung

## Smoke-Ergebnis

Der Smoke wurde ausgefuehrt, ist aber weiterhin vor Output/Reload blockiert.

Sanitisierte Pflichtmetriken:

- `candidateFilesChecked=95`
- `candidateLoaded=true`
- `smokeExecuted=true`
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- `reloadSuccessful=false`
- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `fieldItemsTotalReload=0`
- `fieldItemReloadMismatches=339`
- `visibleFieldItemReloadMismatches=339`
- `hiddenFieldItemReloadMismatches=339`
- `tmFieldItemSlotMismatches=339`
- `nonTmFieldItemSlotMismatches=339`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0`
- `exceptionClass=com.uprfvx.random.exceptions.RandomizationException`
- `stacktrace=com.uprfvx.random.exceptions.RandomizationException`

Sanitisierte TM-Pool-Metriken:

- `randomTmNeededSlots=0`
- `randomTmCurrentSlots=0`
- `randomTmRequiredTotal=24`
- `randomTmRequiredPresent=24`
- `randomTmRequiredMissingBefore=0`
- `randomTmRequiredMissingAfter=0`
- `randomTmLoadedPoolSize=50`
- `randomTmAllowedPoolSize=0`
- `randomTmUniquePoolSize=50`
- `randomTmFillerNeeded=0`
- `randomTmFillerAvailable=26`
- `randomTmDuplicateSelections=0`
- `randomTmPoolDeficit=0`
- `randomTmResultSize=0`
- `randomTmResultUniqueSize=0`

Nicht-private Exception-Ursache:

- `exceptionMessage=Could not randomize TM field items, more required TMs than TM field item slots.`

## Einordnung

Der urspruengliche Unique-TM-Filler-Pool-Blocker aus Diagnose 103/104 ist nicht mehr der aktive Engpass:

- `randomTmLoadedPoolSize=50`
- `randomTmUniquePoolSize=50`
- `randomTmFillerAvailable=26`
- `randomTmPoolDeficit=0`

Der neue Blocker liegt im API-/Scope-Mismatch zwischen Raw-Field-Item-Diagnose und `romHandler.getFieldItems()`:

- Raw-Diagnosen 100/103/104 fanden `tmFieldItemSlots=28` und `requiredFieldTMsTotal=24`.
- Der Randomizer-TM-Pfad sieht im aktuellen `getFieldItems()`-API-Scope aber `randomTmNeededSlots=0` / `randomTmCurrentSlots=0`.
- Dadurch ist `requiredTMs.size() > neededTMAmount` und der PR-#36-Schutz bricht korrekt mit `RandomizationException` ab.

Das ist kein Reload-Mismatch und kein Preserve-Write-Fehler, weil kein Output-ROM erzeugt wurde.

## Preserve-/Skip-Folgen

Bis zum Abbruch blieben die Preserve-Grenzen stabil:

- `fieldItemsTotalBefore=339`
- `fieldItemsTotalAfter=339`
- `requiredFieldTMMissingAfter=0`
- `requiredItemPolicyViolations=0`
- `progressionItemPolicyViolations=0`
- `invalidFieldItemWrites=0`
- `unloadedFieldItemWrites=0`
- `fallbackFieldItemWrites=0`
- `placeholderFieldItemWrites=0`
- `disallowedFieldItemWrites=0`
- `scriptPatternExpansion=0`
- `badFieldItemWrites=0`

Da kein Output/Reload vorliegt, sind Reload-Mismatch-Zahlen nur Blocker-Folgen und nicht als Writer-Preserve-Verletzung zu werten.

## Feature-Status

- `FVX-ITEM-001 Field Items Shuffle`: bleibt `GUI-kompatibel` im engen allowed-slot Scope aus Diagnose 102.
- `FVX-ITEM-002 Field Items Random`: bleibt `Write modelliert` / blockiert; keine GUI-kompatibel-Hochstufung.
- `FVX-ITEM-003 Field Items Random even distribution`: bleibt `Write modelliert`.
- `FVX-ITEM-004 Field Items Ban Bad Items`: bleibt `Write modelliert`.

## Lokale Artefakte

Der lokale Smoke-Harness und dessen Output bleiben unter ignored `05_builds/**`.

Keine ROMs, Output-ROMs, Logs, private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Map-Daten, Script-Bytes, Secrets oder `.env`-Inhalte werden dokumentiert oder committed.

## Checks

- Workspace: `git status --short`
- Workspace: `git submodule status --recursive`
- Workspace: `git diff --stat`
- Workspace: `git diff --submodule`
- Workspace: `git diff --check`
- Workspace: `git diff --cached --check`
- Local smoke prerequisite: `./gradlew :random:classes` completed successfully to refresh local classes for UPR-FVX pin `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd`.

## Naechster minimaler Schritt

Planblock fuer den neuen API-/Scope-Blocker:

- `analysis/upr-fvx-cfru-dpe-field-items-random-api-tm-slot-scope-plan`

Ziel:

- Read-only klaeren, warum `Gen3RomHandler.getFieldItems()` / `setFieldItems(...)` im CFRU/DPE-Gen9-BPRE-Scope keine TM-Field-Item-Slots an `ItemRandomizer.randomizeTMFieldItems(...)` uebergibt, obwohl Raw-Map-/Script-Diagnosen `tmFieldItemSlots=28` und `requiredFieldTMsTotal=24` belegen.
