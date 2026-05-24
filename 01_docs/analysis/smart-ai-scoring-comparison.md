# Smart AI Move-Scoring Comparison

Stand: 2026-05-24

## Executive Summary

Der lokale Smoke-Befund, dass CFRU Smart Trainer AI mit `AI_SCRIPT_CHECK_GOOD_MOVE` haeufig Sand Attack oder andere Status-/Utility-Moves nutzt, ist source-backed plausibel.

Die wichtigste Abweichung: NatDex/Ironmon `0x07` ist nicht semantisch identisch mit CFRU `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.

- NatDex/Ironmon `0x07` setzt in der lokalen NatDex-FireRed-Quelle die klassischen Gen3-Scripts `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY` und `AI_SCRIPT_TRY_TO_FAINT`.
- CFRU Runtime-Bit 2 heisst zwar numerisch ebenfalls Bit `1 << 2`, fuehrt aber `AIScript_Positives` aus. Diese Logik ist breiter als NatDex `AI_CheckViability` und bewertet Utility-/Status-Moves ueber Kampfklassen und helper wie `GoodIdeaToLowerAccuracy`.
- CFRU `AIScript_SemiSmart` ist bei gesetztem `AI_SCRIPT_CHECK_GOOD_MOVE` praktisch nicht additiv: die Funktion macht ihre Semi-Smart-Arbeit nur, wenn `AI_SCRIPT_CHECK_GOOD_MOVE` nicht gesetzt ist.
- Sand Attack wird in CFRU nicht als schlechter Move gewertet, solange Accuracy-Senkung moeglich ist; `AIScript_Positives` kann den Move als guten Status-/Utility-Move aufwerten.
- NatDex `AI_CheckViability` behandelt Accuracy-Down zwar ebenfalls explizit, aber deutlich konservativer und mit kleinen +/- Score-Schritten; `AI_TryToFaint` bleibt ein separater KO-/Most-Powerful-Move-Anreiz.

Fazit: Der aktuelle CFRU-v1-Schalter ist source-backed nahe an der numerischen NatDex/Ironmon-`0x07`-Idee, aber nicht verhaltensgleich. Fuer eine Ironmon/NatDex-naehere Version reicht ein reines Flag-Mapping wahrscheinlich nicht; entweder muss die Flag-Kombination konservativer getestet werden oder die alte Gen3-Scriptlogik tiefer portiert/nachgebildet werden.

Follow-up nach lokalem Smoke: v1 war technisch aktiv, zeigte aber im beobachteten Test den erwarteten Utility-/Accuracy-Drop-Spam. Sanitized Befund: ein gegnerisches Taubsi nutzte viermal hintereinander Sandwirbel, obwohl Tackle verfuegbar war. Smart Trainer AI v2 entfernt deshalb `AI_SCRIPT_CHECK_GOOD_MOVE` aus dem `FLAG_SMART_TRAINER_AI`-Hook und testet konservativer `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.

## Scope

Untersucht wurden nur Source- und Dokumentationsquellen. Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, Screenshots, raw Logs, private Pfade oder Patches wurden gelesen, erzeugt oder dokumentiert.

## CFRU AI-Flag- und Script-Mapping

