# 061 - P1 Regression-Smoke-Plan fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll plant spaetere Regression-Smokes fuer priorisierte FVX-GUI-Suboptionen aus Diagnose 060 und der FVX Feature-Coverage-Matrix. Es fuehrt keine Tests aus, verlangt keine neuen Randomizer-Laeufe und aendert keinen Code.

Scope:

- Nur bestehende Protokolle, Feature-Coverage-Dokumentation und read-only Befunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Grenzen:

- Diagnose 055 bleibt die Grenze fuer Log-Hygiene, Fallback-Marker und Placeholder-/Null-Species.
- Diagnose 056 bleibt die Grenze fuer MoveData-Write.
- Diagnose 057 bleibt die Grenze fuer Field Items, Shops, Pickup und allgemeine Item-Randomization.
- Diagnose 058 bleibt die Grenze fuer echte Palette-Randomization und Graphics/Sprites.
- Diagnose 059 bleibt die Grenze fuer TypeChart und Type-Effectiveness.
- Diagnose 060 bleibt die direkte Suboptions-Klassifikation. 061 stuft keine Suboption hoeher ein als 060.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `055_type_log_placeholder_hygiene.md`
- `056_p1_move_data_write_model.md`
- `057_p1_field_items_shops_pickup_model.md`
- `058_p1_palette_randomization_model.md`
- `059_p1_type_chart_model.md`
- `060_p1_gui_suboptions_regression_matrix.md`

Feature-Coverage-Belege:

- `01_docs/randomizer/fvx-feature-coverage.md`
- `00_project-control/roadmap/fvx-feature-roadmap.md`
- `01_docs/decisions/DEC-011-fvx-feature-coverage.md`

Coverage-Ausgangslage:

| Feld | Wert |
|---|---:|
| Feature-/Suboption-Zeilen gesamt | `130` |
| Nicht begonnen | `40` |
| Plan erstellt | `35` |
| Write modelliert | `23` |
| GUI-kompatibel | `32` |

061 nutzt diese Zaehlung zur Rueckverfolgbarkeit, erhebt aber keine neuen Testwerte.

## Allgemeine Smoke-Metriken fuer spaetere Laeufe

Jeder spaetere, separat freigegebene Smoke soll mindestens folgende Metriken dokumentieren, ohne private Artefakte offenzulegen:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload der geschriebenen ROM-Daten erfolgreich |
| Mismatches | relevanter Mismatch-Zaehler `0` |
| Stacktrace | `stacktrace=none` |
| Artefakte | keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs oder Tool-Binaries dokumentiert oder committed |
| Marker | `Bad Egg`, `<unknown>` und Unknown-/Fallback-Marker nach 055 klassifizieren, nicht als neuen Fehler werten |

Pfadspezifische Mismatch-Zaehler sollen aus dem jeweiligen Datenpfad stammen, z. B. `writeReloadMismatches=0`, `writeReloadBaseStatsMismatches=0`, `typeIdMismatches=0`, `writeReloadAbilityMismatches=0`, `writeReloadHiddenAbilityMismatches=0`, `writeReloadLearnsetMismatches=0`, `writeReloadMoveMismatches=0`, `writeReloadEncounterHeldItemMismatches=0`, `writeReloadEggMoveMismatches=0` oder ein klar benannter aequivalenter Zaehler.

## Smoke-Gruppen

### 1. Global Species Pools / Generation Limits

Ziel: Pool- und Restriction-Suboptionen gegen bereits stabile Species-Writer pruefen, ohne neue Writer zu aktivieren.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-GEN-001` | Limit Pokemon | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-GEN-002` | No Premature Evolutions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| related Pokemon / Generation Limits | Subdialog zu `Limit Pokemon` | Plan erstellt ueber `FVX-GEN-001` | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |

Empfohlene spaetere Smoke-Schnitte:

1. `Limit Pokemon` mit mehreren Generation-Limits gegen einen einzigen Species-Writer, z. B. Starters oder Wild Standard/Fallback.
2. `Limit Pokemon` mit related Pokemon gegen denselben Writer.
3. No Premature Evolutions nur als Poolfilter mit stabilem Species-Writer.

Nicht mischen:

- Keine MoveData-, Item-, Palette-, TypeChart-, Text- oder Graphics-Optionen.
- Keine `Change Impossible Evolutions` oder Evolution-Methoden-Rewrites.

### 2. Similar Strength / Same Type Pooling

