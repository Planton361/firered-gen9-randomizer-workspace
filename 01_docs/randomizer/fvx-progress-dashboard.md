# FVX Progress Dashboard

## Zweck

Dieses Dashboard ist die schnelle Lesedatei fuer den aktuellen Universal Pokemon Randomizer FVX-Kompatibilitaetsstand im FireRed Gen9 Randomizer Workspace.

Es ersetzt keine Detaildiagnosen. Es verdichtet die Detailquellen auf eine Statusuebersicht:

- Was ist P1-supported?
- Was ist nur in einem Carrier getestet?
- Was ist read-only oder write-only modelliert?
- Was ist blockiert?
- Was ist als Naechstes dran?
- Welche Diagnoseprotokolle belegen den Stand?

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
| Aktueller enger Blocker | Trainer Type Diversity / Type Themes |
| Zuletzt entblockt | Wild Similar Strength und Wild Type Restrictions durch Wild-Nullslot-Fix |
| Zuletzt validiert | TypeChart / TypeEffectiveness Fix und Folgesmokes |
| Carrier-Smokes bestanden | Global Species Pool, Starter-Suboptions, Trainer Similar Strength |
| Danach | Evolution Similar Strength und Evolution Same Typing |
| Grosse offene Writer | MoveData Write, Field Items/Shops/Pickup, Palette Randomization |
| Spaeter / P2 | Special Tutors/Text/Menu, Graphics/Sprites, Misc Tweaks |

## Statusmodell

| Status | Bedeutung |
|---|---|
| P1-supported | Im getesteten CFRU/DPE Gen9-BPRE-Scope stabil belegt. Save/Log/Output/Reload oder aequivalente Kriterien sind bestanden. |
| Getestet im Carrier | Suboption wurde in einem bestimmten stabilen Hauptpfad getestet, aber nicht global fuer alle Kombinationen freigegeben. |
| Gefixt, Folgesmokes offen | Fix existiert, aber noch nicht durch vollstaendige Folgesmokes abgesichert. |
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
| P2 | Spaeterer Scope, zum Beispiel Special Tutors, Text/Menu oder Graphics/Sprites. |

## Gesamtfortschritt nach Feature-Paketen

| Paket | Leitstatus | Stabil belegt | Carrier-tested | Blocker / Luecke | Naechster Schritt | Belege |
|---|---|---|---|---|---|---|
| General Options | Gemischt | - | Limit Pokemon, No Premature Evolutions im Starter-Carrier | Race Mode, Intro Mon offen | separater General-Smoke | 064 |
| Pokemon Traits | Gemischt | Base Stats, Species Types, Abilities, normale Evolutions | - | Evolution Similar Strength, Evolution Same Typing | Evolution-Blocker nach Trainer-Blocker isolieren | 051, 052, 059, 070, 075 |
| Starters, Statics & Trades | Gemischt | Starter Species, Static/Gift Species | Starter-Filter | Starter Held Items, Trades offen | spaeter Trades/Held Items | 065 |
| Moves & Movesets | Gemischt | Movesets/Learnsets, Reorder Damaging | einige Filter-/Sanity-Optionen | MoveData Write offen | MoveData Write Preserve | 049, 056 |
| Foe Pokemon / Trainer | Blockiert in Suboption | Trainer Species, Movesets, Held Items, Similar Strength | Similar Strength im Trainer-Carrier | Type Diversity / Type Themes | naechster enger Diagnose-/Fixblock | 070, 075, 077 |
| Wild Pokemon | Stark | Standard/Fallback Wild, Wild Held Items | Similar Strength, Type Restrictions im Wild-Carrier | Catch Rate, Catch Em All, Level Modifier offen | spaeter Wild-Level/Catch | 075 |
| TM/HMs & Tutors | Stark, Suboptionen offen | TM/HM 128-Slot, Tutor 152-Slot, Compatibility, Sanity | Filter-/Follow-Suboptionen teilweise Carrier | Special Tutors/Text/Menu out of scope | normale Suboptionen spaeter testen | 038, 040, 049 |
| Items | Write modelliert / Fix offen | Encounter Held Items separat stabil | - | Field Items/Shops/Pickup Fix offen | Item-Writer-Fix | 054, 057 |
| Types | Getestet / Kandidat fuer P1-supported | TypeEffectiveness Random/Balanced/Inverse/Update/Add Immunities | - | keine enge TypeChart-Luecke bekannt | Status ggf. auf P1-supported hochziehen | 066, 068 |
| Graphics | Write modelliert / P2 gemischt | Palette Safety / unchanged | - | echte Palette Randomization, Custom Player Graphics | Palette Fix spaeter | 058 |
| Misc Tweaks | Nicht begonnen | - | - | alle Misc Tweaks offen | Misc-Inventar | offen |

