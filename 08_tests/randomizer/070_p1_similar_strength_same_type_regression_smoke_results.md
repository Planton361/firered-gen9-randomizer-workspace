# 070 - P1 Similar Strength / Same Type Regression-Smoke Results

Datum: 2026-05-14

Branch: `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke`

## Ziel

Dieses Protokoll dokumentiert die lokal einzeln ausgefuehrten Regression-Smokes aus Plan 069 fuer BST-/Type-basierte Poolfilter:

- `FVX-WILD-011` Wild Similar Strength
- `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary
- Trainer Similar Strength als Suboption unter `FVX-FOE-001`
- `FVX-FOE-009` Trainer Type Diversity / Type Themes
- `FVX-TRAIT-018` Evolutions Similar Strength
- `FVX-TRAIT-019` Evolutions Same Typing

Die Ergebnisse sind sanitisiert. ROM-, Log-, Output-ROM-, Build-Pfade, ROM-Namen, Hashes, private Pfade und Loginhalte werden nicht dokumentiert. Lokale Artefakte bleiben ignored.

## Grenzen

Aktiviert wurden nur der jeweilige Carrier-Writer und die geplante Suboption. Ausgeschlossen blieben:

- TypeChart / TypeEffectiveness
- MoveData Write / Update Moves
- Field Items / Shops / Pickup
- Encounter Held Items
- Palette Randomization / Follow Types / Follow Evolutions / Shiny Palette
- Graphics / Sprites / Repointing
- Text / Menu / Description
- Trainer/Wild Level Modifier
- Evolution-Methoden-Writer
- Starter Held Items
- Race Mode / Intro Mon
- Better Movesets
- Trainer Additional Pokemon
- Trainer Battle Style
- Trainer Names/Class Names
- Catch Em All
- Minimum Catch Rate
- Wild held items
- custom Day/Night-Wild

## Ergebnisuebersicht

| Slice | Feature-ID | Carrier | Ergebnis |
|---|---|---|---|
| Wild Similar Strength | `FVX-WILD-011` | `FVX-WILD-001` Standard/Fallback Wild Species Writer | blockiert: Save fehlgeschlagen |
| Wild Type Restrictions / Type Themes / Keep Primary | `FVX-WILD-004` | `FVX-WILD-001` Standard/Fallback Wild Species Writer | blockiert: Save fehlgeschlagen |
| Trainer Similar Strength | `FVX-FOE-001` Suboption | Trainer-Species-Writer | bestaetigt im Carrier-Smoke |
| Trainer Type Diversity / Type Themes | `FVX-FOE-009` | `FVX-FOE-001` Trainer Pokemon | blockiert: Save fehlgeschlagen |
| Evolutions Similar Strength | `FVX-TRAIT-018` | `FVX-TRAIT-016` Evolution-Species-Writer | blockiert: Reload-Mismatches und `Bad Egg`-Marker |
| Evolutions Same Typing | `FVX-TRAIT-019` | `FVX-TRAIT-016` Evolution-Species-Writer | blockiert: Save fehlgeschlagen |

## Slice-Ergebnisse

### `FVX-WILD-011` Wild Similar Strength

- Aktive Settings: `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `similarStrengthEncounters=true`
- Carrier-Writer: `FVX-WILD-001` Standard/Fallback Wild Species Writer
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- Reload erfolgreich: `false`
- `writeReloadWildPokemonMismatches=-1` wegen fehlendem Output
- `filterViolations=not separately asserted`
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `IllegalStateException`

Stop-Regel: Save fehlgeschlagen. Kein P1-Support-Nachweis fuer `FVX-WILD-011` aus diesem Smoke.

### `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary

- Aktive Settings: `randomizeWildPokemon=true`, `wildPokemonZoneMod=GAME`, `wildPokemonTypeMod=KEEP_PRIMARY`
- Carrier-Writer: `FVX-WILD-001` Standard/Fallback Wild Species Writer
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- Reload erfolgreich: `false`
- `writeReloadWildPokemonMismatches=-1` wegen fehlendem Output
- `filterViolations=0` bis zum Abbruchzustand; nicht als voller Erfolg zu werten
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `IllegalStateException`

Stop-Regel: Save fehlgeschlagen. Kein P1-Support-Nachweis fuer `FVX-WILD-004` aus diesem Smoke.