| Datei / Funktion | Source-backed Befund | Bedeutung fuer Smart Trainer AI |
| --- | --- | --- |
| `02_external/CFRU-expansion/include/battle.h:523-525` | Runtime-CFRU definiert `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_SEMI_SMART`, `AI_SCRIPT_CHECK_GOOD_MOVE` als Bits 0, 1, 2. | Das sind die Flags, die `GetAIFlags` und der v1-Schalter wirklich nutzen. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c:44-48` | `sBattleAIScriptTable` mappt Bit 0 auf `AIScript_Negatives`, Bit 1 auf `AIScript_SemiSmart`, Bit 2 auf `AIScript_Positives`. | CFRU Bit 2 ist keine alte Gen3-`TRY_TO_FAINT`-Routine, sondern die CFRU-Positive-Utility-Heuristik. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c:122-130` | Verwendbare Moves starten mit Score `100`; blockierte Moves werden spaeter auf `0` gesetzt. | Kleine Score-Erhoehungen koennen reichen, wenn Damage-Moves keinen groesseren Boost bekommen. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c:165-238` | `GetAIFlags` liest `VAR_GAME_DIFFICULTY`, laedt Trainer-Flags, aendert sie je nach Difficulty und ORt bei `FLAG_SMART_TRAINER_AI` die Smart-Trainer-AI-Flags dazu. | Der Schalter aendert Trainer-AI-Flags, nicht `VAR_GAME_DIFFICULTY`. |
| `02_external/CFRU-expansion/src/Battle_AI/ai_master.c:880-909` | CFRU fuehrt pro Flag/Funktion C-Heuristiken aus und ersetzt den Move-Score mit dem Rueckgabewert. | Das ist nicht die alte Gen3-AI-Bytecode-Ausfuehrung. |

## CFRU Difficulty-Stufen und AI-Flags

| Difficulty | Source in `GetAIFlags` | Trainer-AI-Effekt | Grenze |
| --- | --- | --- | --- |
| Normal / `0` | Basisfall | Nutzt Trainerdaten-`aiFlags` unveraendert. | Keine globale Smart-Trainer-Anhebung. |
| Easy / `1` | `OPTIONS_EASY_DIFFICULTY` | Entfernt `AI_SCRIPT_CHECK_GOOD_MOVE` von smarten Trainern und setzt sonst `AI_SCRIPT_CHECK_BAD_MOVE`. | Macht Trainer-AI leichter. |
| Hard / `2` | `OPTIONS_HARD_DIFFICULTY` | Fuegt normalen Trainern `AI_SCRIPT_SEMI_SMART` hinzu, wenn sie nicht schon `AI_SCRIPT_CHECK_GOOD_MOVE` haben. | Keine automatische `CHECK_GOOD_MOVE`-Anhebung fuer alle Trainer. |
| Expert / `3` | `OPTIONS_EXPERT_DIFFICULTY` | Trainer wie Hard; wild Pokemon erhalten zusaetzlich `AI_SCRIPT_CHECK_BAD_MOVE | WildMonIsSmart(...)`. | Expert hat weitere Nicht-AI-Nebeneffekte in anderen Dateien. |
| Smart Trainer AI v1 | `FLAG_SMART_TRAINER_AI` | ORt in Trainerkaempfen `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`. | Bleibt numerisch `0x07`-nah, aber aktiviert CFRU-`AIScript_Positives`. |
| Smart Trainer AI v2 | `FLAG_SMART_TRAINER_AI` | ORt in Trainerkaempfen `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`. | Weniger NatDex-`0x07`-nah, aber vermeidet den `AIScript_Positives`-Pfad, der Accuracy-/Utility-Spam ausloesen kann. |

## CFRU Move-Scoring: Sand Attack und Status

### Negative / Bad-Move-Pruefung

`AIScript_Negatives` ist der CFRU-Bit-0-Pfad:

- `02_external/CFRU-expansion/src/Battle_AI/ai_negatives.c:111-130` initialisiert Kontext, Move, Prediction, Effect, Split, Typ, Accuracy und Viability.
- `ai_negatives.c:435-441` macht Accuracy-Down schlecht, wenn Keen Eye den Effekt verhindert.
- `ai_negatives.c:1247-1340` behandelt Stat-Down-Effekte. Attack-/SpAtk-Down werden nur sinnvoll gelassen, wenn passende gegnerische physische/spezielle Moves vorhanden sind. Accuracy-Down wird dagegen nur hart abgestraft, wenn der Accuracy-Stat nicht gesenkt werden kann, und laeuft sonst durch die Substitute-Pruefung.

Konsequenz: Sand Attack wird durch die negative Pruefung nicht abgestraft, wenn Accuracy-Senkung technisch moeglich ist.

### Positive / Good-Move-Pruefung

`AIScript_Positives` ist der CFRU-Bit-2-Pfad:

- `02_external/CFRU-expansion/src/Battle_AI/ai_positives.c:42-78` startet die positive Bewertung mit Kampfklasse, Prediction und Move-Effekt-Switch.
- `ai_positives.c:532-536` wertet `EFFECT_ACCURACY_DOWN` und `EFFECT_ACCURACY_DOWN_2` auf, wenn `GoodIdeaToLowerAccuracy(...)` true ist.
- `02_external/CFRU-expansion/src/Battle_AI/ai_util.c:3414-3425` macht `GoodIdeaToLowerAccuracy` nur von KO-Shortcut, Contrary/Clear Body/stat-lowering-blocks, Mind's Eye und Clear Amulet abhaengig. Es prueft nicht, ob der Gegner physisch oder speziell angreift.
- `02_external/CFRU-expansion/src/Battle_AI/ai_advanced.c:1726-1798` wandelt `INCREASE_STATUS_VIABILITY(1)` je nach Kampfklasse in groessere Score-Erhoehungen um, z. B. `4 + boost` fuer `FIGHT_CLASS_SWEEPER_SETUP_STATUS`, `3 + boost` fuer Stall/Cleric oder noch mehr in einigen Doubles-Klassen.

Konsequenz: Ein technisch gueltiger Accuracy-Drop kann in CFRU als guter Status-/Utility-Move gelten. Wenn ein Damage-Move keinen sicheren schnellen KO liefert, kann die Status-Aufwertung die Damage-Aufwertung ueberholen.

### Damage- und KO-Anreiz

Damage wird in CFRU trotzdem bewertet:

- `02_external/CFRU-expansion/src/Battle_AI/ai_positives.c:2761-2862` erhoeht Viability fuer schnelle sichere KOs, langsamere KO-Moves, desperate strongest moves und strongest moves.
- Schnelle sichere KOs koennen `+9` bekommen.
- Ein normaler strongest move ohne sicheren KO bekommt haeufig nur `+2`; class-abhaengige Sonderfaelle koennen hoeher sein.

Damit ist CFRU nicht "status-only". Der observed Sand-Attack-Effekt entsteht eher aus einer Utility-Heuristik, die Accuracy-Drops breit als nuetzlich ansieht, waehrend Damage nicht immer stark genug priorisiert wird.

### SemiSmart ist bei CHECK_GOOD_MOVE nicht additiv

`02_external/CFRU-expansion/src/Battle_AI/ai_positives.c:2866-2979` definiert `AIScript_SemiSmart`.

Wichtiger Punkt: Die Funktion arbeitet nur, wenn `AI_SCRIPT_CHECK_GOOD_MOVE` nicht gesetzt ist. Wenn der v1-Schalter alle drei Bits setzt, gibt `AIScript_SemiSmart` am Ende nur `originalViability` zurueck. Der eigentliche v1-Verhaltenssprung kommt daher hauptsaechlich von:

- `AIScript_Negatives`
- `AIScript_Positives`
- gemeinsam genutzten AI-Pfaden, die `aiFlags > AI_SCRIPT_CHECK_BAD_MOVE` als "smarter als basic" interpretieren

Nicht von einer additiven Kombination aus SemiSmart plus GoodMove-Scoring.

## NatDex / Ironmon `0x07` Scoring

Die lokale NatDex-/Ironmon-Quelle bleibt der source-backed Beleg fuer das Smart-AI-Patchverhalten:

| Datei / Funktion | Source-backed Befund | Bedeutung |
| --- | --- | --- |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/romhandlers/Gen3RomHandler.java:2067-2068` | Smart-AI-Mode ORt das Trainer-AI-Flag-Byte mit `0x07`. | Smart AI wird trainerdatenbasiert gesetzt, nicht ueber CFRU Difficulty. |
| `02_external/references/cyansmp64-pokefirered-natdex/include/constants/battle_ai.h:37-39` | Bits 0-2 sind `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY`, `AI_SCRIPT_TRY_TO_FAINT`. | NatDex-Name/Semantik unterscheidet sich von CFRU Runtime-Namen. |
| `02_external/references/cyansmp64-pokefirered-natdex/src/battle_ai_script_commands.c:304-389` | Move-Scores starten bei `100`; Trainer-AI-Flags kommen aus `gTrainers[...].aiFlags`; Sonderfaelle wie Battle Tower koennen ebenfalls `0x07` nutzen. | Klassische Gen3-AI-Flag-Ausfuehrung. |
| `02_external/references/cyansmp64-pokefirered-natdex/src/battle_ai_script_commands.c:405-424` | Fuer jedes gesetzte Bit wird der passende Script-Table-Eintrag ausgefuehrt. | `0x07` laeuft alle drei klassischen Scripts. |
| `02_external/references/cyansmp64-pokefirered-natdex/data/battle_ai_scripts.s:19-22` | Script-Table: `AI_CheckBadMove`, `AI_CheckViability`, `AI_TryToFaint`. | Das sind die drei Scripts hinter NatDex `0x07`. |
| `02_external/references/cyansmp64-pokefirered-natdex/src/battle_ai_script_commands.c:425-454` | Nach Scoring wird der hoechste Score gewaehlt, Ties random. | Kleine Score-Differenzen koennen Move-Auswahl bestimmen. |

