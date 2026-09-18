# Final Gen1–9 source-data reconciliation

Date: 2026-09-15. Result: one bounded DATA_BUG repaired in a draft candidate;
final authoritative modernization parity is **UNKNOWN**, not certified complete.
No ROM, save, state, private output or new upstream dataset was accessed.

## Exact scope and reproducible evidence

Workspace `7437cd551545ab5e4dcd57a2ff5dbf9672193d74` pins DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` and CFRU
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`. The audit reads revision-qualified
Git objects, never the original dirty checkouts. DPE owns Base Stats and ability
assignments; CFRU owns active level-up learnsets and contextual ability names.
At the DPE pin, `EXPAND_LEARNSETS` is disabled. Comparing its dormant table as
if it were the runtime table would give a false reconciliation result.

Run from this documentation branch, pointing to a source workspace with the
pinned Git history (no submodule checkout or protected artifact required):

```sh
python3 07_scripts/data_audit/reconcile_pinned_pilot.py --source-workspace /path/to/workspace --output /tmp/pilot-source.json
python3 07_scripts/data_audit/reconcile_pinned_pilot.py --source-workspace /path/to/workspace --cfru-ref 5ea11537ef0def6a718d007ce5f4a765f6585205 --output /tmp/pilot-candidate.json
```

[Baseline inventory](gen1-9-source-reconciliation.json) and
[candidate inventory](gen1-9-candidate-reconciliation.json) record each
cross-component learnset difference, aliases, invalid dormant references,
generation coverage and numeric bounds. These are source inventories, not a
comparison against an unrecorded external authority.

## Findings and classification

| Area / discrepancy | Classification | Evidence and disposition |
|---|---|---|
| Pikachu, Rotom, Necrozma, Zacian, Zamazenta active tables contain only END | DATA_BUG | Five empty named tables serve 31 species/form pointers. Restore only these blocks from tracked pre-sync CFRU `53273184bab06f91cdc3ad6e0e5af4a8ba41591a`; all pointers and other tables unchanged. |
| Base Stats encoding | No detected encoding DATA_BUG | 1,412 explicit rows spanning IDs 0..1439. All six stats on real rows fit 1..255; this validates representation, not every modern numeric value. |
| Egg's six zero stats | OUT_OF_SCOPE | Sentinel, not a playable species requiring modern base stats. |
| Ability assignments | No detected encoding DATA_BUG | 4,233 slots resolve within 0..254. No assignment uses a DPE-only macro; shared CFRU/DPE ability constants have zero drift. |
| 33 shared ability macro aliases | INTENTIONAL_ALIAS | Full list in JSON. IDs deliberately reuse existing CFRU semantics; names alone do not confer new battle effects. Preserve species-context checks. |
| Contextual / shortened ability names | INTENTIONAL_ALIAS | 328 indexed/dynamic labels; maximum name width 16 plus FF terminator. No overlength labels. `GetAbilityNameOverride` selects species-specific names; shared IDs cannot be assigned a single universal Gen9 meaning. |
| Commander, Hospitality, Embody Aspect absent; Palafin and Terapagos mechanics partial | ENGINE_LIMITATION | M-010's accepted engine boundary. Do not implement transformations, triggers or new battle effects as a data correction. |
| Inactive DPE vs active CFRU learnsets | OUT_OF_SCOPE | Baseline 38 differing pointer rows / 15 invalid dormant references; candidate 69 differences because 31 shared active rows are restored. Dormant undefined names (including TERASTORM / DIALGA_PRIMAL) are not active-pilot breakage. Do not enable DPE learnset expansion. |
| Active CFRU move/level encoding | No detected encoding DATA_BUG after restoration | 1,105 blocks / 1,414 pointers; max 34 moves. All parsed active entries have levels 0..100 and defined nonzero move IDs below 992. Shared move constants have zero drift. |
| Exact current authoritative values for stats, assignments, learnsets and names | UNKNOWN | Approved Showdown aliases and synchronization scripts are tracked, but raw pokedex.ts / learnsets.ts / abilities.ts and a reproducible authoritative input snapshot are not. Historical zero-drift reports cannot certify the present source; indeed they missed the empty tables. |
| All missing modern mechanics beyond baseline | OUT_OF_SCOPE | CFRU/DPE remain the engine baseline. No DPE or battle implementation is included. |

Before repair, National Dex coverage with both a base row and nonempty active
learnset was 150/151, 100/100, 135/135, 106/107, 156/156, 72/72, 87/88,
94/96, 120/120 across Generations 1–9. The candidate reaches all **1,025 / 1,025**
National Dex identities under this structural check. This is not a promise
that every form is encounter-safe, or that every move matches the latest games.

## Candidate and tests

[CFRU draft #46](https://github.com/Planton361/CFRU-expansion/pull/46), exact
candidate `5ea11537ef0def6a718d007ce5f4a765f6585205`, is stacked on M-013
`d8468e1d12dbe33f646e2778bbde51ece7010a73` to preserve both bounded M-009
source-guard extensions. User merge order: #45 first, then retarget/rebase #46
to the compatibility branch and review its five-block diff. Nothing is merged.

PASS: exact tracked-source restoration check (31 pointers), active-source
inventory for baseline and candidate, ARM syntax check on the learnset unit,
M-009 source/eight negative/host checks, inherited M-013 host regression,
`git diff --check`, workspace Git safety before/after.

Clean/full CFRU build was attempted in a fresh worktree. C, assembly, strings
and image stages completed; audio stopped on missing `wav2agb` (`mid2agb` also
absent). Full link/build is not passed. No tool binary was fetched/requested.

Runtime gate: five base species plus safely reachable shared-form representatives,
starting moves, later learning boundary, summary/PC display, save/reload and
randomized learnset/pool smoke. Candidate source documentation contains the
exact bounded matrix. Do not force unsupported transformations.

## Remaining decision

No DPE change is required for the discovered active-pilot bug. Restoring lost
tracked data is reviewable now, but declaring all modernization complete still
requires a separately approved, reproducible authoritative dataset comparison
or an explicit documented acceptance of the historical baseline and UNKNOWN
items. Do not silently relabel that uncertainty as PASS or add engine mechanics.
