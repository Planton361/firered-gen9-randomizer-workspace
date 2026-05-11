# Route 1 Fallback Wild Randomizer Check

## Datum

2026-05-11

## Ziel

Prüfen, ob Route 1 nach Deaktivierung der CFRU-Custom-Day/Night-Wild-Tabelle wieder über die von UPR-FVX randomisierte Vanilla/Fallback-Wild-Tabelle läuft.

## Änderung

Die CFRU-Route-1-Custom-Wild-Tabelle ist im Randomizer-Kompatibilitätsbuild per Macro standardmäßig deaktiviert:

```c
#define FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0
```

## Ergebnis laut UPR-FVX-Log

UPR-FVX erkennt Route 1 wieder als normale Encounter-Area:

```text
Area #3 - ROUTE 1 Grass/Cave
```

Im Log wurden für Route 1 randomisierte Encounters wie Geodude und Abra ausgegeben.

## Interpretation

FVX randomisiert Route 1 über die Vanilla/Fallback-Wilddaten. Die vorher aktive CFRU-Custom-Day/Night-Tabelle hatte die von FVX randomisierte Vanilla-Route-1-Tabelle ingame übersteuert.

## Offen

- Ingame Route 1 gegen den Log prüfen.
- Gen4-Gen9 Species-Pool bleibt separat offen.
- `<unknown>`-Einträge im Wild-Log müssen separat analysiert werden.

## Sicherheitsstatus

- Keine ROMs committed.
- Keine Builds committed.
- Keine Saves oder Emulator States committed.
- Keine Tool-Binaries committed.
