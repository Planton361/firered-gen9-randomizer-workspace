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
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-species-write-paths`

## Aktueller Arbeitsblock

Read-only Diagnose der Species-Schreibpfade ausserhalb von Standard-Wild nach abgeschlossenem P0.

## Ziel

Konkret klaeren:

- welche P1-Pfade weiterhin `pokedexToInternal[Species.number]` oder Dex-ID-Keying verwenden
- welche Pfade wahrscheinlich denselben internen-ID-Ansatz wie der Wild-Write-Fix nutzen koennen
- welche Pfade erst ein eigenes CFRU/DPE-Datenmodell brauchen
- welcher praktische P1-Diagnoselauf als naechstes minimal sinnvoll ist

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #37 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-p1-species-write-paths` von aktuellem `main` erstellt.
- UPR-FVX-Submodule steht weiter auf `compat/firered-gen9-cfru-dpe` bei `843b75a8f1016fa41a1879408fbeca45de7e030a`.
- UPR-FVX-, CFRU-, DPE- und Referenzpfade read-only analysiert.
- Neues Species-Schreibpfadmodell erstellt: `01_docs/compat/upr-fvx-cfru-dpe-species-write-paths.md`.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine funktionalen Fixes vorgenommen.
- Keine Starter-, Static-, Trainer-, Evolution-, Learnset-, TM-, Tutor-, Ability-, Day/Night-Wild-, Swarm-, Roamer-, DexNav-, Raid- oder Nullslot-Fixes umgesetzt.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade committed.

## Ergebnis

- Starters, Static Pokemon/Gifts und Trainer Pokemon lesen Species als interne IDs, schreiben aber weiterhin ueber `pokedexToInternal[Species.number]`.
- Diese drei Pfade sind die kleinsten Kandidaten fuer praktische P1-Diagnoselaeufe und spaetere kleine interne-ID-Fixes.
- Evolutions, Learnsets, TM/HM, Tutor und Ability-Pfade brauchen vor einem Fix mehr Datenmodellierung, weil Quelle, Tabellenbreite, Map-Keys, Hidden Ability und DPE/CFRU-Konfiguration eine groessere Rolle spielen.
- Empfehlung: erster praktischer P1-Diagnoselauf ist Starters-only.

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

`analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics`

Zweck: Starters-only Diagnose fuer erweiterte CFRU/DPE-BPRE-Hacks. Pruefen, ob Gen4+-Starter nach Randomizer-Write und Reload als interne Species-ID erhalten bleiben. Keine Static-, Trainer-, Evolution-, Learnset-, TM-, Tutor-, Ability-, Day/Night-Wild- oder Nullslot-Fixes in diesem Folgeblock.
