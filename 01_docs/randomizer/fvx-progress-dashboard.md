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
| Stand | Nach UPR-FVX PR #106 Pre/Post Runtime-Trainer-Audit, PR #105 Runtime-Source-Trainer-Randomization-Smoke, PR #104 Strict-Runtime-Trainer-Source-Sync, coverage-generated CLI profile matrix run und exact-coverage Batches 01 bis 18 CLI-Log-Smokes |
| UPR-FVX-Pin im Workspace | `5bb1d853f132095922be2aceef55af2878192b85` |
| Breites GUI-Profil | GUI Working Settings Matrix passed: Wild Standard/Fallback, Trainer Pokemon core, Pokemon Movesets Random completely, Trainer Movesets, Trainer Names, Field Items basic, Abilities, TM/HM, Tutors, Shops, Pickup, In-Game Trades, Static Pokemon, Type Effectiveness, Base Stats und Move Data |
| CLI Profile Matrix | Coverage-generated `.rnqs` profile matrix log-smoke passed for 14 profiles; exact-coverage Batch 01 passed for 19 profiles; Batch 02 Items passed for 13 profiles; Batches 03-17 passed for 165 generator-capable exact/cumulative/mode profiles; Batch 18 confirmed 4 Gen-Limit `MODE-*` overlays fail as expected; bad markers 0 and warnings 0 for all PASS profiles |
| Stable Visual Profile | Passed im kurzen lokalen Smoke; Trainer Class Names, Evolution Randomization und Special-Wild bleiben OFF |
| Zuletzt entblockt | UPR-FVX PR #106 stellt das Post-Audit-Tooling bereit; PR #105 macht generische `RUNTIME-SOURCE` Trainer randomizer-eligible; sanitized local evidence bestaetigt Viridian Forest `531/532` mit randomized loaded/raw parties, Ingame-Smoke Eiscue und randomized-output Audit `unloaded-valid-parties total=0`; Rival 2 `329/330/331` und Brock `414` zeigen ebenfalls randomisierte Parties in sanitized observations; PR #104 synchronisiert strict valide `trainerbattle` runtime-source TrainerData rows aus der Audit-Klasse `VALID_RUNTIME_NOT_LOADED`; PR #103 stellt den opt-in globalen Runtime-Trainer-Source-Audit bereit |
| Aktuelle Caveats | Runtime-source strict sync plus randomizer eligibility ist fuer Viridian Forest `531/532` lokal bestaetigt, aber keine breite Trainer/Foe-P1-Promotion; `loaded-mismatch`, invalid-pointer, empty-party und out-of-range rows sowie Full-Playthrough bleiben Diagnose-/Follow-up-Scope; Trainer Class Names bleibt textlabel-only; Graphics/Palettes und Misc Tweaks brauchen Visual-/Behavior-Smokes; Intro Mon braucht visuelle Bestaetigung; Gen-Limit-1-9 `MODE-*` Overlays bleiben unsupported by Settings format; Special-Wild/Day-Night/Swarms bleiben separater Scope; `Rival Carries Starter Through Game` hat CLI-Log-Smoke, aber keinen Ingame-/Full-Rival-Smoke |
| Keine P1-Promotion | Aktuelle Updates sind Workspace-/Smoke-Status, keine neue P1-Freigabe |
| Naechster sinnvoller Block | `loaded-mismatch`/`invalid` Runtime-Source-Rows separat triagieren; weitere suspected runtime-source battles nur mit eigener sanitized Evidence aufnehmen; danach gezielt Ingame-/Visual-/Behavior-Smokes isolieren: Trainer Held Items Sensible, Graphics/Palettes, Misc Tweaks, Special-Wild und Full-Rival-Carry |

## Statusmodell