## GUI-Feature-Gruppen

| GUI-Gruppe | Hauptstatus | Was funktioniert? | Was ist nur Carrier-tested? | Offen / blockiert | Naechster Schritt |
|---|---|---|---|---|---|
| General Options | Teilweise getestet | - | Limit Pokemon, No Premature Evolutions | Race Mode, Intro Mon | General-Smoke spaeter |
| Pokemon Base Stats | P1-supported | Random/Shuffle Base Stats | Follow Evolutions nur geplant | EXP Curves, Gen Update offen | Suboptionen spaeter |
| Pokemon Types | P1-supported fuer Species Types | Type Read/Write | Force Dual Types geplant | TypeChart separat, inzwischen getestet | keine enge Luecke |
| Pokemon Abilities | P1-supported | Ability1/2 + Hidden Ability | Ban-/Filter-Suboptionen geplant | - | Suboption-Smoke spaeter |
| Evolutions | Teilweise supported, Suboptionen blockiert | normale Evolution Randomization | einige Filter geplant | Similar Strength, Same Typing | nach Trainer-Type-Blocker |
| Starters | Stark / Carrier-tested | Starter Species | Basic/Type/BST/Legendary Filter | Starter Held Items | spaeter Held Items |
| Static/Gift | P1-supported fuer Species | Static/Gift Species | Similar Strength im Scope | Level Modifier/Fix Music offen | spaeter |
| In-Game Trades | Nicht begonnen | - | - | Species/Text/Item/IV/OT/Nickname | eigenes Modell |
| Trainer | Teilweise blockiert | Species, Movesets, Held Items, Similar Strength | Similar Strength | Type Diversity / Type Themes | naechster enger Blocker |
| Wild | Stark | Standard/Fallback Wild, Held Items | Similar Strength, Type Restrictions | Catch Rate, Catch Em All, Level Modifier | spaeter |
| Movesets | P1-supported | Learnsets/Movesets/Reorder/Sanity | Filter-Suboptionen | - | Regression spaeter |
| MoveData | Write modelliert | Read vorhanden | - | Power/Accuracy/PP/Type/Names/Update Write offen | MoveData Writer |
| TM/HM | P1-supported, Suboptionen offen | TM/HM moves + compatibility | Field/Filter/Follow-Suboptionen | - | spaeter |
| Tutors | P1-supported normal, P2 Special | normal tutor moves + compatibility | filter/follow-suboptions | Special Tutors/Text/Menu | P2 |
| Items | Write modelliert | Encounter Held Items separat | - | Field Items/Shops/Pickup | Item Writer |
| TypeEffectiveness | Gefixt + Smokes bestanden | Random/Balanced/Inverse/Update/Add Immunities | - | keine enge Luecke | Status ggf. P1-supported |
| Palettes | Write modelliert | unchanged/safety path | - | echte Palette Randomization | Palette Fix |
| Graphics/Sprites | P2 / Nicht begonnen | - | - | Custom Player Graphics, Sprites | P2 |
| Misc Tweaks | Nicht begonnen | - | - | 12 Tweaks offen | Inventar |

## Offene Blocker

