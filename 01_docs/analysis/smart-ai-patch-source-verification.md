# Smart AI Patch Source Verification

Stand: 2026-05-24

## Executive Summary

Die originale tom-overton FireRed/LeafGreen Smart-AI-Source-Aenderung ist source-backed ein Trainerdaten-Flag-Patch, kein Battle-AI-Scoring-Patch.

Der funktionale Commit auf `tom-overton/pokefirered` Branch `smart-ai` aendert nur `src/data/trainers.h`: bestehende Trainer-`aiFlags = AI_SCRIPT_CHECK_BAD_MOVE` werden auf `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY` erweitert. Die Battle-AI-Scriptdateien, AI-Command-Implementierung und AI-Flag-Konstanten bleiben gegenueber der Basis unveraendert. Der nachfolgende Branch-Commit aendert nur die Titelgrafik.

Die CyanSMP64-NatDex-Randomizer-Integration macht dasselbe Prinzip zur Laufzeit beim Schreiben der Trainerdaten: Gen3 `smartAiMode` setzt fuer jeden Trainerdatensatz das AI-Flag-Byte per `|= 0x07`. In der lokalen NatDex-FireRed-Quelle sind Bits 0-2 `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY` und `AI_SCRIPT_TRY_TO_FAINT`.

Fuer CFRU bedeutet das: v1 war nur numerisch nah an `0x07`, aber nicht verhaltensgleich, weil CFRU Runtime-Bit 2 `AI_SCRIPT_CHECK_GOOD_MOVE` auf `AIScript_Positives` mappt. v2 ist weniger numerisch nah, aber vermeidet genau den `CHECK_GOOD_MOVE`-/`AIScript_Positives`-Pfad, der im lokalen Smoke Sand-Attack-/Utility-Spam plausibel erklaert.

## Scope und Sicherheitsgrenze

Geprueft wurden nur Source/Web/API- und lokale read-only Referenzquellen. Es wurden keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, Patch-Assets, Screenshots, raw Logs, privaten Pfade oder Secrets gelesen, heruntergeladen, erzeugt oder dokumentiert.

Keine externen Repos wurden geklont. Die tom-overton-Pruefung erfolgte ueber GitHub Web/API und Branch-/Commit-/Compare-Metadaten.

## Gepruefte Quellen

| Quelle | Stand / Branch | Source-backed Befund |
| --- | --- | --- |
| `tom-overton/pokefirered` Release `smart-ai` | Release `All Trainers Have "Smart AI"` | Release-Text sagt, dass die Patches FR/LG-Trainern "Smart AI" geben und dass die exakte Code-Aenderung auf Branch `smart-ai` sichtbar ist. |
| `tom-overton/pokefirered` Branch `smart-ai` | Compare ab Branch-Basis `0c17a3b` bis Branch-Head `6f3f738` | Zwei Commits ahead: `fdbe1eb` aendert `src/data/trainers.h`; `6f3f738` aendert nur `graphics/title_screen/copyright_press_start.png`. |
| `tom-overton/pokefirered` Commit `fdbe1eb` | `Give every trainer in the game "smart AI"` | Einzige Datei im funktionalen Commit: `src/data/trainers.h`, 657 Ersetzungen von Trainer-AI-Flag-Ausdruecken. |
| `tom-overton/pokefirered/include/constants/battle_ai.h` | Branch `smart-ai` | Bits 0-2 sind `CHECK_BAD_MOVE`, `CHECK_VIABILITY`, `TRY_TO_FAINT`. |
| Lokale CyanSMP64 UPR-ZX NatDex-Referenz | `02_external/references/cyansmp64-upr-zx-natdex`, Branchstand `natdex` | Gen3 `smartAiMode` setzt im Trainerdaten-Schreibpfad `rom[trOffset + (entryLen - 12)] |= 0x07`. |
| Lokale CyanSMP64 FireRed NatDex-Referenz | `02_external/references/cyansmp64-pokefirered-natdex`, Branchstand `natdex` | AI-Flag-Semantik und Battle-AI-Scripts entsprechen der klassischen Gen3-Struktur. |
| Lokale CFRU-Referenz | `02_external/CFRU-expansion`, aktueller Smart-Trainer-AI-v2-Pin | Runtime-AI-Bits 0-2 sind CFRU-eigene `CHECK_BAD_MOVE`, `SEMI_SMART`, `CHECK_GOOD_MOVE`; v2 nutzt nur Bits 0 und 1. |

