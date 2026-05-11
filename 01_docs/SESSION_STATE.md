# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- Workspace PR #29 ist gemerged; das CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand bleibt in diesem Workspace auf `223ee9ef compat: preserve CFRU DPE species identity`.
- Die neu eingebundenen NatDex-/Randomizer-/FireRed-Referenz-Submodules sind in `main` verfuegbar und wurden read-only inventarisiert.
- Die projektrelevanten Befunde aus `02_external/CFRU-expansion/CFRU Documentation.pdf` sind als dauerhaftes Referenzdokument extrahiert.
- devkitPro/devkitARM wurde lokal installiert und geprueft.
- DPE Gen9 baut lokal erfolgreich.
- CFRU auf DPE baut lokal erfolgreich.
- UPR-FVX wurde aus Source gebaut und startet.
- UPR-FVX kann die CFRU/DPE-ROM laden, minimal randomisieren und speichern.
- BizHawk bootet die randomisierte ROM; neues Spiel, Starterwahl und Rivalenkampf funktionieren.
- Wild-Encounter-Randomization funktioniert fuer Vanilla-/Fallback-Encounter-Tabellen.
- Route 1 wurde fuer den Randomizer-Kompatibilitaetsbuild per `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` auf Vanilla/Fallback-Wilddaten zurueckgefuehrt.
- PR #3 behebt den SpeciesSet-Kollaps: `speciesList.size` steigt im Diagnosebefund von `412` auf `799`, `maxSpeciesIdentityNumber=823`, Skrelp bis Hawlucha werden Gen6 statt Gen3.
- Der finale Wild-Randomizer-Pool bleibt im dokumentierten Gen4+-Diagnoselauf auf Gen1-3 begrenzt, weil `Settings.tweakForRom()` Gen3-ROMs auf `generationOfPokemon() == 3` kappt und `GameRandomizer.setupSpeciesRestrictions()` diese Restrictions auch bei `limitPokemon=false` setzt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/cfru-documentation-randomizer-relevance`

## Aktueller Arbeitsblock

Read-only Extraktion der projektrelevanten CFRU-Documentation-PDF-Befunde fuer UPR-FVX/CFRU/DPE-Kompatibilitaet.

## Ziel

Konkret klaeren:

- welche CFRU-Dokumentationspunkte fuer Randomizer-Kompatibilitaet dauerhaft relevant sind
- welche CFRU-Runtime-Systeme nicht mit dem P0-GenRestrictions-Fix vermischt werden duerfen
- welche Folgen sich fuer P0/P1/P2/P3/P4 ergeben
- welche Source-of-Truth-Pfade aus der CFRU-Dokumentation spaeter wichtig werden

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Branch `analysis/cfru-documentation-randomizer-relevance` von aktuellem `main` erstellt.
- Pflichtdokumente und bestehende Kompatibilitaetsmodelle gelesen.
- `02_external/CFRU-expansion/CFRU Documentation.pdf` read-only ausgewertet.
- Neues Referenzdokument erstellt: `01_docs/compat/cfru-documentation-randomizer-relevance.md`.
- Bestehendes Kompatibilitaetsmodell um einen Querverweis auf das neue CFRU-Doku-Relevanzdokument ergaenzt.
- Keine Codeaenderungen vorgenommen.
- Keine Builds gestartet.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade gelesen, kopiert, geaendert oder committed.

## Ergebnis

- CFRU Documentation bestaetigt die DPE-before-CFRU-Reihenfolge und die Trennung zwischen DPE-Datenmodell und CFRU-Laufzeitmodell.
- `SPECIES_NONE=0` bestaetigt die Nullslot-Interpretation fuer `<unknown>` mit `rawInternalSpeciesId=0`.
- CFRU hat eigene Runtime-Randomizer-Flags und Banlisten; diese sind nicht identisch mit UPR-FVX-Offline-Randomisierung.
- CFRU-Time-of-Day-Wild-Header, Swarms und Roamers sind separate Wild-Systeme und bleiben ausserhalb von P0.
- Hidden Ability im BaseStats-Byte `0x1A`, `TRAINERS_WITH_EVS`, TM/HM/Tutor-Erweiterung und `EXPAND_MOVESETS` vs. DPE-Learnsets sind P1-Risiken.
- Save Expansion und Roamer-Speicher machen RAM-/Ironmon-Mapping relevant, aber erst als P4.
- P0 bleibt: erweiterte CFRU/DPE-BPRE-Hacks duerfen im finalen `RestrictedSpeciesService` nicht mehr blind auf Gen1-3 gekappt werden.

## Noch nicht gestartet

- UPR-FVX-Fix fuer CFRU/DPE-Generation-Restrictions
- Trainer-/Starter-/Evolution-/Learnset-Diagnosen nach PR #3
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen oder gelesen.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Codeaenderungen in `02_external/**`.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

`compat/upr-fvx-cfru-dpe-gen-restrictions`

Zweck: Im UPR-FVX-Fork verhindern, dass erweiterte CFRU/DPE-BPRE-Hacks trotz erweitertem Species-Pool durch `Settings.tweakForRom()` und `RestrictedSpeciesService` auf Gen1-3 begrenzt werden.