| Prioritaet | Blocker | Status | Betroffene Feature-IDs | Ursache / Symptom | Naechster Schritt | Belege |
|---|---|---|---|---|---|---|
| P0 | Trainer Type Diversity / Type Themes | Blockiert / naechster enger Blocker | `FVX-FOE-009` | Diagnose 077 isoliert `primaryType == null` in `EnumSet<Type>` bei `updateUsedTypes(...)` als wahrscheinliche Ursache | eng gegateter Fixblock | 070, 075, 077 |
| P1 | Evolution Similar Strength | Blockiert | `FVX-TRAIT-018` | Mismatch-/Bad-Egg-Slice aus bisherigem Similar-Strength-Smoke | separater Evolution-Similar-Strength-Block | 070, 075 |
| P1 | Evolution Same Typing | Blockiert | `FVX-TRAIT-019` | Same-Type-Evolution-Slice nicht freigegeben | separater Evolution-Same-Typing-Block | 070, 075 |
| P1 | MoveData Write | Write modelliert / Fix offen | `FVX-MOVE-001` bis `FVX-MOVE-006` | Writer fuer moderne MoveData-Felder offen | MoveData Preserve Writer | 056 |
| P1 | Field Items/Shops/Pickup | Write modelliert / Fix offen | `FVX-ITEM-001` bis `FVX-ITEM-010` | eigene Item-/Shop-/Pickup-Writer offen | Item Writer Fix | 057 |
| P1 | Palette Randomization | Write modelliert / Fix offen | `FVX-GFX-001` bis `FVX-GFX-004` | compressed/shared/repointing risks | Palette Preserve/Repoint Fix | 058 |
| P2 | Special Tutors/Text/Menu | P2 / Out of scope | Tutor-Sonderpfade | Text/Menu/Special-Tutor-Logik ist nicht normaler Tutor-Scope | spaeter P2-Modell | 047, 060 |
| P2 | Graphics/Sprites | P2 / Nicht begonnen | `FVX-GFX-005`, `FVX-GFX-006` | Custom Player Graphics / Sprites getrennt von Paletten | spaeter Graphics-Modell | 058 |

## Naechste empfohlene Arbeitspakete

| Reihenfolge | Arbeitspaket | Ziel | Warum jetzt? | Erwartetes Ergebnis |
|---:|---|---|---|---|
| 1 | Trainer Type Diversity / Type Themes | engsten aktuellen Trainer-Blocker isolieren/fixen | naechster enger Blocker; Diagnose 077 hat wahrscheinliche Ursache eingegrenzt | `FVX-FOE-009` wird P1-supported oder klar als Fix offen dokumentiert |
| 2 | Evolution Similar Strength | Evolution-Mismatch/Bad-Egg-Slice isolieren | direkt danach offen | `FVX-TRAIT-018` geklaert |
| 3 | Evolution Same Typing | Same-Type-Evolution-Slice isolieren | direkt danach offen | `FVX-TRAIT-019` geklaert |
| 4 | MoveData Write | Power/Accuracy/PP/Type/Update Moves absichern | grosser offener Moves-Tab-Writer | `FVX-MOVE-001` bis `FVX-MOVE-006` hochstufen |
| 5 | Field Items/Shops/Pickup | Items-Tab praktisch absichern | grosser offener Items-Tab-Writer | `FVX-ITEM-001` bis `FVX-ITEM-010` hochstufen |
| 6 | Palette Randomization | echte Palettenaenderungen absichern | grosser Graphics/Palette-Writer | `FVX-GFX-001` bis `FVX-GFX-004` hochstufen |
| 7 | Special Tutors/Text/Menu | P2-Sonderpfade modellieren | nicht normaler Tutor-Tabellenpfad | P2-Entscheidung |
| 8 | Graphics/Sprites | Custom Player Graphics/Sprites modellieren | getrennt von Paletten | P2-Entscheidung |

## Zuletzt abgeschlossene PRs / Diagnosen

| Diagnose / PR | Bereich | Ergebnis | Statuswirkung |
|---|---|---|---|
| 077 | Trainer Type Diversity Code Diagnosis | wahrscheinliche Null-Type-Ursache in `updateUsedTypes(...)` eingegrenzt | naechster enger Fixblock vorbereitet |
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
3. `Offene Blocker` aktualisieren.
4. `Zuletzt abgeschlossene PRs / Diagnosen` um eine Zeile ergaenzen.
5. `Carrier-tested, aber nicht global` aktualisieren, falls ein Smoke nur Carrier-Scope hat.

Dieses Dashboard bleibt kurz. Details gehoeren in die Diagnoseprotokolle unter `08_tests/randomizer/` und in die Feature-Matrix `01_docs/randomizer/fvx-feature-coverage.md`.

## Sicherheitsregeln

- Keine ROMs, Saves, Emulator States, Builds, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, Hashes, Secrets oder `.env`-Inhalte dokumentieren.
- Keine Detailwerte aus lokalen privaten Laeufen aufnehmen, wenn sie private Artefakte offenlegen koennten.
- Diagnose-IDs und PR-Nummern reichen als Nachweisanker.
