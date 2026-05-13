# 050 - CFRU/DPE Base Stats, Types, Abilities and Encounter Held Items Model

## Kontext

Arbeitsbranch: `analysis/upr-fvx-cfru-dpe-p1-base-stats-types-abilities-model`

Voraussetzungen:

- UPR-FVX PR #25 ist gemerged.
- Workspace PR #87 ist gemerged.
- Diagnose 049 bestaetigt Pokemon Movesets/Learnsets im getesteten CFRU/DPE Gen9-BPRE GameRandomizer-/Settings-nahen Scope als P1-supported.

Scope dieses Protokolls:

- Read-only Modellierung von Base Stats, Pokemon Types, Ability Slots, Hidden Abilities und Encounter Held Items.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine ROMs, Saves, Builds, Logs, Output-ROMs, privaten Pfade oder Secrets beruehrt oder dokumentiert.

## Relevante Dateien und Symbole

| Bereich | Pfad / Symbol | Befund |
|---|---|---|
| FVX Gen3 Base-Stats Pointer | `Gen3Constants.pokemonStatsPointer = 0x1BC` | FVX liest `PokemonStats` ueber den GBA-Pointerblock. |
| CFRU Base-Stats Pointer | `CFRU-expansion/include/new/rom_locs.h`, `gBaseStats ((struct BaseStats*) *((u32*) 0x80001BC))` | CFRU nutzt denselben Pointer-Ort `0x080001BC` / ROM-Offset `0x0001BC`. |
| FVX Entry-Size | `Gen3Constants.baseStatsEntrySize = 0x1C` | FVX nimmt 28 Bytes pro Species an. |
| CFRU Entry-Layout | `CFRU-expansion/include/pokemon.h`, `struct BaseStats` | CFRU-Struct ist ebenfalls bis Offset `0x1A` im 28-Byte-Frame modelliert. |
| Species-Grenze | `SPECIES_PECHARUNT = 0x59F`, `NUM_SPECIES = SPECIES_PECHARUNT + 1` | Interner Species-Scope reicht bis `0x59F`, also `NUM_SPECIES=0x5A0` / `1440`. |
| Types | `TYPE_FAIRY=0x17`, `TYPE_STELLAR=0x18`, `NUMBER_OF_MON_TYPES=TYPE_STELLAR+1` | CFRU/DPE hat moderne Type-IDs bis Stellar. |
| Abilities | `ABILITY_PASTELVEIL=0xFE`, `ABILITIES_COUNT=ABILITY_PASTELVEIL+1` | CFRU Ability-ID-Scope reicht bis `254`, Count `255`; Gen9-Faehigkeiten sind teils auf bestehende IDs geleech-t. |
| Items CFRU | `ITEM_FREE_SPACE3=0x30A`, `ITEMS_COUNT=ITEM_FREE_SPACE3+1` | CFRU-Itemcount `0x30B` / `779`. |
| Items DPE Gen9 | `ITEM_SHINY_SPACE20` nach `0x308..` enum, `ITEMS_COUNT=ITEM_SHINY_SPACE20+1` | DPE-Itemcount `0x31F` / `799`, falls dieser Header massgeblich ist. |

## Base-Stats-Datenmodell

CFRU/DPE nutzt fuer `gBaseStats` weiterhin ein Gen3-kompatibles, direkt indexiertes Species-Array. Der aktive Pointer wird ueber `0x080001BC` geladen. FVX liest denselben Pointer-Ort ueber `Gen3Constants.pokemonStatsPointer = 0x1BC` und speichert ihn als `romEntry.PokemonStats`.

CFRU `struct BaseStats`:

