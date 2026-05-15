# FVX Progress Dashboard

## Zweck

Dieses Dashboard ist die schnelle Lesedatei fuer den aktuellen Universal Pokemon Randomizer FVX-Kompatibilitaetsstand im FireRed Gen9 Randomizer Workspace.

Es ersetzt keine Detaildiagnosen. Es verdichtet die Detailquellen auf eine Statusuebersicht und listet zusaetzlich alle aktuell erfassten FVX-Features einmal kompakt auf.

Optionaler XLSX-Export fuer filterbare Tabellen:
`python 07_scripts/randomizer/export_fvx_progress_dashboard_xlsx.py --input 01_docs/randomizer/fvx-progress-dashboard.md --output /tmp/fvx-progress-dashboard.xlsx`.
Markdown bleibt Source of Truth.

- Was ist P1-supported?
- Was ist nur in einem Carrier getestet?
- Was ist read-only oder write-only modelliert?
- Was ist blockiert?
- Was ist als Naechstes dran?
- Welche Diagnoseprotokolle belegen den Stand?
- Welche konkreten Features existieren aktuell in der Matrix?

## Detailquellen

| Datei / Bereich | Rolle |
|---|---|
| `01_docs/randomizer/fvx-feature-coverage.md` | vollstaendige FVX-Feature-/Suboption-Matrix mit Feature-IDs |
| `00_project-control/roadmap/fvx-feature-roadmap.md` | feature-orientierte Roadmap und Arbeitsbranch-Reihenfolge |
| `00_project-control/roadmap/roadmap-status.md` | allgemeine Projekt-Roadmap |
| `08_tests/randomizer/*.md` | Diagnose-, Smoke- und Modellprotokolle |
| `01_docs/NEXT_STEPS.md` | naechster minimaler Arbeitsblock |
| `01_docs/SESSION_STATE.md` | chronologischer Arbeitsstand |

## Snapshot

| Feld | Aktueller Stand |
|---|---|
| Stand | Nach PR #41 / Diagnose 163B und Workspace PR #209 |
| Aktueller enger Blocker | In-Game Trades bleiben `blocked-pending-evidence`; Writer-Preserve-Test ist gemerged, aber aktive Rows bleiben unbewiesen |
| Zuletzt entblockt | Item-Scope im getesteten CFRU/DPE Gen9-BPRE-Scope: Field Items, Pickup Items, Shop Items, Held Items |
| Zuletzt validiert | In-Game-Trades Guard + Non-ROM `TradeRandomizerTest` + ROM-freier `Gen3InGameTradeWriterTest` |
| Carrier-Smokes bestanden | Global Species Pool, Starter-Suboptions, Trainer Similar Strength, Wild Similar Strength/Type Restrictions |
| Danach | In-Game-Trades guarded/preserve-only Entscheidung oder weitere read-only Active-Row-Evidenz |
| Grosse offene Writer | MoveData Write, Palette Randomization, mehrere Trainer/Evolution-Sonderoptionen |
| Spaeter / P2 | Special Tutors/Text/Menu, Graphics/Sprites, Misc Tweaks |

## Statusmodell

| Status | Bedeutung |
|---|---|
| P1-supported | Im getesteten CFRU/DPE Gen9-BPRE-Scope stabil belegt. Save/Log/Output/Reload oder aequivalente Kriterien sind bestanden. |
| Supported im getesteten Scope | Praktisch freigegeben fuer den konkret getesteten CFRU/DPE Gen9-BPRE-Scope, aber nicht automatisch fuer alle ROM-Hack-Varianten. |
| Getestet im Carrier | Suboption wurde in einem bestimmten stabilen Hauptpfad getestet, aber nicht global fuer alle Kombinationen freigegeben. |
| Gefixt, Folgesmokes offen | Fix existiert, aber noch nicht durch vollstaendige Folgesmokes abgesichert. |
| Guarded / Preserve-only | Unsichere Writes werden defensiv uebersprungen, aber das Feature ist fachlich nicht als kompatibel freigegeben. |
| Read-only modelliert | Datenmodell/Risiken sind dokumentiert, aber kein Writer-Fix oder Smoke-Nachweis. |
| Write modelliert / Fix offen | Writer-Risiko ist verstanden; Implementierung oder Fix fehlt noch. |
| Blockiert | Bekannter Fehler, Mismatch, fehlender Reload oder Abbruch. |
| P2 / Out of scope | Bewusst spaeter oder nicht Teil des aktuellen P1-Scope. |
| Nicht begonnen | Noch kein Plan, Modell oder Test. |

## Scope-Modell

| Scope | Bedeutung |
|---|---|
| Global | Eigenstaendiger Featurepfad ist stabil belegt. |
| Carrier | Nur innerhalb eines Traegerpfads getestet, zum Beispiel Starter-, Wild- oder Trainer-Carrier. |
| Writer | Schreibt Daten oder repointet Datenstrukturen. |
| No-write | Aendert nur Pool, Filter, Settings oder nutzt einen Nicht-Schreibpfad. |
| Guard / Preserve | Writer schuetzt vor unsicheren Rows, aber keine Feature-Freigabe. |
| P2 | Spaeterer Scope, zum Beispiel Special Tutors, Text/Menu oder Graphics/Sprites. |

