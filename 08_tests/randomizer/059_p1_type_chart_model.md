# 059 - P1 Type-Chart-Modell fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll modelliert Type-Chart und moderne Type-Interaktion fuer den getesteten CFRU/DPE Gen9-BPRE-Stand. Es trennt Pokemon-Type-Read/Write aus Diagnose 051 strikt von Type-Chart-/Effectiveness-Randomization.

Scope:

- Nur bestehende Protokolle und read-only `rg`-/Quellbefunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Grenzen:

- Diagnose 058 bleibt die Grenze fuer Palette-Randomization.
- Diagnose 057 bleibt die Grenze fuer Field Items, Shops, Pickup und allgemeine Item-Randomization.
- Diagnose 056 bleibt die Grenze fuer Move-Data-Write.
- Diagnose 055 bleibt die Grenze fuer Log-Hygiene und Fallback-Marker.
- Diagnose 051 beweist `gBaseStats`-Type-Read/Write, nicht Type-Chart-Support.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `051_base_stats_types_scope_write_diagnostics.md`
- `055_type_log_placeholder_hygiene.md`
- `056_p1_move_data_write_model.md`
- `057_p1_field_items_shops_pickup_model.md`
- `058_p1_palette_randomization_model.md`

Read-only `rg`-Befunde:

- `TypeEffectiveness`
- `Effectiveness`
- `type chart`
- `TypeChart`
- `FAIRY`
- `STELLAR`
- `0x17`
- `0x18`
- `SpeciesTypeRandomizer`
- `Type.FAIRY`

Ergaenzende read-only Codebefunde aus dem lokalen Workspace:

- `SpeciesTypeRandomizer.randomizeSpeciesTypes()` aendert Primary-/Secondary-Type von Species und nutzt `typeService.randomType(random)`.
- `TypeEffectivenessRandomizer` aendert eine `TypeTable` und schreibt sie ueber `romHandler.setTypeTable(...)`.
- `Gen3RomHandler.getTypeTable()` liest die Type-Effectiveness-Daten separat ueber `TypeEffectivenessOffset`.
- `Gen3RomHandler.writeTypeTable(...)` schreibt eine nicht-neutrale Effektivitaetsliste mit Foresight- und End-Table-Terminator.
- `Type` enthaelt `FAIRY`, aber kein `STELLAR`.
- CFRU definiert `TYPE_FAIRY=0x17`, `TYPE_STELLAR=0x18` und `NUMBER_OF_MON_TYPES=TYPE_STELLAR + 1`.

## Grenze zu Pokemon-Type-Read/Write aus 051

Diagnose 051 ist der zentrale Beleg fuer den Species-Type-Scope:

| Bereich | Stand aus 051 |
|---|---|
| Datenstruktur | `gBaseStats` |
| Entry-Size | `0x1C` |
| Type-Felder | Primary-/Secondary-Type-Bytes in BaseStats |
| Fairy | raw `0x17` wird als `Type.FAIRY` gelesen und wieder als `0x17` geschrieben |
| Stellar / unsupported | raw `0x18` bleibt preserve-/skip-only und wird nicht randomisiert |
| Reload | `typeIdMismatches=0` in den dokumentierten 051-Laeufen |

Nicht durch 051 abgedeckt:

- Type-Effectiveness-Table.
- Type-Chart-Randomization.
- Invert Type Effectiveness.
- Balanced Type Effectiveness.
- Keep Type Identities / TypeTable-Swaps.
- Stellar als FVX-Type.
- Gen9-/Terastal-/Stellar-Battle-Interaktionen.

Damit darf 051 nicht als P1-Nachweis fuer Type-Chart-Support gelesen werden. 051 beweist, dass Species-Type-Bytes im getesteten Scope stabil gelesen, geschrieben und reloaded wurden.

## Fairy-Type-Read/Write vs. Type-Chart-Support

Fairy hat im aktuellen Modell mehrere getrennte Ebenen:

| Ebene | Befund | Klassifikation |
|---|---|---|
| CFRU/DPE Type-ID | `TYPE_FAIRY=0x17` | moderne ROM-Type-ID |
| FVX Type-Enum | `Type.FAIRY` existiert | Java-Modell kennt Fairy |
| Species-Type-Read/Write | 051 liest/schreibt Fairy `0x17` mismatch-frei | P1-supported fuer `gBaseStats`-Type-Bytes |
| TypeTable-Pool | Gen3 `readTypeTable()` nutzt im CFRU/DPE-Gate `Type.getAllTypes(6)` | Modell-Hinweis, kein Reload-Nachweis fuer geaenderte TypeChart |
| Type-Effectiveness | keine eigene CFRU/DPE-Diagnose fuer Fairy-Chart | open / not diagnosed |

