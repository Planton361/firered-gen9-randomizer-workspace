# DPE Gen9 and CFRU Build Smoke Test

## Datum

2026-05-11

## Toolchain

- DEVKITPRO: /opt/devkitpro
- DEVKITARM: /opt/devkitpro/devkitARM
- arm-none-eabi-gcc: /opt/devkitpro/devkitARM/bin/arm-none-eabi-gcc
- arm-none-eabi-gcc Version: arm-none-eabi-gcc (devkitARM) 15.2.0
- python3: Python 3.14.4
- Zusatztools: `grit`, `wav2agb`, `mid2agb`

## DPE Gen9

- Branch: compat/firered-gen9-randomizer
- Commit: 5906aa4d4904e41393fd9184a16951c961e96263
- Build-Befehl: `python3 scripts/make.py`
- Input: lokale Kopie von `04_private_roms/BPRE0.gba` als `BPRE0.gba` im DPE-Ordner
- Output lokal: `05_builds/dpe-gen9-first-smoke/test.gba`
- Output SHA-256: 53884a8a64a306c592b6b002ec32ed0f1768ac945aae3cfa9da5acbbbe1e26bf
- offsets.ini SHA-256: d1cf98a85c8786898b32171bdea44bbb3d2805ae4e371b8216c4d602ccb1741b

## CFRU-expansion

- Branch: compat/firered-gen9-randomizer
- Commit: 184dc035b44a866980c6c8b58fce864012f0c76b
- Build-Befehl: `python3 scripts/make.py`
- Input: DPE-Output als `BPRE0.gba` im CFRU-Ordner
- Output lokal: `05_builds/cfru-dpe-gen9-first-smoke/test.gba`
- Output SHA-256: 0610ad0850dbc1fecaac1f2898f7a614860a3420db2c7072d11027267db9666c
- offsets.ini SHA-256: 0a4de34650e24165e13e8a2292bc83ed3192f4c7ea999f4fee6ad2a29f92e012

## Build-Fixes / lokale Tooling-Hinweise

- `grit` war installiert, aber `/opt/devkitpro/tools/bin` musste in den fish PATH aufgenommen werden.
- `wav2agb` und `mid2agb` lagen als Windows-EXE in den Repos und wurden ueber lokale ignored Wine-Wrapper unter `03_tools/releases/local-bin/` verfuegbar gemacht.
- CFRU benoetigte einen Fix im Fork: `src/mini_printf.c` wurde angepasst, damit GCC 15 keinen nicht gelinkten builtin/libc-`strlen`-Aufruf erzeugt.
- CFRU-Fix-Commit: 184dc035b44a866980c6c8b58fce864012f0c76b

## Ergebnis

- DPE Build erfolgreich: ja
- CFRU Build erfolgreich: ja
- ROM/Build committed: nein

## Sicherheitsgrenzen

- Private ROM blieb lokal.
- Build-Ergebnisse blieben lokal in `05_builds/`.
- Keine ROMs oder Builds committed.
- devkitPro wurde nur als Toolchain genutzt; kein devkitPro-Source-Code wurde geaendert.
