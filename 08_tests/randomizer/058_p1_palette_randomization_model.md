# 058 - P1 Palette-Randomization-Modell fuer CFRU/DPE Gen9-BPRE

## Ziel

Dieses read-only Protokoll modelliert Palette-Randomization fuer den getesteten CFRU/DPE Gen9-BPRE-Stand. Es trennt die bereits belegte Palette-Safety strikt von echter geaenderter Palette-/Graphics-Randomization.

Scope:

- Nur bestehende Protokolle und read-only `rg`-/Quellbefunde.
- Keine Codeaenderung, kein Fix, keine Aenderung an `02_external/**`.
- Keine neuen Randomizer-Laeufe.
- Keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Logs, Output-ROMs, Tool-Binaries, privaten Pfade, ROM-Namen, Hashes, Secrets oder `.env`-Inhalte gelesen oder dokumentiert.

Grenzen:

- Diagnose 057 bleibt die Grenze fuer Field Items, Shops, Pickup und allgemeine Item-Randomization.
- Diagnose 056 bleibt die Grenze fuer Move-Data-Write.
- Diagnose 055 bleibt die Grenze fuer Log-Hygiene und Fallback-Marker.
- Graphics/Sprites bleiben ein eigenes P2-Modell.
- Dieses Protokoll beweist keine sichere geaenderte Palette-Randomization.

## Genutzte Belege

Primaere Belege:

- `047_fvx_gui_options_compatibility_matrix.md`
- `055_type_log_placeholder_hygiene.md`
- `056_p1_move_data_write_model.md`
- `057_p1_field_items_shops_pickup_model.md`
- `upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md`
- `upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.md`

Read-only `rg`-Befunde:

- `Palette`
- `Pokemon Palettes`
- `savePokemonPalettes`
- `loadPokemonPalettes`
- `Gen3to5PaletteRandomizer`
- `PaletteRandomizer`
- `compressed`
- `repoint`
- `sprite`
- `graphics`
- `skip unchanged`
- `unchanged palettes`

Ergaenzende read-only Codebefunde aus dem lokalen Workspace:

- `GameRandomizer.maybeRandomizePokemonPalettes()` ruft `paletteRandomizer.randomizePokemonPalettes()` nur bei `PokemonPalettesMod.RANDOM`.
- `Gen3to5PaletteRandomizer.randomizePokemonPalettes()` aendert geladene Pokemon-Paletten auf Basis der Palette-Beschreibungen und optionaler Type-/Evolution-/Shiny-Settings.
- `Gen3RomHandler.loadPokemonPalettes()` nutzt fuer CFRU/DPE einen defensiven Load-Pfad und merkt geladene Normal-/Shiny-Palette-Bytes.
- `Gen3RomHandler.savePokemonPalettes()` ueberspringt fuer CFRU/DPE den Save nur, wenn keine geladene Palette geaendert wurde.
- Sobald irgendeine Palette geaendert ist, bleibt der bestehende `savePokemonPalettes()`-Write-Pfad aktiv.
- `rewriteCompressedPalette()` schreibt ueber `rewriteCompressedData()` und `DataRewriter`, der alte komprimierte Daten ermittelt, freigibt und auf neue FreeSpace-Daten repointet.
- Der komprimierte Palette-Write-Pfad dokumentiert selbst die Single-Pointer-Annahme fuer `rewriteCompressedData(int, byte[])`.

## Bestehende Palette-Safety / Skip-Unchanged-Save

Die bestehenden Palette-Fixes sind Safety-Unblocker, keine Palette-Randomization-Unterstuetzung.

Belegter Safety-Stand:

| Bereich | Beleg | Einordnung |
|---|---|---|
| defensiver Load | `upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md` | fehlende, nullinitialisierte oder ungueltige Palette-Slots brechen den ROM-Load nicht mehr ab |
| missing Palette Save | defensiver Load-Fix | Species mit fehlender geladener Normal- oder Shiny-Palette werden beim Save uebersprungen |
| skip unchanged Save | `upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.md` | unveraenderte CFRU/DPE-Pokemon-Paletten werden nicht neu geschrieben |
| Matrix-Status | 047 | Palette-Safety ist P1-supported fuer unchanged/safety path |

Wichtig:

