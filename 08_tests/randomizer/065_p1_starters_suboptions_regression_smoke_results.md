# 065 - P1 Starters Suboptions Regression-Smoke Results

## Ziel

Dieses Protokoll dokumentiert sanitisiert die lokal ausgefuehrten Starter-Suboptions-Smoke-Slices aus Diagnose 063.

Scope:

- Nur Ergebnisdokumentation eines bereits lokal ausgefuehrten Smokes.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe in diesem Dokumentationsblock.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte dokumentiert oder committed.

## Beleggrenzen

Primaere Plan- und Klassifikationsbelege:

- `055_type_log_placeholder_hygiene.md`
- `060_p1_gui_suboptions_regression_matrix.md`
- `061_p1_regression_smoke_plan.md`
- `063_p1_starters_suboptions_regression_smoke.md`
- `064_p1_global_species_pool_regression_smoke_results.md`

Feature-Coverage-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

065 ist ein Smoke-Ergebnis fuer Starter-Pool-/Filter-Suboptionen ueber den Starter-Species-Writer. Es erweitert nicht:

- Starter Held Items.
- Wild-/Trainer-/Evolution-Kombinationen.
- MoveData-Write.
- Field Items, Shops oder Pickup.
- Palette-Randomization.
- TypeChart oder Type Effectiveness.
- Text, Menu oder Graphics.

## Aktive Smoke-Grenze

Aktiv war jeweils nur:

- der Starter-Species-Writer.
- die Starter-Suboption des jeweiligen Slice.

Explizit aus blieben:

- `FVX-SST-007` Starter Held Items randomisieren.
- `FVX-SST-008` Starter Held Items: Ban Bad Items.
- MoveData Write.
- Field Items, Shops und Pickup.
- Palette-Randomization.
- TypeChart.
- Text, Menu und Graphics.

## Ergebnisse

| Slice | Feature-IDs | Save | Log | Reload | Starter-Mismatches | Filterverletzungen | Stacktrace |
|---|---|---:|---:|---:|---:|---:|---|
| Baseline `FVX-SST-002` | `FVX-SST-002` | true | true | true | 0 | 0 | none |
| `FVX-SST-003` basic with 2 evolutions | `FVX-SST-003` | true | true | true | 0 | 0 | none |
| `FVX-SST-004` any basic | `FVX-SST-004` | true | true | true | 0 | 0 | none |
| `FVX-SST-005` type restrictions | `FVX-SST-005` | true | true | true | 0 | 0 | none |
| `FVX-SST-006` no legendaries | `FVX-SST-006` | true | true | true | 0 | 0 | none |
| `FVX-SST-009` BST min/max | `FVX-SST-009` | true | true | true | 0 | 0 | none |

Weitere sanitisiert dokumentierte Marker:

- `Bad Egg=false` in allen Slice-Logs.
- `<unknown>=false` in allen Slice-Logs.
- Die lokalen Artefakte blieben ignored und werden nicht dokumentiert.

## Einordnung

Das Ergebnis bestaetigt:

- `FVX-SST-003` im getesteten Starter-Species-Writer-Smoke.
- `FVX-SST-004` im getesteten Starter-Species-Writer-Smoke.
- `FVX-SST-005` im getesteten Starter-Species-Writer-Smoke.
- `FVX-SST-006` im getesteten Starter-Species-Writer-Smoke.
- `FVX-SST-009` im getesteten Starter-Species-Writer-Smoke.

Das Ergebnis bestaetigt nicht:

- Starter Held Items `FVX-SST-007` oder `FVX-SST-008`.
- Wild-/Trainer-/Evolution-Kombinationen.
- Interaktion mit Global Species Pools aus 062/064.
- Interaktion mit Similar Strength, Same Type, Level Modifier oder anderen Poolfiltern.
- irgendeinen offenen Writer aus den Grenzen 056-059.

## P1-Bewertung

Fuer den getesteten Starter-Species-Writer-Scope gelten `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` als gesmoked. Die konservative Coverage-Formulierung lautet:

- `FVX-SST-003`: getestet im Starter-Species-Writer-Smoke.
- `FVX-SST-004`: getestet im Starter-Species-Writer-Smoke.
- `FVX-SST-005`: getestet im Starter-Species-Writer-Smoke.
- `FVX-SST-006`: getestet im Starter-Species-Writer-Smoke.
- `FVX-SST-009`: getestet im Starter-Species-Writer-Smoke.
- `FVX-SST-007`/`FVX-SST-008`: separat und weiterhin offen.

Die Suboptionen duerfen deshalb nicht automatisch fuer Wild, Trainer, Evolutionen oder kombinierte GUI-Smokes hochgestuft werden. Weitere Smokes muessen die jeweilige Writer-Oberflaeche und den jeweiligen Mismatch-Zaehler separat benennen.

## Sicherheitsnotizen

- Es wurden keine ROM-/Log-/Output-ROM-/Build-Pfade, ROM-Namen oder Hashes dokumentiert.
- Es wurden keine lokalen Artefakte committed.
- Es wurden keine neuen Randomizer-Laeufe fuer diesen Dokumentationsblock ausgefuehrt.
- Marker aus 055 bleiben Log-Hygiene und werden nur kontextbezogen bewertet.

## Naechster sinnvoller Schritt

Naechster enger Smoke-Scope ist Similar Strength / Same Type Pooling, ohne TypeChart oder MoveData-Write zu aktivieren.
