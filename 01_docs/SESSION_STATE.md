# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- Workspace PR #29 ist gemerged; das CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell ist in `main` verfuegbar.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand bleibt in diesem Workspace auf `223ee9ef compat: preserve CFRU DPE species identity`.
- Die neu eingebundenen NatDex-/Randomizer-/FireRed-Referenz-Submodules sind in `main` verfuegbar und wurden read-only inventarisiert.
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

`analysis/randomizer-natdex-reference-sources`

## Aktueller Arbeitsblock

Read-only Analyse der neu eingebundenen NatDex-/Randomizer-/FireRed-Referenz-Submodules.

## Ziel

Konkret klaeren:

- welche Branches/Commits die Referenz-Submodules aktuell liefern
- welche UPR-FVX-/UPR-ZX-/CyanSMP64-NatDex-Codepfade fuer Settings, GenRestrictions, SpeciesSet und Wild-Pool relevant sind
- welches FireRed-/NatDex-/CFRU-/DPE-Datenmodell fuer Species, Wild, Trainer, Evolutions, Learnsets und TM/Tutor gilt
- welche P0-Fixrichtung fuer GenRestrictions minimal sinnvoll ist

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Branch `analysis/randomizer-natdex-reference-sources` von aktuellem `main` erstellt.
- Pflichtdokumente und bisherige Kompatibilitaets-/Diagnoseprotokolle gelesen.
- UPR-FVX, UPR-FVX upstream, Ajarmar UPR-ZX, CyanSMP64 UPR-ZX NatDex, pret FireRed, CyanSMP64 FireRed NatDex, CFRU-expansion und DPE Gen9 read-only analysiert.
- Neues Quelleninventar erstellt: `01_docs/compat/randomizer-natdex-reference-sources.md`.
- Neues Workflowmodell erstellt: `01_docs/compat/randomizer-workflow-model.md`.
- Neue Implementierungsnotizen erstellt: `01_docs/compat/natdex-reference-implementation-notes.md`.
- Keine Codeaenderungen vorgenommen.
- Keine Builds gestartet.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade gelesen, kopiert, geaendert oder committed.

## Ergebnis

- CyanSMP64 UPR-ZX NatDex erweitert Restrictions auf Gen8/Gen9, Mega, Eternamax und Regional Forms; `limitToGen()` ist dort auskommentiert.
- Ajarmar UPR-ZX und FVX kappen Restrictions dagegen ueber `generationOfPokemon()`.
- CyanSMP64 FireRed NatDex ist eine zusammen entwickelte ROM-/Randomizer-Referenz, aber kein direkt uebertragbares Modell fuer externe CFRU/DPE-Hacks.
- DPE/CFRU bleiben Source-of-Truth fuer den lokalen Species-ID-Raum; CyanSMP64 NatDex ist vor allem als Restriction- und Workflow-Referenz hilfreich.
- P0 bleibt: erweiterte CFRU/DPE-BPRE-Hacks duerfen im finalen `RestrictedSpeciesService` nicht mehr blind auf Gen1-3 gekappt werden.
- Nicht in P0 vermischen: Species-Identity, Day/Night-Wild, Nullslots, Trainer, Starters, Evolutions, Learnsets, TM/Tutor und RAM/Tracker.

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
