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
- UPR-FVX PR #4 ist gemerged; der P0-GenRestrictions-Fix entfernt die Gen1-3-Kappung fuer erweiterte CFRU/DPE-BPRE-Hacks und setzt bei `limitPokemon=false` den unrestricted Pool.
- UPR-FVX PR #5 ist offen; der Gen3/CFRU-DPE-Wild-Write-Fix schreibt Vanilla/Fallback-Wild-Encounters fuer erweiterte BPRE-Hacks ueber interne SpeciesSet-Identitaet statt `pokedexToInternal[Species.number]`.
- Nach PR #5-Diagnose enthaelt der sichtbare Wild-Log Gen4+-Species: Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-wild-internal-species-write`

## Aktueller Arbeitsblock

Gen3/CFRU-DPE-Wild-Write-Fix im UPR-FVX-Fork umgesetzt und lokaler CFRU/DPE-Diagnoselauf dokumentiert.

## Ziel

Konkret klaeren:

- ob `Gen3RomHandler.writeEncounterArea()` fuer erweiterte CFRU/DPE-BPRE-Hacks interne Species-Identitaet schreibt
- ob Vanilla und normale Gen3-Hacks den bisherigen Dex-/Pokedex-Schreibpfad behalten
- ob Gen4+-Species danach im sichtbaren Wild-Log auftauchen
- ob Route 1, Route 22 und Viridian Forest weiterhin sichtbar randomisiert wirken

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Branch `analysis/upr-fvx-cfru-dpe-wild-internal-species-write` von aktuellem `main` erstellt.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-wild-internal-species-write` von `compat/firered-gen9-cfru-dpe` erstellt.
- UPR-FVX-Basis enthaelt PR #4 als Merge-Commit `03b42a1216f5a087d42a3e94a7e81a15db2e977b`.
- UPR-FVX Wild-Write-Fix in `Gen3RomHandler.java` umgesetzt.
- UPR-FVX Commit erstellt: `5f68ec0fc8e1592079486f6d22cf5a122eb08d01`.
- UPR-FVX PR #5 erstellt: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/5`.
- UPR-FVX lokal gebaut und mit demselben CFRU/DPE-Route-1-Fallback-Teststand diagnostisch ausgefuehrt.
- Neues Diagnoseprotokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.md`.
- Keine Settings-/GenRestrictions-Aenderungen vorgenommen.
- Keine Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade committed.

## Ergebnis

- RomHandler-Diagnose bleibt stabil: `PokemonCount=823`, `speciesList.size=799`, `maxSpeciesIdentityNumber=823`, `generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}`.
- Sichtbarer Wild-Log enthaelt nach PR #5 Gen4+-Species: Gen4 `398`, Gen5 `528`, Gen6 `104`.
- Sichtbare Beispiele: `Floatzel`, `Gothorita`, `Quilladin`, `Minccino`, `Keldeo`, `Arceus`, `Garchomp`, `Bergmite`, `Braixen`.
- `<unknown>` faellt im finalen Wild-Log von `17` auf `0`, weil Gen4+-Auswahlen nicht mehr als interne ID `0` zurueckgeschrieben werden.
- Route 1, Route 22 und Viridian Forest wirken weiterhin sichtbar randomisiert.

## Noch nicht gestartet

- UPR-FVX PR #5 Review/Merge
- P1-Diagnose fuer Trainer-/Starter-/Static-/Evolution-/Learnset-Schreibpfade
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

`analysis/upr-fvx-cfru-dpe-p1-encounter-systems`

Zweck: Weitere Gen3-Schreibpfade fuer erweiterte CFRU/DPE-BPRE-Hacks getrennt diagnostizieren, insbesondere Trainer, Starters, Static Pokemon, Evolutions und Learnsets. Keine Day/Night-Wildtable- oder Nullslot-Fixes in diesem Folgeblock.
