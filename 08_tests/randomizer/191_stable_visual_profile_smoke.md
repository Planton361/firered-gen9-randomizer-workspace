# 191 - Stable Visual Profile Smoke

## Scope

Record sanitized local Stable Visual Profile smoke evidence after the merged GUI Working Settings Matrix baseline.

Codex did not read, copy, change or generate ROMs.

## Stable Visual Profile

ON:

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
- Shop Items.
- Pickup Items.
- In-Game Trades.
- Static Pokemon.
- Type Effectiveness.
- Pokemon Base Statistics.
- Move Data Power.
- Move Data Accuracy.
- Move Data PP.
- Move Data Type.
- Move Data Names.

OFF:

- Starter Pokemon.
- Trainer Class Names.
- Evolution Randomization.
- Special-Wild / Day-Night / Swarms.

## Sanitized Evidence

- Randomization completed: yes.
- Output ROM booted: yes.
- Short run played: yes.
- Wild encounters worked: yes.
- Trainer battle worked: yes.
- Items/shops/moves/abilities showed blockers during the short run: no.
- Evolutions unchanged remain expected: yes.
- Missing sprites observed: no.
- Move-less Pokemon observed: no.
- Crash observed: no.
- Freeze observed: no.
- Softlock observed: no.

## Caveats

- This is a short smoke, not a full playthrough.
- Starter/Rival sync remains unresolved and Starter Pokemon stays off.
- Trainer Class Names remains off because class-text remapping can visually mismatch trainer sprites/class ids.
- Special-Wild remains out-of-scope; Day/Night and Swarms stay disabled.
- No P1 promotion is made from this smoke.

## Next Recommended Block

- Isolate Starter Pokemon/rival first-battle sync if Starter Pokemon should enter the stable profile.
- Otherwise continue longer local sampling with the same Stable Visual Profile.

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
