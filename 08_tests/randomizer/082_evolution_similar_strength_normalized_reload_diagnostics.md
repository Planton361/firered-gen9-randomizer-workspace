# 082 - Evolution Similar Strength Normalized Reload Diagnostics

Datum: 2026-05-14

Arbeitsbranch: `test/upr-fvx-cfru-dpe-p1-evolution-similar-strength-normalized-reload`

## Ziel

Dieses Protokoll dokumentiert den einzelnen lokalen Smoke fuer `FVX-TRAIT-018` Evolutions Similar Strength nach Diagnose 081.

Der Smoke prueft nur den `FVX-TRAIT-016` Evolution-Species-Carrier mit Similar Strength. Der Reload-Vergleich ist auf persistierte Gen3-Evolution-Felder normalisiert:

- Evolution-Type.
- ExtraInfo mit Gen3-Item-ID-Normalisierung.
- Ziel-Species per interner `SpeciesSet`-Identitaet.
- `Evolution.forme` wird nicht als Mismatch-Kriterium gewertet.

## Grenzen

Ausgeschlossen bleiben:

- `FVX-TRAIT-019` Evolutions Same Typing.
- Wild- und Trainer-Slices.
- TypeChart / TypeEffectiveness.
- MoveData Write / Update Moves.
- Palette Randomization.
- Items / Field Items / Shops / Pickup / Encounter Held Items.
- Text / Menu.
- Graphics / Sprites.
- Evolution-Methoden-Writer.

Es gab keine Codeaenderung, keinen Fix und keine Aenderung an `02_external/**`. Lokale Smoke-Artefakte blieben ignored unter `05_builds/**`; private Pfade, ROM-Namen, Hashes und Log-Inhalte werden nicht dokumentiert.

## Normalisierte Settings

- Aktive Feature-ID: `FVX-TRAIT-018`.
- Carrier-Writer: `FVX-TRAIT-016` Evolution-Species-Writer.
- Evolutions-Modus: Random Evolutions.
- Similar Strength: aktiv.
- Same Typing: inaktiv.
- Change Impossible Evolutions: inaktiv.
- Make Evolutions Easier: inaktiv.
- Update Moves: inaktiv.
- Wild Held Items: inaktiv.
- Starter Held Items: inaktiv.
- Palette-Modus: unveraendert.
- TypeEffectiveness: unveraendert.
- Race Mode: inaktiv.

## Smoke-Ergebnis

| Metrik | Ergebnis |
|---|---|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| Reload erfolgreich | `true` |
| `normalizedWriteReloadEvolutionMismatches` | `0` |
| `rawWithFormeWriteReloadEvolutionMismatches` | `0` |
| `nonDefaultFormeValuesAfter` | `0` |
| `Bad Egg` | `true`, nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert |
| `<unknown>` | `false` |
| `exceptionClass` | `none` |
| `stacktrace` | `none` |

## Einordnung

Der einzelne `FVX-TRAIT-018` Similar-Strength-Smoke ist im normalisierten Evolution-Reload-Scope stabil. Save, Log, Output-ROM und Reload funktionieren, und der normalisierte Vergleich der persistierten Gen3-Evolution-Felder meldet `0` Mismatches.

Die 070-Meldung `writeReloadEvolutionMismatches=24` wird dadurch als Diagnosevergleichs-/Normalisierungsproblem eingeordnet, nicht als belegter Write-/Reload-Fehler fuer den getesteten Similar-Strength-Scope.

`Bad Egg=true` wird nicht als reiner Freigabebeweis ignoriert, aber nach 055 als vorhandener Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind, `<unknown>=false` ist und der normalisierte Reload-Mismatch-Zaehler `0` bleibt.

## Folge

- `FVX-TRAIT-018` kann fuer diesen engen Similar-Strength-Scope als stabil dokumentiert werden.
- Es ist kein UPR-FVX-Fix fuer diesen konkreten Smoke erforderlich.
- Evolution-Methoden-Writer, weitere Evolution-Suboptionen und `FVX-TRAIT-019` bleiben getrennte Slices und werden aus diesem Ergebnis nicht abgeleitet.
