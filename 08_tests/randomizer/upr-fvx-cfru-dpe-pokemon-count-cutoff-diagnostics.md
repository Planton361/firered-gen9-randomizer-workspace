# UPR-FVX CFRU/DPE PokemonCount Cutoff Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock klaert diagnostisch, warum UPR-FVX im lokalen CFRU/DPE-Gen9-Teststand `PokemonCount=823` erkennt, obwohl DPE/CFRU im Source bis `NUM_SPECIES=1440` / `SPECIES_PECHARUNT=0x59F` reichen.

Es wurde kein funktionaler Fix umgesetzt. Die Diagnoseausgabe ist temporaer und mit `[CFRU-DPE-COUNT-DIAG]` markiert.

## Branches und Commits

UPR-FVX:

```text
repo: Planton361/universal-pokemon-randomizer-fvx
base: compat/firered-gen9-cfru-dpe
branch: analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics
commit: da97b97e chore: add CFRU DPE PokemonCount cutoff diagnostics
PR: https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/7
```

Workspace:

```text
repo: Planton361/firered-gen9-randomizer-workspace
branch: analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics
```

## Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Ergebnis: sauberer UPR-FVX-Commit, Diff-Check ohne Befund, Build erfolgreich.

Lokaler Diagnose-Lauf:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

Exit-Code: `0`.

Lokale Artefakte blieben unter `05_builds/**` und wurden nicht committed.

## Count-Erkennung

| Schritt | Diagnosewert | Interpretation |
|---|---:|---|
| ROM | `BPRE`, Version `0`, `isRomHack=true` | CFRU/DPE-Teststand wird als erweiterter BPRE-Hack behandelt |
| `PokemonNames` | `namesOffset=0x161ED34`, `nameLen=11` | feste 11-Byte-Namensslots |
| Name-Scan Stop | `nameScanStopIndex=1440`, `countAfterNameScan=1439` | Name-Scan erreicht Pecharunt und stoppt erst nach dem Gen9-Ende |
| letzter valider Name | ID `1439`, `Pecharunt` | ROM enthaelt Namen bis `SPECIES_PECHARUNT` |
| Dummy-Abzug | `deductedDummySlot=false` | keine Egg-/Dummy-Kappung |
| Moveset-Tabelle | `movesetsTable=0x25D7B4`, `jamboMovesetHack=false` | vorhandener Offset aus FVX-RomEntry |
| Moveset-Check | `firstInvalidMovesetIndex=1439`, `rawPointer=0x0`, `countAfterMovesetCheck=930` | Moveset-Pointer-Heuristik kappt vor Gen9, aber nicht auf 823 |
| PokedexOrder | `pokedexOrderOffset=0x251FEE` | vorhandener Offset aus FVX-RomEntry |
| PokedexOrder-Check | `firstPdEntryAbove1023Index=824`, `value=1808`, `countAfterPokedexOrderCheck=823` | direkte Ursache fuer `PokemonCount=823` |
| BaseStats | `pokemonStatsOffset=0x19FC4CC` | Stats-Proben sind ueber 823 hinaus lesbar |

## Grenzbereich 800..900

Namen und Stats sind im Bereich 800..900 vorhanden. Der finale Cutoff entsteht nicht durch fehlende Namen oder fehlende Stats.

| ID | Name | Moveset raw / valid | PokedexOrder | Stats-Sanity |
|---:|---|---|---:|---|
| 800 | Clauncher | `0x5360579` / false | 389 | `50/53/62/44/58/63`, Typ `11/11` |
| 808 | Sylveon | `0xD6011E` / false | 397 | `95/65/65/60/110/130`, Typ `23/23` |
| 820 | Bergmite | `0x400` / false | 409 | `55/69/85/28/32/35`, Typ `15/15` |
| 821 | Avalugg | `0x800` / false | 410 | `95/117/184/28/44/46`, Typ `15/15` |
| 822 | Noibat | `0x1000` / false | 411 | `40/30/35/55/45/40`, Typ `2/16` |
| 823 | Noivern | `0x2000` / false | 0 | `85/70/80/123/97/80`, Typ `2/16` |
| 824 | Xerneas | `0x4000` / false | 1808 | `126/131/95/99/131/98`, Typ `23/23` |
| 825 | Yveltal | `0x8000` / false | 112 | `126/131/95/99/131/98`, Typ `17/2` |
| 826 | Zygarde | `0x10000` / false | 508 | `108/100/121/95/81/95`, Typ `16/4` |
| 827 | Diancie | `0x20000` / false | 1022 | `50/100/150/50/100/150`, Typ `5/23` |
| 828 | Hoopa | `0x40000` / false | 2046 | `80/110/60/70/150/130`, Typ `14/7` |
| 830 | Volcanion | `0x100000` / false | 4095 | `80/110/120/70/130/90`, Typ `10/11` |
| 843 | Flabebe | `0x8231CE4` / true | 480 | `44/38/39/42/61/79`, Typ `23/23` |
| 844 | Floette | `0x8231CF0` / true | 1016 | `54/45/47/52/75/98`, Typ `23/23` |
| 848 | Floette | `0x2020101` / false | 8191 | `74/55/57/122/135/128`, Typ `23/23` |
| 878 | Kangaskhan | `0x200A3183` / false | 6690 | `105/125/100/100/60/100`, Typ `0/0` |
| 900 | Camerupt | `<none>` / false | 0 | `70/120/100/20/145/105`, Typ `10/4` |

