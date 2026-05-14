# 090 - CFRU/DPE Move Names fixed-length Reload-Smoke Retry

Datum: 2026-05-14

Workspace-Branch: `test/upr-fvx-cfru-dpe-move-names-fixed-length-reload-smoke-retry`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieser Block wiederholt den engen Name-only Reload-Smoke fuer `FVX-MOVE-005` Randomize Move Names nur dann, wenn ein lokal freigegebener CFRU/DPE Gen9-BPRE-Kandidat beim Load eindeutig den getesteten Move-Scope meldet:

- `moves.total=992`
- hoechster Move `991:PsychicNoise`

Der Scope bleibt gegenueber Diagnose 089 unveraendert:

- nur fixed-length `MoveNames`
- keine Move Descriptions
- kein Pointer-/Repointing
- keine Text/Menu-Umsetzung
- keine MoveData-Byte-Writer-Aenderung

## Sanitisiertes Preflight-Ergebnis

Das lokale Preflight pruefte freigegebene private/ignored Kandidaten, ohne private Pfade, ROM-Namen, Hashes, Logauszuege oder Output-ROMs zu dokumentieren.

```text
candidateFilesChecked=94
candidatePreflightSuccessful=false
candidateMovesTotal=not available
candidateHighestMove=not available
```

Ergebnis:

- Kein lokal verfuegbarer Kandidat erfuellte gleichzeitig `moves.total=992` und `991:PsychicNoise`.
- Der fachliche Name-only Reload-Smoke wurde deshalb nicht ausgefuehrt.
- Es wurden keine fachlichen Save-/Log-/Output-/Reload-Kriterien bewertet.

## Nicht ausgefuehrte Smoke-Kriterien

Die folgenden Kriterien bleiben in diesem Retry bewusst nicht fachlich bewertet:

- `saveSuccessful`
- `logSuccessful`
- `outputRomExists`
- `logNonEmpty`
- Reload erfolgreich
- `moveNameReloadMismatches`
- `moveNameLengthViolations`
- `moveNameTerminatorPaddingMismatches`
- `moveNameByteMismatches`
- `moveNameEncodingFallbacks`
- `moveNameTruncations`
- `moveDescriptionPointerMismatches`
- `moveDescriptionChanged`
- `moveDataByteMismatches`
- `exceptionClass`
- `stacktrace`

## Description-/Pointer-Abgrenzung

In diesem blockierten Retry wurden keine Move Descriptions, Description-Pointer, Text/Menu-Daten oder Repointing-Pfade geaendert oder getestet.

Die Abgrenzung aus Diagnose 088 bleibt gueltig:

- `FVX-MOVE-005` ist kein MoveData-Byte-Writer im `BattleMove`-Scope `+0..+11`.
- Der direkte Name-Pfad ist der bestehende Gen3 fixed-length `MoveNames`-Writer.
- Move Descriptions / Text/Menu / Repointing bleiben ein separater Scope und werden aus diesem Name-only-Smoke nicht abgeleitet.

## Feature-Status

- `FVX-MOVE-005` bleibt `Write modelliert`.
- Keine Hochstufung auf `GUI-kompatibel`, weil kein Kandidat mit `moves.total=992` und `991:PsychicNoise` fuer den fachlichen Smoke verfuegbar war.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.

## Sicherheitsnotizen

- Keine privaten Pfade, ROM-Namen, Hashes, Logauszuege oder Output-ROMs wurden dokumentiert.
- Lokale Preflight-/Harness-Artefakte blieben ignored unter `05_builds/**`.
- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Keine Submodule-Pin-Aenderung.
- Kein Build.
- Kein Randomizer-Smoke nach blockiertem Preflight.
- Keine Original-Upstreams kontaktiert.

## Ergebnis

Der Retry ist blockiert. Ein fachlicher Name-only fixed-length Reload-Smoke fuer `FVX-MOVE-005` kann erst bewertet werden, wenn ein lokal freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und hoechstem Move `991:PsychicNoise` eindeutig verfuegbar ist.
