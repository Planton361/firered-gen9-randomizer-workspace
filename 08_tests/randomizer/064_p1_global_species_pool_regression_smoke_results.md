# 064 - P1 Global Species Pool Regression-Smoke Results

## Ziel

Dieses Protokoll dokumentiert sanitisiert die lokal ausgefuehrten Global-Species-Pool-Smoke-Slices aus Diagnose 062.

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
- `062_p1_global_species_pool_regression_smoke.md`

Feature-Coverage-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`

064 ist ein Smoke-Ergebnis fuer einen engen Carrier-Scope. Es erweitert nicht:

- Wild-/Trainer-/Evolution-Kombinationen.
- MoveData-Write.
- Field Items, Shops, Pickup oder Held-Item-Writer.
- Palette-Randomization, Graphics oder Sprites.
- TypeChart oder Type Effectiveness.
- Text, Menu oder Description.

## Aktive Smoke-Grenze

Aktiv war nur:

- `FVX-SST-002` als Starter-Species-Carrier.
- der jeweilige Global-Species-Poolfilter pro Slice.

Explizit aus blieben:

- Held Items.
- MoveData-Write.
- Palette-Randomization.
- TypeChart.
- Evolution-Methoden-Fixes.
- Intro/Race Mode.

## Ergebnisse

| Slice | Feature-IDs | Save | Log | Reload | Starter-Mismatches | Stacktrace |
|---|---|---:|---:|---:|---:|---|
| Baseline Carrier | `FVX-SST-002` | true | true | true | 0 | none |
| `FVX-GEN-001` Generation Limits | `FVX-GEN-001`, `FVX-SST-002` | true | true | true | 0 | none |
| `FVX-GEN-001` related Pokemon | `FVX-GEN-001`, `FVX-SST-002` | true | true | true | 0 | none |
| `FVX-GEN-002` No Premature Evolutions | `FVX-GEN-002`, `FVX-SST-002` | true | true | true | 0 | none |

Weitere sanitisiert dokumentierte Marker:

- `Bad Egg` trat in den Slice-Logs nicht auf.
- `<unknown>` trat in den Slice-Logs nicht auf.
- Die lokalen Artefakte blieben ignored und werden nicht dokumentiert.

## Einordnung

Das Ergebnis bestaetigt:

- `FVX-GEN-001` im getesteten Starter-Species-Carrier-Smoke mit Generation Limits.
- `FVX-GEN-001` im getesteten Starter-Species-Carrier-Smoke mit related Pokemon.
- `FVX-GEN-002` im getesteten Starter-Species-Carrier-Smoke.

Das Ergebnis bestaetigt nicht:

- globale Vollabdeckung von `FVX-GEN-001` oder `FVX-GEN-002` ueber alle Writer.
- Wild-/Trainer-/Evolution-Kombinationen.
- Interaktion mit Similar Strength, Same Type, Level Modifier oder anderen Poolfiltern.
- irgendeinen offenen Writer aus den Grenzen 056-059.

## P1-Bewertung

Fuer den getesteten Carrier-Scope gelten `FVX-GEN-001` und `FVX-GEN-002` als gesmoked. Die konservative Coverage-Formulierung lautet:

- `FVX-GEN-001`: getestet im Starter-Carrier-Smoke, nicht global vollabgedeckt.
- `FVX-GEN-002`: getestet im Starter-Carrier-Smoke, nicht global vollabgedeckt.

Die Suboptionen duerfen deshalb nicht automatisch fuer Wild, Trainer, Evolutionen oder kombinierte GUI-Smokes hochgestuft werden. Weitere Smokes muessen die jeweilige Writer-Oberflaeche und den jeweiligen Mismatch-Zaehler separat benennen.

## Sicherheitsnotizen

- Es wurden keine ROM-/Log-/Output-ROM-/Build-Pfade, ROM-Namen oder Hashes dokumentiert.
- Es wurden keine lokalen Artefakte committed.
- Es wurden keine neuen Randomizer-Laeufe fuer diesen Dokumentationsblock ausgefuehrt.
- Marker aus 055 bleiben Log-Hygiene und werden nur kontextbezogen bewertet.

## Naechster sinnvoller Schritt

Naechster enger Smoke-Scope ist der bereits geplante Starter-Suboptions-Smoke aus 063, getrennt von Starter Held Items und offenen Writern.