| Status | Bedeutung |
|---|---|
| P1-supported | Im getesteten CFRU/DPE Gen9-BPRE-Scope stabil belegt. Save/Log/Output/Reload oder aequivalente Kriterien sind bestanden. |
| Supported im getesteten Scope | Praktisch freigegeben fuer den konkret getesteten CFRU/DPE Gen9-BPRE-Scope, aber nicht automatisch fuer alle ROM-Hack-Varianten. |
| Getestet im Carrier | Suboption wurde in einem bestimmten stabilen Hauptpfad getestet, aber nicht global fuer alle Kombinationen freigegeben. |
| tested-non-rom | ROM-frei per Unit-/Harness-Test belegt, aber ohne ROM-Smoke/Reload noch nicht P1-supported. |
| Audit-only | Diagnose-/Klassifikationshilfe ohne Runtime-Beweis, Auto-Sync oder Writer-Freigabe. |
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
| General Options | exact coverage passed mit Caveat / no P1 promotion | `FVX-GEN-001`, `FVX-GEN-002` CLI log-smoked; Intro random mode overlay log-smoked | - | Race Mode und No-Random-Intro bleiben nicht voll abgedeckt; Gen-Limit-1-9 `MODE-*` Overlays bleiben unsupported by Settings format | separater General-/Intro-Ingame-Smoke | 064, 197, 198, 201 |
| Pokemon Traits | Working-matrix passed / generated CLI profile passed / exact coverage passed | Base Stats, Species Types, Abilities; Evolutions unchanged preserved; `FVX-TRAIT-001` bis `028` CLI log-smoked | Evolution subsettings log-smoked, hard-combo rows bleiben caveated | Evolution Randomization/Methoden-Slices brauchen weiter Ingame-/Methoden-Smoke; Base-Stats-Log kann Ability-Namen kuerzen, ingame OK | Evolution-Randomization isolieren oder Stable-Profil laenger samplen | 189, 190, 191, 197, 198, 199, 201 |
| Starters, Statics & Trades | Working-matrix passed / Starter Sync passed / exact coverage passed | Starter Pokemon Random completely + Oak-Lab Rival Counter-Sync; Static Pokemon; In-Game Trades ohne `NEW GIVEN = ?`; `FVX-SST-002` bis `015` CLI log-smoked | Starter-Filter, Starter/Static variants, Starter Held Items und Trades log-smoked | `FVX-SST-001` Custom Starters bleibt manual/unsupported; Static null placeholders bleiben null | Stable Visual Profile + Starter Pokemon samplen; Custom Starters nur separater manueller Scope | 190, 192, 197, 198, 199, 201 |
| Moves & Movesets | Working-matrix passed / exact coverage passed | Pokemon Movesets, Trainer Movesets, Move Data Power/Accuracy/PP/Type/Names; `FVX-MOVE-001` bis `005` und `007` bis `011` CLI log-smoked | Filter-/Sanity-Optionen log-smoked | Update Moves bleibt fuer CFRU/DPE Gen9-Basis out-of-scope; Text-Encoding-Detailpfade nicht global P1-promoted | laengeres Stable-Profil-Sampling | 190, 191, 197, 198, 201 |
| Foe Pokemon / Trainer | Working-matrix passed mit Caveat / exact coverage passed / Runtime-source 531-532 smoke passed | Trainer Pokemon core, Trainer Movesets, Trainer Names; `FVX-FOE-001` bis `014` and exact Foe mode overlays CLI log-smoked; strict `VALID_RUNTIME_NOT_LOADED` runtime-source sync merged; generic `RUNTIME-SOURCE` trainers randomizer-eligible; Viridian Forest `531/532` locally confirmed; randomized output audit `unloaded-valid-parties total=0`; Rival 2 `329/330/331` and Brock `414` randomized in sanitized observations | Additional Pokemon, Type Diversity / Type Themes, Battle Style, Full-Rival-Carry, Trainer Held Items and exact Foe modes log-smoked | Runtime-source `531/532` Trainer Pokemon path is locally smoke-confirmed, but broader loaded-mismatch/invalid/out-of-range rows and full playthrough remain Follow-up; Trainer Class Names textlabel-only; Sprite/Class-ID mismatch erwartbar; Sensible Held Items braucht fokussierte Isolation; Full-Rival-Carry braucht Ingame-Smoke | `loaded-mismatch`/`invalid` separat triagieren; weitere suspected runtime-source battles nur mit eigener sanitized Evidence aufnehmen; Trainer Class Names OFF lassen oder Class Assignment separat planen; Sensible Items und Full-Rival-Carry isolieren | 190, 191, 197, 198, 199, 201, 202, 203, 204 |
| Wild Pokemon | Working-matrix passed / exact coverage passed with Special-Wild caveat | Standard/Fallback Wild, normale Encounter-Smokes; `FVX-WILD-001` bis `012` and exact Wild location overlays CLI log-smoked | Similar Strength, Type Restrictions, Catch Rate, Catch Em All, Level Modifier and exact Wild location modes log-smoked | Special-Wild/Day-Night/Swarms bleiben separater Scope trotz clean CLI profile | Special-Wild nur separater Scope | 190, 191, 197, 198, 201 |
| TM/HMs & Tutors | Working-matrix passed / exact coverage passed | TM Moves, TM/HM Compatibility, Move Tutor Moves, Tutor Compatibility; `FVX-TM-001` bis `015` CLI log-smoked | Filter-/Follow-Suboptionen log-smoked | Special Tutors/Text/Menu out of scope; Required-TM-Zwang bei Field Items separat | Ingame-Smoke fuer Suboptionen spaeter | 190, 197, 198, 201 |
| Items | Working-matrix passed mit Caveats / generated CLI profile passed / exact Batch 02 passed | Field Items basic, Pickup Items, Shop Items | Item single/variant profiles in Batch 02 log-smoke | Required-TM-Field-Item-Zwang kann bei expanded TMs blockieren; supported/special shops bestaetigt | local boot/play or item-specific ingame smoke | 190, 191, 197, 198, 200 |
| Types | exact coverage passed mit Caveat / optional chaos | `FVX-TYPE-001` bis `003` and exact Random/Random-Balanced/Keep-Identities/Inverse overlays CLI log-smoked | - | TypeEffectiveness bleibt stark gameplayveraendernd und braucht fokussierte Ingame-Validierung fuer staerkere Claims | Statuspflege/Regression | 190, 197, 198, 201 |
| Graphics | exact coverage passed mit Caveat / P2 gemischt | `FVX-GFX-001` bis `004` Palette Randomization log-smoked ohne Bad Marker | - | Ingame visual smoke fuer Palettes fehlt; Custom Player Graphics bleibt manual/out-of-scope | Palette-Visual-Smoke oder Fix spaeter | 058, 191, 197, 198, 201 |
| Misc Tweaks | exact coverage passed / behavior smoke offen | `FVX-MISC-001` bis `012` log-smoked ohne Bad Marker | - | behavior-spezifische Ingame-/Manual-Smokes fehlen | Misc-Inventar und fokussierte Smokes | 197, 198, 201 |

