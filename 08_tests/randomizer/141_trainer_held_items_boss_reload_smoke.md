# Diagnose 141 - Boss Trainer Held Items Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-trainer-held-items-boss-reload-smoke`
Scope: CFRU/DPE Gen9-BPRE Boss Trainer Held Items Write/Reload-Smoke

## Ziel

Dieser Block testet ausschliesslich Trainer Held Items im engen Boss-Trainers-only Scope.

Getesteter Scope:

- `randomizeHeldItemsForBossTrainerPokemon=true`
- `randomizeHeldItemsForImportantTrainerPokemon=false`
- `randomizeHeldItemsForRegularTrainerPokemon=false`
- `consumableItemsOnlyForTrainers=false`
- `sensibleItemsOnlyForTrainers=false`
- `highestLevelGetsItemsForTrainers=false`
- keine Wild/Encounter Held Items
- keine Starter Held Items
- keine Field Items
- kein Pickup
- keine Shops

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Projekt-Build
- keine Important Trainer Held Items
- keine Regular Trainer Held Items
- keine Wild/Encounter Held Items
- keine Starter Held Items
- keine Field Items
- kein Pickup
- keine Shops
- keine Evolution-, Learnset-, TM/HM/Tutor-, Move-, Ability-, TypeChart-, Palette-, Graphics- oder Text/Menu-Arbeit
- keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries committen
- keine privaten Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes, Scriptdaten, Secrets, Tokens oder `.env`-Inhalte dokumentieren
- keine Original-Upstreams kontaktieren

## Gelesene Dateien

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `08_tests/randomizer/137_held_items_scope_diagnostics_plan.md`
- `08_tests/randomizer/138_held_items_scope_diagnostics.md`
- `08_tests/randomizer/139_wild_held_items_reload_smoke.md`
- `08_tests/randomizer/140_wild_held_items_ban_bad_reload_smoke.md`
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Smoke-Methode

- Verwendet wurde ein temporaerer Harness ausserhalb des Repositories.
- Die lokal freigegebene CFRU/DPE Gen9-BPRE-Kandidatenquelle wurde fuer diesen Block verwendet.
- Der Harness setzte nur den Boss-Trainer-Held-Items-Pfad.
- Lokale Output-ROM- und Log-Artefakte blieben ausserhalb der Dokumentation und wurden nicht committed.
- Die Dokumentation enthaelt nur aggregierte, sanitizte Metriken.
- Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten werden nicht wiedergegeben.

Vergleichsmodell:

- Trainer Held Items wurden ueber `TrainerPokemon.heldItem` verglichen, nicht ueber Species/BaseStats.
- Boss Trainer wurden als Write-Scope gemessen.
- Important Trainer, Regular Trainer und `shouldNotGetBuffs`-Trainer wurden preserve-only gemessen.
- Wild/Encounter und Starter Held Items wurden als Fremdscopes per Fingerprint abgesichert.
- Field Items, Pickup und Shops wurden als Fremdscopes unveraendert erwartet.

## Smoke-Ergebnis

PASS.

```text
candidateFilesChecked=3
candidateLoaded=true
smokeExecuted=true
saveSuccessful=true
logSuccessful=true
outputRomExists=true
logNonEmpty=true
reloadSuccessful=true
trainerHeldItemsTotalBefore=1754
trainerHeldItemsTotalAfter=1754
trainerHeldItemsTotalReload=1754
trainerHeldItemsNonZeroBefore=87
trainerHeldItemsNonZeroAfter=153
trainerHeldItemsNonZeroReload=153
trainerHeldItemsBadBefore=0
trainerHeldItemsBadAfter=15
trainerHeldItemsBadReload=15
trainerHeldItemsTMBefore=0
trainerHeldItemsTMAfter=0
trainerHeldItemsTMReload=0
bossTrainerHeldItemsTotalBefore=74
bossTrainerHeldItemsTotalAfter=74
bossTrainerHeldItemsTotalReload=74
importantTrainerHeldItemsTotalBefore=117
importantTrainerHeldItemsTotalAfter=117
importantTrainerHeldItemsTotalReload=117
regularTrainerHeldItemsTotalBefore=1563
regularTrainerHeldItemsTotalAfter=1563
regularTrainerHeldItemsTotalReload=1563
bossTrainerHeldItemReloadMismatches=0
importantTrainerHeldItemMismatchesAfter=0
importantTrainerHeldItemMismatchesReload=0
regularTrainerHeldItemMismatchesAfter=0
regularTrainerHeldItemMismatchesReload=0
shouldNotGetBuffsTrainerHeldItemMismatchesAfter=0
shouldNotGetBuffsTrainerHeldItemMismatchesReload=0
invalidTrainerHeldItemWrites=0
unloadedTrainerHeldItemWrites=0
fallbackTrainerHeldItemWrites=0
placeholderTrainerHeldItemWrites=0
heldItemPoolAllowedSize=212
heldItemPoolNonBadSize=161
canTMsBeHeld=true
wildHeldItemScopeChanged=false
starterHeldItemScopeChanged=false
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass=none
stacktrace=none
```

