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
- DPE/CFRU-`PokedexOrder` ist read-only modelliert: DPE Order-Tabellen sind Species-ID-Sortierlisten fuer Dex-Views, nicht FVX-kompatible interne-Species-zu-Dex-ID-Mappings.
- UPR-FVX PR #8 ist offen; der konservative CFRU/DPE-Gen9-Count-Fix setzt `PokemonCount=1439` ueber `PokemonNames` plus BaseStats-Sanity und laesst Gen7/8/9 im Species-Load sichtbar werden.
- Lokaler Diagnosebefund nach PR #8: `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`.
- Neuer Folgeblocker: Der vollstaendige CLI-Lauf bricht nach erfolgreichem Species-Load in `loadPokemonPalettes()` mit einem ungueltigen Pointer ab; Wild-Randomization wird in diesem Arbeitsblock deshalb noch nicht erreicht.
- Der Paletten-Loader-Blocker ist read-only modelliert: `0x1a495d8` entspricht DPE `gMonPaletteTable + 1038 * 8`, also `SPECIES_CUBONE_A`; dieser Palette-Slot ist in DPE `Palette_Table.c`/`Shiny_Palette_Table.c` nicht initialisiert.
- UPR-FVX PR #9 ist offen; der defensive Palette-Load/-Save-Fix ueberspringt fuer den CFRU/DPE-Gen9-BPRE-Modus fehlende Pokemon-Palette-Slots statt den ROM-Load abzubrechen.
- Lokaler Diagnosebefund nach PR #9: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`, Palette-Load ueberspringt `normal=2` und `shiny=2` Slots.
- Neuer Folgeblocker nach Palette-Load: Save bricht vor Wild-Log-Erzeugung in `saveTrainers()`/`getMovesLearnt()` mit ungueltigem Pointer `0x25e49c` ab; das ist kein Palette-Fix-Bestandteil.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-defensive-palette-loading`

## Aktueller Arbeitsblock

Dokumentation und Diagnose zum defensiven UPR-FVX-Palette-Load/-Save-Fix fuer CFRU/DPE-Gen9-BPRE.

## Ziel

Konkret festhalten:

- welcher UPR-FVX-Fixbranch fehlende Palette-Slots defensiv behandelt
- welche Palette-Slots lokal uebersprungen werden
- ob `PokemonCount=1439` und Gen7/8/9-Coverage erhalten bleiben
- welcher nachgelagerte Blocker nach dem Palette-Load sichtbar wird

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-defensive-palette-loading` erstellt.
- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-defensive-palette-loading` von `d17b29a2` erstellt, weil PR #8 noch nicht in `compat/firered-gen9-cfru-dpe` gemerged ist.
- UPR-FVX Commit `17e47254 compat: tolerate CFRU DPE missing pokemon palettes` erstellt und PR #9 geoeffnet.
- UPR-FVX `./gradlew test` und `./gradlew clean :random:jar` ausgefuehrt.
- Lokalen CFRU/DPE-CLI-Lauf gestartet; Palette-Load-Diagnose protokolliert, nachgelagerten `saveTrainers()`-/Learnset-Abbruch dokumentiert.
- Neues Protokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md`.

## Ergebnis

- Der Palette-Load bricht nicht mehr bei `gMonPaletteTable[1038]` / `SPECIES_CUBONE_A` ab.
- Die lokale Diagnose meldet uebersprungene Palette-Slots: normal `2`, shiny `2`; Beispiele sind `Cubone`/Identity `1038` und `Oricorio`/Identity `1043`, jeweils mit Tabellenindex `1038`.
- `PokemonCount=1439` und Gen7/8/9-Species-Coverage bleiben erhalten.
- Es gibt noch keinen neuen Wild-Log, weil der Save danach in `saveTrainers()`/`getMovesLearnt()` am Pointer `0x25e49c` abbricht.

## Noch nicht gestartet

- UPR-FVX-Review/Merge von PR #8
- UPR-FVX-Review/Merge von PR #9
- Separates Modell oder Diagnose fuer `saveTrainers()`/`getMovesLearnt()` bei `PokemonCount=1439`
- Praktische P1-Diagnoselaeufe fuer Static/Gifts und Trainer-Species
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. ROMs wurden nur lokal fuer den Diagnose-Lauf geladen; Artefakte blieben unter `05_builds/**` und wurden nicht committed.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX-Codeaenderung erfolgte nur im Submodule auf Arbeitsbranch `compat/upr-fvx-cfru-dpe-defensive-palette-loading`; Workspace dokumentiert den Submodule-Pointer.

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

Zweck: `saveTrainers()`/`getMovesLearnt()`-Blocker nach `PokemonCount=1439` separat diagnostizieren oder modellieren. Kein Palette-, Count-, Static-/Gift-, Wild- oder Day/Night-Fix im selben Branch.
