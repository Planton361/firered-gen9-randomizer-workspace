# 078 - Trainer Type Diversity Null-Type Fix Diagnostics

Datum: 2026-05-14

Workspace-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-p1-trainer-type-diversity-nulltype-fix`

UPR-FVX-Fix-Commit: `d89fc64e3b0223b03a65466422847dc7df30d03c`

## Scope

Dieses Protokoll dokumentiert den eng gegateten Fix fuer den 070/076/077-Blocker:

- `FVX-FOE-009` Trainer Type Diversity / Type Themes
- Carrier: `FVX-FOE-001` Trainer Pokemon

Der Fix bleibt auf `TrainerPokemonRandomizer` begrenzt. Er behandelt Species mit `primaryType == null` defensiv im Force-Diverse-Types-/`usedTypes`-Pfad, bevor ein `EnumSet<Type>` einen `null`-Eintrag erhalten kann.

## Nicht im Scope

- Wild
- Evolution
- TypeChart / TypeEffectiveness
- MoveData Write / Update Moves
- Palette
- Items
- Text / Menu
- Graphics / Sprites
- Trainer Level Modifier
- Trainer Additional Pokemon
- Better Movesets
- Trainer Battle Style
- Trainer Names / Class Names

## Fixzusammenfassung

Geaenderte UPR-FVX-Datei:

- `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`

Der Fix:

- erkennt, ob Type-Diversity oder Type-Themes aktiv sind;
- entfernt im erweiterten BPRE-Hack Species ohne nutzbaren Primary Type aus dem Type-Diversity-/Type-Themes-Trainerpool;
- filtert den Force-Diverse-Types-Replacementpfad vor der `usedTypes`-Auswertung auf Species mit `primaryType != null`;
- traegt Secondary Types nur in `usedTypes` ein, wenn der Secondary Type nicht `null` ist;
- laesst bestehende BST-zero-, all-zero-Ability- und Placeholder-/Special-Species-Grenzen unveraendert.

Der Fix leitet keinen TypeChart-Support ab und aendert keine anderen Writer.

## Diagnose

Lokale Diagnoseartefakte blieben ignored. Dieses Protokoll dokumentiert keine ROM-/Log-/Output-ROM-/Build-Pfade, ROM-Namen, Hashes oder privaten Pfade.

### `FVX-FOE-009` Trainer Type Diversity / Type Themes

Aktive Settings:

- `trainersMod=RANDOM`
- `diverseTypesForBossTrainers=true`
- `diverseTypesForImportantTrainers=true`
- `diverseTypesForRegularTrainers=true`

Sanitisierte Ergebnisse:

| Metrik | Ergebnis |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload erfolgreich | `true` |
| `writeReloadTrainerPokemonMismatches` | `0` |
| `filterViolations` | `0` |
| `Bad Egg` | `false` |
| `<unknown>` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

Bewertung:

- Der 070-Blocker `NullPointerException` ist fuer diesen Slice nicht mehr reproduziert.
- `FVX-FOE-009` ist im eng getesteten Trainer-Type-Diversity-Scope stabil.
- Keine Supportaussage fuer Trainer-Level-, Additional-Pokemon-, Better-Movesets-, Battle-Style-, Names/Class-Names- oder andere offene Trainer-Subpfade.

### Trainer Similar Strength Regression

Aktive Settings:

- `trainersMod=RANDOM`
- `trainersUsePokemonOfSimilarStrength=true`

Sanitisierte Ergebnisse:

| Metrik | Ergebnis |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload erfolgreich | `true` |
| `writeReloadTrainerPokemonMismatches` | `0` |
| `filterViolations` | nicht separat asserted |
| `Bad Egg` | `false` |
| `<unknown>` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

Bewertung:

- Trainer Similar Strength unter `FVX-FOE-001` bleibt stabil.
- Der Fix hat den bestehenden Similar-Strength-Pfad nicht regressiert.

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

## Naechste Schritte

- UPR-FVX-PR gegen `Planton361/universal-pokemon-randomizer-fvx` reviewen und mergen.
- Workspace-PR mit Submodule-Pin und Diagnose 078 reviewen und mergen.
- Danach die verbleibenden 070-Evolution-Blocker getrennt fortsetzen:
  - `FVX-TRAIT-018` Evolutions Similar Strength
  - `FVX-TRAIT-019` Evolutions Same Typing