## GUI-Feature-Gruppen

| GUI-Gruppe | Hauptstatus | Was funktioniert? | Was ist nur Carrier-tested? | Offen / blockiert | Naechster Schritt |
|---|---|---|---|---|---|
| General Options | exact coverage passed fuer `FVX-GEN-001/002` mit Gen-Limit-Caveat | Limit Pokemon, No Premature Evolutions and Intro random mode CLI log-smoked | - | Race Mode, No-Random-Intro und Intro-Visual bleiben offen; Gen-Limit-1-9 `MODE-*` Overlays unsupported by Settings format | General-/Intro-Smoke spaeter |
| Pokemon Base Stats | Working-matrix passed / generated matrix passed | Random/Shuffle Base Stats | Follow Evolutions, EXP Curves und Gen Update log-smoked | Log-Ability-Namen koennen kuerzen; Ingame-Smoke fuer Suboptionen fehlt | Suboptionen spaeter |
| Pokemon Types | Working-matrix passed / generated matrix passed | Type Read/Write | Force Dual Types log-smoked | TypeChart separat, inzwischen getestet | Ingame-Smoke fuer Suboptionen spaeter |
| Pokemon Abilities | Working-matrix passed / generated matrix passed | Ability1/2 + Hidden Ability | Ban-/Filter-Suboptionen log-smoked | Ingame-Smoke fuer Suboptionen fehlt | Suboption-Smoke spaeter |
| Evolutions | Unchanged preserved / generated matrix passed mit Caveats | Evolutions unchanged preserved nach Row-Stride-Fix | Evolution-Randomization und Subsettings log-smoked | Evolution Randomization im Stable-Profil OFF; Methoden-/Ingame-Smoke fehlt | separater Evolution-Smoke |
| Starters | Starter/Rival sync passed / exact coverage passed | Starter Random completely; Oak-Lab Rival Counter-Slot | Basic/Type/BST/Legendary Filter und Starter Held Items log-smoked | Custom Starters manual/unsupported; Full-Rival-Carry bleibt Ingame-Follow-up | Stable Visual Profile + Starters samplen |
| Static/Gift | Working-matrix passed mit Caveat | Static/Gift Species | Similar Strength im Scope | null placeholders bleiben null; Level Modifier/Fix Music offen | spaeter |
| In-Game Trades | Working-matrix passed | Species writes im CFRU/DPE Extended-BPRE-Pfad; kein `NEW GIVEN = ?` | - | Text/Nickname/OT/IV/Item nicht gesondert freigegeben | Detailpfade nur separat |
| Trainer | Working-matrix passed mit Caveat / exact coverage passed / Runtime-source 531-532 smoke passed | Species, Movesets, Trainer Names; strict `VALID_RUNTIME_NOT_LOADED` runtime-source sync merged; generic `RUNTIME-SOURCE` trainers randomizer-eligible; Viridian Forest `531/532` locally confirmed; randomized output audit `unloaded-valid-parties total=0`; Rival 2 `329/330/331` and Brock `414` randomized in sanitized observations | Additional Pokemon, Type Diversity / Type Themes, Special Rules, Battle Style, Full-Rival-Carry, Held Items and exact Foe modes log-smoked | Broader `loaded-mismatch`/invalid/out-of-range rows and full playthrough remain Follow-up; Trainer Class Names textlabel-only; Sensible Held Items und Full-Rival-Carry brauchen fokussierte Ingame-Smokes | `loaded-mismatch`/`invalid` separat triagieren; weitere suspected runtime-source battles nur mit eigener sanitized Evidence aufnehmen; Trainer Class Names fuer Stable-Visual OFF lassen; Sensible Items und Full-Rival-Carry isolieren |
| Wild | Working-matrix passed / generated matrix passed | Standard/Fallback Wild | Similar Strength, Type Restrictions, Catch Rate, Catch Em All, Level Modifier and exact Wild location modes log-smoked | Special-Wild/Day-Night/Swarms separater Scope trotz clean CLI profile | separater Special-Wild-Scope falls freigegeben |
| Movesets | Working-matrix passed | Learnsets/Movesets/Reorder/Sanity | Filter-Suboptionen | - | Regression spaeter |
| MoveData | Working-matrix passed | Power/Accuracy/PP/Type/Names im GUI-Smoke | - | Update Moves / Text-Encoding-Details nicht global P1-promoted | optionaler Reload-Scope nur separat |
| TM/HM | Working-matrix passed / generated matrix passed | TM moves + compatibility | Field/Filter/Follow-Suboptionen log-smoked | Required-TM-Zwang mit expanded TMs separat | spaeter |
| Tutors | Working-matrix passed normal / generated matrix passed | normal tutor moves + compatibility | filter/follow-suboptions log-smoked | Special Tutors/Text/Menu | P2 |
| Items | Working-matrix passed mit Caveats | Field Items basic, Pickup Items, Shop Items | - | Field Items Required-TM-Zwang; supported/special shops bestaetigt | Basic Field Items verwenden |
| TypeEffectiveness | exact coverage passed mit Caveat / optional chaos | Random/Random-Balanced/Keep-Identities/Inverse/Update/Add Immunities CLI log-smoked | - | stark gameplayveraendernd; braucht fokussierte Ingame-Validierung fuer staerkere Claims | Statuspflege |
| Palettes | exact coverage passed mit Caveat | Palette Randomization log-smoked | - | Ingame visual smoke fehlt | Palette Visual Smoke / Fix |
| Graphics/Sprites | P2 / Nicht begonnen | - | - | Custom Player Graphics, Sprites | P2 |
| Misc Tweaks | exact coverage passed / behavior smoke offen | 12 Tweaks log-smoked | - | behavior-spezifische Ingame-/Manual-Smokes fehlen | Inventar und fokussierte Smokes |

