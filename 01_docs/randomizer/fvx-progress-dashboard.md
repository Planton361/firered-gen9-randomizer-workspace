# FVX Progress Dashboard

## Zweck

Dieses Dashboard ist die schnelle Lesedatei fuer den aktuellen Universal Pokemon Randomizer FVX-Kompatibilitaetsstand im FireRed Gen9 Randomizer Workspace.

Es ersetzt keine Detaildiagnosen. Es verdichtet die Detailquellen auf eine Statusuebersicht und zeigt, welche GUI-Features aktuell im getesteten CFRU/DPE-Gen9-BPRE-Profil nutzbar sind, welche nur mit Caveat funktionieren und welche als naechste Arbeitsbloecke offen sind.

Optionaler XLSX-Export fuer filterbare Tabellen:

```powershell
python 07_scripts/randomizer/export_fvx_progress_dashboard_xlsx.py --input 01_docs/randomizer/fvx-progress-dashboard.md --output /tmp/fvx-progress-dashboard.xlsx
```

Markdown bleibt Source of Truth.

## Detailquellen

| Datei / Bereich | Rolle |
|---|---|
| `01_docs/randomizer/fvx-feature-coverage.md` | Langform der FVX-Feature-/Suboption-Matrix mit Feature-IDs |
| `00_project-control/roadmap/fvx-feature-roadmap.md` | Feature-orientierte Roadmap und Arbeitsbranch-Reihenfolge |
| `00_project-control/roadmap/roadmap-status.md` | allgemeine Projekt-Roadmap |
| `08_tests/randomizer/190_gui_working_settings_matrix.md` | GUI Working Settings Matrix nach UPR-FVX PR #89 |
| `08_tests/randomizer/191_stable_visual_profile_smoke.md` | Stable-Visual-Profile Kurzsmoke ohne Starters |
| `08_tests/randomizer/192_starter_rival_sync_pass.md` | Starter/Rival Oak-Lab Counter-Slot-Sync nach UPR-FVX PR #97 |
| `08_tests/randomizer/*.md` | Detaildiagnosen, Smoke- und Modellprotokolle |
| `01_docs/NEXT_STEPS.md` | naechster minimaler Arbeitsblock |
| `01_docs/SESSION_STATE.md` | chronologischer Arbeitsstand |

## Snapshot

| Feld | Aktueller Stand |
|---|---|
| Stand | Nach Workspace PR #264 / UPR-FVX PR #97 |
| UPR-FVX-Pin im Workspace | `51d52a03235664154549105003dadfb45c76d0d0` |
| Hauptprofil | Stable Visual Profile plus optional Starter Pokemon |
| Wichtigste Entblockung | Oak-Lab Rival nutzt jetzt den randomisierten Counter-Starter statt Vanilla/Same-Starter |
| Breites GUI-Profil | Wild, Trainer, Movesets, Trainer Movesets, Trainer Names, Items, Shops/Pickup, Abilities, TMs/HMs/Tutors, In-Game Trades, Static, Type Effectiveness, Base Stats, Move Data und Starters lokal gesmoked |
| Keine P1-Promotion | Alle Evidenzen bleiben als lokaler Smoke / getesteter CFRU-DPE-Gen9-Scope dokumentiert, kein Full-Playthrough und keine globale P1-Freigabe |
| Aktuelle Stable-Visual-Caveats | Trainer Class Names OFF fuer visuelle Konsistenz; Special-Wild/Day-Night/Swarms out-of-scope; Rival Carries Starter Through Game ungetestet |
| Naechster sinnvoller Block | Langeres Sampling mit Stable Visual Profile + Starter Pokemon oder gezielt `Rival Carries Starter Through Game` isolieren |

## Statusmodell

| Status | Bedeutung |
|---|---|
| Stable-profile passed | Im aktuellen lokalen Stable-Visual-Profil kurz gesmoked und ohne Blocker beobachtet. Kein Full-Playthrough, keine globale P1-Promotion. |
| Working-matrix passed | In der GUI Working Settings Matrix lokal randomisiert und per Log/Ingame-Smoke bestaetigt. |
| Passed with caveat | Funktioniert im getesteten Scope, hat aber bekannte Grenzen oder Darstellungs-Caveats. |
| Optional / chaos setting | Technisch bestanden, aber stark gameplay-veraendernd oder fuer normale Runs optional. |
| Textlabel-only | Aendert Textlabels, nicht zwangsläufig dahinterliegende IDs/Sprites. |
| Blocked / OFF | Bekannter Fehler oder fuer Stable-Profil bewusst ausgeschaltet. |
| Out of scope | Aktuell nicht Teil des getesteten Profils. |
| Non-ROM only | Nur ROM-frei getestet, noch kein lokaler Output-/Ingame-Smoke. |
| Not started | Noch kein belastbarer Plan/Test/Fix. |

