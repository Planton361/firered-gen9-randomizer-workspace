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
| Stand | Nach Workspace PR #264 / UPR-FVX PR #97 |
| UPR-FVX-Pin im Workspace | `51d52a03235664154549105003dadfb45c76d0d0` |
| Breites GUI-Profil | GUI Working Settings Matrix passed: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets Random completely, Trainer Movesets, Trainer Names, Field Items basic, Abilities, TM/HM, Tutors, Shops, Pickup, In-Game Trades, Static Pokemon, Type Effectiveness, Base Stats und Move Data |
| Stable Visual Profile | Passed im kurzen lokalen Smoke; Trainer Class Names, Evolution Randomization und Special-Wild bleiben OFF |
| Zuletzt entblockt | Starter Pokemon / Oak-Lab Rival Sync passed: Oak-Lab Rival nutzt den randomisierten Counter-Slot |
| Aktuelle Caveats | Trainer Class Names bleibt textlabel-only; Special-Wild/Day-Night/Swarms bleiben out-of-scope; `Rival Carries Starter Through Game` bleibt ungetestet |
| Keine P1-Promotion | Aktuelle Updates sind Workspace-/Smoke-Status, keine neue P1-Freigabe |
| Naechster sinnvoller Block | Stable Visual Profile + Starter Pokemon laenger samplen oder `Rival Carries Starter Through Game` separat isolieren |

## Statusmodell

| Status | Bedeutung |
|---|---|
| P1-supported | Im getesteten CFRU/DPE Gen9-BPRE-Scope stabil belegt. Save/Log/Output/Reload oder aequivalente Kriterien sind bestanden. |
| Supported im getesteten Scope | Praktisch freigegeben fuer den konkret getesteten CFRU/DPE Gen9-BPRE-Scope, aber nicht automatisch fuer alle ROM-Hack-Varianten. |
| Getestet im Carrier | Suboption wurde in einem bestimmten stabilen Hauptpfad getestet, aber nicht global fuer alle Kombinationen freigegeben. |
| tested-non-rom | ROM-frei per Unit-/Harness-Test belegt, aber ohne ROM-Smoke/Reload noch nicht P1-supported. |
| make-easier-plan-ready | `FVX-TRAIT-025` ist in ROM-freie Condense-Logik und separaten Happiness-Byte-Patch-Scope getrennt geplant. |
| decision-review-ready | Methoden-/Mapping-Decision ist read-only fachlich geprueft und bereit fuer einen kleinen ROM-freien Decision-Test. |
| methods-plan-ready | Methoden-/Improvement-Scope ist read-only geplant, aber noch nicht per Non-ROM-Test, Writer oder Reload belegt. |
| Gefixt, Folgesmokes offen | Fix existiert, aber noch nicht durch vollstaendige Folgesmokes abgesichert. |
| Guarded / Preserve-only | Unsichere Writes werden defensiv uebersprungen, aber das Feature ist fachlich nicht als kompatibel freigegeben. |
| Working-matrix passed | In der lokalen GUI Working Settings Matrix fuer den aktuellen CFRU/DPE-Gen9-Scope bestanden; keine automatische globale P1-Promotion. |
| Stable-profile passed | Im lokalen Stable Visual Profile kurz gesmoked und ohne Blocker beobachtet; kein Full-Playthrough und keine P1-Promotion. |
| Passed with caveat | Im getesteten Scope nutzbar, aber mit dokumentierter Grenze oder Darstellungsabweichung. |
| Textlabel-only | Aendert sichtbare Textlabels, aber nicht zwingend dahinterliegende IDs/Sprites. |
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
| General Options | Gemischt | - | Limit Pokemon, No Premature Evolutions im Starter-Carrier | Race Mode, Intro Mon offen; nicht Teil des Stable Visual Profile | separater General-Smoke | 064 |
| Pokemon Traits | Working-matrix passed fuer Kernteile | Base Stats, Species Types, Abilities; Evolutions unchanged preserved | Evolution Similar Strength und Same Typing diagnosis-ready; `017/020-023`, `024/027`, `025A` tested-non-rom; `026` helper-only | Evolution Randomization/Methoden-Slices bleiben separat; Base-Stats-Log kann Ability-Namen kuerzen, ingame OK | Evolution-Randomization isolieren oder Stable-Profil laenger samplen | 189, 190, 191 |
| Starters, Statics & Trades | Working-matrix passed / Starter Sync passed | Starter Pokemon Random completely + Oak-Lab Rival Counter-Sync; Static Pokemon; In-Game Trades ohne `NEW GIVEN = ?` | Starter-Filter | Starter Held Items offen; `Rival Carries Starter Through Game` ungetestet; Static null placeholders bleiben null | Stable Visual Profile + Starter Pokemon samplen; Full-Rival-Carry separat | 190, 192 |
| Moves & Movesets | Working-matrix passed | Pokemon Movesets, Trainer Movesets, Move Data Power/Accuracy/PP/Type/Names | einige Filter-/Sanity-Optionen | Update Moves / Text-Encoding-Detailpfade nicht global P1-promoted | laengeres Stable-Profil-Sampling | 190, 191 |
| Foe Pokemon / Trainer | Working-matrix passed mit Caveat | Trainer Pokemon core, Trainer Movesets, Trainer Names | Similar Strength im Trainer-Carrier; Additional Pokemon, Type Diversity / Type Themes, Special Rules, Battle Style tested-non-rom | Trainer Class Names textlabel-only; Sprite/Class-ID mismatch erwartbar; `Rival Carries Starter Through Game` ungetestet | Trainer Class Names OFF lassen oder Class Assignment separat planen | 190, 191 |
| Wild Pokemon | Working-matrix passed | Standard/Fallback Wild, normale Encounter-Smokes | Similar Strength, Type Restrictions im Wild-Carrier; Catch Rate, Catch Em All und Level Modifier tested-non-rom | Special-Wild/Day-Night/Swarms out-of-scope | Special-Wild nur separater Scope | 190, 191 |
| TM/HMs & Tutors | Working-matrix passed, Suboptionen offen | TM Moves, TM/HM Compatibility, Move Tutor Moves, Tutor Compatibility | Filter-/Follow-Suboptionen teilweise Carrier | Special Tutors/Text/Menu out of scope; Required-TM-Zwang bei Field Items separat | normale Suboptionen spaeter testen | 190 |
| Items | Working-matrix passed mit Caveats | Field Items basic, Pickup Items, Shop Items | - | Required-TM-Field-Item-Zwang kann bei expanded TMs blockieren; supported/special shops bestaetigt | Basic Field Items verwenden; Sonderoptionen separat | 190, 191 |
| Types | Working-matrix passed / optional chaos | TypeEffectiveness Random/Balanced/Inverse/Update/Add Immunities | - | stark gameplayveraendernd, fuer normale Runs optional | Statuspflege/Regression | 190 |
| Graphics | Write modelliert / P2 gemischt | Palette Safety / unchanged; keine Missing-Sprite-Blocker im Stable Smoke beobachtet | - | echte Palette Randomization, Custom Player Graphics | Palette Fix spaeter | 058, 191 |
| Misc Tweaks | Nicht begonnen | - | - | alle Misc Tweaks offen | Misc-Inventar | offen |

