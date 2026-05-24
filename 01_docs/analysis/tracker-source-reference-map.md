# Tracker Source Reference Map

## Zweck

Dieses Dokument sammelt die lokalen Source-Referenzen für Ironmon Tracker und NatDexExtension.

BizHawk wird als lokales Tool genutzt, aber nicht als Source-Submodule in `02_external/` eingebunden.

## Eingebundene Quellen

Arbeitsblock: `setup/tracker-source-references`.

| Quelle | Lokaler Pfad | Branch | Commit | Zweck |
|---|---|---|---|---|
| Ironmon Tracker | `02_external/Ironmon-Tracker` | `main` | `c450ecaee2d8131a2789bb656e3be792a93712fb` | Source-Referenz für Tracker-Lua, BizHawk-/mGBA-Anbindung, Memory Reads und API-Oberfläche |
| NatDexExtension | `02_external/NatDexExtension` | `dev_new` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` | Source-Referenz für Ironmon/NatDex-Erweiterung; Analysevorlage, keine Drop-in-Annahme für CFRU/DPE/Gen9 |

## Lokale Tools außerhalb von Git

- BizHawk wird lokal gestartet.
- Es gibt kein BizHawk-Source-Submodule in `02_external/`.
- Tracker-/BizHawk-Releases, AppImages, ZIPs, Builds und andere Tool-Binaries bleiben außerhalb von Git.

## Erste Analyseziele

| Bereich | Datei | Relevanz |
|---|---|---|
| Tracker API | `02_external/Ironmon-Tracker/ironmon_tracker/TrackerAPI.lua` | Zentrale Tracker-API-Analysequelle; im Projektkontext als `IronmonTrackerAPI.lua` referenziert. Exportiert `TrackerAPI` und bietet Zugriff auf Spieler-/Gegner-Pokémon, Battle-State, Trainerdaten, Bag-Items, Moves, Abilities, Types und Battle Outcome. |
| Tracker Memory | `02_external/Ironmon-Tracker/ironmon_tracker/Memory.lua` | Memory-Read-/Write-Abstraktion aus Tracker-Sicht; später gegen CFRU/DPE-RAM-Layout prüfen. |
| Tracker Settings | `02_external/Ironmon-Tracker/ironmon_tracker/GameSettings.lua` | ROM-/Game-Erkennung und Tracker-Konfiguration; wichtig für FireRed-/Hack-Kompatibilität. |
| Tracker Daten | `02_external/Ironmon-Tracker/ironmon_tracker/data/PokemonData.lua`, `MoveData.lua`, `AbilityData.lua`, `TrainerData.lua` | Tabellen- und ID-Modell des Trackers für Species, Moves, Abilities und Trainer. |
| NatDexExtension Einstieg | `02_external/NatDexExtension/NatDexExtension.lua` | Erweiterungs-Einstieg; `dev_new` prüft u. a. eine NatDex-ROM-Signatur über `monCountAddress` und überschreibt Tracker-Funktionen für NatDex-Daten. |
| NatDexExtension Daten | `02_external/NatDexExtension/` | Vorlage für Species-/Move-/Ability-/Item-Mapping und Tracker-Erweiterung, aber CyanSMP64-spezifisch. |

## Einordnung

- `02_external/` enthält Source-Referenzen.
- NatDexExtension wird auf `dev_new` als Analyse-Vorlage verwendet, nicht als Drop-in-Lösung für CFRU/DPE/Gen9 angenommen.
- BizHawk bleibt ein lokales Toolziel für spätere Tracker-Smokes. Es wird nicht als Source-Submodule eingebunden und keine BizHawk-Binaries werden committed.
- Lokale Lua-Anpassungen für Tests dürfen nicht als Tool-Binary/privater Arbeitsstand ungeprüft committed werden.

## Sicherheitsregeln

Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, Screenshots, raw Logs, Hashes oder privaten Pfade committen.
