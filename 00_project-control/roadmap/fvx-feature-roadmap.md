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
| Plan erstellt | 28 |
| Read modelliert | 0 |
| Write modelliert | 15 |
| Getestet | 10 |
| GUI-kompatibel | 38 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Feature-Pakete

| Paket | Feature-Zeilen | Leitstatus | Ziel |
|---|---:|---|---|
| General Options | 4 | Gemischt | `FVX-GEN-001/002` sind im Starter-Carrier-Smoke getestet; Race Mode und Intro-Mon separat pruefen |
| Pokemon Traits | 28 | Gemischt | Base Stats, Types, Abilities, Evolutions, EXP Curves und Suboptionen systematisch absichern; Evolution Similar Strength und Same Typing sind im engen `FVX-TRAIT-016`-Scope stabil, weitere Evolution-Suboptionen getrennt halten |
| Starters, Statics & Trades | 15 | Gemischt | Starter-Filter sind im Starter-Species-Writer-Smoke getestet; Starter-Held-Items, Trades und Level-Subpfade ergaenzen |
| Moves & Movesets | 11 | Gemischt | Learnset-/Moveset-GUI halten; MoveData `Update Moves`, Power/Accuracy/PP und Move Types sind stabil; Move Names / Descriptions bleibt als separater Text/Menu-Scope zu planen |
| Foe Pokemon | 14 | Gemischt | Trainer-Species/-Movesets/-Held-Items halten; Trainer Similar Strength und `FVX-FOE-009` sind im `FVX-FOE-001` Carrier stabil |
| Wild Pokemon | 12 | Gemischt | Standard/Fallback-Wild halten; Similar Strength und Type Restrictions sind nach Diagnose 075 im `FVX-WILD-001` Carrier wieder stabil |
| TM/HMs & Tutors | 15 | Gemischt | TM/Tutor-Tabellen halten; Preserve-/Filter-/Follow-Evolution-Suboptionen testen |
| Items | 10 | Write modelliert | Field Items, Shops und Pickup als getrennte Writer implementieren/testen |
| Types | 3 | Getestet | TypeEffectiveness Random, Balanced, Keep Type Identities, Inverse, Add Immunities und Update Type Effectiveness sind einzeln im TypeChart-Scope getestet |
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
| P0.4 | `test/upr-fvx-cfru-dpe-p1-starters-suboptions-regression-smoke` | Starter-Suboptions-Smoke fuer `FVX-SST-003/004/005/006/009` sanitisiert dokumentieren | Erledigt |
| P0.5 | `test/upr-fvx-cfru-dpe-p1-similar-strength-same-type-regression-smoke` | Similar-Strength-/Same-Type-/Type-Restrictions-Smoke sanitisiert dokumentieren | Review/Test |

### P1 - Offene Writer mit vorhandenen Modellen

| Reihenfolge | Branch | Paket | Ziel |
|---|---|---|---|
| P1.1 | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` + `test/upr-fvx-cfru-dpe-p1-type-effectiveness-followup-smokes` | Types | erledigt: TypeEffectiveness Random, Balanced, Keep Type Identities, Inverse, Add Immunities und Update Type Effectiveness mit Reload-/Terminator-/Preserve-Kriterien abgesichert |
| P1.2 | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` + `test/upr-fvx-cfru-dpe-move-data-write-preserve-reload-smoke` | Moves & Movesets | erledigt: UPR-FVX PR #33, Workspace PR #124 und Workspace PR #125 sind gemerged; Diagnose 084 bestaetigt `Update Moves` mit `writeReloadMoveDataMismatches=0`, stabilem category/split-Reload und bytegleich erhaltenen Preserve-Bytes |
| P1.2a | `test/upr-fvx-cfru-dpe-move-data-power-accuracy-pp-reload-smoke` | Moves & Movesets | erledigt: Diagnose 085 bestaetigt `FVX-MOVE-001/002/003` mit `writeReloadMoveDataMismatches=0`, stabilen `+1/+3/+4` Bytes und bytegleich erhaltenen Preserve-Bytes |
| P1.2b | `test/upr-fvx-cfru-dpe-move-data-types-reload-smoke` | Moves & Movesets | blockiert: Diagnose 086 zeigt Save/Log/Output/Reload true und Preserve-Bytes stabil, aber `writeReloadMoveDataMismatches=54` durch Fairy-Type-Byte-Mismatches im MoveData-`+2 type`-Writer |
| P1.2c | `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte` | Moves & Movesets | erledigt und gemerged: UPR-FVX PR #34, Workspace PR #129 und Diagnose 087 bestaetigen `FVX-MOVE-004` mit `writeReloadMoveDataMismatches=0`, `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0` und bytegleich erhaltenen Preserve-Bytes |
| P1.2d | `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan` | Moves & Movesets | naechster konservativer Planungsblock fuer `FVX-MOVE-005` Move Names / Move Descriptions als getrennten Text/Menu-Scope; keine Umsetzung im Sync-Block |
| P1.3 | `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint` | Graphics | echte geaenderte Palette-Randomization mit compressed/shared/repointing Reload-Kriterien absichern |
| P1.4 | `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write` | Items | Field Items, Shops und Pickup mit getrennten Reload-Kriterien absichern |

### P2 - Suboptionen der bereits GUI-kompatiblen Pakete

| Paket | Ziel |
|---|---|
| Pokemon Traits | Follow Evolutions, Force Dual Types, Ability-Ban-/Allow-Filter, EXP Curves testen; `FVX-TRAIT-018` aus 082 und `FVX-TRAIT-019` aus 080 halten, Evolution-Methoden weiter getrennt behandeln |
| Starters, Statics & Trades | Starter-Held-Items und In-Game-Trades absichern; Starter-Type-/Legendary-/BST-Filter ausserhalb des Starter-Species-Writer-Smokes nur separat hochstufen |
| Foe Pokemon | Additional Pokemon, League-Unique, Battle Style, Rival Carry, Trainer Names/Class Names absichern; Force Diverse Types / `FVX-FOE-009` aus 078 im `FVX-FOE-001` Carrier halten |
| Wild Pokemon | Evolution Restrictions, Catch Rate, Catch-em-all und Level-Balance absichern; Wild Similar Strength und Type Restrictions aus 075 im `FVX-WILD-001` Carrier halten |
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
