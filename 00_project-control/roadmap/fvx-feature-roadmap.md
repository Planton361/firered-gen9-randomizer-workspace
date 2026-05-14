# FVX Feature Roadmap

Diese Datei ist die feature-orientierte Roadmap fuer Universal Pokemon Randomizer FVX. Sie verdichtet `01_docs/randomizer/fvx-feature-coverage.md` auf planbare Arbeitspakete.

Die detaillierte Status- und Feature-ID-Matrix bleibt in:

```text
01_docs/randomizer/fvx-feature-coverage.md
```

## Gesamtstand aus Feature-Matrix

| Status | Anzahl |
|---|---:|
| Nicht begonnen | 39 |
| Plan erstellt | 31 |
| Read modelliert | 0 |
| Write modelliert | 23 |
| Getestet | 7 |
| GUI-kompatibel | 30 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Feature-Pakete

| Paket | Feature-Zeilen | Leitstatus | Ziel |
|---|---:|---|---|
| General Options | 4 | Gemischt | `FVX-GEN-001/002` sind im Starter-Carrier-Smoke getestet; Race Mode und Intro-Mon separat pruefen |
| Pokemon Traits | 28 | Gemischt | Base Stats, Types, Abilities, Evolutions, EXP Curves und Suboptionen systematisch absichern |
| Starters, Statics & Trades | 15 | Gemischt | Starter-Filter sind im Starter-Species-Writer-Smoke getestet; Starter-Held-Items, Trades und Level-Subpfade ergaenzen |
| Moves & Movesets | 11 | Gemischt | Learnset-/Moveset-GUI halten; Move-Data-Writer fertig absichern |
| Foe Pokemon | 14 | Gemischt | Trainer-Species/-Movesets/-Held-Items halten; Trainer-Suboptionen ergaenzen |
| Wild Pokemon | 12 | Gemischt | Standard/Fallback-Wild halten; Level/Catch/Catch-em-all-Suboptionen ergaenzen |
| TM/HMs & Tutors | 15 | Gemischt | TM/Tutor-Tabellen halten; Preserve-/Filter-/Follow-Evolution-Suboptionen testen |
| Items | 10 | Write modelliert | Field Items, Shops und Pickup als getrennte Writer implementieren/testen |
| Types | 3 | Write modelliert | Type-Effectiveness-Table mit Fairy/Stellar-Preserve absichern |
| Graphics | 6 | Gemischt | Palette-Randomization absichern; Custom Player Graphics separat modellieren |
| Misc Tweaks | 12 | Nicht begonnen | jeden Misc-Tweak als eigenen Patch-/Risk-Scope inventarisieren |
| GUI-Suboptions-Regressionsmatrix | n/a | Erledigt | vorhandene Diagnose 060 als technische Regressionssicht nutzen |
| Regression-Smoke-Plan | n/a | In Arbeit | konkrete Smoke-/Regression-Laeufe aus Feature-IDs ableiten und sanitisiert dokumentieren |

## Priorisierte Roadmap ab jetzt

### P0 - Coverage und Smoke-Plan

| Reihenfolge | Branch | Ziel | Status |
|---|---|---|---|
| P0.1 | `docs/fvx-feature-coverage-matrix` | FVX-GUI-Features als Requirements-/Coverage-Matrix dokumentieren | In Arbeit |
| P0.2 | `analysis/upr-fvx-cfru-dpe-p1-regression-smoke-plan` | Smoke-/Regression-Plan fuer priorisierte GUI-Suboptionen erstellen, ohne neue Randomizer-Laeufe im Planblock | Erledigt |
| P0.3 | `test/upr-fvx-cfru-dpe-p1-global-species-pool-regression-smoke` | Global-Species-Pool-Smoke fuer `FVX-GEN-001/002` im Starter-Carrier-Scope sanitisiert dokumentieren | Erledigt |
| P0.4 | `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starter-Suboptions-Smoke fuer `FVX-SST-003/004/005/006/009` sanitisiert dokumentieren | In Arbeit |

### P1 - Offene Writer mit vorhandenen Modellen

| Reihenfolge | Branch | Paket | Ziel |
|---|---|---|---|
| P1.1 | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` | Types | Type-Effectiveness-Table mit Fairy-Reload, unsupported/Stellar-Preserve und Terminator-/Kapazitaetskriterien absichern |
| P1.2 | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` | Moves & Movesets | eng gegateten MoveData-Writer mit Preserve-Policy und Reload-Diagnose umsetzen |
| P1.3 | `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint` | Graphics | echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern |
| P1.4 | `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write` | Items | Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern |

### P2 - Suboptionen der bereits GUI-kompatiblen Pakete

| Paket | Ziel |
|---|---|
| Pokemon Traits | Follow Evolutions, Force Dual Types, Ability-Ban-/Allow-Filter, Evolution-Filter, EXP Curves testen |
| Starters, Statics & Trades | Starter-Held-Items und In-Game-Trades absichern; Starter-Type-/Legendary-/BST-Filter ausserhalb des Starter-Species-Writer-Smokes nur separat hochstufen |
| Foe Pokemon | Additional Pokemon, Force Diverse Types, League-Unique, Battle Style, Rival Carry, Trainer Names/Class Names absichern |
| Wild Pokemon | Evolution Restrictions, Catch Rate, Catch-em-all und Level-Balance absichern |
| TM/HMs & Tutors | Keep Field Moves, No Game-Breaking, Good-Damaging-%, Follow-Evolutions und Full-HM-Kompatibilitaet absichern |

### P3 - Noch nicht begonnene Sonderbereiche

| Paket | Ziel |
|---|---|
| General Options | Limit Pokemon und No Premature Evolutions ausserhalb des Starter-Carrier-Smokes weiter pruefen; No Random Intro Mon und Race Mode separat inventarisieren |
| Misc Tweaks | alle 12 Misc Tweaks inventarisieren und pro Tweak Risiko/Writer bestimmen |
| Custom Player Graphics | getrennt von Pokemon-Palette-Randomization modellieren |
| In-Game Trades Text/Items/IVs | Spezies-, Text-, Item- und IV-Writer getrennt pruefen |

## Roadmap-Regel

- Neue Einzeltests referenzieren mindestens eine `FVX-*` Feature-ID aus der Matrix.
- Die Feature-Matrix ist fuer Vollstaendigkeit und Zaehlregel massgeblich.
- Diese Roadmap ist fuer Reihenfolge und Arbeitsbranch-Zuschnitt massgeblich.
- `roadmap-status.md` bleibt die allgemeine Projekt-Roadmap und sollte nur grobe Statuswechsel aufnehmen.
- Keine ROMs, Saves, Builds, Tool-Binaries, private Pfade oder Secrets in Roadmap-Dateien aufnehmen.