## GUI-Feature-Gruppen

| GUI-Gruppe | Hauptstatus | Was funktioniert? | Was ist nur Carrier-tested? | Offen / blockiert | Naechster Schritt |
|---|---|---|---|---|---|
| General Options | Teilweise getestet | - | Limit Pokemon, No Premature Evolutions | Race Mode, Intro Mon; nicht im Stable Visual Profile | General-Smoke spaeter |
| Pokemon Base Stats | Working-matrix passed | Random/Shuffle Base Stats | Follow Evolutions nur geplant | EXP Curves, Gen Update offen; Log-Ability-Namen koennen kuerzen | Suboptionen spaeter |
| Pokemon Types | Working-matrix passed fuer Species Types | Type Read/Write | Force Dual Types geplant | TypeChart separat, inzwischen getestet | keine enge Luecke |
| Pokemon Abilities | Working-matrix passed | Ability1/2 + Hidden Ability | Ban-/Filter-Suboptionen geplant | - | Suboption-Smoke spaeter |
| Evolutions | Unchanged preserved, Randomization separat | Evolutions unchanged preserved nach Row-Stride-Fix | Similar Strength und Same Typing diagnosis-ready; `017/020-023`, `024/027`, `025A` tested-non-rom; `026` helper-only | Evolution Randomization im Stable-Profil OFF | separater Evolution-Smoke |
| Starters | Starter/Rival sync passed | Starter Random completely; Oak-Lab Rival Counter-Slot | Basic/Type/BST/Legendary Filter | Starter Held Items; `Rival Carries Starter Through Game` ungetestet | Stable Visual Profile + Starters samplen |
| Static/Gift | Working-matrix passed mit Caveat | Static/Gift Species | Similar Strength im Scope | null placeholders bleiben null; Level Modifier/Fix Music offen | spaeter |
| In-Game Trades | Working-matrix passed | Species writes im CFRU/DPE Extended-BPRE-Pfad; kein `NEW GIVEN = ?` | - | Text/Nickname/OT/IV/Item nicht gesondert freigegeben | Detailpfade nur separat |
| Trainer | Working-matrix passed mit Caveat | Species, Movesets, Trainer Names | Similar Strength; Additional Pokemon, Type Diversity / Type Themes, Trainer Special Rules, Battle Style tested-non-rom | Trainer Class Names textlabel-only; Sprite/Class-ID mismatch erwartbar | Trainer Class Names fuer Stable-Visual OFF lassen |
| Wild | Working-matrix passed | Standard/Fallback Wild | Similar Strength, Type Restrictions; Catch Rate, Catch Em All, Level Modifier tested-non-rom | Special-Wild/Day-Night/Swarms out-of-scope | separater Special-Wild-Scope falls freigegeben |
| Movesets | Working-matrix passed | Learnsets/Movesets/Reorder/Sanity | Filter-Suboptionen | - | Regression spaeter |
| MoveData | Working-matrix passed | Power/Accuracy/PP/Type/Names im GUI-Smoke | - | Update Moves / Text-Encoding-Details nicht global P1-promoted | optionaler Reload-Scope nur separat |
| TM/HM | Working-matrix passed, Suboptionen offen | TM moves + compatibility | Field/Filter/Follow-Suboptionen | Required-TM-Zwang mit expanded TMs separat | spaeter |
| Tutors | Working-matrix passed normal, P2 Special | normal tutor moves + compatibility | filter/follow-suboptions | Special Tutors/Text/Menu | P2 |
| Items | Working-matrix passed mit Caveats | Field Items basic, Pickup Items, Shop Items | - | Field Items Required-TM-Zwang; supported/special shops bestaetigt | Basic Field Items verwenden |
| TypeEffectiveness | Working-matrix passed / optional chaos | Random/Balanced/Inverse/Update/Add Immunities | - | stark gameplayveraendernd | Statuspflege |
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
| 5 | `FVX-TRAIT-001` | Pokemon Traits | Base Stats: Shuffle / Random | Working-matrix passed | Stable Visual Profile / Log-caveat |
| 6 | `FVX-TRAIT-002` | Pokemon Traits | Base Stats: Follow Evolutions | Plan erstellt | Carrier / Filter |
| 7 | `FVX-TRAIT-003` | Pokemon Traits | Randomize Added Stats on Evolution | Plan erstellt | Carrier / Filter |
| 8 | `FVX-TRAIT-004` | Pokemon Traits | Update Base Stats to Generation | Nicht begonnen | Writer |
| 9 | `FVX-TRAIT-005` | Pokemon Traits | Standardize EXP Curves | Nicht begonnen | Writer |
| 10 | `FVX-TRAIT-006` | Pokemon Traits | Pokemon Types randomisieren | Working-matrix passed | Stable Visual Profile |
| 11 | `FVX-TRAIT-007` | Pokemon Traits | Force Dual Types | Plan erstellt | Carrier / Filter |
| 12 | `FVX-TRAIT-008` | Pokemon Traits | Pokemon Abilities randomisieren | Working-matrix passed | Stable Visual Profile |
| 13 | `FVX-TRAIT-009` | Pokemon Traits | Abilities: Follow Evolutions | Plan erstellt | Carrier / Filter |
| 14 | `FVX-TRAIT-010` | Pokemon Traits | Abilities: Allow Wonder Guard | Plan erstellt | Filter |
| 15 | `FVX-TRAIT-011` | Pokemon Traits | Abilities: Combine Duplicate Abilities | Plan erstellt | Filter |
| 16 | `FVX-TRAIT-012` | Pokemon Traits | Abilities: Ensure Two Abilities | Plan erstellt | Filter |
| 17 | `FVX-TRAIT-013` | Pokemon Traits | Abilities: Ban Trapping Abilities | Plan erstellt | Filter |
| 18 | `FVX-TRAIT-014` | Pokemon Traits | Abilities: Ban Negative Abilities | Plan erstellt | Filter |
| 19 | `FVX-TRAIT-015` | Pokemon Traits | Abilities: Ban Bad Abilities | Plan erstellt | Filter |
| 20 | `FVX-TRAIT-016` | Pokemon Traits | Pokemon Evolutions randomisieren | Unchanged preserved; randomization separat | Evolution row-stride fixed / no P1 promotion |
| 21 | `FVX-TRAIT-017` | Pokemon Traits | Evolutions: Random Every Level | tested-non-rom | Evolution-Species-Carrier / Filter |
| 22 | `FVX-TRAIT-018` | Pokemon Traits | Evolutions: Similar Strength | Diagnosis-ready | Evolution-Species-Carrier |
| 23 | `FVX-TRAIT-019` | Pokemon Traits | Evolutions: Same Typing | Diagnosis-ready | Evolution-Species-Carrier |
| 24 | `FVX-TRAIT-020` | Pokemon Traits | Evolutions: Limit to Three Stages | tested-non-rom | Evolution-Species-Carrier / Graph filter |
| 25 | `FVX-TRAIT-021` | Pokemon Traits | Evolutions: No Convergence | tested-non-rom | Evolution-Species-Carrier / Graph filter |
| 26 | `FVX-TRAIT-022` | Pokemon Traits | Evolutions: Force Change | tested-non-rom | Evolution-Species-Carrier / Target filter |
| 27 | `FVX-TRAIT-023` | Pokemon Traits | Evolutions: Force Growth | tested-non-rom | Evolution-Species-Carrier / BST filter |
| 28 | `FVX-TRAIT-024` | Pokemon Traits | Change Impossible Evolutions | tested-non-rom | Evolution improvement / Methoden |
| 29 | `FVX-TRAIT-025` | Pokemon Traits | Make Evolutions Easier | 025A tested-non-rom; 025B offen | 025A Condense-Level; 025B Happiness-Byte-Patch |
| 30 | `FVX-TRAIT-026` | Pokemon Traits | Use Estimated Evolution Levels | helper-flag / no standalone support claim | Helper for 024/025 |
| 31 | `FVX-TRAIT-027` | Pokemon Traits | Remove Time-Based Evolutions | tested-non-rom | Evolution improvement / Time methods |
| 32 | `FVX-TRAIT-028` | Pokemon Traits | EXP-/Legendary-Kurven-Sonderfaelle | Nicht begonnen | Writer / Filter |
| 33 | `FVX-SST-001` | Starters, Statics & Trades | Starter Pokemon: Custom | P1-supported | Global |
| 34 | `FVX-SST-002` | Starters, Statics & Trades | Starter Pokemon: Random completely | Starter/Rival sync passed | Oak-Lab counter-slot / Stable optional |
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
| 46 | `FVX-SST-014` | Starters, Statics & Trades | In-Game Trades: Given/Requested species | Working-matrix passed | CFRU/DPE Extended-BPRE Species identity |
| 47 | `FVX-SST-015` | Starters, Statics & Trades | In-Game Trades: Nickname/OT/IV/Item | Offen / nicht gesondert freigegeben | Writer / Text |
| 48 | `FVX-MOVE-001` | Moves & Movesets | Randomize Move Power | Working-matrix passed | Stable Visual Profile |
| 49 | `FVX-MOVE-002` | Moves & Movesets | Randomize Move Accuracy | Working-matrix passed | Stable Visual Profile |
| 50 | `FVX-MOVE-003` | Moves & Movesets | Randomize Move PP | Working-matrix passed | Stable Visual Profile |
| 51 | `FVX-MOVE-004` | Moves & Movesets | Randomize Move Types | Working-matrix passed | Stable Visual Profile |
| 52 | `FVX-MOVE-005` | Moves & Movesets | Randomize Move Names | Working-matrix passed | Stable Visual Profile / Text caveat bleibt moeglich |
| 53 | `FVX-MOVE-006` | Moves & Movesets | Update Moves to Generation | tested-non-rom | Writer |
| 54 | `FVX-MOVE-007` | Moves & Movesets | Pokemon Movesets randomisieren | Stable-profile passed | Stable Visual Profile |
| 55 | `FVX-MOVE-008` | Moves & Movesets | Guaranteed Level 1 Moves | Plan erstellt | Carrier / Filter |
| 56 | `FVX-MOVE-009` | Moves & Movesets | Reorder Damaging Moves | P1-supported | Global |
| 57 | `FVX-MOVE-010` | Moves & Movesets | No Game-Breaking Moves | Plan erstellt | Filter |
| 58 | `FVX-MOVE-011` | Moves & Movesets | Force % Good Damaging Moves | Plan erstellt | Filter |
| 59 | `FVX-FOE-001` | Foe Pokemon | Trainer Pokemon randomisieren | Stable-profile passed | Stable Visual Profile |
| 60 | `FVX-FOE-002` | Foe Pokemon | Better Movesets: Boss Trainers | Stable-profile passed | Stable Visual Profile |
| 61 | `FVX-FOE-003` | Foe Pokemon | Better Movesets: Important Trainers | Stable-profile passed | Stable Visual Profile |
| 62 | `FVX-FOE-004` | Foe Pokemon | Better Movesets: Regular Trainers | Stable-profile passed | Stable Visual Profile |
| 63 | `FVX-FOE-005` | Foe Pokemon | Additional Pokemon: Boss Trainers | tested-non-rom | Writer / Mutation |
| 64 | `FVX-FOE-006` | Foe Pokemon | Additional Pokemon: Important Trainers | tested-non-rom | Writer / Mutation |
| 65 | `FVX-FOE-007` | Foe Pokemon | Additional Pokemon: Regular Trainers | tested-non-rom | Writer / Mutation |
| 66 | `FVX-FOE-008` | Foe Pokemon | Trainer Held Items | P1-supported | Global |
| 67 | `FVX-FOE-009` | Foe Pokemon | Force Diverse Types / Type Themes | tested-non-rom | Carrier / Filter |
| 68 | `FVX-FOE-010` | Foe Pokemon | Pokemon League Has Unique Pokemon | tested-non-rom | Filter |
| 69 | `FVX-FOE-011` | Foe Pokemon | Battle Style randomisieren | tested-non-rom | Decision / Writer-risk |
| 70 | `FVX-FOE-012` | Foe Pokemon | Rival Carries Starter Through Game | Ungetestet im aktuellen GUI-Smoke | Full-rival path / separate from Oak-Lab sync |
| 71 | `FVX-FOE-013` | Foe Pokemon | Randomize Trainer Names / Class Names | Trainer Names passed; Class Names textlabel-only caveat | Text / Stable-Visual Class Names OFF |
| 72 | `FVX-FOE-014` | Foe Pokemon | Trainers Evolve Their Pokemon + Level Modifier | tested-non-rom | Writer |
| 73 | `FVX-WILD-001` | Wild Pokemon | Randomize Wild Pokemon | Stable-profile passed | Standard/Fallback Wild |
| 74 | `FVX-WILD-002` | Wild Pokemon | Replacements Per Species | P1-supported | Global |
| 75 | `FVX-WILD-003` | Wild Pokemon | Split by Encounter Types | P1-supported | Global |
| 76 | `FVX-WILD-004` | Wild Pokemon | Type Restrictions | Getestet im Carrier | Carrier |
| 77 | `FVX-WILD-005` | Wild Pokemon | Evolution Restrictions | Plan erstellt | Filter |
| 78 | `FVX-WILD-006` | Wild Pokemon | Don't Use Legendaries | P1-supported | Global |
| 79 | `FVX-WILD-007` | Wild Pokemon | Set Minimum Catch Rate | tested-non-rom | Writer |
| 80 | `FVX-WILD-008` | Wild Pokemon | Randomize Wild Held Items | Working-matrix passed | Stable Visual Profile if enabled |
| 81 | `FVX-WILD-009` | Wild Pokemon | Ban Bad Held Items | Working-matrix passed | Stable Visual Profile if enabled |
| 82 | `FVX-WILD-010` | Wild Pokemon | Catch Em All Mode | tested-non-rom | Filter / Writer |
| 83 | `FVX-WILD-011` | Wild Pokemon | Similar Strength | Getestet im Carrier | Carrier |
| 84 | `FVX-WILD-012` | Wild Pokemon | Balance Low Level Encounters + Level Modifier | tested-non-rom | Writer |
| 85 | `FVX-TM-001` | TM/HMs & Tutors | TM Moves randomisieren | Working-matrix passed | Stable Visual Profile |
| 86 | `FVX-TM-002` | TM/HMs & Tutors | Keep Field Move TMs | Plan erstellt | Filter |
| 87 | `FVX-TM-003` | TM/HMs & Tutors | TM No Game-Breaking Moves | Plan erstellt | Filter |
| 88 | `FVX-TM-004` | TM/HMs & Tutors | TM Force % Good Damaging Moves | Plan erstellt | Filter |
| 89 | `FVX-TM-005` | TM/HMs & Tutors | TM/HM Compatibility randomisieren | Working-matrix passed | Stable Visual Profile |
| 90 | `FVX-TM-006` | TM/HMs & Tutors | TM/Levelup Move Sanity | Working-matrix passed | Stable Visual Profile |
| 91 | `FVX-TM-007` | TM/HMs & Tutors | TM Compatibility Follow Evolutions | Plan erstellt | Filter |
| 92 | `FVX-TM-008` | TM/HMs & Tutors | Full HM Compatibility | Plan erstellt | Filter |
| 93 | `FVX-TM-009` | TM/HMs & Tutors | Move Tutor Moves randomisieren | Working-matrix passed | Stable Visual Profile |
| 94 | `FVX-TM-010` | TM/HMs & Tutors | Keep Field Move Tutors | Plan erstellt | Filter |
| 95 | `FVX-TM-011` | TM/HMs & Tutors | Tutor No Game-Breaking Moves | Plan erstellt | Filter |
| 96 | `FVX-TM-012` | TM/HMs & Tutors | Tutor Force % Good Damaging Moves | Plan erstellt | Filter |
| 97 | `FVX-TM-013` | TM/HMs & Tutors | Tutor Compatibility randomisieren | Working-matrix passed | Stable Visual Profile |
| 98 | `FVX-TM-014` | TM/HMs & Tutors | Tutor/Levelup Sanity | Working-matrix passed | Stable Visual Profile |
| 99 | `FVX-TM-015` | TM/HMs & Tutors | Tutor Compatibility Follow Evolutions | Plan erstellt | Filter |
| 100 | `FVX-ITEM-001` | Items | Field Items Shuffle | Working-matrix passed | Field Items basic; Required-TM caveat |
| 101 | `FVX-ITEM-002` | Items | Field Items Random | Working-matrix passed | Field Items basic; Required-TM caveat |
| 102 | `FVX-ITEM-003` | Items | Field Items Random even distribution | Working-matrix passed | Field Items basic; Required-TM caveat |
| 103 | `FVX-ITEM-004` | Items | Field Items Ban Bad Items | Working-matrix passed | Writer / Filter |
| 104 | `FVX-ITEM-005` | Items | Shop Items Shuffle | Working-matrix passed with caveat | supported/special shops confirmed |
| 105 | `FVX-ITEM-006` | Items | Shop Items Random | Working-matrix passed with caveat | supported/special shops confirmed |
| 106 | `FVX-ITEM-007` | Items | Shop Item Bans | Working-matrix passed with caveat | supported/special shops confirmed |
| 107 | `FVX-ITEM-008` | Items | Guarantee Evolution/X Items | Working-matrix passed with caveat | supported/special shops confirmed |
| 108 | `FVX-ITEM-009` | Items | Balance Shop Prices / Cheap Rare Candies | Working-matrix passed with caveat | supported/special shops confirmed |
| 109 | `FVX-ITEM-010` | Items | Pickup Items Random / Ban Bad Items | Working-matrix passed | Log-confirmed |
| 110 | `FVX-TYPE-001` | Types | Type Effectiveness Random/Balanced/Keep Identities/Inverse | Working-matrix passed / optional chaos | Writer |
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

