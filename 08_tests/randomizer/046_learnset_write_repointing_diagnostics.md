# 046 - CFRU/DPE Learnset Write Repointing Diagnostics

## Scope

Arbeitsbranch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`

Ziel: Full CFRU/DPE `setMovesLearnt()`-Write mit Repointing fuer den getesteten CFRU/DPE Gen9-BPRE-Stand validieren. Der Fix schreibt neue Level-Up-Learnset-Blobs in die diagnostisch nachgewiesene freie `0xFF`-Region und aktualisiert die bestehende `gLevelUpLearnsets`-Pointertable pro interner Species-ID.

Nicht im Scope: Move-Data-Write, Tutor-Text/Menu-Rewrites, Special Tutors, Egg-Move-Ausweitung, Palette/Graphics oder andere Text/Menu-Pfade.

Lokale Diagnoseartefakte blieben ignored unter `05_builds/randomizer-smoke/046_learnset_write_repointing/`. Private ROM-Pfade, ROM-Namen und Hashes werden nicht dokumentiert.

## UPR-FVX-Stand

- UPR-FVX Branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`
- UPR-FVX Commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`
- Basis: CFRU/DPE Learnset bounded Writer aus PR #23

## Implementierter Fix

- CFRU/DPE-Pfad bleibt eng ueber den bestehenden Gen9-BPRE-Gate begrenzt.
- `gLevelUpLearnsets` Pointer-Ort `0x03EA7C` muss auf die erwartete aktive Pointertable bei ROM-Offset `0x25D7B4` zeigen.
- Die bestehende Pointertable wird beibehalten und fuer interne Species-IDs bis `1439` aktualisiert.
- Neue Learnset-Blobs werden aus den geplanten Movesets pro interner `SpeciesSet`-ID erzeugt.
- Entry-Format bleibt `u16 move + u8 level`; Sentinel bleibt `00 00 FF`.
- Move-IDs werden gegen die geladenen `moves.total=992` validiert.
- Byte-identische neue Learnset-Blobs werden dedupliziert; Shared-Pointer-Gruppen aus dem alten ROM werden nicht blind erhalten.
- Die validierte FreeSpace-Region `0x1219A48-0x1600000` wird vor dem Write auf freie Bytes geprueft.
- Pointertable-Eintraege werden als little-endian GBA-Pointer auf die neuen Blob-Adressen geschrieben.
- Placeholder-/Null-Species werden defensiv uebersprungen.
- Vanilla-, Jambo- und andere Gen3-Pfade bleiben unveraendert.

## FreeSpace-Nachweis

| Feld | Wert |
|---|---:|
| ROM-Laenge | `33554432` Bytes / 32 MiB |
| `gLevelUpLearnsets` Pointer-Ort | `0x03EA7C` |
| Aktive Pointertable ROM-Offset | `0x25D7B4` |
| Pointertable-Kapazitaet | `0x1680` Bytes |
| Validierte FreeSpace-Region | `0x1219A48-0x1600000` |
| FreeSpace-Laenge | `4089272` Bytes |
| Worst-case Bedarf aus Modell | `220320` Bytes |
| Planned Blob Bytes im Diagnoseharness | `17418` Bytes |
| Written Blob Bytes nach Dedupe/Alignment | `11547` Bytes |
| Verwendetes Byteintervall | `[0x1219A48, 0x121C763)` |
| Actual Bedarf reservierbar | `true` |
| Worst-case Bedarf reservierbar | `true` |

Hinweis: Der generische FVX-FreeSpace-Allocator kann vor der nachgewiesenen CFRU/DPE-Zielregion freie Bytes finden. Der Fix schreibt deshalb nur nach erfolgreicher Validierung in die explizit nachgewiesene Region und bricht ab, wenn diese Region nicht frei oder zu klein ist.

## Diagnoseablauf

Der lokale Diagnoseharness hat die geladenen CFRU/DPE-Learnsets modifiziert, indem pro nicht vollem Learnset ein hoher gueltiger Move (`991:PsychicNoise`) als zusaetzlicher Level-Up-Eintrag geplant wurde. Danach wurden `setMovesLearnt()`, Save, Reload und ein SpeciesSet-basierter Reload-Vergleich ausgefuehrt.

## Diagnose-Ergebnis

| Metrik | Wert |
|---|---:|
| `moves.total` | `992` |
| Hoechster geladener Move | `991:PsychicNoise` |
| Species total | `1440` |
| Hoechste Species before/after/reload | `1439 / 1439 / 1439` |
| Hoechste Move-ID before/after/reload | `865 / 991 / 991` |
| Planned added Learnsets | `1413` |
| Planned replaced Learnsets | `0` |
| Planned skipped full Learnsets | `0` |
| Unique Blob Count | `416` |
| Deduped Blob Count | `997` |
| Pointertable Entries Updated | `1413` |
| Skipped Placeholder-/Null-Species | `1` |
| Skipped Invalid Moves | `0` |
| Old Shared Pointer Groups Count | `9` |
| Broken Shared Groups Count | `0` |
| Before Species Entries | `1413` |
| After Species Entries | `1413` |
| Reload Species Entries | `1413` |
| Before Learnset Entries | `2980` |
| After Learnset Entries | `4393` |
| Reload Learnset Entries | `4393` |
| Before Empty Learnsets | `977` |
| After Empty Learnsets | `0` |
| Reload Empty Learnsets | `0` |
| Invalid Learnset Moves before/after/reload | `0 / 0 / 0` |
| Write/Reload verglichene Species | `1413` |
| `writeReloadLearnsetMismatches` | `0` |
| `saveSuccessful` | `true` |
| `reloadLoadSuccessful` | `true` |
| `outputRomExists` | `true` |
| Output-ROM-Groesse | `33554432` Bytes |
| `logSuccessful` | `true` |
| `logNonEmpty` | `true` |
| Bad Egg im Log | `false` |
| `<unknown>` Species im Log | `false` |
| Unknown-Move-Marker im Log | `false` |
| Stacktrace / Fehlerpfad | keiner |

Writer-Diagnosezeile:

```text
[CFRU-DPE-LEARNSET-REPOINT] pointerTable=0x25d7b4 freeSpace=0x1219a48-0x121c763 plannedBlobBytes=17418 writtenBlobBytes=11547 uniqueBlobCount=416 dedupedBlobCount=997 pointertableEntriesUpdated=1413 skippedPlaceholderSpecies=1 skippedInvalidMoves=0 oldSharedPointerGroups=9 brokenSharedPointerGroups=0
```

## Gesamtbewertung P1-Support

Full CFRU/DPE Learnset-Write mit Repointing ist fuer den getesteten direkten `setMovesLearnt()`-Scope P1-supported.

Die Diagnose bestaetigt:

- freier Zielbereich ist gross genug fuer actual und worst-case Bedarf,
- neue Blobs werden geschrieben und dedupliziert,
- Pointertable wird pro interner Species-ID aktualisiert,
- Reload liest die repointeten Learnsets stabil zurueck,
- `writeReloadLearnsetMismatches=0`,
- keine Bad-Egg-, `<unknown>`- oder Unknown-Move-Marker im Log.

Die normale GUI-Option fuer komplette Pokemon-Moveset-/Learnset-Randomization sollte weiterhin separat als Kombinationslauf geprueft werden, weil sie zusaetzliche Randomizer-Logik und Settings-Kopplungen aktivieren kann. Der Kernblocker `setMovesLearnt()` ist mit diesem Fix entblockt.

## Risiken / Annahmen

- Der Fix ist absichtlich an die validierte Pointertable `0x25D7B4` und FreeSpace-Region `0x1219A48-0x1600000` gebunden; andere CFRU/DPE-Builds muessen denselben Nachweis erneut liefern.
- Keine ROM-Erweiterung wird angenommen.
- Dedupe ist nur byte-identisch; semantisch gleiche, aber anders kodierte Learnsets werden nicht zusammengelegt.
- Alte Shared-Pointer-Gruppen werden durch neue deduplizierte Blobs ersetzt, nicht konserviert.
- Der Diagnoseharness validiert den direkten Learnset-Write-Pfad; breitere GUI-Kombinationen bleiben Folge-Scope.
- Placeholder-/Null-Species werden nicht als echte Zielspecies beschrieben.

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
