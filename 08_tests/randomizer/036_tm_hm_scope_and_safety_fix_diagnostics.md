# 036 - TM/HM Scope and Safety Fix Diagnostics

## Kontext

- Branch: `compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety`
- UPR-FVX-Basis: `c71fd75e67f5a839560bbf5de7c6f17317a64bd1`
- UPR-FVX-Fix: `32e43ac03a5762542773213a13be4e0389f1deae`
- Seed: `274269061345323`
- Lokale Artefakte: `05_builds/randomizer-smoke/036_tm_hm_scope_and_safety_fix/` (ignored, nicht committed)

## Fix-Scope

- `TMTutorMoveRandomizer.randomizeTMMoves()` behandelt CFRU/DPE-Gen9-BPRE-Move-IDs oberhalb der vorhandenen FVX-Sicherheitslisten defensiv und waehlt sie fuer TM-Randomization nicht aus.
- `TMHMTutorCompatibilityRandomizer` ueberspringt im erweiterten BPRE-Hack-Scope Placeholder-Species ohne Primaertyp.
- Compatibility-Flags und Move-Lookups sind gegen fehlende oder ausserhalb liegende Indizes abgesichert.
- Gate: enger Gen3/CFRU-DPE-Hack-Pfad ueber `Gen3RomHandler.hasExtendedBpreHackSpeciesPool()`.
- Nicht umgesetzt: CFRU/DPE-128-Slot-TM/HM-Modell, Tutor, Egg Moves, Learnset-Write, Move-Data-Write.

## Gemeinsame Befunde

| Feld | Wert |
|---|---:|
| `moves.total` | 992 |
| hoechster Move | `PsychicNoise` |
| hoechste Move-ID | 991 |
| `tmCount` | 50 |
| `hmCount` | 8 |
| `compat.flagLength` | 59 |
| Compatibility-Species-Eintraege | 423 |
| Null-Species | 0 |
| Species mit `null`-Primaertyp | 10 |
| Species mit `null`-Sekundaertyp | 225 |
| TM/HM-Eintraege | 58 |

FVX erkennt weiterhin nur das klassische `50+8`-Modell. Der aktive CFRU/DPE-128-Slot-Ort ist in diesem Branch nicht sicher lokalisiert und wurde nicht implementiert.

## Lauf 1: TM moves + TM/HM compatibility

| Feld | Wert |
|---|---:|
| Optionen | `TMsMod=RANDOM`, `TMsHMsCompatibilityMod=RANDOM_PREFER_TYPE` |
| `saveSuccessful` | true |
| `logSuccessful` | true |
| `outputRomExists` | true |
| `logNonEmpty` | true |
| `logBytes` | 302461 |
| `before.tmhmEntries` | 58 |
| `after.tmhmEntries` | 58 |
| `reload.tmhmEntries` | 58 |
| `before.compatTrueFlags` | 7749 |
| `after.compatTrueFlags` | 9469 |
| `reload.compatTrueFlags` | 9469 |
| `after.invalidTmHmMoves` | 0 |
| `reload.invalidTmHmMoves` | 0 |
| `writeReloadTmHmMismatches` | 0 |
| `writeReloadCompatibilityMismatches` | 0 |
| `Bad Egg` im Log | false |
| `<unknown>` im Log | false |
| Unknown-Move-Marker im Log | false |

## Lauf 2: TM/HM compatibility-only

| Feld | Wert |
|---|---:|
| Optionen | `TMsMod=UNCHANGED`, `TMsHMsCompatibilityMod=RANDOM_PREFER_TYPE` |
| `saveSuccessful` | true |
| `logSuccessful` | true |
| `outputRomExists` | true |
| `logNonEmpty` | true |
| `logBytes` | 286461 |
| `before.tmhmEntries` | 58 |
| `after.tmhmEntries` | 58 |
| `reload.tmhmEntries` | 58 |
| `before.compatTrueFlags` | 7749 |
| `after.compatTrueFlags` | 9180 |
| `reload.compatTrueFlags` | 9180 |
| `after.invalidTmHmMoves` | 0 |
| `reload.invalidTmHmMoves` | 0 |
| `writeReloadTmHmMismatches` | 0 |
| `writeReloadCompatibilityMismatches` | 0 |
| `Bad Egg` im Log | false |
| `<unknown>` im Log | false |
| Unknown-Move-Marker im Log | false |

## Lauf 3: TM moves-only

| Feld | Wert |
|---|---:|
| Optionen | `TMsMod=RANDOM`, `TMsHMsCompatibilityMod=UNCHANGED` |
| `saveSuccessful` | true |
| `logSuccessful` | true |
| `outputRomExists` | true |
| `logNonEmpty` | true |
| `logBytes` | 4216 |
| `before.tmhmEntries` | 58 |
| `after.tmhmEntries` | 58 |
| `reload.tmhmEntries` | 58 |
| `before.compatTrueFlags` | 7749 |
| `after.compatTrueFlags` | 7749 |
| `reload.compatTrueFlags` | 7749 |
| `after.invalidTmHmMoves` | 0 |
| `reload.invalidTmHmMoves` | 0 |
| `writeReloadTmHmMismatches` | 0 |
| `writeReloadCompatibilityMismatches` | 0 |
| `Bad Egg` im Log | false |
| `<unknown>` im Log | false |
| Unknown-Move-Marker im Log | false |

## Bewertung P1-Support

TM/HM-only ist im aktuell von FVX erkannten klassischen Scope `50 TMs + 8 HMs` P1-supported:

- TM moves + Compatibility speichert und reloadet ohne Mismatch.
- Compatibility-only speichert und reloadet ohne Mismatch.
- TM moves-only speichert und reloadet ohne Mismatch.
- Keine invaliden TM/HM-Move-IDs, kein `Bad Egg`, kein `<unknown>` und kein Unknown-Move-Marker im Log.

Nicht als supported bewertet ist ein CFRU/DPE-128-Slot-TM/HM-Modell. Der getestete Fix entblockt bewusst nur den vorhandenen FVX-`50+8`-Pfad.

## Risiken / offene Punkte

- Gen8/9-Moves oberhalb der FVX-Sicherheitslisten werden in TM-Move-Randomization fuer CFRU/DPE defensiv ausgeschlossen, nicht voll modelliert.
- Das echte CFRU/DPE-128-Slot-TM/HM-Modell bleibt separat zu lokalisieren und mit Write/Reload zu beweisen.
- Tutor-, Egg-Move-, Learnset-Write- und Move-Data-Write-Pfade wurden nicht erweitert.
- Placeholder-Species ohne Primaertyp bleiben im Compatibility-Datensatz vorhanden, werden im erweiterten BPRE-Hack-Scope aber nicht randomisiert.

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
