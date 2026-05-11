# CFRU DPE Randomized BizHawk Boot Smoke Test

## Datum

2026-05-11

## Zweck

Pruefen, ob die minimal mit UPR-FVX randomisierte CFRU/DPE-Gen9-ROM in BizHawk startet und ein frueher Spielabschnitt spielbar ist.

## ROM

- Pfad: `05_builds/randomizer-smoke/randomizer-smoke.gba`
- SHA-256: dddaf7285a8c72eb32657bc951dd9533bb2b6f5286fcda458903b3dd03ff148b
- committed: nein
- ignored: ja, via `05_builds/`

## Emulator

- BizHawk gestartet: ja
- ROM geladen: ja

## Ergebnis

- Boot bis Title/Intro: ja
- Neues Spiel gestartet: ja
- Starter/Pokemon waehlen: ja
- Rivalenkampf startet: ja
- Rivalenkampf spielbar: ja
- Crash bis dahin: nein

## Einschraenkungen

- Nur minimaler Boot-/Early-Game-Smoke-Test.
- Keine Aussage zu voller Randomizer-Kompatibilitaet.
- Weitere Feature-Tests fuer Wild Encounters, Trainer, Learnsets, Evolutions, Items/TMs/Tutors stehen noch aus.

## Sicherheitsgrenzen

- Keine ROM wurde committed.
- Keine Saves oder Emulator States werden committed.
- Build- und Emulator-Ausgaben bleiben lokal.