## Vollstaendige Feature-Liste

Diese Tabelle listet alle aktuell erfassten FVX-Features einmal kompakt auf. Sie ist bewusst nicht nach Unterabschnitten getrennt, damit der gesamte Scope in einer einzigen Liste sichtbar ist.

| Nr. | Feature-ID | Bereich | Feature | Dashboard-Status | Scope |
|---:|---|---|---|---|---|
| 1 | `FVX-GEN-001` | General Options | Limit Pokemon | Exact coverage CLI passed with Gen-Limit caveat | Log-smoke / Ingame follow-up needed; exact Gen-Limit-1-9 MODE overlays unsupported |
| 2 | `FVX-GEN-002` | General Options | No Premature Evolutions | Exact coverage CLI passed | Log-smoke / Ingame follow-up needed |
| 3 | `FVX-GEN-003` | General Options | No Random Intro Mon | Intro random CLI passed with caveat | Intro visual confirmation and no-random variant still open |
| 4 | `FVX-GEN-004` | General Options | Race Mode | Nicht begonnen | No-write |
| 5 | `FVX-TRAIT-001` | Pokemon Traits | Base Stats: Shuffle / Random | Working-matrix passed | Stable Visual Profile / Log-caveat |
| 6 | `FVX-TRAIT-002` | Pokemon Traits | Base Stats: Follow Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 7 | `FVX-TRAIT-003` | Pokemon Traits | Randomize Added Stats on Evolution | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 8 | `FVX-TRAIT-004` | Pokemon Traits | Update Base Stats to Generation | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 9 | `FVX-TRAIT-005` | Pokemon Traits | Standardize EXP Curves | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 10 | `FVX-TRAIT-006` | Pokemon Traits | Pokemon Types randomisieren | Working-matrix passed | Stable Visual Profile |
| 11 | `FVX-TRAIT-007` | Pokemon Traits | Force Dual Types | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 12 | `FVX-TRAIT-008` | Pokemon Traits | Pokemon Abilities randomisieren | Working-matrix passed | Stable Visual Profile |
| 13 | `FVX-TRAIT-009` | Pokemon Traits | Abilities: Follow Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 14 | `FVX-TRAIT-010` | Pokemon Traits | Abilities: Allow Wonder Guard | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 15 | `FVX-TRAIT-011` | Pokemon Traits | Abilities: Combine Duplicate Abilities | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 16 | `FVX-TRAIT-012` | Pokemon Traits | Abilities: Ensure Two Abilities | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 17 | `FVX-TRAIT-013` | Pokemon Traits | Abilities: Ban Trapping Abilities | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 18 | `FVX-TRAIT-014` | Pokemon Traits | Abilities: Ban Negative Abilities | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 19 | `FVX-TRAIT-015` | Pokemon Traits | Abilities: Ban Bad Abilities | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 20 | `FVX-TRAIT-016` | Pokemon Traits | Pokemon Evolutions randomisieren | Unchanged preserved; randomization separat | Evolution row-stride fixed / no P1 promotion |
| 21 | `FVX-TRAIT-017` | Pokemon Traits | Evolutions: Random Every Level | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 22 | `FVX-TRAIT-018` | Pokemon Traits | Evolutions: Similar Strength | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 23 | `FVX-TRAIT-019` | Pokemon Traits | Evolutions: Same Typing | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 24 | `FVX-TRAIT-020` | Pokemon Traits | Evolutions: Limit to Three Stages | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 25 | `FVX-TRAIT-021` | Pokemon Traits | Evolutions: No Convergence | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 26 | `FVX-TRAIT-022` | Pokemon Traits | Evolutions: Force Change | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 27 | `FVX-TRAIT-023` | Pokemon Traits | Evolutions: Force Growth | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 28 | `FVX-TRAIT-024` | Pokemon Traits | Change Impossible Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 29 | `FVX-TRAIT-025` | Pokemon Traits | Make Evolutions Easier | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 30 | `FVX-TRAIT-026` | Pokemon Traits | Use Estimated Evolution Levels | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 31 | `FVX-TRAIT-027` | Pokemon Traits | Remove Time-Based Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 32 | `FVX-TRAIT-028` | Pokemon Traits | EXP-/Legendary-Kurven-Sonderfaelle | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 33 | `FVX-SST-001` | Starters, Statics & Trades | Starter Pokemon: Custom | Manual/unsupported by generated exact coverage | Manual-only |
| 34 | `FVX-SST-002` | Starters, Statics & Trades | Starter Pokemon: Random completely | Starter/Rival sync passed | Oak-Lab counter-slot / Stable optional |
| 35 | `FVX-SST-003` | Starters, Statics & Trades | Starter Pokemon: Random basic with 2 evolutions | Getestet im Carrier | Carrier |
| 36 | `FVX-SST-004` | Starters, Statics & Trades | Starter Pokemon: Random any basic | Getestet im Carrier | Carrier |
| 37 | `FVX-SST-005` | Starters, Statics & Trades | Starter Type Restrictions | Getestet im Carrier | Carrier |
| 38 | `FVX-SST-006` | Starters, Statics & Trades | Starter: Don't Use Legendaries | Getestet im Carrier | Carrier |
| 39 | `FVX-SST-007` | Starters, Statics & Trades | Starter Held Items randomisieren | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 40 | `FVX-SST-008` | Starters, Statics & Trades | Starter Held Items: Ban Bad Items | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 41 | `FVX-SST-009` | Starters, Statics & Trades | Starter BST-Min/Max | Getestet im Carrier | Carrier |
| 42 | `FVX-SST-010` | Starters, Statics & Trades | Static Pokemon: Swap Legendaries & Standards | P1-supported | Global |
| 43 | `FVX-SST-011` | Starters, Statics & Trades | Static Pokemon: Random completely | P1-supported | Global |
| 44 | `FVX-SST-012` | Starters, Statics & Trades | Static Pokemon: Random similar strength | P1-supported | Global |
| 45 | `FVX-SST-013` | Starters, Statics & Trades | Static Pokemon: Level Modifier / Fix Music | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 46 | `FVX-SST-014` | Starters, Statics & Trades | In-Game Trades: Given/Requested species | Working-matrix passed | CFRU/DPE Extended-BPRE Species identity |
| 47 | `FVX-SST-015` | Starters, Statics & Trades | In-Game Trades: Nickname/OT/IV/Item | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 48 | `FVX-MOVE-001` | Moves & Movesets | Randomize Move Power | Working-matrix passed | Stable Visual Profile |
| 49 | `FVX-MOVE-002` | Moves & Movesets | Randomize Move Accuracy | Working-matrix passed | Stable Visual Profile |
| 50 | `FVX-MOVE-003` | Moves & Movesets | Randomize Move PP | Working-matrix passed | Stable Visual Profile |
| 51 | `FVX-MOVE-004` | Moves & Movesets | Randomize Move Types | Working-matrix passed | Stable Visual Profile |
| 52 | `FVX-MOVE-005` | Moves & Movesets | Randomize Move Names | Working-matrix passed | Stable Visual Profile / Text caveat bleibt moeglich |
| 53 | `FVX-MOVE-006` | Moves & Movesets | Update Moves to Generation | Out of scope fuer CFRU/DPE Gen9 | By-design disabled |
| 54 | `FVX-MOVE-007` | Moves & Movesets | Pokemon Movesets randomisieren | Stable-profile passed | Stable Visual Profile |
| 55 | `FVX-MOVE-008` | Moves & Movesets | Guaranteed Level 1 Moves | Plan erstellt | Carrier / Filter |
| 56 | `FVX-MOVE-009` | Moves & Movesets | Reorder Damaging Moves | P1-supported | Global |
| 57 | `FVX-MOVE-010` | Moves & Movesets | No Game-Breaking Moves | Plan erstellt | Filter |
| 58 | `FVX-MOVE-011` | Moves & Movesets | Force % Good Damaging Moves | Plan erstellt | Filter |
| 59 | `FVX-FOE-001` | Foe Pokemon | Trainer Pokemon randomisieren | Stable-profile passed | Stable Visual Profile |
| 60 | `FVX-FOE-002` | Foe Pokemon | Better Movesets: Boss Trainers | Stable-profile passed | Stable Visual Profile |
| 61 | `FVX-FOE-003` | Foe Pokemon | Better Movesets: Important Trainers | Stable-profile passed | Stable Visual Profile |
| 62 | `FVX-FOE-004` | Foe Pokemon | Better Movesets: Regular Trainers | Stable-profile passed | Stable Visual Profile |
| 63 | `FVX-FOE-005` | Foe Pokemon | Additional Pokemon: Boss Trainers | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 64 | `FVX-FOE-006` | Foe Pokemon | Additional Pokemon: Important Trainers | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 65 | `FVX-FOE-007` | Foe Pokemon | Additional Pokemon: Regular Trainers | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 66 | `FVX-FOE-008` | Foe Pokemon | Trainer Held Items | Generated CLI profile passed with caveat | Held Items / Sensible caveat |
| 67 | `FVX-FOE-009` | Foe Pokemon | Force Diverse Types / Type Themes | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 68 | `FVX-FOE-010` | Foe Pokemon | Pokemon League Has Unique Pokemon | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 69 | `FVX-FOE-011` | Foe Pokemon | Battle Style randomisieren | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 70 | `FVX-FOE-012` | Foe Pokemon | Rival Carries Starter Through Game | Exact coverage CLI passed | Full-rival ingame smoke still needed |
| 71 | `FVX-FOE-013` | Foe Pokemon | Randomize Trainer Names / Class Names | Trainer Names passed; Class Names textlabel-only caveat | Text / Stable-Visual Class Names OFF |
| 72 | `FVX-FOE-014` | Foe Pokemon | Trainers Evolve Their Pokemon + Level Modifier | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 73 | `FVX-WILD-001` | Wild Pokemon | Randomize Wild Pokemon | Stable-profile passed | Standard/Fallback Wild |
| 74 | `FVX-WILD-002` | Wild Pokemon | Replacements Per Species | P1-supported | Global |
| 75 | `FVX-WILD-003` | Wild Pokemon | Split by Encounter Types | P1-supported | Global |
| 76 | `FVX-WILD-004` | Wild Pokemon | Type Restrictions | Getestet im Carrier | Carrier |
| 77 | `FVX-WILD-005` | Wild Pokemon | Evolution Restrictions | Plan erstellt | Filter |
| 78 | `FVX-WILD-006` | Wild Pokemon | Don't Use Legendaries | P1-supported | Global |
| 79 | `FVX-WILD-007` | Wild Pokemon | Set Minimum Catch Rate | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 80 | `FVX-WILD-008` | Wild Pokemon | Randomize Wild Held Items | Working-matrix passed | Stable Visual Profile if enabled |
| 81 | `FVX-WILD-009` | Wild Pokemon | Ban Bad Held Items | Working-matrix passed | Stable Visual Profile if enabled |
| 82 | `FVX-WILD-010` | Wild Pokemon | Catch Em All Mode | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 83 | `FVX-WILD-011` | Wild Pokemon | Similar Strength | Getestet im Carrier | Carrier |
| 84 | `FVX-WILD-012` | Wild Pokemon | Balance Low Level Encounters + Level Modifier | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 85 | `FVX-TM-001` | TM/HMs & Tutors | TM Moves randomisieren | Working-matrix passed | Stable Visual Profile |
| 86 | `FVX-TM-002` | TM/HMs & Tutors | Keep Field Move TMs | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 87 | `FVX-TM-003` | TM/HMs & Tutors | TM No Game-Breaking Moves | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 88 | `FVX-TM-004` | TM/HMs & Tutors | TM Force % Good Damaging Moves | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 89 | `FVX-TM-005` | TM/HMs & Tutors | TM/HM Compatibility randomisieren | Working-matrix passed | Stable Visual Profile |
| 90 | `FVX-TM-006` | TM/HMs & Tutors | TM/Levelup Move Sanity | Working-matrix passed | Stable Visual Profile |
| 91 | `FVX-TM-007` | TM/HMs & Tutors | TM Compatibility Follow Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 92 | `FVX-TM-008` | TM/HMs & Tutors | Full HM Compatibility | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 93 | `FVX-TM-009` | TM/HMs & Tutors | Move Tutor Moves randomisieren | Working-matrix passed | Stable Visual Profile |
| 94 | `FVX-TM-010` | TM/HMs & Tutors | Keep Field Move Tutors | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 95 | `FVX-TM-011` | TM/HMs & Tutors | Tutor No Game-Breaking Moves | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 96 | `FVX-TM-012` | TM/HMs & Tutors | Tutor Force % Good Damaging Moves | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
| 97 | `FVX-TM-013` | TM/HMs & Tutors | Tutor Compatibility randomisieren | Working-matrix passed | Stable Visual Profile |
| 98 | `FVX-TM-014` | TM/HMs & Tutors | Tutor/Levelup Sanity | Working-matrix passed | Stable Visual Profile |
| 99 | `FVX-TM-015` | TM/HMs & Tutors | Tutor Compatibility Follow Evolutions | Generated CLI profile passed | Log-smoke / Ingame follow-up needed |
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
| 110 | `FVX-TYPE-001` | Types | Type Effectiveness Random/Balanced/Keep Identities/Inverse | Exact coverage CLI passed with caveat | Exact variants log-smoked; gameplay-disruptive ingame follow-up needed |
| 111 | `FVX-TYPE-002` | Types | Add Random Immunities | Exact coverage CLI passed with caveat | Optional chaos / Ingame follow-up needed |
| 112 | `FVX-TYPE-003` | Types | Update Type Effectiveness | Exact coverage CLI passed with caveat | Optional chaos / Ingame follow-up needed |
| 113 | `FVX-GFX-001` | Graphics | Pokemon Palettes Random | Exact coverage CLI passed with caveat | Palette visual smoke needed |
| 114 | `FVX-GFX-002` | Graphics | Palettes: Follow Types | Exact coverage CLI passed with caveat | Palette visual smoke needed |
| 115 | `FVX-GFX-003` | Graphics | Palettes: Follow Evolutions | Exact coverage CLI passed with caveat | Palette visual smoke needed |
| 116 | `FVX-GFX-004` | Graphics | Palettes: Shiny From Normal | Exact coverage CLI passed with caveat | Palette visual smoke needed |
| 117 | `FVX-GFX-005` | Graphics | Custom Player Graphics | Manual/unsupported by generated exact coverage | Manual-only / P2 |
| 118 | `FVX-GFX-006` | Graphics | Character to Replace | Manual/unsupported by generated exact coverage | Manual-only / P2 |
| 119 | `FVX-MISC-001` | Misc Tweaks | Fastest Text | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 120 | `FVX-MISC-002` | Misc Tweaks | Running Shoes Indoors | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 121 | `FVX-MISC-003` | Misc Tweaks | Randomize PC Potion | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 122 | `FVX-MISC-004` | Misc Tweaks | Give National Dex at Start | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 123 | `FVX-MISC-005` | Misc Tweaks | Fast Egg Hatching | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 124 | `FVX-MISC-006` | Misc Tweaks | Lower Case Pokemon Names | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 125 | `FVX-MISC-007` | Misc Tweaks | Randomize Catching Tutorial | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 126 | `FVX-MISC-008` | Misc Tweaks | Ban Lucky Egg | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 127 | `FVX-MISC-009` | Misc Tweaks | Balance Static Pokemon Levels | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 128 | `FVX-MISC-010` | Misc Tweaks | Run Without Running Shoes | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 129 | `FVX-MISC-011` | Misc Tweaks | Reusable TMs | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |
| 130 | `FVX-MISC-012` | Misc Tweaks | Forgettable HMs | Exact coverage CLI passed | Behavior-specific manual/ingame smoke |

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
| P1 | Rival Carries Starter Through Game | exact coverage batch 05 passed | `FVX-FOE-012` | CLI log-smoke passed, aber der Full-Rival-Carry-Pfad hat keinen Ingame-Smoke | separater Ingame-Smoke nur bei Bedarf | 179, 192, 201 |
| P1 | Trainer Special Rules | tested-non-rom | `FVX-FOE-010`, `FVX-FOE-014` | Non-ROM `TrainerSpecialRulesTest` vorhanden; keine ROM-/Reload-Evidenz und kein ROM-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 179 |
| P1 | Trainer Battle Style | exact coverage batch 01 passed | `FVX-FOE-011` | Batch 01 CLI log-smoke passed, aber keine ROM-/Reload-Evidenz und kein Ingame-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 180, 199 |
| P1 | Trainer Names/Class Names | Trainer Names passed; Class Names textlabel-only caveat | `FVX-FOE-013` | Trainer Class Names aendert Textlabels; Sprite/Class-ID mismatch bleibt erwartbar | fuer Stable-Visual OFF lassen; echte Class Assignment waere neues Feature | 190 |
| P1 | Trainer Runtime Source | diagnosis harness ready | `FVX-FOE-001` bis `FVX-FOE-014` | CLI log-smoke clean, aber zweite Rival-, Brock- und einzelne normale Trainer-Battles koennen ingame eine andere Runtime-Quelle nutzen als der Trainer-Log | lokale redaktierte Runtime-Source-Evidence sammeln; keine P1-Promotion | 202 |
| P1 | In-Game Trades Detailpfade | Species path passed; Textdetails offen | `FVX-SST-014`, `FVX-SST-015` | Species schreibt im CFRU/DPE Extended-BPRE-Pfad, aber Nickname/OT/IV/Item nicht gesondert freigegeben | Detailpfade nur separat | 190 |
| P1 | Trainer Additional Pokemon | exact coverage batch 01 passed | `FVX-FOE-005`, `FVX-FOE-006`, `FVX-FOE-007` | Batch 01 CLI log-smoke passed, aber keine ROM-/Reload-Evidenz und kein Ingame-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 178, 197, 199 |
| P1 | Wild Catch / Level | exact coverage batch 04 passed | `FVX-WILD-007`, `FVX-WILD-010`, `FVX-WILD-012` | CLI log-smoke passed, aber keine ROM-/Reload-Evidenz und kein Ingame-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 176, 197, 201 |
| P1 | MoveData Write | exact coverage batch 08 passed fuer generatorfaehige Moves | `FVX-MOVE-001` bis `FVX-MOVE-005`, `FVX-MOVE-007` bis `FVX-MOVE-011`; `FVX-MOVE-006` out-of-scope | CLI log-smoke passed fuer generatorfaehige rows; Move Names/Text und Update-Moves bleiben separate Grenzen | Move Names/Text oder ROM-/Reload-Evidenz separat planen | 056, 083-090, 175, 201 |
| P1 | Trainer Type Diversity / Type Themes | exact coverage batch 01 passed | `FVX-FOE-009` | Batch 01 CLI log-smoke passed, aber keine ROM-/Reload-Evidenz und kein Ingame-Smoke | P1-Promotion nur separat mit ROM-/Reload-Scope | 070, 075, 077, 177, 197, 199 |
| P1 | Palette Randomization | exact coverage batch 09 passed mit Caveat | `FVX-GFX-001` bis `FVX-GFX-004` | CLI log-smoke clean, aber Ingame Visual Smoke und Writer-Risiko bleiben offen | Palette Visual Smoke / Preserve-Repoint-Fix | 058, 197, 201 |
| P1 | Special-Wild / Day-Night / Swarms | generated CLI profile passed mit Scope-Caveat | Wild Sondertabellen ausser Standard/Fallback | CLI log-smoke clean, aber nicht Teil der GUI Working Matrix; Swarms fuer normales Profil deaktiviert | nur separater Special-Wild-Scope | 188, 190, 197, 198 |
| P2 | Special Tutors/Text/Menu | P2 / Out of scope | Tutor-Sonderpfade | Text/Menu/Special-Tutor-Logik ist nicht normaler Tutor-Scope | spaeter P2-Modell | 047, 060 |
| P2 | Graphics/Sprites | manual/unsupported | `FVX-GFX-005`, `FVX-GFX-006` | Custom Player Graphics / Sprites getrennt von Paletten und nicht durch generated exact coverage unterstuetzt | spaeter Graphics-Modell | 058, 201 |
| P2 | Misc Tweaks | exact coverage batch 10 passed | `FVX-MISC-001` bis `FVX-MISC-012` | CLI log-smoke clean, aber behavior-spezifische Ingame-/Manual-Smokes fehlen | spaeter Inventar / fokussierte Smokes | 197, 201 |

