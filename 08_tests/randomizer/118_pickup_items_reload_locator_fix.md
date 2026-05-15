# 118 - CFRU/DPE Pickup Items Reload Locator Fix

Datum: 2026-05-15
Branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`
UPR-FVX-Pin vorher: `328e4441c2981d37aba9e2707a6f27f779b026e2`
UPR-FVX-Fix-Commit: `a2373888ad17145f270ebf6ff17303af41aa86eb`
UPR-FVX PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/38>

## Ziel

Dieser Block implementiert und dokumentiert einen engen UPR-FVX-Fix fuer eine reloadstabile Pickup-Table-Lokalisierung nach `PickupItemsMod.RANDOM` im CFRU/DPE Gen9-BPRE-/FRLG-Gate.

Scope bleibt ausschliesslich `FVX-ITEM-010 Pickup Items Random` mit `banBadRandomPickupItems=false`. Pickup Ban Bad, Field Items, Shops, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution, Text/Menu und Scriptparser-Arbeit bleiben ausserhalb.

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
- `08_tests/randomizer/117_pickup_items_reload_locator_blocker_plan.md`
- `08_tests/randomizer/113_field_items_random_even_ban_bad_reload_smoke.md`
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md`
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `01_docs/references/tool-manifest.md`
- `08_tests/randomizer/README.md`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/ItemRandomizer.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/PickupItem.java`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`

## Fix-Entscheidung

Der Fix wurde in `Gen3RomHandler` umgesetzt.

Entscheidung:

- Der bestehende `PickupTableStartLocator` bleibt unveraendert der klassische Primaerpfad.
- Wenn dieser Inhalts-Locator nicht mehr greift und der sichere CFRU/DPE-Gen9-BPRE-Gate aktiv ist, wird eine reloadstabile Metadata-Fallback-Lokalisierung verwendet.
- Der Fallback ignoriert die randomisierten Item-ID-Woerter und vergleicht nur erhaltene Entry-Metadaten aus dem bestehenden FRLG-Locator-Pattern.
- Der Fallback wird nur akzeptiert, wenn genau ein Tabellenkandidat gefunden wird.
- `PickupItemCount=16`, Entry-Size `4`, `PickupItem.PROBABILITY_SLOTS=10` und das Probability-Modell bleiben unveraendert.
- `setPickupItems(...)` schreibt weiterhin nur Item-ID-Felder.

Nicht geaendert:

- kein Pickup Ban Bad
- keine Field Items
- keine Shops
- keine Held Items
- keine TM/HM/Tutor/Learnset-Ausweitung
- keine Scriptparser-Erweiterung

## UPR-FVX Checks

```text
./gradlew :random:classes = passed
```

Kein separater ROMIO-Test wurde ergaenzt. Die vorhandenen klassischen Pickup-Tests bleiben durch den unveraenderten Primaerpfad abgedeckt; der fachlich relevante CFRU/DPE-Fall wurde mit dem unten dokumentierten sanitized Reload-Smoke geprueft.

## Sanitized Pickup-only Reload-Smoke

Ein lokal freigegebener CFRU/DPE Gen9-BPRE-Kandidat wurde fuer einen Pickup-only `FVX-ITEM-010 Pickup Items Random` Smoke mit `banBadRandomPickupItems=false` verwendet. Lokale Harness-, Output- und Log-Artefakte blieben ignored unter `05_builds/**` und wurden nicht committed.

Aggregierte Metriken:

```text
candidateFilesChecked=99
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
pickupLocatorMode=stable-metadata
pickupContentLocatorUsed=false
pickupLocatorCandidateCount=1
pickupLocatorStableAfterWrite=true
pickupReloadLocatorRegression=false
canTMsBeHeld=true
isTMsReusable=false
fieldItemScopeChanged=false
shopItemScopeChanged=false
heldItemScopeChanged=false
exceptionClass=none
stacktrace=none
```

## Ergebnis

Der Reload-Locator-Blocker aus Diagnose 116 ist fuer `PickupItemsMod.RANDOM` mit `banBadRandomPickupItems=false` behoben.

Wesentliche Verbesserung:

- Vor Diagnose 118: Save/Log/Output/Reopen waren erfolgreich, aber frischer Reload fand `0` Pickup-Items.
- Nach Diagnose 118: frischer Reload findet wieder `16` Pickup-Items, Tabellenlaenge und Probability-Modell bleiben stabil, und `pickupItemReloadMismatches=0`.

## Feature-Statusentscheidung

- `FVX-ITEM-010 Pickup Items Random` ist im engen Pickup-only Scope mit `banBadRandomPickupItems=false` `GUI-kompatibel`.
- Pickup Ban Bad bleibt nicht hochgestuft und muss separat getestet werden.
- Field Items, Shops und Held Items werden durch diesen Block nicht neu bewertet.

## Preserve-/Skip-Policy

- Nur eindeutig lokalisierte Pickup-Tabelle schreiben.
- Tabellenlaenge `16`, Slotreihenfolge, Entry-Size `4` und Probability-Slots `10` erhalten.
- `setPickupItems(...)` schreibt nur Item-ID-Felder.
- Invalid, unloaded, fallback und placeholder Items nie als Picks verwenden.
- Ban Bad bleibt inaktiv.
- TMs entsprechend `canTMsBeHeld=true` und `isTMsReusable=false` behandeln.
- Keine Field Items, Shops oder Held Items beruehren.

## Sicherheitsgrenzen

- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Output-ROMs, Logs oder Tool-Binaries committed.
- Keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentiert.
- Keine Original-Upstreams kontaktiert.
