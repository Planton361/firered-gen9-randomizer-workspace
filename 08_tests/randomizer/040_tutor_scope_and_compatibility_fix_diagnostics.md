# 040 - Tutor Scope and Compatibility Fix Diagnostics fuer CFRU/DPE Gen9-BPRE

Ziel dieses Fixblocks war, Tutor moves-only und Tutor compatibility-only fuer CFRU/DPE Gen9-BPRE minimal zu entblocken. Keine Special-Tutor-Randomization, keine Egg-Move-, Learnset-Write-, Move-Data-Write- oder Tutor-Text-Rewrite-Ausweitung wurde vorgenommen.

## Stand

- Workspace-Branch: `compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility`
- UPR-FVX-Branch: `compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility`
- UPR-FVX-Commit: `4ce93754de390e9177efd2541c02edba0afbb0c4`
- Basis: Workspace PR #76 gemerged; Diagnose 039 hat das Tutor-/Special-Tutor-Modell dokumentiert.
- Test-ROM: lokaler CFRU/DPE Gen9-BPRE-Teststand unter `05_builds/**`, nicht committed.
- Seed: `274269061345323`

## Implementierter Scope

Geaendert wurden nur:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `random/src/main/java/com/uprfvx/random/randomizers/TMTutorMoveRandomizer.java`

Der neue Pfad ist auf sicher erkannte CFRU/DPE-Gen9-BPRE-Hacks begrenzt (`useCfruDpeGen9SpeciesCount`):

- `gMoveTutorMoves` wird ueber Pointer-Location `0x8120BE4` gelesen.
- Zielpointer im Teststand: `0x09A596EA`, ROM-Offset `0x1A596EA`.
- `gMoveTutorMoves` wird als `u16[152]` behandelt.
- `setMoveTutorMoves()` schreibt fuer CFRU/DPE nur diese 152 `u16`-Slots.
- Tutor-Text-Rewrites werden fuer den CFRU/DPE-Pfad nicht ausgeweitet.
- `gTutorLearnsets` wird ueber Pointer-Location `0x8120C30` gelesen.
- Zielpointer im Teststand: `0x09605CD0`, ROM-Offset `0x1605CD0`.
- Aktiver Compatibility-Stride ist `19` Bytes pro Species, also `152` Bits.
- FVX bildet die Flags intern als `boolean[153]` ab, Index `0` bleibt Dummy.
- Placeholder-/Null-Species bleiben im Randomizer-Compatibility-Pfad defensiv uebersprungen.
- Special Tutors bleiben unveraendert und out of scope.
- Tutor-Move-Randomization nutzt fuer hohe Move-IDs dieselbe defensive Ban-Array-Pruefung wie TM/HM.

## Gemeinsame Befunde

| Feld | Wert |
|---|---|
| `moves.total` | `992` |
| Hoechster Move | `PsychicNoise`, ID `991` |
| `tutorMoveCount` | `152` |
| Letzter Tutor-Move | `MOVE_TERABLAST`, ID `966` |
| Hoechste Tutor-Move-ID im Ausgangsbestand | `969` |
| `gMoveTutorMoves` Pointer-Location | `0x8120BE4` |
| `gMoveTutorMoves` Zielpointer / Offset | `0x09A596EA` / `0x1A596EA` |
| `gTutorLearnsets` Pointer-Location | `0x8120C30` |
| `gTutorLearnsets` Zielpointer / Offset | `0x09605CD0` / `0x1605CD0` |
| Nachgewiesener Compatibility-Stride | `19` Bytes pro Species |
| Compatibility flag length | `153` |
| Compatibility species entries | `423` |
| Skipped Placeholder-/Null-Species | `10` |
| Invalid Tutor moves before/after | `0` / `0` |
| Special Tutors | unveraendert / out of scope |
| Bad Egg im Log | `false` |
| `<unknown>` im Log | `false` |
| Unknown-Move-Marker im Log | `false` |