## tom-overton FireRed/LeafGreen Smart-AI-Patch

### Dateidiff

GitHub-Compare `0c17a3b...smart-ai` zeigt zwei Dateien:

| Datei | Status | Bedeutung |
| --- | --- | --- |
| `src/data/trainers.h` | modified, 657 additions / 657 deletions | Funktionale Smart-AI-Aenderung. |
| `graphics/title_screen/copyright_press_start.png` | modified, binary | Spaeterer kosmetischer Branch-Commit "PRESS SMART"; nicht Battle-/Trainer-AI-relevant. |

Der funktionale Commit `fdbe1eb` enthaelt nur:

| Datei | Aenderung |
| --- | --- |
| `src/data/trainers.h` | bestehende `.aiFlags = AI_SCRIPT_CHECK_BAD_MOVE` werden auf `.aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY` erweitert. |

### Was nicht geaendert wurde

Im geprueften Compare sind keine Battle-AI-Scoring-Dateien geaendert:

- `data/battle_ai_scripts.s`
- `src/battle_ai_script_commands.c`
- `include/constants/battle_ai.h`

Die GitHub-Content-Metadaten fuer `data/battle_ai_scripts.s`, `src/battle_ai_script_commands.c` und `include/constants/battle_ai.h` sind zwischen der Branch-Basis und `smart-ai` identisch. Damit gibt es source-backed keinen Hinweis, dass tom-overton Smart AI Sand Attack, Accuracy-Lowering, Stat-Drops, KO-Scoring oder Move-Scoring-Code veraendert.

### Welche Flags gesetzt werden

`tom-overton/pokefirered` Branch `smart-ai` verwendet die klassische FireRed-AI-Flag-Semantik:

| Bit | Name | Funktion |
| --- | --- | --- |
| `1 << 0` | `AI_SCRIPT_CHECK_BAD_MOVE` | Schlechte/unmoegliche Moves abwerten. |
| `1 << 1` | `AI_SCRIPT_CHECK_VIABILITY` | Move-Viability anhand klassischer Gen3-Scriptheuristik bewerten. |
| `1 << 2` | `AI_SCRIPT_TRY_TO_FAINT` | KO-/staerkster-Move-orientierten Anreiz ausfuehren. |

Die Kombination entspricht numerisch `0x07`.

## CyanSMP64 NatDex Randomizer Integration

### Steuerung

| Datei / Funktion | Source-backed Befund |
| --- | --- |
| `Randomizer.java:451-453` | `settings.isSwapTrainerMegaEvos()` ruft `romHandler.smartAiMode()` auf. Der Setting-Name ist legacy; die GUI benennt diese Option als Smart AI Mode. |
| `AbstractRomHandler.java:2837-2839` | `smartAiMode()` laedt aktuelle Trainer und ruft `setTrainers(currentTrainers, false, true)` auf. |
| `RomHandler.java:252` | `setTrainers(..., boolean smartAiMode)` ist die Handler-Schnittstelle fuer den Schreibpfad. |

### Gen3-Schreibpfad

| Datei / Zeile | Source-backed Befund |
| --- | --- |
| `Gen3RomHandler.java:1895-1899` | Der Handler liest Gen3-Trainerdatenfelder; `aiFlags` liegen bei `trOffset + (entryLen - 12)`. |
| `Gen3RomHandler.java:2037-2048` | `setTrainers(...)` schreibt Trainerdaten in einer Schleife ueber alle Trainer. |
| `Gen3RomHandler.java:2067-2068` | Bei `smartAiMode` wird exakt `rom[trOffset + (entryLen - 12)] |= 0x07` gesetzt. |

Das ist ein OR auf das vorhandene AI-Flag-Byte. Es loescht keine bereits gesetzten hoeheren AI-Flags und betrifft nicht Trainer-Level, IVs, EVs, Friendship, PP, Held Items, Movesets, Bag-Regeln, Spieler-Move-Restriktionen, Wild/Raid-AI oder Battle-Rules.

