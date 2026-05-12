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
- Der Palette-Save-Blocker ist read-only modelliert: `0x16b9c08` ist das alte Palette-Datenziel `gFrontSprite252Pal` (`0x096B9C08`), das DPE fuer die Gap-/Dummy-Slots `[252]..[276]` mehrfach verwendet. FVX schreibt Paletten auch ohne Palette-Randomization neu und verletzt damit die `DataRewriter`-Annahme, dass nur ein Pointer auf den alten komprimierten Datenblock zeigt.
- UPR-FVX PR #11 ist gemerged; der Skip-Unchanged-Palette-Save-Unblocker ist in `compat/firered-gen9-cfru-dpe` enthalten.
- Post-Merge-Gen9-Wild-Smoke auf UPR-FVX Merge-Commit `ee82cb4e` ist dokumentiert: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, `generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}`, Output-ROM und Wild-Log entstehen erfolgreich.
- Der Post-Merge-Wild-Log enthaelt Gen7/8/9-Species, darunter `Magearna`, `Meltan`, `Hatenna`, `Calyrex`, `Glimmet`, `Toedscool`, `Tatsugiri`, `Floragato`, `Iron Crown` und `Hydrapple`; `<unknown>` bleibt `0`.
- Im Post-Merge-Wild-Log erscheinen `12` `Bad Egg`-Eintraege; diese sind eine separate Folgeauffaelligkeit und nicht der fruehere `<unknown>`-Nullslot.
- Randomizer-Smoke-Artefakte wurden lokal bereinigt: `05_builds` sank von `1.3G` auf `196M`; der alte flache `05_builds/randomizer-smoke/`-Output ist leer.
- `08_tests/randomizer/README.md` dokumentiert ab jetzt Nummerierungs- und Latest-Konvention fuer Randomizer-Smoke-Protokolle und lokale Artefaktordner.
- UPR-FVX PR #12 ist offen; der CFRU/DPE-spezifische Wild-Ban entfernt im erkannten Gen9-BPRE-Modus `SPECIES_EGG=0x19C` aus dem Wild-Allowed-Pool, ohne Vanilla/normal Gen3 zu aendern.
- Lokaler Diagnosebefund nach PR #12: `Bad Egg` faellt von `12` auf `0`, `<unknown>` bleibt `0`, `saveSuccessful=true`; `Area #174 - ALTERING CAVE Grass/Cave` enthaelt statt `Bad Egg` jetzt `Meowscrada` in allen 12 Slots.
- Workspace PR #56 ist gemerged; `main` pinnt `02_external/upr-fvx` auf `0f127e9b`.
- Static/Gift Species-only Diagnose auf UPR-FVX `0f127e9b`: Static/Gift-Pool erreicht Gen1-Gen9 (`staticPool.size=1414`), der Pick-Pfad erreicht Gen7/8/9 (`pickedGen4plus=18`, `pickedGen7plus=8`), aber der echte Lauf bricht vor Save/Log an vier `<null>`-Static-Eintraegen ab (`saveSuccessful=false`).
- UPR-FVX-Commit `009178e8` behebt den Static/Gift-Scope- und Species-Write-Pfad fuer CFRU/DPE: Null-Static-Eintraege blockieren nicht mehr, echte Static/Gift-Species schreiben ueber interne SpeciesSet-Identitaet.
- Lokaler Diagnosebefund nach `009178e8`: `saveSuccessful=true`, Log nicht leer, Output-ROM erzeugt, Gen7/8/9-Picks sichtbar und `writeReloadMismatches=0`.
- Workspace PR #58 ist gemerged; `main` pinnt `02_external/upr-fvx` auf `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`.
- Trainer-Species-only Diagnose auf UPR-FVX `009178e8`: Trainer-Pool erreicht Gen1-Gen9 (`trainerPool.size=1414`), Trainer-Load funktioniert (`trainers=255`, `trainerPokemon=481`, `nullSpecies=0`), aber `randomizeTrainerPokes()` haengt vor Save/Log in `getRandomAbilitySlot()` auf Zero-Ability-Sonder-Species.
- Im Trainer-Pool liegen acht Zero-Ability-/Zero-BST-Sonder-Species, darunter `Bad Egg`, zwei Zygarde-Sonderslots und vier Gen9-Ogerpon-Formslots; Output-ROM und Trainer-Log entstehen nicht.
- UPR-FVX-Commit `56ec749e` behebt den Trainer-Species-Scope und Trainer-Species-Write-Pfad fuer CFRU/DPE: nicht kampffaehige Sonder-Species werden aus dem Trainer-Replacement-Pool entfernt, `getRandomAbilitySlot()` laeuft nicht mehr endlos, und echte Trainer-Species schreiben ueber interne SpeciesSet-Identitaet.
- Lokaler Diagnosebefund nach `56ec749e`: `saveSuccessful=true`, Log nicht leer, Output-ROM erzeugt, Gen7/8/9-Picks sichtbar und `writeReloadMismatches=0`.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`compat/upr-fvx-cfru-dpe-trainer-scope-and-write`