Konsequenz:

- Fairy `0x17` in Species-Daten beweist keine korrekte Fairy-Effectiveness-Tabelle.
- Ein spaeterer TypeChart-Fix muss Fairy-Interaktionen separat lesen, schreiben und reloaden.
- `TypeEffectivenessUpdater` modelliert klassische Gen6-Updates, ist aber kein CFRU/DPE-Gen9-TypeChart-Nachweis.

## Stellar-/unsupported-Type-Grenze

CFRU/DPE definiert moderne Type-IDs bis Stellar:

| Type-ID | Bedeutung |
|---:|---|
| `0x17` | `TYPE_FAIRY` |
| `0x18` | `TYPE_STELLAR` |

FVX `Type` enthaelt kein `STELLAR`. Diagnose 051 klassifiziert Stellar deshalb bewusst als unsupported/preserve/skip:

- Stellar wird nicht in Random-Pools aufgenommen.
- Species mit nicht representierbarem oder null Primary-Type werden im Type-Randomizer uebersprungen.
- `unsupportedPrimaryTypeBytesBefore=9` und `unsupportedPrimaryTypeBytesReload=9` bleiben aus 051 als Preserve-/Skip-Befund erhalten.

Fuer TypeChart folgt daraus:

- Stellar `0x18` darf nicht stillschweigend in Random-Pools eingefuehrt werden.
- Stellar `0x18` darf nicht stillschweigend in TypeChart-Writes aufgenommen, auf Normal gemappt oder neutralisiert werden.
- Echte Stellar-Unterstuetzung braucht ein separates Type-Enum-/TypeService-/Logger-/Battle-Interaction-Modell.

## Type-Effectiveness-Table-Risiken

Der Gen3-FVX-TypeChart-Pfad ist eine eigene Writer-Oberflaeche:

1. `getTypeTable()` liest ueber `readTypeTable()`.
2. `readTypeTable()` laeuft ab `TypeEffectivenessOffset` ueber 3-Byte-Eintraege.
3. Jeder Eintrag enthaelt Attacker-Type, Defender-Type und Multiplikator.
4. `TYPE_FORESIGHT=0xFE` und `TYPE_ENDTABLE=0xFF` strukturieren Sonderblock und Tabellenende.
5. `setTypeTable()` schreibt ueber `writeTypeTable(...)` eine neue nicht-neutrale Liste.

Bekannte Risiken:

| Risiko | Klassifikation |
|---|---|
| Type-ID-Mapping | Gen3-`typeToByte(...)` und CFRU/DPE-BaseStats-Type-Mapping muessen fuer TypeChart separat passen. |
| Fairy-Interaktionen | Fairy kann im Type-Enum existieren, ohne dass alle ROM-Effectiveness-Eintraege korrekt gelesen/geschrieben werden. |
| Stellar/unsupported | `0x18` ist nicht im FVX-Type-Enum und darf nicht verloren gehen oder als Normal geschrieben werden. |
| Null-Skip beim Read | `readTypeTable()` ueberspringt Eintraege, deren Attacker/Defender nicht abbildbar ist. Das kann unsupported Eintraege aus dem Modell entfernen. |
| Nicht-neutrale Grenze | `writeTypeTable()` bricht ab, wenn `nonNeutralEffectivenessCount()` groesser als `Gen3Constants.nonNeutralEffectivenessCount` ist. |
| Terminator-Struktur | Foresight- und End-Table-Sentinel muessen erhalten bleiben. |
| Moderne Battle-Semantik | Terastal/Stellar, Roostless/Blank und CFRU/DPE-Sondertypen sind nicht durch klassische FVX-TypeTable-Operationen modelliert. |

CFRU dokumentiert die `gTypeEffectiveness`-Eintraege ebenfalls als `u8`-Triplets mit Multiplikatoren `0`, `1`, `5`, `10` und `20` sowie Sonder-IDs `0xFE`/`0xFF`. Das ist strukturell nah am FVX-Modell, beweist aber keinen sicheren Write fuer den getesteten ROM-Stand.

## Type-Randomization-Pool vs. Effectiveness-Randomization

Pokemon-Type-Randomization und Type-Effectiveness-Randomization sind getrennte Randomizer-Pfade:

| Pfad | Komponente | Datenoberflaeche | Einordnung |
|---|---|---|---|
| Pokemon Types | `SpeciesTypeRandomizer` | Species Primary-/Secondary-Type in `gBaseStats` | durch 051 fuer getesteten Scope belegt |
| Type Effectiveness | `TypeEffectivenessRandomizer` | TypeTable / `gTypeEffectiveness` | open / not diagnosed |

