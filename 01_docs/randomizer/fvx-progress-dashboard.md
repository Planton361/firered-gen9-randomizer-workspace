# FVX Progress Dashboard

## Zweck

Dieses Dashboard ist die schnelle Lesedatei fuer den aktuellen Universal Pokemon Randomizer FVX-Kompatibilitaetsstand im FireRed Gen9 Randomizer Workspace.

Es ersetzt keine Detaildiagnosen. Massgeblich bleiben die Detailquellen in `08_tests/randomizer/`, `01_docs/randomizer/fvx-feature-coverage.md`, `00_project-control/roadmap/fvx-feature-roadmap.md`, `00_project-control/roadmap/roadmap-status.md`, `01_docs/SESSION_STATE.md` und `01_docs/NEXT_STEPS.md`.

## Stand

| Feld | Aktueller Stand |
|---|---|
| Stand | Nach PR #207 / Diagnose 162 |
| UPR-FVX-Submodule | `02_external/upr-fvx` zuletzt auf `1eaee2873cd69682335223f817b124bf36d004f2` dokumentiert |
| Aktueller In-Game-Trades-Status | `blocked-pending-evidence`, guarded/preserve-only |
| Zuletzt abgeschlossen | In-Game-Trades Null-/Invalid-Species Guard, Non-ROM `TradeRandomizerTest`, Writer-Preserve-Test-Plan |
| Naechster optionaler enger Block | UPR-FVX `:romio:test` fuer Gen3 Writer-Preserve mit kleinem Test-Seam |
| Nicht freigegeben | ROM-Smoke, Species-Write-Smoke, Text/Nickname/OT/IV/Trade-Held-Item-Scope |

## Kurzfazit

Der getestete CFRU/DPE Gen9-BPRE-Scope hat inzwischen mehrere stabile FVX-Featurebereiche:

- Standard-/Fallback-Wild inklusive Surfing, Fishing und Rock Smash sind supported.
- Wild Similar Strength und Wild Type Restrictions sind im Wild-Carrier entblockt.
- Item-Scope ist im getesteten Scope abgeschlossen: Field Items, Pickup Items, Shop Items und Held Items.
- Learnsets/Movesets, TM/HM-/Tutor-Normalpfade, Trainer-Kernpfade, Starter- und Static/Gift-Species sowie TypeEffectiveness sind dokumentiert stabil bzw. in ihren Carrier-Slices belegt.
- Evolution Species-only ist P1-supported; Evolution Similar Strength und Evolution Same Typing bleiben separate offene Suboptionen.
- In-Game Trades sind technisch defensiv abgesichert, aber fachlich nicht kompatibel freigegeben.

## Aktuelle Feature-Paket-Uebersicht

| Paket | Leitstatus | Stabil belegt / aktuell nutzbar | Offen / blockiert | Naechster sinnvoller Schritt |
|---|---|---|---|---|
| General Options | Teilweise / Carrier | Limit Pokemon, No Premature Evolutions im Carrier | Race Mode, Intro Mon | spaeter separater General-Smoke |
| Pokemon Traits | Stark, Suboptionen offen | Base Stats, Species Types, Abilities, Evolution Species-only | Evolution Similar Strength, Evolution Same Typing, weitere Evolution-/EXP-Writer | Evolution-Suboptionen separat isolieren |
| Starters | Stark | Starter Species, Custom/Random, mehrere Starter-Filter im Carrier | Starter Held Items separat vom Starter-Species-Scope | spaeter Starter-Held-Item-Scope falls noetig |
| Static/Gift | Stark | Static/Gift Species, Similar Strength | Level Modifier/Fix Music offen | spaeter Spezialoptionen |
| In-Game Trades | Blockiert / guarded | Guard gegen unsichere Rows, Non-ROM `TradeRandomizerTest`, Writer-Preserve-Test-Plan | keine validen aktiven Trade-Rows, kein Species-Write-Smoke, kein Text/Nickname/OT/IV/Item-Scope | optionaler ROM-freier `:romio:test` Writer-Preserve |
| Movesets | P1-supported | Learnsets/Movesets, Reorder Damaging, Sanity-Pfade | weitere Filter nur bei Bedarf | Regression spaeter |
| MoveData | Write modelliert / offen | Read-/Modellstand vorhanden | Power/Accuracy/PP/Type/Names/Update-Moves Writer | MoveData Writer/Persistenz-Block |
| Trainer | Teilweise stark, Suboptionen offen | Species, Movesets, Held Items, Similar Strength | Type Diversity / Type Themes, Additional Pokemon, Text-Namen | Trainer-Type-Suboptionen oder spaeter Additional-Pokemon |
| Wild | Stark | Standard/Fallback, Surfing, Fishing, Rock Smash, Held Items, Similar Strength/Type Restrictions im Carrier | Catch Rate, Catch Em All, Level Modifier | spaeter Wild-Level/Catch-Scope |
| TM/HM | Stark | TM/HM Moves, Compatibility, Sanity | Filter-/Follow-Evolution-Suboptionen | spaeter Suboptionen |
| Tutors | Stark fuer normalen Tutor-Scope | normaler Tutor-Move-/Compatibility-Pfad | Special Tutors/Text/Menu P2 | P2-Modell fuer Special Tutors |
| Items | Supported im getesteten Scope | Field Items, Pickup Items, Shop Items, Held Items | Sonderoptionen nur bei neuer Evidenz | Regression/Statuspflege |
| Types | Stark | TypeEffectiveness Random/Balanced/Inverse/Update/Add Immunities | keine enge TypeChart-Luecke bekannt | Statuspflege/Regression |
| Graphics/Palettes | P2 / Writer-Risiko | Safety-/unchanged-Pfade | echte Palette Randomization, Custom Player Graphics | spaeter Palette-/Graphics-Block |
| Misc Tweaks | Nicht begonnen | - | Misc-Tweaks offen | spaeter Inventar |

