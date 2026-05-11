# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand bleibt in diesem Workspace auf `223ee9ef compat: preserve CFRU DPE species identity`.
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

`analysis/cfru-dpe-upr-fvx-compatibility-model`

## Aktueller Arbeitsblock

Read-only Gesamtanalyse des CFRU/DPE-UPR-FVX-Kompatibilitaetsmodells vor weiteren funktionalen Fixes.

## Ziel

Konkret klaeren:

- welche CFRU/DPE-Datenquellen Source-of-Truth fuer Species, Dex, Wild, Trainer, Evolutions und Learnsets sind
- welche UPR-FVX-Codepfade Source-of-Truth fuer ROM-Erkennung, Species-Loading, Restrictions, Wild, Trainer, Starters, Evolutions und Learnsets sind
- wie interne Species-ID, Dex-ID, SpeciesSet-Identitaet und Formes zusammenhaengen
- warum Gen4+ trotz erweitertem RomHandler-Pool noch nicht im finalen Wild-Pool landet
- ob RAM-Mapping jetzt noetig ist
- welche Fix-Reihenfolge minimal sinnvoll ist

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Workspace PR #28 per `gh pr view --repo Planton361/firered-gen9-randomizer-workspace` als `MERGED` geprueft.
- UPR-FVX PR #3 per `gh pr view --repo Planton361/universal-pokemon-randomizer-fvx` als `MERGED` geprueft.
- Branch `analysis/cfru-dpe-upr-fvx-compatibility-model` von aktuellem `main` erstellt.
- Pflichtdokumente und bisherige Randomizer-Protokolle gelesen.
- UPR-FVX, CFRU-expansion und DPE Gen9 read-only analysiert.
- Neues Modell erstellt: `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`.
- Keine Codeaenderungen vorgenommen.
- Keine Builds gestartet.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade gelesen, kopiert, geaendert oder committed.

## Ergebnis

- RAM-Mapping ist jetzt nicht noetig; zuerst muessen ROM-Datenmodell und Randomizer-Pool stabil sein.
- DPE/CFRU Source-of-Truth fuer Species ist der interne `SPECIES_*`-ID-Raum, nicht der kompakte Dex-/Pokedex-Raum.
- FVX muss `Species.number` fuer bestehende Gen3-Schreibpfade weiter als Dex-/Pokedex-ID behandeln, waehrend SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks intern bleiben muss.
- Der naechste technische Fix ist P0: GenRestrictions/finaler Gen4+-Wild-Pool.
- Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet sind P1, weil viele Pfade weiterhin `pokedexToInternal[species.getNumber()]` verwenden.
- CFRU-Day/Night-Custom-Wild-Tabellen sind P2 und bleiben getrennt vom Vanilla/Fallback-Wild-Pool.
- `rawInternalSpeciesId=0`-`<unknown>` ist P3 und bleibt ein eigenes Nullslot-Thema.
- BizHawk/Ironmon/RAM-Mapping ist P4.

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