- `Pokemon Palettes: Unchanged` ist der belegte stabile Safety-Pfad.
- Der Skip greift nur, wenn die geladenen Palette-Bytes unveraendert sind.
- Dieser Safety-Pfad verhindert bekannte Save-/Load-Blocker, beweist aber kein sicheres Schreiben geaenderter Paletten.

## Grenze zwischen Safety-Pfad und echter Palette-Randomization

Die Grenze ist bewusst hart:

| Zustand | Verhalten | Klassifikation |
|---|---|---|
| Paletten unveraendert | `savePokemonPalettes()` ueberspringt CFRU/DPE-Pokemon-Palette-Save | P1-supported Safety |
| Palette fehlt oder ist invalid | defensiver Load/Save skippt betroffene Slots | P1-supported Safety |
| irgendeine geladene Palette wurde geaendert | `savePokemonPalettes()` faellt in bestehenden komprimierten Write-/Repoint-Pfad | open / not diagnosed |
| Palette-Randomizer ist aktiv | `PokemonPalettesMod.RANDOM` ruft `Gen3to5PaletteRandomizer` | open / not diagnosed |

Die Safety-Diagnosen beweisen deshalb nicht echte geaenderte Palette-Randomization. Unveraenderte oder fehlende Paletten sicher zu laden oder zu ueberspringen ist nicht dasselbe wie sicheres Schreiben geaenderter Paletten.

## `PokemonPalettesMod.RANDOM`

FVX trennt die GUI-/Settings-Option:

- `PokemonPalettesMod.UNCHANGED`: keine kosmetische Palette-Randomization.
- `PokemonPalettesMod.RANDOM`: `maybeRandomizePokemonPalettes()` ruft den Palette-Randomizer.
- Zusatzsettings koennen Type-Following, Evolution-Following und Shiny-from-Normal beeinflussen.

Fuer CFRU/DPE gilt:

- Der stabile documented path ist `UNCHANGED`.
- `RANDOM` ist kein Safety-Pfad, sondern ein echter Writer-Pfad.
- Type-Following-Paletten duerfen nicht mit Type-Chart-Support verwechselt werden.
- Evolution-Following-Paletten duerfen nicht mit Evolution-Write-Support verwechselt werden.

## `Gen3to5PaletteRandomizer`

`Gen3to5PaletteRandomizer` ist der relevante Randomizer fuer Gen3-Gen5-Pokemon-Paletten.

Modellierte Risiken:

| Risiko | Einordnung |
|---|---|
| Forms und unterschiedliche Paletten | im Code als TODO sichtbar; CFRU/DPE hat viele moderne Form-/Alt-Species-Kontexte |
| Palette-Beschreibungsindex | Palette-Beschreibungen werden nach `pk.getNumber() - 1` indiziert; das ist nicht automatisch interne CFRU/DPE-Species-Identitaet |
| Type-Following | nutzt Type-Farben, bleibt getrennt von Type-Chart und modernen Type-Enum-Fragen |
| fehlende Palette | Randomizer kann nur mit geladenen Palette-Objekten arbeiten; fehlende Slots bleiben skip/preserve-Kandidaten |
| geaenderte Palette-Bytes | jede Aenderung deaktiviert den Skip-Unchanged-Safety-Pfad und verlangt echten Write-/Reload-Nachweis |

Damit ist der Randomizer-Pfad fachlich ein Hochrisiko-Writer, obwohl der unveraenderte Safety-Pfad stabil ist.

## `savePokemonPalettes()`

Der CFRU/DPE-Safety-Guard im Save-Pfad hat zwei unterschiedliche Rollen:

1. Wenn keine geladene Palette geaendert wurde, wird der Pokemon-Palette-Save uebersprungen.
2. Wenn eine Palette geaendert wurde, laeuft der bestehende Save-Pfad weiter.

Der zweite Fall ist der entscheidende offene Bereich. Dann iteriert der Gen3-Pfad ueber Species, bestimmt Palette-Tabellen-Slots und schreibt Normal-/Shiny-Paletten ueber komprimierte Daten-Rewrites.

Konsequenz:

- `savePokemonPalettes()` ist fuer unveraenderte Paletten entblockt.
- `savePokemonPalettes()` ist fuer geaenderte CFRU/DPE-Paletten nicht als P1-supported belegt.
- Ein spaeterer Fix darf den Skip-Unchanged-Safety-Befund nicht als Reload-Beweis fuer geaenderte Paletten verwenden.

## `rewriteCompressedPalette()` / Compressed Palette Risks

Der Write-Pfad:

1. `rewriteCompressedPalette(pointerOffset, palette)`
2. `rewriteCompressedData(pointerOffset, palette.toBytes())`
3. `DataRewriter.rewriteData(...)`
4. alte Datenlaenge bestimmen
5. alten Datenbereich freigeben
6. neue komprimierte Daten in FreeSpace schreiben
7. Pointer repointen

Risiken:

| Risiko | Klassifikation |
|---|---|
| alter Datenblock nicht dekomprimierbar | bekannter Save-Blocker-Typ; Safety-Fix umgeht ihn nur fuer unchanged Paletten |
| komprimierte Laengenbestimmung | `lengthOfCompressedDataAt()` dekomprimiert und recomprimiert; nicht alle DPE-Daten muessen in diese Annahme passen |
| Palette-Groesse | Gen3-Pokemon-Paletten erwarten 16 Farben; Sonderfaelle/Formen koennen anders organisiert sein |
| FreeSpace | geaenderte Paletten brauchen belastbaren neuen Speicherort |
| Bytegleichheit | unveraenderte Paletten sind safe, geaenderte Paletten brauchen eigenen Reload-Vergleich |

Der bekannte `0x16b9c08`-Blocker ist als compressed/repointing risk einzuordnen, nicht als Count-, Trainer- oder Learnset-Problem.

## Shared/Missing Palette Pointer Risks

Vorhandene Belege:

| Befund | Bedeutung |
|---|---|
| `SPECIES_CUBONE_A` / `gMonPaletteTable[1038]` | erster belegter missing/invalid Normal-Palette-Slot |
| entsprechender Shiny-Slot | Shiny-Palette kann analog fehlen/invalid sein |
| `Oricorio` ueber Tabellenindex `1038` | bestaetigt Dex-/`pokedexToInternal`-Mapping-Risiko im Grafikpfad |
| DPE-Gap `[252]..[276]` | mehrere Slots teilen `gFrontSprite252Pal` |
| Shiny-Gap `[252]..[276]` | mehrere Slots teilen `gBackShinySprite252Pal` |

Risiken:

- Missing Slots duerfen nicht als normale Randomizer-Ziele behandelt werden.
- Shared Datenpointer duerfen nicht mit Single-owner-Repointing beschrieben werden.
- Dex-/Pokedex-Mapping ist fuer den Grafikpfad als Risiko belegt und nicht durch interne Species-Write-Fixes anderer Pfade geloest.
- Bestehende Shared-Paletten sind Preserve-Faelle, bis ein eigenes Multi-pointer-/Dedup-Modell existiert.

## Repointing Risks

Der Palette-Write-Pfad ist nicht nur ein In-place-Farbbyte-Write. Er ist ein komprimierter Repointing-Pfad.

Wichtige Risiken:

| Risiko | Einordnung |
|---|---|
| Single-Pointer-Annahme | `rewriteCompressedData(int, byte[])` geht davon aus, dass es nur einen Pointer auf den alten komprimierten Datenblock gibt |
| Secondary Pointers | Shared Paletten braeuchten explizite Secondary-Pointer-Policy |
| FreeSpace | neue komprimierte Palette muss sicher abgelegt werden |
| alte Daten freigeben | bei Shared-Daten kann Freigeben des alten Blocks andere Slots treffen |
| Reload | Pointer, dekomprimierte Palette und Species-Zuordnung muessen nach Reload stimmen |

Ein spaeterer Palette-Randomization-Fix muss deshalb eher wie ein Repointing-Fix modelliert werden als wie ein einfacher Datenbyte-Write.

## Sprite-/Graphics-Abgrenzung

058 modelliert Pokemon-Palette-Randomization, nicht Sprite-/Graphics-Randomization.

Out of scope:

- Pokemon Front-/Back-Sprite-Images.
- Custom Player Graphics.
- Overworld-Sprites.
- Map Icons.
- Trainer Images.
- Graphics Packs.
- Full DPE/CFRU Graphics-Profil.