## Kompatibilitaetszaehlung nach aktueller praktischer Lesart

Diese Zaehlung ist eine Arbeitszaehlung fuer das Dashboard, keine Ersatz-Matrix.

| Zaehlweise | Ergebnis |
|---|---|
| Groessere aktuell stabile Featurebereiche | Wild, Items, Movesets, TM/HM/Tutors normal, Trainer-Kern, Starter/Static Species, Pokemon Traits-Kern, Types |
| Granulare zuletzt klar bestaetigte Slices | Standard Wild, Surfing, Fishing, Rock Smash, Field Items, Pickup Items, Shop Items, Held Items, Evolution Species-only |
| Aktuell bewusst nicht kompatibel freigegeben | In-Game Trades, MoveData Write, Palette Randomization, mehrere Evolution-/Trainer-Suboptionen, Misc Tweaks |
| In-Game-Trades-Sonderstand | Guarded/preserve-only mit Tests/Plan, aber weiter `blocked-pending-evidence` |

## In-Game-Trades Status nach Diagnose 162

| Thema | Status |
|---|---|
| Locator/Table Model | verstanden, aber valide aktive Rows nicht bestaetigt |
| Preserve/Skip-Policy | dokumentiert; unsichere Rows nicht schreiben |
| Null-/Invalid-Species Guard | in UPR-FVX gemerged und im Workspace gepinnt |
| `TradeRandomizerTest` Non-ROM Harness | vorhanden und dokumentiert |
| Gen3 Writer-Preserve-Test | Plan ready; noch nicht implementiert |
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
| Diagnose 162 / PR #207 | Writer-Preserve-Test-Plan: `writer-test-plan-ready` |

## Offene Blocker / Luecken

| Prioritaet | Blocker | Status | Naechster Schritt |
|---|---|---|---|
| P0/P1 | In-Game Trades | guarded/preserve-only, `blocked-pending-evidence` | optionaler UPR-FVX `:romio:test` Writer-Preserve, sonst weiter blockiert lassen |
| P1 | Evolution Similar Strength | blockiert/offen | eigener Diagnose-/Fixblock |
| P1 | Evolution Same Typing | blockiert/offen | eigener Diagnose-/Fixblock |
| P1 | MoveData Write | write modelliert / Fix offen | Writer-Preserve-/Persistenzblock |
| P1 | Trainer Type Diversity / Type Themes | frueherer enger Blocker, Status gegen neuere Roadmap pruefen | nur bei Fortsetzung Trainer-Scope |
| P1 | Palette Randomization | writer-risk / offen | spaeter Palette-Block |
| P2 | Special Tutors/Text/Menu | out of scope | spaeter P2-Modell |
| P2 | Graphics/Sprites | out of scope | spaeter Graphics-Modell |
| P2 | Misc Tweaks | nicht begonnen | spaeter Inventar |

## Naechste empfohlene Arbeitspakete

| Reihenfolge | Arbeitspaket | Ziel | Erwartetes Ergebnis |
|---:|---|---|---|
| 1 | UPR-FVX Gen3 Writer-Preserve-Test | ROM-freier `:romio:test` fuer unsafe In-Game-Trade Rows, nur mit kleinem Seam | Writer-Preserve-Guard wird testbar belegt oder blockiert |
| 2 | Workspace-Follow-up zum Writer-Test | Submodule-Gitlink und Diagnose dokumentieren | Dashboard/Roadmap/Manifest synchron |
| 3 | Entscheidung In-Game-Trades | guarded/preserve-only abschliessen oder weitere Evidenz suchen | klare Klassifikation fuer diesen Scope |
| 4 | Evolution Similar Strength | blockierte Evolution-Suboption isolieren | supported oder Fix offen |
| 5 | Evolution Same Typing | blockierte Evolution-Suboption isolieren | supported oder Fix offen |
| 6 | MoveData Write | offene MoveData-Writer absichern | P1-Fortschritt Moves-Tab |
| 7 | Palette / Graphics / P2 | spaetere visuelle Spezialpfade | P2-Entscheidung |

## Nicht tun ohne separate Freigabe

- ROMs lesen, kopieren, aendern oder hochladen
- Saves, Emulator States, Output-ROMs, Randomizer-JARs, Tool-Binaries oder Logs committen
- ROM-Smoke oder Species-Write-Smoke fuer In-Game Trades starten
- Text/Nickname/OT/IV/Trade-Held-Item Randomization anfassen
- grosse Refactors oder ROM-backed Testfixtures fuer den Writer-Preserve-Test erzwingen
- Original-Upstreams kontaktieren oder PRs dorthin oeffnen
