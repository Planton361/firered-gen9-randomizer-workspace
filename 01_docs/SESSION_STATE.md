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
- UPR-FVX PR #6 ist offen; der Starter-Write-Fix schreibt Starter fuer erweiterte BPRE-Hacks ueber interne SpeciesSet-Identitaet und erhaelt Pawniard/Scraggy im Reload.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-starter-internal-species-write`

## Aktueller Arbeitsblock

Starter-Write-Fix und Nachher-Diagnose fuer erweiterte CFRU/DPE-BPRE-Hacks.

## Ziel

Konkret klaeren:

- ob `Gen3RomHandler.writeStarterBytes()` fuer erweiterte CFRU/DPE-BPRE-Hacks interne SpeciesSet-Identitaet schreiben kann
- ob Vanilla/normale Gen3-ROMs weiter den bisherigen `pokedexToInternal[Species.number]`-Pfad behalten
- ob Seed `274269061345323` Pawniard/Scraggy nach Write und Reload erhaelt

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #39 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-starter-internal-species-write` von aktuellem `main` erstellt.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-starter-internal-species-write` von `compat/firered-gen9-cfru-dpe` erstellt.
- UPR-FVX-Commit `39c57880` erstellt: `compat: write CFRU DPE starters by internal identity`.
- UPR-FVX PR #6 erstellt: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/6`.
- UPR-FVX lokal mit `./gradlew clean :random:jar` gebaut.
- UPR-FVX `./gradlew test` ausgefuehrt; Build erfolgreich, bekannte bestehende Testfehler bleiben sichtbar.
- Lokaler CFRU/DPE-Teststand mit Starters-only Randomization, `limitPokemon=false`, Seed `274269061345323` und ohne Gen1-3-Einschraenkung ausgefuehrt.
- Neues Diagnoseprotokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-starter-internal-species-write-diagnostics.md`.
- Workspace-Submodule-Pointer auf UPR-FVX `39c57880` vorbereitet.
- Keine Static-, Trainer-, Evolution-, Learnset-, TM-, Tutor-, Ability-, Day/Night-Wild-, Swarm-, Roamer-, DexNav-, Raid- oder Nullslot-Fixes umgesetzt.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade committed.

## Ergebnis

- Vor dem Fix schrieb/reloadete Seed `274269061345323` Pawniard/Scraggy als Drowzee/Jirachi.
- Nach dem Fix loggt und reloadet derselbe Seed `Butterfree`, `Pawniard`, `Scraggy`.
- Reload-Werte nach dem Fix: Pawniard Gen5 identity `677`, Scraggy Gen5 identity `612`.
- Der Fix ist auf `Gen3RomHandler.writeStarterBytes()` beschraenkt und verwendet denselben erweiterten-BPRE-Guard wie der Wild-Write-Fix.
- Ein weiterer praktischer P1-Block sollte Static/Gift-Species getrennt diagnostizieren.

## Noch nicht gestartet

- Praktische P1-Diagnoselaeufe fuer Starters, Static/Gifts und Trainer-Species
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
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

`analysis/upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics`

Zweck: Static-/Gift-Species-Write-/Reload-Diagnose fuer erweiterte CFRU/DPE-BPRE-Hacks. Keine Trainer-, Evolution-, Learnset-, TM-, Tutor-, Ability-, Day/Night-Wild- oder Nullslot-Fixes in diesem Folgeblock.
