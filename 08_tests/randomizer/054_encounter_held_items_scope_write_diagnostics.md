# 054 - CFRU/DPE Encounter Held Items Scope-and-Write Fix Diagnostics

## Ziel

CFRU/DPE Encounter Held Items fuer den getesteten Gen9-BPRE-Stand entblocken. Der Fix erweitert den CFRU/DPE-gegateten Item-Scope, sichert moderne Bad-/Banned-Item-Filter ab und haelt `gBaseStats` `item1`/`item2` bei `0x0C`/`0x0E` read/write/reload-stabil.

Nicht im Scope: Field Items, Shops, Pickup, Move-Data-Write, Tutor, Egg Moves, Palette/Graphics, Type-Chart und Text/Menu.

## Implementierter Fix

- UPR-FVX Commit: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`
- Branch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`
- CFRU/DPE-Gate: vorhandener sicherer Gen9-BPRE-Scope.

### Item-Scope

- Klassischer FireRed-`ItemCount=374` wird fuer CFRU/DPE nicht mehr als harte Ladegrenze verwendet.
- Der Reader prueft den erweiterten DPE-Scope bis `798`; wenn die obere DPE-Region nicht plausibel lesbar ist, faellt er konservativ auf den CFRU-nahen Scope bis `778` zurueck.
- Ergebnis im getesteten Lauf: `item.count=778`, hoechster geladener Eintrag `1778:Free Space 3`.
- Fehlende/implausible Namen werden sichtbar als `item #<id>` fallbacked und nicht als Random-Pick zugelassen.
- Bestehende moderne Held-Item-IDs in `gBaseStats` werden bei Bedarf als nicht erlaubte Fallback-Items angelegt, damit Preserve/Reload nicht zu `0` kollabiert.

### Bad-/Banned-Item-Filter

Der CFRU/DPE-Scope bannt fuer Encounter-Held-Item-Randomization konservativ:

- Key-/System-nahe klassische Ban-Liste
- TMs/HMs
- Mail
- Balls
- Free-/Placeholder-/Shiny-Space-Items
- Booster Energy
- Tera Orb
- Portable PC
- Mega-/Z-/Plate-/Mask-/Form-/Utility-Item-Bereich im modellierten DPE-Sonderblock
- Items mit Fallback- oder implausiblem Namen

### Encounter Held Items

- `gBaseStats` Pointer-Ort: `0x080001BC`
- Zielpointer im Diagnoseinput: ROM-Offset `0x19FC4CC`
- Entry-Size: `0x1C`
- `item1`: Offset `0x0C`
- `item2`: Offset `0x0E`
- Random-Picks kommen nur aus dem sicheren erlaubten Item-Pool.
- Placeholder-/Null-/BST-zero-Species werden defensiv uebersprungen.

## Diagnosekontext

- Lokaler Diagnoseinput: ignored 32-MiB-Ausgabestand aus dem vorherigen Ability/BaseStats/Types-Scope.
- Keine privaten Pfade, ROM-Namen, ROM-Hashes, Logs oder Output-ROMs werden dokumentiert oder committed.
- Lokale Diagnoseartefakte blieben unter `05_builds/**` ignored.

## Diagnose-Ergebnisse

### 1. Encounter Held Items-only

| Metrik | Wert |
|---|---:|
| `item.count` | `778` |
| hoechste geladene Item-ID | `1778:Free Space 3` |
| Itemname-Fallback-Zaehler | `0` |
| Bad-/Banned-Item count | `293` |
| banned item violations | `0` |
| `gBaseStats` Pointer-Ort | `0x080001BC` |
| `gBaseStats` Zieloffset | `0x19FC4CC` |
| `itemData` Zieloffset | `0x114D81C` |
| `item1` / `item2` | `0x0C` / `0x0E` |
| Species total / hoechste Species | `423` / `1065:Minior` |
| Encounter-Held-Item entries before/after/reload | `193` / `113` / `113` |
| hoechste Encounter-Held-Item-ID before/after/reload | `1117` / `1742` / `1742` |
| modern item preservation count | `0` |
| skipped Placeholder-/Null-Species | `0` |
| invalid/missing item IDs | `0` |
| `writeReloadEncounterHeldItemMismatches` | `0` |
| `saveSuccessful` / `logSuccessful` | `true` / `true` |
| `outputRomExists` / `logNonEmpty` | `true` / `true` |
| Bad Egg / `<unknown>` / unknown item marker | `true` / `false` / `false` |
| Stacktrace | `none` |

