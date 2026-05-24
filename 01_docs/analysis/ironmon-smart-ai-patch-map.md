# Ironmon / NatDex Smart AI patch map

Stand: 2026-05-24

## Executive summary

Der source-backed Kern der Ironmon/NatDex-Smart-AI-Variante ist kein CFRU-Difficulty-Modus, sondern ein Trainer-AI-Flag-Upgrade:

- Die öffentliche Super-Kaizo-IronMON-Doku beschreibt Smart AI als Regel/Patch-Ziel für alle Trainer und verweist zusätzlich auf einen Smart-AI-Randomizer.
- Die lokal vorhandene CyanSMP64-NatDex-Randomizer-Quelle implementiert `Smart AI Mode` fuer Gen3, indem sie beim Schreiben jedes Trainerdatensatzes das AI-Flag-Byte mit `0x07` verodert.
- In der lokalen CyanSMP64-FireRed-NatDex-Quelle entsprechen diese drei Bits `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY` und `AI_SCRIPT_TRY_TO_FAINT`.
- Es gibt in den geprueften Quellen keinen Beleg, dass dieser Smart-AI-Randomizer Trainer-Level, IV/EV, Friendship, PP, Bag-Regeln, Spieler-Move-Restriktionen, Wild/Raid-AI oder CFRU-Battle-Rules veraendert.

Damit ist unser CFRU-Ansatz `FLAG_SMART_TRAINER_AI` konzeptionell nah, solange er nur Trainer-AI-Flags in `GetAIFlags` erweitert und `VAR_GAME_DIFFICULTY` Normal laesst. Eine reine `AI_SCRIPT_SEMI_SMART`-Anhebung ist aber wahrscheinlich schwaecher als der NatDex/Ironmon-Randomizer-Beleg `0x07`.

## Gemeinte Varianten

| Variante | Quelle | Source-backed Befund | Risiko / Grenze |
|---|---|---|---|
| Alter BPS/ROM-Patch | `https://github.com/PyroMikeGit/SuperKaizoIronMON` und Release-Seiten | Oeffentliche Regeln sagen, dass jeder Trainer Smart AI hat und fuer FRLG ein ROM-Patch existiert. | BPS/ROM-Patches wurden nicht heruntergeladen, angewendet oder byteweise analysiert. Exakte Patch-Diffs bleiben unbewiesen. |
| Smart AI Randomizer | `https://github.com/PyroMikeGit/SuperKaizoIronMON/releases/tag/smart-ai-v2` | Release beschreibt einen Randomizer, der Smart AI fuer Trainer ohne separaten Patch anwenden kann; Gen6/7 und NatDex werden oeffentlich erwaehnt. | Release-Artefakte wurden nicht heruntergeladen. Der lokale source-backed Implementierungsbeleg kommt aus der CyanSMP64-NatDex-Randomizer-Quelle. |
| NatDex-kompatibler Randomizer | `02_external/references/cyansmp64-upr-zx-natdex/**` | GUI-Text benennt `Smart AI Mode`; Gen3-Schreibpfad setzt `rom[trOffset + (entryLen - 12)] |= 0x07`. | Setting-Name im Code ist legacy `swapTrainerMegaEvos`; GUI-Text/Tooltip repurposen ihn als Smart AI Mode. |
| FireRed AI-Flag-Semantik | `02_external/references/cyansmp64-pokefirered-natdex/**` | Trainerdaten besitzen `aiFlags`; Battle-AI laedt `gTrainers[gTrainerBattleOpponent_A].aiFlags`; Bits 0-2 sind Bad-Move-Check, Viability-Check, Try-to-Faint. | Das ist die NatDex/pret-nahe Gen3-Semantik, nicht automatisch identisch mit CFRU-Scriptnamen. |

## Was oeffentlich dokumentiert ist

