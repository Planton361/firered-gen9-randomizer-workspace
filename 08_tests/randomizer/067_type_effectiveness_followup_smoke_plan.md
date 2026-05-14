# 067 - CFRU/DPE TypeEffectiveness Follow-up Smoke Plan

## Ziel

Dieses read-only Protokoll plant einzelne TypeEffectiveness-Folgesmokes nach dem gemergten TypeChart Preserve Effectiveness Fix aus Diagnose 066.

Scope:

- Nur Plan und Einordnung auf Basis vorhandener Dokumentation.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte gelesen oder dokumentiert.
- Keine Original-Upstream-Kontakte und keine Original-Upstream-PRs.

## Ausgangspunkt

Diagnose 066 bestaetigt den engen TypeEffectiveness-only Random-Smoke nach dem UPR-FVX-Fix `36707e0190d3d9fa587550dfc5631fcaa9abd6b1`:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `writeReloadTypeChartMismatches=0`
- Fairy wird in der geschriebenen TypeChart als raw `0x17` reloaded
- unsupported/Stellar wird nicht eingefuehrt oder still normalisiert
- Foresight- und Endtable-Terminatoren bleiben erhalten
- `Bad Egg=false`
- `<unknown>=false`
- `stacktrace=none`

Dieser Smoke ist die Referenz fuer den TypeChart-Writer-Fix. Er ersetzt aber nicht die Einzelpruefung weiterer TypeEffectiveness-GUI-Modi.

## Geplante Slices

| Slice | Feature-ID | GUI-Modus | Zweck | Nicht Teil des Slices |
|---|---|---|---|---|
| `FVX-TYPE-001-balanced` | `FVX-TYPE-001` | Balanced | `Random Balanced` separat gegen TypeTable-Write, Fairy-Reload, unsupported/Stellar-Preserve und Terminatoren pruefen. | Keine Species-Type-Randomization, kein MoveData, keine Items, keine Palette. |
| `FVX-TYPE-001-keep-identities` | `FVX-TYPE-001` | Keep Type Identities | TypeTable-Identity-Swaps separat pruefen; kein Nachweis aus dem Random-Smoke ableiten. | Kein Species-Type-Write und keine Type-Pool-/Species-Pool-Aenderung. |
| `FVX-TYPE-001-inverse` | `FVX-TYPE-001` | Inverse | Reine Inversion separat pruefen, ohne Add-Random-Immunities zu vermischen. | Keine Add-Immunities-Suboption im gleichen Basis-Slice. |
| `FVX-TYPE-002-add-random-immunities` | `FVX-TYPE-002` | Add Random Immunities | Eigener Risikopunkt: neue Immunities koennen Nicht-Neutral-Zaehler, Preserve-Triplets und Terminator-/Kapazitaetsgrenzen anders belasten. | Nicht mit Balanced oder Update Type Effectiveness buendeln. |
| `FVX-TYPE-003-update-type-effectiveness` | `FVX-TYPE-003` | Update Type Effectiveness | Updater-Pfad separat pruefen; Gen6-Update-Logik ist kein Ersatz fuer CFRU/DPE-Gen9-TypeChart-Reload. | Kein Random/Balanced/Inverse im selben Slice. |

## Gemeinsame Erfolgskriterien fuer spaetere Laeufe

Jeder spaetere Slice soll mindestens folgende Kriterien dokumentieren:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true` |
| Output | `outputRomExists=true` |
| Log-Inhalt | `logNonEmpty=true` |
| Reload | Reload der geschriebenen TypeChart-Daten erfolgreich |
| Mismatches | `writeReloadTypeChartMismatches=0` |
| Fairy | Fairy reloadet korrekt als raw `0x17` |
| Unsupported/Stellar | Wird nicht eingefuehrt oder still normalisiert |
| Foresight-Terminator | Bleibt erhalten |
| Endtable-Terminator | Bleibt erhalten |
| Log-Hygiene | `Bad Egg=false` |
| Unknown-Marker | `<unknown>=false` |
| Fehler | `stacktrace=none` |

Zusaetzlich sollte jeder Slice die aktiven TypeEffectiveness-Settings eindeutig nennen, damit `FVX-TYPE-001`, `FVX-TYPE-002` und `FVX-TYPE-003` rueckverfolgbar bleiben.

## Grenzen

Diese Folgesmokes bleiben strikt auf TypeEffectiveness / TypeChart begrenzt.

Nicht vermischen mit:

- MoveData oder Move-Type-Bytes.
- Palette-Randomization oder Palette-Follow-Types.
- Items, Field Items, Shops oder Pickup.
- Graphics oder Sprites.
- Text/Menu-Writer.
- Species-Type-Write in `gBaseStats`.

Pokemon-Type-Read/Write aus Diagnose 051 bleibt ein eigener Nachweis. Der TypeChart-Fix aus 066 bleibt ein eigener Writer-Nachweis. Die geplanten Folgesmokes pruefen nur weitere TypeEffectiveness-GUI-Modi.

## Stop-Regeln

Ein spaeterer Ausfuehrungsblock soll stoppen und nicht mehrere Modi zusammenfassen, wenn ein Slice:

- Save, Log, Output oder Reload nicht erfolgreich abschliesst.
- `writeReloadTypeChartMismatches` ungleich `0` meldet.
- Fairy nicht als raw `0x17` reloadet.
- unsupported/Stellar-Triplets einfuehrt, verliert oder still normalisiert.
- Foresight- oder Endtable-Terminatoren veraendert.
- `Bad Egg`, `<unknown>` oder einen Stacktrace im TypeEffectiveness-only-Kontext erzeugt.

## Ergebnis

067 ist nur ein Plan. Es wurden keine neuen Randomizer-Laeufe ausgefuehrt und keine neuen Diagnosewerte erhoben.

Naechster sinnvoller Schritt ist ein spaeterer Test-/Diagnosebranch, der die geplanten Slices einzeln ausfuehrt und sanitisiert dokumentiert, ohne andere offene Writer oder GUI-Bereiche zu vermischen.