## NatDex Accuracy-Down / Sand Attack

NatDex behandelt Accuracy-Down in beiden relevanten Scripts:

- `02_external/references/cyansmp64-pokefirered-natdex/data/battle_ai_scripts.s:302-306`: `AI_CheckBadMove` straft Accuracy-Down nur ab, wenn Target-Accuracy schon Minimum ist, Keen Eye greift oder allgemeine Stat-Blocker greifen.
- `battle_ai_scripts.s:1201-1236`: `AI_CheckViability` nutzt kleine, kontextabhaengige Score-Aenderungen fuer Accuracy-Down. Es kann Accuracy-Down abwerten, wenn User/Target-HP- oder Accuracy-Stage-Kontexte schlecht sind, und kann es aufwerten, wenn z. B. Toxic, Leech Seed, Ingrain oder Curse-Kontexte vorliegen.
- `battle_ai_scripts.s:2599-2619`: `AI_TryToFaint` ist davon getrennt und belohnt KO-Moves oder straft nicht-staerkste Moves leicht ab; es macht Accuracy-Down nicht selbst zu einem KO-/Damage-Favoriten.

Interpretation: NatDex/Ironmon `0x07` kann Sand Attack zulassen und in bestimmten Stall-/Residual-Kontexten sogar aufwerten. Der lokale Source-Beleg zeigt aber keine CFRU-aehnliche Kampfklassen-Positive-Utility-Logik, die Accuracy-Drops allgemein als "good move" boostet, sobald sie technisch moeglich sind.