PyroMikeGit/SuperKaizoIronMON dokumentiert Smart AI als Super-Kaizo-Regel: jeder Trainer soll Smart AI haben, und fuer ROM-basierte Workflows existieren Patch-Downloads. Dieselbe Doku nennt einen Smart-AI-Randomizer, der Smart AI fuer Trainer ohne separaten Patch anwenden kann.

Der Release `smart-ai-v2` dokumentiert den Smart-AI-Randomizer als Ersatz fuer den normalen Randomizer-JAR und nennt NatDex als Fall, in dem Smart AI eingebaut ist.

Die oeffentlichen Seiten beweisen damit das Ziel und den Workflow, aber nicht allein den genauen Byte-/Source-Diff. Der genaue lokal belegte Gen3-Mechanismus kommt aus der CyanSMP64-NatDex-Randomizer-Quelle.

## Lokal belegte Implementierung

| Datei / Funktion | Wert / Bedingung | Effekt | Kategorie |
|---|---|---|---|
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/newgui/Bundle.properties:552` | `GUI.tpSwapMegaEvosCheckBox.text=Smart AI Mode` | GUI zeigt die Trainer-Pokemon-Option als Smart AI Mode an. | UI |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/newgui/Bundle.properties:553` | Tooltip: alle Trainer-AIs werden auf das Niveau vieler Gym Leader, Elite Four, Ace Trainer usw. gesetzt. | Dokumentiert erwartetes Verhalten aus Nutzersicht. | UI / Anzeige |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/Randomizer.java:451` | `settings.isSwapTrainerMegaEvos()` | Legacy-Setting triggert `romHandler.smartAiMode()`. | Randomizer-Steuerung |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/romhandlers/AbstractRomHandler.java:2837` | `smartAiMode()` | Laedt aktuelle Trainer und ruft `setTrainers(currentTrainers, false, true)` auf. | Randomizer-Steuerung |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/romhandlers/Gen3RomHandler.java:1882` | Trainerdatensatz-Kommentar `AI Flags; 1 byte` | Belegt die Position des Gen3-AI-Flag-Bytes im Trainerdatensatz. | Trainerdaten |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/romhandlers/Gen3RomHandler.java:2067` | `if (smartAiMode)` | Smart-AI-Schreibzweig ist vom normalen Trainer-Schreibpfad getrennt. | Trainer-AI |
| `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/romhandlers/Gen3RomHandler.java:2068` | `rom[trOffset + (entryLen - 12)] |= 0x07` | Setzt Bits 0, 1 und 2 im Trainer-AI-Flag-Byte, ohne vorhandene hoehere Flags zu loeschen. | Trainer-AI |
| `02_external/references/cyansmp64-pokefirered-natdex/include/constants/battle_ai.h:37` | `AI_SCRIPT_CHECK_BAD_MOVE (1 << 0)` | Bit 0 aktiviert Bad-Move-Pruefung. | Battle-AI |
| `02_external/references/cyansmp64-pokefirered-natdex/include/constants/battle_ai.h:38` | `AI_SCRIPT_CHECK_VIABILITY (1 << 1)` | Bit 1 aktiviert Viability-Pruefung. | Battle-AI |
| `02_external/references/cyansmp64-pokefirered-natdex/include/constants/battle_ai.h:39` | `AI_SCRIPT_TRY_TO_FAINT (1 << 2)` | Bit 2 aktiviert Try-to-Faint-Logik. | Battle-AI |
| `02_external/references/cyansmp64-pokefirered-natdex/include/battle.h:141` | `u32 aiFlags` in `struct Trainer` | Trainerdaten tragen AI-Flags als Battle-relevantes Feld. | Trainerdaten |
| `02_external/references/cyansmp64-pokefirered-natdex/src/battle_ai_script_commands.c:382` | `AI_THINKING_STRUCT->aiFlags = gTrainers[...].aiFlags` | Battle-AI uebernimmt die Trainer-AI-Flags zur Move-/Action-Auswahl. | Battle-AI |
| `02_external/references/cyansmp64-pokefirered-natdex/src/rom_header_gf.c:643` | `.offsetTrainerFlagsAI = offsetof(struct Trainer, aiFlags)` | Exportiert den Trainer-AI-Flag-Offset fuer Tools/Randomizer. | Tooling / Offset-Metadaten |

