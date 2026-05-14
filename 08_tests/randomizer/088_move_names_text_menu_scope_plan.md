# 088 - CFRU/DPE Move Names / Descriptions Text/Menu-Scope Plan

Datum: 2026-05-14

Workspace-Branch: `analysis/upr-fvx-cfru-dpe-move-names-text-menu-scope-plan`

UPR-FVX-Pin: `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`

## Ziel

Dieser Planblock klaert read-only, ob `FVX-MOVE-005` Randomize Move Names / Move Descriptions fuer den getesteten CFRU/DPE Gen9-BPRE-Stand als eigener Text/Menu-Scope machbar ist oder vorerst zurueckgestellt werden sollte.

Es wurden keine Codeaenderungen, keine Randomizer-Laeufe, keine Builds und keine ROM-Zugriffe ausgefuehrt.

## Ausgangspunkt

Die MoveData-Writer-Kette ist nach Diagnose 084 bis 087 fuer den Byte-Writer-Scope abgeschlossen:

- `FVX-MOVE-001` Randomize Move Power ist GUI-kompatibel.
- `FVX-MOVE-002` Randomize Move Accuracy ist GUI-kompatibel.
- `FVX-MOVE-003` Randomize Move PP ist GUI-kompatibel.
- `FVX-MOVE-004` Randomize Move Types ist GUI-kompatibel.
- `FVX-MOVE-006` Update Moves to Generation ist GUI-kompatibel.
- `FVX-MOVE-005` Randomize Move Names bleibt getrennt vom MoveData-Byte-Writer `+0..+11`.

Der Workspace pinnt `02_external/upr-fvx` auf `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3`.

## Read-only Codepfade

Relevante UPR-FVX-Pfade:

- `random/src/main/java/com/uprfvx/random/Settings.java`
- `random/src/main/java/com/uprfvx/random/GameRandomizer.java`
- `random/src/main/java/com/uprfvx/random/gui/RandomizerGUI.java`
- `random/src/main/java/com/uprfvx/random/randomizers/MoveNameRandomizer.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/RomHandler.java`
- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
- `random/src/main/resources/com/uprfvx/random/gui/Bundle.properties`

Ausloeser:

- Die GUI-Checkbox `Randomize Move Names` ist fuer englische ROMs sichtbar und aktivierbar.
- `Settings.randomizeMoveNames` persistiert den Schalter.
- `GameRandomizer` ruft `moveNameRandomizer.randomizeMoveNames()` nach Move Power, Accuracy, PP und Types auf und vor Move Category.
- `MoveNameRandomizer` veraendert nur `Move.name` im geladenen Java-Move-Modell.

Gen3-Write-Pfad:

- `Gen3RomHandler.loadMoves()` liest Move-Namen aus `MoveNames` mit `MoveNameLength`.
- `Gen3RomHandler.saveMoves()` schreibt `moves[i].name` ueber `writeFixedLengthString(...)` in dieselbe fixed-length Tabelle zurueck.
- `Gen3RomHandler.getMaxMoveNameLength()` liefert `12`.
- `writeFixedLengthString(...)` uebersetzt den String, kuerzt auf die feste Laenge, schreibt bei Platz einen Terminator und fuellt den Rest mit Padding.

Move-Descriptions:

- Es wurde kein `FVX-MOVE-005`-Pfad gefunden, der Move-Descriptions randomisiert.
- `MoveDescriptions` wird im Gen3-Pfad sichtbar fuer TM-Item-Text genutzt, etwa um TM-Beschreibungen aus Move-Descriptions zu lesen und umzubrechen.
- Das ist ein anderer Text-/Pointer-Pfad und nicht Teil des aktuellen MoveNameRandomizer-Features.

## Datenmodell-Einordnung

`FVX-MOVE-005` ist fachlich kein MoveData-Byte-Writer im Sinne von `BattleMove` `+0..+11`.

Fuer Gen3/CFRU/DPE-BPRE ist der belegte direkte Writer:

- Move-Namen-Tabelle: fixed-length Eintraege.
- Laenge: `MoveNameLength` aus RomEntry; fuer FireRed klassisch `13` inklusive Terminator/Padding.
- Randomizer-Limit: `getMaxMoveNameLength() = 12` sichtbare Zeichen.
- Write-Semantik: in-place fixed-length, keine Pointer-Rewrites fuer Move-Namen.

Description-/Menu-Scope ist getrennt:

- Move-Description-Pointer-Tabelle ist pointerbasiert.
- Description-Text kann variable Laenge, Zeilenumbrueche und Repointing-Risiken haben.
- Menus, TM-Item-Texte und andere UI-Referenzen koennen Move-Namen oder Move-Descriptions separat anzeigen.
- Ein Description-Fix waere kein minimaler MoveData-Fix, sondern ein eigener Text/Menu-/Pointer-Scope.

## Risiken

### Move Names

- String-Length: Namen muessen innerhalb der sichtbaren 12-Zeichen-Grenze bleiben.
- Terminator/Padding: fixed-length Writes muessen Terminator und Padding stabil halten.
- Encoding: `translateString(...)` kann Sonderzeichen anders zaehlen als Java-String-Laenge.
- Table-Limits: der aktive CFRU/DPE-Stand hat `moves.total=992`; ein Smoke muss bis `991:PsychicNoise` pruefen.
- Gen9-Namen: lange Namen wie `PsychicNoise` passen knapp in die sichtbare Grenze; generierte Namen duerfen nicht wachsen.
- Log-/Fallback-Marker: `<unknown>` darf nicht automatisch als Name-Write-Fehler gelten, solange Name-Reload-Zaehler stabil sind.

### Move Descriptions / Text/Menu

- Pointer-/Repointing-Bedarf: variable Description-Texte koennen nicht sicher in-place geschrieben werden, wenn sie laenger werden.
- Table-Grenzen: Description-Pointer-Tabellen muessen fuer 992 Moves lueckenlos und plausibel sein.
- Menu-Verweise: Kampf-/Bag-/TM-Texte koennen eigene Textquellen oder gecachte Namen nutzen.
- Text-Encoding und Zeilenumbruch: Descriptions brauchen eigene Zeichen- und Line-Length-Regeln.
- Kopplung an TM/HM-/Tutor-Texte: Description- oder Item-Text-Updates duerfen nicht versehentlich TM/HM-, Tutor-, Egg- oder Learnset-Writer ausweiten.

## Grenzen fuer spaetere Arbeit

Ein spaeterer Fix oder Smoke darf nicht beruehren:

- MoveData-Bytes `+0..+11`.
- TypeChart oder TypeEffectiveness.
- Species-Type-Write.
- TM/HM-, Tutor-, Egg- oder Learnset-Write.
- Palette, Items, Field Items, Shops, Pickup.
- Trainer, Wild, Evolutions.
- Graphics.
- Original-Upstreams.

## Planentscheidung

Empfehlung: `FVX-MOVE-005` nicht als breiten Move Descriptions / Text/Menu-Fix umsetzen.

Ein eigener enger Name-only Smoke ist realistisch:

- nur `Randomize Move Names` aktivieren,
- nur fixed-length Move-Namen-Tabelle pruefen,
- keine Move-Descriptions schreiben,
- keine Pointer oder Repointing-Logik einfuehren,
- keine Menu- oder TM/Tutor-Text-Umschreibung.

Move Descriptions sollten vorerst zurueckgestellt und nur in einem spaeteren Text/Menu-Modell behandelt werden, wenn ein konkreter Description-/Pointer-Befund vorliegt.

## Spaetere Reload-/Review-Kriterien

Fuer einen spaeteren Name-only Smoke:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `logNonEmpty=true`
- Reload erfolgreich
- `moves.total=992`
- hoechster Move bleibt `991:PsychicNoise`
- `moveNameReloadMismatches=0`
- `moveNameLengthViolations=0`
- `moveNameTerminatorPaddingMismatches=0`
- `moveDescriptionPointerMismatches=0` oder nicht beruehrt nachweisbar
- `writeReloadMoveDataMismatches=0`, falls der allgemeine Harness MoveData mitprueft
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9`, `+11` bleiben bytegleich, falls der allgemeine Harness MoveData mitprueft
- `exceptionClass=none`
- `stacktrace=none`

Fuer einen spaeteren Description-/Text/Menu-Plan:

- Pointertable-Range und Entry-Count fuer 992 Moves modellieren.
- In-place vs Repointing-Policy vor jeder Umsetzung entscheiden.
- Text-Encoding, Zeilenumbruch und Menu-/TM-Item-Referenzen getrennt pruefen.
- Keine Kopplung an MoveData-Byte-, TM/HM-, Tutor-, Egg- oder Learnset-Writer.

## Ergebnis

`FVX-MOVE-005` bleibt getrennt vom abgeschlossenen MoveData-Writer-Preserve-Scope. Ein enger Name-only Reload-Smoke ist als naechster Schritt sinnvoll und reviewbar. Move Descriptions / Text/Menu-Repointing bleibt vorerst zurueckgestellt.
