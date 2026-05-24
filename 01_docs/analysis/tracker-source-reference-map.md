# Tracker Source Reference Map

## Zweck

Dieses Dokument sammelt die lokalen Source-Referenzen für Ironmon Tracker und NatDexExtension.

BizHawk wird als lokales Tool genutzt, aber nicht als Source-Submodule in `02_external/` eingebunden.

## Eingebundene Quellen

- `02_external/Ironmon-Tracker`
- `02_external/NatDexExtension`

## Lokale Tools außerhalb von Git

- BizHawk wird lokal gestartet.
- Tracker-/BizHawk-Releases, AppImages, ZIPs, Builds und andere Tool-Binaries bleiben außerhalb von Git.

## Erste Analyseziele

- `IronmonTrackerAPI.lua`
- Ironmon-Tracker Lua-Dateien für Memory Reads
- NatDexExtension Entry Points
- NatDexExtension Species-/Moves-/Abilities-/Items-Mapping
- BizHawk-Lua-/Memory-/Scripting-Schnittstelle aus Tracker-Sicht

## Einordnung

- `02_external/` enthält Source-Referenzen.
- NatDexExtension wird auf `dev_new` als Analyse-Vorlage verwendet, nicht als drop-in Lösung für CFRU/DPE/Gen9 angenommen.
- Lokale Lua-Anpassungen für Tests dürfen nicht als Tool-Binary/privater Arbeitsstand ungeprüft committed werden.

## Sicherheitsregeln

Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, Screenshots, raw Logs, Hashes oder privaten Pfade committen.