## Gesamtfortschritt nach Feature-Paketen

| Paket | Leitstatus | Stabil belegt | Carrier-tested | Blocker / Luecke | Naechster Schritt | Belege |
|---|---|---|---|---|---|---|
| General Options | Gemischt | - | Limit Pokemon, No Premature Evolutions im Starter-Carrier | Race Mode, Intro Mon offen | separater General-Smoke | 064 |
| Pokemon Traits | Gemischt | Base Stats, Species Types, Abilities, Evolution Species-only | - | Evolution Similar Strength, Evolution Same Typing | Evolution-Suboptionen isolieren | 051, 052, 059, 070, 075, 026 |
| Starters, Statics & Trades | Gemischt | Starter Species, Static/Gift Species | Starter-Filter | Starter Held Items offen; In-Game Trades guarded/preserve-only aber blockiert | guarded-Abschluss oder Active-Row-Evidenz | 065, 152-163B |
| Moves & Movesets | Gemischt | Movesets/Learnsets, Reorder Damaging | einige Filter-/Sanity-Optionen | MoveData Write offen | MoveData Write Preserve | 049, 056 |
| Foe Pokemon / Trainer | Teilweise blockiert | Trainer Species, Movesets, Held Items, Similar Strength | Similar Strength im Trainer-Carrier | Type Diversity / Type Themes, Additional Pokemon, Textnamen | Trainer-Suboptionen spaeter | 070, 075, 077 |
| Wild Pokemon | Stark | Standard/Fallback Wild, Surfing, Fishing, Rock Smash, Wild Held Items | Similar Strength, Type Restrictions im Wild-Carrier | Catch Rate, Catch Em All, Level Modifier offen | spaeter Wild-Level/Catch | 075 |
| TM/HMs & Tutors | Stark, Suboptionen offen | TM/HM 128-Slot, Tutor 152-Slot, Compatibility, Sanity | Filter-/Follow-Suboptionen teilweise Carrier | Special Tutors/Text/Menu out of scope | normale Suboptionen spaeter testen | 038, 040, 049 |
| Items | Supported im getesteten Scope | Field Items, Pickup Items, Shop Items, Held Items | - | Sonderoptionen nur bei neuer Evidenz | Regression/Statuspflege | Item-Scope Abschlussdiagnosen |
| Types | Stark / getestet | TypeEffectiveness Random/Balanced/Inverse/Update/Add Immunities | - | keine enge TypeChart-Luecke bekannt | Statuspflege/Regression | 066, 068 |
| Graphics | Write modelliert / P2 gemischt | Palette Safety / unchanged | - | echte Palette Randomization, Custom Player Graphics | Palette Fix spaeter | 058 |
| Misc Tweaks | Nicht begonnen | - | - | alle Misc Tweaks offen | Misc-Inventar | offen |

## GUI-Feature-Gruppen

| GUI-Gruppe | Hauptstatus | Was funktioniert? | Was ist nur Carrier-tested? | Offen / blockiert | Naechster Schritt |
|---|---|---|---|---|---|
| General Options | Teilweise getestet | - | Limit Pokemon, No Premature Evolutions | Race Mode, Intro Mon | General-Smoke spaeter |
| Pokemon Base Stats | P1-supported | Random/Shuffle Base Stats | Follow Evolutions nur geplant | EXP Curves, Gen Update offen | Suboptionen spaeter |
| Pokemon Types | P1-supported fuer Species Types | Type Read/Write | Force Dual Types geplant | TypeChart separat, inzwischen getestet | keine enge Luecke |
| Pokemon Abilities | P1-supported | Ability1/2 + Hidden Ability | Ban-/Filter-Suboptionen geplant | - | Suboption-Smoke spaeter |
| Evolutions | Teilweise supported, Suboptionen blockiert | normale Evolution Randomization, Species-only | einige Filter geplant | Similar Strength, Same Typing | eigener Evolution-Suboption-Block |
| Starters | Stark / Carrier-tested | Starter Species | Basic/Type/BST/Legendary Filter | Starter Held Items | spaeter Held Items |
| Static/Gift | P1-supported fuer Species | Static/Gift Species | Similar Strength im Scope | Level Modifier/Fix Music offen | spaeter |
| In-Game Trades | Guarded / blockiert | Null-/Invalid-Species Guard, Non-ROM TradeRandomizerTest, ROM-freier Gen3 Writer-Preserve-Test | - | keine validen aktiven Rows, kein Species-Write-Smoke, kein Text/Nickname/OT/IV/Item | guarded-Abschluss oder Active-Row-Evidenz |
| Trainer | Teilweise blockiert | Species, Movesets, Held Items, Similar Strength | Similar Strength | Type Diversity / Type Themes | spaeter enger Blocker |
| Wild | Stark | Standard/Fallback Wild, Surfing, Fishing, Rock Smash, Held Items | Similar Strength, Type Restrictions | Catch Rate, Catch Em All, Level Modifier | spaeter |
| Movesets | P1-supported | Learnsets/Movesets/Reorder/Sanity | Filter-Suboptionen | - | Regression spaeter |
| MoveData | Write modelliert | Read vorhanden | - | Power/Accuracy/PP/Type/Names/Update Write offen | MoveData Writer |
| TM/HM | P1-supported, Suboptionen offen | TM/HM moves + compatibility | Field/Filter/Follow-Suboptionen | - | spaeter |
| Tutors | P1-supported normal, P2 Special | normal tutor moves + compatibility | filter/follow-suboptions | Special Tutors/Text/Menu | P2 |
| Items | Supported im getesteten Scope | Field Items, Pickup Items, Shop Items, Held Items | - | weitere Sonderoptionen nur bei neuer Evidenz | Regression/Statuspflege |
| TypeEffectiveness | Gefixt + Smokes bestanden | Random/Balanced/Inverse/Update/Add Immunities | - | keine enge Luecke | Statuspflege |
| Palettes | Write modelliert | unchanged/safety path | - | echte Palette Randomization | Palette Fix |
| Graphics/Sprites | P2 / Nicht begonnen | - | - | Custom Player Graphics, Sprites | P2 |
| Misc Tweaks | Nicht begonnen | - | - | 12 Tweaks offen | Inventar |

