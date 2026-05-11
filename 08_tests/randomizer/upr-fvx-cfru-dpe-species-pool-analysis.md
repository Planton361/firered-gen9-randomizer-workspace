# UPR-FVX CFRU/DPE Species Pool Analysis

## Datum

2026-05-11

## Arbeitsbranch

`analysis/upr-fvx-cfru-dpe-species-pool`

## Ziel

Read-only Analyse, warum UPR-FVX den CFRU/DPE-Gen4-Gen9-Species-Pool im aktuellen FireRed-Gen9-Kompatibilitaetsbuild nicht sauber als Wild-Randomizer-Pool nutzt und warum im Wild-Log `<unknown>`-Eintraege entstehen.

## Rahmen und Sicherheitsstatus

- Keine ROMs gelesen, kopiert oder geaendert.
- Keine Builds gestartet.
- Keine Randomizer-JARs oder Tool-Binaries geaendert oder committed.
- Keine Saves oder Emulator States angefasst.
- Keine Original-Upstream-Repos kontaktiert.
- Codepfade unter `02_external/**` wurden nur read-only ueber die dokumentierten Planton361-Forks analysiert.

## Git-/Arbeitsbaum-Checks

Die Analyse wurde in ChatGPT/GitHub-Connector-Umgebung durchgefuehrt. In dieser Umgebung war kein vollstaendiger lokaler Git-Arbeitsbaum gemountet; unter `/mnt/data` lagen nur die Projektkontextdateien, aber kein `.git`-Verzeichnis. Deshalb konnten die lokalen Befehle nicht direkt ausgefuehrt werden:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
```

Ersatzpruefung:

- Workspace-Repo `Planton361/firered-gen9-randomizer-workspace` wurde ueber GitHub geprueft.
- Branch `analysis/upr-fvx-cfru-dpe-species-pool` wurde von `main`-Merge-Commit `5c2cc1eda7e600db461e56eac2eba2c31a575fcc` erstellt.
- `.gitmodules` zeigt nur Planton361-Forks als Submodule:
  - `02_external/upr-fvx` -> `Planton361/universal-pokemon-randomizer-fvx`
  - `02_external/Dynamic-Pokemon-Expansion-Gen-9` -> `Planton361/Dynamic-Pokemon-Expansion-Gen-9`
  - `02_external/CFRU-expansion` -> `Planton361/CFRU-expansion`

## Gelesener Kontext

- `README.md`
- `AGENTS.md`
- `01_docs/PROJECT_BRIEF.md`
- `01_docs/SESSION_STATE.md`
- `01_docs/NEXT_STEPS.md`
- `01_docs/references/tool-manifest.md`
- `01_docs/references/source-index.md`
- `08_tests/session/workspace-build-randomizer-smoke-summary.md`
- `08_tests/randomizer/route-1-fallback-wild-randomizer-check.md`

## Relevanter Vorbefund

Der vorherige Smoke-Test zeigte:

- UPR-FVX konnte die CFRU/DPE-ROM laden, minimal randomisieren und speichern.
- BizHawk bootete die randomisierte ROM.
- Wild-Encounter-Randomization funktionierte fuer Vanilla-/Fallback-Encounter-Tabellen.
- Route 22 randomized zeigte u. a. Golbat/Zubat.
- Viridian Forest randomized zeigte Relaxo.
- Der Wild-Log zeigte aber nur Gen1-3 bzw. `<unknown>`-Eintraege.
- Route 1 war ein separates CFRU-Custom-Day/Night-Tabellenproblem und wurde fuer den Kompatibilitaetsbuild ueber `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` auf Vanilla/Fallback-Wilddaten zurueckgefuehrt.

## Analysierte UPR-FVX-Codepfade

### `Gen3RomHandler.java`

Relevant:

- `detectRomInner(...)` akzeptiert weiterhin normale Gen3-ROM-Groessen und erkennt ROMs ueber `gen3_offsets.ini`-Eintraege nach ROM-Code und Version.
- Fuer `BPRE` Version `0` wird in `midLoadingSetUp()` `basicBPRE10HackSupport()` aktiviert.
- `basicBPRE10HackSupport()` erkennt die Species-Anzahl nicht ueber eine explizite DPE-Metadatenquelle, sondern heuristisch:
  - feste Pokemon-Namenstabelle lesen
  - ungueltigen letzten Egg-/Dummy-Slot abschneiden
  - Moveset-Pointer validieren und ggf. `iPokemonCount` nach unten korrigieren
  - `PokedexOrder` pruefen und bei Eintraegen `> 1023` abschneiden
  - Ergebnis als `PokemonCount` in `romEntry` schreiben
- `loadPokedexOrder()` baut `internalToPokedex` und `pokedexToInternal` aus `PokedexOrder`.
- `loadSpeciesStats()` erzeugt fuer jede interne Species-ID ein `Species`-Objekt mit `number = internalToPokedex[i]` und speichert es in `pokes[number]` sowie `pokesInternal[i]`.
- `constructPokemonList()` filtert im ROM-Hack-Fall nur nach `null`, `unused` und `?`.
- `generationOf(Species pk)` ist hart auf Gen1-3 zugeschnitten:

```java
private int generationOf(Species pk) {
    if (pk.getNumber() >= SpeciesIDs.treecko) {
        return 3;
    } else if (pk.getNumber() >= SpeciesIDs.chikorita) {
        return 2;
    }
    return 1;
}
```

Bewertung:

- `Gen3RomHandler` erkennt keine echte DPE-/Gen9-Species-Anzahl im Sinne eines DPE-Profils.
- `PokemonCount` ist ein heuristischer Wert aus Names/Movesets/PokedexOrder.
- Der Code kann Species abschneiden, wenn Moveset-Pointer ungueltig wirken oder `PokedexOrder`-Eintraege `> 1023` auftreten.
- Wenn Gen4-Gen9-Species ueber National-Dex-Nummern geladen werden, werden sie durch `generationOf()` als Gen3 klassifiziert.
- Wenn Gen4-Gen9-Species nicht im `speciesList`/`getSpeciesSetInclFormes()` landen, liegt zusaetzlich ein Count- oder ID-Mapping-Problem vor.

### `Gen3Constants.java`

Relevant:

- `pokemonCount = 386`
- `unhackedMaxPokedex = 411`
- `unhackedRealPokedex = 386`
- `hoennPokesStart = 252`
- `baseStatsEntrySize = 0x1C`

Bewertung:

- Die Konstanten spiegeln weiterhin Vanilla-/klassische Gen3-ROM-Hack-Annahmen.
- Das ist nicht automatisch falsch fuer einen FireRed-Hack, aber nicht ausreichend, um DPE Gen9 eindeutig zu erkennen.

### `SpeciesIDs.java`

Relevant:

- `SpeciesIDs` enthaelt National-Dex-IDs ueber Gen3 hinaus, z. B. `turtwig = 387` und weitere Gen4+ Konstanten.

Bewertung:

- Die IDs sind im Code vorhanden.
- Das Problem ist nicht, dass FVX keine Gen4+-Konstanten kennt, sondern dass `Gen3RomHandler.generationOf()` sie nicht generationstreu einordnet und dass der Gen3-Hack-Loader nicht DPE-spezifisch zaehlt/mappt.

### `Species.java` und `SpeciesSet.java`

Relevant:

- `Species` speichert `generation` nur als Feld; die Generation wird vom RomHandler gesetzt.
- `SpeciesSet` ist ein Set von `Species`; `add(Species)` ignoriert `null`.

Bewertung:

- Die Generation wird nicht zentral aus `SpeciesIDs` abgeleitet.
- Fuer Gen3-ROMs ist `Gen3RomHandler.generationOf()` damit entscheidend fuer alle spaeteren Gen-Filter.

### `RestrictedSpeciesService.java`

Relevant:

- `setRestrictions(null)` nutzt `romHandler.getSpeciesSetInclFormes()` direkt.
- Mit gesetzten Generation-Restrictions wird zuerst `romHandler.getSpeciesSetInclFormes()` geholt und danach per `sp.getBaseForme().getGeneration() == gen` gefiltert.
- `getSpecies(noLegendaries, allowAltFormes, allowCosmeticFormes)` ist die normale Quelle fuer erlaubte Species-Pools.

Bewertung:

- Wenn Species nicht im RomHandler-Species-Set sind, koennen sie nicht in den Wild-Pool gelangen.
- Wenn Species geladen sind, aber falsche `generation` haben, greifen Generation-Restrictions falsch.
- Gen4-Gen9 koennen daher entweder fehlen oder als Gen3 behandelt werden.

### `WildEncounterRandomizer.java`

Relevant:

- `randomizeEncounters(...)` ruft `romHandler.getEncounters(useTimeOfDay)`.
- Der erlaubte Pool wird so gebildet:

```java
SpeciesSet allowed = new SpeciesSet(rSpecService.getSpecies(noLegendaries, allowAltFormes, false));
allowed.removeAll(banned);
```

Bewertung:

- Ja: Der Wild-Randomizer-Pool kommt ueber `RestrictedSpeciesService`.
- Ja: `RestrictedSpeciesService` haengt wiederum an `romHandler.getSpeciesSetInclFormes()` und an den `generation`-Werten der Species.

### `RandomizationLogger.java`

Der konkrete Logger-Pfad konnte in der GitHub-Connector-Suche nicht eindeutig aufgeloest werden. Der bereits dokumentierte Smoke-Test haelt aber fest, dass Null-Species im Wild-Pokemon-Logger als `<unknown>` behandelt werden.

Bewertung:

- `<unknown>` ist damit sehr wahrscheinlich kein eigener Randomizer-Pool-Eintrag, sondern ein Anzeige-/Fallback fuer eine Encounter-Species, die beim Loggen nicht zu einem geladenen `Species`-Objekt aufgeloest werden konnte.

## Analysierte DPE-/CFRU-Pfade

### DPE Gen9 README

Relevant:

- DPE ist ein dynamisches Einfuegetool fuer erweiterte Pokemon-Daten in FireRed.
- Der Gen9-Fork beschreibt Support fuer sehr viele Pokemon/Formen.
- Der README nennt Support fuer bis zu 1025 Pokedex-Eintraege, ohne Alternate Forms.

Bewertung:

- DPE ist nicht nur eine Vanilla-Gen3-Erweiterung bis 386/411.
- FVX' Gen3-Hack-Heuristik mit `PokedexOrder > 1023` als Cutoff ist mindestens grenzwertig, wenn ein Build tatsaechlich Eintraege 1024/1025 nutzt.
- Alternate Forms koennen zusaetzlich ausserhalb einer simplen National-Dex-Zaehlung liegen.

### CFRU Wild Encounter Tables

Der Vorbefund aus der Smoke-Session bleibt gueltig:

- `CFRU-expansion/src/Tables/wild_encounter_tables.c` hatte explizit nur `ROUTE_1` als Custom-Day/Night-Wild-Pool.
- Route 2 und Route 22 waren keine eigenen CFRU-Custom-Pools.
- Route 1 wurde fuer den Kompatibilitaetsbuild per Macro auf Vanilla/Fallback zurueckgestellt.

Bewertung:

- Route 1 ist nicht mehr der primaere Species-Pool-Befund.
- Day/Night-Custom-Encounter-Tabellen bleiben ein separates spaeteres Kompatibilitaetsthema.

## Konkrete Antworten

### Erkennt `Gen3RomHandler` die echte DPE-Species-Anzahl?

Nicht explizit. `Gen3RomHandler` erkennt bei BPRE 1.0-Hacks eine erweiterte Species-Anzahl ueber Heuristiken aus Namenstabelle, Moveset-Pointern und PokedexOrder. Es gibt im analysierten Pfad keine DPE-spezifische Metadaten-/Konstantenquelle fuer `NUM_SPECIES` oder eine echte DPE-Tabellengrenze.

### Wird `PokemonCount` korrekt erkannt oder abgeschnitten?

Das ist ohne lokalen ROM-Diagnoselog nicht beweisbar. Der Code kann `PokemonCount` aber abschneiden:

- wenn Namen nicht als gueltige fixed-length Eintraege gelesen werden,
- wenn Moveset-Pointer am Ende als ungueltig erscheinen,
- wenn `PokedexOrder`-Eintraege `> 1023` auftreten.

Der beobachtete Wild-Log mit nur Gen1-3 und `<unknown>` spricht fuer mindestens eines dieser Probleme:

1. Species oberhalb des klassischen Bereichs werden nicht in den RomHandler-Pool geladen.
2. Species werden geladen, aber wegen `generationOf()` falsch als Gen3 einsortiert.
3. Wild-Encounter-IDs und Species-Array-Indexing verwenden unterschiedliche ID-Raeume, z. B. interne Species-ID vs. National-Dex-ID.

### Werden Gen4-Gen9 Species geladen, aber falsch klassifiziert?

Wenn sie geladen werden und ihre `Species.number` der National-Dex-Nummer entspricht, dann ja: alle Species ab `SpeciesIDs.treecko` werden als Generation 3 klassifiziert. Damit waeren auch Turtwig und alle spaeteren Species Gen3.

Ob sie im aktuellen Build ueberhaupt voll geladen werden, muss durch ein Diagnose-Log mit `PokemonCount`, `pokedexCount`, `speciesList.size()`, maximaler Species-Nummer und Counts pro Generation bestaetigt werden.

### Ist `generationOf()` in `Gen3RomHandler` auf Gen1-3 hardcoded?

Ja. Die Methode unterscheidet nur:

- Gen3: `number >= treecko`
- Gen2: `number >= chikorita`
- Gen1: sonst

Es gibt keine Branches fuer Gen4-Gen9.

### Kommt der Wild-Randomizer-Pool aus `RestrictedSpeciesService` und `romHandler.getSpeciesSetInclFormes()`?

Ja. `WildEncounterRandomizer` baut den erlaubten Pool ueber `rSpecService.getSpecies(...)`. `RestrictedSpeciesService` baut seine Mengen aus `romHandler.getSpeciesSetInclFormes()` und filtert bei Generation-Restrictions nach `Species.generation`.

### Warum entstehen `<unknown>`-Eintraege im Wild-Log?

Direkter dokumentierter Befund: Null-Species im Wild-Pokemon-Logger werden als `<unknown>` behandelt.

Technische Hypothese:

- Beim Lesen oder Loggen einer Wild-Encounter-Species wird ein Rohwert aus der Encounter-Tabelle nicht zu einem `Species`-Objekt aufgeloest.
- Ursache kann ein abgeschnittener `PokemonCount` sein.
- Ursache kann auch ein ID-Raum-Mismatch sein: Gen3RomHandler speichert `pokes[number]` nach `internalToPokedex[i]`, waehrend Wild-Encounter-Tabellen moeglicherweise interne Species-IDs/Form-Slots enthalten.
- Ursache kann ausserdem sein, dass CFRU/DPE-Formen oder Gen9-Slots ausserhalb der von FVX geladenen/erwarteten Species-Liste liegen.

## Technische Haupthypothese

Das aktuelle Problem ist wahrscheinlich zweigeteilt:

1. **Generation-Mapping-Fehler:** Gen4-Gen9 koennen im Gen3-Handler nicht korrekt als Gen4-Gen9 klassifiziert werden, weil `generationOf()` nur Gen1-3 kennt.
2. **Species-ID-/Count-Mapping-Risiko:** Der BPRE-Hack-Support erkennt `PokemonCount` nur heuristisch und mappt interne IDs ueber `PokedexOrder` auf National-Dex-Nummern. DPE/CFRU kann aber interne Species-IDs, Formen und Pokedex-Grenzen nutzen, die nicht sauber in diese Annahmen passen. Das erklaert `<unknown>` im Log besser als ein reiner Generation-Filter.

## Minimaler Fixplan

Nicht sofort grosse Randomizer-Refactors starten. Minimaler naechster UPR-FVX-Arbeitsblock:

1. Diagnose-Ausgabe fuer CFRU/DPE-BPRE-Hacks ergaenzen:
   - erkannter `PokemonCount`
   - `pokedexCount`
   - groesste interne Species-ID
   - groesste Pokedex-/Species-Nummer
   - `speciesList.size()`
   - Count pro `Species.generation`
   - Beispiele fuer Species `> 386`
   - Roh-Species-ID fuer Wild-Log-`<unknown>` inklusive Area/Encounter-Type
2. `generationOf()` fuer National-Dex-Ranges Gen1-9 erweitern oder eine zentrale SpeciesID->Generation-Hilfsfunktion nutzen.
3. Danach pruefen, ob Gen4-Gen9 im Pool auftauchen.
4. Falls `<unknown>` bleibt: Wild-Encounter-ID-Aufloesung zwischen interner Species-ID und Pokedex-ID trennen und beim Lesen/Loggen korrekt auf `pokesInternal` oder eine explizite interne Map zugreifen.
5. Erst danach funktionale Randomisierung fuer CFRU/DPE-Custom-Day/Night-Encounter-Tabellen planen.

## Risiken

- Ein reiner Fix von `generationOf()` reicht nicht, falls `PokemonCount` bereits zu niedrig ist oder Encounter-IDs im falschen ID-Raum gelesen werden.
- `PokedexOrder > 1023` als Cutoff kann mit DPE-Gen9 kollidieren, wenn der konkrete Build 1024/1025 nutzt.
- Alternate Forms sind laut DPE nicht Teil der einfachen Pokedex-Eintragszaehlung und koennen gesonderte Mapping-Logik brauchen.
- Wild-Encounter-Fallback-Tabellen und CFRU-Day/Night-Custom-Tabellen sind getrennte Probleme.

## Naechster minimaler Schritt

UPR-FVX-Folgebranch im Fork vorbereiten, z. B.:

```text
analysis/log-cfru-dpe-species-diagnostics
```

Ziel: Nur Diagnose-Logging/Analyseausgabe im UPR-FVX-Fork, keine Randomizer-Funktion aendern. Danach mit derselben lokalen CFRU/DPE-Test-ROM erneut laden und Logauszug dokumentieren, ohne ROM oder Build-Artefakte zu committen.