## Naechste empfohlene Arbeitspakete

| Reihenfolge | Arbeitspaket | Ziel | Warum jetzt? | Erwartetes Ergebnis |
|---:|---|---|---|---|
| 1 | Trainer Runtime Source Evidence | zweite Rival-, Brock- und normale Trainer-Battles gegen `TrainerData`-Runtime-Quelle vergleichen | Foe Trainer ist CLI-log-clean, aber ingame partial/caveated | lokale opt-in Diagnose, nur redaktierte Evidence |
| 2 | Stable Visual Profile + Starter Pokemon | groesstes aktuelles Normalprofil laenger samplen | Stable Visual Profile passed und Oak-Lab Rival Sync passed separat | lokaler Smoke mit Starters ON, Trainer Class Names OFF, Special-Wild OFF |
| 3 | Rival Carries Starter Through Game | Full-Rival-Pfad getrennt vom Oak-Lab-Fix ingame pruefen | hat CLI-Log-Smoke, aber keinen Ingame-/Full-Rival-Smoke | separater isolierter Smoke |
| 4 | Evolution Randomization | aktive Evolution-Randomization separat pruefen | Evolutions unchanged preserved, Randomization selbst OFF im Stable-Profil | separater Evolution-Smoke |
| 5 | Trainer Class Assignment / Sprite Sync | klaeren, ob ein neues visuell konsistentes Class-Assignment-Feature gewuenscht ist | Class Names bleibt textlabel-only | neues Feature nur separat planen |
| 6 | Field Items Required-TM Overflow | expanded-TM-Zwang absichern oder vermeiden | Basic Field Items passed, Required-TM-Zwang kann blockieren | Option separat diagnostizieren |
| 7 | Evolution Methods / Make Easier 025B | Methoden-/Byte-Patch-Slices getrennt halten | Non-ROM-Evidenz fuer Teile, Writer-/Reload-Evidenz fehlt | nur explizit freigegebener Scope |
| 8 | Palette Randomization | echte Palettenaenderungen visuell absichern | exact coverage CLI passed, aber Visual Smoke fehlt | `FVX-GFX-001` bis `FVX-GFX-004` de-caveaten |
| 9 | Special-Wild / Special Tutors/Text/Menu | Sonderpfade modellieren | Special-Wild CLI profile clean, aber Scope bleibt separat | P2- oder separater Diagnose-Scope |
| 10 | Graphics/Sprites / Misc Tweaks | Custom Graphics und Misc-Verhalten inventarisieren | Palettes/Misc CLI profiles clean, aber visuelle/manuelle Smokes fehlen | P2-Entscheidung / fokussierte Smokes |