## Vollstaendige Feature-Liste

Diese Tabelle listet alle aktuell erfassten FVX-Features einmal kompakt auf. Sie ist bewusst nicht nach Unterabschnitten getrennt, damit der gesamte Scope in einer einzigen Liste sichtbar ist.

| Nr. | Feature-ID | Bereich | Feature | Dashboard-Status | Scope |
|---:|---|---|---|---|---|
| 1 | `FVX-GEN-001` | General Options | Limit Pokemon | Getestet im Carrier | Carrier |
| 2 | `FVX-GEN-002` | General Options | No Premature Evolutions | Getestet im Carrier | Carrier |
| 3 | `FVX-GEN-003` | General Options | No Random Intro Mon | Nicht begonnen | No-write / P2 offen |
| 4 | `FVX-GEN-004` | General Options | Race Mode | Nicht begonnen | No-write |
| 5 | `FVX-TRAIT-001` | Pokemon Traits | Base Stats: Shuffle / Random | P1-supported | Global |
| 6 | `FVX-TRAIT-002` | Pokemon Traits | Base Stats: Follow Evolutions | Plan erstellt | Carrier / Filter |
| 7 | `FVX-TRAIT-003` | Pokemon Traits | Randomize Added Stats on Evolution | Plan erstellt | Carrier / Filter |
| 8 | `FVX-TRAIT-004` | Pokemon Traits | Update Base Stats to Generation | Nicht begonnen | Writer |
| 9 | `FVX-TRAIT-005` | Pokemon Traits | Standardize EXP Curves | Nicht begonnen | Writer |
| 10 | `FVX-TRAIT-006` | Pokemon Traits | Pokemon Types randomisieren | P1-supported | Global |
| 11 | `FVX-TRAIT-007` | Pokemon Traits | Force Dual Types | Plan erstellt | Carrier / Filter |
| 12 | `FVX-TRAIT-008` | Pokemon Traits | Pokemon Abilities randomisieren | P1-supported | Global |
| 13 | `FVX-TRAIT-009` | Pokemon Traits | Abilities: Follow Evolutions | Plan erstellt | Carrier / Filter |
| 14 | `FVX-TRAIT-010` | Pokemon Traits | Abilities: Allow Wonder Guard | Plan erstellt | Filter |
| 15 | `FVX-TRAIT-011` | Pokemon Traits | Abilities: Combine Duplicate Abilities | Plan erstellt | Filter |
| 16 | `FVX-TRAIT-012` | Pokemon Traits | Abilities: Ensure Two Abilities | Plan erstellt | Filter |
| 17 | `FVX-TRAIT-013` | Pokemon Traits | Abilities: Ban Trapping Abilities | Plan erstellt | Filter |
| 18 | `FVX-TRAIT-014` | Pokemon Traits | Abilities: Ban Negative Abilities | Plan erstellt | Filter |
| 19 | `FVX-TRAIT-015` | Pokemon Traits | Abilities: Ban Bad Abilities | Plan erstellt | Filter |
| 20 | `FVX-TRAIT-016` | Pokemon Traits | Pokemon Evolutions randomisieren | P1-supported | Global |
| 21 | `FVX-TRAIT-017` | Pokemon Traits | Evolutions: Random Every Level | Plan erstellt | Carrier / Filter |
| 22 | `FVX-TRAIT-018` | Pokemon Traits | Evolutions: Similar Strength | Blockiert | Writer / Filter |
| 23 | `FVX-TRAIT-019` | Pokemon Traits | Evolutions: Same Typing | Blockiert | Writer / Filter |
| 24 | `FVX-TRAIT-020` | Pokemon Traits | Evolutions: Limit to Three Stages | Plan erstellt | Filter |
| 25 | `FVX-TRAIT-021` | Pokemon Traits | Evolutions: No Convergence | Plan erstellt | Filter |
| 26 | `FVX-TRAIT-022` | Pokemon Traits | Evolutions: Force Change | Plan erstellt | Filter |
| 27 | `FVX-TRAIT-023` | Pokemon Traits | Evolutions: Force Growth | Plan erstellt | Filter |
| 28 | `FVX-TRAIT-024` | Pokemon Traits | Change Impossible Evolutions | Nicht begonnen | Writer |
| 29 | `FVX-TRAIT-025` | Pokemon Traits | Make Evolutions Easier | Nicht begonnen | Writer |
| 30 | `FVX-TRAIT-026` | Pokemon Traits | Use Estimated Evolution Levels | Nicht begonnen | Writer |
| 31 | `FVX-TRAIT-027` | Pokemon Traits | Remove Time-Based Evolutions | Nicht begonnen | Writer |
| 32 | `FVX-TRAIT-028` | Pokemon Traits | EXP-/Legendary-Kurven-Sonderfaelle | Nicht begonnen | Writer / Filter |
| 33 | `FVX-SST-001` | Starters, Statics & Trades | Starter Pokemon: Custom | P1-supported | Global |
| 34 | `FVX-SST-002` | Starters, Statics & Trades | Starter Pokemon: Random completely | P1-supported | Global |
| 35 | `FVX-SST-003` | Starters, Statics & Trades | Starter Pokemon: Random basic with 2 evolutions | Getestet im Carrier | Carrier |
| 36 | `FVX-SST-004` | Starters, Statics & Trades | Starter Pokemon: Random any basic | Getestet im Carrier | Carrier |
| 37 | `FVX-SST-005` | Starters, Statics & Trades | Starter Type Restrictions | Getestet im Carrier | Carrier |
| 38 | `FVX-SST-006` | Starters, Statics & Trades | Starter: Don't Use Legendaries | Getestet im Carrier | Carrier |
| 39 | `FVX-SST-007` | Starters, Statics & Trades | Starter Held Items randomisieren | Nicht begonnen | Writer |
| 40 | `FVX-SST-008` | Starters, Statics & Trades | Starter Held Items: Ban Bad Items | Nicht begonnen | Writer / Filter |
| 41 | `FVX-SST-009` | Starters, Statics & Trades | Starter BST-Min/Max | Getestet im Carrier | Carrier |
| 42 | `FVX-SST-010` | Starters, Statics & Trades | Static Pokemon: Swap Legendaries & Standards | P1-supported | Global |
| 43 | `FVX-SST-011` | Starters, Statics & Trades | Static Pokemon: Random completely | P1-supported | Global |
| 44 | `FVX-SST-012` | Starters, Statics & Trades | Static Pokemon: Random similar strength | P1-supported | Global |
| 45 | `FVX-SST-013` | Starters, Statics & Trades | Static Pokemon: Level Modifier / Fix Music | Nicht begonnen | Writer |
| 46 | `FVX-SST-014` | Starters, Statics & Trades | In-Game Trades: Given/Requested species | Guarded / blocked-pending-evidence | Guard / Writer |
| 47 | `FVX-SST-015` | Starters, Statics & Trades | In-Game Trades: Nickname/OT/IV/Item | Blockiert / nicht freigegeben | Writer / Text |
| 48 | `FVX-MOVE-001` | Moves & Movesets | Randomize Move Power | Write modelliert / Fix offen | Writer |
| 49 | `FVX-MOVE-002` | Moves & Movesets | Randomize Move Accuracy | Write modelliert / Fix offen | Writer |
| 50 | `FVX-MOVE-003` | Moves & Movesets | Randomize Move PP | Write modelliert / Fix offen | Writer |
| 51 | `FVX-MOVE-004` | Moves & Movesets | Randomize Move Types | Write modelliert / Fix offen | Writer |
| 52 | `FVX-MOVE-005` | Moves & Movesets | Randomize Move Names | Write modelliert / Fix offen | Writer / Text |
| 53 | `FVX-MOVE-006` | Moves & Movesets | Update Moves to Generation | Write modelliert / Fix offen | Writer |
| 54 | `FVX-MOVE-007` | Moves & Movesets | Pokemon Movesets randomisieren | P1-supported | Global |
| 55 | `FVX-MOVE-008` | Moves & Movesets | Guaranteed Level 1 Moves | Plan erstellt | Carrier / Filter |
| 56 | `FVX-MOVE-009` | Moves & Movesets | Reorder Damaging Moves | P1-supported | Global |
| 57 | `FVX-MOVE-010` | Moves & Movesets | No Game-Breaking Moves | Plan erstellt | Filter |
| 58 | `FVX-MOVE-011` | Moves & Movesets | Force % Good Damaging Moves | Plan erstellt | Filter |
| 59 | `FVX-FOE-001` | Foe Pokemon | Trainer Pokemon randomisieren | P1-supported | Global |
| 60 | `FVX-FOE-002` | Foe Pokemon | Better Movesets: Boss Trainers | P1-supported | Global |
| 61 | `FVX-FOE-003` | Foe Pokemon | Better Movesets: Important Trainers | P1-supported | Global |
| 62 | `FVX-FOE-004` | Foe Pokemon | Better Movesets: Regular Trainers | P1-supported | Global |
| 63 | `FVX-FOE-005` | Foe Pokemon | Additional Pokemon: Boss Trainers | Nicht begonnen | Writer |
| 64 | `FVX-FOE-006` | Foe Pokemon | Additional Pokemon: Important Trainers | Nicht begonnen | Writer |
| 65 | `FVX-FOE-007` | Foe Pokemon | Additional Pokemon: Regular Trainers | Nicht begonnen | Writer |
| 66 | `FVX-FOE-008` | Foe Pokemon | Trainer Held Items | P1-supported | Global |
| 67 | `FVX-FOE-009` | Foe Pokemon | Force Diverse Types / Type Themes | Blockiert | Carrier / Filter |
| 68 | `FVX-FOE-010` | Foe Pokemon | Pokemon League Has Unique Pokemon | Nicht begonnen | Filter |
| 69 | `FVX-FOE-011` | Foe Pokemon | Battle Style randomisieren | Nicht begonnen | Writer |
| 70 | `FVX-FOE-012` | Foe Pokemon | Rival Carries Starter Through Game | Nicht begonnen | Carrier |
| 71 | `FVX-FOE-013` | Foe Pokemon | Randomize Trainer Names / Class Names | Nicht begonnen | Text |
| 72 | `FVX-FOE-014` | Foe Pokemon | Trainers Evolve Their Pokemon + Level Modifier | Nicht begonnen | Writer |
| 73 | `FVX-WILD-001` | Wild Pokemon | Randomize Wild Pokemon | P1-supported | Global |
| 74 | `FVX-WILD-002` | Wild Pokemon | Replacements Per Species | P1-supported | Global |
| 75 | `FVX-WILD-003` | Wild Pokemon | Split by Encounter Types | P1-supported | Global |
| 76 | `FVX-WILD-004` | Wild Pokemon | Type Restrictions | Getestet im Carrier | Carrier |
| 77 | `FVX-WILD-005` | Wild Pokemon | Evolution Restrictions | Plan erstellt | Filter |
| 78 | `FVX-WILD-006` | Wild Pokemon | Don't Use Legendaries | P1-supported | Global |
| 79 | `FVX-WILD-007` | Wild Pokemon | Set Minimum Catch Rate | Nicht begonnen | Writer |
| 80 | `FVX-WILD-008` | Wild Pokemon | Randomize Wild Held Items | P1-supported | Global |
| 81 | `FVX-WILD-009` | Wild Pokemon | Ban Bad Held Items | P1-supported | Global |
| 82 | `FVX-WILD-010` | Wild Pokemon | Catch Em All Mode | Nicht begonnen | Filter / Writer |
| 83 | `FVX-WILD-011` | Wild Pokemon | Similar Strength | Getestet im Carrier | Carrier |
| 84 | `FVX-WILD-012` | Wild Pokemon | Balance Low Level Encounters + Level Modifier | Nicht begonnen | Writer |
| 85 | `FVX-TM-001` | TM/HMs & Tutors | TM Moves randomisieren | P1-supported | Global |
| 86 | `FVX-TM-002` | TM/HMs & Tutors | Keep Field Move TMs | Plan erstellt | Filter |
| 87 | `FVX-TM-003` | TM/HMs & Tutors | TM No Game-Breaking Moves | Plan erstellt | Filter |
| 88 | `FVX-TM-004` | TM/HMs & Tutors | TM Force % Good Damaging Moves | Plan erstellt | Filter |
| 89 | `FVX-TM-005` | TM/HMs & Tutors | TM/HM Compatibility randomisieren | P1-supported | Global |
| 90 | `FVX-TM-006` | TM/HMs & Tutors | TM/Levelup Move Sanity | P1-supported | Global |
| 91 | `FVX-TM-007` | TM/HMs & Tutors | TM Compatibility Follow Evolutions | Plan erstellt | Filter |
| 92 | `FVX-TM-008` | TM/HMs & Tutors | Full HM Compatibility | Plan erstellt | Filter |
| 93 | `FVX-TM-009` | TM/HMs & Tutors | Move Tutor Moves randomisieren | P1-supported | Global |
| 94 | `FVX-TM-010` | TM/HMs & Tutors | Keep Field Move Tutors | Plan erstellt | Filter |
| 95 | `FVX-TM-011` | TM/HMs & Tutors | Tutor No Game-Breaking Moves | Plan erstellt | Filter |
| 96 | `FVX-TM-012` | TM/HMs & Tutors | Tutor Force % Good Damaging Moves | Plan erstellt | Filter |
| 97 | `FVX-TM-013` | TM/HMs & Tutors | Tutor Compatibility randomisieren | P1-supported | Global |
| 98 | `FVX-TM-014` | TM/HMs & Tutors | Tutor/Levelup Sanity | P1-supported | Global |
| 99 | `FVX-TM-015` | TM/HMs & Tutors | Tutor Compatibility Follow Evolutions | Plan erstellt | Filter |
| 100 | `FVX-ITEM-001` | Items | Field Items Shuffle | Supported im getesteten Scope | Writer |
| 101 | `FVX-ITEM-002` | Items | Field Items Random | Supported im getesteten Scope | Writer |
| 102 | `FVX-ITEM-003` | Items | Field Items Random even distribution | Supported im getesteten Scope | Writer |
| 103 | `FVX-ITEM-004` | Items | Field Items Ban Bad Items | Supported im getesteten Scope | Writer / Filter |
| 104 | `FVX-ITEM-005` | Items | Shop Items Shuffle | Supported im getesteten Scope | Writer |
| 105 | `FVX-ITEM-006` | Items | Shop Items Random | Supported im getesteten Scope | Writer |
| 106 | `FVX-ITEM-007` | Items | Shop Item Bans | Supported im getesteten Scope | Writer / Filter |
| 107 | `FVX-ITEM-008` | Items | Guarantee Evolution/X Items | Supported im getesteten Scope | Writer / Filter |
| 108 | `FVX-ITEM-009` | Items | Balance Shop Prices / Cheap Rare Candies | Supported im getesteten Scope | Writer |
| 109 | `FVX-ITEM-010` | Items | Pickup Items Random / Ban Bad Items | Supported im getesteten Scope | Writer |
| 110 | `FVX-TYPE-001` | Types | Type Effectiveness Random/Balanced/Keep Identities/Inverse | Getestet | Writer |
| 111 | `FVX-TYPE-002` | Types | Add Random Immunities | Getestet | Writer |
| 112 | `FVX-TYPE-003` | Types | Update Type Effectiveness | Getestet | Writer |
| 113 | `FVX-GFX-001` | Graphics | Pokemon Palettes Random | Write modelliert / Fix offen | Writer |
| 114 | `FVX-GFX-002` | Graphics | Palettes: Follow Types | Write modelliert / Fix offen | Writer / Filter |
| 115 | `FVX-GFX-003` | Graphics | Palettes: Follow Evolutions | Write modelliert / Fix offen | Writer / Filter |
| 116 | `FVX-GFX-004` | Graphics | Palettes: Shiny From Normal | Write modelliert / Fix offen | Writer |
| 117 | `FVX-GFX-005` | Graphics | Custom Player Graphics | P2 / Nicht begonnen | P2 |
| 118 | `FVX-GFX-006` | Graphics | Character to Replace | P2 / Nicht begonnen | P2 |
| 119 | `FVX-MISC-001` | Misc Tweaks | Fastest Text | Nicht begonnen | Writer / Patch |
| 120 | `FVX-MISC-002` | Misc Tweaks | Running Shoes Indoors | Nicht begonnen | Writer / Patch |
| 121 | `FVX-MISC-003` | Misc Tweaks | Randomize PC Potion | Nicht begonnen | Writer / Patch |
| 122 | `FVX-MISC-004` | Misc Tweaks | Give National Dex at Start | Nicht begonnen | Writer / Patch |
| 123 | `FVX-MISC-005` | Misc Tweaks | Fast Egg Hatching | Nicht begonnen | Writer / Patch |
| 124 | `FVX-MISC-006` | Misc Tweaks | Lower Case Pokemon Names | Nicht begonnen | Writer / Patch |
| 125 | `FVX-MISC-007` | Misc Tweaks | Randomize Catching Tutorial | Nicht begonnen | Writer / Patch |
| 126 | `FVX-MISC-008` | Misc Tweaks | Ban Lucky Egg | Nicht begonnen | Writer / Patch |
| 127 | `FVX-MISC-009` | Misc Tweaks | Balance Static Pokemon Levels | Nicht begonnen | Writer / Patch |
| 128 | `FVX-MISC-010` | Misc Tweaks | Run Without Running Shoes | Nicht begonnen | Writer / Patch |
| 129 | `FVX-MISC-011` | Misc Tweaks | Reusable TMs | Nicht begonnen | Writer / Patch |
| 130 | `FVX-MISC-012` | Misc Tweaks | Forgettable HMs | Nicht begonnen | Writer / Patch |

