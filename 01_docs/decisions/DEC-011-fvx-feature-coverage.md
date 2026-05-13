# DEC-011: UPR FVX GUI Features als Requirements-Basis nutzen

## Entscheidung

Die sichtbaren Universal Pokemon Randomizer FVX 1.5.1 GUI-Features werden als primaere Randomizer-Kompatibilitaetsanforderungen dokumentiert.

## Konsequenz

- Detailabdeckung und Statuszaehlung liegen in `01_docs/randomizer/fvx-feature-coverage.md`.
- Feature-orientierte Roadmap-Pakete liegen in `00_project-control/roadmap/fvx-feature-roadmap.md`.
- `00_project-control/roadmap/roadmap-status.md` bleibt die allgemeine Projekt-Roadmap und soll nur grobe Statuswechsel aufnehmen.
- Tests und Diagnoseprotokolle sollen kuenftig Feature-IDs wie `FVX-WILD-001` oder `FVX-TM-005` referenzieren.
- Die Excel-Roadmap bleibt ein visuelles Dashboard und nicht die Source of Truth.

## Begruendung

Die FVX-GUI-Screenshots bilden die genaueste sichtbare Anforderungsflaeche. Eine einzelne allgemeine Roadmap-Liste ist dafuer zu grob, waehrend 130 einzelne Roadmap-Zeilen zu unuebersichtlich waeren. Die getrennte Feature-Matrix liefert Traceability, die Roadmap bleibt planbar.

## Grenzen

- Diese Entscheidung ist eine Dokumentations- und Planungsentscheidung.
- Sie fuehrt keine ROM-, Build-, Toolchain- oder Randomizer-Laeufe aus.
- Keine ROMs, Saves, Builds, Tool-Binaries, private Pfade oder Secrets werden dokumentiert.