Muster: IDs `800..823` bilden den bekannten Gen6-Endbereich ab. Ab ID `824` sind Namen und Stats weiter vorhanden, aber `PokedexOrder` enthaelt Werte, die FVX mit der aktuellen `pdEntry > 1023`-Heuristik als ungueltig behandelt.

## Probe 1000..1050

Der Bereich 1000..1050 zeigt weitere Gen7-/Form-Namen und plausible Stats. Gleichzeitig sind die von FVX gelesenen Moveset-Pointer in dieser Range durchgehend `0x0`, und `PokedexOrder` enthaelt gemischte Werte inklusive vieler Werte `>1023`.

| ID | Name | Moveset raw / valid | PokedexOrder | Stats-Sanity |
|---:|---|---|---:|---|
| 1000 | Hakamo-o | `0x0` / false | 4 | `55/75/90/65/65/70`, Typ `16/1` |
| 1001 | Kommo-o | `0x0` / false | 16404 | `75/110/125/85/100/105`, Typ `16/1` |
| 1002 | Tapu Koko | `0x0` / false | 0 | `70/115/85/130/95/75`, Typ `13/23` |
| 1003 | Tapu Lele | `0x0` / false | 17408 | `70/85/75/95/130/115`, Typ `14/23` |
| 1004 | Tapu Bulu | `0x0` / false | 65280 | `70/130/115/75/85/95`, Typ `12/23` |
| 1008 | Solgaleo | `0x0` / false | 1290 | `137/137/107/97/113/89`, Typ `14/8` |
| 1009 | Lunala | `0x0` / false | 515 | `137/113/89/97/137/107`, Typ `14/7` |
| 1012 | Pheromosa | `0x0` / false | 57346 | `71/137/37/151/137/37`, Typ `6/1` |
| 1017 | Necrozma | `0x0` / false | 57600 | `97/107/101/79/127/89`, Typ `14/14` |
| 1019 | Marshadow | `0x0` / false | 515 | `90/125/80/125/90/90`, Typ `1/7` |
| 1024 | Sandslash | `0x0` / false | 515 | `75/120/100/75/25/65`, Typ `15/8` |
| 1039 | Marowak | `0x0` / false | 2 | `80/90/110/45/50/80`, Typ `10/7` |
| 1048 | Silvally | `0x0` / false | 515 | `95/95/95/95/95/95`, Typ `1/1` |
| 1050 | Silvally | `0x0` / false | 32768 | `95/95/95/95/95/95`, Typ `3/3` |

Muster: Gen7-/Formdaten sind im ROM sichtbar vorhanden, werden aber nicht in den FVX-Species-Load aufgenommen, weil der globale Count bereits bei 823 endet.

## Technische Interpretation

Die konkrete `PokemonCount=823`-Ursache im lokalen Teststand ist der `PokedexOrder`-Sanity-Check in `basicBPRE10HackSupport()`: Bei interner ID `824` liest FVX `pdEntry=1808`, bewertet diesen Wert wegen `pdEntry > 1023` als ungueltig und setzt `iPokemonCount = 823`.

`PokemonNames` ist nicht die Ursache. Der Name-Scan laeuft bis `nameScanStopIndex=1440`, der letzte valide Name bei ID `1439` ist `Pecharunt`.

`PokemonStats` ist ebenfalls nicht die unmittelbare Ursache. Stats sind in den Proberanges ueber 823 hinaus plausibel lesbar.

`PokemonMovesets` ist ein zweiter echter Tabellenkompatibilitaetsbefund: Der Rueckwaertscheck wuerde den Count von 1439 auf 930 kappen. Das erklaert aber nicht den finalen Wert 823, weil danach `PokedexOrder` noch staerker kappt.

Wahrscheinlich passt der von FVX als `PokedexOrder` interpretierte Tabellenbereich im CFRU/DPE-Gen9-ROM nicht mehr zur alten Annahme eines kompakten Dex-Order-Arrays mit Eintraegen `<=1023`. Die Werte ab ID 824 sehen eher nach anderem Layout, Form-/Flag-Codierung oder einem nicht passenden Offset fuer den erweiterten Speciesbereich aus.

## Risiken

- Die UPR-FVX-Diagnoseausgabe ist bewusst temporaer und sehr ausfuehrlich.
- Die Proben belegen Tabellenlesbarkeit, aber keinen vollstaendigen korrekten Gen9-Load.
- Moveset-Pointer und PokedexOrder muessen vor einem Fix getrennt modelliert werden; ein reiner Count-Override waere riskant.
- P1 Static/Gift bleibt sinnvoll pausiert, bis die Count-Heuristik fuer DPE/CFRU sauber verstanden ist.

## Naechster minimaler Schritt

Keinen Static-/Gift-Fix starten. Als naechstes in einem separaten Fix-/Analysebranch die DPE/CFRU-Bedeutung der von FVX gelesenen `PokedexOrder`-Adresse gegen Source-Symbole und generierte ROM-Offsets pruefen und entscheiden, ob `PokemonCount` fuer CFRU/DPE ueber eine DPE-spezifische Count-Quelle statt ueber die alte `PokedexOrder`-Heuristik bestimmt werden muss.