## In-Game-Trades Status nach Diagnose 163B

| Thema | Status |
|---|---|
| Locator/Table Model | verstanden, aber valide aktive Rows nicht bestaetigt |
| Preserve/Skip-Policy | dokumentiert; unsichere Rows nicht schreiben |
| Null-/Invalid-Species Guard | in UPR-FVX gemerged und im Workspace gepinnt |
| `TradeRandomizerTest` Non-ROM Harness | vorhanden und dokumentiert |
| Gen3 Writer-Preserve-Test | UPR-FVX PR #41 gemerged; ROM-freier `Gen3InGameTradeWriterTest` vorhanden |
| Species-Write-Smoke | blockiert |
| Text/Nickname/OT/IV/Held Item | blockiert / nicht freigegeben |
| Kompatibilitaetsklassifikation | `blocked-pending-evidence` |

## Wichtige Belegkette In-Game-Trades

| Diagnose / PR | Ergebnis |
|---|---|
| Diagnose 152 | erster Scope-Diagnostic-Blocker: `tradeScanSuccessful=false`, null/invalid/placeholder Species |
| Diagnose 154 | Locator-/Table-Model verstanden, aber valide aktive Rows nicht bestaetigt |
| Diagnose 155 | Active-Row-Kandidaten bleiben blocked; unsupported-dummy plausibel, aber nicht bewiesen |
| Diagnose 156 | Preserve/Skip-Policy: keine unsicheren Rows schreiben |
| Diagnose 157 | Null-request Guard-Plan |
| UPR-FVX PR #39 / Diagnose 158B | Guard implementiert und Workspace-Gitlink gepinnt |
| Diagnose 159 | Code-Review: `review-pass-with-risks` |
| Diagnose 160 | Non-ROM Harness-Plan: `harness-plan-ready` |
| UPR-FVX PR #40 / Diagnose 161B | `TradeRandomizerTest` Non-ROM Harness gemerged und gepinnt |
| UPR-FVX PR #41 / Diagnose 163B | `Gen3InGameTradeWriterTest` Writer-Preserve-Test gemerged und gepinnt |
| Diagnose 162 / PR #207 | Writer-Preserve-Test-Plan: `writer-test-plan-ready` |