### Trainer Similar Strength unter `FVX-FOE-001`

- Aktive Settings: `trainersMod=RANDOM`, `trainersUsePokemonOfSimilarStrength=true`
- Carrier-Writer: Trainer-Species-Writer
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich: `true`
- `writeReloadTrainerPokemonMismatches=0`
- `filterViolations=not separately asserted`
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `none`

Ergebnis: Trainer Similar Strength ist im `FVX-FOE-001` Trainer-Species-Carrier-Smoke save-/log-/reload-stabil. Da keine eigene Feature-ID existiert, bleibt der Nachweis konservativ als Suboption unter `FVX-FOE-001` dokumentiert.

### `FVX-FOE-009` Trainer Type Diversity / Type Themes

- Aktive Settings: `trainersMod=RANDOM`, `diverseTypesForBossTrainers=true`, `diverseTypesForImportantTrainers=true`, `diverseTypesForRegularTrainers=true`
- Carrier-Writer: `FVX-FOE-001` Trainer Pokemon
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- Reload erfolgreich: `false`
- `writeReloadTrainerPokemonMismatches=-1` wegen fehlendem Output
- `filterViolations=112` bis zum Abbruchzustand; wegen Save-Fehler nicht als vollstaendige Endzustandsmetrik zu werten
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `NullPointerException`

Stop-Regel: Save fehlgeschlagen. `FVX-FOE-009` bleibt offen/blockiert und darf nicht als P1-supported hochgestuft werden.

### `FVX-TRAIT-018` Evolutions Similar Strength

- Aktive Settings: `evolutionsMod=RANDOM`, `evosSimilarStrength=true`
- Carrier-Writer: `FVX-TRAIT-016` Evolution-Species-Writer
- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich: `true`
- `writeReloadEvolutionMismatches=24`
- `filterViolations=not separately asserted`
- `Bad Egg=true`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `none`

Stop-Regel: Reload-Mismatch-Zaehler ist nicht `0`. Der `Bad Egg`-Marker wird hier nicht als unkritischer 055-Logmarker freigegeben, weil gleichzeitig Reload-Mismatches vorliegen. Kein P1-Support-Nachweis fuer `FVX-TRAIT-018` aus diesem Smoke.

### `FVX-TRAIT-019` Evolutions Same Typing

- Aktive Settings: `evolutionsMod=RANDOM`, `evosSameTyping=true`
- Carrier-Writer: `FVX-TRAIT-016` Evolution-Species-Writer
- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `logNonEmpty=false`
- Reload erfolgreich: `false`
- `writeReloadEvolutionMismatches=-1` wegen fehlendem Output
- `filterViolations=0` bis zum Abbruchzustand; nicht als voller Erfolg zu werten
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`
- Exception-Klasse: `NullPointerException`

Stop-Regel: Save fehlgeschlagen. Kein P1-Support-Nachweis fuer `FVX-TRAIT-019` aus diesem Smoke.

## Bewertung

Nur Trainer Similar Strength unter `FVX-FOE-001` erfuellt in diesem Lauf die spaeteren Erfolgskriterien aus 069 vollstaendig.

Die Wild- und Evolution-Slices sowie `FVX-FOE-009` zeigen eigenstaendige Folgeprobleme in bereits belegten Carrier-Scopes. Sie bleiben getrennt zu behandeln und duerfen nicht mit TypeChart, MoveData, Palette, Items, Graphics, Text/Menu oder Level-/Methoden-Writern vermischt werden.

## Naechster Schritt

Empfohlen ist ein read-only Diagnoseplan fuer die blockierten 070-Slices, bevor Fixes umgesetzt werden:

- Wild Similar Strength und Wild Type Restrictions gemeinsam gegen Standard/Fallback-Wild-Nullslot-/Placeholder-Scope pruefen.
- `FVX-FOE-009` getrennt gegen Trainer-Type-Diversity und Null-/Type-Placeholder-Scope pruefen.
- `FVX-TRAIT-018` und `FVX-TRAIT-019` getrennt gegen Evolution-Reload-Mismatches, `Bad Egg`-Marker und Null-Evolution-Scope pruefen.

Keine Codeaenderung und kein Fix wurden in diesem Dokumentationsblock vorgenommen.
