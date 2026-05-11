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

`analysis/upr-fvx-cfru-dpe-p1-encounter-systems`

## Aktueller Arbeitsblock

Read-only Diagnose und Abgrenzung der CFRU/DPE Encounter-Systeme nach abgeschlossenem P0.

## Ziel

Konkret klaeren:

- welche CFRU/DPE-Encounter-Systeme existieren
- welche FVX aktuell randomisiert
- welche Systeme nach P0 supported, partial, unsupported oder separat zu fixen sind
- ob der naechste Fix Day/Night Custom Wildtables oder zuerst weitere P1-Species-Schreibpfade sein sollte

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #36 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-p1-encounter-systems` von aktuellem `main` erstellt.
- UPR-FVX-Submodule steht weiter auf `compat/firered-gen9-cfru-dpe` bei `843b75a8f1016fa41a1879408fbeca45de7e030a`.
- UPR-FVX-, CFRU-, DPE- und Referenzpfade read-only analysiert.
- Neues Encounter-Systemmodell erstellt: `01_docs/compat/cfru-dpe-encounter-systems-model.md`.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine funktionalen Fixes vorgenommen.
- Keine Day/Night-Wildtable-, Swarm-, Roamer-, DexNav-, Raid-, Nullslot-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade committed.

## Ergebnis

- P0-supported sind Standard-Wild/Grass-Cave, Surfing, Fishing und Rock Smash aus `gWildMonHeaders`.
- CFRU Morning/Day/Evening/Night-Header koennen Fallback-Wilddaten zur Laufzeit uebersteuern und bleiben P2.
- Swarms, Roamers, DexNav, Wild Double Battles, Raids, Altering Cave und Tanoby/Unown sind partial oder unsupported und brauchen getrennte Behandlung.
- Empfehlung: naechsten echten Fix nicht Day/Night starten, sondern zuerst P1-Species-Schreibpfade fuer Trainer, Starters, Static Pokemon, Evolutions und Learnsets read-only diagnostizieren.

## Noch nicht gestartet

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