## Offene Blocker

| Prioritaet | Blocker | Status | Betroffene Feature-IDs | Ursache / Symptom | Naechster Schritt | Belege |
|---|---|---|---|---|---|---|
| P0/P1 | In-Game Trades | Guarded / `blocked-pending-evidence` | `FVX-SST-014`, `FVX-SST-015` | keine validen aktiven Rows; Guard und Non-ROM-Tests vorhanden, aber kein Species-Write-Smoke | guarded-Abschluss oder weitere Active-Row-Evidenz | 152-163B |
| P1 | Evolution Similar Strength | Blockiert | `FVX-TRAIT-018` | Mismatch-/Bad-Egg-Slice aus bisherigem Similar-Strength-Smoke | separater Evolution-Similar-Strength-Block | 070, 075 |
| P1 | Evolution Same Typing | Blockiert | `FVX-TRAIT-019` | Same-Type-Evolution-Slice nicht freigegeben | separater Evolution-Same-Typing-Block | 070, 075 |
| P1 | MoveData Write | Write modelliert / Fix offen | `FVX-MOVE-001` bis `FVX-MOVE-006` | Writer fuer moderne MoveData-Felder offen | MoveData Preserve Writer | 056 |
| P1 | Trainer Type Diversity / Type Themes | Blockiert / gegen neue Roadmap pruefen | `FVX-FOE-009` | Diagnose 077 isoliert `primaryType == null` in `EnumSet<Type>` bei `updateUsedTypes(...)` als wahrscheinliche Ursache | bei Trainer-Fortsetzung eng gegateter Fixblock | 070, 075, 077 |
| P1 | Palette Randomization | Write modelliert / Fix offen | `FVX-GFX-001` bis `FVX-GFX-004` | compressed/shared/repointing risks | Palette Preserve/Repoint Fix | 058 |
| P2 | Special Tutors/Text/Menu | P2 / Out of scope | Tutor-Sonderpfade | Text/Menu/Special-Tutor-Logik ist nicht normaler Tutor-Scope | spaeter P2-Modell | 047, 060 |
| P2 | Graphics/Sprites | P2 / Nicht begonnen | `FVX-GFX-005`, `FVX-GFX-006` | Custom Player Graphics / Sprites getrennt von Paletten | spaeter Graphics-Modell | 058 |
| P2 | Misc Tweaks | Nicht begonnen | `FVX-MISC-001` bis `FVX-MISC-012` | Misc-Inventar offen | spaeter Inventar | offen |