## In-Game-Trades Status nach Diagnose 164

| Thema | Status |
|---|---|
| Locator/Table Model | verstanden, aber valide aktive Rows nicht bestaetigt |
| Preserve/Skip-Policy | dokumentiert; unsichere Rows nicht schreiben |
| Null-/Invalid-Species Guard | in UPR-FVX gemerged und im Workspace gepinnt |
| `TradeRandomizerTest` Non-ROM Harness | vorhanden und dokumentiert |
| Gen3 Writer-Preserve-Test | UPR-FVX PR #41 gemerged; ROM-freier `Gen3InGameTradeWriterTest` vorhanden |
| Species-Write-Smoke | Working-matrix passed im CFRU/DPE Extended-BPRE-Pfad; kein `NEW GIVEN = ?` nach PR #89 |
| Text/Nickname/OT/IV/Held Item | offen / nicht gesondert freigegeben |
| Kompatibilitaetsklassifikation | species path passed in current GUI matrix; Text/Nickname/OT/IV/Item bleiben Detailpfade |

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
| Diagnose 164 | Abschlussklassifikation: `guarded/preserve-only, not supported` |
| UPR-FVX PR #89 | CFRU/DPE Extended-BPRE In-Game Trades schreiben interne SpeciesSet-Identity; kein `NEW GIVEN = ?` in lokaler Working Matrix |

