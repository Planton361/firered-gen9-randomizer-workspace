# Workspace Build and Randomizer Integration Plan

## Zweck

Dieses Dokument plant, wie der FireRed-Gen9-Randomizer-Workspace spaeter sauber um private ROM-Basis, GBA-Toolchain, CFRU/DPE-Gen9-Basis und Universal Pokemon Randomizer FVX erweitert wird.

Dieser Arbeitsblock ist nur Planung und Dokumentation:

- keine Installationen
- keine Builds
- keine ROMs lesen, kopieren, aendern oder committen
- keine Saves oder Emulator States anfassen
- keine Tool-Binaries herunterladen oder committen
- keine externen Repos klonen
- keine Forks anlegen
- keine privaten Keys, Tokens, Secrets oder `.env`-Dateien dokumentieren

## Zielzustand

Der Workspace bleibt ein dokumentierter Steuerungs- und Nachweis-Workspace. Er enthaelt Projektstruktur, Planung, Manifeste, Testprotokolle und spaeter kleine, rechtlich unkritische Scripts. Er enthaelt keine ROMs, keine Build-Ergebnisse und keine Tool-Binaries.

### Ordnerrollen

| Ordner | Rolle | Git-Status |
|---|---|---|
| `00_project-control/` | Roadmap und Projektsteuerung | committen |
| `01_docs/` | Projekt-, Setup-, Quellen-, Tool- und Handoff-Dokumentation | committen |
| `02_external/` | spaeter lokale Clone-Ziele fuer externe Repos | Clone-Inhalte nicht committen; nur Manifest/README/Notizen committen |
| `03_tools/` | Tool-Dokumentation und Tool-Notizen | committen |
| `03_tools/releases/` | lokale Tool-Binaries, Releases, JARs, ZIPs | lokal privat/ignored |
| `04_private_roms/` | lokale private ROM-Basis und ggf. lokale Arbeitskopien | lokal privat/ignored |
| `05_builds/` | Build-Ausgaben, gepatchte GBA, Logs mit Pfaden, `offsets.ini`, Zwischenergebnisse | lokal privat/ignored |
| `06_patches/` | nur rechtlich unkritische Patch-Rezepte/Metadaten, falls spaeter freigegeben | committen nur nach Rechts-/Sicherheitspruefung |
| `07_scripts/` | kleine Setup-/Check-Scripts ohne private Pfade oder ROM-Zugriff | committen |
| `08_tests/` | Testplaene und Testprotokolle ohne ROM-Inhalte | committen |

### Was ins Git-Repo darf

- Markdown-Planung und Statusdokumente
- Quellenentscheidungen, Repo-URLs, Branch-Namen und Commit-Hashes
- Tool-Versionen und nicht-private Installationshinweise
- Smoke-Test-Protokolle ohne ROM-Inhalte
- Hash-Pruefanweisungen und Hash-Ergebnisfelder, sofern sie keine ROM-Inhalte enthalten
- kleine Scripts fuer read-only Checks und Sicherheitschecks

### Was lokal privat bleibt

- saubere private Pokemon FeuerRot GBA
- alle ROM-Arbeitskopien, z. B. `BPRE0.gba`
- Saves, Emulator States und Tracker-Laufzeitdaten
- gebaute oder gepatchte GBA-Dateien
- Tool-Binaries, Release-Zips, JARs, Installer und Cache-Dateien
- private absolute Pfade, Tokens, Keys, `.env`-Dateien

## Zielstruktur

```text
firered-gen9-randomizer-workspace/
├── 00_project-control/
│   └── roadmap/
├── 01_docs/
│   ├── setup/
│   ├── quality/
│   └── references/
├── 02_external/
│   ├── upr-fvx/                              # spaeter Clone oder Fork-Clone, nicht als Workspace-Inhalt committen
│   ├── CFRU-expansion/                       # spaeter Shiny-Miner-Kandidat
│   ├── Dynamic-Pokemon-Expansion-Gen-9/      # spaeter Shiny-Miner-Kandidat
│   ├── Complete-Fire-Red-Upgrade/            # spaeter Upstream-Referenz
│   └── Dynamic-Pokemon-Expansion/            # spaeter Upstream-Referenz
├── 03_tools/
│   └── releases/                             # lokal/ignored: JARs, ZIPs, Installer, Tool-Binaries
├── 04_private_roms/                          # lokal/ignored: private ROMs
├── 05_builds/                                # lokal/ignored: Build-Ergebnisse
├── 06_patches/
├── 07_scripts/
└── 08_tests/
```

