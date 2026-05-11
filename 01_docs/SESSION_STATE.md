# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- Workspace PR #29 ist gemerged; das CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand wurde fuer den P0-Folgefix auf `61a15e52 compat: allow CFRU DPE extended generation restrictions` fortgeschrieben.
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
- UPR-FVX PR #4 ist offen; der P0-GenRestrictions-Fix entfernt die Gen1-3-Kappung fuer erweiterte CFRU/DPE-BPRE-Hacks und setzt bei `limitPokemon=false` den unrestricted Pool.
- Der finale `RestrictedSpeciesService`-Pool enthaelt nach PR #4 Gen4+-Species (`gen4plus=381`), aber der sichtbare Wild-Log bleibt Gen1-3. Der naechste Engpass liegt wahrscheinlich im Gen3/CFRU-DPE-Wild-Write-/Reload-Pfad, der weiterhin ueber `pokedexToInternal[Species.number]` arbeitet.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-gen-restrictions`

## Aktueller Arbeitsblock

P0-GenRestrictions-Fix im UPR-FVX-Fork umgesetzt und lokaler CFRU/DPE-Diagnoselauf dokumentiert.

## Ziel

Konkret klaeren:

- ob erweiterte CFRU/DPE-BPRE-Hacks nicht mehr durch `Settings.tweakForRom()` blind auf Gen1-3 gekappt werden
- ob `limitPokemon=false` im finalen `RestrictedSpeciesService` den unrestricted Pool nutzt
- ob Gen4+-Species danach im finalen Pool sichtbar sind
- welcher naechste Engpass verbleibt, falls Wild-Logs weiter Gen1-3 bleiben

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Branch `analysis/upr-fvx-cfru-dpe-gen-restrictions` von aktuellem `main` erstellt.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-gen-restrictions` von `compat/firered-gen9-cfru-dpe` erstellt.
- UPR-FVX P0-Fix in `Settings.java`, `GameRandomizer.java` und `Gen3RomHandler.java` umgesetzt.
- UPR-FVX Commit erstellt: `61a15e521811c5181025e216b3acc27340a495de`.
- UPR-FVX PR #4 erstellt: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/4`.
- UPR-FVX lokal gebaut und mit demselben CFRU/DPE-Route-1-Fallback-Teststand diagnostisch ausgefuehrt.
- Neues Diagnoseprotokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-gen-restrictions-diagnostics-run.md`.
- Keine Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade committed.

## Ergebnis

- P0-GenRestrictions-Fix wirkt im finalen Pool: `limitPokemon=false`, `currentRestrictions=null`, `RestrictedSpeciesService`-Pool `size=798`, `gen4plus=381`.
- RomHandler-Diagnose bleibt stabil: `PokemonCount=823`, `speciesList.size=799`, `maxSpeciesIdentityNumber=823`, `generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}`.
- Sichtbarer Wild-Log bleibt Gen1-3: Gen1 `841`, Gen2 `527`, Gen3 `791`, Gen4+ `0`, `<unknown>` `17`.
- `<unknown>` bleibt unveraendert nur `rawInternalSpeciesId=0`.
- Der naechste Engpass ist wahrscheinlich nicht mehr GenRestrictions, sondern der Gen3/CFRU-DPE-Wild-Write-/Reload-Pfad mit `pokedexToInternal[Species.number]`.

## Noch nicht gestartet

- UPR-FVX-Fix fuer Gen3/CFRU-DPE-Wild-Write-Mapping
- Trainer-/Starter-/Evolution-/Learnset-Diagnosen nach PR #3
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. Lokaler CFRU/DPE-Teststand wurde nur fuer den freigegebenen Diagnoselauf gelesen.

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

`compat/upr-fvx-cfru-dpe-wild-internal-species-write`

Zweck: Im UPR-FVX-Fork read-only analysieren und danach minimal korrigieren, dass Gen3/CFRU-DPE-Wild-Encounter-Schreibpfade die interne Species-Identitaet statt `pokedexToInternal[Species.number]` nutzen.
