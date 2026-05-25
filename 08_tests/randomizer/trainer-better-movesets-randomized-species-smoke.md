# Trainer Better Movesets With Randomized Species Smoke Plan

Datum: 2026-05-25

## Ziel

Dieser Smoke prueft, ob Trainer-Pokemon nach Foe-Pokemon-Randomization plus Better Movesets Moves bekommen, die zur final randomisierten Species passen, statt alte Custom-Moves des Original-TrainerPokemon zu behalten.

Der Plan ist lokal auszufuehren. Keine ROMs, Saves, Emulator States, Screenshots, raw Logs, Hashes, private Pfade, Output-ROMs oder Build-Artefakte werden committed.

## Voraussetzungen

- UPR-FVX mit Trainer-Pokemon-Randomization aktiv.
- Better Trainer Movesets aktiv, idealerweise getrennt und dann kombiniert:
  - Regular
  - Important
  - Boss
- CFRUDPEExtension installiert mit `gBattleMons` Active-Battle-Reader.
- Lokale ignored Manifeste fuer die Extension vorhanden, soweit fuer `gBattleMons` noetig.
- Sanitized Dokumentation nur mit Trainerrolle, Species, Level und Move-Namen.

## Testmatrix

| Fall | Setup | Erwartung |
| --- | --- | --- |
| A: Flag/Basis | Trainer Species randomisiert, Better Movesets aus | Randomisierte Species soll entweder keine Custom-Moves schreiben oder levelbasierte Moves aus dem aktuellen Species-Kontext bekommen. |
| B: Regular Better Movesets | Trainer Species randomisiert, Better Regular Movesets an | Regular Trainer bekommt Moves aus Pool der randomisierten Species oder sicheren Fallback, nicht alte Original-Moves. |
| C: Important/Rival | Trainer Species randomisiert, Better Important Movesets an | Rival-Nichtstarter koennen randomisiert sein; forcierter Starter-Slot muss Counter-Starter bleiben. |
| D: Boss Better Movesets | Trainer Species randomisiert, Better Boss Movesets an | Boss-Trainer bekommen neue Moves oder sicheren Fallback. |
| E: Empty-Pool-Kandidat | Species mit auffaellig leerem/kleinem Pool oder niedrigem Level | Kein altes Move-Set darf erhalten bleiben, wenn Better Movesets keinen Pool findet. |

## Rival-Starter-Sondercheck

Dokumentiere fuer Rival-Battles getrennt:

- Battle-Kontext: Oak-Lab erster Rival, Route-22 Rival oder anderer Trainer.
- Ob der beobachtete Slot der forcierte Starter-Slot oder ein Nichtstarter ist.
- Player-Starter und erwarteter Rival-Counter-Starter nur als Species-Namen.
- Enemy Species/Level/Moves aus `gBattleMons`.

Pass-Kriterium:

- Der forcierte Rival-Starter-Slot bleibt der korrekte Counter-Starter.
- Ein randomisierter Rival-Nichtstarter darf randomisiert sein, darf aber keine alten Custom-Moves behalten.

## Pass/Fail-Kriterien

PASS:

- Randomisierte Trainer-Species zeigen plausible Moves aus ihrer eigenen Learnset-/Better-Movesets-Basis oder einem dokumentierten sicheren Fallback.
- Keine beobachtete randomisierte Species traegt offensichtlich alte Original-Trainer-Moves wie im lokalen Beispiel `Incineroar Lv6` mit `Tackle` / `String Shot` / `Stun Spore`.
- Rival-Starter-Slot bleibt korrekt, wenn eindeutig identifiziert.

FAIL:

- Eine randomisierte Trainer-Species zeigt alte Moves aus dem Original-TrainerMon-Kontext.
- Der forcierte Rival-Starter-Slot ist nicht der erwartete Counter-Starter.
- Better Movesets erzeugt leeren Pool und deaktiviert trotzdem den Reset-Fallback.

## Zu pruefende Fix-Regression

Nach einem Fix sollte ein fokussierter Test bestaetigen:

- `TrainerPokemonRandomizer` setzt nach Species-Ersatz weiterhin `resetMoves=true`.
- `TrainerMovesetRandomizer` setzt `resetMoves=false` erst, wenn ein nichtleerer Pool tatsaechlich Move-Slots geschrieben hat.
- Bei leerem Pool bleibt der Gen3-Writer-Fallback aktiv oder es wird ein expliziter sicherer Fallback geschrieben.
- Bei einem nichtleeren Pool mit `MOVE_NONE` / leerem Slot-Kandidaten werden nur echte Moves geschrieben und nach vorne kompaktiert; ein Ergebnis wie `[-/Move/Move/Move]` ist ein Fail.
- Reload bleibt ohne Species-/Move-Mismatches.
- `gBattleMons` zeigt im Kampf die final erwarteten Moves.

## Implementierungsstand

UPR-FVX Fix-Branch `fix/trainer-better-movesets-empty-pool`:

- Better Movesets schreibt Move-Slots nur noch ueber einen zentralen Helper, der danach `resetMoves=false` setzt.
- Bei leerem Better-Movesets-Pool bleibt `resetMoves` unveraendert; nach Trainer-Species-Randomization bleibt damit der Gen3-Writer-Fallback aktiv.
- ROM-freie Regression deckt ab:
  - leerer Pool behaelt `resetMoves=true` und laesst alte Custom-Moves nicht als aktive Custom-Moves gelten.
  - nichtleerer Pool schreibt neue Moves und setzt `resetMoves=false`.

Der lokale Gameplay-Smoke mit privatem Output-ROM bleibt der naechste Schritt.

UPR-FVX Follow-up-Branch `fix/rival-starter-trainer-moveslot-regression`:

- Better Movesets filtert `MOVE_NONE` / null moves vor dem Custom-Move-Write und kompaktiert echte Moves nach vorne.
- ROM-freie Regression deckt ab:
  - ein nichtleerer Better-Movesets-Pool mit `MOVE_NONE` schreibt `[move1, move2, move3, 0]`.
  - ein Route-22-artiger Rival mit zwei gleichleveligen Slots behaelt den Counter-Starter im geschuetzten letzten Slot, waehrend der Nichtstarter-Slot weiterhin randomisiert sein darf.
- Lokaler Re-Smoke sollte die sanitized Beispiele `[-/Lick/Tackle/Ember]` und `[-/Astonish/Mudslap/Pound]` erneut pruefen.

UPR-FVX Follow-up-Branch `fix/route22-rival-final-moveslots`:

- Der verbleibende `[-/Move/Move/Move]`-Pfad kann aus dem finalen Reset-Move-Fallback / Gen3-Writer kommen, nicht nur aus Better Movesets.
- `getMovesAtLevel()` ignoriert jetzt `MOVE_NONE`-Platzhalter; der Gen3-Trainer-Writer normalisiert Fallback- und Custom-Move-Slots direkt vor dem Write.
- ROM-freie Regression deckt ab:
  - `MoveLearnt(0, ...)` erzeugt keinen fuehrenden leeren Slot im Level-Fallback.
  - `[0, Blizzard, Crunch, Psycho Cut]` wird vor dem Gen3-Trainer-Write zu `[Blizzard, Crunch, Psycho Cut, 0]` normalisiert.
  - ein Route-22-artiger Rival mit Level-9-Starter-Slot behaelt die schwache Starterstufe und wird nicht durch einen spaeteren/evolvierten Rival-Kontext ersetzt.
- Lokaler Re-Smoke sollte das sanitized Beispiel `Decidueye Lv47` mit `moves[-/Blizzard/Crunch/Psychocut]` erneut pruefen. Wenn weiterhin ein Level-47-Rival im Route-22-Kontext erscheint, ist das separat als Script-/Trainerbattle-Quellkontext zu analysieren.

## Offene Smoke-Notizen

- Kein lokaler Pfad, keine Seed-Strings, keine ROM-Hashes und keine raw Logs in diese Datei kopieren.
- Falls `skippedMissingMovesets` sichtbar ist, nur sanitized als vorhanden/nicht vorhanden oder als grobe Count-Kategorie dokumentieren, nicht als raw Log.
- Wenn ein Befund aus einem Rival-Battle stammt, zuerst Slot und Trainer-Kontext klaeren, bevor er als Rival-Starter-Fehler bewertet wird.