Wichtig: `02_external/` ist als Arbeitsort fuer spaetere Clone-Ziele gedacht. Der Workspace soll externe Repo-Inhalte nicht vendorisieren. Vor dem ersten Clone sollte ein separater `.gitignore`-/Manifest-Check sicherstellen, dass keine kompletten externen Repo-Inhalte versehentlich im Workspace-Repo landen.

## ROM-Umgang

### Grundsatz

- Keine ROM ins Git-Repo.
- Keine ROM in ChatGPT hochladen.
- Keine ROM lesen, kopieren oder veraendern, solange kein separater ROM-Arbeitsblock freigegeben ist.
- Lokale private FeuerRot-GBA nur unter `04_private_roms/`.
- Build- oder Toolordner duerfen nur lokale Kopien erhalten, wenn ein spaeterer freigegebener Build-Block das verlangt.

### Geplante lokale Benennung

| Zweck | Lokaler Pfad | Git-Status |
|---|---|---|
| unveraenderte private Basis | `04_private_roms/fire_red_clean_bpre0.gba` | ignored/lokal |
| build-erwartete Arbeitskopie | `04_private_roms/BPRE0.gba` oder spaeter repo-spezifisch lokal kopiert | ignored/lokal |
| Hash-Protokoll | `08_tests/rom-hash-check.md` oder entsprechendes Testprotokoll | committen, wenn ohne ROM-Inhalt |

### Hash-Pruefung

Der spaetere ROM-Check dokumentiert nur:

- Dateiname
- lokaler Pfad relativ zum Workspace
- erwarteter Hash-Typ, bevorzugt SHA-256
- lokaler Pruefbefehl
- Ergebnis `passt` / `passt nicht`

Beispiel fuer spaeteren lokalen Check, nicht in diesem Block ausfuehren:

```sh
sha256sum 04_private_roms/fire_red_clean_bpre0.gba
```

Nicht dokumentieren:

- ROM-Inhalte
- ROM-Auszüge
- Base64/Hex-Dumps
- urheberrechtlich geschuetzte Patch-Inhalte
- Download-Quellen fuer ROMs

## devkitPro/devkitARM-Plan

### Spaeter benoetigt

- devkitPro/devkitARM als primaerer GBA-Toolchain-Kandidat
- `arm-none-eabi-gcc` im PATH oder ueber `${DEVKITARM}/bin/`
- Python 3 fuer CFRU/DPE-Build-Scripts
- `make` fuer toolchainnahe Build-Orchestrierung, soweit vom Zielrepo benoetigt

### Nach Installation zu pruefen

Nur in einem separaten Toolchain-Installationsblock:

```sh
command -v arm-none-eabi-gcc
arm-none-eabi-gcc --version
printf '%s\n' "$DEVKITPRO"
printf '%s\n' "$DEVKITARM"
printf '%s\n' "$PATH"
command -v python3 && python3 --version
command -v make && make --version
```

### Relevante Umgebungsvariablen

| Variable | Zweck | Dokumentationsregel |
|---|---|---|
| `DEVKITPRO` | devkitPro-Basisverzeichnis | Wert nur dokumentieren, wenn nicht privat/sensibel |
| `DEVKITARM` | devkitARM-Verzeichnis | Wert nur dokumentieren, wenn nicht privat/sensibel |
| `PATH` | Erreichbarkeit von `${DEVKITARM}/bin/` und Toolchain-Binaries | nur relevante Ausschnitte dokumentieren, keine Secrets |

### Tool-Manifest-Regel

Nach der Installation werden im Tool-Manifest dokumentiert:

- Installationsquelle/Kanal
- Tool-Versionen
- relevante lokale Pfade ohne Secrets
- Check-Befehle und Ergebnis
- ob `arm-none-eabi-gcc`, Python und `make` erreichbar sind
- offene Abweichungen vom Zielrepo-Buildprozess

In diesem Planungsblock wird keine Installation ausgefuehrt.

## Complete FireRed Upgrade + Dynamic Pokemon Expansion Gen9

### Kandidaten

