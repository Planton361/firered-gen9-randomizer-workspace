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
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-pokedex-order-model`

## Aktueller Arbeitsblock

Read-only Modellierung von CFRU/DPE-`PokedexOrder`, Dex-ID-Layout und sicheren Count-Quellen fuer vollstaendige Gen9-Coverage.

## Ziel

Konkret klaeren:

- was DPE/CFRU `PokedexOrder` bedeutet
- warum die FVX-Heuristik `pdEntry > 1023 => cutoff` fuer CFRU/DPE falsch ist
- welche Quelle fuer `PokemonCount`, `PokedexCount`, SpeciesSet-Identitaet und Dex-Anzeige geeignet ist
- welche konservative Fix-Strategie Vanilla/alte Gen3-Hacks nicht gefaehrdet

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per Fast-Forward geprueft und Branch `analysis/upr-fvx-cfru-dpe-pokedex-order-model` erstellt.
- DPE/CFRU-Quellen read-only geprueft: `include/species.h`, `include/pokedex.h`, `src/Species_To_Pokdex_Table.c`, `src/Pokedex_Orders.c`, `src/updated_code.c`, CFRU `config.h` und `util.c`.
- UPR-FVX `basicBPRE10HackSupport()`, `loadPokedexOrder()` und Gen3 `gen3_offsets.ini` read-only geprueft.
- CyanSMP64 NatDex-Referenzen read-only verglichen: `tools/inigen/inigen.c`, `src/rom_header_gf.c`, NatDex `gen3_offsets.ini`, Gen8/Gen9-`GenRestrictions`.
- Neues Modell erstellt: `01_docs/compat/upr-fvx-cfru-dpe-pokedex-order-model.md`.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**` umgesetzt.

## Ergebnis

- DPE `gPokedexOrder_*`-Tabellen sind Species-ID-Sortierlisten fuer Pokedex-Views. Die DPE-Runtime wandelt diese Eintraege bei Bedarf ueber `SpeciesToNationalPokedexNum()` in National-Dex-IDs um.
- FVX liest `PokedexOrder` dagegen als lineares internes-Species-zu-Dex-ID-Mapping und nutzt den Wert zugleich als Count-Sanity.
- `pdEntry=1808` bei ID `824` ist weder Xerneas-Dex-ID noch Xerneas-Species-ID; der Vanilla/FVX-Offset ist im CFRU/DPE-ROM fuer Count-Zwecke nicht belastbar.
- Werte `>1023` koennen in DPE-Order-Listen valide interne Species-IDs sein, weil Gen8/Gen9 und Forms oberhalb `1023` liegen.
- Sichere naechste Richtung: fuer konservativ erkannte CFRU/DPE-BPRE-Hacks `PokedexOrder` nicht als Count-Grenze nutzen; Count kurzfristig aus `PokemonNames` plus BaseStats-Sanity ableiten, langfristig eigenes CFRU/DPE-Profil mit explizitem SpeciesCount und `gSpeciesToNationalPokedexNum`-Mapping.

## Noch nicht gestartet

- UPR-FVX-Fixbranch fuer CFRU/DPE-spezifische Count-Heuristik ohne P1-Schreibpfade
- Praktische P1-Diagnoselaeufe fuer Static/Gifts und Trainer-Species
- Evolution-/Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. In diesem Arbeitsblock wurden keine ROMs gelesen.

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

Noch festzulegen.

Zweck: UPR-FVX-Fix fuer CFRU/DPE-spezifische Count-Erkennung vorbereiten. Kein Static-/Gift-Fix und kein Learnset-/Moveset-Fix im selben Branch.
