# B1 — Linux / BizHawk host acceptance runbook

Contract: [#689](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/689),
under [#499](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/499).
**CONFIRMED USER DECISION:** the 2026-10-08 Mac-first exception authorizes
this document only. **INTENDED FUTURE STATE:** user-owned Linux execution.
Current host gate: `PENDING_LINUX_HOST / NOT_RUN`;
`BIZHAWK_LOCKED_PILOT_READY = NOT_RUN`. No emulator was run on macOS.

## Revision identity and source expectations

Keep the accepted product/output basis separate from the preparation revision:

| Role | Exact revision |
| --- | --- |
| Locked product Workspace | `3bdfe9919afc0b7bea55c79f37285e832be495c3` |
| Locked product tree | `f6bc65355811d7de153a91091b223fec9b50991e` |
| CFRU | `e68a701aa4e68733ef8ad1e7cadb68825c0d16c2` |
| DPE | `d887185de1f6ae6a78e85c4311bbadde17041d00` |
| UPR-FVX | `4670a5413104ec02bc08c09ff584470a8a6cb7bd` |
| Standard Ironmon Tracker reference | `c450ecaee2d8131a2789bb656e3be792a93712fb` — v9.3.1 |
| NatDexExtension pattern reference | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| Verified preparation `main` (2026-10-08) | `64f3bbb15a778eaed1f529f80b429016187cdcbb` |
| Preparation tree | `73e1f5bdd77b4d8d19bcdfbbc7c83ab8b08c67a1` |

A later documentation/harness commit or merge is not retroactive runtime
evidence. Record the runbook commit actually used separately in the results.
The current Issue contract supersedes older pending milestones/pins in general
docs; [README.md](README.md) and [PROFILE_CONTRACT.md](PROFILE_CONTRACT.md)
explain the identity and trust boundaries. B1 is host acceptance, not proof of
loaded-output detection, Tracker decoding, field confidence or UI correctness.

**CONFIRMED SOURCE EXPECTATIONS, not live PASS:** pinned Tracker
[README](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/README.md)
requires BizHawk >=2.8 and identifies Lua 5.1 for 2.8, Lua 5.4 for 2.9;
extensions must support both. Pinned
[Main.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Main.lua)
(`Main.Version`, `GetBizhawkVersion`, `SetupEmulatorInfo`, `Run`) classifies
2.10+/future versions and uses `client.getversion`, `emu.frameadvance`,
`event.onexit` and `event.onconsoleclose`. Version classification alone is not
compatibility. No exact Linux build, GBA core or Lua engine setting is accepted.
No NLua/LuaInterface switch is prescribed by T0: record the actual selection.

Pinned [Memory.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Memory.lua)
maps reads to `memory.read_u8/read_u16_le/read_u32_le(address, domain)`;
EWRAM/IWRAM addresses require explicit domain-relative offsets. Pinned
[Program.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/Program.lua)
(`mainLoop`, `update`, `changeGameSettingForLR`) and
[CustomCode.lua](https://github.com/besteon/Ironmon-Tracker/blob/c450ecaee2d8131a2789bb656e3be792a93712fb/ironmon_tracker/CustomCode.lua)
drive per-frame hooks and 30-frame program/battle updates. B1 tests the host
primitives; actual Tracker hook/consumer behavior remains T2–T6 evidence.

## User preflight — only after Linux access is confirmed

1. Confirm Linux availability to CONTROL before runtime work. Use an existing,
   user-owned Linux/BizHawk setup and the accepted local locked-pilot output.
   This preparation does not authorize downloads, installs or builds. Record
   OS/distribution/release/architecture (e.g. `uname -srm`, without hostname),
   actual BizHawk version/build from About and `client.getversion()`, selected
   GBA core/version, Lua engine/backend setting and `_VERSION`.
2. Record all product pins above, exact selected public profile/schema ID,
   relevant configuration and variant: Control, Casual NatDex or IronMON NatDex.
   Record the runbook/documentation commit separately. The user must establish
   the local output's association with the accepted revision/profile; return
   only the sanitized method/result. Names, headers, plausible data or a JSON
   import are insufficient. Unknown identity blocks dependent tests. No local
   manifest inspection (`offsets.ini`, `*.local.json`) is part of this protocol.
3. Leave Tracker, all extensions and other scripts unloaded. Disable cheats,
   RAM freezes, memory-writing helpers and automatic output switching. Record
   normal-speed/throttle, audio/video, controller mapping and focus settings;
   use ordinary gameplay input with no turbo/rewind/movie/state manipulation.
   Do not invent a mandatory core or compatibility setting. Any change requires
   a separately recorded configuration and repetition of affected cases.
4. For later Tracker use, explicitly disable **Override Button Mode to LR**:
   `Program.changeGameSettingForLR` can call `Memory.writebyte`. B1 does not
   launch Tracker or permit any `Memory.write*` / `memory.write*` call. No game,
   Tracker or extension file modification and no stock fallback are authorized.
5. Before the RAM case, obtain a separately proven **public** safe RAM symbol
   and immutable source locator applicable to the locked build/configuration.
   Prove domain, domain-relative offset, allowed width/range, alignment and an
   expected sanity predicate in the chosen game context. No pointer guessing,
   scans, NatDex markers, private address extraction or memory writes. **UNKNOWN:**
   this runbook establishes no safe address; it supplies no numeric candidate.
   Without that proof, stop the RAM case as `NOT_RUN / SAFE_RAM_UNPROVEN`.

Protected ROMs, saves, states, builds, binaries and runtime data remain local
and outside Git, prompts and agent context. Ordinary in-game save/reload below
is user-owned future acceptance only. Share no private paths, artifact hashes,
screenshots, raw memory, logs, controller identifiers or secrets.

## Manual test sequence and expected outcomes

Run in order on one recorded host/core/profile configuration. Keep observations
local and return only the sanitized form below. Missing prerequisites mean
`NOT_RUN`; an executed case contradicting its expectation means `FAIL`.

| ID | User steps | Expected result / stop condition |
| --- | --- | --- |
| B1-01 | Open the accepted output in BizHawk with no Tracker/scripts; boot and select Fresh New Game through the locked pilot's Mom/Lab/starter flow. | Title/new game and normal handoff complete without crash, hang or display corruption. Stop on identity uncertainty or blocking fault. |
| B1-02 | Exercise mapped directions, A/B, Start/Select and applicable L/R in gameplay/menus; test the selected keyboard/controller and normal focus return. | Correct, repeatable input with no stuck/missed controls material to Tracker use. Record tested device class only. |
| B1-03 | Save through the game menu; close/reopen the same output and Continue from its ordinary in-game save. Do not use emulator states. | Progress/location/party visibly persist; gameplay/input resume normally. Stop on save loss/corruption. |
| B1-04 | Enter and finish a representative wild encounter using normal input; return to the overworld. | Battle entry, actions and exit remain usable and stable. No Tracker-data claim. |
| B1-05 | Enter and finish a representative trainer battle; return to the overworld. | Trainer flow, actions and exit remain usable and stable. No team-decoding or balance claim. |
| B1-06 | Observe normal-speed audio/video/timing and controls throughout B1-01–05, including menus and battle transitions. | No timing, audio, display or control anomaly material to Tracker use. Record observation scope; no universal performance claim. |
| B1-07 | Open Lua Console; load the local copy of the inline host probe below and record actual version/Lua metadata. | Script loads and runs without API/syntax errors on the actual engine. Source expectations alone do not pass this case. |
| B1-08 | Run the finite frame probe, then the lifecycle probe; stop the script and separately close/reopen Lua Console while it is running. | Frame-driven per-frame/30-frame callbacks progress; exit and console-close callbacks actually fire, with clean recovery. Registration alone is insufficient; unobservable callbacks are NOT_RUN. |
| B1-09 | After separate safe-RAM proof, confirm the required EWRAM/IWRAM domain exists; pause at the proven context and perform only the bounded read described below. | Explicit domain/offset and read width work; value satisfies the proven predicate. An exception, bad domain or contradictory value fails; missing provenance is NOT_RUN. Never print the value. |

The following inline examples are instructions for future user execution,
not a repository helper or an executed test. Copy only into a user-local scratch
script outside the repository; no protected input is supplied to an agent.
For API signatures, consult the actual host's Lua Console Help / Lua Functions
List. The public [BizHawk Lua API reference](https://tasvideos.org/Bizhawk/LuaFunctions)
documents domain-relative reads and lifecycle callbacks; it is not proof that
a selected older Linux build implements them successfully.

B1-07/08 finite host probe (Lua 5.1/5.4 syntax, no memory access):

```lua
assert(client and type(client.getversion) == "function")
assert(emu and type(emu.frameadvance) == "function")
assert(event and type(event.onexit) == "function")
assert(type(event.onconsoleclose) == "function")
print("B1 host version: " .. client.getversion())
print("B1 Lua: " .. _VERSION)
event.onexit(function() print("B1 exit callback observed") end, "B1 exit")
local eachFrame, updates = 0, 0
local function perFrame() eachFrame = eachFrame + 1 end
local function periodicUpdate() updates = updates + 1 end
for frame = 1, 60 do
    emu.frameadvance()
    perFrame()
    if frame % 30 == 0 then periodicUpdate() end
end
assert(eachFrame == 60 and updates == 2)
print("B1 finite frame/update probe complete")
```

Observe actual emulation progression as well as completion. These local
callbacks model the source cadence; they do not exercise Tracker extension
hooks. For lifecycle testing, run a separate local script registering
`event.onexit(function() print("B1 exit observed") end, "B1 exit")` and
`event.onconsoleclose(function() print("B1 console-close observed") end, "B1 close")`,
then `while true do emu.frameadvance() end`. Stop it through Lua Console to
check exit; restart it and close the console to check console-close. Require
an observable callback marker using the host's local console facilities;
if closing hides the marker and it cannot be observed, record that subcase
`NOT_RUN`, not PASS. Reopen the console and verify normal gameplay recovery.
Stop/remove each probe before the next; do not leave duplicate registrations.

B1-09 remains blocked until safe-RAM provenance exists. Enumerate domain names
only with `memory.getmemorydomainlist()`; membership must be confirmed before
checking `memory.getmemorydomainsize(domain)` (size alone is not domain proof).
Use the proven explicit domain-relative offset with
`memory.read_u8(offset, domain)`; use `read_u16_le` or `read_u32_le` only if that
exact wider range/alignment is also proven. Inspect the predicate locally,
discard the value and record only read/predicate success or sanitized failure.
No generic API success certifies an address, layout or Tracker reader.

## Sanitized results form — blank, all runtime cases NOT_RUN

Fill metadata once; every row inherits it. Split rows by subcase where needed
so an unobserved event or untested control cannot inherit another subcase's PASS.

- Date/run label: `<UTC / public label>`
- Host OS/release/architecture: `UNKNOWN`; BizHawk exact build: `UNKNOWN`
- GBA core/version: `UNKNOWN`; Lua backend/setting and `_VERSION`: `UNKNOWN`
- Safe applicable settings/controller class: `<sanitized settings or UNKNOWN>`
- Tested product Workspace/tree and CFRU/DPE/UPR-FVX: `<exact revisions above, confirm>`
- Selected profile/schema/configuration/variant: `UNKNOWN`; identity proof result: `NOT_RUN`
- Tracker/reference pins: `<exact pins above>`; runbook commit used: `<exact SHA>`
- Safe RAM public source locator/domain/width/predicate proof: `UNPROVEN`
- Blockers: `PENDING_LINUX_HOST`; RAM additionally `SAFE_RAM_UNPROVEN`

| Case / steps above | PASS / FAIL / NOT_RUN | Defect severity | Observed outcome (sanitized; no values/logs) | Decision / stop rule |
| --- | --- | --- | --- | --- |
| B1-01 boot/new game | NOT_RUN | — | — | Await Linux/identity preflight |
| B1-02 input/controller | NOT_RUN | — | — | Await prerequisites |
| B1-03 save/reload | NOT_RUN | — | — | Await prerequisites |
| B1-04 wild battle | NOT_RUN | — | — | Await prerequisites |
| B1-05 trainer battle | NOT_RUN | — | — | Await prerequisites |
| B1-06 audio/video/timing/control | NOT_RUN | — | — | Await prerequisites |
| B1-07 Lua console/script | NOT_RUN | — | — | Await host metadata |
| B1-08 frame/update/exit/console-close | NOT_RUN | — | — | Require all subcases observed |
| B1-09 read-only RAM/domain sanity | NOT_RUN | — | — | Stop until safe public proof |
| BIZHAWK_LOCKED_PILOT_READY | NOT_RUN | — | — | CONTROL assessment required |

Severity: `BLOCKING` for crash/hang, save loss, unsafe access/write or unusable
required API/control; `MATERIAL` for timing/audio/video/control defects affecting
Tracker use; `MINOR` for an observed issue without that impact. Missing host or
proof is a blocker with `NOT_RUN`, not an observed emulator defect. Stop on
unsafe behavior or a blocking/material defect, leave dependent rows `NOT_RUN`,
and report sanitized scope/reason. Do not repair components or expand scope.

Only all required B1 cases PASS, exact revision/profile/configuration binding,
and no unresolved material defect can support CONTROL's assessment of
`BIZHAWK_LOCKED_PILOT_READY = PASS`. With accepted T0, that permits CONTROL to
close #689/#499 and unlock the Linux-dependent Tracker work. The Phase A
runbook itself is documentation readiness only. #691–#694 Phase B still need
their own live activation, party/battle fidelity and UI evidence; #695 still
needs Control/Casual/IronMON E2E. B1 never grants Tracker production activation,
#500 acceptance or #501 freeze. Any FAIL or required NOT_RUN keeps #499 open.