## Naechste empfohlene Arbeitspakete

| Reihenfolge | Arbeitspaket | Ziel | Warum jetzt? | Erwartetes Ergebnis |
|---:|---|---|---|---|
| 1 | Entscheidung In-Game-Trades | guarded/preserve-only abschliessen oder weitere Evidenz suchen | Mutation- und Writer-Preserve-Guards sind ROM-frei getestet, aktive Rows aber unbewiesen | klare Klassifikation fuer diesen Scope |
| 2 | Evolution Similar Strength | blockierte Evolution-Suboption isolieren | direkt danach offen | `FVX-TRAIT-018` geklaert |
| 3 | Evolution Same Typing | Same-Type-Evolution-Slice isolieren | direkt danach offen | `FVX-TRAIT-019` geklaert |
| 4 | MoveData Write | Power/Accuracy/PP/Type/Update Moves absichern | grosser offener Moves-Tab-Writer | `FVX-MOVE-001` bis `FVX-MOVE-006` hochstufen |
| 5 | Palette Randomization | echte Palettenaenderungen absichern | grosser Graphics/Palette-Writer | `FVX-GFX-001` bis `FVX-GFX-004` hochstufen |
| 6 | Special Tutors/Text/Menu | P2-Sonderpfade modellieren | nicht normaler Tutor-Tabellenpfad | P2-Entscheidung |
| 7 | Graphics/Sprites | Custom Player Graphics/Sprites modellieren | getrennt von Paletten | P2-Entscheidung |