### NatDex-FireRed-Semantik

| Datei / Zeile | Source-backed Befund |
| --- | --- |
| `include/constants/battle_ai.h:37-39` | Bits 0-2 sind `AI_SCRIPT_CHECK_BAD_MOVE`, `AI_SCRIPT_CHECK_VIABILITY`, `AI_SCRIPT_TRY_TO_FAINT`. |
| `src/battle_ai_script_commands.c:364-382` | Sonderfaelle koennen 0x07-entsprechende Flags setzen; normale Trainer laden danach `gTrainers[gTrainerBattleOpponent_A].aiFlags`. |
| `data/battle_ai_scripts.s:20-22` | Script-Tabelle mappt Bits 0-2 auf `AI_CheckBadMove`, `AI_CheckViability`, `AI_TryToFaint`. |

## Sand Attack / Accuracy-Drop Bewertung

### Vanilla/NatDex/Smart-AI-Patch

Der tom-overton-Patch aendert keine AI-Scoring-Scripts. Damit bleibt Accuracy-Drop-Verhalten das klassische Gen3-Verhalten.

In der lokalen CyanSMP64 FireRed NatDex-Quelle:

- `AI_CheckBadMove` straft Accuracy-Down nur ab, wenn der Effekt technisch sinnlos/geblockt ist.
- `AI_CheckViability` behandelt Accuracy-Down mit kleinen kontextabhaengigen Score-Schritten.
- `AI_TryToFaint` ist davon getrennt und belohnt KO-/staerkste-Move-Situationen.

Wichtig: NatDex/Vanilla `AI_CheckViability` kann Accuracy-Down zulassen oder in bestimmten Kontexten aufwerten. Es gibt aber keinen source-backed Hinweis, dass der originale Patch Accuracy-Drop-Scoring veraendert oder eine CFRU-aehnliche moderne Positive-Utility-Kampfklassenlogik einfuehrt.

### CFRU

CFRU hat zwei unterschiedliche AI-Flag-Namensraeume:

| Datei | Bits 0-2 |
| --- | --- |
| `include/constants/battle_ai.h:37-39` | Alte/konstante Namen: `CHECK_BAD_MOVE`, `TRY_TO_FAINT`, `CHECK_VIABILITY`. |
| `include/battle.h:523-525` | Runtime-Namen: `CHECK_BAD_MOVE`, `SEMI_SMART`, `CHECK_GOOD_MOVE`. |

`GetAIFlags` und `sBattleAIScriptTable` nutzen die Runtime-Namen aus `include/battle.h`:

- Bit 0 -> `AIScript_Negatives`
- Bit 1 -> `AIScript_SemiSmart`
- Bit 2 -> `AIScript_Positives`

`AIScript_Positives` ruft bei `EFFECT_ACCURACY_DOWN` / `_2` `GoodIdeaToLowerAccuracy(...)` auf. Dieser Helper lehnt Accuracy-Down ab, wenn ein sicherer KO naheliegt oder wenn Ability/Item/Statblocker die Senkung verhindern; sonst kann der Move ueber `INCREASE_STATUS_VIABILITY(1)` aufgewertet werden. `AIScript_SemiSmart` ruft `AIScript_Positives` fuer viele Effekte auf, aber nicht fuer reine `EFFECT_ACCURACY_DOWN` / `_2` in der geprueften Switch-Liste.

Damit ist die lokale v1-Beobachtung source-backed plausibel: v1 aktivierte `AI_SCRIPT_CHECK_GOOD_MOVE`, also `AIScript_Positives`; Sand Attack konnte als gueltiger Accuracy-Drop-Utility-Move aufgewertet werden. v2 entfernt diesen Pfad aus dem Smart-Trainer-AI-Hook.

## Vergleich CFRU v1 / v2

