# 075 - Wild Filter Carrier Nullslot Fix Diagnostics

Datum: 2026-05-14

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-wild-filter-carrier-nullslot-fix`

## Ziel

Dieses Protokoll dokumentiert den eng gegateten UPR-FVX-Fix fuer die Wild-Blocker aus Diagnose 070:

- `FVX-WILD-011` Wild Similar Strength
- `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary
- gemeinsamer Carrier: `FVX-WILD-001` Standard/Fallback-Wild

Der Fix bleibt auf den WildEncounterRandomizer-Mapping-/InfoMap-Scope begrenzt. TypeChart, MoveData, Palette, Items, Encounter Held Items, custom Day/Night-Wild, Catch Em All, Minimum Catch Rate, Level Modifier, Text/Menu, Graphics und andere Writer wurden nicht geaendert oder aktiviert.

## UPR-FVX-Fix

Commit: `acaada514d04b1d306581ce872d2d77fe1b4c5b3`

Geaenderte Datei:

- `random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`

Fixinhalt:

- `randomizeArea()` behandelt `Encounter`-Slots mit `species == null` vor der normalen Mapping-/InfoMap-Auswahl.
- Null/unaufloesbare Encounter-Slots werden nicht als valide `zoneMap`-/InfoMap-Anker genutzt.
- Fuer solche Slots wird ein Replacement aus dem bestehenden `remaining`-/`allowed`-Pool gewaehlt.
- Ein vorhandenes Zone-Theme wird respektiert, wenn es vorhanden ist.
- Vorhandene `EncounterArea`-Bans werden weiter angewendet.
- Similar Strength und Keep Primary werden fuer den Nullslot selbst nicht auf `current == null` dereferenziert; normale nicht-null Slots nutzen weiter die bestehenden BST-/Type-Filterpfade.

Nicht geaendert:

- Keine Wild-Tabellenfamilie wurde hinzugefuegt.
- Kein Gen3RomHandler-Wild-Read-/Write-Pfad wurde geaendert.
- `SpeciesSet.add(...)` blieb unveraendert.
- Placeholder-/Special-Species-Bans aus dem bestehenden Wild-Scope wurden nicht aufgeweicht.

## Lokale Smokes

Die zwei passenden Slices wurden einzeln lokal ausgefuehrt. Lokale ROM-, Output-ROM-, Log-, Build- und Diagnoseartefakte blieben ignored und werden nicht committed oder dokumentiert. Es werden keine privaten Pfade, ROM-Namen, Hashes oder Loginhalte dokumentiert.

### `FVX-WILD-011` Wild Similar Strength

- Aktive Feature-ID: `FVX-WILD-011`
- Carrier-Writer: `FVX-WILD-001` Standard/Fallback-Wild
- Normalisierte Settings: `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `wildPokemonTypeMod=NONE`, `similarStrengthEncounters=true`, `useTimeBasedEncounters=true`, `splitByEncounterType=false`, `catchEmAll=false`, `wildHeldItems=false`, `minimumCatchRateLevel=0`, `wildLevelModifier=0`, `palettes=UNCHANGED`, `typeEffectiveness=UNCHANGED`, `updateMoves=false`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich: `true`
- `writeReloadWildPokemonMismatches=0`
- `filterViolations=not separately asserted`
- `Bad Egg=false`
- `<unknown>=false`
- `exceptionClass/stacktrace=none`
- `nullSlotsBefore=0`
- `nullSlotsAfter=0`

Ergebnis: Der Similar-Strength-Slice ist im `FVX-WILD-001` Carrier nach dem Fix save-/log-/reload-stabil.

### `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary

- Aktive Feature-ID: `FVX-WILD-004`
- Carrier-Writer: `FVX-WILD-001` Standard/Fallback-Wild
- Normalisierte Settings: `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `wildPokemonTypeMod=KEEP_PRIMARY`, `similarStrengthEncounters=false`, `useTimeBasedEncounters=true`, `splitByEncounterType=false`, `catchEmAll=false`, `wildHeldItems=false`, `minimumCatchRateLevel=0`, `wildLevelModifier=0`, `palettes=UNCHANGED`, `typeEffectiveness=UNCHANGED`, `updateMoves=false`
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich: `true`
- `writeReloadWildPokemonMismatches=0`
- `filterViolations=0`
- `Bad Egg=false`
- `<unknown>=false`
- `exceptionClass/stacktrace=none`
- `nullSlotsBefore=0`
- `nullSlotsAfter=0`

Ergebnis: Der Keep-Primary-Type-Slice ist im `FVX-WILD-001` Carrier nach dem Fix save-/log-/reload-stabil.

## Bewertung

Der 070-Wild-Blocker ist fuer die zwei getesteten Wild-Slices entblockt:

- `FVX-WILD-011` und `FVX-WILD-004` erreichen Save, Log, Output und Reload.
- Der Wild-Write-/Reload-Vergleich meldet `writeReloadWildPokemonMismatches=0`.
- Der 070-`IllegalStateException`-Abbruch trat in den Fix-Smokes nicht mehr auf.
- `Bad Egg` und `<unknown>` sind in beiden Slice-Logs `false`.

Die lokalen Smokes beobachteten in diesem Teststand keine Nullslots vor oder nach der Randomization. Der Codefix bleibt trotzdem auf den in 074 identifizierten defensiven Null-/unaufloesbar-Scope begrenzt und verhindert, dass solche Slots als valide Mapping-/InfoMap-Anker in die Filterlogik laufen.

## Grenzen

075 ist kein Nachweis fuer:

- TypeChart / TypeEffectiveness.
- MoveData Write / Update Moves.
- Palette Randomization.
- Items / Field Items / Shops / Pickup.
- Encounter Held Items.
- custom Day/Night-Wild.
- Catch Em All / Minimum Catch Rate.
- Wild Level Modifier / Balance Low Level Encounters.
- Text / Menu / Graphics.
- Trainer-, Evolution-, Starter-, Static- oder Trade-Suboptionen.

Die restlichen 070-Blocker bleiben separat:

- `FVX-FOE-009` Trainer Type Diversity / Type Themes.
- `FVX-TRAIT-018` Evolutions Similar Strength.
- `FVX-TRAIT-019` Evolutions Same Typing.

## Checks

UPR-FVX:

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `./gradlew clean :random:jar`

Workspace:

- `git status --short`
- `git submodule status --recursive`
- `git diff --stat`
- `git diff --submodule`
- `git diff --check`

## Naechster Schritt

PRs fuer UPR-FVX und Workspace reviewen und mergen. Danach die restlichen 070-Blocker getrennt fortsetzen, beginnend mit `FVX-FOE-009` Trainer Type Diversity oder den Evolution-Slices `FVX-TRAIT-018/019`, ohne offene Writer zu vermischen.