## Empfohlenes Stable Visual Profile

### ON

| Bereich | Einstellung |
|---|---|
| Wild Pokemon | Standard/Fallback Randomization |
| Trainer Pokemon | Trainer Pokemon core |
| Movesets | Pokemon Movesets -> Random completely |
| Trainer Movesets | Better Movesets fuer relevante Trainergruppen |
| Trainer Names | Randomize Trainer Names |
| Starters | Starter Pokemon: Random completely, mit Oak-Lab Rival Counter-Sync |
| Items | Field Items basic, Shop Items, Pickup Items |
| Abilities | Pokemon Abilities randomisieren |
| TM/HM | TM Moves, TM/HM Compatibility |
| Tutors | Move Tutor Moves, Move Tutor Compatibility |
| Trades | In-Game Trades |
| Static | Static Pokemon |
| Types | Type Effectiveness, wenn Chaos-Setting gewollt |
| Traits | Pokemon Base Statistics |
| Move Data | Power, Accuracy, PP, Type, Names |

### OFF / Caveat

| Einstellung | Grund |
|---|---|
| Trainer Class Names | Funktioniert als Textlabel-Remapping, aber Sprite/Class-ID kann optisch mismatched bleiben. Fuer Stable-Visual-Profil standardmaessig OFF. |
| Evolution Randomization | Evolutions unchanged sind stabil preserved; Evolution-Randomization selbst bleibt separater Scope. |
| Rival Carries Starter Through Game | Oak-Lab Rival ist gefixt; Full-Rival-Carry-Pfad noch nicht lokal getestet. |
| Special-Wild / Day-Night / Swarms | Out-of-scope. CFRU `SWARM_CHANCE=0` fuer normales Profil. |
| Field Items Required-TM-Zwang | Kann bei expanded TMs zu `more required TMs than TM field item slots` fuehren; Basic Field Items verwenden. |

## Gesamtfortschritt nach Feature-Paketen

| Paket | Status | Stabil belegt / funktional | Caveat / Luecke | Naechster Schritt | Belege |
|---|---|---|---|---|---|
| General Options | Teilweise | - | Limit/No Premature/Race/Intro nicht im aktuellen Stable-Profil validiert | separater General-Smoke | aeltere Carrier, offen |
| Pokemon Traits | Working-matrix passed fuer Kernteile | Base Stats, Species Types, Abilities; Evolutions unchanged preserved | Evolution-Randomization/Improvement-Slices bleiben separater Scope; Base-Stats-Log kann Ability-Namen kuerzen, ingame OK | Evolution-Randomization isolieren oder laengeres Sampling | 189, 190, 191 |
| Starters, Statics & Trades | Working-matrix passed | Starters random completely + Oak-Lab Rival Counter-Sync; Static Pokemon; In-Game Trades ohne `NEW GIVEN = ?` | Starter Held Items offen; `Rival Carries Starter Through Game` ungetestet; Static null placeholders bleiben null | Stable-Profil mit Starters laenger samplen; danach Full-Rival-Carry separat | 190, 192 |
| Moves & Movesets | Working-matrix passed | Pokemon Movesets, Trainer Movesets, Move Data Power/Accuracy/PP/Type/Names | Filter-/Sanity-Suboptionen nicht alle einzeln P1; keine globale P1-Promotion | laengeres Sampling | 190, 191 |
| Foe Pokemon / Trainer | Working-matrix passed mit Caveat | Trainer Pokemon core, Trainer Movesets, Trainer Names | Trainer Class Names textlabel-only; Sprite/Class-ID mismatch erwartbar; Additional Pokemon/Level/Battle Style nicht im Stable-Profil | Class Assignment/Sprite nur als eigenes Feature, sonst OFF lassen | 190, 191, PRs #83/#85/#86/#87/#88 |
| Wild Pokemon | Working-matrix passed | Standard/Fallback Wild, normale Encounter-Smokes | Special-Wild/Day-Night/Swarms out-of-scope | Special-Wild nur separater Scope | 190, 191 |
| TM/HMs & Tutors | Working-matrix passed | TM Moves, TM/HM Compatibility, Move Tutor Moves, Tutor Compatibility | Keep Field Move / No Game-Breaking / Force Good / Follow Evolutions nicht alle separat validiert | Suboptionen nur bei Bedarf separat | 190 |
| Items | Working-matrix passed mit Caveats | Field Items basic, Shop Items, Pickup Items | Shop evidence: supported/special shops; Field Items Required-TM-Zwang kann blockieren | Field-Item-TM-Overflow separat behandeln, wenn Option gebraucht wird | 190, 191 |
| Types | Working-matrix passed / optional chaos | Type Effectiveness randomisiert und im Kampf nicht blockierend beobachtet | Chaos-Gameplay; nicht fuer jeden Run empfohlen | optional an/aus je Run | 190 |
| Graphics | P2 / Guarded | Sprites/Paletten im Stable-Profil ohne Missing-Sprite-Blocker beobachtet | echte Palette Randomization und Custom Graphics nicht freigegeben | spaeterer P2-Scope | Ogerpon asset fixes, Stable Smoke |
| Misc Tweaks | Not started | - | alle Misc Tweaks offen | Inventar/Slice spaeter | offen |