## Was nicht source-backed bewiesen ist

- Die BPS/ROM-Patches wurden nicht heruntergeladen, nicht angewendet und nicht byteweise verglichen.
- Der exakte alte FireRed-v1.0/v1.1-BPS-Diff ist in diesem Arbeitsblock nicht bewiesen.
- Die oeffentliche `tom-overton/pokefirered`-Branch `smart-ai` wurde nur als Web-Referenz geprueft, nicht geklont oder lokal diff-geprueft.
- Es ist nicht bewiesen, dass alle historischen Smart-AI-Patchvarianten exakt dieselbe `0x07`-Strategie verwenden.
- Es ist nicht bewiesen, dass die Super-Kaizo-Regeln als Ganzes nur Smart AI betreffen. Die Regel-Doku enthaelt zusaetzliche Challenge-Regeln; diese sind aber Regelwerk/Setup, nicht automatisch Smart-AI-Patchlogik.

## Betrifft der Patch nur Trainer-AI?

Fuer die lokal belegte CyanSMP64-NatDex-Randomizer-Implementierung: ja, der Smart-AI-spezifische Codepfad setzt nur Trainer-AI-Flags.

Nicht belegt als Smart-AI-spezifische Aenderung:

- Trainer-Level-Scaling
- Trainer-IV/EV/Friendship/PP-Buffs
- Trainer-Items oder Movesets
- Spieler-Bag-Restriktionen
- Spieler-Move-Restriktionen
- Wild-AI oder Raid-AI
- Battle-Rules wie Singles/Doubles, Switch-Mode oder Item-Verbote

Wichtig: Der Gen3-Handler schreibt im selben `setTrainers`-Pfad auch Trainerparties, wenn andere Randomizer-Einstellungen Trainerdaten veraendern. Der Smart-AI-Zweig selbst ist aber das `0x07`-OR auf dem AI-Flag-Byte.

## Move-Auswahl, Switching, Items und Regeln

| Bereich | Beleg | Ergebnis |
|---|---|---|
| Move-Auswahl / Battle-AI | Trainer-AI-Flags werden in `AI_THINKING_STRUCT->aiFlags` geladen. Bits 0-2 aktivieren AI-Scripts. | Ja, echte Battle-AI-Entscheidungen sind betroffen. |
| Switching | In den lokal geprueften NatDex-Smart-AI-Randomizer-Treffern kein separater Switching-Hook gefunden. | Nicht belegt. |
| Trainer-Items | Smart-AI-Zweig setzt nur AI-Flag-Byte. | Nicht belegt als Smart-AI-Effekt. |
| Held Items / sensible items | Super-Kaizo-Regeln nennen sensible held items als separate Regel. | Nicht Teil des source-backed Smart-AI-Flag-Mechanismus. |
| Spieler-Regeln | Super-Kaizo-Regeln enthalten zusaetzliche Verbote/Restriktionen. | Regelwerk, nicht als Smart-AI-Patchlogik bewiesen. |
| Wild/Raid | Keine NatDex-Smart-AI-Randomizer-Belege fuer Wild/Raid-Hooks. | Nicht belegt. |

## Vergleich mit unserem CFRU-Ansatz

Unsere CFRU-Dokus zeigen als sauberen Eingriffspunkt `GetAIFlags` in `02_external/CFRU-expansion/src/Battle_AI/ai_master.c`: eine neue Runtime-Option koennte normale Trainer-AI-Flags erweitern, ohne `VAR_GAME_DIFFICULTY` auf Hard/Expert zu setzen.

