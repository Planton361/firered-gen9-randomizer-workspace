# 052 - CFRU/DPE Abilities + Hidden Ability Scope-and-Write Fix Diagnostics

## Ziel

Ability1/2 und Hidden Ability fuer den getesteten CFRU/DPE Gen9-BPRE-Stand stabil lesen, schreiben und reloaden.

Scope:

- CFRU/DPE-gated Ability-Scope bis `0xFE` / `ABILITIES_COUNT=255`.
- `abilitiesPerSpecies()==3` im CFRU/DPE-Scope.
- Hidden Ability bei BaseStats-Offset `0x1A` lesen/schreiben/preserven.
- Ability-Name-/Logger-Fallbacks fuer unbekannte IDs sichtbar halten.
- Placeholder-/Null-/all-zero-Species defensiv aus Ability-Randomization ausschliessen.

Out of scope:

- Encounter Held Items bei `0x0C/0x0E`.
- Move-Data-Write.
- Tutor-, Egg-Move-, Palette/Graphics-, Type-Chart- oder Text/Menu-Ausweitung.

## Code-Stand

- Workspace-Branch: `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
- UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
- UPR-FVX Commit: `639c7e61`
- Ausgangsbasis: Base Stats + Types Scope-and-Write-Fix aus Diagnose 051.

## Implementierter Fix

### `Gen3RomHandler`

- Liest Ability1 weiter aus BaseStats-Offset `0x16`.
- Liest Ability2 weiter aus BaseStats-Offset `0x17`.
- Liest Hidden Ability CFRU/DPE-gegatet aus BaseStats-Offset `0x1A`.
- Schreibt Hidden Ability CFRU/DPE-gegatet wieder nach Offset `0x1A`.
- Meldet im CFRU/DPE-Scope `abilitiesPerSpecies()==3`.
- Meldet im CFRU/DPE-Scope `highestAbilityIndex()==0xFE`.
- Laedt Ability-Namen bis `0xFE`; fehlende oder nicht lesbare Eintraege bleiben `null` und fallen beim Logging sichtbar auf `ability #<id>` zurueck.

### `Gen3Constants`

- Hidden-Ability-Offset `0x1A` als `bsHiddenAbilityOffset` dokumentiert.
- CFRU/DPE-Ability-Grenze `0xFE` als eigener Wert ergänzt.

### `SpeciesAbilityRandomizer`

- Skippt `null` Species und Species mit `BST == 0`.
- Skippt Species, deren Ability1/2/Hidden-Ability alle `0` sind.
- Skippt Species mit Ability-IDs ausserhalb `0..highestAbilityIndex()`.
- Nutzt weiterhin keine Ability `0` als Random-Pick.
- Laesst Vanilla-/Jambo-/andere Gen3-Pfade unveraendert.

## Diagnoseumgebung

Lokaler Diagnoseharness unter ignored `05_builds/**`; ROM-, Output- und Log-Artefakte wurden nicht committed und private Pfade nicht dokumentiert.

Alle Laeufe verwenden denselben getesteten CFRU/DPE Gen9-BPRE-Stand.

Konstante Basiswerte:

| Feld | Wert |
|---|---:|
| `species.total` | `423` |
| hoechste Species im geladenen FVX-Scope | `1065:Minior` |
| `abilitiesPerSpecies` | `3` |
| `highestAbilityIndex` | `254` / `0xFE` |
| `gBaseStats` Pointer-Ort | `0x080001BC` |
| `gBaseStats` Ziel-ROM-Offset | `0x19FC4CC` |
| `skippedPlaceholderNullSpecies` | `2` |
| `skippedAllZeroAbilitySpecies` | `2` |
| `skippedInvalidAbilityIds` | `0` |

## Lauf 1 - Ability1/2-only

Optionen: direkter Ability1/2-Write im Diagnoseharness.

| Feld | Wert |
|---|---:|
| Ability1/2 entries before | `421` |
| Ability1/2 entries after | `421` |
| Ability1/2 entries reload | `421` |
| Hidden Ability entries before | `391` |
| Hidden Ability entries after | `391` |
| Hidden Ability entries reload | `391` |
| hoechste Ability-ID before | `232` |
| hoechste Ability-ID after | `233` |
| hoechste Ability-ID reload | `233` |
| `writeReloadAbilityMismatches` | `0` |
| `writeReloadHiddenAbilityMismatches` | `0` |
| `unknownAbilityFallbackCount` | `563` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Bad Egg im Log | `false` |
| `<unknown>` im Log | `false` |
| unknown ability marker | `false` |
| Stacktrace | keiner |

Bewertung: Ability1/2-Write und Reload sind stabil; Hidden Ability bleibt unveraendert.

