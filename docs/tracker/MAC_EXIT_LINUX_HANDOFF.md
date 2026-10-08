# Mac exit review and Linux receiving handoff — #715

Contract: [#715](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/715).
Reviewed on macOS, 2026-10-08, in a fresh session with one writing agent on
`docs/mac-exit-linux-handoff`. Scope is **DOC_ONLY**: this document is a
revision-bound review, not a second runbook or an operational status database.

**CONFIRMED CURRENT STATE:** accepted Mac source/mock preparation is integrated;
no material safety/procedure defect was found in the accepted B1 runbook.
**Decision:** submit the Mac exit evidence for CONTROL review and user merge.
Mac exit acceptance remains **INTENDED FUTURE STATE** until CONTROL verifies
that merge. Linux execution is **STOP / PENDING_LINUX_HOST**, not an observed
emulator failure. Preserve `production=DENIED`, `liveConfidence=UNKNOWN` and
`BIZHAWK_LOCKED_PILOT_READY = NOT_RUN`.

## Authority and revision split

Read [AGENTS.md](../../AGENTS.md), then [PROJECT](../PROJECT.md),
[ENGINEERING_RULES](../ENGINEERING_RULES.md), [ENVIRONMENT](../ENVIRONMENT.md),
[REPRODUCIBILITY](../REPRODUCIBILITY.md), [ROADMAP](../ROADMAP.md) and
[MODEL_POLICY](../MODEL_POLICY.md). Current Issue contracts and their accepted
CONTROL evidence establish the later product lock and phase dispositions;
older pending-state/pin statements in general docs are historical for those
facts. [Tracker README](README.md) and [PROFILE_CONTRACT](PROFILE_CONTRACT.md)
define source/trust boundaries; historical Session State is not a contract.
GitHub [Project 4](https://github.com/users/Planton361/projects/4) owns order and
status; PRs record revisions/evidence.

| Revision role | Verified commit | Verified tree |
| --- | --- | --- |
| Latest accepted Mac preparation `origin/main` at entry | `9b17c8f5995f05ac329af9e35db8552899dcca20` | `7506bd5c1b5aee6cbed39a8034f85aad6a614d96` |
| Separately accepted product/output lock | `3bdfe9919afc0b7bea55c79f37285e832be495c3` | `f6bc65355811d7de153a91091b223fec9b50991e` |

The live remote main ref, freshly fetched commit/tree and local Git tree agree.
The #715 PR identifies this document's head/tree separately: neither it nor a
later merge SHA replaces the tested product/output basis. All ten Gitlinks
below match both trees; all ten physical checkouts match and are tracked-clean.

| Gitlink path | Exact unchanged commit |
| --- | --- |
| `02_external/CFRU-expansion` | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |
| `02_external/upr-fvx` | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |

Tracker is the standard v9.3.1 reference; NatDexExtension is a pattern reference,
not a compatible marker/address layout. No component repin or private artifact
transfer follows from this handoff.

The complete 144-item Project entry inventory contained no competing OPEN
Doing contract. #715 was present with Status/Priority/Work Type unset; only
#715 was synchronized to actual existing options `Doing / P0 / Verification`.
Missing optional metadata was nonblocking. OPEN #499/#691/#692 still showed
Project `Done`; #500/#501 showed `Backlog`, and #689/#693/#694/#695 had unset
fields. These administrative discrepancies do not prove runtime acceptance:
their live Issues/CONTROL dispositions keep the host gates OPEN. No other
Project item was changed; CONTROL owns their reconciliation.

## Accepted evidence and its limits

**CONFIRMED CURRENT STATE:** [#497 acceptance](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/497#issuecomment-5752185784)
is completed `HANDOFF_READY`; future Linux `TASK_TOOLCHAIN_READY` is UNKNOWN.
[#498 acceptance](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/498#issuecomment-6044186528)
locks ROM/UPR-FVX Control, Casual NatDex and IronMON NatDex within the recorded
profile/exclusions. Missing separate fixed-seed Gen9/regional witnesses and
incomplete individual IM01–IM05 coverage are accepted residual limitations,
not additional PASS assertions. BizHawk/Tracker and #501 were not accepted.

T0/T1 [#688](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/688),
[#690](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/690)
and [#699](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/699)
provide accepted source architecture/profile/lock repair. Mac Phase A under
#691–#694 provides source/Lua 5.4 synthetic guard, party/battle decoder and
detached UI projection evidence, not live Phase B acceptance. [#705](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/705)
is assurance evidence, not a runtime promotion.

The accepted post-merge evidence for [#707 characterization](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/707#issuecomment-6059523556),
[#709 early interposer](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/709#issuecomment-6060633515),
[#711 field bridge](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/711#issuecomment-6061579393)
and [#713 notes quarantine](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/713#issuecomment-6062362948)
is **TEST_ONLY**. Original pinned getter/accessor bodies were exercised in
isolated synthetic oracles with declared stubs and safety traps. Stock hazards
were characterized; no normal Tracker consumer was installed. The modules stay
detached from production. #713's positive move observation proves an equipped,
matching synthetic move identity, not that an attack was actually used.
Reported local suite PASS was CONTROL source-reviewed and merge-verified;
CONTROL did not rerun interpreters and no independent GitHub CI was provided.
This DOC_ONLY review does not rerun or upgrade those suites.

## Existing B1 runbook review

Use only [B1_LINUX_RUNBOOK.md](B1_LINUX_RUNBOOK.md), accepted by
[#689 post-merge review](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/689#issuecomment-6049854525)
through PR #704. Its source commit is
`2c17d3793d7abd17a4483c3fc7df37dc4edd4679`; accepted merge is
`89f83c914d430f20a304e67be76483c02c8b67c8`; reviewed blob at entry is
`3ab91faa5e690833c554057f53df3985e34568a0`. Its preparation SHA `64f3bbb...`
is intentionally historical. Record the revision actually used for Linux
testing separately; do not relabel the runbook's old preparation as current.

| Review area | Source check and conclusion |
| --- | --- |
| B1-01–06 completeness | Covers #689 boot/new game, input, ordinary save/reload, wild/trainer battles and audio/video/timing/control; scripts/Tracker unloaded. No Tracker-data or broad performance PASS follows. |
| B1-07 host expectations | Pinned [README](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/README.md) requires BizHawk >=2.8, recommends >=2.9 on Linux and identifies Lua 5.1/5.4 expectations. The recommendation is not a mandatory accepted build. Exact host/core/backend/settings remain UNKNOWN. |
| B1-08 cadence/lifecycle | Pinned [Main.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Main.lua), [Program.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Program.lua) and [CustomCode.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/CustomCode.lua) support frameadvance, per-frame/30-frame cadence and exit/console-close seams. The probe models cadence, not original Tracker hooks. Every lifecycle subcase requires actual observation; registration or an invisible close marker is NOT_RUN. |
| B1-09 read boundary | Pinned [Memory.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Memory.lua) uses explicit domain-relative reads. Runbook requires domain membership before size, immutable public safe-RAM proof, width/range/alignment and context predicate; supplies no numeric candidate. Missing proof is NOT_RUN / SAFE_RAM_UNPROVEN. |
| Write prevention | Pinned `Program.changeGameSettingForLR` calls `Memory.writebyte`. Later Tracker use must disable **Override Button Mode to LR** and exclude all other write helpers; B1 starts with Tracker/extensions/other scripts unloaded, cheats/freezes disabled. No memory write is authorized. |
| Evidence/STOP form | Existing sanitized blank form includes host/build/core/Lua/settings/profile/runbook/proof fields, all nine NOT_RUN cases and severity/STOP decisions. No required missing case may inherit PASS. It is the sole B1 results form. |

The public [BizHawk Lua API reference](https://tasvideos.org/Bizhawk/LuaFunctions)
was checked for read-domain and lifecycle signatures; it also documents that a
missing domain name can make size lookup return the current domain's size.
The runbook's membership check therefore matters. This evolving reference
does not prove behavior on the future selected host: use that host's Help as
the runbook requires. Review result is **PASS_SOURCE_REVIEW**, not host PASS.
No material CONFLICT was found. A later material defect requires STOP and a
bounded runbook-repair disposition from CONTROL; do not edit that runbook or
declare Mac exit accepted while such a conflict remains.

## Linux receiving checklist — source only

After user-confirmed Linux availability, CONTROL supplies the exact accepted
#715 merge/checkpoint SHA and tree and routes existing #689. Reconstruct from
GitHub and these sources in a fresh session with one writer. The entry SHA
above is historical after merge; never demand it as the new `origin/main`.

1. Inspect repository identity, branch and status before changing anything.
   Do not overwrite unexpected local changes or reuse an unrelated branch.
   The known Mac `CASUAL_NATDEX.rnqs` was unread/untouched/unstaged; it is not a
   transfer artifact or a required Linux file. Transfer public source via GitHub.
2. Fetch GitHub, compare live `origin/main` SHA/tree with CONTROL's accepted
   receiving revision, and confirm this document/runbook blobs. For an existing
   approved same-contract branch, accept movement only with fast-forward-only
   integration; a new writing task uses its approved non-main branch. Never
   commit/push/merge on main or merge a PR. STOP on unexpected remote movement.
3. Check all ten Gitlinks against this table and the product-lock tree, recursive
   submodule status, every physical HEAD and tracked component cleanliness.
   Uninitialized/mismatched/dirty components block receiving GO; any source-only
   synchronization needs the routed contract and must not overwrite changes.
4. Run Git safety before work and handoff. On main only the explicit read-only
   exception is permitted. These POSIX checks inspect source/Git metadata only:

   ```sh
   git fetch origin
   git status --short
   git branch --show-current
   git rev-parse origin/main 'origin/main^{tree}'
   git ls-tree -r origin/main | awk '$1 == "160000"'
   git ls-tree -r 3bdfe9919afc0b7bea55c79f37285e832be495c3 | awk '$1 == "160000"'
   git submodule status --recursive
   git submodule foreach --recursive 'git rev-parse HEAD; git status --short --untracked-files=no'
   python3 07_scripts/bootstrap/check_git_safety.py --allow-main
   ```

   On the approved non-main writing branch, run the safety command without
   `--allow-main`. No installs, binary inspection, build or runtime occurs in
   this source receiving checklist or #715.
5. User-owned later preflight records sanitized **fields**, presently UNKNOWN:
   OS/distribution/release/architecture; actual BizHawk version/build; GBA
   core/version; selected Lua backend/interpreter setting and `_VERSION`;
   throttle/audio/video/input/focus settings; selected output variant, public
   profile/schema/configuration and local binding proof method/result. No
   particular backend switch or exact package version is assumed.

## Required Linux gate order and unresolved blockers

This is the binding dependency order, not a new queue. CONTROL routes from
Project/Issues; each materially new stage requires a fresh bounded approved
Issue/branch/session. Existing repair of the same contract/branch may resume.

| Ordered contract | Remaining evidence / present disposition | GO condition |
| --- | --- | --- |
| [#689](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/689) / [#499](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/499) — B1 | Host/build/core/Lua/settings UNKNOWN; B1-01–09 and BIZHAWK_LOCKED_PILOT_READY NOT_RUN; SAFE_RAM_UNPROVEN. Tracker unloaded. | Accepted exact identity/configuration and every required runbook case/subcase PASS, no unresolved material defect; CONTROL accepts B1/#499. |
| [#691](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/691) — T2 | Real output/session trust, safe address/layout binding, early loader/import/read-back, wrapper/restart ownership and reset/reload/unload lifecycle UNKNOWN / NOT_RUN. | After accepted B1, separately accepted live fail-closed activation and zero-write proof. B1 alone grants no production activation. |
| [#692](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/692) — T3 | Actual multi-slot party/species/form/move/item/HP/status fidelity, effective randomized assignments/types/stats, contextual ability names and move power/category/maxPP UNKNOWN / NOT_RUN. | Accepted T2 then real per-field/profile fidelity; no baseline or stock fallback. |
| [#693](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/693) — T4 | Live enemy/active precedence, u16 battler-slot mapping, trainer A/B ownership, wild/trainer transitions, double/multi scope and true attack-event observation UNKNOWN / NOT_RUN. | Accepted T3 then revision-bound battle/context/epoch evidence; unsupported contexts remain explicit. |
| [#694](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/694) — T5 | Normal TrackerAPI/TrackerScreen/DataHelper/BattleDetails consumers, sprites/additional screens, derived damage/type/PP values, stale saved-note channels and real TDAT persistence UNKNOWN / NOT_RUN; complete API/wrapper sufficiency unproved. | Accepted T4 then actual standard Tracker presentation and suppression of all affected derived/persisted consumers; later user decision for personal notes. |
| [#695](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/695) / [#500](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/500) — T6/parent | User-owned Control/Casual NatDex/IronMON NatDex E2E NOT_RUN; parent integration unaccepted. | Accepted T5 then required 3-variant matrix, clear limitations, no unresolved wrong-data S0/S1-equivalent defect; CONTROL accepts T6/#500. |
| [#501](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/501) — support/freeze | Final supported host/Tracker/extension configuration and freeze NOT_ESTABLISHED. | Only after #499 and #500 acceptance: explicit support scope, revisions, exclusions and change-control decision. |

Safe RAM requires a public source symbol applicable to the exact locked
configuration, correct EWRAM/IWRAM domain-relative location, bounded read and
context predicate. Source ABI facts do not establish live pointers/repointed
tables. No guessing, scanning, private manifest extraction or NatDex marker
reuse. Missing provenance blocks B1-09 and aggregate B1 PASS, not an observed
BizHawk FAIL. Output names/headers, plausible data, matching source pins or
schema-valid JSON cannot prove loaded-output/session association; reset/reload/
output switch invalidates it. UNKNOWN dependencies suppress values and derived
consumers immediately; no silent stock or source-baseline substitution.

Lua 5.1 compatibility remains NOT_RUN; Lua 5.4 mock PASS does not validate the
selected host/backend. Real attack observation, randomized ability names/move
properties, normal host events, actual notes/TDAT retention/reassociation and
screen coverage remain unproved. #713 quarantines synthetic historical input;
it neither deletes nor migrates real notes. Personal-note preservation/review/
migration requires a later user decision and separate runtime evidence.

## STOP/GO decision and final handoff boundary

- **GO — documentation review only:** exact one-added-file #715 diff, clean
  tracked workspace/components, unchanged ten pins, safety/whitespace/link/
  Markdown checks and source-faithful B1 review support CONTROL review. PR
  evidence supplies exact base/head/tree and final check results. #715 changes
  no existing file, including B1 or production extension.
- **STOP — receiving or runtime:** unexpected branch/worktree/revision/pin,
  real competing eligible active contract, protected boundary, insufficient
  identity/address evidence, unobserved required callback, unsafe write or
  material/blocking defect prevents dependent GO. Report sanitized reason to
  CONTROL, leave affected cases NOT_RUN (executed contradictions FAIL). No
  silent repair, broader scope or blanket B1 PASS.
- **CONFLICT — material runbook defect:** report to CONTROL and await its
  separately bounded repair contract; leave Mac exit unaccepted. Unset optional
  Project metadata alone is not this conflict and is not a STOP reason.

No ROM/save/state/build/tool-binary, private path, local manifest, offsets.ini,
*.local.json, .env, secret or personal TDAT access/transfer is authorized.
No emulator, installation, synthetic development or code change occurred in
#715. Old mock/allowlist suites, Clang generation, Lua compatibility execution,
Java/C/build/runtime/UI/TDAT/E2E tests are **NOT_RUN in this DOC_ONLY contract**;
their historical evidence retains its own revisions. New Gen9 mechanics are
not pilot obligations; `UPSTREAM_CONTRIBUTION=DEFERRED`.

Only after CONTROL exact-revision review, confirmed **user merge** and CONTROL
post-merge verification may it establish:

```text
MAC_SOURCE_PREPARATION_HANDOFF_READY = PASS_DOC_ONLY
```

This proposed marker is **not yet established** by authoring this document.
It concludes Mac source/mock/documentation preparation only; production,
BizHawk readiness, active Tracker support and final freeze remain denied or
unproved. CONTROL closes only #715 after acceptance; no auto-closure or agent
merge. No further Mac tasks without a concrete new safety finding.

**Exactly one next operational trigger:** the user tells CONTROL that
Linux/BizHawk is actually available, without private data. CONTROL then resumes
existing #689 for fresh host preflight and user-owned B1 using its existing
sanitized form. Until that signal, wait; no execution request or background
work is scheduled.