## GUI-Feature-Gruppen

| GUI-Gruppe | Status | Aktuelle Empfehlung |
|---|---|---|
| General Options | offen / separater Smoke | Im Stable-Profil nicht breit aktivieren, ausser bekannte benoetigte Optionen. |
| Pokemon Base Stats | Working-matrix passed | Kann in Stable-Visual-Profil verwendet werden; Log-Ability-Namen-Caveat beachten. |
| Pokemon Types | Working-matrix passed | Species Type Randomization nutzbar; Force Dual/Folgeoptionen separat pruefen. |
| Pokemon Abilities | Working-matrix passed | Nutzbar; Ingame-Ability-Namen/Trigger bestaetigt. |
| Evolutions | Unchanged preserved, Randomization separat | Evolution Randomization im Stable-Profil OFF lassen, bis eigener Smoke erfolgt. |
| Starters | Working-matrix passed | Starter Pokemon kann optional ON; Oak-Lab Rival Counter-Slot ist gefixt. |
| Static/Gift | Working-matrix passed mit Caveat | Nutzbar; null placeholders bleiben null. |
| In-Game Trades | Working-matrix passed | Nutzbar; PR #89 verhindert `NEW GIVEN = ?`. Nickname/OT/IV/Item bleiben separate Detailpfade. |
| Trainer Pokemon | Working-matrix passed | Trainer core und Trainer Movesets nutzbar. |
| Trainer Names | Working-matrix passed | Nutzbar. |
| Trainer Class Names | Passed with caveat / textlabel-only | Fuer visuelle Konsistenz OFF; ON nur wenn Textlabel/Sprite-Mismatch akzeptiert wird. |
| Wild Pokemon | Working-matrix passed | Standard/Fallback Wild nutzbar. Special-Wild weiterhin OFF. |
| Pokemon Movesets | Working-matrix passed | Random completely nutzbar. |
| Move Data | Working-matrix passed | Power/Accuracy/PP/Type/Names nutzbar. |
| TM/HM | Working-matrix passed | TM Moves und TM/HM Compatibility nutzbar. |
| Tutors | Working-matrix passed | Move Tutor Moves und Compatibility nutzbar. |
| Items | Working-matrix passed mit Caveats | Field basic, shops, pickup nutzbar; Required-TM-Zwang vermeiden. |
| Type Effectiveness | Optional / chaos passed | Nutzbar, aber stark gameplayveraendernd. |
| Palettes/Graphics | P2 / nicht freigegeben | Echte Randomization nicht in Stable-Profil aufnehmen. |
| Misc Tweaks | Not started | Spaeter inventarisieren. |

## Feature-Liste kompakt

