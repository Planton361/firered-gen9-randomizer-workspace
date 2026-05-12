# UPR-FVX CFRU/DPE Gen9 Species Coverage

## Datum

2026-05-12

## Arbeitsbranch

`analysis/upr-fvx-cfru-dpe-gen9-species-coverage`

## Ziel und Sicherheitsrahmen

Read-only Diagnose, warum UPR-FVX im aktuellen lokalen CFRU/DPE-Gen9-Teststand nur bis `PokemonCount=823` laedt, obwohl DPE Gen9 und CFRU-expansion im Source auf vollstaendige Gen9-Species ausgelegt sind.

Dieser Block nimmt keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keinen Gen9-Fix vor. P0 Standard-Wild Gen4+ bleibt als funktionierend vorausgesetzt. P1 Static/Gift bleibt pausiert, bis der Gen9-Coverage-Befund dokumentiert ist.

## Kurzfazit

DPE Gen9 und CFRU-expansion definieren im Source einen internen Species-Raum bis `SPECIES_PECHARUNT = 0x59F`; `NUM_SPECIES = SPECIES_PECHARUNT + 1`, also `1440` interne Slots inklusive `SPECIES_NONE = 0`. Der National-Dex-Raum reicht bis `NATIONAL_DEX_PECHARUNT = 1025`; DPE definiert `NATIONAL_DEX_COUNT = FINAL_DEX_ENTRY + 1`, CFRU `NATIONAL_DEX_COUNT 1025` fuer Runtime-Kontext.

Der aktuelle UPR-FVX-Diagnosebefund laedt dagegen nur:

```text
PokemonCount=823
pokedexCount=386
speciesList.size=799
maxInternalSpeciesId=823
maxSpeciesNumber=411
maxSpeciesIdentityNumber=823
generationCounts={1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

Damit erreicht FVX im konkreten ROM-Load nur interne DPE-ID `823` (`0x337`). Das liegt noch im Gen6-Bereich; `SPECIES_XERNEAS = 0x338` waere die naechste normale Gen6-Species, `SPECIES_ROWLET = 0x3AB` startet Gen7, `SPECIES_GROOKEY = 0x44E` Gen8 und `SPECIES_SPRIGATITO = 0x50E` Gen9.

Die wahrscheinlichste Cutoff-Ursache ist nicht `SpeciesIDs.java` allein. FVX kennt Gen8/Gen9-Konstanten und `generationOf()` kann Namen ab Sprigatito als Gen9 klassifizieren. Der aktuelle Abbruch entsteht vorher in `Gen3RomHandler.basicBPRE10HackSupport()`: `PokemonCount` wird heuristisch aus `PokemonNames` gestartet und dann durch `PokemonMovesets`-Pointer sowie `PokedexOrder`-Werte gekappt. Ohne ROM-Zugriff bleibt offen, welcher dieser Checks bei `823` konkret abbricht.

## Source-Umfang in DPE und CFRU

### Interne Species-IDs

DPE Gen9 und CFRU-expansion spiegeln denselben Gen7-Gen9-ID-Raum:

| Bereich | DPE/CFRU Symbol | Wert |
|---|---:|---:|
| Gen7 Start | `SPECIES_ROWLET` | `0x3AB` / `939` |
| Gen8 Start | `SPECIES_GROOKEY` | `0x44E` / `1102` |
| Gen9 Start | `SPECIES_SPRIGATITO` | `0x50E` / `1294` |
| Gen9 Legendary | `SPECIES_KORAIDON` | `0x57D` / `1405` |
| Gen9 Legendary | `SPECIES_MIRAIDON` | `0x57E` / `1406` |
| Gen9 Endbereich | `SPECIES_TERAPAGOS` | `0x59C` / `1436` |
| letzte Species | `SPECIES_PECHARUNT` | `0x59F` / `1439` |
| interne Slotanzahl | `NUM_SPECIES` | `SPECIES_PECHARUNT + 1` = `1440` |

Weitere Source-Belege:

- DPE `src/Base_Stats.c` enthaelt Eintraege fuer Rowlet, Grookey, Sprigatito, Koraidon, Miraidon, Terapagos und Pecharunt.
- DPE `src/Learnsets.c` enthaelt `gLevelUpLearnsets[NUM_SPECIES]` und Gen7-Gen9-Learnsets bis Pecharunt.
- CFRU `src/Tables/level_up_learnsets.c` enthaelt Gen7-Gen9-Learnset-Eintraege bis Pecharunt.
- DPE `src/Species_To_Pokdex_Table.c` mappt Gen7-Gen9-Species auf National-Dex-IDs bis Pecharunt.

### Pokedex-/Dex-Umfang

DPE:

```text
NATIONAL_DEX_SPRIGATITO 906
NATIONAL_DEX_TERAPAGOS 1024
NATIONAL_DEX_PECHARUNT 1025
FINAL_DEX_ENTRY NATIONAL_DEX_PECHARUNT
NATIONAL_DEX_COUNT FINAL_DEX_ENTRY + 1
```

CFRU:

```text
NATIONAL_DEX_TERAPAGOS 1024
NATIONAL_DEX_PECHARUNT 1025
src/config.h: NATIONAL_DEX_COUNT 1025
```

Die leichte Schreibweise-Differenz ist wichtig: DPE nutzt den Dex-Count als `FINAL_DEX_ENTRY + 1`, waehrend CFRU im Runtime-Kontext `1025` dokumentiert. Fuer UPR-FVX ist entscheidend, dass beide Quellen Gen9-Dexwerte bis Pecharunt kennen; der aktuelle FVX-Load erreicht diesen Bereich nicht.

## Tatsaechlicher FVX-Load-Umfang

Die bisherigen Diagnosen aus P0 und dem Wild-Write-Smoke zeigen stabil:

| Wert | Diagnosebefund |
|---|---:|
| `PokemonCount` | `823` |
| `maxInternalSpeciesId` | `823` |
| `speciesList.size` nach SpeciesSet-Identity-Fix | `799` |
| `pokedexCount` | `386` |
| `maxSpeciesNumber` | `411` |
| `maxSpeciesIdentityNumber` | `823` |
| sichtbare Wild-Generationen nach P0 | Gen1-Gen6 |
| sichtbare Gen7+ Wild-Slots | `0` |

`PokemonCount=823` bedeutet: FVX legt `pokesInternal` nur fuer interne IDs `1..823` an. Alles ab `824` ist fuer FVX in diesem Lauf nicht Teil des Species-Pools. Das erklaert, warum Gen7-Gen9 nicht sichtbar werden, obwohl Source-Dateien sie enthalten.

## FVX Count-Erkennung

`Gen3RomHandler.basicBPRE10HackSupport()` setzt `PokemonCount` nicht aus DPE/CFRU-Symbolen oder `gNumSpecies`. Die Heuristik ist:

1. Starte bei `PokemonNames`.
   - Scanne feste Namensslots mit `PokemonNameLength`.
   - Erhoehe `iPokemonCount`, solange der naechste Name eine Laenge `>0` und `<= nameLen` hat und nicht mit `0` beginnt.
   - Wenn der letzte Name `?` oder `-` ist, dekrementiere.
2. Bestimme `PokemonMovesets`.
   - Jambo-Moveset-Hack-Sonderfall oder Pointer aus bekanntem Gen3-Codepunkt.
   - Reduziere `iPokemonCount`, solange der Moveset-Pointer am Ende invalid ist (`readPointer(..., true) == -1`).
3. Pruefe `PokedexOrder`.
   - Iteriere von `1` bis `iPokemonCount`.
   - Wenn ein `pdEntry > 1023` gefunden wird, setze `iPokemonCount = i - 1`.
4. Schreibe `romEntry.putIntValue("PokemonCount", iPokemonCount)`.

Gepruefte Tabellen:

| Tabelle | Rolle in FVX |
|---|---|
| `PokemonNames` | primaere Count-Schaetzung ueber feste Namensslots |
| `PokemonMovesets` | nachtraegliche Kappung am letzten validen Moveset-Pointer |
| `PokedexOrder` | Sanity-Kappung bei Dexwerten `>1023` |
| `PokemonStats` | wird nach Count-Erkennung bis `PokemonCount` geladen; kein primaerer Count-Scan in dieser Heuristik |

## Wahrscheinliche Cutoff-Ursachen bei 823

Ohne ROM-Zugriff sind drei Ursachen plausibel:

1. `PokemonNames` endet oder enthaelt einen fuer FVX ungueltigen Slot bei `824`.
   - Dann startet `iPokemonCount` bereits bei `823`.
   - Gen7-Gen9 koennen im Source vorhanden sein, aber die konkret gebaute ROM-Name-Table ist fuer FVX an dieser Stelle nicht als fortlaufende Gen3-Namensliste erkennbar.

2. `PokemonMovesets` kappt nachtraeglich auf `823`.
   - DPE/CFRU koennen Learnsets/Pointer anders organisieren oder in einem Bereich haben, den FVX ueber den bekannten Gen3-Pointer nicht mehr als valide Pointer liest.
   - Dann koennen Stats/Namen teilweise weiter existieren, aber die Moveset-Pointer-Heuristik schneidet den Count ab.

3. `PokedexOrder` kappt bei Eintrag `824`.
   - FVX betrachtet `pdEntry > 1023` als ungueltig.
   - DPE `gPokedexOrder_Regional` enthaelt zwar Gen9-Species bis Pecharunt, aber diese DPE-Order ist eine Species-ID-Liste, keine reine National-Dex-ID-Liste. Ab Gen9 koennen interne Species-IDs `>1023` auftreten.
   - Wenn der konkret von FVX gelesene `PokedexOrder`-Pointer auf eine DPE-Species-ID-Order statt auf eine FVX-erwartete Dex-ID-Order zeigt, ist ein frueher Cutoff durch `pdEntry > 1023` moeglich.

Der exakte Abbruchgrund laesst sich erst mit einer lokalen ROM-Diagnose klaeren, die `iPokemonCount` nach jedem Heuristikschritt protokolliert.

## Rolle von PokedexOrder

DPE `src/Pokedex_Orders.c` ist fuer die Ingame-Dex-Views ausgelegt und enthaelt Gen7-Gen9-Species-Symbole in mehreren Ordnungen. Der regionale Dex endet sichtbar mit:

```text
SPECIES_TERAPAGOS,
SPECIES_PECHARUNT,
```

FVX erwartet in `loadPokedexOrder()` dagegen pro interner Species-ID einen Pokedex-/Dexwert:

```text
internalToPokedex[i] = dexEntry
pokedexToInternal[dexEntry] = i
pokedexCount = maxPokedex
```

Im bisherigen Diagnose-ROM bleibt `pokedexCount=386` und `maxSpeciesNumber=411`. Das spricht dafuer, dass der von FVX gelesene PokedexOrder-Raum nicht dem vollstaendigen DPE-Gen9-Dexmodell entspricht oder nur einen begrenzten/kompakten Legacy-Ausschnitt abbildet. Deshalb kann `PokedexOrder` zugleich zwei Probleme verursachen:

- Count-Erkennung kann frueh stoppen, wenn ein Eintrag `>1023` gelesen wird.
- Selbst fuer geladene Gen4-Gen6-Species bleibt `Species.number` kompakt/kollidierend, weshalb PR #3 die SpeciesSet-Identitaet auf interne IDs umstellen musste.

## Rolle von Moveset-Pointern

FVX nutzt `PokemonMovesets` bereits vor dem eigentlichen Moveset-Load als Count-Sanity. Der aktuelle DPE-Source hat `gLevelUpLearnsets[NUM_SPECIES]` und Gen7-Gen9-Eintraege bis Pecharunt. CFRU hat ebenfalls Gen7-Gen9-Learnset-Zeilen.

Das beweist Source-Coverage, aber nicht, dass der konkrete ROM-Pointer, den FVX aus dem Gen3-Codepunkt liest, auf eine fortlaufende Pointertabelle bis `NUM_SPECIES` zeigt. Wenn DPE/CFRU den aktiven Learnset-Pointer anders relocated oder FVX an der falschen Tabelle bleibt, kann der Moveset-Pointer-Check die Count-Erkennung vor Gen7 kappen.

## Rolle von PokemonNames

FVX setzt voraus, dass `PokemonNames` eine fortlaufende Tabelle fester Gen3-Namensslots ist und dass jeder reale Slot eine valide Variable-Length-String-Laenge `<= PokemonNameLength` hat. DPE/CFRU-Source enthaelt Gen7-Gen9-Namen indirekt ueber `gSpeciesNames[species]`-Nutzung und viele Gen7-Gen9-Datentabellen. Der konkrete ROM-Name-Table-Zustand um interne IDs `820..900` ist aber ohne ROM-Zugriff unbekannt.

Wenn bei `824` ein leerer, terminierter, anders encodierter oder nicht an dieser Stelle liegender Name steht, wird FVX auf `823` stehenbleiben, auch wenn Stats, Sprites oder Learnsets fuer hoehere Species an anderer Stelle vorhanden sind.

## Rolle von SpeciesIDs.java und generationOf()

UPR-FVX `SpeciesIDs.java` enthaelt inzwischen Gen8/Gen9-Konstanten:

```text
grookey = 810
scorbunny = 813
sprigatito = 906
koraidon = 1007
miraidon = 1008
terapagos = 1024
pecharunt = 1025
```

`Gen3RomHandler.generationOf()` nutzt fuer erweiterte BPRE-Hacks zuerst normalisierte Species-Namen gegen `SpeciesIDs` und faellt danach auf `Species.number` zurueck. `generationOfSpeciesId()` kennt Schwellen fuer Gen7, Gen8 und Gen9.

Das ist fuer Namensklassifikation ausreichend, sobald FVX die Species ueberhaupt laedt. Es behebt aber keine Count-Erkennung. Zudem bleibt `GenRestrictions.MAX_GENERATION = 7`; ein echtes Gen8/Gen9-Restriction-UI-/Settings-Modell fehlt in FVX weiterhin. Bei `limitPokemon=false` kann der unrestricted Pool zwar theoretisch auch Gen8/Gen9 enthalten, aber im aktuellen Load existieren diese Species gar nicht im Pool.

## Vergleich zu CyanSMP64 NatDex

CyanSMP64 FireRed NatDex und CyanSMP64 UPR-ZX NatDex verfolgen eine andere Strategie:

- FireRed NatDex exportiert ROM-Header-/Metadaten wie `pokedexCount`, `speciesInfo`, `gLevelUpLearnsets` und weitere Tabellenadressen.
- Die NatDex-Species-Konstanten reichen bis Pecharunt und darueber hinaus zu Form-/Sonderformbereichen; `SPECIES_PECHARUNT = 1050`, `SPECIES_TERAPAGOS_STELLAR = 1235`, `SPECIES_EGG = 1284`, `NUM_SPECIES = SPECIES_EGG`.
- CyanSMP64 UPR-ZX NatDex hat Gen8/Gen9-Restriction-Bits, Mega/Eternamax/Regional-Forms-Bits und eine Range-Strategie fuer Gen8/Gen9.
- `GenRestrictions.limitToGen()` ist dort auskommentiert und kappt hoehere Generationen nicht.

Das ist kein Drop-in-Modell fuer CFRU/DPE, aber der zentrale Architekturhinweis ist klar: Ein NatDex-Randomizer sollte den Species-Count und die Generationen nicht nur aus Vanilla-BPRE-Heuristiken ableiten, sondern mit expliziten NatDex-/Hack-Metadaten oder einer robusteren Tabellenstrategie arbeiten.

## Hypothesen ohne ROM-Zugriff

| Hypothese | Plausibilitaet | Begruendung |
|---|---|---|
| Build enthaelt nur einen Teilbereich bis Gen6 | mittel | Der konkrete FVX-Load endet bei `823`; Source reicht weiter. Ohne ROM kann nicht bewiesen werden, ob der lokale Build vollstaendig insertiert wurde. |
| FVX-Heuristik stoppt zu frueh | hoch | `basicBPRE10HackSupport()` kappt anhand Names, Moveset-Pointern und PokedexOrder, nicht anhand DPE `NUM_SPECIES`. |
| DPE Tabellen sind anders organisiert als FVX erwartet | hoch | DPE `Pokedex_Orders.c` ist Species-ID-orientiert und Learnsets/Names koennen relocated sein; FVX nutzt bekannte Gen3-Pointer/Annahmen. |
| Gen7-Gen9 fehlen in FVX SpeciesIDs/GenRestrictions | teilweise | `SpeciesIDs` kennt Gen8/Gen9, `generationOf()` auch; `GenRestrictions.MAX_GENERATION=7` bleibt aber fuer echte Gen9-Settings unvollstaendig. |
| Gen7-Gen9 sind im ROM vorhanden, aber nicht erreichbar | hoch moeglich | Source-Coverage ist da; wenn eine der FVX-Heuristiken bei `824` kappt, bleiben hoehere ROM-Tabellen fuer FVX unsichtbar. |

## Naechste lokale ROM-Diagnose

Die naechste Diagnose braucht lokalen ROM-Zugriff, ohne ROMs, Builds oder Logs mit privaten Pfaden zu committen:

1. Zusaetzliche stderr-Diagnose in `basicBPRE10HackSupport()`:
   - Count nach `PokemonNames`-Scan.
   - letzter Name und erster ungueltiger Name-Slot.
   - Count nach Moveset-Pointer-Kappung.
   - erster invalid Moveset-Pointer mit Index und Pointerwert.
   - erster `PokedexOrder`-Eintrag `>1023` mit Index und Wert.
   - finaler `PokemonCount`.
2. Name-Table-Scan um interne IDs `820..900`.
3. Moveset-Pointer-Validity-Scan um interne IDs `820..900`.
4. PokedexOrder-Werte um interne IDs `820..900`.
5. Stats-Pointer-/BaseStats-Sanity um interne IDs `820..900`.
6. Optionaler Symbol-/Offset-Abgleich:
   - gelesene FVX-Pointer fuer `PokemonNames`, `PokemonMovesets`, `PokedexOrder`, `PokemonStats`.
   - DPE/CFRU-generierte `offsets.ini` fuer denselben lokalen Build.

Erfolgskriterium der Diagnose ist nicht direkt ein Fix, sondern eine konkrete Aussage: `PokemonCount=823` kommt aus Names, Movesets oder PokedexOrder.

## Risiken

- Ohne ROM-Zugriff bleibt der konkrete Cutoff-Schritt eine Hypothese.
- Source-Coverage beweist nicht automatisch, dass der lokale Teststand diese Tabellen vollstaendig insertiert hat.
- `PokedexOrder` kann im DPE-Kontext Species-ID-Listen enthalten; FVX behandelt es als Dex-ID-Mapping.
- Selbst nach Count-Fix fehlen FVX-seitig Gen8/Gen9-Settings/Restrictions und viele P1-Schreibpfade bleiben zu pruefen.
- Ein spaeterer Fix darf Static/Gift, Trainer, Evolutionen, Learnsets, TM/Tutor, Abilities und Day/Night-Wild nicht in denselben Branch ziehen.

## Naechster minimaler Schritt

Neuer Diagnosebranch fuer UPR-FVX oder Workspace, je nach Freigabe:

```text
analysis/upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics
```

Ziel: Nur die Count-Abbruchursache instrumentieren und lokal gegen den CFRU/DPE-Teststand ausfuehren. Keine Gen9-Fixes, keine Static/Gift-Fixes, keine Builds oder ROM-Artefakte committen.