Ziel: BST- und Type-basierte Poolfilter pruefen, ohne TypeChart oder MoveData-Write zu aktivieren.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-TRAIT-018` | Evolutions: Similar Strength | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-019` | Evolutions: Same Typing | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-FOE-009` | Force Diverse Types | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-WILD-011` | Similar Strength | GUI-kompatibel | wahrscheinlich supported, aber nicht einzeln getestet | Regression-Kandidat |
| `FVX-TM-005` | TM/HM Compatibility randomisieren | GUI-kompatibel | P1-supported fuer Compatibility | Basis, kein Same-Type-Hochstufen |
| `FVX-TM-013` | Tutor Compatibility randomisieren | GUI-kompatibel | P1-supported fuer Compatibility | Basis, kein Same-Type-Hochstufen |

Empfohlene spaetere Smoke-Schnitte:

1. Evolutions `Similar Strength` + `Same Typing`, ohne offene Evolution-Methodenoptionen.
2. Trainer Type-Themes oder Type Diversity getrennt von Trainer-Level-/Additional-Pokemon-Optionen.
3. Wild Similar Strength / Type Restrictions getrennt von Wild-Level-Modifier.
4. TM/Tutor Prefer Same Type getrennt von TypeChart.

Nicht mischen:

- Keine Type Effectiveness aus 059.
- Keine MoveData `Randomize Move Types`.
- Keine Palette `Follow Types`.

### 3. Evolutions Suboptions ohne offene Method-/Item-/Move-Writer

Ziel: Evolution-Suboptionen testen, die laut 060 ueber den bereits belegten Evolution-Species-Writer laufen sollten, ohne methoden-/item-/movebasierte Evolution-Rewrites.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-TRAIT-016` | Pokemon Evolutions randomisieren | GUI-kompatibel | P1-supported | Basis |
| `FVX-TRAIT-017` | Evolutions: Random Every Level | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-018` | Evolutions: Similar Strength | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-019` | Evolutions: Same Typing | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-020` | Evolutions: Limit to Three Stages | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-021` | Evolutions: No Convergence | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-022` | Evolutions: Force Change | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TRAIT-023` | Evolutions: Force Growth | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |

Explizit ausschliessen:

| Feature-ID | Feature | Coverage-Status | Grund |
|---|---|---|---|
| `FVX-TRAIT-024` | Change Impossible Evolutions | Nicht begonnen | offene Methoden-/ExtraInfo-/Item-/Move-/Location-Beruehrung |
| `FVX-TRAIT-025` | Make Evolutions Easier | Nicht begonnen | eigener Methoden-/Level-Rewrite |
| `FVX-TRAIT-026` | Use Estimated Evolution Levels | Nicht begonnen | nur mit Evolution-Methodenblock pruefen |
| `FVX-TRAIT-027` | Remove Time-Based Evolutions | Nicht begonnen | eigener Methodenpfad |

Empfohlene spaetere Reihenfolge:

1. Random Every Level allein.
2. Random + Similar Strength + Same Typing.
3. Random + Limit to Three Stages + No Convergence.
4. Random + Force Change + Force Growth.

### 4. Starters Suboptions

Ziel: Starter-Poolfilter ueber den belegten Starter-Species-Writer pruefen, ohne Starter-Held-Item-Writer.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-SST-002` | Starter Pokemon: Random completely | GUI-kompatibel | P1-supported | Basis |
| `FVX-SST-003` | Starter Pokemon: Random basic with 2 evolutions | GUI-kompatibel | wahrscheinlich supported, aber nicht einzeln getestet | Regression-Kandidat |
| `FVX-SST-004` | Starter Pokemon: Random any basic | GUI-kompatibel | wahrscheinlich supported, aber nicht einzeln getestet | Regression-Kandidat |
| `FVX-SST-005` | Starter Type Restrictions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-SST-006` | Starter: Don't Use Legendaries | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-SST-009` | Starter BST-Min/Max | Nicht begonnen | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat nach Planstatus-Update |

Explizit ausschliessen:

| Feature-ID | Feature | Coverage-Status | Grund |
|---|---|---|---|
| `FVX-SST-007` | Starter Held Items randomisieren | Nicht begonnen | eigener Starter-Held-Item-Writer |
| `FVX-SST-008` | Starter Held Items: Ban Bad Items | Nicht begonnen | Item-Pool-Policy, nicht durch 054/057 belegt |

Empfohlene spaetere Smoke-Schnitte:

1. Random basic / two evolutions ohne weitere Filter.
2. Type Restrictions + No Dual Types / no legendaries.
3. BST-Min/Max separat, damit Pool-Engpaesse isolierbar bleiben.

### 5. Movesets / TM / Tutor / Egg Suboptions

