# 035 - P1 TM/HM-only Diagnose fuer CFRU/DPE Gen9-BPRE

## Kontext

Ziel dieses Diagnoseblocks war, TM/HM-only fuer den getesteten CFRU/DPE Gen9-BPRE-Stand nach dem Move-Data-Reader-Fix read-only zu pruefen. Es wurde kein Fix und keine Codeaenderung vorgenommen.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-tm-hm-only`
- Voraussetzung: UPR-FVX PR #18 gemerged.
- Voraussetzung: Workspace PR #71 gemerged.
- UPR-FVX-Stand: `c71fd75e67f5a839560bbf5de7c6f17317a64bd1`
- Seed: `274269061345323`
- Lokaler Artefaktordner: `05_builds/randomizer-smoke/035_p1_tm_hm_only/` (ignored, nicht committed)
- Keine Aenderungen an `02_external/**`.

## Harness

Der lokale Diagnose-Harness hat den gebauten UPR-FVX-Stand geladen und folgende Werte gesammelt:

- Move-Coverage aus FVX `RomHandler`.
- oeffentliche FVX-TM-/HM-Listen ueber `getTMMoves()` und `getHMMoves()`.
- rohe 128 `u16`-Slots ab dem FVX-`TmMoves`-Offset.
- TM/HM-Kompatibilitaetsmodell ueber `getTMHMCompatibility()`.
- Save-/Log-/Output-/Stacktrace-Ergebnis fuer TM/HM-only Randomizerlaeufe.

## Ausgangsdaten

Move-Daten:

- `moves.total=992`
- `moves.highestLoaded=991`
- `moves.highestLoadedName=PsychicNoise`

FVX-TM/HM-Sicht:

- `romEntry.TmMoves=0x45a5a4`
- `romEntry.PokemonTMHMCompat=0x16002d0`
- `fvx.tmCount=50`
- `fvx.hmCount=8`
- `public.before.tmEntries=50`
- `public.before.hmEntries=8`
- `public.before.invalidTms=0`
- `public.before.invalidHms=0`
- `public.before.tms=[264, 337, 352, 347, 46, 92, 258, 339, 331, 237, 241, 269, 58, 59, 63, 113, 182, 240, 202, 219, 218, 76, 231, 85, 87, 89, 216, 91, 94, 247, 280, 104, 115, 351, 53, 188, 201, 126, 317, 332, 259, 263, 290, 156, 213, 168, 211, 285, 289, 315]`
- `public.before.hms=[15, 19, 57, 70, 148, 249, 127, 291]`

Rohe 128-Slot-Lesung ab FVX-`TmMoves`:

- `raw128.before.slotCount=128`
- `raw128.before.invalidMoves=70`
- `raw128.before.first50` entspricht exakt den 50 FVX-TMs.
- Slots `51..58` entsprechen den klassischen acht HMs aus `public.before.hms`.
- Slots `59..128` sind am FVX-Offset keine plausible Move-Tabelle.
- `raw128.before.hmSlots121to128=[17285, 2066, 27068, 2113, 17553, 2066, 27068, 2113]`

Kompatibilitaet laut FVX:

- `compat.before.species=423`
- `compat.before.flagLength=59`
- `compat.before.totalFlags=24534`
- `compat.before.trueFlags=7749`
- `compat.before.hmFlags=3384`
- `compat.before.trueHmFlags=694`

Bewertung der Ausgangsdaten:

- FVX erkennt fuer diesen ROM-Stand nur das klassische Gen3-Modell `50 TMs + 8 HMs`.
- FVX erkennt kein CFRU/DPE-128-Slot-TM/HM-Modell.
- Das FVX-Kompatibilitaetsmodell ist `boolean[59]`, also 58 Slots plus Nullslot, und liest 8 Bytes pro Species.
- Ein plausibles CFRU/DPE-128-Slot-Kompatibilitaetsmodell waere in diesem Pfad nicht abgebildet.

## Lauf 1: TM moves + TM/HM compatibility

Aktivierte Optionen:

- `tmsMod=RANDOM`
- `tmsHmsCompatibilityMod=RANDOM_PREFER_TYPE`
- `keepFieldMoveTMs=false`
- `tmLevelUpMoveSanity=false`
- `tmsFollowEvolutions=false`

Ergebnis:

- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `outputRomBytes=0`
- `logNonEmpty=false`
- `directLogBytes=0`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`

Fehlerpfad:

```text
java.lang.ArrayIndexOutOfBoundsException: Index 827 out of bounds for length 827
    at com.uprfvx.random.randomizers.TMTutorMoveRandomizer.randomizeTMMoves(TMTutorMoveRandomizer.java:69)
    at com.uprfvx.random.GameRandomizer.maybeRandomizeTMMoves(GameRandomizer.java:465)
    at com.uprfvx.random.GameRandomizer.applyRandomizers(GameRandomizer.java:288)
    at com.uprfvx.random.GameRandomizer.randomize(GameRandomizer.java:205)
```

Einordnung:

- Der Lauf scheitert vor Save, Log und Reload.
- Ursache ist nicht der neue `moves.total=992`-Load selbst, sondern ein nachgelagertes globales Move-Ban-Array im TM-Move-Randomizer.
- `TMTutorMoveRandomizer.randomizeTMMoves()` iteriert den erweiterten Move-Pool bis ID `991`, greift aber auf ein Array der Laenge `827` zu.
- Dadurch ist TM/HM-only nicht P1-supported.

## Lauf 2: TM/HM compatibility-only

Dieser Lauf trennt diagnostisch den Compatibility-Pfad ab, weil Lauf 1 schon vor der Compatibility-Randomization im TM-Move-Pool scheitert.

Aktivierte Optionen:

- `tmsMod=UNCHANGED`
- `tmsHmsCompatibilityMod=RANDOM_PREFER_TYPE`
- `keepFieldMoveTMs=false`
- `tmLevelUpMoveSanity=false`
- `tmsFollowEvolutions=false`

Ergebnis:

- `saveSuccessful=false`
- `logSuccessful=true`
- `outputRomExists=false`
- `outputRomBytes=0`
- `logNonEmpty=false`
- `directLogBytes=0`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`

Fehlerpfad:

```text
java.lang.NullPointerException: Cannot invoke "com.uprfvx.romio.gamedata.Type.equals(Object)" because the return value of "com.uprfvx.romio.gamedata.Species.getPrimaryType(boolean)" is null
    at com.uprfvx.random.randomizers.TMHMTutorCompatibilityRandomizer.getMoveCompatibilityProbability(TMHMTutorCompatibilityRandomizer.java:116)
    at com.uprfvx.random.randomizers.TMHMTutorCompatibilityRandomizer.randomizePokemonMoveCompatibility(TMHMTutorCompatibilityRandomizer.java:73)
    at com.uprfvx.random.randomizers.TMHMTutorCompatibilityRandomizer.randomizeTMHMCompatibility(TMHMTutorCompatibilityRandomizer.java:56)
    at com.uprfvx.random.GameRandomizer.maybeRandomizeTMHMCompatibility(GameRandomizer.java:480)
    at com.uprfvx.random.GameRandomizer.applyRandomizers(GameRandomizer.java:289)
    at com.uprfvx.random.GameRandomizer.randomize(GameRandomizer.java:205)
```

Einordnung:

- Auch der Compatibility-only-Pfad scheitert vor Save, Log und Reload.
- Der Fehler entsteht durch mindestens eine Species mit `null`-Primaertyp im FVX-Kompatibilitaetspool.
- Der Lauf bestaetigt zusaetzlich, dass das klassische FVX-Compatibility-Modell aktuell nicht robust genug fuer den CFRU/DPE-Speciesbestand ist.

## Gesamtbewertung P1-Support

TM/HM-only ist fuer den getesteten CFRU/DPE Gen9-BPRE-Stand nicht P1-supported.

Gruende:

- FVX erkennt nur `50+8`, nicht das in Diagnose 033 modellierte CFRU/DPE-128-Slot-TM/HM-Modell.
- Der TM-Move-Randomizer ist nach `moves.total=992` nicht defensiv gegen Move-IDs oberhalb des alten globalen Ban-Array-Limits.
- Der Compatibility-Randomizer scheitert separat an einer Species mit `null`-Primaertyp.
- Es gibt keinen Save, kein Output-ROM und keinen Reload-Vergleich fuer die aktivierten TM/HM-only-Pfade.

## Antworten auf Diagnosefragen

- Erkennt FVX das CFRU/DPE-128-Slot-Modell? Nein. FVX meldet `tmCount=50`, `hmCount=8` und `compat.flagLength=59`.
- Bleiben Move-IDs innerhalb `moves.total=992`? Die oeffentlichen 50 TMs und 8 HMs sind gueltig. Der erweiterte Randomizer-Pool erreicht aber Move-ID `827+` und triggert ein altes Array-Limit.
- Werden HMs korrekt geschuetzt? Im aktuellen FVX-TM-Move-Pfad werden nur die ersten 50 TMs geschrieben; die oeffentliche HM-Liste bleibt separat. Ein echtes CFRU/DPE-128-Slot-HM-Schutzverhalten ist nicht belegt, weil FVX dieses Modell nicht erkennt.
- Gibt es Bad Egg oder `<unknown>` im Log? Nein, aber die Logs sind leer, weil die Laeufe vor Logging abbrechen.
- Gibt es Unknown-Move-Marker? Nein, aber die Laeufe brechen vor einem sinnvollen Randomizer-Log ab.

## Plausibler minimaler Fixpfad

1. TM-Move-Randomizer defensiv gegen `moves.total=992` machen.

   Die globalen Ban-/Broken-Move-Strukturen duerfen nicht per direktem Indexzugriff auf hohe CFRU/DPE-Move-IDs zugreifen, wenn ihre Laenge kleiner ist als der geladene Move-Pool.

2. CFRU/DPE-TM/HM-Modell separat gaten.

   Fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks muss entschieden werden, ob der getestete ROM-Stand tatsaechlich ein 128-Slot-TM/HM-Modell nutzt und wo die aktive Tabelle liegt. Der aktuelle FVX-Pfad liest nur das klassische `50+8`-Modell.

3. Compatibility-Pool defensiv gegen Null-/Placeholder-Species machen.

   `TMHMTutorCompatibilityRandomizer` darf bei CFRU/DPE-Sonder-/Placeholder-Species mit `null`-Typ nicht abbrechen. Minimal waere ein Skip solcher Species oder ein Gate auf echte, typisierte Species.

4. HM-Schutz explizit fuer das erkannte Modell pruefen.

   Bei klassischem FVX-Modell sind HMs getrennt von den 50 TMs. Bei einem spaeteren CFRU/DPE-128-Slot-Modell muss HM-Slot-Scope separat definiert werden.

5. Keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung im selben Fix.

## Ergebnis

TM/HM-only ist blockiert und braucht einen separaten Fixbranch. Der naechste minimale Fix sollte zuerst den TM-Move-Pool gegen hohe Move-IDs absichern und den Compatibility-Pfad gegen Null-Typ-Species stabilisieren. Das CFRU/DPE-128-Slot-TM/HM-Modell bleibt zusaetzlich ein eigenes, eng gegatetes Tabellenmodellierungsproblem.
