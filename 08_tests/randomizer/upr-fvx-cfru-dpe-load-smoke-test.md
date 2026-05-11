
## Load-Versuch mit CFRU/DPE-Build

- GUI gestartet: ja
- ROM geladen: nein
- Fehlerklasse: `java.lang.IndexOutOfBoundsException`
- Fehler: `Index 1462 out of bounds for length 1375`
- Fehlerstelle: `com.uprfvx.romio.romhandlers.Gen3RomHandler.loadBasicPokeStats`
- Interpretation: Die CFRU/DPE-ROM nutzt mehr interne Species-IDs als UPR-FVX aktuell kennt.
- Naechster Anpassungsbedarf: Species-ID-/Species-Datenbasis in UPR-FVX fuer CFRU/DPE-Gen9 erweitern.