Bewertung:

- Save, Log, Output und Reload waren erfolgreich.
- Boss-Trainer-Held-Items reloaden stabil: `bossTrainerHeldItemReloadMismatches=0`.
- Important Trainer, Regular Trainer und `shouldNotGetBuffs`-Trainer blieben unveraendert.
- Es entstanden keine invaliden, ungeladenen, Fallback- oder Placeholder-Writes.
- Wild Held Items, Starter Held Items, Field Items, Pickup und Shops blieben unveraendert.
- Trainer Held Items sind nur fuer Boss Trainers im getesteten Scope GUI-kompatibel.

## Trainer-Held-Items-Befund

Baseline aus Diagnose 138:

- `trainerHeldItemsReadable=true`
- `trainerHeldItemsTotal=1754`
- `trainerHeldItemsNonZero=87`
- `trainerHeldItemsBad=0`
- `trainerHeldItemsTM=0`
- `bossTrainerHeldItemsTotal=74`
- `importantTrainerHeldItemsTotal=117`
- `regularTrainerHeldItemsTotal=1563`

Smoke-Befund:

- TrainerPokemon-Held-Item-Slots blieben stabil: `1754/1754/1754`.
- Nicht-leere Trainer-Held-Items stiegen erwartungsgemaess durch Boss-Trainer-Writes: `87/153/153`.
- Bad Items im Trainer-Held-Item-Bestand stiegen auf `0/15/15`, weil fuer Trainer in diesem Scope kein Ban-Bad-Filter aktiv ist.
- TM-Held-Items blieben bei `0/0/0`.
- Boss-Trainer-Scope umfasst `74/74/74` TrainerPokemon-Slots.

## Preserve-/Trainerklasse-Befund

- Important-Trainer-Slots blieben stabil: `117/117/117`.
- Regular-Trainer-Slots blieben stabil: `1563/1563/1563`.
- `importantTrainerHeldItemMismatchesAfter=0`.
- `importantTrainerHeldItemMismatchesReload=0`.
- `regularTrainerHeldItemMismatchesAfter=0`.
- `regularTrainerHeldItemMismatchesReload=0`.
- `shouldNotGetBuffsTrainerHeldItemMismatchesAfter=0`.
- `shouldNotGetBuffsTrainerHeldItemMismatchesReload=0`.

Bewertung:

- Boss Trainers only wurde eingehalten.
- Important und Regular Trainer wurden nicht veraendert.
- `shouldNotGetBuffs`-Trainer blieben preserve-only.

## Reload-Befund

- `reloadSuccessful=true`.
- `bossTrainerHeldItemReloadMismatches=0`.
- `invalidTrainerHeldItemWrites=0`.
- `unloadedTrainerHeldItemWrites=0`.
- `fallbackTrainerHeldItemWrites=0`.
- `placeholderTrainerHeldItemWrites=0`.

Bewertung:

- Die geschriebenen Boss-Trainer-Held-Items reloaden stabil.
- Teamflags und TrainerPokemon-Strukturbreiten blieben fuer den dokumentierten Scope konsistent genug, um alle TrainerPokemon-Held-Item-Slots reloadstabil wiederzufinden.

## Scope-Isolation-Befund

- `wildHeldItemScopeChanged=false`.
- `starterHeldItemScopeChanged=false`.
- `fieldItemScopeChanged=false`.
- `pickupScopeChanged=false`.
- `shopScopeChanged=false`.

Bewertung:

- Keine Wild/Encounter-Held-Items wurden veraendert.
- Keine Starter-Held-Items wurden veraendert.
- Field Items, Pickup und Shops blieben ausserhalb des Scopes.

## Risiken / Blocker

Kein Blocker fuer den naechsten Important Trainer Held Items Smoke.

Weiterhin relevant:

- Important Trainer Held Items und Regular Trainer Held Items bleiben getrennte Subscopes und werden durch Diagnose 141 nicht hochgestuft.
- Trainer-Bad-Items sind in diesem Scope erlaubt; ein separater Trainer-Poolfilter-Block waere noetig, falls ein Filter existiert oder gewuenscht ist.
- Consumable-, Sensible- und Highest-Level-Filter bleiben ungetestet.
- Starter Held Items bleiben ein eigener spaeterer Subscope.

## Feature-Status

- Wild/Encounter Held Items ohne Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 139.
- Wild/Encounter Held Items + Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 140.
- Trainer Held Items Boss Trainers only: GUI-kompatibel im getesteten Scope durch Diagnose 141.
- Trainer Held Items Important/Regular: offen.
- Starter Held Items: offen.
- Field Items, Pickup und Shops bleiben unveraendert.

## Naechster minimaler Schritt

`test/upr-fvx-cfru-dpe-trainer-held-items-important-reload-smoke`: Important Trainer Held Items Smoke, nur wenn Boss-Trainer-Held-Items-Reloadstabilitaet aus Diagnose 141 akzeptiert ist.