## Zuletzt abgeschlossene PRs / Diagnosen

| Diagnose / PR | Bereich | Ergebnis | Statuswirkung |
|---|---|---|---|
| 163B / PR #41 | In-Game Trades Writer-Preserve Follow-up | UPR-FVX PR #41 gepinnt; `Gen3InGameTradeWriterTest` vorhanden | Writer-Preserve-Decision ROM-frei getestet |
| 162 / PR #207 | In-Game Trades Writer-Preserve-Test-Plan | `writer-test-plan-ready`; ROM-freier `:romio:test` empfohlen | naechster enger optionaler In-Game-Trades-Test vorbereitet |
| 161B / PR #206 | In-Game Trades Non-ROM Harness Follow-up | UPR-FVX PR #40 gepinnt; `TradeRandomizerTest` vorhanden | Mutation-Skip-Guard ROM-frei getestet |
| 160 / PR #205 | In-Game Trades Non-ROM Harness Plan | `harness-plan-ready` | Test-Scope fuer `TradeRandomizer` festgelegt |
| 159 / PR #204 | In-Game Trades Guard Code Review | `review-pass-with-risks` | Guard-Reihenfolge fachlich geprueft |
| 158B / PR #203 | In-Game Trades Guard Follow-up | UPR-FVX PR #39 gepinnt | Null-/Invalid-Species Guard dokumentiert |
| 152-157 | In-Game Trades Diagnosekette | blocked-pending-evidence, Preserve/Skip-Policy, Guard-Plan | keine Species-Write-Freigabe |
| 077 | Trainer Type Diversity Code Diagnosis | wahrscheinliche Null-Type-Ursache in `updateUsedTypes(...)` eingegrenzt | enger Fixblock vorbereitet |
| 075 | Wild Similar Strength / Wild Type Restrictions | Wild-Carrier-Nullslot-Fix entblockt Wild-Slices | `FVX-WILD-004` und `FVX-WILD-011` im Wild-Carrier stabil |
| 068 | TypeEffectiveness Follow-up Smokes | Balanced, Keep Identities, Inverse, Add Immunities, Update Type Effectiveness bestanden | `FVX-TYPE-001` bis `FVX-TYPE-003` getestet |
| 066 | TypeChart Preserve Effectiveness Fix | Random TypeEffectiveness mit Fairy-Reload und Reload-Kriterien bestanden | TypeChart Fix validiert |
| 065 | Starter Suboptions Smoke | Basic/2 evolutions, any basic, type restrictions, no legendaries, BST | Starter-Suboptionen carrier-tested |
| 064 | Global Species Pool Smoke | Limit Pokemon / No Premature im Starter Carrier | General Options teilweise carrier-tested |
| 060 | GUI Suboptions Regression Matrix | Suboptionen klassifiziert | Grundlage fuer Regression-Smoke-Plan |
| 056-059 | Writer-Modelle | MoveData, Items, Palettes, TypeChart modelliert | grosse Writer priorisiert |