### 2. Encounter Held Items + Base Stats

| Metrik | Wert |
|---|---:|
| `item.count` | `778` |
| hoechste geladene Item-ID | `1778:Free Space 3` |
| Itemname-Fallback-Zaehler | `0` |
| Bad-/Banned-Item count | `293` |
| banned item violations | `0` |
| Encounter-Held-Item entries before/after/reload | `193` / `117` / `117` |
| hoechste Encounter-Held-Item-ID before/after/reload | `1117` / `1739` / `1739` |
| invalid/missing item IDs | `0` |
| `writeReloadEncounterHeldItemMismatches` | `0` |
| `saveSuccessful` / `logSuccessful` | `true` / `true` |
| `outputRomExists` / `logNonEmpty` | `true` / `true` |
| Bad Egg / `<unknown>` / unknown item marker | `true` / `false` / `false` |
| Stacktrace | `none` |

### 3. Encounter Held Items + Abilities

| Metrik | Wert |
|---|---:|
| `item.count` | `778` |
| hoechste geladene Item-ID | `1778:Free Space 3` |
| Itemname-Fallback-Zaehler | `0` |
| Bad-/Banned-Item count | `293` |
| banned item violations | `0` |
| Encounter-Held-Item entries before/after/reload | `193` / `128` / `128` |
| hoechste Encounter-Held-Item-ID before/after/reload | `1117` / `1741` / `1741` |
| invalid/missing item IDs | `0` |
| `writeReloadEncounterHeldItemMismatches` | `0` |
| `saveSuccessful` / `logSuccessful` | `true` / `true` |
| `outputRomExists` / `logNonEmpty` | `true` / `true` |
| Bad Egg / `<unknown>` / unknown item marker | `true` / `false` / `false` |
| Stacktrace | `none` |

### 4. Encounter Held Items + Types

| Metrik | Wert |
|---|---:|
| `item.count` | `778` |
| hoechste geladene Item-ID | `1778:Free Space 3` |
| Itemname-Fallback-Zaehler | `0` |
| Bad-/Banned-Item count | `293` |
| banned item violations | `0` |
| Encounter-Held-Item entries before/after/reload | `193` / `114` / `114` |
| hoechste Encounter-Held-Item-ID before/after/reload | `1117` / `1732` / `1732` |
| invalid/missing item IDs | `0` |
| `writeReloadEncounterHeldItemMismatches` | `0` |
| `saveSuccessful` / `logSuccessful` | `true` / `true` |
| `outputRomExists` / `logNonEmpty` | `true` / `true` |
| Bad Egg / `<unknown>` / unknown item marker | `true` / `false` / `false` |
| Stacktrace | `none` |

## Gesamtbewertung P1-Support

Encounter Held Items sind im getesteten CFRU/DPE Gen9-BPRE-Scope P1-supported:

- Pflichtlaeufe speichern, loggen und erzeugen Output-ROMs.
- `gBaseStats` `item1`/`item2` reloaden ohne Mismatches.
- Der sichere Random-Pick-Pool verletzt keine Bad-/Banned-Item-Regel.
- Moderne bestehende Held-Item-IDs werden nicht mehr durch fehlende Itemliste zu `null` und beim Save zu `0`.
- Base Stats, Abilities und Types bleiben in Kombination stabil.

## Risiken und Annahmen

- Der getestete ROM-Stand liefert keine plausibel lesbare DPE-Oberregion `779..798`; der Fix begrenzt daher auf `778` und preservt hoehere vorhandene IDs nur als Fallback, falls sie auftreten.
- Bad Egg bleibt im Log sichtbar. Das ist ein bestehendes Placeholder-/Sonder-Species-Logrisiko und kein Encounter-Held-Item-Write/Reload-Fehler.
- Field Items, Shops, Pickup und allgemeine Item-Randomization sind nicht durch diesen Fix abgedeckt.
- Items mit Fallback-Namen werden bewusst nicht neu als Random-Pick verwendet.

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

## Naechster sinnvoller Schritt

Nach Merge der UPR-FVX- und Workspace-PRs kann der naechste Analysebranch einen der verbleibenden Matrixbereiche angehen:

- Move-Data-Write-Modell
- Field Items/Shops/Pickup-Item-Modell
- Palette/Graphics-Randomization-Modell
- Type-Chart-Modell
- Placeholder-/Bad-Egg-Log-Hygiene
