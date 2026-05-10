# Linux GBA Toolchain Plan

## Zweck

Dieses Dokument plant das weitere devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen auf Linux/CachyOS.

Dieser Arbeitsblock ist Planungs- und Dokumentationsarbeit:

- keine Installationen
- keine Builds
- keine ROMs, Saves, Emulator States oder Builds anfassen
- keine Tool-Binaries anfassen oder committen
- keine externen Repos klonen
- keine Forks anlegen

## Ausgangsstand

Aus `01_docs/references/tool-manifest.md` und der Linux/CachyOS-Inventur:

| Punkt | Stand |
|---|---|
| Linux/CachyOS | primaere lokale Umgebung |
| Git | vorhanden |
| GitHub CLI | vorhanden und authentifiziert |
| Java | vorhanden: OpenJDK 26.0.1 |
| `make` | vorhanden: GNU Make 4.4.1 |
| devkitPro/devkitARM | nicht nachgewiesen |
| `arm-none-eabi-gcc` | nicht im PATH gefunden |
| `agbcc` | nicht im PATH gefunden; optional |
| `pwsh` | nicht im PATH gefunden; Safety-Check daher nicht direkt ausfuehrbar |

Windows-Toolchain-Befunde bleiben historisch und duerfen nicht als Linux-Ist-Stand verwendet werden.

## Dokumentierte Quellenbasis

Aktuell im Quellenindex dokumentiert:

| Quelle | Relevanz fuer Toolchain |
|---|---|
| devkitPro/devkitARM | GBA-Build-Toolchain; erst lokal pruefen, keine Installation in diesem Block |
| Skeli789 CFRU/DPE | spaetere Build-Referenz; Build erfordert lokale ROM und Toolchain |
| pret/pokefirered | Decomp-/Build-Referenz; Builds erst spaeter |
| UPR FVX Docs | relevant fuer Java/Randomizer-Smoke-Tests, nicht fuer GBA-Cross-Compiler |

Vor einer Installation oder einem Build muessen konkrete Anforderungen aus den spaeter ausgewaehlten Basis-Repos und offiziellen Toolchain-Dokumenten geprueft und dokumentiert werden.

## Optionen

### Option A: devkitPro/devkitARM als primaere GBA-Toolchain

Ziel: Die fuer GBA-Hacks uebliche devkitPro/devkitARM-Toolchain als primaere Build-Toolchain verwenden.

Vorteile:

- passt zum dokumentierten devkitPro/devkitARM-Ziel im Quellenindex
- erwartbar kompatibel mit vielen GBA-Hack- und Decomp-Buildfluesse
- `arm-none-eabi-gcc` waere Bestandteil bzw. erreichbar, wenn die Toolchain korrekt eingerichtet ist

Offene Entscheidungspunkte:

- offizielle Linux/CachyOS-/Arch-nahe Installationsmethode vor Installation dokumentieren
- erwartete Umgebungsvariablen und PATH-Eintraege klaeren
- Klaeren, ob spaetere CFRU/DPE-Basis devkitARM direkt voraussetzt
- Klaeren, ob lokale Pakete oder devkitPro-eigene Paketquelle genutzt werden sollen

Risiken:

- Installation veraendert das lokale System und braucht separaten freigegebenen Arbeitsblock
- falsche PATH-/Umgebungsvariablen koennen spaetere Build-Fehler verdecken
- keine Builds ohne ROM-/Build-Freigabe

### Option B: Distribution-/Systempaket fuer `arm-none-eabi-gcc`

Ziel: Nur den Cross-Compiler ueber Linux/CachyOS-/Arch-nahe Paketquellen bereitstellen.

Vorteile:

- moeglicherweise kleinerer Setup-Umfang
- `arm-none-eabi-gcc` koennte fuer einfache Checks reichen

Offene Entscheidungspunkte:

- Kompatibilitaet mit devkitARM-erwartenden Buildsystemen pruefen
- Version und Binutils-/newlib-Kombination gegen Ziel-Repos pruefen
- Klaeren, ob devkitPro-spezifische Tools trotzdem benoetigt werden

Risiken:

- kann von devkitPro/devkitARM-Erwartungen abweichen
- spaetere CFRU/DPE- oder pret-Builds koennten andere Toolchain-Versionen erwarten

### Option C: Toolchain-Setup bis nach Repo-Pinning verschieben

Ziel: Erst die konkrete FireRed-/CFRU-/DPE-Basis festlegen und danach die dazu passende Toolchain installieren.

Vorteile:

- reduziert Risiko einer unpassenden Toolchain
- Anforderungen koennen aus gepinnten Repos statt aus Vermutungen abgeleitet werden

Offene Entscheidungspunkte:

- welche Basis-Repos zuerst read-only genauer geprueft werden sollen
- ob Toolchain-Installation vor oder nach erstem lokalen Clone geplant wird

Risiken:

- Build-Readiness verschiebt sich
- ohne Toolchain bleiben Build-Checks blockiert

## Empfohlene Richtung

Primaere Richtung: Option A vorbereiten, aber noch nicht ausfuehren.

Begruendung:

- Das Projektziel ist GBA/FireRed-nahe ROM-Hack-Arbeit.
- devkitPro/devkitARM ist bereits als Toolchain-Ziel im Quellenindex dokumentiert.
- `arm-none-eabi-gcc` fehlt aktuell und sollte im Kontext der Ziel-Toolchain geloest werden, nicht isoliert.

Option B bleibt nur Fallback, falls offizielle oder projektkompatible devkitPro/devkitARM-Nutzung auf Linux/CachyOS nicht praktikabel ist.

Option C gilt fuer Build-Details: konkrete Build-Befehle und ROM-nahe Schritte bleiben bis nach Repo-Pinning und separater Freigabe gesperrt.

## Entscheidungspunkte vor Installation

Vor einem Installationsblock muessen dokumentiert sein:

1. Welche offizielle devkitPro/devkitARM-Installationsquelle fuer Linux/CachyOS genutzt werden soll.
2. Welche Pakete oder Komponenten benoetigt werden.
3. Welche Umgebungsvariablen erwartet werden, insbesondere `DEVKITPRO`, `DEVKITARM` und PATH.
4. Wie `arm-none-eabi-gcc --version` nach Installation read-only geprueft wird.
5. Ob `agbcc` fuer den geplanten Buildpfad wirklich benoetigt wird oder optional bleibt.
6. Welche Pfade nicht in Git gelangen duerfen.
7. Welche Build-Schritte weiterhin verboten bleiben, bis ROM- und Build-Freigabe separat erfolgt.

## Naechster konkreter Schritt

Naechster Branch: `setup/linux-gba-toolchain-source-review`.

Ziel dieses Folgeblocks:

- offizielle devkitPro/devkitARM-Dokumentation und die dokumentierten Ziel-Repos read-only auf Toolchain-Anforderungen pruefen
- keine Installation ausfuehren
- keine Builds starten
- keine externen Repos klonen
- daraus einen konkreten Installations-/Pruefplan fuer Linux/CachyOS ableiten

## Weiterhin gesperrt

- ROMs lesen, kopieren, aendern oder committen
- Saves oder Emulator States anfassen
- Builds starten oder committen
- Tool-Binaries anfassen oder committen
- externe Repos klonen
- Forks anlegen
- Installationen durchfuehren
- direkt auf `main` arbeiten
- PRs mergen
