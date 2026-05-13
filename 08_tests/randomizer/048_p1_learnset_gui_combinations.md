# 048 - CFRU/DPE Learnset GUI Combination Diagnostics

## Scope

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-learnset-gui-combinations`

Ziel: normale GUI-/Settings-nahe Pokemon-Movesets-/Learnsets-Laeufe fuer den getesteten CFRU/DPE Gen9-BPRE-Stand diagnostizieren. Fokus ist, ob der neue `setMovesLearnt()`-Repointing-Pfad aus UPR-FVX PR #24 auch im `GameRandomizer`-Flow stabil bleibt.

Keine Codeaenderung, kein Fix. `02_external/**` wurde nur read-only genutzt. Lokale ROM-, Output-ROM- und Log-Artefakte blieben ignored unter `05_builds/randomizer-smoke/048_p1_learnset_gui_combinations/`; private Pfade, ROM-Namen und Hashes werden nicht dokumentiert.

## Ausgangsstand

- UPR-FVX Commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`
- ROM-Laenge: `33554432` Bytes / 32 MiB
- `moves.total=992`
- Hoechster geladener Move: `991:PsychicNoise`
- `gLevelUpLearnsets` Pointer-Ort: `0x03EA7C`
- Aktive Pointertable ROM-Offset: `0x25D7B4`
- Validierte FreeSpace-Region: `0x1219A48-0x1600000`
- FreeSpace-Laenge: `4089272` Bytes

## Diagnosemethode

Der temporäre lokale Harness nutzt `GameRandomizer` mit `Settings`, nicht den direkten `setMovesLearnt()`-Writer aus Diagnose 046. Dadurch werden die normalen Randomizer-Reihenfolgen abgebildet:

- `maybeRandomizeMovesets()` ruft `randomizeMovesLearnt()` und danach `randomizeEggMoves()` auf.
- TM/HM- und Tutor-Kombinationen laufen durch die normalen `TMTutorMoveRandomizer`- und `TMHMTutorCompatibilityRandomizer`-Pfade.
- Trainer-Movesets laufen durch `TrainerMovesetRandomizer`.
- Save/Reload-Vergleiche nutzen die gespeicherte Output-ROM und vergleichen Learnsets, Trainer-Movesets, TM/HM, Tutor und Egg Moves, soweit der Lauf bis Save kommt.

## Gemeinsame Repointing-Werte erfolgreicher Learnset-Writes

Alle Laeufe, die `randomizeMovesLearnt()` erreichen, erzeugen denselben Learnset-Repointing-Plan:

| Metrik | Wert |
|---|---:|
| `plannedBlobBytes` | `30099` |
| `writtenBlobBytes` | `31771` |
| `uniqueBlobCount` | `1413` |
| `dedupedBlobCount` | `0` |
| `pointertableEntriesUpdated` | `1413` |
| `skippedPlaceholderSpecies` | `1` |
| `skippedInvalidMoves` | `0` |
| `oldSharedPointerGroups` | `9` |
| `brokenSharedPointerGroups` | `9` |
| Before Learnset Entries | `2980` |
| After Learnset Entries | `8620` |
| Highest Species before/after | `1439 / 1439` |
| Highest Move before/after | `865 / 991` |

Die GUI-nahe Randomisierung erzeugt mehr Learnset-Daten als Diagnose 046, bleibt aber deutlich innerhalb der validierten FreeSpace-Region.

## Lauf 1 - Pokemon Movesets/Learnsets-only

| Feld | Wert |
|---|---|
| Settings | `movesets=RANDOM_PREFER_SAME_TYPE`, `startGuaranteed=true`, `guaranteedCount=4`, `reorderDamaging=false` |
| Seed | `274269061345323` |
| Save | `true` |
| Log | `false` |
| Output-ROM | `true` |
| Log nicht leer | `true` |
| Reload erfolgreich | `true` |
| Reload Learnset Entries | `8620` |
| Highest Species reload | `1439` |
| Highest Move reload | `991` |
| `writeReloadLearnsetMismatches` | `0` |
| Trainer-Moveset-Mismatches | `0` |
| TM/HM-Mismatches | `0` |
| Tutor-Mismatches | `0` |
| Egg-Move-Mismatches | `0` |
| Bad Egg / `<unknown>` / Unknown-Move-Marker | `false / false / false` |
| Fehlerpfad | Log-Fehler: `NullPointerException: ... List.iterator() ... data is null` |

Bewertung: Save/Reload des Repointing-Pfads ist stabil. Der normale Logger scheitert separat, nachdem die Output-ROM geschrieben wurde.

## Lauf 2 - Pokemon Movesets/Learnsets + Trainer Movesets

| Feld | Wert |
|---|---|
| Settings | Lauf 1 plus `betterBossTrainerMovesets=true`, `betterImportantTrainerMovesets=true`, `betterRegularTrainerMovesets=true` |
| Seed | `274269061345324` |
| Save | `false` |
| Log | `true` |
| Output-ROM | `false` |
| Log nicht leer | `false` |
| Reload erfolgreich | `false` |
| `writeReloadLearnsetMismatches` | nicht pruefbar |
| Fehlerpfad | `NullPointerException: Cannot invoke "java.util.List.stream()" because the return value of "java.util.Map.get(Object)" is null` |

Bewertung: Blockiert vor Save im Trainer-Moveset-Auswahlpfad. Das ist ein separater Kombinationsblocker nach erfolgreichem Learnset-Repointing-Plan.

## Lauf 3 - Pokemon Movesets/Learnsets + TM/HM 128-slot

| Feld | Wert |
|---|---|
| Settings | Lauf 1 plus `tms=RANDOM`, `tmhmCompat=RANDOM_PREFER_TYPE`, `tmSanity=false`, `fullHMCompat=true` |
| Seed | `274269061345325` |
| Save | `true` |
| Log | `false` |
| Output-ROM | `true` |
| Log nicht leer | `true` |
| Reload erfolgreich | `true` |
| Reload Learnset Entries | `8620` |
| Highest Species reload | `1439` |
| Highest Move reload | `991` |
| `writeReloadLearnsetMismatches` | `0` |
| TM/HM-Mismatches | `0` |
| Egg-Move-Mismatches | `0` |
| Bad Egg / `<unknown>` / Unknown-Move-Marker | `false / false / false` |
| Fehlerpfad | Log-Fehler: `NullPointerException: ... List.iterator() ... data is null` |

Bewertung: Repointing plus TM/HM-128-Slot ohne Level-Up-Move-Sanity speichert und reloadet stabil. Logger bleibt separat fehlerhaft.

## Lauf 4 - Pokemon Movesets/Learnsets + Tutor 152-slot

| Feld | Wert |
|---|---|
| Settings | Lauf 1 plus `tutors=RANDOM`, `tutorCompat=RANDOM_PREFER_TYPE`, `tutorSanity=false` |
| Seed | `274269061345326` |
| Save | `true` |
| Log | `false` |
| Output-ROM | `true` |
| Log nicht leer | `true` |
| Reload erfolgreich | `true` |
| Reload Learnset Entries | `8620` |
| Highest Species reload | `1439` |
| Highest Move reload | `991` |
| `writeReloadLearnsetMismatches` | `0` |
| Tutor-Mismatches | `0` |
| Egg-Move-Mismatches | `0` |
| Bad Egg / `<unknown>` / Unknown-Move-Marker | `false / false / false` |
| Fehlerpfad | Log-Fehler: `NullPointerException: ... List.iterator() ... data is null` |

Bewertung: Repointing plus normaler 152-Slot-Tutor-Scope ohne Tutor-Level-Up-Sanity speichert und reloadet stabil. Logger bleibt separat fehlerhaft.

## Lauf 5 - Pokemon Movesets/Learnsets + Egg Moves direct

| Feld | Wert |
|---|---|
| Settings | Lauf 1; Egg Moves sind im normalen `maybeRandomizeMovesets()`-Flow gekoppelt und nicht separat abschaltbar |
| Seed | `274269061345327` |
| Save | `true` |
| Log | `false` |
| Output-ROM | `true` |
| Log nicht leer | `true` |
| Reload erfolgreich | `true` |
| Reload Learnset Entries | `8620` |
| Highest Species reload | `1439` |
| Highest Move reload | `991` |
| `writeReloadLearnsetMismatches` | `0` |
| Egg-Move-Mismatches | `0` |
| Bad Egg / `<unknown>` / Unknown-Move-Marker | `false / false / false` |
| Fehlerpfad | Log-Fehler: `NullPointerException: ... List.iterator() ... data is null` |

Bewertung: Der gekoppelte Egg-Move-Teil im Movesets-Flow reloadet stabil. Logger bleibt separat fehlerhaft.

## Zusaetzliche optionale Blocker

| Lauf | Ergebnis | Fehlerpfad | Bewertung |
|---|---|---|---|
| Movesets + Reorder damaging moves | `saveSuccessful=false`, kein Output, kein Reload | `RomIOException: CFRU/DPE learnset blob allocation 0x1219a48-0x1221663 is not fully free in the validated free-space region` | `orderDamagingMovesByDamage()` ruft `setMovesLearnt()` ein zweites Mal auf derselben ROM-Instanz auf; der statische Repoint-Start ist durch den ersten Write bereits belegt. |
| Movesets + TM/HM Level-Up-Move-Sanity | `saveSuccessful=false`, kein Output, kein Reload | `NullPointerException: Cannot invoke "java.util.List.iterator()" because "moveset" is null` | Sanity-Pfad trifft auf Species-/Learnset-Key-Luecken nach internem Species-ID-Modell. |
| Movesets + Tutor Level-Up-Move-Sanity | `saveSuccessful=false`, kein Output, kein Reload | `NullPointerException: Cannot invoke "java.util.List.iterator()" because "moveset" is null` | Gleiches Risiko wie TM/HM-Sanity, aber im Tutor-Compatibility-Sanity-Pfad. |

## Gesamtbewertung P1-Support

Der neue Repointing-Pfad bleibt im normalen `GameRandomizer`-Flow fuer den Kernscope stabil, solange `setMovesLearnt()` nur einmal pro ROM-Instanz ausgefuehrt wird:

- Movesets/Learnsets-only: Save/Reload stabil, `writeReloadLearnsetMismatches=0`.
- Movesets/Learnsets + TM/HM 128-slot ohne Level-Up-Sanity: Save/Reload stabil, TM/HM-Mismatches `0`.
- Movesets/Learnsets + Tutor 152-slot ohne Level-Up-Sanity: Save/Reload stabil, Tutor-Mismatches `0`.
- Movesets/Learnsets + gekoppelte Egg Moves: Save/Reload stabil, Egg-Move-Mismatches `0`.

Trotzdem ist Pokemon Movesets/Learnsets im vollstaendigen GUI-Scope noch nicht voll P1-supported, weil:

- der Logger in erfolgreichen GameRandomizer-Laeufen mit `NullPointerException` abbricht,
- Trainer-Movesets-Kombinationen blockieren,
- Reorder-Damaging-Moves blockiert durch zweiten Learnset-Repoint-Write,
- TM/HM- und Tutor-Level-Up-Move-Sanity blockieren durch fehlende Moveset-Map-Eintraege.

## Empfohlener Folgepfad

1. `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`
   - `setMovesLearnt()` fuer CFRU/DPE idempotent oder multi-write-sicher machen, damit Reorder-Damaging nach erstem Repoint nicht an belegter FreeSpace-Region scheitert.
   - Moveset-Map-Zugriffe in Trainer-Movesets, TM/HM-Sanity und Tutor-Sanity gegen interne Species-ID-Keys absichern.
   - Logger-Nullpfad fuer erfolgreiche Movesets-Runs isolieren.

2. Danach erneuter Diagnosebranch fuer `049_p1_learnset_gui_flow_safety_fix_diagnostics`.

## Risiken / Annahmen

- Der Harness bildet GUI-nahe `Settings` und `GameRandomizer`-Reihenfolge ab, startet aber keine Swing-GUI.
- Log-Fehler werden als separater Blocker gewertet, weil Save/Reload bereits erfolgreich sein kann.
- Die validierte FreeSpace-Region reicht fuer den ersten Learnset-Repointing-Write aus; das Problem ist Wiederverwendung derselben statischen Startadresse auf derselben ROM-Instanz.
- Keine privaten Pfade oder ROM-Hashes wurden dokumentiert.

## Checks

UPR-FVX:

```text
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Workspace:

```text
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```
