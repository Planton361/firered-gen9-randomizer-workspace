# 049 - CFRU/DPE Learnset GUI Flow Safety Fix Diagnostics

## Kontext

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`

UPR-FVX-Fix: `086d2a9177df7624a0e7ca1876b210a200d7aa98`

Ausgangspunkt war Diagnose 048: der erste CFRU/DPE-Learnset-Repointing-Write war stabil, aber der normale GUI-/Settings-nahe Flow blockierte bei Logger-Nullsafety, Trainer-Movesets, Reorder-Damaging-Zweitwrite sowie TM/HM-/Tutor-Level-Up-Sanity.

Keine privaten ROM-Pfade, ROM-Namen, Hashes, Logs oder Output-ROMs werden dokumentiert. Lokale Diagnoseartefakte blieben ignored unter `05_builds/**`.

## Fixumfang

- Logger: fehlende optionale Settings-/Moveset-Logdaten werden sichtbar als unavailable protokolliert, statt Save/Reload-Erfolge im Log-Schritt scheitern zu lassen.
- Learnset-Repointing: CFRU/DPE-`setMovesLearnt()` sucht bei jedem Write einen freien `0xFF`-Block innerhalb der validierten Region `0x1219A48-0x1600000`; keine ROM-Erweiterung.
- Trainer-Movesets: Moveset-Map-Zugriffe bevorzugen interne `SpeciesSet`-Identitaet und fallen defensiv auf Species-Nummer/Skip zurueck.
- TM/HM Level-Up-Sanity: fehlende Movesets/Compatibility-Eintraege werden gezaehlt und uebersprungen statt per NPE abzubrechen.
- Tutor Level-Up-Sanity: gleiche defensive Strategie wie TM/HM-Sanity.
- Ausdruecklich nicht erweitert: Move-Data-Write, Tutor-Text/Menu, Special Tutors, Egg-Move-Scope, Palette/Graphics, Text/Menu-Pfade.

## Gemeinsame Diagnosewerte

| Feld | Wert |
|---|---:|
| `moves.total` | `992` |
| hoechster Move | `991:PsychicNoise` |
| FreeSpace-Region | `0x1219A48-0x1600000` |
| FreeSpace-Laenge | `4089272` |
| `writeReloadLearnsetMismatches` | `0` in allen Laeufen |
| `saveSuccessful` | `true` in allen Laeufen |
| `logSuccessful` | `true` in allen Laeufen |
| `outputRomExists` | `true` in allen Laeufen |
| `logNonEmpty` | `true` in allen Laeufen |
| `Bad Egg` im Log | `false` in allen Laeufen |
| `<unknown>` im Log | `false` in allen Laeufen |
| Unknown-Move-Marker | `false` in allen Laeufen |
| `loggerUnavailableSections` | `1` in allen Laeufen; Harness-Settings-Metadaten waren unvollstaendig und wurden sichtbar als unavailable geloggt |

## Lauf 1 - Movesets/Learnsets-only

| Feld | Wert |
|---|---|
| Optionen | `movesets=RANDOM_PREFER_SAME_TYPE`, `startGuaranteed=true`, `guaranteedCount=4`, `reorderDamaging=false` |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| `plannedBlobBytes` | `30099` |
| `writtenBlobBytes` | `31771` |
| `uniqueBlobCount` | `1413` |
| `dedupedBlobCount` | `0` |
| `pointertableEntriesUpdated` | `1413` |
| `skippedMissingMovesets` | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | Save, Log, Output und Reload stabil |

## Lauf 2 - Movesets/Learnsets + Trainer Movesets

| Feld | Wert |
|---|---|
| Optionen | Lauf 1 plus `trainerMovesets=true` |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| `plannedBlobBytes` / `writtenBlobBytes` | `30099` / `31771` |
| `pointertableEntriesUpdated` | `1413` |
| `skippedMissingMovesets` | `1` |
| Trainer-Moveset-Mismatches | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | fehlender Moveset-Map-Eintrag wird diagnostiziert und uebersprungen; kein NPE |

## Lauf 3 - Reorder damaging moves

| Feld | Wert |
|---|---|
| Optionen | Lauf 1 plus `reorderDamaging=true` |
| `setMovesLearnt()`-Writes | `2` |
| FreeSpace-Block 1 | `0x1219A48-0x1221663` |
| FreeSpace-Block 2 | `0x1221664-0x122927F` |
| `plannedBlobBytes` je Write | `30099` |
| `writtenBlobBytes` je Write | `31771` |
| `pointertableEntriesUpdated` je Write | `1413` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | zweiter Repointing-Write nutzt neuen freien Block; kein statischer FreeSpace-Konflikt |

## Lauf 4 - Movesets/Learnsets + TM/HM 128-Slot mit Level-Up-Sanity

| Feld | Wert |
|---|---|
| Optionen | Lauf 1 plus `tms=RANDOM`, `tmhmCompat=RANDOM_PREFER_TYPE`, `tmSanity=true`, `fullHMCompat=true` |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| TM/HM-Mismatches | `0` |
| `skippedMissingMovesets` | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | TM/HM-Level-Up-Sanity stabil |

## Lauf 5 - Movesets/Learnsets + Tutor 152-Slot mit Level-Up-Sanity

| Feld | Wert |
|---|---|
| Optionen | Lauf 1 plus `tutors=RANDOM`, `tutorCompat=RANDOM_PREFER_TYPE`, `tutorSanity=true` |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| Tutor-Mismatches | `0` |
| `skippedMissingMovesets` | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | Tutor-Level-Up-Sanity stabil |

## Lauf 6 - Movesets/Learnsets + Egg Moves direct/gekoppelt

| Feld | Wert |
|---|---|
| Optionen | Egg-Move-Daten ueber gekoppelten Movesets-Flow beobachtet |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| Egg-Move-Mismatches | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | gekoppelter Egg-Move-Scope bleibt stabil; keine Egg-Move-Ausweitung in diesem Fix |

## Lauf 7 - Movesets/Learnsets + TM/HM + Tutor Sanity

| Feld | Wert |
|---|---|
| Optionen | Lauf 1 plus TM/HM- und Tutor-Randomization mit Level-Up-Sanity |
| `setMovesLearnt()`-Writes | `1` |
| FreeSpace-Block | `0x1219A48-0x1221663` |
| TM/HM-Mismatches | `0` |
| Tutor-Mismatches | `0` |
| `skippedMissingMovesets` | `0` |
| `writeReloadLearnsetMismatches` | `0` |
| Ergebnis | kombinierter TM/HM-/Tutor-Sanity-Flow stabil |

## Gesamtbewertung P1-Support

Pokemon Movesets/Learnsets sind im getesteten CFRU/DPE Gen9-BPRE-Scope jetzt P1-supported im normalen GameRandomizer-/Settings-nahen Flow.

Die Diagnose bestaetigt:

- Full Learnset-Repointing bleibt nach Save/Reload stabil.
- Wiederholte `setMovesLearnt()`-Writes belegen jeweils freie Blobs innerhalb der validierten Region.
- Trainer-Movesets, TM/HM-Level-Up-Sanity und Tutor-Level-Up-Sanity brechen bei fehlenden Moveset-Map-Eintraegen nicht mehr ab.
- Logger-Nullpfade sind sichtbar markiert und verhindern keinen erfolgreichen Logabschluss.

## Risiken und Grenzen

- `loggerUnavailableSections=1` stammt aus unvollstaendigen Harness-Settings-Metadaten; die Daten werden sichtbar markiert, nicht still verworfen.
- Der Fix reserviert nur innerhalb der validierten FreeSpace-Region `0x1219A48-0x1600000`; andere ROM-Staende muessen diese Region erneut validieren.
- Move-Data-Write, Tutor-Text/Menu, Special Tutors, Egg-Move-Erweiterungen, Palette/Graphics und Text/Menu-Pfade bleiben out of scope.
- Base Stats, Types, Abilities und Hidden Abilities bleiben separate Folgearbeit.

## Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Workspace:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```
