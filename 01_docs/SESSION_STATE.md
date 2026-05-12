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
- UPR-FVX PR #7 ist offen; temporaere `[CFRU-DPE-COUNT-DIAG]`-Ausgaben belegen im lokalen CFRU/DPE-Teststand die konkrete `PokemonCount=823`-Kappung.
- Lokale Count-Diagnose: `PokemonNames` erreicht ID `1439` / Pecharunt, der Moveset-Check kappt `1439 -> 930`, und der `PokedexOrder`-Check kappt wegen `pdEntry=1808` bei interner ID `824` final auf `823`.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics`

## Aktueller Arbeitsblock

Dokumentation der lokalen UPR-FVX-Count-Abbruchdiagnose fuer den aktuellen CFRU/DPE-Teststand.

## Ziel

Konkret dokumentieren:

- welche temporaeren UPR-FVX-Diagnoseausgaben fuer `basicBPRE10HackSupport()` ergaenzt wurden
- welcher Tabellencheck den finalen `PokemonCount=823` verursacht
- welche Diagnosewerte fuer interne IDs `800..900` und `1000..1050` sichtbar sind
- welche Folgeanalyse vor einem Gen9-Fix noetig ist

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics` erstellt.
- UPR-FVX-Submodule `origin` als `Planton361/universal-pokemon-randomizer-fvx` geprueft.
- UPR-FVX-Basisbranch `compat/firered-gen9-cfru-dpe` aktualisiert und Branch `analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics` erstellt.
- In UPR-FVX nur `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` geaendert.
- Temporaere stderr-Diagnose `[CFRU-DPE-COUNT-DIAG]` in `basicBPRE10HackSupport()` ergaenzt; keine funktionale Count-Logik geaendert.
- UPR-FVX mit `./gradlew clean :random:jar` erfolgreich gebaut.
- Lokalen CFRU/DPE-Teststand nur bis ROM-Load/Randomizer-CLI-Diagnose ausgefuehrt; lokale Artefakte blieben unter `05_builds/**` und wurden nicht committed.
- Ergebnisdokument erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics.md`.

## Ergebnis

- Direkte Cutoff-Ursache: `PokedexOrder` liefert bei interner ID `824` den Wert `1808`; die aktuelle FVX-Heuristik `pdEntry > 1023` setzt deshalb `iPokemonCount = 823`.
- `PokemonNames` ist nicht die Ursache: der Name-Scan erreicht `nameScanStopIndex=1440`, ID `1439` ist `Pecharunt`, Dummy-Abzug `false`.
- `PokemonStats` ist nicht die unmittelbare Ursache: Stats sind in den Probe-Ranges ueber ID `823` hinaus plausibel lesbar.
- `PokemonMovesets` ist ein zweiter Tabellenkompatibilitaetsbefund: der Rueckwaertscheck kappt `1439 -> 930`, erklaert aber nicht den finalen Wert `823`.
- Tatsaechlicher FVX-Load bleibt `PokemonCount=823`, `speciesList.size=799`, `maxInternalSpeciesId=823`, `maxSpeciesNumber=411`, sichtbarer Pool Gen1-Gen6.
- UPR-FVX PR #7 ist erstellt: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/7`.

## Noch nicht gestartet

- Fix-/Analysemodell fuer DPE/CFRU-`PokedexOrder` vs. FVX-Count-Heuristik
- Praktische P1-Diagnoselaeufe fuer Static/Gifts und Trainer-Species
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. In diesem Arbeitsblock wurde ein lokaler CFRU/DPE-Teststand nur fuer die Count-Diagnose gelesen; keine ROMs oder Build-Artefakte wurden committed.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX-Codeaenderung nur im Submodule-Branch und nur temporaere Diagnoseausgabe; Workspace committed nur Dokumentation und den Submodule-Pointer.

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

Noch festzulegen.

Zweck: DPE/CFRU-`PokedexOrder`-Offset und eine saubere Count-Quelle fuer Gen9-Coverage modellieren. Keine Static-/Gift-Fixes starten, bis die Count-Heuristik entschieden ist.