## Offene Blocker

| Prioritaet | Blocker | Status | Betroffene Feature-IDs | Ursache / Symptom | Naechster Schritt | Belege |
|---|---|---|---|---|---|---|
| P0/P1 | Stable Visual Profile + Starter Pokemon | offen fuer laengeres Sampling | `FVX-SST-002` plus Stable-Profil-Features | Oak-Lab Rival Counter-Sync passed, aber noch kein laengeres Profil-Sampling mit Starters ON | Stable Visual Profile + Starter Pokemon lokal samplen | 192 |
| P1 | Rival Carries Starter Through Game | ungetestet im aktuellen GUI-Smoke | `FVX-FOE-012` | Oak-Lab Rival Sync ist gefixt, aber der Full-Rival-Carry-Pfad bleibt separat | separater Smoke nur bei Bedarf | 179, 192 |
| P1 | Trainer Special Rules | tested-non-rom | `FVX-FOE-010`, `FVX-FOE-014` | Non-ROM `TrainerSpecialRulesTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 179 |
| P1 | Trainer Battle Style | tested-non-rom | `FVX-FOE-011` | Non-ROM `TrainerBattleStyleTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 180 |
| P1 | Trainer Names/Class Names | Trainer Names passed; Class Names textlabel-only caveat | `FVX-FOE-013` | Trainer Class Names aendert Textlabels; Sprite/Class-ID mismatch bleibt erwartbar | fuer Stable-Visual OFF lassen; echte Class Assignment waere neues Feature | 190 |
| P1 | In-Game Trades Detailpfade | Species path passed; Textdetails offen | `FVX-SST-014`, `FVX-SST-015` | Species schreibt im CFRU/DPE Extended-BPRE-Pfad, aber Nickname/OT/IV/Item nicht gesondert freigegeben | Detailpfade nur separat | 190 |
| P1 | Trainer Additional Pokemon | tested-non-rom | `FVX-FOE-005`, `FVX-FOE-006`, `FVX-FOE-007` | Non-ROM `TrainerAdditionalPokemonTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 178 |
| P1 | Wild Catch / Level | tested-non-rom | `FVX-WILD-007`, `FVX-WILD-010`, `FVX-WILD-012` | Non-ROM `WildCatchLevelDecisionTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 176 |
| P1 | MoveData Write | tested-non-rom fuer Core-Bytes / Text offen | `FVX-MOVE-001` bis `FVX-MOVE-006` | Power/Accuracy/PP/Type/Update haben Non-ROM-Evidenz; Move Names/Text bleibt offen | Move Names/Text oder ROM-/Reload-Evidenz separat planen | 056, 083-090, 175 |
| P1 | Trainer Type Diversity / Type Themes | tested-non-rom | `FVX-FOE-009` | Non-ROM `TrainerTypeDiversityGuardTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 070, 075, 077, 177 |
| P1 | Palette Randomization | Write modelliert / Fix offen | `FVX-GFX-001` bis `FVX-GFX-004` | compressed/shared/repointing risks | Palette Preserve/Repoint Fix | 058 |
| P1 | Special-Wild / Day-Night / Swarms | out-of-scope | Wild Sondertabellen ausser Standard/Fallback | nicht Teil der aktuellen GUI Working Matrix; Swarms fuer normales Profil deaktiviert | nur separater Special-Wild-Scope | 188, 190 |
| P2 | Special Tutors/Text/Menu | P2 / Out of scope | Tutor-Sonderpfade | Text/Menu/Special-Tutor-Logik ist nicht normaler Tutor-Scope | spaeter P2-Modell | 047, 060 |
| P2 | Graphics/Sprites | P2 / Nicht begonnen | `FVX-GFX-005`, `FVX-GFX-006` | Custom Player Graphics / Sprites getrennt von Paletten | spaeter Graphics-Modell | 058 |
| P2 | Misc Tweaks | Nicht begonnen | `FVX-MISC-001` bis `FVX-MISC-012` | Misc-Inventar offen | spaeter Inventar | offen |

## Naechste empfohlene Arbeitspakete

| Reihenfolge | Arbeitspaket | Ziel | Warum jetzt? | Erwartetes Ergebnis |
|---:|---|---|---|---|
| 1 | Stable Visual Profile + Starter Pokemon | groesstes aktuelles Normalprofil laenger samplen | Stable Visual Profile passed und Oak-Lab Rival Sync passed separat | lokaler Smoke mit Starters ON, Trainer Class Names OFF, Special-Wild OFF |
| 2 | Rival Carries Starter Through Game | Full-Rival-Pfad getrennt vom Oak-Lab-Fix pruefen | bleibt ungetestet | separater isolierter Smoke |
| 3 | Evolution Randomization | aktive Evolution-Randomization separat pruefen | Evolutions unchanged preserved, Randomization selbst OFF im Stable-Profil | separater Evolution-Smoke |
| 4 | Trainer Class Assignment / Sprite Sync | klaeren, ob ein neues visuell konsistentes Class-Assignment-Feature gewuenscht ist | Class Names bleibt textlabel-only | neues Feature nur separat planen |
| 5 | Field Items Required-TM Overflow | expanded-TM-Zwang absichern oder vermeiden | Basic Field Items passed, Required-TM-Zwang kann blockieren | Option separat diagnostizieren |
| 6 | Trainer Battle Style / Additional Pokemon / Special Rules | nur bei separater Freigabe writer-/reload-seitig pruefen | Non-ROM-Evidenz liegt vor, aber kein aktueller Stable-Smoke | nur explizit freigegebener Scope |
| 7 | Evolution Methods / Make Easier 025B | Methoden-/Byte-Patch-Slices getrennt halten | Non-ROM-Evidenz fuer Teile, Writer-/Reload-Evidenz fehlt | nur explizit freigegebener Scope |
| 8 | Palette Randomization | echte Palettenaenderungen absichern | grosser Graphics/Palette-Writer | `FVX-GFX-001` bis `FVX-GFX-004` hochstufen |
| 9 | Special-Wild / Special Tutors/Text/Menu | Sonderpfade modellieren | nicht normaler Stable-Profil-Scope | P2- oder separater Diagnose-Scope |
| 10 | Graphics/Sprites / Misc Tweaks | Custom Graphics und Misc inventarisieren | getrennt von aktuellen GUI-Smokes | P2-Entscheidung |

## Zuletzt abgeschlossene PRs / Diagnosen

| Diagnose / PR | Bereich | Ergebnis | Statuswirkung |
|---|---|---|---|
| Workspace PR #264 / UPR-FVX PR #97 | Starter/Rival Sync | UPR-FVX Pin `51d52a03235664154549105003dadfb45c76d0d0`; Oak-Lab Rival Counter-Slot passed | Starter Pokemon kann optional ins Stable Visual Profile; keine P1-Promotion; `Rival Carries Starter Through Game` bleibt separat |
| Workspace PR #263 | Stable Visual Profile Smoke | kurzer lokaler Stable Visual Profile Smoke passed | Stable Visual Profile ohne Starters passed; keine P1-Promotion |
| Workspace PR #262 | GUI Working Settings Matrix | Working Settings Matrix passed nach UPR-FVX PR #89 | breite GUI-Feature-Gruppen lokal nutzbar mit Caveats; keine P1-Promotion |
| 181 / UPR-FVX PR #51 | Trainer Names/Class Names Follow-up | UPR-FVX PR #51 gepinnt; `TrainerNameRandomizerTest` vorhanden | `FVX-FOE-013` `tested-non-rom`, keine P1-Freigabe ohne Gen3 Writer-/Reload-/Text-Encoding-Evidenz |
| 180B / UPR-FVX PR #50 | Trainer Battle Style Follow-up | UPR-FVX PR #50 gepinnt; `TrainerBattleStyleTest` vorhanden | `FVX-FOE-011` `tested-non-rom`, keine P1-Freigabe ohne ROM-/Reload-Evidenz |
| 179B / UPR-FVX PR #49 | Trainer Special Rules Follow-up | UPR-FVX PR #49 gepinnt; `TrainerSpecialRulesTest` vorhanden | `FVX-FOE-010/012/014` `tested-non-rom`, keine P1-Freigabe ohne ROM-/Reload-Evidenz |
| 178B / UPR-FVX PR #48 | Trainer Additional Pokemon Follow-up | UPR-FVX PR #48 gepinnt; `TrainerAdditionalPokemonTest` vorhanden | `FVX-FOE-005/006/007` `tested-non-rom`, keine P1-Freigabe ohne ROM-/Reload-Evidenz |
| 177B / UPR-FVX PR #47 | Trainer Type Diversity Follow-up | UPR-FVX PR #47 gepinnt; `TrainerTypeDiversityGuardTest` vorhanden | `FVX-FOE-009` `tested-non-rom`, keine P1-Freigabe ohne ROM-/Reload-Evidenz |
| 176B / UPR-FVX PR #46 | Wild Catch / Level Follow-up | UPR-FVX PR #46 gepinnt; `WildCatchLevelDecisionTest` vorhanden | `FVX-WILD-007`, `010`, `012` `tested-non-rom`, keine P1-Freigabe ohne ROM-/Reload-Evidenz |
| 175B / UPR-FVX PR #45 | MoveData Write Follow-up | UPR-FVX PR #45 gepinnt; `Gen3MoveDataWriterTest` und `MoveUpdateDecisionTest` vorhanden | `FVX-MOVE-001/002/003/004/006` `tested-non-rom`; `005` Text out of scope |
| 174B / UPR-FVX PR #44 | Evolution Make Evolutions Easier Follow-up | UPR-FVX PR #44 gepinnt; `EvolutionMakeEasierDecisionTest` vorhanden | `FVX-TRAIT-025A` `tested-non-rom`; `025B` offen; `026` helper-only |
| 173 | Evolution Make Evolutions Easier Scope Plan | `make-easier-plan-ready` | `FVX-TRAIT-025` in 025A Condense-/Level-Decision und 025B Gen3-Happiness-Byte-Patch getrennt; `026` helper-only |
| 172B / UPR-FVX PR #43 | Evolution Method Decision Harness Follow-up | UPR-FVX PR #43 gepinnt; `EvolutionMethodDecisionTest` vorhanden | `FVX-TRAIT-024` und `027` `tested-non-rom`, keine P1-Freigabe ohne Writer-/Reload- oder ROM-Smoke-Evidenz |
| 171 | Evolution Methods Decision Review | `decision-review-ready` | `FVX-TRAIT-024` und `027` fachlich reviewt; kleiner ROM-freier Decision-Harness empfohlen |
| 170 | Evolution Methods Scope Plan | `methods-plan-ready` | `FVX-TRAIT-024` bis `027` geplant, keine Test-/P1-Promotion |
| 169B / UPR-FVX PR #42 | Evolution Filter Non-ROM Harness Follow-up | UPR-FVX PR #42 gepinnt; `EvolutionFilterOptionsTest` vorhanden | `FVX-TRAIT-017` und `020-023` `tested-non-rom`, keine P1-Freigabe ohne ROM-Smoke/Reload |
| 168 | Evolution Filter Harness Plan | `harness-plan-ready` | `FVX-TRAIT-017` und `020-023` ROM-frei testbar mit synthetischen Species/Evolution-Daten und `RomHandler`-Proxy/Fake |
| 167 | Evolution Suboptions Consolidation | `evolution-scope-consolidated` | `FVX-TRAIT-016` bis `027` konsolidiert: `016` P1, `018/019` diagnosis-ready, `017/020-023` plan-only, `024-027` separat |
| 166 | Evolution Same Typing Diagnostics | `diagnosis-ready` | `FVX-TRAIT-019` aus aktivem Fixblockerstatus genommen; 079/080 Guard- und Reload-Evidenz bleibt massgeblich |
| 165 | Evolution Similar Strength Diagnostics | `diagnosis-ready` | `FVX-TRAIT-018` aus aktivem Fixblockerstatus genommen; 081/082 normalisierte Reload-Evidenz bleibt massgeblich |
| 164 | In-Game Trades Final Classification | `guarded/preserve-only, not supported` | Trades-Lane fuer aktuellen Scope geschlossen, keine Species-Write-Freigabe |
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
