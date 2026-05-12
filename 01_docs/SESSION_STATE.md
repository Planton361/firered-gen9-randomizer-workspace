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
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-gen9-species-count`

## Aktueller Arbeitsblock

Dokumentation und Diagnose zum konservativen UPR-FVX-CFRU/DPE-Gen9-SpeciesCount-Fix.

## Ziel

Konkret festhalten:

- welcher UPR-FVX-Fixbranch `PokemonCount=1439` erreicht
- welche Checks und lokalen Diagnosewerte vorliegen
- warum Wild-Randomization noch nicht erreicht wird
- welcher naechste minimale Blocker separat modelliert werden muss

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-gen9-species-count` erstellt.
- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-gen9-species-count` von `compat/firered-gen9-cfru-dpe` erstellt.
- UPR-FVX Commit `d17b29a2 compat: detect CFRU DPE Gen9 species count` erstellt und PR #8 geoeffnet.
- Lokalen CFRU/DPE-CLI-Lauf gestartet; Count-/Generation-Diagnose protokolliert, Abbruch in `loadPokemonPalettes()` dokumentiert.
- Neues Protokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-gen9-species-count-diagnostics.md`.

## Ergebnis

- Der Count-Fix greift: `PokemonCount=1439` statt `823`.
- Gen7/8/9 sind im Species-Load sichtbar: Gen7 `123`, Gen8 `127`, Gen9 `120`.
- `PokemonMovesets` und `PokedexOrder` werden fuer den konservativ erkannten CFRU/DPE-Gen9-BPRE-Modus nicht mehr als Count-Grenze genutzt.
- Der vollstaendige Randomizer-Lauf bricht danach im Palettenpfad ab; dieser Folgefehler ist nicht Teil des Count-Fixes.

## Noch nicht gestartet

- UPR-FVX-Review/Merge von PR #8
- Separates Modell oder Fix fuer `loadPokemonPalettes()` bei erweitertem CFRU/DPE-BPRE-Speciesraum
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

UPR-FVX-Codeaenderung erfolgte nur im Submodule auf Arbeitsbranch `compat/upr-fvx-cfru-dpe-gen9-species-count`; Workspace dokumentiert den Submodule-Pointer.

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

Zweck: naechsten Loader-Blocker `loadPokemonPalettes()` fuer erweiterten CFRU/DPE-BPRE-Speciesraum isoliert analysieren oder fixen. Kein Static-/Gift-, Trainer-, Learnset- oder Moveset-Fix im selben Branch.
