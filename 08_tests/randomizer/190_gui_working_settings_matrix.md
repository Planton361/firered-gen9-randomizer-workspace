# 190 - GUI Working Settings Matrix

## Scope

Sync merged UPR-FVX PR #88 and PR #89 and record sanitized local GUI Working Settings Matrix evidence after fixes through PR #89.

Codex did not read, copy, change or generate ROMs.

## Synced Pin

- UPR-FVX PR #88: Trainer Class Names is class-text remapping; trainer class id and sprite source remain unchanged.
- UPR-FVX PR #89: CFRU/DPE Extended-BPRE In-Game Trades write internal SpeciesSet identity.
- Workspace submodule `02_external/upr-fvx`: `f3a6d04ff6db8d48468800194e0baffbafb7505c`.

## Working Settings Passed

- Wild Standard/Fallback.
- Trainer Pokemon core.
- Pokemon Movesets -> Random completely.
- Trainer Movesets.
- Trainer Names.
- Field Items basic.
- Pokemon Abilities.
- TM/HM Compatibility.
- TM Moves.
- Move Tutor Moves.
- Move Tutor Compatibility.
- Shop Items, with supported/special shops confirmed.
- Pickup Items, log-confirmed.
- In-Game Trades, with no `NEW GIVEN = ?` observed after PR #89.
- Static Pokemon, with null placeholder entries remaining null.
- Type Effectiveness, with chaos-setting caveat.
- Pokemon Base Statistics, with ability-name log display caveat.
- Move Data Power.
- Move Data Accuracy.
- Move Data PP.
- Move Data Type.
- Move Data Names.
- Evolutions unchanged preserved.
- Swarms disabled via CFRU `SWARM_CHANCE=0`.

## Caveats

- Trainer Class Names works as textlabel remapping only.
- Trainer Class Names can create expected sprite/class visual mismatch because trainer class id and sprite source remain unchanged.
- For a stable visual profile, keep Trainer Class Names off.
- Starter Pokemon player choices randomize, but rival first-battle sync is unresolved/blocked.
- Special-Wild remains out-of-scope.
- Shop Items evidence covers supported/special shops.
- Static Pokemon null placeholder entries remain null.
- Pokemon Base Statistics ability names in the log can appear truncated; ingame names are correct in sanitized evidence.

## Interpretation

- The current normal walkthrough GUI matrix is usable with the documented caveats.
- PR #89 resolves the unacceptable In-Game Trades `NEW GIVEN = ?` symptom for the CFRU/DPE Extended-BPRE path.
- Trainer Class Names should be treated as a text-only option, not a visual class-assignment option.
- Starters and Special-Wild remain separate future blocks.

## Next Recommended Block

- Isolate Starter Pokemon/rival starter sync if Starter Pokemon should enter the stable profile.
- Otherwise repeat a stable visual profile smoke with Trainer Class Names, Starters and Special-Wild disabled.

## Safety Boundary

- No ROM paths.
- No output ROM paths.
- No hashes.
- No screenshots.
- No full logs.
- No saves or emulator states.
- No secrets, tokens or `.env` details.
- No UPR-FVX/CFRU/DPE code changes.
- No P1 promotion.