| Feature / Cluster | Dashboard-Status | Scope / Hinweis |
|---|---|---|
| Limit Pokemon | Carrier / offen fuer neues Stable-Profil | General-Option separat pruefen |
| No Premature Evolutions | Carrier / offen fuer neues Stable-Profil | General-Option separat pruefen |
| No Random Intro Mon | Not started | General-Option |
| Race Mode | Not started | General-Option |
| Base Stats Shuffle/Random | Working-matrix passed | Ingame OK, Log-Ability-Namen koennen gekuerzt sein |
| Base Stats Follow Evolutions / Added Stats | Plan / nicht im Stable-Profil | separater Trait-Scope |
| EXP Curves / Update Base Stats to Generation | Not started | Writer-Scope |
| Pokemon Types randomisieren | Working-matrix passed | Stable-faehig im getesteten Scope |
| Force Dual Types | Plan / nicht im Stable-Profil | separater Type-Scope |
| Abilities randomisieren | Working-matrix passed | Ingame-Trigger bestaetigt |
| Ability Filter/Follow-Evo-Suboptionen | geplant / nicht breit getestet | separat |
| Evolutions unchanged preserved | Working-matrix passed | Row-stride fix belegt |
| Evolution Randomization | Separater Scope | Stable-Profil OFF |
| Change Impossible / Make Easier / Time-Based | Non-ROM/Plan, kein Stable-Smoke | separat |
| Starter Random Completely | Working-matrix passed | Oak-Lab Rival Counter-Sync passed |
| Starter Filter/BST/Legendary | Carrier / offen | separat bei Bedarf |
| Starter Held Items | Not started | Writer/Item-Scope |
| Static Pokemon Random | Working-matrix passed with caveat | null placeholders bleiben null |
| In-Game Trades Species | Working-matrix passed | kein `NEW GIVEN = ?` nach PR #89 |
| In-Game Trades Text/OT/IV/Item | offen | Detailpfad, nicht gesondert validiert |
| Move Power/Accuracy/PP/Types | Working-matrix passed | Ingame Move-Screen/Battle OK |
| Move Names | Working-matrix passed | Text/UI kurz gesmoked |
| Update Moves to Generation | offen | nicht Teil des aktuellen Stable-Smokes |
| Pokemon Movesets | Working-matrix passed | Random completely nutzbar |
| Moveset Filter/Sanity-Suboptionen | geplant/offen | separat |
| Trainer Pokemon core | Working-matrix passed | Stable-faehig im getesteten Scope |
| Trainer Movesets | Working-matrix passed | genutzt im Stable-Profil |
| Trainer Names | Working-matrix passed | Text sichtbar geaendert |
| Trainer Class Names | Textlabel-only / Caveat | Sprite/Class-ID mismatch erwartbar; OFF fuer Stable-Visual |
| Trainer Class Assignment/Sprite sync | Future feature | nicht gleiche Option wie Class Names |
| Rival Carries Starter Through Game | Nicht getestet | separater Full-Rival-Pfad |
| Trainer Additional Pokemon/Level/Battle Style | Non-ROM/Backlog | separat |
| Wild Standard/Fallback | Working-matrix passed | Stable-faehig |
| Wild Similar Strength/Restrictions | Carrier/Backlog | nicht Hauptprofil |
| Wild Held Items | Working-matrix passed falls im Profil genutzt | keine neuen Blocker beobachtet |
| Special-Wild/Day-Night/Swarms | Out of scope | Swarms via CFRU `SWARM_CHANCE=0` deaktiviert |
| TM Moves | Working-matrix passed | TM01-TM120 im Log |
| TM/HM Compatibility | Working-matrix passed | per Species im Log |
| TM Keep Field/No-Breaking/Force Good/Follow | geplant/offen | Required-TM-Zwang mit expanded TMs vorsichtig |
| Move Tutor Moves | Working-matrix passed | nutzbar |
| Move Tutor Compatibility | Working-matrix passed | nutzbar |
| Special Tutors/Text/Menu | P2 | out-of-scope |
| Field Items basic | Working-matrix passed | Ingame andere Items beobachtet |
| Field Items required TM placement | Blocker/Caveat | `more required TMs than TM field item slots` moeglich |
| Shop Items | Working-matrix passed with caveat | supported/special shops bestaetigt |
| Pickup Items | Working-matrix passed | Log-confirmed |
| Type Effectiveness | Optional chaos passed | Random chart + battle smoke |
| Pokemon Palettes Random | P2 / Write modelliert | nicht in Stable-Profil |
| Custom Player Graphics / Sprites | P2 | nicht begonnen |
| Misc Tweaks | Not started | spaeter inventarisieren |

## Offene Arbeitsbloecke

| Prioritaet | Block | Ziel |
|---|---|---|
| 1 | Stable Visual Profile + Starters laenger samplen | Breiten Run mit aktuell groesstem funktionierenden Profil absichern. |
| 2 | Rival Carries Starter Through Game | Separat testen; nicht mit Oak-Lab-Fix gleichsetzen. |
| 3 | Evolution Randomization | Separater Smoke fuer aktive Evolution-Randomization und Methoden-/Improvement-Suboptionen. |
| 4 | Trainer Class Assignment / Sprite sync | Neues Feature, falls visuell passende random Trainerklassen gewuenscht sind. |
| 5 | Field Items Required-TM Overflow | Suboption absichern oder UI/Fehlermeldung verbessern. |
| 6 | Special-Wild / Day-Night / Swarms | Nur bei Bedarf, getrennt vom normalen Stable-Profil. |
| 7 | Graphics/Palettes/Misc Tweaks | P2-Inventar und spaetere Slices. |

## Nicht dokumentieren / Sicherheitsregeln

- Keine ROMs, Output-ROMs, Saves, Emulator States, Screenshots, private Pfade, Hashes, vollstaendige Logs, Secrets, Tokens oder `.env`-Dateien committen.
- Stable-Visual-Profile-Pass ist ein lokaler Smoke, kein Full-Playthrough und keine P1-Promotion.
- `main` bleibt stabil; neue Codearbeiten weiter ueber Branches und PRs.