## Aktueller Arbeitsblock

P1 Trainer-Scope und Trainer-Species-Write fuer CFRU/DPE.

## Ziel

Trainer-Species-only gezielt entblocken: nicht kampffaehige Sonder-Species aus dem CFRU/DPE-Trainer-Replacement-Pool ausschliessen, Zero-Ability-Species defensiv behandeln und Trainer-Species-Write/Reload ueber interne SpeciesSet-Identitaet bestaetigen. Trainer-Movesets, Held Items, Learnsets, allgemeine Ability-Randomization, Wild, Starter und Static/Gift bleiben ausserhalb dieses Blocks.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #59 als gemerged geprueft.
- `main` per Fast-Forward aktualisiert und Branch `compat/upr-fvx-cfru-dpe-trainer-scope-and-write` erstellt.
- UPR-FVX-Submodule geprueft: Planton361-Fork, Basis-Commit `009178e8848b4272e6b8be54a8bf5b2bed34d5f2`, neue Branch `compat/upr-fvx-cfru-dpe-trainer-scope-and-write`.
- UPR-FVX-Fix umgesetzt und committed: `56ec749eca12a8637c20f943b520a9bb6a9d469a`.
- UPR-FVX PR #14 erstellt: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/14`.
- Trainer-Species-only Settings mit Seed `274269061345323` lokal erneut ausgefuehrt.
- Pool-, Trainer-Log- und Write/Reload-Diagnosen mit temporaeren Helpers ausserhalb des Repos erstellt.
- Neues Protokoll erstellt: `08_tests/randomizer/024_trainer_scope_write_diagnostics.md`.
- `08_tests/randomizer/README.md` auf Latest Nr. 024 aktualisiert.

## Ergebnis

- Species-Coverage bleibt stabil: `PokemonCount=1439`, `speciesList.size=1415`, `maxSpeciesIdentityNumber=1439`, Gen7/8/9 sichtbar.
- Trainer-Pool vor Filter: `trainerPoolBefore.size=1414`, Gen1-Gen9 enthalten.
- Trainer-Pool nach Filter: `trainerPoolAfter.size=1406`, Gen7/8/9 weiterhin enthalten.
- Ausgeschlossen werden acht nicht kampffaehige Sonder-Species: `Bad Egg`, `Warrior`, zwei Zygarde-Sonderslots und vier Gen9-Ogerpon-Formslots.
- Trainer-Load bleibt stabil: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Trainer-Randomization erreicht Save/Log: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM erzeugt, Trainer-Log nicht leer.
- Gen7/8/9-Picks sind im Direct Results und im Trainer-Log sichtbar.
- Write/Reload-Vergleich ueber interne SpeciesSet-Identitaet: `writeReloadCompared=481`, `writeReloadMismatches=0`.
- Trainer-Species-only ist damit fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand P1-supported.

## Noch nicht gestartet

- Separates DPE/CFRU-Learnset-Profil fuer `gLevelUpLearnsets`
- Praktische P1-Diagnoselaeufe fuer Trainer-Species-Movesets, Held Items und Folgepfade
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. ROMs wurden nur lokal fuer den Diagnose-Lauf gelesen; Artefakte blieben unter `05_builds/**` und wurden nicht committed.

Lokale ignored Smoke-Outputs wurden nur summarisch ausgewertet. Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Workspace-Codeaenderungen ausser Dokumentation und Submodule-Gitlink. UPR-FVX-Codeaenderungen sind auf Trainer-Species-Scope, defensive Trainer-Ability-Slot-Auswahl und Trainer-Species-Write begrenzt.

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

`analysis/upr-fvx-cfru-dpe-p1-evolution-species-only`

Zweck: naechsten P1-Species-Pfad separat diagnostizieren, ohne Trainer-Moveset-/Learnset-/Item-/Ability-Randomization zu vermischen.
