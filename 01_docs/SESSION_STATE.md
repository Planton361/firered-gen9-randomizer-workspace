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
- Der Save-/Moveset-Blocker nach Palette-Load ist read-only modelliert: `saveTrainers()` ruft beim Speichern `trainerPokemonToBytes()` fuer jeden Trainer auf, und dieser Pfad laedt aktuell die globale Learnset-Map ueber `getMovesLearnt()`.
- Der Fehlerpointer `0x25e49c` entspricht `PokemonMovesets + 826 * 4`; interne ID `826` ist im DPE/CFRU-Modell `SPECIES_ZYGARDE`. Der Blocker ist damit sehr wahrscheinlich ein falscher/alter `PokemonMovesets`-/Learnset-Tabellenzugriff, nicht ein neuer SpeciesCount- oder Palette-Fehler.
- DPE/CFRU-Source enthaelt Gen7-Gen9-Learnsets in `gLevelUpLearnsets` mit 3-Byte-LevelUpMove-Format bis Pecharunt; FVX erkennt im aktuellen Befund aber `jamboMovesetHack=false` und liest eine nicht passende Tabelle/Formatannahme.
- UPR-FVX PR #10 ist offen; der Lazy-Trainer-Movesets-Unblocker laedt `getMovesLearnt()` in `trainerPokemonToBytes()` nur noch, wenn ein Trainer-Pokemon mit Custom-Moves tatsaechlich `resetMoves=true` hat.
- Lokaler Diagnosebefund nach PR #10: `saveTrainers()`/`getMovesLearnt()` blockiert nicht mehr bei `0x25e49c`; `PokemonCount=1439`, `speciesList.size=1415` und Gen7/8/9-Coverage bleiben erhalten.
- Neuer Folgeblocker nach PR #10: `savePokemonPalettes()` bricht mit `no compressed data found at offset 0x16b9c08` ab; `saveSuccessful=false`, daher entsteht weiterhin kein nutzbarer Wild-Log.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-lazy-trainer-movesets`

## Aktueller Arbeitsblock

Dokumentation des UPR-FVX-Lazy-Trainer-Movesets-Unblockers und des lokalen Diagnosebefunds.

## Ziel

Konkret festhalten:

- welcher UPR-FVX-Commit den Trainer-Save-Pfad lazy macht
- ob `saveTrainers()`/`getMovesLearnt()` weiter bei `0x25e49c` blockiert
- ob `PokemonCount=1439` und Gen7/8/9-Coverage erhalten bleiben
- welcher neue nachgelagerte Blocker nach `saveTrainers()` sichtbar wird

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-lazy-trainer-movesets` erstellt.
- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-lazy-trainer-movesets` von `compat/firered-gen9-cfru-dpe` erstellt.
- UPR-FVX Commit `29c34084 compat: lazily load trainer movesets for CFRU DPE` erstellt und PR #10 geoeffnet.
- UPR-FVX `./gradlew test` und `./gradlew clean :random:jar` ausgefuehrt.
- Lokalen CFRU/DPE-CLI-Lauf und JShell-Result-Auswertung gestartet; Save-Trainers-Unblock und neuen Palette-Save-Blocker dokumentiert.
- Neues Protokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.md`.

## Ergebnis

- `trainerPokemonToBytes()` laedt `getMovesLearnt()` nur noch lazy fuer echte `resetMoves`-Faelle.
- Der lokale Lauf blockiert nicht mehr in `saveTrainers()`/`getMovesLearnt()` am Pointer `0x25e49c`.
- Count und Coverage bleiben stabil: `PokemonCount=1439`, `speciesList.size=1415`, `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`.
- Es gibt weiterhin keinen nutzbaren Wild-Log, weil `savePokemonPalettes()` spaeter mit `no compressed data found at offset 0x16b9c08` abbricht.
- Der volle DPE/CFRU-Learnset-Loader bleibt ein separates Folgepaket.

## Noch nicht gestartet

- UPR-FVX-Review/Merge von PR #8
- UPR-FVX-Review/Merge von PR #9
- UPR-FVX-Review/Merge von PR #10
- Separates Modell oder Diagnose fuer `savePokemonPalettes()` bei `0x16b9c08`
- Separates DPE/CFRU-Learnset-Profil fuer `gLevelUpLearnsets`
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

UPR-FVX-Codeaenderung erfolgte nur im Submodule auf Arbeitsbranch `compat/upr-fvx-cfru-dpe-lazy-trainer-movesets`; Workspace dokumentiert den Submodule-Pointer.

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

`analysis/upr-fvx-cfru-dpe-palette-save-blocker`

Zweck: neuen `savePokemonPalettes()`-Blocker bei `0x16b9c08` separat diagnostizieren. Kein Count-, Learnset-, Trainer-, Static-/Gift-, Wild- oder Day/Night-Fix im selben Branch.