## Zuletzt abgeschlossene PRs / Diagnosen

| Diagnose / PR | Bereich | Ergebnis | Statuswirkung |
|---|---|---|---|
| Workspace sync / UPR-FVX PR #100 | Trainer Runtime Source Diagnostics | UPR-FVX Pin `87bba797620dd2043f02c11c67f7b752a7238a00`; No-ROM/synthetic trainerbattle-to-`TrainerData` diagnostic harness and opt-in report extension available | Foe Trainer remains CLI-log-clean but ingame partial/caveated until redacted runtime-source evidence confirms affected battles use the logged/written source; no P1-Promotion |
| Exact coverage Batches 03-18 | CLI Profile Matrix | 165 generator-capable exact/cumulative/mode profiles log-smoked cleanly across TM/Tutor, Wild, Foe, General/Traits, Starters/Statics/Trades, Moves, Graphics/Palettes, Misc, Types, cumulative profiles and exact Foe/Wild/Type/Intro mode overlays; Batch 18 confirms 4 Gen-Limit MODE overlays fail as expected; bad markers 0, warnings 0 for PASS profiles | Updates generator-capable Feature-Test-Status-Matrix rows to `PASS_LOG` / `PASS_LOG_WITH_CAVEAT`; records Gen-Limit unsupported status; keeps visual/behavior/manual follow-ups and no P1-Promotion |
| Exact coverage Batch 02 Items | CLI Profile Matrix / Items | 13 exact Item single/variant profiles log-smoked cleanly; bad markers 0, warnings 0 | Updates requested Item Feature-Test-Status-Matrix rows to `PASS_LOG`; no P1-Promotion |
| Exact coverage Batch 01 | CLI Profile Matrix | 19 exact single/variant profiles log-smoked cleanly; bad markers 0, warnings 0 | Updates requested Feature-Test-Status-Matrix rows to `PASS_LOG`; no P1-Promotion |
| Workspace PR #270 + generated matrix run | CLI Profile Matrix | 14 generated `.rnqs` profiles log-smoked cleanly; bad markers 0, warnings 0 | Updates Feature-Test-Status-Matrix to `PASS_LOG` / `PASS_LOG_WITH_CAVEAT`; no P1-Promotion |
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