| Offset | Feld | Breite | FVX-Nutzung |
|---:|---|---:|---|
| `0x00` | `baseHP` | `u8` | gelesen/geschrieben |
| `0x01` | `baseAttack` | `u8` | gelesen/geschrieben |
| `0x02` | `baseDefense` | `u8` | gelesen/geschrieben |
| `0x03` | `baseSpeed` | `u8` | gelesen/geschrieben |
| `0x04` | `baseSpAttack` | `u8` | gelesen/geschrieben |
| `0x05` | `baseSpDefense` | `u8` | gelesen/geschrieben |
| `0x06` | `type1` | `u8` | gelesen/geschrieben |
| `0x07` | `type2` | `u8` | gelesen/geschrieben |
| `0x08` | `catchRate` | `u8` | gelesen/geschrieben |
| `0x09` | `expYield` | `u8` | von FVX nicht modelliert |
| `0x0A-0x0B` | EV yields bitfields | `u16` | von FVX nicht modelliert |
| `0x0C` | `item1` | `u16` | Common/Guaranteed Encounter Held Item |
| `0x0E` | `item2` | `u16` | Rare/Guaranteed Encounter Held Item |
| `0x10` | `genderRatio` | `u8` | gelesen/geschrieben |
| `0x11` | `eggCycles` | `u8` | gelesen/geschrieben, falls BreedingInfo vorhanden |
| `0x12` | `friendship` | `u8` | von FVX nicht modelliert |
| `0x13` | `growthRate` | `u8` | gelesen/geschrieben |
| `0x14` | `eggGroup1` | `u8` | gelesen/geschrieben |
| `0x15` | `eggGroup2` | `u8` | gelesen/geschrieben |
| `0x16` | `ability1` | `u8` | gelesen/geschrieben |
| `0x17` | `ability2` | `u8` | gelesen/geschrieben |
| `0x18` | `safariZoneFleeRate` | `u8` | von FVX nicht modelliert |
| `0x19` | `bodyColor/noFlip` | bitfield | von FVX nicht modelliert |
| `0x1A` | `hiddenAbility` | `u8` | von FVX Gen3 aktuell nicht gelesen/geschrieben |
| `0x1B` | Padding/alignment | implizit | nicht modelliert |

Entry-Size bleibt `0x1C`. Das macht Base Stats, Types und Common/Rare Encounter Held Items fuer einen eng gegateten Fix grundsaetzlich einfacher als Learnset-Repointing: kein neues Blob-/Pointertable-Modell ist noetig, solange nur bestehende Felder im bestehenden Array geschrieben werden.

## Species-Indexing

- CFRU/DPE indexiert `gBaseStats[species]` ueber interne Species-ID.
- `SPECIES_NONE=0x0`.
- `SPECIES_EGG=0x19C`.
- `SPECIES_TYPE_NULL=0x3DD`.
- `SPECIES_PECHARUNT=0x59F`.
- `NUM_SPECIES=0x5A0` / `1440`.
- FVX hat fuer den getesteten Stand bereits interne SpeciesSet-Identitaet in relevanten P1-Pfaden etabliert; Base-Stats-Writer muss diese Identitaet beibehalten und darf nicht auf Pokedex-ID roundtrippen.

Placeholder-/Null-Species-Zaehlung wurde in diesem read-only Modell nicht per ROM-Harness erhoben. Aus Quellen und frueheren Diagnosen sind mindestens Sonder-Species wie `SPECIES_NONE`, `SPECIES_EGG` und `SPECIES_TYPE_NULL` relevant; Logger- und Randomizerpfade muessen null/placeholder-defensiv bleiben.

## Pokemon Types

CFRU/DPE Type-IDs:

| Type | ID |
|---|---:|
| `TYPE_NORMAL` | `0x00` |
| `TYPE_FIGHTING` | `0x01` |
| `TYPE_FLYING` | `0x02` |
| `TYPE_POISON` | `0x03` |
| `TYPE_GROUND` | `0x04` |
| `TYPE_ROCK` | `0x05` |
| `TYPE_BUG` | `0x06` |
| `TYPE_GHOST` | `0x07` |
| `TYPE_STEEL` | `0x08` |
| `TYPE_MYSTERY` / typeless | `0x09` |
| `TYPE_FIRE` | `0x0A` |
| `TYPE_WATER` | `0x0B` |
| `TYPE_GRASS` | `0x0C` |
| `TYPE_ELECTRIC` | `0x0D` |
| `TYPE_PSYCHIC` | `0x0E` |
| `TYPE_ICE` | `0x0F` |
| `TYPE_DRAGON` | `0x10` |
| `TYPE_DARK` | `0x11` |
| `TYPE_ROOSTLESS` | `0x13` |
| `TYPE_BLANK` | `0x14` |
| `TYPE_FAIRY` | `0x17` |
| `TYPE_STELLAR` | `0x18` |

FVX `Type` kennt `FAIRY`, aber nicht `STELLAR`, `ROOSTLESS` oder `BLANK`. Gen3 `typeTable` mappt aktuell nur bis `DARK`; `typeToByte(Type.FAIRY)` faellt im Gen3-Pfad durch `default -> 0`, also auf Normal. Daraus folgen zwei getrennte Risiken:

- Read-Risiko: CFRU/DPE-Species mit `TYPE_FAIRY=0x17` oder `TYPE_STELLAR=0x18` werden im aktuellen Gen3-FVX-Type-Table nicht korrekt als Fairy/Stellar gelesen; Fairy wuerde als `null` erscheinen, Stellar ist im FVX-Type-Enum nicht vorhanden.
- Write-Risiko: Type-Randomization kann mit FVX-Fairy arbeiten, schreibt im Gen3-Pfad aber ohne CFRU-Gate keinen Fairy-Wert, sondern Normal. Stellar sollte fuer P1-Type-Randomization vermutlich nicht in den Random-Pool aufgenommen werden, solange Type-Effectiveness, UI und Move-Data-Write nicht modelliert sind.

Minimaler Folgepfad: CFRU/DPE-spezifisch `0x17 -> Type.FAIRY` lesen und `Type.FAIRY -> 0x17` schreiben. `TYPE_STELLAR=0x18` zunaechst defensiv als unsupported/unavailable klassifizieren, nicht randomisieren.

## Ability Slots und Hidden Abilities

FVX Gen3-Modell:

- `abilitiesPerSpecies()` gibt fuer `Gen3RomHandler` aktuell `2` zurueck.
- `highestAbilityIndex()` ist `Gen3Constants.highestAbilityIndex = 77`.
- `loadBasicPokeStats()` liest nur `ability1` bei Offset `0x16` und `ability2` bei Offset `0x17`.
- `saveBasicPokeStats()` schreibt nur `ability1` und `ability2`; bei `ability2 == 0` schreibt FVX Ability 1 in Slot 2.
- `SpeciesAbilityRandomizer` aktiviert Hidden Abilities nur, wenn `abilitiesPerSpecies() == 3`.
- `RandomizationLogger` loggt so viele Ability-Spalten wie `romHandler.abilitiesPerSpecies()` meldet.

CFRU/DPE-Modell:

- `ability1` liegt bei `0x16`.
- `ability2` liegt bei `0x17`.
- `hiddenAbility` liegt bei `0x1A`.
- `ABILITY_PASTELVEIL=0xFE`; `ABILITIES_COUNT=0xFF` / `255`.
- Gen9-Faehigkeiten sind teilweise als Leech-/Alias-Makros auf bestehende Ability-IDs abgebildet, z. B. `ABILITY_SUPERSWEETSYRUP ABILITY_INTIMIDATE`.

Aktueller Blocker fuer Ability-Randomization:

- FVX wuerde nur Ability-IDs `1..77` picken und Namen laden.
- Hidden Ability wird weder gelesen noch geschrieben.
- Species mit Ability-IDs oberhalb `77` koennen zwar als Rohwerte in `Species` landen, aber Logger-Namen fallen auf `ability #<id>` zurueck, weil das Ability-Namenarray nur bis `77` geladen wird.
- Beim Speichern koennen vorhandene Hidden Abilities verloren gehen, wenn spaeter ein Fix nicht explizit Preserve-/Write-Policy definiert.