Ziel: Suboptionen pruefen, die bestehende Learnset-, TM/HM-, Tutor- und Egg-Move-Pfade nutzen, ohne MoveData-Write.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-MOVE-007` | Pokemon Movesets randomisieren | GUI-kompatibel | P1-supported | Basis |
| `FVX-MOVE-008` | Guaranteed Level 1 Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-MOVE-009` | Reorder Damaging Moves | GUI-kompatibel | P1-supported | Regression-Kandidat |
| `FVX-MOVE-010` | No Game-Breaking Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-MOVE-011` | Force % Good Damaging Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-001` | TM Moves randomisieren | GUI-kompatibel | P1-supported | Basis |
| `FVX-TM-002` | Keep Field Move TMs | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat, kein Field-Item-Smoke |
| `FVX-TM-003` | TM No Game-Breaking Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-004` | TM Force % Good Damaging Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-006` | TM/Levelup Move Sanity | GUI-kompatibel | P1-supported fuer getestete Sanity-Flow-Kombinationen | Regression-Kandidat |
| `FVX-TM-007` | TM Compatibility Follow Evolutions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-008` | Full HM Compatibility | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-009` | Move Tutor Moves randomisieren | GUI-kompatibel | P1-supported | Basis |
| `FVX-TM-010` | Keep Field Move Tutors | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat, kein Field-Item-Smoke |
| `FVX-TM-011` | Tutor No Game-Breaking Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-012` | Tutor Force % Good Damaging Moves | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |
| `FVX-TM-014` | Tutor/Levelup Sanity | GUI-kompatibel | P1-supported fuer getestete Sanity-Flow-Kombinationen | Regression-Kandidat |
| `FVX-TM-015` | Tutor Compatibility Follow Evolutions | Plan erstellt | wahrscheinlich supported, aber nicht einzeln getestet | Smoke-Kandidat |

Explizit ausschliessen:

- `FVX-MOVE-001` bis `FVX-MOVE-006`: MoveData-Write / Update Moves nach 056.
- Move-Namen, Move-Descriptions, Tutor text/menu und Special Tutors.

Empfohlene spaetere Smoke-Schnitte:

1. Pokemon Movesets: Guaranteed Level 1 + No Game-Breaking + Force Good Damaging.
2. TM Moves: Keep Field Move TMs + No Game-Breaking + Force Good Damaging.
3. TM Compatibility: Prefer Same Type + Follow Evolutions + Level-Up Sanity.
4. Tutor Moves: Keep Field Move Tutors + No Game-Breaking + Force Good Damaging.
5. Tutor Compatibility: Prefer Same Type + Follow Evolutions + Level-Up Sanity.
6. Egg Moves nur als Regression, wenn gekoppelte Moveset-Optionen aktiv sind.

### 6. Trainer Level Modifier separat

Ziel: Trainer-Level- und Trainer-Evolution-Level-Effekte separat planen, weil sie eigene Level-Write-/Range-Effekte sind.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-FOE-001` | Trainer Pokemon randomisieren | GUI-kompatibel | P1-supported | Basis |
| `FVX-FOE-014` | Trainers Evolve Their Pokemon + Level Modifier | Nicht begonnen | open-not-diagnosed | separater Smoke-Kandidat |

Nicht mischen:

- Keine Additional Pokemon.
- Keine Battle Style.
- Keine Trainer Names / Class Names.
- Keine Item-, MoveData-, TypeChart-, Palette- oder Graphics-Writer.

Empfohlene spaetere Reihenfolge:

1. Trainer Level Modifier ohne Trainer-Species-Randomization, falls GUI/Settings das isoliert erlaubt.
2. Trainer Level Modifier mit Trainer Pokemon randomisieren.
3. Trainers Evolve Their Pokemon / Evolution Level Modifier separat.

### 7. Wild Level Modifier separat

Ziel: Wild-Level- und Catch-/Level-Sonderoptionen getrennt von Species- und Held-Item-Smokes planen.

Feature-IDs:

| Feature-ID | Feature | Coverage-Status | 060-Status | Smoke-Einordnung |
|---|---|---|---|---|
| `FVX-WILD-001` | Randomize Wild Pokemon | GUI-kompatibel | P1-supported fuer Standard/Fallback-Wild | Basis |
| `FVX-WILD-007` | Set Minimum Catch Rate | Nicht begonnen | open-not-diagnosed | separater Smoke-Kandidat |
| `FVX-WILD-010` | Catch Em All Mode | Nicht begonnen | open-not-diagnosed | separater Smoke-Kandidat |
| `FVX-WILD-012` | Balance Low Level Encounters + Level Modifier | Nicht begonnen | open-not-diagnosed | separater Smoke-Kandidat |

Nicht mischen:

