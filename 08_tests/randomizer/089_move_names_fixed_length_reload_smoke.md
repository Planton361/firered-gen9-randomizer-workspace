# 089 - CFRU/DPE Move Names fixed-length Reload-Smoke

Datum: 2026-05-14

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieser Arbeitsblock sollte einen engen, sanitisierten Name-only Reload-Smoke fuer `FVX-MOVE-005` Randomize Move Names ausfuehren.

Geplanter Scope:

- nur Move Names,
- fixed-length `MoveNames`-Tabelle,
- `MoveNameLength` / sichtbare Laengenbegrenzung,
- Terminator/Padding,
- Reload der geschriebenen Move-Namen,
- `moves.total=992`,
- hoechster Move `991:PsychicNoise`.

Nicht Teil des Scopes waren Move Descriptions, Pointer-/Repointing-Arbeit, Text/Menu-Implementierung, MoveData-Byte-Writer-Aenderungen, TypeChart, TypeEffectiveness, Species-Type-Write, TM/HM, Tutor, Egg, Learnsets, Palette, Items, Trainer, Wild, Evolutions oder Graphics.

## Methode

Es wurde ein lokaler, nicht committeter Harness unter ignored `05_builds/**` erstellt.

Der Harness ist darauf ausgelegt:

- `Randomize Move Names` als einzige MoveData-nahe Option zu aktivieren,
- `GameRandomizer.Results` direkt auszuwerten,
- Output-ROM und Log nur lokal/ignored abzulegen,
- nach Reload Move-Namen gegen die nach dem Randomizer-Lauf erwarteten Namen zu vergleichen,
- fixed-length Name-Bytes, Terminator/Padding und Description-Pointer getrennt zu pruefen,
- optional MoveData-Bytes `+0..+11` gegen versehentliche Aenderungen zu pruefen.

Private Pfade, ROM-Namen, Hashes, Logpfade und Output-ROM-Pfade wurden nicht dokumentiert.

## Ergebnis

Der fachliche Smoke konnte in diesem Arbeitsblock nicht ausgewertet werden.

Die lokale Kandidatensuche fand keinen freigegebenen lokalen ROM-Kandidaten, der mit dem gepinnten UPR-FVX-Stand als getesteter CFRU/DPE Gen9-BPRE-Stand erkannt wurde:

- erwartetes Kriterium: `moves.total=992`
- erwartetes Kriterium: hoechster Move `991:PsychicNoise`

Ein automatisch gefundener erster Kandidat war kein CFRU/DPE-Gen9-Stand und wurde verworfen. Anschliessend wurde stumm ueber lokale `.gba`-Kandidaten gesucht, aber kein Kandidat erfuellte die 992-Move-/PsychicNoise-Kriterien.

## Smoke-Ergebnisse

| Kriterium | Ergebnis |
|---|---|
| `saveSuccessful` | nicht ausgewertet |
| `logSuccessful` | nicht ausgewertet |
| `outputRomExists` | nicht ausgewertet |
| `logNonEmpty` | nicht ausgewertet |
| Reload erfolgreich | nicht ausgewertet |
| `moves.total` | kein lokaler Kandidat mit `992` gefunden |
| hoechster Move | kein lokaler Kandidat mit `991:PsychicNoise` gefunden |
| `moveNameReloadMismatches` | nicht ausgewertet |
| `moveNameLengthViolations` | nicht ausgewertet |
| `moveNameTerminatorPaddingMismatches` | nicht ausgewertet |
| `exceptionClass` | nicht ausgewertet |
| `stacktrace` | nicht ausgewertet |

## Reload- und Mismatch-Zaehler

Nicht fachlich ausgewertet:

- `moveNamesChanged`
- `moveNamesUnchanged`
- `moveNameReloadMismatches`
- `moveNameByteMismatches`
- `moveNameEncodingFallbacks`
- `moveNameTruncations`
- `moveDescriptionPointerMismatches`
- `moveDataByteMismatches`

## Name-Length-/Terminator-/Padding-Ergebnis

Nicht fachlich ausgewertet, weil kein lokaler CFRU/DPE-Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` verfuegbar war.

Die Pruefkriterien bleiben fuer den naechsten Versuch:

- `moveNameLengthViolations=0`
- `moveNameTruncations=0`
- `moveNameTerminatorPaddingMismatches=0`
- `moveNameByteMismatches=0`

## Description-/Pointer-Abgrenzung

Keine Move Description, Pointer- oder Repointing-Arbeit wurde umgesetzt.

Der lokale Harness wuerde fuer einen spaeteren erfolgreichen Kandidaten `moveDescriptionPointerMismatches=0` beziehungsweise `moveDescriptionChanged=false` erwarten. In diesem blockierten Lauf wurden diese Werte nicht fachlich ausgewertet.

## Feature-Status

`FVX-MOVE-005` wird nicht hochgestuft.

Status bleibt:

- `FVX-MOVE-001` Randomize Move Power: `GUI-kompatibel`
- `FVX-MOVE-002` Randomize Move Accuracy: `GUI-kompatibel`
- `FVX-MOVE-003` Randomize Move PP: `GUI-kompatibel`
- `FVX-MOVE-004` Randomize Move Types: `GUI-kompatibel`
- `FVX-MOVE-005` Randomize Move Names: `Write modelliert`
- `FVX-MOVE-006` Update Moves to Generation: `GUI-kompatibel`

## Naechster Versuch

Der naechste Versuch sollte denselben Branch-Scope wiederholen, sobald ein freigegebener lokaler CFRU/DPE Gen9-BPRE-ROM-Kandidat fuer den Smoke eindeutig verfuegbar ist.

Der Scope bleibt unveraendert:

- Name-only fixed-length `MoveNames`,
- keine Move Descriptions,
- keine Pointer-/Repointing- oder Text/Menu-Umsetzung,
- keine MoveData-Byte-Writer-Aenderung.