Minimaler Folgepfad: eigener Ability-Fixbranch, der CFRU/DPE eng gatet, `abilitiesPerSpecies()` fuer diesen Scope auf `3` hebt, Offset `0x1A` liest/schreibt, Ability-Namen/Count bis `0xFE` laedt und Placeholder-/Zero-Ability-Species defensiv ueberspringt.

## Encounter Held Items

Encounter Held Items liegen in der BaseStats-Struktur:

- `item1` bei Offset `0x0C`, `u16`.
- `item2` bei Offset `0x0E`, `u16`.
- FVX interpretiert gleiche Items als `guaranteedHeldItem`; unterschiedliche Items als `commonHeldItem` und `rareHeldItem`.
- Dark-Grass-Held-Item ist in Gen3/CFRU-DPE hier nicht Teil des beobachteten BaseStats-Modells.

Abgrenzung zu Trainer Held Items:

- Trainer Held Items liegen in Trainer-Party-Daten und sind seit Diagnose 028/032 im getesteten Scope P1-supported.
- Encounter Held Items sind Species-/BaseStats-Felder und teilen Risiken mit Item-Count, Item-ID-Mapping und BaseStats-Save.

Item-Risiken:

- CFRU `ITEMS_COUNT` liegt bei `0x30B` / `779`.
- DPE Gen9 Header modelliert `ITEMS_COUNT` bis `0x31F` / `799`.
- FVX Gen3 `loadItems()` nutzt `ItemCount` aus dem RomEntry, aber die Standard-/Internal-Mapping-Fallbacks (`UNIQUE_OFFSET + id`) muessen fuer CFRU/DPE-Held-Item-IDs validiert werden.
- Bad-/Key-Item-Filter stammen aktuell aus FVX-Gen3-Listen und bilden moderne Items wie Tera Orb, Masks, Booster Energy, Plates/Z-Crystals/Mega Stones nur teilweise oder gar nicht fachlich ab.

Minimaler Folgepfad: Encounter Held Items nicht zusammen mit Ability-Fix erzwingen. Zuerst Item-Modell/Bad-Item-Scope oder ein eng gegateter Encounter-Held-Item-Branch mit defensivem Itemcount/Name-Fallback und Write/Reload-Diagnose.

## FVX-Codepfade

| GUI-/Settings-Bereich | FVX-Komponente | Datenzugriff |
|---|---|---|
| Update Base Stats | `SpeciesBaseStatUpdater`, `GameRandomizer.maybeUpdateBaseStats` | setzt Stats im geladenen `Species`-Modell, Save ueber `saveBasicPokeStats()` |
| Shuffle/Randomize Base Stats | `SpeciesBaseStatRandomizer` | aendert HP/Atk/Def/SpA/SpD/Spe im `Species`-Modell |
| Pokemon Types | `SpeciesTypeRandomizer` | aendert Primary/Secondary Type; Save ueber Gen3 type mapping |
| Abilities | `SpeciesAbilityRandomizer` | nutzt `abilitiesPerSpecies()`, `highestAbilityIndex()`, Ability-Banlisten und Species Ability Slots |
| Encounter Held Items | `EncounterHeldItemRandomizer` | aendert `guaranteed/common/rare/darkGrassHeldItem`; Gen3 speichert nur item1/item2 |
| Logging | `RandomizationLogger.logSpeciesTraits()` und Ability-/Itemnamen | abhaengig von Type-, Ability- und Item-Namen/Fallbacks |

## Write-/Reload-Risiken