| Variante | Flag-Kombination | Source-backed Bewertung |
| --- | --- | --- |
| NatDex/Ironmon `0x07` | `CHECK_BAD_MOVE | CHECK_VIABILITY | TRY_TO_FAINT` | Trainerdaten-Flag-Upgrade; alte Gen3-Scriptlogik bleibt unveraendert. |
| CFRU v1 | `CHECK_BAD_MOVE | SEMI_SMART | CHECK_GOOD_MOVE` | Numerisch Bits 0-2, aber semantisch nicht gleich: Bit 2 ist `AIScript_Positives`, nicht Gen3 `TRY_TO_FAINT`. |
| CFRU v2 | `CHECK_BAD_MOVE | SEMI_SMART` | Nicht `0x07`-identisch, aber vermeidet den v1-Utility-/Accuracy-Drop-Boost durch `CHECK_GOOD_MOVE`. |

## Ist unser CFRU-Ansatz nahe genug?

Nicht als exakter Smart-AI-Patch-Port.

Was sicher nahe ist:

- separater Trainer-AI-Schalter statt `VAR_GAME_DIFFICULTY`
- keine Trainer-Staerke-, Level-, Wild/Raid-, Bag-, Move-Restriktions- oder Battle-Rule-Nebeneffekte
- Bit-0-Verhalten `CHECK_BAD_MOVE` als klarste gemeinsame Entsprechung

Was nicht sicher verhaltensnah ist:

- CFRU `SEMI_SMART` ist keine 1:1-Entsprechung zu Vanilla/NatDex `CHECK_VIABILITY`.
- CFRU `CHECK_GOOD_MOVE` ist keine 1:1-Entsprechung zu Vanilla/NatDex `TRY_TO_FAINT`.
- CFRU hat moderne Positive-/Utility-/Prediction-/Fighting-Class-Heuristiken, die im originalen Patch nicht geaendert wurden.

## Implementierungsrichtungen

| Option | Naehe zum belegten Patch | Projektbewertung |
| --- | --- | --- |
| a) nur CFRU `CHECK_BAD_MOVE` | Niedrig, aber sicher. | Verhindert schlechte Moves, liefert wahrscheinlich zu wenig "Smart AI". |
| b) CFRU `CHECK_BAD_MOVE | SEMI_SMART` | Mittel als pragmatische CFRU-native v2. | Empfohlen fuer naechsten Smoke, weil `CHECK_GOOD_MOVE`-Utility-Spam vermieden wird. |
| c) echter Vanilla/NatDex `CHECK_VIABILITY` / `TRY_TO_FAINT`-Port | Hoechste Patch-Naehe. | Noetig, wenn "wie Ironmon/NatDex Smart AI" wirklich verhaltensnah gemeint ist. Groesserer Code- und Testaufwand. |
| d) eigener Damage-/KO-orientierter Modus | Nicht originalpatch-nah, aber zielnah fuer Randomizer. | Sinnvoll, wenn das Projekt offensivere Trainer-AI statt historischer Patch-Treue will. Muss klar anders benannt werden. |

## Empfehlung

Fuer den naechsten Implementierungs-/Smoke-Schritt v2 beibehalten: `AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_SEMI_SMART`.

Diese Variante ist nicht als exakter NatDex/Ironmon-`0x07`-Port zu beschreiben, aber sie passt besser zum Projektziel "bessere Trainer-Move-Auswahl ohne Utility-Spam und ohne Difficulty-Nebeneffekte". Falls v2 zu schwach ist, sollte die naechste Entscheidung nicht "CFRU `CHECK_GOOD_MOVE` wieder einschalten" sein, sondern entweder:

- gezielter Port/Nachbau von Vanilla/NatDex `AI_CheckViability` und `AI_TryToFaint`, oder
- ein eigener damage-/KO-orientierter CFRU-Modus mit explizit anderem Ziel als historischer Smart-AI-Patch.

## Offene Punkte

- Der historische IPS/BPS-Patch wurde nicht byteweise analysiert. Source-backed belegt ist der tom-overton-Branch und die NatDex-Randomizer-Integration; Patch-Assets wurden nicht heruntergeladen.
- Es bleibt offen, ob alle Ironmon-Community-Varianten exakt dieselbe `0x07`-Semantik verwenden.
- CFRU-v2 braucht kontrollierte Battle-Smokes mit festen Movesets, um zu pruefen, ob `SEMI_SMART` genug offensive Verbesserung bringt.
- Wenn exakte Patch-Naehe gefordert wird, braucht es einen separaten Source-Port-Designblock fuer klassische `AI_CheckViability` / `AI_TryToFaint`-Semantik in CFRU.