## Lauf 2 - Hidden Ability-only

Optionen: direkter Hidden-Ability-Write im Diagnoseharness.

| Feld | Wert |
|---|---:|
| Ability1/2 entries before | `421` |
| Ability1/2 entries after | `421` |
| Ability1/2 entries reload | `421` |
| Hidden Ability entries before | `391` |
| Hidden Ability entries after | `421` |
| Hidden Ability entries reload | `421` |
| hoechste Ability-ID before | `232` |
| hoechste Ability-ID after | `232` |
| hoechste Ability-ID reload | `232` |
| `writeReloadAbilityMismatches` | `0` |
| `writeReloadHiddenAbilityMismatches` | `0` |
| `unknownAbilityFallbackCount` | `567` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Bad Egg im Log | `false` |
| `<unknown>` im Log | `false` |
| unknown ability marker | `false` |
| Stacktrace | keiner |

Bewertung: Hidden Ability wird am CFRU/DPE-Offset `0x1A` geschrieben und reloadet ohne Mismatches; Ability1/2 bleibt stabil.

## Lauf 3 - Ability1/2 + Hidden Ability

Optionen: GameRandomizer Ability-Randomization.

| Feld | Wert |
|---|---:|
| Ability1/2 entries before | `421` |
| Ability1/2 entries after | `421` |
| Ability1/2 entries reload | `421` |
| Hidden Ability entries before | `391` |
| Hidden Ability entries after | `420` |
| Hidden Ability entries reload | `420` |
| hoechste Ability-ID before | `232` |
| hoechste Ability-ID after | `254` |
| hoechste Ability-ID reload | `254` |
| `writeReloadAbilityMismatches` | `0` |
| `writeReloadHiddenAbilityMismatches` | `0` |
| `unknownAbilityFallbackCount` | `557` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Bad Egg im Log | `true` |
| `<unknown>` im Log | `false` |
| unknown ability marker | `true` |
| Stacktrace | keiner |

Bewertung: Normaler Ability-Randomizer-Flow nutzt den erweiterten Pool bis `0xFE` und reloadet Ability1/2 sowie Hidden Ability ohne Mismatches. Unknown-Ability-Fallbacks sind sichtbar, aber nicht fatal.

## Lauf 4 - Base Stats + Types + Abilities Smoke

Optionen: GameRandomizer Base Stats + Types + Abilities.

| Feld | Wert |
|---|---:|
| Ability1/2 entries before | `421` |
| Ability1/2 entries after | `421` |
| Ability1/2 entries reload | `421` |
| Hidden Ability entries before | `391` |
| Hidden Ability entries after | `420` |
| Hidden Ability entries reload | `420` |
| hoechste Ability-ID before | `232` |
| hoechste Ability-ID after | `254` |
| hoechste Ability-ID reload | `254` |
| `writeReloadAbilityMismatches` | `0` |
| `writeReloadHiddenAbilityMismatches` | `0` |
| `unknownAbilityFallbackCount` | `582` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Bad Egg im Log | `true` |
| `<unknown>` im Log | `false` |
| unknown ability marker | `true` |
| Stacktrace | keiner |

Bewertung: Der Ability-Fix bleibt zusammen mit dem bereits bestaetigten BaseStats-/Types-Fix stabil.

## Gesamtbewertung P1-Support

Ability1/2 und Hidden Ability sind im getesteten CFRU/DPE Gen9-BPRE-Scope P1-supported.

Kriterien:

- CFRU/DPE-Scope meldet `abilitiesPerSpecies=3`.
- Ability-Pool reicht bis `highestAbilityIndex=254`.
- Ability1/2 und Hidden Ability schreiben/reloaden mit `0` Mismatches.
- Placeholder-/Null-/all-zero-Species werden defensiv behandelt.
- Fehlende Ability-Namen crashen nicht, sondern werden als `ability #<id>` sichtbar.
- Base Stats + Types + Abilities bleibt im kombinierten Smoke stabil.

## Risiken und Annahmen

- `Bad Egg` im Log stammt weiterhin aus bekannten Placeholder-/Sonder-Species-Markern im Trait-/Species-Logging und blockiert Save/Reload nicht; keine Type-/Species-Log-Hygiene in diesem Branch.
- Ability-Namen fuer viele moderne IDs fehlen im FVX-Namensbestand; Fallbacks sind sichtbar, aber fachlich keine vollstaendige Text-/Description-Unterstuetzung.
- Encounter Held Items bleiben trotz gleicher `gBaseStats`-Tabelle out of scope.
- Type-Chart-, Move-Data-, Tutor-, Egg-, Palette/Graphics- und Text/Menu-Pfade wurden nicht erweitert.

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