| Bereich | Risiko | Einschaetzung |
|---|---|---|
| Base Stats | 8-bit Stat-Felder, aber Randomizer begrenzt Werte auf `<=255`; Layout passt zu 0x1C | moderat, wahrscheinlich kleinster Fix |
| Types | Fairy wird im Gen3-FVX-Mapping nicht gelesen/geschrieben; Stellar nicht im FVX-Enum | hoch, eigener Type-Gate noetig |
| Abilities | Count `255` vs FVX `77`, Hidden Ability Offset `0x1A` fehlt, Namenarray zu kurz | hoch, eigener Fixbranch sinnvoll |
| Encounter Held Items | moderne Item-IDs, ItemCount-Divergenz CFRU vs DPE, Bad-/Key-Item-Filter unbewiesen | hoch, von Item-Modell abhaengig |
| Logger | Ability-Namen >77 und moderne Items koennen Fallbacks brauchen | mittel-hoch |
| Placeholder Species | Null-/Bad-Egg-/Type-Null-Species duerfen nicht randomisiert oder geloggt werden wie normale Species | hoch, Skip-Zaehler diagnostizieren |

## Empfohlene Folgebranches

1. `compat/upr-fvx-cfru-dpe-base-stats-types-scope-and-write`
   - Base Stats und Fairy-Type-Mapping gemeinsam, falls Diagnose zeigt, dass Type-Randomization ohne Stellar-Scope begrenzt bleibt.
   - Minimal: `gBaseStats` 0x1C in-place, Fairy `0x17`, Stellar preserve/skip.

2. `compat/upr-fvx-cfru-dpe-abilities-hidden-ability-scope-and-write`
   - Ability 1/2/Hidden Ability separat.
   - Minimal: Count/Namen bis `0xFE`, `abilitiesPerSpecies=3` nur fuer CFRU/DPE, Offset `0x1A`, Placeholder-Skip.

3. `analysis/upr-fvx-cfru-dpe-p1-item-data-and-bad-item-model`
   - Vor Encounter Held Items empfohlen, weil Item-ID-Grenzen, Bad-/Key-Items und moderne held items fachlich breiter sind.

4. `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`
   - Nach Itemmodell; nur BaseStats `item1/item2`, keine Trainer-Held-Item-Aenderung.

Ein einzelner Fixbranch fuer Base Stats + Types + Abilities + Encounter Held Items waere zu gross. Die Bereiche teilen zwar die BaseStats-Struktur, haben aber getrennte Count-/Enum-/Logger-Risiken.

## Erwartete Diagnosewerte fuer Folgefixes

| Wert | Erwartung |
|---|---|
| `species.total` | `1440` / hoechste Species `0x59F:Pecharunt` |
| BaseStats Entry-Size | `0x1C` |
| BaseStats Pointer-Ort | `0x080001BC` / ROM-Offset `0x0001BC` |
| Type Count CFRU | `25` IDs bis `TYPE_STELLAR=0x18`, aber nicht alle IDs fachlich normale Mon-Typen |
| Ability Count CFRU | `255`, hoechste echte ID `0xFE:PastelVeil` |
| Item Count CFRU | `779` laut CFRU Header |
| Item Count DPE | `799` laut DPE Gen9 Header |
| Hidden Ability Offset | `0x1A` |
| Encounter Held Item Offsets | `0x0C`, `0x0E` |
| Reload-Kriterien | BaseStats/Types/Abilities/HeldItems before/after/reload ohne Mismatches |
| Logger-Kriterien | keine NPEs, moderne Ability-/Item-Fallbacks sichtbar, kein Bad Egg / `<unknown>` |

## Fazit

`gBaseStats` selbst ist fuer den getesteten CFRU/DPE-Stand gut modellierbar: gleicher Pointer-Ort wie FVX Gen3, `0x1C` Entry-Size und internes Species-Indexing bis `NUM_SPECIES=1440`. Der eigentliche P1-Fix muss aber getrennt werden:

- Base Stats plus Fairy-Type-Mapping sind der kleinste erste Fix.
- Hidden Abilities und Ability-Count brauchen einen eigenen Fix.
- Encounter Held Items sollten erst nach Item-ID-/Bad-Item-Modellierung geschrieben werden.