| Rolle | Quelle | Geplanter lokaler Pfad | Erstentscheidung |
|---|---|---|---|
| Hauptbasis CFRU/Gen9 | `Shiny-Miner/CFRU-expansion` | `02_external/CFRU-expansion` | erster Gen9-Kandidat, vor Nutzung Branch/Commit pinnen |
| Hauptbasis DPE/Gen9 | `Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | erster Gen9-Kandidat, vor Nutzung Branch/Commit pinnen |
| Upstream-Referenz CFRU | `Skeli789/Complete-Fire-Red-Upgrade` | `02_external/Complete-Fire-Red-Upgrade` | read-only Referenz, nicht direkt aendern |
| Upstream-Referenz DPE | `Skeli789/Dynamic-Pokemon-Expansion` | `02_external/Dynamic-Pokemon-Expansion` | read-only Referenz, nicht direkt aendern |
| Decomp-/Strukturreferenz | `pret/pokefirered` | `02_external/pokefirered` | nur Referenz, kein Build ohne Freigabe |

### Fork-Strategie

- Zuerst read-only klonen oder Quellen pruefen, keine Forks.
- Fork nur anlegen, wenn lokale Aenderungen am externen Projekt noetig werden.
- Bei Forks gilt: `origin` eigener Fork, `upstream` Originalrepo.
- Jede externe Quelle wird im Tool-Manifest mit Branch und Commit-Hash gepinnt.
- Codex darf externe Repos nur nach separater Freigabe und nur auf Arbeitsbranches aendern.

### Wahrscheinliche Integrationspunkte

- DPE und CFRU muessen in einer kompatiblen Reihenfolge und Version kombiniert werden.
- DPE verweist upstream darauf, dass Complete Fire Red Upgrade nach der Expansion relevant ist; diese Reihenfolge muss fuer den Gen9-Fork verifiziert werden.
- CFRU nutzt Konfiguration in `src/config.h` bzw. repo-spezifischen Config-Dateien; Gen9-Fork-Abweichungen muessen vor Aenderungen gelesen werden.
- Build-Scripts erwarten wahrscheinlich lokale ROM-Dateinamen wie `BPRE0.gba`; diese Dateien bleiben lokal/ignored.
- Offsets, Linker-Scripts und erzeugte Dateien wie `test.gba` oder `offsets.ini` bleiben lokale Build-Artefakte.

### Risiken

- Shiny-Miner-Forks koennen von Skeli789-Upstream abweichen; Branch/Commit-Pinning ist Pflicht.
- Gen9-DPE und CFRU koennen inkompatible Erwartungen an Defines, Offsets oder Datenstrukturen haben.
- ROM-Hack-Kompatibilitaet mit UPR FVX ist nicht garantiert.
- Build-Anleitungen koennen veraltet sein oder Windows-lastige Annahmen enthalten.
- Rechtlich relevante Inhalte duerfen nicht in Patches, Logs oder Tests gelangen.

## Universal Pokemon Randomizer FVX

### Arbeitsmodell

Zwei saubere Pfade sind moeglich:

| Pfad | Zweck | Lokaler Ort | Git-Status |
|---|---|---|---|
| Release/JAR beschaffen | schnellster Start-Smoke-Test | `03_tools/releases/upr-fvx/` | lokal/ignored |
| Source-Repo klonen | reproduzierbarer Build und Code-Referenz | `02_external/upr-fvx` | Clone-Inhalt nicht committen; Manifest pinnt Branch/Commit |

Empfehlung:

1. Zuerst Release/JAR lokal beschaffen und Start-Smoke-Test dokumentieren.
2. Danach Source-Repo klonen und reproduzierbaren Build klaeren, falls JAR-Build fuer Nachvollziehbarkeit oder Anpassungen benoetigt wird.

### Reproduzierbarkeit fuer JAR/Release

Spaeter zu dokumentieren:

- Bezugsweg: Release-URL oder Source-Repo-Commit
- Dateiname des JAR/Release-Artefakts
- SHA-256 des lokalen Artefakts
- Java-Version (`java -version`)
- Startbefehl
- erwartetes Ergebnis: GUI startet oder CLI-Hilfe erscheint

Beispiel fuer spaeteren lokalen Check, nicht in diesem Block ausfuehren:

```sh
java -jar 03_tools/releases/upr-fvx/<upr-fvx>.jar
```

### Java-Anforderungen

- Lokales OpenJDK ist laut Manifest vorhanden, aber konkrete UPR-FVX-Anforderung muss gegen die aktuelle UPR-FVX-Dokumentation geprueft werden.
- Zu klaeren: minimale Java-Version, Gradle-/Buildsystem-Anforderung, Startmodus GUI/CLI, Linux-x86/Linux-ARM-Artefaktwahl.
- Ergebnis gehoert ins Tool-Manifest und in ein Smoke-Test-Protokoll.

### Start-Smoke-Test

Geplantes Protokoll unter `08_tests/upr-fvx-start-smoke-test.md`:

- Toolpfad ohne private absolute Pfade
- Java-Version
- JAR-/Release-Hash
- Startbefehl
- Ergebnis
- Screenshot nur, wenn keine privaten Pfade/ROM-Namen sichtbar sind
- keine ROM laden in diesem Start-Smoke-Test, sofern nicht separat freigegeben

## Spaetere Arbeitspakete

1. `setup/devkitpro-toolchain-install-check`
   - devkitPro/devkitARM installieren oder freigegebenen Installationsweg ausfuehren
   - `arm-none-eabi-gcc`, `DEVKITPRO`, `DEVKITARM`, Python und `make` pruefen
   - Tool-Manifest aktualisieren
   - keine Builds, keine ROMs

2. `analysis/external-source-pinning`
   - externe Quellen read-only klonen oder ueber GitHub pruefen, wenn freigegeben
   - Branches und Commit-Hashes fuer UPR FVX, CFRU/DPE-Gen9 und Referenzen pinnen
   - entscheiden, ob Forks noetig sind
   - keine Aenderungen an externen Repos

3. `randomizer/upr-fvx-start-smoke-test`
   - UPR-FVX-JAR lokal beschaffen oder aus gepinntem Source-Stand bauen, je nach Freigabe
   - Java-Anforderung pruefen
   - Start-Smoke-Test dokumentieren
   - keine ROM laden, sofern nicht separat freigegeben

4. `build/cfru-dpe-source-readiness`
   - CFRU/DPE-Gen9 lokal strukturell pruefen
   - Build-Anforderungen und Konfigurationsdateien dokumentieren
   - keine ROM, kein Build

5. `rom/fire-red-private-hash-check`
   - private FeuerRot-Basis lokal in `04_private_roms/` pruefen
   - Dateiname und SHA-256-Pruefergebnis dokumentieren
   - keine ROM hochladen, keine ROM committen

6. `build/cfru-dpe-first-smoke-build`
   - erst nach Toolchain-, Quellen- und ROM-Freigabe
   - lokale Build-Arbeitskopie verwenden
   - Build-Ergebnis in `05_builds/`, nicht in Git
   - Log ohne ROM-Inhalte in `08_tests/` dokumentieren

7. `randomizer/custom-build-compatibility-smoke-test`
   - gebaute GBA lokal mit UPR FVX testen
   - Randomizer-Bereiche getrennt testen: Wild Encounters, Trainer, Learnsets, Evolutions, Items/Moves/Abilities
   - Ergebnisse in `08_tests/` dokumentieren
   - keine ROMs oder randomized Builds committen

## Checks fuer diesen Planungsblock

Erwartete Abschlusschecks:

```sh
git status --short
git diff --stat
# falls verfuegbar:
07_scripts/bootstrap/check-git-safety.ps1 oder vorhandenes Safety-Check-Fallback
```

Wenn `pwsh` fehlt, wird der PowerShell-basierte Safety-Check als Einschraenkung dokumentiert. Da dieser Block ueber GitHub-API statt lokalem Arbeitsbaum erstellt wurde, muessen lokale `git status`-/Safety-Checks im Nutzer-Workspace oder durch Codex lokal wiederholt werden.

## Definition of Done

- Integrationsplan ist erstellt.
- Statusdokumente sind auf den Planungsblock synchronisiert.
- Tool-Manifest und Quellenindex enthalten die Planungsentscheidung.
- Keine ROMs, Saves, Builds, Tool-Binaries, externen Clones, Forks oder Installationen wurden angefasst.
- PR nach `main` ist erstellt oder der PR-Befehl ist dokumentiert.