| Punkt | Ironmon/NatDex Smart AI | CFRU `FLAG_SMART_TRAINER_AI`-Ansatz |
|---|---|---|
| Runtime-Difficulty | Kein `VAR_GAME_DIFFICULTY`. | `VAR_GAME_DIFFICULTY` bleibt Normal. |
| Trainer-Build-Strength | Lokal belegter Smart-AI-Zweig setzt nur AI-Flags. | Soll `build_pokemon.c`, IV/EV/Friendship/PP und Level unveraendert lassen. |
| Wild/Raid | Nicht belegt. | Soll nicht mitportiert werden. |
| Anti-Cheese-Expert-Logik | Nicht belegt. | Soll nicht mitportiert werden. |
| AI-Flag-Niveau | Lokal belegt als OR `0x07`: Bits 0, 1, 2. | Bisheriger Minimalvorschlag `AI_SCRIPT_SEMI_SMART` ist nah, aber schwaecher als `0x07`. |
| UI/Randomizer-Semantik | Cyan GUI nennt es Smart AI Mode fuer Trainer. | Sollte als separate Trainer-AI-Option benannt werden, nicht als Difficulty. |

## Bewertung: nahe genug fuer Version 1?

Ja, wenn Version 1 bewusst als nicht-invasive Smart-Trainer-AI-Option definiert wird: getrennt von Difficulty, nur Trainer-AI, keine Trainer-Staerke- oder Spielerrestriktions-Nebeneffekte.

Fuer genaue Ironmon/NatDex-Aequivalenz ist `AI_SCRIPT_SEMI_SMART` allein wahrscheinlich nicht genug. Der staerkere, source-naehere CFRU-Vorschlag waere:

- `VAR_GAME_DIFFICULTY` bleibt Normal.
- Neuer Trainer-AI-Schalter greift nur in `GetAIFlags`.
- Bei aktivem Schalter werden fuer normale Trainer die passenden CFRU-AI-Bits mindestens auf das Ironmon/NatDex-Niveau gehoben.
- Kandidat fuer diese Bits: `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART | AI_SCRIPT_CHECK_GOOD_MOVE`, sofern CFRU-Semantik und Tests bestaetigen, dass dies die naechste Entsprechung zu Gen3 `0x07` ist.

Der konservativere `AI_SCRIPT_SEMI_SMART`-Only-Ansatz ist sicherer, aber sollte dann nicht als exakte Ironmon-Smart-AI-Portierung beschrieben werden.

## Testbedarf

- Source-Test: `GetAIFlags` mit neuer Option pruefen, dass nur Trainer-AI-Flags geaendert werden.
- Regression: `VAR_GAME_DIFFICULTY` bleibt Normal und Hard/Expert-Nebeneffekte bleiben aus.
- Battle-Smoke: normaler Low-AI-Trainer nutzt nach Option bessere Move-Auswahl.
- Negative Tests: keine Aenderung an Trainer-Leveln, IV/EV, Friendship, PP, Items, Movesets, Bag-Zugriff, Spieler-Move-Verboten, Wild/Raid-AI und Battle-Rules.
- Vergleichstest: wenn moeglich lokal einen bekannten NatDex/Smart-AI-Randomizer-Ausgabefall gegen CFRU-Flag-Level vergleichen, ohne ROMs oder Patches in die Workspace-Doku zu uebernehmen.

## Naechste minimale Entscheidung

Fuer den CFRU-Source-Port sollte entschieden werden, ob Version 1:

1. maximal konservativ bleibt und nur `AI_SCRIPT_SEMI_SMART` setzt, oder
2. source-naeher zur Ironmon/NatDex-Variante die drei relevanten CFRU-AI-Bits setzt.

Die Doku spricht gegen `VAR_GAME_DIFFICULTY` als Smart-AI-Schalter. Der naechste technische Schritt sollte eine kleine CFRU-Implementierung mit eigenem Trainer-AI-Schalter sein, plus Tests/rg-Nachweise, dass keine Difficulty-Nebeneffekte aktiviert wurden.
