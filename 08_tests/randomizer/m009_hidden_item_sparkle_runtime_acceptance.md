# M-009 — sanitized targeted Hidden Item Sparkle acceptance

**Classification:** CONFIRMED CURRENT STATE, with targeted runtime caveat.

**Result:** `PASS_TARGETED_VISIBLE_SPARKLE_WITH_CAVEATS`

**Evidence source:** user-supplied targeted runtime observation and visual
acceptance in the M-009 workspace closure request. This is not a new automated
test or an independently repeated agent runtime observation.

## Exact tested revision

Runtime-tested / user-accepted CFRU candidate:
`3da0547d782fb62fc993431278d63575912025da`.

Supported statement: **Hidden Item sparkle behavior was observed in runtime
and visually judged appropriate on the exact candidate.**

## Integrated revision

CFRU PR #43 integrated merge:
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`.

Verified Git relationship: the merge is exactly one commit ahead of the
candidate, the candidate is the merge base, and there are no additional file
changes from candidate to merge. **The merge revision was not separately
runtime-tested.** The workspace pins that integrated merge, not the candidate.

## Limits and later gate

The supplied evidence does not enumerate individual maps/items, an emulator
or version, or a complete test matrix. None is inferred here. In particular,
this result does not establish separate runtime coverage of every Start,
Bag, Party, Quest Log, resource-pressure or lifecycle permutation.

Broader global-frame regression testing belongs to the **later feature-complete
playthrough gate**, including menu entry/return, transitions and warps,
save/reload, pickup and transient expiry, multiple effects, resource pressure,
Quest Log/fades and interactions with the previously integrated milestones.
These are pending broader checks, not reported failures and not invented PASS
results. No broad release/support, target-emulator, Tracker or randomizer
compatibility claim follows from this targeted acceptance.

Prior failed sparkle pilots remain **LEGACY / OBSOLETE** evidence. Their
historical failures and reverts are retained without rewriting them as passes.
The bounded source-owned solution is recorded in
[M-009](../../docs/milestones/M-009.md).

No ROM, save, emulator state, build, screenshot, raw log, generated offset file,
private path or secret was requested, inspected or attached for this record.