## Vergleich: CFRU CHECK_GOOD_MOVE vs NatDex CHECK_VIABILITY

| Frage | Source-backed Antwort |
| --- | --- |
| Entspricht CFRU `CHECK_GOOD_MOVE` NatDex `CHECK_VIABILITY`? | Nein, nicht 1:1. Beide sind Bit 2 vs. NatDex Bit 1/Script-2-aehnliche Viability-Ideen nur konzeptionell verwandt. CFRU `CHECK_GOOD_MOVE` fuehrt `AIScript_Positives` aus, eine C-Heuristik mit Kampfklassen, Predictions und vielen modernen CFRU-Effekten. |
| Entspricht CFRU `SEMI_SMART` NatDex `0x07`? | Nein. `AIScript_SemiSmart` ist eine eigene CFRU-Funktion fuer generische Trainer und macht bei gesetztem `CHECK_GOOD_MOVE` keine SemiSmart-Arbeit. |
| Welche CFRU-Flags sind numerisch am naechsten an NatDex `0x07`? | `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`, weil das CFRU Runtime-Bits 0, 1, 2 setzt. |
| Welche CFRU-Flags sind verhaltensnah? | Nur teilweise. Bit 0 ist am klarsten vergleichbar. Bit 1/2 sind CFRU-eigene Semantiken statt NatDex `CHECK_VIABILITY` / `TRY_TO_FAINT`. |
| Warum kann CFRU Sand Attack hoch bewerten? | Negative prueft nur Blocker/Unmoeglichkeit; Positive ruft `GoodIdeaToLowerAccuracy`; `INCREASE_STATUS_VIABILITY` kann je nach Kampfklasse mehr bringen als ein nicht-KO-Damage-Move. |

## Was der lokale Smoke wahrscheinlich gesehen hat

Bei Normal Difficulty plus v1 `FLAG_SMART_TRAINER_AI` passierte in Trainerkaempfen:

1. `GetAIFlags` ORt `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`.
2. Die negative Pruefung verhindert klar schlechte Moves, aber laesst Sand Attack zu, wenn Accuracy-Senkung moeglich ist.
3. `AIScript_SemiSmart` liefert wegen gesetztem `CHECK_GOOD_MOVE` keine eigene Score-Aenderung.
4. `AIScript_Positives` erkennt Accuracy-Down als gute Idee, solange der Gegner nicht durch relevante Faehigkeiten/Items/Statblocker geschuetzt ist und kein offensichtlicher KO-Shortcut greift.
5. `IncreaseStatusViability` kann den Status-/Utility-Boost groesser machen als den normalen `+2`-Boost fuer den staerksten nicht-KO-Damage-Move.

Das erklaert, warum ein Trainer mit Sand Attack und einem maessigen Angriff haeufig Sand Attack waehlen kann, obwohl ein menschlicher Ironmon-Spieler "Smart AI" eher als damage-orientierter erwartet.

Der lokale Smoke bestaetigte diesen Risikopfad praktisch: ein gegnerisches Taubsi nutzte viermal hintereinander Sandwirbel trotz verfuegbarem Tackle. Das beweist nicht, dass jeder v1-Kampf statuslastig ist, reicht aber als gezielter Regressionsgrund fuer eine konservativere v2-Flag-Kombination ohne `AI_SCRIPT_CHECK_GOOD_MOVE`.

## Bewertung fuer das Projekt

Empfehlung: v1 nicht als "exakter Ironmon/NatDex Smart-AI-Port" beschreiben.

Pragmatische Optionen:

| Option | Bewertung |
| --- | --- |
| v1 behalten | Nicht empfohlen als Randomizer-Default nach dem Sandwirbel-Smoke, ausser das Ziel ist bewusst "CFRU strong utility AI". |
| v2 ohne `CHECK_GOOD_MOVE` | Empfohlen fuer den naechsten Smoke: `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`. Das ist weniger NatDex-`0x07`-nah, aber besser passend zum Ziel "bessere offensive Move-Auswahl ohne Utility-Spam". |
| Tieferer Port | Noetig, wenn das Ziel "Ironmon/NatDex `0x07` verhaltensnah" ist. Dann reicht das CFRU-Bit-Mapping nicht; man muesste die NatDex `AI_CheckViability` / `AI_TryToFaint`-Semantik nachbilden oder gezielt anpassen. |

Projekt-Empfehlung fuer den naechsten Schritt:

- v2-Schalter mit `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART` smoke-testen.
- Den Smoke explizit auf statuslastige Move-Auswahl ausweiten: Sand Attack/Sandwirbel, Accuracy-Drops, Status, Setup, sicherer KO, staerkster Damage-Move.
- Danach entscheiden, ob diese konservativere CFRU-native AI fuer den Randomizer-Default ausreicht oder ob ein tieferer NatDex/Ironmon-Port noetig ist.
- Keine Difficulty-Hard/Expert-Nebeneffekte als Ausweichloesung verwenden.

## Risiken und Annahmen

- Die historische BPS-/ROM-Patchvariante wurde nicht byteweise analysiert; der source-backed Vergleich stuetzt sich auf die lokale CyanSMP64-NatDex-Randomizer- und FireRed-NatDex-Quelle.
- NatDex `0x07` ist als Trainer-Flag-OR belegt, aber nicht jede historische Ironmon-Smart-AI-Variante muss exakt identisch sein.
- CFRU hat moderne Move-Effekte, Kampfklassen, Prediction- und Utility-Pfade, die in der alten NatDex-FireRed-Scriptlogik nicht 1:1 existieren.
- Ohne Battle-Smoke mit kontrollierten Movesets bleibt offen, wie stark der Sand-Attack-Effekt statistisch ist.

## Naechste Analyse-/Testpunkte

- A/B-Smoke mit denselben Trainern und Movesets:
  - Flag off
  - v2 `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`
  - bei Bedarf Vergleich gegen v1 all-three-flags als bekannte utility-lastige Referenz
- Fuer jeden Sample-Trainermove dokumentieren: sicherer KO, staerkster Damage, Status/Accuracy-Drop, Setup, Typeneffekt.
- Source-seitig pruefen, ob eine kleine CFRU-native Tuning-Stelle fuer Accuracy-Drops existiert, ohne NatDex/Ironmon-Naehenaussage zu vermischen.
- Wenn exakte Ironmon-Naehe erforderlich wird, Design fuer einen tieferen Port von `AI_CheckViability` und `AI_TryToFaint` ausarbeiten.