- Keine CFRU Day/Night-Custom-Wild-Tabellen.
- Keine Field Items/Shops/Pickup.
- Keine TypeChart- oder Palette-Optionen.

Empfohlene spaetere Reihenfolge:

1. Wild Level Modifier allein mit Standard/Fallback-Wild.
2. Minimum Catch Rate separat.
3. Catch Em All separat.
4. Balance Low Level Encounters nur nach Level-Modifier-Smoke.

### 8. Offene Writer als Nicht-Smoke-Fixbereiche

Diese Bereiche gehoeren nicht in allgemeine Regression-Smokes. Sie brauchen eigene Fix- oder Modellbranches mit separaten Reload-Kriterien.

| Bereich | Feature-IDs | Coverage-Status | Grenze | Naechster Branch-Typ |
|---|---|---|---|---|
| MoveData Write | `FVX-MOVE-001` bis `FVX-MOVE-006` | Write modelliert | 056 | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` |
| Field Items / Shops / Pickup | `FVX-ITEM-001` bis `FVX-ITEM-010` | Write modelliert | 057 | `compat/upr-fvx-cfru-dpe-field-items-shops-pickup-scope-and-write` |
| Palette Randomization | `FVX-GFX-001` bis `FVX-GFX-004` | Write modelliert | 058 | `compat/upr-fvx-cfru-dpe-palette-randomization-preserve-repoint` |
| TypeChart | `FVX-TYPE-001` bis `FVX-TYPE-003` | Write modelliert | 059 | `compat/upr-fvx-cfru-dpe-type-chart-preserve-effectiveness` |
| Graphics / Sprites | `FVX-GFX-005`, `FVX-GFX-006` | Nicht begonnen | 058 out of scope | P2 Graphics-Modell |
| Text / Menu | Trainer names, class names, move names, tutor text/menu, lowercase names | Nicht begonnen / open | 056/060 Text-Grenze | P2 Text/Menu-Modell |

## Empfohlene Reihenfolge spaeterer Smoke-Checks

Die Reihenfolge minimiert Vermischung und beginnt mit Suboptionen, die nur Pool-/Filterlogik ueber belegte Writer nutzen.

| Reihenfolge | Smoke-Gruppe | Warum zuerst/spaeter |
|---:|---|---|
| 1 | Global Species Pools / Generation Limits | niedrigstes Writer-Risiko; prueft Grundrestriktionen fuer viele Gruppen |
| 2 | Starters Suboptions | kleiner, bereits stabiler Species-Writer |
| 3 | Similar Strength / Same Type Pooling | prueft BST-/Type-Pooling ohne TypeChart |
| 4 | Evolutions Suboptions ohne Methodenwriter | nutzt belegten Evolution-Species-Writer; methodische Rewrites bleiben ausgeschlossen |
| 5 | Movesets/TM/Tutor/Egg Suboptions | mehrere bereits stabile Datenpfade, aber mehr Kombinationsrisiko |
| 6 | Trainer Level Modifier separat | eigener Level-Write-/Range-Effekt |
| 7 | Wild Level Modifier separat | eigener Level-/Catch-Rate-/Wild-Sonderpfad |
| 8 | Offene Writer-Fixbereiche | nur nach separater Freigabe, nicht als allgemeiner Smoke |

## Stop-Regeln

Ein spaeterer Smoke- oder Fixblock soll stoppen, wenn:

1. Ein allgemeiner Regression-Smoke einen offenen Writer aus 056-059 aktiviert.
2. Eine Suboption in 060 nur `wahrscheinlich supported`, `open-not-diagnosed` oder `modelliert, Fix offen` ist, aber als `P1-supported` dokumentiert werden soll.
3. Ein Lauf ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, private Pfade, ROM-Namen, Hashes, Secrets, Tokens oder `.env`-Inhalte offenlegen wuerde.
4. Ein neuer Diagnosewert nicht aus einem tatsaechlichen spaeteren Lauf stammt.
5. `Bad Egg`, `<unknown>` oder Unknown-Fallback-Marker ohne 055-Kontext als neuer Fehler interpretiert werden.
6. Ein Smoke mehrere unabhängige Writer mischt, sodass ein Mismatch nicht eindeutig zugeordnet werden kann.

## Ergebnis

061 legt einen read-only Regression-Smoke-Plan fest. Die priorisierten Smoke-Gruppen decken die 060-Suboptionsklassifikation und die Feature-Coverage-Matrix ab, ohne offene Writer zu vermischen. Spaetere Laeufe muessen Feature-IDs referenzieren, die allgemeinen Metriken dokumentieren und pro Smoke nur eine klar abgegrenzte Writer- oder Pooloberflaeche pruefen.
