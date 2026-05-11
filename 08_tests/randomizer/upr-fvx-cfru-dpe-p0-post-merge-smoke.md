# UPR-FVX CFRU/DPE P0 Post-Merge Smoke

## Datum

2026-05-11

## Ziel

Post-Merge-Bestaetigung der P0-UPR-FVX/CFRU-DPE-Kompatibilitaetskette:

- PR #3: SpeciesSet-Identity-Fix
- PR #4: GenRestrictions-/Settings-Fix
- PR #5: Wild internal species write fix

Dieser Lauf nimmt keine Codeaenderungen und keine funktionalen Fixes vor.

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Branch: `compat/firered-gen9-cfru-dpe`
- Commit: `843b75a8f1016fa41a1879408fbeca45de7e030a`
- Commit-Titel: `Merge pull request #5 from Planton361/compat/upr-fvx-cfru-dpe-wild-internal-species-write`
- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p0-post-merge-smoke`
- Workspace-Vorcommit: `0c46a2c docs: sync merged UPR-FVX wild species write fix`

`git log --oneline -10` im Submodule zeigt die P0-Kette auf dem Zielbranch:

```text
843b75a8 Merge pull request #5 from Planton361/compat/upr-fvx-cfru-dpe-wild-internal-species-write
5f68ec0f compat: write CFRU DPE wild species by internal identity
03b42a12 Merge pull request #4 from Planton361/compat/upr-fvx-cfru-dpe-gen-restrictions
61a15e52 compat: allow CFRU DPE extended generation restrictions
c0f623f8 Merge pull request #3 from Planton361/compat/upr-fvx-gen9-generation-mapping
223ee9ef compat: preserve CFRU DPE species identity
```

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wie in `upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.md`.
- Input-ROM, Output-ROM, Console-Log und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden dokumentiert.

## Build

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis: `BUILD SUCCESSFUL`.

## Settings und Startbefehl

Verwendeter CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p0-post-merge-smoke.gba \
  -S "422AAgEAQQBAAQABwAEAAHkCAARAQEUAAAUAEAEAAEA/wAAAAAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjD84HA048M4ig==" \
  -z 274269061345319 \
  -l
```

Settings-Intent:

- Wild Pokemon Randomization: aktiv
- Wild mode: `GAME`
- `limitPokemon=false`
- keine Gen1-3-Einschraenkung
- keine Wild-Type-, Similar-Strength- oder Evolution-Stage-Einschraenkung
- Time-based Encounters: aus

Der Randomizer schreibt die Settings canonical als:

```text
422AAgEAQQBAAQABwAEAAHkCAARAAEUAAAUAEAEAAEA/////wAAAADkBOQBAAgJ5AYEAOQAAgABAAEBAAAAAAAJAAAAKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjC/hq0048M4ig==
```

## Lokale Artefakte

Nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p0-post-merge-smoke-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p0-post-merge-smoke.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-p0-post-merge-smoke.gba`

Hashes:

```text
f8ed5540cd09b220279f1c677886b9b5b0a1e854651031d2aa7d5188cd6f6028  upr-fvx-cfru-dpe-p0-post-merge-smoke.gba
e3d2f29536ae4267ffda9870fdcf37f4ea5fe4c6b118851dad236881d359e281  upr-fvx-cfru-dpe-p0-post-merge-smoke.gba.log
535e60e9dd7aedf3925e6c43140938d1c5485450c3c33506cc72e2cc17081f13  upr-fvx-cfru-dpe-p0-post-merge-smoke-console.log
```

Der Output-ROM-Hash ist identisch zum PR-#5-Diagnoselauf. Das Randomizer-Log unterscheidet sich vom vorherigen Log nur in `Time elapsed`.

## Species-Pool-Diagnose

stderr-Diagnose aus `Gen3RomHandler`:

```text
ROM code=BPRE
version=0
isRomHack=true
PokemonCount=823
pokedexCount=386
speciesList.size=799
maxInternalSpeciesId=823
maxSpeciesNumber=411
maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

Beispiel-Species ueber 386 bleiben korrekt als Gen6 klassifiziert:

```text
Skrelp, Dragalge, Clauncher, Clawitzer, Helioptile, Heliolisk,
Tyrunt, Tyrantrum, Amaura, Aurorus, Sylveon, Hawlucha
```

## Wild-Log-Auswertung

Ausgewertet wurden die sichtbaren Namen im Randomizer-Wild-Pokemon-Log. Da der Randomizer-Log bis auf `Time elapsed` identisch zum PR-#5-Diagnoselauf ist, bleiben die dortigen Counts stabil:

| Generation | Wild-Slots |
|---|---:|
| Gen1 | 354 |
| Gen2 | 388 |
| Gen3 | 404 |
| Gen4 | 398 |
| Gen5 | 528 |
| Gen6 | 104 |
| Gen7+ | 0 |
| `<unknown>` | 0 |

Weitere Werte:

- Gesamt ausgewertete Wild-Slots: `2176`
- Sichtbare Gen4+-Wild-Slots: `1030`
- Gen4+-Beispiele: `Floatzel`, `Starly`, `Arceus`, `Garchomp`, `Hippowdon`, `Shinx`, `Bonsly`, `Darkrai`, `Burmy`, `Gastrodon`, `Shellos`, `Cherrim`, `Manaphy`, `Cherubi`, `Mime Jr.`, `Glameow`, `Staraptor`, `Rampardos`, `Drapion`.
- Gen5-Beispiele: `Gothorita`, `Purrloin`, `Cryogonal`, `Minccino`, `Keldeo`, `Liepard`, `Crustle`, `Venipede`, `Swanna`, `Sewaddle`, `Munna`, `Sandile`, `Volcarona`, `Simipour`, `Eelektross`, `Conkeldurr`, `Deerling`, `Lampent`, `Larvesta`, `Samurott`, `Roggenrola`.
- Gen6-Beispiele: `Quilladin`, `Bergmite`, `Meowstic`, `Avalugg`, `Braixen`, `Flabebe`, `Vivillon`, `Slurpuff`.

Area-Sanity aus dem Wild-Log:

- Route 1 Grass/Cave: `Minccino`, `Qwilfish`.
- Route 22 Grass/Cave: `Qwilfish`, `Loudred`, `Unown`.
- Viridian Forest Grass/Cave: `Arceus`, `Garchomp`, `Murkrow`, `Bergmite`, `Ivysaur`.

## Diagnose vorher/nachher

| Wert | Vor P0-Kette | Nach PR #3 | Nach PR #4 | Nach PR #5 / Post-Merge |
|---|---:|---:|---:|---:|
| `PokemonCount` | 823 | 823 | 823 | 823 |
| `speciesList.size` | 412 | 799 | 799 | 799 |
| `maxSpeciesIdentityNumber` | nicht vorhanden | 823 | 823 | 823 |
| RestrictedSpeciesService Gen4+ bei `limitPokemon=false` | nicht verfuegbar | durch Gen3-Restrictions entfernt | 381 | 381 |
| sichtbare Gen4+-Wild-Slots | 0 | 0 | 0 | 1030 |
| `<unknown>` | `rawInternalSpeciesId=0` | `rawInternalSpeciesId=0` | 17 | 0 |

## Ergebnis

Die P0-Fixkette ist im Post-Merge-Zielbranch bestaetigt:

- PR #3 verhindert den SpeciesSet-Kollaps und erhaelt interne Species-Identitaet.
- PR #4 entfernt die blinde Gen1-3-Kappung fuer den finalen Pool bei `limitPokemon=false`.
- PR #5 schreibt Vanilla/Fallback-Wild-Encounters fuer erweiterte CFRU/DPE-BPRE-Hacks mit interner Species-Identitaet.
- Der sichtbare Wild-Log enthaelt reproduzierbar Gen4+-Species.

## BizHawk-Smoke

Nicht ausgefuehrt. In diesem Block lag keine separate lokale Freigabe fuer einen BizHawk-Boot-Smoke vor.

## Risiken

- Der Lauf bestaetigt nur Vanilla/Fallback-Wildtabellen, nicht CFRU-Day/Night-Custom-Wildtabellen.
- Der lokale Teststand meldet `PokemonCount=823`; Gen7-Gen9 sind in diesem Lauf nicht repraesentiert.
- Trainer, Starters, Static Pokemon, Evolutions, Learnsets, TM/Tutor und Ability-Pfade bleiben P1.
- Die temporaeren CFRU/DPE-Diagnoseausgaben sind weiterhin im UPR-FVX-Zielbranch vorhanden und sollten spaeter entfernt oder hinter Debug-Logging gelegt werden.

## Naechster minimaler Schritt

Neuer P1-Diagnosebranch:

```text
analysis/upr-fvx-cfru-dpe-p1-encounter-systems
```

Ziel: Trainer, Starters, Static Pokemon, Evolutions, Learnsets und verwandte Schreibpfade getrennt pruefen, ohne Day/Night-Wildtable- oder Nullslot-Fixes zu vermischen.