## Carrier-tested, aber nicht global

| Feature-ID | Feature | Carrier | Ergebnis im Carrier | Nicht automatisch abgedeckt |
|---|---|---|---|---|
| `FVX-GEN-001` | Limit Pokemon | Starter-Carrier | bestanden | Wild/Trainer/Evolution-Kombinationen mit Limit Pokemon |
| `FVX-GEN-002` | No Premature Evolutions | Starter-Carrier | bestanden | globale Poolauswirkungen auf Wild/Trainer/Evolution |
| `FVX-SST-003` | Starter Random basic with 2 evolutions | Starter-Species-Writer | bestanden | Starter Held Items |
| `FVX-SST-004` | Starter Random any basic | Starter-Species-Writer | bestanden | Starter Held Items |
| `FVX-SST-005` | Starter Type Restrictions | Starter-Species-Writer | bestanden | andere Type-Restriction-Nutzer |
| `FVX-SST-006` | Starter Don't Use Legendaries | Starter-Species-Writer | bestanden | globale Legendary-Filter in Wild/Trainer/Evolutions |
| `FVX-SST-009` | Starter BST Min/Max | Starter-Species-Writer | bestanden | globale Similar-Strength-Filter |
| `FVX-WILD-004` | Wild Type Restrictions | Wild-Carrier | nach Nullslot-Fix bestanden | Trainer Type Themes / Evolution Same Typing |
| `FVX-WILD-011` | Wild Similar Strength | Wild-Carrier | nach Nullslot-Fix bestanden | Trainer/Evolution Similar Strength |
| n/a | Trainer Similar Strength | Trainer-Species-Carrier | bestanden | Trainer Type Diversity / Type Themes |

## Pflege-Regeln

Nach jedem Randomizer-Arbeitsblock maximal diese Stellen aktualisieren:

1. `Snapshot` aktualisieren.
2. Eine betroffene Zeile in `Gesamtfortschritt nach Feature-Paketen` aktualisieren.
3. Die betroffene Zeile in `Vollstaendige Feature-Liste` aktualisieren.
4. `Offene Blocker` aktualisieren.
5. `Zuletzt abgeschlossene PRs / Diagnosen` um eine Zeile ergaenzen.
6. `Carrier-tested, aber nicht global` aktualisieren, falls ein Smoke nur Carrier-Scope hat.

Dieses Dashboard bleibt die schnelle Lesedatei. Details gehoeren in die Diagnoseprotokolle unter `08_tests/randomizer/` und in die Feature-Matrix `01_docs/randomizer/fvx-feature-coverage.md`.

## Sicherheitsregeln

- Keine ROMs, Saves, Emulator States, Builds, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, Hashes, Secrets oder `.env`-Inhalte dokumentieren.
- Keine Detailwerte aus lokalen privaten Laeufen aufnehmen, wenn sie private Artefakte offenlegen koennten.
- Diagnose-IDs und PR-Nummern reichen als Nachweisanker.
