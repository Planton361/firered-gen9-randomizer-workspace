# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- Workspace PR #29 ist gemerged; das CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der SpeciesSet-Identity-Fix ist in `compat/firered-gen9-cfru-dpe` enthalten.
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
- UPR-FVX PR #4 ist gemerged; der P0-GenRestrictions-Fix entfernt die Gen1-3-Kappung fuer erweiterte CFRU/DPE-BPRE-Hacks und setzt bei `limitPokemon=false` den unrestricted Pool.
- UPR-FVX PR #5 ist gemerged; der Gen3/CFRU-DPE-Wild-Write-Fix schreibt Vanilla/Fallback-Wild-Encounters fuer erweiterte BPRE-Hacks ueber interne SpeciesSet-Identitaet statt `pokedexToInternal[Species.number]`.
- Der Post-Merge-P0-Smoke auf UPR-FVX Merge-Commit `843b75a8` bestaetigt die Fixkette PR #3/#4/#5: sichtbarer Wild-Log Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- UPR-FVX PR #6 ist gemerged; der Starter-Write-Fix schreibt Starter fuer erweiterte BPRE-Hacks ueber interne SpeciesSet-Identitaet und erhaelt Pawniard/Scraggy im Reload.
- Gen9-Species-Coverage ist read-only analysiert: DPE/CFRU-Source reicht bis `SPECIES_PECHARUNT = 0x59F` / `NUM_SPECIES = 1440`, der aktuelle FVX-Load bleibt aber bei `PokemonCount=823` und erreicht damit keine Gen7-Gen9-Species.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-gen9-species-coverage`

## Aktueller Arbeitsblock

Read-only Gen9-Species-Coverage-Diagnose fuer den aktuellen CFRU/DPE-Teststand.

## Ziel

Konkret klaeren:

- welchen Species-Umfang DPE Gen9 und CFRU-expansion im Source definieren
- warum UPR-FVX im aktuellen Diagnosebefund nur `PokemonCount=823` laedt
- welche Rolle `PokemonNames`, `PokemonMovesets`, `PokedexOrder`, `PokemonStats`, `SpeciesIDs.java` und `GenRestrictions` spielen
- welche naechste lokale ROM-Diagnose die konkrete Count-Abbruchursache klaeren muss

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-gen9-species-coverage` erstellt.
- DPE/CFRU-Header und Tabellen read-only geprueft: `SPECIES_ROWLET = 0x3AB`, `SPECIES_GROOKEY = 0x44E`, `SPECIES_SPRIGATITO = 0x50E`, `SPECIES_PECHARUNT = 0x59F`, `NUM_SPECIES = SPECIES_PECHARUNT + 1`.
- DPE/CFRU-Pokedex-Konstanten read-only geprueft: National-Dex bis Terapagos `1024` und Pecharunt `1025`.
- DPE/CFRU-Tabellen-Coverage read-only geprueft: BaseStats, Learnsets, Species-to-Dex und Pokedex-Orders enthalten Gen7-Gen9-Belege.
- UPR-FVX `Gen3RomHandler.basicBPRE10HackSupport()` read-only analysiert: `PokemonCount` entsteht aus Name-Scan, Moveset-Pointer-Kappung und PokedexOrder-Sanity.
- UPR-FVX `SpeciesIDs.java`, `generationOf()` und `GenRestrictions` read-only geprueft.
- CyanSMP64 NatDex-Strategie read-only verglichen.
- Neues Analysemodell erstellt: `01_docs/compat/upr-fvx-cfru-dpe-gen9-species-coverage.md`.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**` umgesetzt.

## Ergebnis

- Erwarteter Source-Umfang: DPE/CFRU bis `SPECIES_PECHARUNT = 0x59F` und `NUM_SPECIES = 1440` interne Slots.
- Tatsaechlicher FVX-Load-Umfang: `PokemonCount=823`, `speciesList.size=799`, sichtbarer Pool Gen1-Gen6, Gen7+ `0`.
- `PokemonCount=823` liegt bei interner ID `0x337`; `SPECIES_XERNEAS = 0x338` waere bereits ausserhalb des Loads, Gen7 startet erst bei `SPECIES_ROWLET = 0x3AB`.
- Wahrscheinlichster Engpass ist die FVX-BPRE-Hack-Heuristik vor dem eigentlichen Species-Load: `PokemonNames`, `PokemonMovesets` oder `PokedexOrder` kappt den Count.
- `SpeciesIDs.java` kennt Gen8/Gen9 und `generationOf()` kann Gen9 klassifizieren, sobald Species geladen sind; `GenRestrictions.MAX_GENERATION=7` bleibt aber ein spaeteres Gen9-Settings-Risiko.
- Naechste Diagnose muss lokal mit ROM den konkreten Count-Abbruchgrund loggen.

## Noch nicht gestartet

- Lokale Count-Abbruchdiagnose um interne IDs `820..900`
- Praktische P1-Diagnoselaeufe fuer Static/Gifts und Trainer-Species
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. In diesem Arbeitsblock wurde kein ROM gelesen.

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

`analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics`

Zweck: lokale ROM-Diagnose fuer den konkreten `PokemonCount=823`-Abbruchgrund in `basicBPRE10HackSupport()`. Keine Gen9-Fixes, keine Static/Gift-Fixes und keine ROM-/Build-Artefakte committen.