`SpeciesTypeRandomizer`:

- aendert Species-Typen.
- skippt Species mit null Primary-Type.
- nutzt denselben TypeService-Pool wie andere Type-Verbraucher.
- speichert spaeter ueber Species-/BaseStats-Daten.

`TypeEffectivenessRandomizer`:

- liest die alte `TypeTable`.
- erzeugt neue Effectiveness-Verteilungen oder tauscht TypeTable-Spalten/-Chunks.
- schreibt ueber `romHandler.setTypeTable(...)`.
- arbeitet nicht an `gBaseStats`.

Konsequenz: Ein stabiler Species-Type-Reload aus 051 sagt nichts darueber aus, ob `setTypeTable(...)` fuer CFRU/DPE sicher ist.

## Preserve-/Skip-Policy fuer spaetere Fixes

Ein spaeterer TypeChart-Fixbranch sollte konservativ modellieren:

1. Keine TypeChart-Writes ausfuehren, wenn der ROM-Handler TypeEffectiveness nicht ausdruecklich fuer den erkannten CFRU/DPE-Scope unterstuetzt.
2. Unknown-/unsupported TypeChart-Eintraege nicht stillschweigend verwerfen, neutralisieren oder auf Normal mappen.
3. Stellar `0x18` preserve-/skip-only behandeln, bis FVX `Type`, TypeService, Logger und Battle-Interaktionen es explizit modellieren.
4. Fairy `0x17` fuer TypeChart separat lesen, schreiben und reloaden; Species-Type-Fairy aus 051 reicht nicht.
5. Foresight-Block, End-Table-Terminator und Multiplikatorwerte erhalten.
6. `nonNeutralEffectivenessCount()` und ROM-seitige Tabellenkapazitaet vor Write pruefen.
7. Type-Randomization-Pools und Type-Effectiveness-Randomization nicht im selben Nachweis vermischen.
8. Move-Type-Bytes, Palette-Type-Following, Item-/Text-/Log-Hygiene und Graphics/Sprites getrennt halten.

## Reload-/Diagnosekriterien fuer spaetere Fixbranches

Dieses Protokoll erhebt keine neuen Diagnosewerte. Ein spaeterer Fix sollte mindestens folgende Kriterien getrennt dokumentieren:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne privaten Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload der geschriebenen TypeChart-Daten erfolgreich |
| TypeTable-Scope | gelesene TypeTable-Typen und nicht-neutrale Eintraege before/after/reload konsistent dokumentiert |
| Fairy | Fairy-Effectiveness-Eintraege explizit im TypeChart-Reload geprueft |
| Stellar / unsupported | keine stillschweigende Aufnahme in Random-Pools und kein Verlust unsupported Eintraege |
| Terminatoren | Foresight- und End-Table-Struktur bleiben erhalten |
| Mismatches | `writeReloadTypeChartMismatches=0` oder klar aequivalenter Zaehler |
| Scope | Keine Palette-, Item-, MoveData-, Graphics- oder Log-Hygiene-Ausweitung |

Neue Diagnosewerte duerfen nur in einem spaeteren, freigegebenen Diagnose-/Fixblock erhoben werden. 059 erfindet keine Laufwerte.

## Abgrenzung zu anderen Diagnosen

| Grenze | Nicht Teil von 059 |
|---|---|
| 055 Log-Hygiene | `Bad Egg`, Unknown-Type-Marker, Placeholder-Namen und Fallback-Logs beweisen keinen TypeChart-Fehler. |
| 056 Move-Data-Write | Move-Type-Bytes und `BattleMove.split` bleiben eigene MoveData-Fragen. |
| 057 Items | Field Items, Shops, Pickup und Bad-/Banned-Item-Policy bleiben getrennt. |
| 058 Palette | Type-following Paletten sind kein Type-Chart-Support. |
| Graphics/Sprites | Graphics-Repointing und Sprite-Daten bleiben P2. |
| Text/UI | Type-Namen, Menues, Descriptions und UI-Labels bleiben eigenes Text-/UI-Thema. |

## Ergebnis

Der getestete CFRU/DPE Gen9-BPRE-Stand hat durch 051 belegtes `gBaseStats`-Pokemon-Type-Read/Write inklusive Fairy `0x17` und Stellar-preserve/skip. Das ist kein Nachweis fuer Type-Chart-Support.

Type-Effectiveness bleibt ein offener Hochrisiko-Writer. Ein spaeterer Fix muss `TypeEffectivenessRandomizer`, `getTypeTable()`/`setTypeTable()`, Fairy-Effectiveness, unsupported/Stellar-Preserve, Terminatoren, nicht-neutrale Tabellenkapazitaet und Reload-Mismatches separat absichern.