Begruendung:

- Sprites/Graphics nutzen weitere komprimierte Bilddaten und Pointer.
- Player-/Overworld-Grafiken haben eigene Palette- und Image-Semantik.
- Die vorhandenen Palette-Safety-Diagnosen betreffen Pokemon-Palette-Load/Save, nicht allgemeine Graphics-Repointing-Sicherheit.

Graphics/Sprites bleiben deshalb ein eigenes P2-Modell.

## Preserve-/Skip-Policy fuer spaetere Fixes

Ein spaeterer Fixbranch sollte konservativ modellieren:

1. Fehlende, invalid oder nicht geladene Paletten skippen und nicht neu erzeugen.
2. Unveraenderte Paletten weiterhin nicht neu schreiben.
3. Shared Palette-Daten preserven, solange keine Secondary-Pointer-/Dedup-Policy belegt ist.
4. Keine geaenderte Palette schreiben, wenn der alte Datenblock nicht eindeutig dekomprimierbar und single-owner ist.
5. Dex-/Pokedex-Mapping nicht als interne CFRU/DPE-Species-Identitaet ausgeben.
6. Type-following Palette-Logik getrennt von Type-Chart- und Type-Enum-Arbeit halten.
7. Form-/Alt-Species-Paletten nur mit expliziter Policy behandeln.
8. Sprite-/Graphics-Repointing nicht im selben P1-Palette-Fix erzwingen.

## Reload-/Diagnosekriterien fuer spaetere Fixbranches

Dieses Protokoll erhebt keine neuen Diagnosewerte. Ein spaeterer Fix sollte mindestens folgende Kriterien getrennt dokumentieren:

| Kriterium | Erwartung |
|---|---|
| Save | `saveSuccessful=true` |
| Log | `logSuccessful=true`, `logNonEmpty=true` |
| Output | Output-ROM vorhanden, ohne privaten Pfad oder ROM-Namen zu dokumentieren |
| Reload | Reload der geschriebenen Palette-Daten erfolgreich |
| Settings | `PokemonPalettesMod.RANDOM` oder aequivalente aktive Palette-Randomization klar belegt |
| geaenderte Paletten | Anzahl geaenderter Normal-/Shiny-Paletten before/after/reload dokumentiert |
| skipped missing | fehlende/invalid Palette-Slots bleiben skip/preserve und blockieren nicht |
| compressed errors | keine `no compressed data found`-/invalid-pointer-Abbrueche |
| shared pointers | Shared-Pointer-Faelle werden preserved oder mit Secondary-Pointer-Policy reload-stabil behandelt |
| mismatches | `writeReloadPaletteMismatches=0` oder klar aequivalenter Zaehler |
| Scope | Keine Field-Items-, Move-Data-, Type-Chart-, Log-Hygiene- oder Graphics/Sprite-Ausweitung |

Neue Diagnosewerte duerfen nur in einem spaeteren, freigegebenen Diagnose-/Fixblock erhoben werden. 058 erfindet keine Laufwerte.

## Explizite Nicht-Ziele

058 erweitert nicht:

- Field Items, Shops, Pickup oder Item-Randomization aus 057.
- Move-Data-Write aus 056.
- Log-Hygiene oder Fallback-Marker aus 055.
- Type-Chart, Type-Effectiveness oder Type-Enum-Arbeit.
- Sprite-/Graphics-Repointing.
- Custom Player Graphics.
- ROM-/Build-/Harness-Diagnosen.

## Ergebnis

Der getestete CFRU/DPE Gen9-BPRE-Stand hat einen belegten Palette-Safety-Pfad: fehlende/invalid Paletten blockieren den Load nicht mehr, und unveraenderte Paletten werden beim Save uebersprungen. Dieser Safety-Pfad beweist nicht, dass `PokemonPalettesMod.RANDOM`, `Gen3to5PaletteRandomizer` und `savePokemonPalettes()` fuer geaenderte CFRU/DPE-Paletten sicher sind. Echte Palette-Randomization bleibt ein offener Hochrisiko-Writer mit compressed-data-, shared-pointer-, mapping- und repointing-spezifischen Risiken. Graphics/Sprites bleiben ein separates P2-Modell.