Hinweis: Die Compatibility-Species-Anzahl bleibt im aktuellen FVX-Scope bei `423`; dieser Branch erweitert nicht den globalen Species-Kompatibilitaetsumfang.

## Lauf 1: Tutor moves-only

Optionen:

- `moveTutorMoves=RANDOM`
- `moveTutorCompatibility=UNCHANGED`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `7443` |
| before/after/reload Tutor-Move entries | `152` / `152` / `152` |
| before/after/reload Tutor-Compatibility entries | `423` / `423` / `423` |
| `writeReloadTutorMoveMismatches` | `0` |
| `writeReloadTutorCompatibilityMismatches` | `0` |

Bewertung: Tutor-Move-Randomization schreibt 152 normale Tutor-Slots stabil und laesst Special Tutors unangetastet.

## Lauf 2: Tutor compatibility-only

Optionen:

- `moveTutorMoves=UNCHANGED`
- `moveTutorCompatibility=RANDOM_PREFER_TYPE`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `256275` |
| before/after/reload Tutor-Move entries | `152` / `152` / `152` |
| before/after/reload Tutor-Compatibility entries | `423` / `423` / `423` |
| `writeReloadTutorMoveMismatches` | `0` |
| `writeReloadTutorCompatibilityMismatches` | `0` |

Bewertung: Compatibility-only ist mit `19`-Byte-/`152`-Bit-Stride save-/log-/reload-stabil.

## Lauf 3: Tutor moves + Tutor compatibility

Optionen:

- `moveTutorMoves=RANDOM`
- `moveTutorCompatibility=RANDOM_PREFER_TYPE`

Ergebnis:

| Feld | Wert |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `logBytes` | `271223` |
| before/after/reload Tutor-Move entries | `152` / `152` / `152` |
| before/after/reload Tutor-Compatibility entries | `423` / `423` / `423` |
| `writeReloadTutorMoveMismatches` | `0` |
| `writeReloadTutorCompatibilityMismatches` | `0` |

Bewertung: Kombinierter Tutor-Move- und Tutor-Compatibility-Lauf ist save-/log-/reload-stabil.

## Gesamtbewertung P1-Support

CFRU/DPE Tutor-only ist fuer den getesteten Gen9-BPRE-Stand im normalen 152-Slot-Tutor-Scope P1-supported:

- FVX erkennt fuer den gegateten CFRU/DPE-Pfad 152 normale Tutor-Moves.
- Die aktive `gMoveTutorMoves`-Tabelle wird ueber den CFRU/DPE-Pointer gelesen und geschrieben.
- `gTutorLearnsets` nutzt im getesteten ROM 19 Bytes pro Species und laedt/schreibt reload-stabil.
- Alle drei Diagnose-Laeufe erzeugen Output-ROM und nichtleeren Log.
- Es gibt keine invaliden Tutor-Move-IDs, keine Unknown-Move-Marker, kein `Bad Egg` und kein `<unknown>` im Log.

Nicht abgedeckt und bewusst out of scope:

- Special-Tutor-Randomization.
- Tutor-Text-/Menu-Rewrites.
- Egg-Moves.
- Learnset-Write.
- Move-Data-Write.
- Erweiterung des Compatibility-Species-Scopes ueber den aktuell von FVX geladenen Bereich hinaus.

## Risiken und Folgefragen

- Die 19-Byte-Stride-Aussage ist fuer den getesteten ROM-Stand durch Write/Reload belegt. Andere CFRU/DPE-Buildvarianten mit `u32[5]`-/20-Byte-Layout muessen separat gegatet werden.
- Tutor-UI-/Textdaten fuer 152 Slots werden nicht angepasst. Der ROM-Write/Reload des aktiven Tutor-Tabellenmodells ist trotzdem stabil.
- Special Tutors bleiben fachlich separat und werden nicht in normale Tutor-Slots gemischt.

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
