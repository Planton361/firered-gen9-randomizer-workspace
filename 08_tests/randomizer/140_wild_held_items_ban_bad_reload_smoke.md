# Diagnose 140 - Wild Held Items Ban Bad Reload Smoke

Datum: 2026-05-15
Branch: `test/upr-fvx-cfru-dpe-wild-held-items-ban-bad-reload-smoke`
Scope: CFRU/DPE Gen9-BPRE Wild/Encounter Held Items + Ban Bad Write/Reload-Smoke

## Ziel

Dieser Block testet ausschliesslich Wild/Encounter Held Items mit Ban Bad.

Getesteter Scope:

- `randomizeWildPokemonHeldItems=true`
- `banBadRandomWildPokemonHeldItems=true`
- keine Trainer Held Items
- keine Starter Held Items
- keine Field Items
- kein Pickup
- keine Shops

Ausdruecklich ausserhalb des Scopes:

- keine Codeaenderung
- keine Aenderung an `02_external/**`
- keine Submodule-Pin-Aenderung
- kein Projekt-Build
- keine Trainer Held Items
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
- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `00_project-control/roadmap/roadmap-status.md`
- `08_tests/randomizer/README.md`
- `01_docs/references/tool-manifest.md`

## Smoke-Methode

- Verwendet wurde ein temporaerer Harness ausserhalb des Repositories.
- Die lokal freigegebene CFRU/DPE Gen9-BPRE-Kandidatenquelle wurde fuer diesen Block verwendet.
- Der Harness setzte nur den Wild/Encounter-Held-Items-Pfad mit Ban Bad.
- Lokale Output-ROM- und Log-Artefakte blieben ausserhalb der Dokumentation und wurden nicht committed.
- Die Dokumentation enthaelt nur aggregierte, sanitizte Metriken.
- Private Pfade, ROM-Namen, Hashes, Pointer, Offsets, Raw-Bytes und Scriptdaten werden nicht wiedergegeben.

Vergleichsmodell:

- Wild/Encounter Held Items wurden als Species/BaseStats-Held-Item-Felder verglichen, nicht als Encounter-Slots.
- Der Reload-Vergleich nutzt die stabile interne SpeciesSet-Identitaet.
- Fallback-/Placeholder-Bestand aus Diagnose 138 wurde beobachtet, aber nur neue invalid/unloaded/fallback/placeholder Writes gelten als Smoke-Fehler.
- Bad-Item-Writes wurden nur fuer geaenderte Wild-Held-Item-Slots im Ban-Bad-Write gezaehlt.

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
wildHeldItemsTotalBefore=5656
wildHeldItemsTotalAfter=5656
wildHeldItemsTotalReload=5656
wildHeldItemsNonZeroBefore=526
wildHeldItemsNonZeroAfter=320
wildHeldItemsNonZeroReload=320
wildHeldItemsBadBefore=174
wildHeldItemsBadAfter=0
wildHeldItemsBadReload=0
wildHeldItemsTMBefore=0
wildHeldItemsTMAfter=0
wildHeldItemsTMReload=0
wildHeldItemReloadMismatches=0
invalidWildHeldItemWrites=0
unloadedWildHeldItemWrites=0
fallbackWildHeldItemWrites=0
placeholderWildHeldItemWrites=0
badWildHeldItemWrites=0
heldItemPoolAllowedSize=212
heldItemPoolNonBadSize=161
badWildHeldItemPoolCandidates=51
badWildHeldItemPoolExcluded=51
canTMsBeHeld=true
trainerHeldItemScopeChanged=false
starterHeldItemScopeChanged=false
fieldItemScopeChanged=false
pickupScopeChanged=false
shopScopeChanged=false
exceptionClass=none
stacktrace=none
```

Bewertung:

- Save, Log, Output und Reload waren erfolgreich.
- Wild/Encounter-Held-Item-Reload ist stabil: `wildHeldItemReloadMismatches=0`.
- Ban Bad wirkte auf den Wild-Held-Item-Pool: `badWildHeldItemWrites=0`, `wildHeldItemsBadAfter=0`, `wildHeldItemsBadReload=0`.
- Es entstanden keine invaliden, ungeladenen, Fallback- oder Placeholder-Writes.
- Trainer Held Items, Starter Held Items, Field Items, Pickup und Shops blieben unveraendert.
- Wild/Encounter Held Items + Ban Bad sind im getesteten CFRU/DPE Gen9-BPRE Scope GUI-kompatibel.

## Wild/Encounter-Held-Items-Befund

Baseline:

- Diagnose 138: `wildHeldItemsTotal=5656`, `wildHeldItemsNonZero=526`, `wildHeldItemsBad=174`.
- Diagnose 139: Wild/Encounter Held Items ohne Ban Bad reloadstabil mit `wildHeldItemReloadMismatches=0`.

Smoke-Befund:

- Die Gesamtzahl der gemessenen Species/BaseStats-Held-Item-Slots blieb stabil: `5656/5656/5656`.
- Nicht-leere Slots veraenderten sich erwartungsgemaess durch Randomisierung: `526/320/320`.
- Bad Items wurden durch Ban Bad entfernt: `174/0/0`.
- TM-Held-Items blieben bei `0/0/0`.
- `canTMsBeHeld=true` bleibt Messpflicht fuer spaetere Held-Item-Smokes.

## Ban-Bad-/Pool-Befund

- `heldItemPoolAllowedSize=212`.
- `heldItemPoolNonBadSize=161`.
- `badWildHeldItemPoolCandidates=51`.
- `badWildHeldItemPoolExcluded=51`.
- `badWildHeldItemWrites=0`.

Bewertung:

- Ban Bad schaltet den Wild-Held-Item-Pool vom Allowed-Pool auf den Non-Bad-Pool.
- Alle 51 Bad-Item-Kandidaten wurden aus dem Pool ausgeschlossen.
- Nach Write und Reload wurden keine Bad Wild-Held-Items geschrieben.

## Reload-Befund

- `reloadSuccessful=true`.
- `wildHeldItemReloadMismatches=0`.
- `invalidWildHeldItemWrites=0`.
- `unloadedWildHeldItemWrites=0`.
- `fallbackWildHeldItemWrites=0`.
- `placeholderWildHeldItemWrites=0`.

Bewertung:

- Die geschriebenen Wild/Encounter-Held-Items reloaden stabil.
- Die Ban-Bad-Wirkung bleibt nach Reload erhalten.
- Fallback-/Placeholder-Bestand aus Diagnose 138 wurde nicht als neuer Write reproduziert.

## Scope-Isolation-Befund

- `trainerHeldItemScopeChanged=false`.
- `starterHeldItemScopeChanged=false`.
- `fieldItemScopeChanged=false`.
- `pickupScopeChanged=false`.
- `shopScopeChanged=false`.

Bewertung:

- Keine Trainer-Held-Items wurden veraendert.
- Keine Starter-Held-Items wurden veraendert.
- Field Items, Pickup und Shops blieben ausserhalb des Scopes.

## Risiken / Blocker

Kein Blocker fuer den naechsten Trainer Held Items Scope/Smoke.

Weiterhin relevant:

- Trainer Held Items und Starter Held Items bleiben getrennte Subscopes und werden durch Diagnose 140 nicht hochgestuft.
- Fallback-/Placeholder-Bestand bleibt ein Safety-Risiko fuer spaetere Trainer-/Starter-Smokes.
- Trainer-Held-Items brauchen eigene Teamflag-/TrainerPokemon-Preserve-Checks.
- Starter-Held-Items brauchen eigenen `getStarterHeldItems()` / `setStarterHeldItems(...)` Reloadvergleich.

## Feature-Status

- Wild/Encounter Held Items ohne Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 139.
- Wild/Encounter Held Items + Ban Bad: GUI-kompatibel im getesteten Scope durch Diagnose 140.
- Trainer Held Items: bleibt offen.
- Starter Held Items: bleibt offen.
- Field Items, Pickup und Shops bleiben unveraendert.

## Naechster minimaler Schritt

`analysis/upr-fvx-cfru-dpe-trainer-held-items-scope-plan` oder ein enger Trainer Held Items Smoke, bevorzugt Boss Trainers only ohne Consumable/Sensible/Highest-Level-Filter, wenn kein weiterer Planblock gewuenscht ist.
